"""File 15 · Carthage and Before. Tunisia first, then the wider Maghreb: the tophet, the salt that never was, the Capsian
snail mounds, the stone that spoke two languages, a cone of stone balls at a spring, the lake of the Argonauts, a Punic town
abandoned overnight, and the oldest known fossils of our own species. Human remains (the tophet infants) are never shown;
Punic religion is described, never mocked; ancestry is never modern identity."""
import math
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, skull, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box, sphere

SERIES = "Carthage and Before"
SEA = "#3f86b0"
SALT = "#e9e2d2"
PUNIC = "#b85a3c"


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


def tunisia(pins, lon0=7.2, lon1=12.2, lat0=32.2, lat1=37.6, extra=(), cam=None, sea=(11.6, 35.2)):
    v = View(lon0, lon1, lat0, lat1, (40, 330, 920, 900))
    lab = [{"k": "label", "x": v.p(*sea)[0], "y": v.p(*sea)[1], "t": "the Mediterranean", "st": "ital", "c": "#9fd0ff"}] if sea else []
    return mapshot(v, pins=pins, extra=list(extra) + lab, cam=cam), v


# ---------------------------------------------------------------- 15.01 The tophet of Carthage
def tophet():
    field = [{"t": "slab", "x0": -34, "x1": 34, "z0": -22, "z1": 22, "y": 0, "c": "#8f7a5c"}]
    for r in range(5):
        for c in range(9):
            x = -28 + c * 7 + (r % 2) * 3.5; z = -16 + r * 8
            field.append({"t": "cyl", "x": x, "z": z, "y": 0, "r": .9, "h": 1.6, "c": "#b88b5e", "n": 12, "edge": "rgba(0,0,0,.25)"})
            if (r + c) % 3 == 0:
                field.append(box(x + 1.8, z - 1.2, 0, 1.4, .5, 4.2, "#d9cbb0"))
    field += [L_(0, 5, "urns and stone markers · schematic", GOLD, z=-22, dy=-24), L_(0, 0, "no remains are shown here", "#cfe6ff", z=22, dy=44)]
    s0 = iso(field, cam=[1, 500, 920], s=9, x=500, y=1010, az=-26, spin=1.2, el=.45, table=None)
    s1, v = tunisia([("Carthage · the tophet", 10.323, 36.844, {"c": GOLD}), ("Tunis", 10.18, 36.8, {"a": "end", "lx": -18, "ly": 30}), ("Zita", 11.1, 33.5, {"c": SCAN})])
    s2 = stat("c. 20,000", "urns", "estimated for c. 400–200 BCE alone, by the team that dug the tophet in the 1970s", "Stager, Carthage excavations")
    s3 = quote("They chose two hundred of the noblest children and sacrificed them publicly.", "Diodorus 20.14 · some 280 years later", size=42)
    bars = []
    A = [.9, .7, .5, .35, .25, .2, .15]; Bv = [.2, .3, .55, .9, .6, .35, .2]
    for k, (a, b) in enumerate(zip(A, Bv)):
        x = 170 + k * 44; bars.append({"k": "rect", "x": x, "y": 1040 - a * 300, "w": 34, "h": a * 300, "fill": SCAN, "c": "none", "sw": 0, "in": .3 + k * .06})
        x2 = 570 + k * 44; bars.append({"k": "rect", "x": x2, "y": 1040 - b * 300, "w": 34, "h": b * 300, "fill": AMBER, "c": "none", "sw": 0, "in": .6 + k * .06})
    s4 = {"base": "dark", "cam": [1, 500, 880], "els": bars + [
        {"k": "line", "p": [[150, 1042], [480, 1042]], "c": "#8c7152", "w": 2}, {"k": "line", "p": [[550, 1042], [880, 1042]], "c": "#8c7152", "w": 2},
        {"k": "label", "x": 315, "y": 1100, "t": "many before birth", "st": "small", "c": SCAN, "in": .5},
        {"k": "label", "x": 715, "y": 1100, "t": "a peak at 1–2 months", "st": "small", "c": AMBER, "in": .8},
        {"k": "cap", "x": 500, "y": 600, "t": "two teams, two age profiles · schematic", "in": .2},
        {"k": "label", "x": 500, "y": 1190, "t": "Schwartz et al. 2010 · Smith et al. 2011", "st": "small", "c": "#b9aa97", "in": 1.0}]}
    tl, ax = timeline(-800, 100, [(-800, "800 BCE"), (-600, "600"), (-400, "400"), (-200, "200"), (0, "1 CE")], "The tophet, as dated")
    tl["els"] += [{"k": "band", "x0": ax.x(-750), "x1": ax.x(-146), "y": 745, "h": 16, "c": PUNIC, "t": "the tophet in use", "in": .3}] + \
                 event(ax, -310, "Diodorus' crisis", row=1, c=AMBER, i=.6) + event(ax, -146, "Rome destroys Carthage", row=2, c=RED, i=.9) + \
                 [{"k": "band", "x0": ax.x(-50), "x1": ax.x(100), "y": 440, "h": 14, "c": SCAN, "t": "Zita: care, no violence", "in": 1.2}]
    s5 = tl
    s6 = like(s0, cam=[1.16, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:CARTHAGE][sfx:boom][act:hushed, grave]Under a field in Carthage lie thousands of ^urns. [act:quiet, careful]Inside them, the ashes of ^babies.",
                      "[d:tension][cam:1.12|0|0][act:steady, the question everyone asks]For a century, scholars have argued over one ^question. [act:grave, slow][tune:rise]Were they ^sacrificed?"], cut=False),
        B("world", 1, ["[d:calm][k:THE TOPHET][act:plain, orienting]The tophet of Carthage, in today's ^Tunisia. [act:steady, factual]A sacred precinct used@verb for some six ^centuries, until Rome destroyed the city in {146|one forty-six} BCE.",
                       "[d:build][go:2|0][act:quietly astonished]One team estimated about ^twenty thousand urns from just two of those centuries."]),
        B("collision", 3, ["[d:build][k:THE TEXTS][act:serious, measured]Ancient writers say ^yes. [act:reporting, even]Diodorus claims two hundred noble children were sacrificed in a single crisis, in {310|three ten} BCE. [act:fair, a caveat]He wrote ^centuries later, and as an ^outsider.",
                           "[d:build][act:careful, precise]Stone markers above the urns record@verb ^vows to the gods Baal Hammon and ^Tanit."]),
        B("cost", 4, ["[d:build][k:THE BONES][act:laying out the evidence, calm]Then scientists weighed the ^bones. [act:even, clear]One team found many babies who died ^before birth, a pattern that fits ^natural deaths.",
                      "[d:build][act:the counterpoint, fair]Another found most had died at one to two ^months old: too ^regular, they argue, to be chance."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:the crux, slower]And here's the ^catch. [act:gentle, precise]Burned bone can show ^age, but rarely the cause of ^death.",
                          "[d:build][act:warm, careful]At Zita, in southern Tunisia, a later cemetery of infants showed ^illness, and signs of ^care. [act:plain]No violence at ^all."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Child sacrifice at ^Carthage? [act:the verdict, even][tune:fall]*Mixed ^record@noun*. [act:fair, clear]The texts point one ^way. The bones can't ^confirm it.",
                     "[d:tension][p:0.93][act:quiet, humane]Whatever happened here, these were ^children. [act:the last word, gentle][tune:fall]And someone ^mourned them."]),
    ]
    return EP("tophet", "15.01", "Carthage: Sacrifice or Cemetery?", "tophet", "mixed", "Did Carthage sacrifice its children, or is the tophet a cemetery for infants who died naturally?", "Were they *sacrificed*?", beats, shots,
              "Schwartz et al. 2010 (doi:10.1371/journal.pone.0009177) · Smith et al. 2011 (doi:10.1017/S0003598X00068368) · Xella et al. 2013 · Schwartz et al. 2017 (doi:10.15184/aqy.2016.270) · Cerezo-Román et al. 2024 (doi:10.15184/aqy.2024.85) · Garnand & Greene 2023 · Diodorus 20.14",
              "Twenty thousand urns, a Greek historian's accusation, and two teams of scientists reading the same bones in opposite ways. What the tophet of Carthage can and cannot tell us.",
              ["#Carthage", "#Tunisia", "#Archaeology", "#AncientHistory", "#CarthageAndBefore"])


