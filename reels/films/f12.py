"""File 12 · Unreadable. Lost scripts, burned libraries and books no one can read.
The Indus signs, the Voynich manuscript, the Herculaneum scrolls, the Library of Alexandria, the Dead Sea Scrolls and the Piri Reis map.
Sacred texts are quoted, never rated; every date carries its hedge."""
import math, random
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box

SERIES = "Unreadable"
VELLUM = "#e8d9b8"; INK = "#3a2a1c"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


def squiggles(x0, y0, w, rows, seed=1, c=INK, lh=34, i0=.6):
    """Lines of an unknown script: loops and hooks in an ink colour, word gaps included."""
    r = random.Random(seed); out = []
    for row in range(rows):
        x = x0; y = y0 + row * lh
        while x < x0 + w - 30:
            n = r.randint(2, 5)
            for _ in range(n):
                k = r.randint(0, 3)
                if k == 0:
                    out.append({"k": "circle", "x": x + 6, "y": y - 6, "r": 6, "fill": "none", "c": c, "w": 2, "in": i0 + row * .08})
                elif k == 1:
                    out.append({"k": "line", "p": [[x, y], [x + 4, y - 18], [x + 10, y - 4], [x + 13, y]], "c": c, "w": 2, "curve": True, "in": i0 + row * .08})
                elif k == 2:
                    out.append({"k": "line", "p": [[x, y - 10], [x + 6, y], [x + 12, y - 12]], "c": c, "w": 2, "curve": True, "in": i0 + row * .08})
                else:
                    out.append({"k": "line", "p": [[x + 2, y - 20], [x + 2, y], [x + 11, y - 8]], "c": c, "w": 2, "in": i0 + row * .08})
                x += 15
            x += 16
    return out


# ---------------------------------------------------------------- 12.01 Lost scripts
def lost_scripts():
    def sign(x, y, k, c=INK):
        s = 22
        shapes = [[[x - s / 2, y - s], [x - s / 2, y], [x + s / 2, y], [x + s / 2, y - s]], [[x, y - s], [x, y]], [[x - s / 2, y - s], [x + s / 2, y]],
                  [[x - s / 2, y - s / 2], [x + s / 2, y - s / 2]], [[x - s / 2, y], [x, y - s], [x + s / 2, y]]]
        out = [{"k": "line", "p": shapes[k % 5], "c": c, "w": 4, "in": .6 + k * .1}]
        if k % 2:
            out.append({"k": "line", "p": [[x - s / 3, y - s * .8], [x + s / 3, y - s * .8]], "c": c, "w": 3, "in": .7 + k * .1})
        return out
    seal = [{"k": "rect", "x": 250, "y": 520, "w": 500, "h": 500, "fill": "#c9b38a", "c": "#f4e6c8", "sw": 2, "in": .1},
            {"k": "rect", "x": 272, "y": 542, "w": 456, "h": 456, "fill": "#b89e72", "c": "#8c7452", "sw": 1.4, "in": .2}] + \
           [e for i, k in enumerate((0, 3, 1, 4, 2)) for e in sign(340 + i * 80, 640, k)] + \
           [{"k": "poly", "p": [[330, 900], [360, 800], [460, 780], [600, 790], [660, 830], [640, 900], [610, 905], [600, 860], [420, 860], [400, 910]], "fill": "#8c7452", "c": INK, "w": 2, "curve": True, "in": 1.2},
            {"k": "line", "p": [[640, 800], [700, 740]], "c": INK, "w": 4, "in": 1.4},
            {"k": "cap", "x": 500, "y": 460, "t": "an Indus seal · about 3 cm across · schematic", "in": .2},
            {"k": "label", "x": 500, "y": 1110, "t": "five signs: a typical inscription", "c": AMBER, "in": 1.6}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": seal}
    v = View(62, 79, 20, 34, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Mohenjo-daro", 68.139, 27.329, {"c": GOLD}), ("Harappa", 72.86, 30.63, {}), ("Dholavira", 70.21, 23.89, {"a": "end", "lx": -18}), ("Lothal", 72.25, 22.52, {})],
                 extra=[{"k": "label", "x": v.p(66, 21.5)[0], "y": v.p(66, 21.5)[1], "t": "the Arabian Sea", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = stat("5", "signs", "the length of a typical Indus inscription; about 4,000 to 5,000 are known, and none is long", "Parpola 1994; Rao et al. 2009")
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("still unread", "#ffb09a", ["the Indus script · c. 2600–1900 BCE", "Linear A · Crete", "Rongorongo · Rapa Nui", "the Phaistos disc · one of a kind"])}
    s4 = stat("$1,000,000", "prize", "offered in 2025 by the government of Tamil Nadu for a decipherment of the Indus script", "Government of Tamil Nadu 2025")
    tl, ax = timeline(-3500, 2100, [(-3000, "3000 BCE"), (-1500, "1500 BCE"), (1, "1 CE"), (1500, "1500 CE")], "Scripts lost, and found")
    tl["els"] += [{"k": "band", "x0": ax.x(-2600), "x1": ax.x(-1900), "y": 700, "h": 16, "c": GOLD, "t": "the Indus script", "in": .3}] + \
                 event(ax, -1800, "Linear A", row=1, c=AMBER, i=.6) + event(ax, 1952, "Linear B read", row=2, c=SCAN, i=.9) + event(ax, 2022, "Linear Elamite read", row=1, c=SCAN, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:LOST SCRIPTS][sfx:boom][act:setting the scene, quiet wonder]^Thousands of inscriptions from one of the world's first great ^civilisations. [act:hushed, the hook lands]And ^nobody alive can read@present them.",
                      "[d:tension][cam:1.12|0|0][act:a sly aside, eyebrows up][tune:risefall]There's now a ^million-dollar prize."], cut=False),
        B("world", 1, ["[d:calm][k:THE INDUS][act:setting the scene, unhurried]The Indus valley, about {2600|twenty-six hundred} to {1900|nineteen hundred} BCE. [act:quietly impressed]Planned cities, with ^drains. [go:2|0][act:leaning in, curious]And their ^writing: tiny seals, about ^five signs long."]),
        B("collision", 0, ["[d:build][k:THE DEBATE][act:explaining, even-handed]Most experts say it's ^writing: word signs mixed with sound signs, read@past ^right to left.",
                           "[d:build][sfx:shimmer][act:the counter-claim, intrigued]But in {2004|two thousand four} three scholars argued it might not be ^language at all. [act:offering it plainly][tune:level]^Emblems. [act:a modern comparison, lighter][tune:fall]Like ^logos."]),
        B("cost", 3, ["[d:build][k:NOT ALONE][act:warm, a little conspiratorial]It has ^company. [act:counting them off][tune:level]^Linear A, on Crete. [act:next one, same rhythm][tune:level]^Rongorongo, on Easter Island. [act:the last one, landing it][tune:fall]The ^Phaistos disc.",
                      "[d:aside][act:lighter, half-smiling]Some of these we can ^sound out... [act:the gentle sting]and still not understand a ^word."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:brightening, hopeful]But scripts ^do fall. [act:plain fact, a nod]Linear ^B in {1952|nineteen fifty-two}. [sfx:hit][act:wonder, savouring it]And in {2022|twenty twenty-two}, Linear ^Elamite from Iran, cracked with royal names on ^silver cups.",
                          "[d:build][go:4|0][act:bright, raising the stakes]Now ^Tamil Nadu offers a million dollars for the Indus."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]The Indus signs write a ^language? [act:the verdict, measured][tune:fall]^*Plausible*. [act:fair, even]Most experts lean ^yes. [act:honest, a touch lower][tune:fall]Nobody has ^shown it yet.",
                     "[d:tension][p:0.93][act:quiet, the wish]What's missing is one ^long text, or one ^bilingual."]),
    ]
    return EP("lost-scripts", "12.01", "Lost Scripts: The Writing Nobody Can Read", "lost-scripts", "plausible", "Do the Indus signs write a language, and could we ever read them?", "Nobody alive can *read* them.", beats, shots,
              "Parpola 1994 · Rao et al. 2009, Science · Farmer, Sproat & Witzel 2004 · Desset et al. 2022 · Ferrara et al. 2024 · Salgarella 2020",
              "Five thousand Indus inscriptions nobody can read, a million-dollar prize, and the scripts that have fallen: is the Indus writing a language at all?",
              ["#LostScripts", "#IndusValley", "#Decipherment", "#History", "#Unreadable"])


