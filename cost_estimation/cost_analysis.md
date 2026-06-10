# Cost Analysis

> `cost_estimation/cost_analysis.md` — pilot and run costs vs benefit. **All figures are
> planning estimates**, labelled, to be replaced by the client's real numbers (the dashboard
> recomputes everything live). Currency: EUR.

## Pilot cost (10 weeks) — ~€20k

| Item | Estimate | Basis |
|---|---|---|
| Solution build & integration (capture → AI proposal → validation UI) | €15,300 | ~18 days @ €850/day |
| Tooling during pilot (LLM/IDP usage + hosting) | €1,200 | ~€400/mo × 3 |
| Finance team time (validation + training) | €1,350 | ~3 h/wk × 10 × €45/h |
| Contingency (10%) | €1,650 | — |
| **Total pilot** | **≈ €19,500** | |

## Ongoing run cost — ~€13k/year (after rollout)

| Item | Estimate | Basis |
|---|---|---|
| Tooling/hosting at scale (~5,000 invoices/yr) | €4,800 | usage + hosting |
| Support & maintenance | €5,100 | ~0.5 day/mo @ €850 |
| Model/rule tuning + e-invoicing adaptation | €3,000 | periodic |
| **Total ongoing / yr** | **≈ €12,900** | |

> One-off rollout hardening (Phase 2) ≈ €8,000, counted in year 1.

## Benefit (at maturity, real volume)

From the dashboard calculator at **~420 invoices/month, ~78% touchless** (the hotel's assumed
full-property volume — the pilot itself runs on a ~500/yr subset):

| | Value |
|---|---|
| Gross annual saving | **≈ €42,000** |
| Finance hours returned / yr | ≈ 900 h |
| FTE equivalent freed | ≈ 0.6 |

## ROI

| Horizon | Cost | Saving | Net |
|---|---|---|---|
| **Year 1** (pilot €19.5k + rollout €8k + run €13k) | ≈ €40,400 | ≈ €42,000 | **≈ +€1,600 (≈ breakeven)** |
| **Year 2** | ≈ €12,900 | ≈ €42,000 | **≈ +€29,000** |
| **Year 3** | ≈ €12,900 | ≈ €42,000 | **≈ +€29,000** |
| **3-year cumulative** | ≈ €66,200 | ≈ €126,000 | **≈ +€59,800 · ROI ≈ 90%** |

- **Payback:** within ~12 months including the pilot; **~5–6 months** on an ongoing basis.
- **Sensitivity:** the case is volume-driven. Below ~250 invoices/month the year-1 return turns
  negative — hence the pilot gate confirms real volume before scaling. Above ~600/month the
  3-year ROI exceeds ~150%. The calculator exposes this directly.

> Beyond the hard numbers: relieving the lean finance team also addresses **retention** in a
> sector with ~10% workforce shortage — a benefit not monetised above, but real.

---

## Full-tool value stack (expanded business case)

The figures above cover **AP invoice automation** only. The complete tool (the Final-Project
build: AP automation + 3-way match + inventory) unlocks three further, **non-overlapping** value
pools. All are **conservative, assumption-based estimates** for one SME 5★ hotel — to be
replaced by the client's real data. Source rows: `data/processed/value_stack.csv`.

| Value pool | €/yr | Basis (to validate) |
|---|---|---|
| AP automation — invoice processing time saved | **42,000** | ~5,040 invoices/yr, ~78% touchless, €12→€3.9 at €45/h |
| 3-way match — overbilling & price-variance recovered | **10,000** | ~0.6% of ~€1.8M addressable supplier spend; demo caught €2,513 on a 3-month slice |
| Inventory — waste & shrinkage reduction | **9,000** | ~0.5 pt of F&B cost via documented receiving control |
| Inventory — manual stock-entry labour eliminated | **4,500** | ~2 h/week at €45/h loaded |
| **Gross recurring benefit** | **65,500** | |
| Less: ongoing run cost | (13,000) | tooling + support + tuning |
| **Net recurring benefit** | **≈ 52,500 / yr** | |
| One-off working-capital release | +15,000 | ~10% reduction on tied-up F&B inventory (cash, not P&L — shown separately) |

**No double-counting:** processing efficiency (AP) ≠ error recovery (3-way match) ≠ stock waste ≠
stock-entry labour — four distinct pools. **Payback:** the ~€20k pilot is recovered in well under
a year on the net recurring benefit alone. This is what turns the decision into a no-brainer —
*provided* the assumptions are confirmed on the client's real volumes and spend.
