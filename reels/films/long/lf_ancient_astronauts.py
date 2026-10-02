"""LF.09 · The Method · Ancient Astronauts: Six Clues, Weighed (16:9 long film, one wall).

Script: films/long/lf-ancient-astronauts/script.json. Its lines are read from there, word for word; this module only adds the
[go:N|t] markers where the picture changes (see BEATS). One shot per script shot s1..s48 (ep shot index = s number - 1).
Facts: the script's facts_added and sources (von Däniken 1968 and his 2026 obituaries; Lhote 1958, Keenan 2000/2002,
Mercier et al. 2012, Soukopova 2012 for Tassili; Waitkus 1997/2002, Feder 2014, Weeks 1998 for Dendera; Ruz 1973, Schele &
Freidel 1990, Stuart & Stuart 2008 for Palenque; Nickell 1983, Sakai et al. 2024 for Nazca; Heinrich 2008 for Klerksdorp;
König 1938, Eggert 1996 for the Baghdad jar), and the Shorts 'ancient-astronauts', 'tassili', 'ooparts', 'power-plant'.

Drawings are schematic and true to the numbers said: solid = evidence, dashed = inferred, dotted lilac = claimed (every
saucer, helmet, rocket, runway and 'bulb' is drawn dotted). Gods are named, never drawn as beings; the Maya king appears
only as his carved image. Scales: the lid 3.7 m tall beside a 1.7 m person; the Round Head about three people tall beside
its copyist; the hummingbird 93 m against a 100 m bar with a 1.7 m person; Nickell's condor 134 m; the statue of Harsomtus
four palms (30 cm) against its ruler; the spheres 0.5 to 10 cm against a 10 cm ruler; the jar 15 cm with its 9 cm tube;
deep time from 3 billion years ago to today on one bar.

Engine workaround (as in lf_gobekli.py / lf_atlantis.py): the wall only adds elements to a panel on its first visit, at a beat
start or a line start. A shot that returns to a panel mid-line (or with additions) is an alias of that panel whose camera zoom
carries a tiny unique tag (+0.0003 per tag, invisible); after the wall is built, the step that reached that camera gets the
shot's additions as a panel item, built on that step's clock (_attach).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-ancient-astronauts/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-ancient-astronauts/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-ancient-astronauts RC_FILMS_EPS=/tmp/claude-0/sbx_lf-ancient-astronauts/files.json \\
  RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-ancient-astronauts/boards python3 films.py long.lf_ancient_astronauts
"""
import json, math, os, random, re
from films import View
from mural import remix, SENT
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, question, ellipse, scatter, \
    BONE, AMBER, RED, GREEN, BLUE, LILAC, AU

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = json.load(open(os.path.join(HERE, "lf-ancient-astronauts", "script.json"), encoding="utf-8"))

W_, H_ = 1778, 1000                   # the 16:9 frame: drawings in x 80..1700, y 120..800 (captions below 815, HUD above 110)
CAM = [1, 889, 500]
GOLD, DIM, INK, WARM = "#f2c98e", "#cbbca8", "#3a2c20", "#ffb07a"
FLAT = "#17120e"                      # flat ground of panels whose drawings are later veiled (wipes of the same colour)
OCHRE, ROCK, ROCK_E = "#b0643c", "#6e5040", "#a88b66"
STONE, STONE_E, CARVE = "#7d7262", "#cfc3a8", "#e9dfc6"
VC = {"ruled": "#ff8a7a", "open": "#c9c1ee", "await": "#9fd0ff"}     # the Shorts' grade colours (f00.grades_m)


# ================================================================ small drawing helpers (panel units)
def R(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def poly(pts, fill, c="none", w=0, at=0, fx=None, curve=False, op=None, **kw):
    e = {"k": "poly", "p": R(pts), "fill": fill, "c": c, "w": w, "curve": curve, "in": at}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(round(x, 1), round(y, 1), round(w, 1), round(h, 1), fill, c, sw, r, at, op, fx, **kw)


def lab(x, y, t, at=0, c=BONE, size=30, a="middle", **kw):
    return label(round(x, 1), round(y, 1), t, at, c, size, a, **kw)


def ln(pts, at=0, c=BONE, w=3, style="known", dur=None, curve=False, draw=True, op=None, **kw):
    e = line(R(pts), at, c, w, style, dur, curve, draw, op)
    e.update(kw)
    return e


def flat(at=-1):
    """A flat ground for the whole panel (wipes of FLAT then veil cleanly)."""
    return rect(-40, -40, W_ + 80, H_ + 80, FLAT, at=at)


def wipe(x, y, w, h, at, fill=FLAT, op=1.0, dur=.5, r=0):
    e = rect(x, y, w, h, fill, r=r, at=at, op=op)
    e["dur"] = dur
    return e


def tick(x, y, at, c=GREEN, s=1.0):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "draw", "dur": .45, "in": at}


def dimline(x1, y1, x2, y2, t, at, c=GOLD, lx=0, ly=None, dur=1.0):
    e = {"k": "dim", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "t": t, "c": c, "fx": "draw", "dur": dur, "in": at, "lx": lx}
    if ly is not None:
        e["ly"] = ly
    return e


def stars(n, x0, x1, y0, y1, at=-1, seed=3):
    return {"k": "stars", "n": n, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "seed": seed, "in": at}


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.92)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, scl=True, fx="pop")]


def ufo(x, y, at, s=1.0, c=LILAC, w=3):
    """A flying saucer, drawn dotted: a claim, not a thing."""
    return [poly(ellipse(x, y, 90 * s, 22 * s, 30)[:-1], "none", c, w, at, curve=True, style="claimed"),
            poly(ellipse(x, y - 20 * s, 40 * s, 26 * s, 16, 180, 360)[:-1] + [[x + 40 * s, y - 20 * s]], "none", c, w, round(at + .2, 2), style="claimed")]


def roundhead(cx, base, h, fill=OCHRE, c="#d8c7ae", op=None, at=.3, arms=True):
    """A Round Head figure (Tassili), arms raised: after f16.roundhead, feet on `base`, h tall."""
    hr = h * .15
    body = [(cx - h * .09, base - h * .72), (cx + h * .09, base - h * .72), (cx + h * .12, base - h * .42), (cx + h * .07, base - h * .02),
            (cx + h * .02, base - h * .02), (cx, base - h * .3), (cx - h * .02, base - h * .02), (cx - h * .07, base - h * .02), (cx - h * .12, base - h * .42)]
    out = []
    if arms:
        for sx in (-1, 1):
            e = ln([(cx + sx * h * .08, base - h * .66), (cx + sx * h * .24, base - h * .78), (cx + sx * h * .3, base - h * .95)], at, fill, h * .045, curve=True, draw=False)
            if op is not None:
                e.update(op=op, keepop=True)
            out.append(e)
    out.append(poly(body, fill, c, 1.5, at, curve=True, op=op))
    hd = {"k": "circle", "x": round(cx, 1), "y": round(base - h * .72 - hr * .9, 1), "r": round(hr, 1), "fill": fill, "c": c, "w": 1.5, "in": round(at + .1, 2)}
    if op is not None:
        hd.update(op=op, keepop=True)
    out.append(hd)
    return out


def head_of(cx, base, h):
    hr = h * .15
    return cx, base - h * .72 - hr * .9, hr


def cow(x, y, s=1.0, at=0, fill="#d8c7ae", op=None, flip=False):
    """A cow in profile (after f16.cow), feet on y."""
    f = -1 if flip else 1
    X = lambda a: round(x + f * a * s, 1)
    Y = lambda b: round(y + b * s, 1)
    w = max(2.0, 9 * s)
    body = [[X(70 * math.cos(t)), Y(-64 + 28 * math.sin(t))] for t in [2 * math.pi * k / 24 for k in range(24)]]
    head = [[X(50), Y(-80)], [X(80), Y(-102)], [X(100), Y(-96)], [X(108), Y(-74)], [X(92), Y(-66)], [X(62), Y(-52)]]
    e = [{"k": "poly", "p": body, "fill": fill, "c": "none", "w": 0, "in": at, "curve": True},
         {"k": "poly", "p": head, "fill": fill, "c": "none", "w": 0, "in": at}] + \
        [{"k": "line", "p": [[X(a), Y(-50)], [X(a), Y(0)]], "c": fill, "w": w, "in": at} for a in (-50, -34, 38, 54)] + \
        [{"k": "line", "p": [[X(-68), Y(-76)], [X(-82), Y(-30)]], "c": fill, "w": w * .4, "in": at},
         {"k": "line", "p": [[X(78), Y(-100)], [X(68), Y(-118)]], "c": fill, "w": w * .45, "in": at},
         {"k": "line", "p": [[X(90), Y(-100)], [X(100), Y(-118)]], "c": fill, "w": w * .45, "in": at}]
    if op is not None:
        for q in e:
            q.update(op=op, keepop=True)
    return e


def palm(x, y, h, at=-1):
    return {"k": "palm", "x": x, "y": y, "h": h, "in": at}


def book(x, y, w, h, at, c="#7a3424", edge="#e0a070", fx="pop", spine=True):
    out = [rect(x, y, w, h, c, edge, 2, 4, at, fx=fx)]
    if spine:
        out.append(rect(x, y, w * .1, h, "rgba(0,0,0,.25)", r=2, at=at, fx=fx))
    return out


def tv(x, y, w, at, glow_c=BLUE):
    """An old television set, its screen glowing: top-left corner at (x, y), w wide."""
    h = w * .78
    return [rect(x, y, w, h, "#3a3029", "#cbbca8", 2, 10, at, fx="pop"), rect(x + w * .08, y + h * .1, w * .66, h * .72, "#1b2733", glow_c, 1.5, 12, at, fx="pop"),
            glow(round(x + w * .41, 1), round(y + h * .46, 1), round(w * .5, 1), at, .35, "scan"),
            dot(round(x + w * .86, 1), round(y + h * .3, 1), w * .04, "#cbbca8", at), dot(round(x + w * .86, 1), round(y + h * .55, 1), w * .04, "#cbbca8", at),
            ln([(x + w * .3, y), (x + w * .18, y - h * .3)], at, "#cbbca8", 2, draw=False), ln([(x + w * .5, y), (x + w * .64, y - h * .32)], at, "#cbbca8", 2, draw=False)]


def reel(x, y, r, at):
    out = [{"k": "circle", "x": x, "y": y, "r": r, "fill": "#2a2420", "c": "#cbbca8", "w": 2.5, "in": at, "fx": "pop"},
           {"k": "circle", "x": x, "y": y, "r": r * .18, "fill": "#cbbca8", "c": "none", "w": 0, "in": at, "fx": "pop"}]
    for k in range(5):
        a = 2 * math.pi * k / 5 - math.pi / 2
        out.append({"k": "circle", "x": round(x + r * .55 * math.cos(a), 1), "y": round(y + r * .55 * math.sin(a), 1), "r": round(r * .2, 1), "fill": "#120e0b", "c": "#8a7a66",
                    "w": 1, "in": at, "fx": "pop"})
    return out


# ================================================================ the carvings (built once as functions, reused)
LID_RATIO = 2.2 / 3.7                 # Pakal's lid: about 2.2 m wide, 3.6 to 3.8 m long


def lid(cx, top, H, t=None, flames=False, rocket=False, carving_only=False):
    """Pakal's sarcophagus lid, drawn upright, schematic: the sky-band border with glyph blocks, the reclining king at the foot (jade
    skirt, jewels, a plume), the cross-shaped World Tree rising behind him with its serpent bar and jewels, the bird on top, the open
    jaws of the underworld below. t: build times {slab, border, man, tree, bird, jaws, flames}; None = everything at once (-1)."""
    t = t or {}
    T = lambda k, d=-1: t.get(k, d)
    W = H * LID_RATIO
    x0, y0 = cx - W / 2, top
    b = W * .07
    fx0, fy0, fw, fh = x0 + b, y0 + b, W - 2 * b, H - 2 * b
    F = lambda u, v: (fx0 + u * fw, fy0 + v * fh)
    s = fw / 300                                             # stroke scale
    els = []
    if not carving_only:
        els += [rect(x0, y0, W, H, "#8f8470", STONE_E, 2.5, 6, T("slab"), fx="pop" if T("slab") > 0 else None),
                rect(fx0, fy0, fw, fh, STONE, "rgba(40,30,20,.6)", 2, 3, T("slab"))]
        r = random.Random(11)
        marks = []
        n_top = 7
        for k in range(n_top):                                  # glyph blocks along the band (all four sides)
            for (u, v) in ((x0 + b * .2 + (W - b * .4) * (k + .5) / n_top, y0 + b * .5), (x0 + b * .2 + (W - b * .4) * (k + .5) / n_top, y0 + H - b * .5)):
                marks.append((u, v))
        n_side = 12
        for k in range(n_side):
            for u in (x0 + b * .5, x0 + W - b * .5):
                marks.append((u, y0 + b + (H - 2 * b) * (k + .5) / n_side))
        for k, (u, v) in enumerate(marks):
            sz = b * (.42 + .1 * r.random())
            els.append(rect(u - sz / 2, v - sz / 2, sz, sz, "none", "#5a5142", 1.6, 2, T("border")))
    c = CARVE
    tt = T("tree")
    tl = lambda d: round(tt + d, 2) if tt > 0 else -1
    # symbols floating in the field around the tree
    for (u, v) in ((.16, .16), (.84, .16), (.12, .50), (.88, .50), (.18, .64), (.84, .62)):
        els.append(rect(F(u, v)[0] - 11 * s, F(u, v)[1] - 11 * s, 22 * s, 22 * s, "none", c, 2.5 * s, 4 * s, tl(1.3)))
    # the World Tree: trunk, cross arms with curled serpent heads, a draped serpent bar, jewels, mirror signs
    els += [ln([F(.5, .74), F(.5, .15)], tt, c, 16 * s, dur=.9 if tt > 0 else None, draw=tt > 0),
            ln([F(.13, .34), F(.87, .34)], tl(.5), c, 13 * s, dur=.7 if tt > 0 else None, draw=tt > 0)]
    for side in (-1, 1):
        u0 = .5 + side * .37
        curl = [F(u0, .34), F(u0 + side * .06, .29), F(u0 + side * .10, .35), F(u0 + side * .06, .42), F(u0 + side * .01, .39)]
        els.append(ln(curl, tl(1.0), c, 7 * s, curve=True, draw=False))
        for k in range(3):
            u = .5 + side * (.14 + .08 * k)
            els += [ln([F(u, .36), F(u, .43 + .015 * k)], tl(1.1), c, 3 * s, draw=False), dot(round(F(u, .45 + .015 * k)[0], 1), round(F(u, .45 + .015 * k)[1], 1), 6 * s, c, tl(1.1))]
    bar = [F(.18 + .64 * k / 16, .385 + .02 * math.sin(k * 1.2)) for k in range(17)]
    els.append(ln(bar, tl(1.2), c, 5 * s, curve=True, draw=False))
    for (u, v) in ((.5, .50), (.5, .25), (.30, .34), (.70, .34)):
        els.append({"k": "circle", "x": round(F(u, v)[0], 1), "y": round(F(u, v)[1], 1), "r": round(10 * s, 1), "fill": STONE, "c": c, "w": 3 * s, "in": tl(1.1)})
    # the bird on top, wings spread
    bird = [F(.5, .155), F(.44, .12), F(.33, .07), F(.25, .085), F(.31, .03), F(.43, .045), F(.5, .0), F(.57, .045), F(.69, .03), F(.75, .085), F(.67, .07), F(.56, .12)]
    els += [poly(bird, c, at=T("bird"), fx="pop" if T("bird") > 0 else None), dot(round(F(.5, .02)[0], 1), round(F(.5, .02)[1], 1), 11 * s, c, T("bird"))]
    # the jaws of the underworld: a wide U with teeth and curled ends; the earth mask the king rests on
    tj = T("jaws")
    els += [ln([F(.10, .80), F(.15, .90), F(.30, .965), F(.5, .98), F(.70, .965), F(.85, .90), F(.90, .80)], tj, c, 10 * s, curve=True,
               dur=.8 if tj > 0 else None, draw=tj > 0),
            ln([F(.10, .80), F(.04, .755), F(.03, .84), F(.09, .86)], tj, c, 8 * s, curve=True, draw=False),
            ln([F(.90, .80), F(.96, .755), F(.97, .84), F(.91, .86)], tj, c, 8 * s, curve=True, draw=False)]
    for k in range(7):
        u = .22 + .56 * k / 6
        v = .925 + .035 * math.sin(math.pi * k / 6)
        els.append(poly([F(u - .022, v - .02), F(u + .022, v - .02), F(u, v - .065)], c, at=tj))
    tm = T("man")
    els.append(poly(ellipse(F(.53, .79)[0], F(.53, .79)[1], .13 * fw, .022 * fh, 20)[:-1], c, at=tm))
    # the king, reclining at the foot of the tree: plume and head up-left, a jade net skirt, one knee raised
    hx, hy = F(.30, .585)
    king = [poly([F(.285, .57), F(.19, .515), F(.22, .50), F(.27, .52), F(.33, .555)], c, at=tm),                     # plume
            {"k": "circle", "x": round(hx, 1), "y": round(hy, 1), "r": round(24 * s, 1), "fill": c, "c": "none", "w": 0, "in": tm},
            poly([F(.31, .615), F(.37, .598), F(.505, .70), F(.48, .745), F(.40, .72)], c, at=tm),                     # torso
            poly([F(.45, .695), F(.53, .695), F(.575, .765), F(.46, .785)], c, at=tm),                                   # skirt
            ln([F(.47, .715), F(.555, .735)], tm, STONE, 2.5 * s, draw=False), ln([F(.465, .745), F(.565, .758)], tm, STONE, 2.5 * s, draw=False),
            ln([F(.53, .725), F(.62, .645), F(.665, .655)], tm, c, 15 * s, draw=False),                                 # raised thigh
            ln([F(.665, .655), F(.70, .755)], tm, c, 12 * s, draw=False), poly([F(.69, .745), F(.765, .762), F(.70, .775)], c, at=tm),
            ln([F(.54, .765), F(.645, .79), F(.745, .775)], tm, c, 12 * s, draw=False), poly([F(.74, .765), F(.80, .775), F(.745, .788)], c, at=tm),
            ln([F(.355, .625), F(.41, .565), F(.46, .545)], tm, c, 10 * s, curve=True, draw=False), dot(round(F(.47, .54)[0], 1), round(F(.47, .54)[1], 1), 8 * s, c, tm),
            ln([F(.375, .655), F(.45, .66), F(.49, .63)], tm, c, 9 * s, curve=True, draw=False), dot(round(F(.495, .625)[0], 1), round(F(.495, .625)[1], 1), 7 * s, c, tm)]
    king += [dot(round(F(.30 + .025 * k, .625 - .008 * (2 - abs(2 - k)))[0], 1), round(F(.30 + .025 * k, .625 - .008 * (2 - abs(2 - k)))[1], 1), 4.5 * s, STONE, tm)
             for k in range(5)]
    els += king
    if flames:
        for k, u in enumerate((.40, .50, .60)):
            fl = [F(u, .80), F(u - .03, .85), F(u + .02, .89), F(u - .02, .94)]
            els.append(ln(fl, round(T("flames") + .15 * k, 2), LILAC, 5 * s, "claimed", .5, curve=True))
    return els, (x0, y0, W, H), F


