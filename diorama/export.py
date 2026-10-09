"""Export a look/scenes.py scene (the 2D design used by the films) as JSON polygons + a sky PNG, for Blender.
    python export.py zong out/"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dark', 'look'))
import numpy as np, cv2
import scenes as LS
from core import stroke_poly, sky_render
name, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
sc = LS.SCENES[name]()
items = []
for it in sc.items:
    polys = [np.asarray(p, float).tolist() for p in it.polys]
    for p, w in it.lines:
        if len(p) >= 2 and w > 0.4:
            polys.append(stroke_poly(p, w).tolist())
    if polys:
        items.append(dict(name=it.name, z=float(it.z), col=[float(c) for c in it.col], mat=it.mat, emit=float(it.emit),
                          alpha=float(it.alpha), line=bool(it.lines) and not it.polys, polys=polys))
lights = [dict(x=L.x, y=L.y, col=[float(c) for c in L.col], I=float(L.I), r=float(L.r), z=float(L.z)) for L in sc.lights]
sky = sky_render(sc, 1080, 1920, 1.0)
sky = np.clip(1 - np.exp(-np.maximum(sky, 0) * 1.6), 0, 1) ** (1 / 1.2)
cv2.imwrite(os.path.join(out, name + '_sky.png'), (sky[..., ::-1] * 255).astype(np.uint8))
json.dump(dict(items=items, lights=lights, key_dir=list(sc.key_dir), key_col=[float(c) for c in sc.key_col],
               amb=[float(c) for c in sc.amb], sun=sc.sun), open(os.path.join(out, name + '.json'), 'w'))
print(name, len(items), 'items', len(lights), 'lights')
