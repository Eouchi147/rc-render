"""File 10 · Scripture and Stone II. Kings, prophets and signs in the sky: where the texts meet the ground and the sky.
Only physical and historical claims are weighed. What faith holds is never rated, and nothing here is set against scripture."""
import math
from films import like, View, Axis
from scenes import timeline as _timeline, event, stat, quote, papyrus, silhouette, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso, lab, aim
from f09 import B, L_, tablet

SERIES = "Scripture and Stone"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def stele(x=230, y=380, w=540, h=880, rows=12, kind="hieratic"):
    """A standing stone with lines of script."""
    return {"base": "paper", "kind": "stone", "x": x, "y": y, "w": w, "h": h, "holes": [], "cam": [1, 500, 860],
            "els": [{"k": "glyphs", "x": x + 50, "y": y + 70, "w": w - 100, "h": h - 160, "rows": rows, "cols": 9, "kind": kind, "in": .2}]}


# ---------------------------------------------------------------- 10.01 The Exodus
def exodus():
    v = View(30, 36.5, 27.6, 32.2, (40, 330, 920, 900))
    base = mapshot(v, extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s0 = like(base, cam=[1.05, 500, 860], add=[{"k": "pin", "x": v.p(31.83, 30.8)[0], "y": v.p(31.83, 30.8)[1], "t": "Pi-Ramesses · Qantir", "c": GOLD, "in": .3},
                                               {"k": "pin", "x": v.p(32.35, 30.35)[0], "y": v.p(32.35, 30.35)[1], "t": "the Bitter Lakes", "c": SCAN, "in": .6},
                                               {"k": "pin", "x": v.p(34.42, 30.65)[0], "y": v.p(34.42, 30.65)[1], "t": "Kadesh Barnea", "c": BONE, "in": .9},
                                               {"k": "label", "x": v.p(33.6, 29.2)[0], "y": v.p(33.6, 29.2)[1], "t": "Sinai", "st": "ital", "c": "#c9ad85", "in": .4},
                                               {"k": "cap", "x": 500, "y": 380, "t": "forty years in Sinai · where are the camps?", "in": 1.2}])
    s1 = stele(rows=14, kind="hieroglyph")
    s1["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "the Merneptah stele · c. 1208 BCE", "in": .5},
                  {"k": "label", "x": 500, "y": 1320, "t": "'Israel' · written with the sign for a people, not a city", "st": "small", "in": 1.2}]
    # the sea that stepped back: a shallow lagoon, an east wind, the water pushed off a bar
    lagoon = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 110, "prof": [[-80, 0], [-80, 8], [-55, 8], [-30, 2], [0, 4], [30, 2], [55, 8], [80, 8], [80, 0]], "c": "#7a6248", "edge": "rgba(255,236,206,.4)"},
              {"t": "flat", "pts": [[-56, -54], [-30, -54], [-30, 54], [-56, 54]], "y": 6.1, "c": "#3f86b0", "op": .78, "ground": False, "over": 2},
              {"t": "flat", "pts": [[30, -54], [56, -54], [56, 54], [30, 54]], "y": 6.1, "c": "#3f86b0", "op": .78, "ground": False, "over": 2},
              {"t": "line", "p": [[70, 14, -40], [10, 14, -40]], "c": "#cfe6ff", "w": 3, "op": .9, "arrow": True},
              L_(40, 15, "east wind · 12 hours", "#cfe6ff", z=-40, dy=-18), L_(0, 5, "the bar, exposed for hours", GOLD, z=0, dy=-16), L_(-43, 7, "the lagoon, pushed back", "#cfe6ff", z=30, dy=36)]
    s2 = iso(lagoon, cam=[1, 500, 900], s=4.4, x=500, y=980, az=-30, spin=1.4, el=.5, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "wind setdown · a model, not a photograph", "in": .2},
                  {"k": "label", "x": 500, "y": 1300, "t": "Drews & Han 2010: a 100 km/h east wind could bare a land bridge for about four hours", "st": "small", "in": 1.0}]
    s3 = stat("600,000", "men on foot", "the headcount in Exodus 12:37; with families, about two million people crossing Sinai", "Exodus 12:37; Numbers 1:46")
    tl, ax = timeline(-1650, -1100, [(-1600, "1600 BCE"), (-1400, "1400"), (-1200, "1200")], "The candidates, and the one fixed point", y=980)
    tl["els"] += event(ax, -1550, "the Hyksos driven out", row=0, c=AMBER, i=.3) + event(ax, -1446, "the biblical date", row=1, c=SCAN, i=.6, sub="1 Kings 6:1, counted back") + \
                 event(ax, -1250, "Ramesses II", row=2, c=GOLD, i=.9) + event(ax, -1208, "'Israel' in Canaan", row=0, c=BONE, i=1.2, sub="the Merneptah stele")
    s4 = tl
    s5 = quote("Israel is laid waste; its seed is no more.", "the Merneptah stele · c. 1208 BCE", y=720, size=44)
    s6 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE EXODUS][sfx:boom][act:respectful, setting the scene]Two ^scriptures remember it. [act:evoking it, slowly, with weight]A ^tyrant, a parted ^sea, a drowned ^army.",
                      "[d:tension][cam:1.12|0|0][act:plain, even]Egypt kept its ^stones. [act:a quiet contrast]It did not keep the ^story. [act:a small pause, thinking][tune:level]So... [act:the real puzzle, curious][tune:fall]where are the ^camps?"], cut=False),
        B("world", 1, ["[d:calm][k:WHAT IS SOLID][act:grounded, warm, plain]Here is the ^ground. [act:confident fact, steady]West Semitic people lived and worked in the Nile ^Delta for a ^thousand years. [act:matter of fact]Ramesses the Second built his ^capital there.",
                       "[d:build][act:the key fact, leaning in]And a ^stone from {1208|twelve oh eight} BCE names ^*Israel*. [act:precise, adding weight][tune:level]As a ^people. [act:landing it, quiet][tune:fall]In ^Canaan."]),
        B("collision", 3, ["[d:build][k:THE HEADCOUNT][act:turning a page, brisk]Now the ^number@count. [act:reading from the text, careful]Exodus counts six hundred ^thousand men, plus ^families. [act:the scale sinks in, slower]Call it two ^*million*.",
                           "[d:tension][go:4|0][act:reasoning it through, even]Two million people, forty years in Sinai, should leave ^something. [gap:0.45][act:quiet, plain fact][tune:fall]Surveys@noun have found ^nothing from that century."]),
        B("cost", 2, ["[d:wonder][k:THE SEA][act:wonder, a gentle turn]The sea, though, has a ^physics. [sfx:shimmer][act:explaining, vivid, unhurried]A strong ^east wind@air, blowing for twelve hours, can push the water off a shallow lagoon and bare a land ^bridge for hours.",
                      "[d:aside][act:lighter, a gentle correction][tune:fallrise]Not the ^Red Sea we picture. [act:quiet, descriptive]A ^reedy lake that ^silted up long ago."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:leaning in, fair-minded]And absence is ^weak here. [act:explaining, steady]The ^wet Delta kept almost no ^papyrus. [act:plain, reasonable]Nomads leave tent rings a survey@noun can ^miss.",
                          "[d:build][sfx:hit][act:building, thoughtful]A ^smaller departure, a few families carrying a real memory, would leave exactly what we have: ^nothing... [act:warm, quiet, with respect][tune:fall]and a ^story that would not ^die."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]The ^headcount? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:turning to the next, open][tune:rise]A ^smaller exodus? [act:fair and balanced][tune:fall]^Plausible, and ^unproven.",
                     "[d:tension][p:0.93][act:respectful, measured, sincere]The ^events at the heart of both scriptures are not what we ^rate. [act:quiet, certain, gentle][tune:fall]The ^ground is."]),
    ]
    return EP("exodus", "10.01", "Moses, Pharaoh and the Sea That Stepped Back", "exodus", "unsupported", "Did an exodus from Egypt happen on the scale the text gives?", "So... where are the *camps*?", beats, shots,
              "Merneptah stele, Cairo JE 31408 · Drews & Han 2010, PLoS ONE · Bietak 1996 · Hoffmeier 1997, 2005 · Finkelstein & Silberman 2001",
              "Two scriptures, a drowned army and an empty desert: what the Delta, the Sinai surveys and a wind model can and cannot say about the Exodus.",
              ["#Exodus", "#Egypt", "#Archaeology", "#History", "#Sinai"])


