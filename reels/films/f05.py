"""File 05 · Under Giza. The pyramids, the Sphinx and what lies beneath them."""
from films import like, View, Axis
from giza import Section, BASE, HEIGHT
import math


def corridor_view(cx, cy, W=700, H=560, n=8, tone=(214, 190, 150)):
    """One-point perspective down a stone corridor with a gabled roof, lamp-lit, seen through a round endoscope."""
    els = []
    def ring(t):
        k = 1 - t * .86; w, h = W * k / 2, H * k / 2
        return [[cx - w, cy + h], [cx - w, cy - h * .2], [cx, cy - h], [cx + w, cy - h * .2], [cx + w, cy + h]]
    rs = [ring(i / n) for i in range(n + 1)]
    for i in range(n):
        a, b = rs[i], rs[i + 1]; f = 1 - i / n
        for j, (p, q) in enumerate(((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))):
            lit = [.62, .9, .75, .5, .42][j]
            c = tuple(int(v * (.22 + .78 * f * f) * lit) for v in tone)
            els.append({"k": "poly", "p": [a[p], a[q], b[q], b[p]], "fill": "rgb(%d,%d,%d)" % c, "c": "rgba(40,28,18,.8)", "w": 1.2, "op": 1, "in": -1})
    far = rs[-1]
    els.append({"k": "poly", "p": far, "fill": "#0b0907", "c": "rgba(40,28,18,.8)", "w": 1, "in": -1})
    els.append({"k": "glow", "x": cx, "y": cy + 40, "r": 380, "kind": "lamp", "op": .35})
    els.append({"k": "circle", "x": cx, "y": cy, "r": 830, "c": "#0b0907", "w": 700, "op": 1})
    els.append({"k": "circle", "x": cx, "y": cy, "r": 482, "c": "rgba(255,226,168,.35)", "w": 2, "op": 1})
    return els

SERIES = "Under Giza"


def big_void():
    S = Section(s=3.6, cx=500, gy=1150)
    R = S.rooms()
    body = S.body()
    shade = {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "id": "shade"}
    inner = S.els()
    bv, bvc = S.big_void()
    nfc, nfcc = S.nfc()
    sky = {"base": "section", "tod": "night", "ground": 1150, "far": [[95, 220], [915, 110]], "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 60, "c": "#4d3e30", "t": "limestone bedrock", "tex": "blocks", "to": .12}]}
    gg_mid = S.P((R["gg0"][0] + R["gg1"][0]) / 2, (R["gg0"][1] + R["gg1"][1]) / 2 + 4)
    qc = S.P(R["qc"][0], R["qc"][1] + 2)
    kc = S.P(R["kc"][0], R["kc"][1] + 3)
    cam_in = [2.7, bvc[0] - 20, bvc[1] + 40]
    # 0 hook: the void, close
    s0 = dict(sky, cam=cam_in, els=[body, shade] + inner + [dict(bv, **{"in": .3, "fx": "fade"}),
         {"k": "glow", "x": bvc[0], "y": bvc[1], "r": 90, "kind": "blue", "pulse": True, "in": .2},
         {"k": "q", "x": bvc[0], "y": bvc[1] + 16, "size": 44, "in": .9, "fx": "pop"}])
    # 1 world: the whole pyramid
    s1 = dict(sky, cam=[1, 500, 900], els=[dict(body, **{"in": 0}), shade,
         {"k": "dim", "x1": 950, "y1": 1150, "x2": 950, "y2": S.P(0, HEIGHT)[1], "t": "146 m, as built", "in": .6, "lx": 26},
         {"k": "dim", "x1": S.P(0, 0)[0], "y1": 1196, "x2": S.P(BASE, 0)[0], "y2": 1196, "t": "230 m", "ly": 40, "in": .9},
         {"k": "cap", "x": 500, "y": 560, "t": "The Great Pyramid · Khufu", "in": .3, "id": "khufu"},
         {"k": "person", "x": 120, "y": 1150, "h": 6, "t": False}])
    # 2 the three known rooms
    s2 = like(s1, cam=[2.2, 520, 1020], drop=("dim",), add=[dict(e, **{"in": .2 + i * .08, "fx": "draw"}) for i, e in enumerate(inner)] + [
         {"k": "label", "x": kc[0] + 34, "y": kc[1] - 6, "t": "King's Chamber", "a": "start", "in": .8},
         {"k": "label", "x": qc[0] + 30, "y": qc[1] + 20, "t": "Queen's Chamber", "a": "start", "in": 1.1},
         {"k": "label", "x": gg_mid[0] - 20, "y": gg_mid[1] + 40, "t": "Grand Gallery", "a": "end", "in": 1.4}])
    s2["els"] = [e for e in s2["els"] if e.get("k") not in ("dim",)]
    # 3 muons raining through
    s2["els"] = [e for e in s2["els"] if e.get("id") != "khufu"]
    s3 = like(s2, cam=[1.05, 500, 860], drop=("khufu",), add=[{"k": "rays", "x0": 150, "x1": 850, "y0": 250, "y1": 1300, "n": 90, "spread": .35, "in": .1, "fx": "draw", "dur": 2.2},
         {"k": "cap", "x": 500, "y": 330, "t": "cosmic-ray muons", "c": "#9fd0ff", "in": .8}])
    # 4 detectors
    det = [{"k": "pin", "x": qc[0] - 5, "y": qc[1] + 6, "r": 5, "c": "#9fd0ff", "t": "nuclear emulsion · Nagoya", "a": "end", "lx": -30, "ly": 60, "st": "small", "in": .3},
           {"k": "pin", "x": qc[0] + 5, "y": qc[1] + 6, "r": 5, "c": "#9fd0ff", "t": "scintillators · KEK", "lx": 30, "ly": 60, "st": "small", "in": .7},
           {"k": "pin", "x": S.P(10, 1)[0] - 20, "y": 1146, "r": 6, "c": "#9fd0ff", "t": "gas detectors · CEA", "lx": 14, "ly": 36, "st": "small", "in": 1.1}]
    s4 = like(s3, cam=[2.1, 520, 1030], drop=(), add=det)
    s4["els"] = [e for e in s4["els"] if e.get("k") != "rays" and not (e.get("k") == "cap" and "muons" in e.get("t", ""))]
    # 5 the excess: tracks converge on the void
    tr = []
    x0, y0 = qc[0], qc[1] + 4
    base_a = math.atan2(bvc[1] - y0, bvc[0] - x0)
    for i in range(11):
        a = base_a + math.radians((i - 5) * 4.2)
        L = 300 if abs(i - 5) > 2 else 330
        tr.append({"k": "line", "p": [[x0, y0], [round(x0 + math.cos(a) * L, 1), round(y0 + math.sin(a) * L, 1)]], "c": "#9fd0ff", "w": 2.2 if abs(i - 5) <= 2 else 1.2, "op": .85 if abs(i - 5) <= 2 else .4, "in": .2 + i * .05, "fx": "draw"})
    s5 = like(s4, cam=[2.5, bvc[0] - 10, bvc[1] + 60], add=tr + [dict(bv, **{"in": 1.0}),
         {"k": "glow", "x": bvc[0], "y": bvc[1], "r": 110, "kind": "blue", "pulse": True, "in": 1.0},
         {"k": "label", "x": bvc[0] - 60, "y": bvc[1] - 44, "t": "the Big Void · 30 m +", "a": "middle", "c": "#cfe6ff", "in": 1.4}])
    # 6 the north face corridor
    s6 = like(s1, cam=[3.6, nfcc[0] + 40, nfcc[1] + 20], add=[dict(e, **{"in": -1}) for e in inner] + [dict(nfc, **{"in": .4, "fx": "draw"}),
         {"k": "glow", "x": nfcc[0], "y": nfcc[1], "r": 50, "kind": "blue", "in": .4},
         {"k": "label", "x": nfcc[0] + 10, "y": nfcc[1] - 30, "t": "North Face Corridor · 9 m", "c": "#cfe6ff", "in": 1.0},
         {"k": "line", "p": [S.P(17 / math.tan(math.radians(51.84)) - 1, 22.5), S.P(17 / math.tan(math.radians(51.84)) + 2, 26), S.P(17 / math.tan(math.radians(51.84)) + 5, 22.5)], "c": "#f2dcb4", "w": 2, "in": .2}])
    s6["els"] = [e for e in s6["els"] if e.get("k") not in ("dim",)]
    # 7 the camera's view down the corridor: gabled roof, empty
    s7 = {"base": "dark", "cam": [1, 500, 880], "els": corridor_view(500, 860) + [
          {"k": "cap", "x": 500, "y": 300, "t": "endoscope camera · March 2023", "in": .8},
          {"k": "label", "x": 500, "y": 345, "t": "empty, under a gabled roof", "st": "small", "in": 1.2}]}
    # 8 verdict: both spaces, one solid, one inferred
    s8 = like(s1, cam=[1.9, 470, 1010], add=[dict(e, **{"in": -1}) for e in inner] + [dict(nfc, **{"in": .2}), dict(bv, **{"in": .5}),
         {"k": "glow", "x": bvc[0], "y": bvc[1], "r": 100, "kind": "blue", "pulse": True, "in": .5},
         {"k": "q", "x": bvc[0], "y": bvc[1] + 14, "size": 40, "in": 1.2, "fx": "pop"},
         {"k": "label", "x": nfcc[0] - 6, "y": nfcc[1] - 22, "t": "corridor · seen", "a": "middle", "c": "#cfe6ff", "in": .6},
         {"k": "label", "x": bvc[0], "y": bvc[1] - 48, "t": "void · shape unknown", "a": "middle", "c": "#cfe6ff", "in": .9}])
    s8["els"] = [e for e in s8["els"] if e.get("k") not in ("dim",)]
    # the 3-D x-ray views: the pyramid turns slowly, its known rooms solid, the void dashed and glowing
    from iso3d import great_pyramid, shot as iso, lab, aim
    labL = lambda x, y, t, c=None: dict(lab(x, y, t, c), st="lab")
    s0 = aim(iso(great_pyramid(void=True) + [{"t": "q", "x": -26, "y": 62, "z": 0, "size": 120}]), (-20, 56, 0), 4.2)
    s2 = aim(iso(great_pyramid(void=False) + [labL(8, 55, "King's Chamber"), dict(labL(2, 18, "Queen's Chamber"), dy=46), labL(-30, 42, "Grand Gallery")]), (-5, 42, 0), 3.4)
    s8 = aim(iso(great_pyramid(void=True, nfc=True) + [labL(-26, 72, "void · shape unknown", "#cfe6ff"), labL(-100, 30, "corridor · seen", "#cfe6ff")]), (-10, 60, 0), 1.9, dy=40)
    shots = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
    beats = [
        {"role": "hook", "visual": {"from": 0}, "lines": [
            "[d:intrigue][k:INSIDE THE GREAT PYRAMID][sfx:boom][act:hushed wonder, drawing them in]There's a space inside the Great Pyramid that ^*nobody* has ever entered.",
            "[d:tension][cam:1.15|0|0][act:confiding, slowing down]We only ^know it's there... [act:the reveal, quietly delighted]because of particles from ^*space*."]},
        {"role": "world", "visual": {"from": 1, "cut": True}, "lines": [
            "[d:calm][k:GIZA · AT LEAST 4,500 YEARS][act:setting the scene, plain]The Great Pyramid, credited to ^Khufu. [go:2|2.2][act:guiding the eye, unhurried]Three great rooms inside: the ^King's Chamber, the ^Queen's, and the Grand ^Gallery."]},
        {"role": "collision", "visual": {"from": 2}, "lines": [
            "[d:build][k:MUONS][go:3|2][act:explaining, a spark of wonder]Cosmic rays hit our air and make [sfx:shimmer]^muons. [act:lighter, marvelling]Particles that rain through ^*everything*.",
            "[d:build][act:patient, laying it out][tune:level]^Stone stops some. [act:the payoff, clear and simple][tune:fall]^Empty space lets more ^*through*."]},
        {"role": "cost", "visual": {"from": 3}, "lines": [
            "[d:build][k:NOVEMBER 2017][go:4|2][act:brisk, matter of fact]Three teams put detectors ^inside, and ^out.",
            "[d:reveal][go:5|2.2][sfx:hit][act:the discovery, measured]All three saw ^extra muons, coming from ^above the Grand Gallery.",
            "[d:wonder][stamp:NATURE · 2017|gold][act:wonder, slowly]An ^empty space. [act:letting the size land]At least ^*thirty* metres long."]},
        {"role": "reversal", "visual": {"from": 6, "cut": True}, "lines": [
            "[d:reveal][k:THE TWIST][act:leaning in, fresh news]In {2023|twenty twenty-three}, muons found a ^second, smaller corridor behind the north ^face.",
            "[d:build][go:7|0][act:quiet, careful, step by step]A ^camera slid in between the ^stones. [sfx:shimmer][gap:0.4][act:hushed, the reveal][tune:fall]^*Empty*. [act:quiet satisfaction][tune:fall]^Right where the muons said."]},
        {"role": "tag", "visual": {"from": 8, "cut": True}, "lines": [
            "[d:verdict][k:THE VERDICT][p:0.95][act:calm, weighing it up]So the method ^works. [act:turning to the big one][tune:rise]And the Big ^Void? [act:the verdict, level-headed][tune:fall]^*Strong* evidence it's there.",
            "[d:tension][p:0.93][cam:1.25|0|0.02][act:quieter, the open mystery]What it was ^*for*... [act:simple, honest]^nobody knows. [gap:0.4][act:a small hopeful smile][tune:fallrise]^Yet."]},
    ]
    return {"id": "big-void", "code": "05.03", "series": SERIES, "title": "The Big Void", "case": "big-void", "verdict": "strong",
            "claim": "A hidden space above the Grand Gallery?", "mood": "mystery", "hook_text": "A space *nobody* has entered.",
            "beats": beats, "shots": shots,
            "sources": "Morishima et al. 2017, Nature · Procureur et al. 2023, Nature Communications",
            "post": "In 2017, cosmic-ray muons revealed a void at least 30 metres long inside the Great Pyramid. In 2023 a camera confirmed a second, smaller corridor. What the evidence shows.",
            "hashtags": ["#GreatPyramid", "#Giza", "#AncientEgypt", "#Archaeology", "#Physics"]}


def big_void_m():
    """The Big Void as one continuous take (see mural.py): muons rain through stone, a hollow lets more through, three buses for scale, a camera on a cable."""
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, ring, person, BLUE, BONE, AMBER, RED
    ep = big_void()
    S = Section(s=3.6, cx=500, gy=1150)
    bv, bvc = S.big_void()
    # the muon X-ray: rain from the sky, stone stops some, the hollow lets more through, the detector counts a bright spot
    xr = [line([[60, 330], [940, 330]], .2, "#6f8fa8", 2, dur=1.0), label(80, 305, "air", .5, "#9fb8cc", 28, "start"),
          arrow([[620, 260], [560, 326]], .6, "#ffe2a8", 3, "known", .5, False), glow(560, 330, 70, 1.1, .8, "lamp")]
    xr += [{"k": "rays", "x0": 140, "x1": 900, "y0": 340, "y1": 1080, "n": 70, "spread": .3, "c": BLUE, "in": 1.6, "fx": "draw", "dur": 2.0},
           label(860, 420, "muons", 2.6, BLUE, 32, "end"),
           person(150, 1380, 200, 3.6), line([[130, 1150], [140, 1400]], 4.0, "#cfe6ff", 3, dur=.4), line([[170, 1160], [176, 1400]], 4.2, "#cfe6ff", 3, dur=.4)]
    xr += [box(300, 640, 580, 420, "rgba(150,118,84,.92)", "#e7cfa6", 2, 6, 5.2, fx="fill", dur=.8), label(860, 1035, "stone", 5.6, "#2a1f16", 32, "end"),
           box(540, 780, 140, 110, "#0d0b09", "#9fd0ff", 2, 8, 6.6, fx="pop", style="inferred")]
    stopx = (340, 400, 460, 760, 820)
    for k, x in enumerate(stopx):
        yy = 760 + 70 * (k % 3)
        xr += [line([[x, 560], [x, yy]], 5.9 + .08 * k, "#cfe6ff", 2.4, dur=.5), dot(x, yy, 7, RED, 6.4 + .08 * k)]
    for k, x in enumerate((570, 610, 650)):
        xr += [line([[x, 560], [x, 1150]], 6.9 + .12 * k, "#cfe6ff", 3.2, dur=.7)]
    xr += [box(300, 1150, 580, 22, "#3d5566", "#9fd0ff", 2, 4, 7.8, fx="pop"), label(590, 1215, "detector", 8.0, "#cfe6ff", 28)]
    hs = (40, 46, 38, 44, 48, 120, 42, 38, 45)
    for k, h in enumerate(hs):
        xr.append(box(318 + 62 * k, 1380 - h * 1.25, 46, h * 1.25, BLUE if k == 5 else "#56708a", r=4, at=9.0 + .12 * k, fx="fill", dur=.5))
    xr += [glow(628, 1270, 110, 10.8, .8, "blue"), ring(610, 835, 105, 11.2, AMBER, 3), label(640, 1415, "count", 9.6, "#cfe6ff", 28)]
    xray = {"base": "dark", "cam": [1, 500, 860], "els": xr}
    # three buses end to end, the void's length to scale (3.6 px a metre)
    bus = []
    ca, sa = math.cos(math.radians(26)), math.sin(math.radians(26))
    P = lambda u, v: [round(bvc[0] + u * ca + v * sa, 1), round(bvc[1] - u * sa + v * ca, 1)]
    for k in range(3):
        u0 = -53 + 35.5 * k
        bus += [{"k": "poly", "p": [P(u0, -6), P(u0 + 34, -6), P(u0 + 34, 6), P(u0, 6)], "fill": AMBER, "c": "#1a1511", "w": 1, "in": round(2.2 + .3 * k, 2), "fx": "pop"},
                dot(*P(u0 + 7, 8), 3, "#1a1511", round(2.25 + .3 * k, 2)), dot(*P(u0 + 27, 8), 3, "#1a1511", round(2.25 + .3 * k, 2))]
    # the endoscope: a cable snakes in, its lamp lights the empty corridor
    scope = [line([[560, 1420], [540, 1250], [505, 1090], [500, 980]], .4, "#c9ad85", 6, dur=1.4, curve=True), dot(500, 975, 12, "#9fd0ff", 1.8), glow(500, 900, 220, 2.0, .5, "lamp")]
    nfc, nfcc = S.nfc()
    return remix(ep, scenes={3: xray}, adds={7: scope}, cams={4: [1.5, 405, 1000], 5: [2.5, bvc[0] + 35, bvc[1] + 60], 6: [3.6, nfcc[0] + 28, nfcc[1] + 20]}, line_adds={(3, 2): (bus, None)})





# ================================================================ helpers for the rest of the File
from scenes import egypt, giza_plan, sphinx_side, timeline, event, quote, stat, papyrus, SITES, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from films import View


def B(role, frm, lines, cut=True):
    return {"role": role, "visual": {"from": frm, "cut": cut} if cut else {"from": frm}, "lines": lines}


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


# ---------------------------------------------------------------- 05.04 Under the Sphinx
def sphinx_chambers():
    gy = 1000; m = 860 / 73.0                                  # 73 m of Sphinx over 860 px; the head faces east (left)
    X = lambda xm: round(500 - 430 + xm * m, 1)
    Y = lambda dm: round(gy - dm * m, 1)                       # dm metres above the enclosure floor (negative = below)
    sec = {"base": "section", "tod": "dusk", "ground": gy, "lx": 40,
           "layers": [{"d": 0, "c": "#8a6d4d", "t": ""}, {"d": 34, "c": "#6d5640", "t": "layered limestone", "ty": 150, "tex": "blocks", "to": .08}, {"d": 120, "c": "#4e3e30", "t": ""}],
           "water": 59, "waterT": "groundwater", "waterX": 820,
           "els": [{"k": "poly", "p": [[-600, gy - 110], [X(-12), gy - 110], [X(-10), gy], [X(83), gy], [X(85), gy - 110], [1600, gy - 110], [1600, gy], [-600, gy]], "fill": "#7f654a", "c": "rgba(255,226,190,.5)", "w": 1.5, "id": "walls"},
                   {"k": "sphinx", "x": 500, "y": gy, "w": 860, "id": "sph"},
                   {"k": "label", "x": X(-11), "y": gy - 126, "t": "enclosure wall", "st": "small", "id": "lw"}]}
    head = {"k": "line", "p": [[X(15.5), Y(17.6)], [X(15.5), Y(15.2)]], "c": SCAN, "w": 4, "id": "head"}
    bore = {"k": "line", "p": [[X(21.5), Y(13.5)], [X(21.5), Y(13.5 - 8.2)]], "c": SCAN, "w": 3, "style": "inferred", "id": "bore"}
    rumpU = {"k": "line", "p": [[X(69), Y(3)], [X(67), Y(7)]], "c": SCAN, "w": 4, "id": "rumpU"}
    rumpL = {"k": "line", "p": [[X(69), Y(3)], [X(70), Y(-2)]], "c": SCAN, "w": 4, "id": "rumpL"}
    key = {"k": "line", "p": [[X(58), Y(0)], [X(58), Y(-1.5)]], "c": SCAN, "w": 4, "id": "key"}
    hall = {"k": "rect", "x": X(-4), "y": Y(-7), "w": 26 * m, "h": 5 * m, "fill": "rgba(242,201,142,.08)", "c": GOLD, "sw": 2.4, "style": "claimed", "id": "hall"}
    anom = {"k": "rect", "x": X(0), "y": Y(-4.5), "w": 9 * m, "h": 3 * m, "fill": "rgba(159,208,255,.12)", "c": SCAN, "sw": 2.2, "style": "inferred", "id": "anom"}
    drill = {"k": "line", "p": [[X(40), Y(0)], [X(40), Y(-6)]], "c": BONE, "w": 3, "id": "drill"}
    cav = {"k": "circle", "x": X(40), "y": Y(-6.8), "r": 9, "fill": "rgba(245,236,220,.15)", "c": BONE, "w": 1.6, "id": "cav"}
    s0 = sphinx_side("dusk"); s0["cam"] = [1.5, 470, 900]
    s0["els"] += [{"k": "q", "x": 314, "y": 872, "size": 56, "in": .4, "fx": "pop"}, {"k": "q", "x": 770, "y": 1010, "size": 56, "in": .8, "fx": "pop"},
                  {"k": "q", "x": 232, "y": 1135, "size": 64, "in": 1.2, "fx": "pop"}]
    s1 = sphinx_side("dusk"); s1["els"] += [{"k": "dim", "x1": 190, "y1": 1105, "x2": 810, "y2": 1105, "t": "c. 73 m", "ly": 40, "in": .5},
                                          {"k": "person", "x": 870, "y": 1060, "h": 20, "t": False}]
    s2 = dict(sec, cam=[1, 500, 900]); s2 = like(s2, add=[dict(hall, **{"in": .3, "fx": "draw"}), {"k": "label", "x": X(9), "y": Y(-4.2), "t": "a 'Hall of Records'?", "c": GOLD, "in": 1},
                                                        {"k": "cap", "x": 500, "y": 420, "t": "Edgar Cayce · 1933 · a psychic reading", "in": .2}])
    s3 = like(dict(sec, cam=[1.15, 500, 930]), add=[dict(head, **{"in": .3, "fx": "draw"}), dict(bore, **{"in": .6, "fx": "draw"}), dict(rumpU, **{"in": .9, "fx": "draw"}),
                                                   dict(rumpL, **{"in": 1.1, "fx": "draw"}), dict(key, **{"in": 1.3, "fx": "draw"}),
                                                   {"k": "label", "x": X(15.5), "y": Y(19.5), "t": "shaft in the head", "st": "small", "in": .5},
                                                   {"k": "label", "x": X(23), "y": Y(4.5), "t": "1837 boring, 8.2 m", "st": "small", "a": "start", "in": .8}])
    s4 = like(s3, cam=[2.6, X(66), Y(1)], add=[{"k": "label", "x": X(64), "y": Y(8.5), "t": "upper branch · a niche", "st": "small", "a": "end", "in": .3},
                                               {"k": "label", "x": X(71), "y": Y(-3.4), "t": "lower branch · groundwater", "st": "small", "a": "start", "in": .7},
                                               {"k": "label", "x": X(56.5), "y": Y(-2.6), "t": "'keyhole'", "st": "small", "a": "end", "in": 1.0}])
    fan = {"k": "fan", "x": X(4.5), "y": gy, "a0": 55, "a1": 125, "r": 170, "n": 11, "in": .2, "fx": "fade"}
    s5 = like(s3, cam=[2.2, X(8), Y(-1)], add=[fan, dict(anom, **{"in": 1.0}), {"k": "q", "x": X(4.5), "y": Y(-3.4), "size": 44, "in": 1.4, "fx": "pop"},
                                               {"k": "label", "x": X(4.5), "y": Y(-6.2), "t": "1991 seismic anomaly", "st": "small", "c": "#cfe6ff", "in": 1.2}])
    s6 = like(s5, cam=[1.2, 470, 970], add=[dict(drill, **{"in": .3, "fx": "draw"}), dict(cav, **{"in": 1.0}),
                                             {"k": "label", "x": X(40), "y": Y(-9.5), "t": "1998 test drill · natural cavity", "st": "small", "in": 1.2},
                                             {"k": "label", "x": X(4.5), "y": Y(-8.8), "t": "never opened", "st": "small", "c": GOLD, "in": 1.8}])
    s7 = like(s6, cam=[1.05, 500, 930], add=[dict(hall, **{"in": .2, "op": .45}), {"k": "label", "x": X(9), "y": Y(-7.6), "t": "no trace of a hall", "c": GOLD, "st": "small", "in": .6}])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE GREAT SPHINX][sfx:boom][act:playful, drawing them in]The Sphinx has ^holes in it. [act:pointing them out][tune:level]In its ^*head*. [act:one more, a small grin][tune:fall]In its ^*back*.",
                      "[d:tension][cam:1.15|0|0.05][act:lower, conspiratorial]And under its ^paws... [act:hushed, the hook]something ^*nobody* has opened."], cut=False),
        B("world", 1, ["[d:calm][k:GIZA · AT LEAST 4,500 YEARS][act:admiring, unhurried]Seventy-three metres of ^lion, carved straight out of the ^bedrock.",
                       "[d:build][go:2|0][act:neutral storyteller, even-handed]In {1933|nineteen thirty-three}, the American psychic Edgar Cayce said a Hall of ^Records@noun lay beneath it. [act:evenly, no wink]Left by survivors of ^*Atlantis*."]),
        B("collision", 3, ["[d:build][k:THE HOLES][act:curious, getting practical][tune:fall]So what's ^actually in there? [act:counting them off][tune:level]A ^shaft in the ^head. [act:same pace, next one][tune:level]A hole drilled behind it in {1837|eighteen thirty-seven}. [go:4|2.2][act:the last one, a small grin][tune:fall]A ^tunnel in the ^rump.",
                           "[d:list][sfx:hit][act:brisk, factual]Each one has been ^explored. [act:plainly, steady]Each one ends in ^rock... [act:a shrug in the voice][tune:fall]or ^*groundwater*."]),
        B("cost", 4, ["[d:build][k:1991 · THE SCAN][go:5|2.2][act:building, a little intrigue]Then a seismic survey@noun found ^something under the front paws. [act:quiet, letting it land]A ^hollow. [act:tentative, intrigued][tune:fallrise]Maybe cut by ^*hands*."], cut=False),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][go:6|2.2][act:leaning in]In {1998|nineteen ninety-eight}, one anomaly near the Sphinx ^*was* drilled. [sfx:hit][act:plain, a touch deflating][tune:fall]A ^natural cavity.",
                          "[d:reveal][act:turning back to it][tune:rise]But the hollow under the ^paws? [act:quiet, pointed][tune:fall]^*Never* opened."], cut=False),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]A ^small hidden space? [act:fair, open][tune:fall]^Possible. [act:same measure][tune:rise]A hall of ^records@noun? [act:firm, level-headed][tune:fall]Not a ^trace of one.",
                     "[d:tension][p:0.93][cam:1.2|0|0.08][act:the last word, quietly practical]^One narrow drill hole could ^*settle* it."]),
    ]
    return EP("sphinx-chambers", "05.04", "Under the Sphinx", "sphinx-chambers", "unsupported", "A Hall of Records under the Sphinx?",
              "Something *under* the paws.", beats, shots,
              "Lehner & Hawass 2017, Giza and the Pyramids · Dobecki & Schoch 1992, Geoarchaeology · Hawass & Lehner 1994, Archaeology",
              "The Sphinx has a shaft in its head, a tunnel in its rump and an unopened seismic anomaly under its paws. What is actually down there.",
              ["#Sphinx", "#Giza", "#AncientEgypt", "#HallOfRecords", "#Archaeology"])


