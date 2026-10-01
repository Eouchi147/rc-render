"""File 11 · Myths That Came True. Legends the experts wrote off, and a few they were right about.
Troy, Vinland, Knossos, the Sea Peoples, the Amazon's garden cities, King Arthur and the Shroud of Turin.
Faith is never rated: the Shroud film weighs the linen's date, not what the cloth means to believers."""
import math, random
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box

SERIES = "Myths That Came True"
SEA = "#3f86b0"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


# ---------------------------------------------------------------- 11.01 Troy
def troy():
    n = 14; R = 26
    wall = [{"t": "slab", "x0": -40, "x1": 40, "z0": -34, "z1": 34, "y": 0, "c": "#9c8a6a"},
            {"t": "prism", "pts": [[R * .9 * math.cos(2 * math.pi * k / n), R * .9 * math.sin(2 * math.pi * k / n)] for k in range(n)], "y": 0, "h": 7, "c": "#b8a57c", "edge": "rgba(0,0,0,.25)"}]
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        p0 = (R * math.cos(a0), R * math.sin(a0)); p1 = (R * math.cos(a1), R * math.sin(a1))
        q0 = (R * .86 * math.cos(a0), R * .86 * math.sin(a0)); q1 = (R * .86 * math.cos(a1), R * .86 * math.sin(a1))
        wall.append({"t": "prism", "pts": [list(p0), list(p1), list(q1), list(q0)], "y": 0, "h": 8, "c": "#d6c49c", "edge": "rgba(0,0,0,.3)"})
    wall += [box(-R - 2, 0, 0, 5, 6, 10, "#cbb891"), {"t": "person", "x": 30, "y": 0, "z": 12, "h": 1.7},
             L_(0, 8, "Troy VI · the citadel · walls up to 5 m thick", GOLD, z=-R, dy=-24), L_(0, 0, "a lower town spread beyond · schematic", "#cfe6ff", z=R + 6, dy=40)]
    s0 = iso(wall, cam=[1, 500, 900], s=8.4, x=500, y=1000, az=-22, spin=1.2, el=.5, table=None)
    v = View(20, 37, 34.5, 43, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Troy · Hisarlık", 26.2389, 39.9575, {"c": GOLD}), ("Mycenae", 22.756, 37.73, {"a": "end", "lx": -18}), ("Hattusa · the Hittite capital", 34.61, 40.02, {"a": "end", "lx": -18, "ly": -22})],
                 extra=[{"k": "label", "x": v.p(24.5, 38.8)[0], "y": v.p(24.5, 38.8)[1], "t": "the Aegean", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = stat("c. 1280", "BCE", "a Hittite treaty binds Alaksandu, king of Wilusa, the city Greeks called Wilios, Ilion", "Beckman, Bryce & Cline 2011")
    cols = ["#6f5a44", "#7a6248", "#86704f", "#917a56", "#c9a370", "#b04a2a", "#a08260", "#ad8c66", "#b89870"]
    names = ["Troy I · c. 3000 BCE", "II · 'Priam's Treasure' (far too early)", "III", "IV", "V", "VI · the great walled citadel", "VIIa · burned, c. 1180 BCE", "VIII · Greek Ilion", "IX · Roman Ilium"]
    layers = [{"d": (8 - i) * 70, "c": cols[8 - i] if i != 6 else "#b04a2a", "t": names[i]} for i in range(9)][::-1]
    s3 = {"base": "section", "tod": "day", "ground": 520, "lx": 130, "layers": layers, "cam": [1, 500, 900],
          "els": [{"k": "label", "x": 500, "y": 470, "t": "Hisarlık, cut open · nine cities stacked · schematic", "c": AMBER, "in": .5}]}
    s4 = stat("3", "times a year", "the treaty had to be read aloud to the king of Wilusa", "Beckman, Bryce & Cline 2011")
    tl, ax = timeline(-1800, -600, [(-1800, "1800 BCE"), (-1500, "1500"), (-1200, "1200"), (-900, "900"), (-600, "600")], "Troy and the poem")
    tl["els"] += [{"k": "band", "x0": ax.x(-1750), "x1": ax.x(-1300), "y": 700, "h": 16, "c": GOLD, "t": "Troy VI", "in": .3}] + \
                 event(ax, -1280, "the Wilusa treaty", row=1, c=SCAN, i=.6) + event(ax, -1180, "Troy VIIa burns", row=2, c=RED, i=.9) + \
                 [{"k": "band", "x0": ax.x(-750), "x1": ax.x(-650), "y": 700, "h": 16, "c": AMBER, "t": "the Iliad", "in": 1.2}]
    s5 = tl
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:TROY][sfx:boom][act:storytelling, setting the scene]For much of the nineteenth century, serious historians filed Troy under ^poetry. [act:light, a small smile]A city from ^Homer, like ^Olympus.",
                      "[d:tension][cam:1.12|0|0][act:the turn, a glint in the eye]Then two ^amateurs started digging."], cut=False),
        B("world", 1, ["[d:calm][k:THE DIG][act:plain, orienting]Hisarlık, in northwest ^Turkey. [act:storytelling, building][tune:level]A British consul, Frank Calvert, and a rich ^businessman, Heinrich Schliemann, dug into the ^mound...",
                       "[d:build][go:3|0][sfx:shimmer][act:the reveal, delighted wonder]...and found not ^one city, but ^nine, stacked on top of each other."]),
        B("collision", 0, ["[d:build][k:THE WALLS][act:impressed, descriptive]Troy Six: a Bronze Age citadel with sloping stone walls up to ^five metres thick. [act:adding more, bright]And from {1988|nineteen eighty-eight}, surveys@noun found a ^lower town around it."]),
        B("cost", 2, ["[d:build][k:THE NAME][act:turning a page, intrigued]Then the Hittite ^archives. [act:careful, pronouncing it]They name a kingdom in the ^west called ^Wilusa. [act:the connection, slower][tune:level]In Greek: ^Wilios. [act:the payoff, a quiet smile][tune:fall]^Ilion.",
                      "[d:build][go:4|0][act:storytelling, amused]Its king ^Alaksandu signed a treaty that had to be read@past to him ^three times a year. [d:aside][act:lighter, a knowing aside]Homer's Paris has ^another name: ^Alexandros."]),
        B("reversal", 5, ["[d:reveal][k:THE FIRE][act:grave, lower, slower]Troy Seven A ended in ^fire around {1180|eleven eighty} BCE, with bronze ^arrowheads and ^bodies in the ruins.",
                          "[d:build][sfx:hit][act:the complication, fair]But ^no text names the attackers. [act:weighing the options][tune:fall]^Greeks, ^raiders, ^rivals, or the collapse of a whole ^world."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Homer's Troy, a ^real and ^powerful city? [act:the verdict, confident][tune:fall]*Strong ^evidence*. [act:the other half, careful][tune:rise]The war ^exactly as Homer sings it? [act:gentle, warm][tune:fall]Still a ^poem.",
                     "[d:tension][p:0.93][act:candid, even][tune:level]The experts were ^wrong about the city. [act:the last word, a warm smile][tune:fall]The ^shovel was right."]),
    ]
    return EP("troy", "11.01", "Troy: The Myth the Experts Wrote Off", "troy", "strong", "Was Homer's Troy a real city, and did it fall in a real war?", "Then two amateurs started *digging*.", beats, shots,
              "Blegen et al. 1950–1958 · Latacz 2004 · Beckman, Bryce & Cline 2011 · Jablonka & Rose 2004 · Korfmann, Troia project",
              "Nineteenth-century scholars filed Troy under poetry. Then a consul, a banker with a shovel, a Hittite treaty and a buried lower town brought it back.",
              ["#Troy", "#Homer", "#Iliad", "#Archaeology", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.02 Vinland
def vinland():
    def hall(x, z, L, W, H, rot=0):
        return {"t": "ext", "axis": "x", "x": x, "y": 0, "at": z, "d": L, "prof": [[-W / 2, 0], [W / 2, 0], [W / 2 - .4, H * .55], [0, H], [-W / 2 + .4, H * .55]], "c": "#6f8a4a", "edge": "rgba(0,0,0,.3)"}
    halls = [{"t": "slab", "x0": -24, "x1": 24, "z0": -16, "z1": 16, "y": 0, "c": "#8a9a5b"},
             {"t": "flat", "pts": [[-24, 10], [24, 10], [24, 16], [-24, 16]], "y": .05, "c": SEA, "op": .8, "ground": True},
             hall(-8, -2, 28, 8, 4.4), hall(10, -6, 14, 6, 3.6), hall(8, 6, 10, 5, 3.2),
             {"t": "person", "x": -2, "y": 0, "z": 9, "h": 1.7},
             L_(-8, 4.6, "turf halls, Norse style · schematic", GOLD, z=-2, dy=-24), L_(0, 0, "L'Anse aux Meadows · Newfoundland", "#cfe6ff", z=12, dy=40)]
    s0 = iso(halls, cam=[1, 500, 900], s=12, x=500, y=1000, az=-26, spin=1.2, el=.48, table=None)
    v = View(-72, 12, 44, 72, (40, 330, 920, 900))
    route = [(5.3, 60.4), (-21.9, 64.1), (-45.5, 61.15), (-55.53, 51.6)]
    s1 = mapshot(v, pins=[("Norway", 5.3, 60.4, {}), ("Iceland", -21.9, 64.1, {}), ("Greenland · Erik's colony", -45.5, 61.15, {"a": "end", "lx": -18, "ly": -22}), ("L'Anse aux Meadows", -55.53, 51.6, {"c": GOLD, "a": "start", "ly": 34})],
                 extra=[{"k": "line", "p": [v.p(a, b) for a, b in route], "c": GOLD, "w": 1.8, "op": .75, "style": "inferred", "curve": True, "in": .8}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}])
    rings = [{"k": "circle", "x": 500, "y": 860, "r": 20 + i * 7, "fill": "none", "c": "#6b4a2e" if i != 30 else GOLD, "w": 2 if i != 30 else 5, "op": .9, "in": .1 + i * .012} for i in range(60)]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "circle", "x": 500, "y": 860, "r": 450, "fill": "#c9a370", "c": "#6b4a2e", "w": 6, "in": .05}] + rings +
          [{"k": "label", "x": 500, "y": 360, "t": "993 CE: a solar storm marks one ring in every tree on Earth", "c": GOLD, "in": 1.2},
           {"k": "label", "x": 500, "y": 1370, "t": "29 more rings to the bark: the tree was cut in 1021", "c": AMBER, "in": 1.8}]}
    s3 = stat("1021", "CE", "the year Norse blades cut the dated wood: 471 years before Columbus", "Kuitems et al. 2022, Nature")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "poly", "p": [[430, 900], [470, 760], [530, 760], [570, 900], [500, 960]], "fill": "#8c6a48", "c": "#e9dccb", "w": 2, "curve": True, "in": .3},
                                                    {"k": "line", "p": [[500, 770], [500, 950]], "c": "#5a4330", "w": 2, "in": .5},
                                                    {"k": "cap", "x": 500, "y": 640, "t": "butternuts, found in the Norse layers", "in": .2},
                                                    {"k": "label", "x": 500, "y": 1060, "t": "the tree doesn't grow in Newfoundland", "c": AMBER, "in": .9},
                                                    {"k": "label", "x": 500, "y": 1120, "t": "someone went further south", "st": "small", "in": 1.3}]}
    s5 = stat("1920s", "pigment", "in the ink of the famous Vinland Map, which Yale declared a modern forgery in 2021", "Yale University 2021")
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 1, ["[d:intrigue][k:VINLAND][sfx:boom][act:storytelling, setting the scene]Icelandic sagas told of Vikings sailing ^west, to a land of ^grapes. [act:light, amused]For centuries, scholars ^shrugged. [act:playful, quoting the skeptics][tune:risefall]^Nice stories.",
                      "[d:tension][cam:1.12|0|0][act:the hook, wonder]Then a ^solar storm, a thousand years old, gave us the ^exact year."], cut=False),
        B("world", 1, ["[d:calm][k:THE SAGAS][act:storytelling, calm]^Greenland, around the year one ^thousand. [act:simple, vivid]Leif Eriksson sails ^west. [act:warm, naming them]The sagas describe ^halls, ^grapes and ^fights with the local people.",
                       "[d:aside][act:a quiet caveat, lower]Written down about ^two centuries later."]),
        B("collision", 0, ["[d:build][k:THE FIND][act:storytelling, growing excitement]In {1960|nineteen sixty}, the explorer Helge Ingstad and the archaeologist Anne Stine Ingstad found turf ^halls at the tip of ^Newfoundland. [act:counting them off][tune:level]Norse ^iron. [act:building, firmer][tune:level]Norse ^rivets. [act:the clincher, firm][tune:fall]Norse ^buildings."]),
        B("cost", 2, ["[d:build][k:THE DATE][act:curious, a quick one][tune:fall]But ^when? [act:wonder, explaining]In {993|nine ninety-three}, a burst from the ^sun stamped a spike of carbon into that year's ring in ^every tree on Earth.",
                      "[d:build][sfx:shimmer][act:precise, detective work]Three pieces of wood cut with ^metal blades carry that spike, ^twenty-nine rings from the bark. [go:3|0][sfx:hit][act:the answer, firm and clear]Cut in {1021|ten twenty-one}. [act:letting it land, slower]Four hundred and seventy-one years before ^Columbus."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, a delicious clue]And ^butternuts, in the Norse layers. [act:the key fact, plain]They ^don't grow in Newfoundland. [act:the conclusion, warm]The Vikings went further ^south.",
                          "[d:aside][go:5|0][act:lighter, a sideways glance][tune:rise]Meanwhile the famous Vinland ^Map? [act:plain, one beat][tune:highfall]A ^forgery. [act:explaining, brisk]Its ink holds a pigment first made in the {1920s|nineteen twenties}."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Vikings in ^America around the year one thousand? [act:the verdict, confident][tune:fall]^*Established*. [act:the open part, curious][tune:rise]Exactly ^where Vinland was? [act:even, plain][tune:fall]Still ^open.",
                     "[d:tension][p:0.93][act:warm, satisfied][tune:level]The ^sagas were ^right. [act:the last word, dry][tune:fall]The ^map was ^fake."]),
    ]
    return EP("vinland", "11.02", "Vinland: The Sagas Were Right", "vinland", "solid", "Did Norse Greenlanders really reach America five centuries before Columbus?", "Vikings in *America*?", beats, shots,
              "Kuitems et al. 2022, Nature · Ingstad 1977 · Wallace 2003 · Adam of Bremen c. 1075 · Yale University 2021",
              "Icelandic sagas told of a western land of grapes. Turf halls in Newfoundland, butternuts from further south, and a solar storm in the tree rings date the Vikings in America to 1021.",
              ["#Vikings", "#Vinland", "#Newfoundland", "#History", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.03 Knossos
def knossos():
    r = random.Random(11)
    pal = [{"t": "slab", "x0": -34, "x1": 34, "z0": -26, "z1": 26, "y": 0, "c": "#9c8a6a"},
           {"t": "flat", "pts": [[-12.5, -6], [12.5, -6], [12.5, 6], [-12.5, 6]], "y": .05, "c": "#e2cf9e", "ground": True}]
    for gx in range(-30, 31, 6):
        for gz in range(-22, 23, 6):
            if abs(gx) < 16 and abs(gz) < 9:
                continue
            if r.random() < .12:
                continue
            h = r.choice([3, 3, 4.5, 6, 7.5])
            pal.append(box(gx, gz, 0, 5.6, 5.6, h, r.choice(["#d9c9a6", "#cbb893", "#e2d3b0"]), "rgba(0,0,0,.28)"))
    pal += [{"t": "person", "x": 0, "y": 0, "z": 0, "h": 1.7},
            L_(0, 8, "hundreds of rooms, several storeys · schematic", GOLD, z=-20, dy=-24), L_(0, 0, "the central court · about 50 × 25 m", "#cfe6ff", z=0, dy=-14)]
    s0 = iso(pal, cam=[1, 500, 900], s=8.2, x=500, y=1000, az=-26, spin=1.2, el=.55, table=None)
    v = View(21.8, 28.6, 34.4, 38.6, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Knossos", 25.1631, 35.298, {"c": GOLD}), ("Thera · Santorini", 25.4, 36.4, {"c": RED}), ("Athens", 23.73, 37.98, {"a": "end", "lx": -18})],
                 extra=[{"k": "label", "x": v.p(24.8, 34.9)[0], "y": v.p(24.8, 34.9)[1], "t": "Crete", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    tab = [{"k": "rect", "x": 170, "y": 640, "w": 660, "h": 280, "fill": "#b89b72", "c": "#e9dccb", "sw": 1.6, "in": .1},
           {"k": "label", "x": 500, "y": 760, "t": "da-pu₂-ri-to-jo  po-ti-ni-ja", "st": "serif", "size": 40, "c": "#2a2219", "halo": False, "in": .5},
           {"k": "label", "x": 500, "y": 840, "t": "· honey ·", "st": "ital", "c": "#2a2219", "halo": False, "in": .8},
           {"k": "cap", "x": 500, "y": 580, "t": "a Linear B tablet from Knossos · KN Gg 702", "in": .2},
           {"k": "label", "x": 500, "y": 1000, "t": "'to the Mistress of the Labyrinth'", "st": "serif", "size": 38, "c": GOLD, "in": 1.2},
           {"k": "label", "x": 500, "y": 1060, "t": "the usual reading", "st": "small", "in": 1.5}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": tab}
    horns = [{"k": "poly", "p": [[300, 1000], [700, 1000], [700, 940], [640, 940], [620, 760], [580, 760], [590, 900], [410, 900], [420, 760], [380, 760], [360, 940], [300, 940]], "fill": "#d9c9a6", "c": "#fff3dc", "w": 2, "curve": False, "in": .3},
             {"k": "cap", "x": 500, "y": 640, "t": "'horns of consecration' · stone · schematic", "in": .2},
             {"k": "label", "x": 500, "y": 1100, "t": "bull-leaping frescoes · bull's-head vessels · stone horns", "c": AMBER, "in": 1.0}]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": horns}
    tl, ax = timeline(-2000, -1300, [(-2000, "2000 BCE"), (-1800, "1800"), (-1600, "1600"), (-1400, "1400")], "The palace")
    tl["els"] += event(ax, -1900, "first palace", row=1, c=GOLD, i=.3) + event(ax, -1700, "rebuilt", row=0, c=BONE, i=.5) + \
                 [{"k": "band", "x0": ax.x(-1611), "x1": ax.x(-1538), "y": 700, "h": 16, "c": RED, "t": "Thera erupts", "in": .7}] + \
                 event(ax, -1450, "fires across Crete", row=2, c=RED, i=1.0) + event(ax, -1350, "the end", row=1, c=BONE, i=1.2)
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what you see is partly Arthur Evans", "#ffb09a", ["the red columns: rebuilt in concrete", "the 'Throne Room': his name for it", "the upper floors: his reconstruction"])}
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:KNOSSOS · CRETE][sfx:boom][act:mythic, setting the scene][tune:level]A ^monster in a maze. [act:building, a little bigger][tune:level]A ^king who ruled the ^sea. [act:the third, a little darker][tune:fall]A ^volcano next door.",
                      "[d:tension][cam:1.12|0|0][act:curious, pulling us in][tune:fall]How much of the Minotaur was ^real?"], cut=False),
        B("world", 0, ["[d:calm][k:THE PALACE][act:plain, orienting]Knossos, on ^Crete. [act:impressed, descriptive]^Hundreds of rooms, several storeys ^high, around a central court about ^fifty metres long.",
                       "[d:aside][act:playful, a warm smile]Get ^lost in there, and you'd start telling ^stories too."]),
        B("collision", 3, ["[d:build][k:THE BULLS][act:delighted, going through them]And ^bulls everywhere: young people ^leaping over them in frescoes, bull's-head ^vessels, stone ^horns on the roofs.",
                           "[d:build][go:2|0][sfx:shimmer][act:intrigued, building][tune:level]And a clay ^tablet from Knossos records@verb ^honey... [act:the reveal, hushed wonder][tune:fall]for the Mistress of the ^Labyrinth."]),
        B("cost", 5, ["[d:build][k:THE CATCH][act:the catch, candid]But much of what visitors see is Arthur ^Evans, who dug it from {1900|nineteen hundred}. [act:dry, a raised eyebrow]He rebuilt it in ^concrete, and ^he named the rooms."]),
        B("reversal", 4, ["[d:reveal][k:THE VOLCANO][act:dramatic, lower]Next door, the volcano of Santorini ^exploded, somewhere between about {1611|sixteen eleven} and {1538|fifteen thirty-eight} BCE.",
                          "[d:build][sfx:hit][act:the turn, fair]But Knossos carried on for ^generations after. [act:quiet, precise]The myth was told by ^Greeks, ^centuries later."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A myth that remembers a real ^palace and a real ^bull cult? [act:the verdict, warm][tune:fall]^*Plausible*. [act:honest, a gentle limit]The chain of ^memory ^can't be traced.",
                     "[d:tension][p:0.93][act:gentle, clear][tune:level]The ^monster is a ^story. [act:the last word, quiet wonder][tune:fall]The ^maze was a ^building."]),
    ]
    return EP("knossos", "11.03", "Knossos: Inside the Minotaur's Labyrinth", "knossos", "plausible", "Does the Minotaur legend remember a real palace and a real sea power?", "How much of the Minotaur was *real*?", beats, shots,
              "Evans 1921–1935 · Ventris & Chadwick 1953 · Pearson et al. 2022, PNAS Nexus · Knossos excavation reports · Heraklion Archaeological Museum",
              "A monster in a maze, a king of the sea and a volcano next door: the palace of Knossos, its bulls, a tablet for the Mistress of the Labyrinth, and how much is Arthur Evans.",
              ["#Knossos", "#Minotaur", "#Crete", "#GreekMythology", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.04 The Sea Peoples
def sea_peoples():
    ships = [{"k": "boat", "x": 330, "y": 900, "w": 380, "in": .3}, {"k": "boat", "x": 690, "y": 1000, "w": 380, "in": .5}] + \
            [{"k": "person", "x": 250 + i * 40, "y": 880, "h": 60, "t": False, "in": .6 + i * .05} for i in range(5)] + \
            [{"k": "person", "x": 610 + i * 40, "y": 980, "h": 60, "t": False, "in": .8 + i * .05} for i in range(5)] + \
            [{"k": "water", "y": 930, "h": 400, "x0": -100, "x1": 1100, "op": .5, "in": .1},
             {"k": "cap", "x": 500, "y": 560, "t": "the sea battle carved at Medinet Habu · schematic", "in": .2},
             {"k": "label", "x": 500, "y": 1260, "t": "Ramesses III's temple, Egypt · c. 1177 BCE", "st": "small", "c": AMBER, "in": 1.2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": ships}
    v = View(18, 40, 24, 42.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Pylos", 21.67, 37.03, {"c": RED, "a": "end", "lx": -18}), ("Mycenae", 22.756, 37.73, {"c": RED}), ("Hattusa", 34.61, 40.02, {"c": RED}), ("Ugarit", 35.78, 35.6, {"c": RED}),
                          ("Medinet Habu · Thebes", 32.6, 25.72, {"c": GOLD, "a": "end", "lx": -18})],
                 extra=[{"k": "cap", "x": 500, "y": 390, "t": "c. 1225–1150 BCE: palaces burned or abandoned", "c": "#ffb09a", "in": 1.4}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}])
    nm = ["Sherden", "Shekelesh", "Ekwesh", "Lukka", "Teresh", "Peleset", "Tjeker", "Denyen", "Weshesh"]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 470, "t": "nine peoples named by Egypt", "c": AMBER, "in": .2}] +
          [{"k": "label", "x": 330 if i % 2 == 0 else 670, "y": 580 + (i // 2) * 110, "t": n, "st": "serif", "size": 40, "c": GOLD if n == "Peleset" else "#e9dccb", "in": .4 + i * .15} for i, n in enumerate(nm)] +
          [{"k": "label", "x": 500, "y": 1150, "t": "the Peleset: probably the Philistines", "st": "small", "c": AMBER, "in": 2.0}]}
    s3 = stat("3", "years", "of severe drought in tree rings at Gordion in Anatolia, around 1198–1196 BCE, as the Hittite empire ended", "Manning et al. 2023, Nature")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("a system failure", "#8fd9b0", ["drought, and failed harvests", "earthquakes", "broken trade in copper and tin", "revolts", "people on the move"])}
    tl, ax = timeline(-1240, -1150, [(-1240, "1240 BCE"), (-1210, "1210"), (-1180, "1180"), (-1150, "1150")], "A few decades")
    tl["els"] += event(ax, -1208, "Merneptah's battle", row=1, c=GOLD, i=.3) + event(ax, -1197, "the Hittite drought", row=0, c=SCAN, i=.6) + \
                 event(ax, -1191, "Ugarit's harbour burns", row=2, c=RED, i=.9) + event(ax, -1177, "Ramesses III's battles", row=1, c=GOLD, i=1.2)
    s5 = tl
    s6 = like(s1, cam=[1.1, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 1, ["[d:intrigue][k:THE SEA PEOPLES][sfx:boom][act:grave, setting the scene]Around {1200|twelve hundred} BCE, the great palaces of the ancient world ^burned, one after ^another. [act:tolling them, slow][tune:level]^Greece. [act:heavier, slower][tune:level]The ^Hittites. [act:the last, final][tune:fall]^Syria.",
                      "[d:tension][cam:1.12|0|0][act:intrigued, leaning in]Egypt blamed ^raiders from the sea."], cut=False),
        B("world", 0, ["[d:calm][k:THE ACCUSED][act:storytelling, vivid]Pharaoh Ramesses the Third carved the battle into his ^temple: ^ships, ^warriors, ^captives.",
                       "[d:build][go:2|0][act:precise, informative]Egypt named ^nine peoples. [act:the connection, interested]One of them, the Peleset, were ^probably the ^Philistines."]),
        B("collision", 5, ["[d:build][k:THE CASE][act:building the case, confident]And the timing ^fits. [act:evidence, plain]A harbour town of Ugarit burned around {1190|eleven ninety} BCE.",
                           "[d:build][sfx:shimmer][act:the modern clue, intrigued]Ancient DNA from Philistine Ashkelon shows ^newcomers with ^European ancestry."]),
        B("cost", 3, ["[d:build][k:THE DROUGHT][act:the counter-evidence, measured]But tree rings in Anatolia record@verb three years of savage ^drought around {1198|eleven ninety-eight} BCE. [act:quiet, widening the view]Pollen shows the ^whole Levant drying.",
                      "[d:build][act:the surprise, careful][tune:fallrise]And some cities weren't ^stormed at all. [act:quiet, the reveal][tune:fall]They were ^abandoned."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:the big picture, measured]Most experts now see a ^system failure: drought, failed harvests, broken ^trade, earthquakes, ^revolts, people on the ^move.",
                          "[d:build][sfx:hit][act:fair, conceding][tune:fall]The Sea Peoples were ^real. [act:thoughtful, a gentle turn]But maybe more ^symptom than ^cause."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]The Sea Peoples as the ^main cause of the collapse? [act:the verdict, balanced][tune:fall]^*Mixed record@noun*. [act:the other side, fair][tune:rise]A real force ^inside it? [act:simple, warm, sure][tune:highfall]^Yes.",
                     "[d:tension][p:0.93][act:quiet, a gentle warning]A ^connected world can fall ^faster than anyone expects."]),
    ]
    return EP("sea-peoples", "11.04", "The Sea Peoples and the End of the Bronze Age", "sea-peoples", "mixed", "Did the invading Sea Peoples bring down the Bronze Age world?", "Egypt blamed raiders from the *sea*.", beats, shots,
              "Cline 2014, 1177 B.C. · Knapp & Manning 2016 · Kaniewski et al. 2011 · Manning et al. 2023, Nature · Feldman et al. 2019, Science Advances · Drews 1993",
              "Around 1200 BCE palaces from Greece to Syria burned or emptied. Egypt blamed the Sea Peoples; tree rings, pollen and ancient DNA tell a bigger story.",
              ["#SeaPeoples", "#BronzeAge", "#AncientEgypt", "#History", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.05 The Amazon's garden cities
def amazon():
    r = random.Random(5)
    ground = [{"t": "slab", "x0": -40, "x1": 40, "z0": -30, "z1": 30, "y": 0, "c": "#3f6a3a"}]
    for k in range(34):
        x, z = r.uniform(-34, 34), r.uniform(-24, 24)
        ground.append(box(x, z, 0, r.uniform(3, 6), r.uniform(2.5, 5), r.uniform(.8, 2.2), "#a88a5e", "rgba(0,0,0,.3)"))
    ground += [{"t": "line", "p": [[-40, .3, -12], [40, .3, 8]], "c": "#e2cf9e", "w": 3, "op": .9}, {"t": "line", "p": [[-20, .3, -30], [-4, .3, 30]], "c": "#e2cf9e", "w": 3, "op": .9},
               {"t": "person", "x": 20, "y": 0, "z": 22, "h": 1.7},
               L_(0, 3, "earthen platforms and straight roads, under the forest", GOLD, z=-24, dy=-24), L_(0, 0, "as lidar sees them · schematic", "#cfe6ff", z=26, dy=40)]
    s0 = iso(ground, cam=[1, 500, 900], s=7.4, x=500, y=1000, az=-24, spin=1.2, el=.55, table=None)
    v = View(-82, -34, -22, 6, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Upano Valley · Ecuador", -78.1, -2.3, {"c": GOLD}), ("Llanos de Mojos · Bolivia", -65.0, -14.8, {}), ("Acre · Brazil", -67.8, -10.0, {"a": "end", "lx": -18}),
                          ("Upper Xingu", -53.0, -12.0, {})],
                 extra=[{"k": "label", "x": v.p(-60, -4)[0], "y": v.p(-60, -4)[1], "t": "Amazonia", "st": "ital", "c": "#8fd9b0"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}])
    s2 = stat("6,000", "platforms", "mapped by lidar in Ecuador's Upano Valley, built from about 500 BCE", "Rostain et al. 2024, Science")
    s3 = stat("24,000+", "earthworks", "estimated in south-western Amazonia alone, built between about 600 BCE and 850 CE", "Pärssinen et al. 2026")
    sec = {"base": "section", "tod": "day", "ground": 640, "lx": 130, "layers": [{"d": 0, "c": "#2a1f18", "t": "dark earth: charcoal, pottery, bone · made by people"}, {"d": 240, "c": "#c9a86a", "t": "the ordinary pale soil"}],
           "cam": [1, 500, 900], "els": [{"k": "label", "x": 500, "y": 590, "t": "terra preta · built up over centuries", "c": AMBER, "in": .6}]}
    s4 = sec
    tl, ax = timeline(-11500, 2100, [(-10000, "10,000 BCE"), (-6000, "6000"), (-2000, "2000 BCE"), (2000, "2000 CE")], "The dates")
    tl["els"] += event(ax, -10800, "Hancock's lost civilisation", row=2, c="#ffb09a", i=.3, sub="no trace found") + event(ax, -8900, "forest islands, first crops", row=1, c=BONE, i=.6) + \
                 [{"k": "band", "x0": ax.x(-600), "x1": ax.x(1500), "y": 700, "h": 16, "c": GOLD, "t": "the earthworks", "in": .9}]
    s5 = tl
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE AMAZON][sfx:boom][act:wonder, building][tune:level]Lasers fired through the rainforest found ^roads, ^plazas, ^canals... [act:the payoff, awe][tune:fall]and ^thousands of earthen platforms.",
                      "[d:tension][cam:1.12|0|0][act:the surprise, can you believe it][tune:risefall]The ^untouched jungle was once full of ^towns. [act:curious, pulling us in][tune:fall]^Who built them?"], cut=False),
        B("world", 2, ["[d:calm][k:THE FINDS][act:reporting, calm and clear]Ecuador's Upano Valley: about six thousand platforms, from around {500|five hundred} BCE. [go:1|0][act:impressed, vivid]In ^Bolivia, towns with mounds twenty-two metres ^high.",
                       "[d:build][go:3|0][act:the scale, wonder]And in ^one region alone, perhaps twenty-four ^thousand earthworks."]),
        B("collision", 5, ["[d:build][k:THE CASE][act:fair, giving him his due]Graham Hancock saw this ^coming, before much of the ^lidar. [act:even, laying out the idea]His explanation: knowledge inherited from a ^lost civilisation, from before about twelve thousand ^eight hundred years ago."]),
        B("cost", 5, ["[d:build][k:THE DATES][sfx:shimmer][act:the counterpoint, clear and fair]But ^every dated earthwork society falls within roughly the last ^twenty-six hundred years.",
                      "[d:build][act:adding weight, warm]And Amazonians were ^already growing their ^own crops around ^ten thousand years ago."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, playful][tune:rise]And the miracle soil, terra ^preta? [act:the reveal, delighted][tune:fall]^Household waste, ^charcoal and broken ^pottery, built up over ^centuries.",
                          "[d:build][sfx:hit][act:warm, respectful, admiring]The Kuikuro people of the Xingu ^still make it today."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Garden ^cities in the Amazon? [act:confident, warm]^Real, and ^bigger than anyone thought. [act:the other claim, even][tune:rise]^Inherited from a lost Ice Age civilisation? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*.",
                     "[d:tension][p:0.93][act:warm, a knowing smile][tune:fallrise]The Amazon's lost civilisation ^wasn't lost. [act:the last word, proud and plain][tune:fall]It was ^Amazonian."]),
    ]
    return EP("amazon-cities", "11.05", "Amazon Garden Cities: Lost Knowledge or Local Genius?", "amazon-cities", "unsupported", "Were the Amazon's earthworks and dark earths inherited from a lost Ice Age civilisation?", "The untouched jungle was full of *towns*.", beats, shots,
              "Rostain et al. 2024, Science · Prümers et al. 2022, Nature · Pärssinen et al. 2026 · Lombardo et al. 2020, Nature · Schmidt et al. 2023 · Hancock 2019",
              "Lidar found thousands of platforms, roads and earthworks under the Amazon rainforest: were they inherited from a lost Ice Age civilisation, or invented by Amazonians?",
              ["#Amazon", "#Lidar", "#LostCities", "#Archaeology", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.06 King Arthur
def arthur():
    head = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 36, "prof": [[-40, 0], [40, 0], [40, 2], [30, 14], [-4, 16], [-14, 12], [-26, 2], [-40, 1]], "c": "#6f8a4a", "edge": "rgba(0,0,0,.25)"},
            {"t": "flat", "pts": [[-40, -18], [40, -18], [40, 18], [-40, 18]], "y": 1.2, "c": SEA, "op": .7, "ground": False, "over": 2}] + \
           [box(x, z, 15.2, 3.4, 2.6, 1.6, "#9a8a70", "rgba(0,0,0,.3)") for x, z in ((-2, -6), (3, -2), (8, 3), (-4, 4), (12, -5), (16, 1))] + \
           [{"t": "person", "x": 6, "y": 15.5, "z": 8, "h": 1.7},
            L_(6, 17, "Tintagel · a high-status site, 400s–600s CE", GOLD, z=0, dy=-24), L_(0, 0, "imported Mediterranean pottery and glass · schematic", "#cfe6ff", z=18, dy=40)]
    s0 = iso(head, cam=[1, 500, 900], s=7, x=500, y=1000, az=-22, spin=1.2, el=.45, table=None)
    v = View(-8.5, 3, 49.5, 56.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Tintagel", -4.7597, 50.6683, {"c": GOLD, "a": "end", "lx": -18}), ("Glastonbury", -2.72, 51.15, {}), ("London", -0.13, 51.5, {})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    tl, ax = timeline(380, 1250, [(400, "400"), (600, "600"), (800, "800"), (1000, "1000"), (1200, "1200 CE")], "Where Arthur appears")
    tl["els"] += event(ax, 410, "Rome leaves", row=0, c=BONE, i=.3) + [{"k": "band", "x0": ax.x(490), "x1": ax.x(516), "y": 700, "h": 16, "c": GOLD, "t": "Badon", "in": .5}] + \
                 event(ax, 540, "Gildas: no Arthur", row=2, c=SCAN, i=.7) + event(ax, 829, "Arthur named", row=1, c=AMBER, i=1.0) + event(ax, 1136, "King Arthur", row=2, c="#ffb09a", i=1.3, sub="Geoffrey of Monmouth") + \
                 [{"k": "line", "p": [[ax.x(510), 770], [ax.x(829), 770]], "c": "#ffb09a", "w": 2, "style": "inferred", "in": 1.5}, {"k": "label", "x": ax.x(670), "y": 796, "t": "about 300 years", "st": "small", "c": "#ffb09a", "in": 1.6}]
    s2 = tl
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Gildas, writing c. 540", AMBER, ["the only British writer of his time", "a great victory at Mount Badon", "a hero: Ambrosius Aurelianus", "Arthur: not mentioned"])}
    s4 = stat("300", "years", "between the battle of Badon and the first text that names Arthur as its war-leader", "Historia Brittonum, 829–830")
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the candidates", "#9fd0ff", ["Riothamus, a British king in Gaul, c. 470", "Artorius, a Roman officer in Britain", "an unknown victor at Badon", "a hero of myth, given a history"])}
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:KING ARTHUR][sfx:boom][act:epic, restrained]Rome leaves ^Britain. [act:lower, simple]The lights go ^out. [act:mythic, building]And somewhere in the ^dark, a war-leader wins a famous ^battle.",
                      "[d:tension][cam:1.12|0|0][act:intrigued, pulling us in][tune:rise]Was his name ^Arthur?"], cut=False),
        B("world", 1, ["[d:calm][k:THE DARK AGE][act:sober, painting the loss]Britain after {410|four ten}: ^coins, pottery and ^towns ^disappear. [go:0|0][act:a hopeful turn, brighter]But in the ^west, at places like Tintagel, lords still imported pottery and glass from the ^Mediterranean."]),
        B("collision", 3, ["[d:build][k:THE WITNESS][act:introducing a witness, keen]One writer lived through it: Gildas, around {540|five forty}. [act:storytelling, vivid]He describes a great ^victory at Mount ^Badon.",
                           "[d:build][sfx:hit][act:plain, a set-up]He names a ^hero. [gap:0.4][act:quiet, pointed][tune:fall]Not ^Arthur."]),
        B("cost", 4, ["[d:build][k:THE GAP][act:the problem, measured]The ^first text to name Arthur as that war-leader comes about three ^hundred years later, in {829|eight twenty-nine}.",
                      "[d:build][go:2|0][act:light, a touch of wonder]The ^shining King Arthur, with his court, arrives in {1136|eleven thirty-six}, from ^Geoffrey of Monmouth."]),
        B("reversal", 5, ["[d:reveal][k:THE CANDIDATES][act:the turn, fair]Still: ^someone won Badon, and Gildas names almost ^nobody. [sfx:shimmer][act:laying out candidates][tune:level]^Riothamus, a British king who fought in ^Gaul. [act:the second, curious][tune:level]A Roman officer called ^Artorius. [act:the third, softer][tune:fall]Or a hero of ^myth, given a ^history."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A ^real Arthur? [act:the verdict, level-headed][tune:fall]^*Open question*. [act:confident, plain]The ^battle was real. [act:honest, a gentle limit]The ^name can't be pinned on ^anyone.",
                     "[d:tension][p:0.93][act:quiet, sure][tune:fall]^Someone won Badon. [act:the last word, gentle, open][tune:fall]Whether his name was ^Arthur, the evidence may ^never say."]),
    ]
    return EP("arthur", "11.06", "King Arthur: A Real Hero in Britain's Dark Age?", "arthur", "contested", "Did a real war-leader called Arthur fight the Saxons around 500 CE?", "Was his name *Arthur*?", beats, shots,
              "Gildas, De Excidio c. 540 · Historia Brittonum 829–830 · Annales Cambriae · Ward-Perkins 2005 · Barrowman et al. 2007 · Dumville 1977 · Ashe 1985",
              "Rome left, Britain went dark, and a war-leader won the battle of Badon. The one writer of the time never names Arthur: the gap, the candidates, and what Tintagel shows.",
              ["#KingArthur", "#Camelot", "#DarkAges", "#History", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.07 The Shroud of Turin
def shroud():
    cloth = [{"k": "rect", "x": 420, "y": 380, "w": 160, "h": 900, "fill": "#e6dcc6", "c": "#fff8ea", "sw": 1.2, "in": .1}] + \
            [{"k": "line", "p": [[420, 380 + k * 18], [580, 380 + k * 18]], "c": "#d4c7aa", "w": 1, "op": .5, "in": .15} for k in range(44)] + \
            [{"k": "poly", "p": [[480, 470], [520, 470], [530, 520], [556, 560], [552, 780], [530, 820], [470, 820], [448, 780], [444, 560], [470, 520]], "fill": "#c9ae88", "c": "none", "w": 0, "op": .35, "curve": True, "in": .8},
             {"k": "poly", "p": [[480, 1180], [520, 1180], [530, 1130], [556, 1090], [552, 870], [530, 840], [470, 840], [448, 870], [444, 1090], [470, 1130]], "fill": "#c9ae88", "c": "none", "w": 0, "op": .35, "curve": True, "in": 1.0},
             {"k": "cap", "x": 500, "y": 330, "t": "linen · about 4.4 × 1.1 m · schematic", "in": .2}]
    for e in cloth:
        if "y" in e: e["y"] += 120
        if "p" in e: e["p"] = [[x, y + 120] for x, y in e["p"]]
    cloth[0]["h"] = 800
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": cloth}
    v = View(-1, 13, 42.5, 50, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Lirey · first shown, 1350s", 4.05, 48.2, {"c": GOLD}), ("Chambéry · the fire of 1532", 5.92, 45.57, {"c": RED, "a": "end", "lx": -18}), ("Turin · since 1578", 7.6852, 45.0734, {})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = stat("1260–1390", "CE", "radiocarbon dates from three independent laboratories, in Arizona, Oxford and Zurich, 1988", "Damon et al. 1989, Nature")
    tl, ax = timeline(1300, 2040, [(1300, "1300"), (1500, "1500"), (1700, "1700"), (1900, "1900")], "The cloth on record")
    tl["els"] += event(ax, 1355, "first shown", row=1, c=GOLD, i=.3) + event(ax, 1389, "a bishop's report", row=0, c=BONE, i=.5) + event(ax, 1532, "fire", row=2, c=RED, i=.7) + \
                 event(ax, 1898, "the photograph", row=1, c=BONE, i=.9, sub="a negative image") + event(ax, 1988, "radiocarbon", row=0, c=SCAN, i=1.1) + event(ax, 2026, "fragments re-tested", row=2, c=SCAN, i=1.3)
    s3 = tl
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the case for an older date", "#9fd0ff", ["one strip, from one handled corner", "dates drift across the strip (2019)", "an X-ray method on one thread (2022)"])}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("still open", "#e8b87a", ["how the image formed", "any history before the 1350s", "a new, wider test"])}
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE SHROUD OF TURIN][sfx:boom][act:hushed, respectful]A linen sheet, over four metres long, with the ^faint image of a ^crucified man.",
                      "[d:tension][cam:1.1|0|0][act:intrigued, measured]The most ^tested cloth on Earth. [act:even, knowing]And the argument has ^never stopped."], cut=False),
        B("world", 1, ["[d:calm][k:THE RECORD][act:plain, historical]It first appears in France, in the {1350s|thirteen fifties}.",
                       "[d:build][go:3|0][act:careful, even-handed]In {1389|thirteen eighty-nine}, a ^bishop wrote to the pope that an earlier inquiry had found the ^artist who painted it."]),
        B("collision", 2, ["[d:build][k:THE TEST][act:precise, serious]In {1988|nineteen eighty-eight}, ^three laboratories, in Arizona, Oxford and Zurich, dated the linen ^independently.",
                           "[d:build][sfx:hit][act:the result, plain and calm]^Twelve sixty to ^thirteen ninety CE."]),
        B("cost", 4, ["[d:build][k:THE CRITICS][act:fair, giving them their due]Supporters of an older date answer: ^one strip, from one ^much-handled corner. [act:even, reporting]In {2019|twenty nineteen}, a ^reanalysis found the dates ^drift across the sample.",
                      "[d:build][act:balanced, careful]In {2022|twenty twenty-two}, an X-ray method on a ^single thread suggested the ^first century."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:the new evidence, measured]In {2026|twenty twenty-six}, a study of fragments left over from {1988|nineteen eighty-eight} found ^pure linen, ^matching the cloth. [sfx:hit][act:plain, precise][tune:level]No hidden ^repair. [act:calm, final][tune:fall]No ^contamination.",
                          "[d:build][act:open, with genuine wonder][tune:rise]But ^how the image was made? [act:honest, respectful]^Nobody has ^fully reproduced it."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Linen from the ^first century? [act:the verdict, careful and fair][tune:fall]*Ruled ^out* by the dating we have. [act:the open part, gentle][tune:rise]^How the image formed? [act:even, respectful][tune:fall]Still ^open.",
                     "[d:tension][p:0.93][act:sincere, gentle, with respect]What the Shroud ^means to believers is not something a ^laboratory can weigh."]),
    ]
    return EP("shroud", "11.07", "The Shroud of Turin: The Most Tested Cloth on Earth", "shroud", "debunked", "Is the Shroud's linen ancient, and how did its image form?", "The most tested cloth on *Earth*.", beats, shots,
              "Damon et al. 1989, Nature · d'Arcis memorandum 1389 · Casabianca et al. 2019, Archaeometry · De Caro et al. 2022 · Freer-Waters & Jull 2026",
              "A linen sheet with the faint image of a crucified man, dated by three laboratories to 1260–1390: the critics' case, the 2026 re-test, and the image nobody has fully explained.",
              ["#ShroudOfTurin", "#Science", "#History", "#Radiocarbon", "#MythsThatCameTrue"])


