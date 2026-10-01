"""File 02 · The First Signs. Marks, codes and records before writing.
The oldest deliberate marks, Ice Age notation, the signs that appear everywhere, and Peru's band of holes (02.02, Ice Age Europe's 32 signs, was made earlier)."""
import math, random
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_

SERIES = "The First Signs"
OCH = "#b0503a"; CREAM = "#f2e8d6"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "awe",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


def hand(cx, cy, s=1.0, fill="#1a1511"):
    """A left hand, palm on the wall: the shape a stencil leaves."""
    P = [(-60, 160), (-70, 40), (-120, -10), (-110, -30), (-60, 0), (-55, -130), (-35, -135), (-25, -20), (-15, -165), (8, -168), (15, -25), (30, -150), (52, -148), (50, -15),
         (70, -110), (90, -105), (80, 30), (60, 160)]
    return {"k": "poly", "p": [[cx + x * s, cy + y * s] for x, y in P], "fill": fill, "c": "none", "w": 0, "curve": True, "in": .6}


# ---------------------------------------------------------------- 02.01 The oldest marks
def oldest():
    zz = [[330 + k * 34, 820 + (-1) ** k * 40] for k in range(11)]
    shell = [{"k": "poly", "p": [[240, 860], [300, 700], [460, 620], [640, 640], [760, 740], [780, 880], [700, 1000], [500, 1040], [330, 990]], "fill": "#6a6258", "c": "#c9c0ae", "w": 2, "curve": True, "in": .1}] + \
            [{"k": "line", "p": [[300 + k * 30, 700 + k * 30], [760 - k * 20, 760 + k * 25]], "c": "#8a8074", "w": 1, "op": .5, "curve": True, "in": .2} for k in range(6)] + \
            [{"k": "line", "p": zz, "c": CREAM, "w": 4, "in": .8, "fx": "draw", "dur": 1.4},
             {"k": "cap", "x": 500, "y": 520, "t": "a freshwater mussel shell · Trinil, Java", "in": .2},
             {"k": "label", "x": 500, "y": 1140, "t": "a zigzag cut with a sharp point · schematic", "c": AMBER, "in": 1.8}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": shell}
    v = View(-25, 135, -45, 58, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Trinil · Homo erectus", 111.36, -7.38, {"c": GOLD, "a": "end", "lx": -18}), ("Muna · a hand stencil", 122.6, -4.9, {"a": "end", "lx": -18, "ly": 34}),
                          ("Blombos Cave", 21.2, -34.4, {}), ("La Roche-Cotard · Neanderthals", 0.68, 47.35, {"a": "start", "ly": -22})], cam=[1, 500, 860])
    s2 = stat("430,000", "years", "at least: the age of the Trinil zigzag, made when Homo erectus was the only human on Java", "Joordens et al. 2015, Nature")
    och = [{"k": "poly", "p": [[260, 760], [720, 700], [760, 900], [300, 980]], "fill": OCH, "c": "#e9a080", "w": 2, "in": .1}] + \
          [{"k": "line", "p": [[320 + k * 55, 760], [300 + k * 55, 960]], "c": "#f2c9a8", "w": 3, "in": .5 + k * .05} for k in range(8)] + \
          [{"k": "line", "p": [[290, 800 + k * 40], [740, 760 + k * 40]], "c": "#f2c9a8", "w": 3, "in": .9 + k * .05} for k in range(4)] + \
          [{"k": "cap", "x": 500, "y": 600, "t": "crosshatch on ochre · Blombos Cave", "in": .2},
           {"k": "label", "x": 500, "y": 1080, "t": "our own species · about 100,000–75,000 years ago · schematic", "c": AMBER, "in": 1.4}]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": och}
    st = [{"k": "rect", "x": 140, "y": 520, "w": 720, "h": 720, "fill": "#8a6a4e", "c": "none", "sw": 0, "in": .1},
          {"k": "glow", "x": 500, "y": 880, "r": 330, "kind": "red", "op": 1, "in": .3}, hand(500, 900, 1.5, "#a8886a"),
          {"k": "cap", "x": 500, "y": 470, "t": "a hand stencil · Muna, Sulawesi · schematic", "in": .2},
          {"k": "label", "x": 500, "y": 1320, "t": "at least 67,800 years old: the oldest dated cave art (2026)", "c": AMBER, "in": 1.2}]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": st}
    tl, ax = timeline(-560, 20, [(-500, "500,000 yrs ago"), (-400, "400,000"), (-300, "300,000"), (-200, "200,000"), (-100, "100,000"), (0, "today")], "Marks before and with us")
    tl["els"] += event(ax, -430, "the Trinil zigzag", row=1, c=GOLD, i=.3, sub="Homo erectus") + \
                 [{"k": "band", "x0": ax.x(-300), "x1": ax.x(0), "y": 470, "h": 12, "c": "#6a645c", "op": .7, "t": "our species exists", "in": .6}] + \
                 event(ax, -75, "Blombos", row=0, c=OCH, i=.9) + event(ax, -57, "Neanderthal lines", row=2, c=SCAN, i=1.1)
    s5 = tl
    s6 = like(s0, cam=[1.12, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE FIRST MARKS][sfx:boom][act:hushed wonder, setting the scene]A ^zigzag, cut into a mussel shell in ^Java. [act:slower, let the number land]At least ^four hundred and thirty thousand years ago.",
                      "[d:tension][cam:1.12|0|0][act:the reveal, quiet, amazed][tune:fall]Made by a kind of human that wasn't ^us."], cut=False),
        B("world", 0, ["[d:calm][k:THE SHELL][act:plain storytelling]Dug up at Trinil in the {1890s|eighteen nineties}, looked at again with ^modern tools: a ^deliberate@adj zigzag, engraved with a sharp point.",
                       "[d:build][go:2|0][act:significant, lean on it]At that time, Homo erectus was the ^only human on Java."]),
        B("collision", 5, ["[d:build][k:THE OLD STORY][act:recounting the old view, even]Textbooks once said art and symbols exploded ^suddenly, about ^forty thousand years ago, in ^Europe. [sfx:hit][act:flat, final][tune:highfall]That story has ^collapsed."]),
        B("cost", 3, ["[d:build][k:THE NEW MAP][act:touring the map, brisk][tune:level]South Africa: our species engraving ^crosshatches on ochre, up to a ^hundred thousand years ago. [go:4|0][act:next stop, same pace][tune:fall]Sulawesi: a hand stencil at least ^sixty-seven thousand eight hundred years old.",
                      "[d:build][go:1|0][act:the last stop, a note of wonder][tune:fall]France: finger lines by ^Neanderthals, sealed over ^fifty-seven thousand years ago."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][act:honest caveat, slower]But 'before our species' rests almost entirely on ^one shell.",
                          "[d:build][sfx:shimmer][act:conceding, fair]^Deliberate@adj, yes. [act:wondering aloud][tune:rise]But a ^symbol? [act:lighter, playful][tune:rise]A ^doodle? [act:one more guess][tune:rise]A test of a new ^tool? [gap:0.4][act:honest, quiet, certain][tune:fall]^Nobody knows."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Symbolic marks ^before Homo sapiens? [act:the verdict, level-headed][tune:fall]^*Plausible*. [act:the reason, gentle][tune:fall]^One zigzag doesn't make a ^pattern.",
                     "[d:tension][p:0.93][act:quiet wonder, the last thought]The urge to leave a mark may be ^older than ^we are."]),
    ]
    return EP("oldest-marks", "02.01", "Older Than Us: The First Deliberate Marks", "oldest-marks", "plausible", "Did humans before our own species make deliberate marks and symbols?", "Made by a human that wasn't *us*.", beats, shots,
              "Joordens et al. 2015, Nature · Henshilwood et al. 2002, 2009, 2018 · Marquet et al. 2023 · Oktaviana et al. 2026 · Hoffmann et al. 2018",
              "A zigzag cut into a Javan shell at least 430,000 years ago, by Homo erectus: the oldest deliberate marks, and why the 'creative explosion' story collapsed.",
              ["#Archaeology", "#HumanEvolution", "#RockArt", "#History", "#FirstSigns"])


