// Single place that talks to the backend. Components never call fetch directly.
// Same-origin "/api" first (Vercel forwards it to the backend, see vercel.json), then VITE_API_URL if one is set.
import { makeClient } from "./transport.js";

const API_URL = (import.meta.env.VITE_API_URL ?? "").replace(/\/+$/, "");
const client = makeClient({ bases: API_URL ? ["", API_URL] : [""] });
const request = (path, options, opts) => client.request(path, options, opts);

// Recorded result shown when the backend is down or not connected yet.
async function loadDemo() {
  const res = await fetch(`${import.meta.env.BASE_URL}demo-run.json`);
  if (!res.ok) throw new Error("Demo file missing");
  return { ...(await res.json()), demo: true };
}

// Shaded-relief basemap made by the backend from the real terrain tile.
export const reliefUrl = (tileId) => `${client.activeBase()}/api/tiles/${encodeURIComponent(tileId)}/relief.png`;

// Real HiRISE orthophoto of the analysis window, written by scripts/build_basemap.py into public/.
// It is optional: when it is missing the map falls back to the shaded relief.
export const basemapUrl = (tileId) => `${import.meta.env.BASE_URL}basemap-${encodeURIComponent(tileId)}.jpg`;

export async function loadBasemapMeta(tileId) {
  try {
    const res = await fetch(`${import.meta.env.BASE_URL}basemap-${encodeURIComponent(tileId)}.json`);
    if (!res.ok || !(res.headers.get("content-type") ?? "").includes("json")) return null;
    const meta = await res.json();
    return meta?.points?.centre ? meta : null;
  } catch {
    return null;
  }
}

// Fixed report written by scripts/route_feasibility.py into public/. Optional: null when missing or malformed.
export async function loadRouteFeasibility() {
  try {
    const res = await fetch(`${import.meta.env.BASE_URL}route-feasibility.json`);
    if (!res.ok || !(res.headers.get("content-type") ?? "").includes("json")) return null;
    const d = await res.json();
    return Array.isArray(d?.rows) && d?.headline ? d : null;
  } catch {
    return null;
  }
}

export const getHealth = () => request("/api/health", {}, { timeout: 12000 });

export const postRun = async (params) => {
  try {
    return await request("/api/runs", { method: "POST", body: JSON.stringify(params) });
  } catch (e) {
    // The API answered and rejected the input or the rate limit: show the real error.
    if ([400, 422, 429].includes(e.status)) throw e;
    // No answer, or 5xx such as 501 "not connected": fall back to the recording.
    return loadDemo();
  }
};

export const getRun = (id) => request(`/api/runs/${encodeURIComponent(id)}`);
export const explainRun = (id) =>
  request(`/api/runs/${encodeURIComponent(id)}/explain`, { method: "POST" });