"""LF.26 · Sky Watchers · Stonehenge, Stone by Stone (16:9 long film, one wall).

The script is films/long/lf-stonehenge/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s52; s4, the title, is the intro card over the
hero), drawn while it is said. The monument itself is a small 3-D model of the real plan (the ring of thirty sarsens with its lintels,
the horseshoe of five trilithons, the bluestones, the Altar Stone under the fallen stones of the tallest trilithon), projected through a
camera and lit by a low sun: the hero at dusk, the monument rising in about 2500 BCE, and the hero again at night for the close. Plans
of the same layout carry the ditch, the 56 holes, the solstice axis and the calendar. Drawings are schematic and true to the numbers
said: solid = measured, dashed = inferred, dotted = claimed (the legends and the challengers' claims are lilac and dotted).

Facts: the script's facts_added (Clarke et al. 2024, 2026; Clarke & Kirkland 2026; Bevins et al. 2022, 2023, 2024, 2025; Parker Pearson
et al. 2007, 2015, 2019, 2021, 2022, 2024; Darvill 2022a, 2022b; Nash et al. 2020; Thomas 1923; Kellaway 1971; John 2024; Harris 2016;
Evans et al. 2025; Bayliss et al. 1997; Cleal et al. 1995; Darvill et al. 2012; Willis et al. 2016; Snoeck et al. 2018; Brace et al.
2019; Allen et al. 2016; Ruggles 1997; Magli & Belmonte 2023; Parker Pearson & Ramilisonina 1998; Darvill & Wainwright 2009; Wright et
al. 2014; Madgwick et al. 2019; Geoffrey of Monmouth; English Heritage).

Engine workaround (as in lf_troy.py and lf_antikythera.py): the wall only adds elements to a panel on its first visit, at a beat start
or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag,
invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that step's
clock). Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25 syllables a second).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-stonehenge/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-stonehenge/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-stonehenge RC_FILMS_EPS=/tmp/claude-0/sbx_lf-stonehenge/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-stonehenge/boards python3 films.py long.lf_stonehenge
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-stonehenge", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
SARS, SARS_L, SARS_D = "#a89a86", "#e6cda2", "#4e4a52"      # sarsen: mid, sunlit, shade
BLUS, BLUS_L, BLUS_D = "#6f8090", "#a9bccb", "#39424e"      # bluestone (spotted dolerite)
ALTAR, ALTAR_L = "#7d8a6a", "#c9d6a8"                      # the Altar Stone: greenish sandstone
CHALK, CHALK_D = "#e9e2d0", "#b9ae96"
TURF, TURF_D, TURF_L = "#4a5634", "#2c3420", "#6f7c4c"
SKIN, WOOD, WOOD_D = "#e8d6b8", "#7a5434", "#46301e"
SEAC = "#3f86a8"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#c9e48f", "open": "#f0b06a", "awaiting": "#d9c26a", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # BCE, DNA: letters
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
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("-", ""))


def _clock(text):
    """[(word, t)] for a marked-up text whose lines are joined by newlines; t in seconds from its start."""
    out, t = [], 0.0
    for li, ln_ in enumerate(text.split("\n")):
        if li:
            t += LGAP
        cuts = [0] + [m.start() for m in SENT.finditer(ln_) if m.start() > 0] + [len(ln_)]
        for a, z in zip(cuts, cuts[1:]):
            seg = ln_[a:z]
            p = re.search(r"\[p:([\d.]+)\]", seg)
            r = RATE * (float(p.group(1)) if p else 1.0)
            for w in _spoken(seg):
                for part in w.split("-"):
                    if part:
                        out.append((_norm(part), t))
                        t += _syl(part) / r
                if w[-1] in ",:;":
                    t += CGAP
            t += SGAP
    return out, t


SAY = {}                     # shot id -> the narration spoken while its step is on screen (set in film())


def T(sid, phrase, lead=.3, k=1):
    """Seconds after the shot's step starts at which `phrase` is said (its k-th occurrence)."""
    ws, _ = _clock(SAY[sid])
    want = [_norm(p) for w in phrase.replace("-", " ").split() for p in [w] if _norm(p)]
    hits = [i for i in range(len(ws)) if [w for w, _ in ws[i:i + len(want)]] == want]
    assert len(hits) >= k, (sid, phrase, SAY[sid][:200])
    return round(lead + ws[hits[k - 1]][1], 2)


def DUR(sid):
    return round(_clock(SAY[sid])[1], 2)


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
    e = I.line(R(p), round(at, 2), c, w, style, dur, curve, draw, op)
    e.update(kw)
    return e


def arr(p, at, c=AMBER, w=3, style="known", dur=.8, curve=True, **kw):
    e = I.arrow(R(p), round(at, 2), c, w, style, dur, curve)
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


def gl(x, y, r, at, op=.6, kind="lamp", **kw):
    e = glow(round(x, 1), round(y, 1), round(r), round(at, 2), op, kind)
    e.update(kw)
    return e


def E(cx, cy, rx, ry, n=36, a0=0, a1=360):
    pts = ellipse(cx, cy, rx, ry, n, a0, a1)
    return pts[:-1] if (a0, a1) == (0, 360) else pts


def grp(els, at, fx="pop", tr=None, **kw):
    """A group that builds in as one piece (its children have no build-ins of their own); tr = an SVG transform."""
    if tr:
        els = [{"k": "group", "tr": tr, "els": els}]
    e = {"k": "group", "els": els, "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    e.update(kw)
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


def chip(x, y, t, c, at, size=28, a="middle", z=1.0):
    """A pill with a coloured rim and its words (grades, dates); z = the camera zoom it is seen at (the rim scales with the camera,
    the words keep their size)."""
    w = (len(t) * size * .56 + 44) / z
    h = size * 1.7 / z
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36 / z, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


def tick(x, y, at, c=GREEN, s=1.0, w=6):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": w, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cross(x, y, at, c=RED, s=1.0, w=6):
    return [ln([(x - 16 * s, y - 16 * s), (x + 16 * s, y + 16 * s)], at, c, w, dur=.25), ln([(x + 16 * s, y - 16 * s), (x - 16 * s, y + 16 * s)], at + .15, c, w, dur=.25)]


def qmark(x, y, at, size=90, c=LILAC, halo=True):
    out = [gl(x, y - size * .3, size * 1.1, at, .5)] if halo else []
    return out + [lab(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def bracket(x0, x1, y, at, t=None, c=BONE, up=True, size=26, ty=None, style="known"):
    d = -12 if up else 12
    out = [ln([[x0, y + d], [x0, y], [x1, y], [x1, y + d]], at, c, 2, style, dur=.6)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else (y - 16 if not up else y + 36), t, at + .3, c, size))
    return out


def axis(x0, x1, y, ticks, at, t=None):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    return e


def pin(x, y, t, at, c=AMBER, a="start", lx=None, ly=None, st="lab", tc=None):
    e = {"k": "pin", "x": round(x, 1), "y": round(y, 1), "t": t, "c": c, "a": a, "in": round(at, 2), "st": st}
    if lx is not None:
        e["lx"] = lx
    if ly is not None:
        e["ly"] = ly
    if tc:
        e["tc"] = tc
    return e


def blob(cx, cy, rx, ry, n=22, jit=.18, seed=1, rot=0):
    """An irregular closed outline (a boulder, a crag, a cloud)."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + rot
        f = 1 + r.uniform(-jit, jit)
        out.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return out


def rot(pts, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def mix(c1, c2, t):
    """Blend two #rrggbb colours (t = 0 gives c1)."""
    t = max(0.0, min(1.0, t))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[k] + (b[k] - a[k]) * t) for k in range(3))


# ================================================================== figures
def fig(x, y, h, at, c="#1a1410", arms=None, face=1, fx="rise", op=None, lean=0.0):
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up', 'pull' (both forward and low), 'lift'.
    lean > 0 tilts the body forward (hauling)."""
    f = face
    X = lambda a, b=0: x + f * (a * h + lean * b * h)
    Y = lambda b: y - b * h
    els = [circ(X(.01, .9), Y(.9), .085 * h, c, at=at),
           poly([(X(-.13, .78), Y(.78)), (X(.13, .78), Y(.78)), (X(.11, .44), Y(.44)), (X(-.11, .44), Y(.44))], c, at=at),
           poly([(X(-.11, .46), Y(.46)), (X(.11, .46), Y(.46)), (X(.085), Y(0)), (X(.025), Y(0)), (X(0, .3), Y(.3)), (X(-.025), Y(0)), (X(-.085), Y(0))], c, at=at)]
    aw = max(2.5, .045 * h)
    if arms is None:
        els += [ln([(X(-.12, .76), Y(.76)), (X(-.15, .46), Y(.46))], at, c, aw, draw=False), ln([(X(.12, .76), Y(.76)), (X(.15, .46), Y(.46))], at, c, aw, draw=False)]
    elif arms == "point":
        els += [ln([(X(-.12, .76), Y(.76)), (X(-.15, .46), Y(.46))], at, c, aw, draw=False), ln([(X(.1, .75), Y(.75)), (X(.42, .8), Y(.8))], at, c, aw, draw=False)]
    elif arms == "up":
        els += [ln([(X(-.12, .76), Y(.76)), (X(-.15, .46), Y(.46))], at, c, aw, draw=False), ln([(X(.1, .76), Y(.76)), (X(.2, 1.08), Y(1.08))], at, c, aw, draw=False)]
    elif arms == "pull":
        els += [ln([(X(-.1, .75), Y(.75)), (X(.3, .62), Y(.62))], at, c, aw, draw=False), ln([(X(.1, .75), Y(.75)), (X(.36, .6), Y(.6))], at, c, aw, draw=False)]
    elif arms == "lift":
        els += [ln([(X(-.1, .76), Y(.76)), (X(-.2, 1.06), Y(1.06))], at, c, aw, draw=False), ln([(X(.1, .76), Y(.76)), (X(.2, 1.06), Y(1.06))], at, c, aw, draw=False)]
    e = grp(els, at, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return [e]


# ================================================================== the monument: a small 3-D model of the real plan
# Plan units are metres: x east, y north, z up; azimuths in degrees clockwise from north. The solstice axis runs at azimuth 50
# (midsummer sunrise, north-east) and 230 (midwinter sunset, south-west). The ring: 30 sarsen uprights on a circle of radius 15.6 m
# (about 33 m across), 4.1 m tall, 2.1 m wide, 1.1 m thick, the gap between stones 30 and 1 on the axis; lintels 0.8 m thick on top.
# The horseshoe: five trilithons opening north-east, the tallest (55-56) at the south-west, 6.7 m uprights under a 1 m lintel.
AX = 50.0
RING_R = 15.6


def AZ(a, r):
    """The plan point at azimuth a (degrees) and distance r (m) from the centre."""
    t = math.radians(a)
    return (r * math.sin(t), r * math.cos(t))


def ring_az(k):
    """Azimuth of sarsen upright k (1..30), clockwise from the axis gap."""
    return AX + (k - .5) * 12.0


TRIL = [  # (stones, azimuth, distance, upright height, state)
    ((51, 52), AX + 62, 7.4, 5.6, "up"), ((53, 54), AX + 118, 7.0, 6.1, "up"), ((55, 56), AX + 180, 6.6, 6.7, "fallen55"),
    ((57, 58), AX + 242, 7.0, 6.1, "up"), ((59, 60), AX + 298, 7.4, 5.6, "fallen59")]
STANDING = {1, 2, 3, 4, 5, 6, 7, 10, 11, 16, 21, 22, 23, 27, 28, 29, 30}
FALLEN = {8: 1, 9: -1, 12: 1, 14: 1, 15: -1, 19: 1, 25: -1}          # fallen uprights, lying outwards (1) or inwards (-1)
LINTELS = [(29, 30), (30, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7), (21, 22)]


def blk(cx, cy, z0, L, W, H, yaw, kind="sarsen", taper=.92, tag=None, seed=0, at=-1):
    """A stone as a slightly tapering block: centre (cx, cy) in plan, base height z0, length L along azimuth yaw, width W across,
    height H; kind = sarsen, blue, altar."""
    return {"c": (cx, cy, z0), "L": L, "W": W, "H": H, "yaw": yaw, "kind": kind, "taper": taper, "tag": tag, "seed": seed, "at": at}


def monument(state="ruin"):
    """The stones as blocks: 'ruin' (today, with the Altar Stone under the fallen 55 and 156) or 'whole' (as built, about 2500 BCE)."""
    B = []
    r = random.Random(5)
    whole = state == "whole"
    for k in range(1, 31):
        a = ring_az(k)
        x, y = AZ(a, RING_R)
        h = 4.1 + r.uniform(-.15, .15)
        if whole or k in STANDING:
            w = 1.2 if (k == 11 and not whole) else 2.1
            hh = 2.6 if (k == 11 and not whole) else h
            B.append(blk(x, y, 0, w, 1.1, hh, a + 90, "sarsen", .9, "u%d" % k, k))
        elif k in FALLEN:
            d = FALLEN[k]
            fx, fy = AZ(a, RING_R + d * 2.4)
            B.append(blk(fx, fy, 0, 4.0, 2.0, .9, a, "sarsen", .96, "f%d" % k, k))
    for k in range(1, 31):
        if whole or (k, k % 30 + 1) in LINTELS:
            a = ring_az(k) + 6
            x, y = AZ(a, RING_R)
            B.append(blk(x, y, 4.15, 3.25, 1.0, .8, a + 90, "sarsen", 1.0, "l%d" % k, 100 + k))
    for (s1, s2), a, d, h, st in TRIL:
        cx, cy = AZ(a, d)
        ux, uy = math.sin(math.radians(a + 90)), math.cos(math.radians(a + 90))
        for j, s in ((-1, s1), (1, s2)):
            px, py = cx + ux * j * 1.25, cy + uy * j * 1.25
            if whole or not ((st == "fallen55" and s == 55) or (st == "fallen59" and s == 59)):
                B.append(blk(px, py, 0, 2.2, 1.2, h, a + 90, "sarsen", .88, "t%d" % s, s))
        if whole or st == "up":
            B.append(blk(cx, cy, h + .05, 5.0, 1.15, 1.0, a + 90, "sarsen", 1.0, "tl%d" % s1, 200 + s1))
    # bluestones: an outer circle (radius 11.7 m) and an inner horseshoe (radius about 5 m)
    rb = random.Random(11)
    for k in range(40 if whole else 26):
        a = AX + 4.5 + k * (360.0 / (40 if whole else 26)) + (0 if whole else rb.uniform(-3, 3))
        if not whole and rb.random() < .25:
            continue
        x, y = AZ(a, 11.7)
        h = 1.9 if whole else rb.choice([.7, 1.1, 1.6, 1.9, 2.0])
        B.append(blk(x, y, 0, .8, .55, h, a + 90, "blue", .85, "b%d" % k, 300 + k))
    hs = [AX + 180 + d for d in (-80, -60, -40, -22, 22, 40, 60, 80)] if whole else [AX + 180 + d for d in (-78, -58, -38, 38, 58, 78)]
    for k, a in enumerate(hs):
        dd = 4.6 + abs(math.sin(math.radians(a - AX - 180))) * .8
        x, y = AZ(a, dd)
        B.append(blk(x, y, 0, .7, .5, 2.2 if whole else 2.0, a + 90, "blue", .8, "bh%d" % k, 400 + k))
    # the Altar Stone, lying across the axis at the foot of the tallest trilithon
    ax_, ay_ = AZ(AX + 180, 4.3)
    B.append(blk(ax_, ay_, 0, 4.9, 1.0, .5, AX + 90, "altar", 1.0, "altar", 7))
    if not whole:
        # 55 fell inwards and broke in two, across the Altar Stone; its lintel 156 lies beside it
        for j, (dd, off) in enumerate(((3.5, -.4), (2.2, .5))):
            px, py = AZ(AX + 180 + off * 9, dd)
            B.append(blk(px, py, .5 * (1 - j), 2.6, 1.8, .9, AX + 180 + 10 - 25 * j, "sarsen", .97, "f55%d" % j, 55 + j))
        px, py = AZ(AX + 180 + 34, 5.0)
        B.append(blk(px, py, 0, 4.4, 1.2, .9, AX + 112, "sarsen", 1.0, "f156", 156))
        # 59 and 160 fallen at the north end of the horseshoe
        px, py = AZ(AX + 298 - 6, 5.0)
        B.append(blk(px, py, 0, 4.2, 2.0, 1.0, AX + 298 + 60, "sarsen", .97, "f59", 59))
        px, py = AZ(AX + 298 + 8, 4.2)
        B.append(blk(px, py, 0, 4.4, 1.1, .9, AX + 298 - 30, "sarsen", 1.0, "f160", 160))
    return B


class Cam3:
    """A camera that looks horizontally along azimuth `look` from `eye` (x, y, z in m), focal length f (units), the horizon at
    screen height hy (a shifted lens: vertical edges stay vertical)."""

    def __init__(self, eye, look, f=1200.0, cx=889.0, hy=200.0):
        self.e, self.f, self.cx, self.hy = eye, f, cx, hy
        t = math.radians(look)
        self.fw = (math.sin(t), math.cos(t))               # forward, in plan
        self.rt = (math.cos(t), -math.sin(t))              # right, in plan

    def p(self, P):
        dx, dy, dz = P[0] - self.e[0], P[1] - self.e[1], P[2] - self.e[2]
        d = dx * self.fw[0] + dy * self.fw[1]
        xr = dx * self.rt[0] + dy * self.rt[1]
        d = max(d, .5)
        return (self.cx + self.f * xr / d, self.hy - self.f * dz / d, d)


def _corners(b):
    """The 8 corners (4 at the base, 4 on top) of a block, its top a little uneven and leaning (seeded, so each stone keeps its
    own shape in every view)."""
    cx, cy, z0 = b["c"]
    a = math.radians(b["yaw"])
    u = (math.sin(a), math.cos(a))
    v = (math.cos(a), -math.sin(a))
    r = random.Random(b["seed"] * 7 + 3)
    tall = b["H"] > 1.2
    lean = (r.uniform(-.1, .1), r.uniform(-.1, .1)) if tall else (0, 0)
    out = []
    for z, s in ((z0, 1.0), (z0 + b["H"], b["taper"])):
        for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            dz = (r.uniform(-.07, .05) * b["H"] if (z > z0 and tall) else 0)
            x = cx + u[0] * su * b["L"] / 2 * s + v[0] * sv * b["W"] / 2 * s + (lean[0] if z > z0 else 0)
            y = cy + u[1] * su * b["L"] / 2 * s + v[1] * sv * b["W"] / 2 * s + (lean[1] if z > z0 else 0)
            out.append((x, y, z + dz))
    return out


PAL = {"dusk": {"sarsen": ("#39333f", "#8a8076", "#f3c47e"), "blue": ("#283040", "#5d6f80", "#bccddb"), "altar": ("#2e3a2a", "#6f805c", "#dfe8a8"),
                "edge": "rgba(20,14,12,.6)", "rim": "rgba(255,214,150,.75)", "lichen": "#2d3a2a"},
       "night": {"sarsen": ("#171a26", "#454a62", "#aeb6dc"), "blue": ("#141a26", "#384660", "#90a6c8"), "altar": ("#1c2418", "#4b5a3c", "#b8c898"),
                 "edge": "rgba(4,5,9,.65)", "rim": "rgba(190,205,255,.45)", "lichen": "#0d120e"},
       "day": {"sarsen": ("#4f4a44", "#8f877b", "#dccaa5"), "blue": ("#34404c", "#66788a", "#b8c8d6"), "altar": ("#3f4a34", "#7d8a6a", "#d7e2b8"),
               "edge": "rgba(24,18,14,.5)", "rim": "rgba(255,240,210,.5)", "lichen": "#4a5236"}}


def _shade(pal, kind, k):
    dark, mid, light = pal[kind]
    return mix(dark, mid, k / .55) if k < .55 else mix(mid, light, (k - .55) / .6)


def _blotch(scr, r, size=.16):
    """A small irregular patch (lichen, a pit) inside a screen quad, at a random place."""
    u, v = r.uniform(.22, .78), r.uniform(.25, .8)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = scr
    px = (1 - v) * ((1 - u) * x0 + u * x1) + v * ((1 - u) * x3 + u * x2)
    py = (1 - v) * ((1 - u) * y0 + u * y1) + v * ((1 - u) * y3 + u * y2)
    w = math.hypot(x1 - x0, y1 - y0) * size
    h = math.hypot(x3 - x0, y3 - y0) * size * .7
    return blob(px, py, max(1.5, w), max(1.5, h), 9, .3, r.randint(1, 999))


def render(blocks, cam, sun=(305, 8), mood="dusk", at=-1, shadows=True, rise=None, skip=(), only=None, op=None, texture=True):
    """The blocks as lit, depth-sorted polygons through camera `cam`. sun = (azimuth, elevation) of the light. rise = {tag: time}
    gives a block its own build-in (fx rise, as a group); other blocks use `at`. Returns elements."""
    pal = PAL[mood]
    sa, se = math.radians(sun[0]), math.radians(sun[1])
    Ls = (math.sin(sa) * math.cos(se), math.cos(sa) * math.cos(se), math.sin(se))
    ex, ey, ez = cam.e
    items = []
    for b in blocks:
        if b["tag"] in skip or (only is not None and b["tag"] not in only):
            continue
        C = _corners(b)
        cx, cy, z0 = b["c"]
        dist = math.hypot(cx - ex, cy - ey) - .002 * z0
        faces = []
        for idx, nrm in (((4, 5, 6, 7), (0, 0, 1)), ((0, 1, 5, 4), None), ((1, 2, 6, 5), None), ((2, 3, 7, 6), None), ((3, 0, 4, 7), None)):
            pts3 = [C[i] for i in idx]
            mx = sum(p[0] for p in pts3) / 4
            my = sum(p[1] for p in pts3) / 4
            mz = sum(p[2] for p in pts3) / 4
            if nrm is None:
                ox, oy = mx - cx, my - cy
                L = math.hypot(ox, oy) or 1
                nrm = (ox / L, oy / L, 0.0)
            if nrm[0] * (ex - mx) + nrm[1] * (ey - my) + nrm[2] * (ez - mz) <= 0:
                continue
            lit = max(0.0, nrm[0] * Ls[0] + nrm[1] * Ls[1] + nrm[2] * Ls[2])
            k = .1 + 1.0 * lit + .32 * nrm[2]
            scr = [cam.p(p)[:2] for p in pts3]
            faces.append((scr, _shade(pal, b["kind"], k), lit, nrm[2] > .5))
        items.append((dist, b, faces))
    items.sort(key=lambda t: -t[0])
    els = []
    if shadows:
        for dist, b, faces in items:
            if b["H"] < 1.2 or b["c"][2] > .5:
                continue
            C = _corners(b)
            L_ = min(3.2, 1 / max(.2, math.tan(se))) * b["H"] * .55
            sx, sy = -math.sin(sa) * L_, -math.cos(sa) * L_
            tip = [(p[0] + sx, p[1] + sy, 0) for p in C[4:]]
            hull = _hull([cam.p(p)[:2] for p in C[:4] + tip])
            sh = poly(hull, "rgba(6,8,10,.34)" if mood != "night" else "rgba(0,0,6,.3)", at=at)
            if rise and b["tag"] in rise:
                sh["in"], sh["fx"] = rise[b["tag"]] + .3, "fade"
            els.append(sh)
    for dist, b, faces in items:
        sub = []
        rr = random.Random(b["seed"] * 13 + 1)
        for scr, col, lit, top in faces:
            sub.append(poly(scr, col, pal["edge"], 1.0, at))
            if texture and b["kind"] != "altar" and not top and b["H"] > .9:
                for _ in range(2):
                    sub.append(poly(_blotch(scr, rr, .12), pal["lichen"], "none", 0, at, curve=True, op=.16))
            if lit > .3:
                sub.append(ln(scr + scr[:1], at, pal["rim"], 1.3, draw=False, op=min(1, .4 + lit)))
        if rise and b["tag"] in rise:
            for e in sub:
                e["in"] = 0
                e.pop("fx", None)
            els.append(grp(sub, rise[b["tag"]], "rise"))
        else:
            els += sub
    if op is not None:
        for e in els:
            e.update(op=op, keepop=True)
    return els


def _hull(pts):
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in pts))
    if len(pts) < 3:
        return pts
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def ground_ring(cam, r, at, c="rgba(255,236,206,.25)", w=2, z=0.0, n=120, a0=0, a1=360, style="known"):
    """A circle on the ground (radius r m), the part in front of the camera, as a screen polyline."""
    pts = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        x, y = AZ(a, r)
        X, Y, d = cam.p((x, y, z))
        if d > 1.0:
            pts.append((X, Y))
    return [ln(pts, at, c, w, style, draw=False)] if len(pts) > 2 else []


def sky_glow(hy, sx, at=-1, warm=True):
    """The glow of a low sun along the horizon: bands that warm towards it, a halo round the sun at (sx, hy - 28)."""
    els = []
    if warm:
        for k in range(14):
            els.append(rect(-60, hy - 9 * (k + 1), 1900, 9 * (k + 1), "rgba(236,150,90,%.3f)" % (.03 + .008 * (13 - k)), at=at))
        els += [gl(sx, hy - 28, 520, at, .42, "sun"), gl(sx, hy - 28, 230, at, .55, "sun"),
                rect(-60, hy - 5, 1900, 5, "rgba(255,206,150,.35)", at=at)]
    return els


def ground_wash(cam, mood="dusk", at=-1):
    """Light and shade on the turf: a warm wash towards the sun, the near ground darker."""
    hy = cam.hy
    if mood == "night":
        return [rect(-60, hy, 1900, 900, "rgba(6,8,16,.45)", at=at)]
    return [gl(1450, hy + 40, 700, at, .22, "sun")] + [rect(-60, hy + 300 + 36 * k, 1900, 900, "rgba(10,12,6,.035)", at=at) for k in range(14)]


HERO_CAM = Cam3(AZ(AX + 8, 47.0) + (14.5,), AX + 180 + 8, 1250, 889, 225)
SUN_X = 1640
HERO_SUN = (322, 11)


def hero(mood="dusk", at=-1):
    """Stonehenge as it stands, seen from the north-east and above, a little off the axis, at dusk (or by moonlight)."""
    cam = HERO_CAM
    B = monument("ruin")
    els = ground_wash(cam, mood, at)
    els += ground_ring(cam, 52, at, "rgba(232,214,170,.22)", 2.5) + ground_ring(cam, 55.5, at, "rgba(16,20,10,.45)", 5)
    els += render(B, cam, HERO_SUN if mood == "dusk" else (295, 30), mood, at)
    px, py, d = cam.p(AZ(AX + 98, 21.0) + (0,))
    els += fig(px, py, cam.f * 1.7 / d, at, "#14100c" if mood == "dusk" else "#07080c", fx=None)
    return els


def altar_pts(cam=HERO_CAM, z=.5):
    """The Altar Stone's top face on screen (4 points), and its centre."""
    b = next(b for b in monument("ruin") if b["tag"] == "altar")
    C = _corners(b)[4:] if z else _corners(b)[:4]
    pts = [cam.p(p)[:2] for p in C]
    return pts, (sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4)


