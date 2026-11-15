# Walkback Under Uncertainty

For a habitat and an EVA time budget, show the area from which a crew can still walk home, and how confident that result is. The walkback region is predicted from a coarse DEM and validated against a 1 m HiRISE DTM of Jezero crater, degraded to the same coarse scale.

Status: working prototype. The API computes runs on a real Jezero tile, stores them (share links), and an optional AIML explainer summarises a run. The frontend shows the map, results, reliability chart and assumptions. Nothing here is flight software.

## Result and honesty

The pre-registered default setting is a **shortfall**: coverage of the 1 m truth is below the 95 % target (see reports/validation_report.md). That result is kept as registered. A post-hoc diagnostic (reports/start_cell_diagnostic.md) shows why the calibrated region is empty at that setting: the start cell is itself perturbed and blocked in 12.5 % of realizations. With the start cell kept passable the default gives 86.9 % coverage, still a shortfall. We report both, labelled, and we do not pick the best setting as the headline.

### Planner slope finding

The planner DEM is a staircase of 100 constant 200 m blocks, so slope computed on the 20 m grid is exactly 0 inside a block and large only on block edges. The registered model's Brier score (0.0157) is worse than the 0.0020 of a forecast that always says "never steep". Computing slope on the 200 m block grid instead (exploratory, registered before it was run) reaches that no-skill level with about 100 % coverage, but only 0.2 % of 20 m cells reach the 20 deg cutoff, so the first window cannot tell a good planner from a poor one. Scale effect: the 95th percentile slope is 4.4 deg at 200 m and 10.3 deg at 20 m. Details: reports/planner_slope_variant.md.

### Steep-terrain windows

Three steeper windows (steep-1, steep-2, steep-3) were registered before analysis. Every row is reported in the PREREGISTRATION.md change log, none selected. Estimated results:

- The registered model did not run on steep-1 and steep-2: the habitat cell at 200 m is impassable. On steep-3 it ran, but 0 of 9 rows reach 95 % coverage, and the Brier skill score against "never steep" is negative (-0.95 to -0.74) in a window where 17 % of cells are steep.
- The 200 m-grid slope variant (grid200) now beats "never steep" (BSS +0.19 to +0.46, versus about 0 on the first window). This shows the first window was uninformative for steep terrain.
- No row of any model in any steep window has a wider-interval lower end that reaches 95 %. Under the registered rule this is a shortfall.
- On steep-2, 47 % to 58 % of the area grid200 calls "reachable" is not reachable in the 1 m truth (false reach). This is the most serious result for any use of the region.
- hurst (out-of-sample H) covers less (0 % on steep-1) because thin-tailed noise does not produce steep cells. This was registered as expected. It is not promoted.
- Direction of the Minetti cost: truth area changes by a factor of 0.3 to 3 depending on the variant. Uncapped `minetti back` doubles the area on steep-3; that reflects the downhill speed-up assumption, not the terrain. Read `minetti_cap back` for the return-trip question.
- The 16-neighbour solver raises truth area by 6 % to 10 % on the steep windows.

Details and per-row numbers: PREREGISTRATION.md (change log).

## Limitations

What these results support: on this Jezero DTM, in these three steep windows, the registered planner either does not run or does worse than "never steep", and grid200 does not reach 95 % coverage either.

What they do not support:

- "The model is fine for steep terrain" (it is not, here).
- Any statement about other parts of Mars. There are three windows, one DTM, and the windows were chosen by steepness.
- Any use of the walkback region as a safety margin. Estimated false reach is high on at least one window, and no row reaches the coverage target.
- The speed model (Minetti variants, neighbour count) is an assumption. Results move by up to a factor of 3 in area depending on it.

Open design question: the registered model fails on steep-1 and steep-2 because the habitat cell is impassable at 200 m. Fixing this (a window whose habitat cell is below the cutoff, or a different habitat-cell rule) needs a new registration and is not done yet.

## Data

Terrain: Mars 2020 TRN HiRISE DTM (USGS Astrogeology, from NASA HiRISE stereo images; DOI 10.5066/P9REJ9JN), a 2 km window of Jezero crater at 20 m, with the 1 m model as held-out truth. Sources and processing: docs/data-sources.md. NASA does not endorse this project.

## Repository layout

```
src/walkback/        Python package
  api.py             FastAPI app, input validation
  params.py          parameter validation and cache key
  explain.py         result explainer (AIML API), numeric guard
  compute.py         speed model, 8-connected Dijkstra travel time, ensemble calibration
  walkback.py        deprecated stub (moved to compute.py)
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
```

## Setup

Backend and tests (no database needed):

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-api.txt
PYTHONPATH=src pytest -q
```

Full pipeline (needs geo libraries):

```
pip install -r requirements.txt
```

Frontend:

```
cd web && npm install && npm run dev
```

Real Mars basemap (optional, run once with the DTM, then commit the two files it writes):

```
PYTHONPATH=src python scripts/build_basemap.py --dtm path/to/dtm.tif \
    --ortho /vsicurl/https://planetarymaps.usgs.gov/mosaic/mars2020_trn/HiRISE/JEZ_hirise_soc_006_orthoMosaic_25cm_Eqc_latTs0_lon0_first.tif \
    --row-off 9744 --col-off 9700
```

This crops the 25 cm HiRISE orthophoto (DOI 10.5066/P9QJDP48) to the DTM window and writes web/public/basemap-jezero-20m.jpg and .json. Without them the map shows the shaded relief. See docs/adr/004-real-imagery-basemap.md.

Environment variables (see .env.example and web/.env.example): DATABASE_URL, CORS_ORIGINS, AIMLAPI_API_KEY, VITE_API_URL.

## Where to start

Read CONTRIBUTING.md (owners and workflow), docs/methods.md, and .10x/handoff.md (current tasks per person).

## Claims rules

Use "consistent with" and "estimated". Do not write "safe", "guaranteed" or "confirmed" for a walking result. Every number carries a label: measured, derived or assumed.

## Team

Eman (lead, science and validation), Shela (backend), Urooj (frontend).