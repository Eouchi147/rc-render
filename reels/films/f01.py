"""File 01 · Before Us. The humans before history, and the skills older than we thought."""
import math
from films import like, View, Axis
from scenes import (timeline, event, stat, quote, silhouette, skull, leg_bones, footprints, idol, spear_point, raft,
                    BONE, AMBER, SCAN, OCHRE, GOLD, RED)

SERIES = "Before Us"


def B(role, frm, lines, cut=True):
    return {"role": role, "visual": {"from": frm, "cut": cut} if cut else {"from": frm}, "lines": lines}


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def mapshot(v, pins=(), extra=(), ghost=(), cam=None):
    els = [{"k": "map", "land": v.land(), "ghost": [v.line(g) + "Z" for g in ghost], "in": -1}]
    for i, (name, lon, lat, kw) in enumerate(pins):
        x, y = v.p(lon, lat); e = {"k": "pin", "x": x, "y": y, "t": name, "in": .3 + i * .3}; e.update(kw); els.append(e)
    return {"base": "map", "cam": cam or [1, 500, 860], "els": els + list(extra)}


def lineup(items, y=1080, x0=180, dx=160, i=.2):
    """items: (label, metres). 1.7 m = 300 px."""
    els = []
    for k, (lab, m) in enumerate(items):
        els += silhouette(x0 + k * dx, y, 300 * m / 1.7, t=lab, i=i + k * .15, c="#f2c98e" if lab.startswith("us") else "#c9b49a")
    els.append({"k": "line", "p": [[x0 - 90, y], [x0 + dx * (len(items) - 1) + 90, y]], "c": "#8c7152", "w": 2})
    return els


# ---------------------------------------------------------------- 01.02 The Other Humans
def other_humans():
    crowd = lineup([("Neanderthal", 1.65), ("Denisovan", 1.8), ("Flores", 1.1), ("Luzon", 1.3), ("us", 1.72)], x0=170, dx=165)
    s0 = {"base": "dark", "cam": [1.22, 500, 930], "els": crowd + [{"k": "cap", "x": 500, "y": 1180, "t": "60,000 years ago · at least five kinds of human", "in": .8}]}
    v = View(-12, 150, -14, 66, (30, 360, 940, 820))
    s1 = mapshot(v, pins=[("Neanderthals", 10, 48, {"c": AMBER}), ("Denisova Cave", 84.7, 51.4, {"c": SCAN, "a": "end", "lx": -18}),
                          ("Flores", 121, -8.7, {"c": OCHRE, "a": "end", "lx": -18}), ("Luzon", 121.4, 17.7, {"c": OCHRE})])
    s1["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "a crowded planet", "in": .2}]
    s2 = {"base": "dark", "floor": 1000, "cam": [1.2, 500, 880], "els": [
        {"k": "poly", "p": [[470, 1000], [530, 1000], [528, 900], [520, 860], [506, 850], [492, 852], [480, 862], [472, 900]], "fill": "#e8dcc6", "c": "#fff6e6", "w": 1.6, "curve": True, "in": .2},
        {"k": "glow", "x": 500, "y": 920, "r": 260, "kind": "lamp", "op": .4},
        {"k": "cap", "x": 500, "y": 560, "t": "a finger bone · Denisova Cave · DNA published 2010", "in": .4},
        {"k": "label", "x": 500, "y": 1080, "t": "a human group known first from its DNA", "in": 1.0}]}
    s3 = stat("6%", "", "of the DNA of some Papuan people comes from Denisovans", "up to · Reich et al. 2010")
    v2 = View(112, 130, -12, 22, (60, 330, 880, 900))
    s4 = mapshot(v2, pins=[("Flores · 'hobbits', c. 1.1 m", 121.0, -8.6, {"c": OCHRE, "a": "end", "lx": -18}), ("Luzon · Homo luzonensis", 121.4, 17.6, {"c": OCHRE, "a": "end", "lx": -18})])
    s5 = {"base": "dark", "cam": [1.5, 500, 930], "els": lineup([("Flores", 1.1), ("us", 1.72)], x0=380, dx=240) + [{"k": "cap", "x": 500, "y": 560, "t": "island people, isolated for many thousands of years", "in": .4}]}
    s6 = {"base": "dark", "floor": 1000, "cam": [1.05, 500, 880], "els": skull(500, 900, 2.1, robust=True) + [
        {"k": "glow", "x": 500, "y": 860, "r": 320, "kind": "lamp", "op": .3},
        {"k": "cap", "x": 500, "y": 560, "t": "the Harbin skull · at least 146,000 years old", "in": .4},
        {"k": "label", "x": 500, "y": 1100, "t": "named Denisovan by its proteins and DNA, 2025", "in": 1.0}]}
    s7 = like(s0, cam=[1.3, 500, 930])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE OTHER HUMANS][sfx:boom][act:setting the scene, hushed wonder]Sixty thousand years ago, we weren't ^alone.",
                      "[d:tension][cam:1.12|0|0][act:leaning in, the number matters]There were at least ^*four* other kinds of human on Earth."], cut=False),
        B("world", 1, ["[d:calm][k:NEANDERTHALS][act:plain storytelling, introducing them]In Europe and western Asia: the ^Neanderthals. [act:warm, admiring][tune:level]^Strong, ^clever... [act:the surprise, softer, closer][tune:fall]and still ^*inside* us.",
                       "[d:list][act:explaining, friendly and clear]If your family comes from outside ^Africa, around ^two percent of your DNA is Neanderthal."]),
        B("collision", 2, ["[d:build][k:2010 · DENISOVA CAVE][act:building, a detective story]Then, a single ^finger bone from a cave in Siberia gave up its ^DNA. [sfx:hit][act:the reveal, slow and clear]A human group ^nobody had ever seen: the ^Denisovans.",
                           "[d:list][go:3|0][act:topping the last number, brighter]In some people in Papua New Guinea, up to ^*six* percent of their DNA is Denisovan."]),
        B("cost", 4, ["[d:build][k:THE ISLANDS][act:gentle wonder, unhurried]On the island of Flores lived people about ^one metre tall. [go:5|0][act:adding another, a touch lighter]On ^Luzon, in the Philippines, ^another kind again."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:the reveal, slower, delighted]And in {2025|twenty twenty-five}, ancient ^proteins finally gave the Denisovans a ^*face*.",
                          "[d:reveal][sfx:shimmer][act:vivid, showing it off]A ^massive skull from ^Harbin, in China. [act:the odd detail, a small smile]Hidden down a ^well for over ^eighty years."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:calm authority, warm][tune:fall]Humanity was a ^crowd. [act:quiet, a little wistful][tune:fall]We're simply the ^last ones ^*standing*.",
                     "[d:tension][p:0.93][act:inviting, a gentle question][tune:rise]And the ^others? [gap:0.4][act:quiet, certain, the last word][tune:fall]They're still in our ^*blood*."]),
    ]
    return EP("other-humans", "01.02", "The Other Humans", "other-humans", "strong", "How many kinds of human shared the Earth with us?", "We were never *alone*.",
              beats, shots, "Reich et al. 2010, Nature · Green et al. 2010, Science · Brown et al. 2004, Nature · Détroit et al. 2019, Nature · Fu et al. 2025, Science",
              "Neanderthals, Denisovans, the 'hobbits' of Flores and the people of Luzon: humanity was a crowd, and the others are still in our DNA.",
              ["#HumanEvolution", "#Neanderthals", "#Denisovans", "#Science", "#History"])


def _mur():
    from mural import remix
    import illus
    return remix, illus


def _grid(I, x0, y0, n=100, cols=10, cell=26, step=30, at=0, c="#cbbca8", op=.35, dt=.006):
    """A hundred squares: a whole, split into equal parts."""
    return [I.box(x0 + step * (k % cols), y0 + step * (k // cols), cell, cell, c, r=4, at=round(at + dt * k, 3), op=op) for k in range(n)]


def _cell(I, x0, y0, k, c, at, cols=10, cell=26, step=30):
    return I.box(x0 + step * (k % cols), y0 + step * (k // cols), cell, cell, c, r=4, at=at, fx="pop")


def other_humans_m():
    """The other humans as one continuous take (see mural.py): a crowd of five, DNA as a hundred parts, a new branch, a face from proteins."""
    remix, I = _mur()
    ep = other_humans()
    NEA, DEN, FLO = "#e8b87a", "#9fd0ff", "#ff9a80"
    # 0 · the crowd: we stand alone, then four others join us; at the verdict they fade, two of them leave threads in us
    X = [190, 345, 500, 655, 810]; GY = 1080
    who = [("Neanderthal", 1.65), ("Denisovan", 1.8), ("Flores", 1.1), ("Luzon", 1.3), ("us", 1.72)]
    H = [300 * m / 1.7 for _, m in who]
    crowd = [I.line([[100, GY], [900, GY]], 0, "#8c7152", 2, draw=False), I.glow(X[4], GY - 150, 190, .3, .35), I.person(X[4], GY, H[4], .3, "#f2c98e"),
             I.label(X[4], GY + 44, "us", .5, "#f2c98e", 30)]
    for k in range(4):
        at = 3.8 + .4 * k
        crowd += [I.person(X[k], GY, H[k], at, "#c9b49a"), I.label(X[k], GY + 44, who[k][0], at + .2, "#cbbca8", 28)]
    s0 = {"base": "dark", "cam": [1.12, 500, 930], "els": crowd}
    # 1 · the map: the Neanderthals' range; out of Africa, and two parts in a hundred
    v = View(-12, 150, -14, 66, (30, 360, 940, 820))
    nx, ny = v.p(25, 47)
    rng = [I.oval(nx, ny, 200, 70, "rgba(232,184,122,.16)", NEA, 2.5, 1, 3.4, style="inferred"), I.glow(nx, ny, 160, 3.5, .35)]
    gx, gy = 352, 1090
    out = [I.arrow([v.p(38, 4), v.p(40, 22), v.p(36, 33)], 4.5, "#f2c98e", 3, "inferred", 1.0),
           I.arrow([v.p(36, 33), v.p(25, 40), v.p(12, 45)], 5.0, "#f2c98e", 3, "inferred", .8),
           I.arrow([v.p(36, 33), v.p(60, 38), v.p(85, 36)], 5.1, "#f2c98e", 3, "inferred", .8)] + \
          _grid(I, gx, gy, at=2.5) + [_cell(I, gx, gy, k, NEA, 5.5 + .2 * j) for j, k in enumerate((98, 99))] + \
          [I.glow(gx + 30 * 8.9, gy + 30 * 9.4, 70, 5.6, .7), I.label(gx + 330, gy + 290, "2 in 100", 5.9, NEA, 32, "start")]
    # 2 · a finger bone in a cave gives up its DNA; three copies compared letter by letter; a new branch on the family tree
    bone = {"k": "poly", "p": [[488, 712], [512, 712], [511, 662], [506, 644], [500, 640], [494, 642], [489, 662]], "fill": "#efe6d2", "c": "#fff6e6", "w": 1.6, "curve": True, "in": 1.3, "fx": "pop"}
    cave = [{"k": "poly", "p": [[40, 790], [110, 560], [260, 430], [420, 380], [600, 390], [760, 450], [890, 570], [960, 790]], "fill": "#4a3a2c", "c": "#8a6a48", "w": 3, "curve": True, "in": .1},
            {"k": "poly", "p": [[290, 790], [320, 640], [410, 560], [500, 540], [590, 560], [680, 640], [710, 790]], "fill": "#0d0a08", "c": "#2a1f16", "w": 2, "curve": True, "in": .1},
            I.line([[40, 790], [960, 790]], .1, "#8a6a48", 3, draw=False), I.glow(500, 670, 170, 1.3, .55), bone]
    helix = [I.line([[500 + round(26 * math.sin(k * .7 + ph), 1), 722 + 10 * k] for k in range(16)], 3.0, DEN, 3, dur=1.0, curve=True) for ph in (0, math.pi)]
    BASES = ["#e8b87a", "#9fd0ff", "#8fd9b0", "#c9c1ee"]
    seq = [(k * 7 + 3) % 4 for k in range(20)]
    rows = []
    for r, (lab, diff, c) in enumerate((("us", (), "#f2c98e"), ("Neanderthal", (5, 14), NEA), ("the bone", (2, 5, 9, 14, 17), DEN))):
        y = 930 + 66 * r; at = 4.6 + .4 * r
        rows.append(I.label(285, y + 12, lab, at, c, 28, "end"))
        for k in range(20):
            b = (seq[k] + 1) % 4 if k in diff else seq[k]
            rows.append(I.box(305 + 30 * k, y - 18, 24, 36, BASES[b], r=3, at=round(at + .02 * k, 2), op=.9))
        for k in diff:
            rows.append(I.ring(317 + 30 * k, y, 24, 7.0 + .3 * r, "#ff8a7a", 2.5, dur=.4))
    tree = [I.line([[500, 1420], [500, 1350]], 8.2, BONE, 5, dur=.5), I.line([[500, 1350], [280, 1210]], 8.5, "#f2c98e", 5, dur=.6),
            I.line([[500, 1350], [640, 1280]], 8.5, BONE, 5, dur=.5), I.line([[640, 1280], [560, 1210]], 8.8, NEA, 5, dur=.5),
            I.dot(280, 1210, 10, "#f2c98e", 8.9), I.label(280, 1178, "us", 8.9, "#f2c98e", 28), I.dot(560, 1210, 10, NEA, 9.1), I.label(560, 1178, "Neanderthal", 9.1, NEA, 28),
            I.line([[640, 1280], [790, 1210]], 9.7, DEN, 6, dur=.8), I.glow(790, 1205, 110, 10.3, .7), I.dot(790, 1210, 12, DEN, 10.3),
            I.label(800, 1178, "Denisovan", 10.8, DEN, 30)]
    finger = {"base": "dark", "cam": [1, 500, 900], "els": cave + helix + rows + tree}
    # 3 · up to six parts in a hundred: three times the Neanderthal share
    hx, hy, G = 400, 600, dict(cell=34, step=39)
    share = {"base": "dark", "floor": 1150, "cam": [1.05, 500, 900], "els": [I.person(210, 1150, 330, .2, "#e8d6b8"), I.glow(210, 990, 200, .3, .45),
             I.label(210, 1215, "Papua New Guinea", 3.2, BONE, 28)] + _grid(I, hx, hy, at=.6, **G) +
             [_cell(I, hx, hy, k, NEA, 7.9 + .2 * j, **G) for j, k in enumerate((90, 91))] +
             [_cell(I, hx, hy, k, DEN, 4.8 + .2 * j, **G) for j, k in enumerate((94, 95, 96, 97, 98, 99))] +
             [I.label(595, 1060, "6 Denisovan", 6.2, DEN, 32), I.label(595, 1110, "2 Neanderthal", 8.3, NEA, 30)] +
             [I.box(hx - 5 + 39 * c0, hy + 9 * 39 - 5, 83, 44, "none", NEA if c0 == 0 else DEN, 3, 9, (8.1 if c0 == 0 else 6.7 + .3 * j), style="inferred") for j, c0 in enumerate((0, 4, 6, 8))] +
             [I.label(hx + 390 + 14, hy + 9 * 39 + 30, "×3", 8.5, DEN, 40, "start", st="serif")]}
    # 4 · the islands: a road east
    v4 = View(112, 130, -12, 22, (60, 330, 880, 900))
    isl = [I.arrow([[40, v4.p(112, 2)[1]], v4.p(116, 0), v4.p(119, -6)], .4, "#f2c98e", 3, "inferred", 1.2),
           I.glow(*v4.p(121.0, -8.6), 90, 2.7, .7), I.ring(*v4.p(121.0, -8.6), 46, 2.7, FLO, 3), I.glow(*v4.p(121.4, 17.6), 90, 3.4, .7), I.ring(*v4.p(121.4, 17.6), 46, 3.4, FLO, 3)]
    # 5 · Flores: one metre tall, a five-year-old's height; the sea keeps them apart
    FY = 1150; M = 380 / 1.7
    flores = {"base": "dark", "cam": [1.1, 500, 1010], "els": [
        {"k": "water", "y": FY - 6, "x0": -100, "x1": 596, "h": 700, "op": .85, "in": 3.5},
        I.oval(290, FY + 4, 210, 36, "#b89a6a", "#e8cfa0", 2, 1, .1), I.box(600, FY - 4, 420, 720, "#3a2c20", "#8a6a48", 2, 4, at=.1),
        I.glow(290, FY - 120, 160, .3, .4), I.person(290, FY, 1.1 * M, .3, "#c9b49a"), I.label(290, FY - 1.1 * M - 28, "1.1 m", 1.4, FLO, 32),
        I.label(290, FY + 118, "Flores", .6, FLO, 30),
        I.person(700, FY, 1.72 * M, 2.0, "#f2c98e"), I.label(700, FY - 1.72 * M - 28, "1.7 m", 2.2, "#f2c98e", 32),
        I.person(845, FY, 1.1 * M, 2.6, "#e8d6b8"), I.label(845, FY - 1.1 * M - 28, "age 5", 2.8, BONE, 30),
        I.label(770, FY + 70, "today", 3.0, BONE, 30),
        I.oval(290, FY - 10, 262, 66, "none", DEN, 3, 1, 4.4, style="inferred", fx="draw", dur=1.2)]}
    # 6 · a face from proteins: two bead chains match; the skull spent eighty years down a well
    PAL = [NEA, DEN, I.GREEN, I.LILAC, "#e8dcc6"]
    order = [0, 2, 1, 3, 4, 1, 0, 2, 4, 3, 1, 2]
    chains = []
    for r, (lab, y, at) in enumerate((("skull", 990, 5.4), ("Denisovan", 1090, 8.4))):
        chains += [I.line([[250, y], [778, y]], at, "#8a7a66", 3, dur=.6), I.label(222, y + 10, lab, at, PAL[1] if r else "#efe6d2", 28, "end")]
        chains += [I.dot(250 + 48 * k, y, 17, PAL[order[k]], round(at + .06 * k, 2)) for k in range(12)]
    chains += [I.line([[250 + 48 * k, 1010], [250 + 48 * k, 1070]], round(10.1 + .04 * k, 2), I.GREEN, 3, dur=.3) for k in range(12)]
    chains += [I.glow(514, 1040, 260, 10.6, .35)]
    harbin = {"base": "dark", "cam": [1.05, 500, 920], "els": [I.glow(500, 740, 300, 1.2, .35)] + skull(500, 780, 1.6, robust=True, i=1.2) + chains}
    well = [I.line([[560, 1220], [920, 1220]], 5.0, "#8a6a48", 3, draw=False),
            I.box(626, 1220, 18, 190, "#6b5a48", r=2, at=5.2, fx="fill"), I.box(806, 1220, 18, 190, "#6b5a48", r=2, at=5.2, fx="fill"),
            I.box(644, 1220, 162, 190, "#0d0a08", r=0, at=5.2, op=.9)] + skull(728, 1392, .27, robust=True, i=5.8) + \
           [I.label(500, 925, "Harbin · 146,000+ years", 1.2, AMBER, 30), I.label(610, 1300, "down a well", 6.0, BONE, 28, "end"),
            I.label(610, 1350, "80+ years", 6.9, AMBER, 30, "end")]
    # 7 · the verdict on the crowd: four fade, the last one standing; two leave threads in us
    fade = [I.glow(500, 900, 420, .2, .25)] + [I.person(X[k], GY, H[k], 4.6 + .2 * k, "#3e3329") for k in range(4)]
    threads = [I.line([[X[0], GY - H[0] * .55], [(X[0] + X[4]) / 2, GY - 420], [X[4] - 6, GY - H[4] * .55]], 2.4, NEA, 4, dur=1.4, curve=True),
               I.line([[X[1], GY - H[1] * .55], [(X[1] + X[4]) / 2, GY - 380], [X[4] - 6, GY - H[4] * .5]], 2.7, DEN, 4, dur=1.4, curve=True),
               I.glow(X[4], GY - 160, 200, 3.6, .7)]
    return remix(ep, scenes={0: s0, 2: finger, 3: share, 5: flores, 6: harbin}, alias={7: 0},
                 cams={7: [1.12, 500, 930]}, adds={1: rng, 4: isl},
                 beat_adds={5: (fade, None)}, line_adds={(1, 1): (out, [1, 500, 940]), (4, 1): (well, [1, 500, 960]), (5, 1): (threads, None)})


# ---------------------------------------------------------------- 01.03 The First Sailors
SUNDA = [(95, 6), (98, 12), (103, 14), (107, 17), (109, 20), (112, 21.5), (114, 17), (116.5, 12), (118, 9), (118.3, 5.5), (118.6, 1), (117.3, -2.5), (116.2, -5), (115.7, -8.9),
         (114, -9.2), (110, -8.9), (105, -7.3), (101, -5), (97, -1), (94, 3)]


def early_seafarers():
    v = View(104, 128, -12, 20, (40, 330, 920, 900))
    wl = [v.p(115.75, -9.5), v.p(116.4, -5), v.p(118.4, -2), v.p(118.6, 3), v.p(120.2, 7), v.p(122, 11), v.p(124.5, 19)]
    base = mapshot(v, ghost=[SUNDA])
    base["els"] += [{"k": "label", "x": v.p(108, 2)[0], "y": v.p(108, 2)[1], "t": "Ice Age land: Sundaland", "st": "ital", "c": "#c9ad85"}]
    s0 = like(base, cam=[1.35, v.p(120, -4)[0], v.p(120, -4)[1]], add=[{"k": "line", "p": wl, "c": SCAN, "w": 2.4, "style": "inferred", "in": .3, "fx": "draw"}] + raft(v.p(117, -8.4)[0], v.p(117, -8.4)[1], 70, .6))
    s1 = like(base, add=[{"k": "line", "p": wl, "c": SCAN, "w": 2.4, "style": "inferred", "in": .2, "fx": "draw"},
                         {"k": "label", "x": v.p(119.6, 14)[0] + 20, "y": v.p(119.6, 14)[1], "t": "deep water, never dry", "st": "small", "c": "#cfe6ff", "a": "start", "in": .8}])
    pins = [("Flores · 1.02 million yrs", 121, -8.6, {"c": OCHRE, "a": "end", "lx": -18}), ("Sulawesi · 1.04 million+", 120.2, -3.5, {"c": OCHRE}),
            ("Luzon · c. 709,000", 121.4, 17.6, {"c": OCHRE, "a": "end", "lx": -18})]
    s2 = like(s1, add=[e for i, (n, lo, la, kw) in enumerate(pins) for e in [dict({"k": "pin", "x": v.p(lo, la)[0], "y": v.p(lo, la)[1], "t": n, "in": .3 + i * .4}, **kw)]])
    gy = 760; px = 2.2                                           # sea section: 2.2 px per metre of depth
    sec = {"base": "dark", "cam": [1, 500, 860], "els": [
        {"k": "poly", "p": [[-100, gy], [260, gy], [330, gy + 250 * px], [670, gy + 250 * px], [740, gy], [1100, gy], [1100, 1500], [-100, 1500]], "fill": "#4e3e30", "c": "#c9ad85", "w": 2},
        {"k": "water", "y": gy - 120 * px, "h": 120 * px + 250 * px, "x0": 260, "x1": 740, "op": .75},
        {"k": "line", "p": [[-100, gy - 120 * px], [1100, gy - 120 * px]], "c": SCAN, "w": 1.6, "style": "inferred"},
        {"k": "label", "x": 90, "y": gy - 120 * px - 16, "t": "today's sea level", "st": "small", "a": "start", "c": "#cfe6ff"},
        {"k": "label", "x": 90, "y": gy - 16, "t": "Ice Age sea level, 120 m lower", "st": "small", "a": "start", "c": "#cfe6ff"},
        {"k": "dim", "x1": 780, "y1": gy, "x2": 780, "y2": gy + 250 * px, "t": "250 m+", "lx": 30},
        {"k": "label", "x": 500, "y": gy + 250 * px + 60, "t": "the Lombok Strait never dried", "c": GOLD, "in": .6},
        {"k": "cap", "x": 500, "y": 400, "t": "Bali · Lombok · the deep channel", "in": .2}]}
    from iso3d import strait_block, lab as _lab
    L_ = lambda x, y, t, c=None, z=0, **k: dict(_lab(x, y, t, c, z=z), st="lab", **k)
    s3 = {"base": "dark", "stars": 40, "cam": [1, 500, 880], "els": [{"k": "glow", "x": 500, "y": 900, "r": 480, "kind": "lamp", "op": .14},
          {"k": "iso", "x": 500, "y": 900, "s": 5.4, "az": -24, "spin": 1.8, "el": .38, "items": strait_block() + [
              L_(-44, 16, "Bali"), L_(44, 16, "Lombok"), L_(0, 13, "today's sea level", "#cfe6ff", z=30),
              L_(0, 1, "Ice Age sea, 120 m lower", "#cfe6ff", z=30, dy=40), L_(0, -24, "250 m+ deep", GOLD, z=30, dy=40)]},
          {"k": "cap", "x": 500, "y": 400, "t": "Bali · Lombok · the deep channel", "in": .2},
          {"k": "label", "x": 500, "y": 1300, "t": "the Lombok Strait never dried", "c": GOLD, "in": .6},
          {"k": "label", "x": 500, "y": 1345, "t": "vertical scale exaggerated", "st": "small", "c": "#b9aa97", "in": .8}]}
    waves = [{"k": "line", "p": [[-200 + j * 60, 900 + (10 if j % 2 else -10)] for j in range(25)], "c": "#6fb6d6", "w": 3, "curve": True, "op": .8}]
    s4 = {"base": "sky", "tod": "dusk", "ground": 900, "groundc": "url(#k-sea)", "ridges": [], "sun": [760, 760, 30], "cam": [1.1, 500, 900],
          "els": waves + raft(460, 930, 170, .2) + [{"k": "person", "x": 450, "y": 922, "h": 60, "t": False, "in": .4}, {"k": "cap", "x": 500, "y": 480, "t": "castaways on a storm-torn mat?", "in": .6}]}
    s5 = like(s2, cam=[1.1, 500, 820], add=[{"k": "arrow", "p": [v.p(114.5, -8.2), v.p(117, -9), v.p(120.2, -8.8)], "curve": True, "c": AMBER, "w": 2.4, "in": .2, "fx": "draw"},
                                            {"k": "arrow", "p": [v.p(117.5, 1), v.p(119.8, -2)], "curve": True, "c": AMBER, "w": 2.4, "in": .5, "fx": "draw"},
                                            {"k": "arrow", "p": [v.p(118.5, 10.5), v.p(120.8, 16.5)], "curve": True, "c": AMBER, "w": 2.4, "in": .8, "fx": "draw"}])
    s6 = like(s4, cam=[1.25, 480, 920])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:WALLACEA][sfx:boom][act:setting the scene, hushed]About a ^million years ago, someone crossed the ^sea.",
                      "[d:tension][cam:1.12|0|0][act:the sting, quiet and certain][tune:fall]And it ^*wasn't* us."], cut=False),
        B("world", 1, ["[d:calm][k:THE ISLANDS][act:naming them, unhurried][tune:level]Flores. [act:same even rhythm][tune:level]Sulawesi. [act:closing the list][tune:fall]Luzon. [act:explaining, clear and even]Islands that were ^never joined to the mainland, even when Ice Age seas fell a hundred and ^twenty metres.",
                       "[d:build][go:2|2][act:the puzzle, leaning in]Yet stone ^tools sit on ^all three. [act:weighty, slower][tune:fall]On Sulawesi, more than a ^*million* years old."]),
        B("collision", 3, ["[d:build][k:THE GAP][act:measured, laying out the facts]Between Bali and Lombok, the channel is over two hundred and fifty metres ^deep. [act:firm, underlining it][tune:fall]Flores was ^always at least nineteen kilometres of open ^water away."]),
        B("cost", 4, ["[d:build][k:ACCIDENT?][act:fair-minded, the mainstream view]Many scientists think storms or tsunamis swept them ^out, on floating ^mats of vegetation.",
                      "[d:list][sfx:shimmer][act:lighter, a touch of fun]The same way ^rats, giant ^tortoises and dwarf ^elephants arrived."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:leaning in, the turn]But it happened ^again. [act:more pointed][tune:fall]And ^again. [act:laying it out, slower]^Three islands, hundreds of kilometres ^apart. [sfx:hit][act:dry, one eyebrow up][tune:risefall]That's a lot@amount of ^*luck*.",
                          "[d:list][act:amused admiration, storytelling]One researcher built bamboo rafts with ^stone tools, just to see if it could be ^done."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:calm authority][tune:fall]The crossings are ^real. [act:weighing both sides, even][tune:fall]^Planned voyages, or lucky ^castaways? [act:honest, level-headed][tune:fall]An ^*open* question.",
                     "[d:tension][p:0.93][act:wonder, quiet, the last word][tune:fall]The first sailors may have been people we'd ^barely ^*recognise*."]),
    ]
    return EP("first-sailors", "01.03", "The First Sailors", "early-seafarers", "contested", "Did human relatives cross the sea on purpose?", "It *wasn't* us.", beats, shots,
              "Brumm et al. 2010, Nature · Hakim et al. 2025, Nature · Ingicco et al. 2018, Nature · Dennell et al. 2014, Quaternary Science Reviews",
              "Stone tools on Flores, Sulawesi and Luzon show human relatives crossed deep water a million years ago. Voyage or accident?",
              ["#HumanEvolution", "#Archaeology", "#Indonesia", "#Philippines", "#History"])


