"""LF.07 · Impossible Stones · Gunung Padang: Inside the Hill (16:9 long film, one wall).

Script: films/long/lf-gunung-padang/script.json. Its lines are read from there at compile time, untouched; only [go:N|t] markers
are added at the sentence where the picture changes (see BEATS). One shot per script shot s1..s54, drawn while it is said: a
terraced hill in West Java and the pyramid claimed inside it, the terraces as archaeology dates them, lava that splits itself
into columns, the Indonesian team's scans, cores and soil dates at their strongest, the retraction and the team's reply, and the
trench that would settle it. Drawings are schematic and true to the numbers said: solid = observed, dashed = inferred or worn
away, dotted = claimed (the team's reading, the pyramid). The hill sections are roughly to scale (about 4 units a metre; the
summit sections 15 units a metre, after the 2023 paper's own unit thicknesses).

Facts: the script's facts_added and sources (Natawidjaja et al. 2023 and its retraction notice; Archaeology 2024 on Yondri's
excavations; Yondri 2014; Bronto & Langi; USGS; Ege 2001; Müller 1998; Goehring et al. 2006; Voris 2000; Oktaviana et al. 2026;
Lewis 2023; McKie 2023; Rhodes 2011). Short reused: 'gunung-padang' (f06.py): its iso summit (hill, five terraces, the stair),
its map, the hook page and stamp, the lava and drying cracks, the tag tied to soil, all redrawn wide for 16:9. 'drowned-coasts'
(f04.py): its Sundaland outline. 'lost-civilization' (f04.py): the place of the first farms on the time bar.

How the wall is built (copied from lf_gobekli / lf_atlantis): most shots are panels of their own. A shot that adds to a picture
already on the wall is an alias of that panel with its own camera, tagged with a tiny unique extra zoom; its additions are
attached to the step that camera makes, so they build on that step's clock (mural.wall() only adds to a panel on its first visit
or at a line start). A speech Clock estimates when each phrase is said, so build-ins follow the narration.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-gunung-padang/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-gunung-padang/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-gunung-padang RC_FILMS_EPS=/tmp/claude-0/sbx_lf-gunung-padang/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-gunung-padang/boards python3 films.py long.lf_gunung_padang
"""
import json, math, os, random, re
from films import View
from mural import remix, SENT
from illus import person, arrow, line, glow, label, dot, box, oval, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-gunung-padang", "script.json")
W_, H_ = 1778, 1000                   # the 16:9 frame: drawings in x 80..1700, y 120..800 (captions below 815, HUD above 110)
CAM = [1, 889, 500]

BONE, INK, AMBER, RED, GREEN, BLUE, LILAC = "#f5ecdc", "#1a1511", "#e8b87a", "#ff8a7a", "#8fd9b0", "#9fd0ff", "#c9c1ee"
GOLD, DIM, ICE, PAPER = "#f2c98e", "#cbbca8", "#cfe6ff", "#efe6d2"
ANDE, ANDE_L, ANDE_E = "#5b5750", "#7a766d", "#a9a294"           # andesite: a dark grey volcanic rock
TERR, TERR_E = "#b9b3a0", "#efe6d2"                              # the terrace stones, seen in the light
GRASS, GRASS_E, ROCK, SOIL, SOIL_D = "#3d5530", "#8fb070", "#2f2a26", "#6d5a44", "#4a3c2e"
LAVA, OCHRE, FLAT = "#d0502a", "#c8553a", "#17120e"
GRADE = {"established": "#8fd9b0", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#b8b2a8"}


# ================================================================ drawing helpers (panel units)
def R(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def r1(v):
    return round(v, 1)


def poly(pts, fill, c="none", w=0, at=0, fx=None, op=None, curve=False, style="known", **kw):
    e = {"k": "poly", "p": R(pts), "fill": fill, "c": c, "w": w, "in": round(at, 2), "curve": curve, "style": style}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def lab(x, y, t, at, c=BONE, size=28, a="middle", st="lab", **kw):
    return label(r1(x), r1(y), t, round(at, 2), c, size, a, st, **kw)


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(r1(x), r1(y), r1(w), r1(h), fill, c, sw, r, round(at, 2), op, fx, **kw)


def ln(pts, at, c=BONE, w=3, style="known", dur=None, draw=True, op=None, curve=False):
    return line(R(pts), round(at, 2), c, w, style, dur, curve, draw, op)


def arr(pts, at, c=AMBER, w=3, style="known", dur=1.0, curve=True):
    return arrow(R(pts), round(at, 2), c, w, style, dur, curve)


def gl(x, y, r, at, op=.6, kind="lamp"):
    return glow(r1(x), r1(y), r, round(at, 2), op, kind)


def dt(x, y, r, fill, at, fx="pop", op=None):
    return dot(r1(x), r1(y), r, fill, round(at, 2), fx, op)


def chip(x, y, t, c, at, size=27, a="middle", fill="rgba(18,13,10,.88)"):
    """A rounded tag with a few words (centred on x, or starting at x with a='start'); scales with the picture like a plaque."""
    w = len(t) * size * .56 + 40
    h = size * 1.65
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, fill, c, 2.5, h / 2, at, fx="pop"),
            label(r1(x0 + w / 2), r1(y + size * .36), t, round(at + .05, 2), c, size, scl=True, fx="pop")]


def strk(x0, y0, x1, y1, at, c=RED, w=6):
    return strike(r1(x0), r1(y0), r1(x1), r1(y1), round(at, 2), c, w)


def tick(x, y, at, c=GREEN, s=1.0):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "draw", "dur": .45, "in": round(at, 2)}


def dimline(x1, y1, x2, y2, t, at, c=GOLD, lx=0, ly=None, dur=.9):
    e = {"k": "dim", "x1": r1(x1), "y1": r1(y1), "x2": r1(x2), "y2": r1(y2), "t": t, "c": c, "fx": "draw", "dur": dur, "in": round(at, 2), "lx": lx}
    if ly is not None:
        e["ly"] = ly
    return e