def altar_xy(cam=HERO_CAM):
    return altar_pts(cam)[1]


def hero_base(mood="dusk"):
    return {"base": "sky", "tod": "dusk" if mood == "dusk" else "night", "ground": HERO_CAM.hy,
            "sun": [SUN_X, HERO_CAM.hy - 28, 30] if mood == "dusk" else False,
            "groundc": TURF if mood == "dusk" else "#1a2016",
            "ridges": [{"y": HERO_CAM.hy - 14, "a": 24, "c": "#3c3446" if mood == "dusk" else "#151826", "seed": 4},
                       {"y": HERO_CAM.hy - 1, "a": 12, "c": "#2a2f24" if mood == "dusk" else "#10140f", "seed": 8}]}


# ================================================================== COLD OPEN
def s1():
    """The hero image, complete from the first frame: Stonehenge at dusk from the north-east, the sun low at the right, long shadows,
    a person for scale; on 'the Altar Stone', the slab under the fallen stones of the tallest trilithon is outlined in gold and glows."""
    ta = T("s1", "the Altar Stone")
    top, (ax, ay) = altar_pts()
    els = sky_glow(HERO_CAM.hy, SUN_X) + hero("dusk")
    els += [gl(ax, ay, 130, ta, .6, "lamp", pulse=True),
            ln(top + top[:1], ta + .1, "#ffe7b0", 3.5, dur=.7),
            ln([(ax + 24, ay - 26), (ax + 190, ay - 190)], ta + .5, GOLD, 2, dur=.4),
            lab(ax + 200, ay - 204, "the Altar Stone", ta + .7, GOLD, 34, "start")]
    st = hero_base("dusk")
    st.update(cam=CAM, els=els)
    return st


def s1z_add():
    """The push-in on the slab: about five metres long, six tonnes."""
    tl, tt = T("s1z", "About five metres"), T("s1z", "six tonnes")
    top, (ax, ay) = altar_pts()
    # a dimension along the slab's top, end to end (the slab runs across the axis)
    p0 = ((top[0][0] + top[3][0]) / 2, (top[0][1] + top[3][1]) / 2)
    p1 = ((top[1][0] + top[2][0]) / 2, (top[1][1] + top[2][1]) / 2)
    if p0[0] > p1[0]:
        p0, p1 = p1, p0
    els = [ln([p0, p1], tl, "#fff1c8", 2.5, dur=.6), ln([(p0[0], p0[1] - 7), (p0[0], p0[1] + 7)], tl, "#fff1c8", 2.5, draw=False),
           ln([(p1[0], p1[1] - 7), (p1[0], p1[1] + 7)], tl + .5, "#fff1c8", 2.5, draw=False)]
    els += [lab(ax - 120, ay + 70, "about 5 m", tl + .5, GOLD, 30, "end", fx="pop"), lab(ax + 120, ay + 70, "6 tonnes", tt, GOLD, 30, "start", fx="pop")]
    return els



# ================================================================== cold open: the map and the question
VGB = View(-11.0, 2.4, 49.6, 59.2, (90, 120, 1600, 680))
STH = (-1.826, 51.179)        # Stonehenge
CAITH = (-3.35, 58.45)        # Caithness
PRES = (-4.73, 51.97)         # the Preseli Hills (Carn Goedog)
WWOODS = (-1.77, 51.40)       # West Woods


def slab_icon(x, y, w, at, c=ALTAR, fx="pop", tilt=-8):
    """A small slab in three-quarter view (the Altar Stone as an icon)."""
    h, d = w * .2, w * .16
    P = [(x - w / 2, y), (x + w / 2, y), (x + w / 2 + d, y - d * .8), (x - w / 2 + d, y - d * .8)]
    els = [poly(rot(P, x, y, tilt), mix(c, "#ffffff", .25), "rgba(255,255,230,.6)", 1.2, 0),
           poly(rot([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x - w / 2, y + h)], x, y, tilt), c, "rgba(255,255,230,.5)", 1.2, 0)]
    return [grp(els, at, fx)]


def s2():
    """Map of Great Britain: a magnifier on a chip of the stone, tiny crystals glinting (2024); a gold line from the far north-east of
    Scotland down to Stonehenge, more than 700 km."""
    v = VGB
    tc, tn, tk = T("s2", "tiny crystals"), T("s2", "far north-east"), T("s2", "more than seven")
    sx, sy = v.p(*STH)
    cx, cy = v.p(*CAITH)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    mx, my, mr = 330, 420, 150
    els += [circ(mx, my, mr, "rgba(14,12,10,.94)", GOLD, 4, tc - .5, fx="pop"),
            ln([(mx + mr * .72, my + mr * .72), (mx + mr * 1.12, my + mr * 1.12)], tc - .4, GOLD, 13, draw=False)]
    els += [poly(blob(mx, my + 8, 100, 64, 16, .2, 3), ALTAR, "rgba(220,235,190,.6)", 2, tc - .3, fx="pop")]
    rr = random.Random(9)
    for k in range(16):
        a_, d_ = rr.uniform(0, 2 * math.pi), rr.uniform(0, 1) ** .5
        x, y = mx + math.cos(a_) * d_ * 78, my + 8 + math.sin(a_) * d_ * 46
        z = rr.uniform(6, 11)
        els.append(poly([(x, y - z), (x + z * .6, y), (x, y + z * .8), (x - z * .6, y)], rr.choice(["#ffe9b0", "#fff6dc", "#f2c98e", "#ffd2a0"]),
                        "#ffffff", .8, tc + .1 + .07 * k, fx="pop"))
    els += [lab(mx, my + mr + 56, "tiny crystals", tc + .4, GOLD, 30)] + chip(mx, my - mr - 40, "2024", GOLD, tc + .2, 26)
    els += [pin(cx, cy, "north-east Scotland", tn - .2, GOLD, "start", 22, 8)]
    els += slab_icon(cx - 4, cy + 30, 46, tn + .1)
    els += [ln([(cx, cy + 40), (cx + 30, (cy + sy) / 2 - 40), (sx, sy)], tn + .4, GOLD, 4.5, dur=2.2, curve=True),
            gl(sx, sy, 90, tn + 2.4, .6, "lamp"), pin(sx, sy, "Stonehenge", tn + 2.4, GOLD, "start", 22, 8)]
    lx, ly = v.p(1.3, 55.0)
    els += [lab(lx, ly, "more than", tk, GOLD, 30), lab(lx, ly + 40, "700 km", tk + .1, GOLD, 44, st="serif")]
    return {"base": "map", "cam": CAM, "els": els}


def s3_add():
    """The question over the hero, as the dusk deepens: a lilac question mark over the Altar Stone, 'who?' and 'why?'."""
    tq, tw = T("s3", "How did this"), T("s3", "who built")
    ax, ay = altar_xy()
    return [rect(-60, -60, 1900, 1120, "rgba(14,10,30,.3)", at=max(0, tq - .3), dur=1.2)] + qmark(ax, ay - 160, tq + .4, 120) + [
        lab(ax - 470, ay - 300, "who?", tw, LILAC, 46, st="serif", fx="pop"), lab(ax + 500, ay - 300, "why?", tw + 1.0, LILAC, 46, st="serif", fx="pop")]


# ================================================================== CHAPTER 1 · Who built it, and when?
FAR_CAM = Cam3(AZ(AX + 30, 128.0) + (1.7,), AX + 210, 1500, 1050, 505)


def barrow(x, y, w, at=-1, c="#2f3826"):
    return poly(E(x, y, w / 2, w * .12, 18, 180, 360), c, "rgba(255,236,206,.15)", 1, at)


def s5():
    """Salisbury Plain in the morning: long chalk downs, barrows on the skyline, Stonehenge small on the plain; a lilac claim floats
    above it: far older?"""
    tf = T("s5", "far older")
    cam = FAR_CAM
    els = [rect(-60, cam.hy, 1900, 600, "#4f5c38", at=-1),
           poly([(-60, 560), (300, 540), (700, 556), (1100, 548), (1500, 560), (1840, 552), (1840, 1000), (-60, 1000)], "#5d6b40", at=-1, curve=True),
           poly([(-60, 700), (500, 668), (900, 690), (1400, 664), (1840, 690), (1840, 1000), (-60, 1000)], "#6b7a48", at=-1, curve=True),
           rect(-60, 640, 1900, 400, "rgba(0,0,0,.08)", at=-1)]
    els += [barrow(x, cam.hy - 2, w) for x, w in ((180, 70), (260, 54), (520, 60), (1460, 66), (1540, 48), (1650, 58))]
    els += render(monument("ruin"), cam, (95, 16), "day", -1, texture=False)
    els += [lab(330, 760, "Salisbury Plain", .6, BONE, 34, "start", st="serif")]
    els += [rect(830, 250, 460, 74, "rgba(201,193,238,.08)", LILAC, 2.5, 37, tf, fx="pop", style="claimed"),
            lab(1060, 300, "far older?", tf + .1, LILAC, 34, fx="pop"), ln([(1060, 324), (1060, 450)], tf + .3, LILAC, 2, "claimed", dur=.5)]
    els += qmark(1370, 330, tf + .6, 80, halo=False)
    return {"base": "sky", "tod": "day", "ground": cam.hy, "sun": [300, 190, 26], "groundc": "#4f5c38",
            "ridges": [{"y": cam.hy - 30, "a": 40, "c": "#6f7f8c", "seed": 2}, {"y": cam.hy - 6, "a": 22, "c": "#56653f", "seed": 6}],
            "cam": CAM, "els": els}


def car60(x, y, s, at):
    """A small 1960s car in side view (s = its length)."""
    P = lambda a, b: (x + a * s, y - b * s)
    body = [P(-.5, .1), P(-.48, .26), P(-.3, .3), P(-.18, .46), P(.16, .46), P(.3, .3), P(.48, .26), P(.5, .1)]
    els = [poly(body, "#8a3c2c", "rgba(255,230,200,.5)", 1.5, 0, curve=True),
           poly([P(-.15, .32), P(-.09, .42), P(.12, .42), P(.18, .32)], "#bcd6e0", at=0, op=.7),
           circ(*P(-.3, .1), .09 * s, "#1a1714", "#777", 1.5, 0), circ(*P(.3, .1), .09 * s, "#1a1714", "#777", 1.5, 0)]
    return [grp(els, at, "rise")]


def spear_man(x, y, h, at, face=1):
    return fig(x, y, h, at, "#2a2018", arms="up", face=face) + [ln([(x + face * .26 * h, y - .2 * h), (x + face * .14 * h, y - 1.3 * h)], at, "#6b4a30", 3.5, draw=False)]


def s6():
    """The car park, 1966: a cut through the chalk with three large postholes; pine posts rise above them, raised by hunter-gatherers
    between 8,000 and 10,000 years ago."""
    t0, th, tp, tg = T("s6", "In nineteen sixty-six"), T("s6", "holes of large"), T("s6", "raised by"), T("s6", "between eight")
    gy = 440
    els = [rect(-60, gy, 1900, 600, CHALK, at=-1), rect(-60, gy, 1900, 22, "#5a4630", at=-1), rect(-60, gy - 6, 1900, 8, TURF, at=-1)]
    rr = random.Random(4)
    els += [dot(round(rr.uniform(100, 1680), 1), round(rr.uniform(gy + 40, 790), 1), round(rr.uniform(1.5, 4), 1), "#a89c84", -1) for _ in range(70)]
    els += [ln([(80, gy + 120 + 60 * k), (1700, gy + 110 + 60 * k)], -1, "rgba(150,140,120,.35)", 1.5, draw=False) for k in range(5)]
    els += car60(300, gy - 6, 190, t0 + .2) + chip(300, gy - 150, "car park, 1966", AMBER, t0 + .5, 26)
    xs = (640, 960, 1280)
    for k, x in enumerate(xs):
        hole = [(x - 62, gy + 16), (x - 54, gy + 130), (x - 30, gy + 172), (x + 30, gy + 172), (x + 54, gy + 130), (x + 62, gy + 16)]
        els.append(poly(hole, "#4a3a2a", "rgba(40,30,20,.8)", 2, th + .25 * k, fx="pop", curve=True))
    els += [lab(960, gy + 230, "postholes", th + .9, "#3a2c1e", 28, halo=False)]
    for k, x in enumerate(xs):
        top = 150 + 20 * (k % 2)
        trunk = [(x - 26, gy + 160), (x + 26, gy + 160), (x + 20, top), (x - 20, top)]
        els.append(grp([poly(trunk, "#8a5a32", "rgba(255,220,170,.55)", 1.5, 0),
                        ln([(x - 8, gy + 150), (x - 6, top + 10)], 0, "rgba(255,226,180,.35)", 3, draw=False),
                        ln([(x - 22, top + 60), (x + 22, top + 66)], 0, "rgba(60,30,10,.6)", 3, draw=False),
                        ln([(x - 22, top + 120), (x + 22, top + 114)], 0, "rgba(60,30,10,.6)", 3, draw=False)], tp + .3 * k, "rise"))
    els += [lab(1280, 128, "pine posts", tp + 1.0, GOLD, 30)]
    els += spear_man(1460, gy - 6, 190, tp + 1.2) + spear_man(1560, gy - 6, 176, tp + 1.4, face=-1)
    els += [lab(1510, 210, "hunter-gatherers", tp + 1.6, BONE, 28)]
    els += chip(560, 170, "8,000 to 10,000 years ago", GOLD, tg, 30)
    return {"base": "sky", "tod": "day", "ground": gy, "sun": [1650, 200, 24], "cam": CAM, "els": els}


PLAN_C, PLAN_K = (889, 470), 5.45          # the earthwork plan: its centre on the panel, units per metre


def PP(a, r, c=PLAN_C, k=PLAN_K):
    x, y = AZ(a, r)
    return (c[0] + k * x, c[1] - k * y)


def arc_pts(a0, a1, r, n=60, c=PLAN_C, k=PLAN_K):
    return [PP(a0 + (a1 - a0) * i / n, r, c, k) for i in range(n + 1)]


def s7():
    """Plan from above: the ditch draws itself round (a gap for the entrance in the north-east, a small one in the south), the bank
    inside it; 110 m across."""
    t0, tb, td = T("s7", "ring-shaped ditch"), T("s7", "and bank"), T("s7", "a hundred and ten")
    els = [ln(arc_pts(0, 360, 55, 120), .3, "rgba(233,220,192,.3)", 2, "inferred", dur=1.2)]
    for a0, a1 in ((AX + 7, 168), (172, AX + 353)):
        els.append(ln(arc_pts(a0, a1, 55), t0, "#151a0f", 24, dur=1.6))
        els.append(ln(arc_pts(a0, a1, 55), t0 + .2, "rgba(255,236,206,.18)", 2, dur=1.6))
    for a0, a1 in ((AX + 9, 166), (174, AX + 351)):
        els.append(ln(arc_pts(a0, a1, 50.5), tb, "#d9d0b8", 15, dur=1.6, op=.7))
    x0, y0 = PP(270, 55)
    x1, y1 = PP(90, 55)
    els += [{"k": "dim", "x1": round(x0, 1), "y1": round(y0, 1), "x2": round(x1, 1), "y2": round(y1, 1), "t": "110 m", "c": GOLD, "fx": "draw", "dur": 1.0,
             "in": round(td, 2), "ly": -18}]
    lx, ly = PP(AX - 18, 55)
    els += [ln([(lx + 8, ly - 6), (1280, 190)], tb + .4, BONE, 1.6, dur=.4), lab(1290, 180, "ditch and bank", tb + .6, BONE, 30, "start")]
    els += [{"k": "scale", "x": 130, "y": 760, "w": round(PLAN_K * 50, 1), "t": "50 m", "in": .6}]
    return {"base": "plan", "bg": "#29331f", "cam": CAM, "els": els}


