"""File 04 · Drowned Worlds. The coastlines the sea took, and the legends that followed.
The headline mysteries of the drowned world, each weighed: the Eye of the Sahara, Atlantis, Bimini, Yonaguni, the lost civilisation,
the real drowned coasts, stories older than the sea, Dwarka and Rama Setu. Sacred texts are quoted, never rated."""
import math
from films import like, View, Axis
from scenes import timeline as _timeline, event, stat, quote, papyrus, silhouette, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso, lab, aim
from f09 import B, L_

SERIES = "Drowned Worlds"
SEA = "#3f86b0"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def ring(r, y=0.3, c="#8c6a48", w=6, op=1, n=48, rz=None, cx=0, cz=0):
    rz = rz or r
    return {"t": "line", "p": [[cx + r * math.cos(2 * math.pi * k / n), y, cz + rz * math.sin(2 * math.pi * k / n)] for k in range(n + 1)], "c": c, "w": w, "op": op}


def disc(r, y, c, over, op=1, n=40, cx=0, cz=0):
    return {"t": "flat", "pts": [[cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)] for k in range(n)], "y": y, "c": c, "op": op, "ground": False, "over": over}


def water(x0, x1, z0, z1, y, op=.32, over=6):
    return {"t": "flat", "pts": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "y": y, "c": SEA, "op": op, "ground": False, "over": over}


# ---------------------------------------------------------------- 04.01 The Eye of the Sahara
def richat():
    eye = [disc(46, .2, "#c9a370", 1), disc(34, .3, "#b8905e", 2), disc(22, .4, "#c9a370", 3), disc(10, .5, "#a07a50", 4)] + \
          [ring(r, .6, "#6f5236", 5, .95) for r in (44, 32, 20)] + \
          [{"t": "prism", "pts": [[8 * math.cos(2 * math.pi * k / 16), 8 * math.sin(2 * math.pi * k / 16)] for k in range(16)], "y": .5, "h": 2.4, "c": "#d9b98a", "edge": "rgba(0,0,0,.2)"},
           L_(0, 3, "the Richat Structure · about 40 km across", GOLD, z=-46, dy=-20), L_(0, 1, "three rings of hard, tilted rock", "#cfe6ff", z=48, dy=40)]
    s0 = iso(eye, cam=[1, 500, 900], s=6, x=500, y=1000, az=-20, spin=1.2, el=.62, table=None)
    s0["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "Mauritania · as seen from orbit, tilted", "in": .2}]
    v = View(-18, -2, 15, 36.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("the Eye · Richat", -11.39, 21.12, {"c": GOLD}), ("Gibraltar · the Pillars of Heracles", -5.35, 36.0, {"a": "start"}), ("Nouakchott", -15.98, 18.08, {"a": "start", "ly": 34})],
                 extra=[{"k": "label", "x": v.p(-5, 31.5)[0], "y": v.p(-5, 31.5)[1], "t": "the Atlas mountains", "st": "ital", "c": "#c9ad85"},
                        {"k": "label", "x": v.p(-13, 25)[0], "y": v.p(-13, 25)[1], "t": "Sahara", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}])
    R = 30.0; r = R / 8                                     # to scale: 40 km against about 5 km
    plato = [disc(R, .2, "#c9a370", 1, cx=12), disc(R * .74, .3, "#b8905e", 2, cx=12), disc(R * .48, .4, "#c9a370", 3, cx=12), disc(R * .22, .5, "#d9b98a", 4, cx=12)] + \
            [ring(R * f, .6, "#6f5236", 4, .95, cx=12) for f in (.96, .7, .44)] + \
            [disc(r, .8, SEA, 5, cx=-36), disc(r * .8, .9, "#8aa05a", 6, cx=-36), disc(r * .58, 1.0, SEA, 7, cx=-36), disc(r * .38, 1.1, "#8aa05a", 8, cx=-36), disc(r * .22, 1.2, SEA, 9, cx=-36), disc(r * .12, 1.3, "#f2dcb4", 10, cx=-36)] + \
            [L_(-36, 1, "Plato's ring city · about 5 km", "#cfe6ff", z=-4, dy=-26), L_(12, 1, "the Eye · about 40 km", GOLD, z=-R, dy=-20)]
    s2 = iso(plato, cam=[1, 500, 900], s=7, x=520, y=980, az=-12, spin=1.0, el=.6, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "to scale", "in": .2}]
    s3 = stat("8×", "too big", "the Eye is about eight times wider than the ring city Plato describes: 27 stadia, roughly 5 km", "Plato, Critias 115d–116a; Matton et al. 2005")
    arches = []
    for k, c in enumerate(("#e9dccb", "#c9a370", "#8c6a48")):
        pts = [[80 + 70 * i, 1260 - 760 * math.sin(math.pi * i / 12) + 70 * k] for i in range(13)]
        below = [q for q in pts if q[1] >= 700]
        left = [q for q in pts[:7] if q[1] >= 700]; right = [q for q in pts[6:] if q[1] >= 700]
        arches += [{"k": "line", "p": left, "c": c, "w": 5, "curve": True, "op": .95, "in": .3 + k * .2}, {"k": "line", "p": right, "c": c, "w": 5, "curve": True, "op": .95, "in": .3 + k * .2},
                   {"k": "line", "p": [q for q in pts if q[1] <= 760], "c": c, "w": 2, "curve": True, "op": .45, "style": "claimed", "in": 1.0 + k * .2}]
    arches += [{"k": "label", "x": 500, "y": 400, "t": "the top of the dome, worn away by wind", "c": "#ffb09a", "in": 1.4},
               {"k": "label", "x": 500, "y": 1370, "t": "each ring = the edge of a tilted layer · 1,000 to 450 million years old", "st": "small", "in": 1.7}]
    sec = {"base": "section", "tod": "dusk", "ground": 700, "lx": 130, "layers": [{"d": 0, "c": "#b8905e", "t": "the desert surface"}, {"d": 380, "c": "#7a6248", "t": "", "tex": "blocks", "to": .08}],
           "cam": [1, 500, 900], "els": arches}
    s4 = sec
    s5 = quote("There were two of land and three of water, which he turned as with a lathe, out of the centre of the island.", "Plato, Critias 113d · Jowett's translation", y=680, size=40)
    s6 = like(s0, cam=[1.2, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE EYE OF THE SAHARA][sfx:boom][act:wonder, setting the scene]From space, the Sahara has an ^eye. [act:measured, letting it grow][tune:fall]^Forty kilometres across. [act:quiet, a little eerie][tune:fall]Staring straight ^up.",
                      "[d:tension][cam:1.12|0|0][act:reporting the claim, even]^Millions of people online say it's ^Atlantis. [act:brisk, rolling up sleeves][tune:fall]Let's ^look."], cut=False),
        B("world", 5, ["[d:calm][k:PLATO'S CITY][act:storytelling, painting it]Plato described Atlantis as rings: two of ^land, three of ^water, around an ^island. [act:adding detail, unhurried][tune:level]Beyond the Pillars of ^Heracles. [go:1|0][act:placing it, gently final][tune:fall]Facing the ^Atlantic.",
                       "[d:build][act:turning to it, curious][tune:rise]And the ^Eye? [act:ticking them off][tune:level]^Rings. [act:next one][tune:level]Near the ^Atlantic. [act:and one more][tune:level]Mountains to the ^north, the ^Atlas. [sfx:shimmer][act:generous, warm][tune:fall]It's a ^good match. [gap:0.4][act:the small catch, dry][tune:fallrise]At ^first."]),
        B("collision", 2, ["[d:build][k:TO SCALE][act:inviting, hands on the table][tune:fall]Now put them side by ^side. [act:measured, precise][tune:level]Plato's city: about ^five kilometres across. [sfx:hit][act:the punch, blunt][tune:highfall]The Eye: ^forty.",
                           "[d:build][go:3|0][act:plain, a little amused][tune:fall]It's ^eight times too big. [act:adding the second strike][tune:fall]And it's ^high in the desert@noun, hundreds of kilometres from ^any sea."]),
        B("cost", 4, ["[d:build][k:THE ROCK][act:explaining, clear and patient]Cut it open and the rings are ^layers of rock, tilted up into a dome and worn flat by the ^wind@air. [act:a quiet aside of wonder][tune:fall]They carry on ^underground.",
                      "[d:aside][act:light, wide-eyed][tune:fall]The rings are older than the ^dinosaurs. [act:tossed off, then a grin][tune:fall]By a few hundred ^million years."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:the second surprise, lean in][tune:fall]It isn't a ^crater, either. [sfx:shimmer][act:telling the real story, steady]^Molten rock pushed up from below, hot ^water ate out the centre, and ^wind@air did the carving. [d:build][act:summing up, affectionate][tune:fall]A natural ^blister, sanded ^down."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Atlantis in the ^Eye? [act:the verdict, level-headed][tune:fall]*Ruled ^out*. [act:turning to the open door, warmer][tune:rise]People living here when the Sahara was ^green? [act:honest, gently hopeful][tune:fall]^Possible, and ^barely surveyed.",
                     "[d:tension][p:0.93][act:a concession, sincere][tune:fall]The Eye is ^real. [gap:0.45][act:the last word, quiet][tune:fall]The ^city in it ^isn't."]),
    ]
    return EP("richat", "04.01", "The Eye of the Sahara: Atlantis in the Desert?", "richat", "debunked", "Is the Richat Structure Plato's Atlantis?", "The Sahara has an *eye*.", beats, shots,
              "Matton et al. 2005, Journal of African Earth Sciences · Matton & Jébrak 2014 · Abdeina et al. 2024 · Fudali 1969, Science · Plato, Critias 113d–117e",
              "Forty kilometres of rings in the Sahara, shared online as Atlantis: Plato's ring city to scale beside it, and what the rock itself says.",
              ["#EyeOfTheSahara", "#Atlantis", "#Richat", "#Geology", "#Mystery"])


# ---------------------------------------------------------------- 04.02 Atlantis
def atlantis():
    s0 = papyrus(rows=10, cols=8, kind="hieratic", holes=False)
    s0["els"] += [{"k": "cap", "x": 500, "y": 300, "t": "Plato · Timaeus and Critias · c. 360 BCE", "in": .3},
                  {"k": "label", "x": 500, "y": 1260, "t": "the first and only ancient source for Atlantis", "st": "small", "in": 1.0}]
    v = View(-32, 30, 22, 48, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("the Pillars of Heracles", -5.35, 36.0, {"c": GOLD}), ("Spartel Bank", -6.0, 35.9, {"c": SCAN, "a": "end", "lx": -18, "ly": 34}),
                          ("Athens", 23.73, 37.98, {}), ("Saïs · the priests' temple", 30.77, 30.96, {"a": "end", "lx": -18}), ("Thera", 25.4, 36.4, {"c": RED, "a": "end", "lx": -18, "ly": 34}), ("Helike", 22.12, 38.22, {"c": RED, "a": "end", "lx": -18, "ly": -22})],
                 extra=[{"k": "label", "x": v.p(-24, 33)[0], "y": v.p(-24, 33)[1], "t": "the Atlantic", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}])
    city = [disc(46, .2, SEA, 1, op=.95), disc(36, .3, "#8aa05a", 2), disc(27, .4, SEA, 3, op=.95), disc(18, .5, "#8aa05a", 4), disc(11, .6, SEA, 5, op=.95), disc(6, .7, "#c9ad85", 6),
            {"t": "box", "x": 0, "z": 0, "y": .7, "w": 4, "d": 3, "h": 3, "c": "#f2dcb4", "edge": "rgba(0,0,0,.3)"},
            {"t": "line", "p": [[46, 1, 0], [70, 1, 0]], "c": "#9fd0ff", "w": 5, "op": .9},
            L_(0, 5, "the temple of Poseidon", GOLD, z=0, dy=-18), L_(58, 1, "a canal to the sea", "#cfe6ff", z=0, dy=-14), L_(0, 1, "rings of land and water · about 5 km", "#f2dcb4", z=50, dy=40)]
    s2 = iso(city, cam=[1, 500, 900], s=6, x=480, y=1000, az=-20, spin=1.2, el=.6, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "the city as Plato describes it", "in": .2}]
    sec = {"base": "section", "tod": "night", "ground": 640, "lx": 130, "layers": [{"d": 0, "c": "#1e3346", "t": "the Atlantic · 4 to 5 km deep"}, {"d": 260, "c": "#3a3530", "t": "young volcanic crust", "tex": "blocks", "to": .1}],
           "cam": [1, 500, 900], "els": [{"k": "line", "p": [[500, 900], [500, 1400]], "c": RED, "w": 3, "in": .4},
                                         {"k": "label", "x": 520, "y": 960, "t": "the Mid-Atlantic Ridge: new sea floor, spreading", "st": "small", "c": "#ffb09a", "a": "start", "in": .7},
                                         {"k": "label", "x": 500, "y": 590, "t": "nowhere to hide a continent", "c": AMBER, "in": 1.1}]}
    s3 = sec
    tl, ax = timeline(-11200, 0, [(-10000, "10,000 BCE"), (-7500, "7500"), (-5000, "5000"), (-2500, "2500")], "Plato's date, and the real drownings", y=980)
    tl["els"] += event(ax, -9700, "the Ice Age cold snap ends", row=1, c=SCAN, i=.3, sub="the seas rise fast") + event(ax, -9600, "Plato's date for Atlantis", row=2, c=GOLD, i=.6) + \
                 event(ax, -1600, "Thera erupts", row=1, c=RED, i=.9) + event(ax, -373, "Helike sinks", row=0, c=RED, i=1.2, sub="in Plato's lifetime")
    s4 = tl
    s5 = quote("In a single day and night of misfortune... the island of Atlantis disappeared in the depths of the sea.", "Plato, Timaeus 25d · Jowett's translation", y=700, size=42)
    s6 = like(s2, cam=[1.2, 480, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 5, ["[d:intrigue][k:ATLANTIS][sfx:boom][act:hushed wonder, the legend]An island ^empire. [act:slow, ominous but calm][tune:fall]Swallowed by the ^sea, in a ^single day and night.",
                      "[d:tension][cam:1.12|0|0][act:leaning in, the catch][tune:fall]And only ^one person ever wrote it down. [act:dry, letting it land][tune:fall]^Nine thousand years later."], cut=False),
        B("world", 0, ["[d:calm][k:THE SOURCE][act:setting the scene, measured][tune:level]^Plato, around {360|three sixty} BCE. [act:reporting his claim, neutral]He says the story came from ^Egyptian priests, through the lawgiver ^Solon. [go:1|0][act:plain fact, a little weight][tune:fall]No ^older text has ever been found. [act:quiet, firm][tune:highfall]Not ^one."]),
        B("collision", 4, ["[d:build][k:THE COINCIDENCE][act:conspiratorial, drawing closer][tune:fall]But here's the ^strange part. [act:careful, precise][tune:fall]Plato puts the war nine thousand years before Solon: about {9600|ninety-six hundred} BCE.",
                           "[d:build][sfx:shimmer][act:the evidence, steady and clear][tune:fall]Geologists date the end of the last Ice Age cold snap to about {9700|ninety-seven hundred} BCE. [act:brisk, vivid][tune:fall]The seas were rising ^fast. [act:genuinely intrigued, slower][tune:fall]That ^is a strange match."]),
        B("cost", 3, ["[d:build][k:THE OCEAN FLOOR][act:changing scene, brisk][tune:fall]Now the ^ocean. [act:explaining, clear and patient]Beyond Gibraltar, the sea floor is ^young volcanic rock, still ^spreading from a ridge down the middle of the Atlantic.",
                      "[d:build][act:plain, firm][tune:fall]There's ^no sunken continent down there. [act:widening the lens, measured][tune:fall]And ^nowhere on Earth, at that date, is there a ^bronze-working empire with ships."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:the reveal, lean in][tune:fall]Plato didn't need to ^invent a drowning. [sfx:hit][act:vivid, telling it straight]In {373|three seventy-three} BCE an ^earthquake and a wave swallowed the Greek city of ^Helike. [act:quiet, pointed][tune:fall]He was ^alive. [act:a knowing nod][tune:fall]He'd have ^heard.",
                          "[d:aside][act:wry, a small smile][tune:fall]Sometimes the ^news writes the myth."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A sunken Atlantic ^empire? [act:the verdict, level-headed][tune:fall]*Ruled ^out*. [act:lighter, one eyebrow up][tune:rise]The ^date? [act:fair-minded, even][tune:fall]A ^coincidence worth ^noticing.",
                     "[d:tension][p:0.93][act:balanced, sincere][tune:fall]The story is ^Plato's. [act:the last word, quiet and sure][tune:fall]The rising ^seas were ^real."]),
    ]
    return EP("atlantis", "04.02", "Atlantis: Plato's Island and the 9600 BCE Coincidence", "atlantis", "debunked", "Was Atlantis a real drowned civilisation?", "Swallowed by the sea in a single *night*.", beats, shots,
              "Plato, Timaeus and Critias, trans. Jowett · Walker et al. 2009 · Gutscher 2005 · Friedrich et al. 2006, Science · Strabo 8.7.2",
              "The only ancient source for Atlantis, the date that lands on the end of the Ice Age, the ocean floor that has no room for it, and the city that really sank in Plato's lifetime.",
              ["#Atlantis", "#Plato", "#IceAge", "#History", "#Mystery"])


# ---------------------------------------------------------------- 04.03 The Bimini Road
def bimini():
    blocks = []
    for i in range(13):
        a = i / 12
        x = -60 + i * 9.5 + (0 if i < 10 else (i - 9) * -2)
        z = (0 if i < 10 else (i - 9) * 7) + math.sin(i * 1.7) * .8
        blocks.append({"t": "box", "x": x, "z": z, "y": 0, "w": 8.4, "d": 6 + (i % 3) * .6, "h": 1.4, "c": "#cdbb95" if i % 2 else "#bfa983", "edge": "rgba(0,0,0,.3)"})
    road = [{"t": "slab", "x0": -66, "x1": 66, "z0": -22, "z1": 36, "y": -.1, "c": "#c9b48c"}] + blocks + \
           [{"t": "person", "x": -20, "y": 3, "z": 10, "h": 1.7}, water(-66, 66, -22, 36, 6.2, op=.18),
            L_(-10, 2, "flat squared blocks · half a mile", GOLD, z=-4, dy=-20), L_(40, 2, "the hook", "#cfe6ff", z=26, dy=-16), L_(-50, 6.2, "5.5 m of clear water", "#cfe6ff", z=-22, dy=-10)]
    s0 = iso(road, cam=[1, 500, 900], s=5.1, x=545, y=960, az=-28, spin=1.2, el=.55, table=None)
    v = View(-81.5, -76.5, 23.5, 27.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("North Bimini", -79.28, 25.77, {"c": GOLD}), ("Miami", -80.19, 25.76, {"a": "end", "lx": -18}), ("Nassau", -77.34, 25.05, {})],
                 extra=[{"k": "label", "x": v.p(-78.2, 24.3)[0], "y": v.p(-78.2, 24.3)[1], "t": "the Great Bahama Bank · dry land in the Ice Age", "st": "small", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    slab = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 16, "prof": [[x0, 0], [x1, 0], [x1, 6], [x0, 6]], "c": "#c9b48c", "edge": "rgba(0,0,0,.35)"} for x0, x1 in ((-46, -24), (-22, -1), (1, 22), (24, 46))] + \
           [{"t": "line", "p": [[-46, 5 - k * 1.3 + .6, 8.2], [46, 5 - k * 1.3 - .6, 8.2]], "c": "#7a6248", "w": 2, "op": .9} for k in range(4)] + \
           [{"t": "cyl", "x": x, "z": 0, "y": 0, "r": 1.2, "h": 6.4, "c": "#e9dccb", "n": 10, "edge": "rgba(0,0,0,.3)"} for x in (-35, -12, 11, 35)] + \
           [L_(0, 7, "the same seaward-dipping layers, block after block", GOLD, z=0, dy=-18), L_(0, 0, "oriented cores · one slab, broken in place", "#cfe6ff", z=10, dy=40)]
    s2 = iso(slab, cam=[1, 500, 900], s=8.6, x=500, y=960, az=-18, spin=1.0, el=.35, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "beachrock, cut open · schematic", "in": .2}]
    s3 = stat("17", "cores", "drilled from neighbouring blocks: the layers inside run on from one block to the next, as in a single slab that cracked", "McKusick & Shinn 1980; Shinn 2004")
    tl, ax = timeline(-14000, 2000, [(-12000, "12,000 BCE"), (-8000, "8000"), (-4000, "4000"), (0, "1 CE")], "The road, and the Ice Age", y=980)
    tl["els"] += event(ax, -9700, "the Ice Age ends", row=1, c=SCAN, i=.3) + \
                 [{"k": "band", "x0": ax.x(-1900), "x1": ax.x(0), "y": 720, "h": 18, "c": GOLD, "t": "the beachrock forms", "in": .7}] + event(ax, 1968, "divers find it", row=2, c=BONE, i=1.1)
    s4 = tl
    s5 = quote("Expect it in '68 and '69.", "Edgar Cayce · a psychic reading, 1940", y=760, size=52)
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:BIMINI · 1968][sfx:boom][act:painting the picture, hushed]Half a mile of flat, ^squared stones. [act:wonder, slowly][tune:fall]A ^road, under the ^sea.",
                      "[d:tension][cam:1.12|0|0][act:intrigued, the coincidence][tune:fall]Found in the ^very year a famous psychic said Atlantis would ^rise."], cut=False),
        B("world", 5, ["[d:calm][k:THE PREDICTION][act:storytelling, even]In {1940|nineteen forty}, Edgar Cayce said part of Atlantis would reappear near ^Bimini. [act:quoting him, lightly][tune:fall]^Expect it in {'68|sixty-eight}, he said. [go:1|0][act:the payoff, measured][tune:fall]In {1968|nineteen sixty-eight}, divers ^found the blocks. [act:a quiet detail][tune:fall]Five and a half metres ^down."]),
        B("collision", 0, ["[d:build][k:THE CASE][act:giving their case fairly][tune:fall]Too neat to be ^natural, say the believers. [act:laying out the evidence, open]^Straight lines, ^square corners, and some blocks seem to sit on smaller stones, like ^props.",
                           "[d:build][act:conceding, fair][tune:fall]And the Bahama banks ^really were dry land in the Ice Age."]),
        B("cost", 2, ["[d:build][k:THE ROCK][act:turning the page, brisk][tune:fall]Now the ^rock. [act:explaining, clear and friendly]It's ^beachrock: beach sand glued by lime in the ^tide zone. [act:the key point, a little delight][tune:fall]It forms ^fast here, and it cracks into squares all by ^itself.",
                      "[d:build][go:3|0][sfx:shimmer][act:the evidence, crisp][tune:fall]Geologists drilled ^seventeen cores. [act:clear, visual, unhurried][tune:fall]The layers inside run on from block to block, like ^one slab broken in ^place."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, the clincher][tune:fall]And the ^dates. [act:precise, steady][tune:level]The shells in it are about ^three and a half ^thousand years old. [act:quick, pointed][tune:fall]The cement, ^younger. [sfx:hit][act:the sting, quiet and firm][tune:fall]The stone didn't ^exist when the Ice Age ended.",
                          "[d:aside][act:warm, a twinkle][tune:fall]The sea is a very good ^bricklayer."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]An Ice Age ^road? [act:the verdict, level-headed][tune:fall]*Ruled out*, by the rock's ^own age. [act:fair, opening a door][tune:rise]People ^reusing the slabs ^later? [act:honest, even][tune:fallrise]^Not ruled out. [act:plain, gently closing it][tune:fall]^Nothing points to it.",
                     "[d:tension][p:0.93][act:the last word, affectionate][tune:fall]A beautiful ^coincidence, laid by the ^sea."]),
    ]
    return EP("bimini", "04.03", "The Bimini Road: Atlantis Pavement or Beachrock?", "bimini-road", "debunked", "Did people build the Bimini Road before the end of the Ice Age?", "A road, under the *sea*.", beats, shots,
              "McKusick & Shinn 1980, Nature · Shinn 2004, 2009 · Gifford & Ball 1980 · Calvert et al. 1979 · Davaud & Strasser 1984",
              "Half a mile of squared stone under the Bahamas, found the year a psychic said Atlantis would rise: seventeen cores and two radiocarbon dates tell the rest.",
              ["#Bimini", "#Atlantis", "#Bahamas", "#Geology", "#Mystery"])