def sphinx_chambers_m():
    """Under the Sphinx as one continuous take: the lion carved out of the bedrock, a knock that echoes, a hall struck out, one drill hole."""
    import copy
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, ring, strike, tri, question, person, BLUE, BONE, AMBER, RED
    ep = sphinx_chambers()
    gy = 1000; m = 860 / 73.0
    X = lambda xm: round(500 - 430 + xm * m, 1)
    Y = lambda dm: round(gy - dm * m, 1)
    s0 = copy.deepcopy(ep["shots"][0])
    qs = [e for e in s0["els"] if e.get("k") == "q"]
    for e, t in zip(qs, (3.3, 4.3, 5.9)):
        e["in"] = t
    # 73 m of lion, as long as a jumbo jet, not built but carved: the rock beds run straight through walls and lion
    w1 = sphinx_side("dusk", w=620, x=500, gy=1060, pyramid=False)
    jet = [{"k": "poly", "p": [[200, 600], [225, 584], [770, 582], [800, 590], [800, 612], [225, 616]], "fill": "rgba(220,230,240,.12)", "c": "#e8eef4", "w": 2.5, "in": 3.0, "fx": "draw", "dur": 1.0},
           {"k": "poly", "p": [[440, 610], [560, 610], [470, 680]], "fill": "rgba(220,230,240,.12)", "c": "#e8eef4", "w": 2.5, "in": 3.2, "fx": "draw", "dur": .6},
           {"k": "poly", "p": [[730, 586], [780, 520], [805, 520], [790, 588]], "fill": "rgba(220,230,240,.12)", "c": "#e8eef4", "w": 2.5, "in": 3.3, "fx": "draw", "dur": .6},
           label(500, 520, "jumbo jet", 3.6, "#e8eef4", 30)]
    w1["els"] += [{"k": "dim", "x1": 190, "y1": 1105, "x2": 810, "y2": 1105, "t": "73 m", "ly": 40, "in": 2.0}] + jet
    w1["els"] += [box(330 + 120 * (k % 3), 950 + 55 * (k // 3), 112, 50, "none", "#f5ecdc", 2, 4, 3.9 + .06 * k, style="claimed") for k in range(6)] + [strike(320, 1065, 700, 940, 4.5)]
    w1["els"] += [line([[140, 965], [860, 965]], 4.9, "#f5ecdc", 2.5, "claimed", 1.0)] + [arrow([[x, 1045], [x, 900]], 5.3 + .25 * j, AMBER, 3, "known", .5, False) for j, x in enumerate((158, 842))]
    w1["els"] += [line([[40, y], [960, y]], 6.3 + .2 * j, "#ffe2a8", 2.5, dur=.9, op=.75) for j, y in enumerate((985, 1012, 1040))] + [glow(500, 980, 320, 7.1, .35)]
    w1["cam"] = [1.3, 500, 800]
    # the 1991 survey, retimed to the words: a sounding, a knock that echoes, a hollow under the paws
    s5 = copy.deepcopy(ep["shots"][5])
    for e in s5["els"]:
        if e.get("k") == "fan":
            e["in"] = 1.0
        elif e.get("id") == "anom":
            e["in"] = 6.4
        elif e.get("k") == "q" and e.get("in", -1) > 0:
            e["in"] = 7.0
        elif e.get("k") == "label" and "1991" in e.get("t", ""):
            e["in"] = 2.0
    s5["els"] += [ring(X(4.5), gy, r, 3.0 + .4 * j, BLUE, 2, dur=.6) for j, r in enumerate((14, 28, 42))]
    s4 = copy.deepcopy(ep["shots"][4])
    for e in s4["els"]:
        if e.get("k") == "label" and e.get("t", "").startswith("lower branch"):
            e.update(x=X(70), y=Y(-4.6), a="end")
    # the verdict: a small space ringed, the hall struck out; then one narrow drill hole
    hall_x, hall_y, hall_w, hall_h = X(-4), Y(-7), 26 * m, 5 * m
    v = [ring(X(4.5), Y(-6), 75, .6, AMBER, 3), strike(hall_x, hall_y + hall_h, hall_x + hall_w, hall_y, 3.0)]
    drill = [tri(X(4.5), 915, 20, 180, "#cbbca8", .2), line([[X(4.5), 930], [X(4.5), Y(-4.5)]], .4, BONE, 5, dur=1.2), glow(X(4.5), Y(-6), 90, 1.8, .7, "blue")]
    s7 = copy.deepcopy(ep["shots"][7])
    s7["els"] = [e for e in s7["els"] if not (e.get("k") == "label" and e.get("t") in ("1991 seismic anomaly", "never opened", "1998 test drill · natural cavity"))]
    for e in s7["els"]:
        if e.get("k") == "label" and e.get("t") == "no trace of a hall":
            e.update(y=Y(-7) + 5 * m + 48, x=hall_x + hall_w / 2)
    s7["cam"] = [1.6, 330, 1030]
    return remix(ep, scenes={0: s0, 1: w1, 4: s4, 5: s5, 7: s7}, adds={7: v}, cams={4: [2.6, X(66) - 60, Y(1)], 5: [2.2, X(8) + 70, Y(-1)], 6: [1.1, 462, 970]}, line_adds={(5, 1): (drill, None)})


# ---------------------------------------------------------------- 05.06 The Diary of Merer
def merer():
    p0 = papyrus(hl={"x": 250, "y": 520, "w": 460, "h": 150}); p0["cam"] = [1.7, 480, 640]
    p0["els"] += [{"k": "cap", "x": 500, "y": 1240, "t": "Papyrus Jarf B · dated by its text to Khufu's reign", "in": .5, "layer": "top"}]
    m1, v = egypt(29.6, 34.2, 27.6, 31.4, rect=(40, 330, 920, 900),
                  pins=[("Giza", {"a": "end", "lx": -18}), ("Wadi al-Jarf", {"c": OCHRE, "lx": -18, "a": "end", "ly": 40}), ("Cairo", {"r": 5, "c": "#8f8577", "st": "small", "ly": -14})])
    gx, gyy = v.p(*SITES["Giza"]); wx, wy = v.p(*SITES["Wadi al-Jarf"])
    m1["els"] += [{"k": "label", "x": 700, "y": 1180, "t": "Red Sea", "st": "ital", "c": "#9fc4d8", "in": .6},
                  {"k": "arrow", "p": [[gx + 20, gyy + 10], [(gx + wx) / 2, (gyy + wy) / 2 - 60], [wx - 16, wy - 8]], "curve": True, "c": AMBER, "w": 2, "style": "inferred", "in": 1.2, "fx": "draw"}]
    m1["cam"] = [1.2, 560, 880]
    p2 = papyrus(); p2["els"] += [{"k": "cap", "x": 500, "y": 300, "t": "the oldest inscribed papyri known", "in": .3},
                                  {"k": "label", "x": 500, "y": 1260, "t": "found in 2013 in storage galleries at the harbour", "st": "small", "in": .8}]
    log = [("Day 25", "loading stone at Tura North"), ("Day 26", "sailing, with a load of stone"), ("Day 27", "night at She-Khufu"), ("Day 28", "delivered at Akhet-Khufu")]
    p3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 90, "y": 420, "t": "from Merer's logbook · paraphrase after Tallet 2017", "a": "start", "in": .1}] +
          [e for i, (d, t) in enumerate(log) for e in ({"k": "label", "x": 90, "y": 540 + i * 110, "t": d, "st": "mono", "a": "start", "c": AMBER, "in": .4 + i * .5},
                                                        {"k": "label", "x": 250, "y": 540 + i * 110, "t": t, "st": "body", "a": "start", "in": .5 + i * .5, "fx": "type", "dur": .9})]}
    v2 = View(31.08, 31.33, 29.88, 30.01, (40, 330, 920, 900))
    T = v2.p(31.285, 29.935); G = v2.p(31.134, 29.979)
    nile = [v2.p(31.222, 29.88), v2.p(31.226, 29.93), v2.p(31.231, 29.97), v2.p(31.229, 30.01)]
    flood = [v2.p(31.16, 29.88), v2.p(31.165, 30.01), v2.p(31.265, 30.01), v2.p(31.268, 29.88)]
    m4 = {"base": "plan", "north": [900, 360], "cam": [1.08, 500, 860], "els": [
        {"k": "poly", "p": flood, "fill": "rgba(111,182,214,.16)", "c": "rgba(111,182,214,.5)", "w": 1.4, "style": "inferred", "id": "flood"},
        {"k": "label", "x": v2.p(31.20, 30.0)[0], "y": v2.p(31.20, 30.0)[1], "t": "valley under the flood, July to November", "st": "small", "c": "#9fd0ff"},
        {"k": "line", "p": nile, "c": "#6fb6d6", "w": 14, "op": .9, "curve": True},
        {"k": "poly", "p": [v2.p(31.148, 29.972), v2.p(31.19, 29.97), v2.p(31.19, 29.958), v2.p(31.15, 29.956)], "fill": "rgba(111,182,214,.5)", "c": "#9fd0ff", "w": 1.5, "style": "inferred", "curve": True, "id": "basin"},
        {"k": "pyramid", "x": G[0], "y": G[1] + 6, "w": 34, "courses": False, "id": "gp"},
        {"k": "poly", "p": [[T[0] - 20, T[1] - 40], [T[0] + 60, T[1] - 30], [T[0] + 70, T[1] + 40], [T[0] - 10, T[1] + 50]], "fill": "url(#k-hatch)", "c": "#f2dcb4", "w": 1.4, "id": "quarry"},
        {"k": "label", "x": T[0] + 26, "y": T[1] + 88, "t": "Tura limestone quarries", "in": .2},
        {"k": "label", "x": G[0], "y": G[1] + 52, "t": "Akhet-Khufu", "in": .5},
        {"k": "label", "x": G[0], "y": G[1] + 84, "t": "'Horizon of Khufu' · the pyramid", "st": "small", "c": "#cbbca8", "in": .7},
        {"k": "scale", "x": 80, "y": 1170, "w": round(v2.km(5), 1), "t": "5 km"}]}
    route = {"k": "arrow", "p": [[T[0] - 24, T[1]], v2.p(31.24, 29.945), v2.p(31.2, 29.962), [G[0] + 30, G[1] + 10]], "curve": True, "c": AMBER, "w": 3.4, "in": .3, "fx": "draw", "dur": 2.4}
    m5 = like(m4, add=[route, {"k": "label", "x": v2.p(31.168, 29.95)[0], "y": v2.p(31.168, 29.95)[1] + 40, "t": "She-Khufu basin", "st": "small", "c": "#9fd0ff", "in": 1.2},
                       {"k": "boat", "x": v2.p(31.215, 29.953)[0], "y": v2.p(31.215, 29.953)[1], "w": 120, "in": 1.4, "fx": "rise"}])
    s6 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 560, "t": "his boss", "in": .1},
          {"k": "title", "y": 680, "t": "Ankhhaf", "st": "big", "in": .3, "fx": "pop"},
          {"k": "label", "x": 500, "y": 760, "t": "half-brother of King Khufu", "in": .7},
          {"k": "label", "x": 500, "y": 805, "t": "overseer of Ra-shi-Khufu, the harbour at Giza", "st": "small", "c": "#cbbca8", "in": 1.0}]}
    s7 = {"base": "sky", "tod": "dawn", "ground": 1000, "sun": [800, 830, 36], "cam": [1, 500, 900], "els": [
        {"k": "pyramid", "x": 560, "y": 1000, "w": 700, "courses": False, "light": "left", "depth": .05},
        {"k": "water", "y": 1040, "h": 150, "op": .85},
        {"k": "boat", "x": 330, "y": 1110, "w": 330, "in": .3, "fx": "rise"},
        {"k": "block", "x": 262, "y": 1086, "w": 46, "h": 26, "in": .6}, {"k": "block", "x": 318, "y": 1086, "w": 46, "h": 26, "in": .7}, {"k": "block", "x": 374, "y": 1086, "w": 46, "h": 26, "in": .8},
        {"k": "cap", "x": 500, "y": 470, "t": "Akhet-Khufu · white Tura casing, new", "in": 1.2}]}
    shots = [p0, m1, p2, p3, m4, m5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE RED SEA SCROLLS][sfx:boom][act:delighted, a surprising fact][tune:risefall]The oldest written papyrus ever found is a ^*work diary*.",
                      "[d:tension][cam:1.15|0|0.04][act:leaning in, slower]And it names a ^pyramid: the Horizon of ^*Khufu*."], cut=False),
        B("world", 1, ["[d:calm][k:WADI AL-JARF · 2013][act:plain storytelling]In {2013|twenty thirteen}, Pierre Tallet's team was digging an ancient ^harbour on the Red Sea.",
                       "[d:wonder][go:2|0][sfx:shimmer][act:wonder, slowly]In its storage galleries: ^rolls of papyrus. [act:careful, precise]Dated by the reign they name to at least four and a half ^*thousand* years ago."]),
        B("collision", 3, ["[d:build][k:INSPECTOR MERER][act:introducing him, warmly]They belonged to an inspector named ^Merer, in charge of about forty ^boatmen.",
                           "[d:list][go:4|0][act:steady, rhythmic]Day after day, he ^logged the job@work. [act:walking through the route][tune:level]^Loading white limestone at the ^Tura quarries. [go:5|2.6][act:same rhythm][tune:level]^Sailing across the ^flood. [act:arriving, landing it][tune:fall]^Unloading at ^Akhet-Khufu. [act:softer, translating it][tune:fall]The ^*Horizon of Khufu*."]),
        B("cost", 5, ["[d:build][k:THE NUMBERS][act:doing the maths, brisk]Two or three round ^trips every ^ten days. [act:impressed, careful]Perhaps [count:200|blocks a month]^*two hundred* blocks a month."], cut=False),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:leaning in, a tease][tune:rise]And his ^boss? [act:the name, clear][tune:fall]^Ankhhaf. [act:letting it sink in][tune:fall]Khufu's ^own half-brother.",
                          "[d:reveal][sfx:hit][act:building, one by one][tune:level]A ^named ^crew. [act:same beat, building][tune:level]A named ^boss. [act:same beat, higher][tune:level]A named ^pyramid. [act:the payoff, warm wonder][tune:fall]In their own ^*handwriting*."]),
        B("tag", 7, ["[d:verdict][k:WHAT IT SHOWS][p:0.95][act:calm summary, sure-footed]A ^crew, shipping white casing stone to a pyramid named for ^*Khufu*.",
                     "[d:tension][p:0.93][cam:1.15|0|0.05][act:honest, naming the limit]What it ^can't tell us: when the ^first stone was laid. [act:quiet, candid][tune:fall]That's still ^*open*."]),
    ]
    return EP("merer", "05.06", "The Diary of Merer", "merer", "solid", "What did the work crews write down?", "A diary from the *work site*.", beats, shots,
              "Tallet 2017, Les papyrus de la mer Rouge I · Tallet & Marouard 2014, Near Eastern Archaeology · Tallet & Lehner 2021, The Red Sea Scrolls",
              "In 2013, archaeologists found the logbook of Inspector Merer, who shipped limestone to Akhet-Khufu, the Horizon of Khufu. The oldest inscribed papyri known. What it shows, and what it can't.",
              ["#GreatPyramid", "#Khufu", "#AncientEgypt", "#Archaeology", "#History"])


