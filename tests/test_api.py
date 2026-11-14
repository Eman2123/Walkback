from fastapi.testclient import TestClient
from walkback.api import app

client = TestClient(app)

VALID = {
    "tile_id": "jezero-20m",
    "habitat_row": 50, "habitat_col": 50,
    "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20,
    "confidence": 0.9, "roughness": 0.5,
}

def test_health_ok():
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_docs_disabled():
    assert client.get("/docs").status_code == 404

def test_valid_request_reaches_handler():
    r = client.post("/api/runs", json=VALID)
    assert r.status_code == 501

def test_budget_out_of_range_rejected():
    assert client.post("/api/runs", json={**VALID, "budget_s": 999999}).status_code == 422

def test_habitat_outside_grid_rejected():
    assert client.post("/api/runs", json={**VALID, "habitat_row": 100}).status_code == 422

def test_unknown_tile_rejected():
    assert client.post("/api/runs", json={**VALID, "tile_id": "../etc/passwd"}).status_code == 422

def test_extra_fields_rejected():
    assert client.post("/api/runs", json={**VALID, "grid_size": 5000}).status_code == 422
