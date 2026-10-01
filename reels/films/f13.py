"""File 13 · The Files. What institutions hid, and what they only claimed to hide.
Tuskegee, Stargate, Roswell, the UAP disclosures and the unpublished past (MKUltra is 13.01, made earlier).
Every claim is weighed on what is on the record; the documented secrets are stated plainly, the rumoured ones wait for evidence."""
import math
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import sphere, box

SERIES = "The Files"
PAPER = "#efe6d2"; INK = "#2a2219"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags, mood="mystery"):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": mood,
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


def page(x=140, y=420, w=720, h=900, i=.1):
    """A sheet of paper with ruled text lines."""
    return [{"k": "rect", "x": x, "y": y, "w": w, "h": h, "fill": PAPER, "c": "#fff8ea", "sw": 1.2, "in": i}]


# ---------------------------------------------------------------- 13.02 Tuskegee
def tuskegee():
    s0 = stat("600", "men", "enrolled in 1932 in Macon County, Alabama: 399 with syphilis, 201 without", "CDC; Jones 1993")
    v = View(-88.9, -84.4, 29.9, 35.2, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Tuskegee", -85.69, 32.42, {"c": GOLD}), ("Montgomery", -86.3, 32.37, {"a": "end", "lx": -18}), ("Birmingham", -86.8, 33.52, {})],
                 extra=[{"k": "label", "x": v.p(-86.9, 31.2)[0], "y": v.p(-86.9, 31.2)[1], "t": "Alabama", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    tl, ax = timeline(1928, 2008, [(1930, "1930"), (1950, "1950"), (1970, "1970"), (1990, "1990")], "Forty years")
    tl["els"] += [{"k": "band", "x0": ax.x(1932), "x1": ax.x(1972), "y": 470, "h": 16, "c": RED, "op": .85, "t": "the study", "in": .3}] + \
                 event(ax, 1943, "penicillin: the standard cure", row=1, c=SCAN, i=.6, sub="not offered to the men") + event(ax, 1969, "a panel votes to continue", row=0, c=BONE, i=.9) + \
                 event(ax, 1972, "the press story · the end", row=2, c=GOLD, i=1.2) + event(ax, 1997, "the apology", row=1, c=BONE, i=1.5)
    s2 = tl
    s3 = stat("29", "years", "from penicillin becoming the standard cure to the end of the study", "CDC timeline")
    s4 = quote("What was done cannot be undone. But we can end the silence.", "President Bill Clinton · apology, 16 May 1997", y=720, size=46)
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what changed after Tuskegee", "#8fd9b0", ["informed consent, in writing", "the National Research Act, 1974", "review boards for research on people", "the Belmont Report, 1979"])}
    s6 = like(s0, cam=[1.1, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:tension][k:TUSKEGEE · ALABAMA][act:grave, steady]In {1932|nineteen thirty-two}, government doctors began to ^watch ^six hundred Black men. [act:quiet, precise]Three hundred and ^ninety-nine of them had ^syphilis.",
                      "[d:tension][cam:1.1|0|0][act:low, letting it sit]They were ^never ^told what they had."], cut=False),
        B("world", 1, ["[d:calm][k:THE STUDY][act:quiet, placing us there]Macon County, ^Alabama. [act:measured, the deception]The men were told they were being ^treated for 'bad blood'. [act:plainly, heavy]Hot ^meals, ^rides, ^burial money.",
                       "[d:build][act:cold, deliberate]The real aim: to watch what ^untreated syphilis does@verb to the human body, all the way to ^autopsy."]),
        B("collision", 2, ["[d:build][k:THE CURE][act:plain fact, even]By {1943|nineteen forty-three}, penicillin was the standard ^cure. [act:slower, heavy]The men were ^not offered it. [sfx:hit][go:3|0][act:steady, holding back]The study kept ^going. [act:the weight of it, slow]For ^twenty-nine more years."]),
        B("cost", 2, ["[d:build][k:THE CHOICE][act:plain storytelling, respectful]In {1966|nineteen sixty-six}, a health-service investigator, Peter Buxtun, ^objected. [act:dry, disappointed]He was ^brushed off.",
                      "[d:build][act:neutral, setting it up]In {1969|nineteen sixty-nine}, a government ^panel reviewed the study... [act:quiet disbelief, slower]and voted to ^continue."]),
        B("reversal", 4, ["[d:reveal][k:THE END][act:resolve, picking up pace]Buxtun went to the ^press. [act:clear, brisk]In July {1972|nineteen seventy-two}, a reporter, Jean Heller, broke the ^story. [act:quiet relief]The study ^ended that November.",
                          "[d:build][act:measured, sober]A ^settlement followed. [act:solemn, with care]And in {1997|nineteen ninety-seven}, a presidential ^apology."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:grave, weighing it][tune:rise]Left untreated, on ^purpose, for decades? [act:firm, sober][tune:fall]^*Established*, by the government's ^own records@noun.",
                     "[d:tension][p:0.93][act:gentle, to the viewer]It's one big ^reason every medical study now has to ask for your ^consent."]),
    ]
    return EP("tuskegee", "13.02", "Tuskegee: Forty Years Without Treatment", "tuskegee", "solid", "Did the US government deliberately leave Black men with syphilis untreated for decades?", "They were never *told*.", beats, shots,
              "CDC, The USPHS Untreated Syphilis Study at Tuskegee · Jones 1993, Bad Blood · Reverby 2009 · Ad Hoc Advisory Panel 1973 · Heller 1972, AP · Clinton 1997",
              "For forty years, government doctors watched hundreds of Black men with syphilis go untreated, long after the cure existed: the study, the whistleblower, and what changed.",
              ["#Tuskegee", "#History", "#MedicalEthics", "#BlackHistory", "#TheFiles"], mood="cold")


