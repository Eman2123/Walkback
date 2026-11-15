"""Builds the pixel-art favicon (16 x 16 grid) as SVG, PNG and ICO.

Run from the web folder:  python scripts/make_favicon.py
Needs Pillow. Writes into public/.
"""
import math
from pathlib import Path

from PIL import Image

N = 16
NIGHT, STAR = "#1b1226", "#f5e6c8"
LIGHT, BASE, SHADE, DEEP = "#ff9a5c", "#e2582c", "#a63a22", "#6e2418"
DOME, DOME_HI, DOME_BASE = "#7fe8ff", "#e8fbff", "#f5e6c8"
OUTLINE = "#0d0814"

grid = [[NIGHT] * N for _ in range(N)]
for x, y in [(1, 2), (13, 1), (14, 6), (2, 12), (11, 14), (6, 0)]:
    grid[y][x] = STAR

cx, cy, r = 7.5, 8.0, 6.6
for y in range(N):
    for x in range(N):
        d = math.hypot(x - cx, y - cy)
        if d <= r + 0.7 and d > r - 0.3:
            grid[y][x] = OUTLINE
        elif d <= r - 0.3:
            # light comes from the top-left
            t = ((x - cx) * 0.7 + (y - cy) * 0.7) / r
            grid[y][x] = LIGHT if t < -0.35 else BASE if t < 0.25 else SHADE if t < 0.65 else DEEP
for x, y in [(5, 5), (6, 5), (9, 6), (4, 8), (10, 10), (8, 11)]:
    if grid[y][x] in (BASE, SHADE, LIGHT):
        grid[y][x] = SHADE if grid[y][x] != SHADE else DEEP

# Habitat dome on the surface
dome = {
    (6, 8): DOME_HI, (7, 8): DOME, (8, 8): DOME,
    (5, 9): DOME, (6, 9): DOME_HI, (7, 9): DOME, (8, 9): DOME, (9, 9): DOME,
    (5, 10): DOME_BASE, (6, 10): DOME_BASE, (7, 10): DOME_BASE, (8, 10): DOME_BASE, (9, 10): DOME_BASE,
}
for (x, y), c in dome.items():
    grid[y][x] = c
for x in range(4, 11):
    if grid[11][x] != NIGHT:
        grid[11][x] = OUTLINE if x in (4, 10) else grid[11][x]

out = Path(__file__).resolve().parent.parent / "public"
out.mkdir(exist_ok=True)

rects = "".join(
    f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>'
    for y, row in enumerate(grid) for x, c in enumerate(row)
)
(out / "favicon.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" shape-rendering="crispEdges">{rects}</svg>\n',
    encoding="utf-8",
)

img = Image.new("RGB", (N, N))
img.putdata([tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for row in grid for c in row])
for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png")]:
    img.resize((size, size), Image.NEAREST).save(out / name)
img.resize((48, 48), Image.NEAREST).save(out / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote", sorted(p.name for p in out.glob("*") if p.name.startswith(("favicon", "apple", "icon"))))
