"""File 00 · The Method. How we weigh the past, and how you can too.
The cases where nature or hoaxers fooled us: Oklo's natural reactors, the out-of-place artefacts, and the ancient astronauts."""
import math, random
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, papyrus, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box, sphere

SERIES = "The Method"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


# ---------------------------------------------------------------- 00.04 Oklo
def oklo():
    ore = [box(0, 0, 0, 40, 24, 4, "#8c7452"), box(0, 0, 4, 40, 24, 2.2, "#3a3128", "rgba(255,236,206,.3)"), box(0, 0, 6.2, 40, 24, 5, "#b8a57c"), box(0, 0, 11.2, 40, 24, 3, "#c9b894"),
           {"t": "glow", "x": 4, "y": 5.1, "z": 4, "r": 120, "kind": "red", "pulse": True},
           {"t": "line", "p": [[-20, 12, -8], [-10, 8, -4], [0, 5.2, 0]], "c": "#9fd0ff", "w": 3, "op": .9, "style": "inferred"},
           L_(-14, 14.2, "groundwater seeps in", "#9fd0ff", z=-8, dy=-18), L_(4, 6.2, "a uranium-rich seam · a reactor zone", GOLD, z=4, dy=-40),
           L_(0, 0, "sandstone, cut open · schematic", "#cfe6ff", z=12, dy=40)]
    s0 = iso(ore, cam=[1, 500, 900], s=12, x=500, y=1000, az=-26, spin=1.2, el=.45, table=None)
    v = View(7, 16.5, -5.2, 3, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Oklo", 13.16, -1.394, {"c": GOLD}), ("Libreville", 9.45, 0.39, {})],
                 extra=[{"k": "label", "x": v.p(12, -3.2)[0], "y": v.p(12, -3.2)[1], "t": "Gabon", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = stat("0.717%", "uranium-235", "in a 1972 sample from Oklo; in uranium everywhere else on Earth: 0.720%", "Meshik 2005")
    bars = []
    x = 140
    for k in range(4):
        bars += [{"k": "rect", "x": x, "y": 820, "w": 34, "h": 60, "fill": RED, "c": "none", "sw": 0, "in": .3 + k * .3},
                 {"k": "rect", "x": x + 34, "y": 820, "w": 150, "h": 60, "fill": "#2b5d7d", "c": "none", "sw": 0, "in": .45 + k * .3}]
        x += 184
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": bars + [{"k": "cap", "x": 500, "y": 700, "t": "a natural reactor with an off switch", "in": .2},
                                                            {"k": "label", "x": 157, "y": 940, "t": "30 min on", "st": "small", "c": "#ffb09a", "a": "start", "in": 1.2},
                                                            {"k": "label", "x": 250, "y": 780, "t": "2.5 h off", "st": "small", "c": "#9fd0ff", "a": "start", "in": 1.4},
                                                            {"k": "label", "x": 500, "y": 1060, "t": "water slows the neutrons · fission heats it · it boils away · fission stops · water returns", "st": "small", "c": AMBER, "in": 1.8}]}
    tl, ax = timeline(-2600, 0, [(-2500, "2.5 bn yrs ago"), (-2000, "2.0"), (-1000, "1.0"), (0, "today")], "Why only then")
    tl["els"] += event(ax, -2400, "oxygen builds up in the air", row=1, c=SCAN, i=.3, sub="uranium dissolves in water") + event(ax, -2000, "the reactors run", row=2, c=GOLD, i=.6, sub="fissile uranium: about 3.7%") + \
                 event(ax, 0, "today: 0.72%", row=0, c=BONE, i=.9)
    s4 = tl
    s5 = stat("16", "reactor zones", "found in the Franceville basin: the only natural nuclear reactors known", "Gauthier-Lafaye et al. 1996; Meshik 2005")
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 1, ["[d:intrigue][k:OKLO · GABON][sfx:boom][act:setting the scene, a hint of wonder]In {1972|nineteen seventy-two}, French engineers found uranium that had ^already been burned in a nuclear ^reactor.",
                      "[d:tension][cam:1.12|0|0][act:the reveal, slow, wide-eyed][tune:fall]The reactor had shut down ^two billion years ^earlier."], cut=False),
        B("world", 2, ["[d:calm][k:THE CLUE][act:patient, laying out the clue]Uranium everywhere on Earth holds the ^same share of the fissile kind: zero point seven ^two percent. [act:dropping the clue, pointed]Oklo's had ^less. [act:quieter, the bigger surprise]Some samples, ^much less.",
                       "[d:build][act:slow, a detective's conclusion]^Something had used@verb it up."]),
        B("collision", 5, ["[d:build][k:THE CASE][act:presenting the claim, fair, a touch playful]Online, it's an ancient nuclear ^plant, built by ^someone. [act:giving the argument its due]After all, it took the ^Manhattan Project@noun for humans to make a chain reaction.",
                           "[d:aside][act:lighter, adding fuel]And it's happened in only ^one basin on Earth."]),
        B("cost", 4, ["[d:build][k:THE PHYSICS][act:the turn, explaining with relish]But two billion years ago uranium was ^richer: about three point seven percent fissile, close@adj to ^modern reactor fuel.",
                      "[d:build][go:0|0][sfx:shimmer][act:building, step by step]Groundwater seeped into the ^seams, slowed the ^neutrons, and the rock went ^critical. [act:flat, final, a small wonder][tune:highfall]By ^itself."]),
        B("reversal", 3, ["[d:reveal][k:THE TWIST][sfx:hit][act:delighted, lean in]And it ^pulsed. [act:laying out the rhythm][tune:level]Thirty minutes@time ^on, until the water ^boiled away. [act:the other half, slower][tune:fall]Two and a half hours ^off, until it ^seeped back.",
                          "[d:aside][act:admiring aside, lighter]A chemist, Paul Kuroda, ^predicted exactly this in {1956|nineteen fifty-six}, ^sixteen years before anyone found it."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Built by ^someone? [act:dry, simple][tune:fall]Not a ^trace. [act:turning to the answer][tune:rise]A ^natural reactor? [act:the verdict, confident][tune:fall]^*Established*.",
                     "[d:tension][p:0.93][act:warm, amused wonder]^Nature got there first. [act:the kicker, dry][tune:fall]By about ^two billion years."]),
    ]
    return EP("oklo", "00.04", "Oklo: The Two-Billion-Year-Old Nuclear Reactors", "oklo", "solid", "Who, or what, ran nuclear reactors in Gabon two billion years ago?", "The reactor had shut down two billion years *earlier*.", beats, shots,
              "Meshik 2005, Scientific American · Gauthier-Lafaye et al. 1996 · Meshik, Hohenberg & Pravdivtseva 2004, Physical Review Letters · Kuroda 1956",
              "In 1972 French engineers found uranium that had already been burned. The reactor that burned it was natural, and it shut down two billion years ago.",
              ["#Oklo", "#Nuclear", "#Science", "#Geology", "#WeighItYourself"])


