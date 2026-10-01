"""Legacy rebuilds (lg_c), written from scratch at the series' standard: drawn scenes, one continuous take each (see mural.py).
03.01 The Sky Fell? · sky-fell: the Younger Dryas cold, and the comet blamed for it.
02.02 The First Signs · ice-age-signs: zigzags, dots, grids and hands on every continent, and the dates that weigh one lost source.
Each film's base spec is built with its own File's EP (so its series comes out right); <name>_m() is its continuous take."""
import math, random
from films import like, View
from f01 import mapshot, LAURENTIDE, CORDILLERAN
from f03 import EP as EP03, B, mammoth
from f02 import EP as EP02, hand, _glyph, CREAM, OCH
from f09 import B as B09
from illus import label, line, arrow, glow, dot, box, ring, strike, oval, person, question, ellipse, scatter, \
    BONE, AMBER, RED, GREEN, BLUE, LILAC, AU

ICE = "#e6eff6"
WARM = "#ffb07a"


def _poly(p, fill, c="none", w=0, at=0, curve=False, **kw):
    e = {"k": "poly", "p": [[round(x, 1), round(y, 1)] for x, y in p], "fill": fill, "c": c, "w": w, "curve": curve, "in": at}
    e.update(kw)
    return e


def _ghost_person(x, y, h, at, op=.22, c="#cbbca8"):
    return {"k": "lib", "k2": "person", "x": x, "y": y, "h": h, "color": c, "op": op, "keepop": True, "in": at}


# ================================================================ 03.01 The Sky Fell? (sky-fell)
def _sx(ya):
    """The thermometer's time axis: 16,000 years ago at x 130, 10,000 at x 870."""
    return round(130 + 740 * (16000 - ya) / 6000, 1)


_CA = [(16000, 1068), (15700, 1078), (15400, 1062), (15100, 1074), (14800, 1066), (14720, 1050), (14660, 900), (14600, 812), (14450, 800), (14200, 822),
       (13950, 808), (13700, 836), (13450, 826), (13200, 850), (13000, 844), (12920, 856)]
_CB = [(12920, 856), (12870, 980), (12820, 1066)]
_CC = [(12820, 1066), (12600, 1080), (12400, 1070), (12200, 1082), (12000, 1072), (11800, 1080), (11720, 1074)]
_CD = [(11720, 1074), (11680, 940), (11620, 800), (11500, 772), (11200, 764), (10800, 770), (10400, 756), (10000, 762)]
_COMET = (800, 430)


def _thermo():
    """0 · the thermometer of the past: warming, then the plunge back into the cold for 1,200 years, then the warmth for good; the sky, a suspect."""
    C = lambda pts: [[_sx(a), b] for a, b in pts]
    x0, x1 = _sx(12900), _sx(11700)
    els = [box(x0, 640, x1 - x0, 560, "rgba(159,208,255,.13)", at=9.4, fx="fill", dur=1.2),
           line([[110, 1200], [890, 1200]], .1, "#e9dccb", 2.5, dur=.8)] + \
          [line([[_sx(y), 1190], [_sx(y), 1210]], .3, "#e9dccb", 2, draw=False) for y in range(16000, 9999, -1000)] + \
          [label(890, 1252, "years ago", .5, "#cbbca8", 28, "end"),
           arrow([[92, 1130], [92, 770]], .4, BONE, 2.5, dur=.6, curve=False),
           label(112, 772, "warmer", .6, WARM, 28, "start"), label(112, 1150, "colder", .6, BLUE, 28, "start"),
           line(C(_CA), .3, AMBER, 5, dur=1.8),
           line(C(_CB), 3.3, BLUE, 5, dur=.5),
           line([[x0, 1200], [x0, 712]], 6.2, BONE, 2, "inferred", .7), dot(x0, 1200, 7, AU, 6.2), label(x0, 1252, "12,900", 6.4, AU, 30),
           line(C(_CC), 9.6, BLUE, 5, dur=1.6),
           line([[x0, 690], [x1, 690]], 11.6, BONE, 2.5, dur=.6), line([[x0, 676], [x0, 704]], 11.6, BONE, 2.5, draw=False), line([[x1, 676], [x1, 704]], 11.9, BONE, 2.5, draw=False),
           label((x0 + x1) / 2, 668, "1,200 years", 11.9, BONE, 30),
           line(C(_CD), 12.9, AMBER, 5, dur=1.0),
           line([[940, 282], [_COMET[0], _COMET[1]]], 14.4, LILAC, 4, "claimed", .8), glow(_COMET[0], _COMET[1], 70, 15.0, .9, "scan"), dot(_COMET[0], _COMET[1], 11, "#f5f0ff", 15.0)] + \
        question(890, 570, 15.6, 70)
    return {"base": "dark", "stars": 90, "cam": [1.05, 500, 880], "els": els}


def _dryas():
    """(on the thermometer) the cold snap's name: the Younger Dryas, after a little Arctic flower that came back with the cold."""
    fx, fy = 586, 975
    return [label(586, 602, "Younger Dryas", 2.6, AU, 36, st="serif"),
            line([[fx, fy + 16], [fx, 1062]], 4.6, GREEN, 4, dur=.4), oval(fx - 15, 1040, 14, 6, GREEN, at=4.8), oval(fx + 15, 1028, 14, 6, GREEN, at=4.9)] + \
           [dot(round(fx + 18 * math.cos(k * math.pi / 4), 1), round(fy + 18 * math.sin(k * math.pi / 4), 1), 10, "#f7f4ec", round(5.0 + .04 * k, 2)) for k in range(8)] + \
           [dot(fx, fy, 8, AU, 5.4)] + \
           [dot(x, y, 3, "#f7f4ec", round(6.6 + .03 * k, 2), op=.75) for k, (x, y) in enumerate(scatter(22, 525, 650, 730, 930, 5))]


def _sky_verdict():
    """(on the thermometer) the verdict: the cold, ringed as real; the comet, ringed as a claim still waiting."""
    return [_poly(ellipse(586, 950, 125, 190, 40)[:-1], "none", GREEN, 4, 1.0, True, fx="draw", dur=.9),
            ring(_COMET[0], _COMET[1], 64, 3.0, LILAC, 3, "claimed"), glow(_COMET[0], _COMET[1], 130, 4.6, .8, "scan"),
            line([[90, 440], [290, 440]], 6.0, "#8c7152", 2.5, draw=False), line([[122, 440], [152, 466], [190, 474], [228, 466], [258, 440]], 6.2, LILAC, 3, "claimed", .6, True),
            line([[190, 520], [190, 650]], 8.8, AU, 3, dur=.5)] + [dot(190, 530 + 30 * k, 7, AU, round(9.0 + .1 * k, 2)) for k in range(5)] + \
           [glow(190, 540, 150, 11.0, .5, "lamp"), glow(_COMET[0], _COMET[1], 90, 11.0, .7, "lamp")]


