import dataclasses

import numpy as np
import pytest

from walkback.compute import compute_run
from walkback.tiles import synthetic_tile

PARAMS = {"habitat_row": 49, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
          "cutoff_deg": 20.0, "confidence": 0.9, "roughness": 0.5}


def test_habitat_steep_only_at_fine_resolution_is_rejected():
    tile = synthetic_tile()
    fine = tile.fine.copy()
    fine[50, 50] += 500.0  # a spike the 200 m model cannot see
    bad = dataclasses.replace(tile, fine=fine)
    with pytest.raises(ValueError, match="fine resolution"):
        compute_run(bad, PARAMS)


def test_default_habitat_on_synthetic_tile_still_runs():
    res = compute_run(synthetic_tile(), PARAMS)
    assert res["stats"]["counts"]["deterministic"] > 0
