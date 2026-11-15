"""Leave-one-window-out selection of a calibration setting (PREREGISTRATION.md, "Leave-one-window-out calibration").

Pure logic, no terrain. A table maps (tile_id, setting) to {"coverage", "false_reach"} or None when the setting did
not compute on that tile. A setting is (planner, roughness, confidence).
"""
from __future__ import annotations

from itertools import product

PLANNERS = ("staircase", "grid200")
ROUGHNESS = (0.1, 0.3, 0.5, 0.8)
CONFIDENCE = (0.5, 0.7, 0.9, 0.95)
DEFAULT_SETTING = ("staircase", 0.5, 0.9)      # the v2 default setting
TARGET = 0.95

Setting = tuple[str, float, float]


def all_settings(planners=PLANNERS, roughness=ROUGHNESS, confidence=CONFIDENCE) -> list[Setting]:
    return [(p, r, c) for p, r, c in product(planners, roughness, confidence)]


def _scored(row) -> bool:
    return row is not None and row.get("coverage") is not None


def select_setting(table: dict, train_ids: list[str], settings: list[Setting], target: float = TARGET):
    """Choose a setting using the training tiles only.

    Eligible: computes (and has a coverage) on every training tile. Among eligible settings whose mean training
    coverage is at or above target, take the lowest mean training false reach (an empty calibrated region counts as
    0 false reach, it already costs coverage); ties go to the higher confidence, then the lower roughness, then
    staircase. If none reaches the target, take the highest mean training coverage (same ties) and report
    met_target=False. Returns (setting, met_target, n_eligible); setting is None when nothing is eligible.
    """
    if not train_ids:
        raise ValueError("need at least one training tile")
    rows = []
    for s in settings:
        got = [table.get((t, s)) for t in train_ids]
        if not all(_scored(g) for g in got):
            continue
        cov = sum(g["coverage"] for g in got) / len(got)
        fr = sum((g["false_reach"] or 0.0) for g in got) / len(got)
        rows.append((s, cov, fr))
    if not rows:
        return None, False, 0
    tie = lambda s: (-s[2], s[1], PLANNERS.index(s[0]))                        # noqa: E731
    ok = [r for r in rows if r[1] >= target]
    if ok:
        best = min(ok, key=lambda r: (r[2], *tie(r[0])))
        return best[0], True, len(rows)
    best = min(rows, key=lambda r: (-r[1], *tie(r[0])))
    return best[0], False, len(rows)