# ---------------------------------------------------------------- 00.05 Out-of-place artefacts
def ooparts():
    ham = [{"k": "poly", "p": [[240, 1000], [300, 820], [430, 760], [620, 780], [760, 860], [780, 1000], [650, 1080], [380, 1080]], "fill": "#a08a6a", "c": "#e9dccb", "w": 2, "curve": True, "in": .2},
           {"k": "rect", "x": 470, "y": 640, "w": 36, "h": 260, "fill": "#6b4a2e", "c": "#c9a070", "sw": 1.4, "in": .5},
           {"k": "rect", "x": 400, "y": 880, "w": 180, "h": 70, "fill": "#5b5550", "c": "#c9ccd2", "sw": 1.4, "in": .6},
           {"k": "cap", "x": 500, "y": 560, "t": "the London hammer · Texas · found 1936 · schematic", "in": .2},
           {"k": "label", "x": 500, "y": 1160, "t": "a late-1800s American style, in a limey nodule", "c": AMBER, "in": 1.2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": ham}
    plug = [{"k": "circle", "x": 500, "y": 880, "r": 250, "fill": "#7a6a58", "c": "#e9dccb", "w": 2, "in": .2},
            {"k": "circle", "x": 500, "y": 880, "r": 170, "fill": "#20242a", "c": "#9fb0c0", "w": 1.4, "in": .5},
            {"k": "rect", "x": 480, "y": 740, "w": 40, "h": 90, "fill": "#e9e9e9", "c": "#9fb0c0", "sw": 1, "in": .8},
            {"k": "rect", "x": 465, "y": 830, "w": 70, "h": 60, "fill": "#b0b6bc", "c": "#9fb0c0", "sw": 1, "in": .9},
            {"k": "rect", "x": 485, "y": 890, "w": 30, "h": 90, "fill": "#c8743c", "c": "#9fb0c0", "sw": 1, "in": 1.0},
            {"k": "cap", "x": 500, "y": 560, "t": "the Coso artefact · California · found 1961", "in": .2},
            {"k": "label", "x": 500, "y": 1200, "t": "X-rays: a 1920s Champion spark plug", "c": AMBER, "in": 1.4}]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": plug}
    sp = [{"t": "slab", "x0": -8, "x1": 8, "z0": -6, "z1": 6, "y": 0, "c": "#b8a57c"}] + sphere(-3, 0, 1.8, "#6f4a3a") + sphere(2.6, 1.4, 1.4, "#7a5240") + \
         [{"t": "line", "p": [[-3 + 1.82 * math.cos(2 * math.pi * k / 30), 1.8, 1.82 * math.sin(2 * math.pi * k / 30)] for k in range(31)], "c": "#e2cf9e", "w": 2},
          L_(0, 3.8, "the Klerksdorp spheres · about 3-6 cm · schematic", GOLD, z=0, dy=-24), L_(0, 0, "natural nodules, in 3-billion-year-old rock", "#cfe6ff", z=6, dy=40)]
    s2 = iso(sp, cam=[1, 500, 900], s=48, x=500, y=1000, az=-20, spin=1.0, el=.4, table=None)
    ica = [{"k": "poly", "p": [[260, 900], [300, 720], [500, 660], [700, 720], [760, 900], [700, 1060], [500, 1110], [300, 1060]], "fill": "#5a5550", "c": "#c9ccd2", "w": 2, "curve": True, "in": .2},
           {"k": "line", "p": [[360, 950], [400, 880], [480, 860], [560, 870], [620, 830], [660, 780], [680, 800], [640, 860], [600, 900], [600, 960]], "c": "#e9dccb", "w": 3, "curve": True, "in": .6},
           {"k": "line", "p": [[440, 870], [440, 960]], "c": "#e9dccb", "w": 3, "in": .8}, {"k": "line", "p": [[540, 880], [540, 965]], "c": "#e9dccb", "w": 3, "in": .8},
           {"k": "cap", "x": 500, "y": 560, "t": "an Ica stone · Peru · schematic", "in": .2},
           {"k": "label", "x": 500, "y": 1200, "t": "a farmer said he carved them, copying comics and magazines", "c": AMBER, "in": 1.2}]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": ica}
    conc = [{"k": "circle", "x": 500, "y": 880, "r": 60 + k * 45, "fill": "none", "c": "#c9a370", "w": 2, "op": .9 - k * .12, "in": .3 + k * .3} for k in range(6)] + \
           [{"k": "rect", "x": 470, "y": 850, "w": 60, "h": 60, "fill": "#5b5550", "c": "#c9ccd2", "sw": 1, "in": .2},
            {"k": "cap", "x": 500, "y": 520, "t": "a concretion: minerals cement around a core", "in": .2},
            {"k": "label", "x": 500, "y": 1260, "t": "sometimes in years, sometimes in millions of years", "c": AMBER, "in": 2.0}]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": conc}
    s5 = stat("3.3", "million years", "the age of the oldest known stone tools; our own species is about 300,000 years old", "Harmand et al. 2015; Hublin et al. 2017")
    s6 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what would make an object truly out of place", "#8fd9b0", ["found in place, in a dated layer", "recorded as it is dug up", "tested by independent labs"], size=30)}
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:OUT-OF-PLACE ARTEFACTS][sfx:boom][act:showman, laying out the exhibits][tune:level]A hammer inside ^solid rock. [act:raising the stakes][tune:level]A spark plug in a stone called ^half a million years old. [act:the wildest one, slower][tune:fall]Grooved metal spheres ^three billion years old.",
                      "[d:tension][cam:1.12|0|0][act:mock-grave, relishing it]^Impossible objects@noun. [act:playful, rolling up sleeves]Let's put them on ^trial."], cut=False),
        B("world", 0, ["[d:calm][k:EXHIBIT A][act:courtroom clerk, reading the file]The London hammer, found in ^Texas in {1936|nineteen thirty-six}. [act:matter of fact, a hint of a smile]Its style is ^American, from the late ^eighteen hundreds.",
                       "[d:build][go:4|0][act:explaining, unhurried]The rock around it is a ^concretion: minerals that glue themselves around an object@noun, sometimes in just a ^few years."]),
        B("collision", 1, ["[d:build][k:EXHIBIT B][act:next exhibit, crisp]The ^Coso artefact, California, {1961|nineteen sixty-one}. [act:dry, one eyebrow up]Sold as ^half a million years old.",
                           "[d:build][sfx:hit][act:the punchline, deadpan]X-rays showed a ^nineteen-twenties Champion spark plug."]),
        B("cost", 2, ["[d:build][k:EXHIBIT C][act:next exhibit, crisp]The Klerksdorp spheres, South ^Africa. [act:conceding, genuinely impressed]The rock around them ^really is about three billion years old.",
                      "[d:build][act:the turn, gentle but firm]But the ^spheres are mineral nodules that ^grew in it. [act:plain, closing it off]^Natural, and much ^softer than steel."]),
        B("reversal", 3, ["[d:reveal][k:EXHIBIT D][act:wide-eyed, enjoying it]The Ica stones of Peru, with people riding ^dinosaurs. [sfx:shimmer][act:dry, the confession, amused]A farmer said ^he carved them, copying comics, and aged them with dung and ^shoe polish@verb.",
                          "[d:build][go:6|0][act:the real question, thoughtful][tune:fall]So what would make an object@noun ^truly out of place? [act:clear, the criteria]Being found in ^place, in a ^dated layer, as it's ^dug up. [gap:0.4][act:quiet, final][tune:fall]Not ^one of these was."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Objects@noun older than ^humankind? [act:the verdict, level, precise][tune:fall]^*Ruled out*, for every one that's been ^tested.",
                     "[d:tension][p:0.93][act:warm, a genuine open invitation]Find one in the ^rock, record@verb it as you ^dig, and we'll weigh it too."]),
    ]
    return EP("ooparts", "00.05", "Out-of-Place Artefacts: Impossible Objects on Trial", "ooparts", "debunked", "Are there manufactured objects older than humankind?", "Let's put them on *trial*.", beats, shots,
              "Heinrich 2008 · Stromberg & Heinrich 2004 · Polidoro 2002 · Harmand et al. 2015, Nature · Hublin et al. 2017, Nature · Cremo & Thompson 1993",
              "A hammer in stone, a spark plug in a nodule, grooved spheres in 3-billion-year-old rock and stones showing people with dinosaurs: what each impossible object turned out to be.",
              ["#OOPArts", "#Mystery", "#Archaeology", "#Science", "#WeighItYourself"])


# ---------------------------------------------------------------- 00.06 Ancient astronauts
def astronauts():
    s0 = papyrus(rows=10, cols=8, kind="hieratic", holes=True)
    s0["els"] += [{"k": "cap", "x": 500, "y": 300, "t": "Merer's logbook · Wadi al-Jarf · c. 2560 BCE", "in": .3},
                  {"k": "label", "x": 500, "y": 1260, "t": "boat trips carrying limestone to Giza, for Khufu's pyramid", "st": "small", "c": AMBER, "in": 1.0}]
    v = View(-105, 45, -30, 42, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Giza", 31.13, 29.98, {"c": GOLD, "a": "end", "lx": -18}), ("Nazca", -75.13, -14.74, {"c": GOLD}), ("Palenque", -92.05, 17.48, {"c": GOLD})], cam=[1, 500, 860])
    r = random.Random(3)
    stones = [{"k": "circle", "x": r.uniform(120, 880), "y": r.uniform(640, 1120), "r": r.uniform(8, 16), "fill": "#4a3a2e", "c": "none", "w": 0, "in": .1} for _ in range(260)]
    stones = [s for s in stones if not (440 < s["x"] < 560)]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 100, "y": 620, "w": 800, "h": 520, "fill": "#e2cf9e", "c": "none", "sw": 0, "in": .05}] + stones +
          [{"k": "cap", "x": 500, "y": 540, "t": "move the dark stones aside: pale ground shows", "in": .3},
           {"k": "label", "x": 500, "y": 1220, "t": "the Nazca lines · schematic", "st": "small", "c": AMBER, "in": 1.0}]}
    s3 = stat("303", "new figures", "Nazca geoglyphs found in six months with AI help, in 2024; many are small, beside old footpaths", "Sakai et al. 2024, PNAS")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what Pakal's lid says", AMBER, ["a named king: K'inich Janaab' Pakal", "died in 683 CE", "falling into the underworld", "beneath the World Tree"])}
    s5 = stat("1968", "", "Chariots of the Gods? first published, in German; tens of millions of copies sold since", "von Däniken 1968")
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 1, ["[d:intrigue][k:ANCIENT ASTRONAUTS][sfx:boom][act:grand, listing the legends][tune:level]The ^pyramids. [act:keep going][tune:level]The ^Nazca lines. [act:the wildest, a small smile][tune:fall]A Maya king at the controls of a ^rocket.",
                      "[d:tension][cam:1.12|0|0][act:the big question, straight][tune:rise]Did ^aliens help? [act:playful, confident]Let's ask the sites ^themselves."], cut=False),
        B("world", 5, ["[d:calm][k:THE IDEA][act:storyteller, even]In {1968|nineteen sixty-eight}, Erich von Däniken published ^Chariots of the Gods. [act:impressed, a touch wry]It sold ^tens of millions of copies, and launched a whole ^TV genre."]),
        B("collision", 0, ["[d:build][k:GIZA][act:a discovery story, leaning in]In {2013|twenty thirteen}, archaeologists found ^papyri by the Red Sea: the ^logbook of an official named Merer.",
                           "[d:build][sfx:shimmer][act:reading from his diary, fond]His crew shipped ^limestone to Giza for Khufu's pyramid, ^month after month. [d:aside][act:light, a quick aside]There's also a ^workers' town, with bakeries and ^breweries."]),
        B("cost", 2, ["[d:build][k:NAZCA][act:simple, demonstrating]The Nazca lines: move the ^dark desert@noun stones aside, and the ^pale ground shows. [act:plain, reassuring]^Small teams can do it.",
                      "[d:build][go:3|0][act:news, brisk]In {2024|twenty twenty-four}, AI helped find three hundred and three ^new figures, many beside old ^footpaths. [d:aside][act:dry, a small smile]^Walkers, not landings."]),
        B("reversal", 4, ["[d:reveal][k:PALENQUE][act:the reveal, measured]The famous 'astronaut' lid ^names its man: King ^Pakal, who died in {683|six eighty-three}.",
                          "[d:build][sfx:hit][act:respectful, explaining the image]He's ^falling into the underworld, beneath the World ^Tree. [act:calm, matter of fact, with respect]Standard Maya ^religious art."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Monuments that needed ^aliens? [act:the verdict, level-headed][tune:fall]^*Ruled out*. [act:fair, the honest open part][tune:rise]How ^exactly some stones were lifted? [act:honest, even]Still ^argued, between ^human methods.",
                     "[d:tension][p:0.93][act:warm, generous]Credit where credit is ^due. [gap:0.4][act:quiet pride, certain][tune:fall]^People did this."]),
    ]
    return EP("ancient-astronauts", "00.06", "Ancient Astronauts: Credit Where Credit Is Due", "ancient-astronauts", "debunked", "Did ancient monuments need help from visitors from space?", "Let's ask the sites *themselves*.", beats, shots,
              "Tallet 2017 · Tallet & Lehner 2021 · Lehner 1997 · Aveni 1990 · Sakai et al. 2024, PNAS · Schele & Freidel 1990 · von Däniken 1968",
              "Did aliens help build the pyramids, draw the Nazca lines and fly Pakal's rocket? A 4,500-year-old logbook, a desert technique and a named king answer.",
              ["#AncientAliens", "#Pyramids", "#Nazca", "#Maya", "#WeighItYourself"])


