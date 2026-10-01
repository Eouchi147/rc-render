"""Legacy films rebuilt at the new standard, File 05 · Under Giza:
   05.01 Pillars under Khafre?   (the 648-metre radar claim, the real muon discoveries, the retraction)
   05.02 The door inside the Great Pyramid   (Upuaut's door, the stone behind it, the red marks, the record)
Each film is a base spec of drawn scenes (khafre_pillars(), sealed_door()) and one continuous take (the _m() versions,
see mural.py). Honesty in the line: solid = measured, dashed = inferred, dotted = claimed. Drawings are schematic;
depths, heights and lengths said aloud are drawn to scale where a scale is shown."""
import math, copy
from f05 import EP, B
from films import like, _topo
from giza import Section, BASE, SLOPE
from illus import line, arrow, glow, label, dot, box, ring, strike, question, person, oval, ellipse, BLUE, BONE, AMBER, RED, LILAC, GREEN

COP = "#c8743c"          # copper
LIME = "#d8c4a0"         # dressed limestone
INK = "#0d0b09"


def _poly(p, fill, c="none", w=0, at=0, **kw):
    e = {"k": "poly", "p": [[round(x, 1), round(y, 1)] for x, y in p], "fill": fill, "c": c, "w": w, "in": at}
    e.update(kw)
    return e


def _grp(els, tr, at=0, **kw):
    e = {"k": "group", "tr": tr, "els": els, "in": at}
    e.update(kw)
    return e


def _strike(x0, y0, x1, y1, at=0, c=RED, w=6):
    """A strike that fades in (a drawn one shows its round end cap as a dot before it starts)."""
    return {"k": "line", "p": [[x0, y0], [x1, y1]], "c": c, "w": w, "in": at, "dur": .35}


def _check(x, y, s, at, c=GREEN, w=5):
    """A tick mark, drawn."""
    return line([[x - s, y], [x - s * .35, y + s * .65], [x + s, y - s * .75]], at, c, w, dur=.5)


def _paper(x, y, w, h, at, fill="#e9dcc4", c="#fff6e6", fx="pop", rows=5, ink="#6b5a48", **kw):
    """A sheet of paper with a few ruled lines (no readable text)."""
    out = [box(x, y, w, h, fill, c, 2, 6, at, fx=fx, **kw)]
    for r in range(rows):
        yy = y + h * (.22 + .14 * r)
        out.append(line([[x + w * .14, yy], [x + w * (.86 if r % 3 != 2 else .6), yy]], at + .05, ink, 3, draw=False, op=.7))
    return out


def _satellite(x, y, at, s=1.0):
    """A radar satellite: a body, two solar wings, a dish underneath."""
    return [box(x - 72 * s - 20 * s, y - 10 * s, 72 * s, 20 * s, "#3d5566", BLUE, 1.5, 2, at, fx="pop"),
            box(x + 20 * s, y - 10 * s, 72 * s, 20 * s, "#3d5566", BLUE, 1.5, 2, at, fx="pop")] + \
           [line([[x - 92 * s + 18 * s * k, y - 10 * s], [x - 92 * s + 18 * s * k, y + 10 * s]], at, "#9fd0ff", 1, draw=False, op=.6) for k in range(1, 4)] + \
           [line([[x + 20 * s + 18 * s * k, y - 10 * s], [x + 20 * s + 18 * s * k, y + 10 * s]], at, "#9fd0ff", 1, draw=False, op=.6) for k in range(1, 4)] + \
           [box(x - 20 * s, y - 16 * s, 40 * s, 32 * s, "#cfd6dc", BONE, 1.5, 4, at, fx="pop"),
            _poly([[x - 16 * s, y + 26 * s], [x + 16 * s, y + 26 * s], [x, y + 16 * s]], "#cfd6dc", BONE, 1.2, at, fx="pop")]


def _tv(cx, cy, w, at):
    """A television set (rounded case, screen); returns the elements and the screen rectangle."""
    h = w * .7
    sx, sy, sw, sh = cx - w * .42, cy - h * .38, w * .7, h * .76
    return [box(cx - w / 2, cy - h / 2, w, h, "#2a231c", "#c9ad85", 3, 22, at),
            box(sx, sy, sw, sh, "#1d2a33", "#9fd0ff", 1.5, 14, at),
            dot(cx + w * .38, cy - h * .16, 9, "#8c7152", at), dot(cx + w * .38, cy + h * .06, 9, "#8c7152", at)], (sx, sy, sw, sh)


def _robot(x, y, s, at, ang=0.0, op=None, fx="rise"):
    """LIB.robot (a small tracked survey robot with a lamp), optionally tilted to climb a slope (degrees, + = nose up)."""
    r = {"k": "lib", "k2": "robot", "x": x, "y": y, "s": s}
    if op is not None:
        r["op"] = op
    inner = {"k": "group", "tr": "rotate(%.1f %.1f %.1f)" % (-ang, x, y), "els": [r]}
    return {"k": "group", "els": [inner], "in": at, "fx": fx}         # the build-in moves the outer group, the tilt stays on the inner one


# ================================================================ 05.01 Pillars under Khafre?
GY, PX, KX = 460, 1.35, 500                  # the cutaway under Khafre: ground line, pixels per metre (to scale), pyramid centre
KH, KB = 143.5 * PX, 215.3 * PX / 2          # Khafre as built: 143.5 m high, 215.3 m base (Lehner 1997)


def _D(m):
    return round(GY + m * PX, 1)


def _khafre_cut(cam=(1.02, 500, 830), pyr_at=-1, pyr_fx=None):
    """Khafre's pyramid on the plateau, cut open to 700 m below: the ground to scale with the pyramid."""
    def pe(e):
        e = dict(e, **{"in": pyr_at})
        if pyr_fx:
            e["fx"] = pyr_fx
        return e
    els = [pe(_poly([[KX - KB, GY], [KX, GY - KH], [KX + KB, GY]], "url(#k-blocks)", "#f2dcb4", 2)),
           pe(_poly([[KX, GY - KH], [KX + KB, GY], [KX, GY]], "rgba(0,0,0,.28)")),
           pe(_poly([[KX - KB * .2, GY - KH * .8], [KX, GY - KH], [KX + KB * .2, GY - KH * .8]], "#efe0c2", op=.92))]
    return {"base": "section", "tod": "night", "ground": GY, "lx": 40, "cam": list(cam),
            "layers": [{"d": 0, "c": "#7a6248", "t": ""}, {"d": 26, "c": "#6a553f", "t": ""}, {"d": 300, "c": "#57473a", "t": ""}, {"d": 640, "c": "#463a2f", "t": ""}],
            "els": els}


def _kp_hook():
    """The hook: 648 m, straight down, under a pyramid (to scale)."""
    s = _khafre_cut(cam=(1.15, 500, 820), pyr_at=3.1, pyr_fx="rise")
    s["els"] += [label(660, _D(330) + 16, "648 m", .6, BONE, 56, "start", st="serif"),
                 arrow([[KX, GY + 6], [KX, _D(648)]], 1.3, BONE, 4, "known", 1.3, False),
                 line([[KX - 36, _D(648)], [KX + 36, _D(648)]], 2.5, BONE, 4, dur=.3),
                 glow(KX, _D(648), 120, 2.7, .55, "blue")]
    return s


def _kp_stack():
    """Four and a half Khafres, one below another: 646 m, the claim's depth."""
    els = []
    for k in range(4):
        y0, y1 = GY + KH * k, GY + KH * (k + 1)
        els.append(_poly([[KX - KB, y1], [KX, y0], [KX + KB, y1]], "rgba(242,220,180,.07)", BONE, 2, round(2.2 + .55 * k, 2), style="inferred", op=.8))
    y0 = GY + KH * 4
    els.append(_poly([[KX - KB / 2, y0 + KH / 2], [KX, y0], [KX + KB / 2, y0 + KH / 2]], "rgba(242,220,180,.07)", BONE, 2, 4.4, style="inferred", op=.8))
    els += [label(KX - KB - 18, _D(330) + 14, "× 4½", 4.9, AMBER, 46, "end", st="serif"),
            ring(745, _D(330) - 2, 92, 6.6, AMBER, 3, dur=.8)]
    return els