def antler(x, y, s, ang, at, c="#dcc79c", fx=None, worn=False):
    """A red deer antler lying (side view): a curved beam with tines; s = its length, ang = its turn in degrees."""
    beam = [(0, 0), (.25, -.08), (.55, -.1), (.8, -.04), (1.0, .06)]
    tines = [((.1, -.05), (.2, -.32)), ((.32, -.09), (.42, -.36)), ((.62, -.09), (.7, -.3))]
    if worn:
        tines = tines[:1] + [((.32, -.09), (.36, -.2))]
    P = lambda q: rot([(x + q[0] * s, y + q[1] * s)], x, y, ang)[0]
    els = [ln([P(q) for q in beam], 0, "#3a2c1c", max(5, s * .09), draw=False, curve=True),
           ln([P(q) for q in beam], 0, c, max(3, s * .065), draw=False, curve=True)]
    for a_, b_ in tines:
        els += [ln([P(a_), P(b_)], 0, "#3a2c1c", max(4, s * .06), draw=False), ln([P(a_), P(b_)], 0, c, max(2.5, s * .04), draw=False)]
    els += [circ(*P((0, 0)), s * .05, "#b8a27a", "#3a2c1c", 1.5, 0)]
    return [grp(els, at, fx or "pop")]


def s8():
    """The ditch in section: steep sides in white chalk, the bank of spoil beside it; on its floor, red deer antlers, more than a
    hundred, many worn as picks; a digger kneels at the bottom, working the chalk with one."""
    t0, ta = T("s8", "On the floor"), T("s8", "red deer")
    gy, fy = 330, 640
    els = [rect(-60, gy, 1900, 700, CHALK, at=-1), rect(-60, gy - 6, 1900, 10, TURF, at=-1)]
    rr = random.Random(8)
    els += [dot(round(rr.uniform(100, 1680), 1), round(rr.uniform(gy + 20, 790), 1), round(rr.uniform(1.5, 3.5), 1), "#b0a488", -1) for _ in range(60)]
    cut = [(470, gy), (560, fy), (1220, fy), (1320, gy)]
    els += [poly(cut, "#8c8270", "rgba(60,50,40,.7)", 2, -1), poly([(560, fy - 40), (1220, fy - 40), (1220, fy), (560, fy)], "#7a705e", at=-1)]
    els += [poly([(120, gy + 4), (220, 250), (330, 236), (440, gy + 4)], "#d8cfb6", "rgba(120,110,90,.6)", 1.5, -1, curve=True), lab(280, 210, "bank", .6, DIM, 26)]
    spots = [(640, 2), (720, -8), (820, 6), (900, -4), (980, 10), (1070, -10), (1150, 4), (690, 14), (1010, -2)]
    for k, (x, a) in enumerate(spots):
        els += antler(x, fy - 14 - (k % 3) * 6, 120 + 20 * (k % 2), a, ta + .18 * k, worn=(k % 3 == 0))
    # the digger, kneeling at the wall with an antler pick
    kx = 1150
    els += [grp([circ(kx, fy - 150, 16, "#2a2018", at=0), poly([(kx - 22, fy - 132), (kx + 18, fy - 132), (kx + 26, fy - 70), (kx - 10, fy - 60)], "#2a2018", at=0),
                 poly([(kx - 12, fy - 64), (kx + 30, fy - 66), (kx + 34, fy - 4), (kx + 14, fy - 4)], "#2a2018", at=0),
                 ln([(kx + 10, fy - 120), (kx + 60, fy - 110), (kx + 96, fy - 150)], 0, "#2a2018", 8, draw=False)], t0 + .3, "rise")]
    els += antler(kx + 70, fy - 168, 80, -50, t0 + .5, worn=True)
    els += chip(889, 730, "more than 100 antlers", GOLD, ta + 1.6, 30)
    els += [lab(1420, 470, "antler picks", ta + 1.2, "#3a2c1e", 30, halo=False)]
    return {"base": "sky", "tod": "day", "ground": gy, "sun": [1600, 200, 22], "cam": CAM, "els": els}


def s9():
    """Left: an antler and a clock whose hand starts sweeping (radiocarbon); right: a house's foundations in section with a dated
    receipt in the concrete; then the date: about 3000 BCE."""
    t0, tr, td = T("s9", "Antler holds"), T("s9", "dated receipt"), T("s9", "The ditch was dug")
    els = antler(170, 520, 330, -12, t0 - .2)
    cx, cy, r = 600, 430, 120
    els += [circ(cx, cy, r, "rgba(18,13,10,.9)", GOLD, 4, t0 + .4, fx="pop")]
    els += [ln([(cx + (r - 10) * math.sin(math.radians(a)), cy - (r - 10) * math.cos(math.radians(a))), (cx + (r - 24) * math.sin(math.radians(a)), cy - (r - 24) * math.cos(math.radians(a)))],
               t0 + .5, GOLD, 3, draw=False) for a in range(0, 360, 30)]
    els += [ln(arc_pts(0, 300, 1, 40, (cx, cy), r * .72), t0 + .9, "rgba(242,201,142,.6)", 8, dur=3.5),
            ln([(cx, cy), (cx, cy - r * .7)], t0 + .7, "#fff1c8", 5, draw=False), circ(cx, cy, 8, GOLD, at=t0 + .7)]
    els += [lab(450, 640, "radiocarbon clock", t0 + 1.2, GOLD, 30)]
    # the foundations
    gx, gyy = 1120, 470
    els += [rect(980, gyy, 560, 270, "#5a4632", at=-1), rect(980, gyy, 560, 12, TURF, at=-1),
            poly([(1030, gyy), (1030, gyy - 170), (1260, gyy - 290), (1490, gyy - 170), (1490, gyy)], "rgba(233,220,192,.12)", BONE, 2.5, tr - 1.6),
            rect(1010, gyy + 20, 500, 110, "#8f8a82", "#cfc8bc", 2, 2, tr - 1.4)]
    els += [grp([rect(1200, gyy + 44, 120, 64, "#f6efe0", "#bfb6a6", 1.5, 2, 0)] +
                [ln([(1214, gyy + 60 + 12 * k), (1300 - 14 * (k % 2), gyy + 60 + 12 * k)], 0, "#7a7062", 2, draw=False) for k in range(4)], tr - .4, "pop"),
            gl(1260, gyy + 76, 120, tr - .2, .5, "lamp"), lab(1260, gyy + 190, "a dated receipt", tr, GOLD, 30)]
    els += chip(889, 180, "about 3000 BCE", GOLD, td + .5, 34)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s10_add():
    """On the plan: 56 holes just inside the bank, small bluestones (probably) in many of them; cremation burials in and around them
    and along the ditch, 3000 to 2500 BCE."""
    th, tb, tc = T("s10", "a ring of fifty-six"), T("s10", "first bluestones"), T("s10", "burnt bones")
    els = []
    rb = random.Random(3)
    for k in range(56):
        a = AX + 360 * k / 56
        x, y = PP(a, 43.3)
        els.append(circ(x, y, 6.5, "#0f130b", "rgba(255,236,206,.5)", 1.2, th + .02 * k, fx="pop"))
    for k in range(56):
        if rb.random() < .62:
            a = AX + 360 * k / 56
            x, y = PP(a, 43.3)
            els.append(rect(x - 4.5, y - 7, 9, 14, "rgba(111,128,144,.9)", BLUS_L, 1.2, 2, tb + .015 * k, fx="pop", style="inferred"))
    for k in range(38):
        a = rb.uniform(0, 360)
        rr_ = rb.choice([43.3 + rb.uniform(-3, 3), 55 + rb.uniform(-1.5, 1.5)])
        x, y = PP(a, rr_)
        els.append(dot(round(x, 1), round(y, 1), 4, "#f0b06a", tc + .03 * k))
    hx, hy_ = PP(304.3, 43.3)
    els += [ln([(hx - 6, hy_ - 4), (420, 250)], th + 1.4, BONE, 1.6, dur=.4), lab(410, 240, "56 holes", th + 1.6, BONE, 30, "end")]
    bx, by = PP(240.0, 43.3)
    els += [ln([(bx - 6, by + 4), (430, 660)], tb + .6, BLUS_L, 1.6, dur=.4), lab(420, 680, "the first bluestones?", tb + .8, BLUS_L, 28, "end")]
    cx_, cy_ = PP(AX + 80, 55)
    els += [ln([(cx_ + 10, cy_ + 6), (1330, 620)], tc + .8, "#f0b06a", 1.6, dur=.4), lab(1340, 620, "cremations", tc + 1.0, "#f0b06a", 30, "start")]
    els += chip(1450, 680, "3000 to 2500 BCE", "#f0b06a", tc + 1.4, 26)
    return els


BUILD_CAM = Cam3(AZ(AX + 70, 48.0) + (20.0,), AX + 250, 1120, 889, 130)