# ---------------------------------------------------------------- 10.02 Jericho
def jericho():
    mound = [[80 * math.cos(math.radians(a)) * (1 + .12 * math.sin(3 * a * math.pi / 180)), 46 * math.sin(math.radians(a))] for a in range(0, 360, 15)]
    tell = [{"t": "prism", "pts": mound, "y": 0, "h": 8, "c": "#6f5840", "edge": "rgba(255,236,206,.4)"},
            {"t": "prism", "pts": [[q[0] * .82, q[1] * .8] for q in mound], "y": 8, "h": 7, "c": "#7a6248", "edge": "rgba(255,236,206,.4)"},
            {"t": "prism", "pts": [[q[0] * .62, q[1] * .58] for q in mound], "y": 15, "h": 6, "c": "#87704f", "edge": "rgba(255,236,206,.4)"},
            {"t": "cyl", "x": -18, "z": 8, "y": 21, "r": 6, "h": 14, "c": "#c9ad85", "n": 16, "edge": "rgba(0,0,0,.25)"},
            {"t": "line", "p": [[-48, 21.2, -20], [-52, 21.2, 20], [-40, 21.2, 30]], "c": "#f2dcb4", "w": 3, "op": .9},
            {"t": "person", "x": 40, "y": 0, "z": 52, "h": 1.7},
            L_(-18, 35, "the stone tower · c. 8000 BCE · enlarged", GOLD, z=8, dy=-14), L_(0, 0, "Tell es-Sultan · the mound of Jericho", "#cfe6ff", z=56, dy=40)]
    s0 = iso(tell, cam=[1, 500, 900], s=4.6, x=500, y=1000, az=-24, spin=1.5, el=.5, table=None)
    v = View(34.8, 35.9, 31.4, 32.25, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Jericho · Tell es-Sultan", 35.444, 31.871, {"c": GOLD}), ("Jerusalem", 35.23, 31.78, {"a": "end", "lx": -18}), ("Gibeon", 35.185, 31.848, {"a": "end", "lx": -18, "ly": -22})],
                 extra=[{"k": "poly", "p": [v.p(*q) for q in [(35.55, 31.78), (35.62, 31.6), (35.58, 31.4), (35.5, 31.3), (35.45, 31.48), (35.45, 31.7), (35.5, 31.78)]],
                         "fill": "rgba(63,134,176,.55)", "c": SCAN, "w": 1.4, "curve": True}, {"k": "label", "x": v.p(35.75, 31.5)[0], "y": v.p(35.75, 31.5)[1], "t": "Dead Sea", "st": "small", "c": "#cfe6ff"},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(20), "t": "20 km"}])
    sec = {"base": "section", "tod": "night", "ground": 640, "lx": 130,
           "layers": [{"d": 0, "c": "#5a4a3a", "t": "eroded top · Late Bronze scraps"}, {"d": 90, "c": "#2a1a12", "t": "burnt city · c. 1550 BCE", "tex": "blocks", "to": .1},
                      {"d": 230, "c": "#6f5a43", "t": "Early Bronze walls"}, {"d": 420, "c": "#8a6d4d", "t": "the Neolithic tower · c. 8000 BCE"}],
           "cam": [1, 500, 900], "els": [{"k": "label", "x": 500, "y": 560, "t": "the mound, cut open · schematic", "c": AMBER, "in": .3},
                                         {"k": "label", "x": 500, "y": 1340, "t": "Kenyon's trenches, 1952 to 1958 · radiocarbon on grain, 1995", "st": "small", "in": 1.0}]}
    s2 = sec
    s3 = stat("22", "steps", "inside a stone tower built about 8000 BCE, five thousand years before the pyramids", "Kenyon 1957; Barkai & Liran 2008")
    tl, ax = timeline(-1700, -1100, [(-1700, "1700 BCE"), (-1500, "1500"), (-1300, "1300"), (-1100, "1100")], "When the walls fell", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-1617), "x1": ax.x(-1530), "y": 720, "h": 18, "c": RED, "t": "the fire · radiocarbon on grain", "in": .3}] + \
                 event(ax, -1400, "the biblical date", row=2, c=SCAN, i=.7, sub="Wood 1990: the pottery, re-read") + event(ax, -1208, "'Israel' in Canaan", row=1, c=BONE, i=1.0)
    s4 = tl
    s5 = quote("And the wall fell down flat.", "Joshua 6:20 · King James Version", y=760, size=46)
    s6 = like(s0, cam=[1.15, 500, 980])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:JERICHO][sfx:boom][act:wonder, setting the scene]A ^tower with twenty-two ^steps inside it. [act:letting the age land, slower]Built about eight ^thousand BCE.",
                      "[d:tension][cam:1.12|0|0][act:quiet awe]This mound is older than ^writing. [act:leaning in, a hook][tune:level]And its most famous ^walls... [act:the sting, quiet and dry][tune:fall]fell too ^early."], cut=False),
        B("world", 1, ["[d:calm][k:THE JORDAN VALLEY][act:storytelling, warm]Tell es-Sultan, beside a spring, is one of the ^oldest towns on Earth. [go:2|0][act:counting down the layers, vivid]Cut it open and the layers stack up: ^Neolithic, ^Bronze Age, and a burnt city with ^thick walls."]),
        B("collision", 3, ["[d:build][k:THE DATE][act:setting the terms, clear]Joshua's story needs those walls to fall around {1400|fourteen hundred} BCE. [go:4|0][act:the evidence, confident]Radiocarbon on grain from the burnt city says the {1600s|sixteen hundreds} or {1500s|fifteen hundreds}. [act:plain, pointed][tune:fall]At least a ^century early.",
                           "[d:tension][act:fair, giving the other side]Bryant Wood read@past the pottery ^differently and argued for {1400|fourteen hundred}. [act:calm, precise, a gentle point]The ^carbon does@verb ^not depend on pottery."]),
        B("cost", 2, ["[d:build][k:THE MISSING CENTURY][act:explaining, careful]For the centuries usually given to Joshua, Kenyon found ^scraps: a small ^building, some ^tombs. [act:plain, a little rueful]The ^top of the mound had ^eroded away. [d:aside][act:lighter, a small smile]Rain takes ^cities too."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][sfx:hit][act:the twist, measured]So there ^may have been a wall that fell. [act:precise, a fine distinction][tune:fall]Just not the ^one, or the ^century, the argument is about. [act:open-ended, curious]A later, smaller Jericho is ^poorly known, and most of the mound is ^undug."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Walls ^down in {1400|fourteen hundred} BCE? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the other side, steady][tune:rise]A walled city burned two centuries ^earlier? [act:firm, confident, one word][tune:highfall]^Established.",
                     "[d:tension][p:0.93][act:warm, reassuring][tune:fallrise]The story is not out of ^reach. [act:the last word, quiet][tune:fall]It is ^under the erosion."]),
    ]
    return EP("jericho", "10.02", "Jericho: The Walls That Fell Too Early", "jericho", "unsupported", "Did Jericho's walls fall when the Book of Joshua says they did?", "Its most famous walls fell *too early*.", beats, shots,
              "Kenyon 1957 · Bruins & van der Plicht 1995, Radiocarbon · Wood 1990, BAR · Bienkowski 1990 · Barkai & Liran 2008",
              "The oldest tower on Earth, a burnt Bronze Age city, and a date that sits a century before the story: what Jericho's mound can and cannot say.",
              ["#Jericho", "#Archaeology", "#Bible", "#History", "#Radiocarbon"])


