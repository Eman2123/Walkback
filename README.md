# Walkback Under Uncertainty

For a habitat and an EVA time budget, show the area from which a crew can still walk home, and how confident that result is. The walkback region is predicted from a coarse DEM and validated against a 1 m HiRISE DTM of Jezero crater, degraded to the same coarse scale.

Status: foundation. The API validates inputs and returns 501 for compute until the pipeline is connected. The frontend shows only the API status.

## Repository layout

    src/walkback/        Python package
      api.py             FastAPI app, input validation
      params.py          parameter validation and cache key
      explain.py         result explainer (AIML API), numeric guard
      walkback.py        fast marching, speed model
      calibrate.py       reliability bins, Brier, coverage
      slope.py, degrade.py, export.py
      pipeline/          terrain pipeline (scale effect)
      db/                SQLAlchemy models, session, repository
      validation/        validation report
      routing/           routing helpers
      export_io/         GeoJSON and CSV export
    migrations/          Alembic (DATABASE_URL from environment)
    contracts/           JSON schema shared with the frontend
    scripts/             command-line entry points (planned)
    tests/               pytest
    web/                 Vite + React + Tailwind frontend
    docs/                data sources, methods, architecture, ADRs
    reports/             generated validation report and figures
    data/                raw and processed data (not committed)
    .10x/                team state: decisions, status, handoff
    .github/workflows/   CI

## Setup

Backend and tests (no database needed):

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements-api.txt
    PYTHONPATH=src pytest -q

Full pipeline (needs geo libraries):

    pip install -r requirements.txt

Frontend:

    cd web && npm install && npm run dev

Environment variables (see .env.example and web/.env.example): DATABASE_URL, CORS_ORIGINS, AIMLAPI_API_KEY, VITE_API_URL.

## Where to start

Read CONTRIBUTING.md (owners and workflow), docs/methods.md, and .10x/handoff.md (current tasks per person).

## Claims rules

Use "consistent with" and "estimated". Do not write "safe", "guaranteed" or "confirmed" for a walking result. Every number carries a label: measured, derived or assumed.

## Team

Eman (lead, science and validation), Shela (backend), Urooj (frontend).