# ---------------------------------------------------------------- 11.08 The ledger
def _ledger_text():
    v = View(-95, 45, -25, 62, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("Troy", 26.24, 39.96, {"c": GOLD}), ("L'Anse aux Meadows", -55.53, 51.6, {"a": "end", "lx": -18}), ("Knossos", 25.16, 35.3, {"a": "end", "lx": -18, "ly": 34}),
                          ("Medinet Habu", 32.6, 25.72, {"a": "end", "lx": -18}), ("the Amazon", -65, -10, {}), ("Tintagel", -4.76, 50.67, {"a": "end", "lx": -18}), ("Turin", 7.69, 45.07, {})], cam=[1, 500, 860])
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established · strong", "#8fd9b0", ["Vikings in America, 1021", "Troy was a real, walled city", "Amazonian garden cities"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible · mixed · open", "#e8b87a", ["the Minotaur remembers Knossos", "the Sea Peoples ended the Bronze Age", "a real King Arthur"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["the Amazon's knowledge came from an Ice Age civilisation"], size=28)}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["Shroud linen from the first century"])}
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:MYTHS THAT CAME TRUE][sfx:boom][act:warm, opening the book]Seven legends the experts once ^wrote off, or trusted too ^much. [act:inviting, a small smile]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, ticking them off][tune:level]The Vikings reached ^America, in {1021|ten twenty-one} at the latest. [act:plain, sure][tune:level]^Troy was real. [act:the last one, warm][tune:fall]And the ^Amazon was full of ^towns."]),
        B("collision", 2, ["[d:build][k:STILL WEIGHED][act:weighing each, even][tune:level]The ^Minotaur may remember ^Knossos. [act:measured, even][tune:level]The Sea Peoples were part of a ^bigger collapse. [act:light, a quick check][tune:rise]And ^Arthur? [act:plain, open][tune:fall]Still ^open."]),
        B("cost", 3, ["[d:build][k:AWAITING EVIDENCE][act:even, fair]That the Amazon's builders ^inherited their knowledge from a lost Ice Age world. [d:aside][act:lighter, plain][tune:level]The record@noun keeps ^growing. [act:gentle, pointed][tune:fall]That idea ^isn't in it."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:clear, respectful]Shroud linen from the ^first century. [d:aside][act:sincere, gentle]What the cloth ^means is another question, and not ^ours to rate."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:warm, wise, even]Sometimes the myth was ^right and the experts were ^wrong. [act:a small smile][tune:fall]Sometimes the ^reverse. [go:5|1.5][act:simple, the lesson]The only way to know is to ^dig.",
                     "[d:tension][p:0.93][act:the motto, calm and warm]^Coherence is the measure. [act:quiet, the last word][tune:fall]Not ^final demonstration."]),
    ]
    return EP("myths-ledger", "11.08", "Myths That Came True · The Ledger", "", "mixed", "Which legends held up, and which didn't.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 11",
              "The verdicts of Myths That Came True in one ledger: the legends that were right, the ones still being weighed, and the one ruled out.",
              ["#History", "#Mythology", "#Archaeology", "#MythsThatCameTrue", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: seven legends in a cabinet, and an eighth niche with a trench still to dig (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    LAY = [(-150, -110, "#8a6a48"), (-110, -70, "#7a5c3e"), (-70, -30, "#6b4f35"), (-30, 0, "#5a4330")]
    dig = [{"k": "rect", "x": -190, "y": a, "w": 380, "h": b - a, "r": 0, "fill": c, "c": "none", "sw": 0} for a, b, c in LAY] + [
           {"k": "line", "p": [[-190, -150], [190, -150]], "c": "#7fa35a", "w": 4},
           {"k": "rect", "x": -60, "y": -150, "w": 120, "h": 80, "r": 2, "fill": "#1a120c", "c": "#8a6a48", "sw": 1.5},
           {"k": "rect", "x": -60, "y": -70, "w": 120, "h": 62, "r": 2, "fill": "none", "c": "#f5ecdc", "sw": 2, "style": "claimed"},
           {"k": "poly", "p": [[96, -236], [128, -210], [108, -186]], "fill": "#cbbca8", "c": "none", "w": 0},
           {"k": "line", "p": [[112, -211], [150, -250]], "c": "#8a5d33", "w": 7}]
    C = Cabinet([
        {"name": "Vinland", "model": mdl(vinland())},
        {"name": "Troy", "model": mdl(troy())},
        {"name": "Amazon towns", "model": mdl(amazon())},
        {"name": "Knossos", "model": mdl(knossos())},
        {"name": "The Sea Peoples", "model": mdl(sea_peoples(), 0)},
        {"name": "Arthur", "model": mdl(arthur())},
        {"name": "The Shroud", "model": mdl(shroud(), 0), "zk": .55},
        {"name": "Still to dig", "model": dig},
    ])
    C.build()
    VI, TR, AM, KN, SP, AR, SH, DG = range(8)
    G = "#e8c878"
    towns = C.local(AM, [{"k": "circle", "x": x, "y": y, "r": 5, "fill": "#f2c98e", "c": "none", "w": 0, "in": .2 + .06 * k, "fx": "pop"}
                         for k, (x, y) in enumerate([(-150, -40), (-120, -70), (-80, -30), (120, -50), (150, -80), (90, -20), (-30, -20), (40, -35), (-170, -90), (170, -30)])])
    ring = [{"k": "rect", "x": C.cells[SH]["x"] + 16, "y": C.cells[SH]["y"] + 16, "w": C.w - 32, "h": C.h - 32, "r": 6, "fill": "none", "c": G, "sw": 3, "fx": "draw", "dur": 1.4, "in": .6}]
    found = C.local(DG, [{"k": "rect", "x": -60, "y": -70, "w": 120, "h": 62, "r": 2, "fill": "#1a120c", "c": "#8a6a48", "sw": 1.5, "in": .2, "dur": .9},
                         {"k": "circle", "x": 18, "y": -30, "r": 9, "fill": "#e8c878", "c": "none", "w": 0, "in": 1.0, "fx": "pop"},
                         {"k": "glow", "x": 18, "y": -30, "r": 60, "kind": "lamp", "op": .6, "keepop": True, "in": 1.0}])
    s1 = C.step(C.cam_cell(VI), C.verdict(VI, "established", "America, by 1021", .4) + C.people(VI, 3, at=.9))
    s2 = C.step(C.cam_cell(TR), C.verdict(TR, "strong", "a real city", .3))
    s3 = C.step(C.cam_cell(AM), C.verdict(AM, "established", "full of towns", .3))
    s4 = C.step(C.cam_cell(KN), C.verdict(KN, "plausible", "it remembers Knossos?", .3))
    s5 = C.step(C.cam_cell(SP), C.verdict(SP, "plausible", "part of a bigger collapse", .3))
    s6 = C.step(C.cam_cell(AR))
    s7 = C.step(C.cam_cell(AR), C.verdict(AR, "open", at=.1) + C.question(AR, dx=C.w * .3, dy=-170, at=.3, size=70))
    s8 = C.step(C.cam_cell(AM), C.verdict(AM, "awaiting", "a lost Ice Age source?", .2, frame=False))
    s9 = C.step(C.cam_cell(AM), towns)
    s10 = C.step(C.cam_cell(AM), C.note(AM, "no trace of a lost world in it", at=.2, c=VCOL["awaiting"]))
    s11 = C.step(C.cam_cell(SH), C.verdict(SH, "ruled", at=.1) + C.struck(SH, "first-century linen", at=.2))
    s12 = C.step(C.cam_cell(SH), ring + C.note(SH, "what it means: never rated", at=1.0, c=G))
    s13 = C.step(C.cam_cells([VI, TR]), [e for k, i in enumerate((VI, TR)) for e in C.wash(i, VCOL["established"], at=.3 + .2 * k, op=.13)])
    s14 = C.step(C.cam_cells([SH, DG]))
    s15 = C.step(C.cam_cell(DG), found)
    s16 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5, (0, 2): "%d|1.1" % s6, (0, 3): "%d|.3" % s7}),
        3: (s8, {(0, 1): "%d|.3" % s9, (0, 2): "%d|.3" % s10}),
        4: (s11, {(0, 1): "%d|.3" % s12}),
        5: (s13, {(0, 1): "%d|1.1" % s14, (0, 2): "%d|1.0" % s15, (1, 0): "%d|3" % s16}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def _mur():
    from mural import remix
    import illus
    return remix, illus


def sea_peoples_m():
    """The Sea Peoples as one continuous take (see mural.py): palaces burn, nine peoples, three dry years, and a web that breaks."""
    remix, I = _mur()
    ep = sea_peoples()
    pins = [e for e in ep["shots"][1]["els"] if e.get("k") == "pin"]
    fires = [I.glow(p["x"], p["y"], 70, 2.6 + .9 * k, .9, "fire") for k, p in enumerate(pins[:4])]
    helm = lambda x, y, at, kind: [I.person(x, y, 150, at)] + ([I.line([[x - 18, y - 150], [x - 10, y - 185]], at + .1, I.AMBER, 3), I.line([[x, y - 152], [x, y - 190]], at + .1, I.AMBER, 3),
                                                              I.line([[x + 18, y - 150], [x + 10, y - 185]], at + .1, I.AMBER, 3)] if kind == "feather" else
                                                             [I.line([[x - 22, y - 150], [x - 34, y - 175]], at + .1, "#cbbca8", 3), I.line([[x + 22, y - 150], [x + 34, y - 175]], at + .1, "#cbbca8", 3)] if kind == "horn" else [])
    nine = {"base": "dark", "cam": [1, 500, 900], "els": sum([helm(150 + 88 * k, 1000 if k % 2 else 1060, .3 + .2 * k, "feather" if k == 5 else ("horn" if k == 0 else "")) for k in range(9)], []) +
            [I.glow(150 + 88 * 5, 900, 90, 3.0, .7), I.label(150 + 88 * 5, 1110, "Peleset", 3.0, I.AMBER, 30), I.arrow([[590, 1150], [590, 1230]], 3.8, I.AMBER, 3, dur=.4, curve=False),
             I.label(590, 1290, "Philistines?", 4.2, I.AMBER, 32)]}
    dna = [I.line([[160 + 9 * k, round(1290 + 18 * math.sin(k * .6 + ph), 1)] for k in range(40)], .3, I.BLUE, 3, dur=1.0) for ph in (0, math.pi)] + \
          [I.box(560, 1270, 300, 40, I.AMBER, r=6, at=1.2), I.box(760, 1270, 100, 40, I.BLUE, r=6, at=2.2, fx="pop")]
    rings = [I.ring(330, 880, 30 + 22 * k, .2 + .04 * k, "#8a6a48" if k % 2 else "#a8865e", 3, dur=.4) for k in range(12)] + \
            [I.ring(330, 880, 30 + 22 * k, 2.2 + .4 * j, I.RED, 5, dur=.4) for j, k in enumerate((7, 8, 9))]
    lev = [I.box(560, 640, 330, 440, "#5f8a5a", r=12, at=4.0), I.box(560, 640, 330, 440, "#c9a06a", r=12, at=5.2, dur=2.5)]
    city = [I.box(120 + 90 * k, 1260 - 30 * (k % 2), 70, 60, "none", "#cbbca8", 2, 3, 8.6 + .15 * k, style="claimed") for k in range(8)]
    drought = {"base": "dark", "cam": [1, 500, 900], "els": [I.oval(330, 880, 300, 300, "#5a4330", "#8a6a48", 3, 1, .1)] + rings + lev + city}
    icons = [("drought", 0), ("harvest", 1), ("trade", 2), ("quake", 3), ("revolt", 4), ("move", 5)]
    nodes = [(500 + 280 * math.cos(-math.pi / 2 + 2 * math.pi * k / 6), 880 + 280 * math.sin(-math.pi / 2 + 2 * math.pi * k / 6)) for k in range(6)]
    web = [I.line([nodes[a], nodes[b]], .3, "#8a8378", 2, dur=.6) for a in range(6) for b in range(a + 1, 6)]
    web += sum([[I.dot(x, y, 26, "#2a221b", .8 + .8 * k), I.ring(x, y, 26, .8 + .8 * k, I.AMBER, 3, dur=.4), I.label(x, y + 62, n, .9 + .8 * k, I.BONE, 26)] for k, ((n, _), (x, y)) in enumerate(zip(icons, nodes))], [])
    web += [I.strike(nodes[a][0] * .5 + nodes[b][0] * .5 - 20, nodes[a][1] * .5 + nodes[b][1] * .5 - 20, nodes[a][0] * .5 + nodes[b][0] * .5 + 20, nodes[a][1] * .5 + nodes[b][1] * .5 + 20, 5.6 + .3 * j, I.RED, 5)
            for j, (a, b) in enumerate(((0, 1), (1, 2), (2, 4), (3, 5), (0, 3)))]
    web += [{"k": "boat", "x": 860, "y": 1300, "w": 150, "in": 8.0}, I.glow(860, 1270, 90, 8.0, .7)]
    return remix(ep, scenes={2: nine, 3: drought, 4: {"base": "dark", "cam": [1, 500, 900], "els": web}}, alias={6: 1}, cams={6: [1.1, 500, 880], 0: [1.1, 500, 880], 5: [1.3, 500, 800]},
                 drop=("para", "num", "title", "q", "cap"), adds={1: fires}, line_adds={(2, 1): (dna, None)})


def arthur_m():
    """Arthur as one continuous take (see mural.py): the lights go out, one witness, three hundred years of silence, and the candidates."""
    remix, I = _mur()
    ep = arthur()
    dark = [I.dot(330, 1250, 26, I.AU, .6), I.box(450, 1215, 60, 70, "#c8743c", r=18, at=1.0), I.box(580, 1215, 90, 70, "none", "#cbbca8", 3, 4, 1.4)] + \
           [I.line([[570, 1220], [625, 1180], [680, 1220]], 1.4, "#cbbca8", 3, draw=False), I.box(280, 1160, 440, 160, "#120d0a", r=10, at=3.2, op=.75, dur=1.5)]
    witness = {"base": "dark", "floor": 1200, "cam": [1, 500, 900], "els": [I.person(200, 1200, 170, .2), I.box(240, 1090, 140, 20, "#5a4330", r=3, at=.3), I.box(260, 1060, 90, 30, "#e8dcc2", r=4, at=.5),
               I.label(200, 1260, "540", .6, I.BONE, 28),
               {"k": "poly", "p": [[480, 1200], [640, 900], [820, 1200]], "fill": "#4a5a3a", "c": "none", "w": 0, "in": 2.8, "fx": "rise"}, I.line([[640, 900], [640, 800]], 3.4, "#cbbca8", 3),
               {"k": "poly", "p": [[640, 800], [700, 820], [640, 840]], "fill": I.AMBER, "c": "none", "w": 0, "in": 3.5, "fx": "pop"},
               I.person(560, 640, 170, 6.0), I.label(560, 690, "Ambrosius", 6.2, I.GREEN, 30), I.label(780, 690, "Arthur", 7.2, I.LILAC, 30), I.strike(720, 700, 840, 660, 7.6)]}
    X = lambda y: 150 + 700 * (y - 480) / 380
    gap = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[130, 1100], [870, 1100]], .1, "#8c7152", 3), I.dot(X(500), 1100, 12, I.AMBER, .3), I.label(X(500), 1150, "Badon", .3, I.AMBER, 28),
           I.arrow([[X(500), 1040], [X(660), 960], [X(829), 1040]], .8, I.BONE, 3, dur=2.0), I.label(X(665), 930, "about 300 years", 1.6, I.BONE, 36, st="serif"),
           I.box(X(829) - 40, 1120, 80, 100, "#cdb58a", "#8a6a48", 2, 4, 3.0), I.label(X(829), 1260, "829", 3.0, I.BONE, 28)]}
    cand = {"base": "dark", "floor": 1300, "cam": [1, 500, 900], "els": [{"k": "poly", "p": [[300, 900], [500, 620], [700, 900]], "fill": "#4a5a3a", "c": "none", "w": 0, "in": .2},
            I.person(500, 640, 130, .4, c="#8a8378")] + I.question(500, 470, .8, 80) +
           [I.person(220, 1300, 190, 4.2), I.line([[200, 1105], [210, 1085], [220, 1100], [230, 1085], [240, 1105]], 4.3, I.AU, 4), I.label(220, 1350, "Riothamus", 4.4, I.BONE, 28),
            I.person(500, 1300, 190, 6.4), I.line([[480, 1100], [500, 1070], [520, 1100]], 6.5, I.RED, 6), I.label(500, 1350, "Artorius", 6.6, I.BONE, 28),
            I.person(780, 1300, 190, 8.6, c="#c9c1ee"), I.glow(780, 1200, 120, 8.6, .7), I.label(780, 1350, "a myth?", 8.8, I.LILAC, 28)]}
    return remix(ep, scenes={3: witness, 4: gap, 5: cand}, alias={6: 0}, cams={0: [1.2, 500, 960], 6: [1.25, 500, 980], 2: [1.3, 500, 800]},
                 drop=("para", "num", "title", "q", "cap"), beat_adds={1: (dark, None)})