# ---------------------------------------------------------------- 04.04 Yonaguni
def yonaguni():
    steps = [{"t": "box", "x": 0, "z": 0, "y": 0, "w": 60, "d": 40, "h": 7, "c": "#8a7a62", "edge": "rgba(0,0,0,.3)"},
             {"t": "box", "x": -6, "z": -2, "y": 7, "w": 44, "d": 32, "h": 6, "c": "#978670", "edge": "rgba(0,0,0,.3)"},
             {"t": "box", "x": -11, "z": -4, "y": 13, "w": 28, "d": 24, "h": 5, "c": "#a3927a", "edge": "rgba(0,0,0,.3)"},
             {"t": "box", "x": -15, "z": -6, "y": 18, "w": 14, "d": 14, "h": 3, "c": "#b09f86", "edge": "rgba(0,0,0,.3)"},
             {"t": "quad", "p": [[18, 7.05, -18], [24, 7.05, -18], [24, 7.05, 16], [18, 7.05, 16]], "n": [0, 1, 0], "c": "#3a3128", "op": 1, "over": 3},
             {"t": "person", "x": 26, "y": 7, "z": 18, "h": 1.7},
             L_(-15, 21, "flat terraces, sheer walls, right angles", GOLD, z=-6, dy=-22), L_(21, 7, "a 'channel'", "#cfe6ff", z=0, dy=-14), L_(0, 0, "25 m down at the base · 5 m at the top", "#cfe6ff", z=22, dy=40)]
    s0 = iso(steps, cam=[1, 500, 900], s=7, x=510, y=1030, az=-30, spin=1.2, el=.45, table=None)
    v = View(119.5, 129.5, 21.5, 28.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Yonaguni", 123.0, 24.44, {"c": GOLD}), ("Taiwan", 121.0, 23.7, {"a": "end", "lx": -18}), ("Okinawa", 127.7, 26.3, {})],
                 extra=[{"k": "line", "p": [v.p(121.9, 24.0), v.p(122.5, 24.35), v.p(123.0, 24.44)], "c": GOLD, "w": 1.6, "op": .7, "style": "inferred", "curve": True, "in": .8},
                        {"k": "label", "x": v.p(122.2, 23.6)[0], "y": v.p(122.2, 23.6)[1], "t": "225 km by dugout, 2019", "st": "small", "c": GOLD, "in": 1.1}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    sec = {"base": "section", "tod": "dusk", "ground": 640, "lx": 130, "layers": [{"d": 0, "c": "#9a8a70", "t": "Yaeyama sandstone · about 20 million years old"}, {"d": 420, "c": "#6f6250", "t": ""}],
           "cam": [1, 500, 900], "els": [{"k": "line", "p": [[60, 640 + k * 80], [940, 640 + k * 80]], "c": "#5a4e40", "w": 2, "op": .8, "in": .3 + k * .1} for k in range(1, 7)] +
           [{"k": "line", "p": [[x, 640], [x, 1180]], "c": "#3a3128", "w": 2.4, "op": .9, "in": .9 + i * .1} for i, x in enumerate((230, 410, 620, 800))] +
           [{"k": "label", "x": 500, "y": 590, "t": "flat bedding planes + straight vertical joints = steps and right angles", "c": "#ffb09a", "in": 1.2},
            {"k": "label", "x": 500, "y": 1300, "t": "the same shapes stand on the dry coast of the island", "st": "small", "in": 1.5}]}
    s2 = sec
    s3 = stat("225", "km", "paddled from Taiwan to Yonaguni in a replica Stone Age dugout, in 2019, in just over 45 hours", "Kaifu et al. 2025, Science Advances")
    tl, ax = timeline(-32000, 0, [(-30000, "30,000 yrs ago"), (-20000, "20,000"), (-10000, "10,000"), (0, "today")], "People, and the rising sea", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-30000), "x1": ax.x(0), "y": 720, "h": 14, "c": "#c9ad85", "op": .6, "t": "people in the Ryukyu islands", "in": .3}] + \
                 event(ax, -9500, "the base goes under", row=1, c=SCAN, i=.7) + event(ax, -7000, "the top goes under", row=2, c=SCAN, i=1.0)
    s4 = tl
    s5 = like(s0, cam=[1.25, 500, 1000], add=[{"k": "label", "x": 500, "y": 560, "t": "excavated: never", "c": "#ffb09a", "in": .4}])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:YONAGUNI · JAPAN][sfx:boom][act:wonder, setting the scene]Off Japan's last island, giant ^steps go down into the sea. [act:counting them off, slow][tune:level]Flat ^terraces. [act:building][tune:level]Sheer ^walls. [act:landing it][tune:fall]^Right angles.",
                      "[d:tension][cam:1.12|0|0][act:the big mystery, curious][tune:fall]Who ^carved them? [act:hesitant, teasing][tune:level]^Maybe... [act:soft, a knowing smile][tune:fall]^nobody."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:placing it on the map, calm][tune:level]Yonaguni, a hundred and ten kilometres from ^Taiwan. [act:explaining, clear][tune:fall]The formation is ^one piece of bedrock, not blocks: sandstone about twenty ^million years old."]),
        B("collision", 0, ["[d:build][k:THE CASE][act:respectful, giving him his due]A marine geologist, Masaaki Kimura, dived it for decades and mapped a monument: ^terraces, a ^road, a drainage ^channel, even a ^face.",
                           "[d:build][act:laying out the idea, even][tune:fall]Graham Hancock's version: ^nature made the rock, and ^people shaped it while it was still dry land."]),
        B("cost", 2, ["[d:build][k:THE ROCK][act:explaining, hands-on, clear][tune:fall]This sandstone splits along ^flat layers and ^straight cracks. [sfx:shimmer][act:the neat trick, delighted][tune:fall]Flat plus straight gives you ^steps and right angles, for ^free. [act:light, easy][tune:fall]The ^waves do the rest.",
                      "[d:aside][act:lighter, a sideways glance][tune:fall]And the ^dry coast next door has the ^same shapes. [act:dry, gentle][tune:fall]^Nobody claims those were carved."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:the turn, warmer, leaning in][tune:fall]But ^people lived in these islands thirty ^thousand years ago. [go:3|0][act:admiring, vivid][tune:fall]In {2019|twenty nineteen} a team ^paddled a Stone Age dugout here from Taiwan: two hundred and ^twenty-five kilometres.",
                          "[d:build][go:5|0][sfx:hit][act:quiet, pointed][tune:fall]And ^nobody has ever dug the sediment on those terraces. [act:flat, final][tune:highfall]Not ^once."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A ^carved monument? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:warmer, opening a door][tune:rise]^Natural steps that people ^walked on? [act:honest, a little hopeful][tune:fall]^Possible.",
                     "[d:tension][p:0.93][act:the last word, warm and practical][tune:fall]This one gets settled with a ^trowel, not a ^debate."]),
    ]
    return EP("yonaguni", "04.04", "Yonaguni: A Drowned Staircase Off Japan", "yonaguni", "unsupported", "Is the Yonaguni formation a drowned monument?", "Who carved them? Maybe *nobody*.", beats, shots,
              "Ogata et al. 2020 · Kaifu et al. 2025, Science Advances · Schoch 1999 · Hancock 2002 · Kimura 2007 · Lambeck et al. 2014, PNAS",
              "Giant steps and right angles 25 metres under the sea off Japan: what the sandstone does by itself, who lived here while it was dry, and the dig that has never happened.",
              ["#Yonaguni", "#Japan", "#Underwater", "#Mystery", "#Geology"])


# ---------------------------------------------------------------- 04.05 The lost civilisation
def lost_civ():
    v = View(-100, 150, -35, 60, (40, 330, 920, 900))
    sites = [("Göbekli Tepe", 38.92, 37.22), ("Gunung Padang", 107.06, -6.99, "end"), ("Bimini", -79.28, 25.77), ("Yonaguni", 123.0, 24.44, "end"), ("the Eye", -11.39, 21.12), ("Giza", 31.13, 29.98), ("Puma Punku", -68.68, -16.56)]
    sites = [(q + ("start",))[:4] for q in sites]
    s0 = mapshot(v, pins=[(n, lo, la, dict({"c": GOLD if i == 0 else AMBER}, **({"a": "end", "lx": -18} if al == "end" else {}))) for i, (n, lo, la, al) in enumerate(sites)],
                 extra=[{"k": "line", "p": [v.p(lo, la) for n, lo, la, al in sites], "c": GOLD, "w": 1.2, "op": .45, "style": "claimed", "in": 1.6},
                        {"k": "cap", "x": 500, "y": 380, "t": "the map of a civilisation nobody has found", "in": 1.8}], cam=[1, 500, 860])
    tl, ax = timeline(-14000, -8000, [(-14000, "14,000 yrs ago"), (-12000, "12,000"), (-10000, "10,000"), (-8000, "8,000")], "Hancock's timeline, and the evidence", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-12900), "x1": ax.x(-11700), "y": 520, "h": 18, "c": SCAN, "t": "the Younger Dryas · a real climate whiplash", "in": .3}] + \
                 event(ax, -11600, "Göbekli Tepe begins", row=1, c=GOLD, i=.7) + event(ax, -10500, "the first fully domesticated cereals", row=0, c=BONE, i=1.0)
    s1 = tl

    def lst(title, c, items):
        return [{"k": "cap", "x": 500, "y": 500, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": 590 + i * 70, "t": t, "st": "serif", "size": 30, "in": .4 + i * .25} for i, t in enumerate(items)]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": lst("what a civilisation leaves behind", "#ffb09a", ["crops and animals with changed genes", "mines and quarries on dry land", "pottery and tools, everywhere", "pollution in the ice"])}
    s3 = stat("2,000", "years ago", "Roman lead smelting left a signal in Greenland's ice, thousands of kilometres from the mines", "Hong et al. 1994, Science")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": lst("what would change our minds", "#8fd9b0", ["architecture older than 12,900 years", "a domesticated crop older than 12,900 years", "ancient DNA of sudden newcomers", "a confirmed Younger Dryas impact"])}
    s5 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE LOST CIVILISATION][sfx:boom][act:setting the scene, a hint of fun][tune:fall]In {2024|twenty twenty-four}, a writer and an ^archaeologist sat down on the ^biggest podcast on Earth.",
                      "[d:tension][cam:1.12|0|0][act:the hook, quiet intrigue][tune:fall]To argue about a civilisation ^nobody has ever found."], cut=False),
        B("world", 1, ["[d:calm][k:THE IDEA][act:presenting it fairly, even]Graham Hancock's idea: an advanced people, not high-tech but ^wise, wiped out about twelve thousand nine ^hundred years ago. [act:storytelling, measured][tune:fall]^Survivors taught the ^hunters. [go:1|2][act:a touch of grandeur, slower][tune:fall]Then Göbekli ^Tepe rises."]),
        B("collision", 1, ["[d:build][k:WHAT'S REAL][act:generous, meaning it][tune:fall]^Every ingredient is ^real. [sfx:shimmer][act:counting them off, vivid][tune:level]A violent climate ^whiplash. [act:building][tune:level]Coasts drowned by a hundred and ^twenty metres of sea. [act:admiring, warm][tune:fall]Ice Age people who were ^smart, ^artistic, ^seafaring."]),
        B("cost", 2, ["[d:build][k:THE RUBBISH TEST][act:the counterpoint, clear and friendly][tune:fall]Flint Dibble's answer: civilisations leave ^rubbish. [act:ticking them off][tune:level]Crops with changed ^genes. [act:brisk][tune:level]^Mines. [act:rounding it off][tune:fall]Pottery everywhere. [go:3|0][act:a delightful detail, wonder][tune:fall]Greenland's ^ice noticed Roman lead@metal ^smelting, two ^thousand years ago.",
                      "[d:aside][act:light, a small smile][tune:fall]Rome was ^far away. [act:wonder, quiet][tune:fall]The ice ^still noticed."]),
        B("reversal", 2, ["[d:reveal][k:THE TWIST][act:conceding, fair][tune:fallrise]^Some of that can drown. [act:firm, the pivot][tune:highfall]^Genes ^can't. [sfx:hit][act:precise, steady authority][tune:fall]No crop, no animal, no ^people with that signature turns up before about eleven thousand five ^hundred years ago.",
                          "[d:build][act:measured, no gloating][tune:fall]And the theory's two ^pillars, the comet and Gunung Padang, have not ^survived testing."]),
        B("tag", 4, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A lost Ice Age ^civilisation? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:open, genuinely curious][tune:fall]Here's ^exactly what would change our minds.",
                     "[d:tension][p:0.93][go:5|0][act:sincere, looking outward][tune:fall]The coasts where it would be are ^real. [act:the last word, quiet wonder][tune:fall]And almost ^unsearched."]),
    ]
    return EP("lost-civilization", "04.05", "Was There a Lost Ice Age Civilisation?", "lost-civilization", "unsupported", "Did an advanced civilisation flourish in the Ice Age, then vanish?", "A civilisation nobody has *found*.", beats, shots,
              "Hancock 1995, 2015, 2019 · Dibble 2024, SAPIENS · Joe Rogan Experience #2136 · Larson et al. 2014, PNAS · Hong et al. 1994, Science",
              "The most famous debate in alternative history, weighed: every real ingredient of the lost-civilisation idea, the rubbish test it has not yet passed, and the four finds that would change everything.",
              ["#LostCivilization", "#GrahamHancock", "#IceAge", "#Archaeology", "#History"])


# ---------------------------------------------------------------- 04.06 The drowned coasts
def drowned_coasts():
    shelf = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 60, "prof": [[-70, 0], [70, 0], [70, 30], [30, 26], [-10, 12], [-40, 3], [-70, 1]], "c": "#7a6248", "edge": "rgba(255,236,206,.45)"},
             {"t": "flat", "pts": [[-70, -30], [-10, -30], [-10, 30], [-70, 30]], "y": 12.1, "c": SEA, "op": .75, "ground": False, "over": 2},
             {"t": "flat", "pts": [[-70, -30], [-42, -30], [-42, 30], [-70, 30]], "y": 3.1, "c": "#2b5d7d", "op": .8, "ground": False, "over": 1}] + \
            [{"t": "box", "x": x, "z": 6, "y": y, "w": 2.2, "d": 2.2, "h": 1.6, "c": "#c9ad85", "edge": "rgba(0,0,0,.3)"} for x, y in ((-34, 5.5), (-28, 7.5), (-22, 9.3))] + \
            [L_(-40, 4, "Ice Age sea · 120 m lower", "#cfe6ff", z=34, dy=44), L_(-24, 13, "today's sea", "#cfe6ff", z=34, dy=-18), L_(-28, 10, "where people lived", GOLD, z=6, dy=-18)]
    s0 = iso(shelf, cam=[1, 500, 900], s=4.3, x=520, y=900, az=-26, spin=1.6, el=.42, table=None)
    s0["els"] += [{"k": "cap", "x": 500, "y": 420, "t": "the coast, then and now · vertical scale exaggerated", "in": .2}]
    v = View(-15, 125, -15, 62, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Doggerland · the North Sea", 3.0, 54.5, {"c": GOLD}), ("the Blinkerwall · Baltic", 11.9, 54.2, {"a": "start", "ly": 34}), ("Atlit Yam", 34.93, 32.71, {"c": GOLD}),
                          ("the Persian Gulf basin", 51.0, 27.0, {}), ("Madura Strait · Sundaland", 112.8, -7.2, {"c": GOLD})], extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(1000), "t": "1,000 km"}])
    village = [{"t": "slab", "x0": -28, "x1": 28, "z0": -22, "z1": 22, "y": 0, "c": "#a8936e"}] + \
              [{"t": "box", "x": 14 * math.cos(2 * math.pi * k / 7), "z": 14 * math.sin(2 * math.pi * k / 7), "y": 0, "w": 2.4, "d": 1.6, "h": 7 + (k % 3), "c": "#c9ad85", "edge": "rgba(0,0,0,.3)"} for k in range(7)] + \
              [{"t": "cyl", "x": 0, "z": 0, "y": -3, "r": 3, "h": 3.2, "c": "#2a2016", "n": 16, "edge": "rgba(255,236,206,.3)"}, {"t": "person", "x": 24, "y": 0, "z": 14, "h": 1.7},
               L_(0, 10, "seven standing stones around a spring", GOLD, z=0, dy=-26), L_(0, 0, "Atlit Yam · about 8,500 years old · now 10 m under the sea", "#cfe6ff", z=22, dy=40)]
    s2 = iso(village, cam=[1, 500, 900], s=8, x=500, y=1000, az=-24, spin=1.3, el=.5, table=None)
    s3 = stat("971", "metres", "of stones set in a line 21 metres under the Baltic, a Stone Age hunting wall more than 10,000 years old", "Geersen et al. 2024, PNAS")
    tl, ax = timeline(-22000, 0, [(-20000, "20,000 yrs ago"), (-15000, "15,000"), (-10000, "10,000"), (-5000, "5,000"), (0, "today")], "Sea level", y=980)
    pts = [(-22000, -125), (-19000, -120), (-16000, -105), (-14600, -95), (-14300, -78), (-12000, -60), (-10000, -40), (-8000, -18), (-7000, -6), (-4000, -1), (0, 0)]
    tl["els"] += [{"k": "line", "p": [[ax.x(t), 520 - m * 2.1] for t, m in pts], "c": SEA, "w": 5, "curve": True, "in": .3, "fx": "draw", "dur": 2.2},
                  {"k": "label", "x": ax.x(-20500), "y": 770, "t": "−120 m", "st": "small", "c": "#9fd0ff", "a": "start", "in": .6}, {"k": "label", "x": ax.x(-1500), "y": 495, "t": "today's level", "st": "small", "c": "#9fd0ff", "in": 1.2},
                  {"k": "label", "x": ax.x(-14450) + 16, "y": 690, "t": "one pulse: 14–18 m in 350 years", "st": "small", "c": GOLD, "a": "start", "in": 1.6}]
    s4 = tl
    s5 = stat("32", "metres down", "two skull fragments of Homo erectus, dredged from the sea floor between Java and Madura, published in 2025", "Berghuis et al. 2025")
    s6 = like(s1, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE DROWNED COASTS][sfx:boom][act:wonder, drawing them in][tune:level]There's a ^continent's worth of land where Ice Age people ^lived... [act:intimate, a little smile][tune:fall]and you've ^never seen it.",
                      "[d:tension][cam:1.12|0|0][act:the simple reveal, soft][tune:fall]Because it's ^underwater."], cut=False),
        B("world", 4, ["[d:calm][k:THE ICE AGE][act:storytelling, spacious][tune:fall]At the ^coldest point of the last Ice Age, so much water was locked in ice that the sea stood a hundred and twenty metres ^lower.",
                       "[d:build][go:1|0][act:tracing the map, wonder][tune:level]^Britain was joined to ^Europe. [act:moving along][tune:level]^Asia to ^America. [act:one more][tune:level]^Java to ^Borneo. [gap:0.45][act:the turn, lower and slower][tune:fall]Then the ice ^melted."]),
        B("collision", 4, ["[d:build][k:THE PULSE][sfx:shimmer][act:ominous, low][tune:fall]And ^not gently. [act:vivid, gathering pace][tune:fall]In ^one pulse the sea climbed fourteen to eighteen metres in three hundred and ^fifty years. [d:aside][act:quiet, human, picturing it][tune:fall]A few ^generations to watch the beach walk ^inland."]),
        B("cost", 2, ["[d:wonder][k:WHAT'S DOWN THERE][act:tender wonder][tune:fall]And ^people lived there. [act:guiding the eye, unhurried][tune:fall]Off Israel, Atlit Yam: a ^village with seven standing stones around a spring, ten metres ^down.",
                      "[d:build][go:3|0][act:moving on, vivid][tune:level]In the Baltic, nearly a ^kilometre of stones in a line, twenty-one metres ^down. [go:5|0][act:the oldest one, awed][tune:fall]Off Java, skulls of Homo ^erectus, dredged from ^thirty-two metres."]),
        B("reversal", 1, ["[d:reveal][k:THE TWIST][act:candid, leaning in][tune:fall]Here's the ^honest part. [act:plain, careful][tune:fall]Every drowned site found so far matches the tools already known ^inland. [sfx:hit][act:thoughtful, painting it][tune:level]So the missing chapter is probably ^big, ^busy and ^coastal... [act:gentle, firm][tune:fall]not ^high-tech."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]^Important Ice Age sites on the sea floor? [act:the verdict, warm and sure][tune:fall]^*Plausible*. [act:quiet, a call to adventure][tune:fall]And almost ^none of it has been searched.",
                     "[d:tension][p:0.93][act:the last word, a smile in it][tune:fall]The best-kept archive on Earth is ^wet."]),
    ]
    return EP("drowned-coasts", "04.06", "The Drowned Coasts: A Continent's Worth of Lost Land", "drowned-coasts", "plausible", "What human history lies on the drowned Ice Age coasts?", "A continent's worth of land you've never *seen*.", beats, shots,
              "Lambeck et al. 2014, PNAS · Deschamps et al. 2012, Nature · Galili et al. 1993 · Geersen et al. 2024, PNAS · Berghuis et al. 2025 · Gaffney et al. 2007",
              "When the ice melted, the sea rose 120 metres and swallowed the coasts where Ice Age people liked to live: a drowned village, a Stone Age wall under the Baltic, and skulls from the sea floor off Java.",
              ["#IceAge", "#Underwater", "#Archaeology", "#Doggerland", "#History"])


# ---------------------------------------------------------------- 04.07 Stories older than the sea
def aboriginal():
    v = View(112, 155, -44, -9, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("Spencer Gulf", 137.3, -34.0, {"c": GOLD}), ("Kangaroo Island", 137.2, -35.8, {"c": GOLD, "a": "end", "lx": -18}), ("Port Phillip Bay", 144.9, -38.1, {"c": GOLD})],
                 extra=[{"k": "label", "x": 500, "y": 400, "t": "21 places around the coast with stories of the sea coming in", "st": "small", "c": AMBER, "in": 1.2}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}], cam=[1.05, 500, 870])
    isl = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 60, "prof": [[-70, 0], [70, 0], [70, 14], [44, 12], [30, 3], [8, 2], [-6, 9], [-30, 11], [-50, 3], [-70, 1]], "c": "#7a6248", "edge": "rgba(255,236,206,.45)"},
           {"t": "flat", "pts": [[-70, -30], [70, -30], [70, 30], [-70, 30]], "y": 5.1, "c": SEA, "op": .7, "ground": False, "over": 2},
           L_(-20, 12, "Kangaroo Island", GOLD, z=0, dy=-18), L_(56, 14, "the mainland", "#f2dcb4", z=0, dy=-18), L_(18, 5, "the strait · dry until about 10,000 years ago", "#cfe6ff", z=34, dy=40)]
    s1 = iso(isl, cam=[1, 500, 900], s=4.6, x=500, y=960, az=-18, spin=1.4, el=.42, table=None)
    s1["els"] += [{"k": "cap", "x": 500, "y": 420, "t": "schematic · vertical scale exaggerated", "in": .2}]
    s2 = stat("13,070", "years", "the oldest age calculated for a remembered drowning: story, water depth and sea-level curve, put together", "Nunn & Reid 2016, Australian Geographer")
    s3 = stat("300", "generations", "roughly how many tellings separate today from a coast that drowned 7,500 years ago", "Nunn & Reid 2016")
    v2 = View(-135, 150, 20, 55, (40, 330, 920, 900))
    s4 = mapshot(v2, pins=[("Cascadia · the stories", -124.0, 46.5, {"c": GOLD}), ("Japan · the tsunami logs", 140.0, 38.0, {"c": SCAN, "a": "end", "lx": -18})],
                 extra=[{"k": "line", "p": [v2.p(-124.0, 46.5), v2.p(170, 50), v2.p(140.0, 38.0)], "c": SCAN, "w": 1.6, "op": .6, "style": "inferred", "curve": True, "in": .8},
                        {"k": "cap", "x": 500, "y": 390, "t": "January 1700 · one earthquake, two records", "in": .3}])
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:AUSTRALIA][sfx:boom][act:respectful, hushed wonder][tune:fall]All around Australia, the old stories say the ^same thing: the sea came ^in. [act:gentle, clear][tune:fall]Where there's ^water now, there used@to to be ^land.",
                      "[d:tension][cam:1.12|0|0][act:open, curious][tune:level]What if they're ^right... [act:wonder, slowly][tune:rise]and ten ^thousand years old?"], cut=False),
        B("world", 1, ["[d:calm][k:KANGAROO ISLAND][act:with care, sincere storytelling][tune:fall]One story: the ancestral being ^Ngurunderi made the waters rise, and cut the island off from the ^mainland.",
                       "[d:build][act:quietly impressed][tune:fall]^Geology agrees on the ^event. [act:plain, confident][tune:fall]The strait flooded about ten ^thousand years ago."]),
        B("collision", 0, ["[d:build][k:THE METHOD][act:clear, a clever idea coming][tune:fall]A geographer and a ^linguist, Patrick Nunn and Nicholas Reid, took ^twenty-one of these stories. [act:posing it, curious][tune:fall]For each, how ^deep is the water over the land it describes?",
                           "[d:build][go:2|0][sfx:shimmer][act:explaining the trick, bright][tune:fall]Read@present that depth off the sea-level ^curve, and you get a ^date. [act:the result, measured][tune:fall]^Seven thousand to ^thirteen thousand years. [gap:0.4][act:the reveal, slower, awed][tune:fall]Every ^single one inside the window when the seas ^really rose."]),
        B("cost", 3, ["[d:build][k:THE DOUBT][act:fair-minded, raising the doubt][tune:rise]Could each story be a ^later guess, from drowned trees or reefs? [act:honest, even][tune:fallrise]^Possibly. [act:careful, a second caveat][tune:fall]And many were written down by ^colonists, in ^other languages.",
                      "[d:build][act:warm, a little wry][tune:level]Three hundred generations is a long game of ^telephone... [act:the turn, lifting][tune:fall]unless the telling had ^rules. [act:respectful, sure][tune:fall]It ^did: kin who ^checked each telling."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, the evidence][tune:fall]And long memory has been tested ^elsewhere. [sfx:hit][act:vivid, building][tune:fall]Stories on America's Pacific coast of a great shaking match the Japanese record@noun of a tsunami, in January {1700|seventeen hundred}. [gap:0.4][act:quiet astonishment][tune:fall]^Same night."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]The ^oldest memories on Earth? [act:the verdict, warm][tune:fall]^*Plausible*. [act:honest, a careful caveat][tune:fall]^Hard to prove story by ^story.",
                     "[d:tension][p:0.93][act:the last word, tender][tune:fall]Some libraries are made of ^people."]),
    ]
    return EP("aboriginal-sea", "04.07", "Stories Older Than the Sea: Australia's Drowned Coasts", "aboriginal-sea", "plausible", "Can a spoken story remember a coastline that drowned 10,000 years ago?", "What if they're *right*?", beats, shots,
              "Nunn & Reid 2016, Australian Geographer · Nunn 2018, The Edge of Memory · Ludwin et al. 2005 · Lambeck et al. 2014, PNAS",
              "Twenty-one Aboriginal stories of the sea coming in, dated by the depth of the water over the land they describe: possibly the oldest memories anyone has kept by word of mouth.",
              ["#Australia", "#OralHistory", "#IceAge", "#History", "#Science"])