def _sea():
    """1 · the coast in section: the ice sheet on the land, the sea 134 m lower (a forty-storey tower); then the ice melts,
    the sea climbs, and people walk onto the land the ice has left."""
    SKY1 = "#151a26"
    G, SL, LO = 820, 860, 1262                         # the land, today's sea level, the Ice Age sea level (134 m at 3 px a metre)
    slope = lambda y: round(440 + (y - SL) * .801, 1)
    stars = [dot(x, y, round(1.4 + (k % 3) * .6, 1), "#fff6e8", -1, op=.5) for k, (x, y) in enumerate(scatter(40, 20, 980, 40, 420, 2) + scatter(16, 470, 980, 420, 820, 3))]
    land = _poly([(-10, G), (120, G - 8), (260, G - 4), (380, G + 4), (440, SL), (slope(LO), LO), (820, LO + 98), (900, LO + 210), (1010, LO + 280), (1010, 1790), (-10, 1790)],
                 "#4a3b2e", "#8c7152", 2, -1)
    strata = [line([[-10, y], [slope(y), y]], -1, "#3a2e24", 2, draw=False, op=.8) for y in (930, 1040, 1150)]
    old_sea = [_poly([(slope(LO), LO), (1010, LO), (1010, LO + 280), (900, LO + 210), (820, LO + 98)], "#2f6f8f", "#9fd0ff", 2, .4),
               line([[slope(LO), LO], [1000, LO]], .4, "#cfe6ff", 2.5, draw=False)]
    new_sea = _poly([(440, SL), (1010, SL), (1010, LO), (slope(LO), LO)], "rgba(63,134,168,.78)", "none", 0, 18.0, fx="fill", dur=2.0)
    dome = _poly([(30, G - 5), (45, 740), (80, 650), (140, 565), (215, 512), (290, 500), (350, 528), (392, 610), (410, 720), (415, G + 2)], ICE, "#ffffff", 2, 2.0, True, fx="rise")
    eraser = _poly([(-10, 430), (456, 430), (456, 846), (440, 853), (380, G + 1), (260, G - 7), (120, G - 11), (-10, G - 3)], SKY1, SKY1, 2, 16.6, dur=1.6)
    tower = [box(870, SL + 2, 50, LO - SL, "none", BONE, 2, 0, 13.4, style="inferred")] + \
            [line([[873, SL + 2 + 10 * k], [917, SL + 2 + 10 * k]], 13.6, BONE, 1, draw=False, op=.35) for k in range(1, 40)]
    els = [box(-10, -10, 1020, 1800, SKY1, at=-1)] + stars + [land] + strata + old_sea + [new_sea, dome, label(225, 472, "ice sheet", 2.6, "#e6eef6", 30), eraser,
           arrow([[930, LO - 18], [900, 980], [760, 720], [560, 570], [372, 552]], 5.0, BLUE, 3, "inferred", 1.4),
           label(935, LO + 44, "Ice Age", 8.2, "#cfe6ff", 30, "end"),
           line([[440, SL], [1000, SL]], 8.6, BONE, 2.5, "inferred", 1.0), label(470, SL - 18, "sea level today", 8.8, BONE, 28, "start"),
           line([[850, SL], [850, LO]], 10.0, AU, 2.5, dur=.8), line([[838, SL], [862, SL]], 10.0, AU, 2.5, draw=False), line([[838, LO], [862, LO]], 10.7, AU, 2.5, draw=False),
           label(835, 1045, "134 m", 10.6, AU, 32, "end")] + tower + [label(835, 1120, "40 storeys", 14.2, BONE, 30, "end"),
           arrow([[400, G - 20], [470, 940], [560, 1060]], 17.0, BLUE, 3, dur=.7),
           arrow([[300, G - 14], [450, 880], [600, 1080]], 17.3, BLUE, 3, dur=.7)] + \
          [person(x, G - 7, h, at, "#e8d6b8") for x, h, at in ((150, 70, 19.8), (200, 66, 20.1), (250, 72, 20.4))] + \
          [arrow([[110, 720], [330, 720]], 20.6, AU, 3, "inferred", .8, False), label(220, 690, "new lands", 21.0, AU, 30)]
    return {"base": "dark", "cam": [1.0, 500, 880], "els": els}


LANDC = "#3a2f24"


def _mam(x, y, h, at, gone):
    """A small mammoth on the map; at `gone` it is painted out (the land shows through) and a dotted outline stays."""
    b = mammoth(x, y, h, at, "#d2b48c")
    er = mammoth(x, y, h, gone, LANDC)
    for e in er:
        e["w"] = (e.get("w") or 1) + 3; e["c"] = LANDC
    ghost = [dict(e, fill="none", c="#cbbca8", w=2, style="claimed", **{"in": gone + .3}) for e in b if e["k"] == "poly"]
    return b, er + ghost


def _claim():
    """3 · North America under its ice; the claim drawn dotted: a comet, blasts in the sky, fires, the mammoths gone."""
    v = View(-140, -55, 20, 72, (40, 330, 920, 1000))
    P = lambda q: [list(v.p(*p)) for p in q]
    hit = v.p(-84, 52)
    mams = [_mam(*v.p(lo, la), 62, round(.8 + .2 * k, 2), round(8.0 + .2 * k, 2)) for k, (lo, la) in enumerate(((-103, 43.5), (-89, 38), (-117, 39.5)))]
    bursts = [(-95, 51.5), (-77, 45.5), (-107, 51), (-86, 46.5)]
    fires = [(-121, 38), (-99, 36), (-80, 35.5), (-110, 34), (-92, 33), (-76, 40), (-109, 43), (-83, 39.5), (-117, 47), (-96, 43), (-123, 46), (-91, 47.5)]
    els = [e for m in mams for e in m[0]] + [e for m in mams for e in m[1]] + \
          [_poly(P(LAURENTIDE), "rgba(235,245,255,.42)", "#ffffff", 1.6, -1, True), _poly(P(CORDILLERAN), "rgba(235,245,255,.42)", "#ffffff", 1.6, -1, True),
           label(*v.p(-100, 62), "ice", .4, "#e6eef6", 34, st="ital"), label(*v.p(-100, 29.5), "North America", .6, BONE, 34, st="ital")] + \
          [line([[930, 300], list(hit)], 2.2, LILAC, 4, "claimed", .9), glow(hit[0], hit[1], 70, 2.8, .9, "scan"), dot(hit[0], hit[1], 10, "#f5f0ff", 2.8),
           label(880, 290, "a comet?", 2.6, LILAC, 30, "end")] + \
          [line([list(hit), list(v.p(*b))], round(4.2 + .3 * k, 2), LILAC, 2.5, "claimed", .5) for k, b in enumerate(bursts)] + \
          [g for k, b in enumerate(bursts) for g in (glow(*v.p(*b), 90, round(4.5 + .3 * k, 2), .9, "red"), ring(*v.p(*b), 26, round(4.5 + .3 * k, 2), LILAC, 2.5, "claimed"))] + \
          [glow(*v.p(*f), 30 + 7 * (k % 3), round(7.0 + .05 * k, 2), .95, "fire") for k, f in enumerate(fires)]
    return mapshot(v, extra=els, cam=[1.18, 490, 780])