def _kp_claim():
    """The 2025 claim on a clean cut of the same ground, drawn in lilac dots (claimed): radar from orbit, eight shafts with paths
    spiralling round them, two giant cubes far below. The 648 m depth stays marked at the side."""
    s = _khafre_cut(cam=(1.15, 500, 820))
    s["els"] = [dict(e, **{"in": .1}) for e in s["els"]]
    s["els"] += [{"k": "dim", "x1": 880, "y1": GY + 4, "x2": 880, "y2": _D(648), "t": "", "c": "#cbbca8", "in": .2},
                 label(862, _D(330) + 12, "648 m", .3, "#cbbca8", 34, "end", st="serif")]
    sx, sy = 800, 330
    els = _satellite(sx, sy, 2.4) + [label(700, 298, "satellite radar", 2.8, BLUE, 30, "end")]
    els += [line([[sx - 10, sy + 26], [KX - 150, GY - 2]], 3.0, BLUE, 2, "inferred", .7), line([[sx + 4, sy + 26], [KX + 150, GY - 2]], 3.0, BLUE, 2, "inferred", .7)]
    for j, r in enumerate((70, 130, 190)):
        els.append({"k": "line", "p": [[round(sx + r * math.cos(math.radians(a)), 1), round(sy + 26 + r * .55 * math.sin(math.radians(a)), 1)] for a in range(105, 200, 8)],
                    "c": BLUE, "w": 2.4, "curve": True, "in": round(3.2 + .2 * j, 2), "fx": "draw", "dur": .5})
    els.append(glow(KX, GY, 190, 3.6, .4, "blue"))
    top, bot = GY + 10, _D(648) - 104
    for k in range(8):
        x = KX + (k - 3.5) * 30
        at = round(4.0 + .1 * k, 2)
        els.append(box(x - 8, top, 16, bot - top, "rgba(201,193,238,.12)", LILAC, 1.8, 3, at, style="claimed"))
        pts = [[round(x + 6.5 * math.sin(2 * math.pi * (y - top) / 34 + k), 1), y] for y in range(int(top) + 4, int(bot) - 2, 5)]
        els.append({"k": "line", "p": pts, "c": LILAC, "w": 1.6, "curve": True, "op": .75, "keepop": True, "in": round(5.4 + .08 * k, 2)})
    for j, cx in enumerate((KX - 58, KX + 58)):
        x0, x1, y0, y1, d = cx - 48, cx + 48, bot + 6, bot + 102, 18
        at = round(7.6 + .3 * j, 2)
        els += [box(x0, y0, 96, 96, "rgba(201,193,238,.12)", LILAC, 2.4, 2, at, style="claimed"),
                _poly([[x0, y0], [x0 + d, y0 - d * .7], [x1 + d, y0 - d * .7], [x1, y0]], "rgba(201,193,238,.18)", LILAC, 2, at, style="claimed"),
                _poly([[x1, y0], [x1 + d, y0 - d * .7], [x1 + d, y1 - d * .7], [x1, y1]], "rgba(201,193,238,.08)", LILAC, 2, at, style="claimed")]
    els += [label(KX + 150, _D(648) - 30, "claimed", 8.4, LILAC, 32, "start")]
    s["els"] += els
    return s


def _kp_plateau():
    """Giza as a diorama, true size and place, seen from the south-west: Khafre in the middle, the Great Pyramid behind it."""
    from iso3d import shot, giza, PLATEAU, project
    sh = shot(giza(town=False), cam=(1.1, 495, 900), s=.44, x=500, y=1000, az=-160, spin=0, el=.5, table=PLATEAU)
    cx, cy = project(sh, (-135, 0, 470), 0)
    iso = sh["els"][1]
    iso.update(x=round(1000 - cx, 1), y=round(1900 - cy, 1), **{"in": .1})     # the table centred in the panel
    kx, kz = -348.5, 344.7
    P = lambda x, y, z: [round(v, 1) for v in project(sh, (x, y, z), 0)]
    kt, gt, mt = P(kx, 143.5, kz), P(0, 146.6, 0), P(-581, 65.5, 738)
    sh["els"] += [glow(kt[0], kt[1] + 50, 150, 3.9, .5), label(kt[0], kt[1] - 34, "Khafre", 4.1, AMBER, 34),
                  label(gt[0], gt[1] - 30, "Great Pyramid", 5.3, BONE, 30)]
    return sh, P, (kx, kz)


def _kp_height(P, k):
    """Khafre's height as built, a dimension line beside it (vertical lines stay vertical in this projection)."""
    kx, kz = k
    b0, b1 = P(kx + 108, 0, kz + 108), P(kx + 108, 143.5, kz + 108)
    return [{"k": "dim", "x1": b0[0] + 56, "y1": b0[1], "x2": b1[0] + 56, "y2": b1[1], "t": "", "c": AMBER, "in": 4.4},
            label(b1[0] + 72, round((b0[1] + b1[1]) / 2 + 10, 1), "143 m", 4.7, AMBER, 32, "start")]


def _kp_radar():
    """How radar sees: a pulse goes down, its echo comes back, the delay gives the distance; from orbit, the surface and a few metres of dry sand."""
    gy = 930
    s = {"base": "section", "tod": "night", "ground": gy, "lx": 40, "cam": [1.0, 500, 860],
         "layers": [{"d": 0, "c": "#9c7d58", "t": ""}, {"d": 46, "c": "#6a553f", "t": ""}, {"d": 260, "c": "#57473a", "t": ""}], "els": []}
    sx, sy = 500, 380
    els = _satellite(sx, sy, .3, 1.15)
    for j, r in enumerate((90, 200, 320, 450)):
        els.append({"k": "line", "p": ellipse(sx, sy + 30, r * .9, r, 16, 58, 122), "c": BLUE, "w": 3, "curve": True, "in": round(5.4 + .3 * j, 2), "fx": "draw", "dur": .4})
    els += [label(268, 805, "pulse", 5.8, BLUE, 32, "end")]
    for j, r in enumerate((430, 320, 210)):
        els.append({"k": "line", "p": ellipse(sx, gy + 10, r * .9, r * .9, 16, 238, 302), "c": AMBER, "w": 3, "curve": True, "in": round(7.0 + .3 * j, 2), "fx": "draw", "dur": .4})
    els += [label(722, 596, "echo", 7.4, AMBER, 32, "start")]
    cx, cy = 170, 420                                       # a stopwatch times the round trip
    els += [ring(cx, cy, 46, 6.4, BONE, 3, dur=.5), box(cx - 9, cy - 64, 18, 12, BONE, r=3, at=6.4),
            line([[cx, cy], [cx, cy - 34]], 6.6, AMBER, 3, draw=False), {"k": "line", "p": ellipse(cx, cy, 34, 34, 12, -90, 60), "c": AMBER, "w": 4, "curve": True, "in": 6.8, "fx": "draw", "dur": 1.8}]
    els += [arrow([[860, sy + 30], [860, gy - 6]], 8.6, BONE, 3, "known", .8, False), arrow([[860, gy - 6], [860, sy + 30]], 8.6, BONE, 3, "known", .8, False),
            label(848, 720, "distance", 9.2, BONE, 30, "end")]
    els += [line([[80, gy], [920, gy]], 11.2, "#ffe2a8", 4, dur=.9), glow(500, gy, 260, 11.4, .35),
            box(80, gy + 2, 840, 44, "rgba(159,208,255,.30)", r=2, at=13.6, fx="fill", dur=.8),
            label(120, gy + 92, "a few metres of dry sand", 14.2, BLUE, 30, "start")]
    s["els"] = els
    return s


def _kp_deeper():
    """The team's answer: a new way of processing the echoes sees far deeper (claimed)."""
    return [arrow([[500, 990], [500, 1400]], 3.2, LILAC, 4, "claimed", 1.2, False), label(530, 1240, "far deeper?", 4.0, LILAC, 34, "start")]