# ---------------------------------------------------------------- 04.08 Dwarka
def dwarka():
    anch = [{"t": "slab", "x0": -46, "x1": 46, "z0": -30, "z1": 30, "y": 0, "c": "#a8936e"}] + \
           [{"t": "prism", "pts": [[x - 3, z - 2], [x + 3, z - 2], [x, z + 3.5]], "y": 0, "h": 1.2, "c": "#c9b48c", "edge": "rgba(0,0,0,.35)"} for x, z in ((-30, -12), (-18, 8), (-6, -20), (8, 14), (20, -6), (34, 10), (-38, 18), (26, 22))] + \
           [{"t": "box", "x": x, "z": z, "y": 0, "w": 7, "d": 4, "h": 2.4, "c": "#bfa983", "edge": "rgba(0,0,0,.3)"} for x, z in ((-12, -4), (-4, -6), (4, -8))] + \
           [{"t": "person", "x": 40, "y": 0, "z": -20, "h": 1.7},
            L_(-6, 3, "dressed blocks", GOLD, z=-6, dy=-18), L_(20, 2, "stone anchors · well over a hundred", "#cfe6ff", z=10, dy=-16), L_(0, 0, "off Dwarka · 3 to 16 m under the sea", "#cfe6ff", z=34, dy=40)]
    s0 = iso(anch, cam=[1, 500, 900], s=7, x=500, y=1000, az=-26, spin=1.3, el=.5, table=None)
    v = View(67.8, 73.2, 19.8, 23.6, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Dwarka", 68.97, 22.24, {"c": GOLD}), ("Bet Dwarka", 69.1, 22.47, {"a": "start", "ly": -22}), ("the Gulf of Khambhat sonar", 72.35, 21.25, {"c": SCAN, "a": "end", "lx": -18}), ("Lothal · a Harappan port", 72.25, 22.52, {"a": "end", "lx": -18})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 140, "y": 480, "w": 720, "h": 620, "fill": "#161a14", "c": "#3a4a30", "sw": 2, "in": .1}] +
          [{"k": "line", "p": [[180 + (i % 5) * 130, 540 + (i // 5) * 120], [260 + (i % 5) * 130, 540 + (i // 5) * 120], [260 + (i % 5) * 130, 600 + (i // 5) * 120], [180 + (i % 5) * 130, 600 + (i // 5) * 120], [180 + (i % 5) * 130, 540 + (i // 5) * 120]],
            "c": "#7fb07a", "w": 1.6, "op": .35 + .1 * (i % 3), "in": .3 + i * .04} for i in range(20)] +
          [{"k": "cap", "x": 500, "y": 430, "t": "side-scan sonar · 30 to 40 m · 2001 · schematic", "in": .2},
           {"k": "label", "x": 500, "y": 1170, "t": "shapes on a screen, never excavated · every find was dredged", "st": "small", "c": "#ffb09a", "in": 1.2}]}
    s3 = stat("7500", "BCE", "a radiocarbon date on a piece of wood dredged from the Gulf of Khambhat: it dates the wood, not a city", "NIOT reports")
    tl, ax = timeline(-8000, 2000, [(-8000, "8000 BCE"), (-5000, "5000"), (-2000, "2000"), (1, "1 CE"), (1500, "1500")], "Dwarka through time", y=980)
    tl["els"] += event(ax, -7500, "the dredged wood", row=1, c=SCAN, i=.3) + event(ax, -1570, "Bet Dwarka, Late Harappan", row=2, c=AMBER, i=.6) + \
                 [{"k": "band", "x0": ax.x(-300), "x1": ax.x(1500), "y": 720, "h": 18, "c": GOLD, "t": "the anchors: a busy harbour", "in": .9}]
    s4 = tl
    s5 = quote("The sea rushed into the city.", "the Mahabharata, Mausala Parva · Ganguli's translation", y=760, size=52)
    s6 = like(s0, cam=[1.18, 500, 1000])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 5, ["[d:intrigue][k:DWARKA · INDIA][sfx:boom][act:respectful, measured storytelling][tune:fall]The Mahabharata says the sea rushed into Krishna's ^golden city and ^swallowed it.",
                      "[d:tension][cam:1.12|0|0][act:intrigued, reporting][tune:fall]Off the coast of Gujarat, divers have found stone ^blocks. [act:adding the surprise, brighter][tune:fall]And more than a hundred ^anchors."], cut=False),
        B("world", 0, ["[d:calm][k:THE DIVES][act:crediting the work, steady][tune:fall]India's oceanographers dived off Dwarka for ^years: dressed blocks, curved walls, anchors, three to ^sixteen metres down. [go:1|0][act:adding, quietly impressed][tune:fall]And on nearby Bet Dwarka, a ^settlement about thirty-five ^hundred years old."]),
        B("collision", 2, ["[d:build][k:THE SONAR][sfx:shimmer][act:intrigue, building][tune:fall]Then, in {2001|two thousand one}, sonar in the Gulf of Khambhat showed ^geometric shapes, ^forty metres down. [go:3|0][act:careful, precise][tune:fall]A dredged piece of wood dated to about {7500|seventy-five hundred} BCE.",
                           "[d:tension][act:awed, then careful][tune:fall]Older than ^any city on Earth. [gap:0.4][act:the caveat, quiet][tune:fallrise]^If it's a city."]),
        B("cost", 4, ["[d:build][k:THE PROBLEM][act:plain, careful][tune:fall]^Nothing at Khambhat was ^excavated. [act:matter of fact][tune:fall]Everything was dredged up ^blind, with ^no layers. [act:simple logic, gentle][tune:fall]And a date on wood dates the ^wood.",
                      "[d:build][act:explaining, clear][tune:fall]Off Dwarka, the anchors are the kinds ^traders used@verb from about two thousand years ago into ^medieval times. [act:vivid, a little wistful][tune:fall]A busy ^harbour, ^eaten by the sea."]),
        B("reversal", 0, ["[d:reveal][k:THE TWIST][act:respectful, the real story][tune:fall]So the sea ^did swallow a Dwarka: a harbour, over ^centuries. [sfx:hit][act:news, brightening][tune:fall]And in {2025|twenty twenty-five}, India's archaeological survey@noun went back ^underwater. [act:open, suspenseful][tune:fall]The results aren't out ^yet."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, respectful and calm][tune:rise]A city from the age of the ^epic, under the sea? [act:the verdict, level-headed][tune:fall]*Awaiting ^discovery*. [act:plain, simple][tune:rise]A ^drowned harbour? [act:firm, simple][tune:highfall]^Real.",
                     "[d:tension][p:0.93][act:the last word, hopeful][tune:fall]The ^next dive report could ^change this card."]),
    ]
    return EP("dwarka", "04.08", "Dwarka: Krishna's City Under the Sea?", "dwarka", "unsupported", "Does a city from the age of the Mahabharata lie under the sea off Gujarat?", "Divers found a hundred *anchors*.", beats, shots,
              "Gaur, Sundaresh & Tripati 2004, Current Science · Rao 1999 · NIOT reports 2001 · ASI 2025 · the Mahabharata, Mausala Parva, trans. Ganguli",
              "Stone blocks and a hundred anchors off Dwarka, geometric shapes on sonar in the Gulf of Khambhat, and what has and has not been excavated.",
              ["#Dwarka", "#India", "#Underwater", "#Archaeology", "#Mahabharata"])


# ---------------------------------------------------------------- 04.09 Rama Setu
def rama_setu():
    shoals = [{"t": "prism", "pts": [[-78, -14], [-58, -16], [-54, 8], [-78, 12]], "y": 0, "h": 5, "c": "#8aa05a", "edge": "rgba(0,0,0,.25)"},
              {"t": "prism", "pts": [[58, -12], [80, -14], [80, 14], [54, 10]], "y": 0, "h": 5, "c": "#8aa05a", "edge": "rgba(0,0,0,.25)"}] + \
             [{"t": "prism", "pts": [[x - 4, -2.2], [x + 4, -2.6], [x + 4.5, 2.4], [x - 3.5, 2.0]], "y": 0, "h": .9, "c": "#e2cf9e", "edge": "rgba(0,0,0,.2)"} for x in range(-48, 50, 9)] + \
             [water(-80, 80, -30, 30, 1.6, op=.22, over=6), {"t": "person", "x": -6, "y": .9, "z": 0, "h": 1.7},
              L_(-66, 6, "India · Pamban", "#f2dcb4", z=0, dy=-16), L_(66, 6, "Sri Lanka · Mannar", "#f2dcb4", z=0, dy=-16), L_(0, 1, "shoals · 1 to 3 m under water", GOLD, z=10, dy=40)]
    s0 = iso(shoals, cam=[1, 500, 900], s=5.2, x=500, y=980, az=-14, spin=1.1, el=.5, table=None)
    s0["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "Adam's Bridge · Rama Setu · schematic", "in": .2}]
    v = View(78.9, 80.3, 8.55, 9.75, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Rameswaram", 79.31, 9.29, {"c": GOLD}), ("Dhanushkodi", 79.42, 9.18, {"a": "start", "ly": 34}), ("Talaimannar", 79.72, 9.1, {"a": "start", "ly": -22}), ("Mannar", 79.9, 8.98, {})],
                 extra=[{"k": "line", "p": [v.p(79.44, 9.17), v.p(79.55, 9.14), v.p(79.64, 9.12), v.p(79.71, 9.1)], "c": GOLD, "w": 3, "op": .8, "in": .8},
                        {"k": "label", "x": v.p(79.55, 9.4)[0], "y": v.p(79.55, 9.4)[1], "t": "Palk Bay", "st": "ital", "c": "#9fd0ff"}, {"k": "label", "x": v.p(79.4, 8.8)[0], "y": v.p(79.4, 8.8)[1], "t": "Gulf of Mannar", "st": "ital", "c": "#9fd0ff"},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(10), "t": "10 km"}])
    sec = {"base": "section", "tod": "day", "ground": 760, "lx": 130, "layers": [{"d": 0, "c": "#e2cf9e", "t": "sand, beachrock and coral"}, {"d": 180, "c": "#8a7452", "t": "older sediments"}],
           "cam": [1, 500, 900], "els": [{"k": "water", "y": 680, "h": 80, "x0": -600, "x1": 1600, "op": .6, "in": .1},
                                         {"k": "line", "p": [[80, 700], [940, 700]], "c": "#9fd0ff", "w": 2, "style": "inferred", "in": .6},
                                         {"k": "label", "x": 500, "y": 640, "t": "laser from orbit, 2024: the ridge carries on from both land tips", "c": AMBER, "in": .8}]}
    s2 = sec
    s3 = stat("48", "km", "the chain of shoals from India's Pamban Island to Sri Lanka's Mannar Island, almost all of it under water", "Dandabathula et al. 2024, Scientific Reports")
    tl, ax = timeline(-9000, 2100, [(-8000, "8000 BCE"), (-5000, "5000"), (-2000, "2000"), (1, "1 CE")], "When could you walk it?", y=980)
    tl["els"] += event(ax, -6500, "the sea floods the strait", row=1, c=SCAN, i=.3, sub="from about 8,500 years ago") + event(ax, 1480, "storms break the last link", row=2, c=GOLD, i=.7, sub="temple records") + \
                 event(ax, 2024, "the laser map", row=0, c=BONE, i=1.0)
    s4 = tl
    s5 = like(s0, cam=[1.18, 500, 960], add=[{"k": "label", "x": 500, "y": 560, "t": "drilled: never", "c": "#ffb09a", "in": .4}])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:RAMA SETU][sfx:boom][act:wonder, setting the scene][tune:fall]A ^line across the sea, forty-eight kilometres long, from India to Sri ^Lanka.",
                      "[d:tension][cam:1.12|0|0][act:respectful, intrigued][tune:fall]^Exactly where the Ramayana says an army built a ^bridge. [act:weighing the options][tune:rise]^Built... [act:gentle, curious][tune:fall]or ^grown?"], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:describing it, calm][tune:fall]Sandbanks and ^shoals, mostly one to ^three metres under water. [go:2|0][act:a modern marvel, bright][tune:fall]In {2024|twenty twenty-four} a NASA laser satellite mapped it from ^orbit: the ridge carries straight on from ^both land tips."]),
        B("collision", 3, ["[d:build][k:WHAT IT'S MADE OF][sfx:shimmer][act:ticking them off, plain][tune:fall]^Sand, ^beachrock and ^coral. [act:explaining, clear and friendly][tune:fall]The meeting of ^two seas piles sand into long ridges like this all over the ^world.",
                           "[d:build][act:respectful, a telling detail][tune:fall]Temple records@noun say storms broke the last walkable link in {1480|fourteen eighty}."]),
        B("cost", 4, ["[d:build][k:THE ICE AGE][act:wonder, spacious][tune:fall]And in the Ice Age, the ^whole strait was dry land, with ^lakes. [act:plain, confident][tune:fall]The sea came in about eight and a half ^thousand years ago. [d:aside][act:playful, delighted by the paradox][tune:risefall]Which makes the bridge older than the ^sea around it."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][sfx:hit][act:leaning in, the missing test][tune:fall]But here's what ^nobody has done: ^drill it. [act:careful, precise][tune:fall]A ^human layer on top of a natural ridge has never been ^tested. [act:fair, even][tune:fall]So it has never been ruled ^out."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, respectful and calm][tune:rise]A bridge built by an ^army? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:plain, simple][tune:rise]A ^natural ridge? [act:calm, confident][tune:fall]That's what ^every survey@noun shows.",
                     "[d:tension][p:0.93][act:with respect, sincere][tune:fall]The ^epic is not what we rate. [act:the last word, gentle and clear][tune:fall]The ^ridge is."]),
    ]
    return EP("rama-setu", "04.09", "Rama Setu: A Bridge Built by an Army or by the Sea?", "rama-setu", "unsupported", "Is Adam's Bridge a human-made causeway?", "Built... or *grown*?", beats, shots,
              "Dandabathula et al. 2024, Scientific Reports · Dubey et al. 2023, Quaternary Research · the Ramayana, trans. Griffith · Supreme Court of India, 2007",
              "Forty-eight kilometres of shoals between India and Sri Lanka, mapped by laser from orbit in 2024: what the ridge is made of, when you could walk it, and the test nobody has run.",
              ["#RamaSetu", "#India", "#SriLanka", "#Geology", "#Ramayana"])


