"""File 06 · Impossible Stones. Megaliths that seem too big, too precise or too old.
Baalbek, Puma Punku, Sacsayhuamán, Gunung Padang, Nan Madol, the Plain of Jars, the Diquís spheres and the cart ruts of Malta, each weighed.
Every model is schematic unless it says 'to scale'; every date carries its hedge."""
import math
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_

SERIES = "Impossible Stones"
SEA = "#3f86b0"
LIME = "#d8c7a2"
BASALT = "#45423d"
TITICACA = ([(-69.85, -15.25), (-69.45, -15.2), (-69.1, -15.4), (-68.85, -15.75), (-68.8, -16.05), (-68.9, -16.18), (-69.05, -16.12), (-69.2, -16.18), (-69.4, -16.1),
             (-69.65, -16.2), (-69.95, -16.1), (-70.03, -15.85), (-70.0, -15.5)],
            [(-68.88, -16.24), (-68.7, -16.3), (-68.62, -16.4), (-68.7, -16.52), (-68.85, -16.5), (-68.95, -16.42), (-68.98, -16.3)])   # schematic outline


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def box(x, z, y, w, d, h, c=LIME, e="rgba(0,0,0,.32)"):
    return {"t": "box", "x": x, "z": z, "y": y, "w": w, "d": d, "h": h, "c": c, "edge": e}


def tilted(x, z, L, H, D, ang, c=LIME):
    """A long block lying tilted in its quarry: a rotated rectangle extruded D deep."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    p0 = (-L / 2, 0); p1 = (p0[0] + L * ca, p0[1] + L * sa); p2 = (p1[0] - H * sa, p1[1] + H * ca); p3 = (p0[0] - H * sa, p0[1] + H * ca)
    return {"t": "ext", "axis": "x", "x": x, "y": 0, "at": z, "d": D, "prof": [list(p0), list(p1), list(p2), list(p3)], "c": c, "edge": "rgba(0,0,0,.35)"}


def hexcol(x, z, r, h, y=0, c=BASALT, rot=0):
    return {"t": "prism", "pts": [[x + r * math.cos(rot + k * math.pi / 3), z + r * math.sin(rot + k * math.pi / 3)] for k in range(6)], "y": y, "h": h, "c": c, "edge": "rgba(255,236,206,.28)"}


def sphere(x, z, r, c="#8a8176", n=10, y=0):
    """A stone ball as thin turned slices (the iso engine has no true sphere)."""
    out = []
    for k in range(n):
        y0 = -r + 2 * r * k / n; y1 = -r + 2 * r * (k + 1) / n; ym = (y0 + y1) / 2
        out.append({"t": "cyl", "x": x, "z": z, "y": y + r + y0, "r": math.sqrt(max(r * r - ym * ym, .0004)), "h": (y1 - y0) * 1.02, "c": c, "n": 22, "edge": "rgba(0,0,0,0)"})
    return out


def grp(title, c, items, y=520):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": 30, "in": .4 + i * .2} for i, t in enumerate(items)]


# ---------------------------------------------------------------- 06.01 Baalbek
def baalbek():
    tri = [{"t": "slab", "x0": -36, "x1": 36, "z0": -14, "z1": 16, "y": 0, "c": "#9c8a6a"}] + \
          [box(-28.65 + 4.775 + i * 9.55, 0, 0, 9.4, 3.6, 4, "#c8b692") for i in range(6)] + \
          [box(-19.1 + i * 19.1, 0, 4, 18.95, 3.6, 4.3, "#e0cfa8") for i in range(3)] + \
          [{"t": "person", "x": 6, "y": 0, "z": 6, "h": 1.7},
           L_(0, 8.6, "the trilithon · three blocks, each about 19 m and 800 t", GOLD, z=0, dy=-26),
           L_(18, 0, "the course below · about 300 t each", "#cfe6ff", z=4, dy=40)]
    s0 = iso(tri, cam=[1, 500, 900], s=11, x=500, y=1000, az=-24, spin=1.2, el=.42, table=None)
    s0["els"] += [{"k": "cap", "x": 500, "y": 420, "t": "Baalbek · the western podium wall · to scale", "in": .2}]
    v = View(34.6, 37.6, 32.9, 35.2, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Baalbek", 36.2039, 34.0069, {"c": GOLD}), ("Beirut", 35.50, 33.89, {"a": "end", "lx": -18}), ("Damascus", 36.29, 33.51, {})],
                 extra=[{"k": "label", "x": v.p(36.05, 33.75)[0], "y": v.p(36.05, 33.75)[1], "t": "the Beqaa valley", "st": "ital", "c": "#c9ad85"},
                        {"k": "label", "x": v.p(35.1, 34.35)[0], "y": v.p(35.1, 34.35)[1], "t": "the Mediterranean", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    q = [{"t": "slab", "x0": -30, "x1": 30, "z0": -26, "z1": 20, "y": 0, "c": "#b3a07c"},
         tilted(0, -18, 20.5, 4.3, 4.6, 12, "#e0cfa8"), box(-.2, -2, 0, 19.6, 6, 5.5, "#d6c49c"), box(1, 13, 0, 19.5, 4.5, 4.5, "#cbb891"),
         {"t": "person", "x": 13, "y": 0, "z": 18, "h": 1.7},
         L_(8, 8.6, "c. 1,000 t · the Stone of the Pregnant Woman", "#f2dcb4", z=-18, dy=-40), L_(-4, 5.5, "c. 1,650 t · found in 2014", GOLD, z=-2, dy=-10),
         L_(0, 0, "c. 1,240 t · found in the 1990s", "#cfe6ff", z=15, dy=44)]
    s2 = iso(q, cam=[1, 500, 900], s=11, x=500, y=1000, az=-30, spin=1.2, el=.45, table=None)
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "the quarry, 800 m from the temple · schematic", "in": .2}]
    s3 = stat("1,650", "tonnes", "the block found in the quarry in 2014: the largest stone block known from antiquity, still attached to the bedrock", "Abdul Massih 2015; German Archaeological Institute")
    tl, ax = timeline(-300, 300, [(-300, "300 BCE"), (-150, "150"), (1, "1 CE"), (150, "150"), (300, "300")], "The sanctuary, as dated")
    tl["els"] += [{"k": "band", "x0": ax.x(-200), "x1": ax.x(-30), "y": 700, "h": 16, "c": "#c9ad85", "op": .8, "t": "an older terrace of ordinary blocks", "in": .3}] + \
                 event(ax, -15, "Roman colony founded", row=0, c=BONE, i=.6) + event(ax, 60, "Temple of Jupiter largely complete", row=1, c=GOLD, i=.9, sub="an inscription on the building") + \
                 [{"k": "band", "x0": ax.x(-15), "x1": ax.x(200), "y": 540, "h": 14, "c": SCAN, "op": .7, "t": "the giant podium: begun, never finished", "in": 1.2}]
    s4 = tl

    def capstan(i):
        x = 170 + i * 132
        return [{"k": "circle", "x": x, "y": 620, "r": 26, "fill": "#2a2219", "c": GOLD, "w": 2, "in": .5 + i * .08},
                {"k": "line", "p": [[x, 646], [500 + (x - 500) * .25, 1010]], "c": "#c9ad85", "w": 1.6, "op": .8, "in": .7 + i * .08}]
    s5 = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "rect", "x": 250, "y": 1010, "w": 500, "h": 120, "fill": "#cdbb95", "c": "#fff3dc", "sw": 1.5, "in": .2},
                                                    {"k": "label", "x": 500, "y": 1080, "t": "an 800-tonne block, on a timber track", "st": "small", "c": "#2a2219", "halo": False, "in": .4}] +
          [e for i in range(6) for e in capstan(i)] +
          [{"k": "cap", "x": 500, "y": 480, "t": "capstans, pulleys, people · J.-P. Adam, 1977", "in": .2},
           {"k": "label", "x": 500, "y": 1240, "t": "six capstans × 24 people = 144 · about 78 t of pull", "st": "small", "c": AMBER, "in": 1.4}]}
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:BAALBEK · LEBANON][sfx:boom][act:setting the scene, quiet awe]^Three blocks of stone in ^one wall. [act:counting off the size, slow][tune:level]^Nineteen metres long each. [act:the weight, let it land][tune:fall]About eight ^hundred tonnes each.",
                      "[d:tension][cam:1.12|0|0][act:lower, leaning in][tune:level]And in the ^quarry down the road... [act:the reveal, slow and quiet][tune:fall]one ^twice as heavy."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:plain, orienting us]Baalbek, in Lebanon's ^Beqaa valley. [act:easy storytelling]The Romans called it ^Heliopolis and built a vast temple to ^Jupiter here. [go:2|0][act:wonder creeping in]Eight hundred metres away, three even ^bigger blocks still lie in the quarry.",
                       "[d:build][go:3|0][sfx:shimmer][act:savouring the number]The biggest, found in {2014|twenty fourteen}: about ^sixteen hundred and fifty tonnes."]),
        B("collision", 0, ["[d:build][k:THE CASE][act:fair-minded, taking it seriously][tune:rise]Graham Hancock asks the ^fair question: are the giant lower courses ^older than the Roman temple above them?",
                           "[d:build][act:laying out his reasons, even]They're unlike anything ^else the Romans built. [act:a telling detail, pointed]And ^no Roman writer ever ^boasts about moving them."]),
        B("cost", 4, ["[d:build][k:THE DIG][act:confident, matter of fact]The German Archaeological Institute has studied the site for ^decades. [act:uncovering it, slower][tune:level]Under the podium: an ^older, ^smaller terrace... [act:gently deflating, dry]built of ^ordinary blocks.",
                      "[d:build][act:explaining, clear and steady]The giant podium ^wraps around it. [act:the key point, measured]It was begun in the ^Roman programme, and ^never finished. [d:aside][act:a quick aside, lighter]The quarry blocks ^match its length class."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:turning the page, curious][tune:rise]And ^moving them? [act:brisk, glad to explain]In {1977|nineteen seventy-seven} Jean-Pierre Adam worked it out with ^Roman kit: a timber track, capstans, ^pulleys. [sfx:hit][act:counting them off, deliberate][tune:level]^Six capstans. [act:adding up, same pace][tune:level]A hundred and ^forty-four people. [act:the payoff, firm][tune:fall]^One eight-hundred-tonne block.",
                          "[d:aside][act:a fair caveat, lower]Roman silence tells us ^little. [act:plainly, a little rueful]Most of their building records@noun are simply ^lost."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]An ^older megalithic civilisation? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:firm and even]Every clue in the ^ground points to ^Roman engineers.",
                     "[d:tension][p:0.93][act:hopeful, quietly precise]^One sealed layer under the trilithon would ^close@verb the file."]),
    ]
    return EP("baalbek", "06.01", "Baalbek: The Heaviest Stones Ever Moved", "baalbek", "unsupported", "Did Roman builders move Baalbek's giant blocks, or did they inherit them?", "Who moved *800 tonnes*?", beats, shots,
              "Adam 1977, Syria · Lohmann 2010 · Abdul Massih 2015 · van Ess 2008 · Ruprechtsberger 1999 · Hancock 2015, Magicians of the Gods",
              "Three 800-tonne blocks in a temple wall and a 1,650-tonne block still in the quarry: what the German excavations found under the podium, and how Roman engineers could have moved them.",
              ["#Baalbek", "#Megaliths", "#Lebanon", "#AncientEngineering", "#Mystery"])


# ---------------------------------------------------------------- the mural versions: one continuous take (see mural.py)
def _take(ep, **kw):
    """remix() with the science-show narration (rewrite/<id>.json) already in place: every authored 'in' in this File is timed
    against the rewritten words themselves, so nothing is stretched afterwards."""
    import copy
    from mural import remix, rewritten
    return remix(rewritten(copy.deepcopy(ep)), _rewrite=False, **kw)


def _bare(sh, keep=()):
    """An iso shot without its caption and long model labels (the narrator says them; short labels are drawn as they are named)."""
    import copy
    sh = copy.deepcopy(sh)
    sh["els"] = [e for e in sh["els"] if e.get("k") != "cap"]
    for e in sh["els"]:
        if e.get("k") == "iso":
            e["items"] = [it for it in e["items"] if it.get("t") != "label" or it.get("text") in keep]
    return sh


def _ov(sh, items, at, **kw):
    """Items drawn with the shot's own iso projection, so they turn with the model; they build at `at`."""
    base = next(e for e in sh["els"] if e.get("k") == "iso")
    e = {k: base[k] for k in ("x", "y", "s", "az", "spin", "el") if k in base}
    e.update({"k": "iso", "items": list(items), "in": at})
    e.update(kw)
    return e


def _hi(it, c=GOLD, op=.9, style="known"):
    """A highlight of one iso item: the same solid, see-through, outlined in colour."""
    e = dict(it)
    e.update(c=c, xray=True, edge=c, op=op, style=style)
    return e


def _rim(it, c=GOLD, w=4):
    """The top outline of an iso box, as a thick line (an x-ray highlight's edges are hairlines)."""
    x0, x1, z0, z1, y = it["x"] - it["w"] / 2, it["x"] + it["w"] / 2, it["z"] - it["d"] / 2, it["z"] + it["d"] / 2, it["y"] + it["h"]
    return {"t": "line", "p": [[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1], [x0, y, z0]], "c": c, "w": w}


def _spin(sh, v):
    """Slow a model's turn (overlays share it): a gentle turntable keeps added marks where they belong."""
    for e in sh["els"]:
        if e.get("k") == "iso":
            e["spin"] = v
    return sh


def _lab(x, y, z, t, c=GOLD, dy=-16, st="body"):
    return {"t": "label", "x": x, "y": y, "z": z, "text": t, "c": c, "dy": dy, "st": st}


def _go(ep, bi, li, k=0):
    """The step that the k-th [go:] of line li of beat bi (in the finished take) starts."""
    import re
    return int(re.findall(r"\[go:(\d+)", ep["beats"][bi]["lines"][li])[k])


def _inject(ep, step, els):
    """Draw els on the panel that step `step` of the take looks at, timed from that step; they stay on the wall afterwards.
    (mural.remix only builds additions on a first visit, at a beat start or at a line start: this covers a return mid-line.)"""
    from mural import settle
    sh = ep["shots"]
    z, cx, cy = sh[step]["cam"][:3]
    p = next(e for e in sh[step]["els"] if e.get("k") == "panel" and e.get("edge") and e["ox"] <= cx <= e["ox"] + 1000 and e["oy"] <= cy <= e["oy"] + 1778)
    add = {"k": "panel", "ox": p["ox"], "oy": p["oy"], "base": "none", "els": list(els)}
    sh[step]["els"].append(add)
    for s in sh[step + 1:]:
        s["els"].append(settle(add))
    return ep


def _beats(ep, frm):
    """Point beats at other shots (an inserted panel): frm = {beat index: shot index}."""
    for bi, s in frm.items():
        ep["beats"][bi]["visual"] = {"from": s}
    return ep


