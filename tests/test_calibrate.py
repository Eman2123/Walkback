import numpy as np
from walkback.calibrate import brier, coverage

def test_brier_perfect():
    p = np.array([0.0, 1.0]); y = np.array([0.0, 1.0])
    assert brier(p, y) == 0.0

def test_coverage_full():
    truth = np.array([True, True, False])
    pred = np.array([True, True, True])
    assert coverage(pred, truth) == 1.0
