# Power BI — Dashboard Spec (market-evidence, brief-compliant)

> `dashboard/dashboard_spec.md` — the **graded** `.pbix`. Per the Project 5 brief, this is an
> **evidence dashboard** that helps Cleo decide *whether to invest* — it shows **market /
> sector / adoption / cost / risk** metrics, **not** an operational tool. ("The goal is not to
> build an AI tool.") The live web cockpit (`deploy/`) is a **bonus demo** of the piloted tool,
> presented separately.

Theme: deep red `#8C1C2B`, cream `#FBF8F2`, gold `#A8884F`. Communication-layer: clean,
CEO-readable, 5–7 key metrics, clarity over density.

## Data source (simple — public evidence)
Primary table: **`data/processed/ai_adoption_evidence.csv`** (real, cited public figures —
Eurostat, HOTREC, STATEC, KPMG, EU Commission). Columns: `id, pillar, metric, value_num,
value_text, unit, geography, year, source, source_type`.
Plus: **`data/processed/hype_vs_evidence.csv`** (claim / evidence / verdict) for the table visual.
Optional: a few **cost assumptions** as What-If parameters (labelled estimates) for the ROI cards.

> No operational/star schema needed here — the evidence table drives the cards and bars via
> simple measures (one card per metric, filtered by `metric`).

### Evidence card measure pattern (DAX)
```DAX
EU AI Deployment % =
CALCULATE ( MAX ( Evidence[value_num] ),
    Evidence[metric] = "Hospitality enterprises deploying AI" )
```
Duplicate and swap the `metric` filter for each card. For text values (e.g. "2028–2029")
use `MAX ( Evidence[value_text] )`.

## Page 1 · The Decision
**Question:** "Should we invest in AI for the finance back-office — now, later, or as a pilot?"
| Visual | Type | Content |
|---|---|---|
| 6 evidence KPI cards | Card | EU AI deployment **~6%** · W-Europe GOP **33.3%** · workforce gap **~10%** · manual vs auto invoice **€12→€3** · AP-automation market **12.8% CAGR** · EU e-invoicing mandate **2030** |
| Recommendation | Text box | 🟡 **Run a pilot** — don't wait, don't yet invest at full scale |
| Decision logic | 3 cards / shapes | Pressure (margins + talent) → Opportunity (back-office cost) → **Pilot** |
| "How to read this" | Text box | one line: every metric is public & cited; sources on page 3 |

## Page 2 · Market & Sector Evidence (is the pressure real?)
**Question:** "Why would a 5★ hotel even consider this?"
| Visual | Type | Content |
|---|---|---|
| Margin pressure | Bar/cards | W-Europe GOP 33.3% · payroll >35% of operating costs |
| Talent crisis | Bar/cards | workforce gap ~10% · vacancy ~4% · digital-skills gap <15% |
| Luxembourg context | Cards | 216 hotels · ~7,800 rooms · 1.4 M arrivals (STATEC) |
| Takeaway | Text box | revenue no longer expands margin → efficiency is the lever; can't cut staff |

## Page 3 · Adoption vs Hype (the heart of the brief)
**Question:** "Is AI adoption credible here, or is it hype?"
| Visual | Type | Content |
|---|---|---|
| The contrast | 2 big cards | "98% say adopted" vs **~6% actually deploy** (Eurostat) |
| Where AI is real | Bar | back-office 64% · energy 54% · revenue 53% · guest 9% |
| Trust–reliance gap | Cards | trust 6.6/10 · reliance 4.7/10 · formal strategy 8% |
| **Hype vs evidence** | **Table** | `hype_vs_evidence.csv`: claim → evidence → verdict (colour `verdict`) |
| Source transparency | Donut/bar | count of sources by `source_type` (official/industry/vendor/forecast) |

## Page 4 · Opportunity, Cost & Recommendation (invest / wait / pilot)
**Question:** "What's the first move, what does it cost, what's the return?"
| Visual | Type | Content |
|---|---|---|
| The opportunity | Bar | manual vs automated: cost €12→€3, time 15→3 min |
| Why now | Timeline | ViDA 2025 → Belgium/LU 2026 → France 2027 → LU B2B 2028–29 → EU 2030 (Regulatory rows) |
| **Full-tool value stack** | **Waterfall** | `value_stack.csv`: AP automation €42k + manual-matching time €26k + 3-way recovery €10k + inventory waste €9k + stock-entry labour €19.5k − run cost €13k → **~€93.5k/yr net · ~1.2 FTE** (one-off €15k WC shown separately; FTE from labour pools only) |
| Cost & ROI | Cards | pilot ~€20k · **~€106.5k/yr gross · ~€93.5k/yr net · ~1.2 FTE** · payback < 12 mo (labelled estimates — `cost_estimation/`) |
| Opportunity sizing | What-If slicers + card | Volume × Touchless target → projected AP saving (decision input, optional) |
| Recommendation | Text box | 🟡 PILOT + go/no-go gate (touchless ≥65%, accuracy ≥90% at real volume) |

> **Value-stack integrity (say this at the pitch):** the four benefit pools are **distinct, not
> overlapping** — processing time (AP) ≠ error recovery (3-way match) ≠ stock waste ≠ stock-entry
> labour. Every figure is a **conservative, assumption-based estimate** with its basis in
> `value_stack.csv` / `cost_estimation/cost_analysis.md`, to be replaced by the client's real data.
> The €15k working-capital release is a **one-off cash effect**, kept out of the recurring total.

### Building the waterfall (Power BI)
Load `data/processed/value_stack.csv`. Filter to `type = "recurring"`. Native **Waterfall**
visual → Category = `component`, Y = `annual_value_eur` (the −€13k run cost shows as the only
downward step → the bar lands on the **net** figure). Add two cards: **Gross benefit**
`CALCULATE(SUM(value_stack[annual_value_eur]), value_stack[annual_value_eur] > 0, value_stack[type]="recurring")`
and **Net benefit** `CALCULATE(SUM(value_stack[annual_value_eur]), value_stack[type]="recurring")`.

## Cost What-If (optional, labelled estimates)

Parameters: **Volume (monthly)** 50–1200 (def 420), **Touchless target** 0.40–0.95 (def 0.75),
**Finance rate €/h** 30–70 (def 45), **Manual minutes** 5–30 (def 15). Then:
```DAX
Manual Cost = ('Manual Minutes'[Value]/60) * 'Finance Rate'[Value] + 0.75
Auto Min    = 'Touchless Target'[Value]*2.5 + (1-'Touchless Target'[Value])*9
Auto Cost   = (Auto Min/60) * 'Finance Rate'[Value] + 0.8
Projected Annual Saving = ([Manual Cost]-[Auto Cost]) * 'Volume'[Value] * 12
```
(Same logic as the corrected API calculator — manual & auto both derive from the rate.)

## Build order
1. Load `ai_adoption_evidence.csv` + `hype_vs_evidence.csv` (Text/CSV). No relationships needed.
2. Add the evidence-card measures (one per metric) + the 4 What-If parameters.
3. Build pages 1→4; apply the red/cream/gold theme JSON.
4. Centrepiece for the lab: **the 98%-vs-6% contrast + the hype-vs-evidence table** — that *is*
   the "separate hype from value" deliverable, rendered.

## Framing at the meeting (one sentence)
> "This dashboard is my **evidence** that AI adoption is credible *here* — public data on
> pressure, adoption, cost and regulation — leading to a **pilot** recommendation. And here's
> a quick **demo of what that piloted tool would look like** [switch to the web cockpit]."
