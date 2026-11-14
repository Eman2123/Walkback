import numpy as np
from walkback.slope import slope_deg

def test_flat_is_zero():
    assert np.allclose(slope_deg(np.zeros((5, 5)), 1.0), 0.0)
