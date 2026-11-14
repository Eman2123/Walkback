# Walkback Under Uncertainty

For a habitat and an EVA time budget, show the area from which a crew can still walk home, and how confident that result is. The walkback region is predicted from a coarse 200 m DEM and validated against a 1 m HiRISE DTM of Jezero crater, degraded to the same coarse scale.

Status: foundation only. No results yet.

## What is real vs assumed

| Item | Status |
|---|---|
| Jezero HiRISE DTM (1 m) | Real data, to be downloaded (see `data/manifest.csv`) |
| Coarse DEM (200 m, 20 m) | Derived from the 1 m DTM by block averaging |
| Scale effect of slope | Measured from the crop |
| Walking speed | Assumed. Configurable in `contracts/scenario.schema.json` |
| Suit factor on walking cost | Assumed |
| Slope cutoff for impassable cells | Assumed |

## Repository layout

```
src/walkback/   pipeline modules (download, crop, degrade, slope, walkback, calibrate, export)
contracts/      JSON contract shared with the frontend
data/           raw and processed data (not committed)
tests/          pytest tests for pipeline logic
reports/        validation report and figures
web/            frontend (Next.js or Leaflet), reads exported JSON only
docs/           methods note, team plan
```

## Setup

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Claims rules

Use "consistent with" and "estimated". Do not write "safe", "guaranteed" or "confirmed" for a walking result. Every number carries a label: measured, derived or assumed.

## Team

Eman (lead, science and validation), Shela (backend), Urooj (frontend).
