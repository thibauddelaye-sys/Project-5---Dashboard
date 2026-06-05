# Dashboard Documentation

> `dashboard/dashboard_documentation.md` — documents the **graded** dashboard: the Power BI
> **evidence dashboard**. Per the Project 5 brief, it answers *whether AI adoption is worth
> investing in* using public market/adoption/cost/risk evidence — it is **not** an operational
> tool ("the goal is not to build an AI tool"). A bonus live web cockpit demos the piloted tool.

## Audience & purpose
Built for **Cleo**, a non-technical CEO. Communication-layer: 5–7 decision-relevant metrics,
clarity over density, every number public and cited. One question per page — invest/wait/**pilot**.

## Data sources (public, cited)
- **`data/processed/ai_adoption_evidence.csv`** — 32 cited figures across 6 pillars (margin,
  talent, AP cost, adoption, regulatory, Luxembourg sizing). Sources: Eurostat, HOTREC, STATEC,
  KPMG, EU Commission, plus clearly-labelled vendor/forecast figures. Each row carries its
  `source` and `source_type`.
- **`data/processed/hype_vs_evidence.csv`** — claim → evidence → verdict, for the hype table.
- **Cost assumptions** — labelled estimates exposed as What-If parameters (see `cost_estimation/`).

## Pages & key metrics
| Page | Question | Metrics |
|---|---|---|
| 1 · The Decision | invest, wait, or pilot? | EU AI deployment ~6% · W-Europe GOP 33.3% · workforce gap ~10% · invoice cost €12→€3 · AP market 12.8% CAGR · e-invoicing 2030 |
| 2 · Market & Sector Evidence | is the pressure real? | margins, payroll share, workforce gap, vacancy, LU sizing |
| 3 · Adoption vs Hype | is it credible or hype? | 98% vs ~6%, back-office 64% vs guest 9%, trust/reliance, hype-vs-evidence table, source-type mix |
| 4 · Opportunity, Cost & Reco | first move, cost, return? | manual vs auto, ViDA timeline, pilot ~€20k / ~€42k-yr / payback ~12 mo, invest/wait/pilot |

## Metric selection rationale (why these)
Each metric maps to one leg of Cleo's decision: **is there pressure** (margins, talent), **is
adoption real or hype** (Eurostat 6% vs headlines), **is the opportunity worth it** (AP cost
pool, ROI), **why now** (e-invoicing regulation). Operational tool KPIs (touchless rate, etc.)
are deliberately *out* of the graded dashboard — they live in the bonus cockpit.

## Visualization choices
Cards for headline single figures (CEO-glanceable); bars for comparisons (adoption by area,
manual vs auto); a table for hype-vs-evidence (verdict colour-coded); a timeline for the
regulatory "why now"; a source-type breakdown for transparency. No dense analyst visuals.

## Design rationale
Deep red / cream / gold (Cormorant + EB Garamond) — a restrained luxury identity matching the
use-case document, so the whole submission reads as one piece, while staying legible for a CEO.

## Honesty layer
Vendor/forecast figures are labelled and treated as upper bounds; cost figures are labelled
estimates; US-derived benchmarks are flagged. The hype-vs-evidence table shows where claims are
**supported** vs **hype/unverified** — that *is* the brief's "separate hype from value" deliverable.

## Bonus: the live web cockpit (`deploy/`)
A working Node + Chart.js demo of the *piloted tool* (touchless rate, cost/invoice, governance
HITL panel, live savings calculator), reading a deployed FastAPI backend on synthetic data
(`research/01_data_assumptions.md`). Shown at the meeting as "what the pilot would look like" —
not part of the graded evidence dashboard.
