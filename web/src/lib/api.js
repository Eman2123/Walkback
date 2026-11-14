// Single place that talks to the backend. Components never call fetch directly.
const API_BASE = import.meta.env.VITE_API_URL ?? "";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  return res.json();
}

export const getHealth = () => request("/api/health");
export const postRun = (params) => request("/api/runs", { method: "POST", body: JSON.stringify(params) });
export const getRun = (id) => request(`/api/runs/${encodeURIComponent(id)}`);
