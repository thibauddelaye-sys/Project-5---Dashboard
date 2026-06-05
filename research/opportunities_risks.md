# Opportunities & Risk Map

> `research/opportunities_risks.md` — the three AI opportunities considered, scored and
> prioritised, plus a scored risk matrix for the selected one.

## Opportunities considered

Scored on **Value** (impact on margin/people) × **Feasibility** (lift, data, risk), 1–5.

| # | Opportunity | Value | Feasibility | Score | Verdict |
|---|---|---|---|---|---|
| **A** | **Invoice → accounting entry** (G&A), human-validated | 4 | 5 | **20** | **Selected — now** |
| B | OCR cost-control invoices → P&L **+ stock movements** | 5 | 2 | 10 | Phase 2 (roadmap) |
| C | Automated monthly P&L reporting + AI variance commentary | 3 | 4 | 12 | Phase 3 / support |

**Why A wins.** Highest feasibility on a well-benchmarked cost pool, cleanest human-in-the-loop,
lowest regulatory risk, and it protects margin *and* people at once. B carries the genuinely
hard problem (matching invoice lines to internal SKUs + unit conversions); C is more BI than
AI. A also de-risks the looming e-invoicing obligations (ViDA / Luxembourg 2028–29) by building
structured-invoice handling now. B and C are deferred, not dropped — they form the expansion
path once A proves the model.

## Risk matrix (selected use case)

Likelihood (L) × Impact (I), 1–5 → **Score**. 🔴 ≥12 · 🟡 6–11 · 🟢 ≤5.

| # | Risk | L | I | Score | Mitigation |
|---|---|---|---|---|---|
| R1 | Auto-coding accuracy below target on the hotel's real invoice mix (scanned PDFs, new vendors) | 3 | 4 | 🔴 12 | Human-in-the-loop on every entry; confidence threshold routes low-confidence to review; **backtest on real invoices during the pilot** before any scaling |
| R2 | Data security — invoices carry vendor PII; third-party LLM processing | 3 | 4 | 🔴 12 | Data-processing agreement; EU-hosted/processing; data minimisation; no ledger ingested |
| R3 | Invoice volume too low for the ROI to clear | 2 | 4 | 🟡 8 | Confirm real monthly volume up front; **pilot decision gate** kills/holds if volume is thin |
| R4 | Change resistance / finance team distrust of "AI doing the books" | 3 | 3 | 🟡 9 | "Second set of eyes" framing; no headcount cuts; training; team keeps final say |
| R5 | Invoice quality / format drift (illegible scans, layout changes) | 3 | 2 | 🟡 6 | Exception routing + manual fallback; e-invoice share rising reduces this over time |
| R6 | Tooling cost overrun or vendor pricing change | 2 | 3 | 🟡 6 | Usage caps; portable architecture; rising e-invoice share lowers per-invoice cost |
| R7 | EU AI Act / GDPR mis-step (wrong classification, missing DPIA) | 2 | 4 | 🟡 8 | Limited-risk classification documented; DPIA + technical file (Final-Project deliverables) |
| R8 | Vendor lock-in on the automation platform | 2 | 3 | 🟡 6 | Standard formats (EN 16931 / Peppol); architecture portable across tools |

**Top risks (R1, R2) are both structural and both already mitigated by design** — the
human-in-the-loop neutralises accuracy risk, and the data-handling controls neutralise the
PII risk. Neither blocks a *pilot*; both are exactly what the pilot is meant to prove.
