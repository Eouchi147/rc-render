"""File 14 · Arabia Unearthed. The Arabian Peninsula before the caravan cities: giant stone rectangles, footprints by a
vanished lake, life-size camels on cliffs, hunters' traps drawn to scale, a Babylonian king in an oasis, the burial mounds
of Dilmun, the world's oldest complaint letter and Oman's copper, and a meteorite where an explorer hoped for a lost city.
Human remains are never shown; pre-Islamic cults are described neutrally; faith is never rated; no modern politics."""
import copy
import math
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_, tablet
from f06 import box, sphere

SERIES = "Arabia Unearthed"
SAND = "#c9a878"
HORN = "#efe4cc"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def right(els, dx=14):
    """event() labels near the right edge: anchor them at their end, just past the tick."""
    for e in els:
        if e.get("k") == "label":
            e["a"] = "end"; e["x"] = e["x"] + dx
    return els


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


def dark(els, cam=(1, 500, 860)):
    return {"base": "dark", "cam": list(cam), "els": els}


def rnd(seed):
    """A small deterministic generator, so every render draws the same scatter."""
    s = [seed]
    def f():
        s[0] = (s[0] * 1103515245 + 12345) % 2147483648
        return s[0] / 2147483648
    return f


def arabia(pins, lon0=34, lon1=60, lat0=12, lat1=32, extra=(), cam=None):
    v = View(lon0, lon1, lat0, lat1, (40, 330, 920, 900))
    return mapshot(v, pins=pins, extra=list(extra), cam=cam), v


def sea(v, lon, lat, t, a="middle"):
    x, y = v.p(lon, lat)
    return {"k": "label", "x": x, "y": y, "t": t, "st": "ital", "c": "#9fd0ff", "a": a}


# ---------------------------------------------------------------- 14.01 The rectangles (mustatils)
def mustatils():
    m = [{"t": "slab", "x0": -80, "x1": 80, "z0": -24, "z1": 24, "y": 0, "c": "#9a7e5c"},
         box(-4, -10, 0, 136, 1.8, 1.3, "#e0c99e"), box(-4, 10, 0, 136, 1.8, 1.3, "#e0c99e"), box(-72, 0, 0, 1.8, 21.8, 1.3, "#e0c99e"),
         box(64, 0, 0, 12, 21.4, 1.2, "#d4bb90"), box(64, 0, 1.2, 3.6, 3.4, .7, "#b89b70")]
    for k, (dx, dz) in enumerate(((-1, -1), (0, 1), (1, -.4))):
        m.append(box(64 + dx, dz, 1.9, .5, .5, 2.2, "#e0cfa8"))
    r = rnd(7)
    for k in range(14):
        m.append({"t": "cyl", "x": 60 + r() * 9, "z": -4 + r() * 8, "y": 1.2, "r": .35, "h": .35, "c": HORN, "n": 6, "edge": "rgba(0,0,0,.2)"})
    m += [{"t": "person", "x": 56, "y": 0, "z": 14, "h": 1.7},
          L_(-4, 2, "a mustatil · c. 140 m long · schematic", GOLD, z=-10, dy=-30), L_(64, 5, "the head: a chamber, standing stones", "#cfe6ff", z=10, dy=46)]
    s0 = iso(m, cam=[1, 500, 920], s=4.0, x=500, y=1010, az=-32, spin=1.2, el=.5, table=None)
    s1, v = arabia([("AlUla", 37.92, 26.62, {"c": GOLD}), ("Khaybar", 39.29, 25.70, {"a": "end", "lx": -18, "ly": 30}), ("Jubbah", 40.93, 28.02, {})],
                   lon0=33, lon1=45, lat0=21, lat1=32)
    r = rnd(11); dots = []
    while len(dots) < 90:
        lon, lat = 36 + r() * 6, 24 + r() * 6
        if lat - 24 < 1.2 * (lon - 35) and lat < 30.2 - .25 * (lon - 36):
            x, y = v.p(lon, lat); dots.append({"k": "circle", "x": x, "y": y, "r": 3.5, "fill": OCHRE, "c": "none", "w": 0, "op": .8, "in": .8 + len(dots) * .012})
    s1["els"] += dots + [sea(v, 36.3, 22.8, "the Red Sea"), {"k": "cap", "x": 500, "y": 1270, "t": "each dot: many mustatils · schematic", "in": 1.6}]
    s2 = stat("1,600+", "rectangles", "across about 350,000 km² of north-west Arabia", "Kennedy et al. 2024")
    ch = [{"t": "slab", "x0": -5, "x1": 5, "z0": -4, "z1": 4, "y": 0, "c": "#d4bb90"}, box(0, 0, 0, 3.6, 3.4, .9, "#b89b70")]
    ch += [box(-1.1, -1, .9, .45, .45, 2.4, "#e0cfa8"), box(0, 1.1, .9, .45, .45, 2.1, "#e0cfa8"), box(1.2, -.4, .9, .45, .45, 2.6, "#e0cfa8")]
    r = rnd(3)
    for k in range(26):
        ch.append({"t": "cyl", "x": -1.5 + r() * 3, "z": -1.4 + r() * 2.8, "y": .9, "r": .16, "h": .14 + r() * .1, "c": HORN, "n": 6, "edge": "rgba(0,0,0,.2)"})
    ch += [L_(0, 3.4, "the chamber · c. 3 × 3 m · schematic", GOLD, z=-1.7, dy=-26), L_(0, .9, "247 skull and horn fragments, mostly cattle", "#cfe6ff", z=3, dy=52)]
    s3 = iso(ch, cam=[1, 500, 900], s=40, x=500, y=1040, az=-30, spin=1.0, el=.45, table=None)
    tl, ax = timeline(-6000, -2000, [(-6000, "6000 BCE"), (-5000, "5000"), (-4000, "4000"), (-3000, "3000"), (-2000, "2000")], "Older than the famous ones")
    tl["els"] += [{"k": "band", "x0": ax.x(-5400), "x1": ax.x(-4200), "y": 745, "h": 16, "c": OCHRE, "t": "the mustatils", "in": .3}] + \
                 event(ax, -3000, "Stonehenge begins", row=1, c=SCAN, i=.8) + right(event(ax, -2560, "Giza's Great Pyramid", row=2, c=GOLD, i=1.1))
    s4 = tl
    s5 = dark(grp("a cattle cult?", "#8fd9b0", ["horns and skulls in the chamber", "people gathering from afar"], y=440, size=28) +
              grp("or markers on the land?", "#e8b87a", ["along herding routes", "none much grander than the rest"], y=820, size=28))
    s6 = like(s0, cam=[1.14, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:NORTH-WEST ARABIA][sfx:boom][act:hushed, intrigued]About seven thousand years ago, herders in Arabia built more than sixteen hundred giant stone ^rectangles.",
                      "[d:tension][cam:1.12|0|0][act:the strange detail, leaning in][tune:fall]Then they filled them with cattle ^horns."], cut=False),
        B("world", 1, ["[d:calm][k:THE MUSTATILS][act:plain, orienting]Archaeologists call them ^mustatils, from the Arabic for ^rectangle. [act:steady, factual]Some are more than half a ^kilometre long.",
                       "[d:build][go:2|0][act:quietly amazed]They were first noticed in satellite ^images, and nicknamed ^gates."]),
        B("collision", 3, ["[d:build][k:THE CHAMBER][act:precise, building]At one end sits a raised head, with a small chamber and standing ^stones. [act:vivid, careful]In one near AlUla, excavators counted two hundred and forty-seven fragments of skulls and ^horns, mostly ^cattle."]),
        B("cost", 4, ["[d:build][k:THE DATE][act:the reveal, strong]Calibrated radiocarbon puts them in the {6th|sixth} millennium ^BCE. [act:context, wonder]That's some two thousand years before the first phase of ^Stonehenge.",
                      "[d:aside][act:practical, light]And ten people could build one in a few ^weeks."]),
        B("reversal", 5, ["[d:reveal][k:TWO READINGS][act:fair, weighing]The excavators see a ^cattle cult, with people gathering from far ^away. [act:the counterpoint, fair]Other teams read@present them as ^markers, claiming land along herding ^routes.",
                          "[d:build][act:a telling detail, gentle]And none is much grander than the ^others. [act:thoughtful][tune:fall]Builders without ^kings, perhaps."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Monuments older than Stonehenge, in the Arabian ^desert@noun? [act:the verdict, even][tune:fall]*Strong ^evidence*. [act:fair, clear]What they ^meant is still being ^weighed.",
                     "[d:tension][p:0.93][act:the last word, warm][tune:fall]The cattle's teeth may yet tell us where the herds came ^from."]),
    ]
    return EP("mustatils", "14.01", "The Rectangles: Arabia's Oldest Monuments", "mustatils", "strong", "Who built Arabia's giant stone rectangles, and what were they for?", "Older than *Stonehenge*.", beats, shots,
              "Thomas et al. 2021 (doi:10.15184/aqy.2021.51) · Groucutt et al. 2020 (doi:10.1177/0959683620950449) · Kennedy et al. 2023 (doi:10.1371/journal.pone.0281904) · Kennedy et al. 2024 (doi:10.5334/oq.139) · Hatton et al. 2024 (doi:10.1177/09596836241275010)",
              "More than 1,600 giant stone rectangles in north-west Arabia, some half a kilometre long, built about 7,000 years ago and filled with cattle horns. What they were for, weighed.",
              ["#Arabia", "#SaudiArabia", "#Archaeology", "#AncientMysteries", "#ArabiaUnearthed"])


# ---------------------------------------------------------------- the mural versions: small drawings shared by the films below
def _mur():
    from mural import remix
    import illus
    return remix, illus


def _horn(x, y, s=1.0, at=0, c=HORN, fx="pop", op=None):
    """A cattle horn, seen from the side: a curved crescent."""
    ts = [k / 8 for k in range(9)]
    up = [[x + s * (-14 + 28 * t), y - s * (18 * t * t + 5 * (1 - t))] for t in ts]
    lo = [[x + s * (-14 + 28 * t), y - s * (18 * t * t - 5 * (1 - t))] for t in ts[::-1]]
    e = {"k": "poly", "p": [[round(a, 1), round(b, 1)] for a, b in up + lo], "fill": c, "c": "none", "w": 0, "in": at, "fx": fx}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def _plan(x, y, L, W=None, at=0, c="#f0dcb0", w=3, ang=0, head=True, dur=1.0, style="known"):
    """A mustatil seen from above: two long walls, an end wall, and a head at one end (x, y: centre; L: length in px)."""
    W = W or max(8, L * .1)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    P = lambda u, v: [round(x + u * ca - v * sa, 1), round(y + u * sa + v * ca, 1)]
    els = [{"k": "poly", "p": [P(-L / 2, -W / 2), P(L / 2, -W / 2), P(L / 2, W / 2), P(-L / 2, W / 2)], "fill": "none", "c": c, "w": w, "in": at, "fx": "draw", "dur": dur, "style": style}]
    if head:
        h = max(5, W * .8)
        els.append({"k": "poly", "p": [P(L / 2 - h * 1.2, -h / 2), P(L / 2 + h * .3, -h / 2), P(L / 2 + h * .3, h / 2), P(L / 2 - h * 1.2, h / 2)], "fill": c, "c": "none", "w": 0, "in": round(at + dur * .8, 2), "fx": "pop"})
    return els


def _molar(x, y, h=120, at=0, c="#efe6d2"):
    """A tooth: a crown and two roots."""
    s = h / 120
    p = [[-40, -60], [-20, -66], [0, -58], [20, -66], [40, -60], [44, -20], [34, 4], [26, 58], [12, 60], [4, 14], [-4, 14], [-12, 60], [-26, 58], [-34, 4], [-44, -20]]
    return {"k": "poly", "p": [[round(x + a * s, 1), round(y + b * s, 1)] for a, b in p], "fill": c, "c": "#b8a888", "w": 2, "curve": True, "in": at, "fx": "pop"}


def _pitch(x, y, w, at=0):
    """A football pitch from above (105 x 68 m), w pixels long."""
    h = w * 68 / 105
    return [{"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": 2, "fill": "#4f7a46", "c": "#e8f0dc", "sw": 2, "in": at, "fx": "pop"},
            {"k": "line", "p": [[x + w / 2, y], [x + w / 2, y + h]], "c": "#e8f0dc", "w": 2, "in": at},
            {"k": "circle", "x": x + w / 2, "y": y + h / 2, "r": h * .18, "fill": "none", "c": "#e8f0dc", "w": 2, "in": at}]


