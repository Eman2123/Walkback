"""FastAPI service for Walkback. Input is untrusted: every field is range-checked here."""
from __future__ import annotations

import os
import uuid
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from .compute import compute_run
from .params import param_hash
from .store import STORE
from .tiles import DEV_TILE_ID, DEFAULT_TILE_DIR, load_tile, synthetic_tile

ALLOWED_TILES = frozenset({"jezero-20m", "jezero-200m", DEV_TILE_ID})
GRID_SIZE = 100

app = FastAPI(
    title="Walkback API",
    version="0.2.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def _dev_mode() -> bool:
    return os.environ.get("WALKBACK_ENV", "") == "dev"


class RunRequest(BaseModel):
    model_config = {"extra": "forbid"}

    tile_id: str = "jezero-20m"
    habitat_row: int = Field(ge=0, le=GRID_SIZE - 1)
    habitat_col: int = Field(ge=0, le=GRID_SIZE - 1)
    budget_s: int = Field(ge=300, le=1800)
    speed_mps: float = Field(ge=0.3, le=1.0)
    cutoff_deg: float = Field(ge=10, le=30)
    confidence: float = Field(ge=0.5, le=0.95)
    roughness: float = Field(ge=0, le=1)

    @field_validator("tile_id")
    @classmethod
    def tile_must_be_allowed(cls, v: str) -> str:
        if v not in ALLOWED_TILES:
            raise ValueError("unknown tile")
        if v == DEV_TILE_ID and not _dev_mode():
            raise ValueError("unknown tile")
        return v


@lru_cache(maxsize=1)
def _dev_tile():
    return synthetic_tile()


def _get_tile(tile_id: str):
    if tile_id == DEV_TILE_ID:
        return _dev_tile()
    tile = load_tile(tile_id, DEFAULT_TILE_DIR)
    if tile is None:
        raise HTTPException(status_code=503, detail="terrain tile not built yet")
    return tile


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": app.version}


@app.post("/api/runs")
def create_run(req: RunRequest) -> dict:
    params = req.model_dump()
    tile_id = params.pop("tile_id")
    key = param_hash(tile_id, params)

    cached = STORE.get_by_hash(key)
    if cached is not None:
        return {"run_id": cached["run_id"], "cached": True, **cached["result"]}

    tile = _get_tile(tile_id)
    try:
        result = compute_run(tile, {**params})
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    run_id = str(uuid.uuid4())
    STORE.put(run_id, key, {"run_id": run_id, "result": result})
    return {"run_id": run_id, "cached": False, **result}


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict:
    stored = STORE.get(run_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="run not found")
    return {"run_id": run_id, "cached": True, **stored["result"]}
