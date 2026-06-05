# Solution Proposal — Recommendation for Cleo

> `implementation/solution_proposal.md` — the consultant's answer to "should we invest in AI?"

## Recommendation: 🟡 RUN A 10-WEEK PILOT — don't wait, don't yet invest at full scale

Neither "invest at scale now" (the evidence is mostly non-EU and vendor-sourced) nor "wait"
(margins are compressing, talent is scarce, and e-invoicing regulation is arriving). The
lowest-regret path is a **scoped, low-cost pilot** that turns directional benchmarks into
evidence on *this hotel's* real invoices — then a go/no-go decision on facts.

## The solution

AI-assisted invoice processing for general & administrative spend. Incoming supplier invoices
are captured, the AI extracts them and **proposes** an accounting entry (GL account + VAT
treatment + USALI allocation), and a finance team member reviews and approves before anything
is posted. *AI assists, humans decide.* An invoice is **touchless** when the proposal is
accepted with no correction.

## Why a pilot, not a full investment

- The decisive driver — **auto-coding accuracy on the hotel's own invoice mix** — is the one
  number no benchmark can give us. The pilot measures it directly.
- It is **cheap to find out**: ~€20k and 10 weeks (see `cost_estimation/`).
- It **de-risks** the top two risks (accuracy, data security) by running them in a controlled
  scope with a human on every entry.
- It builds the **structured-invoice muscle** the hotel will need anyway for ViDA / Luxembourg
  e-invoicing by 2028–29.

## Scope of the pilot

- **In:** G&A supplier invoices (the vendors in the master), proposed entry + human validation,
  the cockpit + Power BI reporting, the four success metrics below.
- **Out:** cost-control/stock movements (Phase 2), automated P&L reporting (Phase 3), any
  autonomous posting, anything guest-facing or payroll-related.

## Success criteria (the go/no-go gate)

| Metric | Target to justify scaling |
|---|---|
| Touchless / straight-through rate | ≥ 65% by week 10 (and trending up) |
| Account-proposal accuracy | ≥ 90% vs validated entries |
| Handling time per invoice | ≤ 5 min blended (vs ~15 manual) |
| Finance hours returned | Positive and material at real volume |

**Decision rule:** hit the touchless + accuracy targets **at the hotel's real volume** →
scale (Phase 2). Miss narrowly → extend/tune. Miss badly or volume too thin → stop, with the
learning banked. The recommendation is deliberately falsifiable.

## Expected payoff (at maturity, real volume — see `cost_estimation/cost_analysis.md`)

~€42k/year saved and ~0.6 FTE of finance time returned, against ~€20k pilot and ~€13k/yr
ongoing — roughly **breakeven in year 1 (incl. pilot)** and **~€29k/yr net thereafter**.
Every figure recomputes live in the dashboard the moment real numbers replace the assumptions.