def mustatils_m():
    """The mustatils as one continuous take (see mural.py): spotted from orbit, counted in a chamber, dated against Stonehenge, read two ways."""
    remix, I = _mur()
    ep = mustatils()
    SANDY = "#e8d3a8"
    hero = copy.deepcopy(ep["shots"][0])
    for e in hero["els"]:
        if e.get("k") == "iso":
            e["spin"] = .35                                    # a slow turn: the model is on screen at the start and again at the end
    chamber = copy.deepcopy(ep["shots"][3])
    for e in chamber["els"]:
        if e.get("k") == "iso":
            e["items"] = [it for it in e["items"] if not str(it.get("text", "")).startswith("247")]
    # 2 · from above: a satellite scans the desert, outlines appear; one of them, enlarged, beside five football pitches
    sat = [I.box(670, 312, 60, 40, "#cbd2d8", "#8a939c", 2, 4, .1, fx="pop"), I.box(588, 318, 72, 28, "#3f6f9a", "#9fd0ff", 2, 2, .2, fx="pop"),
           I.box(740, 318, 72, 28, "#3f6f9a", "#9fd0ff", 2, 2, .2, fx="pop"),
           I.line([[690, 356], [160, 500]], .5, I.BLUE, 2, "inferred", .8), I.line([[710, 356], [850, 500]], .5, I.BLUE, 2, "inferred", .8),
           I.box(110, 500, 780, 560, "#9a7e5c", SANDY, 2, 10, .3, op=.95)]
    dunes = [I.line([[130, 560 + 90 * k], [300, 540 + 90 * k], [520, 575 + 90 * k], [700, 548 + 90 * k], [870, 566 + 90 * k]], .4, "#b89a72", 3, curve=True, draw=False, op=.6) for k in range(6)]
    spots = [(230, 600, 120, 8), (420, 640, 90, -12), (640, 610, 150, 4), (780, 700, 80, 30), (200, 760, 100, -20), (360, 820, 140, 6), (560, 760, 70, -40),
             (720, 860, 120, 14), (250, 960, 90, 2), (470, 950, 130, -8), (680, 990, 100, 20), (820, 950, 60, -30)]
    outlines = sum([_plan(x, y, L, at=round(.7 + .12 * k, 2), ang=a, dur=.5, w=2.5) for k, (x, y, L, a) in enumerate(spots)], [])
    gate = [I.line([[130, 300], [130, 400]], 3.2, SANDY, 5, dur=.3), I.line([[290, 300], [290, 400]], 3.2, SANDY, 5, dur=.3)] + \
           [I.line([[130, 318 + 30 * j], [290, 318 + 30 * j]], 3.4 + .1 * j, SANDY, 4, dur=.4) for j in range(3)] + [I.line([[134, 378], [286, 318]], 3.7, SANDY, 4, dur=.4),
           I.label(210, 448, "'gates'", 3.8, SANDY, 34, st="ital"), I.ring(640, 610, 92, 3.6, I.AMBER, 3, dur=.6)]
    big = [I.line([[640, 640], [500, 1140]], 5.0, I.AMBER, 2, "inferred", .6)] + _plan(500, 1170, 640, 40, 5.4, SANDY, 4, dur=1.0) + \
          sum([_pitch(180 + 128 * k, 1240, 128, 5.8 + .2 * k) for k in range(5)], []) + [I.label(500, 1385, "5 pitches · over 500 m", 6.8, SANDY, 32)]
    above = {"base": "dark", "stars": 60, "cam": [1, 500, 860], "els": sat + dunes + outlines + gate + big}
    # 3 · the chamber: 247 fragments, counted out one by one
    horns = [_horn(178 + 36 * (k % 19), 360 + 27 * (k // 19), .9, round(6.4 + .009 * k, 3)) for k in range(247)]
    count = horns + [I.label(500, 740, "247 fragments of skull and horn", 9.0, I.AMBER, 32)]
    # 4 · older than Stonehenge: the axis draws, an hourglass runs, the rectangles land 2,000 years before the first stones there
    X = lambda yr: 120 + 760 * (yr + 6000) / 4000
    glass = [I.line([[440, 430], [560, 430], [500, 520], [560, 610], [440, 610], [500, 520], [440, 430]], 2.4, I.BONE, 3, dur=1.0),
             {"k": "poly", "p": [[452, 442], [548, 442], [500, 510]], "fill": "#e8c894", "c": "none", "w": 0, "in": 2.8},
             {"k": "poly", "p": [[500, 530], [552, 600], [448, 600]], "fill": "#e8c894", "c": "none", "w": 0, "in": 3.2, "fx": "fill", "dur": 2.5},
             I.line([[500, 512], [500, 600]], 3.0, "#e8c894", 2, "inferred", .6), I.glow(500, 520, 120, 2.6, .4)]
    henge = sum([[I.box(X(-3000) + dx - 34, 950 - hh, 20, hh, "#cbbca8", r=2, at=8.6 + .1 * j, fx="rise"), I.box(X(-3000) + dx + 14, 950 - hh, 20, hh, "#cbbca8", r=2, at=8.65 + .1 * j, fx="rise"),
                  I.box(X(-3000) + dx - 40, 936 - hh, 80, 16, "#cbbca8", r=2, at=8.8 + .1 * j, fx="pop")] for j, (dx, hh) in enumerate(((-26, 56), (26, 72)))], []) + \
            [I.label(X(-3000), 848, "Stonehenge", 9.0, "#9fd0ff", 30)]
    older = {"base": "dark", "cam": [1.12, 500, 900], "els": [
        I.line([[110, 1000], [890, 1000]], .2, "#e9dccb", 3, dur=1.2)] +
        [I.line([[X(v), 990], [X(v), 1010]], .4, "#e9dccb", 2, draw=False) for v in (-6000, -5000, -4000, -3000, -2000)] +
        [I.label(X(v), 1056, t, .5, "#cbbca8", 28) for v, t in ((-6000, "6000 BCE"), (-4000, "4000"), (-2000, "2000 BCE"))] + glass +
        [I.line([[X(-5400), 1000], [X(-4200), 1000]], 6.0, I.AMBER, 18, dur=1.0)] + _plan((X(-5400) + X(-4200)) / 2, 930, 150, 22, 6.4, SANDY, 3, dur=.7) +
        [I.label((X(-5400) + X(-4200)) / 2, 880, "the mustatils", 6.8, I.AMBER, 30)] + henge +
        [I.arrow([[X(-5000), 830], [X(-4000), 730], [X(-3000) - 6, 792]], 9.4, I.BONE, 3, dur=1.0), I.label(X(-4000), 700, "2,000 years", 9.8, I.BONE, 32)]}
    crew = [I.person(170 + 52 * k, 1330, 80, 1.3 + .1 * k) for k in range(10)] + \
           [I.line([[110, 1352], [890, 1352]], 2.3, "#b89b70", 10, dur=2.0), I.label(500, 1410, "10 people · a few weeks", 3.0, I.BONE, 30)]
    # 5 · two readings: a cult, people walking in to the horns; or markers along a herding route
    cult = _plan(270, 640, 300, 34, .4, SANDY, 3, dur=.8) + [_horn(372 + 34 * j, 600, 1.3, 1.4 + .15 * j) for j in range(3)] + [I.glow(410, 620, 90, 1.4, .6)]
    walk = [(110, 470), (250, 450), (420, 470), (110, 820), (300, 840), (460, 800)]
    cult += sum([[I.person(x, y + (40 if y > 700 else 0), 70, 2.4 + .15 * k), I.arrow([[x + 14, y - 20 + (40 if y > 700 else 0) - (10 if y > 700 else 0)], [404, 640 + (34 if y > 700 else -34)]], 2.6 + .15 * k, I.GREEN, 2, "inferred", .6)]
                 for k, (x, y) in enumerate(walk)], []) + [I.label(270, 960, "a cattle cult?", 3.8, I.GREEN, 32)]
    route = [[560, 400], [700, 490], [620, 600], [780, 700], [700, 810], [860, 880]]
    mark = sum([_plan(px + 40, py, 70, 12, 6.2 + .3 * j, SANDY, 2.5, ang=-20, dur=.4) + [I.line([[px + 74, py - 4], [px + 74, py - 44]], 6.5 + .3 * j, I.BONE, 2, draw=False),
                {"k": "poly", "p": [[px + 74, py - 44], [px + 100, py - 36], [px + 74, py - 28]], "fill": I.AMBER, "c": "none", "w": 0, "in": 6.6 + .3 * j, "fx": "pop"}]
                for j, (px, py) in enumerate((route[1], route[3], route[5]))], [])
    herd = [I.dot(x, y, 7, "#cbbca8", round(7.4 + .1 * k, 2)) for k, (x, y) in enumerate(((610, 445), (640, 545), (690, 650), (740, 755), (780, 850)))]
    markers = [I.line(route, 5.6, I.AMBER, 3, "inferred", 1.4, True)] + mark + herd + [I.label(730, 960, "markers?", 8.0, I.AMBER, 32)]
    two = {"base": "dark", "cam": [1, 500, 880], "els": [I.line([[500, 420], [500, 1000]], .1, "#5a4a3a", 2, draw=False)] + cult + markers}
    bars = sum([_plan(170 + 88 * k, 1390 - hh / 2, hh, 30, round(.3 + .15 * k, 2), SANDY, 3, ang=-90, dur=.5) for k, hh in enumerate((150, 170, 140, 165, 155, 175, 160))], [])
    king = _plan(820, 1390 - 130, 260, 30, 2.0, I.LILAC, 3, ang=-90, dur=.6, style="claimed") + [
            {"k": "poly", "p": [[790, 1110], [798, 1070], [812, 1092], [824, 1060], [836, 1092], [850, 1070], [858, 1110]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": 2.6},
            I.glow(500, 1300, 260, 4.3, .35)]
    # the verdict on the model; then a tooth, a stamp, and the roads it might point to
    teeth = [_molar(500, 520, 150, .3), I.glow(500, 520, 160, .3, .5), I.ring(610, 430, 46, 2.6, I.AMBER, 3, dur=.6), I.ring(610, 430, 34, 2.8, I.AMBER, 2, dur=.5)] + \
            [I.arrow([[500 + 90 * math.cos(a), 520 + 90 * math.sin(a)], [500 + 330 * math.cos(a), 520 + 230 * math.sin(a)]], 3.6 + .2 * k, I.LILAC, 3, "claimed", .8, False)
             for k, a in enumerate((math.pi * .95, math.pi * .62, math.pi * .38, math.pi * .05))] + \
            I.question(500 + 330 * math.cos(math.pi * .95) + 10, 520 + 230 * math.sin(math.pi * .95) + 20, 4.4, 60) + I.question(500 + 330 * math.cos(math.pi * .05) - 10, 520 + 230 * math.sin(math.pi * .05) + 20, 4.6, 60)
    return remix(ep, scenes={0: hero, 2: above, 3: chamber, 4: older, 5: two}, alias={6: 0}, cams={0: [1.15, 500, 980], 6: [1.12, 500, 920]},
                 drop=("para", "num", "title", "q", "cap"), adds={3: count}, line_adds={(3, 1): (crew, None), (4, 1): (bars + king, None), (5, 1): (teeth, None)})


# ---------------------------------------------------------------- 14.02 Footprints by a vanished lake
def oval(x, z, a, b, ang=0, n=12):
    ca, sa = math.cos(ang), math.sin(ang)
    return [[x + a * math.cos(2 * math.pi * k / n) * ca - b * math.sin(2 * math.pi * k / n) * sa,
             z + a * math.cos(2 * math.pi * k / n) * sa + b * math.sin(2 * math.pi * k / n) * ca] for k in range(n)]


def footprints():
    f = [{"t": "slab", "x0": -7, "x1": 7, "z0": -5, "z1": 5, "y": 0, "c": "#8c7a60"},
         {"t": "flat", "pts": [[3.5, -5], [7, -5], [7, 5], [5.2, 5], [4.4, 1], [3.6, -2]], "y": .02, "c": "#4f7f96"}]
    for k in range(9):                                         # an elephant walking toward the water
        x = -6 + k * 1.15; z = 2.4 + (k % 2) * .7
        f.append({"t": "flat", "pts": oval(x, z, .36, .34), "y": .03, "c": "#4a3b2b"})
    for k in range(8):                                         # two people, side by side
        x = -5.5 + k * .8; z = -1.2 + (k % 2) * .28
        f.append({"t": "flat", "pts": oval(x, z, .22, .09, .08), "y": .03, "c": "#2a2019"})
        f.append({"t": "flat", "pts": oval(x + .3, z - 1.1 + (k % 2) * .2, .21, .085, .08), "y": .03, "c": "#2a2019"})
    f += [{"t": "person", "x": -6.3, "y": 0, "z": -3.6, "h": 1.7},
          L_(-1, 0, "elephant tracks", "#e8d3a8", z=2.8, dy=-24), L_(-2, 0, "human tracks, two people side by side", "#cfe6ff", z=-2.2, dy=56),
          L_(5.4, 0, "the lake", "#9fd0ff", z=-1, dy=-10)]
    s0 = iso(f, cam=[1, 500, 920], s=42, x=500, y=1010, az=-18, spin=1.0, el=.55, table=None)
    s1, v = arabia([("Alathar · Nefud (approx.)", 38.0, 28.0, {"c": GOLD}), ("Jebel Faya · Sharjah", 55.847, 25.119, {"a": "end", "lx": -18, "ly": 30}),
                    ("Bab el-Mandeb", 43.4, 12.6, {"c": SCAN, "a": "end", "lx": -18})], lon0=32, lon1=60, lat0=10, lat1=33)
    s1["els"] += [{"k": "arrow", "p": [v.p(42.6, 12.9), v.p(41.2, 18), v.p(39.2, 24.5), v.p(38.3, 27.4)], "curve": True, "c": AMBER, "w": 2.4, "in": 1.4, "fx": "draw"},
                  sea(v, 36.8, 21.0, "the Red Sea"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}]
    s2 = stat("c. 120,000", "years", "the layers above and below the tracks date to about 121,000 and 112,000 years ago", "Stewart et al. 2020, Science Advances")
    counts = [("camels", 107), ("elephants", 43), ("people", 7)]
    bars = []
    for k, (t, n) in enumerate(counts):
        y = 700 + k * 150; w = 620 * n / 107
        bars += [{"k": "rect", "x": 200, "y": y, "w": w, "h": 56, "fill": GOLD if t == "people" else "#8c7152", "c": "none", "sw": 0, "in": .3 + k * .3},
                 {"k": "label", "x": 190, "y": y + 38, "t": t, "a": "end", "c": GOLD if t == "people" else "#e9dccb", "in": .3 + k * .3},
                 {"k": "label", "x": 215 + w, "y": y + 38, "t": str(n), "a": "start", "c": "#e9dccb", "in": .5 + k * .3}]
    s3 = dark(bars + [{"k": "cap", "x": 500, "y": 600, "t": "376 tracks · the ones we can name", "in": .1},
                      {"k": "label", "x": 500, "y": 1190, "t": "plus horses' and cattle's wild relatives", "st": "small", "c": "#b9aa97", "in": 1.3}])
    tl, ax = timeline(-250000, 0, [(-250000, "250,000 years ago"), (-150000, "150,000"), (-50000, "50,000"), (0, "today")], "A door that opened and closed")
    tl["els"] += event(ax, -212000, "Faya: oldest layer", row=1, c=SCAN, i=.3) + event(ax, -125000, "Faya tools", row=2, c=SCAN, i=.6) + \
                 event(ax, -117000, "the footprints", row=0, c=GOLD, i=.9) + \
                 right(event(ax, -55000, "the main wave out of Africa", row=3, c=AMBER, i=1.2))
    s4 = tl
    s5 = dark(grp("solid", "#8fd9b0", ["the footprints", "their dates", "a lake in today's desert"], y=440, size=28) +
              grp("still inferred", "#9fd0ff", ["who the walkers were", "whether their line survived"], y=820, size=28))
    s6 = like(s0, cam=[1.18, 500, 950])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE NEFUD · ARABIA][sfx:boom][act:hushed, wonder]In the middle of today's sand sea, human footprints walk beside ^elephants.",
                      "[d:tension][cam:1.12|0|0][act:the twist, leaning in][tune:fall]To a lake that no longer ^exists."], cut=False),
        B("world", 1, ["[d:calm][k:ALATHAR][act:plain, orienting]The Nefud desert@noun, in northern Saudi ^Arabia. [act:steady, factual]In {2017|twenty seventeen}, researchers found an ancient lakebed there, crossed by ^tracks.",
                       "[d:build][go:3|0][act:counting, amused]Three hundred and seventy-six footprints: camels, elephants, and seven made by ^people."]),
        B("collision", 2, ["[d:build][k:THE DATE][act:the reveal, strong]The layers around them date to about a hundred and twenty ^thousand years ago. [act:warm, vivid]Arabia was ^green again, and animals moved ^in.",
                           "[d:aside][act:gentle, a small smile]Two or three people seem to have stopped for a ^drink, and moved ^on."]),
        B("cost", 4, ["[d:build][k:THE CORRIDOR][act:building, precise]At Jebel ^Faya, in Sharjah, stone tools go back about a hundred and twenty-five thousand years, with older layers ^below. [act:the point, clear][tune:fall]Arabia wasn't a ^wall. It was a ^door, that opened and ^closed."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:the crux, slower]But here's the ^catch. [act:precise]No human ^bones. No ^DNA. [act:fair, the challenger's case]So who walked here is ^inferred, not ^seen.",
                          "[d:build][act:a caveat, gentle]And most people outside Africa today descend from a much ^later wave."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]Our own species, in Arabia, a hundred and twenty thousand years ago? [act:the verdict, measured][tune:fall]^*Plausible*. [act:fair]The prints are ^real.",
                     "[d:tension][p:0.93][act:inviting, warm][tune:fall]The walkers still need a ^name."]),
    ]
    return EP("nefud-footprints", "14.02", "Footprints by a Vanished Lake", "nefud-footprints", "plausible", "Did our species walk through a green Arabia about 120,000 years ago?", "Footprints in a *vanished* lake.", beats, shots,
              "Stewart et al. 2020 (doi:10.1126/sciadv.aba8940) · Armitage et al. 2011 (doi:10.1126/science.1199113) · Bretzke et al. 2022 (doi:10.1038/s41598-022-05617-w) · Groucutt et al. 2021 (doi:10.1038/s41586-021-03863-y) · Markowska et al. 2025 (doi:10.1038/s41586-025-08859-6)",
              "Human footprints beside elephant tracks, on the shore of a lake in what is now the Nefud desert, about 120,000 years ago. What they tell us about a green Arabia, and what they don't.",
              ["#Arabia", "#Prehistory", "#HumanOrigins", "#Archaeology", "#ArabiaUnearthed"])


ELEPHANT = [(0, 40), (20, 10), (70, 0), (120, 4), (150, 10), (170, 30), (184, 60), (190, 100), (186, 132), (176, 130), (176, 98), (166, 72), (156, 70), (150, 84),
            (150, 140), (130, 140), (126, 98), (74, 98), (70, 140), (50, 140), (44, 92), (10, 72)]


def _beast(pts, x, y, s, c="#e0c9a0", w=3, at=0):
    """An outline animal (feet on y), drawing itself."""
    h = max(py for _, py in pts)
    return {"k": "poly", "p": [[round(x + px * s, 1), round(y + (py - h) * s, 1)] for px, py in pts], "fill": "none", "c": c, "w": w, "in": at, "fx": "draw", "dur": 1.0}


def _ghost(x, y, h, at=0, c="#c9c1ee"):
    """A person drawn as a dotted outline: someone inferred, not seen."""
    w = h * .26
    body = [[x - w * .5, y - h * .78], [x + w * .5, y - h * .78], [x + w * .42, y - h * .42], [x + w * .3, y], [x + w * .08, y], [x, y - h * .36], [x - w * .08, y], [x - w * .3, y], [x - w * .42, y - h * .42]]
    return [{"k": "circle", "x": x, "y": round(y - h * .9, 1), "r": round(h * .085, 1), "fill": "none", "c": c, "w": 3, "style": "claimed", "in": at},
            {"k": "poly", "p": [[round(a, 1), round(b, 1)] for a, b in body], "fill": "none", "c": c, "w": 3, "style": "claimed", "in": at}]


