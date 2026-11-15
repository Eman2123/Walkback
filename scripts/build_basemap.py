"""Crop the real HiRISE orthophoto for the analysis window and write the map basemap.

Why: the map should show the real surface that the DTM describes, in exactly the same footprint
as the 100 x 100 grid, instead of an image derived from the planner's own coarse DEM.

Inputs
    --dtm    the 1 m HiRISE DTM used by scripts/build_terrain.py (same --row-off and --col-off)
    --ortho  the 25 cm HiRISE orthomosaic of the same product (USGS, DOI 10.5066/P9QJDP48).
             It can be a local file or a remote one read by range requests, for example
             /vsicurl/https://planetarymaps.usgs.gov/mosaic/mars2020_trn/HiRISE/JEZ_hirise_soc_006_orthoMosaic_25cm_Eqc_latTs0_lon0_first.tif

The window location is read from the DTM's own georeferencing, not typed in, and the same
bounds are read from the orthomosaic. The script stops if the two files use different projections.

Writes (default): web/public/basemap-jezero-20m.jpg and web/public/basemap-jezero-20m.json.
The JSON holds the corner and centre latitude/longitude, so the frontend can show real coordinates.
The image is the orthophoto as it is: grey, north up, only downsampled (area average). No colour is added.

Usage (repo root):
    PYTHONPATH=src python scripts/build_basemap.py --dtm path/to/dtm.tif --ortho <path or /vsicurl/url> \\
        --row-off 9744 --col-off 9700
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from rasterio.crs import CRS
from rasterio.warp import transform as warp_transform
from rasterio.enums import Resampling
from rasterio.windows import from_bounds

from walkback.pipeline.build import FINE_CELL_M, GRID

MARS_RADIUS_M = 3396190.0
WINDOW_M = GRID * FINE_CELL_M          # 2000 m
DTM_DOI = "10.5066/P9REJ9JN"
ORTHO_DOI = "10.5066/P9QJDP48"


def window_bounds(dtm, row_off: int, col_off: int, side_px: int) -> tuple[float, float, float, float]:
    """(left, bottom, right, top) of the DTM window in the DTM's projected coordinates."""
    t = dtm.transform
    if abs(abs(t.a) - 1.0) > 1e-6 or abs(abs(t.e) - 1.0) > 1e-6:
        raise SystemExit(f"expected a 1 m DTM, got pixel size {abs(t.a)} x {abs(t.e)}")
    if t.b or t.d:
        raise SystemExit("the DTM is rotated; this script expects a north-up grid")
    if row_off < 0 or col_off < 0 or row_off + side_px > dtm.height or col_off + side_px > dtm.width:
        raise SystemExit("the window falls outside the DTM")
    x0, y0 = t * (col_off, row_off)
    x1, y1 = t * (col_off + side_px, row_off + side_px)
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def to_lonlat(crs: CRS, points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Projected (x, y) to planetocentric (lon, lat) in degrees on the Mars sphere."""
    geo = CRS.from_proj4(f"+proj=longlat +R={MARS_RADIUS_M} +no_defs")
    lons, lats = warp_transform(crs, geo, [p[0] for p in points], [p[1] for p in points])
    return list(zip(lons, lats))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dtm", required=True)
    ap.add_argument("--ortho", required=True)
    ap.add_argument("--row-off", type=int, default=9744, help="same value as used for build_terrain.py")
    ap.add_argument("--col-off", type=int, default=9700, help="same value as used for build_terrain.py")
    ap.add_argument("--tile-id", default="jezero-20m")
    ap.add_argument("--size", type=int, default=1000, help="output size in pixels (square)")
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--out-dir", type=Path, default=Path("web/public"))
    args = ap.parse_args()

    side_px = int(WINDOW_M)
    with rasterio.open(args.dtm) as dtm, rasterio.open(args.ortho) as ortho:
        if dtm.crs is None or ortho.crs is None:
            raise SystemExit("a file has no CRS; cannot align them")
        if dtm.crs.to_proj4() != ortho.crs.to_proj4():
            raise SystemExit(
                "the DTM and the orthomosaic use different projections:\n"
                f"  DTM   {dtm.crs.to_proj4()}\n  ortho {ortho.crs.to_proj4()}\n"
                "Reproject one of them first. Nothing was written."
            )
        left, bottom, right, top = window_bounds(dtm, args.row_off, args.col_off, side_px)
        ob = ortho.bounds
        if left < ob.left or right > ob.right or bottom < ob.bottom or top > ob.top:
            raise SystemExit("the window is not inside the orthomosaic; check the offsets. Nothing was written.")

        win = from_bounds(left, bottom, right, top, transform=ortho.transform)
        img = ortho.read(1, window=win, out_shape=(args.size, args.size), resampling=Resampling.average)
        ortho_px = abs(ortho.transform.a)
        crs_proj4 = ortho.crs.to_proj4()

        # Corners in lon/lat. Order: NW, NE, SW, SE, centre.
        pts = [(left, top), (right, top), (left, bottom), (right, bottom), ((left + right) / 2, (bottom + top) / 2)]
        ll = to_lonlat(ortho.crs, pts)

    arr = np.asarray(img)
    if arr.dtype != np.uint8:
        raise SystemExit(f"expected an 8-bit orthophoto, got {arr.dtype}")
    if not np.any(arr):
        raise SystemExit("the cropped image is empty (all zero); check the offsets. Nothing was written.")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"basemap-{args.tile_id}"
    jpg = args.out_dir / f"{stem}.jpg"
    Image.fromarray(arr, mode="L").save(jpg, quality=args.quality, optimize=True)

    names = ["nw", "ne", "sw", "se", "centre"]
    meta = {
        "tile_id": args.tile_id,
        "image": f"{stem}.jpg",
        "size_px": args.size,
        "window_m": WINDOW_M,
        "metres_per_pixel": WINDOW_M / args.size,
        "north_up": True,
        "points": {n: {"lon": round(lon, 6), "lat": round(lat, 6)} for n, (lon, lat) in zip(names, ll)},
        "dtm_offsets_px": {"row": args.row_off, "col": args.col_off},
        "sources": {
            "dtm": {"doi": DTM_DOI, "title": "Mars 2020 TRN HiRISE DTM Mosaic (USGS Astrogeology)"},
            "ortho": {"doi": ORTHO_DOI, "pixel_m": ortho_px,
                      "title": "Mars 2020 TRN HiRISE Orthorectified Image Mosaic (USGS Astrogeology)"},
        },
        "credit": "Image: NASA/JPL-Caltech/University of Arizona, processed by USGS Astrogeology",
        "processing": "cropped to the DTM window, area-average downsample, no colour added",
        "crs_proj4": crs_proj4,
        "generated_by": "scripts/build_basemap.py",
    }
    (args.out_dir / f"{stem}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    c = meta["points"]["centre"]
    print(f"wrote {jpg} and {stem}.json. Window centre {c['lat']:.5f} N, {c['lon']:.5f} E")


if __name__ == "__main__":
    main()
