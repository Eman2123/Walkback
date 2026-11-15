"""scripts/build_basemap.py on synthetic Mars-equirectangular GeoTIFFs (no real data needed)."""
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

np = pytest.importorskip("numpy")
rasterio = pytest.importorskip("rasterio")
Image = pytest.importorskip("PIL.Image")
from rasterio.crs import CRS  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
R = 3396190.0


def _crs(lon0=0):
    return CRS.from_proj4(f"+proj=eqc +lat_ts=0 +lat_0=0 +lon_0={lon0} +x_0=0 +y_0=0 +R={R} +units=m +no_defs")


def _write(path, arr, px, ulx, uly, crs):
    with rasterio.open(path, "w", driver="GTiff", height=arr.shape[0], width=arr.shape[1], count=1,
                       dtype=str(arr.dtype), crs=crs, transform=from_origin(ulx, uly, px, px),
                       tiled=True, compress="deflate") as d:
        d.write(arr, 1)


def _run(*args):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "build_basemap.py"), *args],
                          capture_output=True, text=True, env={"PYTHONPATH": str(ROOT / "src"), "PATH": ""})


def test_marker_lands_in_the_right_pixel_and_coordinates_match(tmp_path):
    ulx, uly = math.radians(77.2229) * R, math.radians(18.6693) * R
    _write(tmp_path / "dtm.tif", np.zeros((2300, 2300), "float32"), 1.0, ulx, uly, _crs())
    ortho = np.full((9200, 9200), 90, np.uint8)            # 0.25 m pixels, same upper-left corner
    cx, cy, h = int(1500 / 0.25), int(1200 / 0.25), int(20 / 0.25)   # 40 m marker, 1500 m E, 1200 m S of the corner
    ortho[cy - h:cy + h, cx - h:cx + h] = 250
    _write(tmp_path / "ortho.tif", ortho, 0.25, ulx, uly, _crs())

    r = _run("--dtm", str(tmp_path / "dtm.tif"), "--ortho", str(tmp_path / "ortho.tif"),
             "--row-off", "100", "--col-off", "200", "--out-dir", str(tmp_path))
    assert r.returncode == 0, r.stderr

    img = np.array(Image.open(tmp_path / "basemap-jezero-20m.jpg"))
    assert img.shape == (1000, 1000)
    ys, xs = np.where(img > 170)
    assert abs(ys.mean() - (1200 - 100) / 2) < 1.5 and abs(xs.mean() - (1500 - 200) / 2) < 1.5

    meta = json.loads((tmp_path / "basemap-jezero-20m.json").read_text())
    assert meta["points"]["centre"]["lon"] == pytest.approx(math.degrees((ulx + 200 + 1000) / R), abs=1e-5)
    assert meta["points"]["centre"]["lat"] == pytest.approx(math.degrees((uly - 100 - 1000) / R), abs=1e-5)
    assert meta["sources"]["ortho"]["doi"] == "10.5066/P9QJDP48"


def test_different_projections_stop_the_script_and_write_nothing(tmp_path):
    ulx, uly = math.radians(77.2229) * R, math.radians(18.6693) * R
    _write(tmp_path / "dtm.tif", np.zeros((2100, 2100), "float32"), 1.0, ulx, uly, _crs(0))
    _write(tmp_path / "ortho.tif", np.ones((400, 400), np.uint8), 0.25, ulx, uly, _crs(10))
    r = _run("--dtm", str(tmp_path / "dtm.tif"), "--ortho", str(tmp_path / "ortho.tif"), "--out-dir", str(tmp_path / "out"))
    assert r.returncode != 0 and "different projections" in r.stderr
    assert not (tmp_path / "out").exists()