# ---------------------------------------------------------------- 00.02 How we date the past
def dating():
    cols = ["#c9b894", "#b8a57c", "#a08a66", "#8c7452", "#6f5a44"]
    lay = [box(0, 0, 12 - (i + 1) * 2.4, 40, 24, 2.4, cols[i], "rgba(0,0,0,.3)") for i in range(5)] + \
          [box(-10, 12.2, 10.4, 2, 1.2, 1, "#f4ead6"), box(8, 12.2, 5.6, 1.6, 1.2, 1, "#f4ead6"), box(-4, 12.2, 1, 2.2, 1.2, 1.2, "#f4ead6"),
           L_(-10, 11.4, "younger", "#8fd9b0", z=13, dy=-10), L_(-4, 2.2, "older", "#ffb09a", z=13, dy=30),
           L_(0, 12, "the law of layers: what's deeper is older · schematic", GOLD, z=-12, dy=-40)]
    s0 = iso(lay, cam=[1, 500, 900], s=12, x=500, y=1000, az=-24, spin=1.0, el=.45, table=None)
    X = lambda t: 150 + 700 * t / 50000
    Y = lambda f: 1100 - 460 * f
    curve = [[round(X(t), 1), round(Y(0.5 ** (t / 5730)), 1)] for t in range(0, 50001, 1000)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "line", "p": [[150, 1100], [850, 1100]], "c": "#8c7152", "w": 2, "in": .1}, {"k": "line", "p": [[150, 1100], [150, 620]], "c": "#8c7152", "w": 2, "in": .1},
                                                    {"k": "line", "p": curve, "c": GOLD, "w": 4, "curve": True, "in": .4, "fx": "draw", "dur": 1.6},
                                                    {"k": "line", "p": [[X(5730), 1100], [X(5730), Y(.5)], [150, Y(.5)]], "c": "#9fd0ff", "w": 1.6, "style": "inferred", "in": 1.4},
                                                    {"k": "label", "x": X(5730) + 10, "y": Y(.5) - 16, "t": "half left after 5,730 years", "st": "small", "c": "#9fd0ff", "a": "start", "in": 1.6},
                                                    {"k": "label", "x": 500, "y": 1150, "t": "years since death · 0 to 50,000", "st": "small", "in": .3},
                                                    {"k": "cap", "x": 500, "y": 540, "t": "the carbon-14 clock", "in": .2},
                                                    {"k": "label", "x": 500, "y": 1240, "t": "after about 50,000 years, too little is left to measure", "c": AMBER, "in": 2.0}]}
    rings = [{"k": "circle", "x": 500, "y": 860, "r": 20 + i * 7, "fill": "none", "c": "#6b4a2e" if i != 30 else GOLD, "w": 2 if i != 30 else 5, "in": .1 + i * .012} for i in range(60)]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "circle", "x": 500, "y": 860, "r": 450, "fill": "#c9a370", "c": "#6b4a2e", "w": 6, "in": .05}] + rings +
          [{"k": "label", "x": 500, "y": 360, "t": "tree rings count years exactly, one ring per year", "c": GOLD, "in": 1.2},
           {"k": "label", "x": 500, "y": 1370, "t": "solar-storm spikes, like 993 CE, pin a ring to its year", "c": AMBER, "in": 1.8}]}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the clocks, and how far back they reach", AMBER, ["tree rings · about 14,000 years", "radiocarbon · about 50,000 years", "luminescence · when sand last saw light", "uranium in cave crusts · about 500,000 years", "argon in volcanic rock · millions of years"], y=460, size=28)}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("a date dates the sample, not the site", "#ffb09a", ["an old beam, reused in a new wall", "soil washed in between stones", "a pot that arrived long after the digging"], y=520) +
          [{"k": "label", "x": 500, "y": 880, "t": "always ask: what exactly was dated?", "c": "#9fd0ff", "in": 1.6}]}
    s5 = stat("95%", "confidence", "how a careful date is quoted: as a range, like 1260–1390 CE, not as a single year", "standard practice")
    s6 = like(s0, cam=[1.12, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:HOW WE DATE THE PAST][sfx:boom][act:quoting a headline, crisp][tune:level]^'Twelve thousand years old.' [act:another one, same tone][tune:level]^'Four and a half thousand years old.' [act:pulling back, intrigued]Every mystery hangs on a ^number@count.",
                      "[d:tension][cam:1.12|0|0][act:genuinely curious, leaning in]So ^where do those numbers come from?"], cut=False),
        B("world", 0, ["[d:calm][k:THE LAYERS][act:plain, like a first lesson]Rule one: layers pile ^up. [act:simple logic, then a caveat]What's deeper is ^older, unless something ^dug through it.",
                       "[d:aside][act:light, affectionate, a small smile]Archaeology is mostly the careful reading of ^dirt."]),
        B("collision", 1, ["[d:build][k:THE CARBON CLOCK][act:explaining, clear and even]Living things take in ^carbon, including a rare ^radioactive kind. [act:precise, give the number weight]After death it ^decays: half of it gone every ^fifty-seven hundred and thirty years.",
                           "[d:build][sfx:shimmer][act:the neat payoff, pleased]Measure what's ^left, and you have a ^clock. [act:a quick practical footnote]Good to about ^fifty thousand years."]),
        B("cost", 3, ["[d:build][k:MORE CLOCKS][go:2|0][act:brisk, counting them off][tune:level]Tree rings count years ^exactly. [go:3|0][act:keep the pace][tune:level]Luminescence tells when buried grains last saw ^daylight. [act:reaching further back][tune:level]Uranium in cave crusts reaches back ^half a million years. [act:short, the last and biggest][tune:fall]Volcanic rock, ^millions."]),
        B("reversal", 4, ["[d:reveal][k:THE TRAP][sfx:hit][act:the warning, slower, deliberate]But a date dates the ^sample, not the ^site. [act:an example, concrete][tune:level]An ^old beam reused in a ^new wall. [act:a second example, lighter][tune:fall]Soil ^washed in between stones.",
                          "[d:build][act:pointed, a knowing look]That's exactly how the Gunung Padang pyramid paper ^fell."]),
        B("tag", 5, ["[d:verdict][k:THE RULE][p:0.95][act:warm, handing over the tool]So when you hear a date, ask ^two things. [act:first question, crisp]What ^exactly was dated? [act:second question, thoughtful][tune:fall]And how is it ^tied to what we care about?",
                     "[d:tension][p:0.93][act:light, almost conspiratorial]That's the ^whole trick. [act:warm, a quiet invitation]Now you can weigh it ^yourself."]),
    ]
    return EP("dating-methods", "00.02", "How We Date the Past", None, None, None, "Every mystery hangs on a *number*.", beats, shots,
              "Libby 1952 · Reimer et al. 2020, IntCal20 · Miyake et al. 2012 · Aitken 1998 · standard dating literature",
              "Layers, carbon-14, tree rings, luminescence and uranium: how archaeologists put numbers on the past, and the one question to ask of any date.",
              ["#Archaeology", "#Science", "#Radiocarbon", "#History", "#WeighItYourself"])


# ---------------------------------------------------------------- 00.03 Seven grades of evidence
GRADES = [("Established", "#8fd9b0"), ("Strong evidence", "#7fd1d4"), ("Plausible", "#e8c86a"), ("Open question", "#f0b06a"), ("Mixed record", "#d8c7a8"), ("Awaiting evidence", "#c9c1ee"), ("Ruled out", "#e98a8a")]


