import { useEffect, useState } from "react";

// API base comes from build-time env. Never hard-code secrets in the frontend.
const API_BASE = import.meta.env.VITE_API_URL ?? "";

export default function App() {
  const [health, setHealth] = useState("checking...");

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((j) => setHealth(j.status))
      .catch(() => setHealth("unreachable"));
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 p-6 text-slate-800">
      <h1 className="text-xl font-semibold">Walkback Under Uncertainty</h1>
      <p className="mt-2 text-sm text-slate-500">API status: {health}</p>
      <p className="mt-4 text-xs text-slate-400">
        Scaffold only. Map, sliders and results come next. UI components will come from 21st.dev once an API key is set.
      </p>
    </main>
  );
}
