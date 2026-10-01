"""File 08 · Sky Watchers. What the ancients saw overhead, and what they wrote down.
The Nebra sky disc, the Great Year, Serpent Mound, the Edfu texts and the plasma petroglyphs."""
import math, random
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box, sphere

SERIES = "Sky Watchers"
PATINA = "#3f6e5a"; AU = "#e8c35a"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "space",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


def arc(cx, cy, r, a0, a1, n=24):
    return [[round(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), 1), round(cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / n)), 1)] for k in range(n + 1)]


# ---------------------------------------------------------------- 08.01 The Nebra sky disc
def nebra():
    cx, cy, R = 500, 860, 300
    r = random.Random(32)
    stars = []
    while len(stars) < 25:
        x, y = r.uniform(-240, 240), r.uniform(-240, 240)
        if x * x + y * y < 230 ** 2 and not (x < -40 and y < -40) and not (x > 60 and y < -20 and x < 220) and not (-60 < x < 60 and 40 < y < 120):
            stars.append((x, y))
    stars += [(30 + dx, -80 + dy) for dx, dy in ((0, 0), (22, -8), (40, 6), (14, 18), (32, 26), (52, -14), (-10, 22))]
    disc = [{"k": "circle", "x": cx, "y": cy, "r": R, "fill": PATINA, "c": "#8fb5a0", "w": 3, "in": .1},
            {"k": "circle", "x": cx - 120, "y": cy - 110, "r": 70, "fill": AU, "c": "none", "w": 0, "in": .4},
            {"k": "circle", "x": cx + 140, "y": cy - 90, "r": 70, "fill": AU, "c": "none", "w": 0, "in": .5},
            {"k": "circle", "x": cx + 172, "y": cy - 108, "r": 64, "fill": PATINA, "c": "none", "w": 0, "in": .5}] + \
           [{"k": "circle", "x": cx + x, "y": cy + y, "r": 9, "fill": AU, "c": "none", "w": 0, "in": .6 + i * .03} for i, (x, y) in enumerate(stars)] + \
           [{"k": "line", "p": arc(cx, cy, R - 18, 139, 221), "c": AU, "w": 16, "curve": True, "in": 1.4},
            {"k": "line", "p": arc(cx, cy, R - 18, -41, 41), "c": AU, "w": 16, "curve": True, "op": .25, "style": "inferred", "in": 1.5},
            {"k": "line", "p": arc(cx, cy + 330, 190, 60, 120), "c": AU, "w": 10, "curve": True, "in": 1.7},
            {"k": "cap", "x": 500, "y": 480, "t": "bronze and gold · about 32 cm · schematic", "in": .2},
            {"k": "label", "x": 560, "y": 700, "t": "7 stars: the Pleiades?", "st": "small", "c": AU, "a": "start", "in": 2.0},
            {"k": "label", "x": 500, "y": 1240, "t": "sun or full Moon · crescent · 32 stars · horizon arcs · a boat", "c": AMBER, "in": 2.2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": disc}
    v = View(-7, 18, 45, 56, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Nebra · the Mittelberg", 11.521, 51.284, {"c": GOLD}), ("Mitterberg · the copper", 13.13, 47.43, {"a": "end", "lx": -18}), ("Cornwall · the gold", -5.0, 50.3, {"a": "start", "ly": 34})],
                 extra=[{"k": "line", "p": [v.p(13.13, 47.43), v.p(11.521, 51.284)], "c": "#c8743c", "w": 1.8, "op": .7, "style": "inferred", "in": 1.0},
                        {"k": "line", "p": [v.p(-5.0, 50.3), v.p(3, 52.5), v.p(11.521, 51.284)], "c": AU, "w": 1.8, "op": .7, "style": "inferred", "curve": True, "in": 1.2},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    hz = [{"k": "line", "p": [[120, 1000], [880, 1000]], "c": "#8c7152", "w": 3, "in": .1},
          {"k": "line", "p": arc(500, 1000, 300, 0, 180, 40), "c": "#6a645c", "w": 1.4, "op": .6, "style": "inferred", "in": .2},
          {"k": "line", "p": [[500, 1000], [500 + 330 * math.cos(math.radians(49)), 1000 - 330 * math.sin(math.radians(49))]], "c": GOLD, "w": 2.4, "in": .6},
          {"k": "line", "p": [[500, 1000], [500 + 330 * math.cos(math.radians(131)), 1000 - 330 * math.sin(math.radians(131))]], "c": GOLD, "w": 2.4, "in": .8},
          {"k": "line", "p": arc(500, 1000, 200, 49, 131, 20), "c": AU, "w": 10, "curve": True, "in": 1.1},
          {"k": "circle", "x": 500 + 330 * math.cos(math.radians(49)), "y": 1000 - 330 * math.sin(math.radians(49)), "r": 22, "fill": AU, "c": "none", "w": 0, "in": .7},
          {"k": "circle", "x": 500 + 330 * math.cos(math.radians(131)), "y": 1000 - 330 * math.sin(math.radians(131)), "r": 22, "fill": AU, "c": "none", "w": 0, "in": .9},
          {"k": "label", "x": 760, "y": 700, "t": "summer solstice", "st": "small", "in": 1.0}, {"k": "label", "x": 240, "y": 700, "t": "winter solstice", "st": "small", "in": 1.0},
          {"k": "cap", "x": 500, "y": 540, "t": "sunrise swings about 82° between solstices", "in": .2},
          {"k": "label", "x": 500, "y": 1080, "t": "each gold arc on the disc spans about 82°", "c": AMBER, "in": 1.5}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": hz}
    s3 = stat("c. 1600", "BCE", "radiocarbon on birch bark from a sword buried with the disc", "Pernicka et al. 2020")
    s4 = stat("700,000", "Deutschmarks", "asked for the disc in a Basel hotel in 2002; the buyers were police", "Meller & Michel 2018")
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the doubt, 2020", "#ffb09a", ["nobody recorded it in the ground", "its date is borrowed from the hoard", "an Iron Age style?"]) +
          [{"k": "label", "x": 500, "y": 880, "t": "the reply: the soil, the metals and the corrosion all tie it to the hoard", "c": "#8fd9b0", "in": 1.6}]}
    s6 = like(s0, cam=[1.12, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE NEBRA SKY DISC][sfx:boom][act:setting the scene, hushed]^Looters with a metal detector dug it up at ^night in {1999|nineteen ninety-nine}.",
                      "[d:tension][cam:1.12|0|0][act:the reveal, wonder, slowly]They'd found the ^oldest known picture of the sky."], cut=False),
        B("world", 0, ["[d:calm][k:THE DISC][act:plain description, unhurried]Bronze, ^thirty-two centimetres across. [act:pointing them out, one by one]In ^gold: a sun or full Moon, a crescent, thirty-two stars, and a little cluster of ^seven.",
                       "[d:aside][act:a light aside, warm]Very likely the ^Pleiades."]),
        B("collision", 4, ["[d:build][k:THE STING][act:storytelling, a caper building]In {2002|two thousand two}, a dealer offered it in a Basel hotel for seven hundred ^thousand Deutschmarks. [sfx:hit][act:the punchline, deadpan]The buyers were ^police."]),
        B("cost", 3, ["[d:build][k:THE DATE][act:matter of fact, careful]It had been buried with ^swords and ^axes@axe. [act:the clincher, precise]Birch bark on a sword dates to about {1600|^sixteen hundred} BCE.",
                      "[d:build][go:1|0][act:tracing it, curious][tune:level]Its ^copper comes from the Austrian ^Alps. [act:the surprise, lightly]Its ^gold, from ^Cornwall."]),
        B("reversal", 5, ["[d:reveal][k:THE DOUBT][act:the doubt creeps in, measured]In {2020|twenty twenty}, two archaeologists argued it might be a thousand years ^younger: nobody had ^recorded it in the ground.",
                          "[d:build][go:2|0][sfx:shimmer][act:the counter, steady and sure][tune:fall]But the ^soil, the ^metals and the ^corrosion tie it to the hoard. [act:wonder, slowing down]And its gold arcs span the ^swing of sunrise between the solstices, at ^this latitude."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A ^Bronze Age disc, buried around {1600|^sixteen hundred} BCE? [act:the verdict, level-headed][tune:fall]*Strong ^evidence*. [act:turning, lighter, curious][tune:rise]A calendar rule for ^leap months? [act:honest, a small shrug][tune:fallrise]Still ^argued.",
                     "[d:tension][p:0.93][act:the last word, quiet wonder]Three and a half thousand years ago, someone looked ^up, and wrote it down in ^gold."]),
    ]
    return EP("nebra-disc", "08.01", "The Nebra Sky Disc: A Bronze Age Map of Heaven?", "nebra-disc", "strong", "Is the Nebra sky disc really 3,600 years old, and what did it know?", "The oldest known picture of the *sky*.", beats, shots,
              "Meller 2004 · Pernicka et al. 2020 · Ehser et al. 2011 · Meller & Michel 2018 · Gebhard & Krause 2020",
              "Dug up by looters, recovered in a police sting: the Nebra sky disc's gold stars, its Alpine copper and Cornish gold, and the debate over its date.",
              ["#NebraSkyDisc", "#BronzeAge", "#Astronomy", "#Archaeology", "#SkyWatchers"])


# ---------------------------------------------------------------- 08.02 The Great Year
def great_year():
    t = math.radians(23.4)
    earth = sphere(0, 0, 8, "#3f6e8a", n=12, y=4) + \
            [{"t": "line", "p": [[-14 * math.sin(t), 12 - 14 * math.cos(t), 0], [14 * math.sin(t), 12 + 14 * math.cos(t), 0]], "c": "#e9dccb", "w": 3},
             {"t": "line", "p": [[14 * math.sin(t) * math.cos(2 * math.pi * k / 40), 12 + 14 * math.cos(t), 14 * math.sin(t) * math.sin(2 * math.pi * k / 40)] for k in range(41)], "c": GOLD, "w": 2.4, "style": "inferred"},
             L_(0, 26, "the axis traces a circle", GOLD, z=0, dy=-24), L_(0, 0, "Earth, tilted 23.4° · schematic", "#cfe6ff", z=10, dy=40)]
    s0 = iso(earth, cam=[1, 500, 900], s=18, x=500, y=1060, az=-20, spin=1.4, el=.35, table=None, stars=200)
    s1 = stat("25,772", "years", "for Earth's axis to trace one full circle; the stars drift about 1° every 71.6 years", "modern astronomical value")
    v = View(18, 47, 27, 42, (40, 330, 920, 900))
    s2 = mapshot(v, pins=[("Rhodes · Hipparchus", 28.2176, 36.4349, {"c": GOLD}), ("Alexandria · Ptolemy", 29.91, 31.2, {"a": "end", "lx": -18}), ("Babylon · centuries of star diaries", 44.42, 32.54, {"a": "end", "lx": -18})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}])
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "label", "x": 500, "y": 560, "t": "432,000", "st": "big", "c": GOLD, "in": .2}] +
          grp("one number, three traditions", AMBER, ["years of the Kali Yuga · India", "years of kings before the flood · Berossus", "warriors of Valhalla · 540 doors × 800"], y=700, size=30)}
    tl, ax = timeline(-800, 0, [(-800, "800 BCE"), (-600, "600"), (-400, "400"), (-200, "200"), (0, "1 CE")], "Written records")
    tl["els"] += event(ax, -700, "Hesiod's ages of man", row=1, c=BONE, i=.3) + event(ax, -130, "Hipparchus measures the drift", row=2, c=GOLD, i=.7) + \
                 [{"k": "label", "x": 120, "y": 480, "t": "← myths encoding it before 9600 BCE? no text says so", "st": "small", "c": "#ffb09a", "a": "start", "in": 1.1}]
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what would settle it", "#8fd9b0", ["a text before Hipparchus describing the drift", "a dated monument that requires it", "a sign of it in Babylon's star records"])}
    s6 = like(s0, cam=[1.15, 500, 980])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE GREAT YEAR][sfx:boom][act:hushed wonder, opening wide]The ^whole sky slowly ^turns. [act:savouring the number]One full ^circle every twenty-five thousand seven hundred and ^seventy-two years.",
                      "[d:tension][cam:1.12|0|0][act:the hook, leaning in][tune:rise]Did ancient people ^notice, and ^hide it in their myths?"], cut=False),
        B("world", 1, ["[d:calm][k:THE WOBBLE][act:explaining, patient and clear]Earth's axis ^wobbles like a slowing top, so the stars drift about one degree every ^seventy-two years.",
                       "[d:aside][act:a light aside, gently amused]In one ^lifetime, about one ^finger-width at arm's length."]),
        B("collision", 3, ["[d:build][k:THE CASE][act:laying out the case, warm]Myths everywhere speak of ages, from ^gold to ^iron. [act:intrigued, slowing on the number]And one ^number@count keeps turning up: four hundred and ^thirty-two thousand.",
                           "[d:build][sfx:shimmer][act:counting them off][tune:level]India's Kali ^Yuga. [act:the next, same rhythm][tune:level]Babylon's kings before the ^flood. [act:the last, landing it][tune:fall]Valhalla's ^warriors."]),
        B("cost", 5, ["[d:build][k:THE ARGUMENT][act:storytelling, even-handed]In {1969|nineteen sixty-nine}, a book called Hamlet's Mill argued that a ^lost culture discovered the wobble and ^encoded it in myth.",
                      "[d:build][act:bringing it up to date, brisk]^Today the producer Tyler Engle tells history as ^cycles, turning through a Great Year."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:the turn, leaning in][tune:fall]But the first ^written measurement comes from ^Hipparchus, around {130|one thirty} BCE. [sfx:hit][act:pointed, slower]And ^Babylon, which logged the sky on clay for centuries, shows ^no sign of it.",
                          "[d:build][act:plain, a quiet explanation]The big numbers also fall straight out of ^base-sixty arithmetic."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Myths that encode the wobble, long ^before Hipparchus? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:warmer, turning to the people][tune:rise]People who watched the sky with ^enormous care? [act:warm, wholehearted][tune:highfall]^Absolutely.",
                     "[d:tension][p:0.93][act:quiet and sure]The sky ^really turns. [act:the open riddle, thoughtful][tune:fall]The question is ^who wrote it down ^first."]),
    ]
    return EP("great-year", "08.02", "The Great Year: Did Myths Remember the Turning Sky?", "great-year", "unsupported", "Do ancient myths encode knowledge of precession far older than Hipparchus?", "The whole sky slowly *turns*.", beats, shots,
              "Ptolemy, Almagest VII.2 · Hays, Imbrie & Shackleton 1976 · de Santillana & von Dechend 1969 · Neugebauer 1950 · Sweatman 2019",
              "Earth's axis traces a circle every 25,772 years. Did ancient myths of golden and iron ages encode it before Hipparchus measured it? The number 432,000, and what Babylon's records show.",
              ["#Precession", "#GreatYear", "#Astronomy", "#Mythology", "#SkyWatchers"])


