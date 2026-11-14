"""Run storage. Postgres (Neon) when DATABASE_URL is set, otherwise in-memory for local dev and tests."""
from __future__ import annotations

import os
import threading
from typing import Any


class RunStore:
    def __init__(self) -> None:
        self._by_id: dict[str, dict[str, Any]] = {}
        self._by_hash: dict[str, str] = {}
        self._lock = threading.Lock()

    def get_by_hash(self, param_hash: str) -> dict[str, Any] | None:
        with self._lock:
            rid = self._by_hash.get(param_hash)
            return self._by_id.get(rid) if rid else None

    def get(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            return self._by_id.get(run_id)

    def put(self, run_id: str, param_hash: str, run: dict[str, Any]) -> None:
        with self._lock:
            self._by_id[run_id] = run
            self._by_hash[param_hash] = run_id


def _make_store():
    url = os.environ.get("DATABASE_URL")
    if not url:
        return RunStore()
    from .db.session import make_session_factory
    from .db.store_sql import SqlRunStore

    return SqlRunStore(make_session_factory(url))


STORE = _make_store()
