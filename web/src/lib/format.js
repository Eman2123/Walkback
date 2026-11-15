// Formatting helpers. Every number shown to the user goes through here so units and labels stay consistent.
export const fmtKm2 = (km2) => (km2 == null ? "n/a" : Number(km2).toFixed(2));
export const fmtPct = (x) => (x == null || Number.isNaN(x) ? "n/a" : `${(x * 100).toFixed(1)} %`);
export const fmtCI = (ci) =>
  !ci || ci[0] == null ? "" : ` (CI ${(ci[0] * 100).toFixed(0)}–${(ci[1] * 100).toFixed(0)} %)`;

// Solid chips with dark text, used with the .px-chip class.
export const LABEL_CLASS = {
  measured: "bg-neon",
  derived: "bg-aqua",
  assumed: "bg-blush",
};

// Planetocentric degrees, 5 decimals is about 0.6 m on Mars.
export const fmtLatLon = (lat, lon) =>
  lat == null || lon == null
    ? "n/a"
    : `${Math.abs(lat).toFixed(5)}\u00b0${lat >= 0 ? "N" : "S"}, ${Math.abs(lon).toFixed(5)}\u00b0${lon >= 0 ? "E" : "W"}`;

// Lon/lat of the centre of a grid cell. The basemap is an equirectangular crop, so lon and lat are
// linear in the position inside the window. Returns null when no georeference file is available.
export function cellLatLon(meta, row, col, n = 100) {
  const pt = meta?.points;
  if (!pt?.nw || !pt.ne || !pt.sw) return null;
  const fx = (col + 0.5) / n;
  const fy = (row + 0.5) / n;
  return {
    lon: pt.nw.lon + fx * (pt.ne.lon - pt.nw.lon),
    lat: pt.nw.lat + fy * (pt.sw.lat - pt.nw.lat),
  };
}