def baalbek_m():
    """Baalbek as one continuous take: the three giants light up beside two buses and a car park, the 2014 block is weighed on a seesaw,
    the temple on top asks its question, a dig shows the old terrace inside the podium, 144 people turn six capstans, and the verdict
    comes back to the wall, with the sealed layer that would settle it."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, AMBER as AMB, BLUE, LILAC, BONE as BN, INK
    ep = copy.deepcopy(baalbek())
    S = ep["shots"]
    STONE, STONE2, DARK, PURP = "#d8c49c", "#c8b692", "#2a2219", "#6f55b8"
    # 0 · the wall: three giants, each 19 m (almost two buses) and 800 t (five hundred cars)
    s0 = _spin(_bare(S[0]), .3); s0["cam"] = [1, 500, 860]
    tri = [box(-19.1 + i * 19.1, 0, 4, 18.95, 3.6, 4.3, "#e0cfa8") for i in range(3)]
    bus = lambda x: [box(x, 12.5, 0, 9.6, 2.5, 3.0, "#c8743c", "rgba(255,236,206,.5)"), box(x, 12.5, 1.7, 9.64, 2.54, .8, "#f2e6cc", "rgba(0,0,0,0)")]
    s0["els"] += [_ov(s0, [_hi(t, op=.25), _rim(t)], 2.3 + .45 * i, fx="draw", dur=.8) for i, t in enumerate(tri)] + \
        [_ov(s0, [{"t": "line", "p": [[-9.47, 9.4, 1.8], [9.47, 9.4, 1.8]], "c": BN, "w": 3}, {"t": "line", "p": [[-9.47, 8.7, 1.8], [-9.47, 10.1, 1.8]], "c": BN, "w": 3},
                  {"t": "line", "p": [[9.47, 8.7, 1.8], [9.47, 10.1, 1.8]], "c": BN, "w": 3}], 6.2, fx="draw", dur=1.0),
         _ov(s0, [_lab(0, 10.1, 1.8, "19 m", BN, -12)], 6.9),
         _ov(s0, bus(-4.9), 8.5, fx="rise"), _ov(s0, bus(5.0), 8.9, fx="rise")] + \
        [_ov(s0, [_lab(-19.1 + i * 19.1, 6.1, 1.8, "800 t", BN, 14)], 11.6 + .3 * i, fx="pop") for i in range(3)]
    cars = [bx(318 + 15 * (k % 25), 452 + 10.4 * (k // 25), 11, 6, "#e8b87a", r=2, at=round(13.9 + .0035 * k, 3)) for k in range(500)]
    s0["els"] += cars + [label(500, 700, "one block = 500 cars", 15.6, AMB, 30),
                         arrow([[600, 1350], [760, 1362], [920, 1350]], 16.8, AMB, 3, "inferred", .9), label(760, 1322, "the quarry", 17.2, AMB, 30),
                         label(760, 1410, "twice as heavy", 19.6, BN, 32)] + question(500, 380, 21.7, 100)
    # 1 · the map: the temple to Jupiter at Baalbek
    v = View(34.6, 37.6, 32.9, 35.2, (40, 330, 920, 900))
    px, py = v.p(36.2039, 34.0069)
    tx, ty = px + 10, py - 92
    temple = [{"k": "poly", "p": [[tx - 46, ty - 18], [tx + 46, ty - 18], [tx, ty - 44]], "fill": "none", "c": AMB, "w": 3, "in": 8.6, "fx": "draw", "dur": .6},
              line([[tx - 50, ty - 12], [tx + 50, ty - 12]], 8.3, AMB, 4, dur=.4)] + \
             [line([[tx - 40 + 16 * k, ty - 10], [tx - 40 + 16 * k, ty + 34]], 7.8 + .07 * k, AMB, 4, dur=.3) for k in range(6)] + \
             [line([[tx - 54, ty + 38], [tx + 54, ty + 38]], 7.7, AMB, 4, dur=.4), glow(tx, ty + 10, 90, 7.8, .45)]
    # 2 · the quarry: three bigger blocks
    s2 = _spin(_bare(S[2]), .3)
    iso2 = next(e for e in s2["els"] if e.get("k") == "iso")
    q = [it for it in iso2["items"] if it.get("t") in ("ext", "box")]
    iso2["items"] = iso2["items"][:1] + [box(0, -25, 0, 60, 2, 9, "#9c8a6a", "rgba(0,0,0,.3)"), box(0, -23, 0, 60, 2, 5, "#a8946c", "rgba(0,0,0,.3)")] + iso2["items"][1:]
    wt = [(0, 8.0, -18, "1,000 t"), (-.2, 6.8, -2, "1,650 t"), (1, 5.6, 13, "1,240 t")]
    s2["els"] += [_ov(s2, [_hi(t, op=.25)] + ([_rim(t)] if t["t"] == "box" else []) + [_lab(wt[i][0], wt[i][1], wt[i][2], wt[i][3], GOLD, -8)], 1.9 + .45 * i, fx="draw", dur=.8)
                  for i, t in enumerate(q)]
    # 3 · the 2014 block, still joined to the bedrock; then weighed against two of the wall's giants
    Y = -50
    big = {"base": "dark", "cam": [1, 500, 880], "els": [
        {"k": "poly", "p": [[-20, 640], [1020, 640], [1020, 720], [-20, 720]], "fill": "#6f5a44", "c": "none", "w": 0, "in": .3},
        {"k": "block", "x": 200, "y": 640, "w": 590, "h": 165, "d": 60, "in": .7, "fx": "rise"},
        {"k": "poly", "p": [[790, 640], [790, 420], [826, 400], [1020, 370], [1020, 640]], "fill": "#6f5a44", "c": "#8c7152", "w": 2, "in": .3},
        line([[200, 640], [200, 475], [790, 475]], 1.4, AMB, 3, "inferred", 1.0),
        label(260, 445, "2014", 1.9, AMB, 34, st="serif"), person(140, 640, 51, 2.6),
        glow(800, 560, 110, 3.3, .7), label(495, 580, "1,650 t", 6.0, INK, 44, st="serif", halo=False),
        line([[100, 1330 + Y], [900, 1330 + Y]], 7.5, "#8c7152", 3, draw=False),
        {"k": "poly", "p": [[500, 1242 + Y], [440, 1330 + Y], [560, 1330 + Y]], "fill": "#6b4a2e", "c": "#c9a070", "w": 2, "in": 7.6},
        bx(120, 1230 + Y, 760, 12, "#8c6a48", "#c9a070", 1.5, 3, 7.7),
        {"k": "block", "x": 150, "y": 1230 + Y, "w": 255, "h": 72, "d": 30, "in": 8.1, "fx": "rise"},
        {"k": "block", "x": 595, "y": 1230 + Y, "w": 247, "h": 56, "d": 30, "in": 9.0, "fx": "rise"},
        {"k": "block", "x": 595, "y": 1174 + Y, "w": 247, "h": 56, "d": 30, "in": 9.4, "fx": "rise"},
        label(277, 1204 + Y, "1,650 t", 8.4, INK, 28, halo=False), label(718, 1212 + Y, "800 t", 9.7, INK, 28, halo=False), label(718, 1156 + Y, "800 t", 9.9, INK, 28, halo=False)]}
    # 4 · the question: is the giant base older than the Roman temple on top? (the verdict comes back here)
    U, X0, G = 11.0, 185, 1150
    case = {"base": "dark", "floor": G, "cam": [1, 500, 880], "els": [line([[70, G], [930, G]], .2, "#8c7152", 3, draw=False)] +
            [bx(X0 + 105 * k, G - 44, 104, 44, STONE2, DARK, 2, 2, .4 + .08 * k, fx="pop") for k in range(6)] +
            [bx(X0 + 210 * k, G - 91, 209, 47, "#e0cfa8", DARK, 2, 2, 1.0 + .15 * k, fx="pop") for k in range(3)] +
            [bx(X0 + 22.5 * j, G - 104 - 13 * r, 21.5, 12, "#bfae8a", DARK, 1, 1, 1.6 + .01 * (j + 28 * r)) for r in range(2) for j in range(28)] +
            [bx(X0 - 6, G - 97, 642, 101, "none", LILAC, 3, 6, 3.0, style="claimed"), label(176, G - 40, "older?", 5.0, LILAC, 34, a="end")] +
            [line([[X0 + 30 + 63.3 * k, G - 117], [X0 + 30 + 63.3 * k, G - 337]], 5.8 + .06 * k, BN, 5, dur=.5, op=.85) for k in range(10)] +
            [bx(X0 + 10, G - 372, 610, 35, "none", BN, 2.5, 2, 6.5, fx="draw", dur=.6),
             {"k": "poly", "p": [[X0 + 10, G - 372], [500, G - 450], [X0 + 620, G - 372]], "fill": "none", "c": BN, "w": 2.5, "in": 6.9, "fx": "draw", "dur": .6},
             label(500, G - 482, "the Roman temple", 7.2, AMB, 32)]}
    unlike = [glow(500, G - 70, 260, 1.9, .35), bx(X0 - 3, G - 133, 636, 36, "none", AMB, 3, 4, 3.6), label(824, G - 108, "usual", 3.9, AMB, 30, a="start"),
              bx(110, 360, 300, 170, "#e8dcc2", "#8a7a66", 2, 8, 5.6), bx(98, 352, 22, 186, "#c9b48a", "#8a7a66", 1.5, 6, 5.6), bx(400, 352, 22, 186, "#c9b48a", "#8a7a66", 1.5, 6, 5.6)] + \
        [line([[140, 392 + 26 * j], [380 - 40 * (j % 2), 392 + 26 * j]], 5.9 + .1 * j, INK, 3, "inferred", .4) for j in (0, 1, 3, 4)] + \
        [bx(136, 432, 250, 30, "rgba(111,85,184,.12)", PURP, 3, 4, 7.0, style="inferred"), label(260, 580, "no boast", 7.5, LILAC, 30)]
    clues = ((230, 1330), (500, 1350), (770, 1330))
    verdict = [glow(130, G - 52, 110, .6, .5)] + \
              [x for k, (x0, y0) in enumerate(clues) for x in (dot(x0, y0, 8, AMB, 4.6 + .2 * k), glow(x0, y0, 50, 4.6 + .2 * k, .7))] + \
              [arrow([[x0, y0 - 16], [x0, G + 6]], 6.0 + .15 * k, AMB, 3, "inferred", .7, False) for k, (x0, y0) in enumerate(clues)] + \
              [bx(X0 - 2, G - 93, 634, 93, "none", GOLD, 3, 4, 6.6, style="inferred"), label(824, G - 40, "Roman", 6.9, GOLD, 30, a="start")]
    seal = [bx(X0, G + 10, 630, 34, "rgba(159,208,255,.12)", BLUE, 2.5, 6, 1.6, style="inferred"), label(365, G + 86, "sealed layer", 2.0, BLUE, 32),
            {"k": "poly", "p": [[420, G + 20], [452, G + 16], [458, G + 34], [424, G + 38]], "fill": "#c8743c", "c": "#ffd8a8", "w": 1.5, "in": 6.8, "fx": "pop"},
            glow(440, G + 27, 60, 6.8, .8), label(635, G + 86, "Roman pottery?", 7.2, AMB, 28),
            bx(X0 - 8, G + 2, 646, 50, "none", GOLD, 4, 8, 12.6, fx="draw", dur=1.0), glow(500, G + 27, 320, 12.8, .3)]
    # 5 · the dig: inside the podium, an older terrace of ordinary blocks; the giants wrap around it
    dig = {"base": "section", "tod": "dusk", "ground": 1050, "lx": 130, "layers": [{"d": 0, "c": "#5f4c39", "t": ""}, {"d": 200, "c": "#4a3a2c", "t": ""}],
           "cam": [1, 500, 880], "els": [
        bx(200, 600, 600, 450, "#8f7a5c", "#c9a070", 2, 4, .2),
        person(120, 1050, 110, .6), line([[140, 960], [170, 1040]], .8, "#8a5d33", 6, draw=False),
        bx(330, 640, 340, 410, "#1c1611", BN, 2.5, 4, 2.3, style="inferred", fx="fill", dur=1.0),
        line([[720, 452], [920, 452]], 5.0, "#cbbca8", 4, draw=False),
        bx(740, 410, 160, 40, "#a8865e", r=8, at=5.2, fx="fill"), bx(740, 370, 160, 40, "#c9a070", r=8, at=5.6, fx="fill"), bx(740, 330, 160, 40, "#e8c88a", r=8, at=6.0, fx="fill"),
        label(722, 440, "first", 8.0, AMB, 30, a="end"), glow(820, 430, 90, 8.0, .6), glow(500, 900, 200, 10.4, .4)] +
        [bx(350 + 40 * (k % 8), 1010 - 34 * (k // 8), 37, 31, "#a8977c", "#3a2c1e", 1.5, 2, round(12.2 + .04 * k, 2), fx="pop") for k in range(40)] +
        [label(500, 820, "older terrace", 14.4, BN, 32)]}
    wrap = [bx(205, 605 + 150 * k, 120, 146, STONE, DARK, 2, 3, .4 + .2 * k, fx="pop") for k in range(3)] + \
           [bx(675, 605 + 150 * k, 120, 146, STONE, DARK, 2, 3, .5 + .2 * k, fx="pop") for k in range(3)] + \
           [line([[330, 1046], [330, 640], [670, 640], [670, 1046]], 2.4, GOLD, 5, dur=1.6)] + \
           [dot(500, 960, 24, AMB, 4.8), label(500, 970, "1", 4.9, INK, 28, halo=False, st="serif"),
            dot(265, 680, 24, GOLD, 5.4), label(265, 690, "2", 5.5, INK, 28, halo=False, st="serif"),
            dot(735, 680, 24, GOLD, 5.4), label(735, 690, "2", 5.5, INK, 28, halo=False, st="serif"),
            bx(160, 500, 680, 550, "none", LILAC, 3, 6, 8.8, style="claimed"), label(500, 480, "never finished", 9.4, LILAC, 30),
            bx(150, 1120, 700, 280, "#120d0a", r=12, at=10.2, op=.8),
            bx(240, 1170, 520, 46, "#e0cfa8", DARK, 2, 3, 10.6, fx="pop"), label(500, 1203, "in the wall", 10.8, INK, 26, halo=False),
            bx(240, 1300, 520, 46, STONE, DARK, 2, 3, 11.8, fx="pop"), label(500, 1333, "in the quarry", 12.0, INK, 26, halo=False),
            line([[240, 1150], [240, 1366]], 13.4, AMB, 3, "inferred", .5), line([[760, 1150], [760, 1366]], 13.4, AMB, 3, "inferred", .5),
            label(500, 1272, "same length", 14.0, AMB, 28)]
    # 6 · the capstans: one explained, then six, 144 people and one block on a timber track
    cx_ = [125 + 150 * k for k in range(6)]
    spoke = (0.4, 0.4 + math.pi / 2, 0.4 + math.pi, 0.4 + 1.5 * math.pi)
    capm = {"base": "dark", "cam": [1, 500, 880], "els": [
        bx(464, 1000, 72, 380, STONE, DARK, 2, 3, .3), label(140, 330, "1977", 2.2, AMB, 34, st="serif", a="start")] +
        [line([[x, 960], [x, 1420]], 6.2, "#8c6a48", 4, dur=.8) for x in (446, 554)] +
        [line([[430, 975 + 32 * k], [570, 975 + 32 * k]], 6.4 + .03 * k, "#6b4a2e", 5, draw=False) for k in range(14)] +
        [bx(464, 1000, 72, 380, STONE, DARK, 2, 3, 6.4)] +
        [dot(500, 420, 40, "#8c6a48", 7.2), ring(500, 420, 40, 7.2, "#c9a070", 3)] +
        [line([[500, 420], [500 + 125 * math.cos(a), 420 + 125 * math.sin(a) * .55]], 7.4, "#c9a070", 5, dur=.4) for a in spoke] +
        [ring(486 + 14 * j, 952, 12, 7.9 + .1 * j, BN, 2) for j in range(3)] +
        [person(500 + 125 * math.cos(a), 420 + 125 * math.sin(a) * .55 + 40, 64, 11.6 + .2 * j) for j, a in enumerate(spoke)] +
        [{"k": "arrow", "p": [[500 + 175 * math.cos(a), 420 + 96 * math.sin(a)] for a in [k * .25 for k in range(18)]], "c": AMB, "w": 3, "style": "inferred", "curve": True, "fx": "draw", "dur": 1.2, "in": 13.1},
         line([[536, 438], [520, 700], [500, 940]], 15.0, "#e8d6b8", 3, dur=1.2, curve=True), ring(500, 420, 50, 15.4, "#e8d6b8", 3)] +
        [x for k, cx in enumerate(cx_) for x in (dot(cx, 660, 20, "#8c6a48", 16.5 + .1 * k, fx="pop"), line([[cx - 34, 660], [cx + 34, 660]], 16.6 + .1 * k, "#c9a070", 4, draw=False),
                                                 line([[cx, 640], [cx, 680]], 16.6 + .1 * k, "#c9a070", 4, draw=False))] +
        [line([[cx, 680], [500, 940]], 17.0 + .05 * k, "#e8d6b8", 2, dur=.7) for k, cx in enumerate(cx_)] +
        [dot(round(cx + 48 * math.cos(2 * math.pi * j / 24), 1), round(660 + 48 * math.sin(2 * math.pi * j / 24), 1), 5.5, "#e8d6b8", round(17.6 + .011 * (24 * k + j), 3))
         for k, cx in enumerate(cx_) for j in range(24)] +
        [label(500, 790, "144 people", 19.0, AMB, 34), glow(500, 1190, 200, 19.9, .55), label(650, 1200, "800 t", 20.2, BN, 34, a="start"),
         arrow([[620, 1350], [620, 1060]], 20.5, AMB, 4, "inferred", 1.0, False)]}
    shelf = [line([[90, 1190], [400, 1190]], 3.0, "#8c6a48", 6, dur=.5), line([[90, 1330], [400, 1330]], 3.1, "#8c6a48", 6, dur=.5)] + \
            [bx(100 + 60 * j, 1120 + 140 * r, 46, 66, "#e8dcc2", "#8a7a66", 1.5, 8, 3.4 + .1 * r) for r, j in ((0, 1), (1, 3))] + \
            [bx(100 + 60 * j, 1120 + 140 * r, 46, 66, "none", LILAC, 2.5, 8, round(5.4 + .1 * (j + 5 * r), 2), style="claimed") for r in range(2) for j in range(5) if (r, j) not in ((0, 1), (1, 3))] + \
            [label(245, 1390, "lost", 6.4, LILAC, 32), glow(245, 1230, 170, 7.2, .3)]
    shots = S[:4] + [case] + S[4:]
    _beats(ep, {2: 4, 3: 5, 4: 6, 5: 7})
    ep["shots"] = shots
    return _take(ep, scenes={0: s0, 2: s2, 3: big, 4: case, 5: dig, 6: capm}, alias={7: 4}, adds={1: temple},
                 beat_adds={5: (verdict, [1.15, 500, 1080])}, line_adds={(2, 1): (unlike, None), (3, 1): (wrap, None), (4, 1): (shelf, None), (5, 1): (seal, None)})


# ---------------------------------------------------------------- 06.02 Puma Punku
def puma_punku():
    H = [[0, 0], [.34, 0], [.34, .36], [.86, .36], [.86, 0], [1.2, 0], [1.2, 1.0], [.86, 1.0], [.86, .64], [.34, .64], [.34, 1.0], [0, 1.0]]
    blocks = [{"t": "ext", "axis": "x", "x": -3.6 + i * 1.8, "y": 0, "at": 0, "d": .7, "prof": H, "c": "#8d8e8a", "edge": "rgba(255,255,255,.35)"} for i in range(4)]
    hb = [{"t": "slab", "x0": -4.6, "x1": 4.6, "z0": -2.6, "z1": 2.6, "y": 0, "c": "#6f6a60"}] + blocks + \
         [{"t": "person", "x": 3.8, "y": 0, "z": 1.6, "h": 1.7},
          L_(-1.8, 1.1, "andesite H-blocks · the same profile, again and again", GOLD, z=0, dy=-26), L_(0, 0, "sharp inside corners · schematic", "#cfe6ff", z=1.6, dy=40)]
    s0 = iso(hb, cam=[1, 500, 900], s=70, x=500, y=1000, az=-22, spin=1.2, el=.42, table=None)
    v = View(-72.2, -66.8, -19.2, -14.6, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Tiwanaku · Puma Punku", -68.68, -16.56, {"c": GOLD, "a": "start", "ly": 34}), ("Copacabana", -69.09, -16.17, {"a": "end", "lx": -18}), ("La Paz", -68.15, -16.50, {})],
                 extra=[{"k": "poly", "p": [v.p(a, b) for a, b in TITICACA[0]], "fill": "#1f4f6d", "c": "#6fa7c9", "w": 1.2, "curve": True, "in": -1},
                        {"k": "poly", "p": [v.p(a, b) for a, b in TITICACA[1]], "fill": "#1f4f6d", "c": "#6fa7c9", "w": 1.2, "curve": True, "in": -1},
                        {"k": "label", "x": v.p(-69.6, -18.6)[0], "y": v.p(-69.6, -18.6)[1], "t": "the Andes · 3,850 m", "st": "ital", "c": "#c9ad85"},{"k": "line", "p": [v.p(-69.05, -16.2), v.p(-68.95, -16.42), v.p(-68.72, -16.54)], "c": GOLD, "w": 1.8, "op": .75, "style": "inferred", "curve": True, "in": .8},
                        {"k": "label", "x": v.p(-68.35, -16.05)[0], "y": v.p(-68.35, -16.05)[1], "t": "andesite · about 90 km", "st": "small", "c": GOLD, "in": 1.1},
                        {"k": "label", "x": v.p(-69.5, -15.55)[0], "y": v.p(-69.5, -15.55)[1], "t": "Lake Titicaca", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    slab = [{"t": "slab", "x0": -7, "x1": 7, "z0": -5, "z1": 5, "y": 0, "c": "#6f6a60"}, box(0, 0, 0, 7.8, 5.2, 1.1, "#b06a4e", "rgba(255,236,206,.35)"),
            {"t": "person", "x": 5, "y": 0, "z": 3.4, "h": 1.7}, L_(0, 1.1, "the largest slab · red sandstone · about 131 t", GOLD, z=0, dy=-44), L_(0, 0, "7.8 × 5.2 × 1.1 m · to scale", "#cfe6ff", z=3, dy=40)]
    s2 = iso(slab, cam=[1, 500, 900], s=42, x=500, y=990, az=-26, spin=1.2, el=.45, table=None)
    s3 = stat("536–600", "CE", "radiocarbon from the lowest construction fill of the platform: the first building phase", "Vranich 1999, 2006")
    s4 = {"base": "dark", "cam": [1, 500, 880], "els": [
        {"k": "rect", "x": 150, "y": 700, "w": 346, "h": 360, "fill": "#8d8e8a", "c": "#e8e2d6", "sw": 1.5, "in": .2},
        {"k": "rect", "x": 504, "y": 700, "w": 346, "h": 360, "fill": "#8d8e8a", "c": "#e8e2d6", "sw": 1.5, "in": .3},
        {"k": "poly", "p": [[400, 740], [600, 740], [600, 780], [530, 780], [530, 840], [600, 840], [600, 880], [400, 880], [400, 840], [470, 840], [470, 780], [400, 780]], "fill": "#1a1511", "c": "#fff3dc", "w": 1.4, "in": .6},
        {"k": "poly", "p": [[406, 746], [594, 746], [594, 774], [524, 774], [524, 846], [594, 846], [594, 874], [406, 874], [406, 846], [476, 846], [476, 774], [406, 774]], "fill": "#c8743c", "c": "#ffcf9a", "w": 1.2, "in": 1.1},
        {"k": "cap", "x": 500, "y": 560, "t": "an I-shaped socket, cut across the joint", "in": .5},
        {"k": "label", "x": 500, "y": 1140, "t": "molten bronze poured in on site · copper, arsenic, nickel", "c": AMBER, "in": 1.3},
        {"k": "label", "x": 500, "y": 1200, "t": "an alloy of Tiwanaku's own era", "st": "small", "in": 1.6}]}
    tl, ax = timeline(-16000, 2000, [(-15000, "15,000 BCE"), (-10000, "10,000"), (-5000, "5000"), (1, "1 CE")], "Two dates for one platform")
    tl["els"] += event(ax, -15000, "Posnansky's date", row=1, c=GOLD, i=.3, sub="from star alignments") + \
                 [{"k": "band", "x0": ax.x(500), "x1": ax.x(1000), "y": 700, "h": 16, "c": SCAN, "t": "Tiwanaku", "in": .8}] + event(ax, 560, "radiocarbon", row=2, c=SCAN, i=1.1, sub="AD 536–600")
    s5 = tl
    s6 = like(s0, cam=[1.2, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:PUMA PUNKU · BOLIVIA][sfx:boom][act:curious, drawing us close]Sharp ^inside corners. [act:the marvel, unhurried]^Identical H-shaped blocks, like a ^kit. [act:the kicker, wide-eyed]At ^three thousand eight hundred and fifty metres.",
                      "[d:tension][cam:1.12|0|0][act:a light, dry report]TV calls them ^machined. [act:a playful pause][tune:level]So... [act:the hook, genuinely curious][tune:fall]^who made the kit?"], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:plain storytelling, warm]Puma Punku is a platform in ^Tiwanaku, beside Lake ^Titicaca. [act:matter of fact, steady]The hard grey andesite came from about ^ninety kilometres away, across or ^around the lake.",
                       "[d:build][go:2|0][act:a quick contrast, lighter]The ^red sandstone came from ^ten. [act:weighing it out, impressed]The biggest slab: about a ^hundred and thirty-one tonnes."]),
        B("collision", 5, ["[d:build][k:THE CASE][act:storytelling, intrigued]An explorer, Arthur Posnansky, read@past the site's alignments against the slow drift of the ^stars. [sfx:shimmer][act:the big claim, let it land]His answer: about ^fifteen thousand BCE.",
                           "[d:build][act:brisk, matter of fact]Graham Hancock ^revived that date in the {1990s|nineteen nineties}."]),
        B("cost", 3, ["[d:build][k:THE DATES][act:the turn, crisp][tune:fall]Then ^radiocarbon. [act:precise, reading the lab result]Organic material from the lowest fill under the platform: AD {536|five thirty-six} to {600|six hundred}.",
                      "[d:build][act:stacking up the evidence][tune:level]Tiwanaku ^pottery. [act:same beat, firmer][tune:fall]Tiwanaku ^carvings. [d:aside][act:explaining, fair, not gloating]Posnansky's method had a ^weak spot: small errors in the alignment swing the date by ^thousands of years."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, a new clue]And the ^metal. [sfx:hit][act:vivid, building]The blocks were locked with ^bronze clamps, poured molten into carved sockets, on ^site. [act:the clincher, quiet and sure]An alloy from Tiwanaku's ^own era.",
                          "[d:build][act:admiring, even]Architects who measured the blocks see standard ^templates and patient ^grinding. [act:simple and plain][tune:fall]No ^sign of machines."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:posing it, calm][tune:rise]^Fifteen thousand BCE? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:genuine wonder, softer][tune:fall]How ^exactly they shaped that andesite? [act:honest, a small shrug][tune:fall]Still ^open.",
                     "[d:tension][p:0.93][act:calm, closing the file][tune:fall]The ^age is settled. [act:warm wonder, the last word][tune:fall]The ^skill is still ^astonishing."]),
    ]
    return EP("puma-punku", "06.02", "Puma Punku: The Lego Temple of the Andes", "puma-punku", "debunked", "Is Puma Punku a Tiwanaku temple, or the ruin of something far older?", "So... who made the *kit*?", beats, shots,
              "Vranich 1999, 2006 · Protzen & Nair 2013, The Stones of Tiahuanaco · Lechtman 1998 · Ponce Sanginés 1970 · Posnansky 1945",
              "Identical H-blocks and bronze poured into stone at 3,850 metres: the 15,000 BCE date, the radiocarbon that replaced it, and the precision that still needs explaining.",
              ["#PumaPunku", "#Tiwanaku", "#Bolivia", "#AncientEngineering", "#Mystery"])


def puma_punku_m():
    """Puma Punku as one continuous take: the kit of H-blocks with its corners and templates, the andesite's 90 km, a slab as heavy as a
    blue whale, Posnansky's drifting sunrise, a candle-clock under the platform, bronze poured into a socket, and the patient grinding."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(puma_punku())
    S = ep["shots"]
    H = [[0, 0], [.34, 0], [.34, .36], [.86, .36], [.86, 0], [1.2, 0], [1.2, 1.0], [.86, 1.0], [.86, .64], [.34, .64], [.34, 1.0], [0, 1.0]]
    BRZ = "#c8743c"

    def gear(cx, cy, r, at, c=LILAC):
        return [ring(cx, cy, r, at, c, 4, dur=.5), ring(cx, cy, r * .35, at + .1, c, 3, dur=.3)] + \
               [line([[cx + r * math.cos(a), cy + r * math.sin(a)], [cx + (r + 12) * math.cos(a), cy + (r + 12) * math.sin(a)]], at + .2, c, 6, draw=False) for a in [k * math.pi / 4 for k in range(8)]]
    # 0 · the kit: inside corners, one template fits every block, nearly four kilometres up
    s0 = _spin(_bare(S[0]), .15); s0["cam"] = [1.25, 500, 950]
    x1 = -1.8
    s0["els"] += [_ov(s0, [{"t": "glow", "x": x1 + u, "y": v, "z": .36, "r": 34, "kind": "lamp"} for u, v in ((.34, .36), (.86, .36), (.34, .64), (.86, .64))] +
                      [{"t": "line", "p": [[x1 + .34, .64, .36], [x1 + .34, .36, .36], [x1 + .86, .36, .36], [x1 + .86, .64, .36], [x1 + .34, .64, .36]], "c": GOLD, "w": 4}], 3.0, fx="draw", dur=.8)] + \
        [_ov(s0, [{"t": "line", "p": [[-3.6 + 1.8 * i + u, v, .38] for u, v in H + H[:1]], "c": AMB, "w": 3, "style": "inferred"}], 5.6 + .5 * i, fx="draw", dur=.6) for i in range(4)] + \
        [{"k": "poly", "p": [[148, 660], [240, 580], [300, 610], [400, 500], [500, 600], [600, 545], [700, 630], [790, 590], [852, 660]], "fill": "#3b3140", "c": "#6a5a72", "w": 2, "in": 10.8, "fx": "rise"},
         {"k": "poly", "p": [[372, 530], [400, 500], [428, 530], [410, 525], [398, 538], [386, 527]], "fill": "#efe8da", "c": "none", "w": 0, "in": 11.2},
         label(400, 485, "3,850 m", 12.0, BN, 34, st="serif")] + \
        [bx(610, 1235, 190, 125, "#15100c", "#cbd2d8", 4, 14, 15.6), line([[660, 1235], [635, 1200]], 15.6, "#cbd2d8", 3, draw=False), line([[750, 1235], [775, 1200]], 15.6, "#cbd2d8", 3, draw=False)] + \
        gear(705, 1297, 30, 15.9) + [label(596, 1310, "machined?", 16.2, LILAC, 30, a="end")] + question(300, 1330, 17.6, 90)
    # 1 · the map: Tiwanaku by Lake Titicaca, the andesite's road
    v = View(-70.4, -67.6, -17.6, -15.0, (40, 330, 920, 900))
    m1 = mapshot(v, pins=[("Tiwanaku · Puma Punku", -68.68, -16.56, {"c": GOLD, "a": "start", "ly": 38}), ("Copacabana", -69.09, -16.17, {"a": "end", "lx": -18}),
                          ("La Paz", -68.15, -16.50, {})],
                 extra=[{"k": "poly", "p": [v.p(a_, b_) for a_, b_ in TITICACA[0]], "fill": "#1f4f6d", "c": "#6fa7c9", "w": 1.4, "curve": True, "in": -1},
                        {"k": "poly", "p": [v.p(a_, b_) for a_, b_ in TITICACA[1]], "fill": "#1f4f6d", "c": "#6fa7c9", "w": 1.4, "curve": True, "in": -1},
                        {"k": "label", "x": v.p(-69.45, -15.7)[0], "y": v.p(-69.45, -15.7)[1], "t": "Lake Titicaca", "st": "ital", "c": "#9fd0ff", "in": 3.6},
                        {"k": "label", "x": v.p(-69.0, -17.25)[0], "y": v.p(-69.0, -17.25)[1], "t": "the Andes · 3,850 m", "st": "ital", "c": "#c9ad85", "in": 1.0},
                        {"k": "line", "p": [v.p(-69.05, -16.2), v.p(-68.95, -16.42), v.p(-68.72, -16.54)], "c": GOLD, "w": 4, "style": "inferred", "curve": True, "in": 6.0, "fx": "draw", "dur": 1.6},
                        {"k": "label", "x": v.p(-69.0, -16.75)[0], "y": v.p(-69.0, -16.75)[1], "t": "andesite · about 90 km", "st": "lab", "c": GOLD, "in": 8.0, "a": "end"},
                        {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    for e in m1["els"]:
        if e.get("k") == "pin":
            e["in"] = .4 if "Tiwanaku" in e["t"] else 2.2
    m1["els"] = m1["els"][:1] + [e for e in m1["els"] if e.get("k") == "poly"] + [e for e in m1["els"][1:] if e.get("k") != "poly"] + [glow(*v.p(-68.68, -16.56), 90, 1.6, .55)]
    m1["cam"] = [1.25, 500, 760]
    # 2 · the red sandstone slab: 7.8 × 5.2 m, 131 t, as heavy as a blue whale
    s2 = _spin(_bare(S[2]), .3)
    slab = box(0, 0, 0, 7.8, 5.2, 1.1, "#b06a4e")
    whale = [[300, 560], [360, 520], [460, 505], [580, 515], [690, 545], [760, 560], [800, 540], [840, 500], [850, 535], [830, 570], [860, 610], [840, 612], [790, 585],
             [700, 600], [580, 625], [450, 625], [350, 610], [305, 590]]
    s2["els"] += [label(500, 1300, "red sandstone, from 10 km", 1.2, "#f2b08a", 32),
                  _ov(s2, [_hi(slab, GOLD, .2), _rim(slab)], 3.9, fx="draw", dur=.8),
                  _ov(s2, [{"t": "line", "p": [[-3.9, 1.1, 3.0], [3.9, 1.1, 3.0]], "c": BN, "w": 3}, _lab(0, 1.1, 3.0, "7.8 m", BN, 34),
                           {"t": "line", "p": [[4.3, 1.1, -2.6], [4.3, 1.1, 2.6]], "c": BN, "w": 3}, _lab(4.3, 1.1, 0, "5.2 m", BN, 30)], 4.6, fx="draw", dur=.8),
                  _ov(s2, [_lab(0, 1.4, -1, "131 t", BN, -60, "serif")], 6.0, fx="pop"),
                  {"k": "poly", "p": whale, "fill": "#3f6f8a", "c": "#9fd0ff", "w": 2, "curve": True, "in": 8.0, "fx": "rise"},
                  dot(380, 548, 6, "#0d1a22", 8.2), line([[460, 600], [520, 640], [560, 615]], 8.2, "#9fd0ff", 3, draw=False), glow(560, 560, 260, 8.2, .35, "scan"),
                  label(560, 690, "a blue whale", 8.6, BLUE, 30)]
    # 3 · Posnansky: a wall aimed at a sunrise, the sunrise drifts, count back the years
    HZ = 820
    pos = {"base": "sky", "tod": "dawn", "ground": HZ, "sun": False, "cam": [1, 500, 880], "els": [
        {"k": "block", "x": 250, "y": 1110, "w": 180, "h": 70, "d": 50, "in": .6, "fx": "rise"}, person(200, 1110, 70, .9),
        line([[340, 1040], [420, HZ]], 2.6, AMB, 4, "known", .9), label(250, 1170, "the wall", 2.4, BN, 28),
        {"k": "arrow", "p": [[430, HZ - 90], [500, HZ - 120], [570, HZ - 90]], "c": BN, "w": 3, "curve": True, "fx": "draw", "dur": 1.0, "in": 5.8, "style": "inferred"},
        label(500, HZ - 140, "the sky drifts", 6.2, BN, 30),
        oval(420, HZ, 34, 34, "#c9c1ee", "none", 0, .6, 8.6), glow(420, HZ - 10, 90, 8.6, .5), label(330, HZ - 36, "long ago", 9.0, LILAC, 28),
        oval(580, HZ, 34, 34, "#ffd9a0", "none", 0, 1, 11.0), glow(580, HZ - 10, 130, 11.0, .7, "sun"), label(670, HZ - 36, "today", 11.2, GOLD, 28),
        line([[340, 1040], [580, HZ]], 13.0, GOLD, 3, "inferred", .9),
        {"k": "line", "p": [[380 + 60 * math.cos(math.radians(a)), 1040 - 60 * math.sin(math.radians(a))] for a in range(60, 74, 2)], "c": AMB, "w": 4, "fx": "draw", "dur": .4, "in": 13.8},
        label(470, 975, "mismatch", 14.0, AMB, 28, a="start"),
        bx(90, 1225, 820, 185, "#120d0a", r=14, at=15.0, op=.82), line([[860, 1300], [140, 1300]], 15.2, "#cbbca8", 3, dur=2.0),
        label(860, 1350, "today", 15.2, BN, 26), dot(860, 1300, 8, BN, 15.2),
        arrow([[820, 1265], [500, 1250], [190, 1265]], 15.6, LILAC, 3, "claimed", 1.6),
        dot(140, 1300, 12, LILAC, 17.4), glow(140, 1300, 60, 17.4, .7), label(150, 1350, "15,000 BCE?", 17.6, LILAC, 32, a="start")]}
    hancock = [bx(700, 1050, 110, 140, "#6b3a2a", "#c8743c", 3, 6, .6, fx="pop"), line([[722, 1080], [788, 1080]], .8, "#f2dcb4", 3, draw=False),
               line([[722, 1100], [770, 1100]], .8, "#f2dcb4", 3, draw=False), label(755, 1230, "1990s", 1.0, BN, 28),
               arrow([[700, 1200], [400, 1240], [190, 1285]], 2.4, LILAC, 2, "claimed", 1.0)]
    # 4 · radiocarbon: a plant takes in carbon, the candle-clock, the lowest fill, AD 536-600; then the weak spot
    rc = {"base": "dark", "cam": [1, 500, 880], "els": [
        line([[220, 640], [220, 470]], 2.0, "#7fa35a", 6, dur=.6),
        {"k": "poly", "p": [[220, 560], [160, 520], [150, 490], [200, 510]], "fill": "#7fa35a", "c": "none", "w": 0, "in": 2.4, "fx": "pop"},
        {"k": "poly", "p": [[220, 520], [280, 470], [295, 445], [245, 470]], "fill": "#7fa35a", "c": "none", "w": 0, "in": 2.6, "fx": "pop"},
        line([[120, 645], [320, 645]], 2.0, "#8c7152", 3, draw=False)] +
        [dot(160 + 30 * k, 380 + 22 * (k % 2), 7, GR, 3.2 + .25 * k) for k in range(5)] +
        [arrow([[175 + 30 * k, 400 + 22 * (k % 2)], [205 + 10 * k, 455]], 3.4 + .25 * k, GR, 2, dur=.3, curve=False) for k in range(5)] +
        [bx(640, 420, 50, 220, "none", "#efe6d2", 2, 6, 7.4, style="inferred"), bx(640, 540, 50, 100, "#efe6d2", r=6, at=7.6),
         line([[665, 540], [665, 522]], 7.8, INK, 2, draw=False), glow(665, 505, 70, 7.8, .9, "lamp"), dot(665, 508, 8, "#ffcf8a", 7.8),
         arrow([[720, 440], [720, 530]], 8.8, AMB, 3, dur=.6, curve=False), label(735, 480, "fades", 9.0, AMB, 28, a="start"),
         line([[610, 540], [610, 640]], 11.2, GOLD, 3, dur=.4), line([[600, 540], [620, 540]], 11.2, GOLD, 3, draw=False), line([[600, 640], [620, 640]], 11.2, GOLD, 3, draw=False),
         label(596, 600, "what's left", 11.6, GOLD, 28, a="end"), line([[600, 645], [740, 645]], 7.4, "#8c7152", 3, draw=False)] +
        [bx(170 + 132 * k, 720, 128, 56, "#8d8e8a", "#2a2219", 2, 3, 14.6 + .08 * k) for k in range(5)] +
        [bx(170 + 132 * k, 778, 128, 56, "#b06a4e", "#2a2219", 2, 3, 14.8 + .08 * k) for k in range(5)] +
        [bx(170, 836, 656, 70, "#5f4c39", "#c9a070", 2, 3, 15.4, fx="fill"), label(498, 935, "lowest fill", 16.2, AMB, 28)] +
        [dot(x, y, 6, "#9fcf6a", 17.0 + .08 * k) for k, (x, y) in enumerate(((240, 860), (330, 880), (420, 858), (520, 884), (610, 862), (700, 878), (770, 860)))] +
        [glow(500, 870, 300, 17.2, .45), label(500, 1010, "AD 536–600", 19.0, GOLD, 50, st="serif")]}
    X = lambda y: 150 + 700 * (y + 15000) / 17000
    weak = [line([[X(-15000), 1180], [X(2000), 1180]], .2, "#cbbca8", 3, dur=1.0), label(X(-15000), 1225, "15,000 BCE", .3, LILAC, 26), label(X(2000), 1225, "today", .3, BN, 26),
            bx(X(536) - 6, 1160, 14, 40, GOLD, r=3, at=.6),
            {"k": "vase", "x": 715, "y": 1150, "h": 70, "w": 44, "tone": "#b06a4e", "in": .8}, label(715, 1062, "pottery", 1.0, AMB, 26),
            bx(800, 1080, 70, 70, "#8d8e8a", "#2a2219", 2, 4, 1.8), line([[812, 1102], [835, 1088], [858, 1102]], 2.0, INK, 3, draw=False), line([[815, 1130], [855, 1130]], 2.0, INK, 3, draw=False),
            label(835, 1062, "carvings", 2.0, AMB, 26),
            dot(X(-15000), 1180, 10, LILAC, 4.4), strike(X(-15000) - 30, 1210, X(-15000) + 30, 1150, 4.6),
            line([[300, 1420], [800, 1355]], 7.2, BN, 2, dur=.6), line([[300, 1420], [800, 1395]], 7.2, BN, 2, dur=.6), glow(800, 1375, 70, 7.6, .7),
            label(560, 1465, "a sliver of a degree", 7.6, BN, 28),
            arrow([[X(-15000) + 20, 1272], [X(536) - 20, 1272]], 10.4, RD, 3, dur=.8, curve=False), arrow([[X(536) - 20, 1272], [X(-15000) + 20, 1272]], 10.4, RD, 3, dur=.8, curve=False),
            label(470, 1315, "thousands of years", 10.8, RD, 30)]
    # 5 · the bronze clamp: a socket across the joint, metal poured molten on site; then templates and grinding
    I_ = [[400, 440], [600, 440], [600, 480], [530, 480], [530, 540], [600, 540], [600, 580], [400, 580], [400, 540], [470, 540], [470, 480], [400, 480]]
    cl = {"base": "dark", "cam": [1, 500, 880], "els": [
        bx(150, 380, 346, 260, "#8d8e8a", "#e8e2d6", 2, 4, .3), bx(504, 380, 346, 260, "#8d8e8a", "#e8e2d6", 2, 4, .4), line([[500, 370], [500, 650]], .6, INK, 3, draw=False),
        {"k": "poly", "p": I_, "fill": "none", "c": GOLD, "w": 3, "in": 3.4, "fx": "draw", "dur": .8, "style": "inferred"},
        {"k": "poly", "p": I_, "fill": "#1a1511", "c": "#fff3dc", "w": 1.6, "in": 5.6, "fx": "pop"},
        {"k": "poly", "p": [[700, 250], [790, 250], [780, 320], [710, 320]], "fill": "#5a4a3a", "c": "#c9a070", "w": 2, "in": 8.0, "fx": "pop"},
        line([[705, 300], [620, 400], [560, 470]], 8.8, "#ffb060", 7, dur=.6, curve=True), glow(560, 470, 120, 8.8, .9, "red"),
        {"k": "poly", "p": [[p[0] + (4 if p[0] < 500 else -4) * (1 if p[0] in (400, 600) else 0), p[1] + (4 if p[1] < 510 else -4) * (1 if p[1] in (440, 580) else 0)] for p in I_],
         "fill": BRZ, "c": "#ffcf9a", "w": 1.4, "in": 9.6, "fx": "fill", "dur": 1.2},
        label(500, 700, "bronze", 10.4, BRZ, 34)] +
        [x for k, (el, c) in enumerate((("copper", "#d9894a"), ("arsenic", "#cbd2d8"), ("nickel", "#9fd0ff"))) for x in (dot(250 + 250 * k, 790, 30, c, 11.8 + .4 * k), label(250 + 250 * k, 860, el, 12.0 + .4 * k, c, 28))] +
        [label(500, 940, "Tiwanaku's own era", 13.8, GOLD, 32)]}
    tpl = [{"k": "poly", "p": [[150 + 260 * u, 1120 + 230 * (1 - v)] for u, v in H], "fill": "#8d8e8a", "c": "#e8e2d6", "w": 2, "in": .4}] + \
          [{"k": "poly", "p": [[150 + 260 * u + 6, 1120 + 230 * (1 - v) - 6] for u, v in H], "fill": "rgba(232,184,122,.1)", "c": AMB, "w": 3, "in": 1.6, "fx": "draw", "dur": 1.0, "style": "inferred"},
           label(306, 1400, "a template", 2.0, AMB, 28),
           bx(560, 1240, 300, 110, "#8d8e8a", "#e8e2d6", 2, 4, 3.2), oval(700, 1215, 44, 26, "#6a645c", "#cbbca8", 2, 1, 5.0)] + \
          [{"k": "arrow", "p": [[700 + 80 * math.cos(a), 1215 + 30 * math.sin(a)] for a in [k * .3 + 3.5 for k in range(12)]], "c": BN, "w": 2.5, "curve": True, "fx": "draw", "dur": .8, "in": 5.3},
           label(710, 1400, "grinding", 5.6, BN, 28)] + gear(840, 1100, 32, 7.0, "#cbbca8") + [strike(790, 1150, 890, 1050, 7.6)]
    # 6 → back to the kit: 15,000 BCE struck out; the shaping still open; the people who did it
    verdict = [label(500, 712, "15,000 BCE", .3, LILAC, 44, st="serif"), strike(370, 722, 630, 672, 1.9, RD, 6)] + \
              [_ov(s0, [{"t": "q", "x": 0, "y": 1.6, "z": 0, "c": GOLD, "size": 70}], 3.8, fx="pop")]
    people = [_ov(s0, [{"t": "person", "x": -4.2 + 2.1 * k, "y": 0, "z": 2.5, "h": 1.7, "color": "#e8d6b8"}], 3.0 + .2 * k, fx="rise") for k in range(4)] + [glow(500, 1000, 360, 3.4, .35)]
    shots = S[:3] + [pos, rc, cl, S[6]]
    _beats(ep, {2: 3, 3: 4, 4: 5, 5: 6})
    ep["shots"] = shots
    return _take(ep, scenes={0: s0, 1: m1, 2: s2, 3: pos, 4: rc, 5: cl}, alias={6: 0},
                 beat_adds={5: (verdict, [1.12, 500, 960])},
                 line_adds={(2, 1): (hancock, None), (3, 1): (weak, [1.15, 500, 1150]), (4, 1): (tpl, None), (5, 1): (people, None)})


# ---------------------------------------------------------------- 06.03 Sacsayhuamán
def jigsaw(x0, y0, w, h, cols, rows, seed=3):
    """A polygonal Inca wall: jittered grid points shared by neighbours, so every stone fits the next; a few cells merged into giants."""
    import random
    rnd = random.Random(seed)
    cw, ch = w / cols, h / rows
    P = {(i, j): (x0 + i * cw + (rnd.uniform(-.28, .28) * cw if 0 < i < cols else 0), y0 + j * ch + (rnd.uniform(-.22, .22) * ch if 0 < j < rows else 0))
         for i in range(cols + 1) for j in range(rows + 1)}
    MH = {(i, j): ((P[(i, j)][0] + P[(i + 1, j)][0]) / 2 + rnd.uniform(-.1, .1) * cw, (P[(i, j)][1] + P[(i + 1, j)][1]) / 2 + (rnd.uniform(-.16, .16) * ch if 0 < j < rows else 0))
          for i in range(cols) for j in range(rows + 1)}
    MV = {(i, j): ((P[(i, j)][0] + P[(i, j + 1)][0]) / 2 + (rnd.uniform(-.14, .14) * cw if 0 < i < cols else 0), (P[(i, j)][1] + P[(i, j + 1)][1]) / 2 + rnd.uniform(-.1, .1) * ch)
          for i in range(cols + 1) for j in range(rows)}
    big = {(1, 2), (2, 2), (1, 3), (2, 3), (4, 3), (5, 3)}
    merged = {(1, 2): [(1, 2), (2, 2), (1, 3), (2, 3)], (4, 3): [(4, 3), (5, 3)]}
    out = []

    def cell(i, j, w_=1, h_=1):
        pts = []
        for k in range(w_):
            pts += [P[(i + k, j)], MH[(i + k, j)]]
        for k in range(h_):
            pts += [P[(i + w_, j + k)], MV[(i + w_, j + k)]]
        for k in range(w_ - 1, -1, -1):
            pts += [P[(i + k + 1, j + h_)], MH[(i + k, j + h_)]]
        for k in range(h_ - 1, -1, -1):
            pts += [P[(i, j + k + 1)], MV[(i, j + k)]]
        return pts
    n = 0
    for j in range(rows):
        for i in range(cols):
            if (i, j) in big and (i, j) not in merged:
                continue
            if (i, j) in merged:
                ws = 2; hs = 2 if len(merged[(i, j)]) == 4 else 1
                pts = cell(i, j, ws, hs); tone = "#d9c9a6"
            else:
                pts = cell(i, j); tone = ["#c9b894", "#bfad88", "#d2c19c", "#b8a680"][(i * 3 + j) % 4]
            out.append({"k": "poly", "p": [[round(a, 1), round(b, 1)] for a, b in pts], "fill": tone, "c": "#2a2219", "w": 2.4, "curve": True, "in": .2 + n * .03})
            n += 1
    return out


def sacsayhuaman():
    def zig(y, off, n=7, amp=9, L=84, th=3.2):
        xs = [-L / 2 + L * k / n for k in range(n + 1)]
        front = [[x, off + (amp if k % 2 else 0)] for k, x in enumerate(xs)]
        back = [[x, z - th] for x, z in front][::-1]
        return {"t": "prism", "pts": front + back, "y": y, "h": 5.5, "c": "#cbb893", "edge": "rgba(0,0,0,.3)", "cw": True}
    tw = [{"t": "slab", "x0": -48, "x1": 48, "z0": -26, "z1": 30, "y": 0, "c": "#7f8f5a"},
          zig(0, 14), {"t": "slab", "x0": -46, "x1": 46, "z0": -4, "z1": 11, "y": 5.5, "c": "#7f8f5a"}, zig(5.5, 2), {"t": "slab", "x0": -46, "x1": 46, "z0": -20, "z1": -1, "y": 11, "c": "#7f8f5a"}, zig(11, -10),
          {"t": "person", "x": 10, "y": 0, "z": 26, "h": 1.7},
          L_(0, 16.5, "three zigzag terraces · the longest about 400 m", GOLD, z=-10, dy=-24), L_(0, 0, "the lowest wall about 6 m high · schematic", "#cfe6ff", z=26, dy=40)]
    s0 = iso(tw, cam=[1, 500, 900], s=6.2, x=500, y=980, az=-18, spin=1.2, el=.5, table=None)
    v = View(-80.5, -68.0, -18.5, -8.0, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Sacsayhuamán · above Cusco", -71.9817, -13.5086, {"c": GOLD}), ("Lima", -77.04, -12.05, {"a": "end", "lx": -18}), ("Machu Picchu", -72.545, -13.163, {"a": "end", "lx": -18, "ly": -22})],
                 extra=[{"k": "label", "x": v.p(-71.5, -15.3)[0], "y": v.p(-71.5, -15.3)[1], "t": "3,700 m up in the Andes", "st": "small", "c": AMBER, "in": 1.0},
                        {"k": "label", "x": v.p(-78.5, -15.5)[0], "y": v.p(-78.5, -15.5)[1], "t": "the Pacific", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    s2 = {"base": "dark", "cam": [1, 500, 880], "els": jigsaw(110, 640, 780, 520, 6, 4) +
          [{"k": "person", "x": 860, "y": 1160, "h": 76, "t": False, "in": 1.2}, {"k": "cap", "x": 500, "y": 540, "t": "no mortar · every stone cut to fit its neighbours", "in": .3},
           {"k": "label", "x": 500, "y": 1250, "t": "the biggest blocks: estimates from about 120 to 200 t", "st": "small", "c": AMBER, "in": 1.5}]}
    s3 = stat("20,000", "workers", "on rotation, according to Pedro Cieza de León in the 1550s: 4,000 quarrying, 6,000 hauling with ropes", "Cieza de León 1553")
    s4 = {"base": "dark", "cam": [1, 500, 880], "els": [
        {"k": "poly", "p": [[260, 1110], [740, 1110], [740, 960], [640, 930], [520, 980], [380, 940], [260, 970]], "fill": "#c9b894", "c": "#2a2219", "w": 2.4, "in": .2},
        {"k": "poly", "p": [[260, 820], [380, 790], [520, 830], [640, 780], [740, 810], [740, 640], [260, 640]], "fill": "#d9c9a6", "c": "#2a2219", "w": 2.4, "in": .4},
        {"k": "arrow", "p": [[500, 560], [500, 620]], "c": AMBER, "w": 2.4, "in": .7},
        {"k": "circle", "x": 820, "y": 900, "r": 34, "fill": "#5b5550", "c": "#e8e2d6", "w": 1.4, "in": .9},
        {"k": "label", "x": 820, "y": 970, "t": "hammerstone", "st": "small", "in": 1.0},
        {"k": "cap", "x": 500, "y": 480, "t": "lower it, mark the high spots, pound, repeat", "in": .5},
        {"k": "label", "x": 500, "y": 1190, "t": "Jean-Pierre Protzen reproduced the fit and the texture, 1980s", "c": AMBER, "in": 1.3}]}
    tl, ax = timeline(900, 1600, [(900, "900"), (1100, "1100"), (1300, "1300"), (1500, "1500 CE")], "The hill above Cusco")
    tl["els"] += [{"k": "band", "x0": ax.x(900), "x1": ax.x(1400), "y": 560, "h": 16, "c": "#c9ad85", "op": .8, "t": "the Killke culture on the hill", "in": .3}] + \
                 event(ax, 1440, "Inca works begin", row=1, c=GOLD, i=.6, sub="traditionally under Pachacuti") + event(ax, 1536, "the siege", row=0, c=RED, i=.9) + \
                 event(ax, 1553, "Cieza de León writes", row=2, c=BONE, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 2, ["[d:intrigue][k:SACSAYHUAMÁN · PERU][sfx:boom][act:measured, setting the scene]Stones of well over a ^hundred tonnes. [act:describing, admiring][tune:level]Cut into ^many-sided shapes. [act:the marvel, slower]Fitted so ^tightly you can't slide a ^knife blade between them.",
                      "[d:tension][cam:1.12|0|0][act:posing the riddle][tune:rise]The ^Incas? [act:the other option, lower][tune:fall]Or someone ^before them?"], cut=False),
        B("world", 0, ["[d:calm][k:THE PLACE][act:plain, painting the picture]On the hill above Cusco, three terraced walls ^zigzag for up to ^four hundred metres. [go:1|0][act:lighter, a sense of height]Three thousand seven hundred metres ^up in the Andes."]),
        B("collision", 2, ["[d:build][k:THE CASE][act:fair-minded, presenting the case]Graham Hancock and others say the giant walls are ^older, and the Incas built on ^top. [act:pointing, inviting a look][tune:level]Look: ^huge, perfect@adj blocks at the ^bottom. [act:the contrast, completing it][tune:fall]^Smaller, rougher masonry ^above."]),
        B("cost", 3, ["[d:build][k:THE RECORD][act:historical, steady]Spanish soldiers fought over these walls in {1536|fifteen thirty-six}. [act:the key point, calm]The chroniclers, writing within a ^generation, describe an ^Inca work.",
                      "[d:build][sfx:shimmer][act:quoting the source, impressed]Cieza de León: ^twenty thousand workers on rotation. [act:counting them off][tune:level]^Four thousand ^quarrying. [act:finishing the count][tune:fall]^Six thousand ^hauling with ropes."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, curious][tune:rise]The ^smaller stones up top? [act:simple, a little sad][tune:fall]Many are ^gone. [sfx:hit][act:the explanation, clear]After the siege, the Spanish ^carted them down to build colonial Cusco, and left the ones too ^big to move.",
                          "[d:build][act:the next clue, light][tune:rise]And the ^fit? [act:practical, a craftsman's rhythm]An architect reproduced it with hammerstones: ^lower the block, ^mark the high spots, ^pound, ^repeat."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]An ^older civilisation's walls? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:a fair concession]People lived on the hill ^before the Incas. [act:precise, the crux][tune:fall]No ^older wall has been ^dated.",
                     "[d:tension][p:0.93][act:hopeful, quietly practical]^One radiocarbon date from behind the ^giants would settle it."]),
    ]
    return EP("sacsayhuaman", "06.03", "Sacsayhuamán: Walls That Fit Like a Jigsaw", "sacsayhuaman", "unsupported", "Did the Incas build Sacsayhuamán's giant walls, or inherit them?", "You can't slide a *knife* between them.", beats, shots,
              "Protzen 1985, 1986 · Cieza de León 1553 · Garcilaso de la Vega 1609 · Bauer 2004 · Hemming & Ranney 1982",
              "Hundred-tonne stones fitted without mortar above Cusco: the case for an older builder, the Spanish eyewitnesses, where the smaller stones went, and a hammerstone experiment.",
              ["#Sacsayhuaman", "#Inca", "#Peru", "#AncientEngineering", "#Mystery"])


def sacsayhuaman_m():
    """Sacsayhuamán as one continuous take: a jigsaw of giants a knife can't enter, three zigzags as long as four football pitches,
    two styles and the claim of two builders, a chronicle and 20,000 workers, the upper wall carted off to Cusco, the hammerstone cycle."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(sacsayhuaman())
    S = ep["shots"]
    # 2 · the jigsaw wall (the hook, then the case)
    wall = jigsaw(110, 640, 780, 520, 6, 4)
    giant = next(e for e in wall if e["fill"] == "#d9c9a6")["p"]
    piece = wall[0]["p"]
    corners = [p for p in giant if p[1] < 1159] + [[526.6, 1160.0], [276.1, 1160.0]]
    jig = {"base": "dark", "floor": 1160, "cam": [1, 500, 880], "els": wall + [
        person(918, 1160, 140, 1.2),
        {"k": "poly", "p": giant, "fill": "none", "c": GOLD, "w": 4, "curve": True, "in": 4.6, "fx": "draw", "dur": 1.0}, glow(395, 1040, 170, 4.8, .45),
        label(395, 1050, "100+ t", 5.6, INK, 40, st="serif", halo=False)] +
        [dot(x, y, 7, GOLD, round(7.0 + .1 * k, 2)) for k, (x, y) in enumerate(corners)] +
        [{"k": "poly", "p": [[x, y - 70] for x, y in piece], "fill": "rgba(201,184,148,.18)", "c": BN, "w": 2.5, "curve": True, "style": "inferred", "in": 9.2, "fx": "draw", "dur": .8},
         arrow([[180, 700], [180, 610]], 9.4, BN, 3, dur=.4, curve=False)] +
        [line([[p[0], p[1]] for p in giant[4:9]], 12.0, "#fff3dc", 5, dur=.9, curve=True), glow(500, 1000, 90, 12.2, .6)] +
        [{"k": "poly", "p": [[500, 1000], [660, 985], [660, 1004]], "fill": "#d8dde2", "c": "#9aa0a8", "w": 1.5, "in": 15.8, "fx": "pop"},
         bx(660, 982, 80, 24, "#5a3a22", "#8a5d33", 1.5, 6, 15.8), line([[480, 984], [500, 1004]], 17.0, RD, 5, draw=False), line([[480, 1004], [500, 984]], 17.0, RD, 5, draw=False)] +
        [person(330, 470, 110, 19.4, c="#e8c35a"), label(330, 512, "the Incas?", 19.6, GOLD, 30),
         {"k": "lib", "k2": "person", "x": 670, "y": 470, "h": 110, "color": "#c9c1ee", "op": .5, "keepop": True, "in": 20.8, "fx": "rise"}, label(670, 512, "before them?", 21.0, LILAC, 30)]}
    rough = [bx(118 + 34 * k + (6 if k % 2 else 0), 586 - (k % 3) * 4, 30, 50 + (k % 3) * 4, "#a8977c", "#2a2219", 1.5, 3, round(5.0 + .03 * k, 2)) for k in range(22)]
    case = [bx(104, 634, 792, 532, "none", LILAC, 3, 8, 2.4, style="claimed"), label(500, 1215, "older?", 3.4, LILAC, 34)] + rough + \
           [glow(500, 1000, 380, 8.0, .4), bx(110, 576, 780, 66, "none", AMB, 3, 6, 10.0, fx="draw", dur=.8),
            dot(70, 900, 22, LILAC, 12.6), label(70, 910, "1", 12.7, INK, 26, halo=False, st="serif"), dot(70, 609, 22, AMB, 13.2), label(70, 619, "2", 13.3, INK, 26, halo=False, st="serif")]
    # 0 · the terraces: three zigzags, about four football pitches long
    s0 = _spin(_bare(S[0]), .3); s0["cam"] = [1, 500, 880]
    zz = lambda y, off: [[-42 + 12 * k, y + 5.5, off + (9 if k % 2 else 0)] for k in range(8)]
    s0["els"] += [_ov(s0, [{"t": "line", "p": zz(y, off), "c": GOLD, "w": 5}], 4.5 + .5 * i, fx="draw", dur=1.0) for i, (y, off) in enumerate(((0, 14), (5.5, 2), (11, -10)))] + \
        [_ov(s0, [{"t": "line", "p": [[-42, 18, -14], [42, 18, -14]], "c": BN, "w": 3}, _lab(0, 18, -14, "400 m", BN, -14)], 9.8, fx="draw", dur=.8)] + \
        [x for k in range(4) for x in (bx(140 + 180 * k, 1290, 176, 110, "#3f6b3a", "#e8e2d6", 2, 3, round(11.2 + .25 * k, 2), fx="pop"),
                                         line([[228 + 180 * k, 1290], [228 + 180 * k, 1400]], round(11.3 + .25 * k, 2), "#e8e2d6", 2, draw=False),
                                         ring(228 + 180 * k, 1345, 18, round(11.3 + .25 * k, 2), "#e8e2d6", 2, dur=.3))] + \
        [line([[140, 1270], [860, 1270]], 12.0, BN, 3, dur=.6), label(500, 1252, "four football pitches", 12.4, BN, 30)]
    # 3 · the record: the siege of 1536, a chronicle within a generation; 20,000 workers, 4,000 quarrying, 6,000 hauling
    X = lambda yr: 160 + 680 * (yr - 1500) / 80
    rec = {"base": "dark", "cam": [1, 500, 880], "els": [line([[X(1500), 560], [X(1580), 560]], .3, "#8c7152", 3, dur=1.0),
           label(X(1500), 610, "1500", .4, "#9a938a", 26), label(X(1580), 610, "1580", .4, "#9a938a", 26),
           dot(X(1536), 560, 10, RD, 3.6), line([[X(1536) - 34, 470], [X(1536) + 34, 530]], 3.8, BN, 5), line([[X(1536) + 34, 470], [X(1536) - 34, 530]], 3.9, BN, 5),
           label(X(1536), 610, "1536", 4.0, RD, 30),
           {"k": "arrow", "p": [[X(1536), 450], [X(1546), 420], [X(1556), 450]], "c": AMB, "w": 3, "curve": True, "fx": "draw", "dur": .8, "in": 9.6},
           label(X(1546), 395, "a generation", 10.2, AMB, 28),
           bx(X(1556) - 40, 470, 80, 70, "#e8dcc2", "#8a7a66", 2, 4, 11.0, fx="pop"), line([[X(1556) - 28, 492], [X(1556) + 28, 492]], 11.2, INK, 2, draw=False),
           line([[X(1556) - 28, 512], [X(1556) + 18, 512]], 11.2, INK, 2, draw=False), dot(X(1556), 560, 10, AMB, 11.0),
           label(X(1556) + 60, 520, "an Inca work", 12.3, GOLD, 30, a="start")]}
    fig = lambda k: (150 + 38 * (k % 20), 780 + 54 * (k // 20))
    work = [person(*fig(k), 40, round(2.6 + .01 * k, 2), c="#8a8378", fx="pop") for k in range(200)] + \
           [label(500, 1360, "each figure: 100 workers", 4.6, "#cbbca8", 28)] + \
           [person(*fig(k), 40, round(5.0 + .012 * j, 2), c=AMB, fx="pop") for j, k in enumerate(range(40))] + [label(150, 730, "4,000 quarrying", 5.4, AMB, 30, a="start")] + \
           [person(*fig(k), 40, round(6.6 + .01 * j, 2), c=BLUE, fx="pop") for j, k in enumerate(range(40, 100))] + [label(850, 730, "6,000 hauling", 7.2, BLUE, 30, a="end")]
    # 4 · the upper wall gone to build colonial Cusco; the giants too big to move; then the hammerstone cycle
    gi = [{"k": "poly", "p": p, "fill": "#d9c9a6", "c": "#2a2219", "w": 2.4, "curve": True, "in": .3 + .15 * k} for k, p in enumerate((
        [[120, 760], [200, 640], [330, 620], [360, 700], [340, 790]], [[340, 790], [360, 700], [330, 620], [470, 600], [560, 640], [540, 790]],
        [[540, 790], [560, 640], [690, 615], [760, 660], [740, 790]]))]
    ghost = [bx(130 + 50 * k, 470 + 52 * (k // 6), 46, 48, "none", "#cbbca8", 2, 3, round(1.2 + .04 * k, 2), style="inferred") for k in range(6)] + \
            [bx(160 + 50 * k, 522, 46, 48, "none", "#cbbca8", 2, 3, round(1.5 + .04 * k, 2), style="inferred") for k in range(10)] + \
            [bx(380 + 50 * k, 470, 46, 48, "none", "#cbbca8", 2, 3, round(1.4 + .04 * k, 2), style="inferred") for k in range(6)] + [label(400, 445, "gone", 4.6, LILAC, 32)]
    town = [{"k": "house", "x": 690 + 70 * k, "y": 1010 + (k % 2) * 12, "w": 60, "h": 40, "fill": "#8e7152", "in": 11.0 + .15 * k} for k in range(3)] + \
           [bx(880, 930, 36, 92, "#8e7152", "rgba(255,236,206,.4)", 1, 2, 11.5), {"k": "poly", "p": [[876, 930], [898, 900], [920, 930]], "fill": "#6b4a2e", "c": "none", "w": 0, "in": 11.5},
            label(790, 1075, "colonial Cusco", 12.0, AMB, 30)] + \
           [arrow([[x0, 520], [x0 + 150, 760], [720, 960]], round(7.2 + .3 * k, 2), AMB, 3, "inferred", 1.2) for k, x0 in enumerate((250, 450, 600))] + \
           [bx(x, y, 24, 22, "#a8977c", "#2a2219", 1, 2, round(8.0 + .3 * k, 2), fx="pop") for k, (x, y) in enumerate(((380, 700), (560, 760), (660, 880)))]
    cart = {"base": "dark", "floor": 790, "cam": [1, 500, 880], "els": [line([[90, 790], [930, 790]], .2, "#8c7152", 3, draw=False)] + gi + ghost + town +
            [glow(440, 700, 300, 14.6, .45), label(440, 860, "too big to shift", 16.0, GOLD, 32)]}
    cyc = [oval(250, 1040, 52, 48, "#6a645c", "#cbbca8", 2, 1, 3.0), label(250, 1130, "hammerstone", 3.8, BN, 28), bx(360, 1000, 140, 90, "#c9b894", "#2a2219", 2, 4, 4.6),
           label(430, 1130, "softer block", 5.6, "#cbbca8", 26)] + \
          [bx(120 + 200 * k, 1240, 120, 60, "#c9b894", "#2a2219", 2, 4, round(6.3 + 1.2 * k, 2)) for k in range(4)] + \
          [bx(120, 1180, 120, 50, "#d9c9a6", "#2a2219", 2, 4, 6.4), arrow([[180, 1150], [180, 1176]], 6.6, BN, 3, dur=.3, curve=False), label(180, 1360, "lower", 6.7, BN, 28),
           dot(350, 1240, 7, RD, 7.8), dot(380, 1242, 7, RD, 7.9), dot(410, 1240, 7, RD, 8.0), label(380, 1360, "mark", 8.0, RD, 28),
           oval(580, 1200, 26, 24, "#6a645c", "#cbbca8", 2, 1, 9.0), line([[555, 1232], [545, 1222]], 9.3, AMB, 3, draw=False), line([[605, 1232], [615, 1222]], 9.3, AMB, 3, draw=False),
           label(580, 1360, "pound", 9.2, AMB, 28),
           {"k": "arrow", "p": [[780 + 40 * math.cos(a), 1270 + 40 * math.sin(a)] for a in [k * .4 + 3.6 for k in range(14)]], "c": GOLD, "w": 3, "curve": True, "fx": "draw", "dur": .7, "in": 10.6},
           label(780, 1360, "repeat", 10.8, GOLD, 28)]
    # 6 → back to the hill: the claim of older walls, the people before the Incas, the fill that would date it
    verdict = [_ov(s0, [_hi(box(0, 2, -8, 92, 40, 7.6), LILAC, .5, "claimed"), _lab(0, -8, 22, "older walls?", LILAC, 40)], .8, fx="draw", dur=1.0)] + \
              [_ov(s0, [{"t": "person", "x": -30 + 9 * k, "y": 16.5, "z": -12, "h": 1.7, "color": "#e8d6b8"}], 4.4 + .15 * k, fx="rise") for k in range(4)] + \
              [_ov(s0, [_lab(-12, 16.5, -12, "before the Incas", BN, -50)], 5.2), _ov(s0, [{"t": "q", "x": 0, "y": -4, "z": 4, "c": LILAC, "size": 70}], 7.6, fx="pop")]
    fill = [_ov(s0, [_hi(box(0, 4, 0, 80, 12, 5.4, "#8a6a48"), "#c9a070", .6, "inferred"), _lab(-30, 2.7, 4, "fill", "#e8c88a", 10)], 1.0, fx="draw", dur=1.0),
            _ov(s0, [box(6, 6, 2.0, 1.2, 1.2, 1.0, "#1a1511", "rgba(255,236,206,.8)"), {"t": "glow", "x": 6, "y": 2.5, "z": 6, "r": 70, "kind": "lamp"}], 7.4, fx="pop"),
            _ov(s0, [_lab(6, 3.2, 6, "charcoal", AMB, -24)], 7.8)]
    _beats(ep, {})
    return _take(ep, scenes={0: s0, 2: jig, 3: rec, 4: cart}, alias={5: 4, 6: 0},
                 beat_adds={2: (case, None), 5: (verdict, [1.15, 500, 960])},
                 line_adds={(3, 1): (work, None), (4, 1): (cyc, None), (5, 1): (fill, None)})


# ---------------------------------------------------------------- 06.04 Gunung Padang
def gunung_padang():
    hill = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 56, "prof": [[-70, 0], [70, 0], [52, 6], [30, 13], [-30, 13], [-52, 6]], "c": "#4f6a3a", "edge": "rgba(255,236,206,.25)"}] + \
           [box(-24 + i * 12, 0, 13, 12, 22 - i * 2, 1.6 * (i + 1), "#b5b09c", "rgba(0,0,0,.35)") for i in range(5)] + \
           [{"t": "line", "p": [[-52, 6.2, 0], [-40, 9.5, 0], [-30, 13.2, 0]], "c": GOLD, "w": 3, "op": .9},
            {"t": "person", "x": -27, "y": 13, "z": 8, "h": 1.7},
            L_(12, 21, "five stone terraces on the summit", GOLD, z=0, dy=-24), L_(-46, 7, "about 370 steps", "#f2dcb4", z=0, dy=34), L_(0, 0, "a natural hill of volcanic rock · schematic", "#cfe6ff", z=28, dy=40)]
    s0 = iso(hill, cam=[1, 500, 900], s=5.6, x=540, y=990, az=-20, spin=1.2, el=.48, table=None)
    v = View(105.0, 109.2, -8.0, -5.6, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Gunung Padang", 107.0564, -6.9939, {"c": GOLD}), ("Jakarta", 106.85, -6.2, {"a": "end", "lx": -18}), ("Bandung", 107.61, -6.91, {})],
                 extra=[{"k": "label", "x": v.p(107.8, -7.7)[0], "y": v.p(107.8, -7.7)[1], "t": "Java", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    cols = [hexcol(x, z, 1.3, h) for x, z, h in ((-6, -2, 9), (-3.6, -.6, 10), (-1.2, -2, 8.6), (1.2, -.6, 9.6), (3.6, -2, 8.2), (-4.8, 1.6, 9.2), (-2.4, 3, 9.8), (0, 1.6, 8.8), (2.4, 3, 9.4), (4.8, 1.6, 8))] + \
           [{"t": "ext", "axis": "x", "x": 3, "y": 0, "at": 8, "d": 2.2, "prof": [[-5, 0], [5, 0], [5.6, 1.1], [5, 2.2], [-5, 2.2], [-5.6, 1.1]], "c": BASALT, "edge": "rgba(255,236,206,.28)"},
            {"t": "person", "x": 9, "y": 0, "z": 6, "h": 1.7},
            L_(0, 10.4, "columnar andesite: lava cools and cracks into prisms, by itself", GOLD, z=0, dy=-24), L_(3, 2.2, "a column, taken down and laid flat", "#cfe6ff", z=8, dy=40)]
    s2 = iso(cols, cam=[1, 500, 900], s=22, x=480, y=1010, az=-24, spin=1.2, el=.45, table=None)
    sec = {"base": "section", "tod": "dusk", "ground": 620, "lx": 130, "layers": [{"d": 0, "c": "#8c8a7c", "t": "the terraces · last 2,500 years or so"}, {"d": 90, "c": "#6d5a44", "t": "rubble and soil between the rocks: the dated layers"},
                                                                                    {"d": 330, "c": "#3f3d3a", "t": "the andesite body of the hill", "tex": "blocks", "to": .1}],
           "cam": [1, 500, 900], "els": [{"k": "q", "x": x, "y": y, "c": AMBER, "size": 44, "in": .8 + i * .2} for i, (x, y) in enumerate(((330, 1060), (620, 1180), (760, 1010)))] +
           [{"k": "label", "x": 500, "y": 1320, "t": "the 'chambers': shapes in the scans · never opened", "c": "#ffb09a", "in": 1.4}]}
    s3 = sec
    s4 = stat("27,000", "years", "the age claimed in 2023 in Archaeological Prospection; the journal retracted the paper in March 2024", "Natawidjaja et al. 2023; retraction notice 2024")
    s5 = quote("Not associated with any artifacts or features that could be reliably interpreted as man-made.", "retraction notice · 2024", y=700, size=42)
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 4, ["[d:intrigue][k:GUNUNG PADANG · JAVA][sfx:boom][act:setting it up, a little awed]In {2023|twenty twenty-three}, a ^science journal published it: a pyramid in Java, begun twenty-seven ^thousand years ago.",
                      "[d:tension][cam:1.12|0|0][act:dropping the voice][tune:level]A few ^months later... [act:dry, a small shrug][tune:fall]the journal took it ^back. [act:genuinely curious, inviting][tune:fall]What ^happened?"], cut=False),
        B("world", 0, ["[d:calm][k:THE PLACE][act:warm, generous]The site is ^real, and beautiful: five stone terraces on a hilltop, reached by about three hundred and ^seventy steps. [go:1|0][act:lighter, placing it]In the hills of ^West Java."]),
        B("collision", 3, ["[d:build][k:THE CASE][act:fair, presenting his work]A geologist, Danny Hilman Natawidjaja, scanned the hill with radar and drills and saw ^building phases inside, with ^chambers. [act:teasing it out][tune:rise]The ^oldest? [act:the big number, let it land][tune:fall]Over twenty ^thousand years.",
                           "[d:aside][act:a light aside, quicker]Graham Hancock ^opened his Netflix series with it."]),
        B("cost", 2, ["[d:build][k:THE STONES][act:turning to the evidence, crisp]Now the ^stones. [act:explaining, a touch of wonder]Columnar andesite: lava that cools and cracks into long, neat ^prisms, all by ^itself. [go:3|0][act:the telling detail, pointed]And the dates came from ^soil between the rocks.",
                      "[d:build][sfx:hit][act:counting them off, firm][tune:fall]No ^tools, no ^hearths, no ^bones in any dated layer."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:the explanation, measured]That's ^why the paper was withdrawn: the dated soil wasn't tied to anything clearly made by ^people. [d:build][act:fair to them, even]The team calls the retraction ^unjust.",
                          "[d:build][act:sincere, even-handed]And here's the ^fair part: nobody has dug ^deep into the hill. [act:hopeful, fresh news]A ^dig began in {2025|twenty twenty-five}. [act:patient, a small smile][tune:fallrise]Its results aren't ^published yet."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A ^twenty-seven-thousand-year-old pyramid? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the humbler option, lighter][tune:rise]^Terraces from the last ^few thousand years? [act:plain, grounded][tune:fall]That's what we can ^see.",
                     "[d:tension][p:0.93][act:quiet, practical resolve]One ^deep, ^published trench would end the argument."]),
    ]
    return EP("gunung-padang", "06.04", "Gunung Padang: The Pyramid That Was Retracted", "gunung-padang", "unsupported", "Is there a human-made structure tens of thousands of years old inside Gunung Padang?", "The journal took it *back*.", beats, shots,
              "Natawidjaja et al. 2023, Archaeological Prospection (retracted 2024) · Retraction notice 2024 · Natawidjaja 2024 · Hancock 2022, Ancient Apocalypse",
              "A hilltop of stone terraces in Java, hailed as a 27,000-year-old pyramid and then retracted: the natural columns, the dated soil, and the deep dig that would decide it.",
              ["#GunungPadang", "#AncientApocalypse", "#Indonesia", "#Archaeology", "#Mystery"])


def gunung_padang_m():
    """Gunung Padang as one continuous take: a journal's pyramid, stamped retracted; five terraces and 370 steps; radar, a drill and the
    claimed chambers inside a cutaway hill; lava cracking into prisms like drying mud; dated soil that dates only soil; the deep trench."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(gunung_padang())
    S = ep["shots"]
    PAPER = "#efe6d2"

    def tv(x, y, at):
        return [bx(x, y, 200, 130, "#15100c", "#cbd2d8", 4, 14, at), line([[x + 50, y], [x + 25, y - 34]], at, "#cbd2d8", 3, draw=False), line([[x + 150, y], [x + 175, y - 34]], at, "#cbd2d8", 3, draw=False),
                {"k": "poly", "p": [[x + 60, y + 105], [x + 100, y + 35], [x + 140, y + 105]], "fill": "none", "c": LILAC, "w": 3, "in": at + .3, "fx": "draw", "dur": .5}]
    # 4 · the hook: a journal, a pyramid inside a hill, 27,000 years (a thousand generations); then stamped: retracted
    page = [bx(270, 470, 460, 560, PAPER, "#8a7a66", 2, 6, .3), bx(300, 500, 400, 30, "#3a5a7a", r=3, at=.6)] + \
           [line([[300, 560 + 22 * j], [700 - 60 * (j % 3), 560 + 22 * j]], .8 + .05 * j, "#8a7a66", 3, draw=False) for j in range(4)] + \
           [{"k": "poly", "p": [[320, 920], [420, 790], [580, 780], [680, 920]], "fill": "#6f8a4a", "c": "#3a4a2a", "w": 2, "curve": True, "in": 4.6},
            {"k": "poly", "p": [[400, 910], [500, 760], [600, 910]], "fill": "rgba(201,193,238,.18)", "c": LILAC, "w": 3, "style": "claimed", "in": 5.4, "fx": "draw", "dur": .9},
            label(500, 1000, "27,000 years", 9.0, INK, 40, st="serif", halo=False)] + \
           [{"k": "lib", "k2": "person", "x": 880 - 40 * k, "y": 1180, "h": 50, "color": "#e8d6b8", "op": round(1 - k * .042, 2), "keepop": True, "in": round(11.0 + .06 * k, 2)} for k in range(20)] + \
           [label(500, 1240, "1,000 generations", 12.4, BN, 30)]
    stamp = [strike(280, 1020, 720, 480, 2.0, RD, 8),
             {"k": "group", "tr": "rotate(-14 500 700)", "in": 2.6, "fx": "pop", "els": [bx(330, 650, 340, 90, "rgba(255,138,122,.12)", RD, 6, 10), label(500, 715, "RETRACTED", -1, RD, 52, st="serif")]}] + \
            question(860, 420, 4.0, 90)
    hook = {"base": "dark", "cam": [1, 500, 880], "els": page}
    # 0 · the site: five terraces, about 370 steps
    s0 = _spin(_bare(S[0]), .3); s0["cam"] = [1.1, 520, 940]
    ter = [box(-24 + i * 12, 0, 13, 12, 22 - i * 2, 1.6 * (i + 1), "#b5b09c") for i in range(5)]
    s0["els"] += [_ov(s0, [_hi(t, op=.25), _rim(t)], round(5.0 + .4 * i, 2), fx="draw", dur=.6) for i, t in enumerate(ter)] + \
        [_ov(s0, [{"t": "line", "p": [[-52 + 2.2 * k, 6.2 + .7 * k, 0], [-52 + 2.2 * k, 6.2 + .7 * k + .7, 0]], "c": GOLD, "w": 3} for k in range(10)], 8.8, fx="draw", dur=.8),
         _ov(s0, [_lab(-50, 6.2, 0, "370 steps", GOLD, 44)], 9.6)]
    # 3 · the cutaway hill: a body of columnar rock under rubble and soil; radar, a drill, the claimed phases and chambers
    import random
    rr = random.Random(11)
    outer = [[40, 1420], [130, 1230], [240, 1010], [330, 830], [400, 730], [600, 730], [670, 830], [760, 1010], [870, 1230], [960, 1420]]
    inner = [[150, 1420], [230, 1260], [330, 1060], [420, 900], [580, 900], [670, 1060], [770, 1260], [850, 1420]]

    def top_at(x, pts):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return 1420
    joints = []
    for k in range(17):
        x = 175 + 40 * k + rr.uniform(-8, 8)
        y0 = top_at(x, inner) + 14
        if y0 > 1380:
            continue
        lean = rr.uniform(-10, 10)
        joints.append(line([[round(x, 1), round(y0, 1)], [round(x + lean, 1), 1420]], round(.6 + .03 * k, 2), "#24221f", 3, draw=False))
    pockets = [{"k": "poly", "p": [[x - 9, top_at(x, inner) + 10], [x + 9, top_at(x, inner) + 10], [x + 2, top_at(x, inner) + 70]], "fill": "#8a6a48", "c": "none", "w": 0, "in": .9}
               for x in (300, 380, 455, 535, 610, 690)]
    sec = {"base": "dark", "stars": 60, "cam": [1, 500, 880], "els": [
        {"k": "poly", "p": outer, "fill": "#6d5a44", "c": "#c9a070", "w": 2, "curve": True, "in": .2, "fx": "fill", "dur": .8},
        {"k": "poly", "p": inner, "fill": "#45423d", "c": "#2a2722", "w": 2, "curve": True, "in": .4, "fx": "fill", "dur": .8}] + joints + pockets +
        [bx(400 + 40 * k, 730 - 10 * (k + 1), 40, 10 * (k + 1), "#b5b09c", "#2a2219", 1.5, 1, round(1.0 + .1 * k, 2)) for k in range(5)] +
        [person(420, 720, 70, 1.4),
         bx(505, 662, 30, 22, "#2a2722", "#9fd0ff", 2, 3, 3.2), {"k": "fan", "x": 520, "y": 690, "r": 520, "a0": 60, "a1": 120, "in": 4.6},
         line([[600, 680], [600, 1250]], 10.4, "#cbd2d8", 4, dur=1.6), bx(586, 630, 28, 54, "#8a8378", "#cbd2d8", 2, 3, 10.4),
         {"k": "core", "x": 860, "y": 1120, "w": 46, "h": 300, "grooves": 7, "in": 12.6, "fx": "rise"}, arrow([[640, 900], [820, 900]], 12.4, BN, 3, dur=.5, curve=False)] +
        [{"k": "poly", "p": [[500 - w, 730 + d], [500 + w, 730 + d], [500 + w + 70, 730 + d + 150], [500 - w - 70, 730 + d + 150]], "fill": "none", "c": LILAC, "w": 3, "style": "claimed",
          "in": round(19.6 + .4 * j, 2), "fx": "draw", "dur": .6} for j, (w, d) in enumerate(((120, 40), (200, 220), (290, 400)))] +
        [bx(x, y, 90, 56, "rgba(201,193,238,.14)", LILAC, 3, 6, round(21.0 + .2 * j, 2), style="claimed") for j, (x, y) in enumerate(((330, 960), (530, 1110)))] +
        [label(375, 1000, "?", 21.4, LILAC, 40, st="serif"), label(575, 1150, "?", 21.6, LILAC, 40, st="serif"), label(500, 1330, "20,000+ years?", 23.6, LILAC, 34)]}
    netflix = tv(700, 380, .6)
    # 2 · the stones: lava cracks into prisms by itself, like mud drying into tiles
    s2 = _spin(_bare(S[2]), .3); s2["cam"] = [1.12, 500, 840]
    cols = [(x, z, h) for x, z, h in ((-6, -2, 9), (-3.6, -.6, 10), (-1.2, -2, 8.6), (1.2, -.6, 9.6), (3.6, -2, 8.2), (-4.8, 1.6, 9.2), (-2.4, 3, 9.8), (0, 1.6, 8.8), (2.4, 3, 9.4), (4.8, 1.6, 8))]
    hexes = lambda cx, cy, r: [[round(cx + r * math.cos(a), 1), round(cy + r * math.sin(a), 1)] for a in [k * math.pi / 3 for k in range(7)]]
    cells = [(150 + 52 * i + (26 if j % 2 else 0), 400 + 45 * j) for j in range(4) for i in range(6)]
    s2["els"] += [bx(140, 360, 320, 200, "#d0502a", r=10, at=3.2), glow(300, 460, 200, 3.2, .8, "red"), label(300, 600, "lava", 3.5, "#ff9a6a", 30),
                  bx(140, 360, 320, 200, "#3a3733", r=10, at=4.6, op=.85, dur=1.5)] + \
                 [{"k": "line", "p": hexes(x, y, 30), "c": "#e8b87a", "w": 2.5, "in": round(5.0 + .04 * k, 2), "fx": "draw", "dur": .3} for k, (x, y) in enumerate(cells) if 150 < x < 450 and 365 < y < 555] + \
                 [_ov(s2, [{"t": "line", "p": [[x + 1.3 * math.cos(k * math.pi / 3), h, z + 1.3 * math.sin(k * math.pi / 3)] for k in range(7)], "c": GOLD, "w": 3}], round(6.2 + .1 * j, 2), fx="draw", dur=.4)
                  for j, (x, z, h) in enumerate(cols)] + \
                 [bx(540, 380, 320, 170, "#8a6a48", r=10, at=8.4), glow(840, 360, 90, 8.6, .8, "sun"), dot(840, 360, 22, "#ffe2a8", 8.6)] + \
                 [line(p, round(9.0 + .08 * k, 2), "#3a2a1a", 3, dur=.3) for k, p in enumerate((
                     [[600, 380], [630, 430], [610, 480], [640, 550]], [[630, 430], [700, 450], [730, 380]], [[700, 450], [720, 520], [700, 550]], [[720, 520], [800, 500], [830, 550]],
                     [[800, 500], [790, 430], [840, 400]], [[610, 480], [560, 470]], [[790, 430], [880, 450]]))] + [label(720, 600, "drying mud", 10.0, "#c9a070", 30)]
    # 3 (back) · the dates came from soil between the rocks
    soil = [x for k, (sx, sy) in enumerate(((300, top_at(300, inner) + 40), (455, top_at(455, inner) + 40), (535, top_at(535, inner) + 40), (610, top_at(610, inner) + 40), (690, top_at(690, inner) + 40))) for x in (dot(sx, sy, 9, GOLD, round(2.0 + .2 * k, 2)), glow(sx, sy, 50, round(2.0 + .2 * k, 2), .8))] + \
           [label(500, 860, "dated soil", 3.2, GOLD, 32)]
    nos = lambda x, at, ic, name: ic + [label(x, 540, name, at + .1, BN, 26), strike(x - 40, 510, x + 40, 420, at + .5, RD, 5)]
    tool = [{"k": "poly", "p": [[170, 420], [195, 470], [185, 500], [155, 500], [145, 470]], "fill": "#9aa0a8", "c": "#e8e2d6", "w": 2, "in": .4, "fx": "pop"}]
    hearth = [oval(310 + 18 * k, 495, 14, 10, "#6a645c", "none", 0, 1, 1.6) for k in range(3)] + [glow(328, 470, 50, 1.7, .9, "lamp"), dot(328, 475, 9, "#ffb060", 1.7)]
    bone = [line([[450, 470], [530, 450]], 4.6, "#efe6d2", 10, draw=False), dot(447, 464, 9, "#efe6d2", 4.6), dot(453, 478, 9, "#efe6d2", 4.6), dot(530, 444, 9, "#efe6d2", 4.6), dot(536, 458, 9, "#efe6d2", 4.6)]
    nothing = nos(170, .4, tool, "tools") + nos(328, 1.6, hearth, "hearths") + nos(490, 4.6, bone, "bones") + \
              [arrow([[455, 935], [430, 820], [440, 700]], 10.6, LILAC, 3, "claimed", .9), strike(390, 860, 490, 780, 12.0, RD, 5),
               label(300, 650, "a building?", 11.0, LILAC, 30)]
    # 5 · why it was withdrawn: a date has to be tied to what it dates; the team objects; the deep dig still to come
    tag = lambda x, y, at, c, style="known": [bx(x, y, 70, 40, "rgba(232,195,90,.15)" if style == "known" else "none", c, 3, 6, at, style=style), dot(x + 12, y + 20, 5, c, at)]
    why = {"base": "dark", "cam": [1, 500, 880], "els": [
        bx(120, 330, 200, 240, PAPER, "#8a7a66", 2, 4, .3), {"k": "poly", "p": [[150, 520], [220, 420], [290, 520]], "fill": "none", "c": LILAC, "w": 2, "style": "claimed", "in": .4},
        strike(130, 560, 310, 340, 1.6, RD, 6), label(220, 610, "withdrawn", 2.4, RD, 30),
        oval(260, 840, 110, 60, "#6d5a44", "#c9a070", 2, 1, 3.6), dot(230, 830, 6, GOLD, 3.8), dot(290, 850, 6, GOLD, 3.9), label(260, 940, "soil", 4.0, "#c9a070", 28)] +
        tag(380, 700, 9.6, GOLD) + [line([[392, 720], [300, 800]], 9.8, GOLD, 3, dur=.4), label(415, 680, "date", 10.0, GOLD, 28),
        {"k": "poly", "p": [[580, 900], [710, 700], [840, 900]], "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 14.6, "fx": "draw", "dur": .7},
        label(710, 940, "a pyramid?", 14.8, LILAC, 28)] + tag(560, 600, 15.3, GOLD, "inferred") + \
        [line([[572, 620], [640, 700]], 15.5, GOLD, 3, "inferred", .4), strike(560, 690, 680, 590, 16.0, RD, 5)] + \
        [person(220 + 60 * k, 1200, 120, round(17.6 + .15 * k, 2)) for k in range(3)] + \
        [{"k": "poly", "p": [[420, 1010], [740, 1010], [740, 1090], [470, 1090], [430, 1120], [440, 1090], [420, 1090]], "fill": "rgba(201,193,238,.1)", "c": LILAC, "w": 3, "in": 18.6, "fx": "pop"},
         label(580, 1063, "unjust!", 19.0, LILAC, 34)]}
    dig = [{"k": "poly", "p": [[60, 1560], [180, 1340], [380, 1240], [620, 1240], [820, 1340], [940, 1560]], "fill": "#4f6a3a", "c": "#8fb070", "w": 2, "in": .3, "curve": True},
           bx(400, 1222, 200, 18, "#b5b09c", "#2a2219", 1.5, 2, .5), line([[300, 1270], [360, 1300], [420, 1268]], 2.4, "#c9a070", 4, dur=.4),
           label(330, 1330, "shallow", 2.6, "#c9a070", 28),
           bx(470, 1260, 70, 300, "rgba(159,208,255,.08)", BLUE, 3, 4, 5.4, style="inferred", fx="fill", dur=1.4), label(560, 1420, "2025", 6.6, BLUE, 32, a="start"),
           bx(700, 1300, 150, 110, "none", "#cbbca8", 2, 4, 8.4, style="inferred"), label(775, 1368, "...", 8.6, "#cbbca8", 40, st="serif"), label(775, 1450, "not yet published", 8.8, "#cbbca8", 26)]
    # 6 → back to the hill: the claimed pyramid, the terraces we can see, and the trench that would decide
    verdict = [_ov(s0, [{"t": "pyr", "x": 0, "z": 0, "y": -2, "b": 80, "h": 38, "c": LILAC, "xray": True, "edge": LILAC, "op": 1.6, "style": "inferred"}, _lab(-22, 15, 22, "27,000 years?", LILAC, 0)], .8, fx="draw", dur=1.2)] + \
              [_ov(s0, [_rim(t, GOLD, 5) for t in ter], 4.0, fx="draw", dur=.8), glow(520, 900, 260, 4.2, .4)]
    trench = [_ov(s0, [_hi(box(-6, 0, -8, 10, 8, 21.5), BLUE, .4, "inferred"), _lab(-6, -8, 4, "a deep trench", BLUE, 40)], 1.0, fx="draw", dur=1.0),
              _ov(s0, [{"t": "glow", "x": -6, "y": -2, "z": 0, "r": 70, "kind": "lamp"}, box(-6, 0, -2.3, 1.2, 1.2, .5, "#ffb060", "rgba(0,0,0,0)")], 4.4, fx="pop")]
    shots = S[:4] + [hook, S[5], S[6]]
    ep["shots"] = shots
    out = _take(ep, scenes={0: s0, 2: s2, 3: sec, 4: hook, 5: why}, alias={6: 0},
                beat_adds={5: (verdict, [1.2, 520, 960])},
                line_adds={(0, 1): (stamp, None), (2, 1): (netflix, None), (3, 1): (nothing, None), (4, 1): (dig, [1.1, 500, 1150]), (5, 1): (trench, None)})
    return _inject(out, _go(out, 3, 0, 1), soil)


# ---------------------------------------------------------------- 06.05 Nan Madol
def nan_madol():
    def course(cx, cz, W, D, y, k, h=.9):
        """One course of a square wall of stacked basalt columns: lengthwise logs, then crosswise headers."""
        out = []
        if k % 2 == 0:
            out += [box(cx, cz - D / 2, y, W, h, h, BASALT), box(cx, cz + D / 2, y, W, h, h, BASALT), box(cx - W / 2, cz, y, h, D, h, "#524e48"), box(cx + W / 2, cz, y, h, D, h, "#524e48")]
        else:
            for s in (-1, 1):
                out += [box(cx + t, cz + s * D / 2, y, h * .8, 3.2, h, "#57534c") for t in [(-W / 2) + i * 2.4 for i in range(int(W / 2.4) + 1)]]
                out += [box(cx + s * W / 2, cz + t, y, 3.2, h * .8, h, "#57534c") for t in [(-D / 2) + i * 2.4 for i in range(1, int(D / 2.4))]]
        return out
    wall = [{"t": "flat", "pts": [[-40, -34], [40, -34], [40, 34], [-40, 34]], "y": -.2, "c": SEA, "op": .75, "ground": True},
            {"t": "slab", "x0": -26, "x1": 26, "z0": -22, "z1": 22, "y": 0, "c": "#cfc3a4"}] + \
           [b for k in range(7) for b in course(0, 0, 40, 32, k * .95, k)] + \
           [{"t": "person", "x": 24, "y": 0, "z": 19, "h": 1.7},
            L_(0, 7, "Nandauwas, the royal tomb · walls up to 7.5 m", GOLD, z=-16, dy=-24), L_(0, 0, "basalt columns stacked like a log cabin · schematic", "#cfe6ff", z=22, dy=40)]
    s0 = iso(wall, cam=[1, 500, 900], s=6.4, x=500, y=1000, az=-26, spin=1.2, el=.5, table=None)
    v = View(132, 172, -2, 18, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Pohnpei · Nan Madol", 158.34, 6.84, {"c": GOLD}), ("Guam", 144.8, 13.4, {}), ("Chuuk", 151.8, 7.4, {}), ("Kosrae", 163.0, 5.3, {"a": "start", "ly": 34})],
                 extra=[{"k": "label", "x": 500, "y": 420, "t": "the western Pacific · thousands of km of open ocean", "st": "small", "c": "#9fd0ff", "in": 1.0}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(500), "t": "500 km"}])
    import random
    r = random.Random(7)
    isl = []
    for k in range(46):
        a = -2.4 + k * .1; rr = 300 + r.uniform(-60, 60)
        x = 500 + rr * math.cos(a + 1.1) * 1.3; y = 1180 + rr * math.sin(a + 1.1) * .9 - 260
        w = r.uniform(26, 58); h = r.uniform(20, 44)
        isl.append({"k": "rect", "x": round(x - w / 2), "y": round(y - h / 2), "w": round(w), "h": round(h), "fill": "#57534c", "c": "#bdb3a0", "sw": 1, "in": .3 + k * .02})
    s2 = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "rect", "x": 60, "y": 560, "w": 880, "h": 740, "fill": "#1f4f6d", "c": "none", "sw": 0, "in": .1}] + isl +
          [{"k": "cap", "x": 500, "y": 480, "t": "about 92 islets and tidal canals · schematic", "in": .2},
           {"k": "label", "x": 500, "y": 1370, "t": "built on the reef flat, off Temwen Island", "st": "small", "c": "#9fd0ff", "in": 1.4}]}
    s3 = stat("c. 1180", "CE", "uranium-thorium dates on coral used in building Nandauwas, the royal tomb", "McCoy et al. 2016, Quaternary Research")
    tl, ax = timeline(1, 2100, [(1, "1 CE"), (500, "500"), (1000, "1000"), (1500, "1500"), (2000, "2000")], "Nan Madol through time")
    tl["els"] += [{"k": "band", "x0": ax.x(100), "x1": ax.x(1100), "y": 700, "h": 16, "c": "#c9ad85", "op": .8, "t": "people on the reef edge", "in": .3}] + \
                 event(ax, 1180, "the royal tomb is built", row=1, c=GOLD, i=.6) + event(ax, 1628, "the Saudeleur fall", row=2, c=RED, i=.9, sub="traditional date") + \
                 event(ax, 2016, "UNESCO: in danger", row=0, c=SCAN, i=1.2)
    s4 = tl
    s5 = like(s2, cam=[1.1, 500, 900])
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:NAN MADOL · MICRONESIA][sfx:boom][act:wonder, painting the scene]On a reef in the ^middle of the Pacific: a city of black stone ^logs. [act:letting the scale sink in]Nearly a ^hundred islands, built by ^hand.",
                      "[d:tension][cam:1.12|0|0][act:hushed, a storyteller's smile]The local legend says the stones ^flew."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:orienting, calm]Pohnpei, one of the most ^remote islands on Earth. [go:2|0][act:describing, steady]Off its coast, about ninety-two ^artificial islets, with ^canals between them.",
                       "[d:build][go:0|0][act:a builder's eye, explaining]The walls are basalt columns, stacked ^crosswise and lengthwise, like a ^log cabin. [act:the height, impressed]Up to ^seven and a half metres high."]),
        B("collision", 5, ["[d:build][k:THE CASE][act:the two big unknowns][tune:fall]^Who, and ^when? [sfx:shimmer][act:storytelling, a light touch]In the {1920s|nineteen twenties}, James Churchward called it a relic of ^Mu, a ^lost Pacific continent.",
                           "[d:build][act:respectful, taking it seriously]Graham Hancock took ^seriously the Pohnpeian stories of a ^sunken city out beyond the reef."]),
        B("cost", 3, ["[d:build][k:THE DATES][act:crisp, the turn][tune:fall]Then the ^lab. [act:precise, reading the result]Coral used@verb in building the royal tomb: about {1180|eleven eighty}.",
                      "[d:build][act:the next clue, curious][tune:rise]And the ^stone? [act:quietly conclusive]Its chemistry ties it to quarries on Pohnpei ^itself."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:warm, a pleasing fit]The island's ^own history ^agrees. [act:telling their history, with respect]The Saudeleur dynasty ruled ^all of Pohnpei from here, until a hero named Isokelekel ^overthrew them, traditionally around {1628|sixteen twenty-eight}.",
                          "[d:aside][sfx:hit][act:gentle, an affectionate smile]Maybe 'the stones ^flew' is how 'a very ^big job' sounds, twenty generations later."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Built by ^Pohnpeians, from about eleven eighty? [act:the verdict, warm and sure][tune:fall]^*Strong evidence*. [act:the other claim, lighter][tune:rise]A ^drowned city beyond the reef? [act:plain, honest][tune:fall]^Untested. [act:a playful invitation][tune:fall]^Divers wanted.",
                     "[d:tension][p:0.93][act:a gentle twist, wry]Today the ^real threat is ^mangroves."]),
    ]
    return EP("nan-madol", "06.05", "Nan Madol: The Basalt City on the Reef", "nan-madol", "strong", "Who stacked a city of basalt logs on a Pacific reef, and when?", "The legend says the stones *flew*.", beats, shots,
              "McCoy et al. 2016, Quaternary Research · McCoy & Athens 2011, Journal of Archaeological Science · Hanlon 1988 · Morgan 1988 · UNESCO 2016",
              "Nearly a hundred islets of stacked basalt columns on a Pacific reef: the lost-continent stories, the coral dates, the quarries, and the dynasty that ruled from it.",
              ["#NanMadol", "#Pohnpei", "#Pacific", "#Archaeology", "#Mystery"])