def arc(cx, cy, r, a0, a1, n=16):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def ngon(cx, cy, r, n=6, rot=0.0):
    return [(cx + r * math.cos(math.radians(rot + 360 * k / n)), cy + r * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]


def wipe(x, y, w, h, at, fill=FLAT, op=1.0, dur=.5, r=0):
    """A sheet laid over part of a panel: what was there fades back (op < 1) or is hidden (op 1)."""
    e = rect(x, y, w, h, fill, "none", 0, r, at, op=op)
    e["dur"] = dur
    return e


def smooth(pts, n=8):
    """Points along a Catmull-Rom curve through pts (as kit.js draws curve=True)."""
    P, out = [pts[0]] + list(pts) + [pts[-1]], []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(.5 * (2 * p1[j] + (p2[j] - p0[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out + [tuple(pts[-1])]


def y_at(x, pts):
    """The height of a polyline (sorted by x) at x."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0 or 1)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]


def person_(x, y, h, at, c="#e8d6b8", fx="rise"):
    return person(r1(x), r1(y), r1(h), round(at, 2), c, fx)


# ---------------------------------------------------------------- iso (copied from lf_under_giza)
C30 = math.cos(math.pi / 6)


def iso(items, x, y, s, az, spin=0.0, el=.32, at=-1, **kw):
    e = {"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": items, "in": round(at, 2) if at >= 0 else at}
    e.update(kw)
    return e


def ov(base, items, at, fx="pop", **kw):
    """An overlay model: the same camera, scale and turn as `base`, other items, its own build-in."""
    e = {k: base[k] for k in ("x", "y", "s", "az", "spin", "el")}
    e.update(k="iso", items=items, **{"in": round(at, 2)})
    if fx:
        e["fx"] = fx
    e.update(kw)
    return e


def P3(e, p, t=0.0):
    """Where a world point (x, y, z) of an iso element lands on the panel at local time t."""
    az = math.radians(e.get("az", 35) + e.get("spin", 0) * t)
    ca, sa = math.cos(az), math.sin(az)
    x, y, z = p
    rx, rz = x * ca - z * sa, x * sa + z * ca
    S, el = e["s"], e.get("el", .32)
    return [r1(e["x"] + (rx - rz) * C30 * S), r1(e["y"] - y * S + (rx + rz) * el * S)]


def ibox(x, z, y, w, d, h, c=TERR, e="rgba(0,0,0,.32)", **kw):
    b = {"t": "box", "x": x, "z": z, "y": y, "w": w, "d": d, "h": h, "c": c, "edge": e}
    b.update(kw)
    return b


# ---------------------------------------------------------------- a balance (copied from lf_gobekli)
def balance(cx, py, L, ang, base_y, at, left=None, right=None, drop=170, pan=170, c=BONE):
    a = math.radians(ang)
    ends = [(cx - L / 2 * math.cos(a), py - L / 2 * math.sin(a)), (cx + L / 2 * math.cos(a), py + L / 2 * math.sin(a))]
    out = [rect(cx - 70, base_y - 10, 140, 14, "#5a4836", "#8c7152", 1.5, 4, at), ln([(cx, base_y - 8), (cx, py)], at, "#8c7152", 8, draw=False),
           ln(ends, at, c, 6, draw=False), dt(cx, py, 10, GOLD, at, None)]
    for (ex, ey), stuff in zip(ends, (left, right)):
        fy = ey + drop
        out += [ln([(ex, ey), (ex - pan / 2 + 10, fy)], at, DIM, 1.6, draw=False), ln([(ex, ey), (ex + pan / 2 - 10, fy)], at, DIM, 1.6, draw=False),
                poly([(ex - pan / 2, fy), (ex + pan / 2, fy), (ex + pan / 2 - 18, fy + 16), (ex - pan / 2 + 18, fy + 16)], "#6b5a48", "#cbb79a", 1.5, at)]
        if stuff:
            out += stuff(r1(ex), r1(fy), at)
    return out


# ================================================================ timing: when each word is said (an estimate, from syllables; lf_gobekli)
TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # BCE: three letters
    w = a.lower()
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def _spoken(seg):
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", TAGS.sub(" ", seg))
    return re.sub(r"@\w+", "", s.replace("^", "").replace("*", "")).split()


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Clock:
    """Estimated word times per beat. A shot's step starts at its [go:] marker (or at the beat's first word; at a chapter beat's
    second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said, from the start of shot i's step."""
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
            self.start.setdefault(frm, (bi, sents[1] if b.get("chapter") else 0.0))
            self.words[bi] = ws
            self.end = getattr(self, "end", {})
            self.end[bi] = t

    def at(self, i, phrase, lo=.4):
        bi, ti = self.start[i]
        want = [_norm(x) for x in phrase.split()]
        ws = self.words[bi]
        for k in range(len(ws)):
            if ws[k][1] >= ti - 1e-6 and [w for w, _ in ws[k:k + len(want)]] == want:
                return round(max(lo, ws[k][1] - ti), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))

    def span(self, i):
        """Seconds from shot i's step start to the end of its beat."""
        bi, ti = self.start[i]
        return round(self.end[bi] - ti, 2)


CLK = [None]


def T(n, phrase, d=0.0):
    """When `phrase` is said, in seconds from the start of shot n's step (n = the script's shot number)."""
    return round(max(.1, CLK[0].at(n - 1, phrase) + d), 2)


# ================================================================ the hill: one schematic profile (about 4.1 units a metre)
# north (the stair) on the left, the five terraces stepping up to the south; foot y 800, summit about 110 m above it
TER = [(650, 860, 372), (860, 985, 354), (985, 1085, 345), (1085, 1172, 338), (1172, 1272, 326)]     # (x0, x1, top) T1..T5
HILL_N = [(40, 820), (180, 790), (300, 728), (420, 610), (540, 492), (630, 400), (650, 372)]
HILL_S = [(1272, 326), (1300, 338), (1400, 410), (1520, 520), (1640, 660), (1760, 780), (1840, 820)]


def hill_top():
    pts = list(HILL_N)
    for x0, x1, y in TER:
        if pts[-1][1] != y:
            pts.append((x0, y))
        pts.append((x1, y))
    return pts + HILL_S[1:]


def hill_poly():
    top = hill_top()
    return top + [(1840, 1010), (40, 1010)]


def stair_pts():
    """The stair up the north slope as a zigzag: 18 drawn steps (it has about 370)."""
    a, b, n = (306, 724), (646, 376), 18
    out = [a]
    for k in range(n):
        x0, y0 = out[-1]
        out += [(x0, y0 - (a[1] - b[1]) / n), (x0 + (b[0] - a[0]) / n, y0 - (a[1] - b[1]) / n)]
    return out


def terraces(at, dt_=.3, fill=TERR, edge=TERR_E, fx="rise", op=None, wall=11):
    """The five terraces as low stone walls on the crest (T1 first)."""
    out = []
    for k, (x0, x1, y) in enumerate(TER):
        out.append(poly([(x0 + 4, y - wall), (x1 - 2, y - wall), (x1 - 2, y + 2), (x0 + 4, y + 2)], fill, edge, 1.4, at + dt_ * k, fx, op=op))
    return out


def trees(at, seed=4, n=14, c="#26361e"):
    r = random.Random(seed)
    top = hill_top()
    out = []
    for k in range(n):
        x = r.choice([r.uniform(120, 600), r.uniform(1320, 1700)])
        y = y_at(x, top) + r.uniform(18, 60)
        rr = r.uniform(14, 24)
        out.append(dt(x, y - rr * .5, rr, c, at + .02 * k, fx=None))
    return out


def hill_section(at=-1, grass=True, rock=ROCK, joints=True, seed=3):
    """The hill as a cutaway: rock below a green skin, faint natural column joints inside."""
    top = hill_top()
    out = [poly(hill_poly(), rock, "none", 0, at)]
    if joints:
        r = random.Random(seed)
        for k in range(46):
            x = 90 + 37 * k + r.uniform(-8, 8)
            y0 = y_at(x, top) + 22
            if y0 > 990:
                continue
            lean = r.uniform(-14, 14)
            out.append(ln([(x, y0), (x + lean, 1010)], at, "#1b1815", 3, draw=False, op=.8))
    if grass:
        out.append(ln(top, at, GRASS_E, 3, draw=False))
    return out


# ================================================================ chapter 0: cold open
def s01():
    """The opening image: dusk over West Java, one green hill, five stone terraces on its crest, the stair, far volcanoes."""
    els = [poly([(80, 820), (300, 440), (360, 452), (620, 820)], "#3b3140", "none", 0, -1, op=.85, layer="far"),
           poly([(1180, 820), (1500, 410), (1560, 418), (1840, 820)], "#3b3140", "none", 0, -1, op=.8, layer="far"),
           gl(889, 800, 700, -1, .12, "lamp")]
    els += [poly(hill_poly(), GRASS, GRASS_E, 2.2, -1)] + trees(-1)
    els += terraces(.4)
    els += [ln(stair_pts(), 1.2, TERR_E, 2.2, dur=1.4), person_(1222, 315, 12, 2.2, "#f5ecdc")]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [1420, 250, 22], "cam": CAM, "els": els}


def PYR(cx=960, base=790, w0=880, top=380, n=5):
    """The claimed stepped pyramid inside the hill (dotted: claimed)."""
    h = (base - top) / n
    pts = []
    for k in range(n):
        w = w0 * (1 - k / (n + .6))
        pts += [(cx - w / 2, base - h * k), (cx - w / 2, base - h * (k + 1))]
    pts2 = []
    for k in range(n - 1, -1, -1):
        w = w0 * (1 - k / (n + .6))
        pts2 += [(cx + w / 2, base - h * (k + 1)), (cx + w / 2, base - h * k)]
    return pts + pts2


def s02_add():
    at = T(2, "lies a pyramid", -.2)
    return [poly(hill_poly(), "rgba(14,11,9,.62)", "none", 0, .3, dur=1.0),
            poly(PYR(), "rgba(201,193,238,.07)", LILAC, 3, at, fx="draw", style="claimed", dur=1.6),
            gl(960, 600, 300, at + .4, .25, "blue"),
            lab(960, 660, "27,000 years?", T(2, "twenty-seven"), LILAC, 36)]


def s05_add():
    a = T(5, "So is there", .3)
    b = T(5, "how would anyone")
    trowel = [poly([(752, 330), (772, 300), (792, 330), (772, 352)], "#c9ccd2", "#efe6d2", 1.5, b, fx="pop"),
              ln([(772, 300), (772, 268)], b, "#8a6a44", 6, draw=False)]
    core = [{"k": "lib", "k2": "core", "x": 1222, "y": 318, "w": 18, "h": 64, "grooves": 4, "in": round(b + .4, 2), "fx": "rise"}]
    return [gl(960, 560, 260, a, .45, "blue"), lab(960, 640, "?", a, LILAC, 160, st="big", fx="pop", dur=.8)] + trowel + core


def s03():
    """A time bar of years ago, today on the right: the Ice Age, the first farms, the claimed pyramid at 27,000."""
    X = lambda ya: r1(1600 - ya * 1400 / 27000)
    y = 540
    els = [ln([(1600, y), (200, y)], .3, BONE, 3, dur=1.6)]
    for k, (ya, t) in enumerate(((0, "today"), (10000, "10,000"), (20000, "20,000"), (27000, "27,000"))):
        at = .4 + 1.5 * (1 - (X(ya) - 200) / 1400)
        els += [ln([(X(ya), y - 10), (X(ya), y + 10)], at, BONE, 2, draw=False), lab(X(ya), y + 46, t, at, DIM, 25)]
    els += [lab(200, y + 92, "years ago", 2.0, DIM, 24, "start")]
    ice = T(3, "Ice Age", -.3)
    els += [rect(200, y - 64, X(11700) - 200, 34, "rgba(207,230,255,.22)", ICE, 1.6, 17, ice, fx="pop"),
            lab((200 + X(11700)) / 2, y - 80, "Ice Age", ice + .2, ICE, 32)]
    fa = T(3, "first farms", -.2)
    els += [ln([(X(11500), 330), (X(11500), y - 6)], fa, GOLD, 2.5, dur=.6), dt(X(11500), y, 8, GOLD, fa),
            lab(X(11500) + 14, 300, "first farms", fa + .2, GOLD, 30, "start"), lab(X(11500) + 14, 334, "c. 11,500 years ago", fa + .3, DIM, 24, "start")]
    pa = 2.0
    els += [poly(PYR(200, 470, 150, 380, 4), "rgba(201,193,238,.08)", LILAC, 2.5, pa, fx="draw", style="claimed", dur=1.0),
            lab(140, 330, "the claimed pyramid", pa + .4, LILAC, 26, "start")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s04():
    """The journal page, five month boxes ticking from October 2023 to March 2024, and the stamp."""
    els = [rect(230, 150, 460, 620, PAPER, "#8a7a66", 2, 6, .2), rect(262, 182, 396, 34, "#3a5a7a", r=3, at=.4),
           {"k": "glyphs", "x": 262, "y": 236, "w": 396, "h": 110, "rows": 4, "cols": 7, "kind": "latin", "c": "#6a5a48", "in": .5},
           poly(PYR(460, 560, 230, 400, 4), "rgba(106,90,160,.08)", "#6a5aa0", 2.5, .7, style="claimed"),
           {"k": "glyphs", "x": 262, "y": 600, "w": 396, "h": 140, "rows": 5, "cols": 7, "kind": "latin", "c": "#6a5a48", "in": .8}]
    a = T(4, "published", -.2)
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    x0, w, g = 800, 112, 22
    b = T(4, "Five months", -.1)
    for k, m in enumerate(months):
        x = x0 + k * (w + g)
        els += [rect(x, 300, w, 80, "rgba(245,236,220,.05)", DIM, 1.6, 8, .5 + .05 * k), lab(x + w / 2, 352, m, .55 + .05 * k, BONE, 28)]
        els += [rect(x + 3, 303, w - 6, 74, "rgba(242,201,142,.22)", "none", 0, 7, b + .32 * k, fx="pop")]
    els += [lab(x0 + 1.5 * w + g, 276, "2023", .6, DIM, 24), lab(x0 + 4.5 * w + 4 * g, 276, "2024", .6, DIM, 24),
            dt(x0 + w / 2, 410, 9, GOLD, a), lab(x0 + w / 2, 452, "published", a + .1, GOLD, 26)]
    c = T(4, "took it back", -.2)
    xm = x0 + 5 * (w + g) + w / 2
    els += [dt(xm, 410, 9, RED, c), lab(xm, 452, "retracted", c + .1, RED, 26),
            ln([(x0 + w / 2, 500), (xm, 500)], b + .2, DIM, 2, dur=1.6), lab((x0 + w / 2 + xm) / 2, 540, "about five months", b + 1.6, DIM, 26),
            {"k": "group", "tr": "rotate(-14 460 470)", "in": round(c, 2), "fx": "pop", "els": [
                rect(250, 420, 420, 104, "rgba(255,138,122,.14)", RED, 6, 12), label(460, 494, "RETRACTED", 0, RED, 58, st="serif")]}]
    return {"base": "dark", "cam": CAM, "els": els}


def s06_add():
    return []


# ================================================================ chapter 1: five terraces on a hill
def s07():
    """Western Java: Jakarta, Bandung and Gunung Padang (6.99 S, 107.06 E)."""
    v = View(103.8, 110.4, -8.3, -5.5, (90, 130, 1600, 660))
    gx, gy = v.p(107.0564, -6.9939)
    jx, jy = v.p(106.85, -6.2)
    bx_, by_ = v.p(107.61, -6.91)
    a = T(7, "It crowns", 0)
    els = [{"k": "map", "land": v.land(), "in": -1},
           gl(gx, gy, 120, a + .2, .55, "lamp"),
           {"k": "pin", "x": gx, "y": gy, "t": "Gunung Padang", "c": GOLD, "a": "end", "lx": -20, "ly": 34, "in": round(a + .3, 2)},
           lab(*v.p(108.25, -7.25), "West Java", T(7, "West Java"), "#c9ad85", 32, st="ital"),
           {"k": "pin", "x": jx, "y": jy, "t": "Jakarta", "c": AMBER, "a": "end", "lx": -18, "in": T(7, "Jakarta")},
           {"k": "pin", "x": bx_, "y": by_, "t": "Bandung", "c": AMBER, "in": round(T(7, "West Java") + .5, 2)},
           lab(*v.p(107.9, -5.85), "Java Sea", 1.0, "#9fd0ff", 30, st="ital"), lab(*v.p(105.4, -7.85), "Indian Ocean", 1.2, "#9fd0ff", 30, st="ital"),
           lab(*v.p(104.5, -5.65), "Sumatra", 1.3, "#c9ad85", 26, st="ital"),
           {"k": "scale", "x": 1380, "y": 760, "w": r1(v.km(50)), "t": "50 km", "in": 1.4}]
    return {"base": "map", "cam": CAM, "els": els}


SUMMIT = dict(x=889, y=620, s=7.6, az=-20, el=.46, spin=0.0)


def summit_parts():
    hill = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 56, "prof": [[-70, 0], [70, 0], [52, 6], [30, 13], [-30, 13], [-52, 6]], "c": "#4f6a3a", "edge": "rgba(255,236,206,.25)"}]
    ters = [ibox(-24 + i * 12, 0, 13, 12, 22 - i * 2, 1.6 * (i + 1)) for i in range(5)]
    stair = [{"t": "line", "p": [[-52 + 2.2 * k, 6.2 + .7 * k, 0], [-52 + 2.2 * k, 6.9 + .7 * k, 0], [-49.8 + 2.2 * k, 6.9 + .7 * k, 0]], "c": GOLD, "w": 2.4} for k in range(10)]
    return hill, ters, stair


def s08():
    """The summit (iso, schematic): five terraces from the lowest and largest (north) to the highest (south), the stair, volcanoes behind."""
    hill, ters, stair = summit_parts()
    base = iso(hill, at=.1, **SUMMIT)
    a = T(8, "Five stone terraces", .1)
    els = [gl(889, 560, 620, -1, .16, "lamp"), base]
    els += [ov(base, [t], a + .45 * k, fx="rise") for k, t in enumerate(ters)]
    sa = T(8, "reached by a stair")
    els += [ov(base, stair, sa, fx="draw", dur=1.2)]
    sx, sy = P3(base, (-44, 9, 0))
    els += [lab(sx - 26, sy + 16, "about 370 steps", sa + .8, GOLD, 30, "end")]
    px, py = P3(base, (24, 21, 2))
    els += [ov(base, [{"t": "person", "x": 24, "y": 21, "z": 3, "h": 1.7}], a + 2.5, fx="rise")]
    t1 = P3(base, (-24, 14.6, 11))
    t5 = P3(base, (24, 21, 7))
    els += [lab(t1[0] - 10, t1[1] + 46, "lowest", a + .5, DIM, 24, "end"), lab(t5[0] + 40, t5[1] - 18, "highest", a + 2.3, DIM, 24, "start")]
    va = T(8, "volcanoes", -.2)
    els += [poly([(120, 640), (380, 300), (430, 306), (720, 640)], "#3b3140", "none", 0, va, op=.7, layer="far"),
            poly([(1080, 640), (1380, 260), (1440, 268), (1740, 640)], "#3b3140", "none", 0, va + .4, op=.7, layer="far")]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [1500, 330, 20], "cam": CAM, "els": els}


def mini_terraces(x, y, w, at, c=TERR, op=None, edge=TERR_E):
    """A small stepped icon of the five terraces, base on y, x the left end."""
    h = w * .09
    out = []
    for k in range(5):
        x0 = x + k * w * .16
        out.append(rect(x0, y - h * (k + 1), w - k * w * .16, h, c, edge, 1.2, 2, at, op=op))
    return out


def s09():
    """1880 to 2000: a Dutch report around 1890, the forgotten years, farmers in 1979, mapping in the 1980s."""
    X = lambda yr: r1(200 + (yr - 1880) / 120 * 1380)
    y = 620
    els = [ln([(200, y), (1580, y)], .2, BONE, 3, dur=1.0)]
    for yr in (1900, 1950, 2000):
        els += [ln([(X(yr), y - 9), (X(yr), y + 9)], .5, BONE, 2, draw=False), lab(X(yr), y + 44, str(yr), .6, DIM, 24)]
    a = .4
    nb = [rect(X(1890) - 34, 470, 68, 86, "#8a6a44", "#e7c99a", 2, 4, a, fx="pop")] + [ln([(X(1890) - 22, 494 + 14 * j), (X(1890) + 22, 494 + 14 * j)], a + .1, "#e7c99a", 2, draw=False) for j in range(4)]
    els += nb + [ln([(X(1890), 560), (X(1890), y - 4)], a, GOLD, 2, dur=.4), dt(X(1890), y, 8, GOLD, a), lab(X(1890), 440, "a Dutch report", a + .3, GOLD, 28)]
    els += mini_terraces(700, 560, 300, .9)
    f = T(9, "largely forgotten", -.2)
    r = random.Random(7)
    for k in range(9):
        els.append(dt(720 + 34 * k + r.uniform(-6, 6), 520 + r.uniform(-24, 24), r.uniform(24, 34), "#26361e", f + .12 * k, fx="pop", op=.92))
    els += [lab(850, 420, "largely forgotten", f + .5, DIM, 26, st="ital"), ln([(X(1914), y), (X(1978), y)], f, "#4f6a3a", 8, dur=1.2, op=.8)]
    fm = T(9, "local farmers", -.1)
    els += [person_(X(1979) - 40 + 26 * k, y - 12, 66, fm + .2 * k) for k in range(3)] + [dt(X(1979), y, 8, GOLD, fm), lab(X(1979), 470, "found again, 1979", fm + .5, GOLD, 28)]
    els += mini_terraces(700, 560, 300, fm + .8, "rgba(185,179,160,.9)") + [gl(850, 520, 160, fm + .8, .35, "lamp")]
    mp = T(9, "archaeologists cleared", -.1)
    px, py = 1290, 210
    for k, (x0, x1, _) in enumerate(TER):
        els.append(rect(px + (x0 - 650) * .42, py + (k % 2) * 6, (x1 - x0) * .42 - 4, 46 - k * 4, "rgba(242,201,142,.12)", GOLD, 1.6, 2, mp + .15 * k, fx="pop"))
    els += [lab(px + 130, py + 92, "mapped, 1980s", mp + .8, GOLD, 26), ln([(X(1985), 330), (X(1985), y - 4)], mp + .5, GOLD, 2, "inferred", .5)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def column_side(x0, y0, L, H, at, fx="pop"):
    """A columnar andesite beam lying on its side (a five-sided prism seen from the front): top face, front face, end face."""
    d = H * .32
    out = [poly([(x0 + d, y0 - d), (x0 + L + d, y0 - d), (x0 + L, y0), (x0, y0)], ANDE_L, ANDE_E, 1.2, at, fx),
           poly([(x0, y0), (x0 + L, y0), (x0 + L, y0 + H), (x0, y0 + H)], ANDE, ANDE_E, 1.2, at, fx)]
    cx, cy, rr = x0 + L + d * .45, y0 + H * .42, H * .62
    out.append(poly(ngon(cx, cy, rr, 5, -90), "#6a665e", ANDE_E, 1.6, at, fx))
    return out


def s10():
    """The ringing stone: a long andesite block on the lowest terrace; tapped, it rings."""
    els = [rect(80, 610, 1620, 120, "#3a3229", "none", 0, 0, -1), ln([(80, 610), (1700, 610)], -1, "rgba(255,226,190,.4)", 2, draw=False)]
    els += column_side(440, 470, 760, 130, .4)
    a = T(10, "strike it", -.4)
    els += [ln([(560, 260), (690, 420)], a, "#e8d6b8", 14, draw=False), dt(700, 432, 20, "#9aa0a8", a), dt(700, 432, 6, "#efe6d2", a)]
    for k, rr in enumerate((70, 130, 190)):
        b = a + .35 + .2 * k
        els += [ln(arc(705, 450, rr, 200, 340), b, GOLD, 3, dur=.5, op=.9 - .2 * k), ln(arc(705, 450, rr, -10, 40), b, GOLD, 3, dur=.4, op=.8 - .2 * k)]
    els += [gl(705, 450, 220, a + .4, .45, "lamp"),
            lab(1020, 330, "the ringing stone", T(10, "a stone that rings"), GOLD, 34), lab(1020, 370, "batu kecapi", T(10, "a stone that rings") + .3, DIM, 26, st="ital")]
    return {"base": "dark", "floor": 640, "cam": CAM, "els": els}


def stone_ends(x0, x1, y0, y1, r, at, step=.03, c=ANDE, edge=ANDE_E, seed=2, jit=3):
    """Rows of column ends (five and six sided), as a wall face seen end-on."""
    rr = random.Random(seed)
    out, k = [], 0
    y = y1 - r
    row = 0
    while y - r >= y0 - 1:
        x = x0 + r + (r if row % 2 else 0)
        while x + r <= x1 + 1:
            n = rr.choice((5, 6, 6))
            out.append(poly(ngon(x + rr.uniform(-jit, jit), y + rr.uniform(-jit, jit), r * rr.uniform(.86, 1.0), n, rr.uniform(0, 60)), c, edge, 1.2, at + step * k, fx="pop"))
            x += 2 * r * .98
            k += 1
        y -= 1.72 * r
        row += 1
    return out


def s11():
    """A terrace edge in section: the retaining wall on its soil, a trench beside it, charcoal under the wall's foot."""
    els = [rect(80, 600, 760, 210, SOIL, "none", 0, 0, -1), rect(840, 330, 860, 480, "#5a4a3a", "none", 0, 0, -1),
           ln([(80, 600), (840, 600)], -1, GRASS_E, 3, draw=False), ln([(860, 330), (1700, 330)], -1, GRASS_E, 3, draw=False),
           rect(80, 640, 760, 170, "rgba(0,0,0,.18)", "none", 0, 0, -1)]
    els += stone_ends(770, 880, 340, 606, 22, .3, .025)
    els += [lab(960, 410, "retaining wall", .9, BONE, 28, "start")]
    a = T(11, "has dug here", -.6)
    els += [poly([(600, 600), (770, 600), (770, 690), (900, 690), (900, 740), (600, 740)], "#1d1712", BLUE, 2.5, a, style="inferred", fx="fill", dur=.8),
            person_(660, 740, 112, a + .4), ln([(690, 670), (730, 690)], a + .6, "#c9ccd2", 4, draw=False), lab(560, 780, "a trench", a + .6, BLUE, 26, "end")]
    c = T(11, "found charcoal", -.1)
    r = random.Random(5)
    for k in range(9):
        els.append(dt(790 + r.uniform(0, 90), 618 + r.uniform(0, 30), r.uniform(4, 7), "#0c0a08", c + .05 * k))
    els += [gl(835, 630, 90, c, .6, "fire"), ln([(780, 632), (590, 560)], c + .3, GOLD, 2, dur=.4), lab(580, 552, "charcoal", c + .4, GOLD, 32, "end")]
    return {"base": "sky", "tod": "night", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def s12():
    """A coin under a floorboard: first the coin, then the floor laid over it."""
    gy = 610
    els = [rect(260, gy, 1240, 180, SOIL_D, "none", 0, 0, -1), ln([(260, gy), (1500, gy)], -1, "rgba(255,226,190,.45)", 2, draw=False)]
    a = .5
    els += [arr([(880, 300), (880, 586)], a, GOLD, 2.5, "claimed", .6, False), oval(880, gy - 8, 30, 9, GOLD, "#fff0c8", 2, at=a + .5, fx="pop"),
            lab(880, 690, "1. the coin", a + .7, GOLD, 30)]
    b = T(12, "the floor was laid", -.2)
    for k, x in enumerate(range(320, 1500, 230)):
        els.append(rect(x, gy - 46, 30, 46, "#5a4632", "#a8875c", 1.2, 2, b + .05 * k, fx="rise"))
    for k in range(10):
        els.append(rect(280 + 120 * k, gy - 68, 116, 22, "#a8875c", "#e7c99a", 1.4, 3, b + .5 + .1 * k, fx="rise"))
    els += [lab(1520, gy - 50, "2. the floor", b + 1.6, BONE, 30, "start"), ln([(880, 520), (880, 470)], b + 1.8, DIM, 2, dur=.3),
            lab(880, 450, "laid after", b + 1.9, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s13():
    """300 BCE to 300 CE: charcoal under terrace 1 (about 117 BCE) and under terraces 2 and 4 (about 50 BCE); three generations build."""
    X = lambda yr: r1(200 + (yr + 300) / 600 * 1380)
    y = 560
    els = [ln([(200, y), (1580, y)], .2, BONE, 3, dur=.9)]
    for yr, t in ((-300, "300 BCE"), (-200, ""), (-100, ""), (0, "1 CE"), (100, ""), (200, ""), (300, "300 CE")):
        els += [ln([(X(yr), y - 8), (X(yr), y + 8)], .5, BONE, 2, draw=False)] + ([lab(X(yr), y + 44, t, .6, DIM, 24)] if t else [])
    a = T(13, "charcoal dates", -.1)
    els += [dt(X(-117), y, 11, GOLD, a), gl(X(-117), y, 60, a, .5), ln([(X(-117), y - 14), (X(-117), 410)], a + .2, GOLD, 2, dur=.3),
            lab(X(-117) - 8, 396, "under terrace 1", a + .3, BONE, 27, "end"), lab(X(-117) - 8, 430, "c. 117 BCE", a + .4, GOLD, 25, "end")]
    b = a + .9
    els += [dt(X(-50), y, 11, GOLD, b), gl(X(-50), y, 60, b, .5), ln([(X(-50), y - 14), (X(-50), 410)], b + .2, GOLD, 2, dur=.3),
            lab(X(-50) + 8, 396, "under terraces 2 and 4", b + .3, BONE, 27, "start"), lab(X(-50) + 8, 430, "c. 50 BCE", b + .4, GOLD, 25, "start")]
    c = T(13, "about two thousand years")
    els += [ln([(X(-117), 650), (X(-117), 662), (X(-50), 662), (X(-50), 650)], c, GOLD, 2.5, dur=.5), lab((X(-117) + X(-50)) / 2, 712, "about 2,000 years ago", c + .3, GOLD, 30)]
    g = T(13, "not in one generation")
    tones = ["#e8d6b8", "#d9c3a0", "#c9ad85"]
    for k in range(3):
        at = g + .7 * k
        els += [rect(1180, 300 - 34 * k, 380, 30, TERR, TERR_E, 1.2, 3, at + .2, fx="rise"), person_(1120 - 0 * k, 330, 92 - 6 * k, at, tones[k])]
    els += [lab(1370, 160, "over several generations", g + .3, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s14():
    """Finds and meaning: pottery, a grinding stone, a stone-lined well; the terraces at dusk, people climbing, a lamp on top."""
    a, b, c = T(14, "Pottery", .0), T(14, "a grinding stone"), T(14, "a stone-lined well")
    els = [rect(110, 520, 780, 12, "#4a3a2c", "none", 0, 3, -1)]
    els += [poly(arc(250, 420, 90, 200, 320) + list(reversed(arc(250, 420, 64, 210, 310))), "#b0623a", "#e7a77a", 2, a, fx="pop"),
            lab(250, 580, "pottery", a + .2, BONE, 27)]
    els += [oval(500, 470, 110, 32, "#7a7468", "#c9c1b3", 2, at=b, fx="pop"), oval(500, 438, 50, 18, "#9a948a", "#e0d8c8", 2, at=b + .2, fx="pop"),
            lab(500, 580, "grinding stone", b + .2, BONE, 27)]
    stones = [dt(760 + 62 * math.cos(math.radians(k * 30)), 450 + 26 * math.sin(math.radians(k * 30)), 15, "#8a8378", c + .03 * k) for k in range(12)]
    els += [oval(760, 450, 50, 18, "#0f1a22", "none", 0, at=c)] + stones + [lab(760, 580, "a well", c + .3, BONE, 27)]
    d = T(14, "it fits")
    els += [rect(930, 160, 760, 590, "#231c26", "rgba(255,236,206,.2)", 2, 18, d - .2, fx="pop"),
            gl(1460, 260, 160, d, .5, "sun"),
            poly([(950, 740), (1080, 600), (1200, 500), (1290, 470), (1560, 452), (1640, 520), (1670, 740)], GRASS, GRASS_E, 2, d + .2)]
    for k in range(5):
        els.append(rect(1290 + 54 * k, 466 - 10 * k, 270 - 54 * k, 10 + 10 * k, TERR, TERR_E, 1, 2, d + .4 + .15 * k, fx="rise"))
    els += [person_(1110 + 40 * k, 640 - 52 * k, 34, d + 1.2 + .3 * k, "#efe0c0") for k in range(3)]
    e = T(14, "honoured their ancestors", -.4)
    els += [gl(1520, 400, 120, e, .8, "fire"), dt(1520, 404, 7, "#ffd27a", e), lab(1310, 220, "a stepped sanctuary", T(14, "stepped sanctuary"), GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s15():
    """The hill in section: columns inside, no far quarry; the terraces built from the hill's own stone."""
    els = hill_section(.1) + terraces(.3, .05, fx=None)
    a = T(15, "Thousands of long", 0)
    r = random.Random(8)
    for x0, x1, y in TER:
        for k in range(int((x1 - x0) / 26)):
            els.append(rect(x0 + 6 + 26 * k, y - 10, 20, 8, "#d9d2bf", "none", 0, 2, a + r.uniform(0, .8), fx="pop"))
    b = T(15, "nobody hauled")
    els += [rect(1540, 600, 140, 90, "none", LILAC, 2.5, 6, b, style="claimed"), lab(1610, 720, "a far quarry?", b + .2, LILAC, 25),
            arr([(1560, 590), (1440, 420), (1300, 330)], b + .3, LILAC, 2.5, "claimed", .9), strk(1480, 520, 1420, 400, b + 1.4)]
    c = T(15, "came out of the hill")
    for k, (p0, p1) in enumerate((((560, 560), (700, 362)), ((760, 520), (900, 346)), ((1340, 520), (1220, 318)))):
        els.append(arr([p0, ((p0[0] + p1[0]) / 2 + 30, (p0[1] + p1[1]) / 2 + 30), p1], c + .3 * k, GOLD, 3.5, "known", .8))
    els += [lab(960, 600, "from the hill itself", c + .8, GOLD, 32)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [1460, 220, 18], "cam": CAM, "els": els}


# ================================================================ chapter 2: stones that cut themselves
def pentagon_yz(r):
    """A five-sided section, flat side down, as (u, v) points for an iso 'ext' (u across, v up)."""
    out = []
    for k in range(5):
        th = math.radians(90 + 72 * k)
        out.append([round(r * math.cos(th), 3), round(r * (.809 + math.sin(th)), 3)])
    return out


def s16():
    """One column, about 1.5 m long, on the grass beside a person: its five-sided end traced in gold; no chisel made it."""
    base = iso([{"t": "slab", "x0": -1.6, "x1": 1.8, "z0": -1.2, "z1": 1.2, "y": 0, "c": "#33452a"}], 760, 590, 150, -32, el=.38, at=-1)
    prof = pentagon_yz(.2)
    col = {"t": "ext", "axis": "z", "x": 0, "y": 0, "z": 0, "at": 0, "d": .75, "prof": prof, "c": ANDE, "edge": "rgba(255,236,206,.4)"}
    a = .5
    els = [gl(800, 560, 520, -1, .16, "lamp"), base, ov(base, [col], a, fx="rise"),
           ov(base, [{"t": "person", "x": 1.4, "y": 0, "z": .7, "h": 1.7}], a + .4, fx="rise")]
    b = T(16, "five or six sided", -.2)
    ring = [[.75, v, u] for u, v in prof] + [[.75, prof[0][1], prof[0][0]]]
    els += [ov(base, [{"t": "line", "p": ring, "c": GOLD, "w": 4}], b, fx="draw", dur=.9)]
    ex, ey = P3(base, (.75, .2, 0))
    els += [lab(ex + 30, ey - 40, "five sides", b + .6, GOLD, 30, "start")]
    c = T(16, "look cut", -.2)
    ch = [rect(1290, 300, 150, 24, "#c9ccd2", "#efe6d2", 1.5, 3, c, fx="pop"), poly([(1440, 300), (1478, 312), (1440, 324)], "#e0e4ea", "none", 0, c, fx="pop"),
          rect(1190, 302, 100, 20, "#8a6a44", "#c8a070", 1.5, 4, c, fx="pop"), lab(1340, 270, "a mason's chisel?", c + .2, DIM, 26)]
    els += ch + [strk(1180, 350, 1500, 260, T(16, "Nobody cut"))]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def hexnet(cx, cy, r, cols, rows, at, c="#e8b87a", w=2.5, step=.03, clip=None, squash=1.0, dur=.3):
    out, k = [], 0
    for j in range(rows):
        for i in range(cols):
            x = cx + (i - (cols - 1) / 2) * r * math.sqrt(3) + (r * math.sqrt(3) / 2 if j % 2 else 0)
            y = cy + (j - (rows - 1) / 2) * r * 1.5 * squash
            if clip and not clip(x, y):
                continue
            pts = [(x + r * math.cos(math.radians(30 + 60 * q)), y + r * math.sin(math.radians(30 + 60 * q)) * squash) for q in range(7)]
            out.append(ln(pts, at + step * k, c, w, dur=dur))
            k += 1
    return out


def s17():
    """Lava cooling: it darkens from its top and bottom, cracks grow inward into columns; seen from above the cracks meet in threes;
    a honeycomb; the Giant's Causeway."""
    x0, x1, y0, y1 = 130, 860, 230, 640
    els = [rect(x0, y0, x1 - x0, y1 - y0, LAVA, "#ff9a6a", 2, 10, .2), gl((x0 + x1) / 2, (y0 + y1) / 2, 420, .2, .8, "red"),
           lab((x0 + x1) / 2, y0 - 22, "a thick mass of lava", .5, "#ff9a6a", 28)]
    a = T(17, "When a thick mass", .6)
    els += [wipe(x0, y0, x1 - x0, 90, a, "#3a3733", .92, 1.2, 10), wipe(x0, y1 - 90, x1 - x0, 90, a + .3, "#3a3733", .92, 1.2, 10),
            wipe(x0, y0, x1 - x0, y1 - y0, a + 1.6, "#3a3733", .85, 1.6, 10)]
    els += [arr([(300, y0 + 6), (300, y0 - 54)], a, BLUE, 2.5, dur=.4, curve=False), arr([(690, y1 - 6), (690, y1 + 54)], a + .2, BLUE, 2.5, dur=.4, curve=False),
            lab(318, y0 - 60, "cools", a + .3, BLUE, 25, "start")]
    b = T(17, "cracks run through it", -.2)
    r = random.Random(3)
    for k in range(13):
        x = x0 + 30 + k * 54 + r.uniform(-6, 6)
        els += [ln([(x, y0 + 4), (x + r.uniform(-6, 6), (y0 + y1) / 2 + r.uniform(-30, 10))], b + .06 * k, "#1b1815", 4, dur=.8),
                ln([(x + r.uniform(-14, 14), y1 - 4), (x + r.uniform(-8, 8), (y0 + y1) / 2 + r.uniform(-10, 30))], b + .3 + .06 * k, "#1b1815", 4, dur=.8)]
    els += [lab((x0 + x1) / 2, y1 + 44, "columns", b + 1.6, BONE, 30)]
    c = T(17, "The cracks tend", -.2)
    clip = lambda x, y: 1020 < x < 1440 and 210 < y < 500
    els += [rect(1000, 190, 460, 330, "#3a3733", "rgba(255,236,206,.3)", 2, 12, c), lab(1230, 170, "seen from above", c + .1, DIM, 25)]
    els += hexnet(1230, 355, 42, 7, 5, c + .3, "#1b1815", 4, .025, clip)
    hc = T(17, "honeycomb", -.2)
    els += hexnet(1580, 340, 26, 3, 3, hc, GOLD, 2.5, .03) + [lab(1580, 450, "honeycomb", hc + .3, GOLD, 25)]
    g = T(17, "The same process", .1)
    sea = [rect(980, 700, 720, 100, "#1d3a4a", "none", 0, 0, g), ln([(980, 700), (1700, 700)], g, "#9fd0ff", 2, draw=False, op=.7)]
    tops = []
    rr = random.Random(9)
    for k in range(12):
        x = 1010 + 52 * k
        h = 150 - abs(k - 4) * 14 + rr.uniform(-8, 8)
        tops += [rect(x, 700 - h, 46, h, ANDE, ANDE_E, 1, 2, g + .05 * k, fx="rise"), poly(ngon(x + 23, 700 - h, 23, 6), ANDE_L, ANDE_E, 1, g + .05 * k, fx="rise", op=None)]
    els += sea + tops + [lab(1330, 532, "Giant's Causeway", g + .6, GOLD, 30), lab(1330, 566, "Northern Ireland", g + .7, DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s18():
    """Cornflour and water drying under a lamp: the surface cracks, and a cut shows tiny columns."""
    els = [rect(80, 600, 1620, 40, "#6b5038", "#a8875c", 1.5, 2, -1), rect(80, 640, 1620, 200, "#3a2a1d", "none", 0, 0, -1)]
    lamp = [rect(1140, 586, 140, 16, "#2a2622", "#9a948a", 1.5, 4, .2), ln([(1210, 586), (1150, 360), (980, 270)], .2, "#9a948a", 6, draw=False),
            poly([(930, 250), (1050, 250), (1020, 300), (960, 300)], "#2a2622", "#c9c1b3", 1.5, .2), gl(800, 440, 420, .5, .5, "lamp")]
    els += lamp
    a = T(18, "Mix cornflour", -.1)
    els += [poly([(420, 520), (1000, 520), (980, 600), (440, 600)], "rgba(207,230,255,.10)", ICE, 2, a, fx="pop"),
            oval(710, 530, 280, 22, "#efe9dc", "none", 0, at=a + .3, fx="pop"), lab(710, 470, "cornflour and water", a + .4, BONE, 28)]
    b = T(18, "leave it to dry")
    els += [lab(220, 300, "day 1", b, AMBER, 28), lab(220, 346, "day 2", b + .6, AMBER, 28), lab(220, 392, "day 3", b + 1.2, AMBER, 28)]
    c = T(18, "it cracks into")
    clip = lambda x, y: ((x - 710) / 272) ** 2 + ((y - 530) / 20) ** 2 < 1
    els += hexnet(710, 530, 26, 21, 5, c, "#7a6a50", 2, .01, clip, squash=.14, dur=.25)
    d = c + 1.0
    els += [rect(1260, 300, 400, 200, "#2a2622", "rgba(255,236,206,.3)", 2, 10, d, fx="pop"), rect(1290, 400, 340, 60, "#efe9dc", "none", 0, 0, d + .2)]
    els += [ln([(1296 + 9 * k, 402), (1296 + 9 * k + (k % 3 - 1), 458)], d + .3 + .01 * k, "#9a8e78", 1.6, dur=.3) for k in range(37)]
    els += [lab(1460, 282, "cut open", d + .2, DIM, 25), lab(1460, 540, "tiny columns, a few mm wide", d + .6, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s19():
    """Columns grow at right angles to the cooling surface: upright in a flow, leaning in a tilted body, lying on their sides in a wall."""
    a = T(19, "The cracks grow", .2)
    cards = [(110, "upright"), (640, "leaning"), (1170, "on their sides")]
    ats = [a, T(19, "lean", -.2), T(19, "lie on their sides", -.2)]
    els = []
    for (x, t), at in zip(cards, ats):
        els += [rect(x, 180, 500, 540, "rgba(245,236,220,.04)", "rgba(255,236,206,.22)", 2, 16, at - .1, fx="pop"), lab(x + 250, 236, t, at + .1, GOLD, 32)]
    at = ats[0]
    els += [rect(160, 380, 400, 170, "#3a3733", ANDE_E, 1.5, 4, at)]
    els += [ln([(180 + 30 * k, 384), (180 + 30 * k, 546)], at + .3 + .03 * k, "#151311", 3, dur=.4) for k in range(13)]
    els += [arr([(360, 376), (360, 316)], at + .2, BLUE, 3, dur=.4, curve=False), arr([(360, 554), (360, 614)], at + .2, BLUE, 3, dur=.4, curve=False)]
    at = ats[1]
    ang = math.radians(-28)
    cx, cy = 890, 470
    rot = lambda u, v: (cx + u * math.cos(ang) - v * math.sin(ang), cy + u * math.sin(ang) + v * math.cos(ang))
    els += [poly([rot(-190, -70), rot(190, -70), rot(190, 70), rot(-190, 70)], "#3a3733", ANDE_E, 1.5, at)]
    els += [ln([rot(-170 + 28 * k, -66), rot(-170 + 28 * k, 66)], at + .3 + .03 * k, "#151311", 3, dur=.4) for k in range(13)]
    els += [arr([rot(0, -74), rot(0, -134)], at + .2, BLUE, 3, dur=.4, curve=False), arr([rot(0, 74), rot(0, 134)], at + .2, BLUE, 3, dur=.4, curve=False)]
    at = ats[2]
    els += [rect(1350, 290, 140, 400, "#3a3733", ANDE_E, 1.5, 4, at)]
    els += [ln([(1354, 306 + 28 * k), (1486, 306 + 28 * k)], at + .3 + .03 * k, "#151311", 3, dur=.4) for k in range(14)]
    els += [arr([(1344, 490), (1284, 490)], at + .2, BLUE, 3, dur=.4, curve=False), arr([(1496, 490), (1556, 490)], at + .2, BLUE, 3, dur=.4, curve=False)]
    els += [dt(700, 768, 7, BLUE, ats[0] + 1.0), lab(716, 776, "arrows: the cooling surface", ats[0] + 1.0, BLUE, 25, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s20():
    """Paul Bunyan's Woodpile, Utah: a slope of sideways columns whose ends look like stacked logs (schematic)."""
    els = [poly([(80, 760), (300, 640), (520, 560), (800, 520), (1100, 540), (1400, 600), (1700, 700), (1700, 1010), (80, 1010)], "#5a4636", "#c9a070", 2, -1)]
    r = random.Random(4)
    k = 0
    for row in range(6):
        y = 640 - row * 52
        n = 9 - abs(row - 2)
        x0 = 870 - n * 30
        for i in range(n):
            x = x0 + i * 60 + (30 if row % 2 else 0)
            els.append(poly(ngon(x + r.uniform(-3, 3), y + r.uniform(-3, 3), 29, r.choice((5, 6, 6)), r.uniform(0, 60)), ANDE, ANDE_E, 1.4, .3 + .03 * k, fx="pop"))
            k += 1
    a = T(20, "Paul Bunyan's")
    els += [lab(880, 250, "Paul Bunyan's Woodpile", a, GOLD, 36), lab(880, 290, "Utah", a + .2, DIM, 27)]
    b = T(20, "No lumberjack", -.2)
    axe = [ln([(1380, 640), (1500, 330)], b, LILAC, 4, "claimed", .5), poly([(1470, 300), (1580, 330), (1560, 410), (1500, 380)], "rgba(201,193,238,.08)", LILAC, 3, b + .2, style="claimed")]
    els += axe + [strk(1360, 420, 1620, 340, T(20, "required", -.1))]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [300, 300, 22], "cam": CAM, "els": els}


def s21():
    """An ancient volcano in three stages: lava in its throat; columns grown from the throat's walls; the cone worn away, the neck left
    standing as a hill, terraces on top (after Bronto and Langi)."""
    gy = 700
    els = [rect(80, gy, 1620, 120, "#3a3028", "none", 0, 0, -1), ln([(80, gy), (1700, gy)], -1, "rgba(255,226,190,.35)", 2, draw=False)]
    cone = lambda cx, at, op=None, style="known", fill="#4a3c34", c="#8a7462": poly([(cx - 230, gy), (cx - 26, 270), (cx + 26, 270), (cx + 230, gy)], fill, c, 2, at, op=op, style=style)
    a = .3
    els += [cone(330, a), rect(312, 272, 36, gy - 272, LAVA, "none", 0, 0, a + .3), gl(330, 420, 140, a + .3, .7, "red"), lab(330, 200, "an ancient volcano", a + .5, BONE, 28)]
    els += [arr([(590, 470), (660, 470)], a + 1.0, DIM, 3, dur=.4, curve=False)]
    b = T(21, "lava that cooled")
    els += [cone(889, b, .55), rect(860, 272, 58, gy - 272, "#3a3733", ANDE_E, 1.4, 0, b + .2)]
    els += [ln([(862, 280 + 26 * k), (916, 280 + 26 * k)], b + .5 + .03 * k, "#151311", 3, dur=.3) for k in range(16)]
    els += [lab(889, 200, "lava cools in its throat", b + .3, BONE, 28), arr([(1150, 470), (1220, 470)], b + 1.2, DIM, 3, dur=.4, curve=False)]
    c = T(21, "its columns formed", -.2)
    els += [cone(1450, c, None, "inferred", "none", DIM), lab(1600, 330, "worn away", c + .4, DIM, 24, "start"),
            poly([(1380, gy), (1400, 420), (1500, 420), (1520, gy)], "#3a3733", ANDE_E, 1.6, c + .5, fx="rise")]
    els += [ln([(1402, 440 + 26 * k), (1498, 440 + 26 * k)], c + .8 + .03 * k, "#151311", 3, dur=.3) for k in range(10)]
    els += [rect(1404 + 18 * k, 410 - 6 * k, 92 - 18 * k, 6 + 6 * k, TERR, TERR_E, 1, 1, c + 1.4 + .1 * k, fx="rise") for k in range(5)]
    els += [lab(1450, 200, "the neck remains", c + .3, GOLD, 28), lab(889, 760, "columns formed in place", T(21, "formed right where"), GOLD, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s22():
    """Nature made the bricks (a natural heap of loose columns); people stacked a terrace wall; the question is who, and when."""
    gy = 640
    els = [rect(80, gy, 1620, 160, "#33281f", "none", 0, 0, -1), ln([(80, gy), (1700, gy)], -1, "rgba(255,226,190,.35)", 2, draw=False)]
    r = random.Random(11)
    a = .4
    for k in range(16):
        L, H = r.uniform(120, 190), r.uniform(30, 40)
        cx, cy = 450 + r.uniform(-230, 230), gy - 20 - r.uniform(0, 150) * (1 - abs(k - 8) / 12)
        ang = math.radians(r.uniform(-35, 35))
        pts = [(cx + u * math.cos(ang) - v * math.sin(ang), cy + u * math.sin(ang) + v * math.cos(ang)) for u, v in ((-L / 2, -H / 2), (L / 2, -H / 2), (L / 2, H / 2), (-L / 2, H / 2))]
        els.append(poly(pts, ANDE if k % 2 else ANDE_L, ANDE_E, 1.2, a + .04 * k, fx="pop"))
    els += [lab(450, 720, "made by nature", a + .8, BONE, 28)]
    b = T(22, "the terraces show", -.2)
    els += stone_ends(1060, 1640, 420, gy, 26, b, .02)
    els += [rect(1050, 400, 600, 12, TERR, TERR_E, 1, 2, b + .8), lab(1350, 720, "stacked by people", b + .6, BONE, 28)]
    c = T(22, "shapes alone", -.2)
    els += [gl(889, 470, 200, c, .45, "lamp"), lab(889, 520, "?", c, GOLD, 150, st="big", fx="pop", dur=.8)]
    d = T(22, "who stacked them", -.2)
    clock = [dict(k="circle", x=889, y=250, r=46, fill="rgba(18,13,10,.8)", c=GOLD, w=3, **{"in": round(d, 2), "fx": "pop"}),
             ln([(889, 250), (889, 220)], d + .2, GOLD, 4, draw=False), ln([(889, 250), (912, 262)], d + .2, GOLD, 4, draw=False)]
    els += clock + [lab(889, 350, "how much, and when?", d + .4, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================ chapter 3: a pyramid in the scans
def s23():
    """The hill in section at dusk, the team on its terraces: a radar cart, a line of electrodes, a drilling rig; a trace in the sky."""
    els = hill_section(-1, joints=True, seed=5) + terraces(-1, 0, fx=None)
    a = .4
    els += [person_(674, 372, 28, a), person_(940, 354, 28, a + .2), person_(1196, 326, 28, a + .4)]
    b = T(23, "every tool", -.3)
    radar = [rect(690, 352, 44, 16, "#c9c1b3", "#efe6d2", 1, 3, b, fx="pop"), dt(698, 370, 5, "#2a2622", b), dt(726, 370, 5, "#2a2622", b)]
    elec = [ln([(870 + 25 * k, 346), (870 + 25 * k, 362)], b + .4 + .04 * k, "#e8d6b8", 3, draw=False) for k in range(9)] + \
           [ln([(870, 346), (1070, 342)], b + .7, "#e8b87a", 1.6, dur=.5)]
    rig = [ln([(1214, 326), (1234, 250), (1254, 326)], b + .8, "#c9ccd2", 3, dur=.4), ln([(1234, 250), (1234, 326)], b + 1.0, "#c9ccd2", 3, draw=False)]
    r = random.Random(2)
    trace = [(260 + 18 * k, 200 + (r.uniform(-22, 22) if 30 < k < 46 else r.uniform(-5, 5))) for k in range(70)]
    els += radar + elec + rig + [ln(trace, b + 1.0, BLUE, 2, dur=1.6, op=.7), lab(1540, 180, "from 2011", .6, GOLD, 30)]
    a2 = T(23, "joined by geophysicists", -.2)
    els += [person_(1040 + 26 * k, 344, 26, a2 + .25 * k, "#efe0c0") for k in range(3)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [180, 260, 18], "cam": CAM, "els": els}


def s24_add():
    a = T(24, "Radar sends", .3)
    b = T(24, "echoes", -.3)
    els = [{"k": "fan", "x": 712, "y": 372, "r": 250, "a0": 58, "a1": 122, "c": BLUE, "in": a, "fx": "fade"},
           ln([(560, 520), (650, 506), (760, 512), (880, 498)], a + .4, BLUE, 2.5, "inferred", .6, curve=True)]
    els += [ln(arc(712, 510, rr, 235, 305, 10), b + .2 * k, ICE, 2.5, dur=.4) for k, rr in enumerate((40, 80, 120))]
    els += [lab(800, 300, "radar", a + .2, BLUE, 28, "start")]
    c = T(24, "like a bat", -.2)
    bat = poly([(470, 250), (500, 236), (520, 246), (540, 236), (570, 250), (548, 254), (520, 266), (492, 254)], "#e8d6b8", "none", 0, c, fx="pop")
    els += [bat] + [ln(arc(574, 250, rr, -40, 40, 8), c + .3 + .15 * k, ICE, 2.2, dur=.3) for k, rr in enumerate((24, 44, 64))]
    return els


def s25_add():
    a = T(25, "Electric current", .2)
    els = [ln(arc(970, 350, rr, 15, 165, 18), a + .15 * k, GOLD, 2, dur=.6, op=.75) for k, rr in enumerate((30, 60, 92))]
    b = T(25, "wet clay", -.2)
    els += [poly(ellipse(912, 470, 80, 34)[:-1], "rgba(159,208,255,.35)", BLUE, 2, b, fx="pop", curve=True), lab(870, 540, "wet clay: flows", b + .2, BLUE, 26, "end")]
    c = T(25, "barely through", -.1)
    els += [poly(ellipse(1050, 470, 74, 36)[:-1], "rgba(240,140,80,.35)", AMBER, 2, c, fx="pop", curve=True), lab(1100, 552, "dry rock or a void: resists", c + .2, AMBER, 26, "start")]
    return els


DRILLS = [(700, 20), (790, 16), (880, 28), (960, 24), (1040, 18), (1130, 22), (1230, 36)]          # (x, depth in m) on the hill section


def s26_add():
    top = hill_top()
    a = T(26, "seven drills", -.2)
    els = []
    for k, (x, dm) in enumerate(DRILLS):
        y0 = y_at(x, top)
        els.append(ln([(x, y0), (x, y0 + dm * 4.1)], a + .25 * k, "#e8e2d6", 3.5, dur=.5))
    x, dm = DRILLS[-1]
    y0 = y_at(x, top)
    els += [dimline(x + 34, y0, x + 34, y0 + dm * 4.1, "36 m", a + 2.0, GOLD, lx=40, ly=8)]
    b = T(26, "long cores", -.1)
    els += [{"k": "lib", "k2": "core", "x": 1560, "y": 560, "w": 46, "h": 280, "grooves": 7, "in": b, "fx": "rise"}, lab(1560, 248, "a core", b + .3, BONE, 28)]
    c = T(26, "Then they matched", .1)
    for k, (yc, xs) in enumerate(((330, 980), (420, 1090), (500, 1200))):
        els.append(ln([(1534, yc), (xs, y_at(xs, top) + (yc - 260) * .32)], c + .3 * k, GOLD, 2, "inferred", .6))
    els += [lab(1380, 300, "matched", c + .9, GOLD, 26)]
    return els


# the summit section of the 2023 paper's four units (15 units a metre; schematic, after its fig. 14)
SUM = [(80, 660), (380, 470), (560, 262), (700, 258), (860, 252), (1000, 248), (1140, 246), (1280, 244), (1460, 360), (1700, 560)]


def off(pts, d):
    return [(x, y + d) for x, y in pts]


def band(top, d0, d1, fill, at, edge=None, style="claimed", w=2.5):
    up = off(top, d0)
    dn = list(reversed(off(top, d1)))
    out = [poly(up + dn, fill, "none", 0, at, dur=.8)]
    if edge:
        out.append(ln(off(top, d1), at, edge, w, style, .9))
    return out


def summit_section(at=-1, claimed=True):
    """The summit cut open: Unit 1 (0 to 2 m), Unit 2 (2 to 6 m), Unit 3 (6 to 22 m), Unit 4 below; boundaries dotted when claimed."""
    st = "claimed" if claimed else "inferred"
    e = LILAC if claimed else "rgba(255,236,206,.35)"
    out = [poly(SUM + [(1700, 1010), (80, 1010)], "#3a3836", "none", 0, at)]
    out += band(SUM, 90, 330, "#5f4c39", at, e if claimed else None, st)
    out += band(SUM, 30, 90, "#7a6a58", at, e if claimed else None, st)
    out += band(SUM, 0, 30, "#8c8a7c", at, e if claimed else None, st)
    out += [ln(SUM, at, GRASS_E, 3, draw=False)]
    return out


def s27():
    """The four units of the 2023 paper, each as it is named: terraces on top, columns laid flat with soil they read as mortar,
    a thick layer of rock and soil, a lava core they suggest was sculpted (all their reading: dotted)."""
    els = [poly(SUM + [(1700, 1010), (80, 1010)], "#33302d", "none", 0, -1), ln(SUM, -1, GRASS_E, 3, draw=False)]
    els += [rect(560 + 150 * k, 250 - 4 * k - 12, 140, 12, TERR, TERR_E, 1, 2, -1) for k in range(5)]
    a = T(27, "On top", -.1)
    b = T(27, "Below, columns", -.1)
    c = T(27, "Deeper, a thick", -.1)
    d = T(27, "And at the core", -.1)
    els += band(SUM, 330, 560, "#2e2c2a", d, LILAC)
    els += band(SUM, 90, 330, "#5f4c39", c, LILAC)
    els += band(SUM, 30, 90, "#7a6a58", b, LILAC)
    els += band(SUM, 0, 30, "#8c8a7c", a, LILAC)
    # Unit 2: column ends lying flat, thin soil lines between the rows
    r = random.Random(6)
    k = 0
    for row in range(2):
        for x in range(600, 1270, 30):
            y = y_at(x, SUM) + 46 + 26 * row
            els.append(poly(ngon(x + r.uniform(-2, 2), y, 12, 6, r.uniform(0, 30)), "#4f4b45", "#9a948a", 1, b + .4 + .008 * k, fx="pop"))
            k += 1
    els += [lab(1180, y_at(1180, SUM) + 66, "mortar?", b + 1.2, LILAC, 25, "start")]
    # Unit 4: the lava core, outlined as they suggest (sculpted?)
    core = [(420, 900), (520, 700), (640, 640), (900, 610), (1160, 630), (1300, 690), (1420, 900)]
    els += [poly(core + [(1420, 1010), (420, 1010)], "rgba(70,66,62,.9)", LILAC, 3, d + .4, style="claimed"), lab(920, 700, "sculpted?", d + .9, LILAC, 28)]
    legend = [("Unit 1: the terraces", "#8c8a7c", a), ("Unit 2: columns laid flat", "#7a6a58", b), ("Unit 3: rock and soil", "#5f4c39", c), ("Unit 4: a lava core", "#2e2c2a", d)]
    for k, (t, col, at) in enumerate(legend):
        y = 150 + 44 * k
        els += [rect(100, y - 20, 30, 24, col, LILAC, 1.6, 4, at, fx="pop", style="claimed"), lab(144, y, t, at + .1, BONE, 26, "start")]
    els += [lab(1690, 790, "the team's reading, schematic", .8, DIM, 22, "end")]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": False, "cam": CAM, "els": els}


ANOM = (800, 420)


def s28_add():
    a = T(28, "In the scans", .3)
    x, y = ANOM
    return [poly(ellipse(x, y, 92, 44)[:-1], "rgba(240,140,80,.32)", AMBER, 2.5, a, fx="pop", curve=True),
            poly(ellipse(x + 26, y + 10, 80, 40)[:-1], "rgba(159,208,255,.16)", BLUE, 2.5, a + .9, fx="pop", curve=True, style="inferred"),
            ln([(x - 60, y - 38), (690, 200)], a + .3, AMBER, 2, dur=.4), lab(690, 186, "current barely flows", a + .4, AMBER, 26, "end"),
            ln([(x + 60, y - 30), (980, 200)], a + 1.2, BLUE, 2, dur=.4), lab(980, 186, "vibrations slow", a + 1.3, BLUE, 26, "start")]


def s29():
    """One borehole, 14 m deep (38 units a metre): drilling water poured in vanished between 8 and 14 m: 32 cubes of 1,000 litres."""
    gy, px = 200, 38
    els = [rect(80, gy, 820, 620, "#3a3632", "none", 0, 0, -1), ln([(80, gy), (900, gy)], -1, GRASS_E, 3, draw=False)]
    r = random.Random(12)
    els += [ln([(100 + 40 * k, gy + 10), (100 + 40 * k + r.uniform(-10, 10), 820)], -1, "#26231f", 3, draw=False, op=.9) for k in range(20)]
    els += [rect(486, gy, 28, 14 * px, "#0f0d0b", "#9a948a", 1.5, 0, .3)]
    for m in (0, 8, 14):
        y = gy + m * px
        els += [ln([(516, y), (546, y)], .5, BONE, 2, draw=False), lab(556, y + 9, "%d m" % m, .5, DIM, 25, "start")]
    a = T(29, "drilling water", -.6)
    els += [ln([(500, gy - 60), (500, gy + 14 * px - 4)], a, BLUE, 8, dur=1.4), arr([(500, 120), (500, gy - 10)], a - .4, BLUE, 3, dur=.4, curve=False)]
    b = T(29, "simply vanished", -.4)
    els += [poly(ellipse(500, gy + 11 * px, 150, 128)[:-1], "rgba(159,208,255,.22)", BLUE, 2, b, fx="pop", curve=True, style="inferred"),
            gl(500, gy + 11 * px, 170, b, .35, "blue"), lab(700, gy + 11 * px + 10, "lost here", b + .4, BLUE, 28, "start")]
    s, g = 64, 10
    x0, y0 = 1000, 300
    c0 = T(29, "thirty-two thousand", -.3)
    for k in range(32):
        cx, cy = x0 + (k % 8) * (s + g), y0 + (k // 8) * (s + g)
        els.append(rect(cx, cy, s, s, "rgba(95,168,201,.75)", ICE, 1.5, 6, c0 + .02 * k, fx="pop"))
    for k in range(32):
        cx, cy = x0 + (k % 8) * (s + g), y0 + (k // 8) * (s + g)
        els.append(rect(cx, cy, s, s, "#17120e", BLUE, 1.6, 6, b + .3 + .09 * k, op=.92, style="inferred"))
    els += [lab(x0 + 4 * (s + g) - g / 2, 262, "32,000 litres", c0 + .2, GOLD, 34), lab(x0 + 4 * (s + g) - g / 2, 640, "each cube: 1,000 litres", c0 + .6, DIM, 25)]
    return {"base": "dark", "cam": CAM, "els": els}


def s30_add():
    a = T(30, "points to a hollow", -.1)
    x, y = ANOM
    return [rect(x - 70, y - 36, 150, 80, "rgba(201,193,238,.10)", LILAC, 3, 4, a, fx="pop", style="claimed"), lab(x + 5, y + 92, "a chamber?", a + .3, LILAC, 30)]


def s31():
    """Their argument: columns lying in neat courses (Unit 2, schematic); one block weighed against four adults: up to 300 kg."""
    els = stone_ends(140, 660, 300, 650, 30, .3, .015)
    els += [ln([(140, 650 - 52 * k), (660, 650 - 52 * k)], .8, "#8a7458", 2, draw=False, op=.7) for k in range(1, 7)]
    els += [lab(400, 250, "neatly arranged, shaped", T(31, "neatly arranged"), GOLD, 28)]
    a = T(31, "massive", -.2)

    def blk(x, y, at):
        return column_side(x - 70, y - 44, 130, 40, at)

    def folk(x, y, at):
        return [person_(x - 54 + 36 * k, y, 58, at + .1 * k) for k in range(4)]
    els += balance(1180, 330, 560, 0, 720, a, blk, folk)
    els += [lab(1180, 230, "up to 300 kg", T(31, "three hundred"), GOLD, 36), lab(1460, 590, "about 4 adults", T(31, "three hundred") + .5, DIM, 25)]
    return {"base": "dark", "cam": CAM, "els": els}


def s32():
    """Twelve soil samples (gold) at their depths: a trench and two cores (0 to 12 m); the oldest, 7.5 m down: about 25,000 BCE."""
    y0, px = 190, 46.5
    els = [ln([(250, y0), (250, y0 + 12 * px)], .2, BONE, 2, dur=.6)]
    for m in range(0, 13, 2):
        els += [ln([(240, y0 + m * px), (260, y0 + m * px)], .3, BONE, 2, draw=False), lab(232, y0 + m * px + 8, "%d m" % m, .3, DIM, 24, "end")]
    els += [lab(250, 160, "depth", .3, DIM, 24)]
    cols = [(500, 3.8, "a trench"), (780, 12, "core 1"), (1060, 12, "core 2")]
    for x, d, t in cols:
        els += [rect(x - 26, y0, 52, d * px, "#5f4c39", "rgba(255,236,206,.35)", 1.5, 4, .4, fx="fill", dur=.8), lab(x, y0 - 22, t, .5, BONE, 27)]
    samples = [(500, .55), (500, .82), (500, 1.21), (500, 1.3), (500, 1.5), (500, 3.5), (780, 2.95), (780, 5.0), (780, 11.15), (1060, 3.9), (1060, 7.5), (1060, 11.3)]
    a = T(32, "twelve samples", -.1)
    for k, (x, m) in enumerate(samples):
        els.append(dt(x + (8 if k % 2 else -8) * (x == 500), y0 + m * px, 8, GOLD, a + .12 * k))
    b = T(32, "The oldest", -.1)
    ox, oy = 1060, y0 + 7.5 * px
    els += [gl(ox, oy, 80, b, .8), ln([(ox + 12, oy), (1180, oy)], b + .3, GOLD, 2, dur=.4)]
    els += chip(1186, oy, "c. 25,000 BCE", GOLD, T(32, "twenty-five thousand", -.2), 30, "start")
    els += [lab(1186, oy + 54, "7.5 m down", b + .5, DIM, 25, "start"), dt(1350, 230, 8, GOLD, a), lab(1366, 238, "a dated soil sample", a + .1, GOLD, 25, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s33():
    """The team's reading on a time axis (26,000 BCE to today): built about 25,000 to 14,000 BCE; buried about 7,900 to 6,100 BCE; terraces
    2,000 to 1,100 BCE. All dotted: their reading."""
    X = lambda yr: r1(180 + (yr + 26000) / 28026 * 1420)
    y = 560
    els = [ln([(180, y), (1600, y)], .2, BONE, 3, dur=1.0), lab(889, 220, "the team's reading", .4, LILAC, 30)]
    for yr, t in ((-25000, "25,000 BCE"), (-20000, "20,000"), (-15000, "15,000"), (-10000, "10,000"), (-5000, "5,000"), (2026, "today")):
        els += [ln([(X(yr), y - 8), (X(yr), y + 8)], .5, BONE, 2, draw=False), lab(X(yr), y + 44, t, .6, DIM, 24)]
    rows = [(-25000, -14000, "built?", T(33, "was built between", -.1)), (-7900, -6100, "buried?", T(33, "buried between", -.1)), (-2000, -1100, "terraces", T(33, "crowned with terraces", -.1))]
    for x0, x1, t, at in rows:
        els += [rect(X(x0), y - 74, X(x1) - X(x0), 26, "rgba(201,193,238,.22)", LILAC, 2.5, 10, at, fx="pop", style="claimed"), lab((X(x0) + X(x1)) / 2, y - 96, t, at + .2, LILAC, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


SUNDA = [(95.0, 6.0), (102.0, 8.5), (108.5, 7.0), (117.0, 6.5), (119.5, 0.0), (117.5, -8.6), (106.0, -8.4), (99.0, -3.5), (94.5, 2.0)]    # the drowned-coasts Short's outline
SEA_V = View(90, 132, -11, 9, (90, 130, 1600, 660))


def s34():
    """South-east Asia: at the Ice Age lows the sea stood up to about 120 m lower and the Sunda Shelf joined Java to Asia (after Voris 2000)."""
    v = SEA_V
    a = T(34, "In that era", .2)
    els = [{"k": "map", "land": v.land(), "in": -1},
           poly([v.p(lo, la) for lo, la in SUNDA], "rgba(232,184,122,.28)", AMBER, 2.5, a + .6, style="inferred", curve=True, dur=1.4),
           lab(*v.p(107.5, 2.5), "sea up to 120 m lower", a + 1.2, AMBER, 30, st="ital")]
    for t, lo, la in (("Sumatra", 100.5, -1.0), ("Borneo", 114.2, 0.6), ("Java", 110.2, -7.9), ("Asia", 101.5, 7.4), ("Sulawesi", 121.3, -2.0)):
        els.append(lab(*v.p(lo, la), t, .8, "#c9ad85", 27, st="ital"))
    gx, gy = v.p(107.0564, -6.9939)
    b = T(34, "Java was joined", -.1)
    els += [gl(gx, gy, 70, b, .7), {"k": "pin", "x": gx, "y": gy, "t": "Gunung Padang", "c": GOLD, "a": "end", "lx": -18, "ly": 36, "in": b}]
    return {"base": "map", "cam": CAM, "els": els}


def hand_pts(cx, cy, s):
    """A left hand, palm and five fingers, as one outline (s = palm width)."""
    p = []
    fingers = [(-.42, .95, .17), (-.15, 1.15, .17), (.12, 1.1, .17), (.36, .9, .15)]
    p += [(cx - .5 * s, cy + .6 * s), (cx - .55 * s, cy - .05 * s)]
    for fx_, L, w in fingers:
        x = cx + fx_ * s
        p += [(x - w * s / 2, cy - .1 * s), (x - w * s / 2, cy - L * s), (x, cy - (L + .1) * s), (x + w * s / 2, cy - L * s), (x + w * s / 2, cy - .1 * s)]
    p += [(cx + .5 * s, cy + .05 * s), (cx + .95 * s, cy - .35 * s), (cx + 1.05 * s, cy - .25 * s), (cx + .55 * s, cy + .45 * s), (cx + .45 * s, cy + .7 * s)]
    return p


def s35_add():
    v = SEA_V
    mx, my = v.p(122.6, -4.9)
    a = T(35, "On Sulawesi", .1)
    els = [{"k": "pin", "x": mx, "y": my, "t": "Muna", "c": OCHRE, "lx": 16, "in": a}]
    bx_, by_, bw, bh = 1330, 230, 360, 330
    b = T(35, "pressed a hand", -.2)
    els += [rect(bx_, by_, bw, bh, "#5a4636", "rgba(255,236,206,.35)", 2, 14, b, fx="pop"), ln([(mx + 10, my - 10), (bx_, by_ + bh)], b, OCHRE, 2, "inferred", .5)]
    r = random.Random(3)
    hx, hy, hs = bx_ + bw / 2 - 20, by_ + bh / 2 + 40, 92
    c = T(35, "sprayed paint", -.2)
    for k in range(150):
        ang = r.uniform(0, 2 * math.pi)
        rr = math.sqrt(r.uniform(0, 1))
        x, y = hx + 20 + 150 * rr * math.cos(ang), hy - 40 + 140 * rr * math.sin(ang)
        if bx_ + 12 < x < bx_ + bw - 12 and by_ + 12 < y < by_ + bh - 12:
            els.append(dt(x, y, r.uniform(4, 9), OCHRE, c + .01 * k, fx=None, op=round(r.uniform(.35, .8), 2)))
    els += [poly(hand_pts(hx, hy, hs), "#5a4636", "none", 0, b)]
    els += [lab(bx_ + bw / 2, by_ + bh + 44, "at least 67,800 years", T(35, "sixty-seven thousand", -.2), GOLD, 30)]
    return els


def tv(x, y, w, h, at):
    return [rect(x, y, w, h, "#15100c", "#cbd2d8", 4, 16, at, fx="pop"), ln([(x + w * .25, y), (x + w * .15, y - 50)], at, "#cbd2d8", 3, draw=False),
            ln([(x + w * .75, y), (x + w * .85, y - 50)], at, "#cbd2d8", 3, draw=False), rect(x + w / 2 - 70, y + h, 140, 18, "#2a2622", "#9a948a", 1.5, 4, at)]


def s36():
    """A writer's Netflix series opened on this hill (2022): a TV, the hill and a dotted pyramid on its screen."""
    x, y, w, h = 560, 210, 660, 400
    a = .4
    els = tv(x, y, w, h, a)
    els += [rect(x + 22, y + 22, w - 44, h - 44, "#2a2230", "none", 0, 8, a + .1),
            poly([(x + 40, y + h - 30), (x + 200, y + 220), (x + 300, y + 170), (x + 430, y + 165), (x + 520, y + 220), (x + w - 40, y + h - 30)], GRASS, GRASS_E, 2, a + .3),
            poly(PYR(x + w / 2, y + h - 34, 360, y + 180, 4), "rgba(201,193,238,.08)", LILAC, 2.5, a + .7, fx="draw", style="claimed", dur=1.0),
            poly([(x + w / 2 - 26, y + 120), (x + w / 2 + 34, y + 150), (x + w / 2 - 26, y + 180)], "rgba(245,236,220,.85)", "none", 0, a + 1.2, fx="pop"),
            lab(x + w + 40, y + 40, "2022", a + .8, GOLD, 32, "start"), lab(x + w / 2, y + h + 80, "a Netflix series", a + .9, DIM, 27)]
    return {"base": "dark", "cam": CAM, "els": els}


def s37():
    """Ages in years ago: the Great Pyramid about 4,500, Göbekli Tepe about 11,500, Gunung Padang as claimed 27,000 (dotted); twice
    Göbekli Tepe's age, 23,000, falls short of the claim."""
    x0, k = 560, 1000 / 27000
    X = lambda ya: r1(x0 + ya * k)
    els = [ln([(x0, 640), (X(27000), 640)], .2, BONE, 2, dur=.6)]
    for ya, t in ((0, "0"), (10000, "10,000"), (20000, "20,000")):
        els += [ln([(X(ya), 632), (X(ya), 648)], .3, BONE, 2, draw=False), lab(X(ya), 684, t, .3, DIM, 24)]
    els += [lab(X(27000), 684, "years ago", .4, DIM, 24, "end")]
    rows = [(300, "Great Pyramid of Giza", 4500, "c. 4,500", GOLD, "known", .5), (420, "Göbekli Tepe", 11500, "c. 11,500", GOLD, "known", 1.0)]
    for y, t, ya, v, c, st, at in rows:
        els += [lab(530, y + 10, t, at, BONE, 28, "end"), {"k": "line", "p": [[x0, y], [X(ya), y]], "c": c, "w": 44, "op": .85, "keepop": True, "fx": "draw", "dur": .9, "in": at, "style": st},
                lab(X(ya) + 16, y + 10, v, at + .8, DIM, 25, "start")]
    a = T(37, "Gunung Padang is", -.1)
    els += [lab(530, 550, "Gunung Padang, claimed", a, LILAC, 28, "end"),
            {"k": "rect", "x": x0, "y": 518, "w": r1(X(27000) - x0), "h": 44, "r": 8, "fill": "rgba(201,193,238,.18)", "c": LILAC, "sw": 2.5, "style": "claimed", "in": a, "fx": "draw", "dur": 2.2},
            lab(X(27000) - 10, 500, "27,000?", a + 2.0, LILAC, 28, "end")]
    b = T(37, "more than twice", -.1)
    els += [{"k": "line", "p": [[x0, 590], [X(11500), 590]], "c": GOLD, "w": 10, "op": .5, "keepop": True, "fx": "draw", "dur": .6, "in": b},
            {"k": "line", "p": [[X(11500) + 4, 590], [X(23000), 590]], "c": GOLD, "w": 10, "op": .5, "keepop": True, "fx": "draw", "dur": .6, "in": b + .6},
            lab(X(23000) + 14, 598, "twice Göbekli Tepe", b + 1.1, GOLD, 24, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================ chapter 4: a date for the soil
def s38():
    """Headlines round the world; doubts, many from Indonesian archaeologists; within weeks the journal opens an investigation."""
    els = []
    for k, (rot, x) in enumerate(((-12, 170), (-3, 300), (8, 430))):
        g = {"k": "group", "tr": "rotate(%d %d 420)" % (rot, x + 150), "in": .2 + .3 * k, "fx": "pop", "els": [
            rect(x, 230, 300, 380, "#e9e1d0", "#8a7a66", 2, 4), label(x + 150, 290, "OLDEST", 0, INK, 40, st="serif", halo=False),
            label(x + 150, 334, "PYRAMID", 0, INK, 40, st="serif", halo=False),
            {"k": "glyphs", "x": x + 26, "y": 370, "w": 248, "h": 200, "rows": 7, "cols": 5, "kind": "latin", "c": "#7a6a58"}]}
        els.append(g)
    a = T(38, "So did the doubts", .3)
    for k in range(7):
        x = 830 + 62 * k
        els += [person_(x, 680, 96, a + .1 * k), rect(x - 26, 470 - (k % 2) * 30, 52, 46, "rgba(245,236,220,.1)", BONE, 2, 14, a + .5 + .15 * k, fx="pop"),
                lab(x, 506 - (k % 2) * 30, "?", a + .55 + .15 * k, GOLD, 34, st="serif")]
    els += [lab(1016, 740, "many from Indonesia", T(38, "Indonesian archaeologists"), DIM, 26)]
    b = T(38, "the journal opened", -.2)
    els += [rect(1350, 220, 250, 330, PAPER, "#8a7a66", 2, 4, b - .4, fx="pop"), {"k": "glyphs", "x": 1372, "y": 250, "w": 206, "h": 270, "rows": 9, "cols": 5, "kind": "latin", "c": "#6a5a48", "in": round(b - .3, 2)},
            {"k": "circle", "x": 1470, "y": 380, "r": 70, "fill": "rgba(207,230,255,.12)", "c": "#e0e4ea", "w": 6, "in": round(b + .4, 2), "fx": "pop"},
            ln([(1520, 430), (1590, 500)], b + .4, "#8a6a44", 12, draw=False), lab(1475, 600, "an investigation", b + .7, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def hearth(x, y, at):
    return [oval(x + 34 * k - 34, y, 18, 12, "#6a645c", "none", 0, at=at, fx="pop") for k in range(3)] + [gl(x, y - 20, 70, at, .9, "fire"), dt(x - 6, y - 8, 8, "#0c0a08", at), dt(x + 10, y - 4, 7, "#0c0a08", at)]


def bone(x, y, at, s=1.0):
    return [ln([(x - 46 * s, y + 6 * s), (x + 46 * s, y - 6 * s)], at, PAPER, 12 * s, draw=False)] + [dt(x + dx * s, y + dy * s, 10 * s, PAPER, at) for dx, dy in ((-50, 0), (-46, 14), (48, -12), (52, 2))]


def tool(x, y, at, s=1.0):
    return [poly([(x - 30 * s, y + 24 * s), (x - 4 * s, y - 40 * s), (x + 26 * s, y + 24 * s), (x, y + 36 * s)], "#9aa0a8", "#e8e2d6", 2, at, fx="pop")]


def s39():
    """Not charcoal from a hearth, not a bone, not a tool: soil, packed between the stones."""
    a = T(39, "Not charcoal", -.1)
    b = T(39, "Not a bone", -.1)
    c = T(39, "Not a tool", -.1)
    els = hearth(260, 380, a) + [lab(260, 470, "a hearth", a + .1, BONE, 27), strk(170, 420, 350, 300, a + .5)]
    els += bone(560, 360, b) + [lab(560, 470, "a bone", b + .1, BONE, 27), strk(470, 420, 650, 300, b + .4)]
    els += tool(860, 360, c) + [lab(860, 470, "a tool", c + .1, BONE, 27), strk(770, 420, 950, 300, c + .4)]
    d = T(39, "Soil", -.1)
    els += [rect(1110, 210, 560, 460, SOIL, "rgba(255,236,206,.3)", 2, 10, d - .2, fx="pop")]
    els += stone_ends(1130, 1650, 230, 650, 34, d, .01, seed=7, jit=6)
    r = random.Random(9)
    for k in range(9):
        els.append(dt(1150 + r.uniform(0, 480), 250 + r.uniform(0, 380), 7, GOLD, d + 1.0 + .08 * k))
    els += [gl(1390, 440, 260, d + 1.0, .3), lab(1390, 720, "soil, between the stones", d + .6, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s40():
    """The radiocarbon clock (a candle burning down beside a leaf whose carbon fades); soil gathering carbon from plants over ages;
    a stone set on top: when?"""
    a = .4
    leaf = [poly([(150, 380), (230, 300), (330, 300), (390, 380), (330, 440), (230, 440)], "#4f6a3a", GRASS_E, 2, a, fx="pop")]
    dots = [(200 + 30 * (k % 6), 345 + 32 * (k // 6)) for k in range(12)]
    els = leaf + [dt(x, y, 6, GOLD, a + .3 + .03 * k) for k, (x, y) in enumerate(dots)]
    b = T(40, "like a candle", -.6)
    els += [rect(470, 300, 50, 260, PAPER, "#cbbca8", 1.5, 6, a + .2), gl(495, 280, 50, a + .2, .9, "fire"), dt(495, 288, 8, "#ffd27a", a + .2)]
    for k in range(4):
        els += [wipe(462, 270, 66, 62 * (k + 1) + 20, b + .5 * k, FLAT, 1.0, .3), gl(495, 340 + 62 * k - 52, 46, b + .5 * k, .9, "fire")]
        els += [dt(x, y, 7, "#4f6a3a", b + .5 * k + .05 * q) for q, (x, y) in enumerate(dots[k * 3:k * 3 + 3])]
    els += [lab(340, 220, "the radiocarbon clock", a + .3, GOLD, 30)]
    c = T(40, "And soil is full", -.1)
    gy = 380
    els += [rect(700, gy, 980, 420, SOIL, "none", 0, 0, c - .3, fx="pop"), ln([(700, gy), (1680, gy)], c - .3, GRASS_E, 3, draw=False)]
    r = random.Random(4)
    for cyc in range(3):
        at = c + .9 * cyc
        for k in range(5):
            x = 760 + 200 * k + r.uniform(-30, 30)
            els += [ln([(x, gy), (x + r.uniform(-8, 8), gy - r.uniform(40, 80))], at, GRASS_E, 3, dur=.4), ln([(x, gy), (x + r.uniform(-20, 20), gy + r.uniform(40, 120))], at + .3, "#3a2c20", 2, dur=.5)]
            els += [dt(x + r.uniform(-50, 50), gy + 40 + r.uniform(0, 330), 6, ["#f2c98e", "#d9a868", "#b08048"][cyc], at + .5 + .05 * k)]
    els += [wipe(700, gy - 100, 980, 98, c + 2.7, FLAT, 1.0, .6)]
    els += [lab(1190, 760, "carbon from plants, over ages", c + 2.6, GOLD, 26)]
    d = T(40, "It can't tell you", .2)
    els += column_side(1060, gy - 92, 300, 60, d + .6)
    els += [lab(1210, 240, "set on top: when?", d + 1.2, LILAC, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def westminster(x, gy, at, c="#2b2328", edge="rgba(255,226,190,.55)"):
    """A schematic Palace of Westminster in silhouette: the long front, its pinnacles, the clock tower (left) and a taller tower (right)."""
    out = [poly([(x, gy), (x, gy - 110), (x + 760, gy - 110), (x + 760, gy)], c, edge, 1.5, at)]
    for k in range(19):
        px = x + 20 + 40 * k
        out.append(poly([(px - 7, gy - 110), (px, gy - 140), (px + 7, gy - 110)], c, edge, 1.2, at))
    out += [poly([(x + 40, gy - 110), (x + 40, gy - 300), (x + 54, gy - 340), (x + 70, gy - 390), (x + 86, gy - 340), (x + 100, gy - 300), (x + 100, gy - 110)], c, edge, 1.5, at),
            dt(x + 70, gy - 270, 18, "#e8d6a8", at, fx=None, op=.85),
            poly([(x + 660, gy - 110), (x + 660, gy - 330), (x + 750, gy - 330), (x + 750, gy - 110)], c, edge, 1.5, at)]
    return out


def s41():
    """Flint Dibble's comparison: a core seven metres under the Houses of Parliament could hit soil 40,000 years old."""
    gy = 520
    els = [rect(80, gy, 1620, 300, SOIL_D, "none", 0, 0, -1), ln([(80, gy), (1700, gy)], -1, "rgba(255,226,190,.4)", 2, draw=False)]
    els += westminster(500, gy, .3)
    els += [lab(880, 170, "Houses of Parliament, London", T(41, "Houses of Parliament"), DIM, 26)]
    a = T(41, "drill seven metres", -.2)
    px = 30
    els += [ln([(960, gy - 30), (960, gy + 7 * px)], a, BLUE, 5, dur=1.0), dimline(1000, gy, 1000, gy + 7 * px, "7 m", a + .8, BLUE, lx=34, ly=8)]
    b = T(41, "forty thousand years ago", -.2)
    els += chip(1060, gy + 7 * px + 20, "40,000 years", GOLD, b, 28, "start")
    c = T(41, "That doesn't make", -.1)
    els += [rect(1270, 250, 330, 80, "rgba(201,193,238,.08)", LILAC, 2.5, 10, c, fx="pop", style="claimed"), lab(1435, 300, "built 40,000 years ago?", c + .1, LILAC, 25),
            strk(1270, 330, 1600, 250, c + .8)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [1500, 420, 20], "cam": CAM, "els": els}


def s42():
    """The vanished water again: the deep lava drawn as the paper describes it, full of fractures; water spreads along the cracks."""
    gy, px = 200, 38
    els = [rect(80, gy, 1000, 620, "#3a3632", "none", 0, 0, -1), ln([(80, gy), (1080, gy)], -1, GRASS_E, 3, draw=False),
           rect(686, gy, 28, 14 * px, "#0f0d0b", "#9a948a", 1.5, 0, -1),
           rect(620, gy + 9 * px, 160, 4 * px, "rgba(201,193,238,.06)", LILAC, 2, 4, -1, op=.6, style="claimed"), lab(820, gy + 11 * px + 10, "?", .3, LILAC, 40, "start", st="serif")]
    for m in (8, 14):
        els += [ln([(716, gy + m * px), (740, gy + m * px)], -1, BONE, 2, draw=False), lab(600, gy + m * px + 9, "%d m" % m, -1, DIM, 25, "end")]
    a = T(42, "full of fractures", -.3)
    r = random.Random(21)
    cracks = []
    for k in range(40):
        x, y = r.uniform(100, 1060), r.uniform(gy + 40, 800)
        ang = r.uniform(0, math.pi)
        L = r.uniform(50, 130)
        p = [(x, y), (x + L * math.cos(ang) * .5 + r.uniform(-12, 12), y + L * math.sin(ang) * .5), (x + L * math.cos(ang), y + L * math.sin(ang))]
        cracks.append(p)
        els.append(ln(p, a + .02 * k, "#141210", 3, dur=.4))
    els += [lab(1300, 300, "full of fractures", a + .4, BONE, 30)]
    b = T(42, "Cracked rock", -.2)
    k2 = 0
    for p in cracks:
        mx, my = p[1]
        if gy + 7 * px < my < gy + 15.5 * px and abs(mx - 700) < 420:
            els.append(ln(p, b + .05 * k2 + .3 * abs(mx - 700) / 420, BLUE, 3.5, dur=.4))
            k2 += 1
    els += [ln([(700, gy - 40), (700, gy + 14 * px)], b - .4, BLUE, 7, dur=.8), lab(1300, 560, "cracks swallow water", b + .8, BLUE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s43():
    """The retraction notice: 18 March 2024; its reason in three parts; the pyramid of 9,000 years or more struck; peer review missed it,
    after a review the authors say lasted about nine months."""
    els = [rect(200, 150, 540, 630, PAPER, "#8a7a66", 2, 6, .2), lab(470, 214, "RETRACTION", .3, INK, 40, st="serif", halo=False)]
    rows = [300, 380, 460, 540, 620, 700]
    els += [{"k": "glyphs", "x": 236, "y": y - 22, "w": 468, "h": 50, "rows": 2, "cols": 8, "kind": "latin", "c": "#6a5a48", "in": .4} for y in rows]
    a = T(43, "eighteenth of March", -.1)
    els += chip(470, 258, "18 March 2024", RED, a, 26)
    hl = [(T(43, "the dated soil"), 300, "soil samples", GOLD), (T(43, "any artefacts"), 380, "no artefacts or features", GOLD), (T(43, "was incorrect", -.4), 460, "incorrect", RED)]
    for at, y, t, c in hl:
        els += [{"k": "hl", "x": 226, "y": y - 30, "w": 488, "h": 56, "in": round(at, 2), "fx": "pop"}, ln([(716, y), (790, y)], at + .2, c, 2, dur=.3), lab(800, y + 9, t, at + .3, c, 27, "start")]
    b = T(43, "So reading the hill", -.1)
    els += [poly(PYR(1400, 470, 280, 260, 4), "rgba(201,193,238,.08)", LILAC, 2.5, b, fx="draw", style="claimed", dur=.9), lab(1400, 500, "9,000+ years", b + .3, LILAC, 27),
            strk(1250, 520, 1560, 240, T(43, "was incorrect"))]
    c = T(43, "slipped through peer", -.2)
    els += [rect(1210, 580, 380, 70, "rgba(245,236,220,.06)", DIM, 1.6, 10, c - .2, fx="pop"), lab(1240, 625, "peer review", c, BONE, 27, "start"), tick(1520, 610, c + .2, GREEN),
            tick(1520, 610, c + 1.0, "#6a645c")]
    d = T(43, "about nine", -.3)
    els += [rect(1214 + 41 * k, 668, 34, 24, "rgba(242,201,142,.25)", GOLD, 1.2, 4, d + .08 * k, fx="pop") for k in range(9)]
    els += [lab(1400, 730, "about 9 months, the authors say", d + .8, DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s44():
    """All twelve authors disagreed: the dated soil came from layers they read as built; the dates fit the stones' weathering; 'unjust'."""
    a = .3
    els = [person_(200 + 58 * k, 690, 104 - (k % 3) * 6, a + .06 * k, ["#e8d6b8", "#d9c3a0", "#efe0c0"][k % 3]) for k in range(12)]
    els += [lab(520, 750, "the paper's twelve authors", a + .9, DIM, 25)]
    b = T(44, "layers they had shown", -.4)
    els += [rect(1000, 200, 300, 220, "#5f4c39", "rgba(255,236,206,.3)", 2, 10, b, fx="pop"), rect(1000, 270, 300, 60, "#7a6a58", LILAC, 2.5, 0, b + .2, style="claimed"),
            dt(1150, 300, 9, GOLD, b + .4), lab(1150, 460, "built layers", b + .5, LILAC, 27)]
    c = T(44, "weathered", -.6)
    els += [oval(1500, 310, 120, 86, "#8a8378", "#c9c1b3", 2, at=c, fx="pop"), oval(1500, 310, 92, 62, "#6a645c", "none", 0, at=c + .2, fx="pop"),
            oval(1500, 310, 62, 40, "#4a4640", "none", 0, at=c + .4, fx="pop"), lab(1500, 460, "weathering rinds", c + .5, BONE, 27)]
    d = T(44, "unjust", -.3)
    els += [poly([(380, 420), (720, 420), (720, 500), (600, 500), (560, 548), (566, 500), (380, 500)], "rgba(201,193,238,.12)", LILAC, 3, d, fx="pop"),
            lab(550, 474, "unjust", d + .1, LILAC, 40, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def date_tag(x, y, at, c=GOLD, style="known"):
    return [rect(x, y - 22, 96, 44, "rgba(232,195,90,.15)" if style == "known" else "none", c, 3, 8, at, fx="pop", style=style),
            dt(x + 16, y, 6, c, at), lab(x + 58, y + 9, "date", at + .1, c, 24)]


def tpillar(x, by, h, at, c="#d9c29a", edge="#f2dcb4"):
    w = h * .2
    hh = h * .24
    pts = [(x - w / 2, by), (x + w / 2, by), (x + w / 2, by - h + hh), (x + w * 1.25, by - h + hh), (x + w * 1.25, by - h), (x - w * .75, by - h), (x - w * .75, by - h + hh), (x - w / 2, by - h + hh)]
    return [poly(pts, c, edge, 1.6, at, fx="rise")]


def s45():
    """The rule: a date tag tied to what it dates. Tied to a hearth's charcoal: it counts. Tied to soil, reaching for a pyramid: struck.
    Göbekli Tepe's wall plaster: a date tied to the building itself."""
    a = T(45, "A date counts", -.2)
    els = hearth(360, 270, a) + date_tag(640, 230, a + .4) + [ln([(640, 232), (420, 252)], a + .6, GOLD, 3, dur=.4), lab(820, 240, "tied", a + 1.0, GREEN, 30, "start")]
    b = T(45, "A date for soil", -.2)
    els += [oval(360, 470, 90, 46, SOIL, "#c9a070", 2, at=b, fx="pop"), dt(340, 462, 6, GOLD, b + .2), dt(384, 478, 6, GOLD, b + .2)] + date_tag(640, 430, b + .3) + \
           [ln([(640, 432), (450, 462)], b + .5, GOLD, 3, dur=.4), ln([(736, 432), (1060, 452)], b + .8, GOLD, 3, "inferred", .6),
            poly(PYR(1180, 510, 220, 360, 4), "rgba(201,193,238,.08)", LILAC, 2.5, b + 1.0, style="claimed"), strk(1040, 520, 1320, 350, T(45, "not a date for a pyramid", .2))]
    c = T(45, "At Göbekli Tepe", -.1)
    els += tpillar(330, 730, 160, c) + tpillar(430, 730, 140, c + .1)
    els += [rect(250, 600, 260, 130, "rgba(239,230,210,.55)", "none", 0, 4, c + .6, fx="pop")] + date_tag(640, 640, c + .9) + \
           [ln([(640, 642), (512, 660)], c + 1.1, GOLD, 3, dur=.4), lab(820, 650, "plaster, Göbekli Tepe", c + 1.3, GOLD, 27, "start"), lab(380, 576, "plaster", c + .8, BONE, 25)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================ chapter 5: the weighing
def s46():
    """The summit again (iso): in 2025, excavation squares open on the top terraces and people dig."""
    hill, ters, stair = summit_parts()
    base = iso(hill + ters + stair, at=-1, **SUMMIT)
    els = [gl(889, 560, 620, -1, .16, "lamp"), base]
    a = .4
    sq = []
    for (x, z) in ((18, -4), (24, 3), (12, 4)):
        sq.append({"t": "line", "p": [[x - 2.5, 21.1 if x > 20 else 19.5, z - 2.5], [x + 2.5, 21.1 if x > 20 else 19.5, z - 2.5], [x + 2.5, 21.1 if x > 20 else 19.5, z + 2.5],
                                      [x - 2.5, 21.1 if x > 20 else 19.5, z + 2.5], [x - 2.5, 21.1 if x > 20 else 19.5, z - 2.5]], "c": BLUE, "w": 3, "style": "inferred"})
    els += [ov(base, sq, a, fx="draw", dur=1.0)]
    els += [ov(base, [{"t": "person", "x": 18 + 2.5 * (k - 1), "y": 21.1 if k else 19.5, "z": -1 + 2 * k, "h": 1.7} for k in range(3)], a + .8, fx="rise")]
    tx, ty = P3(base, (20, 22, 0))
    els += chip(tx + 160, ty - 110, "2025", GOLD, T(46, "In twenty", .1), 30)
    els += [lab(tx + 160, ty - 50, "the top terraces", a + 1.2, BONE, 27), ln([(tx + 120, ty - 70), (tx + 30, ty - 10)], a + 1.2, DIM, 2, dur=.4)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [1500, 330, 20], "cam": CAM, "els": els}


def s47():
    """Under the top terrace: a trench four metres deep (95 units a metre), a sample at its foot announced as about 6000 BCE,
    rounded stones; not yet in a journal."""
    gy, px = 250, 95
    els = [rect(80, gy, 1620, 570, "#4a3c2e", "none", 0, 0, -1), ln([(80, gy), (1700, gy)], -1, GRASS_E, 3, draw=False),
           rect(80, gy - 12, 900, 12, TERR, TERR_E, 1, 2, -1), lab(200, gy - 30, "the top terrace", .3, DIM, 25, "start")]
    a = .4
    els += [rect(560, gy, 320, 4 * px, "#17120e", BLUE, 2.5, 4, a, fx="fill", dur=1.0, style="inferred"), dimline(920, gy, 920, gy + 4 * px, "4 m", a + .8, BLUE, lx=30, ly=8)]
    b = T(47, "six thousand", -.4)
    els += [dt(720, gy + 4 * px - 16, 10, GOLD, b), gl(720, gy + 4 * px - 16, 60, b, .7)] + chip(980, gy + 4 * px - 60, "c. 6000 BCE, announced", GOLD, b + .2, 26, "start")
    c = T(47, "rounded stone", -.2)
    els += [oval(620 + 52 * k, gy + 4 * px - 30 - (k % 2) * 10, 24, 16, "#7a7468", "#c9c1b3", 1.5, at=c + .1 * k, fx="pop") for k in range(5)]
    d = T(47, "isn't in a journal", -.3)
    els += [rect(1300, 160, 250, 300, "none", DIM, 2.5, 6, d, style="inferred", fx="pop"), lab(1425, 316, "...", d + .2, DIM, 50, st="serif"), lab(1425, 500, "not yet published", d + .3, DIM, 27)]
    return {"base": "dark", "cam": CAM, "els": els}


LEDGER_ROWS = [220, 335, 450, 565, 680]


def s48():
    """The ledger: rows light as named, each with a small picture and its grade chip."""
    els = [rect(100, 150, 1000, 600, "rgba(18,13,10,.78)", "rgba(255,236,206,.3)", 2, 18, .2)]
    names = ["terraces built by people", "columns made by a volcano", "what lies deeper", "ruled out", "a pyramid in the Ice Age"]
    ats = [T(48, "people built these", -.2), T(48, "from columns a volcano", -.3), T(48, "Open", -.1), T(49, "Ruled", -.1, ), T(50, "A pyramid built", -.1)]
    rows = []
    for k, (y, t) in enumerate(zip(LEDGER_ROWS, names)):
        rows.append((y, t))
    for k, (y, t) in enumerate(rows[:3]):
        at = ats[k]
        els += [rect(120, y - 48, 960, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 9, t, at + .1, BONE, 29, "start")]
    y = LEDGER_ROWS[0]
    els += mini_terraces(150, y + 26, 110, ats[0]) + [dt(205, y + 34, 6, "#0c0a08", ats[0] + .2), gl(205, y + 34, 26, ats[0] + .2, .8, "fire")]
    y = LEDGER_ROWS[1]
    els += column_side(150, y - 10, 90, 26, ats[1])
    y = LEDGER_ROWS[2]
    els += [poly([(140, y + 34), (180, y - 10), (230, y - 20), (270, y + 34)], GRASS, GRASS_E, 1.5, ats[2]), lab(206, y + 26, "?", ats[2] + .2, GOLD, 34, st="serif")]
    els += chip(760, LEDGER_ROWS[0], "Established", GRADE["established"], ats[0] + .8, 27, "start")
    els += chip(760, LEDGER_ROWS[1], "Established", GRADE["established"], ats[1] + .6, 27, "start")
    els += chip(760, LEDGER_ROWS[2], "Open question", GRADE["open"], ats[2] + .8, 27, "start")
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s49_add():
    a = T(49, "And the retraction", .3)
    # the retracted paper on a pan that cannot lift the claimed pyramid
    def paper(x, y, at):
        return [rect(x - 34, y - 70, 68, 70, PAPER, "#8a7a66", 1.5, 3, at), ln([(x - 30, y - 6), (x + 30, y - 64)], at, RED, 4, draw=False)]

    def pyr(x, y, at):
        return [poly(PYR(x, y, 120, y - 90, 3), "rgba(201,193,238,.1)", LILAC, 2.5, at, style="claimed")]
    els = balance(1400, 290, 300, -14, 700, a, paper, pyr, drop=120, pan=130)
    els += [lab(1400, 200, "couldn't carry the claim", T(49, "couldn't carry", -.2), BONE, 26)]
    b = T(49, "didn't dig the hill", -.3)
    els += [poly([(1180, 760), (1280, 640), (1420, 610), (1560, 640), (1680, 760)], GRASS, GRASS_E, 2, b + 1.6),
            ln([(1500, 600), (1560, 540)], b + 1.9, "#8a6a44", 5, draw=False), poly([(1488, 606), (1508, 590), (1520, 620), (1500, 630)], "#c9ccd2", "none", 0, b + 1.9, fx="pop")]
    c = T(49, "Ruled", -.1)
    y = LEDGER_ROWS[3]
    els += [rect(120, y - 48, 960, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, c, fx="pop"), lab(300, y + 9, "ruled out", c + .1, BONE, 29, "start"),
            ln([(170, y + 30), (230, y - 26)], c + .2, "#8a6a44", 5, draw=False), poly([(160, y + 36), (176, y + 18), (192, y + 40), (176, y + 50)], "#c9ccd2", "none", 0, c + .2)]
    els += chip(760, y, "not yet", GRADE["ruled"], T(49, "Not yet", -.1), 27, "start")
    return els


def s50_add():
    a = T(50, "A pyramid built", -.1)
    y = LEDGER_ROWS[4]
    els = [rect(120, y - 48, 960, 96, "rgba(201,193,238,.10)", "rgba(201,193,238,.45)", 1.5, 12, a, fx="pop"), lab(300, y + 9, "a pyramid in the Ice Age", a + .1, BONE, 29, "start"),
           poly([(140, y + 36), (190, y - 14), (260, y - 20), (300, y + 36)], "#2f3a2a", GRASS_E, 1.5, a), poly(PYR(218, y + 32, 90, y - 6, 3), "none", LILAC, 2, a + .2, style="claimed")]
    els += chip(760, y, "Awaiting evidence", GRADE["awaiting"], T(50, "Awaiting", -.2), 27, "start")
    return els


def s51():
    """The test: a trench (blue, to be dug) cut in steps from the terraces down into the deep layer, two people on its steps; a drill hole
    beside it for comparison (summit section, 15 units a metre)."""
    els = summit_section(-1, claimed=False)
    els += [rect(560 + 150 * k, 250 - 4 * k - 12, 140, 12, TERR, TERR_E, 1, 2, -1) for k in range(5)]
    a = T(51, "A trench", -.1)
    xs = [(780, 1100, 0), (810, 1070, 90), (840, 1040, 180), (870, 1010, 270), (900, 980, 360)]
    pts_l, pts_r = [], []
    for x0, x1, d in xs:
        y = y_at(x0, SUM) + d
        pts_l += [(x0, y), (x0, y + 90)]
    for x0, x1, d in reversed(xs):
        y = y_at(x1, SUM) + d
        pts_r += [(x1, y + 90), (x1, y)]
    trench = pts_l + pts_r
    els += [poly(trench, "#141110", BLUE, 3, a, fx="pop", style="inferred")]
    els += [person_(830, y_at(830, SUM) + 180, 26, a + .6), person_(1050, y_at(1050, SUM) + 270, 26, a + .8)]
    els += [lab(940, 205, "a trench", a + .3, BLUE, 30), ln([(1260, y_at(1260, SUM)), (1260, y_at(1260, SUM) + 300)], T(51, "not just a drill"), "#c9ccd2", 3, dur=.6),
            lab(1300, 205, "a drill hole", T(51, "not just a drill") + .2, DIM, 25, "start")]
    b = T(51, "into the deep", -.1)
    els += [lab(140, 330 + 300, "the deep layer", b, BONE, 27, "start"), ln([(330, 625), (900, y_at(900, SUM) + 420)], b + .2, DIM, 2, "inferred", .6)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def s52_add():
    """Close on the trench floor: a laid floor and the foot of a wall; under the floor, sealed, a stone tool and a hearth's charcoal;
    three labs, one published paper; two people who disagree, side by side."""
    fy = y_at(900, SUM) + 450                       # the trench floor (about 30 m down at 15 units a metre: schematic)
    a = T(52, "A wall or a floor", .2)
    els = [rect(902 + 13 * k, fy - 26, 12, 8, "#b9b3a0", "#efe6d2", .8, 1, a + .04 * k, fx="pop") for k in range(6)]
    els += [rect(904, fy - 60 + 9 * k, 14, 8, "#8c8a7c", "#efe6d2", .8, 1, a + .5 + .05 * k, fx="pop") for k in range(4)]
    b = T(52, "with a stone tool", -.1)
    els += tool(950, fy - 12, b, .16) + [gl(966, fy - 12, 10, b + .4, .9, "fire"), dt(964, fy - 12, 2.5, "#0c0a08", b + .4), dt(970, fy - 10, 2.5, "#0c0a08", b + .4)]
    els += [lab(940, fy + 40, "sealed under the floor", b + .6, GOLD, 24)]
    c = T(52, "Dated by more", -.1)
    for k in range(3):
        x = 1035 + 24 * k
        els += [poly([(x - 4, fy - 120), (x + 4, fy - 120), (x + 4, fy - 108), (x + 9, fy - 96), (x - 9, fy - 96), (x - 4, fy - 108)], "rgba(159,208,255,.4)", ICE, 1, c + .3 * k, fx="pop")]
    els += [lab(1059, fy - 134, "three labs", c + .8, ICE, 22)]
    d = T(52, "published for anyone", -.1)
    els += [rect(846, fy - 128, 22, 28, PAPER, "#8a7a66", 1, 2, d, fx="pop"), tick(858, fy - 112, d + .3, GREEN, .5)]
    e = T(52, "dug by people who disagree", -.1)
    els += [person_(926, fy - 26, 14, e, GOLD), person_(944, fy - 26, 14, e + .2, BLUE)]
    return els


def s53():
    """Luminescence: in sunlight a grain's stored charge is wiped clean; buried, it fills again in the dark; in the lab a light releases
    it as a glow, and the glow measures when the grain was buried."""
    a = T(53, "There's even a clock", .2)
    els = [gl(250, 230, 160, a, .8, "sun"), dt(250, 230, 36, "#ffe2b4", a)]
    els += [ln([(250 + 60 * math.cos(math.radians(q)), 230 + 60 * math.sin(math.radians(q))), (250 + 100 * math.cos(math.radians(q)), 230 + 100 * math.sin(math.radians(q)))], a + .2, "#ffe2b4", 3, dur=.3) for q in range(-10, 100, 22)]
    grains = [(330, 450), (470, 470)]
    els += [poly(ngon(x, y, 46, 7, 10), "#d9c9a0", "#fff0c8", 2, a + .3, fx="pop") for x, y in grains]
    els += [lab(400, 580, "sunlight wipes it clean", a + .6, GOLD, 26)]
    b = T(53, "camera film", -.3)
    els += [rect(130, 640, 240, 54, "#2a2622", "#9a948a", 1.5, 4, b, fx="pop")] + [rect(140 + 30 * k, 646, 16, 8, "#9a948a", "none", 0, 1, b) for k in range(8)] + \
           [rect(160, 660, 60, 26, "#efe6d2", "none", 0, 2, b + .1), lab(390, 678, "like film fogged by light", b + .2, DIM, 22, "start")]
    c = T(53, "buried grains", -.1)
    els += [rect(700, 280, 520, 420, SOIL, "rgba(255,236,206,.3)", 2, 12, c, fx="pop")] + [ln([(700, 280 + 70 * k), (1220, 280 + 70 * k)], c + .1, "#4a3c2e", 2, draw=False) for k in range(1, 6)]
    for gi, (x, y) in enumerate(((820, 560), (960, 520), (1100, 580))):
        els.append(poly(ngon(x, y, 46, 7, 20 * gi), "#d9c9a0", "#fff0c8", 2, c + .3))
        for q in range(6):
            els.append(dt(x - 20 + 20 * (q % 3), y - 12 + 24 * (q // 3), 6, GOLD, c + .8 + .25 * q + .08 * gi))
    els += [lab(960, 250, "buried: charge builds up", c + .6, BONE, 26)]
    d = T(53, "Measure it", -.1)
    els += [poly(ngon(1460, 470, 56, 7, 0), "#d9c9a0", "#fff0c8", 2, d, fx="pop"), poly([(1420, 200), (1500, 200), (1490, 400), (1430, 400)], "rgba(159,208,255,.18)", "none", 0, d + .3),
            gl(1460, 470, 140, d + .8, .9, "lamp"), lab(1460, 620, "in the lab: it glows", d + .5, ICE, 26)]
    e = T(53, "when it was", -.2)
    els += chip(1460, 700, "when it was buried", GOLD, e, 26)
    return {"base": "dark", "cam": CAM, "els": els}


def s54_add():
    """The close: the opening hill again, now at night; a lamp in a small trench on the top terrace."""
    els = [rect(-20, -20, W_ + 40, H_ + 40, "url(#k-sky-night)", "none", 0, 0, .1, op=1.0), {"k": "stars", "n": 120, "x0": 0, "x1": W_, "y0": 0, "y1": 700, "seed": 7, "in": .5}]
    els[0]["dur"] = 1.6
    els += [dt(1460, 200, 26, "#efe8da", .6, fx=None, op=.9), poly([(80, 820), (300, 440), (360, 452), (620, 820)], "#1d1a26", "none", 0, .4),
            poly([(1180, 820), (1500, 410), (1560, 418), (1840, 820)], "#1d1a26", "none", 0, .4),
            poly(hill_poly(), "#121810", "rgba(255,236,206,.18)", 1.5, .5)] + terraces(.7, .05, "#3a3830", "rgba(255,236,206,.25)", fx=None)
    a = T(54, "One honest trench", -.3)
    els += [rect(1010, 340, 40, 14, "#060504", "none", 0, 1, a), gl(1030, 346, 90, a + .3, .9, "lamp"), dt(1030, 344, 4, "#ffe2a8", a + .3), person_(1060, 345, 12, a + .5, "#3a3530")]
    return els


# ================================================================ the narration: the script's own lines, with [go:] markers
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


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel shot, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", 1, [(0, "Inside it", 2), (1, "That's deep", 3), (1, "A science journal", 4), (2, "So is there", 5)], {}),
    (0, 1, "title", 6, [], {"intro": True}),
    (1, 0, "world", 7, [(0, "Five stone terraces", 8), (1, "Dutch reports", 9), (1, "On the lowest", 10)], {"chapter": "Five terraces on a hill"}),
    (1, 1, "collision", 11, [(1, "Think of a coin", 12), (1, "Here the charcoal", 13), (2, "Pottery", 14)], {}),
    (1, 2, "reversal", 15, [], {}),
    (2, 0, "world", 16, [], {"chapter": "Stones that cut themselves"}),
    (2, 1, "collision", 17, [(1, "You can watch", 18), (2, "The cracks grow", 19), (2, "In Utah", 20)], {}),
    (2, 2, "reversal", 21, [(0, "Nature made", 22)], {}),
    (3, 0, "world", 23, [(1, "Radar sends", 24), (1, "Electric current", 25), (1, "And seven drills", 26)], {"chapter": "A pyramid in the scans"}),
    (3, 1, "collision", 27, [(1, "In the scans", 28), (1, "And in one borehole", 29), (1, "To the team", 30), (2, "Natawidjaja points", 31)], {}),
    (3, 2, "reversal", 32, [(1, "Their reading", 33)], {}),
    (3, 3, "tag", 34, [(0, "On Sulawesi", 35), (1, "The writer", 36), (1, "If the team", 37)], {}),
    (4, 0, "world", 38, [], {"chapter": "A date for the soil"}),
    (4, 1, "collision", 39, [], {}),
    (4, 2, "cost", 40, [(1, "The archaeologist Flint", 41), (2, "And the vanished", 42)], {}),
    (4, 3, "reversal", 43, [(1, "All the authors", 44)], {}),
    (4, 4, "tag", 45, [], {}),
    (5, 0, "world", 46, [(1, "His team announced", 47)], {"chapter": "The weighing"}),
    (5, 1, "weigh", 48, [(0, "And the retraction", 49), (1, "A pyramid built", 50)], {}),
    (5, 2, "test", 51, [(0, "A wall or a floor", 52), (0, "There's even a clock", 53)], {}),
    (5, 3, "close", 54, [], {}),
]

# alias shots: shot -> (the panel's shot, the camera on that panel, the additions built when the camera arrives)
ALIASES = {
    2: (1, [1, 889, 500], s02_add), 5: (1, [1.25, 960, 470], s05_add), 6: (1, [1, 889, 500], s06_add),
    24: (23, [1.7, 700, 430], s24_add), 25: (23, [1.7, 980, 430], s25_add), 26: (23, [1, 889, 500], s26_add),
    28: (27, [1.35, 820, 440], s28_add), 30: (27, [1.35, 820, 440], s30_add),
    35: (34, [1.35, 1140, 470], s35_add),
    49: (48, [1.3, 1094, 470], s49_add), 50: (48, [1, 889, 500], s50_add),
    52: (51, [2.4, 960, 620], s52_add),
    54: (1, [1, 889, 500], s54_add),
}
NSHOTS = 54


def _tagged(cams):
    """Each alias camera gets a tiny unique extra zoom (a few ten-thousandths: invisible), so its step can be found after the wall is built."""
    out = {}
    for k, i in enumerate(sorted(cams)):
        z, x, y = cams[i]
        out[i] = [round(z + .0003 * (k + 1), 4), x, y]
    return out


def _attach(ep, cams, late):
    """Give each alias step its additions: a panel item on that step (built once, shown from the start of its glide, timed on its clock)."""
    panels = ep["wall"]["panels"]
    for i, els in late.items():
        if not els:
            continue
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


def film():
    script = json.load(open(SCRIPT, encoding="utf-8"))
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % (sid - 1))
        beats.append(B(role, frm - 1, lines, **kw))
    CLK[0] = Clock(beats)
    g = globals()
    shots = []
    for n in range(1, NSHOTS + 1):
        if n in ALIASES:
            shots.append({"base": "dark", "cam": CAM, "els": []})
        else:
            shots.append(g["s%02d" % n]())
    alias = {n - 1: root - 1 for n, (root, cam, fn) in ALIASES.items()}
    cams = _tagged({n - 1: cam for n, (root, cam, fn) in ALIASES.items()})
    late = {n - 1: fn() for n, (root, cam, fn) in ALIASES.items()}
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-gunung-padang", "code": "LF.07", "series": script["series"], "title": script["title"], "case": "gunung-padang",
          "verdict": "unsupported", "claim": "Is there a human-made pyramid, begun in the Ice Age, inside Gunung Padang?", "mood": "mystery",
          "hook_text": "Is there a *pyramid* inside this hill?", "beats": beats, "shots": shots,
          "sources": "Natawidjaja et al. 2023, retracted (doi:10.1002/arp.1912) · Retraction notice 2024 (doi:10.1002/arp.1932) · "
                     "Archaeology 2024, Java's Megalithic Mountain · Yondri 2014 (doi:10.5614/sostek.itbj.2014.13.1.1) · "
                     "Bronto & Langi 2016 (doi:10.33332/jgsm.geologi.v17i1.28) · Müller 1998 (doi:10.1029/98JB00389) · "
                     "Voris 2000 (doi:10.1046/j.1365-2699.2000.00489.x) · Oktaviana et al. 2026 (doi:10.1038/s41586-025-09968-y) · "
                     "Rhodes 2011 (doi:10.1146/annurev-earth-040610-133425)",
          "post": "A terraced hill in Java, hailed in a journal as a pyramid begun 27,000 years ago, then retracted. The terraces people really "
                  "built, the volcanic columns that split themselves, the Indonesian team's scans and soil dates at their strongest, the "
                  "retraction and their reply, and the trench that would settle it.",
          "hashtags": ["#GunungPadang", "#Indonesia", "#Archaeology", "#AncientApocalypse", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": script["intro_title"], "yt_title": script["yt_title"], "description": desc, "end_line": script["end_line"]}
    out = remix(ep, alias=alias, cams=cams)
    return _attach(out, cams, late)


def EPISODES():
    return [film()]
