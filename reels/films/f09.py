"""File 09 · Scripture and Stone I. Floods and first cities: where sacred texts meet the ground.
Only physical and historical claims are weighed. What faith holds is never rated, and nothing here is set against scripture."""
import math
from films import like, View, Axis
from scenes import timeline as _timeline, event, stat, quote, papyrus, silhouette, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso, lab, aim

SERIES = "Scripture and Stone"


def timeline(*a, **k):
    k["y"] = 820                                       # the axis sits where event() expects it, clear of the caption band and the kicker
    return _timeline(*a, x0=200, x1=810, **k)


def B(role, frm, lines, cut=True):
    return {"role": role, "visual": {"from": frm, "cut": cut} if cut else {"from": frm}, "lines": lines}


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def L_(x, y, t, c=None, z=0, **k):
    return dict(lab(x, y, t, c, z=z), st="lab", **k)


def tablet(text_rows=9, x=190, y=420, w=620, h=760):
    """A clay tablet: a rounded stone slab with cuneiform strokes."""
    return {"base": "paper", "kind": "stone", "x": x, "y": y, "w": w, "h": h, "holes": [], "cam": [1, 500, 860],
            "els": [{"k": "glyphs", "x": x + 50, "y": y + 60, "w": w - 100, "h": h - 140, "rows": text_rows, "cols": 8, "kind": "cuneiform", "in": .2}]}


# ---------------------------------------------------------------- 09.01 The Flood
def flood():
    v = View(-170, 175, -55, 75, (20, 300, 960, 900))
    pins = [("Mesopotamia", 44.5, 32), ("Genesis", 35.2, 31.8), ("Greece", 22, 38.5), ("India", 78, 22), ("China", 110, 34), ("Australia", 134, -25),
            ("Andes", -72, -13), ("Great Lakes", -85, 45), ("Pacific", 178, -18)]
    s0 = mapshot(v, extra=[{"k": "glow", "x": v.p(lo, la)[0], "y": v.p(lo, la)[1], "r": 34, "kind": "lamp", "op": .8, "in": .2 + i * .18} for i, (n, lo, la) in enumerate(pins)] +
                 [{"k": "circle", "x": v.p(lo, la)[0], "y": v.p(lo, la)[1], "r": 5, "fill": "#ffe2a8", "c": "none", "w": 0, "in": .2 + i * .18} for i, (n, lo, la) in enumerate(pins)] +
                 [{"k": "cap", "x": 500, "y": 380, "t": "a flood, remembered on every continent", "in": 1.6}], cam=[1.05, 500, 860])
    s1 = tablet()
    s1["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "Atrahasis · copied c. 1646–1626 BCE", "in": .6},
                  {"k": "label", "x": 500, "y": 1260, "t": "a warned hero, a boat, released birds, a sacrifice", "st": "small", "in": 1.2}]
    # the shelf: a coastal block with two sea levels
    shelf = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 60, "prof": [[-70, 0], [70, 0], [70, 30], [30, 26], [-10, 12], [-40, 3], [-70, 1]], "c": "#7a6248", "edge": "rgba(255,236,206,.45)"},
             {"t": "flat", "pts": [[-70, -30], [-10, -30], [-10, 30], [-70, 30]], "y": 12.1, "c": "#3f86b0", "op": .75, "ground": False, "over": 2},
             {"t": "flat", "pts": [[-70, -30], [-42, -30], [-42, 30], [-70, 30]], "y": 3.1, "c": "#2b5d7d", "op": .8, "ground": False, "over": 1},
             L_(-40, 4, "Ice Age sea · 120 m lower", "#cfe6ff", z=34, dy=44), L_(-24, 13, "today's sea", "#cfe6ff", z=34, dy=-18), L_(40, 30, "the drowned plain", GOLD, z=34, dy=-18)]
    s2 = iso(shelf, cam=[1, 500, 900], s=4.3, x=520, y=900, az=-26, spin=1.6, el=.42, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 420, "t": "the shelf · vertical scale exaggerated", "in": .2},
                  {"k": "label", "x": 500, "y": 1340, "t": "a continent's worth of coast, lost within lifetimes", "in": 1.0}]
    s3 = stat("14–25", "metres", "of sea-level rise in a few centuries during Meltwater Pulse 1A, about 14,600 years ago", "Deschamps et al. 2012 · Liu et al. 2016")
    s4 = quote("Long memory is the most economical explanation for the whole set. Twenty-one drowned coasts, remembered for over seven thousand years.", "Nunn & Reid 2016 · Australia's stories", y=700, size=40)
    tl, ax = timeline(-16000, 0, [(-16000, "16,000"), (-12000, "12,000"), (-8000, "8,000"), (-4000, "4,000"), (0, "today")], "Floods, and the first flood texts · years ago", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-15000), "x1": ax.x(-7000), "y": 720, "h": 18, "c": SCAN, "t": "the seas rise 120 m", "in": .3},
                  {"k": "band", "x0": ax.x(-15000), "x1": ax.x(-13000), "y": 640, "h": 18, "c": "#cfe6ff", "t": "Missoula floods, 40 or more", "in": .6},
                  {"k": "band", "x0": ax.x(-14650), "x1": ax.x(-14300), "y": 560, "h": 18, "c": GOLD, "t": "Meltwater Pulse 1A", "in": .9},
                  {"k": "line", "p": [[ax.x(-3650), 820], [ax.x(-3650), 500]], "c": AMBER, "w": 2, "in": 1.2},
                  {"k": "label", "x": ax.x(-3650), "y": 480, "t": "first flood texts · c. 1650 BCE", "c": AMBER, "st": "small", "in": 1.4}]
    s5 = tl
    s6 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE FLOOD][sfx:boom][act:opening wide, hushed wonder]Almost ^every people on Earth remembers a ^*flood*.",
                      "[d:tension][cam:1.12|0|0][act:posing it, slowly]Is that ^one memory... [act:letting it hang, softer][tune:fall]or ^many?"], cut=False),
        B("world", 1, ["[d:calm][k:MESOPOTAMIA][act:plain, scholarly and warm]The oldest ^written versions are ^Mesopotamian. [act:laying out the story's bones]Clay tablets from about {1650|sixteen fifty} BCE: a warned ^hero, a ^boat, released ^birds, a ^sacrifice.",
                       "[d:build][act:respectful, measured]The ^same bones as ^Genesis. [act:with care, even-handed]And the ^Quran remembers ^Nuh and his ark too."]),
        B("collision", 2, ["[d:build][k:THE ICE AGE ENDS][act:shifting gear, brisk]Now the ^ground. [act:plain fact, a sense of scale]As the last Ice Age ended, the seas rose a hundred and ^twenty metres.",
                           "[d:build][go:3|0][sfx:shimmer][act:building, a little faster]In ^one pulse, fourteen to twenty-five metres in a few ^*centuries*. [act:quieter, letting it sink in]Whole plains, gone within ^lifetimes."]),
        B("cost", 4, ["[d:build][k:MEMORY][act:genuinely wondering][tune:rise]Can a story last ^that long? [act:the answer, careful]In Australia, ^twenty-one coastal stories match ^drowned land... [count:7,000|years][act:the wonder of it, slower]for over seven ^*thousand* years."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:weighing it up, generous]So the archives hold ^real floods, ^many of them, ^enormous. [sfx:hit][act:the turn, clear and careful]What they don't hold is ^one flood over every land at ^once, in human times.",
                          "[d:aside][act:warm, gently curious][tune:fall]The child's question stands: which flood is ^*yours* remembering?"]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Real floods behind ^some stories? [act:the verdict, level-headed][tune:fall]^*Plausible*. [act:the second weighing, even][tune:rise]^One shared origin? [act:calm, precise][tune:fall]^Unproved.",
                     "[d:tension][p:0.93][act:respectful, measured, sincere][tune:fall]What scripture ^tells is not what we ^rate. [act:gentle, a thoughtful pause]The ^water... [act:quiet, sure][tune:fall]we ^can measure."]),
    ]
    return EP("flood", "09.01", "The Flood: One Story, Many Waters", "flood", "contested", "Do the world's flood stories remember real floods?", "Is that one memory... or *many*?", beats, shots,
              "Atrahasis tablets, British Museum · Deschamps et al. 2012, Nature · Nunn & Reid 2016, Australian Geographer · Waitt 1980",
              "Flood stories on every continent, the oldest tablets, the 120-metre rise at the end of the Ice Age, and what oral memory can carry. What is rated, and what is left to faith.",
              ["#Flood", "#IceAge", "#Mesopotamia", "#History", "#Science"])


def _mur():
    from mural import remix
    import illus as I
    return remix, I


def _at(w, wo, wn, wps=2.5):
    """Build time (in the original film's clock) for something named at word w of the rewritten step (remix stretches it back)."""
    r = min(2.5, max(1.0, (wn + 3) / (wo + 3)))
    return round(w / wps / r, 2)


def _quiet_iso(shot, drop=(), spin=None):
    """A copy of an iso shot without some of its world labels (the narrator says them), optionally turning less."""
    import copy
    sh = copy.deepcopy(shot)
    for e in sh["els"]:
        if e.get("k") == "iso":
            e["items"] = [i for i in e["items"] if not (i.get("t") == "label" and i.get("text") in drop)]
            if spin is not None:
                e["spin"] = spin
    return sh


def _book(x, y, at, c="#cdb48a"):
    """A closed book, plain (no writing on it)."""
    return [{"k": "rect", "x": x - 55, "y": y - 70, "w": 110, "h": 140, "r": 6, "fill": c, "c": "#f5ecdc", "sw": 2, "in": at, "fx": "pop"},
            {"k": "rect", "x": x - 55, "y": y - 70, "w": 16, "h": 140, "r": 4, "fill": "rgba(0,0,0,.25)", "c": "none", "sw": 0, "in": at, "fx": "pop"}]