def _mat(I, x, y, w, at, c="#7a6a32"):
    """A floating tangle of uprooted branches."""
    out = []
    for k in range(6):
        a = (k - 2.5) * .12
        out.append(I.line([[x - w / 2, y - 4 + 3 * k + w * .5 * math.sin(a) * .2], [x + w / 2, y + 2 - 2 * k - w * .5 * math.sin(a) * .2]], at, c if k % 2 else "#5a4a22", 7, draw=False))
    out += [I.dot(x - w * .35 + w * .14 * k, y - 8 - 4 * (k % 2), 7, "#5f8a4a", at) for k in range(6)]
    return out


def _animal(I, kind, x, y, at):
    """Side views, facing right, feet on y: a rat, a giant tortoise, a dwarf elephant (schematic)."""
    if kind == "rat":
        return [I.line([[x - 26, y - 10], [x - 50, y - 4], [x - 64, y - 14]], at, "#b0a89c", 3, draw=False, curve=True),
                I.oval(x, y - 14, 28, 13, "#9a948c", at=at), I.oval(x + 28, y - 18, 12, 9, "#9a948c", at=at), I.dot(x + 24, y - 28, 6, "#b9b2a6", at), I.dot(x + 33, y - 20, 2.5, "#1a1511", at)]
    if kind == "tortoise":
        return [I.box(x - 34, y - 14, 12, 14, "#6b5f48", r=4, at=at), I.box(x + 20, y - 14, 12, 14, "#6b5f48", r=4, at=at),
                {"k": "poly", "p": [[x - 48, y - 10], [x - 40, y - 44], [x - 14, y - 62], [x + 14, y - 62], [x + 40, y - 44], [x + 48, y - 10]], "fill": "#8a7650", "c": "#c9b48a", "w": 2, "curve": True, "in": at},
                I.line([[x - 20, y - 56], [x - 10, y - 14]], at, "#5a4a32", 2, draw=False), I.line([[x + 16, y - 56], [x + 8, y - 14]], at, "#5a4a32", 2, draw=False),
                I.oval(x + 60, y - 24, 14, 10, "#6b5f48", at=at)]
    return [I.box(x - 40, y - 34, 16, 34, "#8a8580", r=4, at=at), I.box(x + 18, y - 34, 16, 34, "#8a8580", r=4, at=at),
            I.oval(x, y - 52, 52, 32, "#a19b94", at=at), I.oval(x + 52, y - 66, 24, 24, "#a19b94", at=at), I.oval(x + 38, y - 66, 13, 20, "#8a8580", at=at),
            I.line([[x + 70, y - 58], [x + 82, y - 34], [x + 78, y - 14]], at, "#a19b94", 9, draw=False, curve=True)]


def early_seafarers_m():
    """The first sailors as one continuous take (see mural.py): the islands that stayed islands, the deep channel, castaways on mats, and the open question."""
    remix, I = _mur()
    ep = early_seafarers()
    v = View(104, 128, -12, 20, (40, 330, 920, 900))
    FLO, SKY = "#ff9a80", "#9fd0ff"
    wl = [v.p(115.75, -9.5), v.p(116.4, -5), v.p(118.4, -2), v.p(118.6, 3), v.p(120.2, 7), v.p(122, 11), v.p(124.5, 19)]
    rx, ry = v.p(116.4, -9.7)
    # 0 · the hook: the map of the islands; a crossing, a raft, and a question
    wall = {"base": "map", "cam": [1.35, v.p(120, -4)[0], v.p(120, -4)[1]], "els": [{"k": "map", "land": v.land(), "in": -1},
            {"k": "line", "p": wl, "c": SKY, "w": 2.4, "style": "inferred", "in": .3, "fx": "draw"}] + raft(rx, ry, 46, .6) +
            [I.arrow([v.p(115.2, -9.0), v.p(117.6, -10.3), v.p(120.1, -9.1)], 1.4, AMBER, 4, "claimed", 1.4), I.glow(rx, ry, 110, 6.5, .9)]}
    # 1 · Flores, Sulawesi, Luzon; the sea falls 120 m and new land appears, but the islands stay islands
    isl = [(121.0, -8.7), (120.4, -2.2), (121.2, 16.4)]
    names = []
    for k, (lo, la) in enumerate(isl):
        x, y = v.p(lo, la)
        names += [I.ring(x, y, 52, .2 + .32 * k, FLO, 3, dur=.6), I.glow(x, y, 80, .2 + .32 * k, .5)]
    land = [I.box(70, 1120, 84, 170, "none", "#cfe6ff", 2, 6, 6.0), I.line([[60, 1142], [164, 1142]], 6.2, SKY, 3, "inferred", .5),
            I.box(72, 1230, 80, 58, "rgba(63,134,168,.6)", r=4, at=7.0), I.arrow([[112, 1150], [112, 1222]], 6.6, SKY, 3, dur=.6, curve=False),
            I.label(172, 1214, "−120 m", 7.2, "#cfe6ff", 32, "start"),
            {"k": "map", "land": [], "ghost": [v.line(SUNDA) + "Z"], "in": 9.5, "dur": 1.5},
            I.label(v.p(108, 2)[0], v.p(108, 2)[1], "Ice Age land", 10.0, "#c9ad85", 32, st="ital"),
            I.label(v.p(118.6, 3)[0] + 22, v.p(118.6, 3)[1] + 10, "deep water", 11.0, "#cfe6ff", 28, "start")] + \
           [I.ring(*v.p(lo, la), 62, 11.2 + .2 * k, SKY, 3, "inferred", .6) for k, (lo, la) in enumerate(isl)]
    pins = [("Flores · 1.02 million yrs", 121, -8.6, {"c": FLO, "a": "end", "lx": -18}), ("Sulawesi · 1.04 million+", 120.2, -3.5, {"c": FLO}),
            ("Luzon · c. 709,000", 121.4, 17.6, {"c": FLO, "a": "end", "lx": -18})]
    ages = []
    for j, (k, at) in enumerate(((1, 2.3), (0, 4.6), (2, 6.1))):
        n, lo, la, kw = pins[k]; x, y = v.p(lo, la)
        ages += [dict({"k": "pin", "x": x, "y": y, "t": n, "in": at}, **kw), I.tri(x + (26 if k != 1 else -28), y + 26, 13, 20 * k, "#e8dcc6", .8 + .3 * j)]
    # 4 · how did they get there? a storm tears a mat of trees from the shore; people drift; later, rats, tortoises and elephants
    HZ = 820
    drift = {"base": "sky", "tod": "dusk", "ground": HZ, "groundc": "url(#k-sea)", "ridges": [], "sun": [800, 700, 26], "cam": [1, 500, 940], "els": [
        {"k": "poly", "p": [[-100, 690], [60, 680], [150, 740], [220, HZ + 2], [-100, HZ + 2]], "fill": "#241d18", "c": "none", "w": 0, "in": .1},
        {"k": "palm", "x": 40, "y": 690, "h": 120, "in": .1}, {"k": "palm", "x": 120, "y": 712, "h": 100, "in": .1},
        {"k": "poly", "p": [[730, HZ + 2], [790, 790], [870, 786], [960, HZ + 2]], "fill": "#241d18", "c": "none", "w": 0, "in": .1},
        I.oval(250, 450, 170, 50, "#1b1820", at=2.4, op=.95), I.oval(390, 430, 140, 46, "#221d26", at=2.5, op=.95)] +
        [I.line([[180 + 40 * k, 500], [150 + 40 * k, 640]], 2.6 + .05 * k, "#9fb3c8", 2, op=.6, dur=.4) for k in range(8)] +
        _mat(I, 380, HZ + 18, 170, 4.3) + [I.person(355, HZ + 8, 64, 4.5, "#e8d6b8"), I.person(400, HZ + 8, 58, 4.6, "#e8d6b8"),
        I.arrow([[480, HZ + 26], [560, HZ + 40], [640, HZ + 22], [740, HZ + 30]], 5.4, AMBER, 3, "claimed", 1.6), I.glow(380, HZ - 10, 120, 4.5, .45)]}
    beasts = []
    for k, (kind, lab) in enumerate((("rat", "rats"), ("tortoise", "giant tortoises"), ("elephant", "dwarf elephants"))):
        y = 1010 + 150 * k; at = .5 + .45 * k
        beasts += _mat(I, 250, y + 6, 150, at) + _animal(I, kind, 240, y, at + .2) + [I.label(250, y + 62, lab, at + .3, BONE, 28),
                   I.arrow([[350, y], [520, y - 30 - 20 * k], [700, HZ + 70 - 10 * k], [800, HZ + 30]], at + .5, AMBER, 3, "claimed", 1.2)]
    beasts += [I.glow(380, HZ - 10, 150, 5.3, .8)]
    # 5 · again, and again: three crossings; then a researcher's bamboo raft, built with stone tools
    again = [I.arrow([v.p(117.5, 1), v.p(119.8, -2)], 1.0, AMBER, 4, dur=.8), I.arrow([v.p(118.5, 10.5), v.p(120.8, 16.5)], 1.8, AMBER, 4, dur=.8)] + \
            [I.label(*(lambda q: (q[0] + dx, q[1] + 10))(v.p(*p)), str(k + 1), at, AMBER, 44, st="serif")
             for k, (p, dx, at) in enumerate((((120.4, -10.6), 0, .5), ((118.4, -.6), -46, 1.3), ((119.2, 13.5), -46, 2.1)))] + \
            [I.glow(*v.p(*p), 90, 7.4 + .2 * k, .6) for k, p in enumerate(((120.2, -8.8), (119.8, -2), (120.8, 16.5)))]
    bamboo = [I.box(300, 1228, 600, 196, "#14110e", "#8a6a48", 2, 14, .1, op=.94), I.box(320, 1384, 560, 18, "#b89a6a", r=6, at=.2),
              I.person(380, 1384, 130, .3, "#e8d6b8"), I.tri(428, 1300, 14, 30, "#e8dcc6", 1.5), I.glow(428, 1300, 50, 1.5, .8)] + \
             [I.line([[480, 1302 + 10 * k], [850, 1298 + 10 * k]], 4.0 + .18 * k, "#c9b36a", 8, draw=True, dur=.4) for k in range(8)] + \
             [I.line([[x, 1292], [x, 1380]], 5.4 + .2 * j, "#6b4a2e", 4, dur=.4) for j, x in enumerate((520, 665, 810))] + \
             [I.glow(665, 1335, 150, 6.2, .45)]
    # 6 · the verdict: planned, or drifted? the rafts rot, the stones stay
    VZ = 760
    verdict = {"base": "sky", "tod": "dusk", "ground": VZ, "groundc": "url(#k-sea)", "ridges": [], "sun": [830, 640, 22], "cam": [1, 500, 930], "els": [
        {"k": "poly", "p": [[400, VZ + 2], [460, 730], [540, 726], [600, VZ + 2]], "fill": "#241d18", "c": "none", "w": 0, "in": .1}] +
        raft(230, 960, 150, 1.0) + [I.person(215, 950, 70, 1.1, "#e8d6b8"), I.line([[240, 900], [270, 975]], 1.1, "#8a6a48", 4, draw=False),
        I.arrow([[300, 940], [400, 850], [470, 790]], 1.3, AMBER, 4, "inferred", .9, False), I.label(230, 1050, "planned?", 1.4, AMBER, 30)] +
        _mat(I, 770, 966, 150, 1.8) + [I.person(760, 956, 66, 1.9, "#e8d6b8"),
        I.arrow([[700, 940], [660, 880], [600, 860], [560, 800]], 2.0, SKY, 3, "claimed", 1.0), I.label(770, 1050, "drifted?", 2.1, SKY, 30)] +
        I.question(500, 960, 2.3, 100) +
        [{"k": "poly", "p": [[-100, 1290], [200, 1272], [500, 1296], [800, 1268], [1100, 1290], [1100, 1800], [-100, 1800]], "fill": "#3a2f24", "c": "#8a6a48", "w": 2, "in": 3.0}] +
        [I.line([[220 + 12 * k, 1262], [330 + 12 * k, 1270]], 4.1 + .05 * k, "#c9b36a", 5, "claimed", .5) for k in range(5)] +
        [I.tri(x, y, 16, r, "#d9ccb4", 6.0 + .2 * j) for j, (x, y, r) in enumerate(((560, 1272, 10), (620, 1280, 40), (690, 1266, 70)))] +
        [I.glow(625, 1265, 120, 6.4, .8), I.label(625, 1350, "stone tools", 6.6, BONE, 30), I.label(275, 1350, "rafts rot", 4.4, "#c9b36a", 30)]}
    glow2 = [I.glow(215, 910, 110, 2.8, .7), I.glow(760, 916, 110, 3.0, .7)]
    return remix(ep, scenes={0: wall, 4: drift, 6: verdict}, alias={1: 0, 2: 0, 5: 0},
                 cams={1: [1, 500, 860], 2: [1, 500, 860], 5: [1, 500, 900]},
                 beat_adds={1: (names + land, None), 4: (again, None)},
                 line_adds={(1, 1): (ages, None), (3, 1): (beasts, [1, 500, 1000]), (4, 1): (bamboo, [1.15, 560, 1100]), (5, 1): (glow2, [1.25, 500, 900])})


