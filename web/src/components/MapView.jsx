// // Owner: Urooj. SVG map in local metres. Click a cell to place the habitat.
// // Regions come from the API as GeoJSON MultiPolygon in metres (CRS.Simple style, y grows downward).
// const N = 100;

// function toPath(geojson) {
//   if (!geojson || !geojson.coordinates) return "";
//   return geojson.coordinates
//     .map((poly) =>
//       poly
//         .map((ring) => ring.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x} ${y}`).join(" ") + " Z")
//         .join(" ")
//     )
//     .join(" ");
// }

// export default function MapView({ run, habitat, layers, onHabitatClick }) {
//   const cell = run?.tile?.cell_m ?? 20;
//   const size = N * cell;

//   function handleClick(e) {
//     const rect = e.currentTarget.getBoundingClientRect();
//     const col = Math.floor(((e.clientX - rect.left) / rect.width) * N);
//     const row = Math.floor(((e.clientY - rect.top) / rect.height) * N);
//     if (row >= 0 && col >= 0 && row < N && col < N) onHabitatClick(row, col);
//   }

//   const hx = (habitat.habitat_col + 0.5) * cell;
//   const hy = (habitat.habitat_row + 0.5) * cell;

//   return (
//     <svg
//       viewBox={`0 0 ${size} ${size}`}
//       className="mx-auto aspect-square w-full max-w-[720px] cursor-crosshair rounded-lg bg-slate-800"
//       onClick={handleClick}
//       role="img"
//       aria-label="Walkback map. Click to place the habitat."
//     >
//       {run && layers.deterministic && (
//         <path d={toPath(run.regions.deterministic)} fill="rgba(47,111,221,0.35)" />
//       )}
//       {run && layers.calibrated && (
//         <path d={toPath(run.regions.calibrated)} fill="rgba(31,157,85,0.45)" />
//       )}
//       {run && layers.truth && (
//         <path d={toPath(run.regions.truth)} fill="none" stroke="#e07b00" strokeWidth={cell / 6} />
//       )}
//       <circle cx={hx} cy={hy} r={cell * 0.6} fill="#ffffff" />
//       <circle cx={hx} cy={hy} r={cell * 0.35} fill="#1F3A5F" />
//     </svg>
//   );
// }

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
  const line = size / 500;

  const gridLines = [];
  for (let m = 500; m < size; m += 500) gridLines.push(m);

  function handleClick(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const col = Math.floor(((e.clientX - rect.left) / rect.width) * N);
    const row = Math.floor(((e.clientY - rect.top) / rect.height) * N);
    if (row >= 0 && col >= 0 && row < N && col < N) onHabitatClick(row, col);
  }

  const hx = (habitat.habitat_col + 0.5) * cell;
  const hy = (habitat.habitat_row + 0.5) * cell;
  const barX = size * 0.04;
  const barY = size * 0.955;

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      className="mx-auto aspect-square w-full max-w-[720px] cursor-crosshair rounded-xl shadow-inner ring-1 ring-slate-700"
      onClick={handleClick}
      role="img"
      aria-label="Walkback map. Click to place the habitat."
    >
      <defs>
        <radialGradient id="mapbg" cx="50%" cy="50%" r="75%">
          <stop offset="0%" stopColor="#2a374d" />
          <stop offset="100%" stopColor="#121a28" />
        </radialGradient>
      </defs>
      <rect width={size} height={size} fill="url(#mapbg)" />

      {gridLines.map((m) => (
        <g key={m} stroke="#ffffff" strokeOpacity="0.08" strokeWidth={line}>
          <line x1={m} y1={0} x2={m} y2={size} />
          <line x1={0} y1={m} x2={size} y2={m} />
        </g>
      ))}

      {run && layers.deterministic && (
        <path
          d={toPath(run.regions.deterministic)}
          fill="rgba(59,130,246,0.30)"
          stroke="rgba(96,165,250,0.95)"
          strokeWidth={line}
        />
      )}
      {run && layers.calibrated && (
        <path
          d={toPath(run.regions.calibrated)}
          fill="rgba(16,185,129,0.40)"
          stroke="rgba(52,211,153,0.95)"
          strokeWidth={line}
        />
      )}
      {run && layers.truth && (
        <path
          d={toPath(run.regions.truth)}
          fill="none"
          stroke="#f59e0b"
          strokeWidth={line * 1.4}
          strokeDasharray={`${cell * 0.7} ${cell * 0.4}`}
        />
      )}

      {/* Scale bar: 500 m */}
      <g pointerEvents="none">
        <line x1={barX} y1={barY} x2={barX + 500} y2={barY} stroke="#e2e8f0" strokeWidth={line * 2} />
        <line x1={barX} y1={barY - 14} x2={barX} y2={barY + 14} stroke="#e2e8f0" strokeWidth={line * 2} />
        <line x1={barX + 500} y1={barY - 14} x2={barX + 500} y2={barY + 14} stroke="#e2e8f0" strokeWidth={line * 2} />
        <text x={barX + 250} y={barY - 26} textAnchor="middle" fontSize={size / 50} fill="#e2e8f0">
          500 m
        </text>
      </g>

      {/* Habitat marker with a slow pulse */}
      <g pointerEvents="none">
        <circle cx={hx} cy={hy} r={cell * 0.6} fill="none" stroke="#ffffff" strokeWidth={cell / 8}>
          <animate attributeName="r" from={cell * 0.6} to={cell * 2.4} dur="1.8s" repeatCount="indefinite" />
          <animate attributeName="opacity" from="0.8" to="0" dur="1.8s" repeatCount="indefinite" />
        </circle>
        <circle cx={hx} cy={hy} r={cell * 0.7} fill="#ffffff" />
        <circle cx={hx} cy={hy} r={cell * 0.4} fill="#ea580c" />
      </g>
    </svg>
  );
}






