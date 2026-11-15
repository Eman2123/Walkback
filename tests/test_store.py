import pytest

from walkback.store import RunStore


def _put(store, i):
    store.put(f"id{i}", f"hash{i}", {"run_id": f"id{i}", "result": {"n": i}})


def test_store_is_capped_and_drops_the_oldest():
    s = RunStore(max_runs=3)
    for i in range(5):
        _put(s, i)
    assert len(s) == 3
    assert s.get("id0") is None and s.get("id1") is None
    assert s.get("id4") is not None
    assert s.get_by_hash("hash0") is None and s.get_by_hash("hash4") is not None


def test_a_read_keeps_a_run_alive():
    s = RunStore(max_runs=3)
    for i in range(3):
        _put(s, i)
    assert s.get("id0") is not None            # touch the oldest
    _put(s, 3)                                  # evicts id1, not id0
    assert s.get("id0") is not None and s.get("id1") is None


def test_same_hash_stored_again_does_not_leave_a_dangling_hash():
    s = RunStore(max_runs=2)
    s.put("a", "h", {"run_id": "a", "result": {}})
    s.put("b", "h", {"run_id": "b", "result": {}})          # same params, new id: hash now points at b
    _put(s, 1)                                               # evicts a
    assert s.get_by_hash("h")["run_id"] == "b"


def test_max_runs_must_be_positive_and_env_sets_the_default(monkeypatch):
    with pytest.raises(ValueError):
        RunStore(max_runs=0)
    monkeypatch.setenv("WALKBACK_MAX_RUNS", "2")
    s = RunStore()
    for i in range(4):
        _put(s, i)
    assert len(s) == 2
