"""Parameter validation and the cache key. Owner: Shela.

The cache key is SHA-256 over the tile id and parameters rounded to fixed precision,
so the same request always maps to the same stored run.
"""
import hashlib
import json

ROUND = {"budget_s": 0, "speed_mps": 2, "cutoff_deg": 1, "confidence": 2, "roughness": 2}


def param_hash(tile_id: str, params: dict) -> str:
    rounded = {k: (round(v, ROUND[k]) if k in ROUND else v) for k, v in params.items()}
    payload = json.dumps({"tile": tile_id, "params": rounded}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
