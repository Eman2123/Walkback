"""FastAPI service for Walkback. Input is untrusted: every field is range-checked here."""
from __future__ import annotations

import logging
import os
import threading
import time
import uuid
from collections import OrderedDict, defaultdict, deque
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from .compute import PROFILE_V2, compute_run_v2
from .explain import FALLBACK, explain_run
from .params import param_hash
from .relief import relief_png
from .store import STORE
from .tiles import DEFAULT_TILE_DIR, DEV_TILE_ID, load_tile, synthetic_tile

ALLOWED_TILES = frozenset({"jezero-20m", DEV_TILE_ID})
GRID_SIZE = 100

log = logging.getLogger("walkback")

app = FastAPI(title="Walkback API", version="0.3.0", docs_url=None, redoc_url=None, openapi_url=None)


def warn_if_unsafe_deployment() -> bool:
    """Log a warning (and return True) when several workers would each keep their own in-memory run store."""
    try:
        workers = int(os.environ.get("WEB_CONCURRENCY", "1"))
    except ValueError:
        workers = 1
    if workers > 1 and not os.environ.get("DATABASE_URL"):
        log.warning(
            "WEB_CONCURRENCY=%s without DATABASE_URL: each worker has its own in-memory run store and rate limiter, "
            "so GET /api/runs/{id} can return 404 for a run another worker created. Set DATABASE_URL or use one worker.",
            workers,
        )
        return True
    return False


warn_if_unsafe_deployment()

_DEFAULT_ORIGINS = ["https://walkback-rlvz.vercel.app"]
# Frontend previews and aliases of this project on Vercel (walkback-git-<branch>-<team>.vercel.app and similar).
# The API sends no cookies and takes no credentials, so allowing these origins exposes nothing a direct call would not.
_DEFAULT_ORIGIN_REGEX = r"https://walkback[a-z0-9-]*\.vercel\.app"


def cors_settings(env: dict | None = None) -> tuple[list[str], str | None]:
    """Allowed browser origins: CORS_ORIGINS PLUS the default frontend, never instead of it.

    A CORS_ORIGINS that is set (for example the README placeholder) used to replace the default, which blocked the
    real frontend with "No Access-Control-Allow-Origin header". CORS_ORIGIN_REGEX overrides the preview pattern;
    set it to an empty string to turn the pattern off.
    """
    env = os.environ if env is None else env
    configured = [o.strip().rstrip("/") for o in env.get("CORS_ORIGINS", "").split(",") if o.strip()]
    origins = list(dict.fromkeys(configured + _DEFAULT_ORIGINS))
    regex = env.get("CORS_ORIGIN_REGEX", _DEFAULT_ORIGIN_REGEX)
    return origins, (regex or None)


_origins, _origin_regex = cors_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=_origin_regex,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class RateLimiter:
    """Sliding window per client IP. In-memory: resets on restart, fine for one container."""

    def __init__(self, per_minute: int) -> None:
        self.per_minute = per_minute
        self._hits: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key: str, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        with self._lock:
            q = self._hits[key]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= self.per_minute:
                return False
            q.append(now)
            return True


LIMITER = RateLimiter(int(os.environ.get("WALKBACK_RATE_PER_MIN", "30")))


def _limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    if not LIMITER.allow(ip):
        raise HTTPException(status_code=429, detail="too many requests, try again in a minute")


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


@lru_cache(maxsize=4)
def _relief_for(tile_id: str) -> bytes:
    tile = _get_tile(tile_id)
    return relief_png(tile.coarse, tile.cell_m)


@app.get("/api/tiles/{tile_id}/relief.png")
def tile_relief(tile_id: str, request: Request) -> Response:
    """Shaded relief of the coarse DEM, used as the map basemap."""
    _limit(request)
    if tile_id not in ALLOWED_TILES or (tile_id == DEV_TILE_ID and not _dev_mode()):
        raise HTTPException(status_code=404, detail="unknown tile")
    return Response(
        content=_relief_for(tile_id),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@app.post("/api/runs")
def create_run(req: RunRequest, request: Request) -> dict:
    _limit(request)
    params = req.model_dump()
    tile_id = params.pop("tile_id")
    key = param_hash(tile_id, {**params, "profile": PROFILE_V2})   # profile in the key: a v1 run is never served as v2

    cached = STORE.get_by_hash(key)
    if cached is not None:
        return {"run_id": cached["run_id"], "cached": True, **cached["result"]}

    tile = _get_tile(tile_id)
    try:
        result = compute_run_v2(tile, dict(params))
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


_EXPLAIN_CACHE: OrderedDict[str, str] = OrderedDict()   # run_id -> explanation; saves model tokens on repeat clicks
_EXPLAIN_LOCK = threading.Lock()
_EXPLAIN_MAX = 256


@app.post("/api/runs/{run_id}/explain")
def explain(run_id: str, request: Request) -> dict:
    """Plain-language explanation via AIML API. Sends a summary of the run, never the map geometry."""
    _limit(request)
    stored = STORE.get(run_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="run not found")

    with _EXPLAIN_LOCK:
        hit = _EXPLAIN_CACHE.get(run_id)
        if hit is not None:
            _EXPLAIN_CACHE.move_to_end(run_id)
            return {"text": hit}

    api_key = os.environ.get("AIMLAPI_API_KEY")
    model = os.environ.get("AIML_MODEL")
    if not api_key or not model:
        raise HTTPException(status_code=503, detail="explainer not configured")

    from openai import OpenAI  # imported here so the API runs without the package installed

    client = OpenAI(api_key=api_key, base_url=os.environ.get("AIML_BASE_URL", "https://api.aimlapi.com/v1"))
    summary = {k: v for k, v in stored["result"].items() if k != "regions"}
    text = explain_run(summary, client, model)
    if text != FALLBACK:                      # a failed call is never cached, so a retry can succeed
        with _EXPLAIN_LOCK:
            _EXPLAIN_CACHE[run_id] = text
            while len(_EXPLAIN_CACHE) > _EXPLAIN_MAX:
                _EXPLAIN_CACHE.popitem(last=False)
    return {"text": text}
