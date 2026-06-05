# Implementation Plan

> `implementation/implementation_plan.md` — from validation to rollout, with a hard decision
> gate after the pilot. Phases 2–3 are the deferred opportunities (B, C).

## Phase 0 — Preparation (1–2 weeks)
- Confirm the real numbers that drive the case: monthly invoice volume, current AP workflow,
  finance loaded rate. Replace the assumptions in the dashboard.
- Data-processing agreement + EU-processing setup for the extraction model; data minimisation.
- Load the vendor master and chart of accounts; define confidence threshold and the VAT cases
  that must always route to a human.

## Phase 1 — Pilot (10 weeks) ⟵ the recommendation
- Stand up the flow: capture → AI proposes entry → human validates → post. Cockpit + Power BI
  reporting live on the pilot data.
- Run on real G&A invoices; **backtest** AI proposals against validated entries weekly.
- Train the finance team; collect the four success metrics.

### 🚦 Decision gate (end of week 10)
Touchless ≥ 65% **and** accuracy ≥ 90% **at real volume** → proceed to Phase 2. Otherwise
extend/tune or stop (see `solution_proposal.md`).

## Phase 2 — Rollout & hardening (8–10 weeks, if gate passed)
- Harden the pipeline, expand to all G&A vendors, add monitoring/alerting on accuracy drift.
- Formalise the EU AI Act technical file + DPIA (these are the Final-Project deliverables).
- Connect to the e-invoicing / Peppol channel ahead of the Luxembourg B2B obligation.

## Phase 3 — Extend (roadmap)
- **Opportunity B:** cost-control invoices → P&L + stock movements (tackle the SKU-matching
  hard problem with the model proven).
- **Opportunity C:** automated monthly P&L reporting + AI variance commentary.

## Alignment with the regulatory calendar
```
2025 ViDA adopted ─ 2026 Belgium B2B / LU law ─ 2027 France B2B ─ 2028–29 LU domestic B2B ─ 2030 EU intra-B2B
        │                         │                                        │
     Phase 0/1 now           Phase 2 (e-invoicing ready)            already compliant & ahead
```
Building now means the hotel meets the 2028–29 obligation from a position of strength rather
than scrambling to comply.