# ---------------------------------------------------------------- 12.02 The Voynich manuscript
def voynich():
    pg = [{"k": "rect", "x": 170, "y": 430, "w": 660, "h": 900, "fill": VELLUM, "c": "#fff4dc", "sw": 1.2, "in": .1}] + \
         squiggles(210, 500, 580, 5, seed=3) + \
         [{"k": "poly", "p": [[480, 1180], [470, 1060], [440, 980], [470, 900], [520, 900], [540, 980], [520, 1060], [520, 1180]], "fill": "#5f8a4a", "c": INK, "w": 2, "curve": True, "in": 1.0},
          {"k": "poly", "p": [[500, 900], [420, 820], [380, 760], [430, 740], [500, 820]], "fill": "#7fa05a", "c": INK, "w": 2, "curve": True, "in": 1.2},
          {"k": "poly", "p": [[505, 900], [590, 820], [640, 770], [600, 740], [520, 830]], "fill": "#7fa05a", "c": INK, "w": 2, "curve": True, "in": 1.3},
          {"k": "poly", "p": [[500, 745], [470, 700], [485, 690], [500, 715], [515, 690], [530, 700]], "fill": "#b0503a", "c": INK, "w": 2, "curve": True, "in": 1.4},
          {"k": "poly", "p": [[480, 1040], [380, 1010], [340, 960], [400, 975], [480, 1010]], "fill": "#7fa05a", "c": INK, "w": 2, "curve": True, "in": 1.3},
          {"k": "poly", "p": [[520, 1040], [620, 1000], [660, 950], [600, 965], [520, 1005]], "fill": "#7fa05a", "c": INK, "w": 2, "curve": True, "in": 1.3},
          {"k": "line", "p": [[460, 1180], [420, 1250], [470, 1230], [500, 1290], [530, 1230], [580, 1250], [540, 1180]], "c": "#6b4a2e", "w": 3, "curve": True, "in": 1.5},
          {"k": "cap", "x": 500, "y": 390, "t": "a plant page · schematic", "in": .2}]
    for e in pg:                                   # sit the page below the hook title
        if "y" in e: e["y"] += 110
        if "p" in e: e["p"] = [[x, y + 110] for x, y in e["p"]]
    pg[0]["h"] = 880
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": pg}
    s1 = stat("1404–1438", "CE", "radiocarbon dates on four samples of the calfskin the book is written on", "University of Arizona 2011")
    v = View(-2, 22, 38, 55, (40, 330, 920, 900))
    s2 = mapshot(v, pins=[("Prague · the emperor's court", 14.42, 50.08, {"c": GOLD}), ("Rome · Athanasius Kircher", 12.5, 41.9, {"a": "end", "lx": -18})],
                 extra=[{"k": "line", "p": [v.p(14.42, 50.08), v.p(14.6, 46), v.p(12.5, 41.9)], "c": GOLD, "w": 1.6, "op": .7, "style": "inferred", "curve": True, "in": .9},
                        {"k": "label", "x": v.p(17.5, 45.5)[0], "y": v.p(17.5, 45.5)[1], "t": "sent in 1665/66", "st": "small", "c": GOLD, "in": 1.1}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(300), "t": "300 km"}])
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("like a language", "#8fd9b0", ["word counts follow Zipf's law", "key words cluster by section", "five scribes, two 'dialects'"], y=460, size=28) +
          grp("unlike any language", "#ffb09a", ["letters far too predictable", "words repeat in odd runs", "no reading has survived testing"], y=850, size=28)}

    def die(x, y, n):
        pts = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
        return [{"k": "rect", "x": x - 60, "y": y - 60, "w": 120, "h": 120, "fill": "#f2e8d6", "c": "#fff", "sw": 1.4, "in": .3}] + \
               [{"k": "circle", "x": x + a * 32, "y": y + b * 32, "r": 10, "fill": "#1a1511", "c": "none", "w": 0, "in": .4} for a, b in pts]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": die(330, 760, 5) + die(480, 820, 2) +
          [{"k": "rect", "x": 600, "y": 660, "w": 150, "h": 220, "fill": "#f2e8d6", "c": "#fff", "sw": 1.4, "in": .5},
           {"k": "label", "x": 675, "y": 790, "t": "7", "st": "serif", "size": 70, "c": "#9a2a1a", "halo": False, "in": .6},
           {"k": "cap", "x": 500, "y": 540, "t": "2025 · a cipher worked with dice and playing cards", "in": .2},
           {"k": "label", "x": 500, "y": 1020, "t": "Latin or Italian in, Voynich-like text out", "c": AMBER, "in": 1.0},
           {"k": "label", "x": 500, "y": 1080, "t": "a way it could have been made, not a solution", "st": "small", "in": 1.4}]}
    tl, ax = timeline(1380, 2040, [(1400, "1400"), (1600, "1600"), (1800, "1800"), (2000, "2000")], "The book's known life")
    tl["els"] += [{"k": "band", "x0": ax.x(1404), "x1": ax.x(1438), "y": 700, "h": 16, "c": GOLD, "t": "the calfskin", "in": .3},
                  {"k": "band", "x0": ax.x(1440), "x1": ax.x(1600), "y": 620, "h": 10, "c": "#6a645c", "op": .7, "t": "no record at all", "in": .5}] + \
                 event(ax, 1639, "letters to Rome", row=0, c=BONE, i=.7) + event(ax, 1912, "Voynich buys it", row=1, c=BONE, i=.9) + event(ax, 2025, "the dice cipher", row=2, c=SCAN, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.15, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE VOYNICH MANUSCRIPT][sfx:boom][act:setting the scene, measured][tune:level]Two hundred and ^forty pages. [act:building the picture][tune:level]An alphabet ^nobody knows. [act:the strangest one, with wonder][tune:fall]Plants that ^don't exist.",
                      "[d:tension][cam:1.12|0|0][act:admiring, steady]For over a century it has beaten ^every codebreaker. [act:hushed, the real puzzle][tune:rise]Is anything written there at ^all?"], cut=False),
        B("world", 1, ["[d:calm][k:THE BOOK][act:plain facts, reassuring]The calfskin is real and medieval: radiocarbon says {1404|fourteen oh four} to {1438|fourteen thirty-eight}.",
                       "[d:build][go:2|0][act:storytelling, a little wonder]By about {1600|sixteen hundred} it was in ^Prague, at the court of an emperor who collected ^wonders."]),
        B("collision", 3, ["[d:build][k:IT LOOKS LIKE LANGUAGE][act:making the case, brisk]Its word counts follow the ^same law as real languages. [act:one more point, building]Key words cluster by ^section, and match the ^pictures. [act:a surprising detail, lightly]^Five scribes wrote it."]),
        B("cost", 3, ["[d:build][k:IT DOESN'T][sfx:shimmer][act:the counterpoint, crisp]But its letters are far more ^predictable than any known language. [act:puzzled, slower]Words repeat in ^strange runs.",
                      "[d:aside][act:amused, a little wink]And people asked to write ^nonsense produce@verb text that looks a ^lot@amount like this."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:the reveal, lean in]In {2025|twenty twenty-five}, Michael Greshko built a cipher from ^dice and playing ^cards, tools of fifteenth-century Italy. [sfx:hit][act:delighted, slower]It turns ^Latin into something very like ^Voynichese.",
                          "[d:build][act:careful, a raised finger][tune:fallrise]Not a ^solution. [act:precise, calm]A way it ^could have been done."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A real ^language inside? [act:the verdict, even][tune:fall]^*Open question*. [act:firm, matter of fact]^Every claimed decipherment so far has ^failed the test.",
                     "[d:tension][p:0.93][act:dreamy, weighing both][tune:fall]Beautiful ^nonsense, or a ^message nobody can read@present. [act:warm, open-ended]^Both are still on the table."]),
    ]
    return EP("voynich", "12.02", "The Voynich Manuscript: Language or Beautiful Nonsense?", "voynich", "contested", "Does the Voynich script hide a real language, or nothing at all?", "Is anything written there *at all*?", beats, shots,
              "Beinecke MS 408 · University of Arizona 2011 · Currier 1976 · Davis 2020 · Bowern & Lindemann 2021 · Montemurro & Zanette 2013 · Greshko 2025",
              "Two hundred and forty pages in an unknown script, dated to the early 1400s: why it looks like language, why it doesn't, and the dice-and-cards cipher of 2025.",
              ["#Voynich", "#Mystery", "#Cipher", "#History", "#Unreadable"])


