import numpy as np

from walkback.compute import compute_run, runs_to_geojson, travel_time, wilson_ci
from walkback.tiles import synthetic_tile

PARAMS = {
    "habitat_row": 49, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
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


def test_pin_start_is_off_by_default_so_registered_result_is_unchanged():
    tile = synthetic_tile()
    default = compute_run(tile, PARAMS)
    explicit = compute_run(tile, PARAMS, pin_start=False)
    assert default["stats"]["counts"] == explicit["stats"]["counts"]
    assert default["stats"]["coverage"] == explicit["stats"]["coverage"]
    assert default["stats"]["brier"] == explicit["stats"]["brier"]


def test_default_jezero_headline_is_empty_because_the_start_cell_is_rerolled():
    """Regression test for the post-hoc finding in reports/start_cell_diagnostic.md.

    Registered model: the habitat cell is blocked in 2 of 16 realizations (12.5 %), above 1 - 0.9,
    so the calibrated region is empty. Pinning the start cell gives a non-empty region that still
    misses the 95 % target (a shortfall, reported as such).
    """
    import pytest
    from walkback.tiles import DEFAULT_TILE_DIR, load_tile

    tile = load_tile("jezero-20m", DEFAULT_TILE_DIR)
    if tile is None:
        pytest.skip("real tile not built")
    p = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
         "cutoff_deg": 20.0, "confidence": 0.9, "roughness": 0.5}
    registered = compute_run(tile, dict(p))["stats"]
    pinned = compute_run(tile, dict(p), pin_start=True)["stats"]
    assert registered["counts"]["calibrated"] == 0
    assert pinned["counts"]["calibrated"] > 0
    assert pinned["coverage"] < 0.95
