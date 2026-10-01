"""File 10 · Scripture and Stone II, the mural versions of four films (see mural.py): Dhul Qarnayn's barrier, the Ark, the star, the Moon.
Only physical claims are weighed: the proposed sites and walls, the chest's trail, the sky of 7 to 5 BCE, a lunar trough shared as a scar.
What the scriptures recount, and what faith holds, is framed in gold and never rated.

Times ("in") in the authored scenes below are real seconds after the camera arrives, read against the rewritten narration
(films/rewrite/<id>.json): _remix_rt undoes remix's word-count stretch for them only."""
from f10 import *
import f10 as F
import copy
import math

FAITH = "#e8c878"          # the gold of 'never rated'


def _rt(els):
    """Mark authored elements: their times are already real seconds."""
    for e in els:
        e["_rt"] = 1
    return els


def _scene(sc):
    _rt(sc["els"])
    return sc


def _remix_rt(ep, **kw):
    """remix(), then divide the marked (authored) elements' times by the stretch remix gave their step."""
    from mural import remix, _remix, step_words
    out = remix(ep, **kw)
    old = _remix(copy.deepcopy(ep), **kw)

    def walk(e, r):
        if r and e.get("_rt") and isinstance(e.get("in"), (int, float)) and e["in"] > 0:
            e["in"] = round(e["in"] / r, 2)
        e.pop("_rt", None)
        for c in e.get("els", []) or []:
            walk(c, r)
    same = len(old["shots"]) == len(out["shots"])
    wn, wo = step_words(out["beats"]), step_words(old["beats"])
    for k, sh in enumerate(out["shots"]):
        r = max(1.0, min(2.5, (wn.get(k, 0) + 3) / (wo.get(k, 0) + 3))) if same else 1.0
        for e in sh["els"]:
            walk(e, r if r > 1.05 else None)
    return out


def _gold_frame(x, y, w, h, at, sw=5, dur=2.0, op=None):
    e = {"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": 18, "fill": "none", "c": FAITH, "sw": sw, "fx": "draw", "dur": dur, "in": at}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


