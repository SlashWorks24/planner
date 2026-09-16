"""Rebuild data/models.js from Rhino .obj exports (inches, Y-up).
Usage:  pip install shapely
        python3 tools/build_models.py path/to/obj/folder
Expects Object01.obj ... Object05.obj in that folder."""
import json, base64, struct, glob, sys, os
from array import array
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

SRC = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "models.js")
out = {}
for i in range(1, 6):
    key = f"0{i}"
    f = os.path.join(SRC, f"Object0{i}.obj")
    V, N, tris, tri_n = [], [], [], []
    same = True
    for line in open(f):
        if line.startswith('v '):
            p = line.split(); V.append((float(p[1]), float(p[2]), float(p[3])))
        elif line.startswith('vn '):
            p = line.split(); N.append((float(p[1]), float(p[2]), float(p[3])))
        elif line.startswith('f '):
            toks = line.split()[1:]
            vi = []
            for t in toks:
                parts = t.split('/')
                a = int(parts[0]); a = a - 1 if a > 0 else len(V) + a
                if len(parts) > 2 and parts[2]:
                    n = int(parts[2]); n = n - 1 if n > 0 else len(N) + n
                    if n != a: same = False
                vi.append(a)
            for k in range(1, len(vi) - 1):
                tris.append((vi[0], vi[k], vi[k + 1]))
    xs = [v[0] for v in V]; ys = [v[1] for v in V]; zs = [v[2] for v in V]
    cx = (min(xs) + max(xs)) / 2; cz = (min(zs) + max(zs)) / 2; y0 = min(ys)
    # recenter, sit on floor, rotate 180deg about Y so the front faces +Z
    P = [(x - cx, y - y0, z - cz) for x, y, z in V]  # front faces +Z (chair back is at -Z)
    NN = [(n[0], n[1], n[2]) for n in N] if (same and len(N) == len(V)) else None
    pos = array('f', [c for p in P for c in p])
    idx = array('H', [c for t in tris for c in t])
    rec = {
        "w": round(max(xs) - min(xs), 3), "d": round(max(zs) - min(zs), 3), "h": round(max(ys) - y0, 3),
        "pos": base64.b64encode(pos.tobytes()).decode(),
        "idx": base64.b64encode(idx.tobytes()).decode(),
    }
    if NN:
        nb = array('b', [max(-127, min(127, round(c * 127))) for n in NN for c in n])
        rec["nrm"] = base64.b64encode(nb.tobytes()).decode()
    polys = []
    for a, b, c in tris:
        pg = Polygon([(P[a][0], P[a][2]), (P[b][0], P[b][2]), (P[c][0], P[c][2])])
        if pg.area > 1e-6: polys.append(pg)
    u = unary_union(polys).buffer(0.03).buffer(-0.03).simplify(0.015)
    geoms = list(u.geoms) if isinstance(u, MultiPolygon) else [u]
    rp = lambda seq: [[round(x, 2), round(y, 2)] for x, y in list(seq)[:-1]]
    rec["polys"] = [{"ext": rp(g.exterior.coords), "holes": [rp(h.coords) for h in g.interiors if Polygon(h).area > 0.5]} for g in geoms if g.area > 0.5]
    rec["hull"] = rp(u.convex_hull.simplify(0.01).exterior.coords)
    out[key] = rec
    print(key, len(V), 'verts', len(tris), 'tris', 'normals' if NN else 'NO normals',
          rec['w'], rec['d'], rec['h'], 'outline pts', [len(p['ext']) for p in rec['polys']], 'holes', [len(p['holes']) for p in rec['polys']], 'hull', len(rec['hull']))
js = "const MODEL_DATA = " + json.dumps(out, separators=(',', ':')) + ";"
open(OUT, 'w').write(js + "\n")
print('models.js bytes', len(js))