# ---------------------------------------------------------------- 10.03 Joshua's long day
def joshua():
    s0 = {"base": "sky", "tod": "dusk", "ground": 1180, "sun": False, "cam": [1, 500, 880], "els": [
          {"k": "glow", "x": 500, "y": 760, "r": 260, "kind": "sun", "op": .9, "in": .1}, {"k": "circle", "x": 500, "y": 760, "r": 120, "fill": "#ffd98a", "c": "none", "w": 0, "in": .1},
          {"k": "circle", "x": 500, "y": 760, "r": 108, "fill": "#2a2233", "c": "none", "w": 0, "in": .8, "fx": "pop"},
          {"k": "cap", "x": 500, "y": 400, "t": "30 October 1207 BCE · late afternoon · over Gibeon", "in": .3},
          {"k": "label", "x": 500, "y": 1260, "t": "an annular eclipse: a ring of sun around the moon", "in": 1.2}]}
    v = View(34.6, 35.6, 31.5, 32.1, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Gibeon · el-Jib", 35.185, 31.848, {"c": GOLD}), ("Jerusalem", 35.23, 31.78, {"a": "start", "ly": 34}), ("Azekah", 34.93, 31.7, {"c": SCAN, "a": "end", "lx": -18}), ("the valley of Aijalon", 35.02, 31.85, {"a": "end", "lx": -18, "ly": -24})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(10), "t": "10 km"}])
    s2 = papyrus(rows=10, cols=8, kind="hieratic", hl={"x": 200, "y": 700, "w": 600, "h": 70})
    s2["els"] += [{"k": "cap", "x": 500, "y": 300, "t": "the Book of Jashar · quoted, and lost", "in": .3},
                  {"k": "label", "x": 500, "y": 1260, "t": "Joshua 10:12–13 quotes two lines of an older poem nobody has read since antiquity", "st": "small", "in": 1.0}]
    s3 = stat("1", "annular eclipse", "visible from Gibeon in 450 years, between 1500 and 1050 BCE: the afternoon of 30 October 1207 BCE", "Humphreys & Waddington 2017")
    s4 = quote("Sun, stand thou still upon Gibeon; and thou, Moon, in the valley of Ajalon.", "Joshua 10:12 · King James Version", y=700, size=42)
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 560, "t": "one Hebrew verb · two readings", "in": .2},
          {"k": "title", "x": 500, "y": 720, "t": "dom", "st": "serif", "size": 96, "in": .3},
          {"k": "label", "x": 300, "y": 900, "t": "stand still", "c": GOLD, "size": 30, "in": .6}, {"k": "label", "x": 300, "y": 940, "t": "a day that would not end", "st": "small", "in": .7},
          {"k": "label", "x": 700, "y": 900, "t": "stop shining", "c": SCAN, "size": 30, "in": .9}, {"k": "label", "x": 700, "y": 940, "t": "a sun that went dark", "st": "small", "in": 1.0},
          {"k": "line", "p": [[500, 860], [500, 980]], "c": "#8c7152", "w": 1.5, "in": .5},
          {"k": "label", "x": 500, "y": 1120, "t": "the narrator adds: the sun 'hasted not to go down about a whole day'", "st": "small", "c": "#cbbca8", "in": 1.3}]}
    s6 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:GIBEON · 1207 BCE][sfx:boom][act:wonder, painting the sky]A ring of ^fire in the ^afternoon sky. [act:the rarity, slower]The ^only one over this valley in four hundred and ^fifty years.",
                      "[d:tension][cam:1.12|0|0][act:curious, pulling us in][tune:rise]Did a ^poet see it... [act:softer, the real question][tune:rise]and did we keep his ^words?"], cut=False),
        B("world", 4, ["[d:calm][k:THE POEM][act:with care, reading the old lines]Joshua's book quotes two lines from an older book, now ^lost: sun, stand still at Gibeon; moon, in the valley of ^Aijalon.",
                       "[d:build][go:1|0][act:grounded, confident]The places are ^real. [act:naming them, one by one]^Gibeon, ^Aijalon, the road down from the ^hills."]),
        B("collision", 3, ["[d:build][k:THE ECLIPSE][act:storytelling, bright]In {2017|twenty seventeen}, two Cambridge and Oxford scientists ran the sky ^backwards. [sfx:shimmer][act:the result, slow and precise]One annular eclipse, over Gibeon, on the thirtieth of October, {1207|twelve oh seven} BCE.",
                           "[d:build][act:connecting the dots, thoughtful]A ^year after a stone in Egypt first names ^Israel in Canaan. [act:measured, quietly intrigued]The fit is ^unusual."]),
        B("cost", 5, ["[d:build][k:ONE WORD][act:intrigued, zooming in]It all hangs on a ^verb. [act:saying the word, carefully]^Dom. [act:weighing two readings][tune:rise]Stand ^still... [act:the alternative, curious][tune:fall]or stop ^shining? [d:tension][act:fair, the complication]And the narrator, right after the poem, says the sun did not ^hurry to set, for about a whole ^day. [act:plain, gentle, firm]An eclipse does@verb ^not do that."]),
        B("reversal", 2, ["[d:reveal][k:THE TWIST][act:clear, confident]So the ^astronomy is *solid*: the eclipse happened, ^there, ^then. [sfx:hit][act:the pivot, careful and fair]The ^link to the text is the ^open part. [act:plain facts, even][tune:level]The poem's own ^date is ^unknown. [act:quiet, a little wistful][tune:fall]Its ^source is ^lost."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]The ^eclipse? [act:firm, one word][tune:highfall]^Certain. [act:the harder part, careful][tune:rise]The ^poem remembering it? [act:even-handed, measured][tune:fall]An ^*open* question, argued in a ^peer-reviewed journal.",
                     "[d:tension][p:0.93][act:warm, a gentle smile, sincere]Which is ^more than most miracles get."]),
    ]
    return EP("joshua-sun", "10.03", "Joshua's Long Day: The Oldest Eclipse on Record?", "joshua-sun", "contested", "Did Joshua's poet see an annular eclipse?", "A ring of fire in the afternoon *sky*.", beats, shots,
              "Humphreys & Waddington 2017, Astronomy & Geophysics · Sawyer 1972 · Walton 1994 · Holladay 1968 · Merneptah stele",
              "An annular eclipse over Gibeon in 1207 BCE, two lines of a lost poem, and one Hebrew verb: the case that Joshua's long day is the oldest eclipse on record.",
              ["#Eclipse", "#Bible", "#Astronomy", "#History", "#Joshua"])


# ---------------------------------------------------------------- 10.04 Solomon's mines
def solomon():
    slag = [[60 * math.cos(math.radians(a)) * (1 + .15 * math.sin(2 * a * math.pi / 180)), 34 * math.sin(math.radians(a))] for a in range(0, 360, 20)]
    camp = [{"t": "prism", "pts": slag, "y": 0, "h": 6, "c": "#2a221c", "edge": "rgba(255,236,206,.3)"},
            {"t": "prism", "pts": [[q[0] * .7, q[1] * .7] for q in slag], "y": 6, "h": 5, "c": "#332a22", "edge": "rgba(255,236,206,.3)"},
            {"t": "prism", "pts": [[q[0] * .4, q[1] * .4] for q in slag], "y": 11, "h": 4, "c": "#3d332a", "edge": "rgba(255,236,206,.3)"}] + \
           [{"t": "cyl", "x": x, "z": z, "y": 15, "r": 1.6, "h": 2.2, "c": "#8c5a3a", "n": 10, "edge": "rgba(0,0,0,.3)"} for x, z in ((-8, -4), (4, 6), (10, -6), (-2, 9))] + \
           [{"t": "person", "x": 70, "y": 0, "z": 30, "h": 1.7}, L_(0, 17, "furnaces", GOLD, z=0, dy=-14), L_(0, 0, "Khirbat en-Nahas · slag more than 6 m deep", "#cfe6ff", z=44, dy=40)]
    s0 = iso(camp, cam=[1, 500, 900], s=5.2, x=500, y=1000, az=-26, spin=1.4, el=.5, table={"r": 80, "rz": 60, "grid": 20, "strata": [{"h": 2, "c": "#a8845c"}, {"h": 8, "c": "#7d6045"}]})
    v = View(34.2, 36.2, 29.3, 32.2, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Faynan · Khirbat en-Nahas", 35.437, 30.681, {"c": GOLD}), ("Timna", 34.95, 29.78, {"c": GOLD, "a": "end", "lx": -18}), ("Jerusalem", 35.23, 31.78, {}), ("Beersheba", 34.79, 31.25, {"a": "end", "lx": -18})],
                 extra=[{"k": "label", "x": v.p(35.3, 30.2)[0], "y": v.p(35.3, 30.2)[1], "t": "the Arabah", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    sec = {"base": "section", "tod": "night", "ground": 640, "lx": 130,
           "layers": [{"d": 0, "c": "#2a221c", "t": "9th century BCE · slag", "tex": "blocks", "to": .08}, {"d": 200, "c": "#3a2f26", "t": "10th century BCE · the boom", "tex": "blocks", "to": .1},
                      {"d": 420, "c": "#4a3d33", "t": "11th century BCE"}, {"d": 560, "c": "#8a6d4d", "t": "bedrock"}],
           "cam": [1, 500, 900], "els": [{"k": "label", "x": 500, "y": 560, "t": "six metres of smelting waste, dated layer by layer", "c": AMBER, "in": .3},
                                         {"k": "label", "x": 500, "y": 1340, "t": "hundreds of radiocarbon dates · Levy et al. 2008; Ben-Yosef et al. 2012", "st": "small", "in": 1.0}]}
    s2 = sec
    s3 = stat("6", "metres of slag", "stacked up at Khirbat en-Nahas, mostly in the 10th and 9th centuries BCE", "Levy et al. 2008")
    tl, ax = timeline(-1350, -800, [(-1300, "1300 BCE"), (-1100, "1100"), (-900, "900")], "Who was smelting, and when", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-1300), "x1": ax.x(-1140), "y": 720, "h": 18, "c": "#cfe6ff", "t": "Egypt's Hathor shrine at Timna", "in": .3},
                  {"k": "band", "x0": ax.x(-1000), "x1": ax.x(-830), "y": 640, "h": 18, "c": GOLD, "t": "the boom · Faynan and Timna", "in": .6}] + \
                 event(ax, -950, "Solomon · tradition", row=2, c=AMBER, i=.9) + event(ax, -925, "Shishak's campaign", row=0, c=RED, i=1.2, sub="Karnak relief")
    s4 = tl
    s5 = quote("King Solomon's Mines", "H. Rider Haggard, 1885 · a novel, then a nickname", y=760, size=52)
    s6 = like(s0, cam=[1.15, 500, 1000])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE ARABAH][sfx:boom][act:setting the scene, vivid]Six metres of black ^slag. [act:building, rhythmic]^Furnace after furnace. [act:the hook, lower, intrigued]In a desert@noun valley with ^no king's name on it.",
                      "[d:tension][cam:1.12|0|0][act:plain storytelling]For decades the guidebooks called this a ^myth. [gap:0.4][act:the turn, a knowing smile]The myth had the ^right century."], cut=False),
        B("world", 1, ["[d:calm][k:FAYNAN AND TIMNA][act:calm, orienting]Two ^copper districts, either side of a modern ^border. [go:2|0][act:explaining, a little delighted]Dig down through the waste and the layers date themselves: ^hundreds of radiocarbon samples, from ^two teams."]),
        B("collision", 3, ["[d:build][k:THE BOOM][act:a set-up, curious][tune:rise]The ^peak? [act:clear, confident]The ^tenth and ^ninth centuries BCE. [sfx:shimmer][act:the connection, slower]The tenth century is the one tradition gives to David and ^Solomon.",
                           "[d:build][go:4|0][act:fair, recounting the debate]For a generation, one school said that century was nearly ^empty. [act:quiet, confident, a small smile]The ^slag says otherwise."]),
        B("cost", 5, ["[d:build][k:THE NAME][act:light, a fun fact]'King Solomon's Mines' is a ^novel from {1885|eighteen eighty-five}. [act:storytelling, amused]An archaeologist ^borrowed the title in the {1930s|nineteen thirties}. [d:aside][act:wry, quick][tune:level]Good ^marketing. [act:dry, a small smile][tune:fall]Bad ^footnote."]),
        B("reversal", 2, ["[d:reveal][k:THE TWIST][act:the twist, careful]Because ^nothing here names Solomon, or ^Jerusalem. [sfx:hit][act:explaining, even and fair]Most researchers credit a ^local kingdom, largely nomadic, that ran an industry from ^tents. [act:delighted, a touch of wonder]Which is its ^own surprise."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A copper ^boom in Solomon's century? [act:the verdict, confident][tune:highfall]^*Established*. [act:the second one, lighter][tune:rise]Solomon's ^mines? [act:even, a little playful][tune:fall]The ^owner is open.",
                     "[d:tension][p:0.93][act:summing up, warm]^Right century. [act:the open part, slower][tune:level]^Whose kingdom... [act:the last word, a knowing smile][tune:fall]is the ^receipt we don't have."]),
    ]
    return EP("solomon-mines", "10.04", "King Solomon's Mines: Right Century, Whose Kingdom?", "solomon-mines", "solid", "Were the Arabah mines booming in Solomon's day, and whose were they?", "The myth had the right *century*.", beats, shots,
              "Levy et al. 2008, PNAS · Ben-Yosef et al. 2012, BASOR · Ben-Yosef 2019 · Rothenberg 1972 · Sukenik et al. 2021, PLoS ONE",
              "Six metres of slag, hundreds of radiocarbon dates and a name borrowed from a novel: the copper boom of the 10th century BCE, and the kingdom nobody can name.",
              ["#Solomon", "#Archaeology", "#Copper", "#History", "#Timna"])


