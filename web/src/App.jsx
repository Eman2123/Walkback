import { useEffect, useRef, useState } from "react";
import { explainRun, getHealth, getRun, postRun } from "./lib/api.js";
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

// A share link looks like /?run=<run_id>
const sharedId = new URLSearchParams(window.location.search).get("run");

export default function App() {
  const [params, setParams] = useState(DEFAULTS);
  const [run, setRun] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [api, setApi] = useState("checking…");
  const [layers, setLayers] = useState({ deterministic: true, calibrated: true, truth: true });
  const [explanation, setExplanation] = useState("");
  const [explaining, setExplaining] = useState(false);
  const [copied, setCopied] = useState(false);
  const timer = useRef(null);
  const touched = useRef(false);

  useEffect(() => {
    getHealth().then((j) => setApi(j.status)).catch(() => setApi("unreachable"));
  }, []);

  // Open a shared run: load the stored result and show its inputs.
  useEffect(() => {
    if (!sharedId) return;
    setBusy(true);
    getRun(sharedId)
      .then((r) => {
        setRun(r);
        if (r.params) setParams(r.params);
      })
      .catch((e) => setError(`Could not open the shared run: ${e.message}`))
      .finally(() => setBusy(false));
  }, []);

  // Debounced: a slider drag sends one request, not one per pixel.
  useEffect(() => {
    if (sharedId && !touched.current) return; // keep the shared result until the user changes something
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
    touched.current = true;
    setParams((p) => ({ ...p, [key]: value }));
  }

  function placeHabitat(row, col) {
    touched.current = true;
    setParams((p) => ({ ...p, habitat_row: row, habitat_col: col }));
  }

    async function handleExplain() {
    if (!run) return;
    // The demo recording is not a stored run, so the backend has nothing to explain.
    if (run.demo) {
      setExplanation(
        "The explainer is not available for the demo recording. It needs the backend and a stored run."
      );
      return;
    }
    setExplaining(true);
    try {
      const { text } = await explainRun(run.run_id);
      setExplanation(text);
    } catch (e) {
      setExplanation(
        `The explanation is not available right now (${e.message}). The numbers above are still correct.`
      );
    } finally {
      setExplaining(false);
    }
  }
  

  // The demo recording is not a stored run, so it has no share link.
  const canShare = run && !run.demo && run.run_id;

  async function copyLink() {
    const url = `${window.location.origin}${window.location.pathname}?run=${encodeURIComponent(run.run_id)}`;
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt("Copy this link", url);
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
          <div className="flex flex-wrap items-center gap-3 text-sm">
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
            {canShare && (
              <button
                type="button"
                onClick={copyLink}
                className="ml-auto rounded bg-slate-800 px-3 py-1 text-xs text-white"
              >
                {copied ? "Link copied" : "Copy share link"}
              </button>
            )}
          </div>

          <div className="flex flex-wrap gap-4 text-xs text-slate-600">
            <span className="flex items-center gap-1">
              <i className="inline-block h-3 w-3 rounded-sm" style={{ background: "rgba(47,111,221,0.6)" }} />
              Deterministic (coarse DEM)
            </span>
            <span className="flex items-center gap-1">
              <i className="inline-block h-3 w-3 rounded-sm" style={{ background: "rgba(31,157,85,0.7)" }} />
              Calibrated (at your confidence threshold)
            </span>
            <span className="flex items-center gap-1">
              <i className="inline-block h-3 w-3 rounded-sm border-2" style={{ borderColor: "#e07b00" }} />
              Truth (1 m DTM)
            </span>
            <span className="flex items-center gap-1">
              <i className="inline-block h-3 w-3 rounded-full border-2 border-slate-800 bg-white" />
              Habitat
            </span>
          </div>

          <div className="relative mx-auto w-full max-w-[720px]">
            <MapView run={run} habitat={params} layers={layers} onHabitatClick={placeHabitat} />
            {busy && (
              <div
                role="status"
                className="absolute right-2 top-2 rounded bg-white/90 px-2 py-1 text-xs text-slate-700 shadow"
              >
                Updating…
              </div>
            )}
          </div>

          {error && (
            <p role="alert" className="rounded border border-rose-300 bg-rose-50 p-2 text-sm text-rose-800">
              Could not compute this run: {error}. Change an input and try again.
            </p>
          )}
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