# ---------------------------------------------------------------- 10.06 Dhul Qarnayn
def dhul_qarnayn_m():
    """Dhul Qarnayn as one continuous take: the passes on the map, a brick's light clock, the thousand-year gap, the readings of the name
    around a gold-framed account, and the ground beneath the walls that nobody has dug. Only the sites and walls are weighed."""
    from illus import person, arrow, line, glow, label, dot, box, ring, question, strike, AMBER, BLUE, LILAC, BONE, RED as RD, GREEN
    ep = copy.deepcopy(F.dhul_qarnayn())
    # the passes: the steppe to the north, three gaps, each one shut
    v = View(39, 58, 35.5, 46, (40, 330, 920, 900))
    P = lambda lo, la: [round(c, 1) for c in v.p(lo, la)]
    gaps = [(48.29, 42.06), (44.63, 42.74), (54.5, 37.2)]
    passes = [label(*P(41.8, 45.5), "the steppe", 1.0, "#c9ad85", 34, st="ital"),
              arrow([P(46.2, 45.9), P(47.6, 44.0), P(48.0, 42.6)], 6.0, AMBER, 3, "inferred", 1.0),
              arrow([P(43.6, 45.9), P(44.3, 44.4), P(44.6, 43.2)], 6.6, AMBER, 3, "inferred", 1.0),
              arrow([P(57.5, 43.5), P(56.6, 40.0), P(55.0, 37.7)], 7.2, AMBER, 3, "inferred", 1.0)]
    passes += [ring(*P(lo, la), 26, 10.0 + .6 * k, FAITH if k < 2 else BLUE, 4, dur=.6) for k, (lo, la) in enumerate(gaps)]
    # 3 · the dates: a wall builds, one brick is fired, its light clock refills; Sasanian brick and stone, not the iron of the account
    wall = []
    for r_ in range(5):
        y = 1220 - 40 * r_
        off = 0 if r_ % 2 else 28
        for c in range(-1, 11):
            x0 = 200 + off + 56 * c; x1 = x0 + 52
            x0, x1 = max(x0, 200), min(x1, 760)
            if x1 - x0 > 10:
                wall.append(box(x0, y - 36, x1 - x0, 36, "#9a5a3c", "#5c3424", 1.2, 2, round(.3 + .3 * r_, 2)))
    dates = {"base": "dark", "cam": [1, 500, 880], "els": wall + [
        ring(226, 1082, 40, 2.2, AMBER, 3, dur=.6),
        arrow([[226, 1040], [250, 820], [330, 625]], 2.6, AMBER, 3, "known", .8),
        box(340, 420, 320, 190, "#a8603e", "#f2dcb4", 2, 10, 3.2, fx="pop"),
        glow(500, 690, 220, 5.0, .75, "red"),
        {"k": "poly", "p": [[420, 690], [440, 640], [455, 690]], "fill": "#ec5a3c", "c": "none", "w": 0, "in": 5.2, "fx": "pop"},
        {"k": "poly", "p": [[480, 690], [500, 625], [520, 690]], "fill": "#ffb27a", "c": "none", "w": 0, "in": 5.4, "fx": "pop"},
        {"k": "poly", "p": [[545, 690], [560, 645], [580, 690]], "fill": "#ec5a3c", "c": "none", "w": 0, "in": 5.6, "fx": "pop"},
        label(220, 520, "kiln", 5.6, "#ffb09a", 32, "middle"),
        box(340, 770, 400, 70, "none", BONE, 3, 8, 7.0), box(740, 788, 16, 34, BONE, r=3, at=7.0),
        label(322, 818, "0", 7.4, BONE, 34, "end")] +
        [dot(370 + 22 * (k % 13), 450 + 26 * (k // 13) + (7 if k % 2 else 0), 4, "#f2dcb4", round(3.6 + .02 * k, 2), op=.8) for k in range(65)] +
        [box(348 + 39 * k, 778, 33, 54, AMBER, r=4, at=round(10.6 + .75 * k, 2), fx="fill", dur=.6) for k in range(6)] +
        [glow(370 + 44 * k, 500 + 20 * (k % 3), 30, round(11.0 + .7 * k, 2), .7) for k in range(6)] +
        [label(540, 930, "c. 1,500 years", 19.4, AMBER, 40, st="serif"),
         label(480, 1000, "Sasanian · 5th to 6th c. CE", 23.6, FAITH, 30),
         box(200, 1220, 560, 70, "#6f675c", "#2e2a25", 1.5, 4, 31.9, fx="rise"),
         label(185, 1150, "brick", 32.2, "#e8a07a", 30, "end"), label(185, 1262, "stone", 32.6, "#cbbca8", 30, "end"),
         box(805, 1060, 120, 230, "rgba(120,128,140,.35)", FAITH, 3, 6, 33.9, style="claimed"),
         label(865, 1030, "iron, copper", 34.1, FAITH, 28),
         label(782, 1190, "≠", 34.5, BONE, 52, st="serif")]}
    # 4 · the gap, measured on the timeline
    _, ax = F.timeline(-600, 900, [(-500, "500 BCE"), (1, "1 CE"), (500, "500 CE")], "The candidates, and the walls", y=980)
    gap = [arrow([[ax.x(-550), 990], [ax.x(510), 990]], 1.2, AMBER, 4, "known", 1.6, False), label((ax.x(-550) + ax.x(510)) / 2, 1040, "c. 1,000 years", 3.0, AMBER, 30),
           arrow([[ax.x(-330), 1110], [ax.x(510), 1110]], 5.4, BLUE, 4, "known", 1.4, False), label((ax.x(-330) + ax.x(510)) / 2, 1160, "c. 900 years", 6.8, BLUE, 30)]
    # 5 · who? the account in a gold frame (a pass, a barrier), the three readings of the name around it
    mount = lambda xs: {"k": "poly", "p": xs, "fill": "#5a4a3a", "c": "#c9ad85", "w": 1.5, "in": 1.0, "fx": "rise"}
    who = {"base": "dark", "cam": [1, 500, 880], "els": [
        _gold_frame(270, 380, 460, 420, .3),
        label(500, 340, "Dhū al-Qarnayn", .6, FAITH, 36, st="serif"),
        mount([[290, 780], [380, 520], [455, 780]]), mount([[545, 780], [620, 500], [710, 780]]),
        box(452, 600, 96, 180, "#5e6670", "#b8c0c8", 2, 3, 1.8, fx="fill", dur=1.0),
        glow(500, 600, 70, 2.6, .8, "red"), line([[452, 602], [548, 602]], 2.6, "#e8925a", 6, draw=False),
        label(500, 860, "the two-horned", 3.4, FAITH, 30, st="ital")] +
        sum([[line([[500, 880], [x, 990]], at - .3, FAITH, 2, "inferred", .6), box(x - 120, 990, 240, 100, "#2a2018", c, 2.5, 14, at, fx="pop"),
              label(x, 1052, t, at + .2, BONE, 32, st="serif"), label(x, 1135, s, at + .4, c, 28)]
             for x, t, s, c, at in ((180, "Alexander", "commentators", AMBER, 6.4), (500, "earlier king", "Ibn Kathir", GREEN, 8.9), (820, "Cyrus", "modern scholars", BLUE, 13.2))], []) +
        [glow(500, 590, 300, 15.6, .35), box(440, 1220, 120, 160, "none", LILAC, 2.5, 8, 17.0, style="claimed"),
         box(465, 1245, 70, 70, "none", LILAC, 2, 4, 17.3, style="claimed")]}
    # 7 · beneath: the Sasanian wall on top, repairs in it, older ground below, and the undug layer
    sasa = [box(380, 700 - 36 * (r_ + 1), 240, 36, "#9a5a3c", "#5c3424", 1.2, 2, round(.3 + .25 * r_, 2)) for r_ in range(5)]
    patches = [box(x, y, 60, 36, "#c08a5c", "#5c3424", 1.2, 2, at, fx="pop") for x, y, at in ((400, 628, 6.0), (520, 592, 6.6), (440, 556, 7.2), (540, 664, 7.8))]
    papers = [box(770, 1150 - 14 * k, 140, 10, "#e9dfcb", "#8a7a66", 1, 2, round(12.0 + .3 * k, 2), fx="pop") for k in range(9)]
    beneath = {"base": "section", "tod": "dusk", "ground": 700, "lx": 130,
               "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 170, "c": "#5f4c39", "t": ""}, {"d": 340, "c": "#4a3a2c", "t": ""}, {"d": 540, "c": "#3a2e24", "t": ""}],
               "cam": [1, 500, 900], "els": sasa + [label(500, 470, "Sasanian · 5th to 6th c. CE", 1.8, AMBER, 30),
                                                    arrow([[500, 720], [500, 1030]], 3.0, LILAC, 3, "claimed", 1.0, False)] + patches +
               [label(368, 610, "rebuilt", 8.2, "#e8a07a", 28, "end"),
                arrow([[150, 760], [150, 1180]], 10.0, BONE, 3, "known", 1.2, False), label(170, 790, "newer", 10.2, BONE, 28, "start"), label(170, 1170, "older", 10.8, BONE, 28, "start")] + papers +
               [box(400, 1060, 200, 130, "rgba(201,193,238,.08)", LILAC, 2.5, 6, 18.6, style="claimed")] + question(500, 1150, 19.6, 80) +
               [label(500, 1260, "never dug", 20.6, LILAC, 32),
                {"k": "poly", "p": [[690, 640], [740, 640], [715, 700]], "fill": "#c9c1b3", "c": "#6b665f", "w": 1.5, "in": 21.8, "fx": "pop"},
                line([[715, 640], [715, 585]], 21.8, "#8a5d33", 8, draw=False)]}
    # the film's own beats: the reversal moves to the new section; the last line returns to it, closer
    ep["shots"] += [beneath, {"base": "dark", "cam": [1.3, 540, 1020], "els": []}]
    ep["beats"][4]["visual"]["from"] = 7
    for e in ep["shots"][2]["els"]:                      # the Gorgan model turns slowly: its two labels stay apart when the camera returns
        if e.get("k") == "iso":
            e["spin"] = .25
    ep["beats"][5]["lines"][1] = ep["beats"][5]["lines"][1].replace("[d:tension]", "[d:tension][go:8|0]", 1)
    for sc in (dates, who):
        _scene(sc)
    _scene(beneath)
    return _remix_rt(ep, scenes={3: dates, 5: who, 7: beneath}, alias={6: 1, 8: 7}, cams={6: [1.05, 500, 870]}, adds={1: _rt(passes), 4: _rt(gap)})


# ---------------------------------------------------------------- 10.07 The Ark of the Covenant
def ark_covenant_m():
    """The Ark as one continuous take: an Egyptian shrine on poles beside it, the chest leaving the record (and the loot list without it),
    a gold frame around Aksum's living tradition, nineteen centuries counted out, Hancock's route, and Pompey in an empty room."""
    from illus import person, arrow, line, glow, label, dot, box, ring, question, strike, oval, AMBER, BLUE, LILAC, BONE, RED as RD, GREEN
    ep = copy.deepcopy(F.ark_covenant())
    # beat 1 · gilded shrines on poles, from Egypt: a shrine carried by four bearers
    shrine = [box(380, 420, 240, 150, "#e2b45c", "#7a5a2e", 2, 4, 4.8, fx="rise"), box(368, 404, 264, 20, "#f2d27a", "#7a5a2e", 1.5, 3, 4.9, fx="rise"),
              line([[250, 585], [750, 585]], 5.2, "#6b4a2e", 8, draw=False)] + \
             [person(x, 700, 110, round(5.6 + .2 * k, 2)) for k, x in enumerate((285, 395, 605, 715))] + [label(500, 350, "Egypt", 6.6, AMBER, 32)]
    # 4 · off the record: the year of the fall, a dashed silence, and the loot list without the Ark
    _, ax = F.timeline(-1150, 1500, [(-1000, "1000 BCE"), (-500, "500"), (1, "1 CE"), (500, "500"), (1000, "1000")], "The Ark, on and off the record", y=980)
    off = [ring(ax.x(-586), 820, 22, 2.6, RD, 3, dur=.6),
           {"k": "line", "p": [[ax.x(-586), 975], [ax.x(1320), 975]], "c": LILAC, "w": 3, "style": "claimed", "in": 4.4},
           label((ax.x(-586) + ax.x(1320)) / 2, 1015, "no record", 5.2, LILAC, 28),
           box(220, 1070, 34, 120, "#b07a4a", "#5c3e22", 1.5, 3, 9.6, fx="fill", dur=.6),
           {"k": "poly", "p": [[330, 1120], [400, 1120], [390, 1190], [340, 1190]], "fill": "#b07a4a", "c": "#5c3e22", "w": 1.5, "in": 10.6, "fx": "pop"},
           line([[470, 1075], [470, 1160]], 11.6, "#b07a4a", 6, draw=False),
           {"k": "poly", "p": [[450, 1158], [490, 1158], [485, 1192], [455, 1192]], "fill": "#b07a4a", "c": "none", "w": 0, "in": 11.6, "fx": "pop"},
           box(640, 1110, 150, 80, "none", FAITH, 3, 4, 14.8, style="claimed"), line([[610, 1130], [820, 1130]], 14.8, FAITH, 2, "claimed", draw=False),
           label(715, 1235, "not listed", 15.4, FAITH, 28)]
    # 2 · Aksum: the tradition, framed in gold (never rated)
    aksum = [_gold_frame(110, 400, 780, 820, 13.8)]
    # 3 · nineteen centuries, counted out twice: the Ark leaving the record to the written account, and Rome to today
    cent = [box(78, 720, 52, 34, "#e2b45c", "#7a5a2e", 1.5, 3, .6, fx="pop"), line([[66, 748], [142, 748]], .6, "#6b4a2e", 4, draw=False),
            label(70, 690, "c. 586 BCE", 1.0, AMBER, 28, "start")] + \
           [box(150 + 37 * k, 770, 30, 70, AMBER, r=4, at=round(1.6 + .36 * k, 2), fx="fill", dur=.4) for k in range(19)] + \
           [{"k": "poly", "p": [[862, 760], [900, 770], [900, 840], [862, 830]], "fill": "#e9dfcb", "c": "#8a7a66", "w": 1.5, "in": 8.6, "fx": "pop"},
            {"k": "poly", "p": [[900, 770], [938, 760], [938, 830], [900, 840]], "fill": "#d8ccb4", "c": "#8a7a66", "w": 1.5, "in": 8.6, "fx": "pop"},
            label(930, 900, "Kebra Nagast · c. 1320 CE", 8.8, BONE, 28, "end"),
            label(500, 620, "1,900 years", 9.2, AMBER, 64, st="serif")] + \
           [box(150 + 37 * k, 1060, 30, 70, BLUE, r=4, at=round(10.8 + .14 * k, 2), fx="fill", dur=.3) for k in range(19)] + \
           [label(70, 1190, "Roman Empire", 10.6, BLUE, 28, "start"), label(930, 1190, "today", 13.6, BLUE, 28, "end")]
    years = {"base": "dark", "cam": [1, 500, 880], "els": cent}
    # 1 · the route: each real place lights up; no source on any leg
    v = View(27.5, 46, 9, 33.5, (40, 330, 920, 900))
    P = lambda lo, la: [round(c, 1) for c in v.p(lo, la)]
    stops = [(35.23, 31.78), (32.89, 24.09), (37.5, 12.1), (38.72, 14.13)]
    route = [ring(*P(lo, la), 26, at, AMBER, 3, dur=.6) for (lo, la), at in zip(stops, (1.6, 4.0, 7.0, 9.6))]
    for k, ((a, b), (c, d)) in enumerate(zip(stops[:-1], stops[1:])):
        mx, my = P((a + c) / 2, (b + d) / 2)
        route += question(mx + (40, 110, 60)[k], my - (0, 0, 30)[k], round(14.6 + .5 * k, 2), 56)
    # 5 · 63 BCE: the Temple in plan, Pompey's walk to the holiest room, and the room empty
    temple = {"base": "plan", "bg": "#231c15", "north": False, "cam": [1, 500, 880], "els": [
        label(500, 370, "Jerusalem · 63 BCE", .6, AMBER, 32),
        box(150, 430, 700, 930, "none", "#c9ad85", 2.5, 6, .4, fx="draw", dur=1.2),
        box(330, 520, 340, 500, "rgba(201,173,133,.14)", "#e9dccb", 2.5, 4, 1.4, fx="pop"),
        box(400, 540, 200, 170, "rgba(232,200,120,.08)", FAITH, 3, 3, 2.2, fx="pop"),
        line([[400, 710], [480, 710]], 2.2, "#e9dccb", 3, draw=False), line([[520, 710], [600, 710]], 2.2, "#e9dccb", 3, draw=False),
        person(500, 1350, 110, 4.0), label(560, 1300, "Pompey", 4.4, BONE, 30, "start"),
        line([[500, 1230], [500, 1020], [500, 760]], 5.0, AMBER, 3, "inferred", 3.0),
        person(500, 790, 80, 8.0),
        box(455, 590, 90, 56, "none", FAITH, 2.5, 3, 9.4, style="claimed"),
        glow(500, 620, 110, 11.8, .45),
        label(620, 640, "empty", 12.2, FAITH, 30, "start")]}
    # 6 · the verdict at the chapel: one sliver of wood, one carbon clock
    test = [box(150, 1300, 130, 26, "#8a5d33", "#3e2a18", 1.5, 3, .8, fx="pop"), label(215, 1370, "one sliver", 1.4, BONE, 28),
            arrow([[300, 1312], [400, 1312]], 6.2, AMBER, 3, "known", .6, False), ring(470, 1312, 48, 6.6, AMBER, 3),
            line([[470, 1312], [470, 1280]], 7.0, AMBER, 3, draw=False), line([[470, 1312], [496, 1322]], 7.0, AMBER, 3, draw=False)]
    for sc in (years, temple):
        _scene(sc)
    return _remix_rt(ep, scenes={3: years, 5: temple}, alias={6: 2}, cams={6: [1.1, 500, 940]},
                     adds={4: _rt(off), 2: _rt(aksum), 1: _rt(route)}, beat_adds={1: (_rt(shrine), [1, 500, 860])}, line_adds={(5, 1): (_rt(test), None)})


# ---------------------------------------------------------------- 10.08 The star of Bethlehem
def _paths():
    """Jupiter and Saturn in 7 BCE, schematic: both drift east with a backward loop in the middle; Jupiter overtakes Saturn three times,
    passing about one degree from it (here 40 units above)."""
    xj = lambda t: 830 - 520 * t - 150 * math.sin(2 * math.pi * t)
    xs = lambda t: 700 - 260 * t - 75 * math.sin(2 * math.pi * t)
    yj = lambda t: 560 + 120 * t - 100 * math.sin(2 * math.pi * t)
    d = lambda t: xj(t) - xs(t)
    meets = []
    for a, b in ((.05, .4), (.4, .6), (.6, .95)):
        for _ in range(50):
            m = (a + b) / 2
            if d(a) * d(m) <= 0: b = m
            else: a = m
        meets.append((a + b) / 2)
    return xj, xs, yj, meets


def star_m():
    """The star as one continuous take: Jupiter and Saturn looping past each other three times, the wise men and a rising star,
    the road from Babylon, the almanac and the clock run backwards, seventy days of a broom star, the candidates against a turning sky."""
    from illus import person, arrow, line, glow, label, dot, box, ring, question, strike, oval, ellipse, AMBER, BLUE, LILAC, BONE, RED as RD, GREEN
    ep = copy.deepcopy(F.star())
    xj, xs, yj, meets = _paths()
    J, S = "#ffe2a8", "#cfc6b4"
    segs = [(0, meets[0], 4.4, 2.0), (meets[0], meets[1], 7.6, 1.4), (meets[1], meets[2], 9.3, 1.4), (meets[2], 1, 11.0, 1.2)]
    trace = []
    for a, b, at, du in segs:
        ts = [a + (b - a) * k / 16 for k in range(17)]
        trace += [line([[round(xj(t), 1), round(yj(t), 1)] for t in ts], at, J, 3, dur=du, curve=True, op=.85),
                  line([[round(xs(t), 1), round(yj(t) + 40, 1)] for t in ts], at, S, 2.5, dur=du, curve=True, op=.7)]
    sky = [glow(xj(0), yj(0), 60, 1.2, .8), dot(xj(0), yj(0), 8, J, 1.2), label(xj(0) + 20, yj(0) - 20, "Jupiter", 1.6, J, 28, "start"),
           glow(xs(0), yj(0) + 40, 44, 2.0, .6), dot(xs(0), yj(0) + 40, 6, S, 2.0), label(xs(0) + 20, yj(0) + 90, "Saturn", 2.4, S, 28, "start")] + trace
    for k, (t, mo, at) in enumerate(zip(meets, ("May", "Oct", "Dec"), (7.2, 8.9, 10.6))):
        sky += [ring(xj(t), yj(t) + 20, 46, at, AMBER, 3, dur=.5), label(xj(t) - 60, yj(t) + 30, mo, at + .2, AMBER, 30, "end")]
    t3 = meets[2]
    sky += [glow(xj(1), yj(1), 70, 12.2, .9), dot(xj(1), yj(1), 9, J, 12.2), glow(xs(1), yj(1) + 40, 50, 12.2, .7), dot(xs(1), yj(1) + 40, 7, S, 12.2),
            {"k": "dim", "x1": 655, "y1": yj(t3), "x2": 655, "y2": yj(t3) + 40, "c": BONE, "in": 13.6, "upright": True},
            label(674, yj(t3) + 30, "1°", 13.8, BONE, 30, "start"),
            box(730, yj(t3) - 60, 40, 220, "rgba(232,201,168,.55)", "#e8c9a8", 1.5, 20, 15.0, fx="rise")]
    s0 = {"base": "sky", "tod": "night", "ground": 1200, "sun": False, "cam": [1, 500, 860], "els": sky}
    maybe = [glow(830, 430, 50, 3.2, .6), {"k": "line", "p": [[830, 430], [900, 360]], "c": BONE, "w": 2, "op": .5, "keepop": True, "in": 3.4},
             {"k": "line", "p": [[830, 430], [910, 380]], "c": BONE, "w": 1.5, "op": .4, "keepop": True, "in": 3.4}]
    # 5 · one Gospel: wise men from the east, a star at its rising
    rising = {"base": "sky", "tod": "night", "ground": 1150, "sun": False, "cam": [1, 500, 880], "els":
              [label(500, 400, "Matthew 2", .5, AMBER, 32)] +
              [person(x, 1150, h, round(1.6 + .2 * k, 2)) for k, (x, h) in enumerate(((180, 96), (225, 90), (268, 98), (310, 88)))] +
              [glow(760, 1040, 150, 4.6, .8), dot(760, 1040, 9, "#fff3d0", 4.6, "rise"),
               line([[760, 1000], [760, 1080]], 5.0, "#fff3d0", 2, draw=False, op=.7), line([[720, 1040], [800, 1040]], 5.0, "#fff3d0", 2, draw=False, op=.7),
               arrow([[760, 1130], [760, 1075]], 5.4, AMBER, 2, "inferred", .6, False), label(760, 1210, "east", 5.8, AMBER, 30)]}
    # 1 · the road: travellers along it
    v = View(33, 46, 29.5, 34.5, (40, 330, 920, 900))
    road = [v.p(44.42, 32.54), v.p(40.5, 34.2), v.p(36.3, 33.5), v.p(35.23, 31.78)]
    seglen = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(road, road[1:])]
    tot = sum(seglen)
    walk = [glow(*v.p(44.42, 32.54), 90, 3.0, .7)]
    for k in range(1, 10):
        s = tot * k / 10
        for (a, b), L in zip(zip(road, road[1:]), seglen):
            if s <= L:
                walk.append(dot(round(a[0] + (b[0] - a[0]) * s / L, 1), round(a[1] + (b[1] - a[1]) * s / L, 1), 6, AMBER, round(12.6 + .45 * k, 2)))
                break
            s -= L
    # 2 · the almanac: one row lights, and the clock that can run backwards
    almanac = [{"k": "hl", "x": 230, "y": 690, "w": 540, "h": 74, "in": 9.2}, glow(860, 727, 40, 9.8, .8), dot(850, 720, 7, J, 9.8), dot(872, 736, 5, S, 10.0),
               ring(500, 320, 46, 16.4, BONE, 3), line([[500, 320], [500, 290]], 16.8, BONE, 3, draw=False), line([[500, 320], [522, 330]], 16.8, BONE, 3, draw=False),
               {"k": "arrow", "p": ellipse(500, 320, 74, 74, 24, -20, -200), "c": AMBER, "w": 3, "fx": "draw", "dur": 1.2, "in": 19.0, "curve": True},
               line([[600, 330], [612, 344], [640, 306]], 23.4, GREEN, 5, dur=.5)]
    # 3 · a broom star, and seventy days
    comet = {"base": "dark", "stars": 140, "cam": [1, 500, 880], "els": [glow(300, 560, 120, 3.4, .9), dot(300, 560, 10, "#f5ecdc", 3.4)] +
             [line([[300, 560], [300 + 520 * math.cos(math.radians(a)), 560 - 520 * math.sin(math.radians(a)) * .45]], round(5.4 + .1 * k, 2), "#f5ecdc", 2, dur=.9, op=.55)
              for k, a in enumerate((8, 13, 18, 23, 28))] +
             [label(560, 700, "a broom star", 6.6, BONE, 30, st="ital")] +
             [box(230 + 55 * (k % 10), 820 + 52 * (k // 10), 44, 42, "#cfe6ff", r=5, at=round(8.4 + .04 * k, 2), op=.75) for k in range(70)] +
             [label(500, 1250, "70 days", 11.2, BLUE, 40, st="serif")]}
    # 4 · the candidates, their champions, and a sky that turns: nothing in it stops over a house
    arc = ellipse(500, 1250, 380, 330, 30, 180, 360)
    cand = {"base": "dark", "stars": 90, "cam": [1, 500, 880], "els": [
        glow(200, 500, 60, 1.2, .7), dot(188, 498, 11, J, 1.2), dot(214, 514, 8, S, 1.4), label(200, 610, "conjunction", 1.8, AMBER, 28),
        dot(552, 500, 10, J, 4.0), {"k": "circle", "x": 500, "y": 500, "r": 50, "fill": "#cfc6b4", "c": "#e8e0d0", "w": 2, "in": 4.4, "fx": "pop"},
        label(500, 610, "occultation", 4.8, BLUE, 28),
        glow(780, 520, 60, 7.6, .8), dot(780, 520, 8, "#f5ecdc", 7.6), line([[780, 520], [890, 450]], 7.8, "#f5ecdc", 2, dur=.6, op=.6),
        line([[780, 520], [895, 470]], 7.9, "#f5ecdc", 1.5, dur=.6, op=.5), label(800, 610, "comet", 8.2, BONE, 28)] +
        [person(x, 780, 80, at) for x, at in ((200, 10.0), (500, 10.4), (800, 10.8))] +
        [line([[80, 1250], [920, 1250]], 11.8, "#8a6a48", 3, dur=.8),
         {"k": "line", "p": arc, "c": BLUE, "w": 2.5, "style": "inferred", "curve": True, "in": 12.4, "op": .8, "keepop": True},
         label(120, 1300, "rises", 12.8, BLUE, 28), label(880, 1300, "sets", 15.6, BLUE, 28)] +
        [dot(arc[k][0], arc[k][1], 8, "#fff3d0", round(13.0 + .3 * j, 2)) for j, k in enumerate(range(3, 28, 3))] +
        [person(x, 1250, 64, round(17.2 + .15 * j, 2)) for j, x in enumerate((230, 268, 306))] +
        [{"k": "house", "x": 450, "y": 1250, "w": 100, "h": 60, "in": 19.6, "fx": "pop"},
         glow(500, 1130, 90, 23.0, .7), dot(500, 1130, 7, FAITH, 23.0)]}
    # beat 4 · the right few years, drawn on the ground of the opening sky
    X = lambda y: 160 + (y + 8) * 136
    years = [line([[X(-8), 1300], [X(-3), 1300]], .4, BONE, 3, dur=.8)] + \
            [label(X(y), 1350, t, .8, "#cbbca8", 28) for y, t in ((-7, "7 BCE"), (-6, "6"), (-5, "5"), (-4, "4"))] + \
            [dot(X(-6.6), 1300, 10, J, 2.2), dot(X(-5.7), 1300, 10, BLUE, 2.8), dot(X(-4.8), 1300, 10, BONE, 3.4),
             {"k": "line", "p": [[X(-4), 1270], [X(-4), 1330]], "c": RD, "w": 4, "in": 7.6}, label(X(-4) + 14, 1250, "Herod dies", 7.8, RD, 28, "start"),
             box(X(-7.5), 1262, X(-4) - X(-7.5), 14, FAITH, r=7, at=9.0, op=.45),
             label(500, 1420, "Kepler · 1604", 12.2, BONE, 30, st="serif")]
    for sc in (s0, rising, comet, cand):
        _scene(sc)
    return _remix_rt(ep, scenes={0: s0, 3: comet, 4: cand, 5: rising}, alias={6: 0}, cams={6: [1.15, 500, 860]},
                     adds={1: _rt(walk), 2: _rt(almanac)}, beat_adds={4: (_rt(years), [1.05, 500, 960])}, line_adds={(0, 1): (_rt(maybe), None)})


# ---------------------------------------------------------------- 10.09 The splitting of the Moon
def moon_split_m():
    """The Moon as one continuous take: the photo of a trough, the account framed in gold (the sign is never drawn or weighed), the trough
    as a graben, craters that sit on top of it and count its age, its shape against a join all the way round, and the photo struck out
    below a frame left untouched. Only the claim that the trough is a scar is weighed."""
    from illus import person, arrow, line, glow, label, dot, box, ring, question, strike, oval, ellipse, AMBER, BLUE, LILAC, BONE, RED as RD, GREEN
    ep = copy.deepcopy(F.moon_split())
    # 0 · the photo: viewfinder corners, shared online
    corner = lambda x, y, sx, sy: line([[x, y + 60 * sy], [x, y], [x + 60 * sx, y]], 8.0, BONE, 3, dur=.5)
    photo = [corner(170, 490, 1, 1), corner(830, 490, -1, 1), corner(170, 1150, 1, -1), corner(830, 1150, -1, -1),
             label(500, 1225, "shared online", 8.6, BONE, 30)]
    # 3 · the account, framed in gold: a night over the hills, the Moon, people looking up
    account = {"base": "dark", "stars": 120, "cam": [1, 500, 860], "els": [
        _gold_frame(140, 380, 720, 720, .3),
        glow(500, 620, 200, 2.6, .5), {"k": "circle", "x": 500, "y": 620, "r": 92, "fill": "#e8e0d0", "c": "none", "w": 0, "in": 2.6},
        {"k": "poly", "p": [[142, 1000], [260, 940], [380, 985], [500, 930], [640, 990], [760, 945], [858, 985], [858, 1098], [142, 1098]], "fill": "#2a2229", "c": "#4a3d44", "w": 1.5, "in": 1.0, "fx": "rise"},
        label(500, 1150, "Quran 54:1", 3.2, FAITH, 30)] +
        [person(x, y, 58, round(7.0 + .25 * k, 2)) for k, (x, y) in enumerate(((330, 985), (370, 982), (420, 968), (600, 978), (650, 990)))]}
    # 1 · the graben: the surface pulled apart; wet clay does the same
    pull = [arrow([[310, 590], [150, 590]], 9.4, AMBER, 4, "known", .7, False), arrow([[690, 590], [850, 590]], 9.4, AMBER, 4, "known", .7, False),
            box(250, 1310, 190, 60, "#b0805a", "#6b4a2e", 1.5, 4, 12.6, fx="pop"), box(560, 1310, 190, 60, "#b0805a", "#6b4a2e", 1.5, 4, 12.6, fx="pop"),
            box(444, 1332, 112, 60, "#9a6c48", "#6b4a2e", 1.5, 4, 13.6, fx="rise"),
            arrow([[245, 1340], [170, 1340]], 14.2, AMBER, 3, "known", .5, False), arrow([[755, 1340], [830, 1340]], 14.2, AMBER, 3, "known", .5, False)]
    # 2 · craters on top of the trough: younger than it; more craters, older ground
    surf = [box(110, 380, 780, 620, "#7d766a", "#a9a08e", 2, 12, .1),
            {"k": "poly", "p": [[110, 540], [890, 800], [890, 870], [110, 610]], "fill": "#4a443a", "c": "none", "w": 0, "in": .2},
            line([[110, 540], [890, 800]], .2, "#cfc6b4", 2, draw=False), line([[110, 610], [890, 870]], .2, "#cfc6b4", 2, draw=False)]
    cr = lambda x, y, r, at: [{"k": "circle", "x": x, "y": y, "r": r, "fill": "#5f594e", "c": "#cfc6b4", "w": 2, "in": at, "fx": "pop"}]
    craters = sum([cr(x, y, r, at) for x, y, r, at in ((300, 600, 34, .6), (560, 700, 24, 1.0), (700, 500, 40, 1.4), (420, 860, 28, 1.8), (790, 910, 22, 2.2), (230, 450, 24, 2.6))], [])
    news = [box(140, 1080, 300, 210, "#e9dfcb", "#8a7a66", 1.5, 4, 9.4, fx="pop")] + \
           [line([[165, 1110 + 22 * k], [415 - (60 if k % 3 == 2 else 0), 1110 + 22 * k]], 9.6, "#6b5f50", 3, draw=False) for k in range(8)] + \
           [ring(330, 1200, 56, 11.4, "#7a4a22", 7, dur=.8)]
    young = [box(560, 1080, 140, 140, "#7d766a", "#a9a08e", 1.5, 6, 16.0)] + sum([cr(x, y, 9, 16.4) for x, y in ((600, 1120), (660, 1180))], []) + [label(630, 1265, "young", 16.4, BONE, 28)]
    oldp = [box(730, 1080, 140, 140, "#7d766a", "#a9a08e", 1.5, 6, 18.0)] + \
           sum([cr(745 + 25 * (k % 5) + (8 if (k // 5) % 2 else 0), 1100 + 32 * (k // 5), 8, round(18.2 + .08 * k, 2)) for k in range(14)], []) + [label(800, 1265, "old", 18.6, BONE, 28)]
    count = sum([cr(x, y, 10, round(23.8 + .12 * k, 2)) for k, (x, y) in enumerate(((180, 575), (260, 600), (380, 640), (470, 680), (620, 740), (680, 770), (760, 790), (840, 825)))], [])
    crater = {"base": "dark", "cam": [1, 500, 900], "els": surf + craters + [ring(300, 600, 48, 5.0, AMBER, 4, dur=.6)] + news + young + oldp + count +
              [label(500, 1390, "tens of millions of years", 25.6, AMBER, 36, st="serif")]}
    # beat 3 · the shape: a join would run all the way round; the trough is a short crack in one region
    shape = [line([[380, 700], [470, 760], [560, 790], [650, 850]], 3.4, AMBER, 8, dur=1.0),
             {"k": "line", "p": ellipse(500, 820, 300, 110, 48), "c": LILAC, "w": 4, "curve": True, "in": 7.6, "fx": "draw", "dur": 3.0},
             label(500, 470, "all the way round · c. 11,000 km", 12.0, LILAC, 30),
             label(500, 1290, "less than a thirtieth", 19.5, AMBER, 30)]
    # beat 4 · back at the account: the photo below the frame, struck; the frame untouched
    strike_photo = [glow(500, 620, 170, 1.0, .45),
                    box(340, 1200, 320, 210, "#1a1714", BONE, 2.5, 10, 6.8, fx="pop"),
                    {"k": "circle", "x": 500, "y": 1305, "r": 72, "fill": "#cfc6b4", "c": "none", "w": 0, "in": 7.0},
                    line([[455, 1275], [490, 1300], [530, 1310], [560, 1335]], 7.4, "#4a443a", 4, dur=.5),
                    label(320, 1312, "online", 7.8, BONE, 30, "end"),
                    strike(345, 1205, 655, 1405, 11.4, RD, 7), strike(655, 1205, 345, 1405, 11.7, RD, 7),
                    _gold_frame(140, 380, 720, 720, 12.8, 9, 1.6, .55)]
    # 4 · Mina, where the reports place the witnesses
    vm = View(39.4, 40.4, 21.1, 21.8, (40, 330, 920, 900))
    mx, my = vm.p(39.893, 21.413)
    mina = [glow(mx, my, 120, 1.0, .5), ring(mx, my, 40, 1.2, FAITH, 3)]
    # verdict · the 'scar' ringed out, on the Moon
    out = [ring(515, 775, 175, 4.0, RD, 4, dur=.8)]
    ep["shots"].append({"base": "dark", "cam": [1.05, 500, 760], "els": []})
    ep["beats"][3]["visual"]["from"] = 0
    ep["beats"][5]["lines"][1] = ep["beats"][5]["lines"][1].replace("[act:the last word", "[go:6|0][act:the last word", 1)
    for sc in (account, crater):
        _scene(sc)
    return _remix_rt(ep, scenes={3: account, 2: crater}, alias={5: 0, 6: 3},
                     adds={0: _rt(photo), 1: _rt(pull), 4: _rt(mina)},
                     beat_adds={3: (_rt(shape), [1, 500, 860]), 4: (_rt(strike_photo), [.95, 500, 900]), 5: (_rt(out), [1.15, 500, 860])})


def EPISODES():
    return [dhul_qarnayn_m(), ark_covenant_m(), star_m(), moon_split_m()]
