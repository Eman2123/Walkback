"""Build a real tile from a 1 m GeoTIFF window (Jezero HiRISE DTM, once downloaded).

Usage (from repo root):
    PYTHONPATH=src python scripts/build_terrain.py \
        --dtm path/to/dtm.tif --row-off 1000 --col-off 1000 --tile-id jezero-20m \
        --label "HiRISE Jezero DTM, 2 km window (USGS), degraded to 200 m planner"

Writes data/processed/<tile-id>.npz with keys coarse, fine, cell_m, label.
The window must be 2000 x 2000 pixels at 1 m. Verify the CRS and bounds before using the output.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window

from walkback.pipeline.build import FINE_CELL_M, GRID, build_arrays


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dtm", required=True, type=Path)
    ap.add_argument("--row-off", required=True, type=int)
    ap.add_argument("--col-off", required=True, type=int)
    ap.add_argument("--tile-id", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out-dir", type=Path, default=Path("data/processed"))
    args = ap.parse_args()

    side = GRID * int(FINE_CELL_M)
    win = Window(args.col_off, args.row_off, side, side)
    with rasterio.open(args.dtm) as src:
        z = src.read(1, window=win).astype(np.float64)
        if src.nodata is not None:
            z[z == src.nodata] = np.nan
    if np.isnan(z).any():
        raise SystemExit("window contains nodata; choose another offset")

    coarse, fine = build_arrays(z)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"{args.tile_id}.npz"
    np.savez(out, coarse=coarse, fine=fine, cell_m=np.float64(FINE_CELL_M), label=np.str_(args.label))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
