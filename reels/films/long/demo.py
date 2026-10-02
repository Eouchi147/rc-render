"""Long-form engine demo (16:9): a 75 to 90 second landscape film that exercises every part of the long-form engine.

An intro title, two chapters (each opens on its drawn chapter card), eight scenes on one wall: a sky with the opening image,
a map, a timeline, a cross-section, an isometric model, a chart that builds, a 9:16 scene reused from the Short "capsian"
(f15.py, its map) shown through a window of a 16:9 panel (inset with s/crop), and a night sea for the verdict.
Facts: only those of the Short "capsian" (its narration films/rewrite/capsian.json, its labels and sources).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_engine && cp ../episodes/files.json /tmp/claude-0/sbx_engine/
  RC_FILMS_OUT=/tmp/claude-0/sbx_engine RC_FILMS_EPS=/tmp/claude-0/sbx_engine/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_engine/boards python3 films.py long.demo
"""
import copy, math, random
from films import View
from mural import remix, inset
from illus import person, arrow, line, glow, label, dot, box, oval, BONE, AMBER, BLUE, SEA

GOLD, SCAN = "#f2c98e", "#9fd0ff"
W_, H_ = 1778, 1000          # the 16:9 frame; keep drawings in x 80..1700, y 120..800 (captions below 807, HUD above 110)


def sky_hook():
    """The opening image: a shell mound on the steppe at dusk, fires, people; an arrow off towards the sea."""
    mound = [[520, 642], [660, 560], [820, 500], [1000, 478], [1180, 496], [1340, 556], [1500, 642]]
    r = random.Random(4)
    shells = []
    for k in range(60):
        x = r.uniform(690, 1310); top = min(600, 478 + abs(x - 1000) ** 1.6 * .016 + 24)
        shells.append(dot(round(x, 1), round(r.uniform(top, 628), 1), 4.5, "#efe6d2", round(.9 + .02 * k, 2), op=.85))
    return {"base": "sky", "tod": "dusk", "ground": 642, "sun": [330, 470, 30], "cam": [1, 889, 500], "els": [
        {"k": "poly", "p": mound, "fill": "#4d3b2a", "c": "rgba(255,226,190,.35)", "w": 1.4, "curve": True, "in": .1, "dur": 1.0}] + shells + [
        glow(780, 630, 90, 1.4, .75, "fire"), glow(1250, 630, 76, 1.7, .65, "fire"),
        person(720, 642, 84, 2.0), person(764, 642, 76, 2.2), person(1300, 642, 80, 2.4),
        glow(1560, 260, 110, 7.4, .5, "lamp"),
        arrow([[1000, 470], [1250, 330], [1540, 262]], 7.0, BLUE, 3, "claimed", 1.4),
        label(1560, 210, "across the sea?", 8.0, BLUE, 32, "end")]}


