"""Reusable scenes for the films: maps, plans, the Sphinx, timelines, quotes, documents, big numbers.
   Every function returns a shot dict (base + elements) that episode specs extend with `like()`."""
import math
from films import View, Axis, like

BONE, AMBER, SCAN, OCHRE, GOLD, RED = "#f5ecdc", "#e8b87a", "#9fd0ff", "#ec5a3c", "#f2c98e", "#ff7a6b"

# ---------------------------------------------------------------- Egypt
NILE = [(32.90, 24.09), (32.93, 24.45), (32.87, 24.98), (32.55, 25.29), (32.64, 25.69), (32.72, 26.16), (32.24, 26.05), (31.92, 26.23),
        (31.70, 26.55), (31.18, 27.18), (30.75, 28.10), (31.10, 29.07), (31.25, 29.85), (31.23, 30.05), (31.13, 30.19)]
ROSETTA = [(31.13, 30.19), (30.95, 30.55), (30.80, 30.90), (30.42, 31.40)]
DAMIETTA = [(31.13, 30.19), (31.20, 30.60), (31.45, 31.00), (31.81, 31.42)]
SITES = {"Giza": (31.134, 29.979), "Saqqara": (31.216, 29.871), "Tura": (31.28, 29.93), "Wadi al-Jarf": (32.658, 28.892), "Aswan": (32.90, 24.09),
         "Abydos": (31.92, 26.18), "Memphis": (31.255, 29.845), "Cairo": (31.235, 30.044), "Luxor": (32.64, 25.69)}


def egypt(lon0=28.5, lon1=34.8, lat0=23.5, lat1=31.8, rect=(40, 250, 920, 1100), pins=(), extra=()):
    v = View(lon0, lon1, lat0, lat1, rect)
    els = [{"k": "map", "land": v.land(), "rivers": [v.line(NILE), v.line(ROSETTA), v.line(DAMIETTA)], "in": -1}]
    for i, (name, kw) in enumerate(pins):
        x, y = v.p(*SITES[name])
        e = {"k": "pin", "x": x, "y": y, "t": name, "in": .3 + i * .35}
        e.update(kw); els.append(e)
    return {"base": "map", "cam": [1, 500, 860], "els": els + list(extra)}, v


# ---------------------------------------------------------------- Giza plateau plan (metres east / north of Khufu's centre)
def _m(lat, lon):
    return ((lon - 31.134358) * 111320 * math.cos(math.radians(29.979)), (lat - 29.979175) * 110574)


GP = {"khufu": (_m(29.979175, 31.134358), 230.3), "khafre": (_m(29.976058, 31.130744), 215.3), "menkaure": (_m(29.972500, 31.128333), 104.6),
      "sphinx": _m(29.975313, 31.137594), "wall": _m(29.9716, 31.1350), "town": _m(29.9702, 31.1367)}


