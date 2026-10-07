"""File 05 · Under Giza, part b: six films as one continuous take each (see mural.py). Narration in rewrite/<id>.json."""
from f05 import *
import f05 as F
import math, copy


def _mur():
    from mural import remix
    import illus
    return remix, illus


GOLD_ = "#f2c98e"


def _belt(cx, cy, k, at, I, op=None, c="#fff6e6", glow=True):
    """Orion's three belt stars as seen facing south (Alnitak, Alnilam, Mintaka), k pixels per degree, centred on Alnilam."""
    out = []
    for n in ("Alnitak", "Alnilam", "Mintaka"):
        x, y = F.sky_xy(*F.ORI[n], cx=cx, cy=cy, s=k)
        if glow:
            out.append(I.glow(x, y, 34, at, .8 if op is None else op * .8))
        out.append(I.dot(x, y, 6, c, at, op=op))
    return out


def orion_m():
    """The Orion correlation as one continuous take: the slow wobble of the sky, the turn it needs, ten degrees, three reigns."""
    remix, I = _mur()
    ep = F.orion()
    sh = ep["shots"]
    # 2 · the slow wobble: today the belt stands high; around 10,500 BCE it sank to its lowest
    wob = {"base": "sky", "tod": "night", "ground": 1180, "sun": False, "cam": [1, 500, 860], "els": [
        {"k": "pyramid", "x": 330, "y": 1180, "w": 290, "courses": False}, {"k": "pyramid", "x": 130, "y": 1190, "w": 200, "courses": False, "cap": .1},
        I.oval(200, 470, 62, 62, "#2f5f7a", "#9fd0ff", 2, 1, .3), I.line([[166, 553], [234, 387]], .6, "#f5ecdc", 3),
        {"k": "line", "p": I.ellipse(200, 393, 34, 10, 40), "c": GOLD_, "w": 3, "style": "inferred", "curve": True, "in": 1.0, "fx": "draw", "dur": 2.4},
        I.label(200, 610, "26,000-year wobble", 1.6, I.BLUE, 28)] +
        _belt(640, 420, 60, 2.6, I) + [I.label(740, 400, "today", 2.8, I.BONE, 30, "start")] +
        [I.arrow([[520, 440], [520, 990]], 3.2, I.AMBER, 3, "inferred", 2.0, False)] +
        _belt(640, 570, 60, 3.6, I, .35) + _belt(640, 720, 60, 4.1, I, .35) + _belt(640, 870, 60, 4.6, I, .35) +
        _belt(640, 1010, 60, 5.8, I) + [I.glow(640, 1010, 130, 6.0, .45), I.label(740, 990, "10,500 BCE", 6.2, I.AMBER, 32, "start")]}
    # 4 · the check: the belt sits on the pyramids only when the picture of the sky is turned nearly upside down
    figl = [("Betelgeuse", "Alnitak"), ("Bellatrix", "Mintaka"), ("Alnitak", "Saiph"), ("Mintaka", "Rigel"), ("Alnitak", "Alnilam"), ("Alnilam", "Mintaka"),
            ("Betelgeuse", "Meissa"), ("Meissa", "Bellatrix")]
    Q = {n: F.sky_xy(*F.ORI[n], cx=400, cy=560, s=19) for n in F.ORI}
    M = lambda x, y: [round(470 + (x + 290) * .36, 1), round(1150 - (y + 369) * .36, 1)]
    from scenes import GP
    pyr = {n: M(*GP[n][0]) for n in ("khufu", "khafre", "menkaure")}
    half = {"khufu": 41, "khafre": 39, "menkaure": 19}
    za, zm, zl = complex(*Q["Alnitak"]), complex(*Q["Mintaka"]), complex(*Q["Alnilam"])
    k = (complex(*pyr["menkaure"]) - complex(*pyr["khufu"])) / (zm - za); t = complex(*pyr["khufu"]) - k * za
    turned = {n: [round((k * complex(*Q[n]) + t).real, 1), round((k * complex(*Q[n]) + t).imag, 1)] for n in ("Alnitak", "Alnilam", "Mintaka")}
    ak = abs(k); c0 = complex(*pyr["khafre"])
    unturned = {n: [round((c0 + ak * (complex(*Q[n]) - zl)).real, 1), round((c0 + ak * (complex(*Q[n]) - zl)).imag, 1)] for n in ("Alnitak", "Alnilam", "Mintaka")}
    turn = {"base": "dark", "stars": 60, "cam": [1, 500, 860], "els":
            [I.line([Q[a], Q[b]], .3, "#a99cf0", 1.6, dur=.8, op=.7) for a, b in figl] +
            [I.dot(q[0], q[1], 6 if n in ("Betelgeuse", "Rigel") else 4.5, "#fff6e8", .2) for n, q in Q.items()] +
            [I.glow(Q[n][0], Q[n][1], 30, 1.2, .8) for n in ("Alnitak", "Alnilam", "Mintaka")] +
            [I.label(400, 800, "the sky, facing south", 1.0, "#c9c1ee", 28)] +
            [{"k": "poly", "p": [[x - h, y - h], [x + h, y - h], [x + h, y + h], [x - h, y + h]], "fill": "#c9ad85", "c": "#f2dcb4", "w": 1.5, "in": 2.4, "fx": "pop"}
             for n, (x, y) in pyr.items() for h in [half[n]]] +
            [I.label(470, 1395, "Giza, from above", 2.6, I.BONE, 28)] +
            [I.dot(x, y, 7, I.LILAC, 3.2, op=.8) for x, y in unturned.values()] + [I.ring(unturned["Mintaka"][0], unturned["Mintaka"][1], 26, 3.5, I.LILAC, 3, "claimed", .5)] +
            [I.arrow([[round(770 + 90 * math.cos(math.radians(a)), 1), round(1100 + 90 * math.sin(math.radians(a)), 1)] for a in range(-80, 190, 15)], 4.2, I.AMBER, 4, "known", 1.0),
             I.label(770, 1245, "nearly upside down", 4.6, I.AMBER, 28)] +
            sum([[I.glow(x, y, 40, 5.2, .9), I.dot(x, y, 8, "#fff6e6", 5.2)] for x, y in turned.values()], []) +
            [I.ring(turned["Mintaka"][0], turned["Mintaka"][1], 30, 5.6, I.AMBER, 3, "known", .5)]}
    # 5 · ten degrees: the line of the pyramids against the belt's angle in 10,500 BCE
    from scenes import giza_plan
    pl, P = giza_plan(scale=.8, cx=500, cy=800)
    a = P(0, 0); b = P(-581, -738); ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    pt = lambda r, d: [round(a[0] + r * math.cos(math.radians(d)), 1), round(a[1] + r * math.sin(math.radians(d)), 1)]
    ten = copy.deepcopy(sh[2])
    ten["cam"] = [1.3, 360, 720]
    ten["els"] = [e for e in ten["els"] if e.get("k") not in ("cap", "title")] + [
        I.line([a, b], .4, "#f2dcb4", 3, "inferred", 1.2),
        I.line([a, pt(700, ang + 10)], 1.6, I.AMBER, 4, "known", 1.2),
        {"k": "line", "p": [pt(520, ang + d) for d in range(0, 11)], "c": I.AMBER, "w": 3, "curve": True, "in": 2.8, "fx": "draw", "dur": .6},
        I.label(190, 800, "about 10°", 3.2, I.AMBER, 34, "end")]
    # 6 · three kings, one after another: the pyramids rise in turn on a line of time
    X = lambda yr: round(150 + 700 * (yr + 2620) / 140, 1)
    kings = [("Khufu", -2589, -2566, 161), ("Khafre", -2558, -2532, 151), ("Menkaure", -2530, -2503, 73)]
    reign = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[110, 1100], [890, 1100]], .2, "#8c7152", 3)] +
             sum([[{"k": "pyramid", "x": X((s + e) / 2), "y": 1098, "w": w, "courses": False, "in": 1.4 + .6 * j, "fx": "rise"},
                   I.box(X(s), 1114, X(e) - X(s), 14, I.AMBER, r=7, at=1.4 + .6 * j), I.label(X((s + e) / 2), 1180, n, 1.5 + .6 * j, I.AMBER, 28)]
                  for j, (n, s, e, w) in enumerate(kings)], []) +
             [I.label(X(-2600), 1240, "2600 BCE", .4, "#9a938a", 28), I.label(X(-2500), 1240, "2500 BCE", .4, "#9a938a", 28),
              I.arrow([[X(-2589), 1300], [X(-2516), 1300]], 3.4, I.BONE, 3, "known", .8, False), I.arrow([[X(-2516), 1300], [X(-2589), 1300]], 3.4, I.BONE, 3, "known", .8, False),
              I.label((X(-2589) + X(-2516)) / 2, 1355, "about 70 years", 3.8, I.BONE, 30)]}
    return remix(ep, scenes={3: wob, 4: turn, 5: ten, 6: reign}, cams={7: [1, 500, 880]})