# ---------------------------------------------------------------- 01.04 Denisovan Giants
def denisovan_giants():
    s0 = {"base": "dark", "cam": [1.5, 500, 920], "els": lineup([("us, average", 1.72), ("Penghu 3 · c. 1.9 m?", 1.9)], x0=380, dx=240) + [{"k": "q", "x": 650, "y": 660, "size": 60, "in": .9, "fx": "pop"}]}
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 460, "t": "until recently, the whole Denisovan collection", "in": .1}] +
          [{"k": "poly", "p": [[240, 800], [270, 800], [268, 740], [256, 728], [244, 732]], "fill": "#e8dcc6", "c": "#fff6e6", "w": 1.4, "in": .3},
           {"k": "label", "x": 255, "y": 840, "t": "a finger bone", "st": "small", "in": .4}] +
          [{"k": "poly", "p": [[420 + k * 70, 800], [470 + k * 70, 800], [476 + k * 70, 760], [466 + k * 70, 736], [428 + k * 70, 736], [416 + k * 70, 760]], "fill": "#f0e6d2", "c": "#fff6e6", "w": 1.4, "in": .5 + k * .1} for k in range(3)] +
          [{"k": "label", "x": 525, "y": 840, "t": "huge molars", "st": "small", "in": .7},
           {"k": "poly", "p": [[700, 800], [860, 800], [880, 760], [860, 740], [820, 752], [720, 752], [700, 770]], "fill": "#e8dcc6", "c": "#fff6e6", "w": 1.4, "curve": True, "in": .9},
           {"k": "label", "x": 790, "y": 840, "t": "a heavy jaw", "st": "small", "in": 1.0}]}
    s2 = {"base": "dark", "floor": 1000, "cam": [1.05, 500, 880], "els": skull(500, 900, 2.1, robust=True) + [{"k": "glow", "x": 500, "y": 860, "r": 320, "kind": "lamp", "op": .3},
          {"k": "cap", "x": 500, "y": 560, "t": "Harbin · brain c. 1,420 cm³", "in": .4}]}
    v = View(115, 125.5, 19, 29, (60, 330, 880, 900))
    s3 = mapshot(v, pins=[("Penghu Channel", 119.6, 23.5, {"c": OCHRE, "a": "end", "lx": -18})], extra=[
        {"k": "label", "x": v.p(121, 23.8)[0], "y": v.p(121, 23.8)[1], "t": "Taiwan", "st": "ital", "c": "#c9ad85"},
        {"k": "cap", "x": 500, "y": 1240, "t": "two leg bones · 2026 preprint", "in": .6}])
    s4 = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "cap", "x": 500, "y": 460, "t": "when were they last seen?", "in": .1}]}
    tl, ax = timeline(-60000, 0, [(-60000, "60,000 yrs ago"), (-40000, "40,000"), (-20000, "20,000"), (0, "today")], "", y=980)
    s4 = tl
    s4["els"] += [{"k": "band", "x0": ax.x(-60000), "x1": ax.x(-40000), "y": 880, "h": 16, "c": SCAN, "t": "latest known Denisovans", "in": .3},
                  {"k": "band", "x0": ax.x(-3200), "x1": ax.x(-2000), "y": 780, "h": 16, "c": AMBER, "t": "oldest giant stories", "in": .8}]
    s5 = {"base": "dark", "cam": [1.35, 500, 920], "els": lineup([("tall today", 2.0), ("Penghu 3?", 1.9), ("Jinniushan ♀", 1.69), ("us, average", 1.72)], x0=200, dx=200)}
    s6 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "glyphs", "x": 250, "y": 640, "w": 500, "h": 240, "rows": 4, "cols": 12, "kind": "latin", "c": "#9fd0ff", "in": .2},
          {"k": "title", "y": 980, "t": "EPAS1", "st": "big", "in": .6, "fx": "pop"}, {"k": "label", "x": 500, "y": 1040, "t": "a Denisovan gene variant that helps Tibetans at altitude", "in": 1.0}]}
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE DENISOVANS][sfx:boom][act:hushed, pulling us in][tune:level]A ^lost kind of human... [act:wonder, slowly][tune:fall]that may have stood nearly ^*two metres* tall."], cut=False),
        B("world", 1, ["[d:calm][k:WHO THEY WERE][act:plain storytelling]The Denisovans were found through ^DNA in {2010|twenty ten}. [act:a little rueful, counting the scraps]For years, all we had was a finger ^bone, some ^teeth, and a ^jaw.",
                       "[d:build][go:2|0][act:building, weightier][tune:level]^Huge teeth. [act:same weight, continuing][tune:level]^Heavy jaws. [act:the big one, slower]And the ^Harbin skull: one of the ^biggest archaic skulls ever found."]),
        B("collision", 3, ["[d:build][k:2026 · TAIWAN][act:news, brisk and curious][tune:level]Now two ^leg bones, dredged from the sea off Taiwan, point to people about one metre ^eighty... [act:the bigger number, wonder][tune:fall]and one ^*ninety*."]),
        B("cost", 3, ["[d:build][k:THE LEGEND][act:respectful, storyteller's voice]Some link them to the ^giants of ancient stories. [sfx:hit][act:evocative, slower]^Tall, powerful peoples, remembered in ^myth."], cut=False),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:gentle correction, clear]But the last known Denisovans lived ^tens of thousands of years ^before those stories were written.",
                          "[d:list][go:5|0][act:fair, weighing it][tune:level]And one ninety is ^tall... [act:gently deflating][tune:fall]not a ^giant. [act:a careful caveat, lower]The height study isn't ^peer reviewed yet. [act:dry, pointed][tune:fall]And it's ^*two* bones."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]^Big people? [act:measured, fair][tune:fall]^Plausible. [act:the next question, even][tune:rise]Giants of ^legend? [act:the verdict, level-headed][tune:fall]No ^evidence.",
                     "[d:tension][p:0.93][act:warm, a hopeful turn][tune:fall]But their DNA ^still helps people in Tibet breathe at ^*altitude*."]),
    ]
    return EP("denisovan-giants", "01.04", "Denisovan Giants", "denisovan-giants", "plausible", "Were the Denisovans giants?", "Nearly *two metres* tall?", beats, shots,
              "Reich et al. 2010, Nature · Tsutaya et al. 2025, Science · Fu et al. 2025, Science · Huerta-Sánchez et al. 2014, Nature · Kaifu et al. 2026, preprint",
              "Two leg bones from the Taiwan Strait suggest the Denisovans stood tall. Were they the giants of legend? What the evidence shows.",
              ["#Denisovans", "#HumanEvolution", "#Science", "#Archaeology", "#History"])


def _ghost(I, x, y, h, at, c=None, op=None):
    """A person drawn as a dotted outline: claimed, not measured (a giant of legend)."""
    c = c or I.LILAC; w = h * .26
    body = [[x - w * .5, y - h * .78], [x + w * .5, y - h * .78], [x + w * .42, y - h * .42], [x + w * .3, y], [x + w * .08, y], [x, y - h * .36], [x - w * .08, y], [x - w * .3, y], [x - w * .42, y - h * .42]]
    out = [{"k": "circle", "x": x, "y": round(y - h * .9, 1), "r": round(h * .085, 1), "fill": "none", "c": c, "w": 3, "style": "claimed", "in": at},
           {"k": "poly", "p": [[round(a, 1), round(b, 1)] for a, b in body], "fill": "rgba(201,193,238,.06)", "c": c, "w": 3, "style": "claimed", "in": at}]
    if op is not None:
        for e in out:
            e.update(op=op, keepop=True)
    return out


def _molar(I, x, y, s, at):
    return {"k": "poly", "p": [[x - 30 * s, y], [x + 30 * s, y], [x + 34 * s, y - 34 * s], [x + 20 * s, y - 56 * s], [x + 6 * s, y - 46 * s], [x - 8 * s, y - 58 * s], [x - 24 * s, y - 50 * s], [x - 34 * s, y - 34 * s]],
            "fill": "#f0e6d2", "c": "#fff6e6", "w": 1.6, "curve": True, "in": at, "fx": "pop"}


def _jaw(I, x, y, s, at):
    return {"k": "poly", "p": [[x - 120 * s, y], [x + 40 * s, y], [x + 90 * s, y - 20 * s], [x + 110 * s, y - 80 * s], [x + 80 * s, y - 90 * s], [x + 60 * s, y - 44 * s], [x - 110 * s, y - 40 * s], [x - 128 * s, y - 20 * s]],
            "fill": "#e8dcc6", "c": "#fff6e6", "w": 1.6, "curve": True, "in": at, "fx": "pop"}


