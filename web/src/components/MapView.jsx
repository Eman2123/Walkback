// Owner: Urooj. SVG map in local metres. Click a cell to place the habitat.
// Basemap order: real HiRISE orthophoto (public/basemap-<tile>.jpg), then shaded relief from the API, then plain.
// Regions come from the API as GeoJSON MultiPolygon in metres (CRS.Simple style, y grows downward).
import { useEffect, useState } from "react";
import { basemapUrl, reliefUrl } from "../lib/api.js";

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

export default function MapView({ run, habitat, layers, onHabitatClick, tileId: fallbackTileId, onBasemapChange }) {
  const cell = run?.tile?.cell_m ?? 20;
  // The basemap belongs to the tile, not to a run, so it still shows when a run fails.
  const tileId = run?.tile?.id ?? fallbackTileId;
  const [photoOk, setPhotoOk] = useState(true);
  const [reliefOk, setReliefOk] = useState(true);
  // A new tile gets a fresh attempt; a recorded demo has no real terrain to draw.
  useEffect(() => {
    setPhotoOk(true);
    setReliefOk(true);
  }, [tileId]);
  const showPhoto = Boolean(!run?.demo && tileId && photoOk);
  const showRelief = Boolean(!run?.demo && tileId && !showPhoto && reliefOk);
  const showImage = showPhoto || showRelief;
  const kind = showPhoto ? "photo" : showRelief ? "relief" : "none";
  // Tell the page which basemap is really on screen, so its caption never describes the wrong one.
  useEffect(() => {
    onBasemapChange?.(kind);
  }, [kind]);
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

  const px = cell * 0.9; // habitat marker, one block
  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      className="px-map mx-auto aspect-square w-full max-w-[720px] cursor-crosshair border-4 border-ink shadow-[6px_6px_0_0_#0d0814]"
      onClick={handleClick}
      role="img"
      aria-label="Walkback map. Click to place the habitat."
      shapeRendering="crispEdges"
    >
      <rect width={size} height={size} fill="#1b1226" />
      {showImage && (
        <image
          key={showPhoto ? "photo" : "relief"}
          href={showPhoto ? basemapUrl(tileId) : reliefUrl(tileId)}
          x={0}
          y={0}
          width={size}
          height={size}
          preserveAspectRatio="none"
          onError={() => (showPhoto ? setPhotoOk(false) : setReliefOk(false))}
        />
      )}

      {gridLines.map((m) => (
        <g key={m} stroke="#f5e6c8" strokeOpacity={showImage ? 0.22 : 0.1} strokeWidth={line} strokeDasharray={`${cell * 0.5} ${cell * 0.5}`}>
          <line x1={m} y1={0} x2={m} y2={size} />
          <line x1={0} y1={m} x2={size} y2={m} />
        </g>
      ))}

      {run && layers.deterministic && (
        <path d={toPath(run.regions.deterministic)} fill="rgba(76,201,240,0.30)" stroke="#4cc9f0" strokeWidth={line * 1.2} />
      )}
      {run && layers.calibrated && (
        <path d={toPath(run.regions.calibrated)} fill="rgba(94,234,138,0.42)" stroke="#5eea8a" strokeWidth={line * 1.2} />
      )}
      {run && layers.truth && (
        <path
          d={toPath(run.regions.truth)}
          fill="none"
          stroke="#ffd23f"
          strokeWidth={line * 1.6}
          strokeDasharray={`${cell * 0.7} ${cell * 0.4}`}
        />
      )}

      {/* Scale bar: 500 m, built from blocks */}
      <g pointerEvents="none">
        <rect x={barX - 20} y={barY - size / 20} width={540} height={size / 20 + 28} fill="#0d0814" fillOpacity="0.78" />
        {[0, 1, 2, 3, 4].map((i) => (
          <rect key={i} x={barX + i * 100} y={barY - 10} width={100} height={20} fill={i % 2 ? "#ffd23f" : "#f5e6c8"} stroke="#0d0814" strokeWidth={line * 2} />
        ))}
        <text x={barX + 250} y={barY - 20} textAnchor="middle" fontSize={size / 40} fill="#f5e6c8" fontFamily='"Press Start 2P", monospace'>
          500 m
        </text>
      </g>

      {/* Habitat: a blinking block with a dark outline */}
      <g pointerEvents="none">
        <rect x={hx - px * 1.1} y={hy - px * 1.1} width={px * 2.2} height={px * 2.2} fill="#0d0814" />
        <rect x={hx - px * 0.8} y={hy - px * 0.8} width={px * 1.6} height={px * 1.6} fill="#f5e6c8" />
        <rect x={hx - px * 0.4} y={hy - px * 0.4} width={px * 0.8} height={px * 0.8} fill="#ff7b3a" className="px-blink" />
      </g>
    </svg>
  );
}
