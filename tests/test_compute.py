import numpy as np

from walkback.compute import compute_run, runs_to_geojson, travel_time, wilson_ci
from walkback.tiles import synthetic_tile

PARAMS = {
    "habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
    "cutoff_deg": 20, "confidence": 0.9, "roughness": 0.5,
}


def test_travel_time_zero_at_habitat_and_inf_when_blocked():
    speed = np.ones((5, 5))
    speed[:, 2] = 0  # a wall
    T = travel_time(speed, (0, 0), 10.0)
    assert T[0, 0] == 0.0
    assert np.isinf(T[0, 4])


def test_geojson_runs_have_expected_area():
    mask = np.zeros((4, 4), dtype=bool)
    mask[1, 1:3] = True  # one run of 2 cells
    gj = runs_to_geojson(mask, 10.0)
    assert gj["type"] == "MultiPolygon" and len(gj["coordinates"]) == 1
    xs = [p[0] for p in gj["coordinates"][0][0]]
    assert max(xs) - min(xs) == 20.0


def test_wilson_ci_bounds():
    lo, hi = wilson_ci(90, 100)
    assert 0.8 < lo < 0.9 < hi < 0.97


def test_compute_run_is_deterministic_and_reports_labels():
    tile = synthetic_tile()
    a = compute_run(tile, PARAMS)
    b = compute_run(tile, PARAMS)
    assert a["stats"]["counts"] == b["stats"]["counts"]
    assert a["calibration"]["brier"] == b["calibration"]["brier"]
    assert a["stats"]["counts"]["deterministic"] > 0


def test_synthetic_tile_shapes():
    t = synthetic_tile()
    assert t.coarse.shape == (100, 100) and t.fine.shape == (100, 100)
