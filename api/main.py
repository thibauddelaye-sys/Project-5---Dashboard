"""
SCM-of-AP Master API — single source of truth for the cockpit + Power BI.

An authenticated analytics API over the synthetic AP world and the public market-evidence
layer. Both front-ends (the live web cockpit and the Power BI report) read THIS api, so the
numbers always agree.

Run locally:
    pip install -r requirements.txt
    uvicorn api.main:app --reload --port 8000
Then: http://localhost:8000/docs

Auth (demo): POST /auth/token  (form: username, password)  ->  Bearer token.
Defaults username=demo password=demo  (override via env API_USER / API_PASSWORD).
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

# --------------------------------------------------------------------------- config
DATA = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parents[1] / "data"))
API_USER = os.getenv("API_USER", "demo")
API_PASSWORD = os.getenv("API_PASSWORD", "demo")
API_TOKEN = os.getenv("API_TOKEN", "ap-cockpit-demo-token")  # static bearer for the demo
MANUAL_COST = float(os.getenv("MANUAL_COST_PER_INVOICE", "12"))
MANUAL_MIN = float(os.getenv("MANUAL_MINUTES", "15"))
RATE = float(os.getenv("FINANCE_RATE", "45"))

app = FastAPI(title="AP Cockpit API", version="1.0.0",
              description="Synthetic AP analytics + public AI-adoption evidence.")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)
oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


def auth(token: str | None = Depends(oauth2)) -> None:
    """Lightweight bearer check. Mirrors Eugen's OAuth2->Bearer pattern, kept simple."""
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")


# --------------------------------------------------------------------------- data load
@lru_cache(maxsize=1)
def load() -> dict[str, pd.DataFrame]:
    raw = DATA / "raw"
    d = {
        "vendors": pd.read_csv(raw / "vendors.csv"),
        "coa": pd.read_csv(raw / "chart_of_accounts.csv"),
        "invoices": pd.read_csv(raw / "invoices.csv", parse_dates=["invoice_date", "period"]),
        "ap": pd.read_csv(raw / "ap_entries.csv", parse_dates=["period"]),
        "monthly": pd.read_csv(raw / "monthly_kpis.csv"),
        "evidence": pd.read_csv(DATA / "processed" / "ai_adoption_evidence.csv"),
        "value_stack": pd.read_csv(DATA / "processed" / "value_stack.csv"),
    }
    # one joined operational frame, reused by several endpoints
    j = d["ap"].merge(
        d["invoices"][["invoice_id", "net_amount", "gross_amount", "vat_amount"]],
        on="invoice_id")
    j = j.merge(d["vendors"][["vendor_id", "vendor_name", "department"]], on="vendor_id")
    d["joined"] = j
    return d


def recs(df: pd.DataFrame) -> list[dict]:
    """Robust records serialization: NaN -> null, numpy types -> native JSON."""
    return json.loads(df.to_json(orient="records", date_format="iso"))


# --------------------------------------------------------------------------- auth
@app.post("/auth/token", tags=["auth"])
def token(username: str = Form(...), password: str = Form(...)):
    if username != API_USER or password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Bad credentials")
    return {"access_token": API_TOKEN, "token_type": "bearer"}


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "rows": int(len(load()["invoices"]))}


# --------------------------------------------------------------------------- KPIs
@app.get("/api/kpis", tags=["operational"])
def kpis(_: None = Depends(auth)):
    d = load()
    j, m = d["joined"], d["monthly"]
    n = len(j)
    return {
        "invoices_ytd": int(n),
        "touchless_rate": round(float(j["touchless"].mean()), 3),
        "accuracy": round(float(j["account_correct"].mean()), 3),
        "exception_rate": round(float(j["human_corrected"].mean()), 3),
        "avg_minutes": round(float(j["handling_minutes"].mean()), 2),
        "einvoice_share": round(float((j["channel"] == "einvoice").mean()), 3),
        "hours_saved_ytd": round(float(m["hours_saved"].sum()), 1),
        "cost_saved_ytd": int(m["cost_saved"].sum()),
        "spend_net_ytd": int(j["net_amount"].sum()),
        # latest month deltas for the "is it improving?" read
        "touchless_latest": float(m["touchless_rate"].iloc[-1]),
        "touchless_first": float(m["touchless_rate"].iloc[0]),
    }


@app.get("/api/monthly", tags=["operational"])
def monthly(_: None = Depends(auth)):
    return recs(load()["monthly"])