def _kp_muon():
    """The Great Pyramid cut open: muons rain through the stone; stone stops some, a hollow lets more through."""
    S = Section(s=3.6, cx=500, gy=1150)
    bv, bvc = S.big_void()
    sky = {"base": "section", "tod": "night", "ground": 1150, "far": [[870, 120]], "cam": [1.18, 500, 830],
           "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 60, "c": "#4d3e30", "t": ""}]}
    body = dict(S.body(), **{"in": .1})
    shade = {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": .1}
    inner = [dict(e, **{"in": .3}) for e in S.els()]
    els = [body, shade] + inner + [label(500, 580, "Great Pyramid", 1.0, BONE, 32)]
    els += [{"k": "rays", "x0": 120, "x1": 880, "y0": 300, "y1": 1260, "n": 90, "spread": .3, "c": BLUE, "in": 4.6, "fx": "draw", "dur": 2.2},
            label(880, 360, "muons", 5.8, BLUE, 34, "end")]
    stops = [(250, 1010), (330, 930), (410, 820), (640, 880), (720, 990), (790, 1080)]
    els += [dot(x, y, 8, RED, round(8.2 + .12 * k, 2)) for k, (x, y) in enumerate(stops)]
    for j, dx in enumerate((-14, 0, 14)):
        els.append(line([[bvc[0] + dx - 70, 330], [bvc[0] + dx, bvc[1]], [bvc[0] + dx + 26, 1150]], round(10.0 + .15 * j, 2), "#cfe6ff", 3.2, dur=.8))
    els += [glow(bvc[0], bvc[1], 120, 10.8, .7, "blue")]
    s = dict(sky, els=els)
    return s, S, bv, bvc


def _kp_void(S, bv, bvc):
    """2017: the void, at least 30 m, peer reviewed; 2023: a small corridor behind the north face, then a camera sees it."""
    nfc, nfcc = S.nfc()
    els = [dict(bv, **{"in": 2.0}), glow(bvc[0], bvc[1], 110, 2.2, .8, "blue"),
           label(bvc[0] - 30, bvc[1] - 70, "void · 30 m +", 3.4, "#cfe6ff", 32), _check(bvc[0] + 140, bvc[1] - 82, 16, 6.5)]
    els += [dict(nfc, **{"in": 10.0}), glow(nfcc[0], nfcc[1], 60, 10.2, .8, "blue"),
            label(96, nfcc[1] - 70, "corridor · 2023", 10.6, "#cfe6ff", 30, "start")]
    els += [line([[70, 1135], [100, 1110], [130, 1092], [nfcc[0] - 10, nfcc[1] + 2]], 13.0, "#c9ad85", 5, dur=1.2, curve=True),
            dot(nfcc[0] - 8, nfcc[1] + 2, 7, BLUE, 14.2), glow(nfcc[0] + 10, nfcc[1], 80, 14.4, .7, "lamp"),
            label(nfcc[0] + 40, nfcc[1] + 66, "seen", 15.0, GREEN, 32, "start"), _check(nfcc[0] + 128, nfcc[1] + 50, 14, 15.2)]
    return els


def _kp_review():
    """Peer review drawn as a gate of three experts; the Khafre claim never went through it."""
    els = []
    # the claim: a sketch of the shafts on a lilac card, top left; it stops short of the journal
    cx0, cy0 = 110, 360
    els += [box(cx0, cy0, 200, 240, "rgba(201,193,238,.10)", LILAC, 2.5, 8, .3, style="claimed")]
    els += [line([[cx0 + 40 + 17 * k, cy0 + 40], [cx0 + 40 + 17 * k, cy0 + 170]], .5, LILAC, 2, "claimed", draw=False) for k in range(8)]
    els += [box(cx0 + 46, cy0 + 176, 46, 40, "none", LILAC, 2, 2, .6, style="claimed"), box(cx0 + 108, cy0 + 176, 46, 40, "none", LILAC, 2, 2, .6, style="claimed"),
            label(cx0 + 100, cy0 + 290, "Khafre claim", .8, LILAC, 30)]
    # the journal: a bound volume, top right
    jx, jy = 660, 350
    els += [box(jx, jy, 220, 260, "#5a3e2a", "#e8b87a", 2.5, 8, 1.4), box(jx + 16, jy + 16, 188, 228, "#6e4c33", "#c9a070", 1.5, 6, 1.4),
            label(jx + 110, jy + 300, "journal", 1.6, AMBER, 30)]
    els += [arrow([[cx0 + 210, cy0 + 120], [420, cy0 + 110], [520, cy0 + 120]], 2.0, LILAC, 3, "claimed", .6),
            _strike(540, cy0 + 90, 590, cy0 + 150, 2.6, RED, 6), _strike(590, cy0 + 90, 540, cy0 + 150, 2.7, RED, 6)]
    # peer review: three experts; a study goes through, checked three ways, and lands in the journal
    gy = 1110
    els += [label(500, 800, "peer review", 3.2, AMBER, 32)]
    for k, x in enumerate((380, 500, 620)):
        els += [person(x, gy, 170, round(3.6 + .15 * k, 2), "#e8d6b8")]
    els += _paper(96, 920, 130, 170, 5.4, fill="#cfe6ff", c=BLUE, ink="#3d5566")
    els += [arrow([[236, 1030], [380, 1040], [620, 1040], [736, 1030]], 6.0, BLUE, 3, "known", 1.2)]
    els += _paper(750, 920, 130, 170, 7.0, fill="#cfe6ff", c=BLUE, ink="#3d5566")
    for k, (x, at) in enumerate(((380, 7.9), (500, 8.6), (620, 9.3))):
        els.append(_check(x, 860, 16, at))
    els += [ring(815, 1005, 90, 11.0, GREEN, 4, dur=.7), _check(815, 1005, 30, 11.8, GREEN, 7)]
    return els


def _kp_retract():
    """August 2026: the team's earlier study, inside the journal, is struck out: withdrawn."""
    jx, jy = 660, 350
    els = [box(jx + 40, jy + 46, 140, 172, "#f2c98e", "#fff6e6", 2, 6, 2.6, fx="pop")]
    els += [line([[jx + 58, jy + 46 + 172 * (.22 + .14 * r)], [jx + 162, jy + 46 + 172 * (.22 + .14 * r)]], 2.7, "#8a6a48", 3, draw=False, op=.7) for r in range(5)]
    els += [label(jx + 110, jy - 18, "earlier study", 3.2, AMBER, 30),
            _strike(jx + 30, jy + 228, jx + 190, jy + 36, 6.2, RED, 8), _strike(jx + 30, jy + 36, jx + 190, jy + 228, 6.4, RED, 8),
            label(jx + 110, jy + 356, "withdrawn", 7.5, RED, 34)]
    return els


def _kp_tests():
    """What would settle it: a drill core from 648 m, a seismic survey, open data. Dashed: not done."""
    s = _khafre_cut(cam=(1.02, 500, 850))
    s["els"] = [dict(e, **{"in": .1}) for e in s["els"]]
    top, bot = GY + 10, _D(648) - 104
    ghost = [{"k": "line", "p": [[KX + (k - 3.5) * 30, top], [KX + (k - 3.5) * 30, bot]], "c": LILAC, "w": 2, "style": "claimed", "op": .35, "keepop": True, "in": .2} for k in range(8)]
    ghost += [box(cx - 48, bot + 6, 96, 96, "none", LILAC, 2, 2, .2, style="claimed", op=.35) for cx in (KX - 58, KX + 58)]
    s["els"] += ghost
    els = []
    # the drill: a rig on the surface, a dashed string down 648 m, a core of real rock coming up
    rx = 790
    els += [line([[rx - 40, GY], [rx, GY - 150], [rx + 40, GY]], 2.0, "#cbbca8", 4, dur=.6), line([[rx - 24, GY - 60], [rx + 24, GY - 60]], 2.2, "#cbbca8", 3, dur=.3),
            line([[rx, GY], [rx, _D(648)]], 2.6, AMBER, 4, "inferred", 1.8), label(rx - 10, GY - 172, "drill core", 2.4, AMBER, 30)]
    els += [box(rx + 46, GY - 120, 26, 110, "#a88a64", "#f2dcb4", 2, 12, 4.2, fx="rise"), arrow([[rx + 59, _D(300)], [rx + 59, GY + 20]], 3.8, AMBER, 3, "inferred", .8, False)]
    # the seismic survey: a thump, waves down, echoes back up to listening stations
    tx = 225
    els += [box(tx - 34, GY - 40, 68, 40, "#8c7152", "#f2dcb4", 2, 6, 6.2, fx="pop"), label(tx, _D(200), "seismic", 6.6, BLUE, 30)]
    for j, r in enumerate((60, 115, 170)):
        els.append({"k": "line", "p": ellipse(tx, GY, r, r, 14, 40, 140), "c": BLUE, "w": 2.4, "style": "inferred", "curve": True, "in": round(7.0 + .35 * j, 2), "fx": "draw", "dur": .6})
    for k, gx in enumerate((300, 335)):
        els += [_poly([[gx - 9, GY], [gx + 9, GY], [gx, GY - 16]], BLUE, at=round(9.6 + .2 * k, 2), fx="pop"),
                arrow([[tx + 30 + 30 * k, GY + 150], [gx, GY + 6]], round(9.8 + .2 * k, 2), BLUE, 2, "inferred", .5, False)]
    # open data: a file, shared outward
    fx_, fy = 120, 362
    els += [box(fx_ - 30, fy - 38, 60, 76, "#e9dcc4", "#fff6e6", 2, 6, 13.0, fx="pop"), glow(fx_, fy, 90, 13.2, .45)]
    for k, a in enumerate((215, 250, 290, 325)):
        els.append(arrow([[round(fx_ + 46 * math.cos(math.radians(a)), 1), round(fy + 46 * math.sin(math.radians(a)), 1)],
                          [round(fx_ + 80 * math.cos(math.radians(a)), 1), round(fy + 80 * math.sin(math.radians(a)), 1)]],
                         round(13.4 + .12 * k, 2), AMBER, 2.5, "inferred", .4, False))
    els += [label(fx_ + 46, fy + 22, "open data", 13.6, AMBER, 30, "start")]
    return s, els


def _kp_paper():
    """Until then, the pillars stay on paper: a sheet laid over the ground, the claim sketched on it in ink."""
    cx, cy, w, h, ang = 500, 905, 380, 537, math.radians(-3)
    R = lambda x, y: [round(cx + (x - cx) * math.cos(ang) - (y - cy) * math.sin(ang), 1), round(cy + (x - cx) * math.sin(ang) + (y - cy) * math.cos(ang), 1)]
    x0, y0 = cx - w / 2, cy - h / 2
    sheet = [R(x0, y0), R(x0 + w, y0), R(x0 + w, y0 + h), R(x0, y0 + h)]
    ink, at = "#4a3a5a", 1.8
    els = [_poly([[p[0] + 10, p[1] + 14] for p in sheet], "rgba(0,0,0,.35)", at=at, fx="pop"), _poly(sheet, "#efe4cf", "#fff6e6", 2, at, fx="pop")]
    els += [line([R(cx - 70, cy - 150), R(cx, cy - 210), R(cx + 70, cy - 150)], at + .3, ink, 3, dur=.4), line([R(cx - 150, cy - 150), R(cx + 150, cy - 150)], at + .4, ink, 2, dur=.4)]
    for k in range(8):
        x = cx - 35 + 10 * k
        els.append(line([R(x, cy - 140), R(x, cy + 120)], round(at + .5 + .05 * k, 2), ink, 2.4, "claimed", draw=False))
    for x in (cx - 40, cx + 4):
        bx = [R(x, cy + 126), R(x + 36, cy + 126), R(x + 36, cy + 162), R(x, cy + 162)]
        els.append(_poly(bx, "none", ink, 2.4, at + .9, style="claimed"))
    return els


def _globe(cx, cy, R, lon0, lat0, tol=1.6):
    """Orthographic land outlines (points over the horizon pinned to the rim); returns SVG path strings and a projector."""
    l0, p0 = math.radians(lon0), math.radians(lat0)

    def pr(lon, lat):
        l, p = math.radians(lon), math.radians(lat)
        c = math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)
        x = R * math.cos(p) * math.sin(l - l0)
        y = R * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0))
        if c < 0:
            d = math.hypot(x, y) or 1
            x, y = x / d * R, y / d * R
        return cx + x, cy - y, c
    out = []
    for poly in _topo():
        ring_ = poly[0]
        P = [pr(lo, la) for lo, la in ring_]
        if all(q[2] < 0 for q in P) or len(P) < 4:
            continue
        pts, last = [], None
        for x, y, c in P:
            if last and abs(x - last[0]) < tol and abs(y - last[1]) < tol:
                continue
            pts.append((round(x, 1), round(y, 1))); last = (x, y)
        if len(pts) > 3:
            out.append("M" + "L".join(f"{x} {y}" for x, y in pts) + "Z")
    return out, pr