def merer_m():
    """The Diary of Merer as one continuous take: an inspector and forty boatmen, ten days and three round trips, the chain of command up to the king."""
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, ring, person, question, BLUE, BONE, AMBER, GREEN
    ep = merer()
    # Merer and his crew of about forty
    crew = [person(220, 1250, 300, .5), glow(220, 1100, 200, .5, .4), label(220, 1310, "Merer", 1.0, AMBER, 34),
            {"k": "boat", "x": 665, "y": 1260, "w": 520, "in": 1.6, "fx": "rise"}]
    crew += [person(440 + 50 * (k % 10), 760 + 115 * (k // 10), 90, round(2.0 + .04 * k, 2)) for k in range(40)]
    crew += [label(665, 640, "about 40 boatmen", 3.8, BONE, 32),
             box(285, 1040, 70, 92, "#e9dcc4", "#fff6e6", 2, 6, 4.6, fx="pop")] + [line([[295, 1062 + 16 * j], [345, 1062 + 16 * j]], 4.8 + .1 * j, "#6b5640", 2, dur=.3) for j in range(4)]
    crewS = {"base": "dark", "cam": [1.05, 520, 980], "els": crew}
    # ten days, two or three round trips
    days = [box(150 + 72 * j, 1300, 60, 40, "rgba(232,184,122,.18)", AMBER, 1.5, 6, round(5.6 + .06 * j, 2), fx="pop") for j in range(10)]
    days += [line([[180 + 72 * a, 1296], [180 + 72 * (a + 1.5), 1236], [180 + 72 * (a + 3), 1296]], 6.4 + .4 * n, "#9fd0ff", 3, dur=.5, curve=True) for n, a in enumerate((0, 3, 6))]
    days += [label(500, 1392, "10 days", 6.1, AMBER, 30)]
    # the chain of command: a crew, an inspector, a half-brother, a king and his pyramid
    ch = [person(700, 760, 160, .3), label(700, 805, "Ankhhaf", .7, AMBER, 32),
          {"k": "pyramid", "x": 300, "y": 545, "w": 230, "courses": False, "in": 1.6, "fx": "rise"},
          person(300, 760, 170, 1.8, "#f2dcb4"), glow(300, 680, 130, 1.8, .45), label(300, 805, "Khufu", 2.0, "#f2dcb4", 32),
          line([[400, 680], [610, 680]], 2.3, "#f2dcb4", 2, "inferred", .7), label(505, 655, "half-brother", 2.5, "#cbbca8", 28),
          {"k": "boat", "x": 700, "y": 1290, "w": 380, "in": 3.4, "fx": "rise"}]
    ch += [person(600 + 34 * k, 1262, 52, round(3.6 + .05 * k, 2)) for k in range(7)]
    ch += [person(700, 1080, 130, 4.0), label(760, 1040, "Merer", 4.2, AMBER, 30, "start"),
           arrow([[700, 1200], [700, 1100]], 4.4, AMBER, 3, "known", .4, False), arrow([[700, 940], [700, 830]], 4.8, AMBER, 3, "known", .4, False),
           ring(700, 1250, 160, 6.2, AMBER, 3), ring(700, 668, 95, 6.8, AMBER, 3), ring(310, 470, 120, 7.4, AMBER, 3),
           {"k": "glyphs", "x": 110, "y": 1150, "w": 330, "h": 170, "rows": 4, "cols": 6, "kind": "hieratic", "c": "#e9dcc4", "in": 7.9}]
    chain = {"base": "dark", "cam": [1, 500, 880], "els": ch}
    # the casing: the smooth white skin of the lit face; and a question at its first course
    casing = [{"k": "poly", "p": [[210, 1000], [686, 1035], [604, 555]], "fill": "rgba(255,250,240,.3)", "c": "#ffffff", "w": 2.5, "in": 3.4, "fx": "draw", "dur": 1.2}]
    first = question(330, 950, 1.0, 70)
    return remix(ep, scenes={3: crewS, 6: chain}, adds={5: days, 7: casing}, line_adds={(5, 1): (first, None)})


# ---------------------------------------------------------------- 05.09 The Builders' Town
def builders_town():
    pl, P = giza_plan(scale=.8, cx=500, cy=800)
    pl["cam"] = [1.0, 500, 860]
    tx, ty = P(*__import__("scenes").GP["town"])
    s0 = like(pl, cam=[2.1, tx, ty - 40], add=[{"k": "glow", "x": tx, "y": ty, "r": 190, "kind": "red", "pulse": True, "in": .2}])
    from iso3d import plateau, plateau_labels, aim, lab as _lab
    from scenes import GP as _GP
    _tx, _tn = _GP["town"]
    s0 = aim(plateau(extra=[{"t": "glow", "x": _tx, "y": 5, "z": -_tn, "r": 190, "kind": "red", "pulse": True}]), (_tx - 20, 0, -_tn), 3.0)
    s1 = plateau(extra=plateau_labels(), s=.5)
    s1["els"].append({"k": "label", "x": s1["cam"][1], "y": s1["cam"][2] + 470, "t": "true size and place · one grid square = 100 m", "st": "small", "c": "#b9aa97", "in": .8})
    gal = [{"k": "rect", "x": 170 + i * 72, "y": 520, "w": 52, "h": 380, "fill": "rgba(220,191,148,.35)", "c": "#f2dcb4", "sw": 1.6, "in": .1 + i * .08} for i in range(8)]
    bak = [{"k": "circle", "x": 230 + i * 44, "y": 1020, "r": 14, "fill": "rgba(236,90,60,.35)", "c": OCHRE, "w": 1.6, "in": 1.2 + i * .05} for i in range(10)]
    from iso3d import shot as _iso, galleries, lab as _lab
    s2 = _iso(galleries() + [{"t": "person", "x": 23, "y": 0, "z": 22, "h": 1.7},
              dict(_lab(0, 4, "galleries · long halls, perhaps for sleeping crews", z=-17.5), st="lab"),
              dict(_lab(0, 2, "bread-baking pots", "#ffb09a", z=25), st="lab", dy=40)],
              cam=[1, 500, 900], s=13, x=500, y=1000, az=-30, spin=2.0, el=.42, table={"r": 30, "rz": 30, "grid": 5, "strata": [{"h": 1, "c": "#a8845c"}, {"h": 3, "c": "#8a6a4a"}]})
    s3 = stat("11", "cattle a day", "and 37 sheep and goats, by one estimate of what the town ate", "Redding, AERA · from the animal bones")
    s4 = {"base": "sky", "tod": "day", "ground": 1080, "sun": [760, 560, 30], "far": [[640, 280], [880, 160]], "cam": [1, 500, 900], "els": [
        {"k": "house", "x": 240, "y": 1110, "w": 90, "h": 44, "in": .2}, {"k": "house", "x": 360, "y": 1120, "w": 70, "h": 36, "in": .3},
        {"k": "house", "x": 460, "y": 1106, "w": 120, "h": 56, "fill": "#9a7b58", "in": .4},
        {"k": "cap", "x": 500, "y": 420, "t": "14 April 1990 · the builders' cemetery", "in": .6}]}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 520, "t": "titles in their tombs", "in": .1},
          {"k": "title", "y": 640, "t": "overseer of the side of the pyramid", "st": "ital", "in": .4, "fx": "type"},
          {"k": "title", "y": 740, "t": "director of the draftsmen", "st": "ital", "in": 1.3, "fx": "type"},
          {"k": "title", "y": 840, "t": "director for the king's work", "st": "ital", "in": 2.1, "fx": "type"}]}
    bone = [{"k": "poly", "p": [[260, 820], [470, 800], [490, 780], [515, 800], [540, 790], [740, 770], [745, 800], [540, 830], [515, 842], [490, 830], [470, 836], [262, 850]], "fill": "#e8dcc6", "c": "#fff6e6", "w": 1.6, "curve": False, "in": .2},
            {"k": "circle", "x": 505, "y": 815, "r": 42, "c": GOLD, "w": 2.4, "style": "inferred", "in": .8},
            {"k": "label", "x": 505, "y": 900, "t": "healed fracture, set in a splint", "c": GOLD, "in": 1.0}]
    s6 = {"base": "dark", "cam": [1, 500, 860], "els": bone + [{"k": "cap", "x": 500, "y": 620, "t": "from the skeletons", "in": .1},
          {"k": "label", "x": 500, "y": 1000, "t": "worn spines · healed arms and legs · two survived amputations", "st": "small", "in": 1.4}]}
    s7 = {"base": "sky", "tod": "dawn", "ground": 1080, "sun": [780, 880, 34], "cam": [1, 500, 880], "els": [
        {"k": "pyramid", "x": 380, "y": 1040, "w": 520, "cap": 0}, {"k": "pyramid", "x": 760, "y": 1060, "w": 300, "cap": .12},
        {"k": "house", "x": 140, "y": 1150, "w": 110, "h": 50}, {"k": "house", "x": 280, "y": 1160, "w": 90, "h": 40},
        {"k": "person", "x": 520, "y": 1180, "h": 70, "t": False, "in": .3}, {"k": "person", "x": 580, "y": 1182, "h": 66, "t": False, "in": .5},
        {"k": "person", "x": 640, "y": 1178, "h": 72, "t": False, "in": .7}]}
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:GIZA][sfx:boom][act:an opener, curious][tune:fall]^Who worked on the pyramids? [act:playful, a little smile][tune:risefall]We found where they ^*ate*.",
                      "[d:tension][cam:1.12|0|0][act:lower, more serious]And where they were ^*buried*."], cut=False),
        B("world", 1, ["[d:calm][k:1988 · HEIT EL-GHURAB][act:plain storytelling, setting out]South of the Sphinx, past a ^giant stone wall, archaeologist Mark Lehner started ^digging.",
                       "[d:wonder][go:2|0][sfx:shimmer][act:wonder, unfolding it]He found a ^planned ^town. [act:naming the rooms, lightly][tune:level]Long ^galleries. [act:same lightness][tune:level]^Storerooms. [act:delighted, the best one][tune:fall]^*Bakeries*."]),
        B("collision", 3, ["[d:build][k:THE MENU][act:relishing the detail]And the ^bones of their meals. [act:reading the tally, careful]By one estimate@noun: [count:11|cattle a day]^*eleven* cattle, and ^thirty-seven sheep and goats... [act:the kicker, amused][tune:risefall]a ^*day*."]),
        B("cost", 4, ["[d:build][k:1990 · THE CEMETERY][act:lightly, a happy accident]Then a tourist's ^horse stumbled on a mud-brick ^wall.",
                      "[d:list][go:5|0][act:quieter, respectful]Behind it: the ^workers' own ^tombs. [act:gently amused, reading the title]With job@work titles, like ^*overseer* of the ^side of the pyramid."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:gentle, leaning in]Their ^skeletons tell the rest. [act:with care, slowly][tune:level]^Worn spines. [act:tender, the turn][tune:fall]Broken arms, set, and ^*healed*. [sfx:hit][act:quiet admiration]Even ^amputations they survived.",
                          "[d:reveal][act:warm, the heart of it]Someone was ^*caring* for these workers."]),
        B("tag", 7, ["[d:verdict][k:WHAT IT SHOWS][p:0.95][act:calm summary, a warm smile]A workforce, fed on ^bread, ^beer and ^beef. [act:softer, respectful][tune:fall]Buried in the ^shadow of the pyramids.",
                     "[d:tension][p:0.93][cam:1.12|0|0.05][act:honest, the open edge]What it ^can't show: when work on this plateau first ^*began*."]),
    ]
    return EP("builders-town", "05.09", "The Builders' Town", "builders-town", "solid", "Who worked at Giza?", "We found where they *ate*.", beats, shots,
              "Lehner & Hawass 2017, Giza and the Pyramids · Redding 2013, ICAZ proceedings · Hawass, tombs of the pyramid builders",
              "A planned town, bakeries, 11 cattle a day, and the workers' tombs with their healed bones. What they show about who worked at Giza, and what they can't.",
              ["#Pyramids", "#Giza", "#AncientEgypt", "#Archaeology", "#History"])


def _cow(x, y, at):
    from illus import box, line
    c = "#b08a62"
    return [box(x - 34, y - 20, 68, 34, c, r=12, at=at, fx="pop"), box(x + 26, y - 30, 22, 20, c, r=6, at=at, fx="pop")] + \
           [line([[x + dx, y + 12], [x + dx, y + 32]], at, c, 5, draw=False) for dx in (-24, -12, 14, 24)]


