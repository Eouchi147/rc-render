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
    return [flood(), yu(), gilgamesh(), ark(), babel(), iram(), thamud(), sodom(), ledger_recap()]