def tophet_m():
    """The tophet as one continuous take (see mural.py): six centuries and two hundred marks of a hundred urns, a late outsider's account,
    a marker of a vow, two age profiles from two teams, and a calendar that tells when but not why. No remains are ever drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box, oval, question, ring, AMBER, BLUE, GREEN, BONE, LILAC
    ep = tophet()
    # 2 · six centuries of use (c. 750 to 146 BCE), two of them (400 to 200 BCE) holding c. 20,000 urns: 200 marks of 100
    X = lambda yr: round(120 + (yr + 750) / 604 * 760, 1)
    urns = [box(X(-400) + 2 + 25 * (k % 10), 1176 - 25 * (k // 10), 20, 20, "#b88b5e", r=7, at=round(1.6 + .012 * k, 3), fx="pop") for k in range(200)]
    span = {"base": "dark", "cam": [1, 500, 900], "els": [
        box(120, 1230, 760, 22, PUNIC, r=11, at=.2, fx="fill", dur=1.0),
        label(120, 1300, "c. 750 BCE", .6, "#cbbca8", 28, "start"), label(880, 1300, "146 BCE", .9, RED, 28, "end"),
        box(X(-400), 1220, X(-200) - X(-400), 42, "none", GOLD, 3, 8, 1.1, fx="draw")] + urns + [
        label(686, 650, "two centuries", 1.3, GOLD, 32),
        label(330, 900, "c. 20,000 urns", 4.2, BONE, 40, st="serif"), label(330, 960, "1 mark = 100 urns", 4.6, "#cbbca8", 28)]}
    # 3 · Diodorus: a crisis in 310 BCE, told some 280 years later, from outside the city
    D = lambda yr: round(140 + (yr + 400) / 400 * 720, 1)
    texts = {"base": "dark", "cam": [1, 500, 900], "els": [
        line([[120, 640], [880, 640]], .2, "#8c7152", 3),
        ring(D(-310), 640, 62, 1.0, PUNIC, 3), dot(D(-310), 640, 10, PUNIC, 1.2), label(D(-310), 545, "Carthage, 310 BCE", 1.6, PUNIC, 30),
        person(D(-30), 632, 130, 4.2), box(D(-30) + 26, 545, 34, 44, BONE, r=4, at=4.6, fx="pop"), label(D(-30), 470, "Diodorus", 4.6, AMBER, 32),
        arrow([[D(-310), 740], [D(-30) - 10, 740]], 5.4, AMBER, 3, "known", 1.2, False), label((D(-310) + D(-30)) / 2, 712, "c. 280 years later", 6.2, AMBER, 32),
        line([[D(-30) - 30, 600], [D(-310) + 70, 620]], 8.4, LILAC, 2, "claimed", 1.0)]}
    # 3, second line · the marker of a vow, standing over an urn
    vow = [box(80, 1060, 840, 340, "#4a3a2c", r=4, at=.2, fx="fill", dur=.8), line([[80, 1060], [920, 1060]], .2, "#8a6a48", 3, draw=False),
           {"k": "poly", "p": [[470, 1190], [530, 1190], [540, 1210], [575, 1245], [580, 1300], [555, 1345], [445, 1345], [420, 1300], [425, 1245], [460, 1210]],
            "fill": "#b88b5e", "c": "#e0c49a", "w": 2, "curve": True, "in": .6, "fx": "pop"},
           {"k": "poly", "p": [[440, 1062], [560, 1062], [560, 880], [500, 820], [440, 880]], "fill": "#d9cbb0", "c": "#fff3dc", "w": 2, "in": 1.4, "fx": "rise"},
           {"k": "poly", "p": [[500, 935], [468, 1030], [532, 1030]], "fill": PUNIC, "c": "none", "w": 0, "in": 2.2, "fx": "pop"},
           line([[462, 935], [538, 935]], 2.4, PUNIC, 6, dur=.4), dot(500, 905, 15, PUNIC, 2.6),
           glow(500, 940, 120, 3.0, .45), label(600, 900, "a vow", 3.0, AMBER, 34, "start"), label(600, 950, "to Baal Hammon, Tanit", 3.4, "#cbbca8", 28, "start")] + \
        question(800, 1180, 5.6, 90)
    # 4 · two teams, two age profiles (schematic): many before birth / a sharp peak at one to two months
    A = [.9, .75, .6, .45, .3, .2, .15]; Bv = [.15, .25, .4, .6, .95, .45, .2]
    bx = lambda k: 150 + k * 100
    def chart(base, vals, c, at, name):
        out = [line([[120, base], [880, base]], at, "#8c7152", 2, draw=False),
               line([[bx(3) - 15, base + 10], [bx(3) - 15, base - 330]], at + .4, BONE, 2, "inferred", .6),
               label(120, base - 345, name, at + .2, c, 30, "start")]
        out += [box(bx(k), base - v * 280, 70, v * 280, c, r=4, at=round(at + 1.0 + .15 * k, 2), fx="fill", dur=.7) for k, v in enumerate(vals)]
        return out
    ages = {"base": "dark", "cam": [1, 500, 900], "els": chart(820, A, BLUE, .3, "team one") + [
        label(bx(3) - 15, 460, "birth", 1.0, BONE, 28), label(bx(1) + 35, 870, "before birth", 3.0, BLUE, 30),
        glow(bx(1) + 35, 650, 170, 3.4, .4)]}
    team2 = chart(1330, Bv, AMBER, .2, "team two") + [label(bx(4) + 35, 1380, "1 to 2 months", 2.4, AMBER, 30), ring(bx(4) + 35, 1130, 70, 2.8, AMBER, 3)]
    # 5 · the catch: a calendar of age, its last page (the cause) missing; then Zita, a later clue of illness and care
    days = [box(175 + 52 * (k % 5), 640 + 52 * (k // 5), 40, 40, "#3a3029", "#8c7152", 1.5, 4, round(.8 + .04 * k, 2)) for k in range(20)]
    catch = {"base": "dark", "cam": [1, 500, 900], "els": [box(150, 560, 290, 330, "#d8c9a8", "#8a7a66", 2, 10, .3), box(150, 560, 290, 56, PUNIC, r=10, at=.4)]
             + [dot(205 + 60 * k, 560, 9, BONE, .5) for k in range(4)] + days
             + [box(175 + 52 * 2, 640 + 52 * 2, 40, 40, GREEN, r=4, at=2.4, fx="pop"), glow(299, 764, 90, 2.6, .5), label(295, 950, "age", 2.8, GREEN, 34),
                box(560, 560, 290, 330, "none", LILAC, 3, 10, 3.6, style="claimed", fx="draw", dur=1.0), label(705, 950, "cause", 4.4, LILAC, 34)]
             + question(705, 780, 4.2, 110)}
    zita = [label(500, 1040, "Zita · later", .4, BLUE, 32), glow(560, 1240, 220, 1.2, .55, "lamp"),
            person(420, 1330, 200, 1.0), oval(580, 1310, 70, 26, "#8a6a44", "#e7c99a", 2, 1, 1.6),
            oval(580, 1286, 34, 16, "#efe6d2", "none", 0, 1, 1.8),
            arrow([[700, 1200], [890, 1060], [870, 870]], 6.0, LILAC, 3, "claimed", 1.2)]
    return remix(ep, scenes={2: span, 3: texts, 4: ages, 5: catch}, alias={6: 0}, cams={6: [1.16, 500, 960]},
                 line_adds={(2, 1): (vow, None), (3, 1): (team2, None), (4, 1): (zita, None)})


# ---------------------------------------------------------------- 15.02 The salt that never was
def salt():
    R = 16
    har = [{"t": "slab", "x0": -30, "x1": 30, "z0": -30, "z1": 30, "y": 0, "c": "#9c8a6a"},
           {"t": "cyl", "x": 0, "z": 0, "y": 0, "r": R, "h": .3, "c": SEA, "n": 40, "edge": "rgba(255,255,255,.2)"},
           {"t": "cyl", "x": 0, "z": 0, "y": 0, "r": 5, "h": 1.4, "c": "#c9b48a", "n": 28, "edge": "rgba(0,0,0,.25)"}]
    for k in range(30):
        a = 2 * math.pi * k / 30
        har.append({"t": "cyl", "x": 5.9 * math.cos(a), "z": 5.9 * math.sin(a), "y": 0, "r": .45, "h": 1.0, "c": "#e0cfa8", "n": 6, "edge": "rgba(0,0,0,.25)"})
    for k in range(48):
        a = 2 * math.pi * k / 48
        har.append({"t": "cyl", "x": (R + .6) * math.cos(a), "z": (R + .6) * math.sin(a), "y": 0, "r": .55, "h": 1.2, "c": "#d6c49c", "n": 6, "edge": "rgba(0,0,0,.25)"})
    har += [{"t": "flat", "pts": [[-2, R - 1], [2, R - 1], [2, 30], [-2, 30]], "y": .32, "c": SEA},
            L_(0, 2, "the war harbour · c. 325 m across · schematic", GOLD, z=-R, dy=-30), L_(0, 1.5, "an island for the admiral, ringed by ship sheds", "#cfe6ff", z=R + 4, dy=46)]
    s0 = iso(har, cam=[1, 500, 920], s=9, x=500, y=1010, az=-24, spin=1.4, el=.5, table=None)
    v = View(6.5, 16.5, 35.2, 43, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Carthage", 10.32, 36.85, {"c": GOLD}), ("Zama · 202 BCE", 9.4, 36.1, {"a": "end", "lx": -18, "ly": 30}), ("Rome", 12.5, 41.9, {"c": RED})],
                 extra=[{"k": "label", "x": v.p(12.2, 38.6)[0], "y": v.p(12.2, 38.6)[1], "t": "Sicily", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = stat("10", "warships", "the most Carthage was allowed after losing at Zama, in 202 BCE", "Polybius 15.18")
    s3 = like(s0, cam=[1.9, 500, 1000], add=[{"k": "cap", "x": 500, "y": 1330, "t": "c. 170 ship sheds · for a fleet of ten", "in": .6},
                                            {"k": "label", "x": 500, "y": 1395, "t": "Hurst & Stager 1978 · UNESCO campaign", "st": "small", "c": "#b9aa97", "in": 1.0}])
    s4 = stat("1930", "the first 'salting'", "a line in a modern history book. No ancient source mentions salt.", "Ridley 1986 · Stevens 1988")
    tl, ax = timeline(-300, 100, [(-300, "300 BCE"), (-200, "200"), (-100, "100"), (0, "1 CE"), (100, "100")], "The end of Punic Carthage")
    tl["els"] += event(ax, -202, "Zama: ten warships", row=1, c=AMBER, i=.3) + \
                 event(ax, -146, "the last war · the city falls", row=3, c=RED, i=.9) + event(ax, -29, "Roman Carthage founded", row=0, c=SCAN, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:CARTHAGE · 146 BCE][sfx:boom][act:epic, measured]Rome destroyed Carthage, then ^salted the earth, so nothing would ever grow ^again. [act:a wry turn, lighter]At least, that's the ^story.",
                      "[d:tension][cam:1.12|0|0][act:leaning in, intrigued][tune:fall]The real one is ^stranger."], cut=False),
        B("world", 1, ["[d:calm][k:THE CITY][act:plain, orienting]Carthage, beside today's ^Tunis. [act:setting the stakes]A trading power that fought Rome for more than a ^century.",
                       "[d:build][go:2|0][act:precise, a telling detail]After losing at Zama, in {202|two oh two} BCE, it was allowed just ^ten warships."]),
        B("collision", 3, ["[d:build][k:THE HARBOUR][act:impressed, building]Yet archaeologists found a ^circular war harbour, about three hundred and twenty-five metres across, with sheds for about a hundred and ^seventy ships.",
                           "[d:aside][act:dry, amused]For a fleet of ^ten."]),
        B("cost", 5, ["[d:build][k:THE END][act:grave, sober]In {146|one forty-six} BCE, Rome took the city after a long ^siege. [act:heavy, quiet]It was ^burned, and its people killed or ^enslaved."]),
        B("reversal", 4, ["[d:reveal][k:THE SALT][act:the twist, precise][tune:rise]And the ^salt? [act:plain, clear]No ancient writer ^mentions it. [act:revealing, a small smile]The story first appears in a history book from {1930|nineteen thirty}.",
                          "[d:build][go:5|0][act:the irony, warm]Within about a century, Rome ^rebuilt Carthage, as one of its greatest ^cities."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Salted ^earth? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:the other half, confident]A hidden war harbour for a navy it wasn't ^allowed? [act:sure][tune:fall]That part is ^real.",
                     "[d:tension][p:0.93][act:the last word, a small smile]Some myths are ancient. [act:quiet, pointed][tune:fall]This one is barely a ^century old."]),
    ]
    return EP("carthage-salt", "15.02", "Carthage: The Salt That Never Was", "carthage-salt", "debunked", "Did Rome salt the earth of Carthage in 146 BCE?", "Rome *salted* Carthage?", beats, shots,
              "Ridley 1986 (doi:10.1086/366973) · Stevens 1988 (doi:10.1086/367078) · Hurst & Stager 1978 · Polybius 15.18 · Appian, Punica 96",
              "Rome never salted Carthage: the story is a line in a 1930 history book. But the defeated city did build a hidden war harbour for a navy it was forbidden to have.",
              ["#Carthage", "#Tunisia", "#Rome", "#MythBusting", "#CarthageAndBefore"])


def salt_m():
    """The salt that never was, as one continuous take (see mural.py): ten warships, a round harbour with some 170 sheds (three football
    pitches across), the fire of 146 BCE, and two thousand years of silence before a 1930 book adds the salt."""
    from mural import remix
    from illus import arrow, line, glow, label, dot, box, oval, ring, scatter, AMBER, BLUE, GREEN, BONE, LILAC, SEA as SEA_
    ep = salt()
    # 2 · Zama, 202 BCE: ten warships allowed
    ten = {"base": "dark", "cam": [1, 500, 880], "els": [label(500, 560, "after Zama, 202 BCE", .4, AMBER, 34)] +
           [{"k": "boat", "x": 180 + 160 * (k % 5), "y": 820 + 200 * (k // 5), "w": 130, "in": round(1.6 + .22 * k, 2), "fx": "pop"} for k in range(10)] +
           [label(500, 1180, "10 warships", 4.0, BONE, 40, st="serif")]}
    # 3 · the round war harbour from above: c. 325 m across, c. 170 sheds round the rim and the island
    cx, cy, R, r = 500, 820, 290, 92
    sheds = []
    for k in range(136):
        a = 2 * math.pi * k / 136
        sheds.append(line([[round(cx + (R - 34) * math.cos(a), 1), round(cy + (R - 34) * math.sin(a), 1)], [round(cx + R * math.cos(a), 1), round(cy + R * math.sin(a), 1)]],
                          round(4.6 + .026 * k, 3), "#d6c49c", 3, draw=False))
    for k in range(34):
        a = 2 * math.pi * k / 34
        sheds.append(line([[round(cx + r * math.cos(a), 1), round(cy + r * math.sin(a), 1)], [round(cx + (r + 26) * math.cos(a), 1), round(cy + (r + 26) * math.sin(a), 1)]],
                          round(8.2 + .03 * k, 3), "#d6c49c", 3, draw=False))
    harb = {"base": "dark", "cam": [1, 500, 900], "els": [
        oval(cx, cy, R + 14, R + 14, "#9c8a6a", "none", 0, 1, .2), oval(cx, cy, R, R, SEA_, "#9fd0ff", 2, 1, .4), oval(cx, cy, r, r, "#c9b48a", "#e0cfa8", 2, 1, .9),
        arrow([[cx - R, 1185], [cx + R, 1185]], 2.4, BONE, 2, "known", .8, False), arrow([[cx + R, 1185], [cx - R, 1185]], 2.4, BONE, 2, "known", .8, False),
        label(cx, 1165, "c. 325 m", 2.8, BONE, 32)]
        + [box(cx - R + 194 * k + 3, 1235, 188, 110, "rgba(143,217,176,.18)", GREEN, 2, 4, round(3.4 + .35 * k, 2), fx="pop") for k in range(3)]
        + [line([[cx - R + 194 * k + 97, 1235], [cx - R + 194 * k + 97, 1345]], round(3.5 + .35 * k, 2), GREEN, 1.5, draw=False) for k in range(3)]
        + sheds + [label(cx, 480, "c. 170 ship sheds", 9.4, "#d6c49c", 34)]}
    lit = []
    for j, k in enumerate(range(0, 136, 14)[:10]):
        a = 2 * math.pi * k / 136
        lit.append(line([[round(cx + (R - 40) * math.cos(a), 1), round(cy + (R - 40) * math.sin(a), 1)], [round(cx + (R + 4) * math.cos(a), 1), round(cy + (R + 4) * math.sin(a), 1)]],
                        round(.3 + .12 * j, 2), GOLD, 10, draw=False))
    lit += [glow(cx, cy, 330, .4, .25)]
    # 4 · the salt: ancient accounts say nothing; c. 2,000 years later, a 1930 book
    X = lambda yr: round(120 + (yr + 200) / 2200 * 760, 1)
    grains = [dot(x, y, 4, "#f5f1e6", round(5.4 + .03 * k, 2)) for k, (x, y) in enumerate(scatter(36, 760, 900, 880, 1060, 5))]
    silence = {"base": "dark", "cam": [1, 500, 900], "els": [
        line([[110, 940], [890, 940]], .2, "#8c7152", 3), dot(X(-146), 940, 10, RED, .4), label(X(-146) - 10, 1000, "146 BCE", .5, RED, 28, "start")]
        + sum([[box(150 + 70 * k, 790, 46, 70, "#d8c9a8", "#8a7a66", 1.5, 6, round(1.4 + .3 * k, 2), fx="pop"),
                line([[158 + 70 * k, 810], [188 + 70 * k, 810]], round(1.5 + .3 * k, 2), "#8a7a66", 2, draw=False),
                line([[158 + 70 * k, 830], [184 + 70 * k, 830]], round(1.5 + .3 * k, 2), "#8a7a66", 2, draw=False)] for k in range(3)], [])
        + [label(240, 740, "ancient accounts", 2.0, "#cbbca8", 28), label(240, 700, "no salt", 2.8, GREEN, 30),
           arrow([[300, 1080], [800, 1080]], 3.4, AMBER, 3, "inferred", 1.4, False), label(550, 1130, "c. 2,000 years", 4.0, AMBER, 32),
           box(X(1930) - 45, 780, 90, 110, GOLD, "#fff3dc", 2, 6, 4.6, fx="pop"), line([[X(1930) - 45, 780], [X(1930) - 45, 890]], 4.7, "#8a6a44", 5, draw=False),
           dot(X(1930), 940, 10, GOLD, 4.6), label(X(1930) + 20, 1000, "1930", 4.8, GOLD, 30, "end")] + grains}
    tl, ax = timeline(-300, 100, [(-300, "300 BCE"), (-200, "200"), (-100, "100"), (0, "1 CE"), (100, "100")], "The end of Punic Carthage")
    fire = [glow(ax.x(-146), 800, 120, 1.0, .75, "red"), glow(ax.x(-146), 780, 70, 1.6, .6, "red")]
    return remix(ep, scenes={2: ten, 3: harb, 4: silence}, alias={6: 0}, adds={5: fire}, cams={6: [1.18, 500, 960]},
                 line_adds={(2, 1): (lit, None)})


# ---------------------------------------------------------------- 15.03 The Capsian snail mounds
def capsian():
    layers = [{"d": 0, "c": "#6f5a44", "t": "ash and burnt stone"}, {"d": 110, "c": "#b9ab94", "t": "snail shells, flint tools, bone"},
              {"d": 230, "c": "#7a6248", "t": "hearths"}, {"d": 330, "c": "#a8977c", "t": "shells again"}, {"d": 430, "c": "#5a4632", "t": "older ground"}]
    s0 = {"base": "section", "tod": "day", "ground": 600, "lx": 130, "layers": layers, "cam": [1, 500, 900],
          "els": [{"k": "label", "x": 500, "y": 1130, "t": "a Capsian mound, cut open · up to 3 m deep · schematic", "c": AMBER, "in": .5}]}
    v = View(7.2, 15.8, 33.3, 38.9, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Gafsa · old Capsa", 8.784, 34.425, {"c": GOLD}), ("Djebba", 9.10, 36.47, {"c": SCAN}), ("Pantelleria · obsidian", 11.95, 36.83, {"c": OCHRE}),
                          ("Sicily", 13.6, 37.6, {"a": "end", "lx": -18, "ly": -22})],
                 extra=[{"k": "arrow", "p": [v.p(11.0, 37.0), v.p(12.0, 37.5), v.p(12.6, 37.85)], "curve": True, "c": AMBER, "w": 2.4, "in": 1.4, "fx": "draw"},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = stat("c. 25,000", "shells per m³", "counted at one Capsian mound. Some mounds are more than 3 m deep.", "Lubell 2004")
    s3 = stat("c. 5.7%", "European ancestry", "in one forager buried at Djebba, northwest Tunisia, about 7,900 years ago", "Lipson et al. 2025, Nature")
    tl, ax = timeline(-10000, -4000, [(-10000, "10,000 BCE"), (-8000, "8000"), (-6000, "6000"), (-4000, "4000")], "The Capsian, as dated")
    tl["els"] += [{"k": "band", "x0": ax.x(-9000), "x1": ax.x(-5400), "y": 700, "h": 16, "c": GOLD, "t": "the Capsian", "in": .3}] + \
                 event(ax, -5950, "the Djebba forager", row=1, c=SCAN, i=.7) + event(ax, -5200, "farming ideas arrive", row=2, c=AMBER, i=1.0)
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("What the mounds say", "#8fd9b0", ["big game was the main meal", "snails were a side dish", "people crossed the sea"])}
    s6 = like(s1, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:GAFSA · TUNISIA][sfx:boom][act:curious, a little playful]Eight thousand years ago, people in Tunisia left ^hills of snail shells.",
                      "[d:tension][cam:1.12|0|0][act:the twist, intrigued]And one of them had an ancestor from across the ^sea."], cut=False),
        B("world", 1, ["[d:calm][k:THE CAPSIANS][act:plain, orienting]Archaeologists call them the ^Capsians, after Gafsa's ancient name, ^Capsa. [act:steady]Foragers of inland Tunisia and Algeria, from about eleven thousand to seven and a half thousand years ago."]),
        B("collision", 2, ["[d:build][k:THE MOUNDS][act:vivid, a little amazed]Their camps grew into mounds of ash, burnt stone, tools and ^shells, some more than three metres ^deep. [act:counting, amused]At one site, about twenty-five ^thousand shells in a single cubic metre."]),
        B("cost", 5, ["[d:aside][k:THE CATCH][act:light, correcting a myth]But snails weren't the ^main meal. [act:matter of fact][tune:fall]The bones say ^big game was."]),
        B("reversal", 3, ["[d:reveal][k:THE DNA][act:the reveal, leaning in]Then, in {2025|twenty twenty-five}, ancient DNA from a forager buried at ^Djebba. [act:precise, delighted]Almost six percent of his ancestry came from European ^hunter-gatherers, probably by way of ^Sicily.",
                          "[d:build][go:1|0][act:connecting it, wonder]And obsidian from the island of ^Pantelleria shows people were already crossing the ^sea."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]Stone Age sea contact between Tunisia and ^Sicily? [act:the verdict, measured][tune:fall]^*Plausible*. [act:fair, a caveat]The signal is real, but it comes from ^one person.",
                     "[d:tension][p:0.93][act:inviting, warm]We need more ^genomes. [act:the last word, a smile][tune:fall]And perhaps a few more ^snails."]),
    ]
    return EP("capsian", "15.03", "Snails, Ash and a Sicilian Ancestor", "capsian", "plausible", "Were Tunisia's Stone Age foragers cut off from Europe?", "An ancestor from across the *sea*.", beats, shots,
              "Lipson et al. 2025 (doi:10.1038/s41586-025-08699-4) · Lubell 2004 (doi:10.4312/dp.31.1) · Rahmani 2004 (doi:10.1023/B:JOWO.0000038658.50738.eb)",
              "Hills of snail shells in inland Tunisia, and one forager with an ancestor from across the sea. What the Capsian mounds and a 2025 DNA study say about Stone Age sailors.",
              ["#Tunisia", "#Prehistory", "#AncientDNA", "#Archaeology", "#CarthageAndBefore"])


# ---------------------------------------------------------------- 15.04 Dougga's bilingual stone
def dougga():
    t = [{"t": "slab", "x0": -20, "x1": 20, "z0": -20, "z1": 20, "y": 0, "c": "#9c8a6a"},
         box(0, 0, 0, 10, 10, 2.2, "#c8b692"), box(0, 0, 2.2, 8.4, 8.4, 5.4, "#d8c7a0"), box(0, 0, 7.6, 7.2, 7.2, 1.2, "#e0cfa8"),
         box(0, 0, 8.8, 6.2, 6.2, 5.0, "#d8c7a0"), box(0, 0, 13.8, 6.8, 6.8, .8, "#e0cfa8"),
         {"t": "pyr", "x": 0, "z": 0, "y": 14.6, "b": 6.2, "h": 6.2, "c": "#e6d6b2", "edge": "rgba(0,0,0,.3)"},
         {"t": "person", "x": 9, "y": 0, "z": 9, "h": 1.7},
         L_(0, 21, "the mausoleum · c. 21 m · 2nd century BCE", GOLD, z=0, dy=-26), L_(5, 2, "the inscription was here", "#cfe6ff", z=5, dy=40)]
    s0 = iso(t, cam=[1, 500, 900], s=12, x=500, y=1080, az=-30, spin=1.2, el=.4, table=None)
    s1, v = tunisia([("Dougga", 9.22, 36.42, {"c": GOLD}), ("Tunis · the Bardo", 10.13, 36.81, {"a": "end", "lx": -18, "ly": -22}), ("Carthage", 10.32, 36.85, {})])
    rows_l = [{"k": "line", "p": [[150, 700 + r * 44], [470, 700 + r * 44]], "c": "#7a6248", "w": 5, "op": .8, "in": .3 + r * .08} for r in range(7)]
    rows_r = [{"k": "line", "p": [[530, 700 + r * 44], [850, 700 + r * 44]], "c": "#5a4632", "w": 5, "op": .8, "in": .6 + r * .08} for r in range(7)]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 120, "y": 640, "w": 760, "h": 360, "fill": "#cdbb95", "c": "#fff3dc", "sw": 1.5, "in": .1}] + rows_l + rows_r + [
        {"k": "label", "x": 310, "y": 1060, "t": "Punic: readable", "st": "small", "c": AMBER, "in": 1.0}, {"k": "label", "x": 690, "y": 1060, "t": "Libyco-Berber: unknown", "st": "small", "c": SCAN, "in": 1.2},
        {"k": "cap", "x": 500, "y": 580, "t": "one text, two scripts · schematic", "in": .2},
        {"k": "label", "x": 500, "y": 1140, "t": "the stone: 69 × 207 cm · British Museum", "st": "small", "c": "#b9aa97", "in": 1.4}]}
    s3 = stat("22 of 24", "signs read", "in the eastern Libyco-Berber alphabet. The western variant is still largely unread.", "de Saulcy 1843 · Mnamon, Scuola Normale")
    tl, ax = timeline(-300, 2000, [(-300, "300 BCE"), (500, "500 CE"), (1300, "1300"), (2000, "2000")], "One stone, two thousand years")
    tl["els"] += event(ax, -150, "the tomb is built", row=1, c=GOLD, i=.3) + right(event(ax, 1842, "Reade removes the stone", row=3, c=RED, i=.7)) + \
                 right(event(ax, 1843, "sounds deciphered", row=1, c=SCAN, i=1.0)) + right(event(ax, 1910, "tomb rebuilt", row=2, c=AMBER, i=1.3))
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("What we can read", "#8fd9b0", ["names and titles", "'this person, son of that one'"]) +
          [{"k": "cap", "x": 500, "y": 860, "t": "What we can't", "c": "#ff8a7a", "in": 1.2}, {"k": "label", "x": 500, "y": 940, "t": "the language itself", "st": "serif", "size": 30, "in": 1.4}]}
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:DOUGGA · TUNISIA][sfx:boom][act:storytelling, a hint of disbelief]In {1842|eighteen forty-two}, a British consul ^wrecked a royal tomb in Tunisia, to take one ^stone.",
                      "[d:tension][cam:1.12|0|0][act:the turn, wonder]That stone let scholars read@present a lost African ^alphabet."], cut=False),
        B("world", 1, ["[d:calm][k:THE TOMB][act:plain, admiring]The Libyco-Punic mausoleum of ^Dougga: about twenty-one metres of stone, in ^three tiers, from the second century BCE."]),
        B("collision", 2, ["[d:build][k:THE STONE][act:explaining, clear]Its inscription says the same thing in ^two scripts. [act:precise]One is ^Punic, the language of Carthage, which scholars could already read@present. [act:the reveal][tune:fall]The other is ^Libyco-Berber.",
                           "[d:build][go:4|0][act:storytelling, onward]Consul Thomas Reade had it ^pulled out, and the tomb came ^down. [act:plain]The stone went to the British ^Museum."]),
        B("cost", 3, ["[d:build][k:THE KEY][act:the decipherment, delighted]Names work like ^keys. [act:precise, building]Match the names in Punic, and you learn the ^sounds of the other letters. [act:the payoff, confident]Today, twenty-two of the twenty-four eastern signs are ^read@past."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:the twist, softer]But reading letters isn't reading a ^language. [act:careful, precise]The script writes no ^vowels, and most texts are ^names: this person, son of ^that one.",
                          "[d:build][act:quiet wonder]The Tuareg script, ^Tifinagh, descends from it. [act:gentle][tune:fall]Yet the ancient language itself is still mostly ^silent."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A lost alphabet ^cracked? [act:the verdict, confident][tune:fall]^*Established*, for its sounds. [act:open, honest]What those people ^said is still an open question.",
                     "[d:tension][p:0.93][act:plain, the epilogue]The tomb was rebuilt in {1910|nineteen ten}. [act:the last word, quiet][tune:fall]The stone is still in ^London."]),
    ]
    return EP("dougga-bilingual", "15.04", "Dougga: The Stone That Spoke Two Languages", "dougga-bilingual", "solid", "How was the Libyco-Berber script deciphered, and how much of it can we really read?", "One *stone*, a lost alphabet.", beats, shots,
              "British Museum 1852,0305.1 · Mnamon (Scuola Normale Superiore), Libyco-Berber · UNESCO WHC 794 · Chabot 1940, Recueil des inscriptions libyques",
              "A consul brought down a royal tomb in Tunisia to take one stone. That stone, written in two scripts, let scholars read the sounds of a lost African alphabet, but not yet its language.",
              ["#Tunisia", "#Dougga", "#Amazigh", "#Decipherment", "#CarthageAndBefore"])


def dougga_m():
    """Dougga's stone as one continuous take (see mural.py): names as keys (a Punic name matched sign by sign), 22 of 24 signs lit,
    a script without vowels, a name and a father's name, and the letters living on in Tifinagh. Signs are schematic."""
    from mural import remix
    from illus import arrow, line, glow, label, dot, box, ring, question, person, AMBER, BLUE, GREEN, BONE, LILAC
    ep = dougga()

    def sign(kind, x, y, at, c=BONE, s=26, w=4):
        """A geometric sign in the manner of the Libyco-Berber letters (schematic)."""
        if kind == 0:
            return [ring(x, y, s * .8, at, c, w, dur=.4)]
        if kind == 1:
            return [line([[x - s, y - 9], [x + s, y - 9]], at, c, w, dur=.3), line([[x - s, y + 9], [x + s, y + 9]], at + .1, c, w, dur=.3)]
        if kind == 2:
            return [line([[x - s, y], [x + s, y]], at, c, w, dur=.3), line([[x, y - s], [x, y + s]], at + .1, c, w, dur=.3)]
        if kind == 3:
            return [box(x - s * .75, y - s * .75, s * 1.5, s * 1.5, "none", c, w, 2, at, fx="draw", dur=.4)]
        if kind == 4:
            return [dot(x, y - s * .7, 5.5, c, at), dot(x, y, 5.5, c, at + .05), dot(x, y + s * .7, 5.5, c, at + .1)]
        return [line([[x - s * .8, y + s * .8], [x, y - s * .8], [x + s * .8, y + s * .8]], at, c, w, dur=.4)]

    def punic(kind, x, y, at, c=AMBER):
        """A letter in the manner of the Punic script (schematic strokes)."""
        P = [[[-14, -24], [12, -10], [-10, 4], [8, 24]], [[-12, -22], [12, -22], [12, 0], [-8, 0], [6, 24]], [[0, -24], [0, 14], [-14, 24]], [[-16, -12], [-6, 6], [4, -12], [14, 6], [14, 24]]]
        return [line([[x + px, y + py] for px, py in P[kind % 4]], at, c, 4, dur=.4)]

    # 3 · names as keys: one name in each script, matched sign by sign; then 22 of the 24 eastern signs are read
    xs = [320, 440, 560, 680]
    key = {"base": "dark", "cam": [1, 500, 880], "els": [label(500, 470, "a name in Punic", .6, AMBER, 30),
           box(250, 510, 500, 100, "rgba(232,184,122,.08)", AMBER, 2, 14, 1.0, fx="draw")]
           + sum([punic(k, x, 560, round(1.2 + .2 * k, 2)) for k, x in enumerate(xs)], [])
           + [box(250, 690, 500, 100, "rgba(159,208,255,.08)", BLUE, 2, 14, 2.2, fx="draw")]
           + sum([sign(kind, xs[k], 740, round(2.4 + .2 * k, 2), BLUE) for k, kind in enumerate((0, 2, 1, 3))], [])
           + [line([[x, 600], [x, 700]], round(3.6 + .25 * k, 2), GREEN, 3, "inferred", .4) for k, x in enumerate(xs)]
           + [glow(x, 740, 60, round(4.0 + .25 * k, 2), .5) for k, x in enumerate(xs)]
           + [label(500, 850, "the same name in Libyco-Berber", 3.0, BLUE, 30)]}
    tiles = []
    for k in range(24):
        x = 215 + 100 * (k % 6); y = 960 + 92 * (k // 6)
        tiles.append(box(x - 40, y - 34, 80, 68, "#2c2520", "#8c7152", 1.5, 8, round(6.4 + .03 * k, 2)))
        tiles += sign(k % 6, x, y, round(6.5 + .03 * k, 2), "#9a938a", 18, 3)
        if k not in (17, 22):
            tiles.append(box(x - 40, y - 34, 80, 68, "rgba(143,217,176,.28)", GREEN, 2, 8, round(8.6 + .09 * k, 2), fx="pop"))
    tiles += question(215 + 100 * 5, 960 + 92 * 2 + 20, 11.0, 60) + question(215 + 100 * 4, 960 + 92 * 3 + 20, 11.2, 60)
    key["els"] += tiles + [label(500, 1400, "22 of 24 signs read", 11.6, GREEN, 34)]
    # 5 · no vowels: consonant signs with empty slots between; most texts are names, "this person, son of that one"
    nov = {"base": "dark", "cam": [1, 500, 900], "els": []}
    for k, kind in enumerate((2, 0, 3)):
        x = 220 + 280 * k
        nov["els"] += [box(x - 50, 470, 100, 100, "#2c2520", BLUE, 2, 10, round(.4 + .3 * k, 2))] + sign(kind, x, 520, round(.6 + .3 * k, 2), BLUE)
    for k in range(2):
        x = 360 + 280 * k
        nov["els"] += [box(x - 40, 480, 80, 80, "none", LILAC, 2.5, 10, round(2.6 + .4 * k, 2), style="claimed", fx="draw", dur=.5),
                       label(x, 538, "?", round(2.9 + .4 * k, 2), LILAC, 44, st="serif")]
    nov["els"] += [label(500, 640, "no vowels", 3.6, LILAC, 32),
                   person(330, 1000, 230, 5.0), person(660, 1000, 180, 5.6),
                   arrow([[600, 860], [500, 820], [400, 860]], 6.4, AMBER, 3, "known", .8), label(500, 790, "son of", 6.8, AMBER, 30)]
    tif = [label(250, 1080, "ancient", .3, "#cbbca8", 28)] + sum([sign(kind, 160 + 90 * k, 1150, round(.4 + .15 * k, 2), "#cbbca8", 22) for k, kind in enumerate((0, 2, 1))], []) \
        + [arrow([[420, 1150], [570, 1150]], 1.6, AMBER, 3, "known", .8, False)] \
        + sum([sign(kind, 660 + 90 * k, 1150, round(2.2 + .15 * k, 2), BLUE, 22) for k, kind in enumerate((0, 2, 1))], []) \
        + [glow(750, 1150, 150, 2.4, .45), label(750, 1230, "Tifinagh", 2.8, BLUE, 32),
           {"k": "poly", "p": [[380, 1290], [620, 1290], [620, 1380], [470, 1380], [430, 1415], [440, 1380], [380, 1380]], "fill": "none", "c": LILAC, "w": 2.5, "style": "claimed", "in": 4.4, "fx": "draw", "dur": .8},
           label(500, 1352, "?", 5.0, LILAC, 44, st="serif")]
    return remix(ep, scenes={3: key, 5: nov}, alias={6: 0}, cams={6: [1.15, 500, 960]}, line_adds={(4, 1): (tif, None)})


# ---------------------------------------------------------------- 15.05 El Guettar's cone of stone balls
def el_guettar():
    cone = [{"t": "slab", "x0": -12, "x1": 12, "z0": -12, "z1": 12, "y": 0, "c": "#8f7a5c"},
            {"t": "flat", "pts": [[5, -11], [11.5, -11], [11.5, 4], [5, 4]], "y": .05, "c": SEA}]
    rings = [(0, 3.2, 12), (.9, 2.5, 9), (1.8, 1.8, 7), (2.6, 1.1, 5), (3.3, .4, 2)]
    for y, rr, n in rings:
        for k in range(n):
            a = 2 * math.pi * k / n + y
            cone += sphere(rr * math.cos(a) - 2, rr * math.sin(a), .5, c="#d9ccb4" if k % 2 else "#c6b79c", n=6, y=y)
    cone += [{"t": "person", "x": 7, "y": 0, "z": 7, "h": 1.7},
             L_(-2, 4.3, "c. 0.75 m high · more than 60 stone balls", GOLD, z=0, dy=-26), L_(8, 0, "the spring", "#9fd0ff", z=-4, dy=30)]
    s0 = iso(cone, cam=[1, 500, 900], s=22, x=500, y=1060, az=-30, spin=1.4, el=.42, table=None)
    s1, v = tunisia([("El Guettar", 8.949, 34.337, {"c": GOLD}), ("Gafsa", 8.784, 34.425, {"a": "end", "lx": -18}), ("the Bardo Museum", 10.13, 36.81, {"c": SCAN})])
    s2 = stat("60+", "stone balls", "piled in a cone at a spring, with Stone Age flints and the teeth of horses", "Gruet 1954 · Aouadi-Abdeljaouad & Belhouchet 2008")
    s3 = quote("A hermaion: an offering to the spring.", "Michel Gruet's name for the pile, c. 1950", size=46)
    tl, ax = timeline(-200000, 0, [(-200000, "200,000 years ago"), (-100000, "100,000"), (0, "today")], "How old is 'oldest'?")
    tl["els"] += event(ax, -176000, "Bruniquel, France", row=1, c=SCAN, i=.3, sub="Neanderthal stone rings") + \
                 [{"k": "band", "x0": ax.x(-100000), "x1": ax.x(-35000), "y": 700, "h": 16, "c": GOLD, "t": "Middle Stone Age, Maghreb", "in": .6}] + \
                 event(ax, -40000, "the popular '40,000'", row=2, c=AMBER, i=.9, sub="no modern date") + event(ax, -11600, "Göbekli Tepe", row=0, c=RED, i=1.2)
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Solid", "#8fd9b0", ["a deliberate pile", "at a spring", "with chosen teeth"]) +
          [{"k": "cap", "x": 500, "y": 860, "t": "Not yet shown", "c": "#ff8a7a", "in": 1.2}, {"k": "label", "x": 500, "y": 940, "t": "a ritual · its age", "st": "serif", "size": 30, "in": 1.4}]}
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:EL GUETTAR · TUNISIA][sfx:boom][act:hushed, intrigued]Beside a desert@noun ^spring, someone piled more than sixty stone ^balls into a cone.",
                      "[d:tension][cam:1.12|0|0][act:the big question, slow][tune:rise]Is this the oldest ^shrine on Earth?"], cut=False),
        B("world", 1, ["[d:calm][k:THE FIND][act:storytelling, plain]Around {1950|nineteen fifty}, the French archaeologist Michel ^Gruet dug it out of old spring deposits, near ^Gafsa. [act:precise]With the balls: Stone Age ^flints, and the teeth of ^horses."]),
        B("collision", 3, ["[d:build][k:THE IDEA][act:presenting his view, respectful]Gruet called it a ^hermaion: an offering to the ^spring. [act:his best argument, clear]The stones were brought ^in, the teeth ^chosen, and the pile set at the water's ^edge."]),
        B("cost", 4, ["[d:build][k:THE AGE][act:careful, a caveat]The popular claim is forty thousand ^years. [act:plain, honest][tune:fall]That's an old ^estimate@noun. [act:precise]We found no modern date for the ^deposits."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:fair, weighing]Stone balls like these may also be ^tools, or a simple ^cache.",
                          "[d:build][go:4|0][act:a larger view, wonder]And the oldest known built structure is older still: Neanderthal rings of broken stalagmites in a French cave, about a hundred and seventy-six ^thousand years old."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]The world's oldest ^shrine? [act:the verdict, even][tune:fall]*Awaiting ^evidence*. [act:practical, clear]A modern date, and a fresh look at the stones in the Bardo ^Museum, could settle it.",
                     "[d:tension][p:0.93][act:quiet wonder]Until then, it's a ^question. [act:the last word, warm][tune:fall]A very ^old one."]),
    ]
    return EP("el-guettar", "15.05", "El Guettar: The Oldest Shrine?", "el-guettar", "unsupported", "Is the cone of stone balls at El Guettar a Stone Age offering, and the oldest ritual structure known?", "The oldest *shrine* on Earth?", beats, shots,
              "Gruet 1950 (doi:10.3406/bspf.1950.2792) · Aouadi-Abdeljaouad & Belhouchet 2008 (doi:10.1007/s10437-008-9027-z) · Archaeologies 2024 (doi:10.1007/s11759-024-09492-x) · Jaubert et al. 2016 (doi:10.1038/nature18291)",
              "More than sixty stone balls piled at a desert spring in Tunisia, sometimes called the world's oldest shrine. What is solid, what is claimed, and the date nobody has measured yet.",
              ["#Tunisia", "#Prehistory", "#Neanderthals", "#Archaeology", "#CarthageAndBefore"])