def flood_m():
    """The Flood as one continuous take (see mural.py): a tablet's story bones, a sea-level pulse against a building, 21 drowned coasts and 280 generations."""
    remix, I = _mur()
    ep = flood()
    T = lambda w: _at(w, 36, 81)
    CLAY = "#b9a47c"
    # 1 · the oldest written version: two rivers, a tablet, four story bones; Genesis's same bones; the Quran's own account, set apart
    rivers = [I.line([[90, 300 + 40 * j], [300, 330 + 40 * j], [560, 300 + 40 * j], [910, 340 + 40 * j]], T(6) + .3 * j, I.SEA, 5, curve=True) for j in range(2)]
    tab = [I.box(330, 440, 340, 300, CLAY, "#8a6a48", 2, 26, T(16), fx="pop"),
           {"k": "glyphs", "x": 360, "y": 470, "w": 280, "h": 240, "rows": 7, "cols": 6, "kind": "cuneiform", "c": "#3b2a1c", "in": T(17)},
           I.label(500, 790, "Atrahasis · c. 1650 BCE", T(24), I.AMBER, 30)]
    X = (170, 390, 610, 830); Y = 990
    warn = [I.dot(X[0], Y, 10, I.BONE, T(28))] + [I.line([[X[0] + 22 * j, Y - 40 - 8 * j], [X[0] + 34 + 22 * j, Y], [X[0] + 22 * j, Y + 40 + 8 * j]], T(28) + .15 * j, I.AMBER, 4, curve=True, dur=.4) for j in range(3)]
    boat = [{"k": "boat", "x": X[1], "y": Y + 20, "w": 170, "in": T(32), "fx": "rise"}, I.line([[X[1] - 110, Y + 40], [X[1] + 110, Y + 40]], T(32), I.SEA, 3, curve=False, dur=.5)]
    birds = [I.line([[X[2] - 30 + 30 * j, Y + 20 - 40 * j], [X[2] - 15 + 30 * j, Y + 32 - 40 * j], [X[2] + 30 * j, Y + 20 - 40 * j]], T(37) + .25 * j, I.BONE, 4, dur=.3) for j in range(3)]
    altar = [I.box(X[3] - 45, Y, 90, 50, "#8d7a64", "#cbbca8", 2, 4, T(45), fx="pop"), I.glow(X[3], Y - 20, 70, T(45) + .2, .8, "lamp"),
             I.line([[X[3], Y - 10], [X[3] - 14, Y - 50], [X[3] + 10, Y - 90], [X[3] - 6, Y - 130]], T(46), "#cbbca8", 3, "inferred", .8, True)]
    labs = [I.label(x, 1100, t, T(w), I.BONE, 28) for x, t, w in zip(X, ("a warning", "a boat", "birds", "an offering"), (29, 33, 38, 46))]
    gen = _book(300, 1300, T(51)) + [I.label(300, 1405, "Genesis", T(52), I.BONE, 30)] + \
        [I.line([[300, 1225], [x, 1122]], T(54) + .12 * k, I.AMBER, 2, "inferred", .6) for k, x in enumerate(X)]
    qur = _book(720, 1300, T(61), "#b9c9b0") + [I.label(720, 1405, "the Quran", T(62), I.BONE, 30),
                                                {"k": "boat", "x": 720, "y": 1216, "w": 110, "in": T(64), "fx": "rise"}, I.glow(720, 1200, 80, T(64), .5, "lamp")]
    story = {"base": "dark", "cam": [1, 500, 860], "els": rivers + [I.label(500, 410, "Mesopotamia", T(3), "#9fd0ff", 30, st="ital")] + tab + warn + boat + birds + altar + labs + gen + qur}
    # 2 · the ground: a coast in section, the Ice Age sea 120 m down, then the rise that drowned the plain (3.5 px per metre)
    SH = lambda w: _at(w, 17, 43)
    k0, S0 = 3.5, 700
    land = [[60, 690], [250, 700], [330, 712], [480, 740], [640, 790], [760, 860], [810, 1100], [860, 1180], [940, 1200], [940, 1420], [60, 1420]]
    coast = [I.box(60, S0 + 120 * k0, 880, 1420 - S0 - 120 * k0, "#2b5d7d", r=0, at=SH(18), fx="fill", dur=.8, op=.9),
             I.box(60, S0, 880, 120 * k0, "#3f86a8", r=0, at=SH(30), fx="fill", dur=2.4, op=.6),
             {"k": "poly", "p": land, "fill": "#7a6248", "c": "#e8d3a8", "w": 2, "in": 0},
             I.line([[60, S0 + 120 * k0], [940, S0 + 120 * k0]], SH(19), "#9fd0ff", 3, "inferred", .8), I.label(930, S0 + 120 * k0 - 20, "Ice Age sea", SH(20), "#9fd0ff", 28, "end"),
             {"k": "poly", "p": [[60, 420], [200, 380], [360, 400], [420, 470], [300, 520], [60, 520]], "fill": "#eef3f6", "c": "#ffffff", "w": 1.5, "curve": True, "in": SH(12), "fx": "rise", "op": .9, "keepop": True},
             I.label(220, 570, "ice sheets", SH(13), "#eef3f6", 28),
             I.person(560, 768, 60, SH(22)), I.person(610, 784, 52, SH(22) + .2), I.label(600, 900, "the drowned plain", SH(40), I.AU, 30),
             I.arrow([[880, S0 + 120 * k0 - 50], [880, S0 + 6]], SH(33), I.AMBER, 4, "known", 1.2, False), I.label(870, 900, "120 m", SH(34), I.AMBER, 34, "end"),
             I.line([[60, S0], [940, S0]], SH(36), "#cfe6ff", 2, dur=.8), I.label(930, S0 - 18, "today's sea", SH(36), "#cfe6ff", 28, "end")]
    ground = {"base": "dark", "cam": [1, 500, 880], "els": coast}
    # 3 · one pulse of the rise, against a building of five to eight storeys (both drawn to scale)
    P = lambda w: _at(w, 16, 44)
    G0, k1 = 1320, 800 / 120                                  # the whole 120 m rise: 6.7 px per metre
    gauge = [I.box(110, G0 - 800, 90, 800, "none", "#cbbca8", 2, 4, 0, op=.9),
             I.box(112, G0 - 20 * k1, 86, 20 * k1, "#2b5d7d", r=2, at=P(1), fx="fill", dur=1.0, op=.85),
             I.box(112, G0 - 45 * k1, 86, 25 * k1, "#9fd0ff", r=2, at=P(9), fx="fill", dur=.6),
             I.box(112, G0 - 120 * k1, 86, 75 * k1, "#2b5d7d", r=2, at=P(40), fx="fill", dur=1.6, op=.55),
             I.label(155, G0 - 820, "120 m", P(1), "#cbbca8", 28), I.label(155, G0 + 50, "Ice Age sea", P(1), "#cbbca8", 28)]
    k2, B0 = 24, 1320                                          # zoom: 24 px per metre
    zoom = [I.line([[200, G0 - 45 * k1], [330, B0 - 25 * k2]], P(14), "#9fd0ff", 2, "inferred", .6),
            I.line([[200, G0 - 20 * k1], [330, B0]], P(14), "#9fd0ff", 2, "inferred", .6),
            I.line([[330, B0], [900, B0]], P(14), "#8a6a48", 3, draw=False),
            I.box(600, B0 - 14 * k2, 250, 14 * k2, "#3f86a8", r=2, at=P(17), fx="fill", dur=1.0, op=.85),
            I.box(600, B0 - 25 * k2, 250, 11 * k2, "#9fd0ff", r=2, at=P(22), fx="fill", dur=.8, op=.6),
            I.label(725, B0 - 14 * k2 + 40, "14 m", P(18), I.BONE, 30), I.label(725, B0 - 25 * k2 - 18, "25 m", P(23), "#9fd0ff", 30)]
    bld = [I.box(400, B0 - 3 * k2 * (j + 1), 150, 3 * k2 - 6, "#6f5a44", "#cbbca8", 2, 3, round(P(30) + .12 * j, 2), fx="pop") for j in range(8)] + \
          [I.box(420 + 40 * (j % 3), B0 - 3 * k2 * (j // 3 + 1) + 20, 22, 24, "#e8c894", r=2, at=round(P(31) + .05 * j, 2), op=.7) for j in range(24)] + \
          [I.person(570, B0, 1.7 * k2, P(33)), I.label(475, B0 + 50, "8 storeys", P(32), I.BONE, 28)]
    pulse = {"base": "dark", "cam": [1, 500, 880], "els": gauge + zoom + bld}
    # 4 · twenty-one coastal stories round Australia, and 280 generations passing them on
    from films import View
    from f01 import mapshot
    M = lambda w: _at(w, 19, 54)
    v = View(111, 156, -40, -9, (60, 290, 880, 700))
    coast = [(115.0, -33.6), (114.6, -28.6), (113.7, -24.6), (116.8, -20.7), (122.2, -18.1), (125.6, -14.6), (130.8, -12.5), (136.8, -12.3), (141.6, -12.7), (141.4, -16.6), (145.8, -17.0),
             (149.2, -21.2), (153.0, -25.6), (153.5, -28.6), (152.9, -31.6), (151.2, -33.9), (150.0, -37.0), (145.0, -38.3), (140.5, -38.0), (138.4, -35.0), (135.9, -34.7)]
    mp = mapshot(v)["els"]
    lamps = []
    for j, (lo, la) in enumerate(coast):
        x, y = v.p(lo, la)
        lamps += [I.glow(x, y, 34, round(M(26) + .12 * j, 2), .8, "lamp"), I.dot(x, y, 6, "#ffe2a8", round(M(26) + .12 * j, 2))]
    gens = [I.dot(150 + 25 * (j % 28), 1110 + 26 * (j // 28), 7, "#e8c894", round(M(46) + .006 * j, 3)) for j in range(280)]
    mem = {"base": "map", "cam": [1, 500, 860], "els": mp + lamps + [I.label(500, 1050, "280 generations", M(47), I.AMBER, 32)] + gens}
    return remix(ep, scenes={1: story, 2: ground, 3: pulse, 4: mem}, alias={6: 0}, cams={6: [1.15, 500, 880]})

# ---------------------------------------------------------------- 09.02 Yu the Great
def yu():
    v = View(96, 118, 30, 41, (40, 330, 920, 900))
    river = [(96.5, 35.2), (100.5, 36.0), (102.8, 35.85), (103.8, 36.1), (105.5, 37.5), (106.3, 39.2), (109.5, 40.5), (111.2, 39.6), (110.6, 36.0), (110.2, 34.6), (113.0, 34.9), (116.0, 35.8), (118.5, 37.7)]
    base = mapshot(v, extra=[{"k": "line", "p": [v.p(*q) for q in river], "c": "#5fa8c9", "w": 2.4, "op": .8, "curve": True, "id": "river"},
                             {"k": "label", "x": v.p(108, 41)[0], "y": v.p(108, 41)[1], "t": "Yellow River", "st": "ital", "c": "#9fd0ff"}])
    s0 = {"base": "dark", "floor": 1100, "cam": [1.15, 500, 860], "els": [{"k": "circle", "x": 500, "y": 900, "r": 210, "fill": "#8a6a4a", "c": "#c9ad85", "w": 3, "in": .1},
          {"k": "circle", "x": 500, "y": 900, "r": 150, "fill": "#d9c39a", "c": "none", "w": 0, "in": .2}] +
          [{"k": "line", "p": [[500 + 120 * math.cos(math.radians(a)), 900 + 120 * math.sin(math.radians(a))], [500 + 60 * math.cos(math.radians(a + 140)), 900 + 60 * math.sin(math.radians(a + 140))]],
            "c": "#e9dc9a", "w": 4, "curve": True, "in": .3 + i * .05} for i, a in enumerate(range(0, 360, 24))] +
          [{"k": "cap", "x": 500, "y": 520, "t": "Lajia · a bowl of noodles", "in": .3}, {"k": "num", "x": 500, "y": 1180, "t": "4,000", "u": "years old", "in": .9, "fx": "pop", "size": 80}]}
    s1 = like(base, add=[{"k": "pin", "x": v.p(102.8, 35.85)[0], "y": v.p(102.8, 35.85)[1], "t": "Jishi Gorge", "c": GOLD, "in": .3},
                         {"k": "pin", "x": v.p(102.75, 35.87)[0] - 30, "y": v.p(102.75, 35.87)[1] + 40, "t": "Lajia", "c": OCHRE, "a": "end", "lx": -18, "in": .7},
                         {"k": "pin", "x": v.p(112.7, 34.7)[0], "y": v.p(112.7, 34.7)[1], "t": "Erlitou · early Xia?", "in": 1.1},
                         {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}])
    # the gorge: a landslide dam and the lake behind it
    gorge = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 150, "prof": [[-26, 0], [-26, 20], [-13, 20], [-8, 6], [8, 6], [13, 20], [26, 20], [26, 0]], "c": "#7a6248", "edge": "rgba(255,236,206,.45)"},
             {"t": "box", "x": 0, "z": 0, "y": 6, "w": 18, "d": 10, "h": 10, "c": "#8c7152", "edge": "rgba(255,236,206,.5)", "id": "dam"},
             {"t": "flat", "pts": [[-11, 5], [11, 5], [11, 75], [-11, 75]], "y": 15.1, "c": "#3f86b0", "op": .78, "ground": False, "over": 2},
             L_(0, 17, "landslide dam", GOLD, z=0, dy=-34), L_(0, 15, "the lake behind it", "#cfe6ff", z=48, dy=-16), L_(0, 6, "downstream · Lajia", OCHRE, z=-62, dy=44)]
    s2 = iso(gorge, cam=[1, 500, 900], s=4.4, x=500, y=980, az=148, spin=1.4, el=.5, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "Jishi Gorge · a schematic", "in": .2}]
    s3 = stat("400,000", "m³ per second", "the peak flow estimated for the outburst when the dam gave way, one of the largest floods known in the Holocene", "Wu et al. 2016, Science")
    tl, ax = timeline(-2600, -1300, [(-2600, "2600 BCE"), (-2200, "2200"), (-1800, "1800"), (-1400, "1400")], "The dates in dispute", y=980)
    tl["els"] += event(ax, -1920, "the flood · Wu et al.", row=0, c=GOLD, i=.3) + event(ax, -2070, "Xia begins · tradition", row=1, c=AMBER, i=.6) + \
                 event(ax, -1750, "Erlitou · early Xia?", row=2, c=SCAN, i=.9, sub="far downstream of the flood")
    s4 = tl
    s5 = quote("A Zhou bronze vessel of about 900 BCE already credits Yu with channelling the waters, centuries before the classic accounts.", "the Sui Gong xu", y=700, size=40)
    s6 = like(s1, cam=[1.15, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:LAJIA · CHINA][sfx:boom][act:delighted, a little wonder]A bowl of ^noodles, four ^thousand years old. [act:quieter, a shadow falls]Dropped in a ^hurry.",
                      "[d:tension][cam:1.12|0|0][act:grave, gentle, slower]^Everyone in the house@noun died where they ^stood."], cut=False),
        B("world", 1, ["[d:calm][k:THE UPPER YELLOW RIVER][act:telling the legend, warm]Chinese tradition says a hero called ^Yu tamed a great flood, and founded the ^first dynasty.",
                       "[d:build][go:2|0][act:storytelling, building]Upstream, at Jishi Gorge, a ^landslide once ^dammed the river. [sfx:shimmer][act:slow, tension gathering][tune:level]The lake behind it ^rose. [act:the break, heavier]Then the dam gave ^way."]),
        B("collision", 3, ["[d:build][k:THE NUMBER][act:savouring the number, precise]The estimated peak: four hundred ^thousand cubic metres a second. [act:the scale of it, wonder]Among the ^largest floods of the last ten thousand years.",
                           "[d:build][go:4|0][act:intrigued, connecting the dots]Its date, about {1920|^nineteen twenty} BCE, sits close@adj to where tradition begins the ^Xia."]),
        B("cost", 4, ["[d:build][k:THE DISPUTE][act:the counterpoint, fair][tune:fall]But ^other teams date the lake ^thousands of years earlier. [act:even-handed, clear]And they read@present Lajia's deaths as an ^earthquake and a ^mudflow, not a flood."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:leaning in, a pleasant surprise]And Yu's story is ^old. [act:the evidence, clear]A ^bronze vessel from about nine hundred BCE ^already credits him with channelling the waters. [sfx:hit][act:the punch, firm][tune:fall]^Centuries before the classic accounts."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority]A ^real flood, with a real ^hypothesis behind it. [act:turning it over][tune:rise]Its ^link to Yu? [act:the verdict, honest][tune:fall]An ^*open* question.",
                     "[d:tension][p:0.93][act:light, a warm smile]The ^noodles, at least, are ^settled."]),
    ]
    return EP("yu-flood", "09.02", "Yu the Great and the Flood That Made a Dynasty", "yu-xia", "contested", "Did a real megaflood lie behind Yu's flood and the Xia?", "Dropped in a *hurry*.", beats, shots,
              "Wu et al. 2016, Science · Zhang et al. 2018 · Lu et al. 2005, Nature (the noodles) · Sui Gong xu, Poly Art Museum",
              "A landslide dam, a burst lake and a bowl of 4,000-year-old noodles: the case that a real flood lies behind Yu the Great, and the teams who dispute its date.",
              ["#China", "#Flood", "#Archaeology", "#Geology", "#History"])


