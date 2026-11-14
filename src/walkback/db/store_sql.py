"""Neon/Postgres-backed run store. Same interface as walkback.store.RunStore.

Writes one run as: terrain_tiles (upsert), runs, calibration, assumptions. Reads rebuild the
same dict shape the API returns, so the rest of the code does not know which store it uses.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import select

from .models import Assumption, Calibration, Run, TerrainTile


class SqlRunStore:
    def __init__(self, session_factory) -> None:
        self._sf = session_factory

    def get_by_hash(self, param_hash: str) -> dict[str, Any] | None:
        with self._sf() as s:
            run = s.execute(select(Run).where(Run.param_hash == param_hash)).scalar_one_or_none()
            return self._to_dict(s, run) if run else None

    def get(self, run_id: str) -> dict[str, Any] | None:
        with self._sf() as s:
            run = s.get(Run, run_id)
            return self._to_dict(s, run) if run else None

    def put(self, run_id: str, param_hash: str, run: dict[str, Any]) -> None:
        result = run["result"]
        tile = result["tile"]
        with self._sf.begin() as s:
            if s.get(TerrainTile, tile["id"]) is None:
                s.add(TerrainTile(
                    id=tile["id"], dataset_id=None, crop_name=tile["label"],
                    resolution_m=float(tile["cell_m"]), raster_path="", bounds_json={},
                ))
                s.flush()
            s.add(Run(
                id=run_id,
                tile_id=tile["id"],
                params_json=result["params"],
                param_hash=param_hash,
                region_det_geojson=result["regions"]["deterministic"],
                region_cal_geojson=result["regions"]["calibrated"],
                region_truth_geojson=result["regions"]["truth"],
                stats_json=result["stats"],
                runtime_ms=result["stats"].get("runtime_ms"),
            ))
            cal = result["calibration"]
            s.add(Calibration(
                run_id=run_id,
                bins_json=cal["bins"],
                brier=cal["brier"],
                coverage=cal["coverage"],
                coverage_ci_low=cal["coverage_ci"][0],
                coverage_ci_high=cal["coverage_ci"][1],
            ))
            for a in result["assumptions"]:
                s.add(Assumption(run_id=run_id, name=a["name"], value=a["value"], label=a["label"]))

    def _to_dict(self, s, run: Run) -> dict[str, Any]:
        tile = s.get(TerrainTile, run.tile_id)
        cal = s.get(Calibration, run.id)
        assumptions = s.execute(
            select(Assumption).where(Assumption.run_id == run.id).order_by(Assumption.id)
        ).scalars().all()
        result = {
            "tile": {"id": run.tile_id, "cell_m": tile.resolution_m, "label": tile.crop_name},
            "params": run.params_json,
            "regions": {
                "deterministic": run.region_det_geojson,
                "calibrated": run.region_cal_geojson,
                "truth": run.region_truth_geojson,
            },
            "stats": run.stats_json,
            "calibration": {
                "bins": cal.bins_json,
                "brier": cal.brier,
                "coverage": cal.coverage,
                "coverage_ci": [cal.coverage_ci_low, cal.coverage_ci_high],
            },
            "assumptions": [{"name": a.name, "value": a.value, "label": a.label} for a in assumptions],
        }
        return {"run_id": run.id, "result": result}