def rocket_over(F, at):
    """The claimed rocket, dotted, laid over the carving: a nose cone at the bird, a capsule round the king, fins at its sides, exhaust at the jaws."""
    body = [F(.5, -.01), F(.62, .08), F(.70, .22), F(.73, .74), F(.27, .74), F(.30, .22), F(.38, .08)]
    out = [poly(body, "rgba(201,193,238,.06)", LILAC, 5, at, curve=False, style="claimed"),
           poly([F(.30, .50), F(.13, .78), F(.29, .72)], "none", LILAC, 5, round(at + .4, 2), style="claimed"),
           poly([F(.70, .50), F(.87, .78), F(.71, .72)], "none", LILAC, 5, round(at + .4, 2), style="claimed"),
           poly(ellipse(F(.33, .58)[0], F(.33, .58)[1], 70, 60, 24)[:-1], "none", LILAC, 4, round(at + .7, 2), style="claimed")]
    for k, u in enumerate((.38, .46, .54, .62)):
        out.append(ln([F(u, .76), F(u + (u - .5) * .5, .93)], round(at + .9 + .1 * k, 2), LILAC, 5, "claimed", .4))
    return out


def relief(x0, y0, s, t=None, settled=False):
    """The Dendera relief (crypt south 1), schematic, in a 1000 x 500 box scaled by s: a long bulb-shaped envelope (the hn), a snake
    (Harsomtus) rising inside it, the lotus flower at its narrow end with its stem running out, a djed pillar with arms holding it up."""
    t = t or {}
    T = lambda k: -1 if settled else t.get(k, -1)
    P = lambda x, y: (x0 + x * s, y0 + y * s)
    c = "#ece2c8"
    els = [rect(x0, y0, 1000 * s, 500 * s, "#5d5649", "#a59a84", 2, 6, T("slab"))]
    # the envelope: narrow at the flower (x 130), widest near x 780, rounded end at x 930
    rr = lambda x: 18 + 135 * (max(0.0, min(1.0, (x - 130) / 650))) ** 1.25
    top = [P(x, 250 - rr(x)) for x in range(130, 801, 30)]
    end = [P(800 + 130 * math.sin(a), 250 - 153 * math.cos(a)) for a in [math.pi * k / 10 for k in range(1, 10)]]
    bot = [P(x, 250 + rr(x)) for x in range(800, 129, -30)]
    els.append(poly(top + end + bot, "rgba(236,226,200,.07)", c, 3.5 * s / .8, T("bulb"), fx="draw" if not settled else None, curve=True,
                    **({"dur": 1.2} if not settled else {})))
    # the snake: waves from the flower, a raised head near the wide end
    sn = [P(150 + 46 * k, 250 + 26 * math.sin(k * 1.25)) for k in range(14)] + [P(790, 205), P(812, 150), P(836, 140), P(850, 152)]
    els.append(ln(sn, T("snake"), c, 7 * s / .8, curve=True, dur=1.1 if not settled else None, draw=not settled))
    els.append(poly([P(836, 136), P(866, 150), P(840, 160)], c, at=T("snake")))
    # the lotus flower at the narrow end, opening to the right; its stem curls down and runs out at the left edge
    els += [poly([P(130, 250), P(78, 205), P(108, 250), P(78, 295)], c, at=T("flower")),
            poly([P(126, 250), P(96, 228), P(118, 250), P(96, 272)], "#5d5649", at=T("flower")),
            ln([P(80, 252), P(50, 300), P(46, 380), P(80, 440), P(150, 460), P(0, 470)], T("stem"), c, 5 * s / .8, curve=True, dur=.8 if not settled else None, draw=not settled)]
    # the djed pillar under the wide part, two arms reaching up to the envelope
    dx = 700
    djed = [rect(*P(dx - 22, 395), 44 * s, 105 * s, c, at=T("djed"))] + \
           [rect(*P(dx - 40, 360 + 11 * k), 80 * s, 6 * s, c, at=T("djed")) for k in range(4)] + \
           [ln([P(dx - 18, 372), P(dx - 60, 352), P(dx - 70, 300 + 50)], T("djed"), c, 6 * s / .8, curve=True, draw=False),
            ln([P(dx + 18, 372), P(dx + 60, 352), P(dx + 74, 350)], T("djed"), c, 6 * s / .8, curve=True, draw=False)]
    els += djed
    return els, P


def hbird(cx, cy, L, rot=0.0):
    """The Nazca hummingbird as one continuous line (plan), beak pointing left, L long (beak tip to tail): a long beak, a round head,
    two straight wings spread up and down ending in five feather fingers, a forked tail."""
    head = [(0, 0), (.30, -.01), (.31, -.035), (.34, -.052), (.375, -.047), (.395, -.03), (.415, -.032)]
    wing = [(.385, -.30), (.365, -.355), (.39, -.315), (.40, -.375), (.42, -.32), (.435, -.385), (.45, -.32), (.47, -.38), (.482, -.315), (.505, -.36), (.515, -.30), (.50, -.035)]
    body = [(.60, -.04), (.70, -.03)]
    tail = [(.98, -.10), (1.0, -.075), (.80, -.005), (1.0, .075), (.98, .10)]
    up = head + wing + body + tail
    down = [(u, -v) for u, v in reversed(head + wing + body)]
    pts = up + down
    ca, sa = math.cos(rot), math.sin(rot)
    return [(cx + (u - .5) * L * ca - v * L * sa, cy + (u - .5) * L * sa + v * L * ca) for u, v in pts]


def condor_pts(cx, cy, L):
    """A schematic Nazca-style condor in plan, L long: a small head and beak at the left, broad wings up and down ending in a fan of six
    feather fingers, a tapering body and a fanned tail."""
    head = [(0, 0), (.04, -.02), (.08, -.035), (.12, -.03), (.18, -.05)]
    wing = [(.17, -.17), (.15, -.27)]
    for k in range(6):
        u = .17 + .055 * k
        wing += [(u + .012, -.30 - .01 * (k % 2)), (u + .04, -.235)]
    wing += [(.50, -.16), (.47, -.06)]
    body = [(.62, -.055), (.74, -.05)]
    tail = [(.92, -.13), (.90, -.07), (.99, -.075), (.94, -.025), (1.0, 0)]
    up = head + wing + body + tail
    down = [(u, -v) for u, v in reversed(head + wing + body + tail[:-1])]
    pts = up + down
    return [(cx + (u - .5) * L, cy + v * L * .9) for u, v in pts]


def jar(cx, base, k, t=None, settled=False):
    """The 'Baghdad battery' in section, k units a centimetre: a clay jar 15 cm tall, a copper tube 9 cm tall and 2.6 cm across, an iron rod,
    a bitumen seal (schematic shapes, true to those sizes)."""
    t = t or {}
    T = lambda key: -1 if settled else t.get(key, -1)
    H = 15 * k
    prof = [(0, 0), (2.6, .2), (4.3, 1.4), (5.0, 4.0), (4.9, 8.0), (4.0, 11.0), (2.9, 12.6), (2.4, 13.6), (2.8, 14.4), (3.0, 15.0)]
    right = [(cx + r * k, base - y * k) for r, y in prof]
    left = [(cx - r * k, base - y * k) for r, y in reversed(prof)]
    els = [poly(right + left, "#b98a5a", "#e2c49a", 2.5, T("jar"), fx="draw" if not settled else None, curve=True, **({"dur": 1.0} if not settled else {})),
           poly([(cx + r * k * .82, base - y * k) for r, y in prof[1:-2]] + [(cx - r * k * .82, base - y * k) for r, y in reversed(prof[1:-2])], "#3a2a1e", at=T("jar"), curve=True)]
    tube = rect(cx - 1.3 * k, base - 12.6 * k, 2.6 * k, 9 * k, "#d07a3c", "#f0b080", 2, 3, T("tube"), fx="rise" if not settled else None)
    rod = rect(cx - .35 * k, base - 14.2 * k, .7 * k, 10.2 * k, "#7f8a94", "#c9d2d8", 1.5, 2, T("rod"), fx="rise" if not settled else None)
    seal = rect(cx - 2.5 * k, base - 13.9 * k, 5 * k, 1.4 * k, "#141110", "#5a5048", 1.5, 4, T("seal"), fx="pop" if not settled else None)
    return els + [tube, rod, seal], H


# ================================================================ timing: when each word is said (an estimate, from syllables)
TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)
    w = a.lower()
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def _spoken(seg):
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", TAGS.sub(" ", seg))
    return re.sub(r"@\w+!?", "", s.replace("^", "").replace("*", "")).split()


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Clock:
    """Estimated word times per beat. A shot's step starts at its [go:] marker (or at the beat's first word; at a chapter beat's
    second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said, from the start of shot i's step."""
    def __init__(self, beats):
        self.start, self.words = {}, {}
        for bi, b in enumerate(beats):
            t, ws, sents = 0.0, [], []
            for li, l in enumerate(b["lines"]):
                if li:
                    t += LGAP
                cuts = [0] + [m.start() for m in SENT.finditer(l) if m.start() > 0] + [len(l)]
                for a, z in zip(cuts, cuts[1:]):
                    seg = l[a:z]
                    p = re.search(r"\[p:([\d.]+)\]", seg)
                    r = RATE * (float(p.group(1)) if p else 1.0)
                    sents.append(t)
                    for m in GOM.finditer(seg):
                        self.start[int(m.group(1))] = (bi, t)
                    for w in _spoken(seg):
                        ws.append((_norm(w), t))
                        t += _syl(w) / r
                        if w[-1] in ",:;":
                            t += CGAP
                    t += SGAP
            frm = b["visual"]["from"]
            self.start.setdefault(frm, (bi, sents[1] if b.get("chapter") else 0.0))
            self.words[bi] = ws

    def at(self, i, phrase, lo=.4, d=0.0):
        bi, t0 = self.start[i]
        want = [_norm(x) for x in phrase.split()]
        ws = self.words[bi]
        for k in range(len(ws)):
            if ws[k][1] >= t0 - 1e-6 and [w for w, _ in ws[k:k + len(want)]] == want:
                return round(max(lo, ws[k][1] - t0 + d), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))


# ================================================================ the narration: script.json's lines, with [go:] markers added
def go_at(l, anchor, n, t=1.4):
    """Put [go:n|t] at the start of the sentence whose words begin with `anchor` (before its tags, after a [d:] mood tag)."""
    assert l.count(anchor) == 1, (anchor, l[:80])
    i = l.index(anchor)
    j = i
    while j > 0 and l[j - 1] == "]":
        j = l.rindex("[", 0, j - 1)
    if l.startswith("[d:", j):
        j = l.index("]", j) + 1
    return l[:j] + "[go:%d|%s]" % (n, t) + l[j:]


def lines_of(ci, bi, gos=()):
    out = list(SCRIPT["chapters"][ci]["beats"][bi]["lines"])
    for li, anchor, n, t in gos:
        l = out[li]
        if anchor is None:
            if l.startswith("[d:"):
                k = l.index("]") + 1
                out[li] = l[:k] + "[go:%d|%s]" % (n, t) + l[k:]
            else:
                out[li] = "[go:%d|%s]" % (n, t) + l
        else:
            out[li] = go_at(l, anchor, n, t)
    return out


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


def BEATS():
    C = [c["title"] for c in SCRIPT["chapters"]]
    return [
        B("hook", 0, lines_of(0, 0, [(1, None, 1, 1.4), (2, None, 2, 1.4)])),
        B("title", 3, lines_of(0, 1), intro=True),
        B("world", 4, lines_of(0, 2, [(1, None, 5, 1.4), (1, "By December", 6, 1.4), (2, None, 7, 1.4), (3, None, 8, .8), (3, "His clues are still", 9, 1.6)])),
        B("world", 10, lines_of(1, 0), chapter=C[1]),
        B("collision", 11, lines_of(1, 1, [(1, None, 12, 1.4)])),
        B("reversal", 13, lines_of(1, 2, [(1, None, 14, 1.4)])),
        B("cost", 15, lines_of(1, 3)),
        B("tag", 16, lines_of(1, 4)),
        B("world", 17, lines_of(2, 0), chapter=C[2]),
        B("collision", 18, lines_of(2, 1, [(1, None, 19, 1.4)])),
        B("reversal", 20, lines_of(2, 2, [(0, "The crypt was a", 21, 1.4), (1, None, 22, 1.4)])),
        B("world", 23, lines_of(2, 3, [(0, "In {1952", 24, 1.4), (0, "On its great stone lid", 25, 1.4)])),
        B("reversal", 26, lines_of(2, 4, [(1, None, 27, 1.4), (2, None, 28, 1.4)])),
        B("world", 29, lines_of(3, 0), chapter=C[3]),
        B("collision", 30, lines_of(3, 1)),
        B("cost", 31, lines_of(3, 2)),
        B("reversal", 32, lines_of(3, 3, [(0, "Plotting it took", 33, .8), (1, None, 34, 1.4), (1, "What the giant lines", 35, 1.4)])),
        B("world", 36, lines_of(4, 0), chapter=C[4]),
        B("collision", 37, lines_of(4, 1)),
        B("reversal", 38, lines_of(4, 2)),
        B("world", 39, lines_of(4, 3)),
        B("reversal", 40, lines_of(4, 4)),
        B("tag", 41, lines_of(4, 5)),
        B("weigh", 42, lines_of(5, 0, [(1, None, 43, 1.4)]), chapter=C[5]),
        B("reversal", 44, lines_of(5, 1, [(1, None, 45, .8)])),
        B("test", 46, lines_of(5, 2)),
        B("close", 47, lines_of(5, 3)),
    ]


ALIAS = {3: 2, 8: 7, 16: 12, 26: 25, 33: 32, 41: 39, 45: 44}
ALIAS_CAMS = {3: [1, 889, 500], 8: [1, 889, 500], 16: [1, 889, 500], 26: [1, 889, 500], 33: [1, 889, 500], 41: [1, 889, 500], 45: [1, 889, 500]}


# ================================================================ chapter 0 · opening: the lid, the exhibits, the question, the history
LID0 = (1180, 168, 622)               # the hook's lid: centre x, top, height (622 units = 3.7 m: 168 units a metre)


def s01(C):
    """s1 · a dark tomb: Pakal's lid (3.7 m) beside a 1.7 m person; the carving builds as named; dotted 'flames' under the king."""
    cx, top, H = LID0
    tt = {"slab": .4, "border": 1.0, "man": C.at(0, "a man leans"), "tree": C.at(0, "strange"), "bird": C.at(0, "machinery", d=.6),
          "jaws": C.at(0, "flames"), "flames": C.at(0, "flames", d=.3)}
    els, (x0, y0, W, Hh), F = lid(cx, top, H, tt, flames=True)
    vault = [(80, 800), (80, 420), (300, 200), (560, 120), (1720, 120), (1720, 800)]
    m = H / 3.7
    return {"base": "dark", "cam": CAM, "els": [
        poly(vault, "#1d1712", "rgba(255,226,190,.12)", 2, -1),
        poly([(80, 800), (1720, 800), (1720, 830), (80, 830)], "#2a221b", at=-1),
        glow(420, 300, 420, .2, .55, "lamp"), glow(cx, 480, 520, .6, .25, "lamp")] + els + [
        dimline(round(x0 - 40, 1), round(y0, 1), round(x0 - 40, 1), round(y0 + Hh, 1), "over 3.5 m", C.at(0, "metres long", d=-.4), GOLD, lx=-26),
        person(round(x0 + W + 150, 1), round(y0 + Hh, 1), round(1.7 * m, 1), C.at(0, "metres long", d=.2), "#d9c7a6"),
        lab(round(x0 + W + 150, 1), round(y0 + Hh + 0, 1) - 1.7 * m - 22, "1.7 m", C.at(0, "metres long", d=.5), DIM, 24)]}


