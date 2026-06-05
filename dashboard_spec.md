# Power BI — Dashboard Spec (4 pages)

> `dashboard/dashboard_spec.md` — the Power BI report mirrors the web cockpit page-for-page,
> so the two front-ends tell the identical story. Theme: deep red `#8C1C2B`, cream `#FBF8F2`,
> gold `#A8884F` (match the use-case PDF). Set a report theme JSON with these colours.

Each page carries a small **"robust vs validate"** text box → rolls up to invest/wait/**pilot**.

## Page 1 · The Decision
| Visual | Type | Fields / measure |
|---|---|---|
| 6 KPI cards | Card | `Touchless Rate`, `Account Accuracy`, `Hours Returned`, `Cost Saved`, `Auto Cost per Invoice` (vs €12), `e-Invoice Share` |
| Touchless ramp | Line | Axis `Dim_Date[month]`, Value `Touchless Rate` |
| Decision flag | Card | `Touchless Quality` (🟢/🟡/🔴) |
| Recommendation | Text box | "🟡 Run the pilot…" + `Projected Annual Saving`, `Projected FTE Equivalent` |
| Margin link | Text box | "Back-office efficiency protects ~1–2 pts of GOP while W-Europe margins sit ~33%." |

## Page 2 · The Opportunity (USALI)
| Visual | Type | Fields / measure |
|---|---|---|
| Sliders | What-If slicers | `Volume`, `Touchless Target`, `Manual Cost`, `Finance Rate` |
| Savings cards | Card | `Projected Annual Saving`, `Projected Hours Returned`, `Projected FTE Equivalent`, `Projected Saving per Invoice` |
| Manual vs automated | Clustered column | categories Cost/Time/Cycle; series manual vs `Auto Cost per Invoice` etc. |
| Spend by department | Donut | Legend `Dim_Account[department]` (USALI), Value `Net Spend` — **enable cross-filter** |
| Top vendors | Bar | Axis `Dim_Vendor[vendor_name]`, Value `Net Spend`; card `Top Supplier Share`, `Vendor HHI` |

## Page 3 · Adoption vs Hype + Why Now
| Visual | Type | Fields / measure |
|---|---|---|
| Shock contrast | 2 big Cards | "98% adopt" (text) vs `EU Hospitality AI Deployment` ("~6%") |
| Where AI is used | Bar | back-office 64% / energy 54% / revenue 53% / guest 9% (from Evidence or static) |
| Pressure cards | 3 Cards | `Western Europe GOP Margin`, `Workforce Gap`, AP cost €12→€3 |
| ViDA timeline | Line/scatter or formatted table | Evidence rows where `pillar = "Regulatory"`, by `year` |

## Page 4 · Governance & Trust
| Visual | Type | Fields / measure |
|---|---|---|
| HITL flow | Shapes/image | Invoice → AI proposes → **Human validates** → Posting (human step in red) |
| EU AI Act | Card + text | "Limited / minimal risk"; "no autonomous posting" |
| Human oversight | Card | count of `human_corrected = TRUE`, `vat_non_deductible = TRUE` |
| GDPR note | Text box | "Vendor contacts only; ledger never ingested." |
| Honest weak-spots | Text box | scanned PDFs + non-deductible VAT → routed to a human |

## Build order
1. Wire source (static CSV first — fastest path to a working `.pbix`).
2. Set relationships (`data_model.md`), mark `Dim_Date` as date table.
3. Add `_Measures` (all of `measures_dax.md`) + the 4 What-If parameters.
4. Build pages 1→4; apply the red/cream/gold theme.
5. (Upgrade) swap source to the live API via `live_api_connection.md`.
6. Centrepiece for the lab: the **Touchless ramp line + the projected-saving cards** — the
   AP equivalent of Eugen's "predicted vs actual + MAPE card".
