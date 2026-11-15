# Data sources

| Source | Role | Ground truth? | Limits |
| --- | --- | --- | --- |
| HiRISE Jezero DTM, USGS Mars 2020 TRN mosaic (DOI 10.5066/P9REJ9JN, CC0 1.0) | 1 m validation truth, degraded to 20 m and 200 m | Yes | 5.3 GB zip. Crop with windowed reads. Verify CRS and bounds |
| HiRISE orthophoto, USGS Mars 2020 TRN mosaic, 25 cm (DOI 10.5066/P9QJDP48) | Map basemap only, cropped to the DTM window by scripts/build_basemap.py | No | 6.9 GB (3.2 GB LZW GeoTIFF). Published bounds 18.3068 to 18.6693 N, 77.2229 to 77.5840 E. Use constraint: cite the authors; no warranty. Same projection as the DTM is checked by the script |
| JPL Mars Trek (trek.nasa.gov/mars) | Context and exploration link only. Not the live basemap (ADR 004) | No | Confirm download path per product |
| USGS-NASA Planetary Geologic Mapping Program | Terrain units for roughness and Hurst exponent per unit | No | Defines calibration classes |
| Curiosity route map (MSL) | Layout reference for the route panel | No | Visual only |
| Perseverance Raw Images Gallery | Qualitative context for demo | No | Check image licence before reuse |
| NASA Worldview | Not used | No | Earth imagery |

Rule: the HiRISE DTM is the only ground truth.
Each source's own data-use terms apply. NASA does not endorse non-U.S. Government websites.

Correction 2026-11-15: the DTM DOI was written here as 10.5066/P13CPYYU. The USGS page for the Mars 2020 TRN HiRISE DTM Mosaic gives 10.5066/P9REJ9JN, which README and the app already used.