# ---------------------------------------------------------------- 02.03 Ice Age notation
def notation():
    horse = [{"k": "rect", "x": 120, "y": 540, "w": 760, "h": 700, "fill": "#b89a72", "c": "none", "sw": 0, "in": .1},
             {"k": "poly", "p": [[220, 860], [260, 780], [340, 760], [420, 780], [520, 770], [560, 720], [600, 700], [620, 730], [590, 790], [580, 860], [560, 960], [540, 960], [530, 880],
                                 [400, 880], [370, 960], [350, 960], [340, 880], [260, 900]], "fill": "none", "c": "#2a1f18", "w": 6, "curve": True, "in": .3}] + \
            [{"k": "circle", "x": 290 + k * 50, "y": 1040, "r": 12, "fill": OCH, "c": "none", "w": 0, "in": .9 + k * .08} for k in range(6)] + \
            [{"k": "line", "p": [[640, 1000], [660, 1040], [680, 1000]], "c": OCH, "w": 7, "in": 1.5}, {"k": "line", "p": [[660, 1040], [660, 1090]], "c": OCH, "w": 7, "in": 1.5},
             {"k": "cap", "x": 500, "y": 480, "t": "dots and a 'Y' beside a horse · schematic", "in": .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": horse}
    s1 = stat("3,000+", "signs", "on about 260 objects from the caves of the Swabian Jura, 43,000 to 34,000 years old", "Bentz & Dutkiewicz 2026")
    bone = [{"k": "poly", "p": [[200, 900], [240, 840], [760, 820], [820, 860], [800, 920], [240, 940]], "fill": "#d9c9a6", "c": "#fff3dc", "w": 2, "curve": True, "in": .1}] + \
           [{"k": "line", "p": [[260 + k * 22, 842], [260 + k * 22, 862]], "c": "#3a2a1c", "w": 2, "in": .3 + k * .02} for k in range(22)] + \
           [{"k": "line", "p": [[260 + k * 26, 878], [260 + k * 26, 898]], "c": "#3a2a1c", "w": 2, "in": .8 + k * .02} for k in range(19)] + \
           [{"k": "line", "p": [[260 + k * 30, 912], [260 + k * 30, 928]], "c": "#3a2a1c", "w": 2, "in": 1.2 + k * .02} for k in range(17)] + \
           [{"k": "cap", "x": 500, "y": 700, "t": "the Ishango bone · Congo · about 20,000 years", "in": .2},
            {"k": "label", "x": 500, "y": 1060, "t": "168 notches in three columns · schematic", "c": AMBER, "in": 1.6}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": bone}
    s3 = stat("862", "sequences", "of dots, lines and Y signs tested as a calendar of animal life", "Bacon et al. 2023")
    tl, ax = timeline(-46, 0, [(-45, "45,000 yrs ago"), (-35, "35,000"), (-25, "25,000"), (-15, "15,000"), (-5, "5,000")], "Marks, then writing")
    tl["els"] += event(ax, -43, "a notched bone", row=0, c=BONE, i=.3) + [{"k": "band", "x0": ax.x(-43), "x1": ax.x(-34), "y": 700, "h": 16, "c": GOLD, "t": "Swabian signs", "in": .5}] + \
                 event(ax, -20, "Ishango", row=1, c=BONE, i=.8) + event(ax, -5.3, "writing, in Mesopotamia", row=2, c=SCAN, i=1.1)
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("shown, and not shown", AMBER, ["marks added over time: shown", "structured sequences: shown", "what they record: unknown", "that they spell words: not claimed"])}
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:ICE AGE NOTATION][sfx:boom][act:curious, laying out the clues][tune:level]Rows of ^dots beside a painted horse. [act:the second clue][tune:level]^Crosses on an ivory figurine. [act:the third, slower][tune:fall]^Notches on a baboon bone.",
                      "[d:tension][cam:1.1|0|0][act:the question, leaning in][tune:rise]Were Ice Age people keeping ^records@noun?"], cut=False),
        B("world", 1, ["[d:calm][k:THE MARKS][act:setting out the facts, even]In the caves of southern Germany: about two hundred and sixty ^objects@noun, more than ^three thousand signs, up to ^forty-three thousand years old.",
                       "[d:build][go:2|0][act:another exhibit, precise]In Congo, the ^Ishango bone: a hundred and sixty-eight notches, in ^three columns."]),
        B("collision", 0, ["[d:build][k:THE CALENDAR][act:reporting a bold idea, fair]In {2023|twenty twenty-three}, an independent researcher, Bennett Bacon, and academic co-authors argued that dots beside animals count ^lunar months from ^spring,",
                           "[d:build][sfx:shimmer][act:continuing, building]and that a ^Y sign marks the month of ^birth. [act:the neat idea, admiring]A ^hunters' calendar."]),
        B("cost", 3, ["[d:build][k:THE STRUCTURE][act:serious, a notable result]In {2026|twenty twenty-six}, another study measured the German signs and found them as ^structured as the earliest ^proto-writing from Mesopotamia."]),
        B("reversal", 5, ["[d:reveal][k:THE CATCH][sfx:hit][act:the catch, careful and plain]But ^nobody has shown what any sequence ^actually records@verb. [act:even, laying out the doubts]Critics dispute the ^tracings, and patterns turn up in ^any big pile of marks.",
                          "[d:aside][act:fair, a quiet footnote]^Neither team claims the signs spell out ^words."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Ice Age marks that stored ^information? [act:the verdict, level-headed][tune:fall]^*Plausible*. [act:the bigger claim, a little playful][tune:rise]Writing ^before writing? [act:flat, precise][tune:fall]Not ^shown.",
                     "[d:tension][p:0.93][act:warm wonder, the closing image]Some forty thousand years before the ^alphabet, someone was already ^counting something."]),
    ]
    return EP("ice-age-writing", "02.03", "Ice Age Notation: Records Before Writing?", "ice-age-writing", "plausible", "Did Ice Age people record information in signs, long before writing?", "Were they keeping *records*?", beats, shots,
              "Bentz & Dutkiewicz 2026 · Bacon et al. 2023, Cambridge Archaeological Journal · d'Errico et al. 2012 · de Heinzelin 1962 · Texier et al. 2010",
              "Rows of dots beside painted horses, 3,000 signs on Ice Age objects, 168 notches on a bone: were Ice Age people keeping records tens of thousands of years before writing?",
              ["#IceAge", "#CaveArt", "#Writing", "#Archaeology", "#FirstSigns"])


# ---------------------------------------------------------------- 02.04 The same signs everywhere
def shared():
    def cell(i):
        cx = 260 + (i % 3) * 240; cy = 700 + (i // 3) * 300
        k = i
        if k == 0:
            return [hand(cx, cy + 20, .55, "#b0503a")]
        if k == 1:
            return [{"k": "line", "p": [[cx + math.cos(t) * t * 9, cy + math.sin(t) * t * 9] for t in [q * .2 for q in range(60)]], "c": CREAM, "w": 4, "curve": True, "in": .6}]
        if k == 2:
            return [{"k": "line", "p": [[cx - 90 + q * 30, cy + (-1) ** q * 40] for q in range(7)], "c": CREAM, "w": 4, "in": .6}]
        if k == 3:
            return [{"k": "line", "p": [[cx - 80, cy - 80 + q * 40], [cx + 80, cy - 80 + q * 40]], "c": CREAM, "w": 3, "in": .6} for q in range(5)] + \
                   [{"k": "line", "p": [[cx - 80 + q * 40, cy - 80], [cx - 80 + q * 40, cy + 80]], "c": CREAM, "w": 3, "in": .6} for q in range(5)]
        if k == 4:
            return [{"k": "circle", "x": cx, "y": cy, "r": 70, "fill": "none", "c": CREAM, "w": 4, "in": .6}, {"k": "circle", "x": cx, "y": cy, "r": 12, "fill": CREAM, "c": "none", "w": 0, "in": .6}]
        return [{"k": "circle", "x": cx, "y": cy, "r": r, "fill": "none", "c": CREAM, "w": 3, "in": .6} for r in (22, 44, 66)] + \
               [{"k": "circle", "x": cx, "y": cy, "r": 8, "fill": CREAM, "c": "none", "w": 0, "in": .6}, {"k": "line", "p": [[cx, cy], [cx + 90, cy + 40]], "c": CREAM, "w": 3, "in": .6}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": [e for i in range(6) for e in cell(i)] + [{"k": "cap", "x": 500, "y": 480, "t": "the same signs, on every inhabited continent", "in": .2}]}
    v = View(-110, 135, -55, 60, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Muna · hand stencil", 122.6, -4.9, {"a": "end", "lx": -18}), ("Cueva de las Manos", -70.67, -47.15, {}), ("Göbekli Tepe", 38.92, 37.22, {"c": GOLD}),
                          ("Newgrange", -6.475, 53.69, {"a": "end", "lx": -18}), ("La Venta", -94.04, 18.1, {}), ("Trinil · a zigzag", 111.36, -7.38, {"a": "end", "lx": -18, "ly": 34})], cam=[1, 500, 860])

    def bag(cx, cy, lab):
        return [{"k": "rect", "x": cx - 60, "y": cy - 20, "w": 120, "h": 110, "fill": "#8c7452", "c": CREAM, "sw": 2, "in": .4},
                {"k": "line", "p": [[cx - 40, cy - 20], [cx - 30, cy - 70], [cx + 30, cy - 70], [cx + 40, cy - 20]], "c": CREAM, "w": 4, "curve": True, "in": .5},
                {"k": "label", "x": cx, "y": cy + 150, "t": lab, "st": "small", "in": .8}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": bag(220, 860, "Göbekli Tepe") + bag(500, 860, "La Venta") + bag(780, 860, "Assyria") +
          [{"k": "cap", "x": 500, "y": 620, "t": "the 'handbags' · schematic", "in": .2},
           {"k": "label", "x": 500, "y": 1160, "t": "Assyria's is a bucket for sprinkling purifying water", "c": AMBER, "in": 1.6}]}

    def ent(cx, cy, k):
        if k == 0:
            return [{"k": "line", "p": [[cx - 70, cy - 70 + q * 35], [cx + 70, cy - 70 + q * 35]], "c": "#9fd0ff", "w": 2, "in": .4} for q in range(5)] + \
                   [{"k": "line", "p": [[cx - 70 + q * 35, cy - 70], [cx - 70 + q * 35, cy + 70]], "c": "#9fd0ff", "w": 2, "in": .4} for q in range(5)]
        if k == 1:
            return [{"k": "line", "p": [[cx, cy], [cx + 80 * math.cos(a), cy + 80 * math.sin(a)]], "c": "#9fd0ff", "w": 2, "in": .5} for a in [q * math.pi / 4 for q in range(8)]] + \
                   [{"k": "circle", "x": cx, "y": cy, "r": r, "fill": "none", "c": "#9fd0ff", "w": 1.4, "in": .6} for r in (25, 50, 75)]
        if k == 2:
            return [{"k": "circle", "x": cx, "y": cy, "r": r, "fill": "none", "c": "#9fd0ff", "w": 2, "in": .5} for r in (15, 35, 55, 78)]
        return [{"k": "line", "p": [[cx + math.cos(t) * t * 7, cy + math.sin(t) * t * 7] for t in [q * .2 for q in range(60)]], "c": "#9fd0ff", "w": 2.4, "curve": True, "in": .5}]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [e for i in range(4) for e in ent(300 + (i % 2) * 400, 760 + (i // 2) * 260, i)] +
          [{"k": "cap", "x": 500, "y": 560, "t": "lattice · cobweb · tunnel · spiral", "in": .2},
           {"k": "label", "x": 500, "y": 1200, "t": "shapes the human visual system makes by itself", "c": AMBER, "in": 1.4}]}
    s4 = stat("32", "signs", "recur across more than 367 Ice Age sites in Europe, 40,000 to 10,000 years ago", "von Petzinger 2016")
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("one source would leave a trail", "#9fd0ff", ["a single first appearance", "a spread outward over time", "examples in between"]) +
          [{"k": "label", "x": 500, "y": 880, "t": "found so far: none of these", "c": "#ffb09a", "in": 1.5}]}
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE SAME SIGNS EVERYWHERE][sfx:boom][act:counting them off, intrigued][tune:level]^Hand stencils. [act:quicker][tune:level]^Spirals. [act:quicker still][tune:level]^Zigzags. [act:a playful surprise][tune:risefall]Even ^'handbags'. [act:the scale of it, wide]On ^every inhabited continent.",
                      "[d:tension][cam:1.1|0|0][act:posing the choice, even][tune:rise]Inherited from ^one lost source? [act:the alternative, settling][tune:fall]Or invented ^again and again?"], cut=False),
        B("world", 1, ["[d:calm][k:THE PATTERN][act:laying out the facts, calm]The oldest dated hand stencil is on an ^Indonesian island: at least ^sixty-seven thousand eight hundred years old. [act:the contrast, lightly]^Patagonia's begin about ^nine thousand years ago.",
                       "[d:build][go:4|0][act:building the pattern]In Ice Age Europe, ^thirty-two signs repeat across ^hundreds of sites."]),
        B("collision", 2, ["[d:build][k:THE CASE][act:presenting his case fairly]Graham Hancock points to a ^'handbag' at Göbekli Tepe, at the Olmec site of La Venta, and in the hands of ^Assyrian sages.",
                           "[d:build][sfx:shimmer][act:the big idea, intrigued][tune:rise]A badge of ^one lost tradition?"]),
        B("cost", 3, ["[d:build][k:THE BRAIN][act:the turn, explaining with care]But our eyes and brains make certain shapes by ^themselves: lattices, cobwebs, tunnels, ^spirals. [act:softer, a little wonder]People see them in ^migraines, on the edge of ^sleep.",
                      "[d:aside][act:dry, a small smile]And ^every human has hands."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][sfx:hit][act:reasoning it out, clear]One source would leave a trail: a ^first appearance, then a ^spread. [act:the twist, slower][tune:fall]Instead the signs pop up at ^scattered dates, on ^different continents.",
                          "[d:build][go:2|0][act:curious, a closer look][tune:rise]And the 'handbags' up ^close@adj? [act:plain, a little amused]In Assyria, a ^bucket for sprinkling water. [act:crisp, parallel][tune:fall]^Different objects@noun, different ^jobs."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]One lost ^source for the world's symbols? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the alternative, warmer][tune:rise]One shared human ^brain? [act:simple, confident]That explains ^most of it.",
                     "[d:tension][p:0.93][act:gentle, a knowing smile]You don't need a ^lost teacher to draw a spiral. [act:simple, warm, final][tune:fall]You need a ^hand, and an ^eye."]),
    ]
    return EP("shared-symbols", "02.04", "The Same Signs Everywhere: One Source or One Brain?", "shared-symbols", "unsupported", "Why do the same symbols appear in cultures that never met?", "Inherited, or invented *again*?", beats, shots,
              "Oktaviana et al. 2026 · Joordens et al. 2015 · von Petzinger 2016 · Wiggermann 1992 · Klüver 1966 · Bressloff et al. 2001 · Hancock 2015",
              "Hand stencils, spirals, zigzags and 'handbags' on every continent: were they handed down from one lost culture, or invented again and again by the same human brain?",
              ["#Symbols", "#RockArt", "#GobekliTepe", "#Archaeology", "#FirstSigns"])