# ---------------------------------------------------------------- 15.06 Lake Tritonis and the chotts
def tritonis():
    hull = [[-6, 0], [-4.5, -1.6], [4.5, -1.6], [7, 0], [4.5, 1.6], [-4.5, 1.6]]
    s = [{"t": "slab", "x0": -30, "x1": 30, "z0": -22, "z1": 22, "y": 0, "c": SALT},
         {"t": "prism", "pts": hull, "y": 0, "h": 1.6, "c": "#8a5a36", "edge": "rgba(0,0,0,.35)"},
         box(0, 0, 1.6, .3, .3, 7, "#5a4632"), box(0, .2, 3.6, 5.4, .12, 3.4, "#e9dccb"),
         {"t": "person", "x": 9, "y": 0, "z": 6, "h": 1.7},
         L_(0, 9, "the Argo, stranded in the lake · myth", GOLD, z=0, dy=-26), L_(0, 0, "Chott el Djerid today: salt", "#cfe6ff", z=16, dy=40)]
    s0 = iso(s, cam=[1, 500, 900], s=11, x=500, y=1060, az=-28, spin=1.2, el=.38, table=None)
    s1, v = tunisia([("Chott el Djerid", 8.43, 33.70, {"c": GOLD}), ("Gulf of Gabès", 10.4, 34.0, {"c": SCAN}), ("Chott Melrhir", 6.2, 34.1, {"a": "start"})], lon0=4.8, lon1=12.4, lat0=31.8, lat1=37.4, sea=None)
    s2 = stat("c. 7,000", "km²", "of salt flat that floods thinly in winter, 15 to 25 m above sea level", "Chott el Djerid")
    prof = [[150, 820], [260, 815], [380, 790], [500, 800], [620, 860], [720, 930], [820, 900], [870, 880]]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [
        {"k": "line", "p": [[140, 860], [880, 860]], "c": SEA, "w": 2, "op": .8, "in": .2}, {"k": "label", "x": 870, "y": 848, "t": "sea level", "st": "small", "a": "end", "c": "#9fd0ff", "in": .3},
        {"k": "line", "p": prof, "c": "#e9dccb", "w": 3, "curve": True, "in": .4, "fx": "draw"},
        {"k": "label", "x": 170, "y": 800, "t": "Gabès", "st": "small", "a": "start", "in": .8}, {"k": "label", "x": 420, "y": 760, "t": "the chotts of Tunisia · above", "st": "small", "in": 1.0},
        {"k": "label", "x": 720, "y": 970, "t": "Chott Melrhir · below", "st": "small", "c": SCAN, "in": 1.2},
        {"k": "cap", "x": 500, "y": 600, "t": "the 1878 plan to flood the chotts", "in": .2},
        {"k": "label", "x": 500, "y": 1100, "t": "elevation, west to east · schematic, heights exaggerated", "st": "small", "c": "#b9aa97", "in": 1.4}]}
    tl, ax = timeline(-3500, 2000, [(-3500, "3500 BCE"), (-1500, "1500 BCE"), (500, "500 CE"), (2000, "2000")], "Wet, then dry, then the myth")
    tl["els"] += [{"k": "band", "x0": ax.x(-3500), "x1": ax.x(-3000), "y": 700, "h": 16, "c": SEA, "t": "last wet period ends", "in": .3}] + \
                 event(ax, -440, "Herodotus writes", row=1, c=GOLD, i=.6) + right(event(ax, 1878, "the flooding plan", row=2, c=AMBER, i=.9)) + right(event(ax, 1930, "an 'Atlantis' claim", row=3, c=RED, i=1.2))
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Real", "#8fd9b0", ["seasonal salt lakes", "lagoons on the gulf", "a wetter past, long before"]) +
          [{"k": "cap", "x": 500, "y": 860, "t": "Not shown", "c": "#ff8a7a", "in": 1.2}, {"k": "label", "x": 500, "y": 940, "t": "a great lake in Herodotus' day", "st": "serif", "size": 30, "in": 1.4}]}
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:LAKE TRITONIS][sfx:boom][act:storytelling, wonder]Greek myth put a great ^lake in southern Tunisia. [act:playful]Jason's ship, the ^Argo, was stranded in it.",
                      "[d:tension][cam:1.12|0|0][act:the twist, dry][tune:fall]Today it's a salt flat you can ^drive across."], cut=False),
        B("world", 1, ["[d:calm][k:THE MYTH][act:plain, orienting]In the fifth century BCE, Herodotus describes Lake ^Tritonis, with a river flowing into it. [act:lightly]The goddess Athena was said to be ^born there."]),
        B("collision", 2, ["[d:build][k:THE CHOTT][act:describing, vivid]The best candidate is the Chott el ^Djerid: about seven thousand square kilometres of ^salt, that floods only thinly in ^winter.",
                           "[d:build][go:1|0][act:intrigued]And next door, in Algeria, Chott Melrhir lies ^below sea level."]),
        B("cost", 3, ["[d:build][k:THE PLAN][act:storytelling, amused]In {1878|eighteen seventy-eight}, French engineers planned to flood the chotts with a canal from the sea, and make an ^inland sea. [act:the punchline, dry][tune:fall]Surveys@noun showed most of it sat ^above sea level.",
                      "[d:aside][act:a light aside]The idea inspired one of Jules Verne's ^last novels."]),
        B("reversal", 4, ["[d:reveal][k:THE CATCH][act:careful, weighing]Cave records@noun show the region's last wet period ended about five ^thousand years ago. [act:clear][tune:fall]By Herodotus' day, it was already ^dry.",
                          "[d:build][act:sober, brief]In the {1930s|nineteen thirties}, a German geographer placed ^Atlantis here. [act:plain][tune:fall]Scientists rejected it."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]Was Lake Tritonis the ^chott? [act:the verdict, even][tune:fall]*Mixed ^record@noun*. [act:fair]Real, shifting lakes likely lie behind the ^myth.",
                     "[d:tension][p:0.93][act:the moral, warm]Myths remember ^landscapes. [act:the last word, a small smile][tune:fall]Not always the right ^century."]),
    ]
    return EP("tritonis", "15.06", "Lake Tritonis: The Lake That Moved", "tritonis", "mixed", "Was the Greek Lake Tritonis the Chott el Djerid of southern Tunisia?", "A lake you can *drive* across.", beats, shots,
              "Herodotus 4.178–180 · Apollonius, Argonautica 4 · Richards & Vita-Finzi 1982 (doi:10.1038/295054a0) · Chung et al. 2026 (doi:10.1038/s43247-026-03236-1) · Svatek 2021 (doi:10.5194/ica-abs-3-280-2021)",
              "Greek myth stranded Jason's ship in a great lake in southern Tunisia. Today it is a salt flat you can drive across. The chotts, a plan to flood the Sahara, and what the caves say.",
              ["#Tunisia", "#GreekMythology", "#Sahara", "#Argonauts", "#CarthageAndBefore"])


