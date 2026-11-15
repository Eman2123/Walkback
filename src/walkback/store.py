"""Run storage. Postgres (Neon) when DATABASE_URL is set, otherwise in-memory for local dev and tests.

The in-memory store keeps at most WALKBACK_MAX_RUNS runs (default 500) and drops the least recently used one
beyond that, so a client cycling through parameters cannot grow memory without limit. It lives inside one process:
with more than one uvicorn worker each worker has its own copy, so use DATABASE_URL for that.
"""
from __future__ import annotations

import os
import threading
from collections import OrderedDict
from typing import Any

DEFAULT_MAX_RUNS = 500


class RunStore:
    def __init__(self, max_runs: int | None = None) -> None:
        if max_runs is None:
            max_runs = int(os.environ.get("WALKBACK_MAX_RUNS", DEFAULT_MAX_RUNS))
        if max_runs < 1:
            raise ValueError("max_runs must be at least 1")
        self._max = max_runs
        self._by_id: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._by_hash: dict[str, str] = {}
        self._hash_of: dict[str, str] = {}
        self._lock = threading.Lock()

    def get_by_hash(self, param_hash: str) -> dict[str, Any] | None:
        with self._lock:
            rid = self._by_hash.get(param_hash)
            if rid is None or rid not in self._by_id:
                return None
            self._by_id.move_to_end(rid)
            return self._by_id[rid]

    def get(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            run = self._by_id.get(run_id)
            if run is not None:
                self._by_id.move_to_end(run_id)
            return run

    def put(self, run_id: str, param_hash: str, run: dict[str, Any]) -> None:
        with self._lock:
            self._by_id[run_id] = run
            self._by_id.move_to_end(run_id)
            self._by_hash[param_hash] = run_id
            self._hash_of[run_id] = param_hash
            while len(self._by_id) > self._max:
                old, _ = self._by_id.popitem(last=False)
                h = self._hash_of.pop(old, None)
                if h is not None and self._by_hash.get(h) == old:
                    del self._by_hash[h]

    def __len__(self) -> int:
        with self._lock:
            return len(self._by_id)


def _make_store():
    url = os.environ.get("DATABASE_URL")
    if not url:
        return RunStore()
    from .db.session import make_session_factory
    from .db.store_sql import SqlRunStore

    return SqlRunStore(make_session_factory(url))


STORE = _make_store()
