"""LF.03 Göbekli Tepe: What the Stones Say. A 16:9 long film (about eleven minutes) on one wall (see films/long/LONG_ENGINE.md).

Script: films/long/lf-gobekli/script.json (every narration line kept word for word; only [go:N|t] markers added, N = the shot index
below, one shot per script shot s1..s64 in order). Facts: the script's facts_added and sources (DAI excavation reports, Dietrich et al.
2012 and 2019, Clare 2020, Kinzel et al. 2020, Peters & Schmidt 2004, Notroff et al. 2017, Sweatman & Tsikritsis 2017, Sweatman 2024,
Holliday et al. 2023, Karul 2021, Özdoğan 2022). Shorts reused: 'gobekli' (lg_a.py: the hill as a hundred squares, through a window;
its T-pillar drawing), 'sky-fell' (lg_c.py: the thermometer's curve of the Younger Dryas, redrawn wide) and 'lost-civilization' (f04.py:
its idea, drown and minds scenes, redrawn wide). Drawings are schematic and true to the numbers said: solid = measured, dashed =
inferred, dotted = claimed.

How the wall is built: most shots are panels of their own. A shot that adds to a picture already on the wall (a push-in on a pillar, a
second line on a timeline) is an alias of that panel with its own camera; its additions ("late" elements) are attached to the step the
camera makes for it, so they build on that step's clock (mural.wall() only adds to a panel on its first visit or at a line start; see
_attach()). Two shots are merged into the next panel because a chapter card holds their sentence: s7 (the name, on the map panel of s6)
and s46 (Pillar 43 located in Enclosure D, the small plan beside the Vulture Stone of s47).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-gobekli/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-gobekli/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-gobekli RC_FILMS_EPS=/tmp/claude-0/sbx_lf-gobekli/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-gobekli/boards python3 films.py long.lf_gobekli
"""
import copy, math, random, re
from films import View
from mural import remix, inset, SENT
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, question, ellipse, scatter, tri, \
    BONE, AMBER, RED, GREEN, BLUE, LILAC, AU, SEA

GOLD = "#f2c98e"
STONE, STONE_E, RELIEF, INK = "#d9c29a", "#f2dcb4", "#efe0c0", "#3a2c20"
MUTED, AWAIT, GREY, WARM = "#cbbca8", "#9fd0ff", "#b8b2a8", "#ffb07a"
CARD = "#1b1511"                      # the flat ground of a card (masks paint over a drawing with it)
W_, H_ = 1778, 1000                   # the 16:9 frame: drawings in x 80..1700, y 120..800 (captions below 815, HUD above 110)
CAM = [1, 889, 500]