def s11():
    """The monument as built about 2500 BCE (a 3-D view of the full plan in daylight): the thirty uprights rise round the ring, the
    lintels settle on them, then the five trilithons rise, the tallest at the back; people for scale."""
    t0, tl, tt = T("s11", "came the giants"), T("s11", "capped with lintels"), T("s11", "five towering")
    tc = T("s11", "Then, around")
    cam = BUILD_CAM
    B = [b for b in monument("whole") if b["kind"] == "sarsen"]
    rise = {}
    for b in B:
        tg = b["tag"]
        if tg.startswith("u"):
            rise[tg] = t0 + .07 * ((int(tg[1:]) + 8) % 30)
        elif tg.startswith("l"):
            rise[tg] = tl + .05 * ((int(tg[1:]) + 8) % 30)
        elif tg.startswith("t"):
            n = int(re.sub(r"\D", "", tg))
            rise[tg] = tt + .25 * ((n - 51) // 2) + (.5 if tg.startswith("tl") else 0)
    els = [rect(-60, cam.hy, 1900, 900, "#55623b", at=-1)]
    els += ground_ring(cam, 52, -1, "rgba(232,214,170,.3)", 3) + ground_ring(cam, 55.5, -1, "rgba(20,24,12,.5)", 6)
    els += render(B, cam, (205, 26), "day", -1, rise=rise)
    for k, (a, r_) in enumerate(((AX + 8, 21.0), (AX + 14, 22.0), (AX + 2, 20.5))):
        px, py, d = cam.p(AZ(a, r_) + (0,))
        els += fig(px, py, cam.f * 1.7 / d, t0 + .3 + .2 * k, "#2a2018")
    pxl, pyl, d = cam.p(AZ(AX + 8, 21.0) + (0,))
    els += [lab(pxl + 40, pyl + 34, "a person", t0 + 1.0, BONE, 24, "start")]
    els += chip(889, 120 + 70, "about 2500 BCE", GOLD, tc + .2, 30)
    lx, ly, _ = cam.p(AZ(ring_az(20), RING_R) + (4.6,))
    els += [lab(lx - 30, ly - 40, "30 sarsens", tl + 1.0, BONE, 30, "end")]
    gx, gy_, _ = cam.p(AZ(AX + 242, 7.0) + (7.2,))
    els += [lab(gx + 60, gy_ - 50, "5 trilithons", tt + 1.6, GOLD, 30, "start")]
    return {"base": "sky", "tod": "day", "ground": cam.hy, "sun": [1500, 120, 22], "groundc": "#55623b",
            "ridges": [{"y": cam.hy - 10, "a": 18, "c": "#7a8a96", "seed": 3}, {"y": cam.hy - 1, "a": 10, "c": "#5d6b44", "seed": 7}],
            "cam": CAM, "els": els}


def s12():
    """Joints like a carpenter's: the tops of two uprights with knobs (tenons), a lintel coming down with sockets (mortises) to fit
    them; at its end a tongue that slots into the groove of the next lintel; a timber joint beside it."""
    t0, tj, tg = T("s12", "Their builders"), T("s12", "pegs"), T("s12", "grooves")
    S_, L_, D_ = "#9c9184", "#e0cfac", "#5e564c"
    els = []
    for x in (300, 720):
        els += [poly([(x - 92, 780), (x + 92, 780), (x + 86, 440), (x - 86, 440)], S_, "rgba(40,30,20,.6)", 1.5, -1),
                poly([(x + 86, 440), (x + 120, 420), (x + 126, 760), (x + 92, 780)], D_, "rgba(40,30,20,.6)", 1.2, -1),
                poly([(x - 86, 440), (x + 86, 440), (x + 120, 420), (x - 52, 420)], L_, "rgba(40,30,20,.5)", 1.2, -1),
                grp([poly([(x - 24, 432), (x + 24, 432), (x + 22, 392), (x - 22, 392)], L_, "rgba(40,30,20,.7)", 1.5, 0),
                     poly([(x + 24, 432), (x + 34, 426), (x + 32, 388), (x + 22, 392)], D_, "rgba(40,30,20,.7)", 1.2, 0)], tj - .3, "pop")]
    lin = [(170, 300), (880, 300), (880, 200), (170, 200)]
    els += [grp([poly(lin, S_, "rgba(40,30,20,.6)", 1.5, 0), poly([(880, 300), (914, 280), (914, 182), (880, 200)], D_, "rgba(40,30,20,.6)", 1.2, 0),
                 poly([(170, 200), (880, 200), (914, 182), (204, 182)], L_, "rgba(40,30,20,.5)", 1.2, 0),
                 rect(276, 270, 50, 30, "#2e2620", "rgba(255,236,206,.45)", 1.5, 4, 0), rect(696, 270, 50, 30, "#2e2620", "rgba(255,236,206,.45)", 1.5, 4, 0)],
                t0 + .2, "pop"),
            arr([(510, 316), (510, 384)], t0 + .7, BONE, 3, dur=.35, curve=False)]
    els += [ln([(300, 396), (450, 520)], tj + .2, GOLD, 1.6, dur=.3), ln([(720, 396), (570, 520)], tj + .2, GOLD, 1.6, dur=.3),
            lab(510, 560, "peg and socket", tj + .4, GOLD, 30)]
    gx, gy_ = 1130, 230
    els += [poly([(gx, gy_), (gx + 180, gy_), (gx + 180, gy_ + 34), (gx + 222, gy_ + 50), (gx + 180, gy_ + 66), (gx + 180, gy_ + 100), (gx, gy_ + 100)],
                 S_, "rgba(40,30,20,.6)", 1.5, tg - .2, fx="pop"),
            poly([(gx + 232, gy_), (gx + 440, gy_), (gx + 440, gy_ + 100), (gx + 232, gy_ + 100), (gx + 232, gy_ + 66), (gx + 274, gy_ + 50),
                  (gx + 232, gy_ + 34)], S_, "rgba(40,30,20,.6)", 1.5, tg, fx="pop"),
            lab(gx + 220, gy_ + 160, "tongue and groove", tg + .3, GOLD, 30)]
    wx, wy = 1350, 560
    els += [grp([rect(wx - 30, wy, 60, 190, WOOD, "rgba(255,220,170,.4)", 1.5, 2, 0), rect(wx - 12, wy - 30, 24, 32, WOOD, "rgba(255,220,170,.4)", 1.5, 2, 0),
                 rect(wx - 170, wy - 92, 340, 58, mix(WOOD, "#ffffff", .1), "rgba(255,220,170,.4)", 1.5, 2, 0),
                 rect(wx - 14, wy - 48, 28, 14, WOOD_D, at=0)], tg + .6, "pop"),
            lab(wx, wy + 230, "a carpenter's joint", tg + .9, BONE, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def mini_plan(cx, cy, at, kind, r=95):
    """A small plan: the sarsen ring faint, the horseshoe faint, the bluestones in blue as arranged at one stage."""
    els = [circ(cx, cy, r, "none", "rgba(203,188,168,.45)", 6, at), circ(cx, cy, r, "none", "rgba(203,188,168,.25)", 12, at)]
    for k in range(5):
        a = AX + 180 + (-120, -60, 0, 60, 120)[k]
        x, y = cx + .55 * r * math.sin(math.radians(a)), cy - .55 * r * math.cos(math.radians(a))
        els.append(rect(x - 9, y - 9, 18, 18, "rgba(203,188,168,.4)", at=at, r=2))
    def ring_dots(rx, ry, n, a0=0, a1=360, t=at):
        out = []
        for k in range(n):
            a = math.radians(a0 + (a1 - a0) * k / max(1, n - (0 if a1 - a0 < 360 else 0)))
            out.append(dot(round(cx + rx * math.sin(a), 1), round(cy - ry * math.cos(a), 1), 4.2, BLUS_L, round(t + .02 * k, 2)))
        return out
    if kind == "arc":
        els += ring_dots(.82 * r, .82 * r, 26, AX + 60, AX + 300) + ring_dots(.72 * r, .72 * r, 24, AX + 60, AX + 300)
    elif kind == "oval":
        els += ring_dots(.8 * r, .8 * r, 30) + ring_dots(.32 * r, .45 * r, 14)
    else:
        els += ring_dots(.8 * r, .8 * r, 30) + ring_dots(.38 * r, .38 * r, 12, AX + 60, AX + 300)
    return els


def s13():
    """Four small plans in a row, the bluestones (blue) rearranged each time: a double arc, a circle and an oval, a circle and a
    horseshoe; then two rings of pits round the last: the last pits, about 1600 BCE."""
    t0, tl = T("s13", "rearranged"), T("s13", "the last pits")
    cy = 450
    xs = (250, 640, 1030, 1430)
    kinds = ("arc", "oval", "shoe", "shoe")
    els = [lab(889, 190, "rearranged, again and again", t0, BLUS_L, 32, st="serif")]
    for k, (x, kd) in enumerate(zip(xs, kinds)):
        els += mini_plan(x, cy, t0 + .4 + .9 * k, kd)
        if k:
            els += [arr([(xs[k - 1] + 125, cy), (x - 125, cy)], t0 + .2 + .9 * k, BONE, 2.5, dur=.3, curve=False)]
    for rr_, n in ((150, 30), (120, 30)):
        els += [circ(round(1430 + rr_ * math.sin(2 * math.pi * k / n), 1), round(cy - rr_ * math.cos(2 * math.pi * k / n), 1), 5, "#0f0d0a", GOLD, 1.5,
                     tl + .02 * k + (.4 if rr_ == 120 else 0), fx="pop") for k in range(n)]
    els += [lab(1430, cy + 210, "the last pits", tl + .8, GOLD, 28)] + chip(1430, cy + 262, "about 1600 BCE", GOLD, tl + 1.1, 26)
    return {"base": "plan", "bg": "#29331f", "north": False, "cam": CAM, "els": els}


def helix(x, y, h, at, c=BLUE):
    els = []
    for k in range(9):
        t = k / 8
        yy = y - h * t
        dx = 22 * math.sin(t * 2 * math.pi * 1.5)
        els.append(ln([(x - dx, yy), (x + dx, yy)], 0, "rgba(159,208,255,.6)", 2, draw=False))
    els += [ln([(x + 22 * math.sin(k / 30 * 3 * math.pi), y - h * k / 30) for k in range(31)], 0, c, 3, draw=False, curve=True),
            ln([(x - 22 * math.sin(k / 30 * 3 * math.pi), y - h * k / 30) for k in range(31)], 0, c, 3, draw=False, curve=True)]
    return [grp(els, at, "pop")]


def boat(x, y, s, at, c="#4a3422"):
    """A skin boat with a family aboard (s = its length)."""
    P = lambda a, b: (x + a * s, y + b * s)
    els = [poly([P(-.52, -.12), P(-.4, .06), P(.4, .06), P(.54, -.14), P(.32, -.02), P(-.32, -.02)], c, "rgba(255,230,190,.55)", 1.4, 0, curve=True),
           ln([P(-.6, .1), P(.62, .1)], 0, "rgba(159,208,255,.5)", 2, draw=False)]
    for k, (a, h) in enumerate(((-.24, .34), (-.06, .3), (.1, .2), (.24, .33))):
        els += fig(P(a, -.02)[0], P(a, -.02)[1], h * s, 0, "#e8d6b8", fx=None)
    return [grp(els, at, "pop")]


XT = lambda yr: round(160 + (yr + 4500) / 3100 * 1460, 1)       # 4500 BCE to 1400 BCE (BCE negative)


def s14():
    """A timeline from 4500 to 1400 BCE: farmers arrive about 4000 BCE (a boat, a DNA helix), then the ditch, the sarsens, the last
    pits; a bracket: some fourteen centuries."""
    t0, tn = T("s14", "Ancient DNA"), T("s14", "Not one Stonehenge")
    ay = 560
    els = [axis(160, 1620, ay, [(XT(y_), "%d" % -y_) for y_ in (-4000, -3500, -3000, -2500, -2000, -1500)], .2, "BCE")]
    els += boat(XT(-4000) - 10, ay - 40, 220, t0 + .6) + helix(XT(-4000) + 170, ay - 30, 130, t0 + .2)
    els += [lab(XT(-4000), ay - 200, "farmers arrive", t0 + 1.2, BONE, 30)]
    marks = [(-3000, "ditch", t0 + 2.4), (-2500, "sarsens", t0 + 2.9), (-1600, "last pits", t0 + 3.4)]
    for yr_, t_, at in marks:
        els += [ln([(XT(yr_), ay - 60), (XT(yr_), ay)], at, GOLD, 3, dur=.3), dot(XT(yr_), ay - 64, 8, GOLD, at), lab(XT(yr_), ay - 90, t_, at + .1, GOLD, 28)]
    els += [{"k": "band", "x0": XT(-3000), "x1": XT(-1600), "y": ay - 12, "h": 14, "c": GOLD, "op": .5, "in": round(tn, 2), "dur": 1.2}]
    els += bracket(XT(-3000), XT(-1600), ay - 160, tn + .4, "some 14 centuries", GOLD, up=False, size=30, ty=ay - 184)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}



# ================================================================== CHAPTER 2 · Bluestones from Wales
VBI = View(-10.6, 1.8, 50.2, 58.7, (870, 120, 800, 680))


def merlin(x, y, h, at, robe="#4a3a7a", fx="rise"):
    """A robed figure with a staff (the wizard of the tale, as a miniature would show him)."""
    P = lambda a, b: (x + a * h, y - b * h)
    els = [poly([P(-.17, 0), P(.17, 0), P(.1, .62), P(-.1, .62)], robe, "rgba(255,230,160,.6)", 1.2, 0),
           circ(*P(0, .7), .07 * h, "#e8d6b8", at=0), poly([P(-.09, .74), P(.09, .74), P(0, 1.02)], robe, "rgba(255,230,160,.6)", 1, 0),
           ln([P(.16, .58), P(.3, .48)], 0, robe, max(3, .05 * h), draw=False), ln([P(.32, 0), P(.3, .82)], 0, "#8a5a32", max(3, .03 * h), draw=False),
           circ(*P(.3, .84), .03 * h, "#ffe7a0", at=0)]
    return [grp(els, at, fx)]


def tiny_tril(x, y, h, at=0, c="#9a9a9a", e="rgba(30,25,20,.6)"):
    w = h * .7
    return [rect(x - w / 2, y - h, w * .3, h, c, e, 1, 1, at), rect(x + w / 2 - w * .3, y - h, w * .3, h, c, e, 1, 1, at),
            rect(x - w / 2 - 2, y - h - h * .16, w + 4, h * .16, c, e, 1, 1, at)]


def ring_icon(x, y, r, at, c=LILAC, style="claimed", n=12):
    els = [circ(x, y, r, "none", c, 2, 0, style=style)]
    for k in range(n):
        a = 2 * math.pi * k / n
        els.append(rect(x + r * math.cos(a) - 3.5, y + r * math.sin(a) - 6, 7, 12, c, at=0, op=.9))
    return [grp(els, at, "pop")]


def s15():
    """Left: a page of a medieval manuscript with a miniature (a robed figure with a staff before a ring of stones): Geoffrey of
    Monmouth, about 1136. Right: Britain and Ireland, the tale's route in lilac dots: from Africa to Ireland (giants, the Giants' Dance),
    from Ireland to Salisbury Plain (Merlin)."""
    t0, tg, ta = T("s15", "The wizard Merlin"), T("s15", "the Giants' Dance"), T("s15", "from Africa")
    v = VBI
    els = [rect(110, 130, 620, 600, "#e9dcc0", "#a88c5c", 3, 6, -1), rect(126, 146, 588, 568, "none", "rgba(120,80,40,.5)", 1.5, 4, -1)]
    els += [{"k": "glyphs", "x": 150, "y": 165, "w": 540, "h": 110, "rows": 6, "cols": 16, "kind": "latin", "c": "#5a3a22", "in": -1, "op": .75},
            {"k": "glyphs", "x": 150, "y": 600, "w": 540, "h": 104, "rows": 5, "cols": 16, "kind": "latin", "c": "#5a3a22", "in": -1, "op": .75},
            rect(150, 290, 540, 296, "#284a7a", "#c99a3a", 5, 3, -1), rect(150, 490, 540, 96, "#3e6a3a", at=-1),
            lab(166, 210, "S", -1, "#9a2a1e", 70, "start", st="serif", halo=False)]
    for k, x in enumerate((420, 500, 580, 640)):
        els += tiny_tril(x, 530 - 8 * (k % 2), 76 - 6 * (k % 2), -1, "#b9b2a6")
    els += merlin(270, 570, 220, -1)
    els += [lab(330, 776, "Geoffrey of Monmouth", .5, BONE, 30)] + chip(640, 766, "about 1136", GOLD, .8, 24)
    ix, iy = v.p(-7.6, 53.3)
    sx, sy = v.p(*STH)
    bx, by = v.p(-6.6, 50.2)
    els += [{"k": "map", "land": v.land(), "in": -1}]
    els += [arr([(bx, by + 20), (bx - 30, (by + iy) / 2 + 40), (ix, iy + 40)], ta - .4, LILAC, 3, "claimed", dur=1.2),
            lab(bx + 20, by - 10, "giants, from Africa", ta, LILAC, 26, "start")]
    els += ring_icon(ix, iy, 28, tg) + [lab(ix - 10, iy - 52, "the Giants' Dance", tg + .2, LILAC, 26)]
    els += [arr([(ix + 34, iy + 6), ((ix + sx) / 2, iy + 20), (sx - 14, sy - 6)], t0 + 1.4, LILAC, 3, "claimed", dur=1.2),
            pin(sx, sy, "", t0 + 2.4, GOLD), lab(v.p(-4.6, 54.25)[0], v.p(-4.6, 54.25)[1], "Merlin", t0 + 2.0, LILAC, 30)]
    return {"base": "map", "cam": CAM, "els": els}


VSW = View(-5.8, -0.6, 50.3, 53.0, (560, 130, 1100, 640))


def bluestone_sample(x, y, rx, ry, at, seed=4):
    els = [poly(blob(x, y, rx, ry, 18, .14, seed), BLUS, BLUS_L, 2, 0, curve=True)]
    rr = random.Random(seed)
    for _ in range(26):
        a, d = rr.uniform(0, 2 * math.pi), rr.uniform(0, .8) ** .7
        els.append(dot(round(x + math.cos(a) * d * rx * .85, 1), round(y + math.sin(a) * d * ry * .8, 1), round(rr.uniform(3, 6), 1), "#e8eef2", 0, None))
    return [grp(els, at, "pop")]


def s16():
    """Map of southern Britain: a hand lens on a bluestone (Herbert Thomas, 1923); the Preseli Hills in west Wales, a solid gold line
    to Stonehenge, about 230 km."""
    t0, tp, tk = T("s16", "Herbert Thomas"), T("s16", "Preseli Hills"), T("s16", "about two hundred")
    v = VSW
    px, py = v.p(*PRES)
    sx, sy = v.p(*STH)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += bluestone_sample(300, 470, 150, 110, t0 - .4)
    els += [circ(300, 470, 128, "rgba(220,240,255,.12)", GOLD, 5, t0, fx="pop"), ln([(390, 560), (470, 640)], t0 + .1, GOLD, 14, draw=False),
            lab(300, 690, "a bluestone", t0 + .4, BLUS_L, 28)] + chip(300, 250, "Herbert Thomas, 1923", GOLD, t0 + .3, 26)
    els += [poly(blob(px, py, 46, 22, 14, .2, 6), "rgba(111,128,144,.6)", BLUS_L, 2, tp - .2, curve=True, fx="pop"),
            pin(px, py, "Preseli Hills", tp, BLUS_L, "end", -24, -26),
            ln([(px, py), ((px + sx) / 2, (py + sy) / 2 - 30), (sx, sy)], tp + .5, GOLD, 4.5, dur=1.4, curve=True),
            pin(sx, sy, "Stonehenge", tp + 1.6, GOLD, "start", 20, 8),
            lab((px + sx) / 2 + 20, (py + sy) / 2 - 70, "about 230 km", tk, GOLD, 32)]
    els += [{"k": "scale", "x": 1400, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": .8}]
    return {"base": "map", "cam": CAM, "els": els}


def pillar(x, base, w, h, at, c="#56606c", seed=1, fx=None, lean=0.0):
    """A column of dolerite seen from the side: lit left face, shaded right face, white spots, a broken top."""
    r = random.Random(seed)
    top = base - h
    lean = lean or r.uniform(-6, 6)
    tl = (x - w / 2 + lean, top + r.uniform(-14, 14))
    tr = (x + w / 2 + lean, top + r.uniform(-14, 14))
    els = [poly([(x - w / 2, base), (x + w / 2, base), tr, tl], c, "rgba(14,16,22,.7)", 1.4, 0),
           poly([(x + w * .18, base), (x + w / 2, base), tr, (x + w * .18 + lean, top + 4)], "#2b323c", at=0, op=.8),
           poly([tl, tr, (tr[0] + w * .1, tr[1] - 8), (tl[0] + w * .1, tl[1] - 8)], "#8e9aa8", at=0, op=.85)]
    for _ in range(int(h / 40)):
        els.append(dot(round(x + r.uniform(-.38, .1) * w + lean * .5, 1), round(r.uniform(top + 14, base - 10), 1), round(r.uniform(2, 3.5), 1), "#d6dde4", 0, None, op=.55))
    return [grp(els, at, fx)] if fx else els


def heather_hill(y0, at=-1):
    return [poly([(-60, y0 + 40), (300, y0 - 10), (700, y0 + 10), (1100, y0 - 30), (1500, y0 + 20), (1840, y0), (1840, 1000), (-60, 1000)], "#4a3a44", at=at, curve=True),
            poly([(-60, y0 + 140), (500, y0 + 110), (1000, y0 + 130), (1840, y0 + 100), (1840, 1000), (-60, 1000)], "#3a2e36", at=at, curve=True)]


def pencils(x, y, at):
    els = []
    for k in range(5):
        px = x + (k - 2) * 26
        h = 150 + 12 * (k % 2)
        els += [rect(px - 12, y - h, 24, h, "#e8b84a", "#7a5418", 1.5, 1, 0), poly([(px - 12, y - h), (px + 12, y - h), (px, y - h - 30)], "#e6c8a0", "#7a5418", 1.2, 0),
                poly([(px - 4, y - h - 18), (px + 4, y - h - 18), (px, y - h - 30)], "#2a2a2a", at=0)]
    return [grp(els, at, "pop")]


def s17():
    """A crag of tall natural pillars on a heather hillside at dusk (Carn Goedog), a second outcrop below (Craig Rhos-y-felin), two
    tiny people for scale; a bundle of pencils: like giant pencils."""
    t0, tc, tr_, tp = T("s17", "Since twenty eleven"), T("s17", "Carn Goedog"), T("s17", "Craig Rhos-y-felin"), T("s17", "giant pencils")
    base = 610
    els = heather_hill(base - 20)
    rr = random.Random(2)
    xs = [560 + 52 * k for k in range(12)]
    for k, x in enumerate(xs):
        h = 250 + 90 * math.sin(k / 11 * math.pi) + rr.uniform(-30, 30)
        els += pillar(x, base + (k % 3) * 4, 54, h, -1, seed=k + 3)
    els += [poly([(520, base + 10), (1200, base + 10), (1240, base + 40), (480, base + 40)], "#2a2a30", at=-1, op=.6)]
    els += [poly(blob(rr.uniform(500, 1250), rr.uniform(base + 6, base + 40), rr.uniform(14, 30), rr.uniform(8, 14), 9, .3, k + 60), "#4b5560",
                 "rgba(200,210,220,.3)", 1, -1) for k in range(16)]
    for k, x in enumerate((200, 236, 270, 304)):
        els += pillar(x, 745, 34, 110 + 20 * (k % 2), -1, seed=40 + k)
    els += [lab(860, 260, "Carn Goedog", tc, BONE, 34, st="serif"), lab(250, 800 - 20, "Craig Rhos-y-felin", tr_, BLUS_L, 26)]
    els += fig(1270, base + 2, 60, t0 + .6, "#1a1410") + fig(1300, base + 4, 54, t0 + .8, "#1a1410")
    els += pencils(1520, 560, tp) + [lab(1520, 620 + 20, "like giant pencils", tp + .3, "#e8b84a", 28)]
    return {"base": "sky", "tod": "dusk", "ground": base - 20, "sun": [1450, 200, 28], "groundc": "#4a3a44",
            "ridges": [{"y": base - 60, "a": 60, "c": "#2e2a3a", "seed": 5}, {"y": base - 30, "a": 30, "c": "#3a3040", "seed": 9}], "cam": CAM, "els": els}


def s18():
    """The foot of the outcrop: a worker drives a wedge into the crack behind a pillar; the pillar comes down onto a built platform
    of stone and earth; a hearth glows by it with charcoal (about 3000 BCE) and a stone tool."""
    t0, tl, th = T("s18", "The diggers found"), T("s18", "where pillars could"), T("s18", "And hearths")
    base = 620
    els = heather_hill(base, -1)
    for k, x in enumerate([260 + 56 * j for j in range(8)]):
        els += pillar(x, base, 58, 330 + 30 * math.sin(k * 1.3), -1, seed=k + 20)
    gap_x = 260 + 56 * 8
    els += [poly([(gap_x - 29, base), (gap_x + 29, base), (gap_x + 29, base - 340), (gap_x - 29, base - 340)], "#1a1418", at=-1, op=.85)]
    els += [poly([(gap_x - 32, base - 210), (gap_x - 18, base - 200), (gap_x - 32, base - 150)], "#7a6a58", "#e8d6b8", 1.5, t0, fx="pop")]
    els += fig(gap_x - 120, base, 150, t0 - .2, "#1a1410", arms="up", face=1) + [lab(gap_x - 190, base - 240, "wedges", t0 + .5, BONE, 28, "end")]
    plat = [(780, base), (820, base - 60), (1320, base - 60), (1340, base), (1340, base + 70), (780, base + 70)]
    els += [poly(plat, "#6b5a46", "rgba(255,236,206,.35)", 1.5, tl - .6, fx="rise")]
    rr = random.Random(5)
    els += [poly(blob(rr.uniform(820, 1320), rr.uniform(base - 50, base + 50), 18, 10, 8, .3, k), "#8a7a64", at=tl - .4, op=.8) for k in range(14)]
    lying = [(860, base - 66), (1240, base - 108), (1250, base - 64), (870, base - 22)]
    els += [grp([poly(lying, BLUS, "rgba(20,24,30,.6)", 1.4, 0), poly([(860, base - 66), (1240, base - 108), (1236, base - 120), (858, base - 80)], BLUS_L, at=0, op=.8)],
                tl + .3, "rise"),
            arr([(gap_x + 10, base - 300), (760, base - 200), (900, base - 110)], tl, BONE, 2.5, "inferred", dur=.8),
            lab(1060, base + 120, "a platform", tl + .8, BONE, 28)]
    els += [gl(1460, base + 50, 120, th, .8, "fire", pulse=True), poly(blob(1460, base + 70, 50, 14, 12, .3, 8), "#2a1a12", at=th)]
    els += [dot(round(1430 + 12 * k, 1), base + 66 - 4 * (k % 2), 4, "#111", th + .1 * k) for k in range(6)]
    els += [poly(blob(1560, base + 72, 22, 14, 10, .2, 3), "#9a8a74", "#e8d6b8", 1.2, th + .6, fx="pop")]
    els += chip(1480, base - 150, "about 3000 BCE", GOLD, th + .4, 28)
    return {"base": "sky", "tod": "dusk", "ground": base, "sun": [1600, 230, 24], "groundc": "#4a3a44",
            "ridges": [{"y": base - 50, "a": 50, "c": "#2e2a3a", "seed": 5}], "cam": CAM, "els": els}


WM_C = (889, 470)


def WP(a, r):
    return PP(a, r, WM_C, PLAN_K)


def pentagon(x, y, r, rot_=-90):
    return [(x + r * math.cos(math.radians(rot_ + 72 * k)), y + r * math.sin(math.radians(rot_ + 72 * k))) for k in range(5)]


WM_STONES = (292, 305, 318, 331)
WM_HOLES = (344, 357, 10, 23, 36, 279, 266)
WM_KEY = 23


def s19():
    """Plan of Waun Mawn on moorland: an arc of four stones and empty stoneholes on part of a circle; the rest dashed; Stonehenge's
    ditch ring laid over it in gold, the same size (110 m); one hole highlighted: its five-sided outline, and Stone 62's base fitting
    it like a key in a lock (an inset)."""
    t0, tf, tc, tw, tk = (T("s19", "In twenty twenty-one"), T("s19", "found the empty"), T("s19", "part of a circle"), T("s19", "as wide as"),
                          T("s19", "one hole"))
    tl = T("s19", "like a key")
    rr = random.Random(17)
    els = [poly(blob(rr.uniform(150, 1650), rr.uniform(160, 780), rr.uniform(30, 90), rr.uniform(14, 40), 10, .3, k), "rgba(90,60,80,.35)", at=-1, curve=True)
           for k in range(26)]
    els += [lab(130, 190, "Waun Mawn", .4, BONE, 36, "start", st="serif")] + chip(440, 180, "2021", GOLD, t0, 26)
    els += [ln(arc_pts(0, 360, 55, 120, WM_C), tc, "rgba(233,220,192,.55)", 2.5, "inferred", dur=1.8)]
    for k, a in enumerate(WM_STONES):
        x, y = WP(a, 55)
        els += [grp([poly(rot([(x - 9, y - 16), (x + 9, y - 16), (x + 11, y + 14), (x - 11, y + 14)], x, y, a + 90), "#8f8a80", "#e9e2d0", 1.5, 0),
                     poly(rot([(x - 9, y + 14), (x + 11, y + 14), (x + 16, y + 26), (x - 4, y + 26)], x, y, a + 90), "rgba(0,0,0,.35)", at=0)], .4 + .15 * k, "pop")]
    for k, a in enumerate(WM_HOLES):
        x, y = WP(a, 55)
        if a == WM_KEY:
            els.append(poly(pentagon(x, y, 15, a), "#14100c", "rgba(255,236,206,.6)", 1.5, tf + 1.0 + .15 * k, fx="pop"))
        else:
            els.append(poly(E(x, y, 12, 9, 14), "#14100c", "rgba(255,236,206,.5)", 1.2, tf + 1.0 + .15 * k, fx="pop"))
    els += [ln([WP(298, 59), (560, 360)], tf + .9, BONE, 1.4, dur=.3), lab(550, 372, "stones and empty holes", tf + 1.1, BONE, 28, "end")]
    els += [ln(arc_pts(0, 360, 55, 120, WM_C), tw, GOLD, 4, dur=1.4), gl(889, 470, 420, tw + .4, .14, "lamp"),
            lab(889, 470 + 6, "as wide as", tw + .6, GOLD, 30), lab(889, 510, "Stonehenge's ditch", tw + .7, GOLD, 30)]
    kx, ky = WP(WM_KEY, 55)
    ix, iy, ir = 1460, 320, 120
    els += [ln(pentagon(kx, ky, 22, WM_KEY) + pentagon(kx, ky, 22, WM_KEY)[:1], tk, GOLD, 3, dur=.5),
            ln([(kx + 26, ky + 6), (ix - ir + 6, iy - 30)], tk + .3, GOLD, 1.6, dur=.4),
            circ(ix, iy, ir, "rgba(18,14,10,.92)", GOLD, 3, tk + .4, fx="pop"),
            poly(pentagon(ix, iy + 10, 62, 0), "#0b0907", "rgba(255,236,206,.6)", 2, tk + .6, fx="pop"),
            poly(pentagon(ix + 150, iy + 10, 58, 0), "#8fa0b0", "#e6eef4", 2, tk + .9, fx="pop"),
            lab(ix + 150, iy + 100, "Stone 62?", tk + 1.0, BLUS_L, 26),
            poly(pentagon(ix, iy + 10, 58, 0), "rgba(143,160,176,.95)", "#e6eef4", 2, tl, fx="pop"),
            lab(ix, iy + ir + 44, "like a key in a lock", tl + .3, GOLD, 26)]
    return {"base": "plan", "bg": "#3a3326", "cam": CAM, "els": els}


VWM = View(-5.4, -1.2, 50.55, 52.55, (140, 140, 1500, 620))


def s19m():
    """Their suggestion: a small map from the Preseli Hills to Salisbury Plain; a lilac dotted ring leaves Waun Mawn and travels east:
    a first Stonehenge, taken apart and moved?"""
    t0 = T("s19m", "Their suggestion")
    v = VWM
    wx, wy = v.p(-4.80, 51.99)
    sx, sy = v.p(*STH)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += ring_icon(wx, wy, 34, -1, BLUS_L, "known", 10) + [lab(wx, wy - 56, "Waun Mawn", -1, BLUS_L, 28)]
    els += [arr([(wx + 44, wy + 6), ((wx + sx) / 2, wy - 60), (sx - 46, sy - 10)], t0 + .3, LILAC, 3.5, "claimed", dur=1.6)]
    els += ring_icon(sx, sy, 34, t0 + 1.8) + [lab(sx, sy - 56, "Stonehenge", t0 + 1.8, GOLD, 28)]
    els += [lab((wx + sx) / 2, wy - 110, "a first Stonehenge?", t0 + 1.0, LILAC, 32, st="serif")]
    return {"base": "map", "cam": CAM, "els": els}


def bars(x, y, vals, at, c, w=22, gap=10, scale=120):
    return [rect(x + k * (w + gap), y - v * scale, w, v * scale, c, at=at + .06 * k, fx="fill") for k, v in enumerate(vals)]


def s20_add():
    """The chemistry test, as an inset on the plan: the Waun Mawn stones and the chips from the hole against Stone 62, bars that do not
    line up; no match; the stones' source: a nearby outcrop."""
    tt, tn = T("s20", "tested the"), T("s20", "neither the stones")
    els = [rect(1160, 530, 500, 250, "rgba(14,12,10,.92)", "rgba(255,236,206,.4)", 2, 10, tt - .2, fx="pop"),
           lab(1410, 566, "chemistry", tt, BONE, 26)]
    els += bars(1200, 736, [.7, .45, .9, .3, .6], tt + .3, "#bdb6aa", scale=110)
    els += bars(1440, 736, [.35, .85, .4, .75, .25], tt + .6, "#8fa0b0", scale=110)
    els += [lab(1272, 766, "Waun Mawn", tt + .4, BONE, 22), lab(1512, 766, "Stone 62", tt + .7, BLUS_L, 22)]
    els += cross(1410, 660, tn + .6) + [lab(1410, 620, "no match", tn + .9, RED, 28)]
    els += [ln([WP(318, 59), (560, 520)], tn + 1.4, BONE, 1.4, dur=.3), lab(550, 532, "from a nearby outcrop", tn + 1.6, BONE, 26, "end")]
    return els


def s20b_add():
    """Never finished: the built part of the ring (north and west) traced in bone; question marks along the empty south; is it a circle at
    all?"""
    te, ta = T("s20b", "Even its excavators"), T("s20b", "ever a circle")
    els = [ln(arc_pts(262, 365, 57, 40, WM_C), te + .1, BONE, 6, dur=1.0, op=.85)]
    for k, a in enumerate((120, 165, 210)):
        x, y = WP(a, 49)
        els += [lab(x, y + 14, "?", te + .6 + .25 * k, LILAC, 44, st="big", fx="pop")]
    els += [lab(889, 640, "never finished?", te + 1.0, LILAC, 32, st="serif"), lab(889, 360, "a circle at all?", ta, LILAC, 30)]
    return els


def s21_add():
    """Back on the legend's map: west, and right; a solid gold route from west Wales to Salisbury Plain; the tale's route from Ireland
    dims."""
    tw, tr = T("s21", "Merlin's tale"), T("s21", "The stones just")
    v = VBI
    ix, iy = v.p(-7.6, 53.3)
    sx, sy = v.p(*STH)
    px, py = v.p(*PRES)
    els = [ln([(ix + 34, iy + 6), ((ix + sx) / 2, iy + 20), (sx - 14, sy - 6)], tr, "rgba(29,58,74,.85)", 9, draw=False, curve=True)]
    els += [arr([(1560, 220), (1440, 220)], tw + .2, GOLD, 4, dur=.5, curve=False), lab(1600, 230, "west", tw + .4, GOLD, 30, "start")]
    els += [ln([(px, py), ((px + sx) / 2, py - 18), (sx, sy)], tr + .3, GOLD, 5, dur=1.0, curve=True), pin(px, py, "Wales", tr + .4, GOLD, "end", -20, 34)]
    return els


# ================================================================== CHAPTER 3 · A stone from Scotland
VAT = View(-100.0, 10.0, 22.0, 62.0, (1050, 330, 620, 380))


def crane(x, base, h, jib, at):
    """A lattice crane of the 1950s: mast, jib, cable."""
    els = [ln([(x - 14, base), (x - 10, base - h)], 0, "#c9a46a", 4, draw=False), ln([(x + 14, base), (x + 10, base - h)], 0, "#c9a46a", 4, draw=False)]
    for k in range(10):
        y1, y2 = base - h * k / 10, base - h * (k + 1) / 10
        els.append(ln([(x - 12, y1), (x + 12, y2)], 0, "#c9a46a", 2, draw=False))
    els += [ln([(x, base - h), (x + jib, base - h + 60)], 0, "#c9a46a", 5, draw=False), ln([(x, base - h - 30), (x + jib, base - h + 60)], 0, "#c9a46a", 2, draw=False),
            ln([(x + jib, base - h + 60), (x + jib, base - h + 260)], 0, "#e8e2d6", 2, draw=False)]
    return [grp(els, at, "rise")]


def s22():
    """1958: a trilithon being re-erected, a crane and scaffolding, the upright 'Stone 58'; a slim core slides out of it; then across a
    small map of the Atlantic: the core to America, and back (2018)."""
    t0, tc, ta, tb = T("s22", "In nineteen fifty-eight"), T("s22", "a core was"), T("s22", "ended up"), T("s22", "Sixty years")
    base = 720
    els = crane(170, base, 560, 420, -1)
    for x in (420, 650):
        els += [poly([(x - 70, base), (x + 70, base), (x + 62, base - 440), (x - 62, base - 440)], "#8f877b", "rgba(30,25,20,.6)", 1.5, -1),
                poly([(x + 20, base), (x + 70, base), (x + 62, base - 440), (x + 20, base - 440)], "#4f4a44", at=-1, op=.6)]
    els += [poly([(330, base - 440), (740, base - 440), (740, base - 520), (330, base - 520)], "#8f877b", "rgba(30,25,20,.6)", 1.5, -1)]
    for k in range(5):
        els.append(ln([(300 + 110 * k, base), (300 + 110 * k, base - 470)], -1, "rgba(200,190,170,.45)", 2, draw=False))
    for k in range(4):
        els.append(ln([(290, base - 110 * (k + 1)), (770, base - 110 * (k + 1))], -1, "rgba(200,190,170,.45)", 2, draw=False))
    els += [lab(650, base + 50, "Stone 58", t0 + .3, BONE, 28)] + chip(420, 170, "1958", GOLD, t0, 28)
    els += [grp([rect(700, base - 262, 130, 16, "#cfc6b4", "#8f877b", 1.2, 6, 0)], tc, "rise"), lab(770, base - 300, "a core", tc + .3, GOLD, 28)]
    v = VAT
    els += [{"k": "group", "clip": [1050, 330, 620, 380, 8], "els": [rect(1040, 320, 640, 400, "#16303e", at=0), {"k": "map", "land": v.land(), "in": 0}], "in": -1}]
    ux, uy = v.p(-1.8, 51.2)
    ax_, ay_ = v.p(-77.0, 40.0)
    els += [rect(1050, 330, 620, 380, "none", "rgba(159,208,255,.35)", 1.5, 8, -1)]
    els += [arr([(ux, uy), ((ux + ax_) / 2, uy - 120), (ax_, ay_)], ta, AMBER, 3, "claimed", dur=1.0), lab(ax_ + 10, ay_ + 50, "America", ta + .6, AMBER, 26)]
    els += [arr([(ax_ + 10, ay_ + 10), ((ux + ax_) / 2, uy + 40), (ux - 8, uy + 8)], tb, GOLD, 3, dur=1.0)] + chip(1360, 760, "back in 2018", GOLD, tb + .8, 26)
    return {"base": "sky", "tod": "day", "ground": base, "sun": False, "groundc": "#4a5634", "cam": CAM, "els": els}


VWI = View(-2.35, -1.15, 50.98, 51.55, (720, 130, 930, 640))


def sarsen_icon(x, y, h, c, at, fx="pop"):
    w = h * .55
    return [grp([poly([(x - w / 2, y), (x + w / 2, y), (x + w * .42, y - h), (x - w * .42, y - h)], c, "rgba(20,16,12,.6)", 1.2, 0)], at, fx)]


def s23():
    """Map of Wiltshire: Stonehenge in the south, West Woods about 25 km to the north; a fingerprint; a grid of the 52 surviving
    sarsens, 50 gold and 2 grey."""
    tn, tf, tw = T("s23", "David Nash's team"), T("s23", "Fifty of the"), T("s23", "West Woods")
    v = VWI
    sx, sy = v.p(*STH)
    wx, wy = v.p(*WWOODS)
    els = [rect(720, 130, 930, 640, "rgba(74,86,52,.35)", "rgba(255,236,206,.3)", 1.5, 10, -1),
           poly(blob(wx, wy, 70, 40, 14, .25, 3), "rgba(40,70,30,.8)", "rgba(160,200,120,.5)", 1.5, -1, curve=True),
           lab(wx + 90, wy - 60, "Marlborough Downs", -1, DIM, 24, "start")]
    els += [pin(sx, sy, "Stonehenge", .3, GOLD, "start", 22, 8), pin(wx, wy, "West Woods", tw, GOLD, "start", 24, 8),
            ln([(sx, sy - 14), (wx, wy + 14)], tw + .3, GOLD, 4, dur=1.0), lab((sx + wx) / 2 - 30, (sy + wy) / 2, "25 km", tw + 1.0, GOLD, 30, "end")]
    els += [{"k": "scale", "x": 1450, "y": 760, "w": round(v.km(10), 1), "t": "10 km", "in": .6}]
    # the fingerprint
    fx_, fy_ = 280, 250
    els += [grp([poly(E(fx_, fy_, 22 + 12 * k, 32 + 15 * k, 30), "none", "#e8b84a", 2.5, 0, op=.85) for k in range(6)], tn, "pop"),
            lab(fx_ + 130, fy_ + 10, "a fingerprint", tn + .3, "#e8b84a", 26, "start")]
    for k in range(52):
        col, row = k % 13, k // 13
        x, y = 120 + 42 * col, 470 + 70 * row
        odd = k in (25, 47)
        els += sarsen_icon(x, y, 52, "#8f877b" if odd else GOLD, tf + .04 * k)
    els += [lab(300, 740, "50 of 52 match", tf + 2.4, GOLD, 28), lab(560, 740, "2 differ", tf + 2.8, DIM, 28)]
    return {"base": "plan", "bg": "#262c1c", "north": [1600, 190], "cam": CAM, "els": els}


def slab3d(x, y, L, W, H, at, c="#6f7a5e", cl="#a3ad88", cd="#3e4634", fx="pop"):
    """A slab lying flat, in a simple three-quarter view: top face, front face, end face; fine layering on the front."""
    dx, dy = W * .55, -W * .35
    top = [(x - L / 2, y - H), (x + L / 2, y - H), (x + L / 2 + dx, y - H + dy), (x - L / 2 + dx, y - H + dy)]
    front = [(x - L / 2, y), (x + L / 2, y), (x + L / 2, y - H), (x - L / 2, y - H)]
    end = [(x + L / 2, y), (x + L / 2 + dx, y + dy), (x + L / 2 + dx, y - H + dy), (x + L / 2, y - H)]
    els = [poly([(p[0] + 16, p[1] + 20) for p in front + end[1:3]], "rgba(0,0,0,.35)", at=0),
           poly(front, c, "rgba(20,24,16,.6)", 1.5, 0), poly(top, cl, "rgba(20,24,16,.5)", 1.5, 0), poly(end, cd, "rgba(20,24,16,.5)", 1.5, 0)]
    els += [ln([(x - L / 2 + 6, y - H * k / 6), (x + L / 2 - 6, y - H * k / 6 + (2 if k % 2 else -2))], 0, "rgba(40,50,30,.45)", 1.5, draw=False) for k in range(1, 6)]
    return [grp(els, at, fx)]


def s24():
    """The Altar Stone drawn large, a greenish slab with fine layers; a lilac dotted arrow to 'Wales?', struck through: 2023, no match."""
    t0, tw, tn = T("s24", "But one stone"), T("s24", "For a century"), T("s24", "until tests")
    els = [gl(1000, 520, 640, -1, .14, "lamp")]
    els += slab3d(1050, 600, 760, 160, 120, t0 - .2)
    els += [lab(1050, 700, "the Altar Stone", t0 + .3, ALTAR_L, 34, st="serif")]
    els += [arr([(640, 520), (480, 470), (330, 440)], tw, LILAC, 3, "claimed", dur=.8), lab(270, 420, "Wales?", tw + .4, LILAC, 34, "end")]
    els += cross(400, 470, tn, RED, 1.6) + chip(330, 560, "2023: no match", RED, tn + .3, 26)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def stamp(x, y, r, text, at, c="#c9573e", rot_=-8, size=22):
    els = [circ(x, y, r, "rgba(201,87,62,.12)", c, 5, 0), circ(x, y, r - 8, "none", c, 2.5, 0),
           lab(x, y + size * .36, text, 0, c, size, st="lab", halo=False)]
    return [grp(els, at, "pop", tr="rotate(%d %d %d)" % (rot_, x, y))]


def s25():
    """Left: a chip of the stone under a microscope, tiny grains glinting (Anthony Clarke, Curtin University). Right: an open passport
    filling with round stamps, each an age in millions of years; then a gold stamp: Scotland."""
    t0, tp = T("s25", "So a team"), T("s25", "like a stamp")
    mx, my, mr = 400, 430, 190
    els = [circ(mx, my, mr, "rgba(10,12,10,.95)", "#d9d0b8", 6, t0 - .2, fx="pop")]
    rr = random.Random(12)
    for k in range(40):
        a, d = rr.uniform(0, 2 * math.pi), rr.uniform(0, .92) ** .6
        x, y = mx + math.cos(a) * d * mr * .85, my + math.sin(a) * d * mr * .85
        z = rr.uniform(7, 16)
        c = rr.choice(["#f0d8a8", "#e8c07a", "#d8e8f0", "#c9a0a0", "#f5ecd6"])
        els.append(poly([(x - z * .5, y - z * .2), (x, y - z * .7), (x + z * .55, y - z * .1), (x + z * .3, y + z * .5), (x - z * .4, y + z * .45)], c, "#fff",
                        .8, t0 + .4 + .03 * k, fx="pop"))
    els += [lab(mx, my + mr + 50, "mineral grains", t0 + 1.2, GOLD, 30), lab(mx, 170, "Curtin University", t0 + .6, DIM, 26)]
    px, py = 1000, 200
    els += [grp([rect(px, py, 300, 420, "#2a3a5a", "#c9a46a", 3, 8, 0), rect(px + 300, py, 300, 420, "#2a3a5a", "#c9a46a", 3, 8, 0),
                 rect(px + 12, py + 12, 276, 396, "#efe6d2", at=0), rect(px + 312, py + 12, 276, 396, "#efe6d2", at=0),
                 ln([(px + 300, py + 12), (px + 300, py + 408)], 0, "#b9ae96", 2, draw=False)], tp - 1.2, "pop")]
    for k, (x, y, t) in enumerate(((px + 90, py + 110, "460 Myr"), (px + 210, py + 240, "1,000 Myr"), (px + 100, py + 330, "1,600 Myr"),
                                   (px + 400, py + 100, "2,700 Myr"))):
        els += stamp(x, y, 58, t, tp + .5 + .45 * k, rot_=(-12 + 9 * k))
    els += [lab(px + 300, py + 470, "like passport stamps", tp + .4, BONE, 28), lab(px + 300, py + 506, "ages in millions of years", tp + .8, DIM, 22)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


VNS = View(-6.9, -0.5, 56.9, 59.45, (300, 130, 1250, 650))
ORS = [(-3.2, 59.0, 70, 40), (-2.9, 58.85, 50, 30), (-3.3, 58.45, 60, 46), (-3.75, 57.62, 70, 26), (-3.1, 57.68, 60, 22), (-2.6, 57.66, 50, 18)]


def s26():
    """Northern Scotland and Orkney: the old red sandstones shaded amber; the stone circles of Orkney struck through (2024: no match);
    then Caithness glows gold (2026: closest match)."""
    t0, tn, tc = T("s26", "That same year"), T("s26", "no match"), T("s26", "Caithness")
    v = VNS
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for k, (lo, la, rx, ry) in enumerate(ORS):
        x, y = v.p(lo, la)
        els.append(poly(blob(x, y, rx, ry, 14, .25, k + 2), "rgba(232,140,90,.35)", "rgba(240,170,110,.6)", 1.5, .4 + .1 * k, curve=True, op=.9))
    lx, ly = v.p(-5.3, 57.25)
    els += [lab(lx, ly, "old red sandstone", .8, "#f0a070", 26)]
    ox, oy = v.p(-3.22, 59.0)
    els += ring_icon(ox - 20, oy + 6, 14, t0, BONE, "known", 9) + ring_icon(ox + 18, oy - 8, 18, t0 + .2, BONE, "known", 11)
    els += [lab(ox - 80, oy - 50, "Orkney's stone circles", t0 + .4, BONE, 26, "end")]
    els += cross(ox, oy, tn, RED, 1.3) + chip(ox + 160, oy + 40, "2024: no match", RED, tn + .3, 24)
    cx, cy = v.p(*CAITH)
    els += [poly(blob(cx, cy, 64, 46, 16, .2, 7), "rgba(242,201,142,.5)", GOLD, 3, tc, curve=True, fx="pop"), gl(cx, cy, 160, tc + .2, .5, "lamp"),
            lab(cx + 80, cy + 20, "Caithness", tc + .3, GOLD, 32, "start")] + chip(cx + 220, cy + 80, "2026: closest match", GOLD, tc + .8, 26)
    return {"base": "map", "cam": CAM, "els": els}


VGB2 = View(-8.5, 3.5, 49.8, 59.0, (300, 125, 1200, 660))
SEA_ROUTE = [(-3.0, 58.7), (-1.6, 57.9), (-1.5, 56.6), (-1.2, 55.4), (-0.3, 54.3), (0.5, 53.3), (1.8, 52.6), (1.6, 51.3), (0.4, 50.7), (-1.2, 50.65), (-1.75, 50.8)]
LAND_ROUTE = [(-3.4, 58.4), (-4.0, 57.5), (-4.1, 56.6), (-3.4, 55.9), (-2.9, 55.0), (-2.6, 54.2), (-2.3, 53.4), (-2.1, 52.5), (-1.9, 51.8), (-1.83, 51.2)]


def s27():
    """Britain: from Caithness, a blue dashed sea route down the east coast and round to the south; an amber dotted route in stages over
    land and along rivers; both to Stonehenge; a lilac question mark."""
    ts, tl = T("s27", "favoured the"), T("s27", "in stages")
    v = VGB2
    sx, sy = v.p(*STH)
    cx, cy = v.p(*CAITH)
    els = [{"k": "map", "land": v.land(), "in": -1}, pin(cx, cy, "Caithness", .3, GOLD, "start", 20, 8), pin(sx, sy, "Stonehenge", .5, GOLD, "end", -22, 30)]
    els += [ln([v.p(*q) for q in SEA_ROUTE], ts, "#7fc4ff", 4, "inferred", dur=2.0, curve=True), lab(v.p(2.4, 54.6)[0], v.p(2.4, 54.6)[1], "by sea?", ts + 1.0, "#7fc4ff", 32)]
    pts = [v.p(*q) for q in LAND_ROUTE]
    els += [ln(pts, tl, AMBER, 4, "claimed", dur=2.0, curve=True)] + [dot(x, y, 6, AMBER, tl + .2 * k) for k, (x, y) in enumerate(pts[1:-1:2])]
    els += [lab(v.p(-6.6, 55.2)[0], v.p(-6.6, 55.2)[1], "in stages?", tl + 1.0, AMBER, 32)]
    els += qmark(v.p(-0.6, 56.4)[0], v.p(-0.6, 56.4)[1], tl + 2.0, 90)
    return {"base": "map", "cam": CAM, "els": els}


def s28_add():
    """Six tonnes the length of Britain: slab icons along the way; then gold threads from the far corners the stones came from
    (Caithness, west Wales, Wiltshire) to Stonehenge: connected."""
    t0, tc = T("s28", "Six tonnes"), T("s28", "Neolithic Britain")
    v = VGB2
    sx, sy = v.p(*STH)
    els = []
    for k, q in enumerate(LAND_ROUTE[1:-1:2]):
        x, y = v.p(*q)
        els += slab_icon(x + 26, y - 6, 30, t0 + .3 + .25 * k)
    els += [lab(v.p(-7.4, 58.0)[0], v.p(-7.4, 58.0)[1], "6 tonnes", t0 + .2, GOLD, 32)]
    for k, q in enumerate((CAITH, PRES, WWOODS)):
        x, y = v.p(*q)
        els += [ln([(x, y), ((x + sx) / 2 + 20, (y + sy) / 2 - 20), (sx, sy)], tc + .3 * k, GOLD, 2.5, dur=.9, curve=True), dot(x, y, 7, GOLD, tc + .3 * k)]
    els += [gl(sx, sy, 140, tc + 1.0, .6, "lamp", pulse=True), lab(sx + 60, sy - 70, "connected", tc + 1.2, GOLD, 34, "start", st="serif")]
    return els



def s25z_add():
    """The last stamp, in gold: Scotland."""
    ts = T("s25z", "those passport stamps")
    px, py = 1000, 200
    return [gl(px + 450, py + 290, 150, ts + 1.1, .5, "lamp")] + stamp(px + 450, py + 290, 80, "SCOTLAND", ts + 1.2, "#d9a520", 6, 26)


# ================================================================== CHAPTER 4 · Moving the giants
VIC = View(-5.9, -0.7, 50.3, 53.1, (330, 130, 1300, 640))
ICE = [(-5.7, 52.5), (-4.6, 52.95), (-3.6, 52.7), (-3.0, 52.15), (-2.5, 51.75), (-2.05, 51.45), (-1.75, 51.25), (-1.95, 51.0), (-2.6, 51.05),
       (-3.4, 51.15), (-4.3, 51.3), (-5.3, 51.55), (-5.8, 51.9)]


def s29():
    """Southern Britain in the Ice Age: a lilac dotted ice sheet (the claim) spreads from west Wales over the Bristol Channel, boulders
    inside it, its tongue reaching towards Salisbury Plain (since 1971)."""
    t0, tg = T("s29", "Since nineteen seventy-one"), T("s29", "Ice Age glaciers")
    v = VIC
    sx, sy = v.p(*STH)
    els = [{"k": "map", "land": v.land(), "in": -1}, pin(sx, sy, "Stonehenge", .3, GOLD, "start", 22, 8)]
    els += [poly([v.p(*q) for q in ICE], "rgba(201,193,238,.16)", LILAC, 3, tg, curve=True, fx="pop", style="claimed")]
    for k, (lo, la) in enumerate(((-4.9, 52.1), (-4.2, 51.95), (-3.6, 51.7), (-3.0, 51.5), (-2.5, 51.35))):
        x, y = v.p(lo, la)
        els += [poly(blob(x, y, 12, 8, 9, .3, k), "rgba(201,193,238,.4)", LILAC, 1.5, tg + .5 + .2 * k, fx="pop", style="claimed"),
                arr([(x + 16, y), (x + 60, y + 6)], tg + .6 + .2 * k, LILAC, 2, "claimed", dur=.4, curve=False)]
    lx, ly = v.p(-4.6, 52.75)
    els += [lab(lx, ly - 30, "glaciers?", tg + .4, LILAC, 40, st="serif")] + chip(520, 190, "since 1971", LILAC, t0, 26)
    return {"base": "map", "cam": CAM, "els": els}


def balance(x, y, s, at, c=BONE):
    els = [ln([(x, y), (x, y - s)], 0, c, 4, draw=False), ln([(x - s * .7, y - s * .85), (x + s * .7, y - s * .85)], 0, c, 4, draw=False),
           poly([(x - .2 * s, y), (x + .2 * s, y), (x, y - .1 * s)], c, at=0)]
    for sx_ in (-1, 1):
        px = x + sx_ * s * .7
        els += [ln([(px, y - s * .85), (px - .22 * s, y - s * .4)], 0, c, 2, draw=False), ln([(px, y - s * .85), (px + .22 * s, y - s * .4)], 0, c, 2, draw=False),
                poly(E(px, y - s * .4, .26 * s, .07 * s, 16, 0, 180), "none", c, 3, 0)]
    return [grp(els, at, "pop")]


def s30_add():
    """Scarce evidence (a balance with two empty pans); then what ice would leave: lilac dotted boulders and grains scattered over
    Salisbury Plain."""
    tb, tw = T("s30", "direct evidence"), T("s30", "But ice that")
    v = VIC
    els = balance(1500, 330, 120, tb) + [lab(1500, 380, "scarce evidence", tb + .4, BONE, 28)]
    rr = random.Random(21)
    for k in range(26):
        lo, la = rr.uniform(-2.4, -1.2), rr.uniform(50.95, 51.45)
        x, y = v.p(lo, la)
        if rr.random() < .45:
            els.append(poly(blob(x, y, 9, 6, 8, .3, k), "rgba(201,193,238,.4)", LILAC, 1.4, tw + .05 * k, fx="pop", style="claimed"))
        else:
            els.append(dot(x, y, 3.5, LILAC, tw + .05 * k))
    x, y = v.p(-1.0, 50.85)
    els += [lab(x, y + 40, "what ice would leave", tw + 1.4, LILAC, 28)]
    return els


def outcrop_icon(x, y, s, at, label_=None, c="#56606c"):
    els = [poly([(x - s * .8, y + 6), (x - s * .5, y - s * .15), (x + s * .5, y - s * .18), (x + s * .85, y + 6)], "#4a3a44", "rgba(255,236,206,.2)", 1.2, 0, curve=True)]
    for k in range(5):
        els += pillar(x - s * .5 + k * s * .25, y, s * .22, s * (.7 + .25 * math.sin(k * 1.7)), 0, c, seed=90 + k)
    out = [grp(els, at, "pop")]
    if label_:
        out.append(lab(x, y + 40, label_, at + .2, BLUS_L, 26))
    return out


def s31():
    """A small rounded boulder on a museum tray (1924), once called a glacial stray; a gold thread to Craig Rhos-y-felin (2025: a match);
    a broken bluestone stump with its missing top outlined, the boulder fitting there."""
    t0, tm, tp = T("s31", "One boulder"), T("s31", "new tests tied"), T("s31", "most likely")
    bx, by = 400, 470
    els = [rect(200, by + 40, 400, 26, "#3a2c20", "rgba(255,236,206,.4)", 1.5, 4, -1), rect(220, by + 66, 360, 10, "rgba(0,0,0,.4)", at=-1)]
    els += [poly(blob(bx, by, 110, 52, 18, .12, 4), "#7a8796", "#d6e0ea", 2, t0, curve=True, fx="pop")]
    els += [rect(462, by + 4, 92, 38, "#efe6d2", "#8a7a64", 1.2, 3, t0 + .4, fx="pop"), lab(508, by + 32, "1924", t0 + .5, "#4a3a2a", 24, halo=False)]
    els += [lab(bx, by - 110, "a glacial stray?", t0 + .8, LILAC, 32, st="serif")]
    els += outcrop_icon(1380, 330, 150, tm - .3, "Craig Rhos-y-felin")
    els += [ln([(bx + 110, by - 10), (900, 300), (1290, 300)], tm, GOLD, 3, dur=1.0, curve=True)] + chip(1010, 230, "2025: a match", GOLD, tm + .8, 26)
    sx_, sb = 1020, 720
    els += [grp(pillar(sx_, sb, 120, 150, 0, seed=77), tp, "pop"),
            poly([(sx_ - 60, sb - 150), (sx_ + 60, sb - 150), (sx_ + 50, sb - 330), (sx_ - 50, sb - 330)], "rgba(122,135,150,.12)", BLUS_L, 2.5, tp + .3,
                 style="inferred", fx="pop"),
            arr([(bx + 60, by + 40), (700, 620), (sx_ - 70, sb - 240)], tp + .6, BLUS_L, 2.5, "inferred", dur=.8),
            lab(sx_ + 120, sb - 260, "a piece of", tp + 1.0, BLUS_L, 28, "start"), lab(sx_ + 120, sb - 222, "a bluestone", tp + 1.1, BLUS_L, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s32():
    """A chalk stream in section, sand on its bed; a scoop of sand in a magnifier full of grains (500+ zircon grains, 2026); beside it,
    the plain with its streams and the lilac ice tongue struck through: no sign of ice."""
    t0, tz, tn = T("s32", "And in twenty twenty-six"), T("s32", "zircon grains"), T("s32", "showed no sign")
    wy = 600
    els = [rect(80, wy - 20, 900, 200, "#2b5f7a", at=-1, op=.85), rect(80, wy + 180, 900, 40, "#c9b48a", at=-1),
           poly([(80, wy - 20), (80, wy - 120), (220, wy - 40), (300, wy - 20)], TURF, at=-1), poly([(980, wy - 20), (980, wy - 120), (840, wy - 40), (760, wy - 20)], TURF, at=-1)]
    rr = random.Random(30)
    els += [dot(round(rr.uniform(100, 960), 1), round(rr.uniform(wy + 160, wy + 200), 1), round(rr.uniform(2, 5), 1), "#e6d6b0", -1) for _ in range(60)]
    els += [{"k": "water", "y": wy - 20, "h": 4, "x0": 80, "x1": 980, "op": .8, "in": -1}]
    mx, my, mr = 560, 370, 150
    els += [arr([(560, wy + 160), (560, my + mr + 10)], t0, GOLD, 3, dur=.4, curve=False), circ(mx, my, mr, "rgba(12,10,8,.94)", GOLD, 4, t0 + .2, fx="pop")]
    for k in range(60):
        a, d = rr.uniform(0, 2 * math.pi), rr.uniform(0, .93) ** .6
        x, y = mx + math.cos(a) * d * mr * .88, my + math.sin(a) * d * mr * .88
        z = rr.uniform(4, 9)
        c = "#f0b8a0" if k % 7 == 0 else rr.choice(["#e6d6b0", "#d8c49a", "#f0e6cc"])
        els.append(poly([(x - z, y), (x, y - z * .8), (x + z, y), (x, y + z * .8)], c, at=tz + .02 * k, fx="pop"))
    els += chip(mx, my - mr - 44, "500+ zircon grains", GOLD, tz + .6, 26)
    # the plain and its streams, the ice tongue struck through
    px0, py0 = 1100, 260
    els += [rect(px0, py0, 520, 360, "rgba(79,92,56,.6)", "rgba(255,236,206,.35)", 1.5, 10, -1)]
    for k, pts in enumerate(([(1140, 300), (1250, 400), (1300, 520), (1380, 600)], [(1600, 290), (1500, 380), (1400, 470), (1380, 600)], [(1130, 500), (1260, 540), (1380, 600)])):
        els.append(ln(pts, -1, "#6fb6d6", 3, curve=True, draw=False))
    els += [pin(1380, 470, "", -1, GOLD), lab(1380, 640 + 20, "Salisbury Plain", -1, DIM, 24)]
    els += [poly([(1100, 300), (1240, 330), (1330, 420), (1250, 470), (1100, 420)], "rgba(201,193,238,.16)", LILAC, 2.5, t0 + .3, style="claimed", curve=True, fx="pop"),
            strike(1110, 470, 1330, 300, tn + .4, RED, 6), lab(1360, 230, "no sign of ice", tn + .8, BONE, 30)] + chip(1560, 690, "2026", GOLD, tn + .2, 26)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def sledge_side(x, y, L, at, load=None):
    """A wooden sledge in side view on a timber track (sleepers), with a load: 'block' (a grey cube) or 'pillar' (a bluestone)."""
    els = [ln([(x - L / 2, y - 14), (x + L / 2, y - 14), (x + L / 2 + 30, y - 40)], 0, WOOD, 12, draw=False),
           ln([(x - L / 2, y - 14), (x + L / 2, y - 14)], 0, "rgba(255,220,170,.4)", 2, draw=False)]
    if load == "block":
        els += [rect(x - L * .28, y - 20 - L * .5, L * .56, L * .5, "#9a958c", "rgba(30,25,20,.6)", 1.5, 2, 0), rect(x - L * .28, y - 20 - L * .5, L * .56, 10, "#c4bfb4", at=0)]
    elif load == "pillar":
        els += [poly([(x - L * .45, y - 24), (x + L * .45, y - 30), (x + L * .45, y - 30 - L * .18), (x - L * .45, y - 24 - L * .16)], "#6f8090", "rgba(20,24,30,.6)", 1.5, 0)]
    elif load == "sarsen":
        els += [poly([(x - L * .46, y - 24), (x + L * .46, y - 28), (x + L * .44, y - 28 - L * .22), (x - L * .44, y - 24 - L * .2)], "#8f877b", "rgba(30,25,20,.6)", 1.5, 0),
                poly([(x - L * .44, y - 24 - L * .2), (x + L * .44, y - 28 - L * .22), (x + L * .4, y - 36 - L * .24), (x - L * .4, y - 32 - L * .22)], "#cdbb98", at=0)]
    return [grp(els, at, "pop")]


def track(x0, x1, y, at, n=None, c=WOOD_D):
    n = n or int((x1 - x0) / 44)
    return [rect(x0 + (x1 - x0) * k / n - 7, y - 6, 14, 14, c, "rgba(255,220,170,.25)", 1, 2, at) for k in range(n + 1)] + [
        ln([(x0, y - 2), (x1, y - 2)], at, "#5a3a22", 4, draw=False)]


def haulers(x_end, y, n, h, gap, at, dt=.12, c="#1e1712", rows=2, rope_to=None):
    """n figures in `rows` lines hauling leftwards on ropes towards rope_to (the sledge), the first at x_end."""
    els = []
    per = (n + rows - 1) // rows
    for r_ in range(rows):
        yy = y + r_ * 10
        xs = [x_end + k * gap for k in range(per)]
        for k, x in enumerate(xs):
            if r_ * per + k >= n:
                break
            els += fig(x, yy, h * (1 - .04 * r_), at + dt * (r_ * per + k), c, arms="pull", face=-1, lean=.18)
        if rope_to:
            els.append(ln([(xs[0] - .3 * h, yy - .62 * h), rope_to], at, "#d8c49a", 2, draw=False))
    return els


def s33():
    """A London square in 2016: a block of about a tonne on a sycamore sledge sliding on a timber track; ten people haul it (10 people);
    then, smaller, a two-tonne bluestone on a sledge with about twenty people."""
    t0, tt, t10, t20 = T("s33", "In twenty sixteen"), T("s33", "track of"), T("s33", "Ten people"), T("s33", "A two-tonne")
    gy = 640
    els = []
    rr = random.Random(6)
    x = -40
    while x < 1820:
        w, h = rr.choice((140, 170, 200)), rr.choice((230, 260, 290))
        els += [rect(x, gy - h, w - 6, h, "#5a4e46", "rgba(255,236,206,.15)", 1, 0, -1)]
        els += [rect(x + 18 + 34 * j, gy - h + 30 + 52 * i, 16, 28, "rgba(255,226,170,.45)" if rr.random() < .3 else "rgba(30,26,24,.5)", at=-1)
                for i in range(3) for j in range(int((w - 30) / 34))]
        x += w
    for k, x in enumerate((140, 330, 1260, 1460, 1640)):
        els += [rect(x - 6, gy - 120, 12, 120, "#3a2a1c", at=-1), circ(x, gy - 160, 60, "#3f5a34", at=-1, op=.95)]
    els += track(120, 1100, gy + 30, tt)
    els += sledge_side(900, gy + 30, 260, t0 + .3, "block") + [lab(900, gy - 150, "1 tonne", t0 + .6, BONE, 30)] + chip(900, 200, "2016", GOLD, t0, 26)
    els += haulers(150, gy + 26, 10, 120, 58, t10 - .6, rows=1, rope_to=(760, gy - 6))
    els += chip(450, 470, "10 people", GOLD, t10 + .4, 30)
    # the bluestone, smaller
    gx, gy2 = 1180, 420
    els += [rect(1150, 250, 540, 230, "rgba(18,14,10,.75)", "rgba(255,236,206,.35)", 1.5, 10, t20 - .3, fx="pop")]
    els += track(1170, 1670, gy2 + 26, t20 - .2, 12)
    els += sledge_side(1590, gy2 + 26, 130, t20, "pillar")
    els += haulers(1190, gy2 + 22, 20, 46, 32, t20 + .2, dt=.04, rope_to=(1520, gy2 + 4))
    els += [lab(1420, 290, "2 tonnes: about 20", t20 + .8, BLUS_L, 28)]
    return {"base": "sky", "tod": "day", "ground": gy, "sun": [1500, 160, 22], "groundc": "#5d6b44", "cam": CAM, "els": els}


def jaw(x, y, s, at):
    """A cow's lower jaw in side view: a long low body, the ascending branch at the back, a row of six cheek teeth; returns (elements,
    the last tooth's box)."""
    P = lambda a, b: (x + a * s, y - b * s)
    bone = [P(-.52, .02), P(-.4, -.02), P(-.1, -.03), P(.2, -.06), P(.38, -.08), P(.48, -.01), P(.5, .12), P(.47, .3), P(.43, .37), P(.33, .38),
            P(.3, .22), P(.26, .1), P(.0, .09), P(-.3, .07), P(-.46, .1), P(-.54, .08)]
    els = [poly(bone, "#d8cab0", "rgba(60,50,40,.7)", 1.5, 0, curve=True)]
    for k in range(3):
        els.append(poly([P(-.54 + .025 * k, .09), P(-.51 + .025 * k, .09), P(-.53 + .025 * k, .16)], "#efe6cf", "rgba(60,50,40,.6)", 1, 0))
    teeth = []
    for k in range(6):
        tx = -.06 + k * .065
        box_ = (P(tx, .17)[0], P(tx, .17)[1], .055 * s, .08 * s)
        teeth.append(box_)
        els.append(rect(box_[0], box_[1], box_[2], box_[3], "#efe6cf", "rgba(60,50,40,.6)", 1.2, 2, 0))
    return [grp(els, at, "pop")], teeth[-1]


def ox(x, y, s, at, c=LILAC, style="claimed"):
    """An ox in side view as a dotted outline (a possibility)."""
    P = lambda a, b: (x + a * s, y - b * s)
    body = [P(-.5, .55), P(.2, .6), P(.42, .7), P(.55, .62), P(.56, .5), P(.4, .45), P(.35, .2), P(.32, 0), P(.24, 0), P(.22, .3), P(-.2, .3), P(-.26, 0),
            P(-.34, 0), P(-.38, .32), P(-.5, .4)]
    return [poly(body, "rgba(201,193,238,.08)", c, 2.5, at, style=style, fx="pop", curve=True), ln([P(.45, .7), P(.52, .82)], at, c, 2.5, style, draw=False)]


def s34():
    """Left: a cow's lower jaw, one tooth sliced into growth bands that light one by one (about 3000 BCE); a gold arrow west to 'Preseli
    Hills?'. Right: in lilac dots, two oxen pulling a sledge with a bluestone (cattle hauling?)."""
    t0, tc, tp = T("s34", "A cow's jaw"), T("s34", "holds a tooth"), T("s34", "Preseli Hills")
    jel, (tx, ty, tw, th) = jaw(420, 520, 560, t0)
    els = jel + chip(420, 250, "about 3000 BCE", GOLD, t0 + .4, 26) + [lab(420, 640, "a cow's tooth", tc + .6, BONE, 28)]
    els += [rect(tx - 4, ty - 4, tw + 8, th + 8, "none", GOLD, 3, 3, tc, fx="pop")]
    for k in range(9):
        els.append(rect(tx, ty + th * k / 9, tw, th / 9 - 1, "rgba(242,201,142,.85)", at=tc + .3 + .12 * k, fx="pop"))
    els += [arr([(tx + tw / 2, ty - 10), (tx - 60, 300), (190, 300)], tp - .3, GOLD, 3, dur=.7), pin(170, 300, "", tp + .2, GOLD),
            lab(170, 260, "Preseli Hills?", tp + .3, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s34z_add():
    """Cattle hauling? Two oxen in lilac dots pulling a sledge with a bluestone."""
    t0 = T("s34z", "Did cattle haul")
    gy = 600
    els = ox(860, gy, 200, t0) + ox(960, gy + 10, 200, t0 + .2)
    els += [ln([(1000, gy - 110), (1080, gy - 40)], t0 + .4, LILAC, 2.5, "claimed", dur=.3)]
    els += [grp([ln([(1080, gy - 14), (1500, gy - 14)], 0, LILAC, 8, "claimed", draw=False),
                 poly([(1100, gy - 24), (1480, gy - 30), (1480, gy - 90), (1100, gy - 80)], "rgba(111,128,144,.2)", LILAC, 2.5, 0, style="claimed")], t0 + .6, "pop")]
    els += [lab(1160, gy + 70, "cattle hauling?", t0 + 1.0, LILAC, 30, st="serif")]
    return els


def hammerstone(x, y, r, at, seed=1):
    return [poly(blob(x, y, r, r * .8, 12, .15, seed), "#b8a888", "rgba(255,236,206,.5)", 1.5, at, curve=True, fx="pop")]


def house(x, y, w, at, glow_=True, c="#7a6248"):
    h = w * .5
    els = [rect(x - w / 2, y - h, w, h, c, "rgba(255,226,180,.4)", 1.2, 2, 0), poly([(x - w / 2 - 6, y - h), (x, y - h - w * .42), (x + w / 2 + 6, y - h)], "#5a4630", "rgba(255,226,180,.4)", 1.2, 0)]
    if glow_:
        els += [rect(x - w * .1, y - h * .7, w * .2, h * .7, "#ffcf7a", at=0, op=.9)]
    return [grp(els, at, "rise")]


def s35():
    """A sarsen lies on the plain; a lilac dotted machine hovers over it (a lost civilisation?); then the builders' traces pop along the
    ground: an antler pick, hammerstones, a heap of chippings; at the right, their village inside a great bank: Durrington Walls, 3 km."""
    t0, tb, ta, th, tc, tv = (T("s35", "Some books"), T("s35", "But the builders"), T("s35", "antler picks"), T("s35", "stone hammers"),
                              T("s35", "heaps of"), T("s35", "Durrington Walls"))
    gy = 620
    els = sledge_side(560, gy, 420, -1, "sarsen")
    mach = [(380, 230), (740, 230), (700, 300), (420, 300)]
    els += [poly(mach, "rgba(201,193,238,.08)", LILAC, 3, t0 + .6, style="claimed", fx="pop"),
            ln([(420, 300), (390, 520)], t0 + .8, LILAC, 2.5, "claimed", dur=.4), ln([(700, 300), (730, 520)], t0 + .8, LILAC, 2.5, "claimed", dur=.4),
            poly([(470, 300), (650, 300), (690, 520), (430, 520)], "rgba(201,193,238,.1)", "none", 0, t0 + 1.0, fx="fade")]
    els += [lab(560, 190, "a lost civilisation?", t0 + 1.2, LILAC, 32, st="serif")]
    els += antler(180, 730, 140, -8, ta, worn=True) + [lab(250, 790 - 20, "antler pick", ta + .3, BONE, 24)]
    els += hammerstone(470, 735, 26, th, 2) + hammerstone(530, 742, 20, th + .2, 5) + [lab(500, 790 - 20, "hammers", th + .4, BONE, 24)]
    rr = random.Random(7)
    els += [poly(blob(rr.uniform(700, 820), rr.uniform(720, 750), rr.uniform(6, 12), rr.uniform(4, 8), 7, .3, k), "#b9ae96", at=tc + .03 * k, fx="pop") for k in range(22)]
    els += [lab(760, 790 - 20, "chippings", tc + .5, BONE, 24)]
    vx = 1400
    els += [poly(E(vx, gy - 20, 280, 60, 40, 180, 360), "none", "#a8b878", 10, tv - .4, op=.7)]
    for k, (dx, dy) in enumerate(((-180, 0), (-90, -14), (0, 0), (90, -12), (170, 4), (-40, 26), (60, 30))):
        els += house(vx + dx, gy + dy, 60, tv - .2 + .1 * k)
    els += [poly(blob(vx - 60, gy - 120, 24, 14, 9, .3, k), "rgba(200,200,200,.25)", at=tv + .4, curve=True) for k in range(2)]
    els += [lab(vx, gy - 140, "Durrington Walls", tv + .4, BONE, 30)] + chip(vx, gy + 110, "3 km away", GOLD, tv + .8, 24)
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1650, 360, 26], "groundc": "#4f5c38", "cam": CAM, "els": els}


def s36():
    """A great sarsen on a sledge on timber rails, hauled by a long double line of people on ropes; rope, timber, muscle; on 'turn up',
    more people walk in from the edges."""
    t0, tm, tu = T("s36", "No lost machines"), T("s36", "a great many"), T("s36", "It was getting")
    gy = 620
    els = track(980, 1700, gy + 24, -1, 14)
    els += sledge_side(1340, gy + 24, 560, -1, "sarsen")
    els += haulers(200, gy + 16, 40, 92, 38, t0 - .3, dt=.05, rope_to=(1060, gy - 20))
    els += [lab(640, 400, "rope", t0 + .6, BONE, 30), lab(1240, 560 + 130, "timber", t0 + 1.0, BONE, 30), lab(500, 760, "muscle", t0 + 1.4, BONE, 30)]
    for k in range(8):
        x = 120 + 30 * k if k < 4 else 1500 + 40 * (k - 4)
        els += fig(x, gy - 30 - 8 * (k % 2), 70, tu + .15 * k, "#2a2018", face=1 if k < 4 else -1)
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [300, 300, 30], "groundc": "#55623b", "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · Sun, ancestors and feasts
AXC, AXK = (470, 470), 11.5       # the axis plan: centre, units per metre (the axis runs left to right: south-west to north-east)


def AP(a, r):
    t = math.radians(a - AX)
    return (AXC[0] + AXK * r * math.cos(t), AXC[1] + AXK * r * math.sin(t))


def stone_plan(cx, cy, L, W, ang, fill, at, edge="rgba(20,16,12,.6)", fx=None):
    P = [(-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2), (-L / 2, W / 2)]
    a = math.radians(ang)
    pts = [(cx + p[0] * math.cos(a) - p[1] * math.sin(a), cy + p[0] * math.sin(a) + p[1] * math.cos(a)) for p in P]
    return poly(pts, fill, edge, 1.2, at, fx=fx)


def plan_monument(P, k, at=-1, ruin=False, rot_=0.0, sar="#a39a8c", blu="#6f8090"):
    """The stones in plan (top view) through a point mapping P(azimuth, r): the ring, the horseshoe, the bluestones, the Altar Stone."""
    els = []
    for kk in range(1, 31):
        a = ring_az(kk)
        x, y = P(a, RING_R)
        els.append(stone_plan(x, y, 2.1 * k, 1.1 * k, a + rot_, sar, at))
        x2, y2 = P(a + 6, RING_R)
        els.append(stone_plan(x2, y2, 3.2 * k, .9 * k, a + 6 + rot_, mix(sar, "#ffffff", .2), at))
    for (s1, s2), a, d, h, st in TRIL:
        cx, cy = P(a, d)
        els.append(stone_plan(cx, cy, 5.0 * k, 1.2 * k, a + rot_, mix(sar, "#ffffff", .15), at))
    for kk in range(40):
        x, y = P(AX + 4.5 + kk * 9, 11.7)
        els.append(dot(round(x, 1), round(y, 1), max(2.5, .35 * k), blu, at, None))
    x, y = P(AX + 180, 4.3)
    els.append(stone_plan(x, y, 4.9 * k, 1.0 * k, AX + 90 + rot_, ALTAR, at))
    return els


def sun_icon(x, y, r, at, c="#ffd27a", rays=12, red=False):
    col = "#ff7a4a" if red else c
    els = [circ(x, y, r, col, "#fff1c8", 2, 0)]
    for k in range(rays):
        a = 2 * math.pi * k / rays
        els.append(ln([(x + math.cos(a) * r * 1.3, y + math.sin(a) * r * 1.3), (x + math.cos(a) * r * 1.75, y + math.sin(a) * r * 1.75)], 0, col, 3, draw=False))
    return [grp(els, at, "pop"), gl(x, y, r * 4, at + .1, .5, "red" if red else "lamp")]


def s37():
    """Plan of Stonehenge with its axis drawn left to right (south-west to north-east): the Avenue runs off to the north-east past the Heel
    Stone; a gold axis line; the midsummer sun rising at the right; the midwinter sun setting at the left between the uprights of the
    tallest trilithon, over the Altar Stone."""
    t0, tw = T("s37", "At midsummer"), T("s37", "At midwinter")
    els = []
    av0 = 55
    for side in (-1, 1):
        els.append(ln([(AP(AX, av0)[0], AXC[1] + side * 11 * AXK), (1700, AXC[1] + side * 11 * AXK)], -1, "rgba(217,208,184,.55)", 10, draw=False))
    els += [lab(1250, AXC[1] - 11 * AXK - 22, "the Avenue", .5, DIM, 26)]
    els += plan_monument(lambda a, r: AP(a, r), AXK, -1, rot_=-AX + 90)
    hx, hy_ = AP(AX, 77)
    els += [stone_plan(hx, hy_, 2.4 * AXK, 2.0 * AXK, 30, "#a39a8c", -1), lab(hx, hy_ + 60, "Heel Stone", .7, BONE, 26)]
    els += [ln([(110, AXC[1]), (1700, AXC[1])], t0 - .3, GOLD, 3, dur=1.6)]
    els += sun_icon(1630, AXC[1], 34, t0 + .4) + [lab(1640, AXC[1] + 100, "midsummer sunrise", t0 + .7, GOLD, 30, "end")]
    gx, gy_ = AP(AX + 180, 6.6)
    els += sun_icon(140, AXC[1], 34, tw + .2, red=True) + [lab(150, AXC[1] + 100, "midwinter sunset", tw + .5, "#ff9a6a", 30, "start")]
    els += [gl(gx, gy_, 90, tw + .9, .6, "lamp", pulse=True)]
    return {"base": "plan", "bg": "#2c3620", "north": False, "cam": CAM, "els": els}


def s38():
    """A trench across the Avenue (a plan close-up): the two banks; in the trench's white chalk floor, natural grooves draw themselves as
    long stripes; the gold solstice axis lays itself along them."""
    t0, tl, tp = T("s38", "And digging"), T("s38", "lying along"), T("s38", "Perhaps the builders")
    els = [rect(80, 120, 1620, 680, "#3f4a2c", at=-1)]
    for y in (250, 690):
        els += [rect(80, y - 30, 1620, 60, "#5a6640", at=-1), rect(80, y - 8, 1620, 16, "#c9c0a8", at=-1, op=.6)]
    tx0, tx1, ty0, ty1 = 500, 1280, 200, 740
    els += [rect(tx0, ty0, tx1 - tx0, ty1 - ty0, CHALK, "#8f876e", 3, 4, t0, fx="pop")]
    rr = random.Random(3)
    for k in range(8):
        y = ty0 + 50 + k * 62 + rr.uniform(-10, 10)
        pts = [(tx0 + 20, y)] + [(tx0 + 20 + (tx1 - tx0 - 40) * j / 6, y + rr.uniform(-6, 6)) for j in range(1, 6)] + [(tx1 - 20, y + rr.uniform(-4, 4))]
        els += [ln(pts, t0 + .6 + .2 * k, "#9a8f74", 12, dur=1.0, curve=True), ln(pts, t0 + .7 + .2 * k, "#6e6450", 4, dur=1.0, curve=True)]
    els += [lab(890, 170, "Ice Age grooves", t0 + 2.0, BONE, 30)]
    els += [ln([(110, 470), (1700, 470)], tl, GOLD, 4, dur=1.4), lab(1500, 440, "the solstice line", tl + 1.0, GOLD, 28)]
    els += [lab(300, 470 - 30, "the Avenue", .4, DIM, 26)]
    return {"base": "plan", "bg": "#2c3620", "north": False, "cam": CAM, "els": els}


CALC, CALK = (889, 450), 12.0
STN_R = 27.0                      # the Station Stones, drawn closer than their real 43 m so the plan fits


def CP(a, r):
    return PP(a, r, CALC, CALK)


def s39():
    """The plan as a calendar (Darvill 2022): a chip '365 days?' (proposed, lilac); the 30 sarsens of the ring, the 5 trilithons and the 4
    Station Stones on a rectangle outside the ring."""
    t0 = T("s39", "In twenty twenty-two")
    els = plan_monument(CP, CALK, -1)
    for a in (AX - 68, AX + 68, AX + 112, AX + 248):
        x, y = CP(a, STN_R)
        els.append(stone_plan(x, y, 2.0 * CALK, 1.4 * CALK, a, "#a39a8c", -1))
    sx = [CP(a, STN_R) for a in (AX - 68, AX + 68, AX + 112, AX + 248)]
    els += [ln([sx[0], sx[1], sx[2], sx[3], sx[0]], -1, "rgba(217,208,184,.25)", 1.5, draw=False)]
    els += [lab(200, 190, "Timothy Darvill, 2022", t0 + .3, BONE, 28, "start")] + chip(1520, 190, "365 days?", LILAC, t0 + 2.0, 30)
    return {"base": "plan", "bg": "#2c3620", "north": False, "cam": CAM, "els": els}


def s39z_add():
    """Counting: the 30 sarsens light one by one (30 days), x 12 = 360; the 5 trilithons glow (+ 5 days); the 4 Station Stones pop (a leap
    year)."""
    t30, t12, t5, t4 = T("s39z", "Thirty sarsens"), T("s39z", "counted twelve"), T("s39z", "five trilithons"), T("s39z", "four Station")
    els = []
    for k in range(1, 31):
        x, y = CP(ring_az(k), RING_R)
        els.append(circ(x, y, 12, "rgba(242,201,142,.9)", "#fff1c8", 1.2, t30 + .05 * k, fx="pop"))
    els += [lab(889, 450 - 230, "30 days", t30 + .8, GOLD, 30)]
    els += chip(889, 450 + 6, "x 12 = 360", GOLD, t12 + .2, 28)
    for (s1, s2), a, d, h, st in TRIL:
        x, y = CP(a, d)
        els.append(gl(x, y, 60, t5 + .1 * (s1 - 51) / 2, .7, "lamp"))
    els += [lab(1250, 430, "+ 5 days", t5 + .6, GOLD, 30, "start")]
    for k, a in enumerate((AX - 68, AX + 68, AX + 112, AX + 248)):
        x, y = CP(a, STN_R)
        els += [circ(x, y, 26, "none", GOLD, 3, t4 + .2 * k, fx="draw", dur=.4)]
    x, y = CP(AX + 68, STN_R)
    els += [lab(x + 46, y + 56, "leap year", t4 + 1.0, GOLD, 30, "start")]
    return els


def s40():
    """Left: the ring of 30 stones with a lilac '12' at its heart, struck through (no twelve). Right: a horizon at dawn, the rising Sun for
    each day around the solstice crowding onto almost the same spot (days blur together)."""
    t0, t12, td = T("s40", "Two archaeoastronomers"), T("s40", "The number"), T("s40", "And near the solstice")
    cx, cy, r = 430, 450, 210
    els = [circ(cx, cy, r, "none", "rgba(203,188,168,.35)", 16, -1)]
    els += [stone_plan(cx + r * math.sin(math.radians(360 * k / 30)), cy - r * math.cos(math.radians(360 * k / 30)), 22, 12, 360 * k / 30 + 90, "#a39a8c", -1) for k in range(30)]
    els += [lab(cx, cy + 40, "12", t12, LILAC, 110, st="serif", fx="pop")] + [strike(cx - 80, cy + 30, cx + 80, cy - 70, t12 + .6, RED, 7)]
    els += [lab(cx, cy + r + 70, "no twelve in the stones", t12 + 1.0, BONE, 28)]
    els += [lab(889, 190, "Giulio Magli and Juan Antonio Belmonte", t0 + .2, BONE, 26)]
    hx0, hx1, hy = 900, 1660, 560
    els += [rect(hx0, 260, hx1 - hx0, hy - 260, "rgba(199,124,86,.18)", at=-1), rect(hx0, hy, hx1 - hx0, 160, "#2a2a22", at=-1),
            ln([(hx0, hy), (hx1, hy)], -1, "rgba(255,226,180,.6)", 2, draw=False)]
    xs = 1500
    for k, d in enumerate(range(-7, 8)):
        x = xs - 260 * (d / 7) ** 2 * (1 if d < 0 else .98)
        els.append(circ(x, hy - 18, 13, "#ffd27a", "#fff1c8", 1.2, td + .12 * k, fx="pop", op=.75))
    els += [poly([(1474, hy), (1490, hy), (1490, hy - 140), (1474, hy - 140)], "#8f877b", at=-1), poly([(1510, hy), (1526, hy), (1526, hy - 140), (1510, hy - 140)], "#8f877b", at=-1)]
    els += [lab(1280, 330, "days blur together", td + 1.6, GOLD, 30), lab(1280, hy + 70, "sunrise, day by day", td + .4, DIM, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


VMG = View(42.5, 51.0, -26.0, -11.5, (790, 470, 200, 260))


def s41():
    """Two halves: a circle of standing stones in grey at dusk (stone: the ancestors) and a circle of timber posts in warm brown with
    smoke and small figures (wood: the living); a small map of Madagascar between them."""
    t0, tm, ts, tw = T("s41", "Others see"), T("s41", "Madagascar"), T("s41", "stone is for"), T("s41", "and wood")
    gy = 560
    els = []
    for k in range(9):
        a = math.pi * k / 8
        x, y = 380 + 220 * math.cos(a + math.pi), gy - 10 + 50 * math.sin(a) * -1
        els += [grp([poly([(x - 18, y), (x + 18, y), (x + 15, y - 120), (x - 15, y - 120)], "#8f877b", "rgba(30,25,20,.6)", 1.2, 0)], t0 + .4 + .06 * k, "rise")]
    els += [lab(380, gy + 120, "stone: the ancestors", ts + .2, BONE, 30)]
    for k in range(10):
        a = math.pi * k / 9
        x, y = 1400 + 220 * math.cos(a + math.pi), gy - 10 + 50 * math.sin(a) * -1
        els += [grp([rect(x - 9, y - 160, 18, 160, "#8a5a32", "rgba(255,220,170,.4)", 1, 2, 0)], tw - .3 + .05 * k, "rise")]
    els += fig(1360, gy + 20, 80, tw + .3, "#2a2018") + fig(1440, gy + 26, 76, tw + .4, "#2a2018") + [gl(1400, gy - 20, 90, tw + .4, .6, "fire")]
    els += [lab(1400, gy + 120, "wood: the living", tw + .4, "#e8b88a", 30)]
    v = VMG
    els += [{"k": "group", "clip": [790, 470, 200, 260, 10], "els": [rect(780, 460, 220, 280, "#16303e", at=0), {"k": "map", "land": v.land(), "in": 0}],
             "in": round(tm - .2, 2)}, lab(890, 770, "Madagascar", tm + .2, BONE, 26)]
    els += [lab(889, 200, "Mike Parker Pearson and Ramilisonina", t0 + .6, DIM, 26)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [889, 380, 26], "groundc": "#3a4430", "cam": CAM, "els": els}


def urn(x, y, s, at, c="#c9a06a", fx="pop"):
    P = lambda a, b: (x + a * s, y - b * s)
    return [poly([P(-.3, 0), P(.3, 0), P(.42, .5), P(.32, .8), P(.38, .9), P(-.38, .9), P(-.32, .8), P(-.42, .5)], c, "rgba(255,236,206,.5)", 1.2, at, fx=fx, curve=True)]


def s42():
    """Twenty-five small urns in five rows (25 people); ten of them turn blue one by one (at least 10); a blue arrow carries them west to a
    pin: west Wales."""
    t0, t10, tw = T("s42", "And of twenty-five"), T("s42", "at least ten"), T("s42", "west Wales")
    els = []
    for k in range(25):
        x, y = 820 + 110 * (k % 5), 300 + 100 * (k // 5)
        els += urn(x, y + 40, 60, t0 + .05 * k)
    for j, k in enumerate((1, 3, 6, 8, 10, 12, 15, 19, 21, 23)):
        x, y = 820 + 110 * (k % 5), 300 + 100 * (k // 5)
        els += urn(x, y + 40, 60, t10 + .12 * j, "#7fb0e0")
    els += [lab(1040, 230, "25 people", t0 + .6, BONE, 30), lab(1420, 470, "at least 10", t10 + 1.4, "#9fd0ff", 30, "start")]
    els += [arr([(780, 470), (560, 470), (330, 470)], tw - .6, "#9fd0ff", 4, dur=.8, curve=False), pin(260, 470, "", tw, "#9fd0ff"),
            lab(260, 420, "west Wales", tw + .2, "#9fd0ff", 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s43():
    """Three clues in lilac dashes: a scroll (a legend), a bluestone with chips flying off (chipped for charms), a grave with a figure lying
    curled (injuries); a dashed bracket under all three: indirect clues."""
    t0, tl, tc, ti, td = T("s43", "Timothy Darvill"), T("s43", "a legend"), T("s43", "chipped for"), T("s43", "people with"), T("s43", "Intriguing clues")
    els = [lab(889, 190, "a place of healing?", t0 + .4, LILAC, 34, st="serif")]
    sx = 380
    els += [rect(sx - 110, 330, 220, 230, "rgba(201,193,238,.06)", LILAC, 2.5, 8, tl, fx="pop", style="inferred")]
    els += [ln([(sx - 80, 380 + 30 * k), (sx + 80 - 30 * (k % 2), 380 + 30 * k)], tl + .2, LILAC, 3, "inferred", dur=.3) for k in range(5)]
    els += [lab(sx, 610, "a legend", tl + .4, LILAC, 28)]
    bx = 889
    els += [poly([(bx - 50, 560), (bx + 50, 560), (bx + 40, 330), (bx - 40, 330)], "rgba(111,128,144,.25)", LILAC, 2.5, .5, style="inferred", fx="pop")]
    els += [poly(blob(bx + 60 + 26 * k, 380 - 18 * k, 9, 6, 7, .3, k), "rgba(201,193,238,.5)", LILAC, 1.5, tc + .3 + .15 * k, fx="pop") for k in range(4)]
    els += [lab(bx, 610, "chipped for charms", tc + .5, LILAC, 28)]
    gx = 1400
    els += [poly(E(gx, 470, 150, 70, 30), "rgba(201,193,238,.06)", LILAC, 2.5, ti, style="inferred", fx="pop")]
    els += [ln([(gx - 70, 470), (gx - 10, 440), (gx + 50, 460), (gx + 30, 500), (gx - 30, 500)], ti + .3, LILAC, 6, "inferred", dur=.6, curve=True),
            circ(gx - 90, 462, 16, "none", LILAC, 3, ti + .3)]
    els += [lab(gx, 610, "injuries", ti + .6, LILAC, 28)]
    els += bracket(260, 1540, 660, td, "indirect clues", LILAC, up=False, size=30, ty=716, style="inferred")
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def pig(x, y, s, at, c="#d8a890", face=1, fx="pop"):
    f = face
    P = lambda a, b: (x + f * a * s, y - b * s)
    body = [P(-.5, .2), P(-.45, .5), P(-.1, .6), P(.3, .55), P(.48, .42), P(.6, .36), P(.6, .26), P(.46, .24), P(.4, .1), P(.36, 0), P(.28, 0), P(.26, .14),
            P(-.24, .14), P(-.28, 0), P(-.36, 0), P(-.4, .14)]
    return [grp([poly(body, c, "rgba(60,30,20,.6)", 1.2, 0, curve=True), dot(*P(.4, .42), max(1.5, .03 * s), "#2a1a12", 0, None)], at, fx)]


def s44():
    """Durrington Walls on a winter evening: square houses with glowing doors inside a great bank, fires, people, pigs; at the right a
    year wheel: a piglet born in spring, an arc of nine months round to midwinter (a snowflake and a fire)."""
    t0, tp, tb, tm = T("s44", "Three kilometres"), T("s44", "Pig teeth"), T("s44", "born in spring"), T("s44", "eaten in midwinter")
    gy = 600
    els = []
    els += [poly(E(560, gy + 10, 470, 90, 40, 180, 360), "none", "#7a8a5a", 14, -1, op=.6)]
    for k, (dx, dy) in enumerate(((-300, 0), (-170, -20), (-40, 4), (90, -18), (220, 6), (330, -10), (-230, 40), (40, 44), (260, 46))):
        els += house(560 + dx, gy + dy, 74, t0 - .2 + .07 * k)
    els += [gl(430, gy + 60, 100, t0 + .4, .7, "fire", pulse=True), gl(700, gy + 70, 90, t0 + .6, .7, "fire", pulse=True)]
    els += pig(350, gy + 120, 90, tp - .4) + pig(800, gy + 124, 84, tp - .2, face=-1) + pig(560, gy + 140, 80, tp)
    els += fig(470, gy + 90, 90, t0 + .5, "#1a1410") + fig(650, gy + 96, 86, t0 + .7, "#1a1410", face=-1)
    els += [lab(560, 330, "Durrington Walls", t0 + .3, BONE, 32)]
    wx, wy, wr = 1360, 430, 200
    els += [circ(wx, wy, wr, "rgba(18,14,10,.85)", "rgba(255,236,206,.4)", 2, tp - .3, fx="pop")]
    for k in range(12):
        a = math.radians(-90 + 30 * k)
        els.append(ln([(wx + (wr - 16) * math.cos(a), wy + (wr - 16) * math.sin(a)), (wx + wr * math.cos(a), wy + wr * math.sin(a))], tp - .2, "rgba(255,236,206,.5)", 2, draw=False))
    sp = math.radians(-90 + 30 * 3)
    els += pig(wx + (wr - 70) * math.cos(sp) - 10, wy + (wr - 70) * math.sin(sp) + 20, 60, tb, "#f0c8b0")
    els += [lab(wx + 150, wy + wr + 46, "born in spring", tb + .3, "#c9e48f", 26)]
    els += [ln([(wx + (wr - 40) * math.cos(math.radians(-90 + 30 * 3 + 3 * j)), wy + (wr - 40) * math.sin(math.radians(-90 + 30 * 3 + 3 * j))) for j in range(91)],
               tb + .5, GOLD, 5, dur=1.6)]
    ex, ey = wx + (wr - 40) * math.cos(math.radians(-90 + 30 * 3 + 270)), wy + (wr - 40) * math.sin(math.radians(-90 + 30 * 3 + 270))
    els += [gl(ex, ey, 70, tm, .7, "fire"), lab(ex, ey - 50, "eaten in midwinter", tm + .2, GOLD, 26), lab(wx - 10, wy + 10, "9 months", tb + 1.6, GOLD, 30)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": False, "groundc": "#2c3324", "cam": CAM, "els": els}


def s45():
    """Britain: amber arrows draw from Scotland, north-east England and west Wales (and other places) to Durrington Walls, a small pig on
    each."""
    t0 = T("s45", "And their bones")
    v = VGB2
    dx, dy = v.p(-1.79, 51.19)
    els = [{"k": "map", "land": v.land(), "in": -1}, pin(dx, dy, "Durrington Walls", .3, GOLD, "start", 22, 30)]
    srcs = [((-3.6, 57.4), "Scotland"), ((-1.6, 54.8), "north-east England"), ((-4.8, 52.0), "west Wales"), ((-2.7, 53.5), None), ((-3.6, 50.7), None), ((0.6, 52.6), None)]
    for k, ((lo, la), name) in enumerate(srcs):
        x, y = v.p(lo, la)
        els += [arr([(x, y), ((x + dx) / 2 + 20, (y + dy) / 2), (dx, dy - 10)], t0 + .3 + .3 * k, AMBER, 3, dur=.8)]
        els += pig(x, y - 6, 46, t0 + .3 + .3 * k)
        if name:
            els += [lab(x - 30, y - 40, name, t0 + .5 + .3 * k, AMBER, 26, "end" if lo < -2 else "start")]
    return {"base": "map", "cam": CAM, "els": els}


TINY_CAM = Cam3(AZ(AX + 20, 78.0) + (7.0,), AX + 200, 1250, 889, 420)


def s46():
    """Stonehenge small in silhouette at dusk; three icons pop round it as named (a sun, a cremation urn, a fire with a pig); gold arcs
    join them to the stones."""
    t0, td, tf, tq = T("s46", "A monument to the Sun"), T("s46", "to the dead"), T("s46", "to the feast"), T("s46", "Quite possibly")
    cam = TINY_CAM
    els = sky_glow(cam.hy, 1500) + [rect(-60, cam.hy, 1900, 700, "#2c3324", at=-1)]
    els += render(monument("ruin"), cam, (300, 9), "dusk", -1, texture=False)
    els += sun_icon(500, 260, 40, t0 + .3) + urn(889, 230, 90, td) + [gl(1290, 250, 90, tf, .7, "fire")] + pig(1290, 280, 90, tf + .1)
    for k, (x, y) in enumerate(((500, 300), (889, 250), (1290, 290))):
        els.append(ln([(x, y + 30), ((x + 889) / 2, 420), (889, 470)], tq + .2 * k, GOLD, 2.5, dur=.7, curve=True))
    return {"base": "sky", "tod": "dusk", "ground": cam.hy, "sun": False, "cam": CAM, "els": els}


# ================================================================== CHAPTER 6 · The weighing
LROWS = [270, 390, 510, 630]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1200, y, grade, gc, gt, 28, "start")
    return out


def pic_tril(x, y, at):
    return [grp(tiny_tril(x, y + 30, 60, 0, "#a39a8c"), at, "pop")]


def pic_sledge(x, y, at):
    return [grp([ln([(x - 40, y + 20), (x + 40, y + 20)], 0, WOOD, 7, draw=False), poly([(x - 34, y + 14), (x + 34, y + 12), (x + 32, y - 14), (x - 32, y - 12)], BLUS, at=0)], at, "pop")]


def pic_slab(x, y, at):
    return slab_icon(x, y + 8, 70, at)


def pic_ring(x, y, at):
    return [grp([circ(x, y, 32, "none", LILAC, 3, 0, style="inferred")] + [dot(round(x + 32 * math.cos(a), 1), round(y + 32 * math.sin(a), 1), 4, LILAC, 0, None)
                                                                             for a in (3.4, 3.8, 4.2, 4.6)], at, "pop")]


def pic_sunline(x, y, at):
    return [grp([ln([(x - 44, y), (x + 44, y)], 0, GOLD, 3, draw=False), circ(x + 30, y - 4, 13, "#ffd27a", at=0)], at, "pop")]


def pic_urnfire(x, y, at):
    return [grp(urn(x - 18, y + 26, 44, 0, fx=None) + [circ(x + 24, y + 8, 12, "#ff9a4a", "#ffd08a", 2, 0)], at, "pop")]


def pic_dial(x, y, at):
    return [grp([circ(x, y, 32, "none", LILAC, 3, 0, style="inferred"), ln([(x, y), (x + 18, y - 18)], 0, LILAC, 3, draw=False)], at, "pop")]


def pic_star(x, y, at):
    return [grp([poly([(x + 30 * math.cos(math.radians(-90 + 36 * k)) * (1 if k % 2 == 0 else .45), y + 30 * math.sin(math.radians(-90 + 36 * k)) * (1 if k % 2 == 0 else .45))
                       for k in range(10)], "rgba(201,193,238,.12)", LILAC, 2.5, 0, style="claimed")], at, "pop")]


def ledger(title, at):
    return [rect(110, 170, 1560, 530, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, at), lab(140, 205 - 10, title, at + .2, GOLD, 26, "start", st="cap")]


def s47():
    """The ledger, panel one (how it was built): built in stages, about 3000 to 1600 BCE: Established."""
    tr, tg = T("s47", "Built in stages"), T("s47", "Established")
    els = ledger("How it was built", .2)
    els += lrow(0, tr, pic_tril, "built in stages, 3000 to 1600 BCE", "Established", tg, GRADE["established"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s48_add():
    t2, g2, t3, g3, t4, g4 = (T("s48", "Bluestones from Wales"), T("s48", "Strong evidence"), T("s48", "The Altar Stone"), T("s48", "Strong evidence", k=2),
                              T("s48", "A first Stonehenge"), T("s48", "Open question"))
    els = lrow(1, t2, pic_sledge, "bluestones from Wales, moved by people", "Strong evidence", g2, GRADE["strong"])
    els += lrow(2, t3, pic_slab, "the Altar Stone, from north-east Scotland", "Strong evidence", g3, GRADE["strong"])
    els += lrow(3, t4, pic_ring, "a first Stonehenge at Waun Mawn", "Open question", g4, GRADE["open"])
    return els


def s49():
    """The ledger, panel two (what it was for): the solstice line: Established; the dead and midwinter feasts: Strong evidence; a 365-day
    calendar, or healing: Awaiting evidence."""
    t1, g1, t2, g2, t3, g3 = (T("s49", "Built on the solstice"), T("s49", "Established"), T("s49", "A place for the dead"), T("s49", "Strong evidence"),
                              T("s49", "A calendar"), T("s49", "Awaiting evidence"))
    els = ledger("What it was for, and the legends", .2)
    els += lrow(0, t1, pic_sunline, "built on the solstice line", "Established", g1, GRADE["established"])
    els += lrow(1, t2, pic_urnfire, "for the dead, and midwinter feasts", "Strong evidence", g2, GRADE["strong"])
    els += lrow(2, t3, pic_dial, "a 365-day calendar, or healing", "Awaiting evidence", g3, GRADE["awaiting"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s50_add():
    t4, g4 = T("s50", "Merlin's stones"), T("s50", "Ruled out")
    els = lrow(3, t4, pic_star, "Merlin, a lost civilisation, far older stones", "Ruled out", g4, GRADE["ruled"])
    els += [strike(170, LROWS[3] + 30, 262, LROWS[3] - 30, g4 + .2, RED, 5)]
    return els


def s51():
    """What would change our minds: four wanted items in lilac dashes, as named: a sandstone outcrop with a slab-shaped gap (a quarry in
    Caithness); a stone with an equals sign to a Stonehenge stone (a Waun Mawn match); boulders in a gravel section (Welsh boulders); a
    stonehole with a date (an older stonehole)."""
    t0, tq, tw, tb, to = (T("s51", "What would change"), T("s51", "A Neolithic quarry"), T("s51", "A stone at Waun"), T("s51", "Welsh boulders"),
                          T("s51", "Or stones set"))
    els = [lab(889, 180, "what would change our minds", t0, GOLD, 30, st="cap")]
    xs = (290, 690, 1090, 1490)
    # 1 a quarry with a gap
    x = xs[0]
    els += [poly([(x - 150, 560), (x - 130, 380), (x + 140, 360), (x + 160, 560)], "rgba(201,193,238,.06)", LILAC, 2.5, tq, style="inferred", fx="pop"),
            poly([(x - 60, 470), (x + 60, 466), (x + 60, 500), (x - 60, 504)], "#120e0b", LILAC, 2.5, tq + .3, style="inferred", fx="pop"),
            lab(x, 620, "a quarry in Caithness", tq + .4, LILAC, 26)]
    # 2 a match
    x = xs[1]
    els += [poly([(x - 110, 560), (x - 60, 560), (x - 66, 400), (x - 104, 400)], "rgba(201,193,238,.06)", LILAC, 2.5, tw, style="inferred", fx="pop"),
            lab(x, 500, "=", tw + .3, LILAC, 60, st="big"),
            poly([(x + 60, 560), (x + 110, 560), (x + 104, 400), (x + 66, 400)], "rgba(201,193,238,.06)", LILAC, 2.5, tw + .5, style="inferred", fx="pop"),
            lab(x, 620, "a Waun Mawn match", tw + .6, LILAC, 26)]
    # 3 boulders in gravels
    x = xs[2]
    els += [rect(x - 150, 400, 300, 160, "rgba(201,193,238,.05)", LILAC, 2.5, 6, tb, style="inferred", fx="pop")]
    els += [poly(blob(x - 90 + 60 * k, 480 + 20 * (k % 2), 22, 16, 9, .25, k), "rgba(111,128,144,.35)", LILAC, 2, tb + .3 + .1 * k, style="inferred", fx="pop")
            for k in range(4)]
    els += [lab(x, 620, "Welsh boulders", tb + .6, LILAC, 26)]
    # 4 an older stonehole
    x = xs[3]
    els += [poly([(x - 70, 420), (x + 70, 420), (x + 50, 540), (x - 50, 540)], "#120e0b", LILAC, 2.5, to, style="inferred", fx="pop")]
    els += chip(x, 370, "before 3000 BCE", LILAC, to + .3, 24) + [lab(x, 620, "an older stonehole", to + .6, LILAC, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s52():
    """The close: the hero again, by moonlight, on its own panel: stars over the stones, the Altar Stone glowing softly gold; a faint gold
    thread rises from it and runs north across the sky."""
    tc = T("s52", "and carried it")
    top, (ax, ay) = altar_pts()
    els = hero("night")
    els += [gl(ax, ay, 160, .4, .55, "lamp", pulse=True), ln(top + top[:1], .6, "#ffe7b0", 3, dur=.8)]
    els += [ln([(ax, ay - 10), (ax + 120, ay - 260), (ax + 420, 200), (1700, 120)], tc, GOLD, 2.5, dur=2.4, curve=True, op=.8)]
    st = hero_base("night")
    st.update(cam=CAM, els=els, moon=[1480, 150, 26])
    return st


# ================================================================== the film
def _stub(name):
    def f():
        return {"base": "dark", "stars": 20, "cam": CAM, "els": [lab(889, 470, name, -1, DIM, 40, st="serif")]}
    return f


def _stub_add():
    return []


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "About five metres", "s1z"), (1, "In {2024", "s2"), (2, "How did this", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "And in one way", "s6")], {"chapter": "Who built it, and when?"}),
    (1, 1, "collision", "s7", [(0, "On the floor", "s8"), (1, "Antler holds", "s9")], {}),
    (1, 2, "reversal", "s10", [(1, "Then, around {2500", "s11"), (1, "Their builders", "s12"), (2, "Then they rearranged", "s13")], {}),
    (1, 3, "tag", "s14", [], {}),
    (2, 0, "world", "s15", [(1, "The rocks tell", "s16")], {"chapter": "Bluestones from Wales"}),
    (2, 1, "collision", "s17", [(1, "The diggers found", "s18")], {}),
    (2, 2, "reversal", "s19", [(0, "Their suggestion", "s19m"), (1, "Others aren't", "s20"), (1, "Even its excavators", "s20b")], {}),
    (2, 3, "tag", "s21", [], {}),
    (3, 0, "world", "s22", [(1, "In {2020", "s23")], {"chapter": "A stone from Scotland"}),
    (3, 1, "collision", "s24", [(1, "So a team", "s25"), (1, "In {2024", "s25z")], {}),
    (3, 2, "reversal", "s26", [(1, "So, by land", "s27")], {}),
    (3, 3, "tag", "s28", [], {}),
    (4, 0, "world", "s29", [(1, "And for a long", "s30")], {"chapter": "Moving the giants"}),
    (4, 1, "collision", "s31", [(0, "And in {2026", "s32")], {}),
    (4, 2, "reversal", "s33", [(1, "And they may", "s34"), (1, "Did cattle haul", "s34z")], {}),
    (4, 3, "cost", "s35", [], {}),
    (4, 4, "tag", "s36", [], {}),
    (5, 0, "world", "s37", [(1, "And digging", "s38")], {"chapter": "Sun, ancestors and feasts"}),
    (5, 1, "collision", "s39", [(0, "Thirty sarsens", "s39z"), (1, "Two archaeoastronomers", "s40")], {}),
    (5, 2, "reversal", "s41", [(0, "And of twenty-five", "s42"), (1, "Timothy Darvill and", "s43")], {}),
    (5, 3, "cost", "s44", [(0, "And their bones", "s45")], {}),
    (5, 4, "tag", "s46", [], {}),
    (6, 0, "weigh", "s47", [(1, "Bluestones from Wales", "s48"), (2, "Built on the solstice", "s49"), (3, "Merlin's stones", "s50")], {"chapter": "The weighing"}),
    (6, 1, "test", "s51", [], {}),
    (6, 2, "close", "s52", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s1z": ("s1", [1.7, 874, 548], "s1z_add"),
    "s3": ("s1", [1, 889, 500], "s3_add"),
    "s10": ("s7", [1, 889, 500], "s10_add"),
    "s20": ("s19", [1, 889, 500], "s20_add"),
    "s20b": ("s19", [1, 889, 500], "s20b_add"),
    "s21": ("s15", [1, 889, 500], "s21_add"),
    "s28": ("s27", [1, 889, 500], "s28_add"),
    "s25z": ("s25", [1.3, 1120, 430], "s25z_add"),
    "s30": ("s29", [1, 889, 500], "s30_add"),
    "s34z": ("s34", [1.4, 1140, 470], "s34z_add"),
    "s39z": ("s39", [1.1, 889, 470], "s39z_add"),
    "s48": ("s47", [1, 889, 500], "s48_add"),
    "s50": ("s49", [1, 889, 500], "s50_add"),
}


def _segments(script):
    """The narration each shot has on screen (lines joined by newlines), from the beats with their markers (a chapter beat's first
    sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[@%s]" % sid)
        text = "\n".join(lines)
        parts = re.split(r"\[@([\w]+)\]", text)
        head = parts[0]
        if kw.get("chapter"):
            acts = [m.start() for m in SENT.finditer(head) if m.start() > 0]
            if acts:
                head = head[acts[0]:]
        if role != "title":
            say[frm] = say[frm] + "\n" + head if frm in say else head
        for k in range(1, len(parts), 2):
            say[parts[k]] = parts[k + 1].strip("\n")
    return say


def film():
    script = json.load(open(SCRIPT, encoding="utf-8"))
    SAY.clear(); SAY.update(_segments(script))
    g = globals()
    panels = {}
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in ALIASES and sid not in panels:
                panels[sid] = (g.get(sid) or _stub(sid))()
    ids = list(panels) + [a for a in ALIASES]
    idx = {s: i for i, s in enumerate(ids)}
    shots = [panels[s] for s in panels] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[idx[sid]] = idx[root]
        cams[idx[sid]] = [z] + list(cam[1:])
        tags[z] = (g.get(fn) or _stub_add)() if fn else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-stonehenge", "code": "LF.26", "series": script["series"], "title": script["title"], "case": "stonehenge",
          "verdict": "solid", "claim": "Who built Stonehenge, how did its stones get there, and what was it for?", "mood": "mystery",
          "hook_text": "How did this stone get *here*?", "beats": beats, "shots": shots,
          "sources": "Clarke et al. 2024 (doi:10.1038/s41586-024-07652-1) · Clarke et al. 2026 (doi:10.1002/jqs.70080) · "
                     "Nash et al. 2020 (doi:10.1126/sciadv.abc0133) · Parker Pearson et al. 2019 (doi:10.15184/aqy.2018.111) · "
                     "Parker Pearson et al. 2021 (doi:10.15184/aqy.2020.239) · Bevins et al. 2022 (doi:10.1016/j.jasrep.2022.103556) · "
                     "Clarke & Kirkland 2026 (doi:10.1038/s43247-025-03105-3) · Darvill 2022 (doi:10.15184/aqy.2022.5) · "
                     "Magli & Belmonte 2023 (doi:10.15184/aqy.2023.33) · Madgwick et al. 2019 (doi:10.1126/sciadv.aau6078)",
          "post": "A six-tonne slab at the heart of Stonehenge came from the far north-east of Scotland. The ditch and its antler picks, the "
                  "sarsens and the Welsh bluestones, the Waun Mawn idea, glaciers and sledges, the solstice line, the calendar debate, the "
                  "cremations and the midwinter feasts, and the popular claims, weighed.",
          "hashtags": ["#Stonehenge", "#Neolithic", "#Archaeology", "#AncientBritain", "#Prehistory", "#WeighItYourself"],
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
