"""Round trip against a real Postgres (Neon). Skipped unless TEST_DATABASE_URL is set.

Run locally:  $env:TEST_DATABASE_URL="postgresql+psycopg://..."; pytest -q tests/test_store_postgres.py
The test writes one run and removes it again.
"""
import os
import uuid

import pytest

from walkback.compute import compute_run
from walkback.tiles import synthetic_tile

URL = os.environ.get("TEST_DATABASE_URL")
PARAMS = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
          "cutoff_deg": 20.0, "confidence": 0.9, "roughness": 0.5}


@pytest.mark.skipif(not URL, reason="TEST_DATABASE_URL not set")
def test_postgres_round_trip_and_cleanup():
    from sqlalchemy import delete

    from walkback.db.models import Assumption, Calibration, Run
    from walkback.db.session import make_session_factory
    from walkback.db.store_sql import SqlRunStore

    sf = make_session_factory(URL)
    store = SqlRunStore(sf)
    run_id = str(uuid.uuid4())
    key = "test-" + run_id
    result = compute_run(synthetic_tile(), PARAMS)
    try:
        store.put(run_id, key, {"run_id": run_id, "result": result})
        back = store.get(run_id)
        assert back is not None
        assert back["result"]["stats"]["counts"] == result["stats"]["counts"]
        assert back["result"]["regions"]["truth"] == result["regions"]["truth"]
        assert store.get_by_hash(key)["run_id"] == run_id
    finally:
        with sf.begin() as s:
            s.execute(delete(Assumption).where(Assumption.run_id == run_id))
            s.execute(delete(Calibration).where(Calibration.run_id == run_id))
            s.execute(delete(Run).where(Run.id == run_id))