def denisovan_giants_m():
    """Denisovan giants as one continuous take (see mural.py): a shoebox of bones, a bottle of brain, heights from leg bones, an hour of history, and the gene that stayed."""
    remix, I = _mur()
    ep = denisovan_giants()
    DEN, US, LEG = "#9fd0ff", "#f2c98e", I.LILAC
    M = 190
    # 0 · a lost kind of human, nearly two metres tall; the giants of legend? (a dotted giant); weigh the bones
    G0 = 1180
    hook = {"base": "dark", "cam": [1.1, 500, 960], "els": [I.line([[100, G0], [900, G0]], 0, "#8c7152", 2, draw=False),
            I.person(260, G0, 1.72 * M, .3, US), I.label(260, G0 + 44, "us, 1.72 m", .5, US, 28),
            I.glow(480, G0 - 180, 200, 2.6, .35), I.person(480, G0, 1.9 * M, 2.6, "#c9b49a"), I.label(480, G0 + 44, "1.9 m?", 3.2, DEN, 30)] +
            _ghost(I, 730, G0, 3.0 * M, 4.9) + I.question(730, G0 - 3.0 * M - 30, 5.4, 80) + [I.label(730, G0 + 44, "a giant?", 5.3, LEG, 28)]}
    # 1 · found through DNA; all we had: a finger bone, some teeth, a jaw; the lot fits in a shoebox
    helix = [I.line([[160 + 9 * k, round(560 + 18 * math.sin(k * .6 + ph), 1)] for k in range(76)], .9, DEN, 3, dur=1.4, curve=True) for ph in (0, math.pi)]
    box = {"base": "dark", "floor": 1120, "cam": [1.1, 500, 900], "els": helix + [I.label(500, 640, "2010: DNA first", 2.1, DEN, 30),
           {"k": "poly", "p": [[262, 1012], [288, 1012], [287, 952], [281, 934], [275, 930], [269, 932], [263, 952]], "fill": "#efe6d2", "c": "#fff6e6", "w": 1.6, "curve": True, "in": 6.7, "fx": "pop"},
           _molar(I, 400, 1012, .9, 7.4), _molar(I, 470, 1012, .9, 7.55), _molar(I, 540, 1012, .9, 7.7), _jaw(I, 720, 1012, .8, 8.3),
           I.label(275, 1068, "finger", 6.9, BONE, 28), I.label(470, 1068, "teeth", 7.8, BONE, 28), I.label(720, 1068, "jaw", 8.5, BONE, 28),
           I.box(190, 880, 640, 230, "none", AMBER, 3, 10, 9.4, fx="draw", dur=1.2), I.line([[190, 880], [250, 830], [890, 830], [830, 880]], 10.0, AMBER, 3, dur=.6),
           I.line([[890, 830], [890, 1060], [830, 1110]], 10.2, AMBER, 3, dur=.6), I.label(510, 1170, "one shoebox", 10.6, AMBER, 32)]}
    # 2 · huge teeth, heavy jaws, the Harbin skull; its brain space: 1.4 litres, nearly a big bottle of water
    bottle = [I.box(700, 1110, 130, 250, "none", "#cfe6ff", 3, 18, 7.5, fx="draw", dur=.8), I.box(738, 1070, 54, 42, "none", "#cfe6ff", 3, 6, 7.5, fx="draw", dur=.5),
              I.box(704, 1114 + 250 * (1 - 1.42 / 1.5), 122, round(242 * 1.42 / 1.5, 1), "rgba(95,168,201,.75)", r=14, at=7.9, fx="fill", dur=1.6),
              I.label(765, 1410, "1.4 litres", 8.3, "#cfe6ff", 32), I.label(600, 1250, "≈", 7.3, BONE, 60, st="serif")]
    harbin = {"base": "dark", "cam": [1.05, 500, 920], "els": [_molar(I, 210, 600, 1.4, .9), _molar(I, 310, 600, 1.4, 1.0), _jaw(I, 640, 600, 1.2, 1.6),
              I.label(260, 650, "huge teeth", 1.1, BONE, 28), I.label(650, 650, "heavy jaws", 1.8, BONE, 28),
              I.glow(420, 940, 280, 2.5, .35)] + skull(420, 1000, 1.6, robust=True, i=2.5) + \
             [I.label(420, 1150, "Harbin", 2.8, AMBER, 32), {"k": "poly", "p": [[300, 930], [380, 860], [470, 850], [540, 880], [560, 930], [470, 950], [360, 950]], "fill": "rgba(95,168,201,.35)", "c": "#cfe6ff", "w": 2,
              "style": "inferred", "curve": True, "in": 5.4}] + bottle}
    # 3 · two leg bones dredged off Taiwan; longer bones, taller people: 1.8 and 1.9 m; then the giant of the stories
    vm = View(116, 124, 20.5, 27.5, (250, 280, 500, 340))
    px, py = vm.p(119.6, 23.5)
    inset = {"k": "group", "clip": [250, 280, 500, 340, 16], "bg": "#16303d", "in": .2, "els": [{"k": "map", "land": vm.land()},
             {"k": "pin", "x": px, "y": py, "t": "Penghu Channel", "c": "#ff9a80", "a": "end", "lx": -18},
             {"k": "label", "x": vm.p(121.2, 23.6)[0], "y": vm.p(121.2, 23.6)[1], "t": "Taiwan", "st": "ital", "c": "#c9ad85", "size": 30}]}
    GD = 1380; M3 = 174
    def trousers(x, h, at):
        w = h * .26
        return {"k": "poly", "p": [[x - w * .44, GD - h * .44], [x + w * .44, GD - h * .44], [x + w * .32, GD], [x + w * .07, GD], [x, GD - h * .34], [x - w * .07, GD], [x - w * .32, GD]],
                "fill": "#3f5f7a", "c": "#9fd0ff", "w": 1.5, "op": .75, "keepop": True, "in": at}
    legbone = lambda x, h, at: [I.line([[x + 6, GD - h * .52], [x + 6, GD - h * .27]], at, "#fff6e6", 7, dur=.5), I.glow(x + 6, GD - h * .4, 50, at, .9)]
    taiwan = {"base": "dark", "cam": [1, 500, 880], "els": [inset, I.box(250, 660, 500, 140, "#16303d", "none", 0, 12, .2),
              {"k": "water", "y": 680, "x0": 250, "x1": 750, "h": 110, "op": .8, "in": .2}, I.box(250, 780, 500, 20, "#4a3a2c", r=6, at=.2),
              {"k": "boat", "x": 400, "y": 682, "w": 130, "in": 1.3}, I.line([[430, 690], [470, 782]], 1.5, "#cbbca8", 2, dur=.6),
              I.line([[480, 760], [540, 748]], 1.8, "#efe6d2", 7, draw=False), I.line([[520, 776], [585, 770]], 1.9, "#efe6d2", 7, draw=False), I.glow(530, 765, 70, 1.8, .8),
              I.line([[120, GD], [900, GD]], 2.8, "#8c7152", 2, draw=False),
              I.person(230, GD, 1.72 * M3, 3.0, "#6e6458"), I.label(230, GD + 40, "us", 3.1, BONE, 28)] +
             [I.person(420, GD, 1.8 * M3, 4.6, "#c9b49a")] + legbone(420, 1.8 * M3, 4.8) + [I.label(420, GD - 1.8 * M3 - 26, "1.8 m", 10.4, DEN, 32)] +
             [I.person(600, GD, 1.9 * M3, 6.2, "#c9b49a")] + legbone(600, 1.9 * M3, 6.4) + [I.label(600, GD - 1.9 * M3 - 26, "1.9 m", 11.2, DEN, 32)] +
             [trousers(x, h, 9.0 + .2 * j) for j, (x, h) in enumerate(((420, 1.8 * M3), (600, 1.9 * M3)))]}
    legend = _ghost(I, 810, GD, 3.0 * M3, 1.5) + [I.glow(810, GD - 260, 220, 1.5, .3), I.label(810, GD + 40, "the stories", 2.0, LEG, 28)] + I.question(810, GD - 3.0 * M3 - 40, 5.0, 70)
    # 4 · one hour for 60,000 years: the Denisovans fade at minute 20; the giant stories arrive in the last three minutes
    CX, CY, R = 500, 900, 290
    pt = lambda m, r: [round(CX + r * math.cos(math.radians(-90 + 6 * m)), 1), round(CY + r * math.sin(math.radians(-90 + 6 * m)), 1)]
    wedge = lambda m0, m1: [[CX, CY]] + [pt(m0 + (m1 - m0) * k / 24, R - 6) for k in range(25)]
    clock = {"base": "dark", "cam": [1, 500, 900], "els": [I.oval(CX, CY, R, R, "#1c1612", "#cbbca8", 3, 1, .2)] +
             [I.line([pt(m, R - 4), pt(m, R - (26 if m % 15 == 0 else 14))], .3, "#cbbca8", 3 if m % 15 == 0 else 2, draw=False) for m in range(0, 60, 5)] +
             [{"k": "poly", "p": wedge(0, 20), "fill": "rgba(159,208,255,.55)", "c": DEN, "w": 2, "in": .7},
              {"k": "poly", "p": wedge(56.8, 58), "fill": AMBER, "c": AMBER, "w": 2, "in": 2.3}, I.glow(*pt(57.4, R - 40), 80, 2.3, .9),
              {"k": "line", "p": [pt(20 + k * .5, R + 26) for k in range(74)], "c": "#8a7a66", "w": 3, "style": "inferred", "curve": True, "in": 1.3, "fx": "draw", "dur": 1.0},
              I.label(CX, CY + R + 76, "a long gap", 1.6, BONE, 30),
              I.line([[CX, CY], pt(0, R - 30)], 3.2, BONE, 5, draw=False), I.dot(CX, CY, 10, BONE, 3.2),
              I.label(CX + 24, CY - R - 24, "60,000 years ago", 3.5, DEN, 28, "start"), I.label(CX - 24, CY - R - 24, "today", 3.9, AMBER, 28, "end"),
              {"k": "line", "p": [pt(k * .5, R - 50) for k in range(121)], "c": BONE, "w": 2, "op": .6, "keepop": True, "curve": True, "in": 4.0, "fx": "draw", "dur": 1.6},
              I.label(*pt(10, R * .55), "Denisovans", 5.0, "#e8f4ff", 30), I.label(*(lambda q: (q[0] + 26, q[1] + 10))(pt(20, R + 26)), "20", 5.9, DEN, 34, "start", st="serif"),
              I.label(*(lambda q: (q[0] - 10, q[1] + 10))(pt(54.5, R + 40)), "3 min", 8.0, AMBER, 32, "end")]}
    # 5 · 1.9 m is tall, not a giant; not yet reviewed; two bones
    G5 = 1260; M5 = 190
    tall = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[100, G5], [900, G5]], 0, "#8c7152", 2, draw=False),
            I.person(260, G5, 2.0 * M5, 3.0, "#e8d6b8"), I.label(260, G5 + 44, "today, 2 m", 3.2, BONE, 28),
            I.person(440, G5, 1.9 * M5, .2, "#c9b49a"), I.label(440, G5 + 44, "1.9 m", .4, DEN, 30), I.person(600, G5, 1.72 * M5, .2, US), I.label(600, G5 + 44, "us", .4, US, 28)] +
           _ghost(I, 790, G5, 3.0 * M5, .8, op=.8) + [I.strike(690, G5 - 520, 890, G5 - 120, 1.6, I.RED, 6),
            I.box(130, 330, 170, 220, "#e8dcc2", "#8a7a66", 2, 6, 5.9)] + [I.line([[155, 370 + 26 * k], [275, 370 + 26 * k]], 6.1 + .05 * k, "#8a7a66", 3, dur=.2) for k in range(6)] +
           [I.ring(272, 520, 30, 7.6, LEG, 3, "claimed"), I.label(215, 600, "not yet checked", 7.8, LEG, 28),
            I.line([[610, 420], [800, 420]], 9.2, "#efe6d2", 14, draw=False), I.dot(605, 412, 12, "#efe6d2", 9.2), I.dot(605, 428, 12, "#efe6d2", 9.2), I.dot(805, 412, 12, "#efe6d2", 9.2), I.dot(805, 428, 12, "#efe6d2", 9.2),
            I.line([[610, 490], [780, 490]], 9.4, "#efe6d2", 12, draw=False), I.dot(605, 483, 11, "#efe6d2", 9.4), I.dot(605, 497, 11, "#efe6d2", 9.4), I.dot(785, 483, 11, "#efe6d2", 9.4), I.dot(785, 497, 11, "#efe6d2", 9.4),
            I.label(705, 560, "two bones", 9.6, BONE, 30)]}
    # 6 · the verdict: big people, plausible; giants of legend, no evidence; and the gene that helps Tibetans breathe high up
    GV = 760; MV = 150
    air = [I.dot(x, y, 4, "#cfe6ff", round(2.8 + .01 * k, 2), op=.8) for k, (x, y) in enumerate(I.scatter(60, 60, 330, 1220, 1405, 5) + I.scatter(9, 590, 930, 1000, 1085, 6))]
    tibet = [{"k": "poly", "p": [[-100, 1420], [300, 1420], [420, 1300], [520, 1110], [560, 1100], [1100, 1100], [1100, 1800], [-100, 1800]], "fill": "#4a3c30", "c": "#8a6a48", "w": 2, "in": .2, "fx": "rise"},
             I.person(170, 1418, 120, .9, "#cbbca8"), I.person(740, 1100, 120, 1.1, "#e8d6b8"), I.glow(740, 1040, 120, 1.9, .5)] + air + \
            [I.line([[560 + 9 * k, round(935 + 14 * math.sin(k * .6 + ph), 1)] for k in range(38)], 4.2, "#8a8378", 3, dur=1.0, curve=True) for ph in (0, math.pi)] + \
            [I.line([[668 + 9 * k, round(935 + 14 * math.sin(k * .6 + ph), 1)] for k in range(9)], 4.9, DEN, 5, dur=.6, curve=True) for ph in (0, math.pi)] + \
            [I.glow(706, 935, 80, 4.9, .9), I.label(730, 890, "one Denisovan gene", 5.2, DEN, 28)]
    verdict = {"base": "dark", "cam": [1.15, 500, 620], "els": [I.line([[140, GV], [860, GV]], .1, "#8c7152", 2, draw=False),
               I.person(330, GV, 1.9 * MV, .3, "#c9b49a"), I.glow(330, GV - 140, 160, 1.4, .5), I.label(330, GV + 44, "plausible", 1.6, I.GREEN, 30)] +
              _ghost(I, 650, GV, 3.0 * MV, 2.4) + [I.strike(560, GV - 420, 740, GV - 60, 4.0, I.RED, 6), I.label(650, GV + 44, "no evidence", 4.2, I.RED, 30)]}
    return remix(ep, scenes={0: hook, 1: box, 2: harbin, 3: taiwan, 4: clock, 5: tall, 6: verdict},
                 beat_adds={3: (legend, [1.1, 560, 1060])}, line_adds={(5, 1): (tibet, [1.05, 500, 1040])})


# ---------------------------------------------------------------- 01.05 The Ice Age Surgeons
def surgeons():
    v = View(108, 122, -6, 8, (60, 330, 880, 900))
    s0 = {"base": "dark", "floor": 1100, "cam": [1.2, 500, 860], "els": leg_bones(500, 1100, 1.0, cut=.3, healed=True, i=.1) + [{"k": "glow", "x": 500, "y": 800, "r": 300, "kind": "lamp", "op": .3}]}
    s1 = mapshot(v, pins=[("Liang Tebo cave", 117.85, 0.95, {"c": OCHRE, "a": "end", "lx": -18})], extra=[{"k": "label", "x": v.p(114, -1)[0], "y": v.p(114, -1)[1], "t": "Borneo", "st": "ital", "c": "#c9ad85"}])
    burial = [{"k": "poly", "p": [[-100, 1000], [1100, 1000], [1100, 1500], [-100, 1500]], "fill": "#3a2c20", "c": "none", "w": 0},
              {"k": "line", "p": [[240, 960], [760, 960]], "c": "#e8dcc6", "w": 16, "in": .2}] + skull(210, 950, .45, i=.2) + \
             [{"k": "circle", "x": 200 + k * 70, "y": 925 - (k % 2) * 10, "r": 22, "fill": "#8c7f70", "c": "#c9bca9", "w": 1, "in": .6 + k * .1} for k in range(4)] + \
             [{"k": "circle", "x": 270, "y": 990, "r": 12, "fill": "#b0301e", "c": "none", "w": 0, "in": 1.0},
              {"k": "label", "x": 270, "y": 1050, "t": "red ochre", "st": "small", "c": "#ff9a80", "in": 1.1},
              {"k": "label", "x": 330, "y": 870, "t": "rocks over head and arms", "st": "small", "in": .9},
              {"k": "cap", "x": 500, "y": 520, "t": "a careful burial · c. 31,000 years ago", "in": .3}]
    s2 = {"base": "dark", "cam": [1.7, 470, 950], "els": burial}
    s3 = {"base": "dark", "floor": 1100, "cam": [1.05, 500, 860], "els": leg_bones(500, 1100, 1.0, cut=.3, i=.1) + [{"k": "label", "x": 620, "y": 740, "t": "clean, oblique cut through both bones", "st": "small", "a": "start", "c": GOLD, "in": .8}]}
    s4 = {"base": "dark", "floor": 1100, "cam": [1.4, 520, 760], "els": leg_bones(500, 1100, 1.0, cut=.3, healed=True, i=-1) + [{"k": "label", "x": 560, "y": 690, "t": "rounded, healed stump: 6 to 9 more years of life", "st": "small", "a": "start", "c": GOLD, "in": .6}]}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 500, "t": "no antiseptics, no steel, no hospital", "in": .1}] +
          [e for k, t in enumerate(["stop the bleeding", "manage the pain", "keep infection out"]) for e in (
              {"k": "circle", "x": 260, "y": 640 + k * 130, "r": 26, "fill": "none", "c": GOLD, "w": 2.4, "in": .3 + k * .35},
              {"k": "label", "x": 310, "y": 650 + k * 130, "t": t, "st": "body", "a": "start", "in": .4 + k * .35})]}
    tl, ax = timeline(-35000, 0, [(-30000, "30,000 yrs ago"), (-20000, "20,000"), (-10000, "10,000"), (0, "today")], "the oldest known amputations", y=980)
    tl["els"] += event(ax, -31000, "Borneo", y=980, row=1, c=GOLD, i=.4, sub="c. 31,000") + event(ax, -7000, "France", y=980, row=0, i=.9, sub="c. 7,000")
    s6 = tl
    s7 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:BORNEO][sfx:boom][act:hushed, grave, pulling us in][tune:level]About thirty-one thousand years ago, someone cut off a child's ^leg...",
                      "[d:tension][cam:1.12|0|0][gap:0.4][act:quiet wonder, the reveal][tune:fall]And the child ^*survived*."], cut=False),
        B("world", 1, ["[d:calm][k:LIANG TEBO CAVE][act:gentle, respectful storytelling]In a cave in Borneo, archaeologists found a young ^adult, buried with ^care.",
                       "[d:list][go:2|0][act:quiet, noting the details][tune:level]^Rocks placed over the head and ^arms. [act:softly, a tender detail][tune:fall]A lump of red ^ochre by the jaw."]),
        B("collision", 3, ["[d:build][k:THE LEG][act:clinical, precise]The lower left leg was ^missing. [act:careful, observing]Both bones cut ^clean, at an ^angle. [sfx:hit][act:flat, pointed][tune:level]No ^crushing. [act:same flat weight][tune:fall]No ^splinters.",
                           "[d:list][go:4|2][act:the good news, warmer]And the ends had ^healed into a smooth stump. [act:quiet wonder, slower][tune:fall]The child lived another ^six to nine ^*years*."]),
        B("cost", 5, ["[d:build][k:THE HARD PART][act:admiring, counting the feats]In a tropical forest, with no antiseptics, somebody stopped the ^bleeding, managed the ^pain, and kept ^infection away."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:setting up the comparison, clear]Before this, the oldest known amputation was a ^farmer in France, about ^seven thousand years ago.",
                          "[d:reveal][sfx:shimmer][act:the reveal, slower, relishing it]Borneo pushes surgery ^back by about [count:24000|years]twenty-four ^*thousand* years."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:honest caveat, calm][tune:fallrise]^One skeleton. [act:the verdict, confident][tune:fall]But a ^strong case for Ice Age ^medicine.",
                     "[d:tension][p:0.93][act:warm, the last word, quiet][tune:fall]They knew ^more than we ever gave them ^*credit* for."]),
    ]
    return EP("ice-age-surgeons", "01.05", "The Ice Age Surgeons", "stone-age-surgery", "strong", "Surgery 31,000 years ago?", "The child *survived*.", beats, shots,
              "Maloney et al. 2022, Nature · Buquet-Marcon et al. 2009, Antiquity · Oxilia et al. 2015, Scientific Reports",
              "A child's leg was amputated in Borneo about 31,000 years ago, and the child lived for years. The oldest known surgery.",
              ["#Archaeology", "#Medicine", "#Borneo", "#IceAge", "#History"])


def _fig(I, x, fy, h, at, c="#e8d6b8", cut=True):
    """A front-facing pictogram; cut: the lower part of the left leg (on the viewer's right) is missing, drawn dotted."""
    w = max(4, round(h * .05)); hip = fy - h * .40; knee = fy - h * .19; cy = fy - h * .12
    out = [I.dot(x, fy - h * .87, round(h * .075, 1), c, at, fx=None), I.box(x - h * .085, fy - h * .79, h * .17, h * .40, c, r=h * .05, at=at),
           I.line([[x - h * .07, fy - h * .76], [x - h * .14, fy - h * .48]], at, c, w * .8, draw=False), I.line([[x + h * .07, fy - h * .76], [x + h * .14, fy - h * .48]], at, c, w * .8, draw=False),
           I.line([[x - h * .045, hip], [x - h * .06, knee], [x - h * .065, fy]], at, c, w, draw=False)]
    if cut:
        out += [I.line([[x + h * .045, hip], [x + h * .06, knee], [x + h * .062, cy]], at, c, w, draw=False),
                I.line([[x + h * .062, cy], [x + h * .065, fy]], at, c, 3, "claimed", draw=False)]
    else:
        out += [I.line([[x + h * .045, hip], [x + h * .06, knee], [x + h * .065, fy]], at, c, w, draw=False)]
    return out


def _bones(x, y, s, at, broken=False, c="#e8dcc6"):
    """Tibia and fibula (as in scenes.leg_bones), ending 30% short: a clean oblique cut, or a jagged break with splinters."""
    L = 520 * s; bot = y - L * .3
    if not broken:
        return leg_bones(x, y, s, cut=.3, i=at)
    tib = [[x - 22 * s, y - L], [x + 26 * s, y - L], [x + 16 * s, y - L * .8], [x + 12 * s, bot + 4 * s], [x + 6 * s, bot - 12 * s], [x, bot + 10 * s], [x - 6 * s, bot - 14 * s], [x - 14 * s, bot + 2 * s], [x - 12 * s, y - L * .8]]
    fib = [[x + 36 * s, y - L * .96], [x + 46 * s, y - L * .96], [x + 43 * s, bot - 6 * s], [x + 40 * s, bot + 8 * s], [x + 36 * s, bot - 10 * s]]
    return [{"k": "poly", "p": tib, "fill": c, "c": "#fff6e6", "w": 1.6, "in": at}, {"k": "poly", "p": fib, "fill": "#d9ccb4", "c": "#fff6e6", "w": 1.4, "in": at}] + \
           [{"k": "poly", "p": [[x + dx * s, bot + dy * s], [x + (dx + 8) * s, bot + (dy + 18) * s], [x + (dx - 6) * s, bot + (dy + 14) * s]], "fill": c, "c": "none", "w": 0, "in": at}
            for dx, dy in ((-24, 30), (10, 44), (30, 26), (-6, 60))]


