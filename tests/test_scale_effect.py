import math
import pytest

from walkback.pipeline.scale_effect import measure_hurst


def test_measure_hurst_linear_log_relationship():
    values = {
        1: 2,
        10: 20,
        100: 200,
    }

    assert measure_hurst(values) == pytest.approx(1.0)


def test_measure_hurst_constant_values():
    values = {
        1: 5,
        10: 5,
        100: 5,
    }

    assert measure_hurst(values) == pytest.approx(0.0)


def test_measure_hurst_requires_two_measurements():
    with pytest.raises(ValueError):
        measure_hurst({1: 2})


def test_measure_hurst_rejects_zero_slope():
    with pytest.raises(ValueError):
        measure_hurst({1: 0, 10: 2})


def test_measure_hurst_rejects_invalid_scale():
    with pytest.raises(ValueError):
        measure_hurst({0: 2, 10: 4})