# ---------------------------------------------------------------- 10.05 Sheba
def sheba():
    dam = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 130, "prof": [[-70, 0], [-70, 10], [-40, 10], [-20, 2], [20, 2], [40, 10], [70, 10], [70, 0]], "c": "#7a6248", "edge": "rgba(255,236,206,.4)"},
           {"t": "box", "x": 0, "z": 0, "y": 2, "w": 46, "d": 6, "h": 8, "c": "#c9ad85", "edge": "rgba(0,0,0,.3)", "id": "dam"},
           {"t": "box", "x": -30, "z": 0, "y": 2, "w": 8, "d": 12, "h": 11, "c": "#d9c39a", "edge": "rgba(0,0,0,.3)"}, {"t": "box", "x": 30, "z": 0, "y": 2, "w": 8, "d": 12, "h": 11, "c": "#d9c39a", "edge": "rgba(0,0,0,.3)"},
           {"t": "flat", "pts": [[-19, 4], [19, 4], [19, 60], [-19, 60]], "y": 6.1, "c": "#3f86b0", "op": .7, "ground": False, "over": 2},
           {"t": "flat", "pts": [[-68, -62], [-42, -62], [-42, -8], [-68, -8]], "y": 10.1, "c": "#5a8a4a", "op": .8, "ground": False, "over": 2},
           {"t": "flat", "pts": [[42, -62], [68, -62], [68, -8], [42, -8]], "y": 10.1, "c": "#5a8a4a", "op": .8, "ground": False, "over": 2},
           L_(0, 10, "the Great Dam · 580 m", GOLD, z=0, dy=-16), L_(0, 6, "the flash flood, held", "#cfe6ff", z=40, dy=-14), L_(-48, 10, "a garden on the left", "#bfe0a8", z=-30, dy=-14), L_(46, 10, "a garden on the right", "#bfe0a8", z=-30, dy=-14)]
    s0 = iso(dam, cam=[1, 500, 900], s=4.6, x=500, y=980, az=-30, spin=1.4, el=.5, table=None)
    s0["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "Marib · schematic", "in": .2}]
    v = View(35, 49, 9, 20, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Marib · Saba", 45.35, 15.417, {"c": GOLD}), ("Sirwah", 45.0, 15.45, {"a": "end", "lx": -18}), ("Sana'a", 44.2, 15.35, {"a": "end", "lx": -18, "ly": 34}), ("Yeha · a Sabaean temple", 39.02, 14.28, {"c": SCAN, "a": "end", "lx": -18}), ("Aksum", 38.72, 14.13, {"a": "end", "lx": -18, "ly": 36})],
                 extra=[{"k": "label", "x": v.p(42, 13.2)[0], "y": v.p(42, 13.2)[1], "t": "Red Sea", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = stele(rows=11, kind="latin")
    s2["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "Sabaic inscriptions · from about 750 BCE", "in": .5},
                  {"k": "label", "x": 500, "y": 1320, "t": "kings, gods, dams and tribute · no queen, and nothing from Solomon's century", "st": "small", "in": 1.2}]
    s3 = stat("100", "km² of fields", "watered from the Marib dam: two irrigated oases, one either side of the wadi", "Brunner 1983; UNESCO 2023")
    tl, ax = timeline(-1000, 700, [(-1000, "1000 BCE"), (-500, "500"), (1, "1 CE"), (500, "500 CE")], "Saba on the record", y=980)
    tl["els"] += event(ax, -950, "Solomon · tradition", row=2, c=AMBER, i=.3) + event(ax, -750, "first Sabaic inscriptions", row=1, c=GOLD, i=.6) + \
                 event(ax, -715, "tribute to Sargon II", row=0, c=BONE, i=.9) + event(ax, 450, "the dam breached, repaired", row=1, c=SCAN, i=1.2) + event(ax, 575, "the last breach", row=0, c=RED, i=1.4)
    s4 = tl
    s5 = quote("There was indeed a sign for Sheba in their dwelling-place: two gardens on the right hand and on the left.", "Quran 34:15 · Pickthall's translation", y=680, size=40)
    s6 = like(s1, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:MARIB · YEMEN][sfx:boom][act:setting the scene, wonder]A ^dam five hundred and eighty metres ^long. [act:painting it, gently]Two ^gardens, one on ^each side. [act:the drama, lower, slower]And a ^flood that ended a ^kingdom.",
                      "[d:tension][cam:1.12|0|0][act:respectful, measured]The Quran describes ^exactly this. [act:the open question, curious][tune:rise]So did the Queen of Sheba ^visit Solomon?"], cut=False),
        B("world", 1, ["[d:calm][k:SABA][act:confident, plain]Saba was ^real. [act:warm, descriptive]A kingdom of ^incense, rich enough that Assyrian kings logged its ^tribute. [go:3|0][act:quiet wonder, the scale]Its dam watered a hundred square ^kilometres of fields for more than a ^thousand years.",
                       "[d:build][act:sober, a little heavier]And when the dam finally ^failed, in the sixth century, the oases ^died. [act:respectful, quietly noting it]^Exactly as the text says."]),
        B("collision", 2, ["[d:build][k:THE INSCRIPTIONS][act:turning a page, brisk]Now the ^visit. [act:precise, factual]Sabaean writing begins around {750|seven fifty} BCE. [sfx:shimmer][act:the gap, slower]Two ^centuries after Solomon. [act:plain, quiet, even]^None of it names a queen."]),
        B("cost", 4, ["[d:build][k:THE GAP][act:sober, fair]Early Saba is ^barely excavated, and since {2015|twenty fifteen} the war has ^stopped the digging. [d:aside][act:gentle, thoughtful, lighter]The queen, if she reigned, ruled ^before her country learned to write things down."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:counting them off, confident]So the ground confirms the ^kingdom, the ^gardens, the ^dam, the ^flood. [sfx:hit][act:quieter, precise]It is ^silent on the visit. [act:calm, principled, firm]Silence in ^unexcavated ground is ^not a verdict."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Saba and its ^dam? [act:the verdict, confident][tune:fall]^*Established*. [act:gentler, open][tune:rise]The queen's ^journey? [act:level-headed, respectful][tune:fall]Awaiting ^discovery.",
                     "[d:tension][p:0.93][act:quiet wonder, inviting]She ^may be under the ^sand at Marib. [gap:0.45][act:the last word, soft and plain][tune:fall]^Nobody has looked."]),
    ]
    return EP("sheba", "10.05", "The Queen of Sheba and the Flood of the Dam", "sheba", "unsupported", "Did a queen of Saba visit Solomon, and does the dam story fit Marib?", "A flood that ended a *kingdom*.", beats, shots,
              "Simpson (ed.) 2002, British Museum · Brunner 1983 · Vogt 2004 · Eph'al 1982 · UNESCO 2023 · Quran 34:15–16",
              "The real kingdom of Saba, its great dam and the flood that broke it, and the one thing the inscriptions never mention: a queen who travelled north.",
              ["#Sheba", "#Yemen", "#Archaeology", "#Quran", "#History"])


