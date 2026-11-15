"""Planner-slope variant analysis, as registered in PREREGISTRATION.md (section "Planner-slope variant").

EXPLORATORY. It does not replace reports/validation_report.md and it does not change the API default.

Compares, over the same 9 roughness x confidence combinations as the sensitivity analysis:
  staircase  the registered model (slope from the 200 m blocks drawn on the 20 m grid)
  grid200    slope from the 10 x 10 grid of 200 m block means, 200 m spacing

Reported per row: areas, coverage with its Wilson interval, Brier score, and false reach
(share of calibrated cells that are not reachable in the truth). Every row is reported.

Usage (repo root):
    PYTHONPATH=src python scripts/planner_slope_variant.py
"""
import argparse
from pathlib import Path

import numpy as np

from walkback.compute import compute_run, planner_slope
from walkback.slope import slope_deg
from walkback.tiles import load_tile

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
ROUGHNESS = (0.1, 0.3, 0.5)
CONFIDENCE = (0.5, 0.7, 0.9)
MODES = ("staircase", "grid200")


def pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def cell(mode, tile, p):
    try:
        s = compute_run(tile, dict(p), planner_slope_mode=mode)["stats"]
    except ValueError as exc:
        return f"not computed ({exc})"
    ci = f"{pct(s['coverage'])} ({pct(s['coverage_ci'][0])} to {pct(s['coverage_ci'][1])})"
    return (f"{s['area_km2']['calibrated']:.3f} | {ci} | {pct(s['false_reach'])} | {s['brier']:.4f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-id", default="jezero-20m")
    ap.add_argument("--out", type=Path, default=Path("reports/planner_slope_variant.md"))
    args = ap.parse_args()
    tile = load_tile(args.tile_id, args.tile_dir)
    if tile is None:
        raise SystemExit("tile not found")

    cutoff = BASE["cutoff_deg"]
    sf = slope_deg(tile.fine, tile.cell_m)
    steep_share = float((sf >= cutoff).mean())
    lines = [
        "# Planner-slope variant (exploratory, registered before it was run)",
        "",
        "This is not the validation result. The pre-registered headline in validation_report.md is unchanged.",
        "",
        f"Tile: {tile.label}. Habitat ({BASE['habitat_row']}, {BASE['habitat_col']}), budget {BASE['budget_s']} s, "
        f"speed {BASE['speed_mps']} m/s (assumed), cutoff {cutoff} deg (assumed). 16 realizations, seed 1234.",
        "",
        "## What the planner sees",
        "",
        "| planner slope | mean (deg) | 95th percentile (deg) | share of cells at or above the cutoff | share of cells that are exactly 0 |",
        "|---|---|---|---|---|",
    ]
    for mode in MODES:
        s = planner_slope(tile.coarse, tile.cell_m, mode)
        lines.append(f"| {mode} | {s.mean():.2f} | {np.percentile(s, 95):.2f} "
                     f"| {pct(float((s >= cutoff).mean()))} | {pct(float((s == 0).mean()))} |")
    lines += [
        f"| truth (20 m) | {sf.mean():.2f} | {np.percentile(sf, 95):.2f} "
        f"| {pct(float((sf >= cutoff).mean()))} | {pct(float((sf == 0).mean()))} |",
        "",
        "staircase = the registered model. grid200 = slope on the 200 m block means (200 m spacing).",
        "",
        f"Only {pct(float((sf >= cutoff).mean()))} of the 20 m truth cells reach the {cutoff} deg cutoff. A forecast that always says",
        f"\"never steep\" therefore scores a Brier of {steep_share * (1 - steep_share):.4f}. A Brier at or above this value shows no skill.",
        "",
    ]
    for mode in MODES:
        lines += [
            f"## {mode}",
            "",
            "| roughness | confidence | calibrated area (km2) | coverage (95 % CI) | false reach | Brier |",
            "|---|---|---|---|---|---|",
        ]
        for rough in ROUGHNESS:
            for conf in CONFIDENCE:
                p = dict(BASE, confidence=conf, roughness=rough)
                lines.append(f"| {rough} | {conf} | {cell(mode, tile, p)} |")
        lines.append("")
    lines += [
        "How to read it:",
        "",
        "- Coverage = share of truth-reachable cells that the calibrated region contains. False reach = share of calibrated cells that the truth says are not reachable. High coverage with high false reach means an optimistic planner.",
        "- All rows are reported for both models. No row is chosen as the result.",
        "- Speeds, cutoff and roughness are assumptions. One 2 km window of one terrain class.",
        "- grid200 is exploratory and is not promoted to the default without its own registration.",
        "",
    ]
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