def builders_town_m():
    """The Builders' Town as one continuous take: a day's meat drawn head by head, a pyramid side with its overseer, a healed bone in its splint."""
    import copy
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, oval, ring, person, question, BLUE, BONE, AMBER
    ep = builders_town()
    # the menu, read from the bones: 11 cattle and 37 sheep and goats, every day
    bone = lambda x, y, at: [line([[x - 34, y], [x + 34, y]], at, "#efe6d2", 11, draw=False)] + [dot(x + dx, y + dy, 8, "#efe6d2", at, None) for dx in (-38, 38) for dy in (-6, 6)]
    mn = sum([bone(x, y, a) for x, y, a in ((420, 520, .4), (560, 505, .6), (490, 470, .8), (620, 545, 1.0), (380, 560, 1.1))], [])
    mn += [arrow([[500, 600], [500, 670]], 2.4, AMBER, 3, "known", .4, False)]
    mn += sum([_cow(230 + 110 * (k % 6), 740 + 110 * (k // 6), round(3.9 + .08 * k, 2)) for k in range(11)], [])
    mn += [label(500, 925, "11 cattle", 4.9, AMBER, 34)]
    for k in range(37):
        x, y = 200 + 66 * (k % 10), 1010 + 62 * (k // 10); at = round(5.1 + .022 * k, 3)
        mn += [oval(x, y, 20, 14, "#efe6d2", at=at, fx="pop"), dot(x + 18, y - 7, 6, "#cbbca8", at)]
    mn += [label(500, 1290, "37 sheep and goats", 6.0, BONE, 32), glow(840, 400, 110, 6.1, .8, "sun"), dot(840, 400, 34, "#ffd27a", 6.1), label(840, 480, "a day", 6.3, "#ffd27a", 32)]
    menu = {"base": "dark", "cam": [1, 500, 860], "els": mn}
    # a title in a tomb: overseer of the side of the pyramid
    py = {"k": "pyramid", "x": 600, "y": 1150, "w": 560, "courses": False, "in": 1.4, "fx": "rise", "op": .9}
    ax_, ay_ = 600 + 560 * .18 * .35, 1150 - 560 * .636
    tt = [box(110, 1250, 180, 100, "#8a6a4a", "#d8b98e", 2, 10, .3, fx="fill"), box(175, 1282, 50, 68, "#2a1f16", r=4, at=.6), py,
          line([[320, 1150], [ax_, ay_]], 2.6, "#ffcf8a", 8, dur=1.0), glow((320 + ax_) / 2, (1150 + ay_) / 2, 90, 3.0, .6),
          line([[120, 1150], [320, 1150]], 1.4, "#8a6a48", 3, draw=False), person(225, 1150, 150, 3.4), glow(225, 1075, 120, 3.6, .5),
          label(600, 1265, "overseer of the side", 3.8, AMBER, 32),
          ring(225, 1080, 100, 5.4, AMBER, 3)]
    title = {"base": "dark", "cam": [1.2, 500, 1040], "els": tt}
    # the bones, retimed to the words, and a splint: somebody kept that arm still
    s6 = copy.deepcopy(ep["shots"][6])
    for e in s6["els"]:
        if e.get("k") == "poly":
            e["in"] = .4
        elif e.get("k") == "circle":
            e["in"] = 4.0
        elif e.get("k") == "label" and "splint" in e.get("t", ""):
            e["in"] = 4.4
        elif e.get("k") == "label":
            e["in"] = 5.0
        elif e.get("k") == "cap":
            e["in"] = .2
    s6["els"] += [box(420, 760, 170, 12, "#a0784c", "#d8b98e", 1.5, 4, 6.2, fx="pop"), box(420, 852, 170, 12, "#a0784c", "#d8b98e", 1.5, 4, 6.3, fx="pop")]
    s6["els"] += [line([[440 + 40 * j, 750], [440 + 40 * j, 874]], 6.6 + .1 * j, "#efe6d2", 3, dur=.3) for j in range(4)] + [glow(505, 815, 200, 7.8, .55)]
    s6["els"] += [box(792 + (3 if k in (2, 3) else 0), 660 + 34 * k, 54, 24, "#e8dcc6", "#fff6e6", 1.2, 8, round(2.8 + .08 * k, 2), fx="pop") for k in range(6)]
    s6["cam"] = [1.3, 500, 820]
    # bread, beer and beef; and the open edge: when did work begin?
    food = [oval(330, 1310, 46, 26, "#d9a560", "#8a5a2a", 2, at=.8, fx="pop"), line([[300, 1300], [312, 1290]], .9, "#8a5a2a", 2, draw=False), line([[330, 1298], [342, 1288]], .9, "#8a5a2a", 2, draw=False),
            {"k": "poly", "p": [[470, 1270], [530, 1270], [520, 1340], [480, 1340]], "fill": "#b0714a", "c": "#e0b08a", "w": 2, "in": 1.2, "fx": "pop"}] + _cow(670, 1305, 1.6)
    food += question(640, 760, 7.4, 80)
    # the plateau views, re-centred on their panels (the iso origin moved so the aimed point sits mid-panel)
    h0 = copy.deepcopy(ep["shots"][0])
    for e in h0["els"]:
        if e.get("k") == "iso":
            e.update(x=round(e["x"] + 500 - h0["cam"][1], 1), y=round(e["y"] + 900 - h0["cam"][2], 1))
        elif e.get("k") == "glow":
            e.update(y=900)
    h0["cam"] = [3.0, 500, 900]
    p1 = copy.deepcopy(ep["shots"][1])
    for e in p1["els"]:
        if e.get("k") == "iso":
            e["x"] = e["x"] + 165
        elif e.get("k") == "label":
            e.update(x=500, y=1300)
    p1["cam"] = [1, 500, 880]
    return remix(ep, scenes={0: h0, 1: p1, 3: menu, 5: title, 6: s6}, adds={7: food})




# ---------------------------------------------------------------- small drawn props
def tv(x, y, w=300, i=.2):
    h = w * .72
    return [{"k": "rect", "x": x - w / 2, "y": y - h / 2, "w": w, "h": h, "r": 26, "fill": "#2a231c", "c": "#c9ad85", "sw": 3, "in": i},
            {"k": "rect", "x": x - w * .42, "y": y - h * .38, "w": w * .7, "h": h * .76, "r": 18, "fill": "#3d5566", "c": "#9fd0ff", "sw": 1.5, "in": i},
            {"k": "sphinx", "x": x - w * .07, "y": y + h * .22, "w": w * .5, "in": i + .1},
            {"k": "circle", "x": x + w * .38, "y": y - h * .18, "r": 10, "fill": "#8c7152", "c": "#c9ad85", "w": 1, "in": i},
            {"k": "circle", "x": x + w * .38, "y": y + h * .05, "r": 10, "fill": "#8c7152", "c": "#c9ad85", "w": 1, "in": i}]


def rain(x0, x1, y0, y1, n=70, i=.2):
    return {"k": "rays", "x0": x0, "x1": x1, "y0": y0, "y1": y1, "n": n, "spread": .12, "c": "#b9d6e8", "in": i, "fx": "draw", "dur": 1.6}


def wall_face(x, y, w, h, fissures=True, rounded=True):
    """An enclosure wall seen face-on: alternating hard and soft beds, the soft ones cut back into rounded recesses."""
    els = [{"k": "rect", "x": x, "y": y, "w": w, "h": h, "fill": "#a88a64", "c": "rgba(255,236,206,.5)", "sw": 1.5}]
    n = 7
    for i in range(n):
        yy = y + h * (i + .5) / n
        if i % 2:
            els.append({"k": "poly", "p": [[x, yy - 26], [x + w, yy - 26], [x + w, yy + 26], [x, yy + 26]], "fill": "#7d6448", "c": "none", "w": 0})
            if rounded:
                els.append({"k": "line", "p": [[x + j * w / 10, yy - 20 + (8 if j % 2 else -6)] for j in range(11)], "curve": True, "c": "#5a4632", "w": 2, "op": .7})
        els.append({"k": "line", "p": [[x, yy + 27], [x + w, yy + 27]], "c": "#e7cfa6", "w": 1.4, "op": .45})
    if fissures:
        for j, fx in enumerate((.18, .43, .67, .86)):
            els.append({"k": "line", "p": [[x + w * fx, y + 6], [x + w * (fx + .01), y + h * .3], [x + w * (fx - .01), y + h * .6], [x + w * fx, y + h * .92]], "curve": True, "c": "#3a2c1e", "w": 3.5, "op": .85, "id": f"fis{j}"})
    return els


# ---------------------------------------------------------------- 05.05 The Sphinx and the Rain
def sphinx_erosion():
    s0 = sphinx_side("night"); s0["cam"] = [1.3, 470, 930]
    s0["els"] += [rain(-200, 1200, 200, 1300, 110, .2), {"k": "label", "x": 500, "y": 700, "t": "rain, in the desert?", "st": "ital", "c": "#cfe6ff", "in": 1.0}]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": wall_face(120, 440, 760, 720) + [{"k": "cap", "x": 500, "y": 390, "t": "the Sphinx enclosure wall", "in": .2},
          {"k": "label", "x": 500, "y": 1230, "t": "rounded recesses · deep vertical fissures", "in": .8}]}
    s2 = like(s1, add=[rain(160, 840, 440, 1150, 40, .1)] + [{"k": "line", "p": [[120 + 760 * fx, 446], [120 + 760 * fx, 1150]], "c": "#9fd0ff", "w": 2.4, "op": .7, "in": .5 + i * .15, "fx": "draw"} for i, fx in enumerate((.18, .43, .67, .86))] +
               [{"k": "label", "x": 500, "y": 1280, "t": "Schoch: rainwater running down the rock for millennia", "st": "small", "c": "#cfe6ff", "in": 1.2}])
    tl, ax = timeline(-10000, 0, [(-10000, "10,000 BCE"), (-7500, "7500"), (-5000, "5000"), (-2500, "2500"), (0, "1 CE")], "When was it carved?", y=900)
    tl["els"] += [{"k": "band", "x0": ax.x(-7000), "x1": ax.x(-5000), "y": 760, "h": 18, "c": "#9fd0ff", "op": .55, "t": "Schoch, 1992", "in": .4},
                  {"k": "band", "x0": ax.x(-2560), "x1": ax.x(-2490), "y": 660, "h": 18, "c": AMBER, "t": "Khafre · the usual date", "in": 1.0},
                  {"k": "band", "x0": ax.x(-3000), "x1": ax.x(0), "y": 980, "h": 10, "c": "#c9ad85", "op": .45, "t": "", "in": 1.5},
                  {"k": "label", "x": ax.x(-1500), "y": 1030, "t": "Egypt mostly dry, as today", "st": "small", "c": "#cbbca8", "in": 1.6}]
    s3 = tl
    salt = [{"k": "poly", "p": [[500 + (i % 7) * 50 - 150 + (i // 7) * 13, 690 + (i // 7) * 58 + (i % 3) * 8], [512 + (i % 7) * 50 - 150 + (i // 7) * 13, 678 + (i // 7) * 58 + (i % 3) * 8],
                                [524 + (i % 7) * 50 - 150 + (i // 7) * 13, 690 + (i // 7) * 58 + (i % 3) * 8], [512 + (i % 7) * 50 - 150 + (i // 7) * 13, 702 + (i // 7) * 58 + (i % 3) * 8]],
             "fill": "#f7f3ea", "c": "#ffffff", "w": 1, "in": .6 + i * .03} for i in range(21)]
    s4 = like(s1, add=[{"k": "arrow", "p": [[x, 1180], [x, 1000]], "c": "#9fd0ff", "w": 2.6, "in": .2, "fx": "draw"} for x in (220, 400, 600, 780)] + salt +
               [{"k": "label", "x": 500, "y": 1260, "t": "groundwater rises, dries, salt crystals split the soft beds", "st": "small", "c": "#e9dccb", "in": 1.4}])
    s4["els"] = [e for e in s4["els"] if not (e.get("k") == "label" and "rounded" in e.get("t", ""))]
    s5 = sphinx_side("dawn", w=520, x=580)
    s5["els"] += [{"k": "block", "x": 110, "y": 1060, "w": 150, "h": 70, "in": .3, "t": "Sphinx Temple", "ly": 110},
                  {"k": "arrow", "p": [[430, 1050], [330, 1010], [260, 1000]], "curve": True, "c": AMBER, "w": 2.6, "in": .8, "fx": "draw"},
                  {"k": "label", "x": 420, "y": 1130, "t": "core blocks cut from the Sphinx ditch", "st": "small", "c": AMBER, "in": 1.2}]
    s6 = sphinx_side("night"); s6["els"] += [{"k": "q", "x": 500, "y": 780, "size": 70, "in": .6, "fx": "pop"}]
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE GREAT SPHINX][sfx:boom][act:setting it up, unhurried]A ^geologist looked at the Sphinx... [act:quietly amazed][tune:fall]and saw ^*rain*.",
                      "[d:tension][cam:1.12|0|0.04][act:a puzzle, raising the stakes]In a desert@noun that's been ^dry for five ^thousand years."], cut=False),
        B("world", 1, ["[d:calm][k:1990 · ROBERT SCHOCH][act:plain, a respectful introduction]Robert Schoch, a Boston University geologist, studied the ^walls of the ^pit the Sphinx sits in.",
                       "[d:build][go:2|2.2][act:describing it, a careful eye][tune:level]^Rounded ^grooves. [act:same careful eye][tune:level]^Deep vertical ^cracks. [sfx:shimmer][act:sympathetic, his view][tune:fall]To ^him, that's what ^*rainwater* does@verb, over thousands of years."]),
        B("collision", 3, ["[d:build][k:HIS DATE][act:stating his claim, even]So he dated the carving to [stamp:7000–5000 BCE|gold]^seven thousand, to ^five thousand BCE. [act:the implication, weighty]^Long before the pharaohs."]),
        B("cost", 4, ["[d:build][k:THE OTHER SIDE][act:the other side, crisp]^Other geologists answered: ^*salt*. [act:explaining, step by step]^Groundwater seeps into this soft, layered limestone, dries out, and the crystals ^*burst* the stone.",
                      "[d:list][act:simple, matter of fact][tune:fall]No ancient rains ^needed."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:turning the page, curious][tune:rise]And the ^archaeology? [act:revealing, clear]The ^temple in front of the Sphinx is built from blocks cut out of the ^*same* pit.",
                          "[d:reveal][sfx:hit][act:connecting the dots, confident]And that temple fits into King ^Khafre's building works."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:fair, sincere]Schoch's ^observation is ^real. [act:turning, measured][tune:rise]His ^date? [act:the verdict, level-headed][tune:fall]Still ^*awaiting* evidence.",
                     "[d:tension][p:0.93][cam:1.12|0|0.04][act:thoughtful, quieter]Rock ^can't tell ^time... [act:a hopeful lift]unless something ^*dated* turns up in the pit."]),
    ]
    return EP("sphinx-erosion", "05.05", "The Sphinx and the Rain", "sphinx-erosion", "unsupported", "Older than Khafre, carved by rain?", "It saw *rain*.", beats, shots,
              "Schoch 1992, KMT · Gauri et al. 1995, Geoarchaeology · Reader 2001, Archaeometry · Lehner 1992, Cambridge Archaeological Journal",
              "Geologist Robert Schoch read rain erosion in the Sphinx enclosure and dated it to 7000–5000 BCE. Salt, the temple blocks and the dates that answer him.",
              ["#Sphinx", "#Giza", "#Geology", "#AncientEgypt", "#Archaeology"])


def sphinx_erosion_m():
    """The Sphinx and the Rain as one continuous take: a timeline with his rain and the usual date, a temple built from the pit, a clock that cannot be read."""
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, ring, strike, question, BLUE, BONE, AMBER, LILAC
    ep = sphinx_erosion()
    X = lambda yr: round(120 + (yr + 10000) / 10000 * 760, 1)
    tl = [line([[120, 900], [880, 900]], .2, BONE, 3, dur=1.0)] + [line([[X(v), 890], [X(v), 910]], .4, BONE, 2, draw=False) for v in (-10000, -7500, -5000, -2500, 0)]
    tl += [label(120, 955, "10,000 BCE", .5, "#cbbca8", 28, "start"), label(X(-5000), 955, "5000", .5, "#cbbca8", 28), label(880, 955, "1 CE", .5, "#cbbca8", 28, "end")]
    tl += [box(X(-7000), 730, X(-5000) - X(-7000), 22, BLUE, r=11, at=1.0, fx="pop"), label((X(-7000) + X(-5000)) / 2, 795, "Schoch", 1.3, BLUE, 32),
           {"k": "rays", "x0": X(-7000), "x1": X(-5000), "y0": 470, "y1": 715, "n": 30, "spread": .12, "c": "#b9d6e8", "in": 1.5, "fx": "draw", "dur": 1.2}]
    tl += [line([[X(-2530), 900], [X(-2530), 820]], 2.6, AMBER, 3, dur=.4), dot(X(-2530), 900, 11, AMBER, 2.6), label(X(-2530), 795, "Khafre", 2.8, AMBER, 32),
           box(X(-3000), 858, 880 - X(-3000), 14, "#c9ad85", r=7, at=3.4, op=.6, fx="fill"), label(760, 1010, "dry, as today", 3.6, "#cbbca8", 28)]
    tl += [arrow([[X(-2530), 1090], [X(-5000), 1090]], 4.4, AMBER, 3, "known", .8, False), arrow([[X(-5000), 1090], [X(-7000), 1090]], 5.1, BLUE, 3, "inferred", .6, False),
           label(500, 1160, "2,500 to 4,500 years earlier", 5.6, BONE, 30)]
    tline = {"base": "dark", "cam": [1.12, 500, 830], "els": tl}
    # the temple: blocks lifted out of the pit, their beds matching the pit walls; Khafre's pyramid behind; one project
    beds = ["#c8a978", "#8a6a4a", "#c8a978"]
    tp = [line([[40, 1000], [470, 1000]], 0, "#8a6a48", 3, draw=False), line([[40, 1150], [960, 1150]], 0, "#8a6a48", 3, draw=False),
          {"k": "sphinx", "x": 720, "y": 1150, "w": 380, "in": .2}]
    for j, c in enumerate(beds):
        tp += [box(470, 1000 + 50 * j, 50, 50, c, r=0, at=.3), box(910, 1000 + 50 * j, 50, 50, c, r=0, at=.3)]
    tp += [label(715, 1215, "the pit", .6, "#cbbca8", 28),
           box(80, 960, 340, 190, "none", "#f5ecdc", 2, 6, 1.4, style="claimed"),
           arrow([[640, 1110], [500, 930], [425, 985]], 2.0, AMBER, 3, "known", 1.0)]
    order = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2)]
    for k, (cx, rw) in enumerate(order):
        tp.append(box(90 + 80 * cx, 1090 - 60 * rw, 76, 56, beds[(cx + rw) % 3], "#3a2c1e", 1.5, 3, round(2.6 + .1 * k, 2), fx="pop"))
    tp += [label(250, 1215, "the temple", 3.0, "#cbbca8", 28)]
    tp += [line([[210, 1062], [470, 1075]], 4.4, "#ffe2a8", 2.5, "inferred", .6), line([[290, 1002], [470, 1125]], 4.8, "#ffe2a8", 2.5, "inferred", .6),
           ring(495, 1075, 34, 5.2, "#ffe2a8", 3, dur=.5), ring(210, 1062, 34, 5.4, "#ffe2a8", 3, dur=.5)]
    tp += [{"k": "pyramid", "x": 300, "y": 860, "w": 300, "courses": False, "in": 7.4, "fx": "rise"}, label(300, 905, "Khafre", 7.8, AMBER, 30),
           line([[250, 958], [300, 915]], 8.3, AMBER, 3, dur=.5),
           box(70, 640, 880, 640, "none", AMBER, 3, 22, 10.0, fx="draw", dur=1.6)]
    temple = {"base": "dark", "cam": [1.05, 500, 960], "els": tp}
    # the verdict: a question over the date; weathering as a poor clock; a dated fire would answer it
    verdict = question(500, 780, 2.6, 80)
    clock = [ring(760, 480, 50, .3, BONE, 3), line([[760, 480], [760, 446]], .6, BONE, 4, dur=.3), line([[760, 480], [786, 496]], .8, BONE, 4, dur=.3),
             glow(200, 1035, 70, 4.4, .8, "lamp"), dot(200, 1045, 9, "#2a1f16", 4.4), ring(200, 1045, 30, 4.7, AMBER, 3, dur=.5)]
    return remix(ep, scenes={3: tline, 5: temple}, adds={6: verdict}, line_adds={(5, 1): (clock, None)})


# ---------------------------------------------------------------- 05.07 The Sphinx Surveys
def sphinx_surveys():
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": tv(500, 690, 380) + [{"k": "num", "x": 500, "y": 1010, "t": "33 million", "u": "viewers · NBC · 1993", "in": .6, "fx": "pop", "size": 84}]}
    tl, ax = timeline(1975, 2000, [(1975, "1975"), (1980, "1980"), (1985, "1985"), (1990, "1990"), (1995, "1995"), (2000, "2000")], "Surveys at the Sphinx", y=1000)
    ev = [(1978, "SRI", "USA", 0), (1987, "Waseda", "Japan", 1), (1991, "Dobecki & Schoch", "USA", 2), (1992, "Marzouk & Gharib", "Egypt", 3), (1996, "Florida State", "USA", 4)]
    for i, (yv, t, sub, row) in enumerate(ev):
        tl["els"] += event(ax, yv, t, y=1000, row=row, i=.3 + i * .3, sub=sub)
    s1 = tl
    gy = 1000; m = 860 / 73.0; X = lambda xm: round(70 + xm * m, 1); Y = lambda dm: round(gy - dm * m, 1)
    sec = {"base": "section", "tod": "night", "ground": gy, "layers": [{"d": 0, "c": "#8a6d4d"}, {"d": 120, "c": "#4e3e30"}],
           "els": [{"k": "sphinx", "x": 500, "y": gy, "w": 860}]}
    s2 = like(dict(sec, cam=[1.1, 500, 960]), add=[{"k": "fan", "x": X(x), "y": gy, "a0": 60, "a1": 120, "r": 160, "n": 9, "in": .2 + i * .3} for i, x in enumerate((-2, 20, 45, 70))])
    s3 = like(dict(sec, cam=[1.6, X(40), Y(-3)]), add=[{"k": "line", "p": [[X(40), Y(0)], [X(40), Y(-6)]], "c": BONE, "w": 3, "in": .2, "fx": "draw"},
                                                         {"k": "circle", "x": X(40), "y": Y(-6.8), "r": 10, "fill": "rgba(245,236,220,.15)", "c": BONE, "w": 1.6, "in": 1.0},
                                                         {"k": "label", "x": X(40), "y": Y(-9.4), "t": "1998 · natural cavity", "st": "small", "in": 1.2}])
    s4 = like(s3, cam=[1.2, 500, 960], add=[{"k": "cap", "x": 500, "y": 560, "t": "no further drilling", "c": RED, "in": .3}])
    patches = [{"k": "rect", "x": 140 + i * 90, "y": 990 - (i % 2) * 8, "w": 70, "h": 22 + (i % 3) * 6, "fill": "#cdb48e", "c": "#fff3de", "sw": 1, "in": .3 + i * .1} for i in range(8)]
    s5 = like(sphinx_side("day", w=720, x=500, pyramid=False), add=patches + [{"k": "label", "x": 500, "y": 1150, "t": "modern patching of a crumbling statue", "st": "small", "in": 1.2}])
    s6 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 290, "y": 560, "w": 420, "h": 460, "r": 12, "fill": "#e9dcc4", "c": "#fff6e6", "sw": 2, "in": .1},
          {"k": "glyphs", "x": 330, "y": 620, "w": 340, "h": 320, "rows": 9, "cols": 6, "kind": "latin", "c": "#6b5640", "in": .3},
          {"k": "title", "y": 1110, "t": "publish the raw data", "st": "ital", "in": .8, "fx": "type"}]}
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:NBC · 1993][sfx:boom][act:big opener, a touch of awe]Thirty-three ^million people watched a TV show say the Sphinx was ^*thousands* of years older.",
                      "[d:tension][act:darker, slower]Then came the ^fight... [act:the real stakes][tune:fall]over who gets to ^*look*."], cut=False),
        B("world", 1, ["[d:calm][k:THE SURVEYS][act:plain, laying out the facts]Between {1978|nineteen seventy-eight} and {1996|nineteen ninety-six}, at least ^*five* teams scanned the ground around the Sphinx.",
                       "[d:list][go:2|2.2][sfx:shimmer][act:counting them off, crisp][tune:level]^American. [act:same beat][tune:level]^Japanese. [act:same beat, closing][tune:fall]^Egyptian. [act:then the tools, lightly][tune:fall]^Radar, and ^seismic."]),
        B("collision", 3, ["[d:build][k:1998][act:building, precise]In {1998|nineteen ninety-eight}, Egypt allowed ^one test drill, into a spot the radar had ^flagged. [sfx:hit][act:plain, deflating][tune:fall]A ^*natural* cavity.",
                           "[d:tension][go:4|2][act:flat, final][tune:fall]After that: ^no more drilling."]),
        B("cost", 4, ["[d:build][k:THE CHARGE][act:fair, giving the critics' case]Critics say access got ^harder once the old-Sphinx idea got ^famous. [act:pressing the point, even]And that the survey@noun data was ^never fully ^*released*."], cut=False),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:turning it, calmly]But the record@noun shows outside teams ^*were* let in, ^again and again.",
                          "[d:reveal][act:their side, evenly]And the authorities argue the Sphinx is ^crumbling. [sfx:hit][act:serious, weighing it]^Every drill hole is a ^*risk*."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Tight ^control? [act:plainly, no fuss][tune:fall]^Yes. [act:same measure][tune:rise]A ^cover-up? [act:the verdict, level-headed][tune:fall]No ^evidence of one.",
                     "[d:tension][p:0.93][act:practical, warm]The fix is ^simple. [act:firm, friendly][tune:fall]^*Publish* the raw data."]),
    ]
    return EP("sphinx-surveys", "05.07", "The Sphinx Surveys", "sphinx-surveys", "unsupported", "Was research shut down?", "Who gets to *look*?", beats, shots,
              "Dobecki & Schoch 1992, Geoarchaeology · Hawass & Lehner 1997, NOVA · Hawass 1998, The Secrets of the Sphinx",
              "Five surveys, one test drill and a TV special watched by 33 million. What the record shows about access to the Sphinx.",
              ["#Sphinx", "#Giza", "#AncientEgypt", "#Archaeology", "#History"])