def nan_madol_m():
    """Nan Madol as one continuous take: a city of basalt logs on a reef, islets popping up along the coast with canals between them,
    a log-cabin wall taller than a house, a lost continent drawn and sunk, a coral hourglass that reads 1180, a dynasty and twenty
    generations of storytellers, and mangroves creeping in."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(nan_madol())
    S = ep["shots"]
    BAS = "#3a3733"
    # 0 · the city on the reef: islets around it, built by hand; the legend of flying stones
    s0 = _spin(_bare(S[0]), .3); s0["cam"] = [1, 500, 900]
    import random
    rr = random.Random(5)
    isl = []
    for k in range(18):
        a = 2 * math.pi * k / 18 + rr.uniform(-.1, .1); R = rr.uniform(31, 38)
        isl.append(box(round(R * math.cos(a), 1), round(R * math.sin(a) * .85, 1), -.2, round(rr.uniform(3, 6), 1), round(rr.uniform(3, 6), 1), round(rr.uniform(.6, 1.6), 1), "#4a4640", "rgba(255,236,206,.3)"))
    s0["els"] += [_ov(s0, [it], round(6.4 + .08 * k, 2), fx="pop") for k, it in enumerate(isl)] + \
        [_ov(s0, [{"t": "person", "x": 14 + 3 * k, "y": 0, "z": 20, "h": 1.7, "color": "#e8d6b8"}], round(8.8 + .2 * k, 2), fx="rise") for k in range(3)] + \
        []
    flew = [{"k": "group", "tr": "rotate(-24 260 470)", "in": .8, "fx": "pop", "els": [bx(200, 455, 130, 30, BAS, "#8a8378", 2, 12)]},
            {"k": "arrow", "p": [[330, 470], [470, 430], [560, 520], [560, 700]], "c": LILAC, "w": 3, "style": "claimed", "curve": True, "fx": "draw", "dur": 1.2, "in": 1.2},
            line([[180, 500], [140, 520]], 1.0, LILAC, 3, "claimed"), line([[190, 530], [150, 552]], 1.1, LILAC, 3, "claimed"), label(260, 400, "flying stones?", 1.6, LILAC, 32)]
    # 1 · the map: remote Pohnpei, a thousand and two thousand kilometres of ocean
    v = View(132, 172, -2, 18, (40, 330, 920, 900))
    px, py = v.p(158.34, 6.84)
    rings = [{"k": "circle", "x": px, "y": py, "r": round(v.km(d), 1), "fill": "none", "c": "#9fd0ff", "w": 2, "style": "inferred", "in": round(6.8 + .8 * j, 2), "fx": "draw", "dur": .9}
             for j, d in enumerate((1000, 2000))] + [label(px, py - v.km(1000) - 14, "1,000 km", 7.4, "#9fd0ff", 28), label(px, py - v.km(2000) - 14, "2,000 km", 8.2, "#9fd0ff", 28)]
    # 2 · the islets on the reef, the canals between them (then a lost continent, and a sunken city beyond the reef)
    rr = random.Random(7)
    lots = []
    for j in range(8):
        for i in range(12):
            if len(lots) >= 92:
                break
            x = 190 + i * 52 + j * 14 + rr.uniform(-6, 6); y = 600 + j * 52 + rr.uniform(-5, 5)
            if (i + j) % 7 == 3:
                continue
            lots.append((round(x), round(y), round(rr.uniform(30, 44)), round(rr.uniform(26, 40))))
    lots = lots[:92]
    plan = {"base": "map", "grid": 125, "cam": [1, 500, 880], "els": [
        {"k": "poly", "p": [[-20, 300], [620, 300], [560, 420], [420, 500], [240, 560], [-20, 590]], "fill": "#3a4a2a", "c": "#8fb070", "w": 2, "in": .2},
        label(220, 420, "Temwen Island", .6, "#cfe0b8", 30, st="ital"),
        {"k": "poly", "p": [[-20, 590], [240, 560], [420, 500], [560, 420], [620, 300], [1020, 300], [1020, 1080], [-20, 1080]], "fill": "#5fa8c9", "c": "none", "w": 0, "in": .3, "op": .35, "keepop": True},
        line([[-20, 1080], [1020, 1080]], .5, "#e8f4fa", 3, "inferred", 1.0), label(880, 1120, "the reef edge", 1.0, "#e8f4fa", 28, a="end")] +
        [bx(x, y, w, h, "#45423d", "#bdb3a0", 1.2, 3, round(1.4 + .03 * k, 2), fx="pop") for k, (x, y, w, h) in enumerate(lots)] +
        [label(500, 1050, "92 islets", 4.6, BN, 34)] +
        [line([[180 + 14 * j, 588 + 52 * j - 8], [820 + 14 * j, 588 + 52 * j - 8]], round(6.4 + .2 * j, 2), "#bfe6f5", 3, dur=.7, op=.8) for j in range(1, 8, 2)] +
        [{"k": "boat", "x": 560, "y": 732, "w": 60, "in": 9.4}, glow(560, 725, 60, 9.4, .5, "scan")]}
    who = question(330, 470, .6, 80) + question(680, 470, 2.0, 80) + \
          [{"k": "poly", "p": [[60, 1400], [40, 900], [120, 520], [360, 360], [700, 380], [930, 560], [960, 1000], [880, 1400]], "fill": "rgba(201,193,238,.07)", "c": LILAC, "w": 4,
            "style": "claimed", "curve": True, "in": 7.8, "fx": "draw", "dur": 1.4}, label(500, 1280, "Mu?", 8.4, LILAC, 64, st="serif"),
           arrow([[860, 620], [860, 900]], 10.6, LILAC, 4, "claimed", .8, False), label(850, 950, "sunk?", 11.0, LILAC, 30, a="end")]
    sunk = [bx(260 + 70 * k, 1180 + (k % 2) * 30, 56, 40, "rgba(201,193,238,.1)", LILAC, 2.5, 3, round(4.2 + .15 * k, 2), style="claimed") for k in range(6)] + \
           question(500, 1360, 5.4, 70)
    # 3 · the coral hourglass: uranium in, thorium out; c. 1180 CE; the stone's own fingerprint
    coral = [[150, 520], [150, 450], [120, 400], [150, 450], [185, 395], [150, 450], [150, 520], [200, 470], [230, 420], [200, 470], [150, 520]]
    hg = {"base": "dark", "cam": [1, 500, 880], "els": [
        bx(80, 340, 300, 230, "#1f4f6d", r=12, at=.3), line(coral, 1.6, "#f2b8a8", 7, dur=1.0), label(230, 610, "living coral", 2.2, "#f2b8a8", 28)] +
        [dot(110 + 30 * k, 360 + 10 * (k % 2), 6, "#d8f07a", round(3.6 + .25 * k, 2)) for k in range(6)] + [label(240, 316, "uranium", 4.4, "#d8f07a", 28)] +
        [line([[100, 540], [370, 530]], 6.4, RD, 4, "inferred", .5), label(400, 545, "cut", 6.6, RD, 28, a="start"),
         {"k": "poly", "p": [[640, 400], [800, 400], [740, 520], [800, 640], [640, 640], [700, 520]], "fill": "none", "c": BN, "w": 3, "in": 7.8, "fx": "draw", "dur": .8},
         {"k": "poly", "p": [[656, 410], [784, 410], [724, 508], [716, 508]], "fill": "#d8f07a", "c": "none", "w": 0, "in": 8.0},
         {"k": "poly", "p": [[716, 532], [724, 532], [784, 630], [656, 630]], "fill": "#c9a070", "c": "none", "w": 0, "in": 9.2, "fx": "fill", "dur": 3.0},
         line([[720, 508], [720, 630]], 9.0, "#d8f07a", 2, "inferred", .6), label(820, 450, "uranium", 8.4, "#d8f07a", 28, a="start"), label(820, 620, "thorium", 9.8, "#c9a070", 28, a="start"),
         bx(180, 760, 300, 260, BAS, "#8a8378", 2, 6, 13.4)] +
        [bx(180, 760 + 34 * k, 300, 30, "#45423d", "#2a2722", 1.5, 6, round(13.5 + .05 * k, 2)) for k in range(0, 8, 2)] +
        [dot(260 + 40 * k, 900 + 20 * (k % 2), 10, "#f2b8a8", round(14.2 + .1 * k, 2)) for k in range(4)] + [label(330, 1065, "the royal tomb", 14.4, BN, 28),
         arrow([[720, 660], [700, 820], [520, 880]], 15.2, GOLD, 3, dur=.8), label(720, 930, "c. 1180 CE", 16.0, GOLD, 48, st="serif")]}
    bars = lambda x0, at, c: [line([[x0 + dx, 1180], [x0 + dx, 1300]], round(at + .03 * j, 2), c, w, draw=False) for j, (dx, w) in enumerate(((0, 6), (14, 3), (24, 9), (42, 3), (52, 5), (66, 10), (84, 3), (96, 6), (112, 4)))]
    finger = [bx(180, 1150, 120, 170, BAS, "#8a8378", 2, 6, .4), label(240, 1360, "a pillar", .6, BN, 28)] + bars(360, 3.6, GOLD) + \
             [{"k": "poly", "p": [[640, 1320], [700, 1180], [800, 1160], [880, 1250], [850, 1330]], "fill": "#3a4a2a", "c": "#8fb070", "w": 2, "in": 6.6, "curve": True},
              dot(760, 1250, 9, GOLD, 6.8), label(760, 1370, "Pohnpei", 7.0, "#cfe0b8", 28)] + bars(540, 7.2, GOLD) + \
             [label(500, 1130, "match", 8.2, GOLD, 30), glow(500, 1240, 220, 8.2, .35)]
    # 4 · the island's own history: the Saudeleur rule, the hero of c. 1628, twenty generations of storytellers
    X = lambda yr: 150 + 700 * (yr - 1100) / 950
    tl = {"base": "dark", "cam": [1, 500, 880], "els": [line([[X(1100), 900], [X(2050), 900]], .3, "#8c7152", 3, dur=1.0)] +
          [label(X(y), 950, str(y), .5, "#9a938a", 26) for y in (1200, 1600, 2000)] +
          [bx(X(1180), 850, X(1628) - X(1180), 22, GOLD, r=11, at=4.2, fx="fill"), label((X(1180) + X(1628)) / 2, 830, "the Saudeleur", 4.8, GOLD, 32),
           {"k": "poly", "p": [[X(1400) - 30, 780], [X(1400) - 30, 740], [X(1400) - 15, 760], [X(1400), 735], [X(1400) + 15, 760], [X(1400) + 30, 740], [X(1400) + 30, 780]],
            "fill": GOLD, "c": "none", "w": 0, "in": 5.6, "fx": "pop"},
           person(X(1628), 900 - 30, 110, 8.2, c="#f2dcb4"), line([[X(1628), 840], [X(1628), 900]], 9.6, RD, 5, draw=False), glow(X(1628), 820, 90, 9.6, .6),
           label(X(1628), 990, "c. 1628", 11.4, RD, 30)]}
    gen = [person(round(X(1640) + (X(2025) - X(1640)) * k / 19, 1), 1090, 40, round(5.0 + .1 * k, 2), c="#cbbca8") for k in range(20)] + \
          [line([[X(1640), 1110], [X(2025), 1110]], 5.0, "#cbbca8", 2, "claimed", 2.0), label((X(1640) + X(2025)) / 2, 1160, "twenty generations", 6.8, BN, 30)] + \
          [{"k": "block", "x": 160, "y": 1300, "w": 120, "h": 50, "d": 24, "in": 2.6, "fx": "rise"}] + [person(150 + 30 * k, 1300, 50, round(2.8 + .1 * k, 2)) for k in range(5)] + \
          [label(230, 1360, "a very big job", 3.2, AMB, 28),
           {"k": "group", "tr": "rotate(-20 760 1250)", "in": 1.0, "fx": "pop", "els": [bx(700, 1235, 120, 30, BAS, "#8a8378", 2, 12)]},
           line([[680, 1290], [640, 1305]], 1.1, LILAC, 3, "claimed"), line([[690, 1315], [650, 1330]], 1.2, LILAC, 3, "claimed"), label(760, 1360, "the stones flew", 1.4, LILAC, 28)]
    # 6 → back to the city: built by Pohnpeians; a drowned city untested; divers wanted; mangroves
    verdict = [_ov(s0, [{"t": "person", "x": -12 + 5 * k, "y": 0, "z": 19, "h": 1.7, "color": "#e8d6b8"}], round(1.0 + .15 * k, 2), fx="rise") for k in range(6)] + \
              [label(500, 760, "c. 1180 CE", 2.6, GOLD, 40, st="serif"),
               _ov(s0, [_hi(box(0, -32, -6, 30, 8, 4), LILAC, .4, "claimed"), _lab(0, -2, -32, "drowned city?", LILAC, -10)], 5.0, fx="draw", dur=1.0),
               {"k": "group", "tr": "rotate(-70 800 1290)", "in": 7.6, "fx": "pop", "els": [{"k": "person", "x": 800, "y": 1320, "h": 70, "t": False, "color": "#9fd0ff"}]},
               dot(740, 1250, 6, "#bfe6f5", 7.9), dot(725, 1225, 5, "#bfe6f5", 8.0), dot(712, 1200, 4, "#bfe6f5", 8.1)]
    mang = [_ov(s0, [{"t": "cyl", "x": x, "z": z, "y": 0, "r": r, "h": h, "c": "#4f7a3a", "n": 10, "edge": "rgba(0,0,0,.2)"}], round(3.4 + .15 * k, 2), fx="pop")
            for k, (x, z, r, h) in enumerate(((-24, 21, 1.4, 1.6), (-18, 23, 1.1, 1.2), (24, -20, 1.5, 1.8), (26, -12, 1.2, 1.3), (-26, -14, 1.3, 1.5), (-25, 8, 1.0, 1.2), (20, 22, 1.3, 1.4), (5, 24, 1.0, 1.1)))]
    _beats(ep, {})
    out = _take(ep, scenes={0: s0, 2: plan, 3: hg, 4: tl}, alias={5: 2, 6: 0}, adds={1: rings},
                beat_adds={2: (who, [1.05, 500, 900]), 5: (verdict, [1.12, 500, 960])},
                line_adds={(0, 1): (flew, None), (2, 1): (sunk, None), (3, 1): (finger, None), (4, 1): (gen, None), (5, 1): (mang, None)})
    log_x = [box(t, s * 16, .95, .8 * .9, 3.2, .9) for s in (-1, 1) for t in [(-20) + i * 2.4 for i in range(17)]]
    walls = [_ov(s0, [_rim(b, AMB, 3) for b in log_x], 4.4, fx="draw", dur=.8),
             _ov(s0, [_rim(box(0, s * 16, 1.9, 40, .9, .9), GOLD, 4) for s in (-1, 1)] + [_rim(box(s * 20, 0, 1.9, .9, 32, .9), GOLD, 4) for s in (-1, 1)], 5.4, fx="draw", dur=.8),
             _ov(s0, [{"t": "line", "p": [[-20.5, 0, 16.5], [-20.5, 6.65, 16.5]], "c": BN, "w": 3}, _lab(-20.5, 3.3, 16.5, "7.5 m", BN, 0)], 8.0, fx="draw", dur=.6),
             _ov(s0, [box(-31, 18, 0, 5, 5, 5, "#8e7152", "rgba(255,236,206,.4)"), {"t": "pyr", "x": -31, "z": 18, "y": 5, "b": 5.4, "h": 2.4, "c": "#6b4a2e", "edge": "rgba(255,236,206,.4)"}], 10.2, fx="rise"),
             _ov(s0, [_lab(-31, 0, 18, "a house", BN, 40)], 10.6)]
    walls += [{"k": "poly", "p": [[90, 470], [250, 470], [250, 380], [170, 330], [90, 380]], "fill": "none", "c": "#c9a070", "w": 3, "in": 6.2, "fx": "draw", "dur": .8}] + \
             [line([[80, 400 + 16 * j], [260, 400 + 16 * j]], round(6.4 + .05 * j, 2), "#c9a070", 5, draw=False) for j in range(5)] + [label(170, 520, "a log cabin", 6.8, "#c9a070", 28)]
    return _inject(out, _go(out, 1, 1), walls)


# ---------------------------------------------------------------- 06.06 The Plain of Jars
def plain_of_jars():
    import random
    r = random.Random(4)
    jars = [{"t": "slab", "x0": -16, "x1": 16, "z0": -12, "z1": 12, "y": 0, "c": "#8a9a5b"}]
    for k in range(17):
        x, z = r.uniform(-13, 13), r.uniform(-9, 9)
        rr, hh = r.uniform(.6, 1.1), r.uniform(1.4, 3.0)
        jars += [{"t": "cyl", "x": x, "z": z, "y": 0, "r": rr, "h": hh, "c": "#c9b894", "n": 16, "edge": "rgba(0,0,0,.18)"},
                 {"t": "cyl", "x": x, "z": z, "y": hh - .02, "r": rr * .72, "h": .04, "c": "#2a2219", "n": 16, "edge": "rgba(0,0,0,0)"}]
    jars += [{"t": "person", "x": 4, "y": 0, "z": 10.5, "h": 1.7},
             L_(0, 3.4, "hollowed stone jars · the tallest about 3 m", GOLD, z=0, dy=-26), L_(0, 0, "one of more than 120 jar sites · schematic", "#cfe6ff", z=12, dy=40)]
    s0 = iso(jars, cam=[1, 500, 900], s=19, x=500, y=1000, az=-24, spin=1.2, el=.5, table=None)
    v = View(100.5, 107.5, 16.0, 22.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("the Plain of Jars · Phonsavan", 103.2, 19.45, {"c": GOLD}), ("Vientiane", 102.6, 17.97, {}), ("Hanoi", 105.85, 21.03, {})],
                 extra=[{"k": "label", "x": v.p(102.2, 20.6)[0], "y": v.p(102.2, 20.6)[1], "t": "Laos", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s2 = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "vase", "x": 500, "y": 1160, "h": 560, "w": 300, "tone": "#b8a680", "profile": [[0, .62], [.04, .66], [.12, .7], [.4, .72], [.7, .7], [.9, .66], [1, .6]], "in": .2}] +
          [{"k": "line", "p": [[430 + (k % 4) * 42, 1080 - (k // 4) * 44], [470 + (k % 4) * 42, 1060 - (k // 4) * 44]], "c": "#efe4cf", "w": 3, "op": .85, "in": .8 + k * .04} for k in range(12)] +
          [{"k": "cap", "x": 500, "y": 500, "t": "Jar 1, Site 75 · excavated 2024", "in": .3},
           {"k": "label", "x": 500, "y": 1250, "t": "the bones of at least 37 people, toddlers to adults · AD 890–1160", "c": AMBER, "in": 1.4}]}
    s3 = stat("2,100+", "jars", "recorded at more than 120 sites on the Xieng Khouang plateau", "Shewan et al. 2021; UNESCO 2019")
    s4 = stat("80 million", "bomblets", "estimated to have failed to explode, of the cluster munitions dropped on Laos in the 1960s and early 1970s: most jar sites are still undug", "Lao National Regulatory Authority for UXO")
    tl, ax = timeline(-1500, 1500, [(-1500, "1500 BCE"), (-500, "500 BCE"), (500, "500 CE"), (1500, "1500")], "Two sets of dates")
    tl["els"] += [{"k": "band", "x0": ax.x(-1240), "x1": ax.x(-660), "y": 700, "h": 16, "c": GOLD, "t": "jars set in place? maximum ages", "in": .3},
                  {"k": "band", "x0": ax.x(800), "x1": ax.x(1250), "y": 608, "h": 16, "c": SCAN, "t": "the dated burials", "in": .7},
                  {"k": "label", "x": ax.x(70), "y": 520, "t": "about two thousand years apart", "c": "#ffb09a", "in": 1.1}]
    s5 = tl
    s6 = like(s0, cam=[1.18, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE PLAIN OF JARS · LAOS][sfx:boom][act:wonder, setting the scene]More than two ^thousand stone jars, some taller than a person, scattered across a ^plateau in Laos.",
                      "[d:tension][cam:1.12|0|0][act:genuinely curious][tune:fall]What were they ^for? [act:a storyteller, fond]The local legend says ^rice wine. [act:the delightful detail, smiling]For a ^giant king."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:orienting, calm]The Xieng ^Khouang plateau. [act:a telling clue, interested]At least one jar's sandstone came from a quarry ^eight kilometres away, where ^half-finished jars still lie in the rock."]),
        B("collision", 2, ["[d:build][k:THE DEAD][act:respectful, naming the finds][tune:fall]In the {1930s|nineteen thirties}, Madeleine Colani dug around them: burnt human ^bone, ^teeth, glass ^beads.",
                           "[d:build][sfx:shimmer][act:with care, gently]In {2024|twenty twenty-four}, one jar held the bones of at least ^thirty-seven people, from ^toddlers to adults."]),
        B("cost", 5, ["[d:build][k:THE PUZZLE][act:the puzzle opens, leaning in][tune:fall]But look at the ^dates. [act:precise, the first date][tune:level]The burials: about AD {900|nine hundred} to {1200|twelve hundred}. [act:the contrast, slower][tune:fall]The ^sediment under some jars: up to about twelve hundred ^BCE.",
                      "[d:build][sfx:hit][act:letting it land, firm][tune:fall]Two ^thousand years apart. [act:quieter, one more puzzle][tune:fall]And most jars are ^empty."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:a thoughtful idea, gentle]Maybe ^both are true: monuments raised for one purpose, then reused for the dead, the way later Europeans reused ^Stone Age tombs.",
                          "[d:build][act:asking it plainly][tune:fall]Why so ^little digging? [gap:0.4][act:blunt, sober][tune:highfall]^Bombs. [act:sober, matter of fact]The plateau is ^still full of them, from the {1960s|nineteen sixties} and {70s|seventies}."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Jars for the ^dead? [act:the verdict, with a caveat][tune:fall]^*Strong evidence*, in their ^later life. [act:open-handed, curious][tune:fall]What they were ^first made for? [act:honest, simple][tune:fall]Still ^open.",
                     "[d:tension][p:0.93][act:hopeful, quiet conviction]Clear the ^bombs, and the plateau will ^talk."]),
    ]
    return EP("plain-of-jars", "06.06", "The Plain of Jars: Stone Vessels of the Dead?", "plain-of-jars", "strong", "Were the giant stone jars of Laos made to hold the dead?", "Rice wine, for a giant *king*.", beats, shots,
              "Colani 1935 · Shewan et al. 2021, PLOS ONE · Skopal et al. 2024, 2026 · UNESCO 2019 · Plain of Jars Archaeological Project",
              "Two thousand stone jars on a bombed plateau in Laos: the bones inside, the dates two thousand years apart, and why most sites have never been dug.",
              ["#PlainOfJars", "#Laos", "#Archaeology", "#Megaliths", "#Mystery"])


def plain_of_jars_m():
    """The Plain of Jars as one continuous take: jars taller than a person, a giant king's legend, a quarry of half-made jars, the finds
    around and inside a jar (the dead drawn as people, never as bones), two sets of dates two thousand years apart, reuse, and the bombs."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, tooth, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(plain_of_jars())
    S = ep["shots"]
    SAND = "#c9b894"
    import random
    jar2d = lambda x, y, h, at, tone="#b8a680", **kw: dict({"k": "vase", "x": x, "y": y, "h": h, "w": h * .55, "tone": tone, "in": at,
                                                           "profile": [[0, .62], [.04, .66], [.12, .7], [.4, .72], [.7, .7], [.9, .66], [1, .6]]}, **kw)
    # 0 · the plain: two thousand jars, some taller than a person; the legend of a giant king's rice wine
    s0 = _spin(_bare(S[0]), .3); s0["cam"] = [1, 500, 900]
    iso0 = next(e for e in s0["els"] if e.get("k") == "iso")
    jars = [it for it in iso0["items"] if it.get("t") == "cyl" and it["h"] > .1]
    rim = lambda it, c=GOLD: {"t": "line", "p": [[it["x"] + it["r"] * math.cos(a), it["h"], it["z"] + it["r"] * math.sin(a)] for a in [k * math.pi / 8 for k in range(17)]], "c": c, "w": 3}
    s0["els"] += [_ov(s0, [rim(it) for it in jars[k::4]], round(3.8 + .4 * k, 2), fx="draw", dur=.6) for k in range(4)] + \
        [_ov(s0, [{"t": "line", "p": [[-8.51 - 1.0, 0, -7.09], [-8.51 - 1.0, 2.88, -7.09]], "c": BN, "w": 3}, _lab(-8.51 - 1.0, 2.88, -7.09, "3 m", BN, -14)], 8.6, fx="draw", dur=.6),
         _ov(s0, [{"t": "glow", "x": 4, "y": 1.0, "z": 10.5, "r": 60, "kind": "lamp"}, _lab(4, 0, 10.5, "1.7 m", BN, 40)], 9.4)]
    king = [{"k": "lib", "k2": "person", "x": 820, "y": 1240, "h": 640, "color": "#c9c1ee", "op": .28, "keepop": True, "in": 4.6, "fx": "rise"},
            {"k": "poly", "p": [[770, 640], [770, 590], [795, 615], [820, 580], [845, 615], [870, 590], [870, 640]], "fill": "#e8c35a", "c": "none", "w": 0, "in": 5.2, "fx": "pop"},
            label(820, 540, "a giant king?", 5.4, LILAC, 32)] + question(240, 520, .6, 90) + \
           [{"k": "poly", "p": [[150, 700], [190, 640], [230, 700], [215, 720], [165, 720]], "fill": "#e8d6b8", "c": "none", "w": 0, "in": 3.2, "fx": "pop", "curve": True},
            label(190, 770, "rice wine?", 3.4, AMB, 30)]
    # 1 · the map: the Xieng Khouang plateau; a quarry 8 km away with half-made jars
    qy = 1060
    quarry = [bx(110, qy, 780, 340, "#120d0a", r=16, at=3.4, op=.86),
              jar2d(740, qy + 280, 200, 4.4), label(740, qy + 320, "a jar", 4.8, BN, 28),
              {"k": "poly", "p": [[150, qy + 300], [150, qy + 120], [230, qy + 70], [380, qy + 60], [470, qy + 110], [500, qy + 300]], "fill": "#8a7a5c", "c": "#c9b894", "w": 2, "in": 6.4},
              label(325, qy + 330, "the quarry", 6.8, BN, 28),
              arrow([[520, qy + 200], [620, qy + 190], [690, qy + 200]], 7.6, GOLD, 3, dur=.7), label(605, qy + 160, "8 km", 7.8, GOLD, 30)] + \
             [{"k": "poly", "p": [[x - 40, qy + 280], [x - 46, qy + 200], [x - 30, qy + 170], [x + 30, qy + 170], [x + 46, qy + 200], [x + 40, qy + 280]], "fill": "rgba(18,13,10,.25)",
               "c": "#f2dcb4", "w": 2.5, "style": "inferred", "in": round(11.6 + .4 * j, 2), "fx": "draw", "dur": .6} for j, x in enumerate((230, 380))] + \
             [line([[420, qy + 120], [450, qy + 90]], 15.4, "#cbd2d8", 4, draw=False), dot(415, qy + 125, 9, "#8a5d33", 15.4)]
    # 2 · the jar: Colani's finds around it; in 2024, at least 37 people inside one jar, toddlers to adults
    big = jar2d(500, 1160, 560, .2, w=300)
    big["w"] = 300
    finds = [{"k": "line", "p": [[300 + 70 * k, 1180 + 6 * (k % 2)], [336 + 70 * k, 1172 + 6 * (k % 2)]], "c": "#4a3a2c", "w": 7, "in": round(6.0 + .1 * k, 2)} for k in range(3)] + \
            [tooth(x, 1185, 26, round(7.0 + .12 * k, 2)) for k, x in enumerate((560, 600))] + \
            [dot(x, 1192, 7, "#7fc8e8", round(7.7 + .08 * k, 2)) for k, x in enumerate((660, 682, 704, 726))]
    jar = {"base": "dark", "floor": 1160, "cam": [1, 500, 880], "els": [line([[60, 1160], [940, 1160]], .1, "#8c7152", 3, draw=False), big,
           person(170, 1160, 150, 1.4), line([[195, 1060], [235, 1130]], 1.6, "#8a5d33", 6, draw=False), label(170, 1220, "1930s", 1.8, BN, 28),
           bx(260, 1160, 500, 60, "rgba(18,13,10,.4)", BN, 2, 4, 3.4, style="inferred")] + finds +
           [label(330, 1270, "bone", 6.3, "#cbbca8", 26), label(580, 1270, "teeth", 7.1, "#cbbca8", 26), label(695, 1270, "beads", 7.8, "#9fd0ff", 26), glow(500, 1190, 260, 8.6, .35)]}
    folk = [bx(330, 700, 340, 430, "#15100c", "#cbbca8", 2, 40, 2.4, op=.92), label(500, 660, "2024", 1.0, BN, 30)] + \
           [{"k": "lib", "k2": "person", "x": 352 + 33 * (k % 10), "y": 800 + 90 * (k // 10), "h": [24, 30, 36, 42, 46][(k * 3) % 5], "color": "#e8dcc6", "op": .9, "keepop": True,
             "in": round(5.0 + .05 * k, 2)} for k in range(37)] + \
           [label(740, 900, "at least", 6.4, BN, 28, a="start"), label(740, 950, "37 people", 6.6, BN, 34, a="start"), glow(500, 920, 240, 8.0, .3)]
    # 3 · two sets of dates: burials c. 900-1200 CE (from the bones); earth under jars up to c. 1200 BCE (last daylight)
    X = lambda y: 150 + 700 * (y + 1500) / 3000
    tl = {"base": "dark", "cam": [1, 500, 880], "els": [line([[X(-1500), 1000], [X(1500), 1000]], .3, "#8c7152", 3, dur=1.0)] +
          [label(X(v_), 1050, t_, .5, "#9a938a", 26) for v_, t_ in ((-1500, "1500 BCE"), (0, "1 CE"), (1500, "1500 CE"))] +
          [bx(X(900), 975, X(1200) - X(900), 22, BLUE, r=11, at=3.0, fx="fill"), label((X(900) + X(1200)) / 2, 950, "the burials", 3.6, BLUE, 30),
           bx(X(1080) - 20, 760, 40, 110, "#efe6d2", r=6, at=12.4), dot(X(1080), 745, 9, "#ffcf8a", 12.6), glow(X(1080), 740, 60, 12.6, .9, "lamp"),
           arrow([[X(1080) + 40, 760], [X(1080) + 40, 860]], 14.0, AMB, 3, dur=.6, curve=False),
           jar2d(260, 860, 110, 15.4), bx(195, 860, 130, 34, "#8a6a48", r=4, at=15.6), dot(220, 878, 5, GOLD, 15.8), dot(255, 884, 5, GOLD, 15.9), dot(290, 876, 5, GOLD, 16.0),
           dot(150, 700, 26, "#ffe2a8", 19.0), glow(150, 700, 90, 19.0, .8, "sun"), line([[170, 722], [215, 870]], 19.4, "#ffe2a8", 2, "inferred", .6),
           line([[160, 726], [250, 872]], 19.5, "#ffe2a8", 2, "inferred", .6),
           bx(X(-1240), 975, X(-660) - X(-1240), 22, GOLD, r=11, at=21.8, fx="fill"), label((X(-1240) + X(-660)) / 2, 950, "under the jars", 22.4, GOLD, 30)]}
    gap = [arrow([[X(-660) + 10, 920], [X(900) - 10, 920]], .6, RD, 3, dur=.8, curve=False), arrow([[X(900) - 10, 920], [X(-660) + 10, 920]], .6, RD, 3, dur=.8, curve=False),
           label((X(-660) + X(900)) / 2, 900, "2,000 years", 1.2, RD, 32)] + \
          [x for k in range(10) for x in ([jar2d(185 + 70 * k, 1290, 80, round(2.6 + .08 * k, 2))] +
                                          ([dot(185 + 70 * k, 1222, 6, "#e8dcc6", 3.2)] if k in (2, 7) else []))] + question(500, 1420, 7.0, 70)
    # 4 · reuse: raised for one purpose, used later for the dead, as Stone Age tombs were reused; then the bombs
    reuse = {"base": "dark", "cam": [1, 500, 880], "els": [line([[100, 800], [900, 800]], .2, "#8c7152", 3, draw=False),
             jar2d(260, 800, 260, .4)] + question(260, 470, 1.6, 70) +
             [arrow([[400, 640], [600, 640]], 3.6, AMB, 4, dur=.7, curve=False),
              jar2d(740, 800, 260, 4.0)] + [person(700 + 22 * k, 780, 44 - 4 * k, round(4.8 + .15 * k, 2), c="#e8dcc6") for k in range(4)] +
             [label(260, 860, "first purpose?", 2.6, LILAC, 28), label(740, 860, "later, the dead", 5.2, BN, 28),
              line([[150, 1200], [850, 1200]], 6.4, "#8c7152", 3, draw=False),
              bx(360, 1050, 50, 150, "#8a8378", "#2a2219", 2, 4, 6.8), bx(590, 1050, 50, 150, "#8a8378", "#2a2219", 2, 4, 6.9),
              {"k": "poly", "p": [[330, 1050], [670, 1030], [680, 1000], [320, 1010]], "fill": "#9a938a", "c": "#2a2219", "w": 2, "in": 7.2, "fx": "rise"},
              label(500, 1250, "a Stone Age tomb, reused", 7.8, BN, 30), person(500, 1200, 90, 8.8, c="#e8dcc6")]}
    rb = random.Random(9)
    bombs = [{"k": "poly", "p": [[-20, 1330], [1020, 1330], [1020, 1600], [-20, 1600]], "fill": "#4a5a3a", "c": "none", "w": 0, "in": .2},
             line([[-20, 1330], [1020, 1330]], .2, "#8fb070", 2, draw=False)] + [jar2d(x, 1330, 70, .4) for x in (180, 430, 760)] + \
            [bx(520, 1340, 120, 70, "none", BN, 2.5, 4, 1.4, style="inferred"), strike(520, 1410, 640, 1340, 1.8, RD, 5)] + \
            [line([[x, 760], [x - 40, 1000]], round(5.8 + .15 * k, 2), "#ff8a7a", 2, "inferred", .5) for k, x in enumerate((300, 480, 650, 820))] + \
            [dot(x, y, 4.5, "#ff8a7a", round(9.0 + .015 * k, 3)) for k, (x, y) in enumerate([(round(rb.uniform(40, 960), 1), round(rb.uniform(1350, 1580), 1)) for _ in range(150)])] + \
            [label(500, 1290, "80 million unexploded bomblets", 11.4, "#ff8a7a", 30), glow(500, 1460, 380, 13.0, .3, "red")]
    # 6 → back to the plain: jars for the dead; first purpose still open; clear the bombs
    verdict = [_ov(s0, [{"t": "glow", "x": it["x"], "y": it["h"], "z": it["z"], "r": 50, "kind": "lamp"} for it in jars[::3]], 1.0),
               _ov(s0, [{"t": "q", "x": 0, "y": 5, "z": 0, "c": LILAC, "size": 70}], 5.4, fx="pop")]
    clear = [_ov(s0, [{"t": "line", "p": [[-15, .05, 11], [-9, .05, 6], [-3, .05, 8], [2, .05, 3], [8, .05, 5], [14, .05, -2]], "c": GOLD, "w": 4, "style": "inferred", "ground": True}], .6, fx="draw", dur=1.4)] + \
            [_ov(s0, [{"t": "person", "x": -12 + 6 * k, "y": 0, "z": 8.5 - 2 * k, "h": 1.7, "color": "#e8d6b8"}], round(1.6 + .3 * k, 2), fx="rise") for k in range(3)]
    shots = S[:3] + [tl, reuse, S[4], S[6]]
    _beats(ep, {3: 3, 4: 4})
    ep["shots"] = shots
    return _take(ep, scenes={0: s0, 2: jar, 3: tl, 4: reuse}, alias={5: 4, 6: 0}, adds={1: quarry},
                 beat_adds={5: (verdict, [1.12, 500, 960])},
                 line_adds={(0, 1): (king, None), (2, 1): (folk, None), (3, 1): (gap, None), (4, 1): (bombs, [1.05, 500, 1180]), (5, 1): (clear, None)})


# ---------------------------------------------------------------- 06.07 The Diquís spheres
def diquis():
    sp = [{"t": "slab", "x0": -11, "x1": 11, "z0": -6, "z1": 7, "y": 0, "c": "#6f8a4a"}] + \
         sphere(-7, -2, 1.28, "#8a8378") + sphere(-1.5, 0, 1.0, "#948c80") + sphere(3.6, 2, .8, "#7f786e") + sphere(8, 3.8, .55, "#8a8378") + \
         [{"t": "person", "x": -3.6, "y": 0, "z": 3.4, "h": 1.7},
          L_(-7, 2.8, "up to 2.57 m across", GOLD, z=-2, dy=-24), L_(0, 0, "in a line, at Finca 6 · schematic", "#cfe6ff", z=6, dy=40)]
    s0 = iso(sp, cam=[1, 500, 900], s=31, x=530, y=1000, az=-20, spin=1.0, el=.45, table=None)
    v = View(-86.0, -82.5, 8.0, 11.2, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("the Diquís Delta · Finca 6", -83.4667, 8.9333, {"c": GOLD}), ("Isla del Caño", -83.88, 8.71, {"a": "end", "lx": -18}), ("San José", -84.09, 9.93, {})],
                 extra=[{"k": "label", "x": v.p(-84.6, 10.5)[0], "y": v.p(-84.6, 10.5)[1], "t": "Costa Rica", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    dots = [(330, 1000), (470, 960), (610, 920)]
    rays = [(-18, "a solstice sunrise?"), (-4, "an equinox?"), (12, "a moonrise?"), (26, "a mountain?")]
    s2 = {"base": "dark", "cam": [1, 500, 880], "els": [{"k": "circle", "x": x, "y": y, "r": 24, "fill": "#8a8378", "c": "#e8e2d6", "w": 1.4, "in": .2 + i * .15} for i, (x, y) in enumerate(dots)] +
          [{"k": "line", "p": [[610, 920], [610 + 330 * math.cos(math.radians(-16 + a)), 920 + 330 * math.sin(math.radians(-16 + a)) - 120]], "c": [GOLD, AMBER, SCAN, "#c9ad85"][i], "w": 2, "style": "claimed", "in": .8 + i * .25}
           for i, (a, t) in enumerate(rays)] +
          [{"k": "label", "x": 610 + 350 * math.cos(math.radians(-16 + a)), "y": 920 + 350 * math.sin(math.radians(-16 + a)) - 140, "t": t, "st": "small", "a": "end", "c": [GOLD, AMBER, SCAN, "#c9ad85"][i], "in": 1.0 + i * .25}
           for i, (a, t) in enumerate(rays)] +
          [{"k": "cap", "x": 500, "y": 480, "t": "two or three points always make a line", "in": .3},
           {"k": "label", "x": 500, "y": 1180, "t": "the test: many lines, checked against chance", "c": "#ffb09a", "in": 2.0}]}
    s3 = stat("300+", "spheres", "known from the Diquís Delta; most were moved by plantation workers and collectors before anyone mapped them", "Lothrop 1963; Hoopes 2010; UNESCO 2014")
    tl, ax = timeline(400, 2100, [(500, "500 CE"), (1000, "1000"), (1500, "1500"), (2000, "2000")], "The spheres through time")
    tl["els"] += [{"k": "band", "x0": ax.x(600), "x1": ax.x(1500), "y": 700, "h": 16, "c": GOLD, "t": "the spheres are made", "in": .3}] + \
                 event(ax, 1935, "banana plantations find them", row=1, c=BONE, i=.7, sub="the 1930s")
    s4 = tl
    s5 = like(s0, cam=[1.25, 500, 980], add=[{"k": "label", "x": 500, "y": 560, "t": "surveyed for alignment: not yet", "c": "#ffb09a", "in": .4}])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:COSTA RICA][sfx:boom][act:storytelling, a twinkle]In the {1930s|nineteen thirties}, bulldozers clearing jungle for ^bananas hit something ^round. [act:the reveal, simply][tune:fall]^Stone balls. [act:widening, wonder][tune:fall]^Hundreds of them.",
                      "[d:tension][cam:1.12|0|0][act:marvelling, slow][tune:level]Some ^taller than a person. [act:hushed wonder][tune:fall]Almost ^perfectly round."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:orienting, calm]The Diquís Delta, near Costa Rica's ^Pacific coast. [act:giving the range, clear]More than three hundred spheres, from a few ^centimetres to two and a half ^metres across.",
                       "[d:build][act:matter of fact, confident]Made over about nine ^centuries, from about AD {600|six hundred}, by local ^chiefdoms. [act:admiring the craft]Hard rock, ^pecked and ground with ^harder stones."]),
        B("collision", 2, ["[d:build][k:THE CASE][act:intrigued, setting up the claim]Some stand in ^lines. [act:reporting the claim, fairly]Lines that point at ^solstice sunrises, say some writers. [sfx:shimmer][act:the bolder claim, even]Or ^sea routes, encoded by a lost ^ocean-going culture, says one book from {1998|nineteen ninety-eight}."]),
        B("cost", 3, ["[d:build][k:THE PROBLEM][act:the snag, plainly]But almost every sphere was ^moved before anyone ^mapped it. [act:where they went, a little rueful][tune:fall]Rolled to ^plantations, ^gardens, ^government buildings.",
                      "[d:aside][act:a wry aside, quicker]Treasure hunters ^dynamited a few, hoping for ^gold inside. [act:deadpan, understated][tune:fall]There was ^none."]),
        B("reversal", 2, ["[d:reveal][k:THE TWIST][sfx:hit][act:the insight, leaning in]And with two or three points, ^any line points at ^something. [act:counting them off, lightly][tune:level]A ^sunrise. [act:same rhythm][tune:level]A ^moonrise. [act:the punchline, dry][tune:fall]A ^mountain.",
                          "[d:build][act:precise, careful]No ^published survey@noun has tested the lines still in place against ^chance. [go:5|0][act:fair, even-handed][tune:fall]^Untested isn't the same as ^false."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Lines aimed at the ^sky? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the grounded option][tune:rise]Symbols of ^power in chiefs' villages? [act:plain and assured][tune:fall]That's what the ^digs show.",
                     "[d:tension][p:0.93][act:warm, an open invitation]The test is ^simple, and the lines at Finca Six are ^waiting."]),
    ]
    return EP("diquis-spheres", "06.07", "The Stone Spheres of Costa Rica: Round on Purpose", "diquis-spheres", "unsupported", "Were the Diquís spheres lined up to point at the sky or the sea?", "Bulldozers hit something *round*.", beats, shots,
              "Lothrop 1963 · Stone 1943 · Hoopes 2010 · Corrales & Badilla 2005 · UNESCO 2014 · Zapp & Erikson 1998",
              "Hundreds of near-perfect stone balls found by banana-plantation bulldozers in Costa Rica: who made them, the claim that their lines point at the sky, and the survey that would test it.",
              ["#StoneSpheres", "#CostaRica", "#Archaeology", "#Mystery", "#History"])


