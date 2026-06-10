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

| Value pool | €/yr | Kind | Basis (to validate) |
|---|---|---|---|
| AP automation — invoice processing time saved | **42,000** | labour | ~5,040 invoices/yr, ~88% touchless target, €12→€3.9 at €45/h |
| 3-way match — manual PO/delivery/invoice matching time saved | **26,000** | labour | ~1.5 days/week of manual three-way reconciliation across F&B suppliers, at €45/h |
| 3-way match — overbilling & price-variance recovered | **10,000** | cash | ~0.6% of ~€1.8M addressable supplier spend |
| Inventory — waste & shrinkage reduction | **9,000** | cash | ~0.5 pt of F&B cost via documented receiving control |
| Inventory — manual stock-entry labour eliminated | **19,500** | labour | ~4.5 full days/month encoding the month's orders & deliveries before close, at €45/h |
| **Gross recurring benefit** | **106,500** | | |
| Less: ongoing run cost | (13,000) | cost | tooling + support + tuning |
| **Net recurring benefit** | **≈ 93,500 / yr** | | |
| One-off working-capital release | +15,000 | one-off | ~10% reduction on tied-up F&B inventory (cash, not P&L — shown separately) |

**FTE freed ≈ 1.2** — only the **labour** pools count toward FTE (cash recovery and waste are €, not
time): (42,000 + 26,000 + 19,500) ÷ €45/h ÷ 1,600 productive h = **1.22 FTE**. The 3-way-match
*cash* recovery (€10k) is deliberately **not** counted as time — that would double-count the
matching-labour pool.

**No double-counting:** five distinct pools — AP processing time, manual matching time, error
recovery (cash), stock waste (cash), stock-entry time. Time pools feed FTE; cash pools do not.
**Payback:** the ~€20k pilot is recovered in a few months on the net recurring benefit. These are
**upper-realistic, assumption-based** figures — the matching-time and stock-entry-time pools are
the main swing factors and must be confirmed on the client's real processes.