def sphinx_surveys_m():
    """The Sphinx Surveys as one continuous take: thirty-three million viewers, a gate that closes, a locked data file, and the raw data handed out."""
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, ring, strike, tri, question, person, BLUE, BONE, AMBER, RED, LILAC
    ep = sphinx_surveys()
    # a TV special and its 33 million viewers; then a fence: who gets to look?
    tvs = tv(500, 540, 340, .3)
    tvs += [person(180 + 64 * (k % 11), 880 + 90 * (k // 11), 56, round(1.0 + .04 * k, 2)) for k in range(33)]
    tvs += [label(500, 770, "33 million", 2.7, AMBER, 44, st="big"),
            {"k": "sphinx", "x": 500, "y": 1360, "w": 300, "in": 5.4},
            line([[230, 1215], [770, 1215]], 6.0, RED, 4, dur=.8)] + [line([[x, 1185], [x, 1245]], 6.2, RED, 4, dur=.2) for x in (230, 500, 770)]
    tvs += question(840, 1330, 7.6, 80)
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": tvs}
    # after 1998: no more drilling; access harder; the data never fully released
    gt = [line([[250, 360], [200, 560]], .2, "#cbbca8", 4, draw=False), line([[250, 360], [300, 560]], .2, "#cbbca8", 4, draw=False),
          line([[250, 380], [250, 600]], .3, BONE, 4, dur=.5), strike(150, 600, 350, 380, .9), label(420, 480, "no more drilling", 1.1, RED, 30, "start")]
    gt += [{"k": "sphinx", "x": 210, "y": 880, "w": 260, "in": 2.0},
           box(380, 700, 18, 180, "#8c7152", r=3, at=2.2, fx="fill"), box(620, 700, 18, 180, "#8c7152", r=3, at=2.2, fx="fill"),
           line([[398, 760], [620, 760]], 3.4, RED, 6, dur=.6), line([[398, 820], [620, 820]], 3.6, RED, 6, dur=.6)]
    gt += [person(700 + 70 * k, 880, 110, round(2.6 + .15 * k, 2)) for k in range(3)]
    gt += [box(380 + 22 * k, 990 + 22 * k, 220, 260, "#e9dcc4", "#fff6e6", 2, 8, round(4.4 + .15 * k, 2), fx="pop") for k in range(3)]
    gt += [line([[440 + 4 * j, 1080 + 40 * i + 12 * ((j % 4) - 1.5)] for j in range(40)], 4.9 + .1 * i, "#3d5566", 2, dur=.5, curve=True) for i in range(4)]
    gt += [box(360, 970, 300, 340, "none", LILAC, 3, 14, 5.6, style="claimed", fx="draw"), label(510, 1360, "never fully released", 5.9, LILAC, 30)]
    gt += question(820, 1150, 7.6, 80)
    gate = {"base": "dark", "cam": [1, 500, 860], "els": gt}
    # the fix: tight control yes, cover-up no evidence; publish the raw data, and anyone can check the echoes
    pb = [{"k": "sphinx", "x": 500, "y": 740, "w": 440, "in": .2}, ring(500, 680, 250, .5, AMBER, 3, "inferred", 1.0),
          box(260, 520, 480, 260, "rgba(201,193,238,.12)", LILAC, 3, 12, 1.1, style="claimed"), strike(260, 780, 740, 520, 1.7)]
    pb += [box(380, 900, 240, 280, "#e9dcc4", "#fff6e6", 2, 8, 4.8, fx="pop")]
    pb += [line([[400 + 5 * j, 960 + 50 * i + 14 * math.sin(j * (1.1 + .3 * i))] for j in range(40)], 5.1 + .15 * i, "#3d5566", 2.2, dur=.5, curve=True) for i in range(4)]
    for k, x in enumerate((140, 310, 500, 690, 860)):
        pb += [arrow([[500, 1185], [x, 1270]], round(5.9 + .12 * k, 2), AMBER, 2.5, "known", .4, False), person(x, 1400, 100, round(6.1 + .12 * k, 2))]
    pub = {"base": "dark", "cam": [1, 500, 880], "els": pb}
    # the record: teams let in, again and again; a crumbling statue patched; a drill hole as a risk
    import copy
    s5 = copy.deepcopy(ep["shots"][5])
    k5 = 0
    for e in s5["els"]:
        if e.get("k") == "rect" and e.get("in", -1) > 0:
            e["in"] = round(5.6 + .1 * k5, 2); k5 += 1
        elif e.get("k") == "label" and "patching" in e.get("t", ""):
            e["in"] = 6.6
    s5["els"] += [person(180 + 70 * k, 1330, 90, round(.6 + .25 * k, 2)) for k in range(5)] + [arrow([[500, 1290], [560, 1040]], 1.9, AMBER, 3, "known", .5, False)]
    s5["els"] += [line([[620, 820], [620, 975]], 7.2, RED, 5, dur=.6), ring(620, 985, 30, 7.7, RED, 3, dur=.4)]
    return remix(ep, scenes={0: s0, 4: gate, 5: s5, 6: pub})


# ---------------------------------------------------------------- 05.08 The Osiris Shaft
def osiris_shaft():
    gy = 520; m = 20.0                                     # 20 px per metre; about 30 m down
    X = lambda xm: round(500 + xm * m, 1); Y = lambda dm: round(gy + dm * m, 1)
    sec = {"base": "section", "tod": "night", "ground": gy, "lx": 40, "far": [[860, 170]],
           "layers": [{"d": 0, "c": "#6f5a43", "t": "bedrock under Khafre's causeway", "ty": 30}, {"d": 400, "c": "#4b3c2f"}], "water": 27.5 * m, "waterT": "groundwater", "waterX": 820,
           "els": [{"k": "rect", "x": -200, "y": gy - 24, "w": 1400, "h": 24, "fill": "#b39a78", "c": "#f2dcb4", "sw": 1.2, "id": "causeway"},
                   {"k": "label", "x": 250, "y": gy - 40, "t": "causeway", "st": "small"}]}
    L1 = {"k": "poly", "p": [[X(-2), Y(0)], [X(2), Y(0)], [X(2), Y(9)], [X(-2), Y(9)]], "fill": "#0d0b09", "c": BONE, "w": 1.6, "id": "l1"}
    L2 = {"k": "poly", "p": [[X(-9), Y(9)], [X(9), Y(9)], [X(9), Y(13)], [X(-9), Y(13)]], "fill": "#0d0b09", "c": BONE, "w": 1.6, "id": "l2"}
    S2 = {"k": "poly", "p": [[X(-1.4), Y(13)], [X(1.4), Y(13)], [X(1.4), Y(25)], [X(-1.4), Y(25)]], "fill": "#0d0b09", "c": BONE, "w": 1.6, "id": "s2"}
    L3 = {"k": "poly", "p": [[X(-8), Y(25)], [X(8), Y(25)], [X(8), Y(30)], [X(-8), Y(30)]], "fill": "#0d0b09", "c": BONE, "w": 1.6, "id": "l3"}
    boxes2 = [{"k": "box3d", "x": X(x), "y": Y(12.8), "w": 44, "h": 30, "d": 20, "id": f"b2{i}"} for i, x in enumerate((-8, -5, 4, 6.5))]
    isl = [{"k": "water", "y": Y(28.6), "h": Y(30) - Y(28.6), "x0": X(-8), "x1": X(8), "op": .9, "id": "moat"},
           {"k": "rect", "x": X(-3), "y": Y(28.4), "w": 6 * m, "h": 1.6 * m, "fill": "#6f5a43", "c": BONE, "sw": 1, "id": "island"},
           {"k": "box3d", "x": X(-1.6), "y": Y(28.4), "w": 60, "h": 34, "d": 26, "tone": "#4a4040", "light": "#6f6060", "id": "sarc"}] + \
          [{"k": "rect", "x": X(px) - 6, "y": Y(25.2), "w": 12, "h": 3.2 * m, "fill": "#8c7152", "c": "#c9ad85", "sw": 1, "id": f"pil{j}"} for j, px in enumerate((-3.6, 3.2))]
    base = [L1, L2, S2, L3] + boxes2 + isl
    s0 = like(dict(sec, cam=[3.2, X(0), Y(27.6)]), add=base + [{"k": "glow", "x": X(0), "y": Y(28), "r": 120, "kind": "lamp", "in": .1, "op": .8}])
    s1 = like(dict(sec, cam=[1.05, 500, 860]), add=base + [{"k": "dim", "x1": X(10.5), "y1": Y(0), "x2": X(10.5), "y2": Y(30), "t": "c. 30 m", "lx": 30, "in": .5},
                                                          {"k": "label", "x": X(-12), "y": Y(4.5), "t": "level 1", "st": "small", "a": "end", "in": .3},
                                                          {"k": "label", "x": X(-12), "y": Y(11.5), "t": "level 2", "st": "small", "a": "end", "in": .5},
                                                          {"k": "label", "x": X(-12), "y": Y(28), "t": "level 3", "st": "small", "a": "end", "in": .7}])
    from iso3d import osiris_block, lab as _lab
    s1b = {"base": "dark", "stars": 50, "cam": [1, 500, 880], "els": [{"k": "glow", "x": 500, "y": 900, "r": 480, "kind": "lamp", "op": .14},
           {"k": "iso", "x": 545, "y": 560, "s": 17, "az": -32, "spin": 2.2, "el": .36, "items": osiris_block() + [
               dict(_lab(-2.5, -5, "level 1", z=0), st="lab", a="end"), dict(_lab(-9.5, -11, "level 2 · coffins", z=0), st="lab", a="end"),
               dict(_lab(-8.5, -28, "level 3 · water", z=0), st="lab", a="end")]},
           {"k": "label", "x": 500, "y": 1380, "t": "c. 30 m down · proportions simplified", "st": "small", "in": .8}]}
    s2 = like(s1, cam=[2.6, X(0), Y(11)], add=[{"k": "label", "x": X(0), "y": Y(8), "t": "stone coffins · bones · amulets", "st": "small", "c": GOLD, "in": .4}])
    s3 = like(s1, cam=[3.0, X(0), Y(27.4)], add=[{"k": "glow", "x": X(0), "y": Y(28), "r": 110, "kind": "lamp", "in": .2, "op": .7},
                                                 {"k": "label", "x": X(0), "y": Y(24.4), "t": "granite sarcophagus on a rock island", "st": "small", "c": GOLD, "in": .5}])
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": tv(500, 760, 380) + [{"k": "cap", "x": 500, "y": 1020, "t": "live on Fox · 2 March 1999", "in": .6}]}
    tl, ax = timeline(-3000, 0, [(-3000, "3000 BCE"), (-2000, "2000"), (-1000, "1000"), (0, "1 CE")], "What was found, and when", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-2589), "x1": ax.x(-2503), "y": 880, "h": 16, "c": "#c9ad85", "t": "pyramids built", "in": .3},
                  {"k": "band", "x0": ax.x(-1550), "x1": ax.x(-1070), "y": 780, "h": 16, "c": AMBER, "t": "level 3, by its style", "in": .7},
                  {"k": "band", "x0": ax.x(-664), "x1": ax.x(-525), "y": 680, "h": 16, "c": GOLD, "t": "level 2 burials", "in": 1.1},
                  {"k": "band", "x0": ax.x(-3000), "x1": ax.x(-1550), "y": 580, "h": 12, "c": "#9fd0ff", "op": .35, "t": "cut earlier? no dates", "in": 1.5}]
    s5 = tl
    osir = [{"k": "rect", "x": 250, "y": 520, "w": 500, "h": 640, "fill": "rgba(111,182,214,.35)", "c": "#9fd0ff", "sw": 2, "in": .2},
            {"k": "rect", "x": 330, "y": 600, "w": 340, "h": 480, "fill": "#6f5a43", "c": BONE, "sw": 1.6, "in": .4}] + \
           [{"k": "rect", "x": 360 + (i % 2) * 230, "y": 640 + (i // 2) * 88, "w": 40, "h": 40, "fill": "#b39a78", "c": "#f2dcb4", "sw": 1, "in": .6 + i * .04} for i in range(10)]
    s6 = {"base": "plan", "north": [900, 330], "cam": [1, 500, 860], "els": osir + [{"k": "cap", "x": 500, "y": 460, "t": "the Osireion, Abydos · c. 1290 BCE", "in": .1},
          {"k": "label", "x": 500, "y": 1220, "t": "a granite hall on an island, ringed by water", "st": "small", "in": 1.1}]}
    s7 = like(s3, cam=[2.2, X(0), Y(26)], add=[{"k": "q", "x": X(0), "y": Y(21.5), "size": 60, "in": .5, "fx": "pop"}])
    shots = [s0, s1b, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:UNDER GIZA][sfx:boom][act:hushed, a strange scene]Thirty metres under Giza, a granite ^coffin sits on an ^island... [act:wonder, slowly][tune:fall]*surrounded by ^water*."], cut=False),
        B("world", 1, ["[d:calm][k:THE OSIRIS SHAFT][act:plain guide, unhurried]Between the Sphinx and Khafre's pyramid, a ^shaft drops through the bedrock, in ^three levels.",
                       "[d:build][go:2|2][act:taking us down, calm]The ^middle level: stone ^coffins, ^bones, ^amulets. [go:3|2][act:lower, quieter, deeper]The ^bottom: a granite sarcophagus, on a rock island, ringed by ^groundwater."]),
        B("collision", 4, ["[d:build][k:1999][act:building, a bit of showbiz]Zahi Hawass's team pumped it ^dry, and ^opened it... [act:amused, a showman's flourish][tune:risefall]^live@adj!, on American TV.",
                           "[d:list][go:5|0][act:plain fact, confident]He dated the bottom level to the New ^Kingdom. [act:letting the gap sink in]More than a ^*thousand* years after the pyramids."]),
        B("cost", 5, ["[d:build][k:THE CHALLENGE][act:fair, voicing the critics][tune:fall]Critics ask: why so ^little published? [act:genuinely open, curious][tune:rise]And couldn't the shaft be much ^*older* than the things found in it?"], cut=False),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:conceding, sincere]That's a ^fair point. [act:explaining, clear]Objects@noun date when a shaft was ^*used@verb*, not when it was ^cut.",
                          "[d:reveal][go:6|0][sfx:hit][act:the counterweight, firm]But ^every find in it is ^Egyptian. [act:warmer, a nice discovery]And its island design has a dated ^twin at Abydos: the ^Osireion."], cut=False),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]^Older than the pyramids? [act:the verdict, even][tune:fall]No ^evidence yet.",
                     "[d:tension][p:0.93][cam:1.12|0|0.04][act:practical, a little eager]^One radiocarbon date would tell us a ^*lot@amount* more."]),
    ]
    return EP("osiris-shaft", "05.08", "The Osiris Shaft", "osiris-shaft", "unsupported", "Older than its dates?", "A coffin on an *island*.", beats, shots,
              "Hawass 2007, in Essays in Honor of David B. O'Connor · Hassan 1932–60, Excavations at Gîza · Frankfort 1933, The Cenotaph of Seti I",
              "A granite sarcophagus on a rock island, 30 metres under Khafre's causeway. What was found in the Osiris Shaft, and what is still undated.",
              ["#Giza", "#OsirisShaft", "#AncientEgypt", "#Archaeology", "#Mystery"])


def osiris_shaft_m():
    """The Osiris Shaft as one continuous take: pumped dry on live TV, a timeline with a gap and a question, a phone in a cellar, an hourglass of carbon."""
    from mural import remix
    from illus import line, arrow, glow, label, dot, box, ring, strike, question, oval, tri, BLUE, BONE, AMBER, RED, LILAC, GREEN
    ep = osiris_shaft()
    gy = 520; m = 20.0
    Xs = lambda xm: round(500 + xm * m, 1); Ys = lambda dm: round(gy + dm * m, 1)
    # 1999: on a TV screen the bottom level is pumped dry and opened, live
    t = [box(270, 460, 460, 340, "#2a231c", "#c9ad85", 3, 26, .1), box(300, 490, 360, 280, "#1d2a33", "#9fd0ff", 1.5, 16, .1),
         dot(705, 560, 10, "#8c7152", .1), dot(705, 620, 10, "#8c7152", .1),
         box(310, 650, 340, 110, "#4b3c2f", r=6, at=.2), box(310, 680, 340, 80, "rgba(111,182,214,.75)", r=4, at=.3), box(420, 690, 120, 70, "#6f5a43", "#f2dcb4", 1, 2, .4),
         {"k": "box3d", "x": 445, "y": 690, "w": 64, "h": 36, "d": 22, "tone": "#4a4040", "light": "#6f6060", "in": .5},
         line([[330, 720], [330, 520], [200, 430]], 1.4, "#c9ad85", 5, dur=.8), box(130, 380, 70, 60, "#8c7152", "#c9ad85", 2, 8, 1.4, fx="pop"),
         box(310, 680, 110, 80, "#4b3c2f", r=2, at=2.3, fx="fill"), box(540, 680, 110, 80, "#4b3c2f", r=2, at=2.5, fx="fill"),
         box(440, 640, 80, 12, "#6f6060", "#9a8a8a", 1, 2, 3.3, fx="rise"),
         line([[450, 460], [410, 400]], 4.0, "#c9ad85", 3, draw=False), line([[550, 460], [590, 400]], 4.0, "#c9ad85", 3, draw=False)]
    t += [ring(500, 420, r, 4.2 + .25 * j, RED, 3, dur=.4) for j, r in enumerate((30, 55, 80))] + [label(500, 880, "live · 1999", 4.6, RED, 34)]
    tv99 = {"base": "dark", "cam": [1.3, 450, 720], "els": t}
    # the timeline: pyramids, then the bottom level more than a thousand years later; could the cutting be older?
    X = lambda yr: round(120 + (yr + 3000) / 3000 * 760, 1)
    tl = [line([[120, 760], [880, 760]], .2, BONE, 3, dur=1.0)] + [line([[X(v), 750], [X(v), 770]], .4, BONE, 2, draw=False) for v in (-3000, -2000, -1000, 0)]
    tl += [label(120, 810, "3000 BCE", .5, "#cbbca8", 28, "start"), label(X(-2000), 810, "2000", .5, "#cbbca8", 28), label(X(-1000), 810, "1000", .5, "#cbbca8", 28), label(880, 810, "1 CE", .5, "#cbbca8", 28, "end")]
    tl += [box(X(-1550), 700, X(-1070) - X(-1550), 20, AMBER, r=10, at=3.6, fx="pop"), label((X(-1550) + X(-1070)) / 2, 670, "bottom level", 3.9, AMBER, 30)]
    tl += [{"k": "pyramid", "x": X(-2550), "y": 745, "w": 70, "courses": False, "in": 5.6, "fx": "rise"}, label(X(-2550), 670, "pyramids", 5.8, "#f2dcb4", 30)]
    tl += [arrow([[X(-2500), 580], [X(-1560), 580]], 6.1, BONE, 3, "known", .7, False), label((X(-2500) + X(-1560)) / 2, 545, "1,000 + years", 6.4, BONE, 30)]
    tl += [arrow([[X(-1560), 860], [X(-3000) + 10, 860]], 9.4, LILAC, 3, "claimed", 1.0, False), label(X(-2300), 915, "cut earlier?", 10.4, LILAC, 32)]
    tl += [dot(X(-1300), 760, 10, AMBER, 14.2), label(X(-1300), 915, "used", 14.4, AMBER, 30)]
    tl += [line([[180, 1090], [820, 1090]], 16.0, "#8a6a48", 3, draw=False), box(360, 1090, 280, 250, "rgba(77,62,48,.6)", "#cbbca8", 2, 4, 16.3, style="inferred"),
           box(486, 1290, 28, 46, "#1a1511", "#9fd0ff", 2, 6, 17.4, fx="pop"), box(490, 1296, 20, 30, "#3d5566", r=3, at=17.5), glow(500, 1300, 70, 17.6, .7, "blue"),
           label(500, 1395, "lately", 18.2, "#9fd0ff", 30)]
    tl += question(255, 1230, 19.6, 70)
    tline = {"base": "dark", "cam": [1, 500, 880], "els": tl}
    osi = [label(500, 470, "Osireion · Abydos", 4.4, AMBER, 34), label(500, 1290, "c. 1290 BCE", 5.6, "#cbbca8", 30)]
    q7 = question(Xs(0), Ys(21.5), 1.0, 70)
    hx = 880
    hg = [oval(hx, 600, 26, 14, GREEN, at=2.2, fx="pop"), line([[hx, 614], [hx, 650]], 2.2, GREEN, 3, dur=.3),
          {"k": "poly", "p": [[hx - 50, 690], [hx + 50, 690], [hx, 770]], "fill": "rgba(232,184,122,.25)", "c": BONE, "w": 3, "in": 4.0, "fx": "draw", "dur": .5},
          {"k": "poly", "p": [[hx, 770], [hx + 50, 850], [hx - 50, 850]], "fill": "rgba(232,184,122,.25)", "c": BONE, "w": 3, "in": 4.1, "fx": "draw", "dur": .5},
          {"k": "poly", "p": [[hx - 24, 710], [hx + 24, 710], [hx, 748]], "fill": AMBER, "c": "none", "w": 0, "in": 4.3},
          {"k": "poly", "p": [[hx, 820], [hx + 32, 850], [hx - 32, 850]], "fill": AMBER, "c": "none", "w": 0, "in": 4.6, "fx": "fill"},
          line([[hx, 770], [hx, 820]], 4.5, AMBER, 2, dur=.6),
          dot(Xs(-6.5), Ys(29.2), 9, "#2a1f16", 6.0), ring(Xs(-6.5), Ys(29.2), 26, 6.1, AMBER, 3, dur=.4),
          arrow([[Xs(-6.5) + 10, Ys(29.2) - 30], [640, 960], [hx - 40, 870]], 6.4, AMBER, 3, "inferred", .9)]
    return remix(ep, scenes={4: tv99, 5: tline}, adds={6: osi, 7: q7}, line_adds={(5, 1): (hg, [1.05, 500, 900])})


# ---------------------------------------------------------------- stars (J2000, degrees) for Orion
ORI = {"Alnitak": (85.19, -1.94), "Alnilam": (84.05, -1.20), "Mintaka": (83.00, -0.30), "Betelgeuse": (88.79, 7.41), "Rigel": (78.63, -8.20),
       "Bellatrix": (81.28, 6.35), "Saiph": (86.94, -9.67), "Meissa": (83.78, 9.93)}


def sky_xy(ra, dec, cx=500, cy=760, s=34.0, ra0=84.05, dec0=-1.2):
    """Sky as seen facing south: east (larger RA) to the left, north up."""
    return [round(cx - (ra - ra0) * math.cos(math.radians(dec)) * s, 1), round(cy - (dec - dec0) * s, 1)]


def fit_belt(P):
    """Similarity transform taking Alnitak to Khufu and Mintaka to Menkaure. It needs the sky turned about 165 degrees,
       nearly upside down; Alnilam then lands a few tens of metres from Khafre's centre (with these rounded positions)."""
    from scenes import GP
    def star(n):
        ra, dec = ORI[n]; return complex(-(ra - 84.05) * math.cos(math.radians(dec)), (dec + 1.2))
    kh = complex(*GP["khufu"][0]); mk = complex(*GP["menkaure"][0])
    a, c = star("Alnitak"), star("Mintaka")
    k = (mk - kh) / (c - a); t = kh - k * a
    out = {}
    for n in ("Alnitak", "Alnilam", "Mintaka"):
        z = k * star(n) + t; out[n] = P(z.real, z.imag)
    return out


