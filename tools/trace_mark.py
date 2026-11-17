"""Trace a raster script mark (white on black) into the writing-animation data format.

    python3 tools/trace_mark.py assets/precispaspresse.jpg ELANGA_BRAND data/brand.js

Produces the filled outline (potrace, smooth Bézier curves) and the pen strokes
(skeleton of the letters) used by js/signature.js, plus a clean SVG of the outline
next to the source image.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from skimage.morphology import skeletonize
import potrace

src, var, out = sys.argv[1], sys.argv[2], sys.argv[3]
UP = 4            # upscale before tracing for smooth curves
FRONT = 2.2       # seconds for the writing front to cross the mark
SPEED = 520       # pen speed in mark units per second

# ---------- load, crop to the ink, upscale ----------
g = Image.open(src).convert('L')
a = np.array(g)
ys, xs = np.nonzero(a > 128)
pad = 12
x0, y0 = max(xs.min() - pad, 0), max(ys.min() - pad, 0)
x1, y1 = min(xs.max() + pad, a.shape[1]), min(ys.max() + pad, a.shape[0])
crop = g.crop((x0, y0, x1, y1))
W, H = crop.size
big = crop.resize((W * UP, H * UP), Image.LANCZOS).filter(ImageFilter.GaussianBlur(UP * 0.6))
ink = np.array(big) > 128

# ---------- outline with potrace ----------
bm = potrace.Bitmap(~ink)          # potracer fills the False pixels
plist = bm.trace(turdsize=UP * UP * 6, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                 alphamax=1.0, opticurve=True, opttolerance=0.2)


def f(v):
    return f'{v / UP:.2f}'.rstrip('0').rstrip('.')


parts = []
for curve in plist:
    s = curve.start_point
    d = [f'M{f(s.x)} {f(s.y)}']
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f'L{f(seg.c.x)} {f(seg.c.y)}L{f(seg.end_point.x)} {f(seg.end_point.y)}')
        else:
            d.append(f'C{f(seg.c1.x)} {f(seg.c1.y)} {f(seg.c2.x)} {f(seg.c2.y)} {f(seg.end_point.x)} {f(seg.end_point.y)}')
    d.append('Z')
    parts.append(''.join(d))
outline = ''.join(parts)

# ---------- pen strokes from the skeleton (at 2x) ----------
S = 2
mid = crop.resize((W * S, H * S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
m = np.array(mid) > 128
m = ndimage.binary_opening(m, iterations=1)
dt = ndimage.distance_transform_edt(m)
sk = skeletonize(m)
pts = set(zip(*np.nonzero(sk)))
NB = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def neigh(p):
    return [(p[0] + dy, p[1] + dx) for dy, dx in NB if (p[0] + dy, p[1] + dx) in pts]


def key(a, b):
    return (a, b) if a < b else (b, a)


nodes = {p for p in pts if len(neigh(p)) != 2}
used, branches = set(), []
for n in nodes:
    for q in neigh(n):
        if key(n, q) in used:
            continue
        path = [n, q]; used.add(key(n, q)); prev, cur = n, q
        while cur not in nodes:
            nxt = [r for r in neigh(cur) if r != prev and key(cur, r) not in used]
            if not nxt:
                break
            used.add(key(cur, nxt[0])); prev, cur = cur, nxt[0]; path.append(cur)
        branches.append(path)
rest = {p for p in pts if p not in nodes and not any(key(p, q) in used for q in neigh(p))}
while rest:                                     # closed loops (e.g. inside an "o")
    s0 = rest.pop(); path = [s0]; prev = None; cur = s0
    while True:
        nxt = [r for r in neigh(cur) if r != prev and key(cur, r) not in used]
        if not nxt:
            break
        used.add(key(cur, nxt[0])); prev, cur = cur, nxt[0]; rest.discard(cur); path.append(cur)
        if cur == s0:
            break
    branches.append(path)


def rdp(P, eps):
    if len(P) < 3:
        return P
    A, B = np.array(P[0], float), np.array(P[-1], float); d = B - A; L = np.hypot(*d)
    arr = np.array(P, float)
    dist = np.hypot(*(arr - A).T) if L == 0 else np.abs(d[0] * (arr[:, 1] - A[1]) - d[1] * (arr[:, 0] - A[0])) / L
    i = int(dist.argmax())
    return rdp(P[:i + 1], eps)[:-1] + rdp(P[i:], eps) if dist[i] > eps else [P[0], P[-1]]


xmin = W; xmax = 0
items = []
for b in branches:
    L = sum(np.hypot(b[i][0] - b[i + 1][0], b[i][1] - b[i + 1][1]) for i in range(len(b) - 1)) / S
    if L < 2:
        continue
    if b[-1][1] < b[0][1]:
        b = b[::-1]                                # draw left to right
    w = max(dt[p] for p in b) / S
    poly = rdp([(p[1] / S, p[0] / S) for p in b], 0.5)
    mx = min(p[1] for p in b) / S
    xmin, xmax = min(xmin, mx), max(xmax, mx)
    items.append((mx, L, w, poly))

strokes = []
for mx, L, w, poly in items:
    path = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in poly)
    strokes.append([round((mx - xmin) / max(1, xmax - xmin) * FRONT, 3),
                    round(max(0.06, L / SPEED), 3), round(2 * w + 4, 1), path])
strokes.sort()

data = {'viewBox': f'0 0 {W} {H}', 'width': W, 'height': H, 'outline': outline, 'strokes': strokes}
with open(out, 'w') as fh:
    fh.write(f'/* Marque « PrécisPasPressé » — contour vectorisé (potrace) + tracés du stylo. Généré par tools/trace_mark.py */\n')
    fh.write(f'window.{var} = ' + json.dumps(data, separators=(',', ':')) + ';\n')
svg_out = src.rsplit('.', 1)[0] + '.svg'
with open(svg_out, 'w') as fh:
    fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
             f'<title>PrécisPasPressé</title><path fill="#FFFFFF" fill-rule="evenodd" d="{outline}"/></svg>\n')
print(f'{W}x{H}  curves={len(plist)}  strokes={len(strokes)}  outline={len(outline)} chars  -> {out}, {svg_out}')
