"""File 16 · When the Sahara Was Green. The desert as an archive: a stone circle that watched the sun, a pharaoh's jewel
made of impact glass, a lost human lineage, the 'Martian god' of Tassili and the real scandal of its copies, how fast the
rains failed, a lakeside cemetery, painted swimmers in the driest place on Earth, and a kingdom that drank its fossil water.
Human remains are never shown (drawings and symbols only); living traditions are described, never rated; no modern politics."""
import math
from films import like, View
from scenes import timeline as _timeline, event, stat, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box

SERIES = "When the Sahara Was Green"
LAKE = "#4f7f96"
GRASS = "#7d9a5a"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def right(els, dx=14):
    for e in els:
        if e.get("k") == "label":
            e["a"] = "end"; e["x"] = e["x"] + dx
    return els


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


def dark(els, cam=(1, 500, 860)):
    return {"base": "dark", "cam": list(cam), "els": els}


def rnd(seed):
    s = [seed]
    def f():
        s[0] = (s[0] * 1103515245 + 12345) % 2147483648
        return s[0] / 2147483648
    return f


def sahara(pins, lon0, lon1, lat0, lat1, extra=(), cam=None, rect=(40, 330, 920, 900)):
    v = View(lon0, lon1, lat0, lat1, rect)
    return mapshot(v, pins=pins, extra=list(extra), cam=cam), v


def tag_label(v, lon, lat, t, c="#e8c894", a="middle"):
    x, y = v.p(lon, lat)
    return {"k": "label", "x": x, "y": y, "t": t, "st": "ital", "c": c, "a": a, "in": 1.0}


def ring_line(cx, cz, r, y=.05, n=36, c="#e8d3a8", w=2, style=None):
    e = {"t": "line", "p": [[cx + r * math.cos(2 * math.pi * k / n), y, cz + r * math.sin(2 * math.pi * k / n)] for k in range(n + 1)], "c": c, "w": w, "ground": True}
    if style:
        e["style"] = style
    return e


# ---------------------------------------------------------------- 16.01 The stones that watched the sky (Nabta Playa)
def circle_items(lines=True):
    it = [{"t": "slab", "x0": -6, "x1": 6, "z0": -5, "z1": 5, "y": 0, "c": "#c9a36c"}]
    for k in range(28):
        a = 2 * math.pi * k / 28
        it.append({"t": "cyl", "x": 2 * math.cos(a), "z": 2 * math.sin(a), "y": 0, "r": .12, "h": .18, "c": "#7a6248", "n": 6, "edge": "rgba(0,0,0,.2)"})
    for a in (90, 270, 30, 210):                              # four pairs of upright slabs: two on the north-south line
        r_ = math.radians(a)
        for d in (-.35, .35):
            x = 2 * math.cos(r_) - d * math.sin(r_); z = 2 * math.sin(r_) + d * math.cos(r_)
            it.append(box(x, z, 0, .22, .22, .55, "#8a6f52"))
    if lines:
        it += [{"t": "line", "p": [[0, .06, -4.8], [0, .06, 4.8]], "c": "#9fd0ff", "w": 2.4, "ground": True, "style": "inferred"},
               {"t": "line", "p": [[-4.2, .06, -2.4], [4.2, .06, 2.4]], "c": GOLD, "w": 2.4, "ground": True, "style": "inferred"}]
    return it


def nabta():
    c = circle_items() + [{"t": "person", "x": 3.6, "y": 0, "z": 2.8, "h": 1.7},
                          L_(0, .6, "the 'calendar circle' · c. 4 m across · schematic", GOLD, z=-2.2, dy=-30),
                          L_(0, 0, "sightlines: north–south, and midsummer sunrise", "#cfe6ff", z=3.2, dy=50)]
    s0 = iso(c, cam=[1, 500, 920], s=54, x=500, y=1020, az=-24, spin=1.0, el=.55, table=None)
    s1, v = sahara([("Nabta Playa", 30.7256, 22.508, {"c": GOLD}), ("Abu Simbel", 31.6258, 22.3372, {"c": SCAN, "ly": 32}),
                    ("Aswan · Nubia Museum", 32.8886, 24.0826, {"a": "end", "lx": -18, "ly": -24})], 27, 36, 19.5, 27.5)
    s1["els"] += [tag_label(v, 29.2, 25.2, "the Western Desert"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}]
    zoom = like(s0, cam=[1.5, 500, 1000], add=[{"k": "cap", "x": 500, "y": 1330, "t": "four pairs of upright stones", "in": .4}])
    s3 = stat("c. 4800", "BCE", "the circle's date: some 1,800 years before the first phase of Stonehenge", "Malville et al. 1998, Nature")
    tl, ax = timeline(-9000, -2500, [(-9000, "9000 BCE"), (-7000, "7000"), (-5000, "5000"), (-3000, "3000")], "A lake, then a desert")
    tl["els"] += [{"k": "band", "x0": ax.x(-8500), "x1": ax.x(-3600), "y": 745, "h": 14, "c": LAKE, "t": "seasonal lake, herders", "in": .3}] + \
                 event(ax, -5500, "cattle burials", row=2, c=OCHRE, i=.6) + event(ax, -4800, "the circle", row=1, c=GOLD, i=.9) + \
                 right(event(ax, -3000, "Stonehenge begins", row=3, c=SCAN, i=1.2))
    s4 = tl
    s5 = dark(grp("likely", "#8fd9b0", ["north–south and midsummer lines", "a ceremonial centre for herders"], y=440, size=28) +
              grp("overreach", "#ff8a7a", ["a precise calendar", "star maps and star distances"], y=820, size=28))
    s6 = like(s0, cam=[1.12, 500, 960])
    shots = [s0, s1, zoom, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:NABTA PLAYA · EGYPT][sfx:boom][act:hushed, wonder]About seven thousand years ago, herders in the Egyptian Sahara set up a circle of ^stones.",
                      "[d:tension][cam:1.12|0|0][act:the question, leaning in][tune:rise]Was it the world's first ^observatory?"], cut=False),
        B("world", 1, ["[d:calm][k:NABTA PLAYA][act:plain, orienting]Nabta Playa lies about a hundred kilometres west of Abu ^Simbel. [act:steady, factual]Back then, summer rains filled a seasonal ^lake, and herders came with their ^cattle."]),
        B("collision", 2, ["[d:build][k:THE CIRCLE][act:building, precise]The circle is only about four metres ^across, with four pairs of upright ^stones. [act:the claim, intrigued]Two gaps line up north to ^south. [act:the second one]Another faces the midsummer ^sunrise."]),
        B("cost", 3, ["[d:build][k:THE DATE][act:the reveal, strong]It dates to about {4800|forty-eight hundred} BCE. [act:context, wonder]Some eighteen centuries before the first phase of ^Stonehenge.",
                      "[d:build][go:4|0][act:vivid]Nearby, cattle were buried in clay-lined ^chambers, and stones nearly three metres tall were dragged into ^lines."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:fair, the challenger's case]Some go further: star alignments, even a map of ^Orion. [act:the reply, precise]But those dates fall about fifteen hundred years before the ^stones, and some stones may have ^moved.",
                          "[d:build][act:plain, a small smile][tune:fall]Even the excavators say calendar circle may be the wrong ^name."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]The world's first ^observatory? [act:the verdict, measured][tune:fall]*Mixed ^record@noun*. [act:fair]A real ritual landscape, probably watching the ^sun.",
                     "[d:tension][p:0.93][act:the last word, warm][tune:fall]The star maps are a ^stretch."]),
    ]
    return EP("nabta-playa", "16.01", "Nabta Playa: The Stones That Watched the Sky", "nabta-playa", "mixed", "Was Nabta Playa's stone circle an astronomical observatory, 7,000 years ago?", "The first *observatory*?", beats, shots,
              "Malville et al. 1998 (doi:10.1038/33131) · Wendorf & Schild 1998 (doi:10.1006/jaar.1998.0319) · Wendorf & Malville 2001 (doi:10.1007/978-1-4615-0653-9) · Malville 2015 (doi:10.1007/978-1-4614-6141-8_101) · Brophy & Rosen 2005 · Belmonte 2010 (ICOMOS/IAU)",
              "A small stone circle in the Egyptian Sahara, about 7,000 years old, with gaps facing north and the midsummer sunrise. What it probably was, and where the observatory claims overreach.",
              ["#Egypt", "#Sahara", "#Archaeoastronomy", "#Archaeology", "#GreenSahara"])


# ---------------------------------------------------------------- 16.02 Tutankhamun's sky-glass (Libyan Desert Glass)
def scarab(cx, cy, s=1.0, i=.3):
    body = [[cx + 110 * s * math.cos(2 * math.pi * k / 28), cy + 150 * s * math.sin(2 * math.pi * k / 28)] for k in range(28)]
    head = [[cx + 60 * s * math.cos(2 * math.pi * k / 18), cy - 170 * s + 36 * s * math.sin(2 * math.pi * k / 18)] for k in range(18)]
    return [{"k": "poly", "p": body, "fill": "#d9df8e", "c": "#f1cf6a", "w": 5, "in": i},
            {"k": "poly", "p": head, "fill": "#cdd27f", "c": "#f1cf6a", "w": 4, "in": i + .1},
            {"k": "line", "p": [[cx, cy - 130 * s], [cx, cy + 140 * s]], "c": "#a8ad5a", "w": 3, "in": i + .3},
            {"k": "line", "p": [[cx - 100 * s, cy - 40 * s], [cx + 100 * s, cy - 40 * s]], "c": "#a8ad5a", "w": 3, "in": i + .4}]


def glass():
    frame = [{"k": "poly", "p": [[240, 700], [760, 700], [820, 1000], [700, 1220], [300, 1220], [180, 1000]], "fill": "#3a2f22", "c": "#e8b84a", "w": 6, "in": .1},
             {"k": "line", "p": [[180, 1000], [110, 900]], "c": "#e8b84a", "w": 10, "in": .2}, {"k": "line", "p": [[820, 1000], [890, 900]], "c": "#e8b84a", "w": 10, "in": .2}]
    s0 = dark(frame + scarab(500, 980, .82) + [{"k": "label", "x": 500, "y": 1320, "t": "the scarab at the heart of a pectoral · redrawn", "c": AMBER, "in": 1.2}])
    s1, v = sahara([("the glass field (approx.)", 25.5, 25.4, {"c": GOLD}), ("Grand Egyptian Museum", 31.1187, 29.9942, {"c": SCAN, "a": "end", "lx": -18, "ly": -24})], 22, 34, 21, 32.5)
    s1["els"] += [tag_label(v, 26.2, 27.4, "the Great Sand Sea"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}]
    s2 = stat("c. 29", "million years", "the glass's age, by fission tracks. It is 96.5–99% pure silica", "LPI 2003 · Cavosie & Koeberl 2019")
    ground = {"k": "rect", "x": 0, "y": 1040, "w": 1000, "h": 400, "fill": "#8a7050", "c": "none", "sw": 0, "in": -1}
    bowl = {"k": "poly", "p": [[80, 1040], [140, 1100], [250, 1130], [360, 1100], [420, 1040]], "fill": "#5a4632", "c": "#e9dccb", "w": 2, "curve": True, "in": .4}
    s3 = dark([ground, bowl, {"k": "arrow", "p": [[120, 640], [200, 820], [250, 1000]], "c": AMBER, "w": 3, "in": .3, "fx": "draw"},
               {"k": "circle", "x": 750, "y": 820, "r": 90, "fill": "#f0b060", "c": "#ffe0a0", "w": 2, "op": .85, "in": .8},
               {"k": "arrow", "p": [[640, 600], [700, 700], [735, 760]], "c": AMBER, "w": 3, "in": .6, "fx": "draw"},
               {"k": "line", "p": [[640, 1030], [860, 1030]], "c": "#ffe0a0", "w": 6, "op": .8, "in": 1.1},
               {"k": "label", "x": 250, "y": 1210, "t": "an impact crater?", "c": "#e9dccb", "in": .5},
               {"k": "label", "x": 750, "y": 1210, "t": "or an airburst?", "c": "#e9dccb", "in": 1.0},
               {"k": "cap", "x": 500, "y": 560, "t": "two ways to melt a desert · schematic", "in": .1},
               {"k": "label", "x": 500, "y": 1300, "t": "no source crater confirmed yet", "st": "small", "c": "#b9aa97", "in": 1.4}])
    tl, ax = timeline(1900, 2030, [(1900, "1900"), (1950, "1950"), (2000, "2000")], "The scarab, re-read")
    tl["els"] += event(ax, 1922, "Carter: 'chalcedony'", row=1, c=AMBER, i=.3) + event(ax, 1932, "the glass field studied", row=2, c=SCAN, i=.6) + \
                 event(ax, 1998, "re-identified: desert glass", row=3, c=GOLD, i=.9) + right(event(ax, 2019, "impact mineral found", row=1, c=RED, i=1.2))
    s4 = tl
    s5 = dark(grp("signs of an impact", "#8fd9b0", ["a mineral made only by impacts", "melt above 2,750 °C", "shocked quartz in the bedrock"]))
    s6 = like(s0, cam=[1.1, 500, 940])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:TUTANKHAMUN][sfx:boom][act:hushed, intrigued]On Tutankhamun's chest sits a yellow-green ^scarab.",
                      "[d:tension][cam:1.12|0|0][act:the twist, leaning in][tune:fall]It's made of glass, melted by something from ^space."], cut=False),
        B("world", 1, ["[d:calm][k:THE GREAT SAND SEA][act:plain, orienting]The glass lies scattered among the dunes near the border of Egypt and ^Libya.",
                       "[d:build][go:2|0][act:steady, precise]It is almost pure ^silica, and about twenty-nine million years ^old. [act:light, a small smile]Stone Age people made ^tools from it."]),
        B("collision", 4, ["[d:build][k:THE SCARAB][act:storytelling]In {1922|nineteen twenty-two}, Howard Carter listed the scarab as ^chalcedony, a common stone. [act:the reveal, delighted]In the {1990s|nineteen nineties}, a mineralogist looked again: it was desert@noun ^glass."]),
        B("cost", 5, ["[d:build][k:THE IMPACT][act:building, precise]Tiny crystals in the glass keep traces of a mineral that forms only in ^impacts. [act:vivid]The melt passed two thousand seven hundred and fifty ^degrees."]),
        B("reversal", 3, ["[d:reveal][k:THE CATCH][act:the crux, curious][tune:fall]But where's the ^crater? [act:fair, the challenger's case]Some argue for an ^airburst: a blast in the sky that melted the sand without leaving a ^hole.",
                          "[d:build][act:plain]One candidate crater, ^Kebira, failed the ^tests."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A pharaoh's jewel made by a cosmic ^impact? [act:the verdict, measured][tune:fall]*Strong ^evidence*.",
                     "[d:tension][p:0.93][act:the last word, a small smile][tune:fall]The crater is still ^missing."]),
    ]
    return EP("desert-glass", "16.02", "Tutankhamun's Sky-Glass", "desert-glass", "strong", "Is the scarab on Tutankhamun's pectoral made of glass melted by a cosmic impact?", "A scarab made by a *cosmic* blast.", beats, shots,
              "Cavosie & Koeberl 2019 (doi:10.1130/G45974.1) · Kovaleva et al. 2019 (doi:10.1111/maps.13250) · Kovaleva & Helmy 2023 (doi:10.2138/am-2022-8759) · Boslough & Crawford 2008 (doi:10.1016/j.ijimpeng.2008.07.053) · de Michele 1998",
              "The yellow-green scarab on Tutankhamun's pectoral is Libyan Desert Glass, melted about 29 million years ago by a cosmic impact or airburst. What the glass shows, and the crater nobody has found.",
              ["#Tutankhamun", "#Egypt", "#Meteorite", "#Science", "#GreenSahara"])


# ---------------------------------------------------------------- 16.03 The ghost people of the green Sahara (Takarkori)
def shelter(i=.1):
    return [{"k": "rect", "x": 0, "y": 1080, "w": 1000, "h": 400, "fill": GRASS, "c": "none", "sw": 0, "in": -1},
            {"k": "poly", "p": [[0, 560], [980, 560], [1000, 700], [640, 760], [420, 820], [300, 930], [260, 1080], [0, 1080]], "fill": "#5a4636", "c": "#a88b66", "w": 2, "in": -1},
            {"k": "poly", "p": [[600, 1130], [900, 1110], [960, 1180], [700, 1210], [560, 1180]], "fill": LAKE, "c": "#9fd0ff", "w": 1.5, "curve": True, "in": i + .3}] + \
           [{"k": "line", "p": [[x, 1090], [x + 6, 1066]], "c": "#a9c47c", "w": 2, "in": i + .5} for x in range(330, 980, 38)]


def takarkori():
    s0 = dark(shelter() + [{"k": "label", "x": 500, "y": 1320, "t": "Takarkori rock shelter, 7,000 years ago · schematic", "c": AMBER, "in": 1.2}])
    s1, v = sahara([("Takarkori · Libya", 10.333, 24.883, {"c": GOLD}), ("Taforalt · Morocco", -2.40, 34.81, {"c": SCAN})], -8, 20, 18, 37)
    s1["els"] += [{"k": "line", "p": [v.p(10.333, 24.883), v.p(-2.4, 34.81)], "c": AMBER, "w": 2, "op": .7, "in": 1.2, "dash": "8 8"},
                  tag_label(v, 5, 26.5, "the Sahara"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}]
    s2 = stat("c. 50,000", "years", "since their lineage split from sub-Saharan lineages. It then stayed apart", "Salem et al. 2025, Nature")
    tree = [{"k": "line", "p": [[500, 1240], [500, 1080]], "c": "#e9dccb", "w": 4, "in": .1},
            {"k": "line", "p": [[500, 1080], [240, 640]], "c": "#8c7152", "w": 4, "in": .3}, {"k": "line", "p": [[500, 1080], [620, 900]], "c": "#8c7152", "w": 4, "in": .4},
            {"k": "line", "p": [[620, 900], [820, 640]], "c": "#8c7152", "w": 4, "in": .5}, {"k": "line", "p": [[620, 900], [560, 640]], "c": GOLD, "w": 6, "in": .8},
            {"k": "label", "x": 240, "y": 610, "t": "sub-Saharan Africans", "c": "#e9dccb", "in": .5},
            {"k": "label", "x": 850, "y": 610, "t": "people outside Africa", "c": "#e9dccb", "a": "end", "in": .7},
            {"k": "label", "x": 560, "y": 700, "t": "Takarkori", "c": GOLD, "a": "end", "in": 1.0},
            {"k": "label", "x": 580, "y": 760, "t": "Taforalt", "c": SCAN, "a": "start", "in": 1.2},
            {"k": "label", "x": 660, "y": 930, "t": "split, c. 50,000 years ago", "st": "small", "c": "#cbbca8", "a": "start", "in": 1.0},
            {"k": "cap", "x": 500, "y": 520, "t": "a family tree of lineages · simplified", "in": .1}]
    s3 = dark(tree)
    tl, ax = timeline(-6000, -3000, [(-6000, "6000 BCE"), (-5000, "5000"), (-4000, "4000"), (-3000, "3000")], "Herders in a green Sahara")
    tl["els"] += event(ax, -5000, "the first woman", row=1, c=GOLD, i=.3) + event(ax, -4450, "the second", row=2, c=GOLD, i=.6) + \
                 [{"k": "band", "x0": ax.x(-5000), "x1": ax.x(-4000), "y": 745, "h": 14, "c": "#e9dccb", "t": "milk fats in pots", "in": .9}] + \
                 right(event(ax, -3500, "the rains fail", row=3, c=RED, i=1.2))
    s4 = tl
    s5 = dark(grp("what it suggests", "#8fd9b0", ["herders who were mostly local", "cattle spread as an idea"], y=440, size=28) +
              grp("the caveat", "#9fd0ff", ["two people, one site"], y=820, size=28))
    s6 = like(s0, cam=[1.12, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE ACACUS · LIBYA][sfx:boom][act:hushed, tender]Seven thousand years ago, two women died in a green ^Sahara.",
                      "[d:tension][cam:1.12|0|0][act:the reveal, leaning in][tune:fall]Their DNA belongs to a human lineage no one ^knew."], cut=False),
        B("world", 1, ["[d:calm][k:TAKARKORI][act:plain, orienting]A rock shelter in the mountains of south-west ^Libya. [act:steady]Herders lived here with cattle, beside lakes and ^grassland.",
                       "[d:build][act:gentle, careful]The desert@noun air mummified the two women ^naturally."]),
        B("collision", 2, ["[d:build][k:THE GENOMES][act:the reveal, precise]In {2025|twenty twenty-five}, their genomes were ^read@past. [act:building, amazed]Their line split from other African lineages about fifty thousand years ^ago, and then stayed ^apart.",
                           "[d:build][go:3|0][act:connecting it, delighted]Their closest known relatives lived in ^Morocco, fifteen thousand years ^earlier."]),
        B("cost", 4, ["[d:build][k:THE HERDERS][act:the point, clear]So the green Sahara's herders were mostly ^local. [act:thoughtful]Cattle and milk arrived as ^ideas, not with a wave of ^newcomers. [act:light, a small smile]Their pots hold Africa's earliest known milk ^fats."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:fair, a caveat]But two people from one site are not a whole ^people. [act:precise]Teeth and culture elsewhere hint at more ^movement."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]A lost lineage in the green ^Sahara? [act:the verdict, measured][tune:fall]*Strong ^evidence*.",
                     "[d:tension][p:0.93][act:the last word, inviting][tune:fall]Now we need more ^genomes."]),
    ]
    return EP("takarkori", "16.03", "The Ghost Lineage of the Green Sahara", "takarkori", "strong", "Do the first Green Sahara genomes reveal a North African lineage that stayed apart for tens of thousands of years?", "A lineage no one *knew*.", beats, shots,
              "Salem, van de Loosdrecht et al. 2025 (doi:10.1038/s41586-025-08793-7) · Dunne et al. 2012 (doi:10.1038/nature11186) · Di Vincenzo et al. 2015",
              "Two women who died in a green Sahara about 7,000 years ago carry a North African lineage that split off some 50,000 years ago. What their genomes say about the herders, and what two people can't tell us.",
              ["#Sahara", "#AncientDNA", "#Libya", "#Prehistory", "#GreenSahara"])