def metrology_m():
    """Sacred measures as one continuous take: the pyramid scaled to the Earth, a slope that hides two pi, a circle that does too, a target painted late."""
    remix, I = _mur()
    ep = F.metrology()
    # 1 · the claim: the height scaled up meets the polar radius; the base, walked round, meets the equator
    tri = {"k": "poly", "p": [[110, 1300], [290, 1300], [200, 1185]], "fill": "url(#k-blocks)", "c": "#f2dcb4", "w": 2, "in": .1}
    scale = {"base": "dark", "stars": 50, "cam": [1, 500, 880], "els": [tri,
             I.line([[200, 1300], [200, 1185]], .6, I.BLUE, 3, "inferred", .6), I.line([[110, 1312], [290, 1312]], .6, GOLD_, 3, "known", .6),
             I.oval(560, 760, 280, 280, "rgba(111,182,214,.12)", "#9fd0ff", 2, 1, .2),
             I.label(330, 1100, "× 43,200", 1.2, GOLD_, 40, st="serif"),
             I.arrow([[200, 1170], [260, 900], [540, 700]], 1.8, I.BLUE, 3, "inferred", 1.0),
             I.line([[560, 760], [560, 480]], 3.0, I.BLUE, 5, "known", 1.0), I.dot(560, 480, 8, I.BLUE, 3.6),
             I.label(580, 600, "polar radius", 3.6, I.BLUE, 30, "start"), I.label(580, 640, "0.4% off", 4.4, "#cfe6ff", 28, "start"),
             I.arrow([[290, 1300], [420, 1100], [500, 840]], 6.4, GOLD_, 3, "inferred", 1.0),
             {"k": "line", "p": I.ellipse(560, 760, 280, 70, 60), "c": GOLD_, "w": 4, "curve": True, "in": 7.2, "fx": "draw", "dur": 1.6},
             I.label(560, 890, "equator", 7.6, GOLD_, 30), I.label(560, 930, "0.7% off", 8.4, "#f5dcb4", 28)]}
    # 3 · walk once around the base: the height fits into it six and a bit times, at any size
    def unroll(unit, y, at, c, n_lab=True):
        out = [I.line([[100, y], [100 + 6.2857 * unit, y]], at, GOLD_, 6, "known", 1.6)]
        for j in range(6):
            out.append(I.box(round(100 + j * unit + 2, 1), y + 30, round(unit - 4, 1), 22, c, r=4, at=round(at + 1.0 + .25 * j, 2), fx="pop"))
            if n_lab:
                out.append(I.label(round(100 + (j + .5) * unit, 1), y + 95, str(j + 1), round(at + 1.0 + .25 * j, 2), c, 28))
        out.append(I.box(round(100 + 6 * unit + 2, 1), y + 30, round(.2857 * unit - 2, 1), 22, c, r=3, at=round(at + 2.6, 2), op=.55, fx="pop"))
        return out
    U = 127.3
    peri = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "poly", "p": [[400, 700], [600, 700], [500, 572.7]], "fill": "url(#k-blocks)", "c": "#f2dcb4", "w": 2, "in": .2},
            I.line([[500, 700], [500, 572.7]], 1.0, I.BLUE, 4, "known", .5), I.line([[400, 712], [600, 712]], .6, GOLD_, 4, "known", .5),
            I.label(520, 640, "height", 1.0, I.BLUE, 28, "start"), I.label(500, 765, "perimeter", 1.2, GOLD_, 28)] +
           unroll(U, 900, 1.4, I.BLUE) + [I.label(500, 1120, "6.28 ≈ 2π", 4.4, GOLD_, 56, st="serif"),
           {"k": "poly", "p": [[150, 700], [250, 700], [200, 636.4]], "fill": "none", "c": GOLD_, "w": 2, "style": "inferred", "in": 7.6},
           {"k": "poly", "p": [[680, 700], [880, 700], [780, 572.7]], "fill": "none", "c": GOLD_, "w": 2, "style": "inferred", "in": 8.0}]}
    # 4 · and a circle: walk once around, and the radius fits six and a bit times
    R0 = 140
    circ = {"base": "dark", "cam": [1, 500, 880], "els": [I.ring(500, 720, R0, .6, I.BLUE, 3, "known", 1.0),
            I.line([[500, 720], [640, 720]], 1.6, GOLD_, 5, "known", .5), I.dot(500, 720, 6, GOLD_, 1.6), I.label(570, 700, "radius", 1.8, GOLD_, 28)] +
           [I.line([[60, 960], [60 + 6.2832 * R0, 960]], 2.2, I.BLUE, 6, "known", 1.6)] +
           [I.box(round(60 + j * R0 + 2, 1), 990, R0 - 4, 22, GOLD_, r=4, at=round(3.0 + .25 * j, 2), fx="pop") for j in range(6)] +
           [I.label(round(60 + (j + .5) * R0, 1), 1055, str(j + 1), round(3.0 + .25 * j, 2), GOLD_, 28) for j in range(6)] +
           [I.box(round(60 + 6 * R0 + 2, 1), 990, round(.2832 * R0 - 2, 1), 22, GOLD_, r=3, at=4.6, op=.55, fx="pop"),
            I.label(500, 1180, "6.28 ≈ 2π", 5.4, I.BLUE, 56, st="serif")]}
    # 5 · the number: an arrow lands, then the target is painted around it; best fits for height and base differ
    NX = lambda n: round(120 + 760 * (n - 43000) / 600, 1)
    num = {"base": "dark", "cam": [1, 500, 880], "els": [I.label(500, 420, "43,200", 2.0, GOLD_, 84, st="big", fx="pop"),
           I.box(520, 520, 360, 380, "#3b2f26", "#8a7a66", 2, 6, 5.2),
           I.line([[100, 840], [300, 650], [640, 700]], 6.4, "#cbbca8", 2, "inferred", .8, curve=True),
           I.line([[600, 735], [660, 690]], 7.2, "#e9dccb", 5, draw=False), I.dot(660, 690, 6, GOLD_, 7.2),
           I.line([[596, 728], [584, 748]], 7.2, "#c8743c", 4, draw=False), I.line([[606, 742], [592, 758]], 7.2, "#c8743c", 4, draw=False)] +
          [I.ring(660, 690, r, 8.4 + .3 * j, c, 5, "known", .4) for j, (r, c) in enumerate(((30, I.RED), (62, "#f5ecdc"), (94, I.RED), (126, "#f5ecdc")))] +
          [I.line([[120, 1180], [880, 1180]], 9.6, "#8c7152", 3, "known", .6),
           I.dot(NX(43200), 1180, 12, GOLD_, 9.8), I.label(NX(43200), 1240, "43,200", 9.8, GOLD_, 30),
           I.dot(NX(43363), 1180, 12, I.BLUE, 10.6), I.label(NX(43363), 1135, "best for height", 10.6, I.BLUE, 28),
           I.dot(NX(43504), 1180, 12, I.BLUE, 11.4), I.label(NX(43504), 1240, "best for base", 11.4, I.BLUE, 28)]}
    return remix(ep, scenes={1: scale, 3: peri, 4: circ, 5: num}, cams={0: [1.1, 500, 820]})


