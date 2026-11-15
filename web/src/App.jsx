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

const TILE_ID = import.meta.env.VITE_TILE_ID ?? "jezero-20m";
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

const LAYER_META = {
  deterministic: { label: "Deterministic (coarse DEM)", swatch: "bg-blue-500" },
  calibrated: { label: "Calibrated (at your threshold)", swatch: "bg-emerald-500" },
  truth: { label: "Truth (1 m HiRISE DTM)", swatch: "border-2 border-amber-500" },
};

function Card({ title, children, className = "" }) {
  return (
    <section className={`rounded-xl border border-slate-200 bg-white p-4 shadow-sm ${className}`}>
      {title && (
        <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500">{title}</h2>
      )}
      {children}
    </section>
  );
}

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

  const dot = api === "ok" ? "bg-emerald-400" : api === "checking…" ? "bg-slate-400" : "bg-amber-400";

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <header className="bg-slate-900 text-white">
        <div className="mx-auto flex max-w-[1400px] flex-wrap items-center justify-between gap-3 px-6 py-3">
          <div className="flex items-center gap-3">
            <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">
              <circle cx="14" cy="14" r="13" fill="none" stroke="#ea580c" strokeWidth="2" />
              <circle cx="14" cy="14" r="7" fill="none" stroke="#fb923c" strokeWidth="2" />
              <circle cx="14" cy="14" r="2.5" fill="#fff" />
            </svg>
            <div>
              <h1 className="text-base font-semibold leading-tight">Walkback Under Uncertainty</h1>
              <p className="text-xs text-slate-400">
                Terrain: {run?.tile?.label ?? "loading"}. Speed, cutoff and roughness are assumptions.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-200">
            <span className={`h-2 w-2 rounded-full ${dot}`} />
            API: {api}
          </div>
        </div>
      </header>

      {run?.demo && (
        <div className="border-b border-amber-300 bg-amber-50">
          <p className="mx-auto max-w-[1400px] px-6 py-2 text-sm text-amber-900">
            <strong>Demo data (recorded).</strong> The backend is not connected, so sliders and habitat clicks
            do not change this result. The terrain is synthetic and the numbers are placeholders.
          </p>
        </div>
      )}

      <main className="mx-auto grid max-w-[1400px] gap-6 p-6 lg:grid-cols-[minmax(0,1fr)_380px]">
        <div className="space-y-6">
          <Card>
            <div className="mb-3 flex flex-wrap items-center gap-2">
              {Object.entries(LAYER_META).map(([key, m]) => (
                <button
                  key={key}
                  type="button"
                  aria-pressed={layers[key]}
                  onClick={() => setLayers((l) => ({ ...l, [key]: !l[key] }))}
                  className={`flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium transition ${
                    layers[key]
                      ? "border-slate-300 bg-white text-slate-800 shadow-sm"
                      : "border-slate-200 bg-slate-100 text-slate-400"
                  }`}
                >
                  <i className={`inline-block h-3 w-3 rounded-sm ${m.swatch}`} />
                  {m.label}
                </button>
              ))}
              <span className="flex items-center gap-2 px-2 text-xs text-slate-500">
                <i className="inline-block h-3 w-3 rounded-full border-2 border-slate-800 bg-white" />
                Habitat (click the map to move it)
              </span>
              {canShare && (
                <button
                  type="button"
                  onClick={copyLink}
                  className="ml-auto rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-700"
                >
                  {copied ? "Link copied" : "Copy share link"}
                </button>
              )}
            </div>

            <div className="relative">
              <MapView run={run} habitat={params} layers={layers} onHabitatClick={placeHabitat} tileId={TILE_ID} />
              {busy && (
                <div
                  role="status"
                  className="absolute right-3 top-3 rounded-full bg-white/90 px-3 py-1 text-xs text-slate-700 shadow"
                >
                  Updating…
                </div>
              )}
            </div>

            <p className="mt-3 text-xs leading-relaxed text-slate-500">
              <strong className="text-slate-700">Basemap:</strong>{" "}
              {run?.tile?.label?.toUpperCase().includes("SYNTHETIC") || run?.demo ? (
                "synthetic development terrain, not Mars data. "
              ) : (
                <>
                  shaded relief derived from the coarse 20 m DEM, which is derived from the Mars 2020 TRN HiRISE DTM
                  of Jezero crater (USGS Astrogeology, from NASA HiRISE stereo images; DOI 10.5066/P9REJ9JN). Local
                  metres, about 18.4&deg;N 77.6&deg;E.{" "}
                </>
              )}
              Explore the planet in{" "}
              <a
                href="https://trek.nasa.gov/mars/"
                target="_blank"
                rel="noreferrer"
                className="font-medium text-blue-700 underline"
              >
                NASA Mars Trek
              </a>
              . NASA does not endorse this website.
            </p>

            {error && (
              <p role="alert" className="mt-3 rounded-lg border border-rose-300 bg-rose-50 p-3 text-sm text-rose-800">
                Could not compute this run: {error}. Change an input and try again.
              </p>
            )}

               <p className="mt-3 text-xs text-slate-500">
              Sliders change assumptions, not the terrain.{" "}
              {run?.demo
                ? "This is a recorded demo on synthetic terrain, not a validation against HiRISE. "
                : "The headline result is the stored validation against the 1 m HiRISE DTM. "}
              This is a planning aid, not flight software.
            </p>


          </Card>

          <Card title="Result">
            <ResultsPanel run={run} busy={busy} />
          </Card> 
           <Card title="Assumptions">
            <AssumptionsPanel assumptions={run?.assumptions} />
          </Card>
        </div>


           
        <aside className="space-y-6" >
          <Card title="Inputs">
            <ControlPanel params={params} onChange={setParam} />
          </Card>
          <Card title="Reliability">
            <ReliabilityChart bins={run?.calibration?.bins} />
          </Card>
          




          <Card>
            <ExplainPanel onExplain={handleExplain} text={explanation} loading={explaining} disabled={!run} />
          </Card>
        </aside>
      </main>
    </div>
  );
}