def _foot(x, y, s=1.0, at=0, c="#2a2019", ang=0, op=None, side=1):
    """A human footprint from above, toes up (ang turns it, side=-1 mirrors it into a left foot): a sole and five toes."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    P = lambda u, v: [round(x + (side * u * ca - v * sa) * s, 1), round(y + (side * u * sa + v * ca) * s, 1)]
    sole = [P(13 * math.cos(t) * (.72 if math.sin(t) > 0 else 1) - (2 if math.sin(t) > 0 else 0), 22 * math.sin(t) + 4) for t in [k * math.pi / 8 for k in range(16)]]
    els = [{"k": "poly", "p": sole, "fill": c, "c": "none", "w": 0, "curve": True, "in": at, "fx": "pop"}]
    els += [{"k": "circle", "x": P(dx, -24 + abs(dx - 2) * .35)[0], "y": P(dx, -24 + abs(dx - 2) * .35)[1], "r": round(r * s, 1), "fill": c, "c": "none", "w": 0, "in": at, "fx": "pop"}
            for dx, r in ((-8, 4.4), (-1, 3.4), (5, 3), (10, 2.7), (14, 2.3))]
    if op is not None:
        for e in els:
            e.update(op=op, keepop=True)
    return els


def footprints_m():
    """The Nefud footprints as one continuous take (see mural.py): 376 prints counted, a layer cake dated, a door that opens and closes, and the walkers no one has seen."""
    remix, I = _mur()
    ep = footprints()
    MUD, GOLD_ = "#5f4c39", "#f2c98e"
    hero = copy.deepcopy(ep["shots"][0])
    for e in hero["els"]:
        if e.get("k") == "iso":
            e["spin"] = .12                                    # its labels cross if it turns much further
    m = copy.deepcopy(ep["shots"][1])
    m["els"] = [e for e in m["els"] if e.get("k") != "arrow"]   # the route is drawn later, when the door opens
    v = View(32, 60, 10, 33, (40, 330, 920, 900))
    # 3 · every print, one dot: 376 in all; 107 camels, 43 elephants, 7 people
    cell = lambda k: (165 + 35 * (k % 20), 430 + 35 * (k // 20))
    tally = [I.dot(*cell(k), 11, "#4a4038", round(.2 + .003 * k, 3)) for k in range(376)]
    tally += [I.dot(*cell(k), 11, "#c9a06a", round(2.0 + .012 * k, 3)) for k in range(107)] + [I.label(500, 1170, "107 camels", 2.8, "#c9a06a", 32)]
    tally += [I.dot(*cell(107 + k), 11, "#9aa7b4", round(3.5 + .02 * k, 3)) for k in range(43)] + [I.label(500, 1230, "43 elephants", 3.9, "#9aa7b4", 32)]
    tally += sum([[I.glow(*cell(150 + k), 30, 4.4 + .1 * k, .8), I.dot(*cell(150 + k), 12, GOLD_, 4.4 + .1 * k)] for k in range(7)], []) + \
             [I.label(500, 1300, "7 people", 4.9, GOLD_, 36)]
    count = {"base": "dark", "cam": [1.05, 500, 880], "els": [I.label(500, 380, "376 footprints", .2, I.BONE, 34)] + tally}
    # 2 · a layer cake: the prints between two dated layers; above it, the lake as it was, and the walkers who stopped there
    layers = [I.box(140, 840, 720, 120, "#9c8566", r=4, at=1.6, fx="fill", dur=.8), I.box(140, 960, 720, 50, MUD, r=0, at=1.3, fx="fill", dur=.6),
              I.box(140, 1010, 720, 120, "#b49a74", r=4, at=1.1, fx="fill", dur=.8), I.box(140, 1130, 720, 110, "#6f5a44", r=4, at=1.0, fx="fill", dur=.8)]
    layers += [I.oval(220 + 70 * k, 962, 16, 7, "#2a2019", at=1.8 + .05 * k) for k in range(9)] + [I.label(845, 996, "the prints", 2.2, GOLD_, 30, "end")]
    layers += [I.label(165, 1080, "c. 121,000 years", 3.6, I.BONE, 30, "start"), I.label(165, 912, "c. 112,000 years", 5.5, I.BONE, 30, "start"),
               I.box(130, 950, 740, 70, "none", GOLD_, 3, 6, 7.0, fx="draw")]
    then = [I.line([[80, 700], [920, 700]], 9.4, "#c9a878", 3, dur=1.0), I.oval(710, 712, 170, 24, "#3f86a8", "#9fd0ff", 2, .9, 9.6),
            I.glow(710, 700, 200, 9.8, .35)] + \
           [I.line([[110 + 34 * k, 700], [104 + 34 * k + 8 * (k % 2), 670 - 10 * (k % 3)]], 10.0 + .03 * k, "#8fd9b0", 3, draw=False) for k in range(9)] + \
           [_beast(CAMEL, 90, 700, .42, at=10.5), _beast(ELEPHANT, 250, 700, .95, at=10.9),
            I.arrow([[880, 970], [905, 840], [890, 720]], 9.2, GOLD_, 2, "inferred", .8)]
    walkers = [I.person(462 + 32 * k, 702, 90, 11.6 + .2 * k) for k in range(3)] + \
              [I.arrow([[560, 600], [720, 560], [900, 620]], 13.8, I.BONE, 3, "inferred", 1.0)] + [I.dot(600 + 70 * j, 586 - 10 * (j % 2), 5, "#e8d6b8", round(14.0 + .12 * j, 2)) for j in range(4)]
    cake = {"base": "dark", "cam": [1.12, 500, 920], "els": layers + then + walkers}
    # the map again: Faya's layers, the routes, and a door that opens and shuts
    fx_, fy = v.p(55.847, 25.119); sx, sy = v.p(43.4, 12.6)
    door = [I.box(fx_ - 34, fy - 140 + 26 * j, 68, 24, c, r=2, at=1.5 + .15 * j) for j, c in enumerate(("#c9a878", "#9c8566", "#b49a74", "#6f5a44"))] + \
           [I.tri(fx_, fy - 140 + 26 + 12, 10, 0, "#efe6d2", 3.0), I.glow(fx_, fy - 100, 70, 3.0, .7), I.label(fx_, fy - 160, "125,000 years", 4.0, I.BONE, 28, "middle")]
    door += [{"k": "arrow", "p": [v.p(42.6, 12.9), v.p(41.2, 18), v.p(39.2, 24.5), v.p(38.3, 27.4)], "curve": True, "c": I.AMBER, "w": 3, "in": 8.8, "fx": "draw", "dur": 1.4},
             {"k": "arrow", "p": [v.p(43.9, 13.3), v.p(48, 15.6), v.p(52.4, 18.6), v.p(55.3, 24.2)], "curve": True, "c": I.AMBER, "w": 3, "in": 9.1, "fx": "draw", "dur": 1.4, "style": "inferred"}]
    door += [I.box(sx - 30, sy - 116, 60, 104, "none", I.BONE, 4, 3, 8.1, fx="draw"), I.glow(sx, sy - 64, 110, 8.5, .7),
             I.box(sx - 30, sy - 116, 60, 104, "#c9a878", "#8a6a48", 2, 3, 11.2, fx="pop")]
    # 5 · the catch: prints but no bones, no DNA; someone inferred
    no_bone = [I.line([[170, 560], [310, 560]], 1.2, "#efe6d2", 14, draw=False)] + [I.dot(170 + dx, 560 + dy, 12, "#efe6d2", 1.2, None) for dx in (-6, 146) for dy in (-9, 9)] + \
              [I.strike(150, 610, 330, 510, 1.7)]
    helix = [I.line([[650 + 9 * k, round(560 + 26 * math.sin(k * .55 + ph), 1)] for k in range(22)], 2.1, I.BLUE, 4, dur=.6, curve=True) for ph in (0, math.pi)] + \
            [I.strike(640, 610, 850, 510, 2.6)]
    prints = sum([_foot(round(170 + 50 * j + (8 if j % 2 else -8) * .355, 1), round(1110 - 19 * j + (8 if j % 2 else -8) * .935, 1), .9, round(.2 + .1 * j, 2), GOLD_, 69,
                        op=.9, side=-1 if j % 2 else 1) for j in range(6)], [])
    who = _ghost(500, 1010, 280, 3.1) + I.question(500, 640, 3.6, 90)
    catch = {"base": "dark", "floor": 1010, "cam": [1, 500, 920], "els": prints + no_bone + helix + who}
    X = lambda ka: 160 + 700 * (120 - ka) / 120
    lineage = [I.line([[150, 1340], [870, 1340]], .2, "#8c7152", 3, dur=.8), I.label(160, 1390, "120,000 years ago", .4, "#cbbca8", 28, "start"),
               I.label(860, 1390, "today", .4, "#cbbca8", 28, "end"),
               I.line([[X(120), 1300], [X(105), 1296], [X(90), 1304], [X(80), 1300]], 3.3, I.LILAC, 4, "claimed", 1.0)] + I.question(X(74), 1322, 3.8, 50) + \
              [I.line([[X(55), 1280], [860, 1280]], 1.8, I.AMBER, 12, dur=1.2), I.dot(X(55), 1280, 10, I.AMBER, 1.8), I.label(X(55), 1250, "a later wave", 2.0, I.AMBER, 28, "start")] + \
              [I.person(760 + 22 * k, 1266, 44, 2.4 + .06 * k, c="#e8b87a") for k in range(5)]
    bone = [I.line([[400, 520], [600, 520]], 4.6, I.LILAC, 5, "claimed", .8)] + [I.ring(400 + dx, 520 + dy, 13, 4.8, I.LILAC, 3, "claimed", .4) for dx in (-6, 206) for dy in (-11, 11)] + \
           [I.glow(500, 520, 160, 4.6, .4)] + I.question(500, 440, 5.0, 70)
    return remix(ep, scenes={0: hero, 1: m, 2: cake, 3: count, 5: catch}, alias={4: 1, 6: 0},
                 cams={0: [1.15, 500, 980], 4: [1.2, 540, 830], 6: [1.12, 500, 920]}, drop=("para", "num", "title", "q", "cap"),
                 beat_adds={3: (door, [1.2, 540, 830])}, line_adds={(4, 1): (lineage, None), (5, 1): (bone, None)})


# ---------------------------------------------------------------- 14.03 Giant camels on the cliffs
CAMEL = [(0, 120), (18, 62), (60, 32), (100, 0), (140, 30), (168, 44), (196, 24), (226, -18), (248, -40), (274, -40), (282, -26), (258, -14), (242, 22),
         (232, 70), (222, 124), (218, 206), (206, 206), (200, 136), (172, 132), (164, 206), (152, 206), (146, 134), (72, 134), (62, 206), (50, 206),
         (44, 132), (28, 206), (16, 206), (10, 134)]


def camel(x, y, s, c="#f3e2c0", w=4, i=.4):
    return {"k": "poly", "p": [[x + px * s, y + py * s] for px, py in CAMEL], "fill": "none", "c": c, "w": w, "in": i, "fx": "draw"}


def camels():
    cliff = {"k": "poly", "p": [[120, 1240], [150, 660], [260, 590], [520, 570], [760, 600], [880, 690], [900, 1240]], "fill": "#6d5641", "c": "#a88b66", "w": 2, "in": -1}
    s0 = dark([cliff, {"k": "rect", "x": 0, "y": 1240, "w": 1000, "h": 400, "fill": "#8a7050", "c": "none", "sw": 0, "in": -1},
               camel(330, 700, 1.15, i=.6), {"k": "person", "x": 760, "y": 1240, "h": 60, "in": .3},
               {"k": "line", "p": [[860, 700], [860, 1240]], "c": "#e9dccb", "w": 2, "in": 1.2},
               {"k": "label", "x": 850, "y": 930, "t": "up to 39 m", "a": "end", "c": "#e9dccb", "in": 1.3},
               {"k": "label", "x": 500, "y": 1320, "t": "a life-size camel, high on a cliff · schematic", "c": AMBER, "in": 1.5}])
    s1, v = arabia([("Jubbah · rock art", 40.93, 28.02, {"c": GOLD}), ("Sakaka · the Camel Site", 40.21, 29.97, {"a": "end", "lx": -18, "ly": -24}),
                    ("Göbekli Tepe", 38.92, 37.22, {"c": SCAN})], lon0=34, lon1=46, lat0=24, lat1=38.5)
    s1["els"] += [{"k": "label", "x": v.p(41.4, 27.3)[0], "y": v.p(41.4, 27.3)[1], "t": "the Nefud", "st": "ital", "c": "#e8c894", "in": 1.0},
                  {"k": "cap", "x": 500, "y": 1270, "t": "exact sites withheld, to protect the art", "in": 1.6}]
    s2 = stat("176", "engravings", "on 62 panels at three sites; 130 of them life-size, animals 1.7 to 3 m long", "Guagnin et al. 2025, Nature Communications")
    s3 = dark([camel(170, 640, .75, i=.2), camel(560, 700, .55, c="#e0c9a0", i=.5),
               {"k": "cap", "x": 500, "y": 560, "t": "what they carved", "in": .1}] +
              [{"k": "label", "x": 500, "y": 980 + k * 60, "t": t, "st": "serif", "size": 30, "in": .8 + k * .25} for k, t in enumerate(["90 camels", "ibex, gazelles, wild asses", "one wild aurochs"])])
    tl, ax = timeline(-16000, -6000, [(-16000, "16,000 years ago"), (-12000, "12,000"), (-8000, "8,000")], "When the dunes held water")
    tl["els"] += [{"k": "band", "x0": ax.x(-16000), "x1": ax.x(-13000), "y": 745, "h": 14, "c": "#4f7f96", "t": "seasonal lakes", "in": .3},
                  {"k": "band", "x0": ax.x(-12800), "x1": ax.x(-11400), "y": 660, "h": 16, "c": GOLD, "t": "the camp below the art", "in": .6}] + \
                 event(ax, -11600, "Göbekli Tepe rises", row=2, c=SCAN, i=.9) + right(event(ax, -8000, "the youngest the art could be?", row=3, c=RED, i=1.2))
    s4 = tl
    s5 = dark(grp("dated", "#8fd9b0", ["hearths and stone points below", "beads carried 320 km"], y=440, size=28) +
              grp("not dated", "#9fd0ff", ["the carvings themselves"], y=820, size=28))
    s6 = like(s0, cam=[1.15, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:NORTHERN ARABIA][sfx:boom][act:hushed, wonder]About twelve thousand years ago, someone carved a ^camel, life-size, high up a desert@noun ^cliff.",
                      "[d:tension][cam:1.12|0|0][act:the question, leaning in][tune:fall]Why ^there?"], cut=False),
        B("world", 1, ["[d:calm][k:THE NEFUD][act:plain, orienting]The southern edge of the Nefud, in northern ^Arabia. [act:steady]In {2025|twenty twenty-five}, a team published sixty-two carved panels at three ^sites."]),
        B("collision", 2, ["[d:build][k:THE ART][act:impressed, building]A hundred and seventy-six engravings, most of them ^life-size. [act:vivid, a little amazed]One panel sits thirty-nine metres up a ^cliff.",
                           "[d:build][go:3|0][act:counting, delighted]Camels, ibex, gazelles, and one wild ^aurochs."]),
        B("cost", 4, ["[d:build][k:THE DATE][act:precise]Below the panels: hearths, stone points, and beads carried from more than three hundred kilometres ^away. [act:the reveal]They date to about twelve thousand years ^ago, when seasonal lakes filled the ^dunes.",
                      "[d:aside][act:context, wonder]Around the time Göbekli Tepe was rising, far to the ^north."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:the crux, slower]But the carvings themselves aren't ^dated. [act:fair, the challenger's case]One archaeologist notes they could be as young as eight ^thousand years."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]Giant art from the end of the Ice ^Age? [act:the verdict, measured][tune:fall]^*Plausible*. [act:fair]The camp is ^dated. The cliff is not, ^yet.",
                     "[d:tension][p:0.93][act:the last word, warm, a small smile][tune:fall]Perhaps they were ^signposts: water, this ^way."]),
    ]
    return EP("camel-cliffs", "14.03", "Giant Camels on the Cliffs", "camel-cliffs", "plausible", "Were Arabia's life-size cliff engravings carved about 12,000 years ago?", "A camel *39 m* up a cliff.", beats, shots,
              "Guagnin et al. 2025 (doi:10.1038/s41467-025-63417-y) · Guagnin et al. 2021 (doi:10.1016/j.jasrep.2021.103165) · UNESCO, Rock Art in the Hail Region (1472)",
              "Life-size camels carved up to 39 metres high on desert cliffs in northern Arabia, beside a camp about 12,000 years old. Why there, and how sure we are of the date.",
              ["#Arabia", "#RockArt", "#Prehistory", "#Archaeology", "#ArabiaUnearthed"])


# outline animals in profile, facing right, feet at y = 140 (horns drawn as a separate stroke)
IBEX = ([(0, 40), (20, 30), (110, 28), (130, 22), (150, 0), (168, -4), (182, 10), (176, 18), (158, 20), (148, 50), (146, 140), (138, 140), (134, 70), (60, 72),
         (46, 140), (38, 140), (30, 70), (12, 58)], [(156, -2), (140, -40), (112, -58), (88, -50)])
GAZELLE = ([(0, 46), (20, 36), (110, 34), (128, 30), (146, 4), (160, 0), (176, 12), (170, 18), (152, 16), (136, 52), (132, 140), (126, 140), (122, 72), (56, 74),
            (40, 140), (34, 140), (26, 72), (8, 62)], [(152, 0), (148, -26), (140, -44)])
DONKEY = ([(0, 44), (20, 34), (110, 34), (126, 30), (140, 10), (146, -14), (150, -14), (152, 0), (158, -16), (162, -14), (160, 4), (176, 22), (182, 40), (172, 46),
           (156, 36), (140, 56), (138, 140), (128, 140), (124, 76), (56, 78), (40, 140), (30, 140), (24, 74), (6, 64)], [])
AUROCHS = ([(0, 34), (14, 16), (60, 10), (112, 2), (142, 12), (170, 38), (190, 62), (186, 74), (166, 68), (152, 76), (150, 140), (138, 140), (134, 88), (64, 90),
            (52, 140), (40, 140), (34, 86), (10, 72), (2, 52)], [(166, 34), (178, 12), (198, 4)])


def _animal(spec, x, y, s, at=0, c="#f3e2c0", w=3):
    body, horn = spec
    out = [_beast(body, x, y, s, c, w, at)]
    if horn:
        out.append({"k": "line", "p": [[round(x + px * s, 1), round(y + (py - 140) * s, 1)] for px, py in horn], "c": c, "w": w + 1, "curve": True, "in": round(at + .6, 2), "fx": "draw", "dur": .6})
    return out


def camels_m():
    """The cliff camels as one continuous take (see mural.py): a twelve-storey cliff, life-size beasts, the camp below, and a carving no clock has read."""
    remix, I = _mur()
    ep = camels()
    PALE, ROCK = "#f3e2c0", "#5a4636"
    tower = [I.box(62, 700 + 45 * f, 52, 41, "#3b3028", "#cbbca8", 1.5, 2, round(4.6 - .1 * f, 2), fx="pop") for f in range(12)] + \
            [I.box(70 + 22 * j, 712 + 45 * f, 12, 16, "#e8c894", r=1, at=round(4.7 - .1 * f, 2), op=.8) for f in range(12) for j in range(2)]
    # 2 · 176 engravings, 130 of them life-size; then one to scale beside a person
    pill = lambda k, c, at, op=None: I.box(150 + 44 * (k % 16), 390 + 34 * (k // 16), 30, 16, c, r=8, at=at, op=op)
    marks = [pill(k, "#6a5a48", round(.2 + .004 * k, 3)) for k in range(176)] + [pill(k, "#e8c894", round(1.7 + .008 * k, 3)) for k in range(130)] + \
            [I.label(500, 350, "176 engravings", .3, I.BONE, 34), I.label(500, 800, "130 life-size", 2.5, "#e8c894", 34)]
    to_scale = [I.line([[100, 1330], [900, 1330]], 3.8, "#8c7152", 3, dur=.6), I.person(220, 1330, 255, 4.0), I.label(220, 1385, "1.7 m", 4.2, "#cbbca8", 28),
                _beast(CAMEL, 370, 1330, 1.6, PALE, 4, 4.4), I.line([[370, 1360], [821, 1360]], 5.2, "#e8c894", 2, dur=.5),
                I.label(596, 1400, "up to 3 m", 5.4, "#e8c894", 30)]
    life = {"base": "dark", "floor": 1330, "cam": [1, 500, 880], "els": marks + to_scale}
    # 3 · what they carved, engraved on a rock face, named as the narrator names them
    face = {"k": "poly", "p": [[70, 360], [300, 320], [700, 330], [930, 380], [940, 1180], [880, 1420], [120, 1420], [60, 1150]], "fill": ROCK, "c": "#a88b66", "w": 2, "in": .1, "curve": True}
    beasts = [_beast(CAMEL, 359, 650, 1.0, PALE, 4, .3), I.label(500, 700, "90 camels", .7, I.BONE, 32)] + \
             _animal(IBEX, 100, 960, .85, 1.0) + _animal(GAZELLE, 390, 960, .85, 1.3) + _animal(DONKEY, 660, 960, .85, 1.6) + \
             [I.label(180, 1010, "ibex", 1.2, I.BONE, 30), I.label(460, 1010, "gazelles", 1.5, I.BONE, 30), I.label(740, 1010, "wild donkeys", 1.8, I.BONE, 30)] + \
             [I.glow(500, 1250, 200, 2.1, .45)] + _animal(AUROCHS, 362, 1330, 1.4, 2.1, "#ffe9c8", 4) + [I.label(500, 1385, "one wild aurochs", 2.6, "#e8c894", 30)]
    bestiary = {"base": "dark", "cam": [1, 500, 880], "els": [face] + beasts}
    # 4 · the camp at the cliff foot: hearth, points, beads from afar, lakes between the dunes; Göbekli Tepe far to the north
    cliff = {"k": "poly", "p": [[600, 1000], [620, 520], [700, 380], [860, 340], [940, 360], [940, 1000]], "fill": "#6d5641", "c": "#a88b66", "w": 2, "in": .1}
    camp = [cliff, _beast(CAMEL, 650, 560, .6, PALE, 3, .3), I.line([[60, 1000], [940, 1000]], .2, "#c9a878", 3, dur=.8),
            I.box(330, 1002, 480, 288, "#4a3a2c", "#8a6a48", 2, 2, .6, fx="fill", dur=.8),
            I.glow(420, 1170, 90, 3.2, .8, "lamp"), I.oval(420, 1190, 46, 14, "#1f1812", at=3.2), I.dot(405, 1182, 5, "#ff9a5a", 3.4), I.dot(432, 1186, 4, "#ff9a5a", 3.5)] + \
           [I.tri(x, y, 13, r, "#cbbca8", 3.9 + .15 * k) for k, (x, y, r) in enumerate(((540, 1180, 0), (585, 1200, 40), (620, 1170, 80)))] + \
           [I.dot(690 + 18 * k, 1196 - 6 * (k % 2), 7, "#f2c98e", 4.6 + .08 * k) for k in range(5)] + \
           [I.arrow([[80, 1340], [500, 1340], [700, 1230]], 5.2, "#f2c98e", 2, "inferred", 1.2), I.label(90, 1320, "beads from 320 km away", 5.5, "#f2c98e", 28, "start")] + \
           [{"k": "poly", "p": [[60, 1000], [140, 880], [260, 860], [340, 1000]], "fill": "#b0916a", "c": "none", "w": 0, "in": 8.0, "curve": True, "fx": "rise"},
            {"k": "poly", "p": [[300, 1000], [400, 900], [520, 890], [600, 1000]], "fill": "#a3845e", "c": "none", "w": 0, "in": 8.2, "curve": True, "fx": "rise"},
            I.oval(320, 992, 70, 12, "#3f86a8", "#9fd0ff", 2, .9, 8.6), I.label(470, 1080, "c. 12,000 years", 7.2, "#e8c894", 30)]
    pillar = [I.arrow([[200, 760], [200, 470]], 3.4, "#9fd0ff", 3, dur=.8, curve=False), I.box(150, 560, 100, 30, "#cbbca8", r=3, at=1.4, fx="pop"),
              I.box(185, 590, 30, 140, "#cbbca8", r=2, at=1.3, fx="rise"), I.label(260, 650, "Göbekli Tepe", 2.0, "#9fd0ff", 30, "start"),
              I.label(260, 690, "far to the north", 3.5, "#cbbca8", 28, "start")]
    dig = {"base": "dark", "cam": [1, 500, 900], "els": camp}
    # 5 · the catch: the camp has a date, the carving only a span
    X = lambda ka: 140 + 720 * (16 - ka) / 10
    catch = {"base": "dark", "cam": [1, 500, 900], "els": [
        _beast(CAMEL, 359, 720, 1.0, PALE, 4, .2), I.glow(500, 600, 220, .2, .3)] + I.question(720, 470, 1.4, 90) + [
        I.line([[120, 1100], [880, 1100]], 2.0, "#e9dccb", 3, dur=1.0)] +
        [I.label(X(v), 1150, t, 2.2, "#cbbca8", 28) for v, t in ((16, "16,000"), (12, "12,000"), (8, "8,000 years ago"))] +
        [I.line([[X(12.8), 1100], [X(11.4), 1100]], 2.8, "#f2c98e", 16, dur=.6), I.label((X(12.8) + X(11.4)) / 2, 1060, "the camp", 3.0, "#f2c98e", 30),
         I.oval(X(12.1), 1010, 30, 10, "#1f1812", at=3.2), I.glow(X(12.1), 1000, 60, 3.2, .7, "lamp"),
         I.line([[X(12), 900], [X(8), 900]], 5.8, I.LILAC, 4, "claimed", 1.2), I.line([[X(12), 880], [X(12), 920]], 5.8, I.LILAC, 3, "claimed", .3, draw=False),
         I.line([[X(8), 880], [X(8), 920]], 6.4, I.LILAC, 3, "claimed", .3, draw=False), I.label((X(12) + X(8)) / 2, 866, "the carvings: when?", 6.2, I.LILAC, 30),
         I.arrow([[500, 760], [500, 818]], 5.8, I.LILAC, 2, "claimed", .4, False)]}
    lake = [I.oval(210, 1392, 110, 24, "#3f86a8", "#9fd0ff", 2, .9, 2.7), I.glow(210, 1385, 140, 2.7, .45),
            I.arrow([[400, 930], [300, 1100], [225, 1250], [210, 1356]], 3.0, "#9fd0ff", 4, "inferred", 1.0)]
    return remix(ep, scenes={2: life, 3: bestiary, 4: dig, 5: catch}, alias={6: 0}, cams={0: [1.05, 500, 950], 6: [1.08, 500, 960]},
                 drop=("para", "num", "title", "q", "cap"), adds={0: tower}, line_adds={(3, 1): (pillar, None), (5, 1): (lake, None)})


# ---------------------------------------------------------------- 14.04 Stone Age blueprints (desert kites)
def star(cx, cz, r0, r1, n=6):
    return [[cx + (r1 if k % 2 == 0 else r0) * math.cos(math.pi * k / n), cz + (r1 if k % 2 == 0 else r0) * math.sin(math.pi * k / n)] for k in range(2 * n)]


def kite_items(scale=1.0, pits=True):
    it = [{"t": "slab", "x0": -60, "x1": 60, "z0": -40, "z1": 40, "y": 0, "c": "#9a8264"},
          {"t": "line", "p": [[-58, .3, -36], [-20, .3, -12], [14, .3, -3]], "c": "#e6d2ac", "w": 3, "ground": True},
          {"t": "line", "p": [[-58, .3, 36], [-20, .3, 12], [14, .3, 3]], "c": "#e6d2ac", "w": 3, "ground": True},
          {"t": "prism", "pts": star(26, 0, 8, 13), "y": 0, "h": .8, "c": "#cdb58c", "edge": "rgba(0,0,0,.25)"},
          {"t": "flat", "pts": star(26, 0, 7.2, 12.2), "y": .82, "c": "#8a7458"}]
    if pits:
        for k in range(0, 12, 2):
            a = math.pi * k / 6
            if abs(math.cos(a) + 1) < .2:
                continue                                       # the entrance side has no pit
            it.append({"t": "cyl", "x": 26 + 14.5 * math.cos(a), "z": 14.5 * math.sin(a), "y": -.4, "r": 1.6, "h": .5, "c": "#2a2019", "n": 14, "edge": "rgba(0,0,0,0)"})
    r = rnd(5)
    for k in range(9):                                         # gazelles, as small dots, running in
        it.append({"t": "cyl", "x": -40 + k * 5 + r() * 3, "z": -6 + r() * 12, "y": 0, "r": .6, "h": .8, "c": "#f0dcb4", "n": 8, "edge": "rgba(0,0,0,.25)"})
    return it


def kites():
    s0 = iso(kite_items() + [L_(-30, 1, "walls: hundreds of metres to 5 km", GOLD, z=-24, dy=-24), L_(26, 1, "the pen, ringed by pits", "#cfe6ff", z=14, dy=44)],
             cam=[1, 500, 920], s=5.0, x=500, y=1000, az=-20, spin=1.1, el=.55, table=None)
    s1, v = arabia([("Jibal al-Khashabiyeh · Jordan", 37.0, 30.3, {"c": GOLD, "ly": -24}), ("Jebel az-Zilliyat · Saudi Arabia", 39.5, 29.5, {"c": GOLD, "a": "end", "lx": 18, "ly": 36}),
                    ("Amman", 35.93, 31.95, {"c": SCAN})], lon0=33, lon1=43, lat0=26, lat1=34)
    s1["els"] += [{"k": "line", "p": [v.p(37.0, 30.3), v.p(39.5, 29.5)], "c": AMBER, "w": 2, "op": .8, "in": 1.2},
                  {"k": "cap", "x": 500, "y": 1300, "t": "the two engraved stones · 267 km apart", "in": 1.4},
                  {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}]
    s2 = stat("6,721", "kites", "catalogued across 11 countries, from Arabia to Central Asia", "Globalkites · Barge et al. 2025")
    zoom = like(s0, cam=[1.9, 640, 1000], add=[{"k": "cap", "x": 500, "y": 1340, "t": "pits up to 4 m deep", "in": .6}])
    stone = {"k": "poly", "p": [[170, 760], [260, 640], [520, 600], [800, 650], [860, 820], [790, 1040], [500, 1100], [220, 1030]], "fill": "#6f6a62", "c": "#bdb5a8", "w": 2, "curve": True, "in": .1}
    plan = [{"k": "line", "p": [[260, 700], [470, 820], [560, 850]], "c": "#f0e6d2", "w": 3, "in": .6, "fx": "draw"},
            {"k": "line", "p": [[260, 1000], [470, 890], [560, 860]], "c": "#f0e6d2", "w": 3, "in": .7, "fx": "draw"},
            {"k": "poly", "p": [[560 + (70 if k % 2 == 0 else 44) * math.cos(math.pi * k / 6), 855 + (70 if k % 2 == 0 else 44) * math.sin(math.pi * k / 6)] for k in range(12)],
             "fill": "none", "c": "#f0e6d2", "w": 3, "in": .9, "fx": "draw"}]
    plan += [{"k": "circle", "x": 560 + 82 * math.cos(math.pi * k / 3), "y": 855 + 82 * math.sin(math.pi * k / 3), "r": 9, "fill": "#2a2019", "c": "#f0e6d2", "w": 2, "in": 1.2 + k * .1} for k in range(6) if k != 3]
    s4 = dark([stone] + plan + [{"k": "cap", "x": 500, "y": 540, "t": "a kite, engraved on stone · redrawn", "in": .1},
                                {"k": "label", "x": 500, "y": 1180, "t": "Saudi stone: 3.8 m long, at about 1:175", "c": "#e9dccb", "in": 1.6},
                                {"k": "label", "x": 500, "y": 1236, "t": "Jordan stone: 92 kg, at about 1:425", "c": "#e9dccb", "in": 1.8}])
    tl, ax = timeline(-10000, -2000, [(-10000, "10,000 BCE"), (-8000, "8000"), (-6000, "6000"), (-4000, "4000"), (-2000, "2000")], "Hunters, then herders")
    tl["els"] += event(ax, -9500, "Göbekli Tepe", row=1, c=SCAN, i=.3) + \
                 [{"k": "band", "x0": ax.x(-7500), "x1": ax.x(-7000), "y": 745, "h": 16, "c": GOLD, "t": "kites dated in Jordan", "in": .6}] + \
                 event(ax, -5300, "the mustatils", row=2, c=OCHRE, i=.9) + right(event(ax, -2560, "Great Pyramid", row=1, c=AMBER, i=1.2))
    s5 = tl
    s6 = like(s0, cam=[1.14, 500, 950])
    shots = [s0, s1, s2, zoom, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:DESERT KITES][sfx:boom][act:hushed, intrigued]About nine thousand years ago, hunters built stone ^traps so big they're best seen from the ^air.",
                      "[d:tension][cam:1.12|0|0][act:the kicker, leaning in][tune:fall]Then they drew the ^plans. To ^scale."], cut=False),
        B("world", 1, ["[d:calm][k:THE KITES][act:storytelling, plain]Pilots flying over the deserts@noun of Jordan in the {1920s|nineteen twenties} spotted strange shapes on the ^ground. [act:light]They called them ^kites.",
                       "[d:build][go:2|0][act:counting, impressed]Today, more than six thousand seven hundred are ^known."]),
        B("collision", 3, ["[d:build][k:THE TRAP][act:vivid, building]Two long stone walls funnel ^gazelles into a pen. [act:precise, grave]Around it, pits up to four metres ^deep."]),
        B("cost", 4, ["[d:build][k:THE PLANS][act:the reveal, delighted]In {2023|twenty twenty-three}, a team described two engraved stones, one in ^Jordan, one in Saudi ^Arabia. [act:precise, impressed]Each shows a kite, walls, pen and pits, drawn close@adj to ^scale.",
                      "[d:aside][act:context, wonder]Possibly the oldest known scale plans in human ^history."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:fair, precise]Dates from the pits in Jordan put the kites around nine thousand years ^ago. [act:the open question]But were the stones plans for ^building, or maps of traps already ^there? [act:plain][tune:fall]Nobody can say ^yet."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]Stone Age ^blueprints? [act:the verdict, measured][tune:fall]*Strong ^evidence* for drawings to scale. [act:fair]Blueprint is still a ^guess.",
                     "[d:tension][p:0.93][act:the last word, a small smile][tune:fall]But someone, nine thousand years ago, thought like an ^architect."]),
    ]
    return EP("desert-kites", "14.04", "Stone Age Blueprints", "desert-kites", "strong", "Did Stone Age hunters draw scale plans of their giant desert traps?", "Plans drawn to *scale*, 9,000 years ago.", beats, shots,
              "Crassard et al. 2023 (doi:10.1371/journal.pone.0277927) · Crassard et al. 2022 (doi:10.1007/s10963-022-09165-z) · Abu-Azizeh et al. 2026 (doi:10.1007/s12520-026-02409-5) · Barge et al. 2025 (doi:10.5334/joad.150)",
              "Giant stone hunting traps in the deserts of Jordan and Arabia, and two engraved stones that draw them to scale, about 9,000 years ago. The oldest plans, or maps of traps already built?",
              ["#Archaeology", "#Arabia", "#Jordan", "#AncientEngineering", "#ArabiaUnearthed"])


def _kite_plan(cx, cy, s, at=0, c="#f0e6d2", w=3, style="known", pits=True, dur=1.0):
    """A desert kite in plan, pen at (cx, cy), the two walls opening upward (s = 1: about 300 x 300 px)."""
    P = lambda u, v: [round(cx + u * s, 1), round(cy + v * s, 1)]
    els = [{"k": "line", "p": [P(-150, -300), P(-50, -110), P(-14, -46)], "c": c, "w": w, "style": style, "in": at, "fx": "draw", "dur": dur},
           {"k": "line", "p": [P(150, -300), P(50, -110), P(14, -46)], "c": c, "w": w, "style": style, "in": round(at + .1, 2), "fx": "draw", "dur": dur},
           {"k": "poly", "p": [P((44 if k % 2 == 0 else 28) * math.cos(math.pi * k / 6 - math.pi / 2), (44 if k % 2 == 0 else 28) * math.sin(math.pi * k / 6 - math.pi / 2)) for k in range(12)],
            "fill": "none", "c": c, "w": w, "style": style, "in": round(at + dur * .7, 2), "fx": "draw", "dur": dur * .7}]
    if pits:
        els += [{"k": "circle", "x": P(56 * math.cos(math.radians(a)), 0)[0], "y": P(0, 56 * math.sin(math.radians(a)))[1], "r": round(max(2.5, 8 * s), 1), "fill": "#1f1812", "c": c,
                 "w": max(1.5, w * .7), "style": style, "in": round(at + dur * 1.2 + .08 * k, 2), "fx": "pop"} for k, a in enumerate((-30, 30, 90, 150, 210))]
    return els


def kites_m():
    """The desert kites as one continuous take (see mural.py): spotted from a plane, counted across Asia, worked as a trap, engraved to scale, and an open question of order."""
    remix, I = _mur()
    ep = kites()
    PALE, SANDY = "#f0e6d2", "#e8d3a8"
    hero = copy.deepcopy(ep["shots"][0])
    for e in hero["els"]:
        if e.get("k") == "iso":
            e["spin"] = .3
    m = copy.deepcopy(ep["shots"][1])
    m["els"] = [e for e in m["els"] if not (e.get("k") == "line" and e.get("in") == 1.2) and e.get("k") != "cap"]
    v = View(33, 43, 26, 34, (40, 330, 920, 900))
    (ax_, ay_), (bx_, by_) = v.p(33.6, 31.2), v.p(42.4, 30.2)
    plane = [I.line([[ax_, ay_], [(ax_ + bx_) / 2, ay_ - 60], [bx_, by_]], .6, I.BLUE, 3, "inferred", 2.4, True),
             {"k": "poly", "p": [[bx_ + 26, by_], [bx_ - 18, by_ - 5], [bx_ - 26, by_ - 16], [bx_ - 30, by_ - 4], [bx_ - 30, by_ + 4], [bx_ - 26, by_ + 16], [bx_ - 18, by_ + 5]],
              "fill": I.BONE, "c": "none", "w": 0, "in": 2.8, "fx": "pop"},
             {"k": "poly", "p": [[bx_ + 2, by_ - 3], [bx_ - 8, by_ - 30], [bx_ - 14, by_ - 30], [bx_ - 10, by_ - 3], [bx_ - 10, by_ + 3], [bx_ - 14, by_ + 30], [bx_ - 8, by_ + 30], [bx_ + 2, by_ + 3]],
              "fill": I.BONE, "c": "none", "w": 0, "in": 2.8, "fx": "pop"}] + _kite_plan(*v.p(38.2, 31.7), .22, 4.4, SANDY, 2) + _kite_plan(*v.p(36.8, 29.6), .2, 4.8, SANDY, 2)
    # 2 · from Arabia to Central Asia: the sweep, then every mark = 100 kites
    wide = View(28, 76, 8, 48, (40, 320, 920, 700))
    sweep = [{"k": "map", "land": wide.land(), "in": -1},
             {"k": "arrow", "p": [wide.p(37, 30), wide.p(44, 34), wide.p(53, 38), wide.p(63, 42)], "curve": True, "c": I.AMBER, "w": 4, "in": 2.2, "fx": "draw", "dur": 1.6},
             {"k": "arrow", "p": [wide.p(37, 30), wide.p(42, 24), wide.p(46, 19)], "curve": True, "c": I.AMBER, "w": 4, "in": 2.4, "fx": "draw", "dur": 1.2},
             I.glow(*wide.p(37, 30), 60, 2.0, .8), I.label(*wide.p(64, 45.5), "Central Asia", 3.2, "#e8c894", 30, st="ital"),
             I.label(*wide.p(44, 17), "Arabia", 3.0, "#e8c894", 30, st="ital")]
    tally = [I.box(110, 1080, 780, 340, "rgba(13,11,9,.72)", "#5a4a3a", 1.5, 14, .1)] + sum([_kite_plan(150 + 44 * (k % 17), 1140 + 64 * (k // 17), .1, round(.2 + .022 * k, 3), SANDY, 2, pits=False, dur=.3) for k in range(67)], []) + \
            [I.label(500, 1395, "6,721 kites · each mark = 100", 1.8, I.BONE, 30)]
    count = {"base": "map", "cam": [1, 500, 880], "els": sweep + tally}
    # 3 · how a kite works, in plan: the funnel, the herd, the pen, the pits; and a pit cut open beside a person
    herd = [I.dot(x, y, 9, "#e8c894", round(3.2 + .1 * k, 2)) for k, (x, y) in enumerate(((420, 470), (520, 450), (610, 500), (470, 560), (560, 590), (500, 680), (440, 640)))]
    run = [I.arrow([[500, 520], [500, 760], [500, 940]], 3.6, "#e8c894", 3, "inferred", 1.2, False)]
    pit = [I.line([[690, 1220], [930, 1220]], 5.4, SANDY, 3, dur=.4),
           {"k": "poly", "p": [[760, 1220], [764, 1400], [856, 1400], [860, 1220]], "fill": "#1f1812", "c": SANDY, "w": 2, "in": 5.6, "fx": "fill", "dur": .8},
           I.person(725, 1220, 85, 6.2), I.line([[880, 1222], [880, 1398]], 6.4, "#e9dccb", 2, dur=.4), I.label(890, 1318, "4 m", 6.6, "#e9dccb", 30, "start"),
           I.line([[607, 1122], [700, 1180], [760, 1225]], 5.2, "#e9dccb", 2, "inferred", .5, True)]
    pits = [I.dot(round(500 + 123 * math.cos(math.radians(a)), 1), round(1060 + 123 * math.sin(math.radians(a)), 1), 18, "#1f1812", round(4.9 + .1 * k, 2)) for k, a in enumerate((-30, 30, 90, 150, 210))] + \
           [I.ring(round(500 + 123 * math.cos(math.radians(a)), 1), round(1060 + 123 * math.sin(math.radians(a)), 1), 18, round(4.9 + .1 * k, 2), PALE, 3, dur=.4) for k, a in enumerate((-30, 30, 90, 150, 210))]
    trap = {"base": "plan", "north": False, "cam": [1, 500, 880], "els": _kite_plan(500, 1060, 2.2, .3, PALE, 5, pits=False, dur=1.4) +
            [I.label(500, 350, "walls: up to 5 km", 2.2, SANDY, 30)] + herd + run + [I.glow(500, 1060, 140, 4.2, .5)] + pits + pit}
    # 4 · two engraved stones, to scale beside a person; the Saudi plan, scaled up about 175 times
    jord = {"k": "poly", "p": [[85, 1180], [80, 1112], [108, 1062], [188, 1052], [222, 1100], [214, 1180]], "fill": "#6f6a62", "c": "#bdb5a8", "w": 2, "curve": True, "in": 1.6}
    saud = {"k": "poly", "p": [[320, 1180], [330, 950], [420, 870], [700, 860], [860, 900], [890, 1040], [886, 1180]], "fill": "#77706a", "c": "#bdb5a8", "w": 2, "curve": True, "in": 2.6}
    stones = [I.line([[60, 1180], [940, 1180]], .2, "#8c7152", 3, dur=.6), jord, saud, I.person(268, 1180, 255, 3.2), I.label(150, 1235, "Jordan", 1.8, I.BONE, 30),
              I.label(605, 1290, "Saudi Arabia", 2.9, I.BONE, 30), I.line([[320, 1210], [886, 1210]], 3.4, "#e9dccb", 2, dur=.6), I.label(605, 1245, "3.8 m", 3.6, "#e9dccb", 28)] + \
             _kite_plan(150, 1150, .26, 3.6, PALE, 2, dur=.6) + _kite_plan(605, 1112, .72, 3.8, PALE, 3, dur=1.0) + \
             _kite_plan(605, 700, 1.35, 6.8, I.AMBER, 3, "inferred", dur=1.2) + \
             [I.arrow([[605, 1040], [605, 800]], 6.4, I.AMBER, 3, "inferred", .6, False), I.label(700, 760, "× 175", 8.0, I.AMBER, 40, "start", st="serif")]
    shine = [I.glow(150, 1120, 90, .3, .7), I.glow(605, 1060, 220, .5, .6)]
    plans = {"base": "dark", "floor": 1180, "cam": [1, 500, 880], "els": stones}
    # 5 · which came first? plan, then build; or build, then map
    icon_stone = lambda x, y, at: [{"k": "poly", "p": [[x - 70, y + 50], [x - 76, y - 20], [x - 40, y - 56], [x + 60, y - 50], [x + 78, y], [x + 64, y + 52]], "fill": "#6f6a62", "c": "#bdb5a8", "w": 2, "curve": True, "in": at}] + \
                                  _kite_plan(x, y + 34, .26, at + .2, PALE, 2, dur=.5)
    icon_trap = lambda x, y, at: [I.box(x - 90, y - 60, 180, 120, "#9a8264", r=8, at=at)] + _kite_plan(x, y + 38, .3, at + .2, "#3b3028", 3, dur=.5)
    pitd = [I.line([[260, 640], [740, 640]], .2, SANDY, 3, dur=.6), {"k": "poly", "p": [[420, 640], [430, 800], [570, 800], [580, 640]], "fill": "#3b3028", "c": SANDY, "w": 2, "in": .3, "fx": "fill", "dur": .6}] + \
           [I.glow(500, 782, 70, 1.6, .9, "lamp"), I.dot(500, 784, 9, "#ffd9a0", 1.6)] + \
           [I.line([[432, 800 - 26 * j], [568, 800 - 26 * j]], round(2.0 + .3 * j, 2), "#8a6a48", 3, draw=False) for j in range(1, 6)] + \
           [I.arrow([[620, 784], [700, 720]], 4.4, "#e8c894", 2, dur=.4, curve=False), I.label(710, 712, "c. 9,000 years", 4.6, "#e8c894", 30, "start")]
    order = icon_stone(230, 1000, 6.6) + [I.arrow([[330, 1000], [640, 1000]], 7.0, I.GREEN, 3, "inferred", .8, False)] + icon_trap(760, 1000, 7.3) + \
            [I.label(500, 1110, "plan, then build?", 7.6, I.GREEN, 30)] + \
            icon_trap(240, 1260, 8.8) + [I.arrow([[340, 1260], [650, 1260]], 9.2, I.AMBER, 3, "inferred", .8, False)] + icon_stone(770, 1260, 9.5) + \
            [I.label(500, 1370, "build, then map?", 9.8, I.AMBER, 30)] + I.question(905, 1170, 10.9, 64)
    first = {"base": "dark", "cam": [1, 500, 900], "els": pitd + order}
    arch = [{"k": "poly", "p": [[620, 380], [620, 620], [860, 620]], "fill": "none", "c": I.AMBER, "w": 3, "in": 3.4, "fx": "draw", "dur": .8},
            {"k": "poly", "p": [[650, 450], [650, 590], [790, 590]], "fill": "none", "c": I.AMBER, "w": 2, "in": 3.6, "fx": "draw", "dur": .6}] + \
           _kite_plan(330, 600, .55, 1.2, I.AMBER, 3, "inferred", dur=1.0) + [I.glow(480, 520, 240, 1.2, .35)]
    return remix(ep, scenes={0: hero, 1: m, 2: count, 3: trap, 4: plans, 5: first}, alias={6: 0}, cams={0: [1.15, 500, 980], 6: [1.12, 500, 920]},
                 drop=("para", "num", "title", "q", "cap"), adds={1: plane}, line_adds={(3, 1): (shine, None), (5, 1): (arch, None)})


# ---------------------------------------------------------------- 14.05 The king who moved to Arabia (Nabonidus at Tayma)
def nabonidus():
    L_half = [[-4.6, -3.4], [-.1, -3.6], [-.1, 3.5], [-4.2, 3.2], [-4.9, 0]]
    R_half = [[.1, -3.6], [4.5, -3.2], [4.9, .2], [4.4, 3.4], [.1, 3.5]]
    shrink = lambda P, k: [[(x - sum(p[0] for p in P) / len(P)) * k + sum(p[0] for p in P) / len(P), (z - sum(p[1] for p in P) / len(P)) * k + sum(p[1] for p in P) / len(P)] for x, z in P]
    rock = [{"t": "slab", "x0": -11, "x1": 11, "z0": -8, "z1": 8, "y": 0, "c": "#b8925f"},
            {"t": "prism", "pts": shrink(L_half, .5), "y": 0, "h": 1.2, "c": "#8f6c46", "edge": "rgba(0,0,0,.3)"},
            {"t": "prism", "pts": shrink(R_half, .5), "y": 0, "h": 1.0, "c": "#8f6c46", "edge": "rgba(0,0,0,.3)"},
            {"t": "prism", "pts": L_half, "y": 1.2, "h": 5.0, "c": "#c79d6a", "edge": "rgba(0,0,0,.3)"},
            {"t": "prism", "pts": R_half, "y": 1.0, "h": 5.3, "c": "#c79d6a", "edge": "rgba(0,0,0,.3)"},
            {"t": "person", "x": 6.5, "y": 0, "z": 5, "h": 1.7},
            L_(0, 7, "Al-Naslaa · c. 6 m tall · schematic", GOLD, z=-3.6, dy=-26), L_(0, 3, "a natural joint, widened by wind", "#cfe6ff", z=3.6, dy=48)]
    s0 = iso(rock, cam=[1, 500, 900], s=36, x=500, y=1080, az=-40, spin=1.0, el=.3, table=None)
    s1, v = arabia([("Babylon", 44.42, 32.54, {"c": RED}), ("Tayma", 38.544, 27.63, {"c": GOLD}), ("Harran", 39.031, 36.865, {"c": SCAN}),
                    ("al-Hait", 40.476, 25.98, {"a": "end", "lx": -18, "ly": 30}), ("Dadan · AlUla", 37.916, 26.647, {"a": "end", "lx": -18})],
                   lon0=33, lon1=48, lat0=23, lat1=38)
    s1["els"] += [{"k": "arrow", "p": [v.p(44.2, 32.4), v.p(41.6, 30.6), v.p(38.9, 27.9)], "curve": True, "c": AMBER, "w": 2.4, "in": 1.6, "fx": "draw"},
                  {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}]
    s2 = stat("10", "years", "Nabonidus' own count of his stay among the oases of Arabia, c. 552–543 BCE", "the Harran stela")
    s3 = tablet(text_rows=13)
    s3["els"] += [{"k": "person", "x": 700, "y": 1110, "h": 150, "t": False, "color": "#5a4632", "in": .6},
                  {"k": "cap", "x": 500, "y": 1260, "t": "al-Hait: the king, and 26 lines", "in": 1.0},
                  {"k": "label", "x": 500, "y": 1320, "t": "the longest cuneiform text found in Saudi Arabia · redrawn", "st": "small", "c": "#b9aa97", "in": 1.3}]
    tl, ax = timeline(-560, -530, [(-560, "560 BCE"), (-550, "550"), (-540, "540"), (-530, "530")], "A king away from home")
    tl["els"] += event(ax, -556, "Nabonidus becomes king", row=2, c=AMBER, i=.3) + \
                 [{"k": "band", "x0": ax.x(-552), "x1": ax.x(-543), "y": 745, "h": 16, "c": GOLD, "t": "at Tayma", "in": .6}] + \
                 right(event(ax, -539, "Babylon falls to Persia", row=1, c=RED, i=.9))
    s4 = tl
    s5 = dark(grp("why go?", AMBER, ["trade: the incense roads", "faith: the moon god Sîn", "illness, in one later text"]))
    s6 = like(s0, cam=[1.15, 500, 940])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:NEAR TAYMA · ARABIA][sfx:boom][act:playful, intrigued]Near an Arabian oasis stands a boulder split so cleanly, people call it ^laser-cut. [act:a wry turn, lighter]It isn't. Wind@air and a natural crack did ^that.",
                      "[d:tension][cam:1.12|0|0][act:leaning in, the real hook][tune:fall]The real mystery here is a ^king."], cut=False),
        B("world", 1, ["[d:calm][k:TAYMA][act:storytelling, plain]Around {552|five fifty-two} BCE, Nabonidus, the last king of ^Babylon, left his capital. [act:the surprise, measured]He went to ^Tayma, an oasis in north-west ^Arabia.",
                       "[d:build][go:2|0][act:precise]By his own count, he stayed ^ten years."]),
        B("collision", 3, ["[d:build][k:THE PROOF][act:building, confident]Babylon's chronicle keeps repeating it: the king was in ^Tema. [act:the reveal, delighted]And archaeologists have found his name in Arabia: at Tayma, and on a rock at al-Hait, beside a carving of the king ^himself."]),
        B("cost", 4, ["[d:build][k:THE COST][act:grave, measured]While he was away, Babylon's great New Year festival was not ^held. [act:the consequence, quiet][tune:fall]A few years after he came back, Persia took the ^city."]),
        B("reversal", 5, ["[d:reveal][k:WHY?][act:the crux, curious][tune:fall]So why ^go? [act:counting them off, even][tune:level]Trade: Tayma sat on the ^incense roads. [tune:level]Faith: he was devoted to the moon god, ^Sîn. [act:the third, careful][tune:fall]Or illness, as one of the Dead Sea ^Scrolls remembers him."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A king of Babylon, living in ^Arabia? [act:the verdict, firm][tune:fall]*^Established*. [act:fair]His reason is still an open ^question.",
                     "[d:tension][p:0.93][act:the last word, warm, a small smile][tune:fall]Even kings, it seems, needed a change of ^air."]),
    ]
    return EP("nabonidus-tayma", "14.05", "The King Who Moved to Arabia", "nabonidus-tayma", "solid", "Why did Nabonidus, the last king of Babylon, spend ten years at the Arabian oasis of Tayma?", "The king who *left* Babylon.", beats, shots,
              "Eichmann, Hausleiter & Schaudig 2006 (doi:10.1111/j.1600-0471.2006.00269.x) · Hausleiter & Schaudig 2016 · Nabonidus Chronicle (ABC 7) · Harran stela · Macdonald (ed.) 2020, Taymāʾ II · 4Q242",
              "The last king of Babylon left his capital and lived for about ten years at the oasis of Tayma, in Arabia. The inscriptions that place him there, and the three reasons historians give.",
              ["#Babylon", "#Arabia", "#AncientHistory", "#Archaeology", "#ArabiaUnearthed"])



def nabonidus_m():
    """Nabonidus at Tayma as one continuous take (see mural.py): the wind's work on a rock, ten years counted, the king's name in stone, a festival missed, three reasons."""
    remix, I = _mur()
    ep = nabonidus()
    CLAY, STONE, PALE = "#b9a47c", "#8d7a64", "#f0e6d2"
    hero = copy.deepcopy(ep["shots"][0])
    for e in hero["els"]:
        if e.get("k") == "iso":
            e["spin"] = .25
    wind = sum([[I.arrow([[70, y], [260, y - 10], [470, y + 4]], round(5.8 + .25 * k, 2), I.BLUE, 3, "inferred", 1.0, True)] +
                [I.dot(110 + 80 * j + 20 * k, y - 8 + 6 * (j % 2), 3.5, "#e8d3a8", round(6.1 + .25 * k + .06 * j, 2)) for j in range(4)]
                for k, y in enumerate((880, 925, 970))], [])
    # 2 · ten years, by his own count: a stone monument, and the tally carved beside it
    stela = [{"k": "poly", "p": [[150, 1150], [150, 600], [190, 540], [275, 515], [360, 540], [400, 600], [400, 1150]], "fill": STONE, "c": "#bdb5a8", "w": 2, "curve": False, "in": .2},
             {"k": "glyphs", "x": 185, "y": 620, "w": 180, "h": 440, "rows": 11, "cols": 4, "kind": "cuneiform", "c": "#2a2019", "in": .5}]
    tally = []
    for g in range(2):
        x0 = 520 + 190 * g
        tally += [I.line([[x0 + 30 * j, 700], [x0 + 30 * j, 900]], round(1.4 + .11 * (5 * g + j), 2), "#e8c894", 8, dur=.25) for j in range(4)]
        tally += [I.line([[x0 - 16, 870], [x0 + 106, 730]], round(1.4 + .11 * (5 * g + 4), 2), "#e8c894", 8, dur=.25)]
    count = {"base": "dark", "cam": [1, 500, 880], "els": stela + tally + [I.glow(650, 800, 200, 2.4, .4), I.label(650, 990, "10 years", 2.6, "#e8c894", 44, st="serif"),
             I.label(650, 1045, "c. 552–543 BCE", 2.9, "#cbbca8", 28)]}
    # 3 · the evidence: Babylon's chronicle repeating one line; his name at Tayma; the king carved at al-Hait, with 26 lines
    tab = [I.box(110, 400, 320, 480, CLAY, "#8a6a48", 2, 22, .2), {"k": "glyphs", "x": 140, "y": 430, "w": 260, "h": 420, "rows": 12, "cols": 6, "kind": "cuneiform", "c": "#3b2a1c", "in": .4},
           I.label(270, 940, "the chronicle", 1.0, I.BONE, 30)]
    tab += [{"k": "hl", "x": 126, "y": 428 + 35 * r, "w": 288, "h": 30, "in": round(2.7 + .4 * j, 2)} for j, r in enumerate((1, 4, 7, 10))]
    frag = [{"k": "poly", "p": [[140, 1080], [210, 1040], [330, 1050], [380, 1120], [330, 1210], [180, 1220]], "fill": STONE, "c": "#bdb5a8", "w": 2, "in": 6.2, "fx": "pop"},
            {"k": "glyphs", "x": 190, "y": 1080, "w": 150, "h": 100, "rows": 3, "cols": 4, "kind": "cuneiform", "c": "#2a2019", "in": 6.3}, I.label(260, 1270, "Tayma", 6.4, I.BONE, 30)]
    rock = [{"k": "poly", "p": [[500, 1240], [480, 820], [540, 560], [700, 500], [880, 560], [920, 900], [900, 1240]], "fill": "#7d6a56", "c": "#bdb5a8", "w": 2, "curve": True, "in": 7.6},
            I.person(620, 1150, 330, 9.6, c="#cdb48a"), I.glow(620, 1000, 150, 9.6, .4), I.label(700, 1300, "al-Hait", 7.9, I.BONE, 30)]
    rock += [I.line([[730 + 80 * (k // 13), 640 + 36 * (k % 13)], [790 + 80 * (k // 13), 640 + 36 * (k % 13)]], round(10.8 + .04 * k, 2), "#2a2019", 5, dur=.15) for k in range(26)]
    proof = {"base": "dark", "cam": [1, 500, 880], "els": tab + frag + rock}
    # 4 · away: the ten years at Tayma on a strip of years, no New Year festival, then Persia takes the city
    Y = lambda yr: 95 + 45 * (556 - yr)
    away = [I.box(Y(yr), 900, 38, 50, "#e8c894" if 543 <= yr <= 552 else "#4a4038", r=4, at=round(.2 + .03 * (556 - yr), 2), op=.9 if 543 <= yr <= 552 else None) for yr in range(556, 538, -1)] + \
           [I.label(Y(556) + 19, 1000, "556 BCE", .6, "#cbbca8", 28), I.label(Y(539) + 19, 1000, "539", .6, "#cbbca8", 28),
            I.line([[Y(552), 870], [Y(552), 850], [Y(543) + 38, 850], [Y(543) + 38, 870]], .9, "#e8c894", 3, dur=.6), I.label((Y(552) + Y(543) + 38) / 2, 830, "at Tayma", 1.2, "#e8c894", 30)]
    lamp = [{"k": "poly", "p": [[420, 700], [580, 700], [560, 740], [440, 740]], "fill": "none", "c": "#cbbca8", "w": 3, "style": "claimed", "in": 1.6},
            {"k": "poly", "p": [[500, 690], [488, 660], [500, 620], [512, 660]], "fill": "none", "c": "#cbbca8", "w": 3, "style": "claimed", "in": 1.8},
            I.strike(400, 760, 600, 610, 2.2), I.label(500, 570, "no New Year festival", 2.4, "#cbbca8", 30)]
    city = [I.box(560, 1170, 300, 150, "#6f5a44", "#cbbca8", 2, 2, 5.0)] + [I.box(560 + 40 * j, 1150, 22, 22, "#6f5a44", "#cbbca8", 2, 1, 5.0) for j in range(8)] + \
           [I.label(710, 1360, "Babylon", 5.2, I.BONE, 30), I.arrow([[Y(539) + 19, 960], [Y(539) + 19, 1100], [860, 1160]], 6.6, I.RED, 4, dur=.8),
            I.glow(710, 1240, 170, 7.0, .7, "red"), I.label(300, 1250, "Persia takes the city", 7.2, I.RED, 30)]
    gone = {"base": "dark", "cam": [1, 500, 900], "els": away + lamp + city}
    # 5 · three reasons, one picture each
    road = [I.line([[120, 640], [300, 600], [520, 650], [880, 610]], 2.3, "#c9a878", 3, "inferred", 1.0, True), _beast(CAMEL, 380, 640, .4, PALE, 3, 2.5)] + \
           [I.line([[396 + 12 * j, 560], [404 + 12 * j, 530], [392 + 12 * j, 500], [402 + 12 * j, 470]], round(2.9 + .1 * j, 2), "#e8dcc2", 2, "inferred", .6, True) for j in range(3)] + \
           [I.label(500, 720, "trade", 2.7, "#e8c894", 34)]
    moon = [I.glow(500, 900, 140, 6.0, .6, "lamp"), I.oval(500, 900, 70, 70, "#efe8da", at=6.0), I.oval(530, 885, 66, 66, "#2b2219", at=6.0), I.label(500, 1020, "faith", 6.2, "#e8c894", 34)]
    scroll = [I.box(400, 1150, 200, 110, "#d8c9a8", "#8a7a66", 2, 4, 8.7), I.box(385, 1140, 26, 130, "#b9a47c", "#8a7a66", 2, 12, 8.7), I.box(589, 1140, 26, 130, "#b9a47c", "#8a7a66", 2, 12, 8.7)] + \
             [I.line([[425, 1180 + 22 * j], [575, 1180 + 22 * j]], round(8.9 + .1 * j, 2), "#6a5a48", 3, dur=.3) for j in range(3)] + [I.label(500, 1320, "illness?", 9.0, "#e8c894", 34)]
    why = {"base": "dark", "cam": [1.15, 500, 900], "els": road + moon + scroll}
    palm = [I.line([[850, 700], [862, 580], [850, 470]], .3, "#8a6a48", 7, curve=True, dur=.6)] + \
           [I.line([[850, 470], [850 + 70 * math.cos(a), 470 + 34 * math.sin(a) + 26]], .8 + .05 * k, "#8fd9b0", 4, curve=False, dur=.4) for k, a in enumerate((-2.9, -2.4, -1.9, -1.2, -.6, -.2))] + \
           [I.arrow([[120, 520 + 40 * k], [420, 510 + 40 * k], [640, 530 + 40 * k]], round(1.0 + .2 * k, 2), I.BLUE, 2, "inferred", 1.0, True) for k in range(3)]
    return remix(ep, scenes={0: hero, 2: count, 3: proof, 4: gone, 5: why}, alias={6: 0}, cams={0: [1.1, 500, 960], 6: [1.12, 500, 920]},
                 drop=("para", "num", "title", "q", "cap"), adds={0: wind}, line_adds={(5, 1): (palm, None)})

# ---------------------------------------------------------------- 14.06 The island of tombs (Dilmun)
def dilmun():
    f = [{"t": "slab", "x0": -70, "x1": 70, "z0": -46, "z1": 46, "y": 0, "c": "#b39a74"}]
    r = rnd(21); pts = []
    while len(pts) < 70:
        x, z = -64 + r() * 128, -40 + r() * 80
        if abs(x - 40) < 20 and abs(z + 18) < 16:
            continue                                           # room for the royal mounds
        if all((x - a) ** 2 + (z - b) ** 2 > 60 for a, b in pts):
            pts.append((x, z))
    for x, z in pts:
        rr = 2.3 + r() * 2.2
        f += [{"t": "cyl", "x": x, "z": z, "y": 0, "r": rr, "h": .7, "c": "#cdb48a", "n": 14, "edge": "rgba(0,0,0,.18)"},
              {"t": "cyl", "x": x, "z": z, "y": .7, "r": rr * .6, "h": .5, "c": "#d6bf96", "n": 14, "edge": "rgba(0,0,0,.18)"}]
    for x, z, rr in ((34, -22, 13), (50, -10, 9)):
        f += [{"t": "cyl", "x": x, "z": z, "y": 0, "r": rr, "h": 3.2, "c": "#c2a57a", "n": 28, "edge": "rgba(0,0,0,.22)"},
              {"t": "cyl", "x": x, "z": z, "y": 3.2, "r": rr * .7, "h": 2.6, "c": "#cdb48a", "n": 28, "edge": "rgba(0,0,0,.22)"}]
    f += [L_(-20, 2, "burial mounds · 4.5–9 m across · schematic", GOLD, z=-40, dy=-24), L_(34, 6, "royal mounds at A'ali · over 30 m", "#cfe6ff", z=-8, dy=50)]
    s0 = iso(f, cam=[1, 500, 920], s=4.2, x=500, y=1010, az=-22, spin=1.2, el=.5, table=None)
    s1, v = arabia([("Bahrain · Dilmun", 50.55, 26.1, {"c": GOLD}), ("Failaka", 48.333, 29.439, {"a": "end", "lx": -18}), ("Ur", 46.103, 30.962, {"c": SCAN})],
                   lon0=44, lon1=58, lat0=20, lat1=32)
    s1["els"] += [sea(v, 52.2, 27.4, "the Gulf"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}]
    s2 = stat("11,774", "mounds", "protected by UNESCO in 2019; built c. 2200–1750 BCE. Early estimates of the original total: about 75,000", "UNESCO World Heritage 1542")
    cup = {"k": "poly", "p": [[330, 700], [670, 700], [640, 1000], [600, 1060], [400, 1060], [360, 1000]], "fill": "#4d4a44", "c": "#bdb5a8", "w": 2, "in": .1}
    s3 = dark([cup, {"k": "glyphs", "x": 380, "y": 760, "w": 240, "h": 120, "rows": 3, "cols": 6, "kind": "cuneiform", "in": .5},
               {"k": "cap", "x": 500, "y": 600, "t": "a stone vessel · redrawn", "in": .1},
               {"k": "label", "x": 500, "y": 1150, "t": "'Yagli-El, servant of Inzak of Agarum'", "st": "serif", "size": 30, "c": "#e9dccb", "in": 1.2},
               {"k": "label", "x": 500, "y": 1210, "t": "a king of Dilmun, named in his own words", "st": "small", "c": "#b9aa97", "in": 1.5}])
    tl, ax = timeline(-2400, -1500, [(-2400, "2400 BCE"), (-2100, "2100"), (-1800, "1800"), (-1500, "1500")], "Five centuries of mounds")
    tl["els"] += [{"k": "band", "x0": ax.x(-2200), "x1": ax.x(-1750), "y": 745, "h": 16, "c": GOLD, "t": "the mound fields", "in": .3}] + \
                 event(ax, -2050, "royal mounds rise", row=1, c=AMBER, i=.6) + event(ax, -1700, "Yagli-El's tomb", row=2, c=SCAN, i=.9)
    s4 = tl
    s5 = dark(grp("the old idea", "#ff8a7a", ["an island of the dead", "for the whole region"]))
    s6 = like(s0, cam=[1.14, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:BAHRAIN][sfx:boom][act:hushed, wonder]A small island in the Gulf holds one of the densest ancient ^cemeteries on Earth.",
                      "[d:tension][cam:1.12|0|0][act:the question, leaning in][tune:rise]Was it where a whole region sent its ^dead?"], cut=False),
        B("world", 1, ["[d:calm][k:DILMUN][act:plain, orienting]This is ^Bahrain, heart of the Bronze Age land of ^Dilmun. [act:steady, factual]Between about {2200|twenty-two hundred} and {1750|seventeen fifty} BCE, its people raised burial mounds by the ^thousand.",
                       "[d:build][go:2|0][act:quietly astonished]Nearly twelve thousand are protected today. [act:plain]There may once have been ^seventy-five thousand."]),
        B("collision", 5, ["[d:build][k:THE THEORY][act:presenting it, fair]Far more graves than one island could ^fill, some scholars thought. [act:storytelling]And old Sumerian texts called Dilmun a pure, holy ^land. [act:the leap, even][tune:rise]So, an island of the dead, for all of ^Arabia?"]),
        B("cost", 4, ["[d:build][k:THE DIG][act:building, precise]Then, from {1954|nineteen fifty-four}, Danish archaeologists found what the theory ^lacked: towns, temples and a ^harbour. [act:the point, clear]The mounds were built by the island's own people, over five ^centuries."]),
        B("reversal", 3, ["[d:reveal][k:THE KINGS][act:the reveal, delighted]And the biggest mounds, at ^A'ali, belonged to ^kings. [act:precise]Stone vessels even give their ^names: Ri'mum, and Yagli-El, servant of the god ^Inzak."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]An island of the ^dead? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:warm, the other half][tune:fall]An island of the ^living, who honoured their dead for five hundred ^years.",
                     "[d:tension][p:0.93][act:the last word, gentle][tune:fall]And their kings still have their ^names."]),
    ]
    return EP("dilmun-mounds", "14.06", "Bahrain: Island of the Dead?", "dilmun-mounds", "debunked", "Was Bahrain a sacred burial island for the whole region, as once proposed?", "An island of *tombs*.", beats, shots,
              "UNESCO, Dilmun Burial Mounds (1542) · Laursen 2008 (doi:10.1111/j.1600-0471.2008.00298.x) · Højlund 2008 (doi:10.1111/j.1600-0471.2008.00299.x) · Laursen 2017, The Royal Mounds of A'ali in Bahrain",
              "Nearly 12,000 Bronze Age burial mounds survive on Bahrain, from perhaps 75,000. Was it an island where a whole region buried its dead? Excavation found towns, temples and named kings instead.",
              ["#Bahrain", "#Dilmun", "#Archaeology", "#AncientHistory", "#ArabiaUnearthed"])



def _mound(cx, base, w, h, at=0, fill="#cdb48a", c="#e8d3a8"):
    """A burial mound in profile: a low dome, w wide and h high, sitting on y = base."""
    pts = [[round(cx - w / 2 + w * k / 16, 1), round(base - h * math.sin(math.pi * k / 16) ** .8, 1)] for k in range(17)]
    return {"k": "poly", "p": pts, "fill": fill, "c": c, "w": 2, "in": at, "fx": "rise"}


def dilmun_m():
    """Dilmun as one continuous take (see mural.py): the mounds counted, the old idea drawn as arrows, the town that answered it, and the kings' mounds to scale."""
    remix, I = _mur()
    ep = dilmun()
    SANDY = "#e8d3a8"
    hero = copy.deepcopy(ep["shots"][0])
    for e in hero["els"]:
        if e.get("k") == "iso":
            e["spin"] = .3
    v = View(44, 58, 20, 32, (40, 330, 920, 900))
    # 2 · how many: every dot is 250 mounds; 47 survive (11,774), 300 may once have stood (75,000)
    cell = lambda k: (170 + 33 * (k % 20), 470 + 33 * (k // 20))
    count = [I.dot(*cell(k), 11, "#e8c894", round(.3 + .015 * k, 3)) for k in range(47)] + [I.label(500, 420, "today: 11,774", .9, "#e8c894", 32)]
    count += [I.ring(*cell(k), 10, round(1.3 + .005 * (k - 47), 3), "#8c7c68", 2, "claimed", .3) for k in range(47, 300)] + \
             [I.label(500, 1010, "once: perhaps 75,000", 2.4, "#cbbca8", 32), I.label(500, 1060, "each dot: 250 mounds", 2.6, "#8c7c68", 28)]
    clock = [I.ring(500, 1240, 80, 2.8, I.BONE, 3, dur=.8), I.line([[500, 1240], [500, 1180]], 3.2, I.BONE, 4, draw=False), I.line([[500, 1240], [548, 1240]], 3.2, I.BONE, 4, draw=False),
             I.label(500, 1370, "1 a minute: 8 days", 4.6, I.BONE, 30)] + [I.dot(500 + 80 * math.cos(math.pi * k / 6), 1240 + 80 * math.sin(math.pi * k / 6), 4, I.BONE, 3.0) for k in range(12)]
    many = {"base": "dark", "cam": [1, 500, 900], "els": count + clock}
    # the old idea, drawn on the map: the whole region sending its dead to one small island (claimed, dotted)
    bx, by = v.p(50.55, 26.1)
    claim = [I.arrow([v.p(*a), [bx + (12 if v.p(*a)[0] > bx else -12), by + (12 if v.p(*a)[1] > by else -12)]], round(3.4 + .25 * k, 2), I.LILAC, 3, "claimed", 1.0, True)
             for k, a in enumerate(((44.6, 30.4), (44.6, 26.4), (45.2, 22.2), (48.6, 21.0), (55.6, 22.4), (48.3, 29.0)))] + \
            [I.glow(bx, by, 90, 4.8, .6, "lamp"), I.label(bx + 30, by + 60, "an island of the dead?", 9.0, I.LILAC, 30, "start")]
    ux, uy = v.p(46.103, 30.962)
    claim = [I.box(ux - 30, uy - 120, 60, 80, "#b9a47c", "#8a6a48", 2, 8, 6.2), {"k": "glyphs", "x": ux - 22, "y": uy - 110, "w": 44, "h": 60, "rows": 4, "cols": 3, "kind": "cuneiform", "c": "#3b2a1c", "in": 6.3},
             I.label(ux + 44, uy - 70, "'a pure, holy land'", 6.6, SANDY, 28, "start", st="ital")] + claim
    # 4 · the dig: an island of the living (town, temple, harbour), and five centuries of mounds
    isl = {"k": "poly", "p": [[260, 420], [420, 360], [600, 380], [740, 470], [780, 640], [740, 880], [640, 1040], [480, 1080], [340, 1000], [250, 820], [220, 600]],
           "fill": "#9a8264", "c": SANDY, "w": 2, "curve": True, "in": .2}
    field = [I.dot(x, y, 7, "#cdb48a", round(.5 + .01 * k, 3)) for k, (x, y) in enumerate(I.scatter(60, 330, 650, 620, 960, 21))]
    town = [{"k": "house", "x": 330 + 46 * j, "y": 520 - 8 * (j % 2), "w": 40, "h": 30, "in": round(3.0 + .1 * j, 2)} for j in range(5)] + [I.label(350, 470, "town", 3.3, I.BONE, 28, "start")]
    temple = [I.box(560 + 26 * j, 470, 12, 70, SANDY, r=2, at=3.6, fx="rise") for j in range(4)] + [I.box(550, 456, 104, 16, SANDY, r=2, at=3.8, fx="pop"), I.label(602, 580, "temple", 3.9, I.BONE, 28)]
    port = [I.line([[760, 760], [860, 760]], 4.2, SANDY, 5, draw=False), {"k": "boat", "x": 860, "y": 820, "w": 110, "in": 4.4}, I.label(860, 880, "harbour", 4.6, I.BONE, 28)]
    folk = [I.person(400 + 34 * j, 600, 46, round(6.6 + .1 * j, 2)) for j in range(4)]
    X = lambda yr: 170 + 660 * (2200 - yr) / 450
    centuries = [I.line([[170, 1240], [830, 1240]], 8.4, "#8c7152", 3, dur=.6), I.label(170, 1290, "2200 BCE", 8.5, "#cbbca8", 28), I.label(830, 1290, "1750 BCE", 8.5, "#cbbca8", 28)] + \
                [_mound(X(2200 - 90 * j - 45), 1236, 90, 34 + 6 * j, round(8.8 + .35 * j, 2)) for j in range(5)] + [I.label(500, 1350, "five centuries", 10.4, "#e8c894", 30)]
    dig = {"base": "dark", "cam": [1, 500, 880], "els": [isl] + field + town + temple + port + folk + centuries}
    # 3 · the kings: ordinary mounds and a royal mound at A'ali, to scale beside a person; a stone vessel with a name
    kings = [I.line([[60, 820], [940, 820]], .2, "#8c7152", 3, dur=.6), _mound(140, 818, 180, 60, .4), _mound(280, 818, 90, 34, .5),
             _mound(620, 818, 600, 200, 1.0, "#c2a57a"), I.glow(620, 720, 220, 1.0, .35), I.person(370, 818, 34, 1.4), I.label(620, 884, "A'ali: over 30 m", 1.2, "#e8c894", 30),
             I.line([[320, 840], [920, 840]], 2.2, "#e9dccb", 2, dur=.6), I.line([[320, 830], [320, 850]], 2.2, "#e9dccb", 2, draw=False), I.line([[920, 830], [920, 850]], 2.2, "#e9dccb", 2, draw=False)] + \
            [{"k": "rect", "x": 320 + 600 * (1 - 23.77 / 30) / 2, "y": 912, "w": round(600 * 23.77 / 30, 1), "h": 46, "r": 2, "fill": "#4f7a7a", "c": "#e8f0dc", "sw": 2, "in": 3.0, "fx": "pop"},
             I.label(620, 996, "a tennis court", 3.2, "#9fd0ff", 28)]
    vessel = [{"k": "vase", "x": 500, "y": 1330, "h": 230, "w": 170, "profile": [[0, .5], [.06, .52], [.3, .5], [.7, .42], [.92, .3], [1, .26]], "in": 4.7, "fx": "rise"},
              {"k": "glyphs", "x": 440, "y": 1180, "w": 120, "h": 90, "rows": 3, "cols": 4, "kind": "cuneiform", "c": "#2a2019", "in": 5.0},
              I.label(500, 1400, "Yagli-El, servant of Inzak", 5.8, "#e8c894", 30, st="serif"), I.glow(500, 1220, 150, 5.6, .4)]
    royal = {"base": "dark", "cam": [1, 500, 900], "els": kings + vessel}
    names = [I.label(500, 480, "Ri'mum", .6, "#e8c894", 40, st="serif"), I.label(500, 550, "Yagli-El", 1.2, "#e8c894", 40, st="serif"), I.glow(500, 510, 200, .6, .35)]
    return remix(ep, scenes={0: hero, 2: many, 3: royal, 4: dig}, alias={5: 1, 6: 0}, cams={0: [1.15, 500, 980], 5: [1.15, 470, 760], 6: [1.12, 500, 920]},
                 drop=("para", "num", "title", "q", "cap"), beat_adds={2: (claim, [1.15, 470, 760])}, line_adds={(5, 1): (names, None)})

# ---------------------------------------------------------------- 14.07 The first complaint letter (Ea-nasir and Magan's copper)
def eanasir():
    s0 = tablet(text_rows=10, x=300, y=590, w=400, h=620)
    s0["els"] += [{"k": "cap", "x": 500, "y": 1290, "t": "Nanni to Ea-nasir · Ur, c. 1750 BCE · redrawn", "in": 1.0}]
    s1, v = arabia([("Ur", 46.103, 30.962, {"c": RED}), ("Dilmun · Bahrain", 50.52, 26.233, {"c": GOLD}), ("Magan · Bat, Oman", 56.745, 23.27, {"c": OCHRE, "a": "end", "lx": -18, "ly": 30})],
                   lon0=44, lon1=60, lat0=20, lat1=32.5)
    s1["els"] += [{"k": "arrow", "p": [v.p(56.4, 23.9), v.p(54.6, 26.4), v.p(51.2, 26.6)], "curve": True, "c": OCHRE, "w": 2.4, "in": 1.4, "fx": "draw"},
                  {"k": "arrow", "p": [v.p(50.3, 26.8), v.p(48.6, 29.2), v.p(46.5, 30.7)], "curve": True, "c": AMBER, "w": 2.4, "in": 2.0, "fx": "draw"},
                  sea(v, 52.4, 28.2, "the Gulf"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}]
    s2 = stat("c. 1750", "BCE", "a clay tablet, 11.6 × 5 cm, found at Ur. Now in the British Museum", "British Museum 131236")
    tw = [{"t": "slab", "x0": -18, "x1": 18, "z0": -18, "z1": 18, "y": 0, "c": "#9c8a6a"},
          {"t": "cyl", "x": 0, "z": 0, "y": 0, "r": 11, "h": 4.5, "c": "#c8b08a", "n": 36, "edge": "rgba(0,0,0,.22)"},
          {"t": "cyl", "x": 0, "z": 0, "y": 4.5, "r": 1.4, "h": .06, "c": "#1f1812", "n": 20, "edge": "rgba(0,0,0,0)"},
          {"t": "person", "x": 14, "y": 0, "z": 10, "h": 1.7},
          L_(0, 4.5, "a tower at Bat · c. 22 m across · schematic", GOLD, z=-11, dy=-26), L_(0, 4.6, "a well at the centre", "#cfe6ff", z=0, dy=46)]
    s3 = iso(tw, cam=[1, 500, 900], s=17, x=500, y=1060, az=-26, spin=1.1, el=.45, table=None)
    tl, ax = timeline(-3100, -1600, [(-3000, "3000 BCE"), (-2500, "2500"), (-2000, "2000"), (-1600, "1600")], "Magan's copper age")
    tl["els"] += [{"k": "band", "x0": ax.x(-2800), "x1": ax.x(-2000), "y": 745, "h": 16, "c": OCHRE, "t": "the towers of Magan", "in": .3}] + \
                 event(ax, -2300, "Akkad's ships from Magan", row=2, c=AMBER, i=.6) + right(event(ax, -1750, "Nanni complains", row=1, c=RED, i=.9))
    s4 = tl
    s5 = dark(grp("why Oman?", "#8fd9b0", ["lead isotopes match its mountains", "metal from Ur's royal tombs", "texts: copper from Magan"]))
    s6 = like(s0, cam=[1.1, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:UR · c. 1750 BCE][sfx:boom][act:playful, intrigued]The world's oldest known customer ^complaint is about bad ^copper.",
                      "[d:tension][cam:1.12|0|0][act:the twist, leaning in][tune:fall]And that copper probably came from ^Oman."], cut=False),
        B("world", 2, ["[d:calm][k:THE LETTER][act:storytelling, amused]Around {1750|seventeen fifty} BCE, a man named ^Nanni wrote to a trader called ^Ea-nasir. [act:reporting, lightly indignant]The copper was ^poor, he said, and he wanted his money ^back.",
                       "[d:aside][act:dry, deadpan][tune:fall]Nanni was not ^happy."]),
        B("collision", 1, ["[d:build][k:THE ROUTE][act:building, clear]Ea-nasir sailed to ^Dilmun, today's Bahrain, to buy his copper. [act:the connection]Dilmun got it from a mountain land the texts call ^Magan.",
                           "[d:build][act:precise, confident]Lead@metal isotopes in Bronze Age copper point to the mountains of ^Oman."]),
        B("cost", 3, ["[d:build][k:MAGAN][act:vivid, impressed]Magan's people built round stone ^towers, about twenty metres across, some with a ^well at the centre. [act:plain]Kings of Akkad boasted of ships from Magan, and one went to war with ^it."]),
        B("reversal", 4, ["[d:reveal][k:THE CATCH][act:fair, a caveat]But the tablet never says where ^Ea-nasir's copper came from. [act:precise]And what the towers were ^for, monuments, forts or homes of the ^powerful, is still ^argued."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Bronze Age copper from ^Oman? [act:the verdict, measured][tune:fall]*Strong ^evidence*. [act:the last word, amused]As for Nanni's ^refund@noun.",
                     "[d:tension][p:0.93][act:dry, deadpan][tune:fall]Still ^pending."]),
    ]
    return EP("ea-nasir", "14.07", "The First Complaint Letter", "ea-nasir", "strong", "Where did the Bronze Age copper of Mesopotamia, and of Ea-nasir's bad deal, come from?", "The oldest *complaint* on Earth.", beats, shots,
              "Begemann et al. 2010 (doi:10.1111/j.1600-0471.2010.00327.x) · Klein & Hauptmann (eds.) 2016, Metalla 22.1 · Swerida et al. 2024 (doi:10.5334/oq.150) · UNESCO, Bat, Al-Khutm and Al-Ayn (434) · British Museum 131236",
              "Around 1750 BCE, Nanni wrote to the trader Ea-nasir about bad copper: the oldest known customer complaint. The copper trail runs through Bahrain to the mountains of Oman.",
              ["#History", "#Oman", "#Mesopotamia", "#Archaeology", "#ArabiaUnearthed"])