def orion():
    pl, P = giza_plan(scale=.8, cx=500, cy=800)
    pl["els"] = [e for e in pl["els"] if not str(e.get("id", "")).startswith(("gal", "town", "wall"))]
    pl["base"] = "plan"; pl["bg"] = "#1c1814"
    st = fit_belt(P)
    stars = [{"k": "glow", "x": x, "y": y, "r": 60, "kind": "lamp", "in": .3 + i * .25, "op": .9} for i, (x, y) in enumerate(st.values())] + \
            [{"k": "circle", "x": x, "y": y, "r": 7, "fill": "#fff6e6", "c": "#ffffff", "w": 1, "in": .3 + i * .25} for i, (x, y) in enumerate(st.values())]
    s0 = like(pl, cam=[1.25, 330, 690], add=stars)
    lab = [{"k": "label", "x": P(0, 150)[0], "y": P(0, 150)[1], "t": "Khufu", "in": .2}, {"k": "label", "x": P(-348, -210)[0], "y": P(-348, -210)[1], "t": "Khafre", "in": .35},
           {"k": "label", "x": P(-581, -660)[0], "y": P(-581, -660)[1], "t": "Menkaure", "in": .5}]
    s1 = like(pl, cam=[1.2, 330, 690], add=lab)
    s2 = like(s1, add=stars + [{"k": "label", "x": x + 26, "y": y + 46, "t": n, "st": "small", "a": "start", "c": GOLD, "in": 1.0} for n, (x, y) in st.items()])
    sky = {"base": "sky", "tod": "night", "ground": 1180, "sun": False, "cam": [1, 500, 860], "els": []}
    fig = [("Betelgeuse", "Alnitak"), ("Bellatrix", "Mintaka"), ("Alnitak", "Saiph"), ("Mintaka", "Rigel"), ("Alnitak", "Alnilam"), ("Alnilam", "Mintaka"), ("Betelgeuse", "Meissa"), ("Meissa", "Bellatrix")]
    Q = {n: sky_xy(*ORI[n], cy=720, s=30) for n in ORI}
    sky["els"] += [{"k": "line", "p": [Q[a], Q[b]], "c": "#a99cf0", "w": 1.4, "op": .6, "in": .3} for a, b in fig] + \
                  [{"k": "circle", "x": q[0], "y": q[1], "r": 6 if n in ("Betelgeuse", "Rigel") else 4.5, "fill": "#fff6e8", "c": "none", "w": 0, "in": .2} for n, q in Q.items()] + \
                  [{"k": "pyramid", "x": 520, "y": 1180, "w": 300, "courses": False}, {"k": "pyramid", "x": 300, "y": 1190, "w": 260, "courses": False, "cap": .1},
                   {"k": "cap", "x": 500, "y": 330, "t": "Orion · Sah, to the Egyptians", "in": .6}]
    s3 = like(sky, add=[{"k": "cap", "x": 500, "y": 390, "t": "c. 10,500 BCE · the belt at its lowest", "c": GOLD, "in": .3}], cam=[1, 500, 900])
    s3["els"] = [e for e in s3["els"] if "Sah" not in str(e.get("t", ""))]
    s4 = like(s2, cam=[1.2, 330, 690], add=[{"k": "cap", "x": 330, "y": 330, "t": "only with the sky turned upside down", "c": RED, "in": .3}])
    a = P(0, 0); b = P(-581, -738); ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    s5 = like(s2, cam=[1.35, 330, 690], add=[{"k": "line", "p": [a, b], "c": "#f2dcb4", "w": 2, "style": "inferred", "in": .2},
                                             {"k": "line", "p": [st["Alnitak"], [st["Alnitak"][0] + math.cos(math.radians(ang + 10)) * 560, st["Alnitak"][1] + math.sin(math.radians(ang + 10)) * 560]], "c": GOLD, "w": 2, "in": .6},
                                             {"k": "label", "x": 330, "y": 1130, "t": "belt angle in 10,500 BCE: off by c. 10°", "c": GOLD, "in": 1.0}])
    tl, ax = timeline(-2620, -2480, [(-2600, "2600 BCE"), (-2560, "2560"), (-2520, "2520"), (-2480, "2480")], "Three kings, one after another", y=1000)
    tl["els"] += [{"k": "band", "x0": ax.x(-2589), "x1": ax.x(-2566), "y": 900, "h": 18, "c": AMBER, "t": "Khufu", "in": .3},
                  {"k": "band", "x0": ax.x(-2558), "x1": ax.x(-2532), "y": 800, "h": 18, "c": AMBER, "t": "Khafre", "in": .6},
                  {"k": "band", "x0": ax.x(-2530), "x1": ax.x(-2503), "y": 700, "h": 18, "c": AMBER, "t": "Menkaure", "in": .9},
                  {"k": "label", "x": 500, "y": 1150, "t": "reign dates approximate", "st": "small", "c": "#b9aa97"}]
    s6 = tl
    from iso3d import plateau, plateau_labels
    s7 = plateau(extra=plateau_labels(town=False), az=-160, spin=1.0)
    Q2 = {n: sky_xy(*ORI[n], cx=590, cy=330, s=22) for n in ORI}
    s7["els"] = [{"k": "line", "p": [Q2[a], Q2[b]], "c": "#a99cf0", "w": 1.4, "op": .55, "layer": "far"} for a, b in fig] + \
                [{"k": "circle", "x": q[0], "y": q[1], "r": 5 if n in ("Betelgeuse", "Rigel") else 3.8, "fill": "#fff6e8", "c": "none", "w": 0, "layer": "far"} for n, q in Q2.items()] + s7["els"]
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:GIZA FROM ABOVE][sfx:boom][act:slow, a riddle][tune:level]Three ^pyramids. [act:the rhyme, landing it][tune:fall]Three ^stars.",
                      "[d:tension][sfx:shimmer][cam:1.12|0|0][act:curious, pulling them in][tune:rise]Is Giza a ^*map* of Orion's Belt?"], cut=False),
        B("world", 1, ["[d:calm][k:1989 · ROBERT BAUVAL][act:plain, respectful]Robert Bauval noticed the ^pattern. [act:describing it, carefully]Two big pyramids in ^line... [act:pointing to the odd one][tune:fall]the ^third, small and ^*offset*.",
                       "[d:wonder][go:2|2.2][sfx:shimmer][act:wonder, lightly]Just like the ^belt stars."]),
        B("collision", 3, ["[d:build][k:10,500 BCE][act:building, even-handed]With Graham Hancock, he went ^further: the layout matches the sky of about ten thousand, ^five hundred BCE. [act:softer, the romance of it]A memory of a ^lost age."]),
        B("cost", 4, ["[d:build][k:THE CHECK][act:brisk, matter of fact]^Astronomers checked. [act:light, a small smile]The match ^only works if you turn the sky *upside ^down*.",
                      "[d:list][go:5|2][act:precise, adding it up]And in that year, the belt's ^angle misses the pyramids by about ^*ten* degrees."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:plain, confident]The records@noun point to ^three kings, building one after another, over about ^seventy years.",
                          "[d:wonder][go:7|0][act:warmer, generous][tune:fall]But ^one thing is ^true. [act:sincere, with care]Egypt's kings ^*did* look to Orion. [act:gently, the old name]They called it ^Sah... [act:soft wonder, respectful][tune:fall]and hoped to ^join it."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Star ^symbolism? [act:fair, open][tune:fall]^Plausible. [act:same measure][tune:rise]A ^map of ten thousand BCE? [act:the verdict, level-headed][tune:fall]Still ^*awaiting* evidence.",
                     "[d:tension][p:0.93][cam:1.1|0|-0.05][act:warm, an invitation]Look ^up tonight. [gap:0.4][act:quiet wonder, the last word][tune:fall]Orion is still ^*there*."], cut=False),
    ]
    return EP("orion", "05.10", "The Orion Correlation", "orion-correlation", "unsupported", "A map of the sky in 10,500 BCE?", "Three pyramids. *Three stars*.", beats, shots,
              "Bauval 1989, Discussions in Egyptology · Krupp 1997, Sky & Telescope · Fairall 1999, Astronomy & Geophysics · Spence 2000, Nature",
              "The three Giza pyramids look like Orion's Belt. The case for a sky map of 10,500 BCE, and the checks astronomers ran.",
              ["#Orion", "#Giza", "#Pyramids", "#Astronomy", "#AncientEgypt"])


# ---------------------------------------------------------------- 05.11 Sacred Measures
def metrology():
    cx, gy = 500, 1050
    earth = [{"k": "circle", "x": 500, "y": 780, "r": 330, "fill": "rgba(111,182,214,.14)", "c": "#9fd0ff", "w": 2, "id": "earth"}] + \
            [{"k": "line", "p": [[500 - 330 * math.cos(math.radians(a)), 780 - 330 * math.sin(math.radians(a))], [500 + 330 * math.cos(math.radians(a)), 780 - 330 * math.sin(math.radians(a))]], "c": "#9fd0ff", "w": 1, "op": .35} for a in (-60, -30, 0, 30, 60)]
    py = {"k": "pyramid", "x": 500, "y": 780, "w": 520, "courses": True, "depth": .04, "turn": .12, "id": "py"}
    s0 = {"base": "dark", "stars": 80, "cam": [1.1, 500, 780], "els": earth + [dict(py, **{"in": .2})] + [{"k": "num", "x": 500, "y": 1240, "t": "× 43,200", "in": .6, "fx": "pop", "size": 80}]}
    sec = [{"k": "poly", "p": [[240, gy], [500, gy - 331], [760, gy]], "fill": "url(#k-blocks)", "c": "#f2dcb4", "w": 2, "id": "tri"},
           {"k": "dim", "x1": 800, "y1": gy, "x2": 800, "y2": gy - 331, "t": "146.6 m", "lx": 28},
           {"k": "dim", "x1": 240, "y1": gy + 40, "x2": 760, "y2": gy + 40, "t": "230.3 m", "ly": 40}]
    s1 = {"base": "dark", "cam": [1.05, 500, 900], "els": sec + [
        {"k": "label", "x": 500, "y": 540, "t": "height × 43,200 = 6,333 km", "in": .3}, {"k": "label", "x": 500, "y": 585, "t": "polar radius 6,357 km · 0.4% off", "st": "small", "c": "#9fd0ff", "in": .6},
        {"k": "label", "x": 500, "y": 1210, "t": "perimeter × 43,200 = 39,806 km", "in": .9}, {"k": "label", "x": 500, "y": 1255, "t": "equator 40,075 km · 0.7% off", "st": "small", "c": "#9fd0ff", "in": 1.2}]}
    tri = [{"k": "poly", "p": [[260, 1100], [760, 1100], [760, 464]], "fill": "rgba(242,201,142,.1)", "c": GOLD, "w": 2.4, "in": .2, "fx": "draw"},
           {"k": "dim", "x1": 800, "y1": 1100, "x2": 800, "y2": 464, "t": "1 cubit = 7 palms up", "lx": 30, "in": .6},
           {"k": "dim", "x1": 260, "y1": 1140, "x2": 760, "y2": 1140, "t": "5½ palms across", "ly": 44, "in": .9},
           {"k": "label", "x": 330, "y": 1070, "t": "51.84°", "c": GOLD, "in": 1.2}]
    s2 = {"base": "dark", "cam": [1.05, 520, 820], "els": tri + [{"k": "cap", "x": 500, "y": 390, "t": "the seked: how Egyptians set a slope", "in": .1}]}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "title", "y": 640, "t": "perimeter ÷ height", "st": "serif", "in": .1},
          {"k": "title", "y": 760, "t": "= 44 ÷ 7 = 6.286", "st": "serif", "in": .6, "c": GOLD},
          {"k": "title", "y": 880, "t": "2π = 6.283", "st": "serif", "in": 1.1, "c": "#9fd0ff"},
          {"k": "label", "x": 500, "y": 1000, "t": "for a pyramid of any size, at this slope", "in": 1.5},
          {"k": "iso", "x": 500, "y": 450, "s": .95, "az": -20, "spin": 4, "el": .4, "in": .1, "items": [
              {"t": "pyr", "x": 0, "z": 0, "y": 0, "b": 230.3, "h": 146.6, "c": "#e2c79c"},
              {"t": "line", "p": [[-115.2, .5, -115.2], [115.2, .5, -115.2], [115.2, .5, 115.2], [-115.2, .5, 115.2], [-115.2, .5, -115.2]], "c": GOLD, "w": 3},
              {"t": "line", "p": [[0, 0, 0], [0, 146.6, 0]], "c": "#9fd0ff", "w": 2.4, "style": "inferred"}]}]}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "circle", "x": 500, "y": 780, "r": 300, "c": "#9fd0ff", "w": 3, "in": .1, "fx": "draw"},
          {"k": "line", "p": [[500, 780], [800, 780]], "c": GOLD, "w": 3, "in": .6, "fx": "draw"}, {"k": "label", "x": 650, "y": 760, "t": "r", "st": "ital", "c": GOLD, "in": .8},
          {"k": "title", "y": 1180, "t": "circumference ÷ radius = 2π", "st": "serif", "in": 1.0}]}
    s5 = stat("43,200", "", "the only free number: chosen after the fact, and the best fit for height and for base are not the same number", None)
    v = View(28.5, 35, 23.6, 31.8, (60, 330, 880, 900))
    ax_, ay_ = v.p(29.92, 31.2); sx_, sy_ = v.p(32.90, 24.09)
    s6 = {"base": "map", "cam": [1, 500, 860], "els": [{"k": "map", "land": v.land(), "rivers": [v.line(__import__("scenes").NILE)]},
          {"k": "pin", "x": ax_, "y": ay_, "t": "Alexandria", "in": .2}, {"k": "pin", "x": sx_, "y": sy_, "t": "Syene (Aswan)", "a": "end", "lx": -18, "in": .5},
          {"k": "cap", "x": 500, "y": 1230, "t": "Eratosthenes · c. 240 BCE", "in": .9}]}
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE GREAT PYRAMID][sfx:boom][act:a magic trick, setting it up]Multiply the Great Pyramid by ^forty-three thousand, two ^hundred... [act:the reveal, playful wonder][tune:fall]and you get the ^*Earth*."], cut=False),
        B("world", 1, ["[d:calm][k:THE CLAIM][act:laying out the claim, fair]The ^height, scaled up, lands within half a percent of the Earth's ^polar radius. [act:the second fact, same measure]The ^base, within one percent of the ^equator.",
                       "[d:build][act:posing the riddle, slowly]^Coincidence... [act:leaning in, playful][tune:fall]or a ^message in ^*stone*?"]),
        B("collision", 2, ["[d:build][k:THE SLOPE][act:bright, the clue]Here's the ^key. [act:explaining, patient]Egyptians set a slope with a ^*seked*: five and a half palms across, for every cubit ^up.",
                           "[d:list][go:3|0][act:the neat bit, precise]That slope gives a pyramid whose ^perimeter, divided by its height, is almost exactly two ^pi. [sfx:hit][act:a small flourish][tune:highfall]At ^*any* size."]),
        B("cost", 4, ["[d:build][act:turning to it, curious][tune:rise]And the ^Earth? [act:deadpan, obvious][tune:fall]It's ^round. [act:the click, satisfied][tune:fall]Its circumference divided by its radius is two pi ^*too*."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:narrowing it down, clear]So the ^only thing left to explain is the ^number@count itself. [act:slowly, spelling it out][tune:fall]^Forty-three thousand, two ^hundred.",
                          "[d:reveal][sfx:hit][act:the reveal, lower]And that number@count was ^*chosen*... [act:quiet, pointed][tune:fall]^after the fact."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, warm][tune:rise]^Brilliant builders? [act:wholehearted, warm][tune:highfall]^Absolutely. [act:same measure][tune:rise]The Earth's size in ^stone? [act:the verdict, careful][tune:fall]No Egyptian ^text shows they ^*knew* it.",
                     "[d:tension][p:0.93][act:a gentle twist, storytelling]The ^first known measurement came over two ^thousand years later. [act:savouring it]From a ^Greek... [act:the name, with relish][tune:fall]named ^*Eratosthenes*."]),
    ]
    return EP("sacred-measures", "05.11", "Sacred Measures", "sacred-metrology", "unsupported", "Is the Earth built into the pyramid?", "Multiply it by *43,200*.", beats, shots,
              "Petrie 1883, The Pyramids and Temples of Gizeh · Rossi 2004, Architecture and Mathematics in Ancient Egypt · Imhausen 2016, Mathematics in Ancient Egypt",
              "At 1:43,200 the Great Pyramid matches the northern hemisphere within 1%. The seked, 2π and the number that was chosen after the fact.",
              ["#GreatPyramid", "#Mathematics", "#Pi", "#AncientEgypt", "#History"])


# ---------------------------------------------------------------- 05.12 Granite Drill Cores
def drill_cores():
    core = {"k": "core", "x": 500, "y": 1060, "w": 190, "h": 420, "grooves": 11, "id": "core"}
    lamp = {"k": "glow", "x": 500, "y": 820, "r": 420, "kind": "lamp", "op": .35}
    s0 = {"base": "dark", "floor": 1062, "cam": [1.45, 500, 860], "els": [lamp, dict(core, **{"in": .1})]}
    s1 = {"base": "dark", "floor": 1062, "cam": [1.05, 500, 860], "els": [lamp, core,
          {"k": "dim", "x1": 660, "y1": 1060, "x2": 660, "y2": 640, "t": "c. 11 cm", "lx": 30, "in": .4},
          {"k": "cap", "x": 500, "y": 470, "t": "core 7 · Petrie Museum UC16036", "in": .2},
          {"k": "label", "x": 500, "y": 1150, "t": "collected by Flinders Petrie at Giza, 1880s", "st": "small", "in": .8}]}
    blk = [{"k": "block", "x": 220, "y": 1100, "w": 560, "h": 380, "d": 180, "in": .1},
           {"k": "poly", "p": [[420, 720], [500, 720], [500, 1000], [420, 1000]], "fill": "#2a2420", "c": "#fff3de", "w": 1.6, "in": .4},
           {"k": "line", "p": [[430, 740], [490, 750], [430, 770], [490, 780], [430, 800], [490, 810], [430, 840], [490, 850]], "c": "rgba(40,20,20,.7)", "w": 1.4, "in": .5},
           {"k": "line", "p": [[620, 720], [620, 1100]], "c": "#fff3de", "w": 2.4, "in": .8},
           {"k": "label", "x": 460, "y": 690, "t": "tube-drill hole", "st": "small", "in": .6}, {"k": "label", "x": 680, "y": 700, "t": "saw cut", "st": "small", "in": 1.0},
           {"k": "cap", "x": 500, "y": 440, "t": "Aswan granite · worked in the Old Kingdom", "in": .2}]
    s2 = {"base": "dark", "floor": 1100, "cam": [1, 500, 860], "els": blk}
    s3 = like(s0, cam=[1.6, 520, 820], add=[{"k": "dim", "x1": 640, "y1": 790, "x2": 640, "y2": 828, "t": "0.1 inch per turn?", "a": "start", "lx": 30, "upright": True, "c": GOLD, "in": .4},
                                            {"k": "label", "x": 500, "y": 540, "t": "Dunn, 1984: '500 times' a modern drill's feed", "c": GOLD, "in": 1.0}])
    mohs = [(3, "copper", "#d9894a"), (6, "feldspar (in granite)", "#c9ad85"), (7, "quartz sand", "#f5ecdc")]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "axis", "x0": 150, "x1": 850, "y": 1060, "ticks": [[150 + i * 70, str(i)] for i in range(11)], "t": "Mohs hardness", "in": .1}] +
          [{"k": "rect", "x": 150 + v * 70 - 30, "y": 1060 - v * 60, "w": 60, "h": v * 60, "fill": c, "c": "none", "sw": 0, "in": .3 + i * .3} for i, (v, n, c) in enumerate(mohs)] +
          [{"k": "label", "x": 150 + v * 70, "y": 1060 - v * 60 - 18, "t": n, "st": "small", "in": .4 + i * .3} for i, (v, n, c) in enumerate(mohs)]}
    grains = [{"k": "circle", "x": 438 + (j % 2) * 124 + (rnd - .5) * 6, "y": 700 + j * 24, "r": 5, "fill": "#f5ecdc", "c": "none", "w": 0, "in": .6 + j * .03} for j, rnd in enumerate([.1, .7, .3, .9, .5, .2, .8, .4, .6, .1, .9, .3, .7, .5])]
    s5 = {"base": "dark", "cam": [1.05, 500, 860], "els": [{"k": "rect", "x": 250, "y": 640, "w": 500, "h": 520, "fill": "#6d5a52", "c": "#c9b0a8", "sw": 1.4, "in": .1},
          {"k": "rect", "x": 430, "y": 520, "w": 14, "h": 520, "fill": "url(#k-copper)", "c": "none", "sw": 0, "in": .3},
          {"k": "rect", "x": 556, "y": 520, "w": 14, "h": 520, "fill": "url(#k-copper)", "c": "none", "sw": 0, "in": .3},
          {"k": "rect", "x": 444, "y": 640, "w": 112, "h": 400, "fill": "#8a766c", "c": "#c9b0a8", "sw": 1, "in": .3}] + grains +
          [{"k": "label", "x": 500, "y": 480, "t": "copper tube, turning", "st": "small", "c": "#e8b87a", "in": .4},
           {"k": "label", "x": 500, "y": 1210, "t": "sand grinds a ring; a core is left standing", "st": "small", "in": 1.2}]}
    drill = [{"k": "line", "p": [[380, 820], [640, 780]], "c": "url(#k-copper)", "w": 16, "in": .2},
             {"k": "line", "p": [[400, 818], [420, 815]], "c": "#8a4a22", "w": 18, "in": .2}] + \
            [{"k": "line", "p": [[450 + i * 26, 780], [462 + i * 26, 850]], "c": "#8a6a44", "w": 7, "op": .9, "in": .6 + i * .05} for i in range(6)]
    s6 = {"base": "dark", "cam": [1.35, 510, 820], "els": drill + [{"k": "glow", "x": 510, "y": 810, "r": 260, "kind": "lamp", "op": .35},
          {"k": "cap", "x": 510, "y": 640, "t": "copper drill with leather thong · Badari", "in": .6},
          {"k": "label", "x": 510, "y": 960, "t": "Naqada II · over a thousand years before Khufu", "st": "small", "in": 1.0}]}
    s7 = like(s0, cam=[1.25, 500, 860], add=[{"k": "q", "x": 660, "y": 820, "size": 60, "in": .6, "fx": "pop"}])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:CORE 7][sfx:boom][act:turning it over, intrigued]A granite ^core, cut at least four and a half ^thousand years ago... [act:the detail, hushed][tune:fall]with a ^*spiral groove*."], cut=False),
        B("world", 1, ["[d:calm][k:1880s · FLINDERS PETRIE][act:plain storytelling, fond]Flinders Petrie picked it up at ^Giza. [act:small, precise]^Eleven centimetres tall. [act:explaining, clear]The ^waste from a hole, ^*drilled* into granite.",
                       "[d:build][go:2|0][act:admiring, plain]Egypt's masons drilled and sawed the ^hardest stone they had."]),
        B("collision", 3, ["[d:build][k:THE MACHINE IDEA][act:giving his reading, fair]In {1984|nineteen eighty-four}, machinist Christopher Dunn read@past the groove as a ^drill biting a ^tenth of an inch per turn.",
                           "[d:tension][sfx:hit][act:reporting his verdict, even]^Impossible, he said, without ^power tools."]),
        B("cost", 4, ["[d:build][k:THE TEST][act:practical, the test]Then experimenters tried ^copper tubes, fed with ^sand. [act:the key fact, clear]^Quartz sand is ^*harder* than the feldspar in granite.",
                      "[d:list][go:5|0][act:explaining, easy][tune:level]The ^copper just ^carries it round. [act:the point, firm][tune:fall]The ^*sand* does@verb the cutting. [act:honest, drawn out]^Slow... [act:a satisfied nod][tune:fall]but it ^works. [act:a small grin][tune:fall]^Cores and all."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:leaning in, fresh news]And in {2025|twenty twenty-five}, researchers identified a copper ^drill from a grave far ^older than Khufu. [sfx:shimmer][act:wonder, softly]Its ^leather bow-string ^still wrapped around it."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]Lost ^machines? [act:firm, plain][tune:fall]No ^trace of one. [act:fairer, turning][tune:rise]That ^exact groove? [act:honest, open-ended][tune:fallrise]Not ^fully copied, yet.",
                     "[d:tension][p:0.93][act:warm, a challenge]Someone should ^try. [act:spelling out the recipe]With ^copper... [act:smiling, the last word][tune:fall]and ^*sand*."]),
    ]
    return EP("drill-cores", "05.12", "Granite Drill Cores", "granite-drill-cores", "unsupported", "Lost machines, or copper and sand?", "A *spiral* in granite.", beats, shots,
              "Petrie 1883, The Pyramids and Temples of Gizeh · Stocks 2003, Experiments in Egyptian Archaeology · Odler & Kmošek 2025, Egypt and the Levant",
              "Petrie's granite core 7 carries a spiral groove. Copper, sand and a 5,000-year-old drill answer the lost-machine idea.",
              ["#AncientEgypt", "#Granite", "#Archaeology", "#Engineering", "#Giza"])


