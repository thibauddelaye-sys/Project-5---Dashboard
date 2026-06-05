# Use Case Discovery — AI-Assisted Back-Office for Luxury Hospitality

> **Project 5 deliverable** · `research/use_case_discovery.md`
> Module 5 — AI Strategy & Business Impact
> Purpose: select and justify one focused AI adoption use case for the meeting with Cleo.

---

## 1. Strategic framing

Cleo runs a luxury hotel and is not anti-AI — she is anti-hype. The honest answer to "should we invest in AI?" starts from where this sector actually hurts.

The thesis driving this discovery is simple:

> Luxury hospitality margins are being squeezed from both sides — costs rising faster than revenue — and what keeps the segment standing is the **passion of the people** who deliver the experience. The right first AI investment therefore is **not** one that touches the guest or replaces staff. It is one that removes invisible back-office drudgery, so scarce human energy and scarce euros are redirected to the things that justify a luxury rate.

In one line: **take the grind, not the craft.** This is also the design principle for any solution proposed — *AI assists, humans decide.*

---

## 2. Sector and company size (required choices)

| Choice | Selection | Why this framing |
|---|---|---|
| **Sector** | Luxury hospitality — independent and small-group **5-star** hotels | This is the segment that feels the squeeze most acutely and has the least back-office buffer. |
| **Company size** | **SME** — single property to small group, ~80–250 employees | Large chains centralise finance in shared-service centres; independents and small groups do not. The back-office burden lands on a lean team, making the pain (and the ROI) concentrated and visible. |

This mirrors a realistic client profile rather than a generic enterprise, which makes the business case concrete and testable.

---

## 3. Stakeholders, needs, pain points, and constraints

| Stakeholder | What they need | Pain point today | Decision constraint |
|---|---|---|---|
| **CEO / Owner (Cleo)** | Protect margin without damaging the guest experience | Every cost lever risks cutting into service quality | Will not "burn budget on hype"; needs evidence |
| **CFO / Finance Director** | Accurate, timely month-end close; reliable numbers | Close is slow; team firefights instead of analysing | Limited headcount; can't simply hire |
| **Accountant / AP clerk** | Get invoices booked correctly and on time | Manual keying of supplier invoices; repetitive, error-prone | Volume spikes (month-end, season) overwhelm a small team |
| **Cost controller** | Match cost invoices (F&B, consumables) to stock | Reconciling invoices against stock is manual and lagging | Needs accuracy before it can be trusted |
| **General Manager** | Team focused on guests, not paperwork | Skilled staff pulled into admin | Service standards are non-negotiable |
| **Front-line staff (the "passion")** | Meaningful work, not burnout | Admin overload feeds fatigue and turnover | High attrition is already structural |

**Key insight:** the same lean back-office team is both the *bottleneck* (slow close, error risk) and the *flight risk* (burnout, turnover). A solution that relieves them addresses cost **and** retention at once.

---

## 4. Why this matters now — the evidence base

> ⚠️ **Evidence caveat (read first):** most hard benchmarks below come from **US / global** sources. The client context is **Luxembourg / EU**. These figures are treated as **directional**, not as Luxembourg actuals. Securing EU-specific and client-specific figures is a documented task for `market_research.md` and the pilot. This is exactly the kind of assumption Cleo should validate before investing.

### 4.1 The margin squeeze is real and structural (not cyclical)

- Across all property types, gross operating profit (GOP) margins have been declining through 2025; the post-pandemic expense base has reset structurally higher while RevPAR growth has softened and now trails inflation in most markets (HVS, Dec 2025).
- The pressure is explicitly felt in luxury operations, where revenues have recovered but expenses are rising faster (Hospitality Investor, Feb 2026).
- Even ultra-luxury, with a reported ~7.5% TRevPAR rise, saw payroll per available room climb ~8.3% — costs outrunning the revenue gain (HOTELSMag, Nov 2025).
- Labour is the single largest and fastest-growing cost line; operators have been paying ~22% more than 2019 for ~7% fewer hours worked (CRE Daily, May 2025).

**Implication:** rate strategy alone no longer protects profit. Efficiency does. But the usual efficiency lever — cut labour — collides with the next point.

### 4.2 The sector runs on people who are hard to keep

- Hospitality has the highest staff turnover of any major sector, with annual rates commonly cited around 70–80% (Hybrid Payroll, Feb 2026; OysterLink, Jan 2026).
- Roughly two-thirds of hotels report staffing shortages (AHLA, via Escoffier, 2025).
- Replacing a single employee is estimated at ~€4,400–4,700+ in recruiting, hiring and onboarding (OysterLink / SHRM data, 2025–2026).

