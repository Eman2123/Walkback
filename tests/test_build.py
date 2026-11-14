import numpy as np
import pytest

from walkback.pipeline.build import build_arrays


def test_build_arrays_shapes_and_degradation():
    rng = np.random.default_rng(0)
    z = rng.normal(size=(2000, 2000)).cumsum(axis=0)
    coarse, fine = build_arrays(z)
    assert coarse.shape == fine.shape == (100, 100)
    # coarse is constant over each 10 x 10 block (200 m model shown on the 20 m grid)
    assert np.allclose(coarse[0:10, 0:10], coarse[0, 0])


def test_build_arrays_rejects_wrong_window():
    with pytest.raises(ValueError):
        build_arrays(np.zeros((1000, 1000)))
