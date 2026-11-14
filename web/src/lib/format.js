// Formatting helpers. Every number shown to the user goes through here so units and labels stay consistent.
export const fmtKm2 = (cells, cellM = 20) => ((cells * cellM * cellM) / 1e6).toFixed(2);
export const fmtPct = (x) => (x == null || Number.isNaN(x) ? "n/a" : `${(x * 100).toFixed(1)} %`);
