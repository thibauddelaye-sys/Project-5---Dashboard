// server.js — AP Cockpit web server.
// Logs into the AP API server-side, caches all analytics, auto-refreshes, and serves the
// dashboard. The browser never sees the API token — it only talks to this server.
import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

const API_BASE = process.env.API_BASE || "http://localhost:8000";
const API_USER = process.env.API_USER || "demo";
const API_PASSWORD = process.env.API_PASSWORD || "demo";
const REFRESH_MS = (parseInt(process.env.REFRESH_SECONDS || "60", 10)) * 1000;
const PORT = process.env.PORT || 3000;

let TOKEN = null;
let CACHE = { updated_at: null, error: null };

async function login() {
  const body = new URLSearchParams({ username: API_USER, password: API_PASSWORD });
  const r = await fetch(`${API_BASE}/auth/token`, { method: "POST", body });
  if (!r.ok) throw new Error(`auth ${r.status}`);
  TOKEN = (await r.json()).access_token;
}

async function get(p) {
  const r = await fetch(`${API_BASE}${p}`, { headers: { Authorization: `Bearer ${TOKEN}` } });
  if (r.status === 401) { await login(); return get(p); }      // token expired -> re-login
  if (!r.ok) throw new Error(`${p} -> ${r.status}`);
  return r.json();
}

async function refresh() {
  try {
    if (!TOKEN) await login();
    const [kpis, monthly, spendDept, spendVendor, evidence, governance, savings] =
      await Promise.all([
        get("/api/kpis"), get("/api/monthly"),
        get("/api/spend?by=department"), get("/api/spend?by=vendor_name"),
        get("/api/evidence"), get("/api/governance"),
        get("/api/savings"),
      ]);
    CACHE = { updated_at: new Date().toISOString(), error: null,
              kpis, monthly, spendDept, spendVendor, evidence, governance, savings };
    console.log(`[refresh] ok @ ${CACHE.updated_at}`);
  } catch (e) {
    CACHE.error = String(e);
    console.error(`[refresh] FAILED: ${e}`);
  }
}

// the browser reads the cached bundle here
app.get("/data", (_req, res) => res.json(CACHE));

// live opportunity calculator — proxied so the browser stays token-free
app.get("/calc", async (req, res) => {
  try {
    const qs = new URLSearchParams(req.query).toString();
    res.json(await get(`/api/savings?${qs}`));
  } catch (e) { res.status(502).json({ error: String(e) }); }
});

app.get("/invoices", async (req, res) => {
  try {
    const qs = new URLSearchParams(req.query).toString();
    res.json(await get(`/api/invoices?${qs}`));
  } catch (e) { res.status(502).json({ error: String(e) }); }
});

app.use("/vendor", express.static(path.join(__dirname, "node_modules/chart.js/dist")));
app.use(express.static(path.join(__dirname, "public")));

app.listen(PORT, () => {
  console.log(`AP Cockpit on :${PORT}  (API ${API_BASE})`);
  refresh();
  setInterval(refresh, REFRESH_MS);
});