def _ingot(x, y, at=0, poor=False):
    """A bun-shaped copper ingot, seen from the side; a poor one is dull and cracked."""
    els = [{"k": "poly", "p": [[x - 46, y], [x - 40, y - 18], [x - 16, y - 28], [x + 16, y - 28], [x + 40, y - 18], [x + 46, y]], "fill": "#6f5a44" if poor else "#c8743c",
            "c": "#8a6a48" if poor else "#f4b27a", "w": 2, "curve": True, "in": at, "fx": "pop"}]
    if poor:
        els.append({"k": "line", "p": [[x - 10, y - 26], [x - 2, y - 14], [x - 12, y - 6], [x - 4, y]], "c": "#2a2019", "w": 3, "in": round(at + .2, 2), "fx": "draw", "dur": .3})
    return els


def eanasir_m():
    """Ea-nasir's copper as one continuous take (see mural.py): a tablet smaller than a phone, a refund demanded, the copper trail by sea, a fingerprint in the metal, and towers with no agreed purpose."""
    remix, I = _mur()
    ep = eanasir()
    CU, SILVER = "#c8743c", "#cbd2d8"
    v = View(44, 60, 20, 32.5, (40, 330, 920, 900))
    m = copy.deepcopy(ep["shots"][1])
    for e in m["els"]:
        if e.get("k") == "arrow":
            e["in"] = 1.0 if e.get("c") == AMBER else 5.4         # Ea-nasir sails to Dilmun first; Dilmun's copper comes from Magan next
    m["els"] = [e for e in m["els"] if e.get("k") != "cap"] + [{"k": "boat", "x": v.p(48.9, 28.4)[0] + 40, "y": v.p(48.9, 28.4)[1], "w": 90, "in": 1.4}]
    mx, my = v.p(56.6, 23.6)
    finger = [I.tri(mx - 40 + 26 * j, my - 30 - 10 * (j % 2), 22, 0, "#8a7458", round(.4 + .1 * j, 2)) for j in range(4)] + \
             [I.ring(mx + 20, my - 120, 18 + 12 * k, round(2.4 + .15 * k, 2), I.AMBER, 2, dur=.5) for k in range(4)] + \
             [I.line([[mx + 20, my - 60], [mx + 20, my - 40]], 3.0, I.AMBER, 2, "inferred", .3), I.glow(mx, my - 40, 110, 3.6, .6, "lamp")]
    # 2 · the letter: a tablet smaller than a phone; poor copper; money wanted back; one unhappy customer
    tab = [I.box(230, 380, 100, 232, "#b9a47c", "#8a6a48", 2, 14, .2), {"k": "glyphs", "x": 242, "y": 396, "w": 76, "h": 200, "rows": 10, "cols": 3, "kind": "cuneiform", "c": "#3b2a1c", "in": .3},
           I.box(400, 318, 142, 294, "none", "#9fd0ff", 3, 20, 3.6, style="claimed"), I.label(471, 660, "a phone", 4.0, "#9fd0ff", 28),
           I.line([[210, 380], [210, 612]], 2.8, "#e9dccb", 2, dur=.4), I.label(196, 504, "11.6 cm", 3.2, "#e9dccb", 28, "end")]
    deal = [I.person(190, 1330, 200, .8), I.label(190, 1385, "Nanni", 1.0, I.BONE, 30), I.person(810, 1330, 200, 1.4), I.label(810, 1385, "Ea-nasir", 1.6, I.BONE, 30),
            I.arrow([[700, 1040], [500, 1025], [300, 1040]], 5.0, CU, 3, dur=.8)] + _ingot(320, 975, 5.2) + _ingot(430, 975, 7.4, True) + _ingot(540, 970, 7.6, True) + \
           [I.label(500, 900, "poor copper", 7.8, CU, 30)] + \
           [I.arrow([[700, 1160], [500, 1140], [300, 1160]], 9.0, SILVER, 3, "claimed", .8)] + [I.dot(450 + 30 * j, 1130 - 4 * (j % 2), 10, SILVER, round(9.2 + .1 * j, 2)) for j in range(4)] + \
           [I.label(500, 1210, "money back?", 9.6, SILVER, 30)]
    grump = [I.line([[150, 1080], [166, 1060], [182, 1080], [198, 1060], [214, 1080], [230, 1060]], .3, I.RED, 4, dur=.4), I.glow(190, 1070, 70, .3, .6, "red")]
    letter = {"base": "dark", "cam": [1, 500, 880], "els": tab + deal}
    # 3 · Magan's towers: ships boasted of by Akkad's kings, and a war
    tower = copy.deepcopy(ep["shots"][3])
    for e in tower["els"]:
        if e.get("k") == "iso":
            e["spin"] = .3
    akkad = [{"k": "boat", "x": 380, "y": 540, "w": 260, "in": 7.5}, I.glow(380, 520, 170, 7.5, .5), I.label(380, 620, "ships from Magan", 7.9, "#e8c894", 30),
             I.glow(760, 520, 120, 9.8, .7, "red"), I.line([[700, 450], [820, 590]], 10.0, I.RED, 5, dur=.4), I.line([[820, 450], [700, 590]], 10.1, I.RED, 5, dur=.4)]
    # 5 · the catch: where exactly, unknown; and what the towers were for, still argued
    catch = {"base": "dark", "floor": 1300, "cam": [1, 500, 900], "els": [
        I.box(150, 420, 90, 150, "#b9a47c", "#8a6a48", 2, 10, .3), {"k": "glyphs", "x": 160, "y": 432, "w": 70, "h": 120, "rows": 6, "cols": 3, "kind": "cuneiform", "c": "#3b2a1c", "in": .4},
        I.arrow([[260, 500], [450, 440], [640, 500]], 1.0, I.LILAC, 3, "claimed", 1.0)] + I.question(450, 400, 1.4, 64) +
        [I.tri(700 + 34 * j, 540 - 14 * (j % 2), 30, 0, "#8a7458", round(4.5 + .1 * j, 2)) for j in range(4)] +
        [I.label(750, 610, "Oman: the best bet", 4.9, "#e8c894", 28)] +
        [{"k": "poly", "p": [[350, 1300], [360, 1120], [640, 1120], [650, 1300]], "fill": "#c8b08a", "c": "#efe6d2", "w": 2, "in": 6.4, "fx": "rise"},
         I.oval(500, 1120, 140, 16, "#d8c09a", "#efe6d2", 2, 1, 6.4)] +
        [I.line([[500, 1100], [x, y + 40]], 8.0 + .5 * k, I.LILAC, 2, "claimed", .5) for k, (x, y) in enumerate(((200, 900), (500, 820), (800, 900)))] +
        [I.glow(200, 880, 70, 8.2, .8), I.dot(200, 880, 14, "#e8c894", 8.2), I.label(200, 980, "monument?", 8.4, I.BONE, 28)] +
        [I.box(450, 760, 100, 60, "#8a7458", "#efe6d2", 2, 2, 8.7)] + [I.box(450 + 28 * j, 742, 16, 18, "#8a7458", "#efe6d2", 2, 1, 8.7) for j in range(4)] + [I.label(500, 790 + 90, "fort?", 8.9, I.BONE, 28)] +
        [{"k": "house", "x": 760, "y": 900, "w": 80, "h": 50, "in": 9.2}, {"k": "poly", "p": [[752, 850], [800, 820], [848, 850]], "fill": "#8e7152", "c": "none", "w": 0, "in": 9.2},
         I.label(800, 980, "home?", 9.4, I.BONE, 28)]}
    sand = [I.line([[790, 360], [870, 360], [830, 420], [870, 480], [790, 480], [830, 420], [790, 360]], .4, I.BONE, 3, dur=.6),
            {"k": "poly", "p": [[830, 428], [862, 474], [798, 474]], "fill": "#e8c894", "c": "none", "w": 0, "in": .6, "fx": "fill", "dur": 2.5},
            {"k": "poly", "p": [[798, 368], [862, 368], [830, 410]], "fill": "#e8c894", "c": "none", "w": 0, "in": .5}]
    bad = _ingot(830, 980, 3.8, True) + [I.glow(830, 960, 90, 3.8, .5)]
    return remix(ep, scenes={1: m, 2: letter, 3: tower, 5: catch}, alias={4: 5, 6: 0}, cams={0: [1.05, 500, 900], 4: [1, 500, 900], 6: [1.1, 500, 880]},
                 drop=("para", "num", "title", "q", "cap"), adds={0: bad, 3: akkad}, line_adds={(1, 1): (grump, None), (2, 1): (finger, None), (5, 1): (sand, None)})