def drill_cores_m():
    """Granite drill cores as one continuous take: a groove read as a machine's track, a tube and sand that cut a ring, a bow drill older than Khufu."""
    remix, I = _mur()
    ep = F.drill_cores()
    # 3 · Dunn's reading: one turn of the groove, a tenth of an inch, at five hundred times a modern feed
    CX, CB, CW, CH = 300, 1180, 170, 440
    pitch = CH / 110 * 2.54
    helix = [I.line([[CX - CW / 2 + 4, round(CB - CH + 6 + j * pitch, 1)], [CX, round(CB - CH + 6 + j * pitch + pitch * .5 + 2, 1)], [CX + CW / 2 - 4, round(CB - CH + 6 + j * pitch + pitch, 1)]],
                     round(.6 + .02 * j, 2), "rgba(40,20,20,.75)", 1.4, dur=.3, curve=True) for j in range(int((CH - 14) / pitch))]
    mag = [I.oval(690, 740, 200, 200, "#8a766c", "#f2dcb4", 2.5, 1, 2.2)] + \
          [I.line([[500, 640 + 90 * j], [880, 700 + 90 * j]], round(2.6 + .2 * j, 2), "#2a1d17", 7, dur=.5) for j in range(3)] + \
          [I.line([[760, 681], [760, 771]], 3.6, GOLD_, 3, "known", .4), I.line([[745, 681], [775, 681]], 3.6, GOLD_, 3, draw=False), I.line([[745, 771], [775, 771]], 3.6, GOLD_, 3, draw=False),
           I.label(690, 990, "0.1 inch per turn", 4.0, GOLD_, 30)]
    spiral = {"base": "dark", "floor": CB, "cam": [1, 500, 880], "els": [{"k": "glow", "x": CX, "y": 960, "r": 300, "kind": "lamp", "op": .3},
              {"k": "core", "x": CX, "y": CB, "w": CW, "h": CH, "grooves": 0, "in": .1}] + helix +
             [I.ring(CX, 900, 40, 1.8, GOLD_, 3, "known", .5), I.line([[340, 880], [500, 790]], 2.0, GOLD_, 2, "inferred", .4)] + mag +
             [I.label(690, 1090, "× 500", 6.4, GOLD_, 56, st="serif"), I.label(690, 1140, "a modern drill's feed", 6.6, "#e9dccb", 28),
              I.box(240, 470, 120, 150, "none", I.LILAC, 3, 8, 8.8, style="claimed"), I.line([[300, 620], [300, 730]], 9.2, I.LILAC, 3, "claimed", .5),
              I.label(300, 440, "power tools?", 9.4, I.LILAC, 30)]}
    # 5 · copper carries the sand round; the sand grinds a ring; a core is left standing
    COP = "#c8743c"
    tube = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(200, 620, 600, 620, "#6d5a52", "#c9b0a8", 1.4, 4, .1),
            I.box(430, 470, 14, 150, COP, r=2, at=.3), I.box(556, 470, 14, 150, COP, r=2, at=.3),
            {"k": "line", "p": I.ellipse(500, 470, 80, 18, 30, 200, 520), "c": I.AMBER, "w": 3, "curve": True, "in": .5, "fx": "draw", "dur": .8},
            I.label(410, 500, "copper", .6, COP, 30, "end")] +
           [I.dot(x, 612 - 9 * (j % 2), 5, "#f5ecdc", round(1.0 + .05 * j, 2)) for j, x in enumerate((404, 414, 420, 455, 462, 470, 530, 538, 546, 584, 592, 600))] +
           [I.label(620, 590, "sand", 1.4, "#f5ecdc", 30, "start")] +
           [I.line([[437, 622], [437, 1040]], 2.0, "#241b16", 14, "known", 3.6), I.line([[563, 622], [563, 1040]], 2.0, "#241b16", 14, "known", 3.6),
            I.line([[437, 622], [437, 1020]], 2.1, COP, 8, "known", 3.5), I.line([[563, 622], [563, 1020]], 2.1, COP, 8, "known", 3.5)] +
           [I.dot(round(437 + (j % 2) * 126, 1), 1030, 4, "#f5ecdc", round(5.0 + .1 * j, 2)) for j in range(6)] +
           [I.box(448, 622, 104, 418, "none", I.AMBER, 3, 4, 7.4, fx="draw", dur=1.0), I.label(500, 1290, "core", 7.8, I.AMBER, 32)]}
    # 6 · the bow drill from a grave some 750 years older than Khufu (c. 3300 BCE)
    T = lambda yr: round(150 + 700 * (yr + 4000) / 2000, 1)
    bow = {"base": "dark", "floor": 940, "cam": [1, 500, 900], "els": [I.box(150, 940, 700, 30, "#6d5a52", r=4, at=.2),
           I.line([[500, 480], [500, 930]], .4, COP, 14, "known", .8), I.box(470, 450, 60, 34, "#8a6a48", r=6, at=.6),
           I.line([[110, 1150], [890, 1150]], .8, "#8c7152", 3, "known", .6),
           I.dot(T(-3300), 1150, 12, COP, 1.6), I.label(T(-3300), 1205, "the drill", 1.6, COP, 28),
           I.dot(T(-2560), 1150, 12, I.AMBER, 2.4), I.label(T(-2560), 1205, "Khufu", 2.4, I.AMBER, 28),
           I.arrow([[T(-3300), 1110], [(T(-3300) + T(-2560)) / 2, 1070], [T(-2560), 1110]], 2.8, I.BONE, 3, "known", 1.0),
           I.label((T(-3300) + T(-2560)) / 2, 1040, "about 750 years", 3.2, I.BONE, 30)] +
          [I.line([[486, 700 + 14 * j], [514, 708 + 14 * j]], round(4.6 + .1 * j, 2), "#b8875a", 4, draw=False) for j in range(5)] +
          [I.line([[150, 760], [300, 650], [500, 625], [700, 650], [850, 760]], 6.6, "#8a6a48", 9, "known", .8, curve=True),
           I.line([[150, 760], [486, 700]], 6.9, "#b8875a", 3, "known", .5), I.line([[514, 764], [850, 760]], 6.9, "#b8875a", 3, "known", .5),
           I.arrow([[300, 830], [700, 830]], 7.4, I.AMBER, 3, "known", .6, False), I.arrow([[700, 870], [300, 870]], 7.8, I.AMBER, 3, "known", .6, False),
           {"k": "line", "p": I.ellipse(500, 900, 46, 12, 24, 200, 520), "c": I.BLUE, "w": 3, "curve": True, "in": 8.2, "fx": "draw", "dur": .6}]}
    # verdict: back to the core; then the recipe: copper and sand
    recipe = [I.box(190, 850, 60, 210, COP, r=4, at=4.6, fx="rise"), I.label(220, 1110, "copper", 4.8, COP, 30),
              {"k": "poly", "p": [[690, 1060], [720, 1010], [780, 990], [840, 1010], [870, 1060]], "fill": "#e8dcc2", "c": "none", "w": 0, "curve": True, "in": 6.2, "fx": "rise"},
              I.label(780, 1110, "sand", 6.4, "#f5ecdc", 30)]
    return remix(ep, scenes={3: spiral, 5: tube, 6: bow}, alias={7: 0}, cams={7: [1.2, 500, 880], 0: [1.45, 500, 860]}, line_adds={(5, 1): (recipe, None)})