def grades():
    bars = []
    for i, (g, c) in enumerate(GRADES):
        bars += [{"k": "rect", "x": 200, "y": 560 + i * 92, "w": 600, "h": 64, "fill": c, "c": "none", "sw": 0, "op": .9, "in": .3 + i * .2},
                 {"k": "label", "x": 500, "y": 603 + i * 92, "t": g, "st": "serif", "size": 34, "c": "#1a1511", "halo": False, "in": .4 + i * .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": bars + [{"k": "cap", "x": 500, "y": 500, "t": "seven grades, from most to least supported", "in": .2}]}
    ex = ["Vikings in America, 1021", "Troy was a real city", "stories remember the rising seas", "the Voynich hides a language", "the Sea Peoples ended an age", "a lost Ice Age civilisation", "Atlantis in the Atlantic"]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 500, "t": "one example of each, from our files", "in": .2}] +
          [e for i, ((g, c), t) in enumerate(zip(GRADES, ex)) for e in ({"k": "rect", "x": 150, "y": 560 + i * 92, "w": 18, "h": 64, "fill": c, "c": "none", "sw": 0, "in": .3 + i * .2},
                                                                     {"k": "label", "x": 190, "y": 603 + i * 92, "t": t, "st": "serif", "size": 30, "a": "start", "in": .35 + i * .2})]}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what we weigh", "#8fd9b0", ["stones · dates · bones · texts"], y=560) + grp("what we never rate", "#9fd0ff", ["faith"], y=820)}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what moves a grade", AMBER, ["a new, dated find", "a result repeated by others", "a paper retracted", "a dig in the decisive spot"])}
    s4 = quote("Coherence is the measure, not final demonstration.", "Residual Continuum", y=760, size=48)
    s5 = like(s0, cam=[1.08, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:SEVEN GRADES][sfx:boom][act:inviting, setting out the rules]Every case we weigh ends with a ^verdict. [act:promising, a little mischief]Here's what each one ^means... [act:the hook, quieter, sincere][tune:fall]and why ^none of them is final."], cut=False),
        B("world", 1, ["[d:calm][k:THE TOP][act:clear, defining terms]Established: several ^independent lines agree, and ^nothing serious contradicts them. [act:a notch down, still confident]Strong evidence: ^nearly there, with ^one gap left. [act:even, a gentle reservation][tune:fallrise]Plausible: it ^fits, but it hasn't been ^shown."]),
        B("collision", 1, ["[d:build][k:THE MIDDLE][act:balanced, weighing both hands]Open question: good evidence on ^both sides. [act:even, splitting it down the middle]Mixed record@noun: ^some parts of the claim hold, and ^others don't."]),
        B("cost", 1, ["[d:build][k:THE BOTTOM][act:patient, fair-minded]Awaiting evidence: ^possible, but what would show it ^hasn't turned up. [sfx:hit][act:firm, no drama]Ruled out: the evidence points firmly the ^other way."]),
        B("reversal", 2, ["[d:reveal][k:WHAT WE NEVER RATE][act:sincere, measured, with care]And one thing we ^never grade: ^faith. [act:plain, listing our tools][tune:fall]We weigh ^stones, ^dates, ^bones and ^texts. [act:respectful, warm, settled]What people believe is ^theirs.",
                          "[d:build][go:3|0][act:simple principle, even]Grades move when the ^evidence moves. [act:counting them off][tune:level]A new ^dig. [act:second, brisk][tune:level]A ^repeated result. [act:the last one, a touch heavier][tune:fall]A ^retraction."]),
        B("tag", 4, ["[d:verdict][k:THE MOTTO][p:0.95][act:calm, the motto, unhurried]^Coherence is the measure. [gap:0.4][act:quiet, certain][tune:fall]Not ^final demonstration.",
                     "[d:tension][p:0.93][act:warm invitation, straight to camera]Weigh the evidence ^yourself."]),
    ]
    return EP("evidence-grades", "00.03", "Seven Grades of Evidence", None, None, None, "Why none of them is *final*.", beats, shots,
              "Residual Continuum method notes",
              "Established, strong, plausible, open, mixed, awaiting evidence, ruled out: what each of our seven verdicts means, what moves them, and the one thing we never rate.",
              ["#WeighItYourself", "#History", "#Science", "#CriticalThinking", "#Method"])


def _mur():
    from mural import remix
    import illus
    return remix, illus


VC = [("Established", "#8fd9b0"), ("Strong evidence", "#7fd1d4"), ("Plausible", "#f2c98e"), ("Open question", "#c9c1ee"), ("Mixed record", "#e8b87a"),
      ("Awaiting evidence", "#9fd0ff"), ("Ruled out", "#ff8a7a")]


def grades_m():
    """The seven grades as one continuous take (see mural.py): each grade is a little picture of what the evidence looks like."""
    remix, I = _mur()
    ep = grades()
    Y = lambda k: 520 + 118 * k
    def icon(k, at):
        y = Y(k); c = VC[k][1]; x = 250
        if k == 0:
            return [I.line([[x - 90, y - 40], [x, y]], at, c, 4), I.line([[x - 90, y], [x, y]], at + .2, c, 4), I.line([[x - 90, y + 40], [x, y]], at + .4, c, 4), I.dot(x, y, 10, c, at + .6)]
        if k == 1:
            return [I.line([[x - 90, y - 40], [x - 8, y - 4]], at, c, 4), I.line([[x - 90, y + 40], [x, y]], at + .2, c, 4), I.dot(x, y, 10, c, at + .4)]
        if k == 2:
            return [I.box(x - 90, y - 34, 68, 68, "none", "#8a7a66", 3, 4, at), I.box(x - 12, y - 30, 60, 60, "none", c, 3, 4, at + .3, style="inferred")]
        if k == 3:
            return [I.line([[x - 90, y], [x + 40, y]], at, c, 4), I.line([[x - 25, y], [x - 25, y + 40]], at, c, 4), I.dot(x - 80, y - 14, 14, c, at + .3), I.dot(x + 30, y - 14, 14, c, at + .3)]
        if k == 4:
            return [I.box(x - 90, y - 30, 60, 60, "#8fd9b0", r=4, at=at), I.box(x - 26, y - 30, 60, 60, "#ff8a7a", r=4, at=at + .3)]
        if k == 5:
            return [I.box(x - 80, y - 32, 100, 64, "none", c, 3, 6, at, style="claimed"), I.label(x - 30, y + 18, "?", at + .3, c, 44, st="big")]
        return [I.arrow([[x - 90, y], [x + 30, y]], at, c, 4, dur=.5, curve=False), I.strike(x - 90, y + 30, x + 30, y - 30, at + .5, c, 5)]
    rows = lambda ks, t0, step: sum([[I.dot(120, Y(k), 12, VC[k][1], t0 + step * j), I.label(360, Y(k) + 12, VC[k][0], t0 + step * j, VC[k][1], 34, "start")] + icon(k, t0 + step * j + .2)
                                     for j, k in enumerate(ks)], [])
    top = {"base": "dark", "cam": [1.22, 450, 900], "els": rows((0, 1, 2), .3, 4.2)}
    weigh = {"base": "dark", "floor": 1180, "cam": [1, 500, 900], "els": [I.line([[500, 1180], [500, 760]], .2, "#cbbca8", 5), I.line([[240, 800], [760, 800]], .3, "#cbbca8", 5),
             I.line([[260, 800], [220, 900], [360, 900], [300, 800]], .4, "#cbbca8", 2), I.line([[700, 800], [640, 900], [780, 900], [740, 800]], .4, "#cbbca8", 2),
             I.box(235, 870, 50, 30, "#8a7a66", r=3, at=5.0), I.dot(320, 880, 14, "#cbbca8", 5.3), I.box(660, 870, 40, 30, "#e8dcc2", r=8, at=5.6), I.line([[720, 885], [770, 885]], 5.9, "#efe6d2", 10, draw=False),
             I.glow(500, 1330, 180, 1.4, .8), I.dot(500, 1330, 30, "#e8c878", 1.4), I.box(360, 1250, 280, 160, "none", "#e8c878", 3, 18, 1.8)]}
    SEG = 110
    gauge = [I.box(115 + SEG * k, 1100, SEG - 6, 40, VC[6 - k][1], r=6, at=.2 + .05 * k) for k in range(7)]
    mark = lambda k, at: [I.label(115 + SEG * k + SEG / 2 - 3, 1080, "▼", at, I.BONE, 40, st="big")]
    move = {"base": "dark", "cam": [1, 500, 900], "els": gauge + mark(2, .5) + [I.line([[300, 900], [300, 980]], 2.0, "#8a5d33", 6), {"k": "poly", "p": [[280, 980], [320, 980], [300, 1020]], "fill": "#cbbca8", "c": "none", "w": 0, "in": 2.0}] +
            mark(4, 2.4) + [I.box(470, 880, 60, 90, "none", I.GREEN, 3, 4, 3.4), I.box(545, 880, 60, 90, "none", I.GREEN, 3, 4, 3.6)] + mark(5, 3.8) +
            [I.box(700, 870, 90, 120, "#e8dcc2", "#8a7a66", 2, 4, 4.8), I.strike(690, 1000, 800, 860, 5.2)] + mark(2, 5.6)}
    motto = {"base": "dark", "floor": 1100, "cam": [1, 500, 880], "els": [I.line([[500, 1100], [500, 700]], .2, "#cbbca8", 5), I.line([[260, 740], [740, 740]], .4, "#cbbca8", 5, dur=1.2),
             I.dot(260, 760, 22, "#8fd9b0", .8), I.dot(740, 760, 22, "#9fd0ff", .8), I.label(500, 1250, "Coherence is the measure,", 1.2, I.BONE, 40, st="serif"),
             I.label(500, 1310, "not final demonstration.", 2.4, I.BONE, 40, st="serif")]}
    return remix(ep, scenes={1: top, 2: weigh, 3: move, 4: motto}, alias={5: 0}, drop=("para", "num", "title", "q", "cap"),
                 beat_adds={2: (rows((3, 4), .3, 3.2), None), 3: (rows((5, 6), .3, 3.6), None)})