# ---------------------------------------------------------------- 05.13 Egypt's Stone Vases
def stone_vases():
    vase = {"k": "vase", "x": 500, "y": 1060, "h": 420, "w": 330, "veins": True, "tone": "#8a8a90", "id": "v"}
    lamp = {"k": "glow", "x": 500, "y": 820, "r": 430, "kind": "lamp", "op": .35}
    s0 = {"base": "dark", "floor": 1062, "cam": [1.35, 500, 860], "els": [lamp, dict(vase, **{"in": .1})]}
    step = [{"k": "step", "x": 500, "y": 820, "w": 560, "h": 280, "n": 6, "in": .1},
            {"k": "rect", "x": 200, "y": 900, "w": 600, "h": 170, "fill": "#1a1411", "c": "#c9ad85", "sw": 1.4, "in": .3}] + \
           [{"k": "vase", "x": 230 + i * 34, "y": 1055 - (i % 2) * 70, "h": 58, "w": 42, "tone": ["#8a8a90", "#b89a78", "#6d7a70", "#a8604a"][i % 4], "in": .5 + i * .02} for i in range(17)]
    s1 = {"base": "dark", "cam": [1.05, 500, 880], "els": step + [{"k": "num", "x": 500, "y": 470, "t": "40,000+", "u": "stone vessels under Djoser's Step Pyramid", "in": .2, "fx": "pop", "size": 84}]}
    row = [{"k": "vase", "x": 190 + i * 155, "y": 1000, "h": 190 + (i % 2) * 50, "w": 120, "tone": c, "in": .2 + i * .15} for i, c in enumerate(["#3a3a3e", "#a8604a", "#6d7a70", "#c9b89a", "#8a8a90"])] + \
          [{"k": "label", "x": 190 + i * 155, "y": 1050, "t": n, "st": "small", "in": .3 + i * .15} for i, n in enumerate(["basalt", "granite", "diorite", "travertine", "schist"])]
    s2 = {"base": "dark", "floor": 1002, "cam": [1, 500, 880], "els": row}
    scan = [{"k": "line", "p": [[330, 1060 - j * 30], [670, 1060 - j * 30]], "c": "#9fd0ff", "w": 1.2, "op": .55, "in": .2 + j * .05} for j in range(14)]
    s3 = like(s0, cam=[1.2, 500, 860], add=scan + [{"k": "label", "x": 500, "y": 560, "t": "claimed: round to a thousandth of an inch", "c": "#cfe6ff", "in": 1.0}])
    grp = [{"k": "vase", "x": 250 + (i % 2) * 110, "y": 830 + (i // 2) * 250, "h": 150, "w": 100, "tone": "#8a8a90", "in": .2 + i * .1, "op": .8} for i in range(4)] + \
          [{"k": "vase", "x": 640 + (i % 2) * 110, "y": 830 + (i // 2) * 250, "h": 150, "w": 100, "tone": "#b89a78", "in": .6 + i * .1} for i in range(4)] + \
          [{"k": "rect", "x": 170, "y": 600, "w": 280, "h": 520, "fill": "none", "c": GOLD, "sw": 2, "style": "claimed", "in": .2},
           {"k": "rect", "x": 560, "y": 600, "w": 280, "h": 520, "fill": "none", "c": "#8fd9b0", "sw": 2, "in": .6},
           {"k": "label", "x": 310, "y": 580, "t": "bought · no find-spot", "st": "small", "c": GOLD, "in": .4},
           {"k": "label", "x": 700, "y": 580, "t": "excavated · recorded", "st": "small", "c": "#8fd9b0", "in": .8}]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp}
    pts_h = [[330 + (i * 37) % 110, 780 + (i * 53) % 150] for i in range(19)]
    pts_m = [[640 + (i * 29) % 90, 820 + (i * 41) % 90] for i in range(8)]
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 290, "y": 740, "w": 190, "h": 230, "r": 20, "fill": "rgba(143,217,176,.08)", "c": "#8fd9b0", "sw": 1.6, "style": "inferred", "in": .2},
          {"k": "rect", "x": 610, "y": 780, "w": 150, "h": 170, "r": 20, "fill": "rgba(159,208,255,.08)", "c": "#9fd0ff", "sw": 1.6, "style": "inferred", "in": .2},
          {"k": "label", "x": 385, "y": 720, "t": "handmade", "st": "small", "c": "#8fd9b0", "in": .3}, {"k": "label", "x": 685, "y": 760, "t": "machine-made", "st": "small", "c": "#9fd0ff", "in": .3}] +
          [{"k": "circle", "x": x, "y": y, "r": 7, "fill": "#f2c98e", "c": "none", "w": 0, "in": .6 + i * .04} for i, (x, y) in enumerate(pts_h)] +
          [{"k": "circle", "x": x, "y": y, "r": 7, "fill": "none", "c": "#9fd0ff", "w": 2, "in": .6} for x, y in pts_m] +
          [{"k": "cap", "x": 500, "y": 560, "t": "19 museum vases · npj Heritage Science 2025", "in": .1},
           {"k": "label", "x": 500, "y": 1080, "t": "gold dots: the museum vases", "st": "small", "c": GOLD, "in": 1.4}]}
    tool = [{"k": "line", "p": [[500, 480], [500, 960]], "c": "#8a6a44", "w": 12, "in": .1},
            {"k": "line", "p": [[500, 960], [450, 1010]], "c": "#8a6a44", "w": 9, "in": .2}, {"k": "line", "p": [[500, 960], [550, 1010]], "c": "#8a6a44", "w": 9, "in": .2},
            {"k": "poly", "p": [[420, 1012], [580, 1012], [560, 1040], [500, 1052], [440, 1040]], "fill": "#6d6660", "c": "#e9dccb", "w": 1.4, "curve": True, "in": .3},
            {"k": "circle", "x": 455, "y": 560, "r": 34, "fill": "#8c7152", "c": "#e9dccb", "w": 1.4, "in": .4}, {"k": "circle", "x": 545, "y": 560, "r": 34, "fill": "#8c7152", "c": "#e9dccb", "w": 1.4, "in": .4},
            {"k": "vase", "x": 500, "y": 1230, "h": 230, "w": 200, "tone": "#8a8a90", "in": .6},
            {"k": "cap", "x": 500, "y": 410, "t": "the stone-vessel drill, as Egyptians drew it", "in": .6},
            {"k": "label", "x": 640, "y": 1030, "t": "crescent stone borer", "st": "small", "a": "start", "in": 1.0},
            {"k": "label", "x": 600, "y": 520, "t": "weights", "st": "small", "a": "start", "in": 1.1}]
    s6 = {"base": "dark", "cam": [1, 500, 880], "els": tool}
    s7 = like(s0, cam=[1.2, 500, 860], add=[{"k": "num", "x": 500, "y": 520, "t": "c. 800", "u": "hours for one vessel · Stocks 2003", "in": .4, "fx": "pop", "size": 80}])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:PREDYNASTIC EGYPT][sfx:boom][act:an intriguing opener]^Stone jars over five ^thousand years old. [act:reporting the claim, even]So ^round, some say only a ^*lathe* could make them."], cut=False),
        B("world", 1, ["[d:calm][k:DJOSER'S STEP PYRAMID][act:plain, quietly astonished]Under ^one pyramid alone, archaeologists found more than *forty ^thousand* stone vessels.",
                       "[d:list][go:2|0][act:counting them off, crisp][tune:level]^Basalt. [act:same beat][tune:level]^Granite. [act:same beat, closing][tune:fall]^Diorite. [act:marvelling, softer][tune:fall]Some with walls as thin as ^*eggshell*."]),
        B("collision", 3, ["[d:build][k:2023 · THE SCANS][act:building, precise]Then engineers began ^3D-scanning them, and reported roundness to ^*thousandths* of an inch.",
                           "[d:tension][sfx:hit][act:reporting their claim, even]Too ^perfect@adj for ^hands, they said."]),
        B("cost", 4, ["[d:build][k:THE CATCH][act:the catch, careful]But most of those vases came from ^private collections. [act:ticking them off][tune:level]No ^find-spot. [act:same beat][tune:level]No ^proof they're ancient. [act:plain, no drama][tune:fall]And the antiquities market is full of ^*fakes*."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:leaning in, careful]In {2025|twenty twenty-five}, a ^peer-reviewed study scanned nineteen vases with a ^known museum history. [sfx:shimmer][act:the reveal, clear][tune:fall]Their surfaces matched ^*handmade* work.",
                          "[d:list][go:6|0][act:showing us, warm interest]And Egyptian art shows the tool: a ^weighted drill, with a ^crescent-shaped stone bit."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:the verdict, admiring]^Skill, ^patience, and around ^*eight hundred* hours per vessel.",
                     "[d:tension][p:0.93][act:a friendly challenge][tune:rise]Want to ^prove a lost machine? [act:practical, warm][tune:fall]Scan the vases that came out of the ^*ground*."]),
    ]
    return EP("stone-vases", "05.13", "The Stone Vases", "stone-vases", "unsupported", "Too perfect for human hands?", "Only a *lathe* could make them?", beats, shots,
              "Fomitchev-Zamilov 2025, npj Heritage Science · Stocks 2003, Experiments in Egyptian Archaeology · Lacau & Lauer 1959, La Pyramide à degrés",
              "Scans of Egypt's hard-stone vases set the internet alight. Where the precise ones came from, and what a peer-reviewed study found.",
              ["#AncientEgypt", "#StoneVases", "#Archaeology", "#LostTechnology", "#History"])


# ---------------------------------------------------------------- 05.14 The Serapeum Boxes
def serapeum():
    tun = corridor_view(500, 860, W=760, H=600, n=9, tone=(190, 170, 140))
    s0 = {"base": "dark", "cam": [1, 500, 880], "els": tun[:-2] + [{"k": "box3d", "x": 250, "y": 1110, "w": 300, "h": 170, "d": 120, "lid": True, "lidH": 60, "in": .3},
          {"k": "glow", "x": 330, "y": 1020, "r": 260, "kind": "lamp", "op": .5}]}
    gal = [{"k": "rect", "x": 470, "y": 380, "w": 60, "h": 860, "fill": "#1a1411", "c": "#c9ad85", "sw": 1.4, "in": .1}]
    for i in range(12):
        for side in (-1, 1):
            x = 470 - 120 if side < 0 else 530
            y = 410 + i * 68
            gal.append({"k": "rect", "x": x, "y": y, "w": 120, "h": 44, "fill": "#1a1411", "c": "#c9ad85", "sw": 1, "in": .2 + i * .04})
            if (i + (side > 0)) % 2 == 0 or i < 6:
                gal.append({"k": "rect", "x": x + 30, "y": y + 12, "w": 60, "h": 20, "fill": "#6f6660", "c": "#e9dccb", "sw": .8, "in": .5 + i * .04})
    from iso3d import shot as _iso, serapeum_vaults
    s1 = _iso(serapeum_vaults() + [{"t": "person", "x": 0, "y": 0, "z": 14, "h": 1.7}], cam=[1, 500, 880], s=17, x=500, y=1000, az=-38, spin=2.0, el=.46,
              table={"r": 16, "rz": 24, "grid": 4, "strata": [{"h": 1.5, "c": "#a8845c"}, {"h": 4, "c": "#8a6a4a"}]})
    s1["els"] += [{"k": "cap", "x": 500, "y": 330, "t": "the Greater Vaults · Saqqara", "in": .1},
                  {"k": "label", "x": 500, "y": 1420, "t": "a stretch of the galleries, roof removed · 24 boxes remain", "st": "small", "in": 1.0}]
    s2 = {"base": "dark", "floor": 1100, "cam": [1, 500, 880], "els": [{"k": "box3d", "x": 200, "y": 1100, "w": 480, "h": 260, "d": 190, "hollow": True, "in": .1},
          {"k": "person", "x": 820, "y": 1100, "h": 150, "t": "1.7 m", "in": .3},
          {"k": "dim", "x1": 200, "y1": 1150, "x2": 680, "y2": 1150, "t": "c. 3.85 m", "ly": 44, "in": .5},
          {"k": "label", "x": 440, "y": 690, "t": "box c. 38 t · lid c. 24 t", "c": GOLD, "in": .9}]}
    s3 = like(s2, cam=[2.2, 420, 830], add=[{"k": "rect", "x": 330, "y": 812, "w": 90, "h": 8, "fill": "#e9dccb", "c": "none", "sw": 0, "in": .3},
                                            {"k": "label", "x": 375, "y": 790, "t": "a 6-inch straightedge", "st": "small", "in": .6}])
    carts = [("Amasis II", "c. 570–526 BCE"), ("Cambyses II", "c. 525 BCE"), ("Khababash", "c. 336 BCE")]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [e for i, (n, d) in enumerate(carts) for e in (
          {"k": "rect", "x": 250, "y": 520 + i * 200, "w": 500, "h": 130, "r": 65, "fill": "rgba(242,201,142,.08)", "c": GOLD, "sw": 2.2, "in": .2 + i * .4},
          {"k": "label", "x": 500, "y": 585 + i * 200, "t": n, "st": "serif", "in": .3 + i * .4},
          {"k": "label", "x": 500, "y": 625 + i * 200, "t": d, "st": "small", "c": "#cbbca8", "in": .4 + i * .4})] +
          [{"k": "cap", "x": 500, "y": 440, "t": "names inscribed on the boxes", "in": .1}]}
    tl, ax = timeline(-1400, 0, [(-1400, "1400 BCE"), (-1000, "1000"), (-600, "600"), (-200, "200"), (0, "1 CE")], "Burials of the Apis bulls", y=1000)
    tl["els"] += [{"k": "band", "x0": ax.x(-1390), "x1": ax.x(-30), "y": 900, "h": 14, "c": "#c9ad85", "t": "c. 1,400 years of burials", "in": .3},
                  {"k": "band", "x0": ax.x(-664), "x1": ax.x(-30), "y": 780, "h": 18, "c": AMBER, "t": "Greater Vaults, from Psamtik I", "in": .8}]
    s5 = tl
    s6 = like(s2, cam=[1.05, 500, 880], add=[{"k": "line", "p": [[200 + j * 30, 1100], [260 + j * 30, 740]], "c": "#9fd0ff", "w": 1, "op": .5, "in": .2 + j * .03} for j in range(16)] +
              [{"k": "label", "x": 440, "y": 640, "t": "full 3D scans of all 24", "c": "#cfe6ff", "in": 1.0}])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:SAQQARA][sfx:boom][act:hushed, entering the dark]^Underground at Saqqara: two dozen stone ^boxes. [act:letting the weight land]Box and lid, up to ^*sixty* tonnes.",
                      "[d:tension][act:curious, pulling them in][tune:rise]Were they ^really made for ^*bulls*?"], cut=False),
        B("world", 1, ["[d:calm][k:THE SERAPEUM][act:guiding, calm]This is the ^Serapeum. [act:with care, explaining]The tomb of the ^Apis bulls, sacred animals of Memphis, buried here for about ^*fourteen hundred* years.",
                       "[d:build][go:2|0][act:laying it out, steady]In the Greater Vaults stand ^twenty-four granite and ^basalt boxes. [act:precise, impressed]One ^measured box and lid: about [count:62|tonnes]^sixty-two tonnes."]),
        B("collision", 3, ["[d:build][k:THE CLAIM][act:giving his side, fair]Engineer Christopher Dunn checked the ^insides with a straightedge and a ^square. [sfx:hit][act:reporting his words, even]^Flat, and square, like a ^machine shop, he said.",
                           "[d:tension][act:his conclusion, stated plainly][tune:fall]^Machine-made. [act:raising the stakes]And far ^older than the bulls."]),
        B("cost", 4, ["[d:build][k:THE RECORD][act:the counterweight, measured]But some boxes carry the ^names of ^kings. [act:reading them off, clear][tune:level]^Amasis. [act:same beat][tune:level]^Cambyses. [act:same beat, landing][tune:fall]^Khababash.",
                      "[d:list][go:5|0][act:dating it, precise]From the ^sixth to the ^fourth century BCE. [act:the click, a little delighted][tune:fall]^Right when the Greater Vaults were in ^use@noun!."]),
        B("reversal", 3, ["[d:reveal][k:THE TWIST][act:leaning in, skeptical][tune:rise]And the ^precision? [act:dry, precise][tune:fall]A ^few spot checks, with a ^*six-inch* straightedge. [act:plainly, a gentle point]^Never published as ^full measurements.",
                          "[d:list][act:calm, practical]^Hand lapping with sand can make granite ^that flat."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm][tune:rise]^Late Egyptian ^masterwork? [act:fair, confident][tune:fall]Most ^likely. [act:same measure][tune:rise]Something ^older? [act:the verdict, level-headed][tune:fall]Still ^awaiting evidence.",
                     "[d:tension][p:0.93][act:practical, a friendly push]Laser-scan ^all twenty-four. [act:quiet, certain][tune:fall]Then we'll ^*know*."]),
    ]
    return EP("serapeum", "05.14", "The Serapeum Boxes", "serapeum-boxes", "unsupported", "Tombs for bulls, or something older?", "Sixty tonnes. *For bulls*?", beats, shots,
              "Mariette 1857, Le Sérapéum de Memphis · Malinine, Posener & Vercoutter 1968 · Dodson 2005, in Divine Creatures",
              "Twenty-four granite and basalt boxes in the Serapeum at Saqqara. The machine claim, the royal names on them, and the test that would settle it.",
              ["#Serapeum", "#Saqqara", "#AncientEgypt", "#Archaeology", "#Mystery"])


