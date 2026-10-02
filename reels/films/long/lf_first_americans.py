"""LF.15 · Before Us · The First Americans (16:9 long film, one wall).

The script is films/long/lf-first-americans/script.json: its lines are read from there, untouched, and only [go:N|t] markers are
added at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s64; s5, the title, is the intro card
over the panel of s4), drawn while it is said: footprints pressed in the mud of an Ice Age lake, the Clovis points and the wall of
13,000 years, the camp of Monte Verde (its acceptance in 1997 and the 2026 challenge), the caves of Oregon and the riverbank in
Idaho, the White Sands footprints and the long argument over their dates (seeds, pollen, quartz, mud), the claims older still,
the two roads past the ice, the family tree from ancient genomes, and the weighing. Drawings are schematic and true to the numbers
said: solid = measured, dashed = inferred, dotted = claimed. No human remains are drawn: burials are shown as places, with care.

Facts: the Short 'first-americans' (f01.py, rewrite/first-americans.json) and the script's facts_added (Bennett et al. 2021,
Pigati et al. 2023 and 2024, Oviatt et al. 2023, Rhode et al. 2024, Holliday et al. 2025, Waters et al. 2020, Haynes 1964,
Dillehay 1997 and 2008, Meltzer et al. 1997, Surovell et al. 2026 and the 2026 replies, Gilbert et al. 2008, Shillito et al. 2020,
Davis et al. 2019, Ardelean et al. 2020, Chatters et al. 2022, Holen et al. 2017, Heintzman et al. 2016, Clark et al. 2022,
Pedersen et al. 2016, Lesnek et al. 2018, Erlandson et al. 2007, Moreno-Mayar et al. 2018, Raghavan et al. 2014, Rasmussen et al.
2014, Tamm et al. 2007).

Engine workaround (as in lf_voynich.py and lf_gobekli.py): the wall only adds elements to a panel on its first visit, at a beat
start or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom
carries a tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the
shot's additions as a panel item (kit.js builds them on that step's clock). Build-in times inside a sentence come from a
syllable clock (Clock, after lf_gobekli.py).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-first-americans/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-first-americans/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-first-americans RC_FILMS_EPS=/tmp/claude-0/sbx_lf-first-americans/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-first-americans/boards python3 films.py long.lf_first_americans
"""
import json, math, os, random, re
import films
from mural import remix, SENT
import illus as I
from illus import person, arrow, line, glow, label, dot, box, ring, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-first-americans", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, MUTED, DIM = "#f2c98e", "#e8c35a", "#cbbca8", "#9a8f80"
ICE, ICE_E = "#e9f2fb", "#ffffff"
LAND, LAND_E, SEA_C = "#4a3d2f", "#c9ad85", "#173342"
MUD, MUD_D, MUD_L = "#b9a383", "#7b6a52", "#e2d5ba"
WOOD, WOOD_D = "#8a6440", "#4e3622"
OCHRE = "#c0573a"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c86a", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, [go:] markers, a clock
def _find(line_, phrase):
    """Index in the raw line where `phrase` starts, ignoring the ^ stress marks."""
    keep = [i for i, ch in enumerate(line_) if ch != "^"]
    flat = "".join(line_[i] for i in keep)
    assert flat.count(phrase) == 1, (phrase, line_)
    return keep[flat.index(phrase)]


def _mark(line_, phrase, tag):
    """Insert `tag` at the start of the sentence that begins with `phrase`: before its [p:]/[act:]/[sfx:]/[tune:] tags, after a [d:] tag."""
    j = _find(line_, phrase)
    while True:
        m = re.search(r"\[[^\]]*\]$", line_[:j])
        if not m or line_[m.start():m.start() + 3] == "[d:":
            break
        j = m.start()
    return line_[:j] + tag + line_[j:]


TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # DNA: three letters
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
    """Estimated word times per beat (seconds from the beat's first word). A shot's step starts at its [go:] marker (or at the beat's
    first word; at a chapter beat's second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said,
    counted from the start of shot i's step."""
    def __init__(self, beats):
        self.start, self.words = {}, {}
        for bi, b in enumerate(beats):
            t, ws, sents = 0.0, [], []
            for li, ln_ in enumerate(b["lines"]):
                if li:
                    t += LGAP
                cuts = [0] + [m.start() for m in SENT.finditer(ln_) if m.start() > 0] + [len(ln_)]
                for a, z in zip(cuts, cuts[1:]):
                    seg = ln_[a:z]
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
            self.start.setdefault(frm, (bi, sents[1] if b.get("chapter") and len(sents) > 1 else 0.0))
            self.words[bi] = ws

    def at(self, i, phrase, lo=.4, k=1):
        """phrase: words as spoken (numbers in words, hyphens as in the script)."""
        bi, t0 = self.start[i]
        want = [_norm(x) for x in phrase.split() if _norm(x)]
        ws = self.words[bi]
        hits = 0
        for q in range(len(ws)):
            if ws[q][1] >= t0 - 1e-6 and [w for w, _ in ws[q:q + len(want)]] == want:
                hits += 1
                if hits == k:
                    return round(max(lo, ws[q][1] - t0), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))


C = None                    # the clock, set in film()
IDX = {}                    # shot id -> ep shot index, set in film()


def T(sid, phrase, lead=0.0, k=1, lo=.4):
    """Seconds after shot sid's step starts at which `phrase` is said (its k-th occurrence), plus `lead`."""
    return round(C.at(IDX[sid], phrase, lo=lo, k=k) + lead, 2)


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# ================================================================== small drawings
def R(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def poly(p, fill, c="none", w=0, at=0, fx=None, op=None, curve=False, style="known", **kw):
    e = {"k": "poly", "p": R(p), "fill": fill, "c": c, "w": w, "in": round(at, 2), "curve": curve, "style": style}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def ln(p, at, c=BONE, w=3, style="known", dur=None, curve=False, draw=True, op=None, **kw):
    e = line(R(p), round(at, 2), c, w, style, dur, curve, draw, op)
    e.update(kw)
    return e


def lab(x, y, t, at, c=BONE, size=28, a="middle", st="lab", **kw):
    return label(round(x, 1), round(y, 1), t, round(at, 2), c, size, a, st, **kw)


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(round(x, 1), round(y, 1), round(w, 1), round(h, 1), fill, c, sw, r, round(at, 2), op, fx, **kw)


def circ(x, y, r, fill="none", c="none", w=0, at=0, fx=None, op=None, style="known", **kw):
    e = {"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r, 1), "fill": fill, "c": c, "w": w, "in": round(at, 2), "style": style}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def E(cx, cy, rx, ry, n=36):
    return ellipse(cx, cy, rx, ry, n)[:-1]


def group(els, at=0, fx=None, tr=None, op=None, **kw):
    """Elements built together as one (one build-in for all of them); tr = an SVG transform for the children."""
    inner = {"k": "group", "els": els, "in": -1}
    if tr:
        inner["tr"] = tr
    e = {"k": "group", "els": [inner], "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", scl=True, fx="pop")]


def tag(x, y, t, at, c=AMBER, size=26, style="known", a="middle"):
    """A small rounded tag with a few words (dashed for an inference, dotted for a claim)."""
    w = len(t) * size * .55 + 30
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - size * .95, w, size * 1.55, "rgba(18,13,10,.82)", c, 2, size * .7, at, fx="pop", style=style),
            lab(x0 + w / 2, y + size * .2, t, at + .1, c, size, halo=False)]


def tick(x, y, at, c=GREEN, s=1.0, w=6):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": w, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cross(x, y, at, c=RED, s=1.0, w=6):
    return [ln([(x - 14 * s, y - 14 * s), (x + 14 * s, y + 14 * s)], at, c, w, dur=.25), ln([(x + 14 * s, y - 14 * s), (x - 14 * s, y + 14 * s)], at + .15, c, w, dur=.25)]


