import math

import numpy as np
import pytest

from walkback.compute import compute_run_v2, speed_field, travel_time
from walkback.slope import slope_deg
from walkback.tiles import synthetic_tile
from walkback.validation.route_feasibility import (
    planner_tree, route_feasibility, truth_time_along_tree,
)

PARAMS = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0,
          "confidence": 0.7, "roughness": 0.3}


def _habitat_ok_tile():
    t = synthetic_tile()
    from walkback.compute import planner_slope
    ok = (slope_deg(t.fine, t.cell_m) < 20) & (planner_slope(t.coarse, t.cell_m) < 20)
    r, c = min(map(tuple, np.argwhere(ok)), key=lambda rc: (rc[0] - 50) ** 2 + (rc[1] - 50) ** 2)
    return t, dict(PARAMS, habitat_row=int(r), habitat_col=int(c))


def test_tree_times_equal_travel_time():
    t, p = _habitat_ok_tile()
    sp = speed_field(slope_deg(t.coarse, t.cell_m), 0.5, 20.0)
    hab = (p["habitat_row"], p["habitat_col"])
    T, parent, order = planner_tree(sp, hab, t.cell_m)
    ref = travel_time(sp, hab, t.cell_m)
    assert np.allclose(T[np.isfinite(ref)], ref[np.isfinite(ref)])
    assert np.array_equal(np.isfinite(T), np.isfinite(ref))


def test_truth_equal_to_planner_gives_planner_times():
    t, p = _habitat_ok_tile()
    sp = speed_field(slope_deg(t.coarse, t.cell_m), 0.5, 20.0)
    hab = (p["habitat_row"], p["habitat_col"])
    T, parent, order = planner_tree(sp, hab, t.cell_m)
    tt = truth_time_along_tree(sp, parent, order, hab, t.cell_m)
    fin = np.isfinite(T)
    assert np.allclose(tt[fin], T[fin])


def test_route_through_truth_wall_is_blocked():
    sp = np.full((5, 5), 0.5)
    truth = sp.copy()
    truth[:, 2] = 0.0                      # a wall the planner does not know about
    T, parent, order = planner_tree(sp, (2, 0), 20.0)
    tt = truth_time_along_tree(truth, parent, order, (2, 0), 20.0)
    assert math.isinf(tt[2, 4]) and math.isfinite(tt[2, 1])
    region = np.ones((5, 5), dtype=bool)
    res = route_feasibility(region, T, tt, 1e9)
    assert res["blocked"] > 0 and res["feasible"] + res["blocked"] + res["too_slow"] == res["n"]


def test_slow_truth_is_too_slow_not_blocked():
    sp = np.full((3, 6), 0.5)
    truth = np.full((3, 6), 0.25)
    T, parent, order = planner_tree(sp, (1, 0), 20.0)
    tt = truth_time_along_tree(truth, parent, order, (1, 0), 20.0)
    assert np.allclose(tt[1, 5], 2 * T[1, 5])
    res = route_feasibility(np.ones((3, 6), dtype=bool), T, tt, T[1, 5] * 1.5)
    assert res["blocked"] == 0 and res["too_slow"] > 0
    assert res["ratio_median"] == pytest.approx(2.0)


def test_feasible_share_at_most_area_coverage_complement():
    t, p = _habitat_ok_tile()
    res = compute_run_v2(t, p, return_fields=True)
    f = res["_fields"]
    sp = speed_field(f["slope_coarse"], p["speed_mps"], p["cutoff_deg"])
    hab = (p["habitat_row"], p["habitat_col"])
    T, parent, order = planner_tree(sp, hab, t.cell_m)
    tt = truth_time_along_tree(speed_field(f["slope_fine"], p["speed_mps"], p["cutoff_deg"]), parent, order, hab, t.cell_m)
    cal = f["cal"].copy()
    cal[hab] = False
    out = route_feasibility(cal, T, tt, p["budget_s"])
    if out["n"]:
        truly = (f["truth"] & cal).sum()
        assert out["feasible"] <= truly