def surgeons_m():
    """The Ice Age surgeons as one continuous take (see mural.py): a child who grew up, a careful grave, a cut not a break, a bone that healed for years, and 24,000 years."""
    remix, I = _mur()
    ep = surgeons()
    OK, NO, PAST = I.GREEN, I.RED, "#ff9a80"
    # 0 · a child, the lower left leg missing; the child survived (and at the verdict: one case)
    hook = {"base": "dark", "floor": 1220, "cam": [1.05, 500, 920], "els": [I.glow(500, 900, 300, .2, .3)] + _fig(I, 500, 1220, 560, .3) +
            [I.ring(531, 1220 - 560 * .12, 30, 2.8, AMBER, 3, dur=.6), I.glow(500, 860, 260, 5.1, .6)]}
    # 1 · Borneo; the leg was lost in childhood, and the child grew up
    grew = [I.box(250, 1250, 500, 175, "#14110e", "#8a6a48", 2, 14, 4.0, op=.94)] + _fig(I, 360, 1400, 110, 4.2) + \
           [I.arrow([[410, 1340], [480, 1320], [560, 1340]], 5.8, AMBER, 3, "inferred", .8)] + _fig(I, 640, 1400, 160, 6.2) + \
           [I.label(360, 1280, "child", 4.4, BONE, 28), I.label(640, 1225, "young adult", 6.4, BONE, 28)]
    v = View(108, 122, -6, 8, (60, 330, 880, 900))
    cave = [I.glow(*v.p(117.85, 0.95), 120, .6, .6)]
    # 2 · the grave: rocks over the head and arms, red ochre by the jaw
    GR = 860
    grave = {"base": "section", "tod": "night", "ground": 700, "layers": [{"d": 0, "c": "#5f4c39", "t": ""}, {"d": 380, "c": "#4a3a2c", "t": ""}], "cam": [1.15, 500, 900], "els": [
             {"k": "poly", "p": [[180, 700], [820, 700], [800, 960], [200, 960]], "fill": "#2e2318", "c": "#8a6a48", "w": 2, "style": "inferred", "in": .2, "curve": False},
             I.oval(270, GR + 40, 30, 26, "#d8ccb6", at=.4), I.line([[305, GR + 44], [640, GR + 48]], .4, "#d8ccb6", 20, draw=False),
             I.line([[640, GR + 48], [760, GR + 46]], .4, "#d8ccb6", 14, draw=False), I.line([[640, GR + 60], [700, GR + 62]], .4, "#d8ccb6", 14, draw=False),
             I.line([[700, GR + 62], [760, GR + 64]], .4, "#d8ccb6", 3, "claimed", draw=False)] +
            [I.dot(x, y, r, "#8c7f70", round(.4 + .25 * k, 2)) for k, (x, y, r) in enumerate(((250, GR + 10, 24), (296, GR + 6, 20), (400, GR + 26, 22), (460, GR + 22, 20), (520, GR + 28, 18)))] +
            [I.label(380, 650, "rocks", 1.0, BONE, 30), I.line([[380, 664], [300, GR - 16]], 1.0, "#8a7a66", 2, dur=.4), I.line([[380, 664], [450, GR]], 1.0, "#8a7a66", 2, dur=.4),
             I.dot(268, GR + 76, 11, "#c0442c", 3.2), I.glow(268, GR + 76, 50, 3.2, .9), I.label(268, 1030, "red ochre", 3.5, PAST, 30),
             I.glow(500, GR + 40, 330, 6.4, .25)]}
    # 3 · a cut, not a break; the stick test
    stick = lambda x, y, at, jag: [I.line([[x - 200, y], [x - 10, y]], at, "#a8865e", 26, draw=False)] + \
        ([{"k": "poly", "p": [[x - 12, y - 13], [x + 10, y - 5], [x - 2, y], [x + 14, y + 6], [x - 4, y + 9], [x + 6, y + 13], [x - 12, y + 13]], "fill": "#a8865e", "c": "none", "w": 0, "in": at},
          {"k": "poly", "p": [[x + 26, y - 4], [x + 46, y], [x + 28, y + 4]], "fill": "#a8865e", "c": "none", "w": 0, "in": at}] if jag else
         [I.line([[x - 22, y - 13], [x - 2, y + 13]], at, "#f2d9b0", 4, draw=False)])
    cut = {"base": "dark", "floor": 1000, "cam": [1.12, 500, 900], "els": _bones(320, 1000, 1.0, .3) + [I.line([[300, 836], [338, 852]], 1.6, AMBER, 4, dur=.4), I.glow(320, 846, 60, 1.6, .8),
           I.label(270, 860, "cut", 1.9, AMBER, 32, "end")] + _bones(680, 1000, 1.0, 2.6, broken=True) + [I.label(680, 940, "crushed", 2.8, NO, 32),
           {"k": "line", "p": [[600, 470], [760, 900]], "c": NO, "w": 5, "in": 3.0, "fx": "draw", "dur": .5}, {"k": "line", "p": [[760, 470], [600, 900]], "c": NO, "w": 5, "in": 3.3, "fx": "draw", "dur": .5}] +
          stick(410, 1170, 5.8, False) + stick(800, 1170, 4.0, True) + [I.label(310, 1235, "cut", 6.0, BONE, 30), I.label(700, 1235, "snapped", 4.2, BONE, 30),
           I.ring(320, 846, 70, 9.3, OK, 4), I.label(320, 965, "deliberate", 9.5, OK, 32)]}
    # 4 · healing: the cut end rounds off over years; six to nine more years of life
    end = lambda x, at, k: [I.box(x - 34, 460, 68, 300 - [0, 10, 26][k], "#e8dcc6", "#fff6e6", 1.5, [2, 18, 34][k], at)] + \
        ([{"k": "poly", "p": [[x - 34, 740], [x + 34, 712], [x + 34, 764], [x - 34, 764]], "fill": "#120d0a", "c": "none", "w": 0, "in": at}] if k == 0 else [])
    X = lambda yr: 160 + 68 * yr
    heal = {"base": "dark", "cam": [1, 500, 900], "els": end(710, .4, 2) + [I.label(710, 830, "sealed", .6, BONE, 28), I.glow(710, 740, 90, .6, .7),
            *end(230, 2.8, 0), I.label(230, 830, "cut", 2.9, BONE, 28), I.arrow([[290, 610], [360, 610]], 3.4, AMBER, 3, dur=.4, curve=False),
            *end(470, 3.6, 1), I.label(470, 830, "rounding", 3.7, BONE, 28), I.arrow([[530, 610], [600, 610]], 4.1, AMBER, 3, dur=.4, curve=False),
            I.line([[X(0), 1200], [X(10), 1200]], 6.8, "#8c7152", 3, dur=.8)] + [I.line([[X(k), 1188], [X(k), 1212]], 6.9 + .04 * k, "#8c7152", 2, draw=False) for k in range(11)] +
            [I.label(X(0), 1256, "0", 7.0, "#9a938a", 28), I.label(X(10), 1256, "10 years", 7.1, "#9a938a", 28, "end"),
             I.box(X(6), 1186, X(9) - X(6), 28, AMBER, r=10, at=8.4, fx="pop"), I.label((X(6) + X(9)) / 2, 1290, "6 to 9 years", 8.6, AMBER, 32)] +
            _fig(I, X(0), 1150, 110, 7.6) + _fig(I, (X(6) + X(9)) / 2, 1150, 170, 8.8)}
    # 5 · in a tropical forest, with nothing: they stopped the bleeding, managed the pain, kept infection away
    palms = [{"k": "palm", "x": x, "y": 560, "h": h, "in": 1.5} for x, h in ((120, 150), (220, 120), (780, 140), (880, 160))] + [I.line([[60, 560], [940, 560]], 1.5, "#2e3a24", 6, draw=False)]
    struck = [I.box(190, 650, 60, 110, "none", "#cbbca8", 3, 10, 2.3), I.box(205, 630, 30, 22, "#cbbca8", r=4, at=2.3), I.strike(170, 780, 270, 630, 2.5),
              I.line([[440, 760], [560, 650]], 2.8, "#c9d2d8", 10, draw=False), I.line([[420, 780], [450, 750]], 2.8, "#6b4a2e", 14, draw=False), I.strike(410, 780, 590, 630, 3.0),
              I.box(680, 680, 120, 90, "none", "#cbbca8", 3, 4, 3.3), I.line([[740, 700], [740, 750]], 3.3, NO, 6, draw=False), I.line([[715, 725], [765, 725]], 3.3, NO, 6, draw=False),
              {"k": "poly", "p": [[670, 680], [740, 630], [810, 680]], "fill": "none", "c": "#cbbca8", "w": 3, "in": 3.3}, I.strike(660, 790, 820, 630, 3.5)]
    feats = [{"k": "poly", "p": [[220, 960], [250, 1010], [256, 1040], [220, 1068], [184, 1040], [190, 1010]], "fill": "#c0442c", "c": "none", "w": 0, "curve": True, "in": 4.0},
             I.line([[170, 1090], [270, 1090]], 4.4, BONE, 6, draw=False), I.ring(220, 1020, 80, 4.5, OK, 4), I.label(220, 1150, "bleeding", 4.2, BONE, 30),
             {"k": "poly", "p": [[510, 950], [470, 1030], [500, 1030], [480, 1090], [540, 1010], [508, 1010], [530, 950]], "fill": "#e8c35a", "c": "none", "w": 0, "in": 4.9, "op": .55, "keepop": True},
             I.ring(500, 1020, 80, 5.3, OK, 4), I.label(500, 1150, "pain", 5.0, BONE, 30),
             I.ring(780, 1020, 50, 6.4, OK, 4)] + [I.dot(780 + 85 * math.cos(a), 1020 + 85 * math.sin(a), 7, "#b9d27a", 6.0 + .03 * k)
                                                   for k, a in enumerate([j * .7 for j in range(9)])] + \
            [I.label(780, 1150, "infection", 6.2, BONE, 30), I.glow(500, 1030, 380, 8.6, .3)]
    hard = {"base": "dark", "cam": [1.15, 500, 860], "els": palms + struck + feats}
    # 6 · France, 7,000 years; Borneo, 31,000: 24,000 years further back, more than four times as old
    T = lambda ya: 880 - 700 * ya / 31000
    twice = {"base": "dark", "cam": [1.12, 520, 1000], "els": [I.line([[150, 1000], [900, 1000]], .1, "#8c7152", 3), I.label(880, 1050, "today", .2, "#9a938a", 28),
             I.box(T(7000), 860, 880 - T(7000), 34, PAST, r=8, at=2.2, fx="pop"), I.label(T(7000) - 14, 888, "France", 2.4, PAST, 30, "end"),
             I.line([[T(7000), 900], [T(7000), 1000]], 2.4, PAST, 2, "inferred", .4),
             {"k": "poly", "p": [[640, 760], [700, 715], [760, 760]], "fill": "#a8865e", "c": "none", "w": 0, "in": 4.6}, I.box(652, 760, 96, 66, "#8a6a48", r=2, at=4.6), I.box(688, 790, 24, 36, "#2a1d12", r=2, at=4.6)] +
            [I.line([[780, 822 - 14 * k], [890, 822 - 14 * k]], 4.8 + .1 * k, "#7fa35a", 6, draw=False) for k in range(5)] +
            [I.box(T(31000), 1080, 880 - T(31000), 34, I.BLUE, r=8, at=9.0, fx="pop"), I.label(T(31000), 1160, "Borneo", 9.2, I.BLUE, 30, "start"),
             I.line([[T(31000), 1000], [T(31000), 1080]], 9.2, I.BLUE, 2, "inferred", .4)] +
            [I.box(880 - (880 - T(7000)) * (k + 1), 1074, 880 - T(7000), 46, "none", PAST, 3, 8, 11.3 + .25 * k, style="inferred") for k in range(4)] +
            [I.label(T(19000), 1230, "24,000 years more", 10.4, BONE, 30), I.arrow([[T(7000), 1190], [T(31000) + 4, 1190]], 10.0, BONE, 3, dur=1.2, curve=False),
             I.label(214, 1062, "×4", 12.4, PAST, 44, st="serif")]}
    # 7 · the verdict on the figure: one case; others unknown; strong evidence
    one = [I.label(500, 560, "one", .3, AMBER, 40, st="serif")] + sum([_ghost(I, x, 1220, 300, 1.6 + .2 * k, c="#8a7a66") for k, x in enumerate((180, 820))], []) + \
          I.question(180, 860, 2.4, 60) + I.question(820, 860, 2.6, 60) + [I.glow(500, 900, 300, 4.6, .6), I.label(500, 1310, "strong evidence", 5.2, OK, 32)]
    warm = [I.glow(500, 900, 420, .6, .5)]
    return remix(ep, scenes={0: hook, 2: grave, 3: cut, 4: heal, 5: hard, 6: twice}, alias={7: 0}, cams={7: [1, 500, 920]},
                 adds={1: cave + grew}, beat_adds={5: (one, None)}, line_adds={(5, 1): (warm, None)})


# ---------------------------------------------------------------- 01.06 The Shigir Idol
def shigir():
    s0 = {"base": "dark", "floor": 1180, "cam": [1.15, 500, 820], "els": idol(500, 1180, 780, .1) + [{"k": "glow", "x": 500, "y": 800, "r": 380, "kind": "lamp", "op": .3}]}
    gy = 640; pxm = 70
    bog = {"base": "section", "tod": "day", "ground": gy, "layers": [{"d": 0, "c": "#3b3020", "t": "peat", "ty": 50}, {"d": 4.4 * pxm, "c": "#5a4a36", "t": "lake clays", "ty": 60}],
           "cam": [1, 500, 860], "els": [{"k": "dim", "x1": 900, "y1": gy, "x2": 900, "y2": gy + 4 * pxm, "t": "c. 4 m", "lx": 30},
                                         {"k": "cap", "x": 500, "y": 420, "t": "1890 · gold miners in the Shigir bog", "in": .2}] +
           [{"k": "rect", "x": 200 + k * 62, "y": gy + 4 * pxm - 26 + (k % 3) * 6, "w": 52, "h": 20, "fill": "#6b4a2e", "c": "#c9a070", "sw": 1.2, "in": .5 + k * .08} for k in range(10)]}
    s1 = bog
    s2 = {"base": "dark", "floor": 1180, "cam": [1, 500, 820], "els": idol(420, 1180, 760, .1) + silhouette(720, 1180, 144, t="1.7 m", i=.5) +
          [{"k": "dim", "x1": 330, "y1": 1180, "x2": 330, "y2": 420, "t": "c. 5.3 m", "lx": -30, "in": .8}]}
    rings = [{"k": "circle", "x": 500, "y": 820, "r": 40 + k * 26, "fill": "none", "c": "#c9a070", "w": 1.6, "op": .8, "in": .1 + k * .05} for k in range(10)]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "circle", "x": 500, "y": 820, "r": 300, "fill": "#6b4a2e", "c": "#c9a070", "w": 2, "in": .1}] + rings +
          [{"k": "circle", "x": 500, "y": 820, "r": 300, "fill": "none", "c": "#9fd0ff", "w": 40, "op": .35, "in": .9},
           {"k": "label", "x": 500, "y": 1170, "t": "outer wood: soaked in preservative, dates too young", "st": "small", "c": "#cfe6ff", "in": 1.1},
           {"k": "glow", "x": 500, "y": 820, "r": 90, "kind": "lamp", "in": 1.4},
           {"k": "label", "x": 500, "y": 1210, "t": "untouched core: the true age", "st": "small", "c": GOLD, "in": 1.5}]}
    s4 = like(s0, cam=[2.2, 500, 580], add=[{"k": "label", "x": 560, "y": 520, "t": "stone adze and chisel marks, cut in green wood", "st": "small", "a": "start", "c": GOLD, "in": .5}])
    s5 = like(s0, cam=[1.6, 500, 760])
    tl, ax = timeline(-11000, -2000, [(-10000, "10,000 BCE"), (-8000, "8000"), (-6000, "6000"), (-4000, "4000"), (-2000, "2000")], "", y=980)
    tl["els"] += event(ax, -10000, "Shigir idol", y=980, row=1, c=GOLD, i=.3, sub="c. 10,000 BCE") + event(ax, -9500, "Göbekli Tepe", y=980, row=0, i=.7, sub="from c. 9500 BCE") + \
                 event(ax, -2560, "Great Pyramid", y=980, row=0, c="#c9ad85", i=1.1)
    s6 = tl
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE URALS][sfx:boom][act:wonder, setting the scene]A wooden ^giant, carved about ^*twelve* thousand years ago.",
                      "[d:tension][cam:1.12|0|0][act:impressed, building]As old as Göbekli ^Tepe. [act:the punch, delighted][tune:highfall]In ^*wood*."], cut=False),
        B("world", 1, ["[d:calm][k:1890 · SHIGIR BOG][act:storytelling, unhurried]In {1890|eighteen ninety}, gold miners pulled it from four metres of ^peat. [act:quietly vivid][tune:fall]^Ten pieces, carved with ^faces.",
                       "[d:build][go:2|0][act:building to it, wonder]Pieced together, it stood over ^*five* metres tall."]),
        B("collision", 3, ["[d:build][k:THE DATE][act:matter of fact, setting it up]Early radiocarbon tests said about ^nine and a half thousand years. [act:the detective turn, leaning in]Then a ^new team sampled the untouched ^*core* of the wood."]),
        B("cost", 3, ["[d:reveal][stamp:c. 12,000 YEARS|gold][act:the result, firm and clear][tune:fall]About ^twelve thousand years. [act:explaining, a small smile]The outer wood had been soaked in ^preservative, and that made it look ^*younger*."], cut=False),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, precise]The tool marks show it was carved in fresh, ^green wood. [sfx:hit][act:the reveal, deliberate][tune:fall]By ^hunter-gatherers. [act:flat, contrasting][tune:highfall]Not ^farmers.",
                          "[d:list][go:5|2][act:counting them off, fascinated][tune:level]Faces. [act:same rhythm][tune:level]Zigzags. [act:closing the list][tune:fall]Hands. [act:wistful wonder, slower][tune:fall]A whole ^language of symbols, we ^can't *read@present!*."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:calm authority, weighing it]^Monumental art, before ^farming. [act:the verdict, confident][tune:fall]^Strong evidence.",
                     "[d:tension][p:0.93][act:quiet wonder, a real question][tune:fall]How many ^other wooden giants simply ^*rotted* away?"]),
    ]
    return EP("shigir-idol", "01.06", "The Shigir Idol", "shigir-idol", "strong", "A wooden giant from the end of the Ice Age?", "A wooden *giant*.", beats, shots,
              "Zhilin et al. 2018, Quaternary International · Terberger, Zhilin & Savchenko 2021, Quaternary International",
              "Pulled from a Russian peat bog in 1890, the Shigir idol turned out to be about 12,000 years old: monumental art before farming.",
              ["#Archaeology", "#ShigirIdol", "#IceAge", "#AncientArt", "#History"])


def _hand(I, x, y, s, at, c):
    """A carved open hand: a palm and five fingers, as strokes."""
    out = [I.box(x - 14 * s, y - 10 * s, 28 * s, 26 * s, "none", c, 2.5, 6 * s, at)]
    for k, (dx, ln) in enumerate(((-11, 20), (-4, 26), (4, 27), (11, 22))):
        out.append(I.line([[x + dx * s, y - 10 * s], [x + dx * s, y - (10 + ln) * s]], at, c, 2.5, draw=False))
    out.append(I.line([[x - 14 * s, y + 6 * s], [x - 26 * s, y - 6 * s]], at, c, 2.5, draw=False))
    return out


def _candle(I, x, base, h, at, c="#efe6d2", flame=True):
    out = [I.box(x - 26, base - h, 52, h, c, "#fff6e6", 1.5, 6, at, fx="fill")]
    if flame:
        out += [{"k": "poly", "p": [[x, base - h - 46], [x + 12, base - h - 16], [x, base - h - 6], [x - 12, base - h - 16]], "fill": "#ffd27a", "c": "none", "w": 0, "curve": True, "in": at + .3},
                I.glow(x, base - h - 24, 50, at + .3, .9)]
    return out