def _dig():
    """4 · the ground cut open, read like pages: the thin layer the comet team reported at the start of the cold (beads, magnetic
    grains, soot, drawn dotted: the claim); mammoth bones and Clovis points just below; none above."""
    S = 600
    bands = [(1180, 1350, "#7a6248"), (1000, 1180, "#5f4c39"), (812, 1000, "#8a6a4a"), (790, 812, "#231b15"), (600, 790, "#6f5a43")]
    els = [line([[40, S], [960, S]], .2, "#8c7152", 3, draw=False)] + \
          [line([[60 + 26 * k, S], [66 + 26 * k, S - 12]], .2, "#7fa35a", 2, draw=False) for k in range(34)] + \
          [person(130, S, 110, .5, "#e8d6b8"), line([[150, S - 50], [196, S - 6]], .6, "#c9a370", 5, draw=False)] + \
          [box(40, y0, 920, y1 - y0, c, r=0, at=round(3.0 + .45 * k, 2), fx="fill", dur=.5) for k, (y0, y1, c) in enumerate(bands)] + \
          [line([[40, y], [960, y]], round(3.0 + .45 * k, 2), "#e9dccb", 1.2, draw=False, op=.35) for k, y in enumerate((1180, 1000, 812, 790))] + \
          [arrow([[915, 640], [915, 1320]], 7.2, BONE, 2.5, dur=1.0, curve=False), label(898, 650, "newer", 7.4, BONE, 28, "end"), label(898, 1330, "older", 8.4, BONE, 28, "end"),
           box(44, 787, 912, 28, "none", LILAC, 3, 4, 10.6, style="claimed"), label(60, 772, "12,900", 11.0, AU, 30, "start"),
           line([[640, 788], [640, 545]], 13.4, BONE, 2, "inferred", .5), dot(640, 425, 118, "#3a2f26", 13.8, fx="fade"), ring(640, 425, 120, 13.8, BONE, 3, dur=.6)] + \
          [dot(x, y, 10, "#efe6d2", round(15.8 + .07 * k, 2)) for k, (x, y) in enumerate(((585, 380), (620, 350), (668, 372), (700, 410), (600, 440), (650, 470)))] + \
          [_poly([(x - 9, y - 6), (x + 7, y - 9), (x + 10, y + 5), (x - 4, y + 9)], "#6a7480", "#9fd0ff", 1.5, round(17.0 + .07 * k, 2), fx="pop") for k, (x, y) in
           enumerate(((560, 410), (690, 360), (720, 455), (615, 500), (680, 505)))] + \
          [dot(x, y, 4.5, "#0b0908", round(18.1 + .03 * k, 2)) for k, (x, y) in enumerate(scatter(14, 560, 720, 340, 510, 8))] + \
          [line([[230, 905], [300, 868], [380, 858], [430, 872]], 20.6, "#efe6d4", 10, curve=True, dur=.6),
           line([[470, 940], [600, 932]], 20.9, "#efe6d4", 9, draw=False), dot(466, 940, 9, "#efe6d4", 20.9), dot(604, 932, 9, "#efe6d4", 20.9),
           label(330, 975, "mammoth", 21.2, BONE, 28)] + \
          [_poly([(x, 862), (x + 14, 892), (x + 10, 932), (x, 944), (x - 10, 932), (x - 14, 892)], "#c9c3b5", "#f5ecdc", 1.5, round(22.0 + .2 * k, 2), fx="pop") for k, x in enumerate((700, 760, 820))] + \
          [line([[x, 880], [x, 920]], round(22.1 + .2 * k, 2), "#7d7668", 2, draw=False) for k, x in enumerate((700, 760, 820))] + \
          [label(760, 985, "Clovis points", 22.6, BONE, 28)] + \
          [line([[230, 705], [300, 668], [380, 658], [430, 672]], 24.4, BONE, 3, "claimed", .5, True),
           _poly([(760, 662), (774, 692), (770, 732), (760, 744), (750, 732), (746, 692)], "none", BONE, 2.5, 24.6, style="claimed"),
           strike(240, 720, 420, 650, 25.4), strike(730, 750, 790, 655, 25.6)]
    return {"base": "dark", "cam": [1.05, 500, 900], "els": els}


def _core():
    """5 · Greenland's ice: snow piling up year on year, a core read like tree rings; at the start of the cold, platinum jumps
    (a metal rare at Earth's surface, richer in some rocks from space: a clue, not a signature)."""
    yb = 900
    dome = _poly([(70, 525), (120, 450), (210, 392), (320, 372), (430, 392), (520, 450), (570, 525)], ICE, "#ffffff", 2, .3, True, fx="rise")
    snow = [dot(x, y, 4, "#ffffff", round(4.6 + .08 * k, 2), op=.9) for k, (x, y) in enumerate(scatter(6, 120, 230, 270, 350, 3) + scatter(6, 420, 540, 270, 350, 4))]
    layers = [line([[287, y], [373, y]], round(5.4 + .022 * k, 3), "#9cb8cc", 1.2, draw=False) for k, y in enumerate(range(1330, 568, -9))]
    rng = random.Random(4)
    pt = []
    for y in range(1336, 562, -14):
        x = 450 + rng.uniform(0, 26)
        if abs(y - yb) < 10:
            x = 840
        elif abs(y - yb) < 24:
            x = 560
        pt.append([round(x, 1), y])
    ring_els = [dot(770, 445, 100, "#a8845c", 11.2, fx="fade")] + [ring(770, 445, r, round(11.4 + .12 * k, 2), "#6b4f35", 2.5, dur=.3) for k, r in enumerate((18, 34, 50, 64, 78, 92))]
    rock = _poly([(720, 1170), (750, 1140), (800, 1138), (830, 1165), (820, 1205), (770, 1222), (728, 1205)], "#7d6a58", "#e9d3ab", 2, 21.4, True, fx="pop")
    els = [dome, label(320, 335, "Greenland", 3.0, "#e6eef6", 32),
           line([[330, 530], [330, 562]], 1.2, BONE, 2, "inferred", .4),
           box(285, 562, 90, 778, "#d6e6f1", "#ffffff", 2, 6, 1.4, fx="rise")] + snow + layers + ring_els + \
          [box(281, yb - 8, 98, 16, AU, r=3, at=15.0, fx="pop"), label(266, yb + 10, "12,900", 15.2, AU, 30, "end"),
           line([[440, 1340], [440, 560]], 15.6, "#e9dccb", 2, dur=.6), line(pt, 16.0, AU, 3.5, dur=1.4),
           label(828, yb - 28, "platinum", 17.0, AU, 32, "end"), glow(840, yb, 60, 17.2, .8, "lamp"),
           rock] + [dot(x, y, 3.5, AU, round(21.6 + .1 * k, 2)) for k, (x, y) in enumerate(((760, 1165), (792, 1180), (775, 1198)))] + \
          [line([[790, 1132], [830, 960], [842, 916]], 22.2, LILAC, 2.5, "claimed", .7, True), label(775, 1275, "from space?", 22.6, LILAC, 30)]
    return {"base": "dark", "stars": 50, "cam": [1.05, 500, 880], "els": els}


def _test():
    """6 · the tests: no crater of the right age; one blast should give one date everywhere, but the sites scatter; papers retracted."""
    R = 1110
    xs = [500, 300, 690, 410, 820, 230, 506, 610, 360, 760]
    ys = [800 + 30 * k for k in range(10)]
    els = [_poly([(110, 470), (890, 470), (890, 560), (110, 560)], "#3a2f26", "none", 0, .2), line([[110, 470], [890, 470]], .2, "#8c7152", 3, draw=False),
           line([[340, 470], [400, 512], [500, 528], [600, 512], [660, 470]], 1.2, LILAC, 3, "claimed", .8, True)] + question(500, 440, 2.6, 70) + \
          [line([[140, R], [860, R]], 4.8, "#e9dccb", 2.5, dur=.8),
           line([[500, 770], [500, R + 10]], 5.8, AU, 3, dur=.6), label(500, R + 52, "12,900", 6.0, AU, 30)] + \
          [{"k": "circle", "x": 500, "y": y, "r": 11, "fill": "rgba(201,193,238,.18)", "c": LILAC, "w": 2, "in": round(8.4 + .07 * k, 2)} for k, y in enumerate(ys)] + \
          [line([[150, y], [850, y]], round(12.0 + .1 * k, 2), "#5a4e44", 1.2, draw=False, op=.7) for k, y in enumerate(ys)] + \
          [dot(x, y, 11, AU, round(12.4 + .12 * k, 2)) for k, (x, y) in enumerate(zip(xs, ys))]
    sheets = []
    for k, (dx, dy) in enumerate(((-70, 10), (0, 0), (70, 14))):
        cx, cy = 500 + dx, 1300 + dy
        a = math.radians((-8, 2, 10)[k])
        rot = lambda u, v: [round(cx + u * math.cos(a) - v * math.sin(a), 1), round(cy + u * math.sin(a) + v * math.cos(a), 1)]
        sheets.append(_poly([rot(-70, -90), rot(70, -90), rot(70, 90), rot(-70, 90)], "#efe6d2", "#b8a888", 1.5, round(16.0 + .2 * k, 2), fx="rise"))
        sheets += [line([rot(-48, -60 + 18 * j), rot(48, -60 + 18 * j)], round(16.1 + .2 * k, 2), "#8a7a66", 2, draw=False, op=.7) for j in range(7)]
    els += sheets + [strike(400, 1390, 610, 1200, 17.8, RED, 8)]
    return {"base": "dark", "stars": 40, "cam": [1.06, 500, 900], "els": els}