# ---------------------------------------------------------------- 12.03 The Herculaneum scrolls
def herculaneum():
    spiral = [[math.cos(t) * (0.6 + t * .16), 20.2, math.sin(t) * (0.6 + t * .16)] for t in [k * .25 for k in range(0, 100)]]
    sc = [{"t": "slab", "x0": -14, "x1": 14, "z0": -10, "z1": 10, "y": 0, "c": "#5a4a3a"},
          {"t": "cyl", "x": 0, "z": 0, "y": 0, "r": 4.6, "h": 20, "c": "#2a221c", "n": 26, "edge": "rgba(255,236,206,.15)"},
          {"t": "line", "p": spiral, "c": "#8c7a66", "w": 1.4, "op": .9},
          {"t": "cyl", "x": 9, "z": 3, "y": 0, "r": 2.6, "h": 7, "c": "#241d18", "n": 20, "edge": "rgba(255,236,206,.15)"},
          L_(0, 21, "a scroll, turned to charcoal · about 20 cm", GOLD, z=0, dy=-24), L_(0, 0, "open it, and it crumbles", "#ffb09a", z=10, dy=40)]
    s0 = iso(sc, cam=[1, 500, 900], s=22, x=500, y=1060, az=-24, spin=1.2, el=.45, table=None)
    v = View(13.95, 14.75, 40.55, 41.0, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Herculaneum · the Villa of the Papyri", 14.3436, 40.8076, {"c": GOLD, "a": "end", "lx": -18}), ("Vesuvius", 14.426, 40.821, {"c": RED}), ("Pompeii", 14.485, 40.749, {})],
                 extra=[{"k": "label", "x": v.p(14.15, 40.7)[0], "y": v.p(14.15, 40.7)[1], "t": "the Bay of Naples", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(5), "t": "5 km"}])
    sp2 = [[500 + math.cos(t) * (8 + t * 9), 860 + math.sin(t) * (8 + t * 9)] for t in [k * .12 for k in range(0, 260)]]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 140, "y": 500, "w": 720, "h": 720, "fill": "#0c0c0c", "c": "#3a3a3a", "sw": 1.4, "in": .1},
                                                    {"k": "line", "p": sp2, "c": "#d8d8d8", "w": 2.2, "curve": True, "in": .3, "fx": "draw", "dur": 2.0},
                                                    {"k": "cap", "x": 500, "y": 440, "t": "an X-ray slice through the roll · schematic", "in": .2},
                                                    {"k": "label", "x": 500, "y": 1290, "t": "software follows each layer, then flattens it into a page", "c": AMBER, "in": 1.8}]}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 120, "y": 640, "w": 760, "h": 340, "fill": "#1b1714", "c": "#3a3128", "sw": 1.4, "in": .1},
                                                    {"k": "label", "x": 500, "y": 850, "t": "ΠΟΡΦΥΡΑϹ", "st": "serif", "size": 96, "c": "#e9dccb", "in": .6},
                                                    {"k": "cap", "x": 500, "y": 580, "t": "the first word read inside an unopened scroll", "in": .2},
                                                    {"k": "label", "x": 500, "y": 1060, "t": "porphyras: 'purple'", "st": "ital", "c": GOLD, "in": 1.2}]}
    s4 = stat("$700,000", "prize", "the Vesuvius Challenge Grand Prize, February 2024: more than 2,000 letters from inside an unopened scroll", "Vesuvius Challenge 2024")
    tl, ax = timeline(1, 2100, [(1, "1 CE"), (500, "500"), (1000, "1000"), (1500, "1500"), (2000, "2000")], "Buried, found, read")
    tl["els"] += event(ax, 79, "Vesuvius", row=1, c=RED, i=.3) + event(ax, 1752, "the scrolls found", row=0, c=BONE, i=.6) + \
                 event(ax, 2023, "'purple'", row=2, c=SCAN, i=.9) + event(ax, 2026, "a whole scroll read", row=1, c=GOLD, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.18, 500, 980])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:HERCULANEUM][sfx:boom][act:setting the scene, vivid]In {79|seventy-nine} CE, Vesuvius buried a Roman ^library and baked its books into lumps of ^charcoal.",
                      "[d:tension][cam:1.12|0|0][act:gentle, a small wince]Open one, and it ^crumbles. [act:the puzzle, curious][tune:fall]So ^how do you read@present it?"], cut=False),
        B("world", 1, ["[d:calm][k:THE LIBRARY][act:setting the scene, easy]A ^luxury villa at Herculaneum, Pompeii's ^neighbour. [act:plain fact]About ^eighteen hundred rolls came out from {1752|seventeen fifty-two}.",
                       "[d:build][act:careful, holding back]Early attempts to unroll them read@past ^some... [act:the wince, quiet]and destroyed ^many."]),
        B("collision", 2, ["[d:build][k:THE IDEA][act:bright, the idea arrives]So ^scan them instead. [act:explaining, clear]X-rays trace every rolled ^layer, and software flattens each one into a ^page.",
                           "[d:build][act:the problem, dry]The catch: ^carbon ink on carbonised papyrus is almost ^invisible."]),
        B("cost", 3, ["[d:build][k:THE CHALLENGE][act:brisk storytelling]In {2023|twenty twenty-three}, two tech investors and a computer scientist, Brent Seales, released the ^scans and offered ^prizes.",
                      "[d:wonder][sfx:shimmer][act:childlike wonder, slowing]A twenty-one-year-old ^student found the first word: ^purple."]),
        B("reversal", 4, ["[d:reveal][k:THE BREAKTHROUGH][act:growing excitement, controlled]By {2024|twenty twenty-four}: more than two ^thousand letters, from a lost book of ^philosophy.",
                          "[d:build][go:5|0][sfx:hit][act:awe, letting it land]And in {2026|twenty twenty-six}, a ^whole scroll, read@past end to end, without ever ^opening it."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Reading ancient books nobody can ^open? [act:the verdict, warm and sure][tune:fall]^*Established*. [act:hopeful, softer]^Hundreds more are waiting.",
                     "[d:tension][p:0.93][act:quiet, a secret shared]And parts of the villa have ^never been dug. [act:wonder, gently]The library may be ^bigger."]),
    ]
    return EP("herculaneum-scrolls", "12.03", "The Herculaneum Scrolls: Reading a Burned Library", "herculaneum-scrolls", "solid", "Can we read ancient books that would crumble if anyone tried to open them?", "Open one, and it *crumbles*.", beats, shots,
              "Sider 2005 · Seales et al. 2016, Science Advances · Vesuvius Challenge 2024, 2025, 2026 · Mocella et al. 2015, Nature Communications",
              "A Roman library cooked to charcoal by Vesuvius, and the X-rays, machine learning and student prize-winners now reading scrolls nobody can open.",
              ["#Herculaneum", "#Vesuvius", "#AI", "#AncientRome", "#Unreadable"])


