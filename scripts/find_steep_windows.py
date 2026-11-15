"""Find the steepest 2 km windows in a 1 m DTM, for validating on terrain where the slope cutoff matters.

Reads the DTM in row strips, block-averages to the 20 m truth grid (same as build_terrain.py), ranks windows
with walkback.pipeline.steep_windows, and prints ready-to-run build_terrain.py commands.

Usage (repo root):
    PYTHONPATH=src python scripts/find_steep_windows.py --dtm path/to/dtm.tif --top 3

Offsets printed are 1 m pixel offsets from the raster origin, multiples of 20, so they line up with the 20 m
blocks used here. Check CRS, bounds and the picked window by eye before you trust it. Which window is "steep" is
chosen from the same truth you then validate on, so say so in the report: this selects for informative terrain,
it is not a random sample of terrain.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window as RWindow

from walkback.pipeline.build import FINE_CELL_M, GRID
from walkback.pipeline.steep_windows import rank_windows

K = int(FINE_CELL_M)


def load_z20(dtm: Path, strip_blocks: int = 100) -> np.ndarray:
    """20 m block means of the whole DTM. A block with any nodata pixel becomes NaN."""
    with rasterio.open(dtm) as src:
        if abs(abs(src.res[0]) - 1.0) > 1e-6 or abs(abs(src.res[1]) - 1.0) > 1e-6:
            raise SystemExit(f"expected 1 m pixels, got {src.res}; window offsets would be wrong")
        h, w = src.height // K * K, src.width // K * K
        nodata = src.nodata
        rows = []
        for r0 in range(0, h, K * strip_blocks):
            hh = min(K * strip_blocks, h - r0)
            z = src.read(1, window=RWindow(0, r0, w, hh)).astype(np.float64)
            if nodata is not None:
                z[z == nodata] = np.nan
            rows.append(z.reshape(hh // K, K, w // K, K).mean(axis=(1, 3)))
    return np.vstack(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dtm", required=True, type=Path)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--cutoff-deg", type=float, default=20.0)
    ap.add_argument("--stride", type=int, default=25, help="window step in 20 m cells (25 = 500 m)")
    ap.add_argument("--min-steep", type=float, default=0.02, help="min share of cells at or above the cutoff")
    ap.add_argument("--max-steep", type=float, default=0.6, help="max share; mostly-steep windows are uninformative")
    ap.add_argument("--allow-steep-center", action="store_true", help="do not require the habitat cell to be walkable")
    ap.add_argument("--require-planner-center", action="store_true",
                    help="habitat cell must also be below the cutoff in the planner's slope (staircase and grid200)")
    ap.add_argument("--exclude", nargs="*", default=[], metavar="ROW,COL",
                    help="1 m pixel offsets (row,col) of windows already analysed; overlapping candidates are skipped")
    ap.add_argument("--tile-prefix", default="steep")
    ap.add_argument("--site", default="HiRISE Jezero DTM", help="text used in the tile label")
    args = ap.parse_args()

    z20 = load_z20(args.dtm)
    print(f"DTM on the 20 m grid: {z20.shape[0]} x {z20.shape[1]} cells, {np.isnan(z20).mean() * 100:.1f} % nodata")
    wins = rank_windows(
        z20, FINE_CELL_M, GRID, args.cutoff_deg, args.stride, args.top,
        args.min_steep, args.max_steep, require_walkable_center=not args.allow_steep_center,
        require_planner_center=args.require_planner_center,
        exclude=[(int(a.split(",")[0]) // K, int(a.split(",")[1]) // K) for a in args.exclude],
    )
    if not wins:
        raise SystemExit("no window met the filters; relax --min-steep/--max-steep or --stride")

    print(f"\nTop {len(wins)} windows (cutoff {args.cutoff_deg} deg, non-overlapping):\n")
    print("| # | row-off (px) | col-off (px) | share >= cutoff | mean (deg) | p95 (deg) | habitat cell (deg) | planner staircase (deg) | planner grid200 (deg) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i, w in enumerate(wins, 1):
        print(f"| {i} | {w.row * K} | {w.col * K} | {w.steep_share * 100:.1f} % | {w.mean_deg:.1f} "
              f"| {w.p95_deg:.1f} | {w.center_deg:.1f} | {w.planner_stair_deg:.1f} | {w.planner_g200_deg:.1f} |")

    print("\nBuild each tile:\n")
    for i, w in enumerate(wins, 1):
        print(f"PYTHONPATH=src python scripts/build_terrain.py --dtm {args.dtm} "
              f"--row-off {w.row * K} --col-off {w.col * K} --tile-id {args.tile_prefix}-{i} "
              f'--label "{args.site}, 2 km window {i} (selected for steepness), degraded to 200 m planner"')


if __name__ == "__main__":
    main()
