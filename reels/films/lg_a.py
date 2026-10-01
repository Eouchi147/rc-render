"""Legacy rebuilds, File 01 · Before Us, at the new standard (one continuous take, every argument drawn):
01.01 Kalambo Falls, carpentry before our species, and 01.07 Göbekli Tepe, stone giants before farming.
Drawings are schematic and true to the numbers said aloud: solid = measured, dashed = inferred, dotted = claimed."""
import math
from films import View
from f01 import EP, B, mapshot, _ghost
from scenes import skull, BONE, AMBER, SCAN, GOLD
import illus as I

WOOD, WOODD, GRAIN, CUT = "#8a5d33", "#6f4a29", "#c99c68", "#e3b87e"
STONE, STONE_E, RELIEF = "#d9c29a", "#f2dcb4", "#efe0c0"
STRONG, AWAIT = "#8fd9b0", "#9fd0ff"


def shift(els, dt):
    """The same drawing, built dt seconds later (a later line's additions, in the film without one continuous take)."""
    out = []
    for e in els:
        e = dict(e)
        if isinstance(e.get("in"), (int, float)) and e["in"] >= 0:
            e["in"] = round(e["in"] + dt, 2)
        out.append(e)
    return out


def warp(els, pts):
    """Retime a drawing onto its narration: a piecewise-linear map of build times, old -> new, anchored on the words that name things."""
    def f(t):
        if not isinstance(t, (int, float)) or t < 0:
            return t
        for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
            if t <= a1:
                return round(b0 + (b1 - b0) * (t - a0) / (a1 - a0), 2)
        return round(t + pts[-1][1] - pts[-1][0], 2)
    return [dict(e, **{"in": f(e["in"])}) if "in" in e else e for e in els]