# ---------------------------------------------------------------- 12.04 The Library of Alexandria
def alexandria():
    shelf = [{"k": "glow", "x": 500, "y": 900, "r": 520, "kind": "red", "op": .45, "in": .8, "pulse": True}] + \
            [{"k": "circle", "x": 190 + c * 58, "y": 620 + r * 58, "r": 22, "fill": "#c9ad85", "c": "#6b4a2e", "w": 2, "in": .1 + (r * 11 + c) * .006} for r in range(9) for c in range(11)] + \
            [{"k": "cap", "x": 500, "y": 540, "t": "the story everyone knows: one night, one fire", "in": .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": shelf}
    v = View(18, 36, 28, 41, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Alexandria", 29.91, 31.21, {"c": GOLD}), ("Athens", 23.73, 37.98, {}), ("Rhodes", 28.22, 36.43, {})],
                 extra=[{"k": "label", "x": v.p(24, 34)[0], "y": v.p(24, 34)[1], "t": "the Mediterranean", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    tl, ax = timeline(-320, 1300, [(-300, "300 BCE"), (1, "1 CE"), (400, "400"), (800, "800"), (1200, "1200")], "A slow death")
    tl["els"] += event(ax, -285, "founded", row=1, c=GOLD, i=.3) + event(ax, -48, "Caesar's fire", row=0, c=RED, i=.5) + event(ax, 272, "Aurelian's war", row=2, c=RED, i=.7) + \
                 event(ax, 391, "the Serapeum", row=0, c=RED, i=.9) + event(ax, 1203, "the caliph story, written", row=1, c=SCAN, i=1.1) + \
                 [{"k": "line", "p": [[ax.x(642), 760], [ax.x(1203), 760]], "c": "#ffb09a", "w": 2, "style": "inferred", "in": 1.3},
                  {"k": "label", "x": ax.x(920), "y": 790, "t": "560 years", "st": "small", "c": "#ffb09a", "in": 1.4}]
    s2 = tl
    sus = [("Julius Caesar · 48 BCE", "burned books by the docks"), ("Emperor Aurelian · 272 CE", "wrecked the palace quarter"), ("a bishop · 391 CE", "a temple, not the Library"), ("a caliph · 642 CE", "a story written 560 years later")]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 480, "t": "four suspects for one fire", "c": AMBER, "in": .2}] +
          [e for i, (a, b) in enumerate(sus) for e in ({"k": "label", "x": 500, "y": 590 + i * 150, "t": a, "st": "serif", "size": 34, "in": .4 + i * .4},
                                                      {"k": "label", "x": 500, "y": 640 + i * 150, "t": b, "st": "small", "c": "#ffb09a", "in": .7 + i * .4})]}
    s4 = stat("560", "years", "between the Arab conquest of Alexandria and the first written story of a caliph burning its books", "Lewis 1990")
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what really killed it", "#8fd9b0", ["royal money ran out", "scholars were expelled, 145 BCE", "wars in the palace quarter", "books nobody recopied"])}
    s6 = like(s0, cam=[1.15, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE LIBRARY OF ALEXANDRIA][sfx:boom][act:setting it up, knowingly]^Everyone knows the greatest library of the ancient world ^burned to the ground.",
                      "[d:tension][cam:1.12|0|0][act:playful, a little grin][tune:fall]Quick question: ^which fire?"], cut=False),
        B("world", 1, ["[d:calm][k:THE LIBRARY][act:setting the scene, easy]Founded by Egypt's ^Greek kings around {285|two eighty-five} BCE. [act:amused, a modern touch]A ^research institute, with scholars on ^salaries.",
                       "[d:aside][act:lightly, holding up the number]^Ancient writers claim up to ^seven hundred thousand scrolls. [act:dry, a small smile]^Modern historians ^doubt it."]),
        B("collision", 3, ["[d:build][k:FOUR SUSPECTS][act:the line-up, one by one][tune:level]Julius ^Caesar, {48|forty-eight} BCE. [act:next suspect, same pace][tune:level]Emperor ^Aurelian, {272|two seventy-two} CE. [act:keeping the rhythm][tune:level]A ^bishop, in {391|three ninety-one}. [act:the last one, landing it][tune:fall]A ^caliph, in {642|six forty-two}."]),
        B("cost", 2, ["[d:build][k:THE ALIBIS][act:detective, laying out evidence]After Caesar's fire, the geographer ^Strabo worked at the institute. [act:dry, the alibi holds]It was ^still running.",
                      "[d:build][act:careful, precise]In {391|three ninety-one}, a ^temple was destroyed, the Serapeum. [act:even, weighing the sources]^No writer of the time says it ^still held a great library."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][sfx:hit][act:the reveal, slower]And the caliph story first appears about five hundred and ^sixty years after the conquest. [act:calm, scholarly]Historians call it a late ^invention.",
                          "[d:build][go:5|0][act:thoughtful, counting them off]What killed the library was ^slower: lost ^funding, expelled ^scholars, wars, and books nobody ^recopied."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]^One great fire? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:turning it over][tune:rise]A great ^loss of knowledge? [act:sincere, simple][tune:fall]^Real. [act:quiet, the key idea][tune:fall]And ^slow.",
                     "[d:tension][p:0.93][act:gentle, thoughtful][tune:fallrise]Libraries don't ^only burn. [gap:0.45][act:the last word, quiet][tune:fall]They ^starve."]),
    ]
    return EP("alexandria-library", "12.04", "The Library of Alexandria Did Not Burn in a Day", "alexandria-library", "debunked", "Was the Library destroyed in one catastrophe, and what did we really lose?", "Quick question: *which* fire?", beats, shots,
              "Bagnall 2002 · El-Abbadi 1990 · Strabo 17.1.8 · Cassius Dio 42.38 · Lewis 1990 · Fraser 1972",
              "Everyone knows the Library of Alexandria burned. Four suspects, four alibis, a story written 560 years late, and the slower way great libraries really die.",
              ["#LibraryOfAlexandria", "#AncientEgypt", "#History", "#Books", "#Unreadable"])