@app.get("/api/spend", tags=["operational"])
def spend(by: str = Query("department", pattern="^(department|vendor_name)$"),
          _: None = Depends(auth)):
    j = load()["joined"]
    g = (j.groupby(by)
           .agg(spend_net=("net_amount", "sum"),
                invoices=("invoice_id", "count"),
                touchless_rate=("touchless", "mean"))
           .round({"spend_net": 0, "touchless_rate": 3})
           .sort_values("spend_net", ascending=False)
           .reset_index())
    return recs(g)


@app.get("/api/invoices", tags=["operational"])
def invoices(limit: int = 50, only_exceptions: bool = False,
             department: str | None = None, _: None = Depends(auth)):
    j = load()["joined"].copy()
    if only_exceptions:
        j = j[j["human_corrected"]]
    if department:
        j = j[j["department"] == department]
    cols = ["invoice_id", "vendor_name", "department", "period", "channel",
            "net_amount", "ai_confidence", "proposed_account", "final_account",
            "touchless", "human_corrected", "account_correct", "handling_minutes",
            "vat_non_deductible"]
    j = j.sort_values("period", ascending=False).head(limit)
    j["period"] = j["period"].dt.strftime("%Y-%m")
    return recs(j[cols])


# --------------------------------------------------------------------------- evidence
@app.get("/api/evidence", tags=["market"])
def evidence(pillar: str | None = None, _: None = Depends(auth)):
    e = load()["evidence"]
    if pillar:
        e = e[e["pillar"].str.lower() == pillar.lower()]
    return recs(e)


# --------------------------------------------------------------------------- savings calc
@app.get("/api/savings", tags=["decision"])
def savings(monthly_volume: int = Query(420, ge=1),
            touchless_target: float = Query(0.75, ge=0, le=1),
            manual_minutes: float = Query(MANUAL_MIN),
            rate: float = Query(RATE),
            auto_minutes_touchless: float = 2.5,
            auto_minutes_review: float = 9.0,
            manual_overhead: float = 0.75,    # print / archive / error correction per invoice
            software_surcharge: float = 0.8,  # IDP/LLM + hosting per invoice
            _: None = Depends(auth)):
    """Opportunity calculator: project annual savings at the client's real volume.

    Single labour-cost lever (the hourly rate). BOTH the manual and the automated cost per
    invoice are DERIVED from it via their respective handling times, so lowering the rate
    correctly lowers both costs (and the absolute saving) — they can never contradict.
    """
    annual = monthly_volume * 12
    manual_cost = (manual_minutes / 60) * rate + manual_overhead
    # blended automated handling time given the target touchless rate
    auto_min = (touchless_target * auto_minutes_touchless
                + (1 - touchless_target) * auto_minutes_review)
    auto_cost = (auto_min / 60) * rate + software_surcharge
    saving_per_invoice = manual_cost - auto_cost
    minutes_saved = (manual_minutes - auto_min) * annual
    return {
        "annual_invoices": annual,
        "manual_cost_per_invoice": round(manual_cost, 2),
        "blended_auto_minutes": round(auto_min, 2),
        "auto_cost_per_invoice": round(auto_cost, 2),
        "saving_per_invoice": round(saving_per_invoice, 2),
        "annual_cost_saving": round(saving_per_invoice * annual, 0),
        "annual_hours_returned": round(minutes_saved / 60, 0),
        "annual_fte_equiv": round((minutes_saved / 60) / 1600, 2),  # ~1600 productive h/FTE
    }


# --------------------------------------------------------------------------- governance
@app.get("/api/governance", tags=["decision"])
def governance(_: None = Depends(auth)):
    """The differentiator: 'AI assists, humans decide' + EU AI Act posture."""
    j = load()["joined"]
    return {
        "eu_ai_act_class": "Limited / minimal risk",
        "eu_ai_act_reason": ("Back-office accounting automation is not an Annex III "
                             "high-risk category; human validates every posted entry."),
        "human_in_the_loop": True,
        "autonomous_posting": False,
        "invoices_reviewed_by_human": int((~j["touchless"]).sum()),
        "share_human_reviewed": round(float((~j["touchless"]).mean()), 3),
        "non_deductible_vat_routed_to_human": int(j["vat_non_deductible"].sum()),
        "gdpr_personal_data_in_scope": "Vendor contacts only; no special-category data",
    }


@app.get("/api/value_stack", tags=["decision"])
def value_stack(_: None = Depends(auth)):
    """Full-tool value stack: distinct, non-overlapping benefit pools + run cost + one-off."""
    v = load()["value_stack"]
    rec = v[v["type"] == "recurring"]
    return {
        "rows": recs(v),
        "gross": round(float(rec[rec["annual_value_eur"] > 0]["annual_value_eur"].sum())),
        "net": round(float(rec["annual_value_eur"].sum())),
        "one_off": round(float(v[v["type"] == "one-off"]["annual_value_eur"].sum())),
    }