def shigir_m():
    """The Shigir idol as one continuous take (see mural.py): a bog that kept wood, three grown-ups tall, a candle for radiocarbon, chisel marks, and the giants that rotted."""
    remix, I = _mur()
    ep = shigir()
    WOOD, BLUE, GOLD_ = "#c9a070", "#9fd0ff", "#f2c98e"
    # 0 · the idol; as old as Gobekli Tepe, in stone; this one in wood
    import copy
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] += [{"k": "tpillar", "x": 880, "y": 1180, "h": 300, "in": 4.6}, I.label(880, 846, "stone", 5.9, "#cbbca8", 28), I.label(500, 368, "wood", 6.6, WOOD, 30),
                  I.glow(500, 800, 300, 6.6, .5)]
    # 1 · four metres of peat: no air, so nothing rots it; kept like food in a sealed jar; ten pieces
    GY, PX = 640, 70
    air = [I.dot(x, y, 4, BLUE, round(4.0 + .02 * k, 2), op=.7) for k, (x, y) in enumerate(I.scatter(26, 80, 920, 470, 620, 3))]
    bugs = [I.dot(x, y, 5, "#b9d27a", round(5.0 + .03 * k, 2)) for k, (x, y) in enumerate(I.scatter(12, 80, 920, 560, 632, 8))]
    bog = {"base": "section", "tod": "day", "ground": GY, "layers": [{"d": 0, "c": "#3b3020", "t": ""}, {"d": 4.4 * PX, "c": "#5a4a36", "t": ""}], "cam": [1.25, 500, 760], "els": [
           I.person(220, GY, 120, .6, "#2a221b"), I.person(300, GY, 112, .7, "#2a221b"), I.line([[316, GY - 70], [350, GY - 10]], .7, "#6b4a2e", 5, draw=False),
           {"k": "dim", "x1": 900, "y1": GY, "x2": 900, "y2": GY + 4 * PX, "t": "4 m", "lx": -30, "upright": True, "in": 1.6},
           I.box(60, GY + 6, 880, 4 * PX - 12, "rgba(30,24,16,.0)", "#8a6a48", 2, 8, 2.6, style="inferred"), I.label(500, GY + 70, "peat", 2.6, "#cbbca8", 32)] + air + bugs + \
          [I.label(620, 470, "air", 4.2, BLUE, 30), I.box(150, GY + 4 * PX - 70, 700, 96, "none", AMBER, 3, 26, 7.8, fx="draw", dur=1.0), I.line([[170, GY + 4 * PX - 80], [830, GY + 4 * PX - 80]], 8.1, AMBER, 6, dur=.6)] + \
          [I.box(190 + 62 * k, GY + 4 * PX - 40 + (k % 3) * 6, 52, 20, "#6b4a2e", "#c9a070", 1.2, 3, round(8.6 + .1 * k, 2), fx="pop") for k in range(10)] + \
          [I.glow(500, GY + 4 * PX - 30, 260, 9.0, .4)]}
    # 2 · ten pieces stack into a five-metre giant: three grown-ups, head to toe
    IH = 760; FL = 1180; M2 = IH / 5.3
    seg = [I.box(470, FL - IH * (k + 1) / 10, 60, IH / 10 - 4, "#6b4a2e", "#c9a070", 1.2, 4, round(.2 + .12 * k, 2), fx="pop") for k in range(10)]
    stack = {"base": "dark", "floor": FL, "cam": [1, 500, 820], "els": seg + idol(500, FL, IH, 1.5) +
             [{"k": "dim", "x1": 400, "y1": FL, "x2": 400, "y2": FL - IH, "t": "5.3 m", "lx": -34, "in": 1.7}] +
             sum([[I.person(720, FL - 1.7 * M2 * k, 1.7 * M2, 3.0 + .4 * k, "#e8d6b8")] for k in range(3)], []) +
             [I.label(720, FL + 44, "3 × 1.7 m", 4.2, BONE, 30)]}
    # 3 · radiocarbon as a candle: alive, burning down; the outer wood said 9,500; the core said 12,000
    CX, CY, RR = 500, 640, 220
    rings = [I.oval(CX, CY, RR, RR, "#6b4a2e", WOOD, 2, 1, .1)] + [I.ring(CX, CY, 30 + 19 * k, .1 + .03 * k, "#c9a070", 1.6, dur=.3) for k in range(10)]
    log = {"base": "dark", "cam": [1, 500, 880], "els": rings + [I.dot(CX + RR - 14, CY, 12, BLUE, .4), I.glow(CX + RR - 14, CY, 50, .4, .8),
           I.label(CX + RR + 20, CY + 10, "9,500?", 1.2, BLUE, 34, "start")] +
           [I.line([[100, 1310], [900, 1310]], 2.4, "#8c7152", 2, draw=False)] + _candle(I, 250, 1310, 300, 2.6) + _candle(I, 500, 1310, 190, 6.4) + _candle(I, 750, 1310, 80, 7.2) +
           [I.arrow([[200, 1360], [800, 1360]], 6.2, "#cbbca8", 2, "inferred", 1.6, False), I.label(500, 1410, "years pass", 6.6, "#cbbca8", 28),
            I.line([[CX + RR - 14, CY], [CX, CY]], 10.4, GOLD_, 4, dur=.8), I.glow(CX, CY, 70, 11.0, .9)]}
    core = [I.label(CX, CY - RR - 30, "12,000", .4, GOLD_, 40, st="serif"), I.oval(CX, CY, RR - 6, RR - 6, "none", BLUE, 26, .45, 2.4, fx="fade"),
            I.label(CX - RR - 20, CY + 10, "preservative", 2.8, BLUE, 28, "end"), I.box(724, 1310 - 80 - 70, 52, 70, "rgba(95,168,201,.85)", "#cfe6ff", 1.5, 6, 6.7, fx="fill"),
            {"k": "poly", "p": [[750, 1114], [762, 1144], [750, 1154], [738, 1144]], "fill": "#ffd27a", "c": "none", "w": 0, "curve": True, "in": 7.0}, I.glow(750, 1136, 50, 7.0, .9),
            I.label(750, 1080, "too young", 8.6, BLUE, 28)]
    # 4 · chisel marks in green wood; hunter-gatherers, not farmers
    marks = [I.line([[476 + 10 * (k % 4), 436 + 24 * (k // 4)], [468 + 10 * (k % 4) + 20, 450 + 24 * (k // 4)]], round(.4 + .06 * k, 2), AMBER, 4, dur=.3) for k in range(12)] + \
            [{"k": "poly", "p": [[330, 520], [372, 506], [380, 540], [338, 552]], "fill": "#8a8580", "c": "#cbbca8", "w": 1.5, "in": .7}, I.line([[372, 520], [420, 468]], .7, "#6b4a2e", 6, draw=False),
             I.label(350, 600, "stone chisel", .9, BONE, 28), I.dot(612, 470, 9, "#8fd9b0", 3.0), I.dot(624, 500, 7, "#8fd9b0", 3.1), I.label(640, 560, "sap", 3.3, I.GREEN, 28, "start"),
             I.person(290, 1060, 200, 4.7, "#e8d6b8"), I.line([[260, 880], [260, 1070]], 4.8, "#8a6a48", 4, draw=False), I.tri(260, 870, 11, 0, "#cbbca8", 4.8),
             I.label(290, 830, "hunters", 4.9, BONE, 28)] + _ghost(I, 715, 1060, 200, 5.2, c="#8a7a66") + [I.strike(650, 1070, 780, 860, 5.5), I.label(715, 830, "farmers", 5.4, "#8a7a66", 28)]
    # 5 · faces, zigzags, hands: a language we can't read
    H0 = 780
    sym = [I.ring(500, 1180 - H0 * f, 46, .3 + .15 * j, GOLD_, 3, dur=.4) for j, f in enumerate((.93, .62, .3))] + \
          [I.line([[500 - 70 * .8 + j * 70 * .2, 1180 - H0 * b + (8 if j % 2 else -8)] for j in range(9)], 1.1 + .15 * k, AMBER, 4, dur=.5) for k, b in enumerate((.8, .7, .5))] + \
          _hand(I, 486, 1180 - H0 * .4, 1.0, 1.9, "#f2d9b0") + _hand(I, 514, 1180 - H0 * .2, 1.0, 2.0, "#f2d9b0") + I.question(700, 730, 4.0, 90)
    # 6 · twice as old as the Great Pyramid; and all the wooden giants that rotted away
    T = lambda ya: 880 - 700 * ya / 12000
    tl = {"base": "dark", "cam": [1.2, 520, 930], "els": [I.box(T(12000), 900, 700, 30, WOOD, r=8, at=.3, fx="pop"), I.oval(T(12000) + 30, 896, 70, 14, "#3b3020", at=.3)] +
          idol(T(12000) + 30, 886, 240, .3) + [I.label(T(12000), 960, "the idol", .5, WOOD, 30, "start"),
          I.box(T(4585), 1120, 880 - T(4585), 30, "#cbbca8", r=8, at=2.4, fx="pop"), {"k": "pyramid", "x": T(4585) + 60, "y": 1112, "w": 120, "in": 2.4},
          I.label(T(4585) - 16, 1144, "Great Pyramid", 2.6, "#cbbca8", 30, "end"), I.label(880, 1196, "today", .4, "#9a938a", 28, "end"), I.glow(T(12000) + 30, 760, 160, 1.2, .5)] +
          [I.box(880 - (880 - T(4585)) * (k + 1), 894, 880 - T(4585), 42, "none", "#cbbca8", 3, 8, 3.0 + .3 * k, style="inferred") for k in range(2)] +
          [I.label(T(9170) - 14, 870, "×2", 3.6, "#cbbca8", 40, "end", st="serif")]}
    ghosts = [I.glow(T(12000) + 30, 900, 120, 2.4, .8)] + sum([_ghost(I, x, 886, 230, 3.5 + .3 * k, c="#8a6a48", op=.6) for k, x in enumerate((420, 580, 740))], []) + I.question(580, 560, 4.6, 80)
    return remix(ep, scenes={0: s0, 1: bog, 2: stack, 3: log, 6: tl}, alias={4: 0, 5: 0}, cams={4: [1.6, 500, 700], 5: [1.6, 500, 760]},
                 beat_adds={3: (core, None), 4: (marks, None)}, line_adds={(4, 1): (sym, [1.6, 500, 760]), (5, 1): (ghosts, None)})


# ---------------------------------------------------------------- 01.08 The First Americans
LAURENTIDE = [(-140, 70), (-120, 73), (-95, 76), (-70, 76), (-60, 65), (-62, 52), (-70, 44), (-75, 41.5), (-85, 39.5), (-95, 42), (-105, 48), (-113, 50), (-118, 55), (-125, 60), (-135, 65)]
CORDILLERAN = [(-152, 62), (-138, 60.5), (-129, 56), (-123, 48.5), (-117, 47.5), (-116, 52), (-121, 57), (-132, 62), (-146, 64)]
BERINGIA = [(-179, 67), (-168, 69.5), (-160, 70.5), (-158, 66), (-163, 60), (-172, 58.5), (-179, 60)]


def first_americans():
    v = View(-178, -52, 8, 76, (30, 330, 940, 960))
    base = mapshot(v)
    ice = [{"k": "poly", "p": [v.p(*q) for q in LAURENTIDE], "fill": "rgba(235,245,255,.55)", "c": "#ffffff", "w": 1.6, "curve": True, "in": .2},
           {"k": "poly", "p": [v.p(*q) for q in CORDILLERAN], "fill": "rgba(235,245,255,.5)", "c": "#ffffff", "w": 1.4, "curve": True, "in": .2},
           {"k": "poly", "p": [v.p(*q) for q in BERINGIA], "fill": "rgba(201,173,133,.35)", "c": "#c9ad85", "w": 1.4, "style": "inferred", "curve": True, "in": .2},
           {"k": "label", "x": v.p(-95, 58)[0], "y": v.p(-95, 58)[1], "t": "ice sheets, c. 21,000 years ago", "st": "small", "c": "#1a1511", "in": .6},
           {"k": "label", "x": v.p(-168, 64)[0], "y": v.p(-168, 64)[1] + 60, "t": "Beringia", "st": "ital", "c": "#c9ad85", "in": .6}]
    ws = v.p(-106.33, 32.78)
    s0 = {"base": "plan", "bg": "#b7a17e", "north": False, "cam": [1, 500, 860], "els": footprints(180, 1140, 820, 560, n=12, s=1.6, i=.1) + [{"k": "cap", "x": 500, "y": 1230, "t": "White Sands, New Mexico", "c": "#2a1d12", "in": .3}]}
    s1 = like(base, add=[{"k": "pin", "x": v.p(-103, 34.4)[0], "y": v.p(-103, 34.4)[1], "t": "Clovis, New Mexico", "in": .3}] + spear_point(800, 1220, 150, i=.6))
    s2 = like(s1, add=[{"k": "cap", "x": 500, "y": 330, "t": "'Clovis first' · the textbook for 60 years", "in": .2}])
    s3 = like(base, add=[{"k": "pin", "x": v.p(-73.2, -41.5)[0], "y": v.p(-73.2, -41.5)[1], "t": "Monte Verde, Chile", "in": .3},
                         {"k": "label", "x": 500, "y": 1260, "t": "c. 14,500 years · accepted by the sceptics in 1997", "st": "small", "in": .8}], cam=[1, 500, 860])
    s3["els"][0] = {"k": "map", "land": View(-178, -52, -48, 76, (30, 300, 940, 1000)).land(), "in": -1}
    v3 = View(-178, -52, -48, 76, (30, 300, 940, 1000)); mv = v3.p(-73.2, -41.5)
    s3["els"][1] = {"k": "pin", "x": mv[0], "y": mv[1], "t": "Monte Verde, Chile", "a": "end", "lx": -18, "in": .3}
    s4 = like(s0, cam=[1.3, 500, 820], add=[{"k": "label", "x": 500, "y": 1280, "t": "tracks of children and teenagers beside an ancient lake", "st": "small", "c": "#2a1d12", "in": .5}])
    s5 = like(base, add=ice + [{"k": "pin", "x": ws[0], "y": ws[1], "t": "White Sands · c. 23,000–21,000 yrs", "c": GOLD, "a": "end", "lx": -18, "in": 1.0}])
    tl, ax = timeline(-25000, -12000, [(-24000, "24,000 yrs ago"), (-20000, "20,000"), (-16000, "16,000"), (-12000, "12,000")], "", y=980)
    tl["els"] += event(ax, -23000, "White Sands", y=980, row=1, c=GOLD, i=.3) + event(ax, -14500, "Monte Verde", y=980, row=0, i=.7) + event(ax, -13000, "Clovis", y=980, row=1, c="#c9ad85", i=1.1)
    s6 = tl
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:WHITE SANDS · NEW MEXICO][sfx:boom][act:hushed, setting the scene][tune:level]Human ^footprints in New Mexico... [act:wonder, slower][tune:fall]from the depths of the last ^Ice Age."], cut=False),
        B("world", 1, ["[d:calm][k:CLOVIS FIRST][act:plain storytelling, the old view]For sixty years, ^textbooks said the first Americans arrived about ^thirteen thousand years ago. [act:lighter, an aside]The ^Clovis people, with their ^fluted spear points.",
                       "[d:build][go:2|0][act:wry, a small smile]Anyone who claimed an ^older site had a ^*fight* on their hands."]),
        B("collision", 3, ["[d:build][k:MONTE VERDE][act:storytelling, admiring persistence]In Chile, Tom Dillehay spent ^twenty years defending a camp about ^fourteen and a half thousand years old.",
                           "[d:reveal][sfx:hit][act:building, a touch of suspense][tune:level]In {1997|nineteen ninety-seven}, the ^sceptics visited... [act:the payoff, warm][tune:fall]and ^*agreed*."]),
        B("cost", 4, ["[d:build][k:WHITE SANDS][act:tender, vivid]Then, in New Mexico: footprints of ^children and teenagers, beside an ancient ^lake.",
                      "[d:list][act:firm, confident][tune:fall]Dated ^four different ways. [stamp:c. 23,000–21,000 YEARS|gold][act:the number, slow and clear][tune:fall]About ^twenty-three to ^twenty-one thousand years old."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:leaning in, painting it]That's when ice sheets still covered most of ^Canada. [sfx:shimmer][act:the reveal, slower][tune:fall]So people were ^already here, ^*south* of the ice."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Clovis ^first? [act:flat, final][tune:highfall]Ruled ^out. [act:the next question, even][tune:rise]People here by ^twenty-one thousand years ago? [act:the verdict, confident][tune:fall]^*Strong* evidence.",
                     "[d:tension][p:0.93][act:plain, letting it land]The textbook was off by ^eight thousand years. [gap:0.4][act:curious, a playful challenge][tune:fall]What ^*else* is?"]),
    ]
    return EP("first-americans", "01.08", "The First Americans", "first-americans", "strong", "When did people reach the Americas?", "Footprints from the *Ice Age*.", beats, shots,
              "Bennett et al. 2021, Science · Pigati et al. 2023, Science · Holliday et al. 2025 · Dillehay 1997 · Waters et al. 2020, Science Advances",
              "For decades the textbooks said 'Clovis first'. Footprints at White Sands, dated four ways, now put people in North America at least 21,000 years ago.",
              ["#FirstAmericans", "#Archaeology", "#IceAge", "#WhiteSands", "#History"])


def _axis_ya(I, X, y, at, ticks=(25000, 20000, 10000)):
    """A years-ago axis, older to the left."""
    return [I.line([[X(25000), y], [X(10000), y]], at, "#8c7152", 3, dur=.8)] + \
           [e for t in ticks for e in (I.line([[X(t), y - 10], [X(t), y + 10]], at, "#8c7152", 2, draw=False), I.label(X(t), y + 48, f"{t:,}", at + .2, "#9a938a", 28))] + \
           [I.label(X(25000), y + 92, "years ago", at + .3, "#9a938a", 28, "start")]


def _wall(I, x, y0, y1, at):
    out = [I.box(x - 18, y0, 36, y1 - y0, "#b9a47c", "#e8d6b0", 2, 3, at, fx="fill")]
    out += [I.line([[x - 18, yy], [x + 18, yy]], at, "#8a7356", 1.5, draw=False) for yy in range(int(y0) + 30, int(y1), 30)]
    return out


def first_americans_m():
    """The first Americans as one continuous take (see mural.py): a wall at 13,000 years, the first crack, prints pressed in lake mud, and the ice."""
    remix, I = _mur()
    ep = first_americans()
    SAND, ICE, GOLD_, OK = "#e8c878", "#cfe6ff", "#f2c98e", I.GREEN
    v = View(-178, -52, 8, 76, (30, 330, 940, 960))
    cp = v.p(-103, 34.4)
    # 1 · Clovis: a fluted point; the flute takes the shaft
    import copy
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") != "poly"] + spear_point(230, 1180, 220, i=6.4) + \
        [I.label(cp[0] + 18, cp[1] + 44, "13,000 years", 2.5, AMBER, 30, "start"), I.line([[230, 1172], [230, 1100]], 8.4, AMBER, 6, dur=.6), I.glow(230, 1130, 70, 8.4, .8),
         I.label(310, 1110, "flute", 8.6, AMBER, 30, "start"), I.line([[230, 1186], [230, 1420]], 10.0, "#8a6a48", 14, dur=.6),
         I.line([[214, 1196], [246, 1212]], 10.4, "#d9c9a8", 4, draw=False), I.line([[214, 1214], [246, 1230]], 10.5, "#d9c9a8", 4, draw=False), I.label(270, 1340, "shaft", 10.6, "#cbbca8", 28, "start")]
    # 2 · the wall at 13,000 years: older dates bounce off it; then a camp in Chile, the sceptics, the first crack
    X = lambda ya: round(120 + (25000 - ya) / 15000 * 760, 1)
    AY = 1150; WX = X(13000)
    bounce = []
    for k, (ya, y) in enumerate(((20000, 880), (17000, 950), (22500, 1020))):
        bounce += [I.dot(X(ya), y, 13, "#cbbca8", .7 + .3 * k), I.line([[X(ya) + 14, y], [WX - 22, y]], 4.7 + .3 * k, "#cbbca8", 3, "inferred", .5),
                   I.arrow([[WX - 22, y], [WX - 90, y + 24], [X(ya) + 60, y + 34]], 5.1 + .3 * k, I.RED, 3, "claimed", .6)]
    wall = {"base": "dark", "cam": [1.12, 500, 980], "els": _axis_ya(I, X, AY, .3) + _wall(I, WX, 800, AY, 3.4) + [I.label(WX, 780, "13,000", 3.3, AMBER, 32)] + bounce}
    vm = View(-130, -30, -56, 60, (300, 280, 400, 400))
    mv, cl = vm.p(-73.2, -41.5), vm.p(-103, 34.4)
    camp = [{"k": "group", "clip": [300, 280, 400, 400, 16], "bg": "#16303d", "in": .2, "els": [{"k": "map", "land": vm.land()},
             {"k": "pin", "x": cl[0], "y": cl[1], "t": "Clovis", "c": AMBER, "a": "end", "lx": -18}, {"k": "pin", "x": mv[0], "y": mv[1], "t": "Chile", "c": SAND}]},
            I.line([cl, [cl[0] + 60, (cl[1] + mv[1]) / 2], mv], 8.2, SAND, 3, "inferred", 1.0, True),
            {"k": "poly", "p": [[X(14500) - 34, AY], [X(14500), AY - 56], [X(14500) + 34, AY]], "fill": "#8a6a48", "c": SAND, "w": 2, "in": 4.0, "fx": "pop"},
            I.glow(X(14500), AY - 30, 80, 4.0, .7), I.label(X(14500), AY + 48, "14,500", 4.4, SAND, 30)] + I.question(X(14500), AY - 80, 6.2, 60)
    crack = [I.person(X(14500) - 140 + 30 * k, AY, 70, 1.0 + .2 * k, "#cbbca8") for k in range(3)] + [I.ring(X(14500), AY - 28, 52, 2.3, OK, 4),
             I.line([[WX + 4, 800], [WX - 8, 860], [WX + 8, 900], [WX - 6, 960], [WX + 6, 1010]], 3.9, "#fff6e6", 4, dur=.6), I.glow(WX, 900, 90, 3.9, .8)]
    # 4 · children at an ancient lake; the prints are pressed between layers of mud, dated above and below
    SH = 760
    lake = {"base": "sky", "tod": "day", "ground": SH, "ridges": [{"y": SH - 40, "a": 60, "c": "#6a6f7a", "seed": 4}], "sun": [800, 520, 26], "cam": [1.15, 500, 720], "els": [
            {"k": "water", "y": SH - 2, "x0": 560, "x1": 1100, "h": 30, "op": .9, "in": 3.5}] +
            [I.person(180 + 90 * k, SH, h, 2.2 + .25 * k, "#3a2f26") for k, h in enumerate((96, 120, 84))] +
            [I.oval(150 + 46 * k, SH + 10, 12, 5, "#3a2c1e", at=round(4.3 + .15 * k, 2)) for k in range(9)] +
            [I.box(60, SH + 4, 880, 80, "#8a7356", r=0, at=.1), I.box(60, SH + 84, 880, 90, "#9c8466", r=0, at=.1), I.box(60, SH + 174, 880, 90, "#7a6248", r=0, at=.1),
             I.box(60, SH + 264, 880, 90, "#a8917a", r=0, at=.1), I.box(60, SH + 354, 880, 120, "#6e5a44", r=0, at=.1)]}
    PY = SH + 174
    dated = [I.line([[60, PY], [940, PY]], 1.3, GOLD_, 4, dur=1.0)] + [I.oval(180 + 70 * k, PY + 6, 18, 7, "#2a1d12", at=round(1.4 + .08 * k, 2)) for k in range(10)] + \
            [I.label(500, PY + 46, "the prints", 2.0, GOLD_, 30)] + \
            [I.dot(x, y, 12, c, .3 + .2 * j) for j, (x, y, c) in enumerate(((240, SH + 130, I.BLUE), (720, SH + 120, OK), (300, SH + 300, I.LILAC), (780, SH + 310, AMBER)))] + \
            [I.glow(x, y, 50, .3 + .2 * j, .8) for j, (x, y) in enumerate(((240, SH + 130), (720, SH + 120), (300, SH + 300), (780, SH + 310)))] + \
            [I.arrow([[880, SH + 40], [880, PY - 12]], 4.8, ICE, 3, dur=.5, curve=False), I.arrow([[880, SH + 440], [880, PY + 12]], 5.2, ICE, 3, dur=.5, curve=False),
             I.label(860, SH + 70, "younger", 4.9, ICE, 28, "end"), I.label(860, SH + 430, "older", 5.3, ICE, 28, "end")]
    # 5 · the ice over Canada; people already south of it
    south = [I.glow(*v.p(-106.33, 32.78), 120, 6.6, .8)] + [I.person(v.p(-106.33, 32.78)[0] - 20 + 22 * k, v.p(-106.33, 32.78)[1] + 70, 46, 6.8 + .15 * k, GOLD_) for k in range(3)]
    # 6 · the verdict: Clovis first struck; people by 21,000 years ago; 8,000 years, some 300 generations, missed
    verdict = {"base": "dark", "cam": [1, 500, 920], "els": _axis_ya(I, X, AY, .1) + _wall(I, WX, 800, AY, .1) + [I.label(WX, 780, "Clovis first", .2, AMBER, 30),
               I.strike(WX - 70, 820, WX + 70, 1120, 1.6, I.RED, 7), I.box(X(23000), AY - 40, X(21000) - X(23000), 40, GOLD_, r=8, at=3.2, fx="pop"),
               I.label((X(23000) + X(21000)) / 2, AY - 60, "White Sands", 3.4, GOLD_, 30), I.glow((X(23000) + X(21000)) / 2, AY - 20, 120, 6.3, .7)]}
    gens = [I.dot(X(21000) + 12 + 13.3 * (k % 30), AY + 160 + 13 * (k // 30), 4, GOLD_, round(.4 + .004 * k, 3), op=.85) for k in range(300)] + \
           [I.arrow([[X(21000), AY + 130], [WX, AY + 130]], 4.0, BONE, 3, dur=.8, curve=False), I.arrow([[WX, AY + 130], [X(21000), AY + 130]], 4.0, BONE, 3, dur=.8, curve=False),
            I.label((X(21000) + WX) / 2, AY + 300, "8,000 years", 4.3, BONE, 30), I.label((X(21000) + WX) / 2, AY + 340, "~300 generations", 1.6, GOLD_, 28)] + I.question(800, 700, 5.6, 80)
    return remix(ep, scenes={1: s1, 2: wall, 4: lake, 6: verdict}, alias={3: 2}, cams={3: [1, 500, 760]},
                 adds={5: south}, beat_adds={2: (camp, None)}, line_adds={(2, 1): (crack, [1, 500, 900]), (3, 1): (dated, [1.1, 500, 1000]), (5, 1): (gens, [1, 500, 1000])})


# ---------------------------------------------------------------- 01.09 Old Copper
SUPERIOR = [(-92.1, 46.75), (-91.1, 47.2), (-89.6, 48.0), (-89.2, 48.4), (-88.2, 48.9), (-86.6, 48.75), (-85.0, 47.95), (-84.6, 47.3), (-84.6, 46.5), (-85.4, 46.7),
            (-86.6, 46.45), (-87.4, 46.55), (-88.0, 47.0), (-87.8, 47.45), (-88.4, 47.4), (-88.9, 47.0), (-89.4, 46.85), (-90.9, 46.6)]


def old_copper():
    v = View(-93, -83.5, 45.4, 49.6, (40, 360, 920, 820))
    lake = {"k": "poly", "p": [v.p(*q) for q in SUPERIOR], "fill": "rgba(29,58,74,.95)", "c": "#9fd0ff", "w": 1.6, "curve": True}
    base = {"base": "plan", "bg": "#2f3a2c", "north": [900, 330], "cam": [1, 500, 860], "els": [lake, {"k": "label", "x": v.p(-87.2, 47.9)[0], "y": v.p(-87.2, 47.9)[1], "t": "Lake Superior", "st": "ital", "c": "#9fc4d8"}]}
    kp = v.p(-88.3, 47.2); ir = v.p(-88.9, 48.0)
    pits = [{"k": "circle", "x": kp[0] + (k % 7) * 12 - 40, "y": kp[1] + (k // 7) * 12 - 20, "r": 3.5, "fill": "#d9894a", "c": "none", "w": 0, "in": .3 + k * .02} for k in range(28)] + \
           [{"k": "circle", "x": ir[0] + (k % 6) * 10 - 30, "y": ir[1] + (k // 6) * 10 - 10, "r": 3, "fill": "#d9894a", "c": "none", "w": 0, "in": .6 + k * .02} for k in range(12)]
    s0 = like(base, cam=[1.25, 500, 820], add=pits + [{"k": "cap", "x": 500, "y": 330, "t": "a billion pounds of copper?", "c": "#f4b27a", "in": .8}])
    s1 = like(base, add=pits + [{"k": "label", "x": kp[0] + 10, "y": kp[1] + 60, "t": "Keweenaw pits", "st": "small", "in": .8}, {"k": "label", "x": ir[0], "y": ir[1] - 34, "t": "Isle Royale", "st": "small", "in": .9}])
    tools = spear_point(300, 1020, 220, c="url(#k-copper)", i=.2) + spear_point(500, 1020, 260, c="url(#k-copper)", i=.4) + spear_point(700, 1020, 200, c="url(#k-copper)", i=.6) + \
            [{"k": "circle", "x": 500, "y": 700, "r": 70, "fill": "#8c8278", "c": "#d9ccb4", "w": 2, "in": .8}, {"k": "line", "p": [[430, 700], [570, 700]], "c": "#5a5048", "w": 5, "in": .8},
             {"k": "label", "x": 500, "y": 600, "t": "grooved stone hammer", "st": "small", "in": 1.0}, {"k": "label", "x": 500, "y": 1080, "t": "cold-hammered native copper", "st": "small", "c": "#f4b27a", "in": 1.1}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": tools}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 480, "t": "the 1961 calculation", "in": .1},
          {"k": "title", "y": 640, "t": "pit size?", "st": "serif", "in": .3, "c": GOLD}, {"k": "title", "y": 740, "t": "× ore grade?", "st": "serif", "in": .6, "c": GOLD},
          {"k": "title", "y": 840, "t": "× number of pits?", "st": "serif", "in": .9, "c": GOLD}, {"k": "title", "y": 980, "t": "none of them measured", "st": "ital", "in": 1.4, "c": RED}]}
    core = [{"k": "rect", "x": 440, "y": 420, "w": 120, "h": 800, "fill": "#4a3c2e", "c": "#c9ad85", "sw": 1.6, "in": .1}] + \
           [{"k": "rect", "x": 440, "y": 420 + k * 40, "w": 120, "h": 40, "fill": ["#5a4a38", "#4a3c2e", "#3e3226"][k % 3], "c": "none", "sw": 0, "in": .1} for k in range(20)] + \
           [{"k": "line", "p": [[600, 420 + k * 40 + 20] for k in range(20)][::1], "c": "#f4b27a", "w": 2}]
    peaks = [[600 + (60 if k in (11, 12, 14, 15) else 10 + (k % 3) * 6), 440 + k * 40] for k in range(20)]
    core[-1] = {"k": "line", "p": peaks, "c": "#f4b27a", "w": 2.4, "in": .6, "fx": "draw"}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": core + [{"k": "label", "x": 700, "y": 900, "t": "lead from mining, in pulses", "st": "small", "a": "start", "c": "#f4b27a", "in": 1.2},
          {"k": "cap", "x": 500, "y": 370, "t": "lake mud, layer by layer", "in": .2}]}
    tl, ax = timeline(-10000, 0, [(-10000, "10,000 yrs ago"), (-7500, "7,500"), (-5000, "5,000"), (-2500, "2,500"), (0, "today")], "", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-9500), "x1": ax.x(-3000), "y": 880, "h": 18, "c": "#d9894a", "t": "copper tools", "in": .3},
                  {"k": "band", "x0": ax.x(-7000), "x1": ax.x(-5000), "y": 800, "h": 12, "c": "#f4b27a", "t": "peak", "in": .6},
                  {"k": "band", "x0": ax.x(-3000), "x1": ax.x(0), "y": 720, "h": 12, "c": "#8c8278", "t": "back to stone", "in": 1.0}]
    s5 = tl
    s6 = like(s1, cam=[1.2, 500, 820])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:LAKE SUPERIOR][sfx:boom][act:telling a tall tale, intrigued][tune:level]Some say ancient miners dug a ^*billion* pounds of copper out of Lake Superior...",
                      "[d:tension][act:the legend's punchline, hushed][tune:fall]and it ^*vanished*."], cut=False),
        B("world", 1, ["[d:calm][k:THE OLD COPPER CULTURE][act:firm, grounding it][tune:fall]The mining is ^real. [act:storytelling, admiring]At least nine and a half thousand years ago, ^hunter-gatherers here were hammering pure copper into ^tools.",
                       "[d:list][go:2|0][sfx:shimmer][act:wonder, building]Some of the ^oldest metalwork on Earth. [act:counting them off][tune:level]Thousands of ^pits. [act:same rhythm, landing it][tune:fall]Thousands of stone ^hammers."]),
        B("collision", 3, ["[d:build][k:THE NUMBER][act:curious, turning to the claim][tune:rise]And the ^billion pounds? [act:matter of fact]It comes from a {1961|nineteen sixty-one} ^book. [act:walking through the sum, deliberate][tune:fall]Pit ^size, times ore ^grade, times ^number@count of pits.",
                           "[d:reveal][sfx:hit][gap:0.4][act:quiet, pointed][tune:fall]^None of the three was ever ^*measured*."]),
        B("cost", 4, ["[d:build][k:WHAT WE CAN COUNT][act:solid, reassuring]About twenty ^thousand copper objects@noun, in Wisconsin ^alone. [act:fascinated, explaining]And lake ^mud that records@verb! mining in ^pulses, over thousands of years."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:the surprise, gentle][tune:fall]Then, about three thousand years ago, they mostly went ^*back* to stone.",
                          "[d:wonder][sfx:shimmer][act:wonder, slowly][tune:level]A ^metal age... [act:quiet, thoughtful][tune:fall]that people ^*chose* to leave."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Ancient copper ^mining? [act:firm, plain][tune:fall]^Established. [act:the next question, even][tune:rise]A vanished ^billion pounds? [act:the verdict, level-headed][tune:fall]^Never measured.",
                     "[d:tension][p:0.93][act:encouraging, practical][tune:level]Count the pits ^properly... [act:the last word, quiet and certain][tune:fall]and we'll ^*know*."]),
    ]
    return EP("old-copper", "01.09", "Old Copper", "old-copper", "unsupported", "Did a billion pounds of copper vanish?", "A *billion* pounds?", beats, shots,
              "Pompeani et al. 2021, Scientific Reports · Pompeani et al. 2013 · Bebber et al. 2019 · Drier & Du Temple 1961",
              "Lake Superior's Old Copper culture made some of the world's oldest metal tools. The billion-pound figure was never measured.",
              ["#Archaeology", "#OldCopper", "#LakeSuperior", "#NativeAmerican", "#History"])