# ---------------------------------------------------------------- 12.05 The Dead Sea Scrolls
def dead_sea():
    jars = [{"t": "slab", "x0": -14, "x1": 14, "z0": -9, "z1": 9, "y": 0, "c": "#8c7452"}]
    for i, (x, z, h) in enumerate(((-7, -2, 6), (-2, 2, 6.6), (3, -3, 5.8), (8, 1.5, 6.2))):
        jars += [{"t": "cyl", "x": x, "z": z, "y": 0, "r": 1.7, "h": h, "c": "#c9a57a", "n": 18, "edge": "rgba(0,0,0,.2)"},
                 {"t": "cyl", "x": x, "z": z, "y": h, "r": 1.9, "h": .7, "c": "#b8946a", "n": 18, "edge": "rgba(0,0,0,.25)"}]
    jars += [{"t": "person", "x": 11, "y": 0, "z": 6, "h": 1.7}, L_(0, 7.4, "tall clay jars, as found in Cave 1 · schematic", GOLD, z=0, dy=-26), L_(0, 0, "the caves above Qumran", "#cfe6ff", z=8, dy=40)]
    s0 = iso(jars, cam=[1, 500, 900], s=26, x=500, y=1020, az=-24, spin=1.2, el=.45, table=None)
    v = View(34.6, 36.1, 30.9, 32.4, (40, 330, 920, 900))
    DS = [(35.39, 31.76), (35.55, 31.76), (35.58, 31.5), (35.52, 31.2), (35.45, 31.05), (35.38, 31.2), (35.37, 31.5)]
    s1 = mapshot(v, pins=[("Qumran", 35.4592, 31.7417, {"c": GOLD, "a": "start", "ly": -22}), ("Jerusalem", 35.2137, 31.7683, {"a": "end", "lx": -18, "ly": 34})],
                 extra=[{"k": "poly", "p": [v.p(a, b) for a, b in DS], "fill": "#1f4f6d", "c": "#6fa7c9", "w": 1.2, "curve": True, "in": -1},
                        {"k": "label", "x": v.p(35.47, 31.4)[0], "y": v.p(35.47, 31.4)[1], "t": "the Dead Sea", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(20), "t": "20 km"}])
    s2 = stat("981", "manuscripts", "from about 15,000 fragments found in 11 caves near Qumran, 1947 to 1956", "Tov 2002")
    gy = 1120
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "line", "p": [[180, gy], [820, gy]], "c": "#8c7152", "w": 2, "in": .1},
                                                    {"k": "rect", "x": 250, "y": gy - 8 * 16, "w": 170, "h": 8 * 16, "fill": "#ffb09a", "c": "none", "sw": 0, "in": .4, "fx": "grow"},
                                                    {"k": "rect", "x": 580, "y": gy - 32 * 16, "w": 170, "h": 32 * 16, "fill": "#8fd9b0", "c": "none", "sw": 0, "in": 1.0, "fx": "grow"},
                                                    {"k": "label", "x": 335, "y": gy - 8 * 16 - 20, "t": "8 volumes", "st": "serif", "size": 34, "in": .8},
                                                    {"k": "label", "x": 665, "y": gy - 32 * 16 - 20, "t": "32 volumes", "st": "serif", "size": 34, "in": 1.4},
                                                    {"k": "label", "x": 335, "y": gy + 40, "t": "1955–1990 · 35 years", "st": "small", "in": .6},
                                                    {"k": "label", "x": 665, "y": gy + 40, "t": "1991–2009 · 19 years", "st": "small", "in": 1.2},
                                                    {"k": "cap", "x": 500, "y": 460, "t": "the official edition, before and after 1991", "in": .2}]}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 170 + (i % 5) * 136, "y": 620 + (i // 5) * 136, "w": 116, "h": 116, "fill": "#1b1714", "c": "#c9ad85", "sw": 1.2, "in": .3 + i * .04} for i in range(15)] +
          [{"k": "cap", "x": 500, "y": 540, "t": "22 September 1991", "in": .2},
           {"k": "label", "x": 500, "y": 1110, "t": "a library in California opens its photographs of every scroll", "c": AMBER, "in": 1.2}]}
    tl, ax = timeline(1940, 2020, [(1940, "1940"), (1960, "1960"), (1980, "1980"), (2000, "2000"), (2020, "2020")], "Four decades")
    tl["els"] += event(ax, 1947, "the first scrolls", row=1, c=GOLD, i=.3) + event(ax, 1952, "Cave 4", row=0, c=BONE, i=.5) + \
                 event(ax, 1991, "the doors open", row=2, c=SCAN, i=.8) + event(ax, 2009, "the last volume", row=0, c=SCAN, i=1.1)
    s5 = tl
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE DEAD SEA SCROLLS][sfx:boom][act:respectful, a sense of awe]The ^greatest manuscript find of the ^twentieth century.",
                      "[d:tension][cam:1.12|0|0][act:measured, one eyebrow up]And for ^forty years, a small team decided who could ^see it."], cut=False),
        B("world", 1, ["[d:calm][k:THE FIND][act:setting the scene, with care]From {1947|nineteen forty-seven}, in ^caves above the Dead Sea: about ^fifteen thousand fragments. [go:2|0][act:quiet wonder]Nearly a ^thousand different manuscripts, ^two thousand years old."]),
        B("collision", 3, ["[d:build][k:THE TEAM][act:plain storytelling]The thousands of scraps from Cave ^Four went to a ^small international team in Jerusalem.",
                           "[d:build][sfx:shimmer][act:dry, let the number land]In ^thirty-five years, the official edition published ^eight volumes."]),
        B("cost", 5, ["[d:build][k:THE WAIT][act:patient, a little weary]Scholars ^outside the team waited for ^decades. [act:lowering the voice, the rumour][tune:rise]And ^rumours grew: were the texts being hidden because of what they ^said?"]),
        B("reversal", 4, ["[d:reveal][k:THE BREAK][act:the break, quickening]In {1991|nineteen ninety-one}, two scholars rebuilt unpublished texts by ^computer. [sfx:hit][act:warm triumph, open arms]^Days later, a library in California opened its photographs to ^everyone.",
                          "[d:build][go:3|0][act:bright, the contrast lands]The next ^nineteen years: ^thirty-two volumes. [d:aside][act:respectful, calm and even]And ^no secret that shook any church."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A small group restricting access for ^decades? [act:the verdict, plain][tune:fall]^*Established*. [act:the second charge, fair][tune:rise]Texts hidden for what they ^said? [act:measured, respectful]^Nothing released since supports it.",
                     "[d:tension][p:0.93][act:the last word, gentle]The scandal was ^slowness, not secrets."]),
    ]
    return EP("scrolls-monopoly", "12.05", "The Dead Sea Scrolls: Forty Years Behind Closed Doors", "scrolls-monopoly", "solid", "Was access to the Dead Sea Scrolls restricted for decades by a small group?", "A small team decided who could *see* it.", beats, shots,
              "Tov 2002 · Schiffman 1994 · Vermes 2010 · DJD series 1955–2009 · Qimron v. Shanks 2000 · Library of Congress",
              "The century's greatest manuscript find, held by a small team for four decades: the eight volumes, the rumours, and the California library that opened the vault in 1991.",
              ["#DeadSeaScrolls", "#Qumran", "#History", "#Archaeology", "#Unreadable"])


