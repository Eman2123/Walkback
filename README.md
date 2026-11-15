# Walkback Under Uncertainty

For a habitat and an EVA time budget, show the area from which a crew can still walk home, and how confident that result is. The walkback region is predicted from a coarse DEM and validated against a 1 m HiRISE DTM of Jezero crater, degraded to the same coarse scale.

Status: working prototype. The API computes runs on a real Jezero tile, stores them (share links), and an optional AIML explainer summarises a run. The frontend shows the map, results, reliability chart and assumptions. Nothing here is flight software.

## Result and honesty

The pre-registered default setting is a **shortfall**: coverage of the 1 m truth is below the 95 % target (see reports/validation_report.md). That result is kept as registered. A post-hoc diagnostic (reports/start_cell_diagnostic.md) shows why the calibrated region is empty at that setting: the start cell is itself perturbed and blocked in 12.5 % of realizations. With the start cell kept passable the default gives 86.9 % coverage, still a shortfall. We report both, labelled, and we do not pick the best setting as the headline.

## Data

Terrain: Mars 2020 TRN HiRISE DTM (USGS Astrogeology, from NASA HiRISE stereo images; DOI 10.5066/P9REJ9JN), a 2 km window of Jezero crater at 20 m, with the 1 m model as held-out truth. Sources and processing: docs/data-sources.md. NASA does not endorse this project.

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