def qmark(x, y, at, size=90, c=LILAC, halo=True):
    out = [glow(round(x, 1), round(y - size * .3, 1), round(size * 1.1), round(at, 2), .5)] if halo else []
    return out + [lab(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def bracket(x0, x1, y, at, t=None, c=BONE, up=True, size=26, ty=None, style="known"):
    d = -12 if up else 12
    out = [ln([[x0, y + d], [x0, y], [x1, y], [x1, y + d]], at, c, 2, style, dur=.6)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else (y - 14 if not up else y + 34), t, at + .3, c, size))
    return out


def axis(x0, x1, y, ticks, at, t=None, below=True):
    e = {"k": "axis", "x0": round(x0, 1), "x1": round(x1, 1), "y": round(y, 1), "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def band(x0, x1, y, h, c, at, t=None, tc=None, dur=1.0, op=None):
    e = {"k": "band", "x0": round(x0, 1), "x1": round(x1, 1), "y": round(y, 1), "h": h, "c": c, "in": round(at, 2), "dur": dur}
    if t:
        e.update(t=t, tc=tc or c)
    if op is not None:
        e["op"] = op
    return e


def static(els):
    """The same elements already in place when the camera arrives (no build-in)."""
    out = []
    for e in els:
        e = dict(e)
        e["in"] = -1
        e.pop("fx", None)
        out.append(e)
    return out


def later(els, dt):
    """The same elements, built dt seconds later."""
    out = []
    for e in els:
        e = dict(e)
        if isinstance(e.get("in"), (int, float)) and e["in"] >= 0:
            e["in"] = round(e["in"] + dt, 2)
        out.append(e)
    return out


def shift(els, dx=0, dy=0):
    """The same elements moved by (dx, dy)."""
    out = []
    for e in els:
        e = dict(e)
        if "p" in e:
            e["p"] = [[round(x + dx, 1), round(y + dy, 1)] for x, y in e["p"]]
        for k in ("x", "x0", "x1", "x2"):
            if isinstance(e.get(k), (int, float)):
                e[k] = round(e[k] + dx, 1)
        for k in ("y", "y0", "y1", "y2"):
            if isinstance(e.get(k), (int, float)):
                e[k] = round(e[k] + dy, 1)
        if e.get("k") == "axis" and dx:
            e["ticks"] = [[round(a + dx, 1), b] for a, b in e["ticks"]]
        out.append(e)
    return out


def candle(x, base, h, at, w=56, burnt=0, lit=True):
    """A candle standing on `base`, h tall; burnt: a dashed ghost of the part already gone (h * burnt above it)."""
    out = [rect(x - w / 2, base - h, w, h, "#efe6d2", "#fff6e6", 1.2, 5, at, fx="fill", dur=.5)]
    if burnt:
        out.append(rect(x - w / 2, base - h - h * burnt, w, h * burnt, "none", "#efe6d2", 2, 5, at + .2, style="inferred"))
    if lit:
        out += [ln([(x, base - h), (x, base - h - 14)], at + .3, "#3a2c20", 3, draw=False),
                poly([(x, base - h - 44), (x + 10, base - h - 22), (x, base - h - 12), (x - 10, base - h - 22)], "#ffd27a", at=at + .35, curve=True, fx="pop"),
                glow(x, base - h - 26, 60, at + .35, .9)]
    return out


def balance(cx, py, L, ang, base_y, at, left=None, right=None, drop=170, pan=170, c=BONE):
    a = math.radians(ang)
    ends = [(cx - L / 2 * math.cos(a), py - L / 2 * math.sin(a)), (cx + L / 2 * math.cos(a), py + L / 2 * math.sin(a))]
    out = [rect(cx - 70, base_y - 10, 140, 14, "#5a4836", "#8c7152", 1.5, 4, at), ln([(cx, base_y - 8), (cx, py)], at, "#8c7152", 8, draw=False),
           ln(ends, at, c, 6, draw=False), dot(cx, py, 10, GOLD, round(at, 2), None)]
    for (ex, ey), stuff in zip(ends, (left, right)):
        fy = ey + drop
        out += [ln([(ex, ey), (ex - pan / 2 + 10, fy)], at, MUTED, 1.6, draw=False), ln([(ex, ey), (ex + pan / 2 - 10, fy)], at, MUTED, 1.6, draw=False),
                poly([(ex - pan / 2, fy), (ex + pan / 2, fy), (ex + pan / 2 - 18, fy + 16), (ex - pan / 2 + 18, fy + 16)], "#6b5a48", "#cbb79a", 1.5, at)]
        if stuff:
            out += stuff(round(ex, 1), round(fy, 1), at)
    return out


def seated(x, y, h, at, c="#e8d6b8", face=1, op=None):
    """A figure seated on the ground facing right (face=1) or left, h = standing height (a plain silhouette)."""
    X = lambda a: x + face * a
    out = [poly([[X(-.08 * h), y - .58 * h], [X(.1 * h), y - .58 * h], [X(.12 * h), y - .12 * h], [X(-.12 * h), y - .1 * h]], c, at=at, fx="rise", op=op),
           poly([[X(-.06 * h), y - .14 * h], [X(.34 * h), y - .14 * h], [X(.36 * h), y], [X(-.14 * h), y]], c, at=at, fx="rise", op=op),
           circ(X(.01 * h), y - .67 * h, .075 * h, c, at=at, fx="rise", op=op)]
    return out


def stone_point(x, y, h, at, fill="#c9c3b5", c="#f5ecdc", style="known", fx="pop", w=1.5, flute=True, ang=0, stemmed=False):
    """A stone point, tip up, base at (x, y), h tall: a fluted Clovis point (concave base), or a stemmed point (stemmed=True)."""
    s = h / 80
    if stemmed:
        pts = [(0, -80), (5, -72), (10, -58), (13, -42), (13.5, -30), (11, -22), (7, -18), (6.5, -8), (5.5, 0), (-5.5, 0), (-6.5, -8), (-7, -18), (-11, -22),
               (-13.5, -30), (-13, -42), (-10, -58), (-5, -72)]
    else:
        pts = [(0, -80), (4, -75), (8, -66), (11.5, -54), (13.5, -40), (14.2, -26), (14, -14), (13, -6), (12.2, -1.5), (11.6, 0), (7, -1.4), (3.5, -2.2), (0, -2.5),
               (-3.5, -2.2), (-7, -1.4), (-11.6, 0), (-12.2, -1.5), (-13, -6), (-14, -14), (-14.2, -26), (-13.5, -40), (-11.5, -54), (-8, -66), (-4, -75)]
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    P = lambda a, b: (x + (a * ca - b * sa) * s, y + (a * sa + b * ca) * s)
    out = [poly([P(a, b) for a, b in pts], fill, c, w, at, fx=fx, curve=True, style=style)]
    if flute and not stemmed and fill != "none":
        out.append(poly([P(-3.4, -4), P(3.4, -4), P(3, -26), P(0, -31), P(-3, -26)], "#a49a86", at=at, curve=True))
    return out


def figure(x, y, h, at, c="#e8d6b8", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


# ------------------------------------------------------------------ a human footprint, seen from above (an imprint in mud)
_SOLE = [(0, .5), (.1, .48), (.15, .41), (.16, .3), (.17, .17), (.19, .03), (.21, -.1), (.22, -.19), (.19, -.26), (.13, -.3), (.05, -.31),
         (-.04, -.31), (-.12, -.3), (-.18, -.26), (-.21, -.18), (-.19, -.08), (-.12, .02), (-.08, .12), (-.11, .24), (-.14, .36), (-.12, .45), (-.06, .49)]
_TOES = [(-.13, -.39, .072, .09), (-.025, -.425, .046, .056), (.055, -.41, .041, .05), (.125, -.375, .037, .045), (.185, -.32, .033, .04)]


def footprint(cx, cy, L, ang, at, side="R", fill=MUD_D, rim=MUD_L, shade="#5e4f3d", fx="pop", op=None, light=(1, -.6), detail=True):
    """A bare human footprint pressed into mud: L = foot length; ang = the direction the toes point (degrees, 0 = up, clockwise);
    side 'R' or 'L'. A pale rim of squeezed mud on the lit side, the sole and toes, and a darker shadow inside, on the side of the light."""
    m = 1 if side == "R" else -1
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    def P(u, v):                                     # u: across the foot (+ = little-toe side for a right foot), v: along (- = toes)
        x, y = m * u * L, v * L
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    lx, ly = light
    k = L / 190.
    out = []
    sole = [P(u, v) for u, v in _SOLE]
    rimp = [P(u * 1.12, v * 1.06) for u, v in _SOLE]
    out.append(poly([(x - 4 * lx * k, y - 4 * ly * k) for x, y in rimp], rim, at=at, curve=True, op=.55))
    out.append(poly(sole, fill, "rgba(40,30,20,.35)", 1.2, at, curve=True))
    if detail:
        inner = [P(u * .78, v * .9 - .01) for u, v in _SOLE]
        out.append(poly([(x + 7 * lx * k, y + 7 * ly * k) for x, y in inner], shade, at=at, curve=True, op=.75))
    for (u, v, ru, rv) in _TOES:
        tc = P(u, v)
        rr = [P(u + ru * math.cos(t) * 1.25, v + rv * math.sin(t) * 1.18) for t in [2 * math.pi * q / 14 for q in range(14)]]
        out.append(poly([(x - 3 * lx * k, y - 3 * ly * k) for x, y in rr], rim, at=at, curve=True, op=.5))
        tt = [P(u + ru * math.cos(t), v + rv * math.sin(t)) for t in [2 * math.pi * q / 14 for q in range(14)]]
        out.append(poly(tt, fill, "rgba(40,30,20,.35)", 1, at, curve=True))
        if detail:
            ts = [P(u + ru * .6 * math.cos(t), v + rv * .6 * math.sin(t)) for t in [2 * math.pi * q / 12 for q in range(12)]]
            out.append(poly([(x + 3 * lx * k, y + 3 * ly * k) for x, y in ts], shade, at=at, curve=True, op=.7))
    return [group(out, at, fx, op=op)]


def trail(x0, y0, ang, L, step, n, at, dt=.12, gait=.13, first="L", **kw):
    """n footprints along a walk from (x0, y0) heading `ang` (0 = up, clockwise), alternating feet."""
    a = math.radians(ang)
    ux, uy = math.sin(a), -math.cos(a)               # walking direction
    px, py = math.cos(a), math.sin(a)                # to the walker's right
    out = []
    for q in range(n):
        side = first if q % 2 == 0 else ("R" if first == "L" else "L")
        off = gait * L * (1 if side == "R" else -1)
        out += footprint(x0 + ux * step * q + px * off, y0 + uy * step * q + py * off, L, ang + (4 if side == "R" else -4), round(at + dt * q, 2), side, **kw)
    return out


def mud_ground(x0, y0, x1, y1, at=-1, seed=3, n=34, c=MUD, crack="#7d6b52"):
    """Pale lake mud: a flat ground, faint mud cracks, gypsum glints."""
    r = random.Random(seed)
    out = [rect(x0, y0, x1 - x0, y1 - y0, c, at=at)]
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        a = r.uniform(0, 2 * math.pi)
        pts = [(x, y)]
        for q in range(r.randint(3, 6)):
            a += r.uniform(-.9, .9)
            d = r.uniform(30, 90)
            x, y = x + d * math.cos(a), y + d * math.sin(a)
            pts.append((min(max(x, x0), x1), min(max(y, y0), y1)))
        out.append(ln(pts, at, crack, round(r.uniform(1.2, 2.4), 1), draw=False, op=round(r.uniform(.25, .5), 2)))
    for _ in range(60):
        out.append(circ(r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(1.2, 2.8), "#f6efe0", at=at, op=round(r.uniform(.25, .6), 2)))
    return out


# ------------------------------------------------------------------ animals and plants (silhouettes)
def mammoth(x, y, h, at, c="#1f1a17", face=-1, fx="rise", op=None):
    """A woolly mammoth in silhouette (after f03.mammoth), feet on y, h = shoulder height; face=-1 faces left."""
    s = h / 100
    P = [(-30, -102), (0, -98), (30, -84), (55, -62), (62, -40), (60, -15), (52, 18), (50, 52), (30, 52), (28, 22), (20, 10), (-10, 8), (-40, 12), (-40, 52), (-60, 52),
         (-62, 20), (-66, -20), (-72, -42), (-88, -42), (-98, -25), (-106, 0), (-108, 20), (-114, 28), (-118, 14), (-112, -8), (-104, -32), (-100, -56), (-98, -75), (-90, -90), (-72, -97), (-55, -90)]
    f = -face
    body = [(x + f * px * s, y + (py - 52) * s) for px, py in P]
    tusk = [(x + f * px * s, y + (py - 52) * s) for px, py in [(-86, -40), (-108, -20), (-128, -26), (-138, -50)]]
    return [poly(body, c, at=at, fx=fx, curve=True, op=op), ln(tusk, at + .1, "#efe6d4", max(2, 4.2 * s), draw=False, curve=True, op=op)]


def conifer(x, y, h, at, c="#1d2620", fx="pop", edge="rgba(255,226,190,.18)", **kw):
    w = h * .42
    pts = [[x, y - h], [x + w * .32, y - h * .62], [x + w * .2, y - h * .62], [x + w * .45, y - h * .32], [x + w * .3, y - h * .32], [x + w * .5, y - h * .08],
           [x + w * .08, y - h * .08], [x + w * .08, y], [x - w * .08, y], [x - w * .08, y - h * .08], [x - w * .5, y - h * .08], [x - w * .3, y - h * .32],
           [x - w * .45, y - h * .32], [x - w * .2, y - h * .62], [x - w * .32, y - h * .62]]
    e = poly(pts, c, edge, 1, at, fx=fx)
    e.update(kw)
    return e


def helix(x0, y0, x1, y1, at, n=16, amp=18, c1=GOLD, c2=BLUE, w=3, dur=1.0):
    """A DNA double helix drawn as two crossing waves with rungs (after f16.helix)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    P = lambda t, ph: [round(x0 + ux * L * t + nx * amp * math.sin(t * n + ph), 1), round(y0 + uy * L * t + ny * amp * math.sin(t * n + ph), 1)]
    ts = [k / 40 for k in range(41)]
    out = [{"k": "line", "p": [P(t, 0) for t in ts], "c": c1, "w": w, "curve": True, "in": round(at, 2), "fx": "draw", "dur": dur},
           {"k": "line", "p": [P(t, math.pi) for t in ts], "c": c2, "w": w, "curve": True, "in": round(at + .1, 2), "fx": "draw", "dur": dur}]
    out += [{"k": "line", "p": [P(t, 0), P(t, math.pi)], "c": "#e9dccb", "w": 1.5, "op": .5, "keepop": True, "in": round(at + dur * .8, 2)} for t in [k / 10 + .05 for k in range(10)]]
    return out


def flask(x, y, s, at, c=BLUE):
    """A lab flask (chemistry), base at y."""
    P = lambda a, b: (x + a * s, y + b * s)
    return [poly([P(-10, -70), P(10, -70), P(10, -40), P(36, 0), P(-36, 0), P(-10, -40)], "rgba(159,208,255,.12)", c, 2.5, at, fx="pop"),
            poly([P(-26, -12), P(26, -12), P(32, -2), P(-32, -2)], "rgba(143,217,176,.6)", at=at + .1)]


# ================================================================== maps
def _unwrap(ring):
    out, prev = [], None
    for lo, la in ring:
        if prev is not None:
            while lo - prev > 180:
                lo -= 360
            while lo - prev < -180:
                lo += 360
        out.append((lo, la)); prev = lo
    return out


def _clip(ring, x0, x1, y0, y1):
    """Sutherland-Hodgman: a closed ring clipped to a lon/lat box."""
    def cut(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia:
                    out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return out
    def ix(xc):
        return lambda a, b: (xc, a[1] + (b[1] - a[1]) * (xc - a[0]) / ((b[0] - a[0]) or 1e-9))
    def iy(yc):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yc - a[1]) / ((b[1] - a[1]) or 1e-9), yc)
    pts = list(ring)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not pts:
            break
        pts = cut(pts, inside, inter)
    return pts


class Map:
    """An equirectangular map of a lon/lat box fitted in a frame rectangle (like films.View), whose longitudes may run past 180
    (lon0 160, lon1 250: the North Pacific in one piece); land rings are unwrapped, shifted into the box and clipped to it."""
    def __init__(self, lon0, lon1, lat0, lat1, rect=(90, 120, 1600, 680)):
        self.b = (lon0, lon1, lat0, lat1)
        k = math.cos(math.radians((lat0 + lat1) / 2))
        w, h = (lon1 - lon0) * k, (lat1 - lat0)
        s = min(rect[2] / w, rect[3] / h)
        self.s, self.k = s, k
        self.ox = rect[0] + (rect[2] - w * s) / 2
        self.oy = rect[1] + (rect[3] - h * s) / 2

    def p(self, lon, lat):
        lon0, lon1, lat0, lat1 = self.b
        while lon < lon0 - 180:
            lon += 360
        while lon > lon1 + 180:
            lon -= 360
        return (round(self.ox + (lon - lon0) * self.k * self.s, 1), round(self.oy + (lat1 - lat) * self.s, 1))

    def km(self, km):
        return km / 111.32 * self.s

    def land(self, pad=25.0, tol=1.4, minpts=4):
        lon0, lon1, lat0, lat1 = self.b
        out = []
        for poly_ in films._topo():
            ring = _unwrap(poly_[0])
            xs = [q[0] for q in ring]
            for sh in (-360, 0, 360):
                if max(xs) + sh < lon0 - pad or min(xs) + sh > lon1 + pad:
                    continue
                if max(q[1] for q in ring) < lat0 - pad or min(q[1] for q in ring) > lat1 + pad:
                    continue
                cl = _clip([(q[0] + sh, q[1]) for q in ring], lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad)
                if len(cl) < minpts:
                    continue
                pts, last = [], None
                for lo, la in cl:
                    q = self.p(lo, la)
                    if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                        continue
                    pts.append(q); last = q
                if len(pts) >= minpts:
                    out.append("M" + "L".join(f"{x} {y}" for x, y in pts) + "Z")
        return out

    def path(self, lonlats):
        return [self.p(lo, la) for lo, la in lonlats]


class Globe:
    """An orthographic globe centred on (lon0, lat0), radius R at (cx, cy); land on the far side is pressed onto the limb."""
    def __init__(self, lon0, lat0, R, cx, cy):
        self.l0, self.p0, self.R, self.cx, self.cy = math.radians(lon0), math.radians(lat0), R, cx, cy

    def xyz(self, lon, lat):
        l, p = math.radians(lon), math.radians(lat)
        cosc = math.sin(self.p0) * math.sin(p) + math.cos(self.p0) * math.cos(p) * math.cos(l - self.l0)
        x = math.cos(p) * math.sin(l - self.l0)
        y = math.cos(self.p0) * math.sin(p) - math.sin(self.p0) * math.cos(p) * math.cos(l - self.l0)
        return x, y, cosc

    def p(self, lon, lat):
        x, y, c = self.xyz(lon, lat)
        if c < 0:
            d = math.hypot(x, y) or 1
            x, y = x / d, y / d
        return (round(self.cx + self.R * x, 1), round(self.cy - self.R * y, 1))

    def land(self, tol=1.6, minpts=4):
        out = []
        for poly_ in films._topo():
            ring = poly_[0]
            vis = [self.xyz(lo, la)[2] > 0 for lo, la in ring]
            if not any(vis):
                continue
            pts, last = [], None
            for lo, la in ring:
                q = self.p(lo, la)
                if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                    continue
                pts.append(q); last = q
            if len(pts) >= minpts:
                out.append("M" + "L".join(f"{x} {y}" for x, y in pts) + "Z")
        return out


def land_el(paths, at=-1, landc=LAND):
    return {"k": "map", "land": paths, "landc": landc, "in": at}


def pin(x, y, t, at, c=AMBER, a="start", lx=None, ly=None, r=9, tc=None, size=None):
    e = {"k": "pin", "x": round(x, 1), "y": round(y, 1), "t": t, "c": c, "a": a, "r": r, "in": round(at, 2)}
    if lx is not None:
        e["lx"] = lx
    if ly is not None:
        e["ly"] = ly
    if tc:
        e["tc"] = tc
    return e


# Ice sheets about 21,000 years ago (schematic, after f01.first_americans: lon, lat)
LAURENTIDE = [(-140, 70), (-120, 73), (-95, 76), (-70, 76), (-60, 65), (-62, 52), (-70, 44), (-75, 41.5), (-85, 39.5), (-95, 42), (-105, 48), (-113, 50),
              (-118, 55), (-125, 60), (-135, 65)]
CORDILLERAN = [(-152, 62), (-138, 60.5), (-129, 56), (-123, 48.5), (-117, 47.5), (-116, 52), (-121, 57), (-132, 62), (-146, 64)]
CORD_LGM = [(-152, 62), (-138, 60.5), (-129, 56), (-123, 48.5), (-116, 47.5), (-112.5, 51), (-115, 56.5), (-121, 61.5), (-130, 64.5), (-146, 64.5)]   # merged with the Laurentide
BERINGIA = [(-179, 67), (-168, 69.5), (-160, 70.5), (-158, 66), (-163, 60), (-172, 58.5), (-179, 60)]
# the same two sheets drawn apart (the corridor of the Clovis-first model, schematic)
LAUR_OPEN = [(-128, 70.5), (-120, 73), (-95, 76), (-70, 76), (-60, 65), (-62, 52), (-70, 44), (-75, 41.5), (-85, 39.5), (-95, 42), (-103, 47), (-108, 50),
             (-111, 55), (-115, 60), (-121, 65)]
CORD_OPEN = [(-152, 62), (-138, 60.5), (-129, 56), (-123, 48.5), (-118, 48), (-117.5, 52), (-121, 57), (-127, 61.5), (-140, 64)]

SITE = {"whitesands": (-106.33, 32.78), "clovis": (-103.3, 34.27), "monteverde": (-73.2, -41.5), "paisley": (-120.55, 42.75),
        "coopers": (-116.43, 45.73), "chiquihuite": (-101.4, 24.6), "cerutti": (-117.05, 32.75), "usr": (-144.9, 64.2), "anzick": (-110.65, 46.0),
        "malta": (103.0, 52.9), "japan": (142.5, 43.0)}


# ================================================================== a placeholder (only while a scene is being drawn)
def _todo(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 480, sid, .3, MUTED, 60)]}


# ================================================================== the film: beats (script lines + markers), aliases, the wall
# (chapter, beat, role, the beat's panel, [(line, the phrase that opens the sentence, shot)], extra beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "In the depths", "s2"), (1, "So when did", "s3"), (1, "For much of", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(0, "Each one is", "s7"), (1, "Points like these", "s8"), (1, "To date them", "s9"), (1, "The answer, again", "s10")],
     {"chapter": "The Clovis wall"}),
    (1, 1, "collision", "s11", [(0, "When the ice", "s12")], {}),
    (1, 2, "cost", "s13", [(0, "Claim after claim", "s14"), (0, "Thirteen thousand years", "s15")], {}),
    (2, 0, "world", "s16", [(0, "In {1977", "s17"), (1, "The wooden frames", "s18"), (1, "Its age", "s19")], {"chapter": "A camp in Chile"}),
    (2, 1, "collision", "s20", [(1, "Then, in {1997", "s21"), (1, "The wall had", "s22")], {}),
    (2, 2, "cost", "s23", [(0, "In Idaho", "s24")], {}),
    (2, 3, "reversal", "s25", [(0, "They argue", "s26"), (0, "A date dates", "s27"), (1, "The excavators", "s28"), (1, "The jury", "s29")], {}),
    (3, 0, "world", "s30", [(1, "In the old lake", "s31"), (1, "The prints are sealed", "s32"), (2, "The first dates", "s33")],
     {"chapter": "Footprints in the mud"}),
    (3, 1, "collision", "s34", [(0, "It's like lighting", "s35"), (0, "They dated", "s36")], {}),
    (3, 2, "reversal", "s37", [(0, "About seventy-five", "s38"), (0, "And the quartz", "s39"), (1, "Both agreed", "s40"), (1, "Some experts", "s41")], {}),
    (3, 3, "tag", "s42", [(0, "And near San", "s43")], {}),
    (4, 0, "world", "s44", [], {"chapter": "Which road?"}),
    (4, 1, "collision", "s45", [(0, "It took more", "s46")], {}),
    (4, 2, "cost", "s47", [(0, "Along the North", "s48"), (0, "And the stone points", "s49")], {}),
    (4, 3, "reversal", "s50", [(0, "So the first people", "s51")], {}),
    (5, 0, "world", "s52", [], {"chapter": "What the genes say"}),
    (5, 1, "collision", "s53", [(0, "With others", "s54"), (1, "Then came a long", "s55")], {}),
    (5, 2, "cost", "s56", [(0, "In {2014", "s57")], {}),
    (5, 3, "tag", "s58", [(1, "And many Native", "s59")], {}),
    (6, 0, "weigh", "s60", [(1, "People in the Americas", "s61"), (2, "Chiquihuite, at", "s62")], {"chapter": "The weighing"}),
    (6, 1, "test", "s63", [], {}),
    (6, 2, "close", "s64", [], {}),
]

# alias shots: (the panel's shot, the camera on that panel, the additions built when the camera arrives)
ALIASES = {
    "s14": ("s13", CAM, "s14_add"), "s19": ("s16", CAM, "s19_add"),
    "s26": ("s25", CAM, "s26_add"), "s28": ("s25", CAM, "s28_add"), "s29": ("s22", CAM, "s29_add"),
    "s33": ("s32", CAM, "s33_add"), "s41": ("s40", CAM, "s41_add"), "s45": ("s44", [1.45, 620, 400], "s45_add"),
    "s57": ("s56", CAM, "s57_add"),
    "s61": ("s60", CAM, "s61_add"),
}


def film():
    global C
    script = json.load(open(SCRIPT, encoding="utf-8"))
    g = globals()
    order = []
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in order and sid not in ALIASES:
                order.append(sid)
    ids = order + list(ALIASES)
    IDX.clear(); IDX.update({s: i for i, s in enumerate(ids)})
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % IDX[sid])
        beats.append(B(role, IDX[frm], lines, **kw))
    C = Clock(beats)
    shots = [(g[sid]() if sid in g else _todo(sid)) for sid in order] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[IDX[sid]] = IDX[root]
        cams[IDX[sid]] = [z] + list(cam[1:])
        tags[z] = g[fn]() if fn in g else []
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-first-americans", "code": "LF.15", "series": script["series"], "title": script["title"], "case": "first-americans",
          "verdict": "strong", "claim": "When did people first reach the Americas?", "mood": "awe",
          "hook_text": "When did people *first* reach the Americas?", "beats": beats, "shots": shots,
          "sources": "Bennett et al. 2021 (doi:10.1126/science.abg7586) · Pigati et al. 2023 (doi:10.1126/science.adh5007) · "
                     "Holliday et al. 2025 (doi:10.1126/sciadv.adv4951) · Oviatt et al. 2023 (doi:10.1017/qua.2022.38) · "
                     "Waters et al. 2020 (doi:10.1126/sciadv.aaz0455) · Meltzer et al. 1997 (doi:10.2307/281884) · "
                     "Surovell et al. 2026 (doi:10.1126/science.adw9217) · Davis et al. 2019 (doi:10.1126/science.aax9830) · "
                     "Ardelean et al. 2020 (doi:10.1038/s41586-020-2509-0) · Moreno-Mayar et al. 2018 (doi:10.1038/nature25173)",
          "post": "Footprints of teenagers and children, pressed into the mud of an Ice Age lake in New Mexico. How the 'Clovis first' wall of "
                  "13,000 years fell, the fight over Monte Verde (and its 2026 challenge), the long argument over the White Sands dates, the two "
                  "roads past the ice, and what ancient genomes say, weighed.",
          "hashtags": ["#FirstAmericans", "#WhiteSands", "#IceAge", "#Archaeology", "#Clovis", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": script["intro_title"], "yt_title": script["yt_title"], "description": desc, "end_line": script["end_line"]}
    ep = remix(ep, alias=alias, cams=cams)
    # the tagged cameras: give each the additions of its shot, on the step that reached it
    pans = ep["wall"]["panels"]
    for z, els in tags.items():
        hit = [k for k, st in enumerate(ep["shots"]) if round(st["cam"][0], 4) == z]
        assert len(hit) == 1, ("tagged camera reached", z, hit)
        if not els:
            continue
        st = ep["shots"][hit[0]]
        x, y = st["cam"][1], st["cam"][2]
        j = next(j for j, p in enumerate(pans) if p["ox"] <= x <= p["ox"] + p["w"] and p["oy"] <= y <= p["oy"] + p["h"])
        p = pans[j]
        st["els"].append({"k": "panel", "ox": p["ox"], "oy": p["oy"], "w": p["w"], "h": p["h"], "base": "none", "els": els, "pn": j})
    return ep


def EPISODES():
    return [film()]


# ================================================================== cold open
TEEN = dict(x=330, y=560, L=190, step=400, n=4)          # the two trails of the opening (toes pointing 76 degrees: walking up and right)
KID = dict(x=470, y=720, L=135, step=290, n=5)


def s1():
    """The hero image: pale lake mud in low light, two trails of bare footprints (a teenager's and a child's) crossing the frame."""
    tt, tk, tn = T("s1", "teenagers"), T("s1", "children"), T("s1", "New Mexico")
    els = mud_ground(-10, -10, 1790, 1010, -1, seed=5, n=46)
    els += [glow(1640, 120, 760, -1, .32, "lamp")]
    r = random.Random(8)
    for q in range(7):                                                      # faint ripple marks, across the walk
        x0, y0 = r.uniform(100, 1500), r.uniform(150, 760)
        els.append(ln([(x0 + 40 * k, y0 + 10 * math.sin(k * 1.3)) for k in range(6)], -1, "#a08b6c", 2, draw=False, curve=True, op=.35))
    els += trail(TEEN["x"], TEEN["y"], 76, TEEN["L"], TEEN["step"], TEEN["n"], .1, dt=.14, gait=.14)
    els += trail(KID["x"], KID["y"], 76, KID["L"], KID["step"], KID["n"], .18, dt=.12, gait=.14, first="R")
    els += [lab(720, 398, "teenager", tt, "#fff3dc", 30), lab(1030, 664, "child", tk, "#fff3dc", 30),
            lab(1670, 776, "White Sands, New Mexico", max(3.5, tn), "#fff3dc", 30, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def s2():
    """Dusk on an Ice Age lake shore: snowy mountains, the long lake, a teenager and a child walking the wet shore, mammoths far off."""
    SH = 650
    far = [(-20, 470), (120, 420), (260, 380), (420, 300), (560, 360), (700, 330), (860, 250), (1010, 330), (1160, 300), (1320, 360), (1480, 310), (1640, 380), (1800, 360), (1800, 560), (-20, 560)]
    caps = [[(372, 330), (420, 300), (470, 330), (440, 338), (420, 326), (400, 340)], [(810, 280), (860, 250), (912, 284), (880, 290), (858, 278), (836, 292)],
            [(1120, 316), (1160, 300), (1205, 320), (1180, 326), (1160, 316), (1140, 328)], [(1440, 330), (1480, 310), (1522, 332), (1496, 336), (1478, 326), (1460, 338)]]
    near = [(-20, 540), (200, 500), (380, 520), (560, 480), (760, 520), (980, 500), (1200, 530), (1400, 505), (1620, 530), (1800, 515), (1800, 560), (-20, 560)]
    els = [poly(far, "#4c5468", at=-1, curve=True), *[poly(c, "#e6edf5", at=-1, op=.9) for c in caps], poly(near, "#363443", at=-1, curve=True),
           rect(-20, 556, 1840, SH - 556 + 2, "#40627a", at=-1), rect(-20, 556, 1840, 8, "#9fc3d8", at=-1, op=.35),
           glow(1260, 560, 260, -1, .45, "sun")]
    els += [ln([(1100 + 40 * k, 590 + 12 * k), (1180 + 50 * k, 590 + 12 * k)], -1, "#ffe2b4", 2, draw=False, op=.35) for k in range(4)]
    els += [rect(-20, SH - 8, 1840, 16, "#5d6a72", at=-1, op=.6)]                 # the wet margin of the shore
    for k, x in enumerate((1380, 1470, 1560)):
        els += mammoth(x, SH - 4, 56 - 6 * (k == 1), .3 + .2 * k, "#262230", face=-1)
    r = random.Random(3)
    steps_ = [(160 + 34 * k, 772 - 4 * (k % 2) - 1.6 * k) for k in range(15)]
    els += [poly(E(x, y, 9, 4, 12), "#3e352b", at=round(.6 + .05 * k, 2), op=.8) for k, (x, y) in enumerate(steps_)]
    els += [figure(720, 752, 118, .5, "#231d19"), figure(790, 760, 84, .6, "#231d19")]
    els += [lab(889, 200, "the last Ice Age", .9, "#dfe8f2", 34)]
    return {"base": "sky", "tod": "dusk", "ground": SH, "sun": [1260, 545, 20], "ridges": [], "cam": CAM, "els": els}


GLOBE = (-92, 10, 330, 889, 470)


def s3():
    """The Americas on a dark globe; a gold dot at White Sands; a large question mark."""
    g = Globe(*GLOBE)
    lon0, lat0, Rr, cx, cy = GLOBE
    ws = g.p(*SITE["whitesands"])
    tq = T("s3", "Americas", -.6)
    els = [glow(cx, cy, 520, -1, .25, "blue"), circ(cx, cy, Rr, "#163447", at=-1), land_el(g.land(), -1, "#5b4a36"),
           circ(cx, cy, Rr + 4, "none", "#9fd0ff", 5, -1, op=.35), circ(cx, cy, Rr, "none", "#cfe6ff", 1.5, -1, op=.6),
           glow(ws[0], ws[1], 70, .5, .9, "lamp"), dot(ws[0], ws[1], 8, GOLD, .5)]
    els += qmark(1350, 560, tq, 220)
    return {"base": "dark", "stars": 140, "cam": CAM, "els": els}


def XA(ya):                                     # the long axis of the opening: 25,000 years ago at x 200, 10,000 at x 1580
    return round(200 + (25000 - ya) / 15000 * 1380, 1)


def open_book(cx, cy, w, h, at, c="#efe3c8", fx="pop"):
    """An open book seen from above at an angle: two pages with lines."""
    L = [(cx - w, cy - h * .45), (cx - 6, cy - h * .5), (cx - 6, cy + h * .5), (cx - w, cy + h * .55)]
    Rr = [(cx + 6, cy - h * .5), (cx + w, cy - h * .45), (cx + w, cy + h * .55), (cx + 6, cy + h * .5)]
    lines_ = [ln([(cx - w + 14, cy - h * .3 + 14 * k), (cx - 20, cy - h * .33 + 14 * k)], at, "#8a7a62", 2, draw=False) for k in range(5)]
    lines_ += [ln([(cx + 20, cy - h * .33 + 14 * k), (cx + w - 14, cy - h * .3 + 14 * k)], at, "#8a7a62", 2, draw=False) for k in range(5)]
    return [group([poly(L, c, "#fff6e6", 1.5), poly(Rr, c, "#fff6e6", 1.5), ln([(cx, cy - h * .5), (cx, cy + h * .52)], 0, "#8a7a62", 3, draw=False)] + lines_, at, fx)]


def s4():
    """The textbook date (13,000) and the footprints (23,000 to 21,000) on one axis; at least 8,000 years between them."""
    tb, tf, tg = T("s4", "textbooks"), T("s4", "These footprints"), T("s4", "at least eight")
    AY = 560
    els = [axis(200, 1580, AY, [(XA(v), "{:,}".format(v)) for v in (25000, 20000, 15000, 10000)], .2, "years ago")]
    els += open_book(XA(13000), 420, 90, 110, tb) + [lab(XA(13000), 318, "the textbook date", tb + .3, BONE, 30), tick(XA(13000), 500, tb + .5, GOLD),
             ln([(XA(13000), AY - 12), (XA(13000), AY + 12)], tb, GOLD, 4, draw=False)]
    els += [band(XA(23000), XA(21000), AY - 46, 28, GOLD, tf, dur=.8), glow((XA(23000) + XA(21000)) / 2, AY - 32, 130, tf + .2, .7, "lamp")]
    for dx, side, dy in ((-26, "L", 10), (26, "R", -14)):
        els += footprint((XA(23000) + XA(21000)) / 2 + dx, 420 + dy, 92, 0, tf + .3, side, fill="#f2c98e", rim="#fff1d0", shade="#c99a5a", detail=False)
    els += [lab((XA(23000) + XA(21000)) / 2, 318, "the footprints", tf + .4, GOLD, 30)]
    els += bracket(XA(21000), XA(13000), 690, tg, None, GOLD, up=True) + [lab((XA(21000) + XA(13000)) / 2, 750, "at least 8,000 years", tg + .3, GOLD, 32)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== chapter 1: the Clovis wall
def bone(x0, y0, x1, y1, at, w=12, c="#efe6d4", **kw):
    """A long bone: a shaft with knobbed ends."""
    e = [ln([(x0, y0), (x1, y1)], at, c, w, draw=False), circ(x0, y0, w * .9, c, at=at), circ(x1, y1, w * .9, c, at=at),
         circ(x0 + (y1 - y0) * .05, y0 - (x1 - x0) * .05, w * .7, c, at=at), circ(x1 - (y1 - y0) * .05, y1 + (x1 - x0) * .05, w * .7, c, at=at)]
    for q in e:
        q.update(kw)
    return e


def s6():
    """A dig in cross-section near Clovis in the 1930s: diggers at the surface, mammoth bones in the bone bed, spear points among them."""
    tm, td, tp = T("s6", "mammoths"), T("s6", "diggers"), T("s6", "spear points")
    GY = 330
    layers = [{"d": 0, "c": "#8a7356", "t": ""}, {"d": 110, "c": "#a39072", "t": ""}, {"d": 210, "c": "#77705f", "t": ""}, {"d": 330, "c": "#5f4c39", "t": ""}]
    BB = GY + 270                                                          # the bone bed (grey sand)
    els = [figure(470, GY, 120, .3, "#2a221b"), figure(560, GY, 112, .4, "#2a221b"), ln([(586, GY - 66), (628, GY - 4)], .4, "#6b4a2e", 5, draw=False),
           rect(640, GY - 40, 110, 12, "#6b5a48", "#cbb79a", 1.5, 2, .5), ln([(650, GY - 28), (650, GY)], .5, "#6b5a48", 4, draw=False),
           ln([(740, GY - 28), (740, GY)], .5, "#6b5a48", 4, draw=False)]
    tusk = [(700, BB - 10), (820, BB - 70), (960, BB - 84), (1080, BB - 50), (1120, BB - 10)]
    els += [ln(tusk, tm, "#efe6d4", 20, draw=False, curve=True), ln(tusk, tm, "#c9b48e", 2, draw=False, curve=True, op=.6)]
    els += bone(1180, BB + 30, 1420, BB + 10, tm + .2, 16)
    els += [ln([(1240 + 34 * k, BB - 60), (1230 + 34 * k + 20, BB + 2)], round(tm + .3 + .05 * k, 2), "#e2d5bb", 7, draw=False, curve=False) for k in range(6)]
    els += [rect(560, BB - 4, 124, 52, "#d9cbb0", "#fff6e6", 1.5, 12, tm + .4)]     # a molar: a block of enamel plates
    els += [ln([(574 + 12 * k, BB + 2), (568 + 12 * k, BB + 42)], tm + .4, "#9c8e74", 3, draw=False) for k in range(9)]
    for k, (x, y, a) in enumerate(((880, BB + 40, 80), (1150, BB - 30, -60), (1490, BB + 34, 100))):
        els += [glow(x, y, 60, round(tp + .25 * k, 2), .9, "lamp")] + stone_point(x, y + 22, 64, round(tp + .25 * k, 2), ang=a)
    els += [lab(180, 200, "New Mexico, 1930s", .6, BONE, 30, "start"), lab(1290, BB - 110, "mammoth bones", tm + .5, BONE, 30),
            lab(880, BB + 130, "spear points", tp + .6, GOLD, 30)]
    return {"base": "section", "tod": "dusk", "ground": GY, "lx": -400, "layers": layers, "cam": CAM, "els": els}


def s7():
    """One Clovis point, large: flake scars, the flute from the base glowing; a shaft slides into the flute and is bound on."""
    tf, ts, tc = T("s7", "fluted"), T("s7", "shaft"), T("s7", "Clovis points")
    X0, Y0, H = 600, 470, 640                              # base at (X0, Y0), tip to the right
    s = H / 80
    P = lambda a, b: (X0 - b * s, Y0 + a * s)              # local (a across, b along: tip at b = -80)
    half = lambda b: 14.2 if -40 <= b <= -14 else (11.5 + (b + 54) * .14 if b < -40 else 12.8)
    els = [ln([(110, Y0), (X0 + 150, Y0)], ts, WOOD, 32, dur=.9), ln([(110, Y0 - 10), (X0 + 150, Y0 - 10)], ts, "#b08a62", 4, dur=.9, op=.6)]
    els += stone_point(X0, Y0, H, .3, "#d3cbba", "#f5ecdc", ang=90, flute=False, w=2.5)
    for k in range(11):                                     # pressure-flake scars from both edges towards the middle
        b = -9 - 56 * k / 10
        for side in (-1, 1):
            e = half(b) * .93
            els.append(ln([P(side * e, b), P(side * e * .55, b - 3.5), P(side * 1.5, b - 5)], round(.6 + .03 * k, 2), "#a49c8a", 2.4, draw=False, curve=True, op=.75))
    flute = [P(-3.6, -3.5), P(3.6, -3.5), P(3.3, -26), P(1.6, -31), P(0, -32), P(-1.6, -31), P(-3.3, -26)]
    els += [poly(flute, "#9c927e", "#f8f0e0", 2, tf, curve=True, fx="fill"), glow(*P(0, -18), 130, tf + .1, .55, "lamp"),
            ln([P(0, -20), (1020, 260)], tf + .3, GOLD, 2, dur=.4), lab(1036, 252, "flute", tf + .4, GOLD, 34, "start")]
    els += [ln([(X0 - 40 + 16 * k, Y0 - 24), (X0 - 22 + 16 * k, Y0 + 24)], round(ts + .7 + .06 * k, 2), "#e2d2b0", 4, draw=False) for k in range(6)]
    els += [lab(330, Y0 + 72, "shaft", ts + .5, "#d9c2a0", 30), lab(1000, 690, "Clovis point", tc, BONE, 36)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [glow(900, 470, 460, -1, .18, "lamp")] + els}


def _na_ring():
    """The land ring of North America (the one that holds Kansas)."""
    for poly_ in films._topo():
        ring = poly_[0]
        xs = [q[0] for q in ring]; ys = [q[1] for q in ring]
        if min(xs) < -100 < max(xs) and min(ys) < 40 < max(ys) and max(xs) - min(xs) < 180 and _inside(ring, -100, 40):
            return ring
    raise ValueError("no North America ring")


def _inside(ring, lo, la):
    c = False
    for i in range(len(ring)):
        (x1, y1), (x2, y2) = ring[i - 1], ring[i]
        if (y1 > la) != (y2 > la) and lo < (x2 - x1) * (la - y1) / ((y2 - y1) or 1e-9) + x1:
            c = not c
    return c


def s8():
    """Fluted points across North America: about fifty pop from the southern plains outward."""
    m = Map(-128, -62, 14, 56)
    ring = _na_ring()
    r = random.Random(21)
    pts = []
    for _ in range(20000):
        if len(pts) >= 52:
            break
        lo, la = r.uniform(-123, -67), r.uniform(26, 50)
        if la > 47 and r.random() < .6:
            continue
        if lo < -110 and r.random() < .45:                  # fewer in the far west
            continue
        if _inside(ring, lo, la) and all(abs(lo - a) + abs(la - b) > 2.2 for a, b in pts):
            pts.append((lo, la))
    cl = SITE["clovis"]
    pts.sort(key=lambda q: math.hypot(q[0] - cl[0], (q[1] - cl[1]) * 1.2))
    els = [land_el(m.land(), -1)]
    cx, cy = m.p(*cl)
    k = 0
    for lo, la in pts:
        x, y = m.p(lo, la)
        if cx - 300 < x < cx + 36 and cy - 34 < y + 14 < cy + 70:          # keep the pin and its label clear
            continue
        els += stone_point(x, y + 14, 30, round(.5 + .05 * k, 2), "#e2d9c6", "#fff6e6", w=1, flute=False)
        k += 1
    els += [pin(cx, cy, "Clovis, New Mexico", .3, GOLD, "end", -18, 32), lab(150, 190, "Clovis points", 1.2, BONE, 34, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def s9():
    """The carbon clock: a mammoth bone and charcoal with their carbon-14; candles burning down as it fades; what's left tells the time."""
    tc, tf, tl = T("s9", "radioactive carbon"), T("s9", "fades after death"), T("s9", "See what's left")
    els = bone(130, 560, 360, 520, .3, 16) + [poly([(180, 660), (230, 630), (300, 640), (330, 676), (280, 700), (200, 694)], "#1d1916", "#5c5148", 1.5, .4)]
    r = random.Random(4)
    for j in range(12):
        els.append(dot(round(r.uniform(150, 340), 1), round(r.uniform(440, 480), 1), 6, BLUE, round(tc + .05 * j, 2)))
    els += [lab(245, 760, "bone and charcoal", .5, MUTED, 26), lab(245, 410, "carbon-14", tc + .3, BLUE, 26),
            arrow([[420, 560], [530, 560]], tf - .2, AMBER, 3, dur=.4, curve=False)]
    base = 690
    for j, (x, h, n) in enumerate(((680, 330, 16), (900, 230, 8), (1120, 140, 4), (1340, 60, 2))):
        t = tf + .6 * j
        els += candle(x, base, h, t)
        for q in range(n):
            els.append(dot(round(x - 24 + (q % 4) * 16, 1), round(base - h - 80 - (q // 4) * 16, 1), 5, BLUE, round(t + .3 + .02 * q, 2)))
    els += [arrow([[640, 740], [1460, 740]], tf + .4, AMBER, 3, dur=2.0, curve=False), lab(1050, 782, "time since death", tf + 1.0, AMBER, 26)]
    els += [{"k": "dim", "x1": 1400, "y1": base, "x2": 1400, "y2": base - 60, "t": "", "c": GOLD, "dur": .5, "in": round(tl, 2)},
            lab(1425, 604, "what's left", tl + .2, GOLD, 28, "start"), lab(1425, 642, "tells the time", tl + .5, GOLD, 28, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def XC(ya):                                     # the short axis of the Clovis dates: 14,000 years ago at x 200, 12,000 at x 1580
    return round(200 + (14000 - ya) / 2000 * 1380, 1)


def s10():
    """Dates again and again: twenty radiocarbon dates stack into a tight pile between 13,050 and 12,750 years ago."""
    tn = T("s10", "thirteen thousand")
    AY = 560
    els = [axis(200, 1580, AY, [(XC(v), "{:,}".format(v)) for v in (14000, 13500, 13000, 12500, 12000)], .2, "years ago"),
           rect(XC(13050), 300, XC(12750) - XC(13050), AY - 300, "rgba(242,201,142,.12)", at=.4)]
    cols = [XC(13050) + 16 + 25 * k for k in range(8)]
    heights = [1, 2, 4, 5, 5, 4, 2, 1]
    k = 0
    for c, h in zip(cols, heights):
        for q in range(h):
            els.append(rect(c - 10, AY - 30 - 28 * q, 20, 24, GOLD, "#fff1d0", 1, 3, round(.6 + .06 * k, 2), fx="pop"))
            k += 1
    els += [glow((XC(13050) + XC(12750)) / 2, AY - 60, 160, 1.6, .5, "lamp"), lab((XC(13050) + XC(12750)) / 2, 250, "about 13,000 years ago", max(1.8, tn), GOLD, 34),
            lab((XC(13050) + XC(12750)) / 2, 680, "13,050 to 12,750", 2.4, MUTED, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


BRIDGE = [(175, 69.5), (178, 71.6), (186, 73.2), (196, 72.8), (204, 71.4), (206, 66), (204, 60), (198, 55.2), (194.5, 54.3), (190, 56.2), (186.5, 59.2),
          (182, 61.2), (178.5, 62.6), (175, 64.5), (173, 67)]


def s11():
    """Siberia and Alaska; in the Ice Age the shallow sea floor between them rises as land: Beringia."""
    tj, tb = T("s11", "joined by land"), T("s11", "Beringia")
    m = Map(140, 236, 50, 76, (90, 130, 1600, 660))
    els = [poly(m.path(BRIDGE), "#6e5c45", "#e3c99c", 2.5, tj, curve=True, style="inferred", dur=1.2), land_el(m.land(), -1),
           glow(*m.p(187, 66), 220, tj + .2, .3, "lamp")]
    els += [lab(*m.p(152, 64), "Asia", .4, MUTED, 32), lab(*m.p(212, 64), "Alaska", .4, MUTED, 32),
            lab(*m.p(187, 66.5), "Beringia", tb, "#fff1d0", 40, st="ital"), lab(889, 760, "the sea about 120 m lower", tj + .6, BLUE, 26)]
    return {"base": "map", "cam": CAM, "els": els}


GLOBE12 = (-98, 12, 380, 700, 468)


def s12():
    """The Clovis-first model on a globe: the two ice sheets apart, a dotted route from Beringia down the gap and on to the tip of
    South America; 'Clovis first' and three ticks: ice, points, dates."""
    tg, tt, tc, tf = T("s12", "walked south"), T("s12", "tip of South"), T("s12", "Clovis first"), T("s12", "It fitted")
    g = Globe(*GLOBE12)
    lon0, lat0, Rr, cx, cy = GLOBE12
    route = [g.p(lo, la) for lo, la in [(-163, 66), (-150, 64), (-132, 61), (-120, 58), (-115, 53), (-110, 47), (-104, 38), (-100, 28), (-93, 18), (-84, 10),
                                         (-78, 3), (-79, -5), (-75, -15), (-70, -25), (-71, -36), (-73, -45), (-71, -52)]]
    gap = g.p(-118, 57)
    els = [circ(cx, cy, Rr, "#163447", at=-1), land_el(g.land(), -1, "#5b4a36"), circ(cx, cy, Rr + 4, "none", "#9fd0ff", 5, -1, op=.3),
           poly([g.p(lo, la) for lo, la in BERINGIA], "#6e5c45", "#e3c99c", 2, -1, curve=True, style="inferred"),
           poly([g.p(lo, la) for lo, la in LAUR_OPEN], "rgba(233,242,251,.92)", ICE_E, 1.5, .3, curve=True),
           poly([g.p(lo, la) for lo, la in CORD_OPEN], "rgba(233,242,251,.92)", ICE_E, 1.5, .3, curve=True),
           arrow(route, tg, "#ddd6ff", 5, "claimed", dur=max(1.5, tt - tg + .6)),
           ln([(gap[0] - 8, gap[1] + 4), (330, 250)], tg - .1, BONE, 2, dur=.4), lab(316, 244, "the gap", tg, BONE, 30, "end")]
    els += chip(1400, 290, "Clovis first", LILAC, tc, 34)
    for k, w in enumerate(("ice", "points", "dates")):
        els += [tick(1310, 420 + 74 * k, round(tf + .45 * k, 2), GREEN), lab(1352, 432 + 74 * k, w, round(tf + .45 * k, 2), BONE, 32, "start")]
    return {"base": "dark", "stars": 120, "cam": CAM, "els": els}


def _card(x, y, w, h, at, c=BONE):
    return rect(x, y, w, h, "rgba(245,236,220,.05)", c, 2, 16, at, fx="pop", op=.95)


CARDS = (150, 689, 1228)                         # the three test cards: left edges (each 400 wide), y 150..640


def s13():
    """Three tests for an older site, drawn as they are named: real tools or bones; undisturbed layers; sound dates."""
    t1, t2, t3 = T("s13", "real tools"), T("s13", "undisturbed"), T("s13", "sound dates")
    els = []
    for x, t, name in zip(CARDS, (t1, t2, t3), ("real tools or bones", "undisturbed layers", "sound dates")):
        els += [_card(x, 150, 400, 490, t - .2), lab(x + 200, 700, name, t + .2, BONE, 30)]
    x = CARDS[0]
    els += stone_point(x + 140, 370, 170, t1, "#d6cebd") + bone(x + 230, 340, x + 330, 250, t1 + .2, 12)
    x = CARDS[1]
    for k, c in enumerate(("#8a7356", "#a39072", "#77705f", "#93806a", "#5f4c39")):
        els.append(rect(x + 60, 200 + 36 * k, 280, 36, c, at=round(t2 + .08 * k, 2), fx="fill", dur=.3))
    x = CARDS[2]
    els += candle(x + 200, 380, 150, t3)
    els += [tick(x + 300, 250, t3 + .5, GREEN)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s14_add():
    """How claims failed: a rock split by frost; layers churned by roots and a burrow; a date on an old drifted log. Each crossed out."""
    t1, t2, t3 = T("s14", "rocks broken"), T("s14", "layers churned"), T("s14", "dates on the wrong")
    els = []
    x = CARDS[0]
    els += [poly([(x + 110, 560), (x + 150, 470), (x + 196, 456), (x + 188, 520), (x + 170, 566)], "#9a9184", "#e9e1d2", 1.5, t1),
            poly([(x + 206, 456), (x + 250, 470), (x + 290, 540), (x + 250, 570), (x + 198, 528)], "#8a8174", "#e9e1d2", 1.5, t1 + .1),
            ln([(x + 196, 456), (x + 190, 500), (x + 200, 530), (x + 186, 568)], t1 + .2, "#2a2420", 2.5, dur=.3)] + cross(x + 330, 470, t1 + .6)
    x = CARDS[1]
    for k, c in enumerate(("#8a7356", "#a39072", "#77705f", "#93806a")):
        els.append(rect(x + 60, 440 + 36 * k, 280, 36, c, at=t2))
    els += [ln([(x + 120, 440), (x + 136, 480), (x + 118, 520), (x + 140, 572)], t2 + .2, "#3d2f22", 4, dur=.5, curve=True),
            ln([(x + 136, 480), (x + 170, 500)], t2 + .3, "#3d2f22", 3, dur=.3), circ(x + 250, 520, 26, "#2a2018", "#5a4632", 2, t2 + .35, fx="pop"),
            ln([(x + 250, 494), (x + 262, 440)], t2 + .35, "#2a2018", 14, draw=False)] + cross(x + 330, 470, t2 + .7)
    x = CARDS[2]
    els += [poly([(x + 70, 540), (x + 300, 520), (x + 316, 556), (x + 84, 580)], "#6b4a30", "#b08a62", 1.5, t3),
            ln([(x + 100, 548), (x + 290, 532)], t3, "#8a6440", 2, draw=False)] + tag(x + 190, 488, "dated", t3 + .3, AMBER, 24) + cross(x + 330, 470, t3 + .7)
    els += [lab(CARDS[0] + 200, 620, "broken by nature", t1 + .4, RED, 24), lab(CARDS[1] + 200, 620, "churned", t2 + .4, RED, 24),
            lab(CARDS[2] + 200, 620, "the wrong material", t3 + .4, RED, 24)]
    return els


def XW(ya):                                     # the wall's axis: 25,000 years ago at x 160, 10,000 at x 1600
    return round(160 + (25000 - ya) / 15000 * 1440, 1)


def wall_bricks(x, y0, y1, at, w=46, fx="fill"):
    out = [rect(x - w / 2, y0, w, y1 - y0, "#b9a47c", "#e8d6b0", 2, 3, at, fx=fx, dur=.7)]
    out += [ln([(x - w / 2, yy), (x + w / 2, yy)], at + .5, "#8a7356", 1.5, draw=False) for yy in range(int(y0) + 32, int(y1), 32)]
    out += [ln([(x + (8 if (yy // 32) % 2 else -8), yy), (x + (8 if (yy // 32) % 2 else -8), yy + 32)], at + .5, "#8a7356", 1.2, draw=False) for yy in range(int(y0), int(y1) - 31, 32)]
    return out


def wall_axis(at=.2):
    return [axis(160, 1600, 660, [(XW(v), "{:,}".format(v)) for v in (25000, 20000, 15000, 10000)], at, "years ago")]


def s15():
    """A wall at 13,000 years on the axis; three older claimed dates fly at it and bounce back."""
    tw, tb = T("s15", "wall"), T("s15", "older dates")
    WX = XW(13000)
    els = wall_axis() + wall_bricks(WX, 250, 660, tw - .3) + [lab(WX, 226, "13,000", tw, AMBER, 34)]
    for k, (ya, y) in enumerate(((20000, 330), (17000, 430), (22500, 540))):
        t = round(tb + .45 * k, 2)
        els += [dot(XW(ya), y, 14, "#cbbca8", t), ln([(XW(ya) + 16, y), (WX - 26, y)], t + .2, "#cbbca8", 3, "inferred", .5),
                arrow([[WX - 26, y], [WX - 110, y + 26], [XW(ya) + 70, y + 40]], t + .7, RED, 3, "claimed", .6)]
    els += [lab(XW(20000), 280, "older claims", tb, MUTED, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== chapter 2: a camp in Chile
GLOBE16 = (-86, -6, 372, 600, 468)


def creek_inset(cx, cy, r, at):
    """A round window on the creek of Monte Verde from above: forest, a winding creek, the camp beside it."""
    rr = random.Random(16)
    els = [circ(cx, cy, r, "#2c3a26", "#e3c99c", 3, at, fx="pop")]
    trees = []
    for q in range(46):
        a, d = rr.uniform(0, 2 * math.pi), r * math.sqrt(rr.uniform(0, 1)) * .92
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        trees.append(circ(x, y, rr.uniform(10, 18), rr.choice(["#3e5a32", "#4a6a3a", "#35502c"]), at=at + .1, op=.95))
    creek = [(cx - r * .95, cy - r * .3), (cx - r * .5, cy - r * .05), (cx - r * .15, cy - r * .32), (cx + r * .2, cy - r * .02), (cx + r * .5, cy + r * .25), (cx + r * .95, cy + r * .2)]
    els += trees + [ln(creek, at + .3, "#7fb6d6", 12, curve=True, dur=.8), circ(cx + r * .02, cy - r * .2 + 34, 12, GOLD, "#fff1d0", 2, at + .8, fx="pop"),
                    glow(cx + r * .02, cy - r * .2 + 34, 50, at + .8, .9, "lamp")]
    return els


def s16():
    """South America on the globe: a gold pin at Monte Verde, southern Chile; beside it, a window on a winding creek in the forest."""
    g = Globe(*GLOBE16)
    lon0, lat0, Rr, cx, cy = GLOBE16
    mv = g.p(*SITE["monteverde"])
    els = [circ(cx, cy, Rr, "#163447", at=-1), land_el(g.land(), -1, "#5b4a36"), circ(cx, cy, Rr + 4, "none", "#9fd0ff", 5, -1, op=.3),
           pin(mv[0], mv[1], "Monte Verde", .5, GOLD, "end", -20, 8, tc=GOLD), lab(mv[0] + 64, mv[1] - 70, "Chile", .9, MUTED, 28)]
    els += creek_inset(1330, 430, 230, 1.0) + [ln([mv, (1100, 520)], 1.0, "#e3c99c", 2, "inferred", .5), lab(1330, 700, "a creek in the forest", 1.6, BONE, 28)]
    return {"base": "dark", "stars": 120, "cam": CAM, "els": els}


def s19_add():
    """Clovis, far to the north, 13,000; Monte Verde, 14,500; a gold line between them: a whole continent."""
    tn, tc = T("s19", "fourteen and a half"), T("s19", "Older than Clovis")
    g = Globe(*GLOBE16)
    cl, mv = g.p(*SITE["clovis"]), g.p(*SITE["monteverde"])
    path = [g.p(SITE["clovis"][0] + (SITE["monteverde"][0] - SITE["clovis"][0]) * t, SITE["clovis"][1] + (SITE["monteverde"][1] - SITE["clovis"][1]) * t) for t in [q / 24 for q in range(25)]]
    return ([pin(cl[0], cl[1], "Clovis", tc, AMBER, "end", -20, 8)] + tag(mv[0] - 120, mv[1] + 56, "14,500", tn, GOLD, 30) +
            tag(cl[0] - 100, cl[1] + 50, "13,000", tc + .3, AMBER, 28) + [ln(path, tc + .6, GOLD, 3, dur=1.4, curve=True, op=.9),
            lab(830, 470, "a whole continent", tc + 1.6, GOLD, 30, "start")])


def s17():
    """A creek bank in cross-section: a thick dark peat layer lies over the camp like a lid; the creek has cut the bank open; diggers
    at the cut (1977); air stops at the peat; wood and plants below kept; a sealed jar beside it."""
    tp, tj, ta = T("s17", "A peat bog"), T("s17", "like food"), T("s17", "no air")
    GY = 250
    PT, CT, CB = GY + 60, GY + 250, GY + 400                       # peat top, camp top, camp bottom
    rr = random.Random(17)
    els = [rect(-20, GY, 1840, 60, "#5a4632", at=-1), rect(-20, PT, 1840, CT - PT, "#2b221a", at=-1), rect(-20, CT, 1840, CB - CT, "#8c7a5c", at=-1),
           rect(-20, CB, 1840, 400, "#6d6250", at=-1)]
    els += [ln([(x, PT + 12 + rr.uniform(0, 150)), (x + rr.uniform(30, 90), PT + 12 + rr.uniform(0, 150))], -1, "#3f3226", 2, draw=False, op=.8) for x in range(0, 1400, 40)]
    creek = [(1380, GY - 2), (1460, CT - 40), (1520, CB + 20), (1800, CB + 20), (1800, GY - 2)]
    els += [poly(creek, "#9fbfcf", at=-1, op=.25), poly([(1500, CB - 30), (1530, CB + 20), (1800, CB + 20), (1800, CB - 30)], "#3f6f8c", at=-1),
            ln([(1510, CB - 28), (1800, CB - 28)], -1, "#bfe3f5", 2, draw=False, op=.6), ln([(1380, GY), (1460, CT - 40), (1520, CB + 20)], -1, "#e3c99c", 2, draw=False, op=.7)]
    for k in range(8):
        x = 120 + 160 * k + rr.uniform(-30, 30)
        els += [ln([(x, GY), (x, GY - 60)], -1, "#3a2c20", 8, draw=False), circ(x, GY - 100, rr.uniform(46, 60), "#34502e", at=-1), circ(x + 26, GY - 82, 38, "#3e5c34", at=-1)]
    els += [figure(1290, GY, 104, .3, "#1e1813"), figure(1350, GY, 96, .45, "#1e1813"), lab(1180, GY - 60, "1977", .5, BONE, 36, "end")]
    for k, x in enumerate((300, 380, 470, 900, 990)):
        els += [ln([(x, CT + 120), (x + 8, CT + 10)], round(tp + .6 + .1 * k, 2), WOOD, 12, draw=False), glow(x, CT + 70, 44, round(tp + .6 + .1 * k, 2), .45, "lamp")]
    els += [poly([(560, CT + 110), (800, CT + 94), (806, CT + 120), (566, CT + 134)], WOOD, "#b08a62", 1.5, tp + 1.0)]
    els += [circ(640 + 34 * q, CT + 60 + (q % 2) * 12, 9, "#8fbf6a", at=round(tp + 1.1 + .05 * q, 2)) for q in range(5)]
    els += [lab(1080, PT + 110, "peat", tp, "#e3d2b8", 34), lab(1180, CT + 85, "the camp", tp + .5, GOLD, 32)]
    for k, x in enumerate((420, 640, 860, 1080)):
        t = round(ta + .1 * k, 2)
        els += [arrow([[x, 140], [x, PT - 6]], t, BLUE, 3, dur=.5, curve=False), ln([(x - 22, PT - 2), (x + 22, PT - 2)], t + .5, RED, 4, dur=.2)]
    els += [lab(390, 190, "no air", ta + .4, BLUE, 30, "end")]
    jx, jy = 190, 520
    els += [rect(jx - 70, jy - 60, 140, 150, "rgba(159,208,255,.12)", "#cfe6ff", 2.5, 18, tj, fx="pop"), rect(jx - 80, jy - 82, 160, 26, "#8a7356", "#e3c99c", 2, 6, tj),
            circ(jx - 24, jy + 40, 22, "#c0503a", at=tj + .2), circ(jx + 22, jy + 50, 18, "#8fbf6a", at=tj + .25), circ(jx + 8, jy + 14, 16, "#e8b87a", at=tj + .3),
            lab(jx, jy + 140, "a sealed jar", tj + .3, "#cfe6ff", 26)]
    return {"base": "sky", "tod": "day", "ground": GY, "sun": [800, 120, 18], "ridges": [], "cam": CAM, "els": els}


def potato(x, y, s, at):
    return [poly(E(x, y, 16 * s, 11 * s, 14), "#a97c50", "#d9b383", 1.2, at, fx="pop", curve=True), dot(x - 4 * s, y - 2 * s, 1.6 * s, "#5a4024", at), dot(x + 6 * s, y + 3 * s, 1.4 * s, "#5a4024", at)]


def s18():
    """The camp rebuilt: a long hut frame of poles (solid: the wood found) under a dashed hide roof (inferred); hearths; mastodon
    meat and hide; wild potatoes; seaweed. Each as it is named."""
    th, tr, tm, tp, ts = T("s18", "wooden frames"), T("s18", "Hearths"), T("s18", "Meat and hide"), T("s18", "Wild potatoes"), T("s18", "chewed seaweed")
    GY = 650
    rr = random.Random(18)
    els = [poly([(-20, 520), (200, 470), (420, 505), (640, 460), (880, 500), (1100, 455), (1340, 495), (1560, 470), (1800, 500), (1800, 660), (-20, 660)], "#1f2c1c", at=-1, curve=True)]
    for k in range(16):
        x = 40 + 112 * k + rr.uniform(-20, 20)
        y = 500 - 22 * math.sin(k * .9)
        els += [conifer(x, y + 30, rr.uniform(80, 120), -1, "#182416", None)]
    xs = [140 + 66 * k for k in range(10)]
    for k, x in enumerate(xs):                                           # poles of the long frame
        els.append(ln([(x, GY), (x, GY - 210 - 10 * math.sin(k))], round(th + .05 * k, 2), WOOD, 11, draw=False))
    els += [ln([(126, GY - 210), (xs[-1] + 14, GY - 210)], th + .4, WOOD, 9, draw=False), ln([(126, GY - 140), (xs[-1] + 14, GY - 140)], th + .45, WOOD, 7, draw=False),
            poly([(100, GY - 210), (430, GY - 320), (xs[-1] + 44, GY - 210)], "rgba(201,160,112,.14)", "#c9a070", 3, th + .6, style="inferred")]
    els += [figure(560, GY, 130, .4, "#140f0c"), figure(640, GY, 116, .5, "#140f0c"), lab(430, 250, "huts", th + .3, BONE, 32)]
    for k, x in enumerate((880, 1010)):
        t = round(tr + .15 * k, 2)
        els += [glow(x, GY - 24, 90, t, .95, "fire"), poly([(x - 24, GY), (x - 4, GY - 56), (x + 4, GY - 30), (x + 14, GY - 48), (x + 24, GY)], "#ffb36a", at=t, fx="pop"),
                circ(x - 34, GY - 2, 10, "#7a6a5a", at=t), circ(x + 34, GY - 2, 10, "#7a6a5a", at=t)]
    els += [lab(945, 470, "hearths", tr + .3, "#ffd8a0", 30)]
    els += [poly([(1120, GY - 6), (1220, GY - 46), (1310, GY - 36), (1324, GY), (1132, GY + 8)], "#7c3a30", "#c9756a", 2, tm, fx="pop"),
            poly([(1100, GY + 10), (1176, GY - 20), (1226, GY - 8), (1214, GY + 16)], "#5a4636", "#a08060", 1.5, tm + .1, fx="pop"),
            lab(1215, 540, "mastodon meat", tm + .3, "#f0b2a6", 30)]
    for q in range(7):
        els += potato(1400 + (q % 4) * 38 - (q // 4) * -18, GY - 12 - (q // 4) * 26, 1.3, round(tp + .05 * q, 2))
    els += [lab(1450, 470, "wild potatoes", tp + .3, "#e8c896", 30)]
    for q in range(6):
        x0 = 1580 + 22 * q
        els.append(ln([(x0, GY), (x0 + 10, GY - 26), (x0 - 5, GY - 52), (x0 + 8, GY - 76)], round(ts + .06 * q, 2), "#6fae6a", 6, dur=.4, curve=True))
    els += [lab(1610, 540, "seaweed", ts + .3, GREEN, 30)]
    return {"base": "sky", "tod": "dusk", "ground": GY, "sun": [260, 170, 16], "ridges": [], "groundc": "#3d3226", "cam": CAM, "els": els}


def s20():
    """One man with his box of finds; facing him, nine figures with question marks; twenty years of reports pile up beside him."""
    t20 = T("s20", "For twenty years")
    els = [figure(330, 640, 150, .3, "#e8d6b8"), rect(400, 600, 120, 40, "#6b5a48", "#cbb79a", 1.5, 4, .4),
           ln([(430, 600), (436, 560)], .5, WOOD, 7, draw=False)] + stone_point(480, 598, 40, .5, flute=False)
    for k in range(9):
        x = 900 + 80 * k
        els += [figure(x, 640, 120 + 6 * (k % 3), round(.4 + .06 * k, 2), "#9a8f80")] + [lab(x, 470 - 6 * (k % 3), "?", round(.9 + .08 * k, 2), LILAC, 46, st="big", fx="pop")]
    for k in range(20):
        els.append(rect(180, 620 - 9 * k, 90, 8, "#efe3c8", "#8a7a62", 1, 1, round(t20 + .08 * k, 2), fx="pop"))
    els += [ln([(200, 720), (1600, 720)], t20, GOLD, 3, dur=1.6), lab(200, 765, "1977", t20, GOLD, 28), lab(1600, 765, "1997", t20 + 1.6, GOLD, 28),
            lab(900, 704, "twenty years", t20 + .8, GOLD, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s21():
    """1997: nine experts stand round the finds table; on 'agreed', green ticks pop over them one after another."""
    ta = T("s21", "and agreed", -.15)
    els = [rect(690, 560, 400, 26, "#6b5a48", "#cbb79a", 1.5, 4, .3), ln([(710, 586), (710, 640)], .3, "#6b5a48", 6, draw=False),
           ln([(1070, 586), (1070, 640)], .3, "#6b5a48", 6, draw=False), ln([(760, 560), (770, 500)], .5, WOOD, 9, draw=False),
           poly([(840, 556), (960, 540), (966, 556), (846, 562)], WOOD, "#b08a62", 1.2, .5)] + stone_point(1020, 556, 50, .6, flute=False) + [glow(889, 540, 220, .6, .35, "lamp")]
    pos = [(420, 640), (510, 650), (600, 640), (1160, 640), (1250, 650), (1340, 640), (1430, 650), (330, 650), (1520, 640)]
    for k, (x, y) in enumerate(pos):
        els += [figure(x, y, 132, round(.3 + .05 * k, 2), "#cbbca8"), tick(x, y - 175, round(ta + .04 * k, 2), GREEN, 1.1)]
    els += [lab(889, 210, "1997", .5, GOLD, 40)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s22():
    """The wall again, with a gold dot beyond it at 14,500 (Monte Verde); a crack runs down the wall with a flash."""
    tc = T("s22", "first crack", -.4)
    WX = XW(13000)
    mv = (XW(14500), 400)
    els = wall_axis(-1) + static(wall_bricks(WX, 250, 660, 0)) + [lab(WX, 226, "13,000", -1, AMBER, 34)]
    els += [glow(mv[0], mv[1], 70, .3, .8, "lamp"), dot(mv[0], mv[1], 15, GOLD, .3), lab(mv[0] - 26, mv[1] + 10, "Monte Verde", .5, GOLD, 30, "end"),
            lab(mv[0] - 26, mv[1] + 46, "14,500", .6, GOLD, 26, "end")]
    els += [ln([(WX + 4, 252), (WX - 10, 320), (WX + 10, 380), (WX - 8, 450), (WX + 8, 530), (WX - 6, 600), (WX + 4, 658)], tc, "#fffaf0", 5, dur=.7),
            glow(WX, 450, 140, tc, .9, "lamp")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s23():
    """Paisley Caves: a rock shelter at the foot of a basalt rim above an old lake basin; a coprolite in its floor; DNA and
    chemistry both say human."""
    tc, td, tm = T("s23", "dried human dung"), T("s23", "its DNA"), T("s23", "its chemistry")
    GY = 600
    rr = random.Random(23)
    top = [(-20, 300), (80, 286), (160, 296), (240, 276), (330, 288), (420, 270), (520, 282), (610, 268), (700, 284), (790, 276), (860, 300), (920, 360),
           (950, 450), (980, GY)]
    els = [poly([(940, GY - 4), (1800, GY - 30), (1800, GY + 4)], "#d9cdb4", at=-1, op=.6), lab(1180, GY + 40, "the old lake bed", .3, MUTED, 24)]
    els += [poly(top + [(-20, GY)], "#3a3431", "#80746a", 2, -1)]
    for k in range(18):                                                 # columnar joints
        x = 20 + 52 * k + rr.uniform(-8, 8)
        els.append(ln([(x, 300 + rr.uniform(-6, 10)), (x + rr.uniform(-10, 10), GY - 160)], -1, "#26211f", 2.5, draw=False, op=.8))
    els += [poly([(180, GY), (230, GY - 120), (330, GY - 175), (470, GY - 190), (600, GY - 160), (690, GY - 100), (730, GY)], "#1b1715", "#5a4f48", 2, -1, curve=True),
            poly([(250, GY), (300, GY - 90), (400, GY - 130), (520, GY - 128), (620, GY - 80), (660, GY)], "#0f0c0b", at=-1, curve=True),
            poly([(730, GY), (800, GY - 60), (900, GY - 40), (960, GY)], "#8a7f72", at=-1, curve=True)]
    els += [rect(220, GY, 480, 150, "#6b5844", at=-1), rect(220, GY + 50, 480, 46, "#57493a", at=-1), rect(220, GY, 480, 150, "none", "#c9b9a0", 1.5, 0, -1, style="inferred")]
    cx, cy = 470, GY + 72
    els += [poly(E(cx, cy, 28, 15, 16), "#6a4a2a", "#b08a62", 1.5, tc, fx="pop", curve=True), glow(cx, cy, 80, tc, .85, "lamp"),
            ln([(cx + 30, cy - 4), (760, GY + 110)], tc + .3, GOLD, 2, dur=.4)] + tag(900, GY + 120, "over 14,000 years", tc + .5, GOLD, 26)
    els += helix(1150, 280, 1520, 280, td, n=14, amp=22) + [tick(1580, 276, td + .9, GREEN), lab(1330, 360, "DNA: human", td + .6, BONE, 30)]
    els += flask(1330, 500, 1.3, tm) + [tick(1440, 420, tm + .6, GREEN), lab(1330, 540, "chemistry: human", tm + .4, BONE, 30)]
    els += [lab(120, 200, "Paisley Caves, Oregon", .5, BONE, 32, "start")]
    return {"base": "sky", "tod": "day", "ground": GY, "sun": [1480, 150, 22], "ridges": [], "groundc": "#7a6a55", "cam": CAM, "els": els}


def s24():
    """Cooper's Ferry: a terrace above the lower Salmon River in its canyon, cut by a trench; in the lowest layer a hearth, pits and
    stone tools (a stemmed point)."""
    th, tp, tt, ta = T("s24", "a hearth"), T("s24", "pits"), T("s24", "stone tools"), T("s24", "about sixteen")
    GY = 360
    els = [poly([(-20, 140), (300, 200), (600, 300), (760, GY), (-20, GY)], "#5d5a3e", "#8a8660", 2, -1),
           poly([(1100, GY + 120), (1300, 260), (1560, 170), (1800, 150), (1800, GY + 200)], "#57543a", "#8a8660", 2, -1)]
    els += [rect(-20, GY, 1180, 460, "#8a7356", at=-1), rect(-20, GY + 120, 1180, 120, "#9c8466", at=-1), rect(-20, GY + 240, 1180, 220, "#6f5a44", at=-1),
            poly([(1160, GY), (1250, GY + 240), (1800, GY + 240), (1800, GY + 460), (1160, GY + 460)], "#3f5f74", at=-1),
            rect(1250, GY + 236, 560, 10, "#9fc3d8", at=-1, op=.4)]
    els += [lab(1500, GY + 300, "Salmon River", .4, "#cfe6ff", 26)]
    ly = GY + 330
    els += [glow(300, ly, 90, th, .95, "fire"), poly([(270, ly + 4), (300, ly - 34), (330, ly + 4)], "#ffb36a", at=th, fx="pop")]
    els += [poly([(460, ly - 20), (470, ly + 40), (560, ly + 44), (570, ly - 20)], "#2a2018", "#5a4632", 2, tp, curve=True, fx="pop"),
            poly([(640, ly - 20), (652, ly + 30), (720, ly + 34), (730, ly - 20)], "#2a2018", "#5a4632", 2, tp + .2, curve=True, fx="pop")]
    for k, (x, a) in enumerate(((820, 70), (880, -40), (960, 100))):
        els += stone_point(x, ly + 10, 36, round(tt + .15 * k, 2), "#d8cfbf", ang=a, flute=False)
    els += stone_point(1040, ly + 30, 70, tt + .5, "#e2d9c6", stemmed=True) + [glow(1040, ly, 60, tt + .5, .7, "lamp")]
    els += [lab(120, 200, "Cooper's Ferry, Idaho", .5, BONE, 32, "start"), lab(120, 240, "Nez Perce village of Nipéhe", .9, MUTED, 24, "start"),
            lab(640, ly + 84, "about 16,000 years", ta, GOLD, 30)]
    return {"base": "sky", "tod": "day", "ground": GY, "sun": [1500, 120, 22], "ridges": [], "cam": CAM, "els": els}


UT, LT = 300, 430                                       # upper and lower terrace surfaces of the creek valley


def s25():
    """The creek valley in cross-section: an upper terrace, a lower terrace with the camp, the creek; 2026: a team samples a cut bank
    on the upper terrace, some distance away."""
    terr = [(-20, UT), (520, UT), (600, LT), (1250, LT), (1330, 560), (1560, 560), (1640, LT + 10), (1800, LT), (1800, 1010), (-20, 1010)]
    els = [poly(terr, "#8a7356", "#e3c99c", 2, -1)]
    for k, (y, c) in enumerate(((LT + 40, "#9c8466"), (LT + 130, "#77705f"), (LT + 230, "#8c7a5c"), (LT + 330, "#6d6250"))):
        els.append(poly([(-20, y), (1800, y + 8 * math.sin(k)), (1800, y + 70), (-20, y + 70)], c, at=-1, op=.5))
    els += [rect(1330, 528, 230, 32, "#4f8fb0", at=-1), ln([(1340, 534), (1550, 534)], -1, "#bfe3f5", 2, draw=False, op=.6)]
    rr = random.Random(25)
    for k in range(12):
        x = 60 + 140 * k + rr.uniform(-20, 20)
        if 500 < x < 640 or 1240 < x < 1660:
            continue
        y = UT if x < 520 else LT
        els += [ln([(x, y), (x, y - 46)], -1, "#3a2c20", 6, draw=False), circ(x, y - 76, rr.uniform(32, 42), "#34502e", at=-1)]
    els += [rect(820, LT - 14, 200, 16, GOLD, "#fff1d0", 1.5, 4, .4), glow(920, LT - 6, 100, .4, .7, "lamp"), lab(920, LT - 40, "the camp", .6, GOLD, 30)]
    els += [rect(520, UT + 8, 70, 110, "none", "#cfe6ff", 2.5, 4, 1.4, style="inferred"), figure(400, UT, 92, 1.6, "#cbbca8"), figure(470, UT, 86, 1.8, "#cbbca8"),
            lab(430, 170, "2026", 1.0, BONE, 36), lab(560, UT + 160, "sampled here", 2.0, "#cfe6ff", 26)]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [1600, 150, 22], "ridges": [], "cam": CAM, "els": els}


def s26_add():
    """Their claim, dotted: an 11,000-year ash under the camp's ground; the ground under 8,000 years; Ice Age wood washed in by the creek."""
    ta, tw = T("s26", "after the Ice Age"), T("s26", "Ice Age wood")
    els = [ln([(660, LT + 26), (1260, LT + 26)], ta, LILAC, 4, "claimed", 1.0)] + tag(920, LT + 86, "ash, about 11,000 years", ta + .4, LILAC, 24, "claimed")
    els += tag(920, LT - 110, "under 8,000 years?", ta + .8, LILAC, 26, "claimed")
    for k, x in enumerate((1370, 1440, 1510)):
        t = round(tw + .2 * k, 2)
        els += [poly([(x - 28, 540), (x + 28, 532), (x + 32, 542), (x - 24, 550)], WOOD, "#b08a62", 1.2, t, fx="pop"),
                arrow([[x - 70, 520], [x - 30, 538]], t, BLUE, 2.5, dur=.4, curve=False)]
    els += tag(1445, 640, "Ice Age wood", tw + .5, LILAC, 26, "claimed")
    return els


def s28_add():
    """The excavators' answer: they sampled elsewhere; seaweed chewed on the camp floor dates to about 14,200 years."""
    te, ts = T("s28", "never dug"), T("s28", "seaweed chewed")
    els = [{"k": "dim", "x1": 555, "y1": 620, "x2": 920, "y2": 620, "t": "not at the camp", "c": "#cfe6ff", "dur": .6, "in": round(te + .4, 2)}]
    els += [poly(E(985, LT - 8, 15, 8, 12), "#6fae6a", "#c9f0c0", 1.5, ts, fx="pop", curve=True), tick(1030, LT - 34, ts + .3, GREEN)]
    els += tag(1135, LT - 40, "14,200 years", ts + .5, GREEN, 26)
    return els


def s27():
    """The rule as a picture: a new stone wall with an old timber beam set in it; what was dated is the beam."""
    tw, ts = T("s27", "sample"), T("s27", "site")
    els = []
    for row in range(6):
        for k in range(8):
            x = 420 + 120 * k + (60 if row % 2 else 0)
            if x > 1300:
                continue
            els.append(rect(x, 300 + 64 * row, 112, 56, "#a9a090", "#d8d0c0", 1.5, 6, round(.3 + .02 * (row * 8 + k), 2)))
    els += [rect(380, 420, 1000, 54, "#6b4a30", "#b08a62", 2, 4, .9, fx="pop")]
    els += [ln([(400 + 60 * k, 434), (440 + 60 * k, 462)], .9, "#4e3622", 2, draw=False, op=.7) for k in range(15)]
    els += tag(600, 380, "the sample: old wood", tw, GOLD, 28) + tag(1150, 720, "the site: younger", ts, BLUE, 28)
    els += [arrow([[600, 398], [640, 430]], tw + .2, GOLD, 3, dur=.3, curve=False)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s29_add():
    """The jury is out: the Monte Verde dot gets a question mark; two more dots light up on the older side: Paisley Caves and
    Cooper's Ferry; the crack is still there."""
    tj, tw = T("s29", "jury"), T("s29", "Oregon")
    mv = (XW(14500), 400)
    els = [circ(mv[0], mv[1], 30, "none", LILAC, 3, tj, style="claimed")] + [lab(mv[0], mv[1] - 40, "?", tj + .1, LILAC, 54, st="big", fx="pop")]
    for k, (ya, y, name) in enumerate(((14300, 520, "Paisley Caves"), (16000, 300, "Cooper's Ferry"))):
        x = XW(ya)
        t = round(tw + .5 * k, 2)
        els += [glow(x, y, 70, t, .8, "lamp"), dot(x, y, 15, GOLD, t), lab(x - 26, y + 10, name, t + .1, GOLD, 30, "end")]
    return els


# ================================================================== chapter 3: footprints in the mud
def dune(x, y, w, h, at, lit="#f9f6ee", shade="#d6cfbf", fx="rise"):
    """A gypsum dune seen obliquely: a bright windward slope and a shaded slip face."""
    return [poly([(x - w, y), (x - w * .45, y - h * .7), (x - w * .1, y - h), (x + w * .25, y - h * .9), (x + w * .6, y)], lit, "#e6e0d2", 1, at, fx=fx, curve=True),
            poly([(x - w * .1, y - h), (x + w * .25, y - h * .9), (x + w * .6, y), (x + w * .05, y)], shade, at=at, fx=fx, curve=True)]


def s30():
    """The Tularosa Basin, seen from above its edge: in the Ice Age a great lake fills it (Lake Otero); when it dries, its bed turns to
    a pale flat on the left and white gypsum dunes rise on the right, row after row, bigger towards us."""
    td, tg = T("s30", "When it dried"), T("s30", "gypsum dunes")
    HZ = 330
    els = [poly([(-20, HZ), (-20, 210), (90, 190), (200, 230), (320, 260), (420, 300), (520, HZ)], "#5a5450", "#8a7f72", 2, -1, curve=True),
           poly([(1180, HZ), (1300, 280), (1420, 240), (1540, 200), (1660, 186), (1800, 200), (1800, HZ)], "#5e5650", "#8a7f72", 2, -1, curve=True),
           poly([(400, HZ), (600, 300), (800, 312), (1000, 296), (1200, HZ)], "#6e6a74", at=-1, curve=True, op=.8)]
    lake = [(160, 420), (400, 370), (800, 352), (1200, 360), (1560, 390), (1680, 470), (1560, 600), (1200, 660), (700, 670), (300, 620), (120, 520)]
    els += [poly(lake, "#3f7f9c", "#9fd0ff", 2, .4, curve=True), lab(520, 500, "Lake Otero", .8, "#e6f4ff", 38), lab(520, 544, "Ice Age", .9, BLUE, 28)]
    els += [poly(lake, "#e4dccb", "#cfc6b2", 1.5, td, curve=True, dur=.8)]
    rr = random.Random(30)
    k = 0
    for row in range(6):
        y = 380 + 62 * row + 4 * row * row
        n = 7 - row // 2
        w, h = 36 + 22 * row, 8 + 6 * row
        for q in range(n):
            x = 820 + (900 / n) * q + (w * .6 if row % 2 else 0) + rr.uniform(-15, 15)
            t = round(td + .5 + .035 * k, 2); k += 1
            els += dune(x, y, w, h, t)
    els += [lab(1250, 300, "gypsum dunes, today", tg, "#ffffff", 32), lab(420, 640, "the dried lake bed", tg + .6, "#5a5040", 28, halo=False)]
    return {"base": "sky", "tod": "day", "ground": HZ, "sun": [1450, 140, 22], "ridges": [], "groundc": "#cdbfa2", "cam": CAM, "els": els}


def mini_print(x, y, L, at, c="#e9d9b8", ang=0):
    """A small footprint icon (sole and five toes), toes up."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    P = lambda u, v: (x + (u * ca - v * sa) * L, y + (u * sa + v * ca) * L)
    out = [poly([P(u, v) for u, v in _SOLE], c, at=at, curve=True, fx="pop")]
    out += [circ(*P(u, v), max(1.2, ru * L), c, at=at) for u, v, ru, rv in _TOES]
    return out


def s31():
    """Left: a trench wall of thin mud layers with footprint dips on several surfaces, a researcher at the top. Right: 61 footprint
    icons in rows; a teenager and a child, an adult dimmed behind."""
    tm, tt, ta = T("s31", "sixty-one"), T("s31", "Teenagers"), T("s31", "adult prints")
    els = []
    tones = ["#b39d7c", "#c7b391", "#a58f70", "#bba585", "#9c8768", "#c2ad8b", "#ab9574", "#b8a281"]
    for k in range(8):
        els.append(rect(120, 260 + 58 * k, 640, 58, tones[k], at=-1))
    rr = random.Random(31)
    for k in range(1, 8):
        y = 260 + 58 * k
        for q in range(rr.randint(1, 2)):
            x = rr.uniform(170, 700)
            els.append(ln([(x - 26, y), (x - 18, y + 12), (x + 18, y + 12), (x + 26, y)], round(.5 + .12 * k, 2), "#4a3c2c", 4, dur=.3, curve=True))
    els += [rect(120, 260, 640, 464, "none", "#e3c99c", 2, 0, -1)] + seated(300, 258, 110, .3, "#cbbca8") + [ln([(340, 222), (384, 262)], .3, "#cbbca8", 4, draw=False)]
    els += [lab(440, 750, "layer upon layer", .6, BONE, 28)]
    for k in range(61):
        r_, c_ = divmod(k, 10)
        els += mini_print(900 + 52 * c_, 280 + 64 * r_, 44, round(tm + .03 * k, 2), "#e9d9b8", 90)
    els += [lab(1135, 740, "61 footprints", tm + 1.0, GOLD, 32)]
    els += [figure(1470, 640, 64, tt, "#e8d6b8"), figure(1540, 640, 120, tt + .1, "#e8d6b8"), figure(1620, 640, 156, ta, "#6f665c", op=.55),
            lab(1505, 692, "teenagers and children", tt + .3, BONE, 24), lab(1610, 462, "adults rarer", ta + .2, MUTED, 22)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


PL = [270, 330, 390, 450, 510, 570, 630]                   # the layers of the book and of the mud (s32, s33)


def s32():
    """A book seen edge-on with a pressed flower between two pages; beside it, mud layers with a footprint caught between two of
    them; arrows: date the layer above (younger) and below (older)."""
    tb, td, tt = T("s32", "like flowers"), T("s32", "date the pages"), T("s32", "trapped in")
    els = []
    for k, y in enumerate(PL):
        els.append(rect(200, y, 520, 56, "#efe3c8" if k % 2 else "#e4d6b8", "#a89676", 1.2, 3, round(tb - .2 + .04 * k, 2)))
    els += [rect(180, PL[0] - 12, 560, PL[-1] + 68 - PL[0], "none", "#8a6a48", 6, 10, tb - .2)]
    fx, fy = 460, PL[3] + 2
    els += [poly(E(fx, fy, 70, 7, 18), "#c0503a", "#e98a8a", 1.2, tb + .3, curve=True), ln([(fx + 70, fy), (fx + 150, fy + 2)], tb + .3, "#5f8a4a", 4, draw=False),
            lab(460, 230, "pressed between pages", tb + .4, BONE, 26)]
    tones = ["#b39d7c", "#c7b391", "#a58f70", "#bba585", "#9c8768", "#c2ad8b", "#ab9574"]
    for k, y in enumerate(PL):
        els.append(rect(900, y, 560, 60, tones[k], at=round(tb + 1.0 + .04 * k, 2)))
    els += [ln([(1080, PL[3]), (1100, PL[3] + 18), (1170, PL[3] + 18), (1190, PL[3])], tb + 1.4, "#3b2f22", 6, dur=.4, curve=True),
            lab(1180, 230, "layers of mud", tb + 1.2, BONE, 26), glow(1135, PL[3] + 10, 70, tb + 1.4, .7, "lamp")]
    els += [arrow([[1540, PL[1] + 30], [1470, PL[1] + 30]], td, BLUE, 3, dur=.4, curve=False), lab(1550, PL[1] + 40, "date above", td + .2, BLUE, 24, "start"),
            arrow([[1540, PL[5] + 30], [1470, PL[5] + 30]], td + .6, AMBER, 3, dur=.4, curve=False), lab(1550, PL[5] + 40, "date below", td + .8, AMBER, 24, "start"),
            lab(1550, PL[1] + 72, "younger", td + .4, MUTED, 22, "start"), lab(1550, PL[5] + 72, "older", td + 1.0, MUTED, 22, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def ditchgrass(x, y, h, at, c="#7fae6a", seeds=True):
    """A sprig of ditch grass (Ruppia): thin stems and leaves, small seeds."""
    out = [ln([(x, y), (x + 6, y - h * .5), (x - 4, y - h)], at, c, 3, dur=.5, curve=True), ln([(x + 3, y - h * .4), (x + 36, y - h * .7)], at + .2, c, 2.5, dur=.4, curve=True),
           ln([(x - 2, y - h * .65), (x - 40, y - h * .9)], at + .25, c, 2.5, dur=.4, curve=True)]
    if seeds:
        out += [poly(E(x + 36 + 6 * q, y - h * .7 - 10 * q, 4, 6, 10), "#5a4024", at=round(at + .5 + .05 * q, 2), fx="pop") for q in range(3)]
    return out


def s33_add():
    """The first clock: seeds of ditch grass in the layers above and below the print; 21,000 above, 23,000 below; a gold bracket."""
    ts, tn = T("s33", "seeds"), T("s33", "twenty-three")
    els = ditchgrass(805, 520, 200, ts - .3)
    for k, (y, t) in enumerate(((PL[2] + 30, ts), (PL[4] + 30, ts + .3))):
        els += [poly(E(960 + 110 * q, y, 6, 9, 10), "#5a4024", "#c9a070", 1, round(t + .05 * q, 2), fx="pop") for q in range(4)]
    els += tag(1360, PL[2] + 34, "21,000", tn - .6, GOLD, 26) + tag(1360, PL[4] + 34, "23,000", tn - .3, GOLD, 26)
    els += [ln([(895, PL[2] + 30), (880, PL[2] + 30), (880, PL[4] + 30), (895, PL[4] + 30)], tn, GOLD, 4, dur=.5)]
    els += [lab(889, 760, "about 23,000 to 21,000 years", tn + .3, GOLD, 32), glow(1180, PL[3] + 30, 260, tn, .35, "lamp")]
    return els


def s34():
    """Hard water: a ditch grass plant under the lake; groundwater rises from ancient rock through cracks, carrying grey old carbon
    into the water and the plant; gold air carbon stays above the surface."""
    tw, tg = T("s34", "Water plants"), T("s34", "groundwater")
    WY, BED = 250, 520
    els = [rect(-20, WY, 1840, BED - WY, "#2f5f78", at=-1, op=.95), rect(-20, WY, 1840, 6, "#bfe3f5", at=-1, op=.5),
           rect(-20, BED, 1840, 100, "#6f5a44", at=-1), rect(-20, BED + 100, 1840, 400, "#8a8a86", at=-1)]
    for k in range(5):
        els.append(ln([(-20, BED + 160 + 50 * k), (1820, BED + 160 + 50 * k)], -1, "#6d6d69", 2, draw=False, op=.7))
    els += ditchgrass(820, BED, 230, .3, "#8fbf6a", seeds=False) + ditchgrass(900, BED, 180, .4, "#7fae6a", seeds=False)
    rr = random.Random(34)
    els += [dot(rr.uniform(200, 1600), rr.uniform(140, 220), 7, GOLD, round(.5 + .04 * q, 2)) for q in range(16)]
    els += [lab(1660, 180, "air", .8, GOLD, 28)]
    for k, x in enumerate((480, 1180, 1420)):
        t = round(tg + .25 * k, 2)
        els += [ln([(x, BED + 400), (x + 20, BED + 250), (x - 10, BED + 110), (x, BED)], t, "#2a2a28", 3, draw=False)]
        els += [arrow([[x + 6, BED + 330], [x + 10, BED + 160], [x, BED - 20], [820 if x < 820 else 900, BED - 80]], t, BLUE, 3.5, dur=1.0, curve=True)]
        els += [dot(x + 14 * math.sin(q), BED + 300 - 70 * q, 8, "#b8b8b4", round(t + .3 + .15 * q, 2)) for q in range(5)]
    els += [lab(830, 700, "ancient rock", tg + .4, "#dcdcd6", 28), lab(1470, 640, "old carbon", tg + .9, "#dcdcd6", 28, "start"), lab(640, 300, "ditch grass", tw + .2, "#bfe8b0", 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """Two candles lit at the same moment: a fresh one, and one already half burnt (its missing half dashed): it looks older."""
    th = T("s35", "half burnt")
    base = 650
    els = candle(620, base, 360, .3) + candle(1160, base, 180, th, burnt=1.0)
    els += [lab(620, 720, "a fresh candle", .6, BONE, 28), lab(1160, 720, "half burnt already", th + .3, BONE, 28)] + tag(1400, 420, "looks older", th + .9, RED, 28)
    els += [rect(560, 200, 660, 40, "none", "none", 0, 0, 0)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": [glow(889, 420, 500, -1, .15, "lamp")] + els}


def s36():
    """A herbarium sheet with a pressed sprig of ditch grass collected in 1947 at a nearby spring; its radiocarbon age prints: about
    7,400 years."""
    tc, tr = T("s36", "nineteen forty-seven"), T("s36", "seven thousand")
    els = [rect(520, 150, 560, 620, "#efe6d0", "#c9b9a0", 2, 6, .2, fx="pop")]
    els += ditchgrass(760, 640, 380, .5, "#6f8f58", seeds=True)
    els += [rect(870, 650, 180, 90, "#fffaf0", "#8a7a62", 1.5, 4, tc - .2), lab(960, 690, "1947", tc, "#3a2c20", 28, halo=False),
            lab(960, 724, "nearby spring", tc + .1, "#5a4a38", 20, halo=False)]
    els += [arrow([[1110, 420], [1240, 420]], tr - .4, RED, 3, dur=.4, curve=False)] + tag(1440, 420, "about 7,400 years", tr, RED, 32)
    els += [lab(1440, 360, "radiocarbon age", tr - .2, MUTED, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s37():
    """Conifers on the slopes above the lake (2023): air carbon flows into their needles; pollen drifts down and settles in the lake mud."""
    tp, ta = T("s37", "Pollen"), T("s37", "breathing the air")
    GY = 600
    slope = [(700, GY), (900, 470), (1100, 360), (1300, 280), (1500, 230), (1800, 200), (1800, GY)]
    els = [poly(slope, "#3f3b30", "#7a705c", 2, -1), rect(-20, GY - 20, 760, 40, "#3f7f9c", at=-1), rect(-20, GY - 20, 760, 6, "#bfe3f5", at=-1, op=.5)]
    rr = random.Random(37)
    trees = []
    for k in range(13):
        x = 880 + 70 * k + rr.uniform(-15, 15)
        y = max(230, GY - (x - 700) * .55) + 10
        trees.append((x, y))
        els.append(conifer(x, y, rr.uniform(90, 130), round(.2 + .04 * k, 2), ["#2f4a2c", "#365233", "#2a4128"][k % 3], "pop"))
    els += [lab(1450, 470, "pine, spruce, fir", .8, "#bfe8b0", 30), lab(380, 200, "2023", .5, BONE, 36)]
    for q in range(10):
        x, y = trees[q + 2]
        els.append(arrow([[x + 30, y - 220], [x + 4, y - 120]], round(ta - .3 + .05 * q, 2), GOLD, 2.5, dur=.5, curve=False))
    els += [lab(960, 150, "air", ta + .4, GOLD, 28)]
    for q in range(18):
        x0, y0 = trees[q % 10]
        t = round(tp + .04 * q, 2)
        path = [(x0, y0 - 60), (x0 - 200 - 30 * (q % 5), y0 - 10), (520 - 22 * q, GY - 30), (500 - 24 * q, GY + 4)]
        els += [ln(path, t, "#f2d36a", 2, "claimed", 1.0, curve=True, op=.7), dot(path[-1][0], path[-1][1], 6, "#f2d36a", round(t + .9, 2))]
    els += [lab(330, GY + 70, "pollen settles in the mud", tp + 1.2, "#f2d36a", 26)]
    return {"base": "sky", "tod": "day", "ground": GY + 20, "sun": [1600, 140, 0], "ridges": [], "groundc": "#8c7a5c", "cam": CAM, "els": els}


def pine_pollen(x, y, s, at):
    """A pine pollen grain: a body with two air sacs."""
    return [circ(x - 34 * s, y, 30 * s, "#f2d36a", "#fff3c0", 1.5, at, fx="pop", op=.8), circ(x + 34 * s, y, 30 * s, "#f2d36a", "#fff3c0", 1.5, at, fx="pop", op=.8),
            poly(E(x, y, 34 * s, 26 * s, 20), "#d9a944", "#fff3c0", 1.5, at, fx="pop", curve=True)]


def s38():
    """Under a microscope circle, pine pollen grains with their two air sacs; beside it a block of 750 gold dots fills row by row
    (each dot is 100 grains): about 75,000 grains per date."""
    t75 = T("s38", "seventy-five")
    els = [circ(420, 450, 250, "#1a2a20", "#cfe6ff", 6, .2, fx="pop"), glow(420, 450, 260, .3, .35, "blue")]
    els += pine_pollen(360, 380, 1.2, .5) + pine_pollen(490, 500, 1.0, .7) + pine_pollen(330, 560, .8, .9)
    els += [lab(420, 760, "pine pollen, magnified", .8, MUTED, 24)]
    for r_ in range(25):
        y = 200 + 20 * r_
        els.append(ln([(820, y), (820 + 20 * 29, y)], round(t75 + .07 * r_, 2), GOLD, 11, draw=False, dash="0 20"))
    els += [lab(1110, 150, "about 75,000 grains per date", t75 + 1.9, GOLD, 32), lab(1110, 740, "each dot: 100 grains", t75 + .4, MUTED, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def battery(x, y, w, h, frac, at, fill_at=None, dur=2.4, c=GREEN):
    """A battery gauge: a case, a cap, a charge bar (frac of the length), filling from the left (fx draw on a thick line)."""
    out = [rect(x, y, w, h, "rgba(18,13,10,.6)", BONE, 3, 8, at, fx="pop"), rect(x + w, y + h * .3, 12, h * .4, BONE, at=at, r=3)]
    if frac > 0:
        out.append(ln([(x + 10, y + h / 2), (x + 10 + (w - 20) * frac, y + h / 2)], fill_at if fill_at is not None else at, c, h - 18, dur=dur))
    return out


def quartz(x, y, s, at, c="#e6eef5"):
    pts = [(-14, -26), (14, -26), (26, 0), (14, 26), (-14, 26), (-26, 0)]
    return [poly([(x + a * s, y + b * s) for a, b in pts], c, "#ffffff", 1.5, at, fx="pop"), ln([(x - 14 * s, y - 26 * s), (x + 4 * s, y + 6 * s)], at, "#b9c8d6", 1.5, draw=False)]


def s39():
    """The quartz clock: in sunshine a grain's battery drains to empty; buried under layers of mud in the dark, it slowly recharges;
    the charge tells the time."""
    ts, tb, tc = T("s39", "Sunlight"), T("s39", "once buried"), T("s39", "the charge")
    els = [glow(330, 230, 160, .3, .8, "sun"), circ(330, 230, 40, "#ffe7b0", at=.3)]
    els += [ln([(330 + 70 * math.cos(a), 230 + 70 * math.sin(a)), (330 + 100 * math.cos(a), 230 + 100 * math.sin(a))], .4, "#ffe7b0", 3, draw=False) for a in [k * math.pi / 4 for k in range(8)]]
    els += [rect(80, 560, 600, 20, "#b39d7c", at=-1)] + quartz(380, 520, 1.4, .5) + battery(250, 640, 260, 60, 0, ts) + [lab(380, 740, "sunlight: empty", ts + .3, "#ffe7b0", 26)]
    els += [arrow([[720, 520], [880, 520]], tb - .3, BONE, 3, dur=.4, curve=False)]
    tones = ["#b39d7c", "#a58f70", "#9c8768", "#8f7a5c", "#7f6b50"]
    els += [rect(940, 560, 700, 20, "#b39d7c", at=-1)] + quartz(1290, 520, 1.4, tb - .2)
    for k in range(5):
        els.append(rect(940, 540 - 60 * (k + 1), 700, 60, tones[k], at=round(tb + .2 * k, 2), fx="rise"))
    els += [rect(940, 180, 700, 420, "rgba(10,8,6,.35)", at=tb + 1.0)]
    els += battery(1160, 640, 260, 60, .7, tb + .3, tb + 1.2, dur=3.0) + [lab(1290, 740, "buried: recharging", tb + .6, GREEN, 26)]
    els += [lab(1290, 160, "the charge tells the time", tc, GOLD, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def XD(ya):                                     # the dating chart: 25,000 years ago at x 200, 19,000 at x 1580
    return round(200 + (25000 - ya) / 6000 * 1380, 1)


ROWS40 = {"seeds": 260, "pollen": 360, "quartz": 460, "mud": 560}


def s40():
    """Four clocks on one axis: seeds (23,000 to 21,000), pollen (about 23,400 to 22,600), quartz (at least 21,500) and, in 2025,
    the lake mud (22,400 to 20,700)."""
    tb, tm = T("s40", "Both agreed"), T("s40", "lake mud")
    AY = 660
    els = [axis(200, 1580, AY, [(XD(v), "{:,}".format(v)) for v in (25000, 24000, 23000, 22000, 21000, 20000, 19000)], .2, "years ago")]
    els += [band(XD(23000), XD(21000), ROWS40["seeds"] - 14, 28, GOLD, .4), lab(150, ROWS40["seeds"] + 10, "seeds", .4, GOLD, 30, "start")]
    els += [band(XD(23400), XD(22600), ROWS40["pollen"] - 14, 28, GREEN, tb), lab(150, ROWS40["pollen"] + 10, "pollen", tb, GREEN, 30, "start")]
    els += [arrow([[XD(21500), ROWS40["quartz"]], [XD(23600), ROWS40["quartz"]]], tb + .4, BLUE, 6, dur=.6, curve=False),
            ln([(XD(21500), ROWS40["quartz"] - 18), (XD(21500), ROWS40["quartz"] + 18)], tb + .4, BLUE, 5, draw=False),
            lab(150, ROWS40["quartz"] + 10, "quartz", tb + .4, BLUE, 30, "start"), lab(XD(21500) + 16, ROWS40["quartz"] + 10, "at least 21,500", tb + .6, BLUE, 24, "start")]
    els += [band(XD(22400), XD(20700), ROWS40["mud"] - 14, 28, "#c9a070", tm), lab(150, ROWS40["mud"] + 10, "mud", tm, "#e3c99c", 30, "start")] + \
           tag(XD(20700) + 90, ROWS40["mud"] + 2, "2025", tm + .2, "#e3c99c", 24)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s41_add():
    """Doubts, dotted: pollen washed in? quartz not reset? Then a soft gold column over the overlap: one story."""
    td, to = T("s41", "pollen can wash"), T("s41", "one story")
    els = tag(1330, ROWS40["pollen"] + 4, "washed in?", td + .3, LILAC, 26, "claimed") + tag(1330, ROWS40["quartz"] + 4, "not reset?", td + 1.4, LILAC, 26, "claimed")
    els += [rect(XD(23000), 200, XD(21000) - XD(23000), 430, "rgba(242,201,142,.16)", GOLD, 2, 12, to - .6, style="inferred"),
            lab((XD(23000) + XD(21000)) / 2, 180, "one story", to, GOLD, 34)]
    return els


def s42():
    """Chiquihuite Cave, high on a limestone mountain in Mexico; cut away, the cave floor in layers with many small stone pieces
    (dotted: claimed as tools); stones fall from the cave's own roof."""
    tc, tl, tk = T("s42", "Chiquihuite"), T("s42", "thirty thousand"), T("s42", "Critics")
    mtn = [(-20, 800), (60, 690), (140, 610), (200, 560), (250, 500), (300, 470), (350, 400), (400, 360), (440, 300), (480, 250), (520, 280), (560, 236),
           (610, 290), (660, 330), (720, 400), (790, 470), (860, 560), (930, 650), (1000, 800)]
    els = [poly([(-20, 800), (-20, 520), (120, 470), (220, 520), (300, 800)], "#4c4844", at=-1), poly(mtn, "#8f8a80", "#c9c3b8", 2, -1)]
    els += [ln([(x, 800), (x + 120, 520 - (x % 120))], -1, "#a7a196", 2, draw=False, op=.5) for x in range(60, 900, 70)]
    els += [poly([(480, 250), (520, 280), (560, 236), (600, 280), (520, 310)], "#b2ada3", at=-1)]
    els += [poly(E(520, 350, 26, 18, 14), "#1a1715", "#5a524a", 2, .3, curve=True), ln([(548, 350), (1020, 300)], .6, "#e3c99c", 2, "inferred", .5)]
    els += [lab(150, 200, "Chiquihuite Cave, Mexico", .5, BONE, 30, "start")]
    cx, cy, Rr = 1300, 450, 300
    inner = [rect(cx - Rr, cy - Rr, 2 * Rr, 2 * Rr, "#2a2622"),
             poly([(cx - 310, cy - 80), (cx - 150, cy - 170), (cx, cy - 190), (cx + 150, cy - 170), (cx + 310, cy - 80), (cx + 310, cy - 310), (cx - 310, cy - 310)], "#77726a"),
             rect(cx - Rr, cy + 40, 2 * Rr, 70, "#8a7a62"), rect(cx - Rr, cy + 110, 2 * Rr, 80, "#6d604e"), rect(cx - Rr, cy + 190, 2 * Rr, 120, "#5a4e40")]
    els += [{"k": "group", "clip": [cx - Rr, cy - Rr, 2 * Rr, 2 * Rr, Rr], "els": inner, "in": .6, "fx": "pop"}, circ(cx, cy, Rr, "none", "#e3c99c", 3, .6)]
    rr = random.Random(42)
    for q in range(44):
        x, y = cx + rr.uniform(-250, 250), cy + rr.uniform(60, 250)
        if math.hypot(x - cx, y - cy) > Rr - 22:
            continue
        els.append(poly([(x - 8, y), (x, y - 7), (x + 9, y - 2), (x + 4, y + 6)], "#2f6e5e" if q % 2 else "#1f2a2a", "#b9d8cc", 1, round(tc + .6 + .03 * q, 2), fx="pop", style="claimed"))
    els += tag(cx, cy + 300, "nearly 2,000 stones", tc + 1.4, LILAC, 26, "claimed") + tag(cx, cy - Rr - 4, "about 30,000 years?", tl, LILAC, 26, "claimed")
    for k, x in enumerate((cx - 120, cx + 30, cx + 170)):
        t = round(tk + .25 * k, 2)
        els += [arrow([[x, cy - 170], [x + 10, cy - 40], [x + 6, cy + 30]], t, RED, 3, "claimed", .6, True),
                poly([(x - 10, cy + 40), (x, cy + 30), (x + 12, cy + 36), (x + 4, cy + 48)], "#9a948a", at=t + .5, fx="pop")]
    els += [lab(cx + 10, cy - 196, "the cave's own rock?", tk + .5, RED, 26)]
    return {"base": "sky", "tod": "dusk", "ground": 820, "sun": [900, 640, 0], "ridges": [], "cam": CAM, "els": els}


def XL(ya):                                     # the long axis: 140,000 years ago at x 200, 0 at x 1580
    return round(200 + (140000 - ya) / 140000 * 1380, 1)


def broken_bone(x0, y0, x1, y1, at, w=28, c="#e8dcc6", knob=True):
    """A piece of a long bone with a spiral (jagged) break at its far end."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    pts = [(x0 + nx * w / 2, y0 + ny * w / 2), (x1 + nx * w / 2 - ux * 10, y1 + ny * w / 2 - uy * 10), (x1 + ux * 6, y1 + uy * 6 + 4), (x1 - ux * 14 + nx * 2, y1 - uy * 14 + ny * 2),
           (x1 + ux * 2 - nx * w / 2, y1 + uy * 2 - ny * w / 2), (x0 - nx * w / 2, y0 - ny * w / 2)]
    out = [poly(pts, c, "#fff6e6", 1.5, at, fx="pop")]
    if knob:
        out.append(poly(E(x0 - ux * 10, y0 - uy * 10, w * .9, w * .75, 16), c, "#fff6e6", 1.5, at, fx="pop", curve=True))
    return out


def s43():
    """Broken mastodon bones and battered cobbles near San Diego (the objects solid; the hammer blows claimed, dotted), 130,000
    years?; below, a long axis where the claim sits far to the left of White Sands; most specialists unconvinced."""
    tb, tn, tm = T("s43", "broken mastodon"), T("s43", "a hundred and thirty"), T("s43", "Most specialists")
    els = broken_bone(470, 330, 690, 300, tb) + broken_bone(860, 300, 720, 330, tb + .2) + broken_bone(520, 420, 700, 440, tb + .4, knob=False)
    for k, (x, y, r_) in enumerate(((1000, 380, 46), (1120, 330, 36), (1090, 440, 32))):
        t = round(tb + .8 + .15 * k, 2)
        els += [poly(E(x, y, r_, r_ * .8, 18), "#8f8a80", "#cfc9bd", 2, t, fx="pop", curve=True), ln([(x - r_ * .3, y - r_ * .2), (x + r_ * .1, y + r_ * .1)], t, "#5d5850", 2, draw=False)]
    els += [arrow([[960, 360], [880, 320], [780, 318]], tb + 1.4, LILAC, 3, "claimed", .6), arrow([[1060, 450], [900, 470], [720, 440]], tb + 1.6, LILAC, 3, "claimed", .6)]
    els += [lab(360, 230, "near San Diego", tb, BONE, 30)] + tag(1360, 300, "130,000 years?", tn, LILAC, 30, "claimed")
    AY = 590
    els += [axis(200, 1580, AY, [(XL(v), "{:,}".format(v)) for v in (140000, 100000, 50000, 0)], tn + .3, "years ago"),
            dot(XL(130000), AY - 22, 12, LILAC, tn + .6), lab(XL(130000) + 10, AY - 44, "the claim", tn + .7, LILAC, 24, "start"),
            band(XL(23000), XL(21000), AY - 34, 22, GOLD, tn + 1.0), lab(XL(22000), AY - 50, "White Sands", tn + 1.1, GOLD, 24)]
    for k in range(8):
        x = 1240 + 52 * k
        els += [figure(x, 795, 66, round(tm + .05 * k, 2), "#9a8f80")]
        if k != 3:
            els.append(lab(x, 714, "?", round(tm + .3 + .05 * k, 2), LILAC, 30, st="big", fx="pop"))
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}



# ================================================================== chapter 4: which road?
GLOBE44 = (-110, 46, 600, 880, 520)


def s44():
    """North America at the height of the Ice Age on a big globe: the two ice sheets spread white over Canada and meet; Beringia
    joins Alaska to Asia; a gold pin at White Sands with walkers south of the ice; a question mark between."""
    tq = T("s44", "which way")
    g = Globe(*GLOBE44)
    lon0, lat0, Rr, cx, cy = GLOBE44
    ws = g.p(*SITE["whitesands"])
    P = lambda pts: [g.p(lo, la) for lo, la in pts]
    els = [circ(cx, cy, Rr, "#163447", at=-1), land_el(g.land(), -1, "#5b4a36"), circ(cx, cy, Rr + 5, "none", "#9fd0ff", 6, -1, op=.3),
           poly(P(BRIDGE_W), "#6e5c45", "#e3c99c", 2, -1, curve=True, style="inferred"),
           poly(P(CORD_LGM), "rgba(236,244,252,.95)", ICE_E, 2, .3, curve=True), poly(P(LAURENTIDE), "rgba(236,244,252,.95)", ICE_E, 2, .3, curve=True),
           glow(*g.p(-95, 60), 420, .3, .25, "blue")]
    els += [lab(*g.p(-92, 63), "ice sheets", .8, "#2a3440", 34, halo=False), lab(*g.p(-168, 64.5), "Beringia", 1.0, "#fff1d0", 34, st="ital")]
    els += [pin(ws[0], ws[1], "White Sands", T("s44", "walkers"), GOLD, "start", 20, 8, tc=GOLD)]
    els += [figure(ws[0] - 30 + 22 * k, ws[1] + 62, 40, round(T("s44", "walkers") + .2 + .1 * k, 2), GOLD) for k in range(3)]
    els += qmark(*g.p(-135, 47), tq, 120)
    return {"base": "dark", "stars": 120, "cam": CAM, "els": els}


# Beringia in plain longitudes (-180..-150 for the Alaskan side, west of 180 as -185..-180), for the globe
BRIDGE_W = [(-185, 69.5), (-182, 71.6), (-174, 73.2), (-164, 72.8), (-156, 71.4), (-154, 66), (-156, 60), (-162, 55.2), (-165.5, 54.3), (-170, 56.2),
            (-173.5, 59.2), (-178, 61.2), (-181.5, 62.6), (-185, 64.5), (-187, 67)]


def s45_add():
    """Close on the seam between the ice sheets: the corridor's line draws itself (dashed amber), then a white weld closes it;
    a boulder at the old ice edge glows: open again about 13,800 years ago."""
    ti, tm, tr = T("s45", "a gap"), T("s45", "the sheets met"), T("s45", "dating of the rocks")
    g = Globe(*GLOBE44)
    path = [g.p(lo, la) for lo, la in [(-128, 63), (-124, 59), (-120, 56), (-117, 53), (-114, 50.5)]]
    els = [ln(path, ti, AMBER, 7, "inferred", 1.0, curve=True), ln([(724, 366), (path[1][0] - 10, path[1][1])], ti + .4, AMBER, 2, "inferred", .3),
           lab(716, 374, "the ice-free corridor", ti + .5, AMBER, 26, "end")]
    els += [ln(path, tm, "#ffffff", 16, dur=.8, curve=True, op=.95), lab(path[2][0] + 34, path[2][1] + 8, "closed", tm + .5, "#ffffff", 26, "start")]
    bx, by = g.p(-112, 52)
    els += [poly([(bx - 22, by + 10), (bx - 14, by - 12), (bx + 10, by - 16), (bx + 24, by + 2), (bx + 12, by + 14)], "#9a948a", "#e9e1d2", 1.5, tr, fx="pop"),
            glow(bx, by, 50, tr, .8, "lamp")] + tag(bx + 160, by + 60, "open again: 13,800", tr + .4, GOLD, 22)
    return els


def bison(x, y, s, at, c="#5a4636", face=1):
    """A bison in profile: high hump, low head, short legs; feet on y."""
    P = lambda a, b: (x + face * a * s, y + b * s)
    body = [P(-60, -40), P(-50, -62), P(-20, -66), P(10, -80), P(34, -76), P(50, -60), P(62, -40), P(64, -24), P(56, -14), P(48, -24), P(40, -18), P(36, 0),
            P(26, 0), P(22, -16), P(-30, -16), P(-34, 0), P(-44, 0), P(-48, -20), P(-60, -26)]
    return [poly(body, c, "#a08060", 1.2, at, fx="pop", curve=True)]


def XR(ya):                                     # the corridor's axis: 18,000 years ago at x 200, 12,000 at x 1580
    return round(200 + (18000 - ya) / 6000 * 1380, 1)


def s46():
    """The corridor's timetable: opens about 13,800, grass and game about 12,600; Cooper's Ferry about 16,000 on the older side; too late."""
    tg, tc = T("s46", "grass and game"), T("s46", "Too late")
    AY = 600
    els = [axis(200, 1580, AY, [(XR(v), "{:,}".format(v)) for v in (18000, 17000, 16000, 15000, 14000, 13000, 12000)], .2, "years ago")]
    els += [ln([(XR(13800), AY - 260), (XR(13800), AY)], .5, BLUE, 4, dur=.5), lab(XR(13800), AY - 280, "corridor opens", .7, BLUE, 28)]
    els += [ln([(XR(12600), AY - 160), (XR(12600), AY)], tg, GREEN, 4, dur=.5), lab(XR(12600), AY - 180, "grass and game", tg + .2, GREEN, 28)] + bison(XR(12600) + 4, AY - 40, .9, tg + .4)
    els += [glow(XR(16000), AY - 60, 70, tc - 1.0, .8, "lamp"), dot(XR(16000), AY - 60, 14, GOLD, tc - 1.0), lab(XR(16000), AY - 100, "Cooper's Ferry", tc - .9, GOLD, 30)]
    els += bracket(XR(16000), XR(13800), AY + 110, tc, None, RED, up=True) + [lab((XR(16000) + XR(13800)) / 2, AY + 160, "too late", tc + .3, RED, 32)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def seal(x, y, s, at, c="#7d7a74", face=1):
    P = lambda a, b: (x + face * a * s, y + b * s)
    return [poly([P(-60, 0), P(-40, -14), P(0, -18), P(30, -16), P(48, -24), P(60, -20), P(58, -8), P(40, -2), P(10, 4), P(-30, 6), P(-60, 10), P(-74, 4)], c, "#cfc9bd", 1.2, at, fx="pop", curve=True),
            dot(*P(52, -18), 2.2, "#1a1715", at)]


def s47():
    """The coast of southeast Alaska and British Columbia: the ice front (dashed) pulls back from a string of islands, ice-free by about
    17,000 years ago; a cave on one island and a seal: seal bones of that age; a dotted coastal route south."""
    ti, ts = T("s47", "islands off Alaska"), T("s47", "seal bones")
    m = Map(-145, -120, 48.5, 61, (90, 130, 1600, 650))
    ice = m.path([(-150, 61.2), (-144, 60.6), (-139.5, 59.9), (-136.4, 59.1), (-134.4, 58.2), (-132.9, 57.1), (-131.6, 56.1), (-130.4, 55.0), (-129.4, 53.9),
                  (-128.3, 52.9), (-127.4, 51.9), (-126.2, 50.9), (-124.9, 49.9), (-123.4, 49.3), (-121.5, 48.4), (-115, 48), (-100, 48), (-100, 72), (-150, 72)])
    els = [land_el(m.land(), -1), poly(ice, "rgba(236,244,252,.8)", ICE_E, 2.5, .3, curve=True, style="inferred"), lab(*m.p(-126.5, 57.5), "ice", .6, "#2a3440", 30, halo=False)]
    arch = m.p(-134.2, 56.0)
    els += [poly(E(arch[0], arch[1], 150, 130, 30), "rgba(143,217,176,.10)", GREEN, 3, ti, style="inferred", curve=True),
            lab(arch[0] - 200, arch[1] - 60, "ice-free by about 17,000", ti + .5, GREEN, 28, "end")]
    cv = m.p(-133.6, 56.15)
    els += [pin(cv[0], cv[1], "", ts, GOLD), lab(cv[0] - 157, cv[1] + 88, "seal bones, about 17,000", ts + .3, GOLD, 26, "end")] + seal(cv[0] - 165, cv[1] + 30, 1.1, ts + .2)
    route = m.path([(-146, 59.6), (-140, 58.4), (-137, 57.2), (-135.8, 55.4), (-133.6, 53.6), (-131.5, 51.6), (-128.6, 49.6), (-125.6, 48.0)])
    els += [arrow(route, ti + 1.2, BLUE, 4, "claimed", 2.0), lab(*m.p(-139.2, 52.4), "the coast", ti + 2.0, BLUE, 28)]
    return {"base": "map", "cam": CAM, "els": els}


def kelp(x, y0, y1, at, sway=1.0, c="#8a7a32"):
    """A kelp stalk from the sea floor (y0) to near the surface (y1), with blades."""
    n = 7
    pts = [(x + 26 * sway * math.sin(q * .9), y0 - (y0 - y1) * q / n) for q in range(n + 1)]
    out = [ln(pts, at, c, 5, dur=1.0, curve=True)]
    for q in range(1, n + 1):
        px, py = pts[q]
        side = 1 if q % 2 else -1
        out.append(poly([(px, py), (px + side * 40, py - 18), (px + side * 70, py - 8), (px + side * 34, py + 4)], "#9c8a3a", "#c9b860", 1, round(at + .1 * q, 2), fx="pop", curve=True, op=.9))
    return out


def fish(x, y, s, at, c="#cfe6ff", face=1):
    return [poly(E(x, y, 26 * s, 10 * s, 14), c, at=at, fx="pop", curve=True), poly([(x - face * 24 * s, y), (x - face * 42 * s, y - 10 * s), (x - face * 42 * s, y + 10 * s)], c, at=at, fx="pop")]


def boat(x, y, w, at, c="#8a6a44"):
    out = [poly([(x - w / 2, y - 12), (x + w / 2, y - 12), (x + w / 2 - 20, y + 10), (x - w / 2 + 24, y + 10)], c, "#e7c99a", 1.5, at, fx="pop")]
    for k, dx in enumerate((-w * .2, w * .15)):
        out += [figure(x + dx, y - 12, 44, at + .1, "#1d1915", fx="pop"), ln([(x + dx + 6, y - 40), (x + dx + 30, y + 14)], at + .1, "#c9a070", 3, draw=False)]
    return out


def s48():
    """A kelp forest under the North Pacific: tall stalks sway up from rocks; fish, shellfish, a seal and seabirds in turn; a small
    skin boat with two paddlers glides above it: a kelp highway."""
    tk, tf, tsh, tse, tb, th = (T("s48", p) for p in ("forests of", "fish", "shellfish", "seals", "seabirds", "kelp highway"))
    SL = 260
    els = [rect(-20, SL, 1840, 760, "#173f4c", at=-1), rect(-20, SL, 1840, 140, "#21596a", at=-1, op=.8), rect(-20, SL - 3, 1840, 6, "#cfe6ff", at=-1, op=.5),
           poly([(-20, 1010), (-20, 760), (200, 730), (420, 770), (640, 740), (900, 780), (1160, 744), (1400, 776), (1640, 748), (1800, 770), (1800, 1010)], "#2b2a26", at=-1, curve=True)]
    els += [ln([(x, SL + 40), (x - 60, 760)], -1, "#9fd0ff", 30, draw=False, op=.04) for x in range(100, 1800, 160)]
    for k, x in enumerate((180, 330, 520, 700, 960, 1150, 1330, 1560)):
        els += kelp(x, 760 + 10 * (k % 2), SL + 30, round(tk + .1 * k, 2), sway=1 if k % 2 else -1)
    els += fish(600, 470, 1.0, tf, face=1) + fish(660, 520, .8, tf + .1, face=1) + fish(1240, 430, 1.1, tf + .2, face=-1) + fish(1290, 480, .9, tf + .25, face=-1)
    els += [poly(E(420 + 30 * q, 748 - (q % 2) * 6, 14, 8, 12), "#3a3348", "#8a7aa8", 1.2, round(tsh + .05 * q, 2), fx="pop", curve=True) for q in range(5)]
    els += [poly(E(1100 + 26 * q, 740, 16, 9, 12), "#a06a48", "#e2b08a", 1.2, round(tsh + .2 + .05 * q, 2), fx="pop", curve=True) for q in range(3)]
    els += seal(860, 600, 1.6, tse, "#6d6a64")
    for k, (x, y) in enumerate(((1350, 150), (1420, 120), (1490, 160))):
        els.append(ln([(x - 22, y - 6), (x, y + 4), (x + 22, y - 6)], round(tb + .1 * k, 2), "#f5ecdc", 3, dur=.3, curve=True))
    els += boat(980, SL - 2, 200, th - .6)
    els += [lab(300, 400, "kelp forest", tk + .4, "#e2d58a", 30), lab(889, 170, "a kelp highway", th, BONE, 36)]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [400, 130, 18], "ridges": [], "cam": CAM, "els": els}


def s49():
    """The North Pacific from Japan to Idaho in one piece: a dotted arc of coasts from Japan round by Alaska to the Columbia and Idaho;
    a stemmed point at each end: Japan, Cooper's Ferry; they look alike."""
    tp = T("s49", "stone points")
    m = Map(122, 252, 24, 66, (90, 150, 1600, 560))
    route = m.path([(141.8, 41.5), (145, 44.5), (152, 47.5), (158, 52.5), (165, 55.8), (175, 52.8), (185, 52.2), (195, 54.6), (205, 58.6), (215, 60.2),
                    (222, 58.2), (226, 54.6), (229, 51), (234, 48), (236.6, 46.3), (240, 45.9), (243.6, 45.7)])
    jp, cf = m.p(142.5, 43.2), m.p(243.57, 45.73)
    els = [land_el(m.land(), -1), arrow(route, .4, BLUE, 4, "inferred", 2.4), pin(jp[0], jp[1], "", .3, GOLD), pin(cf[0], cf[1], "", .3, GOLD)]
    els += stone_point(310, 760, 170, tp, "#d8cfbf", stemmed=True) + [lab(310, 790, "Japan", tp + .2, BONE, 28)]
    els += stone_point(1470, 760, 170, tp + .5, "#d8cfbf", stemmed=True) + [lab(1470, 790, "Cooper's Ferry", tp + .7, BONE, 28)]
    els += [ln([jp, (310, 560)], tp, "#e3c99c", 2, "inferred", .4), ln([cf, (1470, 560)], tp + .5, "#e3c99c", 2, "inferred", .4),
            lab(889, 700, "they look alike", tp + 1.2, GOLD, 32)]
    return {"base": "map", "cam": CAM, "els": els}


def diver(x, y, s, at, c="#1d2a30"):
    P = lambda a, b: (x + a * s, y + b * s)
    return [poly([P(-60, -8), P(20, -14), P(40, -6), P(40, 6), P(20, 10), P(-60, 8)], c, "#6a8a96", 1.2, at, fx="pop"),
            circ(*P(52, 0), 12 * s, c, "#6a8a96", 1.2, at), rect(*P(-30, -24), 50 * s, 12 * s, "#c9a070", r=4, at=at),
            poly([P(-60, -6), P(-92, -18), P(-96, -8), P(-64, 4)], c, at=at), poly([P(-60, 6), P(-92, 16), P(-96, 6), P(-64, -2)], c, at=at),
            glow(*P(80, 10), 90, at, .9, "lamp")]


def s50():
    """The drowned coast in section: today's sea level, and 120 m below it on the drowned slope the Ice Age shore with a small camp;
    the sea fills down over it; a diver with a lamp swims down towards it."""
    tc, tw, td = T("s50", "the sea stood"), T("s50", "underwater"), T("s50", "divers")
    SL, OS = 280, 580                                                  # sea level today, the Ice Age shore (120 m lower, 2.5 units a metre)
    slope = [(-20, 230), (240, 240), (520, 300), (800, 420), (1050, OS), (1200, OS + 30), (1500, 700), (1800, 760), (1800, 1010), (-20, 1010)]
    els = [poly(slope, "#5a4a38", "#e3c99c", 2, -1, curve=True)]
    els += [rect(-20, SL, 1840, 740, "#2f6f8c", at=tw, op=.55, fx="fill", dur=1.4), ln([(560, SL), (1800, SL)], tw, "#cfe6ff", 3, dur=.8),
            lab(1500, SL - 20, "the sea today", tw + .3, "#cfe6ff", 28)]
    cx = 1080
    els += [poly([(cx - 46, OS + 6), (cx, OS - 54), (cx + 46, OS + 6)], "#8a6a44", "#e7c99a", 1.5, .3, fx="pop"), circ(cx + 80, OS + 2, 10, "#5a4636", at=.4),
            ln([(cx + 70, OS + 4), (cx + 90, OS + 4)], .4, "#3a2c20", 4, draw=False), lab(cx - 20, OS + 90, "Ice Age shore", .6, GOLD, 28)]
    els += [ln([(1050, OS), (1350, OS)], tc, GOLD, 2, "inferred", .5),
            {"k": "dim", "x1": 1330, "y1": SL, "x2": 1330, "y2": OS, "t": "120 m", "c": GOLD, "dur": .8, "in": round(tc + .3, 2), "lx": 52}]
    els += diver(760, 470, 1.0, td)
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [300, 140, 20], "ridges": [], "cam": CAM, "els": els}


def s51():
    """Two roads to White Sands on the Ice Age globe: down the Pacific coast (blue) and inland before the ice closed (amber)."""
    tc, ti = T("s51", "down the coast"), T("s51", "walked inland")
    g = Globe(*GLOBE44)
    lon0, lat0, Rr, cx, cy = GLOBE44
    ws = g.p(*SITE["whitesands"])
    P = lambda pts: [g.p(lo, la) for lo, la in pts]
    els = [circ(cx, cy, Rr, "#163447", at=-1), land_el(g.land(), -1, "#5b4a36"), circ(cx, cy, Rr + 5, "none", "#9fd0ff", 6, -1, op=.3),
           poly(P(BRIDGE_W), "#6e5c45", "#e3c99c", 2, -1, curve=True, style="inferred"),
           poly(P(CORD_LGM), "rgba(236,244,252,.95)", ICE_E, 2, -1, curve=True), poly(P(LAURENTIDE), "rgba(236,244,252,.95)", ICE_E, 2, -1, curve=True),
           pin(ws[0], ws[1], "White Sands", .3, GOLD, "start", 20, 8, tc=GOLD), lab(*g.p(-168, 64.5), "Beringia", .4, "#fff1d0", 34, st="ital")]
    coast = P([(-165, 62), (-152, 58.5), (-140, 58.6), (-134, 55.6), (-129, 51.5), (-125, 47), (-124, 41), (-121, 36), (-115, 33.4), (-108, 33)])
    inland = P([(-158, 66), (-142, 64), (-128, 61), (-120, 56), (-115, 50.5), (-112, 44), (-108.5, 38), (-106.6, 33.6)])
    els += [arrow(coast, tc, BLUE, 6, "inferred", 1.6), lab(*g.p(-136, 46.5), "coast", tc + .9, BLUE, 32, "end"),
            arrow(inland, ti, AMBER, 6, "inferred", 1.6), lab(910, 572, "inland, before the ice closed", ti + 1.0, AMBER, 28, "start")]
    return {"base": "dark", "stars": 120, "cam": CAM, "els": els}


# ================================================================== chapter 5: what the genes say
def book(x, y, w, h, at, c="#8a5a3a", marks=(), mc=RED, fx="pop"):
    """A small closed book, front cover facing us: cover, spine, page edge; red marks = the changes it has gathered."""
    out = [rect(x, y, w, h, c, "#e3c99c", 1.5, 4, at, fx=fx), rect(x, y, w * .14, h, "#5a3a26", at=at), rect(x + w - 6, y + 4, 4, h - 8, "#efe3c8", at=at)]
    for k, (u, v) in enumerate(marks):
        out.append(ln([(x + w * u - 7, y + h * v), (x + w * u + 7, y + h * v)], round(at + .1, 2), mc, 4, draw=False))
    return out


def s52():
    """A recipe book copied down the generations: the line forks; along each branch every copy gains a small red change; at the right
    the differences are counted, and a bracket back to the fork: when they parted."""
    tc, tf, tp = T("s52", "copied"), T("s52", "count the differences"), T("s52", "parted")
    W, H = 64, 86
    els = book(140, 380, W, H, .3) + [lab(270, 510, "a family recipe book", .5, BONE, 26)]
    els += [arrow([[214, 423], [300, 423]], tc, MUTED, 2, dur=.3, curve=False)] + book(310, 380, W, H, tc + .2, marks=[(.55, .3)])
    els += [arrow([[384, 423], [470, 423]], tc + .4, MUTED, 2, dur=.3, curve=False)] + book(480, 380, W, H, tc + .6, marks=[(.55, .3), (.55, .55)])
    els += [ln([(552, 423), (620, 423)], tc + .9, MUTED, 2, dur=.3), ln([(620, 423), (690, 280)], tc + 1.0, MUTED, 2, dur=.3), ln([(620, 423), (690, 566)], tc + 1.0, MUTED, 2, dur=.3),
            dot(620, 423, 8, GOLD, tc + 1.0), glow(620, 423, 50, tc + 1.0, .7, "lamp")]
    up = [(.55, .3), (.55, .55)]
    lo = [(.55, .3), (.55, .55)]
    for k in range(4):
        x = 700 + 200 * k
        t = round(tc + 1.2 + .25 * k, 2)
        up = up + [(.3 + .12 * k, .78)]
        lo = lo + [(.75 - .12 * k, .18)]
        els += book(x, 236, W, H, t, marks=up) + book(x, 522, W, H, t + .1, marks=lo, mc=BLUE)
        if k < 3:
            els += [arrow([[x + W + 10, 279], [x + 190, 279]], t + .1, MUTED, 2, dur=.25, curve=False), arrow([[x + W + 10, 565], [x + 190, 565]], t + .2, MUTED, 2, dur=.25, curve=False)]
    els += [ln([(1386, 300), (1420, 300), (1420, 590), (1386, 590)], tf, GOLD, 3, dur=.5), lab(1440, 430, "count the", tf + .3, GOLD, 28, "start"), lab(1440, 466, "differences", tf + .3, GOLD, 28, "start")]
    els += bracket(620, 1360, 720, tp, None, AMBER, up=True) + [lab(990, 770, "when they parted", tp + .3, AMBER, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s53():
    """Dawn over a river valley in interior Alaska: low hills, a winding river, a line of spruce, the sun rising; a soft glow on a
    terrace by the river (no remains drawn)."""
    GY = 600
    els = [poly([(-20, 470), (220, 430), (460, 470), (700, 420), (960, 460), (1200, 430), (1460, 470), (1800, 440), (1800, GY), (-20, GY)], "#3a3448", at=-1, curve=True),
           poly([(-20, 540), (300, 520), (640, 548), (980, 516), (1320, 548), (1800, 520), (1800, GY), (-20, GY)], "#2a2a30", at=-1, curve=True)]
    rr = random.Random(53)
    for k in range(26):
        x = 40 + 68 * k + rr.uniform(-12, 12)
        els.append(conifer(x, GY + 4, rr.uniform(46, 80), -1, "#1b2620", None))
    river = [(-20, 720), (300, 700), (560, 650), (800, 640), (1020, 670), (1300, 700), (1560, 690), (1800, 700)]
    els += [ln(river, -1, "#d9b38a", 26, draw=False, curve=True, op=.75), ln(river, -1, "#f3d1a6", 6, draw=False, curve=True, op=.6)]
    els += [glow(820, GY + 26, 70, .8, .9, "lamp"), circ(820, GY + 26, 8, GOLD, at=.8)]
    els += [lab(140, 200, "Upward Sun River, Alaska", .4, BONE, 30, "start"), lab(140, 240, "about 11,500 years ago", .7, MUTED, 26, "start"),
            lab(820, GY - 50, "Sunrise Child-girl", T("s53", "named her"), GOLD, 32)]
    return {"base": "sky", "tod": "dawn", "ground": GY, "sun": [1260, 470, 30], "ridges": [], "groundc": "#2d2a26", "cam": CAM, "els": els}


def XT(ya):                                     # the tree's axis: 40,000 years ago at x 160, 10,000 at x 1580
    return round(160 + (40000 - ya) / 30000 * 1420, 1)


def s54():
    """The family tree along a time axis: a trunk of East Asian peoples; a branch splits off (the ancestors of Native Americans);
    from below, Siberians related to the Lake Baikal boy (24,000) join it."""
    tb, tm, tl = T("s54", "branched off"), T("s54", "mixed with Siberians"), T("s54", "Lake Baikal")
    AY = 720
    els = [axis(160, 1580, AY, [(XT(v), "{:,}".format(v)) for v in (40000, 30000, 20000, 10000)], .2, "years ago")]
    els += [ln([(160, 260), (1580, 260)], .4, MUTED, 7, dur=1.2), lab(240, 236, "East Asian peoples", .8, MUTED, 28, "start")]
    br = [(XT(36000), 260), (XT(33000), 340), (XT(29000), 400), (1580, 420)]
    els += [ln(br, tb, GOLD, 8, dur=1.4, curve=True), lab(XT(28500), 456, "ancestors of Native Americans", tb + .8, GOLD, 28)]
    els += [ln([(XT(35000) + 60 * k, 270), (XT(35000) + 60 * k + 20, 360)], round(tb + .9 + .06 * k, 2), GOLD, 2, "inferred", .3) for k in range(8)]
    sib = [(160, 640), (XT(30000), 630), (XT(26000), 600), (XT(23000), 500), (XT(21000), 432)]
    els += [ln(sib, tm, BLUE, 6, "inferred", 1.2, curve=True), lab(240, 616, "Siberians", tm + .3, BLUE, 28, "start")]
    bx, by = XT(24000), 560
    els += [dot(bx, by, 12, BLUE, tl), glow(bx, by, 50, tl, .8, "blue"), lab(bx + 22, by + 44, "Lake Baikal boy, 24,000", tl + .2, BLUE, 26, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def XU(ya):                                     # the second tree panel: 26,000 years ago at x 160, 10,000 at x 1580
    return round(160 + (26000 - ya) / 16000 * 1420, 1)


def s55():
    """The tree goes on (up = north of the ice, down = south of it): the branch runs through a shaded box (the long pause, Beringia?);
    about 20,000 it forks: one twig stays in the north (Ancient Beringians); the other drops below the ice line and forks again about
    16,000 into north and south."""
    tp, tn, ts = T("s55", "long pause"), T("s55", "one branch stayed"), T("s55", "The other moved")
    AY = 720
    els = [axis(160, 1580, AY, [(XU(v), "{:,}".format(v)) for v in (26000, 22000, 18000, 14000, 10000)], .2, "years ago")]
    TY, IY = 360, 430                                   # the trunk (in the north) and the ice line; up = north of the ice, down = south
    els += [ln([(160, TY), (XU(20000), TY)], .3, GOLD, 8, dur=.8)]
    els += [rect(XU(25000), 310, XU(18000) - XU(25000), 100, "rgba(201,173,133,.12)", "#e3c99c", 2, 14, tp, style="inferred"),
            lab((XU(25000) + XU(18000)) / 2, 294, "the pause, Beringia?", tp + .3, "#e3c99c", 28)]
    els += [ln([(XU(20000), TY), (XU(19000), 304), (XU(16000), 300), (XU(11500), 300)], tn, "#c9ad85", 6, dur=1.0, curve=True),
            lab(XU(14000), 280, "Ancient Beringians", tn + .6, "#c9ad85", 26)]
    els += [ln([(XU(19500), IY), (1580, IY)], ts - .2, "#ffffff", 5, dur=.6, op=.8), lab(1580, IY - 14, "the ice", ts, "#ffffff", 26, "end")]
    els += [ln([(XU(20000), TY), (XU(19000), 392), (XU(18000), 470), (XU(16000), 540)], ts, GOLD, 8, dur=.8, curve=True)]
    els += [ln([(XU(16000), 540), (XU(14500), 500), (1580, 500)], ts + .9, GOLD, 6, dur=.8, curve=True), lab(1560, 484, "north", ts + 1.3, GOLD, 28, "end"),
            ln([(XU(16000), 540), (XU(14500), 600), (1580, 620)], ts + 1.0, GOLD, 6, dur=.8, curve=True), lab(1560, 662, "south", ts + 1.4, GOLD, 28, "end"),
            dot(XU(16000), 540, 10, GOLD, ts + .9)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s56():
    """Montana at late afternoon: a sandstone outcrop; Clovis tools coloured with red ochre on the ground by it (no remains drawn); on the
    right, the southern branch fans out into many small figures: many living Native peoples."""
    tb, tl = T("s56", "southern branch"), T("s56", "many living")
    GY = 620
    els = [poly([(-20, 470), (260, 430), (560, 470), (860, 440), (1200, 470), (1500, 430), (1800, 460), (1800, GY), (-20, GY)], "#5a5040", at=-1, curve=True),
           poly([(170, GY), (200, 540), (236, 470), (250, 404), (300, 388), (380, 380), (470, 386), (520, 398), (546, 440), (560, 500), (600, 560), (640, GY)],
                "#a8825a", "#e3c99c", 2, -1),
           poly([(250, 404), (300, 388), (380, 380), (470, 386), (520, 398), (500, 412), (300, 414)], "#c9a070", at=-1)]
    els += [ln([(206 + 4 * k, 430 + 34 * k), (548 + 10 * k, 430 + 34 * k + 6)], -1, "#8a6a48", 2, draw=False, op=.7) for k in range(5)]
    els += [poly([(560, GY), (590, 560), (640, 590), (700, GY)], "#8a7356", at=-1), poly([(150, GY), (170, 580), (210, GY)], "#8a7356", at=-1)]
    els = els
    for k, (x, a) in enumerate(((640, 70), (690, -30), (740, 100), (790, 10), (850, 120), (900, -60))):
        els += stone_point(x, GY + 36, 40, round(.4 + .08 * k, 2), "#c46a4a", "#f0b09a", ang=a, flute=False)
    els += [glow(770, GY + 20, 120, .4, .5, "fire"), lab(560, 200, "Montana, about 12,600 years ago", .6, BONE, 30)]
    els += [ln([(1110, 180), (1180, 280), (1240, 380)], tb, GOLD, 6, dur=.8, curve=True), lab(1110, 160, "south", tb, GOLD, 26)]
    for k in range(13):
        x = 1120 + 46 * k
        t = round(tl + .06 * k, 2)
        els += [ln([(1240, 380), (x, 520)], t, GOLD, 1.5, dur=.4, op=.6), figure(x, 600, 70 + 6 * (k % 3), t + .2, "#e8d6b8")]
    els += [lab(1400, 680, "many living Native peoples", tl + 1.0, BONE, 28)]
    return {"base": "sky", "tod": "dusk", "ground": GY, "sun": [180, 300, 22], "ridges": [], "groundc": "#4a3f30", "cam": CAM, "els": els}


def s57_add():
    """2014: a small group gathered by the outcrop as the light warms; a soft glow where the tools lay."""
    t = T("s57", "twenty fourteen")
    els = [glow(420, 600, 220, t, .5, "lamp")]
    for k, x in enumerate((140, 190, 600, 650, 960, 1010)):
        els.append(figure(x, 640, 96 + 8 * (k % 2), round(t + .2 + .1 * k, 2), "#2a221b"))
    els += [lab(420, 300, "2014", t + .3, GOLD, 40)]
    return els


def XG(ya):                                     # the genes and the prints: 26,000 years ago at x 200, 14,000 at x 1580
    return round(200 + (26000 - ya) / 12000 * 1380, 1)


def s58():
    """The rub: the gold band of White Sands (23,000 to 21,000) above the blue bar of the first parting from genes (22,000 to 18,000),
    reaching older; then three option cards: clocks adjusted? no descendants? dates wrong?"""
    tw, t1, t2, t3 = T("s58", "The White Sands"), T("s58", "Either"), T("s58", "or the first walkers"), T("s58", "say the sceptics")
    AY = 440
    els = [axis(200, 1580, AY, [(XG(v), "{:,}".format(v)) for v in (26000, 24000, 22000, 20000, 18000, 16000, 14000)], .2)]
    els += [band(XG(22000), XG(18000), AY - 90, 26, BLUE, .4), lab((XG(22000) + XG(18000)) / 2, AY - 106, "first parting (genes)", .6, BLUE, 28)]
    els += [band(XG(23000), XG(21000), AY - 190, 26, GOLD, tw), lab((XG(23000) + XG(21000)) / 2, AY - 206, "White Sands", tw + .2, GOLD, 30),
            glow(XG(23000), AY - 176, 90, tw + .4, .6, "lamp")]
    xs = (200, 700, 1200)
    for k, (x, t, name) in enumerate(zip(xs, (t1, t2, t3), ("clocks adjusted?", "no descendants?", "dates wrong?"))):
        els += [rect(x, 540, 380, 200, "rgba(201,193,238,.05)", LILAC, 2, 14, t, style="inferred", fx="pop"), lab(x + 190, 770, name, t + .3, LILAC, 28)]
    cx, cy = 390, 640
    els += [circ(cx, cy, 60, "none", BONE, 3, t1 + .2), ln([(cx, cy), (cx, cy - 40)], t1 + .3, BONE, 4, draw=False), ln([(cx, cy), (cx + 30, cy + 10)], t1 + .3, BONE, 4, draw=False),
            arrow([[cx + 80, cy - 40], [cx + 96, cy], [cx + 80, cy + 40]], t1 + .4, LILAC, 3, dur=.4)]
    els += [ln([(760, 640), (860, 640), (940, 610)], t2 + .2, GOLD, 6, dur=.5, curve=True), ln([(940, 610), (1010, 590)], t2 + .5, GOLD, 6, "claimed", .4)]
    els += [band(1260, 1520, 620, 26, GOLD, t3 + .2)] + qmark(1390, 610, t3 + .5, 70, LILAC, halo=False)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s59():
    """Night under a wide sky of stars: a small fire with a circle of seated figures (plain silhouettes); apart and small at the right,
    a balance with a stone, a seed and a date tag: what this film weighs."""
    tb = T("s59", "this film weighs")
    GY = 640
    els = [glow(760, GY - 30, 260, .3, .7, "fire"), poly([(730, GY), (750, GY - 60), (762, GY - 30), (772, GY - 70), (790, GY)], "#ffb36a", at=.3, fx="pop")]
    for k, (x, f) in enumerate(((560, 1), (620, 1), (680, 1), (840, -1), (900, -1), (960, -1))):
        els += seated(x, GY, 96 + 6 * (k % 2), round(.4 + .08 * k, 2), "#1a1512", face=f)
    rr = random.Random(59)
    els += [dot(760 + rr.uniform(-30, 30), GY - 100 - 40 * q, 3, "#ffd27a", round(.6 + .2 * q, 2)) for q in range(6)]
    def stone(x, y, at):
        return [poly(E(x, y - 14, 26, 16, 14), "#9a948a", "#e9e1d2", 1.5, at, fx="pop", curve=True)]
    def seed_tag(x, y, at):
        return [poly(E(x - 30, y - 10, 9, 13, 12), "#7a5a2a", "#e3c99c", 1.2, at, fx="pop", curve=True)] + tag(x + 30, y - 12, "date", at + .1, AMBER, 20)
    els += balance(1440, 470, 300, 0, 640, tb, stone, seed_tag, drop=110, pan=130)
    els += [lab(1440, 720, "stones, seeds and dates", tb + .4, MUTED, 26)]
    return {"base": "sky", "tod": "night", "ground": GY, "sun": False, "moon": [300, 180, 22], "ridges": [{"y": GY - 40, "a": 60, "c": "#1d1b24", "seed": 5}],
            "groundc": "#1e1914", "cam": CAM, "els": els}


# ================================================================== chapter 6: the weighing
def pic_clovis(x, y, at):
    return stone_point(x, y + 34, 70, at, "#d6cebd")


def pic_before(x, y, at):
    return [poly(E(x - 22, y + 10, 18, 10, 14), "#6a4a2a", "#b08a62", 1.2, at, fx="pop", curve=True)] + stone_point(x + 24, y + 34, 64, at + .1, "#d8cfbf", stemmed=True)


def pic_stake(x, y, at):
    return [ln([(x, y + 34), (x + 6, y - 34)], at, WOOD, 12, draw=False), poly([(x - 6, y + 34), (x + 12, y + 34), (x + 3, y + 48)], WOOD, at=at)]


def pic_print(x, y, at):
    return footprint(x, y, 84, 0, at, "R", fill="#c9a070", rim="#f2dcb0", shade="#8a6a48", detail=False)


def pic_chips(x, y, at):
    return [poly([(x - 30 + 20 * q, y + 8 * (q % 2)), (x - 22 + 20 * q, y - 10), (x - 12 + 20 * q, y - 4), (x - 16 + 20 * q, y + 10)], "#2f6e5e", "#b9d8cc", 1, at, fx="pop", style="claimed") for q in range(3)]


def pic_bone(x, y, at):
    return broken_bone(x - 40, y, x + 20, y - 10, at, w=18) + [poly(E(x + 36, y + 10, 16, 13, 14), "#8f8a80", "#cfc9bd", 1.5, at, fx="pop", curve=True)]


def pic_boat(x, y, at):
    return [ln([(x - 50, y + 20), (x + 50, y + 20)], at, BLUE, 3, draw=False)] + boat(x, y + 18, 90, at)


LROWS = [205, 325, 445]


def lrow(y, at, pic, text, grade=None, gt=None, gc=None, size=30, h=100):
    out = [rect(140, y - h / 2, 1500, h, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, size, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1180, y, grade, gc, gt, 30, "start")
    return out


def s60():
    """The ledger: three rows light as they are named and their grade chips pop (Ruled out, Established, Open question); below them,
    the verdict row waits, unlit."""
    t1, g1 = T("s60", "Clovis first"), T("s60", "Ruled out")
    t2, g2 = T("s60", "People here before"), T("s60", "Established")
    t3, g3 = T("s60", "And Monte Verde itself"), T("s60", "Open question")
    els = [rect(110, 140, 1560, 640, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(LROWS[0], t1, pic_clovis, "Clovis first", "Ruled out", g1, GRADE["ruled"])
    els += lrow(LROWS[1], t2, pic_before, "here before Clovis, 14,000+ years", "Established", g2, GRADE["established"])
    els += lrow(LROWS[2], t3, pic_stake, "Monte Verde at 14,500", "Open question", g3, GRADE["open"])
    els += [rect(140, 520, 1500, 230, "rgba(127,209,212,.04)", "rgba(127,209,212,.35)", 1.5, 14, t3 + 1.0, style="inferred")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s61_add():
    """The verdict row lights: the footprint, 'Strong evidence' large; four small clocks tick (seeds, pollen, mud, quartz); then the
    gaps, muted: one site, some sceptics, no bones or DNA yet."""
    tq, tv, ta, tg = T("s61", "People in the Americas"), T("s61", "Strong evidence"), T("s61", "Seeds, pollen"), T("s61", "What holds")
    els = [rect(140, 520, 1500, 230, "rgba(127,209,212,.10)", GRADE["strong"], 2.5, 14, tq, fx="pop")]
    els += pic_print(230, 600, tq + .1) + [lab(300, 612, "here by about 21,000 years ago", tq + .2, BONE, 32, "start")]
    els += chip(1150, 602, "Strong evidence", GRADE["strong"], tv, 36, "start") + [glow(1330, 602, 260, tv, .35, "lamp")]
    for k, (name, c) in enumerate((("seeds", GOLD), ("pollen", GREEN), ("mud", "#e3c99c"), ("quartz", BLUE))):
        x = 330 + 150 * k
        t = round(ta + .35 * k, 2)
        els += [tick(x, 690, t, c, .8), lab(x + 22, 700, name, t, c, 26, "start")]
    els += [lab(1600, 712, "one site · some sceptics · no bones or DNA yet", tg + .3, MUTED, 24, "end")]
    return els


def s62():
    """A second, shorter ledger: Chiquihuite (Open question), San Diego (Awaiting evidence), the coast first (Plausible)."""
    t1, g1 = T("s62", "Chiquihuite"), T("s62", "Open question")
    t2, g2 = T("s62", "A hundred and thirty"), T("s62", "Awaiting evidence")
    t3, g3 = T("s62", "And the road"), T("s62", "Plausible")
    rows = [270, 430, 590]
    els = [rect(110, 170, 1560, 520, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(rows[0], t1, pic_chips, "Chiquihuite, 30,000 years?", "Open question", g1, GRADE["open"], h=120)
    els += lrow(rows[1], t2, pic_bone, "San Diego, 130,000 years?", "Awaiting evidence", g2, GRADE["awaiting"], h=120)
    els += lrow(rows[2], t3, pic_boat, "down the coast first", "Plausible", g3, GRADE["plausible"], h=120)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s63():
    """Four test boxes (dashed: tests not yet done) fill as named: a tooth and DNA in a layer older than 20,000; new footprints with
    three clocks; a shared trench at Monte Verde; a sonar fan over a drowned shore where a small camp waits."""
    t1, t2, t3, t4 = (T("s63", p) for p in ("A human bone", "More footprint", "At Monte Verde", "And on the drowned"))
    xs = [110, 506, 902, 1298]
    names = ("a bone or DNA, 20,000+", "more footprint sites", "a shared trench", "the drowned coast")
    els = []
    for x, t, name in zip(xs, (t1, t2, t3, t4), names):
        els += [rect(x, 200, 370, 420, "rgba(159,208,255,.05)", BLUE, 2.5, 14, t - .2, style="inferred", fx="pop"), lab(x + 185, 670, name, t + .3, BLUE, 26)]
    x = xs[0]
    els += [rect(x + 30, 420, 310, 160, "#6d604e", at=t1), rect(x + 30, 420, 310, 30, "#8a7a62", at=t1)] + \
           [poly([(x + 120, 470), (x + 150, 470), (x + 146, 520), (x + 136, 540), (x + 124, 520)], "#efe6d4", "#fff6e6", 1.5, t1 + .3, fx="pop")] + \
           helix(x + 200, 500, x + 320, 500, t1 + .6, n=8, amp=12, w=2.5, dur=.6) + [lab(x + 185, 300, "older than 20,000", t1 + .4, GOLD, 24)]
    x = xs[1]
    for k in range(4):
        els += mini_print(x + 90 + 70 * k, 520 - 40 * (k % 2), 50, round(t2 + .1 * k, 2), "#e9d9b8", 70)
    for k in range(3):
        cx = x + 100 + 85 * k
        els += [circ(cx, 320, 28, "none", BONE, 3, round(t2 + .5 + .15 * k, 2)), ln([(cx, 320), (cx, 300)], round(t2 + .5 + .15 * k, 2), BONE, 3, draw=False),
                ln([(cx, 320), (cx + 14, 326)], round(t2 + .5 + .15 * k, 2), BONE, 3, draw=False)]
    x = xs[2]
    els += [rect(x + 120, 430, 130, 140, "#3a2c20", "#e3c99c", 2, 4, t3), rect(x + 30, 410, 340, 20, "#6d604e", at=t3)]
    els += [figure(x + 70 + 26 * k, 410, 70, round(t3 + .3 + .08 * k, 2), AMBER) for k in range(2)] + [figure(x + 280 + 26 * k, 410, 70, round(t3 + .5 + .08 * k, 2), BLUE) for k in range(2)]
    x = xs[3]
    els += [poly([(x + 20, 600), (x + 120, 560), (x + 220, 540), (x + 350, 520), (x + 350, 600)], "#4a3d2f", at=t4),
            rect(x + 20, 260, 330, 280, "#2f5f78", at=t4, op=.5),
            {"k": "fan", "x": x + 185, "y": 268, "r": 270, "a0": 62, "a1": 118, "n": 9, "c": BLUE, "in": round(t4 + .3, 2)},
            poly([(x + 210, 548), (x + 236, 512), (x + 262, 546)], "#8a6a44", "#e7c99a", 1.5, t4 + .8, fx="pop"), glow(x + 236, 530, 50, t4 + .8, .7, "lamp")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s64():
    """Night on the old lake bed under a sky full of stars: a trail of small footprints leads away across the pale ground towards the
    dark dunes; the last print glows softly."""
    tf = T("s64", "still waiting")
    GY = 470
    els = [poly([(-20, GY), (200, GY - 30), (480, GY - 10), (760, GY - 40), (1040, GY - 14), (1340, GY - 36), (1600, GY - 12), (1800, GY - 24), (1800, GY + 4), (-20, GY + 4)],
                "#d6d0c2", at=-1, curve=True, op=.35)]
    for k in range(9):
        t = (k / 8.0)
        L = 120 - 100 * t
        x = 420 + 700 * t ** .8
        y = 790 - (790 - GY - 30) * t ** .7
        els += footprint(x, y, L, 70 - 10 * t, round(.2 + .12 * k, 2), "L" if k % 2 else "R", fill="#6d6458", rim="#b9b1a2", shade="#4a443c", detail=k < 4,
                         light=(-1, -.4))
    lx, ly = 420 + 700, GY + 30
    els += [glow(lx, ly, 70, tf, .9, "lamp")]
    return {"base": "sky", "tod": "night", "ground": GY, "sun": False, "moon": [1460, 190, 24], "ridges": [{"y": GY - 6, "a": 28, "c": "#2a2834", "seed": 7}],
            "groundc": "#8f877a", "cam": CAM, "els": els}