# ---------------------------------------------------------------- 10.06 Dhul-Qarnayn
def dhul_qarnayn():
    derbent = [{"t": "ext", "axis": "z", "z": 0, "y": 0, "at": 0, "d": 140, "prof": [[-70, 0], [-70, 30], [-40, 24], [-10, 8], [30, 2], [70, 1], [70, 0]], "c": "#7a6248", "edge": "rgba(255,236,206,.4)", "flipN": True},
               {"t": "flat", "pts": [[30, -70], [70, -70], [70, 70], [30, 70]], "y": 1.2, "c": "#3f86b0", "op": .75, "ground": False, "over": 2},
               {"t": "box", "x": -50, "z": 0, "y": 24, "w": 16, "d": 16, "h": 8, "c": "#c9ad85", "edge": "rgba(0,0,0,.3)"}] + \
              [{"t": "line", "p": [[-42, 24.5, zz], [-10, 8.5, zz], [30, 2.5, zz], [46, 1.5, zz]], "c": "#f2dcb4", "w": 4, "op": .95} for zz in (-8, 8)] + \
              [L_(-50, 34, "the citadel", GOLD, z=0, dy=-14), L_(10, 10, "two walls · 3.6 km, into the sea", "#f2dcb4", z=-22, dy=-16), L_(55, 1, "the Caspian", "#cfe6ff", z=40, dy=36)]
    s0 = iso(derbent, cam=[1, 500, 900], s=4.4, x=500, y=980, az=-32, spin=1.4, el=.5, table=None)
    s0["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "Derbent · the Caspian Gates · schematic", "in": .2}]
    v = View(39, 58, 35.5, 46, (40, 330, 920, 900))
    caspian = [(47, 44.5), (49.5, 46.5), (52, 46.8), (53.5, 45.5), (51.2, 44), (51, 42), (52.5, 41.5), (54, 40), (53.9, 37.5), (52, 36.7), (50, 37.3), (49, 38.5), (49.4, 40.2), (49.3, 42), (47.5, 43.5)]
    s1 = mapshot(v, pins=[("Derbent", 48.29, 42.06, {"c": GOLD}), ("the Darial Pass", 44.63, 42.74, {"a": "end", "lx": -18}), ("the Gorgan wall · 195 km", 54.5, 37.2, {"c": SCAN}), ("Persepolis", 52.89, 29.93, {"a": "end", "lx": -18})],
                 extra=[{"k": "poly", "p": [v.p(*q) for q in caspian], "fill": "rgba(63,134,176,.55)", "c": SCAN, "w": 1.2, "curve": True, "in": -1}, {"k": "label", "x": v.p(50.5, 41.5)[0], "y": v.p(50.5, 41.5)[1], "t": "Caspian Sea", "st": "ital", "c": "#9fd0ff"}, {"k": "label", "x": v.p(44, 43.6)[0], "y": v.p(44, 43.6)[1], "t": "Caucasus", "st": "ital", "c": "#c9ad85"},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    gorgan = [{"t": "slab", "x0": -80, "x1": 80, "z0": -30, "z1": 30, "y": 0, "c": "#8a7452"}, {"t": "box", "x": 0, "z": 0, "y": 0, "w": 160, "d": 2.5, "h": 3, "c": "#d9c39a", "edge": "rgba(0,0,0,.3)"}] + \
             [{"t": "box", "x": x, "z": 6, "y": 0, "w": 7, "d": 7, "h": 3.5, "c": "#c9ad85", "edge": "rgba(0,0,0,.3)"} for x in range(-70, 71, 20)] + \
             [{"t": "person", "x": 20, "y": 0, "z": 16, "h": 1.7}, L_(0, 5, "the Great Wall of Gorgan · 195 km · more than 30 forts", "#f2dcb4", z=0, dy=-18), L_(0, 0, "fired brick · 5th to 6th century CE", "#cfe6ff", z=24, dy=36)]
    s2 = iso(gorgan, cam=[1, 500, 900], s=4.8, x=500, y=980, az=-20, spin=1.2, el=.5, table=None)
    s3 = stat("195", "kilometres", "the Great Wall of Gorgan, east of the Caspian, dated by luminescence and radiocarbon to the 5th to 6th century CE; in Persian, Alexander's Barrier", "Sauer et al. 2013")
    tl, ax = timeline(-600, 900, [(-500, "500 BCE"), (1, "1 CE"), (500, "500 CE")], "The candidates, and the walls", y=980)
    tl["els"] += event(ax, -550, "Cyrus the Great", row=1, c=AMBER, i=.3) + event(ax, -330, "Alexander", row=2, c=AMBER, i=.5) + event(ax, 75, "Josephus: Alexander's iron gates", row=0, c=BONE, i=.7) + \
                 [{"k": "band", "x0": ax.x(420), "x1": ax.x(600), "y": 720, "h": 18, "c": SCAN, "t": "Derbent and Gorgan built · Sasanian", "in": .9}] + event(ax, 630, "the Syriac Alexander legend", row=2, c=GOLD, i=1.2)
    s4 = tl
    s5 = quote("Give me pieces of iron... Bring me molten copper to pour thereon.", "Quran 18:96 · Pickthall's translation", y=720, size=42)
    s6 = like(s1, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE CAUCASUS][sfx:boom][act:setting the scene, vivid]Two ^walls, running from a mountain citadel straight into the ^sea. [act:simple, clear]Built to ^shut a pass.",
                      "[d:tension][cam:1.12|0|0][act:respectful, measured, storytelling]The Quran tells of a king who built a barrier in a pass, of ^iron and molten ^copper. [act:curious, leaning in][tune:rise]Is ^this it?"], cut=False),
        B("world", 1, ["[d:calm][k:THE PASSES][act:orienting, calm]Between the steppe and the south there are only a ^few gaps. [go:2|0][act:touring them, brisk]Empires walled ^every one: ^Derbent, the ^Darial, and east of the Caspian a wall of a hundred and ninety-five kilometres with thirty ^forts."]),
        B("collision", 3, ["[d:build][k:THE DATES][act:turning a page, brisk]Now the ^dates. [sfx:shimmer][act:clear, confident]Every surviving wall is ^Sasanian. [act:precise, clipped][tune:level]^Fifth or ^sixth century CE. [act:plain, descriptive][tune:level]Fired ^brick and ^stone. [act:quiet, pointed][tune:fall]Not ^iron.",
                           "[d:build][go:4|0][act:measuring the gap, slower][tune:level]A ^thousand years after ^Cyrus. [act:the second measure, even][tune:fall]^Nine hundred after ^Alexander."]),
        B("cost", 5, ["[d:build][k:WHO?][act:genuinely curious, respectful][tune:fall]And ^who was Dhul-Qarnayn, the two-horned? [act:even-handed, laying out views][tune:level]^Classical commentators mostly said ^Alexander. [act:with care, fair][tune:level]^Others, Ibn Kathir among them, said an ^earlier righteous king. [act:the last view, fair][tune:fall]^Modern scholars propose ^Cyrus. [d:aside][act:warm, gentle, a light touch]The text gives a ^portrait, not a ^passport."]),
        B("reversal", 2, ["[d:reveal][k:THE TWIST][act:leaning in, the idea]Here is what ^nobody has done: dig ^*beneath* the Sasanian walls. [sfx:hit][act:explaining, steady]They were ^rebuilt again and again. [act:quiet wonder, inviting]Whatever stood in these passes ^before them is ^still in the ground."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A ^real barrier in a ^real pass? [act:the verdict, level-headed][tune:fall]^*Plausible*. [act:the harder part, curious][tune:fall]^Which wall, and ^whose? [act:even, respectful][tune:fall]An ^open question.",
                     "[d:tension][p:0.93][act:the last word, quiet and warm]The trowel has ^not reached the ^layer this story lives@verb in."]),
    ]
    return EP("dhul-qarnayn", "10.06", "Dhul-Qarnayn and the Wall Against Gog and Magog", "dhul-qarnayn", "contested", "Can archaeology find the barrier of Dhul-Qarnayn?", "Is *this* it?", beats, shots,
              "Sauer et al. 2013, Persia's Imperial Power in Late Antiquity · UNESCO 1070 · van Bladel 2008 · Tesei 2013–2014 · Josephus, Jewish War 7.245",
              "Walls that shut the passes between the steppe and the south, all dated to the 5th and 6th centuries CE, and the layers beneath them that nobody has dug.",
              ["#Quran", "#Caucasus", "#Archaeology", "#History", "#Derbent"])


