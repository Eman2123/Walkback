import pytest
from fastapi.testclient import TestClient

from walkback import api
from walkback.store import RunStore

VALID = {
    "tile_id": "dev-synthetic-20m",
    "habitat_row": 50, "habitat_col": 50,
    "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20,
    "confidence": 0.9, "roughness": 0.5,
}


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("WALKBACK_ENV", "dev")
    monkeypatch.setattr(api, "STORE", RunStore())
    return TestClient(api.app)


def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_docs_disabled(client):
    assert client.get("/docs").status_code == 404


def test_dev_run_returns_regions_stats_and_labelled_assumptions(client):
    r = client.post("/api/runs", json=VALID)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["cached"] is False
    assert set(body["regions"]) == {"deterministic", "calibrated", "truth"}
    assert body["regions"]["deterministic"]["type"] == "MultiPolygon"
    assert all(a["label"] in {"measured", "derived", "assumed"} for a in body["assumptions"])
    assert "SYNTHETIC" in body["tile"]["label"]


def test_second_identical_request_is_cached(client):
    first = client.post("/api/runs", json=VALID).json()
    second = client.post("/api/runs", json=VALID).json()
    assert second["cached"] is True
    assert second["run_id"] == first["run_id"]


def test_get_run_by_id(client):
    run_id = client.post("/api/runs", json=VALID).json()["run_id"]
    assert client.get(f"/api/runs/{run_id}").status_code == 200
    assert client.get("/api/runs/does-not-exist").status_code == 404


def test_dev_tile_rejected_outside_dev(monkeypatch):
    monkeypatch.delenv("WALKBACK_ENV", raising=False)
    c = TestClient(api.app)
    assert c.post("/api/runs", json=VALID).status_code == 422


def test_real_tile_not_built_returns_503(monkeypatch, client):
    monkeypatch.setattr(api, "DEFAULT_TILE_DIR", api.DEFAULT_TILE_DIR.__class__("/nonexistent"))
    r = client.post("/api/runs", json={**VALID, "tile_id": "jezero-20m"})
    assert r.status_code == 503


def test_budget_out_of_range_rejected(client):
    assert client.post("/api/runs", json={**VALID, "budget_s": 999999}).status_code == 422


def test_habitat_outside_grid_rejected(client):
    assert client.post("/api/runs", json={**VALID, "habitat_row": 100}).status_code == 422


def test_unknown_tile_rejected(client):
    assert client.post("/api/runs", json={**VALID, "tile_id": "../etc/passwd"}).status_code == 422


def test_extra_fields_rejected(client):
    assert client.post("/api/runs", json={**VALID, "grid_size": 5000}).status_code == 422
