# Power BI — Measure Layer (DAX)

> `measures/measures_dax.md` — every KPI as plain-English **and** copy-paste DAX. Put them
> all in a dedicated `_Measures` table. Anchored to AP / Procure-to-Pay logic (the finance
> equivalent of Eugen's SCOR layer), with USALI departments as the analytical cut.

> Boolean note: filters below assume the flag columns are typed **Boolean**. If a column is
> text, replace `= TRUE()` with `= "True"`.

## 1 · Operational KPIs

```DAX
Total Invoices = COUNTROWS ( Fact_Invoices )

Net Spend = SUM ( Fact_Invoices[net_amount] )

Touchless Rate =
DIVIDE (
    CALCULATE ( [Total Invoices], Fact_Invoices[touchless] = TRUE () ),
    [Total Invoices]
)

Account Accuracy =
DIVIDE (
    CALCULATE ( [Total Invoices], Fact_Invoices[account_correct] = TRUE () ),
    [Total Invoices]
)

Exception Rate =
DIVIDE (
    CALCULATE ( [Total Invoices], Fact_Invoices[human_corrected] = TRUE () ),
    [Total Invoices]
)

Avg Handling Minutes = AVERAGE ( Fact_Invoices[handling_minutes] )

e-Invoice Share =
DIVIDE (
    CALCULATE ( [Total Invoices], Fact_Invoices[channel] = "einvoice" ),
    [Total Invoices]
)
```

## 2 · Baseline assumptions (edit here — every € flows from these)

```DAX
Manual Cost per Invoice = 12        -- € (HighRadius/Quadient, USD-derived, indicative)
Manual Minutes = 15                 -- min (Artsyl)
Processing Surcharge = 0.8          -- € software/compute per invoice
```
> For the finance loaded rate and the projection volume, use **What-If parameters** (§4) so
> Cleo can move them live: *Modeling ▸ New parameter*. Create **Finance Rate** (30–70, def 45),
> **Volume (monthly)** (50–1200, def 420), **Touchless Target** (0.40–0.95, def 0.75),
> **Manual Cost** (6–20, def 12). Each creates a `<Name>[<Name> Value]` measure.

## 3 · Realised savings (on the pilot data, current filter)

```DAX
Auto Cost per Invoice =
( [Avg Handling Minutes] / 60 ) * 'Finance Rate'[Finance Rate Value] + [Processing Surcharge]

Cost Saved =
( [Manual Cost per Invoice] - [Auto Cost per Invoice] ) * [Total Invoices]

Minutes Saved = ( [Manual Minutes] - [Avg Handling Minutes] ) * [Total Invoices]

Hours Returned = DIVIDE ( [Minutes Saved], 60 )

FTE Equivalent = DIVIDE ( [Hours Returned], 1600 )   -- ~1,600 productive h / FTE / yr
```

## 4 · Projected savings (the opportunity calculator — mirrors the web cockpit)

```DAX
Projected Auto Minutes =
    'Touchless Target'[Touchless Target Value] * 2.5
  + ( 1 - 'Touchless Target'[Touchless Target Value] ) * 9.0

Projected Auto Cost =
( [Projected Auto Minutes] / 60 ) * 'Finance Rate'[Finance Rate Value] + [Processing Surcharge]

Projected Saving per Invoice = 'Manual Cost'[Manual Cost Value] - [Projected Auto Cost]

Projected Annual Saving =
[Projected Saving per Invoice] * 'Volume'[Volume Value] * 12

Projected Hours Returned =
DIVIDE ( ( [Manual Minutes] - [Projected Auto Minutes] ) * 'Volume'[Volume Value] * 12, 60 )

Projected FTE Equivalent = DIVIDE ( [Projected Hours Returned], 1600 )
```
> These four cards + the slider parameters reproduce the cockpit's page II inside Power BI.

## 5 · Decision flag (CEO traffic-light — the honest read)

```DAX
Touchless Quality =
VAR r = [Touchless Rate]
RETURN
SWITCH ( TRUE (),
    r >= 0.70, "🟢 strong — pilot is converting",
    r >= 0.55, "🟡 promising — keep tuning",
    "🔴 below target — investigate"
)
```

## 6 · Supplier concentration (resilience / savings levers)

```DAX
Top Supplier Share =
DIVIDE (
    MAXX ( VALUES ( Dim_Vendor[vendor_name] ), [Net Spend] ),
    [Net Spend]
)

Vendor HHI =                                   -- Herfindahl concentration index
SUMX ( VALUES ( Dim_Vendor[vendor_name] ),
       VAR s = DIVIDE ( [Net Spend], CALCULATE ( [Net Spend], ALL ( Dim_Vendor ) ) )
       RETURN s * s )
```

## 7 · Evidence cards (disconnected Evidence table — Adoption page)

```DAX
EU Hospitality AI Deployment =          -- the "~6%" stat
CALCULATE ( MAX ( Evidence[value_num] ),
    Evidence[metric] = "Hospitality enterprises deploying AI" )

Western Europe GOP Margin =
CALCULATE ( MAX ( Evidence[value_num] ),
    Evidence[metric] = "Western Europe GOP margin" )

Workforce Gap =
CALCULATE ( MAX ( Evidence[value_num] ),
    Evidence[metric] = "Hospitality workforce gap" )
```
> Pattern: one card per headline stat; duplicate the measure and swap the `metric` filter.