def yu_m():
    """Yu's flood as one continuous take (see mural.py): the peak flow as 160 swimming pools a second, and a bronze vessel that already names him."""
    remix, I = _mur()
    ep = yu()
    P = lambda w: _at(w, 20, 49)
    pool = [I.box(400, 330, 200, 90, "#3f86a8", "#cfe6ff", 2, 4, P(14), fx="pop")] + \
           [I.line([[408, 352 + 22 * j], [592, 352 + 22 * j]], P(14) + .1, "#cfe6ff", 1.5, draw=False, op=.6) for j in range(3)] + [I.label(500, 470, "1 Olympic pool", P(15), I.BONE, 30)]
    grid = [I.box(84 + 52 * (j % 16), 560 + 30 * (j // 16), 46, 22, "#3f86a8", "#9fd0ff", 1, 2, round(P(26) + .01 * j, 3), fx="pop") for j in range(160)]
    flow = [I.label(500, 930, "160 pools, every second", P(30), "#9fd0ff", 34),
            I.arrow([[90, 1060], [380, 1010], [640, 1090], [910, 1040]], P(31), "#9fd0ff", 5, "known", 1.2, True),
            I.arrow([[90, 1150], [380, 1100], [640, 1180], [910, 1130]], P(32), "#5fa8c9", 4, "known", 1.2, True),
            I.arrow([[90, 1240], [380, 1190], [640, 1270], [910, 1220]], P(33), "#3f86a8", 3, "known", 1.2, True)]
    pools = {"base": "dark", "cam": [1, 500, 860], "els": pool + grid + flow}
    V = lambda w: _at(w, 25, 35)
    water = [I.line([[110, 340 + 30 * j], [240, 300 + 30 * j], [380, 380 + 30 * j], [520, 340 + 30 * j]], round(V(18) + .15 * j, 2), "#5fa8c9", 4, curve=True) for j in range(3)] + \
            [I.line([[520, 340 + 30 * j], [890, 340 + 30 * j]], round(V(21) + .15 * j, 2), "#9fd0ff", 4) for j in range(3)] + \
            [I.line([[520, 318], [890, 318]], V(20), "#cbbca8", 4), I.line([[520, 422], [890, 422]], V(20), "#cbbca8", 4), I.label(705, 480, "the waters, channelled", V(22), "#9fd0ff", 28)]
    BR = "#6f8f78"
    vessel = [I.glow(350, 860, 230, V(6), .35), {"k": "vase", "x": 350, "y": 1010, "w": 230, "h": 260, "tone": BR, "profile": [[0, .62], [.06, .68], [.14, .6], [.5, .72], [.85, .62], [1, .5]], "in": V(6), "fx": "rise"},
              I.line([[180, 820], [130, 860], [175, 920]], V(7), BR, 8, curve=True, dur=.4), I.line([[520, 820], [570, 860], [525, 920]], V(7), BR, 8, curve=True, dur=.4),
              I.label(350, 1075, "bronze · c. 900 BCE", V(8), I.BONE, 28)]
    rub = [I.box(640, 720, 240, 300, "#e9dcc4", "#fff6e6", 2, 4, V(13), fx="pop"),
           {"k": "glyphs", "x": 665, "y": 745, "w": 190, "h": 250, "rows": 6, "cols": 5, "kind": "hieratic", "c": "#2a2019", "in": V(14)},
           I.label(760, 1075, "its inscription", V(14), I.BONE, 28)]
    X0, X1 = 200, 800
    line_ = [I.line([[120, 1240], [880, 1240]], V(26), "#8a7a66", 3), I.dot(X0, 1240, 10, BR, V(26)), I.label(X0, 1300, "c. 900 BCE", V(26), "#cbbca8", 28),
             I.arrow([[X0 + 20, 1240], [X1 - 24, 1240]], V(27), I.AMBER, 4, "inferred", 1.2, False), I.label(500, 1205, "centuries", V(28), I.AMBER, 32),
             I.dot(X1, 1240, 10, I.AMBER, V(30)), I.label(X1, 1300, "classic accounts", V(30), "#cbbca8", 28)]
    bronze = {"base": "dark", "cam": [1, 500, 860], "els": water + vessel + rub + line_}
    return remix(ep, scenes={3: pools, 5: bronze}, alias={6: 1}, cams={6: [1.15, 500, 860]})

# ---------------------------------------------------------------- 09.03 Gilgamesh
def gilgamesh():
    s0 = tablet(text_rows=10)
    s0["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "the Sumerian King List · c. 1800 BCE", "in": .5},
                  {"k": "num", "x": 500, "y": 1230, "t": "126", "u": "years on the throne", "in": 1.0, "fx": "pop", "size": 84}]
    v = View(42, 48, 29.5, 34.5, (40, 330, 920, 900))
    euph = [(42.3, 34.6), (43.4, 33.9), (44.0, 33.2), (44.42, 32.54), (45.0, 32.1), (45.64, 31.32), (46.2, 31.0), (47.0, 30.7), (47.6, 30.4)]
    tigr = [(43.0, 34.9), (43.9, 34.0), (44.4, 33.4), (45.0, 32.7), (45.8, 32.0), (46.4, 31.5), (47.1, 31.0), (47.6, 30.4)]
    s1 = mapshot(v, pins=[("Uruk", 45.64, 31.32, {"c": GOLD}), ("Kish", 44.6, 32.54, {"c": AMBER}), ("Shuruppak", 45.5, 31.78, {"c": SCAN, "a": "end", "lx": -18}), ("Babylon", 44.42, 32.54, {"a": "end", "lx": -18})],
                 extra=[{"k": "line", "p": [v.p(*q) for q in euph], "c": "#5fa8c9", "w": 2.2, "op": .7, "curve": True}, {"k": "line", "p": [v.p(*q) for q in tigr], "c": "#5fa8c9", "w": 2.2, "op": .7, "curve": True},
                        {"k": "label", "x": v.p(43.1, 33.6)[0], "y": v.p(43.1, 33.6)[1], "t": "Euphrates", "st": "ital", "c": "#9fd0ff", "size": 22}, {"k": "label", "x": v.p(45.6, 33.0)[0], "y": v.p(45.6, 33.0)[1], "t": "Tigris", "st": "ital", "c": "#9fd0ff", "size": 22},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    # Uruk: a walled city as a diorama
    wall = []
    for i in range(24):
        a = i / 24 * 2 * math.pi; a2 = (i + 1) / 24 * 2 * math.pi
        wall.append({"t": "line", "p": [[60 * math.cos(a), 6, 44 * math.sin(a)], [60 * math.cos(a2), 6, 44 * math.sin(a2)]], "c": "#e9dccb", "w": 5, "op": .9})
    city = wall + [{"t": "box", "x": 0, "z": 0, "y": 0, "w": 14, "d": 14, "h": 8, "c": "#b88a64", "edge": "rgba(0,0,0,.25)"}, {"t": "box", "x": 0, "z": 0, "y": 8, "w": 9, "d": 9, "h": 6, "c": "#c49a68", "edge": "rgba(0,0,0,.25)"},
                   {"t": "box", "x": 0, "z": 0, "y": 14, "w": 5, "d": 5, "h": 5, "c": "#d9b67c", "edge": "rgba(0,0,0,.25)"}] + \
           [{"t": "box", "x": 30 * math.cos(a) + 8 * math.sin(3 * a), "z": 22 * math.sin(a), "y": 0, "w": 4, "d": 4, "h": 2.5, "c": "#a8845c", "edge": "rgba(0,0,0,.2)"} for a in [k * .5 for k in range(12)]] + \
           [L_(0, 22, "Uruk · walls of about 9 km", GOLD), L_(0, 2, "one of the first cities on Earth", "#cfe6ff", z=52, dy=36)]
    s2 = iso(city, cam=[1, 500, 900], s=5.0, x=500, y=980, az=-20, spin=1.6, el=.45, table={"r": 78, "rz": 62, "grid": 20, "strata": [{"h": 2, "c": "#a8845c"}, {"h": 6, "c": "#7d6045"}]})
    s3 = {"base": "dark", "floor": 1062, "cam": [1.2, 500, 860], "els": [{"k": "glow", "x": 500, "y": 820, "r": 300, "kind": "lamp", "op": .3},
          {"k": "vase", "x": 500, "y": 1060, "w": 220, "h": 300, "in": .2}, {"k": "glyphs", "x": 420, "y": 880, "w": 160, "h": 60, "rows": 2, "cols": 5, "kind": "cuneiform", "in": .8},
          {"k": "cap", "x": 500, "y": 540, "t": "a stone vessel · c. 2600 BCE", "in": .4},
          {"k": "label", "x": 500, "y": 1150, "t": "'Enmebaragesi, king of Kish' · the rival's father, named in stone", "st": "small", "c": GOLD, "in": 1.2}]}
    s4 = quote("Gilgamesh is already listed as a god in the god lists of Shuruppak, within a few generations of his supposed lifetime.", "Fara god lists · c. 2600 BCE", y=700, size=40)
    tl, ax = timeline(-3000, -1600, [(-3000, "3000 BCE"), (-2600, "2600"), (-2200, "2200"), (-1800, "1800")], "What is attested, and when", y=980)
    tl["els"] += event(ax, -2650, "reign proposed", row=0, c=GOLD, i=.3, sub="no inscription of his own") + event(ax, -2600, "Enmebaragesi in stone", row=1, c=AMBER, i=.6) + \
                 event(ax, -2600, "worshipped as a god", row=2, c=SCAN, i=.9) + event(ax, -1800, "the King List copy", row=0, c="#cfe6ff", i=1.2)
    s5 = tl
    s6 = like(s2, cam=[1.1, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE KING LIST][sfx:boom][act:deadpan, let the number land]A list of kings says Gilgamesh reigned for a ^hundred and twenty-six years.",
                      "[d:tension][cam:1.12|0|0][act:one eyebrow up][tune:rise]The kings ^before the flood? [act:dry, amused, slower]Two hundred and forty ^thousand years between them."], cut=False),
        B("world", 1, ["[d:calm][k:URUK][act:grounding it, plain and warm]He was king of Uruk, one of the ^first cities on Earth, with walls the poem says he ^built.",
                       "[d:build][go:2|0][sfx:shimmer][act:firm, a small delight]Uruk is ^real. [act:plain fact, easy]Its walls ran about ^nine kilometres."]),
        B("collision", 3, ["[d:build][k:IN STONE][act:storytelling, unhurried]In the poem, his ^rival is Aga of Kish, son of ^Enmebaragesi. [act:setting up the surprise]For a long time that name looked as ^legendary as the rest.",
                           "[d:reveal][act:the reveal, lean in]Then stone ^vessels turned up, from about {2600|^twenty-six hundred} BCE... [act:slower, savouring it]carved with the ^name. [act:reading it out, quiet wonder][tune:fall]^Enmebaragesi, king of Kish."]),
        B("cost", 4, ["[d:build][k:A GOD][act:measured, a touch of awe]And within a few ^generations of his supposed lifetime, Gilgamesh was being worshipped as a ^god."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:the catch, plainly][tune:fall]What's missing is his ^own inscription. [sfx:hit][act:the fair twist, a small smile]Which, for Uruk in that century, is missing for almost ^everyone.",
                          "[d:aside][act:light aside, matter of fact]The impossible reigns are ^another matter. [act:dry, reassuring]^Nobody reads those as years."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A ^real king behind the first epic hero? [act:the verdict, warm][tune:fall]^*Plausible*.",
                     "[d:tension][p:0.93][act:the last word, hopeful]^One inscription would make him ^*history*."]),
    ]
    return EP("gilgamesh", "09.03", "Gilgamesh: Was the First Epic Hero a Real King?", "gilgamesh", "plausible", "Was Gilgamesh a real king of Uruk?", "A hundred and twenty-six *years*.", beats, shots,
              "Weld-Blundell Prism, Ashmolean · Fara god lists · Enmebaragesi vessel fragments, Iraq Museum · George 2003, The Babylonian Gilgamesh Epic",
              "The Sumerian King List gives Gilgamesh 126 years. Uruk is real, his rival's father is named in stone, and he was a god within generations. What is missing.",
              ["#Gilgamesh", "#Mesopotamia", "#Sumer", "#Archaeology", "#History"])


def _star(x, y, s, at, c="#e8c35a", w=7):
    """The cuneiform sign for a god: an eight-pointed star of strokes."""
    import illus as I
    return [I.line([[round(x - s * math.cos(a), 1), round(y - s * math.sin(a), 1)], [round(x + s * math.cos(a), 1), round(y + s * math.sin(a), 1)]], round(at + .1 * k, 2), c, w, dur=.3)
            for k, a in enumerate((0, math.pi / 4, math.pi / 2, 3 * math.pi / 4))]


def gilgamesh_m():
    """Gilgamesh as one continuous take (see mural.py): 126 years as 126 squares, a reign beside 240,000 years, and the little star that made him a god."""
    remix, I = _mur()
    ep = gilgamesh()
    R = lambda w: _at(w, 26, 46)
    CLAY = "#b9a47c"
    tab = [I.box(110, 320, 260, 330, CLAY, "#8a6a48", 2, 22, R(1), fx="pop"),
           {"k": "glyphs", "x": 135, "y": 345, "w": 210, "h": 280, "rows": 9, "cols": 5, "kind": "cuneiform", "c": "#3b2a1c", "in": R(2)}, I.label(240, 700, "the King List", R(4), I.AMBER, 30)]
    years = [I.box(450 + 31 * (j % 14), 330 + 31 * (j // 14), 25, 25, I.AMBER, r=4, at=round(R(12) + .012 * j, 3), op=.85) for j in range(126)] + [I.label(667, 660, "126 years", R(15), I.AMBER, 34)]
    train = [I.box(140, 795, 130, 50, "#6f5a44", "#cbbca8", 2, 4, R(24), fx="pop"), I.box(225, 755, 45, 42, "#6f5a44", "#cbbca8", 2, 3, R(24), fx="pop"),
             I.box(160, 768, 18, 28, "#6f5a44", "#cbbca8", 2, 2, R(24), fx="pop")] + [I.dot(165 + 40 * j, 850, 13, "#cbbca8", R(24)) for j in range(3)] + \
            [I.dot(150 - 16 * j, 750 - 16 * j, 7 + 2 * j, "#cbbca8", round(R(24) + .2 + .1 * j, 2), op=.5) for j in range(3)]
    phone = [I.box(770, 750, 66, 116, "#1a1511", "#f5ecdc", 2.5, 12, R(29), fx="pop"), I.box(778, 762, 50, 88, "#3f86a8", r=4, at=R(29) + .1, op=.8)]
    span = [I.arrow([[300, 810], [745, 810]], R(26), I.AMBER, 3, "known", 1.0, False)]
    B = 1340
    bars = [I.line([[120, B], [880, B]], R(33), "#8a7a66", 3), I.box(250, B - 6, 120, 6, I.AMBER, r=2, at=R(34), fx="pop"), I.label(310, B + 48, "126 years", R(34), I.AMBER, 30),
            I.box(570, 960, 120, B - 960, I.LILAC, r=4, at=R(39), fx="fill", dur=1.4, op=.85), I.arrow([[630, 960], [630, 895]], R(42), I.LILAC, 5, "claimed", .5, False),
            I.label(630, B + 48, "240,000 years", R(41), I.LILAC, 30), I.label(550, 1010, "off the chart", R(43), I.LILAC, 28, "end")]
    reigns = {"base": "dark", "cam": [1, 500, 860], "els": tab + years + train + span + phone + bars}
    G = lambda w: _at(w, 16, 47)
    god = [I.label(500, 330, "god lists · Shuruppak · c. 2600 BCE", G(18), I.AMBER, 28),
           I.box(150, 370, 700, 360, CLAY, "#8a6a48", 2, 24, G(1), fx="pop")] + _star(300, 550, 85, G(6)) + \
          [I.glow(300, 550, 140, G(6), .45, "lamp"), {"k": "glyphs", "x": 420, "y": 495, "w": 380, "h": 110, "rows": 1, "cols": 5, "kind": "cuneiform", "c": "#3b2a1c", "in": G(17)},
           I.label(300, 800, "a god's sign", G(9), I.AU, 30), I.label(610, 800, "Gilgamesh", G(18), I.BONE, 30)]
    gens = [I.person(170 + 120 * k, 1250, 120, round(G(30) + .3 * k, 2)) for k in range(4)] + [I.label(350, 1310, "a few generations", G(32), "#cbbca8", 28),
            I.arrow([[620, 1170], [700, 1110], [760, 1090]], G(36), I.AU, 3, "inferred", .8, True)] + _star(830, 1060, 55, G(40)) + \
           [I.glow(830, 1060, 120, G(40), .6, "lamp"), I.label(830, 1170, "a god", G(42), I.AU, 32)]
    godly = {"base": "dark", "cam": [1, 500, 860], "els": god + gens}
    uruk = _quiet_iso(ep["shots"][2], drop=("one of the first cities on Earth",))
    return remix(ep, scenes={0: reigns, 2: uruk, 4: godly}, alias={6: 2}, cams={6: [1.1, 500, 900]})

# ---------------------------------------------------------------- 09.04 Where the Ark Came to Rest
def ark():
    v = View(37, 48, 35.5, 41.5, (40, 330, 920, 900))
    base = mapshot(v)
    lens = [[80 * math.cos(math.radians(a)), 19 * math.sin(math.radians(a))] for a in range(0, 360, 15)]
    hill = [{"t": "prism", "pts": lens, "y": 0, "h": 7, "c": "#6f5840", "edge": "rgba(255,236,206,.4)"},
            {"t": "prism", "pts": [[q[0] * .86, q[1] * .8] for q in lens], "y": 7, "h": 6, "c": "#7a6248", "edge": "rgba(255,236,206,.4)"},
            {"t": "prism", "pts": [[q[0] * .68, q[1] * .55] for q in lens], "y": 13, "h": 5, "c": "#87704f", "edge": "rgba(255,236,206,.4)"},
            {"t": "line", "p": [[-52, 18.2, 0], [-20, 18.2, -4], [20, 18.2, 3], [52, 18.2, 0]], "c": "#b8865a", "w": 2.5, "op": .9, "curve": True},
            L_(0, 20, "Durupınar · 160 m long", GOLD), L_(0, 0, "folded, iron-stained layers of local rock", "#cfe6ff", z=26, dy=40)]
    s0 = iso(hill, cam=[1, 500, 900], s=4.4, x=500, y=980, az=-24, spin=1.5, el=.5, table=None)
    s0["els"] += [{"k": "q", "x": 500, "y": 560, "size": 70, "in": .8, "fx": "pop"}]
    s1 = like(base, add=[{"k": "pin", "x": v.p(44.3, 39.7)[0], "y": v.p(44.3, 39.7)[1], "t": "Mount Ararat · 5,137 m", "c": BONE, "in": .3},
                         {"k": "pin", "x": v.p(44.24, 39.44)[0], "y": v.p(44.24, 39.44)[1], "t": "Durupınar", "c": GOLD, "a": "end", "lx": -18, "ly": 40, "in": .6},
                         {"k": "pin", "x": v.p(42.45, 37.35)[0], "y": v.p(42.45, 37.35)[1], "t": "Cudi Dağı · al-Judi", "c": SCAN, "in": 1.0},
                         {"k": "poly", "p": [v.p(41, 40.8), v.p(46.5, 40.8), v.p(46.5, 37.8), v.p(41, 37.8)], "fill": "rgba(232,184,122,.12)", "c": GOLD, "w": 1.2, "style": "inferred", "in": 1.3},
                         {"k": "label", "x": v.p(43.7, 41.1)[0], "y": v.p(43.7, 41.1)[1], "t": "Urartu · 'the mountains of Ararat'", "st": "small", "c": GOLD, "in": 1.5},
                         {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = quote("Genesis names a region, Urartu. The Quran names al-Judi. Berossus, the Syriac writers and the Aramaic Targum all point to the Cudi range, far to the south.", "where the older witnesses put the landing", y=680, size=38)
    s3 = like(s0, cam=[1.3, 500, 960], add=[{"k": "label", "x": 500, "y": 560, "t": "'rivets', 'beams', 'anchors': natural minerals and local andesite", "st": "small", "c": "#cfe6ff", "in": .4},
                                            {"k": "label", "x": 500, "y": 1300, "t": "excavation found soil and rock · no wood or joinery published", "st": "small", "in": 1.0}])
    tl, ax = timeline(-1000, 2600, [(-1000, "1000 BCE"), (0, "1 CE"), (1000, "1000"), (2000, "2000")], "Where the tradition pointed, over time", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-300), "x1": ax.x(700), "y": 720, "h": 18, "c": SCAN, "t": "the Cudi range · Berossus to the Syriac writers", "in": .3},
                  {"k": "band", "x0": ax.x(610), "x1": ax.x(700), "y": 640, "h": 18, "c": "#cfe6ff", "t": "al-Judi · Quran 11:44", "in": .6},
                  {"k": "band", "x0": ax.x(1000), "x1": ax.x(1900), "y": 560, "h": 18, "c": AMBER, "t": "the high peak of Ararat · medieval tradition", "in": .9},
                  {"k": "band", "x0": ax.x(1948), "x1": ax.x(2000), "y": 480, "h": 18, "c": GOLD, "t": "Durupınar · noticed 1948", "in": 1.2}]
    s4 = tl
    s5 = like(s1, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:EASTERN TURKEY][sfx:boom][act:setting the scene, intrigued][tune:level]A hill shaped like a ^boat. [act:adding detail, same rhythm][tune:level]A hundred and ^sixty metres long. [act:the name that matters, lower]Near Mount ^Ararat.",
                      "[d:tension][cam:1.12|0|0][act:hushed, sincere, asking][tune:rise]Is ^this where the Ark came to rest?"], cut=False),
        B("world", 1, ["[d:calm][k:THE TEXTS][act:respectful, careful and precise]Genesis says the mountains of Ararat, which is a ^region, the old kingdom of Urartu, not ^one peak.",
                       "[d:build][act:with care, even-handed]The Quran names ^al-Judi. [go:2|0][act:building, a scholar's pleasure]And the ^oldest witnesses, Berossus, the Syriac writers, the Aramaic Targum, all point to the ^Cudi range. [act:placing it on the map]Far to the ^south."]),
        B("collision", 3, ["[d:build][k:THE HILL][act:curious, turning to it][tune:fall]So what ^is the boat-shaped hill? [act:plain, the evidence]Geologists who mapped it found ^folded, iron-stained layers of ^local rock.",
                           "[d:list][act:ticking them off, dry][tune:level]The 'rivets' are ^minerals. [act:the next, same tone][tune:level]The 'anchors' are local ^stone. [act:the last, firm and final]Digging found soil and rock; no ^wood, no ^joinery."]),
        B("cost", 4, ["[d:build][k:THE TRADITION][act:explaining, even and clear]The high peak of Ararat ^only became the favourite in the ^Middle Ages. [d:aside][act:a quick aside, lighter]The hill was noticed in {1948|^nineteen forty-eight}."]),
        B("reversal", 3, ["[d:reveal][k:THE TWIST][sfx:hit][act:the twist, even-handed and clear]The textbooks and the hill's fans make the ^same mistake: they assume the tradition ^always meant Ararat. [act:quietly decisive]The ^older witnesses say ^otherwise."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]^This hillside? [act:the verdict, firm and fair][tune:fall]*Ruled ^out*. [act:turning, respectful][tune:rise]The ^landing place? [act:measured, with care]The texts point ^elsewhere.",
                     "[d:tension][p:0.93][act:sincere, clear about limits]We rate a ^hill. [act:respectful, quiet and even]Not the ^story it was mistaken for."]),
    ]
    return EP("ark-rest", "09.04", "Where the Ark Came to Rest: Ararat, Judi, Durupınar", "durupinar", "debunked", "Is the Durupınar formation the Ark?", "A hill shaped like a *boat*.", beats, shots,
              "Collins & Fasold 1996, Journal of Geoscience Education · Josephus, Antiquities 1.93 (Berossus) · Quran 11:44 · Genesis 8:4",
              "A boat-shaped hill near Ararat is called the petrified Ark. Geology says folded rock. And the oldest traditions, including the Quran's al-Judi, point to a different mountain.",
              ["#NoahsArk", "#Ararat", "#Geology", "#History", "#Archaeology"])


def ark_m():
    """The Ark's resting place as one continuous take (see mural.py): the old witnesses pointing south to the Cudi range, and the hill as a fold of rock, cut open."""
    remix, I = _mur()
    from f01 import mapshot
    ep = ark()
    v = View(37, 48, 35.5, 41.5, (40, 330, 920, 900))
    W = lambda w: _at(w, 21, 32)
    axx, axy = v.p(44.3, 39.7); cx, cy = v.p(42.45, 37.35)
    wit = mapshot(v)["els"] + [{"k": "pin", "x": axx, "y": axy, "t": "Mount Ararat", "c": I.BONE, "in": .1},
                               {"k": "pin", "x": cx, "y": cy, "t": "Cudi range", "c": "#9fd0ff", "a": "end", "lx": -18, "in": W(16)}, I.glow(cx, cy, 80, W(16), .8), I.ring(cx, cy, 44, W(16), "#9fd0ff", 3)]
    for k, (x, t, w) in enumerate(((210, "Berossus", 4), (500, "Syriac writers", 8), (790, "Targum", 13))):
        wit += [I.box(x - 60, 1235, 120, 64, "#d8c9a8", "#8a7a66", 2, 4, W(w), fx="pop"), I.box(x - 74, 1226, 22, 82, "#b9a47c", "#8a7a66", 2, 10, W(w), fx="pop"),
                I.box(x + 52, 1226, 22, 82, "#b9a47c", "#8a7a66", 2, 10, W(w), fx="pop"), I.label(x, 1350, t, W(w), I.BONE, 30),
                I.arrow([[x, 1215], [round((x + cx) / 2 + 20, 1), round((1215 + cy) / 2 + 30, 1)], [cx, cy + 30]], W(w) + .3, "#9fd0ff", 3, "known", 1.0, True)]
    wit += [I.line([[axx, axy], [cx, cy]], W(22), I.AMBER, 3, "inferred", 1.0), I.label(round((axx + cx) / 2 + 24, 1), round((axy + cy) / 2, 1), "about 300 km", W(24), I.AMBER, 30, "start")]
    witnesses = {"base": "map", "cam": [1, 500, 860], "els": wit}
    S = lambda w: _at(w, 38, 76)
    G0 = 640
    curve = lambda k: [[x, round(G0 + 55 * k + 110 * math.sin(math.pi * (x - 100) / 800), 1)] for x in range(100, 901, 50)]
    cols = ("#8a5a3a", "#9c8a74", "#7a4a30", "#a89884", "#6f5a44")
    fold = [I.line([[80, G0], [920, G0]], 0, "#8a6a48", 3, draw=False),
            {"k": "poly", "p": [[250, G0], [330, 600], [500, 582], [670, 600], [750, G0]], "fill": "#7a6248", "c": "#e8d3a8", "w": 2, "curve": True, "in": S(2), "fx": "rise"},
            I.label(500, 560, "the boat-shaped hill", S(3), I.BONE, 28)]
    for k in range(5):
        top = curve(k)
        top[0][1] = top[-1][1] = G0 + 55 * k
        fold.append({"k": "poly", "p": top + curve(k + 1)[::-1], "fill": cols[k], "c": "rgba(255,236,206,.35)", "w": 1.2, "in": round(S(11) + .35 * k, 2), "fx": "fill", "dur": .7})
    fold += [I.arrow([[70, 820], [190, 820]], S(24), I.AMBER, 5, "known", .6, False), I.arrow([[930, 820], [810, 820]], S(24), I.AMBER, 5, "known", .6, False),
             I.label(500, 1060, "folded, iron-stained rock", S(16), "#ffb09a", 30)]
    lens = [[250, 400], [370, 345], [500, 330], [630, 345], [750, 400], [630, 455], [500, 470], [370, 455]]
    fold += [{"k": "poly", "p": lens, "fill": "rgba(138,90,58,.55)", "c": "#e8d3a8", "w": 2.5, "in": S(42), "fx": "draw", "dur": 1.0},
             {"k": "poly", "p": [[round(500 + (x - 500) * .6, 1), round(400 + (y - 400) * .55, 1)] for x, y in lens], "fill": "none", "c": "#e8d3a8", "w": 1.5, "in": S(44), "fx": "draw", "dur": .8},
             I.label(500, 300, "seen from above", S(43), "#cbbca8", 28)]
    fold += [I.dot(180 + 22 * (j % 4), 1200 + 18 * (j // 4), 7, I.AU, round(S(56) + .05 * j, 2)) for j in range(8)] + [I.label(215, 1330, "minerals", S(57), I.AU, 30)] + \
            [{"k": "poly", "p": [[440, 1250], [460, 1200], [520, 1190], [545, 1235], [520, 1255]], "fill": "#9c9488", "c": "#e8d3a8", "w": 2, "in": S(62), "fx": "pop"},
             {"k": "poly", "p": [[500, 1255], [530, 1215], [570, 1225], [575, 1255]], "fill": "#7d766c", "c": "#e8d3a8", "w": 2, "in": S(62) + .15, "fx": "pop"}, I.label(505, 1330, "local stone", S(63), I.BONE, 30),
             I.box(720, 1205, 130, 32, "#8a6a44", "#e7c99a", 2, 3, S(70), fx="pop"), I.strike(705, 1260, 865, 1180, S(72)), I.label(785, 1330, "no wood", S(71), I.RED, 30)]
    section = {"base": "dark", "cam": [1, 500, 860], "els": fold}
    hill = _quiet_iso(ep["shots"][0], drop=("folded, iron-stained layers of local rock",))
    return remix(ep, scenes={0: hill, 2: witnesses, 3: section}, alias={5: 1}, cams={5: [1.15, 500, 880]})

# ---------------------------------------------------------------- 09.05 The Tower of Babel
def babel():
    zig = []
    sizes = [(91, 33), (78, 18), (60, 6), (51, 6), (42, 6), (33, 6), (24, 15)]
    y = 0
    for i, (b, h) in enumerate(sizes):
        zig.append({"t": "box", "x": 0, "z": 0, "y": y, "w": b, "d": b, "h": h, "c": "#c49a68" if i % 2 == 0 else "#b88a64", "edge": "rgba(0,0,0,.28)"}); y += h
    zig += [{"t": "line", "p": [[-45.5, 0, 46], [-45.5, 33, 46], [-45.5, 33, 20]], "c": "#f2dcb4", "w": 3, "op": .9},   # the great stair, as a line
            L_(0, y + 6, "Etemenanki · c. 91 m square, about 90 m tall", GOLD), L_(0, 2, "fired brick and bitumen", "#cfe6ff", z=60, dy=40)]
    s0 = iso(zig, cam=[1, 500, 900], s=4.0, x=500, y=1100, az=-28, spin=1.6, el=.42, table={"r": 90, "rz": 90, "grid": 15, "strata": [{"h": 2, "c": "#a8845c"}, {"h": 8, "c": "#7d6045"}]})
    v = View(42, 48, 29.5, 34.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Babylon", 44.42, 32.54, {"c": GOLD}), ("Uruk", 45.64, 31.32, {}), ("Ur", 46.1, 30.96, {"a": "end", "lx": -18})], extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    tl, ax = timeline(-750, -500, [(-750, "750 BCE"), (-700, "700"), (-650, "650"), (-600, "600"), (-550, "550"), (-500, "500")], "The tower, wrecked and rebuilt", y=980)
    tl["els"] += event(ax, -689, "wrecked · Sennacherib", row=0, c=RED, i=.3) + event(ax, -620, "rebuilt · Nabopolassar", row=1, c=AMBER, i=.6) + \
                 event(ax, -580, "finished · Nebuchadnezzar II", row=2, c=GOLD, i=.9, sub="Judean exiles in Babylon") + event(ax, -597, "the exile begins", row=0, c=SCAN, i=1.2)
    s2 = tl
    s3 = {"base": "paper", "kind": "stone", "x": 230, "y": 380, "w": 540, "h": 820, "holes": [], "cam": [1.05, 500, 860], "els": [
        {"k": "poly", "p": [[500, 480], [430, 760], [570, 760]], "fill": "#8a6a4a", "c": "#e9dccb", "w": 1.4, "in": .3},
        {"k": "person", "x": 620, "y": 760, "h": 110, "t": False, "in": .6},
        {"k": "glyphs", "x": 290, "y": 840, "w": 420, "h": 260, "rows": 6, "cols": 7, "kind": "cuneiform", "in": .8},
        {"k": "cap", "x": 500, "y": 300, "t": "the Tower of Babel stele · Nebuchadnezzar's reign", "in": .2},
        {"k": "label", "x": 500, "y": 1260, "t": "the oldest known image of the tower, the king beside it", "st": "small", "in": 1.2}]}
    s4 = quote("I made workers from all the lands of the world carry the brick.", "Nebuchadnezzar II · the royal boast", y=720, size=44)
    s5 = like(s0, cam=[1.15, 500, 1000])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:BABYLON][sfx:boom][act:the surprise, confident]The Tower of Babel was a ^real building. [act:quiet, sure]We ^know where it stood.",
                      "[d:tension][cam:1.12|0|0][act:measuring it out, wonder][tune:level]^Ninety-one metres on a side. [act:slower, looking up]^Seven steps to the top."], cut=False),
        B("world", 1, ["[d:calm][k:ETEMENANKI][act:introducing it, respectful]Its name was ^Etemenanki, the temple tower of the god ^Marduk, in the middle of Babylon.",
                       "[d:build][go:2|0][act:a brisk history][tune:level]^Wrecked in {689|six eighty-nine} BCE. [act:same pace][tune:level]^Rebuilt by ^three kings. [sfx:shimmer][act:slowing, the detail that matters]^Finished by Nebuchadnezzar, while exiles from ^Judah lived in the city."]),
        B("collision", 3, ["[d:build][k:IN STONE][act:showing you, pleased]A ^stele from his reign shows the king ^beside the stepped tower. [act:quiet wonder, warm]The ^oldest picture of it we have."]),
        B("cost", 4, ["[d:build][k:THE BOAST][act:quoting him, a little grand]And the king's ^own words: workers from ^all the lands of the world carried the brick. [d:aside][act:warm, delighted aside]^Every tongue on ^one building site."]),
        B("reversal", 0, ["[d:reveal][k:THE TWIST][act:gathering it up, building]The name, the ^pun on it, the fired ^brick and bitumen, the stepped ^tower, the many ^languages... [sfx:hit][act:the reveal, slower and sure]^every detail of the story has a match in the ^ground."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]The ^tower behind the story? [act:the verdict, confident][tune:fall]^*Strong* evidence. [act:turning, with care][tune:rise]The scattering of languages in a ^day? [act:respectful, sincere and even]That belongs to ^faith, and we don't ^grade it.",
                     "[d:tension][p:0.93][act:gentle, thoughtful]What we ^can measure... [act:the last word, a warm smile]is the ^*brick*."]),
    ]
    return EP("babel", "09.05", "The Tower of Babel Stood in Babylon", "babel", "strong", "Was the Tower of Babel a real building?", "We know where it *stood*.", beats, shots,
              "Koldewey 1914 · George 2005/2006, Archiv für Orientforschung · Schøyen Collection MS 2063 · Finkel & Seymour 2008",
              "Babylon's ziggurat Etemenanki, wrecked in 689 BCE and rebuilt by kings who boasted of workers from every land: the building behind the Tower of Babel.",
              ["#Babel", "#Babylon", "#Archaeology", "#Bible", "#History"])


def babel_m():
    """Babel as one continuous take (see mural.py): the tower wrecked and rebuilt tier by tier on its own timeline, and workers from every land carrying brick."""
    remix, I = _mur()
    ep = babel()
    RB = lambda w: _at(w, 20, 31)
    sizes = [(91, 33), (78, 18), (60, 6), (51, 6), (42, 6), (33, 6), (24, 15)]
    k, y = 4.6, 900
    ghost, tiers = [], []
    for j, (b, h) in enumerate(sizes):
        x0, hh = 500 - b * k / 2, h * k
        ghost.append({"k": "rect", "x": round(x0, 1), "y": round(y - hh, 1), "w": round(b * k, 1), "h": round(hh, 1), "fill": "none", "c": "#cbbca8", "sw": 2, "style": "claimed", "in": 0, "op": .5, "keepop": True})
        tiers.append(I.box(round(x0, 1), round(y - hh, 1), round(b * k, 1), round(hh, 1), "#c49a68" if j % 2 == 0 else "#b88a64", "rgba(40,30,20,.6)", 1.5, 2, round(RB(11) + .3 * j, 2), fx="pop"))
        y -= hh
    X = lambda yr: round(120 + (750 - yr) * 760 / 250, 1)
    axis = [I.line([[120, 1150], [880, 1150]], 0, "#8a7a66", 3, draw=False)] + \
           [I.line([[X(yr), 1140], [X(yr), 1160]], 0, "#8a7a66", 2, draw=False) for yr in (750, 700, 650, 600, 550, 500)] + \
           [I.label(X(yr), 1200, t, 0, "#8a7a66", 28) for yr, t in ((750, "750 BCE"), (650, "650"), (550, "550"))]
    wreck = [{"k": "poly", "p": [[290, 900], [340, 862], [420, 850], [500, 838], [600, 852], [680, 866], [720, 900]], "fill": "#7d5a40", "c": I.RED, "w": 2, "in": RB(7), "fx": "rise"},
             I.glow(500, 860, 180, RB(7), .5, "red"), I.dot(X(689), 1150, 11, I.RED, RB(7)), I.label(X(689), 1110, "689 · wrecked", RB(8), I.RED, 28)]
    built = [I.dot(X(620), 1150, 10, I.AMBER, RB(11)), I.label(X(620) - 20, 1250, "rebuilt", RB(12), I.AMBER, 28),
             I.glow(500, 470, 120, RB(16), .55, "lamp"), I.dot(X(580), 1150, 11, I.AU, RB(16)), I.label(X(580) + 10, 1110, "finished", RB(16), I.AU, 28, "start"),
             I.dot(X(597), 1150, 9, "#9fd0ff", RB(24)), I.label(X(597) + 40, 1300, "exiles from Judah", RB(24), "#9fd0ff", 28)] + \
            [I.person(X(597) - 10 + 34 * j, 1400, 64, round(RB(25) + .2 * j, 2), c="#b8c9d6") for j in range(4)]
    rebuild = {"base": "dark", "cam": [1, 500, 860], "els": ghost + axis + wreck + tiers + built}
    WK = lambda w: _at(w, 22, 35)
    G = 1250
    bricks = []
    idx = 0
    for r in range(6):
        n = 8 - r
        for j in range(n):
            bricks.append(I.box(round(500 - n * 68 / 2 + 68 * j, 1), G - 30 * (r + 1), 64, 27, "#b4673e", "#e8b07a", 1.5, 3, round(WK(14) + .05 * idx, 2), fx="pop")); idx += 1
    folk = [(105, G, 150, "#e8d6b8", "cuneiform"), (215, G, 135, "#c9a878", "hieratic"), (330, 1150, 95, "#b8c9d6", "latin"),
            (670, 1150, 95, "#d6b8c9", "hieroglyph"), (785, G, 135, "#c9d6b8", "cuneiform"), (895, G, 150, "#d6c9a0", "hieratic")]
    crowd = []
    for j, (x, yb, h, c, kind) in enumerate(folk):
        t = round(WK(12) + .25 * j, 2)
        crowd += [I.person(x, yb, h, t, c=c), I.box(x - 18, yb - h - 26, 36, 18, "#b4673e", "#e8b07a", 1.5, 2, t, fx="pop"),
                  I.box(x - 55, yb - h - 100, 110, 52, "rgba(245,236,220,.08)", "#f5ecdc", 1.5, 18, round(WK(26) + .25 * j, 2), fx="pop"),
                  {"k": "glyphs", "x": x - 42, "y": yb - h - 90, "w": 84, "h": 32, "rows": 1, "cols": 3, "kind": kind, "c": "#f5ecdc", "in": round(WK(26) + .25 * j + .1, 2)}]
    crowd += [I.line([[60, G], [940, G]], 0, "#8a6a48", 3, draw=False), I.glow(500, 1100, 260, WK(14), .3, "lamp"),
              I.label(500, 1330, "workers from all lands", WK(16), I.BONE, 30), I.label(500, 700, "every tongue, one site", WK(31), I.AMBER, 34)]
    workers = {"base": "dark", "cam": [1, 500, 900], "els": crowd + bricks}
    zig = _quiet_iso(ep["shots"][0], drop=("fired brick and bitumen",))
    return remix(ep, scenes={0: zig, 2: rebuild, 4: workers}, alias={5: 0}, cams={5: [1.15, 500, 1000]})

# ---------------------------------------------------------------- 09.06 Iram of the Pillars
def iram():
    v = View(51, 57, 16, 20.5, (40, 330, 920, 900))
    tracks = [[(53.2, 19.4), (53.5, 18.8), (53.66, 18.26)], [(54.1, 19.6), (53.9, 18.9), (53.66, 18.26)], [(53.66, 18.26), (54.0, 17.6), (54.44, 17.04)]]
    s0 = {"base": "dark", "stars": 0, "cam": [1.1, 500, 860], "els": [{"k": "rect", "x": 80, "y": 380, "w": 840, "h": 960, "fill": "#2a2216", "c": "#4a3c2a", "sw": 2, "in": .1}] +
          [{"k": "line", "p": [[x, y], [500, 1000]], "c": "#c9a070", "w": 1.4, "op": .55, "in": .3 + k * .12, "fx": "draw", "dur": 1.4}
           for k, (x, y) in enumerate([(140, 380), (330, 380), (560, 380), (760, 380), (80, 560), (80, 900), (920, 620), (920, 1300), (300, 1340)])] +
          [{"k": "glow", "x": 500, "y": 1000, "r": 60, "kind": "lamp", "op": .8, "in": 1.5}, {"k": "circle", "x": 500, "y": 1000, "r": 5, "fill": "#ffe2a8", "c": "none", "w": 0, "in": 1.5},
           {"k": "label", "x": 500, "y": 1050, "t": "Shisr", "c": GOLD, "in": 1.7},
           {"k": "cap", "x": 500, "y": 330, "t": "space shuttle radar · 1984", "in": .2}, {"k": "label", "x": 500, "y": 1400, "t": "old caravan tracks under the sand, converging", "in": 1.0}]}
    s1 = mapshot(v, pins=[("Shisr", 53.66, 18.26, {"c": GOLD}), ("Khor Rori · the port", 54.44, 17.04, {"c": SCAN}), ("Wadi Dawkah · frankincense", 54.05, 17.35, {"a": "end", "lx": -18, "ly": 40})],
                 extra=[{"k": "line", "p": [v.p(*q) for q in t], "c": "#c9a070", "w": 1.6, "op": .7, "style": "claimed", "curve": True, "in": .8 + i * .2} for i, t in enumerate(tracks)] +
                       [{"k": "label", "x": v.p(53.7, 19.9)[0], "y": v.p(53.7, 19.9)[1], "t": "the Empty Quarter", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    ring = [[16 + 12 * math.cos(math.radians(a)), 12 + 9 * math.sin(math.radians(a))] for a in range(0, 360, 20)]
    fort = [{"t": "box", "x": 0, "z": -14, "y": 0, "w": 40, "d": 3, "h": 6, "c": "#b88a64", "edge": "rgba(0,0,0,.25)"}, {"t": "box", "x": -19, "z": 0, "y": 0, "w": 3, "d": 30, "h": 6, "c": "#b88a64", "edge": "rgba(0,0,0,.25)"},
            {"t": "box", "x": 19, "z": -6, "y": 0, "w": 3, "d": 18, "h": 6, "c": "#b88a64", "edge": "rgba(0,0,0,.25)"}, {"t": "box", "x": -8, "z": 14, "y": 0, "w": 24, "d": 3, "h": 6, "c": "#b88a64", "edge": "rgba(0,0,0,.25)"}] + \
           [{"t": "cyl", "x": x, "z": z, "y": 0, "r": 3, "h": 9, "c": "#c49a68", "n": 10, "edge": "rgba(0,0,0,.25)"} for x, z in ((-20, -15), (20, -15), (-20, 15))] + \
           [{"t": "flat", "pts": ring, "y": .3, "c": "#1e1710", "op": 1, "ground": False, "over": 3},
            {"t": "cyl", "x": 16, "z": 12, "y": -14, "r": 11, "h": 14, "c": "#2a2016", "n": 18, "edge": "rgba(255,236,206,.35)", "xray": True},
            L_(0, 9, "Shisr · the fort over the well", GOLD, z=-16, dy=-30), L_(16, -14, "the limestone cavern beneath", "#cfe6ff", z=12, dy=40), L_(16, 1, "the sinkhole", "#ffb09a", z=12, dy=-6)]
    s2 = iso(fort, cam=[1, 500, 900], s=6, x=500, y=1000, az=-30, spin=1.6, el=.5, table={"r": 50, "rz": 45, "grid": 10, "strata": [{"h": 2, "c": "#d9c39a"}, {"h": 12, "c": "#a8845c"}]})
    s2["els"] += [{"k": "label", "x": 500, "y": 1380, "t": "part of the fort collapsed into the sinkhole", "st": "small", "in": 1.0}]
    tl, ax = timeline(-3000, 1000, [(-3000, "3000 BCE"), (-2000, "2000"), (-1000, "1000"), (0, "1 CE"), (1000, "1000")], "Whose ruin is it?", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-300), "x1": ax.x(700), "y": 720, "h": 18, "c": GOLD, "t": "Shisr's main phases", "in": .3},
                  {"k": "band", "x0": ax.x(-3000), "x1": ax.x(-1500), "y": 640, "h": 18, "c": SCAN, "t": "ʿĀd · placed before Thamud", "in": .6, "style": "inferred"},
                  {"k": "label", "x": 500, "y": 540, "t": "a gap of a thousand years or more", "c": "#ffb09a", "in": 1.0}]
    s3 = tl
    s4 = quote("Ubar was a region, not this town.", "Juris Zarins, who dug Shisr · his own conclusion", y=760, size=46)
    s5 = like(s1, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE EMPTY QUARTER][sfx:boom][act:setting the scene, intrigued]From orbit, radar saw old ^roads under the ^sand. [act:leaning in, slower]All leading to ^one place.",
                      "[d:tension][cam:1.12|0|0][act:the hook, hushed][tune:rise]A ^lost city of the desert@noun?"], cut=False),
        B("world", 1, ["[d:calm][k:OMAN · 1992][act:respectful, measured]The Quran remembers ^Iram of the pillars, city of the people of ^ʿĀd. [act:a touch of romance, lighter]Legend called it ^Ubar, the Atlantis of the ^sands.",
                       "[d:build][go:2|0][act:storytelling, building]The tracks led to ^Shisr: a fort with towers around a well, [sfx:shimmer]half swallowed by a ^sinkhole. [act:wonder, slower]A city that ^fell into the earth."]),
        B("collision", 3, ["[d:build][k:THE DATES][act:the complication, plain][tune:fall]But the fort's main phases run from about ^three hundred BCE into ^Islamic times.",
                           "[d:build][act:careful, respectful, precise]The Quran places ʿĀd ^before Thamud, who are attested by ^seven hundred BCE. [act:the gap, plainly]That's a gap of a ^thousand years or more."]),
        B("cost", 4, ["[d:build][k:THE DIGGER][act:plain, a careful fact]^No inscription names Iram or ʿĀd. [act:fair, the expert's view]And the man who ^excavated Shisr concluded that Ubar was a ^region, not this town."]),
        B("reversal", 1, ["[d:reveal][k:THE TWIST][act:turning, a warm yes]The ^collapse is real. [act:building, pleased]The trade is real: this was ^frankincense country, [sfx:hit]and the roads under the sand carried it to the ^sea."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Shisr as ^Iram? [act:the verdict, level-headed][tune:fall]^*Awaiting* evidence. [act:open, respectful]ʿĀd's remains may lie ^elsewhere under the sands.",
                     "[d:tension][p:0.93][act:the last word, quiet wonder]The desert@noun has not ^finished giving things back."]),
    ]
    return EP("iram", "09.06", "ʿĀd and Iram of the Pillars", "iram-ubar", "unsupported", "Is the fort at Shisr the lost Iram?", "A lost city of the *desert*?", beats, shots,
              "Zarins 1997, Journal of the American Oriental Society · Clapp 1998, The Road to Ubar · Edgell 2004, PSAS · UNESCO, Land of Frankincense",
              "Radar from orbit led explorers to a fort swallowed by a sinkhole in Oman. The case that it is Iram of the pillars, and the dates that leave a thousand-year gap.",
              ["#Iram", "#Ubar", "#Oman", "#Archaeology", "#History"])