# ================================================================ drawing helpers (panel units)
def R(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def smooth(pts, n=8):
    """Points along a Catmull-Rom curve through pts (as kit.js draws curve=True), for a shape whose top is curved but whose corners are sharp."""
    P, out = [pts[0]] + list(pts) + [pts[-1]], []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(.5 * (2 * p1[j] + (p2[j] - p0[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out + [tuple(pts[-1])]


def hill(top, fill, edge, w, at, bottom=1010, **kw):
    """A hill or ground: a smooth top edge, straight down to the bottom of the panel."""
    pts = smooth(top)
    return poly(pts + [(pts[-1][0], bottom), (pts[0][0], bottom)], fill, edge, w, at, **kw)


def poly(pts, fill, c="none", w=0, at=0, fx=None, curve=False, op=None, **kw):
    e = {"k": "poly", "p": R(pts), "fill": fill, "c": c, "w": w, "curve": curve, "in": at}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(round(x, 1), round(y, 1), round(w, 1), round(h, 1), fill, c, sw, r, at, op, fx, **kw)


def tpill(x, by, h, at=0, front=1, w=None, c=STONE, edge=STONE_E, fx="rise", op=None, style=None, sw=1.6):
    """A T-pillar on its broad face (side elevation), base on by; the head overhangs towards `front` (+1 right, -1 left)."""
    w = w or h * .2
    hh, back, fwd, s = h * .24, w * .25, w * .75, front
    pts = [(x - s * w / 2, by), (x + s * w / 2, by), (x + s * w / 2, by - h + hh), (x + s * (w / 2 + fwd), by - h + hh), (x + s * (w / 2 + fwd), by - h),
           (x - s * (w / 2 + back), by - h), (x - s * (w / 2 + back), by - h + hh), (x - s * w / 2, by - h + hh)]
    e = poly(pts, c, edge, sw, at, fx, op=op)
    if style:
        e["style"] = style
    return e


def tick(x, y, at, c=GREEN, s=1.0):
    """A check mark that draws itself."""
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "draw", "dur": .45, "in": at}


def dimline(x1, y1, x2, y2, t, at, c=GOLD, lx=0, ly=None, dur=1.0):
    e = {"k": "dim", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "t": t, "c": c, "fx": "draw", "dur": dur, "in": at, "lx": lx}
    if ly is not None:
        e["ly"] = ly
    return e


def stars(n, x0, x1, y0, y1, at=-1, seed=3, layer=None):
    e = {"k": "stars", "n": n, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "seed": seed, "in": at}
    if layer:
        e["layer"] = layer
    return e


def crescent(cx, cy, r, at, c=LILAC):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-90, 91, 15)]
    pts += [(cx + .38 * r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(90, -91, -15)]
    return poly(pts, c, at=at, fx="pop")


def bandpoly(outline, y0, y1, n=6):
    """The part of a bowl (outline: a U from left rim to right rim) between depths y0 < y1, as a polygon."""
    half = len(outline) // 2
    left, right = outline[:half + 1], outline[half:]

    def xat(side, y):
        for (xa, ya), (xb, yb) in zip(side, side[1:]):
            if min(ya, yb) <= y <= max(ya, yb) and ya != yb:
                return xa + (xb - xa) * (y - ya) / (yb - ya)
        return side[-1][0] if abs(side[-1][1] - y) < abs(side[0][1] - y) else side[0][0]
    ys = [y0 + (y1 - y0) * k / n for k in range(n + 1)]
    return [(xat(left, y), y) for y in ys] + [(xat(right, y), y) for y in reversed(ys)]


# ---------------------------------------------------------------- animals (normalised: facing right, feet on y = 0, unit body length)
FOX = [(-.78, -.12), (-.60, -.24), (-.35, -.28), (0, -.30), (.22, -.30), (.28, -.40), (.31, -.50), (.35, -.41), (.39, -.50), (.41, -.39), (.55, -.33),
       (.40, -.27), (.32, -.22), (.30, -.15), (.30, 0), (.25, 0), (.24, -.12), (-.20, -.13), (-.22, 0), (-.28, 0), (-.32, -.15), (-.40, -.17), (-.62, -.10)]
BOAR = [(-.56, -.24), (-.50, -.30), (-.30, -.42), (0, -.47), (.20, -.45), (.32, -.38), (.46, -.28), (.56, -.18), (.58, -.12), (.50, -.10), (.44, -.14),
        (.36, -.12), (.30, -.10), (.30, 0), (.24, 0), (.22, -.10), (-.30, -.10), (-.32, 0), (-.38, 0), (-.40, -.12), (-.50, -.18)]
CRANE = [(-.45, -.56), (-.35, -.62), (-.10, -.70), (.12, -.70), (.20, -.78), (.22, -1.10), (.30, -1.18), (.46, -1.14), (.30, -1.12), (.27, -1.08), (.26, -.76),
         (.20, -.62), (.05, -.56), (.03, 0), (0, 0), (.0, -.55), (-.06, -.55), (-.09, 0), (-.12, 0), (-.10, -.56), (-.25, -.58)]
VULT = [(-.30, -.18), (-.45, -.30), (-.30, -.55), (-.05, -.70), (.15, -.72), (.22, -.78), (.20, -.90), (.28, -.98), (.38, -.94), (.42, -.86), (.34, -.86),
        (.30, -.80), (.30, -.70), (.36, -.55), (.30, -.35), (.15, -.20), (.10, 0), (.04, 0), (.05, -.18), (-.05, -.18), (-.06, 0), (-.12, 0), (-.10, -.20)]
GAZ = [(-.42, -.50), (-.40, -.55), (-.10, -.60), (.22, -.60), (.30, -.70), (.32, -.88), (.28, -1.04), (.36, -.92), (.40, -.82), (.50, -.76), (.48, -.71),
       (.38, -.70), (.34, -.58), (.30, -.45), (.30, 0), (.27, 0), (.25, -.42), (-.25, -.42), (-.28, 0), (-.31, 0), (-.33, -.45)]
AUR = [(-.56, -.50), (-.30, -.54), (.05, -.56), (.22, -.62), (.34, -.58), (.42, -.54), (.47, -.64), (.58, -.74), (.52, -.60), (.57, -.52), (.64, -.36),
       (.58, -.30), (.46, -.33), (.38, -.24), (.34, -.18), (.34, 0), (.27, 0), (.25, -.17), (-.30, -.19), (-.32, 0), (-.39, 0), (-.44, -.22), (-.54, -.30)]
ASS = [(-.52, -.30), (-.45, -.50), (-.10, -.52), (.20, -.52), (.30, -.62), (.34, -.80), (.33, -.92), (.37, -.84), (.40, -.92), (.40, -.80), (.52, -.62),
       (.50, -.57), (.40, -.62), (.34, -.50), (.30, -.38), (.30, 0), (.26, 0), (.24, -.32), (-.28, -.34), (-.30, 0), (-.34, 0), (-.36, -.36), (-.48, -.42)]
LEO = [(-.45, -.36), (.25, -.38), (.30, -.42), (.33, -.47), (.36, -.43), (.45, -.40), (.56, -.33), (.47, -.29), (.55, -.22), (.44, -.20), (.36, -.22),
       (.32, -.14), (.32, 0), (.26, 0), (.25, -.12), (-.30, -.14), (-.32, 0), (-.38, 0), (-.42, -.16), (-.48, -.30), (-.62, -.30), (-.75, -.36), (-.81, -.48),
       (-.75, -.57), (-.72, -.52), (-.76, -.46), (-.72, -.39), (-.62, -.34), (-.48, -.35)]


def beast(pts, x, y, s, at, c=MUTED, face=1, fx="rise", op=None, edge="none", w=0):
    return poly([(x + face * px * s, y + py * s) for px, py in pts], c, edge, w, at, fx, op=op)


def snake(x, y, s, at, c=MUTED, w=7, n=4):
    pts = [(x + s * (k / (2 * n) - .5), y + (s * .09 if k % 2 else -s * .09)) for k in range(2 * n + 1)]
    hx, hy = pts[-1]
    return [{"k": "line", "p": R(pts), "c": c, "w": w, "curve": True, "in": at, "fx": "draw", "dur": .6},
            oval(round(hx + 6, 1), round(hy, 1), round(w * 1.4, 1), round(w, 1), c, at=round(at + .4, 2), fx="pop")]


def scorpion(x, y, s, at, c=MUTED, w=3):
    """Seen from above, claws forward (up), tail curled over its back."""
    k = s / 100.
    P = lambda a, b: (x + a * k, y + b * k)
    out = [oval(x, y, round(14 * k, 1), round(26 * k, 1), c, at=at, fx="pop")]
    for sd in (-1, 1):
        out += [line(R([P(sd * 10, -20), P(sd * 26, -38), P(sd * 22, -54)]), at, c, w, draw=False),
                oval(*R([P(sd * 22, -60)])[0], round(8 * k, 1), round(6 * k, 1), c, at=at)]
        out += [line(R([P(sd * 12, dy), P(sd * 30, dy - 4), P(sd * 36, dy + 8)]), at, c, w * .8, draw=False) for dy in (-8, 2, 12, 22)]
    out.append(line(R([P(0, 24), P(4, 44), P(18, 58), P(30, 50), P(28, 36), P(20, 34)]), at, c, w * 1.4, curve=True, dur=.5))
    return out


def sheep(x, y, s, at, c="#efe6d2", fx="pop"):
    k = s / 100.
    out = [line(R([(x + dx * k, y - 22 * k), (x + dx * k, y)]), at, "#3a3530", max(2, 6 * k), draw=False) for dx in (-26, -12, 14, 28)]
    out += [oval(x, y - 40 * k, 46 * k, 26 * k, c, "#8a7a66", 1.2, at=at, fx=fx), oval(x + 46 * k, y - 50 * k, 15 * k, 11 * k, "#3a3530", at=at, fx=fx)]
    return out


def bird(x, y, s, at, c=RELIEF, edge=INK, face=1):
    k = s / 100.
    return [oval(x, y, round(34 * k, 1), round(20 * k, 1), c, edge, 1.5, at=at, fx="pop"),
            oval(round(x + face * 34 * k, 1), round(y - 16 * k, 1), round(11 * k, 1), round(10 * k, 1), c, edge, 1.5, at=at, fx="pop"),
            poly([(x + face * 42 * k, y - 18 * k), (x + face * 60 * k, y - 12 * k), (x + face * 42 * k, y - 10 * k)], edge, at=at),
            line(R([(x - 4 * k, y + 18 * k), (x - 6 * k, y + 40 * k)]), at, edge, 2, draw=False), line(R([(x + 8 * k, y + 18 * k), (x + 8 * k, y + 40 * k)]), at, edge, 2, draw=False)]


# ---------------------------------------------------------------- things
def pot(x, y, s, at, fx="pop"):
    k = s / 100.
    P = lambda pts: [(x + a * k, y + b * k) for a, b in pts]
    return [poly(P([(-26, -40), (26, -40), (36, -14), (30, 18), (18, 32), (-18, 32), (-30, 18), (-36, -14)]), "#c8743c", "#f4b27a", 1.5, at, fx, curve=True),
            line(R(P([(-24, -40), (24, -40)])), at, "#ffd9a8", 3, draw=False)]


def axe(x, y, s, at, c="#d9894a", fx="pop"):
    k = s / 100.
    P = lambda pts: [(x + a * k, y + b * k) for a, b in pts]
    return [line(R(P([(-22, 38), (16, -36)])), at, "#8a6a44", max(3, 7 * k), draw=False),
            poly(P([(4, -42), (40, -52), (46, -18), (12, -22)]), c, "#f4b27a", 1.5, at, fx)]


def tablet(x, y, s, at, fx="pop"):
    k = s / 100.
    out = [rect(x - 30 * k, y - 38 * k, 60 * k, 76 * k, "#b89a78", "#e9d6ad", 1.5, 8 * k, at, fx)]
    out += [tri(round(x - 18 * k + 15 * k * (j % 3), 1), round(y - 22 * k + 18 * k * (j // 3), 1), max(3, 5 * k), 30, "#5a4632", at) for j in range(9)]
    return out


def field(x, y, s, at, fx="pop"):
    k = s / 100.
    out = [rect(x - 50 * k, y - 26 * k, 100 * k, 52 * k, "#5a4a2c", "#8a7a4a", 1.2, 4, at, fx)]
    out += [line(R([(x - 42 * k + 14 * k * j, y + 16 * k), (x - 38 * k + 14 * k * j, y - 18 * k)]), at, GREEN, max(2, 4 * k), draw=False) for j in range(7)]
    return out


def house_round(x, y, r, at, c="#c9ad85"):
    return [{"k": "circle", "x": x, "y": y, "r": r, "fill": "#3a2f24", "c": c, "w": max(3, r * .16), "in": at, "fx": "pop"}]


def hearth(x, y, at, s=1.0):
    return [glow(x, y, round(60 * s), at, .85, "fire")] + [dot(round(x + 22 * s * math.cos(a), 1), round(y + 14 * s * math.sin(a), 1), round(6 * s, 1), "#8c7152", at)
                                                          for a in [2 * math.pi * j / 7 for j in range(7)]]


def cistern(x, y, s, at):
    k = s / 100.
    return [rect(x - 34 * k, y - 26 * k, 68 * k, 52 * k, "#2a5f78", BLUE, 2, 14 * k, at, "pop"), line(R([(x - 26 * k, y - 8 * k), (x + 26 * k, y - 8 * k)]), at, "#cfe6ff", 2, draw=False)]


def pins(x, y, at, c=AMBER, n=5, seed=4):
    r = random.Random(seed)
    out = []
    for j in range(n):
        px, py = x + r.uniform(-40, 40), y + r.uniform(-22, 22)
        out += [line(R([(px, py), (px, py + 14)]), round(at + .06 * j, 2), c, 2, draw=False), dot(round(px, 1), round(py, 1), 6, c, round(at + .06 * j, 2))]
    return out


def bathtub(x, y, s, at):
    k = s / 100.
    return [rect(x - 40 * k, y - 18 * k, 80 * k, 30 * k, "#dfe9ef", "#9fd0ff", 1.5, 12 * k, at, "pop"), line(R([(x - 44 * k, y - 18 * k), (x + 44 * k, y - 18 * k)]), at, "#ffffff", 2.5, draw=False),
            dot(round(x - 28 * k, 1), round(y + 16 * k, 1), round(4 * k, 1), "#9fd0ff", at), dot(round(x + 28 * k, 1), round(y + 16 * k, 1), round(4 * k, 1), "#9fd0ff", at)]


def quern(x, y, s, at):
    k = s / 100.
    return [oval(x, y, round(20 * k, 1), round(9 * k, 1), "#9a9086", "#d8d0c4", 1, at=at, fx="pop"), oval(round(x + 2 * k, 1), round(y - 8 * k, 1), round(9 * k, 1), round(5 * k, 1), "#cfc6b8", at=at, fx="pop")]


def spade(x, y, s, at):
    k = s / 100.
    return [line(R([(x, y - 70 * k), (x, y + 10 * k)]), at, "#8a6a44", 6 * k, draw=False), line(R([(x - 14 * k, y - 70 * k), (x + 14 * k, y - 70 * k)]), at, "#8a6a44", 6 * k, draw=False),
            poly([(x - 22 * k, y + 6 * k), (x + 22 * k, y + 6 * k), (x + 18 * k, y + 46 * k), (x, y + 60 * k), (x - 18 * k, y + 46 * k)], "#a9a49b", "#e8e4dc", 1.5, at, "pop")]


def candle_clock(x, y, s, at):
    k = s / 100.
    return [rect(x - 14 * k, y - 40 * k, 28 * k, 90 * k, "#efe6d2", "#fff6e6", 1, 4, at, "pop")] + \
           [line(R([(x - 14 * k, y - 20 * k + 18 * k * j), (x - 4 * k, y - 20 * k + 18 * k * j)]), at, "#8c7152", 2, draw=False) for j in range(4)] + \
           [poly([(x, y - 70 * k), (x + 9 * k, y - 50 * k), (x, y - 42 * k), (x - 9 * k, y - 50 * k)], "#ffd27a", at=at, curve=True), glow(x, round(y - 54 * k, 1), round(36 * k), at, .8)]


def city(x0, y, at, c=LILAC, s=1.0, step=.1):
    """A grand city drawn as a claim: towers, a stepped temple and a dome, outlines only (dotted)."""
    out, k = [], 0
    for dx, w, h in ((0, 46, 170), (60, 40, 120), (230, 50, 210), (300, 44, 140)):
        out.append(rect(x0 + dx * s, y - h * s, w * s, h * s, "none", c, 3, 2, round(at + step * k, 2), style="claimed")); k += 1
    tx = x0 + 160 * s
    for j in range(4):
        w = (110 - 24 * j) * s
        out.append(rect(tx - w / 2, y - 36 * s * (j + 1), w, 36 * s, "none", c, 3, 0, round(at + step * k, 2), style="claimed")); k += 1
    out.append(poly([(x0 + 360 * s + 34 * s * math.cos(math.radians(a)), y - 70 * s + 34 * s * math.sin(math.radians(a))) for a in range(180, 361, 20)] + [(x0 + 394 * s, y), (x0 + 326 * s, y)],
                    "none", c, 3, round(at + step * k, 2), style="claimed"))
    return out


def padlock(x, y, s, at, c=LILAC, style="claimed"):
    k = s / 100.
    return [rect(x - 55 * k, y - 20 * k, 110 * k, 84 * k, "rgba(201,193,238,.08)", c, 3, 12 * k, at, style=style),
            {"k": "line", "p": R([(x - 36 * k, y - 20 * k), (x - 34 * k, y - 56 * k), (x, y - 78 * k), (x + 34 * k, y - 56 * k), (x + 36 * k, y - 20 * k)]), "c": c, "w": 4, "style": style, "curve": True, "in": at},
            dot(x, round(y + 16 * k, 1), round(8 * k, 1), c, round(at + .3, 2))]


def stargroup(x, y, s, seed, at, c="#fff2c0", links=True, op=None, lc="#fff2c0", lstyle="claimed"):
    r = random.Random(seed)
    pts = [(x + r.uniform(-1, 1) * s, y + r.uniform(-.6, .6) * s) for _ in range(5)]
    pts.sort()
    out = [dot(round(px, 1), round(py, 1), 4, c, round(at + .04 * j, 2), op=op) for j, (px, py) in enumerate(pts)]
    if links:
        out.append({"k": "line", "p": R(pts), "c": lc, "w": 1.6, "style": lstyle, "in": round(at + .2, 2), "op": .8 if op is None else op, "keepop": True})
    return out


def cloud_face(x, y, s, at):
    k = s / 100.
    bumps = [(-80, 0), (-60, -26), (-26, -40), (14, -44), (50, -30), (78, -6), (70, 18), (30, 26), (-20, 26), (-62, 20)]
    out = [poly([(x + a * k, y + b * k) for a, b in bumps], "rgba(232,236,244,.22)", "#dfe6f0", 2, at, "fade", curve=True)]
    out += [dot(round(x - 22 * k, 1), round(y - 12 * k, 1), round(6 * k, 1), "#dfe6f0", round(at + .4, 2)), dot(round(x + 18 * k, 1), round(y - 14 * k, 1), round(6 * k, 1), "#dfe6f0", round(at + .5, 2)),
            line(R([(x - 22 * k, y + 8 * k), (x - 2 * k, y + 14 * k), (x + 20 * k, y + 6 * k)]), round(at + .7, 2), "#dfe6f0", 3, curve=True, dur=.4)]
    return out


def year_wheel(x, y, r, at, c=BLUE):
    out = [ring(x, y, r, at, c, 3)]
    out += [line(R([(x + r * .7 * math.cos(a), y + r * .7 * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))]), round(at + .3, 2), c, 2, draw=False)
            for a in [2 * math.pi * j / 12 for j in range(12)]]
    return out


def people(x, y, n, h, at, c="#e8d6b8", gap=None, step=.08):
    gap = gap or h * .42
    return [person(round(x + gap * j, 1), y, h, round(at + step * j, 2), c) for j in range(n)]


def figure_outline(x, by, h, at, c=RELIEF, w=3, style="known", fill="none", op=None):
    """A standing human figure without its head, drawn as a plain outline (no anatomical detail)."""
    k = h / 100.
    pts = [(-12, -96), (12, -96), (24, -86), (30, -50), (22, -48), (16, -76), (14, -44), (18, 0), (6, 0), (2, -38), (-2, -38), (-6, 0), (-18, 0), (-14, -44),
           (-16, -76), (-22, -48), (-30, -50), (-24, -86)]
    e = poly([(x + a * k, by + b * k) for a, b in pts], fill, c, w, at, "fade", op=op)
    e["style"] = style
    return e


# ---------------------------------------------------------------- a ring of pillars in perspective (an enclosure seen from the south)
A0 = math.radians(90 - 360 / 22)      # ring pillars start here: none stands straight in front of the central pair (seen from the south)
P43 = 5                               # the ring pillar nearest the north-west (back left from the south, top left in plan): Pillar 43


def enclosure(cx, cy, rx, ry, h, at, step=.1, n=11, hc=None, central=True, sunk=False, c=STONE, back_c="#b9a27c", style=None,
              wall_c="#8a7258", wall_w=None, op_back=None, edge=STONE_E, fill_floor="#17110c"):
    """A ring wall with n pillars set in it (broad faces seen on the sides, heads pointing inwards), two taller ones in the middle.
    Returns (elements in draw order, {pillar index: (x, base y, height)})."""
    out, where = [], {}
    if sunk:
        out.append(oval(cx, cy, rx, ry, fill_floor, at=at))
    out.append({"k": "line", "p": R(ellipse(cx, cy, rx, ry, 48)), "c": wall_c, "w": wall_w or max(5, ry * .16), "op": .9, "keepop": True, "curve": True, "in": at, "fx": "draw", "dur": 1.0,
                **({"style": style} if style else {})})
    angs = [(A0 + 2 * math.pi * k / n) % (2 * math.pi) for k in range(n)]
    order = sorted(range(n), key=lambda k: math.sin(angs[k]))
    t = at + .3
    hc = hc or h * 1.55
    fill = "none" if style else None

    def pil(k, t, col):
        a = angs[k]
        x, by, hh = cx + rx * math.cos(a), cy + ry * math.sin(a), h * (1 + .12 * math.sin(a))
        w = hh * .2 * (.45 + .55 * abs(math.cos(a)))
        where[k] = (round(x, 1), round(by, 1), round(hh, 1))
        return tpill(round(x, 1), round(by, 1), round(hh, 1), round(t, 2), 1 if math.cos(a) < 0 else -1, round(w, 1), fill or col, edge if not style else col, "rise",
                     op_back if (op_back and math.sin(a) < 0) else None, style)
    for k in order:
        if math.sin(angs[k]) < 0:
            out.append(pil(k, t, back_c)); t += step
    if central:
        for j, sd in enumerate((-1, 1)):
            out.append(tpill(round(cx + sd * rx * .18, 1), cy, round(hc, 1), round(t + .25 + .15 * j, 2), 1, round(hc * .22, 1), fill or c, edge if not style else c, "rise", None, style))
        t += .6
    for k in order:
        if math.sin(angs[k]) >= 0:
            out.append(pil(k, t, c)); t += step
    return out, where


# ---------------------------------------------------------------- a balance (beam tipped by ang degrees, right side down when ang > 0)
def balance(cx, py, L, ang, base_y, at, left=None, right=None, drop=170, pan=170, c=BONE):
    a = math.radians(ang)
    ends = [(cx - L / 2 * math.cos(a), py - L / 2 * math.sin(a)), (cx + L / 2 * math.cos(a), py + L / 2 * math.sin(a))]
    out = [rect(cx - 70, base_y - 10, 140, 14, "#5a4836", "#8c7152", 1.5, 4, at), line(R([(cx, base_y - 8), (cx, py)]), at, "#8c7152", 8, draw=False),
           line(R(ends), at, c, 6, draw=False), dot(cx, py, 10, GOLD, at, None)]
    for (ex, ey), stuff in zip(ends, (left, right)):
        fy = ey + drop
        out += [line(R([(ex, ey), (ex - pan / 2 + 10, fy)]), at, MUTED, 1.6, draw=False), line(R([(ex, ey), (ex + pan / 2 - 10, fy)]), at, MUTED, 1.6, draw=False),
                poly([(ex - pan / 2, fy), (ex + pan / 2, fy), (ex + pan / 2 - 18, fy + 16), (ex - pan / 2 + 18, fy + 16)], "#6b5a48", "#cbb79a", 1.5, at)]
        if stuff:
            out += stuff(round(ex, 1), round(fy, 1), at)
    return out


# ================================================================ timing: when each word is said (an estimate, from syllables)
TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # BCE: three letters
    w = a.lower()
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def _spoken(seg):
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", TAGS.sub(" ", seg))
    return re.sub(r"@\w+", "", s.replace("^", "").replace("*", "")).split()


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Clock:
    """Estimated word times per beat (seconds from the beat's first word). A shot's step starts at its [go:] marker (or at the beat's
    first word; at a chapter beat's second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said,
    counted from the start of shot i's step (or of shot `ref`'s)."""
    def __init__(self, beats):
        self.start, self.words = {}, {}
        for bi, b in enumerate(beats):
            t, ws, sents = 0.0, [], []
            for li, ln in enumerate(b["lines"]):
                if li:
                    t += LGAP
                cuts = [0] + [m.start() for m in SENT.finditer(ln) if m.start() > 0] + [len(ln)]
                for a, z in zip(cuts, cuts[1:]):
                    seg = ln[a:z]
                    p = re.search(r"\[p:([\d.]+)\]", seg)
                    r = RATE * (float(p.group(1)) if p else 1.0)
                    sents.append(t)
                    for m in GOM.finditer(seg):
                        self.start[int(m.group(1))] = (bi, t)
                    for w in _spoken(seg):
                        ws.append((_norm(w), t))
                        t += _syl(w) / r
                        if w[-1] in ",:;":
                            t += CGAP
                    t += SGAP
            frm = b["visual"]["from"]
            self.start.setdefault(frm, (bi, sents[1] if b.get("chapter") else 0.0))
            self.words[bi] = ws

    def at(self, i, phrase, ref=None, lo=.4):
        bi, ti = self.start[i]
        t0 = self.start[ref if ref is not None else i][1]
        want = [_norm(x) for x in phrase.split()]
        ws = self.words[bi]
        for k in range(len(ws)):
            if ws[k][1] >= ti - 1e-6 and [w for w, _ in ws[k:k + len(want)]] == want:
                return round(max(lo, ws[k][1] - t0), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))


# ================================================================ the narration (script.json, word for word, with [go:N|t] markers)
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


def BEATS():
    return [
        B('hook', 0, ["[d:intrigue][sfx:boom][act:hushed, awe]Stone ^giants, with arms and ^hands, on a hilltop in Turkey. [go:1|1.4][p:0.93][act:the number lands, slow][tune:fall]Carved about eleven and a half ^*thousand* years ago.",
          "[d:list][go:2|1.4][act:counting what they lacked][tune:level]No ^pottery. [act:same rhythm][tune:level]No ^metal. [act:same rhythm][tune:level]No ^writing. [act:the last one, slower][tune:level]No farm ^animals. [act:the child's question, leaning in][tune:rise]So who ^carved them?",
          "[d:tension][go:3|1.4][act:reporting it fairly, even]Some say: the survivors of a ^lost civilisation. [act:the second claim, intrigued][tune:fall]Others, that one pillar is the record@noun of a ^comet strike."]),
        B('title', 4, ["[d:calm][act:warm, setting out]Göbekli ^Tepe: [act:the promise, a small smile][tune:fall]what the stones say, and what they ^don't."], intro=True),
        B('world', 5, ["[d:calm][act:plain, orienting]This is Göbekli ^Tepe, on a limestone ridge near the city of ^Sanliurfa, in southeast Turkey. [act:a small smile]The name means something like Potbelly ^Hill.",
          "[d:build][go:7|1.4][act:storytelling, unhurried]In {1963|nineteen sixty-three}, surveyors saw broken slabs on it, and took them for ^gravestones of a much later age. [go:8|1.4][act:the turn, leaning in]In {1994|nineteen ninety-four}, the German archaeologist Klaus ^Schmidt looked again, [act:the moment, wonder][tune:fall]and recognised the head of a T-shaped ^pillar, like those he knew from a dig nearby."], chapter='Giants on Potbelly Hill'),
        B('collision', 9, ["[d:wonder][act:describing it, admiring]Digging began in {1995|nineteen ninety-five}. [act:the scale]Out of the hill came great round ^enclosures, up to about twenty metres across: [go:10|1.4][act:the recipe, clear][tune:level]a rubble wall, with pillars set into it facing ^inwards, [act:landing it][tune:fall]and two taller pillars standing free in the ^middle.",
          "[go:11|1.4][p:0.9][act:the number, savouring it]In the best preserved, Enclosure ^D, that central pair stands about five and a half ^metres tall: [act:an everyday picture, light][tune:fall]three grown-ups, stacked head to ^toe.",
          "[d:list][go:12|1.4][sfx:hit][act:inviting, intrigued]Look ^closer. [sfx:shimmer][act:a discovery][tune:level]An arm, bent at the ^elbow. [act:same rhythm][tune:level]Two hands, meeting over the ^belly. [act:same rhythm][tune:level]A belt, and a ^loincloth. [act:delighted, lightly][tune:fall]And under one arm, a ^fox.",
          "[d:reveal][go:13|1.4][p:0.93][act:the reveal, slow]The top of the T reads as a ^head, the shaft as a ^body. [act:careful, a hush]Most researchers see ^figures here: beings, or ancestors, in stone. [go:14|1.4][act:widening out, wonder][tune:level]Around them swarms a whole ^zoo in relief: [act:listing them][tune:fall]snakes most of all, then foxes, boars, cranes, vultures and ^scorpions."]),
        B('cost', 15, ["[d:build][p:0.93][act:curious, the method][tune:rise]How do you carve a stone giant without ^metal? [act:the answer, a smile]The answer lies in the ^quarry next door. [act:explaining, clear]Workers cut a channel around the shape with flint picks, [act:explaining, the next step]then levered the slab free along a natural seam, probably with wooden beams and ^wedges.",
          "[d:aside][go:16|1.4][p:0.9][act:the punchline, savouring it]One pillar never ^left: seven metres long, about fifty ^tonnes. [act:explaining, light]Perhaps a crack showed, and they ^stopped. [act:dry, a small smile][tune:fall]Even Stone Age engineers had ^bad days."]),
        B('reversal', 17, ["[d:reveal][act:the big question, leaning in][tune:rise]And the ^builders? [p:0.93][act:explaining, an everyday picture]A kitchen bin tells you the ^menu. [act:reading the result, precise]Here the bones are of gazelle, wild cattle and wild ^asses: [act:the point, firm][tune:fall]animals people ^hunted, not herded.",
          "[d:build][go:18|1.4][act:the old textbook, even][tune:level]For most of the twentieth century, the textbooks said: farming first, then ^monuments. [sfx:hit][act:the twist, deliberate][tune:fall]Here, the order runs the other ^way. [p:0.93][act:the landing, quiet wonder][tune:fall]The giants came ^first. [act:same rhythm][tune:fall]Farm animals and fully domesticated crops came ^later."]),
        B('world', 19, ["[d:calm][p:0.93][act:the child's question, curious][tune:rise]How do you date a ^stone? [act:plain, a small smile][tune:fall]Not directly. [act:explaining, the method]You date something that was once ^alive. [p:0.93][act:an everyday picture]Living things hold a trace of radioactive carbon, which fades after death at a steady pace, like a candle burning ^down: [act:the payoff, clear][tune:fall]measure what's left, and you know when it ^died."], chapter='Dating a hill of rubble'),
        B('collision', 20, ["[d:tension][act:the catch, leaning in]The catch: the enclosures are packed with rubble, bone and ^flint, [act:the problem, plain][tune:fall]and rubble ^moves. [go:21|1.4][p:0.93][act:an everyday picture, light]Dating the fill is like dating a house@noun from the junk swept into its ^cellar: [act:explaining][tune:fall]some is older than the house@noun, some ^newer. [go:22|1.4][act:a telling detail]Here, some younger samples even lie ^below older ones.",
          "[d:build][go:23|1.4][act:the better clock, pleased]So the team also dated ^plaster and mortar, put on the walls while the buildings ^stood. [p:0.9][act:precise, the number]Plaster from Enclosure D dates to between about nine thousand seven hundred and nine thousand three hundred ^BCE. [go:24|1.4][act:widening out][tune:level]The whole site runs from about nine and a half thousand to eight thousand BCE: [act:the payoff, wonder][tune:fall]fifteen centuries of building, repairing and ^rebuilding."]),
        B('reversal', 25, ["[d:reveal][act:storytelling, the old story]For about twenty years, the story was that when an enclosure went out of use@noun, people buried it on purpose, and ^fast. [act:a wry note][tune:fall]A ritual ^burial. [act:fair, reporting]It even fed a popular claim: that the site was buried to ^hide it.",
          "[d:build][go:26|1.4][sfx:shimmer][act:the turn, admiring the honesty]Then the excavators went back through their own records@noun. [p:0.93][act:explaining, clear]In {2020|twenty twenty}, the team under Lee ^Clare argued that most of the fill had slid in from higher ground, older and younger debris ^mixed. [go:27|1.4][act:a picture, vivid]Slope slides, perhaps after heavy rain or ^earthquakes, damaged the buildings, [act:warm][tune:fall]and people shored them up with terrace walls and ^repairs.",
          "[d:aside][go:28|1.4][act:fair, the counterweight][tune:level]But at Karahan ^Tepe, a sister site to the east, the excavator Necmi ^Karul describes fill laid in by stages, and capped with big flat ^stones. [act:plain][tune:fall]That one looks ^intentional. [go:29|1.4][p:0.93][act:the landing, even][tune:rise]So, hands or ^hillside? [act:weighing it, light][tune:fall]At Göbekli itself, the hillside is now the ^favourite."]),
        B('collision', 30, ["[d:calm][act:presenting it fairly, even]Now the boldest ^idea. [p:0.93][act:laying it out, measured]The writer Graham ^Hancock points to the ^timing. [go:31|1.4][act:the backdrop, graver]About twelve thousand nine hundred years ago, the warming world lurched back into the ^cold, the Younger ^Dryas, for some twelve centuries. [act:storytelling, a touch of grandeur][tune:fall]Soon after it ended, Göbekli Tepe ^rises.",
          "[d:build][go:32|1.4][act:his case, fair and vivid]Something this ambitious, he argues, is no first ^attempt. [p:0.93][act:the claim, measured]Survivors of a lost Ice Age civilisation, ruined by a ^comet, may have passed their knowledge to local ^hunters. [go:33|1.4][act:conceding, generous][tune:fall]And the Ice Age coasts, where such people might have lived, now lie under the ^sea."], chapter='Survivors of a lost world?'),
        B('cost', 34, ["[d:build][p:0.93][act:curious, the test][tune:rise]So how would we ^test it? [act:an everyday picture, warm]A visiting master cook leaves traces in your kitchen: a new pan, a spice from far ^away. [act:the expectation, clear][tune:fall]So we'd look for something with no local ^roots: a technique, a tool, a crop.",
          "[d:calm][go:35|1.4][act:reporting the finds, plain][tune:level]What the ground shows has local ^roots. [act:same rhythm][tune:level]Limestone from the plateau next ^door. [act:same rhythm][tune:level]Tools of the region's own Stone Age ^kinds. [act:the last item, landing][tune:fall]Carvings of the animals that roamed these very ^hills."]),
        B('reversal', 36, ["[d:reveal][sfx:hit][act:the turn, leaning in]And since {2015|twenty fifteen}, the dig has turned up something ^else. [act:counting the finds, delighted][tune:level]^Homes. [act:same rhythm][tune:level]Hearths, used@verb again and ^again. [act:same rhythm][tune:level]Beads of stone and ^bone. [go:37|1.4][act:gently, with care][tune:fall]A grave beneath one floor, holding the remains of at least three ^people.",
          "[d:build][go:38|1.4][p:0.93][act:explaining, a picture]There's no spring on the hill; the nearest is about five kilometres ^away. [go:39|1.4][act:the solution, admiring]So people cut channels in the rock, feeding cisterns that together could hold about a hundred and fifty cubic metres of ^rain. [act:an everyday picture, light][tune:fall]Nearly two thousand ^bathfuls.",
          "[d:build][go:40|1.4][act:the kitchen, vivid]And more than seven ^thousand tools for grinding and pounding ^food. [p:0.93][act:explaining, clear]With no big stores found, the team argues the food was made to be eaten ^fresh, perhaps at great work ^feasts. [act:dry, a small smile][tune:fall]Feed a crowd, and the crowd hauls your ^pillars."]),
        B('tag', 41, ["[d:wonder][act:widening out, wonder]And Göbekli isn't ^alone. [p:0.93][act:the scale]About a dozen sites with T-shaped pillars dot these hills: the Stone ^Hills. [go:42|1.4][act:vivid, a little awed]At Karahan Tepe, people carved a room three and a half metres into the ^bedrock, leaving ten pillars standing out of the living ^rock, [act:the image, hushed][tune:fall]and a human ^head looking on from the wall.",
          "[go:43|1.4][act:a second picture, intrigued]At another site, a carved ^scene: a man between two ^leopards. [go:44|1.4][p:0.93][act:the twist, landing it][tune:fall]No sign of a visiting cook, so ^far. [act:warm, the punch][tune:fall]Just a whole landscape of ^neighbours."]),
        B('world', 46, ["[d:calm][act:quiet wonder, presenting it]Back in Enclosure D stands Pillar {43|forty-three}: the Vulture ^Stone. [act:pointing them out, one by one][tune:level]A great vulture, with a disc beside its ^wing. [act:same rhythm][tune:level]Smaller birds, a scorpion, a ^snake. [act:same rhythm][tune:level]Three boxes with handles along the ^top. [act:low, careful][tune:fall]And near the bottom, a man without a ^head."], chapter='A comet on the Vulture Stone?'),
        B('collision', 47, ["[d:build][act:recounting a bold idea, fair]In {2017|twenty seventeen}, the chemical engineer Martin ^Sweatman and a colleague read@past this pillar as a ^star map. [act:their reading, vivid][tune:level]The animals are ^constellations; [act:completing it][tune:fall]the disc is the ^Sun.",
          "[d:calm][go:48|1.4][p:0.93][act:explaining, a picture]The trick: the Earth wobbles slowly, like a spinning ^top, once in about twenty-six thousand ^years. [act:explaining, clear]So the stars behind the Sun on the longest day slowly ^change. [act:the method, neat][tune:fall]Match the carving to one sky, and you get a ^date.",
          "[d:reveal][go:49|1.4][stamp:10,950 BCE ± 250|gold][p:0.9][act:their result, vivid]Their date: about ten thousand nine hundred and fifty ^BCE, give or take two hundred and fifty ^years. [act:the claim, intrigued]That's close@adj to a proposed ^comet strike at the start of the Younger ^Dryas. [act:their reading, grave][tune:fall]The headless man, they suggest, stands for ^death.",
          "[d:build][go:50|1.4][act:building, fair][tune:level]In {2024|twenty twenty-four}, Sweatman went ^further. [p:0.93][act:explaining, precise]He counts the V-shaped marks on one pillar as ^days: three hundred and sixty-five, twelve Moon-months plus eleven ^more. [act:his claim, measured][tune:fall]A calendar of Sun and Moon, he argues, the oldest ^known."]),
        B('reversal', 51, ["[d:reveal][act:the pushback, firm but fair]The excavators answered in the same journal, the same ^year. [p:0.9][act:the problem, plain][tune:fall]Their oldest date for Enclosure D, from its wall plaster, is seven hundred to a thousand years ^younger than that sky.",
          "[d:aside][go:52|1.4][act:the other side, fair][tune:level]Sweatman's side calls the pillar a ^memorial, and a memorial can be carved long after the ^event. [act:conceding][tune:fall]Possible. [p:0.93][act:the logic, gentle][tune:fall]But then the building can't vouch for the ^date: [act:the consequence]everything rests on the star ^matching.",
          "[d:build][go:53|1.4][p:0.93][act:the method problem, a picture]And star matching is ^flexible. [act:explaining, light]More than sixty pillars are known at the site, many of them carved: [act:the trap, a smile]pick a few, decide which animal is which star group, and patterns appear, like faces in ^clouds. [go:54|1.4][act:the overlooked detail, dry]And, they note, the headless man is carved with an erect ^phallus: [tune:fall]hardly a picture of ^death.",
          "[d:calm][go:55|1.4][act:the bigger picture, careful][tune:level]Even the comet is in ^dispute. [p:0.93][act:reporting both sides, fair]A large review in {2023|twenty twenty-three} called the Younger Dryas impact idea ^refuted; [act:the other side, even]its supporters, Sweatman among them, have published a ^rebuttal. [go:56|1.4][act:one more doubt, explaining][tune:fall]And if the enclosures had ^roofs, as some of the evidence suggests, they made poor ^observatories.",
          "[d:tension][go:57|1.4][p:0.93][act:the landing, quiet][tune:rise]A sky map with a date ^stamp? [act:plain, even][tune:fall]So far, the stamp and the stone disagree by ^centuries."]),
        B('weigh', 58, ["[d:verdict][p:0.95][act:taking stock, calm authority]Let's ^weigh it. [act:firm, plain][tune:level]Established: from about nine and a half thousand BCE, people here raised stone giants, without pottery, metal or farm ^animals. [act:steady][tune:level]Well documented: homes, hearths, cisterns, and a whole landscape of sister ^sites. [act:honest, open][tune:level]Still open: how many people lived here, and for how much of the ^year.",
          "[go:59|1.4][act:honest, open][tune:level]Open too: what the figures meant, whether the enclosures had roofs, and how much of the burying was done by ^hand. [act:firm, even][tune:fall]And ruled out, as far as thirty years of digging can tell: farm herds, metal tools and ^writing.",
          "[d:verdict][go:60|1.4][p:0.95][act:the bold claims, weighing them][tune:rise]A lost civilisation behind the ^giants? [act:even][tune:rise]A comet strike carved on the Vulture ^Stone? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:fair, plain][tune:fall]Not ruled out. [act:same rhythm][tune:fall]Just not ^shown. [act:fair, warm][tune:level]Both make predictions we can test, and that's to their ^credit. [act:plain, even][tune:fall]So far, the spade and the clock haven't delivered ^them."], chapter='The weighing'),
        B('test', 61, ["[d:build][p:0.93][act:practical, clear][tune:rise]What would change our ^minds? [act:the first test][tune:level]A tool, a crop or a technique with no local roots, in the oldest ^layers. [act:the second test][tune:level]Charcoal sealed under the foot of a standing pillar, and ^dated: [act:the payoff, precise][tune:fall]if Enclosure D reached back to about eleven thousand BCE, the star map would gain real ^weight. [act:the third test][tune:fall]Or an impact layer of the right age that even its critics ^accept.",
          "[d:calm][go:62|1.4][act:looking ahead, warm]And the spade isn't finished: about nine-tenths of the hill is still ^unexcavated. [act:fresh news, intrigued][tune:fall]Surveys@noun in {2025|twenty twenty-five} and {2026|twenty twenty-six} already report more buildings beyond the ^dig."]),
        B('close', 63, ["[d:tension][p:0.93][act:quiet, full of promise][tune:level]Somewhere under that hill, more stone giants may still be ^standing. [act:hushed, the last words][tune:fall]Weigh it ^yourself."]),
    ]


# ================================================================ cold open
HILL1 = [(-20, 720), (100, 690), (369, 600), (600, 566), (889, 550), (1180, 566), (1409, 600), (1680, 690), (1800, 720)]
R1 = (889, 640, 520, 60, 170)         # the ring on the hill: centre, radii, ring pillar height (20 m across: 52 units a metre)


def s01(C):
    """Dusk on a bare limestone ridge: a ring of T-shaped giants rises from the hilltop, the two central pillars last (5.5 m beside a 1.7 m person)."""
    cx, cy, rx, ry, h = R1
    ring_els, _ = enclosure(cx, cy, rx, ry, h, .5, step=.12, hc=286)
    return {"base": "sky", "tod": "dusk", "ground": 700, "sun": [1450, 470, 26], "cam": CAM, "els": [
        hill(HILL1, "#3b2f26", "#8a6a48", 2, -1),
        oval(cx, cy, 600, 84, "rgba(150,120,88,.28)", at=-1)] + ring_els + [
        person(1110, 642, 88, 2.6, "#e8d6b8"), glow(cx, 560, 420, 2.2, .22, "lamp")]}


def s02_late(C):
    """Push in on a central pillar: an arm and two hands trace themselves on its side; a thin time bar runs back to 11,500 years ago."""
    sh, ar = "#8c7152", [[773, 434], [769, 500], [775, 534], [801, 548], [824, 552]]
    t = C.at(1, "Carved")
    return [line([[p[0] + 2, p[1] + 3] for p in ar], t, sh, 12, curve=True, dur=1.0, op=.6), line(ar, t, RELIEF, 8, curve=True, dur=1.0),
            oval(828, 552, 8, 10, RELIEF, sh, 1, at=round(t + .9, 2), fx="pop"), glow(805, 520, 70, round(t + .9, 2), .5),
            line([[640, 262], [330, 262]], round(t + .6, 2), BONE, 2.5, dur=1.4), line([[640, 252], [640, 272]], round(t + .4, 2), BONE, 2, draw=False),
            label(640, 240, "today", round(t + .4, 2), MUTED, 24),
            line([[330, 248], [330, 276]], C.at(1, "thousand"), GOLD, 4, draw=False), dot(330, 262, 7, GOLD, C.at(1, "thousand")),
            label(330, 232, "c. 11,500 years ago", C.at(1, "thousand"), GOLD, 26, "start")]


def s03_late(C):
    """What they lacked, struck out as each is named: a clay pot, a copper axe, a marked tablet, a sheep; then a gold question mark."""
    out = []
    for (x, word), make in zip(((800, "pottery"), (1000, "metal"), (1200, "writing"), (1400, "farm animals")), (pot, axe, tablet, None)):
        t = C.at(2, word)
        out += make(x, 190, 100, t) if make else sheep(x - 10, 228, 100, t)
        out.append(strike(x - 46, 236, x + 46, 146, round(t + .45, 2)))
    return out + question(889, 330, C.at(2, "So who"), 120, GOLD)


def s04(C):
    """The two bold claims: a grand city on an Ice Age coast, dotted, its survivors walking to the hill; night falls; a comet streaks
    across and one pillar in the north-west of the ring glows, linked to it by a dotted line."""
    cx, cy, rx, ry, h = 1230, 600, 330, 45, 120
    top = [(40, 800), (120, 730), (210, 704), (520, 700), (700, 640), (950, 572), (1230, 535), (1500, 560), (1700, 610), (1800, 640)]
    ring_els, where = enclosure(cx, cy, rx, ry, h, -1, step=0, hc=200, c="#cdb48e", back_c="#a8916c")
    nx, nby, nh = where[P43]
    tc, tf, tn, tco = C.at(3, "survivors"), C.at(3, "lost civilisation"), C.at(3, "Others"), C.at(3, "comet strike")
    return {"base": "sky", "tod": "dusk", "ground": 700, "sun": False, "cam": CAM, "els": [
        {"k": "water", "y": 712, "x0": -40, "x1": 600, "h": 400, "op": .85, "in": -1, "layer": "far"},
        hill(top, "#3b2f26", "#8a6a48", 2, -1, layer="far"),
        rect(-40, -40, 1860, 1080, "#070912", at=tn, op=.55, dur=1.2, layer="far"),
        stars(90, 0, 1778, 40, 520, round(tn + .5, 2), 11, "far")] + ring_els + \
        city(200, 700, tc, LILAC, .85) + [label(370, 420, "lost civilisation?", round(tf + .4, 2), LILAC, 30)] + \
        [arrow([[530, 690], [700, 650], [900, 600]], round(tf - .2, 2), LILAC, 3, "claimed", 1.2)] + \
        [dict(person(560 + 80 * j, 694 - 18 * j, 56, round(tf + .3 * j, 2), LILAC), op=.6, keepop=True) for j in range(3)] + [
        glow(nx, nby - nh * .55, 90, C.at(3, "one pillar"), .85, "lamp"),
        line([[1730, 120], [1400, 300]], tco, "#ffe2a8", 5, dur=.6), line([[1745, 140], [1412, 306]], tco, "#ffcf8a", 2, dur=.6, op=.6),
        glow(1400, 300, 70, round(tco + .5, 2), .9, "fire"),
        line([[1392, 306], [nx + 4, nby - nh - 10]], round(tco + .5, 2), LILAC, 3, "claimed", .7), label(1560, 330, "a comet?", round(tco + .3, 2), LILAC, 30)]}


def s05(C):
    """The title's ground: the hill and its ring as silhouettes in the last light."""
    cx, cy, rx, ry, h = R1
    ring_els, _ = enclosure(cx, cy, rx, ry, h, -1, step=0, hc=286, c="#1d1714", back_c="#1d1714", edge="rgba(255,226,190,.22)", wall_c="#1d1714")
    return {"base": "sky", "tod": "dusk", "ground": 700, "sun": [1290, 600, 30], "cam": CAM, "els": [
        hill(HILL1, "#1a1411", "rgba(255,226,190,.3)", 1.5, -1)] + ring_els + [glow(1290, 600, 260, .2, .35, "sun")]}


# ================================================================ chapter 1: giants on Potbelly Hill
def s06(C):
    """Map of Turkey: Göbekli Tepe near Şanlıurfa; a square on the pin opens onto the hill's profile (s07: Potbelly Hill, 300 m across,
    15 m high, drawn five times taller), with a 100 m bar and a tiny person on the summit."""
    v = View(26, 46, 33, 43, (70, 140, 1000, 620))
    gx, gy = v.p(38.922, 37.223)
    tp = C.at(5, "Potbelly")
    mound = [(1195, 500), (1240, 478), (1300, 440), (1360, 408), (1405, 396), (1450, 408), (1510, 440), (1570, 478), (1615, 500)]
    return {"base": "map", "cam": CAM, "els": [
        {"k": "map", "land": v.land(), "in": -1},
        label(*v.p(33.2, 39.4), "Turkey", .3, "#d8c7ae", 36, st="ital"),
        {"k": "pin", "x": gx, "y": gy, "c": GOLD, "in": .5},
        label(gx - 24, gy + 10, "Göbekli Tepe", .6, GOLD, 32, "end"), label(gx - 24, gy + 44, "near Şanlıurfa", .8, MUTED, 26, "end"),
        rect(gx - 17, gy - 17, 34, 34, "none", GOLD, 2, 3, 1.0, fx="draw", dur=.4),
        line([[gx + 17, gy - 17], [1110, 230]], 1.2, BONE, 1.5, "inferred", .5, op=.6), line([[gx + 17, gy + 17], [1110, 600]], 1.2, BONE, 1.5, "inferred", .5, op=.6),
        rect(1110, 230, 590, 370, "rgba(16,12,9,.92)", GOLD, 1.5, 10, 1.3),
        poly([(1112, 500), (1698, 500), (1698, 598), (1112, 598)], "#5a4836", at=1.5),
        poly(mound + [(1615, 502), (1195, 502)], "#8a7258", "#e0c9a2", 2, round(tp - .2, 2), curve=False),
        line([[1112, 500], [1698, 500]], 1.5, "#e0c9a2", 2, draw=False),
        label(1405, 360, "Potbelly Hill", tp, GOLD, 34, st="ital"),
        person(1405, 396, 12, round(tp + .5, 2), "#fff2d8"),
        {"k": "scale", "x": 1140, "y": 576, "w": 140, "t": "100 m", "in": round(tp + .6, 2)},
        label(1684, 584, "height × 5", round(tp + .8, 2), MUTED, 24, "end")]}


S8 = [(-20, 610), (300, 575), (650, 525), (1000, 480), (1350, 450), (1800, 430)]


def sy8(x):
    for (xa, ya), (xb, yb) in zip(S8, S8[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / (xb - xa)
    return S8[-1][1]


def s08(C):
    """The hill's slope in section, by day: broken limestone slabs on the surface; in 1963 two surveyors walk past and take them for
    gravestones (a dotted guess, struck through)."""
    ts, tg, tb = C.at(7, "surveyors"), C.at(7, "gravestones"), C.at(7, "broken slabs")
    slabs = []
    for j, (x, w, h, a) in enumerate(((850, 96, 0, 0), (935, 30, 50, -12), (1010, 76, 0, 0), (1085, 32, 58, 9), (1225, 28, 44, -7), (1300, 84, 0, 0))):
        y, t = sy8(x), round(tb + .12 * j, 2)
        if h:
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            P_ = lambda u, v: (x + u * ca - v * sa, y + 4 + u * sa + v * ca)
            slabs.append(poly([P_(-w / 2, 0), P_(w / 2, 0), P_(w / 2, -h * .8), P_(w / 4, -h), P_(-w / 6, -h * .86), P_(-w / 2, -h * .95)], "#a8a49a", "#e8e4dc", 1.5, t, "rise"))
        else:
            slabs.append(poly([(x - w / 2, y - 6), (x + w / 2 - 8, y - 12), (x + w / 2, y + 2), (x - w / 2 + 8, y + 9)], "#a8a49a", "#e8e4dc", 1.5, t, "pop"))
    return {"base": "sky", "tod": "day", "ground": 1000, "sun": [1520, 200, 28], "cam": [1.2, 850, 470],
            "ridges": [{"y": 430, "a": 60, "c": "#8d97a8", "seed": 3}, {"y": 470, "a": 40, "c": "#7d8696", "seed": 9}], "els": [
        hill(S8, "#6e5a44", "#c9ad85", 2, -1),
        line([[x, y + 90] for x, y in S8], -1, "#8a7258", 1.5, "inferred", draw=False, op=.5),
        line([[x, y + 200] for x, y in S8], -1, "#8a7258", 1.5, "inferred", draw=False, op=.4),
        poly([(1105, 456), (1225, 452), (1229, 470), (1101, 474)], "#b9b4aa", "#f2efe8", 1.5, round(tb + .3, 2), "pop"),
        label(365, 420, "1963", .4, MUTED, 30)] + slabs + [
        person(330, round(sy8(330)), 120, ts, "#e8d6b8"), person(405, round(sy8(405)), 116, round(ts + .3, 2), "#e8d6b8"),
        rect(416, 500, 18, 24, BONE, "#8c7152", 1, 2, round(ts + .6, 2)),
        rect(1100, 322, 220, 52, "none", LILAC, 2, 8, tg, style="claimed"), label(1210, 358, "gravestones?", tg, LILAC, 32),
        line([[1106, 348], [1314, 348]], round(tg + 1.6, 2), RED, 3, dur=.5)]}


def s09_late(C):
    """1994: Klaus Schmidt walks up the slope among glittering flint; one slab is ringed in gold, and below it a buried T-pillar
    completes itself (dashed, inferred); beside it, the T-pillar type he knew from Nevalı Çori."""
    tf, tr, tt, ti = C.at(8, "Klaus Schmidt"), C.at(8, "recognised"), C.at(8, "T-shaped pillar"), C.at(8, "like those")
    flakes = [dot(round(x, 1), round(sy8(x) + 3, 1), 4, "#efe9df", round(tf + .9 + .07 * j, 2)) for j, x in enumerate((840, 868, 952, 978, 1040, 1062, 1118))]
    return [label(890, 330, "1994", .5, MUTED, 30), arrow([[640, 540], [740, 520], [850, 502]], round(tf - .3, 2), BONE, 2, "inferred", .8),
            person(890, round(sy8(890)), 120, tf, "#f0dcb8")] + flakes + [glow(950, 490, 90, round(tf + 1.0, 2), .5),
            {"k": "line", "p": R(ellipse(1165, 464, 84, 22, 40)), "c": GOLD, "w": 3, "curve": True, "in": tr, "fx": "draw", "dur": .8}, glow(1165, 464, 120, tr, .55),
            tpill(1150, 730, 272, tt, 1, 62, "none", GOLD, None, None, "inferred", 3),
            rect(1430, 262, 230, 250, "rgba(16,12,9,.88)", GOLD, 1.5, 10, ti), tpill(1530, 490, 190, round(ti + .3, 2), 1, 40),
            label(1545, 552, "Nevalı Çori type", round(ti + .5, 2), GOLD, 26)]


def s10(C):
    """Out of the hill: the top layer of the mound lifts away and four round enclosures appear, lettered as they appear (20 m bar)."""
    t0 = C.at(9, "Out of the hill")
    t1 = C.at(9, "great round enclosures")
    out = [{"k": "line", "p": R(ellipse(889, 560, 800, 230, 60)), "c": BONE, "w": 2, "style": "inferred", "op": .5, "keepop": True, "curve": True, "in": .3},
           label(300, 566, "the mound", .5, MUTED, 26, "start"),
           poly([(330, 270), (520, 205), (889, 178), (1258, 205), (1448, 270), (1258, 300), (889, 315), (520, 300)], "rgba(201,173,133,.08)", BONE, 2, t0, "rise",
                curve=True, style="inferred"),
           arrow([[889, 400], [889, 326]], round(t0 + .3, 2), BONE, 3, dur=.4, curve=False)]
    for j, (L, cx, cy, rx, ry) in enumerate((("A", 603, 451, 132, 59), ("B", 955, 421, 154, 69), ("C", 647, 619, 220, 99), ("D", 1175, 600, 220, 99))):
        t = round(t1 + .45 * j, 2)
        els, _ = enclosure(cx, cy, rx, ry, 77 * min(1, rx / 180), t, step=.04, n=8, hc=121 * min(1, rx / 180), sunk=True)
        out += els + [label(cx - rx - 22, cy + 12, L, round(t + .2, 2), GOLD, 34, "end", st="serif")]
    out.append({"k": "scale", "x": 955, "y": 760, "w": 440, "t": "20 m", "in": C.at(9, "twenty metres")})
    return {"base": "dark", "stars": 40, "cam": CAM, "els": out}


ENC_D = (889, 470, 300, 270)          # Enclosure D in plan (30 units a metre)


def plan_d(cx, cy, rx, ry, t0, step=.1, s=1.0, glow43=None, labels=True, at_c=None):
    """Enclosure D from above: the rubble ring wall, eleven pillars set in it with their narrow faces to the centre (P43 in the
    north-west), low benches between them, and the two central pillars."""
    def bar(x, y, a, L, W, at, fill="#cdb48e"):
        ca, sa = math.cos(a), math.sin(a)
        return poly([(x + ca * dl - sa * dw, y + sa * dl + ca * dw) for dl, dw in ((-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2), (-L / 2, W / 2))], fill, STONE_E, 1.5 * s, at, "pop")
    angs = [A0 + 2 * math.pi * k / 11 for k in range(11)]
    out = [{"k": "line", "p": R(ellipse(cx, cy, rx, ry, 72)), "c": "#9c8466", "w": 44 * s, "curve": True, "in": t0, "fx": "draw", "dur": 1.2},
           {"k": "line", "p": R(ellipse(cx, cy, rx + 22 * s, ry + 22 * s, 72)), "c": BONE, "w": 1.2, "curve": True, "op": .45, "keepop": True, "in": round(t0 + .6, 2)},
           {"k": "line", "p": R(ellipse(cx, cy, rx - 22 * s, ry - 22 * s, 72)), "c": BONE, "w": 1.2, "curve": True, "op": .45, "keepop": True, "in": round(t0 + .6, 2)}]
    tp = t0 + 1.0 if at_c is None else at_c[0]
    pos = []
    for k, a in enumerate(angs):
        x, y = cx + (rx - 8 * s) * math.cos(a), cy + (ry - 8 * s) * math.sin(a)
        pos.append((round(x, 1), round(y, 1)))
        out.append(bar(x, y, a, 70 * s, 22 * s, round(tp + step * k, 2)))
    tb = round(tp + step * 11 + .2, 2)
    for k, a in enumerate(angs):
        b = a + 2 * math.pi / 11
        arc = [(cx + (rx - 62 * s) * math.cos(u), cy + (ry - 62 * s) * math.sin(u)) for u in [a + .14 + (b - a - .28) * j / 6 for j in range(7)]]
        out.append({"k": "line", "p": R(arc), "c": "#b39b7a", "w": 12 * s, "op": .8, "keepop": True, "curve": True, "in": tb})
    tc = round(tb + .6, 2) if at_c is None else at_c[1]
    out += [bar(cx - 38 * s, cy, math.pi / 2, 110 * s, 26 * s, tc, STONE), bar(cx + 38 * s, cy, math.pi / 2, 110 * s, 26 * s, round(tc + .15, 2), STONE),
            glow(cx, cy, 150 * s, round(tc + .3, 2), .45)]
    return out, pos


def s11(C):
    """Enclosure D from above: the rubble ring wall draws itself, eleven pillars pop into it facing inwards, low benches between them,
    then the two central pillars with a soft glow (5 m bar, north up)."""
    cx, cy, rx, ry = ENC_D
    els, _ = plan_d(cx, cy, rx, ry, .4, .1, at_c=(C.at(10, "pillars set"), C.at(10, "two taller pillars")))
    return {"base": "plan", "cam": CAM, "els": els + [label(330, 482, "Enclosure D", round(C.at(10, "two taller pillars") + .9, 2), GOLD, 34, st="serif"),
                                                       {"k": "scale", "x": 1300, "y": 740, "w": 150, "t": "5 m", "in": 1.0}]}


P18 = (760, 762, 600, 130)            # the central pillar on its broad face: x, base, height (5.5 m: 109 units a metre), shaft width


def s12(C):
    """A central pillar of Enclosure D, 5.5 m on its bedrock pedestal (its partner behind), and three 1.8 m grown-ups stacked beside it."""
    x, by, h, w = P18
    tp = C.at(11, "three grown-ups")
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [
        line([[90, 776], [1690, 776]], -1, "#8a6a48", 2, draw=False), rect(610, 762, 300, 16, "#6b5a48", "#a08566", 1.2, 3, .2),
        tpill(470, by, h, .5, 1, w, "#8f7a5e", "#bfa98a", "rise", .55), tpill(x, by, h, .3, 1, w),
        rect(x + w / 2 - 14, by - h * .76, 14, h * .76, "#000", at=.3, op=.16), label(1450, 182, "Enclosure D", C.at(11, "Enclosure D"), GOLD, 34, "start", st="serif")] + \
        [person(1060, by - 196 * j, 196, round(tp + .45 * j, 2), "#e8d6b8", "pop") for j in range(3)] + [
        dimline(1230, by, 1230, by - h, "5.5 m", C.at(11, "five and a half"), GOLD, lx=34, dur=1.2)]}


def s13_late(C):
    """Pillar 18 up close: an arm bent at the elbow, two hands over the belly, a belt, a loincloth hanging from it, and a fox under the arm."""
    sh = "#8c7152"
    arm = [[712, 320], [710, 400], [716, 468], [760, 490], [812, 500]]
    ta, th, tb, tl, tf = C.at(12, "An arm"), C.at(12, "Two hands"), C.at(12, "A belt"), C.at(12, "loincloth"), C.at(12, "a fox")
    lead = lambda x0, y0, x1, y1, t: line([[x0, y0], [x1, y1]], t, BONE, 1.5, draw=False, op=.6)
    return [line([[p[0] + 3, p[1] + 4] for p in arm], ta, sh, 20, curve=True, dur=1.0, op=.55), line(arm, ta, RELIEF, 15, curve=True, dur=1.0),
            label(668, 404, "arm", round(ta + .7, 2), BONE, 30, "end"), lead(674, 395, 700, 395, round(ta + .7, 2)),
            oval(818, 500, 12, 16, RELIEF, sh, 1.2, at=th, fx="pop")] + \
           [line([[806, 488 + 7 * j], [826, 489 + 7 * j]], round(th + .1, 2), sh, 2, draw=False) for j in range(4)] + [glow(815, 500, 70, th, .55),
            label(872, 508, "hands", round(th + .3, 2), BONE, 30, "start"), lead(866, 500, 836, 500, round(th + .3, 2)),
            rect(695, 540, 130, 22, "#b89a78", RELIEF, 2, 3, tb, "pop"), label(872, 560, "belt", round(tb + .2, 2), BONE, 30, "start"),
            poly([(782, 562), (824, 562), (826, 600), (816, 640), (802, 668), (790, 640), (784, 600)], "#d8c3a0", RELIEF, 2, tl, "pop", curve=True),
            label(872, 640, "loincloth", round(tl + .3, 2), BONE, 30, "start"), lead(866, 632, 828, 616, round(tl + .3, 2)),
            beast(FOX, 768, 440, 68, tf, RELIEF, 1, "fade", edge=sh, w=1.5), glow(768, 424, 60, tf, .5),
            label(872, 430, "fox", round(tf + .3, 2), BONE, 30, "start"), lead(866, 422, 812, 424, round(tf + .3, 2))]


def s14_late(C):
    """Head and body: dashed boxes on the top of the T and its shaft; a faint human figure settles over the pillar."""
    x, by, h, w = P18
    th, tb, tf = C.at(13, "head"), C.at(13, "body"), C.at(13, "figures")
    return [rect(650, 150, 285, 165, "none", GOLD, 3, 18, th, style="inferred"), label(955, 246, "head", round(th + .2, 2), GOLD, 34, "start"),
            rect(683, 318, 154, 452, "none", GOLD, 3, 18, tb, style="inferred"), label(664, 724, "body", round(tb + .2, 2), GOLD, 34, "end"),
            {"k": "lib", "k2": "person", "x": x, "y": by, "h": h, "color": BONE, "op": .2, "keepop": True, "in": tf, "dur": 1.6}, glow(x, 430, 330, tf, .25)]


def s15(C):
    """A zoo in relief: the share of each animal among the carvings, bar by bar (Peters & Schmidt 2004); vultures and scorpions too."""
    x0, k = 430, 32
    rows = [("snakes", "snake", 250, 28), ("foxes", "fox", 360, 15), ("boars", "boar", 470, 9), ("cranes", "crane", 580, 6)]
    out = [label(x0, 172, "carved animals", .4, AMBER, 34, "start"), label(1690, 772, "Peters & Schmidt 2004", 1.0, MUTED, 24, "end")]
    for word, name, y, pct in rows:
        t = C.at(14, word)
        if name == "snake":
            icon = snake(330, y - 18, 100, t, MUTED, 7)
        elif name == "fox":
            icon = [beast(FOX, 340, y + 10, 92, t, MUTED, fx="pop")]
        elif name == "boar":
            icon = [beast(BOAR, 335, y + 12, 96, t, MUTED, fx="pop")]
        else:
            icon = [beast(CRANE, 330, y + 38, 66, t, MUTED, fx="pop")]
        out += icon + [label(250, y + 8, name, t, BONE, 28, "end"),
                       {"k": "line", "p": [[x0, y - 10], [x0 + pct * k, y - 10]], "c": AMBER, "w": 40, "op": .9, "keepop": True, "fx": "draw", "dur": .7, "in": round(t + .1, 2)},
                       label(x0 + pct * k + 34, y, "%d%%" % pct, round(t + .7, 2), BONE, 30, "start")]
    tv, tsc = C.at(14, "vultures"), C.at(14, "scorpions")
    out += [beast(VULT, 330, 728, 72, tv, MUTED, fx="pop"), label(250, 700, "vulture", tv, BONE, 28, "end")]
    out += scorpion(640, 688, 70, tsc, MUTED) + [label(700, 700, "scorpion", tsc, BONE, 28, "start")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": out}


def s16(C):
    """The quarry next door: a T outlined in chalk on the bedrock; workers cut a channel round it with flint picks; the slab is levered
    up along a natural seam, probably with wooden beams and wedges (dashed)."""
    X = lambda u, v: round(140 + 80 * v + u * (1500 - 160 * v), 1)
    Y = lambda v: round(470 - 200 * v, 1)
    T = [(.36, .30), (.43, .30), (.43, .42), (.66, .42), (.66, .58), (.43, .58), (.43, .70), (.36, .70)]
    TT = [(.352, .27), (.438, .27), (.438, .39), (.668, .39), (.668, .61), (.438, .61), (.438, .73), (.352, .73)]
    pt = lambda q, dy=0: [[X(u, v), round(Y(v) + dy, 1)] for u, v in q]
    tw, tc, tl, tn, tb = C.at(15, "Workers"), C.at(15, "channel"), C.at(15, "levered"), C.at(15, "natural seam"), C.at(15, "wooden beams")
    workers = [(.30, .45), (.72, .62), (.53, .82)]
    out = [poly([(140, 470), (1640, 470), (1560, 270), (220, 270)], "#d8c09a", STONE_E, 1.5, -1),
           rect(140, 470, 1500, 90, "#c9ae86", at=-1), rect(140, 560, 1500, 90, "#b0956f", at=-1), rect(140, 650, 1500, 160, "#9c8262", at=-1),
           line([[140, 560], [1640, 560]], -1, "#4a3a2c", 3, draw=False), line([[140, 650], [1640, 650]], -1, "#6b5640", 1.5, "inferred", draw=False),
           line(pt(T + T[:1]), C.at(15, "stone giant"), "#ffffff", 3, dur=1.2),
           line(pt(TT + TT[:1]), tc, INK, 10, dur=2.0)]
    for j, (u, v) in enumerate(workers):
        hh = round(120 * (1 - .25 * v))
        x, y = X(u, v), Y(v)
        out += [person(x, y, hh, round(tw + .25 * j, 2), "#e8d6b8"),
                line([[x + hh * .1, y - hh * .62], [x + hh * .34, y - hh * .3]], round(tc - .2 + .2 * j, 2), "#8a6a44", 4, draw=False),
                tri(round(x + hh * .36, 1), round(y - hh * .28, 1), 8, 200, "#6f7680", round(tc - .2 + .2 * j, 2))]
    out += [dot(round(X(u, v) + dx, 1), round(Y(v) - 10 - dy, 1), 3.5, "#f2dcb4", round(tc + .4 + .12 * j, 2))
            for j, ((u, v), dx, dy) in enumerate(zip(TT * 2, (8, -10, 12, -6, 4, 10, -8, 6, -4, 12), (6, 14, 4, 18, 10, 8, 16, 4, 12, 6)))]
    out += [label(X(.72, .62) + 70, Y(.62) - 30, "flint picks", C.at(15, "flint picks"), BONE, 26, "start"),
            poly(pt(T), INK, at=tl), poly(pt(T, -10), "#e6d3ae", "#fff3dc", 1.5, round(tl + .1, 2), "rise"),
            label(160, 548, "natural seam", tn, BONE, 26, "start"), line([[300, 556], [330, 560]], tn, BONE, 1.5, draw=False, op=.6)]
    out += [line([[X(.30, .36), Y(.36) + 26], [X(.40, .42), Y(.42) - 2]], tb, "#c48a5a", 5, "inferred", .5),
            line([[X(.74, .52) + 30, Y(.52) + 20], [X(.66, .50), Y(.50) - 4]], round(tb + .2, 2), "#c48a5a", 5, "inferred", .5)] + \
           [poly([(X(u, .42) - 8, Y(.42) + 2), (X(u, .42) + 8, Y(.42) + 2), (X(u, .42), Y(.42) - 10)], "none", "#c48a5a", 2, round(tb + .4 + .15 * j, 2), style="inferred")
            for j, u in enumerate((.48, .54, .60))] + \
           [label(X(.30, .36) - 10, Y(.36) + 60, "beams, wedges?", round(tb + .5, 2), MUTED, 26, "end")]
    return {"base": "sky", "tod": "day", "ground": 760, "sun": [1520, 170, 26], "cam": CAM, "els": out}


def s17(C):
    """The pillar that never left: 7 m long and 1.5 m thick in its bedrock bed (about 50 tonnes), beside a 5.5 m standing pillar and a
    1.7 m person, to one scale (90 units a metre); a crack runs across it, a pick drops and a worker sits down."""
    tc, te = C.at(16, "a crack"), C.at(16, "Even Stone Age")
    return {"base": "section", "tod": "dusk", "ground": 640, "layers": [{"d": 0, "c": "#bfa57c", "t": ""}, {"d": 90, "c": "#a88f6a", "t": ""}, {"d": 170, "c": "#8f7758", "t": ""}],
            "cam": CAM, "els": [
        rect(160, 640, 20, 136, "#241b14", at=.2), rect(810, 640, 20, 136, "#241b14", at=.2),
        rect(180, 640, 630, 135, STONE, STONE_E, 1.5, 2, .3), rect(180, 640, 110, 135, "#cdb48e", at=.3),
        dimline(180, 604, 810, 604, "7 m", C.at(16, "seven metres"), GOLD, dur=1.0),
        dimline(856, 640, 856, 775, "1.5 m", round(C.at(16, "seven metres") + .8, 2), GOLD, lx=30, dur=.6),
        label(495, 540, "c. 50 tonnes", C.at(16, "fifty tonnes"), AMBER, 34),
        tpill(1250, 640, 495, 1.0, -1, 100), person(1520, 640, 153, 1.3, "#e8d6b8"),
        dimline(1400, 640, 1400, 145, "5.5 m", round(C.at(16, "fifty tonnes") + .7, 2), MUTED, lx=30, dur=1.0),
        line([[470, 640], [482, 668], [466, 690], [486, 718], [470, 745], [488, 775]], tc, RED, 3, dur=.8),
        line([[886, 634], [966, 628]], te, "#8a6a44", 6, draw=False), tri(880, 634, 11, 180, "#6f7680", te),
        poly([(978, 574), (998, 574), (1002, 612), (1026, 614), (1030, 640), (1016, 640), (1012, 626), (976, 626), (970, 606)], "#e8d6b8", at=C.at(16, "bad days"), fx="pop"),
        dot(988, 560, 11, "#e8d6b8", C.at(16, "bad days"))]}


def s18(C):
    """A kitchen bin: a rubbish pit fills with bones layer by layer; gazelle, wild cattle and wild ass rise as they are named; a spear;
    a pen for herding appears dotted and is struck out."""
    bowl = [(220, 520), (260, 640), (360, 715), (490, 735), (620, 715), (720, 640), (760, 520)]
    tb = C.at(17, "kitchen bin")
    r = random.Random(8)
    out = [line(bowl, tb, BONE, 2.5, curve=True, dur=.8, op=.8), label(490, 498, "rubbish pit", round(tb + .4, 2), BONE, 28)]
    for j, (y0, y1, c) in enumerate(((680, 735, "#6b5440"), (615, 680, "#7a6248"), (545, 615, "#8a7258"))):
        t = round(tb + .7 + .55 * j, 2)
        band = bandpoly(bowl, y0, y1)
        out.append(poly(band, c, "none", 0, t, "fill", dur=.6))
        xs = [p[0] for p in band]
        for q in range(7):
            yy = r.uniform(y0 + 10, y1 - 8)
            lim = [p[0] for p in bandpoly(bowl, yy, yy + 1, 1)]
            xx = r.uniform(lim[0] + 18, lim[-1] - 18)
            out.append(line([[round(xx - 9, 1), round(yy, 1)], [round(xx + 9, 1), round(yy - 3, 1)]], round(t + .3 + .04 * q, 2), "#efe6d2", 4, draw=False))
    for name, word, pts, x, s in (("gazelle", "gazelle", GAZ, 950, 120), ("wild cattle", "wild cattle", AUR, 1225, 230), ("wild ass", "wild asses", ASS, 1500, 160)):
        t = C.at(17, word)
        out += [beast(pts, x, 520, s, t, "#d8c7ae"), label(x, 572, name, round(t + .2, 2), BONE, 28)]
    th, tn = C.at(17, "hunted"), C.at(17, "not herded")
    out += [line([[1690, 505], [1640, 250]], th, "#8a6a44", 5, draw=False), tri(1638, 238, 14, 190, "#a9a49b", th)]
    fence = [line([[1080 + 60 * j, 300], [1080 + 60 * j, 220]], tn, MUTED, 4, "claimed", draw=False) for j in range(5)] + \
            [line([[1066, 240], [1334, 240]], tn, MUTED, 4, "claimed", draw=False), line([[1066, 280], [1334, 280]], tn, MUTED, 4, "claimed", draw=False)]
    return {"base": "section", "tod": "dusk", "ground": 520, "layers": [{"d": 0, "c": "#7a6248", "t": ""}, {"d": 120, "c": "#5f4c39", "t": ""}], "cam": CAM,
            "els": out + fence + [label(1200, 200, "herded?", tn, MUTED, 26), strike(1060, 316, 1340, 196, round(tn + .6, 2))]}


def s19(C):
    """The textbook order (farming, then monuments) dims; here the order runs the other way: the giants first, farm animals and crops
    later. Below, the time axis: Göbekli Tepe from c. 9500 BCE, fully domesticated crops and herds after it."""
    X = lambda Y_: round(300 + (10000 - Y_) / 3000 * 1200, 1)
    tf, tm, tw, tg, tl = C.at(18, "farming first"), C.at(18, "then monuments"), C.at(18, "the other way"), C.at(18, "The giants"), C.at(18, "Farm animals")
    return {"base": "dark", "stars": 40, "cam": CAM, "els": [
        label(300, 172, "the textbook order", .5, MUTED, 28, "start"), arrow([[300, 240], [1480, 240]], .3, BONE, 2.5, dur=1.0, curve=False)] +
        field(560, 240, 100, tf) + sheep(760, 266, 90, round(tf + .4, 2)) + [tpill(1200, 286, 96, tm, 1, 22)] + [
        rect(250, 140, 1290, 170, "#0d0b09", at=tw, op=.62),
        label(300, 392, "here", round(tw + .3, 2), GOLD, 30, "start"), arrow([[300, 460], [1480, 460]], round(tw + .3, 2), GOLD, 2.5, dur=1.0, curve=False),
        tpill(560, 506, 96, tg, 1, 22), glow(560, 460, 100, tg, .6)] +
        field(1000, 460, 100, tl) + sheep(1220, 486, 90, round(tl + .4, 2)) + [
        {"k": "axis", "x0": 300, "x1": 1500, "y": 650, "ticks": [[X(y), "{:,}".format(y)] for y in (10000, 9000, 8000, 7000)], "t": "BCE", "in": round(tg - .3, 2)},
        line([[X(9500), 650], [X(9500), 604]], tg, GOLD, 4, draw=False), dot(X(9500), 650, 8, GOLD, tg),
        label(X(9500), 592, "Göbekli Tepe, c. 9500 BCE", round(tg + .2, 2), GOLD, 26),
        {"k": "line", "p": [[X(8500), 618], [X(7000), 618]], "c": GREEN, "w": 16, "op": .85, "keepop": True, "fx": "draw", "dur": 1.0, "in": C.at(18, "came later")},
        label(1200, 600, "fully domesticated crops, herds", round(C.at(18, "came later") + .3, 2), GREEN, 26)]}


# ================================================================ chapter 2: dating a hill of rubble
def s20(C):
    """How do you date a stone? Not directly: a limestone block and a question; a seed, a bone and a charcoal twig, once alive, ticked.
    Their radiocarbon fades at a steady pace (three of twelve dots at a time) while a candle burns down in step; a ruler measures the stub."""
    ta = C.at(19, "once alive")
    tc, tf, tm = C.at(19, "radioactive carbon"), C.at(19, "fades after death"), C.at(19, "measure")
    tw = "#3a2c22"
    out = [{"k": "block", "x": 170, "y": 620, "w": 210, "h": 160, "in": .3}] + question(300, 380, .5, 90, LILAC)
    for j, (x, name) in enumerate(((560, "seed"), (700, "bone"), (840, "charcoal"))):
        t = round(ta + .3 * j, 2)
        if name == "seed":
            out.append(oval(x, 430, 22, 34, "#8a5a32", "#d8a56a", 2, at=t, fx="pop"))
        elif name == "bone":
            out += [line([[x - 40, 430], [x + 40, 430]], t, "#efe6d2", 14, draw=False)] + [dot(x + dx, 430 + dy, 10, "#efe6d2", t) for dx in (-42, 42) for dy in (-8, 8)]
        else:
            out += [line([[x - 46, 446], [x + 40, 418]], t, "#2a221c", 12, draw=False), line([[x, 432], [x + 22, 404]], t, "#2a221c", 8, draw=False)]
        out += [label(x, 500, name, t, MUTED, 26), tick(x, 352, round(t + .3, 2))]
    out += [rect(1000, 170, 650, 590, CARD, "#5a4836", 1.5, 18, round(tc - .6, 2)),
            line([[1060, 646], [1330, 606]], round(tc - .3, 2), tw, 34, draw=False), line([[1220, 622], [1270, 660]], round(tc - .3, 2), tw, 20, draw=False)]
    dots = [(1080 + 21 * j, round(643 - 3.0 * j + (6 if j % 2 else -6), 1)) for j in range(12)]
    out += [dot(x, y, 6, BLUE, round(tc + .04 * j, 2)) for j, (x, y) in enumerate(dots)] + [label(1195, 580, "carbon", round(tc + .3, 2), BLUE, 28)]
    top = [280 + 105 * k for k in range(4)]
    flame = lambda y, t: [poly([(1520, y - 42), (1531, y - 15), (1520, y - 5), (1509, y - 15)], "#ffd27a", at=t, curve=True), glow(1520, y - 22, 46, t, .9)]
    out += [rect(1460, 700, 120, 12, "#8c7152", at=tf), rect(1490, 280, 60, 420, "#efe6d2", "#fff6e6", 1.5, 6, tf)] + flame(280, tf)
    for k in range(1, 4):
        t = round(tf + .5 + 1.3 * k, 2)
        out += [rect(1440, top[k - 1] - 75, 160, top[k] - top[k - 1] + 75, CARD, at=t, dur=.3)] + flame(top[k], round(t + .05, 2))
        out += [dot(x, y, 7.5, tw, t) for x, y in dots[(k - 1) * 3:k * 3]]
    out += [rect(1566, 595, 18, 105, "#e8c35a", "#fff3dc", 1, 3, tm, "pop")] + [line([[1566, 600 + 20 * j], [1576, 600 + 20 * j]], tm, INK, 1.5, draw=False) for j in range(5)] + \
           [label(1576, 742, "what's left", round(tm + .3, 2), BONE, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": out}


def s21(C):
    """A sunken enclosure in section, its two pillars standing in a fill of rubble, bone and flint; stones slide in from the slope above."""
    r = random.Random(21)
    out = [poly([(-20, 332)] + smooth([(-20, 200), (120, 180), (260, 210), (420, 300), (480, 330)]), "#7a6248", "#c9a878", 2, -1),
           rect(480, 330, 820, 392, "#241b14", at=-1), rect(480, 330, 60, 392, "url(#k-blocks)", at=-1), rect(1240, 330, 60, 392, "url(#k-blocks)", at=-1),
           rect(545, 420, 690, 300, "#5a4734", at=.6, fx="fill", dur=.8)]
    tr, tb, tf = C.at(20, "rubble"), C.at(20, "bone"), C.at(20, "flint")
    for j in range(46):
        x, y = r.uniform(560, 1220), r.uniform(436, 708)
        s = r.uniform(9, 16)
        out.append(poly([(x - s, y - s * .5), (x + s * .3, y - s * .8), (x + s, y), (x + s * .2, y + s * .7), (x - s * .8, y + s * .5)], r.choice(("#8f8a80", "#7d766c", "#a39c90")),
                        "#3a332c", 1, round(tr - .9 + .02 * j, 2), "pop"))
    for j in range(14):
        x, y = r.uniform(570, 1210), r.uniform(440, 705)
        a = r.uniform(0, math.pi)
        out.append(line([[round(x - 12 * math.cos(a), 1), round(y - 12 * math.sin(a), 1)], [round(x + 12 * math.cos(a), 1), round(y + 12 * math.sin(a), 1)]],
                        round(tb - .2 + .03 * j, 2), "#efe6d2", 5, draw=False))
    for j in range(14):
        out.append(tri(round(r.uniform(570, 1210), 1), round(r.uniform(445, 705), 1), 8, r.uniform(0, 120), "#2c2a30", round(tf - .2 + .03 * j, 2)))
    out += [tpill(700, 720, 340, .3, 1, 60), tpill(1080, 720, 340, .4, -1, 60),
            label(1330, 488, "rubble", tr, BONE, 28, "start"), label(1330, 568, "bone", tb, "#efe6d2", 28, "start"), label(1330, 648, "flint", tf, MUTED, 28, "start")]
    tm = C.at(20, "rubble moves")
    out += [arrow([[150, 196], [330, 250], [500, 350], [610, 430]], tm, AMBER, 3.5, dur=1.0)] + \
           [poly([(x - 9, y - 4), (x + 4, y - 9), (x + 10, y + 2), (x - 3, y + 8)], "#a39c90", "#3a332c", 1, round(tm + .1 + .08 * j, 2), "pop")
            for j, (x, y) in enumerate(((210, 228), (300, 252), (390, 290), (470, 330), (540, 376)))]
    return {"base": "section", "tod": "dusk", "ground": 330, "layers": [{"d": 0, "c": "#7a6248", "t": ""}, {"d": 160, "c": "#5f4c39", "t": ""}, {"d": 330, "c": "#4a3b2e", "t": ""}],
            "cam": CAM, "els": out}


def s22(C):
    """Like dating a house from the junk in its cellar: the house was built in 1950; an old clock (1890) is older, a phone (2015) newer."""
    th, tj, to, tn = C.at(21, "a house"), C.at(21, "the junk"), C.at(21, "older"), C.at(21, "newer")
    return {"base": "section", "tod": "day", "ground": 540, "layers": [{"d": 0, "c": "#6f5a44", "t": ""}, {"d": 240, "c": "#5a4836", "t": ""}], "cam": CAM, "els": [
        rect(640, 300, 500, 240, "#3a2f26", BONE, 2, 2, th, "rise"), poly([(610, 302), (890, 172), (1170, 302)], "#8e7152", "#e0c9a2", 2, th, "rise"),
        rect(700, 360, 70, 60, "#1e1712", "#a08566", 1.5, 2, th, "rise"), rect(1010, 360, 70, 60, "#1e1712", "#a08566", 1.5, 2, th, "rise"),
        rect(866, 440, 48, 100, "#241b14", "#a08566", 1.5, 2, th, "rise"),
        rect(800, 470, 180, 44, CARD, GOLD, 1.5, 6, round(th + .5, 2)), label(890, 502, "built 1950", round(th + .5, 2), GOLD, 28),
        rect(660, 545, 460, 215, "#1c1510", "#a08566", 1.5, 2, round(tj - .4, 2)),
        rect(728, 690, 64, 70, "#6b4a2e", "#c9a878", 1.5, 4, tj, "rise"), {"k": "circle", "x": 760, "y": 712, "r": 18, "fill": "#efe6d2", "c": "#3a2c20", "w": 2, "in": tj, "fx": "rise"},
        line([[760, 712], [760, 700], [770, 712]], tj, INK, 2, draw=False),
        rect(850, 716, 70, 44, "#8a7258", "#c9ad85", 1.2, 2, round(tj + .2, 2), "rise"), rect(930, 730, 50, 30, "#7a6248", "#c9ad85", 1.2, 2, round(tj + .3, 2), "rise"),
        rect(1000, 700, 34, 60, "#2a2f36", "#cbd2d8", 2, 6, round(tj + .4, 2), "rise"), rect(1005, 707, 24, 40, "#4f93b3", at=round(tj + .4, 2), fx="rise"),
        label(760, 672, "1890", to, AMBER, 28), label(600, 668, "older", round(to + .3, 2), AMBER, 28, "end"),
        arrow([[606, 676], [650, 690], [712, 700]], round(to + .3, 2), AMBER, 2.5, dur=.5),
        label(1017, 682, "2015", tn, BLUE, 28), label(1180, 668, "newer", round(tn + .1, 2), BLUE, 28, "start"),
        arrow([[1174, 676], [1120, 690], [1048, 704]], round(tn + .1, 2), BLUE, 2.5, dur=.4)]}


def s23(C):
    """Upside down: in a column of layers, a younger sample lies below an older one."""
    ty, to = C.at(22, "younger"), C.at(22, "older ones")
    cols = ["#7a6248", "#8a7258", "#6b5440", "#9c8466", "#5f4c39", "#7d644a"]
    out = [rect(770, 170 + 100 * j, 240, 100, c, at=round(.3 + .08 * j, 2), fx="fill", dur=.4) for j, c in enumerate(cols)]
    out += [line([[770, 170 + 100 * j], [1010, 170 + 100 * j]], .9, "rgba(255,226,190,.25)", 1.2, "inferred", draw=False) for j in range(1, 6)]
    out += [arrow([[700, 200], [700, 740]], .6, MUTED, 2, dur=.8, curve=False), label(684, 470, "deeper", .8, MUTED, 26, "end"),
            dot(890, 640, 13, BLUE, ty), glow(890, 640, 70, ty, .8), label(1040, 650, "younger", ty, BLUE, 32, "start"),
            dot(890, 330, 13, AMBER, to), glow(890, 330, 70, to, .8), label(1040, 340, "older", to, AMBER, 32, "start"),
            arrow([[1020, 610], [1110, 490], [1020, 360]], round(to + .4, 2), BONE, 2.5, dur=.7), label(1140, 500, "upside down", round(to + .8, 2), BONE, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": out}


AX24 = lambda Y_: round(200 + (10500 - Y_) / 3000 * 1380, 1)       # the time axis of s24/s25: 10,500 to 7,500 BCE


def s24(C):
    """Plaster smears onto an enclosure wall (left to right); a flake lifts out as a sample and goes down onto the time axis, where its
    date fills in: 9745 to 9314 BCE (Dietrich & Schmidt 2010, 95% range)."""
    r = random.Random(24)
    tp, tf, ta, tr = C.at(23, "plaster and mortar"), C.at(23, "while the buildings"), C.at(23, "Plaster from"), C.at(23, "between about")
    wall = []
    for row in range(5):
        x = 300 - (row % 2) * 40
        while x < 1480:
            w = r.uniform(70, 130)
            x1 = min(1480, x + w)
            if x1 - max(300, x) > 20:
                wall.append(rect(max(300, x) + 2, 152 + 36 * row, x1 - max(300, x) - 4, 32, r.choice(("#8f7556", "#a08566", "#7a6248", "#94795a")), "#3a2c20", 1, 4, -1))
            x = x1
    X = AX24
    return {"base": "dark", "stars": 20, "cam": CAM, "els": wall + [
        label(889, 136, "enclosure wall", .4, MUTED, 24),
        {"k": "line", "p": [[360, 242], [1420, 242]], "c": "rgba(236,226,206,.5)", "w": 120, "fx": "draw", "dur": 1.6, "in": tp},
        label(1500, 250, "plaster", round(tp + 1.0, 2), BONE, 28, "start"),
        poly([(886, 236), (912, 232), (918, 252), (890, 256)], "#fff3dc", "#ffffff", 1, tf, "rise"), glow(900, 244, 60, tf, .9),
        arrow([[900, 290], [760, 420], [650, 548]], round(tf + .6, 2), "#fff3dc", 2, "inferred", .9),
        {"k": "axis", "x0": 200, "x1": 1580, "y": 620, "ticks": [[X(y), "{:,}".format(y)] for y in range(10500, 7499, -500)], "t": "BCE", "in": ta},
        {"k": "line", "p": [[X(9745), 575], [X(9314), 575]], "c": AMBER, "w": 20, "op": .95, "keepop": True, "fx": "draw", "dur": .8, "in": tr},
        label(530, 584, "plaster, Enclosure D", round(tr + .6, 2), AMBER, 26, "end")]}


def s25_late(C):
    """The whole site on the same axis: in use from about 9500 to 8000 BCE (1,500 years); round buildings early, rectangular ones later,
    overlapping in the middle; one round building remodelled as a rectangle (Clare 2020)."""
    X = AX24
    tb, tc, tr, tre = C.at(24, "nine and a half thousand"), C.at(24, "fifteen centuries"), C.at(24, "repairing"), C.at(24, "rebuilding")
    tbu = C.at(24, "building")
    out = [{"k": "line", "p": [[X(9500), 472], [X(8000), 472]], "c": GOLD, "w": 16, "op": .9, "keepop": True, "fx": "draw", "dur": 1.8, "in": tb},
           label(1005, 448, "Göbekli Tepe in use", round(tb + .6, 2), GOLD, 28), label(1372, 480, "1,500 years", tc, BONE, 28, "start")]
    out += [{"k": "circle", "x": x, "y": 395, "r": 14, "fill": "none", "c": BONE, "w": 3, "in": round(tbu + .08 * j, 2), "fx": "pop"} for j, x in enumerate((690, 760, 830, 900, 970))]
    out += [rect(x - 14, 384, 28, 22, "none", BONE, 3, 2, round(tr + .08 * j, 2), "pop") for j, x in enumerate((935, 1005, 1075, 1145, 1215, 1285))]
    out += [{"k": "circle", "x": 1420, "y": 395, "r": 14, "fill": "none", "c": GOLD, "w": 3, "in": tre, "fx": "pop"},
            arrow([[1444, 395], [1480, 395]], round(tre + .2, 2), GOLD, 2, dur=.3, curve=False), rect(1494, 384, 28, 22, "none", GOLD, 3, 2, round(tre + .5, 2), "pop")]
    return out


def s26(C):
    """The old story, drawn as a claim: people tip baskets of rubble into an enclosure and it fills fast; 'ritual burial?'; then a
    dotted padlock settles over the mound (the popular claim that it was buried to hide it)."""
    cx, cy, rx, ry = 889, 540, 380, 110
    ring_els, _ = enclosure(cx, cy, rx, ry, 140, .3, step=.06, hc=215, sunk=True)
    tp, tr, th = C.at(25, "people buried"), C.at(25, "A ritual"), C.at(25, "to hide it")
    figs = [(cx - rx - 50, cy + 14), (cx + rx + 50, cy + 14), (cx - 210, cy + ry + 40), (cx + 230, cy + ry + 40)]
    out = list(ring_els)
    for j, (x, y) in enumerate(figs):
        t = round(tp + .15 * j, 2)
        out += [dict(person(x, y, 74, t, LILAC), op=.7, keepop=True), oval(x + (18 if x < cx else -18), y - 52, 16, 10, "#8a7258", LILAC, 1.5, at=t, fx="pop")]
        out += [dot(round(x + (30 if x < cx else -30) + 8 * q * (1 if x < cx else -1), 1), y - 40 + 9 * q, 4, "#a39c90", round(t + .3 + .08 * q, 2)) for q in range(3)]
    mound = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [math.pi - math.pi * j / 12 for j in range(13)]] + \
            [(cx + rx * .6, cy - ry - 70), (cx, cy - ry - 110), (cx - rx * .6, cy - ry - 70)]
    out += [poly(mound, "rgba(110,92,72,.92)", LILAC, 2.5, round(tp + .3, 2), "fill", curve=True, dur=2.0, style="claimed"),
            rect(180, 150, 1420, 640, "none", LILAC, 3, 20, tr, style="claimed"), label(889, 206, "ritual burial?", round(tr + .2, 2), LILAC, 34)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": out + padlock(889, 360, 100, th) + [glow(889, 340, 160, th, .35, "lamp")]}


def s27(C):
    """The excavators' own records: a stack of field notebooks; the top one opens and turns into a section of the slope (knolls above,
    the sunken enclosure below); a tongue of debris slides down and pours in, older (brown) and younger (grey) mixed."""
    tr, ts = C.at(26, "records"), C.at(26, "In twenty twenty")
    tsl, tmx = C.at(26, "slid in"), C.at(26, "older and younger")
    out = [rect(120, 700 - 34 * (j + 1), 260, 30, c, "#e0c9a2", 1.5, 4, round(.4 + .12 * j, 2), "pop") for j, c in enumerate(("#6b4a2e", "#5a6a4a", "#7a5a3a", "#4a5a6a"))]
    out += [poly([(130, 540), (250, 556), (250, 470), (130, 452)], "#f3ead8", "#8a6a3e", 1.5, tr, "pop"), poly([(250, 556), (370, 540), (370, 452), (250, 470)], "#efe2c8", "#8a6a3e", 1.5, tr, "pop")]
    out += [line([[150 + 0 * j, 480 + 14 * j], [235, 494 + 14 * j]], round(tr + .2, 2), "#8a6a3e", 1.5, draw=False, op=.7) for j in range(4)]
    out += [poly([(268, 490), (300, 474), (330, 486), (352, 476)], "none", "#8a6a3e", 1.5, round(tr + .2, 2))]
    ground = [(480, 330), (620, 270), (760, 300), (900, 360), (1100, 470), (1150, 520), (1550, 520), (1700, 540)]
    out += [rect(470, 170, 1230, 590, CARD, "#5a4836", 1.5, 16, ts), arrow([[380, 470], [430, 400], [480, 360]], round(ts + .2, 2), BONE, 2, "inferred", .5),
            poly(ground + [(1698, 758), (472, 758)], "#4a3b2e", "#c9ad85", 2, round(ts + .4, 2)),
            rect(1160, 520, 380, 200, "#1e1712", at=round(ts + .6, 2)), tpill(1250, 720, 180, round(ts + .8, 2), 1, 34), tpill(1450, 720, 180, round(ts + .9, 2), -1, 34),
            label(700, 240, "higher knolls", C.at(26, "higher ground"), MUTED, 26),
            arrow([[640, 300], [880, 380], [1060, 470], [1190, 560]], tsl, AMBER, 3.5, dur=1.0), arrow([[760, 320], [960, 420], [1120, 500], [1260, 590]], round(tsl + .3, 2), GREY, 3, dur=1.0),
            rect(1162, 600, 376, 120, "#4e3e2e", at=round(tsl + .8, 2), fx="fill", dur=1.0)]
    r = random.Random(27)
    for j in range(30):
        x, y = r.uniform(1180, 1520), r.uniform(612, 708)
        out.append(oval(round(x, 1), round(y, 1), round(r.uniform(9, 15), 1), round(r.uniform(6, 9), 1), "#a0683e" if j % 2 else "#a8a39a", at=round(tmx - .4 + .04 * j, 2), fx="pop"))
    out += [label(1580, 620, "older", tmx, "#d39a68", 28, "start"), label(1580, 664, "younger", round(tmx + .4, 2), "#cfcac2", 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": out}


BACK28 = "#2a2119"


def s28(C):
    """Slope slides: rain, then a shake; a pillar is pushed off true (a few degrees); people build a terrace wall upslope and set a prop
    against the pillar, which steadies (Kinzel, Clare & Sönmez 2020)."""
    ts, tr, te, td = C.at(27, "Slope slides"), C.at(27, "heavy rain"), C.at(27, "earthquakes"), C.at(27, "damaged")
    tp, tt, trp = C.at(27, "shored them up"), C.at(27, "terrace walls"), C.at(27, "repairs")
    T = [(972, 740), (1028, 740), (1028, 565), (1070, 565), (1070, 510), (965, 510), (965, 565), (972, 565)]
    r = random.Random(28)
    out = [poly(smooth([(-20, 330), (200, 318), (420, 380), (560, 462), (600, 470)]) + [(600, 1010), (-20, 1010)], "#4a3b2e", "#c9ad85", 2, -1),
           poly([(1400, 470), (1800, 470), (1800, 1010), (1400, 1010)], "#4a3b2e", "#c9ad85", 2, -1),
           rect(600, 470, 800, 270, BACK28, at=-1), rect(600, 740, 800, 270, "#3a2e24", "#c9ad85", 2, 0, -1),
           rect(600, 470, 40, 270, "url(#k-blocks)", at=-1), rect(1360, 470, 40, 270, "url(#k-blocks)", at=-1),
           poly(T, STONE, STONE_E, 1.6, -1),
           arrow([[160, 300], [330, 340], [520, 440]], ts, AMBER, 3, dur=.9)]
    out += [line([[round(x, 1), round(y, 1)], [round(x - 10, 1), round(y + 26, 1)]], round(tr + .02 * j, 2), BLUE, 2, draw=False, op=.5)
            for j, (x, y) in enumerate(scatter(56, 100, 1700, 150, 440, 9))]
    out += [line([[880 + 18 * j, 760 - (10 if j % 2 else 0)] for j in range(6)], te, RED, 3, dur=.4), line([[1140 + 18 * j, 760 - (10 if j % 2 else 0)] for j in range(6)], te, RED, 3, dur=.4),
            line([[470 + 14 * j, 410 - (8 if j % 2 else 0)] for j in range(5)], round(te + .2, 2), RED, 3, dur=.4)]
    out += [poly(T, BACK28, BACK28, 5, td, dur=.35), {"k": "group", "tr": "rotate(5 1000 740)", "in": td, "dur": .35, "els": [poly(T, STONE, STONE_E, 1.6, -1)]},
            line([[1000, 742], [1000, 490]], round(td + .3, 2), BONE, 1.5, "inferred", draw=False, op=.6),
            arrow([[1006, 500], [1018, 498], [1030, 502]], round(td + .4, 2), RED, 2.5, dur=.3)]
    out += [person(300, 322, 90, tp, "#e8d6b8"), person(250, 320, 84, round(tp + .2, 2), "#e8d6b8")]
    out += [rect(390 + 16 * (j % 4) - 6 * (j // 4), 400 - 18 * (j // 4), 18, 16, "#a39c90", "#3a332c", 1, 2, round(tt + .1 * j, 2), "rise") for j in range(10)]
    out += [label(340, 476, "terrace wall", round(tt + .9, 2), BONE, 26),
            poly([(1100, 740), (1140, 740), (1068, 600), (1048, 612)], "#a39c90", "#e8e4dc", 1.5, trp, "rise"), glow(1010, 600, 150, round(trp + .5, 2), .4, "lamp")]
    return {"base": "sky", "tod": "night", "ground": 1000, "sun": False, "cam": CAM, "els": out}


def s29(C):
    """Karahan Tepe, a sister site to the east (two pins and a thread, no distance written: published figures differ); one of its
    buildings in section: filled in three stages and capped with big flat stones, one of them 2.65 by 1.65 m (Karul 2021)."""
    v = View(38.55, 39.65, 36.85, 37.45, (110, 180, 680, 540))
    g, k, s = v.p(38.922, 37.223), v.p(39.304, 37.093), v.p(38.795, 37.159)
    tk, te, tf, ts, tc, ti = C.at(28, "Karahan Tepe"), C.at(28, "to the east"), C.at(28, "describes fill"), C.at(28, "by stages"), C.at(28, "capped"), C.at(28, "intentional")
    out = [rect(110, 218, 680, 465, "rgba(58,47,36,.55)", MUTED, 1.5, 8, .2),
           {"k": "line", "p": [[180, 300], [300, 280], [420, 330], [520, 300], [700, 360]], "c": MUTED, "w": 1.2, "op": .35, "keepop": True, "curve": True, "in": .3},
           {"k": "line", "p": [[160, 560], [320, 520], [470, 560], [620, 520], [760, 580]], "c": MUTED, "w": 1.2, "op": .35, "keepop": True, "curve": True, "in": .3},
           rect(s[0] - 6, s[1] - 6, 12, 12, MUTED, at=.4), label(s[0] - 14, s[1] + 34, "Şanlıurfa", .5, MUTED, 24, "end"),
           {"k": "pin", "x": g[0], "y": g[1], "c": GOLD, "in": .5}, label(g[0] + 20, g[1] - 16, "Göbekli Tepe", .6, GOLD, 28, "start"),
           {"k": "pin", "x": k[0], "y": k[1], "c": AMBER, "in": tk}, label(k[0] - 22, k[1] + 40, "Karahan Tepe", round(tk + .2, 2), AMBER, 28, "end"),
           line([list(g), list(k)], te, AMBER, 3, dur=.8),
           rect(880, 160, 820, 600, "#18120e", "#5a4836", 1.5, 16, round(tf - .6, 2)), label(1290, 214, "a Karahan Tepe building", round(tf - .4, 2), GOLD, 28),
           rect(900, 300, 780, 440, "#8c7152", at=round(tf - .3, 2)), rect(1040, 300, 500, 420, "#1e1712", at=round(tf - .3, 2)),
           line([[900, 300], [1680, 300]], round(tf - .3, 2), "#e0c9a2", 2, draw=False)]
    for j, (y, c) in enumerate(((640, "#6b5440"), (560, "#7d644a"), (480, "#8f7556"))):
        t = round(ts + .55 * j, 2)
        out += [rect(1040, y, 500, 80, c, at=t, fx="fill", dur=.5), label(1520, y + 50, str(j + 1), round(t + .3, 2), BONE, 26, "end")]
    for j, x in enumerate((1045, 1210, 1375)):
        out.append(rect(x, 448, 160, 30, "#cdb48e", "#fff3dc", 1.5, 3, round(tc + .2 * j, 2), "pop"))
    out += [label(1290, 432, "2.65 × 1.65 m", round(tc + .8, 2), BONE, 28), glow(1290, 462, 200, ti, .45, "lamp")]
    return {"base": "plan", "north": [740, 270], "cam": CAM, "els": out}


def hands_pan(x, y, at):
    return [poly([(x - 34, y), (x + 34, y), (x + 42, y - 44), (x - 42, y - 44)], "#8a6a44", "#d8b98a", 1.5, at, "pop"),
            line([[x - 38, y - 22], [x + 38, y - 22]], at, "#d8b98a", 1.5, draw=False),
            oval(x + 2, y - 70, 17, 15, "#e8d6b8", at=at, fx="pop"), line([[x - 14, y - 72], [x - 28, y - 88]], at, "#e8d6b8", 7, draw=False)] + \
           [line([[x - 9 + 7 * j, y - 80], [x - 10 + 8 * j, y - 104 + (4 if j in (0, 3) else 0)]], at, "#e8d6b8", 7, draw=False) for j in range(4)] + \
           [line([[x + 2, y - 56], [x + 2, y - 44]], at, "#e8d6b8", 14, draw=False)]


def slope_pan(x, y, at):
    return [poly([(x - 60, y), (x + 60, y), (x + 60, y - 70)], "#7a6248", "#c9ad85", 1.5, at, "pop")] + \
           [dot(x + dx, y - dy, 7, "#a39c90", at) for dx, dy in ((14, 34), (-10, 16), (34, 50))] + [arrow([[x + 44, y - 70], [x - 30, y - 20]], at, AMBER, 2, dur=.3)]


def s30(C):
    """Hands or hillside? A balance: a basket and a hand on one pan, a slope with sliding stones on the other; at Göbekli the beam tips
    gently towards the hillside and stops short of the floor (not settled)."""
    th, ts, tg, tf = C.at(29, "hands"), C.at(29, "hillside"), C.at(29, "At Göbekli"), C.at(29, "is now the favourite")
    bal = lambda ang, at, l, r_: balance(889, 300, 640, ang, 700, at, l, r_)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [rect(330, 150, 1120, 610, CARD, "#4a3a2c", 1.5, 18, .1)] + bal(0, .3, None, None) +
            hands_pan(569, 470, th) + slope_pan(1209, 470, ts) + [
            label(569, 650, "hands", th, BONE, 30), label(1209, 650, "hillside", ts, BONE, 30), label(889, 210, "Göbekli Tepe", tg, GOLD, 30),
            rect(420, 236, 940, 372, CARD, at=tf, dur=.5)] + bal(6, tf, hands_pan, slope_pan)}


# ================================================================ chapter 3: survivors of a lost world?
X31 = lambda ya: round(450 + (14000 - ya) / 5000 * 1200, 1)        # Hancock's timeline: 14,000 to 9,000 years ago


def s31(C):
    """The boldest idea: a book opens onto a timeline, 14,000 to 9,000 years ago (Hancock's timeline)."""
    tb, tt = C.at(30, "Graham Hancock"), C.at(30, "the timing")
    return {"base": "dark", "stars": 50, "cam": CAM, "els": [
        rect(150, 380, 200, 150, "#6b4a2e", "#c9a878", 2, 6, .3), line([[166, 380], [166, 530]], .3, "#c9a878", 2, draw=False),
        poly([(126, 372), (250, 388), (250, 540), (126, 524)], "#f3ead8", "#8a6a3e", 1.5, tb, "pop"), poly([(250, 388), (374, 372), (374, 524), (250, 540)], "#efe2c8", "#8a6a3e", 1.5, tb, "pop")] + \
        [line([[142, 404 + 18 * j], [236, 416 + 18 * j]], round(tb + .2, 2), "#8a6a3e", 1.5, draw=False, op=.6) for j in range(6)] + \
        [line([[264, 416 + 18 * j], [358, 404 + 18 * j]], round(tb + .2, 2), "#8a6a3e", 1.5, draw=False, op=.6) for j in range(6)] + [
        label(450, 190, "Hancock's timeline", round(tb + .4, 2), AMBER, 30, "start"),
        arrow([[380, 520], [420, 600], [446, 640]], round(tt - .2, 2), BONE, 2, "inferred", .5),
        {"k": "axis", "x0": 450, "x1": 1650, "y": 650, "ticks": [[X31(y), "{:,}".format(y)] for y in range(14000, 8999, -1000)], "t": "years ago", "in": tt}]}


def s32_late(C):
    """On the timeline, the thermometer of the past (the curve of the Short 'sky-fell'): about 12,900 years ago the warming world drops
    back into the cold for some 1,200 years, the Younger Dryas; soon after it ends, Göbekli Tepe (c. 11,500 years ago)."""
    from lg_c import _CA, _CB, _CC, _CD
    Y = lambda yp: round(270 + (yp - 756) / (1082 - 756) * 300, 1)
    C_ = lambda pts: [[X31(a), Y(b)] for a, b in pts]
    CA = [(14000, 811)] + [q for q in _CA if q[0] <= 13950]
    CD = list(_CD) + [(9500, 760), (9000, 758)]
    t0, tw, tl, tc = C.at(31, "About"), C.at(31, "the warming world"), C.at(31, "lurched back"), C.at(31, "the cold")
    ty, tce, ts, tg = C.at(31, "the Younger Dryas"), C.at(31, "twelve centuries"), C.at(31, "Soon after"), C.at(31, "Göbekli Tepe rises")
    x0, x1 = X31(12900), X31(11700)
    return [line([[x0, 650], [x0, 258]], t0, GOLD, 2, "inferred", .6), label(x0 - 14, 248, "12,900", round(t0 + .3, 2), GOLD, 28, "end"),
            arrow([[420, 590], [420, 280]], round(t0 + .5, 2), BONE, 2, dur=.5, curve=False),
            label(436, 292, "warmer", round(t0 + .6, 2), WARM, 26, "start"), label(436, 600, "colder", round(t0 + .6, 2), BLUE, 26, "start"),
            line(C_(CA), tw, AMBER, 5, dur=1.0), line(C_(_CB), tl, BLUE, 5, dur=.4), line(C_(_CC), tc, BLUE, 5, dur=1.2),
            rect(x0, 258, x1 - x0, 340, "rgba(159,208,255,.13)", at=ty, fx="fill", dur=.8),
            label((x0 + x1) / 2, 304, "Younger Dryas", round(ty + .3, 2), BLUE, 32), label((x0 + x1) / 2, 344, "1,200 years", tce, BONE, 26),
            line(C_(CD), ts, AMBER, 5, dur=1.0),
            tpill(X31(11500), 650, 54, tg, 1, 13, GOLD, "#fff3dc"), glow(X31(11500), 620, 70, tg, .7),
            label(X31(11500) + 26, 616, "Göbekli Tepe, c. 11,500 years ago", round(tg + .2, 2), GOLD, 26, "start")]


def s33(C):
    """The claim, all dotted: a city outline struck by a comet; its survivors walk to local hunters at their fire, beside whom a T-pillar
    rises (the hunters, the fire and the pillar are real; the city and its survivors are the claim)."""
    tt, tci, tco, tk, th = C.at(32, "Something this ambitious"), C.at(32, "lost Ice Age civilisation"), C.at(32, "ruined by a comet"), C.at(32, "passed their knowledge"), C.at(32, "local hunters")
    return {"base": "sky", "tod": "night", "ground": 700, "groundc": "#241d17", "sun": False, "cam": CAM, "els": [
        glow(1260, 680, 110, .4, .9, "fire"), poly([(1248, 696), (1260, 650), (1272, 696)], "#ffd27a", at=.4, curve=True)] +
        people(1130, 700, 2, 84, .5, "#e8d6b8", 56) + people(1330, 700, 2, 80, .6, "#e8d6b8", 56) + [
        tpill(1530, 700, 200, round(tt + .3, 2), -1, 40), label(1250, 560, "local hunters", round(tt + .8, 2), BONE, 28)] +
        city(180, 700, tci, LILAC, 1.0, .08) + [label(380, 430, "lost civilisation?", round(tci + .5, 2), LILAC, 30),
        line([[780, 150], [470, 470]], tco, LILAC, 4, "claimed", .6), glow(460, 480, 140, round(tco + .5, 2), .8, "blue"),
        arrow([[600, 690], [860, 700], [1090, 690]], round(tk - .3, 2), LILAC, 3, "claimed", 1.6)] + \
        [dict(person(650 + 110 * j, 700, 60, round(tk + .35 * j, 2), LILAC), op=.6, keepop=True) for j in range(3)] + [glow(1180, 640, 120, th, .5, "lamp")]}


def s34(C):
    """The Ice Age coast in section: houses on the old shore drawn as a claim (dotted); the sea climbs about 120 m and covers them."""
    surf = [(-20, 300), (250, 315), (480, 338), (560, 360), (760, 430), (980, 520), (1180, 600), (1300, 632), (1460, 648), (1600, 672), (1800, 700)]
    tc, th, ts = C.at(33, "Ice Age coasts"), C.at(33, "might have lived"), C.at(33, "now lie under")
    rise = [(486, 340)] + [p for p in surf if p[0] >= 560] + [(1800, 340)]
    homes = [rect(1170 + 38 * j, 600 + 6 * j - 34, 28, 30, "none", "#e6e0ff", 3, 2, round(th + .15 * j, 2), style="claimed") for j in range(4)] + \
            [poly([(1166 + 38 * j, 600 + 6 * j - 34), (1184 + 38 * j, 600 + 6 * j - 50), (1202 + 38 * j, 600 + 6 * j - 34)], "none", "#e6e0ff", 3, round(th + .15 * j, 2), style="claimed")
             for j in range(4)] + [label(1240, 520, "homes?", round(th + .6, 2), "#e6e0ff", 26)]
    return {"base": "sky", "tod": "dusk", "ground": 1000, "sun": [1420, 250, 26], "cam": CAM, "els": [
        {"k": "water", "y": 640, "x0": 1300, "x1": 1900, "h": 420, "op": .9, "in": -1},
        hill(surf, "#4a3b2e", "#c9ad85", 2, -1),
        line([[x, y + 70] for x, y in surf], -1, "#5f4c39", 1.5, "inferred", draw=False, op=.6),
        label(1330, 700, "Ice Age coast", tc, BONE, 28),
        poly(rise, "rgba(63,134,168,.62)", "#bfe6f5", 1.5, ts, "fill", dur=1.4)] + homes + [
        dimline(1690, 640, 1690, 340, "about 120 m", round(ts + .4, 2), GOLD, lx=-32, dur=1.0),
        line([[486, 340], [1660, 340]], round(ts + 1.0, 2), BONE, 2, "inferred", draw=False, op=.7), label(1000, 326, "sea level today", round(ts + 1.0, 2), BONE, 26)]}


TESTS = (("technique", 1000), ("tool", 1250), ("crop", 1500))


def s35(C):
    """The test: a visiting cook leaves traces in a kitchen, a new pan and a spice from far away (a dotted trail off to the edge);
    so we look for things with no local roots: three empty boxes, a technique, a tool, a crop."""
    tc, tp, ts, tf, tl = C.at(34, "master cook"), C.at(34, "a new pan"), C.at(34, "a spice"), C.at(34, "far away"), C.at(34, "So we'd look")
    out = [rect(100, 170, 800, 530, "#2b221a", "#5a4836", 1.5, 10, .2), line([[100, 700], [900, 700]], .2, "#8a6a48", 3, draw=False),
           rect(140, 330, 280, 14, "#6b5440", "#a08566", 1, 2, .3)] + pot(190, 300, 50, .4) + pot(270, 300, 44, .45) + pot(350, 302, 40, .5) + [
           rect(300, 560, 340, 20, "#6b5440", "#a08566", 1.2, 3, .3), rect(316, 580, 12, 120, "#5a4836", at=.3), rect(612, 580, 12, 120, "#5a4836", at=.3),
           arrow([[930, 640], [860, 640], [800, 640]], round(tc - .3, 2), BONE, 2, "inferred", .5, False), person(760, 700, 200, tc, "#e8d6b8"),
           rect(742, 482, 36, 22, "#f5ecdc", at=tc, fx="rise"),
           oval(430, 548, 46, 12, "#3b3632", "#cbd2d8", 2, at=tp, fx="pop"), line([[476, 548], [540, 540]], tp, "#3b3632", 6, draw=False),
           rect(548, 506, 30, 48, "#b0503a", "#ffb09a", 1.5, 6, ts, "pop"), rect(552, 498, 22, 10, "#8a6a44", at=ts, fx="pop"),
           {"k": "line", "p": [[560, 498], [470, 400], [300, 250], [96, 150]], "c": AMBER, "w": 3, "style": "claimed", "curve": True, "in": tf, "fx": "draw", "dur": 1.0},
           glow(100, 150, 60, round(tf + .8, 2), .8, "lamp"), label(150, 214, "far away", round(tf + .8, 2), AMBER, 26, "start"),
           label(1340, 270, "the test", tl, BLUE, 32)]
    for word, x in TESTS:
        t = C.at(34, "a " + word)
        out += [rect(x - 90, 330, 180, 180, "none", BLUE, 3, 10, t, style="inferred"), label(x, 560, word, round(t + .2, 2), BLUE, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": out}


def s36(C):
    """What the ground shows: limestone from the quarry next door, flint tools of the region's own kinds, the local animals on the
    hills, each ticked; the three test boxes stay empty in a corner."""
    tL, tT, tA = C.at(35, "Limestone"), C.at(35, "Tools"), C.at(35, "the animals")
    out = [poly([(140, 720), (1640, 720), (1500, 380), (280, 380)], "#6e5a44", "#a08566", 2, -1), rect(140, 720, 1500, 70, "#4a3b2e", at=-1),
           poly([(200, 384), (420, 300), (620, 340), (820, 290), (1040, 330), (1260, 286), (1460, 330), (1580, 384)], "#3b2f26", "#8a6a48", 1.5, -1, curve=True),
           poly([(300, 650), (470, 640), (500, 560), (330, 556)], "#cdb48e", "#f2dcb4", 1.5, .3)] + \
          [line([[320 + 30 * j, 640], [340 + 30 * j, 568]], .4, "#8c7152", 1.5, draw=False, op=.7) for j in range(5)]
    for cx, cy, rx, ry, h in ((850, 560, 150, 45, 50), (1150, 500, 120, 36, 40)):
        els, _ = enclosure(cx, cy, rx, ry, h, .5, step=.03, n=9, sunk=True)
        out += els
    out += [rect(1440 + 80 * j, 150, 60, 60, "none", BLUE, 2.5, 6, .8, style="inferred") for j in range(3)]
    out += [arrow([[480, 590], [600, 600], [700, 570]], tL, AMBER, 3, dur=.7), label(560, 660, "limestone", round(tL + .2, 2), BONE, 28), tick(660, 660, round(tL + .8, 2))]
    out += [poly([(1240, 640), (1400, 596), (1530, 640), (1490, 700), (1290, 706)], "none", BONE, 2, tT, curve=True, style="inferred")] + \
           [tri(round(1300 + 34 * (j % 4), 1), round(640 + 26 * (j // 4), 1), 11, 15 * j, "#cfc6b8", round(tT + .3 + .06 * j, 2)) for j in range(7)] + \
           [label(1390, 752, "regional tools", round(tT + .4, 2), BONE, 28), tick(1520, 752, round(tT + 1.2, 2))]
    out += [beast(FOX, 480, 330, 70, tA, "#d8c7ae"), beast(BOAR, 900, 304, 80, round(tA + .3, 2), "#d8c7ae"), beast(CRANE, 1240, 290, 52, round(tA + .6, 2), "#d8c7ae"),
            label(889, 230, "local animals", round(tA + .8, 2), BONE, 28), tick(1010, 230, round(tA + 1.4, 2))]
    return {"base": "sky", "tod": "dusk", "ground": 760, "groundc": "#2e251c", "sun": [1600, 300, 22], "cam": CAM, "els": out}


def s37(C):
    """Homes (Clare 2020): small round-oval houses packed wall to wall beside a larger round building; a hearth used again and again
    (three layers stacking in a small section); beads of stone and bone; a rectangular building."""
    th, thr, tg, tb = C.at(36, "Homes"), C.at(36, "Hearths"), C.at(36, "again and again"), C.at(36, "Beads")
    houses = [(420, 360, 70, 56), (545, 340, 62, 52), (470, 470, 66, 58), (600, 455, 60, 54), (360, 470, 52, 48), (530, 570, 64, 50), (660, 560, 54, 46)]
    out = [label(200, 200, "since 2015", C.at(36, "twenty fifteen"), GOLD, 30, "start"), rect(190, 250, 1040, 520, "none", MUTED, 2, 8, 1.0, style="inferred")]
    out += [oval(x, y, rx, ry, "#3a2f24", "#c9ad85", 8, at=round(th + .1 * j, 2), fx="pop") for j, (x, y, rx, ry) in enumerate(houses)]
    out += [{"k": "circle", "x": 950, "y": 420, "r": 130, "fill": "#3a2f24", "c": "#d8c09a", "w": 12, "in": round(th + .8, 2), "fx": "pop"},
            rect(915, 404, 18, 36, STONE, at=round(th + 1.0, 2)), rect(967, 404, 18, 36, STONE, at=round(th + 1.0, 2))]
    out += hearth(880, 660, thr, 1.2) + [label(880, 724, "hearth", round(thr + .3, 2), BONE, 26)]
    out += [rect(1230, 596, 300, 164, CARD, "#5a4836", 1.5, 10, round(tg - .3, 2)), label(1380, 744, "hearth layers", round(tg - .1, 2), MUTED, 24)]
    out += [rect(1260, 690 - 32 * j, 240, 12, "#5a2a1a", "#c8743c", 1.5, 3, round(tg + .35 * j, 2), "fill") for j in range(3)]
    out += [rect(1260, 702 - 32 * j, 240, 20, "#3a2f24", at=round(tg + .35 * j, 2)) for j in range(3)]
    out += [dot(round(560 + 22 * j, 1), round(700 + (8 if j % 2 else -8), 1), 7, "#9ab0a0" if j % 2 else "#efe6d2", round(tb + .06 * j, 2)) for j in range(8)]
    out += [label(640, 752, "beads", round(tb + .4, 2), BONE, 26),
            rect(1240, 300, 220, 150, "#3a2f24", "#d8c09a", 10, 4, round(tb + .8, 2), "pop")]
    return {"base": "plan", "cam": CAM, "els": out}


def s38_late(C):
    """A grave beneath one floor: under the rectangular building, a burial pit outline (dashed: below the floor) with three small lights
    for at least three people (no remains drawn)."""
    tg, t3 = C.at(37, "A grave"), C.at(37, "at least three")
    pit = [(1290, 380), (1330, 352), (1390, 356), (1420, 384), (1404, 412), (1360, 420), (1330, 404), (1296, 410)]
    return [{"k": "line", "p": R(pit + pit[:1]), "c": "#efe6d2", "w": 3, "style": "inferred", "curve": True, "in": tg}, label(1350, 486, "burial", round(tg + .6, 2), BONE, 28)] + \
           [g for j, (x, y) in enumerate(((1330, 384), (1358, 392), (1386, 380))) for g in (glow(x, y, 34, round(t3 + .3 * j, 2), .7, "lamp"), dot(x, y, 4, "#fff2d8", round(t3 + .3 * j, 2)))]


def s39(C):
    """No spring on the hill: the nearest springs lie on a circle 5 km round the site, to the north-east and south-east (Notroff 2017)."""
    cx, cy, R5 = 889, 460, 260
    tn, tc, tk = C.at(38, "no spring"), C.at(38, "the nearest"), C.at(38, "five kilometres")
    out = [{"k": "line", "p": R(ellipse(cx + dx, cy + dy, rx, ry, 30)), "c": MUTED, "w": 1.4, "op": .35, "keepop": True, "curve": True, "in": .3}
           for dx, dy, rx, ry in ((-20, 10, 340, 160), (-10, 0, 220, 100), (0, -6, 110, 50))]
    out += [{"k": "pin", "x": cx, "y": cy, "c": GOLD, "in": .4}, label(cx, cy - 36, "Göbekli Tepe", .6, GOLD, 30),
            poly([(cx + 40, cy + 30), (cx + 52, cy + 52), (cx + 40, cy + 62), (cx + 28, cy + 52)], BLUE, at=tn, curve=True), strike(cx + 20, cy + 70, cx + 60, cy + 24, round(tn + .3, 2), RED, 4),
            ring(cx, cy, R5, tc, BONE, 2.5, "known", 1.2)]
    for j, a in enumerate((-45, 45)):
        x, y = cx + R5 * math.cos(math.radians(a)), cy + R5 * math.sin(math.radians(a))
        out += [dot(round(x, 1), round(y, 1), 11, BLUE, round(tk + .2 * j, 2)), glow(round(x, 1), round(y, 1), 50, round(tk + .2 * j, 2), .7, "blue"),
                label(round(x + 24, 1), round(y + 9, 1), "spring", round(tk + .2 * j + .2, 2), BLUE, 28, "start")]
    out += [{"k": "scale", "x": 140, "y": 740, "w": R5, "t": "5 km", "in": round(tk + .4, 2)}]
    return {"base": "plan", "cam": CAM, "els": out}


def s40(C):
    """Rainwater: a channel cut in the rock surface runs into a rock-cut cistern, which fills (all the cisterns together: about 150
    cubic metres); then the same water as bathtubs, 19 icons of 100 baths each (153 cubic metres at 80 litres a bath: about 1,900)."""
    tc, tci, tf, tn, tb = C.at(39, "cut channels"), C.at(39, "feeding cisterns"), C.at(39, "together could hold"), C.at(39, "a hundred and fifty"), C.at(39, "Nearly two thousand")
    out = [line([[round(x, 1), round(y, 1)], [round(x - 8, 1), round(y + 22, 1)]], round(.4 + .02 * j, 2), BLUE, 2, draw=False, op=.5) for j, (x, y) in enumerate(scatter(30, 140, 560, 170, 330, 40))]
    out += [line([[120, 386], [580, 386]], tc, INK, 10, dur=1.2), line([[120, 380], [580, 380]], tc, "#e0c9a2", 1.5, dur=1.2),
            rect(580, 380, 320, 260, "#241b14", BONE, 2, 30, tci), label(740, 694, "150 cubic metres", tn, BLUE, 30),
            rect(588, 400, 304, 232, SEA, at=tf, op=.9, fx="fill", dur=2.2), glow(740, 520, 160, round(tf + 1.4, 2), .3, "blue")]
    out.append(rect(1010, 150, 680, 480, CARD, "#4a3a2c", 1.5, 16, round(tb - .4, 2)))
    for j in range(19):
        out += bathtub(1094 + 128 * (j % 5), 230 + 90 * (j // 5), 100, round(tb + .06 * j, 2))
    out += [label(1350, 600, "1 icon = 100 baths", round(tb + 1.2, 2), MUTED, 26)]
    return {"base": "section", "tod": "dusk", "ground": 380, "layers": [{"d": 0, "c": "#bfa57c", "t": ""}, {"d": 140, "c": "#a88f6a", "t": ""}, {"d": 280, "c": "#8f7758", "t": ""}],
            "cam": CAM, "els": out}


def s41(C):
    """More than 7,000 grinding tools (70 icons of 100); no big stores (an empty storeroom, struck); the food eaten fresh at work feasts;
    then the same crowd hauls a T-pillar on wooden rollers."""
    tg, ts, tfe, tcr, th = C.at(40, "seven thousand"), C.at(40, "no big stores"), C.at(40, "great work feasts"), C.at(40, "Feed a crowd"), C.at(40, "hauls your pillars")
    out = []
    for j in range(70):
        out += quern(150 + 50 * (j % 10), 180 + 44 * (j // 10), 100, round(.4 + .03 * j, 2))
    out += [label(375, 528, "7,000+", tg, AMBER, 44, st="serif"), label(375, 566, "1 icon = 100 tools", round(tg + .4, 2), MUTED, 24),
            rect(760, 250, 180, 150, "none", BONE, 3, 4, ts, style="claimed"), poly([(744, 254), (850, 196), (956, 254)], "none", BONE, 3, ts, style="claimed"),
            label(850, 446, "no big stores", round(ts + .3, 2), BONE, 26), strike(746, 416, 954, 190, round(ts + .7, 2))]
    out += hearth(1350, 410, tfe, 1.3) + [poly([(1338, 412), (1350, 360), (1362, 412)], "#ffd27a", at=tfe, curve=True)]
    out += [person(round(1350 + 170 * math.cos(a), 1), round(440 + 40 * math.sin(a), 1), 74, round(tfe + .08 * j, 2), "#e8d6b8")
            for j, a in enumerate([math.radians(200 + 20 * q) for q in range(8)])]
    out += [oval(1300 + 40 * j, 452, 12, 5, "#c8743c", at=round(tfe + .7, 2)) for j in range(3)]
    out += [person(520 + 64 * j, 748, 92, round(tcr + .1 * j, 2), "#e8d6b8") for j in range(10)]
    out += [line([[1150, 672], [560, 676]], th, "#c9a878", 3, dur=.8)]
    out += [{"k": "circle", "x": 1190 + 100 * j, "y": 734, "r": 14, "fill": "#8a6a44", "c": "#c9a878", "w": 2, "in": th, "fx": "pop"} for j in range(5)]
    out += [poly([(1150, 650), (1520, 650), (1520, 628), (1610, 628), (1610, 720), (1520, 720), (1520, 698), (1150, 698)], STONE, STONE_E, 1.6, th, "rise")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": out}


SH_VIEW = View(38.3, 40.0, 36.8, 37.6, (90, 140, 1600, 640))       # the Stone Hills around Şanlıurfa
OTHERS = [(38.55, 37.05), (38.70, 37.36), (38.98, 37.02), (39.12, 37.30), (39.20, 36.96), (39.46, 37.20), (39.58, 37.02), (39.72, 37.36), (38.84, 37.47), (39.36, 37.44)]


def s42(C):
    """The Stone Hills (Taş Tepeler): about a dozen sites with T-shaped pillars around Şanlıurfa; Göbekli Tepe and Karahan Tepe at their
    published positions, the others drawn at schematic places (noted on screen)."""
    v = SH_VIEW
    g, k, s = v.p(38.922, 37.223), v.p(39.304, 37.093), v.p(38.795, 37.159)
    tp, tt = C.at(41, "About a dozen"), C.at(41, "the Stone Hills")
    r = random.Random(42)
    out = [{"k": "line", "p": R([(x, y + r.uniform(-20, 20)) for x, y in [(360 + 120 * q, 200 + 70 * j + (30 if q % 2 else 0)) for q in range(10)]]), "c": MUTED, "w": 1.2,
            "op": .25, "keepop": True, "curve": True, "in": .2} for j in range(8)]
    out += [rect(s[0] - 7, s[1] - 7, 14, 14, MUTED, at=.4), label(s[0] - 16, s[1] + 34, "Şanlıurfa", .5, MUTED, 26, "end"),
            {"k": "pin", "x": g[0], "y": g[1], "c": GOLD, "in": .4}, label(g[0] - 20, g[1] - 20, "Göbekli Tepe", .6, GOLD, 30, "end")]
    for j, (lo, la) in enumerate(OTHERS):
        x, y = v.p(lo, la)
        out.append({"k": "pin", "x": x, "y": y, "c": AMBER, "r": 7, "in": round(tp + .12 * j, 2)})
    out += [{"k": "pin", "x": k[0], "y": k[1], "c": AMBER, "in": round(tp + .5, 2)}, label(k[0] + 20, k[1] + 40, "Karahan Tepe", round(tp + .7, 2), AMBER, 30, "start"),
            label(889, 196, "Taş Tepeler · the Stone Hills", tt, GOLD, 34, st="serif"),
            label(110, 772, "other sites: positions schematic", round(tt + .4, 2), MUTED, 24, "start"),
            {"k": "scale", "x": 1250, "y": 744, "w": round(v.km(20), 1), "t": "20 km", "in": 1.0}]
    return {"base": "plan", "cam": CAM, "els": out}


def s45_late(C):
    """No sign of a visiting cook: threads link the neighbours, a small figure at each site; the three test boxes, still empty."""
    v = SH_VIEW
    pts = [v.p(38.922, 37.223), v.p(39.304, 37.093)] + [v.p(lo, la) for lo, la in OTHERS]
    tb, tl, tn = C.at(44, "No sign"), C.at(44, "landscape"), C.at(44, "neighbours")
    links, seen = [], set()
    for i, (x, y) in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: (pts[j][0] - x) ** 2 + (pts[j][1] - y) ** 2)[1:3]
        for j in near:
            if (min(i, j), max(i, j)) not in seen:
                seen.add((min(i, j), max(i, j))); links.append((i, j))
    out = [rect(1470 + 76 * j, 640, 60, 60, "none", BLUE, 2.5, 6, round(tb + .2 * j, 2), style="inferred") for j in range(3)]
    out += [line([list(pts[i]), list(pts[j])], round(tl + .06 * q, 2), GREEN, 2.5, dur=.5, op=.85) for q, (i, j) in enumerate(links)]
    out += [person(round(x + 16, 1), round(y + 10, 1), 30, round(tn - .3 + .03 * q, 2), "#e8d6b8") for q, (x, y) in enumerate(pts)]
    return out


def s43(C):
    """Karahan Tepe, Structure AB (cutaway): a room about 7 x 6 m cut 3.5 m into the bedrock; ten pillars rise out of the living rock,
    and a human head looks on from the wall; a 1.7 m person at the rim (80 units a metre)."""
    tr, td, tp, th = C.at(42, "carved a room"), C.at(42, "three and a half"), C.at(42, "ten pillars"), C.at(42, "a human head")
    FL, FR, BR, BL = (600, 420), (1160, 420), (1340, 250), (780, 250)
    out = [poly([(300, 420), (1480, 420), (1660, 250), (480, 250)], "#a08566", "#e0c9a2", 1.5, -1), rect(300, 420, 1180, 340, "#8c7152", at=-1),
           line([[300, 520], [1480, 520]], -1, "#6b5640", 1.2, "inferred", draw=False), line([[300, 640], [1480, 640]], -1, "#6b5640", 1.2, "inferred", draw=False),
           label(300, 196, "Karahan Tepe", .5, GOLD, 32, "start", st="serif"), label(300, 232, "Structure AB", .7, MUTED, 26, "start"),
           poly([BL, BR, (1340, 530), (780, 530)], "#5e4a36", "#3a2c20", 1, tr), poly([FL, BL, (780, 530), (600, 700)], "#6e5842", "#3a2c20", 1, tr),
           poly([FR, BR, (1340, 530), (1160, 700)], "#7a6248", "#3a2c20", 1, tr), poly([(600, 700), (1160, 700), (1340, 530), (780, 530)], "#4e3e2e", "#3a2c20", 1, tr),
           person(1404, 420, 136, round(tr + .4, 2), "#e8d6b8"),
           dimline(1520, 420, 1520, 700, "3.5 m", td, GOLD, lx=30, dur=1.0)]
    k = 0
    for v in (.7, .35):
        for u in (.12, .31, .5, .69, .88):
            bx, by = 600 + 560 * u + 180 * v, 700 - 170 * v
            h = 150 - 30 * v
            out.append(rect(round(bx - 17, 1), round(by - h, 1), 34, h, "#b89c74", "#e0c9a2", 1.5, 17, round(tp + .14 * k, 2), "rise")); k += 1
    out += [oval(900, 330, 24, 32, "#c9ad85", "#efe0c0", 2, at=th, fx="pop"), dot(892, 322, 4, INK, round(th + .2, 2)), dot(908, 322, 4, INK, round(th + .2, 2)),
            line([[900, 326], [900, 342]], round(th + .2, 2), INK, 2, draw=False), glow(900, 330, 90, round(th + .3, 2), .6, "lamp")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": out}


def s44(C):
    """Sayburç: a relief along a bench about 3.7 m long, a man between two leopards, and further on a second man beside a bull
    (Özdoğan 2022), schematic."""
    tm, tl = C.at(43, "a man"), C.at(43, "two leopards")
    rel, ink = RELIEF, "#5a4632"
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [
        poly([(150, 400), (1650, 400), (1680, 380), (180, 380)], "#b39b7a", "#e0c9a2", 1.2, .3), rect(150, 400, 1500, 240, "#9c8466", "#e0c9a2", 1.2, 2, .3),
        label(889, 240, "Sayburç, 9th millennium BCE", .6, GOLD, 30), {"k": "scale", "x": 150, "y": 700, "w": 1500, "t": "about 3.7 m", "in": 1.0},
        {"k": "lib", "k2": "person", "x": 760, "y": 628, "h": 190, "color": rel, "in": tm, "fx": "rise"},
        beast(LEO, 540, 628, 300, tl, rel, 1, "rise", edge=ink, w=1.5), beast(LEO, 980, 628, 300, round(tl + .3, 2), rel, -1, "rise", edge=ink, w=1.5),
        {"k": "lib", "k2": "person", "x": 1290, "y": 628, "h": 170, "color": rel, "in": .8, "fx": "rise"},
        beast(AUR, 1500, 628, 240, 1.1, rel, -1, "rise", edge=ink, w=1.5)]}


# ================================================================ chapter 4: a comet on the Vulture Stone?
VS = {"vulture": (1040, 470), "disc": (900, 362), "birds": [(850, 568), (930, 616), (1220, 410)], "scorp": (950, 702), "man": (1180, 770)}


def s47(C):
    """Pillar 43, the Vulture Stone (schematic): beside it a small plan of Enclosure D with P43 glowing in the north-west (s46). Each
    carving draws itself as it is named: the vulture with a disc by its wing, smaller birds, a scorpion, a snake, three handled boxes
    along the top, and near the bottom a headless man (plain outline)."""
    tv, td, tb, ts, tsn, tbx, tm = C.at(46, "great vulture"), C.at(46, "a disc"), C.at(46, "Smaller birds"), C.at(46, "a scorpion"), C.at(46, "a snake"), C.at(46, "Three boxes"), C.at(46, "a man without")
    loc, pos = plan_d(290, 400, 150, 135, -1, 0, s=.5, at_c=(-1, -1))
    for e in loc:
        e["in"] = -1
    px, py = pos[P43]
    rel, ink = "#cdb48e", INK
    vx, vy = VS["vulture"]
    out = loc + [glow(px, py, 60, .2, .9, "lamp"), ring(px, py, 22, .2, GOLD, 3), label(px - 28, py - 22, "P43", .3, GOLD, 28, "end"), label(290, 590, "Enclosure D", -1, MUTED, 26),
                 line([[px + 20, py - 6], [700, 230]], .5, GOLD, 1.5, "inferred", .6, op=.7),
                 rect(700, 150, 650, 150, "#7d6a52", STONE_E, 2, 6, .3), rect(760, 300, 530, 520, "#7d6a52", STONE_E, 2, 0, .3),
                 label(1380, 204, "Pillar 43", .6, BONE, 30, "start"), label(1380, 240, "schematic", .8, MUTED, 24, "start"),
                 oval(vx, vy, 46, 72, rel, ink, 2, at=tv, fx="pop"), oval(vx + 30, vy - 86, 24, 22, rel, ink, 2, at=tv, fx="pop"),
                 poly([(vx + 50, vy - 92), (vx + 74, vy - 80), (vx + 52, vy - 74)], ink, at=tv),
                 poly([(vx - 30, vy - 40), (vx - 120, vy - 80), (vx - 222, vy - 96), (vx - 200, vy - 70), (vx - 214, vy - 58), (vx - 180, vy - 48), (vx - 196, vy - 34),
                       (vx - 160, vy - 28), (vx - 170, vy - 14), (vx - 120, vy - 10), (vx - 60, vy + 10), (vx - 30, vy + 20)], rel, ink, 2, tv, "pop"),
                 line([[vx - 10, vy + 70], [vx - 14, vy + 110]], tv, ink, 4, draw=False), line([[vx + 14, vy + 70], [vx + 18, vy + 110]], tv, ink, 4, draw=False),
                 {"k": "circle", "x": VS["disc"][0], "y": VS["disc"][1], "r": 28, "fill": rel, "c": ink, "w": 2, "in": td, "fx": "pop"}]
    for j, (x, y) in enumerate(VS["birds"]):
        out += bird(x, y, 80, round(tb + .25 * j, 2), rel, ink, -1 if x > 1100 else 1)
    out += scorpion(VS["scorp"][0], VS["scorp"][1], 100, ts, rel, 3)
    out += [{"k": "line", "p": R([(1268, 320), (1252, 370), (1270, 420), (1252, 470), (1270, 520), (1256, 560)]), "c": rel, "w": 9, "curve": True, "in": tsn, "fx": "draw", "dur": .7},
            oval(1268, 316, 10, 8, rel, ink, 1.5, at=round(tsn + .5, 2), fx="pop")]
    for j, x in enumerate((830, 1025, 1220)):
        t = round(tbx + .3 * j, 2)
        out += [rect(x - 60, 205, 120, 70, rel, ink, 2, 6, t, "pop"), {"k": "line", "p": R([(x - 34, 205), (x - 30, 180), (x + 30, 180), (x + 34, 205)]), "c": rel, "w": 6, "curve": True, "in": t}]
    out += [figure_outline(VS["man"][0], VS["man"][1], 130, tm, rel, 3)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": out}


def s48_late(C):
    """The star map reading (Sweatman & Tsikritsis 2017), drawn as a claim: stars come out over the pillar, each animal becomes a cluster
    of star points joined by dotted lines into a constellation, and the disc fills gold as the Sun."""
    tm, tc, ts = C.at(47, "star map"), C.at(47, "constellations"), C.at(47, "the Sun")
    vx, vy = VS["vulture"]
    groups = [[(vx + 30, vy - 86), (vx, vy - 40), (vx - 210, vy - 88), (vx - 190, vy - 30), (vx, vy + 60)],
              [VS["birds"][0], (VS["birds"][0][0] + 34, VS["birds"][0][1] - 16), VS["birds"][1]],
              [(VS["scorp"][0] - 22, VS["scorp"][1] - 60), (VS["scorp"][0], VS["scorp"][1]), (VS["scorp"][0] + 22, VS["scorp"][1] - 60), (VS["scorp"][0] + 30, VS["scorp"][1] + 50)],
              [(1268, 316), (1262, 420), (1256, 560)], [VS["birds"][2], (VS["birds"][2][0] - 34, VS["birds"][2][1] - 16)]]
    out = [stars(70, 690, 1360, 150, 790, tm, 17), label(1380, 300, "a star map?", round(tm + .3, 2), LILAC, 30, "start")]
    k = 0
    for g in groups:
        for (x, y) in g:
            out += [glow(x, y, 26, round(tc + .04 * k, 2), .9), dot(x, y, 5, "#fff2c0", round(tc + .04 * k, 2))]; k += 1
        out.append({"k": "line", "p": R(g), "c": LILAC, "w": 2.5, "style": "claimed", "in": round(tc + .5 + .1 * groups.index(g), 2)})
    dx, dy = VS["disc"]
    return out + [{"k": "circle", "x": dx, "y": dy, "r": 28, "fill": "#f2c76e", "c": "#fff3dc", "w": 2, "in": ts, "fx": "pop"}, glow(dx, dy, 110, ts, .9, "sun")]


def s49(C):
    """The trick: the Earth's axis (tilted 23 degrees) wobbles like a spinning top, a circle in about 26,000 years; so the stars behind
    the Sun on the longest day drift (the sky band, in three steps); turn back the dial until the sky matches the carving (dotted)."""
    tw, tt, tn, ts, tl, tm, td = C.at(48, "wobbles slowly"), C.at(48, "spinning top"), C.at(48, "twenty-six thousand"), C.at(48, "So the stars"), C.at(48, "longest day"), C.at(48, "Match the carving"), C.at(48, "a date")
    ex, ey, er = 380, 430, 120
    sn, cs = math.sin(math.radians(23)), math.cos(math.radians(23))
    out = [{"k": "circle", "x": ex, "y": ey, "r": er, "fill": "#2f5f7a", "c": BLUE, "w": 2, "in": .4, "fx": "pop"},
           oval(ex - 40, ey - 30, 44, 26, "#5f8a5a", at=.5), oval(ex + 30, ey + 40, 30, 20, "#5f8a5a", at=.5),
           line([[ex, ey + 180], [ex, ey - 200]], .7, BONE, 1.5, "inferred", draw=False, op=.5),
           line([[round(ex - sn * 190, 1), round(ey + cs * 190, 1)], [round(ex + sn * 190, 1), round(ey - cs * 190, 1)]], .8, BONE, 3, dur=.6),
           {"k": "line", "p": R(ellipse(ex, ey - cs * 190, sn * 190, 20, 40)), "c": AMBER, "w": 2.5, "curve": True, "in": tw, "fx": "draw", "dur": 2.0},
           label(ex - 110, round(ey - 222, 1), "23°", round(tw - .2, 2), BONE, 26, "end"),
           label(ex, 668, "c. 26,000 years", tn, AMBER, 28),
           poly([(640, 520), (720, 520), (680, 610)], "#c8743c", "#f4b27a", 1.5, tt, "pop"),
           line([[680, 520], [round(680 + sn * 90, 1), round(520 - cs * 90, 1)]], tt, "#8a6a44", 5, draw=False),
           {"k": "line", "p": R(ellipse(680, 520 - cs * 90, sn * 90, 10, 30)), "c": AMBER, "w": 2, "curve": True, "in": round(tt + .3, 2), "fx": "draw", "dur": 1.6}]
    band = [880, 230, 800, 300]
    out += [rect(*band, "#0c1424", "#3a4a6a", 1.5, 10, ts), stars(40, 890, 1670, 240, 520, round(ts + .1, 2), 31)]
    sun = lambda t: [line([[1280, 240], [1280, 520]], t, GOLD, 1.5, "inferred", draw=False, op=.7), {"k": "circle", "x": 1280, "y": 380, "r": 24, "fill": "#f2c76e", "c": "#fff3dc", "w": 2, "in": t}]
    pattern = lambda dx, t, c="#fff2c0", st="known": {"k": "group", "clip": band + [10], "in": t, "els":
                                                        sum([stargroup(cx + dx, 380 + oy, 60, sd, -1, c, True, None, c, st) for cx, oy, sd in ((1000, -40, 5), (1220, 50, 6), (1440, -30, 7))], [])}
    out += sun(ts) + [pattern(0, round(ts + .3, 2)), label(1280, 568, "longest day", tl, GOLD, 28)]
    t1 = round(ts + 1.9, 2)
    out += [rect(*band, "#0c1424", at=t1, op=.7, dur=.3)] + sun(t1) + [pattern(-110, round(t1 + .1, 2))]
    out += [rect(1210, 600, 140, 140, CARD, at=round(tm + .2, 2), r=70), ring(1280, 670, 60, round(tm + .2, 2), MUTED, 2)] + \
           [line([[1280, 670], [round(1280 + 50 * math.cos(math.radians(a)), 1), round(670 + 50 * math.sin(math.radians(a)), 1)]], round(tm + .4 + .6 * j, 2), BONE, 3, draw=False)
            for j, a in enumerate((-90,))] + [label(1370, 678, "back in time", round(tm + .4, 2), MUTED, 24, "start")]
    for j, a in enumerate((-150, -210)):
        t = round(tm + 1.0 + .6 * j, 2)
        out += [{"k": "circle", "x": 1280, "y": 670, "r": 56, "fill": CARD, "c": "none", "w": 0, "in": t, "dur": .2},
                line([[1280, 670], [round(1280 + 50 * math.cos(math.radians(a)), 1), round(670 + 50 * math.sin(math.radians(a)), 1)]], t, BONE, 3, draw=False)]
    t2 = round(tm + 1.6, 2)
    out += [rect(*band, "#0c1424", at=t2, op=.55, dur=.3)] + sun(t2) + [pattern(-220, round(t2 + .1, 2)), pattern(-220, round(t2 + .4, 2), LILAC, "claimed")] + \
           [glow(1170, 380, 220, round(t2 + .5, 2), .35, "lamp"), label(1170, 214, "a match?", round(t2 + .6, 2), LILAC, 26)]
    return {"base": "dark", "stars": 80, "cam": CAM, "els": out}


AX50 = lambda Y_: round(220 + (11500 - Y_) / 2500 * 1340, 1)       # 11,500 to 9,000 BCE


def s50(C):
    """Their date (claimed, dotted): 10,950 BCE give or take 250 years; a comet drops onto it; the start of the Younger Dryas (blue
    tick); the headless man, read as death, glows faintly at the side."""
    X = AX50
    td, tg, tc, ty, th = C.at(49, "ten thousand nine hundred"), C.at(49, "give or take"), C.at(49, "comet strike"), C.at(49, "the Younger Dryas"), C.at(49, "The headless man")
    return {"base": "dark", "stars": 40, "cam": CAM, "els": [
        {"k": "axis", "x0": 220, "x1": 1560, "y": 640, "ticks": [[X(y), "{:,}".format(y)] for y in range(11500, 8999, -500)], "t": "BCE", "in": .3},
        dot(X(10950), 560, 9, LILAC, td), glow(X(10950), 560, 50, td, .7, "blue"),
        rect(X(11200), 549, X(10700) - X(11200), 22, "rgba(201,193,238,.25)", LILAC, 2, 11, tg, style="claimed"),
        label(X(11200) - 16, 568, "the claimed sky", round(tg + .4, 2), LILAC, 28, "end"),
        line([[720, 170], [X(10950) + 6, 548]], tc, "#ffe2a8", 5, dur=.6), line([[736, 184], [X(10950) + 12, 550]], tc, "#ffcf8a", 2, dur=.6, op=.6),
        glow(X(10950), 548, 70, round(tc + .5, 2), .9, "fire"),
        line([[X(10900), 600], [X(10900), 700]], ty, BLUE, 3, draw=False), label(X(10900), 732, "Younger Dryas begins", round(ty + .2, 2), BLUE, 26),
        figure_outline(1560, 440, 170, th, BONE, 2.5, op=.6), glow(1560, 360, 120, round(th + .3, 2), .3, "lamp")]}


def s52_late(C):
    """The excavators' answer (Notroff et al. 2017): their oldest date for Enclosure D, from wall plaster (9745 to 9314 BCE), sits
    700 to 1,000 years after that sky."""
    X = AX50
    tp, ty = C.at(51, "wall plaster"), C.at(51, "seven hundred")
    return [label(1660, 186, "Notroff et al. 2017", .8, MUTED, 26, "end"),
            {"k": "line", "p": [[X(9745), 560], [X(9314), 560]], "c": AMBER, "w": 22, "op": .95, "keepop": True, "fx": "draw", "dur": .8, "in": tp},
            tpill(round((X(9745) + X(9314)) / 2, 1), 549, 80, round(tp + .5, 2), 1, 18), label(round((X(9745) + X(9314)) / 2, 1), 452, "pillar carved", round(tp + .7, 2), GOLD, 28),
            line([[X(10700), 524], [X(10700), 506], [X(9745), 506], [X(9745), 524]], ty, BONE, 2.5, dur=.8),
            label(round((X(10700) + X(9745)) / 2, 1), 490, "700 to 1,000 years", round(ty + .5, 2), BONE, 30)]


def s53_late(C):
    """A memorial carved long after the event (dotted: their reply); but then the building cannot vouch for the date (the plaster band
    dims) and everything rests on the star matching (an arrow back to the star map)."""
    X = AX50
    tm, te, tv, ts = C.at(52, "a memorial"), C.at(52, "the event"), C.at(52, "can't vouch"), C.at(52, "star matching")
    return [poly([(1428, 640), (1428, 590), (1442, 576), (1456, 590), (1456, 640)], "#b39b7a", "#e0c9a2", 1.5, tm, "rise"),
            line([[330, 586], [366, 612]], te, "#ffe2a8", 3, dur=.4), glow(366, 612, 30, te, .8, "fire"),
            line([[372, 616], [1424, 616]], round(te + .3, 2), LILAC, 2.5, "claimed", 1.2),
            rect(X(9745) - 10, 545, X(9314) - X(9745) + 20, 30, "#0d0b09", at=tv, op=.62, dur=.8),
            rect(190, 210, 180, 110, CARD, LILAC, 2, 10, round(ts - .6, 2), style="claimed")] + \
           stargroup(280, 266, 60, 9, round(ts - .4, 2), "#fff2c0", True, None, LILAC, "claimed") + \
           [arrow([[X(11000), 544], [360, 420], [300, 330]], ts, LILAC, 3, "claimed", .8)]


def s51(C):
    """Sweatman 2024, drawn as a claim: V-shaped marks counted as days, twelve Moon-months (29 or 30 marks each, a crescent over each)
    plus eleven more: 365."""
    tv, t365, tm, t11, tk = C.at(50, "V-shaped marks"), C.at(50, "three hundred and sixty-five"), C.at(50, "twelve Moon-months"), C.at(50, "eleven more"), C.at(50, "the oldest known")
    out = [label(120, 182, "Sweatman 2024", .5, LILAC, 28, "start")]
    V = lambda x, y, t: line([[x - 7, y - 6], [x, y + 6], [x + 7, y - 6]], t, LILAC, 2.5, draw=False)
    step = (t365 - tv - .4) / 12
    for g in range(12):
        x0, y0 = 150 + 205 * (g % 6), 270 + 230 * (g // 6)
        n = 30 if g % 2 else 29
        t = round(tv + step * g, 2)
        out += [V(x0 + 22 * (j % 6), y0 + 24 * (j // 6), round(t + .006 * j, 3)) for j in range(n)]
        out.append(crescent(x0 + 56, y0 - 40, 14, round(tm + .1 * g, 2)))
    out += [V(1440 + 22 * (j % 6), 300 + 24 * (j // 6), round(t365 - .3 + .02 * j, 2)) for j in range(11)]
    out += [label(1600, 560, "365", t365, LILAC, 72, st="big"), label(684, 700, "12 Moon-months", round(tm + .4, 2), LILAC, 30),
            rect(1424, 280, 150, 70, "none", LILAC, 2, 10, t11, style="claimed"), label(1500, 386, "+ 11", round(t11 + .2, 2), LILAC, 30),
            label(1600, 640, "a calendar?", tk, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": out}


def s54(C):
    """Star matching is flexible: more than sixty pillars; pick three, and dotted lines can join their animals to many different star
    groups; a cloud drifts by that looks like a face."""
    tp, tk, tg, tc = C.at(53, "More than sixty"), C.at(53, "pick a few"), C.at(53, "which star group"), C.at(53, "faces in clouds")
    cells = [(150 + 60 * (j % 8), 220 + 58 * (j // 8)) for j in range(64)]
    out = [tpill(x, y + 30, 40, round(tp + .02 * j, 2), 1, 9, "#cdb48e", STONE_E, "pop") for j, (x, y) in enumerate(cells)]
    out += [label(360, 736, "more than 60 pillars", round(tp + 1.4, 2), BONE, 28)]
    groups = [(1080, 240), (1330, 230), (1560, 300), (1120, 470), (1380, 440), (1590, 560)]
    for j, (x, y) in enumerate(groups):
        out += stargroup(x, y, 70, 20 + j, round(.4 + .1 * j, 2), "#fff2c0", True, .8, "#fff2c0", "known")
    pick = [cells[17], cells[38], cells[51]]
    out += [poly([(640, 300), (700, 280), (712, 300), (676, 314)], "#e8d6b8", "#8c7152", 1.5, tk, "pop"), line([[640, 300], [610, 304]], tk, "#e8d6b8", 8, draw=False)]
    out += [ring(x, y + 10, 34, round(tk + .3 + .3 * j, 2), GOLD, 3) for j, (x, y) in enumerate(pick)]
    q = 0
    for j, (x, y) in enumerate(pick):
        for gi in ((0, 3, 4), (1, 4, 5), (2, 3, 0))[j]:
            gx, gy = groups[gi]
            out.append(line([[x + 30, y + 10], [gx - 60, gy]], round(tg + .18 * q, 2), LILAC, 2, "claimed", .5)); q += 1
    out += cloud_face(889, 690, 110, tc)
    return {"base": "dark", "stars": 60, "cam": CAM, "els": out}


def s55_late(C):
    """The headless man again: he is carved with an erect phallus (said, not drawn), hardly a picture of death: highlighted, 'not lifeless'."""
    th, tl = C.at(54, "the headless man"), C.at(54, "hardly")
    x, by = VS["man"]
    return [figure_outline(x, by, 130, th, GOLD, 4), glow(x, by - 70, 120, th, .5, "lamp"), label(x - 40, by - 162, "not lifeless", tl, GOLD, 32)]


PAPERS = lambda n, c: (lambda x, y, at: [rect(x - 46 + 3 * (j % 2), y - 14 * (j + 1), 92, 12, c, "#8a7a66", 1, 2, at) for j in range(n)])


def s56(C):
    """Even the comet is in dispute: a balance with a review (2023) on one pan and a rebuttal (2024) on the other; the beam wobbles
    and does not settle; a faint comet above."""
    tc, trv, trf, trb = C.at(55, "the comet"), C.at(55, "A large review"), C.at(55, "refuted"), C.at(55, "a rebuttal")
    L, Rr = PAPERS(6, "#efe6d2"), PAPERS(5, "#e6dcc8")
    bal = lambda ang, at, l, r_: balance(889, 330, 640, ang, 720, at, l, r_)
    mask = lambda t: rect(430, 250, 920, 380, CARD, at=t, dur=.4)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [rect(330, 150, 1120, 620, CARD, "#4a3a2c", 1.5, 18, .1),
            line([[1300, 180], [1090, 236]], tc, "#ffe2a8", 3, dur=.6, op=.4), glow(1090, 236, 50, round(tc + .4, 2), .4, "fire")] +
            bal(0, .3, None, None) + L(569, 500, trv) + [label(569, 690, "review, 2023", trv, BONE, 30),
            mask(trf)] + bal(-5, trf, L, None) + [label(1209, 690, "rebuttal, 2024", trb, BONE, 30), mask(trb)] + bal(2.5, trb, L, Rr) +
            [mask(round(trb + .6, 2))] + bal(-1.5, round(trb + .6, 2), L, Rr)}


def s57(C):
    """If the enclosures had roofs (dashed, inferred), they made poor observatories: a roof draws over the ring and the stars dim."""
    tr, to = C.at(56, "had roofs"), C.at(56, "poor observatories")
    cx, cy, rx, ry = 889, 610, 420, 90
    ring_els, _ = enclosure(cx, cy, rx, ry, 150, .3, step=.05, hc=230)
    roof = [(cx - rx - 40, cy - 130), (cx - rx * .5, cy - 240), (cx, cy - 280), (cx + rx * .5, cy - 240), (cx + rx + 40, cy - 130)]
    return {"base": "sky", "tod": "night", "ground": 760, "groundc": "#241d17", "sun": False, "cam": CAM, "els": [
        rect(-40, -40, 1860, 640, "#070912", at=to, op=.62, dur=1.2, layer="far")] + ring_els + [
        poly(roof + [(cx + rx + 40, cy - 116), (cx - rx - 40, cy - 116)], "rgba(245,236,220,.07)", BONE, 3, tr, curve=False, style="inferred"),
        {"k": "line", "p": R(ellipse(cx, cy - 123, rx + 40, 30, 40)), "c": BONE, "w": 2.5, "style": "inferred", "curve": True, "in": round(tr + .3, 2)},
        label(cx, cy - 310, "a roof?", round(tr + .5, 2), BONE, 30)]}


def s58_late(C):
    """A sky map with a date stamp? The gap between the claimed sky and the plaster pulses softly; a gold question mark over it."""
    X = AX50
    gx = round((X(10700) + X(9745)) / 2, 1)
    return [{"k": "glow", "x": gx, "y": 560, "r": 150, "kind": "lamp", "op": .5, "keepop": True, "in": .5, "pulse": True}] + question(gx, 596, C.at(57, "disagree"), 64, GOLD)


# ================================================================ chapter 5: the weighing
COLS = (("established", GREEN, 360), ("open", BLUE, 890), ("ruled out", GREY, 1420))


def s59(C):
    """The ledger: established (a pillar, c. 9500 BCE; no pottery, metal or farm animals; homes, hearths, cisterns, sister sites),
    still open (how many people, which seasons), and, later, ruled out."""
    tE, t95, tp, tm, ta = C.at(58, "Established"), C.at(58, "nine and a half thousand"), C.at(58, "without pottery"), C.at(58, "metal"), C.at(58, "farm animals")
    tw, th, thr, tc, ts = C.at(58, "Well documented"), C.at(58, "homes"), C.at(58, "hearths"), C.at(58, "cisterns"), C.at(58, "sister sites")
    tO, tpe, ty = C.at(58, "Still open"), C.at(58, "how many people"), C.at(58, "how much of the year")
    out = [hill([(-20, 800), (300, 770), (889, 740), (1480, 770), (1800, 800)], "#2a2119", "#5a4836", 1.5, -1)]
    for name, c, x in COLS[:2]:
        t = tE if name == "established" else tO
        out += [label(x, 186, name, t, c, 36, st="serif"), line([[x - 230, 208], [x + 230, 208]], t, c, 2, dur=.6)]
    out += [tpill(210, 330, 100, t95, 1, 22), label(280, 304, "c. 9500 BCE", round(t95 + .3, 2), GREEN, 30, "start"),
            label(280, 336, "stone giants", round(t95 + .5, 2), MUTED, 24, "start")]
    for (x, mk, t) in ((220, "pot", tp), (360, "axe", tm), (500, "sheep", ta)):
        out += (pot(x, 430, 90, t) if mk == "pot" else axe(x, 430, 90, t) if mk == "axe" else sheep(x - 6, 466, 90, t))
        out.append(strike(x - 42, 476, x + 42, 384, round(t + .3, 2), RED, 4))
    out += [label(360, 532, "well documented", tw, MUTED, 24)]
    out += house_round(200, 600, 34, th) + hearth(320, 602, thr, 1.1) + cistern(440, 602, 100, tc) + pins(555, 598, ts, AMBER, 6)
    out += people(686, 330, 3, 64, tpe, "#e8d6b8", 28) + [label(800, 322, "?", round(tpe + .3, 2), BLUE, 44, st="big"), label(840, 314, "how many people", round(tpe + .4, 2), MUTED, 26, "start")]
    out += year_wheel(716, 400, 30, ty) + [label(800, 418, "?", round(ty + .3, 2), BLUE, 44, st="big"), label(840, 410, "which seasons", round(ty + .4, 2), MUTED, 26, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": out}


def s60_late(C):
    """Open too: what the figures meant, roofs, how much burying was by hand; ruled out (as far as thirty years of digging can tell):
    farm herds, metal tools, writing."""
    tf, tr, tb, tO = C.at(59, "the figures meant"), C.at(59, "had roofs"), C.at(59, "burying"), C.at(59, "ruled out")
    th, tm, tw = C.at(59, "farm herds"), C.at(59, "metal tools"), C.at(59, "writing")
    name, c, x = COLS[2]
    out = [tpill(712, 534, 70, tf, 1, 16), {"k": "lib", "k2": "person", "x": 714, "y": 534, "h": 66, "color": BONE, "op": .35, "keepop": True, "in": round(tf + .3, 2)},
           label(800, 516, "?", round(tf + .3, 2), BLUE, 44, st="big"), label(840, 508, "what figures meant", round(tf + .4, 2), MUTED, 26, "start"),
           poly([(670, 610), (716, 576), (762, 610)], "none", BONE, 2.5, tr, style="inferred"), line([[674, 614], [758, 614]], tr, BONE, 2.5, "inferred", draw=False),
           label(800, 618, "?", round(tr + .3, 2), BLUE, 44, st="big"), label(840, 610, "roofs", round(tr + .4, 2), MUTED, 26, "start")] + \
          balance(716, 676, 96, 0, 760, tb, None, None, drop=36, pan=42) + [label(800, 724, "?", round(tb + .3, 2), BLUE, 44, st="big"),
           label(840, 716, "hands or hillside", round(tb + .4, 2), MUTED, 26, "start"),
           label(x, 186, name, tO, c, 36, st="serif"), line([[x - 230, 208], [x + 230, 208]], tO, c, 2, dur=.6)]
    out += sheep(1340, 350, 76, th, "#d8d2c8") + sheep(1430, 342, 70, round(th + .1, 2), "#d8d2c8") + sheep(1520, 352, 76, round(th + .2, 2), "#d8d2c8") + \
           [strike(1290, 372, 1590, 270, round(th + .4, 2), GREY, 5)]
    out += axe(1420, 490, 100, tm, "#9aa0a8") + [strike(1360, 540, 1480, 432, round(tm + .3, 2), GREY, 5)]
    out += tablet(1420, 640, 100, tw) + [strike(1360, 690, 1480, 590, round(tw + .3, 2), GREY, 5)]
    return out


def lostcity_card(x, y, at):
    out = [rect(x - 110, y - 150, 220, 150, "rgba(201,193,238,.08)", LILAC, 3, 10, at, "rise", style="claimed")]
    out += [rect(x - 80 + 34 * j, y - 24 - (50 + 22 * (j % 3)), 24, 50 + 22 * (j % 3), "none", "#e6e0ff", 2.5, 1, at, "rise", style="claimed") for j in range(5)]
    return out


def comet_card(x, y, at):
    return [rect(x - 110, y - 150, 220, 150, "rgba(201,193,238,.08)", LILAC, 3, 10, at, "rise", style="claimed"),
            tpill(x - 16, y - 16, 92, at, 1, 20, "none", "#e6e0ff", "rise", style="claimed", sw=3),
            line([[x + 92, y - 136], [x + 22, y - 92]], at, "#e6e0ff", 3.5, "claimed", draw=False), glow(x + 22, y - 92, 40, at, .6, "blue")]


def s61(C):
    """The verdict on the bold claims: a lost civilisation and a comet on Pillar 43, as two dotted cards on a balance; 'Awaiting
    evidence' settles over it; the empty test boxes beside them; the spade and the clock under the boxes."""
    tl, tc, tv, tp, ts, tk = C.at(60, "A lost civilisation"), C.at(60, "A comet strike"), C.at(60, "Awaiting evidence"), C.at(60, "predictions we can test"), C.at(60, "the spade"), C.at(60, "the clock")
    out = balance(700, 330, 560, 0, 720, .3, None, None) + lostcity_card(420, 500, tl) + comet_card(980, 500, tc)
    out += [rect(530, 156, 340, 66, "rgba(159,208,255,.14)", AWAIT, 2.5, 33, tv, "pop"), label(700, 200, "Awaiting evidence", tv, AWAIT, 32), glow(700, 190, 200, tv, .35, "blue")]
    out += [rect(1180 + 130 * j, 380, 110, 110, "none", BLUE, 3, 10, round(tp + .2 * j, 2), "rise", style="inferred") for j in range(3)]
    out += spade(1310, 610, 90, ts) + candle_clock(1440, 620, 80, tk)
    return {"base": "dark", "stars": 50, "cam": CAM, "els": out}


def s62(C):
    """What would change our minds: three test boxes fill as they are named. A tool with no local roots in the oldest layer; charcoal
    sealed under the foot of a standing pillar, dated (a tick at 11,000 BCE); an impact layer that even its critics accept."""
    t1, tr, t2, t11, t3 = C.at(61, "A tool"), C.at(61, "no local roots"), C.at(61, "Charcoal"), C.at(61, "eleven thousand BCE"), C.at(61, "an impact layer")
    out = [label(889, 172, "what would change our minds", .4, BONE, 32)]
    out += [rect(120 + 524 * j, 220, 490, 480, "none", BLUE, 3, 14, round(.5 + .2 * j, 2), style="inferred") for j in range(3)]
    cols = ["#8a7258", "#7a6248", "#6b5440", "#5f4c39", "#4e3e2e"]
    out += [rect(150, 290 + 74 * j, 430, 74, c, at=round(t1 + .1 * j, 2), fx="fill", dur=.4) for j, c in enumerate(cols)]
    out += [poly([(340, 640), (392, 626), (400, 636), (350, 652)], "#cfe6ff", "#ffffff", 1.5, tr, "pop"), glow(370, 638, 70, tr, .9, "blue"),
            label(365, 262, "no local roots", round(tr + .3, 2), BLUE, 26), label(365, 690, "oldest layer", round(t1 + .6, 2), MUTED, 24)]
    out += [rect(664, 520, 450, 160, "#8c7152", at=t2), rect(834, 520, 110, 82, "#3a2e24", at=t2), rect(844, 300, 90, 296, STONE, STONE_E, 1.5, 2, t2, "rise"),
            dot(889, 602, 6, "#1a1410", round(t2 + .4, 2)), glow(889, 604, 46, round(t2 + .4, 2), .9, "fire"), label(1000, 632, "charcoal", round(t2 + .6, 2), BONE, 26, "start"),
            line([[700, 270], [1080, 270]], t11, BONE, 2, dur=.6), line([[760, 258], [760, 282]], round(t11 + .3, 2), GOLD, 4, draw=False),
            label(760, 248, "11,000 BCE", round(t11 + .3, 2), GOLD, 24)]
    out += [rect(1200, 270, 140, 410, "#7a6248", at=t3)] + [rect(1200, 270 + 82 * j, 140, 41, "#8a7258", at=t3) for j in range(5)] + \
           [rect(1200, 466, 140, 12, "#141010", at=round(t3 + .4, 2)), glow(1270, 472, 80, round(t3 + .4, 2), .5, "red"), label(1360, 482, "impact layer?", round(t3 + .6, 2), LILAC, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": out}


def s63(C):
    """The spade isn't finished: the hill as a hundred squares from the Short 'gobekli' (lg_a.gob_hill, through a window), about a tenth
    dug; survey lines sweep the rest and faint dashed rings and rectangles appear beyond the dig (2025, 2026 reports)."""
    import lg_a
    sc = copy.deepcopy(lg_a.gob_hill())
    keep = []
    for e in sc["els"]:
        if LILAC in (e.get("c"), e.get("fill")) or e.get("t") == "?" or (e.get("k") == "glow" and (e.get("in") or 0) >= 7.0):
            continue
        keep.append(e)
    tdug = C.at(62, "the spade")
    dug = [e for e in keep if e.get("fill") == AMBER]
    for j, e in enumerate(dug):
        e["in"] = round(tdug + .5 + .07 * j, 2)
    for e in keep:
        if e.get("k") == "glow":
            e["in"] = round(tdug + 1.3, 2)
    sc["els"] = keep
    crop, at, s = [90, 480, 820, 800], [180, 110], .8
    cell = lambda r_, c_: (round(at[0] + (153 + 52 * c_) * s, 1), round(at[1] + (143 + 52 * r_) * s, 1))
    tn, ts, tb = C.at(62, "nine-tenths"), C.at(62, "Surveys"), C.at(62, "more buildings")
    x0, y0 = cell(0, 0)
    els = [label(900, 330, "about 1 in 10 dug", round(tdug + 1.0, 2), AMBER, 30, "start"),
           rect(x0 - 6, y0 - 6, 41.6 * 10 + 6, 41.6 * 10 + 6, "none", BLUE, 2, 6, tn, style="inferred"), label(900, 378, "nine-tenths waiting", round(tn + .4, 2), BLUE, 28, "start")]
    els += [line([[x0 - 6, round(y0 + 41.6 * r_ + 18.4, 1)], [round(x0 + 41.6 * 10, 1), round(y0 + 41.6 * r_ + 18.4, 1)]], round(ts + .12 * r_, 2), BLUE, 2, dur=.35, op=.55) for r_ in range(10)]
    els += [label(900, 470, "surveys 2025, 2026", round(ts + .4, 2), BLUE, 30, "start")]
    shapes = [("rect", 2, 6, 3, 2), ("ring", 3, 1), ("ring", 1, 4), ("rect", 8, 6, 3, 2), ("ring", 4, 8)]
    for j, sh in enumerate(shapes):
        t = round(tb + .25 * j, 2)
        if sh[0] == "rect":
            x, y = cell(sh[1], sh[2])
            els.append(rect(x, y, 41.6 * sh[3] - 4.8, 41.6 * sh[4] - 4.8, "rgba(159,208,255,.08)", BLUE, 2.5, 4, t, style="inferred"))
        else:
            x, y = cell(sh[1], sh[2])
            els.append({"k": "circle", "x": round(x + 18.4, 1), "y": round(y + 18.4, 1), "r": 26, "fill": "rgba(159,208,255,.08)", "c": BLUE, "w": 2.5, "style": "inferred", "in": t})
    els += [label(900, 516, "more buildings reported", round(tb + .6, 2), MUTED, 26, "start")]
    return inset(sc, s=s, crop=crop, at=at, els=els, cam=CAM)


def s64(C):
    """The hill at night in cross-section: under the grass, faint dashed rings of T-pillars glow one after another."""
    tg = C.at(63, "more stone giants")
    out = [hill([(-20, 640), (200, 600), (500, 470), (889, 400), (1280, 470), (1580, 600), (1800, 640)], "#2a2119", "#4a5a3a", 3, -1), glow(889, 420, 500, -1, .12, "lamp")]
    for j, (cx, cy, s) in enumerate(((620, 600, 1.0), (880, 520, .9), (1140, 590, 1.0), (760, 700, .8), (1020, 700, .8))):
        t = round(tg + .45 * j, 2)
        els, _ = enclosure(cx, cy, 100 * s, 22 * s, 48 * s, t, step=.03, n=7, hc=70 * s, style="inferred", c=GOLD, back_c=GOLD, wall_c=GOLD, wall_w=2, op_back=.6)
        out += [glow(cx, cy - 30 * s, 130 * s, t, .4, "lamp")] + els
    return {"base": "sky", "tod": "night", "ground": 1000, "sun": False, "moon": [1450, 200, 26], "cam": CAM, "els": out}


# ================================================================ the film
ALIAS = {1: 0, 2: 0, 6: 5, 8: 7, 12: 11, 13: 11, 24: 23, 31: 30, 37: 36, 44: 41, 45: 46, 47: 46, 51: 49, 52: 49, 54: 46, 57: 49, 59: 58}
ALIAS_CAMS = {1: [1.5, 795, 470], 2: [1, 889, 500], 8: [1.35, 1110, 520], 12: [1.45, 790, 470], 13: [1.08, 823, 470], 24: [1, 889, 500], 31: [1, 889, 500],
              37: [1.4, 1143, 420], 44: [1, 889, 500], 47: [1, 889, 500], 51: [1, 889, 500], 52: [1, 889, 500], 54: [1.5, 1050, 590], 57: [1, 889, 500], 59: [1, 889, 500]}


def _tagged(cams):
    """Each alias camera gets a tiny unique extra zoom (a few ten-thousandths: invisible), so its step can be found after the wall is built."""
    out = {}
    for k, i in enumerate(sorted(cams)):
        z, x, y = cams[i]
        out[i] = [round(z + .0003 * (k + 1), 4), x, y]
    return out


def _attach(ep, cams, late):
    """Give each alias step its additions: a panel item on that step (built once, shown from the start of its glide, timed on its clock)."""
    panels = ep["wall"]["panels"]
    for i, els in late.items():
        z = cams[i][0]
        ks = [k for k, s in enumerate(ep["shots"]) if abs(s["cam"][0] - z) < 1e-9]
        assert len(ks) == 1, ("alias step", i, ks)
        k = ks[0]
        cx, cy = ep["shots"][k]["cam"][1:]
        js = [j for j, p in enumerate(panels) if p["ox"] <= cx <= p["ox"] + p.get("w", W_) and p["oy"] <= cy <= p["oy"] + p.get("h", H_)]
        assert len(js) == 1, ("panel of alias", i, js)
        p = panels[js[0]]
        ep["shots"][k]["els"].append({"k": "panel", "ox": p["ox"], "oy": p["oy"], "w": p.get("w", W_), "h": p.get("h", H_), "base": "none", "els": list(els), "pn": js[0]})
    return ep


def lf_gobekli():
    beats = BEATS()
    C = Clock(beats)
    scenes = {0: s01, 3: s04, 4: s05, 5: s06, 7: s08, 9: s10, 10: s11, 11: s12, 14: s15, 15: s16, 16: s17, 17: s18, 18: s19, 19: s20, 20: s21, 21: s22, 22: s23,
              23: s24, 25: s26, 26: s27, 27: s28, 28: s29, 29: s30, 30: s31, 32: s33, 33: s34, 34: s35, 35: s36, 36: s37, 38: s39, 39: s40, 40: s41, 41: s42,
              42: s43, 43: s44, 46: s47, 48: s49, 49: s50, 50: s51, 53: s54, 55: s56, 56: s57, 58: s59, 60: s61, 61: s62, 62: s63, 63: s64}
    lates = {1: s02_late, 2: s03_late, 8: s09_late, 12: s13_late, 13: s14_late, 24: s25_late, 31: s32_late, 37: s38_late, 44: s45_late, 47: s48_late, 51: s52_late,
             52: s53_late, 54: s55_late, 57: s58_late, 59: s60_late}
    shots = []
    for i in range(64):
        if i in scenes:
            shots.append(scenes[i](C))
        else:
            shots.append({"base": "dark", "cam": CAM, "els": []})             # an alias: a reframing of (or merged into) another panel
    cams = _tagged(ALIAS_CAMS)
    late = {i: f(C) for i, f in lates.items()}
    ep = {"id": "lf-gobekli", "code": "LF.03", "series": "Before Us", "title": "Göbekli Tepe: What the Stones Say", "case": "gobekli-excavation",
          "verdict": "unsupported", "claim": "Survivors of a lost civilisation, and a comet strike carved on a pillar: what do Göbekli Tepe's stones say?",
          "mood": "awe", "hook_text": "Who carved stone *giants* 11,500 years ago?", "beats": beats, "shots": shots,
          "sources": "Dietrich et al. 2012 (doi:10.1017/S0003598X00047840) · Clare 2020 (doi:10.34780/efb.v0i2.1012) · Dietrich L. et al. 2019 (doi:10.1371/journal.pone.0215214) · "
                     "Notroff et al. 2017, MAA 17(2) · Sweatman 2024 (doi:10.1080/1751696X.2024.2373876) · Holliday et al. 2023 (doi:10.1016/j.earscirev.2023.104502)",
          "post": "Stone giants with arms, hands and belts, raised about 11,500 years ago by people with no pottery, metal or farm animals. A lost civilisation? A comet "
                  "recorded on the Vulture Stone? The excavation reports, the radiocarbon dates and the sister sites, weighed.",
          "hashtags": ["#GobekliTepe", "#Archaeology", "#Neolithic", "#YoungerDryas", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": "Göbekli Tepe: What the Stones Say",
          "yt_title": "Göbekli Tepe: A Lost Civilisation, a Comet, and What the Stones Say",
          "description": DESCRIPTION, "end_line": "Somewhere under that hill, more stone giants may still be standing."}
    out = remix(ep, alias=dict(ALIAS), cams=cams)
    return _attach(out, cams, late)


DESCRIPTION = """About eleven and a half thousand years ago, on a hilltop in southeast Turkey, people with no pottery, no metal and no farm animals raised stone giants with arms, hands and belts. Who were they, how do we know when, and what were these rings of pillars for?

We weigh the two boldest claims about Göbekli Tepe, survivors of a lost Ice Age civilisation and a comet strike recorded on the Vulture Stone, against the excavation reports, the radiocarbon dates and the new finds from its sister sites in the Stone Hills. Verdict on the bold claims: Awaiting evidence.

Chapters
{chapters}

Sources
Schmidt 2012, Göbekli Tepe: A Stone Age Sanctuary in South-Eastern Anatolia (ex oriente, Berlin)
Peters & Schmidt 2004, Anthropozoologica 39(1): 179-218
Dietrich & Schmidt 2010, Neo-Lithics 2/10: 82-83 (radiocarbon date from the wall plaster of Enclosure D)
Dietrich, Heun, Notroff, Schmidt & Zarnkow 2012, Antiquity 86: 674-695, doi:10.1017/S0003598X00047840
Dietrich, Köksal-Schmidt, Notroff & Schmidt 2013, Neo-Lithics 1/13 (establishing a radiocarbon sequence for Göbekli Tepe)
Herrmann & Schmidt 2012, in Klimscha et al. (eds), Wasserwirtschaftliche Innovationen im archäologischen Kontext (water at Göbekli Tepe)
Dietrich L., Meister, Dietrich O., Notroff, Kiep, Heeb, Beuger & Schütt 2019, PLOS ONE 14(5): e0215214, doi:10.1371/journal.pone.0215214
Clare 2020, e-Forschungsberichte des DAI 2020(2), doi:10.34780/efb.v0i2.1012
Kinzel, Clare & Sönmez 2020, Istanbuler Mitteilungen 70: 9-45, doi:10.34780/n42qpb15
Haklay & Gopher 2020, Cambridge Archaeological Journal 30(2): 343-357, doi:10.1017/S0959774319000660
Karul 2021, Türk Arkeoloji ve Etnografya Dergisi 82 (buried buildings at Pre-Pottery Neolithic Karahantepe)
Özdoğan 2022, Antiquity 96(390): 1599-1605, doi:10.15184/aqy.2022.125
Sweatman & Tsikritsis 2017, Mediterranean Archaeology and Archaeometry 17(1) (decoding Göbekli Tepe with archaeoastronomy)
Notroff, Dietrich O., Clare, Dietrich L., Schlindwein, Kinzel, Lelek-Tvetmarken & Sönmez 2017, Mediterranean Archaeology and Archaeometry 17(2): 57-63 (More than a vulture)
Sweatman & Tsikritsis 2017, Mediterranean Archaeology and Archaeometry 17(2) (comment on More than a vulture)
Sweatman 2024, Time and Mind, doi:10.1080/1751696X.2024.2373876
Holliday et al. 2023, Earth-Science Reviews 247: 104502, doi:10.1016/j.earscirev.2023.104502
Sweatman, Powell, West & Young 2024, Airbursts and Cratering Impacts 2(1) (rebuttal of Holliday et al.)
Hancock 2015, Magicians of the Gods (Coronet, London)
Dietrich O. 2016, The Tepe Telegrams (DAI Göbekli Tepe project blog): the site's rediscovery (2 June), the quarries (3 May), dating Göbekli Tepe (22 June)
Notroff 2017, The Tepe Telegrams (DAI Göbekli Tepe project blog): a sanctuary, or so fair a house? (24 January); the response to Sweatman and Tsikritsis (21 April, 3 July)
University of Edinburgh 2017, press release on Sweatman & Tsikritsis (Pillar 43 as a memorial to a comet strike)
Taş Tepeler project 2025, site descriptions of Göbeklitepe and Karahantepe (Şanlıurfa Neolithic Research Project)
Austrian Archaeological Institute (ÖAW) 2025, Geoarchaeology at Göbeklitepe, project report (first fieldwork, September to October 2025)
Archaeology (Archaeological Institute of America) news, 20 August 2026: dwellings detected near monuments at Göbekli Tepe (geophysical survey, Karul)"""


def EPISODES():
    return [lf_gobekli()]