# ---------------------------------------------------------------- 12.06 The Piri Reis map
def piri_reis():
    coast = [[300, 520], [330, 600], [360, 700], [420, 780], [470, 880], [480, 980], [470, 1060], [520, 1110], [620, 1130], [720, 1150], [820, 1160]]
    mp = [{"k": "poly", "p": [[180, 450], [820, 440], [860, 1250], [160, 1260]], "fill": "#d9c29a", "c": "#f4e6c8", "w": 1.4, "in": .1},
          {"k": "line", "p": coast, "c": "#6b4a2e", "w": 4, "curve": True, "in": .4, "fx": "draw", "dur": 1.6},
          {"k": "line", "p": [[470, 1060], [520, 1110], [620, 1130], [720, 1150], [820, 1160]], "c": "#b0301e", "w": 6, "curve": True, "op": .7, "in": 2.0, "fx": "draw", "dur": 1.0},
          {"k": "label", "x": 300, "y": 760, "t": "South America", "st": "ital", "c": "#6b4a2e", "halo": False, "in": 1.2},
          {"k": "label", "x": 640, "y": 1210, "t": "the 'southern coast'", "st": "small", "c": "#b0301e", "halo": False, "in": 2.4},
          {"k": "cap", "x": 500, "y": 400, "t": "Piri Reis · 1513 · the surviving third · schematic", "in": .2}]
    for e in mp:
        if "y" in e: e["y"] += 100
        if "p" in e: e["p"] = [[x, y + 100] for x, y in e["p"]]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": mp}
    v = View(-85, 25, -75, 15, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("the Drake Passage · about 800 km of sea", -64, -58, {"c": SCAN, "a": "start", "ly": 34}), ("Queen Maud Land", 0, -71, {"c": GOLD, "a": "end", "lx": -18}),
                          ("Brazil", -45, -10, {})],
                 extra=[{"k": "cap", "x": 500, "y": 390, "t": "the claim, and the geography", "in": .2}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(1000), "t": "1,000 km"}])
    s2 = stat("34", "million years", "how long Antarctica has carried ice sheets; Europeans first sighted its coast in 1820", "DeConto & Pollard 2003")
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("his sources, in his own note", AMBER, ["about twenty charts", "maps after Ptolemy", "an Arab map of India", "four Portuguese maps", "a lost map by Columbus"])}
    s4 = stat("0", "km", "of sea shown between South America and the 'southern coast'; the real gap, the Drake Passage, is about 800 km wide", "McIntosh 2000")
    tl, ax = timeline(1480, 2030, [(1500, "1500"), (1650, "1650"), (1800, "1800"), (1950, "1950")], "The map's life")
    tl["els"] += event(ax, 1492, "Columbus", row=0, c=BONE, i=.3) + event(ax, 1513, "the map", row=1, c=GOLD, i=.5) + event(ax, 1820, "Antarctica first seen", row=2, c=SCAN, i=.8) + \
                 event(ax, 1929, "found in Topkapı", row=0, c=BONE, i=1.0) + event(ax, 1966, "Hapgood's book", row=1, c=AMBER, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE PIRI REIS MAP][sfx:boom][act:setting the scene, intrigued]An Ottoman ^admiral's map from {1513|fifteen thirteen}. [act:lowering the voice, pointing]And along the ^bottom, a ^coastline.",
                      "[d:tension][cam:1.12|0|0][act:wide-eyed, testing the idea][tune:rise]Antarctica, mapped before the ^ice? [act:plain, noncommittal]That's the ^claim."], cut=False),
        B("world", 0, ["[d:calm][k:THE MAP][act:warm storytelling]Piri Reis drew it on ^gazelle skin. [act:a small sigh]Only a ^third survives. [go:3|0][act:delighted, the good part]And he wrote down his ^sources: about ^twenty charts, ^Portuguese ones, and a lost map by ^Columbus."]),
        B("collision", 1, ["[d:build][k:THE CASE][act:laying out the claim, fairly]In {1966|nineteen sixty-six}, the historian Charles Hapgood argued the bottom coast is Queen ^Maud Land in Antarctica, drawn before the ^ice.",
                           "[d:build][sfx:shimmer][act:light, matter of fact]Graham Hancock opened his ^bestseller with it."]),
        B("cost", 2, ["[d:build][k:THE ICE][act:gently firm, the big number]But Antarctica has been under ice sheets for about thirty-four ^million years.",
                      "[d:aside][act:amused, a sense of scale]^Our species has been around for about three hundred ^thousand of them."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][sfx:hit][act:lean in, pointing at it]And ^look at the map: the southern coast runs ^straight on from South America. [act:pointed, one by one][tune:level]No ^Drake Passage. [act:the clincher, firm][tune:fall]No ^eight hundred kilometres of sea.",
                          "[d:build][go:0|0][act:calm explanation, satisfying]Most historians read@present it as South America's ^own coast, bent east to fit the ^skin."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Antarctica before the ^ice? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:warming up, admiring][tune:rise]A ^brilliant map of a brand-new world, from ^twenty sources, in {1513|fifteen thirteen}? [act:wholehearted, a smile][tune:highfall]^Absolutely.",
                     "[d:tension][p:0.93][act:the moral, softly]Sometimes the ^real story is the ^sources."]),
    ]
    return EP("piri-reis", "12.06", "The Piri Reis Map: Antarctica Before the Ice?", "piri-reis", "debunked", "Does a map from 1513 show Antarctica's coast free of ice?", "Antarctica, mapped before the *ice*?", beats, shots,
              "Piri Reis 1513, trans. İnan 1954 · Kahle 1933 · McIntosh 2000 · Hapgood 1966 · DeConto & Pollard 2003",
              "An Ottoman admiral's chart of 1513 with a mysterious southern coast: the Antarctica claim, the ice that says no, and the twenty sources Piri Reis wrote down himself.",
              ["#PiriReis", "#Antarctica", "#Maps", "#History", "#Unreadable"])