def _belt():
    """7 · the Atlantic as a conveyor belt: warm salty water north, cooling, sinking, pulling more warmth behind; a lid of fresh
    meltwater stops the sinking, the belt slows, the north turns cold."""
    sea = _poly([(50, 620), (840, 620), (840, 1180), (790, 1240), (460, 1270), (140, 1240), (50, 1180)], "#1d3a4a", "#5fa8c9", 2, -1)
    north = [_poly([(828, 622), (858, 598), (952, 590), (952, 652), (840, 652)], "#4a3b2e", "#8c7152", 2, -1),
             _poly([(845, 602), (862, 558), (895, 526), (930, 516), (952, 530), (954, 596)], ICE, "#ffffff", 2, -1, True)]
    loop = [[140, 680], [780, 680], [810, 1150], [170, 1180]]
    snow = []
    for k, (x, y) in enumerate(((660, 420), (760, 470), (580, 500), (720, 360), (840, 410))):
        snow += [line([[x - 14 * math.cos(a), y - 14 * math.sin(a)], [x + 14 * math.cos(a), y + 14 * math.sin(a)]], round(21.2 + .15 * k, 2), "#e6f4ff", 2.5, draw=False) for a in (0, math.pi / 3, 2 * math.pi / 3)]
    lid = [_poly([(x0, 618), (x0 + 92, 618), (x0 + 92, 646), (x0, 646)], "rgba(191,230,245,.85)", "none", 0, round(14.2 + .18 * k, 2)) for k, x0 in enumerate(range(748, 300, -92))]
    els = [sea, line([[50, 620], [840, 620]], -1, "#9fd0ff", 2, draw=False)] + north + \
          [label(60, 590, "south", .3, BONE, 28, "start"), label(950, 476, "north", .3, BONE, 28, "end"),
           glow(900, 560, 80, 1.2, .7, "scan"),
           glow(160, 450, 110, 2.6, .9, "sun"), dot(160, 450, 26, "#ffe2b4", 2.6),
           line(loop + [loop[0]], 3.6, BONE, 2, "inferred", 1.4, True, op=.35),
           arrow([[140, 690], [380, 672], [620, 676], [760, 700]], 5.8, WARM, 6, dur=1.4), glow(760, 700, 50, 8.0, .9, "scan"),
           arrow([[780, 715], [810, 860], [810, 1010], [790, 1140]], 8.8, BLUE, 6, dur=1.0),
           arrow([[760, 1185], [470, 1215], [180, 1185]], 9.8, BLUE, 5, dur=1.2),
           arrow([[150, 1160], [110, 920], [130, 720]], 10.6, WARM, 4, "inferred", .9),
           arrow([[150, 726], [330, 714], [470, 716]], 11.2, WARM, 3, dur=.8)] + \
          [glow(900, 560, 80, 13.0, .8, "scan")] + \
          [arrow([[880, 588], [850, 604], [820, 616]], 13.4, "#cfe6ff", 4, dur=.5), arrow([[905, 596], [872, 610], [842, 619]], 13.7, "#cfe6ff", 4, dur=.5)] + lid + \
          [label(600, 598, "fresh meltwater", 16.4, "#bfe6f5", 28),
           strike(770, 900, 850, 820, 19.4), strike(770, 820, 850, 900, 19.6),
           glow(800, 450, 190, 21.0, .7, "scan")] + snow + [glow(600, 632, 170, 24.2, .5, "lamp")]
    return {"base": "dark", "stars": 60, "cam": [1.08, 500, 850], "els": els}


def sky_fell():
    S0 = _thermo()
    S1 = _sea()
    S2 = like(S0, cam=[1.3, 600, 900], add=_dryas())
    S3 = _claim()
    S4 = _dig()
    S5 = _core()
    S6 = _test()
    S7 = _belt()
    S8 = like(S2, cam=[1.05, 500, 880], add=_sky_verdict())
    shots = [S0, S1, S2, S3, S4, S5, S6, S7, S8]
    beats = [
        B("hook", 0, ["[d:intrigue][k:C. 12,900 YEARS AGO][sfx:boom][act:ominous, measured]The Ice Age was ^ending. [act:the turn, darker][tune:fall]Then the cold came ^*back*.",
                      "[d:tension][p:0.93][act:letting it sink in]About {12,900|twelve thousand nine hundred} years ago, the world plunged back into the ^freeze, for {1,200|twelve hundred} ^years. "
                      "[act:a hushed tease][tune:level]Some scientists blame... [act:the reveal, quiet][tune:fall]the ^*sky*."], cut=False),
        B("world", 1, ["[d:calm][k:REWIND][act:brisk storytelling]^Rewind. [p:0.93][act:setting the scene]At the height of the Ice Age, so much water was locked up in ^ice "
                       "that the sea sat {134|a hundred and thirty-four} metres ^*lower*. [act:giving a sense of scale]That's about the height of a forty-storey ^tower.",
                       "[d:build][act:momentum building]Then the ice ^melted, the seas ^climbed, [act:wonder][tune:fall]and people walked into ^*new* lands."]),
        B("collision", 2, ["[d:tension][k:THE YOUNGER DRYAS][act:ominous, naming it]Scientists call this cold snap the Younger ^Dryas, [act:a small, vivid picture]after a little Arctic ^flower "
                           "that came back to northern Europe with the ^cold.",
                           "[d:build][go:3|1.6][p:1.03][act:presenting the bold claim]One group of scientists says a ^*comet* did it. [sfx:boom][act:vivid, quick][tune:level]Blasts in the sky, over North ^America. "
                           "[act:vivid, quick][tune:level]^Fires. [act:low, final][tune:fall]Mammoths, ^gone."]),
        B("cost", 4, ["[d:build][k:THE CLUES][act:fair, taking it seriously]And there ^*are* clues. [p:0.93][act:explaining, an everyday picture]Dig down, and the ground reads like a stack of ^pages: "
                      "the deeper, the ^older. [act:laying out evidence]Right at the start of the cold, the comet team reported a thin ^layer: tiny round ^beads, magnetic ^grains, and ^soot. "
                      "[act:steady]Just below it lie mammoth bones and Clovis spear ^points. [act:the turn, quieter][tune:fall]Within a few ^centuries, they're gone.",
                      "[d:wonder][go:5|1.4][act:intrigued]There's even a ^*platinum* spike in the Greenland ^ice. [p:0.93][act:explaining, clear]Snow piles up there year after year and turns to ^ice, "
                      "so a core drilled through it reads like tree ^rings. [act:precise, leaning in]And right at the start of the cold, platinum ^jumps: "
                      "[act:explaining]a metal rare at Earth's ^surface, but richer in some rocks from ^space."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:the turn, careful][tune:fall]But no ^crater of the right age has been ^found. [p:0.93][act:explaining, the test]And one blast means one ^moment, "
                          "so its layer should carry the same date ^everywhere. [act:plain, sober]When other teams checked the dates, most sites didn't ^match. "
                          "[act:plain, sober]And key impact papers were [stamp:RETRACTED · 2025-26|red]^*retracted*.",
                          "[d:calm][go:7|1.4][act:the mainstream view, clear]Most specialists blame ^meltwater. [p:0.93][act:explaining, an everyday picture]The Atlantic works like a conveyor ^belt: "
                          "warm, salty water flows north, cools, grows heavy and ^sinks, pulling more warmth behind it. [act:explaining, clear]Pour a flood of fresh meltwater on ^top, "
                          "and it floats like a ^lid. [act:the payoff][tune:fall]The belt slows, and the north turns ^cold again. [d:aside][act:dry, a small smile]Less ^cinematic. "
                          "[act:quietly firm]Better ^*evidence*."]),
        B("tag", 8, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing each part][tune:rise]The ^cold? [act:firm][tune:highfall]^*Real*. [act:even][tune:rise]A ^comet behind it? "
                     "[act:the verdict, fair][tune:fall]*Awaiting ^evidence*. [act:practical, clear]A crater of the right ^age, or one layer with one date ^everywhere, would change ^that.",
                     "[d:tension][p:0.93][act:quiet intrigue][tune:level]Until then, the ^sky... [act:a wink of suspense][tune:fall]is still a ^*suspect@noun*."]),
    ]
    return EP03("sky-fell", "03.01", "Did a comet end the Ice Age world?", "younger-dryas-impact", "unsupported", "A comet triggered the Younger Dryas cold?",
                "12,900 years ago, the cold *came back*.", beats, shots,
                "Firestone et al. 2007 · Petaev et al. 2013 · Meltzer et al. 2014, all PNAS",
                "12,900 years ago the world froze again. Did a comet do it? The clues, the retractions, and the verdict.",
                ["#YoungerDryas", "#IceAge", "#Comet", "#Prehistory", "#WeighItYourself"])


