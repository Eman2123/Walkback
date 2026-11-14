"""Run storage. In-memory for now; the Neon-backed version uses walkback.db.repository.

Interface kept small so the swap is one file.
"""
from __future__ import annotations

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


STORE = RunStore()