# ---------------------------------------------------------------- 10.07 The Ark of the Covenant
def ark_covenant():
    box = [{"t": "box", "x": 0, "z": 0, "y": 6, "w": 44, "d": 26, "h": 26, "c": "#e2b45c", "edge": "rgba(0,0,0,.35)"},
           {"t": "box", "x": 0, "z": 0, "y": 32, "w": 46, "d": 28, "h": 2, "c": "#f2d27a", "edge": "rgba(0,0,0,.35)"},
           {"t": "pyr", "x": -12, "z": 0, "y": 34, "b": 8, "h": 12, "c": "#f2d27a", "edge": "rgba(0,0,0,.3)"}, {"t": "pyr", "x": 12, "z": 0, "y": 34, "b": 8, "h": 12, "c": "#f2d27a", "edge": "rgba(0,0,0,.3)"},
           {"t": "line", "p": [[-40, 12, 16], [40, 12, 16]], "c": "#6b4a2e", "w": 6}, {"t": "line", "p": [[-40, 12, -16], [40, 12, -16]], "c": "#6b4a2e", "w": 6},
           {"t": "person", "x": 46, "y": 0, "z": 30, "h": 1.7},
           L_(0, 48, "acacia wood, gold overlay · about 1.1 by 0.7 by 0.7 m", GOLD, z=0, dy=-18), L_(0, 0, "carried on poles · as Egyptian shrines were", "#cfe6ff", z=36, dy=40)]
    s0 = iso(box, cam=[1, 500, 900], s=5.2, x=500, y=1020, az=-30, spin=1.4, el=.45, table={"r": 60, "rz": 45, "grid": 12, "strata": [{"h": 2, "c": "#a8845c"}, {"h": 8, "c": "#7d6045"}]})
    s0["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "as Exodus 25 describes it", "in": .2}]
    v = View(27.5, 46, 9, 33.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Jerusalem", 35.23, 31.78, {"c": GOLD}), ("Elephantine · a Jewish temple, 5th c. BCE", 32.89, 24.09, {"c": SCAN, "a": "end", "lx": -18}), ("Tana Kirkos", 37.5, 12.1, {"a": "end", "lx": -18}), ("Aksum · the Chapel of the Tablet", 38.72, 14.13, {"c": GOLD})],
                 extra=[{"k": "line", "p": [v.p(35.23, 31.78), v.p(32.89, 24.09), v.p(37.5, 12.1), v.p(38.72, 14.13)], "c": GOLD, "w": 1.6, "op": .6, "style": "claimed", "curve": True, "in": .8},
                        {"k": "label", "x": v.p(33.5, 19)[0], "y": v.p(33.5, 19)[1], "t": "the route Hancock proposed", "st": "small", "c": GOLD, "in": 1.2}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}])
    chapel = [{"t": "box", "x": 0, "z": 0, "y": 0, "w": 30, "d": 24, "h": 14, "c": "#c9ad85", "edge": "rgba(0,0,0,.3)"}, {"t": "cyl", "x": 0, "z": 0, "y": 14, "r": 9, "h": 7, "c": "#d9c39a", "n": 18, "edge": "rgba(0,0,0,.25)"},
              {"t": "box", "x": 0, "z": 0, "y": 21, "w": 4, "d": 4, "h": 5, "c": "#e2b45c", "edge": "rgba(0,0,0,.3)"}, {"t": "quad", "p": [[-4, 0.2, 12.2], [4, 0.2, 12.2], [4, 8, 12.2], [-4, 8, 12.2]], "n": [0, 0, 1], "c": "#2a1f16", "op": 1, "over": 3},
              {"t": "person", "x": 10, "y": 0, "z": 22, "h": 1.7}, L_(0, 30, "the Chapel of the Tablet · Aksum", GOLD, z=0, dy=-16), L_(0, 0, "one guardian monk · no visitors, ever", "#cfe6ff", z=30, dy=40)]
    s2 = iso(chapel, cam=[1, 500, 900], s=5.6, x=500, y=1000, az=-24, spin=1.3, el=.45, table={"r": 50, "rz": 40, "grid": 10, "strata": [{"h": 2, "c": "#a8845c"}, {"h": 8, "c": "#7d6045"}]})
    s3 = stat("1,900", "years", "between the Ark's last mention in the record and the written Ethiopian account of its journey, the Kebra Nagast", "Munro-Hay 2005")
    tl, ax = timeline(-1150, 1500, [(-1000, "1000 BCE"), (-500, "500"), (1, "1 CE"), (500, "500"), (1000, "1000")], "The Ark, on and off the record", y=980)
    tl["els"] += event(ax, -950, "in Solomon's Temple · tradition", row=2, c=AMBER, i=.3) + event(ax, -586, "Babylon takes the Temple", row=1, c=RED, i=.6, sub="the Ark is not on the list") + \
                 event(ax, -63, "Pompey finds the sanctuary empty", row=0, c=BONE, i=.9) + event(ax, 1320, "the Kebra Nagast", row=1, c=GOLD, i=1.2, sub="the Aksum account, written")
    s4 = tl
    s5 = quote("The sanctuary contained no image of the god, and the secret recess was vacant.", "Tacitus, Histories 5.9 · on Pompey, 63 BCE", y=700, size=40)
    s6 = like(s0, cam=[1.15, 500, 1000])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE ARK][sfx:boom][act:reverent, setting the scene]A wooden ^chest covered in ^gold. [act:simple, a detail][tune:level]Carried on ^poles. [act:wonder, slower]The most famous ^lost object@noun on Earth.",
                      "[d:tension][cam:1.12|0|0][act:respectful, measured]A church in Ethiopia says it was ^never lost. [act:curious, gently][tune:rise]Can that be ^tested?"], cut=False),
        B("world", 0, ["[d:calm][k:WHAT IT WAS][act:grounded, interested]The description in Exodus fits its ^world: gilded shrines on poles are well known from ^Egypt. [go:4|0][act:quieter, the mystery begins]It ^vanishes from the record@noun around the fall of ^Jerusalem. [act:precise, a telling detail]The Babylonian loot list does@verb ^not mention it."]),
        B("collision", 2, ["[d:build][k:AKSUM][act:respectful, hushed]In Aksum, ^one monk guards a chapel for ^life. [sfx:shimmer][act:quiet, simple]^Nobody else goes in. [act:sincere, with care][tune:fall]The tradition is ^sincere, ^old, and central to a ^living church.",
                           "[d:build][go:3|0][act:plain, even, factual]Its ^written form is nineteen ^hundred years after the events."]),
        B("cost", 1, ["[d:build][k:THE ROUTE][act:fair, recounting it]Graham Hancock traced a route: ^Jerusalem, a Jewish temple on the ^Nile, an island in Lake ^Tana, ^Aksum. [d:aside][act:even, generous][tune:fallrise]^Real places. [act:plain, careful]^No source says the Ark passed through them."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:storytelling, a hush]In sixty-three BCE a Roman general walked into the Temple's ^holiest room. [sfx:hit][act:the reveal, quiet][tune:fall]Tacitus says he found it ^empty. [act:with care, reflective]Whatever the Ark's fate, it had ^already happened."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, respectful][tune:rise]The Ark at ^Aksum? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:even, balanced][tune:level]Nothing ^contradicts it. [act:the same weight, calm][tune:fall]Nothing ^supports it.",
                     "[d:tension][p:0.93][act:thoughtful, a quiet wish]^One radiocarbon date on one sliver of wood would ^settle it. [gap:0.45][act:the last word, gentle, accepting][tune:fall]The door stays ^shut."]),
    ]
    return EP("ark-covenant", "10.07", "The Ark of the Covenant: Lost, Hidden or Guarded?", "ark-covenant", "unsupported", "What happened to the Ark, and could the Aksum tradition ever be tested?", "Can that be *tested*?", beats, shots,
              "Munro-Hay 2005 · Finkelstein & Römer 2018, 2021 · Römer 2015 · Hancock 1992 · Tacitus, Histories 5.9 · 2 Kings 25:13–17",
              "A gilded chest that vanishes from the record, a Roman who found the sanctuary empty, and a chapel in Aksum nobody may enter: what can and cannot be tested about the Ark.",
              ["#ArkOfTheCovenant", "#Ethiopia", "#Bible", "#History", "#Aksum"])


