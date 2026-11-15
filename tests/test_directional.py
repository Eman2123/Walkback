import math

import numpy as np
import pytest

from walkback.compute import (
    NEIGHBOURS, NEIGHBOURS16, compute_run, edge_factors, minetti_cost, minetti_factor, travel_time,
)
from walkback.tiles import synthetic_tile

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0,
        "confidence": 0.7, "roughness": 0.3}


def _tile():
    t = synthetic_tile()
    return t


def _params(t):
    from walkback.compute import planner_slope
    from walkback.slope import slope_deg
    ok = (slope_deg(t.fine, t.cell_m) < 20) & (planner_slope(t.coarse, t.cell_m) < 20)
    r, c = min(map(tuple, np.argwhere(ok)), key=lambda rc: (rc[0] - 50) ** 2 + (rc[1] - 50) ** 2)
    return dict(BASE, habitat_row=int(r), habitat_col=int(c))


def test_minetti_polynomial_matches_the_paper_endpoints():
    assert minetti_cost(0.0) == pytest.approx(2.5)
    assert minetti_cost(0.45) == pytest.approx(17.6, abs=0.1)    # measured 17.33
    assert minetti_cost(-0.45) == pytest.approx(3.6, abs=0.1)    # measured 3.46
    assert minetti_cost(1.0) == minetti_cost(0.45)               # clipped to the fitted range


def test_minetti_factor_is_one_on_flat_ground_and_slower_uphill():
    assert minetti_factor(0.0) == pytest.approx(1.0)
    assert minetti_factor(0.2) < 1.0 < minetti_factor(-0.2)


def test_defaults_equal_explicit_registered_options():
    t = _tile()
    p = _params(t)
    a = compute_run(t, p)
    b = compute_run(t, p, solver="dijkstra8", speed_model="linear", direction="out")
    for r in (a, b):
        r["stats"].pop("runtime_ms")
    assert a == b
    assert "variant" not in a


def test_unknown_options_are_rejected():
    t = _tile()
    p = _params(t)
    for kw in ({"solver": "x"}, {"speed_model": "x"}, {"direction": "x"}):
        with pytest.raises(ValueError):
            compute_run(t, p, **kw)


def test_linear_speed_gives_equal_out_and_back():
    t = _tile()
    p = _params(t)
    out = compute_run(t, p, direction="out", return_fields=True)["_fields"]
    back = compute_run(t, p, direction="back", return_fields=True)["_fields"]
    assert np.array_equal(out["p_reach"], back["p_reach"])


def _flat_time(neigh, n=101, cell=20.0, v=0.5):
    speed = np.full((n, n), v)
    return travel_time(speed, (n // 2, n // 2), cell, neigh)


def test_sixteen_neighbours_cut_the_path_error():
    n, cell, v = 101, 20.0, 0.5
    yy, xx = np.mgrid[0:n, 0:n]
    dist = np.hypot(yy - n // 2, xx - n // 2) * cell
    straight = dist / v
    m = dist > 0
    err8 = (_flat_time(NEIGHBOURS)[m] / straight[m]).max() - 1
    err16 = (_flat_time(NEIGHBOURS16)[m] / straight[m]).max() - 1
    assert err8 == pytest.approx(0.082, abs=0.005)
    assert err16 < 0.03
    # reach area moves closer to the true circle
    budget = 900.0
    true_area = math.pi * (budget * v) ** 2
    a8 = (_flat_time(NEIGHBOURS) <= budget).sum() * cell * cell
    a16 = (_flat_time(NEIGHBOURS16) <= budget).sum() * cell * cell
    assert abs(a16 - true_area) < abs(a8 - true_area)


def test_knight_move_does_not_cut_through_a_wall():
    v = np.full((5, 5), 0.5)
    v[0:4, 1] = 0.0                       # wall in column 1, gap only in row 4
    T = travel_time(v, (0, 0), 20.0, NEIGHBOURS16)
    direct = 20.0 * math.sqrt(5) / 0.5    # what a knight jump across the wall would cost
    assert T[1, 2] > 3 * direct           # it has to go round through the gap
    assert np.isfinite(T[1, 2])


def _ramp(n=21, grade=0.2, cell=20.0):
    cols = np.arange(n) * cell * grade
    return np.tile(cols, (n, 1))          # rises to the right


def test_uphill_is_slower_than_downhill_and_back_reverses_it():
    z = _ramp()
    speed = np.full(z.shape, 0.5)
    hab_left, hab_right = (10, 0), (10, 20)
    f_out = edge_factors(z, 20.0, NEIGHBOURS, "out")
    f_back = edge_factors(z, 20.0, NEIGHBOURS, "back")
    up = travel_time(speed, hab_left, 20.0, NEIGHBOURS, f_out)[10, 20]       # walk up from the left
    down = travel_time(speed, hab_right, 20.0, NEIGHBOURS, f_out)[10, 0]     # walk down from the right
    assert up > down
    # return time to the left habitat from the right end = walking down it... which is the "down" time, not "up"
    back_to_left = travel_time(speed, hab_left, 20.0, NEIGHBOURS, f_back)[10, 20]
    assert back_to_left == pytest.approx(down)
    # and the symmetric speed makes no difference between the directions
    sym = travel_time(speed, hab_left, 20.0, NEIGHBOURS)[10, 20]
    assert sym == pytest.approx(travel_time(speed, hab_right, 20.0, NEIGHBOURS)[10, 0])


def test_cap_removes_the_downhill_speedup():
    z = _ramp(grade=0.1)
    f = edge_factors(z, 20.0, [(0, 1)], "out", cap=True)[(0, 1)]
    g = edge_factors(z, 20.0, [(0, -1)], "out", cap=True)[(0, -1)]
    assert max(max(row) for row in f) <= 1.0 and max(max(row) for row in g) <= 1.0
    assert min(min(row[:-1]) for row in f) < 1.0     # uphill penalty remains


def test_variant_run_labels_itself_and_keeps_the_registered_region_shape():
    t = _tile()
    p = _params(t)
    r = compute_run(t, p, solver="dijkstra16", speed_model="minetti_cap", direction="back")
    assert r["variant"] == {"solver": "dijkstra16", "speed_model": "minetti_cap", "direction": "back"}
    assert any(a["name"] == "directional_speed" for a in r["assumptions"])
    assert r["stats"]["counts"]["calibrated"] >= 0