# ---------------------------------------------------------------- 04.10 The ledger
def _ledger_text():
    v = View(-100, 150, -45, 62, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("the Eye", -11.39, 21.12, {"c": GOLD}), ("Bimini", -79.28, 25.77, {}), ("Yonaguni", 123.0, 24.44, {"a": "end", "lx": -18}), ("Dwarka", 68.97, 22.24, {"a": "end", "lx": -18}),
                          ("Rama Setu", 79.5, 9.1, {"a": "start", "ly": 34}), ("Atlit Yam", 34.93, 32.71, {"a": "end", "lx": -18}), ("Kangaroo Island", 137.2, -35.8, {"a": "end", "lx": -18})], cam=[1, 500, 860])

    def grp(title, c, items):
        return [{"k": "cap", "x": 500, "y": 520, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": 600 + i * 64, "t": t, "st": "serif", "size": 30, "in": .4 + i * .2} for i, t in enumerate(items)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["the sea rose 120 metres", "real villages and walls on the sea floor", "the Eye is natural rock", "Bimini is beachrock"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible", "#e8b87a", ["important sites lost on the drowned coasts", "stories that remember the rising sea", "people walking on Yonaguni's steps"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["a lost Ice Age civilisation", "a carved monument at Yonaguni", "Krishna's city under the sea", "a bridge built across the strait"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["Atlantis in the Atlantic", "Atlantis in the Eye", "an Ice Age road at Bimini"])}
    s5 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:DROWNED WORLDS][sfx:boom][act:inviting, a storyteller's opening][tune:fall]^Nine places where the sea is said to hide a lost ^world. [act:brisk, rolling up sleeves][tune:fall]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:plain, confident][tune:fall]The sea ^really rose a hundred and ^twenty metres. [act:steady, naming what's solid][tune:fall]^Real villages and ^walls lie on the sea floor. [act:gentle, a small smile][tune:fall]And two famous ^'ruins', the Eye and Bimini, are ^natural rock."]),
        B("collision", 2, ["[d:build][k:PLAUSIBLE][act:warmer, the open possibilities][tune:level]^Important Ice Age sites, lost on the drowned ^coasts. [act:with care][tune:level]Stories that may ^remember the rising sea. [act:wonder, rounding it off][tune:fall]People ^walking on Yonaguni's steps while they were ^dry."]),
        B("cost", 3, ["[d:build][k:AWAITING EVIDENCE][act:ticking them off, even][tune:level]A lost ^civilisation. [act:steady][tune:level]A ^carved monument. [act:respectful][tune:level]Krishna's ^city. [act:the last one][tune:fall]A bridge built by an ^army. [d:aside][act:reassuring, warm][tune:fall]^Waiting is not ^losing. [act:light, encouraging][tune:fall]It means ^nobody has ^dug yet."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:crisp, crossing them off][tune:level]Atlantis in the ^Atlantic. [act:crisp][tune:level]Atlantis in the ^Eye. [act:final, firm][tune:fall]An Ice Age ^road at Bimini."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:calm authority, warm][tune:fall]The drowned world is ^real. [go:5|1.5][act:wonder, looking out][tune:fall]Most of it is still ^unsearched. [act:gentle, turning it over][tune:fallrise]That's not a ^disappointment. [gap:0.45][act:bright, sincere, the heart of it][tune:fall]That's an ^invitation.",
                     "[d:tension][p:0.93][act:the last word, quiet and certain][tune:fall]^Coherence is the ^measure. [act:soft, precise][tune:fall]Not ^final demonstration."]),
    ]
    return EP("drowned-ledger", "04.10", "Drowned Worlds · The Ledger", "", "mixed", "What stands, what waits, and what the sea never hid.", "Here's the *ledger*.", beats, shots,
              "Every source in the nine case files of File 04",
              "The verdicts of Drowned Worlds in one ledger: what is established, what is plausible, what waits under the sea, and what is ruled out.",
              ["#History", "#Atlantis", "#Underwater", "#Archaeology", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: a cabinet of the nine drowned places (see cabinet.py). The sea rises in every niche."""
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    C = Cabinet([
        {"name": "Drowned coasts", "model": mdl(drowned_coasts())},
        {"name": "The Eye", "model": mdl(richat())},
        {"name": "Bimini", "model": mdl(bimini())},
        {"name": "Sea stories", "model": mdl(aboriginal())},
        {"name": "Yonaguni", "model": mdl(yonaguni())},
        {"name": "Lost civilisation", "model": mdl(lost_civ(), 0)},
        {"name": "Dwarka", "model": mdl(dwarka())},
        {"name": "Rama Setu", "model": mdl(rama_setu())},
        {"name": "Atlantis", "model": mdl(atlantis())},
    ])
    C.build()
    DC, EY, BI, AB, YO, LC, DW, RS, AT = range(9)
    rise = [e for i in range(9) for e in C.sea(i, at=.3 + .09 * i)] + [
        {"k": "arrow", "p": [[986, C.Y1], [986, C.Y1 - 330]], "c": "#9fd0ff", "w": 3, "fx": "draw", "dur": 1.8, "in": .3},
        {"k": "label", "x": 940, "y": C.Y0 - 44, "t": "sea level +120 m", "a": "end", "st": "small", "c": "#9fd0ff", "size": 34, "scl": True, "in": 1.6}]
    s1 = C.step(C.cam_all(), rise)
    s2 = C.step(C.cam_cell(DC), C.verdict(DC, "established", at=.4) + C.note(DC, "villages and walls on the sea floor", at=.9))
    s3 = C.step(C.cam_cells([EY, BI]), C.verdict(EY, "established", "natural", .3) + C.verdict(BI, "established", "natural", .7) +
                C.note(EY, "rock rings, not ruins", at=1.0) + C.note(BI, "beachrock, not a road", at=1.3))
    s4 = C.step(C.cam_cell(DC), C.verdict(DC, "plausible", "sites offshore", .4, frame=False) + C.note(DC, "Ice Age sites, lost on the shelf", at=.9))
    s5 = C.step(C.cam_cell(AB), C.verdict(AB, "plausible", at=.4) + C.note(AB, "stories of the rising sea", at=.9))
    s6 = C.step(C.cam_cell(YO), C.verdict(YO, "plausible", "walked", .4) + C.people(YO, 3, at=.8))
    s7 = C.step(C.cam_cell(LC), C.verdict(LC, "awaiting", at=.3))
    s8 = C.step(C.cam_cell(YO), C.verdict(YO, "awaiting", "carved?", .3, frame=False) + C.question(YO, dx=C.w * .30, dy=-100, at=.6, size=70, c=VCOL["awaiting"]))
    s9 = C.step(C.cam_cell(DW), C.verdict(DW, "awaiting", at=.3))
    s10 = C.step(C.cam_cell(RS), C.verdict(RS, "awaiting", at=.3))
    s11 = C.step(C.cam_cells([YO, LC, DW, RS]))
    s12 = C.step(C.cam_cells([YO, LC, DW, RS]), [e for k, i in enumerate((LC, DW, RS)) for e in C.question(i, dx=C.w * .28, dy=-150, at=.2 + .25 * k, size=70, c=VCOL["awaiting"])])
    s13 = C.step(C.cam_cell(AT), C.verdict(AT, "ruled", at=.2) + C.struck(AT, "Atlantic island", at=.4))
    s14 = C.step(C.cam_cell(EY), C.verdict(EY, "ruled", at=.2) + C.struck(EY, "Atlantis", at=.4))
    s15 = C.step(C.cam_cell(BI), C.verdict(BI, "ruled", at=.2) + C.struck(BI, "Ice Age road", at=.4))
    s16 = C.step(C.cam_all())
    s17 = C.step(C.cam_all(), [e for i in range(9) for e in C.wash(i, "#3f86a8", at=.2 + .08 * i, op=.10)])
    s18 = C.step(C.cam_all(k=.94, sy=730), [e for i in range(9) for e in C.wash(i, "#f2b36b", at=.2 + .08 * i, op=.10)])
    s19 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5, (0, 2): "%d|1.1" % s6}),
        3: (s7, {(0, 1): "%d|1.0" % s8, (0, 2): "%d|1.0" % s9, (0, 3): "%d|1.0" % s10, (0, 4): "%d|1.4" % s11, (0, 5): "%d|.5" % s12}),
        4: (s13, {(0, 1): "%d|1.0" % s14, (0, 2): "%d|1.0" % s15}),
        5: (s16, {(0, 1): "%d|.8" % s17, (0, 3): "%d|.8" % s18, (1, 0): "%d|4" % s19}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def lost_civ_m():
    """The lost civilisation as one continuous take (see mural.py): the idea, its real ingredients, the rubbish test, and what would change our minds."""
    from mural import remix
    import illus as I
    ep = lost_civ()
    pod = [I.box(180, 1230, 640, 190, "rgba(18,13,10,.85)", "#8a6a48", 2, 16, .2), I.box(300, 1350, 400, 16, "#5a4330", r=3, at=.3),
           I.person(360, 1350, 110, .4), I.person(640, 1350, 110, .5), I.line([[400, 1330], [420, 1300]], .6, "#cbd2d8", 4), I.line([[600, 1330], [580, 1300]], .6, "#cbd2d8", 4)]
    idea = [I.box(160, 1150, 200, 150, "none", I.LILAC, 3, 4, .8, style="claimed"), {"k": "poly", "p": [[160, 1150], [260, 1080], [360, 1150]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": .9},
            I.line([[520, 1020], [320, 1180]], 4.0, "#ffcf8a", 5, dur=.4), I.glow(300, 1200, 160, 4.3, .9, "fire"),
            I.arrow([[380, 1240], [520, 1300], [600, 1310]], 6.4, I.LILAC, 3, "claimed", .8)] + [I.person(640 + 50 * k, 1380, 80, 6.8 + .15 * k) for k in range(3)] + \
           [{"k": "tpillar", "x": 860, "y": 1380, "h": 150, "in": 9.0, "fx": "rise"}]
    real = [I.line([[140, 380], [200, 320], [230, 440], [270, 300], [300, 420]], .3, I.BLUE, 4, dur=.8), I.box(380, 300, 140, 140, "none", "#8a6a48", 2, 4, 2.4),
            I.box(384, 360, 132, 76, "#3f86a8", r=2, at=2.6, fx="fill", dur=1.0)] + [I.person(640 + 70 * k, 440, 110, 5.0 + .4 * k) for k in range(3)] + \
           [I.box(645, 300, 40, 50, "#b0503a", r=10, at=5.6), {"k": "boat", "x": 860, "y": 450, "w": 110, "in": 6.4}]
    rub = {"base": "section", "ground": 700, "tod": "day", "layers": [{"d": 0, "c": "#7a6248", "t": ""}, {"d": 380, "c": "#5f4c39", "t": ""}], "cam": [1, 500, 900], "els":
           [{"k": "poly", "p": [[200, 700], [500, 560], [800, 700]], "fill": "#8a7a66", "c": "none", "w": 0, "in": .3, "fx": "rise"}] +
           [I.line([[300 + 20 * k, 700], [300 + 20 * k, 620 - 10 * (k % 2)]], 2.4 + .05 * k, "#e8c35a", 3) for k in range(5)] +
           [I.line([[640, 700], [640, 1000], [700, 1000]], 3.6, "#cbbca8", 6), {"k": "poly", "p": [[600, 640], [680, 640], [640, 600]], "fill": "#cbd2d8", "c": "none", "w": 0, "in": 3.6}] +
           [I.tri(250 + 60 * (k % 9), 760 + 50 * (k // 9), 14, 30 * k, "#c8743c", 4.4 + .05 * k) for k in range(18)]}
    core = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(600, 520, 160, 800, "#e6f0f7", "#9fd0ff", 2, 12, .2)] +
            [I.line([[605, 540 + 26 * k], [755, 540 + 26 * k]], .3 + .02 * k, "#b8d4e6", 2, draw=False) for k in range(30)] +
            [I.box(602, 780, 156, 26, I.RED, r=4, at=1.6, fx="pop"), I.glow(680, 793, 90, 1.6, .7),
             I.box(140, 1080, 140, 100, "#6b3a2a", "#c8743c", 2, 6, 3.0), I.glow(210, 1060, 90, 3.2, .8, "fire"),
             I.arrow([[280, 1080], [440, 900], [590, 800]], 3.8, I.RED, 3, "inferred", 1.2)]}
    drown = [I.box(160, 820, 680, 130, "#3f86a8", r=4, at=.3, op=.45, fx="fill", dur=1.2)] + \
            [I.line([[440 + 9 * k, round(360 + 18 * math.sin(k * .6 + ph), 1)] for k in range(14)], 2.0, I.GREEN, 4, dur=.8) for ph in (0, math.pi)] + [I.glow(500, 360, 110, 2.2, .7)] + \
            [I.line([[250, 1050], [250, 1200]], 7.6, "#cbbca8", 10), I.strike(200, 1220, 320, 1040, 8.4), {"k": "tpillar", "x": 750, "y": 1220, "h": 150, "in": 7.8}, I.strike(690, 1230, 820, 1060, 8.8)]
    minds = {"base": "dark", "cam": [1, 500, 900], "els": sum([[I.box(150 + 190 * k, 800, 150, 170, "none", I.BLUE, 3, 10, 1.6 + .5 * k, style="inferred"), I.label(225 + 190 * k, 1020, t, 1.8 + .5 * k, I.BLUE, 26)]
                                                              for k, t in enumerate(("a building", "a crop", "DNA", "an impact"))], []) +
             [{"k": "tpillar", "x": 225, "y": 950, "h": 110, "in": 1.8}] + [I.line([[415 + 12 * j, 950], [415 + 12 * j, 840 - 8 * (j % 2)]], 2.3, "#e8c35a", 3) for j in range(5)] +
             [I.line([[570 + 8 * k, round(885 + 20 * math.sin(k * .6 + ph), 1)] for k in range(14)], 2.8, I.GREEN, 3, dur=.6) for ph in (0, math.pi)] +
             [I.ring(795, 890, 50, 3.3, "#c8743c", 4), I.label(500, 1120, "older than 12,900 years", 4.0, I.BONE, 30)]}
    return remix(ep, scenes={2: rub, 3: core, 4: minds}, alias={5: 0}, cams={5: [1.15, 500, 880], 1: [1.1, 500, 880]}, drop=("para", "num", "title", "q", "cap"),
                 adds={0: pod}, beat_adds={1: (idea, None), 2: (real, None), 4: (drown, None)})

# ---------------------------------------------------------------- the mural versions (one continuous take each, see mural.py)
def _iso_relabel(sh, names, drop=("cap",), spin=None):
    """A copy of an iso shot with its long model labels shortened (names: old text -> new text), and its caption cards gone."""
    import copy
    s = copy.deepcopy(sh)
    s["els"] = [e for e in s["els"] if e.get("k") not in drop]
    for e in s["els"]:
        if e.get("k") == "iso":
            if spin is not None:
                e["spin"] = spin
            for it in e["items"]:
                if it.get("t") == "label" and it.get("text") in names:
                    it["text"] = names[it["text"]]
            e["items"] = [it for it in e["items"] if not (it.get("t") == "label" and not it.get("text"))]
    return s


def _pins_relabel(sh, names, drop=("cap",)):
    """A copy of a map shot with long pin and place labels shortened (names: old text -> new text; '' removes the element)."""
    import copy
    s = copy.deepcopy(sh)
    out = []
    for e in s["els"]:
        if e.get("k") in drop:
            continue
        if e.get("t") in names:
            if not names[e["t"]]:
                continue
            e["t"] = names[e["t"]]
        out.append(e)
    s["els"] = out
    return s


def _tick(x, y, at, c="#8fd9b0", s=1.0):
    """A check mark that draws itself."""
    return {"k": "line", "p": [[x - 16 * s, y], [x - 4 * s, y + 13 * s], [x + 20 * s, y - 16 * s]], "c": c, "w": 6, "fx": "draw", "dur": .45, "in": at}


def _heart(x, y, s, at, c="#ff8a7a"):
    pts = [[0, .42], [-.5, -.05], [-.42, -.42], [-.12, -.42], [0, -.2], [.12, -.42], [.42, -.42], [.5, -.05]]
    return {"k": "poly", "p": [[round(x + s * a, 1), round(y + s * b, 1)] for a, b in pts], "fill": c, "c": "none", "w": 0, "curve": True, "in": at, "fx": "pop"}


def _rings(cx, cy, scale, at, step=.12, rot=None):
    """Plato's ring city in plan: three rings of water, two of land, an island (radii in units of `scale`)."""
    out = []
    for k, (r, c) in enumerate(((2.8, SEA), (2.3, "#8aa05a"), (1.8, SEA), (1.3, "#8aa05a"), (.8, SEA))):
        out.append({"k": "circle", "x": cx, "y": cy, "r": round(r * scale, 1), "fill": "none", "c": c, "w": round(.5 * scale, 1), "in": round(at + step * k, 2), "fx": "draw", "dur": .7})
    out.append({"k": "circle", "x": cx, "y": cy, "r": round(.55 * scale, 1), "fill": "#d9b98a", "c": "none", "w": 0, "in": round(at + step * 5, 2), "fx": "pop"})
    return out


def _dino(x, y, s, at, c="#cbbca8"):
    """A long-necked dinosaur in profile, facing right (feet on y, s = body length in px)."""
    pts = [[-.62, -.30], [-.40, -.36], [-.22, -.48], [.08, -.50], [.24, -.44], [.36, -.62], [.46, -.92], [.54, -1.02], [.62, -.98], [.56, -.90],
           [.48, -.66], [.40, -.38], [.30, -.30], [.30, 0], [.20, 0], [.18, -.22], [-.06, -.22], [-.08, 0], [-.18, 0], [-.20, -.26], [-.40, -.30], [-.62, -.30]]
    return {"k": "poly", "p": [[round(x + s * a, 1), round(y + s * b, 1)] for a, b in pts], "fill": c, "c": "none", "w": 0, "in": at, "fx": "rise"}


def _pillars(x, y, h, at, c="#e6d6b2"):
    """Two columns and a lintel: the Pillars of Heracles (schematic)."""
    w = h * .16
    return [{"k": "rect", "x": x, "y": y - h, "w": w, "h": h, "r": 3, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"},
            {"k": "rect", "x": x + h * .55, "y": y - h, "w": w, "h": h, "r": 3, "fill": c, "c": "none", "sw": 0, "in": at + .15, "fx": "rise"},
            {"k": "rect", "x": x - w * .3, "y": y - h - w * .5, "w": h * .55 + w * 1.6, "h": w * .5, "r": 2, "fill": c, "c": "none", "sw": 0, "in": at + .3, "fx": "pop"}]


def _phone(x, y, at, eye=True):
    """A phone screen with the Eye on it, and a heart."""
    out = [{"k": "rect", "x": x - 62, "y": y - 104, "w": 124, "h": 208, "r": 20, "fill": "#17202a", "c": "#cbd2d8", "sw": 3, "in": at, "fx": "pop"}]
    if eye:
        out += [{"k": "circle", "x": x, "y": y - 10, "r": r, "fill": "none", "c": AMBER, "w": 4, "in": at + .2, "fx": "draw", "dur": .4} for r in (40, 27, 14)]
    return out + [_heart(x + 50, y - 96, 42, at + .6)]


def richat_m():
    """The Eye of the Sahara as one continuous take (see mural.py): Plato's rings drawn, eight cities across the Eye, a dome cut open, a blister sanded down."""
    from mural import remix
    import illus as I
    ep = richat()
    eye = _iso_relabel(ep["shots"][0], {"the Richat Structure · about 40 km across": "the Eye · 40 km across", "three rings of hard, tilted rock": "rings of hard rock"}, spin=.2)
    scale = _iso_relabel(ep["shots"][2], {"Plato's ring city · about 5 km": "Plato's city · 5 km", "the Eye · about 40 km": "the Eye · 40 km"}, spin=.2)
    wmap = _pins_relabel(ep["shots"][1], {"Gibraltar · the Pillars of Heracles": "Gibraltar"})
    # hook, line 2: millions online say it's Atlantis
    online = _phone(250, 440, .3) + _phone(500, 420, .9) + _phone(750, 440, 1.5) + [I.label(500, 630, "Atlantis?", 2.4, I.LILAC, 46, st="serif", fx="pop")]
    # 5 · Plato's words, drawn: rings of land and water around an island, beyond the Pillars of Heracles
    plato = {"base": "dark", "cam": [1, 500, 880], "els": [I.person(190, 640, 190, .3), I.glow(190, 560, 140, .3, .35),
             I.box(232, 520, 92, 120, "#e9d6ad", "#8a6a3e", 2, 6, .6), I.label(190, 700, "Plato", .7, I.BONE, 32)]
             + [I.line([[244, 548 + 18 * k], [312, 548 + 18 * k]], .8 + .05 * k, "#8a6a3e", 3, dur=.3) for k in range(5)]
             + [{"k": "circle", "x": 580, "y": 930, "r": r, "fill": "none", "c": c, "w": 50, "in": at, "fx": "draw", "dur": .9}
                for r, c, at in ((130, "#8aa05a", 3.5), (230, "#8aa05a", 3.75), (80, SEA, 4.05), (180, SEA, 4.25), (280, SEA, 4.45))]
             + [I.dot(580, 930, 55, "#d9b98a", 4.9), I.glow(580, 930, 360, 5.4, .25)]
             + _pillars(150, 1390, 150, 6.4) + [I.arrow([[260, 1300], [330, 1250], [370, 1180]], 7.0, I.AMBER, 3, "claimed", .8),
                                                 I.label(205, 1440, "Pillars of Heracles", 6.8, I.BONE, 28, "start")]}
    # 1 · the map: the Atlantic, then three ticks for the Eye
    v = View(-18, -2, 15, 36.5, (40, 330, 920, 900))
    ex, ey = v.p(-11.39, 21.12)
    cx, cy = v.p(-16.6, 21.3)
    atlas = [v.p(lo, la) for lo, la in ((-9.6, 29.9), (-8.5, 30.2), (-7.4, 30.45), (-6.3, 30.65), (-5.2, 30.8), (-4.1, 30.9))]
    mapadd = [I.label(v.p(-16.8, 25.5)[0], v.p(-16.8, 25.5)[1], "Atlantic", .3, I.BLUE, 40, st="ital"),
              I.ring(ex, ey, 46, 2.4, I.AMBER, 3), I.ring(ex, ey, 30, 2.6, I.AMBER, 3), _tick(ex + 70, ey - 40, 3.4),
              I.arrow([[ex - 30, ey + 4], [(ex + cx) / 2, ey + 22], [cx + 14, cy]], 4.4, I.BLUE, 3, "inferred", .8), _tick(cx + 10, cy + 60, 5.2)] + \
             [I.tri(x, y - 6, 16, 0, "#c9ad85", 6.0 + .1 * k) for k, (x, y) in enumerate(atlas)] + [_tick(atlas[-1][0] + 50, atlas[-1][1] + 6, 8.9)] + \
             [I.glow(ex, ey, 160, 9.6, .45)]
    # 3 · eight of Plato's cities across the Eye; and the Eye high in the desert, far from the sea
    eight = {"base": "dark", "cam": [1, 500, 860], "els": [I.oval(500, 640, 360, 360, "rgba(201,163,112,.16)", "none", 0, 1, .2),
             I.ring(500, 640, 360, .2, "#c9a370", 5), I.ring(500, 640, 262, .4, "#a07a50", 4), I.ring(500, 640, 164, .6, "#c9a370", 4),
             I.label(500, 248, "the Eye", .5, I.AMBER, 34)]
             + sum([_rings(185 + 90 * k, 640, 15.5, 1.2 + .32 * k, .03) for k in range(8)], [])
             + [I.line([[140, 1030], [860, 1030]], 4.0, I.AMBER, 3), I.line([[140, 1015], [140, 1045]], 4.0, I.AMBER, 3, draw=False), I.line([[860, 1015], [860, 1045]], 4.0, I.AMBER, 3, draw=False),
                I.label(500, 1085, "40 km", 4.2, I.AMBER, 34), I.label(185, 570, "5 km", 1.4, I.BLUE, 30)]
             + [{"k": "poly", "p": [[60, 1330], [230, 1330], [330, 1300], [460, 1250], [600, 1215], [940, 1205], [940, 1420], [60, 1420]], "fill": "#8a6a48", "c": "#c9ad85", "w": 2, "in": 5.0, "fx": "rise"},
                I.box(60, 1318, 175, 30, SEA, r=4, at=5.1, op=.85), I.label(130, 1300, "sea", 5.2, I.BLUE, 28),
                I.ring(800, 1190, 30, 5.6, I.AMBER, 4), I.ring(800, 1190, 16, 5.7, I.AMBER, 3), I.glow(800, 1190, 90, 5.7, .6),
                I.arrow([[230, 1400], [790, 1400]], 6.4, I.BONE, 3, dur=1.0, curve=False), I.label(510, 1370, "hundreds of km", 6.7, I.BONE, 30)]
             + [{"k": "circle", "x": 800, "y": 1080, "r": r, "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": 8.0} for r in (40, 26, 12)] + I.question(880, 1100, 8.3, 64)}
    # 4 · the Eye cut open: layers pushed up into a dome, the top shaved off by the wind; the cut edges are the rings
    S, BOT, X0, X1, CX = 820, 1180, 100, 900, 500
    apex = [600, 660, 720, 780, 860, 940]
    kq = (S - apex[0]) / 330 ** 2
    yb = lambda k, x: apex[k] + kq * (x - CX) ** 2
    cols = ["#d9b98a", "#7a6248", "#e6cfa6", "#8c6a48", "#cdb48e", "#6f5a44", "#a08060"]
    bands = []
    for k in range(-1, 6):                                  # band k lies between boundary k and k+1 (-1: the surface layer, 5: the core)
        segs, cur = [], []
        for x in range(X0, X1 + 1, 8):
            top = S if k < 0 else max(S, yb(k, x))
            bot = BOT if k == 5 else min(BOT, yb(k + 1, x))
            if top < bot - .5:
                cur.append((x, top, bot))
            elif cur:
                segs.append(cur); cur = []
        if cur:
            segs.append(cur)
        for sg in segs:
            p = [[x, round(t, 1)] for x, t, b in sg] + [[x, round(b, 1)] for x, t, b in reversed(sg)]
            bands.append({"k": "poly", "p": p, "fill": cols[k + 1], "c": "none", "w": 0, "in": round(1.0 + .25 * (5 - k), 2), "fx": "fill", "dur": .8})
    ghost = []
    for k in range(4):
        d = math.sqrt((S - apex[k]) / kq)
        ghost.append(I.line([[round(x, 1), round(yb(k, x), 1)] for x in [CX - d + 2 * d * j / 24 for j in range(25)]], 4.5 + .25 * k, I.BONE, 3, "inferred", 1.2, curve=True, op=.6))
    cross = [math.sqrt((S - apex[k]) / kq) for k in range(4)]
    plan = []
    for k, d in enumerate(cross):
        plan += [{"k": "line", "p": I.ellipse(CX, 420, d * .7, d * .24, 40), "c": cols[k + 1] if k % 2 == 0 else "#b8905e", "w": 7, "curve": True, "in": round(7.7 + .35 * k, 2), "fx": "draw", "dur": .7}]
        plan += [I.line([[CX - d, S], [CX - d * .7, 420]], 7.9 + .35 * k, I.AMBER, 2, "inferred", .5, op=.7), I.line([[CX + d, S], [CX + d * .7, 420]], 7.9 + .35 * k, I.AMBER, 2, "inferred", .5, op=.7)]
    wind = [I.arrow([[40, y], [300, y - 14], [620, y + 8], [960, y - 6]], 6.0 + .3 * j, "#cfe6ff", 3, "known", 1.1) for j, y in enumerate((800, 750, 700))]
    dome = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(X0, S, X1 - X0, BOT - S, "none", "#f5ecdc", 2, 2, .3, fx="draw")] + bands +
            [I.line([[X0, S], [X1, S]], .3, "#ffe2be", 3, dur=.8), I.arrow([[CX, BOT - 10], [CX, 900]], 4.0, I.BONE, 4, dur=.7, curve=False)] + ghost + wind + plan +
            [I.label(CX, 300, "seen from above", 7.6, I.AMBER, 30)] +
            [I.arrow([[x, BOT - 30], [x, BOT + 40]], 11.8, I.AMBER, 3, dur=.4, curve=False) for x in (150, 850)]}
    # beat 4, line 2: older than the dinosaurs, by a few hundred million years
    X = lambda ma: 120 + 760 * (1000 - ma) / 1000
    deep = [I.line([[100, 1330], [900, 1330]], .2, "#8c7152", 3), I.box(X(1000), 1318, X(450) - X(1000), 24, I.AMBER, r=12, at=2.0, fx="pop"),
            I.label(X(725), 1300, "these rocks", 2.4, I.AMBER, 30), _dino((X(230) + X(66)) / 2, 1318, 120, 5.0), I.box(X(230), 1322, X(66) - X(230), 16, "#cbbca8", r=8, at=5.0, op=.7),
            I.label(X(1000), 1385, "1,000 million years ago", 1.0, "#cbbca8", 28, "start"), I.label(X(0), 1385, "today", 1.0, "#cbbca8", 28, "end"),
            I.arrow([[X(450), 1250], [X(340), 1215], [X(230), 1250]], 6.0, I.BONE, 3, dur=.8)]
    # beat 5: not a crater; molten rock below, hot water in the centre, the wind
    craterx = [I.line(I.ellipse(845, 300, 80, 40, 20, 0, 180), .6, "#cbbca8", 5, dur=.5, curve=True), I.line([[755, 300], [935, 300]], .6, "#8c7152", 3, draw=False),
               I.dot(905, 205, 14, "#cbbca8", 1.9), I.line([[960, 160], [915, 197]], 1.9, "#ffcf8a", 5, dur=.3), I.glow(905, 205, 60, 1.9, .7),
               I.strike(770, 370, 930, 190, 2.9), I.strike(770, 190, 930, 370, 3.0)]
    hot = [I.oval(CX, 1150, 150, 50, "#c8502a", "none", 0, 1, 3.7), I.glow(CX, 1130, 220, 3.7, .8, "red"),
           I.arrow([[CX - 60, 1110], [CX - 70, 960]], 4.6, "#ff8a5a", 4, dur=.6, curve=False), I.arrow([[CX + 60, 1110], [CX + 70, 960]], 4.8, "#ff8a5a", 4, dur=.6, curve=False)] + \
          [I.line([[CX + dx + 10 * math.sin(j * 1.3), 1060 - 22 * j] for j in range(9)], 6.3 + .25 * k, I.BLUE, 3, dur=.9, curve=True) for k, dx in enumerate((-30, 0, 30))] + \
          [I.oval(CX, 826, 110, 16, "#2a1d12", "none", 0, 1, 8.0), I.glow(CX, 830, 120, 8.0, .5)] + \
          [I.arrow([[960, y], [700, y + 10], [420, y - 6], [60, y + 6]], 9.9 + .3 * j, "#cfe6ff", 3, "inferred", 1.1) for j, y in enumerate((640, 560))] + \
          [I.glow(CX, 760, 420, 12.1, .3)]
    # the verdict: Atlantis struck; people when the Sahara was green, barely surveyed
    tag = [I.strike(380, 650, 620, 590, 1.5)] + \
          [I.oval(250, 1385, 110, 28, SEA, "#9fd0ff", 2, .8, 4.0)] + [I.line([[380 + 24 * k, 1410], [386 + 24 * k, 1372 - 10 * (k % 2)]], 4.2 + .03 * k, I.GREEN, 3, draw=False) for k in range(14)] + \
          [I.person(560 + 70 * k, 1410, 100, 4.6 + .25 * k) for k in range(3)] + I.question(830, 1380, 7.7, 64, I.GREEN) + [I.glow(500, 1000, 420, 10.2, .3)]
    return remix(ep, scenes={0: eye, 1: wmap, 2: scale, 3: eight, 4: dome, 5: plato}, alias={6: 0}, cams={0: [1, 500, 900]},
                 adds={1: mapadd}, line_adds={(0, 1): (online, None), (3, 1): (deep, [1.05, 500, 980])},
                 beat_adds={4: (craterx + hot, [1, 500, 860]), 5: (tag, None)})


def _scroll(x, y, w, at, c="#e9d6ad", style="known", op=None):
    """A small open scroll (a written text), centred on x, y."""
    h = w * .7
    if style != "known":
        return [{"k": "rect", "x": x - w / 2, "y": y - h / 2, "w": w, "h": h, "r": 6, "fill": "none", "c": c, "sw": 3, "style": style, "in": at}]
    out = [{"k": "rect", "x": x - w / 2, "y": y - h / 2, "w": w, "h": h, "r": 6, "fill": c, "c": "#8a6a3e", "sw": 2, "in": at, "fx": "pop"}]
    out += [{"k": "rect", "x": x - w / 2 - 8, "y": y - h / 2 - 4, "w": 14, "h": h + 8, "r": 7, "fill": "#cdb58a", "c": "#8a6a3e", "sw": 1.5, "in": at},
            {"k": "rect", "x": x + w / 2 - 6, "y": y - h / 2 - 4, "w": 14, "h": h + 8, "r": 7, "fill": "#cdb58a", "c": "#8a6a3e", "sw": 1.5, "in": at}]
    out += [{"k": "line", "p": [[x - w * .32, y - h * .25 + h * .17 * k], [x + w * .32, y - h * .25 + h * .17 * k]], "c": "#8a6a3e", "w": 2.5, "in": at + .2 + .05 * k, "fx": "draw", "dur": .3} for k in range(4)]
    return out


def _houses(x, y, n, at, w=34, c="#e6d6b2"):
    """A row of small flat-roofed houses (a town), feet on y."""
    out = []
    for k in range(n):
        h = w * (.8 + .35 * ((k * 7) % 3) / 2)
        out.append({"k": "rect", "x": x + k * w * 1.15, "y": y - h, "w": w, "h": h, "r": 2, "fill": c, "c": "#8a6a48", "sw": 1.5, "in": round(at + .06 * k, 2), "fx": "rise"})
    return out


def _wave(x0, x1, y, at, c="#9fd0ff", amp=14, n=None, w=4, dur=.8):
    n = n or max(6, int((x1 - x0) / 40))
    return {"k": "line", "p": [[round(x0 + (x1 - x0) * j / (2 * n), 1), round(y - amp * (j % 2), 1)] for j in range(2 * n + 1)], "c": c, "w": w, "curve": True, "in": at, "fx": "draw", "dur": dur}


def _temple(x, y, w, at, c="#e6d6b2"):
    """A columned temple front, feet on y."""
    h = w * .55
    out = [{"k": "rect", "x": x - w / 2, "y": y - h * .12, "w": w, "h": h * .12, "r": 2, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"}]
    for k in range(5):
        out.append({"k": "rect", "x": x - w * .42 + k * w * .2, "y": y - h * .82, "w": w * .07, "h": h * .7, "r": 1, "fill": c, "c": "none", "sw": 0, "in": round(at + .08 * k, 2), "fx": "rise"})
    out.append({"k": "poly", "p": [[x - w * .52, y - h * .82], [x + w * .52, y - h * .82], [x, y - h * 1.2]], "fill": c, "c": "none", "w": 0, "in": at + .5, "fx": "pop"})
    return out


def atlantis_m():
    """Atlantis as one continuous take (see mural.py): an island drowned in a day and a night, a chain of tellers, a strange match of dates,
    an ocean floor with no room for a continent, and a real city lost in Plato's lifetime."""
    from mural import remix
    import illus as I
    ep = atlantis()
    city = _iso_relabel(ep["shots"][2], {"the temple of Poseidon": "Poseidon's temple", "a canal to the sea": "", "rings of land and water · about 5 km": "Plato's city · 5 km"}, spin=.2)
    # 5 · the hook: an island empire; the sea rises over it in a day and a night; one man wrote it down, 9,000 years later
    isle = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(60, 1000, 880, 420, "#1d3a4a", r=0, at=-1),
            {"k": "poly", "p": [[150, 1000], [260, 900], [380, 830], [500, 800], [620, 830], [740, 900], [850, 1000]], "fill": "#8aa05a", "c": "#c9d79a", "w": 2, "curve": True, "in": .2, "fx": "rise"}]
            + _temple(500, 812, 170, .7) + _houses(300, 880, 3, 1.1, 30) + _houses(610, 880, 3, 1.2, 30) + [I.glow(500, 760, 200, 1.4, .45)]
            + [I.glow(200, 420, 120, 3.4, .9, "sun"), I.dot(200, 420, 34, "#ffe2a8", 3.4),
               I.line([[250, 400], [400, 330], [600, 330], [750, 400]], 4.0, "#cbbca8", 2, "inferred", 1.2, curve=True),
               I.dot(800, 420, 30, "#efe8da", 4.6), I.dot(814, 410, 30, "#2a2018", 4.6), I.glow(800, 420, 90, 4.6, .4)]
            + [I.box(60, 690, 880, 730, SEA, r=0, at=3.0, op=.82, fx="fill", dur=3.0), _wave(60, 940, 690, 5.6, "#bfe6f5", 10, 18, 3, 1.2)]}
    wrote = [I.glow(500, 760, 260, .3, .5), I.person(830, 640, 120, 2.5), _scroll(890, 580, 56, 3.3)[0], I.glow(830, 590, 110, 2.6, .4),
             I.arrow([[500, 760], [600, 640], [760, 590]], 4.3, I.AMBER, 3, "inferred", 1.2), I.label(560, 560, "9,000 years", 4.7, I.AMBER, 34, st="serif")]
    # 0 · the chain of tellers: Egyptian priests, then Solon, then Plato and his two dialogues
    relay = {"base": "dark", "cam": [1, 500, 880], "els": [I.person(380, 1330, 190, .3), I.glow(380, 1240, 150, .3, .35), I.label(380, 1385, "Plato · 360 BCE", .5, I.BONE, 30)]
             + _scroll(560, 1220, 90, 2.75) + _scroll(680, 1260, 90, 3.0)
             + [{"k": "poly", "p": [[230, 600], [370, 600], [355, 400], [245, 400]], "fill": "#c9a878", "c": "none", "w": 0, "in": 4.8, "fx": "rise"},
                {"k": "poly", "p": [[470, 600], [610, 600], [595, 400], [485, 400]], "fill": "#c9a878", "c": "none", "w": 0, "in": 4.9, "fx": "rise"},
                I.box(370, 470, 100, 130, "#2a2018", r=2, at=5.0), I.person(420, 600, 100, 5.2), I.label(420, 650, "priests in Egypt", 5.4, I.AMBER, 30)]
             + [I.person(640, 960, 160, 6.4), I.label(640, 1010, "Solon", 6.6, I.BONE, 32),
                I.arrow([[500, 560], [610, 680], [630, 770]], 7.1, I.AMBER, 3, "inferred", .9), I.arrow([[620, 980], [520, 1060], [430, 1120]], 7.7, I.AMBER, 3, "inferred", .9)]}
    # 1 · the map: Plato's text in Greece; nothing older in Egypt
    v = View(-32, 30, 22, 48, (40, 330, 920, 900))
    ax_, ay_ = v.p(23.73, 37.98); sx, sy = v.p(30.77, 30.96)
    mapadd = _scroll(840, 600, 64, .6) + [I.line([[840, 625], [ax_, ay_ - 12]], .9, "#e9d6ad", 2, "inferred", .4)] + \
             _scroll(900, 990, 64, 2.2, I.LILAC, "claimed") + [I.line([[900, 965], [sx, sy + 12]], 2.3, I.LILAC, 2, "claimed", .4)] + I.question(900, 1010, 2.6, 52) + \
             [I.label(v.p(-22, 40)[0], v.p(-22, 40)[1], "Atlantis?", 4.0, I.LILAC, 40, st="serif", fx="pop")]
    # 4 · the strange match: 9,000 years before Solon, and the end of the Ice Age cold snap
    X = lambda bce: round(100 + 800 * (10000 - bce) / 10000, 1)
    sl = [(10000, -60), (9000, -50), (8000, -40), (7000, -28), (6000, -18), (5000, -7), (4000, -3), (2000, -1), (0, 0)]
    Y = lambda m: round(400 - m * 4.6, 1)
    coin = {"base": "dark", "cam": [1, 500, 860], "els": [I.line([[90, 820], [910, 820]], .3, "#8c7152", 3, dur=1.0),
            I.label(100, 870, "10,000 BCE", .6, "#cbbca8", 28, "start"), I.label(900, 870, "1 CE", .6, "#cbbca8", 28, "end"),
            I.person(X(600), 810, 110, 3.9), I.label(X(600) - 20, 690, "Solon", 4.0, I.BONE, 30, "end"),
            {"k": "arrow", "p": [[X(600) - 10, 840], [X(5000), 990], [X(9600) + 6, 840]], "c": I.AMBER, "w": 3, "curve": True, "fx": "draw", "dur": 1.6, "in": 4.6},
            I.label(X(5000), 1040, "9,000 years", 5.0, I.AMBER, 34, st="serif"),
            I.dot(X(9600), 820, 11, I.AMBER, 5.4), I.label(X(9600) + 22, 772, "Plato's date", 5.6, I.AMBER, 30, "start"),
            I.dot(X(9700), 820, 11, I.BLUE, 10.4), I.label(X(9700) + 22, 732, "Ice Age ends", 10.6, I.BLUE, 30, "start")]
            + [I.box(200, 1170, 600, 90, "#dfeaf2", "#9fd0ff", 2, 40, 11.4, fx="pop")]
            + [I.line([[220 + 12 * j, 1180], [220 + 12 * j, 1250]], round(11.8 + .02 * j, 2), "#5a7f9a" if j < 30 else "#c9a370", 2, draw=False) for j in range(48)]
            + [I.label(500, 1310, "layers of polar ice", 11.9, "#cfe6ff", 30), I.line([[220 + 12 * 30, 1160], [X(9700), 840]], 13.6, I.BLUE, 2, "inferred", .8),
            {"k": "line", "p": [[X(t), Y(m)] for t, m in sl], "c": SEA, "w": 5, "curve": True, "in": 17.1, "fx": "draw", "dur": 2.2},
            I.label(X(1500), Y(0) - 26, "sea level", 17.9, I.BLUE, 30), I.arrow([[X(8600), Y(-38)], [X(6900), Y(-20)]], 18.2, I.BLUE, 3, dur=.6, curve=False),
            I.ring(X(9650), 820, 34, 19.6, I.AMBER, 4), I.glow(X(9650), 820, 90, 19.6, .8)]}
    # beat 5 on the same panel: zoom on Plato's own century: Helike swallowed in 373 BCE, while Plato lived
    Z = lambda bce: round(180 + 700 * (420 - bce) / 100, 1)
    helike = [I.ring(X(400), 820, 30, .2, I.BONE, 3), I.line([[X(400) - 22, 845], [180, 1110]], .6, I.BONE, 2, "inferred", .5), I.line([[X(400) + 20, 845], [880, 1110]], .6, I.BONE, 2, "inferred", .5),
              I.box(140, 1110, 780, 300, "#1b1511", "#cbbca8", 2, 12, .8),
              I.line([[180, 1340], [880, 1340]], 1.4, "#8c7152", 3), I.box(180, 1300, Z(348) - 180, 16, I.AMBER, r=8, at=9.3, op=.8), I.label(200, 1290, "Plato's life", 9.5, I.AMBER, 28, "start")]
    helike += _houses(Z(373) - 70, 1250, 4, 3.0, 30) + [I.line([[Z(373) - 80 + 12 * j, 1262 + 6 * (j % 2)] for j in range(14)], 3.6, "#ffcf8a", 3, dur=.5),
               {"k": "poly", "p": [[Z(373) - 100, 1262], [Z(373) - 60, 1190], [Z(373), 1160], [Z(373) + 50, 1185], [Z(373) + 80, 1262]], "fill": SEA, "c": "#bfe6f5", "w": 2, "op": .85, "keepop": True, "curve": True, "in": 6.2, "fx": "rise"},
               I.label(Z(373), 1385, "Helike · 373 BCE", 7.5, I.BLUE, 30)]
    helike += [I.person(Z(355), 1290, 90, 9.4), I.glow(Z(355), 1250, 80, 9.4, .4), I.line([[Z(373) + 70, 1215], [Z(355) - 20, 1225]], 11.7, I.BONE, 2, "inferred", .5)]
    news = _scroll(Z(355) + 90, 1190, 60, .8) + [I.arrow([[Z(373) + 20, 1150], [Z(363), 1120], [Z(355) + 60, 1170]], 2.4, I.AMBER, 3, "inferred", .8)]
    # 3 · the ocean floor: a ridge down the middle, new floor spreading both ways; no room for a continent, no ships yet
    RX = 500
    stripes = []
    for k in range(6):
        for sgn in (-1, 1):
            x0 = RX + sgn * (20 + 62 * k)
            stripes.append(I.box(min(x0, x0 + sgn * 62), 990, 62, 70, "#5a4a40" if k % 2 else "#7a6a5c", r=0, at=round(7.2 + .45 * k, 2), fx="pop"))
    ocean = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(60, 430, 880, 560, "#1d3a4a", r=0, at=.2), _wave(60, 940, 430, .3, "#bfe6f5", 8, 20, 3, 1.0),
             I.label(500, 390, "the Atlantic", .4, I.BLUE, 34, st="ital"),
             {"k": "poly", "p": [[60, 380], [150, 380], [190, 990], [60, 990]], "fill": "#8a6a48", "c": "none", "w": 0, "in": .5},
             {"k": "poly", "p": [[850, 380], [940, 380], [940, 990], [810, 990]], "fill": "#8a6a48", "c": "none", "w": 0, "in": .5},
             {"k": "poly", "p": [[190, 990], [300, 960], [420, 900], [480, 840], [520, 840], [580, 900], [700, 960], [810, 990]], "fill": "#4a3c34", "c": "#cbbca8", "w": 2, "in": 2.0, "fx": "rise"},
             I.box(RX - 20, 990, 40, 70, "#c8502a", r=0, at=6.4)] + stripes +
            [I.glow(RX, 1100, 160, 6.4, .8, "red"), I.arrow([[RX - 40, 1110], [RX - 300, 1110]], 10.3, I.AMBER, 4, dur=.8, curve=False), I.arrow([[RX + 40, 1110], [RX + 300, 1110]], 10.3, I.AMBER, 4, dur=.8, curve=False),
             {"k": "poly", "p": [[240, 960], [260, 860], [330, 820], [400, 860], [410, 930]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": 11.7, "curve": True},
             I.strike(220, 980, 430, 800, 13.0), I.strike(220, 800, 430, 980, 13.1),
             {"k": "boat", "x": 680, "y": 440, "w": 150, "in": 16.6}, I.strike(600, 470, 760, 360, 17.6),
             {"k": "poly", "p": [[880, 360], [905, 300], [925, 355], [905, 372]], "fill": "#9aa0a8", "c": "#e8e4dc", "w": 1.5, "in": 18.6, "fx": "pop"}, I.glow(905, 340, 70, 18.6, .7)]}
    # the verdict, on Plato's city: two dates side by side; Plato's story, and the real rising sea
    tag = [I.box(250, 330, 220, 60, "none", I.AMBER, 3, 30, 3.0), I.label(360, 372, "9600 BCE", 3.0, I.AMBER, 30),
           I.box(530, 330, 220, 60, "none", I.BLUE, 3, 30, 3.4), I.label(640, 372, "9700 BCE", 3.4, I.BLUE, 30)] + I.question(500, 500, 5.0, 64) + \
          _scroll(300, 1350, 80, 8.0) + [I.label(300, 1420, "Plato's story", 8.2, I.BONE, 28),
          I.arrow([[700, 1420], [700, 1300]], 10.1, I.BLUE, 4, dur=.6, curve=False), _wave(600, 800, 1300, 10.3, "#9fd0ff", 10, 4, 3), I.label(700, 1420, "the real sea", 10.5, I.BLUE, 28)]
    return remix(ep, scenes={0: relay, 2: city, 3: ocean, 4: coin, 5: isle}, alias={6: 2}, cams={},
                 adds={1: mapadd, 2: tag}, line_adds={(0, 1): (wrote, None), (4, 1): (news, None)}, beat_adds={4: (helike, [1, 500, 900])})


def _diver(x, y, h, at, c="#e8d6b8"):
    """A swimming figure (a standing person turned on its side), centred near x, y."""
    return {"k": "group", "tr": "rotate(-78 %s %s)" % (x, y), "in": at, "els": [{"k": "person", "x": x, "y": y + h / 2, "h": h, "t": False, "color": c}]}


def _block(x, y, w, h, at, c="#cdbb95", layers=0, tilt=0.0, lc="#7a6248", fx="rise", ldelay=.3):
    """A stone block in side view, feet on y; optional bedding layers inside at a tilt (rise per px)."""
    out = [{"k": "rect", "x": x, "y": y - h, "w": w, "h": h, "r": 3, "fill": c, "c": "#8a6a48", "sw": 1.5, "in": at, "fx": fx}]
    for k in range(layers):
        y0 = y - h * (k + 1) / (layers + 1)
        a, b = [x + 4, y0 - tilt * w / 2], [x + w - 4, y0 + tilt * w / 2]
        out.append({"k": "line", "p": [[round(a[0], 1), round(a[1], 1)], [round(b[0], 1), round(b[1], 1)]], "c": lc, "w": 2.5, "in": round(at + ldelay + .05 * k, 2), "fx": "draw", "dur": .4})
    return out


def bimini_m():
    """The Bimini Road as one continuous take (see mural.py): a prophecy, a find, sand turning to stone and cracking, seventeen cores, and two dates."""
    from mural import remix
    import illus as I
    ep = bimini()
    road = _iso_relabel(ep["shots"][0], {"flat squared blocks · half a mile": "squared blocks · half a mile"}, spin=.12)
    # hook, line 2: 1968, the year the prophecy named
    year = [I.box(110, 270, 180, 100, "#f5ecdc", "#8a6a48", 2, 10, .3, fx="pop"), I.box(110, 270, 180, 24, I.RED, r=10, at=.3),
            I.label(200, 356, "1968", .5, "#1a1511", 40, st="serif", halo=False)] + \
           [{"k": "poly", "p": [[660, 370], [700, 310], [760, 290], [820, 310], [860, 370]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "curve": True, "in": 3.75}] + \
           [_wave(640, 880, 374, 3.75, I.BLUE, 8, 6, 3, .6)] + I.question(760, 350, 4.3, 50)
    # 5 · the prophecy: 1940, 'expect it in '68', 1968
    X = lambda yr: 160 + 640 * (yr - 1940) / 28
    pro = {"base": "dark", "cam": [1, 500, 880], "els": [I.line([[110, 1150], [890, 1150]], .2, "#8c7152", 3, dur=.8),
           I.person(X(1940), 1140, 190, .6), I.label(X(1940), 1200, "1940", .7, I.BONE, 32), I.glow(X(1940), 1040, 140, .7, .3)]
           + [_wave(560, 900, 900, 3.55, I.BLUE, 10, 8, 3, .8),
              {"k": "poly", "p": [[600, 900], [650, 820], [730, 780], [810, 810], [860, 900]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "curve": True, "in": 3.7},
              I.label(730, 740, "Atlantis rises?", 3.9, I.LILAC, 32)]
           + [{"k": "poly", "p": [[230, 880], [430, 880], [430, 960], [300, 960], [262, 1000], [270, 960], [230, 960]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": 7.65},
              I.label(330, 935, "'68", 7.8, I.LILAC, 40, st="serif"),
              I.arrow([[X(1940) + 60, 1100], [500, 1070], [X(1968) - 20, 1110]], 8.4, I.AMBER, 3, "claimed", 1.2), I.dot(X(1968), 1150, 12, I.AMBER, 9.1), I.label(X(1968), 1200, "1968", 9.1, I.AMBER, 32)]}
    # 1 · the map: the find, 5.5 m down
    bx_, by_ = 448.5, 725.0
    found = [I.ring(bx_, by_, 40, .3, I.AMBER, 3), I.glow(bx_, by_, 110, .3, .7), I.line([[bx_ - 10, by_ + 40], [300, 1000]], .6, "#cbbca8", 2, "inferred", .5),
             I.box(90, 1000, 360, 330, "#10202a", "#cbbca8", 2, 14, .8, fx="pop"), I.box(92, 1060, 356, 268, SEA, r=0, at=1.0, op=.55),
             _wave(92, 448, 1060, 1.0, "#bfe6f5", 6, 8, 2, .6), I.line([[92, 1300], [448, 1300]], 1.2, "#c9b48c", 4, draw=False)] + \
            sum([_block(130 + 72 * k, 1300, 60, 22, 1.4 + .1 * k, fx="pop") for k in range(4)], []) + \
            [_diver(250, 1150, 90, 3.1), {"k": "dim", "x1": 420, "y1": 1064, "x2": 420, "y2": 1296, "t": "5.5 m", "c": "#cfe6ff", "in": 4.0, "lx": -30}]
    # beat 3 on the road: straight lines, square corners, blocks on props; and the banks were dry in the Ice Age
    case = sum([_block(140 + 190 * k, 1405 - (22 if k == 1 else 0), 170, 70, .4 + .2 * k, fx="pop") for k in range(4)], []) + \
           [I.line([[110, 1405], [890, 1405]], .2, "#8c7152", 3, draw=False)] + \
           [I.dot(345 + 40 * j, 1394, 11, "#9aa0a8", 6.3 + .1 * j) for j in range(4)] + \
           [I.line([[120, 1290], [880, 1290]], 3.3, I.LILAC, 3, "claimed", 1.0), I.label(500, 1270, "straight?", 3.5, I.LILAC, 30)] + \
           [I.line([[140, 1335], [140, 1310], [165, 1310]], 4.5, I.LILAC, 3, dur=.3), I.line([[690, 1335], [690, 1310], [715, 1310]], 4.6, I.LILAC, 3, dur=.3)] + \
           [I.ring(410, 1394, 46, 7.5, I.LILAC, 3), I.label(410, 1440, "props?", 7.7, I.LILAC, 30)]
    dry = [I.line([[100, 500], [900, 500]], .3, "#c9b48c", 7, draw=False), I.label(110, 485, "the bank", .4, "#c9b48c", 28, "start"),
           _wave(100, 900, 430, .8, I.BLUE, 6, 16, 3, .8), I.label(890, 415, "sea today", 1.0, I.BLUE, 28, "end"),
           I.label(500, 545, "dry land", 2.8, I.AMBER, 30),
           I.arrow([[200, 436], [200, 590]], 4.6, I.BLUE, 3, dur=.4, curve=False), I.line([[100, 600], [900, 600]], 4.8, I.BLUE, 2, "inferred", .8),
           I.label(890, 640, "Ice Age sea", 5.0, I.BLUE, 28, "end")]
    # 2 · beachrock: sand in the tide zone, soaked and dried, cemented by lime, then cracked into squares
    sandy = [I.box(60, 560, 880, 460, "#c9b48c", r=0, at=.2), I.box(60, 1020, 880, 400, SEA, r=0, at=.2, op=.8)] + \
            [I.dot(x, y, 4, "#8a7452", .3 + .002 * k) for k, (x, y) in enumerate(I.scatter(120, 80, 920, 580, 1000, 4))] + \
            [_wave(60, 940, 1020, .4, "#bfe6f5", 10, 20, 3, 1.0),
             I.line([[60, 780], [940, 780]], 3.4, "#9fd0ff", 3, "inferred", .8), I.label(80, 765, "high tide", 3.5, I.BLUE, 28, "start"),
             I.line([[60, 1000], [940, 1000]], 3.6, "#9fd0ff", 3, "inferred", .8), I.label(80, 1060, "low tide", 3.7, "#cfe6ff", 28, "start")]
    lime = [I.arrow([[200 + 140 * k, 1060], [210 + 140 * k, 900]], 4.8 + .15 * k, I.BLUE, 3, dur=.5, curve=False) for k in range(5)] + \
           [I.glow(820, 420, 120, 6.0, .9, "sun"), I.dot(820, 420, 40, "#ffe2a8", 6.0)] + \
           [I.dot(x, y, 5, "#ffffff", 6.6 + .004 * k) for k, (x, y) in enumerate(I.scatter(90, 90, 910, 800, 990, 9))] + \
           [I.box(70, 800, 860, 186, "#d8c8a0", "#f5ecdc", 2, 6, 8.9, op=.92, fx="pop"), I.label(500, 900, "beachrock", 9.2, "#5a4632", 34, halo=False)]
    kettle = [{"k": "poly", "p": [[290, 425], [350, 362], [364, 372], [300, 452]], "fill": "#8a939c", "c": "#cbd2d8", "w": 2, "in": 7.55, "fx": "pop"},
              {"k": "poly", "p": [[140, 470], [150, 372], [182, 342], [258, 342], [290, 372], [300, 470]], "fill": "#8a939c", "c": "#cbd2d8", "w": 2, "in": 7.55, "fx": "pop"},
              I.line([[176, 344], [190, 296], [250, 296], [264, 344]], 7.55, "#cbd2d8", 6, curve=True, draw=False), I.dot(220, 336, 9, "#cbd2d8", 7.55),
              I.box(146, 440, 150, 28, "#ffffff", r=4, at=7.9)]
    crack = [I.line([[70 + 120 * k + 8 * (k % 2), 800], [72 + 120 * k - 6 * (k % 2), 986]], 10.2 + .12 * k, "#3a2a1c", 4, dur=.4) for k in range(1, 8)] + \
            [I.line([[70, 893], [930, 897]], 11.2, "#3a2a1c", 4, dur=.8)]
    beach = {"base": "dark", "cam": [1, 500, 860], "els": sandy + lime + kettle + crack}
    # 3 · seventeen cores; the layers run on from block to block; builders' blocks would tilt every which way
    cores = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(150 + 42 * (k % 17), 330, 22, 70, "#e9dccb", "#8a7a66", 1.5, 10, .3 + .06 * k, fx="pop") for k in range(17)] +
             [I.label(500, 450, "17 cores", 1.4, I.BONE, 34)] +
             sum([_block(110 + 200 * k, 1000, 180, 260, 2.4 + .2 * k, "#c9b48c", fx="pop") for k in range(4)], []) +
             [I.line([[110, 820 + 40 * j - 30], [890, 820 + 40 * j + 30]], 4.4 + .3 * j, "#7a6248", 3, dur=1.4) for j in range(4)] +
             [I.box(190 + 200 * k, 740, 22, 200, "#e9dccb", "#8a7a66", 1.5, 10, 3.4 + .15 * k, fx="fill") for k in range(4)] +
             [I.label(500, 1060, "one slab, broken", 6.4, I.AMBER, 32)] +
             _block(220, 1360, 150, 120, 7.5, "#c9b48c", 3, .5, I.LILAC, "pop") + _block(420, 1360, 150, 120, 7.7, "#c9b48c", 3, -.45, I.LILAC, "pop") +
             _block(620, 1360, 150, 120, 7.9, "#c9b48c", 3, .1, I.LILAC, "pop") + [I.label(500, 1420, "laid by builders?", 8.1, I.LILAC, 30)]}
    # 4 · the dates: a candle burns down at a steady pace; shells 3,500 years old, the cement younger; no stone when the Ice Age ended
    T = lambda ya: round(120 + 760 * (12000 - ya) / 12000, 1)
    cand = []
    cand += [{"k": "poly", "p": [[130, 560], [160, 440], [200, 420], [240, 440], [270, 560]], "fill": "#e8c89a", "c": "#8a6a48", "w": 2, "curve": True, "in": 1.0, "fx": "pop"}] + \
            [I.line([[200, 556], [150 + 25 * k, 450 + 6 * abs(k - 2)]], 1.2, "#8a6a48", 2, draw=False) for k in range(5)] + \
            [I.dot(x, y, 6, I.GREEN, round(1.8 + .25 * k, 2), op=round(.9 - .1 * k, 2)) for k, (x, y) in enumerate(((120, 400), (280, 410), (110, 590), (295, 580), (200, 375), (90, 480)))]
    for k, h in enumerate((200, 140, 80)):
        cx = 440 + 160 * k
        cand += [I.box(cx - 22, 600 - h, 44, h, "#efe6d2", "#cbbca8", 1.5, 6, 4.6 + .5 * k), I.line([[cx, 600 - h], [cx, 590 - h]], 4.6 + .5 * k, "#1a1511", 2, draw=False),
                 {"k": "poly", "p": [[cx, 560 - h], [cx + 12, 585 - h], [cx, 595 - h], [cx - 12, 585 - h]], "fill": "#ffcf8a", "c": "none", "w": 0, "curve": True, "in": 4.7 + .5 * k}, I.glow(cx, 575 - h, 60, 4.7 + .5 * k, .8, "fire")]
    dates = {"base": "dark", "cam": [1, 500, 860], "els": cand + [I.line([[380, 610], [780, 610]], 4.6, "#8c7152", 3, draw=False),
             I.line([[100, 1000], [900, 1000]], .2, "#8c7152", 3, dur=.8), I.label(110, 1050, "12,000 years ago", .3, "#cbbca8", 28, "start"), I.label(890, 1050, "today", .3, "#cbbca8", 28, "end"),
             I.dot(T(3500), 1000, 12, I.AMBER, 8.0), I.label(T(3500), 960, "shells: 3,500 years", 8.2, I.AMBER, 30),
             I.arrow([[T(3500) + 16, 1020], [T(2000), 1020]], 10.5, I.BONE, 3, dur=.5, curve=False), I.label(T(2700), 1080, "cement", 10.7, I.BONE, 28),
             I.dot(T(11700), 1000, 12, I.BLUE, 11.9), I.label(T(11700) + 10, 900, "Ice Age ends", 12.0, I.BLUE, 30, "start"),
             I.box(T(11700) - 40, 760, 120, 90, "none", I.LILAC, 3, 6, 12.7, style="claimed"), I.strike(T(11700) - 50, 860, T(11700) + 90, 750, 13.6),
             I.line([[T(11700), 1120], [T(11700), 1150], [T(3500), 1150], [T(3500), 1120]], 13.0, I.BONE, 2, "inferred", 1.0), I.label((T(11700) + T(3500)) / 2, 1200, "no stone yet", 13.4, I.BONE, 30)]}
    layer = [_wave(160, 460, 1320, .3, "#9fd0ff", 18, 4, 5, .8)] + sum([_block(520 + 110 * k, 1360, 100, 50, .8 + .3 * k, "#c9b48c", fx="pop") for k in range(3)], []) + \
            [I.arrow([[440, 1290], [520, 1300]], .6, "#9fd0ff", 3, dur=.4)]
    # the verdict on the road: people reusing the slabs later? not ruled out, nothing points to it
    tag = [I.strike(670, 390, 850, 280, 2.0)] + [I.person(275 + 42 * k, 850 + 10 * k, 70, 4.0 + .2 * k, c=I.LILAC) for k in range(3)] + I.question(400, 790, 9.7, 54) + [I.glow(500, 940, 380, 13.3, .3)]
    return remix(ep, scenes={0: road, 2: beach, 3: cores, 4: dates, 5: pro}, alias={6: 0}, cams={6: [1.12, 500, 900]},
                 adds={1: found}, line_adds={(0, 1): (year, None), (2, 1): (dry, None), (4, 1): (layer, None)}, beat_adds={2: (case, None), 5: (tag, None)})


def _stairs(pts, at, fill="#8a7a62", c="#c9b49a", bottom=1420, fx="rise"):
    """A stepped rock profile (side view) from a list of corner points, filled down to `bottom`."""
    p = [list(q) for q in pts] + [[pts[-1][0], bottom], [pts[0][0], bottom]]
    return {"k": "poly", "p": p, "fill": fill, "c": c, "w": 2, "in": at, "fx": fx}


def _canoe(x, y, w, at, n=5):
    """A dugout canoe with paddlers, centred on x, waterline y."""
    out = [{"k": "poly", "p": [[x - w / 2, y - 10], [x + w / 2, y - 14], [x + w / 2 - 20, y + 10], [x - w / 2 + 16, y + 10]], "fill": "#7a4a2a", "c": "#c9905a", "w": 2, "in": at, "fx": "pop"}]
    for k in range(n):
        px = x - w / 2 + 34 + k * (w - 68) / max(1, n - 1)
        out += [{"k": "person", "x": round(px, 1), "y": y - 8, "h": 46, "t": False, "color": "#e8d6b8", "in": round(at + .15 + .08 * k, 2), "fx": "rise"},
                {"k": "line", "p": [[round(px + 8, 1), y - 30], [round(px - 14, 1), y + 14]], "c": "#cbbca8", "w": 3, "in": round(at + .3 + .08 * k, 2)}]
    return out


def _trowel(x, y, s, at):
    """A trowel, blade down-left, handle up-right."""
    return [{"k": "poly", "p": [[x, y], [x + .55 * s, y - .25 * s], [x + .75 * s, y - .75 * s], [x + .25 * s, y - .55 * s]], "fill": "#cbd2d8", "c": "#8a939c", "w": 2, "in": at, "fx": "pop"},
            {"k": "line", "p": [[x + .62 * s, y - .62 * s], [x + 1.0 * s, y - 1.0 * s]], "c": "#c9905a", "w": max(6, s * .1), "in": at}]


def yonaguni_m():
    """Yonaguni as one continuous take (see mural.py): a monument read into the rock, the trick of flat layers and straight cracks,
    people on dry steps, a dugout crossing, and the sediment nobody has dug."""
    from mural import remix
    import illus as I
    ep = yonaguni()
    steps = _iso_relabel(ep["shots"][0], {"flat terraces, sheer walls, right angles": "terraces · walls · right angles", "25 m down at the base · 5 m at the top": "base 25 m down · top 5 m"}, spin=.12)
    ymap = _pins_relabel(ep["shots"][1], {"225 km by dugout, 2019": ""})
    ymap["els"] = [e for e in ymap["els"] if not (e.get("k") == "line" and e.get("style") == "inferred")]
    who = [I.person(800, 700, 130, .3, c=I.LILAC), I.line([[830, 620], [880, 580]], .5, "#cbbca8", 5, draw=False)] + I.question(880, 570, .7, 56)
    # 1 · the map: 110 km from Taiwan, the far end of a chain of islands; base 25 m down, top 5 m
    v = View(119.5, 129.5, 21.5, 28.5, (40, 330, 920, 900))
    yx, yy = v.p(123.0, 24.44)
    tx, ty = v.p(121.85, 24.5)
    chain = [v.p(lo, la) for lo, la in ((124.2, 24.4), (125.3, 24.8), (126.6, 25.6), (127.7, 26.3), (128.6, 27.4))]
    madd = [I.line([[tx + 6, ty], [yx - 14, yy]], .6, I.AMBER, 3, dur=.8), I.label((tx + yx) / 2, yy - 24, "110 km", 1.0, I.AMBER, 30),
            I.line([[yx + 12, yy - 4]] + [list(q) for q in chain], 3.0, I.AMBER, 2, "inferred", 1.6, curve=True),
            I.box(70, 1000, 400, 380, "#10202a", "#cbbca8", 2, 14, 5.3, fx="pop"), _wave(72, 468, 1060, 5.5, "#bfe6f5", 6, 8, 2, .6),
            _stairs([[90, 1350], [200, 1350], [200, 1280], [280, 1280], [280, 1200], [360, 1200], [360, 1110], [450, 1110]], 5.7, bottom=1378),
            I.label(270, 1250, "one piece", 6.5, "#efe6d2", 28),
            {"k": "dim", "x1": 120, "y1": 1064, "x2": 120, "y2": 1346, "t": "25 m", "c": "#cfe6ff", "in": 9.5, "lx": -24},
            {"k": "dim", "x1": 425, "y1": 1064, "x2": 425, "y2": 1106, "t": "5 m", "c": "#cfe6ff", "in": 10.5, "lx": -40, "upright": True}]
    # beat 3 on the model: what Kimura mapped (claimed); line 2: Hancock's version, people shaping dry steps
    icons = []
    for k, (t, at) in enumerate((("terraces", 6.7), ("a road", 7.4), ("a channel", 8.2), ("a face", 9.2))):
        x = 170 + 220 * k
        icons += [I.box(x - 80, 290, 160, 130, "none", I.LILAC, 3, 12, at, style="claimed"), I.label(x, 460, t, at + .1, I.LILAC, 30)]
    icons += [I.line([[100, 400], [130, 400], [130, 370], [160, 370], [160, 340], [190, 340], [190, 310], [240, 310]], 6.8, I.LILAC, 4, dur=.5),
              I.line([[330, 400], [410, 300]], 7.5, I.LILAC, 4, dur=.4), I.line([[370, 400], [450, 300]], 7.5, I.LILAC, 4, dur=.4),
              I.box(570, 320, 80, 70, "none", I.LILAC, 4, 2, 8.3), I.line([[590, 320], [590, 390], [630, 390], [630, 320]], 8.4, I.LILAC, 3, dur=.4),
              I.ring(830, 355, 46, 9.3, I.LILAC, 4), I.dot(814, 345, 5, I.LILAC, 9.4), I.dot(846, 345, 5, I.LILAC, 9.4), I.line([[815, 375], [830, 382], [845, 375]], 9.5, I.LILAC, 3, dur=.3),
              _diver(200, 620, 110, .8), I.glow(200, 620, 90, .9, .4)]
    shaped = [_stairs([[220, 1400], [380, 1400], [380, 1340], [520, 1340], [520, 1280], [660, 1280], [660, 1230], [780, 1230]], .4, "#8a7a62", bottom=1430),
              I.glow(860, 1180, 90, .6, .9, "sun"), I.dot(860, 1180, 26, "#ffe2a8", .6),
              I.person(450, 1340, 70, 3.4, c=I.LILAC), I.person(590, 1280, 70, 3.6, c=I.LILAC), I.line([[470, 1300], [500, 1320]], 3.8, "#cbbca8", 4, draw=False),
              I.label(330, 1310, "shaped?", 4.0, I.LILAC, 30), I.arrow([[930, 1420], [930, 1240]], 6.5, I.BLUE, 4, dur=.8, curve=False)]
    # 2 · the trick: flat layers + straight cracks = steps and right angles; the waves pluck out the loose pieces
    G0, GX, GY, CW, RH = 150, 520, 1000, 100, 120
    trick = [I.box(60, 440, 880, 560, SEA, r=0, at=.2, op=.55), _wave(60, 940, 440, .2, "#bfe6f5", 8, 20, 3, .8),
             I.box(G0, GX, 700, 480, "#b8a47e", "#8a7a62", 2, 2, .4, fx="pop")] + \
            [I.line([[G0, GX + RH * j], [G0 + 700, GX + RH * j]], 2.2 + .2 * j, "#5a4e40", 3, dur=.6) for j in (1, 2, 3)] + \
            [I.line([[G0 + CW * j, GX], [G0 + CW * j, GY]], 3.1 + .1 * j, "#3a3128", 3, dur=.4) for j in range(1, 7)] + \
            [I.box(100, 290 + 14 * k, 200, 11, "#efe6d2", "#8a7a66", 1, 2, 4.7 + .05 * k) for k in range(6)] + [I.line([[200, 270], [200, 390]], 5.9, I.RED, 3, "inferred", .4)]
    gone = [(0, 3), (0, 4), (0, 5), (0, 6), (1, 5), (1, 6), (2, 6)]
    trick += [I.line([[G0 + 300, GX], [G0 + 300, GX + RH], [G0 + 500, GX + RH], [G0 + 500, GX + 2 * RH], [G0 + 600, GX + 2 * RH], [G0 + 600, GX + 3 * RH], [G0 + 700, GX + 3 * RH]], 8.2, I.AMBER, 5, dur=1.0)] + \
             [I.box(G0 + CW * c + 1, GX + RH * r + 1, CW - 2, RH - 2, "#2c5a72", r=0, at=10.9 + .2 * k, fx="pop") for k, (r, c) in enumerate(gone)] + \
             [I.arrow([[960, 470 + 60 * k], [880, 500 + 60 * k]], 10.6 + .2 * k, "#bfe6f5", 4, dur=.4, curve=False) for k in range(3)] + \
             [I.line([[G0 + CW * c, GX + RH * r + 26], [G0 + CW * c + 26, GX + RH * r + 26], [G0 + CW * c + 26, GX + RH * r]], 9.1 + .3 * k, I.GREEN, 4, dur=.3)
              for k, (r, c) in enumerate(((1, 3), (2, 5), (3, 6)))]
    trick += [_stairs([[100, 1300], [300, 1300], [300, 1220], [460, 1220], [460, 1150], [600, 1150], [600, 1090]], 14.1, "#b8a47e", "#e9dccb", 1400),
              I.line([[60, 1300], [940, 1300]], 14.1, "#8c7152", 3, draw=False), I.person(520, 1150, 80, 14.6), I.glow(800, 1120, 90, 14.3, .9, "sun"), I.dot(800, 1120, 26, "#ffe2a8", 14.3),
              I.label(760, 1260, "dry coast", 14.8, "#c9b48c", 30)]
    # 4 · people on these islands 30,000 years ago, the sea low, the steps in the open air
    lived = {"base": "dark", "cam": [1, 500, 880], "els": [I.line([[60, 520], [940, 520]], .3, "#9fd0ff", 2, "inferred", .8), I.label(80, 500, "sea today", .4, I.BLUE, 28, "start"),
             _stairs([[60, 1240], [300, 1240], [300, 1070], [480, 1070], [480, 900], [640, 900], [640, 740], [780, 740], [780, 600], [940, 600]], .5),
             _wave(60, 940, 1330, 3.25, "#bfe6f5", 8, 20, 3, .8), I.box(60, 1330, 880, 90, SEA, r=0, at=3.25, op=.75), I.label(920, 1385, "sea, then", 3.4, "#cfe6ff", 28, "end"),
             I.person(380, 1070, 110, 1.85), I.person(560, 900, 110, 2.0), I.person(860, 600, 110, 2.15), I.glow(420, 1050, 90, 2.3, .9, "fire"), I.dot(420, 1062, 10, "#ffcf8a", 2.3)]}
    # 3 · the crossing: Taiwan to Yonaguni by dugout, 225 km, just over 45 hours
    cross = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(60, 900, 880, 520, SEA, r=0, at=.2, op=.7), _wave(60, 940, 900, .2, "#bfe6f5", 8, 22, 3, .8),
             {"k": "poly", "p": [[60, 900], [60, 620], [120, 600], [190, 680], [240, 820], [280, 900]], "fill": "#6f7a4a", "c": "#c9d79a", "w": 2, "in": .4, "fx": "rise"},
             I.label(150, 960, "Taiwan", .6, "#c9d79a", 32),
             {"k": "poly", "p": [[780, 900], [810, 850], [870, 840], [910, 880], [920, 900]], "fill": "#6f7a4a", "c": "#c9d79a", "w": 2, "in": .8, "fx": "rise"},
             I.label(850, 960, "Yonaguni", 1.0, "#c9d79a", 32)] + _canoe(520, 905, 260, 1.6) +
            [I.arrow([[300, 860], [520, 760], [770, 850]], 5.4, I.AMBER, 3, "inferred", 1.4), I.label(520, 720, "225 km", 6.0, I.AMBER, 40, st="serif"),
             I.glow(300, 420, 80, 7.3, .9, "sun"), I.dot(300, 420, 24, "#ffe2a8", 7.3), I.dot(450, 420, 22, "#efe8da", 7.55), I.dot(460, 414, 22, "#2a2018", 7.55),
             I.glow(600, 420, 80, 7.8, .9, "sun"), I.dot(600, 420, 24, "#ffe2a8", 7.8), I.dot(750, 420, 22, "#efe8da", 8.05), I.dot(760, 414, 22, "#2a2018", 8.05),
             I.label(520, 520, "just over 45 hours", 8.3, I.BONE, 32)]}
    # 5 · the sediment nobody has dug; then the verdict, and the trowel
    prof = [[60, 1270], [300, 1270], [300, 1100], [480, 1100], [480, 930], [640, 930], [640, 760], [780, 760], [780, 590], [940, 590]]
    sed = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(60, 420, 880, 1000, SEA, r=0, at=.2, op=.45), _wave(60, 940, 420, .2, "#bfe6f5", 8, 20, 3, .8), _stairs(prof, .3)] +
           [I.box(x0, y - 18, x1 - x0, 18, "#5a4632", "#8a6a48", 1.5, 3, .4 + .1 * k, fx="fill") for k, (x0, x1, y) in enumerate(((60, 300, 1270), (300, 480, 1100), (480, 640, 930), (640, 780, 760)))] +
           [I.label(560, 985, "sediment", 1.2, "#efe6d2", 28), I.box(500, 896, 120, 46, "none", I.AMBER, 3, 4, 1.6, style="inferred"), I.label(560, 870, "never dug", 1.7, I.AMBER, 30)] +
           [{"k": "poly", "p": [[530, 924], [544, 908], [556, 924]], "fill": "none", "c": I.LILAC, "w": 2, "style": "claimed", "in": 4.3}, I.glow(590, 920, 40, 4.6, .7, "fire")]}
    verdict = [{"k": "line", "p": [[180, 610], [240, 560]], "c": I.LILAC, "w": 5, "in": .8}, I.label(170, 650, "carved?", 1.0, I.LILAC, 30), I.strike(130, 670, 260, 540, 2.2)] + \
              [I.person(400, 1100, 90, 2.7), I.person(700, 760, 90, 2.85), I.arrow([[880, 1360], [880, 640]], 3.9, I.BLUE, 4, dur=1.4, curve=False)] + I.question(300, 980, 6.0, 56, I.GREEN)
    trowel = _trowel(610, 900, 110, 2.0) + [I.glow(600, 880, 120, 2.1, .6)]
    return remix(ep, scenes={0: steps, 1: ymap, 2: {"base": "dark", "cam": [1, 500, 880], "els": trick}, 3: cross, 4: lived, 5: sed}, cams={},
                 adds={1: madd}, line_adds={(0, 1): (who, None), (2, 1): (shaped, None), (5, 1): (trowel, None)}, beat_adds={2: (icons, None), 5: (verdict, None)})


