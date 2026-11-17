import json, sys
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import skeletonize

img = np.array(Image.open('sig.png').convert('L')) < 128
dt = ndimage.distance_transform_edt(img)
sk = skeletonize(img)
H, W = sk.shape
nb = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
pts = set(zip(*np.nonzero(sk)))
def neigh(p):
    y, x = p
    return [(y+dy, x+dx) for dy, dx in nb if (y+dy, x+dx) in pts]
deg = {p: len(neigh(p)) for p in pts}
nodes = {p for p in pts if deg[p] != 2}
used = set()
branches = []
def ekey(a, b): return (a, b) if a < b else (b, a)
for n in nodes:
    for m in neigh(n):
        if ekey(n, m) in used: continue
        path = [n, m]; used.add(ekey(n, m))
        prev, cur = n, m
        while cur not in nodes:
            nxt = [q for q in neigh(cur) if q != prev and ekey(cur, q) not in used]
            if not nxt: break
            used.add(ekey(cur, nxt[0])); prev, cur = cur, nxt[0]; path.append(cur)
        branches.append(path)
# isolated loops (all degree 2)
rest = {p for p in pts if p not in nodes and not any(ekey(p, q) in used for q in neigh(p))}
while rest:
    s = rest.pop(); path = [s]; prev = None; cur = s
    while True:
        nxt = [q for q in neigh(cur) if q != prev and ekey(cur, q) not in used]
        if not nxt: break
        used.add(ekey(cur, nxt[0])); prev, cur = cur, nxt[0]; rest.discard(cur); path.append(cur)
        if cur == s: break
    branches.append(path)

def rdp(P, eps):
    if len(P) < 3: return P
    a, b = np.array(P[0]), np.array(P[-1]); d = b - a; L = np.hypot(*d)
    arr = np.array(P)
    if L == 0: dist = np.hypot(*(arr - a).T)
    else: dist = np.abs(d[0]*(arr[:,1]-a[1]) - d[1]*(arr[:,0]-a[0])) / L
    i = int(dist.argmax())
    if dist[i] > eps: return rdp(P[:i+1], eps)[:-1] + rdp(P[i:], eps)
    return [P[0], P[-1]]

out = []
for b in branches:
    L = sum(np.hypot(b[i][0]-b[i+1][0], b[i][1]-b[i+1][1]) for i in range(len(b)-1))
    if L < 4: continue
    xs = [p[1] for p in b]
    if b[-1][1] < b[0][1]: b = b[::-1]  # draw left -> right
    w = max(dt[p] for p in b)
    simp = rdp([(int(p[1]), int(p[0])) for p in b], 0.8)
    out.append({'pts': simp, 'len': float(L), 'minx': int(min(xs)), 'w': float(w)})
print(len(out), 'branches', file=sys.stderr)
json.dump(out, open('branches.json', 'w'))