def dating_m():
    """How we date the past as one continuous take (see mural.py): the clocks drawn to scale, and the traps drawn in a wall."""
    remix, I = _mur()
    ep = dating()
    older = [I.arrow([[900, 560], [900, 1260]], 1.0, I.AMBER, 4, dur=1.2, curve=False), I.label(880, 1310, "older", 1.6, I.AMBER, 30, "end"),
             I.box(420, 560, 140, 520, "none", I.LILAC, 3, 8, 4.4, style="claimed")]
    L = lambda yrs: 150 + 700 * (math.log10(yrs) - 3) / (math.log10(5e6) - 3)
    clocks = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[150, 1240], [850, 1240]], .1, "#8c7152", 3)] +
              [I.label(L(v), 1290, t, .2, "#9a938a", 24) for v, t in ((1e3, "1,000"), (1e4, "10,000"), (1e5, "100,000"), (1e6, "1 million"))] +
              sum([[I.line([[150, y], [L(v), y]], at, c, 26, dur=.9), I.label(L(v) + 14, y + 10, t, at + .6, c, 28, "start")]
                   for v, y, c, t, at in ((14000, 620, "#a8865e", "tree rings", .4), (50000, 740, "#9fd0ff", "radiocarbon", 1.4), (200000, 860, "#f2c98e", "luminescence", 2.6),
                                          (500000, 980, "#c9c1ee", "uranium", 4.4), (4e6, 1100, "#ff8a7a", "argon", 6.2))], [])}
    stones = [I.box(200 + 150 * (k % 4) + (70 if (k // 4) % 2 else 0), 700 + 110 * (k // 4), 140, 100, "#8a7a66", "#5a4a3a", 2, 6, .2 + .05 * k) for k in range(15)]
    trap = {"base": "dark", "cam": [1, 500, 900], "els": stones + [I.box(270, 915, 460, 40, "#5a3a22", "#8a5d33", 2, 3, 1.4), I.label(500, 890, "old beam", 1.8, I.AMBER, 28)] +
            [I.dot(470 + 30 * k, 700 + 60 * k, 6, "#c8a878", 3.6 + .15 * k) for k in range(8)] + [I.arrow([[440, 700], [470, 1100]], 3.6, "#c8a878", 3, "inferred", 1.0, False),
             I.box(700, 1180, 170, 210, "#e8dcc2", "#8a7a66", 2, 4, 6.0), I.strike(690, 1400, 880, 1170, 6.6)]}
    ask = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(240, 700, 90, 160, "rgba(159,208,255,.25)", I.BLUE, 3, 12, 1.2)] + I.question(285, 660, 2.0, 70, I.BLUE) +
           [I.line([[340, 790], [600, 790]], 3.6, I.AMBER, 4, "inferred", 1.0), {"k": "poly", "p": [[620, 900], [760, 640], [900, 900]], "fill": "#c9a86a", "c": "none", "w": 0, "in": 3.8}] +
           I.question(470, 750, 4.6, 70, I.AMBER)}
    return remix(ep, scenes={3: clocks, 4: trap, 5: ask}, alias={6: 0}, cams={0: [1.15, 500, 950], 6: [1.2, 500, 980]},
                 drop=("para", "num", "title", "q", "cap"), beat_adds={1: (older, None)})


def astronauts_m():
    """Ancient astronauts as one continuous take (see mural.py): the book, the boats of Merer, the walkers of Nazca, and a king falling to the underworld."""
    remix, I = _mur()
    ep = astronauts()
    book = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(380, 620, 240, 320, "#6b3a2a", "#c8743c", 3, 6, .3), I.label(500, 1000, "1968", .6, I.BONE, 34, st="serif")] +
            [I.box(160 + 32 * (k % 22), 1180 - 22 * (k // 22), 26, 18, "#6b3a2a", r=2, at=2.4 + .02 * k) for k in range(88)] +
            [I.box(620, 560, 260, 180, "#15100c", "#cbd2d8", 4, 10, 5.4), I.oval(750, 650, 60, 20, "none", I.LILAC, 3, 1, 5.8)]}
    boats = [{"k": "boat", "x": 200 + 250 * k, "y": 1280, "w": 180, "in": .3 + .4 * k} for k in range(3)] + [I.box(160 + 250 * k, 1230, 70, 40, "#cbbca8", r=3, at=.5 + .4 * k) for k in range(3)] + \
            [{"k": "house", "x": 300 + 120 * k, "y": 1420, "w": 90, "h": 50, "in": 4.0 + .2 * k} for k in range(4)] + [I.glow(420, 1400, 120, 4.6, .5, "fire")]
    paths = [I.line([[100, 700 + 200 * j], [300, 760 + 190 * j], [600, 690 + 210 * j], [900, 740 + 200 * j]], .3 + .2 * j, "#c8a878", 3, "inferred", 1.2, True) for j in range(3)]
    figs = []
    for k in range(24):
        j = k % 3; t = (k // 3) / 8
        x = 120 + 760 * t; y = 700 + 200 * j + 30 * math.sin(t * 6) - 50
        figs += [I.ring(x, y, 14, 1.4 + .12 * k, "#f2dcb4", 3, dur=.3)]
    walkers = [I.person(200 + 250 * j, 790 + 200 * j, 70, 5.0 + .3 * j) for j in range(3)]
    nazca = {"base": "plan", "bg": "#8a6a48", "north": False, "cam": [1, 500, 900], "els": paths + figs + walkers}
    lid = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(200, 520, 600, 860, "#6f6456", "#9a8e7c", 3, 8, .1),
           I.line([[500, 1180], [500, 640]], .5, "#3a332b", 12), I.line([[330, 760], [670, 760]], .7, "#3a332b", 10), I.dot(500, 610, 22, "#3a332b", .9),
           I.label(500, 480, "Pakal · 683", .4, I.BONE, 34),
           {"k": "poly", "p": [[380, 1000], [520, 930], [600, 960], [470, 1050]], "fill": "#e8dcc2", "c": "none", "w": 0, "in": 3.0},
           I.dot(360, 990, 24, "#e8dcc2", 3.0),
           {"k": "poly", "p": [[300, 1300], [500, 1180], [700, 1300], [640, 1340], [500, 1260], [360, 1340]], "fill": "#3a332b", "c": "none", "w": 0, "in": 4.2}]}
    return remix(ep, scenes={3: nazca, 4: lid, 5: book}, alias={6: 0}, cams={6: [1.1, 500, 860]}, drop=("para", "num", "title", "q", "cap"),
                 line_adds={(2, 1): (boats, None)})


def _dots(x0, y0, cols, rows, dx, c="#6f675d", w=8, at=.2, step=.02, op=.9):
    """A field of atoms as rows of round dots (one dashed line per row: light to draw, cols x rows dots)."""
    return [{"k": "line", "p": [[x0, round(y0 + dx * r, 1)], [round(x0 + dx * (cols - 1), 1), round(y0 + dx * r, 1)]], "c": c, "w": w, "dash": "0.1 %.2f" % (dx - .1),
             "op": op, "keepop": True, "in": round(at + step * r, 2)} for r in range(rows)]


def oklo_m():
    """Oklo as one continuous take (see mural.py): a thousand atoms of which seven can split, a chain reaction, an hourglass of uranium,
    water as a brake on neutrons, and a reactor that switches itself on and off."""
    remix, I = _mur()
    import copy
    from iso3d import project
    ep = oklo()
    sec = lambda r: (lambda t: round(t / r, 2))             # times below are seconds into the rewritten narration; remix stretches each step by r
    AU, U0 = "#e8c35a", "#6f675d"
    atom = lambda x, y, at, r=7.5: {"k": "circle", "x": x, "y": y, "r": r, "fill": AU, "c": "#fff1c8", "w": 1.5, "in": at, "fx": "pop"}
    # 1 · the hook, on the map: Oklo ringed, a reactor glow, two billion years, and the question
    t = sec(1.68)
    v = View(7, 16.5, -5.2, 3, (40, 330, 920, 900))
    ox, oy = v.p(13.16, -1.394)
    hook = [I.ring(ox, oy, 44, t(4.6), I.AMBER, 3), I.glow(ox, oy, 150, t(10.2), .85, "red"), I.label(ox, oy - 92, "2 billion years ago", t(14.6), I.AMBER, 32)] + \
        I.question(ox + 170, oy - 190, t(15.8), 80)
    # 2 · the clue: a thousand uranium atoms, seven of the kind that can split; at Oklo, some have gone out
    t = sec(1.97)
    X = lambda c: 130 + 19 * c
    Y = lambda r: 600 + 19 * r
    lit = [(3, 7), (5, 31), (10, 18), (13, 4), (16, 26), (20, 12), (22, 35)]
    gone = [(10, 18), (16, 26), (3, 7)]
    clue = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(110, 580, 781, 496, "rgba(255,236,206,.04)", "#8a7a66", 2, 14, t(.3))] + _dots(X(0), Y(0), 40, 25, 19, U0, 8, t(.4), t(.06)) +
            [I.label(500, 545, "1,000 uranium atoms", t(8.0), I.BONE, 32)] + [atom(X(c), Y(r), t(11.6 + .25 * k)) for k, (r, c) in enumerate(lit)] +
            [I.label(500, 1160, "0.72%", t(14.6), AU, 56, st="serif")] +
            sum([[I.dot(X(c), Y(r), 9.5, "#4a433c", t(at)), I.ring(X(c), Y(r), 17, t(at + .1), I.RED, 3, dur=.5)] for (r, c), at in zip(gone, (16.8, 18.4, 18.7))], []) +
            [I.label(500, 1240, "Oklo: less", t(17.0), I.RED, 34)] +
            sum([[I.dot(X(c) - 15, Y(r) - 9, 4, I.RED, t(19.8 + .2 * k)), I.dot(X(c) + 15, Y(r) + 9, 4, I.RED, t(19.8 + .2 * k))] for k, (r, c) in enumerate(gone)], [])}
    # 5 · the claim and the chain reaction: a plant built by someone?; one neutron splits an atom, two more split two, four...
    t = sec(2.08)
    A = (500, 730); G1 = [(300, 870), (700, 870)]; G2 = [(180, 1010), (420, 1010), (580, 1010), (820, 1010)]
    tower = [[300, 560], [322, 480], [340, 420], [345, 380], [340, 350], [460, 350], [455, 380], [460, 420], [478, 480], [500, 560]]
    dome = [[540, 560], [540, 480]] + I.ellipse(615, 480, 75, 66, 16, 180, 360) + [[690, 560]]
    def hit(a, b, at, c=I.BLUE, short=0):
        d = math.hypot(b[0] - a[0], b[1] - a[1]); k0, k1 = 34 / d, (34 + short) / d
        return I.arrow([[a[0] + (b[0] - a[0]) * k0, a[1] + (b[1] - a[1]) * k0], [b[0] - (b[0] - a[0]) * k1, b[1] - (b[1] - a[1]) * k1]], at, c, 3, dur=.5, curve=False)
    def split(p, at):
        return [I.glow(p[0], p[1], 90, at, .9, "red")] + [I.line([[p[0] + 34 * math.cos(a), p[1] + 34 * math.sin(a)], [p[0] + 50 * math.cos(a), p[1] + 50 * math.sin(a)]], at, AU, 3, dur=.3)
                                                          for a in (0.3, 1.35, 2.4, 3.45, 4.5, 5.55)]
    chain = {"base": "dark", "cam": [1, 500, 900], "els": [{"k": "poly", "p": tower, "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "curve": True, "in": t(3.2)},
             {"k": "poly", "p": dome, "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": t(3.5)},
             I.oval(398, 318, 44, 16, "none", I.LILAC, 2, 1, t(3.8), style="claimed")] + I.question(800, 470, t(4.6), 80) +
            [I.dot(170, A[1], 8, I.BLUE, t(7.0)), I.label(160, A[1] - 34, "neutron", t(7.0), I.BLUE, 28, "start"), hit((150, A[1]), A, t(7.4)), atom(A[0], A[1], t(6.8), 28)] +
            split(A, t(9.4)) + [hit(A, G1[0], t(10.4)), hit(A, G1[1], t(10.6)), I.arrow([[A[0] + 10, A[1] + 34], [A[0] + 30, A[1] + 110]], t(10.8), I.BLUE, 3, "inferred", .5, False)] +
            [atom(x, y, t(10.7), 24) for x, y in G1] + sum([split(p, t(13.4)) for p in G1], []) +
            [hit(G1[0], G2[0], t(14.0)), hit(G1[0], G2[1], t(14.1)), hit(G1[1], G2[2], t(14.2)), hit(G1[1], G2[3], t(14.3))] + [atom(x, y, t(14.3), 20) for x, y in G2] +
            sum([split(p, t(15.2)) for p in G2], []) + [I.arrow([[x + dx * 26, y + 30], [x + dx * 60, y + 90]], t(15.6), I.BLUE, 3, dur=.4, curve=False) for x, y in G2 for dx in (-1, 1)] +
            [I.glow(500, 870, 420, t(20.2), .35, "lamp")]}
    t = sec(1.83)
    basin = [I.oval(500, 1250, 290, 72, "rgba(232,184,122,.08)", "#c9a370", 2, 1, t(2.4), style="inferred")] + \
        [I.dot(x, y, 7, AU, t(3.4 + .06 * k)) for k, (x, y) in enumerate(I.scatter(16, 290, 710, 1215, 1285, 16))] + [I.label(500, 1385, "16 reactor zones", t(4.0), I.BONE, 30), I.glow(500, 1250, 260, t(6.4), .45, "lamp")]
    # 4 · uranium changes with time: thirty-seven fissile atoms in a thousand two billion years ago, seven today
    t = sec(2.5)
    BX = lambda x0, c: x0 + 12.6 * c
    BY = lambda r: 640 + 12.6 * r
    import random as _r
    rr = _r.Random(12)
    cells = rr.sample([(r, c) for r in range(40) for c in range(25)], 37)
    hour = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(100, 622, 338, 527, "rgba(255,236,206,.04)", "#8a7a66", 2, 12, t(.6)), I.box(562, 622, 338, 527, "rgba(255,236,206,.04)", "#8a7a66", 2, 12, t(.6))] +
            _dots(118, 640, 25, 40, 12.6, U0, 6, t(.8), t(.03)) + _dots(580, 640, 25, 40, 12.6, U0, 6, t(.8), t(.03)) +
            [I.line([[470, 830], [530, 830], [470, 950], [530, 950], [470, 830]], t(6.8), I.BONE, 3, dur=1.0), {"k": "poly", "p": [[500, 892], [522, 945], [478, 945]], "fill": AU, "c": "none", "w": 0, "in": t(7.6), "fx": "fill", "dur": 2.0},
             {"k": "poly", "p": [[478, 836], [522, 836], [500, 868]], "fill": AU, "c": "none", "w": 0, "in": t(7.0)}, I.arrow([[466, 990], [534, 990]], t(9.4), I.BONE, 3, dur=.5, curve=False)] +
            [I.label(269, 600, "2 billion years ago", t(10.2), I.BONE, 30), I.label(731, 600, "today", t(11.8), I.BONE, 30)] +
            [atom(BX(580, c), BY(r), t(12.0 + .08 * k), 5.5) for k, (r, c) in enumerate(cells[:7])] + [I.label(731, 1205, "0.72%", t(12.8), AU, 44, st="serif")] +
            [atom(BX(118, c), BY(r), t(14.8 + .04 * k), 5.5) for k, (r, c) in enumerate(cells)] + [I.label(269, 1205, "about 3.7%", t(16.0), AU, 44, st="serif")] +
            [I.box(150, 1250, 240, 34, "#8a939c", "#cbd2d8", 2, 17, t(18.4), fx="pop")] + [I.line([[150 + 40 * k, 1252], [150 + 40 * k, 1282]], t(18.6), "#5b6168", 2, draw=False) for k in range(1, 6)] +
            [I.label(269, 1330, "reactor fuel", t(18.8), I.BONE, 28)]}
    # 0 · the seam (still, so the drawings stay on it): groundwater runs in, a neutron slowed by water, the rock goes critical
    s0 = copy.deepcopy(ep["shots"][0])
    iso_e = next(e for e in s0["els"] if e.get("k") == "iso")
    iso_e["spin"] = 0
    iso_e["items"] = [it for it in iso_e["items"] if it.get("t") not in ("glow", "label")]
    P = lambda p: tuple(round(v, 1) for v in project(s0, p))
    path = [(-20, 12, -8), (-10, 8, -4), (0, 5.2, 0)]
    def along(f):
        seg = min(int(f * 2), 1); u = f * 2 - seg; a, b = path[seg], path[seg + 1]
        return P(tuple(a[i] + (b[i] - a[i]) * u for i in range(3)))
    t = sec(2.5)
    seam = [P((-20 + 40 * f, 5.1, 12)) for f in (.25, .5, .75)]
    bub = (720, 500)
    mol = [(650, 450), (700, 560), (760, 430), (640, 545), (745, 610), (822, 585)]
    s0["els"] += [I.dot(*along(f), 7, I.BLUE, t(.4 + 1.4 * f)) for f in (0, .2, .4, .6, .8, 1)] + [I.label(230, 655, "groundwater", t(.8), I.BLUE, 30)] + \
        [I.label(seam[0][0], 1190, "uranium seam", t(2.4), AU, 30), I.line([[seam[0][0], 1158], [seam[0][0], seam[0][1] + 12]], t(2.4), AU, 2, dur=.5)] + \
        [I.oval(bub[0], bub[1], 150, 150, "rgba(18,13,10,.82)", "#cbd2d8", 2, 1, t(3.0), fx="pop"), I.line([[630, 618], P((4, 6.2, 4))[0:2]], t(3.0), "#cbd2d8", 2, "inferred", .6)] + \
        [I.oval(x, y, 15, 15, "rgba(159,208,255,.25)", I.BLUE, 2, 1, t(3.4 + .1 * k)) for k, (x, y) in enumerate(mol)] + \
        [I.line([[586, 482], [668, 488], [688, 524], [730, 500], [794, 500]], t(5.6), I.BLUE, 3, dur=2.4), atom(814, 500, t(3.8), 16)] + \
        [I.glow(814, 500, 80, t(8.0), .9, "red")] + [I.glow(x, y, 120, t(13.4 + .2 * k), .8, "red") for k, (x, y) in enumerate(seam)] + [I.glow(*P((4, 5.1, 4)), 260, t(15.2), .7, "red")]
    # 3 · the pulse: water in, reactor on, water boils off, reactor off, water back, on again; and the clock of it
    t = sec(1.75)
    drops = lambda at: [I.line([[x, 404], [x + 6, 566]], at + .12 * k, I.BLUE, 3, "inferred", .8) for k, x in enumerate((230, 380, 530, 680, 800))]
    pulse = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(120, 400, 760, 170, "#b8a57c", r=4, at=t(.2)), I.box(120, 570, 760, 80, "#3a3128", "#6f5a44", 2, 2, t(.2)),
             I.box(120, 650, 760, 160, "#8c7452", r=4, at=t(.2))] + drops(t(.4)) + [I.box(124, 576, 752, 68, "#3f86a8", r=2, at=t(1.2), op=.6, fx="fill")] +
            [I.glow(500, 610, 300, t(2.0), .9, "red")] + [I.line([[x + 12 * math.sin(j * 1.3 + k), round(392 - 18 * j, 1)] for j in range(7)], t(3.8 + .2 * k), "#e9e2d6", 4, dur=.8, curve=True, op=.75) for k, x in enumerate((250, 370, 500, 630, 750))] +
            [I.box(124, 576, 752, 68, "#3a3128", r=2, at=t(4.8)), I.box(120, 400, 760, 410, "#0d0b09", r=4, at=t(7.4), op=.6)] +
            drops(t(9.0)) + [I.box(124, 576, 752, 68, "#3f86a8", r=2, at=t(10.0), op=.6, fx="fill"), I.glow(500, 610, 300, t(11.4), .9, "red")] +
            [I.box(140 + 240 * k, 1000, 40, 56, I.RED, r=3, at=t(12.6 if k == 0 else 14.9 + .4 * k)) for k in range(3)] +
            [I.box(180 + 240 * k, 1000, 200, 56, "#2b5d7d", r=3, at=t(14.4 if k == 0 else 15.1 + .4 * k)) for k in range(3)] +
            [I.label(160, 1102, "30 min", t(12.8), I.RED, 28), I.label(280, 1102, "2.5 h", t(14.6), I.BLUE, 28)]}
    t = sec(1.32)
    kuroda = [I.box(205, 1180, 70, 90, "#efe6d2", "#8a7a66", 2, 4, t(.6), fx="pop")] + [I.line([[218, 1200 + 14 * k], [262, 1200 + 14 * k]], t(1.0), "#6a5a46", 2, draw=False) for k in range(5)] + \
        [I.label(240, 1320, "1956", t(.8), I.BONE, 30), I.arrow([[300, 1225], [690, 1225]], t(6.6), I.AMBER, 3, dur=1.4, curve=False), I.label(495, 1200, "16 years", t(7.0), I.AMBER, 34, st="serif"),
         I.glow(760, 1225, 70, t(7.8), .9, "red"), I.oval(760, 1232, 48, 30, "#8c7452", "#cbbca8", 2, 1, t(7.8)), I.label(760, 1320, "1972", t(8.0), I.BONE, 30)]
    return remix(ep, scenes={0: s0, 2: clue, 3: pulse, 4: hour, 5: chain}, alias={6: 0}, cams={6: [1.12, 500, 930]}, adds={1: hook},
                 line_adds={(2, 1): (basin, None), (4, 1): (kuroda, None)})