def _deer(x, y, s, at, c="#cbbca8", face=1):
    """A deer in profile (feet on y, s = body length in px), facing right (face=1) or left (-1)."""
    P = lambda a, b: [round(x + face * s * a, 1), round(y + s * b, 1)]
    body = [P(-.5, -.62), P(.28, -.66), P(.42, -.86), P(.58, -.92), P(.6, -.84), P(.46, -.7), P(.38, -.42), P(-.46, -.4), P(-.58, -.55)]
    out = [{"k": "poly", "p": body, "fill": c, "c": "none", "w": 0, "curve": True, "in": at, "fx": "rise"}]
    for a in (-.4, -.28, .22, .32):
        out.append({"k": "line", "p": [P(a, -.45), P(a + .02, 0)], "c": c, "w": max(3, s * .05), "in": at})
    out += [{"k": "line", "p": [P(.52, -.9), P(.5, -1.12), P(.42, -1.22)], "c": c, "w": 3, "in": at + .1}, {"k": "line", "p": [P(.5, -1.05), P(.62, -1.16)], "c": c, "w": 3, "in": at + .1}]
    return out


def _fossil(x, y, s, at, c="#e8dcc6"):
    """A small curved piece of fossil bone (schematic), centred on x, y."""
    return {"k": "poly", "p": [[round(x + s * a, 1), round(y + s * b, 1)] for a, b in ((-.5, .1), (-.3, -.3), (.1, -.42), (.48, -.2), (.5, .05), (.2, -.08), (-.2, -.02))],
            "fill": c, "c": "#8a7a66", "w": 1.5, "curve": True, "in": at, "fx": "pop"}