def _kp_globe():
    cx, cy, R = 500, 860, 390
    land, pr = _globe(cx, cy, R, 28, 22)
    els = [glow(cx, cy, R + 140, .1, .35, "blue"), oval(cx, cy, R, R, "#1d3a4a", "#9fd0ff", 2, at=.1),
           {"k": "map", "land": land, "landc": "#4a3c2e", "in": .2}]
    for lat in (-30, 0, 30, 60):
        pts = [pr(lo, lat) for lo in range(-62, 120, 6)]
        pts = [[round(x, 1), round(y, 1)] for x, y, c in pts if c > .02]
        if len(pts) > 2:
            els.append({"k": "line", "p": pts, "c": "#9fd0ff", "w": 1, "op": .25, "keepop": True, "curve": True, "in": .3})
    gx, gy_, _ = pr(31.13, 29.98)
    els += [{"k": "pin", "x": round(gx, 1), "y": round(gy_, 1), "r": 9, "c": AMBER, "in": .7}, ring(round(gx, 1), round(gy_, 1), 34, 1.4, AMBER, 3, dur=.6),
            label(round(gx, 1) + 42, round(gy_, 1) - 30, "Giza", .9, AMBER, 32, "start")]
    spots = [(-60, 10), (-100, 40), (10, 50), (35, -5), (80, 30), (105, 15), (-10, 15), (55, 50), (20, -25), (-45, -10)]
    k = 0
    for lo, la in spots:
        x, y, c = pr(lo, la)
        if c > .35:
            els.append(label(round(x, 1), round(y, 1), "?", round(3.0 + .18 * k, 2), LILAC, 44, st="serif", op=.85))
            k += 1
    return {"base": "dark", "stars": 120, "cam": [1.0, 500, 860], "els": els}


def _kp_parts():
    hook = _kp_hook()
    pl, P, k = _kp_plateau()
    muon, S, bv, bvc = _kp_muon()
    rev = {"base": "dark", "cam": [1.1, 500, 790], "els": _kp_review()}
    tests, tests_els = _kp_tests()
    kx, ky = P(k[0], 70, k[1])
    return dict(hook=hook, plateau=pl, height=_kp_height(P, k), Kpos=(kx, ky), stack=_kp_stack(), claim=_kp_claim(), radar=_kp_radar(), deeper=_kp_deeper(),
                muon=muon, void=_kp_void(S, bv, bvc), rev=rev, retract=_kp_retract(), tests=tests, tests_els=tests_els, paper=_kp_paper(), globe=_kp_globe())


def khafre_pillars():
    p = _kp_parts()
    kx, ky = p["Kpos"]
    s0 = p["hook"]
    s1 = p["plateau"]
    s2 = like(s0, cam=[1.15, 500, 820], add=p["stack"])
    s3 = p["claim"]
    s4 = dict(p["radar"], els=p["radar"]["els"] + p["deeper"])
    s5 = dict(p["muon"], els=p["muon"]["els"] + p["void"])
    s6 = dict(p["rev"], els=p["rev"]["els"] + p["retract"])
    s7 = dict(p["tests"], els=p["tests"]["els"] + p["tests_els"] + p["paper"])
    s8 = p["globe"]
    shots = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
    beats = [
        B("hook", 0, ["[d:intrigue][k:648 METRES DOWN][sfx:boom][act:stating the claim, deadpan]{648|Six hundred and forty-eight} metres. [act:letting it land][tune:fall]Straight ^*down*. [act:the kicker][tune:fall]Under a ^*pyramid*.",
                      "[d:tension][sfx:rumble][act:dry, knowing]That's the ^claim, about a pyramid in ^Egypt. [act:intrigued, drawing them in][tune:level]What happened ^*next*... [act:quiet promise][tune:fall]is the ^real story."], cut=False),
        B("world", 1, ["[d:calm][k:GIZA][act:plain, placing it]This is ^Giza, in Egypt: the pyramid credited to the pharaoh ^Khafre, beside the Great ^Pyramid.",
                       "[d:calm][p:0.93][act:a touch of awe]At least four and a half ^*thousand* years old, and about a hundred and forty-three metres ^tall when new."]),
        B("collision", 2, ["[d:build][k:THE CLAIM][p:0.93][act:doing the sum, vivid]Now stack four and a half of those pyramids, one below another, down into the ^rock. [act:letting it land][tune:fall]That's how deep the claim ^goes.",
                           "[d:build][go:3|1.6][act:reporting the announcement, brisk]In {2025|twenty twenty-five}, an Italian team said satellite ^radar had found [sfx:whoosh]^*eight* shafts down there, spiralling ^deep. [act:the big claim, eyebrows up]And far below, [sfx:hit]two giant ^*cubes*.",
                           "[d:aside][p:1.06][act:dry, amused]Not bad, for a survey@noun that never touched the ^*ground*."]),
        B("collision", 4, ["[d:build][k:HOW RADAR SEES][act:fair, curious][tune:rise]Can radar from space see that ^deep? [p:0.93][act:explaining, clear]Radar works like an ^echo: send a pulse, time its ^return, and you know how far it ^travelled. [act:patient, the limit]From orbit, it sees the ^surface, and in very dry sand, a few metres ^below.",
                           "[d:build][act:fair, their side]The team says its new way of processing echoes sees far ^*deeper*. [p:0.93][act:even, the rule]But a new tool earns trust one way: it gets ^tested, on something we can ^check."]),
        B("cost", 5, ["[d:wonder][k:WHAT'S REAL][act:fair, what is real]And hidden spaces at Giza ^*are* real. [p:0.93][act:explaining, a spark of wonder]Cosmic rays hitting our air make [sfx:shimmer]^muons, particles that rain through almost ^everything. [act:the analogy, clear]Stone stops some. [act:the payoff]An empty space lets more ^through, like an ^X-ray.",
                      "[d:wonder][act:precise, a little wonder]In {2017|twenty seventeen}, muons revealed a ^void, at least ^*thirty* metres long, inside the Great ^Pyramid. [stamp:NATURE · 2017|gold][act:firm, a credential]Peer ^reviewed. [act:the test, leaning in]Then in {2023|twenty twenty-three}, they pointed to a small ^corridor behind its north ^face. [act:quiet, careful]A camera slid in... [act:quiet satisfaction][tune:fall]and there it ^was."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][p:0.96][act:the turn][tune:rise]The Khafre ^shafts? [act:plain, sober][tune:fall]No peer-reviewed ^paper. [p:0.93][act:explaining, simple]Peer review: other experts check a study before a journal prints it, the method, the data, the ^sums. [act:light, an everyday picture]Like a referee checking a goal, before it ^counts.",
                          "[d:reveal][act:sober, a heavy fact]And in August {2026|twenty twenty-six}, the team's earlier pyramid study, in the journal Remote Sensing, was [stamp:RETRACTED · AUG 2026|red]^*retracted*. [act:explaining, plain]The journal ^withdrew it. [act:quiet, firm][tune:fall]It no longer stands in the ^record@noun."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:naming what is missing][tune:level]What would settle it? [act:explaining, brisk]A drill ^core: real rock, brought up from that ^depth. [act:same pace, the next one][tune:level]A seismic ^survey@noun: sound sent into the ground, echoes timed, like a ship mapping the ^seabed. [act:the last one][tune:fall]And open ^data, for anyone to ^check.",
                     "[d:verdict][act:the verdict, a small smile][tune:level]Until then, the pillars stay... [act:gently final][tune:fall]on ^*paper*. [act:the verdict, level][tune:fall]^Awaiting evidence.",
                     "[d:wonder][p:0.95][go:8|2.6][act:widening out, curious][tune:rise]And ^Giza? [act:warm wonder]One dot, on a planet full of ^*open* questions."]),
    ]
    sources = "Morishima et al. 2017, Nature · Procureur et al. 2023, Nature Communications · Remote Sensing retraction notice, 2026"
    post = "648 metres of 'pillars' under a pyramid? The claim, the real muon discoveries, and the retraction. Full case and sources: Residual Continuum."
    return EP("khafre-pillars", "05.01", "Pillars under Khafre?", "khafre-radar", "unsupported", "A vast structure 648 metres under Khafre's pyramid?",
              "648 metres *under* a pyramid?", beats, shots, sources, post, ["#Giza", "#Khafre", "#Pyramids", "#AncientEgypt", "#WeighItYourself"])