def tritonis_m():
    """Lake Tritonis as one continuous take (see mural.py): a salt flat the size of an 84 km square that shimmers thinly in winter,
    the 1878 canal meeting ground above sea level, and a stalagmite's layers as the region's diary."""
    from mural import remix
    from illus import arrow, line, glow, label, dot, box, oval, ellipse, strike, AMBER, BLUE, GREEN, BONE, LILAC, SEA as SEA_
    import random as _r
    ep = tritonis()
    # 2 · the Chott el Djerid: c. 7,000 km2 of salt (the same area as a square c. 84 km a side), flooding thinly in winter
    rr = _r.Random(3)
    shore = [[round(500 + 380 * math.cos(math.radians(a)) * (1 + .06 * rr.uniform(-1, 1)), 1), round(700 + 133 * math.sin(math.radians(a)) * (1 + .1 * rr.uniform(-1, 1)), 1)] for a in range(0, 360, 15)]
    flat = {"base": "dark", "cam": [1, 500, 900], "els": [
        label(500, 520, "Chott el Djerid", .4, GOLD, 34),
        {"k": "poly", "p": shore, "fill": SALT, "c": "#fff6e6", "w": 2, "curve": True, "in": .6, "fx": "pop"},
        {"k": "poly", "p": shore, "fill": "rgba(255,255,255,.0)", "c": "#cfc6b3", "w": 1, "curve": True, "in": 1.4, "style": "inferred"},
        box(300, 930, 400, 400, "rgba(233,226,210,.10)", BONE, 2.5, 2, 3.2, style="inferred", fx="draw", dur=1.0),
        label(500, 1140, "c. 7,000 km²", 4.0, BONE, 40, st="serif"), label(720, 1140, "84 km", 4.4, "#cbbca8", 28, "start"),
        line([[712, 940], [712, 1320]], 4.4, "#cbbca8", 2, draw=False),
        {"k": "poly", "p": shore, "fill": "rgba(63,134,176,.45)", "c": "#9fd0ff", "w": 2, "curve": True, "in": 6.0, "fx": "fill", "dur": 1.2},
        label(880, 880, "winter", 6.6, BLUE, 30, "end")]}
    # 3 · the 1878 plan, west to east (heights exaggerated): Chott Melrhir below sea level, the Tunisian chotts above, the sea at the east
    ground = [[80, 900], [130, 960], [200, 985], [280, 960], [340, 900], [420, 845], [500, 828], [590, 835], [670, 850], [740, 880], [790, 862], [830, 905], [850, 990]]
    plan = {"base": "dark", "cam": [1, 500, 900], "els": [
        {"k": "poly", "p": ground + [[850, 1250], [80, 1250]], "fill": "#6f5a44", "c": "none", "w": 0, "in": .2, "fx": "fill", "dur": .8},
        line(ground, .2, "#e9dccb", 3, dur=1.0, curve=True),
        {"k": "poly", "p": [[835, 905], [930, 905], [930, 1250], [850, 1250], [850, 990]], "fill": SEA_, "c": "none", "w": 0, "in": .4},
        line([[70, 905], [930, 905]], .8, "#9fd0ff", 2, "inferred", 1.0), label(80, 885, "sea level", 1.0, BLUE, 28, "start"),
        label(890, 960, "sea", 1.2, BLUE, 30), label(200, 1050, "Melrhir", 1.6, "#ff8a7a", 30), label(520, 790, "the chotts", 1.8, GOLD, 30),
        label(500, 1330, "west to east · heights exaggerated", 2.0, "#b9aa97", 28),
        arrow([[915, 895], [740, 895], [570, 895]], 3.0, AMBER, 5, "claimed", 1.4, False), label(800, 800, "canal", 3.4, AMBER, 30),
        glow(560, 880, 110, 6.4, .5, "red"), strike(530, 865, 590, 925, 6.8), strike(590, 865, 530, 925, 6.9),
        {"k": "poly", "p": [[96, 905], [130, 960], [200, 985], [280, 960], [334, 905]], "fill": "rgba(63,134,176,.7)", "c": "#9fd0ff", "w": 1.5, "in": 8.2, "fx": "fill", "dur": 1.0}]}
    verne = [box(420, 1370 - 230, 160, 210, "#5a4632", "#e9dccb", 2, 6, .4, fx="pop"), line([[432, 1142], [432, 1348]], .5, "#e9dccb", 3, draw=False),
             line([[450, 1250], [480, 1238], [510, 1250], [540, 1238], [565, 1250]], .9, BLUE, 3, curve=True), glow(500, 1245, 140, 1.0, .45)]
    # 4 · the cave's diary: a stalagmite, its layers drawn drop by drop; then the dry years
    tl, ax = timeline(-3500, 2000, [(-3500, "3500 BCE"), (-1500, "1500 BCE"), (500, "500 CE"), (2000, "2000")], "Wet, then dry, then the myth")
    stal = [{"k": "poly", "p": [[150, 1200], [250, 1200], [228, 1150], [214, 1060], [205, 990], [195, 990], [186, 1060], [172, 1150]], "fill": "#cdbb95", "c": "#fff3dc", "w": 1.5, "in": .4, "fx": "rise"}]
    stal += [line([[round(200 - (48 - 43 * (20 + 26 * k) / 210), 1), 1180 - 26 * k], [round(200 + (48 - 43 * (20 + 26 * k) / 210), 1), 1180 - 26 * k]], round(.8 + .12 * k, 2), BLUE if k in (1, 2, 3) else "#8c7152", 2, draw=False) for k in range(7)]
    stal += [dot(200, 960, 6, "#9fd0ff", .6), label(200, 1250, "a stalagmite", 1.2, "#cbbca8", 28),
             box(ax.x(-3000), 812, ax.x(2000) - ax.x(-3000), 16, "#c9a66b", r=8, at=2.8, fx="fill", dur=1.4), label(ax.x(-1200), 790, "dry", 3.4, "#c9a66b", 30)]
    return remix(ep, scenes={2: flat, 3: plan}, alias={5: 0, 6: 0}, adds={4: stal}, cams={6: [1.15, 500, 960], 4: [1.05, 500, 880]}, line_adds={(3, 1): (verne, None)})