def diquis_m():
    """The Diquís spheres as one continuous take: bulldozers in a banana plantation hit stone balls; a delta, a tennis ball and a
    door for scale; nine centuries of pecking; lines toward a solstice sunrise or sea routes; spheres rolled away from their lines;
    the catch that any two points aim at something; and the survey still waiting at Finca 6."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(diquis())
    S = ep["shots"]
    GAB = "#8a8378"
    # 0 · the find: banana plantation, a bulldozer, stone balls; taller than a person, almost perfectly round
    s0 = _spin(_bare(S[0]), .25); s0["cam"] = [1, 520, 900]
    sph = [(-7, -2, 1.28), (-1.5, 0, 1.0), (3.6, 2, .8), (8, 3.8, .55)]
    belt = lambda x, z, r, c=GOLD, w=3: {"t": "line", "p": [[x + r * math.cos(a), r, z + r * math.sin(a)] for a in [k * math.pi / 12 for k in range(25)]], "c": c, "w": w}
    merid = lambda x, z, r, c=GOLD: {"t": "line", "p": [[x + r * math.cos(a), r + r * math.sin(a), z] for a in [k * math.pi / 12 for k in range(25)]], "c": c, "w": 3}
    dozer = [bx(110, 700, 130, 56, "#c8a03a", "#2a2219", 2, 6, 4.6), bx(150, 650, 60, 50, "#c8a03a", "#2a2219", 2, 4, 4.6), bx(110, 752, 140, 22, "#3a332b", r=10, at=4.6),
             {"k": "poly", "p": [[240, 690], [262, 690], [270, 770], [244, 770]], "fill": "#8a8378", "c": "#2a2219", "w": 2, "in": 4.7}]
    s0["els"] += [{"k": "palm", "x": x, "y": 780, "h": h, "in": round(2.4 + .15 * k, 2), "fx": "rise"} for k, (x, h) in enumerate(((330, 120), (430, 150), (560, 130), (690, 160), (820, 125), (920, 140)))] + \
        dozer + [_ov(s0, [{"t": "glow", "x": -7, "y": 1.3, "z": -2, "r": 120, "kind": "lamp"}], 6.2),
                 _ov(s0, [belt(x, z, r) for x, z, r in sph], 7.3, fx="draw", dur=.8)] + \
        [dot(x, y, r, GAB, round(8.2 + .012 * k, 3), op=.85) for k, (x, y, r) in enumerate(
            [(round(80 + (k * 137) % 840), round(1260 + (k * 53) % 150), 3 + (k * 7) % 9) for k in range(70)])]
    tall = [_ov(s0, [{"t": "line", "p": [[-8.6, 0, -.6], [-8.6, 2.56, -.6]], "c": BN, "w": 3}, _lab(-8.6, 2.56, -.6, "2.5 m", BN, -14)], .6, fx="draw", dur=.6),
            _ov(s0, [{"t": "glow", "x": -3.6, "y": 1.0, "z": 3.4, "r": 60, "kind": "lamp"}, _lab(-3.6, 0, 3.4, "1.7 m", BN, 40)], 1.0),
            _ov(s0, [merid(-7, -2, 1.32)], 2.0, fx="draw", dur=1.0)] + question(520, 560, 3.8, 90)
    # 1 · the delta, the size range (a tennis ball to taller than a door); nine centuries of chiefdoms and pecking
    v = View(-86.0, -82.5, 8.0, 11.2, (40, 330, 920, 900))
    dx, dy = v.p(-83.4667, 8.9333)
    river = [line([[dx - 60, dy - 120], [dx - 30, dy - 60], [dx - 10, dy - 20]], 4.6, "#6fb6d6", 4, dur=.6, curve=True)] + \
            [line([[dx - 10, dy - 20], [dx - 10 + ex, dy + 30]], round(5.2 + .2 * k, 2), "#6fb6d6", 3, dur=.4, curve=False) for k, ex in enumerate((-40, -10, 20, 50))]
    IY = 1080
    sizes = [bx(100, IY, 800, 320, "#120d0a", r=16, at=10.6, op=.88), line([[130, IY + 280], [870, IY + 280]], 10.8, "#8c7152", 3, draw=False),
             dot(170, IY + 276, 4, "#d8e86a", 13.0), label(170, IY + 240, "tennis ball", 16.4, "#d8e86a", 26)] + \
            [dot(x, IY + 280 - r, r, GAB, round(13.4 + .3 * k, 2)) for k, (x, r) in enumerate(((240, 10), (310, 24), (410, 46)))] + \
            [dot(620, IY + 180, 100, GAB, 14.6), ring(620, IY + 180, 100, 14.6, "#cbbca8", 2), label(620, IY + 190, "2.5 m", 15.2, INK, 34, halo=False),
             bx(770, IY + 120, 64, 160, "#5a3a22", "#c9a070", 2, 3, 17.0), dot(822, IY + 205, 5, "#e8c35a", 17.1), label(802, IY + 100, "a door", 17.2, BN, 26)]
    chief = [bx(100, 290, 800, 270, "#120d0a", r=16, at=.3, op=.88),
             line([[150, 380], [470, 380]], .8, GOLD, 6, dur=1.0), label(150, 345, "AD 600", 1.2, GOLD, 26, a="start"), label(470, 345, "1500", 2.6, GOLD, 26, a="end"),
             label(310, 420, "nine centuries", 3.0, BN, 28)] + \
            [{"k": "house", "x": 150 + 70 * k, "y": 520, "w": 54, "h": 34, "in": round(5.4 + .15 * k, 2)} for k in range(3)] + \
            [person(400, 520, 64, 6.0, c="#e8c35a"), label(300, 548, "chiefdoms", 6.4, AMB, 26)] + \
            [dot(680, 430, 70, GAB, 8.8), oval(785, 340, 20, 18, "#5a534c", "#cbbca8", 2, 1, 9.8)] + \
            [line([[740 + 16 * math.cos(a), 372 + 16 * math.sin(a)], [740 + 32 * math.cos(a), 372 + 32 * math.sin(a)]], round(10.2 + .05 * k, 2), AMB, 3, draw=False)
             for k, a in enumerate((2.4, 3.0, 3.6))] + \
            [{"k": "arrow", "p": [[680 + 95 * math.cos(a), 430 + 95 * math.sin(a)] for a in [k * .25 - .6 for k in range(10)]], "c": BN, "w": 3, "curve": True, "fx": "draw", "dur": .8, "in": 12.6}]
    # 2 · the claim: a line of spheres aimed at a solstice sunrise, or sea routes; and the care behind every sphere
    HZ = 760
    row = [(330, 1200, 56), (470, 1080, 42), (580, 990, 32)]
    lines_ = {"base": "sky", "tod": "dawn", "ground": HZ, "sun": False, "cam": [1, 500, 880], "els":
              [x for k, (x0, y0, r) in enumerate(row) for x in (oval(x0, y0 + r * .9, r * 1.1, r * .25, "#000", "none", 0, .3, .3 + .2 * k), dot(x0, y0, r, GAB, .3 + .2 * k), ring(x0, y0, r, .3 + .2 * k, "#cbbca8", 2, dur=.5))] +
              [line([[300, 1240], [700, HZ]], 1.8, BN, 3, "inferred", 1.0),
               oval(700, HZ, 40, 40, "#ffd9a0", "none", 0, 1, 3.6), glow(700, HZ - 10, 150, 3.6, .8, "sun"), label(700, HZ - 70, "solstice sunrise?", 4.4, GOLD, 30),
               {"k": "line", "p": [[160 + 680 * k / 20, HZ - 360 * math.sin(math.pi * k / 20)] for k in range(21)], "c": GOLD, "w": 3, "style": "inferred", "curve": True, "in": 6.6, "fx": "draw", "dur": 1.0},
               {"k": "line", "p": [[340 + 320 * k / 20, HZ - 150 * math.sin(math.pi * k / 20)] for k in range(21)], "c": BLUE, "w": 3, "style": "inferred", "curve": True, "in": 7.8, "fx": "draw", "dur": .8},
               label(500, HZ - 375, "longest day", 7.2, GOLD, 28), label(500, HZ - 165, "shortest", 8.4, BLUE, 28),
               bx(760, HZ - 4, 260, 30, "#3f86a8", r=4, at=10.4), {"k": "boat", "x": 860, "y": HZ - 6, "w": 70, "in": 10.8},
               {"k": "arrow", "p": [[820, HZ - 30], [700, HZ - 120], [560, HZ - 200]], "c": LILAC, "w": 3, "style": "claimed", "curve": True, "fx": "draw", "dur": .9, "in": 11.4},
               label(560, HZ - 230, "sea routes?", 12.0, LILAC, 30),
               bx(790, 1060, 90, 110, "#6b3a2a", "#c8743c", 3, 6, 13.6, fx="pop"), label(835, 1200, "1998", 13.8, BN, 28),
               ring(330, 1200, 66, 17.6, GOLD, 4), glow(330, 1200, 110, 17.6, .5), person(200, 1260, 120, 18.2)]}
    catch = [{"k": "fan", "x": 470, "y": 1080, "r": 560, "a0": 190, "a1": 350, "n": 15, "c": "#cbd2d8", "in": 3.4},
             dot(250, 500, 30, "#efe8da", 5.8), dot(262, 494, 30, "#141726", 5.8), line([[470, 1080], [250, 500]], 5.9, BN, 3, "inferred", .7),
             {"k": "poly", "p": [[60, HZ], [150, HZ - 120], [240, HZ]], "fill": "#3b3140", "c": "#6a5a72", "w": 2, "in": 6.8}, line([[470, 1080], [150, HZ - 120]], 6.9, BN, 3, "inferred", .7)]
    chance = [line([[x0, 1340], [x1, HZ]], round(1.2 + .1 * k, 2), "#9a938a", 2, "claimed", .6) for k, (x0, x1) in enumerate(((120, 300), (200, 820), (380, 120), (520, 640), (640, 260), (760, 900), (880, 480), (300, 560)))] + \
             [label(500, 1400, "chance?", 3.4, LILAC, 32), bx(760, 1180, 120, 150, "#e8dcc2", "#8a7a66", 2, 6, 6.4)] + \
             [line([[780, 1215 + 25 * j], [860, 1215 + 25 * j]], round(6.6 + .1 * j, 2), "#8a7a66", 2, "inferred", .3) for j in range(4)] + \
             [bx(780, 1300, 30, 22, "none", LILAC, 3, 3, 7.6, style="claimed"), label(820, 1150, "no survey yet", 8.0, LILAC, 26)]
    # 3 · moved before mapping: from their line to plantations, gardens and government buildings; a sentence shuffled; dynamite, no gold
    base = [(260, 640), (380, 610), (500, 580), (620, 550)]
    moved = {"base": "plan", "bg": "#2b2a1f", "north": False, "cam": [1, 500, 880], "els":
             [x for k, (x0, y0) in enumerate(base) for x in (ring(x0, y0, 34, .4 + .15 * k, "#cbbca8", 2, "inferred", .5), dot(x0, y0, 30, GAB, .6 + .15 * k))] +
             [line([[200, 655], [700, 535]], .3, BN, 2, "inferred", .8), label(450, 520, "a line", 1.0, BN, 28),
              arrow([[260, 680], [230, 820], [190, 950]], 5.4, AMB, 3, "inferred", .7), arrow([[380, 650], [480, 800], [520, 950]], 5.8, AMB, 3, "inferred", .7),
              arrow([[620, 590], [720, 500], [800, 420]], 6.2, AMB, 3, "inferred", .7)] +
             [{"k": "palm", "x": 120 + 50 * k, "y": 1060, "h": 80, "in": round(6.0 + .1 * k, 2)} for k in range(4)] + [label(195, 1110, "plantations", 6.4, AMB, 26),
              dot(190, 990, 24, GAB, 6.6)] +
             [dot(470 + 30 * k, 1030 - 12 * (k % 2), 14, ["#d97a9a", "#e8c35a", "#9fcf6a"][k % 3], round(7.2 + .08 * k, 2)) for k in range(4)] + [label(520, 1110, "gardens", 7.6, AMB, 26),
              dot(520, 990, 24, GAB, 7.4)] +
             [bx(760, 380, 140, 14, "#d8c49c", r=2, at=8.4)] + [line([[776 + 22 * k, 394], [776 + 22 * k, 450]], 8.5, "#d8c49c", 5, draw=False) for k, _ in enumerate(range(6))] +
             [{"k": "poly", "p": [[750, 380], [830, 340], [910, 380]], "fill": "#d8c49c", "c": "none", "w": 0, "in": 8.6}, bx(750, 450, 160, 12, "#d8c49c", r=2, at=8.5),
              label(830, 500, "government", 8.8, AMB, 26), dot(800, 470, 20, GAB, 8.9)] +
             [x for k, w_ in enumerate(("the", "line", "points", "east")) for x in (bx(170 + 170 * k, 1200, 150, 54, "#e8dcc2", "#8a7a66", 2, 8, round(11.2 + .15 * k, 2)),
                                                                                  label(245 + 170 * k, 1237, w_, round(11.3 + .15 * k, 2), INK, 28, halo=False))] +
             [x for k, (w_, p) in enumerate((("points", 0), ("east", 1), ("the", 2), ("line", 3))) for x in (bx(170 + 170 * p, 1320, 150, 54, "#e8dcc2", "#8a7a66", 2, 8, round(13.0 + .15 * k, 2), fx="pop"),
                                                                                                          label(245 + 170 * p, 1357, w_, round(13.1 + .15 * k, 2), INK, 28, halo=False))]}
    dyn = [dot(700, 760, 60, GAB, .4), line([[680, 712], [700, 760], [690, 808]], 1.6, "#2a2722", 4, dur=.3), line([[700, 760], [748, 752]], 1.7, "#2a2722", 4, dur=.3),
           glow(700, 760, 160, 1.8, .9, "red"), label(700, 860, "dynamite", 2.0, RD, 28),
           dot(620, 700, 14, "#e8c35a", 4.0), strike(596, 724, 644, 676, 5.0, RD, 5), label(600, 650, "gold?", 4.2, "#e8c35a", 28)]
    # 5 → back to the spheres: aimed at the sky? symbols of power in chiefs' villages; the survey still waiting at Finca 6
    untested = [bx(860, 640, 54, 54, "none", LILAC, 3, 6, 1.2, style="claimed"), label(887, 740, "untested", 1.6, LILAC, 28)]
    verdict = [_ov(s0, [{"t": "line", "p": [[x, 2 * r, z], [x - 3 + 1.5 * k, 2 * r + 9, z - 3]], "c": BLUE, "w": 2.5, "style": "claimed"} for k, (x, z, r) in enumerate(sph[:3])], .6, fx="draw", dur=.8),
               _ov(s0, [{"t": "label", "x": -2, "y": 10.5, "z": -3, "text": "the sky?", "st": "body", "c": BLUE, "dy": -10}], 1.2)] + \
              [_ov(s0, [box(x, z, 0, 2.2, 2.2, 1.6, "#8e7152", "rgba(255,236,206,.4)"), {"t": "pyr", "x": x, "z": z, "y": 1.6, "b": 2.6, "h": 1.2, "c": "#6b4a2e", "edge": "rgba(255,236,206,.4)"}],
                    round(4.0 + .2 * k, 2), fx="rise") for k, (x, z) in enumerate(((-9.5, 5.5), (-5, 6.2), (6.5, -4.5), (10, -2)))] + \
              [_ov(s0, [{"t": "person", "x": 1, "y": 0, "z": 5, "h": 1.7, "color": "#e8c35a"}], 5.0, fx="rise"),
               _ov(s0, [_hi(box(-1.5, 0, -.6, 3.4, 3.4, .6), GOLD, .3, "inferred")], 6.6, fx="draw", dur=.6)]
    survey = [_ov(s0, [{"t": "line", "p": [[-10, .05, -3.2], [10, .05, 4.6]], "c": GOLD, "w": 3, "style": "inferred", "ground": True}] +
                   [{"t": "line", "p": [[-10 + 2 * k, .05, -3.2 + .78 * k], [-10 + 2 * k, .6, -3.2 + .78 * k]], "c": GOLD, "w": 2} for k in range(11)], 1.0, fx="draw", dur=1.2),
              _ov(s0, [{"t": "label", "x": 10, "y": .2, "z": 4.6, "text": "Finca 6", "st": "body", "c": GOLD, "dy": 40}], 1.8), glow(520, 1000, 300, 3.0, .3)]
    shots = S[:4] + [S[3], S[5]]
    ep["shots"] = shots
    out = _take(ep, scenes={0: s0, 2: lines_, 3: moved}, alias={4: 3, 5: 0}, cams={5: [1.15, 520, 960]}, adds={1: river + sizes},
                beat_adds={4: (catch, None), 5: (verdict, [1.15, 520, 960])},
                line_adds={(0, 1): (tall, None), (1, 1): (chief, None), (3, 1): (dyn, None), (4, 1): (chance, None), (5, 1): (survey, None)})
    return _inject(out, _go(out, 4, 1, 1), untested)


# ---------------------------------------------------------------- 06.08 The cart ruts
def cart_ruts():
    cliff = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 40, "prof": [[-12, 0], [40, 0], [40, 4], [14, 4], [12, 0.2], [-12, .2]], "c": "#d9c8a0", "edge": "rgba(0,0,0,.25)", "flipN": False},
             {"t": "flat", "pts": [[-12, -20], [12, -20], [12, 20], [-12, 20]], "y": .6, "c": SEA, "op": .6, "ground": False, "over": 3}]

    def rut(p0, p1, g=1.4, y=4.05, c="#6d5a3e"):
        dx, dz = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dz); nx, nz = -dz / L * g / 2, dx / L * g / 2
        return [{"t": "line", "p": [[p0[0] + s * nx, y, p0[1] + s * nz], [p1[0] + s * nx, y, p1[1] + s * nz]], "c": c, "w": 4, "op": .95} for s in (-1, 1)]
    ruts = rut((38, -14), (15, -4)) + rut((38, 10), (15, 2)) + rut((36, -18), (20, 16)) + rut((30, 18), (22, -18))
    ruts += [{"t": "line", "p": [[14.6 + s * .7, 3.4 - k, -3.4 + k * .6 - s * .0] for k in range(2)], "c": "#6d5a3e", "w": 3, "op": .7} for s in (-1, 1)]
    ruts += [{"t": "line", "p": [[11.6 + s * .7 * 0, .7, -2.6 + s * .7], [2 + s * 0, .7, -1 + s * .7]], "c": "#4a6f86", "w": 3, "op": .75, "style": "inferred"} for s in (-1, 1)]
    scene = cliff + ruts + [{"t": "person", "x": 30, "y": 4, "z": 4, "h": 1.7},
                            L_(32, 4, "paired grooves in bare limestone", GOLD, z=-14, dy=-40), L_(4, .6, "some run into the sea", "#cfe6ff", z=-1, dy=-20), L_(26, 4, "gauge about 1.40 m · schematic", "#f2dcb4", z=18, dy=40)]
    s0 = iso(scene, cam=[1, 500, 900], s=11, x=430, y=990, az=-30, spin=1.2, el=.5, table=None)
    v = View(10.5, 17.0, 34.6, 38.6, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Malta · 'Clapham Junction'", 14.3869, 35.8556, {"c": GOLD}), ("Sicily · more ruts", 14.9, 37.2, {}), ("Tunisia", 10.9, 35.6, {"a": "start"})],
                 extra=[{"k": "label", "x": v.p(15.9, 35.2)[0], "y": v.p(15.9, 35.2)[1], "t": "the Mediterranean", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    gy = 820
    s2 = {"base": "dark", "cam": [1, 500, 880], "els": [
        {"k": "poly", "p": [[60, gy], [300, gy], [320, gy + 150], [360, gy + 160], [380, gy], [620, gy], [640, gy + 150], [680, gy + 160], [700, gy], [940, gy], [940, 1350], [60, 1350]], "fill": "#d9c8a0", "c": "#fff3dc", "w": 1.6, "in": .2},
        {"k": "rect", "x": 322, "y": gy - 270, "w": 36, "h": 420, "fill": "#6b4a2e", "c": "#c9a070", "sw": 1.4, "in": .6},
        {"k": "rect", "x": 642, "y": gy - 270, "w": 36, "h": 420, "fill": "#6b4a2e", "c": "#c9a070", "sw": 1.4, "in": .6},
        {"k": "line", "p": [[340, gy - 60], [660, gy - 60]], "c": "#8c6a48", "w": 10, "in": .8},
        {"k": "rect", "x": 250, "y": gy - 170, "w": 500, "h": 40, "fill": "#8c6a48", "c": "#c9a070", "sw": 1.4, "in": .9},
        {"k": "label", "x": 500, "y": gy - 80, "t": "the axle", "st": "small", "c": "#f2dcb4", "in": 1.0},
        {"k": "dim", "x1": 340, "y1": 1260, "x2": 660, "y2": 1260, "t": "about 1.40 m", "lx": 0},
        {"k": "cap", "x": 500, "y": 460, "t": "wet, soft limestone + two-wheeled carts", "in": .3},
        {"k": "label", "x": 500, "y": 1380, "t": "every pass cuts deeper, until the axle scrapes: then a new line", "c": AMBER, "in": 1.3}]}
    s3 = stat("1.40", "metres", "the typical gauge of the ruts, centre to centre, in a measured sample", "Groucutt 2022; Mottershead et al. 2008")
    tl, ax = timeline(-7000, 2000, [(-7000, "7000 BCE"), (-4000, "4000"), (-1000, "1000 BCE"), (2000, "2000 CE")], "What the ruts can't be older than")
    tl["els"] += event(ax, -6500, "people reach Malta", row=1, c=BONE, i=.3, sub="about 8,500 years ago") + event(ax, -3500, "the first wheels", row=2, c=GOLD, i=.6, sub="far from Malta") + \
                 [{"k": "band", "x0": ax.x(-3600), "x1": ax.x(-2500), "y": 700, "h": 14, "c": "#c9ad85", "op": .8, "t": "the Temple Period", "in": .9}] + event(ax, -700, "Punic tombs cut some ruts", row=0, c=SCAN, i=1.2) + \
                 [{"k": "label", "x": 120, "y": 470, "t": "← Koltypin's claim: 12–14 million years ago, far off this chart", "st": "small", "c": "#ffb09a", "a": "start", "in": 1.5}]
    s4 = tl
    sec = {"base": "section", "tod": "day", "ground": 800, "lx": 130, "layers": [{"d": 0, "c": "#d9c8a0", "t": "limestone"}, {"d": 260, "c": "#b8a57c", "t": ""}],
           "cam": [1, 500, 900], "els": [{"k": "water", "y": 740, "h": 620, "x0": 520, "x1": 1600, "op": .55, "in": .2},
                                         {"k": "line", "p": [[120, 796], [520, 796], [700, 830]], "c": "#6d5a3e", "w": 5, "in": .5},
                                         {"k": "label", "x": 640, "y": 700, "t": "the ruts go down about a metre or two", "c": AMBER, "in": .8},
                                         {"k": "line", "p": [[520, 1300], [940, 1300]], "c": "#9fd0ff", "w": 2, "style": "inferred", "in": 1.1},
                                         {"k": "label", "x": 730, "y": 1270, "t": "Ice Age shorelines: over 100 m deeper", "st": "small", "c": "#9fd0ff", "in": 1.3}]}
    s5 = sec
    s6 = like(s0, cam=[1.18, 480, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:MALTA · THE CART RUTS][sfx:boom][act:intrigued, setting the scene]Pairs of ^grooves cut into bare ^rock. [act:vivid, building]They cross like ^railway lines. [act:stranger still][tune:level]Some run off ^cliffs. [act:the eerie one, slower][tune:fall]Some run into the ^sea.",
                      "[d:tension][cam:1.12|0|0][act:quiet, the hook][tune:fall]And ^nobody can date them."], cut=False),
        B("world", 1, ["[d:calm][k:THE PLACE][act:plain, informative]Malta has more of them than ^anywhere on Earth: about thirty-five kilometres, in ^pieces. [go:3|0][act:a curious detail, interested]And the gauge is ^surprisingly standard: about one metre ^forty."]),
        B("collision", 4, ["[d:build][k:THE CLAIMS][act:reporting the claim, even]A geologist, Alexander Koltypin, dated similar tracks in Turkey to twelve to fourteen ^million years ago. [d:aside][act:an aside, eyebrows raised][tune:level]Before ^humans. [act:going further, dry][tune:fall]Before our ^genus.",
                           "[d:build][go:5|0][act:the second claim, fair]And Malta's ruts that slide into the sea look, to ^some, like a lost ^Ice Age coastline."]),
        B("cost", 2, ["[d:build][k:THE MECHANISM][act:explaining, clear and patient]Geomorphologists worked out how: two-wheeled ^carts on thin soil, in the ^wet season. [act:simple, the key fact][tune:fall]The limestone ^softens.",
                      "[d:build][sfx:shimmer][act:showing the process, rhythmic]Every pass cuts ^deeper, until the axle ^scrapes. [act:the neat solution, pleased]Then the drivers move ^over and start a ^new line."]),
        B("reversal", 4, ["[d:reveal][k:THE TWIST][act:leaning in, the turn]And the timeline ^boxes it in. [act:laying down the limits][tune:level]No ^people on Malta before about eight and a half ^thousand years ago. [act:the second limit, firm][tune:fall]No ^wheels ^anywhere before about {3500|thirty-five hundred} BCE.",
                          "[d:build][sfx:hit][act:the flaw, pointed and calm][tune:fall]Koltypin dated the ^rock, not the ^groove. [go:5|0][act:the second flaw, steady][tune:level]And the ruts under the sea go down a ^metre or two. [act:the clincher, quiet][tune:fall]Ice Age shores are more than a ^hundred metres deeper."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]^Ice Age ruts? [act:the verdict, firm][tune:fall]*Ruled ^out*. [act:naming the candidates][tune:fall]^Stone Age temple builders, ^Bronze Age farmers or ^Romans? [act:honest, open][tune:fall]Still ^open.",
                     "[d:tension][p:0.93][act:the last word, calm and wise][tune:fall]The age of the ^rock is not the age of the ^road."]),
    ]
    return EP("cart-ruts", "06.08", "The Cart Ruts of Malta: Railway Lines Cut in Stone", "cart-ruts", "debunked", "How old are the cart ruts, and could they be older than any known civilisation?", "Nobody can *date* them.", beats, shots,
              "Mottershead, Pearson & Schaefer 2008 · Groucutt 2022 · Sagona 2004 · Bugeja 2001 · Trump 2002 · Scerri et al. 2025 · Furlani et al. 2013",
              "Paired grooves up to 60 cm deep cross Malta's bare rock, run off cliffs and into the sea: the claim of an Ice Age or older date, how carts cut them, and the dates that box them in.",
              ["#Malta", "#CartRuts", "#Archaeology", "#Mystery", "#History"])


def cart_ruts_m():
    """The cart ruts as one continuous take: thirty-five kilometres in pieces against a marathon, a gauge a little less than a
    person is tall, the million-year claim on a deep-time line, the drowned-road idea, carts cutting deeper in wet limestone,
    the timeline that boxes the ruts in, and the shallow drowned ruts against the deep Ice Age shore."""
    import copy
    from illus import person, arrow, line, glow, label, dot, box as bx, ring, question, strike, oval, AMBER as AMB, BLUE, LILAC, BONE as BN, INK, RED as RD, GREEN as GR
    ep = copy.deepcopy(cart_ruts())
    S = ep["shots"]
    ROCK, SOIL, RUT = "#d9c8a0", "#6d5a3e", "#6d5a3e"
    s0 = _spin(_bare(S[0], keep=("some run into the sea",)), .25)
    hook = question(470, 560, .3, 90)
    # 1 · the map: the pieces, joined: about 35 km, almost a marathon (42 km), at the same scale
    pieces = [bx(70, 1270, 860, 150, "rgba(18,13,10,.88)", "#8c7152", 2, 14, 5.8)] + \
             [line([[110 + 60 * k, 1310 + 14 * (k % 3)], [150 + 60 * k, 1310 + 14 * (k % 3)]], round(6.2 + .1 * k, 2), "#c9ad85", 5, dur=.2) for k in range(10)] + \
             [line([[110, 1310], [110 + 580, 1310]], 9.8, GOLD, 6, dur=.8), label(700, 1320, "35 km", 10.4, GOLD, 30, "start"),
              line([[110, 1380], [110 + 700, 1380]], 11.6, BN, 4, "inferred", .8), label(820, 1390, "marathon", 12.2, BN, 28, "start")]
    # 3 · the gauge: two grooves about 1.40 m apart; stood on end, a little less than a person is tall (250 px per metre)
    gauge = {"base": "dark", "cam": [1, 500, 900], "els": [
        {"k": "poly", "p": [[60, 640], [295, 640], [305, 700], [345, 700], [355, 640], [645, 640], [655, 700], [695, 700], [705, 640], [940, 640], [940, 820], [60, 820]],
         "fill": ROCK, "c": "#fff3dc", "w": 2, "in": .2},
        ring(325, 680, 50, .9, GOLD, 3, dur=.5), ring(675, 680, 50, 1.2, GOLD, 3, dur=.5),
        {"k": "dim", "x1": 325, "y1": 570, "x2": 675, "y2": 570, "t": "about 1.40 m", "in": 3.4, "c": GOLD},
        line([[150, 1320], [850, 1320]], 5.8, "#8c7152", 3, draw=False),
        bx(380, 1320 - 350, 60, 350, GOLD, r=4, at=6.2, fx="fill", dur=.8), label(360, 1150, "1.40 m", 6.8, GOLD, 30, "end"),
        person(600, 1320, 425, 7.2), label(600, 1380, "1.70 m", 7.8, BN, 28)]}
    # 4 · deep time: the claim at 12 to 14 million years, every human far to the right (14 My across 800 px)
    MX = lambda my: round(900 - my * 800 / 14, 1)
    deep = {"base": "dark", "cam": [1, 500, 900], "els": [
        line([[100, 700], [900, 700]], .3, BN, 3, dur=.8), label(100, 760, "14 million years ago", .6, "#cbbca8", 28, "start"), label(900, 760, "today", .6, "#cbbca8", 28, "end"),
        bx(MX(14), 684, MX(12) - MX(14), 32, LILAC, LILAC, 3, 16, 5.2, op=.55), glow(MX(13), 700, 90, 5.4, .5),
        label(MX(13) - 14, 640, "the claim", 5.8, LILAC, 30, "start")] +
        [person(MX(2.8) + 32 * k, 690, 40 + 4 * k, round(8.4 + .15 * k, 2)) for k in range(5)] +
        [line([[MX(2.8), 600], [MX(2.8), 585], [895, 585], [895, 600]], 9.8, GOLD, 3, dur=.6), label(895, 560, "all humans", 10.4, GOLD, 28, "end")]}
    WX = lambda yr: round(120 + (yr + 7000) * 760 / 9000, 1)
    limits = [line([[897, 716], [880, 1100]], .9, BN, 2, "inferred", .5), line([[897, 716], [120, 1100]], .9, BN, 2, "inferred", .5), ring(897, 700, 14, .7, GOLD, 3, dur=.3),
              line([[120, 1150], [880, 1150]], .4, BN, 3, dur=.7), label(120, 1210, "7000 BCE", .8, "#cbbca8", 28, "start"), label(880, 1210, "today", .8, "#cbbca8", 28, "end"),
              person(WX(-6500), 1140, 70, 4.4), line([[WX(-6500), 1135], [WX(-6500), 1165]], 4.4, BN, 3, draw=False), label(WX(-6500) - 20, 1050, "people arrive", 5.0, BN, 28, "start"),
              ring(WX(-3500), 1085, 34, 8.4, GOLD, 4, dur=.5)] + \
             [line([[WX(-3500) - 30 * math.cos(a), 1085 - 30 * math.sin(a)], [WX(-3500) + 30 * math.cos(a), 1085 + 30 * math.sin(a)]], 8.8, GOLD, 2, draw=False) for a in (0, math.pi / 3, 2 * math.pi / 3)] + \
             [label(WX(-3500), 1280, "first wheels", 9.2, GOLD, 28), bx(WX(-3500), 1300, 880 - WX(-3500), 26, GOLD, r=13, at=11.2, fx="fill", op=.7),
              label(880, 1370, "carts, then ruts", 11.8, GOLD, 28, "end")]
    rockage = [strike(MX(14) - 6, 720, MX(12) + 6, 676, 1.0, RD, 6), label(MX(13), 820, "the rock's age", 1.8, RD, 28)]
    # 5 · the drowned-road idea: ruts slide under the sea; a dotted road down to a lost Ice Age shore; the sea stood far lower
    SEA_Y, ICE_Y = 760, 1300                              # 25 px per metre: the ruts end about 1.2 m down; the Ice Age line about 22 m down
    land = {"k": "poly", "p": [[60, 640], [440, 640], [520, SEA_Y + 30], [700, 980], [860, 1200], [940, 1320], [940, 1420], [60, 1420]], "fill": ROCK, "c": "#fff3dc", "w": 2, "in": .2}
    sea = {"base": "dark", "cam": [1, 500, 900], "els":
           [{"k": "water", "y": SEA_Y, "h": 700, "x0": 440, "x1": 1000, "op": .55, "in": .1}, land,
            line([[120, 640], [440, 640], [520, SEA_Y + 30]], .6, RUT, 6, dur=.8), line([[120, 652], [440, 652], [516, SEA_Y + 40]], .7, "#4a3a28", 4, dur=.8),
            ring(505, SEA_Y + 10, 44, 2.4, BLUE, 3, dur=.5),
            line([[537, SEA_Y + 40], [714, 990], [874, 1205], [936, ICE_Y - 10]], 5.4, LILAC, 6, "claimed", 1.0)] + question(780, 1060, 7.0, 60) +
           [{"k": "poly", "p": [[90, 420], [200, 360], [330, 380], [380, 440], [300, 470], [140, 470]], "fill": "#eef6fb", "c": BLUE, "w": 2, "in": 9.8, "fx": "rise"},
            label(235, 520, "ice", 10.2, BLUE, 28),
            arrow([[880, SEA_Y + 20], [880, ICE_Y - 20]], 12.4, BLUE, 3, "known", .8, False), line([[600, ICE_Y], [940, ICE_Y]], 13.4, BLUE, 3, "inferred", .6),
            label(860, ICE_Y + 50, "Ice Age sea", 14.0, BLUE, 28, "end")]}
    flaw = [{"k": "dim", "x1": 470, "y1": SEA_Y, "x2": 470, "y2": SEA_Y + 30, "in": .6, "c": GOLD, "upright": True}, label(455, SEA_Y + 90, "1 to 2 m", 1.0, GOLD, 30, "end"),
            {"k": "dim", "x1": 600, "y1": SEA_Y + 40, "x2": 600, "y2": ICE_Y, "t": "over 100 m", "in": 4.2, "c": BN, "lx": -26},
            strike(700, 1050, 860, 930, 6.2, RD, 5)]
    # 2 · how carts cut them: a two-wheeled cart, thin soil, rain; wet limestone softens; every pass deeper, then a new line
    cart = [bx(60, 700, 880, 260, ROCK, "#fff3dc", 2, 0, .2), bx(60, 684, 880, 18, SOIL, r=0, at=3.4, fx="fill")] + \
           [bx(260, 520, 300, 80, "#8c6a48", "#c9a070", 2, 6, 1.6, fx="rise"), line([[560, 560], [720, 600]], 1.8, "#8c6a48", 8, draw=False),
            ring(400, 620, 62, 1.8, "#c9a070", 8, dur=.6), dot(400, 620, 10, "#c9a070", 1.8), person(780, 684, 120, 2.2)] + \
           [line([[x, y], [x - 8, y + 26]], round(4.8 + .03 * k, 2), BLUE, 2, draw=False) for k, (x, y) in enumerate([(100 + (j * 97) % 820, 330 + (j * 53) % 150) for j in range(30)])] + \
           [bx(60, 700, 880, 50, BLUE, r=0, at=7.0, op=.25), label(500, 1010, "wet limestone softens", 7.4, BLUE, 28)]
    deeper = []
    for k, d in enumerate((30, 70, 110)):
        at = round(.6 + 1.2 * k, 2)
        deeper += [line([[160, 1120], [270, 1120], [280, 1120 + d], [330, 1120 + d], [340, 1120], [560, 1120], [570, 1120 + d], [620, 1120 + d], [630, 1120], [700, 1120]], at, "#fff3dc" if k < 2 else GOLD, 3 if k < 2 else 4, dur=.6)]
    deeper = [bx(140, 1120, 580, 260, ROCK, r=0, at=.2)] + deeper + \
             [bx(285, 1120 + 110 - 150, 40, 150, "#6b4a2e", "#c9a070", 2, 2, 3.6), bx(575, 1120 + 110 - 150, 40, 150, "#6b4a2e", "#c9a070", 2, 2, 3.6),
              line([[300, 1100], [600, 1100]], 4.0, "#8c6a48", 10, draw=False), glow(450, 1118, 70, 5.2, .9, "red"), label(450, 1060, "the axle scrapes", 5.4, RD, 28),
              arrow([[660, 1080], [780, 1080]], 7.6, AMB, 3, "known", .5, False)] + \
             [line([[800, 1120], [810, 1150], [840, 1150], [850, 1120]], 8.4, GOLD, 4, dur=.4), label(825, 1210, "new line", 8.8, GOLD, 28)] + \
             [line(p, round(11.4 + .2 * k, 2), RUT, 4, dur=.5, curve=True) for k, p in enumerate((
                 [[620, 1300], [760, 1340], [920, 1370]], [[620, 1330], [760, 1370], [920, 1400]], [[640, 1400], [780, 1330], [920, 1290]], [[660, 1410], [800, 1350], [930, 1320]]))]
    mech = {"base": "dark", "cam": [1, 500, 900], "els": cart}
    out = _take(ep, scenes={0: s0, 2: mech, 3: gauge, 4: deep, 5: sea}, alias={6: 0}, cams={6: [1.18, 480, 960]}, adds={1: pieces},
                beat_adds={4: (limits, None)}, line_adds={(0, 1): (hook, None), (3, 1): (deeper, None), (4, 1): (rockage, None)})
    return _inject(out, _go(out, 4, 1, 1), flaw)


# ---------------------------------------------------------------- 06.09 The ledger (the cabinet: one continuous film)
def _ledger_v1():
    from cabinet import Cabinet
    hero = lambda fn: next(e for e in fn()["shots"][0]["els"] if e.get("k") == "iso")
    C = Cabinet([
        {"name": "Nan Madol", "model": hero(nan_madol)},
        {"name": "Plain of Jars", "model": hero(plain_of_jars)},
        {"name": "Puma Punku", "model": hero(puma_punku)},
        {"name": "Baalbek", "model": hero(baalbek)},
        {"name": "Sacsayhuamán", "model": hero(sacsayhuaman)},
        {"name": "Gunung Padang", "model": hero(gunung_padang)},
        {"name": "Diquís spheres", "model": hero(diquis)},
        {"name": "Malta's cart ruts", "model": hero(cart_ruts)},
    ])
    C.build()                                                                                     # 0 the whole cabinet lights up, niche by niche
    NM, JAR, PP, BA, SQ, GP, DQ, MT = range(8)
    s1 = C.step(C.cam_cell(NM), C.verdict(NM, "strong", "Pohnpeians, from c. 1180", .5) + C.people(NM, 3, at=1.0))
    s2 = C.step(C.cam_cell(JAR), C.verdict(JAR, "strong", "burials, in their later life", .4))
    s3 = C.step(C.cam_cell(PP), C.verdict(PP, "strong", "Tiwanaku, from AD 536", .4) + C.people(PP, 3, at=.9))
    claimed = lambda it: dict(it, style="claimed", op=.25, xray=True, c="#9fd0ff", edge="rgba(159,208,255,.95)")
    s4 = C.step(C.cam_cell(BA), C.verdict(BA, "awaiting", "an older builder?", .4) + [C.iso_like(BA, [claimed({"t": "box", "x": 0, "z": 0, "y": -7, "w": 62, "d": 6, "h": 7})], **{"in": 1.0})])
    s5 = C.step(C.cam_cell(SQ), C.verdict(SQ, "awaiting", "older walls beneath?", .4) + [C.iso_like(SQ, [claimed({"t": "box", "x": 0, "z": 0, "y": -8, "w": 110, "d": 30, "h": 8})], **{"in": .9})])
    s6 = C.step(C.cam_cell(GP), C.verdict(GP, "awaiting", "a pyramid, 27,000 years old?", .4) + [C.iso_like(GP, [claimed({"t": "pyr", "x": 0, "z": 0, "y": -2, "b": 78, "h": 36})], **{"in": .9})])
    sky = [{"k": "line", "p": [[-60 + 60 * k, -70], [-150 + 150 * k, -236]], "c": "#9fd0ff", "w": 2, "style": "claimed", "fx": "draw", "in": .8 + .15 * k} for k in range(3)]
    s7 = C.step(C.cam_cell(DQ), C.verdict(DQ, "awaiting", "aimed at the sky?", .4) + C.local(DQ, sky + [{"k": "stars", "n": 16, "x0": -180, "x1": 180, "y0": -236, "y1": -196, "seed": 7, "in": .7}]))
    trench = lambda i, at: C.local(i, [{"k": "rect", "x": -C.w * .40, "y": -C.h * .58, "w": C.w * .80, "h": C.h * .62, "r": 10, "fill": "rgba(159,208,255,.04)", "c": "#9fd0ff", "sw": 2.4,
                                       "style": "inferred", "fx": "draw", "dur": 1.0, "in": at}])
    s8 = C.step(C.cam_cells([BA, SQ, GP, DQ]), trench(BA, .3) + trench(SQ, .5) + trench(GP, .7) + trench(DQ, .9))
    s9 = C.step(C.cam_cell(PP), C.verdict(PP, "ruled", frame=False, at=.3) + C.struck(PP, "built in 15,000 BCE", dy=-150, at=.6))
    s10 = C.step(C.cam_cell(MT), C.verdict(MT, "ruled", at=.3) + C.struck(MT, "cut in the Ice Age", dy=-170, at=.6))
    top = C.cam_cells([NM, JAR, PP, BA])
    s11 = C.step(top, C.question(PP, dx=C.w * .22, dy=-150, at=.2) + C.note(PP, "how was it shaped?", at=.5, c="#f2c98e"))
    s12 = C.step(top, C.question(JAR, dx=C.w * .22, dy=-150, at=.1) + C.note(JAR, "first made for?", at=.4, c="#f2c98e"), keep_notes=True)
    s13 = C.step(top, C.question(BA, dx=C.w * .22, dy=-150, at=.1) + C.note(BA, "how was it lifted?", at=.4, c="#f2c98e"), keep_notes=True)
    s14 = C.step(C.cam_all())
    s15 = C.step(C.cam_all(), [e for i in (JAR, BA, SQ, GP, DQ, MT) for e in C.people(i, 3, at=.2 + .1 * i)])
    s16 = C.step(C.cam_all(z=.64, sy=700))
    shots = C.shots
    beats = [
        B("hook", 0, ["[d:intrigue][sfx:boom][act:inviting, a warm opener]Eight places where the stones seem too ^big, too ^precise, or too ^old. [act:brisk, rolling up sleeves][tune:fall]Here's the ^ledger."], cut=False),
        B("world", s1, ["[d:calm][act:confident, ticking them off][tune:level]Nan Madol, built by ^Pohnpeians from about eleven eighty. [go:%d|1.1][act:with care][tune:level]The jars of Laos, holding the ^dead. [go:%d|1.3][act:the last one, settled][tune:fall]Puma Punku, a ^Tiwanaku temple from the ^sixth century." % (s2, s3)], cut=False),
        B("collision", s4, ["[d:build][act:fair, going down the column][tune:level]An older builder at ^Baalbek. [go:%d|1.2][act:same even pace][tune:level]Older walls under ^Sacsayhuamán. [go:%d|1.1][act:steady, unhurried][tune:level]A twenty-seven-thousand-year pyramid in ^Java. [go:%d|1.2][act:closing the column][tune:fall]Spheres aimed at the ^sky. [go:%d|1.4][d:aside][act:a gentle explanation]Waiting means ^nobody has dug the ^decisive spot yet." % (s5, s6, s7, s8)], cut=False),
        B("cost", s9, ["[d:reveal][sfx:hit][act:crisp, closing doors][tune:level]Puma Punku in ^fifteen thousand BCE. [go:%d|1.5][act:same, and final][tune:fall]Cart ruts from the ^Ice Age." % s10], cut=False),
        B("reversal", s11, ["[d:build][act:genuine curiosity, open][tune:level]How exactly the hard stone was ^shaped. [go:%d|.6][act:still curious][tune:level]What the jars were ^first made for. [go:%d|.6][act:the last open door][tune:fall]How the heaviest blocks were ^lifted. [d:aside][act:candid, warm]The honest answer to 'how' is often: we have good ^ideas, not ^certainty." % (s12, s13)], cut=False),
        B("tag", s14, ["[d:verdict][p:0.95][act:calm, grounding][tune:fall]The stones are ^real. [go:%d|.8][act:warm, turning to the people]So is the ^skill of the ^people who moved them. [act:tender wonder]That's the ^real mystery, and it's a ^beautiful one." % s15,
                       "[d:tension][p:0.93][go:%d|4][act:the motto, quiet and sure][tune:fall]^Coherence is the measure. [gap:0.45][act:gentle, the closing note][tune:fall]Not ^final demonstration." % s16], cut=False),
    ]
    return EP("stones-ledger", "06.09", "Impossible Stones · The Ledger", "", "mixed", "What stands, what waits, and what the stones never said.", "Here's the *ledger*.", beats, shots,
              "Every source in the eight case files of File 06",
              "The verdicts of Impossible Stones in one ledger: what has strong evidence, what is awaiting evidence, what is ruled out, and what is still open.",
              ["#History", "#Megaliths", "#AncientEngineering", "#Archaeology", "#WeighItYourself"])


def ledger():
    """Impossible Stones, the recap, told like a science show: every case gets its own moment in the cabinet (where it is, the mystery,
    a little demonstration of how we know, the verdict), then the eight are read together. One continuous take (see cabinet.py)."""
    from cabinet import Cabinet, VCOL
    hero = lambda fn: next(e for e in fn()["shots"][0]["els"] if e.get("k") == "iso")
    C = Cabinet([
        {"name": "Nan Madol", "model": hero(nan_madol)},
        {"name": "Plain of Jars", "model": hero(plain_of_jars)},
        {"name": "Puma Punku", "model": hero(puma_punku)},
        {"name": "Baalbek", "model": hero(baalbek)},
        {"name": "Sacsayhuamán", "model": hero(sacsayhuaman)},
        {"name": "Gunung Padang", "model": hero(gunung_padang)},
        {"name": "Diquís spheres", "model": hero(diquis)},
        {"name": "Malta's cart ruts", "model": hero(cart_ruts)},
    ])
    C.build()
    C.note_min_rows = 2
    NM, JAR, PP, BA, SQ, GP, DQ, MT = range(8)
    AMB, BLUE, BONE_, RED_ = "#f2c98e", "#9fd0ff", "#e9dccb", "#ff8a7a"
    s_all = C.step(C.cam_all(k=.95), [e for i in range(8) for e in C.question(i, dx=C.w * .3, dy=-190, at=.2 + .08 * i, size=46, c="#c9c1ee", id="q%d" % i)])
    claimed = lambda it: dict(it, style="claimed", op=.25, xray=True, c=BLUE, edge="rgba(159,208,255,.95)")
    L_ = C.local

    def case(i, where, claim, evid, verdict):
        """claim, evid and verdict are callables, drawn in order, so notes and chips stack in the order they appear."""
        a = C.step(C.cam_cell(i), C.note(i, where, at=.5, c=BONE_), drop=["q%d" % k for k in range(8)] if i == NM else ())
        b = C.step(C.cam_cell(i), claim(), keep_notes=True)
        c = C.step(C.cam_cell(i), evid(), keep_notes=True)
        d = C.step(C.cam_cell(i), verdict(), keep_notes=True)
        return a, b, c, d
    # the little demonstrations, in niche units (0, 0 = middle of the shelf; the free space is on the right, above the model)
    hourglass = lambda i: L_(i, [{"k": "line", "p": [[120, -250], [180, -250], [150, -205], [180, -160], [120, -160], [150, -205], [120, -250]], "c": BONE_, "w": 3, "in": .3},
                                 {"k": "poly", "p": [[126, -245], [174, -245], [150, -210]], "fill": AMB, "c": "none", "w": 0, "in": .4},
                                 {"k": "poly", "p": [[128, -164], [172, -164], [150, -186]], "fill": AMB, "c": "none", "w": 0, "in": 1.6, "fx": "fill", "dur": 2.0},
                                 {"k": "line", "p": [[150, -205], [150, -170]], "c": AMB, "w": 2, "style": "inferred", "in": 1.2}])
    candle = lambda i: L_(i, [{"k": "rect", "x": 140, "y": -210, "w": 22, "h": 70, "r": 3, "fill": "#efe6d2", "c": "none", "sw": 0, "in": .6},
                              {"k": "glow", "x": 151, "y": -222, "r": 40, "kind": "fire", "op": .9, "keepop": True, "in": .7},
                              {"k": "circle", "x": 151, "y": -220, "r": 6, "fill": "#ffcf8a", "c": "none", "w": 0, "in": .7}])
    capstans = lambda i: L_(i, [x for k in range(6) for x in (
        {"k": "circle", "x": -150 + 60 * k, "y": -14, "r": 11, "fill": "none", "c": AMB, "w": 3, "in": 3.2 + .12 * k, "fx": "draw", "dur": .4},
        {"k": "line", "p": [[-150 + 60 * k, -25], [-60 + 24 * k, -110]], "c": AMB, "w": 1.5, "in": 3.4 + .12 * k, "fx": "draw", "dur": .5},
        {"k": "person", "x": -128 + 60 * k, "y": -2, "h": 30, "t": False, "color": "#e8d6b8", "in": 3.5 + .12 * k, "fx": "rise"})])
    hammer = lambda i: L_(i, [{"k": "circle", "x": 150, "y": -200, "r": 16, "fill": "#8a8378", "c": "#cbbca8", "w": 2, "in": 3.0, "fx": "pop"}] +
                          [{"k": "line", "p": [[122 + 18 * k, -175], [118 + 18 * k, -160]], "c": AMB, "w": 3, "in": 3.3 + .25 * k} for k in range(3)])
    hexes = lambda i: L_(i, [{"k": "line", "p": [[cx + 22 * math.cos(math.radians(60 * m)), cy + 22 * math.sin(math.radians(60 * m))] for m in range(7)], "c": AMB, "w": 3,
                              "in": .6 + .3 * k, "fx": "draw", "dur": .5} for k, (cx, cy) in enumerate(((120, -220), (158, -198), (120, -176), (158, -154)))])
    shuffle = lambda i: L_(i, [{"k": "arrow", "p": [[x0, y0], [(x0 + x1) / 2, min(y0, y1) - 40], [x1, y1]], "curve": True, "c": BLUE, "w": 2, "style": "claimed", "fx": "draw", "dur": .7,
                                "in": 1.4 + .3 * k} for k, (x0, y0, x1, y1) in enumerate(((-120, -60, 60, -100), (40, -40, -60, -120), (120, -80, 160, -180), (-40, -110, -150, -150)))])
    cart = lambda i: L_(i, [{"k": "rect", "x": 100, "y": -232, "w": 90, "h": 34, "r": 4, "fill": "#8a6a48", "c": "none", "sw": 0, "in": .4},
                            {"k": "circle", "x": 112, "y": -190, "r": 16, "fill": "none", "c": BONE_, "w": 4, "in": .5}, {"k": "circle", "x": 178, "y": -190, "r": 16, "fill": "none", "c": BONE_, "w": 4, "in": .5}] +
                           [{"k": "line", "p": [[96, -168 + 7 * k], [196, -168 + 7 * k]], "c": AMB, "w": 2, "in": 1.2 + .4 * k} for k in range(3)])
    K = {}
    K[NM] = case(NM, "Pohnpei, in the middle of the Pacific", lambda: C.question(NM, dx=-C.w * .05, dy=-215, at=.2, size=64),
                 lambda: hourglass(NM) + C.note(NM, "coral: c. 1180 CE", at=3.4, c=AMB, stack=True),
                 lambda: C.verdict(NM, "strong", "built by Pohnpeians", .2) + C.people(NM, 3, at=.6))
    K[JAR] = case(JAR, "the Xieng Khouang plateau, Laos", lambda: C.question(JAR, dx=C.w * .3, dy=-190, at=.2, size=70),
                  lambda: C.note(JAR, "human bones: c. 900–1200 CE", at=.8, c=AMB, stack=True),
                  lambda: C.verdict(JAR, "strong", "jars for the dead", .2) + C.verdict(JAR, "open", "first made for?", 2.4, frame=False))
    K[PP] = case(PP, "near Lake Titicaca, Bolivia", lambda: C.claim(PP, "15,000 BCE?", at=.4, rows=1),
                 lambda: candle(PP) + C.note(PP, "radiocarbon: 6th century CE", at=4.6, c=AMB, stack=True) + C.people(PP, 3, at=5.0),
                 lambda: C.verdict(PP, "ruled", at=.1) + C.strike_claim(PP, .4))
    K[BA] = case(BA, "the Beqaa valley, Lebanon", lambda: [C.iso_like(BA, [claimed({"t": "box", "x": 0, "z": 0, "y": -7, "w": 62, "d": 6, "h": 7})], **{"in": .3})],
                 lambda: C.note(BA, "below: ordinary stones", at=1.2, c=AMB, stack=True) + capstans(BA),
                 lambda: C.verdict(BA, "awaiting", "an older builder?", .2))
    K[SQ] = case(SQ, "above Cusco, Peru", lambda: [C.iso_like(SQ, [claimed({"t": "box", "x": 0, "z": 0, "y": -8, "w": 110, "d": 30, "h": 8})], **{"in": .3})],
                 lambda: C.people(SQ, 4, at=.6) + hammer(SQ),
                 lambda: C.verdict(SQ, "awaiting", "older walls?", .2))
    K[GP] = case(GP, "West Java, Indonesia", lambda: [C.iso_like(GP, [claimed({"t": "pyr", "x": 0, "z": 0, "y": -2, "b": 78, "h": 36})], **{"in": .4})] + C.note(GP, "a paper, 2023 · withdrawn", at=2.6, c=RED_, stack=True),
                 lambda: hexes(GP),
                 lambda: C.verdict(GP, "awaiting", "a deep dig, published", .2))
    sky = [{"k": "line", "p": [[-60 + 60 * k, -70], [-150 + 150 * k, -236]], "c": BLUE, "w": 2, "style": "claimed", "fx": "draw", "in": .4 + .15 * k} for k in range(3)]
    K[DQ] = case(DQ, "the Diquís delta, Costa Rica", lambda: L_(DQ, sky + [{"k": "stars", "n": 16, "x0": -180, "x1": 180, "y0": -236, "y1": -196, "seed": 7, "in": .3}]),
                 lambda: shuffle(DQ),
                 lambda: C.verdict(DQ, "awaiting", "aimed at the sky?", .2))
    K[MT] = case(MT, "Malta, in the Mediterranean", lambda: C.claim(MT, "Ice Age roads?", at=.3, rows=1),
                 lambda: cart(MT) + C.note(MT, "people: c. 6500 BCE · wheels: c. 3500 BCE", at=4.8, c=AMB, stack=True),
                 lambda: C.verdict(MT, "ruled", at=.1) + C.strike_claim(MT, .4))
    e1 = C.step(C.cam_all())
    e2 = C.step(C.cam_all(), [x for i in (NM, JAR, PP, MT) for x in C.wash(i, VCOL["strong"], at=.2 + .15 * i, op=.13)])
    trench = lambda i, at: L_(i, [{"k": "rect", "x": -C.w * .40, "y": -C.h * .58, "w": C.w * .80, "h": C.h * .62, "r": 10, "fill": "rgba(159,208,255,.04)", "c": BLUE, "sw": 2.4,
                                   "style": "inferred", "fx": "draw", "dur": 1.0, "in": at}])
    e3 = C.step(C.cam_all(), trench(BA, .2) + trench(SQ, .35) + trench(GP, .5) + trench(DQ, .65))
    e4 = C.step(C.cam_all(), [x for i in range(8) for x in C.people(i, 3, at=.2 + .1 * i)])
    e5 = C.step(C.cam_all(k=.86, sy=720))
    g = lambda st, d=".6": "[go:%d|%s]" % (st, d)

    def L(i, t1, t2, t3, t4):
        a, b, c, d = K[i]
        return "[gap:0.4]" + g(a, "1.5") + t1 + " " + g(b) + t2 + " " + g(c) + t3 + " " + g(d) + t4
    P = "[p:0.93]"
    beats = [
        B("hook", 0, ["[d:intrigue][sfx:boom][p:0.94][act:hushed, drawing us in]Imagine a single stone as heavy as about five hundred ^cars. [act:a playful challenge]Now imagine moving it... with no ^engines. " +
                      g(s_all, "1.3") + "[act:wonder, widening out]All over the world there are stones like that: too ^big, too ^precise, or too ^old, it seems, for the people who lived nearby. "
                      "[act:the big question, clear][tune:rise]So who ^really built them? [act:bright, rolling up sleeves][tune:fall]Let's investigate ^eight of them, one by ^one."], cut=False),
        B("world", s_all, [
            L(NM, "[d:calm]" + P + "[act:storytelling, like a guide]First stop: ^Nan Madol, on a tiny island lost in the middle of the ^Pacific. [act:painting the picture]Nearly a hundred artificial islands, built from black stone columns stacked like ^logs.",
              "[act:raising the old idea, playful][tune:rise]The ruin of a sunken ^continent, some said?",
              "[act:explaining, delighted by the trick]Here's how we know. Coral used@verb in a royal tomb works like an ^hourglass: once it's cut, a trace of uranium in it slowly turns into ^thorium. [act:landing it]The hourglass reads about {1180|eleven eighty} CE.",
              "[act:the verdict, settled][tune:fall]Built by the island's own people: *strong ^evidence*."),
            L(JAR, P + "[act:storytelling]Next: the ^Plain of Jars, in Laos. [act:painting the picture]More than two thousand stone jars, some taller than a ^person.",
              "[act:genuinely curious][tune:rise]What on Earth were they ^for?",
              "[act:the evidence, gentle]Archaeologists looked inside. Human ^bones, from people buried about {900|nine hundred} to {1200|twelve hundred} CE.",
              "[act:the verdict][tune:fall]Jars for the dead: *strong ^evidence*. [act:a curious caveat][tune:rise]But what they were ^first made for? [act:light][tune:fall]Still ^open.")], cut=False),
        B("collision", K[JAR][3], [
            L(PP, "[d:build]" + P + "[act:storytelling]Now, Bolivia, near Lake ^Titicaca: ^Puma Punku. [act:admiring]Blocks with razor-sharp corners, and one slab about as heavy as a ^blue whale.",
              "[act:the old claim, fair]An early explorer measured its alignment with the ^stars, and announced: fifteen thousand ^BCE.",
              "[act:explaining, clear and friendly]So, the test: radiocarbon. Every living thing holds a little radioactive ^carbon, and after death it fades at a steady pace, like a candle burning ^down. [act:landing it]Plant remains from under the platform say: the ^sixth century CE.",
              "[act:the verdict, firm][tune:fall]Fifteen thousand BCE: *ruled ^out*."),
            L(BA, P + "[act:storytelling]^Baalbek, in Lebanon. [act:awed]A Roman temple sits on stones of about eight hundred ^tonnes each, among the heaviest ever ^moved.",
              "[act:the question, fair][tune:rise]Could an older, forgotten civilisation have left them ^there?",
              "[act:the evidence]Archaeologists dug underneath: the older layer is made of ^ordinary stones. [act:explaining, a little demo]And an engineer worked out how Romans could move one giant: six ^capstans, about a hundred and fifty people, turning, and turning, and ^turning.",
              "[act:the verdict, even][tune:fall]An older builder: *awaiting ^evidence*. [act:plain]Everything found so far points to ^Rome.")], cut=False),
        B("cost", K[BA][3], [
            L(SQ, "[d:build]" + P + "[act:storytelling]^Sacsayhuamán, above Cusco, in Peru. [act:admiring]Stones of more than a hundred tonnes, fitted so tightly you can't slip a ^knife blade between them.",
              "[act:the claim, fair][tune:rise]Did the Incas just build on top of ^older walls?",
              "[act:the evidence]Spanish writers who saw it in the fifteen hundreds describe an ^Inca work, with ^thousands of workers. [act:explaining, a little demo]And the fit? Lower the stone, mark the high spots, pound them down with a harder stone, try ^again. [act:warm]^Patience.",
              "[act:the verdict, even][tune:fall]Older walls: *awaiting ^evidence*."),
            L(GP, P + "[act:storytelling]^Gunung Padang, in Java: stone terraces on top of a ^hill.",
              "[act:the claim, measured]In {2023|twenty twenty-three}, a science journal published it as a pyramid twenty-seven thousand years ^old. [act:the twist][tune:fall]Then it withdrew the ^paper.",
              "[act:explaining, clear]Why? The stone columns can form ^all by themselves: cooling lava cracks into neat prisms, a bit like mud drying in the ^sun. [act:precise]And the dated soil wasn't tied to anything ^people had made.",
              "[act:the verdict, even][tune:fall]*Awaiting ^evidence*, until someone digs deep, and ^publishes.")], cut=False),
        B("reversal", K[GP][3], [
            L(DQ, "[d:build]" + P + "[act:storytelling]Costa Rica: hundreds of stone ^spheres, some taller than a person, made by local chiefdoms from about {600|six hundred} CE.",
              "[act:the claim][tune:rise]Were some lined up to point at the ^sky?",
              "[act:explaining, with a smile]Problem: nearly all of them were ^moved before anyone mapped them. [act:the analogy]It's like reading a sentence after someone ^shuffled the words.",
              "[act:the verdict, even][tune:fall]Aimed at the sky: *awaiting ^evidence*."),
            L(MT, P + "[act:storytelling]Last stop: ^Malta. [act:painting the picture]Pairs of grooves cut into bare rock, like ^tram lines, some running straight into the ^sea.",
              "[act:the claim][tune:rise]Roads from the ^Ice Age?",
              "[act:explaining, a little demo]Picture a cart on soft, wet limestone: every pass cuts a little deeper, like a sled in ^snow. [act:the evidence, clear]But nobody lived on Malta before about eight and a half thousand years ago, and wheels appear only around {3500|thirty-five hundred} BCE.",
              "[act:the verdict, firm][tune:fall]Ice Age ruts: *ruled ^out*.")], cut=False),
        B("tag", K[MT][3], ["[d:verdict][gap:0.5]" + g(e1, "2") + P + "[act:stepping back, calm]So, what do our eight stones tell us ^together? " + g(e2, ".8") +
                            "[act:clear, warm]Wherever a date could be tested, it pointed to people ^already known to archaeology: islanders, Andean builders, ^Romans. " + g(e3, ".8") +
                            "[act:fair, precise]Where it couldn't, what's missing is a ^trench, or a ^date. [act:firm, gentle][tune:fall]Not a lost ^civilisation. " + g(e4, ".8") +
                            "[act:tender wonder]And the real mystery? How human ^hands moved all this. [act:warm, sincere][tune:fall]That one is ^beautiful.",
                            "[d:tension][p:0.93]" + g(e5, "4") + "[act:the motto, quiet and sure][tune:fall]^Coherence is the measure. [gap:0.45][act:gentle, the closing note][tune:fall]Not ^final demonstration."], cut=False),
    ]
    return EP("stones-ledger", "06.09", "Impossible Stones · The Ledger", "", "mixed", "What stands, what waits, and what the stones never said.", "Who *really* built them?", beats, C.shots,
              "Every source in the eight case files of File 06",
              "Eight places where the stones seem too big, too precise or too old, investigated one by one: where each is, the mystery, how we know, and the verdict.",
              ["#History", "#Megaliths", "#AncientEngineering", "#Archaeology", "#WeighItYourself"])


def EPISODES():
    return [baalbek_m(), puma_punku_m(), sacsayhuaman_m(), gunung_padang_m(), nan_madol_m(), plain_of_jars_m(), diquis_m(), cart_ruts_m(), ledger()]
