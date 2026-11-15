import numpy as np
import pytest

from walkback.pipeline.steep_windows import rank_windows


def _ramp_field(shape=(400, 400)):
    """Flat ground at 0 m, with a steep ramp region (about 40 deg at 20 m cells) in rows 120..260."""
    z = np.zeros(shape)
    rows = np.arange(shape[0])
    rise = 20.0 * 0.84   # tan(40 deg) * 20 m per cell
    z += np.where(rows >= 120, np.minimum(rows - 120, 140) * rise, 0.0)[:, None]
    return z


def test_flat_has_no_candidates():
    assert rank_windows(np.zeros((300, 300)), min_steep_share=0.02) == []


def test_picks_window_over_the_steep_band():
    wins = rank_windows(_ramp_field(), top_n=1, max_steep_share=0.9, require_walkable_center=False)
    assert len(wins) == 1
    w = wins[0]
    assert w.steep_share > 0.5 and w.p95_deg > 30
    # the window must overlap the band of steep rows (120..260)
    assert w.row < 260 and w.row + 100 > 120


def test_windows_do_not_overlap_and_are_sorted():
    z = _ramp_field((600, 600))
    z[:, 300:] += np.arange(600)[:, None] * 5.0   # second, gentler-but-still-steep area
    wins = rank_windows(z, top_n=3, max_steep_share=0.95, require_walkable_center=False)
    assert len(wins) >= 2
    for i, a in enumerate(wins):
        for b in wins[i + 1:]:
            assert max(abs(a.row - b.row), abs(a.col - b.col)) >= 100
    shares = [w.steep_share for w in wins]
    assert shares == sorted(shares, reverse=True)


def test_nodata_windows_are_excluded():
    z = _ramp_field()
    z[150, 150] = np.nan
    wins = rank_windows(z, top_n=5, max_steep_share=0.95, require_walkable_center=False)
    for w in wins:
        covers = (w.row - 1 <= 150 < w.row + 101) and (w.col - 1 <= 150 < w.col + 101)
        assert not covers


def test_mostly_steep_windows_are_filtered_out():
    wins = rank_windows(_ramp_field(), max_steep_share=0.05, min_steep_share=0.0, require_walkable_center=False)
    assert all(w.steep_share <= 0.05 for w in wins)


def test_rejects_small_grid():
    with pytest.raises(ValueError):
        rank_windows(np.zeros((50, 50)))