# ---------------------------------------------------------------- 08.03 Serpent Mound
def serpent():
    pts = []
    for k in range(80):
        s = k / 79
        x = -40 + 80 * s
        z = 10 * math.sin(s * 3.3 * math.pi) * (1 - .25 * s)
        pts.append([round(x, 2), .6, round(z, 2)])
    tail = [[-40 + 5 * math.cos(a), .6, 5 * math.sin(a) - 5] for a in [k * .35 for k in range(18)]]
    body = tail[::-1] + pts
    snake = [{"t": "slab", "x0": -50, "x1": 52, "z0": -24, "z1": 24, "y": 0, "c": "#6f8a4a"},
             {"t": "line", "p": body, "c": "#4f6a3a", "w": 22, "op": .9}, {"t": "line", "p": body, "c": "#a8c07a", "w": 14},
             {"t": "line", "p": [[40 + 4 * math.cos(a), .7, 3 * math.sin(a) + pts[-1][2]] for a in [k * .3 for k in range(22)]], "c": "#a8c07a", "w": 8},
             {"t": "line", "p": [pts[-1], [60, .7, pts[-1][2] - 12]], "c": GOLD, "w": 3, "style": "inferred"},
             L_(0, 1, "about 411 m along its body · schematic", GOLD, z=-20, dy=-20), L_(56, 1, "summer solstice sunset", AMBER, z=pts[-1][2] - 10, dy=-16)]
    s0 = iso(snake, cam=[1, 500, 900], s=8.4, x=500, y=1000, az=-16, spin=1.0, el=.55, table=None)
    v = View(-89, -78, 35.5, 43.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Serpent Mound", -83.4304, 39.0254, {"c": GOLD}), ("Cincinnati", -84.51, 39.1, {"a": "end", "lx": -18}), ("Columbus", -83.0, 39.96, {})],
                 extra=[{"k": "label", "x": v.p(-83, 40.6)[0], "y": v.p(-83, 40.6)[1], "t": "Ohio", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = like(s0, cam=[1.35, 700, 900], add=[{"k": "label", "x": 500, "y": 520, "t": "the head points to where the sun sets on the longest day", "c": AMBER, "in": .3}])
    s3 = stat("411", "metres", "the serpent's length along its body; about 6–7 m wide and up to about a metre high", "Ohio History Connection")
    tl, ax = timeline(-1000, 1400, [(-1000, "1000 BCE"), (-500, "500"), (1, "1 CE"), (500, "500"), (1000, "1000")], "Two camps, one serpent")
    tl["els"] += event(ax, -300, "built by the Adena?", row=1, c=GOLD, i=.3, sub="one camp") + event(ax, 1070, "built by Fort Ancient?", row=2, c=SCAN, i=.6, sub="the other camp") + \
                 [{"k": "label", "x": 120, "y": 480, "t": "← laid out in the Ice Age, 13,000 years ago? nothing dated there", "st": "small", "c": "#ffb09a", "a": "start", "in": 1.0}]
    s4 = tl
    s5 = stat("<1°", "shift", "in the solstice sunset point between 1,000 and 13,000 years ago: too small to date an earthen head", "this case's calculation")
    s6 = like(s0, cam=[1.12, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:SERPENT MOUND · OHIO][sfx:boom][act:setting the scene, a sense of scale]A giant earthen ^snake, four hundred metres long, ^uncoils along a ridge in Ohio.",
                      "[d:tension][cam:1.12|0|0][act:the hook, wonder in the voice]And its head ^swallows the summer ^solstice sunset."], cut=False),
        B("world", 3, ["[d:calm][k:THE SERPENT][act:describing it, unhurried]A coiled ^tail, open ^jaws, an ^oval in its mouth. [go:2|0][act:showing you, gently]Sight along the ^head, and it points to where the sun sets on the ^longest day."]),
        B("collision", 4, ["[d:build][k:THE CASE][act:presenting the claim, fair and even]Graham Hancock suggests the layout could be far older than its builders: about ^thirteen thousand years, judged from the slow change in Earth's ^tilt.",
                           "[d:build][act:lighter, a curious aside]And some see the constellation ^Draco in its coils."]),
        B("cost", 4, ["[d:build][k:THE DATES][act:laying out the evidence, precise]Radiocarbon from inside and beneath the mound splits archaeologists into two camps: about {300|^three hundred} BCE, or about {1070|^ten seventy} CE.",
                      "[d:build][sfx:shimmer][act:the point, quietly firm]^Both inside the last ^three thousand years."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][sfx:hit][act:turning to it, one eyebrow up][tune:rise]And the ^tilt argument? [act:plain fact, measured]Over thirteen thousand years, the solstice sunset moves by ^less than a degree. [act:the sting, dry and gentle]Smaller than the ^error in sighting along a ^rebuilt earthen head.",
                          "[d:aside][act:a light aside, matter of fact]And Draco is a ^Mediterranean constellation."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]An ^Ice Age serpent? [act:the verdict, firm and kind][tune:fall]*Ruled ^out*. [act:brighter, genuinely curious][tune:fall]^Adena or Fort ^Ancient builders? [act:warm, inviting]That's the ^real open question.",
                     "[d:tension][p:0.93][act:the last word, warm and proud]Either way, it's ^Native American ^genius, aimed at the sun."]),
    ]
    return EP("serpent-mound", "08.03", "Serpent Mound: How Old Is the Great Snake?", "serpent-mound", "debunked", "Was Serpent Mound first laid out in the Ice Age, as its sunset alignment is said to show?", "Its head swallows the *sunset*.", beats, shots,
              "Squier & Davis 1848 · Putnam 1890 · Fletcher et al. 1996 · Herrmann et al. 2014 · Lepper et al. 2018 · Hardman & Hardman 1987",
              "A 411-metre earthen serpent in Ohio swallows the summer solstice sunset. Was it laid out in the Ice Age? The radiocarbon, the tilt argument, and the real open question.",
              ["#SerpentMound", "#Ohio", "#NativeAmerican", "#Solstice", "#SkyWatchers"])