# ---------------------------------------------------------------- 15.07 Kerkouane
def kerkouane():
    h = [{"t": "slab", "x0": -24, "x1": 24, "z0": -20, "z1": 20, "y": 0, "c": "#b3a07c"}]
    for (x, z, w, d) in [(-12, -9, 14, 1), (-12, 9, 14, 1), (-19, 0, 1, 19), (-5, 0, 1, 19), (6, -9, 12, 1), (6, 9, 12, 1), (12, 0, 1, 19), (0, 0, 1, 7)]:
        h.append(box(x, z, 0, w, d, 2.4, "#d6c49c"))
    h += [box(-15, -4, 0, 3.2, 2.2, 1.0, "#b0442c"), {"t": "cyl", "x": -9, "z": 4, "y": 0, "r": 1.0, "h": 1.0, "c": "#5a4632", "n": 12, "edge": "rgba(0,0,0,.3)"},
          {"t": "flat", "pts": [[-4, -20], [5, -20], [5, 20], [-4, 20]], "y": .02, "c": "#cbb891"},
          {"t": "person", "x": 1, "y": 0, "z": 12, "h": 1.7},
          L_(-15, 1.2, "a seated bath, red mortar", "#ffb09a", z=-4, dy=-30), L_(-9, 1.2, "a well", "#cfe6ff", z=4, dy=40), L_(0, 3, "a street", GOLD, z=-18, dy=-24)]
    s0 = iso(h, cam=[1, 500, 900], s=11, x=500, y=1060, az=-24, spin=1.2, el=.5, table=None)
    v = View(9.6, 11.6, 36.2, 37.3, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Kerkouane", 11.0992, 36.9464, {"c": GOLD}), ("Kelibia", 11.09, 36.85, {"a": "end", "lx": -18, "ly": 30}), ("Carthage", 10.32, 36.85, {})],
                 extra=[{"k": "label", "x": v.p(10.9, 37.15)[0], "y": v.p(10.9, 37.15)[1], "t": "Cap Bon", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(20), "t": "20 km"}])
    s2 = stat("c. 250", "BCE", "Kerkouane is abandoned, and never lived in again", "UNESCO World Heritage 332")
    s3 = stat("c. 1,200", "people", "on about nine hectares: a street grid, wells, baths, and purple dye from sea snails", "an estimate")
    tl, ax = timeline(-600, -100, [(-600, "600 BCE"), (-450, "450"), (-300, "300"), (-150, "150")], "The town, as dated")
    tl["els"] += [{"k": "band", "x0": ax.x(-550), "x1": ax.x(-350), "y": 700, "h": 12, "c": "#8c7152", "t": "earliest traces", "in": .3},
                  {"k": "band", "x0": ax.x(-340), "x1": ax.x(-250), "y": 700, "h": 16, "c": GOLD, "t": "the town we see", "in": .6}] + \
                 right(event(ax, -256, "Regulus lands, 256 BCE", row=2, c=RED, i=.9), dx=-14) + right(event(ax, -250, "abandoned", row=3, c=AMBER, i=1.2), dx=-14)
    s4 = tl
    s5 = like(s1, cam=[1.12, 500, 880])
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:KERKOUANE · TUNISIA][sfx:boom][act:curious, inviting]A town where nearly every house@noun had its own ^bathtub.",
                      "[d:tension][cam:1.12|0|0][act:the mystery, quieter]Then, around {250|two fifty} BCE, everyone ^left. [act:hushed][tune:fall]And nobody ever came ^back."], cut=False),
        B("world", 1, ["[d:calm][k:CAP BON][act:plain, orienting]Kerkouane, on Tunisia's Cap ^Bon: a ^Punic town, a neighbour of Carthage. [act:storytelling]Spotted in {1952|nineteen fifty-two}, and a World Heritage site since {1985|nineteen eighty-five}."]),
        B("collision", 3, ["[d:build][k:THE TOWN][act:vivid, admiring][tune:level]A grid of ^streets. [tune:level]A ^well in the courtyards. [act:the delightful detail][tune:fall]And baths with ^seats, lined in red ^mortar.",
                           "[d:build][act:precise]Perhaps twelve hundred people, who made purple ^dye from sea snails."]),
        B("cost", 0, ["[d:build][k:THE SIGNS][act:gentle, curious]In one floor, set into the paving, the sign of the goddess ^Tanit. [act:wonder]And from the tombs, a rare painted wooden ^lid, nicknamed the Princess of ^Kerkouane."]),
        B("reversal", 4, ["[d:reveal][k:THE EXIT][act:the turn, measured][tune:fall]Why ^leave? [act:weighing, careful]In {256|two fifty-six} BCE, a Roman army under ^Regulus landed on Cap Bon.",
                          "[d:build][act:the likely answer, calm]War is the likely ^reason. [act:an honest caveat][tune:fall]The link comes from the ^timing, not from a written record@noun."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it][tune:rise]A Punic town, left around {250|two fifty} BCE and never ^rebuilt? [act:the verdict, confident][tune:fall]*Strong ^evidence*. [act:open, fair]Exactly ^why, is still debated.",
                     "[d:tension][p:0.93][act:wistful]Carthage fell, and ^rose again. [act:the last word, quiet][tune:fall]Kerkouane just ^stopped."]),
    ]
    return EP("kerkouane", "15.07", "Kerkouane: The Town Nobody Rebuilt", "kerkouane", "strong", "Why was the Punic town of Kerkouane abandoned around 250 BCE and never reoccupied?", "Everyone left. Nobody came *back*.", beats, shots,
              "UNESCO WHC 332 · Fantar 1984–86, Kerkouane · Polybius 1.29 (Regulus on Cap Bon)",
              "A Punic town on Tunisia's Cap Bon, where nearly every house had its own bath. Around 250 BCE everyone left, and nobody came back. What the ruins show, and why.",
              ["#Tunisia", "#Carthage", "#Phoenicians", "#Archaeology", "#CarthageAndBefore"])