def khafre_pillars_m():
    """Pillars under Khafre as one continuous take: the 648-metre plunge drawn to scale under the pyramid, Giza as a model, four and a half
    pyramids stacked down to reach the claim's depth, the claim in lilac dots on a clean cut, how radar's echo works and how deep it reaches,
    the muon X-ray that was tested and seen, a gate of peer review the claim never passed, a study withdrawn, the tests still undone,
    the claim left on paper, Giza one dot on a globe."""
    from mural import remix
    p = _kp_parts()
    ep = khafre_pillars()
    kx, ky = p["Kpos"]
    scenes = {0: p["hook"], 1: p["plateau"], 3: p["claim"], 4: p["radar"], 5: p["muon"], 6: p["rev"],
              7: dict(p["tests"], els=p["tests"]["els"] + p["tests_els"]), 8: p["globe"]}
    return remix(ep, scenes=scenes, alias={2: 0},
                 beat_adds={2: (p["stack"], [1.15, 500, 820])},
                 line_adds={(1, 1): (p["height"], [1.45, kx - 17, ky - 15]),
                            (2, 2): ([glow(800, 330, 150, .4, .6, "blue"), ring(800, 330, 58, .5, BLUE, 2.5, dur=.6)], None),
                            (3, 1): (p["deeper"], None), (4, 1): (p["void"], None), (5, 1): (p["retract"], None),
                            (6, 1): (p["paper"], None)})


# ================================================================ 05.02 The door inside the Great Pyramid
def _shaft_view(cx, cy, W=760, n=7, kend=.38, tone=(214, 190, 150)):
    """Looking up a square stone shaft through a robot's camera: block joints, lamp light, the slab at the end (round view)."""
    els = []
    def sq(t):
        k = 1 - t * (1 - kend); w = W * k / 2
        return [[cx - w, cy - w], [cx + w, cy - w], [cx + w, cy + w], [cx - w, cy + w]]
    rs = [sq(i / n) for i in range(n + 1)]
    for i in range(n):
        a, b = rs[i], rs[i + 1]; f = 1 - i / n
        for j, (p, q) in enumerate(((0, 1), (1, 2), (2, 3), (3, 0))):
            lit = [.55, .72, .95, .62][j]
            c = tuple(int(v * (.22 + .78 * f * f) * lit) for v in tone)
            els.append({"k": "poly", "p": [a[p], a[q], b[q], b[p]], "fill": "rgb(%d,%d,%d)" % c, "c": "rgba(40,28,18,.85)", "w": 1.4 if i % 2 else 1, "op": 1, "in": -1})
    far = rs[-1]
    els.append({"k": "poly", "p": far, "fill": LIME, "c": "rgba(255,236,206,.7)", "w": 2, "in": -1, "id": "door"})
    els.append({"k": "poly", "p": [[far[0][0] + 12, far[0][1] + 12], [far[1][0] - 12, far[1][1] + 12], [far[2][0] - 12, far[2][1] - 12], [far[3][0] + 12, far[3][1] - 12]],
                "fill": "#e6d3b0", "c": "none", "w": 0, "in": -1, "op": .7})
    els.append({"k": "glow", "x": cx, "y": cy + 30, "r": 360, "kind": "lamp", "op": .32, "in": -1})
    els.append({"k": "circle", "x": cx, "y": cy, "r": 830, "c": "#0b0907", "w": 700, "op": 1, "in": -1})
    els.append({"k": "circle", "x": cx, "y": cy, "r": 482, "c": "rgba(255,226,168,.35)", "w": 2, "op": 1, "in": -1})
    return els, far


def _pins(cx, cy, at):
    """The two copper fittings on the slab's face (schematic)."""
    out = []
    for sgn in (-1, 1):
        x = cx + sgn * 72
        out += [line([[x, cy - 40], [x, cy - 96], [x + sgn * 16, cy - 108]], at, COP, 8, dur=.4), line([[x - 2, cy - 44], [x - 2, cy - 92]], at + .2, "#f4b27a", 2, draw=False, op=.8),
                glow(x, cy - 70, 50, at, .5)]
    return out


def _sd_hook():
    cx, cy = 500, 820
    els, far = _shaft_view(cx, cy)
    els += _pins(cx, cy, 1.0)
    els += [box(cx - 118, cy - 108, 248, 248, "none", BLUE, 3, 4, 5.6, style="inferred"), glow(cx + 6, cy + 16, 160, 5.8, .45, "blue")]
    els += question(cx, cy + 100, 7.6, 110)
    return {"base": "dark", "cam": [1.05, 500, 840], "els": els}