# ---------------------------------------------------------------- 16.04 The great Martian god (Tassili n'Ajjer)
def roundhead(cx, base, h, c="#d8c7ae", fill="#b0643c", op=1.0, i=.3):
    hr = h * .15
    body = [[cx - h * .09, base - h * .72], [cx + h * .09, base - h * .72], [cx + h * .12, base - h * .42], [cx + h * .07, base - h * .02],
            [cx + h * .02, base - h * .02], [cx, base - h * .3], [cx - h * .02, base - h * .02], [cx - h * .07, base - h * .02], [cx - h * .12, base - h * .42]]
    arm = lambda sx: {"k": "line", "p": [[cx + sx * h * .08, base - h * .66], [cx + sx * h * .24, base - h * .78], [cx + sx * h * .3, base - h * .95]],
                      "c": fill, "w": h * .045, "op": op, "curve": True, "in": i}
    return [arm(-1), arm(1), {"k": "poly", "p": body, "fill": fill, "c": c, "w": 1.5, "op": op, "curve": True, "in": i},
            {"k": "circle", "x": cx, "y": base - h * .72 - hr * .9, "r": hr, "fill": fill, "c": c, "w": 1.5, "op": op, "in": i + .1}]


def tassili():
    wall = {"k": "rect", "x": 0, "y": 520, "w": 1000, "h": 900, "fill": "#7a5a42", "c": "none", "sw": 0, "in": -1}
    s0 = dark([wall] + roundhead(440, 1240, 640, i=.4) + [{"k": "person", "x": 800, "y": 1240, "h": 150, "in": .8},
               {"k": "label", "x": 500, "y": 1320, "t": "a 'Round Head' figure, up to 5 m tall · redrawn", "c": AMBER, "in": 1.2}])
    s1, v = sahara([("Djanet", 9.485, 24.555, {"c": SCAN, "a": "end", "lx": -18, "ly": 30}), ("Tassili n'Ajjer", 9.6, 24.9, {"c": GOLD})], 0, 16, 18, 32)
    s1["els"] += [tag_label(v, 4.5, 28.5, "Algeria"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}]
    s2 = stat("15,000+", "images", "painted and engraved across the plateau. UNESCO World Heritage since 1982", "UNESCO · TARA")
    s3 = dark(roundhead(270, 1150, 420, fill="#8a5a40", op=.35, i=.2) + roundhead(730, 1150, 420, fill="#c4582c", c="#fff0d8", i=.5) +
              [{"k": "label", "x": 270, "y": 1230, "t": "the painting today", "c": "#e9dccb", "in": .4},
               {"k": "label", "x": 730, "y": 1230, "t": "a bold 1950s copy", "c": "#e9dccb", "in": .7},
               {"k": "cap", "x": 500, "y": 560, "t": "wetted to look brighter, then faded · schematic", "in": .1}] +
              [{"k": "circle", "x": 250 + k * 18, "y": 700 + (k % 3) * 60, "r": 6, "fill": "#9fd0ff", "c": "none", "w": 0, "op": .7, "in": 1.0 + k * .08} for k in range(6)])
    tl, ax = timeline(1950, 2010, [(1950, "1950"), (1970, "1970"), (1990, "1990"), (2010, "2010")], "How a painting became a spaceman")
    tl["els"] += event(ax, 1956, "Lhote's copying expedition", row=1, c=AMBER, i=.3) + event(ax, 1968, "'ancient astronauts'", row=2, c=RED, i=.6) + \
                 event(ax, 1982, "UNESCO listing", row=3, c=SCAN, i=.9) + right(event(ax, 2000, "'systematic vandalism'", row=1, c=GOLD, i=1.2))
    s4 = tl
    s5 = dark(grp("what's real", "#8fd9b0", ["an early style, c. 9,500–7,500 years ago", "masks, body paint, or spirit beings"], y=440, size=28) +
              grp("the scandal", "#ff8a7a", ["paintings wetted to brighten them", "some published works faked"], y=820, size=28))
    s6 = like(s0, cam=[1.12, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:TASSILI · ALGERIA][sfx:boom][act:playful, intrigued]In the {1950s|nineteen fifties}, an explorer nicknamed a painted giant in the Sahara the great Martian ^god.",
                      "[d:tension][cam:1.12|0|0][act:dry, a small smile][tune:fall]Some people took him ^literally."], cut=False),
        B("world", 1, ["[d:calm][k:TASSILI N'AJJER][act:plain, orienting]Tassili n'Ajjer, a sandstone plateau in south-east ^Algeria.",
                       "[d:build][go:2|0][act:quietly amazed]It holds more than fifteen thousand ancient ^images."]),
        B("collision", 4, ["[d:build][k:THE CLAIM][act:presenting it, fair]The figures called Round Heads have smooth, featureless ^heads. [act:the challenger's case, fair]By {1968|nineteen sixty-eight}, ancient astronaut writers saw ^helmets. [act:plain]And they really are unlike later ^art."]),
        B("cost", 3, ["[d:build][k:THE REAL SCANDAL][act:grave, measured]The real damage came from the ^copyists. [act:precise]To brighten the paintings, the team wetted and sponged ^them, and they faded ^faster.",
                      "[d:build][act:the sting, quiet][tune:fall]Some published pictures were later said to be ^fakes."]),
        B("reversal", 5, ["[d:reveal][k:WHAT THEY ARE][act:fair, clear]Archaeologists date the Round Heads, indirectly, to about nine and a half to seven and a half thousand years ^ago. [act:thoughtful]The blank heads look like a ^convention: masks, body paint, or spirit ^beings.",
                          "[d:build][act:respectful, even]Tuareg tradition credits some paintings to spirits, a living ^belief."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Astronauts on the ^rocks? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:warm, the other half]The art is extraordinary on its ^own.",
                     "[d:tension][p:0.93][act:the last word, quiet][tune:fall]It deserves better ^copies."]),
    ]
    return EP("tassili", "16.04", "Tassili: The Great Martian God", "tassili", "debunked", "Do the Round Head paintings of Tassili n'Ajjer show ancient astronauts?", "The great *Martian* god?", beats, shots,
              "Keenan 2000 (doi:10.1017/S0003598X00059287) · Keenan 2002 (doi:10.1179/pua.2002.2.3.131) · Mercier et al. 2012 (doi:10.1016/j.quageo.2011.11.010) · Le Quellec 2009, Des Martiens au Sahara · TARA, Rock Art of the Tassili n Ajjer",
              "A 1950s explorer joked that a giant painted figure in the Sahara was the 'great Martian god', and ancient-astronaut writers took him at his word. What the Round Heads are, and the real scandal of how they were copied.",
              ["#RockArt", "#Algeria", "#AncientAstronauts", "#MythBusting", "#GreenSahara"])


# ---------------------------------------------------------------- 16.05 The day the Sahara switched off (the end of the Green Sahara)
MEGA = [(12.0, 16.2), (12.6, 17.7), (15.4, 18.5), (18.6, 18.0), (19.6, 16.2), (19.2, 13.6), (17.2, 11.6), (14.6, 10.9), (12.8, 11.9), (11.9, 13.9)]
CHAD = [(13.3, 13.0), (14.0, 13.7), (14.5, 13.4), (14.3, 12.7), (13.7, 12.6)]


def switchoff():
    s0, v = sahara([("Lake Chad today", 14.2, 13.2, {"c": SCAN, "ly": 34}), ("Bodélé", 17.8, 16.8, {"c": GOLD})], 6, 26, 6, 24, rect=(40, 520, 920, 760))
    s0["els"] += [{"k": "poly", "p": [v.p(a, b) for a, b in MEGA], "fill": "rgba(79,127,150,.55)", "c": "#9fd0ff", "w": 2, "curve": True, "in": .3},
                  {"k": "poly", "p": [v.p(a, b) for a, b in CHAD], "fill": LAKE, "c": "#9fd0ff", "w": 1.5, "in": .1},
                  {"k": "label", "x": 500, "y": 1330, "t": "Lake Mega-Chad · c. 360,000 km² · schematic", "c": AMBER, "in": 1.2}]
    s1, w = sahara([("Mauritania dust core", -18.58, 20.75, {"c": GOLD, "ly": -24}), ("Lake Yoa · Chad", 20.52, 19.05, {"c": SCAN, "a": "end", "lx": -18, "ly": -24}),
                    ("the Richat", -11.4, 21.12, {"ly": 34})], -20, 26, 8, 32)
    s1["els"] += [tag_label(w, 5, 24, "the Sahara"), {"k": "scale", "x": 80, "y": 1240, "w": w.km(500), "t": "500 km"}]
    s2 = stat("c. 10×", "today's rain", "at the height of the African Humid Period, about 11,000 to 5,000 years ago", "Tierney et al. 2017")
    X0, X1, Y0 = 180, 840, 1000
    cliff = [[X0, Y0], [X0 + 380, Y0], [X0 + 400, Y0 - 250], [X1, Y0 - 260]]
    ramp = [[X0, Y0 + 200], [X1, Y0 + 40]]
    s3 = dark([{"k": "line", "p": cliff, "c": RED, "w": 4, "in": .3, "fx": "draw"}, {"k": "line", "p": ramp, "c": GRASS, "w": 4, "in": .9, "fx": "draw"},
               {"k": "label", "x": X1, "y": Y0 - 290, "t": "dust off Mauritania: a cliff", "c": RED, "a": "end", "in": .8},
               {"k": "label", "x": X1, "y": Y0 - 20, "t": "Lake Yoa, Chad: a ramp", "c": GRASS, "a": "end", "in": 1.4},
               {"k": "line", "p": [[X0, 1240], [X1, 1240]], "c": "#8c7152", "w": 2, "in": .1},
               {"k": "label", "x": X0, "y": 1280, "t": "8,000 years ago", "st": "small", "c": "#cbbca8", "in": .2},
               {"k": "label", "x": X1, "y": 1280, "t": "3,000", "st": "small", "c": "#cbbca8", "a": "end", "in": .2},
               {"k": "cap", "x": 500, "y": 560, "t": "two records of drying · schematic", "in": .1}])
    tl, ax = timeline(-11000, 0, [(-11000, "11,000 years ago"), (-7000, "7,000"), (-3000, "3,000"), (0, "today")], "The green, then the dust")
    tl["els"] += [{"k": "band", "x0": ax.x(-11000), "x1": ax.x(-5000), "y": 745, "h": 16, "c": GRASS, "t": "the Green Sahara", "in": .3}] + \
                 event(ax, -5500, "dust jumps", row=1, c=RED, i=.6) + event(ax, -5000, "Mega-Chad falls", row=2, c=SCAN, i=.9) + \
                 right(event(ax, -1000, "the Bodélé dries", row=1, c=GOLD, i=1.2))
    s4 = tl
    s5 = dark(grp("no support", "#ff8a7a", ["a sudden catastrophe"], y=460, size=28) +
              grp("still debated", "#9fd0ff", ["did herders speed the end,", "or slow it down?"], y=780, size=28))
    s6 = like(s0, cam=[1.12, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE GREEN SAHARA][sfx:boom][act:hushed, wonder]Where the Sahara is now, there was once a lake about the size of the Caspian ^Sea.",
                      "[d:tension][cam:1.12|0|0][act:the question, leaning in]Then the rain ^stopped. [act:curious][tune:rise]Fast, or ^slow?"], cut=False),
        B("world", 1, ["[d:calm][k:THE HUMID PERIOD][act:plain, explaining]From about eleven thousand to five thousand years ago, a slow wobble in Earth's orbit strengthened the ^monsoon.",
                       "[d:build][go:2|0][act:vivid]Rain fell at about ten times today's ^rate."]),
        B("collision", 3, ["[d:build][k:TWO RECORDS][act:building, precise]Dust off the coast of Mauritania jumps about five and a half thousand years ago, within decades to ^centuries. [act:the counterpoint]But a lake in Chad records@verb a slow change, over thousands of ^years."]),
        B("cost", 4, ["[d:build][k:THE END][act:grave, measured]Lake Mega-Chad shrank fast, about five thousand years ^ago. [act:the twist, wonder]Its last basin, the ^Bodélé, dried only about a thousand years ago, and is now Earth's biggest source of ^dust."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:fair, weighing][tune:rise]So, a ^collapse? [act:clear]The best answer: sudden in some places, gradual in ^others. [act:dry, light]A catastrophe that ended it all? No evidence at ^all.",
                          "[d:build][act:curious, even]Some argue herders sped up the end. One model says they ^slowed it."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]The Sahara switched off ^overnight? [act:the verdict, measured][tune:fall]*Mixed ^record@noun*. [act:fair]The green Sahara itself is well ^established.",
                     "[d:tension][p:0.93][act:the last word, warm][tune:fall]How fast it faded depends on where you ^stand."]),
    ]
    return EP("green-sahara", "16.05", "The Day the Sahara Switched Off", "green-sahara", "mixed", "Did the Green Sahara end abruptly, within a few generations?", "When the Sahara *switched off*.", beats, shots,
              "deMenocal et al. 2000 (doi:10.1016/S0277-3791(99)00081-5) · Kröpelin et al. 2008 (doi:10.1126/science.1154913) · Shanahan et al. 2015 (doi:10.1038/ngeo2329) · Armitage et al. 2015 (doi:10.1073/pnas.1417655112) · Tierney et al. 2017 (doi:10.1126/sciadv.1601503) · Wright 2017 (doi:10.3389/feart.2017.00004) · Brierley et al. 2018 (doi:10.1038/s41467-018-06321-y)",
              "A lake the size of the Caspian Sea once filled the southern Sahara. Then the monsoon weakened. Did the green Sahara collapse in a few generations, or fade over thousands of years?",
              ["#Sahara", "#Climate", "#Prehistory", "#Science", "#GreenSahara"])


# ---------------------------------------------------------------- 16.06 The embrace at Gobero
def gobero():
    g = [{"t": "slab", "x0": -40, "x1": 40, "z0": -28, "z1": 28, "y": 0, "c": "#cfae78"},
         {"t": "flat", "pts": [[20 + 18 * math.cos(2 * math.pi * k / 24), -6 + 14 * math.sin(2 * math.pi * k / 24)] for k in range(24)], "y": .04, "c": LAKE}]
    r = rnd(4)
    for k in range(34):
        x, z = -34 + r() * 36, -22 + r() * 44
        g.append({"t": "flat", "pts": [[x - 1.1, z - .6], [x + 1.1, z - .6], [x + 1.1, z + .6], [x - 1.1, z + .6]], "y": .05, "c": "#8a6a44"})
    for k in range(9):
        a = 2 * math.pi * k / 9
        g.append({"t": "cyl", "x": -6 + 1.4 * math.cos(a), "z": 6 + 1.0 * math.sin(a), "y": 0, "r": .35, "h": .3, "c": ["#e8a0b8", "#f0d060", "#ffffff"][k % 3], "n": 8, "edge": "rgba(0,0,0,0)"})
    g += [L_(-16, 0, "graves beside a vanished lake · schematic", GOLD, z=-22, dy=-24), L_(-6, 0, "flowers in one grave", "#cfe6ff", z=8, dy=46),
          L_(20, 0, "the lake", "#9fd0ff", z=-6, dy=0)]
    s0 = iso(g, cam=[1, 500, 920], s=7.6, x=500, y=1010, az=-22, spin=1.0, el=.55, table=None)
    s1, v = sahara([("Gobero", 9.52, 17.08, {"c": GOLD}), ("Agadez", 7.99, 16.97, {"c": SCAN, "a": "end", "lx": -18})], 2, 16, 10, 24)
    s1["els"] += [tag_label(v, 11.5, 19.5, "the Ténéré"), tag_label(v, 8.5, 21.8, "Niger", c="#cbbca8"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}]
    s2 = stat("c. 200", "burials", "the Sahara's largest early Holocene cemetery, beside a lake up to about 3 km wide", "Sereno et al. 2008, PLoS ONE")
    pit = {"k": "poly", "p": [[260, 760], [740, 760], [760, 1060], [240, 1060]], "fill": "#6a5238", "c": "#e9dccb", "w": 2, "in": .1}
    rr = rnd(12)
    fl = [{"k": "circle", "x": 290 + rr() * 420, "y": 790 + rr() * 250, "r": 10, "fill": ["#e8a0b8", "#f0d060", "#ffffff"][k % 3], "c": "none", "w": 0, "in": .4 + k * .05} for k in range(16)]
    s3 = dark([pit] + fl + [{"k": "cap", "x": 500, "y": 600, "t": "the triple burial · c. 3300 BCE", "in": .1},
                            {"k": "label", "x": 500, "y": 1150, "t": "a woman and two children, together", "st": "serif", "size": 30, "c": "#e9dccb", "in": 1.2},
                            {"k": "label", "x": 500, "y": 1210, "t": "pollen suggests flowers · no remains shown", "st": "small", "c": "#b9aa97", "in": 1.5}])
    tl, ax = timeline(-8000, -2000, [(-8000, "8000 BCE"), (-6000, "6000"), (-4000, "4000"), (-2000, "2000")], "Two phases, one lake")
    tl["els"] += [{"k": "band", "x0": ax.x(-7700), "x1": ax.x(-6200), "y": 745, "h": 16, "c": SCAN, "t": "Kiffian", "in": .3},
                  {"k": "band", "x0": ax.x(-6200), "x1": ax.x(-5200), "y": 745, "h": 16, "c": "#6f6a62", "t": "dry", "in": .6},
                  {"k": "band", "x0": ax.x(-5200), "x1": ax.x(-2500), "y": 745, "h": 16, "c": GOLD, "t": "Tenerian", "in": .9}] + \
                 event(ax, -3300, "the embrace", row=2, c="#e8a0b8", i=1.2)
    s4 = tl
    s5 = dark(grp("2008", "#e8b87a", ["two peoples, a thousand years apart"], y=460, size=28) +
              grp("2025", "#8fd9b0", ["their teeth: hard to tell apart", "perhaps one people all along"], y=760, size=28))
    s6 = like(s0, cam=[1.14, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE TÉNÉRÉ · NIGER][sfx:boom][act:hushed, tender]About five thousand three hundred years ago, in what is now a desert@noun, a woman and two children were buried in an ^embrace.",
                      "[d:tension][cam:1.12|0|0][act:quiet, wonder][tune:fall]On a bed of ^flowers."], cut=False),
        B("world", 1, ["[d:calm][k:GOBERO][act:plain, orienting]Gobero, in ^Niger. [act:storytelling]In {2000|two thousand}, a team led by Paul ^Sereno found a cemetery beside a vanished ^lake.",
                       "[d:build][go:2|0][act:impressed]About two hundred ^burials, with fish, hippo and crocodile bones ^nearby."]),
        B("collision", 4, ["[d:build][k:TWO PEOPLES?][act:building, precise]The first group, called ^Kiffian, fished with harpoons from about {7700|seventy-seven hundred} BCE. [act:grave]Then a long dry spell, and the lake ^emptied.",
                           "[d:build][act:the change]When the water came back, the burials looked ^different: the ^Tenerians, with ^cattle."]),
        B("cost", 3, ["[d:build][k:THE EMBRACE][act:tender, careful]The embrace belongs to this second ^phase. [act:gentle][tune:fall]Pollen suggests flowers were laid in the ^grave."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:fair, even]In {2008|two thousand eight}, the team saw two different ^peoples. [act:the twist, precise]But in {2025|twenty twenty-five}, a study of their teeth, with Sereno as a co-author, found them hard to tell ^apart."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]One people, or ^two? [act:the verdict, measured][tune:fall]*Open ^question*. [act:fair]Ancient DNA could ^settle it.",
                     "[d:tension][p:0.93][act:the last word, warm, gentle][tune:fall]Either way, someone loved ^them."]),
    ]
    return EP("gobero", "16.06", "The Embrace at Gobero", "gobero", "contested", "Were Gobero's two phases of burials made by two different peoples, or one?", "Buried in an *embrace*.", beats, shots,
              "Sereno et al. 2008 (doi:10.1371/journal.pone.0002995) · Stojanowski, Irish & Sereno 2025 (doi:10.1002/ajpa.70262) · Stojanowski & Knudson 2011 (doi:10.1002/ajpa.21542)",
              "A lakeside cemetery in today's Ténéré desert, used for thousands of years, and a woman and two children buried together on flowers. Two peoples, or one? The teeth have changed the answer.",
              ["#Sahara", "#Niger", "#Archaeology", "#Prehistory", "#GreenSahara"])