**Implication:** you cannot cost-cut your way out via headcount without worsening the turnover and service-quality problem. The viable lever is to make the *existing* team's time go further — and to remove the low-value tasks that fuel burnout.

### 4.3 The back-office "tax" is large, manual, and quietly expensive

- Manual invoice processing commonly costs ~€11–14 per invoice; best-in-class automation brings this to ~€2–5 — a reduction of up to ~80% (HighRadius / Quadient / Nanonets, 2025).
- Average manual invoice cycle time is ~14.6 days, compressible to ~3–5 days with automation (DocuClipper / Ascend, 2025).
- ~68% of teams still manually key invoices into their ERP; under a third have an automated process (DocuClipper, 2025).
- Manual processes carry high error rates (~39% of invoices contain some error in cited surveys); automated straight-through error rates fall toward ~0.1% (DocuClipper / Artsyl, 2025).
- Per-invoice handling can drop from ~15 minutes to ~3 minutes once automated (Artsyl, 2025).

**Implication:** this is a concentrated, measurable cost pool sitting on the exact lean team identified in §3 — high effort, low strategic value, and largely unautomated in SMEs today.

### 4.4 The three forces connect

```
 Margin squeeze        Talent crisis          Manual back-office
 (costs > revenue)  +  (70-80% turnover)  +   (~€12/invoice, 15 min, errors)
        \                    |                        /
         \___________________|_______________________/
                             v
   Every hour and euro spent keying invoices is an hour/euro
   NOT spent on the guest experience that justifies the luxury rate
   — and it burns out the very people the segment depends on.
```

This is why a back-office automation use case is the credible *first* AI move for this segment: it attacks cost and retention simultaneously, without touching the guest-facing craft.

---

## 5. Candidate use cases considered

Three opportunities were mapped before narrowing to one.

| # | Candidate | Core value | Main risk / difficulty | Verdict |
|---|---|---|---|---|
| **A** | **AI-assisted invoice → accounting entry** (general & admin spend), human-validated | Direct labour + error reduction on a known cost pool; clean human-in-the-loop | Auto-coding to the right GL account must be reliable | **Selected** |
| **B** | OCR cost-control invoices → P&L entry **+ stock movements** (F&B, consumables) | Extends value into inventory accuracy | Matching invoice lines to internal item/SKU and unit conversions is genuinely hard | Roadmap phase 2 |
| **C** | Automated monthly **P&L reporting** + AI variance commentary | Visible management value, fast to show | Less "AI core", more BI; weaker as a standalone adoption case | Roadmap / supporting |

Candidates B and C are deliberately deferred to the implementation roadmap rather than dropped — they form a credible expansion path once A proves the model.

---

## 6. Selected use case

**AI-assisted invoice processing and accounting entry, with mandatory human validation.**

The system captures incoming supplier invoices (general and administrative spend), extracts the structured data, proposes a draft accounting entry (account, VAT treatment, analytical allocation), and routes it to a finance team member who reviews, corrects, and approves before anything is posted.

**Why this one wins for an SME luxury hotel:**

1. **Highest, most defensible ROI** — it targets a cost pool with well-established benchmarks (§4.3), so the business case rests on industry data, not optimism.
2. **Clear, contained pain** — the lean finance team in §3 feels it daily; relief is immediately tangible.
3. **Lowest regulatory risk** — back-office accounting automation is not a high-risk category under the EU AI Act (it is not in the Annex III list covering employment, biometrics, essential services, etc.), and the human-in-the-loop design reinforces a low-risk posture. (Full classification belongs to the final-project compliance work.)
4. **Protects margin and people at once** — money saved *and* burnout reduced, aligned to the strategic thesis.
5. **Honest about AI's role** — "AI assists, humans decide" is built in, not bolted on. The human stays accountable for every posted entry.
6. **Sets up the capstone** — this use case is the natural POC to carry into the final project.

---

## 7. Adoption timing — why *now* and not "wait"

| Signal | Reading |
|---|---|
| **Cost curves have crossed** | Manual vs automated per-invoice economics now differ by ~70–80% (§4.3) — the saving is no longer marginal. |
| **Technology has matured** | Intelligent document processing / LLM-based extraction handles varied invoice layouts far better than legacy template OCR. |
| **Adoption is still low in SMEs** | With under a third automated, this is an early-but-proven move — past the bleeding edge, ahead of the laggards. |
| **Regulatory picture is clear enough** | For this low-risk use case, the EU AI Act does not impose high-risk obligations, removing a common "let's wait" objection. |