def stone_vases_m():
    """The stone vases as one continuous take: a scan finer than a hair, a lathe nobody found, and a hundred working days for one jar."""
    remix, I = _mur()
    ep = F.stone_vases()
    # 3 · the scans: light sweeps the surface; a thousandth of an inch against a hair
    scan = {"base": "dark", "floor": 1182, "cam": [1, 500, 880], "els": [{"k": "glow", "x": 420, "y": 960, "r": 340, "kind": "lamp", "op": .3},
            {"k": "vase", "x": 420, "y": 1180, "h": 420, "w": 300, "veins": True, "tone": "#8a8a90", "in": .1}] +
           [I.line([[250, round(790 + j * 28, 1)], [590, round(790 + j * 28, 1)]], round(1.2 + .1 * j, 2), I.BLUE, 1.6, "known", .4, op=.6) for j in range(14)] +
           [I.glow(640, 760, 60, 1.2, .8, "scan"), I.ring(520, 800, 26, 4.4, GOLD_, 3, "known", .4), I.line([[540, 785], [650, 650]], 4.6, GOLD_, 2, "inferred", .4),
            I.oval(750, 540, 140, 140, "#2a2420", "#f2dcb4", 2.5, 1, 4.8),
            I.line([[800, 420], [800, 660]], 5.4, I.BLUE, 6, "known", .5), I.line([[700, 420], [712, 660]], 6.6, "#9a6a3a", 18, "known", .5),
            I.label(706, 725, "a hair", 6.8, "#d9a066", 28, "end"), I.label(800, 725, "1/1000 inch", 5.6, I.BLUE, 28, "start"),
            I.box(90, 860, 80, 150, "none", I.LILAC, 3, 6, 10.0, style="claimed"), I.line([[170, 935], [250, 935]], 10.2, I.LILAC, 3, "claimed", .4),
            I.line([[80, 1240], [700, 1240]], 10.2, I.LILAC, 3, "claimed", .6), I.label(130, 1300, "a lathe?", 10.6, I.LILAC, 30, "start")]}
    # 7 · long hours of grinding with sand, day after day, for one jar (no figure: none could be verified)
    days = {"base": "dark", "floor": 1100, "cam": [1, 500, 880], "els": [{"k": "glow", "x": 200, "y": 980, "r": 220, "kind": "lamp", "op": .3},
            {"k": "vase", "x": 200, "y": 1100, "h": 260, "w": 180, "tone": "#8a8a90", "in": .2},
            I.label(630, 690, "day after day", 1.2, GOLD_, 56, st="serif")] +
           [I.box(380 + 46 * j, 760, 38, 38, I.AMBER, r=5, at=round(3.0 + .12 * j, 2), fx="pop") for j in range(10)] +
           [I.arrow([[850, 779], [930, 779]], 4.3, I.AMBER, 3, "inferred", .6, False), I.label(630, 870, "for one jar", 5.0, I.BONE, 32)]}
    dig = [I.box(120, 1250, 760, 150, "#5f4c39", r=4, at=.4), {"k": "vase", "x": 500, "y": 1385, "h": 110, "w": 90, "tone": "#b89a78", "in": 1.0}] + \
          [I.line([[430, round(1290 + 18 * j, 1)], [570, round(1290 + 18 * j, 1)]], round(2.6 + .1 * j, 2), I.BLUE, 1.6, "known", .3, op=.7) for j in range(5)] + \
          [I.glow(500, 1330, 90, 3.4, .7, "scan")]
    return remix(ep, scenes={3: scan, 7: days}, cams={0: [1.35, 500, 860]}, line_adds={(5, 1): (dig, None)})


