# Power BI — Data Model

> `dashboard/data_model.md` — the star schema behind the Power BI report. Two source modes
> (static CSV / live API) feed the **same** model, so the measures and visuals never change.

## Tables (star schema)

```
                    ┌────────────────┐
                    │   Dim_Date     │
                    └───────┬────────┘
                            │ date
        ┌──────────────┐    │    ┌──────────────┐
        │  Dim_Vendor  │    │    │  Dim_Account │
        └──────┬───────┘    │    └──────┬───────┘
       vendor_id│           │           │account
                ▼           ▼           ▼
              ┌──────────────────────────────┐
              │       Fact_Invoices          │   (grain: 1 row = 1 invoice)
              └──────────────────────────────┘

        ┌──────────────────────┐
        │  Evidence (market)   │   disconnected — feeds the Adoption page only
        └──────────────────────┘
```

### Fact_Invoices — grain: one supplier invoice
| Column | Type | Notes |
|---|---|---|
| invoice_id | text | key |
| vendor_id | text | → Dim_Vendor |
| final_account | text | → Dim_Account (the validated GL account) |
| invoice_date / period | date | → Dim_Date |
| net_amount | decimal | USALI spend |
| handling_minutes | decimal | time to process |
| ai_confidence | decimal | 0–1 |
| channel | text | pdf / email / einvoice |
| touchless | **boolean** | straight-through (no human correction) |
| human_corrected | **boolean** | routed to / corrected by a human |
| account_correct | **boolean** | AI proposal matched the validated account |
| vat_non_deductible | **boolean** | tricky VAT → human review |
| department | text | USALI dept (denormalised for convenience) |

> ⚠️ In **static (CSV) mode**, set the four flag columns to **Boolean** in Power Query
> (they import from Python as `True`/`False`). In **live API mode** they arrive as JSON
> booleans already. If any flag stays *text*, change the DAX filters from `= TRUE()` to
> `= "True"`.

### Dim_Vendor (`vendors.csv` / `/api/...`)
vendor_id, vendor_name, default_account, vat_treatment, channel, department

### Dim_Account (`chart_of_accounts.csv`)
account, label, type, department (USALI)

### Dim_Date (`dim_date.csv`)
date, year, month, month_name, period, quarter, day_of_week — **mark as Date table**.

### Evidence (`ai_adoption_evidence.csv` / `/api/evidence`)
id, pillar, metric, value_num, value_text, unit, geography, year, source, source_type.
Disconnected (no relationship) — drives the cards/timeline on the Adoption page.

## Relationships
- `Fact_Invoices[vendor_id]` → `Dim_Vendor[vendor_id]` (many-to-one, single)
- `Fact_Invoices[final_account]` → `Dim_Account[account]` (many-to-one, single)
- `Fact_Invoices[invoice_date]` → `Dim_Date[date]` (many-to-one, single)

## Two source modes
1. **Static CSV (primary / safe):** Get Data ▸ Text/CSV ▸ `data/raw/*.csv`. In static mode,
   `Fact_Invoices` is `ap_entries.csv` **merged with** `invoices.csv` on `invoice_id`
   (to bring in `net_amount`) and with `vendors.csv` for `department`.
2. **Live API (wow factor):** follow `dashboard/live_api_connection.md` — `/api/invoices`
   already returns the joined fact table; `/api/evidence` returns the market table. Auto-login
   on every refresh. Switch modes by swapping the query source; the model stays identical.