# ---------------------------------------------------------------- 13.03 Stargate
def stargate():
    sk = page(160, 440, 680, 820) + \
         [{"k": "label", "x": 200, "y": 500, "t": "TARGET 4471 · coordinates only", "st": "small", "c": INK, "halo": False, "a": "start", "in": .3},
          {"k": "line", "p": [[330, 1080], [330, 700], [700, 700], [700, 1080]], "c": INK, "w": 3, "in": .6, "fx": "draw", "dur": 1.2},
          {"k": "line", "p": [[300, 700], [730, 700]], "c": INK, "w": 5, "in": 1.2, "fx": "draw", "dur": .6},
          {"k": "line", "p": [[520, 700], [520, 820], [490, 850], [550, 850]], "c": INK, "w": 2, "in": 1.6, "fx": "draw", "dur": .8},
          {"k": "line", "p": [[270, 1080], [760, 1080]], "c": INK, "w": 2, "in": 1.8, "fx": "draw"},
          {"k": "label", "x": 600, "y": 660, "t": "big · metal · a wheel? a crane?", "st": "ital", "c": "#7a2a1a", "halo": False, "in": 2.2},
          {"k": "label", "x": 500, "y": 1210, "t": "a viewer's sketch · schematic", "st": "small", "c": "#6a645c", "halo": False, "in": 2.5}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": sk}
    v = View(-125, -66, 24, 50, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("SRI · Menlo Park", -122.18, 37.46, {"c": GOLD}), ("Fort Meade · Maryland", -76.74, 39.11, {"a": "end", "lx": -18})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}])
    s2 = stat("23", "years", "of government-funded remote viewing, 1972 to 1995, at a cost of about $20 million", "AIR 1995; CIA CREST files")
    names = ["GONDOLA WISH", "GRILL FLAME", "CENTER LANE", "SUN STREAK", "STAR GATE"]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 520, "t": "one army unit, five code names", "c": AMBER, "in": .2}] +
          [{"k": "label", "x": 500, "y": 620 + i * 90, "t": n, "st": "serif", "size": 44 if i == 4 else 34, "c": GOLD if i == 4 else "#e9dccb", "in": .5 + i * .35} for i, n in enumerate(names)]}
    s4 = quote("Vague and ambiguous.", "the evaluation for the CIA · 1995", y=740, size=64)
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 480, "t": "the two scientists who reviewed the lab work", "in": .2},
                                                    {"k": "line", "p": [[500, 560], [500, 1060]], "c": "#6a645c", "w": 1.4, "in": .3},
                                                    {"k": "label", "x": 290, "y": 640, "t": "Jessica Utts", "st": "serif", "size": 36, "in": .5}, {"k": "label", "x": 290, "y": 690, "t": "statistician", "st": "small", "in": .6},
                                                    {"k": "label", "x": 290, "y": 820, "t": "a real effect", "st": "serif", "size": 34, "c": "#8fd9b0", "in": 1.0},
                                                    {"k": "label", "x": 710, "y": 640, "t": "Ray Hyman", "st": "serif", "size": 36, "in": .7}, {"k": "label", "x": 710, "y": 690, "t": "psychologist", "st": "small", "in": .8},
                                                    {"k": "label", "x": 710, "y": 820, "t": "premature", "st": "serif", "size": 34, "c": "#ffb09a", "in": 1.3},
                                                    {"k": "label", "x": 500, "y": 1140, "t": "1978: critics found cues left in the transcripts", "st": "small", "c": AMBER, "in": 1.7}]}
    tl, ax = timeline(1968, 2022, [(1970, "1970"), (1980, "1980"), (1990, "1990"), (2000, "2000"), (2020, "2020")], "The programme")
    tl["els"] += [{"k": "band", "x0": ax.x(1972), "x1": ax.x(1995), "y": 470, "h": 16, "c": GOLD, "op": .85, "t": "government money", "in": .3}] + \
                 event(ax, 1974, "a paper in Nature", row=1, c=BONE, i=.6) + event(ax, 1977, "the army unit", row=0, c=SCAN, i=.8) + \
                 event(ax, 1995, "evaluated · shut down", row=2, c=RED, i=1.1) + event(ax, 2017, "the files go online", row=1, c=BONE, i=1.4)
    s6 = tl
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 2, ["[d:intrigue][k:STARGATE][sfx:boom][act:setting it up, straight face]For ^twenty-three years, the United States government paid people to ^spy... [act:the payoff, wide-eyed][tune:risefall]with their ^minds.",
                      "[d:tension][cam:1.12|0|0][act:matter of fact]The files are ^public now. [act:curious, leaning in][tune:rise]Did it ^work?"], cut=False),
        B("world", 1, ["[d:calm][k:THE PROGRAMME][act:storytelling, easy]It began in {1972|nineteen seventy-two}, at a research institute in ^California, with ^CIA money. [go:3|0][act:moving on, brisk]Then an ^army unit in Maryland, under a string of ^code names.",
                       "[d:build][act:relishing the names][tune:level]Gondola Wish. [act:same rhythm][tune:level]Grill Flame. [act:keeping the beat][tune:level]Center Lane. [act:one more][tune:level]Sun Streak. [sfx:shimmer][act:the famous one, a flourish][tune:highfall]^Star Gate."]),
        B("collision", 0, ["[d:build][k:THE METHOD][act:introducing the term, plainly]^Remote viewing. [act:explaining, a hint of wonder]Give a viewer a target they ^can't see, just a number@count, and they ^sketch it.",
                           "[d:build][act:telling the legend, animated]The viewers describe real hits: a giant ^crane at a secret Soviet site, sketched from ^half a world away."]),
        B("cost", 5, ["[d:build][k:THE LAB][act:even-handed, setting up both]The scientists who reviewed the lab work ^split. [act:one side, fair][tune:fallrise]A ^statistician saw a ^real effect. [act:the other side, crisp][tune:fall]A ^psychologist said: ^premature.",
                      "[d:aside][act:quieter, a telling detail]Back in {1978|nineteen seventy-eight}, critics had found ^clues to the targets left in the ^transcripts."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:serious now, lean in]In {1995|nineteen ninety-five} the CIA ordered an ^evaluation. [act:dry, quoting it]Its word for the spying: ^vague and ^ambiguous.",
                          "[d:build][sfx:hit][act:plain, damning]^No operation had been guided by it. [act:dry, a small shake of the head]The unit was down to ^three people. [go:6|0][act:final, closing the file]It was ^shut down that year."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]^Reliable psychic intelligence? [act:the verdict, firm][tune:fall]*Ruled ^out*, by the programme's ^own evaluation. [act:fair, the open part][tune:rise]A real effect in the ^lab? [act:honest, even][tune:fallrise]^Still argued over.",
                     "[d:tension][p:0.93][act:a gentle joke, deadpan][tune:fall]The psychic spies never ^saw that report coming."]),
    ]
    return EP("stargate-psychic", "13.03", "Stargate: The Pentagon's Psychic Spies", "stargate-psychic", "debunked", "Did government-funded remote viewing ever produce reliable intelligence?", "Spies... with their *minds*.", beats, shots,
              "Mumford, Rose & Goslin 1995 (AIR) · Utts 1996 · Hyman 1996 · Targ & Puthoff 1974, Nature · Marks & Kammann 1978, Nature · CIA CREST files",
              "Twenty-three years and about $20 million of US government money spent on remote viewing: the code names, the famous hits, the lab fight and the evaluation that closed it.",
              ["#Stargate", "#CIA", "#RemoteViewing", "#ColdWar", "#TheFiles"])


# ---------------------------------------------------------------- 13.04 Roswell
def roswell():
    np_ = page(120, 420, 760, 940) + \
          [{"k": "label", "x": 500, "y": 490, "t": "ROSWELL DAILY RECORD", "st": "serif", "size": 40, "c": INK, "halo": False, "in": .3},
           {"k": "line", "p": [[160, 520], [840, 520]], "c": INK, "w": 2, "in": .3}, {"k": "label", "x": 500, "y": 548, "t": "Tuesday, 8 July 1947", "st": "small", "c": "#6a645c", "halo": False, "in": .4},
           {"k": "line", "p": [[160, 566], [840, 566]], "c": INK, "w": 1, "in": .4},
           {"k": "label", "x": 500, "y": 650, "t": "RAAF Captures Flying Saucer", "st": "serif", "size": 54, "c": INK, "halo": False, "in": .7},
           {"k": "label", "x": 500, "y": 720, "t": "On Ranch in Roswell Region", "st": "serif", "size": 44, "c": INK, "halo": False, "in": 1.0}] + \
          [{"k": "line", "p": [[170 + c * 230, 790 + r * 26], [370 + c * 230, 790 + r * 26]], "c": "#8c8478", "w": 2, "op": .7, "in": 1.2 + r * .02} for c in range(3) for r in range(16)]
    for e in np_:                                  # sit the paper below the hook title
        if "y" in e: e["y"] += 140
        if "p" in e: e["p"] = [[x, y + 140] for x, y in e["p"]]
    np_[0]["h"] = 800
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": np_}
    v = View(-113, -100, 28.5, 38, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Roswell Army Air Field", -104.52, 33.39, {"c": GOLD}), ("the debris, near Corona", -105.3, 33.95, {"a": "end", "lx": -18, "ly": -22}), ("Alamogordo · the balloon launches", -105.96, 32.9, {"a": "end", "lx": -18, "ly": 34})],
                 extra=[{"k": "line", "p": [v.p(-105.96, 32.9), v.p(-105.7, 33.5), v.p(-105.3, 33.95)], "c": GOLD, "w": 1.6, "op": .7, "style": "inferred", "curve": True, "in": 1.0},
                        {"k": "label", "x": v.p(-106.5, 36.6)[0], "y": v.p(-106.5, 36.6)[1], "t": "New Mexico", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    train = [{"t": "slab", "x0": -14, "x1": 14, "z0": -10, "z1": 10, "y": 0, "c": "#b8905e"}, {"t": "line", "p": [[0, 2, 0], [0, 64, 0]], "c": "#e9dccb", "w": 1.4, "op": .8}]
    for k in range(6):
        train += sphere(0, 0, 1.6, "#e9dccb", n=8, y=38 + k * 4.4)
    for y in (12, 20, 28):
        train += [{"t": "prism", "pts": [[-1.6, 0], [0, -1.6], [1.6, 0], [0, 1.6]], "y": y, "h": 2.4, "c": "#c9ccd2", "edge": "rgba(0,0,0,.35)"}]
    train += [{"t": "box", "x": 0, "z": 0, "y": 6, "w": 1.2, "d": 1.2, "h": 1.4, "c": "#5b5550", "edge": "rgba(255,236,206,.3)"},
              L_(0, 62, "Project Mogul · a train of balloons", GOLD, z=0, dy=-24), L_(0, 24, "radar reflectors: foil, paper, sticks", "#cfe6ff", z=0, dy=0),
              L_(0, 7, "a microphone for Soviet atomic tests", "#f2dcb4", z=0, dy=0), L_(0, 0, "schematic · the real trains were far taller", "#cfe6ff", z=10, dy=40)]
    for L in train:
        if L.get("t") == "label" and L.get("dy") == 0:
            L["dy"] = -8; L["a"] = "start"; L["x"] = 3
    s2 = iso(train, cam=[1, 500, 900], s=12, x=360, y=1180, az=-20, spin=.8, el=.4, table=None)
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what the rancher described, 9 July 1947", AMBER, ["rubber strips", "tinfoil", "a rather tough paper", "sticks", "no engine · no metal parts"])}
    s4 = stat("4", "explanations", "a flying disc, a weather balloon, a secret balloon project, and test dummies for the bodies", "Roswell Daily Record 1947; Air Force 1995, 1997")
    tl, ax = timeline(1940, 2030, [(1940, "1940"), (1960, "1960"), (1980, "1980"), (2000, "2000"), (2020, "2020")], "A story in layers")
    tl["els"] += event(ax, 1947, "the find", row=1, c=GOLD, i=.3, sub="disc, then balloon") + event(ax, 1978, "Marcel's interview", row=0, c=BONE, i=.6) + \
                 event(ax, 1994, "Air Force: Project Mogul", row=2, c=SCAN, i=.9) + event(ax, 1997, "'Case Closed': dummies", row=1, c=SCAN, i=1.1) + event(ax, 2024, "the Pentagon's review", row=0, c=SCAN, i=1.4)
    s5 = tl
    s6 = like(s2, cam=[1.15, 400, 880])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:ROSWELL · 1947][sfx:boom][act:setting the scene, measured]July eighth, {1947|nineteen forty-seven}. [act:deadpan, let the absurdity land]An American ^army base announces it has captured a flying ^saucer.",
                      "[d:tension][cam:1.12|0|0][act:dry, unimpressed][tune:fall]A few hours later, it's a ^weather balloon. [act:skeptical, one eyebrow up][tune:rise]Case ^closed? [act:quiet, certain, a knowing smile][tune:fall]Not ^even close@adj."], cut=False),
        B("world", 1, ["[d:calm][k:THE FIND][act:plain storytelling]A rancher, Mac Brazel, found ^debris scattered across his land and told the ^sheriff. [act:matter of fact]An officer from the base, Major Jesse Marcel, collected it.",
                       "[d:build][go:3|0][act:reading out the evidence, slightly amused]What Brazel described: rubber strips, tinfoil, tough paper, sticks. [act:flat, pointed]No ^engine. No ^metal parts."]),
        B("collision", 5, ["[d:build][k:THE CASE][act:the turn: news that changes everything]Thirty-one years later, Marcel said the balloon story was a ^cover. [sfx:shimmer][act:building, a little faster]Researchers collected ^hundreds of interviews: strange material, threats, ^bodies.",
                           "[d:aside][act:a quiet caveat, lower]Most of them recorded ^thirty to ^fifty years after the event."]),
        B("cost", 2, ["[d:build][k:THE SECRET][act:revealing a fact, confident]In {1994|nineteen ninety-four}, the Air Force ^named it: Project@noun ^Mogul. [act:explaining, brisk]Top secret trains of balloons, carrying microphones to listen for Soviet atomic tests.",
                      "[d:aside][act:wry, a small smile]A real ^secret. [act:dry, pointed]Just not ^that one."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in]But the official story kept ^changing. [act:counting them off][tune:level]Disc. [tune:level]Weather balloon. [tune:fall]Mogul. [act:the punchline, slower]Then, for the bodies: test ^dummies... [act:the sting, quiet][tune:fall]not dropped until the {1950s|nineteen fifties}.",
                          "[d:build][sfx:hit][act:heavier, deliberate][tune:rise]And the base's ^records@noun from those years? [act:flat, final][tune:highfall]Destroyed. [act:letting it hang, quieter][tune:fall]^Nobody knows who authorised it."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A crashed alien ^craft? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:firm, precise][tune:fall]Not one ^piece, ^photo or ^document from {1947|forty-seven} ^supports it.",
                     "[d:tension][p:0.93][act:a concession, sincere][tune:fall]The cover-up was ^real. [gap:0.5][act:the last word, quiet and certain][tune:fall]What it ^covered, as far as the record@noun shows, was a ^balloon."]),
    ]
    return EP("roswell-mogul", "13.04", "Roswell: A Balloon, a Secret and a Legend", "roswell-mogul", "unsupported", "Was a craft of non-human origin recovered at Roswell in 1947 and hidden?", "Case closed? *Not even close*.", beats, shots,
              "Roswell Daily Record, 8–9 July 1947 · GAO 1995 · Weaver & McAndrew 1995 · McAndrew 1997 · AARO 2024 · Randle & Schmitt 1991 · Saler, Ziegler & Moore 1997",
              "In July 1947 the army said it had captured a flying disc, then took it back within hours: the secret balloon project, the shifting explanations, the destroyed records and the legend that grew.",
              ["#Roswell", "#UFO", "#Area51", "#ColdWar", "#TheFiles"])


