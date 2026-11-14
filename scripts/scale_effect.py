"""Measure the slope scale effect on the real 1 m DTM window and write reports/scale_effect.md.

Usage (repo root, venv active):
    python scripts/scale_effect.py --dtm "<path to .tif>" --row-off 9744 --col-off 9700
"""
import argparse
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window

from walkback.pipeline.build import FINE_CELL_M, GRID
from walkback.pipeline.scale_effect import measure_scale_effect


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dtm", required=True, type=Path)
    ap.add_argument("--row-off", required=True, type=int)
    ap.add_argument("--col-off", required=True, type=int)
    ap.add_argument("--out", type=Path, default=Path("reports/scale_effect.md"))
    args = ap.parse_args()

    side = GRID * int(FINE_CELL_M)
    with rasterio.open(args.dtm) as src:
        z = src.read(1, window=Window(args.col_off, args.row_off, side, side)).astype(np.float64)
        nd = src.nodata
    if nd is not None:
        z[z == nd] = np.nan
    if np.isnan(z).any():
        raise SystemExit("window has nodata; choose another offset")

    res = measure_scale_effect(z, cell_m=1.0)
    lines = [
        "# Slope scale effect (measured on the 2 km window at 1 m)",
        "",
        f"Fit over {len(res['baselines_m'])} baselines: log G = a + b log L, H = b + 1.",
        f"H = {res['H']:.3f}, b = {res['slope_b']:.3f}, R2 = {res['r2']:.3f}.",
        "",
        "| baseline (m) | RMS gradient |",
        "|---|---|",
    ]
    for L, g in zip(res["baselines_m"], res["rms_gradient"]):
        lines.append(f"| {L:g} | {g:.4f} |")
    lines += ["", "Measured from one window. Not a claim about other terrain."]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"H = {res['H']:.3f}, R2 = {res['r2']:.3f}")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