# ---------------------------------------------------------------- 14.08 The meteorite that was not a lost city (Wabar)
def ring(r, y=.35, n=40, c="#e8d3a8", w=2.4):
    return {"t": "line", "p": [[r * math.cos(2 * math.pi * k / n), y, r * math.sin(2 * math.pi * k / n)] for k in range(n + 1)], "c": c, "w": w, "ground": True}


def wabar():
    w = [{"t": "slab", "x0": -90, "x1": 90, "z0": -60, "z1": 60, "y": 0, "c": "#c9a36c"},
         {"t": "flat", "pts": [[58 * math.cos(2 * math.pi * k / 30) - 20, 58 * math.sin(2 * math.pi * k / 30)] for k in range(30)], "y": .05, "c": "#8a6b45"},
         {"t": "flat", "pts": [[32 * math.cos(2 * math.pi * k / 24) + 52, 32 * math.sin(2 * math.pi * k / 24) + 18] for k in range(24)], "y": .05, "c": "#8a6b45"},
         {"t": "flat", "pts": [[5.5 * math.cos(2 * math.pi * k / 12) + 60, 5.5 * math.sin(2 * math.pi * k / 12) - 40] for k in range(12)], "y": .05, "c": "#6f5334"}]
    r = rnd(9)
    for k in range(60):
        a = r() * 2 * math.pi; d = 60 + r() * 22
        w.append({"t": "cyl", "x": -20 + d * math.cos(a), "z": d * math.sin(a), "y": 0, "r": .9, "h": .3, "c": "#1b1714", "n": 6, "edge": "rgba(0,0,0,0)"})
    for R_, cx, cz in ((58, -20, 0), (32, 52, 18), (5.5, 60, -40)):     # crater rims
        rim = ring(R_, c="#f0dcb0"); rim["p"] = [[x + cx, y, z + cz] for x, y, z in rim["p"]]; w.append(rim)
    for k in range(3):
        w.append({"t": "prism", "pts": [[-88, -58 + k * 16], [-40, -60 + k * 14], [-30, -52 + k * 14], [-86, -50 + k * 16]], "y": 0, "h": 2.5 + k, "c": "#d8b47c", "edge": "rgba(0,0,0,.15)"})
    w += [L_(-20, 1, "craters 116 m and 64 m across · schematic", GOLD, z=-58, dy=-24), L_(-20, 1, "black glass beads", "#cfe6ff", z=64, dy=40)]
    s0 = iso(w, cam=[1, 500, 920], s=3.3, x=500, y=1010, az=-20, spin=1.1, el=.55, table=None)
    s1, v = arabia([("Wabar", 50.474, 21.503, {"c": GOLD}), ("Riyadh · the iron today", 46.711, 24.648, {"c": SCAN})],
                   lon0=42, lon1=58, lat0=15, lat1=28)
    s1["els"] += [{"k": "label", "x": v.p(51.5, 19.6)[0], "y": v.p(51.5, 19.6)[1], "t": "the Empty Quarter", "st": "ital", "c": "#e8c894", "in": 1.0},
                  {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}]
    s2 = stat("c. 300", "years", "luminescence age of the impact glass: 290 ± 38 years, measured in 2004", "Prescott et al. 2004")
    iron = sphere(0, 0, 1.0, c="#4a4642") + sphere(.9, .3, .75, c="#565049") + sphere(-.8, -.2, .7, c="#4a4642")
    iron += [{"t": "slab", "x0": -4, "x1": 4, "z0": -3, "z1": 3, "y": 0, "c": "#5a4a3a"}, {"t": "person", "x": 2.8, "y": 0, "z": 1.6, "h": 1.7},
             L_(0, 2.2, "the Camel's Hump · c. 2.2 tonnes of iron", GOLD, z=0, dy=-26), L_(0, 0, "National Museum, Riyadh", "#cfe6ff", z=2, dy=50)]
    s3 = iso(iron, cam=[1, 500, 900], s=90, x=500, y=1060, az=-30, spin=1.0, el=.3, table=None)
    tl, ax = timeline(1600, 2030, [(1600, "1600"), (1700, "1700"), (1800, "1800"), (1900, "1900"), (2000, "2000")], "Young craters")
    tl["els"] += [{"k": "band", "x0": ax.x(1676), "x1": ax.x(1752), "y": 745, "h": 16, "c": GOLD, "t": "the impact, by luminescence", "in": .3}] + \
                 event(ax, 1932, "Philby arrives", row=1, c=AMBER, i=.6) + right(event(ax, 2008, "a crater buried by dunes", row=2, c=SCAN, i=.9))
    s4 = tl
    s5 = dark(grp("found", "#8fd9b0", ["meteoritic iron", "black glass beads", "shocked sand"], y=440, size=28) +
              grp("not found", "#ff8a7a", ["walls", "tools", "people"], y=820, size=28))
    s6 = like(s0, cam=[1.14, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE EMPTY QUARTER][sfx:boom][act:storytelling, intrigued]In {1932|nineteen thirty-two}, an explorer crossed Arabia's Empty Quarter looking for a lost ^city.",
                      "[d:tension][cam:1.12|0|0][act:the twist, a small smile][tune:fall]He found a ^meteorite instead."], cut=False),
        B("world", 1, ["[d:calm][k:WABAR][act:plain, orienting]The explorer was the Briton, ^Philby. [act:steady]His guides spoke of ^Wabar, a place of ruins and ^iron, deep in the ^sands.",
                       "[d:build][act:the arrival, wonder]What he found were ^craters, ringed with black ^glass."]),
        B("collision", 3, ["[d:build][k:THE IRON][act:building, clear]He took them for a ^volcano. [act:the correction, precise]They were made by a falling iron ^meteorite: the biggest crater is a hundred and sixteen metres ^across.",
                           "[d:aside][act:vivid, a little amazed]The largest piece of iron, the Camel's Hump, weighs about two ^tonnes."]),
        B("cost", 2, ["[d:build][k:THE DATE][act:the reveal, precise]Then came the ^date. [act:plain, confident]Luminescence puts the impact only about three hundred years ^ago. [act:the point, clear][tune:fall]Far too young for any ancient ^city."]),
        B("reversal", 5, ["[d:reveal][k:THE SANDS][act:fair, even]The ground holds iron, glass and shocked ^sand. [act:plain][tune:fall]But no walls, no tools, no ^people.",
                          "[d:build][go:4|0][act:wry, light]And by {2008|two thousand eight}, one crater had vanished under the ^dunes."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A lost city destroyed from the ^sky? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:warm, the other half][tune:rise]A real impact, a few centuries ^ago? [act:sure][tune:fall]That part is ^real.",
                     "[d:tension][p:0.93][act:the last word, a small smile][tune:fall]Philby lost a city, and found a ^star."]),
    ]
    return EP("wabar", "14.08", "Wabar: The Meteorite That Was Not a City", "wabar", "debunked", "Are the Wabar craters in the Empty Quarter the ruins of a city destroyed from the sky?", "He found a *meteorite* instead.", beats, shots,
              "Prescott et al. 2004 (doi:10.1029/2003JE002136) · Gnos et al. 2013 (doi:10.1111/maps.12218) · Wynn & Shoemaker 1998, Scientific American · Philby 1933, The Empty Quarter",
              "In 1932 an explorer crossed the Empty Quarter looking for a lost city and found meteorite craters instead. How old they are, and why no city ever stood there.",
              ["#Meteorite", "#Arabia", "#EmptyQuarter", "#Science", "#ArabiaUnearthed"])


