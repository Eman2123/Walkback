import numpy as np

from walkback.pipeline.scale_effect import measure_scale_effect


def test_linear_ramp_has_no_scale_dependence():
    cell = 1.0
    x = np.arange(400) * cell
    z = np.add.outer(0.05 * x, np.zeros(400))  # constant gradient 0.05 at every scale
    res = measure_scale_effect(z, cell_m=cell)
    assert abs(res["slope_b"]) < 1e-6
    assert abs(res["H"] - 1.0) < 1e-6


def test_fit_returns_finite_values_on_rough_terrain():
    rng = np.random.default_rng(0)
    z = rng.normal(size=(400, 400)).cumsum(axis=0).cumsum(axis=1)
    res = measure_scale_effect(z, cell_m=1.0)
    assert np.isfinite(res["H"]) and np.isfinite(res["r2"])
    assert len(res["baselines_m"]) >= 3