# ---------------------------------------------------------------- 05.15 The Giza Power Plant
def power_plant():
    S = Section(s=3.6, cx=500, gy=1150)
    R = S.rooms(); body = S.body(); inner = S.els()
    shade = {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0}
    sky = {"base": "section", "tod": "night", "ground": 1150, "far": [[95, 220], [915, 110]], "layers": [{"d": 0, "c": "#6f5a43"}, {"d": 60, "c": "#4d3e30"}]}
    kc = S.P(R["kc"][0], R["kc"][1] + 3); qc = S.P(R["qc"][0], R["qc"][1] + 3)
    shafts = [{"k": "line", "p": [kc, S.P(R["kc"][0] + 60, 85)], "c": "#9fd0ff", "w": 1.6, "id": "ks"}, {"k": "line", "p": [kc, S.P(R["kc"][0] - 55, 81)], "c": "#9fd0ff", "w": 1.6, "id": "kn"},
              {"k": "line", "p": [qc, S.P(R["qc"][0] + 50, 60)], "c": "#9fd0ff", "w": 1.4, "id": "qs"}, {"k": "line", "p": [qc, S.P(R["qc"][0] - 50, 58)], "c": "#9fd0ff", "w": 1.4, "id": "qn"}]
    beam = {"k": "line", "p": [kc, [kc[0] + 700, kc[1] - 560]], "c": "#ffe2a8", "w": 6, "style": "claimed", "op": .9}
    s0 = dict(sky, cam=[1.6, 520, 960], els=[body, shade] + inner + [dict(beam, **{"in": .5, "fx": "draw"}), {"k": "glow", "x": kc[0], "y": kc[1], "r": 90, "kind": "lamp", "pulse": True, "in": .2}])
    s1 = dict(sky, cam=[2.1, 520, 1010], els=[body, shade] + inner + [dict(e, **{"in": .2 + i * .15, "fx": "draw"}) for i, e in enumerate(shafts)] +
              [{"k": "label", "x": kc[0] + 34, "y": kc[1] - 20, "t": "King's Chamber · granite", "a": "start", "in": .8}])
    claim = [{"k": "label", "x": qc[0] - 20, "y": qc[1] + 36, "t": "chemicals poured in?", "st": "small", "a": "end", "c": GOLD, "in": .3},
             {"k": "label", "x": kc[0] - 60, "y": kc[1] - 60, "t": "resonators?", "st": "small", "a": "end", "c": GOLD, "in": .7},
             {"k": "label", "x": kc[0] + 34, "y": kc[1] + 30, "t": "granite vibrating?", "st": "small", "a": "start", "c": GOLD, "in": 1.1}]
    s2 = like(s1, add=claim + [dict(beam, **{"in": 1.4, "fx": "draw"})])
    checks = ["salt on the walls", "crystals in the granite", "names in sealed rooms"]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "cap", "x": 500, "y": 520, "t": "a machine leaves traces · so check", "in": .1}] +
          [e for i, t in enumerate(checks) for e in ({"k": "rect", "x": 200, "y": 620 + i * 130, "w": 60, "h": 60, "r": 10, "fill": "none", "c": GOLD, "sw": 2.4, "in": .3 + i * .3},
                                                     {"k": "label", "x": 300, "y": 663 + i * 130, "t": t, "st": "body", "a": "start", "in": .4 + i * .3})]}
    cubes = [{"k": "poly", "p": [[x, y], [x + 40, y - 20], [x + 80, y], [x + 40, y + 20]], "fill": "#f4f1ea", "c": "#ffffff", "w": 1, "in": .3 + i * .05} for i, (x, y) in enumerate([(300, 760), (420, 720), (520, 800), (620, 740), (380, 860), (560, 900), (460, 960)])] + \
            [{"k": "poly", "p": [[x, y], [x + 40, y + 20], [x + 40, y + 60], [x, y + 40]], "fill": "#d9d3c6", "c": "#ffffff", "w": 1, "in": .3 + i * .05} for i, (x, y) in enumerate([(300, 760), (420, 720), (520, 800), (620, 740), (380, 860), (560, 900), (460, 960)])]
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "rect", "x": 200, "y": 640, "w": 600, "h": 460, "fill": "#b0936c", "c": "none", "sw": 0, "in": .1}] + cubes +
          [{"k": "cap", "x": 500, "y": 560, "t": "Queen's Chamber salt · 2026 study", "in": .1}, {"k": "label", "x": 500, "y": 1170, "t": "halite: rock salt, from the limestone itself", "in": .9}]}
    grains = [{"k": "arrow", "p": [[x, y], [x + 34 * math.cos(a), y + 34 * math.sin(a)]], "c": "#ffe2a8", "w": 2, "head": 9, "in": .3 + i * .02} for i, (x, y, a) in enumerate(
        [(340 + (i % 6) * 70, 660 + (i // 6) * 90, (i * 2.39) % 6.28) for i in range(30)])]
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "circle", "x": 500, "y": 880, "r": 290, "fill": "#6d5a52", "c": "#c9b0a8", "w": 2, "in": .1}] + grains +
          [{"k": "cap", "x": 500, "y": 520, "t": "quartz grains point every which way", "in": .1}, {"k": "label", "x": 500, "y": 1240, "t": "their charges mostly cancel", "in": 1.3}]}
    rel = [{"k": "rect", "x": 300, "y": 420 + i * 150, "w": 400, "h": 110, "fill": "#1a1411", "c": "#c9ad85", "sw": 1.6, "in": .1 + i * .1} for i in range(5)] + \
          [{"k": "rect", "x": 390, "y": 470 + i * 150, "w": 150, "h": 44, "r": 22, "fill": "none", "c": "#c43a24", "sw": 3, "in": .8 + i * .2} for i in (0, 2, 3)] + \
          [{"k": "label", "x": 465, "y": 500 + i * 150, "t": "Khufu", "st": "ital", "c": "#e4553a", "in": .9 + i * .2} for i in (0, 2, 3)]
    s6 = {"base": "dark", "cam": [1, 500, 860], "els": rel + [{"k": "cap", "x": 500, "y": 380, "t": "the sealed chambers above the King's Chamber", "in": .1},
          {"k": "label", "x": 500, "y": 1210, "t": "work-gang marks in red ochre · first entered 1837", "st": "small", "in": 1.4}]}
    s7 = dict(sky, cam=[1, 500, 900], els=[body, shade] + inner + [{"k": "person", "x": 150 + i * 18, "y": 1150, "h": 7, "t": False} for i in range(8)] +
              [{"k": "label", "x": kc[0] + 40, "y": kc[1] - 10, "t": "a king's tomb", "a": "start", "c": GOLD, "in": .5}])
    # 3-D: the pyramid turns, its shafts and chambers seen through the stone; the sealed rooms as a cutaway stack
    from iso3d import great_pyramid, shot as iso, lab, aim, relieving_stack
    labL = lambda x, y, t, c=None, **k: dict(lab(x, y, t, c), st="lab", **k)
    KC = (8.2, 46.0, 0)
    gpS = great_pyramid(void=False, shafts=True)
    s1 = aim(iso(gpS + [labL(14, 52, "King's Chamber · granite", a="start")], az=-20), (4, 50, 0), 2.6)
    s1["els"][-1]["items"][-1]["a"] = "start"
    beam3 = {"t": "line", "p": [list(KC), [KC[0] + 120, KC[1] + 150, -40]], "c": "#ffe2a8", "w": 6, "style": "claimed", "op": .9}
    s2 = aim(iso(gpS + [beam3, labL(-8, 18, "chemicals poured in?", GOLD, a="end"), labL(8, 66, "resonators?", GOLD), labL(16, 42, "granite vibrating?", GOLD, a="start")], az=-20), (4, 50, 0), 2.6)
    stack, top = relieving_stack()
    s6 = {"base": "dark", "stars": 40, "cam": [1, 500, 900], "els": [{"k": "glow", "x": 500, "y": 900, "r": 480, "kind": "lamp", "op": .16},
          {"k": "iso", "x": 500, "y": 1210, "s": 30, "az": -35, "spin": 2.4, "el": .34, "items": stack},
          {"k": "cap", "x": 500, "y": 330, "t": "the sealed chambers above the King's Chamber", "in": .1},
          {"k": "label", "x": 500, "y": 1400, "t": "work-gang marks in red ochre · first entered 1837", "st": "small", "in": 1.4}]}
    s7 = aim(iso(great_pyramid(void=False) + [{"t": "glow", "x": KC[0], "y": KC[1], "z": 0, "r": 70, "kind": "lamp", "pulse": True},
              labL(KC[0], KC[1] + 14, "a king's name inside", GOLD)], spin=1.6), (0, 60, 0), 1.7)
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE GREAT PYRAMID][sfx:boom][act:playful, what if]What if the Great Pyramid wasn't a ^tomb... [act:wide-eyed, intrigued][tune:rise]but a ^*power plant*?"], cut=False),
        B("world", 1, ["[d:calm][k:1998 · THE THEORY][act:plain, respectful]That's the idea of engineer Christopher ^Dunn.",
                       "[d:list][go:2|0][act:walking through his idea, fair][tune:level]^Chemicals poured down the ^shafts. [act:same pace][tune:level]Granite that ^*vibrates*. [sfx:shimmer][act:the big finish, even][tune:fall]^Energy, beamed out of the ^King's Chamber."]),
        B("collision", 3, ["[d:build][k:TESTABLE][act:bright, genuinely pleased]Here's the ^good part: a machine leaves ^traces. [act:warm, eager][tune:fall]So we can ^*check*."]),
        B("cost", 4, ["[d:build][act:first test, crisp][tune:rise]^Salt on the chamber walls? [act:reporting the result, clear]Tested in {2026|twenty twenty-six}: ^rock salt, from the ^limestone itself. [act:plain, closing it][tune:fall]Not a ^chemical reaction.",
                      "[d:list][go:5|0][act:next test, same tone][tune:rise]Granite as a ^crystal generator? [act:explaining, a little amused]Its ^quartz grains point every which ^way. [act:simple, settled][tune:fall]Their effects mostly ^*cancel* out."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:lower, leaning in]And in ^sealed rooms above the King's Chamber, ^unopened until {1837|eighteen thirty-seven}...",
                          "[d:reveal][sfx:hit][act:the reveal, slower]work ^gangs painted a king's ^name. [gap:0.4][act:the name, clear and firm][tune:highfall]^*Khufu*. [act:quiet, letting it sit][tune:fall]More than a ^dozen times."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:calm summary]A king's name, ^sealed inside. [act:turning to it, even][tune:rise]The ^power plant? [act:the verdict, firm and kind][tune:fall]*Ruled ^out*, by the evidence.",
                     "[d:tension][p:0.93][act:warm, reflective]The ^only machine we can ^trace... [act:the last word, a warm smile][tune:fall]is ^*people*."]),
    ]
    return EP("power-plant", "05.15", "The Giza Power Plant", "giza-power-plant", "debunked", "A machine, not a tomb?", "A *power plant*?", beats, shots,
              "Sessa et al. 2026 · Tuck, Stacey & Starkey 1977, Tectonophysics · Vyse 1840–42 · Tallet & Lehner 2021, The Red Sea Scrolls",
              "Christopher Dunn's power-plant theory makes predictions. The salt, the granite and Khufu's name in sealed chambers answer them.",
              ["#GreatPyramid", "#Giza", "#AncientEgypt", "#Science", "#Archaeology"])


# ---------------------------------------------------------------- 05.16 The Ledger
def _ledger_text():
    s0 = {"base": "sky", "tod": "night", "ground": 1100, "sun": False, "moon": [760, 520, 30], "cam": [1.1, 500, 940], "els": [
        {"k": "pyramid", "x": 380, "y": 1100, "w": 520}, {"k": "pyramid", "x": 740, "y": 1110, "w": 340, "cap": .1}, {"k": "sphinx", "x": 200, "y": 1170, "w": 260}]}
    from iso3d import plateau, plateau_labels, aim
    s0 = plateau(extra=plateau_labels(town=False), az=-160, spin=1.0)
    s0["els"].insert(0, {"k": "circle", "x": 780, "y": 420, "r": 30, "fill": "#efe8da", "c": "none", "w": 0, "layer": "far"})
    grp = lambda title, col, items, y0=560: [{"k": "cap", "x": 500, "y": y0 - 80, "t": title, "c": col, "in": .1}] + \
        [{"k": "label", "x": 500, "y": y0 + i * 92, "t": t, "st": "body", "in": .3 + i * .25} for i, t in enumerate(items)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["Merer's logbook: stone shipped to Akhet-Khufu", "a planned town that fed a workforce", "workers' tombs, and their healed bones", "Khufu's name in sealed chambers"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Strong evidence", "#7fd1d4", ["a void, 30 m long, seen by muons", "a corridor, seen by a camera"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Open", "#f0b06a", ["when the first stones were laid", "a hollow under the Sphinx's paws", "a spiral groove in granite", "when the Osiris Shaft was cut"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting discovery", "#c9c1ee", ["a Sphinx carved by ancient rain", "a star map of 10,500 BCE", "the Earth's size in stone", "machine-cut boxes", "pillars 600 m down"])}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#e98a8a", ["a power plant"])}
    s6 = aim(plateau(az=-120, spin=1.4), (0, 60, 0), 2.4)
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:UNDER GIZA · THE LEDGER][sfx:boom][act:warm, taking stock]^Fifteen films under Giza. [act:laying out the ledger]Here's what's ^real, what's ^open... [act:the last column, crisp][tune:fall]and what's been *ruled ^out*."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:calm, the solid ground][tune:level]A ^papyrus diary logs stone shipped to a pyramid named for ^Khufu. [act:same steady pace][tune:level]A planned ^town fed a ^workforce. [act:gently, with care][tune:fall]Workers lie ^buried nearby, their injuries ^*healed*.",
                       "[d:wonder][go:2|0][act:wonder, lighter]And a ^void, thirty metres long, seen by ^cosmic rays. [act:quiet, a little longing][tune:fall]Still ^*unopened*."]),
        B("collision", 3, ["[d:build][k:OPEN][act:the open questions, thoughtful][tune:level]When the ^first stones on the plateau were ^laid. [act:same thoughtful pace][tune:level]A ^hollow under the Sphinx's paws, never ^drilled. [act:same pace][tune:level]A ^spiral groove in granite, never fully ^copied. [act:closing the column][tune:fall]A ^shaft, never ^dated."]),
        B("cost", 4, ["[d:build][k:AWAITING DISCOVERY][act:brisk roll call, even][tune:level]A far ^older Sphinx. [act:same brisk pace][tune:level]A ^star map from ten thousand BCE. [act:keep it moving][tune:level]The ^Earth in stone. [act:keep it moving][tune:level]^Machine-cut boxes. [act:the last one, landing it][tune:fall]^Pillars under ^Khafre.",
                      "[d:list][sfx:hit][act:fair, even-handed]^Big claims. [act:patient, not dismissive][tune:fall]Still waiting for ^*evidence*."]),
        B("reversal", 5, ["[d:reveal][k:RULED OUT][act:plain, closing the file][tune:fall]A ^power plant. [act:calm, the evidence speaks]The sealed rooms hold a king's ^name, and no trace of a ^*machine*."]),
        B("tag", 6, ["[d:verdict][k:WHAT WOULD CHANGE OUR MINDS][p:0.95][act:practical, counting them off][tune:level]One ^borehole. [act:same beat][tune:level]One ^radiocarbon date. [act:landing it][tune:fall]One ^open data set.",
                     "[d:tension][p:0.93][act:warm, looking forward]Giza isn't ^done talking. [gap:0.4][act:the last word, a smile][tune:fall]Neither are ^*we*."]),
    ]
    return EP("giza-ledger", "05.16", "The Ledger: Under Giza", "", "mixed", "What is known under Giza?", "What's *real* at Giza?", beats, shots,
              "Full references for every film in the case files", "Fifteen films, one ledger: what is established at Giza, what is open, and what has been ruled out.",
              ["#Giza", "#Pyramids", "#Sphinx", "#AncientEgypt", "#Archaeology"])


def ledger():
    """The ledger as one continuous film: twelve niches under Giza (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    from iso3d import plateau
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    khafre = [{"k": "rect", "x": -128, "y": -120, "w": 256, "h": 120, "r": 2, "fill": "#3b2a1c", "c": "#6b4f35", "sw": 1},
              {"k": "poly", "p": [[-70, -120], [0, -192], [70, -120]], "fill": "#c9a86a", "c": "#e8d6b0", "w": 1.5},
              {"k": "line", "p": [[-128, -120], [128, -120]], "c": "#8a6a48", "w": 2}]
    C = Cabinet([
        {"name": "Merer's diary", "model": mdl(merer(), 0)},
        {"name": "The builders' town", "model": mdl(builders_town())},
        {"name": "The Big Void", "model": mdl(big_void())},
        {"name": "The plateau", "model": mdl({"shots": [plateau(az=-120, spin=1.4)]}), "fw": .95, "fh": .6},
        {"name": "The Sphinx", "model": mdl(sphinx_chambers(), 0)},
        {"name": "The spiral groove", "model": mdl(drill_cores(), 0)},
        {"name": "The Osiris Shaft", "model": mdl(osiris_shaft())},
        {"name": "Orion", "model": mdl(orion(), 3)},
        {"name": "Sacred measures", "model": mdl(metrology())},
        {"name": "The Serapeum", "model": mdl(serapeum())},
        {"name": "Khafre's pillars", "model": khafre},
        {"name": "A power plant?", "model": mdl(power_plant())},
    ])
    C.build(stagger=.36)
    ME, BT, BV, PL, SP, SG, OS, OR, SM, SE, KP, PP = range(12)
    muons = C.local(BV, [{"k": "line", "p": [[x, -200], [x * .35, -100]], "c": "#9fd0ff", "w": 2, "style": "inferred", "fx": "draw", "dur": .8, "in": .7 + .1 * k}
                         for k, x in enumerate((-110, -60, -10, 40, 90))])
    pillars = C.local(KP, [{"k": "line", "p": [[x, -118], [x, -12]], "c": "#c9c1ee", "w": 3, "style": "claimed", "fx": "draw", "dur": .9, "in": .5 + .12 * k} for k, x in enumerate((-48, -16, 16, 48))])
    cart = C.local(PP, [{"k": "rect", "x": 40, "y": -236, "w": 76, "h": 34, "r": 17, "fill": "rgba(18,13,10,.8)", "c": "#e8b87a", "sw": 2.5, "in": .4, "fx": "pop"},
                        {"k": "line", "p": [[54, -228], [54, -210]], "c": "#e8b87a", "w": 3, "in": .7}, {"k": "circle", "x": 70, "y": -219, "r": 6, "c": "#e8b87a", "w": 2.5, "in": .8},
                        {"k": "line", "p": [[84, -226], [96, -212], [106, -226]], "c": "#e8b87a", "w": 2.5, "in": .9}])
    bore = C.local(SP, [{"k": "line", "p": [[-70, -160], [-70, -24]], "c": "#9fd0ff", "w": 4, "style": "inferred", "fx": "draw", "dur": 1.0, "in": .1}])
    c14 = C.local(OS, [{"k": "circle", "x": 60, "y": -190, "r": 16, "fill": "rgba(159,208,255,.25)", "c": "#9fd0ff", "w": 2.5, "in": .1, "fx": "pop"},
                       {"k": "circle", "x": 60, "y": -190, "r": 5, "fill": "#9fd0ff", "c": "none", "w": 0, "in": .3}])
    grid_ = C.local(KP, [{"k": "rect", "x": 62 + 15 * a, "y": -96 + 15 * b, "w": 12, "h": 12, "r": 2, "fill": "#9fd0ff", "c": "none", "sw": 0, "op": .75, "keepop": True, "in": .1 + .03 * (a + 4 * b)}
                         for a in range(4) for b in range(3)])
    s1 = C.step(C.cam_cell(ME), C.verdict(ME, "established", "stone shipped for Khufu", .4))
    s2 = C.step(C.cam_cell(BT), C.verdict(BT, "established", "a town that fed them", .3) + C.people(BT, 3, at=.7))
    s3 = C.step(C.cam_cell(BT), C.verdict(BT, "established", "injuries healed", .1, frame=False))
    s4 = C.step(C.cam_cell(BV), C.verdict(BV, "strong", "seen by muons", .3) + muons)
    s5 = C.step(C.cam_cell(BV), C.note(BV, "still unopened", at=.2, c=VCOL["strong"]))
    s6 = C.step(C.cam_cell(PL), C.verdict(PL, "open", "when were they laid?", .2))
    s7 = C.step(C.cam_cell(SP), C.verdict(SP, "open", "a hollow, never drilled", .2))
    s8 = C.step(C.cam_cell(SG), C.verdict(SG, "open", "never fully copied", .2))
    s9 = C.step(C.cam_cell(OS), C.verdict(OS, "open", "never dated", .2))
    s10 = C.step(C.cam_cell(SP), C.verdict(SP, "awaiting", "far older?", .1))
    s11 = C.step(C.cam_cell(OR), C.verdict(OR, "awaiting", "10,500 BCE?", .1))
    s12 = C.step(C.cam_cell(SM), C.verdict(SM, "awaiting", "the Earth in stone?", .1))
    s13 = C.step(C.cam_cell(SE), C.verdict(SE, "awaiting", "machine-cut?", .1))
    s14 = C.step(C.cam_cell(KP), C.verdict(KP, "awaiting", "600 m down?", .1) + pillars)
    s15 = C.step(C.cam_all(), [e for k, i in enumerate((SP, OR, SM, SE, KP)) for e in C.wash(i, VCOL["awaiting"], at=.1 + .12 * k, op=.13)])
    s16 = C.step(C.cam_cell(PP), C.verdict(PP, "ruled", at=.1) + C.struck(PP, "a power plant", at=.2))
    s17 = C.step(C.cam_cell(PP), cart + C.note(PP, "Khufu's name, in the sealed rooms", at=.9, c="#e8b87a"))
    s18 = C.step(C.cam_cell(SP), bore)
    s19 = C.step(C.cam_cell(OS), c14)
    s20 = C.step(C.cam_cell(KP), grid_)
    s21 = C.step(C.cam_all())
    s22 = C.step(C.cam_all(k=.86, sy=720), [e for i in range(12) for e in C.wash(i, "#f2b36b", at=.2 + .06 * i, op=.10)])
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|.3" % s3, (1, 0): "%d|1.1" % s4, (1, 1): "%d|.3" % s5}),
        2: (s6, {(0, 1): "%d|1.0" % s7, (0, 2): "%d|1.0" % s8, (0, 3): "%d|1.0" % s9}),
        3: (s10, {(0, 1): "%d|.9" % s11, (0, 2): "%d|.9" % s12, (0, 3): "%d|.9" % s13, (0, 4): "%d|.9" % s14, (1, 0): "%d|1.2" % s15}),
        4: (s16, {(0, 1): "%d|.3" % s17}),
        5: (s18, {(0, 1): "%d|1.0" % s19, (0, 2): "%d|1.0" % s20, (1, 0): "%d|1.3" % s21, (1, 1): "%d|3" % s22}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/giza-ledger.json)."""
    import recap
    return recap.recap(ledger, "giza-ledger", None)


def EPISODES():
    import f05b      # the six films reworked in their own module (wave 2)
    import lg_b      # 05.01 and 05.02 rebuilt from the legacy films
    return [lg_b.khafre_pillars_m(), lg_b.sealed_door_m(), big_void_m(), sphinx_chambers_m(), sphinx_erosion_m(), merer_m(), sphinx_surveys_m(), osiris_shaft_m(), builders_town_m(), f05b.orion_m(), f05b.metrology_m(),
            f05b.drill_cores_m(), f05b.stone_vases_m(), f05b.serapeum_m(), f05b.power_plant_m(), ledger_recap()]
