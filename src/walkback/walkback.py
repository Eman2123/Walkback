"""Deprecated location. The computation lives in walkback.compute (pure Python, no scikit-fmm).

Kept as a re-export so older imports still work.
"""
from .compute import speed_field as speed_from_slope  # noqa: F401
from .compute import travel_time  # noqa: F401
