import sys
from pathlib import Path

import numpy as np
import pytest

from walkback.validation.loo import DEFAULT_SETTING, all_settings, select_setting

A, B, C = ("staircase", 0.5, 0.9), ("grid200", 0.5, 0.9), ("grid200", 0.1, 0.5)


def row(cov, fr):
    return {"coverage": cov, "false_reach": fr}


def test_default_setting_is_in_the_grid_and_grid_has_32_settings():
    assert DEFAULT_SETTING in all_settings() and len(all_settings()) == 32


def test_picks_lowest_false_reach_among_settings_meeting_the_target():
    t = {("t1", A): row(0.96, 0.20), ("t2", A): row(0.97, 0.22),
         ("t1", B): row(0.95, 0.10), ("t2", B): row(0.96, 0.12),
         ("t1", C): row(0.99, 0.30), ("t2", C): row(0.99, 0.35)}
    sel, met, n = select_setting(t, ["t1", "t2"], [A, B, C])
    assert (sel, met, n) == (B, True, 3)


def test_falls_back_to_highest_coverage_and_flags_it():
    t = {("t1", A): row(0.60, 0.0), ("t1", B): row(0.80, 0.4), ("t1", C): row(0.70, 0.1)}
    sel, met, _ = select_setting(t, ["t1"], [A, B, C])
    assert sel == B and met is False


def test_a_setting_that_does_not_compute_on_a_training_tile_is_ineligible():
    t = {("t1", A): row(0.99, 0.0), ("t2", A): None, ("t1", B): row(0.96, 0.3), ("t2", B): row(0.96, 0.3)}
    sel, met, n = select_setting(t, ["t1", "t2"], [A, B])
    assert sel == B and n == 1 and met is True


def test_nothing_eligible_returns_none():
    assert select_setting({("t1", A): None}, ["t1"], [A]) == (None, False, 0)


def test_selection_ignores_the_held_out_tile():
    t = {("train", A): row(0.96, 0.10), ("train", B): row(0.96, 0.20),
         ("held", A): row(0.0, 1.0), ("held", B): row(1.0, 0.0)}
    assert select_setting(t, ["train"], [A, B])[0] == A


def test_ties_prefer_higher_confidence_then_lower_roughness_then_staircase():
    s1, s2 = ("grid200", 0.5, 0.7), ("grid200", 0.5, 0.9)
    t = {("t", s1): row(0.97, 0.1), ("t", s2): row(0.97, 0.1)}
    assert select_setting(t, ["t"], [s1, s2])[0] == s2
    s3, s4 = ("grid200", 0.3, 0.9), ("grid200", 0.5, 0.9)
    t = {("t", s3): row(0.97, 0.1), ("t", s4): row(0.97, 0.1)}
    assert select_setting(t, ["t"], [s3, s4])[0] == s3
    s5, s6 = ("staircase", 0.5, 0.9), ("grid200", 0.5, 0.9)
    t = {("t", s5): row(0.97, 0.1), ("t", s6): row(0.97, 0.1)}
    assert select_setting(t, ["t"], [s5, s6])[0] == s5


def test_empty_calibrated_region_counts_as_zero_false_reach_but_fails_the_target():
    t = {("t", A): row(0.0, None), ("t", B): row(0.97, 0.3)}
    assert select_setting(t, ["t"], [A, B])[0] == B


def test_needs_training_tiles():
    with pytest.raises(ValueError):
        select_setting({}, [], [A])


def _make_tile(path, seed):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:100, 0:100].astype(float)
    p = rng.uniform(0, 6.28, 2)
    fine = 6 * np.sin(2 * np.pi * xx / 55 + p[0]) * np.cos(2 * np.pi * yy / 70 + p[1]) + rng.normal(0, 0.15, (100, 100))
    small = fine.reshape(10, 10, 10, 10).mean(axis=(1, 3))
    coarse = np.repeat(np.repeat(small, 10, axis=0), 10, axis=1)
    np.savez(path, coarse=coarse, fine=fine, cell_m=20.0, label=np.array(f"synthetic {seed}"))


def test_script_runs_end_to_end_on_synthetic_tiles(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import loo_calibration as lc

    for i in range(3):
        _make_tile(tmp_path / f"s{i}.npz", i)
    md, cs = lc.run(tmp_path, ["s0", "s1", "s2"], all_settings(("staircase", "grid200"), (0.3,), (0.5, 0.9)),
                    tmp_path / "out")
    text = md.read_text(encoding="utf-8")
    for t in ("s0", "s1", "s2"):                                                   # every fold is reported
        assert f"| {t} | selected |" in text and f"| {t} | v2 default |" in text
    assert "not a claim about other terrain" in text
    rows = cs.read_text(encoding="utf-8").strip().splitlines()
    assert len(rows) == 1 + 6


def test_script_refuses_fewer_than_three_tiles(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import loo_calibration as lc

    _make_tile(tmp_path / "a.npz", 0)
    _make_tile(tmp_path / "b.npz", 1)
    with pytest.raises(SystemExit):
        lc.run(tmp_path, ["a", "b"], all_settings(), tmp_path / "out")