# ---------------------------------------------------------------- 12.07 The ledger
def _ledger_text():
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 200, "y": 500, "w": 600, "h": 760, "fill": VELLUM, "c": "#fff4dc", "sw": 1.2, "in": .1}] + squiggles(240, 580, 520, 14, seed=9, i0=.3) +
          [{"k": "cap", "x": 500, "y": 440, "t": "what we can read, and what we can't", "in": .2}]}
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["unopened Roman scrolls, now readable", "the Dead Sea Scrolls were held back", "Alexandria died slowly"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Plausible", "#e8c86a", ["the Indus signs write a language"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Open question", "#e8b87a", ["a real language in the Voynich"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["one great fire at Alexandria", "Antarctica on the Piri Reis map"])}
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:UNREADABLE][sfx:boom][act:the roll call, with relish]Lost ^scripts, burned ^libraries and books nobody can ^read@present. [act:inviting, a little smile]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, plain]Roman scrolls nobody can ^open are being ^read@past. [act:even, on the record]The Dead Sea Scrolls were held ^back for ^decades. [act:gentle, correcting the myth]And Alexandria's library died ^slowly, not in one night."]),
        B("collision", 2, ["[d:build][k:PLAUSIBLE][act:measured, leaning yes]The Indus signs ^probably write a language. [go:3|0][d:tension][act:a playful shrug][tune:rise]The ^Voynich? [act:honest, open-minded]A genuine ^open question."]),
        B("cost", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:firm, closing the file][tune:level]One great ^fire at Alexandria. [act:the second one, firm][tune:fall]Antarctica before the ^ice, on a map from {1513|fifteen thirteen}."]),
        B("reversal", 5, ["[d:build][k:THE PATTERN][act:reflective, slower]The real losses were ^quiet: books not recopied, scripts with ^no one left to read@present them. [d:aside][act:warmer, hopeful]And the real ^rescues are quiet too: patience, and now ^machines."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:warm conviction]Every ^unread page is still ^evidence. [act:tender, a smile]It's just waiting for a ^reader.",
                     "[d:tension][p:0.93][act:the house motto, calm]^Coherence is the measure. [act:quiet, the last word]Not ^final demonstration."]),
    ]
    return EP("unreadable-ledger", "12.07", "Unreadable · The Ledger", "", "mixed", "What we can read, what we can't, and what was never there.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 12",
              "The verdicts of Unreadable in one ledger: the scrolls now being read, the scripts still waiting, and the famous stories that are ruled out.",
              ["#History", "#Books", "#Decipherment", "#Unreadable", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: six unread (or re-read) libraries in a cabinet (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    C = Cabinet([
        {"name": "Herculaneum", "model": mdl(herculaneum())},
        {"name": "The Dead Sea Scrolls", "model": mdl(dead_sea())},
        {"name": "Alexandria", "model": mdl(alexandria(), 0)},
        {"name": "The Indus signs", "model": mdl(lost_scripts(), 0)},
        {"name": "The Voynich", "model": mdl(voynich(), 0)},
        {"name": "The Piri Reis map", "model": mdl(piri_reis(), 0)},
    ])
    C.build()
    HE, DS, AL, IN, VO, PR = range(6)
    c = C.cells[HE]
    read = C.local(HE, squiggles(-170, -296, 340, 2, seed=5, c="#9fd0ff", lh=30, i0=.9))
    scan = C.local(HE, [{"k": "line", "p": [[-190, -330], [190, -330]], "c": "#9fd0ff", "w": 3, "op": .8, "keepop": True, "in": .6, "fx": "draw", "dur": .7}])
    s1 = C.step(C.cam_cell(HE), C.verdict(HE, "established", "being read", .3) + scan + read)
    s2 = C.step(C.cam_cell(DS), C.verdict(DS, "established", "held back for decades", .3))
    s3 = C.step(C.cam_cell(AL), C.verdict(AL, "established", "a slow death", .3))
    s4 = C.step(C.cam_cell(IN), C.verdict(IN, "plausible", "a language, probably", .3))
    s5 = C.step(C.cam_cell(VO))
    s6 = C.step(C.cam_cell(VO), C.verdict(VO, "open", at=.1) + C.question(VO, dx=C.w * .32, dy=-200, at=.3, size=80))
    s7 = C.step(C.cam_cell(AL), C.verdict(AL, "ruled", at=.1) + C.struck(AL, "one great fire", at=.2))
    s8 = C.step(C.cam_cell(PR), C.verdict(PR, "ruled", at=.1) + C.struck(PR, "ice-free Antarctica", at=.2))
    s9 = C.step(C.cam_cells([AL, IN]), [e for k, i in enumerate((AL, IN)) for e in C.wash(i, "#6a645c", at=.4 + .3 * k, op=.22)])
    s10 = C.step(C.cam_cells([HE, DS]), [e for k, i in enumerate((HE, DS)) for e in C.wash(i, VCOL["established"], at=.4 + .3 * k, op=.12)])
    s11 = C.step(C.cam_all(), [e for k, i in enumerate((IN, VO)) for e in C.wash(i, "#f2b36b", at=.3 + .3 * k, op=.14)])
    s12 = C.step(C.cam_all(), [{"k": "glow", "x": C.cells[i]["cx"], "y": C.cells[i]["cy"], "r": C.w * .7, "kind": "lamp", "op": .6, "keepop": True, "in": .3 + .3 * k} for k, i in enumerate((IN, VO))])
    s13 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5, (0, 2): "%d|.3" % s6}),
        3: (s7, {(0, 1): "%d|1.1" % s8}),
        4: (s9, {(0, 1): "%d|1.2" % s10}),
        5: (s11, {(0, 1): "%d|.4" % s12, (1, 0): "%d|3" % s13}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def _mur():
    from mural import remix
    import illus
    return remix, illus


def alexandria_m():
    """The Library of Alexandria as one continuous take (see mural.py): four suspects, their alibis, a story 560 years late, and a slow death."""
    remix, I = _mur()
    ep = alexandria()
    SCR = "#e8dcc2"
    scroll = lambda x, y, at, op=None, c=SCR, style="known": [I.box(x - 34, y - 9, 68, 18, c if style == "known" else "none", "#8a7a66" if style == "known" else c, 1.5, 9, at, op=op, style=style)]
    claims = [I.box(360, 1180 - 22 * k, 90, 20, SCR, "#8a7a66", 1.5, 10, .2 + .05 * k) for k in range(5)] + \
             [I.box(360, 580, 90, 490, "none", I.LILAC, 3, 10, 1.4, style="claimed")] + I.question(560, 820, 3.6, 80)
    X = lambda yr: 150 + 700 * (yr + 100) / 800
    suspects = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[120, 1150], [880, 1150]], .1, "#8c7152", 3)] +
                sum([[I.person(X(yr), 1150, 180, at), I.line([[X(yr) + 20, 1020], [X(yr) + 40, 960]], at + .2, "#8a5d33", 6, draw=False),
                      I.glow(X(yr) + 42, 950, 60, at + .3, .9, "fire"), I.label(X(yr), 1200, lab, at, I.AMBER, 28)]
                     for yr, lab, at in ((-48, "48 BCE", .5), (272, "272", 2.4), (391, "391", 4.2), (642, "642", 6.0))], [])}
    X2 = lambda yr: 150 + 700 * (yr - 600) / 700
    late = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[120, 1100], [880, 1100]], .1, "#8c7152", 3),
            I.dot(X2(642), 1100, 12, I.AMBER, .3), I.label(X2(642), 1150, "642", .3, I.AMBER, 30),
            I.arrow([[X2(642), 1040], [X2(950), 980], [X2(1203), 1040]], .8, I.BONE, 3, dur=2.2),
            I.label(X2(922), 940, "560 years", 1.6, I.BONE, 40, st="serif"),
            I.dot(X2(1203), 1100, 12, I.LILAC, 3.0), I.label(X2(1203), 1150, "c. 1200", 3.0, I.LILAC, 30)] + scroll(X2(1203), 1220, 3.4, c=I.LILAC, style="claimed")}
    shelf = [I.box(160, 560 + 110 * r, 680, 12, "#5a4330", r=2, at=.1) for r in range(4)] + \
            sum([scroll(220 + 80 * j, 548 + 110 * r, .2 + .02 * (j + 8 * r), op=.35 if (j + r) % 3 == 0 else None) for r in range(4) for j in range(8)], [])
    slow = {"base": "dark", "cam": [1, 500, 900], "els": shelf +
            [I.dot(250 + 30 * k, 1110, 16, "#e8c35a", 1.0 + .1 * k) for k in range(4)] + [I.strike(220, 1140, 380, 1080, 1.8, I.RED, 4)] +
            [I.person(480 + 45 * k, 1150, 110, 2.6 + .2 * k) for k in range(3)] + [I.arrow([[470, 1170], [640, 1190], [720, 1170]], 3.0, I.LILAC, 3, "claimed", .8)] +
            [I.glow(800, 1080, 90, 3.8, .8, "fire")] + [I.box(160, 540, 680, 460, "#120d0a", r=4, at=5.0, op=.45, dur=2.5)]}
    return remix(ep, scenes={3: suspects, 4: late, 5: slow}, alias={6: 0}, cams={0: [1.1, 500, 880], 6: [1.15, 500, 900], 2: [1.35, 500, 830]},
                 drop=("para", "num", "title", "q", "cap"), line_adds={(1, 1): (claims, None)})


