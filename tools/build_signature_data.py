"""Build data/signature.js from the skeleton branches.

Usage:
    python3 tools/skeleton.py            # writes branches.json (needs sig.png, see that script)
    python3 tools/build_signature_data.py branches.json assets/signature-blanc.svg > data/signature.js

Each stroke is [delay s, duration s, mask width, SVG path]. Delays follow the
horizontal position so the signature is written left to right; durations follow
stroke length at a constant pen speed.
"""
import json
import re
import sys

FRONT = 3.0      # seconds for the writing front to cross the signature
SPEED = 620      # pen speed, px per second
X0, X1 = 34, 1943

branches = json.load(open(sys.argv[1]))
outline = re.search(r' d="([^"]+)"', open(sys.argv[2]).read()).group(1)

strokes = []
for br in branches:
    path = 'M' + ' L'.join(f"{x} {y}" for x, y in br['pts'])
    delay = round((br['minx'] - X0) / (X1 - X0) * FRONT, 3)
    dur = round(max(0.09, br['len'] / SPEED), 3)
    strokes.append([delay, dur, round(2 * br['w'] + 5, 1), path])
strokes.sort()

data = {'viewBox': '20 20 1940 620', 'outline': outline, 'strokes': strokes}
print("/* Signature Anthony Elanga — géométrie d'origine + tracés du stylo (tools/skeleton.py).")
print("   strokes: [délai s, durée s, largeur, chemin] */")
print('window.ELANGA_SIGNATURE = ' + json.dumps(data, separators=(',', ':')) + ';')