# ---------------------------------------------------------------- 13.05 UAP disclosure
def uap():
    G = "#9fe0a8"
    flir = [{"k": "rect", "x": 100, "y": 460, "w": 800, "h": 800, "fill": "#0d1a12", "c": "#2f5a3a", "sw": 2, "in": .1}] + \
           [{"k": "line", "p": [[500, 560], [500, 800]], "c": G, "w": 1.6, "op": .8, "in": .3}, {"k": "line", "p": [[500, 920], [500, 1160]], "c": G, "w": 1.6, "op": .8, "in": .3},
            {"k": "line", "p": [[200, 860], [440, 860]], "c": G, "w": 1.6, "op": .8, "in": .3}, {"k": "line", "p": [[560, 860], [800, 860]], "c": G, "w": 1.6, "op": .8, "in": .3},
            {"k": "rect", "x": 440, "y": 800, "w": 120, "h": 120, "fill": "none", "c": G, "sw": 1.6, "in": .5},
            {"k": "glow", "x": 500, "y": 860, "r": 70, "op": .5, "in": .8}, {"k": "circle", "x": 500, "y": 860, "r": 14, "fill": "#f4fff2", "c": "none", "w": 0, "in": .8},
            {"k": "label", "x": 130, "y": 500, "t": "IR  ·  NAR  ·  TRK", "st": "small", "c": G, "a": "start", "in": .4},
            {"k": "label", "x": 870, "y": 500, "t": "RNG ---", "st": "small", "c": G, "a": "end", "in": .4},
            {"k": "cap", "x": 500, "y": 400, "t": "a Navy targeting camera · schematic", "in": .2},
            {"k": "label", "x": 500, "y": 1320, "t": "three such videos released by the Pentagon, April 2020", "st": "small", "c": AMBER, "in": 1.2}]
    for e in flir:                                 # clear of the hook title
        if "y" in e: e["y"] += 90
        if "p" in e: e["p"] = [[x, y + 90] for x, y in e["p"]]
    flir[0]["h"] = 760
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": flir}
    s1 = stat("144", "reports", "reviewed by US intelligence in 2021; only one could be explained", "ODNI 2021")
    hr = [{"k": "rect", "x": 150, "y": 980, "w": 700, "h": 60, "fill": "#5a4330", "c": "#c9a070", "sw": 1.4, "in": .2},
          {"k": "person", "x": 500, "y": 980, "h": 170, "t": False, "in": .4},
          {"k": "rect", "x": 470, "y": 940, "w": 60, "h": 24, "fill": "#1a1511", "c": "#c9a070", "sw": 1, "in": .5},
          {"k": "cap", "x": 500, "y": 560, "t": "under oath · House subcommittee · 26 July 2023", "in": .3},
          {"k": "label", "x": 500, "y": 680, "t": "“a crash-retrieval programme”", "st": "serif", "size": 38, "in": .8},
          {"k": "label", "x": 500, "y": 740, "t": "“non-human biologics”", "st": "serif", "size": 38, "in": 1.1},
          {"k": "label", "x": 500, "y": 1120, "t": "his sources: other people · access: denied", "c": "#ffb09a", "in": 1.6}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": hr}
    s3 = stat("2,000+", "cases", "in the Pentagon's UAP office by February 2026; about 1,000 lack enough data to analyse", "DefenseScoop 2026")
    tl, ax = timeline(2016, 2027, [(2017, "2017"), (2019, "2019"), (2021, "2021"), (2023, "2023"), (2025, "2025")], "Nine years of disclosure")
    tl["els"] += event(ax, 2017, "a hidden study revealed", row=1, c=GOLD, i=.3) + event(ax, 2020, "Navy videos", row=0, c=BONE, i=.5) + \
                 event(ax, 2021, "144 reports", row=2, c=SCAN, i=.7) + event(ax, 2023, "testimony", row=0, c=AMBER, i=.9) + \
                 event(ax, 2024, "review: no evidence", row=1, c=SCAN, i=1.1) + event(ax, 2026, "six file releases", row=2, c=GOLD, i=1.3)
    s4 = tl
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("on the record", "#8fd9b0", ["a hidden UFO study, 2007–2012", "sightings still unexplained", "alien stories spread as hazing"], y=460, size=28) +
          grp("only said", "#ffb09a", ["recovered craft", "non-human bodies", "reverse-engineering"], y=850, size=28)}
    s6 = stat("0", "craft", "made available for independent examination, after nine years and six releases of files", "AARO 2024; Pentagon releases 2026")
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:UAP · THE PENTAGON][sfx:boom][act:setting the scene, intrigued]In {2017|twenty seventeen}, the New York Times revealed that the Pentagon had been ^secretly studying ^UFOs.",
                      "[d:tension][cam:1.12|0|0][act:brisk, stacking it up]Nine years later: ^sworn testimony, a presidential ^order, ^six releases of files. [act:the real point, curious][tune:fall]So what has ^actually been ^admitted?"], cut=False),
        B("world", 0, ["[d:calm][k:ON THE RECORD][act:plain facts, one by one][tune:level]A ^hidden study, funded from {2007|two thousand seven} to {2012|twenty twelve}. [act:next item, steady][tune:fall]^Navy videos, released in {2020|twenty twenty}.",
                       "[d:build][go:1|0][sfx:shimmer][act:building, careful]In {2021|twenty twenty-one}, US intelligence reviewed a hundred and ^forty-four reports... [act:the sting, dry]and could explain ^one."]),
        B("collision", 2, ["[d:build][k:UNDER OATH][act:serious, reporting it straight]In {2023|twenty twenty-three}, a former intelligence officer, David Grusch, told Congress under ^oath about a decades-long ^crash-retrieval programme. [act:careful, measured]And ^non-human biologics.",
                           "[d:build][act:the caveat, fair]But he heard it from ^others. [act:neutral, reporting]He says he was ^denied access."]),
        B("cost", 3, ["[d:build][k:THE REVIEW][act:plain, the scale of it]The Pentagon's UAP office now has over two ^thousand cases. [act:firm, precise]Its {2024|twenty twenty-four} review found ^no verifiable evidence of alien technology. [gap:0.4][act:one-word punch, calm][tune:highfall]^Ever.",
                      "[d:aside][act:amused, a strange aside]And in {2025|twenty twenty-five}, a twist: some airmen had been told, as a ^hazing ritual, that they'd joined a secret ^alien programme."]),
        B("reversal", 4, ["[d:reveal][k:THE FILES][act:the big moment, measured]In {2026|twenty twenty-six}, the ^president ordered the files ^out. [act:counting, steady]^Six releases. [sfx:hit][act:what they held, plainly][tune:level]^Unresolved sightings. [act:one by one, firm][tune:level]No ^craft. [act:same beat][tune:level]No ^bodies. [act:the last, final][tune:fall]No ^material.",
                          "[d:build][go:5|0][act:fair, open-minded]Some cases remain ^unexplained. [act:gentle, the key distinction]And ^unexplained isn't the same as ^alien."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]^Recovered alien craft? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the other side, fair][tune:rise]^Hidden studies and ^false stories? [act:plain, firm][tune:fall]On the ^record@noun.",
                     "[d:tension][p:0.93][act:sincere, an open door]^One piece of material, examined in public, would change ^everything."]),
    ]
    return EP("uap-disclosure", "13.05", "UAP Disclosure: What the Government Has Admitted", "uap-disclosure", "unsupported", "Does the US government hold recovered craft of non-human origin?", "What has actually been *admitted*?", beats, shots,
              "Cooper, Blumenthal & Kean 2017, NYT · ODNI 2021 · US House 2023 · NASA 2023 · AARO 2024 · Schectman & Viswanatha 2025, WSJ · CBS News 2026",
              "Secret studies, sworn testimony and six releases of Pentagon files: nine years into UFO disclosure, what is on the record and what is still only said.",
              ["#UAP", "#UFO", "#Disclosure", "#Pentagon", "#TheFiles"])


