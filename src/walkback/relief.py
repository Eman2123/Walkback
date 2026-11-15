"""Shaded-relief image of a terrain tile, for the map basemap.

Derived from the coarse DEM the planner sees (itself derived from the USGS HiRISE DTM).
Pure numpy + zlib, so the API needs no imaging dependency.
"""
from __future__ import annotations

import struct
import zlib

import numpy as np

_SUN_AZIMUTH_DEG = 315.0
_SUN_ALTITUDE_DEG = 40.0
# Warm, Mars-like tint applied to the grey shading. Cosmetic only.
_TINT_LOW = np.array([120.0, 78.0, 58.0])
_TINT_HIGH = np.array([236.0, 176.0, 132.0])


def _upsample(z: np.ndarray, factor: int) -> np.ndarray:
    """Separable linear interpolation, so the relief is smooth instead of blocky."""
    n = z.shape[0]
    src = np.arange(n)
    dst = np.linspace(0, n - 1, n * factor)
    rows = np.array([np.interp(dst, src, z[:, j]) for j in range(z.shape[1])]).T
    return np.array([np.interp(dst, src, rows[i, :]) for i in range(rows.shape[0])])


def hillshade(z: np.ndarray, cell_m: float) -> np.ndarray:
    """Lambertian hillshade in [0, 1]. Light from the north-west, 40 degrees above the horizon."""
    dzdy, dzdx = np.gradient(z, cell_m)
    slope = np.arctan(np.hypot(dzdx, dzdy))
    aspect = np.arctan2(dzdy, -dzdx)
    az = np.deg2rad(360.0 - _SUN_AZIMUTH_DEG + 90.0)
    alt = np.deg2rad(_SUN_ALTITUDE_DEG)
    shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return np.clip(shade, 0.0, 1.0)


def _png(rgb: np.ndarray) -> bytes:
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[i].tobytes() for i in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 6))
        + chunk(b"IEND", b"")
    )


def relief_png(coarse: np.ndarray, cell_m: float, factor: int = 3) -> bytes:
    z = np.asarray(coarse, dtype=float)
    zf = _upsample(z, factor)
    shade = hillshade(zf, cell_m / factor)
    lo, hi = float(np.nanmin(zf)), float(np.nanmax(zf))
    t = (zf - lo) / (hi - lo) if hi > lo else np.zeros_like(zf)
    base = _TINT_LOW[None, None, :] * (1 - t[..., None]) + _TINT_HIGH[None, None, :] * t[..., None]
    rgb = np.clip(base * (0.35 + 0.9 * shade[..., None]), 0, 255).astype(np.uint8)
    return _png(rgb)