def giza_plan(scale=.95, cx=500, cy=860, rot=0):
    """Top-down plan, north up. Pyramids as squares with their corner diagonals; causeways; the Sphinx; the Wall of
       the Crow and the builders' town south of it (positions approximate)."""
    def P(x, y):
        return [round(cx + (x + 150) * scale, 1), round(cy - (y + 420) * scale, 1)]
    els = []
    for k in ("khufu", "khafre", "menkaure"):
        (x, y), b = GP[k]; h = b / 2
        sq = [P(x - h, y - h), P(x + h, y - h), P(x + h, y + h), P(x - h, y + h)]
        els.append({"k": "poly", "p": sq, "fill": "rgba(220,191,148,.55)", "c": "#f2dcb4", "w": 1.8, "id": "pl-" + k})
        els.append({"k": "line", "p": [sq[0], sq[2]], "c": "#8c7152", "w": 1, "op": .8, "id": "pd1-" + k})
        els.append({"k": "line", "p": [sq[1], sq[3]], "c": "#8c7152", "w": 1, "op": .8, "id": "pd2-" + k})
    sx, sy = GP["sphinx"]
    els.append({"k": "rect", "x": P(sx - 40, sy + 10)[0], "y": P(sx - 40, sy + 10)[1], "w": 70 * scale, "h": 22 * scale, "fill": "rgba(220,191,148,.8)", "c": "#f2dcb4", "sw": 1.4, "id": "pl-sphinx"})
    kx, ky = GP["khafre"][0]
    els.append({"k": "line", "p": [P(kx + 108, ky), P(sx - 30, sy - 5)], "c": "#c9ad85", "w": 2.2, "op": .8, "id": "causeway"})
    wx, wy = GP["wall"]
    els.append({"k": "line", "p": [P(wx - 100, wy), P(wx + 100, wy)], "c": "#f2dcb4", "w": 5, "id": "wall"})
    tx, ty = GP["town"]
    els.append({"k": "rect", "x": P(tx - 110, ty + 120)[0], "y": P(tx - 110, ty + 120)[1], "w": 230 * scale, "h": 260 * scale, "fill": "rgba(236,90,60,.10)", "c": OCHRE, "sw": 1.6, "style": "inferred", "id": "town"})
    for gset in range(4):                                  # gallery blocks (schematic, after AERA plans)
        gx0, gy0 = tx - 95 + (gset % 2) * 105, ty + 100 - (gset // 2) * 120
        for i in range(7):
            q = P(gx0 + i * 13, gy0)
            els.append({"k": "rect", "x": q[0], "y": q[1], "w": 8 * scale, "h": 80 * scale, "fill": "rgba(236,160,120,.45)", "c": "none", "sw": 0, "id": f"gal{gset}{i}"})
    return {"base": "plan", "north": [900, 330], "cam": [1, 500, 860], "els": els}, P


# ---------------------------------------------------------------- the Sphinx in its enclosure, side view (east to the left)
def sphinx_side(tod="dawn", w=620, x=500, gy=1060, pyramid=True):
    els = []
    if pyramid:
        els.append({"k": "pyramid", "x": x + 180, "y": gy - 70, "w": 520, "cap": .1, "light": "left", "layer": "far", "id": "khafre"})
    els.append({"k": "poly", "p": [[-600, gy - 95], [x - w * .62, gy - 95], [x - w * .6, gy], [x + w * .6, gy], [x + w * .62, gy - 95], [1600, gy - 95], [1600, 2400], [-600, 2400]],
                "fill": "url(#k-sand)", "c": "rgba(255,226,190,.4)", "w": 1.5, "id": "encl"})
    els.append({"k": "sphinx", "x": x, "y": gy, "w": w, "id": "sphinx"})
    return {"base": "sky", "tod": tod, "ground": gy - 95, "sun": [180, gy - 330, 30], "cam": [1.35, 500, 960], "els": els}


# ---------------------------------------------------------------- time
def timeline(a, b, ticks, t="", y=860, log=False, x0=150, x1=850, base="dark"):
    ax = Axis(a, b, x0, x1, log)
    tk = [[ax.x(v), lab] for v, lab in ticks]
    return {"base": base, "cam": [1.22, 500, y - 40], "els": [{"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": tk, "t": t, "in": .1, "id": "axis"}]}, ax


def event(ax, v, text, y=820, row=0, c=AMBER, i=.4, sub=None):
    x = ax.x(v); yy = y - 70 - row * 92
    els = [{"k": "line", "p": [[x, y - 10], [x, yy + 12]], "c": c, "w": 1.6, "op": .8, "in": i},
           {"k": "circle", "x": x, "y": y, "r": 8, "fill": c, "c": "#fff6e6", "w": 2, "in": i},
           {"k": "label", "x": x, "y": yy, "t": text, "c": c, "in": i + .15}]
    if sub:
        els.append({"k": "label", "x": x, "y": yy + 30, "t": sub, "st": "small", "c": "#cbbca8", "in": i + .3})
    return els


# ---------------------------------------------------------------- words on screen
def quote(text, who, y=760, w=820, size=46):
    return {"base": "dark", "cam": [1, 500, 860], "els": [
        {"k": "label", "x": 92, "y": y - 70, "t": "“", "st": "big", "a": "start", "c": AMBER, "size": 150, "in": .1},
        {"k": "para", "x": 100, "y": y, "t": text, "w": w, "st": "ital", "size": size, "lh": size * 1.28, "c": BONE, "in": .2, "fx": "type", "dur": 2.2},
        {"k": "cap", "x": 100, "y": y + 250, "t": who, "a": "start", "in": 1.6}]}


def stat(num, unit, cap, sub=None, bg="dark", y=820):
    els = [{"k": "num", "x": 500, "y": y, "t": num, "u": unit, "in": .1, "fx": "pop"},
           {"k": "para", "x": 500, "y": y + 130, "t": cap, "w": 760, "st": "lab", "size": 30, "a": "middle", "c": "#e9dccb", "in": .5}]
    if sub:
        lines = max(1, -(-len(cap) // 46))                  # rough line count at 30px in 760px
        els.append({"k": "label", "x": 500, "y": y + 150 + lines * 40 + 24, "t": sub, "st": "small", "c": "#b9aa97", "in": .8})
    return {"base": bg, "cam": [1, 500, 860], "els": els}


def papyrus(lines_tr=None, x=150, y=360, w=700, h=820, cols=9, rows=11, kind="hieratic", holes=True, hl=None):
    hs = [[[x + w * .7, y + h * .1], [x + w * .78, y + h * .06], [x + w * .82, y + h * .16], [x + w * .74, y + h * .2]],
          [[x + w * .08, y + h * .78], [x + w * .16, y + h * .72], [x + w * .2, y + h * .84], [x + w * .1, y + h * .9]]] if holes else []
    els = [{"k": "glyphs", "x": x + 50, "y": y + 60, "w": w - 100, "h": h - 140, "rows": rows, "cols": cols, "kind": kind, "red": True, "in": .2, "fx": "fade"}]
    if hl:
        els.append(dict({"k": "hl"}, **hl, **{"in": 1.0}))
    return {"base": "paper", "kind": "papyrus", "x": x, "y": y, "w": w, "h": h, "holes": hs, "cam": [1, 500, 860], "els": els}


# ---------------------------------------------------------------- bodies, bones and things (drawn from simple outlines, labelled schematic)
def silhouette(x, y, h, t=None, c="#1a1511", i=.2, lab=None):
    """A standing figure of height h px, with an optional label under it."""
    els = [{"k": "glow", "x": x, "y": y - h * .5, "r": h * .55, "kind": "lamp", "op": .25, "in": i},
           {"k": "person", "x": x, "y": y, "h": h, "t": False, "color": c, "in": i}]
    if t:
        els.append({"k": "label", "x": x, "y": y + 36, "t": t, "st": "small", "in": i + .2})
    if lab:
        els.append({"k": "label", "x": x, "y": y - h - 22, "t": lab, "st": "small", "c": AMBER, "in": i + .3})
    return els


def skull(x, y, s=1.0, robust=False, c="#e8dcc6", i=.2):
    """Side view of an archaic human skull, facing left (schematic). robust: lower vault, bigger brow ridge."""
    v = .8 if robust else 1.0
    P = [(-95, 55), (-40, 62), (10, 58), (30, 40), (28, 8), (60, 10), (110, -8), (128, -44), (104, -92 * v), (44, -118 * v), (-20, -116 * v), (-70, -98 * v),
         (-102 if robust else -96, -70), (-124 if robust else -112, -58), (-112, -48), (-116, -34), (-122, -10), (-118, 10), (-112, 25), (-104, 30), (-100, 40)]
    pts = [[round(x + px * s, 1), round(y + py * s, 1)] for px, py in P]
    return [{"k": "poly", "p": pts, "fill": c, "c": "#fff6e6", "w": 1.8, "curve": True, "in": i},
            {"k": "circle", "x": x - 84 * s, "y": y - 50 * s, "r": 19 * s, "fill": "#2a2420", "c": "none", "w": 0, "in": i},
            {"k": "poly", "p": [[x - 110 * s, y - 30 * s], [x - 100 * s, y - 34 * s], [x - 102 * s, y - 12 * s], [x - 112 * s, y - 14 * s]], "fill": "#2a2420", "c": "none", "w": 0, "in": i},
            {"k": "line", "p": [[x - 112 * s, y + 25 * s], [x - 60 * s, y + 30 * s]], "c": "#8c7152", "w": 2, "op": .7, "in": i},
            {"k": "line", "p": [[x - 30 * s, y + 20 * s], [x + 28 * s, y + 8 * s]], "c": "#b9a888", "w": 1.4, "op": .6, "in": i},
            {"k": "circle", "x": x + 40 * s, "y": y - 6 * s, "r": 7 * s, "fill": "#2a2420", "c": "none", "w": 0, "in": i},
            {"k": "line", "p": [[x - 60 * s, y - 100 * v * s], [x + 20 * s, y - 60 * s], [x + 90 * s, y - 80 * v * s]], "c": "#b9a888", "w": 1.2, "op": .5, "curve": True, "in": i}]


def leg_bones(x, y, s=1.0, cut=None, healed=False, i=.2):
    """Tibia and fibula, standing; cut: fraction of length removed from the bottom (clean oblique cut)."""
    L = 520 * s; bot = y if not cut else y - L * cut
    tib = [[x - 22 * s, y - L], [x + 26 * s, y - L], [x + 16 * s, y - L * .8], [x + 12 * s, bot + (8 * s if cut else 0)], [x - 14 * s, bot - (10 * s if cut else 0)], [x - 12 * s, y - L * .8]]
    fib = [[x + 36 * s, y - L * .96], [x + 46 * s, y - L * .96], [x + 42 * s, bot + (4 * s if cut else 0)], [x + 34 * s, bot - (6 * s if cut else 0)]]
    els = [{"k": "poly", "p": tib, "fill": "#e8dcc6", "c": "#fff6e6", "w": 1.6, "curve": False, "in": i},
           {"k": "poly", "p": fib, "fill": "#d9ccb4", "c": "#fff6e6", "w": 1.4, "in": i}]
    if cut:
        ghost = [[x - 14 * s, bot - 10 * s], [x + 12 * s, bot + 8 * s], [x + 18 * s, y], [x - 18 * s, y]]
        els.append({"k": "poly", "p": ghost, "fill": "none", "c": "#e8dcc6", "w": 1.6, "style": "claimed", "in": i + .4})
        if healed:
            els.append({"k": "circle", "x": x, "y": bot, "r": 46 * s, "c": GOLD, "w": 2.2, "style": "inferred", "in": i + .8})
    return els


def footprints(x0, y0, x1, y1, n=8, s=1.0, c="#3a2c1e", i=.2):
    els = []
    for k in range(n):
        t = k / max(1, n - 1); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t; side = -1 if k % 2 else 1
        ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang) * 16 * s * side, math.cos(ang) * 16 * s * side
        cx, cy = x + nx, y + ny; ux, uy = math.cos(ang), math.sin(ang)
        pts = [[cx + ux * 28 * s + (-uy) * 8 * s, cy + uy * 28 * s + ux * 8 * s], [cx + ux * 30 * s - (-uy) * 9 * s, cy + uy * 30 * s - ux * 9 * s],
               [cx - ux * 4 * s - (-uy) * 8 * s, cy - uy * 4 * s - ux * 8 * s], [cx - ux * 26 * s - (-uy) * 6 * s, cy - uy * 26 * s - ux * 6 * s],
               [cx - ux * 28 * s + (-uy) * 6 * s, cy - uy * 28 * s + ux * 6 * s], [cx - ux * 2 * s + (-uy) * 9 * s, cy - uy * 2 * s + ux * 9 * s]]
        els.append({"k": "poly", "p": pts, "fill": c, "c": "rgba(0,0,0,.25)", "w": 1, "curve": True, "op": .85, "in": i + k * .18})
    return els


def idol(x, y, h, i=.2):
    """A tall carved wooden plank with faces and zigzag bands (after the Shigir idol, schematic)."""
    w = h * .09
    els = [{"k": "poly", "p": [[x - w, y], [x + w, y], [x + w * .9, y - h * .92], [x + w * .6, y - h], [x - w * .6, y - h], [x - w * .9, y - h * .92]], "fill": "#6b4a2e", "c": "#c9a070", "w": 1.6, "in": i}]
    for f in (.93, .62, .3):                                       # faces
        cy = y - h * f
        els += [{"k": "circle", "x": x - w * .35, "y": cy, "r": w * .14, "fill": "#2a1d12", "c": "none", "w": 0, "in": i + .2},
                {"k": "circle", "x": x + w * .35, "y": cy, "r": w * .14, "fill": "#2a1d12", "c": "none", "w": 0, "in": i + .2},
                {"k": "line", "p": [[x, cy + w * .1], [x, cy + w * .5]], "c": "#2a1d12", "w": 3, "in": i + .2},
                {"k": "line", "p": [[x - w * .3, cy + w * .75], [x + w * .3, cy + w * .75]], "c": "#2a1d12", "w": 3, "in": i + .2}]
    for b in (.8, .7, .5, .42, .18, .1):                           # zigzags
        cy = y - h * b; zz = [[x - w * .8 + j * w * .2, cy + (8 if j % 2 else -8)] for j in range(9)]
        els.append({"k": "line", "p": zz, "c": "#2a1d12", "w": 2.4, "op": .8, "in": i + .4})
    return els


def spear_point(x, y, h, c="#b9b2a6", i=.2):
    w = h * .32
    return [{"k": "poly", "p": [[x, y - h], [x + w / 2, y - h * .45], [x + w * .42, y], [x + w * .18, y - h * .06], [x, y + h * .02], [x - w * .18, y - h * .06], [x - w * .42, y], [x - w / 2, y - h * .45]], "fill": c, "c": "#fff6e6", "w": 1.4, "in": i},
            {"k": "poly", "p": [[x - w * .1, y - h * .05], [x + w * .1, y - h * .05], [x + w * .06, y - h * .4], [x - w * .06, y - h * .4]], "fill": "rgba(0,0,0,.2)", "c": "none", "w": 0, "in": i}]


def raft(x, y, w, i=.2):
    els = [{"k": "line", "p": [[x - w / 2 + k * w / 7, y - 6], [x - w / 2 + k * w / 7 + 8, y + 10]], "c": "#8a7a3a", "w": 9, "in": i} for k in range(8)]
    els += [{"k": "line", "p": [[x - w / 2, y - 2], [x + w / 2 + 10, y - 2]], "c": "#6b5a2a", "w": 3, "in": i},
            {"k": "line", "p": [[x - w / 2, y + 8], [x + w / 2 + 10, y + 8]], "c": "#6b5a2a", "w": 3, "in": i}]
    return els
