"""LF.09 · The Method · Ancient Astronauts: Six Clues, Weighed (16:9 long film, one wall).

Script: films/long/lf-ancient-astronauts/script.json. Its lines are read from there, word for word; this module only adds the
[go:N|t] markers where the picture changes (see BEATS). One shot per script shot s1..s48 (ep shot index = s number - 1), plus three
alias shots that let a picture build across sentences: 50 (s1's second sentence: the lid's parts light up as named), 48 and 49 (s2's
Egypt and Peru exhibits, each on its own line).
Facts: the script's facts_added and sources (von Däniken 1968 and his 2026 obituaries; Lhote 1958, Keenan 2000/2002,
Mercier et al. 2012, Soukopova 2012 for Tassili; Waitkus 1997/2002, Feder 2014, Weeks 1998 for Dendera; Ruz 1973, Schele &
Freidel 1990, Stuart & Stuart 2008 for Palenque; Nickell 1983, Sakai et al. 2024 for Nazca; Heinrich 2008 for Klerksdorp;
König 1938, Eggert 1996 for the Baghdad jar), and the Shorts 'ancient-astronauts', 'tassili', 'ooparts', 'power-plant'.

Drawings are schematic and true to the numbers said: solid = evidence, dashed = inferred, dotted lilac = claimed (every
saucer, helmet, rocket, runway and 'bulb' is drawn dotted). Gods are named, never drawn as beings; the Maya king appears
only as his carved image. Scales: the lid 3.8 by 2.2 m (drawn upright) beside a 1.7 m person; the Round Head about three people tall beside
its copyist; the hummingbird 93 m against a 100 m bar with a 1.7 m person; Nickell's condor 134 m; the statue of Harsomtus
four palms (30 cm) against its ruler; the spheres 0.5 to 10 cm against a 10 cm ruler; the jar 15 cm with its 9 cm tube;
deep time from 3 billion years ago to today on one bar.

Engine workaround (as in lf_gobekli.py / lf_atlantis.py): the wall only adds elements to a panel on its first visit, at a beat
start or a line start. A shot that returns to a panel mid-line (or with additions) is an alias of that panel whose camera zoom
carries a tiny unique tag (+0.0003 per tag, invisible); after the wall is built, the step that reached that camera gets the
shot's additions as a panel item, built on that step's clock (_attach). Long scenes are handed on sentence by sentence the same way
(SPLITS, _split): same moments in the film, but each step opens on something new.
Kit notes: a line built with fx 'draw' shows its round cap as a dot at its start from its step's first frame, so strikes, ticks and
thick lines here fade or pop in instead; person() ignores 'op' (faint figures use the 'lib' element).

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
    """A tick that pops in (a drawn line shows its round cap as a dot at its start from the step's first frame)."""
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "pop", "dur": .45, "in": at}


def strike(x0, y0, x1, y1, at=0, c=RED, w=6):
    """A strike-through that fades in quickly (illus.strike draws it, and a drawn line's round cap shows as a dot before it is drawn)."""
    return {"k": "line", "p": [[round(x0, 1), round(y0, 1)], [round(x1, 1), round(y1, 1)]], "c": c, "w": w, "in": at, "dur": .3}


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
LID_RATIO = 2.2 / 3.8                 # Pakal's lid: about 3.8 m long and 2.2 m wide (drawn upright, the bird at the top)


LID_B = .075                          # its sky band: a fraction of the lid's width