def kerkouane_m():
    """Kerkouane as one continuous take (see mural.py): the town plan drawn street by street, a well in each courtyard, a seated bath
    in each house, twelve hundred people and the purple of the sea snails; the sign of Tanit; and two dates on one page."""
    from mural import remix
    from illus import arrow, line, glow, label, dot, box, oval, person, AMBER, BLUE, GREEN, BONE, LILAC
    ep = kerkouane()
    # 3 · the town from above: streets on a grid, houses round courtyards, a well in each, a seated bath lined in red mortar
    town = {"base": "dark", "cam": [1, 500, 880], "els": [box(110, 420, 780, 560, "#9c8a6a", r=6, at=.1, op=.9)]}
    town["els"] += [box(110, 682, 780, 36, "#cbb891", r=2, at=.4, fx="draw"), box(357, 420, 36, 560, "#cbb891", r=2, at=.7, fx="draw"), box(607, 420, 36, 560, "#cbb891", r=2, at=1.0, fx="draw")]
    k = 0
    for row, y0 in enumerate((440, 736)):
        for col, x0 in enumerate((130, 413, 663)):
            w = 210 if col == 0 else 190
            town["els"] += [box(x0, y0, w, 226, "#d6c49c", "#8a6a44", 2, 4, round(1.6 + .15 * k, 2), fx="pop"),
                            box(x0 + 50, y0 + 60, w - 100, 106, "#b3a07c", r=3, at=round(1.7 + .15 * k, 2))]
            town["els"] += [dot(x0 + w / 2, y0 + 113, 13, "#3f86b0", round(3.4 + .12 * k, 2)), dot(x0 + w / 2, y0 + 113, 6, "#9fd0ff", round(3.5 + .12 * k, 2))]
            town["els"] += [box(x0 + 14, y0 + 16, 46, 30, "#b0442c", "#ffb09a", 1.5, 12, round(5.2 + .12 * k, 2), fx="pop"),
                            box(x0 + 16, y0 + 18, 16, 26, "#7a2e1e", r=4, at=round(5.3 + .12 * k, 2))]
            k += 1
    town["els"] += [label(235, 375, "a bath", 5.4, "#ffb09a", 30), arrow([[220, 390], [170, 440]], 5.6, "#ffb09a", 2, "known", .5, False),
                    label(760, 375, "a well", 3.6, BLUE, 30), arrow([[760, 390], [758, 540]], 3.8, BLUE, 2, "known", .5, False)]
    people = [person(115 + 70 * j, 1270, 86, round(.4 + .12 * j, 2)) for j in range(12)] + [label(500, 1330, "1 figure = 100 people", 2.0, "#cbbca8", 28)]
    snail = [{"k": "line", "p": [[round(330 + (4 + 3.2 * t) * math.cos(t), 1), round(1080 + (4 + 3.2 * t) * math.sin(t), 1)] for t in [i * .3 for i in range(40)]],
              "c": "#efe6d2", "w": 4, "fx": "draw", "dur": .8, "in": 2.8, "curve": True},
             arrow([[400, 1080], [500, 1080]], 3.6, "#b07ad0", 3, "known", .6, False),
             {"k": "poly", "p": [[560, 1040], [585, 1085], [575, 1110], [545, 1110], [535, 1085]], "fill": "#7b3fa0", "c": "#d9b0f0", "w": 1.5, "curve": True, "in": 4.2, "fx": "pop"},
             glow(560, 1085, 90, 4.4, .5), label(620, 1095, "purple dye", 4.6, "#d9b0f0", 30, "start")]
    # 0, again · the sign of Tanit set in a floor; the painted lid from the tombs
    tanit = [box(690, 1230, 190, 190, "#cbb891", "#8a6a44", 2, 6, .3, fx="pop"),
             {"k": "poly", "p": [[785, 1295], [750, 1395], [820, 1395]], "fill": "#f5ecdc", "c": "none", "w": 0, "in": .8, "fx": "pop"},
             line([[745, 1292], [825, 1292]], 1.0, "#f5ecdc", 6, dur=.3), dot(785, 1265, 15, "#f5ecdc", 1.2), glow(785, 1320, 140, 1.4, .5),
             label(785, 1205, "the sign of Tanit", 1.6, GOLD, 30),
             {"k": "poly", "p": [[120, 1262], [168, 1254], [200, 1286], [200, 1398], [176, 1420], [144, 1420], [120, 1398]], "fill": "#8a5a36", "c": "#e8c35a", "w": 2, "curve": True, "in": 3.4, "fx": "rise"},
             oval(160, 1306, 21, 24, "#e8d6b8", "none", 0, 1, 3.8), label(225, 1380, "a painted lid", 4.2, AMBER, 30, "start")]
    # 4, second line · two dates on the same page: the landing and the end of the town
    tl, ax = timeline(-600, -100, [(-600, "600 BCE"), (-450, "450"), (-300, "300"), (-150, "150")], "The town, as dated")
    page = [box(ax.x(-262) - 60, 420, ax.x(-246) - ax.x(-262) + 120, 430, "rgba(232,184,122,.06)", GOLD, 3, 12, .6, style="inferred", fx="draw", dur=1.2),
            label(ax.x(-254), 900, "the same moment?", 1.8, GOLD, 30, "end")]
    return remix(ep, scenes={3: town}, alias={2: 0, 5: 1, 6: 0}, cams={6: [1.15, 500, 960]}, beat_adds={3: (tanit, [1.05, 500, 1000])},
                 line_adds={(2, 1): (people + snail, None), (4, 1): (page, None)})


# ---------------------------------------------------------------- 15.08 Jebel Irhoud and Casablanca
def irhoud():
    sk = skull(500, 880, s=1.9)
    s0 = {"base": "dark", "cam": [1, 500, 880], "els": sk + [
        {"k": "label", "x": 250, "y": 1010, "t": "a modern face", "c": GOLD, "in": 1.0}, {"k": "label", "x": 720, "y": 1010, "t": "an archaic, long braincase", "c": SCAN, "in": 1.3},
        {"k": "label", "x": 500, "y": 1120, "t": "Jebel Irhoud · schematic", "st": "small", "c": "#b9aa97", "in": 1.6}]}
    v = View(-11.5, -1, 28, 36.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Jebel Irhoud", -8.873, 31.855, {"c": GOLD}), ("Casablanca · Thomas Quarry I", -7.66, 33.55, {"c": SCAN}), ("Marrakech", -7.99, 31.63, {"a": "end", "lx": -18, "ly": 30})],
                 extra=[{"k": "label", "x": v.p(-9.8, 34.6)[0], "y": v.p(-9.8, 34.6)[1], "t": "the Atlantic", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = stat("c. 315,000", "years", "burnt flints from the layer with the oldest known Homo sapiens fossils", "Hublin et al. 2017; Richter et al. 2017")
    s3 = stat("c. 773,000", "years", "jaws and teeth from a Casablanca quarry, placed near the root of our lineage", "Hublin et al. 2026, Nature")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [
        {"k": "circle", "x": 330, "y": 860, "r": 130, "fill": "none", "c": "#8c7152", "w": 3, "in": .2}, {"k": "circle", "x": 670, "y": 860, "r": 130, "fill": "none", "c": "#8c7152", "w": 3, "in": .2},
        {"k": "line", "p": [[330, 950], [330, 770]], "c": RED, "w": 6, "in": .4}, {"k": "label", "x": 330, "y": 745, "t": "S", "c": RED, "in": .5},
        {"k": "line", "p": [[670, 770], [670, 950]], "c": SCAN, "w": 6, "in": .9}, {"k": "label", "x": 670, "y": 745, "t": "N", "c": SCAN, "in": 1.0},
        {"k": "cap", "x": 500, "y": 600, "t": "Earth's magnetic field flips", "in": .2},
        {"k": "label", "x": 500, "y": 1080, "t": "the Matuyama–Brunhes reversal · c. 773,000 years ago", "st": "small", "c": "#b9aa97", "in": 1.3}]}
    tl, ax = timeline(-900000, 0, [(-900000, "900,000 years ago"), (-450000, "450,000"), (0, "today")], "Two dawns in Morocco")
    tl["els"] += event(ax, -773000, "Casablanca jaws", row=1, c=SCAN, i=.3) + event(ax, -315000, "Jebel Irhoud", row=2, c=GOLD, i=.7)
    s5 = tl
    s6 = like(s0, cam=[1.1, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:JEBEL IRHOUD · MOROCCO][sfx:boom][act:awe, measured]The oldest known fossils of our own species weren't found in East ^Africa.",
                      "[d:tension][cam:1.12|0|0][act:the reveal, a small smile][tune:fall]They came from a mine in ^Morocco."], cut=False),
        B("world", 1, ["[d:calm][k:THE MINE][act:storytelling]In {1961|nineteen sixty-one}, miners at Jebel ^Irhoud found a ^skull. [act:plain, building]From {2004|two thousand four}, a team led by Jean-Jacques Hublin found ^more: at least five ^people."]),
        B("collision", 2, ["[d:build][k:THE DATE][act:the reveal, strong]Burnt flints from the same layer gave about three hundred and fifteen ^thousand years. [act:context, wonder]More than a hundred thousand years older than the earlier record@noun, in ^Ethiopia."]),
        B("cost", 0, ["[d:build][k:THE FACE][act:describing, intrigued]The faces look ^modern. [act:the twist, precise]The braincases are long and ^archaic. [act:the idea, clear]Our lineage, it seems, got its face ^first, and its round head ^later."]),
        B("reversal", 3, ["[d:reveal][k:THE SECOND DAWN][act:the new find, excited but measured]Then, in {2026|twenty twenty-six}, jaws and teeth from a quarry in ^Casablanca: about seven hundred and seventy-three ^thousand years old.",
                          "[d:build][go:4|0][act:precise, delighted]Dated by a ^flip of Earth's magnetic field, and placed near the ^root of our lineage."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it][tune:rise]North Africa, part of our species' story from the ^start? [act:the verdict, confident][tune:fall]*Strong ^evidence*. [act:fair]Whether Irhoud counts as fully Homo ^sapiens is still debated.",
                     "[d:tension][p:0.93][act:the big picture, warm]Not one ^cradle. [act:the last word, quiet wonder][tune:fall]A whole ^continent."]),
    ]
    return EP("jebel-irhoud", "15.08", "Morocco's Two Dawns", "jebel-irhoud", "strong", "Did our species emerge across Africa, Morocco included, far earlier than once thought?", "The oldest *Homo sapiens*?", beats, shots,
              "Hublin et al. 2017 (doi:10.1038/nature22336) · Richter et al. 2017 (doi:10.1038/nature22335) · Hublin et al. 2026 (doi:10.1038/s41586-025-09914-y)",
              "The oldest known fossils of our species came from a Moroccan mine, about 315,000 years old. Then a Casablanca quarry gave jaws near the root of our lineage, dated by a flip of Earth's magnetic field.",
              ["#Morocco", "#HumanOrigins", "#HomoSapiens", "#Paleoanthropology", "#CarthageAndBefore"])