def ooparts_m():
    """Out-of-place artefacts as one continuous take (see mural.py): four exhibits on trial. A hammer dated by its style, a crust
    that grows like limescale, an X-ray, nodules that grew in their rock, a carving copied from comics, and the rules of a real find."""
    remix, I = _mur()
    import copy
    from iso3d import project
    ep = ooparts()
    sec = lambda r: (lambda t: round(t / r, 2))             # times below are seconds into the rewritten narration; remix stretches each step by r
    ROCK, STEEL, WOOD = "#a08a6a", "#5b5550", "#6b4a2e"
    def hammer(x, y, at, s=1.0, style="known", c=None):
        """A claw hammer standing on its head: head centred on (x, y)."""
        head = [[x + dx * s, y + dy * s] for dx, dy in ((-75, -24), (-34, -24), (-34, -15), (22, -15), (70, -46), (82, -36), (34, 15), (-34, 15), (-34, 24), (-75, 24))]
        if style != "known":
            return [I.box(x - 13 * s, y - 250 * s, 26 * s, 235 * s, "none", c, 3, 4, at, style=style), {"k": "poly", "p": head, "fill": "none", "c": c, "w": 3, "style": style, "in": at}]
        return [I.box(x - 13 * s, y - 250 * s, 26 * s, 235 * s, WOOD, "#c9a070", 1.4, 4, at), {"k": "poly", "p": head, "fill": STEEL, "c": "#c9ccd2", "w": 1.4, "in": at + .2}]
    def plug(x, y, at, s=1.0, c="#e9e9e9"):
        return [I.box(x - 18 * s, y - 120 * s, 36 * s, 90 * s, c, "#9fb0c0", 1.2, 6 * s, at), I.box(x - 32 * s, y - 30 * s, 64 * s, 46 * s, "#b0b6bc", "#9fb0c0", 1.2, 3, at + .1),
                I.box(x - 14 * s, y + 16 * s, 28 * s, 70 * s, "#c8743c", "#9fb0c0", 1.2, 2, at + .2)] + \
               [I.line([[x - 14 * s, y + (26 + 12 * k) * s], [x + 14 * s, y + (32 + 12 * k) * s]], at + .2, "#6a3a1c", 2, draw=False) for k in range(5)]
    def sphere2d(x, y, r, at):
        return [I.oval(x, y, r, r, "#6f4a3a", "#c9a07a", 2, 1, at), I.line([[x - r, y], [x - r * .5, y + r * .14], [x, y + r * .18], [x + r * .5, y + r * .14], [x + r, y]], at + .2, "#e2cf9e", 3, curve=True, draw=False)]
    def ica(x, y, at, s=1.0):
        return [I.oval(x, y, 70 * s, 52 * s, "#5a5550", "#c9ccd2", 2, 1, at), I.line([[x - 40 * s, y + 18 * s], [x - 10 * s, y], [x + 22 * s, y - 2 * s], [x + 36 * s, y - 26 * s]], at + .2, "#c9ccd2", 3, draw=False)]
    tag = lambda x, y, ch, at: [I.box(x - 23, y - 23, 46, 46, "#efe6d2", "#8a7a66", 2, 6, at, fx="pop"), I.label(x, y + 11, ch, at, "#1a1511", 30, st="serif", halo=False)]
    nodule = [[300, 610], [322, 500], [400, 440], [520, 430], [640, 470], [700, 560], [680, 660], [560, 700], [400, 690]]
    # 0 · the exhibits: a hammer in rock, a spark plug in a stone, a grooved sphere; then their tags; then (beat 1) a close look at A
    t = sec(1.09)
    wall = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "poly", "p": nodule, "fill": ROCK, "c": "#e9dccb", "w": 2, "curve": True, "in": t(.3)}] + hammer(500, 560, t(.7)) +
            [{"k": "poly", "p": [[190, 1320], [215, 1250], [290, 1230], [360, 1260], [378, 1340], [330, 1400], [240, 1405]], "fill": "#7a6a58", "c": "#e9dccb", "w": 2, "curve": True, "in": t(2.6)}] +
            plug(285, 1322, t(3.2), .5, "rgba(233,233,233,.5)") + [I.label(285, 1222, "?", t(6.0), I.LILAC, 50, st="big")] + sphere2d(720, 1325, 70, t(8.2)) +
            tag(290, 430, "A", t(12.2)) + tag(150, 1225, "B", t(12.4)) + tag(850, 1225, "C", t(12.6))}
    t = sec(1.71)
    look = [I.label(300, 330, "Texas, 1936", t(2.8), I.BONE, 30, "start")] + hammer(756, 640, t(8.4), .68, "inferred", I.AMBER) + \
        [I.label(822, 720, "1800s style", t(11.6), I.AMBER, 30, "end")]
    # 4 · the crust: water carries minerals in, layer after layer grows round the head, like limescale in a kettle
    t = sec(1.43)
    crust = {"base": "dark", "cam": [1, 500, 880], "els": hammer(500, 810, t(.3)) +
             [I.arrow([[500 + 330 * math.cos(a), 810 + 280 * math.sin(a)], [500 + 250 * math.cos(a), 810 + 210 * math.sin(a)]], t(3.6 + .15 * k), I.BLUE, 3, "inferred", .5, False) for k, a in enumerate((0.3, 1.2, 2.0, 2.9, 3.6, 5.6))] +
             [I.dot(500 + 300 * math.cos(a), 810 + 255 * math.sin(a), 6, I.BLUE, t(3.4 + .15 * k)) for k, a in enumerate((0.3, 1.2, 2.0, 2.9, 3.6, 5.6))] +
             [{"k": "poly", "p": I.ellipse(500, 812, 110 + 30 * k, 60 + 26 * k, 36)[:-1], "fill": "none", "c": "#c9a370", "w": 3, "curve": True, "in": t(5.2 + .4 * k), "fx": "draw", "dur": .7} for k in range(6)] +
             [I.oval(500, 812, 262, 192, "#a08a6a", "none", 0, .45, t(7.8))] +
             [I.line([[708, 525], [668, 492], [642, 450]], t(8.4), "#cbd2d8", 9, curve=True, draw=False), I.line([[866, 470], [916, 482], [918, 540], [878, 560]], t(8.4), "#cbd2d8", 6, curve=True, draw=False),
              {"k": "poly", "p": [[706, 580], [700, 505], [716, 458], [790, 436], [864, 458], [880, 505], [874, 580]], "fill": "#3a3a3e", "c": "#cbd2d8", "w": 2, "curve": True, "in": t(8.4)},
              I.dot(790, 426, 10, "#cbd2d8", t(8.4)), I.box(712, 556, 156, 20, "#d8c9a8", r=6, at=t(9.0), fx="fill"), I.box(716, 540, 148, 16, "#c9b894", r=6, at=t(9.4), fx="fill"),
              I.label(500, 1160, "a few years", t(10.8), I.BONE, 38, st="serif")]}
    # 1 · the Coso artefact: a stone, a price, an X-ray, a spark plug of the 1920s
    t = sec(1.91)
    coso = [[300, 830], [330, 690], [450, 620], [600, 630], [700, 720], [710, 860], [620, 990], [460, 1010], [340, 950]]
    xray = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "poly", "p": coso, "fill": "#7a6a58", "c": "#e9dccb", "w": 2, "curve": True, "in": t(.4)},
             I.label(500, 1110, "500,000 years?", t(6.0), I.LILAC, 34), I.box(450, 330, 100, 46, "#2a2622", "#9fd0ff", 2, 6, t(8.4)),
             {"k": "fan", "x": 500, "y": 380, "a0": 66, "a1": 114, "r": 640, "n": 11, "c": I.BLUE, "in": t(8.6)},
             I.oval(500, 820, 175, 175, "#15191e", I.BLUE, 2, .92, t(10.4))] + plug(500, 840, t(15.0), 1.2) +
            [I.glow(500, 820, 240, t(15.0), .35, "scan"), I.strike(330, 1130, 670, 1080, t(16.4)), I.label(500, 1190, "1920s spark plug", t(16.0), I.AMBER, 34)]}
    # 2 · the spheres (still): the rock is old; the spheres grew in it, layer by layer; steel scratches them
    s2 = copy.deepcopy(ep["shots"][2])
    ie = next(e for e in s2["els"] if e.get("k") == "iso")
    ie["spin"] = 0
    ie["items"] = [it for it in ie["items"] if it.get("t") != "label"]
    P = lambda p: tuple(round(v, 1) for v in project(s2, p))
    A, B = P((-3, 1.8, 0)), P((2.6, 1.4, 1.4))
    t = sec(1.97)
    s2["els"] += [I.label(530, 1185, "3 billion years old", t(12.0), I.BONE, 32)] + \
        [I.ring(A[0], A[1], 18 * k, t(15.6 + .4 * k), I.AMBER, 2, dur=.4) for k in range(1, 5)] + [I.ring(B[0], B[1], 14 * k, t(17.2 + .4 * k), I.AMBER, 2, dur=.4) for k in range(1, 5)] + \
        [I.label(A[0], A[1] - 112, "natural", t(22.4), I.GREEN, 32),
         {"k": "poly", "p": [[815, 760], [690, 890], [674, 880], [796, 748]], "fill": "#cbd2d8", "c": "#ffffff", "w": 1, "in": t(24.0), "fx": "rise"},
         {"k": "poly", "p": [[815, 760], [796, 748], [850, 700], [870, 716]], "fill": "#3b2a1c", "c": "#8a6a48", "w": 1, "in": t(24.0), "fx": "rise"},
         I.line([[B[0] + 10, B[1] - 40], [B[0] + 48, B[1] - 6]], t(25.8), "#ffffff", 4, dur=.5)]
    # 3 · the Ica stone: a rider on a sauropod; dinosaurs and humans, tens of millions of years apart; comics, dung and polish
    t = sec(1.57)
    dino = [[300, 975], [380, 930], [450, 895], [540, 890], [600, 870], [640, 800], [675, 760], [705, 752], [712, 770], [690, 780], [668, 820], [648, 880], [640, 940], [625, 1000],
            [600, 1000], [598, 955], [560, 960], [548, 1005], [522, 1005], [520, 960], [470, 962], [462, 1005], [436, 1005], [432, 955], [390, 950]]
    stone = [[220, 900], [260, 700], [480, 620], [720, 680], [790, 880], [720, 1080], [500, 1130], [290, 1070]]
    Xd = lambda my: 150 + 700 * (66 - my) / 66
    icas = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "poly", "p": stone, "fill": "#5a5550", "c": "#c9ccd2", "w": 2, "curve": True, "in": t(.3)},
             {"k": "poly", "p": dino, "fill": "#c9ccd2", "c": "none", "w": 0, "op": .85, "keepop": True, "in": t(3.0)}, I.person(512, 892, 74, t(4.0), "#c9ccd2"),
             I.line([[150, 1260], [850, 1260]], t(5.2), "#8c7152", 3), I.box(150, 1250, 16, 20, "#8a8f7a", r=4, at=t(5.6)), I.label(150, 1310, "dinosaurs", t(5.6), "#cbbca8", 28, "start"),
             I.box(Xd(3.3), 1250, 850 - Xd(3.3), 20, I.AMBER, r=4, at=t(8.8)), I.label(850, 1310, "humans", t(8.8), I.AMBER, 28, "end"),
             I.arrow([[180, 1215], [800, 1215]], t(6.4), I.BONE, 2, "inferred", 1.0, False), I.label(490, 1196, "tens of millions of years", t(7.0), I.BONE, 28),
             I.box(650, 300, 220, 250, "#efe6d2", "#8a7a66", 2, 4, t(11.6)), I.line([[760, 310], [760, 540]], t(11.7), "#8a7a66", 2, draw=False), I.line([[660, 425], [860, 425]], t(11.7), "#8a7a66", 2, draw=False),
             {"k": "poly", "p": [[x * .26 + 600, y * .26 + 130] for x, y in dino], "fill": "#3a2a1c", "c": "none", "w": 0, "in": t(11.8)},
             I.label(760, 595, "comics", t(12.0), I.BONE, 28), I.arrow([[650, 500], [600, 640]], t(12.6), I.AMBER, 3, "inferred", .6, False),
             {"k": "poly", "p": stone, "fill": "#3a2a1c", "c": "none", "w": 0, "curve": True, "op": .45, "keepop": True, "in": t(14.4), "dur": 1.6},
             I.oval(200, 420, 60, 18, "#2a2018", "#c9a070", 2, 1, t(15.6)), I.box(140, 420, 120, 50, "#2a2018", "#c9a070", 2, 4, t(15.6)), I.oval(200, 470, 60, 18, "#2a2018", "#c9a070", 2, 1, t(15.6)),
             I.label(200, 545, "shoe polish", t(15.8), I.BONE, 28)]}
    # 6 · what a real find needs: found in place, in a datable layer, recorded as it is dug; none of the four was
    t = sec(1.40)
    dig = {"base": "section", "ground": 760, "tod": "day", "layers": [{"d": 0, "c": "#8a6a48", "t": ""}, {"d": 160, "c": "#6f5a44", "t": ""}, {"d": 330, "c": "#5a4632", "t": ""},
                                                                      {"d": 500, "c": "#4a3a2c", "t": ""}], "cam": [1, 500, 880], "els": [
             I.box(380, 760, 240, 520, "rgba(12,9,7,.25)", I.BONE, 2, 2, t(4.4), style="inferred"),
             {"k": "poly", "p": [[600, 1196], [640, 1196], [620, 1150]], "fill": "#f2c94c", "c": "#1a1511", "w": 2, "in": t(6.2), "fx": "pop"}, I.label(620, 1190, "1", t(6.2), "#1a1511", 22, halo=False),
             I.box(470, 1170, 70, 24, STEEL, "#c9ccd2", 1.4, 4, t(5.8)), I.ring(505, 1182, 48, t(7.8), I.AMBER, 3),
             I.box(40, 1090, 920, 170, I.AMBER, r=2, at=t(9.4), op=.16), I.label(910, 1130, "dated layer", t(9.6), I.AMBER, 30, "end"),
             I.person(250, 760, 170, t(12.0), "#2a2018"), I.box(282, 640, 40, 28, "#2a2622", "#cbd2d8", 2, 4, t(12.4)), I.glow(302, 652, 90, t(12.6), .9, "lamp"),
             I.box(170, 650, 46, 60, "#efe6d2", "#8a7a66", 1.5, 3, t(12.8))] +
            hammer(200, 445, t(14.2), .3) + plug(400, 440, t(14.4), .45) + sphere2d(600, 425, 36, t(14.6)) + ica(800, 425, t(14.8), .7) +
            [I.strike(150 + 200 * k, 470, 250 + 200 * k, 370, t(15.0 + .15 * k)) for k in range(4)]}
    # 5 · the verdict: humankind's span; each exhibit turned out younger, or natural; and an empty slot for a real find
    t = sec(1.93)
    X = lambda my: 130 + 740 * (3.3 - my) / 3.3
    verdict = {"base": "dark", "cam": [1, 500, 880], "els": [I.label(500, 560, "older than humankind?", t(.4), I.LILAC, 36), I.strike(290, 580, 710, 520, t(2.2))] +
               [I.box(130, 880, 740, 26, I.AMBER, r=6, at=t(6.0), fx="fill", op=.85), I.label(130, 960, "3.3 million years ago", t(8.0), I.AMBER, 28, "start"),
                I.label(300, 860, "stone tools", t(6.2), I.AMBER, 30), I.box(X(.3), 872, 870 - X(.3), 42, I.BONE, r=6, at=t(11.0)),
                I.label(870, 850, "our species", t(11.2), I.BONE, 30, "end"), I.label(870, 960, "today", t(11.4), "#cbbca8", 28, "end")] +
               hammer(150, 1160, t(13.8), .3) + [I.label(150, 1240, "1800s", t(13.8), I.BONE, 28)] + plug(330, 1150, t(14.2), .45) + [I.label(330, 1240, "1920s", t(14.2), I.BONE, 28)] +
               sphere2d(510, 1150, 36, t(16.0)) + [I.label(510, 1240, "natural", t(16.0), I.GREEN, 28)] + ica(690, 1150, t(14.6), .7) + [I.label(690, 1240, "modern", t(14.6), I.BONE, 28)] +
               [I.box(830, 1105, 80, 90, "none", I.BONE, 2.5, 8, t(17.6), style="inferred")] + I.question(870, 1180, t(18.2), 56, I.BONE)}
    return remix(ep, scenes={0: wall, 1: xray, 2: s2, 3: icas, 4: crust, 5: verdict, 6: dig}, cams={},
                 beat_adds={1: (look, [1.5, 540, 560])})


def EPISODES():
    import lg_d      # 00.01 rebuilt from the legacy film
    return [lg_d.where_we_stand_m(), dating_m(), grades_m(), oklo_m(), ooparts_m(), astronauts_m()]
