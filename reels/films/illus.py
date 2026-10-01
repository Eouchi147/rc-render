"""Small drawing helpers for the mural scenes (all in frame units: 1000 x 1778, captions live below y = 1480)."""
import math, random

BONE, INK, AMBER, SEA, RED, GREEN, BLUE, LILAC = "#f5ecdc", "#1a1511", "#e8b87a", "#3f86a8", "#ff8a7a", "#8fd9b0", "#9fd0ff", "#c9c1ee"
AU = "#e8c35a"


def ellipse(cx, cy, rx, ry, n=36, a0=0, a1=360):
    return [[round(cx + rx * math.cos(math.radians(a)), 1), round(cy + ry * math.sin(math.radians(a)), 1)] for a in [a0 + (a1 - a0) * k / n for k in range(n + 1)]]


def oval(cx, cy, rx, ry, fill, c="none", w=0, op=1, at=0, **kw):
    e = {"k": "poly", "p": ellipse(cx, cy, rx, ry)[:-1], "fill": fill, "c": c, "w": w, "curve": True, "in": at}
    if op != 1:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def label(x, y, t, at=0, c=BONE, size=30, a="middle", st="small", **kw):
    e = {"k": "label", "x": x, "y": y, "t": t, "st": st, "c": c, "size": size, "a": a, "in": at}
    e.update(kw)
    return e


def person(x, y, h=90, at=0, c="#e8d6b8", fx="rise"):
    return {"k": "person", "x": x, "y": y, "h": h, "t": False, "color": c, "in": at, "fx": fx}


def balls(cx, base_y, rows=8, r=12, at=0, step=.03, fill="#cbbca8", c="#8a7a66"):
    """A cone of stone balls, built bottom row first."""
    out, k = [], 0
    for row in range(rows):
        n = rows - row
        for j in range(n):
            x = cx + (j - (n - 1) / 2) * r * 2.1
            y = base_y - row * r * 1.75
            out.append({"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": r, "fill": fill, "c": c, "w": 1.5, "in": round(at + step * k, 2), "fx": "pop"})
            k += 1
    return out


def arrow(p, at=0, c=AMBER, w=3, style="known", dur=1.0, curve=True):
    return {"k": "arrow", "p": p, "c": c, "w": w, "style": style, "fx": "draw", "dur": dur, "in": at, "curve": curve}


def line(p, at=0, c=BONE, w=3, style="known", dur=None, curve=False, draw=True, op=None):
    e = {"k": "line", "p": p, "c": c, "w": w, "style": style, "in": at, "curve": curve}
    if draw:
        e.update(fx="draw", dur=dur or 1.0)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def glow(x, y, r=120, at=0, op=.6, kind="lamp"):
    return {"k": "glow", "x": x, "y": y, "r": r, "kind": kind, "op": op, "keepop": True, "in": at}


def tri(x, y, s=14, rot=0, fill="#9aa0a8", at=0):
    pts = []
    for k in range(3):
        a = math.radians(rot + 90 + k * 120)
        pts.append([round(x + s * math.cos(a), 1), round(y - s * math.sin(a), 1)])
    return {"k": "poly", "p": pts, "fill": fill, "c": "none", "w": 0, "in": at, "fx": "pop"}


def tooth(x, y, h=30, at=0, rot=0):
    return {"k": "rect", "x": x - h * .18, "y": y - h / 2, "w": h * .36, "h": h, "r": h * .18, "fill": "#efe6d2", "c": "#b8a888", "sw": 1.2, "in": at, "fx": "pop"}


def ring(cx, cy, r, at=0, c=AMBER, w=3, style="known", dur=1.0):
    return {"k": "circle", "x": cx, "y": cy, "r": r, "fill": "none", "c": c, "w": w, "style": style, "in": at, "fx": "draw", "dur": dur}


def dot(x, y, r=6, fill=BONE, at=0, fx="pop", op=None):
    e = {"k": "circle", "x": x, "y": y, "r": r, "fill": fill, "c": "none", "w": 0, "in": at, "fx": fx}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def box(x, y, w, h, fill, c="none", sw=0, r=6, at=0, op=None, fx=None, **kw):
    e = {"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": r, "fill": fill, "c": c, "sw": sw, "in": at}
    if op is not None:
        e.update(op=op, keepop=True)
    if fx:
        e["fx"] = fx
    e.update(kw)
    return e


def strike(x0, y0, x1, y1, at=0, c=RED, w=6):
    return {"k": "line", "p": [[x0, y0], [x1, y1]], "c": c, "w": w, "fx": "draw", "dur": .5, "in": at}


def question(x, y, at=0, size=110, c=LILAC):
    return [glow(x, y - 30, 130, at, .55), label(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def scatter(n, x0, x1, y0, y1, seed=1):
    r = random.Random(seed)
    return [(round(r.uniform(x0, x1), 1), round(r.uniform(y0, y1), 1)) for _ in range(n)]