def iram_m():
    """Iram and Shisr as one continuous take (see mural.py): radar seeing through sand to buried tracks, the gap in the dates, and a region that is not a town."""
    remix, I = _mur()
    ep = iram()
    RD = lambda w: _at(w, 20, 60)
    SAND = "#b0916a"
    sh = [{"k": "poly", "p": [[140, 330], [230, 316], [272, 330], [230, 344]], "fill": "#e9e4da", "c": "#ffffff", "w": 1.5, "in": RD(3), "fx": "pop"},
          {"k": "poly", "p": [[175, 338], [230, 338], [205, 372]], "fill": "#cfc8bb", "c": "none", "w": 0, "in": RD(3), "fx": "pop"},
          I.label(300, 340, "space shuttle · 1984", RD(4), I.BONE, 28, "start")]
    ground = [I.box(60, 560, 880, 150, SAND, r=0, at=0, op=.9), I.label(820, 610, "dry sand", RD(16), "#2a1d10", 28, halo=False),
              I.line([[60, 672], [940, 672]], RD(21), "#3b2a1c", 7)]
    beams = [I.line([[220, 360], [x, 560]], round(RD(8) + .1 * j, 2), "#9fd0ff", 2, "inferred", .6) for j, x in enumerate((180, 260, 340, 420))] + \
            [I.line([[x, 560], [x + 30, 668]], round(RD(17) + .1 * j, 2), "#9fd0ff", 3, "claimed", .5) for j, x in enumerate((180, 260, 340, 420))] + \
            [I.arrow([[440, 668], [520, 520], [560, 420]], RD(22), "#9fd0ff", 3, "known", .8, True), I.label(680, 655, "old track", RD(22), "#f5ecdc", 28)]
    plan = [I.box(80, 780, 840, 600, "#2a2216", "#4a3c2a", 2, 4, RD(36), fx="pop"), I.label(110, 830, "seen from above", RD(36), "#cbbca8", 28, "start")]
    plan += [I.line([[x, y], [500, 1220]], round(RD(38) + .12 * j, 2), "#c9a070", 2, dur=1.2, op=.7)
             for j, (x, y) in enumerate([(140, 780), (330, 780), (560, 780), (760, 780), (80, 920), (80, 1160), (920, 880), (920, 1300), (300, 1380)])]
    plan += [I.glow(500, 1220, 70, RD(45), .9, "lamp"), I.dot(500, 1220, 7, "#ffe2a8", RD(45)), I.label(500, 1280, "Shisr", RD(46), I.AU, 32)] + I.question(700, 1100, RD(52), 100)
    radar = {"base": "dark", "cam": [1, 500, 860], "els": sh + ground + beams + plan}
    RG = lambda w: _at(w, 21, 38)
    slab = [{"k": "poly", "p": [[330, 360], [670, 360], [700, 400], [700, 720], [300, 720], [300, 400]], "fill": "#8d7a64", "c": "#bdb5a8", "w": 2, "in": RG(1), "fx": "pop"}] + \
           [I.line([[340, 430 + 52 * j], [660, 430 + 52 * j]], round(RG(3) + .1 * j, 2), "#cbbca8", 2, "claimed", .4, op=.5) for j in range(5)] + \
           I.question(500, 600, RG(6), 110) + [I.label(500, 790, "no name found", RG(7), I.BONE, 30)]
    reg = [{"k": "poly", "p": [[150, 1010], [300, 890], [520, 870], [760, 910], [860, 1050], [820, 1250], [600, 1350], [330, 1330], [160, 1210]], "fill": "rgba(232,184,122,.12)",
            "c": I.AMBER, "w": 3, "style": "inferred", "curve": True, "in": RG(20)},
           I.label(500, 960, "Ubar: a region?", RG(21), I.AMBER, 32),
           I.box(560, 1130, 36, 36, "#b88a64", "#f5ecdc", 2, 2, RG(13), fx="pop"), I.label(578, 1240, "Shisr", RG(14), I.BONE, 30), I.ring(578, 1148, 50, RG(25), I.BONE, 2)]
    region = {"base": "dark", "cam": [1, 500, 860], "els": slab + reg}
    _, ax = timeline(-3000, 1000, [(-3000, "3000 BCE"), (-2000, "2000"), (-1000, "1000"), (0, "1 CE"), (1000, "1000")], "Whose ruin is it?", y=980)
    g0, g1 = ax.x(-1500), ax.x(-300)
    gap = [I.arrow([[(g0 + g1) / 2, 680], [g0 + 6, 680]], _at(50, 36, 59), I.RED, 3, "known", .5, False), I.arrow([[(g0 + g1) / 2, 680], [g1 - 6, 680]], _at(50, 36, 59), I.RED, 3, "known", .5, False)]
    return remix(ep, scenes={0: radar, 4: region}, alias={5: 1}, cams={5: [1.15, 500, 880]}, adds={3: gap})