def range_map():
    """Where the Capsians lived: inland Tunisia and eastern Algeria (the outline is schematic)."""
    v = View(-1.5, 19.5, 30.6, 39.4, (90, 120, 1600, 680))
    rng = [(5.9, 34.7), (6.9, 35.7), (8.4, 36.1), (10.1, 35.8), (10.5, 34.7), (9.6, 33.7), (7.6, 33.6), (6.3, 34.0)]
    gx, gy = v.p(8.784, 34.425)
    sx, sy = v.p(13.9, 37.55)
    return {"base": "map", "cam": [1, 889, 500], "els": [
        {"k": "map", "land": v.land(), "in": -1},
        {"k": "poly", "p": [v.p(lo, la) for lo, la in rng], "fill": "rgba(232,184,122,.16)", "c": AMBER, "w": 2.4, "style": "inferred", "curve": True, "in": 2.4, "dur": 1.0},
        {"k": "pin", "x": gx, "y": gy, "t": "Gafsa, ancient Capsa", "c": GOLD, "in": .5},
        label(v.p(8.2, 33.0)[0], v.p(8.2, 33.0)[1], "inland Tunisia and Algeria", 3.0, AMBER, 28),
        label(sx, sy, "Sicily", 1.0, "#cbbca8", 26),
        {"k": "scale", "x": 140, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": 1.2}]}


def timeline():
    """About 11,000 to 7,500 years ago: the band builds on an axis of years ago."""
    X = lambda ya: round(200 + (12000 - ya) / 6000 * 1380, 1)
    ticks = [[X(12000), "12,000"], [X(10000), "10,000"], [X(8000), "8,000"], [X(6000), "6,000"]]
    return {"base": "dark", "stars": 60, "cam": [1, 889, 500], "els": [
        {"k": "axis", "x0": 200, "x1": 1580, "y": 520, "ticks": ticks, "t": "years ago", "in": .1},
        {"k": "line", "p": [[X(11000), 470], [X(11000), 520]], "c": GOLD, "w": 2, "fx": "draw", "dur": .5, "in": .8},
        {"k": "line", "p": [[X(7500), 470], [X(7500), 520]], "c": GOLD, "w": 2, "fx": "draw", "dur": .5, "in": 2.6},
        {"k": "band", "x0": X(11000), "x1": X(7500), "y": 430, "h": 20, "c": GOLD, "t": "the Capsians", "tc": GOLD, "in": 1.4, "dur": 1.2},
        label(X(11000), 400, "about 11,000", 1.0, "#cbbca8", 24),
        label(X(7500), 400, "about 7,500", 2.8, "#cbbca8", 24)]}


def section():
    """A Capsian mound cut open: layer on layer, more than three metres deep (100 units = 1 m); a person and a room for scale."""
    layers = [{"d": 0, "c": "#6f5a44", "t": "ash and burnt stone"}, {"d": 70, "c": "#b9ab94", "t": "snail shells, flint tools, bone"},
              {"d": 150, "c": "#7a6248", "t": "hearths"}, {"d": 220, "c": "#a8977c", "t": "shells again"}, {"d": 310, "c": "#5a4632", "t": "older ground"}]
    return {"base": "section", "tod": "dusk", "ground": 300, "lx": 130, "layers": layers, "cam": [1, 889, 500], "els": [
        person(1000, 300, 170, .6),
        label(1000, 112, "a person, 1.7 m", 1.0, "#cbbca8", 24),
        {"k": "dim", "x1": 1600, "y1": 300, "x2": 1600, "y2": 610, "t": "more than 3 m", "c": GOLD, "fx": "draw", "dur": 1.2, "in": 2.4, "lx": 30},
        {"k": "rect", "x": 1250, "y": 300, "w": 230, "h": 250, "r": 4, "fill": "rgba(245,236,220,.06)", "c": BONE, "sw": 2, "style": "inferred", "in": 5.6},
        label(1365, 435, "a room,", 6.0, BONE, 24), label(1365, 467, "2.5 m tall", 6.0, BONE, 24)]}


def iso_cube():
    """One cubic metre, a box one metre on each side, beside a person (iso units: 10 = 1 m)."""
    items = [{"t": "slab", "x0": -24, "x1": 24, "z0": -24, "z1": 24, "y": 0, "c": "#3a2f24"},
             {"t": "box", "x": 0, "z": 0, "y": 0, "w": 10, "d": 10, "h": 10, "c": "#d8ccb4", "edge": "rgba(40,30,20,.55)"},
             {"t": "person", "x": 13, "y": 0, "z": 6, "h": 17, "color": "#d9c7a6"},
             {"t": "line", "p": [[-5, 0, 7], [5, 0, 7]], "c": GOLD, "w": 2},
             {"t": "label", "x": 0, "y": 0, "z": 9, "text": "1 m", "st": "small", "c": GOLD, "dy": 34}]
    return {"base": "dark", "stars": 80, "cam": [1, 889, 500], "els": [
        glow(889, 560, 480, 0, .18, "lamp"),
        {"k": "iso", "x": 889, "y": 640, "s": 15, "az": -28, "spin": 2.2, "el": .34, "items": items, "in": .1},
        label(889, 210, "one cubic metre", .8, AMBER, 30),
        glow(1120, 470, 120, 5.2, .45, "lamp"),
        label(1130, 380, "about 25,000 shells", 5.4, GOLD, 34, "start", st="lab", fx="pop")]}


def chart():
    """One snail a minute, non-stop: 25,000 minutes is about 17 days. The bar draws itself across the days."""
    x0, k = 260, 65                    # 65 units per day
    days = 25000 / 60 / 24             # 17.36
    x1 = round(x0 + days * k, 1)
    ax = [[round(x0 + d * k, 1), t] for d, t in ((0, "0"), (7, "1 week"), (14, "2 weeks"), (21, "3 weeks"))]
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": [
        label(x0, 250, "one snail a minute, non-stop", .2, AMBER, 30, "start"),
        {"k": "axis", "x0": x0, "x1": round(x0 + 21 * k, 1), "y": 560, "ticks": ax, "t": "days", "in": .3},
        {"k": "line", "p": [[x0, 470], [x1, 470]], "c": AMBER, "w": 54, "op": .9, "keepop": True, "fx": "draw", "dur": 3.2, "in": .8}] + [
        dot(round(x0 + (d + .5) * k, 1), 385, 9, GOLD, round(.8 + d * 3.2 / days, 2)) for d in range(17)] + [
        {"k": "line", "p": [[x1, 400], [x1, 545]], "c": BONE, "w": 2, "style": "inferred", "in": 4.0},
        label(x1 + 18, 362, "about 17 days", 4.2, BONE, 32, "start", st="lab")]}


def ancestry():
    """The 9:16 map of the Short "capsian" through a window, and beside it the forager's ancestry: 100 parts, almost 6 from Europe."""
    import f15
    m = copy.deepcopy(f15.capsian()["shots"][1])
    m["els"] = [e for e in m["els"] if not str(e.get("t", "")).startswith("Pantelleria")]   # obsidian is not part of this telling
    crop, at = [40, 380, 920, 900], [120, 100]
    s = round(680 / crop[3], 4)
    dj = next(e for e in m["els"] if e.get("t") == "Djebba")
    sc = next(e for e in m["els"] if e.get("t") == "Sicily")
    P = lambda x, y: [round(at[0] + (x - crop[0]) * s, 1), round(at[1] + (y - crop[1]) * s, 1)]
    gx, gy, pitch, sq = 1080, 150, 50, 42
    cells = []
    for k in range(100):
        cx, cy = gx + pitch * (k % 10), gy + pitch * (k // 10)
        blue = k >= 94
        cells.append(box(cx, cy, sq, sq, BLUE if blue else AMBER, r=5, at=round(4.6 + .25 * (k - 94), 2) if blue else round(.5 + .012 * k, 3),
                         op=None if blue else .55, fx="pop"))
    els = cells + [
        glow(*P(dj["x"], dj["y"]), 70, .4, .5, "lamp"),
        arrow([P(sc["x"], sc["y"]), [960, 430], [gx + 4 * pitch - 18, gy + 9 * pitch + 21]], 5.4, BLUE, 2.5, "claimed", 1.2),
        label(gx + 250, 690, "almost 6 in 100 from Europe", 5.8, BLUE, 28),
        label(gx + 250, 734, "probably by way of Sicily", 7.4, "#cbbca8", 24)]
    return inset(m, s=s, crop=crop, at=at, els=els, cam=[1, 889, 500])


def sea():
    """The verdict at night: two coasts, a route drawn in dots, one person on the shore, and the many still to come."""
    left = [[-60, 700], [-60, 548], [110, 532], [280, 566], [400, 628], [452, 700]]
    right = [[1340, 700], [1400, 618], [1500, 560], [1650, 532], [1840, 548], [1840, 700]]
    ghosts = [person(130 + 46 * k, 556 - k * 3, 54, round(10.2 + .25 * k, 2), "#c9c1ee") for k in range(5)]
    for g in ghosts:
        g.update(op=.4, keepop=True)
    r = random.Random(5)
    shells = [dot(round(r.uniform(300, 420), 1), round(r.uniform(600, 640), 1), 3.5, "#efe6d2", round(12.4 + .05 * k, 2)) for k in range(14)]
    return {"base": "sky", "tod": "night", "ground": 1200, "sun": False, "moon": [1460, 210, 30], "cam": [1, 889, 500], "els": [
        {"k": "water", "y": 630, "h": 500, "op": .9, "in": -1},
        {"k": "poly", "p": left, "fill": "#2b2328", "c": "rgba(255,226,190,.3)", "w": 1.2, "curve": True, "in": -1},
        {"k": "poly", "p": right, "fill": "#2b2328", "c": "rgba(255,226,190,.3)", "w": 1.2, "curve": True, "in": -1},
        label(220, 680, "Tunisia", .3, "#cbbca8", 26), label(1600, 680, "Sicily", .3, "#cbbca8", 26),
        {"k": "line", "p": [[450, 662], [900, 672], [1350, 662]], "c": AMBER, "w": 3, "style": "claimed", "curve": True, "fx": "draw", "dur": 1.6, "in": .8},
        {"k": "boat", "x": 900, "y": 640, "w": 120, "in": 1.6, "fx": "rise"},
        label(900, 560, "?", 2.6, "#c9c1ee", 70, st="big", fx="pop"),
        person(240, 540, 58, .2, "#e8d6b8"),
        glow(240, 512, 70, 6.6, .7, "lamp")] + ghosts + shells}


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


def demo():
    shots = [sky_hook(), range_map(), timeline(), section(), iso_cube(), chart(), ancestry(), sea()]
    beats = [
        B("hook", 0, ["[d:intrigue][sfx:boom][act:curious, a little playful]About eight thousand years ago, people in Tunisia, in North Africa, left behind whole ^hills of snail shells.",
                      "[d:tension][act:the twist, intrigued]And the DNA of one of them points to an ancestor from across the ^sea."]),
        B("title", 0, ["[d:calm][act:warm, setting out]Snails, ash, and a Sicilian ^ancestor."], intro=True),
        B("world", 1, ["[d:calm][act:plain, orienting]Archaeologists call these people the ^Capsians, after ^Capsa, the ancient name of the town of ^Gafsa. "
                       "[p:0.93][act:steady, explaining]They were foragers, living by hunting and gathering across inland Tunisia and ^Algeria."], chapter="The mounds"),
        B("world", 2, ["[act:steady]Their story runs from about eleven thousand to seven and a half thousand years ^ago."]),
        B("collision", 3, ["[d:build][act:vivid, a little amazed]Their camps grew into mounds of ash, burnt stone, tools and ^shells, some more than three metres ^deep: deeper than an ordinary room is ^tall."]),
        B("collision", 4, ["[p:0.93][gap:0.4][act:counting, amused]At one site, archaeologists counted the shells in a single cubic ^metre. [p:0.9][act:the punchline, savouring it]About twenty-five ^thousand.",
                           "[go:5][p:0.93][act:playful, doing the sum]Eat one snail a minute@time, non-stop, and that box alone would take you more than two ^weeks."]),
        B("reversal", 6, ["[d:reveal][act:the reveal, leaning in]Then, in {2025|twenty twenty-five}, came ancient ^DNA from a forager buried at ^Djebba, in northwest Tunisia. "
                          "[p:0.9][act:precise, delighted]Split his ancestry into a hundred ^parts, and almost ^six came from hunter-gatherers of ^Europe. [act:the clue, careful]Probably by way of ^Sicily."],
          chapter="The ancestor"),
        B("tag", 7, ["[d:verdict][p:0.95][act:weighing it, even][tune:rise]Stone Age sea contact between Tunisia and ^Sicily? [act:the verdict, measured][tune:fall]^*Plausible*. "
                     "[act:fair, a caveat]The signal is real, but it comes from ^one person.",
                     "[d:tension][p:0.93][act:inviting, warm]We need more ^genomes. [act:the last word, a smile][tune:fall]And perhaps a few more ^snails."]),
    ]
    ep = {"id": "lf-demo", "code": "LF.00", "series": "Long form", "title": "Snails, Ash and a Sicilian Ancestor", "case": "capsian",
          "verdict": "plausible", "claim": "Were Tunisia's Stone Age foragers cut off from Europe?", "mood": "mystery",
          "hook_text": "An ancestor from across the *sea*.", "beats": beats, "shots": shots,
          "sources": "Lipson et al. 2025 (doi:10.1038/s41586-025-08699-4) · Lubell 2004 (doi:10.4312/dp.31.1) · Rahmani 2004 (doi:10.1023/B:JOWO.0000038658.50738.eb)",
          "post": "Engine demo: a 16:9 long-form film on one wall.", "hashtags": ["#Tunisia", "#Prehistory"],
          "aspect": "16:9", "intro_title": "Snails, Ash and a Sicilian Ancestor",
          "yt_title": "Stone Age Tunisia: snail mounds and an ancestor from across the sea",
          "description": "Hills of snail shells in inland Tunisia, and one forager whose DNA points across the sea to Sicily.\n\nChapters\n{chapters}\n\nSources\nLipson et al. 2025, Nature, doi:10.1038/s41586-025-08699-4\nLubell 2004, Documenta Praehistorica, doi:10.4312/dp.31.1\nRahmani 2004, Journal of World Prehistory, doi:10.1023/B:JOWO.0000038658.50738.eb",
          "end_line": "One genome is a clue, not yet a pattern."}
    return remix(ep)


def EPISODES():
    return [demo()]