def irhoud_m():
    """Morocco's two dawns as one continuous take (see mural.py): a burnt flint's clock filling like a bucket in the rain, 315,000 years
    against the earlier Ethiopian record, a face first and a round head later, a jaw more than twice as old, rock layers that froze a
    compass flip, and a whole continent."""
    from mural import remix
    from illus import arrow, line, glow, label, dot, box, oval, ring, ellipse, scatter, AMBER, BLUE, GREEN, BONE, LILAC, RED as RED_
    ep = irhoud()
    # 2 · burnt flint: the clock resets in the fire, then fills like a bucket in the rain; 315,000 years, and the earlier record
    rain = [dot(x, y, 4, "#9fd0ff", round(3.9 + .04 * k, 2)) for k, (x, y) in enumerate(scatter(28, 600, 760, 360, 480, 4))]
    flint = {"base": "dark", "cam": [1, 500, 900], "els": [
        {"k": "poly", "p": [[230, 640], [300, 520], [370, 560], [390, 640]], "fill": "#9aa0a8", "c": "#dfe3e8", "w": 2, "in": .4, "fx": "pop"},
        glow(310, 640, 150, 1.2, .8, "red"), glow(310, 650, 90, 1.6, .7, "red"), label(310, 720, "burnt flint", 1.4, "#cbbca8", 30),
        {"k": "poly", "p": [[600, 520], [760, 520], [740, 700], [620, 700]], "fill": "none", "c": BONE, "w": 3, "in": 2.4, "fx": "draw", "dur": .6},
        label(680, 750, "its clock: 0", 2.6, BONE, 30)] + rain + [
        {"k": "poly", "p": [[606, 580], [754, 580], [740, 700], [620, 700]], "fill": "rgba(63,134,176,.7)", "c": "none", "w": 0, "in": 4.4, "fx": "fill", "dur": 1.6},
        label(500, 850, "c. 315,000 years", 6.8, GOLD, 42, st="serif"),
        box(120, 1000, 760, 40, GOLD, r=8, at=7.6, fx="fill", dur=.9), label(130, 980, "Jebel Irhoud", 7.6, GOLD, 30, "start"), label(880, 980, "today", 7.6, "#cbbca8", 28, "end"),
        box(410, 1110, 470, 40, BLUE, r=8, at=8.3, fx="fill", dur=.7), label(420, 1090, "Ethiopia", 8.3, BLUE, 30, "start"),
        arrow([[120, 1200], [404, 1200]], 8.9, AMBER, 3, "known", .6, False), label(262, 1250, "> 100,000 years", 9.2, AMBER, 30)]}
    # 0, again · a modern face; a long braincase, where ours is round
    vault = {"k": "line", "p": ellipse(545, 840, 205, 215, 24, 180, 340), "c": GREEN, "w": 3, "style": "claimed", "curve": True, "fx": "draw", "dur": 1.0, "in": 3.2}
    face = [glow(330, 860, 140, .8, .5), vault, label(720, 590, "later: round", 3.8, GREEN, 30)]
    # 3 · the Casablanca jaw, and its age against Irhoud's: more than twice as old
    jaw = [[300, 560], [330, 640], [420, 680], [600, 680], [690, 650], [700, 540], [670, 540], [650, 610], [440, 615], [370, 590], [345, 540]]
    casa = {"base": "dark", "cam": [1, 500, 900], "els": [
        {"k": "poly", "p": jaw, "fill": "#e8dcc6", "c": "#fff6e6", "w": 2, "curve": True, "in": .4, "fx": "pop"}]
        + [box(450 + 34 * k, 588, 24, 30, "#efe6d2", "#b8a888", 1.2, 8, round(.8 + .08 * k, 2), fx="pop") for k in range(6)]
        + [label(500, 760, "jaws and teeth · Casablanca", 1.2, BLUE, 30),
           box(120, 960, 760, 40, BLUE, r=8, at=2.8, fx="fill", dur=1.0), label(130, 940, "c. 773,000 years", 3.2, BLUE, 30, "start"),
           box(570, 1080, 310, 40, GOLD, r=8, at=4.0, fx="fill", dur=.6), label(560, 1108, "c. 315,000", 4.2, GOLD, 28, "end"),
           box(258, 1150, 310, 40, "none", GOLD, 2.5, 8, 5.6, style="inferred", fx="draw", dur=.5), box(570, 1150, 310, 40, "none", GOLD, 2.5, 8, 5.4, style="inferred", fx="draw", dur=.5),
           label(260, 1230, "twice Irhoud", 6.2, GOLD, 28, "start"), label(880, 1230, "today", 2.9, "#cbbca8", 28, "end")]}
    # 4 · the compass flip, frozen in rock: arrows point one way in the older layers, the other way in the younger; the jaws lie at the flip
    col = [box(560, 420 + 140 * k, 300, 140, ("#7a6248", "#8f7a5c", "#6f5a44", "#a08b6a", "#7a6248", "#8f7a5c")[k], r=0, at=round(1.8 + .15 * (5 - k), 2), fx="fill", dur=.4) for k in range(6)]
    arrows = []
    for k in range(6):
        y = 490 + 140 * k
        up = k < 3
        for j in range(3):
            x = 620 + 90 * j
            arrows.append(arrow([[x, y + 34], [x, y - 34]] if up else [[x, y - 34], [x, y + 34]], round(2.4 + .25 * (5 - k) + .05 * j, 2), BLUE if up else RED_, 3, "known", .3, False))
    flip = {"base": "dark", "cam": [1, 500, 900], "els": [
        ring(270, 560, 130, .3, "#8c7152", 3), arrow([[270, 610], [270, 470]], .6, BLUE, 6, "known", .4, False), label(270, 400, "N", .7, BLUE, 34),
        arrow([[300, 470], [300, 640]], 1.3, RED_, 6, "known", .4, False), label(300, 710, "flipped", 1.4, RED_, 30)] + col + arrows + [
        line([[540, 840], [880, 840]], 3.9, GOLD, 4, "inferred", .5), label(530, 848, "c. 773,000 years", 4.0, GOLD, 30, "end"),
        glow(710, 840, 110, 4.3, .55), label(710, 1320, "rock layers", 1.9, "#cbbca8", 28),
        line([[270, 1360], [270, 1150]], 4.5, BONE, 4), line([[270, 1150], [180, 980]], 4.7, BONE, 3), line([[270, 1150], [370, 1000]], 4.7, BONE, 3), line([[370, 1000], [330, 900]], 4.9, BONE, 2), line([[370, 1000], [420, 910]], 4.9, BONE, 2),
        dot(270, 1240, 14, GOLD, 5.2), glow(270, 1240, 80, 5.2, .6), label(270, 860, "our lineage", 5.0, BONE, 28)]}
    # 6 · not one cradle: the whole continent
    v = View(-20, 52, -36, 38, (60, 330, 880, 1050))
    afr = mapshot(v, pins=[("Morocco", -7.9, 32.6, {"c": GOLD, "in": .4}), ("Ethiopia", 39, 8.5, {"c": SCAN, "a": "end", "lx": -18, "in": .9})], cam=[1, 500, 860])
    xm, ym = v.p(-7.9, 32.6); xe, ye = v.p(39, 8.5)
    afr["els"] += [glow(xm, ym, 120, .6, .7), glow(xe, ye, 120, 1.1, .6)]
    whole = [glow(v.p(20, 3)[0], v.p(20, 3)[1], 480, .3, .5)]
    return remix(ep, scenes={2: flint, 3: casa, 4: flip, 6: afr}, alias={5: 1}, beat_adds={3: (face, None)}, line_adds={(5, 1): (whole, None)})


