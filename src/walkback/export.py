"""Write the scenario JSON that the frontend reads. Schema: contracts/scenario.schema.json."""
import json
from pathlib import Path

def write_scenario(payload: dict, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return dst