# ---------------------------------------------------------------- 09.07 Thamud
def thamud():
    rock = [[-46, -20], [-30, -24], [0, -22], [30, -25], [46, -18], [48, 0], [44, 20], [20, 22], [-10, 20], [-40, 22], [-48, 6]]
    fac = [(-30, 20, 18), (-8, 22, 22), (14, 20, 19), (34, 21, 16)]                                  # x, z of the face, height of the facade
    cliff = [{"t": "prism", "pts": rock, "y": 0, "h": 30, "c": "#b8865a", "edge": "rgba(0,0,0,.25)"}] + \
            [{"t": "quad", "p": [[x - 8, 0.2, z + .3], [x + 8, 0.2, z + .3], [x + 8, h, z + .3], [x - 8, h, z + .3]], "n": [0, 0, 1], "c": "#8a6040", "op": 1, "over": 3} for x, z, h in fac] + \
            [{"t": "quad", "p": [[x - 3, 0.2, z + .5], [x + 3, 0.2, z + .5], [x + 3, 7, z + .5], [x - 3, 7, z + .5]], "n": [0, 0, 1], "c": "#2a1f16", "op": 1, "over": 4} for x, z, h in fac] + \
            [{"t": "line", "p": [[x - 8, h, z + .6], [x - 5, h + 2, z + .6], [x - 5, h + 3.5, z + .6], [x + 5, h + 3.5, z + .6], [x + 5, h + 2, z + .6], [x + 8, h, z + .6]], "c": "#f2dcb4", "w": 2, "op": .9} for x, z, h in fac] + \
            [{"t": "person", "x": 48, "y": 0, "z": 28, "h": 1.7}, L_(0, 34, "Hegra · rock-cut facades", GOLD, dy=-14), L_(0, -1, "carved into the sandstone outcrops", "#cfe6ff", z=34, dy=40)]
    s0 = iso(cliff, cam=[1, 500, 900], s=5.4, x=500, y=1000, az=-16, spin=1.2, el=.4, table={"r": 70, "rz": 45, "grid": 10, "strata": [{"h": 2, "c": "#d9c39a"}, {"h": 8, "c": "#a8845c"}]})
    v = View(33, 44, 22, 31, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Hegra · al-Hijr", 37.95, 26.79, {"c": GOLD}), ("Ruwafa · the temple", 36.9, 27.9, {"c": SCAN, "a": "end", "lx": -18}), ("Tayma", 38.5, 27.63, {"a": "start"}), ("Medina", 39.6, 24.47, {})],
                 extra=[{"k": "label", "x": v.p(36, 25)[0], "y": v.p(36, 25)[1], "t": "north-west Arabia", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    tl, ax = timeline(-800, 500, [(-800, "800 BCE"), (-500, "500"), (-200, "200"), (100, "100 CE"), (400, "400")], "Thamud, attested", y=980)
    tl["els"] += event(ax, -715, "Sargon II lists the Tamudi", row=0, c=AMBER, i=.3) + event(ax, -150, "Greek geographers place them here", row=1, c=SCAN, i=.6) + \
                 event(ax, 166, "their temple at Ruwafa", row=2, c=GOLD, i=.9, sub="a Greek and Nabataean bilingual") + event(ax, 400, "horsemen in Roman service", row=0, c=BONE, i=1.2)
    s2 = tl
    s3 = quote("The Thamud of Robathu built this temple for the emperors Marcus Aurelius and Lucius Verus.", "the Ruwafa inscription · 160s CE, in two languages", y=720, size=42)
    s4 = like(s0, cam=[1.18, 500, 960], add=[{"k": "label", "x": 500, "y": 520, "t": "the facades: Nabataean tombs, c. 1 BCE to 75 CE", "c": "#ffb09a", "in": .4, "size": 26},
                                            {"k": "label", "x": 500, "y": 1320, "t": "a Thamudic phase at Hegra itself: still to be shown", "st": "small", "in": 1.0}])
    s5 = like(s1, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:AL-HIJR][sfx:boom][act:awed, setting the scene]Houses@noun carved into ^mountains. [act:respectful, measured]The Quran remembers the people who made them: ^*Thamud*.",
                      "[d:tension][cam:1.12|0|0][act:sincere, simply asked][tune:rise]Were they ^real?"], cut=False),
        B("world", 1, ["[d:calm][k:NORTH-WEST ARABIA][act:confident, warm]^Few ancient Arabian peoples are ^better documented.",
                       "[d:list][go:2|0][act:citing the witnesses, one by one][tune:level]An ^Assyrian king lists them around seven hundred and ^fifteen BCE. [act:the second witness][tune:level]^Greek geographers place them ^here. [sfx:shimmer][act:the third, landing it]Their horsemen served ^Rome around four hundred CE."]),
        B("collision", 3, ["[d:build][k:IN TWO LANGUAGES][act:the find, quietly thrilled]At Ruwafa, in the {160s|one sixties} CE, an ^inscription in Greek and Nabataean records@verb a ^temple. [act:reading the dedication, slower]Built by the ^Thamud, for the ^emperors."]),
        B("cost", 4, ["[d:build][k:HEGRA][act:turning to it, plain]Now the carved facades at ^Hegra. [act:precise, even]They are ^tombs, cut by the ^Nabataeans between about one BCE and ^seventy-five CE.",
                      "[d:aside][act:careful, fair]Thamud were ^here, in this region. [act:precise, gently][tune:fall]Whether these ^particular facades were theirs is a ^narrower question."]),
        B("reversal", 1, ["[d:reveal][k:THE TWIST][act:counting them, building][tune:fall]The ^region, the ^people, the ^dates: [sfx:hit]the ground and the text ^agree, exactly where the text places them."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Thamud, a ^real people of north-west Arabia? [act:the verdict, confident][tune:fall]^*Established*. [act:turning, careful][tune:rise]Hegra's facades as their ^houses@noun? [act:honest, even][tune:fallrise]Still ^open.",
                     "[d:tension][p:0.93][act:the last word, a warm smile]Sometimes the mountain keeps the ^receipt."]),
    ]
    return EP("thamud", "09.07", "Thamud, Salih and the Houses Carved in Mountains", "thamud-hegra", "solid", "Were Thamud a real people, and are Hegra's facades theirs?", "Houses carved into *mountains*.", beats, shots,
              "Annals of Sargon II · Ruwafa inscription, Bowersock 1975 · Nehmé (ed.) 2015, Les tombeaux nabatéens de Hégra · Ptolemy, Geography 6.7",
              "The Quran remembers Thamud. Assyrian, Greek and Roman sources, and a temple inscription of the 160s CE, place them exactly where the text does. Hegra's facades are a narrower question.",
              ["#Thamud", "#Hegra", "#Arabia", "#Archaeology", "#History"])