**Recommendation direction (to be confirmed in the solution proposal):** not "invest at scale now", not "wait", but **run a scoped pilot** — the lowest-regret way to convert these directional benchmarks into client-specific evidence.

---

## 8. Preliminary success criteria (measurable)

To be finalised with the client, but the system "works" if it can show:

1. **Touchless / straight-through rate** — % of invoices the AI proposes correctly with no human correction (target to be baselined in pilot).
2. **Handling time per invoice** — minutes from receipt to approved entry vs the manual baseline.
3. **Finance hours returned per month** — hours freed for higher-value work or simply not worked overtime.
4. **Accuracy / exception rate** — error rate on posted entries vs the manual baseline.

(At least two measurable outcomes are required by the brief; four are defined here so the pilot can pick the most credible.)

---

## 9. Assumptions and evidence gaps (to validate)

| Assumption | Why it matters | How to validate |
|---|---|---|
| US/global benchmarks are directionally valid for Luxembourg | Whole ROI case leans on them | Source EU/Lux figures in `market_research.md`; confirm with client |
| The hotel's invoice volume is high enough for ROI | Per-invoice savings only matter at volume | Get actual monthly invoice count from client |
| A lean team currently keys invoices manually | The pain premise | Confirm current AP workflow with client |
| Auto-coding to the correct GL account is achievable at usable accuracy | Core feasibility of the value | Test in the final-project POC on sample data |
| Luxury labour-cost and turnover dynamics match the segment averages cited | Retention half of the argument | Cross-check with EU hospitality sources |

---

## 10. Explicitly out of scope

To keep the case honest and the risk low, this use case does **not**:

- touch payroll or any HR/worker-management decision (would change the risk profile);
- face the guest or alter the guest experience;
- post any accounting entry autonomously — a human approves every entry;
- (in this phase) handle stock movements or cost-control invoices — that is the deferred roadmap.

---

## Sources

All figures are directional industry benchmarks unless stated; EU/Luxembourg-specific sourcing is a follow-up task.

- HVS — *Hotel Profitability in Transition* (Dec 2025): https://www.hvs.com/article/10345-hotel-profitability-in-transition-cost-pressures-and-budgeting-priorities-for-2026
- Hospitality Investor — *How to protect profit in your luxury hotel* (Feb 2026): https://www.hospitalityinvestor.com/hotels/how-protect-profit-your-luxury-hotel
- HOTELSMag — *Margin Call: Hotel profits stabilize, but costs rise in the Americas* (Nov 2025): https://hotelsmag.com/news/margin-call-hotel-profits-stabilize-but-costs-rise-in-the-americas/
- Hotel Online — *Beneath the Calm: Profit Margins Face Subtle Strain* (Jun 2025): https://www.hotel-online.com/news/beneath-the-calm-profit-margins-face-subtle-strain-in-u-s-hotels
- CRE Daily — *Operating Costs 2025 Trends* (May 2025): https://www.credaily.com/briefs/operating-costs-2025-trends-driving-hotel-profit-margins-down/
- RSM US — *Hospitality bifurcates as luxury outpaces lower tiers* (Aug 2025): https://rsmus.com/insights/industries/real-estate/hospitality-bifurcates-as-luxury-outpaces-lower-tiers.html
- Hybrid Payroll — *Employee Turnover in Hospitality* (Feb 2026): https://hybridpayroll.com/employee-turnover-in-hospitality-industry/
- OysterLink — *Hospitality Turnover Rates* (Jan 2026): https://oysterlink.com/spotlight/high-turnover-in-hospitality-2025/
- Escoffier — *2025 Hospitality Hiring Trends* (Sep 2025): https://escoffierglobal.com/blog/hospitality-hiring-trends-what-employers-need-to-know/
- DocuClipper — *59 Accounts Payable Statistics for 2025* (Mar 2025): https://www.docuclipper.com/blog/accounts-payable-statistics/
- HighRadius — *AP Cost Per Invoice* (Sep 2025): https://www.highradius.com/resources/Blog/ap-cost-per-invoice/
- Quadient — *AP automation cost in 2025*: https://www.quadient.com/en/blog/how-much-does-accounts-payable-ap-automation-cost
- Parseur — *AI Invoice Processing Benchmarks 2026* (Nov 2025): https://parseur.com/blog/ai-invoice-processing-benchmarks
- Nanonets — *How Much Does It Cost to Process an Invoice in 2025* (Sep 2025): https://nanonets.com/blog/cost-of-processing-an-invoice/
- Artsyl — *Invoice Processing Automation: 2025 ROI Formula Guide* (Oct 2025): https://www.artsyltech.com/blog/invoice-processing-automation-guide