def sky_fell_m():
    """The Younger Dryas as one continuous take (see mural.py): the thermometer of the past plunges, the sea sits 134 m lower and
    climbs, the cold gets its flower's name, the comet claim is drawn dotted over North America, the dig, the ice core and its
    platinum, the tests (no crater, scattered dates, retractions), the Atlantic's conveyor stalled by a lid of meltwater, and the verdict."""
    from mural import remix
    return remix(sky_fell(), alias={2: 0, 8: 0},
                 beat_adds={2: (_dryas(), [1.3, 600, 900]), 5: (_sky_verdict(), [1.05, 500, 880])},
                 line_adds={(5, 1): ([], [1.55, 670, 620])})


# ================================================================ 02.02 The First Signs (ice-age-signs)
WALL = "#7a5c44"


def _sign(k, x, y, at, c=CREAM, s=1.0):
    """32 simple signs: the 16 of f02._glyph and 16 more (open angle, roof, feather, club, heart, comb, fan, half circle, oval,
    bean, crosshatch, cross with bars, hand, finger lines, hook, star)."""
    if k < 16:
        return _glyph(k, x, y, at, c, s)
    q = lambda pts: [[round(x + a * s, 1), round(y + b * s, 1)] for a, b in pts]
    L = lambda pts, curve=False: {"k": "line", "p": q(pts), "c": c, "w": 3, "curve": curve, "in": at}
    k -= 16
    if k == 0: return [L([(12, -14), (-12, 0), (12, 14)])]
    if k == 1: return [L([(-14, 14), (-14, -2), (0, -14), (14, -2), (14, 14)])]
    if k == 2: return [L([(0, 14), (0, -14)])] + [L([(0, -8 + 8 * j), (-9, -14 + 8 * j)]) for j in range(3)] + [L([(0, -8 + 8 * j), (9, -14 + 8 * j)]) for j in range(3)]
    if k == 3: return [L([(0, 14), (0, -4)]), {"k": "circle", "x": x, "y": round(y - 8 * s, 1), "r": round(6 * s, 1), "fill": c, "c": "none", "w": 0, "in": at}]
    if k == 4: return [L([(0, 13), (-13, -2), (-10, -12), (-3, -13), (0, -7), (3, -13), (10, -12), (13, -2), (0, 13)], True)]
    if k == 5: return [L([(-14, -10), (14, -10)])] + [L([(-12 + 6 * j, -10), (-12 + 6 * j, 10)]) for j in range(5)]
    if k == 6: return [L([(0, 14), (-14 * math.cos(a), 14 - 26 * math.sin(a))]) for a in (math.radians(d) for d in (20, 55, 90, 125, 160))]
    if k == 7: return [L([(-14, 6), (-10, -4), (0, -9), (10, -4), (14, 6)], True), L([(-14, 6), (14, 6)])]
    if k == 8: return [{"k": "poly", "p": [[round(x + 10 * s * math.cos(t), 1), round(y + 15 * s * math.sin(t), 1)] for t in (j * math.pi / 8 for j in range(16))],
                        "fill": "none", "c": c, "w": 3, "curve": True, "in": at}]
    if k == 9: return [L([(-12, 4), (-8, -8), (4, -10), (12, -2), (6, 8), (-2, 4), (-8, 10), (-12, 4)], True)]
    if k == 10: return [L([(-14, -5), (14, -5)]), L([(-14, 5), (14, 5)]), L([(-5, -14), (-5, 14)]), L([(5, -14), (5, 14)])]
    if k == 11: return [L([(-14, 0), (14, 0)]), L([(0, -14), (0, 14)]), L([(-14, -5), (-14, 5)]), L([(14, -5), (14, 5)]), L([(-5, -14), (5, -14)])]
    if k == 12:
        h = hand(x, y, .085 * s, c); h["in"] = at; return [h]
    if k == 13: return [L([(-8 + 8 * j, -14), (-10 + 8 * j, 0), (-7 + 8 * j, 14)], True) for j in range(3)]
    if k == 14: return [L([(-6, 14), (-6, -6), (0, -13), (8, -9)], True)]
    return [L([(-14 * math.cos(a), -14 * math.sin(a)), (14 * math.cos(a), 14 * math.sin(a))]) for a in (j * math.pi / 4 for j in range(4))]


def _zig(x, y, w, h, at, c=CREAM, n=7, sw=4, dur=.8):
    return line([[round(x - w / 2 + w * j / (n - 1), 1), y + (h / 2 if j % 2 else -h / 2)] for j in range(n)], at, c, sw, dur=dur)


def _grid(x, y, s, at, c=CREAM, n=4, sw=3):
    return [line([[x - s, y - s + 2 * s * j / (n - 1)], [x + s, y - s + 2 * s * j / (n - 1)]], round(at + .05 * j, 2), c, sw, dur=.3) for j in range(n)] + \
           [line([[x - s + 2 * s * j / (n - 1), y - s], [x - s + 2 * s * j / (n - 1), y + s]], round(at + .2 + .05 * j, 2), c, sw, dur=.3) for j in range(n)]