def thamud_m():
    """Thamud as one continuous take (see mural.py): a temple inscription written twice, and a Nabataean tomb inside the land the witnesses give to Thamud."""
    remix, I = _mur()
    ep = thamud()
    TB = lambda w: _at(w, 24, 56)
    ST = "#cdb48a"
    temple = [I.box(250, 600, 500, 28, ST, "#8a6a48", 2, 2, TB(2), fx="pop")] + \
             [I.box(275 + 105 * j, 440, 40, 160, ST, "#8a6a48", 2, 2, round(TB(2) + .1 * j, 2), fx="rise") for j in range(5)] + \
             [I.box(250, 416, 500, 26, ST, "#8a6a48", 2, 2, TB(3), fx="pop"), {"k": "poly", "p": [[250, 416], [500, 336], [750, 416]], "fill": "#d9c39a", "c": "#8a6a48", "w": 2, "in": TB(3), "fx": "pop"},
              I.label(500, 680, "Ruwafa · 160s CE", TB(6), I.AMBER, 30)]
    slab = [I.box(140, 730, 720, 580, "#d8c39c", "#8a6a48", 2, 10, TB(10), fx="pop"),
            I.label(180, 785, "Greek", TB(15), "#3b2a1c", 28, "start", halo=False),
            {"k": "glyphs", "x": 180, "y": 810, "w": 640, "h": 175, "rows": 5, "cols": 9, "kind": "latin", "c": "#3b2a1c", "in": TB(16)},
            I.label(180, 1045, "Nabataean", TB(20), "#3b2a1c", 28, "start", halo=False),
            {"k": "glyphs", "x": 180, "y": 1070, "w": 640, "h": 175, "rows": 5, "cols": 9, "kind": "hieratic", "c": "#3b2a1c", "in": TB(21)},
            {"k": "hl", "x": 390, "y": 842, "w": 160, "h": 36, "in": TB(31)}, {"k": "hl", "x": 540, "y": 1102, "w": 160, "h": 36, "in": TB(31.5)},
            I.label(500, 1370, "built by the Thamud", TB(32), I.AU, 32)]
    insc = {"base": "dark", "cam": [1, 500, 860], "els": temple + slab}
    FC = lambda w: _at(w, 36, 58)
    cliff = [{"k": "poly", "p": [[100, 1180], [120, 720], [210, 540], [360, 460], [600, 445], [780, 500], [880, 660], [900, 1180]], "fill": "#b8865a", "c": "#e8c39a", "w": 1.5, "curve": True, "in": 0},
             I.line([[100, 1180], [900, 1180]], 0, "#8a6a48", 3, draw=False)]
    fac = [{"k": "poly", "p": [[330, 1180], [330, 680], [670, 680], [670, 1180]], "fill": "#a8744c", "c": "#f2dcb4", "w": 2.5, "in": FC(2), "fx": "draw", "dur": 1.0},
           {"k": "poly", "p": [[330, 680], [330, 640], [380, 640], [380, 600], [440, 600], [440, 640], [560, 640], [560, 600], [620, 600], [620, 640], [670, 640], [670, 680]],
            "fill": "#a8744c", "c": "#f2dcb4", "w": 2.5, "in": FC(3), "fx": "draw", "dur": .8},
           I.line([[360, 700], [360, 1180]], FC(3), "#f2dcb4", 2), I.line([[640, 700], [640, 1180]], FC(3), "#f2dcb4", 2),
           I.box(450, 960, 100, 220, "#2a1f16", "#f2dcb4", 2, 2, FC(4), fx="pop"), {"k": "poly", "p": [[430, 960], [500, 910], [570, 960]], "fill": "none", "c": "#f2dcb4", "w": 2, "in": FC(5), "fx": "draw", "dur": .5},
           I.person(740, 1180, 54, FC(6)),
           I.label(500, 1265, "Nabataean tomb", FC(10), I.BONE, 30), I.label(500, 1315, "c. 1 BCE to 75 CE", FC(16), "#ffb09a", 30),
           I.box(440, 830, 120, 44, "#d8c9a8", "#f2dcb4", 1.5, 3, FC(24), fx="pop"), {"k": "glyphs", "x": 450, "y": 838, "w": 100, "h": 30, "rows": 2, "cols": 4, "kind": "hieratic", "c": "#3b2a1c", "in": FC(24) + .1},
           I.glow(500, 852, 80, FC(25), .5, "lamp")]
    reg = [I.ring(500, 820, 410, FC(36), I.AMBER, 3, "inferred", 1.4), I.label(500, 385, "Thamud's region", FC(38), I.AMBER, 32)] + I.question(780, 800, FC(48), 90)
    facade = {"base": "dark", "cam": [1, 500, 860], "els": cliff + fac + reg}
    cliff0 = _quiet_iso(ep["shots"][0], drop=("carved into the sandstone outcrops",))
    return remix(ep, scenes={0: cliff0, 3: insc, 4: facade}, alias={5: 1}, cams={5: [1.15, 500, 880]})