# ---------------------------------------------------------------- 08.04 The Edfu texts
def edfu():
    pylon = [{"k": "poly", "p": [[150, 1200], [200, 600], [460, 600], [440, 1200]], "fill": "#d8c7a2", "c": "#fff3dc", "w": 1.6, "in": .1},
             {"k": "poly", "p": [[560, 1200], [540, 600], [800, 600], [850, 1200]], "fill": "#d8c7a2", "c": "#fff3dc", "w": 1.6, "in": .1},
             {"k": "rect", "x": 440, "y": 820, "w": 120, "h": 380, "fill": "#1a1511", "c": "#8c7452", "sw": 1.4, "in": .2}] + \
            [{"k": "line", "p": [[200 + 12 * i * .12, 660 + i * 34], [440 - 12 * i * .12, 660 + i * 34]], "c": "#8c7452", "w": 2, "op": .6, "in": .3 + i * .03} for i in range(16)] + \
            [{"k": "line", "p": [[550 + 12 * i * .12, 660 + i * 34], [790 - 12 * i * .12, 660 + i * 34]], "c": "#8c7452", "w": 2, "op": .6, "in": .3 + i * .03} for i in range(16)] + \
            [{"k": "cap", "x": 500, "y": 520, "t": "the Temple of Horus, Edfu · 237–57 BCE", "in": .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": pylon}
    v = View(27, 37, 22, 32, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Edfu", 32.8734, 24.9779, {"c": GOLD}), ("Luxor", 32.64, 25.69, {"a": "end", "lx": -18}), ("Cairo", 31.24, 30.04, {})],
                 extra=[{"k": "label", "x": v.p(30, 27)[0], "y": v.p(30, 27)[1], "t": "Egypt", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    isl = [{"k": "water", "y": 960, "h": 400, "x0": -100, "x1": 1100, "op": .7, "in": .1},
           {"k": "poly", "p": [[300, 980], [380, 920], [500, 900], [620, 920], [700, 980]], "fill": "#d8c7a2", "c": "#fff3dc", "w": 1.6, "curve": True, "in": .4}] + \
          [{"k": "line", "p": [[400 + k * 40, 930], [395 + k * 40 + (k % 3) * 6, 780 - (k % 2) * 30]], "c": "#8fb57a", "w": 3, "in": .7 + k * .05} for k in range(6)] + \
          [{"k": "poly", "p": [[500, 760], [540, 740], [575, 750], [545, 770], [520, 800], [500, 790]], "fill": "#6b4a2e", "c": "#e9dccb", "w": 1.4, "in": 1.3},
           {"k": "cap", "x": 500, "y": 560, "t": "an island of reeds rises · a falcon alights", "in": .2},
           {"k": "label", "x": 500, "y": 1160, "t": "the Edfu creation story · schematic", "st": "small", "c": AMBER, "in": 1.6}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": isl}
    tl, ax = timeline(-2600, 0, [(-2500, "2500 BCE"), (-2000, "2000"), (-1500, "1500"), (-1000, "1000"), (-500, "500")], "Which came first")
    tl["els"] += event(ax, -2400, "the Pyramid Texts", row=1, c=BONE, i=.3, sub="the first mound in the waters") + event(ax, -360, "Plato writes Atlantis", row=0, c=AMBER, i=.6) + \
                 [{"k": "band", "x0": ax.x(-237), "x1": ax.x(-57), "y": 700, "h": 16, "c": GOLD, "t": "Edfu carved", "in": .9}]
    s3 = tl
    s4 = quote("The first records of Atlantis that we have.", "Tyler Engle, reportedly · JRE #2558, 2026", y=720, size=48)
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what the texts describe", AMBER, ["creation from a mound in the waters", "Edfu's gods, and its own temple", "a world destroyed and made again, in mythic time"])}
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE EDFU TEXTS][sfx:boom][act:storyteller, low and inviting]On the walls of an Egyptian ^temple, priests carved the story of an island in the first waters, its builder gods, and its ^destruction.",
                      "[d:tension][cam:1.12|0|0][act:the hook, a raised eyebrow]Some say it's the ^oldest record@noun of ^Atlantis."], cut=False),
        B("world", 1, ["[d:calm][k:THE TEMPLE][act:plain, setting the facts down]The Temple of Horus at Edfu, begun in {237|^two thirty-seven} BCE and finished in {57|^fifty-seven} BCE. [go:0|0][act:quiet admiration]Its walls hold one of the ^largest bodies of hieroglyphic text ^anywhere."]),
        B("collision", 2, ["[d:build][k:THE STORY][act:telling the myth, slow and rhythmic]An ^island rises from the waters, covered in ^reeds. [act:same spell, unhurried]Creator beings ^gather. [act:a small image, gently]A ^falcon god ^lands on a reed.",
                           "[d:build][sfx:shimmer][act:darker, then hope returns]^Enemies attack, the first gods ^die, and the world is made ^again."]),
        B("cost", 4, ["[d:build][k:THE CASE][act:reporting the claim, even-handed]On a huge podcast this month, a researcher reportedly called these texts the first records@noun of ^Atlantis, older than ^Plato.",
                      "[d:build][act:fair, giving it its due]Graham Hancock reads a sacred island destroyed by ^flood, whose sages sailed away to ^rebuild the world."]),
        B("reversal", 3, ["[d:reveal][k:THE TWIST][sfx:hit][act:the turn, clear and deliberate][tune:fall]But the stone was carved more than a century ^after Plato wrote. [act:building, a little wonder]And the island rising from the waters is Egypt's ^oldest creation image, already in the Pyramid Texts, two ^thousand years earlier.",
                          "[d:aside][act:gentle, an image to picture]In a land where the fields ^rose from the water every year, as the Nile flood ^fell."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A memory of a ^lost civilisation? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:precise, unhurried]^Nothing in the texts points ^outside Egypt. [act:warmer, generous][tune:rise]Ideas ^older than the stone? [act:easy, confident]Very ^likely.",
                     "[d:tension][p:0.93][act:the last word, gentle and clear]A ^creation story is not a ^travel report. [act:warm, a small smile]It can ^still be one of the ^oldest on any wall."]),
    ]
    return EP("edfu-texts", "08.04", "The Edfu Texts: A Lost Homeland on a Temple Wall?", "edfu-texts", "unsupported", "Do the Edfu texts remember a real civilisation older than Egypt?", "The oldest record of *Atlantis*?", beats, shots,
              "Reymond 1969 · Kurth 2004 · McClain 2011 · Collins 1998 · Hancock 2015 · The Joe Rogan Experience #2558, 2026",
              "Ptolemaic priests carved the story of a primeval island, its builder gods and its ruin on the Temple of Horus at Edfu. Is it the oldest record of Atlantis, or Egypt's own creation myth?",
              ["#Edfu", "#AncientEgypt", "#Atlantis", "#Mythology", "#SkyWatchers"])


# ---------------------------------------------------------------- 08.05 Thunder beings: the plasma petroglyphs
def plasma():
    C = "#f2dcb4"
    rock = [{"k": "poly", "p": [[140, 1180], [120, 760], [260, 600], [700, 580], [880, 720], [870, 1200]], "fill": "#6b3a2a", "c": "#b8765a", "w": 2, "curve": True, "in": .1},
            {"k": "circle", "x": 420, "y": 740, "r": 30, "fill": "none", "c": C, "w": 5, "in": .4},
            {"k": "line", "p": [[420, 770], [420, 960]], "c": C, "w": 5, "in": .5},
            {"k": "line", "p": [[340, 800], [360, 860], [480, 860], [500, 800]], "c": C, "w": 5, "in": .6},
            {"k": "line", "p": [[350, 1040], [370, 960], [470, 960], [490, 1040]], "c": C, "w": 5, "in": .7}] + \
           [{"k": "circle", "x": s[0], "y": s[1], "r": 9, "fill": C, "c": "none", "w": 0, "in": .8 + i * .05} for i, s in enumerate(((330, 790), (510, 790), (340, 1060), (500, 1060), (310, 880), (530, 880)))] + \
           [{"k": "line", "p": [[640, 700], [640, 1080]], "c": C, "w": 4, "in": 1.0}, {"k": "line", "p": [[720, 700], [720, 1080]], "c": C, "w": 4, "in": 1.0}] + \
           [{"k": "line", "p": [[640, 720 + k * 45], [720, 720 + k * 45]], "c": C, "w": 4, "in": 1.1 + k * .05} for k in range(9)] + \
           [{"k": "cap", "x": 500, "y": 520, "t": "a 'squatter man' and a ladder · schematic", "in": .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": rock}
    col = [{"k": "glow", "x": 500, "y": 860, "r": 380, "kind": "lamp", "op": .5, "in": .1}] + \
          [{"k": "circle", "x": 500, "y": 560 + k * 75, "r": 70 + 30 * math.sin(k * 1.3), "fill": "none", "c": "#cfe6ff", "w": 3, "op": .85, "in": .3 + k * .1} for k in range(9)] + \
          [{"k": "line", "p": [[500, 520], [500, 1220]], "c": "#ffffff", "w": 6, "op": .7, "in": .2},
           {"k": "cap", "x": 500, "y": 440, "t": "a Z-pinch: plasma squeezed into rings", "in": .2},
           {"k": "label", "x": 500, "y": 1300, "t": "laboratory physics · schematic", "st": "small", "c": AMBER, "in": 1.2}]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": col}
    s2 = stat("24,000", "carvings", "at Petroglyph National Monument, New Mexico; most were made between 1300 and the 1680s CE", "National Park Service")
    s3 = stat("9", "extreme solar storms", "recorded in tree rings over the last 15,000 years, including 774 and 993 CE", "Bard et al. 2023; Miyake et al. 2012")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the test nobody has run", "#9fd0ff", ["direct dates for the motifs", "do they cluster in a few short windows?", "a control set of sites"])}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("two claims, two weights", AMBER, ["an extreme aurora, carved on rocks", "plasma used as a technology"], y=560) +
          [{"k": "label", "x": 500, "y": 900, "t": "the first: possible, untested · the second: no evidence", "c": "#ffb09a", "in": 1.4}]}
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THUNDER BEINGS][sfx:boom][act:conjuring images, curious][tune:level]Stick figures with ^ladders for bodies. [act:the next image, same rhythm][tune:level]Stacks of ^rings. [act:widening out, wonder]Carved on rocks all over the ^world.",
                      "[d:tension][cam:1.1|0|0][act:the hook, intrigued]A Los Alamos ^physicist saw his ^lab experiments in them."], cut=False),
        B("world", 1, ["[d:calm][k:THE PHYSICIST][act:explaining, clear and respectful]In {2003|two thousand three}, plasma physicist Anthony Peratt published a paper: the shapes ^match what happens when a huge current squeezes plasma into rings and ^twists.",
                       "[d:build][act:painting it, building wonder]His idea: an aurora far ^stronger than any today, glowing over the whole sky, drawn by people ^everywhere."]),
        B("collision", 3, ["[d:build][k:THE SUN CAN DO IT][sfx:shimmer][act:genuinely impressed, warm]And the Sun really ^can surprise us. [act:the evidence, precise]Tree rings record@verb ^nine extreme solar storms in the last ^fifteen thousand years."]),
        B("cost", 2, ["[d:build][k:THE PROBLEM][act:the problem, fair and plain][tune:fall]But stick figures, circles and ladders are the ^simplest shapes ^anyone can carve. [act:matter of fact, lighter]Some resemblance is ^expected by ^chance.",
                      "[d:build][act:steady, building the case]And the carvings spread across ^thousands of years. [act:the detail that matters, precise]At one famous site, ^most were made after {1300|^thirteen hundred} CE."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][sfx:hit][act:leaning in, this matters]The theory makes a ^testable prediction: the motifs should cluster in a few ^short windows. [gap:0.45][act:the sting, quiet][tune:fall]^Nobody has tested it with ^direct dates.",
                          "[d:aside][go:5|0][act:an aside, dry and plain]And the ^newer claim, that ancient builders used@verb plasma as a technology, has no evidence at ^all."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Rock art recording a ^plasma sky? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:fair-minded, a touch rueful]The idea has been ^ignored more than ^tested.",
                     "[d:tension][p:0.93][act:sincere, principled]A bold theory deserves a ^fair test. [act:the last word, quiet][tune:fall]This one is ^still waiting for it."]),
    ]
    return EP("plasma-petroglyphs", "08.05", "Thunder Beings: Did Rock Art Record a Plasma Sky?", "plasma-petroglyphs", "unsupported", "Do prehistoric petroglyphs record a real, extreme plasma display in the sky?", "He saw his lab experiments in *rock art*.", beats, shots,
              "Peratt 2003, IEEE Transactions on Plasma Science · Peratt et al. 2007 · Miyake et al. 2012, Nature · Bard et al. 2023 · National Park Service",
              "A Los Alamos plasma physicist saw his laboratory instabilities carved on rocks worldwide. Did our ancestors watch the sky catch fire? The physics, the dates, and the test nobody has run.",
              ["#Petroglyphs", "#Plasma", "#Aurora", "#RockArt", "#SkyWatchers"])