def drowned_m():
    """The drowned coasts as one continuous take (see mural.py): the sea drops 120 m into the ice, land bridges appear, a pulse read from corals,
    a village, a hunting wall, fossils from the sea floor, and a coastal chapter still unsearched."""
    from mural import remix
    import illus as I
    ep = drowned_coasts()
    shelf = _iso_relabel(ep["shots"][0], {}, spin=.12)
    village = _iso_relabel(ep["shots"][2], {"seven standing stones around a spring": "seven stones, a spring", "Atlit Yam · about 8,500 years old · now 10 m under the sea": "Atlit Yam · 10 m down"}, spin=.12)
    camps = [I.glow(x, y, 50, 3.4 + .3 * k, .9, "fire") for k, (x, y) in enumerate(((300, 790), (345, 772), (390, 752)))]
    # 4 · the Ice Age: water locked in ice sheets, the sea 120 m lower (a forty-storey tower)
    prof = [[60, 820], [250, 790], [400, 720], [520, 640], [640, 560], [760, 470], [860, 420], [940, 400]]
    Ym = lambda m: round(440 - m * 2.5, 1)
    ice = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(60, Ym(-120), 880, 820 - Ym(-120) + 40, SEA, r=0, at=7.4, op=.85, fx="fill", dur=1.2),
           {"k": "poly", "p": prof + [[940, 900], [60, 900]], "fill": "#7a6248", "c": "#e9dccb", "w": 2, "in": .3},
           I.line([[60, Ym(0)], [940, Ym(0)]], .8, "#9fd0ff", 3, "inferred", .8), I.label(80, Ym(0) - 14, "sea today", 1.0, I.BLUE, 28, "start"),
           {"k": "poly", "p": [[700, 500], [760, 380], [840, 330], [940, 310], [940, 420], [860, 420], [760, 470]], "fill": "#e6f0f7", "c": "#ffffff", "w": 2, "curve": True, "in": 5.8, "fx": "fill", "dur": 1.6},
           I.label(860, 290, "ice sheet", 6.2, "#e6f0f7", 30)] +
          [I.arrow([[300 + 90 * k, Ym(0) + 6], [380 + 100 * k, 400 - 20 * k], [700, 400]], 5.2 + .3 * k, "#cfe6ff", 2, "inferred", 1.0) for k in range(3)] +
          [_wave(60, 940, Ym(-120), 7.8, "#bfe6f5", 6, 20, 3, .8), I.label(80, Ym(-120) + 36, "Ice Age sea", 8.0, "#cfe6ff", 28, "start"),
           {"k": "dim", "x1": 240, "y1": Ym(0) + 4, "x2": 240, "y2": Ym(-120) - 4, "t": "120 m", "c": I.AMBER, "in": 8.7, "lx": -34},
           {"k": "poly", "p": [[400, 720], [520, 640], [640, 560], [760, 470], [760, Ym(-120)], [372, Ym(-120)]], "fill": I.AMBER, "c": "none", "w": 0, "op": .25, "keepop": True, "in": 9.3},
           I.label(560, 700, "dry land", 9.5, I.AMBER, 30),
           I.box(120, Ym(-120) - 300, 60, 300, "#3a3540", "#cbd2d8", 2, 2, 10.6, fx="fill", dur=1.2)] +
          [I.line([[126, Ym(-120) - 7.5 * j], [174, Ym(-120) - 7.5 * j]], 10.8, "#e8c35a", 1, draw=False, op=.5) for j in range(1, 40, 2)] +
          [I.label(150, Ym(-120) - 316, "40 storeys", 11.4, "#cbd2d8", 28)]}
    # beat 3 on the same panel: the sea-level curve read from dated corals, one pulse, generations on a moving beach
    T = lambda ya: round(120 + 760 * (22000 - ya) / 22000, 1)
    Yc = lambda m: round(960 - m * -2.8, 1) if False else round(960 + (-m) * 2.8, 1)
    pts = [(22000, -125), (19000, -120), (16000, -105), (14600, -95), (14300, -78), (12000, -60), (10000, -40), (8000, -18), (7000, -6), (4000, -1), (0, 0)]
    pulse = [I.line([[100, 1330], [900, 1330]], .2, "#8c7152", 3), I.label(110, 1380, "20,000 years ago", .3, "#cbbca8", 28, "start"), I.label(890, 1380, "today", .3, "#cbbca8", 28, "end"),
             {"k": "line", "p": [[T(a), Yc(m)] for a, m in pts], "c": SEA, "w": 5, "curve": True, "in": .6, "fx": "draw", "dur": 2.4},
             I.label(890, Yc(0) - 18, "sea level", 1.6, I.BLUE, 28, "end"),
             {"k": "line", "p": [[T(14600), Yc(-95)], [T(14450), Yc(-86)], [T(14300), Yc(-78)]], "c": I.AMBER, "w": 10, "in": 2.0, "fx": "draw", "dur": .5},
             I.glow(T(14450), Yc(-86), 70, 2.0, .9), I.label(T(14450) + 40, Yc(-86) + 10, "the pulse", 2.2, I.AMBER, 30, "start")]
    for k, (a, m) in enumerate(((19000, -120), (16000, -105), (14500, -90), (12000, -60), (10000, -40), (8000, -18))):
        x, y = T(a), Yc(m)
        pulse += [I.line([[x, y + 4], [x, y + 26]], 5.9 + .3 * k, "#ff9fb0", 3, draw=False), I.line([[x, y + 14], [x - 9, y + 4]], 5.9 + .3 * k, "#ff9fb0", 3, draw=False),
                  I.line([[x, y + 18], [x + 9, y + 8]], 5.9 + .3 * k, "#ff9fb0", 3, draw=False)]
    pulse += [I.label(T(9000) + 10, Yc(-30) + 40, "dated corals", 7.5, "#ff9fb0", 28, "start"), I.label(T(14450) + 40, Yc(-86) + 46, "4 to 5 cm a year", 9.6, I.AMBER, 28, "start")]
    pulse += [I.line([[620, 1300], [900, 1230]], 12.8, "#c9b48c", 5, draw=False)] + [_wave(620 + 66 * k, 696 + 66 * k, 1298 - 16.5 * k, 13.0 + .25 * k, "#9fd0ff", 5, 2, 3, .3) for k in range(4)] + \
             [I.person(660 + 66 * k, 1282 - 16.5 * k, 50 + 8 * k, 13.1 + .25 * k) for k in range(4)]
    # 1 · the map: land bridges and drowned shelves, then the melt
    v = View(-15, 125, -15, 62, (40, 330, 920, 900))
    poly = lambda pts_, at, c=I.AMBER: {"k": "poly", "p": [list(v.p(lo, la)) for lo, la in pts_], "fill": c, "c": c, "w": 2.5, "op": .3, "keepop": True, "style": "inferred", "curve": True, "in": at}
    dogger = [(-5.5, 50.0), (-1.0, 49.4), (3.0, 50.8), (8.2, 53.2), (9.0, 56.8), (5.0, 58.4), (0.0, 58.0), (-3.0, 56.0)]
    sunda = [(95.0, 6.0), (102.0, 8.5), (108.5, 7.0), (117.0, 6.5), (119.5, 0.0), (117.5, -8.6), (106.0, -8.4), (99.0, -3.5), (94.5, 2.0)]
    gulf = [(47.8, 30.4), (50.6, 29.6), (54.5, 25.8), (56.6, 26.6), (56.3, 24.6), (52.0, 23.8), (49.8, 26.2)]
    madd = [poly(dogger, .5), I.glow(v.p(3, 54.5)[0], v.p(3, 54.5)[1], 60, .6, .8),
            I.arrow([[900, 470], [960, 455]], 2.4, I.AMBER, 4, dur=.4, curve=False), I.label(940, 430, "to America", 2.6, I.AMBER, 28, "end"),
            poly(sunda, 4.2), I.label(v.p(108, 9)[0], v.p(108, 9)[1] - 8, "Sundaland", 4.6, I.AMBER, 28), poly(gulf, 5.4)] + \
           [_wave(v.p(lo, la)[0] - 40, v.p(lo, la)[0] + 40, v.p(lo, la)[1], 7.2 + .3 * k, "#9fd0ff", 6, 3, 3, .5) for k, (lo, la) in enumerate(((3, 54.5), (52, 26.5), (108, 0)))]
    # 3 · the Baltic wall: nearly a kilometre of stones, 21 m down, probably for hunting
    wall = [(round(100 + 800 * j / 69, 1), round(900 - 40 * j / 69 + 10 * math.sin(j * .5), 1)) for j in range(70)]
    baltic = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(60, 300, 880, 1120, "#1d3a4a", r=12, at=.2), _wave(80, 920, 340, .3, "#bfe6f5", 6, 20, 3, .8),
              I.arrow([[880, 350], [880, 520]], 3.6, "#cfe6ff", 3, dur=.5, curve=False), I.label(860, 570, "21 m down", 3.8, "#cfe6ff", 30, "end")] +
             [I.dot(x, y, 9, "#b0a08a", round(.6 + .03 * j, 2)) for j, (x, y) in enumerate(wall)] +
             [I.line([[100, 1000], [900, 960]], 2.6, I.BONE, 3, dur=1.0), I.line([[100, 985], [100, 1015]], 2.6, I.BONE, 3, draw=False), I.line([[900, 945], [900, 975]], 2.6, I.BONE, 3, draw=False),
              I.label(500, 1040, "nearly 1 km", 2.9, I.BONE, 32)] +
             _deer(300, 860, 90, 4.9) + _deer(430, 852, 80, 5.1) + _deer(560, 846, 90, 5.3) +
             [I.arrow([[230, 800], [420, 780], [640, 790]], 5.5, I.AMBER, 3, "inferred", .9), I.person(760, 840, 90, 5.7), I.person(820, 836, 90, 5.85),
              I.label(500, 720, "a hunting wall?", 6.0, I.AMBER, 30)]}
    # 5 · off Java: two skull pieces of Homo erectus, dredged from 32 m
    dredge = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(60, 470, 880, 700, SEA, r=0, at=.2, op=.7), _wave(60, 940, 470, .2, "#bfe6f5", 8, 20, 3, .8),
              {"k": "boat", "x": 420, "y": 470, "w": 260, "in": .5}, I.box(60, 1170, 880, 250, "#6f5a44", r=0, at=.4),
              I.line([[470, 460], [600, 600], [640, 1140]], 3.9, "#cbd2d8", 3, dur=1.0, curve=True), I.box(600, 1120, 90, 50, "#8a939c", "#cbd2d8", 2, 6, 4.2, fx="pop"),
              {"k": "dim", "x1": 880, "y1": 476, "x2": 880, "y2": 1164, "t": "32 m", "c": "#cfe6ff", "in": 4.5, "lx": -30},
              I.box(640, 270, 240, 150, "#2a2018", "#cbbca8", 2, 12, 1.2, fx="pop"), _fossil(710, 350, 90, 1.4), _fossil(810, 340, 70, 1.6), I.glow(760, 345, 120, 1.5, .5),
              I.label(760, 455, "skull pieces", 1.8, I.BONE, 28), I.arrow([[650, 1110], [700, 800], [740, 430]], 5.0, "#cbbca8", 2, "inferred", .8)]}
    # beat 5 on the map: matching tools offshore and inland; busy coasts, not high-tech
    tool = lambda x, y, at, c: {"k": "poly", "p": [[x - 9, y + 12], [x, y - 14], [x + 9, y + 12], [x, y + 16]], "fill": c, "c": "none", "w": 0, "in": at, "fx": "pop"}
    honest = []
    for k, ((lo, la), (lo2, la2)) in enumerate((((3, 54.5), (6, 51.0)), ((51.5, 26.5), (47.5, 31.5)), ((108, -1.0), (104, 3.0)))):
        (x1, y1), (x2, y2) = v.p(lo, la), v.p(lo2, la2)
        honest += [tool(x1, y1, 2.0 + .5 * k, I.BLUE), tool(x2, y2, 2.2 + .5 * k, I.AMBER), I.line([[x1, y1], [x2, y2]], 2.3 + .5 * k, I.BONE, 2, "inferred", .4)]
    honest += [I.glow(x, y, 40, round(5.6 + .15 * j, 2), .9, "fire") for j, (x, y) in enumerate(
        [v.p(lo, la) for lo, la in ((0, 55), (4, 53), (6.5, 55.5), (-2, 51.5), (49.5, 28), (52.5, 25.5), (54.5, 25.2), (100, 4), (105, -2), (112, -5), (115, 3), (98, 0))])]
    honest += [I.box(110, 1060, 70, 200, "none", I.LILAC, 3, 4, 12.4, style="claimed")] + [I.line([[122, 1080 + 30 * j], [168, 1080 + 30 * j]], 12.5, I.LILAC, 2, "claimed", .3) for j in range(6)] + \
              [I.strike(90, 1280, 200, 1040, 13.0)]
    tag = [I.box(x - 9, y - 9, 18, 18, "#ffffff", r=3, at=3.7 + .2 * k, fx="pop") for k, (x, y) in enumerate((v.p(34.93, 32.71), v.p(11.9, 54.2), v.p(112.8, -7.2)))] + \
          [I.ring(480, 820, 60, 5.6, I.BONE, 3), I.line([[523, 863], [570, 910]], 5.8, I.BONE, 6)] + \
          I.question(480, 840, 6.2, 46) + [I.glow(500, 760, 520, 10.6, .3)]
    return remix(ep, scenes={0: shelf, 2: village, 3: baltic, 4: ice, 5: dredge}, alias={6: 1}, cams={6: [1.12, 500, 880]},
                 adds={0: camps, 1: madd, 2: [_wave(150, 850, 560, .4, "#bfe6f5", 8, 14, 3, .8), {"k": "dim", "x1": 900, "y1": 566, "x2": 900, "y2": 930, "t": "10 m", "c": "#cfe6ff", "in": 8.3, "lx": -30}]},
                 beat_adds={2: (pulse, [1, 500, 980]), 4: (honest, None), 5: (tag, None)})