# ---------------------------------------------------------------- 10.08 The star of Bethlehem
def star():
    s0 = {"base": "sky", "tod": "night", "ground": 1200, "sun": False, "cam": [1, 500, 860], "els": [
          {"k": "glow", "x": 470, "y": 700, "r": 90, "kind": "lamp", "op": .9, "in": .2}, {"k": "circle", "x": 470, "y": 700, "r": 9, "fill": "#fff3d0", "c": "none", "w": 0, "in": .2},
          {"k": "glow", "x": 530, "y": 716, "r": 60, "kind": "lamp", "op": .7, "in": .5}, {"k": "circle", "x": 530, "y": 716, "r": 6, "fill": "#ffe2a8", "c": "none", "w": 0, "in": .5},
          {"k": "label", "x": 470, "y": 660, "t": "Jupiter", "st": "small", "c": "#fff3d0", "in": .8}, {"k": "label", "x": 560, "y": 750, "t": "Saturn", "st": "small", "c": "#ffe2a8", "in": .9},
          {"k": "cap", "x": 500, "y": 400, "t": "7 BCE · Jupiter meets Saturn, three times, in Pisces", "in": .3},
          {"k": "label", "x": 500, "y": 1280, "t": "about one degree apart, in May, October and December", "in": 1.2}]}
    v = View(33, 46, 29.5, 34.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Babylon", 44.42, 32.54, {"c": GOLD}), ("Jerusalem", 35.23, 31.78, {"a": "end", "lx": -18}), ("Bethlehem", 35.2, 31.705, {"c": GOLD, "a": "end", "lx": -18, "ly": 34})],
                 extra=[{"k": "line", "p": [v.p(44.42, 32.54), v.p(40.5, 34.2), v.p(36.3, 33.5), v.p(35.23, 31.78)], "c": GOLD, "w": 1.6, "op": .6, "style": "inferred", "curve": True, "in": .8},
                        {"k": "label", "x": v.p(39.5, 34.6)[0], "y": v.p(39.5, 34.6)[1], "t": "the road the Magi would take · about 900 km", "st": "small", "c": GOLD, "in": 1.2}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = tablet(text_rows=11)
    s2["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "a Babylonian almanac for 7/6 BCE", "in": .5},
                  {"k": "label", "x": 500, "y": 1260, "t": "the planets' positions, predicted a year ahead: Jupiter and Saturn in Pisces", "st": "small", "in": 1.2}]
    s3 = stat("70", "days", "a 'broom star', a comet, logged by Chinese astronomers in spring 5 BCE", "Han shu; Humphreys 1991")
    tl, ax = timeline(-8, -3, [(-8, "8 BCE"), (-7, "7"), (-6, "6"), (-5, "5"), (-4, "4")], "The sky over Judea", y=980)
    tl["els"] += event(ax, -6.6, "Jupiter and Saturn meet", row=1, c=GOLD, i=.3, sub="three times in 7 BCE") + event(ax, -5.7, "the Moon covers Jupiter", row=2, c=SCAN, i=.6) + \
                 event(ax, -4.8, "the comet of 5 BCE", row=0, c=BONE, i=.9) + event(ax, -3.9, "Herod dies", row=1, c=RED, i=1.2, sub="the usual date")
    s4 = tl
    s5 = quote("We have seen his star in the east, and are come to worship him.", "Matthew 2:2 · King James Version", y=720, size=42)
    s6 = like(s0, cam=[1.15, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:7 BCE][sfx:boom][act:wonder, painting the sky]Two ^planets, drifting ^together in the night sky. [act:the marvel, slower]^Three times in ^one year.",
                      "[d:tension][cam:1.12|0|0][act:curious, pulling us in][tune:rise]Was ^this the star? [act:the second option][tune:rise]Or was it the ^comet two years later? [act:the last possibility, quieter][tune:fall]Or was it ^nothing at all?"], cut=False),
        B("world", 5, ["[d:calm][k:ONE GOSPEL][act:respectful, storytelling]^Only Matthew tells it: wise men from the ^east, a star at its ^rising. [go:1|0][act:thoughtful, connecting]If they were ^sky-readers, they came from a land that had logged the sky for a ^thousand years."]),
        B("collision", 2, ["[d:build][k:THE ALMANAC][act:leaning in, intrigued]Here is the ^strange part. [sfx:shimmer][act:the reveal, precise]A Babylonian tablet ^predicted the {7|seven} BCE meetings of Jupiter and Saturn a year in ^advance. [act:quiet wonder, warm]Sky-watchers were ^expecting them.",
                           "[d:build][go:3|0][act:adding another, bright]And in {5|five} BCE, ^Chinese astronomers logged a comet for ^seventy days."]),
        B("cost", 4, ["[d:build][k:THE CANDIDATES][act:counting them off]^Conjunction, ^occultation, ^comet. [act:even, a little amused]Each has its ^champion. [d:aside][act:gentle, respectful, precise]^None of them walks ahead of travellers and ^stops over a house@noun. [act:with care, thoughtful]The text may be doing something ^other than reporting."]),
        B("reversal", 0, ["[d:reveal][k:THE TWIST][act:the turn, leaning in]Yet the candidates are ^real and datable, and they crowd into ^exactly the right few years. [sfx:hit][act:storytelling, delighted]^Kepler noticed that in {1604|sixteen oh four}. [act:warm, a gentle smile]It has ^not stopped being odd."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A real ^sign behind the story? [act:the verdict, warm][tune:fall]^*Plausible*. [act:lighter, quick][tune:fall]^Which one? [act:plain, one word][tune:fall]^Open.",
                     "[d:tension][p:0.93][act:reflective, respectful][tune:level]The ^sky keeps its records@noun. [act:the last word, warm and sincere][tune:fall]The ^Gospel kept a ^star."]),
    ]
    return EP("star-bethlehem", "10.08", "The Star of Bethlehem: A Sky Worth Reading", "star-bethlehem", "plausible", "Was Matthew's star a real event in the sky?", "Or was it *nothing* at all?", beats, shots,
              "Humphreys 1991, QJRAS · Molnar 1999 · Hughes 1976, Nature · Sachs & Walker 1984 · Matney 2025 · Kepler 1606",
              "Three meetings of Jupiter and Saturn, a Babylonian almanac that predicted them, and a comet logged in China: the sky of 7 to 5 BCE, and the one Gospel that mentions a star.",
              ["#StarOfBethlehem", "#Astronomy", "#History", "#Bible", "#Kepler"])


# ---------------------------------------------------------------- 10.09 The splitting of the Moon
def moon_split():
    s0 = {"base": "dark", "stars": 160, "cam": [1, 500, 860], "els": [
          {"k": "glow", "x": 500, "y": 820, "r": 420, "kind": "lamp", "op": .35, "in": .1}, {"k": "circle", "x": 500, "y": 820, "r": 300, "fill": "#cfc6b4", "c": "#e8e0d0", "w": 2, "in": .1}] +
          [{"k": "circle", "x": 500 + dx, "y": 820 + dy, "r": r, "fill": "#a9a08e", "c": "none", "w": 0, "in": .3} for dx, dy, r in ((-120, -80, 60), (90, -140, 40), (140, 60, 70), (-60, 150, 45), (20, 20, 30), (-180, 60, 28))] +
          [{"k": "line", "p": [[380, 700], [470, 760], [560, 790], [650, 850]], "c": "#5a5040", "w": 3, "op": .9, "in": .8, "fx": "draw"},
           {"k": "label", "x": 690, "y": 890, "t": "Rima Ariadaeus · 300 km", "st": "small", "c": "#fff6e6", "a": "start", "in": 1.2},
           {"k": "cap", "x": 500, "y": 400, "t": "the 'scar' shared online", "in": .3}]}
    sec = {"base": "section", "tod": "night", "ground": 700, "lx": 130, "layers": [{"d": 0, "c": "#8a8070", "t": "lunar crust"}, {"d": 260, "c": "#5a5248", "t": "", "tex": "blocks", "to": .08}],
           "cam": [1, 500, 900], "els": [{"k": "line", "p": [[330, 700], [300, 1300]], "c": RED, "w": 2.2, "style": "inferred", "in": .3}, {"k": "line", "p": [[670, 700], [700, 1300]], "c": RED, "w": 2.2, "style": "inferred", "in": .5},
                                         {"k": "rect", "x": 330, "y": 700, "w": 340, "h": 40, "fill": "#1a1714", "c": "none", "sw": 0, "in": .7},
                                         {"k": "label", "x": 500, "y": 640, "t": "a graben: a strip of crust dropped between two faults", "c": "#ffb09a", "in": .8},
                                         {"k": "label", "x": 500, "y": 1240, "t": "craters on the youngest grabens give ages of tens of millions of years", "st": "small", "in": 1.2}]}
    s1 = sec
    s2 = stat("300", "kilometres", "the length of Rima Ariadaeus, a strip of crust that dropped between faults as the Moon's surface stretched", "Wilhelms 1987; Watters et al. 2012")
    s3 = quote("The hour drew nigh and the moon was rent in twain.", "Quran 54:1 · Pickthall's translation", y=760, size=44)
    v = View(39.4, 40.4, 21.1, 21.8, (40, 330, 920, 900))
    s4 = mapshot(v, pins=[("Mina", 39.893, 21.413, {"c": GOLD}), ("Mecca", 39.826, 21.4225, {"a": "end", "lx": -18})], extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(5), "t": "5 km"},
                 {"k": "label", "x": 500, "y": 400, "t": "where the reports place the witnesses", "st": "small", "c": AMBER, "in": .8}])
    s5 = like(s0, cam=[1.15, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE MOON][sfx:boom][act:intrigued, setting the scene]A crack three hundred kilometres long, shared ^online as the scar of a ^miracle.",
                      "[d:tension][cam:1.12|0|0][act:curious, inviting][tune:fall]What can a rille ^tell us? [act:the careful half][tune:fall]And what ^can't it?"], cut=False),
        B("world", 3, ["[d:calm][k:THE ACCOUNT][act:respectful, measured]The Quran opens a chapter with the Moon ^split. [act:with care, even]Reports in the hadith describe ^witnesses at Mina seeing it in ^two. [go:4|0][act:sincere, recounting][tune:fall]A ^sign, ^seen, and dismissed by some as ^magic. [act:plain, respectful, simple]That is the ^account."]),
        B("collision", 1, ["[d:build][k:THE RILLE][act:turning a page, brisk]Now the ^crack. [sfx:shimmer][act:explaining, clear and curious]Rima Ariadaeus is a ^graben: a strip of crust that dropped between two faults as the surface ^stretched.",
                           "[d:build][go:2|0][act:plain, a detective's clue]Craters sit on ^top of it. [act:the reveal, measured]Count them, and the trough is tens of ^millions of years old."]),
        B("cost", 2, ["[d:build][k:THE SHAPE][act:reasoning, careful]A Moon split in two and rejoined would leave ^global traces of a different kind: a ^seam, a ^remelting, a ^resurfacing. [d:aside][act:quiet, factual]Rock samples show ^none. [act:gentle, precise]^One trough is ^not that shape."]),
        B("reversal", 3, ["[d:reveal][k:THE TWIST][act:leaning in, respectful]And notice: ^neither the Quran nor the reports say a ^mark was left behind. [sfx:hit][act:clear, even]The scar is a ^modern addition. [act:the key point, calm and fair]Ruling it out rules out ^nothing the texts say."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]The ^'scar'? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:gentler, respectful][tune:rise]The ^sign itself? [act:with care, sincere, measured][tune:fall]A matter of ^faith, and not ^ours to rate.",
                     "[d:tension][p:0.93][act:quiet, principled][tune:level]We weigh ^rock. [act:the last word, sincere and gentle][tune:fall]We do ^not weigh ^belief."]),
    ]
    return EP("moon-split", "10.09", "The Splitting of the Moon: What a Rille Can't Tell Us", "moon-split", "debunked", "Are lunar rilles the scar of the Moon's splitting?", "What can a rille *tell* us?", beats, shots,
              "Watters et al. 2012, Nature Geoscience · Andrews-Hanna et al. 2013 · Wilhelms 1987, USGS · Sahih al-Bukhari 3869 · Quran 54:1–2",
              "A 300 km lunar trough shared as the scar of a miracle: what crater counts and rock samples say about the rille, and why that leaves the sign itself untouched.",
              ["#Moon", "#Quran", "#Geology", "#Astronomy", "#History"])