# ---------------------------------------------------------------- 16.07 Swimmers in the sand (Wadi Sura)
def swimmer(x, y, s=1.0, i=.3, c="#f0d8b0"):
    return [{"k": "circle", "x": x + 26 * s, "y": y - 6 * s, "r": 7 * s, "fill": c, "c": "none", "w": 0, "in": i},
            {"k": "line", "p": [[x - 30 * s, y], [x + 18 * s, y - 4 * s]], "c": c, "w": 4 * s, "in": i},
            {"k": "line", "p": [[x + 8 * s, y - 3 * s], [x + 30 * s, y - 22 * s]], "c": c, "w": 3 * s, "in": i},
            {"k": "line", "p": [[x - 30 * s, y], [x - 48 * s, y + 8 * s]], "c": c, "w": 3 * s, "in": i}]


def wadisura():
    over = {"k": "poly", "p": [[0, 560], [1000, 560], [1000, 760], [700, 820], [300, 800], [0, 760]], "fill": "#6d5641", "c": "#a88b66", "w": 2, "in": -1}
    wall = {"k": "rect", "x": 0, "y": 760, "w": 1000, "h": 480, "fill": "#b08a60", "c": "none", "sw": 0, "in": -1}
    sw = []
    for k, (x, y) in enumerate(((260, 900), (420, 870), (600, 930), (760, 880), (340, 1010), (560, 1040), (720, 1000))):
        sw += swimmer(x, y, 1.5, i=.3 + k * .15, c="#7a3a26")
    s0 = dark([wall, over] + sw + [{"k": "rect", "x": 0, "y": 1240, "w": 1000, "h": 300, "fill": "#caa878", "c": "none", "sw": 0, "in": -1},
                                   {"k": "label", "x": 500, "y": 1320, "t": "the 'swimmers' · Cave of Swimmers · redrawn", "c": AMBER, "in": 1.4}])
    s1, v = sahara([("Cave of Swimmers", 25.2335, 23.5947, {"c": GOLD}), ("Luxor · the Nile", 32.64, 25.69, {"c": SCAN, "a": "end", "lx": -18, "ly": -24})], 22, 34, 20, 28.5)
    s1["els"] += [tag_label(v, 26.2, 22.4, "Gilf Kebir"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}]
    s2 = stat("5,000–8,000", "figures", "in the Cave of Beasts, a shelter 17 m wide, found in 2002", "Kuper (ed.) 2013")
    hand = [[430, 1000], [430, 850], [445, 845], [455, 930], [462, 820], [478, 818], [484, 925], [494, 830], [510, 832], [512, 935], [524, 860], [540, 866], [534, 1000]]
    s3 = dark([{"k": "poly", "p": [[x - 150, y] for x, y in hand], "fill": "none", "c": "#f0d8b0", "w": 3, "in": .3, "fx": "draw"},
               {"k": "line", "p": [[690, 1000], [690, 880]], "c": "#f0d8b0", "w": 4, "in": .8},
               {"k": "line", "p": [[690, 880], [650, 820]], "c": "#f0d8b0", "w": 3, "in": .9}, {"k": "line", "p": [[690, 880], [690, 810]], "c": "#f0d8b0", "w": 3, "in": .9},
               {"k": "line", "p": [[690, 880], [730, 820]], "c": "#f0d8b0", "w": 3, "in": .9}, {"k": "line", "p": [[690, 880], [750, 870]], "c": "#f0d8b0", "w": 3, "in": 1.0},
               {"k": "line", "p": [[690, 880], [630, 870]], "c": "#f0d8b0", "w": 3, "in": 1.0},
               {"k": "label", "x": 340, "y": 1060, "t": "a baby's hand?", "c": "#e9dccb", "in": .6},
               {"k": "label", "x": 690, "y": 1060, "t": "no: a lizard's foot", "c": GOLD, "in": 1.2},
               {"k": "cap", "x": 500, "y": 600, "t": "thirteen tiny stencils, re-examined · schematic", "in": .1}])
    tl, ax = timeline(-7000, -1000, [(-7000, "7000 BCE"), (-5000, "5000"), (-3000, "3000"), (-1000, "1000")], "A long gap to bridge")
    tl["els"] += [{"k": "band", "x0": ax.x(-6500), "x1": ax.x(-4400), "y": 745, "h": 16, "c": OCHRE, "t": "the paintings", "in": .3}] + \
                 event(ax, -3100, "Egypt's first kings", row=1, c=AMBER, i=.7) + right(event(ax, -1300, "the Book of Gates", row=2, c=SCAN, i=1.0))
    s4 = tl
    s5 = dark(grp("reading one", "#9fd0ff", ["people swimming in a real lake"], y=460, size=28) +
              grp("reading two", "#e8b87a", ["the dead, floating in the waters", "before creation"], y=760, size=28))
    s6 = like(s0, cam=[1.12, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:WADI SURA · EGYPT][sfx:boom][act:hushed, intrigued]Someone painted ^swimmers, in one of the driest places on ^Earth.",
                      "[d:tension][cam:1.12|0|0][act:the question, leaning in][tune:rise]Were they swimming, or ^dead?"], cut=False),
        B("world", 1, ["[d:calm][k:THE CAVE OF SWIMMERS][act:storytelling]In {1933|nineteen thirty-three}, the explorer ^Almásy found this cave in the far south-west of ^Egypt. [act:light, a small smile]Decades later, The English Patient made it ^famous."]),
        B("collision", 2, ["[d:build][k:THE CAVE OF BEASTS][act:impressed, building]In {2002|two thousand two}, a second shelter turned up nearby, with five to eight thousand ^figures. [act:vivid]Hands, swimmers, and headless ^beasts.",
                           "[d:build][go:3|0][act:delighted, a little amazed]Some of the tiny hand stencils were made with the feet of ^lizards."]),
        B("cost", 5, ["[d:build][k:TWO READINGS][act:fair, even]Almásy thought the swimmers showed a real ^lake. [act:the other reading, measured]Many archaeologists see the dead, floating in the waters before ^creation, an idea found much later in Egyptian ^tombs."]),
        B("reversal", 4, ["[d:reveal][k:THE CATCH][act:the crux, precise]The paintings date to roughly six and a half to four and a half thousand years ^BCE. [act:fair]The Egyptian texts come two or three thousand years ^later. [act:plain][tune:fall]That's a long gap to ^bridge."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]Did Egyptian ideas of the afterlife begin in these ^caves? [act:the verdict, measured][tune:fall]*Open ^question*.",
                     "[d:tension][p:0.93][act:the last word, warm, a small smile][tune:fall]The swimmers aren't telling ^yet."]),
    ]
    return EP("wadi-sura", "16.07", "Swimmers in the Sand", "wadi-sura", "contested", "Do the painted 'swimmers' of Wadi Sura show real swimming, or the dead in a watery afterworld?", "Swimmers in the *desert*?", beats, shots,
              "Kuper (ed.) 2013, Wadi Sura: The Cave of Beasts · Honoré et al. 2016 (doi:10.1016/j.jasrep.2016.02.014) · di Lernia & Gallinaro 2010 (doi:10.1017/S0003598X00067016) · Förster, Riemer & Kuper 2012",
              "Painted swimmers in one of the driest places on Earth, and a second cave with thousands of figures and hand stencils made with lizard feet. Real swimmers, or the dead in the waters before creation?",
              ["#Egypt", "#RockArt", "#Sahara", "#Archaeology", "#GreenSahara"])


# ---------------------------------------------------------------- 16.08 The kingdom that drank its fossil water (Garamantes)
def garamantes():
    els = []
    for k in range(8):
        x = 150 + k * 95
        els += [{"k": "line", "p": [[x, 700], [x, 700 + 300 - k * 30]], "c": "#2a2019", "w": 8, "in": .2 + k * .08},
                {"k": "poly", "p": [[x - 30, 700], [x - 16, 684], [x + 16, 684], [x + 30, 700]], "fill": "#b8925f", "c": "#e9dccb", "w": 1, "in": .2 + k * .08}]
    els += [{"k": "line", "p": [[120, 1010], [850, 800]], "c": "#9fd0ff", "w": 5, "in": 1.0, "fx": "draw"},
            {"k": "line", "p": [[60, 1060], [940, 1060]], "c": "#9fd0ff", "w": 2, "dash": "10 8", "op": .7, "in": 1.3},
            {"k": "label", "x": 880, "y": 1100, "t": "ancient groundwater", "a": "end", "c": "#9fd0ff", "in": 1.4},
            {"k": "label", "x": 500, "y": 1320, "t": "a foggara: shafts over an underground canal · schematic", "c": AMBER, "in": 1.6}]
    s0 = {"base": "section", "tod": "day", "ground": 700, "lx": 60, "layers": [{"d": 0, "c": "#b8925f", "t": ""}, {"d": 200, "c": "#8a6b45", "t": ""}], "cam": [1, 500, 900], "els": els}
    s1, v = sahara([("Germa · old Garama", 12.78, 26.55, {"c": GOLD}), ("Murzuq", 13.92, 25.92, {"a": "end", "lx": -18, "ly": 30}),
                    ("Leptis Magna · the Roman coast", 14.29, 32.64, {"c": SCAN, "a": "end", "lx": -18, "ly": -24})], 6, 20, 22, 34)
    s1["els"] += [tag_label(v, 11.2, 27.6, "Fezzan"), {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}]
    s2 = stat("c. 9 m", "average shaft depth", "over hundreds of underground canals; some shafts reach about 40 m", "Wilson 2012 · Sterry, Mattingly & Wilson 2022")
    t = [{"t": "slab", "x0": -8, "x1": 8, "z0": -6, "z1": 6, "y": 0, "c": "#c9a36c"}, box(0, 0, 0, 5, 5, .6, "#a88660"),
         {"t": "pyr", "x": 0, "z": 0, "y": .6, "b": 4.2, "h": 3.8, "c": "#b89266", "edge": "rgba(0,0,0,.3)"}, {"t": "person", "x": 4.2, "y": 0, "z": 3, "h": 1.7},
         L_(0, 4.6, "a mudbrick pyramid tomb · 3–4.5 m · schematic", GOLD, z=0, dy=-26)]
    s3 = iso(t, cam=[1, 500, 900], s=54, x=500, y=1080, az=-30, spin=1.0, el=.35, table=None)
    tl, ax = timeline(-1000, 900, [(-1000, "1000 BCE"), (-500, "500"), (0, "1 CE"), (500, "500 CE")], "A desert state")
    tl["els"] += [{"k": "band", "x0": ax.x(-1000), "x1": ax.x(700), "y": 745, "h": 14, "c": GOLD, "t": "the Garamantes", "in": .3},
                  {"k": "band", "x0": ax.x(-400), "x1": ax.x(700), "y": 660, "h": 14, "c": "#9fd0ff", "t": "foggaras in use", "in": .6}] + \
                 event(ax, -440, "Herodotus writes", row=3, c=AMBER, i=.9) + right(event(ax, 700, "decline", row=3, c=RED, i=1.2))
    s4 = tl
    fall = [[180, 760], [360, 800], [540, 880], [700, 1000], [840, 1120]]
    s5 = dark([{"k": "line", "p": fall, "c": "#9fd0ff", "w": 5, "curve": True, "in": .3, "fx": "draw"},
               {"k": "line", "p": [[180, 900], [840, 900]], "c": "#e9dccb", "w": 2, "dash": "10 8", "in": .8},
               {"k": "label", "x": 190, "y": 940, "t": "deepest the shafts could reach", "a": "start", "c": "#e9dccb", "in": 1.0},
               {"k": "label", "x": 190, "y": 740, "t": "the water table", "a": "start", "c": "#9fd0ff", "in": .5},
               {"k": "cap", "x": 500, "y": 600, "t": "a falling water table · schematic", "in": .1}])
    s6 = like(s0, cam=[1.1, 500, 940])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:FEZZAN · LIBYA][sfx:boom][act:intrigued, measured]Rome called them ^barbarians. [act:the reveal, leaning in]They built towns, pyramids, and hundreds of kilometres of ^tunnels.",
                      "[d:tension][cam:1.12|0|0][act:the twist][tune:fall]In the middle of the ^Sahara."], cut=False),
        B("world", 1, ["[d:calm][k:THE GARAMANTES][act:plain, orienting]The Garamantes of Fezzan, in south-west ^Libya, from about a thousand BCE to seven hundred ^CE. [act:amused, storytelling]Herodotus describes their chariots, and cattle that grazed walking ^backwards."]),
        B("collision", 2, ["[d:build][k:THE TUNNELS][act:building, precise]Their secret was ^water. [act:vivid]Underground canals, called ^foggaras, tapped ancient groundwater, through shafts about nine metres deep on ^average."]),
        B("cost", 3, ["[d:build][k:THE STATE][act:impressed]With that water came oasis ^towns, the first in the ^Sahara, and pyramid ^tombs. [act:plain]Trade across the desert@noun kept them ^rich."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:grave, measured]But that groundwater fell as rain thousands of years earlier, in wetter ^times, and it doesn't come ^back. [act:precise]As the water table sank, the canals ran ^dry.",
                          "[d:build][act:fair, careful]Shifting trade, and scarce labour, perhaps ^enslaved, played a part ^too."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, even][tune:rise]A desert@noun kingdom that drank its fossil ^water? [act:the verdict, measured][tune:fall]^*Plausible*. [act:fair]A leading explanation, but not the only ^one.",
                     "[d:tension][p:0.93][act:the last word, quiet][tune:fall]A warning, perhaps, written in ^tunnels."]),
    ]
    return EP("garamantes", "16.08", "The Kingdom That Drank Its Fossil Water", "garamantes", "plausible", "Did the Garamantes' desert state fade when its ancient groundwater ran out?", "Pyramids and *tunnels* in the Sahara.", beats, shots,
              "Mattingly & Sterry 2013 (doi:10.1017/S0003598X00049097) · Wilson 2012 (doi:10.1080/0067270X.2012.727614) · Sterry, Mattingly & Wilson 2022 · Sterry & Mattingly (eds) 2020 · Herodotus 4.183",
              "The Garamantes built the Sahara's first towns, pyramid tombs and hundreds of kilometres of underground canals, all on ancient groundwater. Did the water running out bring them down?",
              ["#Sahara", "#Libya", "#AncientHistory", "#Archaeology", "#GreenSahara"])