def _r(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def poly(pts, fill, c="none", w=0, at=0, fx=None, curve=False, op=None, **kw):
    e = {"k": "poly", "p": _r(pts), "fill": fill, "c": c, "w": w, "curve": curve, "in": at}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def handaxe(x, y, s=1.0, at=0, rot=0, fx="pop"):
    """A chipped stone tool (schematic): a teardrop of grey stone with flake scars."""
    a = math.radians(rot); ca, sa = math.cos(a), math.sin(a)
    R = lambda px, py: (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
    body = [R(*p) for p in ((-26, -46), (10, -42), (36, -10), (34, 32), (12, 58), (-18, 50), (-38, 16), (-40, -20))]
    scars = [[R(-20, -30), R(4, -6), R(-6, 24)], [R(18, -20), R(4, -6), R(22, 18)], [R(4, -6), R(4, 44)]]
    return [poly(body, "#a49d92", "#efe6d2", 1.5, at, fx, True)] + [I.line(_r(p), at, "#6f6a62", 1.6, draw=False) for p in scars]


def tpil(x, by, h, at=0, c=STONE, edge=STONE_E, fx="rise", op=None, front=1, w=None):
    """A T-shaped pillar seen on its broad face: the head overhangs the shaft, more at the front (front=1: right)."""
    w = w or h * .2
    hh, back, fwd, s = h * .24, w * .25, w * .75, front
    P = [(x - s * w / 2, by), (x + s * w / 2, by), (x + s * w / 2, by - h + hh), (x + s * (w / 2 + fwd), by - h + hh), (x + s * (w / 2 + fwd), by - h),
         (x - s * (w / 2 + back), by - h), (x - s * (w / 2 + back), by - h + hh), (x - s * w / 2, by - h + hh)]
    return poly(P, c, edge, 1.6, at, fx, op=op)


# ---------------------------------------------------------------- the Kalambo joint, in its own units
# log 1 lies across the picture with a notch cut in its top; log 2 runs back into the picture through the notch
# (an oblique view: its far end up and right, its near end down and left, the cut end facing us)
LOG1 = [(160, 902), (330, 898), (500, 897), (670, 898), (840, 902), (858, 918), (866, 960), (858, 1002), (840, 1018),
        (670, 1022), (500, 1023), (330, 1022), (160, 1018), (142, 1002), (134, 960), (142, 918)]
NOTCH = [(438, 893), (562, 893), (562, 945), (552, 962), (534, 967), (466, 967), (448, 962), (438, 945)]
L2B, L2M, L2F, L2R = (657, 785), (500, 907), (343, 1029), 58


def _end(T, s, at):
    """The near, sawn-looking end of log 2: end grain with rings."""
    x, y = T(L2F)
    return [I.dot(x, y, L2R * s, "#b88a58", at), {"k": "circle", "x": x, "y": y, "r": round(L2R * s, 1), "fill": "none", "c": CUT, "w": max(1, 2 * s), "in": at}] + \
           [{"k": "circle", "x": x, "y": y, "r": round(r * s, 1), "fill": "none", "c": "#7a5230", "w": max(.8, 1.5 * s), "op": .8, "in": at} for r in (40, 24)] + \
           [I.dot(x, y, max(1.5, 4 * s), "#5a3a1e", at)]


def joint_icon(cx, cy, s, at=0):
    """The two logs, small and still (a callback on a map, a timeline, a cross-section)."""
    T = lambda p: (round(cx + (p[0] - 500) * s, 1), round(cy + (p[1] - 960) * s, 1))
    w = round(2 * L2R * s, 1)
    return [I.line([T(L2B), T(L2M)], at, WOODD, w, draw=False), poly([T(p) for p in LOG1], WOOD, GRAIN, max(1, 1.6 * s), at, curve=True),
            poly([T(p) for p in NOTCH], "#241b14", at=at), I.line([T(L2M), T(L2F)], at, WOOD, w, draw=False)] + _end(T, s, at)


def kal_hook():
    """0 · the hook: a log; a stone tool cuts a notch; a second log slides in through it."""
    FL = 1110
    T = lambda p: p
    els = [I.line([[90, FL], [910, FL]], -1, "#6b5640", 2, draw=False)] + [I.dot(x, y, 3, "#a8977c", -1, op=.5) for x, y in I.scatter(40, 100, 900, FL + 10, FL + 60, 11)]
    els += [poly(LOG1, WOOD, GRAIN, 1.6, -1, curve=True)]
    els += [I.line([(175, y0), (330, y0 - 3), (500, y0 - 2), (670, y0 - 3), (845, y0)], -1, GRAIN, 1.5, curve=True, draw=False, op=.35) for y0 in (928, 955, 985)]
    els += handaxe(372, 800, 1.0, .35, -30) + [I.arrow([[412, 838], [452, 878]], .7, BONE, 2, dur=.3, curve=False)]
    els += [poly(NOTCH, "#241b14", at=.95, fx="pop"), I.line([NOTCH[0], NOTCH[7], NOTCH[6], NOTCH[5], NOTCH[4], NOTCH[3], NOTCH[2], NOTCH[1]], 1.05, CUT, 3, dur=.4),
            I.glow(500, 930, 100, .95, .6)]
    els += [I.tri(x, y, s, r, CUT, round(1.0 + .07 * k, 2)) for k, (x, y, s, r) in enumerate(((468, 862, 9, 20), (536, 850, 8, 70), (505, 830, 7, 140), (450, 842, 6, 200), (562, 872, 7, 260)))]
    # the slide: log 2 appears piece by piece from its far end to its near end (a thick round-capped line cannot 'draw' cleanly)
    seg = lambda a, b, k, n: [[round(a[0] + (b[0] - a[0]) * k / n, 1), round(a[1] + (b[1] - a[1]) * k / n, 1)], [round(a[0] + (b[0] - a[0]) * (k + 1) / n, 1), round(a[1] + (b[1] - a[1]) * (k + 1) / n, 1)]]
    for k in range(4):
        at = round(2.4 + .1 * k, 2)
        for clip in ([0, 0, 1000, 898], [438, 893, 124, 74]):
            els.append({"k": "group", "clip": clip, "els": [{"k": "line", "p": seg(L2B, L2M, k, 4), "c": WOODD, "w": 116, "in": -1}], "in": at, "dur": .25})
    els += [dict(I.line(seg(L2M, L2F, k, 4), round(2.8 + .1 * k, 2), WOOD, 116, draw=False), dur=.25) for k in range(4)]
    off = (17.2, 22.1)
    els += [I.line([[L2M[0] + k * off[0], L2M[1] + k * off[1]], [L2F[0] + k * off[0], L2F[1] + k * off[1]]], 3.4, GRAIN, 1.6, draw=False, op=.45) for k in (-1, 1)]
    els += _end(T, 1.0, 3.4)
    l1 = [I.label(500, 1250, "c. 476,000 years ago", .6, AMBER, 40, st="serif"), I.glow(500, 930, 280, 4.4, .45)]
    return {"base": "dark", "floor": FL, "cam": [1.1, 500, 950], "els": els}, l1


def kal_verdict():
    """the verdict, back on the logs: the notch, the tool marks, the sand; then what it was for, and what else."""
    v = [I.glow(500, 930, 120, 3.8, .7), I.glow(372, 800, 90, 4.8, .7), I.glow(500, 1110, 300, 6.0, .4)] + \
        [I.dot(x, y, 4, CUT, round(6.0 + .01 * k, 2)) for k, (x, y) in enumerate(I.scatter(30, 160, 840, 1116, 1150, 5))] + \
        [I.label(500, 1340, "strong evidence", 8.0, STRONG, 34)]
    D = dict(style="inferred")
    wk = [I.box(92, 590, 226, 26, "rgba(63,127,156,.55)", r=4, at=2.0)] + \
         [{"k": "circle", "x": 117 + 29 * k, "y": 577, "r": 13, "fill": "rgba(138,93,51,.35)", "c": CUT, "w": 2.2, "style": "inferred", "in": round(2.0 + .05 * k, 2)} for k in range(7)] + \
         [I.person(205, 564, 62, 2.5, BONE)]
    pf = [I.box(390, 600, 220, 26, "rgba(63,127,156,.55)", r=4, at=3.0)] + [I.line([[x, 612], [x, 540]], 3.0, CUT, 3, "inferred", dur=.4) for x in (410, 500, 590)] + \
         [I.box(392, 526, 216, 16, "rgba(138,93,51,.35)", CUT, 2.2, 3, 3.3, style="inferred"), I.person(470, 526, 50, 3.6, BONE)]
    sh = [I.box(705, 588, 180, 18, "rgba(138,93,51,.35)", CUT, 2.2, 3, 3.9, style="inferred"),
          I.line([[700, 590], [795, 462], [890, 590]], 4.1, CUT, 3, "inferred", dur=.6), I.line([[740, 590], [795, 516], [850, 590]], 4.3, CUT, 2, "inferred", dur=.5)]
    vign = wk + pf + sh + I.question(850, 800, 6.0, 100)
    return warp(v, [(0, 0), (3.8, 4.2), (4.8, 5.2), (6.0, 6.6), (8.0, 8.0)]), warp(vign, [(0, 0), (2.0, 2.7), (3.0, 3.5), (3.9, 4.4), (6.0, 6.6)])


def kal_map():
    v = View(-20, 56, -37, 39, (40, 330, 920, 900))
    kx, ky = v.p(31.24, -8.6)
    m = mapshot(v, pins=[("", 31.24, -8.6, {"c": GOLD, "in": .8})], cam=[1.05, 520, 860])
    m["els"] += [I.label(kx + 24, ky + 10, "Kalambo Falls", 1.1, GOLD, 30, "start"), I.label(*v.p(4, 12), "Africa", 1.9, "#d8c7ae", 40, st="ital"),
                 I.label(*v.p(30.3, -14.4), "Zambia", 3.2, BONE, 30, st="ital"), I.label(*v.p(38.5, -3.6), "Tanzania", 3.9, BONE, 30, st="ital")]
    m["els"] = warp(m["els"], [(0, 0), (1.1, 1.1), (1.9, 2.1), (3.2, 4.2), (3.9, 4.9)])
    return m


def kal_falls():
    """2 · a river drops more than 200 m: as tall as a sixty-storey tower (60 x c. 3.3 m)."""
    GY, TOP = 1300, 470
    els = [poly([(-40, TOP), (392, TOP), (404, 490), (396, 640), (414, 800), (402, 980), (420, 1150), (410, GY), (-40, GY)], "#5d4a39", "#8a6a48", 2, .1),
           poly([(-40, 452), (380, 452), (398, 462), (406, 476), (-40, 476)], "#4f93b3", at=.1),
           I.line([[404, 474], [408, 700], [414, 1000], [420, 1292]], .9, "#cfe9f5", 26, dur=1.3, curve=True, op=.85)] + \
          [I.line([[404 + d, 480], [409 + d, 760], [415 + d, 1050], [421 + d, 1290]], 1.0, "#ffffff", 3, dur=1.3, curve=True, op=.7) for d in (-7, 6)] + \
          [I.glow(425, 1268, 150, 1.8, .55, "blue"),
           I.line([[412, TOP], [536, TOP]], 1.8, BONE, 1.5, "inferred", dur=.4), I.line([[520, TOP], [520, GY]], 1.9, BONE, 2, dur=.8),
           I.line([[506, TOP], [534, TOP]], 1.9, BONE, 2, draw=False), I.line([[506, GY], [534, GY]], 1.9, BONE, 2, draw=False),
           I.label(540, 900, "200+ m", 2.3, BONE, 32, "start"),
           I.box(700, 500, 100, 800, "#39434f", "#9fb3c8", 1.5, 2, 3.6, fx="fill", dur=1.3)] + \
          [I.line([[702, 500 + 800 * k / 60], [798, 500 + 800 * k / 60]], 4.7, "#9fb3c8", 1, draw=False, op=.35) for k in range(1, 60)] + \
          [I.label(750, 470, "60 storeys", 5.0, BONE, 30)]
    return {"base": "sky", "tod": "day", "ground": GY, "sun": [180, 380, 22], "cam": [1, 500, 880], "els": els}


def kal_bank():
    """3 · waterlogged banks: rot needs air; below the water, there is none."""
    GY = 560
    air = [I.dot(x, y, 4, SCAN, round(5.3 + .02 * k, 2), op=.75) for k, (x, y) in enumerate(I.scatter(18, 380, 680, 572, 632, 3) + I.scatter(6, 880, 960, 572, 632, 4))]
    bugs = [I.dot(x, y, 5, "#b9d27a", round(3.7 + .05 * k, 2)) for k, (x, y) in enumerate(I.scatter(12, 690, 880, 572, 630, 8))]
    twig = [(700, 602), (760, 594), (820, 598), (870, 590)]
    els = [poly([(40, GY), (360, GY), (340, 600), (290, 636), (200, 643), (110, 628), (60, 600)], "#3f7f9c", "#bfe6f5", 1.5, .2),
           I.box(-20, 640, 1040, 1200, "rgba(63,127,156,.42)", r=0, at=1.0, fx="fill", dur=1.4),
           I.line([[x, round(640 + 4 * math.sin(x / 22), 1)] for x in range(-20, 1041, 20)], 2.2, "#bfe6f5", 2, dur=1.0, curve=True, op=.7),
           I.label(820, 712, "waterlogged", 2.4, AWAIT, 30)] + joint_icon(560, 1080, .42, .2) + \
          [I.line(twig, 3.0, WOOD, 9, draw=False), I.line([[760, 594], [785, 574]], 3.0, WOOD, 5, draw=False)] + bugs + \
          [I.line(twig, 4.7, "#2a1d12", 9, draw=False, op=.7), I.line(twig, 4.9, CUT, 2, "claimed", draw=False)] + air + \
          [I.label(470, 535, "air", 5.7, AWAIT, 30), I.ring(560, 1058, 178, 7.2, AMBER, 3), I.label(560, 1290, "no air", 8.4, AMBER, 30), I.glow(560, 1058, 200, 9.4, .5)]
    els = warp(els, [(0, 0), (2.4, 2.4), (3.0, 3.1), (3.7, 4.4), (4.9, 5.6), (5.3, 6.1), (5.7, 6.5), (7.2, 7.6), (8.4, 8.8), (9.4, 9.8)])
    return {"base": "section", "tod": "day", "ground": GY, "layers": [{"d": 0, "c": "#7a6248", "t": ""}, {"d": 330, "c": "#5f4c39", "t": ""}], "cam": [1, 500, 900], "els": els}


def kal_evidence():
    """4 · look closer: a notch cut on purpose, the other log locked in it, chop marks, a shaped end."""
    LOG = [(180, 912), (300, 908), (425, 908), (432, 914), (436, 950), (452, 978), (500, 986), (548, 978), (564, 950), (568, 914), (575, 908), (700, 908), (770, 912),
           (805, 928), (838, 962), (845, 980), (838, 998), (805, 1032), (770, 1048), (700, 1052), (500, 1054), (300, 1052), (180, 1048), (162, 1032), (152, 980), (162, 928)]
    U = [(432, 912), (436, 950), (452, 978), (500, 986), (548, 978), (564, 950), (568, 912)]
    END = [(770, 912), (805, 928), (838, 962), (845, 980), (838, 998), (805, 1032), (770, 1048)]
    vee = lambda x, y, at: I.line([[x - 11, y - 14], [x, y + 6], [x + 11, y - 14]], at, "#2a1d12", 3.5, dur=.25)
    els = [poly(LOG, WOOD, GRAIN, 1.8, .2, "pop", True)] + \
          [I.line([(185, y0), (420, y0 - 2)], .2, GRAIN, 1.5, draw=False, op=.35) for y0 in (940, 975, 1010)] + \
          [I.line([(580, y0 - 2), (790, y0)], .2, GRAIN, 1.5, draw=False, op=.35) for y0 in (940, 975, 1010)] + \
          [I.line(U, 1.9, AMBER, 4, dur=.8, curve=True), I.glow(500, 950, 110, 2.0, .5),
           I.arrow([[500, 700], [500, 842]], 3.0, BONE, 3, dur=.5, curve=False)] + \
          [I.dot(500, 918, 68, "#b88a58", 3.5), {"k": "circle", "x": 500, "y": 918, "r": 68, "fill": "none", "c": CUT, "w": 2, "in": 3.5}] + \
          [{"k": "circle", "x": 500, "y": 918, "r": r, "fill": "none", "c": "#7a5230", "w": 1.5, "op": .8, "in": 3.6} for r in (48, 30, 12)] + \
          handaxe(250, 790, 1.1, 5.0, -35) + [vee(x, y, round(5.6 + .18 * k, 2)) for k, (x, y) in enumerate(((235, 952), (290, 1000), (345, 945), (640, 958), (690, 1006), (735, 950)))] + \
          [I.label(300, 1120, "chop marks", 6.5, BONE, 30),
           I.line([[790, 916], [826, 958]], 7.5, "#5a3a1e", 2.5, dur=.3), I.line([[826, 1002], [790, 1044]], 7.6, "#5a3a1e", 2.5, dur=.3),
           I.line(END, 7.7, AMBER, 4, dur=.7, curve=True), I.label(790, 1120, "shaped end", 8.1, AMBER, 30)]
    els = warp(els, [(0, 0), (.2, .2), (1.9, 2.4), (3.0, 3.4), (3.6, 4.0), (5.0, 5.6), (5.6, 5.9), (6.5, 7.0), (7.5, 8.2), (8.1, 8.7)])
    return {"base": "dark", "floor": 1180, "cam": [1.1, 500, 940], "els": els}


def kal_dating():
    """5 · how to date it: carbon reaches back only 50,000 years; the sand around the logs, by luminescence, reaches them."""
    X = lambda ya: round(860 - 720 * ya / 500000, 1)            # the bar: 500,000 years ago at x 140, today at x 860
    BY, XL = 1220, X(476000)
    sand = [(x, y) for x, y in I.scatter(220, 70, 930, 500, 975, 9) if (x - 500) ** 2 / 270 ** 2 + (y - 712) ** 2 / 150 ** 2 > 1]
    ring = [(500 + q[0] * math.cos(a), 712 + q[0] * .62 * math.sin(a)) for q, a in zip(I.scatter(40, 240, 290, 0, 1, 4), [k * math.pi / 20 + .3 for k in range(40)])]
    els = [I.box(-20, 480, 1040, 500, "#6f5a44", r=0, at=-1), I.line([[-20, 480], [1020, 480]], -1, "#cbbca8", 2, draw=False)] + \
          [I.dot(x, y, 3.5, "#a8977c", -1, op=.6) for x, y in sand] + joint_icon(500, 760, .55, -1) + I.question(790, 640, 1.0, 80) + \
          [I.line([[140, BY], [860, BY]], 2.4, BONE, 3, dur=.8), I.line([[140, BY - 12], [140, BY + 12]], 2.6, BONE, 2, draw=False), I.line([[860, BY - 12], [860, BY + 12]], 2.6, BONE, 2, draw=False),
           I.label(130, BY + 70, "476,000 years ago", 2.7, BONE, 28, "start"), I.label(870, BY + 70, "today", 2.8, BONE, 28, "end")] + \
          joint_icon(XL + 10, BY - 62, .15, 2.8) + \
          [I.box(X(50000), BY - 18, 860 - X(50000), 18, AMBER, r=4, at=3.6, fx="pop"), I.label(X(50000) + 6, BY - 44, "carbon", 3.9, AMBER, 28, "start"),
           I.line([[X(50000), BY - 26], [X(50000), BY + 30]], 4.9, I.RED, 3, "inferred", dur=.4)] + \
          [I.dot(x, y, 4.5, GOLD, round(6.2 + .02 * k, 2)) for k, (x, y) in enumerate(ring)] + [I.glow(500, 712, 300, 6.4, .3)] + \
          [I.arrow([[300, 860], [210, 1010], [XL + 4, BY - 110]], 8.0, SCAN, 3, "inferred", .8),
           I.line([[860, BY + 18], [XL, BY + 18]], 8.2, SCAN, 10, dur=1.4), I.label(520, BY + 70, "luminescence", 8.6, AWAIT, 28), I.glow(XL, BY + 10, 80, 9.4, .8)]
    els = warp(els, [(0, 0), (1.0, 1.8), (2.4, 3.2), (2.8, 3.5), (3.6, 4.0), (3.9, 4.3), (4.9, 6.0), (6.2, 8.4), (6.4, 8.6), (8.0, 9.4), (8.2, 9.6), (8.6, 10.0), (9.4, 10.8)])
    return {"base": "dark", "cam": [1, 500, 880], "els": els}


def kal_bucket():
    """6 · each grain of sand is a bucket: the sun empties it; sand buries it; radiation fills it drop by drop; full / rate = years."""
    cx, cy = 500, 905
    grain = [(cx + (105 + 9 * math.sin(3 * a + 1)) * math.cos(a), cy + (100 + 8 * math.cos(2 * a)) * math.sin(a)) for a in [k * math.pi / 8 for k in range(16)]]
    sparks = []
    for k, a in enumerate((200, 235, 270, 305, 340, 20, 160, 90)):
        r0 = math.radians(a); sx, sy = cx + 175 * math.cos(r0), cy + 165 * math.sin(r0)
        at = round(8.2 + .12 * k, 2)
        sparks += [I.dot(sx, sy, 5, "#ffcf6a", at), I.arrow([[sx, sy], [cx + 128 * math.cos(r0), cy + 122 * math.sin(r0)]], at + .1, "#ffcf6a", 2, dur=.4, curve=False)]
    bands = [I.box(-20, y0, 1040, y1 - y0, c, r=0, at=at, fx="fill", dur=.5) for (y0, y1, c, at) in
             ((870, 1010, "#7a6248", 4.7), (730, 870, "#6f5a44", 5.0), (590, 730, "#8a6e50", 5.3), (450, 590, "#5f4c39", 5.6), (300, 450, "#7a6248", 5.9))]
    bucket = [I.box(-20, 1010, 1040, 800, "#3b2e22", r=0, at=-1), I.line([[-20, 1010], [1020, 1010]], -1, "#8a6a48", 2, draw=False)] + \
             [I.dot(x, y, 4, CUT, -1) for x, y in I.scatter(60, 70, 930, 994, 1008, 6)] + \
             [I.dot(190, 560, 30, "#ffe2a8", 2.9), I.glow(190, 560, 120, 2.9, .7, "fire")] + \
             [I.line([[222, 580 + 14 * k], [436 + 6 * k, 852 + 8 * k]], 3.1 + .1 * k, "#ffd27a", 3, dur=.5) for k in range(3)] + \
             [I.dot(x, y, 6, SCAN, round(3.6 + .1 * k, 2)) for k, (x, y) in enumerate(((585, 842), (615, 824), (645, 822), (672, 838), (690, 862)))] + bands + \
             [poly(grain, "rgba(239,230,210,.22)", "#efe6d2", 2.5, .5, "pop", True),
              poly([(440, 860), (560, 860), (548, 960), (452, 960)], "rgba(20,15,10,.35)", BONE, 3, 1.6, "pop"),
              I.line([[440, 860], [470, 826], [500, 816], [530, 826], [560, 860]], 1.7, BONE, 2.5, dur=.4, curve=True),
              poly([(449, 895), (551, 895), (546, 956), (454, 956)], "#4f93b3", at=6.0, fx="fill", dur=4.5)] + sparks + \
             [I.line([[578, 895], [598, 895], [598, 956], [578, 956]], 11.4, AMBER, 3, dur=.5), I.label(612, 935, "how full", 11.7, AMBER, 28, "start"),
              poly([(500, 728), (516, 760), (513, 776), (500, 784), (487, 776), (484, 760)], SCAN, at=13.0, fx="pop", curve=True), I.label(462, 768, "how fast", 13.3, AWAIT, 28, "end"),
              I.label(500, 1180, "c. 476,000 years", 15.6, GOLD, 46, st="serif"), I.glow(500, 1160, 240, 15.6, .4)]
    bucket = warp(bucket, [(0, 0), (.5, .9), (1.6, 2.6), (1.7, 2.7), (2.9, 3.8), (3.1, 4.1), (3.6, 4.6), (4.7, 5.6), (5.9, 6.8), (6.0, 7.0), (8.2, 9.2), (11.4, 12.0),
                           (11.7, 12.3), (13.0, 13.9), (13.3, 14.2), (15.6, 16.4)])
    return {"base": "dark", "cam": [1.25, 500, 860], "els": bucket}


def kal_wood():
    """6 · wood rots, stone stays: a camp, buried; only the stone tools come back; the wood was there all along."""
    GY = 1150
    shelter = [[[190, GY], [330, 830]], [[470, GY], [330, 830]], [[240, GY], [330, 830]], [[420, GY], [330, 830]], [[300, GY], [330, 830]]]
    spear, stick, logs = [[750, GY], [812, 790]], [[225, GY - 4], [330, GY - 10]], [[[585, GY - 8], [660, GY - 30]], [[588, GY - 30], [662, GY - 6]]]
    stones = lambda at: handaxe(700, 1112, .7, at, 20) + [I.tri(785, 1138, 13, 30, "#9a948a", at), I.tri(560, 1140, 12, 200, "#9a948a", at), I.tri(515, 1136, 12, 110, "#9a948a", at)]
    els = [I.line([[60, GY], [940, GY]], .1, "#8a6a48", 3, draw=False)] + \
          [I.line(p, round(.2 + .06 * k, 2), WOOD, 8, draw=False) for k, p in enumerate(shelter)] + [I.line([[262, 980], [398, 980]], .5, WOOD, 5, draw=False)] + \
          [I.line(spear, .5, WOOD, 6, draw=False), I.line(stick, .6, WOOD, 6, draw=False)] + [I.line(p, .6, WOOD, 9, draw=False) for p in logs] + \
          [I.glow(622, 1100, 90, .6, .9, "fire"), I.person(870, GY, 220, .7, "#c9b49a")] + stones(.8) + \
          [I.box(-20, 760, 1040, 700, "#4a3a2c", r=0, at=5.0, fx="fill", dur=2.0), I.line([[60, 760], [940, 760]], 6.8, "#8a6a48", 3, draw=False)] + \
          stones(8.2) + [I.glow(650, 1130, 190, 8.3, .5), I.label(650, 1215, "stone", 8.4, BONE, 30)] + \
          [I.line(p, round(10.0 + .1 * k, 2), AMBER, 3, "inferred", dur=.6) for k, p in enumerate(shelter)] + \
          [I.line(spear, 10.5, AMBER, 3, "inferred", dur=.6), I.line(stick, 10.6, AMBER, 3, "inferred", dur=.4)] + [I.line(p, 10.7, AMBER, 3, "inferred", dur=.4) for p in logs] + \
          [I.label(330, 1215, "wood", 10.6, AMBER, 30)] + \
          I.question(330, 700, 12.5, 90)
    els = warp(els, [(0, 0), (.8, .8), (5.0, 6.8), (6.8, 9.0), (8.2, 10.4), (8.3, 10.5), (10.0, 12.6), (10.7, 13.3), (12.5, 15.2)])
    return {"base": "dark", "cam": [1.05, 500, 920], "els": els}


def kal_day():
    """7 · the time since the logs, squeezed into one day: our species turns up at about 9 a.m. (300,000 of 476,000 years)."""
    X0, X1 = 180, 840
    xy = lambda ya: round(X1 - (X1 - X0) * ya / 476000, 1)
    XS = xy(300000)
    HOUR = ["#1d2440"] * 5 + ["#5b4a5c", "#c77c56"] + ["#d9c29a"] * 10 + ["#e39a62", "#a45d45", "#3d3350"] + ["#1d2440"] * 4
    core = joint_icon(X0, 690, .2, .3) + \
        [I.line([[X0, 800], [X1, 800]], .4, BONE, 3, dur=.8), I.line([[X0, 776], [X0, 824]], .6, BONE, 2, draw=False), I.line([[X1, 776], [X1, 824]], .6, BONE, 2, draw=False),
         I.label(X0 - 20, 930, "476,000", .9, BONE, 30, "start"), I.label(X0 - 20, 972, "years ago", 1.0, "#cbbca8", 28, "start"), I.label(X1 + 20, 930, "today", 1.0, BONE, 30, "end")] + \
        skull(XS, 690, .42, i=2.6) + [I.dot(XS, 800, 9, GOLD, 2.6), I.label(XS, 930, "300,000", 3.0, GOLD, 30)] + \
        [I.box(round(X0 + (X1 - X0) * h / 24, 1), 780, round((X1 - X0) / 24 + .5, 1), 40, HOUR[h], r=0, at=round(6.5 + .035 * h, 3), fx="pop") for h in range(24)] + \
        [I.label(X0 - 20, 870, "midnight", 9.2, "#cbbca8", 28, "start"), I.label(X1 + 20, 870, "midnight", 9.4, "#cbbca8", 28, "end"),
         I.line([[XS, 725], [XS, 778]], 11.4, GOLD, 3, dur=.4), I.ring(XS, 680, 70, 11.8, GOLD, 3), I.label(XS, 870, "9 am", 12.0, GOLD, 30), I.glow(XS, 690, 120, 12.0, .6)]
    l1 = [I.glow(X0, 690, 110, .3, .7),
          I.line([[X0, 1030], [X0, 1050], [XS - 6, 1050], [XS - 6, 1030]], 1.6, I.LILAC, 3, dur=.8), I.label((X0 + XS) / 2, 1100, "before us", 2.0, I.LILAC, 30),
          I.line([[XS + 6, 1030], [XS + 6, 1050], [X1, 1050], [X1, 1030]], 2.2, GOLD, 3, dur=.8), I.label((XS + X1) / 2, 1100, "us", 2.5, GOLD, 30),
          I.person((XS + X1) / 2, 1370, 200, 2.7, "#f2c98e")] + _ghost(I, (X0 + XS) / 2, 1370, 200, 3.8) + I.question((X0 + XS) / 2 + 85, 1300, 5.8, 70)
    core = warp(core, [(0, 0), (1.0, 1.0), (2.6, 2.4), (3.0, 4.6), (6.5, 9.4), (7.3, 10.2), (9.2, 10.9), (9.4, 11.4), (11.4, 14.6), (12.0, 15.2)])
    l1 = warp(l1, [(0, 0), (5.0, 5.0), (5.8, 7.0)])
    return {"base": "dark", "cam": [1.1, 500, 820], "els": core}, l1


def kalambo():
    s0, hook_l1 = kal_hook()
    verdict, vign = kal_verdict()
    s8, day_l1 = kal_day()
    sh0 = dict(s0, els=s0["els"] + shift(hook_l1, 5.0))
    sh8 = dict(s8, els=s8["els"] + shift(day_l1, 16.5))
    sh9 = dict(s0, cam=[1, 500, 880], els=[dict(e, **{"in": -1}) for e in sh0["els"]] + verdict + shift(vign, 9.5))
    shots = [sh0, kal_map(), kal_falls(), kal_bank(), kal_evidence(), kal_dating(), kal_bucket(), kal_wood(), sh8, sh9]
    beats = [
        B("hook", 0, ["[d:intrigue][sfx:boom][act:hushed, drawing them in]Someone cut a ^notch into a log, [act:the image, slowly]and slotted ^*another* log into it.",
                      "[d:wonder][p:0.93][act:slow wonder]About four hundred and seventy-six ^*thousand* years ago. [act:quiet awe][tune:fall]The ^oldest wooden structure ever found."], cut=False),
        B("world", 1, ["[d:calm][act:plain, placing us on the map]This is Kalambo ^Falls, in Africa, on the border between ^Zambia and ^Tanzania. [go:2|1.2][act:a little impressed]Here a river drops more than two hundred ^metres: [act:an everyday picture]about as tall as a sixty-storey ^tower.",
                       "[d:calm][go:3|1.2][act:explaining a lucky accident]Along the river, the banks stayed ^waterlogged. [p:0.93][act:explaining, simple]Wood rots because tiny living things ^eat it, and they need ^air. [act:the payoff, warm][tune:fall]Sealed in wet sand, with no air, this wood ^*never* rotted."]),
        B("collision", 4, ["[d:list][act:inviting, leaning in]Look ^closer. [act:laying out the evidence]The notch was cut on ^*purpose*, to lock the two logs ^together. [act:the next clue][tune:level]The wood carries chop marks from stone ^tools. [act:the last clue][tune:fall]Even the ends were ^shaped.",
                           "[d:calm][go:5|1.2][act:curious, the method][tune:rise]But how do you date a log ^that old? [act:explaining, plain]Carbon dating runs out at about fifty thousand ^years. [act:the answer, clear]So the date comes from the ^sand around it, by ^luminescence.",
                           "[d:build][go:6|1.2][p:0.93][act:an everyday picture, warm]Each grain of sand is like a tiny ^bucket. [act:step by step]Sunlight ^empties it. [act:step by step, slower]Buried in the dark, it fills again, drop by ^drop, from faint natural radiation in the ^soil. [p:0.9][act:the neat payoff]Measure how full it is, divide by how fast it fills, and you get the years since it was ^buried."]),
        B("cost", 7, ["[d:wonder][act:gentle regret]That's what makes this so ^rare: wood almost ^never survives. [p:0.93][act:painting it, slow]Leave a camp for a few thousand years, and everything wooden rots ^away. [act:plain][tune:fall]Only the stone tools ^stay. [act:a small revelation]So the Stone Age was also a ^*wood* age. [act:soft, wistful][tune:fall]We just can't ^*see* it."]),
        B("reversal", 8, ["[d:tension][p:0.96][act:leaning in, conspiratorial]Here's the ^thing. [act:setting up the twist, measured]The oldest fossils of our own species are about three hundred ^thousand years old. [p:0.93][act:an everyday picture]Squeeze the time since the logs into a single ^day, from midnight to midnight. [act:the payoff, careful][tune:fall]Our species only turns up at about ^nine in the morning.",
                          "[d:reveal][p:0.94][sfx:hit][act:the reveal, slow and quiet]Whoever built ^this... [act:sure, a little awed]it wasn't ^*us*. [act:fair, honest]No bones were found with the logs, so we don't yet know ^which human relative it was."]),
        B("tag", 9, ["[d:verdict][p:0.96][act:weighing it, calm][tune:rise]Human relatives, building with wood, before we ^existed? [act:counting the clues, even][tune:level]A cut notch, stone-tool marks, and a date from the ^sand. [act:the verdict, firm][tune:fall]*Strong ^evidence*.",
                     "[d:tension][p:0.93][act:honest, open]What it was for, nobody knows yet: [act:wondering aloud][tune:level]a walkway, a platform, the base of a ^shelter? [act:curious, a spark][tune:fall]And what ^*else* did they build?"]),
    ]
    ep = EP("kalambo", "01.01", "Carpentry before our species", "kalambo-structure", "strong", "Human relatives built with wood before our species existed?", "Built *476,000* years ago.",
            beats, shots, "Barham et al. 2023, Nature · Duller et al. 2015, Journal of Human Evolution",
            "Two logs joined with a cut notch, 476,000 years ago, before our species existed. The evidence, rated.",
            ["#Archaeology", "#HumanEvolution", "#Prehistory", "#Africa", "#WeighItYourself"])
    ep["mood"] = "awe"
    return ep


def kalambo_m():
    """Kalambo Falls as one continuous take (see mural.py): a notch is cut and a log slides through it; a river taller than a tower;
    water that keeps the air out; the marks of the tools; a grain of sand as a bucket; a camp that rots to its stones; one day of time."""
    from mural import remix
    ep = kalambo()
    s0, hook_l1 = kal_hook()
    verdict, vign = kal_verdict()
    s8, day_l1 = kal_day()
    return remix(ep, scenes={0: s0, 8: s8}, alias={9: 0}, cams={9: [1, 500, 900]},
                 beat_adds={5: (verdict, [1, 500, 900])},
                 line_adds={(0, 1): (hook_l1, None), (4, 1): (day_l1, [1.05, 500, 960]), (5, 1): (vign, [1, 500, 860])})


# ---------------------------------------------------------------- 01.07 Göbekli Tepe
def gob_hook():
    """0 · a hill at dusk; stone giants rise in a ring. Then: no metal, no writing, no farms; stone, flint, and a plan."""
    HILL = [(-60, 1200), (100, 1160), (240, 1100), (380, 1055), (520, 1040), (660, 1052), (800, 1100), (940, 1165), (1060, 1200), (1060, 1500), (-60, 1500)]
    els = [poly(HILL, "#3b2f26", "#8a6a48", 2, -1)]
    ring = [(2 * math.pi * k / 10 + .31) for k in range(10)]
    back = [a for a in ring if math.sin(a) < 0]
    front = [a for a in ring if math.sin(a) >= 0]
    pil = lambda a, at, c: tpil(520 + 250 * math.cos(a), 1046 + 34 * math.sin(a), 100 * (1 + .12 * math.sin(a)), at, c)
    els += [pil(a, round(2.8 + .1 * k, 2), "#b9a27c") for k, a in enumerate(sorted(back, key=math.sin))]
    els += [tpil(488, 1050, 185, 3.4), tpil(556, 1046, 185, 3.5)]
    els += [pil(a, round(3.6 + .1 * k, 2), STONE) for k, a in enumerate(sorted(front, key=math.sin))]
    els = warp(els, [(0, 0), (2.8, 3.3), (4.0, 4.6)])
    # the second line: what they lacked, struck out; flint on the ground; a plan in gold
    l1 = [poly([(232, 545), (308, 545), (296, 505), (244, 505)], "#c8743c", "#f4b27a", 1.5, .15, "pop"), I.line([[250, 514], [292, 514]], .15, "#ffd9a8", 2, draw=False),
          I.strike(228, 562, 312, 488, .55),
          I.box(462, 486, 76, 70, "#b89a78", "#e9d6ad", 1.5, 8, 1.25, fx="pop")] + \
         [I.tri(478 + 15 * (k % 4), 503 + 17 * (k // 4), 5, 30, "#5a4632", 1.3) for k in range(12)] + \
         [I.strike(455, 566, 545, 478, 1.65),
          I.line([[730, 566], [730, 482]], 2.4, "#e8c35a", 3, dur=.3)] + \
         [I.oval(730 + (8 if k % 2 else -8), 496 + 12 * k, 7, 11, "#e8c35a", at=round(2.45 + .03 * k, 2)) for k in range(5)] + \
         [I.strike(690, 566, 770, 480, 2.85), I.glow(520, 980, 260, 3.6, .35),
          poly([(178, 1236), (226, 1222), (240, 1262), (196, 1282), (172, 1262)], "#4a5560", "#9fb3c8", 1.5, 4.5, "pop"), I.glow(205, 1255, 80, 4.5, .6)] + \
         [I.line(I.ellipse(520, 690, 92, 70, 40), 5.6, GOLD, 3, dur=.9, curve=True)] + \
         [I.dot(520 + 78 * math.cos(2 * math.pi * k / 10), 690 + 58 * math.sin(2 * math.pi * k / 10), 5, GOLD, round(6.0 + .03 * k, 2)) for k in range(10)] + \
         [I.box(500, 676, 10, 28, GOLD, r=2, at=6.4, fx="pop"), I.box(530, 676, 10, 28, GOLD, r=2, at=6.4, fx="pop"), I.glow(520, 690, 120, 6.4, .45)]
    l1 = warp(l1, [(0, 0), (1.65, 1.65), (2.4, 2.7), (2.85, 3.2), (3.6, 4.2), (4.5, 5.1), (5.6, 6.3), (6.4, 6.9)])
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [800, 1080, 28], "cam": [1.1, 500, 950], "els": els}, l1


def gob_map():
    v = View(25, 46, 32, 43, (40, 330, 920, 900))
    gx, gy = v.p(38.92, 37.22)
    m = mapshot(v, pins=[("", 38.92, 37.22, {"c": GOLD, "in": .8})], cam=[1.1, 540, 820])
    m["els"] += [I.label(gx + 20, gy + 10, "Göbekli Tepe", 1.0, GOLD, 30, "start"), I.label(*v.p(33, 39.2), "Turkey", 2.2, "#d8c7ae", 40, st="ital"),
                 I.label(gx - 22, gy + 58, "c. 11,600 years ago", 5.4, AMBER, 30, "end")]
    m["els"] = warp(m["els"], [(0, 0), (1.0, 1.0), (2.2, 3.0), (5.4, 6.4)])
    return m


def gob_quarry():
    """2 · a pillar cut from the bedrock with flint; ten tonnes on a balance against seven cars."""
    PIL = [(220, 610), (640, 610), (640, 580), (770, 580), (770, 745), (640, 745), (640, 700), (220, 700)]
    TR = [(206, 596), (626, 596), (626, 566), (784, 566), (784, 759), (626, 759), (626, 714), (206, 714)]

    def car(x, by, at):
        return [I.box(x - 38, by - 30, 76, 20, "#8fae7a", "#cfe0b8", 1.2, 6, at, fx="pop"), poly([(x - 20, by - 30), (x - 12, by - 44), (x + 14, by - 44), (x + 22, by - 30)], "#6f8f5c", "#cfe0b8", 1.2, at, "pop"),
                I.dot(x - 22, by - 8, 8, "#2a2622", at), I.dot(x + 22, by - 8, 8, "#2a2622", at)]
    els = [poly([(60, 520), (200, 505), (330, 515), (470, 500), (620, 512), (780, 502), (940, 515), (940, 840), (60, 840)], "#bfa57c", "#e8d6b5", 2, .1)] + \
          [I.line(p, .1, "#8c7152", 1.5, draw=False, op=.5) for p in ([[90, 560], [160, 600], [150, 660]], [[860, 560], [830, 640]], [[880, 760], [800, 800]])] + \
          [poly(TR, "#4a3a2c", at=2.2), poly(PIL, "#e6d3ae", "#fff3dc", 1.5, 2.4), I.line(PIL + [PIL[0]], .9, BONE, 3, dur=1.4)] + \
          [poly([(118, 640), (150, 618), (176, 636), (162, 668), (128, 670)], "#4a5560", "#9fb3c8", 1.5, 3.3, "pop")] + \
          [I.dot(x, y, 4, "#ffd27a", round(3.5 + .08 * k, 2)) for k, (x, y) in enumerate(((240, 598), (330, 598), (420, 716), (510, 598), (600, 716), (700, 568), (785, 650)))] + \
          [poly([(468, 1390), (532, 1390), (500, 1336)], "#8c7152", at=4.6), I.box(110, 1322, 780, 14, "#6b5a48", "#a08566", 1, 4, 4.7, fx="pop"),
           tpil(230, 1322, 300, 5.0), I.label(230, 990, "10 tonnes", 5.8, AMBER, 32)] + \
          sum([car(x, 1322, round(7.0 + .12 * k, 2)) for k, x in enumerate((590, 675, 760, 845))], []) + \
          sum([car(x, 1278, round(7.5 + .12 * k, 2)) for k, x in enumerate((632, 717, 802))], []) + [I.label(717, 1210, "7 cars", 8.3, BONE, 30)]
    els = warp(els, [(0, 0), (.1, .1), (.9, 1.3), (2.2, 3.0), (2.4, 3.2), (3.3, 3.9), (3.5, 4.1), (4.6, 5.4), (5.0, 5.8), (5.8, 6.8), (7.0, 7.9), (8.3, 9.0)])
    return {"base": "dark", "cam": [1, 500, 880], "els": els}


def gob_plan():
    """3 · seen from above: a ring wall lined with pillars, two taller ones in the middle."""
    cx, cy = 500, 900

    def bar(x, y, a, L, W, at, big=False):
        ca, sa = math.cos(a), math.sin(a)
        P = [(x + ca * dl - sa * dw, y + sa * dl + ca * dw) for dl, dw in ((-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2), (-L / 2, W / 2))]
        return poly(P, STONE if big else "#cdb48e", STONE_E, 1.5, at, "pop")
    els = [I.line(I.ellipse(cx, cy, 300, 270, 72), 1.0, "#a08566", 36, dur=1.2, curve=True),
           I.line(I.ellipse(cx, cy, 318, 288, 72), 1.4, BONE, 1.5, curve=True, draw=False, op=.5), I.line(I.ellipse(cx, cy, 282, 252, 72), 1.4, BONE, 1.5, curve=True, draw=False, op=.5),
           I.label(cx, 560, "Enclosure D", 1.6, GOLD, 30)] + \
          [bar(cx + 288 * math.cos(a), cy + 258 * math.sin(a), a, 66, 22, round(2.2 + .1 * k, 2)) for k, a in enumerate([2 * math.pi * j / 12 + .26 for j in range(12)])] + \
          [bar(462, cy, math.pi / 2, 96, 28, 4.3, True), bar(538, cy, math.pi / 2, 96, 28, 4.5, True), I.glow(cx, cy, 160, 4.8, .5)]
    els = warp(els, [(0, 0), (1.6, 1.6), (2.2, 2.9), (4.3, 5.3), (4.8, 5.8)])
    return {"base": "plan", "north": [880, 330], "cam": [1, 500, 900], "els": els}


def gob_body():
    """4 · a central pillar, broad face: arms, hands over the belly, a belt, a fox pelt; a person for scale (pillar c. 5.5 m)."""
    BY = 1380
    P = [(400, BY), (580, BY), (580, 700), (680, 700), (680, 480), (360, 480), (360, 700), (400, 700)]
    arm = [[422, 722], [436, 850], [446, 962], [500, 992], [556, 1004]]
    els = [poly(P, STONE, STONE_E, 2, .1), I.box(560, 700, 20, 680, "#000", r=0, at=.1, op=.18), I.box(660, 480, 20, 220, "#000", r=0, at=.1, op=.18),
           I.person(820, BY, 278, .5, "#e8d6b8"), I.line([[60, BY], [940, BY]], .1, "#8a6a48", 2, draw=False),
           I.line([[p[0] + 4, p[1] + 5] for p in arm], 1.6, "#8c7152", 24, dur=1.0, curve=True, op=.5), I.line(arm, 1.6, RELIEF, 20, dur=1.0, curve=True), I.glow(440, 860, 120, 1.9, .45),
           I.oval(546, 1004, 16, 20, RELIEF, "#8c7152", 1.2, 1, 2.9, fx="pop")] + \
          [I.line([[548, 990 + 8 * k], [578, 992 + 8 * k]], round(3.0 + .05 * k, 2), RELIEF, 5, dur=.2) for k in range(4)] + [I.glow(560, 1004, 80, 3.1, .6)] + \
          [I.box(400, 1052, 180, 26, "#b89a78", RELIEF, 1.5, 3, 4.3, fx="pop"), I.box(474, 1056, 26, 18, "none", "#5a4632", 2, 3, 4.4), I.glow(490, 1065, 110, 4.5, .45),
           poly([(528, 1078), (568, 1078), (574, 1150), (566, 1230), (552, 1290), (540, 1236), (532, 1150)], "#a0703c", CUT, 1.5, 5.3, "pop", True), I.glow(550, 1180, 100, 5.4, .5)]
    l2 = [I.box(345, 465, 350, 250, "none", GOLD, 3, 26, 2.4, style="inferred"), I.label(712, 600, "head", 2.7, GOLD, 30, "start"),
          I.box(388, 718, 204, 650, "none", GOLD, 3, 26, 4.2, style="inferred"), I.label(372, 1000, "torso", 4.5, GOLD, 30, "end"), I.glow(490, 930, 430, 6.0, .35)]
    els, l2 = warp(els, [(0, 0), (2.9, 3.2), (4.3, 4.6), (5.3, 5.6)]), warp(l2, [(0, 0), (2.4, 3.4), (4.2, 5.0), (6.0, 6.6)])
    return {"base": "dark", "cam": [1, 500, 900], "els": els}, l2


def gob_vulture():
    """5 · the Vulture Stone (schematic): its carvings read as stars; the Earth's wobble shifts the sky; a match gives a date; a comet."""
    head, shaft = [(270, 400), (730, 400), (730, 560), (270, 560)], [(320, 560), (680, 560), (680, 1760), (320, 1760)]
    ink, STN, REL = "#3a2c20", "#7d6a52", "#cdb48e"
    carve = [poly([(470, 770), (360, 740), (338, 800), (410, 812), (470, 822)], REL, ink, 2, .3), poly([(530, 770), (640, 735), (662, 795), (590, 812), (530, 822)], REL, ink, 2, .3),
             I.oval(500, 800, 38, 62, REL, ink, 2, 1, .3), I.oval(500, 722, 20, 20, REL, ink, 2, 1, .3), poly([(484, 718), (470, 732), (486, 730)], ink, at=.3),
             I.line([[488, 858], [480, 892]], .3, ink, 4, draw=False), I.line([[512, 858], [520, 892]], .3, ink, 4, draw=False),
             I.oval(610, 680, 30, 30, REL, ink, 2, 1, .3),
             I.oval(480, 1030, 24, 40, REL, ink, 2, 1, .3), I.line([[480, 1068], [498, 1100], [528, 1094], [536, 1062]], .3, REL, 6, curve=True, draw=False),
             I.line([[468, 996], [452, 980], [462, 964]], .3, REL, 5, curve=True, draw=False), I.line([[492, 996], [508, 980], [498, 964]], .3, REL, 5, curve=True, draw=False)]
    S = [(345, 770), (500, 820), (655, 765), (500, 722), (610, 680), (480, 995), (535, 1060)]
    links = [(0, 1), (1, 2), (3, 1), (1, 5), (5, 6), (2, 4)]
    ex, ey = 190, 1290
    tip = (ex + 70 * math.sin(math.radians(23)), ey - 70 * math.cos(math.radians(23)))
    els = [{"k": "stars", "n": 80, "x0": 60, "x1": 940, "y0": 300, "y1": 1420, "seed": 7, "in": 4.2},
           poly(head, STN, STONE_E, 2, .1), poly(shaft, STN, STONE_E, 2, .1), I.label(500, 362, "the Vulture Stone · schematic", 3.0, BONE, 28)] + carve + \
          [I.glow(x, y, 40, round(4.1 + .08 * k, 2), .9) for k, (x, y) in enumerate(S)] + [I.dot(x, y, 8, "#fff2c0", round(4.1 + .08 * k, 2)) for k, (x, y) in enumerate(S)] + \
          [I.line([S[a], S[b]], round(4.6 + .1 * k, 2), "#fff2c0", 2.5, "inferred", dur=.4) for k, (a, b) in enumerate(links)] + \
          [I.oval(ex, ey, 50, 50, "#2f5f7a", SCAN, 2, 1, 5.6), I.oval(ex - 12, ey - 8, 20, 14, "#5f8a5a", at=5.6),
           I.line([[2 * ex - tip[0], 2 * ey - tip[1]], tip], 5.8, BONE, 3, dur=.4), I.line(I.ellipse(tip[0], tip[1], 26, 8, 40), 6.2, AMBER, 2.5, curve=True, dur=2.0),
           I.arrow([[830, 1260], [872, 1110], [858, 940]], 8.8, I.LILAC, 3, "inferred", 1.2)] + \
          [I.line([S[a], S[b]], round(12.0 + .08 * k, 2), GOLD, 4, dur=.4) for k, (a, b) in enumerate(links)] + [I.glow(500, 830, 300, 12.4, .4),
           I.line([[935, 300], [800, 405]], 15.4, "#ffe2a8", 6, dur=.7), I.line([[950, 330], [812, 412]], 15.5, "#ffcf8a", 2, dur=.7, op=.6), I.glow(796, 410, 70, 16.0, .9, "fire")]
    els = warp(els, [(0, 0), (3.0, 3.4), (4.1, 4.8), (4.6, 5.3), (5.6, 6.4), (8.8, 10.4), (12.0, 14.2), (15.4, 18.6), (16.0, 19.2)])
    return {"base": "dark", "cam": [1, 500, 880], "els": els}


def gob_dates():
    """6 · the pushback: the claimed sky (10,950 BCE, dotted) against the carving (c. 9600 BCE, from radiocarbon): 1,000+ years apart."""
    X = lambda Y: round(150 + 700 * (11500 - Y) / 2500, 1)
    AY = 1000

    def candle(x, h, at):
        base = 1380
        return [I.box(x - 22, base - h, 44, h, "#efe6d2", "#fff6e6", 1.5, 6, at, fx="fill"),
                poly([(x, base - h - 42), (x + 11, base - h - 15), (x, base - h - 5), (x - 11, base - h - 15)], "#ffd27a", at=at + .3, curve=True), I.glow(x, base - h - 22, 46, at + .3, .9)]
    els = [I.line([[150, AY], [850, AY]], .3, BONE, 3, dur=.8)] + [I.line([[X(y), AY - 10], [X(y), AY + 10]], .5, BONE, 2, draw=False) for y in (11000, 10000, 9000)] + \
          [I.label(X(11000), AY + 46, "11,000 BCE", .6, "#cbbca8", 28), I.label(X(10000), AY + 46, "10,000", .6, "#cbbca8", 28), I.label(X(9000) + 20, AY + 46, "9000", .6, "#cbbca8", 28, "end"),
           I.box(X(11200), AY - 8, X(10700) - X(11200), 16, "rgba(201,193,238,.25)", I.LILAC, 2, 8, .8, style="claimed"), I.dot(X(10950), AY, 9, I.LILAC, .8),
           I.line([[380, 790], [316, 852]], 1.0, "#ffe2a8", 5, dur=.5), I.glow(310, 858, 60, 1.3, .9, "fire"), I.label(X(10950), 760, "the comet?", 1.2, I.LILAC, 30)] + \
          candle(230, 150, 3.4) + candle(330, 95, 4.2) + candle(430, 40, 5.0) + \
          [I.label(520, 1330, "radiocarbon", 3.2, AMBER, 30, "start"), I.arrow([[560, 1290], [640, 1180], [676, 1050]], 7.0, AMBER, 3, "known", .8),
           tpil(X(9600), AY - 10, 150, 7.4), I.label(X(9600), 800, "pillar carved", 7.8, GOLD, 30),
           I.line([[X(10950), 1090], [X(10950), 1110], [X(9600), 1110], [X(9600), 1090]], 10.2, BONE, 3, dur=.8), I.label((X(10950) + X(9600)) / 2, 1160, "1,000+ years", 10.8, BONE, 32)] + \
          I.question((X(10950) + X(9600)) / 2, 930, 13.4, 64)
    els = warp(els, [(0, 0), (1.3, 1.3), (3.2, 2.4), (3.4, 4.0), (5.0, 5.2), (7.0, 7.8), (7.8, 8.6), (10.2, 11.6), (10.8, 12.2), (13.4, 14.4)])
    return {"base": "dark", "cam": [1.1, 500, 1000], "els": els}


GCELL, GSTEP, GX0, GY0 = 46, 52, 243, 623
DUG = [r * 10 + c for r in (6, 7) for c in range(1, 6)]


def gob_hill():
    """7 · the hill from above as a hundred squares: about a tenth dug in thirty years; why so slow? (the claim, dotted: a lock)."""
    cells = [I.box(GX0 + GSTEP * (k % 10), GY0 + GSTEP * (k // 10), GCELL, GCELL, "#5a4a3a", "#7a6248", 1, 4, round(.3 + .006 * k, 3)) for k in range(100)]
    dug = [I.box(GX0 + GSTEP * (k % 10), GY0 + GSTEP * (k // 10), GCELL, GCELL, AMBER, "#ffe2b8", 1.5, 4, round(4.0 + .08 * j, 2), fx="pop") for j, k in enumerate(DUG)]
    lock = [I.box(520, 720, 110, 84, "rgba(201,193,238,.08)", I.LILAC, 3, 12, 8.6, style="claimed"),
            I.line([[538, 720], [540, 688], [575, 668], [610, 688], [612, 720]], 8.6, I.LILAC, 4, "claimed", curve=True, draw=False), I.dot(575, 756, 8, I.LILAC, 9.0)]
    els = [I.oval(500, 880, 390, 380, "#3b2f26", "#8a6a48", 2, 1, .1), I.oval(500, 880, 410, 400, "none", "#8a6a48", 1.5, .4, .1, style="inferred")] + cells + dug + \
          [I.glow(425, 985, 200, 4.8, .5)] + I.question(840, 600, 7.2, 90) + lock + [I.glow(560, 760, 300, 10.4, .3, "blue")]
    els = warp(els, [(0, 0), (7.2, 7.2), (8.6, 9.6), (9.0, 10.0), (10.4, 11.2)])
    return {"base": "dark", "cam": [1, 500, 880], "els": els}


def gob_trench():
    """8 · why slow: digging destroys what it reads (a book that burns as you turn it); every layer recorded; some left for future tools."""
    LAY = [(800, 900, "#8a6e50"), (900, 1000, "#6f5a44"), (1000, 1100, "#a8977c"), (1100, 1200, "#7a6248"), (1200, 1320, "#5a4632")]
    lp, rp = [(310, 430), (492, 446), (492, 590), (310, 574)], [(508, 446), (690, 430), (690, 574), (508, 590)]
    TP = [(508, 446), (556, 370), (622, 352), (606, 470), (508, 590)]              # the page being turned, lifted
    txt = lambda x0, x1, at: [I.line([[x0, 470 + 22 * k], [x1, 470 + 22 * k - 2]], at, "#8a7a66", 2, draw=False, op=.7) for k in range(5)]
    els = [I.box(100, y0, 800, y1 - y0, c, r=0, at=.1) for (y0, y1, c) in LAY] + [I.line([[60, 800], [940, 800]], .1, "#cbbca8", 2, draw=False),
           I.box(100, 800, 400, 100, "#1a1410", r=0, at=1.0, fx="pop"), I.box(100, 800, 400, 100, "none", BONE, 2, 2, 1.5, style="inferred"),
           I.person(300, 900, 90, .6, "#e8d6b8"), I.line([[318, 846], [352, 880]], .7, "#8a6a48", 4, draw=False),
           poly(lp, "#efe6d2", "#b8a888", 1.5, 2.8, "pop"), poly(rp, "#efe6d2", "#b8a888", 1.5, 2.8, "pop")] + txt(330, 476, 2.9) + txt(524, 670, 2.9) + \
          [poly(TP, "#f5ecdc", "#b8a888", 1.5, 3.8, "pop"), I.glow(590, 440, 90, 4.3, .9, "fire"), poly(TP, "#2a1d12", "#ff9a5a", 2.5, 4.7, op=.92)] + \
          [I.dot(x, y, 4, "#ff9a5a", round(4.9 + .1 * k, 2)) for k, (x, y) in enumerate(((600, 372), (622, 344), (584, 330), (640, 322), (606, 300)))] + \
          [I.box(130, 729, 100, 22, "#e8c35a", "#fff3dc", 1, 3, 8.0, fx="pop")] + [I.line([[140 + 12 * k, 729], [140 + 12 * k, 738 + (6 if k % 2 else 0)]], 8.0, "#5a4632", 1.5, draw=False) for k in range(8)] + \
          [I.box(290, 704, 60, 72, "#efe6d2", "#b8a888", 1, 3, 8.8, fx="pop"), I.line([[298, 760], [312, 730], [326, 748], [342, 716]], 9.0, "#5a4632", 2, dur=.4),
           I.box(424, 716, 72, 48, "#3b3632", "#cbbca8", 2, 6, 9.6, fx="pop"), {"k": "circle", "x": 460, "y": 740, "r": 14, "fill": "#1a1511", "c": "#cbbca8", "w": 2, "in": 9.6},
           I.box(560, 800, 340, 520, "none", GOLD, 3, 4, 12.0, style="inferred"), I.glow(730, 1060, 220, 12.4, .3),
           I.box(696, 672, 68, 30, "#5a6670", "#cfe6ff", 1.5, 6, 14.0, fx="pop"), I.line([[742, 672], [752, 650]], 14.0, "#cfe6ff", 2, draw=False),
           {"k": "fan", "x": 730, "y": 704, "a0": 62, "a1": 118, "r": 560, "n": 11, "c": SCAN, "in": 14.2}]
    els = warp(els, [(0, 0), (1.0, 1.4), (1.5, 2.0), (2.8, 3.2), (3.8, 5.0), (4.7, 5.6), (4.9, 5.8), (8.0, 9.2), (8.8, 9.8), (9.6, 10.4), (12.0, 14.0), (12.4, 14.4),
                     (14.0, 15.6), (14.2, 15.8)])
    return {"base": "dark", "cam": [1, 500, 880], "els": els}


def gob_verdict():
    """the verdict on the hill: the dug tenth, done with care; the reports, published as it goes; nine-tenths waiting."""
    v = [I.box(GX0 + GSTEP - 6, GY0 + 6 * GSTEP - 6, 5 * GSTEP + 6, 2 * GSTEP + 6, "none", GOLD, 3, 6, 2.2, fx="draw", dur=.8)] + \
        [I.box(800, 1244 - 16 * k, 100, 13, "#efe6d2", "#b8a888", 1, 2, round(3.9 + .15 * k, 2), fx="pop") for k in range(6)] + \
        [I.label(850, 1300, "reports", 4.9, BONE, 28), I.label(470, 1330, "awaiting evidence", 5.9, AWAIT, 34)]
    l1 = [I.glow(520, 800, 340, .5, .3, "blue"), I.box(GX0 - 8, GY0 - 8, 10 * GSTEP + 10, 10 * GSTEP + 10, "none", AWAIT, 2, 8, .8, style="inferred")]
    return warp(v, [(0, 0), (2.2, 3.0), (3.9, 4.4), (4.9, 5.4), (5.9, 6.2)]), l1


def gobekli():
    s0, hook_l1 = gob_hook()
    s4, body_l2 = gob_body()
    s7 = gob_hill()
    verdict, wait = gob_verdict()
    sh0 = dict(s0, els=s0["els"] + shift(hook_l1, 6.8))
    sh4 = dict(s4, els=s4["els"] + shift(body_l2, 7.0))
    sh9 = dict(s7, cam=[1, 500, 900], els=[dict(e, **{"in": -1}) for e in s7["els"]] + verdict + shift(wait, 7.8))
    shots = [sh0, gob_map(), gob_quarry(), gob_plan(), sh4, gob_vulture(), gob_dates(), s7, gob_trench(), sh9]
    beats = [
        B("hook", 0, ["[d:intrigue][sfx:boom][act:awe, building]Some six ^*thousand* years before Stonehenge, someone raised stone ^*giants* on a hill in ^Turkey.",
                      "[d:list][act:counting what they lacked][tune:level]No ^metal. [act:same rhythm][tune:level]No ^writing. [act:same rhythm][tune:level]No ^farms. [act:then the turn][tune:level]Just stone, ^flint... [act:the surprise, warm][tune:fall]and a ^*plan*."], cut=False),
        B("world", 1, ["[d:wonder][act:quiet wonder, presenting it]This is Göbekli ^Tepe, in the southeast of ^Turkey. [act:plain, precise]Its great stones went up about eleven thousand six hundred years ^ago.",
                       "[d:build][sfx:chisel][go:2][act:describing the work, impressed]They carved T-shaped pillars straight out of the ^bedrock, with flint ^tools. [act:a telling detail]The biggest weigh around [count:10|tonnes]^*ten* tonnes: [act:an everyday picture, light]as heavy as seven ^cars."]),
        B("collision", 3, ["[d:calm][act:simple, calm]Then they stood them in ^rings: [act:describing it, admiring]a stone wall lined with ^pillars, and two taller ones in the ^middle.",
                           "[d:list][sfx:hit][go:4][act:inviting, intrigued]Look ^closer. [sfx:shimmer][act:a discovery]They have ^*arms*. [act:pointing out details][tune:level]Hands over the ^belly. [act:same rhythm][tune:level]A ^belt. [act:same rhythm][tune:fall]A fox ^pelt.",
                           "[d:reveal][p:0.95][act:the reveal, slow]These aren't just ^pillars. [p:0.93][act:explaining, simple]The top of the T is a ^head, the long shaft a ^torso. [act:sure, a hush]They're ^*bodies*."]),
        B("cost", 5, ["[d:build][act:recounting a bold idea]In {2017|twenty seventeen}, two researchers read@past one pillar, the Vulture ^Stone, as a ^*star map*. [p:0.93][act:explaining, a picture]The Earth wobbles slowly, like a spinning ^top, so the stars seen in each season shift over thousands of ^years. [act:explaining, the trick]Match a carving to that sky, and you get a ^date. [act:their reading, vivid]They read@past it as the record@noun of a ^comet strike,",
                      "[d:calm][stamp:10,950 BCE ± 250|gold][act:completing the thought][tune:fall]around ^eleven thousand BCE."]),
        B("reversal", 6, ["[d:reveal][act:the pushback, firm]The excavators pushed ^back. [p:0.93][act:explaining, the method]Radiocarbon, a clock that burns down like a candle in anything that once ^lived, dates the enclosure ^itself. [act:the problem, plain]The pillar was carved more than a ^*thousand* years after that ^sky. [act:fair, weighing][tune:rise]A sky from a thousand years ^earlier?",
                          "[d:reveal][go:7][act:relishing the real shock][tune:rise]And the real ^shock? [act:quiet amazement]After thirty years of digging, only about [count:10|%]a ^*tenth* of the site has been ^excavated. [act:the suspicion, fair][tune:rise]Why so ^slow? [act:their case, even]Some say the dig is being held back, to hide what's ^buried.",
                          "[d:build][go:8][p:0.93][act:explaining, patient]But digging ^destroys what it uncovers: [act:a picture, vivid]like reading a book that ^burns, page by page, as you turn it. [act:explaining, clear]So every layer is measured, drawn and photographed before it ^goes. [act:plain, reassuring]And part of a site is often left untouched, for the better tools of the ^future."]),
        B("tag", 9, ["[d:verdict][p:0.96][act:weighing it, even][tune:rise]Hidden on ^purpose? [act:the evidence, calm and fair]The record@noun shows slow, ^careful work, published as it ^goes. [act:the verdict, measured][tune:fall]*Awaiting ^evidence*.",
                     "[d:tension][p:0.93][act:quiet, full of promise][tune:level]The other ^nine-tenths are still underground... [act:hushed][tune:fall]^*waiting*."]),
    ]
    ep = EP("gobekli", "01.07", "Stone giants before farming", "gobekli-excavation", "unsupported", "Göbekli Tepe's dig is being slowed to hide what's buried?", "Older than Stonehenge by *6,000 years*.",
            beats, shots, "Schmidt 2012 · Clare 2020, e-Forschungsberichte des DAI · Sweatman & Tsikritsis 2017",
            "Stone giants with arms and belts, 11,600 years ago, before farming. And only a tenth of the hill has been dug. The evidence, rated.",
            ["#GobekliTepe", "#Archaeology", "#Neolithic", "#AncientHistory", "#WeighItYourself"])
    ep["mood"] = "awe"
    return ep


def gobekli_m():
    """Göbekli Tepe as one continuous take (see mural.py): giants rise on a hill; a pillar cut from the rock and weighed against cars;
    the ring from above; a body in stone; a star map and the dates that undo it; the hill as a hundred squares; a book that burns as you read."""
    from mural import remix
    ep = gobekli()
    s0, hook_l1 = gob_hook()
    s4, body_l2 = gob_body()
    verdict, wait = gob_verdict()
    return remix(ep, scenes={0: s0, 4: s4, 7: gob_hill()}, alias={9: 7}, cams={9: [1, 500, 900]},
                 beat_adds={5: (verdict, [1, 500, 900])},
                 line_adds={(0, 1): (hook_l1, None), (2, 2): (body_l2, None), (5, 1): (wait, [1.15, 500, 860])})


def EPISODES():
    return [kalambo_m(), gobekli_m()]
