import math

import numpy as np
import pytest

from walkback.validation.metrics import (
    CONF_CURVE,
    block_bootstrap_ci,
    brier_skill_score,
    coverage_by_confidence,
    reach_reliability,
    wider_interval,
)


def test_brier_skill_score():
    assert brier_skill_score(0.0, 0.002) == 1.0
    assert brier_skill_score(0.002, 0.002) == 0.0
    assert brier_skill_score(0.0157, 0.0020) < 0          # worse than saying "never steep"
    assert math.isnan(brier_skill_score(0.1, 0.0))


def test_block_bootstrap_is_degenerate_when_region_equals_truth():
    truth = np.zeros((100, 100), dtype=bool)
    truth[10:60, 10:60] = True
    lo, hi, used = block_bootstrap_ci(truth.copy(), truth, n_boot=200)
    assert (lo, hi) == (1.0, 1.0) and used > 0


def test_block_bootstrap_is_wider_than_zero_when_coverage_varies_by_block():
    rng = np.random.default_rng(0)
    truth = np.ones((100, 100), dtype=bool)
    cal = np.zeros_like(truth)
    cal[:, :50] = True                                   # left half covered, right half not
    lo, hi, _ = block_bootstrap_ci(cal, truth, n_boot=1000)
    assert lo < 0.5 < hi and hi - lo > 0.05


def test_block_bootstrap_is_deterministic_and_handles_empty_truth():
    truth = np.zeros((100, 100), dtype=bool)
    truth[:50] = True
    cal = np.zeros_like(truth)
    cal[:30] = True
    assert block_bootstrap_ci(cal, truth) == block_bootstrap_ci(cal, truth)
    assert block_bootstrap_ci(cal, np.zeros_like(truth)) == (None, None, 0)


def test_block_bootstrap_rejects_shape_mismatch():
    with pytest.raises(ValueError):
        block_bootstrap_ci(np.zeros((10, 10), bool), np.zeros((20, 20), bool))


def test_coverage_never_rises_with_the_confidence_threshold():
    rng = np.random.default_rng(1)
    p = rng.random((60, 60))
    truth = rng.random((60, 60)) < 0.4
    rows = coverage_by_confidence(p, truth)
    assert [r["threshold"] for r in rows] == list(CONF_CURVE)
    covs = [r["coverage"] for r in rows]
    assert all(a >= b for a, b in zip(covs, covs[1:]))
    cells = [r["cells"] for r in rows]
    assert all(a >= b for a, b in zip(cells, cells[1:]))


def test_reach_reliability_bins_cover_every_cell():
    rng = np.random.default_rng(2)
    p = rng.random((40, 40))
    truth = rng.random((40, 40)) < p                      # perfectly calibrated by construction
    bins = reach_reliability(p, truth)
    assert sum(b["n"] for b in bins) == p.size
    assert all(abs(b["pred"] - b["obs"]) < 0.12 for b in bins)


def test_wider_interval():
    assert wider_interval((0.1, 0.4), (0.2, 0.5)) == (0.1, 0.5)
    assert wider_interval((None, None), (0.2, 0.5)) == (0.2, 0.5)
    assert wider_interval((0.2, 0.5), (None, None)) == (0.2, 0.5)