# ---------------------------------------------------------------- 08.06 The ledger
def _ledger_text():
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "circle", "x": 500, "y": 860, "r": 260, "fill": PATINA, "c": "#8fb5a0", "w": 3, "in": .1}] +
          [{"k": "circle", "x": 500 + 200 * math.cos(k * 2.4), "y": 860 + 200 * math.sin(k * 2.4) * .9, "r": 8, "fill": AU, "c": "none", "w": 0, "in": .2 + k * .04} for k in range(24)] +
          [{"k": "cap", "x": 500, "y": 520, "t": "what the ancients saw overhead", "in": .2}]}
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Strong evidence", "#7fd1d4", ["the Nebra disc: Bronze Age, c. 1600 BCE"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["myths encoding the Great Year", "a lost homeland in the Edfu texts", "a plasma sky carved on rocks"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["an Ice Age Serpent Mound"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Still open", "#e8b87a", ["Adena or Fort Ancient?", "a leap-month rule on the disc?"])}
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:SKY WATCHERS][sfx:boom][act:recalling them fondly]A disc of gold ^stars, a turning ^sky, a snake that eats the ^sunset. [act:brisk, inviting]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:STRONG EVIDENCE][act:confident, plain]The Nebra sky disc: a ^real Bronze Age view of the heavens, buried about ^thirty-six hundred years ago."]),
        B("collision", 2, ["[d:build][k:AWAITING EVIDENCE][act:running through them][tune:level]Myths that encode the Great ^Year. [act:the second, same pace][tune:level]A lost ^homeland in the Edfu texts. [act:the last of them][tune:fall]A ^plasma sky carved on rocks. [d:aside][act:lighter, fair]Bold ideas, still ^untested."]),
        B("cost", 3, ["[d:reveal][k:RULED OUT][sfx:hit][act:flat, final][tune:highfall]An ^Ice Age Serpent Mound."]),
        B("reversal", 4, ["[d:build][k:STILL OPEN][act:open, curious][tune:fall]Who built the serpent, ^Adena or Fort ^Ancient. [act:the second open door]And whether the disc carries a ^calendar rule."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:the moral, warm and unhurried]People have watched the sky with ^care for as long as there have ^been people. [go:5|1.5][act:gentle, firm]Giving them ^credit doesn't ^need a lost civilisation.",
                     "[d:tension][p:0.93][act:the house motto, quiet and sure]Coherence is the ^measure. [gap:0.4][act:closing, calm and final]Not final ^demonstration."]),
    ]
    return EP("sky-ledger", "08.06", "Sky Watchers · The Ledger", "", "mixed", "What the ancients saw overhead, weighed.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 08",
              "The verdicts of Sky Watchers in one ledger: the disc with strong evidence, the ideas awaiting evidence, the one ruled out and the questions still open.",
              ["#History", "#Astronomy", "#Archaeology", "#SkyWatchers", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: five skies in a cabinet, and a sixth niche for the people who watched them (see cabinet.py)."""
    import random as _r
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    rnd = _r.Random(8)
    stars = [[rnd.uniform(-185, 185), rnd.uniform(-350, -70), rnd.uniform(1.2, 2.6)] for _ in range(26)]
    watch = [{"k": "rect", "x": -200, "y": -372, "w": 400, "h": 336, "r": 8, "fill": "#161a2c", "c": "#3a3550", "sw": 1.5}] + \
            [{"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r, 1), "fill": "#f5ecdc", "c": "none", "w": 0} for x, y, r in stars] + \
            [{"k": "circle", "x": 130, "y": -300, "r": 18, "fill": "#efe8da", "c": "none", "w": 0}, {"k": "circle", "x": 139, "y": -305, "r": 16, "fill": "#161a2c", "c": "none", "w": 0},
             {"k": "rect", "x": -200, "y": -40, "w": 400, "h": 40, "r": 2, "fill": "#2a1f15", "c": "none", "sw": 0}] + \
            [{"k": "person", "x": x, "y": -4, "h": 48, "t": False, "color": "#e8d6b8"} for x in (-70, -20, 40)]
    C = Cabinet([
        {"name": "The Nebra disc", "model": mdl(nebra(), 0)},
        {"name": "The Great Year", "model": mdl(great_year())},
        {"name": "Serpent Mound", "model": mdl(serpent())},
        {"name": "The Edfu texts", "model": mdl(edfu(), 0)},
        {"name": "A plasma sky?", "model": mdl(plasma(), 0)},
        {"name": "The sky watchers", "model": watch},
    ])
    C.build()
    NE, GY, SM, ED, PL, SW = range(6)
    twinkle = C.local(SW, [{"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r * 2.4, 1), "fill": "rgba(255,226,168,.35)", "c": "none", "w": 0, "in": .3 + .05 * k, "fx": "pop"}
                           for k, (x, y, r) in enumerate(stars[:14])])
    s1 = C.step(C.cam_cell(NE), C.verdict(NE, "strong", "about 3,600 years old", .4) + C.note(NE, "a real Bronze Age view of the heavens", at=1.2))
    s2 = C.step(C.cam_cell(GY), C.verdict(GY, "awaiting", "myths that encode it?", .2))
    s3 = C.step(C.cam_cell(ED), C.verdict(ED, "awaiting", "a lost homeland?", .2))
    s4 = C.step(C.cam_cell(PL), C.verdict(PL, "awaiting", "a plasma sky?", .2))
    s5 = C.step(C.cam_all(), [e for k, i in enumerate((GY, ED, PL)) for e in C.wash(i, VCOL["awaiting"], at=.1 + .15 * k, op=.13)])
    s6 = C.step(C.cam_cell(SM), C.verdict(SM, "ruled", at=.1) + C.struck(SM, "an Ice Age mound", at=.2, rows=2))
    s7 = C.step(C.cam_cell(SM), C.verdict(SM, "open", "Adena, or Fort Ancient?", .1, frame=False) + C.question(SM, dx=C.w * .34, dy=-200, at=.4, size=70))
    s8 = C.step(C.cam_cell(NE), C.verdict(NE, "open", "a calendar rule?", .1, frame=False) + C.question(NE, dx=C.w * .34, dy=-200, at=.4, size=70))
    s9 = C.step(C.cam_cell(SW), C.verdict(SW, "established", "watched with care", .3) + twinkle)
    s10 = C.step(C.cam_all(), [e for i in range(6) for e in C.wash(i, "#f2b36b", at=.2 + .1 * i, op=.11)])
    s11 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {}),
        2: (s2, {(0, 1): "%d|1.1" % s3, (0, 2): "%d|1.1" % s4, (0, 3): "%d|1.2" % s5}),
        3: (s6, {}),
        4: (s7, {(0, 1): "%d|1.1" % s8}),
        5: (s9, {(0, 1): "%d|1.2" % s10, (1, 0): "%d|3" % s11}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def nebra_m():
    """The Nebra disc as one continuous take (see mural.py): the sting, the hoard and the doubt are drawn, not written."""
    import copy
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN
    ep = nebra()
    short = lambda e: e.get("k") == "label" and len(e.get("t", "")) <= 24
    # the disc, read aloud: 32 cm, the sun or full Moon, the crescent, the stars, the seven
    look = [line([[200, 1200], [800, 1200]], .8, BN, 2, dur=.8), line([[200, 1185], [200, 1215]], .8, BN, 2, draw=False), line([[800, 1185], [800, 1215]], .8, BN, 2, draw=False),
            label(500, 1250, "32 cm", 1.2, BN, 32),
            ring(380, 750, 88, 3.3, AU, 3), ring(640, 770, 88, 4.4, AU, 3)] + \
           [glow(500 + x, 860 + y, 26, 5.3 + .02 * k, .8) for k, (x, y) in enumerate([(-200, 40), (-150, 150), (-60, 210), (40, 160), (150, 120), (200, 30), (-100, -200), (60, -220)])] + \
           [ring(548, 786, 62, 6.8, BLUE, 3)]
    # the sting: a hotel table, the disc, a dealer, two buyers; the buyers were police
    sting = {"base": "dark", "floor": 1180, "cam": [1.3, 500, 1010], "els": [
                bx(250, 1040, 500, 22, "#5a4330", r=4, at=.2), line([[300, 1062], [300, 1180]], .2, "#5a4330", 8, draw=False), line([[700, 1062], [700, 1180]], .2, "#5a4330", 8, draw=False),
                oval(500, 1025, 90, 26, PATINA, "#8fb5a0", 2, 1, .5), dot(470, 1020, 12, AU, .7), dot(530, 1018, 10, AU, .7),
                person(170, 1180, 230, .9), glow(170, 1000, 120, 1.0, .35)] +
             [bx(560 + 30 * k, 980 - 12 * k, 110, 26, "#8fae7a", "#5f7d4c", 1.5, 3, 2.6 + .25 * k, fx="pop") for k in range(3)] +
             [label(620, 900, "700,000 DM", 3.4, AMB, 38), person(760, 1180, 230, 4.0), person(860, 1180, 215, 4.2),
              glow(810, 930, 160, 6.3, .8, "scan"), glow(810, 930, 110, 6.6, .7, "fire")]}
    # the hoard and its date: the disc buried with two swords and two axes; birch bark on a hilt
    sword = lambda x, y, a: [line([[x, y], [x + 260 * math.cos(a), y - 260 * math.sin(a)]], .9, "#c9a86a", 9, draw=False),
                             line([[x - 22 * math.sin(a), y - 22 * math.cos(a)], [x + 22 * math.sin(a), y + 22 * math.cos(a)]], .9, "#8a6a48", 7, draw=False)]
    hoard = {"base": "section", "ground": 620, "tod": "night", "layers": [{"d": 0, "c": "#5f4c39", "t": ""}, {"d": 400, "c": "#4a3a2c", "t": ""}], "cam": [1.3, 500, 1020], "els":
             [oval(500, 900, 110, 34, PATINA, "#8fb5a0", 2, 1, .3)] + sword(250, 1060, .18) + sword(300, 1110, .12) +
             [{"k": "poly", "p": [[640, 1030], [720, 1020], [735, 1060], [650, 1062]], "fill": "#c9a86a", "c": "none", "w": 0, "in": 1.3},
              {"k": "poly", "p": [[660, 1100], [740, 1092], [752, 1130], [668, 1134]], "fill": "#c9a86a", "c": "none", "w": 0, "in": 1.4},
              bx(248, 1050, 40, 20, "#efe6d2", r=3, at=3.4, fx="pop"), glow(268, 1060, 80, 3.4, .8),
              label(500, 1260, "c. 1600 BCE", 4.4, AU, 44, st="serif")]}
    # the doubt: a thousand years younger? nobody recorded it in the ground
    ax0, ax1 = 150, 850
    xt = lambda y: ax0 + (ax1 - ax0) * (y + 2000) / 2000
    doubt = {"base": "dark", "cam": [1.2, 500, 900], "els": [line([[ax0, 1150], [ax1, 1150]], .1, "#8c7152", 3),
             label(xt(-1600), 1210, "1600 BCE", .3, AU, 28), label(xt(-600), 1210, "600 BCE", .3, LILAC, 28),
             dot(xt(-1600), 1150, 10, AU, .4), oval(xt(-1600), 1060, 70, 70, PATINA, "#8fb5a0", 2, 1, .5),
             oval(xt(-600), 1060, 70, 70, "none", LILAC, 3, 1, 2.2, style="claimed"), arrow([[xt(-1600) + 80, 1000], [xt(-1100), 950], [xt(-600) - 80, 1000]], 2.0, LILAC, 3, "claimed", 1.0)] +
             question(xt(-600), 960, 2.6, 80) +
             [bx(360, 560, 280, 200, "none", LILAC, 3, 6, 4.4, style="claimed"), label(500, 680, "no record", 5.0, LILAC, 30)]}
    return remix(ep, scenes={3: hoard, 4: sting, 5: doubt}, alias={6: 0}, cams={6: [1.12, 500, 860]}, keep=short,
                 drop=("para", "num", "title", "q", "cap", "label"), beat_adds={1: (look, [1.1, 500, 900])})


def great_year_m():
    """The Great Year as one continuous take (see mural.py): the wobble, the number and the argument are drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, ellipse, scatter, AMBER as AMB, BLUE, LILAC, BONE as BN
    ep = great_year()
    short = lambda e: e.get("k") == "label" and len(e.get("t", "")) <= 30
    ax = [500 + 330 * math.sin(math.radians(23.4)), 1060 - 330 * math.cos(math.radians(23.4))]
    wobble = {"base": "dark", "stars": 120, "cam": [1.1, 500, 960], "els": [
                oval(500, 1060, 110, 110, "#2f5f7a", "#9fd0ff", 2, 1, .2), oval(470, 1030, 40, 26, "#5f8a5a", "none", 0, .9, .3),
                line([[500 - (ax[0] - 500) * .45, 1060 + (1060 - ax[1]) * .45], ax], .5, BN, 3),
                {"k": "line", "p": ellipse(500, ax[1], ax[0] - 500, 26, 48), "c": AU, "w": 3, "style": "inferred", "curve": True, "in": 1.2, "fx": "draw", "dur": 4.0},
                dot(ax[0], ax[1], 7, AU, 1.2), glow(500, ax[1], 120, 1.4, .4),
                person(170, 1300, 150, 6.4), line([[190, 1210], [300, 1150]], 6.8, "#e8d6b8", 6), line([[300, 1150], [312, 1140]], 7.2, AU, 8),
                dot(330, 1128, 6, BN, 7.4), dot(346, 1120, 6, BLUE, 8.2), arrow([[330, 1110], [346, 1102]], 8.0, BLUE, 2, dur=.6, curve=False)]}
    ages = [bx(380 + 15 * k, 500 + 62 * k, 240 - 30 * k, 40, c, r=8, at=.4 + .5 * k, fx="pop") for k, c in enumerate(("#e8c35a", "#cbd2d8", "#c8743c", "#6a645c"))]
    icons = [ring(210, 1170, 50, 9.0, AMB, 4), line([[160, 1170], [260, 1170]], 9.2, AMB, 3), line([[210, 1120], [210, 1220]], 9.2, AMB, 3),
             {"k": "poly", "p": [[440, 1220], [560, 1220], [540, 1180], [520, 1180], [505, 1140], [495, 1140], [480, 1180], [460, 1180]], "fill": "#c9a86a", "c": "none", "w": 0, "in": 10.6, "fx": "rise"},
             bx(700, 1150, 200, 80, "none", "#cbd2d8", 2.5, 6, 12.2)] + [bx(712 + 38 * k, 1162, 26, 58, "#6a645c", r=12, at=12.3 + .05 * k) for k in range(5)]
    links = [line([[500, 930], [210, 1110]], 9.1, AMB, 2, "inferred"), line([[500, 930], [500, 1130]], 10.7, AMB, 2, "inferred"), line([[500, 930], [800, 1140]], 12.3, AMB, 2, "inferred")]
    number = {"base": "dark", "cam": [1.05, 500, 920], "els": ages + [label(500, 900, "432,000", 6.6, AU, 110, st="big", fx="pop", dur=.8), glow(500, 860, 260, 6.6, .45)] + links + icons}
    mill = {"base": "dark", "cam": [1.1, 500, 940], "els": [
                bx(170, 800, 260, 340, "#3b2a1c", "#c9a86a", 3, 8, .4, fx="pop"), ring(300, 930, 70, .8, AU, 4)] +
            [line([[300, 930], [300 + 70 * math.cos(math.radians(a)), 930 + 70 * math.sin(math.radians(a))]], .9, AU, 3) for a in range(0, 360, 45)] +
            [label(300, 1080, "1969", 1.2, BN, 34, st="serif"),
             oval(760, 720, 120, 40, "none", LILAC, 3, 1, 2.8, style="claimed"), bx(690, 640, 140, 80, "none", LILAC, 3, 4, 3.0, style="claimed"),
             arrow([[700, 780], [560, 840], [440, 900]], 3.6, LILAC, 3, "claimed", 1.0),
             {"k": "line", "p": ellipse(640, 1200, 170, 90, 40, -80, 250), "c": AMB, "w": 4, "curve": True, "in": 9.0, "fx": "draw", "dur": 2.0},
             arrow([[640 + 170 * math.cos(math.radians(240)), 1200 + 90 * math.sin(math.radians(240))], [640 + 170 * math.cos(math.radians(270)), 1200 - 90]], 10.8, AMB, 4, dur=.4, curve=False)] +
            [dot(640 + 170 * math.cos(math.radians(a)), 1200 + 90 * math.sin(math.radians(a)), 11, c, 9.4 + .3 * k) for k, (a, c) in enumerate(((-30, "#e8c35a"), (60, "#cbd2d8"), (150, "#c8743c"), (210, "#6a645c")))]}
    return remix(ep, scenes={1: wobble, 3: number, 5: mill}, alias={2: 1, 6: 0}, cams={0: [1.25, 500, 980], 6: [1.3, 500, 1000]}, keep=short,
                 drop=("para", "num", "title", "q", "cap", "label"))


def plasma_m():
    """Thunder beings as one continuous take (see mural.py): the aurora, the tree rings, the chance shapes and the missing test are drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, scatter, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN
    ep = plasma()
    C = "#f2dcb4"
    curt = lambda x0, c, at: [line([[x0 + 30 * k, round(430 + 70 * math.sin(k * .8), 1)], [x0 + 30 * k + 12, round(880 + 30 * math.cos(k), 1)]], at + .05 * k, c, 6, dur=.8, op=.5) for k in range(10)]
    aurora = curt(50, "#7fe3a8", .3) + curt(650, "#e79ad0", .6) + [line([[40, 1380], [960, 1380]], .2, "#6a645c", 3, draw=False)] + \
             [person(150 + 110 * k, 1380, 70, 1.4 + .15 * k) for k in range(7)] + [glow(500, 700, 460, .2, .25)]
    # 3 · the Sun can surprise us: a tree's rings, nine storm years lit up
    rings = [ring(500, 960, 30 + 26 * k, .2 + .04 * k, "#8a6a48" if k % 2 else "#a8865e", 3, dur=.5) for k in range(11)]
    storms = [ring(500, 960, 30 + 26 * k, 3.6 + .35 * j, AU, 5, dur=.4) for j, k in enumerate((1, 2, 3, 4, 6, 7, 8, 9, 10))] + \
             [glow(500 + (30 + 26 * k) * math.cos(a), 960 + (30 + 26 * k) * math.sin(a), 40, 3.7 + .35 * j, .8) for j, (k, a) in enumerate(((1, 1), (2, 2.5), (3, 4), (4, 5.5), (6, .5), (7, 2), (8, 3.3), (9, 4.6), (10, 6)))]
    sun = [dot(500, 480, 60, "#ffe2a8", .1), glow(500, 480, 180, .1, .7, "fire")] + [line([[500 + 70 * math.cos(a), 480 + 70 * math.sin(a)], [500 + 150 * math.cos(a), 480 + 150 * math.sin(a)]], .6 + .1 * k, "#ffcf8a", 4, dur=.4)
                                                                                     for k, a in enumerate((.3, 1.2, 2.2, 3.4, 4.4, 5.4))]
    tree = {"base": "dark", "cam": [1, 500, 860], "els": sun + [oval(500, 960, 320, 320, "#5a4330", "#8a6a48", 3, 1, .1)] + rings + storms}
    # 2 · simple shapes anyone can carve; carvings spread over millennia, most after 1300 CE
    stick = lambda x, y, at: [ring(x, y - 40, 14, at, C, 4, dur=.3), line([[x, y - 26], [x, y + 20]], at + .1, C, 4, dur=.3), line([[x - 26, y - 12], [x, y - 2], [x + 26, y - 12]], at + .2, C, 4, dur=.3)]
    ladder = lambda x, y, at: [line([[x - 16, y - 50], [x - 16, y + 30]], at, C, 4, dur=.3), line([[x + 16, y - 50], [x + 16, y + 30]], at, C, 4, dur=.3)] + \
        [line([[x - 16, y - 40 + 16 * k], [x + 16, y - 40 + 16 * k]], at + .1 + .05 * k, C, 3, dur=.2) for k in range(5)]
    glyphs = []
    for k, (x, y) in enumerate([(180, 560), (380, 560), (620, 560), (820, 560), (180, 760), (380, 760), (620, 760), (820, 760)]):
        at = .4 + .45 * k
        glyphs += stick(x, y, at) if k % 3 == 0 else ladder(x, y, at) if k % 3 == 1 else [ring(x, y - 10, 34, at, C, 4, dur=.4), ring(x, y - 10, 16, at + .2, C, 4, dur=.3)]
    rock = [bx(80, 440, 840, 440, "#6b3a2a", "#b8765a", 2, 24, .1, op=.8)]
    X = lambda yr: 120 + 760 * (yr + 3000) / 4700
    dots = [dot(X(yr), 1180 - 16 * (k % 4), 7, C, 8.2 + .02 * k) for k, yr in enumerate([-2800, -2200, -1500, -900, -300, 200, 600, 900] + [1300 + 9 * j for j in range(42)])]
    chance = {"base": "dark", "cam": [1, 500, 880], "els": rock + glyphs + [line([[100, 1200], [900, 1200]], 7.8, "#8c7152", 3), label(X(-3000), 1250, "3000 BCE", 7.9, BN, 26),
              label(X(1500), 1250, "1300–1680 CE", 9.8, AMB, 28), bx(X(1300) - 6, 1100, X(1680) - X(1300) + 12, 110, "none", AMB, 2.5, 10, 9.8)] + dots}
    # 4 · the prediction nobody has tested: short windows, and no direct dates yet
    test = {"base": "dark", "cam": [1, 500, 880], "els": [line([[100, 1100], [900, 1100]], .1, "#8c7152", 3),
            bx(260, 900, 80, 200, BLUE, "#9fd0ff", 2, 6, 1.2, op=.18, style="inferred"), bx(620, 900, 80, 200, BLUE, "#9fd0ff", 2, 6, 1.6, op=.18, style="inferred"),
            bx(262, 902, 76, 196, "none", BLUE, 2.5, 6, 1.2, style="inferred"), bx(622, 902, 76, 196, "none", BLUE, 2.5, 6, 1.6, style="inferred")] +
           question(300, 1000, 4.6, 70, BLUE) + question(660, 1000, 4.8, 70, BLUE) +
           [bx(450, 620, 100, 150, "none", LILAC, 3, 10, 5.4, style="claimed"), bx(470, 590, 60, 30, "none", LILAC, 3, 4, 5.4, style="claimed")]}
    # 5 · plasma as a technology: a claimed bolt over a pyramid, struck through
    tech = {"base": "dark", "floor": 1150, "cam": [1, 500, 900], "els": [{"k": "poly", "p": [[260, 1150], [500, 800], [740, 1150]], "fill": "#c9a86a", "c": "#e8d6b0", "w": 2, "in": .2},
            line([[500, 800], [470, 700], [530, 620], [490, 520], [540, 420]], 1.0, "#cfe6ff", 5, "claimed", .8), glow(500, 620, 160, 1.2, .5, "scan"),
            strike(280, 760, 720, 520, 3.6)]}
    return remix(ep, scenes={2: chance, 3: tree, 4: test, 5: tech}, alias={6: 0}, cams={6: [1.1, 500, 860]},
                 drop=("para", "num", "title", "q", "cap", "label"), line_adds={(1, 1): (aurora, None)})


def serpent_m():
    """Serpent Mound as one continuous take (see mural.py): the snake drawn, the tilt argument, the dates and the finger-width shift are drawn."""
    import copy
    from mural import remix
    from iso3d import project
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN
    ep = serpent()
    ep["beats"][2]["visual"]["from"] = 1                       # the tilt argument gets its own panel; the dates panel is first seen with the dates
    GRN, SUN = "#a8c07a", "#ffd9a0"
    # 0 · the snake, held still so the sun can sit at the end of its sightline
    s0 = copy.deepcopy(ep["shots"][0])
    iso_ = next(e for e in s0["els"] if e.get("k") == "iso")
    iso_.update(spin=0, s=7.0, x=400)
    iso_["items"] = [it for it in iso_["items"] if not (it.get("t") == "label" and "sunset" in it.get("text", ""))]
    zh = 10 * math.sin(3.3 * math.pi) * .75
    hx, hy = project(s0, [40, .6, zh])
    sx, sy = project(s0, [52, .7, zh - 7.2])
    sun = [glow(sx, sy - 10, 150, 6.0, .9, "sun"), dot(sx, sy - 6, 26, SUN, 6.0)]
    # 3 · the serpent, drawn: a bank as wide as a road and waist high; tail, body, jaws, oval; four pitches long
    coil = [[200 + (12 + 9 * t) * math.cos(t), 860 + (12 + 9 * t) * math.sin(t)] for t in [k * .2 for k in range(32)]]
    body = [[round(268 + 492 * k / 40, 1), round(860 + 70 * math.sin(k / 40 * 3.3 * math.pi) * (1 - .25 * k / 40), 1)] for k in range(41)]
    ex, ey = body[-1]
    pitch = lambda x, at: [bx(x, 1060, 170, 110, "#3f6e3a", "#e8f0e0", 2, 2, at, fx="pop"), line([[x + 85, 1060], [x + 85, 1170]], at + .1, "#e8f0e0", 2, draw=False),
                           ring(x + 85, 1115, 18, at + .1, "#e8f0e0", 2, dur=.3)]
    drawn = {"base": "dark", "cam": [1, 500, 880], "els": [line([[180, 520], [820, 520]], .2, "#8c7152", 3, draw=False),
             {"k": "poly", "p": ellipse(500, 520, 162, 50, 24, 180, 360), "fill": "#6f8a4a", "c": GRN, "w": 2, "curve": True, "in": .4, "fx": "fill", "dur": .6},
             person(720, 520, 85, 1.6), label(500, 590, "a road wide, waist high", 1.8, "#cbbca8", 28),
             line(coil, 2.2, GRN, 16, dur=.8, curve=True), line(body, 2.6, GRN, 16, dur=1.2, curve=True),
             line([[ex, ey], [ex + 70, ey - 44]], 3.4, GRN, 14, dur=.4), line([[ex, ey], [ex + 70, ey + 44]], 3.4, GRN, 14, dur=.4),
             oval(ex + 76, ey, 34, 22, "#6f8a4a", GRN, 4, 1, 3.9)] +
            sum([pitch(150 + 180 * k, round(4.6 + .3 * k, 2)) for k in range(4)], []) + [label(500, 1240, "about 411 m", 5.8, AMB, 36, st="serif")]}
    # 1 · the claim: Earth's lean slowly rocks, the solstice sunset creeps; read the head's aim, read the year
    ax_ = lambda deg, L=170: [[round(330 - L * math.sin(math.radians(deg)), 1), round(640 + L * math.cos(math.radians(deg)), 1)], [round(330 + L * math.sin(math.radians(deg)), 1), round(640 - L * math.cos(math.radians(deg)), 1)]]
    rock = [[round(330 + 205 * math.sin(math.radians(a)), 1), round(640 - 205 * math.cos(math.radians(a)), 1)] for a in range(14, 34, 2)]
    draco = [(600, 470), (650, 420), (720, 440), (760, 500), (740, 570), (800, 620), (860, 590), (890, 530), (850, 480)]
    tilt = {"base": "dark", "stars": 60, "cam": [1, 500, 880], "els": [label(500, 340, "13,000 years ago?", 2.4, LILAC, 40, st="serif"),
            oval(330, 640, 110, 110, "#2f5f7a", "#9fd0ff", 2, 1, 3.6), oval(300, 610, 42, 28, "#5f8a5a", "none", 0, .9, 3.7),
            line(ax_(23.4), 4.0, BN, 3), arrow(rock, 4.8, AMB, 3, dur=.6), arrow(rock[::-1], 5.4, AMB, 3, dur=.6),
            bx(100, 1060, 800, 160, "#2c2419", r=0, at=7.0, op=.9), line([[100, 1060], [900, 1060]], 7.0, "#8c7152", 3, dur=.6)] +
           [ring(600 + 40 * k, 1040, 20, 7.6 + .4 * k, SUN, 2, "inferred", .4) for k in range(2)] + [dot(680, 1040, 20, SUN, 8.4), glow(680, 1040, 90, 8.4, .8, "sun"),
            arrow([[600, 1000], [680, 1000]], 8.0, AMB, 3, dur=.6, curve=False),
            line([[150, 1250], [230, 1200], [300, 1180]], 9.0, GRN, 12, dur=.5, curve=True), oval(318, 1176, 20, 13, "#6f8a4a", GRN, 3, 1, 9.2),
            line([[318, 1176], [680, 1060]], 9.4, AMB, 2, "inferred", .8)] + question(680, 960, 10.6, 70) +
           [line([list(a), list(b)], 12.0 + .08 * k, LILAC, 2, "claimed", .3) for k, (a, b) in enumerate(zip(draco, draco[1:]))] +
           [dot(x, y, 6, "#fff6e8", 11.6 + .08 * k) for k, (x, y) in enumerate(draco)] + [label(760, 700, "Draco", 13.0, LILAC, 32)]}
    # 4 · the dates: a carbon clock in the charcoal, what lies beneath came first; two camps, both in the last 3,000 years
    X = lambda yr: 120 + 760 * (yr + 11000) / 13000
    dates = {"base": "dark", "cam": [1, 500, 880], "els": [line([[120, 640], [880, 640]], .1, "#8c7152", 3, draw=False),
             {"k": "poly", "p": ellipse(500, 640, 220, 110, 30, 180, 360), "fill": "#6f8a4a", "c": GRN, "w": 2, "curve": True, "in": .2, "fx": "fill", "dur": .6}] +
            [dot(440 + 30 * k, 600 + (8 if k % 2 else -6), 8, "#1a1511", 1.0 + .1 * k, op=.95) for k in range(5)] + [glow(500, 600, 90, 1.4, .7, "lamp"),
             dot(620, 668, 13, AU, 3.6), glow(620, 668, 50, 3.7, .7), label(650, 680, "there first", 4.0, AU, 28, "start"),
             line([[120, 1000], [880, 1000]], 5.6, "#8c7152", 3, dur=.8), label(120, 1050, "11,000 BCE", 5.8, "#cbbca8", 28, "start"), label(X(-5000), 1050, "5000 BCE", 5.9, "#cbbca8", 28),
             label(880, 1050, "today", 6.0, "#cbbca8", 28, "end"),
             dot(X(-300), 1000, 10, AU, 7.6), line([[X(-300), 990], [X(-300), 940]], 7.7, AU, 2, draw=False), label(X(-300) - 8, 930, "Adena, 300 BCE", 7.8, AU, 28, "end"),
             dot(X(1070), 1000, 10, BLUE, 9.2), line([[X(1070), 990], [X(1070), 890]], 9.3, BLUE, 2, draw=False), label(X(1070) - 8, 880, "Fort Ancient, 1070 CE", 9.4, BLUE, 28, "end"),
             line([[X(-1000), 1080], [X(-1000), 1092], [881, 1092], [881, 1080]], 10.2, AMB, 3), label(793, 1140, "last 3,000 years", 10.4, AMB, 28),
             ring(120, 1000, 22, 11.4, LILAC, 3, "claimed"), label(130, 940, "Ice Age claim", 11.4, LILAC, 28, "start"), label(130, 1140, "nothing dated here", 11.8, LILAC, 28, "start")]}
    # 5 · less than a degree: smaller than a finger at arm's length, smaller than the aim of an earthen head
    shift = {"base": "dark", "stars": 50, "cam": [1, 500, 880], "els": [ring(439, 822, 40, 1.4, SUN, 2, "inferred", .5), dot(560, 822, 40, SUN, 2.4), glow(560, 800, 200, 2.4, .8, "sun"),
             bx(60, 820, 880, 600, "#2c2419", r=0, at=.1), line([[60, 820], [940, 820]], .1, "#8c7152", 3, draw=False),
             arrow([[439, 745], [560, 745]], 3.4, AMB, 3, dur=.5, curve=False), label(500, 660, "less than 1°", 3.8, AMB, 36, st="serif"),
             {"k": "poly", "p": [[500, 1380], [200, 822], [800, 822]], "fill": AMB, "c": "none", "w": 0, "in": 7.8, "op": .14, "keepop": True},
             line([[500, 1380], [200, 822]], 7.8, AMB, 2, "inferred", .6), line([[500, 1380], [800, 822]], 7.8, AMB, 2, "inferred", .6),
             oval(500, 1385, 80, 26, "#6f8a4a", GRN, 3, 1, 7.2),
             bx(425, 860, 150, 340, "#e8d6b8", "#c9b08a", 2, 75, 4.6, op=.55, fx="rise"), bx(458, 876, 84, 96, "#f5ecdc", "#c9b08a", 1.5, 40, 4.6, op=.55, fx="rise")]}
    draco2 = [(620, 380), (670, 340), (740, 355), (780, 410), (760, 470), (820, 510), (880, 485), (905, 430)]
    away = [line([list(a), list(b)], .9 + .08 * k, LILAC, 2, "claimed", .3) for k, (a, b) in enumerate(zip(draco2, draco2[1:]))] + \
           [dot(x, y, 6, "#fff6e8", .5 + .08 * k) for k, (x, y) in enumerate(draco2)] + [label(760, 560, "Draco", 1.2, LILAC, 32)]
    proud = [glow(sx, sy - 10, 240, 1.0, .7, "sun"), line([[hx, hy], [sx, sy]], 1.2, AMB, 3, "inferred", .8)]
    return remix(ep, scenes={0: s0, 1: tilt, 3: drawn, 4: dates, 5: shift}, alias={2: 0, 6: 0},
                 cams={0: [1.05, 480, 900], 2: [1.6, 690, hy - 40], 6: [1.05, 480, 920]},
                 drop=("para", "num", "title", "q", "cap"), adds={0: sun}, line_adds={(4, 1): (away, None), (5, 1): (proud, None)})


def edfu_m():
    """The Edfu texts as one continuous take (see mural.py): the island rises, the claim floods it, the dates line up, the Nile falls and the fields appear."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN
    ep = edfu()
    ep["beats"][3]["visual"]["from"] = 3                       # the claim and the dates swap walls, so the take runs neighbour to neighbour
    ep["beats"][4]["visual"]["from"] = 4
    SAND, NILE = "#d8c7a2", "#3f7f9c"
    # 0 · the temple's walls fill with carved text; is it Atlantis?
    walls = [{"k": "glyphs", "x": 222, "y": 650, "w": 200, "h": 520, "rows": 14, "cols": 5, "c": "#6b5236", "sw": 2.5, "in": .6, "fx": "draw", "dur": 1.6},
             {"k": "glyphs", "x": 578, "y": 650, "w": 200, "h": 520, "rows": 14, "cols": 5, "c": "#6b5236", "sw": 2.5, "in": 1.2, "fx": "draw", "dur": 1.6, "seed": 7}] + question(500, 540, 9.6, 90)
    # 2 · the story: an island rises, reeds, creator beings, a falcon lands; enemies, ruin, the world made again
    isl = [[300, 980], [380, 920], [500, 900], [620, 920], [700, 980]]
    story = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "water", "y": 960, "h": 400, "x0": 60, "x1": 940, "op": .7, "in": .2},
             {"k": "poly", "p": isl, "fill": SAND, "c": "#fff3dc", "w": 1.6, "curve": True, "in": 1.6, "fx": "fill", "dur": .9}] +
            [line([[400 + k * 40, 930], [395 + k * 40 + (k % 3) * 6, 780 - (k % 2) * 30]], 3.2 + .1 * k, "#8fb57a", 3, dur=.4) for k in range(6)] +
            [person(x, 955, 56, 4.6 + .2 * k, "#e8c35a") for k, x in enumerate((370, 440, 560, 630))] +
            [arrow([[860, 460], [700, 560], [560, 735]], 6.0, AMB, 2, "inferred", .8),
             {"k": "poly", "p": [[500, 760], [540, 740], [575, 750], [545, 770], [520, 800], [500, 790]], "fill": "#6b4a2e", "c": "#e9dccb", "w": 1.4, "in": 6.6, "fx": "pop"},
             glow(500, 950, 360, 8.4, .7, "red"),
             line([[90, 1080], [140, 1050], [190, 1090], [240, 1050], [290, 1080]], 8.6, RD, 5, dur=.6, curve=True),
             line([[910, 1080], [860, 1050], [810, 1090], [760, 1050], [710, 1080]], 8.8, RD, 5, dur=.6, curve=True),
             bx(270, 700, 460, 300, "#120d0a", r=20, at=10.0, op=.55),
             glow(500, 620, 260, 11.4, .9, "sun"), line(isl, 11.6, AU, 4, dur=1.0, curve=True)]}
    # 3 · the claim: these walls are the first record of Atlantis; a sacred island flooded, its wise men sail away
    boat = lambda x, y, at: [{"k": "poly", "p": [[x - 30, y], [x + 30, y], [x + 20, y + 14], [x - 20, y + 14]], "fill": "#8a6a48", "c": "none", "w": 0, "in": at, "fx": "pop"},
                             {"k": "poly", "p": [[x, y - 40], [x, y - 2], [x + 22, y - 6]], "fill": "#efe6d2", "c": "none", "w": 0, "in": at, "fx": "pop"}]
    claim = {"base": "dark", "cam": [1, 500, 880], "els": [bx(462, 360, 36, 70, "#cbbca8", "#8a7a66", 2, 18, .2), line([[480, 430], [480, 480]], .2, "#8a7a66", 4, draw=False),
             line([[450, 480], [510, 480]], .2, "#8a7a66", 4, draw=False), ring(480, 400, 60, .5, LILAC, 2, "claimed"), ring(480, 400, 95, .8, LILAC, 2, "claimed"),
             {"k": "poly", "p": [[110, 780], [130, 560], [290, 560], [280, 780]], "fill": SAND, "c": "#fff3dc", "w": 1.6, "in": .6},
             {"k": "glyphs", "x": 150, "y": 580, "w": 120, "h": 180, "rows": 6, "cols": 4, "c": "#6b5236", "sw": 2.2, "in": .7},
             arrow([[300, 670], [400, 640], [520, 680]], 3.0, LILAC, 3, "claimed", .8),
             oval(700, 690, 150, 40, "none", LILAC, 3, 1, 3.4, style="claimed"), label(700, 610, "Atlantis?", 3.6, LILAC, 34, st="serif"),
             bx(160, 920, 80, 40, "#e2d2b4", "#8a7a66", 1.5, 8, 5.2), bx(150, 914, 12, 52, "#b89a70", r=3, at=5.2), bx(238, 914, 12, 52, "#b89a70", r=3, at=5.2),
             label(200, 1020, "Plato, 360 BCE", 5.2, BN, 30),
             bx(540, 650, 320, 110, NILE, r=10, at=9.4, op=.8, fx="fill", dur=1.0)] +
            boat(560, 830, 10.8) + boat(700, 880, 11.1) + boat(850, 830, 11.4) +
            [arrow([[560, 860], [470, 1000], [400, 1150]], 11.0, LILAC, 2, "claimed", .7), arrow([[700, 910], [700, 1100], [690, 1240]], 11.3, LILAC, 2, "claimed", .7),
             arrow([[850, 860], [890, 1000], [900, 1150]], 11.6, LILAC, 2, "claimed", .7)] + question(620, 1330, 13.0, 80)}
    # 4 · the dates: Plato first, then Edfu's stone; the island image already in the Pyramid Texts; and the Nile that taught it
    tl, ax = timeline(-2600, 0, [(-2500, "2500 BCE"), (-2000, "2000"), (-1500, "1500"), (-1000, "1000"), (-500, "500")], "Which came first")
    tl["els"] = [e for e in tl["els"] if e.get("k") not in ("cap", "title")]
    tl["els"] += event(ax, -360, "Plato writes Atlantis", row=0, c=AMB, i=1.9) + [{"k": "band", "x0": ax.x(-237), "x1": ax.x(-57), "y": 700, "h": 16, "c": GOLD, "t": "Edfu carved", "in": 2.6}] + \
                 event(ax, -2400, "the Pyramid Texts", row=1, c=BN, i=8.3) + \
                 [arrow([[ax.x(-150), 640], [ax.x(-1300), 500], [ax.x(-2400) + 12, 600]], 11.6, AMB, 3, dur=1.2), label(ax.x(-1300), 470, "2,000 years earlier", 12.0, AMB, 30)]
    tl["cam"] = [1, 500, 880]
    vig = lambda x0, at: [{"k": "poly", "p": [[x0, 1130], [x0 + 40, 1250], [x0 + 200, 1250], [x0 + 240, 1130], [x0 + 240, 1300], [x0, 1300]], "fill": "#4a3a2c", "c": "none", "w": 0, "in": at}]
    nile = vig(100, 1.2) + [bx(110, 1140, 220, 110, NILE, r=4, at=1.4, op=.85, fx="fill", dur=.6)] + \
           vig(370, 2.8) + [oval(440, 1205, 34, 16, "#3b2a1c", at=3.0), oval(540, 1205, 30, 14, "#3b2a1c", at=3.0), bx(380, 1205, 220, 45, NILE, r=4, at=3.0, op=.85, fx="fill", dur=.5)] + \
           vig(640, 4.2) + [oval(705, 1200, 42, 20, "#3b2a1c", at=4.4), oval(815, 1200, 40, 18, "#3b2a1c", at=4.4), bx(740, 1232, 40, 18, NILE, r=4, at=4.4, op=.85),
                            oval(705, 1186, 36, 8, "#8fb57a", at=4.8), oval(815, 1186, 34, 8, "#8fb57a", at=4.8), glow(760, 1190, 140, 5.4, .7, "lamp"),
                            label(500, 1360, "the Nile, every summer", 1.4, "#9fd0ff", 30)]
    # 5 · the verdict: everything points inside Egypt; the ideas are older than the stone
    nl = [[560, 330], [520, 450], [545, 580], [500, 720], [520, 860], [470, 1040]]
    verdict = {"base": "dark", "cam": [1, 500, 880], "els": [line(nl, .2, NILE, 9, dur=1.0, curve=True), line([[x + 22, y] for x, y in nl], .4, "#5f8a4a", 4, op=.6, curve=True),
               line([[x - 22, y] for x, y in nl], .4, "#5f8a4a", 4, op=.6, curve=True),
               {"k": "poly", "p": ellipse(520, 640, 60, 24, 16, 180, 360), "fill": SAND, "c": "#fff3dc", "w": 1.5, "curve": True, "in": 1.0, "fx": "fill", "dur": .5}] +
              [line([[505 + 14 * k, 625], [503 + 14 * k, 575]], 1.3 + .1 * k, "#8fb57a", 3, dur=.3) for k in range(3)] +
              [dot(505, 860, 10, GOLD, .6), label(540, 870, "Edfu", .6, GOLD, 28, "start"),
               ring(510, 690, 330, 4.2, AMB, 3), label(330, 520, "Egypt", 4.4, AMB, 34, st="ital"), arrow([[640, 700], [780, 640], [930, 560]], 5.0, LILAC, 3, "claimed", .6), strike(770, 560, 880, 680, 6.0, RD, 5),
               bx(380, 1110, 240, 110, SAND, "#fff3dc", 1.5, 4, 7.0)] +
              [bx(300, 1220 + 40 * k, 400, 40, c, r=2, at=7.4 + .2 * k) for k, c in enumerate(("#6a5640", "#544432", "#3e3226"))] +
              [glow(500, 1290, 220, 8.6, .8, "lamp"), arrow([[500, 1320], [500, 1230]], 8.8, AMB, 3, "inferred", .5, curve=False),
               glow(520, 620, 160, 10.8, .8, "lamp"),
               {"k": "glyphs", "x": 400, "y": 1124, "w": 200, "h": 84, "rows": 3, "cols": 6, "c": "#6b5236", "sw": 2.4, "in": 13.8, "fx": "draw", "dur": 1.2}]}
    return remix(ep, scenes={2: story, 3: claim, 4: tl, 5: verdict}, alias={6: 0}, cams={0: [1.05, 500, 900]},
                 drop=("para", "num", "title", "q", "cap"), adds={0: walls}, line_adds={(4, 1): (nile, None)})


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/sky-ledger.json)."""
    import recap
    return recap.recap(ledger, "sky-ledger", None)


def EPISODES():
    return [nebra_m(), great_year_m(), serpent_m(), edfu_m(), plasma_m(), ledger_recap()]