# ---------------------------------------------------------------- 16.09 The ledger
def _ledger_text():
    v = View(-18, 36, 10, 36, (40, 440, 920, 820))
    s0 = mapshot(v, pins=[("Nabta Playa", 30.7256, 22.508, {"c": GOLD, "a": "end", "lx": -18, "ly": 30}), ("Wadi Sura", 25.2335, 23.5947, {"ly": -22}),
                          ("Tassili · Takarkori", 10.0, 24.9, {"a": "end", "lx": -18}), ("Germa", 12.78, 26.55, {"ly": -24}),
                          ("Gobero", 9.52, 17.08, {}), ("Lake Chad", 14.2, 13.2, {"c": SCAN})], cam=[1, 500, 860])
    s1 = dark(grp("Established · strong", "#8fd9b0", ["a green Sahara, 11,000–5,000 years ago", "Tutankhamun's scarab: impact glass", "a lost lineage at Takarkori"]))
    s2 = dark(grp("Plausible · mixed", "#e8b87a", ["the Garamantes' fossil water", "Nabta's sun-watching stones", "a switch-off: sudden here, slow there"]))
    s3 = dark(grp("Open question", "#9fd0ff", ["Gobero: one people or two?", "the swimmers: alive or dead?"], size=28))
    s4 = dark(grp("Ruled out", "#ff8a7a", ["astronauts at Tassili"]))
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:WHEN THE SAHARA WAS GREEN][sfx:boom][act:warm, opening the book]Eight cases from the ^Sahara. [act:inviting, a small smile]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, ticking them off][tune:level]The Sahara was ^green, with lakes, fishers and ^herders. [act:plain, sure][tune:level]Tutankhamun's scarab is impact ^glass. [act:the last one, warm][tune:fall]And a lost lineage lived at ^Takarkori."]),
        B("collision", 2, ["[d:build][k:STILL WEIGHED][act:weighing each, even][tune:level]The Garamantes and their fossil water: ^plausible. [act:measured][tune:level]Nabta's stones: watching the sun, not the ^stars. [act:light][tune:fall]And the switch-off: sudden here, slow ^there."]),
        B("cost", 3, ["[d:build][k:OPEN QUESTIONS][act:curious, even]One people at Gobero, or ^two? [act:practical][tune:fall]And the swimmers: alive, or ^dead?"]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:clear, a small smile]Astronauts at ^Tassili. [act:dry][tune:fall]The real story was the ^copies."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:warm, wise, even]The Sahara isn't an empty space on the ^map. [act:the lesson, simple][tune:fall]It's an archive, drying in the ^sun.",
                     "[d:tension][p:0.93][act:the motto, calm and warm]^Coherence is the measure. [act:quiet, the last word][tune:fall]Not ^final demonstration."]),
    ]
    return EP("sahara-ledger", "16.09", "When the Sahara Was Green · The Ledger", "", "mixed", "What held up, and what didn't, across the Sahara.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 16",
              "The verdicts of When the Sahara Was Green in one ledger: what is established about the green Sahara, what is plausible or mixed, what is still open, and what is ruled out.",
              ["#Sahara", "#History", "#Archaeology", "#GreenSahara", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: the cabinet of the eight cases (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    iso_shot = lambda ep: next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
    iso_el = lambda sh: next((e for e in sh["els"] if e.get("k") == "iso"), None)
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = iso_shot(ep); e = iso_el(sh)
        return e if e else sh
    C = Cabinet([
        {"name": "The green Sahara", "model": mdl(switchoff(), 0)},
        {"name": "Desert glass", "model": mdl(glass(), 0)},
        {"name": "Takarkori", "model": mdl(takarkori(), 0)},
        {"name": "The Garamantes", "model": mdl(garamantes())},
        {"name": "Nabta Playa", "model": mdl(nabta())},
        {"name": "Gobero", "model": mdl(gobero())},
        {"name": "The swimmers", "model": mdl(wadisura(), 0)},
        {"name": "Tassili", "model": mdl(tassili(), 0)},
    ])
    C.build()
    GS, GL, TK, GA, NA, GO, WS, TA = range(8)
    s1 = C.step(C.cam_cell(GS), C.verdict(GS, "established", "lakes, fishers, herders", .4) + C.wash(GS, VCOL["established"], at=.9, op=.14))
    s2 = C.step(C.cam_cell(GL), C.verdict(GL, "established", "the scarab is impact glass", .4))
    s3 = C.step(C.cam_cell(TK), C.verdict(TK, "established", "a lost lineage", .4) + C.people(TK, 2, at=1.0))
    s4 = C.step(C.cam_cell(GA), C.verdict(GA, "plausible", "fossil water", .4))
    s5 = C.step(C.cam_cell(NA), C.verdict(NA, "mixed", "the sun, not the stars", .4))
    s6 = C.step(C.cam_cell(GS), C.verdict(GS, "mixed", "sudden here, slow there", .3))
    s7 = C.step(C.cam_cell(GO), C.verdict(GO, "open", "one people, or two?", .4) + C.question(GO, dx=C.w * .26, dy=-160, at=.8))
    s8 = C.step(C.cam_cell(WS), C.verdict(WS, "open", "alive, or dead?", .4) + C.question(WS, dx=C.w * .26, dy=-160, at=.8))
    s9 = C.step(C.cam_cell(TA), C.verdict(TA, "ruled", at=.2) + C.struck(TA, "astronauts on the rock", dy=-170, at=.5))
    s10 = C.step(C.cam_cell(TA), C.note(TA, "the real story: the copies", at=.3, c="#f2c98e"))
    s11 = C.step(C.cam_all())
    s12 = C.step(C.cam_all(), [e for i in range(8) for e in C.wash(i, "#f2b36b", at=.3 + .1 * i, op=.12)])
    s13 = C.step(C.cam_all(z=.64, sy=700))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5, (0, 2): "%d|1.6" % s6}),
        3: (s7, {(0, 1): "%d|1.1" % s8}),
        4: (s9, {(0, 1): "%d|.4" % s10}),
        5: (s11, {(0, 1): "%d|.8" % s12, (1, 0): "%d|4" % s13}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/sahara-ledger.json)."""
    import recap
    return recap.recap(ledger, "sahara-ledger", None)


# ================================================================ the continuous takes (one mural per film: see mural.py)
def _mur():
    from mural import remix
    import illus
    return remix, illus


def _t(els, r):
    """Timings written in seconds of the new narration on that step, turned into the remix's own clock (it stretches every
    step's build-ins by r, how much longer the step's words became: see mural.remix)."""
    out = []
    for e in els:
        e = dict(e)
        if isinstance(e.get("in"), (int, float)) and e["in"] > 0:
            e["in"] = round(e["in"] / r, 2)
        out.append(e)
    return out


def cow(x, y, s=1.0, at=0, fill="#d8c7ae", op=None, lying=False, flip=False, horns=None):
    """A cow in profile (feet on y), facing right (flip: left): a body, legs, a head and horns (horns: forward-curving ones, Herodotus' cattle)."""
    f = -1 if flip else 1
    X = lambda a: round(x + f * a * s, 1)
    Y = lambda b: round(y + b * s, 1)
    w = max(2.0, 9 * s)
    if lying:
        body = [[X(85 * math.cos(t)), Y(-34 + 30 * math.sin(t))] for t in [2 * math.pi * k / 24 for k in range(24)]]
        head = [[X(56), Y(-50)], [X(84), Y(-86)], [X(104), Y(-84)], [X(118), Y(-64)], [X(104), Y(-56)], [X(80), Y(-40)]]
        e = [{"k": "poly", "p": body, "fill": fill, "c": "none", "w": 0, "in": at, "curve": True},
             {"k": "poly", "p": head, "fill": fill, "c": "none", "w": 0, "in": at},
             {"k": "line", "p": [[X(40), Y(-6)], [X(76), Y(-4)]], "c": fill, "w": w, "in": at},
             {"k": "line", "p": [[X(-84), Y(-44)], [X(-98), Y(-12)]], "c": fill, "w": w * .4, "in": at}]
        hx, hy = 92, -86
    else:
        body = [[X(70 * math.cos(t)), Y(-64 + 28 * math.sin(t))] for t in [2 * math.pi * k / 24 for k in range(24)]]
        head = [[X(50), Y(-80)], [X(80), Y(-102)], [X(100), Y(-96)], [X(108), Y(-74)], [X(92), Y(-66)], [X(62), Y(-52)]]
        e = [{"k": "poly", "p": body, "fill": fill, "c": "none", "w": 0, "in": at, "curve": True},
             {"k": "poly", "p": head, "fill": fill, "c": "none", "w": 0, "in": at}] + \
            [{"k": "line", "p": [[X(a), Y(-50)], [X(a), Y(0)]], "c": fill, "w": w, "in": at} for a in (-50, -34, 38, 54)] + \
            [{"k": "line", "p": [[X(-68), Y(-76)], [X(-82), Y(-30)]], "c": fill, "w": w * .4, "in": at}]
        hx, hy = 84, -100
    if horns == "forward":
        e += [{"k": "line", "p": [[X(hx - 6), Y(hy)], [X(hx + 22), Y(hy - 10)], [X(hx + 46), Y(hy + 18)], [X(hx + 50), Y(hy + 54)]], "c": "#efe6d2", "w": w * .45, "in": at, "curve": True}]
    else:
        e += [{"k": "line", "p": [[X(hx - 6), Y(hy)], [X(hx - 16), Y(hy - 18)]], "c": "#efe6d2", "w": w * .45, "in": at},
              {"k": "line", "p": [[X(hx + 6), Y(hy)], [X(hx + 16), Y(hy - 18)]], "c": "#efe6d2", "w": w * .45, "in": at}]
    if op is not None:
        for q in e:
            q.update(op=op, keepop=True)
    return e


def trilithon(x, y, at=0, c="#cbbca8"):
    return [{"k": "rect", "x": x - 38, "y": y - 84, "w": 20, "h": 84, "r": 3, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"},
            {"k": "rect", "x": x + 18, "y": y - 84, "w": 20, "h": 84, "r": 3, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"},
            {"k": "rect", "x": x - 46, "y": y - 102, "w": 92, "h": 18, "r": 3, "fill": c, "c": "none", "sw": 0, "in": at + .3, "fx": "pop"}]


def column(x, y, at=0, c="#e8dcc2"):
    return [{"k": "rect", "x": x - 24, "y": y - 14, "w": 48, "h": 14, "r": 2, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"},
            {"k": "rect", "x": x - 13, "y": y - 96, "w": 26, "h": 82, "r": 2, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"},
            {"k": "rect", "x": x - 26, "y": y - 110, "w": 52, "h": 14, "r": 2, "fill": c, "c": "none", "sw": 0, "in": at, "fx": "rise"}]


def nabta_m():
    """Nabta Playa as one continuous take (see mural.py): the playa fills, the gates line up with north and the midsummer
    sunrise, 1,800 years drawn twice, cattle chambers and dragged stones, and a star map that drifts out of true."""
    import copy
    remix, I = _mur()
    ep = nabta()
    # 0 · the model, without its long labels (the narrator names everything)
    s0 = copy.deepcopy(ep["shots"][0])
    for e in s0["els"]:
        if e.get("k") == "iso":
            e["items"] = [it for it in e["items"] if it.get("t") != "label"]
    sky = [(200, 520), (262, 498), (324, 476)]
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") != "scale"]
    hook = _t([I.glow(x, y, 50, 9.8 + .25 * k, .8, "lamp") for k, (x, y) in enumerate(sky)] + [I.dot(x, y, 7, "#fff6e8", 9.8 + .25 * k) for k, (x, y) in enumerate(sky)], 1.36)
    # 1 · the map: a hundred kilometres from Abu Simbel; a playa, cut open: rain, a seasonal lake, herders and cattle
    v = View(27, 36, 19.5, 27.5, (40, 330, 920, 900))
    nx, ny = v.p(30.7256, 22.508); ax_, ay_ = v.p(31.6258, 22.3372)
    X0, Y0, W, H = 200, 1110, 560, 300
    hollow = [[X0, 1250], [X0 + 90, 1250], [X0 + 130, 1310], [X0 + 330, 1310], [X0 + 370, 1250], [X0 + W, 1250], [X0 + W, Y0 + H], [X0, Y0 + H]]
    water = [[X0 + 96, 1258], [X0 + 132, 1306], [X0 + 328, 1306], [X0 + 364, 1258]]
    mp = _t([I.arrow([[ax_ - 4, ay_ + 22], [(nx + ax_) / 2 + 10, ay_ + 64], [nx + 6, ny + 24]], 4.0, I.AMBER, 3, dur=.8),
             I.label(ax_ + 14, ay_ + 84, "100 km", 4.4, I.AMBER, 30, "start"),
             I.line([[nx, ny + 14], [nx, Y0]], 8.8, I.AMBER, 2, "inferred", .6),
             I.box(X0, Y0, W, H, "#1c1713", I.AMBER, 2.5, 22, 9.0, fx="pop"),
             {"k": "poly", "p": hollow, "fill": "#8a7050", "c": "#c9ad85", "w": 2, "in": 9.6}] +
            [I.line([[X0 + 60 + 42 * k, Y0 + 30], [X0 + 46 + 42 * k, Y0 + 80]], 15.6 + .05 * k, I.BLUE, 2.5, draw=False) for k in range(9)] +
            [{"k": "poly", "p": water, "fill": LAKE, "c": "#9fd0ff", "w": 1.5, "in": 17.0, "fx": "fill", "dur": 1.6}] +
            cow(X0 + 450, 1250, .5, 19.6, "#e8dcc6") + cow(X0 + 70, 1250, .46, 20.0, "#cbbca8", flip=True) +
            [I.person(X0 + 520, 1250, 76, 20.4, "#e8d6b8")], 2.04)
    # 2 · the circle in plan: four metres, five strides, four pairs of stones, north-south, and the midsummer sunrise
    C, R = (500, 860), 180
    sun = (math.sin(math.radians(64)), -math.cos(math.radians(64)))
    ring = [I.dot(round(C[0] + R * math.cos(2 * math.pi * k / 28), 1), round(C[1] + R * math.sin(2 * math.pi * k / 28), 1), 9, "#9a8466", .5 + .05 * k) for k in range(28)]
    pairs = []
    for j, (dx, dy) in enumerate([(0, -1), (0, 1), sun, (-sun[0], -sun[1])]):
        for side in (-1, 1):
            px, py = C[0] + R * dx - side * 30 * dy, C[1] + R * dy + side * 30 * dx
            pairs.append(I.box(round(px - 15, 1), round(py - 15, 1), 30, 30, "#d9c39a", "#fff0d0", 1.5, 4, 6.6 + .25 * j, fx="pop"))
    sx, sy = C[0] + 330 * sun[0], C[1] + 330 * sun[1]
    plan = {"base": "plan", "north": False, "cam": [1.25, 500, 860], "els": _t(
        ring + [I.line([[C[0] - R, 1105], [C[0] + R, 1105]], 2.0, I.BONE, 2.5, dur=.6), I.line([[C[0] - R, 1088], [C[0] - R, 1122]], 2.0, I.BONE, 2.5, draw=False),
                I.line([[C[0] + R, 1088], [C[0] + R, 1122]], 2.0, I.BONE, 2.5, draw=False), I.label(C[0] + R + 22, 1116, "4 m", 2.4, I.BONE, 34, "start")] +
        [I.oval(C[0] - R + 34 + 72 * k, 1168 + 24 * (k % 2), 11, 19, "#e8d6b8", op=.85, at=3.8 + .45 * k) for k in range(5)] +
        pairs + [I.glow(C[0], C[1], 120, 7.6, .25, "lamp")] +
        [I.line([[C[0], 1060], [C[0], 590]], 11.4, I.BLUE, 4, "inferred", 1.6), I.arrow([[C[0], 600], [C[0], 560]], 12.6, I.BLUE, 4, dur=.3, curve=False),
         I.label(C[0], 530, "N", 12.8, I.BLUE, 38, st="lab")] +
        [I.glow(sx + 40, sy - 20, 150, 17.4, .8, "sun"), I.dot(sx + 40, sy - 20, 24, "#ffe2a8", 17.6),
         I.line([[C[0] - 300 * sun[0], C[1] - 300 * sun[1]], [sx, sy]], 18.2, I.AU, 4, "inferred", 1.6),
         I.label(880, sy - 80, "midsummer sunrise", 19.2, I.AU, 30, "end")], 2.24)}
    # 3 · 1,800 years, drawn twice: Nabta to Stonehenge, and Rome to us
    X = lambda yr: 150 + 720 * (yr + 5400) / 7450
    yb = 1020
    def bracket(a, b, at):
        return [I.arrow([[X(a) + 6, yb - 130], [(X(a) + X(b)) / 2, yb - 190], [X(b) - 6, yb - 130]], at, I.AMBER, 3, dur=.9),
                I.label((X(a) + X(b)) / 2, yb - 210, "1,800 years", at + .5, I.AMBER, 30)]
    dates = {"base": "dark", "cam": [1.2, 500, 930], "els": _t(
        [I.line([[110, yb], [890, yb]], .2, "#8c7152", 3, dur=1.2)] +
        [I.ring(X(-4800), yb - 40, 34, .8, "#cbbca8", 6, dur=.8), I.dot(X(-4800), yb, 8, I.AU, .8), I.label(X(-4800), yb + 50, "4800 BCE", 1.2, I.AU, 30)] +
        trilithon(X(-3000), yb - 2, 4.0) + [I.dot(X(-3000), yb, 8, "#cbbca8", 4.0), I.label(X(-3000), yb + 50, "Stonehenge", 4.4, "#cbbca8", 30)] + bracket(-4800, -3000, 5.2) +
        column(X(226), yb - 2, 8.6) + [I.dot(X(226), yb, 8, "#e8dcc2", 8.6), I.label(X(226), yb + 50, "Rome", 8.8, "#e8dcc2", 30)] +
        [I.person(X(2026) - 10, yb - 2, 110, 10.0, "#f2c98e"), I.label(X(2026) - 10, yb + 50, "us", 10.2, I.AU, 30)] + bracket(226, 2026, 10.6), 1.84)}
    # 4 · nearby: cattle in a clay-lined chamber; stones nearly three metres tall, dragged into lines
    G = 880
    burials = {"base": "section", "ground": G, "tod": "day", "sun": [860, 380, 30], "layers": [{"d": 0, "c": "#9c7e58", "t": ""}, {"d": 330, "c": "#6f5a44", "t": ""}],
               "cam": [1.15, 500, 880], "els": _t(
        [{"k": "poly", "p": [[110, G], [130, G + 210], [430, G + 210], [450, G]], "fill": "#2e2219", "c": "#c9774a", "w": 7, "in": .4, "fx": "draw", "dur": 1.2},
         {"k": "poly", "p": [[118, G + 2], [136, G + 202], [424, G + 202], [442, G + 2]], "fill": "#3a2b1f", "c": "none", "w": 0, "in": .6}] +
        cow(285, G + 190, 1.25, 1.4, "#d8c7ae", lying=True) + [I.glow(285, G + 120, 150, 1.6, .35, "lamp"), I.label(280, G + 260, "clay-lined chamber", 2.0, "#e6b48a", 28)] +
        [I.box(484 + 95 * k, G - 224 + 8 * (k % 2), 56, 224 - 8 * (k % 2), "#b9a27e", "#e8d6b0", 1.5, 6, 3.4 + .4 * k, fx="rise") for k in range(4)] +
        [I.line([[850, G], [850, G - 224]], 5.0, I.BONE, 2.5, dur=.6), I.line([[838, G - 224], [862, G - 224]], 5.0, I.BONE, 2.5, draw=False),
         I.label(866, G - 100, "3 m", 5.2, I.BONE, 32, "start")] +
        [{"k": "poly", "p": [[130, G - 2], [130, G - 46], [330, G - 52], [336, G - 2]], "fill": "#b9a27e", "c": "#e8d6b0", "w": 1.5, "in": 6.4, "fx": "rise"},
         I.line([[336, G - 30], [372, G - 72], [404, G - 76]], 7.0, "#e8d6b8", 2.5, dur=.4),
         I.person(380, G, 136, 7.0, "#2a2018"), I.person(424, G, 130, 7.2, "#2a2018"),
         I.arrow([[180, G - 180], [300, G - 240], [440, G - 260]], 7.8, I.AMBER, 4, "known", 1.0)], 1.5)}
    # 5 · a star map? Orion overhead, stones below; the stars drift over the centuries; 1,500 years apart; a stone moved
    st = [(380, 370), (625, 405), (468, 548), (503, 532), (538, 516), (430, 690), (612, 682)]
    gx = lambda x: 500 + (x - 500) * 1.15
    gy = lambda y: 1090 + (y - 370) * .3
    stars = {"base": "dark", "stars": 70, "cam": [1, 500, 860], "els": _t(
        [I.box(-40, 1040, 1080, 420, "#2e241b", r=0), I.line([[-40, 1040], [1040, 1040]], 0, "#6a5640", 2, draw=False)] +
        [I.glow(x, y, 46, 2.4 + .12 * k, .9, "lamp") for k, (x, y) in enumerate(st)] + [I.dot(x, y, 7, "#fff6e8", 2.4 + .12 * k) for k, (x, y) in enumerate(st)] +
        [I.line([st[a], st[b]], 4.4, "#cfc6e8", 1.5, dur=.5) for a, b in ((0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6))] +
        [I.box(gx(x) - 12, gy(y) - 18, 24, 22, "#b9a27e", "#e8d6b0", 1.2, 3, 5.2 + .1 * k, fx="pop") for k, (x, y) in enumerate(st)] +
        [I.line([[x, y + 12], [gx(x), gy(y) - 22]], 6.2 + .15 * k, I.LILAC, 2.5, "claimed", .8) for k, (x, y) in enumerate(st[2:5])] +
        [I.ring(x + 84, y + 52, 13, 10.4 + .1 * k, "#cfc6e8", 2.5, "inferred", .4) for k, (x, y) in enumerate(st)] +
        [I.arrow([[x + 12, y + 8], [x + 70, y + 44]], 11.0 + .1 * k, "#cfc6e8", 2.5, dur=.5, curve=False) for k, (x, y) in enumerate(st)] +
        [I.line([[220, 1350], [780, 1350]], 16.2, "#8c7152", 3, dur=.6), I.dot(260, 1350, 10, I.LILAC, 16.6), I.label(260, 1400, "the stars", 16.8, I.LILAC, 28),
         I.dot(740, 1350, 10, I.AU, 18.0), I.label(740, 1400, "the stones", 18.2, I.AU, 28),
         I.arrow([[270, 1316], [500, 1280], [730, 1316]], 18.6, I.BONE, 3, dur=.9), I.label(500, 1262, "1,500 years", 19.0, I.BONE, 30)] +
        [I.box(gx(612) - 12, gy(682) - 18, 24, 22, "none", "#e8d6b0", 1.5, 3, 22.2, style="inferred"),
         I.arrow([[gx(612) - 14, gy(682) - 6], [gx(612) - 70, gy(682) + 4]], 22.6, I.RED, 3, dur=.4, curve=False)] +
        [I.label(255, 905, "calendar circle", 25.6, "#e9dccb", 40, st="serif"), I.strike(100, 895, 410, 880, 28.0, I.RED, 4)], 1.93)}
    # 6 · the verdict, back at the circle: a sun rising over it; the stars, struck
    tag = _t([I.glow(800, 560, 170, 2.4, .7, "sun"), I.dot(800, 560, 26, "#ffe2a8", 2.6), I.strike(160, 548, 364, 448, 10.0, I.RED, 4)], 1.43)
    return remix(ep, scenes={0: s0, 1: s1, 2: plan, 3: dates, 4: burials, 5: stars}, alias={6: 0}, adds={0: hook, 1: mp},
                 cams={1: [1.45, 480, 1060], 6: [1.12, 500, 960]}, beat_adds={5: (tag, [1.12, 500, 960])})


def glass_m():
    """Tutankhamun's sky-glass as one continuous take (see mural.py): the glass field on the border, tracks counted like
    tally marks, a museum tag rewritten, a melt twice as hot as lava, and a blast in the sky with no hole beneath it."""
    import copy
    remix, I = _mur()
    ep = glass()
    GL, GLs = "#d9df8e", "#f1f5c0"
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] = [e for e in s0["els"] if e.get("k") != "label"]
    hook = _t([I.glow(500, 980, 230, 10.2, .55, "lamp"), I.arrow([[960, 300], [860, 420], [700, 640]], 11.0, I.AMBER, 4, dur=.8),
               I.glow(700, 640, 90, 11.6, .8, "sun")], 1.84)
    # 1 · the map: the border of Egypt and Libya, and the glass scattered over the dunes beside it
    v = View(22, 34, 21, 32.5, (40, 330, 920, 900))
    fx_, fy_ = v.p(25.5, 25.4)
    pts = [(round(fx_ - 8 + 46 * math.cos(a_) * r_, 1), round(fy_ + 18 + 26 * math.sin(a_) * r_, 1)) for a_, r_ in
           [(2.4 * k, .25 + .75 * ((k * 37) % 11) / 10) for k in range(26)]]
    s1 = copy.deepcopy(ep["shots"][1])
    for e in s1["els"]:
        if e.get("k") == "pin" and e.get("t", "").startswith("the glass field"):
            e.update(ly=-34, lx=22)
    mp = _t([I.line([v.p(25, 22), v.p(25, 29.5), v.p(25.15, 31.6)], 4.2, "#e9dccb", 3, "inferred", 1.2),
             I.label(v.p(25, 23.4)[0] - 20, v.p(25, 23.4)[1], "Libya", 4.8, "#cbbca8", 32, "end"),
             I.label(v.p(25, 23.4)[0] + 20, v.p(25, 23.4)[1], "Egypt", 4.8, "#cbbca8", 32, "start")] +
            [I.dot(x, y, 5, GL, 8.4 + .06 * k) for k, (x, y) in enumerate(pts)] + [I.glow(fx_, fy_, 90, 8.6, .5, "lamp")], 2.29)
    # 2 · silica like sand and window glass; 29 million years, read from tracks counted like tally marks; Stone Age tools
    chunk = [[380, 520], [470, 470], [590, 488], [650, 560], [628, 660], [540, 712], [430, 700], [362, 620]]
    r7 = rnd(7)
    tracks = [[[round(x, 1), round(y, 1)], [round(x + 26 * math.cos(a_), 1), round(y + 26 * math.sin(a_), 1)]] for x, y, a_ in
              [(330 + r7() * 170, 950 + r7() * 150, r7() * 3.1) for _ in range(12)]]
    tally = []
    for g in range(3):
        for j in range(4):
            tally.append(I.line([[650 + 72 * g + 11 * j, 960], [650 + 72 * g + 11 * j, 1040]], 18.2 + .5 * g + .09 * j, I.BONE, 4, dur=.15))
        tally.append(I.line([[642 + 72 * g, 1030], [700 + 72 * g, 968]], 18.6 + .5 * g, I.AMBER, 4, dur=.2))
    age = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        [{"k": "poly", "p": chunk, "fill": GL, "c": GLs, "w": 3, "in": .4, "op": .9, "keepop": True}, I.glow(505, 590, 200, .6, .45, "lamp"),
         I.line([[430, 560], [520, 520]], .8, "#ffffff", 3, op=.6), I.label(505, 790, "almost pure silica", 1.6, GL, 32)] +
        [{"k": "poly", "p": [[100, 680], [140, 650], [185, 620], [230, 650], [270, 680]], "fill": "#c9a76a", "c": "none", "w": 0, "curve": True, "in": 2.4, "fx": "rise"}] +
        [I.dot(x, y, 4, "#e8cf98", 2.6 + .02 * k) for k, (x, y) in enumerate(scatter_heap(185, 676, 30))] +
        [I.box(770, 520, 120, 150, "rgba(159,208,255,.18)", "#cfe6ff", 3, 4, 3.6, fx="pop"), I.line([[830, 520], [830, 670]], 3.8, "#cfe6ff", 2, draw=False),
         I.line([[770, 595], [890, 595]], 3.8, "#cfe6ff", 2, draw=False)] +
        [I.label(500, 1250, "29 million years", 5.4, I.AU, 52, st="serif", fx="pop")] +
        [I.line([[470, 815], [432, 900]], 9.6, I.BONE, 2, "inferred", .5), I.oval(420, 1030, 128, 128, "#2f2b1c", I.BONE, 3, 1, 10.0), I.line([[510, 1120], [580, 1200]], 10.0, I.BONE, 8, draw=False)] +
        [I.line(p_, 12.0 + .35 * k, "#fff6e8", 3, dur=.2) for k, p_ in enumerate(tracks)] + tally +
        [I.person(160, 1410, 160, 23.0, "#e8d6b8"), {"k": "poly", "p": [[196, 1306], [236, 1290], [228, 1318], [204, 1332]], "fill": GL, "c": GLs, "w": 1.5, "in": 23.4, "fx": "pop"},
         I.glow(214, 1312, 60, 23.4, .7, "lamp")], 2.5)}
    # 4 · the museum tag: 'chalcedony' in 1922; a lens in the 1990s; 'desert glass'
    tagbox = lambda y, at, c: [I.box(140, y, 330, 86, "#efe3c8", "#8a7a66", 2, 10, at, fx="pop"), I.dot(166, y + 43, 9, "#2a2018", at)]
    tags = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        scarab(520, 760, .78, .3) + [I.line([[470, 900], [420, 960], [460, 1000]], 1.4, "#cbbca8", 2, dur=.6, curve=True)] +
        tagbox(990, 1.6, "#efe3c8") + [I.label(300, 970, "1922", 1.8, "#cbbca8", 30), I.label(320, 1046, "chalcedony", 5.0, "#2a2018", 36, st="serif", halo=False)] +
        [I.ring(520, 760, 215, 8.6, "#cfe6ff", 6, dur=1.0), I.line([[672, 912], [790, 1030]], 9.0, "#cfe6ff", 14, draw=False), I.glow(520, 760, 220, 9.4, .4),
         I.label(720, 560, "1990s", 9.8, "#cfe6ff", 32)] +
        [I.strike(200, 1036, 450, 1028, 14.2, I.RED, 5)] + tagbox(1150, 14.6, "#efe3c8") +
        [I.label(320, 1206, "desert glass", 15.0, "#5a6a10", 36, st="serif", halo=False), I.glow(305, 1190, 170, 15.0, .35, "lamp")], 1.5)}
    # 5 · what melted it: a shock only an impact makes, no volcano; then 2,750 degrees, more than twice as hot as lava
    T = lambda c: 150 + 700 * c / 3000
    crystal = [[300, 640], [350, 690], [350, 860], [300, 910], [250, 860], [250, 690]]
    heat = {"base": "dark", "cam": [1.05, 500, 880], "els": _t(
        [{"k": "poly", "p": crystal, "fill": "rgba(232,220,194,.18)", "c": "#e8dcc2", "w": 3, "in": 1.8, "fx": "draw"}] +
        [I.line([[262, 720 + 30 * j], [338, 690 + 30 * j]], 3.8 + .15 * j, I.AU, 3) for j in range(6)] + [I.glow(300, 775, 120, 4.4, .55, "lamp")] +
        [I.line([[520, 600], [880, 600]], 6.4, "#8c7152", 3, dur=.5), I.arrow([[920, 300], [820, 420], [700, 590]], 7.0, I.AMBER, 4, dur=.7), I.glow(700, 600, 120, 7.8, .9, "sun"),
         I.oval(700, 600, 70, 20, "#3a2b1f", I.AMBER, 2, 1, 8.0)] +
        [I.arrow([[700, 640], [420, 760]], 9.6, I.AMBER, 3, "inferred", .8)] +
        [{"k": "poly", "p": [[620, 1000], [700, 860], [740, 860], [820, 1000]], "fill": "#6a4a34", "c": "#c9774a", "w": 2, "in": 12.8, "fx": "rise"},
         I.glow(720, 850, 60, 12.9, .7, "red"), I.strike(600, 1010, 840, 840, 13.8, I.RED, 5)] +
        [I.line([[T(0), 1240], [T(3000), 1240]], 15.2, "#3a3028", 34, draw=False), I.line([[T(0), 1240], [T(2750), 1240]], 15.6, "#ff9a5a", 26, dur=2.2),
         I.label(T(2750), 1195, "2,750 °C", 17.8, "#ffb27a", 36, "end")] +
        [I.line([[T(1200), 1215], [T(1200), 1290]], 19.8, I.BONE, 3, draw=False), I.label(T(1200), 1330, "lava", 20.0, I.BONE, 30),
         I.line([[T(2400), 1210], [T(2400), 1295]], 21.0, I.BONE, 3, "inferred", .3), I.label(T(2400), 1330, "2 × lava", 21.2, I.BONE, 30)], 2.14)}
    # 3 · where's the crater? an airburst melts the sand without a hole; Kebira, tested, fails
    gy = 1100
    rr = rnd(5)
    catch = {"base": "sky", "tod": "day", "ground": gy, "sun": False, "cam": [1.05, 500, 900], "els": _t(
        [I.dot(round(120 + rr() * 760, 1), round(gy + 12 + rr() * 70, 1), 5, GL, .4 + .02 * k) for k in range(30)] +
        I.question(300, 880, 1.0, 120) +
        [I.arrow([[960, 280], [860, 400], [720, 560]], 6.6, I.AMBER, 4, dur=.8), I.glow(700, 600, 230, 8.4, .95, "sun"), I.glow(700, 600, 120, 8.6, .9, "red"),
         I.ring(700, 600, 90, 8.8, "#ffe2a8", 3, dur=.6), I.ring(700, 600, 160, 9.4, "#ffe2a8", 2, dur=.8)] +
        [I.arrow([[700 + 40 * k, 680], [700 + 90 * k, gy - 20]], 12.9 + .12 * abs(k), "#ffb27a", 3, dur=.6, curve=False) for k in (-2, -1, 0, 1, 2)] +
        [I.line([[520, gy], [880, gy]], 14.6, "#ffb27a", 10, dur=1.2), I.glow(700, gy, 220, 14.8, .6, "red")], 1.88)}
    kebira = _t([{"k": "poly", "p": I.ellipse(300, gy, 170, 60, 24, 0, 180), "fill": "#3a2b1f", "c": "#e9dccb", "w": 3, "in": .4, "fx": "draw"},
                 I.label(300, gy + 110, "Kebira", 1.0, "#e9dccb", 32), I.strike(150, gy + 70, 450, gy - 50, 3.8, I.RED, 6), I.strike(150, gy - 50, 450, gy + 70, 4.0, I.RED, 6)], 1.40)
    tag = _t(I.question(820, 760, 10.0, 90), 1.83)
    return remix(ep, scenes={0: s0, 1: s1, 2: age, 3: catch, 4: tags, 5: heat}, alias={6: 0}, adds={0: hook, 1: mp},
                 cams={1: [1.3, 430, 780], 6: [1.1, 500, 940]}, line_adds={(4, 1): (kebira, None)}, beat_adds={5: (tag, [1.1, 500, 940])})


