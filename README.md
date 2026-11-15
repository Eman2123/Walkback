# Walkback Under Uncertainty

For a habitat and an EVA time budget, show the area from which a crew can still walk home, and how confident that result is. The walkback region is predicted from a coarse DEM and validated against a 1 m HiRISE DTM of Jezero crater, degraded to the same coarse scale.

Status: working prototype. The API computes runs on a real Jezero tile, stores them (share links), and an optional AIML explainer summarises a run. The frontend shows the map, results, reliability chart and assumptions. Nothing here is flight software.

## Result and honesty

The pre-registered default setting is a **shortfall**: coverage of the 1 m truth is below the 95 % target (see reports/validation_report.md). That result is kept as registered. A post-hoc diagnostic (reports/start_cell_diagnostic.md) shows why the calibrated region is empty at that setting: the start cell is itself perturbed and blocked in 12.5 % of realizations. With the start cell kept passable the default gives 86.9 % coverage, still a shortfall. We report both, labelled, and we do not pick the best setting as the headline.

### Planner slope finding

The planner DEM is a staircase of 100 constant 200 m blocks, so slope computed on the 20 m grid is exactly 0 inside a block and large only on block edges. The registered model's Brier score (0.0157) is worse than the 0.0020 of a forecast that always says "never steep". Computing slope on the 200 m block grid instead (exploratory, registered before it was run) reaches that no-skill level with about 100 % coverage, but only 0.2 % of 20 m cells reach the 20 deg cutoff, so this window cannot tell a good planner from a poor one. Scale effect: the 95th percentile slope is 4.4 deg at 200 m and 10.3 deg at 20 m. Details: reports/planner_slope_variant.md. Next step: windows with steeper terrain, registered before analysis.

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

Real Mars basemap (optional, run once with the DTM, then commit the two files it writes):

    PYTHONPATH=src python scripts/build_basemap.py --dtm path/to/dtm.tif \
        --ortho /vsicurl/https://planetarymaps.usgs.gov/mosaic/mars2020_trn/HiRISE/JEZ_hirise_soc_006_orthoMosaic_25cm_Eqc_latTs0_lon0_first.tif \
        --row-off 9744 --col-off 9700

This crops the 25 cm HiRISE orthophoto (DOI 10.5066/P9QJDP48) to the DTM window and writes web/public/basemap-jezero-20m.jpg and .json. Without them the map shows the shaded relief. See docs/adr/004-real-imagery-basemap.md.

Environment variables (see .env.example and web/.env.example): DATABASE_URL, CORS_ORIGINS, AIMLAPI_API_KEY, VITE_API_URL.

## Where to start

Read CONTRIBUTING.md (owners and workflow), docs/methods.md, and .10x/handoff.md (current tasks per person).

## Claims rules

Use "consistent with" and "estimated". Do not write "safe", "guaranteed" or "confirmed" for a walking result. Every number carries a label: measured, derived or assumed.

## Team

Eman (lead, science and validation), Shela (backend), Urooj (frontend).
