// Formatting helpers. Every number shown to the user goes through here so units and labels stay consistent.
export const fmtKm2 = (km2) => (km2 == null ? "n/a" : Number(km2).toFixed(2));
export const fmtPct = (x) => (x == null || Number.isNaN(x) ? "n/a" : `${(x * 100).toFixed(1)} %`);
export const fmtCI = (ci) =>
  !ci || ci[0] == null ? "" : ` (CI ${(ci[0] * 100).toFixed(0)}–${(ci[1] * 100).toFixed(0)} %)`;

export const LABEL_CLASS = {
  measured: "bg-emerald-100 text-emerald-800",
  derived: "bg-blue-100 text-blue-800",
  assumed: "bg-rose-100 text-rose-800",
};