def _sd_section():
    """The Great Pyramid cut open; the Queen's Chamber and the narrow shaft climbing south from it to a stone door.
    Returns the panel, and the close-up additions (the shaft's mouth, sealed until 1872; no known way out)."""
    S = Section(s=3.6, cx=500, gy=1150)
    R = S.rooms()
    qx, qh = R["qc"]
    a = math.radians(39.5)
    p0, p1 = (qx + 2.6, 22.0), (qx + 4.6, 22.0)
    p2 = (p1[0] + 58 * math.cos(a), p1[1] + 58 * math.sin(a))
    u = (BASE - p2[0]) * math.tan(SLOPE) - p2[1]
    u = u / (math.sin(a) + math.cos(a) * math.tan(SLOPE))
    p3 = (p2[0] + u * math.cos(a), p2[1] + u * math.sin(a))
    P0, P1, P2, P3 = S.P(*p0), S.P(*p1), S.P(*p2), S.P(*p3)
    sky = {"base": "section", "tod": "night", "ground": 1150, "far": [[150, 110]], "cam": [1.2, 500, 900],
           "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 60, "c": "#4d3e30", "t": ""}]}
    els = [dict(S.body(), **{"in": .1}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": .1}] + [dict(e, **{"in": .3, "op": .75}) for e in S.els()]
    qc = S.P(qx, qh + 3)
    els += [line([P0, P1, P2], 4.6, AMBER, 3.4, dur=1.5), glow(P2[0], P2[1], 70, 6.1, .8),
            line([[P2[0] - 6.4, P2[1] - 7.7], [P2[0] + 6.4, P2[1] + 7.7]], 6.1, LIME, 6, dur=.3),
            label(P2[0] - 16, P2[1] - 36, "the door", 6.4, AMBER, 32, "end"),
            glow(qc[0], qc[1], 70, 8.2, .7), label(qc[0] + 18, qc[1] + 54, "Queen's Chamber", 8.4, BONE, 30, "start")]
    zoom = [line([[P0[0] - 1, P0[1] - 10], [P0[0] - 1, P0[1] + 10]], 1.8, "#ffe2a8", 6, dur=.3), glow(P0[0], P0[1], 40, 1.9, .9),
            label(P0[0] - 26, P0[1] - 16, "1872", 3.6, "#ffe2a8", 32, "end"),
            line([P2, P3], 5.4, AMBER, 2.6, "inferred", .8)] + question(P3[0] + 40, P3[1] - 20, 6.2, 60)
    zc = [2.3, round((P0[0] + P3[0]) / 2 + 10, 1), round((P0[1] + P3[1]) / 2 + 30, 1)]
    return dict(sky, els=els), zoom, zc


def _bust(cx, top, cm):
    """A head-and-shoulders outline to scale (cm px per centimetre): head c. 15 cm wide, shoulders c. 45 cm."""
    hw, hh = 7.8 * cm, 11.5 * cm
    sh = 22.5 * cm; ny = top + 2 * hh
    head = ellipse(cx, top + hh, hw, hh, 30)
    body = [[cx - 6 * cm, ny - 6], [cx - 6 * cm, ny + 2 * cm], [cx - sh * .8, ny + 6 * cm], [cx - sh, ny + 16 * cm], [cx - sh, ny + 30 * cm],
            [cx + sh, ny + 30 * cm], [cx + sh, ny + 16 * cm], [cx + sh * .8, ny + 6 * cm], [cx + 6 * cm, ny + 2 * cm], [cx + 6 * cm, ny - 6]]
    return head, body


def _cat(cx, by, s, at):
    """A cat crouched to walk in, seen from the front (schematic): about 15 cm wide at s px per cm."""
    c, d = "#b8a48c", "#8a7660"
    body = [[cx - 7.5 * s, by], [cx - 7.8 * s, by - 5 * s], [cx - 6 * s, by - 9 * s], [cx + 6 * s, by - 9 * s], [cx + 7.8 * s, by - 5 * s], [cx + 7.5 * s, by]]
    head = [[cx - 5.6 * s, by - 9.5 * s], [cx - 6 * s, by - 14 * s], [cx - 5.2 * s, by - 18.6 * s], [cx - 3 * s, by - 15.6 * s], [cx + 3 * s, by - 15.6 * s],
            [cx + 5.2 * s, by - 18.6 * s], [cx + 6 * s, by - 14 * s], [cx + 5.6 * s, by - 9.5 * s], [cx, by - 8 * s]]
    out = [_poly(body, c, "#efe2cc", 2, at, fx="pop", curve=True), _poly(head, c, "#efe2cc", 2, at + .1, fx="pop"),
           dot(cx - 2.3 * s, by - 13 * s, .95 * s, "#ffd36a", at + .3), dot(cx + 2.3 * s, by - 13 * s, .95 * s, "#ffd36a", at + .3),
           line([[cx - 2.3 * s, by - 13.6 * s], [cx - 2.3 * s, by - 12.4 * s]], at + .3, INK, 3, draw=False), line([[cx + 2.3 * s, by - 13.6 * s], [cx + 2.3 * s, by - 12.4 * s]], at + .3, INK, 3, draw=False),
           _poly([[cx - .8 * s, by - 11.4 * s], [cx + .8 * s, by - 11.4 * s], [cx, by - 10.6 * s]], "#e39a8a", at=at + .3)]
    out += [line([[cx + sg * 1.6 * s, by - 10.8 * s], [cx + sg * 7 * s, by - (11.6 - .9 * k) * s]], at + .5, "#f5ecdc", 1.5, dur=.3) for sg in (-1, 1) for k in range(3)]
    out += [line([[cx - 3 * s, by - 2 * s], [cx - 3 * s, by]], at + .1, d, 2, draw=False), line([[cx + 3 * s, by - 2 * s], [cx + 3 * s, by]], at + .1, d, 2, draw=False)]
    return out


def _sd_wall(at, hole=True, dims=True):
    """The stone face around the shaft's mouth at 15 px a centimetre, the 20 cm square hole, its two dimensions."""
    cm = 15.0
    hx0, hy0, hs = 350, 550, 20 * cm
    els = [box(80, 330, 840, 1080, "#a88a64", "rgba(255,236,206,.4)", 1.5, 8, at),
           box(80, 330, 840, 1080, "url(#k-speck)", r=8, at=at),
           line([[80, 400], [920, 400]], at, "#6b5640", 2, draw=False, op=.6), line([[700, 400], [700, 1410]], at, "#6b5640", 2, draw=False, op=.5)]
    if hole:
        els.append(box(hx0, hy0, hs, hs, INK, "#3a2c1e", 3, 2, at))
    if dims:
        d = at if at > .5 else 1.6
        els += [{"k": "dim", "x1": hx0, "y1": hy0 - 30, "x2": hx0 + hs, "y2": hy0 - 30, "t": "", "c": BONE, "in": d},
                label(500, hy0 - 52, "20 cm", d, BONE, 32),
                {"k": "dim", "x1": hx0 + hs + 26, "y1": hy0, "x2": hx0 + hs + 26, "y2": hy0 + hs, "t": "", "c": BONE, "in": d + .1},
                label(hx0 + hs + 44, hy0 + hs / 2 + 10, "20 cm", d + .1, BONE, 32, "start")]
    return els


def _sd_square():
    """Twenty centimetres square, to scale: a sheet of printer paper over it; then a person's shoulders; then a cat that just fits.
    Each comparison is wiped (the stone face redrawn) before the next."""
    cm = 15.0
    els = _sd_wall(.1)
    pw, ph = 21 * cm, 29.7 * cm                              # printer paper, A4
    els += [box(500 - pw / 2, 550, pw, ph, "rgba(250,246,236,.72)", "#fff", 2, 2, 4.3, fx="pop"),
            label(500, 550 + ph - 30, "printer paper", 4.6, INK, 30, halo=False)]
    els += _sd_wall(5.5)
    head, body = _bust(500, 530, cm)
    els += [{"k": "line", "p": head, "c": BONE, "w": 3.5, "style": "inferred", "curve": True, "in": 5.9},
            {"k": "line", "p": body, "c": BONE, "w": 3.5, "style": "inferred", "in": 5.9},
            _strike(500 - 22.5 * cm - 10, 1040, 500 - 22.5 * cm + 50, 980, 6.8, RED, 8), _strike(500 + 22.5 * cm + 10, 1040, 500 + 22.5 * cm - 50, 980, 7.0, RED, 8)]
    els += _sd_wall(7.6)
    els += _cat(500, 550 + 300 - 6, cm, 8.0)
    return {"base": "dark", "cam": [1.05, 500, 870], "els": els}


SA = math.radians(39.5)


def _sd_climb():
    """Up the southern shaft from the Queen's Chamber, about 60 m, at 14.7 px a metre along it (the shaft's width drawn larger than life)."""
    m = 880 / 60.0
    q0 = (150, 1330); q1 = (q0[0] + 2 * m, q0[1])
    L = 58 * m
    E = (q1[0] + L * math.cos(SA), q1[1] - L * math.sin(SA))
    ux, uy = math.cos(SA), -math.sin(SA)                     # up the shaft
    nx, ny = math.sin(SA), math.cos(SA)                      # across it, towards the floor
    hw = 20
    edge_a = [[q0[0], q0[1] - hw], [q1[0] + hw * math.tan(SA / 2), q1[1] - hw], [E[0] - nx * hw, E[1] - ny * hw]]
    edge_b = [[q0[0], q0[1] + hw], [q1[0] - hw * math.tan(SA / 2), q1[1] + hw], [E[0] + nx * hw, E[1] + ny * hw]]
    els = [box(60, 520, 880, 900, "url(#k-blocks)", r=10, at=.1, op=.55),
           box(60, 520, 880, 900, "rgba(13,11,9,.3)", r=10, at=.1),
           _poly(edge_a + edge_b[::-1], "#120e0b", "none", 0, .2),
           {"k": "line", "p": edge_a, "c": "#c9ad85", "w": 1.8, "in": .2}, {"k": "line", "p": edge_b, "c": "#c9ad85", "w": 1.8, "in": .2},
           _poly([[64, 1352], [150, 1352], [150, 1274], [107, 1252], [64, 1274]], INK, BONE, 2, .2),
           glow(107, 1312, 70, .3, .5), label(92, 1404, "Queen's Chamber", .6, BONE, 30, "start")]
    def at_u(f, off=14):
        return (round(q1[0] + L * f * ux + nx * off, 1), round(q1[1] + L * f * uy + ny * off, 1))
    rx, ry = at_u(.04)
    els += [_robot(rx, ry, 1.15, 4.4, 39.5), glow(rx + 30, ry - 36, 60, 6.6, .8), label(420, 1330, "Upuaut · 1993", 5.4, AMBER, 30, "start")]
    return {"base": "dark", "cam": [1.12, 500, 960], "els": els}, (q1, L, (ux, uy), (nx, ny), E)


def _sd_climb2(geo):
    """It crawls up, metre by metre; about 60 m up, a slab closes the shaft."""
    q1, L, (ux, uy), (nx, ny), E = geo
    P = lambda f, off=0: (round(q1[0] + L * f * ux + nx * off, 1), round(q1[1] + L * f * uy + ny * off, 1))
    els = [line([P(.04, 4), P(.93, 4)], .3, "#cbbca8", 2.5, dur=3.0)]
    for k, f in enumerate((.3, .55, .78)):
        x, y = P(f, 14)
        els.append(_robot(x, y, 1.15, round(.9 + .7 * k, 2), 39.5, op=.4, fx="fade"))
    x, y = P(.93, 14)
    els += [_robot(x, y, 1.15, 3.0, 39.5), glow(x + 40, y - 40, 80, 3.2, .8)]
    a, b = P(0, -60), P(1, -60)
    els += [{"k": "dim", "x1": a[0], "y1": a[1], "x2": b[0], "y2": b[1], "t": "", "c": BONE, "in": 3.6},
            label((a[0] + b[0]) / 2 - 30, (a[1] + b[1]) / 2 - 30, "c. 60 m", 3.7, BONE, 32, "end")]
    d0, d1 = (E[0] - nx * 22, E[1] - ny * 22), (E[0] + nx * 22, E[1] + ny * 22)
    els += [line([d0, d1], 5.0, LIME, 14, dur=.3), glow(E[0], E[1], 90, 5.1, .8),
            dot(E[0] - ux * 9 - nx * 9, E[1] - uy * 9 - ny * 9, 4.5, COP, 5.3), dot(E[0] - ux * 9 + nx * 9, E[1] - uy * 9 + ny * 9, 4.5, COP, 5.3)]
    return els


Y0, Y1 = 1050, 1250                                          # the shaft's floor and ceiling in the side cut (10 px a centimetre)


def _sd_interior(at, door=True, hole=False, stone=False):
    """The inside of the shaft's last metres, drawn over whatever was there (a scene reset), with the slab, the hole, the stone behind."""
    els = [box(60, Y0, 880, Y1 - Y0, "#15110d", r=0, at=at)]
    if door:
        els += [box(600, Y0, 60, Y1 - Y0, LIME, "rgba(255,236,206,.7)", 2, 2, at), line([[600, 1080], [584, 1080], [584, 1098]], at, COP, 6, draw=False)]
    if hole:
        els.append(box(600, 1146, 60, 9, INK, r=1, at=at))
    if stone:
        els.append(box(770, Y0, 80, Y1 - Y0, "#cdb48e", "rgba(255,236,206,.6)", 2, 2, at))
    return els


def _sd_cut():
    """The end of the shaft cut open sideways, at 10 px a centimetre (schematic): the slab, a robot, the dark beyond."""
    els = [box(60, 930, 880, Y0 - 930, "#a88a64", "rgba(255,236,206,.35)", 1.2, 4, .1), box(60, Y1, 880, 1370 - Y1, "#a88a64", "rgba(255,236,206,.35)", 1.2, 4, .1),
           box(60, 930, 880, 440, "url(#k-speck)", r=4, at=.1)]
    for x in (280, 540, 800):
        els.append(line([[x, 930], [x, Y0]], .1, "#6b5640", 2, draw=False, op=.7))
    for x in (170, 430, 690):
        els.append(line([[x, Y1], [x, 1370]], .1, "#6b5640", 2, draw=False, op=.7))
    els += _sd_interior(.1)
    # 1993 ... 2002: nine years pass
    X = lambda yr: round(210 + (yr - 1993) * 64.4, 1)
    ty = 330
    els += [line([[X(1993), ty], [X(2002), ty]], .9, "#8c7152", 3, dur=1.8), dot(X(1993), ty, 11, AMBER, .4), label(X(1993), ty + 55, "1993", .5, AMBER, 30)]
    els += [line([[X(1993 + k), ty - 14], [X(1993 + k), ty + 14]], round(.9 + .2 * k, 2), BONE, 2, draw=False) for k in range(1, 9)]
    els += [dot(X(2002), ty, 11, AMBER, 3.3), label(X(2002), ty + 55, "2002", 3.4, AMBER, 30), label((X(1993) + X(2002)) / 2, ty - 30, "9 years", 2.0, BONE, 30)]
    # a new robot drills a tiny hole through the slab; then a camera on a probe slides through it
    els += [_robot(420, Y1, 3.0, 4.9, 0), arrow([[498, 1166], [596, 1150]], 6.0, "#cbbca8", 6, "known", .5, False)]
    els += [box(600, 1146, 60, 9, INK, r=1, at=7.2, fx="fill")]
    els += [line([[500, 1150], [690, 1150]], 13.6, BLUE, 3, dur=.8), dot(694, 1150, 8, BLUE, 14.4), glow(710, 1150, 90, 14.6, .7, "lamp")]
    return {"base": "dark", "cam": [1.0, 500, 860], "els": els}


def _sd_live():
    """All of it live on television; then, behind the slab, another stone."""
    els, (sx, sy, sw, sh) = _tv(500, 528, 300, .3)
    els += [box(sx + sw * .3, sy + sh * .18, sw * .4, sh * .64, LIME, r=2, at=.5), dot(sx + sw * .4, sy + sh * .3, 4, COP, .6), dot(sx + sw * .6, sy + sh * .3, 4, COP, .6),
            glow(500, 528, 110, .6, .3, "lamp")]
    els += [ring(700, 440, r, round(1.0 + .25 * j, 2), RED, 3, dur=.4) for j, r in enumerate((14, 28, 42))] + [label(752, 450, "live", 1.2, RED, 32, "start")]
    els += [box(770, Y0, 80, Y1 - Y0, "#cdb48e", "rgba(255,236,206,.6)", 2, 2, 5.2, fx="pop"), glow(810, 1150, 110, 5.3, .5),
            label(812, 1035, "another stone", 5.8, AMBER, 32)]
    return els


def _sd_djedi():
    """2011: the scene reset to the shaft as it stood (slab, hole, stone behind); a new robot pushes a bendy snake camera through the
    same hole; red painted marks on the floor of the little space (schematic strokes)."""
    els = [box(60, Y0, 880, Y1 - Y0, "#15110d", r=0, at=.2)] + _sd_interior(.2, door=True, hole=True, stone=True)
    els += [_robot(420, Y1, 3.0, 1.4, 0), label(560, 985, "Djedi · 2011", 1.8, GREEN, 32, "start")]
    els += [line([[498, 1166], [560, 1152], [600, 1150], [660, 1150], [696, 1160], [716, 1194]], 3.0, GREEN, 4, dur=1.6, curve=True),
            dot(718, 1200, 8, GREEN, 4.6), glow(722, 1212, 80, 6.2, .75, "lamp")]
    marks = [[[680, 1244], [690, 1236]], [[694, 1246], [700, 1236]], [[708, 1244], [726, 1244]], [[732, 1238], [744, 1246]], [[750, 1236], [752, 1246]]]
    els += [line(mk, round(9.6 + .15 * k, 2), "#d8402e", 5, dur=.3) for k, mk in enumerate(marks)]
    els += [glow(716, 1240, 70, 10.2, .6, "red"), label(716, 1310, "red paint", 10.6, "#ff8a7a", 32)]
    return els


def _sd_record():
    """The record: three robots, nine years apart; a lock on the access; what each saw was shown or published."""
    X = lambda yr: round(140 + (yr - 1990) * 29.2, 1)
    ay = 880
    els = [line([[X(1990), ay], [X(2015), ay]], .2, "#8c7152", 3, dur=1.0)]
    els += [{"k": "line", "p": ellipse(500, 470, 46, 52, 18, 180, 360), "c": "#cbbca8", "w": 10, "curve": True, "in": .6, "fx": "draw", "dur": .5},
            box(436, 466, 128, 104, "#8c7152", "#f2dcb4", 2.5, 12, .5, fx="pop"), dot(500, 508, 10, INK, .7), box(495, 512, 10, 26, INK, r=2, at=.7)]
    for k, (yr, at) in enumerate(((1993, 1.6), (2002, 1.9), (2011, 2.2))):
        els += [_robot(X(yr), ay - 14, 1.5, at, 0), dot(X(yr), ay, 9, AMBER, at), label(X(yr), ay + 54, str(yr), at + .1, AMBER, 30)]
    els += [box(X(1993), ay + 82, X(2002) - X(1993), 12, AMBER, r=6, at=2.6, fx="pop"), box(X(2002), ay + 82, X(2011) - X(2002), 12, AMBER, r=6, at=3.0, fx="pop"),
            label((X(1993) + X(2002)) / 2, ay + 134, "9 years", 2.8, BONE, 30), label((X(2002) + X(2011)) / 2, ay + 134, "9 years", 3.2, BONE, 30)]
    els += question((X(1993) + X(2002)) / 2, ay - 120, 6.6, 72) + question((X(2002) + X(2011)) / 2, ay - 120, 7.0, 72)
    fx_ = X(1993)
    els += [box(fx_ - 50, 1170, 100, 70, "#2a231c", "#c9ad85", 2, 4, 11.0, fx="pop")] + \
           [box(fx_ - 44 + 18 * k, 1176, 10, 8, "#c9ad85", r=1, at=11.0) for k in range(6)] + [box(fx_ - 44 + 18 * k, 1226, 10, 8, "#c9ad85", r=1, at=11.0) for k in range(6)] + \
           [box(fx_ - 30, 1190, 60, 30, LIME, r=2, at=11.1)]
    tvs, _ = _tv(X(2002), 1205, 110, 12.0)
    els += tvs + [dot(X(2002) + 40, 1170, 5, RED, 12.2)]
    jx = X(2013)
    els += _paper(jx - 46, 1150, 92, 116, 14.0, fill="#e9dcc4", ink="#6b5a48") + [label(jx, 1310, "2013", 15.4, BONE, 30)]
    els += [line([[X(2011), ay + 10], [jx, 1146]], 14.2, "#cbbca8", 2, "inferred", .5)]
    els += [glow(x, 1205, 110, 16.4, .35) for x in (fx_, X(2002), jx)]
    return {"base": "dark", "cam": [1.05, 500, 860], "els": els}


def _sd_parts():
    hook = _sd_hook()
    sec, zoom, zc = _sd_section()
    climb, geo = _sd_climb()
    return dict(hook=hook, sec=sec, zoom=zoom, zc=zc, sq=_sd_square(), climb=climb, climb2=_sd_climb2(geo), cut=_sd_cut(), live=_sd_live(), djedi=_sd_djedi(),
                record=_sd_record(), tag=[ring(810, 1150, 100, .8, LILAC, 3, "claimed", .8)] + question(895, 1190, 2.6, 96))


def sealed_door():
    p = _sd_parts()
    s0 = p["hook"]
    s1 = dict(p["sec"], els=p["sec"]["els"] + p["zoom"])
    s2 = p["sq"]
    s3 = dict(p["climb"], els=p["climb"]["els"] + p["climb2"])
    s4 = like(s0, cam=[1.9, 500, 790])
    s5 = dict(p["cut"], els=p["cut"]["els"] + p["live"])
    s6 = like(s5, cam=[1.75, 640, 1150], add=p["djedi"])
    s7 = p["record"]
    s8 = like(s6, cam=[2.0, 745, 1150], add=p["tag"])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
    beats = [
        B("hook", 0, ["[d:intrigue][k:INSIDE THE GREAT PYRAMID][sfx:boom][act:a secret, confiding]There's a ^*door*, deep inside the Great Pyramid of ^Egypt.",
                      "[d:tension][act:suspense, slow][tune:level]Behind it... [act:the twist][tune:fall]^*another* door. [act:hushed mystery]And ^nobody knows what's behind ^*that* one."], cut=False),
        B("world", 1, ["[d:calm][k:THE SHAFT][act:plain, orienting]It sits in the heart of the pyramid, at the end of a long, narrow shaft that climbs from a room called the Queen's ^Chamber.",
                       "[d:calm][p:0.93][act:intrigued, a little detail]The shaft's mouth was hidden behind the chamber wall until {1872|eighteen seventy-two}, and it has no known way ^out.",
                       "[d:aside][go:2|2.2][p:0.93][act:showing how small]It's just twenty ^*centimetres* square, about the width of a sheet of printer ^paper. [p:1.05][act:light, amused]Too narrow for a ^person. [act:a playful image]Barely wide enough for a ^*cat*."]),
        B("collision", 3, ["[d:build][k:1993][act:storytelling, onward]So in {1993|nineteen ninety-three}, the engineer Rudolf ^Gantenbrink sent in a small ^robot, called ^Upuaut, with a lamp and a ^camera.",
                           "[d:build][sfx:whoosh][act:the climb, growing excitement]It crawled up the steep shaft, metre by ^metre. [act:the discovery, hushed]About sixty metres up, its camera found [go:4|2.4][sfx:hit]a stone ^door, with two ^*copper* fittings."]),
        B("cost", 5, ["[d:tension][k:2002][act:the wait, wry]Then the work ^stopped. [act:plain, counting]Nine ^years later, in {2002|two thousand and two}, a new robot drilled a tiny hole through the ^door. [p:0.93][act:explaining, clear]It's the same trick as a doctor's keyhole ^camera: make a small opening, and slide a lens ^through.",
                      "[d:tension][sfx:drill][act:live television suspense]All of it ^live@adj, on ^television. [act:holding the breath]The camera went in, and found... [sfx:hit][act:the anticlimax, wry][tune:fall]^*another* stone."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:a new clue, intrigued]In {2011|twenty eleven}, another robot, ^Djedi, slipped a bendy snake camera through the same ^hole, and looked ^around. [sfx:shimmer][act:the reveal, hushed]On the floor of the little space: red, ^*painted* marks. [act:the sensible answer, calm]Probably the builders' own ^notes. [act:explaining, a nice detail]Work gangs left red paint marks elsewhere in the pyramid ^too, like a carpenter's pencil marks on ^wood.",
                          "[d:calm][go:7|2.2][act:sober, factual]Access is tightly ^rationed: three robots, nine years ^apart. [act:fair, the critics][tune:rise]So it's fair to ask: was something found, and kept ^quiet? [act:even, careful]But what the robots saw was ^shown: on film, on live@adj television, and in a robotics journal, in {2013|twenty thirteen}. [act:plain][tune:fall]Nothing on record@noun shows a hidden ^find."], cut=False),
        B("tag", 8, ["[d:verdict][k:THE VERDICT][p:0.95][act:the open question, honest][tune:rise]So what's behind the second ^stone? [act:plain truth][tune:fall]Still ^*unknown*. [act:weighing it][tune:rise]A secret kept from ^us? [act:the verdict, measured][tune:fall]^Awaiting evidence.",
                     "[d:tension][p:0.93][act:hushed, inviting][tune:level]Somewhere in the ^dark... [act:quiet promise][tune:fall]the answer is ^*waiting*."]),
    ]
    sources = "Richardson et al. 2013, Journal of Field Robotics · Lehner & Hawass 2017, Giza and the Pyramids"
    post = "A robot found a sealed door inside the Great Pyramid in 1993. Then the work stopped for nine years. What the record shows."
    return EP("sealed-door", "05.02", "The door inside the Great Pyramid", "upuaut-door", "unsupported", "Egypt hid what lies behind the Great Pyramid's doors?",
              "A door behind *a door*.", beats, shots, sources, post, ["#GreatPyramid", "#Giza", "#AncientEgypt", "#Archaeology", "#WeighItYourself"])


def sealed_door_m():
    """The door inside the Great Pyramid as one continuous take: the slab seen up the shaft, the shaft in the pyramid and its mouth sealed
    until 1872, twenty centimetres against a sheet of paper, a person's shoulders and a cat, the robot's climb, nine years on a line,
    a hole drilled live on television, another stone, a snake camera and red marks, three robots nine years apart and what each showed,
    a question in the dark."""
    from mural import remix
    p = _sd_parts()
    ep = sealed_door()
    scenes = {0: p["hook"], 1: p["sec"], 2: p["sq"], 3: p["climb"], 5: p["cut"], 7: p["record"]}
    return remix(ep, scenes=scenes, alias={4: 0, 6: 5, 8: 5},
                 cams={4: [1.9, 500, 790]},
                 beat_adds={4: (p["djedi"], [1.75, 640, 1150]), 5: (p["tag"], [2.0, 745, 1150])},
                 line_adds={(1, 1): (p["zoom"], p["zc"]), (2, 1): (p["climb2"], None), (3, 1): (p["live"], [1.0, 500, 860])})


def EPISODES():
    return [khafre_pillars_m(), sealed_door_m()]