LID_A = (1 / LID_RATIO - 2 * LID_B) / (1 - 2 * LID_B)    # the carved field: its height in field widths (about 1.86)
def _ell(x, y, rx, ry, n=16):
    return [(x + rx * math.cos(2 * math.pi * k / n), y + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


def _cr(pts, n=8):
    """Points along the smooth open curve the kit draws through pts (Catmull-Rom as cubic Beziers)."""
    out, m = [tuple(pts[0])], len(pts)
    for i in range(m - 1):
        p0, p1, p2, p3 = pts[max(0, i - 1)], pts[i], pts[i + 1], pts[min(m - 1, i + 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        for k in range(1, n + 1):
            s = k / n
            a, b, c, d = (1 - s) ** 3, 3 * (1 - s) ** 2 * s, 3 * (1 - s) * s * s, s ** 3
            out.append((a * p1[0] + b * c1[0] + c * c2[0] + d * p2[0], a * p1[1] + b * c1[1] + c * c2[1] + d * p2[1]))
    return out


def _lobe(b, t, w):
    """A feather or petal from base b to tip t, w wide near its base (closed outline, drawn smooth)."""
    (bx, by), (tx, ty) = b, t
    L = math.hypot(tx - bx, ty - by) or 1
    ux, uy = (tx - bx) / L, (ty - by) / L
    nx, ny = -uy, ux
    side = [(0, .5), (.45, .62), (.82, .42)]
    return [(bx + ux * L * f + nx * w * q, by + uy * L * f + ny * w * q) for f, q in side] + [(tx, ty)] + \
           [(bx + ux * L * f - nx * w * q, by + uy * L * f - ny * w * q) for f, q in reversed(side)]


def _lid_parts():
    """Pakal's lid carving in field units (x 0..1 across the carved field, y 0..LID_A down it, the bird at the top), after Merle
    Greene Robertson's drawing, simplified: the Principal Bird on top; the cross-shaped World Tree, its branch ends square-snouted
    serpent heads, a jewelled double-headed serpent draped in its branches; the king reclining at its foot (head back at the left,
    face turned up, a knee raised, a jade net skirt) on the head of the earth monster; the open jaws of the underworld round the
    bottom; a few floating signs. {part: (raised faces, incised details)}."""
    Mx = lambda pts: [(1 - x, y) for x, y in pts]
    ID = lambda pts: pts
    P = {}
    f, i = [], []                                                    # the bird
    for k in range(4):
        lo = _lobe((.448, .165 + .02 * k), (.105 + .028 * k, .07 + .06 * k), .052 - .005 * k)
        f += [("poly", lo, True), ("poly", Mx(lo), True)]
    for b, tp in (((.478, .262), (.405, .392)), ((.46, .255), (.36, .358))):
        lo = _lobe(b, tp, .034)
        f += [("poly", lo, True), ("poly", Mx(lo), True)]
    f.append(("oval", (.5, .205), .085, .075))
    for tp in ((.585, .018), (.616, .05), (.606, .09)):
        f.append(("poly", _lobe((.5, .082), tp, .03), True))
    f += [("disc", (.478, .108), .052), ("poly", [(.44, .086), (.39, .098), (.336, .126), (.33, .146), (.392, .133), (.446, .127)], True)]
    i += [("disc", (.484, .1), .011), ("ring", (.5, .212), .032, .008), ("line", [(.44, .125), (.395, .118)], .006, False)]
    P["bird"] = (f, i)
    f, i = [], []                                                    # the World Tree and the serpent in its branches
    f += [("poly", [(.468, .255), (.532, .255), (.549, 1.43), (.451, 1.43)], False),
          ("poly", [(.115, .624), (.5, .613), (.885, .624), (.9, .69), (.5, .70), (.1, .69)], True)]
    for S in (ID, Mx):
        f += [("poly", S([(.022, .566), (.094, .548), (.136, .612), (.132, .706), (.058, .722), (.014, .668)]), True),
              ("line", S([(.05, .566), (.028, .5), (.063, .458), (.106, .472), (.1, .512)]), .026, True),
              ("line", S([(.125, .735), (.2, .802), (.29, .838), (.38, .818), (.452, .778)]), .03, True),
              ("disc", S([(.118, .748)])[0], .036),
              ("line", S([(.29, .845), (.292, .905)]), .011, False), ("disc", S([(.292, .913)])[0], .017)]
        i += [("ring", S([(.074, .632)])[0], .021, .008), ("line", S([(.026, .678), (.1, .684)]), .008, False),
              ("ring", S([(.112, .745)])[0], .012, .006)]
    f.append(("disc", (.5, .657), .07))
    i += [("ring", (.5, .657), .045, .009), ("disc", (.5, .657), .017), ("oval", (.5, .44), .018, .036), ("oval", (.5, .985), .018, .036),
          ("oval", (.5, 1.2), .016, .03), ("oval", (.3, .657), .032, .016), ("oval", (.7, .657), .032, .016)]
    P["tree"] = (f, i)
    spots = ((.115, .40), (.885, .40), (.13, .885), (.87, .885), (.885, 1.06))     # floating signs (sun flowers)
    P["signs"] = ([("poly", [(x + (.03 if k % 2 == 0 else .013) * math.cos(math.pi * k / 4), y + (.03 if k % 2 == 0 else .013) * math.sin(math.pi * k / 4))
                              for k in range(8)], True) for x, y in spots], [("disc", (x, y), .007) for x, y in spots])
    hc = (.258, 1.078)                                               # the king: head back at the left, face turned up to the tree
    f = [("poly", _lobe((.235, 1.03), (.118, .968), .05), True), ("poly", _lobe((.228, 1.045), (.112, 1.012), .042), True),       # feathers of the headdress
         ("poly", _lobe((.226, 1.06), (.13, 1.055), .036), True),
         ("disc", hc, .06),
         ("poly", [(.25, 1.018), (.29, 1.02), (.314, 1.03), (.308, 1.05), (.321, 1.063), (.314, 1.074), (.32, 1.088), (.303, 1.114), (.27, 1.124),
                   (.255, 1.08)], True),                                                                                                 # the face in profile
         ("poly", [(.205, 1.066), (.208, 1.03), (.232, 1.006), (.27, .996), (.296, 1.006), (.285, 1.022), (.25, 1.026), (.228, 1.05)], True),   # headband
         ("line", [(.282, 1.0), (.3, .972)], .02, False), ("line", [(.3, .972), (.32, .947), (.304, .928), (.324, .906)], .011, True),     # forehead ornament
         ("line", [(.268, 1.12), (.29, 1.15)], .048, False),                                                                                # neck
         ("poly", [(.262, 1.142), (.33, 1.147), (.385, 1.212), (.432, 1.298), (.424, 1.345), (.345, 1.366), (.29, 1.292), (.255, 1.205)], True),
         ("line", [(.322, 1.19), (.372, 1.278), (.442, 1.212)], .038, False),                                                             # arm, hand raised
         ("poly", [(.432, 1.226), (.448, 1.18), (.474, 1.162), (.484, 1.182), (.47, 1.21), (.452, 1.232)], True),
         ("line", [(.56, 1.392), (.70, 1.457)], .042, False), ("poly", [(.69, 1.44), (.79, 1.452), (.787, 1.476), (.69, 1.474)], True),  # far leg
         ("poly", [(.345, 1.305), (.442, 1.293), (.506, 1.37), (.482, 1.458), (.37, 1.452), (.322, 1.382)], True),                       # jade net skirt
         ("line", [(.462, 1.372), (.636, 1.226)], .064, False), ("disc", (.636, 1.226), .033),                                            # raised knee
         ("line", [(.636, 1.226), (.667, 1.415)], .05, False), ("poly", [(.646, 1.398), (.738, 1.422), (.742, 1.447), (.648, 1.443)], True)]
    i = [("ring", (.238, 1.086), .018, .007), ("disc", (.296, 1.046), .0075), ("line", [(.302, 1.095), (.315, 1.093)], .005, False),   # ear flare, eye, mouth
         ("line", [(.21, 1.04), (.29, 1.012)], .006, True), ("line", [(.413, 1.206), (.447, 1.241)], .008, False),
         ("line", [(.646, 1.388), (.69, 1.386)], .009, False), ("ring", (.352, 1.214), .012, .006)] + \
        [("disc", (.298 + .019 * k, 1.152 + .0115 * k + .001 * k * k), .0085) for k in range(5)] + \
        [("line", p, .006, False) for p in ([(.35, 1.33), (.42, 1.44)], [(.39, 1.31), (.47, 1.43)], [(.43, 1.30), (.49, 1.39)],
                                            [(.34, 1.40), (.43, 1.30)], [(.37, 1.44), (.47, 1.32)], [(.42, 1.45), (.495, 1.36)])]
    P["king"] = (f, i)
    P["monster"] = ([("poly", [(.27, 1.472), (.36, 1.446), (.5, 1.44), (.64, 1.452), (.712, 1.492), (.704, 1.572), (.62, 1.616), (.45, 1.626), (.32, 1.602),
                                (.255, 1.546)], True), ("line", [(.27, 1.5), (.222, 1.488), (.205, 1.53), (.236, 1.552)], .022, True)],
                    [("ring", (.385, 1.517), .034, .009), ("disc", (.385, 1.517), .013), ("line", [(.33, 1.488), (.385, 1.468), (.44, 1.486)], .008, True),
                     ("line", [(.45, 1.585), (.48, 1.606), (.51, 1.585), (.54, 1.606), (.57, 1.585), (.6, 1.606), (.63, 1.585)], .007, False)])
    Lj = [(.08, 1.165), (.056, 1.30), (.074, 1.46), (.15, 1.632), (.29, 1.756), (.5, 1.80)]       # the jaws of the underworld
    tip = [(.08, 1.172), (.098, 1.118), (.15, 1.112), (.166, 1.16), (.128, 1.19)]
    f = [("line", Lj, .078, True), ("line", Mx(Lj), .078, True), ("line", tip, .042, True), ("line", Mx(tip), .042, True)]
    d = _cr(Lj, 12)
    cum = [0.0]
    for a, b in zip(d, d[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    for q in (.13, .24, .35, .46, .57, .68, .79, .90):
        s = q * cum[-1]
        j = max(1, next(k for k, c in enumerate(cum) if c >= s))
        (ax, ay), (bx, by) = d[j - 1], d[j]
        L = math.hypot(bx - ax, by - ay) or 1
        tx, ty = (bx - ax) / L, (by - ay) / L
        nx, ny = -ty, tx
        if nx * (.5 - ax) + ny * (1.42 - ay) < 0:
            nx, ny = -nx, -ny
        h = .062 if q < .3 else .048
        cx, cy = ax + nx * .034, ay + ny * .034
        tri = [(cx - tx * .021, cy - ty * .021), (cx + nx * h, cy + ny * h), (cx + tx * .021, cy + ty * .021)]
        f += [("poly", tri, False), ("poly", Mx(tri), False)]
    P["jaws"] = (f, [("ring", (.072, 1.31), .02, .007), ("ring", (.928, 1.31), .02, .007)])
    return P


LID_PARTS = _lid_parts()


LID_ORDER = ("tree", "signs", "jaws", "monster", "king", "bird")


LID_FRONT = {"tree": ("king", "bird"), "monster": ("king",), "signs": (), "jaws": (), "king": (), "bird": ()}


def _shape(sp, P, fw, col, at, dx=0.0, dy=0.0, op=None):
    """One carving shape (field units) as a kit element in colour col."""
    k = sp[0]
    Q = lambda pts: [(P(x, y)[0] + dx, P(x, y)[1] + dy) for x, y in pts]
    if k == "poly":
        return poly(Q(sp[1]), col, at=at, curve=sp[2], op=op)
    if k == "line":
        return ln(Q(sp[1]), at, col, max(.8, round(sp[2] * fw, 1)), curve=sp[3], draw=False, op=op)
    if k == "oval":
        return poly(Q(_ell(sp[1][0], sp[1][1], sp[2], sp[3])), col, at=at, curve=True, op=op)
    x, y = P(*sp[1])
    e = {"k": "circle", "x": round(x + dx, 1), "y": round(y + dy, 1), "r": round(max(.6, sp[2] * fw), 1), "in": at}
    if k == "disc":
        e.update(fill=col, c="none", w=0)
    else:
        e.update(fill="none", c=col, w=max(.8, round(sp[3] * fw, 1)))
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def _sign(k, x, y, r, at, c="#d6caae"):
    """A small sky-band sign in a glyph block: sun flower, moon, star, crossed bands, darkness, three dots."""
    w = max(1.0, round(r * .32, 1))
    if k == 0:
        return poly([(x + (r if j % 2 == 0 else r * .42) * math.cos(math.pi * j / 4), y + (r if j % 2 == 0 else r * .42) * math.sin(math.pi * j / 4)) for j in range(8)],
                    c, at=at, curve=True)
    if k == 1:
        return poly([(x + r * math.cos(a), y + r * math.sin(a)) for a in [math.pi * (.35 + 1.3 * j / 8) for j in range(9)]] +
                    [(x - r * .25 + r * .7 * math.cos(a), y + r * .7 * math.sin(a)) for a in [math.pi * (1.65 - 1.3 * j / 8) for j in range(9)]], c, at=at, curve=True)
    if k == 2:
        return {"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r * .8, 1), "fill": "none", "c": c, "w": w, "in": at}
    if k == 3:
        return ln([(x - r * .8, y - r * .8), (x + r * .8, y + r * .8), (x, y), (x + r * .8, y - r * .8), (x - r * .8, y + r * .8)], at, c, w, draw=False)
    if k == 4:
        return ln([(x - r, y + r * .25), (x - r * .5, y - r * .35), (x, y + r * .25), (x + r * .5, y - r * .35), (x + r, y + r * .25)], at, c, w, curve=True, draw=False)
    return ln([(x - r * .8, y), (x + r * .8, y)], at, c, round(r * .55, 1), draw=False, dash="0.1 %.1f" % (r * .8))


def _band(x0, y0, W, H, b, at):
    """The sky band round the carving: glyph blocks all the way round, each with a small sign."""
    s = b * .8
    def run(ax, ay, bx, by):
        n = max(2, int(round(math.hypot(bx - ax, by - ay) / (b * 1.06))))
        return [(ax + (bx - ax) * (k + .5) / n, ay + (by - ay) * (k + .5) / n) for k in range(n)]
    cells = run(x0 + b, y0 + b / 2, x0 + W - b, y0 + b / 2) + run(x0 + b, y0 + H - b / 2, x0 + W - b, y0 + H - b / 2) + \
        run(x0 + b / 2, y0 + b, x0 + b / 2, y0 + H - b) + run(x0 + W - b / 2, y0 + b, x0 + W - b / 2, y0 + H - b) + \
        [(x0 + b / 2, y0 + b / 2), (x0 + W - b / 2, y0 + b / 2), (x0 + b / 2, y0 + H - b / 2), (x0 + W - b / 2, y0 + H - b / 2)]
    out = []
    for k, (x, y) in enumerate(cells):
        out += [rect(x - s / 2, y - s / 2, s, s, "#93876f", "#4a4135", max(1.0, round(s * .06, 1)), round(s * .2, 1), at), _sign((k * 5) % 6, x, y, s * .3, at)]
    return out


CARVE_F, CARVE_SH, CARVE_IN, CARVE_LIT = "#ddd1b6", "#2c241c", "#5a4e3f", "#fff4dc"
SLAB, SLAB_F, SLAB_SIDE = "#a3977f", "#8b806b", "#564d41"


def lid(cx, top, H, t=None, flames=False, carving_only=False, parts=None, icon=False):
    """Pakal's sarcophagus lid drawn upright (the bird at the top), schematic but true to the real one (about 3.8 by 2.2 m): a slab with
    its thickness and a sky band of glyph blocks round a recessed field, the carving in raised relief (lit from the top left, each
    shape with its shadow; see _lid_parts). t: build times {slab, border, tree, signs, jaws, monster, king, bird, flames}, a missing
    key = -1 (there from the start). parts: only those carving parts (no slab). icon: small and plain (no shadows, signs or band).
    Returns elements, (x0, y0, W, H), F with F(u, v) = a point of the carved field (u, v in 0..1)."""
    t = t or {}
    T = lambda k: t.get(k, -1)
    W = H * LID_RATIO
    x0, y0 = cx - W / 2, top
    b = W * LID_B
    fx0, fy0, fw, fh = x0 + b, y0 + b, W - 2 * b, H - 2 * b
    F = lambda u, v: (fx0 + u * fw, fy0 + v * fh)
    P = lambda x, y: (fx0 + x * fw, fy0 + y * fw)
    els = []
    whole = parts is None and not carving_only
    if whole:
        ts = T("slab")
        d = W * .045
        els += [poly([(x0 + W, y0 + d * .4), (x0 + W + d, y0 + d), (x0 + W + d, y0 + H + d * .3), (x0 + W, y0 + H)], SLAB_SIDE, "rgba(255,236,206,.16)", 1, ts),
                rect(x0, y0, W, H, SLAB, "#d9ceb5", max(1.0, round(W * .005, 1)), round(W * .012, 1), ts),
                rect(fx0, fy0, fw, fh, SLAB_F, at=ts)]
        if not icon:
            els += [ln([(fx0, fy0 + fh), (fx0, fy0), (fx0 + fw, fy0)], ts, "#3a3128", round(max(1.5, W * .008), 1), draw=False, op=.75),
                    ln([(fx0 + fw, fy0), (fx0 + fw, fy0 + fh), (fx0, fy0 + fh)], ts, "#d4c8ad", round(max(1.0, W * .004), 1), draw=False, op=.6)]
            els += _band(x0, y0, W, H, b, T("border"))
        else:
            els.append(rect(x0 + b * .5, y0 + b * .5, W - b, H - b, "none", "#5e5446", max(1.0, round(b * .3, 1)), 2, ts))
    off = fw * .009
    for name in (parts or LID_ORDER):
        if icon and name == "signs":
            continue
        face, inc = LID_PARTS[name]
        at = T(name)
        if not icon:
            els += [_shape(sp, P, fw, CARVE_SH, at, off, off * 1.25, .6) for sp in face]
        els += [_shape(sp, P, fw, CARVE_F, at) for sp in face]
        if not icon:
            els += [_shape(sp, P, fw, CARVE_IN, at) for sp in inc]
    if whole and not icon:
        els.append(rect(x0, y0, W, H, "url(#k-shade)", at=T("slab")))
    if flames:
        els += lid_flames(cx, top, H, T("flames"))
    return els, (x0, y0, W, H), F


def lid_flames(cx, top, H, at):
    """The claimed reading, drawn dotted in lilac: flames licking up under the king (they are the jaws of the underworld)."""
    W = H * LID_RATIO
    b = W * LID_B
    fx0, fy0, fw = cx - W / 2 + b, top + b, W - 2 * b
    P = lambda x, y: (fx0 + x * fw, fy0 + y * fw)
    out = []
    for k, x in enumerate((.34, .42, .5, .58, .66)):
        h = .3 if k in (1, 3) else .24
        pts = [P(x, 1.745), P(x - .028, 1.745 - h * .3), P(x + .022, 1.745 - h * .6), P(x - .016, 1.745 - h * .85), P(x + .01, 1.745 - h)]
        out.append(ln(pts, round(at + .12 * k, 2), LILAC, round(max(2.0, fw * .014), 1), "claimed", curve=True, draw=False))
    return out


def lid_lights(cx, top, H, t):
    """The parts of the lid catching the light as they are named: a warm glow over each, the part redrawn bright on top (and the parts
    in front of it redrawn over it, so the relief keeps its layers). t: {part: time}."""
    W = H * LID_RATIO
    b = W * LID_B
    fx0, fy0, fw = cx - W / 2 + b, top + b, W - 2 * b
    P = lambda x, y: (fx0 + x * fw, fy0 + y * fw)
    centre = {"king": ((.47, 1.25), .5), "tree": ((.5, .66), .62), "bird": ((.5, .17), .5), "monster": ((.48, 1.53), .34), "jaws": ((.5, 1.6), .62)}
    off = fw * .009
    def draw(name, at, col, dur, shadow=False):
        face, inc = LID_PARTS[name]
        out = [_shape(sp, P, fw, CARVE_SH, at, off, off * 1.25, .6) for sp in face] if shadow else []
        out += [_shape(sp, P, fw, col, at) for sp in face] + [_shape(sp, P, fw, CARVE_IN, at) for sp in inc]
        for e in out:
            e["dur"] = dur
        return out
    out, lit = [], {}
    for name in sorted(t, key=t.get):
        at = round(t[name], 2)
        (gx, gy), gr = centre[name]
        x, y = P(gx, gy)
        out.append(glow(round(x, 1), round(y, 1), round(gr * fw, 1), at, .55, "lamp"))
        out += draw(name, at, CARVE_LIT, .9)
        lit[name] = at
        for fr in LID_FRONT[name]:
            out += draw(fr, at, CARVE_LIT, .05) if fr in lit else draw(fr, at, CARVE_F, .05, True)
    return out


def rocket_over(F, at):
    """The claimed rocket, dotted, laid over the carving: a nose at the bird, a body round the tree, a cockpit round the king, fins at
    its sides, exhaust where the jaws are."""
    A = LID_A
    G = lambda x, y: F(x, y / A)
    body = [G(.5, -.02), G(.64, .12), G(.72, .4), G(.74, 1.4), G(.26, 1.4), G(.28, .4), G(.36, .12)]
    out = [poly(body, "rgba(201,193,238,.06)", LILAC, 5, at, style="claimed"),
           poly([G(.27, 1.0), G(.08, 1.5), G(.27, 1.36)], "none", LILAC, 5, round(at + .4, 2), style="claimed"),
           poly([G(.73, 1.0), G(.92, 1.5), G(.73, 1.36)], "none", LILAC, 5, round(at + .4, 2), style="claimed"),
           poly([(G(.42, 1.22)[0] + 70 * math.cos(a), G(.42, 1.22)[1] + 58 * math.sin(a)) for a in [2 * math.pi * k / 24 for k in range(24)]], "none", LILAC, 4,
                round(at + .7, 2), style="claimed")]
    for k, u in enumerate((.36, .45, .55, .64)):
        out.append(ln([G(u, 1.44), G(u + (u - .5) * .5, 1.76)], round(at + .9 + .1 * k, 2), LILAC, 5, "claimed", draw=False))
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
    """The Nazca hummingbird as one continuous line (plan), L long from beak tip to tail and 0.71 L across the wings (93 m by 66 m),
    beak pointing along -u: a long straight beak, a small head, wings spread straight out ending in four long feathers each, a slender
    body and a fanned tail. Centre (cx, cy) at mid-length; rot turns it (radians, 0 = beak to the left)."""
    up = [(0, 0), (.27, .006), (.285, .022), (.31, .032), (.345, .03), (.36, .034), (.4, .04), (.385, .15), (.37, .262),
          (.36, .335), (.372, .352), (.384, .338), (.39, .268), (.398, .34), (.412, .356), (.422, .338), (.428, .27), (.436, .342), (.45, .356),
          (.46, .338), (.466, .268), (.474, .338), (.488, .352), (.498, .332), (.505, .262), (.52, .15), (.525, .042), (.6, .036), (.72, .032),
          (.8, .03), (.94, .12), (.975, .112), (.965, .09), (.9, .06), (.985, .055), (.99, .038), (.93, .012)]
    pts = up + [(u, -v) for u, v in reversed(up[1:])]
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

    def at(self, i, phrase, lo=.4, d=0.0, after=0.0):
        bi, t0 = self.start[i]
        want = [_norm(x) for x in phrase.split()]
        ws = self.words[bi]
        for k in range(len(ws)):
            if ws[k][1] >= t0 + after - 1e-6 and [w for w, _ in ws[k:k + len(want)]] == want:
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
        B("hook", 0, lines_of(0, 0, [(0, "On it, a man", 50, 1.4), (1, None, 1, 1.4), (1, "In Egypt", 48, 1.4), (1, "In Peru", 49, 1.4), (2, None, 2, 1.4)])),
        B("title", 3, lines_of(0, 1), intro=True),
        B("world", 4, lines_of(0, 2, [(1, None, 5, 1.4), (1, "By December", 6, 1.4), (2, None, 7, 1.4), (2, "American television", 51, 1.4), (2, "Today, Ancient", 52, 1.4),
                                      (3, None, 8, .8), (3, "His clues are still", 9, 1.6)])),
        B("world", 10, lines_of(1, 0), chapter=C[1]),
        B("collision", 11, lines_of(1, 1, [(0, "In one shelter", 53, 1.4), (0, "Lhote nicknamed", 54, 1.4), (1, None, 12, 1.4)])),
        B("reversal", 13, lines_of(1, 2, [(1, None, 14, 1.4)])),
        B("cost", 15, lines_of(1, 3)),
        B("tag", 16, lines_of(1, 4)),
        B("world", 17, lines_of(2, 0), chapter=C[2]),
        B("collision", 18, lines_of(2, 1, [(1, None, 19, 1.4)])),
        B("reversal", 20, lines_of(2, 2, [(0, "The crypt was a", 21, 1.4), (1, None, 22, 1.4)])),
        B("world", 23, lines_of(2, 3, [(0, "In {1952", 24, 1.4), (0, "On its great stone lid", 25, 1.4)])),
        B("reversal", 26, lines_of(2, 4, [(1, None, 27, 1.4), (1, "In a temple nearby", 55, 1.4), (2, None, 28, 1.4)])),
        B("world", 29, lines_of(3, 0), chapter=C[3]),
        B("collision", 30, lines_of(3, 1)),
        B("cost", 31, lines_of(3, 2)),
        B("reversal", 32, lines_of(3, 3, [(0, "With five relatives", 56, 1.4), (0, "Plotting it took", 33, .8), (1, None, 34, 1.4), (1, "What the giant lines", 35, 1.4)])),
        B("world", 36, lines_of(4, 0), chapter=C[4]),
        B("collision", 37, lines_of(4, 1)),
        B("reversal", 38, lines_of(4, 2)),
        B("world", 39, lines_of(4, 3, [(0, "Inside, a copper", 57, 1.4), (0, "Fill it with", 58, 1.4)])),
        B("reversal", 40, lines_of(4, 4)),
        B("tag", 41, lines_of(4, 5)),
        B("weigh", 42, lines_of(5, 0, [(1, None, 43, 1.4)]), chapter=C[5]),
        B("reversal", 44, lines_of(5, 1, [(0, "Because the question", 59, 1.4), (0, "And because the past", 60, 1.4), (0, "But the theory", 61, 1.4), (1, None, 45, .8)])),
        B("test", 46, lines_of(5, 2)),
        B("close", 47, lines_of(5, 3)),
    ]


ALIAS = {3: 2, 8: 7, 16: 12, 26: 25, 33: 32, 41: 39, 45: 44, 48: 1, 49: 1, 50: 0}     # 48, 49: the gallery's 2nd and 3rd exhibits; 50: the lid's parts
SPLITS = {7: (51, 52), 11: (53, 54), 27: (55,), 32: (56,), 39: (57, 58), 44: (59, 60, 61)}   # long scenes handed on sentence by sentence (_split)
for _b, _cuts in SPLITS.items():
    ALIAS.update({_a: _b for _a in _cuts})
ALIAS_CAMS = {i: [1, 889, 500] for i in ALIAS}


# ================================================================ chapter 0 · opening: the lid, the exhibits, the question, the history
LID0 = (1198, 134, 648)               # the hook's lid: centre x, top, height (648 units = 3.8 m: about 170 units a metre)


def _vault(ax, top=104, half=95, step=(70, 48), n=7, floor=790):
    """The opening of a corbel-vaulted Maya chamber, its ridge at ax: stepped sides closing in to a narrow capstone. Returns the
    outline and, per course, the y of the joint and the x where the course meets the left side."""
    sx, sy = step
    left, x, y = [(ax - half, top)], ax - half, top
    for k in range(n):
        left += [(x, y + sy), (x - sx, y + sy)]
        x -= sx
        y += sy
    courses = [(top + sy * (k + 1), ax - half - sx * k) for k in range(n)]
    return [(x, floor)] + list(reversed(left)) + [(2 * ax - px, py) for px, py in left] + [(2 * ax - x, floor)], courses, x


def s01(C):
    """s1 · the cold open: a dark Maya tomb under a corbel vault, an oil lamp breathing at the top left, faint stucco figures on the
    wall; Pakal's lid (3.8 by 2.2 m) stands carved and lit from the first second (sky band, bird, World Tree, king, jaws: the famous
    lid at a glance); its band catches the light as 'a carved stone lid' is said; its length (3.8 m) and a 1.7 m person beside it as
    'more than three and a half metres long' is said. Its parts light up one by one in the next sentence (s01_late)."""
    cx, top, H = LID0
    tl, tlen, tm = C.at(0, "carved stone lid"), C.at(0, "more than"), C.at(0, "metres long")
    lid_els, (x0, y0, W, Hh), F = lid(cx, top, H, {"slab": .05, "border": .15, "tree": .2, "signs": .3, "jaws": .3, "monster": .35, "king": .4, "bird": .45})
    m = H / 3.8
    opening, courses, xl = _vault(cx)
    els = [rect(-40, -40, W_ + 80, H_ + 80, "#100c09", at=-1), poly(opening, "#2a2019", "rgba(255,226,190,.16)", 2, -1)]
    for y, xa in courses:
        els.append(ln([(xa + 6, y), (2 * cx - xa - 6, y)], -1, "#120d0a", 2, draw=False, op=.55))
    for k, y in enumerate(range(488, 790, 48)):
        els.append(ln([(xl + 6, y), (2 * cx - xl - 6, y)], -1, "#120d0a", 2, draw=False, op=.45))
        for j in range(8):
            xj = xl + 70 + 140 * j + (70 if k % 2 else 0)
            els.append(ln([(xj, y - 48), (xj, y)], -1, "#120d0a", 1.6, draw=False, op=.35))
    for j, y in enumerate(range(152, 790, 48)):                        # the masonry of the wall in front of the vault
        xb = xl if y > 440 else cx - 95 - 70 * ((y - 104) // 48 - 1)
        els.append(ln([(60, y), (xb - 8, y)], -1, "#2b2219", 2, draw=False, op=.7))
        for xj in range(60 + (60 if j % 2 else 0), int(xb) - 40, 120):
            els.append(ln([(xj, y), (xj, y + 48)], -1, "#2b2219", 1.6, draw=False, op=.55))
    els += [rect(-40, 790, W_ + 80, 260, "#1a140f", at=-1), ln([(-40, 790), (W_ + 40, 790)], -1, "rgba(255,226,190,.2)", 1.5, draw=False),
            rect(430, 318, 84, 74, "#070504", "rgba(255,226,190,.2)", 1.5, 6, -1), poly([(458, 386), (486, 386), (482, 394), (462, 394)], "#8a6a48", at=-1),
            poly([(472, 386), (466, 368), (472, 350), (478, 368)], "#ffd27a", at=.1)]
    g = glow(472, 360, 430, -1, .55, "lamp")
    g["pulse"] = True                                                # it breathes (no build-in: the breathing sets its opacity)
    els += [g, glow(x0 + W * .35, y0 + Hh * .45, 560, .2, .3, "lamp"), glow(x0 + W * .5, 800, 360, .2, .3, "lamp"),
            poly([(x0 + W + 16, y0 + 40), (x0 + W + 120, y0 + 96), (x0 + W + 120, y0 + Hh), (x0 + W + 16, y0 + Hh + 6)], "rgba(0,0,0,.4)", at=.15)]
    els += lid_els
    ring = [(0, 0), (.5, 0), (1, 0), (1, .33), (1, .66), (1, 1), (.5, 1), (0, 1), (0, .66), (0, .33)]
    els += [glow(round(x0 + W * u, 1), round(y0 + Hh * v, 1), round(W * .3, 1), round(tl + .1 * k, 2), .35, "lamp") for k, (u, v) in enumerate(ring)]
    px = x0 + W + 158
    els += [dimline(x0 - 34, y0, x0 - 34, y0 + Hh, "", tlen, GOLD), lab(x0 - 52, y0 + Hh / 2 + 10, "3.8 m", round(tlen + .5, 2), GOLD, 32, "end"),
            glow(px, y0 + Hh - 140, 200, tm, .25, "lamp"), person(px, y0 + Hh, round(1.7 * m, 1), tm, "#dcc9a6"),
            lab(px, round(y0 + Hh - 1.7 * m - 26, 1), "1.7 m", round(tm + .4, 2), DIM, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s01_late(C):
    """s1, its second sentence (shot 50, an alias of the lid's panel): as the narrator names them, the reclining king, the cross-shaped
    tree (the 'machinery'), the bird at its top, then the earth monster and the open jaws below catch the light; dotted lilac flame
    strokes lick up under him on 'flames' (the claimed reading, drawn dotted)."""
    cx, top, H = LID0
    tk, ttr, tma, tfl = C.at(50, "a man leans", lo=.4), C.at(50, "frame of"), C.at(50, "machinery"), C.at(50, "flames")
    out = lid_lights(cx, top, H, {"king": tk, "tree": ttr, "bird": round(tma + .5, 2), "monster": round(tfl - .3, 2), "jaws": round(tfl - .3, 2)})
    return out + lid_flames(cx, top, H, round(tfl + .2, 2))


def _shifted(els, dx, dy, col, op):
    """Shadow copies of carving elements (polys, lines, rects, circles): moved by dx, dy and recoloured."""
    out = []
    for e in els:
        e = json.loads(json.dumps(e))
        if "p" in e:
            e["p"] = [[round(x + dx, 1), round(y + dy, 1)] for x, y in e["p"]]
        if "x" in e:
            e["x"], e["y"] = round(e["x"] + dx, 1), round(e["y"] + dy, 1)
        if e.get("fill") not in (None, "none"):
            e["fill"] = col
        if e.get("c") not in (None, "none"):
            e["c"] = col
        e.pop("fx", None)
        e.update(op=op, keepop=True)
        out.append(e)
    return out


def _exhibit(k, at, inner, name):
    """Exhibit k of the opening gallery: a dark mount, the picture in its window (clipped), a spotlight from above, the place name."""
    x = GAL_X[k]
    win = {"k": "group", "clip": [x, GAL_Y, GAL_W, GAL_H, 8], "els": inner}
    return [glow(x + GAL_W / 2, GAL_Y + 60, 340, at, .3, "lamp"),
            {"k": "group", "els": [rect(x - 14, GAL_Y - 14, GAL_W + 28, GAL_H + 28, "#15100c", "rgba(255,236,206,.42)", 2, 16), win], "in": at, "fx": "pop"},
            lab(x + GAL_W / 2, GAL_Y + GAL_H + 64, name, round(at + .35, 2), GOLD, 32)]


def _sahara(x, y):
    """The Round Head giant of Tassili, painted in ochre on a sandstone wall, arms raised, its round head blank; a person at its foot."""
    r = random.Random(31)
    out = [rect(x, y, GAL_W, GAL_H, "#7b563d")]
    for k in range(10):
        bx, by = x + r.uniform(0, GAL_W), y + r.uniform(0, GAL_H)
        rx, ry = r.uniform(50, 120), r.uniform(24, 60)
        out.append(poly([(bx + rx * (1 + .25 * r.uniform(-1, 1)) * math.cos(a), by + ry * (1 + .25 * r.uniform(-1, 1)) * math.sin(a)) for a in [2 * math.pi * j / 10 for j in range(10)]],
                        "#6a4632" if k % 2 else "#8c674a", curve=True, op=.45))
    for k in range(3):
        cx0, cy0 = x + r.uniform(30, GAL_W - 30), y + r.uniform(30, GAL_H - 30)
        out.append(ln([(cx0, cy0), (cx0 + r.uniform(-60, 60), cy0 + r.uniform(30, 80)), (cx0 + r.uniform(-80, 80), cy0 + r.uniform(90, 150))], -1, "#3f2a1d", 2, draw=False, op=.6))
    out += roundhead(x + 70, y + 250, 110, fill="#a5603a", op=.38, at=-1) + roundhead(x + 418, y + 230, 96, fill="#a5603a", op=.34, at=-1)
    out += roundhead(x + GAL_W * .46, y + GAL_H - 30, 340, fill="#b6542b", c="#e3a47c", at=-1)
    out += [person(x + GAL_W * .82, y + GAL_H - 30, 104, -1, "#1b140f")]
    return out


def _dendera(x, y):
    """The long 'bulb' relief of the Dendera crypt in pale raised relief on darker stone (its shadows to the lower right)."""
    out = [rect(x, y, GAL_W, GAL_H, "#5c5547")]
    for k in range(1, 4):
        out.append(ln([(x, y + 105 * k), (x + GAL_W, y + 105 * k)], -1, "#3d382f", 2, draw=False, op=.5))
    rel, _ = relief(x + 14, y + 100, .452, settled=True)
    rel = rel[1:]
    return out + _shifted(rel, 3, 3.5, "#221d17", .7) + rel


def _pampa(x, y):
    """The Nazca desert from above: dark stones on pale ground, two long straight lines crossing it."""
    r = random.Random(12)
    out = [rect(x, y, GAL_W, GAL_H, "#a9845b")]
    for k in range(6):
        bx, by = x + r.uniform(0, GAL_W), y + r.uniform(0, GAL_H)
        out.append(poly(_ell(bx, by, r.uniform(50, 110), r.uniform(25, 55), 10), "#b8946a" if k % 2 else "#9b7650", curve=True, op=.5))
    out += [dot(round(x + r.uniform(4, GAL_W - 4), 1), round(y + r.uniform(4, GAL_H - 4), 1), round(r.uniform(1.6, 3.4), 1), "#5a3c28", -1, fx=None, op=.55) for _ in range(110)]
    out += [ln([(x - 20, y + 330), (x + GAL_W + 20, y + 95)], -1, "#ead8b2", 7, draw=False, op=.45),
            ln([(x + 30, y - 20), (x + 250, y + GAL_H + 20)], -1, "#ead8b2", 5, draw=False, op=.35)]
    return out


GAL_X, GAL_Y, GAL_W, GAL_H = (109, 649, 1189), 172, 480, 420


def s02(C):
    """s2 · a gallery wall of three framed exhibits; the first, the Round Head giant of the Sahara, pops in as it is named (the Egyptian
    relief and the Nazca hummingbird follow on their own lines: s02_egypt, s02_peru)."""
    t1 = C.at(1, "In the Sahara", lo=.4)
    els = [rect(60, 120, 1658, 680, "rgba(255,236,206,.035)", at=-1), ln([(60, 120), (1718, 120)], -1, "rgba(255,236,206,.18)", 2, draw=False)]
    for k in range(3):
        els.append(rect(GAL_X[k] - 14, GAL_Y - 14, GAL_W + 28, GAL_H + 28, "none", "rgba(255,236,206,.10)", 1.5, 16, -1, style="inferred"))
    return {"base": "dark", "stars": 24, "cam": CAM, "els": els + _exhibit(0, t1, _sahara(GAL_X[0], GAL_Y), "Sahara")}


def s02_egypt(C):
    """s2, 'In Egypt' (shot 48, alias of the gallery): the long bulb-shaped relief of Dendera pops into the second frame."""
    return _exhibit(1, .3, _dendera(GAL_X[1], GAL_Y), "Egypt")


def s02_peru(C):
    """s2, 'In Peru' (shot 49, alias of the gallery): the desert from above pops into the third frame and the hummingbird draws itself
    in one line, a 1.7 m person a speck at its tail (93 m of bird: the person is ringed)."""
    x, y = GAL_X[2], GAL_Y
    L, rot = 352, math.pi / 2                                        # upright: the beak up, the tail fan down
    bx, by = x + GAL_W / 2 + 10, y + GAL_H / 2 - 6
    hb = hbird(bx, by, L, rot)
    tx, ty = bx + 14, by + .5 * L + 24
    return _exhibit(2, .3, _pampa(x, y), "Peru") + [
        ln(hb + [hb[0]], .6, "#f7ecd4", 3.5, dur=1.5),
        person(round(tx, 1), round(ty, 1), 7, 1.9, "#1b140f", fx="pop"), ring(round(tx, 1), round(ty - 3, 1), 17, 1.9, BONE, 2, dur=.4)]


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
        poly([(372, g - 250), (372, g - 292), (428, g - 292), (428, g - 250)], "#15110f", "rgba(255,226,190,.25)", 1.5, -1),
        poly([(386, g - 292), (390, g - 322), (410, g - 322), (414, g - 292)], "#15110f", "rgba(255,226,190,.25)", 1.5, -1),
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
    """s7 · a stack of books grows from the first words ('December 1968', 'a bestseller'); the Moon with Apollo 8's dotted orbit and
    the Earth rising; a long dotted arrow from a far star towards the Earth."""
    tb0, tb, tap, tmoon, tq = C.at(6, "By December", lo=.3), C.at(6, "bestseller", lo=.5), C.at(6, "Apollo"), C.at(6, "around the Moon"), C.at(6, "visited ours")
    els = []
    for k in range(9):
        els += book(180 + (k % 2) * 14, 700 - 44 * (k + 1), 230, 40, round(tb0 + .12 * k, 2), ["#7a3424", "#6a3a2a", "#8a4430"][k % 3], "#e0a070", fx="pop", spine=False)
    els += [lab(305, 220, "December 1968", round(tb0 + .4, 2), DIM, 26), lab(305, 260, "a bestseller", tb, GOLD, 32)]
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
    """s8 · the media timeline from 1968 to 2026, callouts at their years (dots on the axis, decades below): the German book, the
    English edition, the film's Oscar nomination, Rod Serling's special, Leonard Nimoy's series, Ancient Aliens and its twenty-two
    seasons."""
    Y = 640
    ten, tfilm, ttv, tnim, taa = C.at(7, "In English"), C.at(7, "A film"), C.at(7, "American television"), C.at(7, "Leonard"), C.at(7, "Today")
    ticks = [[TL_X(y), str(y)] for y in (1970, 1980, 1990, 2000, 2010, 2020)]
    els = [{"k": "axis", "x0": 170, "x1": 1610, "y": Y, "ticks": ticks, "in": .2}]
    calls = [(1968, 190, .5, ["the book"]), (1969, 420, ten, ["Chariots", "of the Gods?"]), (1970, 650, tfilm, ["Oscar nomination"]),
             (1973, 880, ttv, ["Rod Serling"]), (1977, 1110, tnim, ["Leonard Nimoy"])]
    for yr, x, at, txt in calls:
        at = round(at, 2)
        els += [ln([(TL_X(yr), Y - 8), (x, 560)], at, DIM, 1.6, "inferred", .5), dot(TL_X(yr), Y, 6, GOLD, at)]
        if yr in (1968, 1969):
            els += book(x - 40, 330, 80, 110, round(at + .2, 2), "#7a3424" if yr == 1968 else "#2f4a6a", "#e0a070")
        elif yr == 1970:
            els += reel(x, 385, 55, round(at + .2, 2))
        else:
            els += tv(x - 60, 340, 120, round(at + .2, 2))
        els += [lab(x, 498 + 30 * j, t, round(at + .4, 2), BONE, 26) for j, t in enumerate(txt)]
    x = TL_X(2009)
    els += [ln([(x, Y - 8), (1360, 560)], taa, DIM, 1.6, "inferred", .5), dot(x, Y, 6, GOLD, taa)] + tv(1300, 340, 120, round(taa + .2, 2)) + \
           [lab(1360, 498, "Ancient Aliens", round(taa + .4, 2), BONE, 26)]
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
    els += [lab(1392, 222, "60 million+ copies", tc + 1.4, GOLD, 28, "start"),
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
    """s12 · inside a shelter, 1956: a Round Head giant about three people tall over the copyists with a drawing board; on 'no eyes,
    no nose, no mouth' faint eyes, a nose and a mouth sketched on the blank head are struck out one by one; the nickname in lilac."""
    gx, gb, gh = GIANT
    tgi, tey, tno, tmo, tmar = C.at(11, "painted giant"), C.at(11, "no eyes"), C.at(11, "no nose"), C.at(11, "no mouth"), C.at(11, "Lhote nicknamed")
    hx, hy, hr = head_of(gx, gb, gh)
    over = [(-40, 140), (300, 120), (900, 135), (1300, 150), (1800, 120), (1800, -40), (-40, -40)]
    wall = [(80, 800), (80, 300), (200, 190), (1100, 170), (1500, 230), (1700, 300), (1700, 800)]
    els = [poly(wall, ROCK, "rgba(255,226,190,.2)", 2, -1), poly(over, "#2a1f18", at=-1),
           poly([(-40, 800), (1800, 800), (1800, 1040), (-40, 1040)], "#3a2c22", at=-1)]
    els += roundhead(gx, gb, gh, at=round(tgi, 2)) + [glow(gx, hy, 260, tgi, .3, "lamp")]
    els += [person(1150, 790, 170, .5, "#1a1511"), person(1290, 790, 160, .8, "#1a1511"),
            rect(1172, 680, 70, 52, "#efe6d2", "#8a7a66", 1.5, 3, .7), lab(1220, 520, "1956", .9, GOLD, 34),
            lab(1220, 565, "the copyists", 1.2, DIM, 26)]
    ex, ey = hr * .42, hy - hr * .18
    els += [poly(_ell(hx - ex, ey, hr * .22, hr * .12, 18), "none", BONE, 3.5, round(tey - .2, 2), style="inferred", curve=True),
            poly(_ell(hx + ex, ey, hr * .22, hr * .12, 18), "none", BONE, 3.5, round(tey - .2, 2), style="inferred", curve=True),
            strike(hx - hr * .78, ey + hr * .02, hx + hr * .78, ey - hr * .06, round(tey + .3, 2), RED, 6),
            ln([(hx + hr * .02, hy - hr * .02), (hx - hr * .12, hy + hr * .3), (hx + hr * .08, hy + hr * .33)], round(tno - .2, 2), BONE, 3.5, "inferred", .3),
            strike(hx - hr * .22, hy + hr * .32, hx + hr * .24, hy + hr * .02, round(tno + .3, 2), RED, 6),
            ln([(hx - hr * .36, hy + hr * .55), (hx, hy + hr * .64), (hx + hr * .36, hy + hr * .55)], round(tmo - .2, 2), BONE, 3.5, "inferred", .3, curve=True),
            strike(hx - hr * .5, hy + hr * .68, hx + hr * .5, hy + hr * .5, round(tmo + .3, 2), RED, 6)]
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
          [ln([(110, 580), (710, 580)], tlay, "#8a6a48", 3, dur=.6), ln([(110, 600), (710, 600)], round(tlay + .2, 2), "#6f5a44", 3, dur=.6)] + \
          cow(470, 520, 1.0, tover, "#efe6d2") + [lab(560, 190, "painted over", round(tover + .4, 2), BONE, 28)]
    els += [rect(840, 200, 230, 300, "#4f7f96", "#cfe6ff", 2, 4, tpos, fx="pop"), ln([(870, 260), (1040, 260)], tpos, "#cfe6ff", 3, draw=False),
            rect(930, 260, 230, 300, "#c96f3c", "#ffd0a0", 2, 4, round(tpos + .6, 2), fx="pop"), ln([(960, 330), (1130, 330)], round(tpos + .6, 2), "#ffd0a0", 3, draw=False),
            lab(1000, 600, "newer on top", round(tpos + 1.0, 2), DIM, 26)]
    A = lambda ya: round(220 + 1360 * (12000 - ya) / 12000, 1)
    els += [{"k": "axis", "x0": 220, "x1": 1580, "y": 740, "ticks": [[A(12000), "12,000"], [A(9000), "9,000"], [A(6000), "6,000"], [A(0), "today"]], "in": .6},
            rect(A(9500), 712, A(7500) - A(9500), 22, OCHRE, r=11, at=tband, fx="pop"),
            lab((A(9500) + A(7500)) / 2, 696, "Round Heads", round(tband + .4, 2), "#e8a070", 26),
            lab(1580, 690, "years ago", .9, DIM, 24, "end")]
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
    """s17 · back on the round head: the dotted helmet struck through, a warm glow on the painting, 'a painting style' beside it."""
    cx, cy, r = HEAD2
    tst = C.at(16, "painting style")
    return [strike(cx - r * 1.3, cy + r * .9, cx + r * 1.3, cy - r * 1.7, tst, RED, 7), glow(cx, cy, 340, round(tst + .4, 2), .5, "lamp"),
            lab(cx + r * 1.32, cy + r * .45, "a painting style", round(tst + .3, 2), GOLD, 34, "start")]


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
    """s19 · in the narrow crypt: the relief on its wall, there in the lamplight from the start (dim); each part catches the light as the
    narrator names it, with a dotted lilac claim label (bulb?, filament?, socket?, cable?, insulator?)."""
    x0, y0, s = REL
    tb, tf, tso, tca, tin = C.at(18, "bulb"), C.at(18, "filament"), C.at(18, "socket"), C.at(18, "cable"), C.at(18, "insulator")
    base, P = relief(x0, y0, s, settled=True)
    slab, carv = base[0], base[1:]
    slab["in"] = .2
    for e in carv:
        for key in ("fill", "c"):
            if e.get(key) == "#ece2c8":
                e[key] = "#a3987f"
        e["in"] = .6
    lit, _ = relief(x0, y0, s, {"bulb": round(tb - .6, 2), "snake": round(tf - .6, 2), "flower": round(tso - .5, 2), "stem": round(tca - .4, 2), "djed": round(tin - .7, 2)})
    W1, H1 = 1000 * s, 500 * s
    walls = [poly([(60, 110), (x0 - 46, y0 - 70), (x0 - 46, y0 + H1 + 70), (60, 840)], "#2a221b", "rgba(255,226,190,.12)", 1.5, -1),
             poly([(1718, 110), (x0 + W1 + 46, y0 - 70), (x0 + W1 + 46, y0 + H1 + 70), (1718, 840)], "#241d17", "rgba(255,226,190,.1)", 1.5, -1),
             poly([(60, 840), (1718, 840), (x0 + W1 + 46, y0 + H1 + 70), (x0 - 46, y0 + H1 + 70)], "#1d1712", at=-1),
             rect(x0 - 46, y0 - 70, W1 + 92, H1 + 140, "#332a22", at=-1)]
    top_y, bot_y = 196, 752
    rows = [(tb, P(520, 125), "bulb?", 900, top_y), (tf, P(800, 200), "filament?", 1180, top_y), (tso, P(100, 250), "socket?", 600, bot_y),
            (tca, P(44, 400), "cable?", 420, bot_y), (tin, P(700, 455), "insulator?", 1060, bot_y)]
    out = [flat()] + walls + [glow(x0 + 500 * s, y0 + 250 * s, 620, .2, .22, "lamp"), rect(x0 - 30, y0 - 30, W1 + 60, H1 + 60, "#2a241e", r=8, at=.2), slab] + \
          _shifted(carv, 3, 3.5, "#1a1612", .7) + carv + lit[1:]
    for at, (px, py), t, lx, ly in rows:
        ey = ly + 12 if ly < y0 else ly - 34
        out += [glow(round(px, 1), round(py, 1), 90, round(at, 2), .35, "lamp"), ln([(px, py), (lx, ey)], round(at + .2, 2), LILAC, 2, "claimed", .5),
                dot(px, py, 6, LILAC, round(at + .1, 2)), lab(lx, ly, t, round(at + .4, 2), LILAC, 32)]
    return {"base": "dark", "cam": CAM, "els": out}


def _monkey(mx, my, c, at):
    """The Nazca monkey, schematic: a small head, arms up with long fingers, legs, and its famous spiral tail."""
    sp = [(mx + 30 + (26 - 1.55 * q) * math.cos(-math.pi / 2 + q * .55), my + 2 + (26 - 1.55 * q) * math.sin(-math.pi / 2 + q * .55)) for q in range(15)]
    return [{"k": "circle", "x": mx - 40, "y": my - 34, "r": 10, "fill": "none", "c": c, "w": 3, "in": at},
            poly(_ell(mx - 18, my - 4, 20, 26, 14), "none", c, 3, at, curve=True),
            ln([(mx - 30, my - 20), (mx - 58, my - 48)], at, c, 3, draw=False)] + \
           [ln([(mx - 58, my - 48), (mx - 58 + dx, my - 48 + dy)], at, c, 2.5, draw=False) for dx, dy in ((-10, -10), (-2, -14), (6, -12))] + \
           [ln([(mx - 6, my - 18), (mx + 2, my - 52)], at, c, 3, draw=False)] + \
           [ln([(mx + 2, my - 52), (mx + 2 + dx, my - 52 + dy)], at, c, 2.5, draw=False) for dx, dy in ((-8, -10), (0, -14), (8, -10))] + \
           [ln([(mx - 26, my + 18), (mx - 36, my + 46)], at, c, 3, draw=False), ln([(mx - 8, my + 20), (mx - 2, my + 48)], at, c, 3, draw=False),
            ln([(mx - 2, my + 12), (mx + 28, my + 30)] + sp[::-1], at, c, 3, curve=True, draw=False)]


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
    """s26 · the lid (settled), and the claimed rocket drawn dotted over it: 'a rocket?' (its labels high at the right, where s27's
    veil will cover them cleanly: the lamp glow stays on the lid)."""
    cx, top, H = LIDC
    tr = C.at(25, "rocket", lo=.5)
    els, (x0, y0, W, Hh), F = lid(cx, top, H)
    return {"base": "dark", "cam": CAM, "els": [flat(), glow(cx, 470, 300, .2, .3, "lamp")] + els + rocket_over(F, round(tr - .9, 2)) + [
        lab(x0 + W + 90, 250, "a rocket?", tr, LILAC, 38, "start"), lab(x0 + W + 90, 295, "von Däniken, 1968", round(tr + .3, 2), LILAC, 26, "start")]}


def s27_late(C):
    """s27 · the rocket fades (the carved field is wiped and the carving drawn again over it, the claim's labels veiled); the glyph
    band glows; labels as said: his name, died 683 CE, ruled 68 years (a bar 615 to 683), World Tree, sacred bird, jaws of the
    underworld."""
    cx, top, H = LIDC
    els, (x0, y0, W, Hh), F = lid(cx, top, H)
    G = lambda x, y: tuple(round(v, 1) for v in F(x, y / LID_A))
    b = W * LID_B
    tname, tdie, truled, ttree, tbird, tjaw = (C.at(26, "names its man", lo=.3), C.at(26, "the year he died"), C.at(26, "He had ruled"), C.at(26, "World"),
                                               C.at(26, "sacred bird"), C.at(26, "open jaws"))
    tw = round(tname - .3, 2)
    carv, _, _ = lid(cx, top, H, carving_only=True)
    for e in carv:
        e["in"] = round(tw + .45, 2)
        e.pop("fx", None)
    out = [wipe(x0 + b, y0 + b, W - 2 * b, Hh - 2 * b, tw, SLAB_F, 1.0, .45)] + carv + \
          [rect(x0 + b, y0 + b, W - 2 * b, Hh - 2 * b, "url(#k-shade)", at=round(tw + .45, 2)), wipe(x0 + W + 60, 196, 600, 130, tw, FLAT, 1.0, .45)]
    ring_ = [(0, 0), (.5, 0), (1, 0), (1, .33), (1, .66), (1, 1), (.5, 1), (0, 1), (0, .66), (0, .33)]
    out += [glow(round(x0 + W * u, 1), round(y0 + Hh * v, 1), round(W * .25, 1), round(tname + .1 + .06 * k, 2), .4, "lamp") for k, (u, v) in enumerate(ring_)]
    L, Rr = x0 - 40, x0 + W + 40
    out += [lab(L, 210, "K'inich Janaab Pakal", round(tname + .5, 2), GOLD, 32, "end"),
            lab(L, 252, "died 683 CE", tdie, BONE, 28, "end"),
            rect(L - 300, 300, 300, 14, "rgba(242,201,142,.25)", GOLD, 1.5, 7, truled, fx="fill"),
            lab(L - 300, 290, "615", round(truled + .2, 2), DIM, 24, "start"), lab(L, 290, "683", round(truled + .2, 2), DIM, 24, "end"),
            lab(L - 150, 350, "ruled 68 years", round(truled + .4, 2), BONE, 26)]
    ax, ay = G(.9, .657)
    out += [ln([G(.5, 1.4), G(.5, .27)], ttree, GREEN, 5, draw=False), ln([G(.12, .657), G(.88, .657)], round(ttree + .4, 2), GREEN, 5, draw=False),
            ln([(ax, ay), (Rr - 10, ay)], round(ttree + .6, 2), GREEN, 1.6, dur=.3), lab(Rr, ay + 10, "World Tree", round(ttree + .7, 2), GREEN, 32, "start")]
    bx, by = G(.8, .13)
    out += [ln([(bx, by), (Rr - 10, by - 30)], tbird, GOLD, 1.6, dur=.3), lab(Rr, by - 20, "sacred bird", round(tbird + .1, 2), GOLD, 30, "start")]
    jx, jy = G(.95, 1.5)
    out += [ln([(jx, jy), (Rr - 10, jy)], tjaw, GOLD, 1.6, dur=.3), lab(Rr, jy - 4, "jaws of the", round(tjaw + .1, 2), GOLD, 30, "start"),
            lab(Rr, jy + 32, "underworld", round(tjaw + .1, 2), GOLD, 30, "start")]
    return out


def s28(C):
    """s28 · the same tree twice: at the left Pakal's lid (small, its tree catching the light); at the right the Temple of the Cross
    tablet, the same cross-shaped tree with its bird rising from the same monster head, between two standing figures (Pakal's son,
    young and grown) and its glyph columns; a dashed link: 'the same tree'."""
    tsym, tson, tsame = C.at(27, "symbol"), C.at(27, "Pakal's son"), C.at(27, "very same")
    lx, ly, lh = 330, 232, 480
    els_l, (x0, y0, W, Hh), F = lid(lx, ly, lh, {"slab": .2, "border": .3, "tree": .35, "signs": .4, "jaws": .4, "monster": .4, "king": .45, "bird": .5})
    G = lambda x, y: tuple(round(v, 1) for v in F(x, y / LID_A))
    els = els_l + [glow(*G(.5, .66), round(W * .55, 1), round(tsym, 2), .5, "lamp"), lab(lx, 772, "Pakal's lid", .6, DIM, 26)]
    fw = 262
    Wt = fw / (1 - 2 * LID_B)
    Ht = Wt / LID_RATIO
    tcx, ttop = 1150, 246 - Wt * LID_B
    tab = round(tson - .8, 2)
    els += [rect(690, 222, 920, 508, "#8a7f6b", STONE_E, 2, 6, tab), rect(704, 236, 892, 480, "#7b705e", at=tab),
            {"k": "glyphs", "x": 722, "y": 256, "w": 110, "h": 440, "rows": 11, "cols": 2, "kind": "hieroglyph", "c": "#e2d6bb", "in": tab, "seed": 3, "sw": 3},
            {"k": "glyphs", "x": 1468, "y": 256, "w": 110, "h": 440, "rows": 11, "cols": 2, "kind": "hieroglyph", "c": "#e2d6bb", "in": tab, "seed": 9, "sw": 3}]
    tree_r, _, Ft = lid(tcx, ttop, Ht, {"tree": round(tson - .4, 2), "bird": round(tson - .2, 2), "monster": round(tson - .4, 2)}, parts=("tree", "monster", "bird"))
    Gt = lambda x, y: tuple(round(v, 1) for v in Ft(x, y / LID_A))
    els += tree_r
    for x, h, at in ((925, 220, round(tson + .2, 2)), (1378, 290, round(tson + .4, 2))):
        sgn = 1 if x < tcx else -1
        els += [person(x, 700, h, at, CARVE, fx="rise"),
                poly(_lobe((x - sgn * h * .02, 700 - h * .96), (x - sgn * h * .34, 700 - h * 1.16), h * .1), CARVE, at=at, curve=True),
                poly(_lobe((x - sgn * h * .03, 700 - h * .92), (x - sgn * h * .3, 700 - h * .98), h * .07), CARVE, at=at, curve=True)]
    els += [lab(tcx, 772, "Temple of the Cross", tson, GOLD, 28)]
    a, bpt = G(.5, .02), Gt(.5, .02)
    els += [ln([a, ((a[0] + bpt[0]) / 2, 172), bpt], tsame, GOLD, 3, "inferred", 1.0, curve=True),
            lab((a[0] + bpt[0]) / 2, 150, "the same tree", round(tsame + .6, 2), GOLD, 32),
            glow(*Gt(.5, .66), round(Wt * .55, 1), round(tsame + .3, 2), .5, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


def s29(C):
    """s29 · the reclining king alone, larger (the foot of the lid's carving: the king, the monster head, the jaws): a dashed arrow down
    into the jaws (falling?), a dashed arrow up beside a sprouting maize plant (rising reborn?); then a warm glow over him."""
    tf, tr, th = C.at(28, "falling"), C.at(28, "rising"), C.at(28, "hope")
    fw = 640
    W = fw / (1 - 2 * LID_B)
    H = W / LID_RATIO
    fx0, fy0 = 889 - fw / 2, 156 - .95 * fw
    els, _, F = lid(889, fy0 - W * LID_B, H, parts=("jaws", "monster", "king"))
    G = lambda x, y: tuple(round(v, 1) for v in F(x, y / LID_A))
    hx, hy = G(.258, 1.078)
    els = [glow(889, 560, 560, .2, .22, "lamp")] + els
    els += [arrow([[hx - 150, hy - 60], [hx - 200, hy + 160], [G(.3, 1.66)[0], G(.3, 1.66)[1]]], tf, LILAC, 4, "inferred", 1.0),
            lab(hx - 214, hy + 70, "falling?", round(tf + .4, 2), LILAC, 32, "end"),
            arrow([[G(.7, 1.2)[0] + 40, G(.7, 1.2)[1]], [G(.8, 1.05)[0] + 20, G(.8, 1.05)[1] - 40], [G(.78, .98)[0] + 10, 150]], tr, GREEN, 4, "inferred", 1.0),
            lab(G(.8, 1.0)[0] + 60, 214, "rising reborn?", round(tr + .5, 2), GREEN, 32, "start")]
    mx, my = 1380, 730
    els += [ln([(mx, my), (mx, my - 300)], round(tr + .4, 2), "#8fbf5a", 6, dur=.8)] + \
           [ln([(mx, my - 80 - 50 * k), (mx + (1 if k % 2 else -1) * 90, my - 140 - 50 * k)], round(tr + .6 + .15 * k, 2), "#8fbf5a", 5, curve=True, draw=False) for k in range(4)] + \
           [poly(ellipse(mx + 14, my - 320, 14, 36, 16)[:-1], "#e8c35a", at=round(tr + 1.2, 2), fx="pop"), lab(mx + 60, my + 10, "maize", round(tr + 1.3, 2), "#a9d47c", 26, "start")]
    els += [glow(*G(.45, 1.25), 420, th, .55, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================ chapter 3 · Nazca
PAMPA = "#a9835a"


def s30(C):
    """s30 · the pampa from above: two long straight lines cross it; small framed thumbnails of the monkey and the spider (not to the
    same scale); then the hummingbird draws itself, 93 m against a 100 m bar, with a 1.7 m person at its beak (a speck, ringed)."""
    tlin, tmon, tspi, tani, thum, tm93 = C.at(29, "Straight lines"), C.at(29, "a monkey"), C.at(29, "a spider"), C.at(29, "giant animals"), C.at(29, "hummingbird"), C.at(29, "ninety-three")
    L = 760                               # 93 m: 8.17 units a metre
    m = L / 93
    hb = hbird(780, 470, L)
    els = [ln([(-20, 250), (1800, 700)], tlin, "#f1e2c2", 9, dur=1.4, op=.8), ln([(300, 820), (1500, 130)], round(tlin + .6, 2), "#f1e2c2", 7, dur=1.4, op=.7)]
    els += [ln(hb + [hb[0]], tani, "#fff2d6", 5, dur=2.4)]
    bx = 260
    els += [ln([(bx, 778), (bx + 100 * m, 778)], tm93, BONE, 3, dur=.8), ln([(bx, 766), (bx, 790)], tm93, BONE, 3, draw=False),
            ln([(bx + 100 * m, 766), (bx + 100 * m, 790)], round(tm93 + .5, 2), BONE, 3, draw=False), lab(bx - 16, 788, "100 m", round(tm93 + .6, 2), BONE, 28, "end"),
            lab(780, 160, "hummingbird, 93 m", round(thum + .3, 2), GOLD, 32)]
    px, py = hb[0]
    els += [person(px - 10, py + 6, round(1.7 * m, 1), round(tm93 + .9, 2), "#1a1511"), ring(px - 10, py - 4, 26, round(tm93 + .9, 2), BONE, 2, dur=.5),
            lab(px - 10, py + 60, "a person", round(tm93 + 1.1, 2), BONE, 24)]
    def frame(x, y, at, t):
        return [rect(x, y, 170, 150, "rgba(26,21,17,.75)", "#e9dccb", 2, 8, at, fx="pop"), lab(x + 85, y + 182, t, round(at + .2, 2), BONE, 24)]
    c = "#fff2d6"
    els += frame(1420, 150, tmon, "monkey") + _monkey(1505, 232, c, round(tmon + .2, 2))
    sp = [ln([(1505, 455), (1505 + dx, 455 + dy)], round(tspi + .2, 2), c, 3, draw=False) for dx, dy in ((-50, -40), (50, -40), (-55, 0), (55, 0), (-50, 40), (50, 40), (-35, 60), (35, 60))]
    els += frame(1420, 380, tspi, "spider") + [poly(ellipse(1505, 455, 22, 30, 16)[:-1], "#3a2c20", c, 3, round(tspi + .2, 2))] + sp
    return {"base": "plan", "bg": PAMPA, "north": False, "cam": CAM, "els": els}


def s31(C):
    """s31 · a low view of the plain, its long lines and a wide trapezoid running to the horizon from the start; on 'runways' the
    trapezoid is outlined dotted (the claim) with a dotted saucer at its end; then a person at eye level, the bird's lines running off
    past him, a dotted sightline up: 'seen from above?'"""
    tl, tr, tdr, tab = C.at(30, "some lines", lo=.4), C.at(30, "runways"), C.at(30, "draw a bird"), C.at(30, "above")
    hz = 330
    els = [poly([(-20, hz), (1800, hz), (1800, 1040), (-20, 1040)], "#9a7650", at=-1), ln([(-20, hz), (1800, hz)], -1, "rgba(255,226,190,.4)", 1.5, draw=False)]
    els += [poly([(830, hz + 10), (950, hz + 10), (1220, 780), (560, 780)], "#d9c29a", at=round(tl, 2), op=.45),
            poly([(300, hz + 4), (316, hz + 4), (60, 1040), (-60, 1040)], "#e6d3ae", at=round(tl + .3, 2), op=.5),
            poly([(1640, hz + 4), (1652, hz + 4), (1790, 760), (1760, 760)], "#e6d3ae", at=round(tl + .5, 2), op=.45)]
    els += [poly([(560, 780), (1220, 780), (950, hz + 10), (830, hz + 10)], "rgba(201,193,238,.08)", LILAC, 3, tr, style="claimed"),
            lab(540, 740, "runway?", round(tr + .4, 2), LILAC, 34, "end")] + ufo(890, hz - 60, round(tr + .6, 2), 1.0)
    els += [ln([(1300, 800), (1340, 600), (1290, 470), (1180, hz + 20)], round(tdr, 2), "#f1e2c2", 5, dur=.8, op=.8, curve=True),
            ln([(1720, 760), (1630, 520), (1500, hz + 40)], round(tdr + .2, 2), "#f1e2c2", 5, dur=.8, op=.8, curve=True),
            person(1540, 790, 170, round(tdr + .4, 2), "#1a1511"), ln([(1545, 640), (1620, 260)], round(tab - .2, 2), LILAC, 3, "claimed", .6),
            lab(1600, 220, "seen from above?", tab, LILAC, 32, "end")]
    return {"base": "sky", "tod": "day", "ground": hz, "sun": [300, 200, 26], "cam": CAM, "els": els}


def s32(C):
    """s32 · the desert floor from above, its dark rust-coloured stones on pale ground there from the start; a strip is swept clear
    (a pale line draws through) and the moved stones heap on both sides; inset, a dusty car door with a finger line; then a dotted
    wheel sinks: 'too soft'."""
    tmv, tcar, tsoft = C.at(31, "Move them"), C.at(31, "dusty"), C.at(31, "too soft")
    els = [rect(80, 130, 1000, 640, "#e4cfa2", at=.2)]
    r = random.Random(5)
    for k in range(240):
        x, y = r.uniform(96, 1064), r.uniform(146, 754)
        els.append(dot(round(x, 1), round(y, 1), round(r.uniform(9, 17), 1), ["#6a3f26", "#7a4a2c", "#5c3826"][k % 3], round(.4 + .004 * k, 2), fx=None))
    els += [rect(96, 413, 968, 74, "#efdcb0", r=30, at=tmv, dur=1.2)]
    for k in range(40):
        x = 110 + 23.5 * k + r.uniform(-5, 5)
        for sd in (-1, 1):
            els.append(dot(round(x, 1), round(450 + sd * (44 + r.uniform(0, 10)), 1), round(r.uniform(9, 14), 1), "#5c3826", round(tmv + .04 * k, 2)))
    els += [lab(580, 800 - 12, "pale ground shows through", round(tmv + 1.0, 2), BONE, 28)]
    els += [rect(1180, 180, 470, 300, "#7d8590", "#cfd6de", 2, 22, tcar, fx="pop"), rect(1180, 180, 470, 300, "rgba(200,180,140,.55)", r=22, at=tcar),
            ln([(1240, 380), (1330, 300), (1450, 350), (1580, 270)], round(tcar + .3, 2), "#dfe6ee", 10, curve=True, draw=False), lab(1415, 520, "a finger in the dust", round(tcar + .5, 2), BONE, 26)]
    els += [{"k": "circle", "x": 1415, "y": 650, "r": 60, "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": tsoft},
            arrow([[1415, 560], [1415, 640]], round(tsoft + .2, 2), LILAC, 3, "claimed", .4, False), rect(1300, 690, 230, 14, "#c9a370", r=4, at=round(tsoft + .3, 2)),
            lab(1415, 760, "too soft", round(tsoft + .5, 2), LILAC, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


COND = (889, 450, 1000)               # Nickell's condor in the field: centre, length (134 m: 7.5 units a metre)


def s33(C):
    """s33 · a field from above: a cord as the centre line from beak to tail; Joe Nickell, then five relatives (to scale, specks); a
    wooden T; '134 m' as it is said; stakes pop at measured offsets (dashed cords), then the outline joins them: the condor."""
    cx, cy, L = COND
    t82, tjoe, tsix, tT, tsc, t134, tpt = (C.at(32, "In nineteen"), C.at(32, "the investigator"), C.at(32, "five relatives"), C.at(32, "wooden T"),
                                           C.at(32, "scaled up"), C.at(32, "a hundred and"), C.at(32, "point by point"))
    m = L / 134
    pts = condor_pts(cx, cy, L)
    els = [rect(-20, -20, W_ + 40, H_ + 40, "#4f6a3c", at=-1)] + \
          [ln([(-20, y), (W_ + 20, y + 30)], -1, "#5a7646", 26, draw=False, op=.5) for y in range(60, 1000, 90)] + \
          [lab(110, 245, "Kentucky, 1982", t82, GOLD, 30, "start"), ln([(cx - L / 2, cy), (cx + L / 2, cy)], round(t82 + .5, 2), BONE, 2.5, dur=1.2)]
    spots = [(170, 600), (240, 650), (310, 610), (1480, 600), (1550, 650), (1620, 610)]
    for k, (x, y) in enumerate(spots):
        at = round(tjoe if k == 0 else tsix + .15 * k, 2)
        els += [person(x, y, round(1.7 * m, 1), at, "#f0e6d0"), ring(x, y - 6, 16, at, "rgba(240,230,208,.5)", 1.5, dur=.3)]
    els += [lab(110, 700, "Joe Nickell", round(tjoe + .3, 2), BONE, 26, "start"), lab(110, 734, "+ 5 relatives, to scale", round(tsix + 1.0, 2), DIM, 24, "start")]
    sel = pts[::2]
    for k, (x, y) in enumerate(sel):
        at = round(tsc + .09 * k, 2)
        els += [ln([(x, cy), (x, y)], at, "#e8d6b0", 1.5, "inferred", .2), dot(round(x, 1), round(y, 1), 5, "#f2c98e", round(at + .1, 2))]
    tx = sel[6][0]
    els += [ln([(tx - 22, cy), (tx + 22, cy)], tT, "#c9a370", 6, draw=False), ln([(tx, cy), (tx, cy - 30)], tT, "#c9a370", 6, draw=False)]
    els += [dimline(cx - L / 2, cy + 300, cx + L / 2, cy + 300, "", t134, GOLD), lab(cx + L / 2 + 22, cy + 311, "134 m", round(t134 + .4, 2), GOLD, 32, "start"),
            ln(pts, tpt, "#fff2d6", 4, dur=2.2), lab(cx, 160, "the Nazca condor", round(tpt + 1.2, 2), BONE, 30)]
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
    els += [ln(condor_pts(cx, cy, L), .1, "#fff2d6", 4, draw=False), lab(cx, 160, "the Nazca condor", .1, BONE, 30),
            {"k": "dim", "x1": cx - L / 2, "y1": cy + 300, "x2": cx + L / 2, "y2": cy + 300, "t": "", "c": GOLD, "in": .1},
            lab(cx + L / 2 + 22, cy + 311, "134 m", .1, GOLD, 32, "start")]
    for sx in (-1, 1):
        for sy in (-1, 1):
            X0, Y0 = cx + sx * (L / 2 + 30), cy + sy * 290
            els.append(ln([(X0, Y0 - sy * 60), (X0, Y0), (X0 - sx * 80, Y0)], tair, BONE, 5, draw=False))
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
    """s36 · a giant straight line at dusk: a procession walks along it (faint: inferred), spread out in depth; a water drop; a
    question mark over the far end."""
    tc, tw, tb = C.at(35, "ceremonial"), C.at(35, "water"), C.at(35, "both")
    hz = 380
    els = [poly([(820, hz + 2), (960, hz + 2), (1500, 1040), (300, 1040)], "#e9d6ae", at=-1, op=.85)]
    for k in range(8):
        f = .14 + .1 * k
        y = hz + 14 + (800 - hz - 14) * f ** 1.25
        h = 26 + 190 * f ** 1.25
        x = 890 + (1 if k % 2 else -1) * (14 + 150 * f)
        els.append({"k": "lib", "k2": "person", "x": round(x, 1), "y": round(y, 1), "h": round(h, 1), "color": "#2a2018", "op": .72, "keepop": True, "in": round(tc + .14 * k, 2)})
    els += [lab(1240, 560, "ceremonial walks?", round(tc + .4, 2), LILAC, 30, "start"),
            poly([(520, 480), (490, 540), (520, 560), (550, 540)], "#7fbfe6", "#cfe6ff", 2, tw, fx="pop", curve=True), lab(520, 620, "rituals for water?", round(tw + .3, 2), BLUE, 28),
            glow(890, hz - 40, 160, tb, .5, "scan"), lab(890, hz - 10, "?", tb, LILAC, 100, st="big", fx="pop")]
    return {"base": "sky", "tod": "dusk", "ground": hz, "sun": [1450, hz - 60, 30], "cam": CAM, "els": els}


# ================================================================ chapter 4 · out of place
def s37(C):
    """s37 · a map of South Africa with a pin near Klerksdorp; a pale pyrophyllite quarry face (there from 'mines'), dark grooved spheres
    in it as they are named; three spheres by size beside a 10 cm ruler (24 units a centimetre), the smallest pea-sized."""
    v = View(15, 34, -35.5, -21.5, (100, 150, 500, 540))
    tm, tsp, tsz = C.at(36, "From mines"), C.at(36, "spheres"), C.at(36, "pea-sized")
    px, py = v.p(26.0, -26.8)
    win = [90, 140, 520, 560]
    els = [{"k": "group", "clip": win + [12], "bg": "#1d3a4a", "in": -1, "els": [{"k": "map", "land": v.land()}]}, rect(*win, "none", "rgba(255,236,206,.35)", 2, 12, -1),
           {"k": "pin", "x": px, "y": py, "t": "near Klerksdorp", "c": GOLD, "lx": -16, "ly": -26, "a": "end", "in": tm},
           lab(350, 670, "South Africa", .5, DIM, 26, st="ital")]
    els += [rect(700, 140, 960, 280, "#d8d0c0", "#f5ecdc", 2, 8, round(tm + .4, 2))]
    rq = random.Random(17)
    for k in range(9):
        rx, ry = rq.uniform(50, 110), rq.uniform(14, 28)
        bx, by = rq.uniform(712 + rx, 1648 - rx), rq.uniform(154 + ry, 406 - ry)
        els.append(poly(_ell(bx, by, rx, ry, 12), "#bfb4a0" if k % 2 else "#e6dfd2", at=round(tm + .45, 2), curve=True, op=.55))
    for k, y in enumerate((178, 226, 262, 318, 360, 396)):
        els.append(ln([(708, y), (1652, y + 6 * ((-1) ** k))], round(tm + .5, 2), "#a99d86", 2 if k % 2 else 3, draw=False, op=.8))
    els += [ln([(980, 150), (1010, 230), (990, 300), (1030, 410)], round(tm + .5, 2), "#8f8471", 2, draw=False, op=.7),
            ln([(1390, 150), (1370, 260), (1400, 330)], round(tm + .5, 2), "#8f8471", 2, draw=False, op=.6)]
    for k, (x, y, r) in enumerate([(800, 240, 28), (960, 310, 36), (1120, 210, 22), (1300, 320, 32), (1460, 230, 30), (1570, 350, 18)]):
        at = round(tsp - .5 + .15 * k, 2)
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
    """s38 · deep time on one bar, there from the first words: the rock at the left end, the bar filling from 3 billion years ago to
    today as the age is said; the first animals a short band near the right end (about 600 million years ago); our species a
    hairline; then dotted claims round a sphere."""
    X = lambda ma: round(160 + 1460 * (3000 - ma) / 3000, 1)
    tbil, tani, tclaim = C.at(37, "three billion"), C.at(37, "animal"), C.at(37, "perfectly")
    Y = 520
    els = [rect(160, Y - 18, 1460, 36, "rgba(232,184,122,.06)", "rgba(232,184,122,.45)", 2, 18, .3),
           ln([(190, Y), (1612, Y)], round(tbil - .2, 2), "rgba(232,184,122,.6)", 30, dur=1.4),
           {"k": "circle", "x": 190, "y": Y, "r": 30, "fill": "#6a3f2c", "c": "#c9a07a", "w": 2, "in": .3, "fx": "pop"},
           lab(190, Y - 54, "the rock", .8, BONE, 26), lab(1620, Y + 70, "today", 1.0, DIM, 26, "end"),
           lab(160, Y + 70, "3 billion years ago", round(tbil + .3, 2), AMBER, 28, "start"),
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
           [rect(bx + 35, by - 16, 40, 16, "#cbbca8", r=3, at=round(tvo + .6, 2)), lab(bx + 55, by + 345, "torch battery: 1.5 V", round(tvo + .9, 2), AMBER, 26)]
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
        els, _, _ = lid(x, y - 42, 84, icon=True)
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
    """s43 · the ledger: its six rows there from the start, dim (a small picture and the clue); each row lights as it is named and its
    chip pops as its grade is said."""
    rows = [190, 295, 400, 505, 610, 715]
    names = ["spacemen at Tassili", "a lamp at Dendera", "a rocket at Palenque", "runways at Nazca", "machined spheres", "a battery in use"]
    kinds = ["head", "bulb", "lid", "bird", "sphere", "jar"]
    anchors = ["Spacemen", "An electric lamp", "A rocket on", "Runways", "Machined", "And the Baghdad"]
    grades = [("ruled out", "Ruled out", "ruled")] * 4 + [("ruled out", "Ruled out", "ruled"), ("awaiting evidence", "Awaiting evidence", "await")]
    els = [rect(110, 130, 1560, 650, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    for k, y in enumerate(rows):
        t0 = C.at(42, anchors[k])
        d0 = round(.3 + .1 * k, 2)
        dim = rect(130, y - 46, 1520, 92, "rgba(242,201,142,.03)", "rgba(242,201,142,.12)", 1.5, 12, d0)
        pics = mini(kinds[k], 230, y, d0)
        for e in pics:
            if e.get("k") in ("poly", "line", "circle", "rect"):
                e.update(op=.45, keepop=True)
        els += [dim, lab(340, y + 11, names[k], d0, "#8f8474", 32, "start")] + pics
        els += [rect(130, y - 46, 1520, 92, "rgba(242,201,142,.08)", "rgba(242,201,142,.42)", 1.5, 12, t0, fx="pop"),
                lab(340, y + 11, names[k], round(t0 + .1, 2), BONE, 32, "start")] + mini(kinds[k], 230, y, round(t0 + .1, 2))
        tg = C.at(42, grades[k][0], lo=0, after=t0)
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
    """s45 · a person under the stars looks up, a question beside them; the four groups of ancient makers come in with their work as
    'how did they do this?' is said; a dotted saucer; a dotted arrow lifts their work away towards it."""
    tq, thow, tsec, tgo, tel = C.at(44, "pull us", lo=.6), C.at(44, "how did"), C.at(44, "secret"), C.at(44, "hands their work"), C.at(44, "someone")
    els = [flat(), stars(70, 60, 1720, 120, 380, seed=5), stars(30, 60, 1720, 380, 520, seed=8),
           person(240, 520, 140, .4, "#e8d6b8"), ln([(250, 400), (330, 300)], .6, BONE, 1.5, "inferred", .5), lab(360, 290, "?", tq, BONE, 60, st="big", fx="pop")]
    for k, (x, t) in enumerate(GROUPS):
        at = round(thow + .25 * k, 2)
        els += [person(x - 40 + 30 * j, 760, 80 + 6 * (j % 2), at, "#e8d6b8") for j in range(3)]
    els += roundhead(GROUPS[0][0], 650, 70, at=round(thow + .2, 2))
    rel, _ = relief(GROUPS[1][0] - 60, 590, .12, settled=True)
    for e in rel:
        e["in"] = round(thow + .45, 2)
    els += rel
    ld, _, _ = lid(GROUPS[2][0], 572, 84, icon=True)
    for e in ld:
        e["in"] = round(thow + .7, 2)
        e.pop("fx", None)
    els += ld
    hb = hbird(GROUPS[3][0], 615, 120)
    els += [ln(hb + [hb[0]], round(thow + .95, 2), "#fff2d6", 2, draw=False)]
    els += ufo(1420, 200, round(tsec, 2), 1.0)
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


def _split(C, base, els, cuts):
    """Hand the later build-ins of a long scene to alias steps that start at its later sentences (same panel, same moments in the
    film): an element goes to the last cut whose sentence has begun by its time (less 0.3 s), re-timed from that step's start. Each
    step then opens on something new, which is also what a still taken a few seconds into each step shows."""
    bi, t0 = C.start[base]
    offs = []
    for a in cuts:
        b2, t = C.start[a]
        assert b2 == bi, (base, a)
        offs.append((a, t - t0))
    keep, out = [], {a: [] for a in cuts}
    for e in els:
        at, dest = e.get("in"), None
        if isinstance(at, (int, float)) and at >= 0:
            for a, off in offs:
                if at >= off - .3:
                    dest = (a, off)
        if dest:
            e = dict(e)
            e["in"] = round(max(.1, at - dest[1]), 2)
            out[dest[0]].append(e)
        else:
            keep.append(e)
    return keep, out


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
    lates = {8: s09_late, 16: s17_late, 26: s27_late, 33: s34_late, 41: s42_late, 45: s46_late, 48: s02_egypt, 49: s02_peru, 50: s01_late}
    shots = []
    for i in range(62):
        shots.append(scenes[i](C) if i in scenes else {"base": "dark", "cam": CAM, "els": []})
    cams = _tagged(ALIAS_CAMS)
    late = {i: f(C) for i, f in lates.items()}
    for base, cuts in SPLITS.items():
        shots[base]["els"], parts = _split(C, base, shots[base]["els"], cuts)
        late.update(parts)
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