def _hammer(I, x, y, s, at, c="#8c8278"):
    """A grooved stone hammer, lying."""
    return [I.oval(x, y, 34 * s, 22 * s, c, "#d9ccb4", 1.5, 1, at), I.line([[x - 4 * s, y - 22 * s], [x - 4 * s, y + 22 * s]], at, "#5a5048", 3 * s, draw=False)]


def old_copper_m():
    """Old Copper as one continuous take (see mural.py): pure copper hammered cold, a sum of three guesses, a diary of lake mud, and a metal age left behind."""
    remix, I = _mur()
    ep = old_copper()
    CU, CU2, NO = "#d9894a", "#f4b27a", I.RED
    v = View(-93, -83.5, 45.4, 49.6, (40, 360, 920, 820))
    kp, ir = v.p(-88.3, 47.2), v.p(-88.9, 48.0)
    # 0 · the lake and its pits; the claimed billion pounds, a dotted heap that vanished
    import copy
    s0 = copy.deepcopy(ep["shots"][0])
    heap = [{"k": "poly", "p": [[700, 690], [900, 690], [840, 590], [760, 590]], "fill": "rgba(217,137,74,.12)", "c": CU2, "w": 3, "style": "claimed", "in": 1.6},
            {"k": "poly", "p": [[760, 590], [840, 590], [800, 540]], "fill": "rgba(217,137,74,.12)", "c": CU2, "w": 3, "style": "claimed", "in": 1.6},
            I.label(870, 762, "a billion pounds?", 1.9, CU2, 28, "end")] + I.question(800, 520, 7.0, 70)
    s0["els"] = [e for e in s0["els"] if e.get("k") != "cap"] + heap
    # 1 · real mining: the pits; copper comes out of the rock pure; no furnace
    real = [I.label(kp[0] + 10, kp[1] + 60, "Keweenaw pits", .6, BONE, 28), I.label(ir[0], ir[1] - 34, "Isle Royale", .8, BONE, 28),
            I.box(110, 1110, 780, 300, "#14110e", "#8a6a48", 2, 14, 5.6, op=.94),
            {"k": "poly", "p": [[170, 1360], [200, 1200], [300, 1150], [420, 1170], [470, 1260], [440, 1360]], "fill": "#6e6a64", "c": "#b9b2a6", "w": 2, "curve": True, "in": 5.8},
            I.line([[220, 1300], [280, 1240], [330, 1260], [400, 1200]], 8.6, CU, 7, dur=.6, curve=True), I.line([[250, 1340], [320, 1310], [420, 1320]], 8.8, CU, 5, dur=.5, curve=True),
            I.oval(350, 1220, 18, 12, CU2, at=9.0), I.glow(330, 1260, 90, 9.0, .7), I.label(310, 1396, "pure copper", 8.4, CU2, 28),
            {"k": "poly", "p": [[600, 1340], [610, 1220], [680, 1170], [750, 1220], [760, 1340]], "fill": "#4a3a2c", "c": "#8a6a48", "w": 2, "curve": True, "in": 9.9},
            I.glow(680, 1290, 60, 9.9, .8, "red"), I.strike(580, 1360, 780, 1160, 10.3), I.label(680, 1396, "no furnace", 10.3, BONE, 28)]
    # 2 · hammered cold: lump, slab, point; thousands of pits, thousands of hammers
    stages = [I.oval(200, 640, 46, 34, CU, "#f4b27a", 2, 1, .3), {"k": "poly", "p": [[400, 670], [560, 660], [570, 690], [396, 700]], "fill": CU, "c": CU2, "w": 2, "in": 1.6}] + \
             spear_point(780, 720, 220, c="url(#k-copper)", i=2.5) + \
             [I.arrow([[270, 660], [360, 660]], 1.2, AMBER, 3, dur=.4, curve=False), I.arrow([[600, 660], [690, 660]], 2.2, AMBER, 3, dur=.4, curve=False)] + \
             _hammer(I, 200, 520, 1.3, .5) + [I.line([[170, 556], [176, 590]], .9, BONE, 2, draw=False), I.line([[230, 556], [224, 590]], .9, BONE, 2, draw=False), I.glow(200, 610, 60, .9, .8)]
    pits = [I.oval(170 + 34 * (k % 10), 940 + 34 * (k // 10), 11, 8, "#2a1d12", "#d9894a", 1.5, 1, round(5.4 + .01 * k, 2)) for k in range(60)]
    hams = sum([_hammer(I, 560 + 36 * (k % 10), 940 + 34 * (k // 10), .42, round(6.4 + .01 * k, 2)) for k in range(60)], [])
    hammer = {"base": "dark", "cam": [1.15, 500, 860], "els": stages + pits + hams + [I.label(320, 1180, "thousands of pits", 5.8, CU2, 28), I.label(720, 1180, "of hammers", 6.8, BONE, 28)]}
    # 3 · the 1961 sum: pit size × ore grade × number of pits; none measured; double each guess, the answer is eight times
    book = [I.box(420, 330, 160, 110, "#5a4330", "#c9a070", 2, 6, 1.6), I.line([[500, 334], [500, 436]], 1.6, "#c9a070", 2, draw=False), I.label(500, 480, "1961", 1.8, AMBER, 34, st="serif")]
    pit = [I.box(110, 600, 120, 90, "#2a1d12", CU2, 2, 4, 2.4), I.line([[100, 600], [240, 600]], 2.4, "#8a6a48", 4, draw=False), I.label(170, 740, "pit size", 2.5, BONE, 28)]
    ore = [{"k": "poly", "p": [[300, 690], [310, 610], [370, 586], [440, 610], [450, 690]], "fill": "#6e6a64", "c": "#b9b2a6", "w": 2, "curve": True, "in": 2.9},
           I.line([[330, 660], [380, 620], [420, 640]], 2.9, CU, 6, draw=False), I.label(375, 740, "ore grade", 3.0, BONE, 28), I.glow(375, 640, 80, 5.6, .8)]
    cnt = [I.oval(520 + 30 * k, 640, 11, 8, "#2a1d12", CU2, 1.5, 1, round(3.5 + .05 * k, 2)) for k in range(4)] + [I.label(580, 740, "number", 3.7, BONE, 28)]
    ops = [I.label(270, 660, "×", 2.8, BONE, 44, st="serif"), I.label(485, 660, "×", 3.3, BONE, 44, st="serif"), I.label(680, 660, "=", 4.0, BONE, 44, st="serif"),
           {"k": "poly", "p": [[720, 700], [920, 700], [860, 600], [780, 600]], "fill": "rgba(217,137,74,.12)", "c": CU2, "w": 3, "style": "claimed", "in": 4.1},
           I.label(820, 740, "a billion lb", 4.2, CU2, 28)]
    jar = lambda x, y, f, at: [I.box(x - 26, y - 70, 52, 70, "none", "#cfe6ff", 2.5, 10, at)] + ([I.box(x - 23, y - 70 * f + 2, 46, 70 * f - 5, "#e8b87a", r=8, at=at + .2, fx="fill")] if f else [])
    jars = jar(170, 920, .9, 8.1) + jar(375, 920, .45, 8.9) + sum([jar(540 + 50 * k, 920, .9, 9.9 + .1 * k) for k in range(3)], [])
    total = {"base": "dark", "cam": [1, 500, 880], "els": book + pit + ore + cnt + ops + jars}
    Q = [I.box(x0, 570, w, 200, "none", I.LILAC, 3, 10, .3 + .3 * k, style="claimed") for k, (x0, w) in enumerate(((90, 160), (290, 170), (500, 160)))] + \
        [I.label(x, 560, "?", .4 + .3 * k, I.LILAC, 40, st="serif") for k, x in enumerate((170, 375, 580))]
    cube = lambda x, y, s, at, c: [{"k": "poly", "p": [[x, y], [x + s, y], [x + s, y - s], [x, y - s]], "fill": c, "c": "#fff6e6", "w": 1.5, "in": at},
                                   {"k": "poly", "p": [[x, y - s], [x + s, y - s], [x + s * 1.4, y - s * 1.35], [x + s * .4, y - s * 1.35]], "fill": "#f4c89a", "c": "#fff6e6", "w": 1.5, "in": at},
                                   {"k": "poly", "p": [[x + s, y], [x + s * 1.4, y - s * .35], [x + s * 1.4, y - s * 1.35], [x + s, y - s]], "fill": "#a8622f", "c": "#fff6e6", "w": 1.5, "in": at}]
    eight = cube(220, 1300, 70, 1.7, CU) + [I.label(255, 1350, "one guess", 1.8, BONE, 28)] + \
            [I.label(x, 1220, "×2", 2.3 + .15 * k, NO, 34, st="serif") for k, x in enumerate((380, 440, 500))] + \
            sum([cube(560 + 70 * (k % 2) + 28 * (k // 4), 1300 - 70 * ((k // 2) % 2) - 25 * (k // 4), 70, round(3.4 + .08 * j, 2), CU) for j, k in enumerate((4, 5, 6, 7, 0, 1, 2, 3))], []) + \
            [I.label(680, 1350, "8 times", 3.9, NO, 30)]
    # 4 · what we can count: 20,000 objects (each dot 100); the lake's diary of mud, with lead at the busy times
    objs = [I.dot(220 + 28 * (k % 20), 340 + 28 * (k // 20), 9, CU, round(1.3 + .004 * k, 3)) for k in range(200)] + \
           [I.label(500, 664, "20,000 objects", 2.4, CU2, 32), I.label(500, 710, "each dot: 100", 2.7, "#cbbca8", 28)]
    layers = [I.box(140, 1300 - 50 * (k + 1), 720, 48, ["#5a4a38", "#4a3c2e", "#665440", "#3e3226"][k % 4], r=2, at=round(5.2 + .18 * k, 2), fx="fill") for k in range(8)]
    lead = [I.box(680, 1300 - 50 * (k + 1) + 6, 60, 36, CU2, r=4, at=9.3 + .2 * j, fx="pop") for j, k in enumerate((2, 3, 5))]
    mud = {"base": "dark", "cam": [1, 500, 860], "els": objs + [{"k": "water", "y": 760, "x0": 140, "x1": 860, "h": 140, "op": .85, "in": 3.0}] + layers +
           [I.box(680, 900, 60, 400, "none", "#cfe6ff", 2, 6, 8.0, fx="draw", dur=.8)] + lead +
           [I.glow(710, 1100, 140, 9.8, .5), I.label(770, 1150, "lead", 9.0, CU2, 30, "start"), I.label(150, 1340, "older", 7.0, "#9a938a", 28, "start"),
            I.label(150, 945, "newer", 7.2, "#9a938a", 28, "start")]}
    # 5 · copper for some 6,500 years, then mostly back to stone
    T = lambda ya: 140 + 720 * (10000 - ya) / 10000
    back = {"base": "dark", "cam": [1.15, 500, 1000], "els": [I.line([[T(10000), 1100], [T(0), 1100]], .1, "#8c7152", 3)] +
            [I.label(T(t), 1150, lab, .2, "#9a938a", 28) for t, lab in ((10000, "10,000"), (5000, "5,000"), (0, "today"))] +
            [I.label(T(10000), 1194, "years ago", .3, "#9a938a", 28, "start"),
             I.box(T(9500), 1040, T(3000) - T(9500), 30, CU, r=10, at=.4, fx="pop"), I.box(T(7000), 1030, T(5000) - T(7000), 50, CU2, r=12, at=.8, fx="pop")] +
            spear_point(T(6000), 990, 150, c="url(#k-copper)", i=.6) +
            [I.box(T(3000), 1046, T(0) - T(3000), 20, "#8c8278", r=8, at=3.2, fx="pop")] + spear_point(T(1500), 1000, 120, i=3.4) +
            [I.arrow([[T(3300), 860], [T(3000), 940], [T(2600), 960]], 3.0, BONE, 3, dur=.6)] + I.question(T(3000), 800, 4.9, 70)}
    span = [I.arrow([[T(9500), 1260], [T(3000), 1260]], 2.5, CU2, 3, dur=.8, curve=False), I.arrow([[T(3000), 1260], [T(9500), 1260]], 2.5, CU2, 3, dur=.8, curve=False),
            I.label((T(9500) + T(3000)) / 2, 1310, "6,500 years of copper", 3.0, CU2, 30)]
    # 6 · the verdict: the mining is established; the billion never measured; count, measure, test
    settle = [I.ring(kp[0], kp[1], 90, 1.7, I.GREEN, 4), I.label(kp[0], kp[1] + 140, "established", 1.9, I.GREEN, 30), I.label(870, 810, "never measured", 4.3, I.LILAC, 28, "end")]
    count = [I.ring(kp[0] + (k % 7) * 12 - 40, kp[1] + (k // 7) * 12 - 20, 9, round(.3 + .03 * k, 2), BONE, 2, dur=.3) for k in range(0, 28, 3)] + \
            [I.line([[kp[0] - 60, kp[1] + 40], [kp[0] + 60, kp[1] + 40]], 1.5, AMBER, 3, dur=.4), I.glow(kp[0], kp[1], 100, 3.4, .6)]
    return remix(ep, scenes={0: s0, 2: hammer, 3: total, 4: mud, 5: back}, alias={1: 0, 6: 0}, cams={1: [1, 500, 860], 6: [1.1, 520, 900]},
                 beat_adds={1: (real, [1, 500, 900]), 5: (settle, None)}, line_adds={(2, 1): (Q + eight, [1, 500, 940]), (4, 1): (span, None), (5, 1): (count, None)})


# ---------------------------------------------------------------- 01.10 The Ledger
def _ledger_text():
    grp = lambda title, col, items, y0=560: [{"k": "cap", "x": 500, "y": y0 - 80, "t": title, "c": col, "in": .1}] + \
        [{"k": "label", "x": 500, "y": y0 + i * 92, "t": t, "st": "body", "in": .3 + i * .25} for i, t in enumerate(items)]
    s0 = {"base": "dark", "cam": [1.22, 500, 930], "els": lineup([("Neanderthal", 1.65), ("Denisovan", 1.8), ("Flores", 1.1), ("Luzon", 1.3), ("us", 1.72)], x0=170, dx=165)}
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Strong evidence", "#7fd1d4", ["building with wood, 476,000 years ago", "other humans, still in our DNA", "surgery, 31,000 years ago",
                                                                                          "a wooden giant, 12,000 years ago", "people in America, 21,000+ years ago"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Open", "#f0b06a", ["sailors, or castaways, a million years ago"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible", "#e8c86a", ["tall Denisovans"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting discovery", "#c9c1ee", ["a vanished billion pounds of copper", "Göbekli's hidden nine-tenths"])}
    s5 = like(s0, cam=[1.28, 500, 930])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:BEFORE US · THE LEDGER][sfx:boom][act:inviting, taking stock]^Nine films on the people before ^history. [act:warm, confident][tune:fall]Here's what we ^*know*."], cut=False),
        B("world", 1, ["[d:calm][k:STRONG EVIDENCE][act:ticking them off, steady][tune:level]Human relatives building with ^wood, nearly half a ^million years ago. [act:warm, continuing the list][tune:fall]^Other humans, still in our ^DNA.",
                       "[d:wonder][act:wonder, listing the marvels][tune:level]^Surgery in the ^Ice Age. [act:same delight, lighter][tune:level]A wooden ^giant. [act:landing the list][tune:fall]People in America ^twenty-one thousand years ago."]),
        B("collision", 2, ["[d:build][k:OPEN][act:posing the question, even][tune:rise]Did the first sailors ^plan their crossings... [act:the alternative, lighter][tune:fall]or ^drift? [act:honest, level-headed][tune:fall]Still ^open."]),
        B("cost", 3, ["[d:build][k:PLAUSIBLE][act:brisk, weighing it][tune:rise]^Tall Denisovans? [act:fair, measured][tune:fallrise]^Plausible, on ^two bones. [act:the next question, brisk][tune:rise]Giants of ^legend? [act:flat, final][tune:highfall]^No."]),
        B("reversal", 4, ["[d:reveal][k:AWAITING DISCOVERY][act:dry, a small smile]A billion pounds of copper, ^never measured. [act:wonder, lower, full of promise][tune:fall]And ^nine-tenths of Göbekli Tepe, still ^*underground*."]),
        B("tag", 5, ["[d:verdict][k:WHAT IT ADDS UP TO][p:0.95][act:warm authority, the big picture]Every time we dig deeper, our ancestors get ^*older*, and more ^capable.",
                     "[d:tension][p:0.93][gap:0.4][act:the last word, quiet wonder][tune:fall]The story of us is ^still being ^*written*."]),
    ]
    return EP("before-us-ledger", "01.10", "The Ledger: Before Us", "", "mixed", "What do we know about the people before history?", "What we *know*.", beats, shots,
              "Full references for every film in the case files", "Nine films, one ledger: what is established about the people before history, what is open, and what awaits discovery.",
              ["#HumanEvolution", "#Archaeology", "#IceAge", "#History", "#Science"])


def ledger():
    """The ledger as one continuous film: a cabinet of the nine cases of File 01 (see cabinet.py)."""
    import math as _m
    from cabinet import Cabinet, VCOL, retime
    WOODC, GRAIN = "#9a6a3c", "#c99c68"
    kalambo = [{"k": "rect", "x": -125, "y": -44, "w": 250, "h": 40, "r": 4, "fill": "#3f86a8", "c": "none", "sw": 0, "op": .45},
               {"k": "rect", "x": -125, "y": -10, "w": 250, "h": 10, "r": 2, "fill": "#5a4330", "c": "none", "sw": 0},
               {"k": "line", "p": [[-105, -118], [100, -38]], "c": WOODC, "w": 20},
               {"k": "line", "p": [[-100, -120], [96, -44]], "c": GRAIN, "w": 2, "op": .55},
               {"k": "line", "p": [[-80, -28], [88, -132]], "c": "#8a5d33", "w": 20},
               {"k": "line", "p": [[-76, -34], [84, -136]], "c": GRAIN, "w": 2, "op": .55},
               {"k": "circle", "x": 1, "y": -79, "r": 9, "fill": "#2a1d12", "c": "#e8b87a", "sw": 1.5}]
    gob = [{"k": "rect", "x": -128, "y": -118, "w": 256, "h": 118, "r": 3, "fill": "#5a4330", "c": "#7a5c3e", "sw": 1},
           {"k": "rect", "x": -118, "y": -118, "w": 92, "h": 74, "r": 2, "fill": "#1a120c", "c": "#8a6a48", "sw": 1.5},
           {"k": "tpillar", "x": -92, "y": -46, "h": 62}, {"k": "tpillar", "x": -50, "y": -46, "h": 62}]
    helix = []
    for sgn in (1, -1):
        helix.append({"k": "line", "p": [[-104 + 8 * k, round(-196 + sgn * 13 * _m.sin(k * .55), 1)] for k in range(27)], "c": "#9fd0ff", "w": 3, "fx": "draw", "dur": 1.4, "in": .5})
    helix += [{"k": "line", "p": [[-104 + 8 * k, round(-196 + 13 * _m.sin(k * .55), 1)], [-104 + 8 * k, round(-196 - 13 * _m.sin(k * .55), 1)]], "c": "#9fd0ff", "w": 1.5, "op": .6, "keepop": True, "in": 1.0 + .03 * k}
              for k in range(1, 27, 2)]
    C = Cabinet([
        {"name": "Kalambo Falls", "model": kalambo},
        {"name": "Other humans", "model": other_humans()["shots"][0], "wy": -150, "zk": .9},
        {"name": "Ice Age surgery", "model": surgeons()["shots"][0]},
        {"name": "The Shigir idol", "model": shigir()["shots"][0], "zk": .72},
        {"name": "First Americans", "model": first_americans()["shots"][0]},
        {"name": "First sailors", "model": early_seafarers()["shots"][4]},
        {"name": "Denisovans", "model": denisovan_giants()["shots"][0]},
        {"name": "Old Copper", "model": old_copper()["shots"][2]},
        {"name": "Göbekli Tepe", "model": gob},
    ])
    C.build()
    KA, OH, SU, SH, FA, FS, DE, OC, GT = range(9)
    s1 = C.step(C.cam_cell(KA), C.verdict(KA, "strong", "476,000 years", .4) + C.people(KA, 2, at=1.0))
    s2 = C.step(C.cam_cell(OH), C.verdict(OH, "strong", "in our DNA", .3) + C.local(OH, helix))
    s3 = C.step(C.cam_cell(SU), C.verdict(SU, "strong", "31,000 years", .3) + C.note(SU, "the patient lived on for years", at=.9))
    s4 = C.step(C.cam_cell(SH), C.verdict(SH, "strong", "12,000 years", .3))
    s5 = C.step(C.cam_cell(FA), C.verdict(FA, "strong", "21,000+ years", .3) + C.people(FA, 2, at=.8))
    plan = C.local(FS, [{"k": "arrow", "p": [[-105, -150], [100, -150]], "c": "#f5ecdc", "w": 3, "style": "inferred", "fx": "draw", "dur": 1.0, "in": .6}])
    drift = C.local(FS, [{"k": "line", "p": [[-105 + 7 * k, round(-104 + 9 * _m.sin(k * .8), 1)] for k in range(31)], "c": "#9fd0ff", "w": 3, "style": "claimed", "fx": "draw", "dur": 1.0, "in": .1}])
    s6 = C.step(C.cam_cell(FS), plan)
    s7 = C.step(C.cam_cell(FS), drift)
    s8 = C.step(C.cam_cell(FS), C.verdict(FS, "open", at=.1) + C.question(FS, dx=C.w * .3, dy=-190, at=.3, size=70))
    s9 = C.step(C.cam_cell(DE))
    s10 = C.step(C.cam_cell(DE), C.verdict(DE, "plausible", "two bones", .1))
    s11 = C.step(C.cam_cell(DE), C.struck(DE, "giants of legend", at=.1, rows=2))
    s12 = C.step(C.cam_cell(DE), C.verdict(DE, "ruled", frame=False, at=.05))
    s13 = C.step(C.cam_cell(OC), C.verdict(OC, "awaiting", "never measured", .3) + C.question(OC, dx=C.w * .3, dy=-150, at=.8, size=70, c=VCOL["awaiting"]))
    under = C.local(GT, [{"k": "rect", "x": x0, "y": -108, "w": 44, "h": 60, "r": 3, "fill": "none", "c": "#f5ecdc", "sw": 2, "style": "claimed", "fx": "draw", "dur": .9, "in": .8 + .15 * k}
                         for k, x0 in enumerate((-16, 34, 84))])
    s14 = C.step(C.cam_cell(GT), C.verdict(GT, "awaiting", "nine-tenths unexcavated", .2) + under)
    s15 = C.step(C.cam_all(), [e for i in range(9) for e in C.wash(i, "#f2b36b", at=.4 + .1 * i, op=.12)])
    s16 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (1, 0): "%d|1.1" % s3, (1, 1): "%d|1.0" % s4, (1, 2): "%d|1.0" % s5}),
        2: (s6, {(0, 1): "%d|.4" % s7, (0, 2): "%d|.4" % s8}),
        3: (s9, {(0, 1): "%d|.3" % s10, (0, 2): "%d|.3" % s11, (0, 3): "%d|.3" % s12}),
        4: (s13, {(0, 1): "%d|1.1" % s14}),
        5: (s15, {(1, 0): "%d|3.5" % s16}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/before-us-ledger.json)."""
    import recap
    return recap.recap(ledger, "before-us-ledger", None)


def EPISODES():
    import lg_a      # 01.01 and 01.07 rebuilt from the legacy films
    return [lg_a.kalambo_m(), other_humans_m(), early_seafarers_m(), denisovan_giants_m(), surgeons_m(), shigir_m(), lg_a.gobekli_m(), first_americans_m(), old_copper_m(), ledger_recap()]