# ---------------------------------------------------------------- 15.09 The ledger
def _ledger_text():
    v = View(-12, 24, 28, 44, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("Carthage", 10.32, 36.85, {"c": GOLD}), ("Dougga", 9.22, 36.42, {"a": "end", "lx": -18}), ("Gafsa · El Guettar", 8.8, 34.4, {"a": "end", "lx": -18, "ly": 30}),
                          ("Kerkouane", 11.1, 36.95, {}), ("Chott el Djerid", 8.43, 33.7, {"a": "end", "lx": -18, "ly": 34}), ("Jebel Irhoud", -8.87, 31.86, {"c": SCAN})], cam=[1, 500, 860])
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established · strong", "#8fd9b0", ["our species in Morocco, 315,000 years ago", "the sounds of the Libyco-Berber script", "Kerkouane, left and never rebuilt"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible · mixed", "#e8b87a", ["Stone Age sea contact with Sicily", "sacrifice at the tophet", "Lake Tritonis in the chotts"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["El Guettar, the oldest shrine"], size=28)}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["Rome salting Carthage's earth"])}
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:CARTHAGE AND BEFORE][sfx:boom][act:warm, opening the book]Eight cases from Tunisia and the ^Maghreb. [act:inviting, a small smile]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, ticking them off][tune:level]Our species was in ^Morocco some three hundred thousand years ago. [act:plain, sure][tune:level]The sounds of the Libyco-Berber script are ^read@past. [act:the last one, warm][tune:fall]And Kerkouane was left, and never ^rebuilt."]),
        B("collision", 2, ["[d:build][k:STILL WEIGHED][act:weighing each, even][tune:level]Stone Age sailors reaching ^Sicily: plausible. [act:measured, even][tune:level]Sacrifice at the ^tophet: a mixed record@noun. [act:light][tune:fall]And the lake of the ^Argonauts: real lakes, the wrong century."]),
        B("cost", 3, ["[d:build][k:AWAITING EVIDENCE][act:even, fair]The world's oldest ^shrine, at El Guettar. [act:practical]It needs a ^date. [act:hopeful, light][tune:fall]One modern date from the ^deposit could settle it."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:clear, a small smile]Rome salting ^Carthage. [act:dry]A story from {1930|nineteen thirty}. [act:amused, plain][tune:fall]No ancient writer mentions ^salt at all."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:warm, wise, even]Much of what we think we know about this coast came from its ^enemies, or from modern ^writers. [act:the lesson, simple][tune:fall]The ground tells its own ^story.",
                     "[d:tension][p:0.93][act:the motto, calm and warm]^Coherence is the measure. [act:quiet, the last word][tune:fall]Not ^final demonstration."]),
    ]
    return EP("maghreb-ledger", "15.09", "Carthage and Before · The Ledger", "", "mixed", "What held up, and what didn't, in Tunisia and the Maghreb.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 15",
              "The verdicts of Carthage and Before in one ledger: what is established about Tunisia and the Maghreb, what is still being weighed, and the myth that is ruled out.",
              ["#Tunisia", "#Maghreb", "#Carthage", "#CarthageAndBefore", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: the cabinet of the eight cases (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    iso_shot = lambda ep: next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
    iso_el = lambda sh: next((e for e in sh["els"] if e.get("k") == "iso"), None)
    def mdl(ep):
        sh = iso_shot(ep); e = iso_el(sh)
        return e if e else sh
    C = Cabinet([
        {"name": "Jebel Irhoud", "model": mdl(irhoud())},
        {"name": "Dougga", "model": mdl(dougga())},
        {"name": "Kerkouane", "model": mdl(kerkouane())},
        {"name": "Capsian foragers", "model": [{"k": "water", "x0": -190, "x1": 190, "y": -46, "h": 44, "op": .85},
                                               {"k": "boat", "x": -80, "y": -52, "w": 170},
                                               {"k": "person", "x": -40, "y": -62, "h": 34, "t": False, "color": "#e8d6b8"},
                                               {"k": "person", "x": 0, "y": -62, "h": 30, "t": False, "color": "#e8d6b8"},
                                               {"k": "line", "p": [[-150, -150], [150, -150]], "c": "#cfe6ff", "w": 1.4, "style": "claimed"},
                                               {"k": "circle", "x": 150, "y": -150, "r": 10, "fill": "#c9ad85", "c": "#c9ad85", "w": 1}]},
        {"name": "The tophet", "model": mdl(tophet())},
        {"name": "Lake Tritonis", "model": mdl(tritonis())},
        {"name": "El Guettar", "model": mdl(el_guettar())},
        {"name": "Carthage's salt", "model": mdl(salt())},
    ])
    C.build()
    IR, DO, KE, CP, TO, TR, EG, SA = range(8)
    s1 = C.step(C.cam_cell(IR), C.verdict(IR, "established", "c. 300,000 years ago", .4) + C.people(IR, 2, at=1.0))
    s2 = C.step(C.cam_cell(DO), C.verdict(DO, "established", "its sounds are read", .4))
    s3 = C.step(C.cam_cell(KE), C.verdict(KE, "established", "left c. 250 BCE, never rebuilt", .4))
    s4 = C.step(C.cam_cell(CP), C.verdict(CP, "plausible", "sailors to Sicily?", .4))
    s5 = C.step(C.cam_cell(TO), C.verdict(TO, "mixed", "a mixed record", .4))
    s6 = C.step(C.cam_cell(TR), C.verdict(TR, "mixed", "real lakes, the wrong century", .4))
    s7 = C.step(C.cam_cell(EG), C.verdict(EG, "awaiting", "the oldest shrine?", .4))
    s8 = C.step(C.cam_cell(EG), C.question(EG, dx=C.w * .26, dy=-160, at=.2, c=VCOL["awaiting"]) + C.note(EG, "one modern date could settle it", at=.8, c=VCOL["awaiting"]))
    s9 = C.step(C.cam_cell(SA), C.verdict(SA, "ruled", at=.2) + C.struck(SA, "Rome salted the fields", dy=-170, at=.5))
    s10 = C.step(C.cam_cell(SA), C.note(SA, "first told in 1930", at=.3, c=VCOL["ruled"]))
    s11 = C.step(C.cam_all())
    s12 = C.step(C.cam_all(), [e for i in range(8) for e in C.wash(i, "#e8b87a", at=.3 + .1 * i, op=.12)])
    s13 = C.step(C.cam_all(z=.64, sy=700))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.3" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5, (0, 2): "%d|1.1" % s6}),
        3: (s7, {(0, 1): "%d|.5" % s8}),
        4: (s9, {(0, 1): "%d|.4" % s10}),
        5: (s11, {(0, 1): "%d|.8" % s12, (1, 0): "%d|4" % s13}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def el_guettar_m():
    """El Guettar as one continuous take across a wall of scenes (see mural.py): the find, the idea and the catch are drawn, not written."""
    from mural import remix
    from illus import balls, tri, tooth, person, arrow, line, glow, oval, label, question, dot, box, SEA as SEA_, AMBER, BLUE, LILAC, GREEN
    ep = el_guettar()
    # 2 · the find: Gruet's trench through the old spring deposits, the cone inside, flints and horse teeth around it
    find = {"base": "section", "ground": 640, "tod": "dusk", "layers": [{"d": 0, "c": "#8a6a48", "t": ""}, {"d": 250, "c": "#6f5a44", "t": ""}, {"d": 700, "c": "#4a3a2c", "t": ""}],
            "cam": [1, 500, 880], "els": [
                person(300, 640, 120, .2), line([[330, 560], [372, 520]], .4, "#8a5d33", 6, draw=False),
                {"k": "rect", "x": 400, "y": 640, "w": 330, "h": 450, "r": 4, "fill": "rgba(18,13,10,.35)", "c": "#f5ecdc", "sw": 2, "style": "inferred", "in": .5, "fx": "draw", "dur": 1.0}]
            + balls(565, 1060, rows=9, r=13, at=1.2, step=.025)
            + [tri(x, y, 12, r * 40, at=4.6 + .12 * k) for k, (x, y, r) in enumerate([(430, 1075, 0), (700, 1080, 1), (455, 1030, 2), (690, 1020, 3), (620, 1085, 4)])]
            + [tooth(x, y, 30, 5.6 + .15 * k) for k, (x, y) in enumerate([(470, 1070), (660, 1060), (520, 1085)])]
            + [glow(565, 1040, 160, 5.8, .35)]
            + [line([[400, 1150 + 14 * k], [440, 1144 + 14 * k], [480, 1152 + 14 * k], [520, 1146 + 14 * k], [560, 1150 + 14 * k], [600, 1145 + 14 * k], [640, 1151 + 14 * k], [680, 1146 + 14 * k], [730, 1150 + 14 * k]],
                    6.4 + .2 * k, BLUE, 3, "inferred", 1.2, True) for k in range(2)]}
    # 3 · the idea: people carry stones to the spring, choose the teeth, set the pile at the water's edge
    idea = {"base": "sky", "tod": "dusk", "ground": 1150, "sun": [820, 900, 26], "cam": [1, 500, 900], "els": [
                oval(600, 1215, 190, 44, SEA_, "#9fd0ff", 2, .9, .4), glow(600, 1210, 200, .6, .35, "lamp")]
            + [line([[430 + 16 * k, 1190], [424 + 16 * k, 1120 - 12 * (k % 3)]], .7, "#7fa35a", 3, draw=False) for k in range(4)]
            + [person(120 + 90 * k, 1190, 100, 3.3 + .25 * k) for k in range(3)]
            + [dot(140 + 90 * k, 1128, 9, "#cbbca8", 3.5 + .25 * k) for k in range(3)]
            + [arrow([[60, 1270], [260, 1262], [400, 1232]], 3.4, AMBER, 3, "claimed", 1.2)]
            + [tooth(x, 1250, 34, 5.2 + .2 * k) for k, x in enumerate((650, 690, 730))] + [glow(690, 1250, 90, 5.2, .6)]
            + balls(790, 1188, rows=6, r=10, at=6.6, step=.035) + [glow(790, 1150, 140, 7.4, .45)]}
    # 5 · the catch: the same balls could be tools, or a cache, as well as an offering
    catch = {"base": "dark", "cam": [1, 500, 860], "els":
             balls(800, 960, rows=5, r=11, at=.2, step=.02) + [glow(800, 930, 130, .6, .5), label(800, 1060, "an offering?", .8, AMBER, 32)]
             + [dot(185, 900, 22, "#cbbca8", 1.6), tri(250, 955, 30, 20, "#9aa0a8", 1.9), line([[140, 860], [165, 880]], 2.0, "#f5ecdc", 3), line([[130, 890], [158, 896]], 2.05, "#f5ecdc", 3),
                label(200, 1060, "a tool?", 2.1, BLUE, 32)]
             + [{"k": "poly", "p": [[400, 900], [600, 900], [575, 975], [425, 975]], "fill": "#2a1d12", "c": "#8a6a48", "w": 2, "in": 3.0, "fx": "rise"}]
             + [dot(450 + 25 * k, 950 - (k % 2) * 16, 11, "#cbbca8", 3.2 + .05 * k) for k in range(7)] + [label(500, 1060, "a cache?", 3.4, LILAC, 32)]}
    b = ep["beats"]
    b[1]["lines"][0] = b[1]["lines"][0].replace("[act:precise]With the balls", "[go:2][act:precise]With the balls")
    return remix(ep, scenes={2: find, 3: idea, 5: catch}, alias={6: 0}, cams={0: [1.3, 500, 1010], 5: [1.15, 500, 970], 6: [1.6, 500, 1030]})


def capsian_m():
    """The Capsians as one continuous take (see mural.py): the mound grows, a cubic metre fills with shells, one forager's ancestry lights up."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box, oval, question, scatter, AMBER, BLUE, BONE
    import random as _r
    import copy
    ep = capsian()
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] = [e for e in s0["els"] if e.get("k") != "label"]
    shells = [dot(x, y, 5, "#efe6d2", .8 + .01 * k, op=.9) for k, (x, y) in enumerate(scatter(40, 120, 900, 720, 820, 3) + scatter(30, 120, 900, 940, 1020, 4))]
    s0["els"] += shells + [glow(380, 880, 70, 1.2, .7, "fire"), glow(700, 880, 60, 1.4, .6, "fire")] + \
        [person(430 + 40 * k, 600, 70, .4 + .15 * k) for k in range(3)] + [glow(520, 590, 50, .6, .8, "fire")] + \
        [glow(470, 560, 90, 3.2, .8), arrow([[470, 540], [640, 420], [940, 380]], 3.4, BLUE, 3, "claimed", 1.2)]
    # the mound grows, layer on layer, to three metres; then one cubic metre fills with shells
    bands = [(1250, 1170, "#5a4632"), (1170, 1090, "#b9ab94"), (1090, 1020, "#6f5a44"), (1020, 950, "#a8977c"), (950, 900, "#7a6248")]
    mound = []
    for k, (y0, y1, c) in enumerate(bands):
        w0 = 380 - (1250 - y0) * .55; w1 = 380 - (1250 - y1) * .55
        mound.append({"k": "poly", "p": [[500 - w0, y0], [500 + w0, y0], [500 + w1, y1], [500 - w1, y1]], "fill": c, "c": "none", "w": 0, "in": .3 + .7 * k, "dur": .9, "fx": "fill"})
    mound += [arrow([[880, 1250], [880, 900]], 3.4, AMBER, 3, "known", 1.0, False), arrow([[880, 900], [880, 1250]], 3.4, AMBER, 3, "known", 1.0, False),
              label(915, 1085, "3 m", 3.8, AMBER, 36, "start")]
    cube = [box(420, 1030, 150, 150, "rgba(18,13,10,.55)", "#f5ecdc", 2.5, 2, 6.2, fx="pop"),
            line([[420, 1030], [470, 990], [620, 990], [570, 1030]], 6.4, BONE, 2.5), line([[620, 990], [620, 1140], [570, 1180]], 6.5, BONE, 2.5)]
    r = _r.Random(7)
    cube += [dot(round(r.uniform(428, 562), 1), round(r.uniform(1038, 1172), 1), 3.2, "#efe6d2", round(6.8 + .012 * k, 3)) for k in range(150)]
    cube += [label(495, 1230, "1 m³", 7.2, BONE, 34)]
    find = {"base": "dark", "floor": 1250, "cam": [1.05, 500, 1000], "els": [line([[60, 1250], [940, 1250]], 0, "#8a6a48", 3, draw=False)] + mound + cube}
    # one forager, and his ancestry: 94 local squares, 6 that came from across the sea
    grid = [box(560 + 29 * (k % 10), 800 + 29 * (k // 10), 24, 24, AMBER, r=4, at=2.2 + .006 * k, op=.55) for k in range(100)]
    euro = [box(560 + 29 * (k % 10), 800 + 29 * (k // 10), 24, 24, BLUE, r=4, at=5.2 + .15 * j, fx="pop") for j, k in enumerate((93, 94, 95, 96, 97, 98))]
    dna = {"base": "dark", "floor": 1220, "cam": [1, 500, 900], "els": [person(300, 1220, 330, .3), glow(300, 1060, 200, .4, .5)] +
           [line([[430 + 9 * k, round(1060 + 16 * math.sin(k * .6 + ph), 1)] for k in range(14)], 1.4, BLUE, 3, dur=1.0) for ph in (0, math.pi)] + grid + euro +
           [arrow([[980, 380], [880, 560], [780, 790]], 6.6, BLUE, 3, "claimed", 1.2), label(930, 350, "Sicily", 7.0, BLUE, 32, "end")]}
    # the meal: a tall stack of big-game bone, a small heap of snails
    bone = lambda x, y, at: [line([[x - 40, y], [x + 40, y]], at, "#efe6d2", 12, draw=False)] + [dot(x + dx, y + dy, 9, "#efe6d2", at, None) for dx in (-44, 44) for dy in (-7, 7)]
    meal = {"base": "dark", "floor": 1200, "cam": [1, 500, 900], "els": [line([[140, 1200], [860, 1200]], 0, "#8a6a48", 3, draw=False),
            box(560, 1110, 170, 90, "#b9ab94", r=6, at=.6, fx="fill", dur=1.0)] + [dot(580 + 24 * k, 1090, 9, "#efe6d2", 1.0 + .08 * k) for k in range(6)] +
           [label(645, 1260, "snails", 1.2, BONE, 32), box(270, 760, 170, 440, AMBER, r=6, at=2.6, fx="fill", dur=1.4)] + bone(355, 720, 3.6) + [label(355, 1260, "big game", 3.0, AMBER, 32)]}
    return remix(ep, scenes={0: s0, 2: find, 3: dna, 5: meal}, alias={4: 3, 6: 1}, cams={6: [1.12, 500, 880]})


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/maghreb-ledger.json)."""
    import recap
    return recap.recap(ledger, "maghreb-ledger", None)


def EPISODES():
    return [tophet_m(), salt_m(), capsian_m(), dougga_m(), el_guettar_m(), tritonis_m(), kerkouane_m(), irhoud_m(), ledger_recap()]
