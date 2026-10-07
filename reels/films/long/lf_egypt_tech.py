"""LF.31 · Under Giza · Egypt's Lost Machines? (16:9 long film, one wall).

The script is films/long/lf-egypt-tech/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s53; s5, the title, is the intro card over the
hero), drawn while it is said. The hero is a hard-stone jar built as a small 3-D model (a surface of revolution of 40 facets with a
few hundred stone grains on it) that turns slowly in a beam of light; it returns for the vases' landing and for the close.
Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted = claimed (the challengers' claims
are lilac and dotted).

Facts: the script's facts_added (Fomitchev-Zamilov 2025; Lacau & Lauer 1959, 1965; Quibell 1934, 1935; Aston 1994; Petrie 1883; UCL
Petrie Museum UC16036; Dunn 1984, 1998, 2010; Gorelick & Gwinnett 1983; Stocks 1993, 2001, 2023; Kruglyakov 2018; Odler & Kmosek 2025;
Thot Sign List U24; Davies 1943; Mariette 1857, 1882; Malinine, Posener & Vercoutter 1968; Dodson 2005; Brugsch 1891; Sessa et al.
2026; Tuck, Stacey & Starkey 1977; Vyse 1840-42; Tallet 2017; Tallet & Lehner 2021; Lehner 1997).

Engine workaround (as in lf_stonehenge.py, lf_troy.py and lf_antikythera.py): the wall only adds elements to a panel on its first
visit, at a beat start or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique
tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item
(built on that step's clock). Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25
syllables a second).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-egypt-tech/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-egypt-tech/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-egypt-tech RC_FILMS_EPS=/tmp/claude-0/sbx_lf-egypt-tech/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-egypt-tech/boards python3 films.py long.lf_egypt_tech
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import glow, label, dot, box, ellipse, strike
from giza import Section, BASE as GB, SLOPE

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-egypt-tech", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
GRAN, GRAN_L, GRAN_D = "#b98a7c", "#e3b9ab", "#5c4440"      # Aswan granite: mid, lit, shade
DIOR, DIOR_L = "#5f5c63", "#e9e5dc"                         # speckled gneiss / diorite: body, grains
BAS = "#2d2d32"                                             # basalt
TRAV = "#e9dcc4"                                            # travertine
COP, COP_D = "#c8743c", "#7a3f1c"                           # copper
LIME, LIME_L, LIME_D = "#d8c49c", "#f2dcb4", "#8f7456"      # limestone
OCHRE = "#c4472c"
SKIN = "#e8d6b8"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#c9e48f", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}
C30 = math.cos(math.pi / 6)


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
    if sid not in SAY:
        return 1.0
    ws, _ = _clock(SAY[sid])
    want = [_norm(p) for w in phrase.replace("-", " ").split() for p in [w] if _norm(p)]
    hits = [i for i in range(len(ws)) if [w for w, _ in ws[i:i + len(want)]] == want]
    assert len(hits) >= k, (sid, phrase, SAY[sid][:200])
    return round(lead + ws[hits[k - 1]][1], 2)


def DUR(sid):
    return round(_clock(SAY[sid])[1], 2) if sid in SAY else 10.0


def _find(line_, phrase):
    """Index in the raw line where `phrase` starts, ignoring the ^ stress marks."""
    keep = [i for i, ch in enumerate(line_) if ch != "^"]
    flat = "".join(line_[i] for i in keep)
    assert flat.count(phrase) == 1, (phrase, line_)
    return keep[flat.index(phrase)]


def _mark(line_, phrase, tag):
    """Insert `tag` at the start of the sentence that begins with `phrase`: before its [p:]/[act:]/[sfx:]/[tune:] tags, after a [d:] tag."""
    j = _find(line_, phrase)
    while j > 0 and line_[j - 1] in "^*":           # a stressed or emphasised first word keeps its marks: the tag goes before them
        j -= 1
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


def gdim(e, f):
    """Dim a group: a group carries no opacity of its own on the page, so each drawn child gets it (multiplied into its own)."""
    for c in e.get("els", []):
        if c.get("k") == "group":
            gdim(c, f)
        else:
            c["op"] = round((c["op"] if c.get("op") is not None else 1.0) * f, 3)
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
    """A pill with a coloured rim and its words (grades, dates); z = the camera zoom it is seen at."""
    w = (len(t) * size * .56 + 44) / z
    h = size * 1.7 / z
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36 / z, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


def tick(x, y, at, c=GREEN, s=1.0, w=6):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": w, "fx": "draw", "dur": .45, "in": round(at, 2)}


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


def blob(cx, cy, rx, ry, n=22, jit=.18, seed=1, rot=0):
    """An irregular closed outline (a boulder, a chip, a cloud)."""
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
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up', 'pull' (both forward and low), 'lift', 'press'
    (both forward and down, pressing on something at waist height). lean > 0 tilts the body forward."""
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
    elif arms == "press":
        els += [ln([(X(-.1, .75), Y(.75)), (X(.28, .52), Y(.52))], at, c, aw, draw=False), ln([(X(.1, .75), Y(.75)), (X(.3, .5), Y(.5))], at, c, aw, draw=False)]
    elif arms == "lift":
        els += [ln([(X(-.1, .76), Y(.76)), (X(-.2, 1.06), Y(1.06))], at, c, aw, draw=False), ln([(X(.1, .76), Y(.76)), (X(.2, 1.06), Y(1.06))], at, c, aw, draw=False)]
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return [e]


def seated(x, y, h, at, c="#1a1410", face=1, fx="rise", op=None, arms="drill"):
    """A craftsman seated on a low stool, facing `face`, feet on y; h = his standing height. arms 'drill': both hands forward at
    shoulder height on a drill's crank; 'hold': forearms forward and low."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    els = [circ(X(.06), Y(.66), .075 * h, c, at=at),                                                        # head
           poly([(X(-.1), Y(.58)), (X(.12), Y(.58)), (X(.1), Y(.3)), (X(-.08), Y(.28))], c, at=at),          # torso
           poly([(X(-.08), Y(.3)), (X(.26), Y(.31)), (X(.27), Y(.24)), (X(-.06), Y(.22))], c, at=at),       # thigh
           poly([(X(.22), Y(.3)), (X(.27), Y(.3)), (X(.25), Y(0)), (X(.19), Y(0))], c, at=at),               # shin
           rect(X(-.14) if f > 0 else X(.06), Y(.22), .2 * h, .03 * h, c, at=at)]                             # stool
    aw = max(2.5, .04 * h)
    if arms == "drill":
        els += [ln([(X(.08), Y(.55)), (X(.3), Y(.5)), (X(.36), Y(.56))], at, c, aw, draw=False),
                ln([(X(.06), Y(.53)), (X(.26), Y(.44)), (X(.34), Y(.47))], at, c, aw, draw=False)]
    else:
        els += [ln([(X(.06), Y(.55)), (X(.2), Y(.4)), (X(.36), Y(.4))], at, c, aw, draw=False)]
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return [e]


# ================================================================== stone vessels
# A vessel profile: [(height, radius)] from the foot up, radius 1 at the widest; the hero is a broad-shouldered jar with a short neck
# and a flat, slightly flared rim (the shape of the Early Dynastic hard-stone jars).
JAR = [(round(h * 1.1, 3), r) for h, r in [(0.0, .45), (.06, .60), (.18, .82), (.36, .97), (.52, 1.0), (.68, .96), (.84, .84), (.98, .66),
                                           (1.10, .48), (1.20, .36), (1.32, .33), (1.40, .38), (1.46, .46)]]
JAR_IN = .30                     # the mouth
BOWL = [(0.0, .52), (.04, .66), (.14, .84), (.28, .96), (.40, 1.0)]
TALL = [(0.0, .40), (.10, .58), (.40, .74), (.80, .80), (1.15, .72), (1.40, .52), (1.52, .40), (1.62, .44)]
CYL = [(0.0, .62), (.06, .66), (1.3, .70), (1.42, .82)]


def _r3(v):
    return [round(v[0], 4), round(v[1], 4), round(v[2], 4)]


def jar_items(prof=JAR, rin=JAR_IN, nseg=40, body=DIOR, grain=(DIOR_L, "#bdb8b0", "#1d1c20"), weights=(.62, .23, .15), n=340, seed=7,
              edge="rgba(70,68,74,.55)", ew=.7):
    """The jar as iso items: a surface of revolution (y up, radius 1 at the belly) in `nseg` facets, a flat rim, a dark mouth, and `n`
    stone grains (small facets just outside the surface, culled on the far side, so they turn with the jar)."""
    it = []
    for i in range(len(prof) - 1):
        (y0, r0), (y1, r1) = prof[i], prof[i + 1]
        dy, dr = y1 - y0, r1 - r0
        L = math.hypot(dy, dr)
        for j in range(nseg):
            a0, a1 = 2 * math.pi * j / nseg, 2 * math.pi * (j + 1) / nseg
            am = (a0 + a1) / 2
            p = [[r0 * math.cos(a0), y0, r0 * math.sin(a0)], [r0 * math.cos(a1), y0, r0 * math.sin(a1)],
                 [r1 * math.cos(a1), y1, r1 * math.sin(a1)], [r1 * math.cos(a0), y1, r1 * math.sin(a0)]]
            it.append({"t": "quad", "p": [_r3(q) for q in p], "n": _r3([dy / L * math.cos(am), -dr / L, dy / L * math.sin(am)]), "c": body,
                       "edge": edge, "ew": ew})
    yt, rt = prof[-1]
    for j in range(nseg):
        a0, a1 = 2 * math.pi * j / nseg, 2 * math.pi * (j + 1) / nseg
        p = [[rt * math.cos(a0), yt, rt * math.sin(a0)], [rt * math.cos(a1), yt, rt * math.sin(a1)],
             [rin * math.cos(a1), yt, rin * math.sin(a1)], [rin * math.cos(a0), yt, rin * math.sin(a0)]]
        it.append({"t": "quad", "p": [_r3(q) for q in p], "n": [0, 1, 0], "c": mix(body, "#ffffff", .12), "edge": edge, "ew": ew})
    it.append({"t": "quad", "p": [_r3([rin * math.cos(2 * math.pi * j / nseg), yt - .002, rin * math.sin(2 * math.pi * j / nseg)]) for j in range(nseg)],
               "n": [0, 1, 0], "c": "#0c0b0d", "edge": "rgba(255,236,206,.25)", "ew": 1})
    # grains: area-weighted over the bands, small irregular facets tangent to the surface
    rnd = random.Random(seed)
    bands = []
    for i in range(len(prof) - 1):
        (y0, r0), (y1, r1) = prof[i], prof[i + 1]
        bands.append((math.hypot(y1 - y0, r1 - r0) * (r0 + r1) / 2, i))
    tot = sum(a for a, _ in bands)
    for k in range(n):
        u = rnd.uniform(0, tot)
        for a, i in bands:
            u -= a
            if u <= 0:
                break
        (y0, r0), (y1, r1) = prof[i], prof[i + 1]
        dy, dr = y1 - y0, r1 - r0
        L = math.hypot(dy, dr)
        s = rnd.uniform(.08, .92)
        phi = rnd.uniform(0, 2 * math.pi)
        rr, yy = (r0 + s * dr) * 1.012, y0 + s * dy
        c = [rr * math.cos(phi), yy, rr * math.sin(phi)]
        tu = [-math.sin(phi), 0, math.cos(phi)]
        tv = [dr / L * math.cos(phi), dy / L, dr / L * math.sin(phi)]
        size = rnd.uniform(.014, .034)
        pts = []
        for m in range(5):
            ang = 2 * math.pi * m / 5 + rnd.uniform(-.3, .3)
            q = size * rnd.uniform(.6, 1.2)
            pts.append(_r3([c[d] + q * (math.cos(ang) * tu[d] + .8 * math.sin(ang) * tv[d]) for d in range(3)]))
        roll = rnd.random()
        col = grain[0] if roll < weights[0] else (grain[1] if roll < weights[0] + weights[1] else grain[2])
        it.append({"t": "quad", "p": pts, "n": _r3([dy / L * math.cos(phi), -dr / L, dy / L * math.sin(phi)]), "c": col, "edge": "none",
                   "ew": .01, "over": .03})
    return it


def jar_grains(prof=JAR, n=1100, seed=7, grain=("#ffffff", "#d6d1c8", "#121114"), weights=(.55, .3, .15), size=(.006, .019)):
    """Stone grains as iso items: small irregular facets just outside the jar's surface, culled on the far side, so they turn with it."""
    it, rnd, bands = [], random.Random(seed), []
    for i in range(len(prof) - 1):
        (y0, r0), (y1, r1) = prof[i], prof[i + 1]
        bands.append((math.hypot(y1 - y0, r1 - r0) * (r0 + r1) / 2, i))
    tot = sum(a for a, _ in bands)
    for k in range(n):
        u = rnd.uniform(0, tot)
        for a, i in bands:
            u -= a
            if u <= 0:
                break
        (y0, r0), (y1, r1) = prof[i], prof[i + 1]
        dy, dr = y1 - y0, r1 - r0
        L = math.hypot(dy, dr)
        t = rnd.uniform(.05, .95)
        phi = rnd.uniform(0, 2 * math.pi)
        rr, yy = (r0 + t * dr) * 1.008, y0 + t * dy
        c = [rr * math.cos(phi), yy, rr * math.sin(phi)]
        tu = [-math.sin(phi), 0, math.cos(phi)]
        tv = [dr / L * math.cos(phi), dy / L, dr / L * math.sin(phi)]
        sz = rnd.uniform(*size)
        pts = []
        for m in range(5):
            ang = 2 * math.pi * m / 5 + rnd.uniform(-.35, .35)
            q = sz * rnd.uniform(.55, 1.25)
            pts.append(_r3([c[d] + q * (math.cos(ang) * tu[d] + .85 * math.sin(ang) * tv[d]) for d in range(3)]))
        roll = rnd.random()
        col = grain[0] if roll < weights[0] else (grain[1] if roll < weights[0] + weights[1] else grain[2])
        # a horizontal normal: the kit culls a facet by a fixed view direction, right for a view from about el .45; a jar seen from lower
        # down (el .2) would show grains of the far shoulder above its outline. Horizontal normals cull exactly the far half.
        it.append({"t": "quad", "p": pts, "n": _r3([math.cos(phi), 0, math.sin(phi)]), "c": col, "edge": "none", "ew": .01})
    return it


def jar_body(x, y, s, prof=JAR, rin=JAR_IN, tone=DIOR, el=.2, at=-1):
    """The jar's body in 2-D, as the iso camera sees it (a surface of revolution keeps one outline as it turns): the silhouette with the
    foot's front edge and the rim, shaded by the kit's diagonal light (k-shade), soft highlight bands on the lit left side, the rim's top
    and the dark mouth."""
    hw = lambda r: r * 1.2247 * s
    ry = lambda r: r * 1.4142 * el * s
    h0, r0 = prof[0]
    ht, rt = prof[-1]
    right = [(x + hw(r), y - h * s) for h, r in prof]
    top = E(x, y - ht * s, hw(rt), ry(rt), 24, 0, -180)[1:-1]
    left = [(x - hw(r), y - h * s) for h, r in reversed(prof)]
    foot = E(x, y - h0 * s, hw(r0), ry(r0), 24, 180, 0)[1:-1]
    sil = right + top + left + foot
    els = [poly(E(x, y + 4, hw(r0) * 1.25, ry(r0) * 1.5 + 6, 36), "#000000", at=at, op=.45),
           poly(sil, mix(tone, "#000000", .2), "rgba(255,236,206,.3)", 1.2, at),
           poly(sil, "url(#k-shade)", "none", 0, at)]
    inner = prof[1:-1]
    for k in range(10):                      # a soft highlight on the lit left side: ten nested bands, each a little narrower
        a_, b_ = -.92 + .04 * k, .5 - .095 * k
        pts = [(x + a_ * hw(r), y - h * s) for h, r in inner] + [(x + b_ * hw(r), y - h * s) for h, r in reversed(inner)]
        els.append(poly(pts, "#ffffff", at=at, curve=True, op=.032))
    for k in range(4):                       # a faint rim of reflected light on the right edge
        a_ = .78 + .04 * k
        pts = [(x + a_ * hw(r), y - h * s) for h, r in inner] + [(x + .97 * hw(r), y - h * s) for h, r in reversed(inner)]
        els.append(poly(pts, "#ffe2b8", at=at, curve=True, op=.03))
    els += [poly(E(x, y - ht * s, hw(rt), ry(rt), 40), mix(tone, "#ffffff", .3), "rgba(255,236,206,.5)", 1.2, at),
            poly(E(x, y - ht * s + 2, hw(rin), ry(rin), 40), "#0b0a0c", "rgba(255,236,206,.35)", 1, at)]
    return els


def jar_iso(x, y, s, at=-1, spin=6.0, az=20, el=.2, prof=JAR, tone="#46444b", n=1100, seed=7, **kw):
    """The turning jar: its foot centred on (x, y); s = units per jar radius (the drawn half-width is 1.22 s)."""
    return jar_body(x, y, s, prof, JAR_IN, tone, el, at) + [
        {"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": jar_grains(prof, n, seed, **kw), "in": at}]


def jar_outline(x, y, s, el=.2, prof=JAR, k=1.0):
    """The jar's silhouette on the panel (a surface of revolution keeps one outline as it turns)."""
    hw = lambda r: r * 1.2247 * s * k
    right = [(x + hw(r), y - h * s) for h, r in prof]
    left = [(x - hw(r), y - h * s) for h, r in reversed(prof)]
    return right + left


def ring_y(x, y, s, h, r, el=.2, half="front"):
    """The projected circle at height h, radius r (an ellipse: the front half is its lower half)."""
    rx, ry, cy = r * 1.2247 * s, r * 1.4142 * el * s, y - h * s
    return E(x, cy, rx, ry, 30, 0, 180) if half == "front" else E(x, cy, rx, ry, 60)


def vessel(x, y, h, prof=JAR, tone=DIOR, grain=None, at=0, fx="pop", op=None, n=40, seed=1, lit=.35, w=None):
    """A 2-D stone vessel (side view, foot on y, height h): a body shaded in vertical strips (light from the upper left), a dark mouth,
    and optional grains of stone clamped inside its outline."""
    H = prof[-1][0]
    s = h / H
    W = w if w is not None else s
    pts_r = [(x + r * W, y - hh * s) for hh, r in prof]
    pts_l = [(x - r * W, y - hh * s) for hh, r in reversed(prof)]
    sharp = lambda a_, b_: [a_[0], a_[0]] + a_[1:-1] + [a_[-1], a_[-1], b_[0], b_[0]] + b_[1:-1] + [b_[-1], b_[-1]]   # doubled corners: no overshoot
    els = [poly(sharp(pts_r, pts_l), mix(tone, "#000000", .35), "rgba(255,236,206,.35)", 1.2, 0, curve=True)]
    for k, (a, b, t) in enumerate(((-.82, .55, .18), (-.62, .25, .32), (-.48, .02, .45), (-.36, -.12, .55))):
        sp = [(x + b * r * W, y - hh * s) for hh, r in prof]
        sl = [(x + a * r * W, y - hh * s) for hh, r in reversed(prof)]
        els.append(poly(sharp(sp, sl), mix(tone, "#ffffff", t * lit), "none", 0, 0, curve=True, op=.55 + .1 * k))
    hl = [(x - .55 * r * W, y - hh * s) for hh, r in prof[1:-1]] + [(x - .4 * r * W, y - hh * s) for hh, r in reversed(prof[1:-1])]
    els.append(poly(hl, "#ffffff", "none", 0, 0, curve=True, op=.16))
    rt = prof[-1][1]
    wide = rt > .6                                   # an open bowl shows its hollow, not a black hole
    els.append(poly(E(x, y - H * s, rt * W, rt * W * .2, 24), mix(tone, "#000000", .62) if wide else "#0f0d0c", "rgba(255,236,206,.5)", 1.2, 0))
    if wide:
        els.append(poly(E(x - rt * W * .12, y - H * s + rt * W * .03, rt * W * .7, rt * W * .1, 20), mix(tone, "#000000", .8), "none", 0, 0, op=.8))
    if grain:
        rnd = random.Random(seed)
        for _ in range(n):
            hh = rnd.uniform(.05 * H, .97 * H)
            r = _interp(prof, hh)
            xx = x + rnd.uniform(-.88, .88) * r * W
            els.append(circ(xx, y - hh * s, rnd.uniform(1.2, 2.8) * max(.6, h / 200), rnd.choice(grain), at=0))
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return [e]


def _interp(prof, hh):
    for (h0, r0), (h1, r1) in zip(prof, prof[1:]):
        if h0 <= hh <= h1:
            return r0 + (r1 - r0) * (hh - h0) / max(1e-6, h1 - h0)
    return prof[-1][1]


def beam(x, top, bottom, w0, w1, at=-1, op=.07):
    """A beam of warm light from above: two soft trapezoids, a glow at the source and a pool on the floor."""
    return [poly([(x - w0, top), (x + w0, top), (x + w1, bottom), (x - w1, bottom)], "rgba(255,226,170,1)", at=at, op=op),
            poly([(x - w0 * .45, top), (x + w0 * .45, top), (x + w1 * .55, bottom), (x - w1 * .55, bottom)], "rgba(255,236,200,1)", at=at, op=op * .9),
            gl(x, top + 20, 260, at, .45),
            poly(E(x, bottom, w1 * 1.05, 42, 40), "rgba(255,226,170,1)", at=at, op=.1),
            gl(x, bottom - 10, w1 * .9, at, .22)]


def motes(x0, x1, y0, y1, n=40, at=-1, seed=5):
    return [{"k": "stars", "n": n, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "seed": seed, "in": at}]


# ================================================================== COLD OPEN
HX, HY, HS = 980, 728, 250            # the hero jar: foot centre, scale (belly half-width 1.22 x 268 = 328)


def hero_base(at=-1):
    """Black, a beam of light from above, motes in it, the jar turning in it."""
    els = beam(HX, 112, HY, 70, 380, at) + motes(HX - 300, HX + 300, 150, HY - 20, 36, at)
    els += jar_iso(HX, HY, HS, at, spin=6.0)
    return els


