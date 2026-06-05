# Power BI — Live API Connection (Power Query)

> `dashboard/live_api_connection.md` — paste-ready Power Query (M) to wire the `.pbix` to the
> deployed AP API, with **auto-login on every refresh**. Plus the static-CSV fallback.

## Mode A — Live API (auto-login → Bearer)

Set two parameters first (*Home ▸ Manage Parameters*): `ApiBase` (your Railway API URL, e.g.
`https://ap-api-production.up.railway.app`), `ApiUser`, `ApiPassword`.

### Query: `Token` (gets a fresh bearer token each refresh)
```m
let
    Body = "username=" & ApiUser & "&password=" & ApiPassword,
    Response = Web.Contents(
        ApiBase,
        [
            RelativePath = "auth/token",
            Headers = [#"Content-Type" = "application/x-www-form-urlencoded"],
            Content = Text.ToBinary(Body)
        ]
    ),
    Token = Json.Document(Response)[access_token]
in
    Token
```

### Query: `Fact_Invoices` (the joined fact table, row-level)
```m
let
    Response = Web.Contents(
        ApiBase,
        [
            RelativePath = "api/invoices",
            Query = [ limit = "100000" ],
            Headers = [ Authorization = "Bearer " & Token ]
        ]
    ),
    Data  = Json.Document(Response),
    Table = Table.FromList(Data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expand = Table.ExpandRecordColumn(Table, "Column1",
        {"invoice_id","vendor_name","department","period","channel","net_amount",
         "ai_confidence","proposed_account","final_account","touchless",
         "human_corrected","account_correct","handling_minutes","vat_non_deductible"}),
    Typed = Table.TransformColumnTypes(Expand, {
        {"net_amount", type number}, {"ai_confidence", type number},
        {"handling_minutes", type number}, {"period", type date},
        {"touchless", type logical}, {"human_corrected", type logical},
        {"account_correct", type logical}, {"vat_non_deductible", type logical}})
in
    Typed
```

### Query: `Evidence`
```m
let
    Response = Web.Contents( ApiBase,
        [ RelativePath = "api/evidence", Headers = [ Authorization = "Bearer " & Token ] ]),
    Data  = Json.Document(Response),
    Table = Table.FromList(Data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expand = Table.ExpandRecordColumn(Table, "Column1",
        {"id","pillar","metric","value_num","value_text","unit","geography","year","source","source_type"}),
    Typed = Table.TransformColumnTypes(Expand, {{"value_num", type number}, {"year", Int64.Type}})
in
    Typed
```
> `Dim_Vendor`, `Dim_Account`, `Dim_Date` likewise: in live mode build them from
> `Fact_Invoices` (or load the small CSVs statically — dimensions rarely change).

### Refresh gotchas (important)
- **Credentials:** the first time, Power BI asks how to authenticate the web source — choose
  **Anonymous** (our auth lives in the request header, not in Power BI's credential store).
- **Dynamic URL + scheduled refresh:** always use `Web.Contents(BaseUrl, [RelativePath=…,
  Query=…])` — *never* string-concatenate the full URL — or the Power BI Service refuses to
  refresh. The pattern above is already compliant.
- **Privacy levels:** set the source to *Public/Organizational* to avoid the formula-firewall
  blocking the `Token` → data chain. If you hit a firewall error, tick *Ignore Privacy Levels*
  for this file (*Options ▸ Current File ▸ Privacy*).

## Mode B — Static CSV (safe fallback / lab-only)

*Get Data ▸ Text/CSV* on each `data/raw/*.csv`. Build `Fact_Invoices` by merging
`ap_entries.csv` ⟕ `invoices.csv` on `invoice_id` (for `net_amount`) ⟕ `vendors.csv`
(for `department`). Set the four flag columns to **True/False (Logical)**. Same model, same
measures — only the source differs.

## Why both
The static file is the no-deploy safety net for grading day. The live API is the "wired to a
real backend, auto-refreshing" version that matches the web cockpit number-for-number,
because both read the same source of truth.