# ---------------------------------------------------------------- 10.10 The ledger
def _ledger_text():
    v = View(28, 60, 8, 46, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("Jerusalem", 35.23, 31.78, {"c": GOLD}), ("Sinai", 33.6, 29.2, {"a": "end", "lx": -18}), ("Marib", 45.35, 15.417, {}), ("Aksum", 38.72, 14.13, {"a": "end", "lx": -18}), ("Derbent", 48.29, 42.06, {}), ("Faynan", 35.437, 30.681, {"a": "start", "ly": 34}), ("Babylon", 44.42, 32.54, {})], cam=[1.05, 500, 870])

    def grp(title, c, items):
        return [{"k": "cap", "x": 500, "y": 520, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": 600 + i * 64, "t": t, "st": "serif", "size": 30, "in": .4 + i * .2} for i, t in enumerate(items)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["Saba, its dam and the flood that broke it", "a copper boom in the 10th century BCE", "the eclipse of 30 October 1207 BCE", "the meetings of Jupiter and Saturn in 7 BCE"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible or open", "#e8b87a", ["a smaller exodus", "the poem remembering the eclipse", "a real barrier in a real pass", "a real sign behind the star"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting discovery", "#9fd0ff", ["the headcount of Exodus", "Jericho's walls in 1400 BCE", "the queen's journey to Solomon", "the Ark at Aksum"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["the lunar 'scar'"])}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 560, "t": "never rated", "c": "#cbbca8", "in": .2}, {"k": "title", "x": 500, "y": 720, "t": "What faith holds.", "size": 60, "in": .5},
          {"k": "label", "x": 500, "y": 860, "t": "We weigh stones, dates, slag and skies. Not signs.", "st": "small", "in": 1.0}]}
    s6 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:SCRIPTURE AND STONE II][sfx:boom][act:warm, opening the book]^Nine stories from the texts. [act:naming them, with wonder]^Kings, ^prophets, and signs in the ^sky. [act:inviting, a small smile]Here is the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, ticking them off][tune:level]Saba was ^real, and so was its ^dam. [act:steady, confident][tune:level]The Arabah was smelting ^copper in Solomon's century. [act:plain, sure][tune:level]An ^eclipse crossed Gibeon in {1207|twelve oh seven} BCE. [act:the last one, warm][tune:fall]^Jupiter met ^Saturn in {7|seven} BCE."]),
        B("collision", 2, ["[d:build][k:PLAUSIBLE OR OPEN][act:weighing each, even][tune:level]A ^smaller exodus. [act:open, thoughtful][tune:level]A ^poem that may remember the eclipse. [act:curious, open][tune:level]A barrier in a pass ^nobody has dug beneath. [act:the last, gentle][tune:fall]A ^sign behind the star."]),
        B("cost", 3, ["[d:build][k:AWAITING DISCOVERY][act:patient, going through them][tune:level]The ^headcount of Exodus. [act:even, steady][tune:level]Jericho's ^walls at {1400|fourteen hundred}. [act:gentle, softer][tune:level]The queen's ^journey. [act:the last, respectful][tune:fall]The Ark at ^Aksum. [d:aside][act:calm, principled]Absence, in ground ^nobody has excavated, is ^not a verdict."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:clear, precise]^One thing only: the lunar ^scar. [act:quiet, respectful, fair]A ^modern claim the texts ^never made."]),
        B("tag", 5, ["[d:verdict][k:NEVER RATED][p:0.95][act:sincere, gentle, with respect]And what ^faith holds, we do ^not weigh. [go:6|2][act:counting them off, warm]We weigh ^stones, ^dates, ^slag and ^skies.",
                     "[d:tension][p:0.93][act:the motto, calm and warm]^Coherence is the measure. [act:quiet, the last word][tune:fall]Not ^final demonstration."]),
    ]
    return EP("scripture-ledger-2", "10.10", "Scripture and Stone II · The Ledger", "", "mixed", "What stands, what waits, and what is never rated.", "Here is the *ledger*.", beats, shots,
              "Every source in the nine case files of File 10",
              "The verdicts of Scripture and Stone II in one ledger: what the ground and the sky confirm, what waits in unexcavated ground, and what is never rated.",
              ["#History", "#Archaeology", "#Bible", "#Quran", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: nine stories from the texts. Only stones, dates, slag and skies are weighed; what faith holds is framed in gold and never rated."""
    from cabinet import Cabinet, VCOL, retime, X0, X1
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    C = Cabinet([
        {"name": "Saba's dam", "model": mdl(sheba())},
        {"name": "The Arabah", "model": mdl(solomon())},
        {"name": "Gibeon's sun", "model": mdl(joshua(), 0)},
        {"name": "The star", "model": mdl(star(), 0), "zk": 1.6, "wy": -170},
        {"name": "The exodus", "model": mdl(exodus())},
        {"name": "Jericho", "model": mdl(jericho())},
        {"name": "The barrier", "model": mdl(dhul_qarnayn())},
        {"name": "Aksum", "model": mdl(ark_covenant())},
        {"name": "Lunar rilles", "model": mdl(moon_split(), 0), "zk": .72},
    ])
    C.build()
    SA, AM, JS, ST, EX, JE, BR, AK, LR = range(9)
    G = "#e8c878"
    gold = [{"k": "rect", "x": X0 - 34, "y": round(C.Y0 - 34, 1), "w": X1 - X0 + 68, "h": round(C.Y1 - C.Y0 + 68, 1), "r": 18, "fill": "none", "c": G, "sw": 6, "fx": "draw", "dur": 2.0, "in": .2},
            {"k": "rect", "x": 320, "y": round(C.Y0 - 64, 1), "w": 360, "h": 60, "r": 30, "fill": "#1c140e", "c": G, "sw": 2, "in": 1.4, "fx": "pop"},
            {"k": "label", "x": 500, "y": round(C.Y0 - 23, 1), "t": "NEVER RATED", "st": "small", "c": G, "size": 32, "scl": True, "halo": False, "in": 1.5}]
    s1 = C.step(C.cam_cell(SA), C.verdict(SA, "established", "real, and its dam", .4))
    s2 = C.step(C.cam_cell(AM), C.verdict(AM, "established", "copper, that century", .3) + C.people(AM, 2, at=.8))
    s3 = C.step(C.cam_cell(JS), C.verdict(JS, "established", "eclipse, 1207 BCE", .3))
    s4 = C.step(C.cam_cell(ST), C.verdict(ST, "established", "7 BCE", .3))
    s5 = C.step(C.cam_cell(EX), C.verdict(EX, "plausible", "a smaller one", .2))
    s6 = C.step(C.cam_cell(JS), C.verdict(JS, "open", "a poem remembers it?", .2, frame=False))
    s7 = C.step(C.cam_cell(BR), C.verdict(BR, "open", "never dug beneath", .2) + C.question(BR, dx=C.w * .3, dy=-150, at=.6, size=64))
    s8 = C.step(C.cam_cell(ST), C.verdict(ST, "plausible", "a sign behind it", .2, frame=False))
    s9 = C.step(C.cam_cell(EX), C.verdict(EX, "awaiting", "the headcount", .1))
    s10 = C.step(C.cam_cell(JE), C.verdict(JE, "awaiting", "walls at 1400?", .1))
    s11 = C.step(C.cam_cell(SA), C.verdict(SA, "awaiting", "the journey?", .1, frame=False))
    s12 = C.step(C.cam_cell(AK), C.verdict(AK, "awaiting", "the Ark here?", .1))
    s13 = C.step(C.cam_all(), [e for k, i in enumerate((EX, JE, SA, AK)) for e in C.wash(i, VCOL["awaiting"], at=.2 + .15 * k, op=.13)])
    s14 = C.step(C.cam_cell(LR), C.verdict(LR, "ruled", at=.1) + C.struck(LR, "rilles as a scar", at=.2))
    s15 = C.step(C.cam_cell(LR), C.note(LR, "a modern claim, not the texts'", at=.3, c="#f2c98e"))
    s16 = C.step(C.cam_all(k=.9), gold)
    s17 = C.step(C.cam_all(k=.9), [e for i in range(9) for e in C.wash(i, "#cbbca8", at=.1 + .1 * i, op=.08)])
    s18 = C.step(C.cam_all(k=.84, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.0" % s2, (0, 2): "%d|1.0" % s3, (0, 3): "%d|1.0" % s4}),
        2: (s5, {(0, 1): "%d|1.0" % s6, (0, 2): "%d|1.0" % s7, (0, 3): "%d|1.0" % s8}),
        3: (s9, {(0, 1): "%d|.9" % s10, (0, 2): "%d|.9" % s11, (0, 3): "%d|.9" % s12, (0, 4): "%d|1.2" % s13}),
        4: (s14, {(0, 1): "%d|.3" % s15}),
        5: (s16, {(0, 1): "%d|.4" % s17, (1, 0): "%d|3" % s18}),
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
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/scripture-ledger-2.json)."""
    import recap
    return recap.recap(ledger, "scripture-ledger-2", _gold)


def EPISODES():
    return [exodus(), jericho(), joshua(), solomon(), sheba(), dhul_qarnayn(), ark_covenant(), star(), moon_split(), ledger_recap()]