def wabar_m():
    """Wabar as one continuous take: a streak from the sky onto the craters; sand grains as little batteries that the impact emptied
    and that have been charging for about 300 years; what the ground holds (iron, glass, shocked sand) and what it never held."""
    from mural import remix
    from illus import person, line, glow, label, dot, box, oval, strike, AMBER, BLUE, BONE, RED, GREEN, LILAC
    ep = wabar()

    def _relabel(o):     # a shorter crater label: the long one ran off the frame on the last panel
        if isinstance(o, dict):
            return {k: _relabel(v) for k, v in o.items()}
        if isinstance(o, list):
            return [_relabel(v) for v in o]
        return "craters 116 m and 64 m" if o == "craters 116 m and 64 m across · schematic" else o
    ep = _relabel(ep)
    hook = [line([[900, 260], [560, 900]], .9, "#ffe2b4", 5, dur=.5), glow(560, 900, 190, 1.35, .85, "fire")]
    # the date: a grain of sand as a battery that the impact's heat emptied, charging ever since
    seg = lambda k, at, c: box(578, 1000 - 40 * (k + 1), 74, 34, c, r=5, at=at, fx="pop")
    clock = {"base": "dark", "floor": 1300, "cam": [1, 500, 880], "els": [
        oval(300, 760, 150, 118, "#d8b47c", "#f5ecdc", 2, at=.3), label(300, 940, "a grain of sand", .6, BONE, 30),
        box(560, 560, 110, 450, "rgba(18,13,10,.55)", "#f5ecdc", 2.5, r=10, at=.9), box(590, 532, 50, 28, "#f5ecdc", r=4, at=.9)] +
        [seg(k, 1.5 + .22 * k, "#8fd9b0") for k in range(6)] +
        [glow(300, 760, 230, 3.4, .9, "fire"), box(566, 566, 98, 438, "#171310", r=8, at=3.6, fx="pop"), label(300, 380, "the impact's heat: empty", 3.6, AMBER, 30)] +
        [seg(k, 4.4 + .3 * k, "#e8c35a") for k in range(8)] +
        [label(700, 700, "charging since", 4.6, BONE, 28, "start"), label(700, 745, "the impact", 4.6, BONE, 28, "start"),
         label(700, 840, "≈ 300 years", 7.0, "#e8c35a", 40, "start"),
         box(160, 1130, 90, 30, "#e8c35a", r=6, at=8.0, fx="fill"), label(270, 1155, "Wabar: 300 years", 8.1, "#e8c35a", 28, "start"),
         box(160, 1200, 680, 30, "rgba(201,193,238,.25)", LILAC, 1.5, r=6, at=8.6, fx="fill"), label(160, 1270, "an ancient city: thousands of years", 8.8, LILAC, 28, "start"),
         strike(150, 1215, 850, 1215, 9.6)]}
    # what the ground holds, and what it never held
    beads = [dot(470 + 64 * math.cos(2 * math.pi * k / 11), 560 + 40 * math.sin(2 * math.pi * k / 11), 9, "#1b1714", 1.5 + .03 * k) for k in range(11)]
    shock = [line([[740 + dx, 530], [790 + dx, 600]], 2.2 + .05 * i, "#f5ecdc", 2, dur=.3) for i, dx in enumerate((-10, 15, 40))]
    wall = [box(130 + 46 * (k % 4) + (23 if (k // 4) % 2 else 0), 860 - 30 * (k // 4), 42, 26, "#a8977c", r=3, at=3.3 + .03 * k, op=.6) for k in range(12)]
    tool = [line([[470, 900], [530, 790]], 3.8, "#b9ab94", 7, draw=False), {"k": "poly", "p": [[515, 770], [565, 790], [545, 830], [522, 805]], "fill": "#9aa0a8", "c": "none", "w": 0, "in": 3.8}]
    ground = {"base": "dark", "floor": 1200, "cam": [1, 500, 820], "els": [
        oval(220, 560, 74, 54, "#565049", "#2a2622", 2, at=.9), label(220, 660, "iron", 1.0, GREEN, 30)] + beads +
        [label(470, 660, "black glass", 1.6, GREEN, 30), oval(780, 560, 60, 50, "#d8b47c", "#f5ecdc", 1.5, at=2.1)] + shock +
        [label(780, 660, "shocked sand", 2.3, GREEN, 30)] + wall + [label(230, 960, "walls", 3.4, RED, 30), strike(120, 800, 340, 900, 3.6)] +
        tool + [label(510, 960, "tools", 3.9, RED, 30), strike(430, 780, 600, 910, 4.1)] +
        [person(780, 900, 120, 4.3), label(780, 960, "people", 4.4, RED, 30), strike(710, 770, 850, 910, 4.6)]}
    verdict = [label(500, 430, "a lost city?", .5, LILAC, 40), strike(370, 420, 630, 420, 2.0), glow(500, 330, 90, 3.4, .8), label(500, 345, "\u2605", 3.4, "#e8c35a", 54)]
    return remix(ep, scenes={2: clock, 5: ground}, adds={0: hook, 6: verdict})


# ---------------------------------------------------------------- 14.09 The ledger
def ledger():
    """The ledger as one continuous film: the cabinet of the eight cases (see cabinet.py)."""
    from cabinet import Cabinet, VCOL
    first = lambda fn: next(sh for sh in fn()["shots"] if any(e.get("k") == "iso" for e in sh["els"]))
    hero = lambda fn: next(e for e in first(fn)["els"] if e.get("k") == "iso")
    C = Cabinet([
        {"name": "Tayma", "model": hero(nabonidus)},
        {"name": "The mustatils", "model": hero(mustatils)},
        {"name": "The desert kites", "model": hero(kites)},
        {"name": "Copper of Magan", "model": first(eanasir)},
        {"name": "Nefud footprints", "model": hero(footprints)},
        {"name": "Camels on the cliffs", "model": camels()["shots"][0]},
        {"name": "The Dilmun mounds", "model": hero(dilmun)},
        {"name": "Wabar", "model": hero(wabar)},
    ])
    C.build()
    TA, MU, KI, CU, FO, CA, DI, WA = range(8)
    s1 = C.step(C.cam_cell(TA), C.verdict(TA, "established", "a king of Babylon lived here", .4))
    s2 = C.step(C.cam_cells([MU, KI]), C.verdict(MU, "established", "built by herders", .3) + C.people(MU, 3, at=.8) +
                C.verdict(KI, "established", "hunters' traps", .9) + C.people(KI, 3, at=1.4))
    s3 = C.step(C.cam_cell(CU), C.verdict(CU, "established", "copper for Mesopotamia", .4))
    s4 = C.step(C.cam_cell(FO), C.verdict(FO, "plausible", "c. 120,000 years", .4) + C.people(FO, 2, at=1.0))
    s5 = C.step(C.cam_cell(CA), C.verdict(CA, "plausible", "c. 12,000 years?", .4))
    top = C.cam_cells([TA, MU])
    s6 = C.step(top, C.verdict(TA, "open", frame=False, at=.1) + C.question(TA, dx=C.w * .26, dy=-160, at=.2, id="qTA") + C.note(TA, "why did Nabonidus come?", at=.5, c=VCOL["open"]))
    s7 = C.step(top, C.verdict(MU, "open", frame=False, at=.1) + C.question(MU, dx=C.w * .26, dy=-160, at=.2) + C.note(MU, "what did they mean?", at=.5, c=VCOL["open"]), keep_notes=True)
    s8 = C.step(C.cam_cell(DI), C.verdict(DI, "ruled", at=.2) + C.struck(DI, "an island of the dead", dy=-170, at=.5))
    s9 = C.step(C.cam_cell(WA), C.verdict(WA, "ruled", at=.2) + C.struck(WA, "a city destroyed here", dy=-170, at=.5))
    s10 = C.step(C.cam_cell(TA), C.verdict(TA, "ruled", frame=False, at=.2) + C.struck(TA, "cut by a laser", at=.5), drop=["qTA"])
    s11 = C.step(C.cam_all(), [e for i in range(8) for e in C.wash(i, VCOL["established"], at=.4 + .12 * i, op=.13)])
    s12 = C.step(C.cam_all(), [e for i in (TA, CU, CA, DI, WA) for e in C.people(i, 2, at=.2 + .1 * i)])
    s13 = C.step(C.cam_all(z=.64, sy=700))
    shots = C.shots
    beats = [
        B("hook", 0, ["[d:intrigue][sfx:boom][act:warm, opening the book]Eight cases from the Arabian ^peninsula. [act:inviting, a small smile]Here's the ^ledger."], cut=False),
        B("world", s1, ["[d:calm][act:confident, ticking them off][tune:level]A king of Babylon lived at ^Tayma. [go:%d|1.3][act:plain, sure][tune:level]Herders and hunters built giant rectangles and ^traps. [go:%d|1.2][act:the last one, warm][tune:fall]And Oman's copper fed ^Mesopotamia." % (s2, s3)], cut=False),
        B("collision", s4, ["[d:build][act:weighing each, even][tune:level]Footprints of our species, a hundred and twenty thousand years ^old. [go:%d|1.1][act:measured][tune:fall]And giant camels on the cliffs, perhaps twelve thousand years ^old." % s5], cut=False),
        B("cost", s6, ["[d:build][act:curious, even]Why Nabonidus ^came. [go:%d|.5][act:practical][tune:fall]And what the rectangles ^meant." % s7], cut=False),
        B("reversal", s8, ["[d:reveal][sfx:hit][act:clear, a small smile][tune:level]An island of the ^dead. [go:%d|1.1][tune:level]A city destroyed at ^Wabar. [go:%d|1.6][act:dry][tune:fall]And a laser-cut ^rock." % (s9, s10)], cut=False),
        B("tag", s11, ["[d:verdict][p:0.95][act:warm, wise, even]Arabia was never an empty ^quarter. [act:the lesson, simple][tune:fall]It turned green again and again, [go:%d|.8]and people were always ^there." % s12,
                       "[d:tension][p:0.93][go:%d|4][act:the motto, calm and warm]^Coherence is the measure. [act:quiet, the last word][tune:fall]Not ^final demonstration." % s13], cut=False),
    ]
    return EP("arabia-ledger", "14.09", "Arabia Unearthed · The Ledger", "", "mixed", "What held up, and what didn't, across ancient Arabia.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 14",
              "The verdicts of Arabia Unearthed in one ledger: what is established about ancient Arabia, what is plausible, what is still open, and what is ruled out.",
              ["#Arabia", "#History", "#Archaeology", "#ArabiaUnearthed", "#WeighItYourself"])


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/arabia-ledger.json)."""
    import recap
    return recap.recap(ledger, "arabia-ledger", None)


def EPISODES():
    return [mustatils_m(), footprints_m(), camels_m(), kites_m(), nabonidus_m(), dilmun_m(), eanasir_m(), wabar_m(), ledger_recap()]
