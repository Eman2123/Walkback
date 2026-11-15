import math

import numpy as np
import pytest

from walkback.compute import compute_run, hurst_subgrid
from walkback.degrade import block_mean
from walkback.tiles import Tile

from walkback.compute import planner_slope
from walkback.slope import slope_deg

BASE = {"budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0, "confidence": 0.7, "roughness": 0.5}


def _block_tile(seed=3):
    """100 x 100 tile whose planner DEM is made of constant 200 m blocks, like the real tile.

    Smooth long waves (what the 200 m model sees) plus short waves of about 180 m (what it averages away).
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:100, 0:100].astype(float)
    p = rng.uniform(0, 2 * np.pi, 4)
    z = 15 * np.sin(2 * np.pi * xx / 60 + p[0]) * np.cos(2 * np.pi * yy / 80 + p[1])
    z += 6 * np.sin(2 * np.pi * xx / 9 + p[2]) * np.sin(2 * np.pi * yy / 11 + p[3])
    small = block_mean(z, 10)
    coarse = np.repeat(np.repeat(small, 10, axis=0), 10, axis=1)
    return Tile("block-test", 20.0, coarse, z, "synthetic test tile")


def _params(tile, cutoff=20.0, **over):
    """Parameters with a habitat cell that is passable at both resolutions and in both planner slope modes."""
    ok = ((slope_deg(tile.fine, 20.0) < cutoff) & (planner_slope(tile.coarse, 20.0, "grid200") < cutoff)
          & (planner_slope(tile.coarse, 20.0, "staircase") < cutoff))
    r, c = min(map(tuple, np.argwhere(ok)), key=lambda rc: (rc[0] - 50) ** 2 + (rc[1] - 50) ** 2)
    return dict(BASE, habitat_row=int(r), habitat_col=int(c), cutoff_deg=cutoff, **over)


def test_sigma_matches_the_registered_formula():
    t = _block_tile()
    for H in (0.5, 0.853):
        s = hurst_subgrid(t.coarse, t.cell_m, H)
        expected = math.sqrt(s["g200"] ** 2 * (10 ** (2 * (1 - H)) - 1) / 2)
        assert s["sigma"] == pytest.approx(expected, rel=1e-9)
        assert s["g20_pred"] == pytest.approx(s["g200"] * 10 ** (1 - H))


def test_no_subgrid_noise_when_h_is_one_or_more():
    t = _block_tile()
    assert hurst_subgrid(t.coarse, t.cell_m, 1.0)["sigma"] == 0.0
    assert hurst_subgrid(t.coarse, t.cell_m, 1.3)["sigma"] == 0.0


def test_hurst_refuses_non_block_dem_and_non_finite_h():
    rng = np.random.default_rng(0)
    with pytest.raises(ValueError):
        hurst_subgrid(rng.random((100, 100)), 20.0, 0.8)
    with pytest.raises(ValueError):
        hurst_subgrid(_block_tile().coarse, 20.0, float("nan"))


def test_hurst_mode_needs_grid200_and_an_exponent():
    t = _block_tile()
    with pytest.raises(ValueError):
        compute_run(t, _params(t), roughness_mode="hurst", hurst=0.8)                       # staircase
    with pytest.raises(ValueError):
        compute_run(t, _params(t), planner_slope_mode="grid200", roughness_mode="hurst")    # no H
    with pytest.raises(ValueError):
        compute_run(t, _params(t), roughness_mode="nonsense")


def test_hurst_run_is_deterministic_ignores_roughness_and_labels_itself():
    t = _block_tile()
    kw = dict(planner_slope_mode="grid200", roughness_mode="hurst", hurst=0.7)
    a = compute_run(t, _params(t, roughness=0.1), **kw)
    b = compute_run(t, _params(t, roughness=0.9), **kw)
    assert a["stats"]["counts"] == b["stats"]["counts"]
    assert a["stats"]["brier"] == b["stats"]["brier"]
    names = [x["name"] for x in a["assumptions"]]
    assert "unresolved_roughness" not in names and "hurst_exponent" in names
    assert a["variant"]["roughness_mode"] == "hurst" and a["variant"]["hurst"] == 0.7


def test_registered_output_has_no_variant_or_field_keys():
    t = _block_tile()
    r = compute_run(t, _params(t))
    assert "variant" not in r and "_fields" not in r
    assert "unresolved_roughness" in [x["name"] for x in r["assumptions"]]


def test_return_fields_exposes_arrays():
    t = _block_tile()
    r = compute_run(t, _params(t), return_fields=True)
    f = r["_fields"]
    assert f["p_reach"].shape == f["truth"].shape == (100, 100)
    assert f["cal"].dtype == bool


def test_hurst_can_flag_cells_where_the_staircase_slope_is_exactly_zero():
    """The blind spot that motivated the variant: multiplicative roughness cannot lift a flat staircase cell."""
    t = _block_tile()
    p = _params(t, cutoff=15.0)
    stair = compute_run(t, p, return_fields=True)["_fields"]
    hurst = compute_run(t, p, planner_slope_mode="grid200", roughness_mode="hurst", hurst=0.5,
                        return_fields=True)["_fields"]
    rows = (np.arange(100) % 10 >= 1) & (np.arange(100) % 10 <= 8)
    interior = np.outer(rows, rows)
    assert np.all(stair["slope_coarse"][interior] == 0.0)
    assert stair["p_steep"][interior].max() == 0.0
    assert hurst["p_steep"][interior].max() > 0.0
