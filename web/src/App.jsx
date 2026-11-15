import { useEffect, useRef, useState } from "react";
import SoundToggle from "./components/SoundToggle.jsx";
import { sfx, speak, stopSpeaking, tick } from "./lib/sound.js";
import { useSoundOn } from "./lib/useSound.js";
import { explainRun, getHealth, getRun, loadBasemapMeta, postRun } from "./lib/api.js";
import { cellLatLon, fmtLatLon } from "./lib/format.js";
import {
  AssumptionsPanel,
  ControlPanel,
  ExplainPanel,
  MapView,
  ReliabilityChart,
  ResultsPanel,
  RouteFeasibilityPanel,
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
  deterministic: { label: "Deterministic", swatch: "bg-aqua" },
  calibrated: { label: "Calibrated", swatch: "bg-neon" },
  truth: { label: "Truth 1 m", swatch: "border-2 border-dashed border-sun" },
};

function Card({ title, children, className = "" }) {
  return (
    <section className={`px-box p-4 ${className}`}>
      {title && (
        <h2 className="px-title mb-4 flex items-center gap-2">
          <i className="inline-block h-3 w-3 bg-mars" aria-hidden="true" />
          {title}
        </h2>
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
  const [basemapKind, setBasemapKind] = useState("photo");
  const [basemapMeta, setBasemapMeta] = useState(null);
  const timer = useRef(null);
  const touched = useRef(false);
  const soundOn = useSoundOn();

  // Sound effects for every pixel button and slider, in one place. All calls do nothing while sound is off.
  useEffect(() => {
    const onClick = (e) => {
      if (e.target.closest?.(".px-btn:not([data-silent]), .px-toggle:not([data-silent])")) sfx("click");
    };
    const onInput = (e) => {
      const el = e.target;
      if (el.classList?.contains("wb-range")) tick((el.value - el.min) / (el.max - el.min));
    };
    document.addEventListener("click", onClick);
    document.addEventListener("input", onInput);
    return () => {
      document.removeEventListener("click", onClick);
      document.removeEventListener("input", onInput);
    };
  }, []);

  // A new result gets a sound. A result that misses the 95 % target must not sound like a win.
  useEffect(() => {
    if (!run?.stats) return;
    sfx(run.stats.coverage != null && run.stats.coverage < 0.95 ? "shortfall" : "done");
  }, [run?.run_id]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (error) sfx("error");
  }, [error]);

  // Stop reading when the inputs change (the text no longer matches the screen).
  useEffect(() => {
    if (!explanation) stopSpeaking();
  }, [explanation]);

  useEffect(() => {
    loadBasemapMeta(TILE_ID).then(setBasemapMeta);
  }, []);

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
    sfx("place");
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
      if (soundOn) speak(text); // read aloud automatically only when the visitor turned sound on
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

  const dot = api === "ok" ? "bg-neon" : api === "checking…" ? "bg-mute" : "bg-sun";
  const habitatPos = basemapKind === "photo" ? cellLatLon(basemapMeta, params.habitat_row, params.habitat_col) : null;
  const synthetic = run?.demo || run?.tile?.label?.toUpperCase().includes("SYNTHETIC");

  return (
    <div className="min-h-screen text-cream">
      <header className="border-b-4 border-ink bg-panel shadow-[0_4px_0_0_#0d0814]">
        <div className="mx-auto flex max-w-[1400px] flex-wrap items-center justify-between gap-4 px-6 py-4">
          <div className="flex items-center gap-4">
            <img src="/favicon.svg" alt="" width="48" height="48" className="border-4 border-ink" style={{ imageRendering: "pixelated" }} />
            <div>
              <h1 className="font-pixel text-sm leading-snug text-sun sm:text-base">Walkback Under Uncertainty</h1>
              <p className="mt-1 text-sm text-mute">
                Terrain: {run?.tile?.label ?? "loading"}. Speed, cutoff and roughness are assumptions.
              </p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-3">
          <SoundToggle />
          <div className="px-inset flex items-center gap-3 px-3 py-2 font-pixel text-[9px] uppercase text-cream">
            <span className={`inline-block h-3 w-3 ${dot} ${api === "ok" ? "" : "px-blink"}`} />
            API: {api}
          </div>
          </div>
        </div>
      </header>

      {run?.demo && (
        <div className="border-b-4 border-ink bg-sun">
          <p className="mx-auto max-w-[1400px] px-6 py-2 text-base text-ink">
            <strong className="font-pixel text-[10px]">DEMO DATA (RECORDED).</strong> The backend is not connected,
            so sliders and habitat clicks do not change this result. The terrain is synthetic and the numbers are
            placeholders.
          </p>
        </div>
      )}

      <main className="mx-auto grid max-w-[1400px] gap-8 p-6 lg:grid-cols-[minmax(0,1fr)_380px]">
        <div className="space-y-8">
          <Card>
            <div className="mb-4 flex flex-wrap items-center gap-3">
              {Object.entries(LAYER_META).map(([key, m]) => (
                <button
                  key={key}
                  type="button"
                  aria-pressed={layers[key]}
                  onClick={() => setLayers((l) => ({ ...l, [key]: !l[key] }))}
                  className="px-toggle"
                >
                  <i className={`inline-block h-3 w-3 ${m.swatch}`} />
                  {m.label}
                </button>
              ))}
              <span className="flex items-center gap-2 px-1 text-sm text-mute">
                <i className="inline-block h-3 w-3 bg-cream outline outline-2 outline-ink" />
                Habitat (click the map to move it)
                {habitatPos && <span className="text-cream">: {fmtLatLon(habitatPos.lat, habitatPos.lon)}</span>}
              </span>
              {canShare && (
                <button type="button" onClick={copyLink} className="px-btn ml-auto">
                  {copied ? "Link copied" : "Copy share link"}
                </button>
              )}
            </div>

            <div className="relative">
              <MapView run={run} habitat={params} layers={layers} onHabitatClick={placeHabitat} tileId={TILE_ID} onBasemapChange={setBasemapKind} />
              {busy && (
                <div
                  role="status"
                  className="absolute right-3 top-3 border-4 border-ink bg-sun px-2 py-1 font-pixel text-[9px] uppercase text-ink"
                >
                  Updating…
                </div>
              )}
            </div>

            {error && (
              <p role="alert" className="mt-4 border-4 border-ink bg-blush p-3 text-base text-ink shadow-[4px_4px_0_0_#0d0814]">
                Could not compute this run: {error}. Change an input and try again.
              </p>
            )}

            <p className="mt-4 text-sm leading-snug text-mute">
              <strong className="font-pixel text-[9px] font-normal uppercase text-sun">Basemap </strong>
              {synthetic ? (
                "synthetic development terrain, not Mars data. "
              ) : basemapKind === "photo" ? (
                <>
                  real HiRISE orthophoto of this exact 2 km window (NASA/JPL-Caltech/University of Arizona; USGS
                  Astrogeology Mars 2020 TRN orthomosaic, DOI 10.5066/P9QJDP48), north up, shown as captured, with
                  no colour added.
                  {basemapMeta?.points?.centre &&
                    ` Window centre ${fmtLatLon(basemapMeta.points.centre.lat, basemapMeta.points.centre.lon)}.`}{" "}
                </>
              ) : (
                <>
                  shaded relief derived from the coarse 20 m DEM, which is derived from the Mars 2020 TRN HiRISE DTM
                  of Jezero crater (USGS Astrogeology, from NASA HiRISE stereo images; DOI 10.5066/P9REJ9JN). Local
                  metres, Jezero crater.{" "}
                </>
              )}
              Explore the planet in{" "}
              <a href="https://trek.nasa.gov/mars/" target="_blank" rel="noreferrer">
                NASA Mars Trek
              </a>
              . NASA does not endorse this website.
            </p>

            <p className="mt-3 text-sm leading-snug text-mute">
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

        <aside className="space-y-8">
          <Card title="Inputs">
            <ControlPanel params={params} onChange={setParam} />
          </Card>
          <Card title="Reliability">
            <ReliabilityChart bins={run?.calibration?.bins} />
          </Card>
          <Card title="Route check">
            <RouteFeasibilityPanel params={params} />
          </Card>
          <Card>
            <ExplainPanel onExplain={handleExplain} text={explanation} loading={explaining} disabled={!run} />
          </Card>
        </aside>
      </main>

      <footer className="mx-auto max-w-[1400px] px-6 pb-10 text-center font-pixel text-[8px] uppercase leading-relaxed text-mute">
        NASA Space Apps Challenge 2026 &middot; Interplanetary Survival Guide &middot; Planning aid, not flight software
      </footer>
    </div>
  );
}