# ---------------------------------------------------------------- 02.05 The band of holes
def holes():
    r = random.Random(8)
    ridge = [{"t": "slab", "x0": -60, "x1": 60, "z0": -26, "z1": 26, "y": 0, "c": "#b89a72"}]
    for k in range(34):
        s = k / 33
        cx = -54 + 108 * s; cz = 10 * math.sin(s * 2.2 * math.pi)
        for row in range(-3, 4):
            if r.random() < .12:
                continue
            x = cx + r.uniform(-.4, .4); z = cz + row * 2.4 + r.uniform(-.3, .3)
            ridge.append({"t": "flat", "pts": [[x + .9 * math.cos(a), z + .9 * math.sin(a)] for a in [q * math.pi / 6 for q in range(12)]], "y": .05, "c": "#3a2a1c", "ground": True})
    ridge += [{"t": "person", "x": 30, "y": 0, "z": 22, "h": 1.7},
              L_(0, 0, "about 5,200 holes, 1–2 m across · schematic", GOLD, z=-24, dy=-22), L_(0, 0, "a band about 1.5 km long", "#cfe6ff", z=26, dy=40)]
    s0 = iso(ridge, cam=[1, 500, 900], s=7.6, x=500, y=1000, az=-22, spin=1.0, el=.55, table=None)
    v = View(-81, -69, -18.5, -8, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Monte Sierpe · Pisco Valley", -75.8745, -13.7111, {"c": GOLD}), ("Lima", -77.04, -12.05, {"a": "end", "lx": -18}), ("Nazca", -75.13, -14.74, {})],
                 extra=[{"k": "label", "x": v.p(-79, -15.5)[0], "y": v.p(-79, -15.5)[1], "t": "the Pacific", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    grid = [{"k": "circle", "x": 240 + c * 74, "y": 600 + rr * 74, "r": 26, "fill": "#3a2a1c", "c": "#b89a72", "w": 2, "in": .2 + (rr * 8 + c) * .01} for rr in range(9) for c in range(8)]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 190, "y": 550, "w": 620, "h": 690, "fill": "#b89a72", "c": "none", "sw": 0, "in": .1}] + grid +
          [{"k": "cap", "x": 500, "y": 490, "t": "one section: nine rows of eight holes", "in": .2}]}
    s3 = stat("5,200", "holes", "in a band about 1.5 km long on a desert ridge; mapped by drone in 2025", "Bongers et al. 2025, Antiquity")
    kh = [{"k": "line", "p": [[180, 620], [820, 620]], "c": "#c9a370", "w": 8, "in": .1}] + \
         [{"k": "line", "p": [[220 + k * 50, 620], [220 + k * 50 + (k % 3) * 6, 1040 - (k % 4) * 40]], "c": ["#c9a370", "#b0503a", "#e9dccb", "#8c7452"][k % 4], "w": 4, "curve": True, "in": .3 + k * .05} for k in range(13)] + \
         [{"k": "circle", "x": 220 + k * 50 + (k % 3) * 3, "y": 700 + ((k * 37) % 5) * 60, "r": 8, "fill": "#3a2a1c", "c": "none", "w": 0, "in": 1.0 + k * .04} for k in range(13)] + \
         [{"k": "cap", "x": 500, "y": 540, "t": "a khipu: knotted-cord accounts · schematic", "in": .2},
          {"k": "label", "x": 500, "y": 1160, "t": "the Inca recorded numbers in cords and knots", "c": AMBER, "in": 1.5}]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": kh}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the evidence, 2025", "#8fd9b0", ["at least 60 sections, repeating counts", "pollen: maize, and basket reeds", "a date: about 1320–1405 CE", "between two Inca centres"])}
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE BAND OF HOLES · PERU][sfx:boom][act:painting the picture, wonder]Five thousand two hundred holes, each big enough to ^stand in, snaking over a desert@noun ridge for a ^kilometre and a half.",
                      "[d:tension][cam:1.12|0|0][act:quiet, the mystery hanging][tune:fall]For ninety years, ^nobody could say ^why."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:placing us on the map, calm]Monte Sierpe, in Peru's ^Pisco Valley. [act:plain, a bit of history]Photographed from the ^air in {1933|nineteen thirty-three}.",
                       "[d:build][act:rattling off the guesses][tune:level]The guesses since: ^graves, ^storage, ^defence, ^fog-catchers... [act:dry, one eyebrow up][tune:risefall]and, on TV, something ^stranger."]),
        B("collision", 2, ["[d:build][k:THE MAP][act:news, brisk and bright]In {2025|twenty twenty-five}, a team mapped it by ^drone. [sfx:shimmer][act:the discovery, leaning in]The band splits into at least sixty sections, some with ^repeating counts: nine rows of ^eight."]),
        B("cost", 5, ["[d:build][k:THE DIRT][act:reading the lab report, pleased]Inside the holes: pollen of ^maize, and of reeds used@verb for ^baskets. [act:crisp, one more fact]A date in the {1300s|^thirteen hundreds}.",
                      "[d:build][act:connecting the dots]And the site sits ^between two Inca centres, on ^trade routes."]),
        B("reversal", 4, ["[d:reveal][k:THE ANSWER][sfx:hit][act:the reveal, delighted but careful]Their reading: a ^marketplace, where goods were counted out by the ^basketful, hole by hole.",
                          "[d:build][act:tentative, the extra idea]Later, ^perhaps, an Inca tribute counter, laid out like a ^khipu: the Inca's accounts in knotted cords."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A giant ^accounting device? [act:the verdict, level-headed][tune:fall]^*Plausible*. [act:honest caveat, even][tune:fallrise]The ^best evidence yet, though it rests on ^one date and a set of samples.",
                     "[d:tension][p:0.93][act:playful wonder, a smile]Maybe the world's biggest ^spreadsheet. [act:the kicker, dry][tune:fall]Dug into a ^mountain."]),
    ]
    return EP("band-of-holes", "02.05", "The Band of Holes: A Spreadsheet Dug Into a Mountain?", "band-of-holes", "plausible", "Who dug thousands of holes in rows on a Peruvian ridge, and why?", "Nobody could say *why*.", beats, shots,
              "Bongers et al. 2025, Antiquity · Shippee 1933 · Hyslop 1984",
              "Some 5,200 man-sized holes snake over a desert ridge in Peru for 1.5 km. Drones, pollen and a radiocarbon date now point to an ancient system for counting goods.",
              ["#Peru", "#Inca", "#Archaeology", "#Mystery", "#FirstSigns"])