def piri_reis_m():
    """The Piri Reis map as one continuous take (see mural.py): twenty sources, thirty-four million years of ice, and a missing sea."""
    remix, I = _mur()
    ep = piri_reis()
    lost = [I.box(170, 520, 660, 760, "none", I.LILAC, 3, 8, 2.2, style="claimed")]
    src = []
    for k in range(20):
        a = math.pi * (.08 + .84 * k / 19)
        x, y = 500 - 360 * math.cos(a), 900 - 330 * math.sin(a)
        c = I.AMBER if k in (5, 7, 9, 11) else (I.LILAC if k == 14 else "#cbbca8")
        st = "claimed" if k == 14 else "known"
        src += [I.box(x - 26, y - 20, 52, 40, "none", c, 2.5, 4, 1.0 + .12 * k, style=st), I.line([[x, y + 20], [500, 1080]], 1.3 + .12 * k, c, 1.5, "inferred" if k != 14 else "claimed", .6)]
    sources = {"base": "dark", "cam": [1, 500, 900], "els": src + [I.box(400, 1080, 200, 150, "#cdb58a", "#8a6a48", 2, 4, .5), I.glow(500, 1150, 140, 4.0, .4)]}
    ice = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[120, 900], [880, 900]], .3, "#e6f0f7", 34, dur=3.0), I.label(500, 840, "34 million years of ice", .6, "#e6f0f7", 32),
           I.line([[874, 880], [880, 880]], 4.4, I.AMBER, 40, draw=False), I.glow(877, 900, 60, 4.4, .9), I.person(877, 1120, 120, 4.8),
           I.arrow([[877, 990], [877, 930]], 5.0, I.AMBER, 3, dur=.4, curve=False), I.label(877, 1180, "us", 5.2, I.AMBER, 32, "end")]}
    coast = I.line([[140, 640], [200, 760], [230, 900], [260, 1040], [340, 1120], [520, 1150], [700, 1160], [860, 1170]], .4, "#cdb58a", 6, dur=2.0, curve=True)
    gap = {"base": "map", "cam": [1, 500, 900], "els": [coast, I.label(600, 1220, "the map", .8, "#cdb58a", 28),
           {"k": "poly", "p": [[520, 520], [600, 560], [640, 700], [620, 820], [580, 900], [560, 820], [530, 700]], "fill": "#6f5a44", "c": "none", "w": 0, "in": 3.2, "curve": True},
           {"k": "poly", "p": [[420, 1300], [560, 1250], [760, 1260], [900, 1320], [900, 1420], [420, 1420]], "fill": "#e6f0f7", "c": "none", "w": 0, "in": 3.6, "curve": True},
           I.arrow([[580, 920], [590, 1240]], 4.4, I.BLUE, 3, dur=.8, curve=False), I.arrow([[590, 1240], [580, 920]], 4.4, I.BLUE, 3, dur=.8, curve=False),
           I.label(610, 1090, "800 km of sea", 4.8, I.BLUE, 30, "start")]}
    return remix(ep, scenes={2: ice, 3: sources, 4: gap}, alias={5: 0, 6: 0}, cams={0: [1.1, 500, 880], 6: [1.12, 500, 880]},
                 drop=("para", "num", "title", "q", "cap"), beat_adds={1: (lost, None)})


def lost_scripts_m():
    """Lost scripts as one continuous take (see mural.py): thousands of tiny seals, three unread neighbours, a prize."""
    remix, I = _mur()
    ep = lost_scripts()
    C = "#e8dcc2"
    seals = [I.box(150 + 58 * (k % 12), 560 + 58 * (k // 12), 44, 44, "#b9ab94", "#8a7a66", 1, 4, .3 + .012 * k) for k in range(96)]
    big = [I.box(330, 1100, 340, 150, "#b9ab94", "#8a7a66", 2, 8, 1.8, fx="pop")] + [I.line([[380 + 60 * j, 1135], [380 + 60 * j, 1215]], 2.2 + .35 * j, I.INK, 6, dur=.3) for j in range(5)]
    debate = [I.arrow([[700, 760], [300, 760]], 2.0, I.AMBER, 4, dur=1.2, curve=False)] + [I.ring(500, 900, 230, 6.8, I.LILAC, 3, "claimed", 1.0)] + I.question(760, 640, 7.4, 70)
    tab = [I.box(110, 640, 220, 300, "#b9a47c", "#8a6a48", 2, 6, .6)] + [I.line([[130, 680 + 30 * j], [310, 680 + 30 * j]], .8 + .05 * j, I.INK, 2, "inferred", .3) for j in range(8)]
    rongo = [I.box(390, 660, 220, 280, "#6b4a2e", "#3b2a1c", 2, 30, 2.0)] + sum([[I.line([[410 + 26 * j, 700 + 40 * r], [420 + 26 * j, 690 + 40 * r], [430 + 26 * j, 700 + 40 * r]], 2.2 + .01 * (j + 7 * r), C, 2, draw=False)
                                                                           for j in range(7)] for r in range(6)], [])
    disc = [I.oval(780, 790, 120, 120, "#c9a06a", "#8a6a48", 2, 1, 3.6)] + [I.line([[780 + (20 + 12 * t) * math.cos(t), 790 + (20 + 12 * t) * math.sin(t)] for t in [j * .2 for j in range(45)]], 3.8, I.INK, 2, dur=1.2, curve=True)]
    company = {"base": "dark", "cam": [1, 500, 880], "els": tab + rongo + disc + [I.ring(220, 790, 190 + 40 * k, 6.0 + .3 * k, I.BLUE, 2, "inferred", .6) for k in range(2)] + I.question(220, 1120, 7.4, 70)}
    prize = {"base": "dark", "floor": 1150, "cam": [1, 500, 900], "els": [I.box(380, 1000, 240, 150, "#5a4330", "#8a6a48", 2, 6, .2),
             I.box(400, 850, 200, 150, "#b9ab94", "#8a7a66", 2, 8, .5, fx="pop")] + [I.line([[430 + 36 * j, 880], [430 + 36 * j, 960]], .7 + .1 * j, I.INK, 5, dur=.2) for j in range(5)] +
            [I.glow(500, 900, 260, 1.0, .7), I.label(500, 760, "$1,000,000", 1.4, I.AU, 64, st="big", fx="pop")]}
    return remix(ep, scenes={2: {"base": "dark", "cam": [1, 500, 880], "els": seals + big}, 3: company, 4: prize}, alias={6: 0},
                 cams={0: [1.1, 500, 880], 6: [1.15, 500, 880]}, drop=("para", "num", "title", "q", "cap", "label"),
                 beat_adds={2: (debate, [1.1, 500, 880])})


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/unreadable-ledger.json)."""
    import recap
    return recap.recap(ledger, "unreadable-ledger", None)


def EPISODES():
    return [lost_scripts_m(), voynich(), herculaneum(), alexandria_m(), dead_sea(), piri_reis_m(), ledger_recap()]
