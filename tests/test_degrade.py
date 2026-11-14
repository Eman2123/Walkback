import numpy as np
from walkback.degrade import block_mean

def test_block_mean_shape_and_value():
    z = np.arange(16, dtype=float).reshape(4, 4)
    out = block_mean(z, 2)
    assert out.shape == (2, 2)
    assert out[0, 0] == np.mean([0, 1, 4, 5])
