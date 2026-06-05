"""
generate_data.py — Synthetic data world for the AP / invoice-automation cockpit.

Use case: an SME 5-star hotel (Luxembourg) piloting AI-assisted invoice processing.
The AI extracts each supplier invoice and PROPOSES an accounting entry (GL account +
VAT treatment + analytical allocation); a finance team member validates before posting.
"AI assists, humans decide."

Everything is internally consistent: the same vendors, accounts and dates flow through
every table, so KPIs are believable rather than random. All data is SYNTHETIC — randomly
generated to be *plausible*, not real. No real company or personal data is used.

Outputs (data/raw/):
  dim_date.csv            one row per day of the pilot year
  vendors.csv             vendor master (default GL, VAT treatment, channel)
  chart_of_accounts.csv   GL accounts (Lux PCN-style families, simplified)
  invoices.csv            one row per incoming supplier invoice
  ap_entries.csv          the proposed vs validated accounting entry per invoice
  monthly_kpis.csv        month-level roll-up (touchless rate, cost, hours saved...)

Run:  python scripts/generate_data.py
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)

OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

# --- Pilot window: 12 months ending the most recent full month -------------
START = pd.Timestamp("2025-06-01")
MONTHS = pd.date_range(START, periods=12, freq="MS")

# --- Manual baseline (industry benchmark, EUR, directional) -----------------
MANUAL_COST_PER_INVOICE = 12.0      # ~€11-15 manual (HighRadius/Quadient/Nanonets)
MANUAL_MINUTES = 15.0               # ~15 min manual handling (Artsyl)
FINANCE_LOADED_RATE_PER_HOUR = 45.0 # loaded cost of a finance FTE (assumption, to confirm)

# ---------------------------------------------------------------------------
# 1. Chart of accounts (simplified Luxembourg PCN-style families)
# ---------------------------------------------------------------------------
COA = [
    ("6011", "Food purchases (F&B)",            "expense", "F&B"),
    ("6012", "Beverage purchases (F&B)",        "expense", "F&B"),
    ("6061", "Energy & utilities",              "expense", "Undistributed"),
    ("6063", "Cleaning & consumables",          "expense", "Rooms"),
    ("6065", "Laundry & linen",                 "expense", "Rooms"),
    ("6122", "Equipment rental & leasing",      "expense", "Undistributed"),
    ("6135", "Maintenance & repairs",           "expense", "Undistributed"),
    ("6161", "Insurance",                       "expense", "Undistributed"),
    ("6181", "Telecom & IT subscriptions",      "expense", "A&G"),
    ("6226", "Professional fees (legal/audit)", "expense", "A&G"),
    ("6231", "Advertising & marketing",         "expense", "Sales & Mktg"),
    ("6251", "Travel & representation",         "expense", "A&G"),
    ("6257", "OTA & booking commissions",       "expense", "Sales & Mktg"),
    ("6064", "Office supplies",                 "expense", "A&G"),
]
coa = pd.DataFrame(COA, columns=["account", "label", "type", "department"])

# ---------------------------------------------------------------------------
# 2. Vendor master  (default GL, VAT treatment, dominant channel)
#    VAT treatment matters in hospitality: some input VAT is non-deductible
#    (e.g. representation / certain F&B), which the AI must flag.
# ---------------------------------------------------------------------------
# vat_treatment: STD17 = deductible 17%, RED3 = reduced 3% (food), ND = non-deductible
VENDORS = [
    ("V001", "Cactus Wholesale Food",      "6011", "RED3",  "pdf",        180),
    ("V002", "Vins & Domaines Moselle",    "6012", "STD17", "pdf",         60),
    ("V003", "Enovos Luxembourg (energy)", "6061", "STD17", "einvoice",    12),
    ("V004", "CleanPro Supplies",          "6063", "STD17", "pdf",         48),
    ("V005", "Elis Luxembourg (laundry)",  "6065", "STD17", "einvoice",    24),
    ("V006", "TechRent Equipment",         "6122", "STD17", "email",       18),
    ("V007", "BâtiServ Maintenance",       "6135", "STD17", "email",       40),
    ("V008", "Foyer Assurances",           "6161", "ND",    "pdf",          8),
    ("V009", "POST Telecom / IT SaaS",     "6181", "STD17", "einvoice",    20),
    ("V010", "Audit & Conseil S.à r.l.",   "6226", "STD17", "pdf",          6),
    ("V011", "Brand Studio Marketing",     "6231", "STD17", "email",       16),
    ("V012", "Représentation & Events",    "6251", "ND",    "pdf",         22),
    ("V013", "Booking.com Commissions",    "6257", "STD17", "einvoice",    14),
    ("V014", "Office Direct LU",           "6064", "STD17", "email",       30),
]
vendors = pd.DataFrame(
    VENDORS,
    columns=["vendor_id", "vendor_name", "default_account", "vat_treatment",
             "channel", "annual_invoices"],
)
vendors = vendors.merge(coa[["account", "department"]],
                        left_on="default_account", right_on="account", how="left") \
                 .drop(columns="account")

VAT_RATE = {"STD17": 0.17, "RED3": 0.03, "ND": 0.17}  # ND still charged, just not deductible

# ---------------------------------------------------------------------------
# 3. Invoices — generate per-vendor across the 12 months
# ---------------------------------------------------------------------------
# Touchless ramp: the AI improves as the pilot matures and as more vendors move
# to structured e-invoices. Monthly target straight-through rate:
TOUCHLESS_RAMP = np.array([0.34, 0.41, 0.48, 0.55, 0.61, 0.66,
                           0.70, 0.73, 0.76, 0.78, 0.80, 0.82])
# e-invoice share also grows over the year (ViDA / Peppol tailwind)
EINV_RAMP = np.linspace(0.18, 0.34, 12)

rows = []
inv_counter = 0
for _, v in vendors.iterrows():
    # distribute the vendor's annual invoices across months (Poisson around mean/12)
    base = v["annual_invoices"] / 12.0
    for mi, month in enumerate(MONTHS):
        n = rng.poisson(base)
        for _ in range(int(n)):
            inv_counter += 1
            day = int(rng.integers(1, month.days_in_month + 1))
            date = month + pd.Timedelta(days=day - 1)
            # amount: log-normal per department scale
            scale = {"F&B": 850, "Rooms": 400, "Undistributed": 1500,
                     "A&G": 600, "Sales & Mktg": 1200}.get(v["department"], 700)
            net = float(np.round(rng.lognormal(mean=np.log(scale), sigma=0.6), 2))
            # channel: vendor's dominant channel, but with growing e-invoice share
            if rng.random() < EINV_RAMP[mi] and v["channel"] != "einvoice":
                channel = "einvoice"
            else:
                channel = v["channel"]
            rows.append([
                f"INV{inv_counter:05d}", v["vendor_id"], date.normalize(),
                month.normalize(), net, v["vat_treatment"], channel,
            ])

invoices = pd.DataFrame(rows, columns=[
    "invoice_id", "vendor_id", "invoice_date", "period", "net_amount",
    "vat_treatment", "channel"])
invoices["vat_amount"] = (invoices["net_amount"]
                          * invoices["vat_treatment"].map(VAT_RATE)).round(2)
invoices["gross_amount"] = (invoices["net_amount"] + invoices["vat_amount"]).round(2)

# ---------------------------------------------------------------------------
# 4. AP entries — the AI's proposed entry vs the validated one
# ---------------------------------------------------------------------------
inv = invoices.merge(
    vendors[["vendor_id", "default_account", "vat_treatment", "channel", "department"]],
    on="vendor_id", suffixes=("", "_v"))

month_idx = {m.normalize(): i for i, m in enumerate(MONTHS)}

ap = []
for _, r in inv.iterrows():
    mi = month_idx[r["period"]]
    # structured e-invoices are easier → higher confidence
    base_conf = 0.93 if r["channel"] == "einvoice" else 0.80
    confidence = float(np.clip(rng.normal(base_conf, 0.06), 0.4, 0.999))

    # touchless if confidence clears the month's bar AND not a tricky VAT case
    tricky = r["vat_treatment"] == "ND"  # non-deductible VAT needs human eyes
    threshold = 1.0 - TOUCHLESS_RAMP[mi]  # higher ramp -> lower threshold to pass
    touchless = (confidence > (0.78 + threshold * 0.1)) and not (tricky and rng.random() < 0.8)

    # proposed account: usually the vendor default; occasionally the AI mis-proposes
    proposed_account = r["default_account"]
    mis = rng.random() < (0.06 if r["channel"] == "einvoice" else 0.12)
    if mis:
        proposed_account = rng.choice(coa["account"].values)
    # human corrects when not touchless and the proposal was wrong (or VAT tricky)
    corrected = (not touchless) and (mis or tricky)
    final_account = r["default_account"] if corrected else proposed_account
    account_correct = final_account == r["default_account"]

    # handling time: touchless ~ quick review; manual ~ closer to baseline
    if touchless:
        minutes = float(np.clip(rng.normal(2.5, 0.8), 1.0, 6))
    else:
        minutes = float(np.clip(rng.normal(9.0, 3.0), 4, 20))

    ap.append([
        r["invoice_id"], r["vendor_id"], r["period"], r["channel"],
        round(confidence, 3), proposed_account, final_account,
        bool(touchless), bool(corrected), bool(account_correct),
        round(minutes, 1), bool(tricky),
    ])

ap_entries = pd.DataFrame(ap, columns=[
    "invoice_id", "vendor_id", "period", "channel", "ai_confidence",
    "proposed_account", "final_account", "touchless", "human_corrected",
    "account_correct", "handling_minutes", "vat_non_deductible"])

# ---------------------------------------------------------------------------
# 5. Monthly KPI roll-up
# ---------------------------------------------------------------------------
m = ap_entries.merge(invoices[["invoice_id", "net_amount", "gross_amount"]], on="invoice_id")
g = m.groupby("period")
monthly = pd.DataFrame({
    "invoices":          g.size(),
    "touchless_rate":    g["touchless"].mean().round(3),
    "accuracy":          g["account_correct"].mean().round(3),
    "exception_rate":    g["human_corrected"].mean().round(3),
    "avg_minutes":       g["handling_minutes"].mean().round(2),
    "einvoice_share":    g["channel"].apply(lambda s: (s == "einvoice").mean()).round(3),
    "spend_net":         g["net_amount"].sum().round(2),
}).reset_index()

# economics vs the manual baseline
monthly["minutes_saved"] = ((MANUAL_MINUTES - monthly["avg_minutes"])
                            * monthly["invoices"]).round(0)
monthly["hours_saved"] = (monthly["minutes_saved"] / 60).round(1)
monthly["cost_per_invoice"] = (
    (monthly["avg_minutes"] / 60) * FINANCE_LOADED_RATE_PER_HOUR + 0.8  # +software/processing
).round(2)
monthly["cost_saved"] = (
    (MANUAL_COST_PER_INVOICE - monthly["cost_per_invoice"]) * monthly["invoices"]
).round(0)
monthly["month"] = monthly["period"].dt.strftime("%Y-%m")

# ---------------------------------------------------------------------------
# 6. Date dimension
# ---------------------------------------------------------------------------
days = pd.date_range(MONTHS[0], MONTHS[-1] + pd.offsets.MonthEnd(0), freq="D")
dim_date = pd.DataFrame({
    "date": days,
    "year": days.year, "month": days.month, "month_name": days.strftime("%b"),
    "period": days.to_period("M").to_timestamp(),
    "quarter": days.quarter, "day_of_week": days.strftime("%a"),
})

# ---------------------------------------------------------------------------
# Write everything
# ---------------------------------------------------------------------------
def w(df, name):
    df.to_csv(OUT / name, index=False)
    print(f"  {name:24s} {len(df):>6,} rows")

print("Writing synthetic AP data world to data/raw/ ...")
w(dim_date, "dim_date.csv")
w(coa, "chart_of_accounts.csv")
w(vendors, "vendors.csv")
w(invoices, "invoices.csv")
w(ap_entries, "ap_entries.csv")
w(monthly, "monthly_kpis.csv")

# Headline sanity print
tl = ap_entries["touchless"].mean()
acc = ap_entries["account_correct"].mean()
print(f"\nHeadline (full year): {len(invoices):,} invoices | "
      f"touchless {tl:.0%} | account accuracy {acc:.0%} | "
      f"hours saved {monthly['hours_saved'].sum():,.0f} | "
      f"€ saved {monthly['cost_saved'].sum():,.0f}")
