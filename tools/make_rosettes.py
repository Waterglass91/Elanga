"""Generate a seamless black-panther rosette tile (assets/panther-rosettes.svg).

    python3 tools/make_rosettes.py

Rosettes are broken rings of irregular blobs, the way they show on a black
panther's coat in raking light. Original artwork, drawn procedurally.
"""
import math
import random
from pathlib import Path

random.seed(19)                  # his number, and a stable result
T = 260                          # tile size
COLOR = '#08090B'
shapes = []


def blob_points(rx, ry, rot):
    """An irregular blob outline (jittered ellipse), relative to its centre."""
    n = 7
    pts = []
    c, s = math.cos(rot), math.sin(rot)
    for i in range(n):
        a = 2 * math.pi * i / n
        k = random.uniform(0.78, 1.12)
        x, y = rx * k * math.cos(a), ry * k * math.sin(a)
        pts.append((x * c - y * s, x * s + y * c))
    return pts


def blob(cx, cy, pts):
    """Closed smooth curve through the blob points, placed at (cx, cy)."""
    P = [(cx + x, cy + y) for x, y in pts]
    n = len(P)
    d = f'M{(P[0][0] + P[-1][0]) / 2:.1f} {(P[0][1] + P[-1][1]) / 2:.1f}'
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        d += f'Q{p[0]:.1f} {p[1]:.1f} {(p[0] + q[0]) / 2:.1f} {(p[1] + q[1]) / 2:.1f}'
    return d + 'Z'


# rosette centres spread over the tile with a minimum spacing
centres = []
while len(centres) < 8:
    c = (random.uniform(0, T), random.uniform(0, T))
    if all(min(abs(c[0] - o[0]), T - abs(c[0] - o[0])) ** 2 + min(abs(c[1] - o[1]), T - abs(c[1] - o[1])) ** 2 > 74 ** 2 for o in centres):
        centres.append(c)

for cx, cy in centres:
    r = random.uniform(19, 24)
    n = random.randint(3, 5)
    start = random.uniform(0, 2 * math.pi)
    for i in range(n):
        if random.random() < 0.12:
            continue                                  # broken ring
        a = start + 2 * math.pi * i / n + random.uniform(-0.2, 0.2)
        shapes.append((cx + r * math.cos(a), cy + r * math.sin(a), random.uniform(11, 15), random.uniform(6, 8.5), a + math.pi / 2))
# a few loose spots between rosettes
for _ in range(10):
    shapes.append((random.uniform(0, T), random.uniform(0, T), random.uniform(2.6, 4.5), random.uniform(2.2, 3.6), random.uniform(0, math.pi)))

paths = []
for cx, cy, rx, ry, rot in shapes:
    pts = blob_points(rx, ry, rot)                     # same jitter for every wrapped copy
    for dx in (-T, 0, T):                             # wrap copies: seamless tile
        for dy in (-T, 0, T):
            x, y = cx + dx, cy + dy
            if -20 < x < T + 20 and -20 < y < T + 20:
                paths.append(blob(x, y, pts))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}">'
       f'<path fill="{COLOR}" d="{"".join(paths)}"/></svg>\n')
out = Path(__file__).resolve().parent.parent / 'assets' / 'panther-rosettes.svg'
out.write_text(svg)
print(f'{out.name}: {len(shapes)} taches, {len(svg)} octets')