def s1():
    """HERO: on black, a speckled hard-stone jar turning slowly in a vertical beam of warm light, motes drifting. On 'five thousand years
    old', a chip; on 'copper', a copper chisel glances off the stone with a spark."""
    t5, tc = T("s1", "five thousand"), T("s1", "copper")
    els = hero_base(-1)
    els += chip(470, 330, "over 5,000 years old", GOLD, t5, 30)
    # the chisel, its edge touching the belly on the right
    bx, by = HX + 1.2247 * HS * .99, HY - .55 * HS
    ch = [(bx + 8, by - 6), (bx + 260, by - 70), (bx + 272, by - 50), (bx + 20, by + 12)]
    els += [poly(ch, "url(#k-copper)", "rgba(255,226,190,.6)", 1.2, tc, fx="rise"),
            poly([(bx + 200, by - 54), (bx + 262, by - 70), (bx + 272, by - 50), (bx + 210, by - 34)], COP_D, at=tc)]
    sp = [ln([(bx + 4, by), (bx + 4 + 34 * math.cos(a), by + 34 * math.sin(a))], tc + .5, "#ffe2a8", 3, dur=.25) for a in (-2.4, -1.6, -.9, -.2, .6)]
    els += sp + [gl(bx + 4, by, 70, tc + .5, .7), lab(bx + 150, by + 90, "copper won't scratch it", tc + .9, "#e8b87a", 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s2_add():
    """Scan: pale-blue rings sweep down the jar, top to bottom; a dashed outline locks on; the claim, dotted lilac."""
    t0 = .4
    els = []
    hs = [1.42, 1.3, 1.2, 1.1, .98, .86, .74, .62, .5, .38, .26, .14, .04]
    for k, h in enumerate(hs):
        r = _interp(JAR, h)
        els.append(ln(ring_y(HX, HY, HS, h, r * 1.01), t0 + .16 * k, BLUE, 2, dur=.5, op=.75))
    els.append(poly(jar_outline(HX, HY, HS, k=1.03), "none", BLUE, 2.4, t0 + 2.3, style="inferred", fx="draw", dur=1.0))
    tl = T("s2", "only a")
    els += [lab(1480, 400, "only a machine?", tl, LILAC, 34), ln([(1395, 420), (1310, 470)], tl + .2, LILAC, 2.5, "claimed", dur=.5)]
    return els


def s3():
    """Three vignettes, each in a pool of lamplight, as named: a granite core with a gold spiral groove; a giant box in a tunnel with a
    person for scale; the Great Pyramid at night with a dotted beam."""
    tc, tb, tp = T("s3", "a granite core"), T("s3", "Stone boxes"), T("s3", "And a pyramid")
    els = []
    # 1 the core
    cx, cy = 380, 620
    els += [gl(cx, cy - 120, 260, tc, .5), grp(core(cx, cy, 120, 300, gold=True), tc), lab(cx, 700, "a spiral groove", tc + .4, GOLD, 30)]
    # 2 the box in a tunnel
    bx, by = 760, 620
    tun = [poly([(bx - 120, by + 20), (bx - 120, 330), (bx + 130, 260), (bx + 380, 330), (bx + 380, by + 20)], "#241c16", "rgba(255,236,206,.18)", 1.5, tb)]
    els += tun + [gl(bx + 130, 520, 280, tb, .55),
                  {"k": "box3d", "x": bx - 40, "y": by, "w": 300, "h": 181, "d": 110, "lid": True, "lidH": 56, "tone": "#3b3632", "light": "#5a534c", "in": tb, "fx": "rise"},
                  {"k": "person", "x": bx + 330, "y": by, "h": 132, "t": False, "color": "#d8c7a6", "in": round(tb + .3, 2), "fx": "rise"},
                  lab(bx + 130, 700, "up to 60 tonnes", tb + .4, GOLD, 30)]
    # 3 the pyramid at night
    px, py = 1440, 620
    els += [gl(px, py - 80, 300, tp, .35),
            {"k": "pyramid", "x": px, "y": py, "w": 330, "in": tp, "fx": "rise"},
            ln([(px + 10, py - 120), (px + 140, py - 250), (px + 230, py - 340)], tp + .5, LILAC, 4, "claimed", dur=.8),
            gl(px + 10, py - 120, 60, tp + .4, .8, pulse=True),
            lab(px, 700, "a power plant?", tp + .6, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def core(x, y, w, h, gold=False, n=11, tone=GRAN, taper=.88):
    """A granite drill core, foot on y, a little narrower at the top (taper), grooved; gold=True lights one groove up as a spiral."""
    wt = w * taper
    body = [(x - w / 2, y), (x - wt / 2, y - h), (x + wt / 2, y - h), (x + w / 2, y)]
    els = [poly(body, GRAN_D, "rgba(255,236,206,.35)", 1.2, 0)]
    for k, (a, b, t) in enumerate(((-.5, .3, .25), (-.42, .05, .45), (-.3, -.1, .6))):
        els.append(poly([(x + a * w, y), (x + a * wt, y - h), (x + b * wt, y - h), (x + b * w, y)], mix(GRAN_D, GRAN_L, t), at=0, op=.8))
    rnd = random.Random(3)
    for _ in range(70):
        yy = rnd.uniform(y - h + 6, y - 6)
        ww = w + (wt - w) * (y - yy) / h
        els.append(circ(x + rnd.uniform(-.44, .44) * ww, yy, rnd.uniform(1.2, 2.6), rnd.choice(["#f4e6dc", "#2a1e1c", "#e9c7b8"]), at=0, op=.8))
    els.append(poly(E(x, y - h, wt / 2, wt * .16, 30), GRAN_L, "rgba(255,236,206,.5)", 1.2, 0))
    for i in range(1, n + 1):
        yy = y - h + i * h / (n + 1)
        ww = w + (wt - w) * (y - yy) / h
        els.append(ln([(x - ww / 2, yy + ww * .05), (x, yy + ww * .14), (x + ww / 2, yy - ww * .05)], 0, "rgba(40,20,20,.6)", 1.6, curve=True, draw=False))
    if gold:
        i = n // 2
        yy = y - h + i * h / (n + 1)
        ww = w + (wt - w) * (y - yy) / h
        els.append(ln([(x - ww / 2, yy + ww * .05), (x, yy + ww * .14), (x + ww / 2, yy - ww * .05)], 0, GOLD, 3.5, curve=True, draw=False))
    return els


def s4_add():
    return qmark(470, 560, .3, 130)


# ================================================================== CHAPTER 1 · The impossible vases
def s6():
    """Djoser's Step Pyramid at dusk, the rock cut away beneath it: two long galleries fill with tiny vessels, row by row; on 'names of
    earlier kings', three vessels glow gold with a little inscription."""
    tj, tg, tk = T("s6", "Jars, bowls"), T("s6", "packed into"), T("s6", "names of earlier")
    gy = 430
    els = [rect(0, gy, W_, 600, "#2a2119", at=-1)]
    for k, yy in enumerate((470, 520, 585, 660, 740)):
        els.append(ln([(0, yy), (W_, yy + (8 if k % 2 else -6))], -1, "rgba(255,236,206,.07)", 2, draw=False))
    els += [{"k": "step", "x": 889, "y": gy, "w": 520, "h": 260, "n": 6, "in": -1},
            gl(889, gy - 120, 420, -1, .18),
            ln([(840, gy), (840, 540)], -1, "rgba(255,236,206,.35)", 3, "inferred", draw=False),
            ln([(1010, gy), (1010, 620)], -1, "rgba(255,236,206,.35)", 3, "inferred", draw=False)]
    gal = [(560, 540, 1320), (640, 620, 1400)]
    for x0, yy, x1 in gal:
        els.append(rect(x0, yy, x1 - x0, 46, "#120e0b", "rgba(255,236,206,.45)", 1.5, 3, -1))
    cols = [TRAV, TRAV, TRAV, "#d9cbb2", DIOR, GRAN, BAS]
    rnd = random.Random(11)
    k = 0
    for gi, (x0, yy, x1) in enumerate(gal):
        for row in range(2):
            for j in range(int((x1 - x0 - 20) / 15)):
                xx = x0 + 12 + j * 15 + (7 if row else 0)
                if xx > x1 - 10:
                    continue
                col = rnd.choice(cols)
                at = tg + .02 * k
                els.append(poly([(xx - 5, yy + 40 - row * 18), (xx + 5, yy + 40 - row * 18), (xx + 6, yy + 33 - row * 18), (xx + 3, yy + 27 - row * 18),
                                 (xx - 3, yy + 27 - row * 18), (xx - 6, yy + 33 - row * 18)], col, at=at, fx="pop"))
                k += 1
    els += [lab(400, 250, "Djoser's Step Pyramid", tj - .2, GOLD, 32)] + chip(400, 300, "c. 2650 BCE", DIM, tj + .2, 24)
    els += [lab(1460, 540, "30,000 to 40,000", -1, GOLD, 36, "start", st="serif"), lab(1460, 585, "stone vessels", -1, DIM, 28, "start")]
    for xx, yy in ((720, 562), (980, 640), (1240, 562)):
        els += [gl(xx, yy, 46, tk, .9), rect(xx - 9, yy - 38, 18, 24, "none", AU, 2, 2, tk + .2, fx="pop")]
    els += [lab(980, 730, "many carry older kings' names", tk + .4, AU, 28)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1500, 330, 34], "cam": CAM, "els": els}


def s7():
    """A shelf of vessels in lamplight: a crowd of pale travertine jars at the back ('most: travertine'); in front, as named, a granite jar,
    a basalt jar and a speckled gneiss bowl; a worn copper chisel beside them."""
    tg, tb, tn, tw = T("s7", "granite"), T("s7", "basalt"), T("s7", "speckled gneiss"), T("s7", "Heavy, tough")
    els = [gl(889, 520, 700, -1, .22), rect(120, 560, 1540, 14, "#5a4634", "rgba(255,236,206,.3)", 1, 2, -1)]
    rnd = random.Random(4)
    profs = [JAR, TALL, CYL, JAR, BOWL, TALL, JAR, CYL, TALL, JAR, BOWL, TALL, JAR]
    for k, pr in enumerate(profs):
        xx = 200 + k * 116
        hh = rnd.uniform(110, 150) if pr is not BOWL else 60
        els += vessel(xx, 560, hh, pr, TRAV, at=-1, fx=None, op=.5, lit=.5)
    els += [lab(889, 360, "most: travertine", -1, DIM, 30)]
    front = [(520, GRAN, ["#f4e6dc", "#2a1e1c", "#e9c7b8"], JAR, "granite", tg, 240, 140),
             (889, BAS, None, TALL, "basalt", tb, 250, 105),
             (1250, DIOR, [DIOR_L, "#1d1c20", "#bdb8b0"], BOWL, "speckled gneiss", tn, 95, 150)]
    for xx, tone, gr, pr, name, t, hh, ww in front:
        els += [gl(xx, 690 - hh * .5, hh * 1.2, t, .45)]
        els += vessel(xx, 700, hh, pr, tone, gr, t, "rise", n=90, seed=int(xx), lit=.45, w=ww)
        els += [lab(xx, 748, name, t + .3, BONE, 28)]
    cx, cy = 1520, 720
    els += [poly([(cx - 110, cy), (cx + 120, cy - 40), (cx + 128, cy - 22), (cx - 104, cy + 16)], "url(#k-copper)", "rgba(255,226,190,.6)", 1.2, tw, fx="rise"),
            poly(E(cx - 108, cy + 8, 9, 12, 16), COP_D, at=tw),
            lab(cx, 640, "they wear tools down", tw + .4, AMBER, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s8():
    """Scanning: a dark granite vase on a turntable; a structured-light scanner on a tripod throws pale-blue stripes across it; a laptop
    fills with points that become the vase's outline."""
    t0, tm = .4, T("s8", "maps millions")
    vx, vy = 640, 640
    els = [gl(vx, 520, 380, -1, .28), poly(E(vx, vy + 8, 170, 30, 40), "#2c2420", "rgba(255,236,206,.35)", 1.5, -1)]
    els += vessel(vx, vy, 290, JAR, GRAN, ["#f4e6dc", "#2a1e1c", "#e9c7b8"], -1, None, n=120, seed=8)
    els += [arr([(vx + 190, vy + 30), (vx + 120, vy + 46), (vx + 40, vy + 48)], .6, DIM, 2, dur=.6)]
    # the scanner on its tripod
    sx, sy = 1060, 420
    els += [ln([(sx, sy + 40), (sx - 70, 700)], -1, "#8a8278", 4, draw=False), ln([(sx, sy + 40), (sx + 60, 700)], -1, "#8a8278", 4, draw=False),
            ln([(sx, sy + 40), (sx, 700)], -1, "#8a8278", 4, draw=False),
            rect(sx - 90, sy - 30, 180, 70, "#2a2a30", "rgba(255,236,206,.4)", 1.5, 10, -1),
            circ(sx - 55, sy + 5, 16, "#0d0f14", "#9fd0ff", 2, -1), circ(sx + 55, sy + 5, 16, "#0d0f14", "#9fd0ff", 2, -1),
            rect(sx - 14, sy - 8, 28, 26, "#9fd0ff", at=-1, op=.8)]
    for k in range(9):
        yy = vy - 40 - k * 27
        els.append(poly([(sx - 14, sy + 5), (sx - 14, sy + 8), (vx + 60, yy + 6), (vx + 60, yy)], "rgba(159,208,255,1)", at=t0 + .05 * k, op=.12))
        els.append(ln([(vx - 120 + abs(k - 4) * 12, yy + 3), (vx, yy + 12), (vx + 120 - abs(k - 4) * 12, yy + 3)], t0 + .05 * k, BLUE, 2, curve=True, dur=.4, op=.8))
    # the laptop and its point cloud
    lx, ly = 1440, 600
    els += [poly([(lx - 170, ly), (lx + 170, ly), (lx + 200, ly + 26), (lx - 200, ly + 26)], "#3a3a40", "rgba(255,236,206,.35)", 1, -1),
            rect(lx - 160, ly - 230, 320, 222, "#0b0d12", "rgba(255,236,206,.45)", 2, 8, -1)]
    out = jar_outline(lx, ly - 30, 110, k=.62)
    rnd = random.Random(2)
    pts = []
    for k in range(70):
        a, b = out[k % len(out)], out[(k + 1) % len(out)]
        u = rnd.random()
        pts.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
    for k in range(60):
        hh = rnd.uniform(.05, 1.4)
        r = _interp(JAR, hh) * 110 * 1.2247 * .62
        pts.append((lx + rnd.uniform(-r, r) * .9, ly - 30 - hh * 110))
    for k, (px, py) in enumerate(pts):
        els.append(dot(round(px, 1), round(py, 1), 2.4, BLUE, round(1.4 + (tm + .4 - 1.4) * k / len(pts), 2)))
    els += [lab(vx, 255, "a private collection", .5, DIM, 28), lab(sx, 330, "3D scanner", .9, BLUE, 28), lab(lx, 680, "millions of points", tm + .6, BLUE, 26)]
    els += chip(260, 200, "from 2023", GOLD, .2, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def s9():
    """Precision: a slice of a vase as a circle, its tiny error exaggerated against a perfect dashed circle; a thousandth of an inch beside
    a human hair, to scale; on 'lathe', a lilac dotted lathe (headstock, spinning vase, fixed blade)."""
    tl = T("s9", "this is the work")
    cx, cy, r = 430, 450, 210
    rnd = random.Random(6)
    wob = [(cx + (r + 5 * math.sin(3 * a) + 3 * math.sin(7 * a + 1)) * math.cos(a), cy + (r + 5 * math.sin(3 * a) + 3 * math.sin(7 * a + 1)) * math.sin(a))
           for a in [2 * math.pi * k / 90 for k in range(90)]]
    els = [poly(wob, "rgba(95,92,99,.55)", BONE, 2.4, .3, curve=True, fx="pop"),
           circ(cx, cy, r, "none", BLUE, 2.4, .9, style="inferred", fx="draw"),
           lab(cx, cy + r + 50, "a slice through a vase", .5, DIM, 26),
           lab(cx, cy - r - 30, "error shown 100 times larger", 1.2, BLUE, 24)]
    # 25 micrometres vs a 70 micrometre hair, at 3 units per micrometre
    k_ = 3.0
    hx, hy = 980, 450
    els += [rect(hx - 25 * k_ / 2, hy - 140, 25 * k_, 14, GOLD, at=1.6, fx="pop"),
            lab(hx, hy - 160, "a thousandth of an inch", 1.7, GOLD, 26),
            circ(hx, hy + 60, 35 * k_, "#3a2a1c", "#e8c49a", 2.4, 2.4, fx="pop"),
            lab(hx, hy + 60 + 35 * k_ + 40, "a human hair, end on", 2.6, DIM, 26)]
    # the lathe, claimed: headstock, spindle, the vase lying on its side (foot to the left), a fixed blade under its belly, a curved arrow
    L = LILAC
    lx, ly, vs = 1380, 450, 70
    vo = [(lx - 30 - yy, ly + xx) for xx, yy in jar_outline(0, 0, vs)]
    els += [rect(lx - 250, ly - 80, 110, 160, "rgba(201,193,238,.06)", L, 2.5, 6, tl, style="claimed", fx="pop"),
            ln([(lx - 140, ly), (lx + 150, ly)], tl + .2, L, 3, "claimed", dur=.5),
            poly(vo, "rgba(201,193,238,.08)", L, 2.5, tl + .3, style="claimed", fx="pop", curve=True),
            arr([(lx - 20, ly - 110), (lx + 25, ly - 126), (lx + 70, ly - 110)], tl + .6, L, 2.5, "claimed", dur=.5),
            poly([(lx + 2, ly + 175), (lx + 22, ly + 92), (lx + 38, ly + 96), (lx + 32, ly + 175)], "rgba(201,193,238,.15)", L, 2.5, tl + .8, style="claimed", fx="pop"),
            rect(lx - 280, ly + 175, 460, 16, "rgba(201,193,238,.06)", L, 2, 4, tl, style="claimed", fx="pop"),
            lab(lx - 50, ly + 245, "a lathe? (claimed)", tl + 1.0, L, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s10():
    """The catch: left, a vase on a dark velvet stand under a spotlight, a blank tag ('no find-spot', dotted gold frame); right, as named,
    a vase lying in a tomb cut into a layered section ('the tomb', 'the layer', 'the date'; green frame); then a small modern lathe."""
    tt, tl, td, tm = T("s10", "the tomb"), T("s10", "the layer"), T("s10", "the date"), T("s10", "still turned")
    els = [rect(150, 230, 640, 470, "rgba(242,201,142,.03)", GOLD, 2.4, 14, .2, style="claimed", fx="pop"),
           lab(470, 205, "no find-spot", .4, GOLD, 30)]
    vx, vy = 360, 600
    els += [gl(vx, 380, 240, -1, .5), poly([(vx - 110, vy), (vx + 110, vy), (vx + 120, vy + 60), (vx - 120, vy + 60)], "#3a1c22", "rgba(255,236,206,.25)", 1.2, -1),
            poly(E(vx, vy, 110, 16, 30), "#4a2630", "rgba(255,236,206,.3)", 1, -1)]
    els += vessel(vx, vy + 4, 250, TALL, DIOR, [DIOR_L, "#1d1c20"], -1, None, n=90, seed=3, w=105)
    els += [ln([(vx + 80, vy - 150), (vx + 140, vy - 190)], .8, DIM, 2, draw=False),
            poly([(vx + 140, vy - 205), (vx + 220, vy - 205), (vx + 220, vy - 170), (vx + 140, vy - 170)], "#efe3c8", "rgba(0,0,0,.4)", 1, .8, fx="pop"),
            lab(vx + 180, vy - 179, "?", .9, "#5a3a20", 30, st="lab")]
    # right: a dated tomb in its layer
    x0, x1 = 980, 1620
    els += [rect(x0, 230, x1 - x0, 470, "rgba(143,217,176,.03)", GREEN, 2.4, 14, .2, fx="pop")]
    lay = [(250, "#7a6248"), (330, "#a8946c"), (430, "#6f5a44"), (560, "#8f7a5e"), (640, "#5e4a38")]
    for k, (yy, c) in enumerate(lay):
        nxt = lay[k + 1][0] if k + 1 < len(lay) else 690
        els.append(rect(x0 + 10, yy, x1 - x0 - 20, nxt - yy, c, at=-1, op=.55))
    els += [rect(1130, 440, 340, 112, "#15100c", "rgba(255,236,206,.5)", 2, 6, tt, fx="pop"),
            gl(1300, 500, 120, tt + .2, .4),
            grp(vessel(0, 0, 150, TALL, GRAN, ["#f4e6dc", "#2a1e1c"], 0, None, n=40, seed=5, w=58), tt + .3, "pop", tr="translate(1378 500) rotate(-90)"),
            lab(1300, 420, "the tomb", tt + .2, BONE, 26),
            rect(x0 + 10, 430, x1 - x0 - 20, 130, "none", GREEN, 3, 0, tl, fx="pop"),
            lab(x0 + 30, 600, "the layer", tl + .2, GREEN, 26, "start")]
    els += chip(1500, 300, "a date", GREEN, td, 26)
    # a modern lathe turning a stone vase, inside the left frame
    mx, my = 610, 560
    els += [rect(mx - 60, my - 36, 36, 72, "#3a3d44", "rgba(255,236,206,.45)", 1.2, 4, tm, fx="pop"),
            ln([(mx - 24, my), (mx + 120, my)], tm + .1, "#9aa0a8", 3, draw=False),
            grp(vessel(0, 0, 90, TALL, GRAN, None, 0, None, w=34), tm + .2, "pop", tr="translate(%d %d) rotate(90)" % (mx - 10, my)),
            rect(mx - 70, my + 40, 220, 10, "#3a3d44", at=tm, fx="pop"),
            lab(mx + 40, my + 90, "made today?", tm + .4, AMBER, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def vicon(x, y, c, at, s=1.0, fx="pop"):
    """A small vase icon, foot on y."""
    pr = [(0, .5), (.25, .95), (.55, 1.0), (.85, .6), (1.0, .42), (1.08, .5)]
    hh, ww = 46 * s, 16 * s
    pts = [(x + r * ww, y - h * hh / 1.08) for h, r in pr] + [(x - r * ww, y - h * hh / 1.08) for h, r in reversed(pr)]
    return poly(pts, c, "rgba(0,0,0,.35)", 1, at, fx=fx, curve=True)


def s11():
    """The fair test: three groups of small vase icons count in as named: 19 gold (Petrie Museum, documented), 25 blue (machine-made,
    modern), 24 green (handmade, modern); a chip names the journal."""
    tn, tm, th = T("s11", "nineteen vases"), T("s11", "twenty-five machine-made"), T("s11", "twenty-four handmade")
    els = chip(889, 190, "peer reviewed · npj Heritage Science · Dec 2025", GOLD, .4, 26)
    for gx_, w_ in ((330, 330), (889, 330), (1440, 386)):
        els += [rect(gx_ - w_ / 2, 300, w_, 450, "rgba(242,201,142,.03)", "rgba(242,201,142,.35)", 2, 18, .6, style="inferred", fx="pop")]
    els += [gl(889, 520, 420, .6, .18, "blue")]
    groups = [(330, 19, 5, AU, tn, "19 · Petrie Museum", "documented"), (889, 25, 5, BLUE, tm, "25 · machine-made", "modern"),
              (1440, 24, 6, GREEN, th, "24 · handmade", "modern")]
    for gx, n, cols, c, t0, name, sub in groups:
        rows = (n + cols - 1) // cols
        for k in range(n):
            col, row = k % cols, k // cols
            x = gx + (col - (cols - 1) / 2) * 56
            y = 380 + row * 72
            els.append(vicon(x, y, c, t0 + .05 * k))
        els += [lab(gx, 330 - 40, name, t0 - .1, c, 30), lab(gx, 380 + rows * 72 + 10, sub, t0 + .4, DIM, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s12():
    """The result: a schematic quality chart (less round to the right, more off-centre upwards): the machine-made dots in a tight cluster
    at the bottom left, the handmade dots spread in the middle, the ancient outer surfaces among them; an inset cross-section shows an
    inside that is round but off-centre."""
    tc, ta, ti = T("s12", "The machine-made vases"), T("s12", "The ancient vases'"), T("s12", "Their insides")
    ox, oy, W, H = 230, 700, 860, 470
    els = [ln([(ox, oy), (ox + W, oy)], .2, DIM, 2.5, dur=.6), ln([(ox, oy), (ox, oy - H)], .2, DIM, 2.5, dur=.6),
           arr([(ox + W - 80, oy + 34), (ox + W, oy + 34)], .5, DIM, 2, dur=.4, curve=False), lab(ox + W - 100, oy + 44, "less round", .5, DIM, 24, "end"),
           arr([(ox - 34, oy - H + 80), (ox - 34, oy - H)], .5, DIM, 2, dur=.4, curve=False), lab(ox - 4, oy - H - 14, "more off-centre", .5, DIM, 24, "start")]
    rnd = random.Random(12)
    for k in range(25):
        x, y = ox + 70 + rnd.gauss(0, 18), oy - 60 + rnd.gauss(0, 14)
        els.append(dot(round(x, 1), round(y, 1), 8, BLUE, round(tc + .03 * k, 2)))
    els += [lab(ox + 70, oy - 120, "machine-made", tc + .6, BLUE, 26)]
    hand = []
    for k in range(24):
        x, y = ox + 380 + rnd.gauss(0, 120), oy - 250 + rnd.gauss(0, 85)
        hand.append((x, y))
        els.append(dot(round(x, 1), round(y, 1), 8, GREEN, round(tc + .9 + .02 * k, 2)))
    els += [lab(ox + 560, oy - 420, "handmade, modern", tc + 1.3, GREEN, 26)]
    for k in range(19):
        x, y = ox + 400 + rnd.gauss(0, 110), oy - 240 + rnd.gauss(0, 80)
        els.append(dot(round(x, 1), round(y, 1), 9, AU, round(ta + .05 * k, 2)))
    els += [lab(ox + 400, oy + 56, "ancient vases: outer surface", ta + .8, AU, 28)]
    # inset: round but off-centre
    cx, cy = 1430, 420
    els += [rect(1210, 200, 440, 440, "rgba(18,13,10,.6)", "rgba(255,236,206,.3)", 2, 16, ti - .2, fx="pop"),
            circ(cx, cy, 160, "#5f5c63", BONE, 2.4, ti),
            circ(cx + 22, cy + 16, 104, "#120f0e", BLUE, 2.4, ti + .4),
            dot(cx, cy, 5, BONE, ti + .8), dot(cx + 22, cy + 16, 5, BLUE, ti + .9),
            lab(cx, 610, "inside: round, off-centre", ti + 1.0, BLUE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s13():
    """The landing: the hero jar again, smaller, turning in its beam; beside it a seated craftsman in warm silhouette holds a polishing
    stone to its belly; label 'the work of hands'."""
    th = T("s13", "the work of")
    x, y, s_ = 980, 690, 165
    els = beam(x, 112, y, 50, 270, -1) + motes(x - 220, x + 220, 150, y - 20, 30, -1, seed=9)
    els += jar_iso(x, y, s_, -1, spin=6.0, seed=7, n=420)
    els += [gl(x - 330, y - 170, 260, .2, .35)]
    els += driller_sil(560, y, 500, (772, 576), (770, 612), .3, c="#3a2618")
    els += [poly(blob(x - 1.2247 * s_ * .97 - 16, y - .6 * s_, 20, 14, 9, .2, 3), "#a8977e", "rgba(0,0,0,.4)", 1, .6, fx="pop")]
    els += [lab(x + 420, 380, "the work of hands", th, GOLD, 34, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 2 · A spiral in granite
def granite_rect(x, y, w, h, at=-1, seed=1, n=None, op=None):
    """A block face of pink Aswan granite: base colour and a scatter of grains (feldspar pink, quartz pale, mica dark)."""
    els = [rect(x, y, w, h, GRAN, "rgba(255,236,206,.3)", 1.5, 2, at)]
    rnd = random.Random(seed)
    for _ in range(n if n is not None else int(w * h / 1400)):
        els.append(circ(x + rnd.uniform(4, w - 4), y + rnd.uniform(4, h - 4), rnd.uniform(1.5, 3.6), rnd.choice(["#e9c7b8", "#f6ece4", "#3a2a28", "#a0645a"]), at=at, op=.85))
    if op is not None:
        for e in els:
            e.update(op=op, keepop=True)
    return els


def s14():
    """Core 7 large in a museum light at the right (11 cm, a tag); at the left, on 'hollow tube', a granite block in cutaway with a copper
    tube sunk in its ring-shaped slot and the core standing inside; on 'pastry cutter', a cutter in dough; on 'Giza', a chip."""
    th, tp, tg = T("s14", "hollow tube"), T("s14", "pastry cutter"), T("s14", "Flinders Petrie")
    cx, cy, w, h = 1300, 700, 180, 420
    els = [gl(cx, 470, 380, -1, .4)]
    els += [grp(core(cx, cy, w, h, n=12), -1, None)]
    els += [{"k": "dim", "x1": cx + 150, "y1": cy, "x2": cx + 150, "y2": cy - h, "t": "11 cm", "lx": 34, "c": GOLD, "in": .5, "fx": "draw", "dur": .8},
            lab(cx, 230, "core 7", .2, GOLD, 34, st="serif")]
    # the block in cutaway: two slots of the ring, the copper tube in them, the core between
    bx, by, bw, bh = 230, 430, 520, 280
    els += granite_rect(bx, by, bw, bh, -1, 4)
    sx0, sx1, depth = 410, 560, 190
    for sx in (sx0, sx1):
        els += [rect(sx, by - 2, 22, depth, "#120d0b", at=th, fx="pop")]
        els += [rect(sx + 5, by - 160, 12, depth + 150, "url(#k-copper)", "rgba(255,226,190,.6)", 1, 2, th + .3, fx="rise")]
    els += [rect(sx0 + 22, by - 2, sx1 - sx0 - 22, depth + 2, GRAN_L, at=th + .2, op=.5),
            lab(sx0 - 20, by - 120, "a hollow copper tube", th + .5, AMBER, 28, "end")]
    # a pastry cutter pressing a disc out of a sheet of dough
    px, py = 700, 290
    els += [poly([(px - 110, py + 30), (px + 110, py + 30), (px + 140, py + 62), (px - 80, py + 62)], "#e6cf9e", "rgba(90,60,30,.5)", 1.2, tp, fx="pop"),
            poly(E(px + 15, py + 46, 46, 11, 24), "#d8bd86", "#b9bec6", 3, tp + .2, fx="pop"),
            poly([(px - 31, py + 44), (px - 31, py - 20), (px + 61, py - 20), (px + 61, py + 44)], "rgba(185,190,198,.25)", "#b9bec6", 3, tp + .2, fx="pop"),
            lab(px + 15, py - 40, "like a pastry cutter", tp + .4, DIM, 26)]
    els += chip(cx, 780 - 40, "Giza, 1881", AMBER, tg, 26)
    return {"base": "dark", "cam": CAM, "els": els}


def s15():
    """Giza at dusk, the pyramids dim behind; in front, a surveyor in a hat at his tripod theodolite, a lamp glowing by a rock-cut doorway;
    label 'Flinders Petrie at Giza, 1880 to 1882'."""
    gy = 640
    els = [{"k": "pyramid", "x": 560, "y": gy - 10, "w": 520, "in": -1, "op": .55},
           {"k": "pyramid", "x": 1150, "y": gy - 30, "w": 430, "in": -1, "op": .45},
           {"k": "pyramid", "x": 1520, "y": gy - 40, "w": 220, "in": -1, "op": .4},
           poly([(-20, gy), (W_ + 20, gy), (W_ + 20, 1020), (-20, 1020)], "#4a3b2c", at=-1),
           ln([(-20, gy), (W_ + 20, gy)], -1, "rgba(255,226,190,.25)", 1.5, draw=False)]
    # a rock-cut doorway with a lamp, left
    els += [poly([(120, gy), (120, 470), (330, 450), (360, gy)], "#6a5641", "rgba(255,236,206,.25)", 1.2, -1),
            rect(190, 520, 70, 120, "#120d0a", at=-1), gl(225, 560, 120, .4, .7, "fire")]
    # the surveyor at his theodolite
    fx_, fy = 900, gy
    els += fig(fx_, fy, 230, .4, "#1a1410", "point", 1)
    els += [grp([poly(E(fx_ + 2, fy - 220, 36, 6, 24), "#1a1410", at=0),                                   # a brimmed hat
                 poly([(fx_ - 17, fy - 221), (fx_ - 15, fy - 240), (fx_ - 6, fy - 245), (fx_ + 10, fy - 245), (fx_ + 19, fy - 240), (fx_ + 21, fy - 221)],
                      "#1a1410", at=0, curve=True)], .4, "rise")]
    tx, ty = fx_ + 120, fy - 150
    els += [ln([(tx, ty), (tx - 40, fy)], .6, "#2a2016", 4, draw=False), ln([(tx, ty), (tx + 36, fy)], .6, "#2a2016", 4, draw=False),
            ln([(tx, ty), (tx + 4, fy)], .6, "#2a2016", 4, draw=False),
            rect(tx - 30, ty - 34, 60, 30, "#8a7a5a", "rgba(255,236,206,.5)", 1.2, 4, .7, fx="pop"),
            ln([(tx + 30, ty - 20), (tx + 70, ty - 26)], .8, "#c9b48a", 4, draw=False),
            ln([(tx + 70, ty - 26), (1500, 420)], 1.2, GOLD, 1.5, "inferred", dur=1.2, op=.6)]
    els += [lab(889, 230, "Flinders Petrie at Giza, 1880 to 1882", .8, GOLD, 32)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1380, 520, 30], "cam": CAM, "els": els}


def helix_front(x, y, w, h, y0, pitch, turns=1.0):
    """The front half of a helical groove on a cylinder (x, foot y, width w): it runs left to right, sinking `pitch` units per turn."""
    pts = []
    n = 24
    for k in range(n + 1):
        a = math.pi * k / n                    # 0..pi: the front half
        xx = x - w / 2 * math.cos(a)
        yy = y0 + pitch * (a / (2 * math.pi)) + w * .12 * math.sin(a)
        pts.append((xx, yy))
    return pts


def s16():
    """The groove: core 7 close up, one groove lit gold winding round it; beside it, the groove unrolled: one turn about 15 cm, a drop of
    0.1 inch (2.5 mm), 1 in 60 (to scale, then magnified); then Petrie's idea, a tube rim with fixed jewel teeth (dotted), pressed by a
    weight of a ton or two."""
    t0, tj, tt = .3, T("s16", "fixed jewel"), T("s16", "a ton or")
    tr, tm_ = T("s16", "sinks a tenth"), T("s16", "two and a half")
    cx, cy, w, h = 330, 720, 220, 500
    els = [gl(cx, 470, 320, -1, .35)] + [grp(core(cx, cy, w, h, n=12), -1, None)]
    for k in range(3):
        y0 = cy - h + 150 + k * 54
        ww = w * (1 - .12 * (1 - (cy - y0) / h))
        els.append(ln(helix_front(cx, cy, ww, h, y0, 54), t0 + .5 * k, GOLD, 4, curve=True, dur=.5))
    # unrolled: 600 units = one turn (about 15 cm, 6 inches); 1 in 60 = a drop of 10 units
    ux0, ux1, uy = 640, 1240, 300
    els += [ln([(ux0, uy), (ux1, uy)], tr, DIM, 2, "inferred", dur=.6),
            ln([(ux0, uy), (ux1, uy + 10)], tr + .2, GOLD, 4, dur=.8),
            lab((ux0 + ux1) / 2, uy - 30, "one turn: about 15 cm", tr + .3, DIM, 26),
            lab(ux1 + 14, uy + 20, "1 in 60", tm_ + 1.2, GOLD, 28, "start")]
    # magnified end of the drop
    mx, my = 1240, 300
    els += [circ(mx, my + 5, 22, "none", BLUE, 2, tm_ - .2, fx="draw"),
            ln([(mx - 16, my + 22), (mx - 120, 420)], tm_ - .1, BLUE, 1.5, dur=.4),
            rect(820, 410, 320, 120, "rgba(18,13,10,.8)", BLUE, 2, 10, tm_, fx="pop"),
            ln([(840, 440), (1120, 440)], tm_ + .1, DIM, 2, "inferred", dur=.4),
            ln([(840, 440), (1120, 500)], tm_ + .2, GOLD, 4, dur=.5),
            lab(980, 560, "a drop of 0.1 inch, 2.5 mm", tm_ + .3, GOLD, 26)]
    # Petrie's idea: a tube rim with fixed jewel teeth, a heavy weight above
    rx, ry = 1460, 650
    els += [poly(E(rx, ry, 110, 30, 40), "none", COP, 10, tj, fx="pop"),
            rect(rx - 110, ry - 140, 220, 140, "rgba(200,116,60,.25)", COP, 2, 0, tj, fx="pop")]
    for k in range(9):
        a = math.pi * k / 8
        px, py = rx - 110 * math.cos(a), ry + 30 * math.sin(a)
        els.append(poly([(px - 7, py), (px + 7, py), (px, py + 16)], "rgba(201,193,238,.6)", LILAC, 1.5, tj + .2 + .05 * k, style="claimed", fx="pop"))
    els += [rect(rx - 90, ry - 290, 180, 110, "rgba(201,193,238,.08)", LILAC, 2.5, 8, tt, style="claimed", fx="rise"),
            lab(rx, ry - 225, "1 to 2 tons", tt + .2, LILAC, 28),
            arr([(rx, ry - 175), (rx, ry - 150)], tt + .3, LILAC, 3, "claimed", dur=.3, curve=False),
            lab(rx, ry + 80, "Petrie: fixed jewel points", tj + .5, LILAC, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s17():
    """Feed per turn, on one scale: at the top right, Petrie's figure (core 7 and its gold groove, 0.1 inch a turn); then a hair-thin bar
    for a modern diamond drill (0.0002 inch) and a long gold bar 500 times longer for Petrie's groove (0.1 inch); a chip 'x 500'; the
    machinist's silhouette dim at the left."""
    tf, tm, tp = T("s17", "Petrie's figure"), T("s17", "A modern diamond"), T("s17", "Petrie's groove:")
    els = fig(230, 720, 300, .2, "#2a2018", "press", 1, op=.75)
    els += [rect(300, 560, 180, 160, "#3a3d44", "rgba(255,236,206,.3)", 1.2, 6, .2, fx="rise", op=.75),
            lab(260, 360, "Christopher Dunn, machinist", .5, DIM, 28)]
    els += [gl(1500, 290, 150, tf, .35), grp(core(1500, 350, 70, 150, gold=True, n=6), tf, "rise"),
            lab(1500, 405, "Petrie, 1883: 0.1 inch a turn", tf + .3, GOLD, 26)]
    x0, k = 560, 1000.0 / .1          # 0.1 inch = 1000 units
    els += [lab(x0, 300, "how deep a drill bites in one turn", .8, AMBER, 28, "start", st="cap")]
    yy = 460
    els += [rect(x0, yy - 10, .0002 * k, 20, BLUE, at=tm, fx="pop"),
            circ(x0 + 1, yy, 26, "none", BLUE, 2.5, tm + .2, fx="draw"),
            lab(x0 + 40, yy + 10, "modern diamond drill: 0.0002 inch", tm + .4, BLUE, 28, "start")]
    yy2 = 590
    els += [ln([(x0, yy2), (x0 + .1 * k, yy2)], tp, GOLD, 26, dur=1.6),
            lab(x0, yy2 + 60, "Petrie's groove: 0.1 inch", tp + .4, GOLD, 30, "start")]
    els += chip(x0 + 1000 - 90, yy2 - 64, "x 500", GOLD, tp + 1.2, 34)
    return {"base": "dark", "cam": CAM, "els": els}


def bow_drill(x, y, h, at, c="#e8d6b8", op=1.0):
    """A hand bow drill, upright, its foot on (x, y), h tall: a shaft, a cap, a bow whose string loops round the shaft."""
    els = [ln([(x, y), (x, y - h)], 0, c, 5, draw=False),
           poly(E(x, y - h - 8, 28, 10, 20), c, at=0),
           ln([(x - 150, y - h * .55), (x - 40, y - h * .66), (x + 70, y - h * .62), (x + 150, y - h * .5)], 0, c, 5, curve=True, draw=False),
           ln([(x - 150, y - h * .55), (x, y - h * .5), (x + 150, y - h * .5)], 0, c, 1.5, draw=False)]
    e = grp(els, at, "pop")
    if op != 1.0:
        gdim(e, op)
    return [e]


def s18():
    """A lilac dotted ultrasonic drill head over a granite block, fine vibration rings at its tip ('Dunn, 1984 (proposed)'); on 'could hand
    tools', a bow drill in warm silhouette beside it, a question mark between them."""
    th = T("s18", "could hand")
    els = granite_rect(250, 520, 560, 220, -1, 5)
    dx = 530
    els += [rect(dx - 60, 200, 120, 150, "rgba(201,193,238,.08)", LILAC, 2.5, 10, .3, style="claimed", fx="pop"),
            rect(dx - 14, 350, 28, 150, "rgba(201,193,238,.12)", LILAC, 2.5, 4, .5, style="claimed", fx="pop")]
    for k in range(4):
        els.append(poly(E(dx, 510, 30 + 22 * k, 8 + 6 * k, 30), "none", LILAC, 2, .8 + .15 * k, style="claimed", fx="pop", op=.9 - .18 * k))
    els += [lab(dx, 160, "an ultrasonic drill? (Dunn, 1984)", .9, LILAC, 28)]
    els += granite_rect(1050, 520, 460, 220, -1, 6, op=.45)
    els += bow_drill(1280, 520, 300, th, "#e8c49a")
    els += [lab(1280, 170, "or hand tools?", th + .3, "#e8c49a", 30)]
    els += qmark(905, 470, th + .5, 110)
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · Copper, sand and patience
def s19():
    """A workbench in lamplight: an experimenter turning a bow drill on a block of pink granite, a heap of sand and copper tubes beside
    him; label 'Denys Stocks, experimental archaeologist'; on 'hardness', a label."""
    th = T("s19", "The secret")
    els = [gl(800, 470, 520, -1, .35), rect(330, 600, 900, 26, "#5a4634", "rgba(255,236,206,.3)", 1.2, 4, -1),
           ln([(380, 626), (380, 790)], -1, "#3a2c20", 14, draw=False), ln([(1180, 626), (1180, 790)], -1, "#3a2c20", 14, draw=False)]
    els += granite_rect(560, 470, 300, 130, -1, 7)
    els += fig(470, 780, 330, -1, "#2a2018", "pull", 1, fx=None)
    els += [ln([(730, 470), (730, 300)], -1, "#c9b48a", 6, draw=False), poly(E(730, 296, 26, 9, 20), "#8a7a5a", at=-1),
            ln([(560, 400), (700, 390), (860, 400)], -1, "#c9b48a", 5, curve=True, draw=False),
            ln([(560, 400), (730, 405), (860, 400)], -1, "#e9dcc4", 1.5, draw=False)]
    rnd = random.Random(3)
    els += [poly([(930, 600), (980, 548), (1040, 540), (1100, 600)], "#d8c08e", "rgba(90,60,30,.4)", 1, -1, curve=True)]
    els += [circ(rnd.uniform(950, 1080), rnd.uniform(560, 595), 2, "#f2e2b8", at=-1) for _ in range(30)]
    for k in range(3):
        els.append(rect(1110 + k * 26, 520 - k * 6, 18, 80, "url(#k-copper)", "rgba(255,226,190,.5)", 1, 3, -1))
    els += [lab(800, 220, "Denys Stocks, experimental archaeologist", .3, GOLD, 30),
            lab(1030, 500, "sand", .6, DIM, 24), lab(1150, 410, "copper tubes", .7, AMBER, 24)]
    els += chip(800, 290, "the secret: hardness", BLUE, th, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def s20():
    """A hardness scale from 1 to 10 ('what scratches what'): bars rise as named, copper 3, feldspar 6 (a granite chip), quartz 7 (a heap of
    sand); a dashed line at 6, 'granite's minerals'."""
    tc, tf, tq = T("s20", "copper at"), T("s20", "the feldspar"), T("s20", "and quartz")
    x0, k, base = 330, 120, 700
    ticks = [[x0 + (i - 1) * k, str(i)] for i in range(1, 11)]
    els = [axis(x0, x0 + 9 * k, base, ticks, .2, "hardness: what scratches what")]
    bars = [(3, COP, "copper", tc), (6, "#d9a090", "feldspar in granite", tf), (7, "#eef0f2", "quartz: sand", tq)]
    for v, c, name, t in bars:
        xx = x0 + (v - 1) * k
        anc, dx = {3: ("middle", 0), 6: ("end", 30), 7: ("start", -30)}[v]
        els += [rect(xx - 36, base - v * 62, 72, v * 62, c, "rgba(0,0,0,.3)", 1, 4, t, fx="fill"),
                lab(xx + dx, base - v * 62 - 22, name, t + .4, c if c != "#eef0f2" else BONE, 28, anc)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s21():
    """A magnified cutaway of a tube's rim in its slot: the copper wall turning, sand grains rolling and grinding under it, chips of granite
    flying off the floor of the slot; 'copper carries', 'sand cuts'."""
    tc, ts = T("s21", "So the copper"), T("s21", "The sand")
    els = granite_rect(180, 470, 1420, 300, -1, 8, n=520)
    els += [rect(700, 360, 400, 260, "#100c0a", at=-1)]
    els += [rect(780, 120, 240, 440, "url(#k-copper)", "rgba(255,226,190,.6)", 1.5, 4, .3, fx="rise")]
    rnd = random.Random(21)
    for k in range(26):
        x = 700 + 10 + (k % 13) * 30 + rnd.uniform(-4, 4)
        y = 585 + (k // 13) * 22 + rnd.uniform(-3, 3)
        els.append(poly(blob(x, y, 11, 9, 7, .3, k), "#f2e6c8", "rgba(80,60,30,.6)", 1, ts + .03 * k, fx="pop"))
    for k in range(10):
        x = 720 + k * 36
        els.append(ln([(x, 625), (x - 14 + 6 * (k % 3), 655)], ts + .8 + .05 * k, "#e9c7b8", 3, dur=.3))
    els += [arr([(1060, 200), (1110, 240), (1060, 280)], tc, AMBER, 3, dur=.5),
            lab(1130, 230, "copper carries", tc + .2, AMBER, 30, "start"),
            lab(1130, 640, "sand cuts", ts + .3, "#f2e6c8", 32, "start"),
            arr([(1120, 625), (1050, 610)], ts + .4, "#f2e6c8", 2.5, dur=.4)]
    return {"base": "dark", "cam": CAM, "els": els}


def s22():
    """Aswan granite at dawn: three men at a block, one pushing a long bow, one pressing on the drill's cap, one pouring sand (the copper tube
    is 8 cm across, to scale with them); magnified at the right, the hole fills to 6 cm as a clock counts 20 hours; then the core, ringed
    with grooves."""
    tr, tc = T("s22", "After twenty"), T("s22", "and left a")
    gy = 700
    els = granite_rect(250, 560, 520, 140, -1, 9)
    # people at the scale of the block (1 m = 140 units): the tube is 8 cm = 11 units across
    sc = 140.0
    tx = 510
    els += [rect(tx - 6, 520, 12, 40, "url(#k-copper)", at=-1), ln([(tx, 520), (tx, 470)], -1, "#c9b48a", 5, draw=False),
            poly(E(tx, 468, 14, 6, 16), "#8a7a5a", at=-1)]
    els += fig(410, gy, 1.7 * sc, -1, "#2a1d14", "pull", 1, fx=None)
    els += fig(600, gy, 1.65 * sc, -1, "#2a1d14", "press", -1, fx=None)
    els += [ln([(380, 505), (450, 500), (560, 506), (640, 516)], -1, "#c9b48a", 5, curve=True, draw=False),
            ln([(380, 505), (tx, 496), (640, 516)], -1, "#e9dcc4", 1.5, draw=False)]
    els += fig(820, gy, 1.7 * sc, -1, "#2a1d14", "point", -1, fx=None)
    els += [ln([(760, 520), (560, 556)], .4, "#f2e2b8", 2, "inferred", dur=.5)]
    els += [lab(510, 250, "Aswan: a bow, a copper tube, dry sand", .3, GOLD, 28),
            lab(510, 330, "the tube: 8 cm across", .8, AMBER, 26), ln([(510, 345), (510, 460)], .9, AMBER, 1.5, "inferred", dur=.4)]
    # magnified: 7 units per mm... the tube 8 cm = 240 units wide, the hole 6 cm = 180 deep
    mx, my, s7 = 1200, 360, 3.0
    els += [circ(mx - 300, 400, 34, "none", BLUE, 2, .6, fx="draw"), ln([(mx - 266, 400), (mx - 80, 400)], .7, BLUE, 1.5, dur=.4)]
    els += granite_rect(mx - 70, my, 380, 300, -1, 10, n=60)
    for sx in (mx, mx + 240 - 12):
        els.append(rect(sx, my, 12, 60 * s7, "#120d0b", at=.9, fx="fill", dur=6.0))
    els += [{"k": "dim", "x1": mx + 290, "y1": my, "x2": mx + 290, "y2": my + 60 * s7, "t": "6 cm", "lx": 30, "c": GOLD, "in": round(tr, 2), "fx": "fade", "dur": .6},
            lab(mx + 120, my - 30, "magnified", .8, BLUE, 24)]
    # the clock
    cx_, cy_ = 1640, 240
    els += [circ(cx_, cy_, 44, "rgba(18,13,10,.8)", BONE, 2.5, .8, fx="pop"),
            ln([(cx_, cy_), (cx_, cy_ - 32)], .9, BONE, 3, draw=False), ln([(cx_, cy_), (cx_ + 22, cy_ + 10)], .9, BONE, 3, draw=False),
            lab(cx_, cy_ + 84, "20 hours", tr, GOLD, 28)]
    # the core, lifted out
    els += [gl(1625, 640, 120, tc, .4), grp(core(1625, 700, 90, 140, n=7), tc, "rise")]
    els += [lab(1690, 748, "a core, with grooves", tc + .4, BONE, 26, "end")]
    return {"base": "sky", "tod": "dawn", "ground": gy, "sun": [1500, 640, 30], "cam": CAM, "els": els}


def s23():
    """Slow: a chip '3 mm an hour'. Magnified: a single hard grain caught between the copper and the core scratches a groove that jumps from
    one ring to the next and, seen from the side, reads as a slanting spiral."""
    tg, tj = T("s23", "And the grooves"), T("s23", "which experimenters")
    els = chip(330, 230, "about 3 mm an hour", GOLD, .3, 32)
    els += [lab(330, 300, "copper and sand at Aswan", .5, DIM, 24)]
    # magnified slot: copper wall at the right, core at the left
    cx0 = 760
    els += granite_rect(cx0 - 330, 300, 330, 420, -1, 12, n=110)
    els += [rect(cx0, 300, 70, 420, "#120d0b", at=-1), rect(cx0 + 70, 240, 60, 480, "url(#k-copper)", "rgba(255,226,190,.5)", 1.2, 3, -1)]
    els += [lab(cx0 - 165, 270, "the core", .4, "#e3b9ab", 26), lab(cx0 + 100, 220, "copper", .4, AMBER, 26)]
    rows = [380, 430, 480, 530, 580, 630]
    for k, yy in enumerate(rows):
        els.append(ln([(cx0 - 330, yy), (cx0, yy)], tg + .3 * k, "rgba(40,20,20,.7)", 2.5, dur=.3))
    # the grain jumping from line to line
    path = [(cx0 + 4, 380), (cx0 - 120, 382), (cx0 - 200, 404), (cx0 - 330, 430)]
    els += [poly(blob(cx0 + 18, 380, 16, 12, 8, .3, 3), "#f2e6c8", "rgba(80,60,30,.6)", 1.2, tg, fx="pop"),
            ln(path, tj, GOLD, 4, dur=1.2),
            ln([(cx0 - 330, 430), (cx0 - 400, 452)], tj + 1.0, GOLD, 4, "inferred", dur=.4),
            lab(cx0 - 170, 790 - 40, "a scratch can jump a line", tj + .6, GOLD, 28)]
    # an experimental core seen from the side: grooves that look like a spiral
    els += [grp(core(1350, 700, 150, 380, gold=False, n=9), tg + .5, "rise")]
    for k in range(3):
        y0 = 700 - 380 + 110 + k * 70
        els.append(ln(helix_front(1350, 700, 150 * .94, 380, y0, 40), tj + .6 + .3 * k, GOLD, 3, curve=True, dur=.5))
    els += [lab(1350, 270, "an experimental core", tg + .7, DIM, 26), lab(1350, 760, "looks like a spiral", tj + 1.4, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def relief_driller(x, y, s, at, c="#9a4a2a", line="#3a2014", fx="pop", op=None, jar=True, sil=False):
    """An Egyptian relief figure, in profile facing right, seated on a low block and turning a weighted drill in a stone jar: x, y = the
    foot of his block; s = scale (1 = a seated figure about 300 units tall). Flat colour with a dark outline, as on a tomb wall; sil=True
    draws him all in colour c (a silhouette with a lit rim of colour `line`)."""
    P = lambda pts: [(x + a * s, y - b * s) for a, b in pts]
    els = [poly(P([(-80, 0), (20, 0), (20, 70), (-80, 70)]), c if sil else "#cdb48e", line, 2, 0),            # the block he sits on
           poly(P([(-60, 70), (30, 70), (40, 110), (-40, 120)]), c if sil else "#efe6d2", line, 2, 0),        # kilt
           poly(P([(20, 82), (110, 76), (118, 70), (112, 4), (96, 0), (98, 70), (30, 70)]), c, line, 2, 0),    # thigh and shin
           poly(P([(94, 0), (128, 0), (126, 10), (96, 10)]), c, line, 2, 0),                                  # foot
           poly(P([(-40, 118), (40, 112), (60, 200), (-36, 206)]), c, line, 2, 0),                            # torso
           poly(P([(-30, 206), (56, 200), (70, 222), (-44, 230)]), c, line, 2, 0),                            # shoulders
           poly(E(x + 18 * s, y - 252 * s, 34 * s, 36 * s, 24), c, line, 2, 0),                               # head
           poly(P([(-12, 280), (48, 282), (50, 236), (30, 218), (-14, 222), (-22, 250)]), mix(c, "#000000", .3) if sil else "#1a1410", line, 2, 0),  # wig
           circ(x + 40 * s, y - 252 * s, 4 * s, c if sil else "#1a1410", at=0),                               # eye
           ln(P([(50, 206), (120, 176), (178, 214)]), 0, c, 11 * s, draw=False),                               # arm to the crank
           ln(P([(40, 196), (112, 150), (170, 150)]), 0, c, 11 * s, draw=False)]                               # arm to the shaft
    if jar:
        jx, jy = x + 205 * s, y
        els += [poly(P([(170, 0), (240, 0), (262, 40), (252, 92), (226, 112), (184, 112), (158, 92), (148, 40)]), "#7d7a80", line, 2, 0, curve=True),
                poly(E(jx, y - 112 * s, 24 * s, 6 * s, 16), "#2a2628", line, 1.5, 0),
                ln(P([(205, 108), (205, 250)]), 0, "#6a4a2a", 7 * s, draw=False),                               # the shaft
                ln(P([(205, 250), (182, 262), (170, 232), (178, 214)]), 0, "#6a4a2a", 6 * s, curve=True, draw=False),   # the crank
                ln(P([(205, 236), (186, 218)]), 0, "#3a2a1a", 2, draw=False), ln(P([(205, 236), (226, 218)]), 0, "#3a2a1a", 2, draw=False),
                poly(E(x + 184 * s, y - 210 * s, 13 * s, 16 * s, 16), "#8a7d70", line, 1.5, 0),                 # weights
                poly(E(x + 228 * s, y - 210 * s, 13 * s, 16 * s, 16), "#8a7d70", line, 1.5, 0)]
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return [e]


def u24(x, y, h, at, c="#1a1410", w=5):
    """The hieroglyph U24 (a stoneworker's drill weighted with stones): a shaft, a cranked top, two stone weights, a borer below."""
    s = h / 300.0
    P = lambda pts: [(x + a * s, y - b * s) for a, b in pts]
    els = [ln(P([(0, 0), (0, 260)]), 0, c, w * 1.6, draw=False),
           ln(P([(0, 260), (-34, 280), (-52, 250), (-40, 226)]), 0, c, w * 1.3, curve=True, draw=False),
           ln(P([(0, 236), (-30, 206)]), 0, c, w * .6, draw=False), ln(P([(0, 236), (30, 206)]), 0, c, w * .6, draw=False),
           poly(E(x - 34 * s, y - 186 * s, 18 * s, 24 * s, 16), c, at=0), poly(E(x + 34 * s, y - 186 * s, 18 * s, 24 * s, 16), c, at=0),
           poly(P([(-26, 0), (26, 0), (16, -22), (-16, -22)]), c, at=0)]
    return [grp(els, at, "pop")]


def s24():
    """A tomb-relief scene on a limestone wall (register lines): a craftsman seated by a stone jar, turning a drill whose cranked top carries
    two stone weights; beside him, as on such walls, a column of caption hieroglyphs (faint); on 'hieroglyph', the drill sign U24 lights up
    large in that column, 'craft'. Label 'tomb reliefs, Old Kingdom'."""
    tw, th = T("s24", "a drill with"), T("s24", "hieroglyph")
    els = [rect(120, 180, 1500, 560, "#d9c39a", "rgba(90,60,30,.6)", 2, 6, -1),
           rect(120, 180, 1500, 560, "url(#k-speck)", at=-1),
           ln([(120, 230), (1620, 230)], -1, "#8a5a32", 4, draw=False), ln([(120, 690), (1620, 690)], -1, "#8a5a32", 4, draw=False),
           ln([(1290, 230), (1290, 690)], -1, "#8a5a32", 3, draw=False), ln([(1530, 230), (1530, 690)], -1, "#8a5a32", 3, draw=False)]
    els += [{"k": "glyphs", "x": 1310, "y": 248, "w": 200, "h": 96, "rows": 2, "cols": 3, "kind": "hieroglyph", "c": "#6a4a2a", "seed": 5, "sw": 4, "op": .5, "in": -1},
            {"k": "glyphs", "x": 1310, "y": 600, "w": 200, "h": 80, "rows": 2, "cols": 3, "kind": "hieroglyph", "c": "#6a4a2a", "seed": 9, "sw": 4, "op": .5, "in": -1}]
    els += relief_driller(420, 690, 1.45, .2)
    els += [lab(870, 160, "tomb reliefs, Old Kingdom", .3, GOLD, 28)]
    # the borer inside the jar (cutaway), on 'a drill with'
    jx, jy = 420 + 205 * 1.45, 690
    els += [poly([(jx - 30, jy - 40), (jx + 30, jy - 40), (jx + 20, jy - 28), (jx - 20, jy - 28)], "#3a3436", "#f2e6c8", 1.5, tw + .4, fx="pop"),
            lab(jx + 150, jy - 60, "a stone borer inside", tw + .8, "#3a2014", 24, "start", halo=False)]
    # the sign, in the caption column
    els += [rect(1300, 356, 220, 236, "rgba(255,240,200,.55)", "#b07a3a", 2.5, 8, th - .2, fx="pop"), gl(1410, 470, 160, th - .2, .45)]
    els += u24(1410, 538, 160, th)
    els += [lab(1410, 586, "craft", th + .5, "#3a2014", 30, st="serif", halo=False), lab(1410, 160, "the hieroglyph", th + .3, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s25():
    """A museum spotlight on a slim copper-green drill bit, 63 mm long, with six coils of dark leather thong round its shank; label 'Badari,
    grave 3932', chip 'c. 3300 BCE'; a faint bow behind shows how the string spun it."""
    els = [gl(889, 470, 460, -1, .45)]
    x0, x1, y = 470, 1310, 470             # 63 mm drawn 840 units long (magnified)
    els += [poly([(x0, y - 16), (x1 - 60, y - 14), (x1, y), (x1 - 60, y + 14), (x0, y + 16)], "#5f7a62", "rgba(220,240,220,.5)", 1.5, .2, fx="pop"),
            poly([(x0, y - 16), (x1 - 60, y - 14), (x1 - 60, y - 4), (x0, y - 4)], "#8fae8e", at=.2, op=.5)]
    for k in range(6):
        xx = 640 + k * 34
        els.append(poly([(xx, y - 26), (xx + 22, y - 24), (xx + 26, y + 24), (xx + 4, y + 26)], "#4a3020", "#2a1a10", 1.5, .6 + .12 * k, fx="pop"))
    els += [{"k": "dim", "x1": x0, "y1": y + 70, "x2": x1, "y2": y + 70, "t": "63 mm", "ly": 40, "c": GOLD, "in": 1.0, "fx": "draw", "dur": .8},
            lab(889, 300, "Badari, grave 3932", .5, GOLD, 32),
            lab(745, 380, "six coils of leather thong", 1.6, "#d9b48a", 24)]
    els += chip(889, 650, "c. 3300 BCE", AMBER, 1.2, 28)
    els += [ln([(380, 600), (520, 560), (900, 540), (1300, 560), (1420, 600)], 1.8, "#c9b48a", 4, curve=True, dur=1.0, op=.35),
            ln([(380, 600), (720, 490), (1420, 600)], 2.2, "#e9dcc4", 1.5, "inferred", dur=1.0, op=.35)]
    return {"base": "dark", "cam": CAM, "els": els}


def s26():
    """Core 7 (gold groove) and an experimental core side by side, a ruler between them; a tick by 'copper and sand: it works' and a small
    lilac question mark between the two grooves, 'exact groove: not yet matched'."""
    tw, to = T("s26", "Copper, sand"), T("s26", "Only core")
    els = [gl(889, 470, 520, -1, .3)]
    els += [grp(core(640, 700, 170, 400, gold=True, n=12), -1, None), grp(core(1140, 700, 150, 300, n=9), -1, None)]
    els += [lab(640, 250, "core 7, Giza", .3, GOLD, 28), lab(1140, 350, "copper and sand", .3, BONE, 28)]
    els += [rect(860, 300, 26, 400, "#d9c39a", "rgba(0,0,0,.4)", 1, 2, .4, fx="rise")]
    for k in range(9):
        els.append(ln([(860, 320 + k * 45), (874 if k % 2 else 880, 320 + k * 45)], .5, "#3a2a1a", 2, draw=False))
    els += [tick(1310, 480, tw, GREEN, 1.3), lab(1350, 492, "it works", tw + .2, GREEN, 30, "start")]
    els += qmark(889, 250, to, 90) + [lab(889, 770 - 10, "exact groove: not yet matched", to + .3, LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 4 · Boxes in the dark
BOXC, BOXT, BOXS = "#3a3634", "#5a544e", "#25211f"          # dark granite: front, top, side


def stone_box(x, y, L, H, D, at=-1, tone=BOXC, top=BOXT, side=BOXS, lid=0.0, lid_dx=0.0, grains=70, seed=1, fx=None, op=None,
              hollow=False, edge="rgba(255,236,206,.35)"):
    """A granite box in three-quarter view: front face x..x+L, y-H..y; its far side runs back up and to the right (D deep, drawn at
    .55 D across and .33 D up); an optional lid (lid = its height) on top, slid lid_dx units along the box; grains on the front face."""
    ox, oy = D * .55, -D * .33

    def blk(x0, y0, h, cf, ct, cs):
        return [poly([(x0, y0), (x0 + L, y0), (x0 + L, y0 - h), (x0, y0 - h)], cf, edge, 1.2, 0),
                poly([(x0 + L, y0), (x0 + L + ox, y0 + oy), (x0 + L + ox, y0 - h + oy), (x0 + L, y0 - h)], cs, edge, 1, 0),
                poly([(x0, y0 - h), (x0 + L, y0 - h), (x0 + L + ox, y0 - h + oy), (x0 + ox, y0 - h + oy)], ct, edge, 1, 0)]
    els = blk(x, y, H, tone, top, side)
    if hollow:
        t = min(L, D) * .08
        els.append(poly([(x + t * 1.6, y - H - t * .25), (x + L - t * .8, y - H - t * .25), (x + L + ox - t * 1.6, y - H + oy + t * .25),
                         (x + ox + t * .8, y - H + oy + t * .25)], "#0c0a09", at=0))
    rnd = random.Random(seed)
    for _ in range(grains):
        els.append(circ(x + rnd.uniform(6, L - 6), y - rnd.uniform(6, H - 6), rnd.uniform(1, 2.3), rnd.choice(["#cfc8be", "#141110", "#8a8078"]), at=0, op=.6))
    els.append(poly([(x, y), (x + L * .5, y), (x + L * .5, y - H), (x, y - H)], "#ffe9c8", at=0, op=.05))          # lamplight from the left
    if lid:
        els += blk(x + lid_dx, y - H, lid, mix(tone, "#ffffff", .07), mix(top, "#ffffff", .1), side)
        els += [ln([(x + lid_dx, y - H), (x + lid_dx + L, y - H), (x + lid_dx + L + ox, y - H + oy)], 0, "rgba(255,236,206,.55)", 1.6, draw=False),
                ln([(x, y - H + 3), (x + L, y - H + 3)], 0, "rgba(0,0,0,.45)", 3, draw=False)]           # the joint: a lit edge, a shadow under it
        for _ in range(int(grains * lid / max(H, 1))):
            els.append(circ(x + lid_dx + rnd.uniform(6, L - 6), y - H - rnd.uniform(4, lid - 4), rnd.uniform(1, 2.2), rnd.choice(["#cfc8be", "#141110"]), at=0, op=.6))
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return [e]


def iso_el(items, x, y, s, az, el=.42, spin=0.0, at=-1, **kw):
    e = {"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": items, "in": round(at, 2)}
    e.update(kw)
    return e


def P3(e, p):
    """Where a world point (x, y, z) of a still iso element lands on the panel."""
    az = math.radians(e.get("az", 35))
    ca, sa = math.cos(az), math.sin(az)
    x, y, z = p
    rx, rz = x * ca - z * sa, x * sa + z * ca
    S, el_ = e["s"], e.get("el", .32)
    return (round(e["x"] + (rx - rz) * C30 * S, 1), round(e["y"] - y * S + (rx + rz) * el_ * S, 1))


# the Greater Vaults, a stretch of them, roof cut away (after iso3d.serapeum_vaults): metres, the corridor along z
V_N, V_NICHE, V_WALL, V_DEPTH, V_CORR, V_H = 5, 6.8, .9, 7.5, 3.2, 3.4
V_ROCK = "#7d6851"


def vault_boxes():
    """(x, z, side, lid shift) of each box in the stretch: one per side room, a few rooms empty, most lids pushed aside."""
    L = V_N * V_NICHE
    z0 = -L / 2
    out = []
    for side in (-1, 1):
        for i in range(V_N):
            if (side, i) in ((-1, 3), (1, 1)):
                continue
            zc = z0 + i * V_NICHE + V_NICHE / 2
            xc = side * (V_CORR / 2 + V_DEPTH / 2 + .2)
            shift = [(-side * 1.0, 0), (0, .9), (-side * .7, -.5), (0, 0), (-side * 1.2, .3)][(i + (side > 0) * 2) % 5]
            out.append((xc, zc, side, shift))
    return out


def vault_items():
    L = V_N * V_NICHE
    z0 = -L / 2
    xw = V_CORR / 2 + V_DEPTH + .9
    out = [{"t": "flat", "pts": [[-xw, z0 - 1], [xw, z0 - 1], [xw, z0 + L + 1], [-xw, z0 + L + 1]], "y": .02, "c": "#221b15"}]
    for side in (-1, 1):
        out.append({"t": "box", "x": side * (V_CORR / 2 + V_DEPTH + .6), "z": 0, "y": 0, "w": 1.8, "d": L + 1.8, "h": V_H, "c": V_ROCK, "edge": "rgba(0,0,0,.35)"})
        for i in range(V_N + 1):
            out.append({"t": "box", "x": side * (V_CORR / 2 + V_DEPTH / 2), "z": z0 + i * V_NICHE, "y": 0, "w": V_DEPTH, "d": V_WALL, "h": V_H, "c": V_ROCK,
                        "edge": "rgba(0,0,0,.35)"})
    for side in (-1, 1):                                                   # the far end walls, low
        pass
    out.append({"t": "box", "x": 0, "z": z0 - .6, "y": 0, "w": 2 * xw, "d": 1.2, "h": V_H, "c": V_ROCK, "edge": "rgba(0,0,0,.35)"})
    for xc, zc, side, (dx, dz) in vault_boxes():
        out.append({"t": "box", "x": xc, "z": zc, "y": 0, "w": 3.85, "d": 2.32, "h": 2.32, "c": "#3c393e", "edge": "rgba(255,236,206,.4)"})
        out.append({"t": "box", "x": xc + dx, "z": zc + dz, "y": 2.32, "w": 3.85, "d": 2.32, "h": .98, "c": "#57535b", "edge": "rgba(255,236,206,.4)"})
    return out


VAULT = dict(x=990, y=470, s=19.5, az=-36, el=.44)


def vault_el(at=-1):
    return iso_el(vault_items() + [{"t": "person", "x": .2, "y": 0, "z": 6.0, "h": 1.7, "color": "#e8d6b8"}], VAULT["x"], VAULT["y"], VAULT["s"],
                  VAULT["az"], VAULT["el"], 0.0, at)


def s27():
    """The Greater Vaults, a stretch of them with the roof cut away: a corridor in the rock, side rooms on both sides, a dark granite box
    in most of them, lids pushed aside; lamps glow along the corridor; a person for scale. On 'its own side room', one room lights."""
    ts, tl = T("s27", "its own side"), T("s27", "pushed aside")
    e = vault_el(-1)
    els = [gl(990, 500, 760, -1, .16), e]
    L = V_N * V_NICHE
    z0 = -L / 2
    for k in range(V_N + 1):
        x, y = P3(e, (0, 2.6, z0 + k * V_NICHE))
        els.append(gl(x, y, 120, -1, .35))
    bx = vault_boxes()
    xc, zc, side, _ = bx[1]
    x, y = P3(e, (xc, 1.6, zc))
    els += [gl(x, y, 200, ts, .8), ln([(x - 40, y + 6), (x - 150, y + 60), (560, y + 60)], ts + .1, GOLD, 1.5, dur=.4, op=.8),
            lab(548, y + 70, "one box, one room", ts + .2, GOLD, 28, "end")]
    x2, y2 = P3(e, (bx[6][0] + bx[6][3][0], 3.3, bx[6][1] + bx[6][3][1]))
    els += [ln([(x2, y2 - 10), (x2 + 70, y2 - 90)], tl, DIM, 2, dur=.4), lab(x2 + 80, y2 - 100, "lid pushed aside", tl + .2, DIM, 26, "start")]
    els += [lab(250, 190, "the Serapeum, Saqqara", .4, GOLD, 34, "start", st="serif"),
            lab(250, 236, "a stretch of the Greater Vaults, roof cut away", .7, DIM, 24, "start")]
    return {"base": "dark", "stars": 18, "cam": CAM, "els": els}


def s38_add():
    """Scan: pale-blue outlines trace every box of the stretch, one after another; a chip, all 24."""
    e = vault_el(-1)
    out = []
    for k, (xc, zc, side, (dx, dz)) in enumerate(vault_boxes()):
        x0, x1, z0_, z1 = xc - 1.95, xc + 1.95, zc - 1.2, zc + 1.2
        top = 3.35
        items = [{"t": "line", "p": [[x0, top, z0_], [x1, top, z0_], [x1, top, z1], [x0, top, z1], [x0, top, z0_]], "c": BLUE, "w": 2.2},
                 {"t": "line", "p": [[x0, 0, z1], [x0, top, z1]], "c": BLUE, "w": 1.6}, {"t": "line", "p": [[x1, 0, z1], [x1, top, z1]], "c": BLUE, "w": 1.6},
                 {"t": "line", "p": [[x1, 0, z0_], [x1, top, z0_]], "c": BLUE, "w": 1.6}]
        o = {kk: e[kk] for kk in ("x", "y", "s", "az", "spin", "el")}
        o.update(k="iso", items=items, **{"in": round(.4 + .22 * k, 2), "fx": "fade"})
        out.append(o)
    out += chip(400, 700, "scan all 24, inside and out", BLUE, 1.0, 28)
    return out


def sphinx_head(x, y, s, at, fx="rise", op=None):
    """A sphinx's head in the nemes headdress, in profile facing right, rising out of the sand at (x, y); s = its height."""
    k = s / 100.0
    P = lambda pts: [(x + a * k, y - b * k) for a, b in pts]
    els = [poly(P([(-38, 0), (-40, 40), (-30, 70), (-8, 92), (14, 98), (30, 90), (36, 70), (34, 46), (40, 30), (34, 22), (36, 12), (30, 0)]),
                "#cdb085", "rgba(255,236,206,.5)", 1.2, 0),                                                   # head and nemes
           poly(P([(-38, 0), (-40, 40), (-30, 70), (-8, 92), (-6, 60), (-14, 30), (-12, 0)]), "#b8996c", at=0, op=.9),   # lappet in shade
           poly(P([(6, 66), (30, 64), (32, 52), (24, 46), (8, 50)]), "#e2c79c", at=0, op=.8),                # face light
           circ(x + 24 * k, y - 58 * k, 2.4 * k, "#3a2a1a", at=0)]
    for j in range(5):                                                                                       # nemes stripes
        els.append(ln(P([(-34 + j * 6, 8 + j * 4), (-26 + j * 7, 84 - j * 3)]), 0, "#8f7456", 2, draw=False, op=.5))
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return [e]


def s28():
    """Saqqara's dunes at dusk: a sphinx's head in the sand ('1850'); the buried avenue of sphinxes, only their backs showing, leads
    along a dotted line to a dark doorway in the rock ('1851'); a small figure with a lamp, 'Auguste Mariette'."""
    t50, tm, tav, t51 = T("s28", "eighteen fifty"), T("s28", "Auguste Mariette"), T("s28", "followed a buried"), T("s28", "eighteen fifty-one")
    gy = 640
    els = [poly([(80, gy - 20), (420, gy - 60), (760, gy - 30), (1100, gy - 70), (1500, gy - 40), (1700, gy - 60), (1700, 830), (80, 830)], "#a07c52", at=-1, curve=True, op=.55),
           poly([(80, gy + 10), (500, gy - 10), (900, gy + 6), (1300, gy - 12), (1700, gy + 4), (1700, 830), (80, 830)], "#c69d68", "rgba(255,236,206,.25)", 1.2, -1, curve=True)]
    # the rock face and its doorway, right
    els += [poly([(1330, gy + 2), (1350, 420), (1450, 380), (1610, 400), (1660, gy + 2)], "#7a6046", "rgba(255,236,206,.3)", 1.2, -1),
            rect(1470, 500, 72, gy - 498, "#0c0907", "rgba(255,236,206,.2)", 1, 2, -1)]
    # the head, first
    hx, hy = 330, gy + 4
    els += [gl(hx, hy - 60, 160, t50, .5)] + sphinx_head(hx, hy, 110, -1)
    els += chip(hx, 440, "1850", GOLD, t50, 28)
    # the avenue: sphinx backs, buried, along a dotted line to the doorway
    pts = []
    for k in range(9):
        u = (k + 1) / 10.0
        px, py = hx + 60 + u * (1450 - hx - 60), gy + 2 - 4 * math.sin(u * 3)
        pts.append((px, py))
        w = 70 - 30 * u
        els.append(poly([(px - w / 2, py + 2), (px - w * .3, py - w * .22), (px + w * .2, py - w * .26), (px + w * .32, py - w * .5),
                         (px + w * .45, py - w * .42), (px + w / 2, py + 2)], "#d8b884", "rgba(90,60,30,.5)", 1, tav + .25 * k, fx="rise"))
    els += [ln([(hx + 40, gy - 30)] + [(px, py - 34) for px, py in pts] + [(1490, 560)], tav, GOLD, 2.5, "inferred", dur=2.2, op=.8)]
    els += [lab(900, 760, "a buried avenue of sphinxes", tav + .8, DIM, 26)]
    # Mariette with his lamp, at the doorway
    els += fig(1410, gy + 2, 150, tm, "#1a1410", "point", 1)
    els += [gl(1468, gy - 86, 70, tm + .2, .9, "fire"), lab(1410, gy + 52, "Auguste Mariette", tm + .3, BONE, 28)]
    els += [gl(1506, 560, 120, t51, .9)] + chip(1506, 340, "1851: the vaults", GOLD, t51 + .1, 28)
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [980, 560, 26], "cam": CAM, "els": els}


def car(x, y, at, c="#cbbca8"):
    """A small car in profile, wheels on y (about 64 units long)."""
    return grp([poly([(x - 32, y - 6), (x - 30, y - 16), (x - 14, y - 18), (x - 6, y - 28), (x + 14, y - 28), (x + 22, y - 18), (x + 32, y - 15), (x + 32, y - 6)],
                     c, "rgba(0,0,0,.3)", 1, 0, curve=False),
                circ(x - 18, y - 5, 6, "#1a1511", c, 2, 0), circ(x + 18, y - 5, 6, "#1a1511", c, 2, 0)], at, "pop")


def s29():
    """One box with its lid on, in three-quarter view, a person of 1.7 m beside it (to scale: 3.85 m long, 2.32 m high, the lid 0.98 m);
    '3.85 m'; a chip 'box and lid: up to 62 tonnes'; then forty small cars fill a grid, '= about 40 cars'."""
    tl, tw, tc = T("s29", "nearly four"), T("s29", "sixty-two"), T("s29", "about the weight")
    m = 100.0                                    # 100 units a metre
    x0, y0 = 210, 700
    L, H, D, lid = 3.85 * m, 2.32 * m, 2.32 * m, .98 * m
    els = [gl(450, 520, 520, -1, .3)] + stone_box(x0, y0, L, H, D, -1, lid=lid, seed=4, grains=90)
    els += [{"k": "person", "x": x0 + L + D * .55 + 110, "y": y0, "h": 1.7 * m, "t": "1.7 m", "color": "#e8d6b8", "in": .4, "fx": "rise"},
            {"k": "dim", "x1": x0, "y1": y0 + 40, "x2": x0 + L, "y2": y0 + 40, "t": "3.85 m", "ly": 44, "c": GOLD, "in": round(tl, 2), "fx": "fade", "dur": .6}]
    els += chip(x0 + L / 2 + 40, 225, "box and lid: up to 62 tonnes", GOLD, tw, 30)
    cx0, cy0 = 1030, 300
    for k in range(40):
        c_, r_ = k % 8, k // 8
        els.append(car(cx0 + c_ * 76, cy0 + r_ * 62, tc + .04 * k))
    els += [lab(cx0 + 3.5 * 76, cy0 + 5 * 62 + 30, "= about 40 cars", tc + 1.8, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def apis(x, y, s, at, c=GOLD, fill="rgba(242,201,142,.10)"):
    """The Apis bull in the Egyptian manner, walking right in gold line, the sun disc between its lyre-shaped horns: (x, y) = between its
    hooves; s = its length."""
    k = s / 100.0
    P = lambda pts: [(x + (a_ - 50) * k, y - (60 - b_) * k) for a_, b_ in pts]
    body = [(8, 15), (20, 13), (34, 13.5), (48, 13), (58, 11), (64, 9.5), (70, 10.5), (76, 13.5), (81, 16.5), (85, 17.5), (88, 20), (93, 27),
            (96.5, 33), (97, 36), (95, 38.5), (91, 38), (87, 35.5), (83, 33), (80, 34), (77, 38), (74, 42), (72, 44),
            (72, 47), (73, 53), (72.5, 58), (73.5, 60), (69.5, 60), (69, 54), (68.5, 48), (67, 47.5),
            (66, 50), (65.5, 58), (66, 60), (62.5, 60), (62.5, 53), (62, 47), (56, 46), (44, 46.5), (34, 45.5),
            (31, 47), (30.5, 54), (31.5, 60), (28, 60), (27, 53), (27, 48), (25, 47.5),
            (23.5, 50), (21.5, 54), (22.5, 58), (23.5, 60), (19.5, 60), (18, 55), (16.5, 48), (11, 42), (8.5, 34), (7.5, 24)]
    w = max(2.0, .55 * k)
    els = [poly(P(body), fill, c, w, 0),
           ln(P([(8, 16), (4.5, 24), (3, 36), (3.5, 46)]), 0, c, w, curve=True, draw=False),                     # the tail
           poly(E(*P([(3.6, 49.5)])[0], 1.6 * k, 3.2 * k, 12), c, at=0),
           ln(P([(81, 15.5), (78, 9), (78.5, 3), (82, -.5)]), 0, c, w * 1.2, curve=True, draw=False),                # the horns, a lyre
           ln(P([(84.5, 16.5), (88.5, 10), (89, 3.5), (85.6, -.5)]), 0, c, w * 1.2, curve=True, draw=False),
           circ(*P([(83.8, -4.2)])[0], 4.8 * k, "rgba(232,184,122,.35)", c, w, 0),                                # the sun disc
           poly(E(*P([(79.5, 19)])[0], 2.4 * k, 1.3 * k, 12), c, at=0, op=.8),                                   # the ear
           circ(*P([(89.2, 24)])[0], .9 * k, c, at=0),                                                           # the eye
           poly(P([(86.5, 20.5), (89, 21.5), (87.2, 23)]), c, at=0, op=.7)]                                       # the white blaze
    for j in range(4):                                                                                       # the saddle cloth
        els.append(ln(P([(38 + j * 5, 14), (37 + j * 5, 30)]), 0, c, w * .6, draw=False, op=.55))
    els.append(ln(P([(36, 30), (58, 29)]), 0, c, w * .6, draw=False, op=.55))
    return [grp(els, at, "fade", dur=1.2)]


def s30():
    """The Apis bull in gold line, Egyptian style, a sun disc between its horns; under it a timeline 1400 BCE to 1 CE, and a band of
    about 1,400 years of burials at Saqqara, from Amenhotep III to the Ptolemies."""
    tb, tt = T("s30", "Apis bulls"), T("s30", "fourteen hundred")
    els = [gl(889, 380, 420, -1, .25)] + apis(889, 520, 460, .3)
    els += [lab(889, 160, "the Apis bull of Memphis", tb, GOLD, 32, st="serif")]
    X = lambda yr: 250 + (yr + 1400) / 1400.0 * 1280
    els += [axis(250, 1530, 650, [(X(-1400), "1400 BCE"), (X(-1000), "1000"), (X(-600), "600"), (X(-200), "200"), (X(0), "1 CE")], tt - .6),
            rect(X(-1390), 598, X(-30) - X(-1390), 20, AMBER, at=tt, fx="fill", r=10),
            lab(X(-1390), 580, "Amenhotep III", tt + .4, DIM, 24, "start"), lab(X(-30), 580, "the Ptolemies", tt + .5, DIM, 24, "end"),
            lab((X(-1390) + X(-30)) / 2, 580, "burials for about 1,400 years", tt + .8, AMBER, 28)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s31():
    """Inside a box: the inner wall face-on, a small figure holding a steel straightedge to it with a torch behind; beside it the method,
    magnified: a true edge on a surface with a dip lets a sliver of light through; on the box wall, no light."""
    tse, tto, thold, tdip, tnone, tflat = (T("s31", "straightedge"), T("s31", "torch"), T("s31", "Hold a true"), T("s31", "any dip"),
                                           T("s31", "He saw none"), T("s31", "Perfectly flat"))
    thold = min(thold, tse + .6)                  # the true edge on a surface comes with the word 'straightedge'; its light with 'any dip'
    els = [gl(450, 470, 520, -1, .25)]
    # the inner wall of a box, a figure in it
    els += [rect(120, 200, 640, 520, BOXC, "rgba(255,236,206,.35)", 2, 4, -1),
            poly([(120, 200), (760, 200), (700, 250), (180, 250)], "#4a4542", at=-1), poly([(120, 720), (760, 720), (700, 690), (180, 690)], "#1d1a18", at=-1)]
    rnd = random.Random(31)
    els += [circ(rnd.uniform(140, 740), rnd.uniform(260, 690), rnd.uniform(1, 2.3), rnd.choice(["#cfc8be", "#141110", "#8a8078"]), at=-1, op=.55) for _ in range(160)]
    els += fig(560, 715, 330, .3, "#1a1410", "point", -1)
    els += chip(440, 160, "Christopher Dunn, 1995", GOLD, .5, 28)
    els += [rect(300, 420, 130, 7, "#dfe3e8", "rgba(0,0,0,.4)", 1, 1, tse, fx="pop"), gl(360, 420, 60, tse + .1, .5, "blue")]
    els += [gl(300, 470, 90, tto, .9), lab(250, 520, "a torch", tto + .2, DIM, 24, "end")]
    # the method, magnified: a dip lets light through
    fx0 = 920
    els += [rect(fx0, 180, 740, 270, "rgba(18,13,10,.85)", "rgba(255,236,206,.3)", 2, 12, thold - .3, fx="pop"),
            lab(fx0 + 370, 222, "a true edge on a surface", thold - .1, DIM, 26)]
    sy = 380
    dip = [(fx0 + 40, sy)] + [(fx0 + 40 + u * 660, sy + 16 * math.sin(math.pi * min(1, max(0, (u - .3) / .4)))) for u in [i / 30 for i in range(31)]] + [(fx0 + 700, sy)]
    els += [poly(dip + [(fx0 + 700, 430), (fx0 + 40, 430)], "#6f6a66", "rgba(255,236,206,.4)", 1.2, thold, fx="pop"),
            rect(fx0 + 40, sy - 26, 660, 26, "#dfe3e8", "rgba(0,0,0,.5)", 1, 2, thold + .3, fx="pop"),
            gl(fx0 + 370, sy + 4, 150, tdip - .5, .55)]
    sl = [(fx0 + 40 + u * 660, sy + 16 * math.sin(math.pi * min(1, max(0, (u - .3) / .4)))) for u in [i / 30 for i in range(9, 22)]]
    els += [poly([(sl[0][0], sy)] + sl + [(sl[-1][0], sy)], "#ffe9a8", at=tdip, fx="pop"),
            lab(fx0 + 560, sy + 52 if False else 290, "a dip shows as light", tdip + .2, "#ffe9a8", 28)]
    # on the box wall: no light
    els += [rect(fx0, 490, 740, 250, "rgba(18,13,10,.85)", "rgba(255,236,206,.3)", 2, 12, tnone - .2, fx="pop"),
            rect(fx0 + 40, 640, 660, 60, BOXC, "rgba(255,236,206,.4)", 1.2, 0, tnone),
            rect(fx0 + 40, 614, 660, 26, "#dfe3e8", "rgba(0,0,0,.5)", 1, 2, tnone + .2, fx="pop"),
            lab(fx0 + 370, 545, "on the box wall: no light", tnone + .3, BONE, 28),
            lab(fx0 + 370, 590, "perfectly flat, he reported", tflat, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s32():
    """The box from outside, dotted lilac 'machined?'; a dotted arrow runs back along a timeline to 'older than the tunnels?' and loops back
    into a tunnel: 'reused?' (claims, dotted)."""
    tm, to, tr = T("s32", "Machined"), T("s32", "older than"), T("s32", "and reused")
    els = [gl(560, 470, 460, -1, .25)] + stone_box(380, 560, 360, 210, 200, -1, lid=90, lid_dx=60, seed=7)
    els += [poly([(366, 574), (754, 574), (874, 520), (874, 230), (480, 230), (366, 284)], "none", LILAC, 2.5, tm, style="claimed", fx="draw", dur=.7),
            lab(620, 190, "machined? (Dunn)", tm + .3, LILAC, 32)]
    X = lambda u: 220 + u * 1340
    els += [ln([(X(0), 690), (X(1), 690)], .2, DIM, 2.5, dur=.6), lab(X(1), 740, "Late Period: c. 612 BCE", .4, GOLD, 26, "end"),
            circ(X(.86), 690, 9, GOLD, at=.4, fx="pop"), lab(X(0), 740, "earlier?", to, LILAC, 26, "start")]
    els += [arr([(840, 600), (700, 650), (X(.2), 676)], to, LILAC, 3, "claimed", dur=.9),
            lab(X(.17), 630, "older than the tunnels?", to + .5, LILAC, 30, "start")]
    # a tunnel mouth at the right, the arrow loops into it
    tx, ty = 1380, 560
    els += [poly([(tx - 120, ty), (tx - 120, ty - 150)] + E(tx, ty - 150, 120, 110, 18, 180, 360)[1:-1] + [(tx + 120, ty - 150), (tx + 120, ty)],
                  "#0f0c0a", "rgba(255,236,206,.35)", 2, -1),
            arr([(X(.14), 700), (X(.5), 760), (tx - 60, 720), (tx - 20, ty - 60)], tr, LILAC, 3, "claimed", dur=1.0),
            lab(tx, 300, "reused?", tr + .5, LILAC, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def cartouche(x, y, w, h, name, sub, at):
    """A horizontal cartouche plaque: an oval ring with a tie at the right end, the king's name and his dates under it."""
    return [rect(x - w / 2, y - h / 2, w, h, "rgba(242,201,142,.08)", GOLD, 3, h / 2, at, fx="pop"),
            rect(x + w / 2 + 6, y - h / 2 + 8, 9, h - 16, GOLD, at=at, fx="pop"),
            lab(x, y + 11, name, at + .1, GOLD, 34, st="serif"), lab(x, y + h / 2 + 40, sub, at + .3, DIM, 26)]


def kings_timeline(at_axis, at_dots, at_band, y=640):
    """700 to 300 BCE: the Greater Vaults band from c. 612 BCE (still in use after 300), three gold dots for the kings' dated burials."""
    X = lambda yr: 230 + (yr + 700) / 400.0 * 1320
    els = [axis(230, 1550, y, [(X(-700), "700 BCE"), (X(-600), "600"), (X(-500), "500"), (X(-400), "400"), (X(-300), "300")], at_axis)]
    els += [rect(X(-612), y - 66, X(-300) - X(-612) + 40, 20, AMBER, at=at_band, fx="fill", r=10, op=.85),
            lab(X(-612) - 16, y - 50, "Greater Vaults, from c. 612 BCE", at_band + .3, AMBER, 26, "end")]
    for k, (yr, nm) in enumerate(((-548, "Amasis"), (-524, "Cambyses"), (-337, "Khababash"))):
        els += [circ(X(yr), y, 11, GOLD, "#1a1410", 2, at_dots + .2 * k, fx="pop")]
    return els, X


def s33():
    """Three gold cartouche plaques pop as named (Amasis II, Cambyses II, Khababash, with their dates); a timeline 700 to 300 BCE draws
    under them, the kings' dated burials as gold dots, and the Greater Vaults band from c. 612 BCE."""
    ta, tc, tk, tr, tv = T("s33", "Amasis"), T("s33", "Cambyses"), T("s33", "Khababash"), T("s33", "They ruled"), T("s33", "Greater Vaults")
    els = [lab(889, 160, "names carved on the boxes", .4, DIM, 28)]
    els += [rect(x - 165, 208, 330, 84, "none", "rgba(242,201,142,.3)", 2, 42, -1, style="inferred") for x in (380, 889, 1398)]
    for x, nm, sub, t in ((380, "Amasis II", "c. 570 to 526 BCE", ta), (889, "Cambyses II", "c. 525 BCE", tc), (1398, "Khababash", "c. 336 BCE", tk)):
        els += cartouche(x, 250, 330, 84, nm, sub, t)
    tl, X = kings_timeline(.6, tr + .6, tv)
    els += tl
    for k, (yr, x) in enumerate(((-548, 380), (-524, 889), (-337, 1398))):
        els.append(ln([(x, 350), (X(yr), 628)], tr + .9 + .2 * k, "rgba(242,201,142,.5)", 1.5, "inferred", dur=.5))
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def stela(x, y, w, h, at, bull=False):
    els = [poly([(x - w / 2, y), (x - w / 2, y - h + w / 2)] + E(x, y - h + w / 2, w / 2, w / 2, 12, 180, 360)[1:-1] + [(x + w / 2, y - h + w / 2), (x + w / 2, y)],
                "#d8c7a4", "rgba(90,60,30,.6)", 1, 0)]
    for j in range(3):
        els.append(ln([(x - w * .32, y - h * .45 + j * h * .12), (x + w * .32, y - h * .45 + j * h * .12)], 0, "#7a5a3a", 1.5, draw=False, op=.7))
    if bull:
        els.append(poly([(x - w * .28, y - h * .62), (x + w * .2, y - h * .64), (x + w * .3, y - h * .72), (x + w * .26, y - h * .58), (x - w * .26, y - h * .54)], "#8a5a32", at=0))
    return grp(els, at, "pop")


def s34():
    """A wall of small round-topped stelae (some with a bull carved on them) pops in; under them the timeline of s33, and a bracket closes
    round the three kings' dots: 'inside the window'."""
    th, tw = T("s34", "Hundreds of inscribed"), T("s34", "The kings' names")
    els = []
    rnd = random.Random(34)
    k = 0
    for r_ in range(3):
        for c_ in range(14):
            x = 300 + c_ * 84 + (42 if r_ % 2 else 0)
            if x > 1490:
                continue
            els.append(stela(x, 220 + r_ * 92 + 70, 56, 76, th + .03 * k, bull=rnd.random() < .35))
            k += 1
    els += [lab(889, 160, "stelae of priests and pilgrims, dated by reign", th + .4, DIM, 26)]
    tl, X = kings_timeline(-1, -1, -1, y=660)
    els += static(tl)
    els += bracket(X(-560), X(-325), 576, tw, "inside the window", GOLD, up=False, size=28, ty=556)
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """The box's long inner wall drawn to scale (3.17 m by 1.73 m inside), three short straightedge marks on it; then a dotted pale-blue
    grid spreads over the whole wall: 'a full survey: not yet done'; 'his wish: scan it all'."""
    tf, tn, td = T("s35", "A few checks"), T("s35", "never published"), T("s35", "Dunn himself")
    m = 300.0
    x0, y0, W, H = 360, 200, 3.17 * m, 1.73 * m
    els = [rect(x0, y0, W, H, BOXC, "rgba(255,236,206,.4)", 2, 2, -1)]
    rnd = random.Random(35)
    els += [circ(rnd.uniform(x0 + 6, x0 + W - 6), rnd.uniform(y0 + 6, y0 + H - 6), rnd.uniform(1, 2.4), rnd.choice(["#cfc8be", "#141110", "#8a8078"]), at=-1, op=.55)
            for _ in range(240)]
    els += [{"k": "dim", "x1": x0, "y1": y0 - 26, "x2": x0 + W, "y2": y0 - 26, "t": "inside: 3.17 m", "ly": -16, "c": DIM, "in": .3, "fx": "draw", "dur": .7}]
    for k, (x, y) in enumerate(((x0 + 260, y0 + 160), (x0 + 520, y0 + 330), (x0 + 760, y0 + 210))):
        els += [rect(x - 25, y - 4, 50, 8, "#dfe3e8", at=tf + .3 * k, fx="pop"), gl(x, y, 40, tf + .3 * k, .6, "blue")]
    els += [lab(x0 + W / 2, y0 + H + 50, "a few short checks", tf + .8, BONE, 28)]
    for j in range(1, 8):
        els.append(ln([(x0 + j * W / 8, y0), (x0 + j * W / 8, y0 + H)], tn + .06 * j, BLUE, 1.5, "inferred", dur=.5, op=.75))
    for j in range(1, 5):
        els.append(ln([(x0, y0 + j * H / 5), (x0 + W, y0 + j * H / 5)], tn + .5 + .06 * j, BLUE, 1.5, "inferred", dur=.5, op=.75))
    els += [rect(x0, y0, W, H, "none", BLUE, 2.5, 2, tn, style="inferred", fx="draw"),
            lab(x0 + W + 30, y0 + 60, "a full survey:", tn + .9, BLUE, 28, "start"), lab(x0 + W + 30, y0 + 100, "not yet done", tn + 1.0, BLUE, 28, "start"),
            lab(x0 + W + 30, y0 + 200, "his wish:", td, GOLD, 26, "start"), lab(x0 + W + 30, y0 + 236, "scan it all", td + .1, GOLD, 26, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s36():
    """Lapping by hand, in three steps left to right: two stones in section, the upper rubbed back and forth over the lower with sand
    between; the lower's high spots (exaggerated) wear down until the line is flat."""
    t1, t2, t3 = T("s36", "rub stone"), T("s36", "with sand"), T("s36", "the high spots")
    els = [lab(889, 190, "lapping, by hand", .3, GOLD, 34, st="serif")]
    amps = [(22, t1), (11, t2), (0, t3)]
    names = ["high spots", "sand between", "flat"]
    for k, (a, t) in enumerate(amps):
        cx = 360 + k * 530
        x0, x1, ty = cx - 200, cx + 200, 520
        prof = [(x0 + u * 400, ty - a * max(0, math.sin(u * 9.4)) ** 2) for u in [i / 40 for i in range(41)]]
        top = min(p[1] for p in prof)
        ts_ = .5 if k == 0 else t                 # the first pair is there from the start; the others wait as faint outlines
        if k:
            els += [poly([(x0, 640)] + prof + [(x1, 640)], "none", "rgba(255,236,206,.22)", 1.5, -1, style="inferred"),
                    rect(cx - 130, top - 90, 260, 86, "none", "rgba(255,236,206,.22)", 1.5, 2, -1, style="inferred")]
        els += [poly([(x0, 640)] + prof + [(x1, 640)], GRAN, "rgba(255,236,206,.35)", 1.2, ts_, fx="pop"),
                rect(cx - 130, top - 90, 260, 86, mix(GRAN, "#ffffff", .15), "rgba(255,236,206,.35)", 1.2, 2, ts_ + .2, fx="pop"),
                arr([(cx - 60, top - 120), (cx + 60, top - 120)], t + .4, AMBER, 3, dur=.4, curve=False),
                arr([(cx + 60, top - 104), (cx - 60, top - 104)], t + .5, AMBER, 3, dur=.4, curve=False)]
        if k == 1:
            rnd = random.Random(3)
            els += [circ(x0 + rnd.uniform(10, 390), top - 2 + rnd.uniform(0, 8), 3, "#f2e6c8", at=t + .6, fx="pop") for _ in range(26)]
        els += [lab(cx, 700, names[k], t + .5, BONE if k < 2 else GREEN, 28)]
        if k < 2:
            els.append(arr([(cx + 220, 560), (cx + 300, 560)], t + .7, DIM, 2.5, dur=.4, curve=False))
    return {"base": "dark", "cam": CAM, "els": els}


def s37():
    """Left: a strip map of the Nile from Aswan (bottom) to Saqqara (top), a barge with a box drawing its route north, 'nearly 900 km'.
    Right: a plan of the gallery and one side room; a box on a sledge in the corridor and a dotted lilac arc into the room: 'how? not
    recorded'."""
    tg, th = T("s37", "The granite came"), T("s37", "how each box")
    from scenes import NILE
    mx0, my0, mw, mh = 140, 140, 600, 650
    v = View(29.9, 34.1, 23.7, 30.3, rect=(mx0, my0, mw, mh))
    nile = [v.p(lo, la) for lo, la in NILE[:13]]
    els = [{"k": "group", "clip": [mx0, my0, mw, mh, 14], "in": -1, "els": [
               rect(mx0, my0, mw, mh, "#22343f", at=0), {"k": "map", "land": v.land(), "in": 0},
               ln(nile, 0, "#3f86a8", 9, curve=True, draw=False), ln(nile, 0, "#8fc4dc", 2.5, curve=True, draw=False)]},
           rect(mx0, my0, mw, mh, "none", "rgba(255,236,206,.35)", 2, 14, -1)]
    ax_, ay_ = nile[0]
    sx_, sy_ = nile[-1]
    els += [circ(ax_, ay_, 10, GOLD, "#1a1410", 2, -1), lab(ax_ - 22, ay_ + 10, "Aswan", -1, GOLD, 30, "end"),
            circ(sx_, sy_, 10, GOLD, "#1a1410", 2, -1), lab(sx_ - 22, sy_ + 10, "Saqqara", -1, GOLD, 30, "end"),
            ln(nile, tg, AMBER, 5, curve=True, dur=2.6),
            lab(mx0 + mw / 2 + 120, my0 + mh / 2 + 40, "nearly 900 km", tg + 1.2, AMBER, 30, "middle")]
    bx_, by_ = v.p(31.18, 27.18)
    els += [grp([poly([(bx_ - 44, by_ - 6), (bx_ + 44, by_ - 6), (bx_ + 32, by_ + 12), (bx_ - 32, by_ + 12)], "#8a6a44", "#e7c99a", 1.2, 0),
                 rect(bx_ - 22, by_ - 24, 44, 18, BOXC, "rgba(255,236,206,.6)", 1, 1, 0)], tg + 1.4, "pop"),
            lab(bx_ - 56, by_ + 6, "a barge", tg + 1.6, BONE, 24, "end")]
    # the plan of a gallery stretch and one side room
    px0, px1, cy0, cy1 = 900, 1660, 520, 640
    els += [rect(px0, cy0, px1 - px0, cy1 - cy0, "#2a2119", "rgba(255,236,206,.35)", 2, 2, th - .6, fx="pop"),
            rect(1180, 250, 280, 270, "#2a2119", "rgba(255,236,206,.35)", 2, 2, th - .6, fx="pop"),
            rect(1180, 516, 280, 8, "#2a2119", at=th - .55),
            lab(px0 + 20, cy1 + 40, "corridor", th - .4, DIM, 24, "start"), lab(1320, 230, "side room", th - .4, DIM, 24)]
    els += [rect(960, 548, 200, 64, BOXC, "rgba(255,236,206,.5)", 1.5, 2, th, fx="pop"),
            ln([(950, 616), (1170, 616)], th, "#a8875a", 4, draw=False), ln([(950, 544), (1170, 544)], th, "#a8875a", 4, draw=False)]
    els += [arr([(1100, 540), (1200, 470), (1290, 420), (1320, 330)], th + .5, LILAC, 3, "claimed", dur=1.0),
            lab(1560, 380, "how?", th + 1.2, LILAC, 34),
            lab(1560, 430, "not recorded", th + 1.4, LILAC, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · A power plant?
GS = Section(s=4.2, cx=889, gy=770)            # the Great Pyramid in north-south section, north on the left, 4.2 units a metre
SECBASE = {"base": "section", "tod": "night", "ground": 770, "lx": 40,
           "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 60, "c": "#4d3e30", "t": ""}]}
SA = math.radians(39.5)
KCX, KCY = 923.6, 577.2                        # the King's Chamber's centre on the panel (5.2 m by 5.8 m)
QCX, QCY = 889.0, 668.0                        # the Queen's Chamber's centre
SKY_Y0, SKY_Y1 = -900, 770                     # the night sky's gradient runs over these heights (the section base's sky rectangle)
ROOM = "#2a2018"                               # the inside of the passages and chambers: dark, warm


def face_hit(x, h, dx, dh):
    """Where a ray from (x, h) along (dx, dh) meets the pyramid's faces (metres)."""
    t = math.tan(SLOPE)
    best = None
    for kind in ("n", "s"):
        if kind == "n":
            den, num = dh - dx * t, x * t - h
        else:
            den, num = dh + dx * t, (GB - x) * t - h
        if abs(den) > 1e-9:
            u = num / den
            if u > 0 and (best is None or u < best):
                best = u
    return (x + dx * best, h + dh * best)


def gp_shafts():
    """The four shafts as panel polylines: the Queen's Chamber pair (about 39.5 degrees, the northern one bent, both ending at small stone
    doors short of the faces) and the King's Chamber pair (the southern at about 45 degrees, the northern about 32.5), out to the faces."""
    R = GS.rooms()
    qx, _ = R["qc"]
    kx, kh = R["kc"]
    s1 = (qx + 4.6, 22.0)
    qs = [(qx + 2.6, 22.0), s1, (s1[0] + 58 * math.cos(SA), s1[1] + 58 * math.sin(SA))]
    n1 = (qx - 4.6, 22.0)
    n2 = (n1[0] - 24 * math.cos(SA), n1[1] + 24 * math.sin(SA))
    b = math.radians(46)
    n3 = (n2[0] - 9 * math.cos(b), n2[1] + 9 * math.sin(b))
    qn = [(qx - 2.6, 22.0), n1, n2, n3, (n3[0] - 26 * math.cos(SA), n3[1] + 26 * math.sin(SA))]
    a45, a32 = math.radians(45), math.radians(32.5)
    ks0, kn0 = (kx + 2.6, kh + 1.0), (kx - 2.6, kh + 1.5)
    ks = [ks0, face_hit(*ks0, math.cos(a45), math.sin(a45))]
    kn = [kn0, face_hit(*kn0, -math.cos(a32), math.sin(a32))]
    P = lambda q: tuple(GS.P(*q))
    return {"qs": [P(q) for q in qs], "qn": [P(q) for q in qn], "ks": [P(q) for q in ks], "kn": [P(q) for q in kn]}


def gp_body(at=-1, fx=None, dur=None):
    """The pyramid in section: its body, the light on its faces, the passages, the Grand Gallery, both chambers and the five low rooms
    above the King's Chamber (the descending passage stops at the bedrock line of the drawing)."""
    S = GS
    R = S.rooms()
    ent, sub = R["ent"], R["sub"]
    u = (ent[1] + 4.0) / (ent[1] - sub[1])
    low = (ent[0] + u * (sub[0] - ent[0]), -4.0)
    els = [dict(S.body()), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0},
           {"k": "line", "p": [S.P(*ent), S.P(*low)], "c": BONE, "w": 2.2, "op": .85}]
    els += [dict(e, op=.85) for e in S.els(which=("asc", "gg", "qc", "kc", "reliev"), fill=ROOM)]
    g = gp_shafts()
    els += [ln(g[k], 0, "#e8d6b8", 2.2, draw=False, op=.8) for k in ("qs", "qn", "ks", "kn")]
    els += [poly([(KCX - 10.9, KCY - 12.2), (KCX + 10.9, KCY - 12.2), (KCX + 10.9, KCY + 12.2), (KCX - 10.9, KCY + 12.2)], GRAN, BONE, 1.8, 0)]
    e = grp(els, at, fx)
    if dur:
        e["dur"] = dur
    return e


def sky_veil(pts, at, dur=1.2):
    """A patch of the night sky laid over what is drawn there (it fades in, so what was there fades out): its fill is the sky's own
    gradient, mapped to the same heights by two zero-width spikes that stretch its bounding box from the top of the sky to the ground."""
    x0, y0 = pts[0]
    p = list(pts) + [(x0, y0), (x0, SKY_Y0), (x0, y0), (x0, SKY_Y1), (x0, y0)]
    e = poly(p, "url(#k-sky-night)", "none", 0, at, fx="fade")
    e["dur"] = dur
    return e


def band(p0, p1, w):
    """A quadrilateral w units either side of the segment p0 p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * w, dx / L * w
    return [(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)]


BEAM_END = (1262, 257)                          # the claimed beam, out of the southern shaft into the night
LBL_KC = (1185, 458)                            # "King's Chamber, granite", out beyond the south face
LBL_ENGINE = (420, 330)                         # "the parts of an engine?", in the sky to the north
LBL_BEAM = (1292, 302)                          # "a microwave beam?"


def s39():
    """The Great Pyramid in north-south section at night, to scale (base 230 m, 146.6 m high, 4.2 units a metre): passages, the Grand
    Gallery, both chambers and the five low rooms; on 'narrow shafts' its four shafts trace themselves; on 'granite heart' the King's
    Chamber glows granite pink ('King's Chamber, granite'); on 'parts of an engine', a lilac question."""
    tsh, tg, te = T("s39", "narrow shafts"), T("s39", "granite heart"), T("s39", "parts of an")
    S = GS
    R = S.rooms()
    ent, sub = R["ent"], R["sub"]
    u = (ent[1] + 4.0) / (ent[1] - sub[1])
    low = (ent[0] + u * (sub[0] - ent[0]), -4.0)
    els = [dict(S.body(), **{"in": -1}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": -1},
           {"k": "line", "p": [S.P(*ent), S.P(*low)], "c": BONE, "w": 2.2, "op": .85, "in": -1}]
    els += [dict(e, **{"in": -1, "op": .85}) for e in S.els(which=("asc", "gg", "qc", "kc", "reliev"), fill=ROOM)]
    els += chip(420, 262, "Dunn, 1998", GOLD, .4, 28)
    g = gp_shafts()
    for k, key in enumerate(("kn", "ks", "qn", "qs")):
        els.append(ln(g[key], tsh + .12 * k, "#e8d6b8", 2.2, dur=.8, op=.8))
    els += [gl(KCX, KCY, 90, tg, .8),
            poly([(KCX - 10.9, KCY - 12.2), (KCX + 10.9, KCY - 12.2), (KCX + 10.9, KCY + 12.2), (KCX - 10.9, KCY + 12.2)], GRAN, BONE, 1.8, tg, fx="pop"),
            ln([(KCX + 13, KCY - 4), (LBL_KC[0] - 12, LBL_KC[1] - 10)], tg + .2, GOLD, 1.5, dur=.5, op=.8),
            lab(LBL_KC[0], LBL_KC[1], "King's Chamber, granite", tg + .4, GOLD, 28, "start"),
            lab(QCX, 742, "Queen's Chamber", tsh - .4, BONE, 26)]
    els += [lab(LBL_ENGINE[0], LBL_ENGINE[1], "the parts of an engine?", te, LILAC, 30)]
    return dict(SECBASE, cam=CAM, els=els)


def s40_add():
    """Dunn's machine, drawn in lilac dots as it is named: drops run down the Queen's Chamber shafts to a pale cloud ('hydrogen?'); rings
    ripple round the granite King's Chamber ('ringing granite?'); a beam leaves through the southern shaft into the night ('a microwave
    beam?')."""
    tq, th, tk, tb = T("s40", "Chemicals fed"), T("s40", "make hydrogen"), T("s40", "The granite"), T("s40", "a beam")
    g = gp_shafts()
    els = []
    for key in ("qs", "qn"):
        pts = g[key]
        els.append(ln(pts, tq, LILAC, 3.5, "claimed", dur=.7))
        segs = list(zip(pts, pts[1:]))
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
        for k in range(7):                                    # drops, from the far end down to the chamber
            d = L * (1 - (k + .5) / 7)
            for a, b in segs:
                sl = math.hypot(b[0] - a[0], b[1] - a[1])
                if d <= sl:
                    x, y = a[0] + (b[0] - a[0]) * d / sl, a[1] + (b[1] - a[1]) * d / sl
                    break
                d -= sl
            els.append(circ(x, y, 5, LILAC, at=tq + .3 + .18 * k, fx="pop"))
    els += [poly(blob(QCX + 4, QCY + 2, 62, 30, 20, .18, 5), "rgba(201,193,238,.22)", LILAC, 2.2, th, style="claimed", fx="pop"),
            lab(1010, 712, "hydrogen?", th + .3, LILAC, 28, "start")]
    for k in range(3):
        els.append(circ(KCX, KCY, 34 + 20 * k, "none", LILAC, 2.6, tk + .5 + .25 * k, style="claimed", fx="pop", op=.95 - .2 * k))
    els += [lab(KCX, 478, "ringing granite?", tk + 1.0, LILAC, 28)]
    ex, ey = g["ks"][-1]
    els += [ln([(KCX + 8, KCY - 6), g["ks"][0], (ex, ey), BEAM_END], tb, LILAC, 14, dur=1.3, op=.1),
            ln([(KCX + 8, KCY - 6), g["ks"][0], (ex, ey), BEAM_END], tb, LILAC, 5.5, "claimed", dur=1.3),
            lab(LBL_BEAM[0], LBL_BEAM[1], "a microwave beam?", tb + 1.1, LILAC, 28, "start")]
    return els


CHK = [("the salt", "salt"), ("the granite", "granite"), ("the builders", "builders")]


def cube(x, y, s, at=0, fx=None, tones=("#f7f4ee", "#dcd6ca", "#bdb5a6"), op=None):
    """A small isometric cube (a salt crystal): its front bottom corner on (x, y), edge s."""
    c, h = s * C30, s * .5
    B, Lf, Rt, Tp = (x, y), (x - c, y - h), (x + c, y - h), (x, y - s)
    TL, TR, TT = (x - c, y - h - s), (x + c, y - h - s), (x, y - 2 * h - s)
    edge = "rgba(90,80,70,.45)"
    els = [poly([B, Lf, TL, Tp], tones[1], edge, .8, 0), poly([B, Rt, TR, Tp], tones[2], edge, .8, 0), poly([Tp, TL, TT, TR], tones[0], edge, .8, 0)]
    e = grp(els, at, fx)
    if op is not None:
        gdim(e, op)
    return e


def icon(kind, x, y, s=1.0, at=-1):
    """The picture of each check: the salt (three little crystals), the granite (a speckled pink disc), the builders (a red cartouche)."""
    if kind == "salt":
        els = [cube(x - 13 * s, y + 14 * s, 15 * s), cube(x + 13 * s, y + 16 * s, 12 * s), cube(x + 1 * s, y + 3 * s, 13 * s)]
    elif kind == "granite":
        rnd = random.Random(8)
        els = [circ(x, y, 22 * s, GRAN, "rgba(255,236,206,.5)", 1.4, 0)]
        els += [circ(x + rnd.uniform(-14, 14) * s, y + rnd.uniform(-14, 14) * s, rnd.uniform(1.6, 3.2) * s, rnd.choice(["#f6ece4", "#3a2a28", "#e9c7b8"]), at=0)
                for _ in range(12)]
    else:
        els = [rect(x - 13 * s, y - 25 * s, 26 * s, 46 * s, "none", OCHRE, 3, 13 * s, 0), ln([(x - 11 * s, y + 26 * s), (x + 11 * s, y + 26 * s)], 0, OCHRE, 3, draw=False),
               circ(x, y - 12 * s, 5 * s, "none", OCHRE, 2, 0), ln([(x - 6 * s, y + 2 * s), (x + 6 * s, y + 2 * s)], 0, OCHRE, 2, draw=False),
               ln([(x - 6 * s, y + 11 * s), (x + 6 * s, y + 11 * s)], 0, OCHRE, 2, draw=False)]
    return grp(els, at, "pop" if at >= 0 else None)


def checkbox(x, y, at, size=40):
    return rect(x - size / 2, y - size / 2, size, size, "rgba(18,13,10,.6)", GOLD, 2.2, 8, at, fx="pop" if at >= 0 else None)


def checks_row(x0, y, done=0, now=None, at=0.0, gap=128):
    """The three checks as a row of pictures, each beside its box: the first `done` already ticked; box `now` ticks at `at`."""
    els = []
    for k, (_, kind) in enumerate(CHK):
        x = x0 + k * gap
        els += [icon(kind, x, y, .85, -1), checkbox(x + 46, y, -1, 34)]
        if k < done:
            els += static([tick(x + 46, y, 0, GREEN, .9, 5)])
        elif k == now:
            els.append(tick(x + 46, y, at, GREEN, .9, 5))
    return els


def chamber_wall(x0, y0, m, at=-1):
    """The east wall of the Queen's Chamber face-on (m units a metre): 5.23 m wide, 4.67 m to the eaves, a gable to 6.23 m; limestone
    courses, and the stepped niche a little south of the middle. (x0, y0) = its bottom left corner."""
    W, He, Ha = 5.23 * m, 4.67 * m, 6.23 * m
    xm = x0 + W / 2
    out = [poly([(x0, y0), (x0 + W, y0), (x0 + W, y0 - He), (xm, y0 - Ha), (x0, y0 - He)], LIME, "rgba(255,236,206,.45)", 1.5, 0),
           poly([(x0, y0), (x0 + W, y0), (x0 + W, y0 - He), (xm, y0 - Ha), (x0, y0 - He)], "url(#k-speck)", "none", 0, 0)]
    rnd = random.Random(41)
    yy = y0
    while yy > y0 - He + 20:
        hh = rnd.uniform(.8, 1.05) * m
        top = max(y0 - He, yy - hh)
        out.append(ln([(x0, top), (x0 + W, top)], 0, "rgba(90,70,50,.55)", 1.6, draw=False))
        xx = x0 + rnd.uniform(.3, 1.2) * m
        while xx < x0 + W - 20:
            out.append(ln([(xx, top), (xx, yy)], 0, "rgba(90,70,50,.45)", 1.4, draw=False))
            xx += rnd.uniform(1.1, 1.9) * m
        yy = top
    for side in (-1, 1):                                          # the gable's sloping beams
        out.append(ln([(xm, y0 - Ha), (xm + side * W / 2, y0 - He)], 0, "rgba(90,70,50,.6)", 2, draw=False))
    nx, nw = xm + .55 * m, 1.57 * m                               # the corbelled niche: four steps in
    for k in range(5):
        w = nw - k * .22 * m
        h0, h1 = k * .934 * m, (k + 1) * .934 * m
        out.append(poly([(nx - w / 2, y0 - h0), (nx + w / 2, y0 - h0), (nx + w / 2, y0 - h1), (nx - w / 2, y0 - h1)], mix(LIME, "#3a2c1e", .32 + .06 * k), "rgba(90,70,50,.6)", 1.2, 0))
    return [grp(out, at, None)]


def salt_patch(x, y, w, at, seed=1, n=9):
    """A bloom of salt crust: white flakes and tiny crystals, about w units across."""
    rnd = random.Random(seed)
    els = [poly(blob(x, y, w * .5, w * .22, 14, .35, seed), "rgba(250,248,242,.55)", "none", 0, 0)]
    for _ in range(n):
        els.append(cube(x + rnd.uniform(-.4, .4) * w, y + rnd.uniform(-.12, .14) * w, rnd.uniform(4, 8)))
    return grp(els, at, "pop")


def s41():
    """A machine leaves traces, so check: the three checks build in at the left (the salt, the granite, the builders, each with its
    picture and an empty box); at the right the east wall of the Queen's Chamber (gable, niche, a person for scale); on 'The salt',
    white crusts bloom on it; on 'Dunn read it', a lilac note: 'a chemical residue? (Dunn)'."""
    tm, tc, ts, td = T("s41", "a machine leaves"), T("s41", "checked"), T("s41", "The salt on"), T("s41", "Dunn read")
    els = [gl(1170, 520, 620, -1, .2)]
    for k, (name, kind) in enumerate(CHK):
        y = 340 + k * 130
        t = tm + .45 * k
        els += [checkbox(170, y, t, 50), icon(kind, 265, y, 1.15, t + .1), lab(318, y + 11, name, t + .2, BONE, 32, "start")]
        els += [gl(170, y, 70, tc + .15 * k, .7)]
    m = 88.0
    x0, y0 = 960, 760
    els += chamber_wall(x0, y0, m)
    els += [{"k": "person", "x": x0 + 1.1 * m, "y": y0, "h": 1.7 * m, "t": False, "color": "#2a2018", "in": -1},
            lab(x0 + 2.6 * m, 190, "the Queen's Chamber", -1, DIM, 28)]
    spots = [(x0 + .7 * m, y0 - .6 * m, 120), (x0 + 1.9 * m, y0 - 1.5 * m, 100), (x0 + 4.4 * m, y0 - .8 * m, 130), (x0 + 3.9 * m, y0 - 2.6 * m, 90),
             (x0 + .9 * m, y0 - 3.2 * m, 90), (x0 + 4.7 * m, y0 - 3.9 * m, 70), (x0 + 2.4 * m, y0 - 4.4 * m, 80)]
    for k, (x, y, w) in enumerate(spots):
        els.append(salt_patch(x, y, w, ts + .14 * k, seed=k + 3))
    els += [lab(x0 + 4.4 * m, y0 - 1.45 * m, "salt", ts + .9, BONE, 30)]
    els += [arr([(1500, 520), (1470, 560), (x0 + 4.75 * m, y0 - 2.75 * m)], td, LILAC, 2.5, "claimed", dur=.6),
            lab(1560, 470, "a chemical residue?", td + .2, LILAC, 28), lab(1560, 506, "(Dunn)", td + .3, LILAC, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def nummulite(x, y, r, at=-1, op=.75):
    """A coin-shaped fossil (a nummulite) in the stone, cut through: a disc and its spiral."""
    pts = [(x + r * (.12 + .88 * a / (6 * math.pi)) * math.cos(a), y + r * .62 * (.12 + .88 * a / (6 * math.pi)) * math.sin(a)) for a in [k * .3 for k in range(63)]]
    return [poly(E(x, y, r, r * .62, 24), "#c9b087", "rgba(110,85,55,.6)", 1.2, at, op=op), ln(pts, at, "rgba(110,85,55,.7)", 1.2, curve=True, draw=False, op=op)]


def s42():
    """The answer, magnified: a face of limestone full of coin-shaped fossils of sea creatures; on 'rock salt', cubes of salt grow out of
    it; on 'ancient sea', 'limestone from an ancient sea'. Then the same wall in 2022 (bare) and 2024 (crusted), 'still growing'. The
    first box ticks."""
    t26, tr, ta, tg, t22, t24 = (T("s42", "In twenty twenty-six"), T("s42", "rock salt"), T("s42", "ancient sea"), T("s42", "still growing"),
                                 T("s42", "bare in"), T("s42", "crusted by"))
    fx0, fy0, fw, fh = 120, 230, 760, 470
    rnd = random.Random(42)
    face = [rect(fx0, fy0, fw, fh, LIME, at=0), rect(fx0, fy0, fw, fh, "url(#k-speck)", at=0)]
    for _ in range(26):
        r = rnd.uniform(12, 30)
        face += nummulite(rnd.uniform(fx0 + r, fx0 + fw - r), rnd.uniform(fy0 + r, fy0 + fh - r), r, 0)
    els = [{"k": "group", "clip": [fx0, fy0, fw, fh, 16], "els": face, "in": -1},
           rect(fx0, fy0, fw, fh, "none", "rgba(255,236,206,.45)", 2, 16, -1),
           lab(fx0 + fw - 16, fy0 + fh - 18, "magnified", -1, DIM, 24, "end")]
    els += chip(fx0 + 140, 186, "a 2026 study", GOLD, t26, 26)
    spots = [(260, 330), (330, 300), (300, 390), (540, 290), (610, 340), (480, 460), (720, 420), (790, 520), (380, 570), (240, 610), (580, 620),
             (760, 640), (430, 350), (660, 540)]
    for k, (x, y) in enumerate(spots):
        s_ = rnd.uniform(16, 30)
        els.append(cube(x, y + s_, s_, tr + .08 * k, "pop"))
    els += [lab(330, 268, "rock salt", tr + .6, "#ffffff", 32)]
    els += [lab(fx0 + fw / 2, fy0 + fh + 48, "limestone from an ancient sea", ta, GOLD, 30)]
    for (x, y) in ((220, 520), (520, 540), (720, 300)):
        els.append({"k": "circle", "x": x, "y": y, "r": 34, "fill": "none", "c": GOLD, "w": 2.2, "in": round(ta + .2, 2), "fx": "draw", "dur": .5})
    # 2022 and 2024
    els += [lab(1305, 330, "still growing", tg, BONE, 32)]
    for k, (x, t, yr) in enumerate(((990, t22, "2022"), (1340, t24, "2024"))):
        els += [rect(x, 380, 280, 230, mix(LIME, "#1a140f", .55), "rgba(255,236,206,.25)", 1.5, 8, -1)]
        els += [rect(x, 380, 280, 230, LIME, "rgba(255,236,206,.45)", 1.5, 8, t, fx="pop"),
                ln([(x, 470), (x + 280, 470)], t, "rgba(90,70,50,.5)", 1.5, draw=False), ln([(x, 545), (x + 280, 545)], t, "rgba(90,70,50,.5)", 1.5, draw=False),
                ln([(x + 120, 380), (x + 120, 470)], t, "rgba(90,70,50,.45)", 1.4, draw=False), ln([(x + 200, 470), (x + 200, 545)], t, "rgba(90,70,50,.45)", 1.4, draw=False),
                lab(x + 140, 660, yr, t + .1, GOLD, 32, st="serif")]
    for k, (x, y, w) in enumerate(((1420, 565, 100), (1540, 572, 110), (1475, 505, 90), (1425, 440, 70), (1560, 455, 60))):
        els.append(salt_patch(x, y, w, t24 + .3 + .12 * k, seed=20 + k, n=6))
    els += [arr([(1280, 495), (1330, 495)], t24 - .1, DIM, 2.5, dur=.4, curve=False)]
    els += checks_row(1250, 190, 0, 0, ta + .9)
    return {"base": "dark", "cam": CAM, "els": els}


def quartz(x, y, w, h, at=-1, fx=None):
    """A clear quartz crystal standing upright: a six-sided column (three faces seen) and its pointed tip; (x, y) = its foot's centre."""
    t = h * .26
    c = [(x - w / 2, y), (x - w / 6, y + w * .08), (x + w / 6, y + w * .08), (x + w / 2, y)]
    up = lambda p, d: (p[0], p[1] - d)
    tip = (x, y - h - t)
    faces = [poly([c[0], c[1], up(c[1], h), up(c[0], h)], "rgba(236,240,244,.55)", "rgba(255,255,255,.8)", 1.4, 0),
             poly([c[1], c[2], up(c[2], h), up(c[1], h)], "rgba(250,252,255,.75)", "rgba(255,255,255,.85)", 1.4, 0),
             poly([c[2], c[3], up(c[3], h), up(c[2], h)], "rgba(200,206,214,.55)", "rgba(255,255,255,.8)", 1.4, 0),
             poly([up(c[0], h), up(c[1], h), tip], "rgba(236,240,244,.6)", "rgba(255,255,255,.85)", 1.4, 0),
             poly([up(c[1], h), up(c[2], h), tip], "rgba(255,255,255,.8)", "rgba(255,255,255,.9)", 1.4, 0),
             poly([up(c[2], h), up(c[3], h), tip], "rgba(200,206,214,.6)", "rgba(255,255,255,.85)", 1.4, 0)]
    return [grp(faces, at, fx)]


def s43():
    """Granite as a crystal generator? Left: a clear quartz crystal between two metal plates; on 'Squeeze' they press in, on 'electric
    charge' the plates show + and - and a small spark jumps ('a tiny charge'). Right: a disc of granite, its quartz grains each with a
    small arrow pointing its own way ('every which way'); on 'cancel' the same arrows laid head to tail wander and end near where they
    began ('they mostly cancel'). The second box ticks."""
    tq, tsq, tch, tw, tca = (T("s43", "Granite as"), T("s43", "Squeeze"), T("s43", "electric charge"), T("s43", "the grains point"), T("s43", "mostly cancel"))
    els = [lab(889, 190, "a crystal generator?", tq, LILAC, 32)]
    # the crystal and the plates
    cx, cy = 470, 610
    els += [gl(cx, 470, 300, -1, .2)] + quartz(cx, cy - 10, 120, 230, tsq - .2, "pop")
    els += [rect(cx - 170, cy - 8, 340, 22, "#6d6f76", "rgba(255,236,206,.5)", 1.2, 4, tsq, fx="rise"),
            rect(cx - 170, cy - 330, 340, 22, "#6d6f76", "rgba(255,236,206,.5)", 1.2, 4, tsq, fx="rise"),
            arr([(cx, cy - 400), (cx, cy - 342)], tsq + .3, AMBER, 3, dur=.3, curve=False), arr([(cx, cy + 78), (cx, cy + 22)], tsq + .3, AMBER, 3, dur=.3, curve=False),
            lab(cx + 82, cy - 150, "quartz", tsq + .4, BONE, 28, "start")]
    for k in range(4):
        mx_ = cx - 120 + k * 80
        els += [lab(mx_, cy - 340, "+", tch, "#ffd27a", 34, st="lab"), ln([(mx_ - 9, cy + 40), (mx_ + 9, cy + 40)], tch + .1, BLUE, 4, draw=False)]
    sx, sy = cx - 250, cy - 160
    els += [ln([(cx - 170, cy - 319), (sx, cy - 319), (sx, sy - 18)], tch + .2, "#c9b48a", 2, dur=.4), ln([(cx - 170, cy + 3), (sx, cy + 3), (sx, sy + 18)], tch + .2, "#c9b48a", 2, dur=.4),
            ln([(sx, sy - 18), (sx + 9, sy - 6), (sx - 7, sy + 4), (sx, sy + 18)], tch + .6, "#ffe9a8", 3, dur=.2), gl(sx, sy, 60, tch + .6, .8, "blue"),
            lab(sx - 20, sy - 50, "a tiny charge", tch + .8, "#ffe9a8", 28, "middle")]
    # the granite: grains every which way
    gx, gy, R_ = 1150, 480, 215
    rnd = random.Random(43)
    disc = [circ(gx, gy, R_, GRAN, "rgba(255,236,206,.5)", 2, 0)]
    grains = []
    tries = 0
    while len(grains) < 16 and tries < 500:
        tries += 1
        a, rr = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, R_ - 34)
        x, y = gx + rr * math.cos(a), gy + rr * math.sin(a)
        if all(math.hypot(x - u, y - v) > 70 for u, v, _ in grains):
            grains.append((x, y, rnd.uniform(0, 2 * math.pi)))
    for x, y, _ in grains:
        disc.append(poly(blob(x, y, 24, 18, 7, .3, int(x)), "rgba(236,240,244,.7)", "rgba(255,255,255,.7)", 1, 0))
    for _ in range(90):
        a, rr = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, R_ - 6)
        disc.append(circ(gx + rr * math.cos(a), gy + rr * math.sin(a), rnd.uniform(1.4, 3), rnd.choice(["#3a2a28", "#f6ece4", "#a0645a"]), at=0))
    els += [grp(disc, -1, None), lab(gx, gy + R_ + 46, "granite", -1, DIM, 28)]
    for k, (x, y, a) in enumerate(grains):
        els.append(arr([(x - 26 * math.cos(a), y - 26 * math.sin(a)), (x + 26 * math.cos(a), y + 26 * math.sin(a))], tw + .07 * k, "#5a2a10", 4.5, dur=.25, curve=False))
    els += [lab(gx, gy - R_ - 22, "every which way", tw + .6, "#ffd27a", 28)]
    # head to tail: the sum wanders and comes back near where it began
    px, py = 1500, 470
    pts = [(px, py)]
    acc_x = acc_y = 0.0
    for _, _, a in grains:
        acc_x += 46 * math.cos(a)
        acc_y += 46 * math.sin(a)
        pts.append((px + acc_x, py + acc_y))
    # nudge the chain so it closes near its start, as random directions mostly cancel
    n = len(pts) - 1
    dx_, dy_ = (pts[-1][0] - px) * .85, (pts[-1][1] - py) * .85
    pts = [(x - dx_ * k / n, y - dy_ * k / n) for k, (x, y) in enumerate(pts)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = 1545 - (min(xs) + max(xs)) / 2, 460 - (min(ys) + max(ys)) / 2
    pts = [(x + ox, y + oy) for x, y in pts]
    els += [ln(pts, tca, "#ffd27a", 3.5, dur=1.2), dot(round(pts[0][0], 1), round(pts[0][1], 1), 8, GREEN, tca), dot(round(pts[-1][0], 1), round(pts[-1][1], 1), 8, "#ff8a7a", tca + 1.1),
            lab(1545, max(ys) + oy + 50, "they mostly cancel", tca + .6, "#ffd27a", 28)]
    els += checks_row(1250, 175 - 0, 1, 1, tca + 1.0)
    return {"base": "dark", "cam": CAM, "els": els}


def s44():
    """The five low rooms over the King's Chamber, cut away (after iso3d.relieving_stack, drawn wide, no names yet): granite beams,
    a limestone gable on top; on 'King's Chamber' its label; on 'five low rooms' they glow one by one; arrows carry the weight round the
    sides; 'entered 1765' by the lowest; on '1837' the top four light up, 'blasted open, 1837'; then 'sealed since built'."""
    import iso3d
    tk, tf, tw, t37, ts = T("s44", "Above the"), T("s44", "five low rooms"), T("s44", "spread the"), T("s44", "eighteen thirty-seven"), T("s44", "sealed since")
    items, top = iso3d.relieving_stack(names=())
    e = iso_el(items, 760, 705, 24.0, -35, .34, 0.0, -1)
    els = [gl(760, 450, 560, -1, .16), e]
    ys = [5.8 + 1.3 + .475 + i * 2.25 for i in range(5)]
    cs = [P3(e, (0, y, 5.0)) for y in ys]
    kx, ky = P3(e, (0, 2.9, 5.0))
    els += [lab(kx + 300, ky + 30, "King's Chamber", tk, BONE, 30, "start"), ln([(kx + 60, ky + 10), (kx + 290, ky + 20)], tk, BONE, 1.5, dur=.4, op=.7)]
    for i, (x, y) in enumerate(cs):
        els.append(gl(x, y, 70, tf + .25 * i, .55))
    els += [lab(cs[0][0] + 330, cs[0][1] + 10, "entered 1765", tf + 1.4, DIM, 26, "start"), ln([(cs[0][0] + 150, cs[0][1]), (cs[0][0] + 320, cs[0][1] + 2)], tf + 1.3, DIM, 1.5, dur=.4, op=.6)]
    gx, gy = P3(e, (0, top + 2.4, 0))
    for side in (-1, 1):
        els.append(arr([(gx + side * 70, gy + 20), (gx + side * 205, gy + 110), (gx + side * 240, ky - 100), (gx + side * 228, ky - 25)], tw + .2 * (side > 0), AMBER, 3.5, dur=1.0))
    for i in range(1, 5):
        x, y = cs[i]
        els += [gl(x, y, 90, t37 + .3 * i, .9, "fire"), ln([(x - 40, y), (x + 40, y)], t37 + .3 * i, "#ffd08a", 4, dur=.3)]
    x1, y1 = cs[1]
    x4, y4 = cs[4]
    els += [ln([(x4 + 310, y4 - 10), (x4 + 330, y4 - 10), (x1 + 330, y1 + 10), (x1 + 310, y1 + 10)], t37 + 1.4, "#ffd08a", 2.5, dur=.6),
            lab(x4 + 350, (y1 + y4) / 2 + 10, "blasted open, 1837", t37 + 1.5, "#ffd08a", 30, "start"),
            lab(x4 + 350, (y1 + y4) / 2 + 58, "sealed since built", ts, BONE, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def khufu_cartouche(x, y, s, at, rot=0, c=OCHRE, fx="pop"):
    """Khufu's name in a cartouche, as the work gangs painted it in red ochre: the oval ring and its tie, and inside, from the top, the
    sieve sign (kh), a quail chick (w), a horned viper (f) and a quail chick (w); (x, y) = its centre, s = its height."""
    k = s / 200.0
    P = lambda pts: [(x + a * k, y + b * k) for a, b in pts]
    els = [rect(x - 46 * k, y - 100 * k, 92 * k, 200 * k, "none", c, 4.5 * k + 1, 46 * k, 0), ln(P([(-40, 112), (40, 112)]), 0, c, 5 * k + 1, draw=False)]
    els += [circ(x, y - 62 * k, 18 * k, "none", c, 3 * k + 1, 0)] + [ln(P([(-12, -66 + 7 * j), (12, -66 + 7 * j)]), 0, c, 2 * k + .8, draw=False) for j in range(2)]
    for yy in (-14, 66):                                                       # the chicks
        els += [poly(P([(-14, yy + 10), (-16, yy - 4), (-6, yy - 12), (6, yy - 14), (12, yy - 6), (16, yy + 8), (4, yy + 14)]), c, at=0, op=.9),
                ln(P([(-2, yy + 14), (-4, yy + 22)]), 0, c, 2.4 * k + .6, draw=False), ln(P([(6, yy + 14), (6, yy + 22)]), 0, c, 2.4 * k + .6, draw=False)]
    els += [ln(P([(-30, 30), (-16, 22), (0, 30), (16, 22), (30, 28)]), 0, c, 4 * k + 1, curve=True, draw=False),       # the viper
            ln(P([(26, 26), (24, 16)]), 0, c, 2.4 * k + .6, draw=False), ln(P([(31, 26), (33, 16)]), 0, c, 2.4 * k + .6, draw=False)]
    return [grp(els, at, fx, tr="rotate(%g %g %g)" % (rot, x, y) if rot else None)]


def s45():
    """Inside the sealed rooms, face-on in lamplight: rough granite and limestone blocks; on 'work gangs' red-ochre builders' marks paint
    themselves on (levelling lines, gang signs; 'work-gang marks, red ochre'); on 'a king's name' red cartouches of Khufu appear one after
    another, some upside down, as on the stones; on 'Khufu' the name in gold."""
    tw, tn, tk = T("s45", "work gangs"), T("s45", "a king's name"), T("s45", "Khufu")
    rnd = random.Random(45)
    blocks = []
    rows = [(140, 330), (330, 540), (540, 770)]
    for r_, (y0, y1) in enumerate(rows):
        x = 90 + rnd.uniform(-60, 0)
        while x < 1690:
            w = rnd.uniform(240, 420)
            tone = "#a8908a" if (r_ + int(x / 300)) % 3 == 0 else "#c7ad86"
            pts = [(x + 4, y0 + rnd.uniform(2, 8)), (x + w - 4, y0 + rnd.uniform(2, 8)), (x + w - rnd.uniform(2, 8), y1 - 4), (x + rnd.uniform(2, 8), y1 - 4)]
            blocks += [poly(pts, tone, "rgba(40,28,20,.6)", 2, 0), poly(pts, "url(#k-speck)", "none", 0, 0)]
            x += w
    blocks += [rect(80, 130, 1620, 650, "rgba(10,8,6,.25)", at=0)]
    els = [{"k": "group", "clip": [80, 130, 1620, 650, 14], "els": blocks, "in": -1}, rect(80, 130, 1620, 650, "none", "rgba(255,236,206,.3)", 2, 14, -1),
           gl(889, 470, 760, -1, .28)]
    marks = [ln([(180, 300), (520, 300)], tw, OCHRE, 4, dur=.4), ln([(330, 290), (330, 312)], tw + .2, OCHRE, 4, dur=.2),
             ln([(1180, 690), (1560, 690)], tw + .3, OCHRE, 4, dur=.4), ln([(1370, 680), (1370, 702)], tw + .5, OCHRE, 4, dur=.2),
             ln([(250, 640), (290, 600), (330, 640)], tw + .4, OCHRE, 4, dur=.3), ln([(1460, 250), (1500, 210), (1540, 250), (1500, 290), (1460, 250)], tw + .6, OCHRE, 4, dur=.4),
             ln([(700, 690), (760, 690), (760, 640)], tw + .5, OCHRE, 4, dur=.3)]
    els += marks + [lab(889, 160, "work-gang marks, red ochre", tw + 1.0, "#ff9a7a", 28)]
    for k, (x, y, s_, rot) in enumerate(((560, 450, 210, 0), (930, 360, 170, 180), (1240, 470, 200, 0), (420, 650, 130, 90), (1080, 640, 130, -90))):
        els += khufu_cartouche(x, y, s_, tn + .35 * k, rot)
    els += [gl(930, 360, 160, tk, .55), lab(930, 238, "Khufu", tk, GOLD, 48, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def s46():
    """A papyrus sheet rises (columns of hieratic, a red heading), 'Merer's logbook, found 2013'; beside it a schematic map: the Nile, the
    Tura quarries on the east bank, Giza and its pyramid on the west; on 'shipping limestone' a boat with a white block crosses; on
    'Horizon of Khufu', the pyramid glows and its name appears. The third box ticks."""
    tl, tm, tsh, th = T("s46", "A logbook"), T("s46", "named Merer"), T("s46", "shipping limestone"), T("s46", "the Horizon")
    els = [gl(450, 450, 460, -1, .22)]
    px0, py0, pw, ph = 150, 230, 600, 440
    sheet = [rect(px0, py0, pw, ph, "#e6d3a8", "rgba(110,80,40,.6)", 1.5, 4, 0), rect(px0, py0, pw, ph, "url(#k-speck)", at=0)]
    for j in range(1, 6):
        sheet.append(ln([(px0 + j * pw / 6, py0 + 70), (px0 + j * pw / 6, py0 + ph - 20)], 0, "rgba(110,80,40,.35)", 1.5, draw=False))
    sheet += [{"k": "glyphs", "x": px0 + 30, "y": py0 + 24, "w": pw - 60, "h": 40, "rows": 1, "cols": 9, "kind": "hieratic", "c": "#b0301e", "seed": 3, "in": 0},
              {"k": "glyphs", "x": px0 + 20, "y": py0 + 84, "w": pw - 40, "h": ph - 110, "rows": 9, "cols": 12, "kind": "hieratic", "c": "#2a1d10", "seed": 7, "in": 0}]
    els += [grp(sheet, .3, "rise"), lab(px0 + pw / 2, py0 - 26, "Merer's logbook, found 2013", tl + .2, GOLD, 30)]
    # the map: north up; the Nile between Giza (west) and the Tura quarries (east)
    mx0, my0, mw, mh = 900, 200, 760, 520
    river = [(1300, my0), (1285, 300), (1310, 400), (1290, 500), (1305, 600), (1295, my0 + mh)]
    els += [rect(mx0, my0, mw, mh, "#3a2f24", "rgba(255,236,206,.35)", 2, 14, -1),
            ln(river, -1, "#3f86a8", 26, curve=True, draw=False), ln(river, -1, "#8fc4dc", 3, curve=True, draw=False, op=.6),
            lab(1330, 290, "Nile", -1, "#9fd0ff", 26, "start", st="ital")]
    gxm, gym = 1060, 430
    els += [{"k": "pyramid", "x": gxm, "y": gym + 40, "w": 110, "in": -1}, lab(gxm, gym + 92, "Giza", -1, BONE, 30)]
    tx, ty = 1520, 560
    els += [poly([(tx - 70, ty + 30), (tx - 50, ty - 20), (tx + 50, ty - 30), (tx + 80, ty + 30)], "#a8916c", "rgba(255,236,206,.4)", 1.2, -1),
            rect(tx - 30, ty - 6, 26, 18, LIME_L, at=-1), rect(tx + 8, ty - 12, 30, 22, LIME_L, at=-1), lab(tx, ty + 72, "Tura quarries", -1, BONE, 28)]
    route = [(tx - 70, ty + 4), (1400, 520), (1300, 490), (1180, 460), (gxm + 70, gym + 20)]
    els += [ln(route, tsh, AMBER, 3, "inferred", dur=1.6, curve=True)]
    bx, by = 1300, 490
    els += [grp([poly([(bx - 40, by - 4), (bx + 40, by - 4), (bx + 30, by + 12), (bx - 30, by + 12)], "#8a6a44", "#e7c99a", 1.2, 0),
                 rect(bx - 16, by - 22, 32, 18, LIME_L, "rgba(90,70,50,.6)", 1, 2, 0)], tsh + .6, "pop")]
    els += [gl(gxm, gym, 120, th, .8), lab(gxm, my0 + 44, "the Horizon of Khufu", th + .2, GOLD, 30, st="serif")]
    els += checks_row(210, 740, 2, 2, th + 1.0, gap=150)
    return {"base": "dark", "cam": CAM, "els": els}


def s47_add():
    """A king's tomb: the pyramid is drawn again over Dunn's machine (it fades out under it), the sky closes over the beam and the lilac
    notes; a warm lamp glows in the King's Chamber, 'a king's tomb'; the three checks, all ticked, at the left."""
    els = []
    g = gp_shafts()
    ex, ey = g["ks"][-1]
    ux, uy = (BEAM_END[0] - ex) / math.hypot(BEAM_END[0] - ex, BEAM_END[1] - ey), (BEAM_END[1] - ey) / math.hypot(BEAM_END[0] - ex, BEAM_END[1] - ey)
    els += [sky_veil(band((ex - 6 * ux, ey - 6 * uy), (BEAM_END[0] + 26 * ux, BEAM_END[1] + 26 * uy), 22), 1.2, 1.4),
            sky_veil([(LBL_BEAM[0] - 14, LBL_BEAM[1] - 34), (LBL_BEAM[0] + 270, LBL_BEAM[1] - 34), (LBL_BEAM[0] + 270, LBL_BEAM[1] + 14),
                      (LBL_BEAM[0] - 14, LBL_BEAM[1] + 14)], 1.2, 1.4),
            sky_veil([(LBL_ENGINE[0] - 200, LBL_ENGINE[1] - 36), (LBL_ENGINE[0] + 200, LBL_ENGINE[1] - 36), (LBL_ENGINE[0] + 200, LBL_ENGINE[1] + 14),
                      (LBL_ENGINE[0] - 200, LBL_ENGINE[1] + 14)], 1.2, 1.4)]
    els += [gp_body(1.2, "fade", 1.4)]
    els += [gl(KCX, KCY, 150, 2.2, .9, "fire"), lab(QCX, 742, "Queen's Chamber", 1.2, BONE, 26, fx="fade"),
            lab(KCX, 470, "a king's tomb", 2.4, GOLD, 36, st="serif")]
    for k, (name, kind) in enumerate(CHK):
        y = 470 + k * 90
        els += [icon(kind, 200, y, 1.0, -1), checkbox(270, y, -1, 40)] + static([tick(270, y, 0, GREEN, 1.0, 5)])
    return els


# ================================================================== CHAPTER 6 · The weighing
def ledger(title, at, y0=150, y1=720):
    return [rect(110, y0, 1560, y1 - y0, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, at), lab(140, y0 + 38, title, at + .2, GOLD, 26, "start", st="cap")]


def lrow(y, at, pic, text, grade=None, gt=None, gc=None, h=96):
    out = [rect(140, y - h / 2, 1500, h, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1230, y, grade, gc, gt, 28, "start")
    return out


def pic_bowdrill(x, y, at):
    return [grp([ln([(x - 2, y + 30), (x - 2, y - 30)], 0, "#c9b48a", 4, draw=False), poly(E(x - 2, y - 33, 12, 5, 12), "#8a7a5a", at=0),
                 ln([(x - 40, y - 4), (x - 2, y - 12), (x + 38, y - 2)], 0, "#c9b48a", 3.5, curve=True, draw=False), rect(x - 24, y + 22, 48, 12, GRAN, at=0)], at, "pop")]


def pic_vase(x, y, at):
    return [vicon(x, y + 28, LILAC, at, 1.2)]


def pic_core(x, y, at):
    return [grp(core(x, y + 32, 34, 64, gold=True, n=5), at, "pop")]


def pic_q(x, y, at):
    return [lab(x, y + 20, "?", at, "#f0b06a", 52, st="big", fx="pop")]


def pic_box(x, y, at, cart=True):
    els = stone_box(x - 34, y + 26, 52, 36, 30, at=0, lid=10, seed=3, grains=12)
    if cart:
        els += [rect(x - 22, y, 28, 14, "none", GOLD, 1.8, 7, 0)]
    return [grp(els, at, "pop")]


def pic_box_old(x, y, at):
    return [grp(stone_box(x - 30, y + 26, 52, 36, 30, at=0, lid=10, seed=3, grains=12) +
                [arr([(x + 28, y - 30), (x - 6, y - 36), (x - 40, y - 30)], 0, LILAC, 2.5, "claimed", dur=.3)], at, "pop")]


def pic_pyr(x, y, at):
    return [grp([poly([(x - 40, y + 28), (x, y - 22), (x + 40, y + 28)], "rgba(242,220,180,.2)", "#f2dcb4", 2, 0),
                 ln([(x + 4, y + 2), (x + 44, y - 30)], 0, LILAC, 3, "claimed", draw=False)], at, "pop")]


def s48():
    """The ledger, panel one (how the stone was worked): row 1, 'copper, sand, borers and time' (a bow drill), its chip 'Strong evidence'
    as it is said; under it the four witnesses tick one by one: the tools, the cores, the art, the experiments."""
    tq, tg, tt, tc, ta, te = (T("s48", "Egypt's craftsmen"), T("s48", "Strong evidence"), T("s48", "the tools"), T("s48", "the cores"),
                              T("s48", "the art"), T("s48", "the experiments"))
    els = ledger("How the stone was worked", .2)
    els += [rect(140, yy - 48, 1500, 96, "none", "rgba(242,201,142,.22)", 1.5, 12, .4, style="inferred", fx="pop") for yy in (415, 530, 645)]
    y = 262
    els += [rect(140, y - 58, 1500, 150, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, tq, fx="pop"),
            lab(300, y + 2, "copper, sand, borers and time", tq + .1, BONE, 30, "start")] + pic_bowdrill(215, y + 6, tq + .1)
    els += chip(1230, y - 6, "Strong evidence", GRADE["strong"], tg, 28, "start")
    wit = [("the tools", tt), ("the cores", tc), ("the art", ta), ("the experiments", te)]
    for k, (name, t) in enumerate(wit):
        x = 330 + k * 250
        els += [tick(x, y + 58, t, GREEN, .8, 4), lab(x + 24, y + 66, name, t + .1, DIM, 24, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s49_add():
    """Rows 2 to 4 of the same ledger: machine-made vases (Awaiting evidence); core 7's groove as a machine's track (Awaiting evidence);
    exactly how it was cut (Open question)."""
    t1, g1, t2, g2, t3, g3 = (T("s49", "Machine-made vases"), T("s49", "Awaiting evidence"), T("s49", "Core seven's"), T("s49", "Awaiting evidence", k=2),
                              T("s49", "Exactly how"), T("s49", "open question"))
    els = lrow(415, t1, pic_vase, "machine-made vases", "Awaiting evidence", g1, GRADE["awaiting"])
    els += lrow(530, t2, pic_core, "core 7's groove, a machine's track", "Awaiting evidence", g2, GRADE["awaiting"])
    els += lrow(645, t3, pic_q, "exactly how it was cut", "Open question", g3, GRADE["open"])
    return els


def s50():
    """The ledger, panel two (the boxes and the pyramid): the boxes made for the Apis burials, Strong evidence; older than the bulls,
    Awaiting evidence; a power plant at Giza, Ruled out, a red strike across its picture."""
    t1, g1, t2, g2, t3, g3 = (T("s50", "The Serapeum boxes"), T("s50", "Strong evidence"), T("s50", "Older than"), T("s50", "Awaiting evidence"),
                              T("s50", "A power plant"), T("s50", "Ruled out"))
    els = ledger("The boxes and the pyramid", .2, 170, 640)
    els += [rect(140, yy - 48, 1500, 96, "none", "rgba(242,201,142,.22)", 1.5, 12, .4, style="inferred", fx="pop") for yy in (400, 530)]
    els += lrow(270, t1, pic_box, "boxes made for the Apis burials", "Strong evidence", g1, GRADE["strong"])
    els += lrow(400, t2, pic_box_old, "older than the bulls", "Awaiting evidence", g2, GRADE["awaiting"])
    els += lrow(530, t3, pic_pyr, "a power plant at Giza", "Ruled out", g3, GRADE["ruled"])
    els += [strike(170, 555, 262, 505, g3 + .2, RED, 5)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def gear(x, y, r, n=10, at=0, c=LILAC, style="claimed", fx="pop", fill="rgba(201,193,238,.06)"):
    pts = []
    for k in range(n * 4):
        a = 2 * math.pi * k / (n * 4)
        rr = r if (k % 4) in (0, 1) else r * .78
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return [poly(pts, fill, c, 2.5, at, style=style, fx=fx), circ(x, y, r * .3, "none", c, 2.5, at, style=style, fx=fx)]


def s51():
    """The whole picture: 'a lost high technology?' and, as it is said, the chip 'Awaiting evidence'; three empty dotted outlines pop as
    named (a machine, a machine part, a dated machine-made object); then, on 'people', craftsmen in warm silhouette rise along the bottom,
    a vessel driller, two men at a bow drill, a polisher, with a heap of sand and an hourglass."""
    tq, tg, tm, tp, to, tpe, tsa, tti = (T("s51", "And a lost"), T("s51", "Awaiting evidence"), T("s51", "No machine"), T("s51", "no part"),
                                         T("s51", "no machine-made object"), T("s51", "is people"), T("s51", "skill, sand"), T("s51", "great deal"))
    els = [lab(889, 196, "a lost high technology?", tq, LILAC, 34, st="serif")]
    els += chip(889, 262, "Awaiting evidence", GRADE["awaiting"], tg, 32)
    xs = (420, 889, 1358)
    els += gear(xs[0], 400, 62, 10, tm)
    els += [lab(xs[0], 505, "no machine", tm + .2, LILAC, 28)]
    els += [poly([(xs[1] - 70, 380), (xs[1] + 40, 380), (xs[1] + 70, 400), (xs[1] + 40, 420), (xs[1] - 70, 420)], "rgba(201,193,238,.06)", LILAC, 2.5, tp, style="claimed", fx="pop"),
            circ(xs[1] - 70, 400, 34, "rgba(201,193,238,.06)", LILAC, 2.5, tp, style="claimed", fx="pop"),
            lab(xs[1], 505, "no machine part", tp + .2, LILAC, 28)]
    vo = jar_outline(xs[2], 455, 70)
    els += [poly(vo, "rgba(201,193,238,.06)", LILAC, 2.5, to, style="claimed", fx="pop", curve=True),
            rect(xs[2] + 70, 360, 110, 34, "none", LILAC, 2, 17, to + .2, style="claimed", fx="pop"), lab(xs[2] + 125, 384, "dated?", to + .2, LILAC, 22),
            lab(xs[2], 505, "no dated machine-made object", to + .3, LILAC, 28)]
    # the people: waiting in the dark from the start, lit on 'people'
    gy = 770

    def people(at, lit):
        c, rim = ("#3a2618", "rgba(255,214,170,.55)") if lit else ("#1c140e", "rgba(255,214,170,.12)")
        fx = "rise" if lit else None
        jx_, jtop = 470, gy - 92
        drill = [vessel(jx_, gy, 92, JAR, DIOR if lit else "#241c18", None, 0, None, w=56)[0],
                 ln([(jx_, jtop + 4), (jx_, jtop - 96)], 0, "#3a2414", 5, draw=False), ln([(jx_, jtop - 96), (jx_ - 6, jtop - 108), (jx_ - 28, jtop - 110), (jx_ - 36, jtop - 100)], 0, "#3a2414", 4, curve=True, draw=False),
                 poly(E(jx_ - 18, jtop - 58, 10, 13, 14), "#4a3a2c", rim, 1, 0), poly(E(jx_ + 18, jtop - 58, 10, 13, 14), "#4a3a2c", rim, 1, 0)]
        out = [grp(drill, at, fx)] + driller_sil(300, gy, 280, (jx_ - 36, jtop - 100), (jx_ - 3, jtop - 40), at, c=c, rim=rim)
        out += fig(760, gy, 190, at + (.3 if lit else 0), c, "pull", 1, fx=fx) + fig(940, gy, 186, at + (.4 if lit else 0), c, "press", -1, fx=fx)
        out += [rect(800, gy - 70, 110, 70, GRAN if lit else "#2a1e1a", rim, 1, 2, at + (.35 if lit else 0), fx=fx),
                ln([(850, gy - 70), (850, gy - 150)], at + (.45 if lit else 0), "#c9b48a" if lit else "#2a2018", 4, draw=False),
                ln([(782, gy - 118), (850, gy - 124), (920, gy - 116)], at + (.45 if lit else 0), "#c9b48a" if lit else "#2a2018", 3, curve=True, draw=False)]
        out += seated(1180, gy, 230, at + (.6 if lit else 0), c, 1, fx, arms="hold") + vessel(1330, gy, 80, JAR, DIOR if lit else "#241c18", None, at + (.6 if lit else 0), fx, w=50)
        if not lit:
            for e in out:
                if e.get("k") == "group":
                    gdim(e, .55)
                else:
                    e["op"] = round((e["op"] if e.get("op") is not None else 1.0) * .55, 3)
        return out

    els += people(-1, False) + [gl(889, 700, 700, tpe, .3)] + people(tpe + .1, True)
    els += [poly([(1400, gy), (1460, gy - 46), (1530, gy)], "#d8c08e", "rgba(90,60,30,.5)", 1, tsa + .4, curve=True, fx="rise")]
    hx, hy = 1600, gy - 70
    els += [grp([poly([(hx - 30, hy - 60), (hx + 30, hy - 60), (hx + 4, hy), (hx + 30, hy + 60), (hx - 30, hy + 60), (hx - 4, hy)], "rgba(255,236,206,.08)", BONE, 2, 0),
                 poly([(hx - 22, hy + 56), (hx + 22, hy + 56), (hx, hy + 30)], "#d8c08e", at=0), poly([(hx - 12, hy - 40), (hx + 12, hy - 40), (hx, hy - 10)], "#d8c08e", at=0),
                 ln([(hx - 38, hy - 64), (hx + 38, hy - 64)], 0, "#8a6a44", 5, draw=False), ln([(hx - 38, hy + 64), (hx + 38, hy + 64)], 0, "#8a6a44", 5, draw=False)], tti, "pop")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s52():
    """What would change our minds: four wanted things in lilac dashes, as named: a vase in a sealed, dated tomb whose scan dot sits in the
    machine cluster; core 7 beside a copper-and-sand test core under a scanner; a box inside a scan grid; a gear on a workshop bench."""
    t0, t1, t2, t3, t4 = T("s52", "What would"), T("s52", "A vase from"), T("s52", "Core seven"), T("s52", "A full scan"), T("s52", "Or a single")
    els = [lab(889, 190, "what would change our minds", t0, GOLD, 30, st="cap")]
    xs = (300, 690, 1090, 1480)
    I_ = "inferred"
    # 1 a vase in a sealed, dated tomb, its scan in the machine cluster
    x = xs[0]
    els += [rect(x - 150, 330, 300, 260, "rgba(201,193,238,.05)", LILAC, 2.5, 8, t1, style=I_, fx="pop"),
            poly(jar_outline(x - 40, 550, 62), "rgba(201,193,238,.08)", LILAC, 2.5, t1 + .3, style=I_, fx="pop", curve=True),
            rect(x - 150, 330, 300, 24, "rgba(201,193,238,.15)", LILAC, 2, 4, t1 + .5, style=I_, fx="pop")]
    els += chip(x + 80, 390, "dated", LILAC, t1 + .7, 22) + [dot(x + 80, 500, 12, BLUE, t1 + 2.6), circ(x + 80, 500, 28, "none", BLUE, 2, t1 + 2.6, style=I_, fx="pop")]
    els += [lab(x, 655, "a lathe-true vase, dated", t1 + .8, LILAC, 26)]
    # 2 core 7 beside a test core, under a scanner
    x = xs[1]
    els += [grp(core(x - 50, 590, 60, 150, gold=True, n=6), t2, "pop"), grp(core(x + 50, 590, 56, 130, n=5), t2 + .4, "pop"),
            rect(x - 70, 330, 140, 40, "rgba(201,193,238,.06)", LILAC, 2.5, 8, t2 + .6, style=I_, fx="pop")]
    els += [poly([(x - 40, 370), (x + 40, 370), (x + 110, 590), (x - 110, 590)], "rgba(159,208,255,.10)", BLUE, 1.5, t2 + .8, style=I_, fx="pop")]
    els += [lab(x, 655, "core 7 beside a test core", t2 + .9, LILAC, 26)]
    # 3 a box in a scan grid
    x = xs[2]
    els += stone_box(x - 120, 570, 190, 120, 110, t3, lid=40, seed=9, grains=30, fx="pop")
    for j in range(7):
        els.append(ln([(x - 150 + j * 50, 360), (x - 150 + j * 50, 600)], t3 + .4 + .05 * j, BLUE, 1.5, I_, dur=.4, op=.7))
    for j in range(5):
        els.append(ln([(x - 150, 360 + j * 60), (x + 150, 360 + j * 60)], t3 + .7 + .05 * j, BLUE, 1.5, I_, dur=.4, op=.7))
    els += [lab(x, 655, "all 24 boxes scanned", t3 + .9, LILAC, 26)]
    # 4 a machine part on an ancient bench
    x = xs[3]
    els += [rect(x - 140, 550, 280, 18, "rgba(201,193,238,.06)", LILAC, 2.5, 4, t4, style=I_, fx="pop")]
    els += gear(x, 470, 70, 12, t4 + .3, LILAC, I_)
    els += [lab(x, 655, "one machine part, dated", t4 + .6, LILAC, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def driller_sil(x, y, h, hand1, hand2, at=-1, c="#24170f", rim="rgba(255,214,170,.5)"):
    """A craftsman seated on a low stool in profile, facing right, leaning in to his work (h = his standing height; x, y = the foot of the
    stool): a smooth silhouette with a thin lit rim; his hands on hand1 (the crank) and hand2 (the shaft)."""
    P = lambda a, b: (x + a * h, y - b * h)
    sh = P(.13, .6)                                                     # the shoulder
    els = [poly([P(-.1, .2), P(.09, .2), P(.08, 0), P(-.09, 0)], c, rim, 1.2, 0),                                         # the stool
           poly([P(-.07, .24), P(-.06, .4), P(0, .55), P(.09, .64), P(.17, .64), P(.2, .56), P(.12, .42), P(.1, .26), P(.03, .2)], c, rim, 1.5, 0, curve=True),   # torso
           poly([P(-.04, .19), P(.27, .3), P(.31, .26), P(.03, .17)], c, rim, 1.2, 0, curve=True)]                         # thigh
    els += [ln([P(.29, .28), P(.33, .03)], 0, rim, .068 * h + 3, draw=False), ln([P(.29, .28), P(.33, .03)], 0, c, .068 * h, draw=False),   # shin
            poly([P(.3, .03), P(.41, .02), P(.41, 0), P(.3, 0)], c, rim, 1, 0)]                                           # foot
    hx, hy = P(.17, .72)
    els += [circ(hx, hy, .072 * h, c, rim, 1.4, 0),                                                                         # head
            poly([P(.1, .79), P(.2, .8), P(.24, .74), P(.2, .7), P(.13, .66), P(.09, .7)], mix(c, "#000000", .3), rim, 1, 0, curve=True)]   # wig
    for hand in (hand1, hand2):
        dx, dy = hand[0] - sh[0], hand[1] - sh[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        if ny < 0:
            nx, ny = -nx, -ny
        ex, ey = (sh[0] + hand[0]) / 2 + nx * .07 * h, (sh[1] + hand[1]) / 2 + ny * .07 * h          # the elbow, bent down
        els += [ln([sh, (ex, ey), hand], 0, rim, .05 * h + 3, draw=False), ln([sh, (ex, ey), hand], 0, c, .05 * h, draw=False),
                circ(hand[0], hand[1], .03 * h, c, at=0)]
    return [grp(els, at, None if at < 0 else "rise")]


def s53():
    """The close: the hero jar again, turning in its beam, and beside it, in warm silhouette, a craftsman on his stool turning the drill
    weighted with two stones, its borer in the jar's mouth; on 'turned', a curved arrow round the crank; on 'came true', the jar's rim
    catches the light."""
    tt, tc = T("s53", "turned a"), T("s53", "came true")
    s_ = 135
    jx, jy = 1010, 700
    top = jy - JAR[-1][0] * s_
    els = beam(jx, 112, jy, 46, 240, -1) + motes(jx - 210, jx + 210, 150, jy - 20, 34, -1, seed=11)
    els += jar_iso(jx, jy, s_, -1, spin=6.0, seed=7, n=560)
    # the drill: a shaft into the mouth, a cranked top, two stones lashed under the crank
    sx0, sy0, sy1 = jx, top + 4, top - 190
    crank = [(sx0, sy1), (sx0 - 10, sy1 - 22), (sx0 - 48, sy1 - 26), (sx0 - 62, sy1 - 6)]
    els += [ln([(sx0, sy0), (sx0, sy1)], -1, "#3a2414", 8, draw=False), ln(crank, -1, "#3a2414", 7, curve=True, draw=False),
            ln([(sx0, sy1 + 30), (sx0 - 30, sy1 + 52)], -1, "#2a1a10", 2.5, draw=False), ln([(sx0, sy1 + 30), (sx0 + 30, sy1 + 52)], -1, "#2a1a10", 2.5, draw=False),
            poly(E(sx0 - 34, sy1 + 70, 20, 25, 18), "#4a3a2c", "rgba(255,214,170,.45)", 1.2, -1),
            poly(E(sx0 + 34, sy1 + 70, 20, 25, 18), "#4a3a2c", "rgba(255,214,170,.45)", 1.2, -1)]
    els += driller_sil(670, jy, 560, crank[-1], (sx0 - 4, sy1 + 118), -1)
    els += [arr([(sx0 - 110, sy1 - 40), (sx0 - 30, sy1 - 70), (sx0 + 50, sy1 - 44)], tt, "#e8b87a", 2.5, dur=.6),
            poly([(jx + 170, jy), (jx + 225, jy - 32), (jx + 300, jy)], "#d8c08e", "rgba(90,60,30,.4)", 1, -1, curve=True)]
    els += [ln(ring_y(jx, jy, s_, JAR[-1][0], JAR[-1][1]), tc, "#ffe9b8", 3, dur=.8, op=.9), gl(jx, top, 150, tc, .6)]
    return {"base": "dark", "cam": CAM, "els": els}


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
    (0, 0, "hook", "s1", [(1, "Scanned in three", "s2"), (2, "Nearby, a granite", "s3"), (3, "Did ancient Egypt", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "Most are soft", "s7")], {"chapter": "The impossible vases"}),
    (1, 1, "collision", "s8", [(1, "Some vases, they", "s9")], {}),
    (1, 2, "cost", "s10", [], {}),
    (1, 3, "reversal", "s11", [(1, "The machine-made vases", "s12")], {}),
    (1, 4, "tag", "s13", [], {}),
    (2, 0, "world", "s14", [], {"chapter": "A spiral in granite"}),
    (2, 1, "collision", "s15", [(1, "Around the core", "s16")], {}),
    (2, 2, "cost", "s17", [(1, "In {1984", "s18")], {}),
    (3, 0, "world", "s19", [(1, "Geologists rank", "s20"), (1, "So the copper", "s21")], {"chapter": "Copper, sand and patience"}),
    (3, 1, "collision", "s22", [(1, "Slow:", "s23")], {}),
    (3, 2, "reversal", "s24", [(1, "And a copper drill", "s25")], {}),
    (3, 3, "tag", "s26", [], {}),
    (4, 0, "world", "s27", [(0, "In {1850", "s28"), (1, "One giant", "s29"), (1, "This was the", "s30")], {"chapter": "Boxes in the dark"}),
    (4, 1, "collision", "s31", [(1, "Machined, he", "s32")], {}),
    (4, 2, "cost", "s33", [(1, "Hundreds of inscribed", "s34")], {}),
    (4, 3, "reversal", "s35", [(1, "And flat stone", "s36"), (1, "The granite came", "s37")], {}),
    (4, 4, "tag", "s38", [], {}),
    (5, 0, "world", "s39", [(1, "Chemicals fed", "s40")], {"chapter": "A power plant?"}),
    (5, 1, "collision", "s41", [(1, "In {2026", "s42")], {}),
    (5, 2, "cost", "s43", [], {}),
    (5, 3, "reversal", "s44", [(1, "Inside, work gangs", "s45"), (2, "A logbook found", "s46")], {}),
    (5, 4, "tag", "s47", [], {}),
    (6, 0, "weigh", "s48", [(1, "Machine-made vases", "s49"), (2, "The Serapeum boxes", "s50"), (3, "And a lost high", "s51")], {"chapter": "The weighing"}),
    (6, 1, "test", "s52", [], {}),
    (6, 2, "close", "s53", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.16, 1010, 520], "s2_add"),
    "s4": ("s1", [1, 889, 500], "s4_add"),
    "s38": ("s27", [1, 889, 500], "s38_add"),
    "s40": ("s39", [1.2, 960, 520], "s40_add"),
    "s47": ("s39", [1, 889, 500], "s47_add"),
    "s49": ("s48", [1, 889, 500], "s49_add"),
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
    ep = {"id": "lf-egypt-tech", "code": "LF.31", "series": script["series"], "title": script["title"], "case": "egypt-tech",
          "verdict": "unsupported", "claim": "Did ancient Egypt have a lost high technology?", "mood": "mystery",
          "hook_text": "Did Egypt have lost *machines*?", "beats": beats, "shots": shots,
          "sources": "Fomitchev-Zamilov 2025 (doi:10.1038/s40494-025-02196-7) · Petrie 1883, The Pyramids and Temples of Gizeh · "
                     "Stocks 2001 (doi:10.1017/S0003598X00052777) · Stocks 2023 (doi:10.4324/9781003269922) · "
                     "Odler & Kmošek 2025 (doi:10.1553/AEundL35s289) · Mariette 1882, Le Sérapéum de Memphis · Dodson 2005, Divine Creatures · "
                     "Sessa et al. 2026 (doi:10.1038/s41598-026-48805-8) · Vyse 1840-42 · Tallet & Lehner 2021, The Red Sea Scrolls",
          "post": "Egypt's impossible vases, Petrie's granite drill core, the Serapeum's giant boxes and the Giza power plant: the 2025 scan of "
                  "museum vases, copper and sand at Aswan, the weighted drill of the tomb reliefs, the kings' names on the boxes, the 2026 salt "
                  "study and Khufu's name in sealed chambers, weighed.",
          "hashtags": ["#AncientEgypt", "#StoneVases", "#Serapeum", "#GreatPyramid", "#Archaeology", "#WeighItYourself"],
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
