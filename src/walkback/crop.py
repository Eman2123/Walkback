"""Windowed read of a crop from the Jezero HiRISE DTM GeoTIFF (avoids loading the full 5.3 GB mosaic)."""
from pathlib import Path

CROP_BOUNDS_DEG = {"lat_min": 18.30, "lat_max": 18.36, "lon_min": 77.20, "lon_max": 77.26}  # placeholder, confirm

def crop_dtm(src: Path, dst: Path) -> Path:
    """TODO (Shela): use rasterio.windows.from_bounds on the mosaic CRS; write a 2 km x 2 km window (2000 x 2000 px at 1 m) to match the 100 x 100 grid at 20 m. See docs/adr/002-map-and-crop.md."""
    raise NotImplementedError
