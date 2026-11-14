import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from walkback.compute import compute_run
from walkback.db.models import Base
from walkback.db.store_sql import SqlRunStore
from walkback.tiles import synthetic_tile

PARAMS = {
    "habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
    "cutoff_deg": 20, "confidence": 0.9, "roughness": 0.5,
}


def make_store():
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return SqlRunStore(sessionmaker(bind=engine, expire_on_commit=False))


def test_round_trip_matches_original_result():
    store = make_store()
    result = compute_run(synthetic_tile(), PARAMS)
    store.put("run-1", "hash-1", {"run_id": "run-1", "result": result})
    back = store.get("run-1")["result"]
    assert back["stats"]["counts"] == result["stats"]["counts"]
    assert back["regions"]["calibrated"] == result["regions"]["calibrated"]
    assert [a["name"] for a in back["assumptions"]] == [a["name"] for a in result["assumptions"]]
    assert back["calibration"]["brier"] == result["calibration"]["brier"]


def test_lookup_by_hash_and_missing():
    store = make_store()
    result = compute_run(synthetic_tile(), PARAMS)
    store.put("run-2", "hash-2", {"run_id": "run-2", "result": result})
    assert store.get_by_hash("hash-2")["run_id"] == "run-2"
    assert store.get_by_hash("nope") is None
    assert store.get("missing") is None


def test_second_tile_write_reuses_tile_row():
    store = make_store()
    result = compute_run(synthetic_tile(), PARAMS)
    store.put("a", "ha", {"run_id": "a", "result": result})
    store.put("b", "hb", {"run_id": "b", "result": result})
    assert store.get("b") is not None
