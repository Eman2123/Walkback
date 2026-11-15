import json
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient

from walkback import api
from walkback.compute import PROFILE_V2, compute_run, compute_run_v2
from walkback.params import param_hash
from walkback.store import RunStore
from walkback.tiles import DEV_TILE_ID, synthetic_tile

P = {"habitat_row": 49, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0,
     "confidence": 0.9, "roughness": 0.5}


def _strip(r):
    r = json.loads(json.dumps(r))
    r["stats"].pop("runtime_ms")
    return r


def test_v2_equals_registered_with_pinned_start_and_labels_itself():
    t = synthetic_tile()
    v2 = compute_run_v2(t, dict(P))
    ref = compute_run(t, dict(P), pin_start=True, direction="back")
    assert v2["stats"]["counts"] == ref["stats"]["counts"] and v2["stats"]["brier"] == ref["stats"]["brier"]
    assert v2["variant"]["profile"] == PROFILE_V2 and v2["variant"]["pin_start"] is True
    names = [a["name"] for a in v2["assumptions"]]
    assert {"start_cell", "return_direction", "mobility_not_modelled"} <= set(names)
    assert all(a["label"] in {"measured", "derived", "assumed"} for a in v2["assumptions"])


def test_return_time_equals_time_from_the_habitat_under_the_linear_model():
    t = synthetic_tile()
    a = compute_run(t, dict(P), direction="out", return_fields=True)["_fields"]
    b = compute_run(t, dict(P), direction="back", return_fields=True)["_fields"]
    assert np.array_equal(a["truth"], b["truth"]) and np.array_equal(a["p_reach"], b["p_reach"])


def test_v1_defaults_are_unchanged():
    t = synthetic_tile()
    r = compute_run(t, dict(P))
    assert "variant" not in r and "start_cell" not in [a["name"] for a in r["assumptions"]]


def test_v2_never_empties_the_calibrated_region_because_of_the_start_cell():
    t = synthetic_tile()
    p = dict(P, roughness=1.0, confidence=0.95)
    r1 = compute_run(t, dict(p), return_fields=True)["_fields"]
    r2 = compute_run_v2(t, dict(p))
    assert r2["stats"]["counts"]["calibrated"] >= int(r1["cal"].sum())


def test_profile_fixed_arguments_cannot_be_overridden():
    with pytest.raises(TypeError):
        compute_run_v2(synthetic_tile(), dict(P), pin_start=False)
    with pytest.raises(TypeError):
        compute_run_v2(synthetic_tile(), dict(P), direction="out")


def test_profile_is_part_of_the_cache_key():
    params = {k: v for k, v in P.items()}
    assert param_hash("jezero-20m", params) != param_hash("jezero-20m", {**params, "profile": PROFILE_V2})


def test_api_serves_v2_by_default(monkeypatch):
    monkeypatch.setenv("WALKBACK_ENV", "dev")
    monkeypatch.setattr(api, "STORE", RunStore())
    c = TestClient(api.app)
    body = {"tile_id": DEV_TILE_ID, **P}
    r = c.post("/api/runs", json=body).json()
    assert r["variant"]["profile"] == "v2"
    assert c.post("/api/runs", json=body).json()["cached"] is True


def test_real_tile_default_setting_is_not_empty_in_v2_and_v1_is_unchanged():
    from walkback.tiles import load_tile
    t = load_tile("jezero-20m", Path("data/processed"))
    if t is None:
        pytest.skip("tile not built")
    p = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0,
         "confidence": 0.9, "roughness": 0.5}
    v1 = compute_run(t, dict(p))
    v2 = compute_run_v2(t, dict(p))
    assert v1["stats"]["counts"]["calibrated"] == 0 and v1["stats"]["coverage"] == 0.0     # registered headline
    assert v2["stats"]["counts"]["calibrated"] > 0 and v2["stats"]["coverage"] > 0.8        # the start-cell fix
    assert v2["stats"]["coverage"] < 0.95                                                   # still a shortfall, said so
