"""Post-hoc diagnostic: why is the default calibrated region empty?

EXPLORATORY, not validation. It does not replace the pre-registered headline in
reports/validation_report.md. See the change log in PREREGISTRATION.md.

Finding it tests: in the registered model the unresolved-roughness factor is also applied to the
habitat cell. In some realizations that makes the start cell impassable, so nothing is reachable.
If the share of such realizations exceeds 1 - confidence, no cell can reach the confidence
threshold, and the calibrated region is empty everywhere, whatever the terrain does.

Usage (repo root):
    PYTHONPATH=src python scripts/start_cell_diagnostic.py
"""
import argparse
from pathlib import Path

import numpy as np

from walkback.compute import ENSEMBLE_K, ENSEMBLE_SEED, compute_run
from walkback.slope import slope_deg
from walkback.tiles import load_tile

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
ROUGHNESS = (0.1, 0.3, 0.5)
CONFIDENCE = (0.5, 0.7, 0.9)


def start_blocked_share(slope_coarse, hab, cutoff, rough):
    """Share of ensemble realizations in which the start cell itself reaches the slope cutoff.

    Uses the same random stream as compute_run (same seed, same draw order).
    """
    rng = np.random.default_rng(ENSEMBLE_SEED)
    blocked = 0
    for _ in range(ENSEMBLE_K):
        factor = np.exp(rough * rng.standard_normal(slope_coarse.shape))
        blocked += (slope_coarse * factor)[hab] >= cutoff
    return blocked / ENSEMBLE_K


def pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-id", default="jezero-20m")
    ap.add_argument("--out", type=Path, default=Path("reports/start_cell_diagnostic.md"))
    args = ap.parse_args()
    tile = load_tile(args.tile_id, args.tile_dir)
    if tile is None:
        raise SystemExit("tile not found")

    hab = (BASE["habitat_row"], BASE["habitat_col"])
    sc = slope_deg(tile.coarse, tile.cell_m)
    lines = [
        "# Start-cell diagnostic (post-hoc, exploratory)",
        "",
        "This is not the validation result. The pre-registered headline in validation_report.md is unchanged.",
        "",
        f"Tile: {tile.label}. Habitat {hab}, coarse slope at the habitat {sc[hab]:.1f} deg, cutoff {BASE['cutoff_deg']} deg.",
        f"Ensemble: {ENSEMBLE_K} realizations, seed {ENSEMBLE_SEED}.",
        "",
        "Registered = the model exactly as run for the report. Pinned = same model, but the habitat cell",
        "keeps its deterministic speed in every realization (the crew is already standing there).",
        "",
        "| roughness | confidence | start cell blocked | registered area (km2) | registered coverage (95 % CI) | pinned area (km2) | pinned coverage (95 % CI) |",
        "|---|---|---|---|---|---|---|",
    ]
    for rough in ROUGHNESS:
        blocked = start_blocked_share(sc, hab, BASE["cutoff_deg"], rough)
        for conf in CONFIDENCE:
            p = dict(BASE, confidence=conf, roughness=rough)
            a = compute_run(tile, dict(p))["stats"]
            b = compute_run(tile, dict(p), pin_start=True)["stats"]
            ci = lambda s: f"{pct(s['coverage'])} ({pct(s['coverage_ci'][0])} to {pct(s['coverage_ci'][1])})"
            lines.append(
                f"| {rough} | {conf} | {pct(blocked)} | {a['area_km2']['calibrated']:.3f} | {ci(a)} "
                f"| {b['area_km2']['calibrated']:.3f} | {ci(b)} |"
            )
    lines += [
        "",
        "How to read it:",
        "",
        "- A row is empty in the registered model when the start-cell blocked share is above 1 minus the confidence.",
        "  Then even the habitat cell cannot reach the confidence threshold.",
        "- Rows where pinned coverage is still below 95 % are still shortfalls. Report them as shortfalls.",
        "- All speeds, cutoffs and roughness values are assumptions. This is one 2 km window of one terrain class.",
        "- This table was produced after the headline result was known. It explains the headline; it does not replace it.",
        "",
    ]
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
