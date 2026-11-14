"""FastAPI service for Walkback. Input is untrusted: every field is range-checked here.

Compute is not wired yet: POST /api/runs validates and returns 501 until the pipeline is connected.
"""
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

ALLOWED_TILES = frozenset({"jezero-20m", "jezero-200m"})
GRID_SIZE = 100  # cells per side; fixed so a request cannot ask for a bigger grid

app = FastAPI(
    title="Walkback API",
    version="0.1.0",
    docs_url=None,      # no public docs in production
    redoc_url=None,
    openapi_url=None,
)

_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,          # set to the Vercel domain in production; empty means no cross-origin access
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


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
        return v


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": app.version}


@app.post("/api/runs")
def create_run(req: RunRequest) -> dict:
    # Pipeline connection comes next. Until then, be explicit rather than return fake results.
    raise HTTPException(status_code=501, detail="compute not wired yet")
