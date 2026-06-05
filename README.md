# AP Master — AI-Assisted Invoice Processing for Luxury Hospitality

An executive-facing cockpit answering one CEO-level question for an independent 5★ hotel
(Luxembourg, SME): **"Is investing in AI to automate the finance back-office actually worth
it?"** Instead of a slide deck of opinions, it backs the answer with a working system you can
click through — and an honest *pilot / wait / invest* recommendation.

Audience: **Cleo**, a non-technical CEO. Principle: **AI assists, humans decide.**

## 🔗 Live

- **Power BI evidence dashboard** *(the graded Project 5 deliverable)* — `dashboard/dashboard_spec.md` → `.pbix`
- **Live web cockpit** *(bonus: a working demo of the piloted tool)* — `https://ap-cockpit-production.up.railway.app`
- **API (source of truth for the demo)** — `https://fantastic-presence-production.up.railway.app` · `/docs`

## What it is

A complete end-to-end answer, in four layers:

1. **A synthetic-but-consistent data world** — a Python generator produces internally-coherent
   CSVs (vendors, chart of accounts, invoices, proposed-vs-validated entries, monthly KPIs).
   Same vendors/accounts/dates flow through every table, so the numbers are believable.
2. **A deployed backend (FastAPI on Railway)** — authenticated analytics endpoints (OAuth2 →
   Bearer) for KPIs, spend, invoices, market evidence, a live savings calculator and a
   governance panel. The single source of truth both front-ends read.
3. **A live web cockpit** (Node + Chart.js) — *bonus: a working demo of what the piloted tool
   would look like*. Server-side login, auto-refresh, cross-filtering, click-to-drill KPIs
   (every number opens its formula + source), and a live opportunity calculator.
4. **A Power BI evidence dashboard** — *the graded Project 5 deliverable*. Per the brief, it
   shows **market / adoption / cost / risk** evidence (public, cited data) leading to the
   invest/wait/**pilot** recommendation — **not** an operational tool. Centrepiece: the
   98%-vs-6% adoption contrast + the hype-vs-evidence table. Spec in `dashboard/dashboard_spec.md`.

> **Two artifacts, two roles.** The **Power BI evidence dashboard** is the brief's graded
> dashboard (does the market support investing?). The **API + web cockpit** are a **bonus
> demo** of what the recommended pilot tool would look like in practice. The brief is explicit:
> *"the goal is not to build an AI tool"* — so the tool is shown as a demo, not as the answer.

Plus a full **AI-adoption consulting case** (research → recommendation) in `research/`,
`implementation/` and `cost_estimation/`.

## Headline result (synthetic pilot)

> Touchless / straight-through rate rose **~46% → ~74%** across a 12-month pilot, account
> accuracy **~94%**, as e-invoice share grew **~26% → ~50%**.
> Projected at the hotel's real volume: **↓ €42k/yr saved, ↓ 0.6 FTE returned** — roughly
> breakeven in year 1 (incl. pilot), ~€29k/yr net thereafter (3-yr ROI ~90%).

> ⚠️ **Operational data is synthetic** — generated to be *plausible*, labelled as such, no real
> company/personal data. **Market-evidence data is real & cited.** See
> `research/01_data_assumptions.md`.

## 📋 The consulting case (Project 5)

- **Sector:** luxury hospitality — independent 5★ hotels. **Size:** SME (~80–250 employees).
- **Use case:** AI proposes the accounting entry for each supplier invoice; a human validates
  before posting. Highest, most defensible ROI; lowest regulatory risk; protects margin *and*
  the lean finance team.
- **Why now:** Western-Europe hotel margins ~33%, EU hospitality short ~10% of staff, and the
  ViDA / Luxembourg e-invoicing wave (B2B by 2028–29) makes structured invoices the norm.
- **Recommendation:** 🟡 **run a 10-week, ~€20k pilot** — don't wait, don't yet scale.

### 📁 Deliverables map (Project 5 rubric)
| Deliverable | File |
|---|---|
| Use-case discovery & selection | `research/use_case_discovery.md` |
| Market research & data gathering | `research/market_research.md` |
| Data assumptions / methodology | `research/01_data_assumptions.md` |
| Opportunity & risk map | `research/opportunities_risks.md` |
| Hype-vs-evidence analysis | `research/hype_vs_evidence.md` |
| Dashboard (Power BI) | `dashboard/` + `.pbix` |
| Dashboard documentation | `dashboard/dashboard_documentation.md` |
| Solution proposal (invest/wait/pilot) | `implementation/solution_proposal.md` |
| Implementation plan | `implementation/implementation_plan.md` |
| Cost analysis | `cost_estimation/cost_analysis.md` |
| Timeline estimate | `cost_estimation/timeline_estimate.md` |
| Source list | `sources.md` |

## Frameworks anchored (no ad-hoc KPIs)
- **USALI** (Uniform System of Accounts for the Lodging Industry) — spend cut by department
  (Rooms, F&B, A&G, Sales & Mktg, Undistributed).
- **Procure-to-Pay / AP** — touchless (straight-through) rate, cost per invoice, cycle time,
  exception rate, accuracy, supplier concentration (HHI).
- **EU AI Act & GDPR** — limited-risk classification, human-in-the-loop, data minimisation.

## Project structure
```
.
├── api/main.py                  # FastAPI — single source of truth
├── scripts/generate_data.py     # synthetic data generator (seed 42)
├── data/
│   ├── raw/                     # 6 synthetic operational CSVs
│   └── processed/ai_adoption_evidence.csv   # public, cited evidence
│   └── processed/hype_vs_evidence.csv       # claim → evidence → verdict
├── deploy/                      # live web cockpit (Node + Chart.js)
│   └── server.js · package.json · public/index.html
├── dashboard/                   # Power BI: spec · documentation · theme · data_model · live_api_connection
├── measures/measures_dax.md
├── research/                    # discovery · market · assumptions · opportunities/risks · hype-vs-evidence
├── implementation/              # solution_proposal · implementation_plan
├── cost_estimation/             # cost_analysis · timeline_estimate
└── requirements.txt · .env.example · Procfile · sources.md · README.md
```

## Quick start
```bash
# 1. Data
pip install -r requirements.txt
python scripts/generate_data.py            # -> data/raw/*.csv

# 2. API (source of truth)
uvicorn api.main:app --port 8000           # -> http://localhost:8000/docs

# 3. Web cockpit (separate terminal)
cd deploy && npm install
API_BASE=http://localhost:8000 npm start   # -> http://localhost:3000

# 4. Power BI: follow dashboard/dashboard_spec.md + dashboard/data_model.md + measures/measures_dax.md
#    (static CSV first; live API via dashboard/live_api_connection.md)
```

## Why it stands out
The data is wired end-to-end and the same source feeds both front-ends, so the numbers always
agree. KPIs are anchored to recognised frameworks (USALI, P2P), every figure drills to its
formula and source, and the case is *honest* — it names where the model is weak and routes
exactly those cases to a human. Built to survive a sceptical CEO asking "where does that number
come from?"
