import pytest
from fastapi.testclient import TestClient

from walkback import api
from walkback.store import RunStore

VALID = {
    "tile_id": "dev-synthetic-20m",
    "habitat_row": 49, "habitat_col": 50,
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


def test_explain_404_for_unknown_run(client):
    assert client.post("/api/runs/nope/explain").status_code == 404


def test_explain_503_when_not_configured(client, monkeypatch):
    monkeypatch.delenv("AIMLAPI_API_KEY", raising=False)
    run_id = client.post("/api/runs", json=VALID).json()["run_id"]
    assert client.post(f"/api/runs/{run_id}/explain").status_code == 503


def test_explain_returns_text_and_sends_no_geometry(client, monkeypatch):
    monkeypatch.setenv("AIMLAPI_API_KEY", "test-key")
    monkeypatch.setenv("AIML_MODEL", "test-model")
    seen = {}

    def fake_explain(summary, client_obj, model):
        seen["summary"] = summary
        seen["model"] = model
        return "The calibrated region is consistent with the run."

    class FakeOpenAI:
        def __init__(self, **kwargs):
            pass

    monkeypatch.setattr(api, "explain_run", fake_explain)
    import types, sys
    fake_mod = types.ModuleType("openai")
    fake_mod.OpenAI = FakeOpenAI
    monkeypatch.setitem(sys.modules, "openai", fake_mod)

    run_id = client.post("/api/runs", json=VALID).json()["run_id"]
    r = client.post(f"/api/runs/{run_id}/explain")
    assert r.status_code == 200
    assert r.json()["text"].startswith("The calibrated")
    assert "regions" not in seen["summary"]
    assert seen["model"] == "test-model"


def test_rate_limit_returns_429(client, monkeypatch):
    monkeypatch.setattr(api, "LIMITER", api.RateLimiter(2))
    assert client.post("/api/runs", json=VALID).status_code == 200
    assert client.post("/api/runs", json={**VALID, "budget_s": 600}).status_code == 200
    assert client.post("/api/runs", json={**VALID, "budget_s": 700}).status_code == 429