def shroud_m():
    """The Shroud as one continuous take (see mural.py): three laboratories, one corner, one thread, and an image no one has reproduced."""
    remix, I = _mur()
    ep = shroud()
    labs = {"base": "dark", "cam": [1, 500, 900], "els": sum([[I.box(170 + 250 * k, 620, 90, 130, "rgba(159,208,255,.25)", I.BLUE, 3, 12, .4 + .9 * k), I.box(190 + 250 * k, 590, 50, 34, "#cbbca8", r=4, at=.4 + .9 * k),
                                                              I.label(215 + 250 * k, 800, n, .6 + .9 * k, I.BONE, 26), I.line([[215 + 250 * k, 840], [500, 1040]], 3.4, I.BLUE, 2, "inferred", .8)]
                                                             for k, n in enumerate(("Arizona", "Oxford", "Zurich"))], []) +
            [I.line([[130, 1100], [870, 1100]], 3.0, "#8c7152", 3), I.box(430, 1070, 140, 60, I.AMBER, r=8, at=4.4, fx="pop"), I.label(500, 1180, "1260–1390", 4.8, I.AMBER, 40, st="serif"),
             I.label(160, 1150, "0", 3.1, "#9a938a", 26), I.label(840, 1150, "2000", 3.1, "#9a938a", 26)]}
    corner = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(150, 560, 560, 760, "#d8c9a8", "#8a7a66", 2, 4, .2), I.box(640, 1200, 70, 120, "none", I.AMBER, 4, 2, 1.0),
              I.oval(600, 1260, 30, 18, "#b9a47c", "none", 0, .7, 1.6), I.oval(650, 1150, 26, 16, "#b9a47c", "none", 0, .7, 1.8)] +
             [I.box(740, 1200, 40, 120, c, r=2, at=4.6 + .2 * j) for j, c in enumerate(("#b0503a", "#c8743c", "#e8b87a"))] +
             [I.line([[760, 1180], [790, 800]], 7.0, "#e8dcc2", 2, dur=.8), I.arrow([[790, 800], [820, 640]], 8.0, I.LILAC, 3, "claimed", .6), I.label(820, 600, "1st century?", 8.3, I.LILAC, 30)]}
    fibers = [I.line([[220, 600 + 26 * j], [780, 610 + 26 * j + 8 * math.sin(j)]], .3 + .05 * j, "#d8c9a8", 5, dur=.6, curve=True) for j in range(14)]
    fibers += [I.ring(500, 780, 280, .2, "#8a939c", 6), I.line([[600, 1000], [680, 940], [760, 1030]], 3.0, I.GREEN, 8, dur=.4),
               I.box(420, 700, 120, 90, "none", I.LILAC, 3, 6, 4.0, style="claimed"), I.strike(410, 800, 550, 690, 4.6),
               I.box(320, 1150, 360, 200, "#d8c9a8", "#8a7a66", 2, 4, 7.4), I.oval(500, 1250, 50, 80, "none", "#b9a47c", 3, 1, 7.8)] + I.question(620, 1250, 8.6, 70)
    G = "#e8c878"
    gold = [I.box(90, 480, 820, 920, "none", G, 5, 18, .2, fx="draw", dur=2.0)]
    return remix(ep, scenes={2: labs, 4: corner, 5: {"base": "dark", "cam": [1, 500, 900], "els": fibers}}, alias={6: 0}, cams={6: [1.05, 500, 880], 3: [1.3, 500, 800]},
                 drop=("para", "num", "title", "q", "cap"), line_adds={(5, 1): (gold, None)})


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/myths-ledger.json)."""
    import recap
    return recap.recap(ledger, "myths-ledger", None)


def EPISODES():
    return [troy(), vinland(), knossos(), sea_peoples_m(), amazon(), arthur_m(), shroud_m(), ledger_recap()]
