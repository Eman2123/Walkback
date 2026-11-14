import { useEffect, useRef, useState } from "react";
import { explainRun, getHealth, postRun } from "./lib/api.js";
import {
  AssumptionsPanel,
  ControlPanel,
  ExplainPanel,
  MapView,
  ReliabilityChart,
  ResultsPanel,
} from "./components/index.js";

const TILE_ID = import.meta.env.VITE_TILE_ID ?? "dev-synthetic-20m";
const DEFAULTS = {
  habitat_row: 50,
  habitat_col: 50,
  budget_s: 900,
  speed_mps: 0.5,
  cutoff_deg: 20,
  confidence: 0.9,
  roughness: 0.5,
};

export default function App() {
  const [params, setParams] = useState(DEFAULTS);
  const [run, setRun] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [api, setApi] = useState("checking…");
  const [layers, setLayers] = useState({ deterministic: true, calibrated: true, truth: true });
  const [explanation, setExplanation] = useState("");
  const [explaining, setExplaining] = useState(false);
  const timer = useRef(null);

  useEffect(() => {
    getHealth().then((j) => setApi(j.status)).catch(() => setApi("unreachable"));
  }, []);

  // Debounced: a slider drag sends one request, not one per pixel.
  useEffect(() => {
    clearTimeout(timer.current);
    timer.current = setTimeout(async () => {
      setBusy(true);
      setError("");
      setExplanation("");
      try {
        setRun(await postRun({ tile_id: TILE_ID, ...params }));
      } catch (e) {
        setError(e.message);
      } finally {
        setBusy(false);
      }
    }, 300);
    return () => clearTimeout(timer.current);
  }, [params]);

  function setParam(key, value) {
    setParams((p) => ({ ...p, [key]: value }));
  }

  function placeHabitat(row, col) {
    setParams((p) => ({ ...p, habitat_row: row, habitat_col: col }));
  }

  async function handleExplain() {
    if (!run) return;
    setExplaining(true);
    try {
      const { text } = await explainRun(run.run_id);
      setExplanation(text);
    } catch (e) {
      setExplanation(`Explanation unavailable: ${e.message}`);
    } finally {
      setExplaining(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 p-4 text-slate-800">
      <header className="mb-4">
        <h1 className="text-xl font-semibold">Walkback Under Uncertainty</h1>
        <p className="text-xs text-slate-500">
          API: {api}. The terrain shown is {run?.tile?.label ?? "loading"}. Speed, cutoff and roughness are assumptions.
        </p>
      </header>
            {run?.demo && (
        <p className="mb-3 rounded border border-amber-300 bg-amber-50 p-2 text-sm text-amber-900">
          Demo data (recorded). The backend is not connected, so sliders and habitat clicks do not change
          this result. The terrain is synthetic and the numbers are placeholders.
        </p>
      )}

      <div className="grid gap-4 lg:grid-cols-[1fr_360px]">
        <section className="space-y-3">
          <div className="flex flex-wrap gap-3 text-sm">
            {Object.keys(layers).map((k) => (
              <label key={k} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={layers[k]}
                  onChange={(e) => setLayers((l) => ({ ...l, [k]: e.target.checked }))}
                />
                {k}
              </label>
            ))}
          </div>
          <MapView run={run} habitat={params} layers={layers} onHabitatClick={placeHabitat} />
          {error && <p className="text-sm text-rose-700">Error: {error}</p>}
        </section>

        <aside className="space-y-4">
          <div className="rounded-lg border bg-white p-4">
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">Inputs</h2>
            <ControlPanel params={params} onChange={setParam} />
          </div>
          <div className="rounded-lg border bg-white p-4">
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">Result</h2>
            <ResultsPanel run={run} busy={busy} />
          </div>
          <div className="rounded-lg border bg-white p-4">
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">Reliability</h2>
            <ReliabilityChart bins={run?.calibration?.bins} />
          </div>
          <div className="rounded-lg border bg-white p-4">
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">Assumptions</h2>
            <AssumptionsPanel assumptions={run?.assumptions} />
          </div>
          <div className="rounded-lg border bg-white p-4">
            <ExplainPanel
              onExplain={handleExplain}
              text={explanation}
              loading={explaining}
              disabled={!run}
            />
          </div>
        </aside>
      </div>
    </main>
  );
}
