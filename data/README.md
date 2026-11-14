# Data folder

- raw/: downloaded source files. Not committed (see .gitignore). Record each file in manifest.csv.
- processed/: crops, degraded grids, slope rasters. Not committed. Rebuild with scripts/build_terrain.py.
- labels/: labelled sites, if used later. Committed when small.
- manifest.csv: source, URL, checksum, access date. Committed.

Never edit raw files in place.