def scatter_heap(cx, base, n):
    """Points of a little heap of sand grains (base y, peak above cx)."""
    r = rnd(11)
    out = []
    for k in range(n * 3):
        x = cx + (r() - .5) * 150
        h = 70 * (1 - abs(x - cx) / 80)
        if h > 4:
            out.append((round(x, 1), round(base - r() * h, 1)))
        if len(out) >= n:
            break
    return out


def helix(x0, y0, x1, y1, at, n=16, amp=18, c1="#f2c98e", c2="#9fd0ff", w=3, dur=1.0):
    """A DNA double helix drawn as two crossing waves (with rungs) from (x0, y0) to (x1, y1)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    P = lambda t, ph: [round(x0 + ux * L * t + nx * amp * math.sin(t * n + ph), 1), round(y0 + uy * L * t + ny * amp * math.sin(t * n + ph), 1)]
    ts = [k / 40 for k in range(41)]
    out = [{"k": "line", "p": [P(t, 0) for t in ts], "c": c1, "w": w, "curve": True, "in": at, "fx": "draw", "dur": dur},
           {"k": "line", "p": [P(t, math.pi) for t in ts], "c": c2, "w": w, "curve": True, "in": at + .1, "fx": "draw", "dur": dur}]
    out += [{"k": "line", "p": [P(t, 0), P(t, math.pi)], "c": "#e9dccb", "w": 1.5, "op": .5, "keepop": True, "in": at + dur * .8} for t in [k / 10 + .05 for k in range(10)]]
    return out


def takarkori_m():
    """Takarkori as one continuous take (see mural.py): a green valley, the desert returns, a lineage's typos counted on its
    branches, an idea passed hand to hand, milk fat in a pot, and two people in a whole crowd."""
    import copy
    remix, I = _mur()
    ep = takarkori()
    W2 = "#f2c98e"
    # 0 · a rock shelter in a green Sahara: herders, cattle, a lake; two women (drawn alive); their DNA
    GY = 1100
    under = [[600, 622], [520, 652], [444, 702], [402, 780], [386, 880], [396, 980], [420, 1060], [440, GY]]
    face = [[0, 420], [200, 398], [380, 428], [520, 470], [604, 522], [632, 580]] + under + [[0, GY]]
    green = {"base": "sky", "tod": "day", "ground": GY, "groundc": "#6f8a4c", "sun": [820, 520, 30], "cam": [1.15, 520, 830], "els":
             [{"k": "poly", "p": under + [[590, GY], [632, 590]], "fill": "#3a2418", "c": "none", "w": 0, "op": .55, "in": -1},
              {"k": "poly", "p": face, "fill": "#7a5240", "c": "#d8a47a", "w": 2, "in": -1}] + [I.line([[30 + 60 * k, 470 + 9 * (k % 3)], [80 + 60 * k, 466 + 9 * (k % 3)]], -1, "#94654c", 2, draw=False) for k in range(7)] + [
              I.oval(790, 1170, 160, 34, LAKE, "#9fd0ff", 1.5, 1, -1)] +
             [{"k": "line", "p": [[x, GY + 4], [x + 5, GY - 16]], "c": "#a9c47c", "w": 2, "in": -1} for x in range(620, 990, 34)] +
             [I.line([[900, GY], [904, 930]], -1, "#3a2a1c", 8, draw=False), I.oval(905, 925, 80, 22, "#4f6a3a", at=-1)] +
             _t(cow(640, GY - 4, .55, 1.4, "#cbb8a0") + cow(760, GY - 10, .5, 1.8, "#e8dcc6", flip=True) + [I.person(835, GY, 110, 2.2, "#2a2018")] +
                [I.glow(475, 1000, 170, 3.4, .6, "lamp"), I.person(445, GY, 140, 3.6, W2), I.person(505, GY, 130, 3.9, W2)] +
                helix(475, 700, 475, 930, 9.0, n=14, amp=22), 1.58)}
    # 1 · the map: Takarkori; a green Sahara spreads around it; then the desert returns, dry air over the shelter
    v = View(-8, 20, 18, 37, (40, 330, 920, 900))
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") not in ("scale",) and not (e.get("k") == "line" and e.get("dash"))]
    tx, ty = v.p(10.333, 24.883)
    wash = [v.p(a_, b_) for a_, b_ in [(-6, 21), (0, 26), (8, 28.5), (16, 28), (20, 26.5), (20, 18), (-6, 18)]]
    mp = _t([I.glow(tx, ty, 90, 1.2, .8, "lamp"),
             {"k": "poly", "p": wash, "fill": "rgba(125,154,90,.5)", "c": "none", "w": 0, "curve": True, "in": 7.0, "dur": 1.6, "op": .9, "keepop": True},
             I.oval(tx + 30, ty + 14, 16, 8, LAKE, "#9fd0ff", 1, 1, 8.6), I.oval(tx - 70, ty + 60, 22, 9, LAKE, "#9fd0ff", 1, 1, 9.0),
             I.oval(tx + 120, ty + 90, 26, 10, LAKE, "#9fd0ff", 1, 1, 9.4)] + cow(tx - 40, ty + 30, .2, 10.4, "#e8dcc6") + cow(tx + 70, ty + 40, .2, 10.8, "#e8dcc6", flip=True), 1.57)
    dry = _t([{"k": "poly", "p": wash, "fill": "#3a2f24", "c": "none", "w": 0, "curve": True, "in": 1.0, "dur": 2.0},
              I.glow(tx, ty - 110, 160, 1.6, .8, "sun")] +
             [I.line([[tx - 40 + 40 * j + 10 * math.sin(k), ty - 30 - 14 * k] for k in range(7)], 4.4 + .3 * j, "#ffd9a0", 2.5, dur=.8, curve=True) for j in range(3)] +
             [I.line([[tx + dx, ty + dy], [tx + dx + 14, ty + dy + 10], [tx + dx + 6, ty + dy + 24], [tx + dx + 20, ty + dy + 34]], 2.4 + .1 * k, "#6a5640", 2.5, draw=False)
              for k, (dx, dy) in enumerate(((-120, 40), (-60, 90), (40, 70), (110, 30), (-150, -40), (150, -60)))] +
             [I.dot(tx, ty, 9, GOLD, 1.2), I.label(tx + 18, ty + 8, "Takarkori", 1.2, "#f5ecdc", 25, "start", st="lab"), I.glow(tx, ty, 50, 6.0, .7, "lamp")], 2.5)
    # 2 · their genomes, read; typos pile up on two branches; 50,000 years; and the branches never meet again
    BASES = ["#e8b87a", "#9fd0ff", "#8fd9b0", "#ff8a7a"]
    r3 = rnd(3)
    strip = [I.box(120 + 38 * k, 440, 30, 44, BASES[int(r3() * 4)], r=5, at=.8 + .15 * k, fx="pop") for k in range(20)]
    S = (170, 800); U = (840, 640); D = (840, 950)
    pt = lambda A, f: (A[0] * f + S[0] * (1 - f), A[1] * f + S[1] * (1 - f))
    def tick(A, f, at):
        x, y = pt(A, f); return I.line([[x - 6, y - 16], [x + 6, y + 16]], at, I.RED, 5, draw=False)
    genome = {"base": "dark", "cam": [1.05, 500, 760], "els": _t(strip +
        [I.line([[90, 800], [S[0], S[1]]], 6.2, "#cbbca8", 6, draw=False), I.dot(S[0], S[1], 10, "#e9dccb", 6.2),
         I.line([S, U], 6.6, W2, 6, dur=1.2), I.line([S, D], 6.8, "#cbbca8", 6, dur=1.2)] +
        [tick(U, f, 7.8 + 1.1 * k) for k, f in enumerate((.22, .45, .63, .84))] + [tick(D, f, 8.3 + 1.1 * k) for k, f in enumerate((.3, .52, .7, .9))] +
        [I.person(880, 648, 70, 8.6, W2), I.person(910, 652, 64, 8.8, W2)] + [I.person(870 + 30 * k, 958, 64, 8.8 + .1 * k, "#cbbca8") for k in range(2)] +
        [I.line([[S[0], 1080], [880, 1080]], 20.4, "#8c7152", 3, dur=.8), I.dot(S[0], 1080, 9, W2, 20.6), I.label(S[0] - 20, 1130, "50,000 years ago", 21.0, W2, 30, "start"),
         I.label(880, 1130, "7,000", 21.6, "#cbbca8", 30, "end")] +
        [I.arrow([[700, 760], [700, 870]], 25.4, I.BONE, 3, dur=.4, curve=False), I.arrow([[700, 870], [700, 760]], 25.4, I.BONE, 3, dur=.4, curve=False), I.glow(700, 815, 110, 25.6, .35, "lamp")], 2.5)}
    # 3 · the tree: a twig to Morocco, fifteen thousand years earlier
    twig = _t([I.line([[592, 830], [690, 840]], 2.0, I.BLUE, 5, dur=.5), I.glow(706, 820, 70, 2.4, .8), I.person(706, 852, 60, 2.4, I.BLUE)], 1.14)
    # 4 · herders mostly local; cattle and milk passed hand to hand, not a wave of newcomers; milk fat in a pot's clay
    xs = [170, 335, 500, 665, 830]
    ideas = {"base": "dark", "floor": 700, "cam": [1.05, 500, 920], "els": _t(
        [I.line([[100, 700], [900, 700]], .3, "#8c7152", 3, draw=False)] + [I.person(x, 700, 120, .8 + .2 * k, W2) for k, x in enumerate(xs)] +
        cow(xs[0], 560, .32, 4.0, "#e8dcc6") +
        sum([[I.arrow([[xs[k] + 30, 520], [(xs[k] + xs[k + 1]) / 2, 470], [xs[k + 1] - 30, 520]], 4.6 + .7 * k, I.AMBER, 3, dur=.5)] + cow(xs[k + 1], 560, .32, 5.0 + .7 * k, "#e8dcc6")
             for k in range(4)], []) +
        [I.person(130 + 44 * k, 960, 84, 8.0 + .08 * k, "#8a8178") for k in range(6)] + [I.arrow([[400, 900], [560, 880], [720, 900]], 8.4, "#8a8178", 3, "claimed", .8),
         I.strike(110, 975, 740, 830, 9.4, I.RED, 5)] +
        [{"k": "poly", "p": [[300, 1080], [460, 1080], [480, 1110], [500, 1200], [470, 1330], [400, 1370], [360, 1370], [290, 1330], [260, 1200], [280, 1110]], "fill": "#9a6a48",
          "c": "#d8a878", "w": 3, "in": 10.2, "fx": "rise"}, I.glow(380, 1200, 110, 11.2, .7, "lamp"), I.oval(380, 1200, 34, 20, "#fff6e8", op=.9, at=11.2)] +
        [I.dot(x, y, 4, "#fff6e8", 14.4 + .05 * k, op=.8) for k, (x, y) in enumerate(I.scatter(18, 268, 300, 1120, 1320, 9) + I.scatter(18, 462, 494, 1120, 1320, 10))] +
        [I.box(620, 1220, 240, 90, "#8a5d33", "#c9a06a", 2, 10, 16.6, fx="pop"), I.oval(720, 1250, 50, 18, "#c9a06a", op=.7, at=17.4)] +
        [I.ring(480, 1230, 70, 19.6, I.BLUE, 4, dur=.6), I.line([[530, 1280], [580, 1330]], 19.8, I.BLUE, 8, draw=False)], 1.90)}
    # 5 · two people are not a whole people; teeth and culture elsewhere; people coming and going
    crowd = []
    for row in range(5):
        for j in range(8):
            if (row, j) in ((2, 3), (2, 4)):
                continue
            crowd.append(I.person(185 + 90 * j + 20 * (row % 2), 640 + 85 * row, 64, 1.4 + .03 * (row * 8 + j), "#8a8178"))
    whole = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        [I.person(185 + 90 * 3, 810, 64, .4, W2), I.person(185 + 90 * 4, 810, 64, .5, W2), I.glow(500, 780, 130, .5, .55, "lamp")] + crowd +
        [I.tooth(330, 1210, 60, 9.6), I.label(330, 1290, "teeth", 9.8, "#e9dccb", 30),
         {"k": "poly", "p": [[640, 1180], [720, 1170], [740, 1220], [690, 1250], [630, 1230]], "fill": "#9a6a48", "c": "#d8a878", "w": 2, "in": 10.4, "fx": "pop"},
         I.label(690, 1290, "culture", 10.6, "#e9dccb", 30)] +
        [I.arrow([[60, 1100], [300, 1060], [520, 1100]], 11.6, I.BLUE, 3, "inferred", .9), I.arrow([[940, 1110], [700, 1150], [480, 1110]], 12.6, I.BLUE, 3, "inferred", .9)], 1.77)}
    # 6 · the verdict: more people, waiting for their genomes
    tag = _t([I.person(560 + 70 * k, 1300 + 12 * (k % 2), 126, 9.4 + .15 * k, "#5e6a76") for k in range(5)], 1.82)
    return remix(ep, scenes={0: green, 1: s1, 2: genome, 4: ideas, 5: whole}, alias={6: 0}, adds={1: mp, 3: twig},
                 cams={6: [1.12, 500, 960]}, line_adds={(1, 1): (dry, [1.25, 560, 800])}, beat_adds={5: (tag, [1.12, 500, 960])})


def ufo(x, y, at, c="#c9c1ee", s=1.0):
    """A flying saucer, drawn dotted: the claim, not a thing."""
    return [{"k": "poly", "p": I_ellipse(x, y, 90 * s, 22 * s), "fill": "none", "c": c, "w": 3, "style": "claimed", "in": at},
            {"k": "poly", "p": I_ellipse(x, y - 22 * s, 40 * s, 26 * s, 18, 180, 360)[:-1] + [[x + 40 * s, y - 22 * s]], "fill": "none", "c": c, "w": 3, "style": "claimed", "in": at + .2}]


def I_ellipse(*a, **k):
    from illus import ellipse
    return ellipse(*a, **k)


def tassili_m():
    """Tassili as one continuous take (see mural.py): a five-metre figure and a dotted saucer, fifteen thousand images on a
    wall, a helmet drawn on a face that never had one, a painting sponged to death, and what the blank heads more likely are."""
    import copy
    remix, I = _mur()
    ep = tassili()
    OC = "#b0643c"
    # 0 · the giant, to scale (a person is 1.7 m: the figure, head to foot, about 5 m); the 'Martian god', drawn dotted
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] = [e for e in s0["els"] if e.get("k") not in ("label", "person")]
    hook = _t([I.line([[175, 1240], [175, 597]], 4.6, I.BONE, 2.5, dur=.7), I.line([[160, 597], [190, 597]], 4.6, I.BONE, 2.5, draw=False),
               I.line([[160, 1240], [190, 1240]], 4.6, I.BONE, 2.5, draw=False), I.label(160, 930, "5 m", 5.2, I.BONE, 34, "end"),
               I.person(800, 1240, 219, 5.6, "#1a1511")] + ufo(760, 420, 8.0) +
              [I.line([[730, 440], [600, 620]], 12.6, I.LILAC, 2, "claimed", .6), I.line([[790, 440], [720, 640]], 12.6, I.LILAC, 2, "claimed", .6)], 1.52)
    # 1 · the map: the plateau, its shelters, its paintings
    v = View(0, 16, 18, 32, (40, 330, 920, 900))
    plat = [v.p(a_, b_) for a_, b_ in [(5.8, 26.9), (7.5, 26.9), (9.5, 25.8), (11.2, 24.6), (11.0, 23.8), (9.6, 24.2), (7.8, 25.2), (6.0, 26.0)]]
    r5 = rnd(21)
    marks = []
    for k in range(26):
        f = r5() * .8
        lon, lat = 6.3 + 4.2 * f, 26.4 - 2.0 * f + (r5() - .5) * .9
        marks.append(v.p(lon, lat))
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") != "scale"]
    mp = _t([{"k": "poly", "p": plat, "fill": "rgba(176,100,60,.35)", "c": "#e8a070", "w": 2.5, "curve": True, "in": 2.0, "fx": "draw", "dur": 1.4}] +
            [I.dot(x, y, 3.5, "#ffb27a", 6.4 + .04 * k) for k, (x, y) in enumerate(marks)], 2.45)
    # 2 · fifteen thousand images: 150 marks of a hundred each; a minute each, eight hours a day: about a month
    wall = [I.box(70, 430, 860, 560, "#6e5040", "#a88b66", 2, 14, .2)]
    r9 = rnd(9)
    pos = sorted([(round(110 + (k % 15) * 54 + r9() * 18, 1), round(480 + (k // 15) * 50 + r9() * 14, 1), r9()) for k in range(150)], key=lambda q: q[2])
    figs = []
    for k, (x, y, q) in enumerate(pos):
        at = .8 + .022 * k
        if k % 3 == 0:
            figs.append(I.person(x, y + 16, 26, at, "#e0a070"))
        elif k % 3 == 1:
            figs.append(I.dot(x, y + 4, 6, "#f0d8b0", at))
        else:
            figs.append({"k": "poly", "p": [[x - 12, y + 8], [x + 10, y + 6], [x + 14, y - 2], [x + 6, y + 14], [x - 10, y + 14]], "fill": "#d8b090", "c": "none", "w": 0, "in": at, "fx": "pop"})
    clock = [I.ring(230, 1200, 80, 5.8, I.BONE, 4, dur=.6), I.line([[230, 1200], [230, 1140]], 6.2, I.BONE, 5, draw=False), I.line([[230, 1200], [272, 1222]], 6.4, I.AMBER, 4, draw=False),
             I.label(230, 1330, "1 a minute", 6.6, I.BONE, 30)]
    cal = [I.box(450 + 62 * (d % 7), 1100 + 56 * (d // 7), 52, 46, I.AMBER, r=6, at=8.4 + .1 * d, fx="pop", op=.85) for d in range(31)]
    count = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(wall + figs + [I.label(500, 1040, "each mark: 100 images", 2.0, "#cbbca8", 28)] + clock + cal +
                                                            [I.label(665, 1420, "about a month", 11.6, I.AMBER, 34, st="serif")], 2.5)}
    # 4 · the Round Heads: no eyes, no nose, no mouth; a helmet drawn on in 1968; unlike the art that came later
    eye = lambda x, y, at: [{"k": "poly", "p": I_ellipse(x, y, 34, 16, 20)[:-1], "fill": "none", "c": I.BONE, "w": 3, "in": at}, I.dot(x, y, 7, I.BONE, at)]
    heads = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        [I.box(60, 460, 880, 960, "#6e5040", r=14, at=.1)] + roundhead(330, 1340, 620, fill=OC, i=.5) + [I.glow(330, 760, 160, 1.0, .35, "lamp")] +
        eye(760, 620, 4.0) + [I.line([[760, 680], [748, 740], [770, 744]], 4.6, I.BONE, 3, draw=False),
                              {"k": "line", "p": I_ellipse(760, 770, 34, 14, 12, 20, 160), "c": I.BONE, "w": 3, "in": 5.2, "curve": True}] +
        [I.strike(700, 800, 820, 580, 6.2, I.RED, 5)] +
        [I.ring(330, 768, 128, 8.0, I.LILAC, 4, "claimed"), {"k": "line", "p": I_ellipse(330, 790, 92, 52, 18, 200, 340), "c": I.LILAC, "w": 4, "style": "claimed", "curve": True, "in": 8.6},
         I.line([[330, 640], [330, 560]], 9.0, I.LILAC, 3, "claimed", .4), I.dot(330, 552, 9, I.LILAC, 9.3), I.label(520, 560, "1968", 9.4, I.LILAC, 34, "start")] +
        cow(700, 1330, .62, 12.2, "#efe6d2") + [I.person(860, 1330, 150, 12.6, "#efe6d2"), I.label(760, 1395, "later art", 13.0, "#e9dccb", 30)], 1.67)}
    # 3 · the copyists: water and a sponge; brighter for a moment, then faded; a published copy with a figure that isn't there
    copies = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        [I.box(60, 460, 520, 760, "#6e5040", r=14, at=.1)] + roundhead(320, 1150, 520, fill="#9a5434", i=.4) +
        [I.box(620, 520, 300, 420, "#efe3c8", "#8a7a66", 2, 6, 3.4, fx="pop")] + roundhead(735, 890, 300, fill="#d0602c", c="#d0602c", i=3.8) +
        [I.dot(x, y, 9, "#9fd0ff", 5.0 + .08 * k, op=.85) for k, (x, y) in enumerate(I.scatter(14, 220, 420, 620, 1000, 4))] +
        [I.box(420, 880, 110, 60, "#e8d070", "#b8a040", 2, 18, 6.6, fx="pop"), I.arrow([[470, 860], [380, 760], [300, 820], [240, 760]], 7.0, "#e8d070", 3, dur=1.0)] +
        roundhead(320, 1150, 520, fill="#e2763c", c="#ffd0a0", i=10.2) + [I.glow(320, 820, 220, 10.2, .5, "lamp")] +
        [I.box(70, 470, 500, 740, "#6e5040", r=12, at=12.0, op=.78, dur=1.6)] +
        roundhead(860, 890, 220, fill="#d0602c", c="#d0602c", i=14.6) +
        [I.box(800, 560, 112, 350, "none", I.RED, 3, 6, 15.2, style="inferred")] + I.question(856, 1010, 15.8, 64), 1.52)}
    # 5 · what they are: dated indirectly (layers; paintings over paintings, like posters); 9,500-7,500 years ago;
    #     masks, body paint, or spirit beings; and a living tradition that credits some to spirits
    A = lambda yago: 140 + 720 * (12000 - yago) / 12000
    what = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(I.question(500, 540, .4, 100) +
        [I.box(110, 820 - 40 * (3 - k), 300, 40, c, r=2, at=7.2 + .4 * k, fx="fill") for k, c in enumerate(("#5a4632", "#7a6248", "#a8977c", "#8a7050"))] +
        [I.box(560, 640, 330, 220, "#6e5040", r=10, at=9.6)] + roundhead(650, 850, 200, fill="#7a4a30", op=.8, i=9.8) +
        cow(780, 840, .7, 11.2, "#efe6d2") + [I.label(725, 900, "painted over", 11.6, "#e9dccb", 28)] +
        [I.line([[A(12000), 1020], [A(0), 1020]], 14.4, "#8c7152", 3, dur=.6),
         {"k": "rect", "x": A(9500), "y": 1008, "w": A(7500) - A(9500), "h": 24, "r": 12, "fill": OC, "c": "none", "sw": 0, "in": 15.0, "fx": "pop"},
         I.label(A(9500), 1072, "9,500", 15.4, "#e8a070", 28), I.label(A(7500) + 10, 1072, "7,500", 15.6, "#e8a070", 28), I.label(A(0), 1072, "today", 15.8, "#cbbca8", 28, "end")] +
        roundhead(200, 1330, 220, fill=OC, i=22.4) + [{"k": "poly", "p": I_ellipse(200, 1150, 42, 30, 16)[:-1], "fill": "#e8dcc2", "c": "none", "w": 0, "in": 23.2, "fx": "pop"},
                                                     I.dot(186, 1146, 5, "#2a2018", 23.3), I.dot(214, 1146, 5, "#2a2018", 23.3)] +
        roundhead(470, 1330, 220, fill=OC, i=22.6) + [I.line([[450 + 14 * j, 1220], [450 + 14 * j, 1310]], 24.4 + .1 * j, "#f5ecdc", 4, draw=False) for j in range(4)] +
        roundhead(740, 1330, 220, fill="#e8c8a0", op=.45, i=25.6) + [I.glow(740, 1240, 150, 25.8, .7, "lamp")] +
        [I.glow(890, 1330, 90, 27.6, .7, "lamp"), I.person(890, 1400, 120, 27.8, "#e8d6b8")], 1.83)}
    tag = _t([I.strike(650, 470, 870, 380, 2.0, I.RED, 6), I.glow(440, 900, 260, 6.6, .45, "lamp")], 1.55)
    return remix(ep, scenes={0: s0, 1: s1, 2: count, 3: copies, 4: heads, 5: what}, alias={6: 0}, adds={0: hook, 1: mp},
                 cams={1: [1.6, 530, 760], 6: [1.12, 500, 960]}, beat_adds={5: (tag, [1.12, 500, 960])})


CASPIAN = [(46.7, 44.9), (47.6, 45.9), (49.2, 46.6), (51.8, 47.0), (53.2, 46.4), (53.1, 45.3), (51.3, 44.6), (50.3, 44.4), (51.2, 43.0), (52.6, 42.2),
           (52.9, 41.0), (53.0, 40.0), (53.9, 39.0), (54.0, 37.4), (53.0, 36.9), (51.0, 36.8), (49.6, 37.5), (48.9, 38.4), (49.0, 39.5), (49.5, 40.3),
           (48.6, 41.8), (47.6, 42.8), (47.2, 43.8)]


def _scaled(P, k):
    cx, cy = sum(a for a, b in P) / len(P), sum(b for a, b in P) / len(P)
    return [(round(cx + (a - cx) * k, 3), round(cy + (b - cy) * k, 3)) for a, b in P]


MEGA_A = _scaled(MEGA, .814)            # the schematic outline, scaled to the c. 360,000 km² the film states (the raw outline encloses c. 540,000)


def switchoff_m():
    """The end of the green Sahara as one continuous take (see mural.py): a lake the size of the Caspian, the monsoon pushed
    north by a wobbling Earth, ten times the rain, mud read like a diary (a cliff here, a ramp there), the lake shrinking to
    the Bodélé and its dust, and a map where the answer depends on where you stand."""
    import copy
    remix, I = _mur()
    ep = switchoff()
    v = View(6, 26, 6, 24, (40, 520, 920, 760))
    w = View(-20, 26, 8, 32, (40, 330, 920, 900))
    # 0 · Lake Mega-Chad, with the Caspian Sea beside it at the same scale
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] = [e for e in s0["els"] if e.get("k") != "label"]
    for e in s0["els"]:
        if e.get("k") == "poly" and str(e.get("fill", "")).startswith("rgba(79,127,150"):
            e["p"] = [v.p(a_, b_) for a_, b_ in MEGA_A]
    pins0 = [copy.deepcopy(e) for e in s0["els"] if e.get("k") == "pin"]
    k15 = math.cos(math.radians(15.5))
    casp = [v.p(22.6 + (a_ - 50.5) * math.cos(math.radians(42)) / k15, 15.6 + (b_ - 42)) for a_, b_ in _scaled(CASPIAN, .974)]
    hook = _t([{"k": "poly", "p": casp, "fill": "rgba(159,208,255,.12)", "c": "#9fd0ff", "w": 2.5, "style": "inferred", "in": 4.2, "curve": True},
               I.label(sum(p_[0] for p_ in casp) / len(casp), max(p_[1] for p_ in casp) + 46, "Caspian Sea", 4.6, "#9fd0ff", 30)], 1.22)
    # 1 · the wide map: green spreads; the monsoon blows in from the south; the lakes fill
    wash = [w.p(a_, b_) for a_, b_ in [(-17, 16), (-16, 21), (-12, 27), (-5, 30), (5, 31), (15, 30.5), (25, 29), (26, 22), (26, 15), (15, 13), (0, 14), (-10, 14)]]
    mp = _t([{"k": "poly", "p": wash, "fill": "rgba(125,154,90,.45)", "c": "none", "w": 0, "curve": True, "in": 1.6, "dur": 1.6, "op": .9, "keepop": True}] +
            [I.arrow([w.p(lo, 8.4), w.p(lo + 1.5, 13.5), w.p(lo + 1, 19)], 6.0 + .25 * k, I.BLUE, 4, dur=1.0) for k, lo in enumerate((-12, -4, 4, 12, 20))] +
            [{"k": "poly", "p": [w.p(a_, b_) for a_, b_ in MEGA_A], "fill": "rgba(79,127,150,.75)", "c": "#9fd0ff", "w": 1.5, "curve": True, "in": 10.4, "fx": "pop"}], 1.62)
    # 2 · why: the wobble; northern summers get more sun; warm land draws in wet ocean air; ten times the rain
    E = (740, 480)
    tip = (E[0] + 120 * math.sin(math.radians(23)), E[1] - 120 * math.cos(math.radians(23)))
    GY = 940
    orbit = {"base": "dark", "stars": 60, "cam": [1.05, 500, 860], "els": _t(
        [{"k": "line", "p": I_ellipse(470, 480, 270, 70, 60), "c": "#8c7152", "w": 2, "style": "inferred", "in": .8, "curve": True},
         I.glow(400, 480, 160, .4, .9, "sun"), I.dot(400, 480, 44, "#ffe2a8", .4),
         I.oval(E[0], E[1], 70, 70, "#2f5f7a", "#9fd0ff", 2, 1, 1.4), I.oval(E[0] - 10, E[1] - 26, 34, 18, "#7d9a5a", at=1.5),
         I.line([[2 * E[0] - tip[0], 2 * E[1] - tip[1]], list(tip)], 1.8, I.BONE, 3),
         {"k": "line", "p": I_ellipse(E[0], tip[1], tip[0] - E[0], 16, 40), "c": I.AU, "w": 3, "style": "inferred", "curve": True, "in": 2.4, "fx": "draw", "dur": 3.0}] +
        [I.arrow([[460, 446 + 18 * j], [650, 438 + 14 * j]], 5.0 + .2 * j, I.AU, 3, dur=.6, curve=False) for j in range(3)] + [I.glow(E[0] - 20, E[1] - 30, 70, 5.8, .8, "lamp")] +
        [I.box(100, GY, 330, 180, "#2a5a78", r=0, at=7.2), I.box(430, GY, 470, 180, "#a88a5c", r=0, at=7.2), I.line([[100, GY], [900, GY]], 7.2, "#e9dccb", 2, draw=False),
         I.label(265, GY + 60, "ocean", 7.4, "#cfe6ff", 28), I.label(665, GY + 60, "land", 7.4, "#2a2018", 28, halo=False),
         I.glow(665, GY - 10, 200, 8.2, .6, "red")] +
        [I.arrow([[600 + 70 * j, GY - 20], [610 + 70 * j, GY - 110], [600 + 70 * j, GY - 170]], 9.4 + .15 * j, "#ffb27a", 3, dur=.7) for j in range(3)] +
        [I.arrow([[150, GY - 40 - 30 * j], [330, GY - 60 - 30 * j], [520, GY - 50 - 30 * j]], 11.4 + .2 * j, I.BLUE, 4, dur=.8) for j in range(2)] +
        [I.oval(690, GY - 230, 120, 40, "#cfd8e0", at=13.2, op=.95), I.oval(620, GY - 220, 70, 32, "#cfd8e0", at=13.3, op=.95), I.oval(760, GY - 220, 70, 30, "#cfd8e0", at=13.4, op=.95)] +
        [I.line([[620 + 30 * j, GY - 180], [608 + 30 * j, GY - 120]], 14.0 + .05 * j, I.BLUE, 3, draw=False) for j in range(6)] +
        [I.box(220, 1370 - 22, 90, 22, I.BLUE, r=3, at=15.6, fx="pop"), I.label(265, 1414, "today", 15.8, "#cfe6ff", 30)] +
        [I.box(560, 1370 - 22 * (k + 1), 90, 20, I.BLUE, r=3, at=16.2 + .2 * k, fx="pop") for k in range(10)] +
        [I.label(605, 1414, "then", 16.4, "#cfe6ff", 30), I.label(680, 1260, "× 10", 18.4, I.BLUE, 44, "start", st="serif")], 2.5)}
    # 3 · how we know: mud settles like pages; a core is drilled and read; off Mauritania a cliff, in Chad a ramp
    X = lambda yago: 170 + 680 * (8000 - yago) / 5000
    WET, DRY = 980, 1290
    rec = {"base": "dark", "cam": [1.05, 500, 870], "els": _t(
        [I.box(110, 380, 420, 190, "#2a5a78", r=6, at=.3)] +
        [I.box(110, 680 - 22 * (k + 1), 420, 22, c, r=0, at=4.4 + .55 * k, fx="fill") for k, c in enumerate(("#6f5a44", "#a8977c", "#7a6248", "#b9ab94", "#5a4632", "#8a7050"))] +
        [I.box(110, 680, 420, 60, "#4a3a2c", r=0, at=.3)] +
        [I.box(300, 330, 40, 400, "none", I.BONE, 3, 6, 11.8, fx="draw"), I.arrow([[320, 300], [320, 360]], 12.0, I.BONE, 3, dur=.4, curve=False)] +
        [I.box(640, 380, 70, 320, "#3a2e24", I.BONE, 2.5, 30, 13.6, fx="pop")] +
        [I.box(646, 690 - 50 * (k + 1), 58, 46, c, r=4, at=14.0 + .3 * k, fx="pop") for k, c in enumerate(("#8a7050", "#5a4632", "#b9ab94", "#7a6248", "#a8977c", "#6f5a44"))] +
        [I.ring(780, 560, 46, 16.0, I.AMBER, 3, dur=.5), I.line([[812, 592], [850, 630]], 16.2, I.AMBER, 7, draw=False)] +
        [I.line([[X(8000), DRY + 40], [X(3000), DRY + 40]], 18.0, "#8c7152", 3, dur=.6), I.label(X(8000), DRY + 90, "8,000 years ago", 18.2, "#cbbca8", 28, "start"),
         I.label(X(3000), DRY + 90, "3,000", 18.2, "#cbbca8", 28, "end"),
         I.label(X(8000) - 14, WET + 10, "wet", 18.4, "#8fd9b0", 30, "end"), I.label(X(8000) - 14, DRY + 10, "dry", 18.4, "#e8b87a", 30, "end"),
         I.line([[X(8000), WET], [X(5560), WET], [X(5440), DRY], [X(3000), DRY]], 20.2, I.RED, 5, dur=2.4), I.label(X(5500) + 30, WET - 30, "off Mauritania", 21.0, I.RED, 30, "start"),
         I.dot(X(5500), DRY + 40, 9, I.RED, 23.0), I.label(X(5500), DRY + 140, "5,500", 23.2, I.RED, 28),
         I.line([[X(8000), WET + 10], [X(6000), WET + 20], [X(4500), WET + 160], [X(3000), DRY - 10]], 28.4, I.GREEN, 5, dur=3.0, curve=True),
         I.label(X(3000), WET + 120, "a lake in Chad", 29.4, I.GREEN, 30, "end")], 2.46)}
    # 4 (on 0) · Mega-Chad falls; the Bodélé holds on; then it dries, and its dust blows west
    bx_, by_ = v.p(17.6, 17.1)
    shrink = _t([{"k": "poly", "p": [v.p(a_, b_) for a_, b_ in MEGA_A], "fill": "#3a2f24", "c": "none", "w": 0, "curve": True, "in": 1.0, "dur": 1.8},
                 {"k": "poly", "p": [v.p(a_, b_) for a_, b_ in CHAD], "fill": LAKE, "c": "#9fd0ff", "w": 1.5, "in": 1.2},
                 I.oval(bx_, by_, 52, 22, LAKE, "#9fd0ff", 1.5, 1, 1.4)] +
                [dict(e, **{"in": 1.6 + .1 * k}) for k, e in enumerate(pins0)] +
                [I.oval(bx_, by_, 54, 24, "#3a2f24", at=9.6), I.glow(bx_ - 30, by_ + 12, 60, 10.0, .6, "red")] +
                [dict(e, **{"in": 9.8}) for e in pins0 if "Bod" in e.get("t", "")] +
                [I.arrow([[bx_ - 20, by_ - 6 + 14 * j], [bx_ - 160, by_ - 40 + 30 * j], [bx_ - 320, by_ - 30 + 46 * j]], 10.8 + .25 * j, "#e8b87a", 4, "inferred", 1.2) for j in range(3)], 1.19)
    # 5 (on 1) · sudden here, gradual there; a single catastrophe: struck
    mx, my = w.p(-18.58, 20.75); yx, yy = w.p(20.52, 19.05)
    where = _t([I.line([[mx + 24, my + 34], [mx + 62, my + 34], [mx + 68, my + 90], [mx + 106, my + 90]], 2.6, I.RED, 5, dur=.6), I.glow(mx + 64, my + 62, 70, 2.8, .7, "red"),
                I.line([[yx + 8, yy + 30], [yx + 86, yy + 90]], 3.8, I.GREEN, 5, dur=.6), I.glow(yx + 46, yy + 60, 70, 4.0, .5)] +
               [I.arrow([[880, 380], [740, 480], [600, 640]], 6.4, I.LILAC, 4, "claimed", .8), I.ring(585, 660, 44, 7.0, I.LILAC, 3, "claimed"),
                I.strike(520, 720, 900, 360, 9.2, I.RED, 6)], 1.12)
    # 6 (on 1) · and people? herders sped the end, or slowed it
    hx, hy = w.p(4, 15.2)
    ppl = _t(cow(hx - 40, hy, .3, 1.2, "#e8dcc6") + cow(hx + 40, hy + 6, .28, 1.4, "#cbb8a0", flip=True) + [I.person(hx, hy + 4, 60, 1.6, "#e8d6b8")] +
             [I.line([[hx - 160, hy + 70], [hx + 160, hy + 70]], 2.4, "#7d9a5a", 10, dur=.6), I.dot(hx + 70, hy + 70, 11, I.BONE, 2.6),
              I.arrow([[hx + 64, hy + 104], [hx - 40, hy + 104]], 3.6, I.RED, 4, dur=.5, curve=False), I.label(hx - 50, hy + 150, "sooner?", 4.0, I.RED, 28),
              I.arrow([[hx + 76, hy + 104], [hx + 180, hy + 104]], 6.0, I.GREEN, 4, dur=.5, curve=False), I.label(hx + 190, hy + 150, "later?", 6.4, I.GREEN, 28)], 1.44)
    verdict = _t([I.glow(mx + 64, my + 62, 110, 13.8, .8, "red"), I.glow(yx + 46, yy + 60, 110, 14.2, .8)], 1.0)
    mcx, mcy = v.p(15.8, 15.2)
    return remix(ep, scenes={0: s0, 2: orbit, 3: rec}, alias={4: 0, 5: 1, 6: 1}, adds={0: hook, 1: mp},
                 cams={0: [1.55, 590, 880], 1: [1, 500, 780], 4: [1.6, 560, 880], 5: [1, 500, 780], 6: [1.1, 470, 790]},
                 beat_adds={3: (shrink, [1.6, 560, 880]), 4: (where, [1, 500, 780]), 5: (verdict, [1.1, 470, 790])}, line_adds={(4, 1): (ppl, [1.05, 500, 800])})


def fish(x, y, s=1.0, at=0, c="#cfe6ff"):
    return [I_oval(x, y, 30 * s, 12 * s, c, at), {"k": "poly", "p": [[x - 28 * s, y], [x - 48 * s, y - 12 * s], [x - 48 * s, y + 12 * s]], "fill": c, "c": "none", "w": 0, "in": at}]


def hippo(x, y, s=1.0, at=0, c="#9a8a96"):
    return [I_oval(x, y - 34 * s, 62 * s, 32 * s, c, at), I_oval(x + 64 * s, y - 40 * s, 30 * s, 20 * s, c, at),
            {"k": "line", "p": [[x - 36 * s, y - 10 * s], [x - 36 * s, y]], "c": c, "w": 14 * s, "in": at}, {"k": "line", "p": [[x + 30 * s, y - 10 * s], [x + 30 * s, y]], "c": c, "w": 14 * s, "in": at},
            I_oval(x + 56 * s, y - 60 * s, 6 * s, 6 * s, c, at)]


def croc(x, y, s=1.0, at=0, c="#7d9a5a"):
    body = [[x - 110 * s, y], [x - 40 * s, y - 14 * s], [x + 40 * s, y - 16 * s], [x + 70 * s, y - 10 * s], [x + 120 * s, y - 6 * s], [x + 120 * s, y + 2 * s], [x + 60 * s, y + 4 * s],
            [x + 30 * s, y + 10 * s], [x - 40 * s, y + 8 * s]]
    return [{"k": "poly", "p": body, "fill": c, "c": "none", "w": 0, "in": at}] + \
           [{"k": "line", "p": [[x + dx * s, y + 6 * s], [x + (dx - 6) * s, y + 20 * s]], "c": c, "w": 5 * s, "in": at} for dx in (-20, 40)]


def I_oval(x, y, rx, ry, c, at):
    from illus import oval
    return oval(x, y, rx, ry, c, at=at)


def gobero_m():
    """Gobero as one continuous take (see mural.py): two hundred graves beside a lake deep enough for hippos, a lake that fills,
    empties and fills again, an embrace drawn only as light, pollen like signatures, and teeth that blur two peoples into one."""
    import copy
    remix, I = _mur()
    ep = gobero()
    s0 = copy.deepcopy(ep["shots"][0])
    for e in s0["els"]:
        if e.get("k") == "iso":
            e["items"] = [it for it in e["items"] if it.get("t") != "label"]
    hook = _t([I.glow(500, 1000, 260, 10.2, .45, "lamp")], 1.06)
    # 1 · the map: Gobero; the lake that vanished
    v = View(2, 16, 10, 24, (40, 330, 920, 900))
    gx_, gy_ = v.p(9.52, 17.08)
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") != "scale"]
    mp = _t([I.glow(gx_, gy_, 80, 1.0, .8, "lamp"), I.ring(gx_, gy_, 46, 13.2, I.BLUE, 3, "inferred")], 1.86)
    # 2 · two hundred graves; fish, hippos, crocodiles; deep water all year; a lake up to 3 km wide
    lake = [[560, 520], [700, 470], [860, 500], [930, 640], [920, 860], [880, 1040], [760, 1110], [620, 1080], [560, 940], [540, 760]]
    r2 = rnd(8)
    gp = []
    while len(gp) < 200:
        x, y = 90 + r2() * 440, 560 + r2() * 600
        if ((x - 320) / 220) ** 2 + ((y - 860) / 290) ** 2 < 1 and all(abs(x - a_) > 14 or abs(y - b_) > 9 for a_, b_ in gp[-40:]):
            gp.append((round(x, 1), round(y, 1)))
    graves = [I.oval(x, y, 8, 5, "#cbbca8", at=.3 + .0065 * k, fx="pop") for k, (x, y) in enumerate(gp)]
    shore = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        [{"k": "poly", "p": lake, "fill": LAKE, "c": "#9fd0ff", "w": 2, "curve": True, "in": .1}] + graves +
        fish(700, 640, 1.2, 2.4) + fish(800, 600, .9, 2.6) + hippo(720, 860, 1.0, 3.4) + croc(730, 1000, 1.0, 4.2) +
        [{"k": "poly", "p": [[540, 1200], [940, 1200], [880, 1320], [600, 1320]], "fill": LAKE, "c": "#9fd0ff", "w": 2, "in": 5.8, "fx": "fill"},
         I.line([[500, 1200], [980, 1200]], 5.8, "#8c7152", 3, draw=False)] + hippo(740, 1300, .7, 6.4) +
        [I.arrow([[600, 1210], [600, 1312]], 6.8, I.BONE, 3, dur=.4, curve=False), I.label(586, 1270, "deep", 7.0, I.BONE, 30, "end")] +
        [I.line([[548, 450], [930, 450]], 10.4, I.BONE, 3, dur=.6), I.line([[548, 434], [548, 466]], 10.4, I.BONE, 3, draw=False),
         I.line([[930, 434], [930, 466]], 10.4, I.BONE, 3, draw=False), I.label(740, 420, "3 km", 10.8, I.BONE, 32)], 2.5)}
    # 4 · the lake fills (Kiffian, harpoons), empties (a thousand empty years), fills again (Tenerian, cattle)
    X = lambda y: 120 + 760 * (y + 8000) / 6000
    AX = 1120
    level = {"base": "dark", "cam": [1.2, 500, 990], "els": _t(
        [I.line([[100, AX], [900, AX]], .2, "#8c7152", 3, dur=.8), I.label(X(-7700), AX + 50, "Kiffian", .8, I.BLUE, 32)] +
        [I.box(X(-7700), AX - 160, X(-6200) - X(-7700), 160, LAKE, r=4, at=3.8, fx="fill", dur=1.2), I.label(X(-7700), AX + 96, "7700 BCE", 4.4, "#cbbca8", 28)] +
        [I.oval(X(-7600) + 22 * k, AX - 186, 8, 5, "#cbbca8", at=2.2 + .1 * k) for k in range(8)] +
        [I.person(X(-6950) - 20, AX - 210, 110, 5.2, "#e8d6b8"), I.line([[X(-6950), AX - 300], [X(-6950) + 70, AX - 250]], 5.6, "#e8d6b8", 4, draw=False),
         I.line([[X(-6950) + 54, AX - 262], [X(-6950) + 62, AX - 248]], 5.6, "#e8d6b8", 3, draw=False)] + fish(X(-6950) + 30, AX - 80, 1.0, 6.0) +
        [I.line([[X(-6200) + 10 + 22 * k, AX - 4], [X(-6200) + 20 + 22 * k, AX - 16], [X(-6200) + 28 + 22 * k, AX - 2]], 8.4 + .08 * k, "#a88a5c", 3, draw=False) for k in range(5)] +
        [I.label((X(-6200) + X(-5200)) / 2, AX + 50, "dry", 8.8, "#e8b87a", 32),
         I.arrow([[X(-6200) + 6, AX - 260], [(X(-6200) + X(-5200)) / 2, AX - 300], [X(-5200) - 6, AX - 260]], 12.4, I.BONE, 3, dur=.8),
         I.label((X(-6200) + X(-5200)) / 2, AX - 320, "1,000 years", 12.8, I.BONE, 30)] +
        [I.box(X(-5200), AX - 160, X(-2500) - X(-5200), 160, LAKE, r=4, at=16.2, fx="fill", dur=1.2)] +
        [I.oval(X(-5000) + 22 * k, AX - 186, 8, 5, "#e8c88a", at=17.4 + .1 * k) for k in range(12)] +
        cow(X(-3700) + 40, AX - 200, .55, 21.6, "#e8dcc6") + [I.person(X(-3700) - 60, AX - 200, 110, 21.8, "#f2c98e"), I.label(X(-3850), AX + 50, "Tenerian", 22.2, I.AU, 32)], 1.74)}
    # 3 · the embrace, drawn only as light; pollen grains, each with its shape; flowers in the grave
    spike = lambda x, y, r, at: [I.oval(x, y, r, r, "#e8d070", at=at)] + [I.line([[x + r * math.cos(t), y + r * math.sin(t)], [x + (r + 9) * math.cos(t), y + (r + 9) * math.sin(t)]], at, "#e8d070", 3, draw=False)
                                                                       for t in [k * math.pi / 6 for k in range(12)]]
    rf = rnd(12)
    flowers = [I.dot(round(330 + rf() * 340, 1), round(850 + rf() * 210, 1), 10, ["#e8a0b8", "#f0d060", "#ffffff"][k % 3], 10.8 + .08 * k) for k in range(18)]
    embrace = {"base": "dark", "cam": [1.05, 500, 880], "els": _t(
        [I.box(300, 820, 400, 270, "#3a2b1f", "#e9dccb", 2.5, 60, .4, fx="draw")] +
        [I.glow(470, 950, 150, 1.0, .85, "lamp"), I.glow(560, 930, 95, 1.4, .85, "lamp"), I.glow(545, 1005, 90, 1.7, .85, "lamp"), I.label(500, 1150, "c. 3300 BCE", 2.2, "#cbbca8", 28)] +
        [I.ring(730, 520, 140, 3.6, I.BONE, 3, dur=.6), I.line([[630, 620], [560, 820]], 3.8, I.BONE, 2, "inferred", .5)] +
        spike(680, 480, 28, 4.6) + [I.oval(780, 500, 34, 24, "#d8c070", at=5.6), I.line([[756, 500], [804, 500]], 5.6, "#8a7a40", 3, draw=False)] +
        [{"k": "poly", "p": [[700, 600], [740, 560], [770, 610]], "fill": "#e8c060", "c": "none", "w": 0, "curve": True, "in": 6.6}, I.dot(726, 590, 4, "#8a7a40", 6.6)] +
        flowers + [I.glow(500, 950, 260, 11.6, .4, "lamp")], 2.17)}
    # 5 · two peoples in 2008; how teeth tell relatives; in 2025, the teeth match
    molar = [[420, 1180], [430, 1130], [455, 1112], [480, 1128], [500, 1110], [520, 1128], [545, 1112], [570, 1130], [580, 1180], [565, 1260], [540, 1330], [520, 1270],
             [500, 1250], [480, 1270], [460, 1330], [435, 1260]]
    teeth = {"base": "dark", "cam": [1.05, 500, 900], "els": _t(
        [I.person(x, 780, 140, .5 + .15 * k, I.BLUE) for k, x in enumerate((180, 260, 340))] + [I.person(x, 780, 140, 1.0 + .15 * k, I.AU) for k, x in enumerate((660, 740, 820))] +
        [I.line([[500, 560], [500, 800]], 1.6, I.BONE, 4, dur=.6), I.label(500, 520, "2008", 1.8, I.BONE, 34)] +
        [{"k": "poly", "p": molar, "fill": "#efe6d2", "c": "#b8a888", "w": 2, "curve": True, "in": 6.0, "fx": "pop"}] +
        [I.ring(x, y, 14, 10.6 + .25 * k, I.AMBER, 3, dur=.3) for k, (x, y) in enumerate(((455, 1122), (500, 1120), (545, 1122)))] +
        [I.tooth(x, 880, 46, 17.6 + .1 * k) for k, x in enumerate((180, 260, 340, 660, 740, 820))] +
        [I.label(500, 896, "≈", 21.0, I.GREEN, 72, st="serif"), I.glow(500, 870, 120, 21.0, .5), I.label(500, 950, "2025", 17.2, I.GREEN, 34)], 2.0)}
    tag = _t(helix(330, 600, 670, 600, 2.6, n=18, amp=18) + I.question(720, 600, 3.2, 60) + [I.glow(500, 1000, 300, 7.0, .5, "lamp")], 1.32)
    return remix(ep, scenes={0: s0, 1: s1, 2: shore, 3: embrace, 4: level, 5: teeth}, alias={6: 0}, adds={0: hook, 1: mp},
                 cams={1: [1.4, gx_, gy_ + 60], 6: [1.14, 500, 960]}, beat_adds={5: (tag, [1.14, 500, 960])})


def lying(x, y, L=86, at=0, c="#e8d6b8"):
    """A person lying down, head at x (feet toward +x), on the line y: L px long."""
    return [{"k": "circle", "x": x + L * .1, "y": y - L * .1, "r": L * .09, "fill": c, "c": "none", "w": 0, "in": at, "fx": "pop"},
            {"k": "line", "p": [[x + L * .24, y - L * .1], [x + L * .9, y - L * .08]], "c": c, "w": L * .14, "in": at, "fx": "pop"}]


def beast(x, y, s=1.0, at=0, c="#e8d6b8"):
    """A headless beast, as painted at Wadi Sura: a body, legs and a tail, no head."""
    body = [[x - 52 * s, y - 52 * s], [x - 30 * s, y - 66 * s], [x + 10 * s, y - 62 * s], [x + 40 * s, y - 74 * s], [x + 60 * s, y - 70 * s], [x + 62 * s, y - 50 * s],
            [x + 44 * s, y - 34 * s], [x - 40 * s, y - 32 * s]]
    return [{"k": "poly", "p": body, "fill": c, "c": "none", "w": 0, "curve": True, "in": at}] + \
           [{"k": "line", "p": [[x + a_ * s, y - 38 * s], [x + (a_ + b_) * s, y - 18 * s], [x + (a_ + b_ / 2) * s, y]], "c": c, "w": 6 * s, "in": at} for a_, b_ in ((-36, -8), (-22, 8), (30, -6), (44, 10))] + \
           [{"k": "line", "p": [[x - 50 * s, y - 50 * s], [x - 70 * s, y - 40 * s], [x - 78 * s, y - 16 * s]], "c": c, "w": 3 * s, "in": at, "curve": True},
            {"k": "line", "p": [[x + 58 * s, y - 70 * s], [x + 70 * s, y - 82 * s]], "c": c, "w": 12 * s, "in": at}]


def wadisura_m():
    """Wadi Sura as one continuous take (see mural.py): a wall seventeen metres long, thousands of figures, a stencil made
    and a lizard's foot found, two ways to read a swimmer, and a bridge of three thousand years with a gap in it."""
    import copy
    remix, I = _mur()
    ep = wadisura()
    RD = "#7a3a26"
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] = [e for e in s0["els"] if e.get("k") != "label"]
    hook = _t([I.glow(820, 420, 160, 3.0, .85, "sun"), I.dot(820, 420, 30, "#fff1d2", 3.0)], 1.68)
    # 1 · the map: Egypt's borders; the cave in the far south-west; a film made it famous
    v = View(22, 34, 20, 28.5, (40, 330, 920, 900))
    cx_, cy_ = v.p(25.2335, 23.5947)
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") != "scale" and not (e.get("k") == "pin" and e.get("t", "").startswith("Luxor"))]
    film = [I.box(cx_ + 70, cy_ - 170, 150, 70, "#1a1511", I.BONE, 2, 4, 9.6, fx="pop")] + \
           [I.box(cx_ + 78 + 18 * k, cy_ - 164, 9, 9, I.BONE, r=1, at=9.7) for k in range(8)] + [I.box(cx_ + 78 + 18 * k, cy_ - 115, 9, 9, I.BONE, r=1, at=9.7) for k in range(8)] + \
           [I.box(cx_ + 92 + 40 * k, cy_ - 148, 30, 26, "#7fa0b8", r=2, at=9.9) for k in range(3)]
    mp = _t([I.glow(cx_, cy_, 80, 1.0, .8, "lamp"), I.line([v.p(25, 28.5), v.p(25, 22), v.p(34, 22)], 3.4, "#e9dccb", 3, "inferred", 1.4),
             I.label(v.p(29.5, 25.6)[0], v.p(29.5, 25.6)[1], "Egypt", 4.2, "#cbbca8", 36, st="serif")] + film, 1.35)
    # 2 · the Cave of Beasts: a wall 17 m long (ten people head to toe), thousands of figures; hands, swimmers, headless beasts
    W0, W1 = 70, 930
    r6 = rnd(6)
    marks = []
    for k in range(300):
        x, y = W0 + 20 + r6() * (W1 - W0 - 40), 640 + r6() * 330
        kind = k % 3
        at = 12.4 + .008 * k
        marks.append(I.dot(round(x, 1), round(y, 1), 4.5, ["#f0d8b0", "#c8643c", "#e8d6b8"][kind], at))
    hand = [[-50, 90], [-50, -60], [-35, -65], [-25, 20], [-18, -90], [-2, -92], [4, 15], [14, -80], [30, -78], [32, 25], [44, -40], [60, -34], [54, 90]]
    beasts = {"base": "dark", "cam": [1.05, 500, 920], "els": _t(
        [{"k": "poly", "p": [[0, 520], [1000, 520], [1000, 640], [700, 660], [300, 650], [0, 640]], "fill": "#5a4636", "c": "#a88b66", "w": 2, "in": .6, "fx": "rise"},
         I.box(W0, 600, W1 - W0, 400, "#b08a60", r=6, at=.8)] +
        [I.line([[W0, 1040], [W1, 1040]], 6.0, I.BONE, 2.5, dur=.6), I.line([[W0, 1024], [W0, 1056]], 6.0, I.BONE, 2.5, draw=False),
         I.line([[W1, 1024], [W1, 1056]], 6.0, I.BONE, 2.5, draw=False), I.label(500, 1092, "17 m", 6.4, I.BONE, 34)] +
        sum([lying(W0 + 86 * k, 1150, 86, 8.0 + .25 * k, "#e8d6b8" if k % 2 else "#e8b87a") for k in range(10)], []) + marks +
        [{"k": "poly", "p": [[230 + a_ * .9, 1290 + b_ * .9] for a_, b_ in hand], "fill": "none", "c": "#f0d8b0", "w": 3, "in": 15.4, "fx": "draw"},
         I.glow(230, 1290, 90, 15.4, .5, "red")] + swimmer(500, 1300, 2.0, 15.9, "#e0905c") + beast(780, 1360, 1.3, 16.4, "#e8d6b8"), 1.92)}
    # 3 · a stencil, made; a baby's hand?; no: a lizard's foot
    HX, HY = 300, 900
    hpts = [[HX + a_ * 1.3, HY + b_ * 1.3] for a_, b_ in hand]
    spray = [I.dot(round(HX + (r6() - .5) * 260, 1), round(HY + (r6() - .5) * 320, 1), 7, "#a8402a", 2.6 + .04 * k, op=.85) for k in range(60)]
    lizard = {"base": "dark", "cam": [1.1, 500, 900], "els": _t(
        [I.box(80, 560, 840, 720, "#b08a60", r=10, at=.2), {"k": "poly", "p": hpts, "fill": "#e8d6b8", "c": "none", "w": 0, "in": 1.0, "fx": "pop"}] + spray +
        [{"k": "poly", "p": hpts, "fill": "#b08a60", "c": "#f5ecdc", "w": 3, "in": 5.4, "fx": "draw", "dur": 1.2}] +
        [I.label(HX, 1170, "a baby's hand?", 8.0, "#f5ecdc", 32)] +
        [I.oval(700, 830, 30, 80, "#6f8a4c", at=11.2), I.oval(700, 730, 20, 28, "#6f8a4c", at=11.2),
         {"k": "line", "p": [[700, 900], [712, 980], [744, 1040], [760, 1100]], "c": "#6f8a4c", "w": 12, "curve": True, "in": 11.2}] +
        [I.line([[700 + sx * 20, y0], [700 + sx * 66, y0 + dy]], 11.2, "#6f8a4c", 9, draw=False) for sx, y0, dy in ((-1, 790, -24), (1, 790, -24), (-1, 870, 30), (1, 870, 30))] +
        sum([[I.line([[700 + sx * 66, y0 + dy], [700 + sx * 66 + 26 * math.cos(t), y0 + dy + 26 * math.sin(t)]], 11.4, "#6f8a4c", 4, draw=False)
              for t in [math.radians(a_) for a_ in ((-150, -120, -90, -60, -30) if dy < 0 else (30, 60, 90, 120, 150))]] for sx, y0, dy in ((-1, 790, -24), (1, 790, -24), (-1, 870, 30), (1, 870, 30))], []) +
        [I.ring(634, 766, 46, 12.0, I.AU, 4, dur=.5)] +
        [I.label(704, 1170, "no: a lizard's foot", 12.8, I.AU, 32)], 2.5)}
    # 5 · two readings: real swimmers in a real lake; or the dead in the waters before creation (a world rising); later, in tombs
    read = {"base": "dark", "cam": [1.05, 500, 880], "els": _t(I.question(500, 470, .4, 90) +
        [I.box(90, 560, 820, 300, "#3f7f9c", r=10, at=2.6), I.box(90, 560, 820, 90, "#8aa3b8", r=10, at=2.6), I.line([[90, 650], [910, 650]], 2.8, "#e9f2f8", 3, draw=False),
         I.box(90, 650, 200, 20, "#7d9a5a", r=0, at=2.8)] + swimmer(560, 700, 2.4, 3.6, RD) +
        [I.line([[420 + 30 * j, 740 + 10 * (j % 2)], [450 + 30 * j, 740 + 10 * (j % 2)]], 4.2 + .05 * j, "#e9f2f8", 2, draw=False) for j in range(6)] +
        [I.label(500, 900, "a real lake?", 5.0, "#cfe6ff", 32)] +
        [I.box(90, 960, 820, 300, "#0d1a26", "#2a4a5a", 2, 10, 8.6)] + [I.dot(130 + 60 * k, 990 + 23 * (k % 5), 2, "#9fd0ff", 8.8, op=.5) for k in range(13)] +
        swimmer(500, 1090, 2.2, 10.0, "#c8a890") + [I.glow(500, 1090, 130, 10.2, .5, "lamp"), I.label(500, 1300, "the waters before creation?", 11.4, "#e8b87a", 32)] +
        [{"k": "poly", "p": [[600, 1260], [680, 1170], [760, 1150], [840, 1180], [900, 1260]], "fill": "#8a7050", "c": "#c9ad85", "w": 2, "curve": True, "in": 15.6, "fx": "rise"}] +
        [I.box(370, 1340, 260, 80, "#c9ad85", "#8a6a48", 3, 4, 20.4, fx="pop")] + swimmer(500, 1380, 1.2, 21.0, RD), 2.23)}
    # 4 · the gap: paintings 6500-4500 BCE; texts 2,000-3,000 years later; like a Roman mosaic read through a book of today
    X = lambda y: 110 + 780 * (y + 7000) / 9026
    AY = 1060
    gap = {"base": "dark", "cam": [1.15, 500, 950], "els": _t(
        [I.line([[90, AY], [910, AY]], .3, "#8c7152", 3, dur=1.0),
         {"k": "rect", "x": X(-6500), "y": AY - 12, "w": X(-4500) - X(-6500), "h": 24, "r": 12, "fill": "#c8643c", "c": "none", "sw": 0, "in": .8, "fx": "pop"},
         I.label((X(-6500) + X(-4500)) / 2, AY + 56, "paintings", 1.4, "#e8a070", 30), I.label((X(-6500) + X(-4500)) / 2, AY + 96, "6500–4500 BCE", 2.0, "#cbbca8", 28)] +
        swimmer((X(-6500) + X(-4500)) / 2, AY - 70, 1.3, 1.0, "#c8643c") +
        [{"k": "rect", "x": X(-2400), "y": AY - 12, "w": X(-1300) - X(-2400), "h": 24, "r": 12, "fill": "#e8dcc2", "c": "none", "sw": 0, "in": 7.0, "fx": "pop"},
         I.box((X(-2400) + X(-1300)) / 2 - 30, AY - 110, 60, 76, "#e8dcc2", "#8a7a66", 2, 4, 7.2, fx="pop"), I.label((X(-2400) + X(-1300)) / 2, AY + 56, "texts", 7.4, "#e8dcc2", 30),
         I.arrow([[X(-4500), AY - 30], [(X(-4500) + X(-2400)) / 2, AY - 240], [X(-2400), AY - 30]], 8.2, I.BONE, 3, "inferred", 1.2),
         I.label((X(-4500) + X(-2400)) / 2, AY - 270, "2,000–3,000 years", 8.8, I.BONE, 30)] +
        [I.box(X(1) - 34 + 18 * (k % 4), AY - 110 + 18 * (k // 4), 16, 16, ["#c8643c", "#e8dcc2", "#3f7f9c", "#e8b87a"][(k + k // 4) % 4], r=1, at=11.2 + .03 * k) for k in range(16)] +
        [I.label(X(1), AY + 56, "Rome", 11.6, "#e8dcc2", 30), I.box(X(2026) - 46, AY - 96, 44, 62, "#8fb5a0", "#e8dcc2", 2, 3, 12.6, fx="pop"),
         I.label(X(2026) - 20, AY + 56, "today", 12.8, "#cbbca8", 30),
         I.arrow([[X(1) + 10, AY - 140], [(X(1) + X(2026)) / 2, AY - 230], [X(2026) - 20, AY - 140]], 13.4, I.AMBER, 3, dur=.9),
         I.label((X(1) + X(2026)) / 2, AY - 252, "2,000 years", 14.0, I.AMBER, 28)] +
        [I.dot(round(X(-4500) + (X(-2400) - X(-4500)) * f, 1), round(AY - 30 - 4 * 210 * f * (1 - f), 1), 9, c, 15.6 + .3 * j)
         for j, (f, c) in enumerate(((.15, "#c8643c"), (.33, "#d8905c"), (.5, "#c9c1ee"), (.67, "#9fd0ff"), (.85, "#e8dcc2")))] +
        I.question((X(-4500) + X(-2400)) / 2, AY - 120, 20.6, 70), 1.64)}
    tag = _t([I.arrow([[120, 480], [220, 410], [330, 460]], 3.2, I.BONE, 3, "inferred", .7), I.arrow([[470, 460], [560, 410], [640, 480]], 3.6, I.BONE, 3, "inferred", .7)] +
             I.question(400, 480, 4.8, 64), 1.55)
    return remix(ep, scenes={0: s0, 1: s1, 2: beasts, 3: lizard, 4: gap, 5: read}, alias={6: 0}, adds={0: hook, 1: mp},
                 cams={1: [1.35, cx_ + 120, cy_ - 40], 6: [1.12, 500, 960]}, beat_adds={5: (tag, [1.12, 500, 960])})


def palm(x, y, h=80, at=0, c="#6f8a4c", trunk="#6a4a30"):
    """A date palm: a leaning trunk and a crown of fronds (drawn in colour, readable on a dark wall)."""
    top = (x + h * .08, y - h)
    e = [{"k": "line", "p": [[x, y], [x + h * .06, y - h * .5], top], "c": trunk, "w": max(3, h * .07), "curve": True, "in": at}]
    for k in range(7):
        a = math.pi * (1.05 + .9 * k / 6)
        e.append({"k": "line", "p": [list(top), [top[0] + math.cos(a) * h * .3, top[1] + math.sin(a) * h * .22 - 6], [top[0] + math.cos(a) * h * .48, top[1] + math.sin(a) * h * .1 + 10]],
                  "c": c, "w": max(2, h * .05), "curve": True, "in": at})
    return e


def chariot(x, y, s=1.0, at=0, c="#e8d6b8"):
    return [{"k": "circle", "x": x, "y": y - 22 * s, "r": 22 * s, "fill": "none", "c": c, "w": 4 * s, "in": at},
            {"k": "line", "p": [[x - 22 * s, y - 40 * s], [x + 30 * s, y - 40 * s], [x + 40 * s, y - 64 * s]], "c": c, "w": 5 * s, "in": at},
            {"k": "line", "p": [[x + 30 * s, y - 40 * s], [x + 90 * s, y - 34 * s]], "c": c, "w": 3 * s, "in": at},
            {"k": "person", "x": x + 4 * s, "y": y - 40 * s, "h": 60 * s, "t": False, "color": c, "in": at}]


def garamantes_m():
    """The Garamantes as one continuous take (see mural.py): towns, a pyramid and tunnels; seventeen centuries; chariots and
    backward-walking cattle; how a foggara works and how deep its shafts go; then the rain that fell long ago, a savings account
    with no deposits, a sinking water table, and the canals running dry."""
    import copy
    remix, I = _mur()
    ep = garamantes()
    # 0 · the hook: towns, a pyramid, then the tunnels (the original section, its build delayed until the tunnels are named)
    s0 = copy.deepcopy(ep["shots"][0])
    s0["els"] = [dict(e, **{"in": round(e["in"] + 3.8, 2)}) if isinstance(e.get("in"), (int, float)) and e["in"] > 0 else e
                 for e in s0["els"] if e.get("k") != "label"]
    hook = _t([{"k": "house", "x": 832 + 34 * k, "y": 700, "w": 30, "h": 30 + 10 * (k % 2), "in": 2.6 + .15 * k, "fill": "#a88660"} for k in range(3)] +
              [{"k": "pyramid", "x": 80, "y": 700, "w": 110, "courses": False, "in": 3.6, "fx": "rise"}], 1.22)
    # 1 · the map: Fezzan; seventeen centuries; chariots; cattle grazing backwards
    v = View(6, 20, 22, 34, (40, 330, 920, 900))
    gx_, gy_ = v.p(12.78, 26.55)
    s1 = copy.deepcopy(ep["shots"][1])
    s1["els"] = [e for e in s1["els"] if e.get("k") != "scale"]
    fez = [v.p(a_, b_) for a_, b_ in [(10, 28.3), (13, 28.6), (16, 27.6), (16.2, 25.2), (14, 24.2), (11, 24.4), (9.6, 26)]]
    T0, T1 = 200, 800
    mp = _t([I.glow(gx_, gy_, 80, .8, .8, "lamp"), {"k": "poly", "p": fez, "fill": "rgba(232,184,122,.12)", "c": "#e8b87a", "w": 2.5, "style": "inferred", "curve": True, "in": 1.6}] +
            [I.line([[T0, 1330], [T1, 1330]], 4.2, "#8c7152", 3, dur=.6), {"k": "rect", "x": T0, "y": 1318, "w": T1 - T0, "h": 24, "r": 12, "fill": GOLD, "c": "none", "sw": 0,
              "in": 4.6, "fx": "pop"}, I.label(T0, 1382, "1000 BCE", 4.8, "#cbbca8", 28, "start"), I.label(T1, 1382, "700 CE", 5.2, "#cbbca8", 28, "end"),
             I.label(500, 1300, "1,700 years", 7.6, GOLD, 32)] +
            chariot(250, 1180, 1.2, 10.2) + cow(660, 1180, .62, 13.0, "#e8dcc6", horns="forward") +
            [I.arrow([[600, 1215], [480, 1215]], 13.8, I.AMBER, 4, dur=.5, curve=False)], 1.62)
    # 2 · how a foggara works: a gentle slope from the groundwater to the fields; shafts for diggers and air; nine metres, a three-storey house
    HILL = [[0, 600], [250, 630], [500, 700], [700, 820], [860, 960]]
    surf = lambda x: next(HILL[i][1] + (HILL[i + 1][1] - HILL[i][1]) * (x - HILL[i][0]) / (HILL[i + 1][0] - HILL[i][0]) for i in range(len(HILL) - 1) if HILL[i][0] <= x <= HILL[i + 1][0])
    tun = lambda x: 880 + 80 * (x - 130) / 750
    WT = [[0, 800], [430, 872]]
    sx = [200, 320, 440, 560, 680, 780]
    foggara = {"base": "sky", "tod": "day", "ground": 960, "sun": [880, 420, 28], "cam": [1.05, 500, 860], "els": _t(
        [{"k": "poly", "p": HILL + [[860, 970], [0, 970]], "fill": "#9c7e58", "c": "#e9d3a8", "w": 2, "in": -1},
         {"k": "poly", "p": WT + [[560, 1040], [500, 1170], [0, 1170]], "fill": "rgba(79,147,179,.45)", "c": "none", "w": 0, "in": 1.8, "dur": 1.2, "curve": False},
         I.line(WT, 2.0, I.BLUE, 3, "inferred", 1.0), I.label(40, 1135, "ancient groundwater", 4.0, "#cfe6ff", 30, "start")] +
        [I.line([[130, tun(130)], [880, tun(880)]], 6.0, "#2a2019", 14, dur=2.0), I.line([[130, tun(130)], [880, tun(880)]], 7.6, I.BLUE, 5, dur=2.0)] +
        [I.arrow([[x, tun(x) - 22], [x + 60, tun(x + 60) - 22]], 9.0 + .3 * k, "#cfe6ff", 3, dur=.4, curve=False) for k, x in enumerate((200, 380, 560, 740))] +
        [{"k": "rect", "x": 870, "y": 950, "w": 130, "h": 14, "r": 4, "fill": "#6f8a4c", "c": "none", "sw": 0, "in": 12.0, "fx": "pop"},
        ] + palm(905, 958, 90, 12.4) + palm(962, 958, 74, 12.6) +
        [I.line([[x, surf(x)], [x, tun(x)]], 15.8 + .25 * k, "#2a2019", 9, dur=.5) for k, x in enumerate(sx)] +
        [I.person(440, tun(440) - 8, 46, 18.0, "#e8d6b8"), I.arrow([[322, surf(320) - 40], [322, tun(320) - 30]], 20.0, "#e9f2f8", 3, "inferred", .6)] +
        [I.line([[548, surf(560)], [548, tun(560)]], 22.4, GOLD, 3, dur=.5), I.label(536, (surf(560) + tun(560)) / 2 + 10, "9 m", 22.8, GOLD, 32, "end")] +
        [I.box(590, surf(560) - 190, 86, 190, "rgba(242,201,142,.12)", GOLD, 3, 2, 24.6, fx="rise")] +
        [I.line([[590, surf(560) - 190 + 63 * j], [676, surf(560) - 190 + 63 * j]], 25.0, GOLD, 2, draw=False) for j in (1, 2)] +
        [I.box(604 + 30 * (j % 2), surf(560) - 172 + 63 * (j // 2), 18, 22, GOLD, r=2, at=25.2, op=.6) for j in range(6)], 2.5)}
    # 3 · oasis towns; the pyramid tomb (3-4.5 m); trade across the desert
    s3 = copy.deepcopy(ep["shots"][3])
    for e in s3["els"]:
        if e.get("k") == "iso":
            for it in e["items"]:
                if it.get("t") == "label":
                    it["text"] = "3–4.5 m"
    town = _t([{"k": "house", "x": 90 + 52 * k, "y": 820 - 14 * (k % 2), "w": 44, "h": 26 + 8 * (k % 3), "in": 1.0 + .15 * k} for k in range(5)] +
              sum([palm(110 + 80 * k, 800, 80, 1.6 + .2 * k) for k in range(3)], []) +
              [I.arrow([[80, 1360], [500, 1330], [920, 1360]], 11.4, I.AMBER, 3, "inferred", 1.6)] +
              [I.box(200 + 150 * k, 1326 - 4 * (k % 2), 30, 22, "#c9a06a", r=4, at=12.0 + .3 * k, fx="pop") for k in range(5)], 2.21)
    # 4 (on 2) · rain long ago; a savings account with no deposits; the water table sinks; the canals run dry
    WT2 = [[0, 1000], [430, 1072]]
    dry = _t([I.oval(160, 440, 120, 40, "#b8c4cc", op=.9, at=.6), I.oval(300, 430, 90, 34, "#b8c4cc", op=.9, at=.8)] +
             [I.line([[110 + 40 * j, 480], [96 + 40 * j, 560]], 1.2 + .04 * j, I.BLUE, 3, "inferred", .4) for j in range(8)] +
             [I.box(640, 400, 140, 170, "rgba(159,208,255,.12)", "#e9f2f8", 3, 18, 5.6, fx="pop"), I.box(646, 470, 128, 94, I.BLUE, r=12, at=5.8, op=.8),
              I.line([[600, 360], [680, 360], [680, 396]], 6.4, "#e9f2f8", 6, draw=False), I.strike(600, 400, 700, 330, 7.2, I.RED, 5),
              I.arrow([[790, 540], [860, 540], [860, 600]], 10.2, I.BLUE, 4, dur=.4, curve=False), I.box(646, 470, 128, 50, "#2a3440", r=6, at=10.6)] +
             [{"k": "poly", "p": WT + WT2[::-1], "fill": "#7a6248", "c": "none", "w": 0, "in": 13.0, "dur": 1.6, "op": .95, "keepop": True},
              I.line(WT2, 13.4, I.BLUE, 3, "inferred", 1.0)] +
             [I.arrow([[x, 812 + .17 * x], [x, 990 + .17 * x]], 13.6 + .2 * k, I.BLUE, 3, dur=.5, curve=False) for k, x in enumerate((80, 220, 360))] +
             [I.line([[130, tun(130)], [880, tun(880)]], 15.0, "#7a6248", 6, dur=1.6), {"k": "rect", "x": 870, "y": 948, "w": 130, "h": 18, "r": 4, "fill": "#a88a5c", "c": "none",
              "sw": 0, "in": 16.2}, I.strike(870, 990, 960, 900, 16.6, I.RED, 5)], 1.57)
    trade = _t([I.arrow([[60, 560], [300, 520], [520, 560], [700, 470], [900, 360]], 2.2, I.AMBER, 3, "inferred", 1.4)] +
               [I.box(160 + 160 * k, 528 - 10 * k, 26, 20, "#c9a06a", r=4, at=2.6 + .2 * k, fx="pop") for k in range(4)] +
               [I.person(x, surf(x), 60, 4.0 + .2 * k, "#e8d6b8" if k == 0 else "#7a6a58") for k, x in enumerate((236, 356, 476, 596))], 1.79)
    return remix(ep, scenes={0: s0, 1: s1, 2: foggara, 3: s3}, alias={4: 1, 5: 2, 6: 0}, adds={0: hook, 1: mp, 3: town},
                 cams={1: [1, 500, 860], 5: [1.05, 500, 840], 6: [1.1, 500, 940]}, beat_adds={4: (dry, [1.05, 500, 840])}, line_adds={(4, 1): (trade, None)})


def EPISODES():
    return [nabta_m(), glass_m(), takarkori_m(), tassili_m(), switchoff_m(), gobero_m(), wadisura_m(), garamantes_m(), ledger_recap()]
