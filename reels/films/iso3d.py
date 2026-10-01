"""Isometric 3-D models for the films (world units: metres; x east, z south, y up)."""
import math
from scenes import GP

SPHINX_PROF = [(0, 0), (1.5, 3.3), (12.4, 3.6), (13.9, 8.8), (12.0, 14.6), (9.9, 18.2), (9.1, 22.6), (10.2, 27.0), (14.6, 29.6), (19.0, 27.0), (20.8, 19.7),
               (21.9, 15.0), (29.2, 15.7), (43.8, 15.0), (58.4, 12.8), (65.7, 11.7), (70.4, 9.5), (71.9, 5.1), (73, 0)]


def sphinx(x, z, y=0, c="#dcbf94", scale=1.0, **kw):
    """The Sphinx as its side profile (73 m long, 20 m high) extruded 19 m wide; the head faces east (-x)."""
    prof = [(px * scale - 36.5 * scale, py * scale * .68) for px, py in SPHINX_PROF]
    d = dict({"t": "ext", "prof": prof, "axis": "x", "x": x, "y": y, "at": z, "d": 19 * scale, "c": c, "flipN": True}, **kw)
    return [d]


def giza(pyr_c="#e2c79c", town=True, sph=True):
    """The plateau: pyramids at true relative size and place (north = -z)."""
    out = []
    for k in ("khufu", "khafre", "menkaure"):
        (x, n), b = GP[k]; h = {"khufu": 146.6, "khafre": 143.5, "menkaure": 65.5}[k]
        out.append({"t": "pyr", "x": x, "z": -n, "y": 0, "b": b, "h": h, "c": pyr_c, "id": k})
    if sph:
        sx, sn = GP["sphinx"]; out += sphinx(sx, -sn, 0, scale=1.0)
    wx, wn = GP["wall"]
    out.append({"t": "box", "x": wx, "z": -wn, "y": 0, "w": 200, "d": 10, "h": 10, "c": "#cdb48e", "id": "wall"})
    if town:
        tx, tn = GP["town"]
        for gs in range(4):
            gx0, gz0 = tx - 95 + (gs % 2) * 105, -tn - 100 + (gs // 2) * 120
            for i in range(7):
                out.append({"t": "box", "x": gx0 + i * 13, "z": gz0 + 40, "y": 0, "w": 8, "d": 80, "h": 4, "c": "#b88a64", "edge": "rgba(0,0,0,.25)"})
    return out


def great_pyramid(xray=True, void=True, nfc=False, shafts=False, reliev=True, glow_void=True):
    """The Great Pyramid with its known spaces, world x = north to south (metres from the centre), y up."""
    from giza import Section, BASE
    S = Section(); R = S.rooms(); c0 = BASE / 2
    X = lambda x: x - c0
    a = math.radians(26.0)
    g0, g1 = R["gg0"], R["gg1"]
    nx, ny = -math.sin(a) * 8.6, math.cos(a) * 8.6
    gg = {"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 2.1, "c": "#2a2420", "xray": False, "edge": "rgba(255,236,206,.7)",
          "prof": [[X(g0[0]), g0[1]], [X(g1[0]), g1[1]], [X(g1[0] + nx), g1[1] + ny], [X(g0[0] + nx), g0[1] + ny]]}
    items = [{"t": "pyr", "x": 0, "z": 0, "y": 0, "b": BASE, "h": 146.6, "c": "#e2c79c", "xray": xray, "id": "gp"}, gg,
             {"t": "box", "x": X(R["kc"][0]), "z": 0, "y": R["kc"][1], "w": 5.2, "d": 10.5, "h": 5.8, "c": "#4a4440", "xray": False, "id": "kc"},
             {"t": "box", "x": X(R["qc"][0]), "z": 0, "y": R["qc"][1], "w": 5.2, "d": 5.8, "h": 6.2, "c": "#4a4440", "xray": False, "id": "qc"},
             {"t": "line", "p": [[X(R["ent"][0]), R["ent"][1], 0], [X(R["sub"][0]), R["sub"][1], 0]], "c": "#f2dcb4", "w": 2, "op": .8},
             {"t": "line", "p": [[X(R["junc"][0]), R["junc"][1], 0], [X(g0[0]), g0[1], 0]], "c": "#f2dcb4", "w": 2, "op": .8},
             {"t": "line", "p": [[X(g0[0]), g0[1], 0], [X(R["qc"][0]) - 2.6, R["qc"][1], 0]], "c": "#f2dcb4", "w": 2, "op": .8}]
    if reliev:
        for i in range(5):
            items.append({"t": "box", "x": X(R["kc"][0]), "z": 0, "y": R["kc"][1] + 6.6 + i * 2.6, "w": 5.2, "d": 10.5, "h": 1.3, "c": "#6a605a", "xray": False, "edge": "rgba(255,236,206,.4)"})
    if void:
        t0, L, up = 14.0, 30.0, 16.0
        vx0, vy0 = g0[0] + t0 * math.cos(a) - math.sin(a) * up, g0[1] + t0 * math.sin(a) + math.cos(a) * up
        vx1, vy1 = vx0 + L * math.cos(a), vy0 + L * math.sin(a)
        items.append({"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 2.5, "c": "#9fd0ff", "style": "inferred", "xray": True, "edge": "#9fd0ff",
                      "prof": [[X(vx0), vy0], [X(vx1), vy1], [X(vx1) - math.sin(a) * 7, vy1 + math.cos(a) * 7], [X(vx0) - math.sin(a) * 7, vy0 + math.cos(a) * 7]], "id": "bv"})
        if glow_void:
            items.append({"t": "glow", "x": X((vx0 + vx1) / 2), "y": (vy0 + vy1) / 2 + 3, "z": 0, "r": 110, "kind": "blue", "pulse": True})
    if nfc:
        h = 20.0; x0 = h / math.tan(math.radians(51.84)) + .8
        items.append({"t": "box", "x": X(x0 + 4.5), "z": 0, "y": h, "w": 9, "d": 2, "h": 2.2, "c": "#9fd0ff", "xray": False, "edge": "#cfe6ff", "id": "nfc"})
    if shafts:
        kc = (X(R["kc"][0]), R["kc"][1] + 3); qc = (X(R["qc"][0]), R["qc"][1] + 3)
        for (x, y), dx, top in ((kc, 60, 85), (kc, -55, 81), (qc, 50, 60), (qc, -50, 58)):
            items.append({"t": "line", "p": [[x, y, 0], [x + dx, top, 0]], "c": "#9fd0ff", "w": 1.6, "op": .9})
    return items


def ground(r=300, c="#5e4c3a", grid=50, y=0.0):
    """A square of plateau under a model, with a faint 50 m grid for scale."""
    out = [{"t": "slab", "x0": -r, "z0": -r, "x1": r, "z1": r, "y": y, "c": c}]
    k = -r
    while k <= r:
        out.append({"t": "line", "p": [[k, y + .1, -r], [k, y + .1, r]], "c": "#f5ecdc", "w": .8, "op": .12, "ground": True})
        out.append({"t": "line", "p": [[-r, y + .1, k], [r, y + .1, k]], "c": "#f5ecdc", "w": .8, "op": .12, "ground": True})
        k += grid
    return out


STRATA = [{"h": 4, "c": "#a8845c"}, {"h": 16, "c": "#8a6a4a"}, {"h": 26, "c": "#6a513b"}]


def diorama(r=170, c="#43372b", grid=50, strata=STRATA, rz=None, cx=0.0, cz=0.0):
    """A floating block of ground: a gridded top and cut strata on its sides, the classic isometric table."""
    rz = rz or r
    x0, x1, z0, z1 = cx - r, cx + r, cz - rz, cz + rz
    out = [{"t": "block", "x0": x0, "x1": x1, "z0": z0, "z1": z1, "y": -.05, "layers": strata, "under": True, "xray": False, "edge": "rgba(255,236,206,.18)"},
           {"t": "slab", "x0": x0, "z0": z0, "x1": x1, "z1": z1, "y": 0, "c": c}]
    k = x0
    while k <= x1 + .1:
        out.append({"t": "line", "p": [[k, .1, z0], [k, .1, z1]], "c": "#f5ecdc", "w": .8, "op": .10, "ground": True})
        k += grid
    k = z0
    while k <= z1 + .1:
        out.append({"t": "line", "p": [[x0, .1, k], [x1, .1, k]], "c": "#f5ecdc", "w": .8, "op": .10, "ground": True})
        k += grid
    return out


def shot(items, cam=(1, 500, 900), s=1.7, x=500, y=1150, az=-28, spin=2.0, el=.32, table=170, stars=110, glow=True, **kw):
    """A whole iso shot: a dark field of stars, a soft floor glow, and the model standing on its diorama table."""
    els = []
    if glow:
        els.append({"k": "glow", "x": x, "y": y - 40, "r": 520, "kind": "lamp", "op": .18})
    base = (diorama(**table) if isinstance(table, dict) else diorama(table)) if table else []
    els.append({"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": base + list(items)})
    return dict({"base": "dark", "stars": stars, "cam": list(cam), "els": els}, **kw)


def lab(x, y, t, c=None, z=0, dy=-18):
    return {"t": "label", "x": x, "y": y, "z": z, "text": t, "st": "small", "c": c, "dy": dy}


def project(sh, p, t=0.0):
    """Where a world point lands on the frame (1000 x 1778) at time t, given the shot's iso element and camera."""
    e = next(x for x in sh["els"] if x.get("k") == "iso")
    az = math.radians(e.get("az", 35) + e.get("spin", 0) * t); ca, sa = math.cos(az), math.sin(az)
    x, y, z = p; rx, rz = x * ca - z * sa, x * sa + z * ca
    S, el, C30 = e.get("s", 4), e.get("el", .32), math.cos(math.pi / 6)
    wx, wy = e.get("x", 500) + (rx - rz) * C30 * S, e.get("y", 900) - y * S + (rx + rz) * el * S
    return wx, wy


def aim(sh, p, z, t=2.0, dy=0.0):
    """Point the camera at a world point (seen at time t, the middle of a slow spin)."""
    wx, wy = project(sh, p, t)
    sh["cam"] = [z, round(wx, 1), round(wy + dy, 1)]
    return sh


def relieving_stack(names=(0, 2, 3), granite="#8a6a62", lime="#cdb48e"):
    """The King's Chamber and the five low spaces above it, capped by a gable of limestone (a cutaway, metres)."""
    out = [{"t": "box", "x": 0, "z": 0, "y": 0, "w": 5.2, "d": 10.5, "h": 5.8, "c": "#2a2320", "edge": "rgba(255,236,206,.6)", "id": "kc"}]
    y = 5.8; labs = []
    for i in range(5):
        for j in range(8):  # granite beams, side by side, spanning north to south
            out.append({"t": "box", "x": 0, "z": -5.9 + j * 1.3 + .65 - .5, "y": y, "w": 8.2, "d": 1.24, "h": 1.3, "c": granite, "edge": "rgba(255,236,206,.35)"})
        y += 1.3
        out.append({"t": "box", "x": 0, "z": 0, "y": y, "w": 5.2, "d": 10.5, "h": .95, "c": "#1a1411", "edge": "rgba(255,236,206,.45)"})
        if i in names:
            labs.append({"t": "label", "x": -2.6, "y": y + .45, "z": 5.3, "text": "Khufu", "st": "ital", "c": "#e4553a", "dy": 8})
        y += .95
    out.append({"t": "ext", "axis": "x", "x": 0, "y": y, "at": 0, "d": 11.5, "c": lime, "prof": [[-5.4, 0], [5.4, 0], [0, 3.6]], "edge": "rgba(255,236,206,.5)", "over": 50})
    return out + labs, y


PLATEAU = {"r": 560, "rz": 640, "cx": -135, "cz": 470, "grid": 100,
           "strata": [{"h": 10, "c": "#a8845c"}, {"h": 40, "c": "#8a6a4a"}, {"h": 60, "c": "#6a513b"}]}


def plateau_labels(c=None, town=True):
    from scenes import GP
    L = [lab(0, 170, "Khufu", c), lab(-348, 165, "Khafre", c, z=345), lab(-581, 80, "Menkaure", c, z=738)]
    sx, sn = GP["sphinx"]; L.append(lab(sx, 40, "Sphinx", c, z=-sn))
    if town:
        tx, tn = GP["town"]; L.append(lab(tx, 40, "builders' town", "#ffb09a", z=-tn))
    return L


def plateau(cam=None, az=15, spin=1.2, s=.56, el=.5, extra=(), town=True, night=False, **kw):
    """The Giza plateau as a diorama: three pyramids, the Sphinx, the wall and the town, true size and place."""
    sh = shot(giza(town=town) + list(extra), cam=cam or (1, 500, 900), s=s, x=500, y=1000, az=az, spin=spin, el=el, table=PLATEAU, **kw)
    if cam is None:
        aim(sh, (-135, 60, 470), 1.0, dy=60)
    return sh


def galleries(n=8, L=35.0, W=5.0, t=.7, h=2.2, c="#b88a64"):
    """Long mud-brick halls side by side (the Gallery Complex, simplified), plus a row of bread moulds."""
    out = []; x0 = -(n * W) / 2
    for i in range(n + 1):
        out.append({"t": "box", "x": x0 + i * W, "z": 0, "y": 0, "w": t, "d": L, "h": h, "c": c, "edge": "rgba(0,0,0,.25)"})
    for i in range(n):  # back wall with a doorway gap at the front
        out.append({"t": "box", "x": x0 + i * W + W / 2, "z": -L / 2, "y": 0, "w": W, "d": t, "h": h, "c": c, "edge": "rgba(0,0,0,.25)"})
        for k in range(3):  # low platforms, perhaps for sleeping, along each hall
            out.append({"t": "box", "x": x0 + i * W + W / 2, "z": -L / 2 + 6 + k * 9, "y": 0, "w": W - 2.2, "d": 6.5, "h": .45, "c": "#9d7656", "edge": "rgba(0,0,0,.2)"})
    for j in range(10):
        out.append({"t": "cyl", "x": x0 + 2 + j * (n * W - 4) / 9, "z": L / 2 + 5, "y": 0, "r": .7, "h": 1.2, "c": "#c0503a", "n": 12, "edge": "rgba(0,0,0,.3)"})
    return out


def serapeum_vaults(n=6, niche=6.8, wall=.9, depth=7.5, corr=3.2, h=3.0, rock="#8f7a60"):
    """A roofless cutaway of a stretch of the Greater Vaults: a corridor, side chambers, a granite box in most of them."""
    out = []; L = n * niche
    z0 = -L / 2
    out.append({"t": "flat", "pts": [[-corr / 2 - depth, z0], [corr / 2 + depth, z0], [corr / 2 + depth, z0 + L], [-corr / 2 - depth, z0 + L]], "y": .02, "c": "#2a2320"})
    for side in (-1, 1):
        xo = side * (corr / 2 + depth + .6)
        out.append({"t": "box", "x": xo, "z": 0, "y": 0, "w": 1.2, "d": L, "h": h, "c": rock, "edge": "rgba(0,0,0,.25)"})  # back rock wall
        for i in range(n + 1):
            out.append({"t": "box", "x": side * (corr / 2 + depth / 2), "z": z0 + i * niche, "y": 0, "w": depth, "d": wall, "h": h, "c": rock, "edge": "rgba(0,0,0,.25)"})
        for i in range(n):
            if (i + (side > 0)) % 3 == 2:
                continue
            zc = z0 + i * niche + niche / 2; xc = side * (corr / 2 + depth / 2 + .3)
            out.append({"t": "box", "x": xc, "z": zc, "y": 0, "w": 3.85, "d": 2.3, "h": 2.4, "c": "#3d3a40", "edge": "rgba(255,236,206,.35)"})
            out.append({"t": "box", "x": xc, "z": zc, "y": 2.4, "w": 3.85, "d": 2.3, "h": .9, "c": "#56525a", "edge": "rgba(255,236,206,.35)"})
    return out


def osiris_block(xr=12.0, zr=7.0, depth=32.0):
    """A cut block of bedrock with the shaft's three levels inside (translucent rock, simplified proportions)."""
    out = [{"t": "box", "x": 0, "z": 0, "y": -depth, "w": 2 * xr, "d": 2 * zr, "h": depth, "c": "#6f5a43", "xray": True, "edge": "rgba(255,236,206,.5)"},
           {"t": "box", "x": 0, "z": 0, "y": 0, "w": 2 * xr + 4, "d": 6, "h": .8, "c": "#b39a78", "edge": "rgba(255,236,206,.5)"}]  # the causeway above
    dk = "#0d0b09"; ed = "rgba(242,220,180,.8)"
    out += [{"t": "box", "x": 0, "z": 0, "y": -9, "w": 4, "d": 3, "h": 9, "c": dk, "edge": ed, "xray": True},
            {"t": "box", "x": 0, "z": 0, "y": -13, "w": 18, "d": 6, "h": 4, "c": dk, "edge": ed, "xray": True},
            {"t": "box", "x": 0, "z": 0, "y": -25, "w": 2.8, "d": 2.8, "h": 12, "c": dk, "edge": ed, "xray": True},
            {"t": "box", "x": 0, "z": 0, "y": -30, "w": 16, "d": 8, "h": 5, "c": dk, "edge": ed, "xray": True},
            {"t": "flat", "pts": [[-8, -4], [8, -4], [8, 4], [-8, 4]], "y": -29.6, "c": "#3f7fa6", "op": .85, "ground": False, "over": 1},
            {"t": "box", "x": 0, "z": 0, "y": -29.6, "w": 6, "d": 4, "h": .5, "c": "#6f5a43", "edge": ed, "over": 2},
            {"t": "box", "x": 0, "z": 0, "y": -29.1, "w": 3, "d": 1.4, "h": 1.5, "c": "#4a4040", "edge": ed, "over": 3}]
    for x in (-8, -5, 4, 6.5):
        out.append({"t": "box", "x": x, "z": 0, "y": -13, "w": 2.2, "d": 1.1, "h": 1.4, "c": "#6b6360", "edge": ed, "over": 1})
    return out


def strait_block(depth=25.0, zr=28.0):
    """A block diagram of a deep sea channel between two islands (vertical scale exaggerated: 1 unit = 10 m)."""
    land = [[-60, -35], [60, -35], [60, 14], [26, 14], [18, 0], [10, -depth], [-10, -depth], [-18, 0], [-26, 14], [-60, 14]]
    wx = 26 - 8 * (2 / 14.0)
    water = [[-wx, 12], [-18, 0], [-10, -depth], [10, -depth], [18, 0], [wx, 12]]
    out = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 2 * zr, "prof": land, "c": "#7a6248", "edge": "rgba(255,236,206,.45)"},
           {"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 2 * zr - .2, "prof": water, "c": "#3f86b0", "op": .6, "xray": False, "edge": "#9fd0ff", "over": 5},
           {"t": "line", "p": [[-18, .15, -zr], [18, .15, -zr], [18, .15, zr], [-18, .15, zr], [-18, .15, -zr]], "c": "#cfe6ff", "w": 2, "style": "inferred", "op": .9}]
    for x0, x1 in ((-60, -26), (26, 60)):  # green-brown island tops
        out.append({"t": "box", "x": (x0 + x1) / 2, "z": 0, "y": 14, "w": x1 - x0, "d": 2 * zr, "h": .6, "c": "#6d7a4a", "edge": "rgba(255,236,206,.3)"})
    return out
