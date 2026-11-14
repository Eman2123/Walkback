# Data sources

| Source | Role | Ground truth? | Limits |
| --- | --- | --- | --- |
| HiRISE Jezero DTM, USGS mosaic (DOI 10.5066/P13CPYYU) | 1 m validation truth, degraded to 20 m and 200 m | Yes | 5.3 GB zip. Crop with windowed reads. Verify CRS and bounds |
| JPL Mars Trek (trek.nasa.gov/mars) | Base imagery and MOLA context, tile checks | No | Confirm download path per product |
| USGS-NASA Planetary Geologic Mapping Program | Terrain units for roughness and Hurst exponent per unit | No | Defines calibration classes |
| Curiosity route map (MSL) | Layout reference for the route panel | No | Visual only |
| Perseverance Raw Images Gallery | Qualitative context for demo | No | Check image licence before reuse |
| NASA Worldview | Not used | No | Earth imagery |

Rule: the HiRISE DTM is the only ground truth.
Each source's own data-use terms apply. NASA does not endorse non-U.S. Government websites.