def holes_m():
    """The band of holes as one continuous take (see mural.py): fifteen pitches of holes, the old guesses, a drone that finds order,
    pollen and a date from inside a hole, traders filling holes basket by basket, and the khipu that keeps the same count."""
    import copy
    from mural import remix, rewritten
    import illus as I
    ep = rewritten(copy.deepcopy(holes()))              # authored times below follow the rewritten words (about 2.4 words a second)
    S = ep["shots"]
    HOLE, SAND = "#3a2a1c", "#b89a72"
    # 0 · the ridge: short labels only; fifteen football pitches laid end to end for scale
    s0 = copy.deepcopy(S[0])
    for e in s0["els"]:
        if e.get("k") == "iso":
            e["items"] = [it for it in e["items"] if it.get("t") != "label"] + [L_(0, 0, "about 5,200 holes", GOLD, z=-24, dy=-22), L_(0, 0, "about 1.5 km", "#cfe6ff", z=26, dy=40)]
            e.update(x=540, s=6.8)
            iso0 = {k: e[k] for k in ("x", "y", "s", "az", "spin", "el")}
    pitches = [I.box(82 + 56 * k, 400, 50, 32, "#3f7a4a", "#cfe6b0", 1.5, 2, round(13.2 + .12 * k, 2)) for k in range(15)] + \
              [I.line([[107 + 56 * k, 400], [107 + 56 * k, 432]], round(13.25 + .12 * k, 2), "#cfe6b0", 1.2, draw=False) for k in range(15)] + \
              [I.label(500, 375, "15 football pitches", 15.2, "#cfe6b0", 30)]
    # 1 · the map: a plane photographs the ridge in 1933; then the old guesses, each fitting a few holes
    v = View(-81, -69, -18.5, -8, (40, 330, 920, 900))
    px, py = v.p(-75.8745, -13.7111)
    ux, uy = -190 / 291.0, 220 / 291.0                       # the direction of flight; nx, ny across it
    nx, ny = -uy, ux
    cx_, cy_ = px + 175, py - 185
    P = lambda a, b: [round(cx_ + ux * a + nx * b, 1), round(cy_ + uy * a + ny * b, 1)]
    plane = [I.line([[px + 230, py - 260], [px + 40, py - 40]], 6.8, I.BONE, 2, "inferred", 1.0),
             {"k": "poly", "p": [P(34, 0), P(26, 5), P(-30, 4), P(-30, -4), P(26, -5)], "fill": I.BONE, "c": "none", "w": 0, "in": 7.4, "fx": "pop"},
             {"k": "poly", "p": [P(10, 4), P(-4, 38), P(-12, 38), P(-6, 4), P(-6, -4), P(-12, -38), P(-4, -38), P(10, -4)], "fill": I.BONE, "c": "none", "w": 0, "in": 7.4, "fx": "pop"},
             {"k": "poly", "p": [P(-22, 3), P(-30, 16), P(-34, 16), P(-30, 3), P(-30, -3), P(-34, -16), P(-30, -16), P(-22, -3)], "fill": I.BONE, "c": "none", "w": 0, "in": 7.4, "fx": "pop"},
             I.label(px + 215, py - 215, "1933", 8.2, I.BONE, 32, "start"), I.ring(px, py, 46, 9.6, GOLD, 3)]
    gx = [180, 340, 500, 660, 820]
    guess = [I.box(70, 1110, 860, 290, "rgba(18,13,10,.9)", "#8c7152", 2, 16, .2)] + \
            [I.oval(gx[0], 1235, 52, 22, "#6a5640", "#c9ad85", 2, 1, .9), I.box(gx[0] - 10, 1170, 20, 48, "#c9ad85", r=3, at=1.0)] + \
            [{"k": "lib", "k2": "vase", "x": gx[1], "y": 1255, "h": 92, "w": 60, "in": 1.6, "fx": "rise"}] + \
            [{"k": "poly", "p": [[gx[2] - 60, 1255], [gx[2] - 60, 1185], [gx[2] - 40, 1185], [gx[2] - 40, 1170], [gx[2] - 20, 1170], [gx[2] - 20, 1185], [gx[2], 1185], [gx[2], 1170],
                                [gx[2] + 20, 1170], [gx[2] + 20, 1185], [gx[2] + 40, 1185], [gx[2] + 40, 1170], [gx[2] + 60, 1170], [gx[2] + 60, 1255]], "fill": "#8c7152", "c": "#c9ad85", "w": 2, "in": 2.3}] + \
            [I.box(gx[3] - 55, 1165, 110, 90, "none", "#cfe6ff", 2, 2, 3.0)] + [I.line([[gx[3] - 55 + 22 * j, 1165], [gx[3] - 55 + 22 * j, 1255]], 3.0, "#cfe6ff", 1, draw=False) for j in range(1, 5)] + \
            [I.dot(gx[3] - 30 + 20 * j, 1272 + 6 * (j % 2), 5, I.BLUE, round(3.3 + .1 * j, 2)) for j in range(4)] + \
            I.question(gx[4], 1250, 4.4, 80) + \
            [I.label(x, 1335, t, round(.9 + .7 * k, 2), c, 28) for k, (x, t, c) in enumerate(zip(gx, ("graves?", "storage?", "defence?", "fog nets?", "on TV"), (I.BONE,) * 4 + (I.LILAC,)))]
    # 2 · the drone: overlapping photos stitched into one map; the band falls into sections; one section is nine rows of eight
    drone = [I.box(455, 395, 90, 26, "#d8dde2", "#5a636c", 2, 8, 1.4, fx="pop")] + \
            [I.line([[465, 400], [420, 380]] if s < 0 else [[535, 400], [580, 380]], 1.4, "#d8dde2", 3, draw=False) for s in (-1, 1)] + \
            [I.oval(x, 376, 34, 7, "#9aa3ab", "none", 0, .9, 1.5) for x in (420, 580)] + \
            [{"k": "fan", "x": 500, "y": 425, "r": 250, "a0": 62, "a1": 118, "n": 9, "c": I.BLUE, "in": 3.0}]
    tiles = [I.box(90 + 95 * k, 590 + (k % 2) * 18, 150, 120, "rgba(159,208,255,.06)", I.BLUE, 2, 4, round(4.6 + .35 * k, 2), style="inferred") for k in range(8)]
    rr = random.Random(5)
    secs = [(110 + 84 * k, 70 if k % 3 else 56) for k in range(10)]
    strip = [I.box(90, 625, 820, 92, SAND, r=8, at=8.0, op=.9)] + \
            [I.dot(round(x0 + 9 + 11 * (j % (w // 11)), 1), 640 + 11 * (j // (w // 11)) + rr.choice((0, 1)), 3.6, HOLE, round(8.4 + .04 * k, 2))
             for k, (x0, w) in enumerate(secs) for j in range((w // 11) * 6)]
    gaps = [I.line([[x0 - 7, 618], [x0 - 7, 724]], round(15.6 + .1 * k, 2), GOLD, 3, dur=.3) for k, (x0, w) in enumerate(secs) if k]
    G = [(296 + 58 * c, 920 + 58 * r) for r in range(9) for c in range(8)]
    zoom = [I.ring(secs[4][0] + 33, 671, 48, 19.0, GOLD, 3, dur=.5), I.line([[secs[4][0] - 10, 712], [262, 892]], 19.3, GOLD, 2, "inferred", .5), I.line([[secs[4][0] + 76, 712], [738, 892]], 19.3, GOLD, 2, "inferred", .5),
            I.box(262, 892, 476, 520, SAND, r=10, at=19.6, op=.95)] + \
           [I.dot(x, y, 21, HOLE, round(20.4 + .16 * (k // 8) + .02 * (k % 8), 2)) for k, (x, y) in enumerate(G)] + \
           [I.label(500, 850, "9 × 8 = 72", 23.6, GOLD, 40, st="serif")]
    s2 = {"base": "dark", "cam": [1, 500, 880], "els": drone + tiles + strip + gaps + zoom}
    # 5 · inside a hole: pollen of maize and of reeds, then a date that burns down like a candle
    lab = [I.line([[70, 560], [400, 560]], .2, "#8c7152", 3, draw=False),
           {"k": "poly", "p": [[140, 560], [150, 660], [200, 690], [270, 690], [320, 660], [330, 560]], "fill": "#5a4632", "c": "#c9ad85", "w": 2, "in": .4},
           {"k": "poly", "p": [[150, 650], [200, 680], [270, 680], [320, 650], [323, 620], [147, 620]], "fill": "#7a6248", "c": "none", "w": 0, "in": 1.0, "fx": "fill"},
           I.person(375, 560, 120, .6), I.ring(235, 650, 26, 2.6, I.BLUE, 3, dur=.4),
           I.line([[258, 640], [500, 560]], 3.0, I.BLUE, 2, "inferred", .6), I.dot(650, 560, 150, "#1d1813", 3.4, op=.95), I.ring(650, 560, 150, 3.4, I.BLUE, 4, dur=.7)] + \
          [x for k, (gx_, gy_) in enumerate(((590, 500), (680, 470), (640, 590))) for x in (I.dot(gx_, gy_, 26, "#e8c35a", round(5.0 + .3 * k, 2)), I.dot(gx_, gy_, 7, "#8a6a2a", round(5.0 + .3 * k, 2)))] + \
          [I.oval(x, y, 18, 10, "#9fcf6a", "#5e7d3a", 1.5, 1, round(5.9 + .3 * k, 2)) for k, (x, y) in enumerate(((730, 560), (700, 640), (585, 630)))] + \
          [I.label(600, 760, "maize", 11.8, "#e8c35a", 30), I.label(760, 760, "reeds", 13.6, "#9fcf6a", 30),
           {"k": "poly", "p": [[830, 640], [900, 640], [890, 700], [840, 700]], "fill": "#a8865a", "c": "#e8d6b8", "w": 2, "in": 14.6, "fx": "pop"}] + \
          [I.line([[835 + 13 * j, 645], [845 + 13 * j, 698]], 14.7, "#6b4a2e", 1.5, draw=False) for j in range(4)]
    candle = lambda x, h, at: [I.box(x - 22, 1080 - h, 44, h, "#efe6d2", "#b8a888", 1.5, 4, at), I.line([[x, 1080 - h], [x, 1068 - h]], at, I.INK, 2, draw=False),
                               I.oval(x, 1048 - h, 10, 20, "#ffd27a", "none", 0, 1, at), I.glow(x, 1050 - h, 60, at, .7, "lamp")]
    date = candle(200, 200, 17.0) + candle(320, 120, 19.0) + candle(440, 45, 21.0) + [I.line([[150, 1080], [490, 1080]], 16.8, "#8c7152", 2, draw=False)] + \
           [I.line([[560, 1040], [920, 1040]], 25.0, I.BONE, 2, draw=False)] + \
           [I.line([[560 + 120 * k, 1030], [560 + 120 * k, 1050]], 25.0, I.BONE, 2, draw=False) for k in range(4)] + \
           [I.label(560 + 120 * k, 1090, t, 25.0, "#cbbca8", 28) for k, t in enumerate(("1200", "1300", "1400", "1500"))] + \
           [I.box(560 + 120 * 1.2, 1026, 120 * .85, 28, GOLD, r=14, at=26.4, fx="fill"), I.glow(731, 1040, 110, 26.4, .5)]
    s5 = {"base": "dark", "cam": [1, 500, 880], "els": lab + date}
    route = [I.line([[120, 1300], [300, 1270], [500, 1300], [700, 1270], [880, 1300]], .3, "#c9ad85", 4, "inferred", 1.4, True)] + \
            [{"k": "house", "x": x, "y": 1300, "w": 90, "h": 56, "in": .8 + .3 * k, "fx": "rise"} for k, x in enumerate((85, 825))] + \
            [I.label(x, 1360, "Inca centre", 1.2 + .3 * k, GOLD, 28) for k, x in enumerate((130, 870))] + \
            [I.box(452, 1222, 92, 52, SAND, r=8, at=1.9)] + [I.dot(470 + 14 * (j % 5), 1235 + 12 * (j // 5), 4, HOLE, round(2.0 + .02 * j, 2)) for j in range(15)] + [I.ring(498, 1248, 62, 2.4, GOLD, 3)] + \
            [I.person(x, 1290 if k % 2 else 1278, 70, round(4.2 + .4 * k, 2)) for k, x in enumerate((260, 370, 640, 740))]
    # 4 · the marketplace: traders fill one hole per basketful and count; later a khipu keeps the same count in cords and knots
    HX = [170 + 95 * k for k in range(8)]
    market = [I.box(110, 520, 780, 120, SAND, r=10, at=.2, op=.9)] + [I.dot(x, 580, 30, HOLE, round(.4 + .05 * k, 2)) for k, x in enumerate(HX)] + \
             [I.person(80, 500, 110, 1.4)] + [{"k": "poly", "p": [[95, 410], [140, 410], [134, 440], [101, 440]], "fill": "#a8865a", "c": "#e8d6b8", "w": 2, "in": 1.6}] + \
             [{"k": "poly", "p": [[x - 22, 462], [x + 22, 462], [x + 17, 494], [x - 17, 494]], "fill": "#a8865a", "c": "#e8d6b8", "w": 2, "in": round(2.5 + .45 * k, 2), "fx": "pop"} for k, x in enumerate(HX)] + \
             [I.dot(x, 580, 22, "#e8c35a", round(2.8 + .45 * k, 2)) for k, x in enumerate(HX)] + \
             [I.line([[x - 14 + 7 * j, 668], [x - 14 + 7 * j, 696]], round(7.0 + .25 * k, 2), I.BONE, 3, draw=False) for k, x in enumerate(HX) for j in range(1)] + \
             [I.label(500, 760, "8 baskets", 10.4, GOLD, 34)]
    khipu = [I.line([[150, 900], [850, 900]], 7.6, "#c9a370", 8, dur=.8)] + \
            [I.line([[HX[k], 900], [HX[k] + (k % 3) * 5, 1330 - (k % 4) * 30]], round(8.6 + .12 * k, 2), ["#c9a370", OCH, "#e9dccb", "#8c7452"][k % 4], 4, dur=.5, curve=True) for k in range(8)] + \
            [I.arrow([[HX[k], 620], [HX[k], 885]], round(14.0 + .15 * k, 2), GOLD, 2, "inferred", .4, False) for k in range(8)] + \
            [I.dot(HX[k] + (k % 3) * 2, 960 + 34 * j, 9, HOLE, round(16.4 + .08 * (k * 3 + j), 2)) for k in range(8) for j in range(1 + (k * 5) % 4)]
    # 6 → back on the ridge: the world's biggest spreadsheet
    grid = [{"t": "line", "p": [[x, .1, -20], [x, .1, 20]], "c": GOLD, "w": 2, "op": .8, "ground": True} for x in range(-56, 57, 8)] + \
           [{"t": "line", "p": [[-56, .1, z], [56, .1, z]], "c": GOLD, "w": 2, "op": .8, "ground": True} for z in range(-20, 21, 5)]
    sheet = [dict(iso0, k="iso", items=grid, **{"in": .3, "fx": "draw", "dur": 1.6})]
    return remix(ep, _rewrite=False, scenes={0: s0, 2: s2, 4: {"base": "dark", "cam": [1, 500, 880], "els": market}, 5: s5}, alias={3: 0, 6: 0},
                 cams={6: [1.08, 540, 990]}, adds={0: pitches, 1: plane},
                 line_adds={(0, 1): (I.question(500, 560, .4, 90), [1.08, 500, 900]), (1, 1): (guess, None), (3, 1): (route, None), (4, 1): (khipu, None), (5, 1): (sheet, None)})


# ---------------------------------------------------------------- 02.06 The ledger
def _ledger_text():
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 140, "y": 540, "w": 720, "h": 700, "fill": "#8a6a4e", "c": "none", "sw": 0, "in": .1},
                                                    {"k": "glow", "x": 500, "y": 880, "r": 300, "kind": "red", "op": .8, "in": .2}, hand(500, 900, 1.3, "#8a6a4e"),
                                                    {"k": "cap", "x": 500, "y": 480, "t": "marks, codes and records before writing", "in": .2}]}
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["our species made symbols over 70,000 years ago", "hand stencils on every inhabited continent"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible", "#e8c86a", ["marks by humans before our species", "Ice Age signs that stored information", "Peru's holes as an accounting device"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["one lost source for the world's symbols"])}
    s4 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE FIRST SIGNS][sfx:boom][act:quick recap, warm][tune:fall]^Zigzags, ^hands, ^dots and ^holes. [act:inviting, opening the book]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, plain facts]Our species made symbols more than ^seventy thousand years ago. [act:steady, same certainty]Hand stencils appear on ^every inhabited continent."]),
        B("collision", 2, ["[d:build][k:PLAUSIBLE][act:listing, a notch less certain][tune:level]Marks by humans ^before our species. [act:the next item][tune:level]Ice Age signs that stored ^information. [act:the last one, a smile][tune:fall]And Peru's band of holes as a giant ^counting device."]),
        B("cost", 3, ["[d:build][k:AWAITING EVIDENCE][act:fair, unhurried]One lost source for ^all the world's symbols. [d:aside][act:light, a knowing aside]The shared human brain explains ^more, with ^less."]),
        B("tag", 4, ["[d:verdict][k:THE MORAL][p:0.95][act:warm, reflective][tune:fall]Long before writing, people were already ^marking, ^counting and ^remembering. [go:4|1.5][act:gentle contrast, slower][tune:fallrise]That's not a lost ^civilisation. [gap:0.45][act:quiet, certain, a smile][tune:fall]That's ^us.",
                     "[d:tension][p:0.93][act:calm, the motto]^Coherence is the measure. [act:quiet, certain][tune:fall]Not ^final demonstration."]),
    ]
    return EP("signs-ledger", "02.06", "The First Signs · The Ledger", "", "mixed", "Marks, codes and records before writing, weighed.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 02",
              "The verdicts of The First Signs in one ledger: what is established, what is plausible, and what still awaits evidence.",
              ["#History", "#Archaeology", "#Symbols", "#FirstSigns", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: the four cases in a cabinet; a lost source is drawn dotted, then the shared human brain (see cabinet.py)."""
    import math as _m
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    C = Cabinet([
        {"name": "The oldest marks", "model": mdl(oldest(), 0)},
        {"name": "Ice Age signs", "model": mdl(notation(), 0)},
        {"name": "Shared symbols", "model": mdl(shared(), 0)},
        {"name": "The band of holes", "model": mdl(holes()), "fw": .92, "fh": .6},
    ])
    C.build()
    OM, IA, SS, BH = range(4)
    cx, cy = 500, round((C.Y0 + C.Y1) / 2, 1)
    tips = [[c["cx"], round(C.floor(c["i"]) - C.h * .28, 1)] for c in C.cells]
    lost = [{"k": "line", "p": [[cx, cy], t], "c": "#c9c1ee", "w": 3, "style": "claimed", "fx": "draw", "dur": 1.0, "in": .6 + .12 * k} for k, t in enumerate(tips)] + [
            {"k": "circle", "x": cx, "y": cy, "r": 58, "fill": "#120d0a", "c": "#c9c1ee", "w": 3, "style": "claimed", "in": .3},
            {"k": "label", "x": cx, "y": cy + 26, "t": "?", "st": "big", "c": "#c9c1ee", "size": 76, "scl": True, "in": .4, "fx": "pop"}]
    r = 62
    ell = lambda a0, a1, sx: [[round(cx + sx * r * .92 * _m.cos(_m.radians(a)), 1), round(cy - 4 + r * .78 * _m.sin(_m.radians(a)), 1)] for a in range(a0, a1 + 1, 10)]
    squig = lambda y, sx: [[round(cx + sx * (10 + 5 * k), 1), round(y + 6 * _m.sin(k * 1.3), 1)] for k in range(9)]
    brain = [{"k": "line", "p": [[cx, cy], t], "c": "#f2c98e", "w": 4, "fx": "draw", "dur": .9, "in": .9 + .1 * k} for k, t in enumerate(tips)] + [
             {"k": "circle", "x": cx, "y": cy, "r": 72, "fill": "#1c140e", "c": "#f2c98e", "w": 3, "in": .1, "fx": "pop"},
             {"k": "line", "p": ell(-90, 90, 1), "c": "#f5ecdc", "w": 3, "curve": True, "in": .3, "fx": "draw", "dur": .7},
             {"k": "line", "p": ell(90, 270, 1), "c": "#f5ecdc", "w": 3, "curve": True, "in": .3, "fx": "draw", "dur": .7},
             {"k": "line", "p": [[cx, cy - r * .78 - 2], [cx, cy + r * .7]], "c": "#f5ecdc", "w": 2, "in": .5}] + [
             {"k": "line", "p": squig(y, sx), "c": "#e8b87a", "w": 2, "curve": True, "in": .6, "fx": "draw", "dur": .6} for y in (cy - 30, cy - 4, cy + 22) for sx in (1, -1)]
    s1 = C.step(C.cam_cell(OM), C.verdict(OM, "established", "our species, 70,000+ years", .4))
    s2 = C.step(C.cam_cell(SS), C.verdict(SS, "established", "every inhabited continent", .3))
    s3 = C.step(C.cam_cell(OM), C.verdict(OM, "plausible", "before our species", .3))
    s4 = C.step(C.cam_cell(IA), C.verdict(IA, "plausible", "signs that stored information", .3))
    s5 = C.step(C.cam_cell(BH), C.verdict(BH, "plausible", "a giant counting device", .3))
    s6 = C.step(C.cam_all(), C.verdict(SS, "awaiting", "one lost source?", .2, frame=False) + lost)
    s7 = C.step(C.cam_all(), brain)
    s8 = C.step(C.cam_all(), [e for i in range(4) for e in C.wash(i, "#f2b36b", at=.3 + .15 * i, op=.12)])
    s9 = C.step(C.cam_all(), [e for i in range(4) for e in C.people(i, 3, at=.1 + .1 * i)])
    s10 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2}),
        2: (s3, {(0, 1): "%d|1.1" % s4, (0, 2): "%d|1.1" % s5}),
        3: (s6, {(0, 1): "%d|.3" % s7}),
        4: (s8, {(0, 2): "%d|.3" % s9, (1, 0): "%d|3.5" % s10}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def notation_m():
    """Ice Age notation as one continuous take (see mural.py): the marks, a hunters' calendar, a structure test, and what nobody has shown."""
    from mural import remix
    import illus as I
    ep = notation()
    tokens = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(130 + 28 * (k % 26), 580 + 44 * (k // 26), 20, 34, "#e8dcc2", "#b8a888", 1, 8, round(.2 + .006 * k, 3)) for k in range(260)] +
              [I.line([[135 + 28 * (k % 26), 590 + 44 * (k // 26)], [145 + 28 * (k % 26), 600 + 44 * (k // 26)]], round(2.2 + .01 * k, 3), OCHRE, 2, draw=False) for k in range(0, 260, 3)] +
              [I.label(500, 1100, "43,000 years", 4.6, I.BONE, 40, st="serif")]}
    moons = []
    for k in range(6):
        x = 290 + k * 50
        moons += [I.dot(x, 990, 11, "#efe8da", 3.6 + .35 * k), I.dot(x + 5 - k * 2, 988, 10, "#b89a72", 3.6 + .35 * k)]
    cal = moons + [I.ring(660, 1045, 60, 8.6, I.AMBER, 4), I.glow(660, 1045, 90, 8.8, .6)]
    X = lambda k: 170 + 36 * k
    seq = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(130, 600, 330, 300, "#e8dcc2", "#b8a888", 2, 30, .2)] +
           [I.line([[170 + 30 * (k % 9), 650 + 50 * (k // 9)], [175 + 30 * (k % 9), 680 + 50 * (k // 9)]], .4 + .03 * k, OCHRE, 4, draw=False) for k in range(36)] +
           [I.box(540, 600, 330, 300, "#b9a47c", "#8a6a48", 2, 6, 1.4)] + [I.line([[570 + 32 * (k % 9), 640 + 50 * (k // 9)], [590 + 32 * (k % 9), 660 + 50 * (k // 9)]], 1.6 + .03 * k, I.INK, 4, draw=False) for k in range(36)] +
           [I.box(260, 1200 - 220, 70, 220, I.AMBER, r=6, at=3.4, fx="fill"), I.box(670, 1200 - 225, 70, 225, "#b9a47c", r=6, at=3.8, fx="fill"),
            I.line([[200, 1200], [800, 1200]], 3.2, "#8c7152", 3), I.label(500, 1100, "=", 4.4, I.BONE, 80, st="big")]}
    catch = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[180 + 30 * k, 620], [185 + 30 * k, 660]], .3 + .04 * k, OCHRE, 4, draw=False) for k in range(12)] + I.question(620, 640, 1.6, 70) +
             [I.line([[190 + 30 * k, 800], [196 + 30 * k, 842]], 3.6 + .03 * k, I.LILAC, 3, "claimed", .3) for k in range(12)] +
             [I.dot(x, y, 5, "#cbbca8", 5.4 + .01 * k) for k, (x, y) in enumerate(I.scatter(80, 180, 820, 950, 1150, 9))] + [I.ring(480, 1050, 70, 7.0, I.AMBER, 3)] +
             [I.box(330, 1230, 340, 110, "rgba(18,13,10,.85)", I.LILAC, 3, 40, 8.6, style="claimed"), I.strike(320, 1350, 680, 1220, 9.6)]}
    return remix(ep, scenes={1: tokens, 3: seq, 5: catch}, alias={4: 0, 6: 0}, cams={6: [1.1, 500, 860]}, drop=("para", "num", "title", "q", "cap"),
                 beat_adds={2: (cal, [1.15, 500, 900])})


def oldest_m():
    """The oldest marks as one continuous take (see mural.py): the zigzag cut and looked at again, Java when only Homo erectus lived there,
    the old 'explosion' timeline giving way, ochre, a stencil made before our eyes, three kinds of human, and the one shell it all rests on."""
    from mural import remix
    import illus as I
    ep = oldest()
    sec = lambda r: (lambda t: round(t / r, 2))             # times below are seconds into the rewritten narration; remix stretches each step by r
    SHELL = [[240, 860], [300, 700], [460, 620], [640, 640], [760, 740], [780, 880], [700, 1000], [500, 1040], [330, 990]]
    ZZ = [[330 + k * 34, 820 + (-1) ** k * 40] for k in range(11)]
    # 0 · the shell, its zigzag, the age; a human who wasn't us
    t = sec(1.13)
    shell = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "poly", "p": SHELL, "fill": "#6a6258", "c": "#c9c0ae", "w": 2, "curve": True, "in": t(.2)}] +
             [I.line([[300 + k * 30, 700 + k * 30], [760 - k * 20, 760 + k * 25]], t(.4), "#8a8074", 1, curve=True, draw=False, op=.5) for k in range(6)] +
             [I.line(ZZ, t(.6), CREAM, 4, dur=1.6), I.label(500, 1150, "at least 430,000 years", t(6.0), AMBER, 36, st="serif"),
              I.person(890, 1330, 210, t(9.4), "#c9b49a"), I.glow(890, 1230, 150, t(9.4), .3), I.label(890, 1385, "not us", t(11.0), "#cbbca8", 30)]}
    t = sec(2.5)
    look = [I.label(250, 560, "Trinil, 1890s", t(1.4), BONE, 30, "start")] + \
        [I.line([[x0, y0], [x0 + dx, y0 + dy]], t(13.6 + .1 * k), "#a89e90", 1.5, dur=.3) for k, (x0, y0, dx, dy) in enumerate([(300, 740, 60, 30), (580, 690, 50, -18), (400, 960, 70, 10), (620, 940, 40, 32), (690, 820, 36, -40)])] + \
        [I.ring(560, 820, 100, t(7.6), "#cbd2d8", 4), I.line([[631, 891], [700, 960]], t(7.8), "#cbd2d8", 10, draw=False), I.line(ZZ[6:10], t(21.0), AMBER, 5, dur=.8),
         {"k": "poly", "p": [[668, 772], [702, 736], [712, 780]], "fill": "#efe6d2", "c": "#8a7a66", "w": 1.5, "in": t(23.6), "fx": "pop"}, I.label(330, 1000, "deliberate", t(21.4), AMBER, 32)]
    # 2 · Java, then: Homo erectus on a river bank; our species not yet on the time ruler
    t = sec(2.21)
    XR = lambda ky: 150 + 700 * (430 - ky) / 430
    java = {"base": "sky", "tod": "dusk", "ground": 1150, "sun": [790, 1000, 26], "cam": [1, 500, 880], "els": [
                {"k": "water", "y": 1215, "h": 300, "op": .85, "in": t(.2)},
                {"k": "palm", "x": 140, "y": 1150, "h": 230, "in": t(.3)}, {"k": "palm", "x": 860, "y": 1150, "h": 200, "in": t(.3)}] +
            [I.oval(x, 1192, 13, 7, "#d8cfc0", "none", 0, 1, t(.5)) for x in (250, 300, 640, 700, 740)] +
            [I.person(x, 1150, h, t(1.6 + .3 * k), "#2a1f16") for k, (x, h) in enumerate(((360, 200), (470, 185), (590, 205)))] +
            [I.label(475, 905, "Homo erectus", t(3.8), AMBER, 32),
             I.line([[150, 430], [850, 430]], t(7.0), "#cbbca8", 3, dur=.8), I.dot(150, 430, 10, AMBER, t(7.2)), I.label(150, 480, "430,000 years ago", t(7.2), AMBER, 28, "start"),
             I.label(850, 480, "today", t(7.4), "#cbbca8", 28, "end"), I.box(XR(300), 420, 850 - XR(300), 20, BONE, r=6, at=t(9.6), fx="pop"), I.label(XR(150), 400, "our species", t(9.8), BONE, 30)]}
    # 5 · the timeline: the old 'explosion' in Europe, struck; older marks further back; (reversal) our species, one shell, three readings
    t = sec(1.68)
    X = lambda ky: 140 + 720 * (500 - ky) / 500
    AY = 1000
    rays = [I.line([[802 + 40 * math.cos(a), 840 + 40 * math.sin(a)], [802 + 70 * math.cos(a), 840 + 70 * math.sin(a)]], t(7.4), "#ffe2a8", 3, dur=.3) for a in [k * math.pi / 4 for k in range(8)]]
    tl = {"base": "dark", "cam": [1, 500, 880], "els": [I.line([[120, AY], [880, AY]], t(.3), "#e9dccb", 2, dur=.8)] +
          [e for ky, lab in ((500, "500,000"), (300, "300,000"), (100, "100,000"), (0, "today")) for e in (I.line([[X(ky), AY - 8], [X(ky), AY + 8]], t(.6), "#e9dccb", 2, draw=False),
                                                                                                             I.label(X(ky), AY + 50, lab, t(.6), "#cbbca8", 26))] +
          [I.glow(802, 840, 120, t(7.2), .9, "lamp"), I.dot(802, 840, 14, "#ffe2a8", t(7.2))] + rays + [I.line([[802, 860], [802, AY]], t(7.4), "#ffe2a8", 2, "inferred", .4),
           I.label(800, 770, "Europe, 40,000", t(5.4), AMBER, 30, "end"), I.strike(590, 790, 810, 740, t(8.8))] +
          [e for k, ky in enumerate((57, 67.8, 100, 430)) for e in (I.dot(X(ky), AY, 9, AMBER if ky != 430 else CREAM, t(10.8 + .5 * k)), I.ring(X(ky), AY, 16, t(10.8 + .5 * k), AMBER, 2, dur=.4))]}
    t = sec(1.31)
    rev = [I.box(X(300), 950, 860 - X(300), 22, BONE, r=6, at=t(.8), op=.7, fx="pop"), I.label(X(150), 930, "our species", t(1.0), BONE, 30),
           I.box(X(500), 945, X(300) - X(500) - 8, 90, "rgba(201,193,238,.08)", "#c9c1ee", 2, 8, t(2.6), style="inferred"), I.ring(X(430), AY, 30, t(4.4), AMBER, 4),
           I.label(X(430), 925, "one shell", t(4.6), AMBER, 30)]
    t = sec(1.67)
    B3 = [(250, 540), (500, 540), (750, 540)]
    opts = [I.line([[X(430), AY - 32], [x, y + 64]], t((1.2, 3.4, 4.8)[k]), "#c9c1ee", 2, "claimed", .6) for k, (x, y) in enumerate(B3)] + \
        [I.oval(x, y, 62, 62, "rgba(18,13,10,.8)", "#c9c1ee", 2, 1, t((1.4, 3.6, 5.0)[k]), style="claimed") for k, (x, y) in enumerate(B3)] + \
        [I.ring(250, 540, 22, t(1.6), AMBER, 3), I.dot(250, 540, 8, AMBER, t(1.6)), I.line([[205, 540], [295, 540]], t(1.7), AMBER, 2, dur=.4),
         I.line([[455, 550], [475, 520], [495, 560], [515, 515], [540, 555]], t(3.8), CREAM, 3, curve=True, dur=.5),
         {"k": "poly", "p": [[730, 570], [750, 498], [770, 570]], "fill": "#efe6d2", "c": "#8a7a66", "w": 1.5, "in": t(5.3), "fx": "pop"}] + \
        [I.label(x, y + 100, s, t((1.8, 4.0, 5.6)[k]), "#c9c1ee", 28) for k, ((x, y), s) in enumerate(zip(B3, ("a symbol?", "a doodle?", "a tool test?")))] + \
        I.question(150, 800, t(7.2), 80)
    # 3 · ochre from South Africa: the crosshatch engraved, and the red earth as paint
    t = sec(1.5)
    lump = [[220, 820], [300, 700], [520, 650], [740, 690], [800, 820], [720, 960], [480, 1000], [280, 960]]
    ochre = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "poly", "p": lump, "fill": OCH, "c": "#e9a080", "w": 2, "curve": True, "in": t(.3)}, I.label(500, 610, "ochre", t(4.4), BONE, 30)] +
             [I.line([[300, y], [720, y]], t(2.0 + .2 * k), "#f2c9a8", 3, dur=.5) for k, y in enumerate((775, 850, 925))] +
             [I.line([[300 + 60 * k, 775], [360 + 60 * k, 850]], t(2.6 + .08 * k), "#f2c9a8", 3, dur=.3) for k in range(7)] +
             [I.line([[360 + 60 * k, 850], [300 + 60 * k, 925]], t(3.2 + .08 * k), "#f2c9a8", 3, dur=.3) for k in range(7)] +
             [I.line([[290, 1140], [380, 1118], [520, 1130], [640, 1112], [720, 1124]], t(5.4), "#c0442c", 22, curve=True, dur=1.0),
              I.label(500, 1240, "up to 100,000 years ago", t(7.8), AMBER, 34, st="serif")]}
    # 4 · Sulawesi: a hand pressed to the rock, red blown round it, the hand lifted: the stencil stays
    t = sec(2.5)
    WALL = "#8a6a4e"
    h_on = hand(500, 900, 1.5, "#2a1d14"); h_on["in"] = t(3.8)
    h_off = hand(500, 900, 1.5, WALL); h_off["in"] = t(8.2); h_off["dur"] = .9
    spray = [I.dot(x, y, 5, "#c0442c", t(6.0 + .004 * k), fx="fade", op=.75) for k, (x, y) in enumerate(I.scatter(240, 230, 770, 610, 1210, 21))]
    sten = {"base": "dark", "cam": [1, 500, 880], "els": [I.box(140, 520, 720, 760, WALL, r=18, at=t(.2)), I.label(500, 470, "Sulawesi", t(1.2), BONE, 30), h_on,
            I.glow(500, 900, 380, t(5.8), .95, "red")] + spray + [h_off, I.label(500, 1360, "at least 67,800 years", t(12.4), AMBER, 36, st="serif")]}
    # 1 · the map: France ringed, a sealed envelope, then the four places and three kinds of human
    t = sec(2.5)
    v = View(-25, 135, -45, 58, (40, 330, 920, 900))
    fr, tr, bl = v.p(0.68, 47.35), v.p(111.36, -7.38), v.p(21.2, -34.4)
    mapadd = [I.ring(fr[0], fr[1], 30, t(.6), AMBER, 3), I.box(150, 390, 110, 70, "#efe6d2", "#8a7a66", 2, 4, t(9.2)), I.line([[150, 390], [205, 430], [260, 390]], t(9.4), "#8a7a66", 2, dur=.4),
              I.dot(205, 430, 9, "#b0301e", t(9.8))] + \
        [I.ring(x, y, 30, t(13.8 + .2 * k), AMBER, 3) for k, (x, y) in enumerate((tr, v.p(122.6, -4.9), bl, fr))] + \
        [I.person(x + dx, y + 120, 80, t(15.2 + .4 * k), c) for k, ((x, y), dx, c) in enumerate(((tr, -70, "#c9b49a"), (bl, 70, "#f2c98e"), (fr, 70, "#9fd0ff")))]
    t = sec(1.41)
    second = [I.box(150, 1140, 230, 150, "none", I.GREEN, 3, 70, t(6.0), style="inferred")] + I.question(265, 1225, t(6.6), 60, I.GREEN)
    import copy
    world = copy.deepcopy(ep["shots"][1])
    for e in world["els"]:
        if e.get("k") == "pin" and e["t"].startswith(("Trinil", "Muna")):
            e["ly"] = -24 if e["t"].startswith("Trinil") else 42
    return remix(ep, scenes={0: shell, 1: world, 2: java, 3: ochre, 4: sten, 5: tl}, alias={6: 0}, cams={6: [1.12, 500, 900]}, adds={1: mapadd},
                 beat_adds={1: (look, [1.4, 500, 800]), 4: (rev, None), 5: (second, None)}, line_adds={(4, 1): (opts, None)})


def _revisit(ep, bi, li, els):
    """remix draws only on a panel's first visit; this draws els on the panel that the first [go:] of line li of beat bi returns to
    (their "in" in real seconds after the camera arrives), and keeps them on the wall for the rest of the take."""
    import re as _re
    from mural import settle, PW, PH
    s = int(_re.search(r"\[go:(\d+)", ep["beats"][bi]["lines"][li]).group(1))
    cam = ep["shots"][s]["cam"]
    fr = next(e for e in ep["shots"][s]["els"] if e.get("k") == "panel" and e.get("base") != "none" and e["ox"] <= cam[1] < e["ox"] + PW and e["oy"] <= cam[2] < e["oy"] + PH)
    add = {"k": "panel", "ox": fr["ox"], "oy": fr["oy"], "base": "none", "els": list(els)}
    ep["shots"][s]["els"].append(add)
    for sh in ep["shots"][s + 1:]:
        sh["els"].append(settle(add))
    return ep


def _glyph(k, x, y, at, c=CREAM, s=1.0):
    """One of 16 simple signs (a stroke or two), drawn small: the Ice Age sign list in miniature."""
    import illus as I
    q = lambda pts: [[round(x + a * s, 1), round(y + b * s, 1)] for a, b in pts]
    L = lambda pts, curve=False: {"k": "line", "p": q(pts), "c": c, "w": 3, "curve": curve, "in": at}
    k %= 16
    if k == 0: return [I.dot(x, y, 6 * s, c, at)]
    if k == 1: return [L([(-14, 0), (14, 0)])]
    if k == 2: return [L([(-8, -14), (-8, 14)]), L([(8, -14), (8, 14)])]
    if k == 3: return [L([(-14, 0), (14, 0)]), L([(0, -14), (0, 14)])]
    if k == 4: return [L([(-12, -14), (0, 0), (12, -14)]), L([(0, 0), (0, 16)])]
    if k == 5: return [L([(-16, 6), (-8, -8), (0, 6), (8, -8), (16, 6)])]
    if k == 6: return [I.ring(x, y, 13 * s, at, c, 3, dur=.3)]
    if k == 7: return [I.ring(x, y, 14 * s, at, c, 3, dur=.3), I.dot(x, y, 4 * s, c, at)]
    if k == 8: return [L([(math.cos(t) * t * 2.2, math.sin(t) * t * 2.2) for t in [j * .35 for j in range(22)]], True)]
    if k == 9: return [L([(-14, 12), (0, -14), (14, 12), (-14, 12)])]
    if k == 10: return [L([(-13, -12), (13, -12), (13, 12), (-13, 12), (-13, -12)])]
    if k == 11: return [L([(-8, -14), (-8, 14)]), L([(8, -14), (8, 14)])] + [L([(-8, -8 + 8 * j), (8, -8 + 8 * j)]) for j in range(3)]
    if k == 12: return [I.dot(x - 10 * s, y, 4 * s, c, at), I.dot(x, y, 4 * s, c, at), I.dot(x + 10 * s, y, 4 * s, c, at)]
    if k == 13: return [L([(-14, -14), (14, 14)]), L([(14, -14), (-14, 14)])]
    if k == 14: return [L([(-14, 10), (-4, -12), (6, 10), (14, -6)], True)]
    return [L([(-12, 14), (-12, -14), (12, -14)]), L([(-12, 0), (6, 0)])]


def shared_m():
    """The same signs everywhere as one continuous take (see mural.py): six signs and two answers, two hands 60,000 years apart,
    32 signs, three 'handbags', shapes the brain draws by itself, ripples that should be there and are not, a bucket of water."""
    from mural import remix
    import illus as I
    ep = shared()
    sec = lambda r: (lambda t: round(t / r, 2))             # times below are seconds into the rewritten narration; remix stretches each step by r
    BLUE = "#9fd0ff"
    CX = lambda i: 260 + (i % 3) * 240
    CY = lambda i: 700 + (i // 3) * 300
    def sign(i, at):
        cx, cy = CX(i), CY(i)
        if i == 0:
            h = hand(cx, cy + 20, .55, "#b0503a"); h["in"] = at; return [I.glow(cx, cy, 110, at, .5, "red"), h]
        if i == 1:
            return [I.line([[cx + math.cos(t) * t * 9, cy + math.sin(t) * t * 9] for t in [q * .2 for q in range(60)]], at, CREAM, 4, dur=.8, curve=True)]
        if i == 2:
            return [I.line([[cx - 90 + q * 30, cy + (-1) ** q * 40] for q in range(7)], at, CREAM, 4, dur=.6)]
        if i == 3:
            return bag(cx, cy + 10, at, 1.0)
        if i == 4:
            return [I.line([[cx - 80, cy - 80 + q * 40], [cx + 80, cy - 80 + q * 40]], at, CREAM, 3, dur=.3) for q in range(5)] + \
                   [I.line([[cx - 80 + q * 40, cy - 80], [cx - 80 + q * 40, cy + 80]], at + .2, CREAM, 3, dur=.3) for q in range(5)]
        return [I.ring(cx, cy, r, at + .1 * j, CREAM, 3, dur=.4) for j, r in enumerate((22, 44, 66))] + [I.dot(cx, cy, 8, CREAM, at)]
    def bag(cx, cy, at, s=1.0, fill="#8c7452"):
        return [I.box(cx - 60 * s, cy - 20 * s, 120 * s, 110 * s, fill, CREAM, 2, 10 * s, at),
                I.line([[cx - 40 * s, cy - 20 * s], [cx - 30 * s, cy - 70 * s], [cx + 30 * s, cy - 70 * s], [cx + 40 * s, cy - 20 * s]], at + .1, CREAM, 4, curve=True, dur=.4)]
    # 0 · six signs as they are named; then one lost source (dotted, below the signs) or six separate sparks
    t = sec(1.57)
    src = (500, 430)
    tree = [I.line([[src[0], src[1] + 40], [CX(i), CY(i)]], t(9.8 + .12 * i), "#c9c1ee", 2, "claimed", .6) for i in range(6)]
    signs = {"base": "dark", "cam": [1, 500, 880], "els": tree + sum([sign(i, t(at)) for i, at in zip(range(6), (.3, 1.0, 1.6, 2.6, 4.6, 5.2))], []) +
             [I.oval(src[0], src[1], 52, 52, "rgba(18,13,10,.85)", "#c9c1ee", 3, 1, t(9.4), style="claimed"), I.label(src[0], src[1] + 24, "?", t(9.6), "#c9c1ee", 64, st="big")] +
             [I.glow(CX(i) + 70, CY(i) - 70, 50, t(12.6 + .2 * i), .95, "lamp") for i in range(6)] + [I.dot(CX(i) + 70, CY(i) - 70, 6, "#ffe2a8", t(12.6 + .2 * i)) for i in range(6)]}
    # 1 · the map: two hand stencils, two dates, half a planet and nearly 60,000 years apart
    t = sec(1.82)
    v = View(-110, 135, -55, 60, (40, 330, 920, 900))
    mu, cu = v.p(122.6, -4.9), v.p(-70.67, -47.15)
    hands = [I.label(mu[0] - 18, mu[1] + 50, "67,800 years", t(6.0), AMBER, 30, "end"), I.label(cu[0] + 18, cu[1] + 50, "9,000 years", t(13.0), AMBER, 30, "start"),
             I.line([[mu[0], mu[1] + 20], [740, 1180], [420, 1220], [cu[0] + 6, cu[1] + 22]], t(15.0), AMBER, 3, "inferred", 1.6, True), I.label(560, 1290, "nearly 60,000 years apart", t(16.4), BONE, 32, st="serif")]
    # 4 · 32 signs, repeated across hundreds of sites
    t = sec(1.5)
    rr = random.Random(32)
    sites = I.scatter(367, 120, 880, 960, 1330, 7)
    many = {"base": "dark", "cam": [1, 500, 880], "els": sum([_glyph(k, 170 + 94 * (k % 8), 520 + 96 * (k // 8), t(3.6 + .04 * k)) for k in range(32)], []) +
            [I.label(500, 900, "32 signs", t(5.2), AMBER, 34, st="serif")] + [I.dot(x, y, 3.2, "#cbbca8", t(5.8 + .003 * j), fx="fade", op=.8) for j, (x, y) in enumerate(sites)] +
            sum([_glyph(rr.choice((5, 7, 8, 13)), x, y, t(6.4 + .03 * j), AMBER, .55) for j, (x, y) in enumerate(sites[::18])], []) +
            [I.label(500, 1400, "hundreds of sites", t(6.6), BONE, 30)]}
    # 2 · three 'handbags': Göbekli Tepe, La Venta, Assyria; one tradition?
    t = sec(1.53)
    BX = (200, 500, 800)                                      # La Venta, across the ocean, on the left; Göbekli Tepe; Assyria
    ORD = (1, 0, 2)                                           # the order they are named in
    slabs = [I.box(BX[i] - 115, 600, 230, 380, "#6f6456", "#9a8e7c", 2, 8, t((3.0, 5.8, 8.4)[k])) for k, i in enumerate(ORD)]
    bags3 = sum([bag(BX[i], 820, t((3.4, 6.2, 8.8)[k]), .9, "#a08a6a") for k, i in enumerate(ORD)], []) + \
        [I.label(BX[i], 1040, n, t((3.6, 6.3, 8.9)[k]), BONE, 28) for k, (i, n) in enumerate(zip(ORD, ("Göbekli Tepe", "La Venta", "Assyria")))]
    apart = [I.line([[350 + 10 * math.sin(j * 1.4 + k), 620 + 26 * j] for j in range(14)], t(12.2 + .2 * k), BLUE, 3, curve=True, dur=.8) for k in range(2)] + \
        [I.label(350, 1110, "an ocean apart", t(12.6), BLUE, 28)]
    link = [I.line([[BX[0] + 60, 800], [BX[1] - 60, 800]], t(14.8), "#c9c1ee", 3, "claimed", .6), I.line([[BX[1] + 60, 800], [BX[2] - 60, 800]], t(15.2), "#c9c1ee", 3, "claimed", .6)] + \
        I.question(500, 500, t(16.4), 70)
    handbags = {"base": "dark", "cam": [1, 500, 880], "els": slabs + bags3 + apart + link}
    # 3 · shapes the brain draws by itself: an eye and a brain, four form constants, a closed eye; then (line 2) hands everywhere
    t = sec(2.0)
    EYE = [[300, 440], [340, 410], [380, 400], [420, 410], [460, 440], [420, 470], [380, 480], [340, 470]]
    ent = [(300, 720), (700, 720), (300, 1000), (700, 1000)]
    def form(i, cx, cy, at):
        if i == 0:
            return [I.line([[cx - 80, cy - 80 + q * 40], [cx + 80, cy - 80 + q * 40]], at, BLUE, 2, dur=.3) for q in range(5)] + \
                   [I.line([[cx - 80 + q * 40, cy - 80], [cx - 80 + q * 40, cy + 80]], at + .15, BLUE, 2, dur=.3) for q in range(5)]
        if i == 1:
            return [I.line([[cx, cy], [cx + 85 * math.cos(a), cy + 85 * math.sin(a)]], at, BLUE, 2, dur=.3) for a in [q * math.pi / 4 for q in range(8)]] + \
                   [I.ring(cx, cy, r, at + .2, BLUE, 1.6, dur=.4) for r in (28, 54, 80)]
        if i == 2:
            return [I.ring(cx, cy, r, at + .1 * j, BLUE, 2.4, dur=.4) for j, r in enumerate((14, 34, 56, 80))]
        return [I.line([[cx + math.cos(t_) * t_ * 7, cy + math.sin(t_) * t_ * 7] for t_ in [q * .2 for q in range(60)]], at, BLUE, 2.6, dur=.8, curve=True)]
    brainp = (620, 440)
    brain = [I.oval(brainp[0], brainp[1], 70, 52, "#3a2a30", "#e8b8c0", 3, 1, t(1.4)), I.line([[brainp[0], brainp[1] - 50], [brainp[0], brainp[1] + 48]], t(1.6), "#e8b8c0", 2, draw=False)] + \
        [I.line([[brainp[0] + sx * (12 + 9 * j), brainp[1] - 30 + 22 * r + 6 * math.sin(j)] for j in range(5)], t(1.6), "#e8b8c0", 2, curve=True, draw=False) for sx in (1, -1) for r in range(3)]
    shapes = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "poly", "p": EYE, "fill": "#efe6d2", "c": BONE, "w": 2, "curve": True, "in": t(.8)}, I.dot(380, 440, 26, "#3f6e8a", t(.9)), I.dot(380, 440, 11, "#120d0a", t(.9))] +
              brain + sum([form(i, x, y, t(at)) for i, ((x, y), at) in enumerate(zip(ent, (4.6, 5.2, 5.8, 6.4)))], []) +
              [I.glow(x, y, 140, t(8.0), .35, "scan") for x, y in ent] +
              [I.line([[x0 - 70, 1185], [x0, 1205], [x0 + 70, 1185]], t(11.6), BONE, 3, curve=True, dur=.5) for x0 in (420, 580)] +
              [I.line([[x0 + dx, 1200], [x0 + dx * 1.3, 1222]], t(12.0), BONE, 2, draw=False) for x0 in (420, 580) for dx in (-40, -14, 14, 40)] +
              [I.dot(500 + 120 * math.cos(a), 1150 + 40 * math.sin(a), 5, BLUE, t(13.0 + .15 * k)) for k, a in enumerate((3.5, 4.2, 5.0, 5.8))] +
              [I.line([[brainp[0] + 20, brainp[1] + 50], [x, y - 95]], t(17.0 + .25 * k), "#e8b8c0", 2, "inferred", .5) for k, (x, y) in enumerate(ent)]}
    t = sec(1.62)
    many_hands = []
    for k, (x, c) in enumerate(zip((140, 320, 500, 680, 860), ("#b0503a", "#e9dccb", "#c8743c", "#b0503a", "#e9dccb"))):
        hh = hand(x, 1335, .33, c); hh["in"] = t(.6 + .3 * k); hh["fx"] = "pop"; many_hands.append(hh)
    # 5 · what one source would look like (ripples from a stone in a pond) against what we find (scattered dates)
    t = sec(1.69)
    vt = View(-110, 135, -55, 60, (80, 330, 840, 380))
    vb = View(-110, 135, -55, 60, (80, 900, 840, 380))
    o = vt.p(40, 20)
    ripples = [{"k": "group", "clip": [80, 330, 840, 380, 12], "in": t(3.0 + .6 * j), "els": [{"k": "circle", "x": o[0], "y": o[1], "r": 60 + 80 * j, "fill": "none", "c": "#c9c1ee", "w": 3, "style": "inferred"}]}
               for j in range(5)]
    found = [(122.6, -4.9), (-70.67, -47.15), (-6.475, 53.69), (-94.04, 18.1), (38.92, 37.22), (111.36, -7.38)]
    trail = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "map", "land": vt.land(), "in": t(.3)}, {"k": "map", "land": vb.land(), "in": t(.3)},
             I.label(500, 300, "one source?", t(.6), "#c9c1ee", 30), I.dot(o[0], o[1], 10, "#c9c1ee", t(1.6))] + ripples + \
            [I.dot(o[0] + (60 + 80 * j) * math.cos(a), o[1] + (60 + 80 * j) * math.sin(a), 6, "#c9c1ee", t(8.6 + .3 * j)) for j, a in ((0, 2.6), (1, .3), (2, 3.6), (3, 1.0))] + \
            [I.label(500, 870, "what we find", t(10.8), AMBER, 30)] + \
            [e for k, (lo, la) in enumerate(found) for e in (I.dot(*vb.p(lo, la), 9, AMBER, t(12.0 + .45 * k)), I.ring(*vb.p(lo, la), 18, t(12.0 + .45 * k), AMBER, 2, dur=.4))]}
    # 2 again (line 2 of the reversal, drawn on the return): the Assyrian 'bag' is a bucket, with a cone to sprinkle purifying water
    bucket = [I.glow(BX[2], 830, 150, 2.0, .5, "scan"), I.box(BX[2] - 48, 812, 96, 30, BLUE, r=4, at=2.4, op=.7, fx="fill"),
              {"k": "poly", "p": [[BX[2] + 60, 700], [BX[2] + 85, 640], [BX[2] + 110, 700], [BX[2] + 85, 722]], "fill": "#c9a86a", "c": "#efe6d2", "w": 1.5, "in": 3.8, "fx": "pop"}] + \
        [I.dot(BX[2] + 80 - 9 * j, 742 + 22 * j, 5, BLUE, 4.2 + .15 * j) for j in range(5)] + \
        [I.label(BX[2], 1120, "a bucket", 3.0, BLUE, 30), I.strike(BX[0] + 50, 830, BX[1] - 50, 770, 6.0), I.strike(BX[1] + 50, 830, BX[2] - 50, 770, 6.3)]
    # 0 again: one shared human brain, wired to every sign
    t = sec(1.24)
    bc = (500, 850)
    def seg(i, r0=66, r1=96):
        dx, dy = CX(i) - bc[0], CY(i) - bc[1]; d = math.hypot(dx, dy)
        return [[round(bc[0] + dx * r0 / d, 1), round(bc[1] + dy * r0 / d, 1)], [round(CX(i) - dx * r1 / d, 1), round(CY(i) - dy * r1 / d, 1)]]
    wire = [I.line(seg(i), t(8.8 + .1 * i), AMBER, 3, dur=.5) for i in range(6)] + \
        [I.oval(bc[0], bc[1], 64, 48, "#3a2a30", "#e8b8c0", 3, 1, t(8.4), fx="pop"), I.line([[bc[0], bc[1] - 46], [bc[0], bc[1] + 44]], t(8.6), "#e8b8c0", 2, draw=False)] + \
        [I.line([[bc[0] + sx * (10 + 8 * j), bc[1] - 26 + 20 * r + 5 * math.sin(j)] for j in range(5)], t(8.6), "#e8b8c0", 2, curve=True, draw=False) for sx in (1, -1) for r in range(3)] + \
        [I.ring(CX(1), CY(1), 105, t(14.6), AMBER, 4), I.ring(CX(0), CY(0), 105, t(16.6), AMBER, 4)]
    ep2 = remix(ep, scenes={0: signs, 2: handbags, 3: shapes, 4: many, 5: trail}, alias={6: 0}, cams={6: [1.05, 500, 880]}, adds={1: hands},
                beat_adds={5: (wire, None)}, line_adds={(3, 1): (many_hands, None)})
    return _revisit(ep2, 4, 1, bucket)


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/signs-ledger.json)."""
    import recap
    return recap.recap(ledger, "signs-ledger", None)


def EPISODES():
    import lg_c      # 02.02 rebuilt from the legacy film
    return [oldest_m(), lg_c.ice_age_signs_m(), notation_m(), shared_m(), holes_m(), ledger_recap()]