# ---------------------------------------------------------------- 09.08 Sodom and the People of Lut
def sodom():
    v = View(34.6, 36.4, 30.6, 32.3, (40, 330, 920, 900))
    sea = [(35.55, 31.78), (35.62, 31.6), (35.58, 31.4), (35.5, 31.28), (35.42, 31.2), (35.39, 31.05), (35.45, 31.0), (35.5, 31.12), (35.53, 31.3), (35.48, 31.48), (35.45, 31.7), (35.5, 31.78)]
    base = mapshot(v, extra=[{"k": "poly", "p": [v.p(*q) for q in sea], "fill": "rgba(63,134,176,.55)", "c": SCAN, "w": 1.4, "curve": True, "id": "sea"},
                             {"k": "label", "x": v.p(35.85, 31.45)[0], "y": v.p(35.85, 31.45)[1], "t": "Dead Sea · 430 m below sea level", "st": "small", "c": "#cfe6ff"}])
    s0 = like(base, cam=[1.2, 500, 860], add=[{"k": "pin", "x": v.p(35.67, 31.84)[0], "y": v.p(35.67, 31.84)[1], "t": "Tall el-Hammam", "c": GOLD, "in": .3},
                                              {"k": "pin", "x": v.p(35.53, 31.25)[0], "y": v.p(35.53, 31.25)[1], "t": "Bab edh-Dhra", "c": AMBER, "a": "start", "in": .6},
                                              {"k": "pin", "x": v.p(35.39, 31.08)[0], "y": v.p(35.39, 31.08)[1], "t": "Mount Sodom · the salt ridge", "c": BONE, "a": "end", "lx": -18, "in": .9},
                                              {"k": "scale", "x": 80, "y": 1240, "w": v.km(20), "t": "20 km"}])
    # the rift: a section with faults, bitumen and salt
    sec = {"base": "section", "tod": "night", "ground": 760, "lx": 130, "layers": [{"d": 0, "c": "#6f5a43", "t": "the rift floor"}, {"d": 200, "c": "#4b3c2f", "t": "salt and marl", "tex": "blocks", "to": .1}],
           "cam": [1, 500, 900], "els": [{"k": "line", "p": [[250, 760], [230, 1400]], "c": RED, "w": 2.2, "style": "inferred", "in": .3}, {"k": "line", "p": [[760, 760], [790, 1400]], "c": RED, "w": 2.2, "style": "inferred", "in": .5},
                                            {"k": "water", "y": 760, "h": 60, "x0": 280, "x1": 740, "op": .8, "in": .1},
                                            {"k": "label", "x": 500, "y": 700, "t": "an active rift: faults, earthquakes, bitumen, sulphur, salt", "c": "#ffb09a", "in": .8},
                                            {"k": "label", "x": 240, "y": 1200, "t": "fault", "st": "small", "c": RED, "a": "end", "in": .4}, {"k": "label", "x": 800, "y": 1200, "t": "fault", "st": "small", "c": RED, "a": "start", "in": .6}]}
    s1 = sec
    s2 = {"base": "sky", "tod": "night", "ground": 1100, "sun": False, "cam": [1.1, 500, 900], "els": [{"k": "house", "x": 300, "y": 1100, "w": 100, "h": 50, "in": .1}, {"k": "house", "x": 470, "y": 1110, "w": 140, "h": 60, "fill": "#9a7b58", "in": .2}, {"k": "house", "x": 660, "y": 1100, "w": 90, "h": 46, "in": .3},
          {"k": "rays", "x0": 200, "x1": 800, "y0": 300, "y1": 1080, "n": 40, "spread": .25, "in": .8, "fx": "draw", "dur": 1.6},
          {"k": "glow", "x": 500, "y": 620, "r": 200, "kind": "red", "pulse": True, "in": .8},
          {"k": "cap", "x": 500, "y": 400, "t": "the claim · an airburst, c. 1650 BCE", "in": .2}]}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 200, "y": 560, "w": 600, "h": 560, "fill": "#e9dcc4", "c": "#fff6e6", "sw": 2, "in": .1},
          {"k": "glyphs", "x": 240, "y": 620, "w": 520, "h": 400, "rows": 10, "cols": 14, "kind": "latin", "c": "#3a2c1e", "in": .3},
          {"k": "cap", "x": 500, "y": 480, "t": "Scientific Reports · the paper", "in": .2},
          {"k": "label", "x": 500, "y": 1200, "t": "independent analysis: no mineralogical or geochemical signs of impact", "st": "small", "in": 1.0}]}
    tl, ax = timeline(-3200, -1200, [(-3200, "3200 BCE"), (-2800, "2800"), (-2400, "2400"), (-2000, "2000"), (-1600, "1600")], "The towns that ended", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-3000), "x1": ax.x(-2350), "y": 720, "h": 18, "c": AMBER, "t": "Bab edh-Dhra · 20,000 shaft tombs", "in": .3},
                  {"k": "band", "x0": ax.x(-2600), "x1": ax.x(-2400), "y": 640, "h": 18, "c": RED, "t": "Numeira · ended in fire", "in": .6},
                  {"k": "line", "p": [[ax.x(-1650), 820], [ax.x(-1650), 540]], "c": GOLD, "w": 2.2, "in": .9},
                  {"k": "label", "x": ax.x(-1650) - 10, "y": 520, "t": "Tall el-Hammam destroyed · c. 1650", "c": GOLD, "st": "small", "a": "end", "in": 1.1}]
    s4 = tl
    s5 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE DEAD SEA][sfx:boom][act:respectful, measured, grave]Genesis and the Quran ^both remember towns near this lake, overturned by ^fire and stones from the sky.",
                      "[d:tension][cam:1.12|0|0][act:the hook, a hint of caution]In {2021|twenty twenty-one}, a paper said it had found the ^*cause*."], cut=False),
        B("world", 1, ["[d:calm][k:THE RIFT][act:setting the scene, a sense of depth]This is the ^lowest place on Earth's land: four hundred and thirty metres below the sea, in an ^active rift.",
                       "[d:list][go:2|0][act:naming the hazards, one by one][tune:level]^Earthquakes. [act:same rhythm][tune:level]Burning ^bitumen. [act:keep going][tune:level]^Sulphur. [act:a vivid one, slightly slower][tune:level]A ridge of ^salt called Mount Sodom. [sfx:shimmer][act:the one that matters, grave]And ^real Bronze Age towns that were ^destroyed."]),
        B("collision", 2, ["[d:build][k:THE CLAIM][act:reporting the claim, even-handed]The paper: a ^comet exploded over Tall el-Hammam around {1650|sixteen fifty} BCE, like Tunguska, and burned the city in an ^instant."]),
        B("cost", 3, ["[d:build][k:THE TEST][act:plain, methodical]Other scientists ^checked the minerals. [act:ticking off the findings][tune:level]No ^shock. [act:same, dry][tune:level]No ^impact chemistry. [act:matter of fact][tune:fall]^Image problems were flagged. [stamp:RETRACTED · 2025|red][gap:0.45][act:the journal's verdict, calm]The journal ^retracted the paper in {2025|twenty twenty-five}.",
                      "[d:aside][act:fair, even-handed]^Eleven of its authors ^disagreed. [act:a light reservation][tune:fallrise]So it isn't ^quite dead. [act:precise, calm]It's ^unsupported."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, genuinely asking][tune:fall]And which ^town was Sodom? [act:laying out the options][tune:level]Bab edh-Dhra in the ^south ended around {2350|^twenty-three fifty} BCE. [act:the contrast, clear]Tall el-Hammam in the ^north, a ^thousand years later. [sfx:hit][act:quiet, respectful, plain]The texts give ^no date to check."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:grave, calm authority]Real ^towns, really ^destroyed. [act:weighing it, even][tune:rise]The ^airburst? [act:the verdict, level-headed][tune:fall]^*Awaiting* evidence. [act:one more, brisk][tune:rise]Which ^town? [act:honest, simple][tune:fall]^Open.",
                     "[d:tension][p:0.93][act:sincere, clear about limits]We rate a ^paper and a ^layer. [act:respectful, with care]The account ^itself is not ^ours to grade."]),
    ]
    return EP("sodom", "09.08", "Sodom, the People of Lut, and a Comet Paper That Fell", "sodom", "unsupported", "Did an airburst destroy a real Sodom?", "It had found the *cause*.", beats, shots,
              "Bunch et al. 2021, Scientific Reports (retracted 2025) · Jaret & Harris 2022 · Rast & Schaub 2003 · Neev & Emery 1995",
              "Bronze Age towns by the Dead Sea really ended in fire. A 2021 paper blamed a comet airburst and was retracted in 2025. What is open, and what is not rated.",
              ["#Sodom", "#DeadSea", "#Archaeology", "#Science", "#History"])