def s02(C):
    """s2 · three framed exhibits pop in as named: the Round Head (Sahara), the bulb relief (Egypt), the hummingbird (Peru)."""
    t1, t2, t3 = C.at(1, "In the Sahara", lo=.5), C.at(1, "In Egypt"), C.at(1, "In Peru")
    fw, fh, fy = 430, 470, 170
    xs = [130, 674, 1218]
    els = [rect(80, 140, 1620, 600, "rgba(255,236,206,.03)", at=-1)]
    # 1 · the Round Head on rock
    x = xs[0]
    els += [rect(x, fy, fw, fh, ROCK, "#d8c7ae", 3, 8, t1, fx="pop")] + roundhead(x + fw / 2, fy + fh - 30, 400, at=round(t1 + .2, 2)) + \
           [lab(x + fw / 2, fy + fh + 50, "Sahara", round(t1 + .3, 2), GOLD, 30)]
    # 2 · the bulb relief, scaled into its frame
    x = xs[1]
    rel, _ = relief(x + 15, fy + 120, .4, settled=True)
    for e in rel:
        e["in"] = round(t2 + .2, 2)
    els += [rect(x, fy, fw, fh, "#4a443b", "#d8c7ae", 3, 8, t2, fx="pop")] + rel + [lab(x + fw / 2, fy + fh + 50, "Egypt", round(t2 + .3, 2), GOLD, 30)]
    # 3 · the hummingbird from above, a speck of a person at its tail
    x = xs[2]
    hb = hbird(x + fw / 2, fy + fh / 2, 360)
    els += [rect(x, fy, fw, fh, "#a77f55", "#d8c7ae", 3, 8, t3, fx="pop"),
            ln(hb + [hb[0]], round(t3 + .2, 2), "#f4e6c8", 4, dur=1.4),
            person(x + fw / 2 + 200, fy + fh / 2 + 30, 7, round(t3 + 1.2, 2), "#2a2018"),
            lab(x + fw / 2, fy + fh + 50, "Peru", round(t3 + .3, 2), GOLD, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s03(C):
    """s3 · night over a desert horizon, a Maya temple and an Egyptian pylon in silhouette; a dotted saucer glides down; a question."""
    g = 640
    maya = [(220, g), (220, g - 40), (250, g - 40), (250, g - 80), (280, g - 80), (280, g - 120), (310, g - 120), (310, g - 160), (340, g - 160), (340, g - 200),
            (360, g - 200), (360, g - 250), (440, g - 250), (440, g - 200), (460, g - 200), (460, g - 160), (490, g - 160), (490, g - 120), (520, g - 120),
            (520, g - 80), (550, g - 80), (550, g - 40), (580, g - 40), (580, g)]
    pylon = [(1250, g), (1272, g - 210), (1380, g - 210), (1392, g - 150), (1470, g - 150), (1482, g - 210), (1590, g - 210), (1612, g)]
    t = C.at(2, "space", lo=.3)
    return {"base": "sky", "tod": "night", "ground": g, "sun": False, "moon": [1530, 210, 24], "cam": CAM, "els": [
        poly(maya, "#15110f", "rgba(255,226,190,.25)", 1.5, -1), poly(pylon, "#15110f", "rgba(255,226,190,.25)", 1.5, -1),
        glow(889, 300, 300, .3, .35, "scan")] + ufo(889, 290, .3, 1.4) + [
        ln([(830, 315), (430, 400)], .8, LILAC, 2, "claimed", .6), ln([(950, 315), (1420, 430)], .9, LILAC, 2, "claimed", .6),
        glow(889, 520, 140, t, .5, "lamp"), lab(889, 560, "?", t, LILAC, 110, st="big", fx="pop", dur=.8)]}


def s05(C):
    """s5 · a hotel office at night in the Alps (a window on snowy peaks), a typewriter, a lamp; a book rises, 'Memories of the Future',
    1968; then sixty little blocks of a hundred copies each: the first printing, 6,000."""
    t68, thot, tpub, tmem, tcop = C.at(4, "In nineteen"), C.at(4, "hotel manager"), C.at(4, "published"), C.at(4, "Memories"), C.at(4, "The first printing")
    win = [rect(150, 170, 420, 300, "#1f2a3a", "#cbbca8", 3, 6, -1)]
    peaks = poly([(152, 468), (210, 330), (260, 380), (330, 250), (400, 360), (450, 300), (568, 468)], "#3a4458", "rgba(255,255,255,.3)", 1.5, -1)
    snow = [poly([(310, 280), (330, 250), (352, 285), (338, 278), (326, 290)], "#eef2f6", at=-1), poly([(438, 315), (450, 300), (464, 320), (452, 316)], "#eef2f6", at=-1)]
    desk = [rect(110, 600, 760, 30, "#5a3e28", "#8a6a48", 2, 4, -1), rect(150, 630, 26, 160, "#4a3220", at=-1), rect(800, 630, 26, 160, "#4a3220", at=-1)]
    typ = [rect(250, 540, 220, 60, "#2c2a28", "#8a8a86", 2, 8, .5), rect(280, 500, 160, 46, "#efe6d2", "#cbbca8", 1, 2, .7),
           ln([(290, 515), (430, 515)], .9, "#7a6a58", 2, draw=False), ln([(290, 527), (400, 527)], 1.0, "#7a6a58", 2, draw=False)]
    lamp = [ln([(700, 600), (700, 470), (650, 440)], .3, "#cbbca8", 4, draw=False), poly([(610, 420), (690, 420), (670, 460), (630, 460)], "#c9a050", at=.3),
            glow(650, 480, 260, .4, .7, "lamp")]
    els = [stars(40, 160, 560, 175, 300)] + win + [peaks] + snow + desk + typ + lamp + [
        lab(360, 160, "1968", t68, GOLD, 36, st="serif"), lab(360, 680, "a hotel in the Alps", thot, DIM, 26)]
    bx, by = 960, 230
    els += book(bx, by, 260, 360, tpub, "#7a3424", "#e0a070", fx="rise") + [
        lab(bx + 140, by + 120, "Memories", tmem, "#f5e6c8", 30, st="serif"), lab(bx + 140, by + 160, "of the Future", tmem, "#f5e6c8", 30, st="serif"),
        lab(bx + 140, by + 300, "1968", tmem, GOLD, 26)]
    for k in range(60):
        x = 1290 + 34 * (k % 10)
        y = 270 + 46 * (k // 10)
        els += [rect(x, y, 26, 36, "#a0503a", "#e0a070", 1.2, 3, round(tcop + .5 + .025 * k, 2), fx="pop")]
    els += [lab(1450, 590, "6,000 copies", tcop + 1.0, GOLD, 32), lab(1450, 632, "each block: 100", tcop + 1.4, DIM, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s06(C):
    """s6 · the claim, dotted: a saucer over an ancient building site; 'taught?' to the people, 'traces?' on a carving and a pyramid."""
    g = 680
    tvis, ttau, ttra = C.at(5, "visitors from space"), C.at(5, "taught"), C.at(5, "traces")
    crew = [person(520 + 46 * k, g, 84, round(.4 + .1 * k, 2), "#e8d6b8") for k in range(4)]
    els = [{"k": "pyramid", "x": 1260, "y": g, "w": 520, "in": -1, "op": .95},
           rect(260, g - 70, 150, 70, "#cdb58a", "#8a6a48", 2, 3, .3), ln([(410, g - 40), (520, g - 60)], .5, "#c9a370", 3, draw=False)] + crew + [
        rect(820, g - 210, 120, 210, "#8f8470", STONE_E, 2, 4, .6), ln([(850, g - 170), (910, g - 170)], .8, CARVE, 4, draw=False),
        {"k": "circle", "x": 880, "y": g - 120, "r": 26, "fill": "none", "c": CARVE, "w": 4, "in": .8}]
    els += ufo(700, 250, tvis, 1.3) + [glow(700, 250, 160, tvis, .35, "scan"),
                                        arrow([[640, 290], [600, g - 120]], ttau, LILAC, 3, "claimed", .7, False), lab(560, 380, "taught?", ttau + .3, LILAC, 30, "end")]
    for k, (x, y) in enumerate([(880, g - 230), (1200, g - 330), (1290, g - 250), (1150, g - 180)]):
        els += [dot(x, y, 7, LILAC, round(ttra + .15 * k, 2)), ring(x, y, 18, round(ttra + .15 * k, 2), LILAC, 2, "claimed", .4)]
    els += [lab(1340, 340, "traces?", ttra + .6, LILAC, 30, "start")]
    return {"base": "sky", "tod": "dusk", "ground": g, "sun": [300, 560, 26], "cam": CAM, "els": els}


def s07(C):
    """s7 · a stack of books grows ('a bestseller', December 1968); the Moon with Apollo 8's dotted orbit and the Earth rising;
    a long dotted arrow from a far star towards the Earth."""
    tb, tap, tmoon, tq = C.at(6, "bestseller", lo=.5), C.at(6, "Apollo"), C.at(6, "around the Moon"), C.at(6, "visited ours")
    els = []
    for k in range(9):
        els += book(180 + (k % 2) * 14, 700 - 44 * (k + 1), 230, 40, round(tb + .1 * k, 2), ["#7a3424", "#6a3a2a", "#8a4430"][k % 3], "#e0a070", fx="pop", spine=False)
    els += [lab(305, 260, "a bestseller", tb + 1.0, GOLD, 32), lab(305, 220, "December 1968", tb + 1.2, DIM, 26)]
    mx, my, mr = 1030, 470, 200
    els += [{"k": "circle", "x": mx, "y": my, "r": mr, "fill": "#9a968e", "c": "#dcd6ca", "w": 2, "in": tap, "fx": "pop"},
            glow(mx, my, 330, tap, .25, "lamp")]
    for (dx, dy, r) in [(-60, -50, 34), (50, 30, 22), (-20, 90, 28), (90, -80, 18), (-110, 40, 16)]:
        els.append({"k": "circle", "x": mx + dx, "y": my + dy, "r": r, "fill": "#85817a", "c": "none", "w": 0, "in": tap})
    orbit = ellipse(mx, my, mr + 70, 70, 60)
    te = round(tmoon + .4, 2)
    els += [ln(orbit, tmoon, BONE, 2.5, "inferred", 1.6, curve=True), dot(mx - mr - 70, my, 8, "#f5f0e6", round(tmoon + 1.5, 2)),
            {"k": "circle", "x": 1490, "y": 250, "r": 66, "fill": "#2f6f9f", "c": "#cfe6ff", "w": 2, "in": te, "fx": "pop"},
            poly([(1446, 214), (1470, 200), (1492, 210), (1488, 236), (1500, 262), (1478, 290), (1462, 270), (1452, 240)], "#8a9a5a", at=te, curve=True),
            poly([(1506, 206), (1532, 214), (1540, 240), (1522, 250), (1510, 232)], "#8a9a5a", at=te, curve=True),
            poly(ellipse(1490, 196, 40, 9, 16)[:-1], "#f2f6fa", at=te, op=.8),
            lab(1490, 352, "Earth", round(te + .3, 2), "#cfe6ff", 26), lab(1030, 760, "Apollo 8", tap + .3, BONE, 32)]
    els += [glow(620, 160, 60, tq, .8, "scan"), dot(620, 160, 6, "#ffffff", tq),
            arrow([[640, 170], [1100, 140], [1410, 215]], round(tq + .2, 2), LILAC, 3, "claimed", 1.2), lab(1130, 195, "someone else?", round(tq + .9, 2), LILAC, 28)]
    return {"base": "dark", "stars": 110, "cam": CAM, "els": els}


TL_X = lambda y: round(170 + (y - 1966) / 62 * 1440, 1)       # the media timeline: 1966 at x 170, 2028 at x 1610


def s08(C):
    """s8 · the media timeline from 1968 to 2026, callouts to their years: the German book, the English edition, the film's Oscar
    nomination, Rod Serling's special, Leonard Nimoy's series, Ancient Aliens and its twenty-two seasons."""
    Y = 640
    ten, tfilm, ttv, tnim, taa = C.at(7, "In English"), C.at(7, "A film"), C.at(7, "American television"), C.at(7, "Leonard"), C.at(7, "Today")
    ticks = [[TL_X(y), str(y)] for y in (1970, 1980, 1990, 2000, 2010, 2020)]
    els = [{"k": "axis", "x0": 170, "x1": 1610, "y": Y, "ticks": ticks, "in": .2}]
    calls = [(1968, 190, .5, "1968", ["the book"]), (1969, 420, ten, "1969", ["Chariots", "of the Gods?"]), (1970, 650, tfilm, "1970", ["Oscar", "nomination"]),
             (1973, 880, ttv, "1973", ["Rod Serling"]), (1977, 1110, tnim, "1977", ["Leonard", "Nimoy"])]
    for yr, x, at, ytxt, txt in calls:
        at = round(at, 2)
        els += [ln([(TL_X(yr), Y - 8), (x, 560)], at, DIM, 1.6, "inferred", .5), dot(TL_X(yr), Y, 6, GOLD, at)]
        if yr in (1968, 1969):
            els += book(x - 40, 330, 80, 110, round(at + .2, 2), "#7a3424" if yr == 1968 else "#2f4a6a", "#e0a070")
        elif yr == 1970:
            els += reel(x, 385, 55, round(at + .2, 2))
        else:
            els += tv(x - 60, 340, 120, round(at + .2, 2))
        els += [lab(x, 300, ytxt, round(at + .3, 2), GOLD, 26)] + [lab(x, 498 + 30 * j, t, round(at + .4, 2), BONE, 26) for j, t in enumerate(txt)]
    x = TL_X(2009)
    els += [ln([(x, Y - 8), (1360, 560)], taa, DIM, 1.6, "inferred", .5), dot(x, Y, 6, GOLD, taa)] + tv(1300, 340, 120, round(taa + .2, 2)) + \
           [lab(1360, 300, "2009", round(taa + .3, 2), GOLD, 26), lab(1360, 498, "Ancient Aliens", round(taa + .4, 2), BONE, 26)]
    for k in range(22):
        xx = 1470 + 17 * (k % 11)
        yy = 350 + 40 * (k // 11)
        els.append(rect(xx, yy, 9, 28, BLUE, r=3, at=round(taa + 1.0 + .06 * k, 2), fx="pop"))
    els += [lab(1560, 460, "22 seasons", round(taa + 2.4, 2), BLUE, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s09_late(C):
    """s9 · on the timeline: sixty little books, one a million copies; a quiet tick at 2026."""
    tc, td = C.at(8, "sold"), C.at(8, "He died")
    els = []
    for k in range(60):
        x = 300 + 36 * (k % 30)
        y = 160 + 52 * (k // 30)
        els += [rect(x, y, 26, 38, "#a0503a", "#e0a070", 1.2, 3, round(tc + .03 * k, 2), fx="pop")]
    els += [lab(1420, 210, "60 million+", tc + 1.4, GOLD, 32, "start"), lab(1420, 248, "copies", tc + 1.4, GOLD, 26, "start"),
            ln([(TL_X(2026), 600), (TL_X(2026), 680)], td, BONE, 2.5, dur=.4), lab(TL_X(2026), 740, "1935 to 2026", td + .3, DIM, 26, "end")]
    return els


def s10(C):
    """s10 · the world: six pins in the film's order."""
    v = View(-115, 65, -38, 40, (90, 125, 1600, 650))
    tc = C.at(9, "His clues", lo=.4)
    pins = [("Tassili", 9.5, 25.0, -18, -22, "end"), ("Dendera", 32.67, 26.14, -16, 36, "end"), ("Palenque", -92.05, 17.48, -18, -24, "end"),
            ("Nazca", -75.13, -14.74, 22, 8, "start"), ("Klerksdorp", 26.0, -26.8, 22, 8, "start"), ("near Baghdad", 44.4, 33.3, 22, -14, "start")]
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for k, (name, lo, la, lx, ly, a) in enumerate(pins):
        x, y = v.p(lo, la)
        at = round(tc + .45 * k, 2)
        els.append({"k": "pin", "x": x, "y": y, "t": name, "c": GOLD, "lx": lx, "ly": ly, "a": a, "in": at})
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================ chapter 1 · Tassili
def s11(C):
    """s11 · the central Sahara in a map window: the plateau near Djanet with its shelters; at the right a rock wall where 150 marks pop
    (each mark a hundred images: more than 15,000)."""
    v = View(-6, 26, 16, 38, (90, 130, 760, 640))
    plat = [v.p(a, b) for a, b in [(5.8, 26.9), (7.5, 26.9), (9.5, 25.8), (11.2, 24.6), (11.0, 23.8), (9.6, 24.2), (7.8, 25.2), (6.0, 26.0)]]
    tpl, tsh, tim = C.at(10, "sandstone plateau"), C.at(10, "shelters"), C.at(10, "fifteen thousand")
    r = random.Random(21)
    marks = []
    for k in range(26):
        f = r.random() * .8
        marks.append(v.p(6.3 + 4.2 * f, 26.4 - 2.0 * f + (r.random() - .5) * .9))
    ax, ay = v.p(2.5, 28.5)
    dj = v.p(9.485, 24.555)
    win = [100, 140, 740, 620]
    els = [{"k": "group", "clip": win + [16], "bg": "#1d3a4a", "in": -1, "els": [{"k": "map", "land": v.land()}]},
           rect(*win, "none", "rgba(255,236,206,.35)", 2, 16, -1),
           lab(ax, ay, "Algeria", .5, DIM, 28, st="ital"), lab(v.p(13, 34.6)[0], v.p(13, 34.6)[1], "Mediterranean", .5, "#9fc4dc", 24, st="ital"),
           poly(plat, "rgba(176,100,60,.35)", "#e8a070", 2.5, tpl, fx="draw", curve=True, dur=1.2),
           lab(plat[2][0] + 20, plat[2][1] - 40, "Tassili n'Ajjer", round(tpl + .6, 2), GOLD, 30, "start"),
           {"k": "pin", "x": dj[0], "y": dj[1], "t": "Djanet", "c": BLUE, "lx": -18, "ly": 30, "a": "end", "in": round(tpl + .9, 2), "r": 6}]
    els += [dot(x, y, 4, "#ffb27a", round(tsh + .04 * k, 2)) for k, (x, y) in enumerate(marks)]
    els += [rect(930, 150, 720, 520, ROCK, ROCK_E, 2, 14, round(tim - .5, 2))]
    rr = random.Random(9)
    for k in range(150):
        x = round(970 + (k % 15) * 46 + rr.random() * 12, 1)
        y = round(190 + (k // 15) * 47 + rr.random() * 10, 1)
        at = round(tim + .02 * k, 2)
        if k % 3 == 0:
            els.append(person(x, y + 18, 26, at, "#e0a070"))
        elif k % 3 == 1:
            els.append(dot(x, y + 6, 6, "#f0d8b0", at))
        else:
            els.append(poly([(x - 12, y + 8), (x + 10, y + 6), (x + 14, y - 2), (x + 6, y + 14), (x - 10, y + 14)], "#d8b090", at=at, fx="pop"))
    els += [lab(1290, 720, "15,000+ images", round(tim + 2.0, 2), GOLD, 34), lab(1290, 760, "each mark: 100", round(tim + 2.3, 2), DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


GIANT = (620, 760, 520)               # the shelter's Round Head: x, feet, height (about three times the 1.7 m copyist: about 5 m)


def s12(C):
    """s12 · inside a shelter, 1956: a Round Head giant about three people tall over a copyist with a drawing board; an eye, a nose
    and a mouth sketched on its blank head are struck out one by one; the nickname in lilac."""
    gx, gb, gh = GIANT
    tgi, tno, tmar = C.at(11, "painted giant"), C.at(11, "no eyes"), C.at(11, "Lhote nicknamed")
    hx, hy, hr = head_of(gx, gb, gh)
    over = [(-40, 140), (300, 120), (900, 135), (1300, 150), (1800, 120), (1800, -40), (-40, -40)]
    wall = [(80, 800), (80, 300), (200, 190), (1100, 170), (1500, 230), (1700, 300), (1700, 800)]
    els = [poly(wall, ROCK, "rgba(255,226,190,.2)", 2, -1), poly(over, "#2a1f18", at=-1),
           poly([(-40, 800), (1800, 800), (1800, 1040), (-40, 1040)], "#3a2c22", at=-1)]
    els += roundhead(gx, gb, gh, at=round(tgi, 2)) + [glow(gx, hy, 260, tgi, .3, "lamp")]
    els += [person(1150, 790, 170, .5, "#1a1511"), person(1290, 790, 160, .8, "#1a1511"),
            rect(1172, 680, 70, 52, "#efe6d2", "#8a7a66", 1.5, 3, .7), lab(1220, 520, "1956", .9, GOLD, 34),
            lab(1220, 565, "the copyists", 1.2, DIM, 26)]
    feats = [poly(ellipse(hx - hr * .38, hy - hr * .15, hr * .2, hr * .1, 16)[:-1], "none", BONE, 3, tno, style="inferred"),
             poly(ellipse(hx + hr * .38, hy - hr * .15, hr * .2, hr * .1, 16)[:-1], "none", BONE, 3, tno, style="inferred"),
             ln([(hx, hy - hr * .05), (hx - hr * .08, hy + hr * .25), (hx + hr * .06, hy + hr * .27)], round(tno + .5, 2), BONE, 3, "inferred", .3),
             ln([(hx - hr * .3, hy + hr * .5), (hx, hy + hr * .58), (hx + hr * .3, hy + hr * .5)], round(tno + 1.0, 2), BONE, 3, "inferred", .3, curve=True)]
    els += feats + [strike(hx - hr * .65, hy - hr * .02, hx - hr * .1, hy - hr * .3, round(tno + .4, 2)), strike(hx + hr * .1, hy - hr * .02, hx + hr * .65, hy - hr * .3, round(tno + .5, 2)),
                    strike(hx - hr * .2, hy + hr * .32, hx + hr * .2, hy + hr * .15, round(tno + .9, 2)), strike(hx - hr * .4, hy + hr * .66, hx + hr * .4, hy + hr * .44, round(tno + 1.4, 2))]
    els += [lab(gx + 330, 300, "\"the great", tmar + .3, LILAC, 40, "start", st="ital"), lab(gx + 330, 350, "Martian god\"", tmar + .3, LILAC, 40, "start", st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


HEAD2 = (560, 450, 190)               # the close-up head: centre, radius


def s13(C):
    """s13 · close on the round head: 'half in jest?'; a book with a dotted saucer (others took him literally); later art at the
    right (cattle and people, another style); a dotted helmet and antenna drawn onto the head, 1968."""
    cx, cy, r = HEAD2
    tj, tlit, tlat, thel = C.at(12, "Half in jest"), C.at(12, "took him"), C.at(12, "unlike the art"), C.at(12, "books saw")
    els = [flat(), rect(80, 130, 960, 680, ROCK, ROCK_E, 2, 18, -1),
           poly([(cx - r * .55, cy + r * .8), (cx + r * .55, cy + r * .8), (cx + r * 1.15, cy + r * 1.9), (cx - r * 1.15, cy + r * 1.9)], OCHRE, "#d8c7ae", 1.5, -1),
           {"k": "circle", "x": cx, "y": cy, "r": r, "fill": OCHRE, "c": "#d8c7ae", "w": 2, "in": -1},
           ln([(cx - r * .9, cy + r * 1.1), (cx - r * 1.6, cy + r * .2), (cx - r * 1.7, cy - r * .5)], -1, OCHRE, 26, curve=True, draw=False),
           glow(cx, cy, 300, .3, .25, "lamp"),
           lab(cx + r + 40, cy - r - 30, "half in jest?", tj, DIM, 28, "start", st="ital")]
    els += book(1170, 170, 200, 150, tlit, "#2f4a6a", "#cfe6ff", fx="pop") + ufo(1280, 250, round(tlit + .3, 2), .55) + \
           [lab(1270, 360, "taken literally", round(tlit + .5, 2), LILAC, 26)]
    els += [rect(1100, 430, 560, 330, "#8a6650", ROCK_E, 2, 14, tlat)] + cow(1260, 690, .9, round(tlat + .3, 2), "#efe6d2") + cow(1480, 700, .7, round(tlat + .45, 2), "#e8dcc2", flip=True) + \
           [person(1380, 700, 110, round(tlat + .6, 2), "#efe6d2"), person(1560, 690, 96, round(tlat + .7, 2), "#efe6d2"), lab(1380, 470, "later art", round(tlat + .5, 2), BONE, 30)]
    vis = [(cx - r * 1.12, cy - r * .1), (cx - r * 1.12, cy - r * 1.2), (cx, cy - r * 1.45), (cx + r * 1.12, cy - r * 1.2), (cx + r * 1.12, cy - r * .1)]
    els += [poly(ellipse(cx, cy - r * .1, r * 1.18, r * 1.25, 40)[:-1], "none", LILAC, 4, thel, style="claimed"),
            poly([(cx - r * .7, cy - r * .3), (cx + r * .7, cy - r * .3), (cx + r * .6, cy + r * .25), (cx - r * .6, cy + r * .25)], "rgba(201,193,238,.08)", LILAC, 3,
                 round(thel + .3, 2), style="claimed"),
            ln([(cx + r * .5, cy - r * 1.2), (cx + r * .8, cy - r * 1.75)], round(thel + .5, 2), LILAC, 3, "claimed", .4), dot(round(cx + r * .8, 1), round(cy - r * 1.78, 1), 9, LILAC, round(thel + .8, 2)),
            lab(cx - r - 60, cy - r - 40, "1968", round(thel + .4, 2), LILAC, 34, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def s14(C):
    """s14 · dating: a Round Head with a later cow painted over its legs; two posters, one pasted over the other; a time axis from 12,000
    years ago to today with the Round Heads' band from 9,500 to 7,500 years ago, and the green Sahara (grass, a lake) above it."""
    tlay, tover, tpos, tband, tgreen = C.at(13, "from the layers"), C.at(13, "painted over which"), C.at(13, "like posters"), C.at(13, "nine and a half"), C.at(13, "green")
    els = [rect(110, 140, 600, 420, ROCK, ROCK_E, 2, 12, .2)] + roundhead(330, 520, 320, fill="#8a4a30", at=.4) + \
          [ln([(110, 580), (710, 580)], tlay, "#8a6a48", 3, dur=.6), ln([(110, 600), (710, 600)], round(tlay + .2, 2), "#6f5a44", 3, dur=.6),
           lab(410, 640, "layers", round(tlay + .3, 2), DIM, 24)] + \
          cow(470, 520, 1.0, tover, "#efe6d2") + [lab(560, 190, "painted over", round(tover + .4, 2), BONE, 28)]
    els += [rect(840, 200, 230, 300, "#4f7f96", "#cfe6ff", 2, 4, tpos, fx="pop"), ln([(870, 260), (1040, 260)], tpos, "#cfe6ff", 3, draw=False),
            rect(930, 260, 230, 300, "#c96f3c", "#ffd0a0", 2, 4, round(tpos + .6, 2), fx="pop"), ln([(960, 330), (1130, 330)], round(tpos + .6, 2), "#ffd0a0", 3, draw=False),
            lab(1000, 600, "newer on top", round(tpos + 1.0, 2), DIM, 26)]
    A = lambda ya: round(220 + 1360 * (12000 - ya) / 12000, 1)
    els += [{"k": "axis", "x0": 220, "x1": 1580, "y": 740, "ticks": [[A(12000), "12,000"], [A(9000), "9,000"], [A(6000), "6,000"], [A(3000), "3,000"], [A(0), "today"]], "in": round(tband - 1.6, 2)},
            rect(A(9500), 712, A(7500) - A(9500), 22, OCHRE, r=11, at=tband, fx="pop"),
            lab((A(9500) + A(7500)) / 2, 696, "Round Heads", round(tband + .4, 2), "#e8a070", 26),
            lab(1580, 690, "years ago", round(tband - 1.2, 2), DIM, 24, "end")]
    gx0, gx1 = 1240, 1640
    els += [poly(ellipse(1440, 470, 150, 34, 30)[:-1], "#4f7f96", "#9fd0ff", 1.5, tgreen, curve=True)] + \
           [ln([(x, 560), (x + 6, 532)], round(tgreen + .02 * k, 2), "#8fbf5a", 3, draw=False) for k, x in enumerate(range(gx0, gx1, 22))] + \
           [lab(1440, 390, "a green Sahara", round(tgreen + .3, 2), "#a9d47c", 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s15(C):
    """s15 · what the blank heads may be: a mask, body paint, a spirit being; then a person by a fire: a living tradition."""
    tm, tb, ts, tt = C.at(14, "masks"), C.at(14, "body paint"), C.at(14, "spirit"), C.at(14, "Tuareg")
    B_ = 700
    els = [rect(90, 150, 1150, 610, ROCK, ROCK_E, 2, 16, .2)]
    els += roundhead(300, B_, 360, at=.5)
    hx, hy, hr = head_of(300, B_, 360)
    els += [poly(ellipse(hx, hy + 4, hr * .78, hr * .95, 20)[:-1], "#e8dcc2", "none", 0, tm, fx="pop"), dot(hx - hr * .3, hy - 2, 5, "#2a2018", tm), dot(hx + hr * .3, hy - 2, 5, "#2a2018", tm),
            lab(300, 750, "masks", round(tm + .2, 2), BONE, 28)]
    els += roundhead(660, B_, 360, at=.7) + [ln([(630 + 15 * j, 520), (630 + 15 * j, 640)], round(tb + .1 * j, 2), "#f5ecdc", 5, draw=False) for j in range(5)] + \
           [lab(660, 750, "body paint", round(tb + .2, 2), BONE, 28)]
    els += roundhead(1010, B_, 360, fill="#e8c8a0", op=.5, at=.9) + [glow(1010, 520, 200, ts, .7, "lamp"), lab(1010, 750, "spirit beings", round(ts + .2, 2), BONE, 28)]
    els += [glow(1450, 640, 160, tt, .8, "fire"), poly([(1420, 690), (1450, 640), (1480, 690)], "#ffb060", at=tt), person(1530, 700, 150, round(tt + .2, 2), "#e8d6b8"),
            lab(1480, 760, "a living tradition", round(tt + .5, 2), GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s16(C):
    """s16 · the copies: water drops and a sponge on a painted figure; it flares bright, then fades below its first strength; a bold
    paper copy, one of its figures boxed in red dashes with a question mark: 'said to be faked'."""
    tw, tbr, tfad, tfake = C.at(15, "wetted"), C.at(15, "brighter"), C.at(15, "faded"), C.at(15, "later said")
    els = [flat(), rect(100, 150, 780, 620, ROCK, ROCK_E, 2, 14, -1)] + roundhead(450, 730, 470, fill="#9a5434", at=-1)
    els += [dot(x, y, 9, "#9fd0ff", round(tw + .07 * k, 2), op=.85) for k, (x, y) in enumerate(scatter(16, 260, 640, 260, 640, 4))]
    els += [rect(520, 440, 130, 70, "#e8d070", "#b8a040", 2, 22, round(tw + 1.2, 2), fx="pop"), arrow([[580, 420], [470, 330], [360, 400], [280, 330]], round(tw + 1.5, 2), "#e8d070", 3, dur=1.0)]
    els += roundhead(450, 730, 470, fill="#e2763c", c="#ffd0a0", at=tbr) + [glow(450, 420, 300, tbr, .5, "lamp")]
    veil = rect(104, 154, 772, 612, ROCK, at=tfad, op=.8)
    veil["dur"] = 1.6
    els += [veil]
    els += [lab(250, 200, "brighter", tbr + .2, "#ffd0a0", 28), lab(720, 200, "then faded", tfad + .6, DIM, 28)]
    els += [rect(1020, 170, 520, 580, "#efe3c8", "#8a7a66", 2, 6, tw + .6, fx="pop")] + roundhead(1200, 690, 420, fill="#d0602c", c="#d0602c", at=round(tw + .9, 2)) + \
           roundhead(1420, 690, 260, fill="#d0602c", c="#d0602c", at=round(tw + 1.1, 2)) + \
           [rect(1340, 400, 160, 310, "none", RED, 3, 6, tfake, style="inferred"), lab(1420, 380, "?", round(tfake + .2, 2), RED, 50, st="big", fx="pop"),
            lab(1280, 790, "said to be faked", round(tfake + .4, 2), RED, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s17_late(C):
    """s17 · back on the round head: the dotted helmet struck through, a warm glow on the painting, 'a painting style'."""
    cx, cy, r = HEAD2
    tst = C.at(16, "painting style")
    return [strike(cx - r * 1.3, cy + r * .9, cx + r * 1.3, cy - r * 1.7, tst, RED, 7), glow(cx, cy, 340, round(tst + .4, 2), .5, "lamp"),
            lab(cx, cy + r + 150, "a painting style", round(tst + .3, 2), GOLD, 34)]


# ================================================================ chapter 2 · Dendera and Palenque
def s18(C):
    """s18 · dusk at Dendera: the temple front (a cavetto cornice with a winged sun disc, six columns with square capitals, screen walls), palms;
    'Temple of Hathor, Dendera', 'begun about 54 BCE'."""
    g = 700
    tbe = C.at(17, "begun")
    els = [rect(330, 300, 1120, 400, "#c9ad85", "#f2dcb4", 2, 0, .3),
           poly([(318, 300), (1462, 300), (1490, 238), (290, 238)], "#d8bd93", "#f2dcb4", 2, .3),
           rect(312, 292, 1156, 14, "#b9a07a", at=.3)]
    els += [{"k": "circle", "x": 889, "y": 266, "r": 15, "fill": "#e8c35a", "c": "#fff0c0", "w": 1.5, "in": .6},
            poly([(872, 266), (800, 252), (760, 262), (806, 270), (872, 274)], "#c9a050", at=.6), poly([(906, 266), (978, 252), (1018, 262), (972, 270), (906, 274)], "#c9a050", at=.6)]
    for k in range(6):
        x = 400 + k * 190
        els += [rect(x, 370, 90, 330, "#d9c29a", "#8a6a48", 1.5, 0, round(.5 + .1 * k, 2)), rect(x - 12, 318, 114, 56, "#e2cfa8", "#8a6a48", 1.5, 4, round(.5 + .1 * k, 2)),
                ln([(x + 10, 334), (x + 80, 334)], round(.5 + .1 * k, 2), "#a88b66", 2, draw=False)]
    for k in range(5):
        x = 490 + k * 190
        els += [rect(x, 560, 100, 140, "#bfa47c", "#8a6a48", 1.5, 0, round(.9 + .05 * k, 2)), rect(x, 548, 100, 14, "#a88f6a", at=round(.9 + .05 * k, 2))]
    els += [palm(200, g, 170), palm(260, g, 130), palm(1580, g, 160), glow(889, 500, 600, .3, .2, "lamp"),
            lab(889, 196, "Temple of Hathor, Dendera", .8, GOLD, 34), lab(889, 760, "begun about 54 BCE", tbe, BONE, 30)]
    return {"base": "sky", "tod": "dusk", "ground": g, "sun": [1450, 470, 26], "cam": CAM, "els": els}


REL = (464, 250, .85)                 # the relief in s19: top-left corner and scale (a 1000 x 500 box -> 850 x 425)


def s19(C):
    """s19 · the relief, built as named; each part gets a dotted lilac claim label (above or below it): bulb?, filament?, socket?, cable?, insulator?"""
    x0, y0, s = REL
    tb, tf, tso, tca, tin = C.at(18, "bulb"), C.at(18, "filament"), C.at(18, "socket"), C.at(18, "cable"), C.at(18, "insulator")
    els, P = relief(x0, y0, s, {"slab": .4, "bulb": round(tb - .6, 2), "snake": round(tf - .6, 2), "flower": round(tso - .5, 2), "stem": round(tca - .4, 2), "djed": round(tin - .7, 2)})
    top_y, bot_y = 196, 752
    rows = [(tb, P(520, 125), "bulb?", 900, top_y), (tf, P(800, 200), "filament?", 1180, top_y), (tso, P(100, 250), "socket?", 600, bot_y),
            (tca, P(44, 400), "cable?", 420, bot_y), (tin, P(700, 455), "insulator?", 1060, bot_y)]
    out = [flat(), rect(x0 - 30, y0 - 30, 1000 * s + 60, 500 * s + 60, "#2a241e", r=8, at=-1), glow(x0 + 500 * s, y0 + 250 * s, 600, .3, .2, "lamp")] + els
    for at, (px, py), t, lx, ly in rows:
        ey = ly + 12 if ly < y0 else ly - 34
        out += [ln([(px, py), (lx, ey)], round(at + .2, 2), LILAC, 2, "claimed", .5), dot(px, py, 6, LILAC, round(at + .1, 2)),
                lab(lx, ly, t, round(at + .4, 2), LILAC, 32)]
    return {"base": "dark", "cam": CAM, "els": out}


def s20(C):
    """s20 · a tomb corridor: a painter at the wall, a small oil lamp; a dotted 'smoke?'; a pottery shard with hieratic strokes:
    a receipt for lamps, Valley of the Kings; then salt grains fall into the lamp."""
    tsm, trec, tsalt = C.at(19, "smoke"), C.at(19, "receipt"), C.at(19, "salt")
    vx, vy = 760, 420
    els = [poly([(80, 130), (vx - 70, vy - 60), (vx - 70, vy + 80), (80, 800)], "#4a3a2c", "rgba(255,226,190,.15)", 1.5, -1),
           poly([(1440, 130), (vx + 70, vy - 60), (vx + 70, vy + 80), (1440, 800)], "#3e3125", "rgba(255,226,190,.12)", 1.5, -1),
           poly([(80, 130), (1440, 130), (vx + 70, vy - 60), (vx - 70, vy - 60)], "#2c231b", at=-1),
           poly([(80, 800), (1440, 800), (vx + 70, vy + 80), (vx - 70, vy + 80)], "#33281f", at=-1),
           rect(vx - 70, vy - 60, 140, 140, "#0e0b09", at=-1)]
    for k in range(4):
        y = 260 + 80 * k
        els.append(ln([(170 + 30 * k, y), (420, y + 20 - 6 * k)], .3 + .1 * k, "#d8b070", 3, draw=False, op=.7))
    els += [person(520, 780, 300, .3, "#1a1511"), ln([(540, 560), (470, 470), (430, 440)], .5, "#1a1511", 12, draw=False),
            poly([(600, 770), (680, 770), (668, 790), (612, 790)], "#b98a5a", "#e2c49a", 1.5, .6), poly([(636, 770), (642, 735), (650, 770)], "#ffd27a", at=.7),
            glow(642, 740, 260, .7, .9, "fire")]
    els += [ln([(642, 720), (630, 660), (660, 600), (640, 540)], tsm, LILAC, 4, "claimed", .8, curve=True), lab(700, 540, "smoke?", round(tsm + .4, 2), LILAC, 30, "start")]
    shard = [(1180, 300), (1380, 260), (1600, 320), (1640, 470), (1560, 600), (1300, 620), (1170, 520)]
    els += [poly(shard, "#d9c4a0", "#8a6a48", 2, trec, fx="pop"), {"k": "glyphs", "x": 1230, "y": 330, "w": 340, "h": 240, "rows": 5, "cols": 8, "kind": "hieratic", "c": "#3a2416",
                                                                    "in": round(trec + .3, 2), "seed": 4},
            lab(1410, 680, "a receipt for lamps", round(trec + .6, 2), GOLD, 30), lab(1410, 720, "Valley of the Kings", round(trec + .9, 2), DIM, 26)]
    els += [dot(600 + 8 * k, 690 + 14 * (k % 3), 4, "#ffffff", round(tsalt + .12 * k, 2)) for k in range(6)] + [lab(560, 690, "salt?", round(tsalt + .5, 2), BONE, 26, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def s21(C):
    """s21 · the caption: the relief again (smaller, settled), a column of hieroglyphs writes itself beside it; 'Harsomtus', 'lotus
    flower', a small sun rising from the flower; then a gold statue of a cobra rising from a lotus beside a ruler of four palms (30 cm)."""
    tcap, thar, tlot, tsun, tgold, tpal = (C.at(20, "caption"), C.at(20, "Harsomtus"), C.at(20, "lotus"), C.at(20, "the sun on"), C.at(20, "gold"), C.at(20, "four palms"))
    x0, y0, s = 120, 260, .76
    rel, P = relief(x0, y0, s, settled=True)
    for e in rel:
        e["in"] = .3
    els = [rect(x0 - 24, y0 - 40, 1000 * s + 48, 500 * s + 80, "#2a241e", at=.2)] + rel
    els += [rect(950, 210, 140, 500, "#5d5649", "#a59a84", 2, 4, round(tcap - .2, 2), fx="pop"),
            {"k": "glyphs", "x": 965, "y": 228, "w": 110, "h": 466, "rows": 12, "cols": 2, "kind": "hieroglyph", "c": "#ece2c8", "in": round(tcap + .3, 2), "seed": 7, "sw": 4}]
    hx, hy = P(560, 150)
    fx_, fy_ = P(100, 250)
    sx_, sy_ = P(175, 175)
    els += [lab(hx, y0 - 62, "Harsomtus", thar, GOLD, 34), ln([(hx, y0 - 50), P(600, 220)], round(thar + .2, 2), GOLD, 2, dur=.4),
            lab(fx_, y0 + 500 * s + 80, "lotus flower", tlot, GOLD, 30), ln([(fx_, y0 + 500 * s + 50), (fx_, fy_ + 50)], round(tlot + .2, 2), GOLD, 2, dur=.3),
            glow(sx_, sy_, 120, tsun, .8, "sun"), dot(sx_, sy_, 16, "#ffe2a0", tsun)] + \
           [ln([(sx_ + 24 * math.cos(a), sy_ + 24 * math.sin(a)), (sx_ + 38 * math.cos(a), sy_ + 38 * math.sin(a))], round(tsun + .2, 2), "#ffe2a0", 3, draw=False)
            for a in [math.pi * (1.0 + k / 5) for k in range(6)]]
    # the statue: a cobra rising from a lotus on a little base; 30 cm = 240 units (8 a centimetre), beside four palm bands (7.5 cm each)
    sx, sb, k = 1360, 700, 8
    cup = [(sx, sb - 3 * k), (sx - 10 * k, sb - 10 * k), (sx - 6 * k, sb - 9 * k), (sx - 3 * k, sb - 12 * k), (sx, sb - 8 * k), (sx + 3 * k, sb - 12 * k),
           (sx + 6 * k, sb - 9 * k), (sx + 10 * k, sb - 10 * k)]
    body = [(sx, sb - 9 * k), (sx - 3 * k, sb - 14 * k), (sx + 2 * k, sb - 19 * k), (sx - 1 * k, sb - 24 * k)]
    st = [rect(sx - 7 * k, sb - 3 * k, 14 * k, 3 * k, "#c9a050", "#ffe2a0", 1.5, 3, tgold),
          poly(cup, AU, "#fff0c0", 1.5, tgold), ln(body, tgold, AU, 2.2 * k, curve=True, draw=False),
          poly(ellipse(sx - 1 * k, sb - 26.5 * k, 2.6 * k, 3.4 * k, 18)[:-1], AU, "#fff0c0", 1.5, tgold),
          poly([(sx - 2 * k, sb - 29 * k), (sx + 2.5 * k, sb - 30 * k), (sx - .5 * k, sb - 28 * k)], AU, at=tgold),
          glow(sx, sb - 15 * k, 170, tgold, .55, "lamp")]
    ruler = []
    for j in range(4):
        y1 = sb - j * 7.5 * k
        ruler += [rect(sx + 120, y1 - 7.5 * k, 40, 7.5 * k - 3, "rgba(242,201,142,.18)" if j % 2 else "rgba(242,201,142,.32)", GOLD, 1.5, 2, round(tpal + .25 * j, 2), fx="pop")]
    els += st + ruler + [lab(sx - 100, sb - 28 * k, "gold", round(tgold + .2, 2), AU, 34, "end"),
                         lab(sx + 180, sb - 15 * k - 8, "4 palms", round(tpal + 1.0, 2), GOLD, 30, "start"),
                         lab(sx + 180, sb - 15 * k + 30, "about 30 cm", round(tpal + 1.2, 2), BONE, 26, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s22(C):
    """s22 · the crypt in cutaway: a long, low, narrow room inside the temple's wall; small relief panels on its walls light up one by
    one; the statues they picture stand in front, drawn dashed (they are gone); a lamp."""
    tsto, tpic = C.at(21, "storeroom"), C.at(21, "picture")
    els = [rect(80, 160, 1620, 600, "#9a8466", "#d8bd93", 2, 0, -1), rect(80, 160, 1620, 30, "#b9a07a", at=-1),
           lab(889, 140, "the temple", .3, DIM, 26),
           rect(160, 380, 1460, 230, "#1b1511", "#d8bd93", 2, 2, .4), lab(889, 680, "a crypt in the wall", .8, BONE, 28)]
    for k in range(7):
        x = 220 + k * 200
        at = round(tpic + .25 * k, 2)
        els += [rect(x, 410, 120, 90, "#5d5649", "#a59a84", 1.5, 3, at), ln([(x + 20, 470), (x + 60, 440), (x + 100, 455)], at, "#ece2c8", 3, curve=True, draw=False),
                glow(x + 60, 455, 70, at, .45, "lamp")]
        sx, sb = x + 60, 600
        els += [poly([(sx, sb - 20), (sx - 24, sb - 50), (sx - 8, sb - 30), (sx, sb - 56), (sx + 8, sb - 30), (sx + 24, sb - 50)], "none", AU, 2, round(at + .3, 2), style="inferred"),
                ln([(sx, sb - 50), (sx - 6, sb - 66), (sx + 4, sb - 78)], round(at + .3, 2), AU, 3, "inferred", .3, curve=True)]
    els += [glow(260, 560, 120, tsto, .8, "fire"), lab(889, 360 - 2, "a storeroom", tsto + .2, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s23(C):
    """s23 · a trench in section; three dotted ghosts in its layers (a coil of wire, a glass bulb, a socket); a lamp sweeps it: 'not found'."""
    tt, tn = C.at(22, "traces"), C.at(22, "None")
    lay = [{"d": 0, "c": "#8a6a48", "t": ""}, {"d": 140, "c": "#6f5a44", "t": ""}, {"d": 290, "c": "#5a4632", "t": ""}, {"d": 420, "c": "#4a3a2c", "t": ""}]
    els = [rect(560, 300, 660, 460, "rgba(12,9,7,.35)", BONE, 2, 2, .3, style="inferred"), person(500, 300, 150, .5, "#1a1511")]
    coil = [(760 + 26 * math.cos(a) + a * 7, 470 + 26 * math.sin(a)) for a in [k * .5 for k in range(40)]]
    els += [ln(coil, tt, LILAC, 3, "claimed", .9, curve=True), lab(860, 430, "wires?", round(tt + .3, 2), LILAC, 26),
            poly(ellipse(1000, 560, 40, 52, 24)[:-1], "none", LILAC, 3, round(tt + .5, 2), style="claimed"), rect(982, 610, 36, 26, "none", LILAC, 3, 3, round(tt + .5, 2), style="claimed"),
            lab(1000, 490, "glass?", round(tt + .7, 2), LILAC, 26),
            rect(1080, 660, 70, 50, "none", LILAC, 3, 6, round(tt + .9, 2), style="claimed"), lab(1115, 740, "sockets?", round(tt + 1.1, 2), LILAC, 26)]
    els += [glow(700 + 160 * k, 520 + 40 * (k % 2), 140, round(tn - .6 + .3 * k, 2), .35, "lamp") for k in range(4)] + \
           [lab(889, 240, "not found", tn + .2, GOLD, 40, st="serif")]
    return {"base": "section", "tod": "night", "ground": 300, "lx": 40, "layers": lay, "cam": CAM, "els": els}


def s24(C):
    """s24 · across the Atlantic: a dotted arc from Dendera to Palenque."""
    v = View(-105, 45, 0, 42, (90, 130, 1600, 640))
    d, p = v.p(32.67, 26.14), v.p(-92.05, 17.48)
    tp = C.at(23, "Palenque")
    mid = ((d[0] + p[0]) / 2, min(d[1], p[1]) - 210)
    return {"base": "map", "cam": CAM, "els": [
        {"k": "map", "land": v.land(), "in": -1},
        {"k": "pin", "x": d[0], "y": d[1], "t": "Dendera", "c": DIM, "lx": 20, "ly": 8, "in": .3, "r": 7},
        ln([d, mid, p], .6, GOLD, 3, "inferred", 1.6, curve=True),
        {"k": "pin", "x": p[0], "y": p[1], "t": "Palenque", "c": GOLD, "lx": 18, "ly": 34, "in": tp},
        lab(v.p(-40, 28)[0], v.p(-40, 28)[1], "Atlantic Ocean", .5, "#9fc4dc", 28, st="ital"),
        lab(v.p(-102, 26)[0], v.p(-102, 26)[1], "Mexico", round(tp + .3, 2), DIM, 28, st="ital")]}


def s25(C):
    """s25 · the Temple of the Inscriptions in section, at dusk in the forest: a stepped pyramid, its temple on top, a stairway inside
    down to the crypt near ground level; a lamp travels down and lights the crypt and its sarcophagus; 'Ruz, 1952'."""
    g = 740
    t52, ttomb = C.at(24, "In nineteen"), C.at(24, "sealed tomb")
    tiers = 8
    els = []
    for k in range(tiers):
        w = 900 - k * 70
        els.append(rect(889 - w / 2, g - (k + 1) * 46, w, 46, "#9a8466" if k % 2 else "#a8927a", "#d8bd93", 1.5, 0, -1))
    top = g - tiers * 46
    els += [rect(889 - 160, top - 90, 320, 90, "#b9a07a", "#e2cfa8", 1.5, 0, -1), rect(889 - 180, top - 104, 360, 16, "#8f7a5e", at=-1),
            rect(889 - 30, top - 70, 60, 70, "#1b1511", at=-1)]
    stair = [(889, top), (889 - 40, top + 80), (889 + 120, top + 170), (889 + 60, g - 60), (889, g - 40)]
    els += [ln(stair, round(t52 + .3, 2), BONE, 3, "inferred", 1.6), rect(889 - 90, g - 70, 180, 64, "#1b1511", "#d8bd93", 2, 2, round(ttomb - .3, 2)),
            rect(889 - 60, g - 44, 120, 30, "#8f8470", STONE_E, 1.5, 2, round(ttomb + .2, 2))]
    els += [glow(x, y, 70, round(t52 + .3 + .4 * k, 2), .8, "fire") for k, (x, y) in enumerate(stair)] + [glow(889, g - 40, 160, round(ttomb + .1, 2), .8, "lamp")]
    els += [palm(160, g, 200), palm(240, g, 150), palm(1560, g, 190), palm(1640, g, 140),
            lab(889, top - 140, "Temple of the Inscriptions", .5, GOLD, 30), lab(1300, 560, "Ruz, 1952", t52 + .4, BONE, 30, "start"),
            lab(1300, 600, "a sealed tomb", ttomb + .3, DIM, 26, "start"), ln([(1290, 600), (990, g - 40)], ttomb + .3, DIM, 1.5, "inferred", .5)]
    return {"base": "sky", "tod": "dusk", "ground": g, "sun": [300, 520, 22], "cam": CAM, "els": els}


LIDC = (889, 150, 640)                # the lid in chapter 2: centre x, top, height


def s26(C):
    """s26 · the lid (settled), and the claimed rocket drawn dotted over it: 'a rocket?'"""
    cx, top, H = LIDC
    tr = C.at(25, "rocket", lo=.5)
    els, (x0, y0, W, Hh), F = lid(cx, top, H)
    return {"base": "dark", "cam": CAM, "els": [flat(), glow(cx, 480, 520, .2, .25, "lamp")] + els + rocket_over(F, round(tr - .9, 2)) + [
        lab(x0 + W + 50, 300, "a rocket?", tr, LILAC, 38, "start"), lab(x0 + W + 50, 345, "von Däniken, 1968", round(tr + .3, 2), LILAC, 24, "start")]}


def s27_late(C):
    """s27 · the rocket fades (the field is wiped and the carving drawn again, the claim's labels veiled); the glyph band glows; labels
    as said: his name, died 683 CE, ruled 68 years (a bar 615 to 683), World Tree, sacred bird, jaws of the underworld."""
    cx, top, H = LIDC
    els, (x0, y0, W, Hh), F = lid(cx, top, H)
    b = W * .07
    tname, tdie, truled, ttree, tbird, tjaw = (C.at(26, "names its man", lo=.3), C.at(26, "the year he died"), C.at(26, "He had ruled"), C.at(26, "World"),
                                               C.at(26, "sacred bird"), C.at(26, "open jaws"))
    tw = round(tname - .3, 2)
    carv, _, _ = lid(cx, top, H, carving_only=True)
    for e in carv:
        e["in"] = round(tw + .45, 2)
        e.pop("fx", None)
    out = [wipe(x0 + b, y0 + b, W - 2 * b, Hh - 2 * b, tw, STONE, 1.0, .45)] + carv + \
          [wipe(x0 + W + 10, 230, 560, 150, tw, FLAT, 1.0, .45)]
    for k in range(6):
        u = (k + .5) / 6
        out.append(glow(round(x0 + W * u, 1), round(y0 + b / 2, 1), 60, round(tname + .1 + .08 * k, 2), .6, "lamp"))
    L, Rr = x0 - 40, x0 + W + 40
    out += [lab(L, 210, "K'inich Janaab Pakal", round(tname + .5, 2), GOLD, 32, "end"),
            lab(L, 252, "died 683 CE", tdie, BONE, 28, "end"),
            rect(L - 300, 300, 300, 14, "rgba(242,201,142,.25)", GOLD, 1.5, 7, truled, fx="fill"),
            lab(L - 300, 290, "615", round(truled + .2, 2), DIM, 24, "start"), lab(L, 290, "683", round(truled + .2, 2), DIM, 24, "end"),
            lab(L - 150, 350, "ruled 68 years", round(truled + .4, 2), BONE, 26)]
    tx, ty = F(.5, .34)
    out += [ln([F(.5, .74), F(.5, .15)], ttree, GREEN, 5, dur=.8), ln([F(.13, .34), F(.87, .34)], round(ttree + .4, 2), GREEN, 5, dur=.6),
            ln([F(.92, .34), (Rr - 10, ty)], round(ttree + .6, 2), GREEN, 1.6, dur=.3), lab(Rr, ty + 10, "World Tree", round(ttree + .7, 2), GREEN, 32, "start")]
    bx, by = F(.7, .05)
    out += [ln([(bx, by), (Rr - 10, by - 20)], tbird, GOLD, 1.6, dur=.3), lab(Rr, by - 10, "sacred bird", round(tbird + .1, 2), GOLD, 30, "start")]
    jx, jy = F(.90, .86)
    out += [ln([(jx, jy), (Rr - 10, jy)], tjaw, GOLD, 1.6, dur=.3), lab(Rr, jy - 4, "jaws of the", round(tjaw + .1, 2), GOLD, 30, "start"),
            lab(Rr, jy + 32, "underworld", round(tjaw + .1, 2), GOLD, 30, "start")]
    return out


def s28(C):
    """s28 · the same tree twice: at the left a small copy of the lid's tree; at the right the Temple of the Cross tablet with the
    same cross-shaped tree between two standing figures (Pakal's son, young and grown); a dashed link: 'the same tree'."""
    tsym, tson, tsame = C.at(27, "symbol"), C.at(27, "Pakal's son"), C.at(27, "very same")
    def tree(cx, top, h, at, c=CARVE, w=1.0):
        out = [ln([(cx, top + h), (cx, top + h * .12)], at, c, 12 * w, dur=.6), ln([(cx - h * .38, top + h * .3), (cx + h * .38, top + h * .3)], round(at + .3, 2), c, 10 * w, dur=.5)]
        for sd in (-1, 1):
            u = cx + sd * h * .38
            out.append(ln([(u, top + h * .3), (u + sd * h * .06, top + h * .25), (u + sd * h * .09, top + h * .33), (u + sd * h * .04, top + h * .38)], round(at + .5, 2), c, 5 * w,
                          curve=True, draw=False))
        out.append(poly([(cx, top + h * .1), (cx - h * .1, top + h * .06), (cx - h * .2, top), (cx - h * .06, top + h * .01), (cx, top - h * .05),
                         (cx + h * .06, top + h * .01), (cx + h * .2, top), (cx + h * .1, top + h * .06)], c, at=round(at + .6, 2), fx="pop"))
        return out
    els = [rect(150, 200, 420, 560, STONE, STONE_E, 2, 6, .2)] + tree(360, 270, 380, .4) + [lab(360, 800 - 10, "Pakal's lid", .6, DIM, 26)]
    els += [rect(780, 170, 860, 590, "#8a7f6c", STONE_E, 2, 6, round(tson - .8, 2))] + tree(1210, 240, 420, round(tson - .4, 2))
    els += [person(960, 700, 230, round(tson + .2, 2), CARVE), person(1460, 700, 290, round(tson + .4, 2), CARVE), lab(1210, 800 - 10, "Temple of the Cross", round(tson, 2), GOLD, 28)]
    els += [ln([(470, 380), (900, 330), (1090, 360)], tsame, GOLD, 3, "inferred", 1.0, curve=True), lab(700, 290, "the same tree", round(tsame + .6, 2), GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s29(C):
    """s29 · the reclining king alone, larger (the foot of a big copy of the lid): a dashed arrow down into the jaws (falling?), a dashed
    arrow up beside a maize plant (rising reborn?); then a warm glow over him."""
    tf, tr, th = C.at(28, "falling"), C.at(28, "rising"), C.at(28, "hope")
    els, (x0, y0, W, Hh), F = lid(889, -411, 1222, None)
    keep = []
    for e in els:                                         # keep only the king, his earth mask and the jaws: drop slab, band, tree, bird, symbols
        if e.get("k") == "rect":
            continue
        ys = [p[1] for p in e.get("p", [])] or [e.get("y", 0)]
        if min(ys) > 250:
            keep.append(e)
    els = [glow(889, 560, 560, .2, .2, "lamp")] + keep
    els += [arrow([[640, 230], [600, 470], [700, 650]], tf, LILAC, 4, "inferred", 1.0), lab(580, 420, "falling?", round(tf + .4, 2), LILAC, 32, "end"),
            arrow([[1100, 520], [1160, 360], [1140, 180]], tr, GREEN, 4, "inferred", 1.0), lab(1190, 250, "rising reborn?", round(tr + .5, 2), GREEN, 32, "start")]
    mx, my = 1340, 720
    els += [ln([(mx, my), (mx, my - 300)], round(tr + .4, 2), "#8fbf5a", 6, dur=.8)] + \
           [ln([(mx, my - 80 - 50 * k), (mx + (1 if k % 2 else -1) * 90, my - 140 - 50 * k)], round(tr + .6 + .15 * k, 2), "#8fbf5a", 5, curve=True, dur=.4) for k in range(4)] + \
           [poly(ellipse(mx + 14, my - 320, 14, 36, 16)[:-1], "#e8c35a", at=round(tr + 1.2, 2), fx="pop"), lab(mx + 70, my + 10, "maize", round(tr + 1.3, 2), "#a9d47c", 26, "start")]
    els += [glow(889, 420, 500, th, .55, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================ chapter 3 · Nazca
PAMPA = "#a9835a"


def s30(C):
    """s30 · the pampa from above: two long straight lines cross it; the hummingbird draws itself, 93 m against a 100 m bar, with a
    1.7 m person at its beak (a speck); small framed thumbnails of the monkey and the spider (not to the same scale)."""
    tlin, tmon, tspi, tani, thum, tm93 = C.at(29, "Straight lines"), C.at(29, "a monkey"), C.at(29, "a spider"), C.at(29, "giant animals"), C.at(29, "hummingbird"), C.at(29, "ninety-three")
    L = 760                               # 93 m: 8.17 units a metre
    m = L / 93
    hb = hbird(780, 470, L)
    els = [ln([(-20, 250), (1800, 700)], tlin, "#f1e2c2", 9, dur=1.4, op=.8), ln([(300, 820), (1500, 130)], round(tlin + .6, 2), "#f1e2c2", 7, dur=1.4, op=.7)]
    els += [ln(hb + [hb[0]], tani, "#fff2d6", 5, dur=2.4)]
    bx = 260
    els += [ln([(bx, 770), (bx + 100 * m, 770)], tm93, BONE, 3, dur=.8), ln([(bx, 758), (bx, 782)], tm93, BONE, 3, draw=False),
            ln([(bx + 100 * m, 758), (bx + 100 * m, 782)], round(tm93 + .5, 2), BONE, 3, draw=False), lab(bx + 50 * m, 750, "100 m", round(tm93 + .6, 2), BONE, 28),
            lab(780, 150, "hummingbird, 93 m", round(thum + .3, 2), GOLD, 32)]
    px, py = hb[0]
    els += [person(px - 10, py + 6, round(1.7 * m, 1), round(tm93 + .9, 2), "#1a1511"), ring(px - 10, py - 4, 26, round(tm93 + .9, 2), BONE, 2, dur=.5),
            lab(px - 10, py + 60, "a person", round(tm93 + 1.1, 2), BONE, 24)]
    def frame(x, y, at, t):
        return [rect(x, y, 170, 150, "rgba(26,21,17,.75)", "#e9dccb", 2, 8, at, fx="pop"), lab(x + 85, y + 182, t, round(at + .2, 2), BONE, 24)]
    c = "#fff2d6"
    mx, my, a = 1505, 228, round(tmon + .2, 2)
    spiral = [(mx + 22 + (4 + 3.2 * q) * math.cos(q * 1.1), my + 18 + (4 + 3.2 * q) * math.sin(q * 1.1)) for q in range(14)]
    monkey = [poly(ellipse(mx - 10, my, 26, 18, 16)[:-1], "none", c, 3, a), {"k": "circle", "x": mx - 44, "y": my - 22, "r": 11, "fill": "none", "c": c, "w": 3, "in": a},
              ln([(mx - 30, my + 10), (mx - 46, my + 40)], a, c, 3, draw=False), ln([(mx + 6, my + 12), (mx + 4, my + 44)], a, c, 3, draw=False),
              ln([(mx - 30, my - 8), (mx - 56, my - 44)], a, c, 3, draw=False), ln(spiral[::-1] + [(mx + 14, my + 4)], a, c, 3, curve=True, draw=False)]
    els += frame(1420, 150, tmon, "monkey") + monkey
    sp = [ln([(1505, 455), (1505 + dx, 455 + dy)], round(tspi + .2, 2), c, 3, draw=False) for dx, dy in ((-50, -40), (50, -40), (-55, 0), (55, 0), (-50, 40), (50, 40), (-35, 60), (35, 60))]
    els += frame(1420, 380, tspi, "spider") + [poly(ellipse(1505, 455, 22, 30, 16)[:-1], "#3a2c20", c, 3, round(tspi + .2, 2))] + sp
    return {"base": "plan", "bg": PAMPA, "north": False, "cam": CAM, "els": els}


def s31(C):
    """s31 · a low view of the plain: a dotted runway trapezoid and a dotted saucer at its end ('runway?'); then a person at eye level,
    the bird's lines running off past him, a dotted sightline up: 'seen from above?'"""
    tr, tab = C.at(30, "runways"), C.at(30, "above")
    hz = 330
    els = [poly([(-20, hz), (1800, hz), (1800, 1040), (-20, 1040)], "#9a7650", at=-1), ln([(-20, hz), (1800, hz)], -1, "rgba(255,226,190,.4)", 1.5, draw=False)]
    els += [poly([(560, 780), (1220, 780), (950, hz + 10), (830, hz + 10)], "rgba(201,193,238,.08)", LILAC, 3, tr, style="claimed"),
            lab(540, 740, "runway?", round(tr + .4, 2), LILAC, 34, "end")] + ufo(890, hz - 50, round(tr + .6, 2), .7)
    els += [ln([(1300, 800), (1340, 600), (1290, 470), (1180, hz + 20)], round(tab - 1.6, 2), "#f1e2c2", 5, dur=.8, op=.8, curve=True),
            ln([(1720, 760), (1630, 520), (1500, hz + 40)], round(tab - 1.4, 2), "#f1e2c2", 5, dur=.8, op=.8, curve=True),
            person(1540, 790, 170, round(tab - 1.2, 2), "#1a1511"), ln([(1545, 640), (1620, 260)], round(tab - .2, 2), LILAC, 3, "claimed", .6),
            lab(1600, 220, "seen from above?", tab, LILAC, 32, "end")]
    return {"base": "sky", "tod": "day", "ground": hz, "sun": [300, 200, 26], "cam": CAM, "els": els}


def s32(C):
    """s32 · the desert floor from above: dark rust-coloured stones on pale ground; a strip is swept clear (a pale line draws through)
    and the moved stones heap on both sides; inset, a dusty car door with a finger line; then a dotted wheel sinks: 'too soft'."""
    tdk, tmv, tcar, tsoft = C.at(31, "dark"), C.at(31, "Move them"), C.at(31, "dusty"), C.at(31, "too soft")
    els = [rect(80, 130, 1000, 640, "#e4cfa2", at=-1)]
    r = random.Random(5)
    for k in range(240):
        x, y = r.uniform(96, 1064), r.uniform(146, 754)
        els.append(dot(round(x, 1), round(y, 1), round(r.uniform(9, 17), 1), ["#6a3f26", "#7a4a2c", "#5c3826"][k % 3], round(tdk + .004 * k, 2), fx=None))
    els += [ln([(118, 450), (1042, 450)], tmv, "#efdcb0", 74, dur=1.6)]
    for k in range(40):
        x = 110 + 23.5 * k + r.uniform(-5, 5)
        for sd in (-1, 1):
            els.append(dot(round(x, 1), round(450 + sd * (44 + r.uniform(0, 10)), 1), round(r.uniform(9, 14), 1), "#5c3826", round(tmv + .04 * k, 2)))
    els += [lab(580, 800 - 12, "pale ground shows through", round(tmv + 1.0, 2), BONE, 28)]
    els += [rect(1180, 180, 470, 300, "#7d8590", "#cfd6de", 2, 22, tcar, fx="pop"), rect(1180, 180, 470, 300, "rgba(200,180,140,.55)", r=22, at=tcar),
            ln([(1240, 380), (1330, 300), (1450, 350), (1580, 270)], round(tcar + .3, 2), "#dfe6ee", 10, curve=True, dur=1.0), lab(1415, 520, "a finger in the dust", round(tcar + .5, 2), BONE, 26)]
    els += [{"k": "circle", "x": 1415, "y": 650, "r": 60, "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": tsoft},
            arrow([[1415, 560], [1415, 640]], round(tsoft + .2, 2), LILAC, 3, "claimed", .4, False), rect(1300, 690, 230, 14, "#c9a370", r=4, at=round(tsoft + .3, 2)),
            lab(1415, 760, "too soft", round(tsoft + .5, 2), LILAC, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


COND = (889, 450, 1000)               # Nickell's condor in the field: centre, length (134 m: 7.5 units a metre)


def s33(C):
    """s33 · a field from above: a cord as the centre line from beak to tail; six people (to scale, specks); a wooden T; stakes pop at
    measured offsets (dashed cords), then the outline joins them and the condor appears; '134 m'."""
    cx, cy, L = COND
    t82, tsix, tT, tsc, tpt = C.at(32, "In nineteen"), C.at(32, "five relatives"), C.at(32, "wooden T"), C.at(32, "scaled up"), C.at(32, "point by point")
    m = L / 134
    pts = condor_pts(cx, cy, L)
    els = [rect(-20, -20, W_ + 40, H_ + 40, "#4f6a3c", at=-1), lab(110, 245, "Kentucky, 1982", t82, GOLD, 30, "start"),
           ln([(cx - L / 2, cy), (cx + L / 2, cy)], round(t82 + .5, 2), BONE, 2.5, dur=1.2)]
    spots = [(170, 600), (240, 650), (310, 610), (1480, 600), (1550, 650), (1620, 610)]
    for k, (x, y) in enumerate(spots):
        els += [person(x, y, round(1.7 * m, 1), round(tsix + .15 * k, 2), "#f0e6d0"), ring(x, y - 6, 16, round(tsix + .15 * k, 2), "rgba(240,230,208,.5)", 1.5, dur=.3)]
    els += [lab(240, 700, "six people,", round(tsix + 1.0, 2), BONE, 24), lab(240, 730, "to scale", round(tsix + 1.0, 2), BONE, 24)]
    sel = pts[::2]
    for k, (x, y) in enumerate(sel):
        at = round(tsc + .09 * k, 2)
        els += [ln([(x, cy), (x, y)], at, "#e8d6b0", 1.5, "inferred", .2), dot(round(x, 1), round(y, 1), 5, "#f2c98e", round(at + .1, 2))]
    tx = sel[6][0]
    els += [ln([(tx - 22, cy), (tx + 22, cy)], tT, "#c9a370", 6, draw=False), ln([(tx, cy), (tx, cy - 30)], tT, "#c9a370", 6, draw=False)]
    els += [ln(pts, tpt, "#fff2d6", 4, dur=2.2), dimline(cx - L / 2, cy + 300, cx + L / 2, cy + 300, "", round(tpt + 1.6, 2), GOLD),
            lab(cx, cy + 290, "134 m", round(tpt + 1.8, 2), GOLD, 32), lab(cx, 160, "the Nazca condor", round(tpt + 1.2, 2), BONE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s34_late(C):
    """s34 · a clock sweeps nine hours; an aerial frame closes over the condor and a green tick: 'from the air, it matched'."""
    tnine, tair = C.at(33, "nine"), C.at(33, "from the air")
    x, y, r = 1560, 230, 70
    els = [{"k": "circle", "x": x, "y": y, "r": r, "fill": "rgba(18,13,10,.85)", "c": BONE, "w": 3, "in": round(tnine - .4, 2), "fx": "pop"}]
    for k in range(10):
        a = -math.pi / 2 + 2 * math.pi * (k * .75) / 12
        els.append(ln([(x, y), (x + r * .78 * math.cos(a), y + r * .78 * math.sin(a))], round(tnine + .12 * k, 2), GOLD if k == 9 else "rgba(242,201,142,.35)", 4, draw=False))
    els += [lab(x, y + r + 40, "about 9 hours", round(tnine + 1.2, 2), GOLD, 28)]
    cx, cy, L = COND
    for sx in (-1, 1):
        for sy in (-1, 1):
            X0, Y0 = cx + sx * (L / 2 + 30), cy + sy * 290
            els.append(ln([(X0, Y0 - sy * 60), (X0, Y0), (X0 - sx * 80, Y0)], tair, BONE, 5, dur=.4))
    els += [tick(1440, 420, round(tair + .6, 2), GREEN, 1.4), lab(1480, 432, "from the air,", round(tair + .7, 2), GREEN, 30, "start"),
            lab(1480, 472, "it matched", round(tair + .8, 2), GREEN, 30, "start")]
    return els


def s35(C):
    """s35 · a plan of the pampa: dashed old footpaths; '430 known', then '+303 in six months' as 303 small marks pop near the paths;
    little walkers move along a path: 'beside the footpaths'."""
    t24, tdbl, tfoot, twalk = C.at(34, "in twenty"), C.at(34, "doubling"), C.at(34, "footpaths"), C.at(34, "walking")
    paths = [[(80, 300), (400, 340), (760, 260), (1100, 330), (1480, 250), (1700, 300)],
             [(80, 560), (420, 520), (700, 610), (1050, 540), (1400, 620), (1700, 560)],
             [(500, 800), (560, 640), (640, 470), (760, 330), (860, 140)]]
    els = [ln(p, .3 + .2 * k, "#f1e2c2", 3, "inferred", 1.2, curve=True) for k, p in enumerate(paths)]
    r = random.Random(7)
    def near(path):
        k = r.randrange(len(path) - 1)
        (xa, ya), (xb, yb) = path[k], path[k + 1]
        f = r.random()
        return xa + (xb - xa) * f + r.uniform(-40, 40), ya + (yb - ya) * f + r.uniform(-40, 40)
    marks = [near(paths[k % 3]) for k in range(303)]
    marks = [(min(1690, max(90, x)), min(790, max(130, y))) for x, y in marks]
    els += [rect(1290, 650, 380, 130, "rgba(26,21,17,.8)", "#e9dccb", 2, 10, t24, fx="pop"), lab(1480, 700, "430 known before", round(t24 + .3, 2), BONE, 28)]
    els += [dot(round(x, 1), round(y, 1), 4.5, "#3a2416", round(t24 + .8 + .006 * k, 2)) for k, (x, y) in enumerate(marks)]
    els += [lab(1480, 750, "+303 in six months", tdbl, GOLD, 30)]
    p = paths[1]
    for k in range(5):
        f = .15 + .14 * k
        i = int(f * (len(p) - 1))
        g = f * (len(p) - 1) - i
        x = p[i][0] + (p[i + 1][0] - p[i][0]) * g
        y = p[i][1] + (p[i + 1][1] - p[i][1]) * g
        els.append(person(round(x, 1), round(y, 1), 40, round(twalk + .15 * k, 2), "#1a1511"))
    els += [lab(560, 470, "beside the footpaths", tfoot + .3, BONE, 30)]
    return {"base": "plan", "bg": PAMPA, "north": False, "cam": CAM, "els": els}


def s36(C):
    """s36 · a giant straight line at dusk: a procession walks along it, drawn faint (inferred); a water drop; a question mark."""
    tc, tw, tb = C.at(35, "ceremonial"), C.at(35, "water"), C.at(35, "both")
    hz = 380
    els = [poly([(820, hz + 2), (960, hz + 2), (1500, 1040), (300, 1040)], "#e9d6ae", at=-1, op=.85)]
    for k in range(9):
        f = (k + 1) / 10
        x = 890 + (k % 2) * 26 - 10 + 0 * f
        y = hz + 20 + (800 - hz) * f ** 1.4
        h = 30 + 160 * f ** 1.4
        e = person(round(x + (k % 2) * 40 * f, 1), round(y, 1), round(h, 1), round(tc + .12 * (9 - k), 2), "#2a2018")
        e.update(op=.7, keepop=True)
        els.append(e)
    els += [lab(1240, 560, "ceremonial walks?", round(tc + .4, 2), LILAC, 30, "start"),
            poly([(520, 480), (490, 540), (520, 560), (550, 540)], "#7fbfe6", "#cfe6ff", 2, tw, fx="pop", curve=True), lab(520, 620, "rituals for water?", round(tw + .3, 2), BLUE, 28),
            glow(890, hz - 40, 160, tb, .5, "scan"), lab(890, hz - 10, "?", tb, LILAC, 100, st="big", fx="pop")]
    return {"base": "sky", "tod": "dusk", "ground": hz, "sun": [1450, hz - 60, 30], "cam": CAM, "els": els}


# ================================================================ chapter 4 · out of place
def s37(C):
    """s37 · a map of South Africa with a pin near Ottosdal; a pale pyrophyllite face with dark grooved spheres; three spheres by size
    beside a 10 cm ruler (24 units a centimetre), the smallest pea-sized."""
    v = View(15, 34, -35.5, -21.5, (100, 150, 500, 540))
    tm, tsp, tsz = C.at(36, "From mines"), C.at(36, "spheres"), C.at(36, "pea-sized")
    px, py = v.p(26.0, -26.8)
    win = [90, 140, 520, 560]
    els = [{"k": "group", "clip": win + [12], "bg": "#1d3a4a", "in": -1, "els": [{"k": "map", "land": v.land()}]}, rect(*win, "none", "rgba(255,236,206,.35)", 2, 12, -1),
           {"k": "pin", "x": px, "y": py, "t": "near Klerksdorp", "c": GOLD, "lx": -16, "ly": -26, "a": "end", "in": tm},
           lab(350, 670, "South Africa", .5, DIM, 26, st="ital")]
    els += [rect(700, 140, 960, 280, "#d8d0c0", "#f5ecdc", 2, 8, tsp - .5), lab(1180, 455, "rock about 3 billion years old", tsp + .4, DIM, 24)]
    for k, (x, y, r) in enumerate([(800, 240, 28), (960, 310, 36), (1120, 210, 22), (1300, 320, 32), (1460, 230, 30), (1570, 350, 18)]):
        at = round(tsp + .15 * k, 2)
        els += [{"k": "circle", "x": x, "y": y, "r": r, "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": at, "fx": "pop"},
                ln([(x - r, y), (x - r * .5, y + r * .16), (x, y + r * .2), (x + r * .5, y + r * .16), (x + r, y)], at, "#e2cf9e", 3, curve=True, draw=False)]
    k = 24                                    # units a centimetre
    base, rx = 780, 760
    els += [rect(rx, base, 10 * k, 12, "#e9dccb", at=tsz), lab(rx + 5 * k, base - 14, "10 cm", round(tsz + .2, 2), BONE, 24)]
    for j in range(11):
        els.append(ln([(rx + j * k, base), (rx + j * k, base + (8 if j % 5 else 12))], tsz, "#1a1511", 2, draw=False))
    for (cxs, d, at) in [(1080, .5, tsz + .3), (1200, 4, tsz + .6), (1420, 10, tsz + .9)]:
        r = d * k / 2
        els += [{"k": "circle", "x": cxs, "y": round(base - 4 - r, 1), "r": round(r, 1), "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": round(at, 2), "fx": "pop"}]
        if r > 10:
            els.append(ln([(cxs - r, base - 4 - r), (cxs, base - 4 - r * .8), (cxs + r, base - 4 - r)], round(at, 2), "#e2cf9e", 3, curve=True, draw=False))
    els += [lab(1080, base - 30, "pea", round(tsz + .4, 2), DIM, 24), lab(1200, base - 120, "4 cm", round(tsz + .7, 2), DIM, 24), lab(1420, base - 270, "10 cm", round(tsz + 1.0, 2), DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s38(C):
    """s38 · deep time on one bar: 3 billion years ago at the left to today; the rock at the left end; the first animals a short band
    near the right (about 600 million years ago); our species a hairline; then dotted claims round a sphere."""
    X = lambda ma: round(160 + 1460 * (3000 - ma) / 3000, 1)
    tbil, tani, tclaim = C.at(37, "three billion"), C.at(37, "animal"), C.at(37, "perfectly")
    Y = 520
    els = [rect(160, Y - 18, 1460, 36, "rgba(232,184,122,.18)", AMBER, 2, 18, tbil, fx="fill"),
           lab(160, Y + 70, "3 billion years ago", round(tbil + .3, 2), AMBER, 28, "start"), lab(1620, Y + 70, "today", round(tbil + .5, 2), DIM, 26, "end"),
           {"k": "circle", "x": 190, "y": Y, "r": 30, "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": round(tbil + .2, 2), "fx": "pop"},
           lab(190, Y - 54, "the rock", round(tbil + .4, 2), BONE, 26),
           rect(X(600), Y - 18, X(0) - X(600), 36, GREEN, r=10, at=tani, fx="pop", op=.8), lab(X(300), Y - 34, "animals", round(tani + .2, 2), GREEN, 26),
           ln([(X(0.3), Y - 60), (X(0.3), Y + 30)], round(tani + .5, 2), BONE, 2, draw=False), lab(X(0) - 4, Y - 70, "us", round(tani + .6, 2), BONE, 24, "end")]
    sx, sy = 889, 250
    els += [{"k": "circle", "x": sx, "y": sy, "r": 56, "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": round(tclaim - .3, 2), "fx": "pop"},
            ln([(sx - 56, sy), (sx - 28, sy + 9), (sx, sy + 11), (sx + 28, sy + 9), (sx + 56, sy)], round(tclaim - .3, 2), "#e2cf9e", 3, curve=True, draw=False),
            lab(sx - 100, sy - 40, "perfectly round?", tclaim, LILAC, 28, "end"), lab(sx + 100, sy - 40, "harder than steel?", round(tclaim + 1.0, 2), LILAC, 28, "start"),
            lab(sx, sy + 110, "lost technology?", round(tclaim + 2.0, 2), LILAC, 28)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s39(C):
    """s39 · sediment in section with one thin fine layer; a concretion grows ring by ring from a seed, notched where it crosses the
    fine layer: the groove; a pearl beside it; then a steel blade scratches a sphere."""
    tcon, tpe, tfine, tgro, tsc = C.at(38, "concretions"), C.at(38, "pearl"), C.at(38, "fine"), C.at(38, "the groove"), C.at(38, "steel blade")
    cx, cy, band = 560, 450, 18
    els = [rect(120, 170, 900, 580, "#b9a888", "#e9dccb", 2, 8, -1)]
    for k, y in enumerate(range(200, 740, 46)):
        els.append(ln([(130, y), (1010, y + 4)], -1, "#9c8a6c", 2, draw=False, op=.6))
    els += [rect(124, cy - band, 892, 2 * band, "#7a6a54", at=round(tfine - .3, 2)), lab(1000, cy - band - 14, "a fine layer", round(tfine, 2), BONE, 24, "end")]
    for k in range(7):
        r = 46 + 30 * k
        notch = min(22.0, .22 * r)
        pts = []
        for j in range(72):
            a = 2 * math.pi * j / 72
            dy = r * math.sin(a)
            x = cx + r * math.cos(a)
            if abs(dy) < band:
                x = cx + math.copysign(max(0.0, abs(r * math.cos(a)) - notch * (1 - (abs(dy) / band) ** 2)), math.cos(a))
            pts.append((x, cy + dy))
        last = k == 6
        els.append(poly(pts, "rgba(106,63,44,.35)" if last else "none", "#c9a07a" if last else "#6a3f2c", 3, round(tcon + .4 * k, 2), fx="draw", dur=.6))
    els += [dot(cx, cy, 8, "#3a2416", round(tcon - .2, 2)),
            arrow([[cx + 330, cy + 130], [cx + 236, cy + 10]], tgro, GOLD, 3, dur=.5, curve=False), lab(cx + 340, cy + 168, "the groove", round(tgro + .2, 2), GOLD, 30, "start")]
    els += [{"k": "circle", "x": 1300, "y": 280, "r": 60, "fill": "#efe9e0", "c": "#ffffff", "w": 2, "in": tpe, "fx": "pop"}] + \
           [{"k": "circle", "x": 1300, "y": 280, "r": 20 + 13 * k, "fill": "none", "c": "#c9c0b4", "w": 1.5, "in": round(tpe + .1 * k, 2)} for k in range(3)] + \
           [lab(1300, 380, "a pearl grows too", round(tpe + .3, 2), BONE, 26)]
    els += [{"k": "circle", "x": 1350, "y": 620, "r": 70, "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": round(tsc - .6, 2), "fx": "pop"},
            poly([(1480, 470), (1360, 600), (1346, 590), (1462, 458)], "#cbd2d8", "#ffffff", 1, round(tsc - .2, 2), fx="rise"),
            poly([(1480, 470), (1462, 458), (1520, 410), (1540, 426)], "#3b2a1c", "#8a6a48", 1, round(tsc - .2, 2), fx="rise"),
            ln([(1316, 586), (1384, 640)], round(tsc + .4, 2), "#ffffff", 4, dur=.5), lab(1350, 730, "steel scratches it", round(tsc + .6, 2), BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


JAR = (620, 730, 30)                  # the jar in s40: centre, base, units a centimetre (15 cm = 450 units)


def s40(C):
    """s40 · the jar in section, 15 cm tall: clay, a copper tube (9 cm), an iron rod, a bitumen seal; 1936, near Baghdad; lemon juice
    drops in; a meter on a replica swings to about 0.5 V beside a torch battery of 1.5 V (three parts, one lit)."""
    cx, base, k = JAR
    tj, tcu, tfe, tse, tju, tvo = C.at(39, "a clay jar"), C.at(39, "copper"), C.at(39, "iron"), C.at(39, "bitumen"), C.at(39, "lemon juice"), C.at(39, "half")
    els, H = jar(cx, base, k, {"jar": tj, "tube": tcu, "rod": tfe, "seal": tse})
    L = cx - 230
    els = [glow(cx, base - 220, 420, .2, .2, "lamp")] + els + [
        dimline(cx + 200, base, cx + 200, base - H, "about 15 cm", round(tj + .8, 2), GOLD, lx=26),
        lab(L, base - 8 * k + 10, "copper", round(tcu + .3, 2), "#f0b080", 28, "end"), ln([(L + 10, base - 8 * k), (cx - 1.3 * k - 4, base - 8 * k)], round(tcu + .3, 2), DIM, 1.5, dur=.3),
        lab(L, base - 11.4 * k + 10, "iron", round(tfe + .3, 2), "#c9d2d8", 28, "end"), ln([(L + 10, base - 11.4 * k), (cx - .35 * k - 4, base - 11.4 * k)], round(tfe + .3, 2), DIM, 1.5, dur=.3),
        lab(L, base - 13.2 * k + 10, "bitumen", round(tse + .3, 2), BONE, 28, "end"), ln([(L + 10, base - 13.2 * k), (cx - 2.5 * k - 4, base - 13.2 * k)], round(tse + .3, 2), DIM, 1.5, dur=.3),
        lab(cx, 785, "1936, near Baghdad", .6, GOLD, 30)]
    els += [dot(cx + 30 + 6 * (j % 2), 220 + 22 * j, 7, "#f2e27a", round(tju + .15 * j, 2)) for j in range(4)] + [lab(cx + 60, 236, "lemon juice", round(tju + .3, 2), "#f2e27a", 24, "start")]
    mx, my = 1180, 450
    els += [rect(mx - 140, my - 120, 280, 210, "#2a2622", "#cbbca8", 2, 14, round(tju + .6, 2), fx="pop"), poly(ellipse(mx, my + 30, 110, 110, 30, 200, 340), "none", BONE, 2, round(tju + .7, 2)),
            ln([(mx, my + 30), (mx - 80, my - 30)], round(tju + .8, 2), "rgba(255,255,255,.3)", 3, draw=False),
            ln([(mx, my + 30), (mx - 40, my - 62)], tvo, GOLD, 5, draw=False), lab(mx, my + 140, "replicas: about 0.5 V", round(tvo + .2, 2), GOLD, 28)]
    bx, by = 1480, 360
    els += [rect(bx, by + 100 * j, 110, 96, AMBER if j == 2 else "rgba(232,184,122,.15)", AMBER, 2, 6, round(tvo + .6 + .1 * j, 2), fx="pop") for j in range(3)] + \
           [rect(bx + 35, by - 16, 40, 16, "#cbbca8", r=3, at=round(tvo + .6, 2)), lab(bx + 55, by + 340, "a torch battery", round(tvo + .9, 2), BONE, 26),
            lab(bx + 55, by + 376, "1.5 V", round(tvo + 1.0, 2), AMBER, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s41(C):
    """s41 · a small jar with a dotted wire to a dotted plated cup, both struck out; then a jar from Seleucia in section with a rolled
    papyrus in a metal tube; a warm glow: 'a blessing?'"""
    tw, tpl, tsel, tbl = C.at(40, "no wires"), C.at(40, "electroplated"), C.at(40, "Seleucia"), C.at(40, "blessing")
    els1, _ = jar(260, 640, 20, settled=True)
    for e in els1:
        e["in"] = .3
    els = els1 + [ln([(270, 340), (400, 260), (560, 300), (640, 380)], tw, LILAC, 3, "claimed", .8, curve=True), strike(380, 240, 480, 340, round(tw + .7, 2)),
                  poly([(620, 420), (760, 420), (730, 520), (650, 520)], "none", LILAC, 3, tpl, style="claimed"), strike(640, 540, 740, 400, round(tpl + .5, 2)),
                  lab(450, 200, "no wires", round(tw + .9, 2), RED, 28), lab(700, 580, "nothing plated", round(tpl + .7, 2), RED, 28)]
    els2, _ = jar(1240, 720, 34, settled=True)
    for e in els2:
        if e.get("k") == "rect":
            continue
        e["in"] = tsel
        els.append(e)
    k = 34
    sx = 1240
    els += [rect(sx - 1.3 * k, 720 - 12.6 * k, 2.6 * k, 9 * k, "#9a8a5a", "#e2cf9e", 2, 3, round(tsel + .3, 2), fx="rise")] + \
           [ln([(sx - 26 + 8 * j, 720 - 12 * k + 10), (sx - 26 + 8 * j, 720 - 4 * k)], round(tsel + .6, 2), "#efe0b8", 3, draw=False) for j in range(7)] + \
           [lab(sx, 160, "Seleucia", round(tsel + .3, 2), GOLD, 30), lab(1490, 470, "rolled papyrus", round(tsel + .9, 2), "#efe0b8", 26, "start"),
            ln([(1480, 460), (sx + 40, 720 - 8 * k)], round(tsel + .9, 2), DIM, 1.5, dur=.3),
            glow(sx, 720 - 8 * k, 260, tbl, .55, "lamp"), lab(1490, 560, "a blessing?", round(tbl + .2, 2), GOLD, 30, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s42_late(C):
    """s42 · back on the jar: a green tick by the meter (in a lab: yes); a lilac question mark over the jar (in use: no evidence yet)."""
    cx, base, k = JAR
    ty, tq = C.at(41, "Yes"), C.at(41, "No evidence")
    return [tick(1060, 290, ty, GREEN, 1.4), lab(1100, 302, "in a lab: yes", round(ty + .2, 2), GREEN, 30, "start"),
            glow(cx - 120, 170, 90, tq, .5), lab(cx - 120, 196, "?", tq, LILAC, 70, st="big", fx="pop"),
            lab(cx - 70, 176, "in use: no evidence yet", round(tq + .3, 2), LILAC, 28, "start")]


# ================================================================ chapter 5 · the weighing
def mini(kind, x, y, at):
    """Small row pictures for the ledger."""
    if kind == "head":
        return roundhead(x, y + 40, 90, at=at)
    if kind == "bulb":
        rel, _ = relief(x - 60, y - 30, .12, settled=True)
        for e in rel:
            e["in"] = at
        return rel
    if kind == "lid":
        els, _, _ = lid(x, y - 42, 84)
        for e in els:
            e["in"] = at
            e.pop("fx", None)
        return els
    if kind == "bird":
        hb = hbird(x, y, 120)
        return [ln(hb + [hb[0]], at, "#fff2d6", 2, draw=False)]
    if kind == "sphere":
        return [{"k": "circle", "x": x, "y": y, "r": 26, "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": at},
                ln([(x - 26, y), (x, y + 6), (x + 26, y)], at, "#e2cf9e", 2.5, curve=True, draw=False)]
    els, _ = jar(x, y + 40, 5.5, settled=True)
    for e in els:
        e["in"] = at
    return els


def s43(C):
    """s43 · the ledger: six rows, each a small picture; each row lights as it is named, its chip pops as its grade is said."""
    rows = [190, 295, 400, 505, 610, 715]
    names = ["spacemen at Tassili", "a lamp at Dendera", "a rocket at Palenque", "runways at Nazca", "machined spheres", "a battery in use"]
    kinds = ["head", "bulb", "lid", "bird", "sphere", "jar"]
    anchors = ["Spacemen", "An electric lamp", "A rocket on", "Runways", "Machined", "And the Baghdad"]
    grades = [("ruled out", "Ruled out", "ruled")] * 4 + [("ruled out", "Ruled out", "ruled"), ("awaiting evidence", "Awaiting evidence", "await")]
    els = [rect(110, 130, 1560, 650, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    for k, y in enumerate(rows):
        t0 = C.at(42, anchors[k])
        els += [rect(130, y - 46, 1520, 92, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, t0, fx="pop"),
                lab(340, y + 11, names[k], round(t0 + .1, 2), BONE, 32, "start")] + mini(kinds[k], 230, y, round(t0 + .1, 2))
        tg = C.at(42, grades[k][0], lo=0) if k != 3 else C.at(42, "Runways") + 1.4
        if k == 3:
            tg = C.at(42, "Runways", lo=0) + 1.4
        els += chip(1000, y, grades[k][1], VC[grades[k][2]], round(tg, 2), 28, "start")
    to = C.at(42, "open question")
    els += chip(1250, rows[3], "Open question", VC["open"], to, 28, "start")
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s44(C):
    """s44 · a dotted saucer struck in red with a 'Ruled out' chip; below, warm and solid: a block on a sledge hauled by a crew, and a
    Round Head, each with a lilac question mark: 'open, and human'."""
    tex, tru, thu, tst, tpi = C.at(43, "explanation"), C.at(43, "Ruled"), C.at(43, "human"), C.at(43, "stones were"), C.at(43, "pictures meant")
    els = ufo(889, 230, .4, 1.6) + [glow(889, 230, 200, .4, .3, "scan"), strike(700, 300, 1080, 160, tru, RED, 8)] + chip(889, 360, "Ruled out", VC["ruled"], round(tru + .3, 2), 34)
    g = 720
    els += [rect(240, g - 90, 200, 90, "#cdb58a", "#8a6a48", 2, 3, tst), ln([(220, g + 4), (470, g + 4)], tst, "#8a6a48", 6, draw=False)] + \
           [person(560 + 50 * j, g, 90, round(tst + .1 * j, 2), "#e8d6b8") for j in range(5)] + [ln([(440, g - 50), (560, g - 70)], round(tst + .1, 2), "#c9a370", 3, draw=False),
                                                                                      lab(480, 560, "?", round(tst + .4, 2), LILAC, 80, st="big", fx="pop")]
    els += roundhead(1260, g, 300, at=tpi) + [lab(1440, 520, "?", round(tpi + .3, 2), LILAC, 80, st="big", fx="pop")]
    els += [lab(889, 790, "open, and human", thu, GOLD, 34)]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


GROUPS = [(330, "painters of Tassili"), (700, "sculptors of Dendera"), (1070, "scribes of Palenque"), (1440, "walkers of Nazca")]


def s45(C):
    """s45 · a person under the stars looks up, a small question; four groups of ancient makers at the foot; a dotted arrow lifts their
    work (tiny icons) away towards a dotted saucer."""
    tq, tgo, tel = C.at(44, "how did"), C.at(44, "hands their work"), C.at(44, "someone")
    els = [flat(), stars(70, 60, 1720, 120, 380, seed=5), stars(30, 60, 1720, 380, 520, seed=8),
           person(240, 520, 140, .4, "#e8d6b8"), ln([(250, 400), (330, 300)], .6, BONE, 1.5, "inferred", .5), lab(360, 290, "?", tq, BONE, 60, st="big", fx="pop")]
    for k, (x, t) in enumerate(GROUPS):
        at = round(tgo - 1.2 + .15 * k, 2)
        els += [person(x - 40 + 30 * j, 760, 80 + 6 * (j % 2), at, "#e8d6b8") for j in range(3)]
    els += roundhead(GROUPS[0][0], 650, 70, at=round(tgo - .8, 2))
    rel, _ = relief(GROUPS[1][0] - 60, 590, .12, settled=True)
    for e in rel:
        e["in"] = round(tgo - .7, 2)
    els += rel
    ld, _, _ = lid(GROUPS[2][0], 572, 84)
    for e in ld:
        e["in"] = round(tgo - .6, 2)
        e.pop("fx", None)
    els += ld
    hb = hbird(GROUPS[3][0], 615, 120)
    els += [ln(hb + [hb[0]], round(tgo - .5, 2), "#fff2d6", 2, draw=False)]
    els += ufo(1420, 200, round(tgo - .2, 2), 1.0)
    for k, (x, t) in enumerate(GROUPS):
        els.append(ln([(x, 545), ((x + 1420) / 2, 330 + 40 * k), (1400, 240)], round(tgo + .2 * k, 2), LILAC, 2.5, "claimed", 1.0, curve=True))
    els += [lab(1420, 140, "someone else?", round(tel + .2, 2), LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s46_late(C):
    """s46 · the dotted saucer and its arrows fade (a clean sheet over the sky, its stars drawn again); the four groups come forward with
    their names; a warm glow behind them all."""
    tn = [C.at(45, w) for w in ("painters", "sculptors", "scribes", "walkers")]
    tp = C.at(45, "People did")
    tw = round(tn[0] - .3, 2)
    els = [wipe(420, 100, 1320, 205, tw, FLAT, 1.0, .8), wipe(320, 300, 1420, 256, tw, FLAT, 1.0, .8),
           stars(40, 430, 1720, 120, 300, at=round(tw + .5, 2), seed=12), stars(24, 330, 1720, 300, 520, at=round(tw + .5, 2), seed=13)]
    for k, (x, t) in enumerate(GROUPS):
        els += [glow(x, 680, 150, tn[k], .45, "lamp"), lab(x, 806 - 20, t, round(tn[k] + .1, 2), GOLD, 26)]
    els += [glow(889, 640, 900, tp, .35, "lamp"), lab(889, 420, "People did this.", round(tp + .2, 2), BONE, 48, st="serif")]
    return els


def s47(C):
    """s47 · the test, drawn dashed (not met yet): a sealed, dated layer with an object glinting in it; an archaeologist with a camera
    and notebook; 'no ancient workshop'; three lab flasks tick in turn; an empty frame with a question mark."""
    tob, tlay, trec, twork, tlab, tfind = (C.at(46, "One made"), C.at(46, "dated layer"), C.at(46, "recorded"), C.at(46, "no ancient workshop"),
                                         C.at(46, "independent"), C.at(46, "Find that"))
    lay = [{"d": 0, "c": "#8a6a48", "t": ""}, {"d": 150, "c": "#6f5a44", "t": ""}, {"d": 300, "c": "#5a4632", "t": ""}, {"d": 430, "c": "#4a3a2c", "t": ""}]
    els = [rect(300, 300, 640, 460, "rgba(12,9,7,.25)", BONE, 2, 2, .3, style="inferred"),
           rect(304, 600, 632, 60, "rgba(242,201,142,.18)", GOLD, 2, 0, tlay, style="inferred"), lab(926, 590, "sealed, dated layer", round(tlay + .3, 2), GOLD, 26, "end"),
           rect(600, 616, 60, 28, "none", AU, 3, 4, tob, style="inferred"), glow(630, 630, 80, tob, .6, "lamp"),
           person(380, 300, 170, round(trec - .3, 2), "#1a1511"), rect(410, 180, 44, 30, "#2a2622", "#cbd2d8", 2, 4, trec), glow(432, 194, 60, trec, .7, "lamp"),
           lab(470, 160, "recorded as dug", round(trec + .3, 2), BONE, 26, "start")]
    ax, ay = 1100, 260
    els += [rect(ax, ay, 120, 40, "none", LILAC, 3, 4, twork, style="inferred"), rect(ax + 30, ay + 40, 60, 50, "none", LILAC, 3, 4, twork, style="inferred"),
            strike(ax - 10, ay + 100, ax + 130, ay - 10, round(twork + .4, 2)), lab(ax + 60, ay - 24, "no workshop could make it", round(twork + .3, 2), LILAC, 26)]
    for j in range(3):
        fx_, fy_ = 1120 + 160 * j, 600
        at = round(tlab + .35 * j, 2)
        els += [poly([(fx_ - 18, fy_ - 90), (fx_ + 18, fy_ - 90), (fx_ + 18, fy_ - 50), (fx_ + 50, fy_), (fx_ - 50, fy_), (fx_ - 18, fy_ - 50)], "rgba(159,208,255,.15)", BLUE, 2.5, at,
                     style="inferred"), tick(fx_, fy_ - 130, round(at + .3, 2), GREEN, 1.0)]
    els += [lab(1280, 660, "independent labs", round(tlab + 1.0, 2), BLUE, 28)]
    els += [rect(1480, 160, 160, 160, "none", BONE, 2.5, 10, tfind, style="inferred"), lab(1560, 270, "?", round(tfind + .2, 2), BONE, 80, st="big", fx="pop"),
            lab(1560, 360, "not found yet", round(tfind + .4, 2), DIM, 26)]
    return {"base": "section", "tod": "night", "ground": 300, "lx": 40, "layers": lay, "cam": CAM, "els": els}


def s48(C):
    """s48 · the close: the lid at Palenque once more (settled), framed on the king and the tree, his name beside him; a lamp warms it."""
    cx, top, H = 889, 140, 660
    els, (x0, y0, W, Hh), F = lid(cx, top, H)
    tk = C.at(47, "name", lo=.5)
    return {"base": "dark", "cam": [1.18, 889, 520], "els": [glow(cx, 480, 600, -1, .2, "lamp")] + els + [
        glow(F(.45, .66)[0], F(.45, .66)[1], 260, 1.0, .55, "lamp"), glow(cx, y0 + 12, 200, round(tk, 2), .45, "lamp"),
        lab(x0 - 40, 380, "K'inich Janaab Pakal", round(tk + .2, 2), GOLD, 30, "end"), lab(x0 - 40, 420, "603 to 683 CE", round(tk + .4, 2), DIM, 26, "end")]}


# ================================================================ assembly
def _tagged(cams):
    """Each alias camera gets a tiny unique extra zoom (invisible), so its step can be found after the wall is built."""
    out = {}
    for k, i in enumerate(sorted(cams)):
        z, x, y = cams[i]
        out[i] = [round(z + .0003 * (k + 1), 4), x, y]
    return out


def _attach(ep, cams, late):
    """Give each alias step its additions: a panel item on that step (built once, shown from the start of its glide, timed on its clock)."""
    panels = ep["wall"]["panels"]
    for i, els in late.items():
        z = cams[i][0]
        ks = [k for k, s in enumerate(ep["shots"]) if abs(s["cam"][0] - z) < 1e-9]
        assert len(ks) == 1, ("alias step", i, ks)
        k = ks[0]
        cx, cy = ep["shots"][k]["cam"][1:]
        js = [j for j, p in enumerate(panels) if p["ox"] <= cx <= p["ox"] + p.get("w", W_) and p["oy"] <= cy <= p["oy"] + p.get("h", H_)]
        assert len(js) == 1, ("panel of alias", i, js)
        p = panels[js[0]]
        ep["shots"][k]["els"].append({"k": "panel", "ox": p["ox"], "oy": p["oy"], "w": p.get("w", W_), "h": p.get("h", H_), "base": "none", "els": list(els), "pn": js[0]})
    return ep


def description():
    d = SCRIPT["description"]
    a = d.index("Chapters\n") + len("Chapters\n")
    b = d.index("\n\nSources")
    return d[:a] + "{chapters}" + d[b:]


def lf_ancient_astronauts():
    beats = BEATS()
    C = Clock(beats)
    scenes = {0: s01, 1: s02, 2: s03, 4: s05, 5: s06, 6: s07, 7: s08, 9: s10, 10: s11, 11: s12, 12: s13, 13: s14, 14: s15, 15: s16,
              17: s18, 18: s19, 19: s20, 20: s21, 21: s22, 22: s23, 23: s24, 24: s25, 25: s26, 27: s28, 28: s29,
              29: s30, 30: s31, 31: s32, 32: s33, 34: s35, 35: s36, 36: s37, 37: s38, 38: s39, 39: s40, 40: s41,
              42: s43, 43: s44, 44: s45, 46: s47, 47: s48}
    lates = {8: s09_late, 16: s17_late, 26: s27_late, 33: s34_late, 41: s42_late, 45: s46_late}
    shots = []
    for i in range(48):
        shots.append(scenes[i](C) if i in scenes else {"base": "dark", "cam": CAM, "els": []})
    cams = _tagged(ALIAS_CAMS)
    late = {i: f(C) for i, f in lates.items()}
    ep = {"id": "lf-ancient-astronauts", "code": "LF.09", "series": "The Method", "title": "Ancient Astronauts: Six Clues, Weighed", "case": "ancient-astronauts",
          "verdict": "debunked", "claim": "Did visitors from space help ancient peoples make their art and monuments?", "mood": "mystery",
          "hook_text": "Did visitors from *space* help the ancients?", "beats": beats, "shots": shots,
          "sources": "Sakai et al. 2024 (doi:10.1073/pnas.2407652121) · Keenan 2002 (doi:10.1179/pua.2002.2.3.131) · Mercier et al. 2012 (doi:10.1016/j.quageo.2011.11.010) · "
                     "Waitkus 2002, SAK 30 · Nickell 1983, Skeptical Inquirer 7(3) · Eggert 1996, Skeptical Inquirer 20(3) · Stuart & Stuart 2008 · von Däniken 1968",
          "post": "A Martian god in the Sahara, a light bulb in an Egyptian crypt, a rocket on a Maya king's lid, runways in Peru, grooved spheres three billion years old "
                  "and an ancient battery: the six famous clues of the ancient astronaut theory, weighed one by one, and the real makers given their credit back.",
          "hashtags": ["#AncientAliens", "#AncientAstronauts", "#Archaeology", "#Nazca", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": "Ancient Astronauts", "yt_title": SCRIPT["yt_title"], "description": description(),
          "end_line": "At Palenque, a king still rests beneath his tree, his name carved beside him."}
    out = remix(ep, alias=dict(ALIAS), cams=cams)
    return _attach(out, cams, late)


def EPISODES():
    return [lf_ancient_astronauts()]