def _dots(x, y, at, c=OCH, r=9, cols=4, rows=3, gap=30):
    return [dot(round(x + (j % cols - (cols - 1) / 2) * gap, 1), round(y + (j // cols - (rows - 1) / 2) * gap, 1), r, c, round(at + .05 * j, 2)) for j in range(cols * rows)]


def _stencil(cx, cy, s, t_on, t_spray, t_off, wall=WALL, n=220, seed=21, spread=(270, 300)):
    """A hand stencil made before our eyes: the hand pressed to the rock, red blown around it, the hand lifted."""
    h_on = hand(cx, cy, s, "#2a1d14"); h_on["in"] = t_on
    h_off = hand(cx, cy, s, wall); h_off["in"] = t_off; h_off["dur"] = .9
    rr = random.Random(seed)
    sp = []
    for k in range(n):
        a = rr.uniform(0, 2 * math.pi); d = math.sqrt(rr.uniform(0, 1))
        sp.append(dot(round(cx + spread[0] * s / 1.35 * d * math.cos(a), 1), round(cy + spread[1] * s / 1.35 * d * math.sin(a), 1), round(4 + 3 * s, 1), "#c0442c", round(t_spray + .004 * k, 3), fx="fade", op=.7))
    return [h_on, glow(cx, cy, int(380 * s / 1.35), t_spray, .95, "red")] + sp + [h_off]


def _cave():
    """0 · a cave wall in torchlight: a zigzag, dots, a grid, and a hand blown in red, as they are named."""
    wall = _poly([(70, 420), (160, 350), (340, 322), (520, 336), (700, 318), (870, 362), (935, 480), (920, 760), (940, 1020), (905, 1280), (770, 1380), (520, 1400), (290, 1380),
                  (130, 1320), (70, 1110), (90, 820), (60, 600)], WALL, "#a8865a", 2, -1, True)
    lit = _poly([(170, 470), (360, 420), (600, 430), (820, 480), (850, 760), (840, 1100), (700, 1290), (440, 1310), (220, 1250), (150, 1000), (160, 700)], "#8d6c50", "none", 0, -1, True, op=.7, keepop=True)
    cracks = [line(p, -1, "#5a4232", 2.5, curve=True, draw=False, op=.8) for p in ([[130, 560], [200, 610], [215, 700]], [[880, 520], [810, 580], [830, 680]],
                                                                                 [[400, 1320], [460, 1270], [540, 1300]], [[860, 1150], [820, 1200], [830, 1270]])]
    els = [wall, lit] + cracks + [glow(210, 1240, 300, -1, .4, "fire"),
                                  _zig(300, 560, 260, 70, .2, CREAM, 8, 6)] + _dots(690, 560, 1.0, OCH, 11) + _grid(300, 930, 110, 1.7, CREAM, 5, 4) + \
          _stencil(680, 960, .95, 2.6, 3.0, 4.2, "#8d6c50")
    return {"base": "dark", "cam": [1.0, 500, 870], "els": els}


_CONT = [((-100, 42), "zig"), ((-68, -38), "hand"), ((8, 47), "dots"), ((22, -20), "grid"), ((120, -2), "hand"), ((135, -27), "dots")]


def _badge(x, y, kind, at, r=32):
    out = [dot(x, y, r, "#1c140e", at), ring(x, y, r, at, "#a8865a", 2, dur=.4)]
    if kind == "zig":
        out.append(_zig(x, y, 40, 16, at + .1, CREAM, 6, 3, .4))
    elif kind == "dots":
        out += _dots(x, y, at + .1, OCH, 4.5, 3, 2, 12)
    elif kind == "grid":
        out += _grid(x, y, 14, at + .1, CREAM, 4, 2)
    else:
        h = hand(x, y + 2, .13, "#c0442c"); h["in"] = at + .1; out.append(h)
    return out


def _world():
    """1 · the world: the same shapes on every inhabited continent; each its own spark, or one lost source (drawn dotted)."""
    v = View(-170, 180, -56, 75, (40, 700, 920, 520))
    pts = [v.p(*ll) for ll, _ in _CONT]
    src = (500, 545)
    els = [e for k, ((x, y), (_, kind)) in enumerate(zip(pts, _CONT)) for e in _badge(x, y, kind, round(.8 + .38 * k, 2))] + \
          [glow(x, y, 60, round(6.4 + .1 * k, 2), .9, "lamp") for k, (x, y) in enumerate(pts)] + \
          [line([[src[0], src[1] + 40], [x, y - 34]], round(8.8 + .12 * k, 2), LILAC, 2.5, "claimed", .6) for k, (x, y) in enumerate(pts)] + \
          [dot(src[0], src[1], 40, "#120d0a", 7.6), ring(src[0], src[1], 40, 7.6, LILAC, 3, "claimed"), label(src[0], src[1] + 24, "?", 11.0, LILAC, 64, st="big")]
    return mapshot(v, extra=els, cam=[1.1, 500, 840])


def _tx(ya):
    """The long ruler: 500,000 years ago at x 110, today at x 890."""
    return round(890 - 780 * ya / 500000, 1)


_RY = 990


def _ruler():
    """2 · writing, and everything before it: a clay tablet; the last half-million years on one line, writing a sliver at its end;
    everything older filed in a drawer labelled 'art'."""
    els = [box(720, 380, 140, 180, "#b89a72", "#e9d3ab", 2, 14, 1.2, fx="rise"),
           {"k": "glyphs", "x": 738, "y": 400, "w": 104, "h": 140, "rows": 6, "cols": 5, "kind": "cuneiform", "c": "#3a2a1c", "in": 5.0},
           line([[905, 330], [852, 404]], 5.2, "#c9a370", 6, draw=False), label(790, 604, "writing", 1.8, AU, 32),
           line([[110, _RY], [890, _RY]], 7.6, "#e9dccb", 3, dur=1.4)] + \
          [line([[x, _RY - 10], [x, _RY + 10]], 8.4, "#e9dccb", 2, draw=False) for x in (110, 500, 890)] + \
          [label(110, _RY + 50, "500,000 years ago", 8.6, "#cbbca8", 28, "start"), label(890, _RY + 50, "today", 8.6, "#cbbca8", 28, "end"),
           box(881, _RY - 14, 9, 28, AU, r=2, at=12.0, fx="pop"), glow(885, _RY, 70, 12.0, .9, "lamp"),
           line([[835, 624], [884, _RY - 22]], 12.4, AU, 2, "inferred", .6),
           line([[110, _RY - 34], [874, _RY - 34]], 15.4, BONE, 2, "inferred", .8), line([[110, _RY - 44], [110, _RY - 24]], 15.4, BONE, 2, draw=False), line([[874, _RY - 44], [874, _RY - 24]], 16.0, BONE, 2, draw=False),
           box(110, 1080, 764, 160, "#5a4632", "#c9ad85", 2, 10, 16.4, fx="rise"), box(445, 1172, 110, 22, "#c9ad85", r=10, at=16.8),
           label(500, 1146, "art", 17.2, BONE, 40, st="serif")] + question(760, 1190, 19.8, 60)
    return {"base": "dark", "cam": [1.08, 500, 900], "els": els}


_SPOTS = [  # (years ago, icon kind, icon x, icon y, place)
    (430000, "zig", 219, 770, "Java"),
    (73000, "grid", 500, 790, "South Africa"),
    (67800, "hand", 640, 680, "Sulawesi"),
    (25000, "dots", 760, 790, "Europe"),
]
_HEAD = [(-70, -10), (-66, -58), (-38, -90), (8, -96), (50, -78), (70, -44), (74, -18), (90, 4), (74, 14), (78, 32), (68, 46), (64, 66), (34, 78), (10, 82), (6, 104), (-34, 104), (-44, 62), (-68, 22)]


def _head(x, y, s, at, fill="#1c140e", c=AMBER, w=3):
    return _poly([(x + a * s, y + b * s) for a, b in _HEAD], fill, c, w, at, True, fx="pop")


def _icon(kind, x, y, at):
    if kind == "zig":
        return [_zig(x, y, 70, 26, at, CREAM, 7, 4, .5)]
    if kind == "grid":
        return [line([[x - 26 + 10 * j, y - 24], [x - 30 + 10 * j, y + 24]], round(at + .05 * j, 2), "#c0442c", 3.5, dur=.25) for j in range(6)] + \
               [line([[x - 34, y - 12 + 14 * j], [x, y - 14 + 14 * j], [x + 34, y - 10 + 14 * j]], round(at + .35 + .05 * j, 2), "#c0442c", 3.5, dur=.25, curve=True) for j in range(3)]
    if kind == "hand":
        h = hand(x, y + 4, .2, "#c0442c"); h["in"] = at; return [glow(x, y, 50, at, .8, "red"), h]
    return _dots(x, y, at, OCH, 6, 4, 3, 18)


def _signs_verdict():
    """(on the long ruler) one lost source? drawn dotted, with the trail it would leave; then the real dates, scattered over
    continents and over 400,000 years, and our species too young for the oldest."""
    src = (400, 470)
    els = [dot(src[0], src[1], 26, "#120d0a", .6), ring(src[0], src[1], 26, .6, LILAC, 3, "claimed"), label(src[0], src[1] + 16, "?", 1.0, LILAC, 44, st="big")] + \
          [{"k": "circle", "x": src[0], "y": src[1], "r": r, "fill": "none", "c": LILAC, "w": 2.5, "style": "claimed", "in": round(11.4 + .35 * j, 2)} for j, r in enumerate((44, 60, 76))]
    for k, (ya, kind, x, y, place) in enumerate(_SPOTS):
        at = round(13.8 + .9 * k, 2)
        X = _tx(ya)
        els += _icon(kind, x, y, at) + [label(x, y + 58, place, at + .2, BONE, 28),
                                         line([[x, y + 72], [X, _RY - 12]], at + .3, AU, 2, "inferred", .5), dot(X, _RY, 8, AU, at + .4)]
    els += [box(_tx(40000), _RY - 7, _tx(10000) - _tx(40000), 14, AU, r=6, at=16.8, op=.9)]
    els += [box(_tx(300000), _RY + 12, 890 - _tx(300000), 10, BONE, r=5, at=20.4, op=.8, fx="pop"), label(_tx(300000) + 8, _RY + 50, "our species", 20.6, BONE, 28, "start"),
            ring(_tx(430000), _RY, 22, 21.6, AU, 3)]
    return els


def _signs_mind():
    """(line 2 of the verdict) one kind of mind: a head where the lost source was, and the same head beside every sign."""
    src = (400, 470)
    els = [_head(src[0], src[1], 1.15, .8)] + [_zig(src[0] + 6, src[1] - 30, 60, 18, 1.4, CREAM, 6, 3, .4)] + _dots(src[0] + 6, src[1] + 8, 1.6, OCH, 4, 4, 1, 14) + \
          [_head(x - 52, y - 28, .3, round(2.4 + .3 * k, 2), "#1c140e", AMBER, 2) for k, (_, _, x, y, _) in enumerate(_SPOTS)] + \
          [glow(src[0], src[1], 150, 5.6, .6, "lamp"), glow(src[0], src[1], 120, 8.4, .5, "scan")]
    return els


def _petz():
    """3 · Ice Age Europe: cave after cave, every sign logged; just 32 of them, repeated for thirty thousand years."""
    caves = []
    for k, x in enumerate((200, 350, 500, 650, 800)):
        caves += [_poly(ellipse(x, 500, 52, 64, 18, 180, 360), "#120d0a", "#8c7152", 2.5, round(.4 + .35 * k, 2), True, fx="pop")]
        caves += [dot(x + 6, 478, 6, AU, round(4.8 + .5 * k, 2))]
    grid = []
    for k in range(32):
        x, y = 150 + 100 * (k % 8), 660 + 92 * (k // 8)
        grid += _sign(k, x, y, round(8.2 + .045 * k, 3), CREAM, 1.25)
    rep_k = [5, 12, 26, 28, 5, 12, 26, 28]
    rep = [e for j, kk in enumerate(rep_k) for e in _sign(kk, 190 + 89 * j, 1150, round(12.0 + .18 * j, 2), AMBER, .95)]
    els = caves + [person(110, 560, 84, 3.4, "#e8d6b8"), line([[140, 556], [880, 556]], 4.6, BONE, 2, "inferred", 2.4)] + grid + \
          [label(500, 1040, "32 signs", 9.4, AU, 36, st="serif"),
           line([[150, 1210], [850, 1210]], 11.6, BONE, 3, dur=.8), line([[150, 1198], [150, 1222]], 11.6, BONE, 2.5, draw=False), line([[850, 1198], [850, 1222]], 12.2, BONE, 2.5, draw=False),
           label(500, 1265, "30,000 years", 12.8, AU, 32)] + rep
    return {"base": "dark", "cam": [1.0, 500, 880], "els": els}


def _sulawesi():
    """4 · Sulawesi: a hand stencil made before our eyes; then water seeps down and a thin mineral crust grows over it, carrying a
    uranium clock: the crust is younger than the hand beneath, so its age is a minimum."""
    W = "#8a6a4e"
    crust = [(520, 600), (600, 590), (690, 640), (720, 760), (690, 880), (610, 920), (540, 860), (505, 720)]
    els = [box(120, 430, 760, 860, W, "#a8865a", 2, 22, .2), label(500, 395, "Sulawesi", 3.0, BONE, 32)] + \
          _stencil(480, 870, 1.35, 4.2, 4.8, 6.0, W) + \
          [label(500, 1370, "at least 67,800 years", 7.4, AU, 36, st="serif")] + question(250, 560, 9.6, 64) + \
          [line([[600 + 8 * math.sin(j), 440 + 26 * j] for j in range(7)], 11.8, BLUE, 3, "inferred", .8, True),
           line([[668 + 8 * math.sin(j + 1), 440 + 30 * j] for j in range(7)], 12.2, BLUE, 3, "inferred", .8, True),
           dot(604, 610, 6, BLUE, 12.6), dot(672, 630, 6, BLUE, 12.9),
           _poly(crust, "rgba(240,236,226,.26)", "rgba(255,250,240,.75)", 2, 14.4, True, fx="fill", dur=1.4),
           line([[530, 640], [600, 610], [680, 650]], 15.4, "rgba(255,250,240,.6)", 2, curve=True, draw=False),
           dot(780, 560, 34, "#1a1511", 20.4), ring(780, 560, 34, 20.4, AU, 3, dur=.5), line([[780, 560], [780, 536]], 20.7, AU, 3, draw=False), line([[780, 560], [797, 568]], 20.7, AU, 3, draw=False),
           glow(780, 560, 70, 20.6, .6, "lamp"),
           label(732, 680, "younger", 23.2, "#f5ecdc", 30, "start"), label(330, 1150, "older", 26.2, BONE, 30),
           line([[330, 1392], [670, 1392]], 28.2, AU, 3, dur=.6)]
    return {"base": "dark", "cam": [1.0, 500, 880], "els": els}


def _blombos():
    """5 · South Africa: on a flake of stone, a few crossed red lines drawn with a lump of ochre."""
    flake = [(260, 760), (340, 660), (520, 620), (700, 660), (760, 780), (720, 960), (560, 1040), (360, 1010), (270, 900)]
    RD = "#c0442c"
    els = [label(500, 470, "South Africa", .4, BONE, 32),
           _poly(flake, "#b9ab94", "#efe6d2", 2, .6, True, fx="rise"),
           line([[340, 700], [470, 760], [560, 730]], .8, "#8f8371", 2, curve=True, draw=False, op=.5), line([[300, 900], [450, 860], [600, 960]], .8, "#8f8371", 2, curve=True, draw=False, op=.5)] + \
          [line([[392 + 34 * k, 730], [374 + 34 * k, 965]], round(2.0 + .14 * k, 2), RD, 5, dur=.3) for k in range(6)] + \
          [line([[350, 790 + 64 * j], [470, 768 + 64 * j], [610, 798 + 64 * j]], round(2.9 + .22 * j, 2), RD, 5, dur=.4, curve=True) for j in range(3)] + \
          [_poly([(730, 1070), (790, 1040), (835, 1068), (826, 1138), (776, 1168), (734, 1138)], "#a8452c", "#e9a080", 2, 5.0, True, fx="pop"),
           line([[738, 1074], [790, 1046]], 5.2, "#e9a080", 3, draw=False),
           line(flake + [flake[0]], 7.0, AU, 3, dur=1.0, curve=True),
           label(500, 1250, "73,000 years", 8.8, AU, 40, st="serif")]
    return {"base": "dark", "cam": [1.0, 500, 880], "els": els}


def _java():
    """6 · Java: a zigzag scratched into a mussel shell, at least 430,000 years ago, by Homo erectus; our species not yet born."""
    SHELL = [[240, 860], [300, 700], [460, 620], [640, 640], [760, 740], [780, 880], [700, 1000], [500, 1040], [330, 990]]
    ZZ = [[330 + k * 34, 820 + (-1) ** k * 40] for k in range(11)]
    els = [_poly(SHELL, "#6a6258", "#c9c0ae", 2, .3, True, fx="rise")] + \
          [line([[300 + k * 30, 700 + k * 30], [760 - k * 20, 760 + k * 25]], .5, "#8a8074", 1, curve=True, draw=False, op=.5) for k in range(6)] + \
          [_poly([(700, 760), (720, 724), (728, 770)], "#efe6d2", "#8a7a66", 1.5, .8, fx="pop"),
           line(ZZ, 1.0, CREAM, 4, dur=1.6), label(500, 560, "Java", 3.2, BONE, 32),
           label(500, 1110, "at least 430,000 years", 6.8, AU, 38, st="serif"),
           person(230, 1390, 200, 9.6, "#c9b49a"), glow(230, 1290, 150, 9.6, .3), label(230, 1165, "Homo erectus", 10.0, AU, 30),
           _ghost_person(770, 1390, 200, 12.0), label(770, 1165, "us: not yet", 12.4, "#cbbca8", 30)]
    return {"base": "dark", "cam": [1.0, 500, 880], "els": els}


def ice_age_signs():
    S0 = _cave()
    S1 = _world()
    S2 = _ruler()
    S3 = _petz()
    S4 = _sulawesi()
    S5 = _blombos()
    S6 = _java()
    S7 = like(S2, cam=[1.0, 500, 870], add=_signs_verdict())
    shots = [S0, S1, S2, S3, S4, S5, S6, S7]
    beats = [
        B09("hook", 0, ["[d:list][k:THE SAME SIGNS][sfx:shimmer][act:laying them out, one by one][tune:level]^Zigzags. [act:same rhythm][tune:level]^Dots. [act:same rhythm][tune:level]^Grids. "
                        "[act:vivid][tune:fall]Hands, blown in ^*red*.",
                        "[d:intrigue][go:1|1.4][act:intrigued, emphatic]The same shapes turn up on ^*every* inhabited continent, on cave walls and rock ^shelters. [act:teasing][tune:rise]^Coincidence? "
                        "[act:a hint of mystery][tune:rise]Or a ^*lesson*, taught to the whole world by one lost ^culture?"], cut=False),
        B09("world", 2, ["[d:calm][k:WHERE WRITING BEGINS][act:the textbook view, plain]Writing starts about {5,300|five thousand three hundred} years ago, in ^Mesopotamia: signs pressed into ^clay. "
                         "[p:0.93][act:explaining, a picture]Put the last half-million years on one ^line, and writing is this thin ^sliver at the very end.",
                         "[d:aside][act:wry, gently critical]Everything older gets filed under ^'art', as mere ^decoration. [act:a thoughtful doubt]Maybe too ^*quickly*."]),
        B09("collision", 3, ["[d:build][k:ICE AGE EUROPE][act:admiring a patient researcher]In the Ice Age caves of ^Europe, the researcher Genevieve von Petzinger logged every sign, cave after ^cave. "
                             "[act:the surprise][tune:fall]She found just ^*thirty-two* of them. [p:0.93][act:slower, letting it land]The same thirty-two, repeated for thirty ^thousand years."]),
        B09("cost", 4, ["[d:build][k:OLDER][act:going deeper, building]Go further ^back. [act:precise, impressed]On the island of Sulawesi, a hand stencil is at least {67,800|sixty-seven thousand eight hundred} years ^old. "
                        "[p:0.93][act:curious, the method]How can paint be ^dated? [act:explaining, an everyday picture]Water seeping down the rock leaves a thin mineral crust over it, like scale in a ^kettle, "
                        "and that crust carries a natural uranium ^clock. [act:clear, the logic]The crust grew on ^top, so the hand beneath must be ^older. [act:landing it][tune:fall]Hence: at ^least.",
                        "[d:wonder][go:5|1.4][act:wonder, softly]In South Africa, a few crossed red lines, drawn with a lump of ^ochre on a flake of ^stone: "
                        "[tune:fall]{73,000|^seventy-three thousand} years ago."]),
        B09("reversal", 5, ["[d:tension][k:THE TWIST][act:setting up the big one][tune:rise]And the ^oldest? [sfx:boom][go:6|1.4][act:a surprising answer]A ^zigzag, scratched into a mussel shell from ^Java.",
                            "[d:reveal][p:0.9][act:the reveal, slow]At least {430,000|^four hundred and thirty thousand} years ^old. [act:precise]Engraved by Homo ^erectus, long before our own species ^existed. "
                            "[act:quiet, pointed]Not by ^*us*."]),
        B09("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.96][act:weighing the big theory][tune:rise]One lost ^culture, teaching the world the same ^signs? [act:the verdict, even][tune:fall]*Awaiting ^evidence*. "
                       "[act:plain, decisive]The ^dates don't line up. [p:0.93][act:explaining, clear]One teacher would leave one starting ^point, and a trail spreading ^out. "
                       "[act:precise]Instead, the signs turn up at scattered dates, on different ^continents, [act:the clincher][tune:fall]and the oldest is older than our own ^species.",
                       "[d:wonder][p:0.94][act:warmer, the likelier idea][tune:rise]One kind of ^mind, drawing the same shapes, again and ^again? [act:gently sure]Far more ^likely. "
                       "[act:hushed wonder][tune:level]And ^maybe... [act:the last thought, quiet][tune:fall]the ^*bigger* mystery."]),
    ]
    return EP02("ice-age-signs", "02.02", "The same signs, everywhere", "shared-symbols", "unsupported", "One lost culture taught the world the same signs?",
                "The same signs, on *every* continent.", beats, shots,
                "Oktaviana et al. 2026, Nature · Henshilwood et al. 2018, Nature · Joordens et al. 2015, Nature",
                "Zigzags, dots, grids and red hands on every continent. One lost culture, or one kind of mind? The dates, rated.",
                ["#CaveArt", "#Prehistory", "#Archaeology", "#Symbols", "#WeighItYourself"])


def ice_age_signs_m():
    """The same signs everywhere as one continuous take (see mural.py): signs appear on a cave wall and on every continent, writing
    is a sliver at the end of half a million years, 32 signs repeat across Ice Age Europe, a stencil is made and dated through its
    crust, red lines are drawn on a flake, a zigzag is scratched on a shell by Homo erectus, and the ruler comes back for the verdict."""
    from mural import remix
    return remix(ice_age_signs(), alias={7: 2},
                 beat_adds={5: (_signs_verdict(), [1.0, 500, 870])},
                 line_adds={(5, 1): (_signs_mind(), None)})


def EPISODES():
    return [sky_fell_m(), ice_age_signs_m()]