# ---------------------------------------------------------------- 13.06 The unpublished past
def unpublished():
    shelves = [{"t": "slab", "x0": -16, "x1": 16, "z0": -10, "z1": 10, "y": 0, "c": "#5a4a3a"}]
    for row in range(3):
        z = -6 + row * 6
        shelves += [box(0, z, 0, 26, 1.6, .15, "#7a6248"), box(0, z, 2, 26, 1.6, .15, "#7a6248"), box(0, z, 4, 26, 1.6, .15, "#7a6248")]
        for lvl in range(3):
            for k in range(8):
                if (row * 7 + lvl * 3 + k) % 5 == 0:
                    continue
                shelves.append(box(-11.2 + k * 3.2, z, lvl * 2 + .15, 2.8, 1.4, 1.5, ["#c9ad85", "#b8a57c", "#d6c49c"][(k + lvl) % 3], "rgba(0,0,0,.35)"))
    shelves += [{"t": "person", "x": 14, "y": 0, "z": 7, "h": 1.7},
                L_(0, 6.2, "boxes of finds, catalogued or not", GOLD, z=-6, dy=-24), L_(0, 0, "a storeroom · schematic", "#cfe6ff", z=9, dy=40)]
    s0 = iso(shelves, cam=[1, 500, 900], s=18, x=500, y=1010, az=-28, spin=1.0, el=.45, table=None)
    v = View(24, 36, 22.5, 32, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Oxyrhynchus", 30.66, 28.54, {"c": GOLD}), ("Cairo", 31.24, 30.04, {})],
                 extra=[{"k": "label", "x": v.p(28, 26)[0], "y": v.p(28, 26)[1], "t": "Egypt", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = stat("500,000", "fragments", "of papyrus, roughly, dug at Oxyrhynchus from 1896 to 1907; about 5,476 texts published by 2019", "Parsons, in Press 2020")
    s3 = stat("10,000+", "digs", "rescue and salvage excavations in Israel since 1948, many never properly published", "Israel Antiquities Authority")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("why finds stay in the box", AMBER, ["digging gets funded; writing up doesn't", "construction digs outpace the specialists", "excavators retire, and die", "storerooms fill up"])}
    tl, ax = timeline(1880, 2035, [(1900, "1900"), (1940, "1940"), (1980, "1980"), (2020, "2020")], "The backlog")
    tl["els"] += event(ax, 1896, "Oxyrhynchus dug", row=1, c=GOLD, i=.3) + event(ax, 1967, "Kenyon's Jerusalem dig ends", row=0, c=BONE, i=.6, sub="published about 50 years later") + \
                 event(ax, 2001, "a call to pause new digs", row=2, c=SCAN, i=.9) + event(ax, 2025, "Israel's database online", row=1, c=SCAN, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.2, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE STOREROOMS][sfx:boom][act:setting it up, curious]^Much of what archaeologists dig up... [act:the surprise, quieter]is ^never fully published.",
                      "[d:tension][cam:1.12|0|0][act:tempting the viewer][tune:rise]Hidden on ^purpose? [act:dry, a small smile]The real reason is more ^boring. [act:the turn, serious]And more ^worrying."], cut=False),
        B("world", 1, ["[d:calm][k:THE PAPYRI][act:setting the scene]Egypt, {1896|eighteen ninety-six}. [act:amused, storytelling]Two Oxford scholars dig the ^rubbish mounds of Oxyrhynchus. [go:2|0][act:wonder, the haul]Roughly ^half a million papyrus fragments.",
                       "[d:build][act:dry, letting the gap show]More than a ^century later, about ^five and a half thousand texts are published."]),
        B("collision", 3, ["[d:build][k:THE BACKLOG][act:reporting, steady]Israel's antiquities authority says it has run over ten ^thousand rescue digs since {1948|nineteen forty-eight}, many ^never properly published.",
                           "[d:aside][act:wry, gentle amazement]One famous Jerusalem dig was ^still being written up about ^fifty years after it ended."]),
        B("cost", 0, ["[d:build][k:THE CLAIM][act:laying out the claim, fairly]Some writers say a ^filter keeps ^inconvenient finds out of the textbooks. [sfx:shimmer][act:respectful, taking it seriously]It's a ^serious charge. [act:the real test, curious][tune:rise]So is there ^evidence finds were buried for what they said?"]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][sfx:hit][act:the answer, plain]What the record@noun shows is ^money and ^time. [act:first half, even][tune:level]^Digging gets funded. [act:the sting, dry][tune:fall]Years of ^writing up don't.",
                          "[d:build][act:explaining, sympathetic]Rescue digs before construction turn up ^more than the specialists can study. [act:quiet, a little sad]And excavators ^die with their ^notes."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A huge ^unpublished past? [act:the verdict, confident][tune:fall]^*Strong evidence*. [act:the second charge, fair][tune:rise]Finds hidden because they ^contradict history? [act:level-headed, patient][tune:fall]^*Awaiting evidence*.",
                     "[d:tension][p:0.93][act:playful wonder, a smile]The next great dig might be a ^basement."]),
    ]
    return EP("unpublished-finds", "13.06", "The Unpublished Past: Finds That Never Left the Storeroom", "unpublished-finds", "strong", "How much excavated evidence has never been published, and why?", "Hidden on *purpose*?", beats, shots,
              "Kletter & De-Groot 2001 · Israel Antiquities Authority, Favissa · Press 2020 · Maeir 2022 · Childs 2004 · Kersel 2015 · Cremo & Thompson 1993",
              "Half a million papyrus fragments, ten thousand rescue digs, one Jerusalem excavation written up fifty years late: why so much of the dug-up past never reaches print.",
              ["#Archaeology", "#History", "#Egypt", "#Papyrus", "#TheFiles"])