def _bubble(x, y, w, at, c="#e8b87a", style="known", fill="none", op=None):
    """A speech bubble (a told story), centred on x, y."""
    h = w * .62
    p = [[x - w / 2, y - h / 2], [x + w / 2, y - h / 2], [x + w / 2, y + h / 2], [x - w * .1, y + h / 2], [x - w * .3, y + h * .85], [x - w * .25, y + h / 2], [x - w / 2, y + h / 2]]
    e = {"k": "poly", "p": [[round(a, 1), round(b, 1)] for a, b in p], "fill": fill, "c": c, "w": 3, "style": style, "in": at, "fx": "pop"}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def aboriginal_m():
    """Stories older than the sea as one continuous take (see mural.py): the Ice Age coast of Australia, depth read as a date on the sea-level curve,
    a game of telephone with rules, and one night in 1700 written down on both sides of the Pacific."""
    from mural import remix
    import illus as I
    ep = aboriginal()
    au = _pins_relabel(ep["shots"][0], {"21 places around the coast with stories of the sea coming in": ""})
    isle = _iso_relabel(ep["shots"][1], {"the strait · dry until about 10,000 years ago": "the strait"}, spin=.12)
    v = View(112, 155, -44, -9, (40, 330, 920, 900))
    sahul = [(113.0, -21.5), (114.5, -19.5), (117.0, -18.0), (120.0, -16.0), (122.5, -14.0), (124.5, -12.3), (126.5, -11.0), (128.5, -9.6), (130.5, -9.0), (133.0, -8.0),
             (140.0, -7.5), (142.0, -9.2), (143.8, -11.0), (145.2, -14.5), (147.0, -17.0), (149.5, -20.0), (151.5, -22.5), (153.6, -25.0), (153.9, -28.5), (153.5, -31.5),
             (152.6, -33.5), (151.2, -35.5), (150.4, -37.6), (148.6, -38.8), (148.7, -40.6), (148.5, -42.5), (147.5, -44.2), (145.5, -44.2), (144.2, -42.0), (143.3, -40.0),
             (142.0, -39.0), (140.5, -38.8), (139.0, -37.6), (137.0, -36.6), (135.5, -35.7), (134.0, -34.6), (132.0, -33.6), (129.0, -33.2), (126.0, -33.6), (123.5, -34.6),
             (120.0, -35.1), (117.5, -35.7), (115.0, -34.8), (114.4, -33.0), (114.6, -30.0), (113.4, -27.0), (112.6, -24.0)]
    pins = [v.p(137.3, -34.0), v.p(137.2, -35.8), v.p(144.9, -38.1)]
    hook = [_bubble(x + dx, y - 54, 54, 1.7 + .2 * k, I.AMBER) for k, ((x, y), dx) in enumerate(zip(pins, (-40, 40, 0)))] + \
           [I.arrow([[x + dx * 2, y + 110], [x + dx, y + 30]], 4.0 + .15 * k, I.BLUE, 3, dur=.5, curve=False) for k, ((x, y), dx) in enumerate(zip(pins, (-30, 30, 0)))] + \
           [{"k": "poly", "p": [list(v.p(lo, la)) for lo, la in sahul], "fill": I.AMBER, "c": I.AMBER, "w": 3, "op": .22, "keepop": True, "style": "inferred", "curve": True, "in": 6.4, "fx": "fill", "dur": 1.4},
            I.label(70, 470, "the Ice Age coast", 6.9, I.AMBER, 30, "start")]
    whatif = [I.label(x + dx + 34, y - 84, "?", .3 + .2 * k, I.LILAC, 44, st="serif", fx="pop") for k, ((x, y), dx) in enumerate(zip(pins, (-40, 40, 0)))] + \
             [I.label(500, 1140, "10,000 years old?", 1.9, I.LILAC, 40, st="serif", fx="pop")]
    # 1 · Kangaroo Island: the waters rise; geology agrees, about 10,000 years ago
    kadd = [I.arrow([[860, 1150], [860, 980]], 3.9, I.BLUE, 4, dur=.8, curve=False), _wave(780, 940, 975, 4.1, "#bfe6f5", 8, 4, 3, .5)]
    geo = [_tick(250, 430, .6), I.box(300, 400, 420, 64, "none", I.GREEN, 3, 32, 4.8), I.label(510, 444, "about 10,000 years ago", 5.0, I.GREEN, 30)]
    # beat 3 on the map: twenty-one stories, and one question: how deep is the water over the land?
    story = [I.person(110, 1340, 110, .4), I.person(180, 1340, 110, .6), I.glow(145, 1290, 90, .5, .4)] + \
            [_bubble(300 + 96 * (k % 7), 1205 + 56 * (k // 7), 48, round(3.1 + .08 * k, 2), I.AMBER) for k in range(21)] + \
            [I.arrow([[pins[0][0] + 6, pins[0][1] + 60], [pins[0][0] + 6, pins[0][1] + 140]], 9.5, I.BLUE, 3, dur=.5, curve=False), I.label(pins[0][0] + 24, pins[0][1] + 150, "how deep?", 9.8, I.BLUE, 30, "start")]
    # 2 · depth to date on the sea-level curve; the window; twenty-one dots inside it
    X = lambda ya: round(180 + 680 * (14000 - ya) / 14000, 1)
    Y = lambda m: round(700 - m * 7.5, 1)
    cv = [(14000, -78), (13000, -68), (12000, -60), (11000, -50), (10000, -40), (9000, -28), (8000, -18), (7000, -7), (6000, -2.5), (4000, -1), (0, 0)]
    def at_depth(m):
        for (a1, m1), (a2, m2) in zip(cv, cv[1:]):
            if m1 <= m <= m2:
                return a1 + (a2 - a1) * (m - m1) / (m2 - m1)
    t30 = at_depth(-30)
    def on_curve(a):
        for (a1, m1), (a2, m2) in zip(cv, cv[1:]):
            if a2 <= a <= a1:
                return m1 + (m2 - m1) * (a1 - a) / (a1 - a2)
    graph = {"base": "dark", "cam": [1, 500, 880], "els": [I.line([[180, 640], [180, 1340], [880, 1340]], .3, "#8c7152", 3, dur=.8),
             I.label(170, Y(0) + 8, "0 m", .5, "#cbbca8", 28, "end"), I.label(170, Y(-60) + 8, "60 m", .5, "#cbbca8", 28, "end"),
             I.label(180, 1390, "14,000 years ago", .5, "#cbbca8", 28, "start"), I.label(880, 1390, "today", .5, "#cbbca8", 28, "end"),
             {"k": "line", "p": [[X(a), Y(m)] for a, m in cv], "c": SEA, "w": 5, "curve": True, "in": 1.6, "fx": "draw", "dur": 2.0},
             I.label(860, Y(0) - 20, "sea level", 2.2, I.BLUE, 30, "end"),
             _wave(300, 700, 440, .3, "#bfe6f5", 6, 8, 3, .6), {"k": "poly", "p": [[300, 600], [420, 560], [560, 540], [700, 520], [700, 620], [300, 620]], "fill": "#7a6248", "c": "#c9ad85", "w": 2, "in": .4},
             _bubble(500, 400, 70, .6, I.AMBER), {"k": "dim", "x1": 520, "y1": 446, "x2": 520, "y2": 544, "t": "depth", "c": "#cfe6ff", "in": 1.0, "lx": 50, "upright": True},
             I.box(176, Y(0), 10, Y(-30) - Y(0), I.BLUE, r=3, at=4.8, fx="fill"),
             I.arrow([[186, Y(-30)], [X(t30) - 6, Y(-30)]], 5.6, I.AMBER, 3, dur=.8, curve=False),
             I.arrow([[X(t30), Y(-30) + 6], [X(t30), 1334]], 6.6, I.AMBER, 3, dur=.7, curve=False), I.glow(X(t30), 1340, 60, 8.1, .9), I.label(X(t30), 1300, "a date", 8.2, I.AMBER, 30),
             I.box(X(13000), 1310, X(7000) - X(13000), 30, I.AMBER, r=8, at=9.5, op=.35, fx="pop"), I.label(X(7000) + 16, 1334, "7,000 to 13,000 years ago", 9.7, I.AMBER, 30, "start")] +
            [I.dot(X(a), Y(on_curve(a)), 8, I.AMBER, round(11.8 + .06 * k, 2)) for k, a in enumerate([13000 - 6000 * j / 20 for j in range(21)])] +
            [I.glow((X(13000) + X(7000)) / 2, Y(-40), 220, 13.6, .5)]}
    # 3 · the doubts; then a game of telephone, and telling with rules
    doubt = [I.box(60, 470, 560, 260, SEA, r=6, at=.3, op=.6), _wave(60, 620, 470, .3, "#bfe6f5", 6, 12, 3, .6),
             I.line([[260, 730], [262, 600]], .8, "#7a5a3a", 12, draw=False), I.line([[262, 640], [230, 600]], .9, "#7a5a3a", 6, draw=False), I.line([[262, 620], [296, 590]], .9, "#7a5a3a", 6, draw=False),
             {"k": "poly", "p": [[620, 470], [940, 470], [940, 730], [620, 730]], "fill": "#8a6a48", "c": "none", "w": 0, "in": .3},
             I.person(700, 470, 120, 2.2), I.line([[690, 380], [300, 610]], 2.8, I.LILAC, 2, "claimed", .8)] + I.question(470, 380, 4.1, 56) + \
            [I.box(740, 290, 170, 130, "#efe6d2", "#8a7a66", 2, 6, 6.4, fx="pop")] + \
            [I.line([[760, 315 + 20 * j], [760 + 110 + 20 * (j % 2), 315 + 20 * j]], 6.6 + .06 * j, "#5a4632", 3, dur=.3) for j in range(5)] + \
            [I.person(840, 640, 100, 7.0), I.label(820, 455, "written down later", 7.4, I.BONE, 28)]
    chain = []
    for k in range(6):
        x = 120 + 150 * k
        chain += [I.person(x, 1040, 90, 9.9 + .25 * k), _bubble(x + 40, 930, 60, 10.0 + .25 * k, I.LILAC, "claimed" if k else "known")]
        if k:
            chain.append(I.line([[x + 12 + 6 * j, 930 + (k * 3 if j % 2 else -k * 3)] for j in range(6)], 10.1 + .25 * k, I.LILAC, 2, dur=.3))
    chain += [I.label(500, 1100, "a game of telephone", 12.1, I.LILAC, 30)]
    for k in range(6):
        x = 120 + 150 * k
        chain += [I.person(x, 1330, 90, 16.2 + .15 * k), _bubble(x + 40, 1220, 60, 16.3 + .15 * k, I.AMBER)]
        if k:
            chain += [I.line([[x - 120, 1260], [x - 75, 1235], [x - 30, 1260]], 18.0 + .15 * k, I.GREEN, 3, dur=.3, curve=True), _tick(x - 75, 1210, 18.1 + .15 * k)]
    chain += [I.label(500, 1395, "checked by kin", 19.0, I.GREEN, 30), I.label(880, 1150, "300 generations", 9.9, I.BONE, 28, "end")]
    # 4 · one night in January 1700, on both sides of the Pacific
    jap = {"k": "poly", "p": [[60, 380], [150, 420], [190, 560], [170, 760], [220, 940], [180, 1080], [100, 1160], [60, 1160]], "fill": "#6f7a4a", "c": "#c9d79a", "w": 2, "curve": True, "in": .3}
    ame = {"k": "poly", "p": [[940, 360], [860, 420], [840, 600], [870, 820], [830, 1000], [860, 1200], [940, 1260]], "fill": "#6f7a4a", "c": "#c9d79a", "w": 2, "curve": True, "in": .3}
    pac = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(60, 340, 880, 940, "#1d3a4a", r=12, at=.1), jap, ame, I.label(120, 1220, "Japan", .5, "#c9d79a", 32),
           I.label(880, 1310, "America", .5, "#c9d79a", 32, "end"), I.label(500, 1220, "the Pacific", .6, I.BLUE, 34, st="ital")] +
          [I.glow(925, 850, 60, 4.4, .9, "fire"), I.dot(925, 858, 8, "#ffcf8a", 4.4)] + [I.person(895, 862, 70, 4.3)] + [_bubble(870, 750, 64, 4.5, I.AMBER)] +
          [I.line([[870 + 10 * (j % 2), 900 + 24 * j] for j in range(9)], 6.2, "#ffcf8a", 3, dur=.5)] +
          [{"k": "line", "p": I.ellipse(850, 820, 110 + 105 * j, 110 + 105 * j, 24, 150, 210), "c": "#9fd0ff", "w": 4, "curve": True, "in": round(8.7 + .35 * j, 2), "fx": "draw", "dur": .5} for j in range(6)] +
          _scroll(190, 700, 90, 7.4) + [I.label(200, 640, "January 1700", 12.3, I.AMBER, 30, "start")] +
          [I.dot(500, 430, 34, "#efe8da", 13.2), I.dot(516, 420, 34, "#1d3a4a", 13.2), I.glow(500, 430, 110, 13.2, .5),
           I.line([[260, 640], [480, 470]], 13.3, I.BONE, 2, "inferred", .6), I.line([[720, 690], [520, 470]], 13.3, I.BONE, 2, "inferred", .6), I.label(500, 380, "same night", 13.4, I.BONE, 32)]}
    tag = [I.glow(590, 1260, 360, 3.0, .45)] + [_tick(300 + 96 * (k % 7), 1203 + 56 * (k // 7), round(4.6 + .05 * k, 2), s=.6) for k in range(21)] + \
          [I.person(330 + 80 * k, 1420, 64, 8.2 + .1 * k) for k in range(7)] + [I.glow(590, 1390, 300, 8.4, .5, "lamp")]
    return remix(ep, scenes={0: au, 1: isle, 2: graph, 3: {"base": "dark", "cam": [1, 500, 880], "els": doubt + chain}, 4: pac}, alias={5: 0}, cams={5: [1.12, 500, 900]},
                 adds={0: hook, 1: kadd}, line_adds={(0, 1): (whatif, None), (1, 1): (geo, None)}, beat_adds={2: (story, None), 5: (tag, None)})


def _anchor(x, y, s, at, c="#c9b48c"):
    """A stone anchor (a pierced triangular slab), centred on x, y."""
    return [{"k": "poly", "p": [[x - s * .5, y + s * .45], [x + s * .5, y + s * .45], [x, y - s * .55]], "fill": c, "c": "#8a7452", "w": 1.5, "in": at, "fx": "pop"},
            {"k": "circle", "x": x, "y": round(y - s * .12, 1), "r": round(s * .1, 1), "fill": "#1a1511", "c": "none", "w": 0, "in": at}]


def _skyline(x0, y, at, c="#e8c35a", s=1.0):
    """A city of the epic, in gold line: towers, domes and a gate (an illustration, not a reconstruction)."""
    out = []
    for k, (dx, w, h, dome) in enumerate(((0, 70, 120, 1), (80, 50, 170, 0), (140, 90, 140, 1), (240, 60, 200, 0), (310, 110, 110, 1), (430, 60, 160, 0), (500, 80, 130, 1))):
        x = x0 + dx * s
        out.append({"k": "rect", "x": round(x, 1), "y": round(y - h * s, 1), "w": round(w * s, 1), "h": round(h * s, 1), "r": 2, "fill": "rgba(232,195,90,.18)", "c": c, "sw": 2.5, "in": round(at + .12 * k, 2), "fx": "rise"})
        if dome:
            out.append({"k": "poly", "p": [[round(x + w * s * a, 1), round(y - h * s - w * s * .5 * math.sin(math.pi * a), 1)] for a in [j / 10 for j in range(11)]], "fill": "rgba(232,195,90,.18)", "c": c, "w": 2.5, "in": round(at + .12 * k + .1, 2), "fx": "rise"})
    return out


def dwarka_m():
    """Dwarka as one continuous take (see mural.py): the epic's golden city drawn as an illustration, the dives, sonar explained,
    a date on wood, a dredge that shuffles the pages, a harbour of anchors, and a survey still under way. Faith is never weighed."""
    from mural import remix
    import illus as I
    ep = dwarka()
    site = _iso_relabel(ep["shots"][0], {"stone anchors · well over a hundred": "anchors · over a hundred", "off Dwarka · 3 to 16 m under the sea": "3 to 16 m down"}, spin=.12)
    # 5 · the hook: the epic, as an illustrated leaf; then the real sea floor, blocks and anchors
    leaf = [I.box(70, 340, 860, 360, "#d8b878", "#8a6a3e", 3, 60, .2, fx="pop"), I.box(250, 360, 500, 320, "#2a2018", r=16, at=.4),
            {"k": "glyphs", "x": 100, "y": 380, "w": 130, "h": 280, "rows": 7, "cols": 3, "c": "#5a3a1a", "seed": 4, "in": .5},
            {"k": "glyphs", "x": 770, "y": 380, "w": 130, "h": 280, "rows": 7, "cols": 3, "c": "#5a3a1a", "seed": 9, "in": .5}] + _skyline(268, 650, .8, s=.8) + \
           [I.glow(500, 560, 220, 1.4, .6, "lamp"), I.box(252, 480, 496, 198, SEA, r=12, at=3.0, op=.75, fx="fill", dur=2.5), _wave(260, 740, 480, 4.8, "#bfe6f5", 6, 10, 3, .8)]
    floor = [I.box(60, 820, 880, 600, "#1d3a4a", r=8, at=.2), _wave(60, 940, 820, .3, "#bfe6f5", 6, 20, 3, .8), I.box(60, 1330, 880, 90, "#8a7452", r=0, at=.4),
             _diver(300, 950, 110, 1.0), I.glow(300, 950, 90, 1.0, .4)] + \
            sum([_block(420 + 90 * k, 1335, 80, 44, 4.0 + .15 * k, "#c9b48c", fx="pop") for k in range(4)], []) + \
            sum([_anchor(100 + 52 * (k % 16) + 18 * ((k // 16) % 2), 1270 - 32 * (k // 16), 18, round(6.2 + .012 * k, 3)) for k in range(112)], []) + \
            [I.label(500, 1395, "more than 100 anchors", 7.4, I.BONE, 30)]
    # 0 · the dives: oceanographers mapping blocks, walls and anchors, 3 to 16 m down
    dives = [_diver(240, 480, 110, .6), _diver(720, 520, 110, 1.0), I.line([[260, 540], [700, 560]], 1.4, I.AMBER, 2, "inferred", 1.0),
             I.line(I.ellipse(500, 420, 160, 50, 16, 200, 340), 4.8, "#c9b48c", 6, curve=True)]
    # 1 · Bet Dwarka: a settlement about 3,500 years old
    bx_, by_ = 261.5, 638.8
    bet = _houses(bx_ + 30, by_ - 40, 4, .5, 26) + [I.glow(bx_, by_, 100, .4, .7), I.label(bx_ + 30, by_ - 100, "about 3,500 years old", 3.6, I.AMBER, 30, "start")]
    # 2 · sonar: a ship sends sound down and listens; shapes 40 m down, never excavated
    sonar = {"base": "dark", "cam": [1, 500, 860], "els": [I.box(60, 420, 880, 580, SEA, r=0, at=.2, op=.55), _wave(60, 940, 420, .2, "#bfe6f5", 8, 20, 3, .8),
             I.box(60, 1000, 880, 80, "#6f5a44", r=0, at=.3), {"k": "boat", "x": 500, "y": 420, "w": 200, "in": .4},
             {"k": "fan", "x": 500, "y": 440, "a0": 62, "a1": 118, "r": 560, "n": 11, "in": 1.4},
             {"k": "dim", "x1": 900, "y1": 426, "x2": 900, "y2": 996, "t": "40 m", "c": "#cfe6ff", "in": 3.9, "lx": -30},
             I.box(160, 1120, 680, 280, "#161a14", "#3a4a30", 2, 10, 2.9, fx="pop")] +
            [I.box(200 + 130 * (k % 5), 1150 + 120 * (k // 5), 90, 70, "none", "#7fb07a", 2, 3, round(3.2 + .1 * k, 2), op=.75) for k in range(10)] +
            [{"k": "line", "p": I.ellipse(500, 440, 140 * j, 140 * j * .9, 20, 60, 120), "c": I.BLUE, "w": 4, "curve": True, "in": round(5.6 + .35 * j, 2), "fx": "draw", "dur": .4} for j in (1, 2, 3)] +
            [{"k": "line", "p": I.ellipse(500, 990, 120 * j, 100 * j, 20, 240, 300), "c": I.AMBER, "w": 3, "style": "inferred", "curve": True, "in": round(6.6 + .3 * j, 2)} for j in (1, 2, 3)] +
            [I.glow(500, 1260, 300, 8.5, .5, "lamp")]}
    # 3 · the wood: dated to about 7500 BCE; a city? if it's a city
    wood = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "poly", "p": [[220, 980], [700, 940], [720, 1040], [240, 1080]], "fill": "#7a5232", "c": "#c9905a", "w": 2, "in": .3, "fx": "pop"},
            I.oval(720, 990, 30, 50, "#a0784a", "#c9905a", 2, 1, .3)] + [I.ring(720, 990, 10 + 9 * j, .5 + .1 * j, "#6a4426", 2) for j in range(3)] +
           [I.box(380, 860, 260, 70, "#efe6d2", "#8a7a66", 2, 8, 3.5, fx="pop"), I.label(510, 908, "c. 7500 BCE", 3.7, "#1a1511", 34, st="serif", halo=False),
            I.line([[510, 930], [480, 970]], 3.6, "#efe6d2", 2, draw=False)] +
           [{"k": "rect", "x": 300 + 80 * k, "y": 560 - 40 * (k % 3), "w": 60, "h": 140 + 40 * (k % 3), "r": 2, "fill": "none", "c": I.LILAC, "sw": 3, "style": "claimed", "in": round(6.4 + .15 * k, 2)} for k in range(5)] +
           I.question(500, 470, 9.2, 80)}
    # 4 · the dredge shuffles the pages; a date on wood dates the wood
    L0 = 520
    strata = [I.box(60, L0 + 90 * k, 560, 90, c, r=0, at=round(.1 + .1 * k, 2), fx="fill") for k, c in enumerate(("#8a7452", "#6f5a44", "#7a6248", "#5a4632"))]
    items = [{"k": "poly", "p": [[150, L0 + 40], [175, L0 + 20], [200, L0 + 45]], "fill": "#cbbca8", "c": "none", "w": 0, "in": .5},
             I.oval(380, L0 + 135, 30, 18, "#b0503a", "none", 0, 1, .55), I.box(240, L0 + 210, 110, 26, "#7a5232", r=10, at=.6), I.dot(520, L0 + 315, 14, "#cbbca8", .65)]
    pages = [I.line([[640, L0 + 45 + 90 * k], [700, L0 + 45 + 90 * k]], 3.4 + .15 * k, I.BONE, 2, "inferred", .3) for k in range(4)] + \
            [I.label(720, L0 + 60 + 90 * k, t, 3.5 + .15 * k, I.BONE, 28, "start") for k, t in enumerate(("page 1", "page 2", "page 3", "page 4"))]
    scoop = [I.arrow([[560, 380], [430, 600], [300, 760], [160, 700]], 1.7, "#cbd2d8", 4, dur=1.2), I.box(640, 340, 300, 120, "#3a3128", "#cbbca8", 2, 10, 2.2, fx="pop"),
             {"k": "poly", "p": [[745, 335], [760, 310], [775, 338]], "fill": "#cbbca8", "c": "none", "w": 0, "in": 2.4}, I.oval(820, 420, 26, 15, "#b0503a", "none", 0, 1, 2.45),
             I.box(690, 380, 100, 24, "#7a5232", r=10, at=2.5), I.dot(880, 395, 13, "#cbbca8", 2.55), I.label(790, 500, "no layers", 2.8, I.RED, 30),
             I.arrow(I.ellipse(790, 400, 120, 40, 16, 200, 520), 6.8, I.AMBER, 3, "inferred", .9)]
    tree = [I.line([[160, 1000], [160, 880]], 9.0, "#7a5232", 12, draw=False), I.oval(160, 850, 60, 50, "#5f7a45", "none", 0, 1, 9.0),
            I.line([[230, 990], [380, 990]], 9.8, "#7a5232", 14, draw=False), I.label(305, 960, "the tree died", 10.0, I.AMBER, 28),
            I.person(560, 1000, 100, 11.0, c=I.LILAC), I.label(560, 1040, "who used it?", 11.2, I.LILAC, 28)] + I.question(620, 880, 11.4, 50)
    shuffle = {"base": "dark", "cam": [1, 500, 860], "els": strata + items + pages + scoop + tree}
    Xh = lambda ya: round(140 + 720 * (2400 - ya) / 2400, 1)
    harbour = [I.line([[120, 1300], [880, 1300]], .2, "#8c7152", 3), I.label(Xh(2000), 1350, "2,000 years ago", .4, "#cbbca8", 28), I.label(Xh(600), 1350, "medieval", .4, "#cbbca8", 28),
               I.label(880, 1390, "today", .4, "#cbbca8", 28, "end"), I.box(Xh(2000), 1280, Xh(600) - Xh(2000), 20, I.AMBER, r=10, at=5.0, op=.7, fx="pop")] + \
              sum([_anchor(Xh(2000) + 50 * k, 1230, 30, round(5.3 + .06 * k, 2)) for k in range(int((Xh(600) - Xh(2000)) / 50) + 1)], []) + \
              [{"k": "boat", "x": 300 + 160 * k, "y": 1160, "w": 90, "in": round(3.0 + .2 * k, 2)} for k in range(3)] + \
              [I.box(Xh(600) + 10, 1100, Xh(0) - Xh(600) - 20, 200, SEA, r=6, at=10.0, op=.6, fx="fill"), _wave(Xh(600) + 10, Xh(0) - 10, 1100, 10.2, "#bfe6f5", 8, 4, 3, .6)]
    # beat 5 on the site: the sea took a harbour over centuries; 2025, a new survey, results pending
    slow = [I.arrow([[880, 1400], [880, 1250]], .8, I.BLUE, 4, dur=1.4, curve=False), I.label(860, 1235, "over centuries", 4.6, I.BLUE, 28, "end"),
            I.box(120, 1290, 150, 60, "none", I.AMBER, 3, 30, 6.2), I.label(195, 1332, "2025", 6.3, I.AMBER, 32), _diver(380, 1320, 100, 8.7),
            I.box(520, 1260, 160, 120, "none", I.LILAC, 3, 8, 11.2, style="claimed"), I.label(600, 1400, "results", 11.3, I.LILAC, 28)] + I.question(600, 1330, 11.4, 54)
    tag = [_tick(870, 900, 6.6), I.glow(500, 950, 300, 6.8, .35)] + \
          [I.box(250, 300, 90, 60, "#c9b48c", "#8a7452", 2, 4, 11.2, fx="pop"), I.box(440, 300, 120, 60, "#efe6d2", "#8a7a66", 2, 8, 12.3, fx="pop"),
           I.label(500, 342, "date", 12.3, "#1a1511", 28, halo=False)] + [I.box(660, 300 + 15 * k, 100, 15, c, r=0, at=13.1) for k, c in enumerate(("#8a7452", "#6f5a44", "#7a6248", "#5a4632"))]
    return remix(ep, scenes={0: site, 2: sonar, 3: wood, 4: shuffle, 5: {"base": "dark", "cam": [1, 500, 880], "els": leaf}}, alias={6: 0}, cams={6: [1.12, 500, 900]},
                 adds={0: dives, 1: bet}, line_adds={(0, 1): (floor, None), (3, 1): (harbour, [1, 500, 1000])}, beat_adds={4: (slow, None), 5: (tag, None)})


def _satellite(x, y, s, at):
    """A small satellite: a body and two solar panels."""
    return [{"k": "rect", "x": x - s * .25, "y": y - s * .2, "w": s * .5, "h": s * .4, "r": 4, "fill": "#cbd2d8", "c": "#8a939c", "sw": 2, "in": at, "fx": "pop"},
            {"k": "rect", "x": x - s * 1.05, "y": y - s * .14, "w": s * .7, "h": s * .28, "r": 2, "fill": "#2c4a72", "c": "#9fd0ff", "sw": 1.5, "in": at + .1, "fx": "pop"},
            {"k": "rect", "x": x + s * .35, "y": y - s * .14, "w": s * .7, "h": s * .28, "r": 2, "fill": "#2c4a72", "c": "#9fd0ff", "sw": 1.5, "in": at + .1, "fx": "pop"}]


def _diya(x, y, s, at):
    """An oil lamp with a flame: a gentle sign of a sacred place (no rating, only respect)."""
    return [{"k": "poly", "p": [[x - s, y - s * .2], [x + s, y - s * .2], [x + s * .6, y + s * .35], [x - s * .6, y + s * .35]], "fill": "#c9905a", "c": "#e8c89a", "w": 2, "curve": True, "in": at, "fx": "pop"},
            {"k": "poly", "p": [[x + s * .5, y - s * .9], [x + s * .7, y - s * .45], [x + s * .5, y - s * .25], [x + s * .3, y - s * .45]], "fill": "#ffcf8a", "c": "none", "w": 0, "curve": True, "in": at + .3},
            {"k": "glow", "x": x + s * .5, "y": y - s * .55, "r": s * 2.2, "kind": "lamp", "op": .8, "keepop": True, "in": at + .3}]


def rama_m():
    """Rama Setu as one continuous take (see mural.py): a line seen from space, a laser from orbit, two seas piling sand, a strait that was dry land,
    and the drill core nobody has taken. The epic is honoured, never rated; only the ridge is weighed."""
    from mural import remix
    import illus as I
    ep = rama_setu()
    shoals = _iso_relabel(ep["shots"][0], {"shoals · 1 to 3 m under water": "shoals · 1 to 3 m deep"}, spin=.12)
    seen = [{"k": "dim", "x1": 110, "y1": 1260, "x2": 890, "y2": 1260, "t": "48 km", "c": I.AMBER, "in": 1.4}] + _satellite(820, 360, 70, 5.2) + \
           [I.line([[800, 390], [560, 760]], 5.6, "#9fd0ff", 2, "inferred", .8), I.line([[840, 390], [700, 820]], 5.6, "#9fd0ff", 2, "inferred", .8)]
    epic = [I.box(80, 290, 620, 220, "#d8b878", "#8a6a3e", 3, 50, .6, fx="pop"), I.box(220, 305, 340, 190, "#2a2018", r=14, at=.7),
            {"k": "glyphs", "x": 100, "y": 320, "w": 105, "h": 160, "rows": 5, "cols": 2, "c": "#5a3a1a", "seed": 3, "in": .8},
            {"k": "glyphs", "x": 575, "y": 320, "w": 105, "h": 160, "rows": 5, "cols": 2, "c": "#5a3a1a", "seed": 7, "in": .8},
            _wave(225, 555, 450, 1.0, "#9fd0ff", 5, 8, 2, .6)] + \
           [I.dot(240 + 20 * j, 446, 7, "#e8c35a", round(2.4 + .05 * j, 2)) for j in range(16)] + \
           [{"k": "person", "x": 270 + 60 * j, "y": 440, "h": 60, "t": False, "color": "#e8c35a", "in": round(2.6 + .15 * j, 2), "fx": "rise"} for j in range(5)] + \
           [I.dot(270 + 60 * j, 372, 8, "#e8c35a", round(2.7 + .15 * j, 2)) for j in range(5)] + \
           _diya(800, 600, 36, 4.4) + \
           [I.box(300, 1310, 150, 70, "none", I.AMBER, 3, 10, 6.4), I.label(375, 1418, "built?", 6.5, I.AMBER, 30)] + \
           [I.line([[310 + 14 * j, 1372 - 22 * (j % 3)], [330 + 14 * j, 1372 - 22 * (j % 3)]], 6.45, I.AMBER, 8, draw=False) for j in range(8)] + \
           [{"k": "poly", "p": [[560, 1380], [610, 1330], [660, 1310], [710, 1330], [760, 1380]], "fill": "#e2cf9e", "c": "none", "w": 0, "curve": True, "in": 6.9, "fx": "rise"},
            I.label(660, 1418, "grown?", 7.0, I.BLUE, 30), I.label(518, 1370, "or", 6.7, I.BONE, 28)]
    # 1 · the map: sandbanks 1 to 3 m deep along the line
    v = View(78.9, 80.3, 8.55, 9.75, (40, 330, 920, 900))
    (ax_, ay_), (bx2, by2) = v.p(79.44, 9.17), v.p(79.71, 9.1)
    banks = [I.oval(round(ax_ + (bx2 - ax_) * f, 1), round(ay_ + (by2 - ay_) * f, 1), 16, 7, "#e2cf9e", "none", 0, 1, round(1.0 + .12 * k, 2)) for k, f in enumerate([j / 9 for j in range(10)])] + \
            [I.label((ax_ + bx2) / 2 + 20, (ay_ + by2) / 2 + 100, "1 to 3 m deep", 2.8, "#e2cf9e", 30), {"k": "boat", "x": (ax_ + bx2) / 2 - 10, "y": (ay_ + by2) / 2 - 60, "w": 70, "in": 4.0}]
    # 2 · the laser: pulses of green light down and back; the ridge carries on from both land tips
    SURF = 820
    floor = [(120 + 760 * j / 24, round(SURF + 22 + 6 * math.sin(j * .9), 1)) for j in range(25)]
    laser = {"base": "dark", "stars": 80, "cam": [1, 500, 880], "els": _satellite(500, 360, 90, .4) +
             [I.box(60, SURF, 880, 560, SEA, r=0, at=.3, op=.6), _wave(60, 940, SURF, .3, "#bfe6f5", 6, 20, 3, .8),
              {"k": "poly", "p": [[60, 760], [150, 760], [180, SURF + 20], [60, SURF + 20]], "fill": "#8aa05a", "c": "none", "w": 0, "in": .6},
              {"k": "poly", "p": [[940, 760], [850, 760], [820, SURF + 20], [940, SURF + 20]], "fill": "#8aa05a", "c": "none", "w": 0, "in": .6},
              I.label(110, 730, "India", .8, "#c9d79a", 30), I.label(890, 730, "Sri Lanka", .8, "#c9d79a", 30, "end"),
              I.box(60, 1000, 880, 380, "#6f5a44", r=0, at=.5, op=.8)] +
             [I.line([[500, 400], [x, y]], round(3.2 + .2 * j, 2), "#7fe3a8", 2, "known", .3, op=.8) for j, (x, y) in enumerate(floor[::3])] +
             [I.line([[x, y], [500, 400]], round(3.4 + .2 * j, 2), "#7fe3a8", 2, "inferred", .3, op=.5) for j, (x, y) in enumerate(floor[::3])] +
             [I.dot(x, y, 7, "#7fe3a8", round(6.6 + .06 * j, 2)) for j, (x, y) in enumerate(floor)] +
             [{"k": "line", "p": [[x, y] for x, y in floor], "c": "#e2cf9e", "w": 5, "curve": True, "in": 9.4, "fx": "draw", "dur": 1.0},
              I.label(500, SURF + 90, "the ridge", 9.8, "#e2cf9e", 32)]}
    # 3 · two seas meet and pile sand into a ridge; sand, beachrock, coral; snow against a fence
    MID = 880
    seas = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(60, 480, 880, MID - 480, SEA, r=0, at=.2, op=.7), I.box(60, MID + 40, 880, 1300 - MID - 40, SEA, r=0, at=.2, op=.7),
             {"k": "poly", "p": [[60, 480], [160, 480], [190, 1300], [60, 1300]], "fill": "#8aa05a", "c": "none", "w": 0, "in": .3},
             {"k": "poly", "p": [[940, 480], [840, 480], [810, 1300], [940, 1300]], "fill": "#8aa05a", "c": "none", "w": 0, "in": .3},
             I.label(330, 560, "the northern sea", 2.6, "#cfe6ff", 28), I.label(500, 1250, "the southern sea", 2.8, "#cfe6ff", 28)] +
            [I.dot(220 + 12 * j, 330 + 8 * (j % 3), 5, "#e2cf9e", .6 + .02 * j) for j in range(10)] + [I.label(270, 420, "sand", .8, I.BONE, 28),
             I.box(420, 320, 130, 40, "#c9b48c", "#8a7452", 2, 4, 1.2, fx="pop"), I.label(485, 420, "beachrock", 1.4, I.BONE, 28)] +
            [I.line([[700, 370], [700 + 30 * math.cos(a), 370 - 50 * math.sin(a)]], 1.8, "#ff9fb0", 4, dur=.3) for a in (1.2, 1.57, 1.94)] + [I.label(700, 420, "coral", 2.0, I.BONE, 28)] +
            [I.arrow([[260 + 120 * k, 640], [270 + 120 * k, MID - 20]], round(4.4 + .15 * k, 2), "#bfe6f5", 3, dur=.5, curve=False) for k in range(5)] +
            [I.arrow([[320 + 120 * k, 1140], [310 + 120 * k, MID + 60]], round(4.6 + .15 * k, 2), "#bfe6f5", 3, dur=.5, curve=False) for k in range(5)] +
            [I.box(170, MID, 660, 40, "#e2cf9e", r=12, at=5.6, fx="pop")] + [I.dot(x, y, 4, "#f5ecdc", round(5.8 + .01 * k, 2)) for k, (x, y) in enumerate(I.scatter(60, 190, 810, MID + 6, MID + 34, 6))] +
            [I.line([[700 + 30 * j, 1390], [700 + 30 * j, 1330]], 7.6, "#8a6a48", 4, draw=False) for j in range(6)] + [I.line([[690, 1345], [860, 1345]], 7.6, "#8a6a48", 3, draw=False),
             {"k": "poly", "p": [[600, 1395], [700, 1340], [720, 1395]], "fill": "#f5ecdc", "c": "none", "w": 0, "curve": True, "in": 8.0, "fx": "rise"},
             I.arrow([[560, 1350], [640, 1360]], 8.0, "#f5ecdc", 3, dur=.4), I.glow(500, MID + 20, 380, 9.2, .5)]}
    walked = _scroll(250, 760, 70, .2) + [I.person(280, MID + 10, 70, .4), I.person(340, MID + 10, 70, .6), I.arrow([[370, MID - 40], [470, MID - 40]], .9, I.BONE, 2, "inferred", .5)] + \
             [I.oval(620 + 70 * k, 470, 70, 30, "#5a6470", "none", 0, .9, 2.2 + .15 * k) for k in range(3)] + \
             [I.line([[650, 500], [628, 600], [660, 600], [622, 760]], 2.8, "#ffe2a8", 4, dur=.3)] + \
             [I.box(560, MID - 4, 90, 48, SEA, r=0, at=3.4, fx="pop"), _wave(560, 650, MID + 2, 3.6, "#bfe6f5", 6, 2, 3, .3), I.label(605, MID - 40, "1480", 4.9, I.AMBER, 34, st="serif")]
    # 4 · the Ice Age: the strait dry, with lakes; then the sea comes in around the ridge
    dry = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(60, 420, 880, 900, "#9a8a5a", r=12, at=.3),
            {"k": "poly", "p": [[60, 420], [200, 420], [230, 1320], [60, 1320]], "fill": "#6f7a4a", "c": "none", "w": 0, "in": .4},
            {"k": "poly", "p": [[940, 420], [800, 420], [770, 1320], [940, 1320]], "fill": "#6f7a4a", "c": "none", "w": 0, "in": .4},
            I.label(130, 400, "India", .6, "#c9d79a", 30), I.label(870, 400, "Sri Lanka", .6, "#c9d79a", 30),
            I.box(200, 870, 600, 40, "#e2cf9e", r=12, at=.8)] +
           [I.oval(x, y, rx, ry, SEA, "#9fd0ff", 2, .9, round(4.4 + .2 * k, 2)) for k, (x, y, rx, ry) in enumerate(((330, 600, 70, 40), (560, 700, 90, 45), (450, 1100, 80, 40), (680, 1180, 60, 30)))] +
           [I.label(560, 640, "lakes", 5.2, "#cfe6ff", 28),
            I.box(215, 420, 570, 448, SEA, r=0, at=6.8, op=.85, fx="fill", dur=2.0), I.box(215, 912, 570, 408, SEA, r=0, at=7.0, op=.85, fx="fill", dur=2.0),
            I.box(380, 1140, 240, 64, "none", I.BLUE, 3, 32, 8.8), I.label(500, 1182, "8,500 years ago", 9.0, "#cfe6ff", 30),
            I.glow(500, 890, 260, 13.5, .7), I.label(500, 840, "older than the sea", 13.7, I.AMBER, 32)]}
    # 5 · the drill core nobody has taken; a human layer, never tested
    drill = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(60, 600, 880, 820, SEA, r=0, at=.2, op=.55), _wave(60, 940, 600, .2, "#bfe6f5", 6, 20, 3, .8),
             {"k": "poly", "p": [[60, 1100], [240, 1000], [400, 720], [600, 720], [760, 1000], [940, 1100], [940, 1420], [60, 1420]], "fill": "#e2cf9e", "c": "#f5ecdc", "w": 2, "in": .3},
             {"k": "poly", "p": [[60, 1240], [300, 1150], [700, 1150], [940, 1240], [940, 1420], [60, 1420]], "fill": "#a08a5a", "c": "none", "w": 0, "in": .5},
             {"k": "boat", "x": 500, "y": 600, "w": 160, "in": .8}, I.line([[500, 470], [500, 590]], .9, "#cbd2d8", 6, draw=False),
             I.line([[500, 610], [500, 1300]], 1.2, I.AMBER, 4, "inferred", 1.2), I.label(530, 1330, "drilled: never", 1.8, I.AMBER, 30, "start")] +
            [I.box(130, 330, 60, 250, "#e2cf9e", "#8a7452", 2, 20, 3.2, fx="fill")] + [I.box(132, 360 + 50 * j, 56, 22, c, r=2, at=3.6 + .1 * j) for j, c in enumerate(("#c9b48c", "#ff9fb0", "#a08a5a", "#c9b48c"))] +
            [I.label(210, 470, "a core", 3.8, I.BONE, 28, "start"),
             {"k": "rect", "x": 400, "y": 692, "w": 200, "h": 28, "r": 6, "fill": "none", "c": I.LILAC, "sw": 3, "style": "claimed", "in": 7.6},
             I.label(500, 680, "placed by people?", 8.0, I.LILAC, 30)] + I.question(650, 760, 12.3, 54)}
    verdict = [_tick(780, 900, 4.8), I.label(760, 960, "natural ridge", 5.0, I.GREEN, 30)] + _diya(820, 420, 36, 8.0) + [I.glow(500, 900, 360, 12.1, .35)]
    return remix(ep, scenes={0: shoals, 2: laser, 3: seas, 4: dry, 5: drill}, cams={5: [1, 500, 880]},
                 adds={0: seen, 1: banks}, line_adds={(0, 1): (epic, None), (2, 1): (walked, None)}, beat_adds={5: (verdict, None)})


def _sea(C, data):
    """The sea rises 120 metres in every niche while the hook says so."""
    rise = [e for i in range(C.n) for e in C.sea(i, at=.3 + .09 * i)] + [
        {"k": "arrow", "p": [[986, C.Y1], [986, C.Y1 - 330]], "c": "#9fd0ff", "w": 3, "fx": "draw", "dur": 1.8, "in": .3},
        {"k": "label", "x": 940, "y": C.Y0 - 44, "t": "sea level +120 m", "a": "end", "st": "small", "c": "#9fd0ff", "size": 34, "scl": True, "in": 1.6}]
    return {"hook": rise}


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/drowned-ledger.json)."""
    import recap
    return recap.recap(ledger, "drowned-ledger", _sea)


def EPISODES():
    return [richat_m(), atlantis_m(), bimini_m(), yonaguni_m(), lost_civ_m(), drowned_m(), aboriginal_m(), dwarka_m(), rama_m(), ledger_recap()]
