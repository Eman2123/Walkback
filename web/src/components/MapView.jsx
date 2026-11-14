// Owner: Urooj. SVG map in local metres. Click a cell to place the habitat.
// Regions come from the API as GeoJSON MultiPolygon in metres (CRS.Simple style, y grows downward).
const N = 100;

function toPath(geojson) {
  if (!geojson || !geojson.coordinates) return "";
  return geojson.coordinates
    .map((poly) =>
      poly
        .map((ring) => ring.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x} ${y}`).join(" ") + " Z")
        .join(" ")
    )
    .join(" ");
}

export default function MapView({ run, habitat, layers, onHabitatClick }) {
  const cell = run?.tile?.cell_m ?? 20;
  const size = N * cell;

  function handleClick(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const col = Math.floor(((e.clientX - rect.left) / rect.width) * N);
    const row = Math.floor(((e.clientY - rect.top) / rect.height) * N);
    if (row >= 0 && col >= 0 && row < N && col < N) onHabitatClick(row, col);
  }

  const hx = (habitat.habitat_col + 0.5) * cell;
  const hy = (habitat.habitat_row + 0.5) * cell;

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      className="mx-auto aspect-square w-full max-w-[720px] cursor-crosshair rounded-lg bg-slate-800"
      onClick={handleClick}
      role="img"
      aria-label="Walkback map. Click to place the habitat."
    >
      {run && layers.deterministic && (
        <path d={toPath(run.regions.deterministic)} fill="rgba(47,111,221,0.35)" />
      )}
      {run && layers.calibrated && (
        <path d={toPath(run.regions.calibrated)} fill="rgba(31,157,85,0.45)" />
      )}
      {run && layers.truth && (
        <path d={toPath(run.regions.truth)} fill="none" stroke="#e07b00" strokeWidth={cell / 6} />
      )}
      <circle cx={hx} cy={hy} r={cell * 0.6} fill="#ffffff" />
      <circle cx={hx} cy={hy} r={cell * 0.35} fill="#1F3A5F" />
    </svg>
  );
}