# ---------------------------------------------------------------- 13.08 The ledger
def _ledger_text():
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": page(200, 520, 600, 740, .1) +
          [{"k": "rect", "x": 250, "y": 520 + k * 110, "w": 500 - (k % 2) * 140, "h": 34, "fill": "#1a1511", "c": "none", "sw": 0, "in": .5 + k * .15} for k in range(1, 6)] +
          [{"k": "label", "x": 500, "y": 590, "t": "THE FILES", "st": "serif", "size": 44, "c": INK, "halo": False, "in": .3}, {"k": "cap", "x": 500, "y": 440, "t": "what was hidden, and what was only claimed", "in": .2}]}
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["MKUltra drugged unwitting people", "Tuskegee: forty years untreated", "Roswell's secret was a balloon project", "the Pentagon hid a UFO study"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Strong evidence", "#7fd1d4", ["a huge unpublished archaeological past"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["an alien craft at Roswell", "recovered craft today", "finds hidden for what they say"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["reliable psychic spies"])}
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE FILES][sfx:boom][act:the roll call, with relish]^Secret programmes, ^cover stories and ^shredded files. [act:inviting, a small smile]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:plain, sober]The CIA ^drugged people who ^didn't know. [act:grave, steady]Government doctors left sick men untreated for ^forty years. [act:lighter, a nod]Roswell hid a ^real secret. [act:plain, closing the set]The Pentagon hid a ^UFO study."]),
        B("collision", 2, ["[d:build][k:STRONG EVIDENCE][act:measured, confident]A ^huge share of what's been dug up has ^never been published. [d:aside][act:a quick aside, plain]Mostly for lack of ^money and ^time."]),
        B("cost", 3, ["[d:build][k:AWAITING EVIDENCE][act:naming them, even][tune:level]An alien craft at ^Roswell. [act:next one][tune:level]Recovered craft ^today. [act:the last, landing it][tune:fall]Finds ^buried for what they say. [d:aside][act:fair, careful]^Sworn words, no ^public evidence. [act:open door, a light touch][tune:fallrise]^Yet."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:firm, closing the file]Psychic spies you could ^rely on. [act:plain, final]The programme's ^own evaluation closed it."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:sincere, calm authority]Institutions really ^do hide things. [go:5|1.5][act:the principle, warm and even]That's exactly why we ask for evidence, from ^them and from their ^critics.",
                     "[d:tension][p:0.93][act:the house motto, quiet]^Coherence is the measure. [act:the last word, gentle]Not ^final demonstration."]),
    ]
    return EP("files-ledger", "13.08", "The Files · The Ledger", "", "mixed", "What institutions hid, and what they only claimed to hide.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 13",
              "The verdicts of The Files in one ledger: the secrets that are on the record, the one with strong evidence, the claims still awaiting evidence, and the one ruled out.",
              ["#History", "#CIA", "#UFO", "#TheFiles", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: six files in a cabinet, what was hidden and what was only claimed (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    folder = [{"k": "poly", "p": [[-150, -300], [-60, -300], [-40, -280], [150, -280], [150, -30], [-150, -30]], "fill": "#cdb58a", "c": "#8a6a48", "w": 1.5},
              {"k": "rect", "x": -120, "y": -250, "w": 150, "h": 14, "r": 2, "fill": "#e8dcc2", "c": "none", "sw": 0}] + \
             [{"k": "rect", "x": -120, "y": y, "w": w, "h": 14, "r": 2, "fill": "#15100c", "c": "none", "sw": 0} for y, w in ((-215, 230), (-185, 180), (-155, 240), (-125, 150), (-95, 210))] + \
             [{"k": "rect", "x": 60, "y": -86, "w": 30, "h": 50, "r": 6, "fill": "rgba(159,208,255,.35)", "c": "#9fd0ff", "sw": 2}, {"k": "rect", "x": 64, "y": -96, "w": 22, "h": 12, "r": 2, "fill": "#cbbca8", "c": "none", "sw": 0}]
    ticks = lambda op, c, i0=None: [dict({"k": "line", "p": [[-135 + 30 * (k % 10), -255 + 52 * (k // 10)], [-135 + 30 * (k % 10), -225 + 52 * (k // 10)]], "c": c, "w": 4, "op": op},
                                         **({"in": i0 + .03 * k, "keepop": True} if i0 is not None else {})) for k in range(40)]
    C = Cabinet([
        {"name": "MKUltra", "model": folder},
        {"name": "Tuskegee", "model": ticks(.22, "#cbbca8")},
        {"name": "Roswell", "model": mdl(roswell())},
        {"name": "The UFO study", "model": mdl(uap(), 0)},
        {"name": "Unpublished finds", "model": mdl(unpublished())},
        {"name": "Stargate", "model": mdl(stargate(), 0)},
    ])
    C.build()
    MK, TU, RO, UA, UN, SG = range(6)
    s1 = C.step(C.cam_cell(MK), C.verdict(MK, "established", "drugged, without consent", .4))
    s2 = C.step(C.cam_cell(TU), C.verdict(TU, "established", "forty years untreated", .2) + C.local(TU, ticks(1, "#ff8a7a", .5)))
    s3 = C.step(C.cam_cell(RO), C.verdict(RO, "established", "a real secret", .3))
    s4 = C.step(C.cam_cell(UA), C.verdict(UA, "established", "a hidden UFO study", .3))
    s5 = C.step(C.cam_cell(UN), C.verdict(UN, "strong", "never published", .3))
    s6 = C.step(C.cam_cell(UN), C.note(UN, "for lack of money and time", at=.2))
    s7 = C.step(C.cam_cell(RO), C.verdict(RO, "awaiting", "an alien craft?", .1))
    s8 = C.step(C.cam_cell(UA), C.verdict(UA, "awaiting", "craft, today?", .1))
    s9 = C.step(C.cam_cell(UN), C.verdict(UN, "awaiting", "buried for what they say?", .1, frame=False))
    s10 = C.step(C.cam_cells([RO, UA]), C.note(RO, "sworn words", at=.3, c=VCOL["awaiting"]) + C.note(UA, "no public evidence", at=.7, c=VCOL["awaiting"]))
    s11 = C.step(C.cam_cells([RO, UA]), C.question(RO, dx=C.w * .3, dy=-180, at=.05, size=70, c=VCOL["awaiting"]) + C.question(UA, dx=C.w * .3, dy=-180, at=.15, size=70, c=VCOL["awaiting"]), keep_notes=True)
    s12 = C.step(C.cam_cell(SG), C.verdict(SG, "ruled", at=.1) + C.struck(SG, "reliable psychic spies", at=.2))
    s13 = C.step(C.cam_cell(SG), C.note(SG, "closed by its own evaluation", at=.3, c="#ff8a7a"))
    s14 = C.step(C.cam_all(), [e for k, i in enumerate((MK, TU, RO, UA)) for e in C.wash(i, VCOL["established"], at=.2 + .15 * k, op=.12)])
    s15 = C.step(C.cam_all(), [e for i in range(6) for e in C.wash(i, VCOL["awaiting"], at=.2 + .1 * i, op=.08)])
    s16 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3, (0, 3): "%d|1.1" % s4}),
        2: (s5, {(0, 1): "%d|.3" % s6}),
        3: (s7, {(0, 1): "%d|1.1" % s8, (0, 2): "%d|1.1" % s9, (0, 3): "%d|1.1" % s10, (0, 4): "%d|.2" % s11}),
        4: (s12, {(0, 1): "%d|.3" % s13}),
        5: (s14, {(0, 1): "%d|.6" % s15, (1, 0): "%d|3" % s16}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def _mur():
    from mural import remix
    import illus
    return remix, illus


def tuskegee_m():
    """Tuskegee as one continuous take (see mural.py): six hundred men, twenty-nine years, a newspaper, and a signature."""
    remix, I = _mur()
    ep = tuskegee()
    men = [I.box(170 + 22 * (k % 30), 620 + 30 * (k // 30), 12, 22, I.AMBER if k < 399 else "#8a8378", r=6, at=round(.3 + .004 * k, 3)) for k in range(600)]
    told = [I.box(330, 1260, 340, 110, "rgba(18,13,10,.85)", I.LILAC, 3, 30, .3, style="claimed")] + [I.dot(430 + 70 * j, 1315, 10, I.LILAC, .6 + .15 * j) for j in range(3)] + [I.strike(320, 1380, 680, 1250, 1.4)]
    hook = {"base": "dark", "cam": [1, 500, 900], "els": men}
    perks = [I.box(120, 1250, 760, 150, "rgba(18,13,10,.82)", "#c9ad85", 2, 14, .1),
             I.oval(260, 1330, 60, 22, "#c9ad85", "none", 0, 1, 3.0), I.line([[230, 1290], [240, 1270]], 3.1, "#cbbca8", 3), I.line([[270, 1290], [280, 1266]], 3.2, "#cbbca8", 3),
             I.box(420, 1300, 150, 44, "#8a939c", r=14, at=3.8), I.dot(450, 1350, 14, "#3a3f45", 3.9), I.dot(540, 1350, 14, "#3a3f45", 3.9),
             I.dot(740, 1325, 34, "#e8c35a", 4.6), I.dot(740, 1325, 24, "#c9a86a", 4.6)]
    watch = [I.box(760, 560, 170, 220, "#e8dcc2", "#8a7a66", 2, 8, .3)] + [I.line([[785, 610 + 30 * j], [905, 610 + 30 * j]], .5 + .1 * j, I.INK, 2, "inferred", .3) for j in range(5)] + \
            [I.oval(640, 640, 60, 30, "none", I.BONE, 3, 1, .8), I.dot(640, 640, 12, I.BONE, 1.0)]
    X = lambda y: 150 + 700 * (y - 1943) / 29
    cure = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(180, 620, 70, 150, "rgba(159,208,255,.35)", I.BLUE, 3, 10, .2), I.box(190, 600, 50, 26, "#cbbca8", r=4, at=.2),
            I.label(215, 820, "1943", .3, I.BLUE, 32), I.strike(150, 800, 290, 590, 2.0)] +
            [I.line([[X(y), 1000], [X(y), 1060]], 3.4 + .1 * (y - 1943), I.AMBER, 4, draw=False) for y in range(1943, 1973)] +
            [I.label(X(1943), 1110, "1943", 3.4, I.BONE, 28), I.label(X(1972), 1110, "1972", 6.3, I.BONE, 28), I.label(500, 950, "29 years", 6.5, I.AMBER, 40, st="serif")]}
    paper = [I.box(140, 560, 330, 420, "#e8dcc2", "#8a7a66", 2, 4, 2.6, fx="pop"), I.box(165, 590, 280, 60, I.INK, r=3, at=2.9)] + \
            [I.line([[165, 690 + 28 * j], [445, 690 + 28 * j]], 3.0 + .05 * j, "#6a645c", 3, draw=False) for j in range(9)] + [I.label(305, 1030, "1972", 3.0, I.BONE, 30)]
    end = [I.box(560, 600, 300, 220, "#cdb58a", "#8a6a48", 2, 6, 5.0), I.box(610, 670, 200, 70, "none", I.RED, 4, 6, 5.6, fx="pop"), I.line([[630, 705], [790, 705]], 5.7, I.RED, 6)]
    apology = [I.box(420, 1150, 160, 120, "#5a4330", "#8a6a48", 2, 6, 8.2), I.person(500, 1150, 170, 8.0), I.label(500, 1320, "1997", 8.4, I.BONE, 30)]
    close = {"base": "dark", "cam": [1, 500, 900], "els": paper + end + apology}
    consent = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(260, 560, 480, 620, "#e8dcc2", "#8a7a66", 2, 6, 3.6)] +
               [I.line([[300, 620 + 40 * j], [700, 620 + 40 * j]], 3.8 + .05 * j, "#6a645c", 3, draw=False) for j in range(9)] +
               [I.line([[300, 1080], [700, 1080]], 4.2, I.INK, 2, draw=False),
                I.line([[320, 1070], [360, 1030], [390, 1075], [430, 1040], [470, 1070], [520, 1045], [560, 1066]], 5.2, I.INK, 4, dur=1.2, curve=True),
                I.line([[620, 1010], [650, 1050], [700, 980]], 6.6, I.GREEN, 7, dur=.5)]}
    return remix(ep, scenes={0: hook, 3: cure, 4: close, 5: consent}, alias={6: 0}, cams={6: [1.1, 500, 900]}, drop=("para", "num", "title", "q", "cap"),
                 line_adds={(0, 1): (told, None), (1, 1): (watch, None)}, beat_adds={1: (perks, None), 3: ([], [1.35, 500, 800])})


def uap_m():
    """UAP files as one continuous take (see mural.py): 144 reports, a witness who heard it from others, a hazing story, and an empty tray."""
    remix, I = _mur()
    ep = uap()
    short = lambda e: e.get("k") == "label" and len(e.get("t", "")) <= 20
    reports = {"base": "dark", "cam": [1, 500, 900], "els": [I.dot(270 + 42 * (k % 12), 640 + 42 * (k // 12), 12, "#6a645c", .3 + .01 * k) for k in range(144)] +
               [I.dot(270 + 42 * 11, 640 + 42 * 11, 14, I.GREEN, 3.2), I.glow(270 + 42 * 11, 640 + 42 * 11, 60, 3.2, .8)]}
    hearsay = [I.person(130 + 70 * k, 1300, 90, .3 + .2 * k, c="#8a8378") for k in range(3)] + \
              [I.arrow([[140 + 70 * k, 1200], [320, 1100], [440, 1000]], .5 + .2 * k, I.LILAC, 2, "claimed", .8) for k in range(3)] + \
              [I.box(730, 1060, 150, 240, "#3a2f25", "#8a6a48", 3, 4, 3.0), I.ring(805, 1165, 18, 3.4, I.RED, 4), I.strike(720, 1310, 890, 1050, 3.8)]
    cases = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(150 + 14 * (k % 25), 1140 - 10 * (k // 25), 12, 8, "#cdb58a", r=1, at=.2 + .01 * k) for k in range(200)] +
             [I.label(330, 880, "2,000+", 2.2, I.BONE, 44, st="serif"), I.ring(700, 760, 90, 3.6, I.BLUE, 5), I.line([[764, 824], [840, 900]], 3.8, I.BLUE, 10),
              I.label(700, 790, "0", 4.6, I.BLUE, 80, st="big", fx="pop")] +
             [I.person(560 + 80 * k, 1300, 120, 9.0 + .2 * k) for k in range(3)] +
             [I.box(560, 1040, 260, 110, "rgba(18,13,10,.85)", I.LILAC, 2.5, 40, 10.0, style="claimed"), I.oval(690, 1095, 60, 16, "none", I.LILAC, 3, 1, 10.3, style="claimed"),
              I.oval(690, 1085, 26, 12, "none", I.LILAC, 3, 1, 10.3, style="claimed")]}
    venn = {"base": "dark", "cam": [1, 500, 900], "els": [I.oval(380, 880, 230, 230, "rgba(159,208,255,.12)", I.BLUE, 3, 1, 3.0), I.label(380, 890, "unexplained", 3.2, I.BLUE, 34),
            I.oval(780, 880, 110, 110, "none", I.LILAC, 3, 1, 5.0, style="claimed"), I.label(780, 890, "alien", 5.2, I.LILAC, 30), I.label(640, 900, "≠", 5.8, I.BONE, 80, st="big")]}
    tray = {"base": "dark", "floor": 1150, "cam": [1, 500, 900], "els": [I.glow(500, 800, 360, .2, .5), I.line([[500, 380], [300, 1050]], .2, "#ffe9c8", 2, draw=False, op=.2), I.line([[500, 380], [700, 1050]], .2, "#ffe9c8", 2, draw=False, op=.2),
            I.box(250, 1050, 500, 60, "#8a939c", "#cbd2d8", 2, 6, .4), I.box(330, 990, 340, 60, "none", I.LILAC, 3, 8, 1.0, style="claimed")] + I.question(500, 960, 1.6, 80)}
    return remix(ep, scenes={1: reports, 3: cases, 5: venn, 6: tray}, cams={0: [1.1, 500, 880], 4: [1.3, 500, 800]}, keep=short,
                 drop=("para", "num", "title", "q", "cap", "label"), line_adds={(2, 1): (hearsay, None)})


def stargate_m():
    """Stargate as one continuous take (see mural.py): a mind aimed at a far target, five code names, a split review, a foggy report."""
    remix, I = _mur()
    ep = stargate()
    short = lambda e: e.get("k") == "label" and len(e.get("t", "")) <= 32
    X = lambda y: 170 + 660 * (y - 1972) / 23
    mind = {"base": "dark", "cam": [1, 500, 900], "els": [I.person(220, 1020, 200, .2), I.glow(220, 860, 90, .5, .6),
            I.line([[260, 850], [480, 760], [700, 690]], .9, I.LILAC, 3, "claimed", 1.4), I.box(700, 600, 140, 120, "none", "#8a8378", 3, 4, 1.8),
            I.line([[700, 600], [770, 540], [840, 600]], 1.9, "#8a8378", 3)] +
           [I.line([[X(y), 1150], [X(y), 1200]], 3.0 + .08 * (y - 1972), I.AMBER, 4, draw=False) for y in range(1972, 1996)] +
           [I.label(X(1972), 1250, "1972", 3.0, I.BONE, 28), I.label(X(1995), 1250, "1995", 4.8, I.BONE, 28)]}
    files = [I.box(640 + 12 * k, 520 - 10 * k, 180, 130, "#cdb58a", "#8a6a48", 2, 6, .2 + .15 * k) for k in range(4)] + I.question(780, 470, 1.4, 70)
    names = ["GONDOLA WISH", "GRILL FLAME", "CENTER LANE", "SUN STREAK", "STAR GATE"]
    code = {"base": "dark", "cam": [1, 500, 900], "els": sum([[I.box(230, 560 + 150 * k, 540, 110, "#cdb58a", "#8a6a48", 2, 6, 4.4 + 1.1 * k), I.box(230, 540 + 150 * k, 160, 30, "#cdb58a", r=6, at=4.4 + 1.1 * k),
                                                             I.label(500, 628 + 150 * k, n, 4.6 + 1.1 * k, I.INK, 40, st="big")] for k, n in enumerate(names)], [])}
    crane = [I.line([[640, 1260], [640, 900], [880, 900]], .3, I.AMBER, 6, dur=1.0), I.line([[860, 900], [860, 1010]], 1.1, I.AMBER, 3), I.line([[640, 960], [740, 900]], 1.0, I.AMBER, 4),
             I.arrow([[420, 1000], [520, 980], [620, 960]], 1.4, I.LILAC, 3, "claimed", .8)]
    split = {"base": "dark", "cam": [1, 500, 900], "els": [I.line([[500, 560], [500, 1300]], .3, "#6a645c", 2, "inferred", 1.0),
             I.person(280, 1000, 200, .9), I.box(170, 580, 220, 150, "none", I.GREEN, 3, 6, 1.6)] + [I.box(190 + 45 * j, 710 - 30 * (j + 1), 30, 30 * (j + 1), I.GREEN, r=3, at=1.8 + .1 * j) for j in range(4)] +
            [I.person(720, 1000, 200, 3.0), I.box(660, 600, 120, 120, "none", I.AMBER, 3, 60, 3.6), I.line([[700, 630], [700, 690]], 3.7, I.AMBER, 8), I.line([[740, 630], [740, 690]], 3.7, I.AMBER, 8)]}
    clues = [I.box(330, 1080, 340, 290, "#e8dcc2", "#8a7a66", 2, 4, .2)] + [I.line([[355, 1110 + 30 * j], [645, 1110 + 30 * j]], .3 + .04 * j, "#6a645c", 3, draw=False) for j in range(8)] + \
            [I.box(420, 1162, 90, 16, I.AMBER, r=3, at=1.6, op=.7), I.box(520, 1252, 110, 16, I.AMBER, r=3, at=2.0, op=.7), I.ring(600, 1250, 50, 2.4, I.BONE, 4)]
    fog = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(300, 560, 400, 520, "#e8dcc2", "#8a7a66", 2, 4, .3)] +
           [I.line([[330, 620 + 34 * j], [670, 620 + 34 * j]], .5 + .05 * j, "#6a645c", 3, draw=False) for j in range(12)] +
           [I.glow(500, 820, 260, 2.4, .9, "scan"), I.oval(500, 820, 220, 120, "#cbd2d8", "none", 0, .55, 2.6), I.label(500, 1130, "1995", .6, I.BONE, 30),
            I.person(400, 1350, 110, 6.0), I.person(500, 1350, 110, 6.2), I.person(600, 1350, 110, 6.4)]}
    return remix(ep, scenes={2: mind, 3: code, 4: fog, 5: split}, cams={0: [1.1, 500, 880], 6: [1.3, 500, 800]}, keep=short,
                 drop=("para", "num", "title", "q", "cap", "label"), line_adds={(0, 1): (files, None), (2, 1): (crane, None), (3, 1): (clues, None)})


def unpublished_m():
    """The storerooms as one continuous take (see mural.py): half a million fragments, ten thousand digs, and the money and time behind them."""
    remix, I = _mur()
    ep = unpublished()
    frag = [I.box(185 + 21 * (k % 30), 560 + 21 * (k // 30), 16, 16, "#b9ab94", r=2, at=round(.2 + .002 * k, 3), op=.55) for k in range(900)]
    pub = [I.box(185 + 21 * (k % 30), 560 + 21 * (k // 30), 16, 16, I.AU, r=2, at=5.4 + .1 * j, fx="pop") for j, k in enumerate((31, 212, 377, 455, 610, 702, 818, 861, 95, 540))]
    papyri = {"base": "dark", "cam": [1, 500, 900], "els": frag + pub}
    digs = [I.box(140 + 36 * (k % 20), 560 + 36 * (k // 20), 26, 26, "#5a4330", "#8a6a48", 1, 3, round(.3 + .01 * k, 3)) for k in range(300)]
    digs += [I.box(140 + 36 * (k % 20) + 6, 560 + 36 * (k // 20) + 6, 14, 14, I.BONE, r=2, at=4.0 + .05 * j) for j, k in enumerate((7, 44, 101, 160, 233, 287))]
    X = lambda y: 170 + 660 * (y - 1967) / 50
    fifty = [I.line([[X(1967), 1300], [X(2017), 1300]], 6.0, I.AMBER, 6, dur=2.0), I.label(X(1967), 1350, "dig ends", 6.0, I.BONE, 26), I.label(X(2017), 1350, "written up", 8.0, I.BONE, 26),
             I.label(500, 1260, "50 years", 7.0, I.AMBER, 36, st="serif")]
    backlog = {"base": "dark", "cam": [1, 500, 920], "els": digs + fifty}
    funnel = [{"k": "poly", "p": [[330, 560], [670, 560], [540, 760], [540, 900], [460, 900], [460, 760]], "fill": "none", "c": I.LILAC, "w": 3, "style": "claimed", "in": 1.0}] + I.question(500, 540, 5.2, 70)
    why = {"base": "dark", "floor": 1300, "cam": [1, 500, 900], "els":
           [I.box(170, 1300 - 18 * k, 90, 16, "#e8c35a", "#b8942a", 1, 8, 2.0 + .06 * k) for k in range(18)] + [I.label(215, 1350, "digging", 2.0, I.BONE, 28)] +
           [I.box(320, 1300 - 18 * k, 90, 16, "#e8c35a", "#b8942a", 1, 8, 3.2 + .1 * k) for k in range(3)] + [I.label(365, 1350, "writing up", 3.2, I.BONE, 28)] +
           [I.box(520, 1180, 170, 90, "#c9a86a", "#8a6a48", 2, 6, 6.0), I.dot(550, 1285, 16, "#3a3f45", 6.0), I.dot(660, 1285, 16, "#3a3f45", 6.0),
            I.line([[690, 1210], [770, 1150], [800, 1190]], 6.1, "#c9a86a", 6, draw=False)] +
           [I.dot(760 + 26 * (k % 5), 1280 - 22 * (k // 5), 10, "#b9ab94", 6.8 + .06 * k) for k in range(20)] +
           [I.person(600 + 60 * k, 900, 100, 8.0 + .2 * k, c="#8a8378") for k in range(2)] +
           [I.box(300 + 30 * k, 700 - 8 * k, 120, 20, "#cdb58a", "#8a6a48", 1, 3, 10.5 + .1 * k) for k in range(4)] + [I.box(290, 640, 180, 110, "#120d0a", r=6, at=12.0, op=.6, dur=1.5)]}
    return remix(ep, scenes={2: papyri, 3: backlog, 4: why}, alias={5: 0, 6: 0}, cams={0: [1.2, 500, 960], 6: [1.25, 500, 980]},
                 drop=("para", "num", "title", "q", "cap"), beat_adds={3: (funnel, [1.1, 500, 900])})


def roswell_m():
    """Roswell as one continuous take (see mural.py): a saucer in the headline, debris on the ground, memory copied and recopied, a train of balloons, four answers, and a cover lifted."""
    import copy
    remix, I = _mur()
    ep = roswell()
    saucer = lambda x, y, s, at, c=I.LILAC: [{"k": "poly", "p": I.ellipse(x, y, 150 * s, 30 * s)[:-1], "fill": "rgba(201,193,238,.10)", "c": c, "w": 3, "curve": True, "style": "claimed", "in": at, "fx": "draw", "dur": .8},
                                              {"k": "poly", "p": I.ellipse(x, y - 18 * s, 62 * s, 44 * s, a0=180, a1=360), "fill": "rgba(201,193,238,.10)", "c": c, "w": 3, "curve": True, "style": "claimed", "in": at + .3, "fx": "draw", "dur": .6}]
    balloon = lambda x, y, r, at: [I.line([[x, y + r], [x, y + r + 2.2 * r]], at + .2, "#cbbca8", 2, dur=.5), I.oval(x, y, r, r * 1.12, "#efe6d2", "#ffffff", 2, 1, at, fx="rise"),
                                   I.box(x - r * .22, y + r * 3.2, r * .44, r * .3, "#a8865e", r=2, at=at + .5)]
    hook = saucer(330, 400, 1, 2.2) + [I.glow(330, 400, 140, 2.2, .45)]
    back = [I.strike(505, 755, 845, 785, .6, I.RED, 7), I.strike(170, 470, 490, 330, 1.0, I.RED, 6)] + balloon(740, 340, 60, 1.6) + [I.glow(740, 340, 110, 1.6, .5, "lamp")] + I.question(880, 520, 3.4, 70)
    # the map: debris scattered on the ranch, carried to the base
    v = View(-113, -100, 28.5, 38, (40, 330, 920, 900))
    db, rw = v.p(-105.3, 33.95), v.p(-104.52, 33.39)
    debris = [I.dot(x, y, 5, "#efe6d2", round(1.4 + .05 * k, 2)) for k, (x, y) in enumerate(I.scatter(22, db[0] - 60, db[0] + 60, db[1] - 36, db[1] + 36, 4))] + \
             [I.arrow([[db[0] + 16, db[1] + 12], [rw[0] - 12, rw[1] - 10]], 3.0, I.AMBER, 4, dur=1.0, curve=False)]
    # what the rancher described, laid out on the ground; no engine, no metal; a kite
    G = 1250
    lay = [I.line([[80, G], [920, G]], .1, "#8c7152", 3, draw=False), I.box(80, G, 840, 100, "#3a2f24", r=0, at=.1)]
    lay += [I.line([[130, G - 20 - 18 * j], [170, G - 40 - 18 * j], [210, G - 22 - 18 * j], [250, G - 42 - 18 * j], [290, G - 24 - 18 * j]], 1.3 + .1 * j, "#6a6560", 9, dur=.4, curve=True) for j in range(3)] + \
           [I.label(210, G + 60, "rubber", 1.4, I.BONE, 30)]
    lay += [{"k": "poly", "p": [[330, G - 10], [350, G - 70], [390, G - 54], [420, G - 92], [460, G - 60], [480, G - 14], [440, G - 28], [400, G - 6]], "fill": "#c9ccd2", "c": "#ffffff", "w": 2, "in": 1.8, "fx": "pop"},
            I.line([[360, G - 40], [400, G - 50], [440, G - 36]], 1.9, "#ffffff", 2, draw=False), I.label(405, G + 60, "foil", 1.9, I.BONE, 30)]
    lay += [{"k": "poly", "p": [[520, G - 8], [540, G - 92], [660, G - 78], [650, G - 2]], "fill": "#e8dcc2", "c": "#8a7a66", "w": 2, "in": 2.5, "fx": "pop"}, I.label(590, G + 60, "paper", 2.6, I.BONE, 30)]
    lay += [I.line([[700 + 14 * j, G - 6 - 10 * j], [880 - 10 * j, G - 60 + 14 * j]], 3.0 + .1 * j, "#a8865e", 6, draw=False) for j in range(3)] + [I.label(790, G + 60, "sticks", 3.2, I.BONE, 30)]
    gear = [I.ring(320, 560, 80, 3.5, I.LILAC, 4, "claimed")] + [I.box(round(320 + 92 * math.cos(a) - 12, 1), round(560 + 92 * math.sin(a) - 12, 1), 24, 24, I.LILAC, r=3, at=3.6, op=.6)
                                                                  for a in [k * math.pi / 4 for k in range(8)]] + [I.ring(320, 560, 28, 3.6, I.LILAC, 4, "claimed"), I.strike(210, 670, 430, 450, 3.9, I.RED, 7),
                                                                  I.label(320, 720, "engine", 3.7, I.LILAC, 28)]
    nut = [{"k": "poly", "p": [[round(680 + 70 * math.cos(math.pi / 3 * k), 1), round(560 + 70 * math.sin(math.pi / 3 * k), 1)] for k in range(6)], "fill": "rgba(201,193,238,.12)", "c": I.LILAC, "w": 4, "style": "claimed", "in": 4.1},
           I.ring(680, 560, 26, 4.2, I.LILAC, 4, "claimed"), I.strike(580, 660, 780, 460, 4.4, I.RED, 7), I.label(680, 720, "metal", 4.2, I.LILAC, 28)]
    kite = [{"k": "poly", "p": [[500, 820], [590, 940], [500, 1100], [410, 940]], "fill": "rgba(232,220,194,.35)", "c": "#e8dcc2", "w": 3, "in": 4.7, "fx": "pop"},
            I.line([[500, 820], [500, 1100]], 4.9, "#a8865e", 4, dur=.4), I.line([[410, 940], [590, 940]], 5.0, "#a8865e", 4, dur=.4),
            I.line([[500, 1100], [470, 1140], [530, 1170], [480, 1200]], 5.2, "#c9ccd2", 3, dur=.5, curve=True)]
    ground = {"base": "dark", "cam": [1, 500, 900], "els": lay + gear + nut + kite}
    # memory: 1947, 1978, then hundreds of interviews; a photocopy of a photocopy
    X = lambda y: round(110 + 780 * (y - 1940) / 60, 1)
    mem = [I.line([[90, 1000], [910, 1000]], .1, "#cbbca8", 3, dur=1.0), I.dot(X(1947), 1000, 14, I.AU, .3), I.label(X(1947), 1060, "1947", .4, I.AU, 32),
           I.arrow([[X(1947), 960], [(X(1947) + X(1978)) / 2, 900], [X(1978) - 10, 960]], 1.0, I.AMBER, 3, dur=1.0), I.label((X(1947) + X(1978)) / 2, 870, "31 years", 1.3, I.AMBER, 32),
           I.person(X(1978), 1000, 150, 1.8), I.label(X(1978), 1060, "1978", 1.9, I.BONE, 32),
           {"k": "poly", "p": [[X(1978) + 30, 820], [X(1978) + 170, 820], [X(1978) + 170, 900], [X(1978) + 70, 900], [X(1978) + 45, 930], [X(1978) + 50, 900], [X(1978) + 30, 900]], "fill": "#e8dcc2", "c": "none", "w": 0, "in": 2.4, "fx": "pop"},
           I.label(X(1978) + 100, 875, "a cover", 2.5, I.INK, 28, halo=False)]
    mem += [I.box(x - 11, y - 8, 22, 16, "#e8dcc2", r=5, at=round(3.4 + .02 * k, 2), op=.8) for k, (x, y) in enumerate(I.scatter(90, 460, 900, 460, 760, 11))]
    gap = [I.line([[X(1947), 1110], [X(1977), 1110]], .3, I.AMBER, 4, dur=.6), I.line([[X(1977), 1110], [X(1997), 1110]], .8, I.AMBER, 4, "inferred", .6),
           I.label((X(1947) + X(1997)) / 2, 1160, "30 to 50 years later", 1.0, I.AMBER, 30)]
    for k in range(4):
        x = 150 + 190 * k
        gap += [I.box(x, 1220, 130, 170, "#e8dcc2", "#8a7a66", 2, 4, 2.4 + .5 * k, op=1 - .18 * k),
                I.line([[x + 20, 1290], [x + 65, 1265], [x + 110, 1290]], 2.5 + .5 * k, I.INK, 5 - k, draw=False, op=1 - .22 * k),
                I.oval(x + 65, 1300, 40 - 4 * k, 10, "none", I.INK, max(1, 4 - k), 1 - .22 * k, 2.5 + .5 * k)]
        gap += [I.dot(px, py, 2.5, "#3a3530", 2.6 + .5 * k, op=.8) for px, py in I.scatter(10 * k, x + 8, x + 122, 1230, 1380, 20 + k)]
        if k:
            gap += [I.arrow([[x - 50, 1305], [x - 10, 1305]], 2.3 + .5 * k, "#cbbca8", 3, dur=.3, curve=False)]
    memory = {"base": "dark", "cam": [1, 500, 900], "els": mem}
    # Mogul: listening for a faraway test; reflectors of foil, paper and sticks
    boom = [{"k": "fan", "x": 900, "y": 1330, "a0": 196, "a1": 246, "r": 520, "n": 9, "c": "#9fd0ff", "in": 3.2}, I.glow(900, 1330, 80, 3.0, .8, "red")]
    secret = [I.box(600, 420, 300, 90, "none", I.RED, 5, 10, .4, fx="pop"), I.label(750, 480, "TOP SECRET", .5, I.RED, 34), I.strike(600, 520, 900, 410, 1.6, I.LILAC, 4)]
    # four answers, then the records
    card = lambda x, y, at: I.box(x - 160, y - 150, 320, 300, "rgba(18,13,10,.6)", "#8a7a66", 2, 14, at)
    four = [card(300, 560, .2), card(700, 560, .3), card(300, 930, .4), card(700, 930, .5)]
    four += saucer(300, 560, .8, 1.0) + [I.label(300, 680, "1947: a disc", 1.2, I.BONE, 28)]
    four += [I.arrow([[470, 560], [530, 560]], 1.8, "#cbbca8", 3, dur=.3, curve=False)] + balloon(700, 500, 44, 2.0) + [I.label(700, 680, "1947: a balloon", 2.2, I.BONE, 28)]
    four += [I.arrow([[560, 690], [440, 790]], 2.8, "#cbbca8", 3, dur=.3, curve=False), I.line([[300, 810], [300, 1030]], 3.0, "#cbbca8", 2, dur=.6)] + \
            [I.oval(300, 820 + 34 * k, 16, 18, "#efe6d2", "none", 0, 1, 3.0 + .1 * k) for k in range(3)] + \
            [{"k": "poly", "p": [[300, 935], [322, 960], [300, 985], [278, 960]], "fill": "#c9ccd2", "c": "#ffffff", "w": 1.5, "in": 3.4, "fx": "pop"},
             I.label(300, 1050, "1994: Mogul", 3.5, I.BONE, 28)]
    four += [I.arrow([[470, 930], [530, 930]], 4.2, "#cbbca8", 3, dur=.3, curve=False),
             I.line([[640, 860], [700, 800], [760, 860]], 4.4, "#cbbca8", 3, dur=.4, curve=True), I.line([[640, 860], [700, 900]], 4.5, "#cbbca8", 1.5, draw=False),
             I.line([[760, 860], [700, 900]], 4.5, "#cbbca8", 1.5, draw=False), I.person(700, 1010, 110, 4.6, c="#9aa0a8"), I.label(700, 1050, "1997: dummies", 4.8, I.BONE, 28)]
    XA = lambda y: round(560 + 300 * (y - 1945) / 15, 1)
    four += [I.line([[540, 1150], [880, 1150]], 5.4, "#cbbca8", 2, dur=.6), I.dot(XA(1947), 1150, 10, I.AU, 5.6), I.label(XA(1947), 1200, "1947", 5.6, I.AU, 26),
             I.box(XA(1953), 1138, XA(1959) - XA(1953), 24, I.LILAC, r=4, at=6.2, fx="pop"), I.label((XA(1953) + XA(1959)) / 2, 1200, "1950s drops", 6.4, I.LILAC, 26),
             I.arrow([[700, 1080], [(XA(1953) + XA(1959)) / 2, 1130]], 6.6, I.LILAC, 3, dur=.4)]
    answers = {"base": "dark", "cam": [1, 500, 900], "els": four}
    files = [I.box(150 + 14 * k, 1250 - 26 * k, 240, 40, "#cdb58a", "#8a6a48", 2, 4, .2 + .1 * k) for k in range(4)] + \
            [I.glow(280, 1260, 140, 1.4, .95, "red"), I.glow(250, 1210, 90, 1.6, .9, "red"), I.label(270, 1360, "records destroyed", 1.8, I.RED, 28)] + I.question(470, 1300, 3.0, 64)
    # the verdict: an empty evidence table, then the cover lifted off a balloon
    tray = lambda x, at, lab: [I.box(x - 110, 640, 220, 200, "none", "#cbbca8", 3, 10, at, style="inferred"), I.label(x, 890, lab, at + .2, "#cbbca8", 28)]
    verdict = {"base": "dark", "cam": [1, 500, 900], "els": saucer(500, 450, 1.1, .3) + [I.glow(500, 450, 160, .3, .4)] +
               tray(220, 3.2, "piece") + tray(500, 3.6, "photo") + tray(780, 4.0, "document") +
               [I.label(500, 945, "nothing from 1947", 4.6, I.LILAC, 32)]}
    cover = [{"k": "poly", "p": [[260, 1410], [300, 1250], [420, 1185], [580, 1185], [700, 1250], [740, 1410]], "fill": "#4a4440", "c": "#8a8378", "w": 2, "in": .3, "fx": "rise"}] + \
            balloon(500, 1070, 56, 2.6) + [I.glow(500, 1070, 130, 2.6, .6, "lamp")]
    mog = copy.deepcopy(ep["shots"][2])
    for it in mog["els"][-1]["items"]:
        if str(it.get("text", "")).startswith("schematic"):
            it.update(text="schematic: real trains were far taller", x=3, z=0, a="start")
    return remix(ep, scenes={2: mog, 3: ground, 4: answers, 5: memory, 6: verdict}, cams={0: [1, 500, 860], 1: [1.9, 560, 790]},
                 drop=("para", "num", "title", "q", "cap"), adds={0: hook, 1: debris, 2: boom},
                 line_adds={(0, 1): (back, None), (2, 1): (gap, None), (3, 1): (secret, None), (4, 1): (files, None), (5, 1): (cover, None)})


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/files-ledger.json)."""
    import recap
    return recap.recap(ledger, "files-ledger", None)


def EPISODES():
    import lg_d      # 13.01 rebuilt from the legacy film
    return [lg_d.mkultra_m(), tuskegee_m(), stargate_m(), roswell_m(), uap_m(), unpublished_m(), ledger_recap()]