def sodom_m():
    """Sodom as one continuous take (see mural.py): the rift's hazards drawn one by one, the claimed airburst over them, and the checks that found no impact."""
    remix, I = _mur()
    ep = sodom()
    HZ = lambda w: _at(w, 18, 41)
    GY = 1100
    hz = [I.line([[470, GY], [490, 1160], [458, 1220], [492, 1290], [466, 1360]], HZ(2), I.RED, 5, dur=.6),
          I.line([[440, GY - 30], [450, GY - 50]], HZ(2) + .3, I.RED, 3, dur=.2), I.line([[500, GY - 30], [490, GY - 50]], HZ(2) + .3, I.RED, 3, dur=.2),
          I.oval(570, GY + 8, 50, 16, "#14100c", "#3b2a1c", 2, at=HZ(6)), I.glow(570, GY - 20, 90, HZ(7), .8, "red"), I.label(570, 1180, "bitumen", HZ(8), "#ffb09a", 28),
          ] + [I.dot(640 + 14 * (j % 4), GY - 6 - 12 * (j // 4), 6, "#f2e36a", round(HZ(14) + .04 * j, 2)) for j in range(8)] + \
         [I.label(675, 1240, "sulphur", HZ(15), "#f2e36a", 28),
          {"k": "poly", "p": [[720, GY], [760, 980], [810, 925], [870, 950], [930, GY]], "fill": "#e9e4da", "c": "#ffffff", "w": 1.5, "in": HZ(18), "fx": "rise"},
          I.label(830, 890, "Mount Sodom", HZ(19), I.BONE, 28)] + \
         [{"k": "house", "x": x, "y": GY, "w": w, "h": h, "fill": f, "in": round(HZ(26) + .2 * j, 2)} for j, (x, w, h, f) in enumerate(((110, 90, 46, "#8e7152"), (215, 120, 60, "#9a7b58"), (345, 80, 42, "#8e7152")))] + \
         [I.label(250, 1180, "Bronze Age towns", HZ(27), I.BONE, 28), I.glow(250, GY - 30, 160, HZ(30), .35, "red")]
    hazards = {"base": "sky", "tod": "night", "ground": GY, "sun": False, "cam": [1, 500, 860], "els": hz}
    CL = lambda w: _at(w, 22, 44)
    claim = [I.label(500, 330, "the claim: an airburst", CL(4), "#ffb09a", 30),
             I.arrow([[880, 380], [600, 520], [330, 700]], CL(12), "#ffd9a0", 4, "claimed", 1.0, True), I.glow(300, 720, 220, CL(14), .75, "red"),
             {"k": "rays", "x0": 120, "x1": 480, "y0": 740, "y1": 1080, "n": 24, "spread": .25, "in": CL(15), "fx": "draw", "dur": 1.2},
             I.label(300, 560, "no crater", CL(22), "#ffb09a", 28), I.glow(250, GY - 40, 200, CL(44), .7, "red")]
    TS = lambda w: _at(w, 34, 65)
    grain = [I.ring(200, 470, 115, TS(8), "#cbbca8", 4), {"k": "poly", "p": [[140, 450], [175, 400], [240, 405], [270, 460], [235, 530], [165, 525]], "fill": "#d9d2c3", "c": "#f5ecdc", "w": 2, "in": TS(9), "fx": "pop"}] + \
            [I.line([[150, 455 + 20 * j], [260, 418 + 20 * j]], round(TS(15) + .1 * j, 2), "#9fd0ff", 3, "claimed", .3) for j in range(4)] + \
            [I.strike(110, 380, 290, 560, TS(24)), I.strike(290, 380, 110, 560, TS(24) + .1), I.label(200, 640, "no shock", TS(25), I.BONE, 28)]
    chem = [I.line([[420, 560], [420, 390]], TS(18), "#cbbca8", 2, dur=.3), I.line([[420, 560], [600, 560]], TS(18), "#cbbca8", 2, dur=.3),
            I.line([[420, 540], [490, 540], [512, 410], [534, 540], [600, 540]], TS(20), I.RED, 3, "claimed", .6), I.line([[420, 535], [600, 535]], TS(27), I.GREEN, 4, dur=.6),
            I.label(510, 640, "no impact chemistry", TS(28), I.BONE, 28)]
    img = [I.box(720, 400, 160, 130, "#2a2016", "#f5ecdc", 2, 4, TS(32), fx="pop"),
           {"k": "poly", "p": [[735, 515], [780, 450], [815, 490], [845, 440], [868, 515]], "fill": "#6f5a44", "c": "none", "w": 0, "in": TS(32) + .1},
           I.line([[885, 400], [885, 330]], TS(34), "#cbbca8", 3, dur=.3), {"k": "poly", "p": [[885, 330], [928, 345], [885, 362]], "fill": I.RED, "c": "none", "w": 0, "in": TS(34) + .2, "fx": "pop"},
           I.label(800, 640, "image problems", TS(35), I.BONE, 28)]
    paper = [I.box(330, 720, 340, 400, "#e9dcc4", "#fff6e6", 2, 4, TS(37), fx="pop"),
             {"k": "glyphs", "x": 360, "y": 760, "w": 280, "h": 320, "rows": 10, "cols": 8, "kind": "latin", "c": "#3a2c1e", "in": TS(37) + .2}]
    authors = [I.label(500, 1210, "11 authors disagreed", TS(48), "#cbbca8", 28)] + [I.person(180 + 64 * j, 1360, 100, round(TS(49) + .08 * j, 2)) for j in range(11)]
    tests = {"base": "dark", "cam": [1, 500, 860], "els": grain + chem + img + paper + authors}
    return remix(ep, scenes={2: hazards, 3: tests}, alias={5: 0}, cams={5: [1.1, 500, 860]}, beat_adds={2: (claim, None)})

# ---------------------------------------------------------------- 09.09 The Ledger
def _ledger_text():
    v = View(30, 60, 12, 42, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("Babylon", 44.42, 32.54, {"c": GOLD}), ("Uruk", 45.64, 31.32, {"a": "end", "lx": -18}), ("Dead Sea", 35.5, 31.4, {}), ("Cudi Dağı", 42.45, 37.35, {}), ("Hegra", 37.95, 26.79, {}), ("Shisr", 53.66, 18.26, {})], cam=[1.05, 500, 870])
    grp = lambda title, col, items, y0=560: [{"k": "cap", "x": 500, "y": y0 - 80, "t": title, "c": col, "in": .1}] + \
        [{"k": "label", "x": 500, "y": y0 + i * 92, "t": t, "st": "body", "in": .3 + i * .25} for i, t in enumerate(items)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["Thamud, a real people of north-west Arabia", "the tower behind Babel, in Babylon", "towns by the Dead Sea, really destroyed"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible or open", "#f0b06a", ["Gilgamesh as a real king", "real floods behind some flood stories", "a megaflood behind Yu", "which town was Sodom"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting discovery", "#c9c1ee", ["Shisr as Iram of the pillars", "the Tall el-Hammam airburst"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#e98a8a", ["the boat-shaped hill as the Ark"])}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 620, "t": "never rated", "c": GOLD, "in": .1},
          {"k": "title", "y": 760, "t": "What faith holds.", "st": "serif", "in": .4}, {"k": "label", "x": 500, "y": 900, "t": "We weigh layers, dates, mines and skies. Not signs.", "in": .9}]}
    s6 = like(s0, cam=[1.2, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:SCRIPTURE AND STONE · THE LEDGER][sfx:boom][act:inviting, warm and respectful]Eight films where sacred ^texts meet the ^ground. [act:counting them off, brisk]Here's what's ^real, what's ^open... [act:softer, sincere]and what we ^never rate."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, respectful]Thamud were a ^real people, ^exactly where the Quran places them. [act:plain, sure][tune:level]Babel's tower ^stood in Babylon. [act:grave, even]Towns by the Dead Sea ^really ended in fire."]),
        B("collision", 2, ["[d:build][k:OPEN][act:running through them][tune:level]Gilgamesh as a ^king: ^plausible. [act:the same again][tune:level]Real floods behind ^some flood stories: plausible. [act:landing on the last]Yu's ^megaflood, and which town was Sodom: ^open."]),
        B("cost", 3, ["[d:build][k:AWAITING DISCOVERY][act:naming them, even][tune:level]Shisr as ^Iram. [act:the second one][tune:fall]The ^airburst over Tall el-Hammam. [d:aside][act:fair, open-minded]Both could ^still turn up their evidence. [act:plain, quiet][tune:fall]^Neither has."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][act:firm, final][tune:highfall]^One boat-shaped hill. [sfx:hit][act:dry, a small smile]Which the ^older traditions ^never pointed to anyway."]),
        B("tag", 5, ["[d:verdict][k:NEVER RATED][p:0.95][act:respectful, sincere, slow]What ^faith holds. [act:plain, naming our tools][tune:fall]We weigh ^layers, ^dates, ^mines and ^skies. [gap:0.4][act:quiet, with care]Not ^signs.",
                     "[d:tension][p:0.93][go:6|1.2][act:thoughtful, warm]The ground keeps its ^own account. [act:the last word, even-handed, a small smile]So far, it agrees with ^more than the ^sceptics expected."]),
    ]
    return EP("scripture-ledger", "09.09", "Scripture and Stone I · The Ledger", "", "", "Where do sacred texts meet the ground?", "What's real, what's open, what we *never* rate.", beats, shots,
              "Full references for every film in the case files", "Eight films, one ledger: where the ground agrees with the texts, where it is silent, and what the archive never grades.",
              ["#Scripture", "#Archaeology", "#History", "#Bible", "#Quran"])


def ledger():
    """The ledger as one continuous film: eight places where sacred texts meet the ground. Only the ground is weighed; what faith holds is framed in gold and never rated."""
    from cabinet import Cabinet, VCOL, retime, X0, X1
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    C = Cabinet([
        {"name": "Thamud", "model": mdl(thamud())},
        {"name": "Babel", "model": mdl(babel())},
        {"name": "The Dead Sea towns", "model": mdl(sodom(), 2)},
        {"name": "Gilgamesh", "model": mdl(gilgamesh())},
        {"name": "The flood stories", "model": mdl(flood(), 0)},
        {"name": "Yu's flood", "model": mdl(yu())},
        {"name": "Iram", "model": mdl(iram())},
        {"name": "A boat-shaped hill", "model": mdl(ark()), "fh": .42, "fw": .7},
    ])
    C.build()
    TH, BA, SO, GI, FL, YU, IR, AR = range(8)
    G = "#e8c878"
    gold = [{"k": "rect", "x": X0 - 34, "y": round(C.Y0 - 34, 1), "w": X1 - X0 + 68, "h": round(C.Y1 - C.Y0 + 68, 1), "r": 18, "fill": "none", "c": G, "sw": 6, "fx": "draw", "dur": 2.0, "in": .2},
            {"k": "rect", "x": 320, "y": round(C.Y0 - 64, 1), "w": 360, "h": 60, "r": 30, "fill": "#1c140e", "c": G, "sw": 2, "in": 1.4, "fx": "pop"},
            {"k": "label", "x": 500, "y": round(C.Y0 - 23, 1), "t": "NEVER RATED", "st": "small", "c": G, "size": 32, "scl": True, "halo": False, "in": 1.5}]
    s1 = C.step(C.cam_cell(TH), C.verdict(TH, "established", "a real people", .4) + C.people(TH, 3, at=.9))
    s2 = C.step(C.cam_cell(BA), C.verdict(BA, "established", "it stood in Babylon", .3))
    s3 = C.step(C.cam_cell(SO), C.verdict(SO, "established", "towns that ended in fire", .3))
    s4 = C.step(C.cam_cell(GI), C.verdict(GI, "plausible", "a real king", .3))
    s5 = C.step(C.cam_cell(FL), C.verdict(FL, "plausible", "real floods, behind some", .3))
    s6 = C.step(C.cam_cells([SO, YU]), C.verdict(YU, "open", "a megaflood?", .2) + C.verdict(SO, "open", "which town?", .5, frame=False) +
                C.question(YU, dx=C.w * .32, dy=-190, at=.8, size=70) + C.question(SO, dx=C.w * .32, dy=-150, at=1.0, size=70))
    s7 = C.step(C.cam_cell(IR), C.verdict(IR, "awaiting", "Shisr as Iram?", .2))
    s8 = C.step(C.cam_cell(SO), C.verdict(SO, "awaiting", "an airburst?", .2, frame=False))
    s9 = C.step(C.cam_cells([SO, GI, FL, YU, IR, AR]))
    s10 = C.step(C.cam_cells([SO, GI, FL, YU, IR, AR]), [e for k, i in enumerate((SO, IR)) for e in C.wash(i, VCOL["awaiting"], at=.1 + .2 * k, op=.13)])
    s11 = C.step(C.cam_cell(AR), C.verdict(AR, "ruled", at=.1) + C.struck(AR, "the Ark, in this hill", at=.2))
    s12 = C.step(C.cam_cell(AR), C.note(AR, "older traditions point to Mount Cudi", at=.4, c="#f2c98e"))
    s13 = C.step(C.cam_all(k=.9), gold)
    s14 = C.step(C.cam_all(k=.9), [e for i in range(8) for e in C.wash(i, "#cbbca8", at=.1 + .12 * i, op=.08)])
    s15 = C.step(C.cam_all(k=.86, sy=720), [e for k, i in enumerate((TH, BA, SO, GI, FL)) for e in C.wash(i, VCOL["established"], at=.3 + .15 * k, op=.12)])
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5, (0, 2): "%d|1.2" % s6}),
        3: (s7, {(0, 1): "%d|1.1" % s8, (0, 2): "%d|1.1" % s9, (0, 3): "%d|.4" % s10}),
        4: (s11, {(0, 1): "%d|.3" % s12}),
        5: (s13, {(0, 1): "%d|.4" % s14, (1, 0): "%d|3" % s15}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old

def _gold(C, data):
    """What faith holds is framed in gold and never rated: the frame draws itself on the close sentence that says so."""
    from cabinet import X0, X1
    G = "#e8c878"
    k = next((j for j, s in enumerate(data["close"]) if "faith" in s), len(data["close"]) - 1)
    frame = [{"k": "rect", "x": X0 - 34, "y": round(C.Y0 - 34, 1), "w": X1 - X0 + 68, "h": round(C.Y1 - C.Y0 + 68, 1), "r": 18, "fill": "none", "c": G, "sw": 6, "fx": "draw", "dur": 2.0, "in": .2},
             {"k": "rect", "x": 320, "y": round(C.Y0 - 64, 1), "w": 360, "h": 60, "r": 30, "fill": "#1c140e", "c": G, "sw": 2, "in": 1.4, "fx": "pop"},
             {"k": "label", "x": 500, "y": round(C.Y0 - 23, 1), "t": "NEVER RATED", "st": "small", "c": G, "size": 32, "scl": True, "halo": False, "in": 1.5}]
    return {"close": {min(k, 3): frame}}


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/scripture-ledger.json)."""
    import recap
    return recap.recap(ledger, "scripture-ledger", _gold)


def EPISODES():
    return [flood_m(), yu_m(), gilgamesh_m(), ark_m(), babel_m(), iram_m(), thamud_m(), sodom_m(), ledger_recap()]