def serapeum_m():
    """The Serapeum boxes as one continuous take: a straightedge and a square, three royal names, a six-inch check on a four-metre wall, and twenty-four scans."""
    remix, I = _mur()
    ep = F.serapeum()
    GR, GRD = "#5f5a58", "#3f3b3a"
    # 3 · Dunn's check: a straightedge laid on the inner face, a square in the corner
    check = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "glow", "x": 450, "y": 700, "r": 380, "kind": "lamp", "op": .3},
             I.box(160, 380, 90, 520, GR, "#9a938a", 1.5, 2, .1), I.box(160, 880, 700, 70, GR, "#9a938a", 1.5, 2, .1),
             I.line([[500, 874], [800, 874]], 1.4, "#e9dccb", 10, "known", .6), I.label(650, 835, "straightedge", 1.6, "#e9dccb", 28),
             I.line([[262, 560], [262, 872], [450, 872]], 2.2, GOLD_, 9, "known", .8), I.label(300, 520, "square", 2.4, GOLD_, 28, "start"),
             I.line([[500, 880], [800, 880]], 3.6, "#ffe2a8", 2, "known", .6, op=.8), I.glow(650, 880, 90, 3.6, .5),
             I.glow(262, 872, 80, 4.8, .55),
             I.arrow([[800, 470], [520, 470]], 9.2, I.LILAC, 3, "claimed", .8, False), I.label(820, 480, "far older?", 9.6, I.LILAC, 30, "start")]}
    # return to it: a six-inch straightedge against a wall nearly four metres long, a few spot checks
    L0, L1 = 120, 880
    six = L0 + (L1 - L0) * .1524 / 3.85
    spot = [I.line([[L0, 1080], [L1, 1080]], .4, "#9a938a", 10, "known", .8),
            I.box(300, 1068, round(six - L0, 1), 24, GOLD_, r=3, at=1.0, fx="pop"), I.label(315, 1145, "6 inches", 1.2, GOLD_, 28)] + \
           [I.box(x, 1068, round(six - L0, 1), 24, GOLD_, r=3, at=at, fx="pop") for x, at in ((520, 1.8), (700, 2.2))] + \
           [I.label(500, 1035, "c. 3.85 m", 3.8, "#cbbca8", 28)]
    lap = [I.box(200, 1300, 600, 80, GR, "#9a938a", 1.5, 3, .4), I.box(400, 1236, 170, 60, GRD, "#9a938a", 1.5, 6, 1.2, fx="pop"),
           I.arrow([[380, 1206], [600, 1206]], 1.6, I.AMBER, 3, "known", .5, False), I.arrow([[590, 1222], [370, 1222]], 2.0, I.AMBER, 3, "known", .5, False)] + \
          [I.dot(round(395 + 23 * j, 1), 1299, 4, "#f5ecdc", round(2.6 + .05 * j, 2)) for j in range(8)] + \
          [I.label(585, 1280, "sand", 2.8, "#f5ecdc", 28, "start")]
    # 4 · royal names carved on the boxes
    names = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "glow", "x": 500, "y": 860, "r": 420, "kind": "lamp", "op": .3},
             I.box(130, 660, 740, 420, GR, "#9a938a", 2, 4, .2), I.box(130, 640, 740, 40, GRD, "#9a938a", 2, 4, .2)] +
            sum([[I.box(150 + 240 * j, 800, 220, 90, "rgba(242,201,142,.08)", GOLD_, 3, 45, at, fx="draw", dur=.6),
                  I.label(260 + 240 * j, 856, n, at + .3, GOLD_, 32, st="serif")] for j, (n, at) in enumerate((("Amasis", 3.4), ("Cambyses", 4.1), ("Khababash", 4.8)))], [])}
    from scenes import timeline
    tl, ax = timeline(-1400, 0, [(-1400, "1400 BCE"), (-1000, "1000"), (-600, "600"), (-200, "200"), (0, "1 CE")], "Burials of the Apis bulls", y=1000)
    kings = [I.dot(round(ax.x(y), 1), 690, 10, GOLD_, at) for y, at in ((-548, 1.0), (-525, 1.3), (-336, 1.6))] + \
            [I.label(round(ax.x(-440), 1), 650, "the kings", 1.8, GOLD_, 30),
             I.box(round(ax.x(-612), 1), 770, round(ax.x(-30) - ax.x(-612), 1), 38, "none", GOLD_, 3, 12, 5.4, fx="draw", dur=1.0)]
    # 6 · the test that would settle it: scan all twenty-four
    grid = [I.box(150 + 190 * (j % 4), 470 + 130 * (j // 4), 120, 70, GR, "#9a938a", 1.5, 4, round(.2 + .02 * j, 2), op=.75) for j in range(24)] + \
           [I.box(150 + 190 * (j % 4), 470 + 130 * (j // 4), 120, 70, "rgba(159,208,255,.45)", I.BLUE, 2, 4, round(9.0 + .12 * j, 2), fx="pop") for j in range(24)] + \
           [I.label(500, 1320, "24 boxes", .6, "#cbbca8", 30), I.glow(500, 820, 380, 12.2, .25, "scan")]
    return remix(ep, scenes={3: check, 4: names, 6: {"base": "dark", "cam": [1, 500, 880], "els": grid}}, adds={5: kings},
                 beat_adds={4: (spot, None)}, line_adds={(4, 1): (lap, None)})


def power_plant_m():
    """The power plant as one continuous take: three places to look, salt from the stone, quartz that cancels, a king's name, and people."""
    remix, I = _mur()
    ep = F.power_plant()
    from giza import Section
    S = Section(s=3.6, cx=500, gy=1150)
    R = S.rooms(); body = S.body(); inner = S.els()
    shade = {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0}
    kc = S.P(R["kc"][0], R["kc"][1] + 3); qc = S.P(R["qc"][0], R["qc"][1] + 3)
    # 3 · a machine leaves traces: three places to look
    look = {"base": "section", "tod": "night", "ground": 1150, "far": [[95, 220], [915, 110]], "layers": [{"d": 0, "c": "#6f5a43"}, {"d": 60, "c": "#4d3e30"}],
            "cam": [1.3, 520, 960], "els": [body, shade] + inner + [
            I.ring(qc[0], qc[1], 30, 5.4, I.AMBER, 4, "known", .5), I.line([[qc[0] + 30, qc[1] + 8], [700, 1090]], 5.5, I.AMBER, 2, "known", .3), I.label(710, 1100, "salt", 5.6, I.AMBER, 30, "start"),
            I.ring(kc[0], kc[1], 26, 5.8, I.AMBER, 4, "known", .5), I.line([[kc[0] + 26, kc[1]], [700, 1010]], 5.9, I.AMBER, 2, "known", .3), I.label(710, 1020, "granite", 6.0, I.AMBER, 30, "start"),
            I.ring(kc[0], kc[1] - 50, 22, 6.2, I.AMBER, 4, "known", .5), I.line([[kc[0] + 22, kc[1] - 54], [700, 920]], 6.3, I.AMBER, 2, "known", .3),
            I.label(710, 930, "sealed rooms", 6.4, I.AMBER, 30, "start")] +
            [I.ring(300, 820, 60, 4.4, "#e9dccb", 5, "known", .5), I.line([[258, 862], [200, 930]], 4.6, "#e9dccb", 9, "known", .3)]}
    # 4 · the salt: limestone laid down under an ancient sea; water carries its salt out to the face
    salt_x = 640
    cubes = lambda pts, at: [{"k": "poly", "p": [[x, y - 9], [x + 10, y], [x, y + 9], [x - 10, y]], "fill": "#f4f1ea", "c": "#ffffff", "w": 1, "in": round(at + .08 * j, 2), "fx": "pop"}
                             for j, (x, y) in enumerate(pts)]
    salt = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(150, 560, salt_x - 150, 700, "#cdb58a", "#8a7a66", 2, 4, .2)] +
            [I.line([[150, 640 + 110 * j], [salt_x, 650 + 110 * j]], .3, "#b49d74", 2, draw=False) for j in range(6)] +
            cubes([(salt_x + 6, 640 + 70 * j) for j in range(4)], .8) +
            [I.label(salt_x + 40, 600, "rock salt", 3.4, "#f4f1ea", 30, "start"), I.label(395, 1320, "limestone", 4.0, "#cdb58a", 30)] +
            [I.line([[150 + 40 * k, round(470 + 12 * math.sin(k), 1)] for k in range(13)], 5.6 + .3 * w, I.BLUE, 3, "known", 1.0, curve=True) for w in range(2)] +
            [I.line([[150 + 40 * k, round(500 + 12 * math.sin(k + 1), 1)] for k in range(13)], 5.9, I.BLUE, 3, "known", 1.0, curve=True)] +
            [{"k": "line", "p": [[x + 8 * math.cos(t / 3), y + 8 * math.sin(t / 3)] for t in range(0, 19)], "c": "#8a7a66", "w": 2, "curve": True, "in": round(6.2 + .1 * j, 2)}
             for j, (x, y) in enumerate(((230, 760), (330, 980), (470, 700), (260, 1150), (520, 1100), (400, 850)))] +
            [I.arrow([[200 + 60 * (j % 3), 700 + 130 * j], [salt_x - 20, 680 + 130 * j]], round(7.0 + .3 * j, 2), I.BLUE, 3, "inferred", .8, False) for j in range(4)] +
            cubes([(salt_x + 6, 920 + 60 * j) for j in range(5)], 8.6)}
    # 6 · the sealed rooms: the iso stack keeps its model, without its words
    stack = copy.deepcopy(ep["shots"][6])
    stack["els"] = [e for e in stack["els"] if e.get("k") not in ("cap", "label")]
    marks = [I.label(x, y, "Khufu", round(2.6 + .3 * j, 2), "#e4553a", 30, st="ital") for j, (x, y) in enumerate(((250, 560), (760, 640), (230, 820), (780, 930), (300, 1080)))]
    crowd = [I.person(140 + 60 * j, 1330, 46, round(3.0 + .08 * j, 2)) for j in range(13)]
    return remix(ep, scenes={3: look, 4: salt, 6: stack}, line_adds={(4, 1): (marks, None), (5, 1): (crowd, None)})


def EPISODES():
    return [orion_m(), metrology_m(), drill_cores_m(), stone_vases_m(), serapeum_m(), power_plant_m()]
