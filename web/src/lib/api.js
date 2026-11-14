// Single place that talks to the backend. Components never call fetch directly.
const API_BASE = import.meta.env.VITE_API_URL ?? "";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err = new Error(body.detail ?? `HTTP ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

// Recorded result shown when the backend is down or not connected yet.
async function loadDemo() {
  const res = await fetch(`${import.meta.env.BASE_URL}demo-run.json`);
  if (!res.ok) throw new Error("Demo file missing");
  return { ...(await res.json()), demo: true };
}

export const getHealth = () => request("/api/health");

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