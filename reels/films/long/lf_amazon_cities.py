"""LF.29 · Myths That Came True · The Amazon's Lost Cities: From Legend to Lidar (16:9 long film, one wall).

The script is films/long/lf-amazon-cities/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s53; s5, the title, is the intro card over the panel
of s4), drawn while it is said: the Upano valley seen from the air, its forest stripped away by lidar strip by strip to show the
platforms and straight roads (the hero), the 2015 survey as a plan, the seekers and the doubters, the golden one on a mountain lake and
the Muisca raft, Orellana's route down the river, Carvajal's crowded banks and the same banks emptied, Fawcett the surveyor, his last
letter and the route that stops, an Upper Xingu town in plan and in reconstruction, stone against earth, the rainforest's poor soil,
wealth in the trees, slash and burn, the ceiling, terra preta and what is in it, the Kuikuro making dark earth, the 227 kinds of tree,
the Llanos de Mojos, lidar in side view, Cotoca and Landivar to scale, the 22 m cone, causeways in the flood, 230 Olympic pools, the
ten-thousand-year timeline, Rostain's trench, a platform cluster, the straight road over the hills, the lake core, the sudden end
against the slow decline, the geoglyphs of Acre, the 2026 flight lines, 24,000 earthworks and the people, the ledger, the endings, gold
and stone against earth, the tests, and the canopy at dusk. Drawings are schematic and true to the numbers said: solid = measured,
dashed = inferred, dotted = claimed (El Dorado's golden city and Fawcett's stone Z are lilac and dotted throughout).

Facts: the Short 'amazon-cities' (f11.py, rewrite/amazon-cities.json) and the script's facts_added (Carvajal 1542; Hemming 1978; Fawcett
1953; Heckenberger et al. 2003, 2008; Meggers 1954, 1971; Glaser et al. 2001; Schmidt et al. 2023; ter Steege et al. 2013; Levis et al.
2017; Prumers et al. 2022; Lombardo et al. 2020; Rostain et al. 2024; Bush et al. 2025; Watling et al. 2017; Parssinen et al. 2026;
Peripato et al. 2023; McMichael et al. 2012; Denevan 1996, 2003; Clement et al. 2015; Koch et al. 2019).

Engine workaround (as in lf_troy.py and lf_antikythera.py): the wall only adds elements to a panel on its first visit, at a beat start
or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag,
invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that
step's clock). Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25 syllables a
second). The hero's reveal: the forest is drawn once; the bare earth is drawn over it in vertical strips (clipped groups) that appear
left to right, each carrying the glowing scan front at its right edge, which the next strip covers.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-amazon-cities/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-amazon-cities/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-amazon-cities RC_FILMS_EPS=/tmp/claude-0/sbx_lf-amazon-cities/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-amazon-cities/boards python3 films.py long.lf_amazon_cities
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-amazon-cities", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
LEAF_DD, LEAF_D, LEAF, LEAF_L, LEAF_H = "#13261a", "#1f3a26", "#2f5a34", "#4f8a50", "#86b86e"
EARTH, EARTH_L, EARTH_D, CLAY = "#a88a5e", "#d9bf8f", "#6e5536", "#b0663a"
TP, TP_L, PALE, OXI = "#1c1410", "#3a2a20", "#d8c08c", "#c98a4a"
LID, LID_D, LID_DD, SCANC = "#c9c1b0", "#9c9383", "#6d665b", "#9fd0ff"
RIVER, WATER_L, FLOOD = "#3f86a8", "#6fb3d0", "#4f93b3"
THATCH, THATCH_D, THATCH_L = "#c9a35a", "#8a6a34", "#e2c27e"
SKIN, WOOD, WOOD_D = "#e8d6b8", "#6b4a30", "#3a281a"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#c9e48f", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
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


def grp(els, at, fx="pop", tr=None, clip=None, **kw):
    """A group that builds in as one piece (its children have no build-ins of their own); tr = an SVG transform; clip = [x, y, w, h]."""
    inner = {"k": "group", "els": els}
    if clip:
        inner["clip"] = [round(v, 1) for v in clip]
    if tr:
        inner["tr"] = tr
    e = {"k": "group", "els": [inner], "in": round(at, 2)}
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


def chip(x, y, t, c, at, size=28, a="middle"):
    """A pill with a coloured rim and its words (grades, dates)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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


def blob(cx, cy, rx, ry, n=22, jit=.18, seed=1, rot_=0):
    """An irregular closed outline (a crown, a lump, a heap)."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + rot_
        f = 1 + r.uniform(-jit, jit)
        out.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return out


def fig(x, y, h, at, c="#1a1410", arms=None, face=1, fx="rise", hat=False, coat=False, helmet=False):
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up', 'hold' (both forward), 'lift' (both up), 'spread'."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    els = [circ(X(.01), Y(.9), .085 * h, c),
           poly([(X(-.13), Y(.78)), (X(.13), Y(.78)), (X(.11), Y(.44)), (X(-.11), Y(.44))], c),
           poly([(X(-.11), Y(.46)), (X(.11), Y(.46)), (X(.085), Y(0)), (X(.025), Y(0)), (X(0), Y(.3)), (X(-.025), Y(0)), (X(-.085), Y(0))], c)]
    if coat:
        els.append(poly([(X(-.13), Y(.76)), (X(.13), Y(.76)), (X(.16), Y(.3)), (X(-.16), Y(.3))], c))
    if hat:          # a wide-brimmed hat
        els += [poly([(X(-.08), Y(.94)), (X(.08), Y(.94)), (X(.06), Y(1.04)), (X(-.06), Y(1.04))], c), poly([(X(-.17), Y(.94)), (X(.17), Y(.94)), (X(.15), Y(.965)), (X(-.15), Y(.965))], c)]
    if helmet:       # a crested sixteenth-century helmet (morion)
        els += [poly([(X(-.13), Y(.93)), (X(.13), Y(.93)), (X(.08), Y(1.02)), (X(0), Y(1.06)), (X(-.08), Y(1.02))], c, curve=True),
                poly([(X(-.04), Y(1.0)), (X(.04), Y(1.0)), (X(.02), Y(1.12)), (X(-.02), Y(1.12))], c)]
    aw = max(2.5, .045 * h)
    arm = {None: [[(X(-.12), Y(.76)), (X(-.15), Y(.46))], [(X(.12), Y(.76)), (X(.15), Y(.46))]],
           "point": [[(X(-.12), Y(.76)), (X(-.15), Y(.46))], [(X(.1), Y(.75)), (X(.42), Y(.8))]],
           "up": [[(X(-.12), Y(.76)), (X(-.15), Y(.46))], [(X(.1), Y(.76)), (X(.2), Y(1.08))]],
           "hold": [[(X(-.1), Y(.75)), (X(.22), Y(.56))], [(X(.1), Y(.75)), (X(.28), Y(.6))]],
           "lift": [[(X(-.1), Y(.76)), (X(-.2), Y(1.06))], [(X(.1), Y(.76)), (X(.2), Y(1.06))]],
           "spread": [[(X(-.1), Y(.75)), (X(-.3), Y(.55))], [(X(.1), Y(.75)), (X(.34), Y(.62))]]}[arms]
    els += [ln(a_, 0, c, aw, draw=False) for a_ in arm]
    return [grp(els, at, fx)]


def lamp_fig(x, y, h, at, c="#1a1410", face=1, hat=False, helmet=False):
    """A walking figure holding a lantern forward."""
    out = fig(x, y, h, at, c, "hold", face, hat=hat, helmet=helmet)
    lx, ly = x + face * .3 * h, y - .52 * h
    out += [gl(lx, ly, h * .9, at + .2, .7, "lamp"), circ(lx, ly, h * .045, "#ffe2a8", at=at + .2, fx="pop")]
    return out


# ------------------------------------------------------------------ forest pieces (side views)
def crown_row(x0, x1, base, r, at, c=LEAF, top=None, seed=1, hi=LEAF_L, op=None, jit=.35, step=None, fx=None):
    """A row of tree crowns as one shape: bumps of radius ~r along x0..x1, their tops near base - r*1.6, filled down to base."""
    rnd = random.Random(seed)
    step = step or r * 1.25
    pts, his = [(x0, base)], []
    x = x0
    while x < x1 + step:
        rr = r * rnd.uniform(1 - jit, 1 + jit)
        cy = base - r * 1.2 - rnd.uniform(0, r * .6)
        arc = [(x + rr * math.cos(math.radians(a)), cy - rr * math.sin(math.radians(a))) for a in range(180, -1, -30)]
        pts += arc
        his.append(arc[1:4])
        x += step
    pts.append((x1 + step, base))
    out = [poly(pts, c, "none", 0, at, op=op, fx=fx)]
    if hi:
        out.append(ln([p for seg in his for p in seg], at, hi, 2, draw=False, op=.5 if op is None else op * .5))
    return out


def tree(x, ground, h, at, c=LEAF, trunk="#3a2a1e", w=None, seed=1, fx=None, hi=LEAF_L, op=None):
    """A rainforest tree in side view: a straight trunk and a lumpy crown."""
    w = w or h * .55
    out = [ln([(x, ground), (x, ground - h * .62)], at, trunk, max(3, h * .045), draw=False, op=op)]
    rnd = random.Random(seed)
    cy = ground - h * .78
    for k in range(4):
        ox = (k - 1.5) * w * .22 + rnd.uniform(-6, 6)
        oy = rnd.uniform(-h * .06, h * .06)
        out.append(poly(blob(x + ox, cy + oy, w * .32, h * .16, 18, .15, seed + k), c, "none", 0, at, op=op))
    if hi:
        out.append(poly(blob(x - w * .12, cy - h * .1, w * .2, h * .06, 14, .2, seed + 9), hi, "none", 0, at, op=.55 if op is None else op * .55))
    if fx:
        return [grp(out, at, fx)]
    return out


def palm(x, ground, h, at, c="#2a4a2c", lean=0.0, fx=None, fruit=None):
    """A slender palm (acai-like): a thin stem and a spray of fronds."""
    tx, ty = x + lean * h, ground - h
    out = [ln([(x, ground), (x + lean * h * .5, ground - h * .5), (tx, ty)], at, "#5a4a36", max(2.5, h * .025), curve=True, draw=False)]
    for k in range(9):
        a = math.radians(-170 + k * 20)
        L = h * .32
        out.append(ln([(tx, ty), (tx + math.cos(a) * L * .6, ty + math.sin(a) * L * .45 - 6), (tx + math.cos(a) * L, ty + math.sin(a) * L * .55 + 10)], at, c, max(2.5, h * .022), curve=True, draw=False))
    if fruit:
        out += [circ(tx + dx, ty + 18 + dy, 3.2, fruit, at=at) for dx, dy in ((-10, 6), (-6, 12), (-12, 14), (8, 8), (12, 14), (5, 16))]
    if fx:
        return [grp(out, at, fx)]
    return out


def hut(x, ground, w, h, at, c=THATCH, edge=THATCH_D, door=True, fx="pop", smoke=False):
    """A thatched house in side view: a tall rounded thatch roof down to the ground."""
    pts = [(x - w / 2, ground), (x - w * .48, ground - h * .45), (x - w * .3, ground - h * .85), (x, ground - h), (x + w * .3, ground - h * .85),
           (x + w * .48, ground - h * .45), (x + w / 2, ground)]
    out = [poly(pts, c, edge, 1.5, curve=True)]
    for k in range(1, 4):
        yy = ground - h * k * .24
        hw = w / 2 * math.sqrt(max(0.05, 1 - (k * .24) ** 2)) * .98
        out.append(ln([(x - hw, yy), (x + hw, yy)], 0, edge, 1.2, draw=False, op=.6))
    if door:
        out.append(rect(x - w * .07, ground - h * .3, w * .14, h * .3, "#2a1d12", "none", 0, 3))
    if smoke:
        out += [poly(blob(x + 6 + k * 5, ground - h - 18 - k * 20, 10 + k * 4, 7 + k * 2, 12, .2, k + 3), "rgba(220,214,204,.35)") for k in range(3)]
    return [grp(out, at, fx)] if fx else out


def canoe(x, y, w, at, c="#5a3a22", people=2, pc="#1a1410", fx="pop"):
    """A dugout canoe on the waterline y, with paddlers."""
    out = [poly([(x - w / 2, y - 6), (x + w / 2, y - 6), (x + w * .42, y + 4), (x - w * .42, y + 4)], c, "#8a6a48", 1.2)]
    for k in range(people):
        px = x - w * .3 + k * w * .6 / max(1, people - 1)
        out += [circ(px, y - 20, 5, pc), poly([(px - 5, y - 15), (px + 5, y - 15), (px + 4, y - 4), (px - 4, y - 4)], pc),
                ln([(px + 6, y - 18), (px - 8, y + 10)], 0, "#8a6a48", 2, draw=False)]
    return [grp(out, at, fx)]


def brigantine(x, y, w, at, c="#2a1d14", sail="#d9c7a6", fx=None):
    """A small sixteenth-century river brigantine: hull on the waterline y, one mast and a square sail."""
    hull = [(x - w * .5, y - w * .1), (x + w * .5, y - w * .12), (x + w * .42, y), (x - w * .4, y)]
    out = [poly(hull, c, "rgba(255,226,190,.3)", 1.2), ln([(x, y - w * .1), (x, y - w * .62)], 0, c, 3, draw=False),
           poly([(x - w * .18, y - w * .55), (x + w * .18, y - w * .55), (x + w * .2, y - w * .2), (x - w * .2, y - w * .2)], sail, "rgba(60,40,20,.5)", 1),
           ln([(x - w * .5, y - w * .1), (x - w * .62, y - w * .2)], 0, c, 2, draw=False)]
    return [grp(out, at, fx)] if fx else out


def plane(x, y, s, at, c="#e9e2d6", fx=None):
    """A small survey aircraft seen from below and behind (a silhouette)."""
    out = [poly([(x - s, y), (x + s, y), (x + s * .9, y + s * .1), (x - s * .9, y + s * .1)], c, "none"),
           poly(E(x, y + s * .05, s * .14, s * .32, 18), c, "none"),
           poly([(x - s * .3, y - s * .28), (x + s * .3, y - s * .28), (x + s * .26, y - s * .22), (x - s * .26, y - s * .22)], c, "none"),
           circ(x, y + s * .3, s * .05, "#9fd0ff")]
    return [grp(out, at, fx)] if fx else out


def jar(x, ground, h, at, fx="pop"):
    """A painted polychrome jar (Amazonian style, schematic): cream slip with red and black bands."""
    w = h * .8
    body = [(x - w * .18, ground - h), (x + w * .18, ground - h), (x + w * .16, ground - h * .9), (x + w * .5, ground - h * .55), (x + w * .42, ground - h * .2),
            (x + w * .2, ground), (x - w * .2, ground), (x - w * .42, ground - h * .2), (x - w * .5, ground - h * .55), (x - w * .16, ground - h * .9)]
    out = [poly(body, "#eadcc0", "#8a5a3a", 1.5, curve=True)]
    for k, (yy, c) in enumerate(((.72, "#b0442a"), (.55, "#2a1d14"), (.38, "#b0442a"))):
        hw = w * (.47 if k == 1 else .43)
        out.append(ln([(x - hw, ground - h * yy), (x + hw, ground - h * yy)], 0, c, 4 if k != 1 else 2.5, draw=False))
    for k in range(5):
        xx = x - w * .32 + k * w * .16
        out.append(ln([(xx, ground - h * .5), (xx + w * .06, ground - h * .44), (xx, ground - h * .4)], 0, "#2a1d14", 1.6, draw=False))
    return [grp(out, at, fx)]


# ================================================================== maps (coasts from films.View; rivers and the Andes drawn here, schematic)
RIV = {
    "amazon": [(-73.4, -4.4), (-72.9, -3.45), (-71.3, -4.0), (-69.95, -4.2), (-68.0, -3.5), (-66.3, -3.3), (-64.7, -3.4), (-63.1, -4.0), (-61.4, -3.6),
               (-60.0, -3.15), (-58.4, -3.1), (-56.6, -2.6), (-55.5, -1.95), (-54.7, -2.35), (-53.2, -1.85), (-52.0, -1.45), (-50.9, -0.6), (-50.0, 0.1)],
    "napo": [(-77.8, -0.95), (-76.98, -0.46), (-76.0, -0.75), (-75.4, -0.95), (-74.4, -1.8), (-73.6, -2.6), (-72.9, -3.45)],
    "coca": [(-77.75, -0.05), (-77.3, -0.25), (-76.98, -0.46)],
    "maranon": [(-77.6, -5.4), (-76.2, -4.7), (-75.0, -4.6), (-73.4, -4.4)],
    "ucayali": [(-74.5, -8.4), (-74.0, -6.9), (-73.7, -5.5), (-73.4, -4.4)],
    "negro": [(-67.1, 1.0), (-67.1, -0.1), (-65.4, -0.4), (-62.9, -0.95), (-61.2, -2.2), (-60.0, -3.15)],
    "jurua": [(-72.7, -8.2), (-72.6, -7.6), (-70.9, -6.9), (-69.9, -6.6), (-67.9, -5.2), (-66.6, -3.6), (-65.9, -2.7)],
    "purus": [(-70.6, -10.6), (-69.0, -9.6), (-67.4, -8.75), (-66.0, -7.9), (-64.8, -7.25), (-63.4, -5.6), (-61.5, -3.9)],
    "madeira": [(-65.35, -10.5), (-64.9, -9.6), (-63.9, -8.75), (-63.0, -7.5), (-61.3, -5.8), (-59.8, -4.4), (-58.8, -3.4)],
    "mamore": [(-64.8, -16.6), (-64.95, -14.85), (-65.3, -13.0), (-65.2, -11.8), (-65.35, -10.5)],
    "beni": [(-67.6, -14.4), (-66.7, -12.6), (-66.2, -11.2), (-65.35, -10.5)],
    "guapore": [(-60.0, -14.6), (-61.6, -13.5), (-63.3, -12.4), (-64.9, -11.9), (-65.2, -11.8)],
    "tapajos": [(-56.6, -9.8), (-57.6, -7.4), (-57.4, -5.9), (-56.0, -4.3), (-54.9, -2.6)],
    "xingu": [(-53.1, -12.9), (-53.0, -11.6), (-52.6, -10.1), (-52.3, -8.6), (-51.9, -6.7), (-52.3, -4.6), (-52.2, -3.2), (-52.0, -1.8)],
    "culuene": [(-53.4, -14.5), (-53.2, -13.4), (-53.1, -12.9)],
    "acre": [(-70.5, -10.9), (-69.3, -10.6), (-67.8, -9.97), (-67.4, -8.75)],
}
ANDES = [(-75.5, 7.5), (-76.2, 4.5), (-77.4, 1.8), (-78.5, -0.5), (-79.1, -2.6), (-78.6, -5.2), (-77.3, -8.6), (-75.6, -11.4), (-73.0, -13.6),
         (-70.5, -15.6), (-68.5, -16.8), (-67.0, -18.6)]


def coast(v, at=-1, fill="#2f3b2a", edge="rgba(255,236,206,.35)"):
    return {"k": "map", "land": v.land(), "in": at, "landc": fill}


def river(v, name, at, c=RIVER, w=3.0, dur=1.2, draw=True, op=None, part=None):
    pts = RIV[name] if part is None else RIV[name][part[0]:part[1]]
    return ln([v.p(lo, la) for lo, la in pts], at, c, w, dur=dur, curve=True, draw=draw, op=op)


def andes(v, at=-1, w=26, op=.5):
    pts = [v.p(lo, la) for lo, la in ANDES]
    return [ln(pts, at, "#6b5a48", w, curve=True, draw=False, op=op), ln(pts, at, "#a8957a", w * .35, curve=True, draw=False, op=op * .7)]


# ================================================================== the Upano valley from the air (s1, s4, s37): a true perspective
class Persp:
    """A pinhole camera at height H (m) above the valley floor, pitched down by `pitch` degrees, focal length F (units); world X east,
    Z away from the camera (m)."""

    def __init__(self, H=150.0, pitch=8.0, F=1140.0, cx=889.0, cy=500.0):
        self.H, self.F, self.cx, self.cy = H, F, cx, cy
        a = math.radians(pitch)
        self.ca, self.sa = math.cos(a), math.sin(a)

    def p(self, X, Z, Y=0.0):
        dy = Y - self.H
        yc = dy * self.ca + Z * self.sa
        zc = -dy * self.sa + Z * self.ca
        return (self.cx + self.F * X / zc, self.cy - self.F * yc / zc)

    def depth(self, X, Z, Y=0.0):
        return -(Y - self.H) * self.sa + Z * self.ca

    def horizon(self):
        return self.cy - self.F * self.sa / self.ca


PV = Persp()
ZNEAR, ZSCAN = 250.0, 3200.0              # the bare earth the lidar shows runs from the bottom of the frame to ZSCAN


def _rot(x, z, a):
    c, s = math.cos(a), math.sin(a)
    return (x * c - z * s, x * s + z * c)


def _road_pts():
    """The two straight roads (world X, Z ends) and their bearing."""
    return [((-420.0, 260.0), (1500.0, 3600.0)), ((560.0, 250.0), (-1700.0, 3500.0))]


def _city():
    """Platforms (X, Z, w, d, angle) round plazas (X, Z, s, angle), laid out along the two roads and scattered off them, plus
    drained-field patches. Schematic, but the platforms are about 20 by 10 m as in the Science paper."""
    rnd = random.Random(29)
    plats, plazas, fields = [], [], []

    def cluster(X, Z, a, n):
        s = rnd.uniform(34, 46)
        plazas.append((X, Z, s, a))
        slots = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, 1), (1, -1), (-1, 1)]
        rnd.shuffle(slots)
        for ox, oz in slots[:n]:
            if ox and oz:
                lx, lz, w, d = ox * (s / 2 + 12), oz * (s / 2 + 12), 18, 18 * .55
            elif ox:
                lx, lz, w, d = ox * (s / 2 + 8), 0, 10, 20
            else:
                lx, lz, w, d = 0, oz * (s / 2 + 8), 20, 10
            dx, dz = _rot(lx, lz, a)
            plats.append((X + dx, Z + dz, w * rnd.uniform(.9, 1.15), d * rnd.uniform(.9, 1.15), a, rnd.uniform(2.2, 3.4)))

    for (x0, z0), (x1, z1) in _road_pts():
        L = math.hypot(x1 - x0, z1 - z0)
        ux, uz = (x1 - x0) / L, (z1 - z0) / L
        a = math.atan2(uz, ux)
        t = 120.0
        side = 1
        while t < L - 60:
            for sd in (side, -side) if rnd.random() < .6 else (side,):
                off = sd * rnd.uniform(46, 66)
                X = x0 + ux * (t + rnd.uniform(-20, 20)) - uz * off
                Z = z0 + uz * t + ux * off
                if ZNEAR + 60 < Z < ZSCAN - 120 and not any(math.hypot(X - p[0], Z - p[1]) < 70 for p in plazas):
                    cluster(X, Z, a, rnd.choice((5, 6, 6, 7)))
            t += rnd.uniform(110, 170)
            side = -side
    for k in range(150):                    # clusters off the roads
        Z = rnd.uniform(420, ZSCAN - 200)
        half = (Z * PV.ca + PV.H * PV.sa) * (PV.cx + 60) / PV.F
        X = rnd.uniform(-half, half)
        if any(math.hypot(X - p[0], Z - p[1]) < 95 for p in plazas):
            continue
        cluster(X, Z, rnd.uniform(-.5, .5), rnd.choice((3, 4, 5)))
    for k in range(26):                     # drained fields: patches of parallel ditches
        Z = rnd.uniform(380, ZSCAN - 300)
        half = (Z * PV.ca + PV.H * PV.sa) * PV.cx / PV.F
        X = rnd.uniform(-half, half)
        if any(math.hypot(X - p[0], Z - p[1]) < 70 for p in plazas):
            continue
        fields.append((X, Z, rnd.uniform(60, 110), rnd.uniform(40, 80), rnd.uniform(-.6, .6)))
    return plats, plazas, fields


def _quad(X, Z, w, d, a, Y=0.0):
    pts = []
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        dx, dz = _rot(sx * w / 2, sz * d / 2, a)
        pts.append(PV.p(X + dx, Z + dz, Y))
    return pts


def _box_faces(X, Z, w, d, a, h):
    """The visible faces of a platform: [(points, shade)], top last; h exaggerated x1.6 for legibility."""
    h = h * 1.6
    c = []
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        dx, dz = _rot(sx * w / 2, sz * d / 2, a)
        c.append((X + dx, Z + dz))
    faces = []
    for i in range(4):
        (x0, z0), (x1, z1) = c[i], c[(i + 1) % 4]
        nx, nz = (z1 - z0), -(x1 - x0)            # outward normal (corners run counter-clockwise seen from above)
        mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
        if nx * (0 - mx) + nz * (0 - mz) > 0:     # faces the camera (at X 0, Z 0)
            shade = "#9a7a50" if abs(nx) > abs(nz) else "#b08e60"
            faces.append(([PV.p(x0, z0), PV.p(x1, z1), PV.p(x1, z1, h), PV.p(x0, z0, h)], shade))
    faces.append(([PV.p(x, z, h) for x, z in c], "#e6cc96"))
    return faces


def _ground_y(Z):
    return PV.p(0, Z)[1]


def _canopy_rows(z0, z1, seed=7, tod="dawn", ratio=1.15, rmin=7.0):
    """Forest rows from far (z1) to near (z0): each row the clean upper outline of its crowns (bumps of radius r, at least rmin units)
    over a base line, darker and hazier far away, alternate rows a shade apart, and a few emergent crowns."""
    rnd = random.Random(seed)
    rows = []
    Zs = []
    Z = z0
    while Z < z1:
        Zs.append(Z)
        Z *= ratio
    hz = PV.horizon()
    dusk = tod == "dusk"
    for k, Z in enumerate(reversed(Zs)):
        d = PV.depth(0, Z)
        r = max(rmin, PV.F * 11.0 / d)            # a crown about 22 m across, never smaller than rmin units
        top_y = PV.p(0, Z, 28.0)[1]
        base = PV.p(0, Z / ratio, 0.0)[1] + 2
        t = min(1.0, max(0.0, (top_y - hz) / (H_ - hz)))
        far = 1 - t
        c0 = ("#2c5232", "#26492d") if not dusk else ("#22392a", "#1d3325")
        col = _mix(c0[k % 2], "#5c6c66" if not dusk else "#363645", far ** 1.6 * .85)
        hi = _mix("#4f8a50" if not dusk else "#365a3c", "#7f8a80" if not dusk else "#4a4a5c", far ** 1.6 * .75)
        bumps = []
        x = -60 - rnd.uniform(0, r)
        while x < W_ + 60 + r:
            rr = r * rnd.uniform(.8, 1.3)
            bumps.append((x, top_y + rr * 1.0 + rnd.uniform(-r * .3, r * .3), rr))
            x += r * rnd.uniform(.85, 1.25)
        outline = []
        dx = max(2.0, r / 3.0)
        xx = -60.0
        j = 0
        while xx <= W_ + 60:
            y = base
            while j < len(bumps) - 1 and bumps[j][0] + bumps[j][2] < xx:
                j += 1
            for bx, by, br in bumps[max(0, j - 2):j + 3]:
                u = (xx - bx) / br
                if abs(u) < 1:
                    y = min(y, by - br * 1.0 * math.sqrt(1 - u * u))
            outline.append((round(xx, 1), round(y, 1)))
            xx += dx
        em = []
        if r > rmin * 1.05:                       # emergent crowns stand above the canopy here and there
            n = int(W_ / (r * 9))
            for j2 in range(n):
                ex = rnd.uniform(0, W_)
                er = r * rnd.uniform(1.3, 1.8)
                em.append((ex, top_y - er * .2, er, _mix(("#3d6b3c", "#4a7a42", "#2f5e36")[j2 % 3] if not dusk else "#2a4630", "#5c6c66" if not dusk else "#363645", far ** 1.6 * .85)))
        rows.append((Z, base, outline, col, hi, em))
    return rows


def _row_els(row, x0=None, x1=None, at=-1):
    """A forest row (or the part of it between x0 and x1): its crowns as one shape with a lit edge, and its emergent crowns."""
    Z, base, outline, col, hi, em = row
    sel = [q for q in outline if (x0 is None or q[0] >= x0) and (x1 is None or q[0] <= x1)]
    if len(sel) < 2:
        return []
    pts = [(sel[0][0], base)] + sel + [(sel[-1][0], base)]
    out = [poly(pts, col, "none", 0, at), ln(sel, at, hi, 1.4, draw=False, op=.6)]
    for ex, ey, er, ec in em:
        if (x0 is None or ex >= x0) and (x1 is None or ex <= x1):
            out += [poly(blob(ex, ey, er, er * .72, 14, .16, int(ex)), ec, "none", 0, at),
                    poly(blob(ex - er * .25, ey - er * .25, er * .45, er * .25, 10, .2, int(ex) + 1), hi, "none", 0, at, op=.45)]
    return out


def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def _mountains(tod="dawn", at=-1):
    """The Andes behind the valley in three layers, and Sangay's cone at right with its plume."""
    hz = PV.horizon()
    rnd = random.Random(3)
    out = []
    cols = {"dawn": ["#4a4560", "#3a3a52", "#2d3344"], "dusk": ["#3d3350", "#2e2a40", "#232433"]}[tod]
    for k, (base_y, amp, seed) in enumerate(((hz - 70, 70, 11), (hz - 38, 52, 5), (hz - 12, 30, 8))):
        pts = [(-60, hz + 20)]
        x = -60
        rr = random.Random(seed)
        while x <= W_ + 60:
            pts.append((x, base_y - rr.uniform(0, amp) * (1 if k else 1.0)))
            x += rr.uniform(40, 90)
        pts.append((W_ + 60, hz + 20))
        out.append(poly(pts, cols[k], "none", 0, at, curve=True))
    sx, sy, sw = 1312, hz - 152, 150               # Sangay: a steep, symmetric cone
    cone = [(sx - sw * 1.7, hz - 30), (sx - sw * .55, sy + 50), (sx - 14, sy), (sx + 14, sy), (sx + sw * .55, sy + 50), (sx + sw * 1.7, hz - 30)]
    out.append(poly(cone, "#3b3550" if tod == "dawn" else "#2f2a40", "none", 0, at, curve=False))
    out.append(ln(cone[:-1][1:] if False else cone[1:-1], at, "rgba(255,226,190,.28)", 1.2, draw=False))
    out.append(poly([(sx - 40, sy + 30), (sx - 14, sy), (sx + 14, sy), (sx + 40, sy + 30), (sx + 18, sy + 22), (sx, sy + 34), (sx - 20, sy + 22)], "#cfc6d8", "none", 0, at, op=.55))
    for k in range(6):                             # the plume drifts left
        out.append(poly(blob(sx - 30 - k * 46, sy - 30 - k * 14, 28 + k * 9, 16 + k * 4, 16, .2, 40 + k), "rgba(214,206,214,%.2f)" % (.42 - k * .05), "none", 0, at))
    return out


def valley(tod="dawn", reveal=None, strips=16, scan_at=(5.4, 9.2), forest_only=False, ghost_at=None):
    """The hero: the valley floor in perspective; the forest drawn once, the bare earth over it in strips (reveal = how many strips are
    already open at the first frame; the rest open between scan_at[0] and scan_at[1]). forest_only: the close (no strips), with the
    city's ghost glowing through the canopy from ghost_at."""
    hz = PV.horizon()
    els = []
    els += _mountains(tod)
    # haze on the far forest
    rows = _canopy_rows(ZNEAR * .9, 14000, 7, tod)
    for row in rows:
        els += _row_els(row)
    els.append(rect(-40, hz - 30, W_ + 80, 60, "rgba(232,190,160,.10)" if tod == "dawn" else "rgba(180,140,160,.08)", "none", 0, 0, -1))
    plats, plazas, fields = _city()
    if forest_only:
        if ghost_at is not None:
            gh = []
            for (x0, z0), (x1, z1) in _road_pts():
                z1c = min(z1, ZSCAN)
                t = (z1c - z0) / (z1 - z0)
                gh.append(ln([PV.p(x0, z0, 30), PV.p(x0 + (x1 - x0) * t, z1c, 30)], 0, GOLD, 2.2, draw=False, op=.55))
            for X, Z, w, d, a, h in plats:
                if Z < 1700:
                    q = [PV.p(*_rot2(X, Z, w, d, a, sx, sz), 30) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                    gh.append(poly(q, "none", GOLD, 1.3, 0, op=.6))
            els.append(grp(gh, ghost_at, "fade", dur=2.4))
        return els
    # the bare earth, in strips
    y_top = _ground_y(ZSCAN) - 6
    strip_w = (W_ + 80) / strips
    city = []                                         # (x-range, element)
    # the bare earth: opaque bands, lighter towards the camera; low hills (lit tops, shaded feet); two streams
    rnd = random.Random(5)
    ground = []
    nb = 16
    ys = [y_top + (H_ + 40 - y_top) * (k / nb) ** 1.35 for k in range(nb + 1)]
    for k in range(nb):
        ground.append(rect(-40, ys[k], W_ + 80, ys[k + 1] - ys[k] + 1.5, _mix("#7f7a72", "#b1a996", (k + .5) / nb), "none", 0, 0, 0))
    for k in range(10):
        Zc = rnd.uniform(520, ZSCAN - 300)
        Xc = rnd.uniform(-1000, 1000)
        rx, rz = rnd.uniform(160, 300), rnd.uniform(90, 160)
        f = min(1.0, (Zc - 300) / (ZSCAN - 300))
        base_c = _mix("#b1a996", "#7f7a72", f ** .7)
        q = [PV.p(Xc + rx * math.cos(math.radians(a)), Zc + rz * math.sin(math.radians(a))) for a in range(0, 360, 20)]
        q2 = [PV.p(Xc - rx * .08 + rx * .82 * math.cos(math.radians(a)), Zc + rz * .1 + rz * .75 * math.sin(math.radians(a)), 6) for a in range(0, 360, 20)]
        ground += [poly(q, _mix(base_c, "#5f5a52", .16), "none", 0, 0, curve=True), poly(q2, _mix(base_c, "#e8dfcc", .1), "none", 0, 0, curve=True)]
    for X0, ph in ((-640, .4), (980, 1.7)):
        pts = []
        for k in range(15):
            Z = 280 + k * 220
            if Z > ZSCAN - 40:
                break
            pts.append(PV.p(X0 + 130 * math.sin(k * .9 + ph), Z))
        ground.append(ln(pts, 0, "#6a645a", 2.6, curve=True, draw=False))
    for X, Z, sw, sd, a in fields:
        q = _quad(X, Z, sw, sd, a)
        n = 7
        for k in range(n):
            u = -1 + 2 * (k + .5) / n
            p0 = PV.p(*_rot2(X, Z, sw, sd, a, u, -1))
            p1 = PV.p(*_rot2(X, Z, sw, sd, a, u, 1))
            city.append((min(p0[0], p1[0]), max(p0[0], p1[0]), ln([p0, p1], 0, "#6f685d", 1.2, draw=False), Z))
    for (x0, z0), (x1, z1) in _road_pts():                          # the roads: a dark sunken strip between two pale banks
        z1c = min(z1, ZSCAN - 30)
        t = (z1c - z0) / (z1 - z0)
        xe, ze = x0 + (x1 - x0) * t, z1c
        L = math.hypot(xe - x0, ze - z0)
        nx, nz = -(ze - z0) / L, (xe - x0) / L
        for off, col, wd in ((-9, "#efe6d2", 2.0), (9, "#efe6d2", 2.0)):
            a_ = PV.p(x0 + nx * off, z0 + nz * off)
            b_ = PV.p(xe + nx * off, ze + nz * off)
            city.append((min(a_[0], b_[0]), max(a_[0], b_[0]), ln([a_, b_], 0, col, wd, draw=False, op=.8), 0))
        q = [PV.p(x0 + nx * -7, z0 + nz * -7), PV.p(xe + nx * -7, ze + nz * -7), PV.p(xe + nx * 7, ze + nz * 7), PV.p(x0 + nx * 7, z0 + nz * 7)]
        city.append((min(p[0] for p in q), max(p[0] for p in q), poly(q, "#5a544b", "none", 0, 0), 1))
    for X, Z, s, a in plazas:
        q = _quad(X, Z, s, s, a)
        city.append((min(p[0] for p in q), max(p[0] for p in q), poly(q, "#77715f", "#d8cdb4", 1.0, 0), Z + 1))
    for X, Z, w, d, a, h in plats:
        fs = _box_faces(X, Z, w, d, a, h)
        xs = [p[0] for f, _ in fs for p in f]
        for f, col in fs:
            city.append((min(xs), max(xs), poly(f, col, "rgba(60,44,28,.35)", .6, 0), Z))
    # far to near, so nearer platforms cover farther ones
    lay_lines = [c for c in city if c[3] > 1 and c[2]["k"] == "line"]
    lay_roads = [c for c in city if c[3] in (0, 1)]
    lay_rest = [c for c in city if c[3] > 1 and c[2]["k"] != "line"]
    lay_rest.sort(key=lambda c: -c[3])
    ordered = lay_lines + [c for c in lay_roads if c[3] == 1] + [c for c in lay_roads if c[3] == 0] + lay_rest
    edge_rows = [r for r in rows if ZSCAN * .98 <= r[0] <= ZSCAN * 1.5]
    reveal = strips if reveal is None else reveal
    t0, t1 = scan_at
    for k in range(strips):
        xa = -40 + k * strip_w
        xb = xa + strip_w
        cx0 = xa - (70 if k else 0)
        inside = [c[2] for c in ordered if c[1] >= cx0 - 2 and c[0] <= xb + 2]
        tree_line = []
        for row in edge_rows:
            tree_line += _row_els(row, cx0 - 30, xb + 30, 0)
        front = [rect(xb - 70, y_top + 4, 70, H_ - y_top, "rgba(159,208,255,.10)", "none", 0, 0, 0),
                 rect(xb - 22, y_top + 4, 22, H_ - y_top, "rgba(159,208,255,.16)", "none", 0, 0, 0),
                 ln([(xb, y_top + 2), (xb, H_ + 40)], 0, SCANC, 4, draw=False, op=.95),
                 ln([(xb - 4, y_top + 2), (xb - 4, H_ + 40)], 0, "#e6f3ff", 1.2, draw=False, op=.7)]
        edge = [ln([(cx0, y_top + 1.5), (xb + 2, y_top + 1.5)], 0, "#6f9cc2", 1.4, draw=False)]
        body = ground + inside + tree_line + edge + (front if k < strips - 1 else [])
        at = -1 if k < reveal else round(t0 + (t1 - t0) * (k - reveal) / max(1, strips - reveal - 1), 2)
        els.append(grp(body, at, "fade", clip=[cx0, y_top - 40, xb - cx0 + (0 if k < strips - 1 else 60), H_ - y_top + 120], dur=.22))
    return els


def _rot2(X, Z, w, d, a, sx, sz):
    dx, dz = _rot(sx * w / 2, sz * d / 2, a)
    return (X + dx, Z + dz)


def s1():
    """The hero: dawn over the Upano valley, the left of the floor already scanned, the rest stripped of its forest on 'strip the
    trees away'; the aircraft and its fan of laser rays above."""
    t0 = T("s1", "strip the trees") - .1
    els = valley("dawn", reveal=5, strips=16, scan_at=(t0, t0 + 2.8))
    px, py = 1080, 168
    hz = PV.horizon()
    rays = [ln([(px, py + 14), (x, y)], -1, SCANC, 1.2, draw=False, op=.28) for x, y in ((260, 700), (520, 600), (760, 560), (980, 545), (1220, 560), (1460, 620), (1640, 720))]
    els += rays + plane(px, py, 46, -1)
    els.append(gl(px, py + 12, 70, -1, .35, "glowb"))
    return {"base": "sky", "tod": "dawn", "ground": 1400, "ridges": [], "sun": [1520, PV.horizon() - 60, 22], "cam": CAM, "els": els}


def s2_add():
    """Push-in on the revealed city: platform tops glint, the roads light up, km ticks along one, the age (chips placed for the zoom,
    clear of the roads, and kept on top of the lit roads)."""
    plats, plazas, fields = _city()
    near = sorted([p for p in plazas if 560 < p[1] < 1200 and abs(PV.p(p[0], p[1])[0] - 900) < 420], key=lambda p: p[1])[:3]
    out, top = [], []
    t = T("s2", "earthen platforms")
    k = 0
    for X, Z, s_, a in near:
        for P in plats:
            if math.hypot(P[0] - X, P[1] - Z) < s_ + 30:
                x, y = PV.p(P[0], P[1], P[5] * 1.6)
                out.append(gl(x, y, 24, t + .1 * k, .85, "lamp"))
                k += 1
    top += chip(520, 520, "6,000+ platforms", GOLD, t + .5, 30)
    tr = T("s2", "roads as straight")
    for i, ((x0, z0), (x1, z1)) in enumerate(_road_pts()):
        z1c = min(z1, ZSCAN - 30)
        tt = (z1c - z0) / (z1 - z0)
        out.append(ln([PV.p(x0, z0, 1), PV.p(x0 + (x1 - x0) * tt, z1c, 1)], tr + .3 * i, AMBER, 4, dur=1.6))
    top += chip(1290, 700, "straight roads", AMBER, tr + .8, 28)
    (x0, z0), (x1, z1) = _road_pts()[0]
    L = math.hypot(x1 - x0, z1 - z0)
    tk = T("s2", "running for kilometres")
    offs = {1: (56, 34), 2: (45, 36), 3: (78, 28)}       # each km chip just below and right of its dot, stepped clear of the next
    for km in range(4):
        t_ = (km * 1000 + 200) / L
        if t_ > (ZSCAN - 30 - z0) / (z1 - z0):
            break
        x, y = PV.p(x0 + (x1 - x0) * t_, z0 + (z1 - z0) * t_, 1)
        out += [circ(x, y, 6, AMBER, "#1a120c", 1.5, at=tk + .25 * km, fx="pop")]
        if km:
            dx, dy = offs[km]
            top += chip(x + dx, y + dy, "%d km" % km, AMBER, tk + .25 * km, 22)
    top += chip(900, 380, "about 2,500 years old", GOLD, T("s2", "two and a half thousand"), 30)
    return out + top


def s4_add():
    t = T("s4", "who built this")
    out = qmark(889, 560, t, 130)
    tv = T("s4", "vanish under the trees")
    rnd = random.Random(4)
    for k, (y, r) in enumerate(((625, 30), (668, 26), (765, 22))):      # in the bands left free by the push-in's chips
        out += [poly(_bumps(160, 1620, y, r, rnd), "none", LILAC, 2, tv + .25 * k, style="claimed", fx="fade")]
    return out


def _bumps(x0, x1, y, r, rnd):
    pts = []
    x = x0
    while x < x1:
        rr = r * rnd.uniform(.8, 1.2)
        pts += [(x + rr * math.cos(math.radians(a)), y - rr * .8 * math.sin(math.radians(a))) for a in range(180, -1, -30)]
        x += r * 1.3
    return pts


def s53():
    """The close: the canopy at dusk, the city's ghost glowing through it."""
    els = valley("dusk", forest_only=True, ghost_at=T("s53", "made of earth"))
    for k, (x, y) in enumerate(((620, 300), (660, 290), (700, 304))):
        els.append(ln([(x - 10, y), (x, y - 6), (x + 10, y)], 1.0 + .2 * k, "#2a2230", 2.4, draw=False))
    return {"base": "sky", "tod": "dusk", "ground": 1400, "ridges": [], "sun": [1460, PV.horizon() - 40, 20], "cam": CAM, "els": els}



# ================================================================== COLD OPEN, second panel
def s3():
    """The seekers and the doubters, at night: explorers with lanterns walk into the forest under a lilac mirage of a golden city; a
    soil cut under the same forest, a thin dark top over pale soil, and three huts under a dashed lid."""
    ta, tb, tc = T("s3", "explorers hunted"), T("s3", "lost cities"), T("s3", "many scientists doubted")
    G = 700
    els = [rect(-40, G, W_ + 80, 400, "#1c1712", "none", 0, 0, -1)]
    els += crown_row(330, 860, G - 120, 46, -1, "#1e3524", seed=3, hi="#2f4f34")
    for k, x in enumerate((380, 470, 560, 660, 760, 840)):
        els += tree(x, G, 230 + (k % 3) * 30, -1, "#22402a", seed=k + 4, hi="#355a3a")
    els += lamp_fig(170, G, 120, ta, "#120e0b", 1, helmet=True) + lamp_fig(270, G, 116, ta + .4, "#120e0b", 1, hat=True)
    # the mirage: a skyline of towers and domes in lilac dots, gold glints
    sky = [(250, 380), (250, 330), (290, 330), (290, 290), (320, 270), (350, 290), (350, 330), (400, 330), (400, 250), (430, 220), (460, 250), (460, 330),
           (520, 330), (540, 300), (580, 290), (620, 300), (640, 330), (690, 330), (690, 270), (720, 270), (720, 330), (770, 330), (770, 380)]
    els += [gl(510, 300, 260, tb, .25, "lamp"), ln(sky, tb, LILAC, 3, "claimed", dur=1.4)]
    els += [circ(x, y, 4, AU, at=tb + .6 + .05 * k, fx="pop") for k, (x, y) in enumerate(sky[1:-1:2])]
    els += chip(510, 190, "lost cities?", LILAC, tb + .8, 30)
    # the doubters: a soil cut under the forest at right
    S = 470
    els += [rect(930, S, 760, 22, "#3a2c20", "none", 0, 0, tc), rect(930, S + 22, 760, 300, "#c9a46a", "none", 0, 0, tc),
            rect(930, S + 22, 760, 300, "url(#k-speck)", "none", 0, 0, tc)]
    els += crown_row(930, 1690, S, 34, tc, "#24402a", seed=9, hi="#3a6040", fx="fade")
    els += [ln([(1000, S + 60), (1000, S + 200)], tc + .5, BLUE, 2.5, dur=.6), ln([(1200, S + 60), (1200, S + 220)], tc + .6, BLUE, 2.5, dur=.6),
            ln([(1400, S + 60), (1400, S + 210)], tc + .7, BLUE, 2.5, dur=.6)]
    els += hut(1180, S, 50, 50, tc + .9) + hut(1260, S, 44, 44, tc + 1.0) + hut(1330, S, 48, 48, tc + 1.1)
    els += [ln([(1100, S - 80), (1420, S - 80)], tc + 1.4, RED, 3, "inferred", dur=.8)]
    els += chip(1310, 330, "too poor for cities?", LILAC, tc + 1.6, 28)
    return {"base": "sky", "tod": "night", "ground": 1400, "ridges": [], "sun": False, "moon": [1560, 170, 24], "cam": CAM, "els": els}


# ================================================================== CHAPTER 1 · A river of villages
def s6():
    """El dorado: dawn on a round mountain lake; a reed raft with attendants and, at its centre, a figure that glows with gold dust;
    gold falls into the water as offerings."""
    t1, t2, t3 = T("s6", "the golden one"), T("s6", "covered in gold dust"), T("s6", "made offerings")
    els = []
    for k, (y, amp, col, seed) in enumerate(((300, 90, "#3a4a3e", 2), (360, 70, "#2d3d33", 5))):
        pts = [(-40, 600)]
        rr = random.Random(seed)
        x = -40
        while x < W_ + 60:
            pts.append((x, y - rr.uniform(0, amp)))
            x += rr.uniform(70, 140)
        pts.append((W_ + 60, 600))
        els.append(poly(pts, col, "none", 0, -1, curve=True))
    els += [rect(-40, 440, W_ + 80, 640, "#24332a", "none", 0, 0, -1),
            poly([(-40, 600), (180, 450), (420, 470), (600, 440), (889, 452), (1200, 440), (1420, 466), (1640, 450), (W_ + 40, 600)], "#24332a", "none", 0, -1, curve=True),
            poly(E(889, 640, 820, 175, 48), "#2f5f78", "rgba(255,236,206,.35)", 1.5, -1),
            poly(E(889, 668, 640, 110, 48), "#3a7390", "none", 0, -1, op=.6),
            poly([(-40, 1040), (-40, 760), (200, 770), (420, 800), (700, 812), (1000, 812), (1300, 800), (1560, 770), (W_ + 40, 750), (W_ + 40, 1040)], "#1f2a22", "none", 0, -1, curve=True)]
    rx, ry, S = 889, 676, 1.55
    raft = [(rx - 150 * S, ry), (rx + 150 * S, ry), (rx + 120 * S, ry + 22 * S), (rx - 180 * S, ry + 22 * S)]
    els += [poly(raft, "#7a5a32", "#c9a46a", 1.5, -1)] + [ln([(rx - 160 * S + 26 * S * k, ry + 3), (rx - 175 * S + 26 * S * k, ry + 20 * S)], -1, "#5a4022", 1.6, draw=False) for k in range(12)]
    for k, x in enumerate((rx - 170, rx - 95, rx + 95, rx + 165)):
        els += fig(x, ry + 6, 62 * S, -1, "#1a1410", None if k % 2 else "hold", 1 if x < rx else -1, fx=None)
    els += fig(rx, ry + 6, 92 * S, -1, "#2a1d14", "lift", 1, fx=None)
    els += [gl(rx, ry - 80, 230, t1, .75, "lamp")] + fig(rx, ry + 6, 92 * S, t1, AU, "lift", 1, fx="fade")
    rnd = random.Random(3)
    els += [circ(rx + rnd.uniform(-40, 40), ry - 40 - rnd.uniform(0, 100), 3.2, "#fff2c0", at=t2 + .08 * k, fx="pop") for k in range(16)]
    for k in range(7):                                                       # offerings fall; rings on the water
        x = rx - 150 + k * 50
        y = ry + 50 + (k % 3) * 10
        els += [circ(x, y, 4.5, AU, at=t3 + .25 * k, fx="pop"), poly(E(x, y + 14, 22, 5, 18), "none", "rgba(255,226,160,.6)", 1.4, t3 + .3 + .25 * k)]
    els += [poly(E(rx, ry + 95, 170, 18, 24), "rgba(255,210,120,.18)", "none", 0, t1)]
    els += [lab(rx, 300, "the golden one", t1 + .3, GOLD, 42, st="serif"), lab(1480, 560, "a mountain lake", t3 + .4, DIM, 28)]
    return {"base": "sky", "tod": "dawn", "ground": 1400, "ridges": [], "sun": [1350, 250, 22], "cam": CAM, "els": els}

def muisca_raft(cx, cy, s, at):
    """The gold raft from Pasca (schematic, three-quarter view): a raft of thin parallel strands, a tall central figure with a fanned
    headdress, smaller attendants round the edges, two of them holding staffs."""
    out = []
    W, D = 300 * s, 120 * s
    A = (cx - W / 2, cy)
    def P(u, v):                       # u along the raft (0..1), v across (0..1) in an oblique view
        return (cx - W / 2 + u * W + v * 70 * s, cy - v * D * .45)
    deck = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
    out.append(poly(deck, "#b8862a", "#ffe08a", 1.5))
    for k in range(14):
        u = (k + .5) / 14
        out.append(ln([P(u, 0), P(u, 1)], 0, "#8a5f18", 1.6, draw=False))
    out.append(poly([P(0, 0), P(1, 0), (P(1, 0)[0], P(1, 0)[1] + 10 * s), (P(0, 0)[0], P(0, 0)[1] + 10 * s)], "#7a5214", "none"))
    def man(u, v, h, staff=False, crown=False):
        x, y = P(u, v)
        g = [poly([(x - .16 * h, y), (x + .16 * h, y), (x + .12 * h, y - .7 * h), (x - .12 * h, y - .7 * h)], "#d9a63a", "#ffe08a", 1),
             circ(x, y - .82 * h, .13 * h, "#d9a63a", "#ffe08a", 1)]
        if crown:
            g.append(poly([(x - .3 * h, y - .9 * h), (x - .22 * h, y - 1.2 * h), (x - .08 * h, y - 1.0 * h), (x, y - 1.26 * h), (x + .08 * h, y - 1.0 * h),
                           (x + .22 * h, y - 1.2 * h), (x + .3 * h, y - .9 * h)], "#f2c96a", "#ffe08a", 1))
        if staff:
            g.append(ln([(x + .2 * h, y), (x + .2 * h, y - 1.25 * h)], 0, "#e8b84a", 2.2, draw=False))
        return g
    for u, v in ((.08, .15), (.2, .85), (.32, .1), (.68, .1), (.8, .85), (.92, .15), (.1, .6), (.9, .6)):
        out += man(u, v, 46 * s, staff=(u in (.2, .8)))
    out += man(.5, .5, 92 * s, crown=True)
    out += man(.5, .9, 42 * s)
    out += man(.5, .08, 42 * s)
    return [grp(out, at, "pop", dur=.9)]


def s7():
    """The Muisca: a small map of the Colombian highlands (clipped to its frame), then the gold raft found in 1969, in lamp light."""
    t1, t2 = T("s7", "Muisca people"), T("s7", "small gold raft")
    fx0, fy0, fw, fh = 1010, 150, 640, 560
    v = View(-80.0, -66.0, -2.0, 12.0, (fx0, fy0, fw, fh))
    bx, by = v.p(-74.07, 4.71)
    mp = [rect(fx0, fy0, fw, fh, "#1d3a4a", "none", 0, 0, 0), {"k": "map", "land": v.land(), "in": 0, "landc": "#3b4a33"}] + andes(v, 0, 10, .45)
    els = [grp(mp, -1, None, clip=[fx0, fy0, fw, fh]), rect(fx0, fy0, fw, fh, "none", "rgba(255,236,206,.3)", 1.5, 14, -1)]
    els += [pin(bx, by, "Muisca", t1, GOLD), lab(fx0 + fw / 2, fy0 + fh - 28, "Colombian highlands", t1 + .5, DIM, 26)]
    els += [rect(250, 600, 540, 60, "#3a2c20", "rgba(255,236,206,.3)", 1.5, 4, -1), rect(270, 300, 500, 300, "rgba(200,220,230,.05)", "rgba(220,235,245,.35)", 2, 6, -1),
            ln([(270, 300), (300, 280), (800, 280), (770, 300)], -1, "rgba(220,235,245,.35)", 2, draw=False), ln([(800, 280), (800, 580), (770, 600)], -1, "rgba(220,235,245,.35)", 2, draw=False)]
    els += [gl(520, 470, 330, t2, .45, "lamp")] + muisca_raft(520, 520, 1.25, t2)
    els += [circ(520 + dx, 420 + dy, 3, "#fff6cf", at=t2 + 1.0 + .15 * k, fx="pop") for k, (dx, dy) in enumerate(((-90, 30), (40, -60), (120, 40), (-30, 70)))]
    els += [lab(520, 710, "Muisca raft", t2 + .6, GOLD, 32, st="serif")] + chip(520, 230, "found 1969", AU, t2 + 1.0, 28)
    els += [ln([(340, 750), (700, 750)], t2 + 1.3, BONE, 2, dur=.6), ln([(340, 740), (340, 760)], t2 + 1.3, BONE, 2, draw=False),
            ln([(700, 740), (700, 760)], t2 + 1.3, BONE, 2, draw=False), lab(520, 785, "about 19.5 cm", t2 + 1.5, DIM, 24)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}

VN = View(-82.0, -45.0, -13.0, 8.5, (90, 120, 1600, 680))


def _basin(v, at=-1, names=("amazon", "napo", "coca", "maranon", "ucayali", "negro", "jurua", "purus", "madeira", "tapajos", "xingu", "mamore", "beni"), aw=10):
    els = [{"k": "map", "land": v.land(), "in": at, "landc": "#2e3d2c"}]
    els += andes(v, at, aw, .35)
    for n in names:
        els.append(river(v, n, at, "#4f8fae", 3.2 if n == "amazon" else 1.8, draw=False, op=.85))
    return els

VE = View(-81.6, -72.4, -4.4, 1.9, (90, 130, 1600, 660))


def s8():
    """Ecuador up close: the army's dashed route east from Quito over the Andes; hunger; Orellana's boat and its gold route start down
    the Napo; an arrow back upstream, crossed."""
    v = VE
    qx, qy = v.p(-78.47, -0.18)
    t0, t1, t2 = T("s8", "found hunger"), T("s8", "Francisco de Orellana"), T("s8", "the current never")
    els = [{"k": "map", "land": v.land(), "in": -1, "landc": "#2e3d2c"}] + andes(v, -1, 34, .4)
    for n in ("napo", "coca", "maranon", "amazon"):
        els.append(river(v, n, -1, "#4f8fae", 3.2, draw=False, op=.9))
    els += [pin(qx, qy, "Quito", -1, BONE, a="end", lx=-16), lab(v.p(-78.7, -2.2)[0], v.p(-78.7, -2.2)[1], "the Andes", -1, DIM, 26, st="ital")]
    route = [v.p(-78.47, -0.18), v.p(-78.1, -0.32), v.p(-77.75, -0.2), v.p(-77.3, -0.3), v.p(-76.98, -0.46)]
    els += [ln(route, .3, DIM, 3.5, "inferred", dur=1.4)] + chip(qx, qy - 70, "1541", DIM, .6, 26)
    for k, (lo, la) in enumerate(((-78.2, -0.3), (-77.9, -0.26), (-77.55, -0.25))):
        x, y = v.p(lo, la)
        els += fig(x, y - 4, 34, .5 + .2 * k, "#d9c7a6", None, 1)
    hx, hy = v.p(-77.35, -0.32)
    els += [gl(hx, hy, 70, t0, .55, "red"), lab(hx + 22, hy - 62, "hunger", t0 + .2, "#ffb09a", 26)]       # above the glow, clear of the rivers
    napo = [v.p(lo, la) for lo, la in RIV["napo"][1:]]
    els += [ln(napo, t1 + .5, GOLD, 5, dur=3.4, curve=True)]
    bx, by = v.p(-76.75, -0.55)
    els += [poly([(bx - 18, by - 5), (bx + 18, by - 5), (bx + 12, by + 6), (bx - 12, by + 6)], "#e8d6b8", "none", 0, t1 + .2, fx="pop")]
    els += chip(bx + 40, by - 64, "December 1541", GOLD, t1 + .3, 24, "start") + [lab(bx + 14, by + 84, "about 50 men", t1 + .9, GOLD, 26)]
    ax, ay = v.p(-75.0, -1.15)
    els += [arr([(ax + 89, ay + 6), (ax - 11, ay - 60)], t2, DIM, 3, curve=False)] + cross(ax + 39, ay - 27, t2 + .5, RED, 1.2, 5)   # beside the route
    els += [lab(v.p(-74.6, -2.5)[0], v.p(-74.6, -2.5)[1], "Napo", .2, "#9fd0ff", 26, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def s9():
    """The whole basin: the gold route, already down the Napo, runs on down the Amazon to the Atlantic; August 1542."""
    v = VN
    t1 = T("s9", "reached the Atlantic")
    els = _basin(v)
    qx, qy = v.p(-78.47, -0.18)
    els += [pin(qx, qy, "Quito", -1, BONE, a="end", lx=-16)]
    napo = [v.p(lo, la) for lo, la in RIV["napo"][1:]]
    els += [ln(napo, -1, GOLD, 4.5, curve=True, draw=False)]
    amaz = [v.p(lo, la) for lo, la in RIV["amazon"][1:]]
    els += [ln(amaz, .4, GOLD, 4.5, dur=4.2, curve=True)]
    mx, my = v.p(-50.0, 0.1)
    els += [gl(mx, my, 80, 4.4, .6, "lamp")] + chip(mx - 30, my - 70, "August 1542", GOLD, 4.5, 26, "end")
    els += [lab(v.p(-47.2, 3.2)[0], v.p(-47.2, 3.2)[1], "the Atlantic", t1, BLUE, 30, st="ital"), lab(v.p(-61.0, -1.4)[0], v.p(-61.0, -1.4)[1], "Amazon", 1.0, "#9fd0ff", 26, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}

def s10():
    """Carvajal's river: across the water, high red banks under the forest where villages pop one after another, paths running inland,
    a fleet of canoes; in front, the brigantine with the friar writing; a painted jar in its own lamp-lit window."""
    t0, t1, t2, t3, t4 = T("s10", "wrote down"), T("s10", "Village after village"), T("s10", "Roads running"), T("s10", "Fleets of war"), T("s10", "And pottery")
    W0, BT = 520, 380                          # waterline, top of the far bank
    els = [rect(-40, W0, W_ + 80, 520, "#2f6e8c", "none", 0, 0, -1), rect(-40, W0, W_ + 80, 14, "rgba(255,236,206,.18)", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, BT - 70, 30, -1, "#1e3a26", seed=13, hi="#2f5034")
    els += crown_row(-40, W_ + 40, BT - 8, 34, -1, "#2a4a2c", seed=12, hi="#3f6a40")
    bank = [(-40, W0 + 4), (-40, BT + 4)] + [(x, BT + 8 * math.sin(x / 160.0)) for x in range(0, W_ + 60, 40)] + [(W_ + 40, W0 + 4)]
    els += [poly(bank, "#a0583a", "rgba(255,226,190,.3)", 1.2, -1, curve=True)]
    els += [ln([(x, BT + 24 + 8 * math.sin(x / 160.0)), (x + 26, W0 - 6)], -1, "#7a3a22", 1.4, draw=False, op=.5) for x in range(40, W_, 80)]
    xs = [180, 420, 660, 900, 1140, 1380]
    for k, x in enumerate(xs):
        y = BT + 8 * math.sin(x / 160.0) + 2
        tk = t1 + .3 * k
        els += hut(x - 44, y, 52, 58, tk, THATCH_D, "#5a4020", smoke=(k % 2 == 0)) + hut(x + 8, y, 64, 70, tk + .08, THATCH_D, "#5a4020") + hut(x + 58, y, 46, 50, tk + .16, THATCH_D, "#5a4020")
    for k, x in enumerate(xs[::2]):
        y = BT + 8 * math.sin(x / 160.0) - 10
        els.append(ln([(x, y), (x + 30 + 20 * k, y - 150)], t2 + .2 * k, "#e2c27e", 3.5, "inferred", dur=.8))
    for k in range(8):
        els += canoe(520 + k * 130 + (k % 2) * 30, W0 + 60 + (k % 3) * 34, 100, t3 + .12 * k, people=3)
    els += brigantine(250, W0 + 330, 360, -1)
    els += fig(225, W0 + 294, 92, -1, "#1a1410", "hold", 1, fx=None, coat=True)
    els += [rect(268, W0 + 228, 26, 20, "#efe6d2", "none", 0, 2, -1), lab(250, W0 + 380 - 100, "", -1)]
    els += [lab(400, W0 + 220, "Carvajal", t0, BONE, 28, "start")]
    vx, vy, vr = 1520, 640, 120
    els += [circ(vx, vy, vr, "#1a1410", "rgba(255,236,206,.4)", 2, t4, fx="pop"), gl(vx, vy, 150, t4, .55, "lamp")] + jar(vx, vy + 70, 140, t4 + .1)
    els += [lab(vx, vy - vr - 18, "finer than Malaga's", t4 + .4, GOLD, 28)]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [300, 140, 20], "cam": CAM, "els": els}

def amazon_warrior(x, y, h, at):
    """A warrior woman in black figure, as on a Greek vase: crested helmet, crescent shield, spear."""
    BLK = "#1d130d"
    out = [poly([(x - .08 * h, y - .5 * h), (x + .08 * h, y - .5 * h), (x + .2 * h, y), (x - .2 * h, y)], BLK),
           poly([(x - .07 * h, y - .78 * h), (x + .07 * h, y - .78 * h), (x + .09 * h, y - .48 * h), (x - .09 * h, y - .48 * h)], BLK),
           circ(x, y - .86 * h, .075 * h, BLK),
           poly([(x - .02 * h, y - .93 * h), (x + .02 * h, y - 1.02 * h), (x - .18 * h, y - .98 * h), (x - .24 * h, y - .86 * h), (x - .08 * h, y - .92 * h)], BLK, curve=True),
           ln([(x - .3 * h, y - .15 * h), (x + .35 * h, y - 1.08 * h)], 0, BLK, .03 * h, draw=False),
           poly([(x + .1 * h, y - .75 * h), (x + .36 * h, y - .7 * h), (x + .3 * h, y - .5 * h), (x + .22 * h, y - .58 * h), (x + .12 * h, y - .52 * h)], BLK, curve=True)]
    return [grp([circ(x, y - .5 * h, .62 * h, "#c46d3a", "#9c4f26", 2)] + out, at, "pop")]


def s11_add():
    """The gaps: a long stretch of the route turns grey, two hundred leagues; then the warrior women and the river's name."""
    v = VN
    t1, t2 = T("s11", "two hundred leagues"), T("s11", "warriors led by women")
    gap = [v.p(lo, la) for lo, la in RIV["napo"][2:]] + [v.p(lo, la) for lo, la in RIV["amazon"][1:4]]
    out = [ln(gap, t1, "#9a938a", 7, dur=1.4, curve=True)]
    gx, gy = v.p(-71.5, -6.4)
    out += [ln([v.p(-73.6, -2.9), (gx, gy - 24)], t1 + .4, DIM, 1.5, "inferred", dur=.5)] + chip(gx, gy, "200 leagues, no village", DIM, t1 + .6, 26)
    wx, wy = v.p(-62.0, 3.6)
    out += amazon_warrior(wx, wy, 110, t2)
    nx, ny = v.p(-58.5, -4.6)
    out += [lab(nx, ny, "River of the Amazons", t2 + 1.2, GOLD, 30, st="ital")]
    return out

def s12():
    """The same bank, at dusk and empty: forest down to the water, faint outlines where houses stood, one canoe; a red wash sweeps along
    it; the friar's book, 'tall tale?'; then 'made up?' and 'emptied?'."""
    t1, t2, t3 = T("s12", "Epidemics"), T("s12", "tall tale"), T("s12", "Either Carvajal")
    W0, BT = 520, 380
    els = [rect(-40, W0, W_ + 80, 520, "#20485e", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, BT - 70, 30, -1, "#172d1f", seed=13, hi="#253f2b")
    els += crown_row(-40, W_ + 40, BT - 8, 34, -1, "#1d3624", seed=12, hi="#2c4a31")
    bank = [(-40, W0 + 4), (-40, BT + 4)] + [(x, BT + 8 * math.sin(x / 160.0)) for x in range(0, W_ + 60, 40)] + [(W_ + 40, W0 + 4)]
    els += [poly(bank, "#6e3e28", "rgba(255,226,190,.2)", 1.2, -1, curve=True)]
    els += crown_row(560, W_ + 40, BT + 40, 30, -1, "#22402a", seed=23, hi="#2f5034")
    for k, x in enumerate((660, 900, 1140, 1380)):
        y = BT + 8 * math.sin(x / 160.0) - 6
        els += [poly([(x - 34, y), (x - 30, y - 46), (x, y - 60), (x + 30, y - 46), (x + 34, y)], "none", "rgba(245,236,220,.55)", 2, -1, curve=True, style="inferred")]
    els += canoe(1100, W0 + 110, 100, -1, people=1)
    els += [gl(620 + 150 * k, BT - 10 + (k % 2) * 30, 150, t1 + .22 * k, .32, "red") for k in range(8)]
    els += [poly([(120, 330), (290, 310), (460, 330), (460, 560), (290, 540), (120, 560)], "#e9dcc0", "#8a6a44", 1.5, -1),
            ln([(290, 310), (290, 540)], -1, "#8a6a44", 1.5, draw=False)]
    els += [{"k": "glyphs", "x": 140, "y": 345, "w": 130, "h": 180, "rows": 9, "cols": 5, "kind": "latin", "c": "#5a4632", "in": -1},
            {"k": "glyphs", "x": 310, "y": 335, "w": 130, "h": 190, "rows": 9, "cols": 5, "kind": "latin", "c": "#5a4632", "in": -1}]
    els += chip(290, 255, "tall tale?", LILAC, t2, 28)
    els += chip(290, 620, "made up?", LILAC, t3 + .2, 28) + chip(1150, 250, "emptied?", LILAC, t3 + 1.6, 28)
    return {"base": "sky", "tod": "dusk", "ground": 1400, "ridges": [], "sun": [1520, 300, 20], "cam": CAM, "els": els}



# ================================================================== CHAPTER 2 · The lost city of Z
def theodolite(x, ground, h, at):
    """A surveyor's theodolite on a tripod."""
    top = ground - h
    out = [ln([(x, top + 10), (x - h * .28, ground)], 0, "#8a6a48", 3, draw=False), ln([(x, top + 10), (x + h * .28, ground)], 0, "#8a6a48", 3, draw=False),
           ln([(x, top + 10), (x + h * .05, ground)], 0, "#6a5038", 3, draw=False),
           rect(x - h * .12, top - h * .1, h * .24, h * .14, "#c9b38a", "#5a4632", 1.2, 3),
           ln([(x - h * .22, top - h * .14), (x + h * .2, top - h * .06)], 0, "#3a2c20", h * .06, draw=False)]
    return [grp(out, at, "rise")]


def stone_ruin(x0, base, w, at, c=LILAC, statue=True):
    """A ruined stone city as Fawcett imagined Z (claimed, lilac and dotted): three arches on pillars, a broken column, a statue."""
    out = []
    aw = w / 4.2
    for k in range(3):
        xa = x0 + k * aw * 1.25
        out.append(ln([(xa, base), (xa, base - aw * .9)] + [(xa + aw / 2 + aw / 2 * math.cos(math.radians(a)), base - aw * .9 - aw / 2 * math.sin(math.radians(a))) for a in range(180, -1, -20)]
                      + [(xa + aw, base)], at + .15 * k, c, 3, "claimed", dur=.9))
    cx = x0 + 3 * aw * 1.25 + aw * .2
    out.append(ln([(cx, base), (cx, base - aw * .7), (cx + aw * .3, base - aw * .75), (cx + aw * .3, base)], at + .5, c, 3, "claimed", dur=.6))
    if statue:
        sx = x0 + 3.9 * aw * 1.25
        out += [ln([(sx - aw * .3, base), (sx + aw * .3, base), (sx + aw * .3, base - aw * .25), (sx - aw * .3, base - aw * .25), (sx - aw * .3, base)], at + .7, c, 3, "claimed", dur=.5),
                ln([(sx, base - aw * .25), (sx - aw * .12, base - aw * .9), (sx, base - aw * 1.1), (sx + aw * .12, base - aw * .9), (sx, base - aw * .25)], at + .8, c, 3, "claimed", dur=.6),
                ln([(sx, base - aw * 1.12), (sx, base - aw * 1.18)], at + .9, c, 5, "claimed", dur=.2)]
    return out


def s13():
    """Fawcett: a lilac Z glows; the surveyor at his theodolite before a map with a border drawing itself; an old Portuguese page, and
    above it a lilac dotted mirage of stone arches and a statue."""
    tz, ts, tb, ta, tr = T("s13", "called it Z"), T("s13", "seasoned surveyor"), T("s13", "remote borders"), T("s13", "Portuguese account"), T("s13", "stone arches")
    G = 720
    els = [rect(-40, G, W_ + 80, 400, "#1c1712", "none", 0, 0, -1)]
    els += [gl(889, 230, 160, tz, .45, "lamp"), lab(889, 300, "Z", tz, LILAC, 170, st="serif", fx="pop")]
    els += [poly([(470, 370), (850, 350), (870, 640), (480, 660)], "#e3d3b0", "#8a6a44", 1.5, ts - .2, fx="fade"),
            ln([(520, 420), (600, 470), (650, 450), (720, 520), (800, 500)], ts, RIVER, 2.4, dur=.8, curve=True),
            ln([(520, 560), (600, 540), (700, 600), (820, 580)], ts + .1, RIVER, 2.4, dur=.8, curve=True)]
    els += [ln([(500, 500), (580, 470), (640, 520), (720, 470), (840, 490)], tb, RED, 3, "inferred", dur=1.2), lab(670, 700, "borders", tb + .6, "#ff9a8a", 26)]
    els += fig(300, G, 230, ts, "#1a1410", "hold", 1, hat=True) + theodolite(400, G, 150, ts + .2)
    els += [lab(300, 770, "Percy Fawcett", ts + .5, BONE, 28)]
    els += [poly([(1180, 450), (1480, 440), (1490, 700), (1190, 710)], "#e9dcc0", "#8a6a44", 1.5, ta, fx="pop"),
            {"k": "glyphs", "x": 1205, "y": 470, "w": 260, "h": 210, "rows": 10, "cols": 7, "kind": "latin", "c": "#5a4632", "in": round(ta + .1, 2)}]
    els += chip(1335, 760, "1750s", DIM, ta + .4, 26)
    els += [gl(1330, 300, 230, tr, .3, "lamp")] + stone_ruin(1150, 400, 380, tr)
    els += [lab(1335, 190, "stone arches, a statue", tr + .9, LILAC, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


RIV["araguaia"] = [(-53.2, -17.4), (-52.3, -15.2), (-50.7, -12.8), (-50.1, -10.6), (-49.3, -8.4)]
RIV["teles"] = [(-55.6, -13.6), (-55.9, -11.6), (-56.6, -9.9), (-57.6, -7.4)]
VM = View(-60.0, -48.6, -17.0, -9.0, (90, 120, 1600, 680))


def s14():
    """Mato Grosso: from Cuiaba a dashed route north to Dead Horse Camp, 29 May 1925; the last letter; then lilac dots into the Xingu
    forest that stop at a question mark."""
    v = VM
    t0, t1, t2, t3, t4 = T("s14", "He took his son"), T("s14", "twenty-ninth of May"), T("s14", "no fear"), T("s14", "his last letter"), T("s14", "None of the three")
    els = [rect(-40, -40, W_ + 80, H_ + 80, "#2b3a28", "none", 0, 0, -1)]
    for n in ("xingu", "culuene", "araguaia", "teles"):
        els.append(river(v, n, -1, "#4f8fae", 3, draw=False, op=.9))
    cx, cy = v.p(-56.1, -15.6)
    dx, dy = v.p(-54.58, -11.72)
    els += [pin(cx, cy, "Cuiaba", -1, BONE, a="end", lx=-16)]
    els += [lab(v.p(-57.6, -13.3)[0], v.p(-57.6, -13.3)[1], "Mato Grosso", -1, DIM, 30, st="ital"), lab(v.p(-52.0, -11.0)[0], v.p(-52.0, -11.0)[1], "Upper Xingu", -1, "#9fd0ff", 28, st="ital")]
    for k, (nm, ox) in enumerate((("Percy", -70), ("Jack", 0), ("Raleigh", 74))):
        els += fig(cx + 130 + ox, cy + 90, 54, t0 + .3 * k, "#e8d6b8", None, 1)
        els += [lab(cx + 130 + ox, cy + 124, nm, t0 + .3 * k + .2, DIM, 22)]
    route = [(cx, cy), v.p(-55.8, -14.6), v.p(-55.3, -13.2), v.p(-54.9, -12.3), (dx, dy)]
    els += [ln(route, t0 + .8, GOLD, 3.5, "inferred", dur=2.2, curve=True)]
    els += [pin(dx, dy, "Dead Horse Camp", t1, GOLD, a="end", lx=-16)] + chip(dx - 150, dy + 56, "29 May 1925", GOLD, t1 + .4, 24)
    lx0, ly0 = 1200, 170
    els += [poly([(lx0, ly0), (lx0 + 380, ly0 - 10), (lx0 + 390, ly0 + 230), (lx0 + 6, ly0 + 240)], "#efe4cc", "#8a6a44", 1.5, t2 - .4, fx="pop"),
            {"k": "glyphs", "x": lx0 + 30, "y": ly0 + 30, "w": 320, "h": 70, "rows": 3, "cols": 8, "kind": "latin", "c": "#6a5a44", "in": round(t2 - .3, 2)},
            lab(lx0 + 195, ly0 + 150, "no fear of any failure", t2, "#5a3a22", 30, st="ital", halo=False)]
    els += [ln([(dx + 6, dy - 10), (lx0 + 20, ly0 + 200)], t2 - .3, DIM, 1.5, "inferred", dur=.5)]
    lost = [(dx, dy), v.p(-54.2, -11.3), v.p(-53.8, -10.9), v.p(-53.4, -10.6)]
    els += [ln(lost, t3 + .3, LILAC, 3.5, "claimed", dur=1.8, curve=True)] + qmark(v.p(-53.25, -10.45)[0] + 30, v.p(-53.25, -10.45)[1] - 10, t4, 80)
    return {"base": "map", "cam": CAM, "els": els}


def oval_house(x, ground, w, h, at, fx="pop", c=THATCH, edge=THATCH_D):
    """A large Upper Xingu house in side view: a long, rounded thatch hull down to the ground, a low door."""
    pts = [(x - w / 2, ground)] + [(x + w / 2 * math.cos(math.radians(a)), ground - h * math.sin(math.radians(a)) ** .8) for a in range(170, 9, -10)] + [(x + w / 2, ground)]
    out = [poly(pts, c, edge, 1.5, curve=True)]
    for k in range(1, 4):
        yy = ground - h * k * .24
        hw = w / 2 * (1 - (k * .24) ** 1.4) * .97
        out.append(ln([(x - hw, yy), (x + hw, yy)], 0, edge, 1.2, draw=False, op=.55))
    out.append(rect(x - w * .05, ground - h * .28, w * .1, h * .28, "#2a1d12", "none", 0, 3))
    return [grp(out, at, fx)] if fx else out


def s15():
    """An Upper Xingu town in plan (schematic): forest, a stream; then, as named, the ditch, the plaza and its houses, bridges, ponds,
    and two broad straight roads; the archaeologists with the Kuikuro at the edge."""
    ta, tk, tf = T("s15", "archaeologists came"), T("s15", "Kuikuro people"), T("s15", "Afukaka")
    td, tp, tb, tq, tr = T("s15", "ditches up to"), T("s15", "plazas"), T("s15", "bridges"), T("s15", "ponds"), T("s15", "roads up to fifty")
    rnd = random.Random(15)
    els = []
    for k in range(260):
        x, y = rnd.uniform(-20, W_ + 20), rnd.uniform(-20, H_ + 20)
        els.append(poly(blob(x, y, rnd.uniform(16, 30), rnd.uniform(14, 26), 9, .25, k), ("#203a24", "#284a2c", "#1b3320")[k % 3], "none", 0, -1))
    stream = [(-40, 760), (200, 720), (380, 760), (560, 700), (760, 740), (960, 690), (1160, 730), (1360, 680), (1560, 720), (W_ + 40, 690)]
    els += [ln(stream, -1, "#3f7f9c", 12, curve=True, draw=False), ln(stream, -1, "#6fb3d0", 4, curve=True, draw=False, op=.7)]
    TX, TY = 760, 400
    els += [ln([(TX + 290 * math.cos(math.radians(a)), TY + 230 * math.sin(math.radians(a))) for a in range(150, 391, 8)], td, "#4a3420", 22, dur=1.6, curve=True),
            ln([(TX + 290 * math.cos(math.radians(a)), TY + 230 * math.sin(math.radians(a))) for a in range(150, 391, 8)], td + .1, "#8a6a44", 4, dur=1.6, curve=True)]
    els += [lab(TX - 330, TY - 230, "ditches, up to 5 m deep", td + .6, AMBER, 26, "start")]
    els += [poly(E(TX, TY, 110, 86, 40), "#a08a62", "#e2c27e", 2, tp, fx="fade")]
    for k in range(14):
        a = math.radians(k * 360 / 14)
        hx, hy = TX + 150 * math.cos(a), TY + 118 * math.sin(a)
        els.append(poly(E(hx, hy, 22, 13, 16), THATCH, THATCH_D, 1.2, tp + .3 + .03 * k, fx="pop"))
    els += [lab(TX, TY + 8, "plaza", tp + .4, "#2a1d12", 24, halo=False)]
    road1 = [(TX + 130, TY - 110), (1700, -40)]
    road2 = [(TX - 120, TY + 110), (380, 900)]
    road3 = [(TX + 120, TY + 110), (1250, 900)]
    for k, rd in enumerate((road1, road2, road3)):
        (x0, y0), (x1, y1) = rd
        L = math.hypot(x1 - x0, y1 - y0)
        nx, ny = -(y1 - y0) / L * 26, (x1 - x0) / L * 26
        els += [poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], "#9a8058", "none", 0, tr + .3 * k, fx="fade"),
                ln([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny)], tr + .3 * k, "#e2c27e", 2.5, dur=1.0), ln([(x0 - nx, y0 - ny), (x1 - nx, y1 - ny)], tr + .3 * k, "#e2c27e", 2.5, dur=1.0)]
    els += [lab(1250, 230, "roads, up to 50 m wide", tr + .8, AMBER, 26, "start")]
    for k, (bx, by) in enumerate(((535, 712), (1107, 702))):
        els += [rect(bx - 30, by - 22, 60, 44, "#7a5a3a", "#e2c27e", 2, 4, tb + .25 * k, fx="pop")]
    els += [lab(1240, 800, "bridges", tb + .4, AMBER, 24)]
    for k, (px, py, rx_, ry_) in enumerate(((300, 640, 60, 26), (980, 625, 70, 28), (1460, 640, 54, 24))):
        els += [poly(E(px, py, rx_, ry_, 24), "#3f7f9c", "#9fd0ff", 1.5, tq + .2 * k, fx="pop")]
    els += [lab(300, 600, "ponds", tq + .4, "#9fd0ff", 24)]
    gx = 1450
    els += [rect(gx - 170, 380, 340, 170, "rgba(20,30,20,.75)", "rgba(255,236,206,.25)", 1.5, 12, ta)]
    els += fig(gx - 120, 520, 92, ta + .1, "#e8d6b8", None, 1, hat=True) + fig(gx - 70, 520, 88, ta + .2, "#e8d6b8", "point", 1, hat=True)
    for k in range(3):
        els += fig(gx + 10 + k * 46, 520, 90, tk + .15 * k, "#c98a5a", None, -1)
    els += [ln([(gx + 150, 520), (gx + 150, 410)], tk + .5, "#e8d6b8", 3, draw=False), circ(gx + 150, 408, 6, "#e8c35a", at=tk + .5, fx="pop")]
    els += [lab(gx, 580, "with the Kuikuro", tk + .3, BONE, 26)] + chip(gx, 340, "co-author: Afukaka Kuikuro", GOLD, tf, 22)
    return {"base": "plan", "bg": "#1b2a1c", "north": [1640, 170], "cam": CAM, "els": els}


def s16():
    """One town reconstructed (schematic, earth and thatch): oval houses round a plaza, palisade and ditch, a straight road out of the
    gate, fields and orchards; the dates; the archaeologist's words."""
    td, tq = T("s16", "twelve fifty"), T("s16", "calls it")
    G0 = 400
    els = [rect(-40, G0, W_ + 80, 700, "#4a5a34", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, G0 + 4, 26, -1, "#2a4a2c", seed=31, hi="#3f6a40")
    for k, (x, y, w, h) in enumerate(((300, 520, 300, 90), (1460, 540, 320, 90), (250, 690, 360, 100), (1520, 700, 340, 100))):
        els += [poly(E(x, y, w / 2, h / 2, 24), "#5e7a3a", "#7f9a52", 1.5, -1)]
        els += [ln([(x - w * .4 + j * w * .1, y - h * .3), (x - w * .4 + j * w * .1, y + h * .3)], -1, "#7f9a52", 2, draw=False, op=.6) for j in range(9)]
    els += [poly(E(889, 600, 470, 160, 48), "#3a2a1c", "none", 0, -1), poly(E(889, 600, 440, 148, 48), "#6e5a3a", "none", 0, -1)]
    for k in range(48):
        a = math.radians(180 + k * 3.75)
        x, y = 889 + 420 * math.cos(a), 600 + 140 * math.sin(a)
        els.append(ln([(x, y), (x, y - 30)], -1, "#5a4022", 4, draw=False))
    els += [poly(E(889, 610, 260, 80, 40), "#b49a6a", "#e2c27e", 2, -1)]
    for k in range(9):
        a = math.radians(200 + k * 17.5)
        x, y = 889 + 330 * math.cos(a), 612 + 102 * math.sin(a)
        sc = .75 + .25 * (y - 510) / 200
        els += oval_house(x, y, 120 * sc, 74 * sc, -1, None)
    for k in range(4):
        a = math.radians(20 + k * 45)
        x, y = 889 + 340 * math.cos(a), 616 + 110 * math.sin(a)
        els += oval_house(x, y, 150, 92, -1, None)
    els += [poly([(830, 760), (948, 760), (1300, 1040), (480, 1040)], "#a08a62", "#e2c27e", 1.5, -1),
            poly([(860, 470), (918, 470), (1050, 300), (1000, 300)], "#9a8462", "#e2c27e", 1.2, -1, op=.8)]
    els += fig(858, 630, 40, -1, "#2a1d14") + fig(936, 598, 36, -1, "#2a1d14", None, -1) + fig(900, 860, 70, -1, "#2a1d14")   # in the open plaza
    els += chip(889, 210, "about 1250 to 1650 CE", GOLD, td, 30)
    els += chip(889, 300, "not cities, but urbanism", BONE, tq + .4, 30) + [lab(1180, 305, "Heckenberger", tq + .8, DIM, 24, "start")]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [1500, 180, 18], "cam": CAM, "els": els}


def s17():
    """Stone against earth: the lilac dotted city of the dream at left, solid earthworks at right; 'Z?' between."""
    tz, ts, te = T("s17", "So was this Z"), T("s17", "looking for stone"), T("s17", "The towns were")
    els = [rect(-40, 640, W_ + 80, 400, "#1c1712", "none", 0, 0, -1), ln([(889, 160), (889, 760)], -1, "rgba(255,236,206,.15)", 2, "inferred", draw=False)]
    els += qmark(889, 330, tz, 90) + [lab(830, 330, "Z", tz, LILAC, 90, st="serif", fx="pop")]
    els += stone_ruin(160, 640, 560, -1, "rgba(201,193,238,.25)")
    els += [gl(440, 460, 260, ts, .3, "lamp")] + stone_ruin(160, 640, 560, ts)
    els += [lab(440, 720, "stone", ts + .8, LILAC, 34, st="serif")]
    E0 = 640
    earth = [(1000, E0), (1060, E0), (1090, E0 + 60), (1170, E0 + 60), (1200, E0), (1250, E0), (1290, E0 - 40), (1400, E0 - 40), (1440, E0), (1700, E0)]
    els += [poly(earth + [(1700, 800), (1000, 800)], "#2e261c", "rgba(226,194,126,.25)", 2, -1)]
    els += [poly(earth + [(1700, 800), (1000, 800)], "#6e5536", "#e2c27e", 2, te, fx="fade")]
    els += hut(1345, E0 - 40, 110, 110, te + .3, THATCH, THATCH_D)
    els += [poly([(1480, E0 - 2), (1700, E0 - 2), (1700, E0 + 10), (1470, E0 + 10)], "#a08a62", "none", 0, te + .5, fx="fade"), lab(1590, E0 + 50, "road", te + .6, DIM, 22),
            lab(1130, E0 + 100, "ditch", te + .6, DIM, 22), lab(1345, E0 + 70, "mound", te + .6, DIM, 22)]
    els += [lab(1340, 400, "earth", te + .4, AMBER, 34, st="serif")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · A counterfeit paradise?
def forest_section(G, at=-1, seed=3, n=11, x0=60, x1=1720, hmin=230, hmax=320, palms=True):
    """A dense rainforest in side view standing on the ground line G: back crowns, trees, palms, front crowns."""
    rnd = random.Random(seed)
    els = crown_row(x0, x1, G - hmax * .55, 40, at, "#1b3322", seed=seed, hi="#29482f")
    for k in range(n):
        x = x0 + (x1 - x0) * (k + .5) / n + rnd.uniform(-30, 30)
        els += tree(x, G, rnd.uniform(hmin, hmax), at, ("#24452b", "#2c5232", "#2f5a34")[k % 3], seed=seed + k * 7)
    if palms:
        for k in range(4):
            els += palm(x0 + 120 + k * (x1 - x0 - 240) / 3 + rnd.uniform(-40, 40), G, rnd.uniform(150, 200), at)
    els += crown_row(x0, x1, G, 26, at, "#2f5a34", seed=seed + 50, hi="#4f8a50")
    return els


def s18():
    """The rainforest cut open: a lush canopy over a thin dark topsoil and deep pale soil; rain washes small dots of goodness down."""
    tc, ta, tp, tr = T("s18", "counterfeit paradise"), T("s18", "Her argument"), T("s18", "Most soils"), T("s18", "washed out")
    G = 470
    layers = [{"d": 0, "c": "#3a2a1e", "t": ""}, {"d": 24, "c": "#c98a4a", "t": ""}, {"d": 180, "c": "#b9783e", "t": ""}, {"d": 330, "c": "#a8693a", "t": ""}]
    els = forest_section(G)
    els += chip(889, 150, "a counterfeit paradise?", LILAC, tc, 30)
    els += [lab(1560, 420, "lush forest", ta, LEAF_H, 30, st="serif")]
    els += [lab(889, 640, "poor soil", tp, "#2a1608", 38, st="serif", halo=False), lab(889, 684, "old, acid, washed out", tp + .4, "#3a2010", 28, halo=False)]
    rnd = random.Random(4)
    for k in range(40):
        x, y = rnd.uniform(80, 1700), rnd.uniform(120, 380)
        if abs(x - 889) < 240 and y < 190:          # no rain across the chip
            y += 90
        els.append(ln([(x, y), (x - 8, y + 26)], tr + .02 * k, "#bfe6f5", 1.8, draw=False, op=.7))
    for k, x in enumerate((360, 700, 1060, 1400)):
        els += [arr([(x, G + 40), (x, G + 290)], tr + .4 + .2 * k, BLUE, 3, curve=False, dur=1.0)]
        els += [circ(x + 18, G + 70 + 60 * j, 5, AU, at=tr + .6 + .2 * k + .25 * j, fx="pop") for j in range(4)]
    return {"base": "section", "tod": "day", "ground": G, "lx": 2000, "layers": layers, "cam": CAM, "els": els}


def s27_add():
    """Cultivated: black earth spreads under two clearings with huts; three trees turn gold."""
    t = T("s27", "A cultivated one")
    G = 470
    out = []
    for k, (x, w) in enumerate(((520, 260), (1250, 300))):
        out += [poly([(x - w / 2, G), (x + w / 2, G), (x + w * .42, G + 90), (x - w * .42, G + 90)], TP, "none", 0, t - 1.2 + .3 * k, fx="fade")]
        out += hut(x - 40, G, 60, 60, t - 1.0 + .3 * k, THATCH_D, "#5a4020") + hut(x + 40, G, 52, 52, t - .9 + .3 * k, THATCH_D, "#5a4020")
    for k, x in enumerate((300, 900, 1550)):
        out += [poly(blob(x, G - 230, 80, 50, 18, .15, 70 + k), "none", GOLD, 4, t + .2 * k, fx="draw")]
    out += chip(889, 232, "cultivated", GOLD, t + .5, 34)
    return out


def armchair(x, ground, s, at):
    out = [rect(x - 70 * s, ground - 60 * s, 140 * s, 50 * s, "#7a4a30", "#c9a46a", 1.5, 8), rect(x - 70 * s, ground - 150 * s, 140 * s, 95 * s, "#8a5a38", "#c9a46a", 1.5, 14),
           rect(x - 92 * s, ground - 100 * s, 30 * s, 90 * s, "#6a3e26", "#c9a46a", 1.5, 10), rect(x + 62 * s, ground - 100 * s, 30 * s, 90 * s, "#6a3e26", "#c9a46a", 1.5, 10),
           ln([(x - 60 * s, ground - 10 * s), (x - 60 * s, ground)], 0, "#3a2414", 5, draw=False), ln([(x + 60 * s, ground - 10 * s), (x + 60 * s, ground)], 0, "#3a2414", 5, draw=False)]
    return [grp(out, at, "rise")]


def s19():
    """Wealth in the trees: one big tree full of small gold dots, the soil under it with three; an armchair and a cabinet stuffed with
    coins."""
    tw, tf = T("s19", "keeps its wealth"), T("s19", "savings are all")
    G = 700
    els = [rect(80, G, 1000, 120, "#c98a4a", "none", 0, 0, -1), rect(80, G, 1000, 14, "#3a2a1e", "none", 0, 0, -1)]
    els += [ln([(560, G), (560, G - 330)], -1, "#7a5a3a", 30, draw=False), ln([(560, G - 250), (470, G - 360)], -1, "#7a5a3a", 14, draw=False),
            ln([(560, G - 270), (660, G - 380)], -1, "#7a5a3a", 14, draw=False)]
    for k, (ox, oy, rx_, ry_) in enumerate(((-120, -420, 150, 90), (110, -430, 160, 95), (0, -500, 170, 90), (-40, -380, 140, 70), (90, -360, 120, 60))):
        els.append(poly(blob(560 + ox, G + oy, rx_, ry_, 18, .12, 30 + k), ("#2c5232", "#336039", "#2f5a34")[k % 3], "none", 0, -1))
    rnd = random.Random(19)
    for k in range(36):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 1)
        x, y = 560 + 230 * r * math.cos(a), G - 440 + 90 * r * math.sin(a)
        els.append(circ(x, y, 7, AU, "#7a5a14", 1, at=tw + .03 * k, fx="pop"))
    for k in range(6):
        els.append(circ(560, G - 40 - 50 * k, 7, AU, "#7a5a14", 1, at=tw + 1.2 + .05 * k, fx="pop"))
    els += [circ(x, G + 50, 7, AU, "#7a5a14", 1, at=tw + 1.6 + .1 * k, fx="pop") for k, x in enumerate((300, 640, 900))]
    els += [lab(560, 160, "wealth in the trees", tw + .5, GOLD, 32, st="serif"), lab(900, 772, "the soil: little", tw + 1.8, "#2a1608", 32, st="serif", halo=False)]
    els += armchair(1300, G, 1.3, tf)
    els += [rect(1480, G - 230, 170, 230, "#6a3e26", "#c9a46a", 1.5, 6, tf + .2, fx="rise"), ln([(1565, G - 225), (1565, G - 5)], tf + .2, "#c9a46a", 1.5, draw=False),
            circ(1550, G - 120, 5, "#c9a46a", at=tf + .2), circ(1580, G - 120, 5, "#c9a46a", at=tf + .2)]
    for k, (x, y) in enumerate(((1240, G - 70), (1290, G - 75), (1340, G - 70), (1380, G - 120), (1215, G - 120), (1500, G - 236), (1540, G - 238), (1600, G - 236), (1640, G - 234))):
        els.append(circ(x, y, 10, AU, "#7a5a14", 1.5, at=tf + .5 + .08 * k, fx="pop"))
    els += [lab(1420, 400, "savings in the furniture", tf + .8, GOLD, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def crop(x, ground, h, at, c="#6fae4a"):
    out = [ln([(x, ground), (x, ground - h)], 0, "#4f8a3a", 3, draw=False)]
    for k in range(3):
        y = ground - h * (.3 + .25 * k)
        s_ = 1 if k % 2 else -1
        out.append(ln([(x, y), (x + s_ * h * .25, y - h * .12), (x + s_ * h * .4, y - h * .05)], 0, c, 3, curve=True, draw=False))
    return [grp(out, at, "rise")]


def s20():
    """Slash and burn: felled trunks, fire, ash, a row of crops; three harvest bars shrink; 'spent'."""
    tb, ta, ts = T("s20", "Burn the trees"), T("s20", "feeds your crops"), T("s20", "then the field")
    G = 640
    els = [rect(-40, G, W_ + 80, 400, "#4a3a28", "none", 0, 0, -1)] + forest_section(G, -1, 7, 4, 40, 300, 240, 300, False) + forest_section(G, -1, 8, 3, 1000, 1240, 240, 300, False)
    for k, (x, a) in enumerate(((380, -8), (520, 6), (660, -4), (800, 10))):
        els.append(ln([(x - 70, G - 8 + a * .5), (x + 70, G - 8 - a * .5)], -1, "#5a3a22", 12, draw=False))
    for k, x in enumerate((420, 560, 700, 840)):
        els += [gl(x, G - 40, 120, tb + .2 * k, .7, "fire")] + [poly([(x - 18, G - 10), (x, G - 70), (x + 18, G - 10)], "#ff9a4a", "#ffd08a", 1, tb + .2 * k, fx="pop", curve=True)]
    rnd = random.Random(20)
    els += [circ(rnd.uniform(360, 900), rnd.uniform(G - 6, G + 20), 3, "#9a948c", at=tb + 1.2 + .03 * k, fx="pop") for k in range(30)]
    for k in range(7):
        els += crop(380 + k * 80, G, 90 + (k % 2) * 16, ta + .1 * k)
    bx, bw = 1360, 70
    for k, (h, t_) in enumerate(((240, ta + .6), (150, ta + 1.2), (60, ts - .6))):
        x = bx + k * 110
        els += [rect(x - bw / 2, G - h, bw, h, "#6fae4a", "#cfe6a0", 1.5, 4, t_, fx="fill"), lab(x, G + 40, "year %d" % (k + 1), t_, BONE, 26)]
    els += chip(bx + 220, G - 120, "spent", "#e0a080", ts, 28)
    els += [lab(1470, 360, "harvest", ta + .6, BONE, 28)]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [1600, 150, 18], "cam": CAM, "els": els}


def s21():
    """The ceiling: small villages and their people under a dashed red line; above it, a big town in lilac dashes that cannot rise."""
    tc = T("s21", "a ceiling")
    G = 680
    els = [rect(-40, G, W_ + 80, 400, "#1c1712", "none", 0, 0, -1)]
    for k, x in enumerate((260, 650, 1040, 1430)):
        els += hut(x - 40, G, 50, 52, .2 + .15 * k) + hut(x + 10, G, 58, 60, .25 + .15 * k) + hut(x + 60, G, 46, 48, .3 + .15 * k)
        els += fig(x - 70, G, 44, .4 + .15 * k, "#e8d6b8") + fig(x + 100, G, 42, .45 + .15 * k, "#e8d6b8", None, -1)
    els += [ln([(80, 520), (1700, 520)], tc - .3, RED, 4, "inferred", dur=1.2)]
    town = [(500, 520), (500, 300), (620, 300), (620, 240), (700, 220), (780, 240), (780, 300), (980, 300), (980, 200), (1080, 200), (1080, 300), (1280, 300), (1280, 520)]
    els += [ln(town, tc + .5, LILAC, 3, "claimed", dur=1.4)]
    els += chip(889, 160, "a ceiling?", LILAC, tc + .2, 32)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s22():
    """Two soil columns: ordinary soil (thin dark top, pale below) and terra preta (black from the top down), each under a strip of
    ground; a tiny village on the black earth."""
    to, tt = T("s22", "look closer"), T("s22", "terra preta")
    G = 330
    els = []
    for x0, w, kind, t_ in ((150, 340, "ord", to), (900, 340, "tp", tt - 1.0)):     # ord far enough left to leave the push-in
        els += [rect(x0, G, w, 440, "#c99a5a", "rgba(255,236,206,.35)", 1.5, 0, t_, fx="fill"),
                rect(x0, G, w, 440, "url(#k-speck)", "none", 0, 0, t_)]
        if kind == "ord":
            els += [rect(x0, G, w, 22, "#3a2a1e", "none", 0, 0, t_)]
        else:
            els += [rect(x0, G, w, 330, TP, "none", 0, 0, t_ + .3, fx="fill"), rect(x0, G + 330, w, 30, "#5a4030", "none", 0, 0, t_ + .3)]
        els += [crop(x0 + 40 + 60 * k, G, 46, t_ + .4) for k in range(5)][0:0]
        for k in range(5):
            els += crop(x0 + 40 + 64 * k, G, 46, t_ + .4)
    els += hut(1000, G, 56, 56, tt + .3) + hut(1080, G, 64, 64, tt + .4) + hut(1160, G, 50, 50, tt + .5)
    els += [lab(320, G - 60, "ordinary soil", to + .3, DIM, 28), lab(1070, G - 96, "terra preta", tt, GOLD, 34, st="serif")]   # above, clear of the captions
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s23_add():
    """Inside the black earth: charcoal, pottery, bone and food scraps pop as named; a compost heap; the 70 times bars."""
    tc, tp, tb, tf, th, t70 = T("s23", "charcoal"), T("s23", "broken pottery"), T("s23", "bone"), T("s23", "food"), T("s23", "compost heap"), T("s23", "seventy times")
    G = 330
    rnd = random.Random(23)
    out = []
    for k in range(18):
        x, y = rnd.uniform(920, 1220), rnd.uniform(G + 30, G + 310)
        out.append(poly([(x - 9, y - 4), (x + 3, y - 9), (x + 10, y + 2), (x - 2, y + 8)], "#0a0806", "#5a5048", 1, tc + .04 * k, fx="pop"))
    for k in range(9):
        x, y = rnd.uniform(930, 1210), rnd.uniform(G + 40, G + 300)
        out.append(poly([(x - 12, y + 6), (x + 2, y - 10), (x + 14, y + 4)], "#c4602e", "#f0a070", 1, tp + .06 * k, fx="pop"))
    for k in range(7):
        x, y = rnd.uniform(930, 1210), rnd.uniform(G + 40, G + 300)
        out.append(ln([(x - 10, y), (x + 10, y - 3)], tb + .06 * k, "#f2ead8", 4, draw=False))
    for k in range(10):
        x, y = rnd.uniform(930, 1210), rnd.uniform(G + 30, G + 280)
        out.append(circ(x, y, 4, ("#7a9a3a", "#a86a3a")[k % 2], at=tf + .05 * k, fx="pop"))
    out += [poly([(1210, G), (1250, G - 40), (1300, G - 52), (1350, G - 36), (1380, G)], "#4a3626", "#8a6a44", 1.5, th, fx="rise")]
    out += [circ(1260 + 18 * k, G - 30 - (k % 2) * 10, 5, ("#7a9a3a", "#c4602e", "#f2ead8")[k % 3], at=th + .2 + .05 * k, fx="pop") for k in range(6)]
    out += [lab(1300, G - 80, "a compost heap", th + .3, BONE, 24)]
    bx = 1450
    out += [rect(bx, G + 300, 50, 4, "#c99a5a", "none", 0, 1, t70), rect(bx + 110, G + 20, 50, 284, "#0a0806", "#8a8078", 1.5, 2, t70 + .3, fx="fill")]
    out += [lab(bx + 25, G + 330, "around it", t70, DIM, 22), lab(bx + 135, G - 10, "up to 70 times", t70 + .6, BONE, 24), lab(bx + 135, G - 42, "charcoal", t70 + .6, DIM, 22)]
    return out


def s24():
    """The Kuikuro make dark earth on purpose (schematic, by day): big oval houses round a plaza; a midden of food scraps and ash grows;
    a figure spreads ash over a field; a ring of charcoal round the base of a fruit tree."""
    tk, tm, ta, tc = T("s24", "Kuikuro still make"), T("s24", "heap food scraps"), T("s24", "spread ash"), T("s24", "set charcoal")
    G = 560
    els = [rect(-40, G - 60, W_ + 80, 600, "#6e7a44", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, G - 100, 30, -1, "#2a4a2c", seed=41, hi="#3f6a40")
    els += [poly(E(700, G + 60, 420, 90, 40), "#c9b48a", "none", 0, -1)]
    for k, (x, y, w, h) in enumerate(((380, G - 10, 180, 100), (600, G - 30, 160, 90), (820, G - 30, 160, 90), (1030, G - 10, 180, 100))):
        els += oval_house(x, y, w, h, -1, None)
    els += oval_house(300, G + 150, 230, 120, -1, None) + oval_house(1110, G + 160, 240, 124, -1, None)
    els += fig(640, G + 90, 60, -1, "#2a1d14") + fig(760, G + 80, 56, -1, "#2a1d14", None, -1)
    mx = 1330
    els += [poly([(mx - 80, G + 120), (mx - 40, G + 70), (mx + 10, G + 56), (mx + 60, G + 72), (mx + 90, G + 120)], "#4a3626", "#8a6a44", 1.5, tm, fx="rise")]
    rnd = random.Random(24)
    els += [circ(mx + rnd.uniform(-60, 70), G + rnd.uniform(70, 110), 4, ("#7a9a3a", "#c4602e", "#9a948c")[k % 3], at=tm + .3 + .04 * k, fx="pop") for k in range(14)]
    els += [lab(mx, G + 160, "midden", tm + .5, BONE, 24)]
    fx0 = 1450
    els += [rect(fx0, G + 210, 280, 90, "#5a4a2a", "none", 0, 4, -1)] + [crop(fx0 + 20 + 40 * k, G + 250, 40, -1) for k in range(7)][0:0]
    for k in range(7):
        els += crop(fx0 + 20 + 40 * k, G + 250, 40, -1)
    els += fig(fx0 - 30, G + 250, 80, ta - .3, "#2a1d14", "spread", 1)
    els += [circ(fx0 + rnd.uniform(0, 260), G + rnd.uniform(150, 240), 3, "#bdb6ac", at=ta + .05 * k, fx="pop") for k in range(22)]
    els += [lab(fx0 + 140, G + 330, "ash on the field", ta + .5, BONE, 24)]
    tx = 160
    els += tree(tx, G + 260, 260, -1, "#2f5a34", seed=24, w=180)
    els += [circ(tx + 46 * math.cos(math.radians(a)), G + 262 + 12 * math.sin(math.radians(a)), 5, "#0a0806", at=tc + .02 * k, fx="pop") for k, a in enumerate(range(0, 360, 20))]
    els += [lab(tx + 20, G + 310, "charcoal", tc + .4, BONE, 24)]
    els += chip(889, 150, "Kuikuro: eegepe", GOLD, tk, 30) + [lab(889, 215, "dark earth, on purpose", tk + .5, BONE, 26)]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [1600, 120, 18], "cam": CAM, "els": els}


def tree_icon(x, y, s, c, at, fx="pop", edge=None):
    return [grp([ln([(x, y), (x, y - 14 * s)], 0, "#6b4a30", 3 * s, draw=False), circ(x, y - 26 * s, 15 * s, c, edge or "none", 1.5 if edge else 0)], at, fx)]


def s25():
    """A hundred trees, 20 by 5: then half of them turn gold, the 227 kinds that make up half of all the trees."""
    t0, t1 = T("s25", "sixteen thousand"), T("s25", "two hundred and twenty-seven")
    els = []
    x0, y0, dx, dy = 290, 270, 63, 82
    for k in range(100):
        r, c = divmod(k, 20)
        els += tree_icon(x0 + c * dx, y0 + r * dy, 1.0, "#3f6a40", round(.2 + .01 * k, 2))
    for k in range(50):
        r, c = divmod(k, 20)
        els += tree_icon(x0 + c * dx, y0 + r * dy, 1.0, AU, round(t1 + .5 + .02 * k, 2))
    els += [lab(889, 175, "16,000 kinds of tree", t0, BONE, 32, st="serif")]
    els += bracket(x0 - 20, x0 + 19 * dx + 20, y0 + 4 * dy + 30, t1 + 1.6, None, AU, False)
    els += [lab(889, y0 + 4 * dy + 80, "half of all trees: just 227 kinds", t1 + 1.9, GOLD, 30)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def brazil_nut(x, ground, h, at):
    """A Brazil nut tree: a tall straight trunk, an umbrella crown above the canopy, round woody pods."""
    out = [ln([(x, ground), (x, ground - h * .78)], 0, "#8a6a4a", h * .045, draw=False),
           ln([(x, ground - h * .7), (x - h * .18, ground - h * .82)], 0, "#8a6a4a", h * .02, draw=False),
           ln([(x, ground - h * .7), (x + h * .2, ground - h * .84)], 0, "#8a6a4a", h * .02, draw=False)]
    for k, (ox, oy, rx_) in enumerate(((-.2, -.86, .17), (.2, -.87, .17), (0, -.93, .2), (-.08, -.82, .14), (.1, -.8, .13))):
        out.append(poly(blob(x + ox * h, ground + oy * h, rx_ * h, rx_ * h * .5, 16, .12, 90 + k), ("#2f5a34", "#3a6a3c", "#336039")[k % 3], GOLD, 2))
    out += [circ(x + (k - 1.5) * h * .07, ground - h * .78, h * .022, "#7a4a24", "#3a2414", 1) for k in range(4)]
    return [grp(out, at, "rise")]


def acai(x, ground, h, at):
    """An acai palm: a clump of slender stems with feathery fronds and hanging bunches of dark purple fruit."""
    out = []
    for k, (dx, hh, lean) in enumerate(((-18, 1.0, -.04), (6, .9, .03), (24, .8, .07))):
        tx, ty = x + dx + lean * h * hh, ground - h * hh
        out.append(ln([(x + dx, ground), (tx, ty)], 0, "#6a5a40", 4, draw=False))
        for j in range(8):
            a = math.radians(-165 + j * 21)
            L = h * .2
            out.append(ln([(tx, ty), (tx + math.cos(a) * L * .6, ty + math.sin(a) * L * .4 - 4), (tx + math.cos(a) * L, ty + math.sin(a) * L * .5 + 12)], 0, "#3a6a3c", 3, curve=True, draw=False))
        out += [circ(tx - 8 + 5 * m, ty + 16 + 4 * (m % 2), 4, "#4a2a5a", GOLD, .8) for m in range(4)]
    return [grp(out, at, "rise")]


def s26_add():
    """The Brazil nut tree and the acai palm, gold, at either side; 'domesticated'; two bars, 1 and 5."""
    tb, tp, t5 = T("s26", "Brazil nut"), T("s26", "acai"), T("s26", "five times")
    out = brazil_nut(150, 740, 520, tb) + [lab(150, 780, "Brazil nut", tb + .3, GOLD, 28)]
    out += acai(1640, 740, 430, tp) + [lab(1640, 780, "acai palm", tp + .3, GOLD, 28)]
    out += chip(1340, 175, "domesticated by people", GOLD, tp + .6, 26)
    out += [rect(760, 716, 60, 20, "#3f6a40", "none", 0, 3, t5, fx="fill"), rect(760, 750, 300, 20, AU, "none", 0, 3, t5 + .4, fx="fill"),
            lab(745, 733, "others", t5, DIM, 26, "end"), lab(745, 767, "domesticated", t5 + .4, GOLD, 26, "end"), lab(1075, 767, "5 times likelier", t5 + .8, GOLD, 28, "start")]
    return out



# ================================================================== CHAPTER 4 · Causeways in the floodplain
def forest_island(x, y, rx, ry, at=-1, seed=1, dark=False):
    """A round clump of forest standing out of the flooded savannah, seen obliquely."""
    out = [poly(E(x, y + ry * .35, rx * 1.05, ry * .45, 24), "#3e4a2c", "none", 0, at)]
    rnd = random.Random(seed)
    for k in range(7):
        ox, oy = rnd.uniform(-.6, .6) * rx, rnd.uniform(-.5, .1) * ry
        out.append(poly(blob(x + ox, y + oy, rx * rnd.uniform(.35, .55), ry * rnd.uniform(.45, .7), 14, .18, seed * 10 + k), ("#2a4a2c", "#2f5a34", "#24452b")[k % 3] if not dark else "#1e3524", "none", 0, at))
    out.append(poly(blob(x - rx * .2, y - ry * .35, rx * .3, ry * .22, 10, .2, seed + 77), "#4f8a50", "none", 0, at, op=.5))
    return out


def s28():
    """The Llanos de Mojos in the wet season: grass, sheets of water, round forest islands; a forested mound with a trench and two
    diggers; the dates; then, under the trees, dashed outlines of what the forest hid."""
    td, tc, th = T("s28", "archaeologists had dug"), T("s28", "Casarabe culture"), T("s28", "forest hid")
    HZ = 330
    els = [rect(-40, HZ, W_ + 80, 760, "#7a8a4a", "none", 0, 0, -1)]
    rnd = random.Random(28)
    for k in range(9):
        y = rnd.uniform(HZ + 20, 760)
        f = (y - HZ) / 430
        els.append(poly(blob(rnd.uniform(0, W_), y, 90 + 260 * f, 8 + 30 * f, 16, .3, k), "#7fa6b8", "rgba(255,255,255,.25)", 1, -1))
    els += [rect(-40, HZ - 2, W_ + 80, 6, "#5a6a3a", "none", 0, 0, -1)]
    for k, (x, y, r) in enumerate(((180, 360, 40), (420, 350, 28), (1330, 356, 36), (1560, 370, 50), (300, 470, 70), (1480, 500, 90), (120, 620, 110), (1680, 640, 120))):
        els += forest_island(x, y, r, r * .55, -1, k + 3)
    MX, MY = 880, 520
    els += [poly([(MX - 330, MY + 70), (MX - 240, MY - 10), (MX + 230, MY - 20), (MX + 340, MY + 70)], "#6a5a3a", "none", 0, -1)]
    els += forest_island(MX, MY - 60, 330, 120, -1, 9)
    els += [poly([(MX + 150, MY + 70), (MX + 175, MY + 14), (MX + 260, MY + 10), (MX + 290, MY + 70)], "#3a2a1c", "#c9a46a", 1.5, td, fx="fade")]
    els += fig(MX + 200, MY + 58, 40, td + .2, "#e8d6b8", "hold", 1, hat=True) + fig(MX + 250, MY + 58, 38, td + .3, "#e8d6b8", None, -1)
    els += chip(MX + 230, MY + 120, "dug since 1908", BONE, td + .5, 24)
    els += chip(889, 170, "Casarabe culture, about 500 to 1400 CE", GOLD, tc, 28)
    els += [ln([(MX - 120, MY - 40), (MX - 120, MY - 120), (MX + 60, MY - 120), (MX + 60, MY - 40)], th, BONE, 2.5, "inferred", dur=.8),
            ln([(MX + 340, MY + 50), (1700, MY + 140)], th + .4, BONE, 3, "inferred", dur=1.2), ln([(MX - 330, MY + 50), (-40, MY + 160)], th + .5, BONE, 3, "inferred", dur=1.2)]
    els += [lab(MX - 30, MY - 140, "hidden?", th + .9, BONE, 24)]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [1450, 170, 18], "cam": CAM, "els": els}


def side_plane(x, y, s, at):
    """A small survey aircraft in side view."""
    out = [poly([(x - s, y), (x + s * .8, y - s * .04), (x + s, y + s * .06), (x + s * .8, y + s * .14), (x - s * .9, y + s * .12)], "#e9e2d6", "none", curve=True),
           poly([(x - s * .9, y), (x - s, y - s * .32), (x - s * .78, y - s * .3), (x - s * .66, y)], "#e9e2d6", "none"),
           poly([(x - s * .1, y + s * .04), (x + s * .3, y + s * .04), (x + s * .1, y + s * .36), (x - s * .2, y + s * .36)], "#d9d2c6", "none"),
           circ(x + s * .55, y + s * .02, s * .07, "#9fd0ff"), rect(x - s * .08, y + s * .12, s * .16, s * .1, "#2a2622", "none", 0, 2)]
    return [grp(out, at, None)] if at == -1 else [grp(out, at, "pop")]


def s29():
    """Lidar in side view: an aircraft; pulses fan down; most stop in the crowns, a few reach the ground; sunlight flecks; then the
    ground points join into a profile that shows a mound and a raised causeway, and the trees dim away."""
    t19, tl, tm, tf, ts, tk = T("s29", "twenty nineteen"), T("s29", "A laser beneath"), T("s29", "Most hit leaves"), T("s29", "a few slip"), T("s29", "sunlight dappling"), T("s29", "Keep only those")
    G = 690
    def gy(x):                                   # the ground profile: flat, a terrace and cone, a raised causeway
        y = G
        if 520 < x < 1080:
            y -= 60 * min(1, (x - 520) / 60, (1080 - x) / 60)
        if 700 < x < 900:
            y -= 120 * (1 - abs(x - 800) / 100)
        if 1300 < x < 1440:
            y -= 26 * min(1, (x - 1300) / 30, (1440 - x) / 30)
        return y
    prof = [(x, gy(x)) for x in range(80, 1710, 10)]
    BG = "#17120e"
    els = [rect(-40, -40, W_ + 80, H_ + 80, BG, "none", 0, 0, -1), poly(prof + [(1710, 1000), (80, 1000)], "#3a2c20", "none", 0, -1)]
    trees_x = [130 + 115 * k for k in range(14)]
    crowns = []
    for k, x in enumerate(trees_x):
        h = 210 + (k * 37) % 70
        crowns.append((x, gy(x) - h * .8, h))
        els += tree(x, gy(x), h, -1, ("#24452b", "#2c5232", "#2f5a34")[k % 3], seed=k + 50, w=130)
    els += side_plane(889, 150, 70, -1) + chip(1040, 140, "2019", SCANC, t19, 26)
    rnd = random.Random(29)
    hits, gaps = [], []
    for k, (x, y, h) in enumerate(crowns):
        hits.append((x + rnd.uniform(-30, 30), y + rnd.uniform(-20, 10)))
    for x in (185, 415, 645, 1110, 1245, 1480, 1590):
        gaps.append((x, gy(x)))
    for k, (x, y) in enumerate(hits):
        els += [ln([(889, 172), (x, y)], tm + .08 * k, SCANC, 1.4, dur=.35, op=.8), circ(x, y, 6, SCANC, at=tm + .08 * k + .35, fx="pop")]
    for k, (x, y) in enumerate(gaps):
        els += [ln([(889, 172), (x, y)], tf + .15 * k, "#e6f3ff", 2, dur=.45), circ(x, y, 7, "#e6f3ff", SCANC, 1.5, at=tf + .15 * k + .45, fx="pop")]
    els += [poly(E(x, G + 6, 26, 6, 14), "rgba(255,226,150,.7)", "none", 0, ts + .1 * k, fx="pop") for k, (x, _) in enumerate(gaps)]
    els += [poly([(-40, 175), (-40, G - 3)] + [(x, y - 3) for x, y in prof] + [(W_ + 40, G - 3), (W_ + 40, 175)], BG, "none", 0, tk, dur=1.0)]   # edge to edge
    els += [ln(prof, tk + .4, AU, 4, dur=1.2), lab(800, gy(800) - 30, "mound", tk + 1.0, GOLD, 26), lab(1370, gy(1370) - 26, "causeway", tk + 1.2, GOLD, 26)]
    els += [lab(240, 120, "lidar", tl, SCANC, 30, st="serif")][0:0]
    return {"base": "dark", "cam": CAM, "els": els}


def _footprint(cx, cy, r, seed, n=11):
    rnd = random.Random(seed)
    return [(cx + r * rnd.uniform(.86, 1.08) * math.cos(2 * math.pi * k / n + .3), cy + r * rnd.uniform(.86, 1.08) * math.sin(2 * math.pi * k / n + .3)) for k in range(n)]


def s30():
    """Lidar plan of the two towns, to scale with each other (250 units = 1 km): Cotoca 147 ha and Landivar 315 ha, their mounds, then
    three concentric rings of moat and rampart round each."""
    tc, tl, tr = T("s30", "Cotoca"), T("s30", "Landivar"), T("s30", "three lines")
    U = 250.0                                         # units per km
    els = [rect(-40, -40, W_ + 80, H_ + 80, "#2a2824", "none", 0, 0, -1)]
    rnd = random.Random(30)
    for k in range(40):
        y = rnd.uniform(0, H_)
        els.append(ln([(-40, y), (W_ + 40, y + rnd.uniform(-30, 30))], -1, "#34312c", 2, draw=False))
    for name, cx, cy, ha, t_, seed in (("Cotoca, 147 ha", 520, 470, 147, tc, 3), ("Landívar, 315 ha", 1190, 470, 315, tl, 5)):
        r = math.sqrt(ha / 100.0 / math.pi) * U
        outer = _footprint(cx, cy, r, seed)
        els += [poly(outer, "#57524a", "#c9c1b0", 2, t_, fx="fade")]
        els += [poly(_footprint(cx, cy, r * .42, seed + 1, 8), "#6e675c", "#d8cdb4", 1.5, t_ + .2, fx="pop")]
        for j in range(4):
            a = 2 * math.pi * j / 4 + .4
            x, y = cx + r * .2 * math.cos(a), cy + r * .2 * math.sin(a)
            els.append(rect(x - 16, y - 10, 32, 20, "#b9ad92", "#efe6d2", 1, 2, t_ + .4 + .1 * j, fx="pop"))
        els += [circ(cx + r * .05, cy - r * .02, 14, "#d9c79a", "#ffffff", 1.5, at=t_ + .5, fx="pop")]
        els += [lab(cx, cy + r + 46, name, t_ + .3, GOLD, 30)]
        for j, f in enumerate((1.0, .82, .64)):
            ring = _footprint(cx, cy, r * f, seed)
            els.append(ln(ring + [ring[0]], tr + .3 * j + (0 if seed == 3 else .15), "#9fd0ff", 3, dur=1.0))
    els += [ln([(1440, 790), (1440 + .5 * U, 790)], .3, BONE, 2.5, draw=False), lab(1440 + .25 * U, 774, "500 m", .3, BONE, 24)]
    els += [lab(880, 150, "three moat-and-rampart rings", tr + 1.0, "#9fd0ff", 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s31():
    """To scale (16 units = 1 m): a conical earthen pyramid 22 m tall on its terrace and a seven-storey building of the same height;
    a person."""
    tc, tb = T("s31", "a cone of earth"), T("s31", "seven-storey")
    G, M = 720, 16.0
    els = [rect(-40, G, W_ + 80, 300, "#2a2219", "none", 0, 0, -1)]
    cx = 640
    h = 22 * M
    els += [poly([(cx - 380, G), (cx - h * .95, G - 2), (cx - 30, G - h), (cx + 30, G - h), (cx + h * .95, G - 2), (cx + 380, G)], "#7a6244", "#d9bf8f", 2, tc, fx="fill"),
            poly([(cx - 30, G - h), (cx + 30, G - h), (cx + h * .95, G - 2), (cx + 120, G)], "#5a4630", "none", 0, tc, fx="fill", op=.5)]
    els += [ln([(cx - 420, G), (cx - 420, G - h)], tc + .8, GOLD, 2.5, dur=.8), lab(cx - 440, G - h / 2, "22 m", tc + 1.0, GOLD, 30, "end")]
    bx, bw = 1260, 190
    els += [rect(bx, G - h, bw, h, "#6a6e74", "#cbbca8", 2, 2, tb, fx="fill")]
    for k in range(1, 7):
        els.append(ln([(bx, G - k * h / 7), (bx + bw, G - k * h / 7)], tb + .6 + .05 * k, "#cbbca8", 1.5, draw=False))
    for k in range(7):
        for j in range(3):
            els.append(rect(bx + 22 + j * 56, G - (k + 1) * h / 7 + 12, 34, h / 7 - 26, "#ffe2a8", "none", 0, 2, tb + .8 + .03 * (k * 3 + j), op=.7))
    els += [lab(bx + bw / 2, G - h - 26, "7 storeys", tb + .5, BONE, 28), ln([(cx - 30, G - h), (bx, G - h)], tb + 1.2, "rgba(255,236,206,.4)", 1.5, "inferred", dur=.6)]
    els += [person(1080, G, 1.7 * M, tb + .4)]
    return {"base": "sky", "tod": "dusk", "ground": 1400, "ridges": [], "sun": [1600, 380, 16], "cam": CAM, "els": els}


def _obl(u, v, h=0.0):
    """Oblique projection for the town on the plain: plan units (u east, v south) to the panel, heights up."""
    return (889 + u - v * .18, 480 + v * .42 - h)


CAUSE = [((0, -150), (60, -1200)), ((0, 150), (-110, 1300)), ((180, 0), (1500, 70)), ((-180, 0), (-1400, -40))]


def _causeway_els(at, step=.25):
    out = []
    for k, ((u0, v0), (u1, v1)) in enumerate(CAUSE):
        L = math.hypot(u1 - u0, v1 - v0)
        nu, nv = -(v1 - v0) / L * 18, (u1 - u0) / L * 18
        top = [_obl(u0 + nu, v0 + nv, 10), _obl(u1 + nu, v1 + nv, 10), _obl(u1 - nu, v1 - nv, 10), _obl(u0 - nu, v0 - nv, 10)]
        side = [_obl(u0 - nu, v0 - nv, 10), _obl(u1 - nu, v1 - nv, 10), _obl(u1 - nu, v1 - nv, 0), _obl(u0 - nu, v0 - nv, 0)]
        out += [poly(side, "#6a5638", "none", 0, at + step * k, fx="fade"), poly(top, "#b49a6a", "#e2c27e", 1.2, at + step * k, fx="fade")]
    return out


def _town_els(at, fx=None):
    """The town on its terrace (oblique): the terrace, the cone, three platform houses."""
    terr = [_obl(u, v, 0) for u, v in ((-200, -170), (200, -170), (200, 170), (-200, 170))]
    terr_t = [_obl(u, v, 40) for u, v in ((-200, -170), (200, -170), (200, 170), (-200, 170))]
    out = [poly([terr[3], terr[2], terr_t[2], terr_t[3]], "#6a5638", "none", 0), poly([terr[2], terr[1], terr_t[1], terr_t[2]], "#5a4830", "none", 0),
           poly(terr_t, "#a08458", "#e2c27e", 1.5, 0)]
    cx, cy = _obl(30, -40, 40)
    out += [poly([(cx - 90, cy + 20), (cx - 8, cy - 150), (cx + 8, cy - 150), (cx + 90, cy + 20)], "#8a7048", "#e2c27e", 1.5, 0),
            poly([(cx, cy - 150), (cx + 8, cy - 150), (cx + 90, cy + 20), (cx + 20, cy + 22)], "#6a5436", "none", 0, 0)]
    for u, v in ((-120, 60), (120, 80), (-100, -110)):
        x, y = _obl(u, v, 40)
        out += [poly([(x - 34, y), (x + 34, y), (x + 30, y - 18), (x - 30, y - 18)], "#b9a072", "#e2c27e", 1, 0)]
    return [grp(out, at, fx)] if at != -1 else static(out)


def s32():
    """The town on its terraces, with its cone, and the straight raised causeways running out across the plain in four directions;
    canals beside them; a round reservoir."""
    tw, tc, tr = T("s32", "causeways"), T("s32", "canals"), T("s32", "reservoirs")
    els = [rect(-40, 250, W_ + 80, 800, "#6f7f44", "none", 0, 0, -1), rect(-40, 246, W_ + 80, 8, "#4a5a30", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, 250, 18, -1, "#2a4a2c", seed=32, hi="#3f6a40")
    for k, (u, v, r) in enumerate(((-900, -500, 60), (700, -620, 50), (1100, 300, 90), (-1000, 400, 110), (-500, -700, 40))):
        x, y = _obl(u, v)
        els += forest_island(x, y, r, r * .45, -1, k + 40)
    for k, ((u0, v0), (u1, v1)) in enumerate(CAUSE):
        L = math.hypot(u1 - u0, v1 - v0)
        nu, nv = -(v1 - v0) / L * 34, (u1 - u0) / L * 34
        els.append(ln([_obl(u0 + nu, v0 + nv), _obl(u1 + nu, v1 + nv)], tc + .2 * k, "#4f93b3", 4, dur=1.0))
    els += _causeway_els(tw)
    els += _town_els(-1)
    rx, ry = _obl(-420, 260)
    els += [poly(E(rx, ry, 120, 46, 30), "#3f7f9c", "#9fd0ff", 2, tr, fx="pop")]
    els += [lab(_obl(60, -900)[0] + 70, _obl(60, -900)[1], "causeways", tw + .6, GOLD, 28, "start"),
            lab(_obl(560, 60)[0], _obl(560, 60)[1] + 54, "canals", tc + .6, "#9fd0ff", 26), lab(rx, ry + 76, "reservoir", tr + .4, "#9fd0ff", 26)]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [300, 140, 18], "cam": CAM, "els": els}


def s33_add():
    """The flood: water spreads over the plain, the causeways stay dry above it; then the reservoir glints."""
    tf, td, ts = T("s33", "floods every year"), T("s33", "dry road"), T("s33", "a reservoir is")
    out = [rect(-40, 262, W_ + 80, 790, "rgba(79,147,179,.62)", "none", 0, 0, tf, dur=1.4)]
    out += _causeway_els(tf + 1.0, .05)
    out += _town_els(tf + 1.0, "fade")
    rx, ry = _obl(-420, 260)
    cx_, cy_ = _obl(560, 60)                    # the drowned reservoir and canals keep crisp outlines and names above the water
    out += [poly(E(rx, ry, 120, 46, 30), "none", "#9fd0ff", 2.5, tf + 1.0, fx="fade"),
            lab(rx, ry + 76, "reservoir", tf + 1.0, "#9fd0ff", 26, fx="fade"), lab(cx_, cy_ + 54, "canals", tf + 1.0, "#9fd0ff", 26, fx="fade")]
    x, y = _obl(-110, 900, 10)
    out += chip(x + 40, y - 70, "a dry road", GOLD, td, 28)
    out += [gl(rx, ry, 150, ts, .6, "glowb")] + chip(rx, ry - 90, "water for the dry season", BLUE, ts + .2, 26)
    return out


def s34():
    """About 570,000 cubic metres: Cotoca's centre in section at left; 230 Olympic pools pop in rows at right."""
    tv, tp = T("s34", "five hundred and seventy thousand"), T("s34", "About two hundred")
    G = 560
    els = [rect(80, G, 560, 14, "#4a3a28", "none", 0, 0, -1)]
    els += [poly([(110, G), (170, G - 70), (550, G - 70), (610, G)], "#7a6244", "#d9bf8f", 2, .3, fx="fill"),
            poly([(300, G - 70), (352, G - 220), (366, G - 220), (420, G - 70)], "#8a7048", "#e2c27e", 2, .6, fx="fill"),
            poly([(190, G - 70), (205, G - 100), (265, G - 100), (280, G - 70)], "#9a7e52", "#e2c27e", 1.5, .8, fx="fill"),
            poly([(450, G - 70), (465, G - 96), (525, G - 96), (540, G - 70)], "#9a7e52", "#e2c27e", 1.5, .9, fx="fill")]
    els += [lab(360, G + 50, "Cotoca's centre", .9, DIM, 26)] + chip(360, G + 120, "about 570,000 cubic metres", GOLD, tv, 28)
    cols, w, h, gx, gy = 13, 58, 22, 74, 33
    x0, y0 = 760, 170
    for k in range(230):
        r, c = divmod(k, cols)
        x, y = x0 + c * gx, y0 + r * gy
        els.append(grp([rect(x - w / 2, y - h / 2, w, h, "#3f86b0", "#9fd0ff", 1.2, 4), ln([(x - w / 2 + 4, y - 4), (x + w / 2 - 4, y - 4)], 0, "#bfe6f5", 1, draw=False),
                        ln([(x - w / 2 + 4, y + 4), (x + w / 2 - 4, y + 4)], 0, "#bfe6f5", 1, draw=False)], round(tp - .2 + .007 * k, 2), "pop"))
    els += [lab(x0 + 6 * gx, 150 - 20, "about 230 Olympic pools", tp + 1.2, "#9fd0ff", 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def squash(x, y, s, at):
    return [grp([poly(E(x, y, 22 * s, 16 * s, 18), "#e8a43a", "#8a5a14", 1.5), ln([(x, y - 16 * s), (x + 4 * s, y - 24 * s)], 0, "#4f8a3a", 3, draw=False)], at, "pop")]


def manioc(x, y, s, at):
    return [grp([poly([(x - 30 * s, y - 4 * s), (x + 26 * s, y - 10 * s), (x + 32 * s, y), (x + 26 * s, y + 8 * s), (x - 30 * s, y + 4 * s)], "#a8774e", "#5a3a22", 1.5, curve=True),
                 ln([(x - 30 * s, y), (x - 40 * s, y - 10 * s)], 0, "#4f8a3a", 3, draw=False)], at, "pop")]


def s35():
    """Two time lines. Top: 11,000 years ago to today: forest islands and first crops from about 10,850 years ago (squash about 10,250,
    manioc about 10,350), the Casarabe towns. Below, close up, 300 to 1600 CE: the towns end about 1400; Europeans, 1492."""
    t1, tc, te = T("s35", "ten thousand years"), T("s35", "Casarabe towns faded"), T("s35", "before any European")
    X = lambda ya: round(200 + (11000 - ya) / 11000 * 1380, 1)
    els = [axis(200, 1580, 330, [(X(11000), "11,000 years ago"), (X(8000), "8,000"), (X(4000), "4,000"), (X(0), "today")], .2)]
    els += [{"k": "band", "x0": X(10850), "x1": X(0), "y": 270, "h": 14, "c": "#6fae4a", "in": .5, "dur": 1.2},
            lab(X(10850), 240, "forest islands, first crops", .9, GREEN, 26, "start")]
    els += manioc(X(10350), 190, 1.0, t1 + .8) + squash(X(10250) + 70, 190, 1.0, t1 + 1.0)
    els += [{"k": "band", "x0": X(1526), "x1": X(626), "y": 300, "h": 16, "c": AU, "in": round(t1 + 1.6, 2), "dur": .6}]
    D = lambda yr: round(300 + (yr - 300) / 1300 * 1250, 1)
    els += [axis(300, 1550, 640, [(D(300), "300 CE"), (D(700), "700"), (D(1100), "1100"), (D(1500), "1500")], tc - .4)]
    els += [ln([(X(1526), 316), (D(500), 590)], tc - .4, "rgba(232,195,90,.4)", 1.5, "inferred", dur=.6), ln([(X(626), 316), (D(1400), 590)], tc - .4, "rgba(232,195,90,.4)", 1.5, "inferred", dur=.6)]
    els += [{"k": "band", "x0": D(500), "x1": D(1400), "y": 590, "h": 22, "c": AU, "in": round(tc, 2), "dur": 1.0}, lab(D(950), 565, "Casarabe towns, 500 to 1400 CE", tc + .3, GOLD, 28)]
    els += [ln([(D(1492), 540), (D(1492), 650)], te, RED, 4, dur=.4), lab(D(1492) + 12, 530, "Europeans, 1492", te + .2, RED, 26, "start")]
    els += bracket(D(1400), D(1492), 690, te + .6, "about a century", BONE, False, 24, ty=730)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}



# ================================================================== CHAPTER 5 · The valley of straight roads

def s37():
    """The whole picture, from above (schematic, lidar style): the valley floor in plan, the two straight roads, the platform clusters
    and drained fields, the river; the survey and publication dates."""
    tl, tp = T("s37", "lidar survey"), T("s37", "published the whole")
    plats, plazas, fields = _city()
    K = .30                                           # units per metre
    P = lambda X, Z: (889 + X * K, 820 - Z * K * .62 + (Z - 1600) * 0)
    def pp(X, Z):
        return (889 + X * K, 800 - (Z - 250) * K * .62)
    els = [rect(-40, -40, W_ + 80, H_ + 80, "#4a4640", "none", 0, 0, -1)]
    rnd = random.Random(37)
    for k in range(26):
        y = rnd.uniform(0, H_)
        els.append(ln([(-40, y), (W_ + 40, y + rnd.uniform(-20, 20))], -1, "#524d46", 3, draw=False))
    els += [ln([(-40, 200), (300, 240), (600, 190), (900, 230), (1200, 170), (1500, 210), (W_ + 40, 160)], -1, "#3f7f9c", 10, curve=True, draw=False),
            lab(1500, 170, "Upano river", -1, "#9fd0ff", 24, st="ital")]
    for X, Z, sw, sd, a in fields:
        x, y = pp(X, Z)
        if 100 < x < 1680 and 230 < y < 790:
            for k in range(5):
                els.append(ln([(x - 26 + 13 * k, y - 12), (x - 26 + 13 * k, y + 12)], -1, "#36332e", 2, draw=False))
    for (x0, z0), (x1, z1) in _road_pts():
        els.append(ln([pp(x0, z0), pp(x1, z1)], .3, "#efe6d2", 4, dur=1.2))
    for X, Z, w, d, a, h in plats:
        x, y = pp(X, Z)
        if 90 < x < 1690 and 230 < y < 795:
            els.append(rect(x - 3, y - 2, 6, 4, "#e6cc96", "none", 0, 1, round(.4 + (y - 230) / 565 * 1.6, 2), fx="pop"))
    els += [ln([(1340, 770), (1340 + 1000 * K, 770)], .3, BONE, 2.5, draw=False), lab(1340 + 500 * K, 754, "1 km", .3, BONE, 24)]
    els += chip(560, 150, "2015: lidar survey", SCANC, tl, 28) + chip(950, 150, "2024: published", GOLD, tp, 28)   # below the HUD, clear of the river
    return {"base": "dark", "cam": CAM, "els": els}


def s36():
    """Rostain's trench: a platform at the edge of the forest, Sangay smoking behind; in the trench section a hearth, pottery and the
    floor of the platform show as named; two diggers."""
    tr, t9, th, tp, tm = T("s36", "Stephen Rostain"), T("s36", "nineteen nineties"), T("s36", "hearths"), T("s36", "pottery"), T("s36", "hearths") + .2     # the floor shows with the hearth that sits on it
    hz = PV.horizon()
    els = _mountains("dawn")
    els += [rect(-40, hz - 4, W_ + 80, 900, "#3a4a30", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, hz + 70, 30, -1, "#22402a", seed=36, hi="#355a38")
    G = 700
    els += [rect(-40, hz + 66, W_ + 80, 800, "#6a5a3a", "none", 0, 0, -1)]
    els += [poly([(360, G), (520, G - 130), (1260, G - 130), (1420, G)], "#8a7048", "#e2c27e", 2, -1)]
    tx0, tx1 = 780, 1060
    els += [rect(tx0, G - 130, tx1 - tx0, 160, "#3a2c1e", "#e2c27e", 1.5, 0, -1)]
    for k, (y, c) in enumerate(((G - 120, "#6a5236"), (G - 80, "#56422c"), (G - 40, "#4a3826"))):
        els.append(rect(tx0, y, tx1 - tx0, 26, c, "none", 0, 0, -1))
    els += [ln([(tx0, G - 64), (tx1, G - 64)], tm, "#e2c27e", 3, dur=.8), lab(tx1 + 20, G - 60, "a platform floor", tm + .15, GOLD, 24, "start")]
    els += [gl(860, G - 50, 70, th, .8, "fire"), poly(E(860, G - 46, 34, 8, 16), "#1a0e08", "#ff9a4a", 1.5, th, fx="pop"), lab(860, G + 60, "hearth", th + .3, "#ffb07a", 24)]
    rnd = random.Random(36)
    els += [poly([(x - 10, y + 6), (x + 2, y - 8), (x + 12, y + 4)], "#c4602e", "#f0a070", 1, tp + .1 * k, fx="pop") for k, (x, y) in enumerate(((960, G - 100), (1000, G - 30), (930, G - 20), (1030, G - 90)))]
    els += [lab(990, G + 60, "pottery", tp + .3, "#f0a070", 24)]
    els += fig(700, G - 130, 80, tr - .2, "#e8d6b8", "point", 1, hat=True) + fig(1110, G - 130, 76, tr, "#e8d6b8", "hold", -1, hat=True)
    els += [lab(700, G - 230, "Stephen Rostain", tr + .3, BONE, 26)] + chip(1300, 470, "since the 1990s", GOLD, t9, 26)
    return {"base": "sky", "tod": "dawn", "ground": 1400, "ridges": [], "sun": [1520, hz - 60, 22], "cam": CAM, "els": els}


def _platform_plan(x, y, w, h, at, fx="pop"):
    """A platform in lidar plan: a raised rectangle with a lit edge and a shadow."""
    return [grp([rect(x + 6, y + 8, w, h, "#1e1c18", "none", 0, 4), rect(x, y, w, h, "#c9bfa8", "#efe6d2", 1.5, 4),
                 ln([(x + 4, y + 4), (x + w - 4, y + 4)], 0, "#f7f1e2", 2, draw=False)], at, fx)]


CL = (700, 450, 8.0)                      # the cluster's plaza centre and the scale (units per metre)


def _cluster_rects():
    cx, cy, M = CL
    s = 44 * M / 2
    W, D = 20 * M, 10 * M
    return [(cx - s, cy - s - D - 22, W, D), (cx + s - W, cy - s - D - 22, W, D), (cx - s, cy + s + 22, W, D), (cx + s - W, cy + s + 22, W, D),
            (cx - s - D - 22, cy - W / 2, D, W), (cx + s + 22, cy - W / 2, D, W)]


def s38():
    """One cluster in lidar plan (8 units = 1 m): six platforms about 20 by 10 m round a low square plaza; dimensions; drained fields
    gridded between this cluster and the next; a sunken street along the bottom."""
    tp, td, tg, tf = T("s38", "six thousand platforms"), T("s38", "twenty metres by"), T("s38", "set in groups"), T("s38", "drained fields")
    cx, cy, M = CL
    s_ = 44 * M / 2
    els = [rect(-40, -40, W_ + 80, H_ + 80, "#57524a", "none", 0, 0, -1)]
    rnd = random.Random(38)
    for k in range(30):
        y = rnd.uniform(0, H_)
        els.append(ln([(-40, y), (W_ + 40, y + rnd.uniform(-20, 20))], -1, "#5f5a51", 3, draw=False))
    els += [rect(-40, 770, W_ + 80, 50, "#3a3630", "none", 0, 0, -1), ln([(-40, 768), (W_ + 40, 768)], -1, "#efe6d2", 2, draw=False), ln([(-40, 822), (W_ + 40, 822)], -1, "#efe6d2", 2, draw=False)]
    els += [rect(cx - s_, cy - s_, 2 * s_, 2 * s_, "#4a4640", "#d8cdb4", 1.5, 6, tg, fx="fade"), lab(cx, cy + 10, "plaza", tg + .3, "#d8cdb4", 28)]
    for k, (x, y, w, h) in enumerate(_cluster_rects()):
        els += _platform_plan(x, y, w, h, tp + .12 * k)
    x, y, w, h = _cluster_rects()[0]
    els += [{"k": "dim", "x1": x, "y1": y - 26, "x2": x + w, "y2": y - 26, "t": "20 m", "c": GOLD, "fx": "draw", "dur": .8, "in": round(td, 2)},
            {"k": "dim", "x1": x - 26, "y1": y, "x2": x - 26, "y2": y + h, "t": "10 m", "c": GOLD, "fx": "draw", "dur": .6, "in": round(td + .8, 2)}]
    for gx0, gy0, gw, gh in ((1090, 150, 560, 280), (1090, 470, 560, 260), (120, 560, 300, 170)):
        for k in range(int(gw / 40) + 1):
            els.append(ln([(gx0 + 40 * k, gy0), (gx0 + 40 * k, gy0 + gh)], tf + .02 * k, "#2e2b26", 2.5, dur=.5))
        for k in range(int(gh / 70) + 1):
            els.append(ln([(gx0, gy0 + 70 * k), (gx0 + gw, gy0 + 70 * k)], tf + .3 + .03 * k, "#2e2b26", 2.5, dur=.6))
    els += [lab(1370, 140, "drained fields", tf + .6, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s40_add():
    """Garden urbanism: thatched houses rise on the platforms, crops fill the drained fields."""
    t = T("s40", "garden urbanism")
    out = []
    for k, (x, y, w, h) in enumerate(_cluster_rects()):
        out += [grp([rect(x + w * .15, y + h * .15, w * .7, h * .7, THATCH, THATCH_D, 1.5, min(w, h) * .3),
                     ln([(x + w * .2, y + h / 2), (x + w * .8, y + h / 2)] if w > h else [(x + w / 2, y + h * .2), (x + w / 2, y + h * .8)], 0, THATCH_D, 2, draw=False)], t - .8 + .1 * k, "pop")]
    rnd = random.Random(40)
    for gx0, gy0, gw, gh in ((1090, 150, 560, 280), (1090, 470, 560, 260), (120, 560, 300, 170)):
        for k in range(int(gw / 40) * int(gh / 70)):
            out.append(circ(gx0 + 20 + 40 * (k % int(gw / 40)), gy0 + 35 + 70 * (k // int(gw / 40)), 9, ("#6fae4a", "#4f8a3a")[k % 2], at=t - .4 + .01 * k, fx="pop"))
    out += chip(700, 120, "garden urbanism", GOLD, t + .3, 32)
    return out


def s39():
    """A road dug dead straight across hills and stream valleys, at least 25 km; below, its cross-section (24 units = 1 m): dug down,
    the earth banked up on either side; a person."""
    tr, tk = T("s39", "roads dug"), T("s39", "twenty-five kilometres")
    els = [rect(80, 130, 1620, 340, "#4f4a42", "rgba(255,236,206,.25)", 1.5, 12, -1)]
    for k, (hx, hy, rx_, ry_) in enumerate(((330, 260, 160, 80), (760, 360, 200, 70), (1150, 230, 180, 70), (1500, 340, 170, 80))):
        for j in range(4):
            els.append(poly(E(hx, hy, rx_ * (1 - .22 * j), ry_ * (1 - .22 * j), 28), "none", "#8a8070", 1.6, -1, curve=True))
    els += [ln([(80, 420), (400, 380), (700, 440), (1000, 400), (1300, 450), (1700, 410)], -1, "#4f8fae", 3, curve=True, draw=False),
            ln([(560, 130), (600, 300), (560, 470)], -1, "#4f8fae", 3, curve=True, draw=False)]
    els += [ln([(100, 330), (1680, 270)], tr, "#efe6d2", 9, dur=1.8), ln([(100, 330), (1680, 270)], tr, "#3a3630", 4, dur=1.8)]
    els += bracket(100, 1680, 490, tk, None, GOLD, False)
    els += [lab(889, 535, "at least 25 km", tk + .3, GOLD, 30)]
    M, G, cx = 24.0, 700, 889
    half, depth, bank = 5 * M, 2.5 * M, 1.5 * M
    sec = [(140, G), (cx - half - 4 * M, G), (cx - half - 1.5 * M, G - bank), (cx - half, G - bank * .6), (cx - half + .6 * M, G + depth), (cx + half - .6 * M, G + depth),
           (cx + half, G - bank * .6), (cx + half + 1.5 * M, G - bank), (cx + half + 4 * M, G), (1640, G), (1640, 800), (140, 800)]
    els += [poly(sec, "#6e5a3e", "#e2c27e", 2, tr + .8, fx="fade")]
    els += [person(cx, G + depth, 1.7 * M, tr + 1.2)]
    els += [lab(cx, G + depth + 50, "dug down", tr + 1.4, BONE, 26)][0:0]
    els += [lab(cx - half - 1.5 * M, G - bank - 22, "earth banked up", tr + 1.4, BONE, 24), lab(cx + 330, G - 40, "dug down", tr + 1.5, BONE, 24, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s41():
    """A lake in section with a core tube driven into its mud; the core shown beside it, layer by layer; a gold band low down: maize,
    about 570 BCE."""
    tl, tm = T("s41", "Mud from a nearby lake"), T("s41", "maize growing")
    els = [rect(80, 300, 860, 120, "#2f6e8c", "none", 0, 0, -1), ln([(80, 300), (940, 300)], -1, "#9fd0ff", 2, draw=False)]
    cols = ["#5a5048", "#6e6052", "#4a4038", "#7a6a56", "#3f362e", "#6a5a48"]
    for k in range(6):
        els.append(rect(80, 420 + 60 * k, 860, 60, cols[k], "none", 0, 0, -1))
    els += [poly([(80, 300), (40, 780), (80, 780)], "#3a3228", "none", 0, -1), poly([(940, 300), (980, 780), (940, 780)], "#3a3228", "none", 0, -1)]
    els += [rect(440, 268, 160, 26, "#8a6a44", "#e2c27e", 1.5, 3, -1)] + fig(520, 268, 70, -1, "#e8d6b8", "hold", 1)
    els += [ln([(560, 200), (560, 700)], tl, "#cfd6dc", 8, dur=1.4), lab(600, 190, "core", tl + .4, BONE, 24, "start")]
    cx = 1300
    els += [rect(cx - 36, 180, 72, 580, "#6e6052", "#cfd6dc", 2, 6, tl + 1.2, fx="fill")]
    for k in range(14):
        els.append(rect(cx - 34, 182 + 41 * k, 68, 20, cols[k % 6], "none", 0, 0, tl + 1.4 + .03 * k))
    els += [rect(cx - 34, 610, 68, 24, AU, "none", 0, 0, tm, fx="pop")]
    els += [poly([(cx + 70, 600), (cx + 92, 580), (cx + 112, 600), (cx + 112, 650), (cx + 92, 670), (cx + 70, 650)], "#e8c35a", "#8a6a14", 1.5, tm + .2, fx="pop", curve=True)]
    els += [circ(cx + 84 + 10 * (k % 2), 596 + 12 * (k // 2), 4, "#fff2c0", at=tm + .3) for k in range(8)]
    els += chip(cx + 132, 600, "maize", GOLD, tm + .4, 28, "start") + [lab(cx + 136, 660, "about 570 BCE", tm + .6, GOLD, 26, "start")]   # inside the frame
    els += [lab(cx, 160, "top: today", tl + 1.4, DIM, 22), lab(cx, 800, "bottom: oldest", tl + 1.4, DIM, 22), lab(510, 760, "a nearby lake", tl + .6, "#9fd0ff", 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s42():
    """Two endings, schematic: the excavators' sudden end (lilac dotted, a drop at 400 to 600 CE) and the lake's slow decline (gold)
    from about 250 to 550 CE; a single great ashfall, crossed."""
    ts, tg, ta = T("s42", "end suddenly"), T("s42", "slow decline"), T("s42", "not one great")
    X = lambda yr: round(200 + (yr + 700) / 1600 * 1380, 1)
    els = [axis(200, 1580, 690, [(X(-500), "500 BCE"), (X(0), "1 CE"), (X(500), "500 CE"), (X(900), "900")], .2),
           lab(200, 180, "human activity", .3, DIM, 24, "start")]
    els += [rect(X(400), 240, X(600) - X(400), 440, "rgba(201,193,238,.12)", "none", 0, 0, ts)]
    els += [ln([(X(-500), 320), (X(400), 320), (X(600), 660), (X(900), 660)], ts + .2, LILAC, 4, "claimed", dur=1.4), lab(X(500) + 30, 300, "a sudden end?", ts + .8, LILAC, 28, "start")]
    gold = [(X(-570), 660), (X(-400), 520), (X(-200), 390), (X(0), 350), (X(250), 345), (X(350), 400), (X(450), 500), (X(550), 640), (X(650), 660)]
    els += [ln(gold, tg, AU, 5, dur=2.0, curve=True), lab(X(330), 470, "a slow decline", tg + 1.0, GOLD, 28, "end")]
    for k in range(18):
        els.append(circ(X(470) + random.Random(k).uniform(-60, 60), 230 + random.Random(k + 5).uniform(-20, 20), 5, "#9a948c", at=ta + .02 * k, fx="pop"))
    tx = T("s42", "volcanic ash") - .1
    els += cross(X(470), 230, tx, RED, 1.6, 6) + [lab(X(470) + 90, 236, "one big ashfall?", ta + .3, "#bdb6ac", 26, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s43():
    """Cleared pasture in Acre, from the air: a giant ditched circle and a square cut into the grass, stumps, cattle, a person; the
    forest edge behind; 450+; and an inset section of a ditch 11 m wide."""
    tc, tg, tq, t11 = T("s43", "ranchers cleared"), T("s43", "giant circles"), T("s43", "squares"), T("s43", "eleven metres")
    HZ = 300
    els = [rect(-40, HZ, W_ + 80, 800, "#8a9a52", "none", 0, 0, -1)]
    els += crown_row(-40, W_ + 40, HZ + 10, 24, -1, "#24452b", seed=43, hi="#3f6a40")
    rnd = random.Random(43)
    els += [rect(rnd.uniform(60, 1700), rnd.uniform(HZ + 40, 780), 14, 8, "#6a4a2a", "none", 0, 2, tc + .03 * k, fx="pop") for k in range(16)]
    ring = [(650 + 330 * math.cos(math.radians(a)), 530 + 120 * math.sin(math.radians(a))) for a in range(0, 361, 6)]
    els += [ln(ring, tg, "#4a3a26", 22, dur=1.6, curve=True), ln([(650 + 352 * math.cos(math.radians(a)), 530 + 132 * math.sin(math.radians(a))) for a in range(0, 361, 6)], tg + .2, "#c9b48a", 5, dur=1.6, curve=True)]
    sq = [(1080, 470), (1480, 450), (1560, 640), (1140, 670), (1080, 470)]
    els += [ln(sq, tq, "#4a3a26", 20, dur=1.4), ln([(1060, 455), (1500, 432), (1585, 655), (1125, 690), (1060, 455)], tq + .2, "#c9b48a", 5, dur=1.4)]
    for k in range(9):
        x, y = rnd.uniform(200, 1700), rnd.uniform(HZ + 60, 760)
        els += [rect(x, y, 20, 9, "#efe6d8", "none", 0, 3, -1), ln([(x + 3, y + 9), (x + 3, y + 15)], -1, "#efe6d8", 2, draw=False), ln([(x + 17, y + 9), (x + 17, y + 15)], -1, "#efe6d8", 2, draw=False)]
    els += [person(980, 640, 30, -1)]
    els += chip(889, 200, "450+ geoglyphs", GOLD, tg + 1.0, 30)
    ix, iy = 1240, 740
    M = 9.0
    els += [rect(ix - 150, iy - 110, 400, 150, "rgba(20,16,12,.85)", "rgba(255,236,206,.3)", 1.5, 10, t11, fx="pop")]
    sec = [(ix - 130, iy - 40), (ix - 50, iy - 40), (ix - 40, iy - 40 + 4 * M), (ix - 50 + 11 * M - 10, iy - 40 + 4 * M), (ix - 50 + 11 * M, iy - 40), (ix + 230, iy - 40), (ix + 230, iy + 30), (ix - 130, iy + 30)]
    els += [poly(sec, "#8a7048", "#e2c27e", 1.5, t11 + .1, fx="pop"), {"k": "dim", "x1": ix - 50, "y1": iy - 70, "x2": ix - 50 + 11 * M, "y2": iy - 70, "t": "11 m", "c": GOLD, "fx": "draw", "dur": .6, "in": round(t11 + .3, 2)}]
    els += [person(ix + 140, iy - 40, 1.7 * M, t11 + .3)]
    return {"base": "sky", "tod": "day", "ground": 1400, "ridges": [], "sun": [1600, 150, 18], "cam": CAM, "els": els}


def s44_add():
    """The forest as it was: dashed bamboo forest round the geoglyphs, leaving small clearings; a magnifier with tiny plant fossils."""
    tf, tl = T("s44", "Tiny plant fossils"), T("s44", "living forest")
    out = []
    rnd = random.Random(44)
    for k in range(60):
        x, y = rnd.uniform(-20, 1780), rnd.uniform(330, 800)
        if ((x - 650) / 400) ** 2 + ((y - 530) / 170) ** 2 < 1 or (1030 < x < 1640 and 400 < y < 830):   # clear of the ring, square and inset
            continue
        out.append(poly(blob(x, y, 46, 22, 12, .2, k), "none", "#9fd0a0", 2, tl + .015 * k, style="inferred", fx="fade"))
    out += [lab(650, 380, "small clearings", tl + 1.0, BONE, 26)]
    mx, my = 1500, 210
    out += [circ(mx, my, 92, "rgba(16,22,26,.9)", "#e6f3ff", 4, tf, fx="pop"), ln([(mx - 66, my + 66), (mx - 120, my + 120)], tf, "#e6f3ff", 10, draw=False)]
    for k in range(7):
        a = 2 * math.pi * k / 7
        x, y = mx + 46 * math.cos(a), my + 40 * math.sin(a)
        out.append(poly([(x - 14, y), (x - 4, y - 12), (x + 12, y - 8), (x + 14, y + 6), (x, y + 12)], "rgba(200,230,255,.55)", "#ffffff", 1.2, tf + .3 + .08 * k, fx="pop"))
    out += [lab(mx - 120, my + 24, "tiny plant fossils", tf + .6, "#cfe6ff", 26, "end")]
    return out


VA = View(-74.0, -63.6, -11.4, -6.0, (90, 120, 1600, 680))


def s45():
    """Southwest Amazonia (Acre and southern Amazonas): flight lines draw across the forest; along them 396 new earthworks pop in gold,
    and 36 known ones in grey."""
    t26, tf, t432, t36 = T("s45", "twenty twenty-six"), T("s45", "Along its flight lines"), T("s45", "four hundred and thirty-two"), T("s45", "thirty-six were known")
    v = VA
    els = [rect(-40, -40, W_ + 80, H_ + 80, "#22382a", "none", 0, 0, -1)]
    for n in ("purus", "jurua", "acre", "madeira", "beni"):
        els.append(river(v, n, -1, "#4f8fae", 2.5, draw=False, op=.9))
    rx, ry = v.p(-67.81, -9.97)
    els += [pin(rx, ry, "Rio Branco", -1, BONE), lab(v.p(-71.0, -9.0)[0], v.p(-71.0, -9.0)[1], "Acre", -1, DIM, 30, st="ital"), lab(v.p(-66.6, -7.2)[0], v.p(-66.6, -7.2)[1], "Amazonas", -1, DIM, 30, st="ital")]
    rnd = random.Random(45)
    lines = []
    for k in range(9):
        y0 = 180 + k * 64 + rnd.uniform(-10, 10)
        a = [(110, y0 + rnd.uniform(-30, 30)), (1670, y0 + rnd.uniform(-60, 60))]
        lines.append(a)
        els.append(ln(a, tf - 1.6 + .15 * k, SCANC, 2, dur=1.0, op=.7))
    pts = []
    for k in range(432):
        (x0, y0), (x1, y1) = lines[k % 9]
        u = rnd.uniform(0, 1)
        pts.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + rnd.uniform(-8, 8)))
    for k, (x, y) in enumerate(pts[:396]):
        els.append(circ(x, y, 5, AU, at=round(t432 + .004 * k, 2), fx="pop"))
    for k, (x, y) in enumerate(pts[396:]):
        els.append(circ(x, y, 7, "#9a938a", "#efe6d2", 1.5, at=round(t36 - .4 + .02 * k, 2), fx="pop"))
    els += chip(400, 768, "432 found", GOLD, t432 + 1.2, 26) + chip(700, 768, "36 known before", "#bdb6ac", t36 + .1, 26)   # above the captions
    els += chip(1560, 170, "2026", SCANC, t26, 28)                                             # last: on top of the flight lines
    return {"base": "map", "cam": CAM, "els": els}


def s47_add():
    """Beyond the flight lines, the forest not yet scanned glows faintly, a question mark."""
    t = .3
    return [gl(x, y, 260, t + .1 * k, .25, "lamp") for k, (x, y) in enumerate(((300, 300), (900, 500), (1450, 380)))] + qmark(889, 470, t + .4, 110) + chip(889, 560, "not yet scanned", LILAC, t + .8, 26)


def s46():
    """Left, 300 squares, each 100 earthworks: 240 solid and 60 dashed (24,000 to 30,000). Right, people, each 100,000: 12 and a half
    solid, the rest dashed to 30 (1.25 to 3 million, proposed); the period."""
    te, tm, tt, tc = T("s46", "twenty-four to thirty thousand"), T("s46", "over a million"), T("s46", "perhaps three million"), T("s46", "one hundred and three hundred")
    els = []
    x0, y0, c = 150, 250, 26
    for k in range(300):
        r, q = divmod(k, 20)
        x, y = x0 + q * c, y0 + r * c
        if k < 240:
            els.append(rect(x, y, 20, 20, AU, "none", 0, 3, round(te + .006 * k, 2), fx="pop"))
        else:
            els.append(rect(x, y, 20, 20, "none", AU, 1.5, 3, round(te + 1.6 + .01 * (k - 240), 2), style="inferred"))
    els += [lab(x0 + 10 * c, 200, "24,000 to 30,000 earthworks", te, GOLD, 30), lab(x0 + 10 * c, y0 + 15 * c + 36, "each square: 100", te + .5, DIM, 24)]
    px0, py0 = 1000, 270
    for k in range(30):
        r, q = divmod(k, 6)
        x, y = px0 + q * 100, py0 + r * 92 + 70
        if k < 12:
            els += fig(x, y, 70, round(tm + .05 * k, 2), "#e8d6b8", None, 1, "pop")
        elif k == 12:
            els += fig(x, y, 70, round(tm + .7, 2), "rgba(232,214,184,.5)", None, 1, "pop")
        else:
            els.append(grp([circ(x, y - 63, 6, "none", "#e8d6b8", 1.5, style="inferred"), poly([(x - 9, y - 55), (x + 9, y - 55), (x + 8, y), (x - 8, y)], "none", "#e8d6b8", 1.5, style="inferred")],
                           round(tt + .04 * (k - 13), 2), "pop"))
    els += [lab(px0 + 250, 200, "1.25 to 3 million people?", tm, BONE, 30), lab(px0 + 250, py0 + 5 * 92 + 110, "each figure: 100,000 (proposed)", tm + .5, DIM, 24)]
    els += chip(889, 140, "100 to 300 CE", GOLD, tc, 26)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== THE WEIGHING
LROWS = [190, 315, 440, 565]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None, rows=LROWS):
    y = rows[k]
    out = [rect(150, y - 52, 1480, 104, "rgba(18,13,10,.65)", "rgba(255,236,206,.18)", 1.5, 14, at, fx="fade")]
    out += pic(260, y, at + .1)
    out += [lab(360, y + 11, text, at + .2, BONE, 30, "start")]
    if grade:
        out += chip(1480, y, gt, gc, grade, 28)
    return out


def pic_town(x, y, at):
    return [grp([rect(x - 50, y - 6, 100, 30, "#8a7048", "#e2c27e", 1.5, 3), poly([(x - 14, y - 6), (x, y - 40), (x + 14, y - 6)], "#a08458", "#e2c27e", 1.5),
                 ln([(x - 80, y + 26), (x + 80, y + 18)], 0, "#e2c27e", 4, draw=False)], at, "pop")]


def pic_soil(x, y, at):
    return [grp([rect(x - 40, y - 40, 80, 80, "#c99a5a", "rgba(255,236,206,.4)", 1.5, 4), rect(x - 40, y - 40, 80, 56, TP, "none", 0, 0)], at, "pop")]


def pic_bank(x, y, at):
    return [grp([rect(x - 60, y + 6, 120, 30, "#2f6e8c", "none", 0, 3), poly([(x - 60, y + 6), (x - 60, y - 14), (x + 60, y - 14), (x + 60, y + 6)], "#a0583a", "none", 0)]
                + hut(x - 26, y - 14, 30, 30, 0, THATCH_D, "#5a4020", False, None) + hut(x + 14, y - 14, 34, 34, 0, THATCH_D, "#5a4020", False, None), at, "pop")]


def pic_tree(x, y, at):
    return [grp([ln([(x, y + 36), (x, y)], 0, "#7a5a3a", 6, draw=False), poly(blob(x, y - 14, 44, 30, 14, .15, 3), "#2f5a34", GOLD, 2)], at, "pop")]


def s48():
    """The ledger, first half: four rows fill as their questions are asked; each grade chip pops as it is said."""
    q1, q2, q3, q4 = T("s48", "Planned towns"), T("s48", "Dark earth made"), T("s48", "Carvajal's crowded"), T("s48", "A forest shaped")
    g1, g2, g3, g4 = T("s48", "Established", k=1), T("s48", "Established", k=2), T("s48", "Strong evidence", k=1), T("s48", "Strong evidence", k=2)
    els = lrow(0, q1, pic_town, "planned towns, long before Europeans", g1, "Established", GRADE["established"])
    els += lrow(1, q2, pic_soil, "dark earth made by people", g2, "Established", GRADE["established"])
    els += lrow(2, q3, pic_bank, "Carvajal's crowded banks", g3, "Strong evidence", GRADE["strong"])
    els += lrow(3, q4, pic_tree, "a forest shaped by people", g4, "Strong evidence", GRADE["strong"])
    els += [lab(360, LROWS[2] + 42, "villages clustered, gaps between", g3 + .4, DIM, 22, "start"),
            lab(360, LROWS[3] + 42, "clearest near old settlements", g4 + .4, DIM, 22, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def pic_cities(x, y, at):
    return [grp([rect(x - 54, y - 20, 30, 40, "#9a938a", "#efe6d2", 1.2, 2), rect(x - 18, y - 34, 26, 54, "#9a938a", "#efe6d2", 1.2, 2),
                 hut(x + 34, y + 20, 34, 34, 0, THATCH, THATCH_D, False, None)[0], circ(x + 14, y + 14, 8, "#6fae4a")], at, "pop")]


def pic_people(x, y, at):
    return [grp([circ(x - 30 + 20 * k, y - 12, 7, "#e8d6b8") for k in range(4)] + [rect(x - 38 + 20 * k, y - 4, 16, 30, "#e8d6b8", "none", 0, 4) for k in range(4)], at, "pop")]


def s49():
    """The ledger, second half: 'cities, or garden cities?' and 'how many people in 1492?' with a range bar, both Open question."""
    q1, q2 = T("s49", "Cities, or garden"), T("s49", "How many")
    g1, g2 = T("s49", "Open question", k=1), T("s49", "Open question", k=2)
    rows = [250, 470]
    els = lrow(0, q1, pic_cities, "cities, or garden cities?", g1, "Open question", GRADE["open"], rows)
    els += [lab(360, rows[0] + 42, "no agreed word yet", T("s49", "no agreed word"), DIM, 22, "start")]
    els += lrow(1, q2, pic_people, "how many people in 1492?", g2, "Open question", GRADE["open"], rows)
    X = lambda m: 760 + (m - 4) / 6 * 520
    te, tc = T("s49", "five million"), T("s49", "soil cores")
    els += [ln([(X(4), 640), (X(10), 640)], te - .2, "rgba(255,236,206,.3)", 2, draw=False)]
    els += [ln([(X(5), 640), (X(8), 640)], te, AU, 10, dur=.8), ln([(X(8), 640), (X(10), 640)], te + .8, AU, 4, "inferred", dur=.6)]
    els += [lab(X(5), 690, "5 million", te + .1, GOLD, 24), lab(X(8), 690, "8 million", te + .6, GOLD, 24), lab(X(10), 690, "more?", te + 1.0, GOLD, 24)]
    els += [rect(400, 600, 30, 110, "#c99a5a", "#efe6d2", 1.5, 4, tc, fx="fill"), circ(415, 640, 4, "#0a0806", at=tc + .4), lab(450, 690, "few signs far from rivers", tc + .4, DIM, 22, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s50():
    """What emptied the towns: bands that end as named, long before 1492; then 1492, and epidemics and slave raids after it."""
    tq, tf, te = T("s50", "what emptied"), T("s50", "Some faded"), T("s50", "epidemics")
    X = lambda yr: round(160 + (yr + 700) / 2500 * 1460, 1)
    els = [axis(160, 1620, 690, [(X(-500), "500 BCE"), (X(0), "1 CE"), (X(500), "500"), (X(1000), "1000"), (X(1500), "1500")], .2)]
    rows = [("Upano valley", -500, 550, 260), ("Acre earthworks", -600, 850, 360), ("Casarabe towns", 500, 1400, 460), ("Upper Xingu towns", 1250, 1650, 560)]
    for k, (nm, a, b, y) in enumerate(rows):
        t_ = tq + .4 + .3 * k if k < 3 else tf + 1.2
        lx, la = (X(a), "start") if k < 3 else (X(1492) - 14, "end")      # the last name ends left of the 1492 line
        els += [{"k": "band", "x0": X(a), "x1": X(b), "y": y, "h": 18, "c": AU if k < 3 else "#d9b46a", "in": round(t_, 2), "dur": .8},
                lab(lx, y - 14, nm, t_ + .2, GOLD, 24, la)]
    els += [ln([(X(1492), 220), (X(1492), 700)], te - .6, RED, 4, dur=.6), lab(X(1492) + 12, 205, "1492", te - .4, RED, 26, "start")]
    els += [{"k": "band", "x0": X(1500), "x1": X(1800), "y": 620, "h": 22, "c": "#a8402a", "in": round(te, 2), "dur": 1.0},
            lab(X(1650), 666, "epidemics, slave raids", te + .4, "#ff9a8a", 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s51():
    """Gold and stone against earth: a lilac dotted golden city and the stone city of Z above; 'Awaiting evidence'; below, solid on
    the ground, an earthen town of platforms, a causeway and thatched houses."""
    tq, ta, te = T("s51", "cities of gold"), T("s51", "Awaiting evidence"), T("s51", "towns of earth")
    els = [rect(-40, 600, W_ + 80, 500, "#2a2219", "none", 0, 0, -1)]
    sky = [(260, 380), (260, 300), (310, 300), (310, 250), (350, 220), (390, 250), (390, 300), (450, 300), (450, 200), (490, 160), (530, 200), (530, 300),
           (600, 300), (620, 260), (660, 250), (700, 260), (720, 300), (760, 300), (760, 380)]
    els += [gl(510, 280, 240, tq, .3, "lamp"), ln(sky, tq, AU, 3, "claimed", dur=1.2)] + [circ(x, y, 4, AU, at=tq + .5 + .04 * k, fx="pop") for k, (x, y) in enumerate(sky[1:-1:2])]
    els += [lab(510, 440, "El Dorado?", tq + .6, GOLD, 28)]
    els += stone_ruin(1020, 380, 420, tq + .8) + [lab(1240, 440, "Z?", tq + 1.2, LILAC, 30, st="serif")]
    els += chip(889, 140, "Awaiting evidence", GRADE["awaiting"], ta, 30)
    for k, x in enumerate((320, 620, 1160, 1460)):
        els += [poly([(x - 110, 700), (x - 80, 650), (x + 80, 650), (x + 110, 700)], "#3a3024", "rgba(226,194,126,.3)", 1.5, -1)]
    els += [poly([(-40, 712), (W_ + 40, 712), (W_ + 40, 730), (-40, 730)], "#4a3e2c", "none", 0, -1)]
    for k, x in enumerate((320, 620, 1160, 1460)):
        els += [poly([(x - 110, 700), (x - 80, 650), (x + 80, 650), (x + 110, 700)], "#8a7048", "#e2c27e", 1.5, te + .15 * k, fx="rise")]
        els += hut(x, 650, 70, 64, te + .15 * k + .2, THATCH, THATCH_D)
    els += [poly([(-40, 712), (W_ + 40, 712), (W_ + 40, 730), (-40, 730)], "#b49a6a", "#e2c27e", 1.2, te + .6, fx="fade")]
    els += [lab(889, 790, "towns of earth", te + .8, AMBER, 32, st="serif")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s52():
    """The tests: the Amazon basin dark with a few bright lidar strips (under 0.1% by 2023); a trench and a sample to date; a lake and
    a core."""
    tl, td, tm = T("s52", "Lidar over"), T("s52", "Digs to date"), T("s52", "mud from many")
    v = View(-80.0, -44.0, -18.0, 5.0, (110, 180, 480, 470))
    els = [grp([{"k": "map", "land": v.land(), "in": 0, "landc": "#1e3324"}], tl, "fade", clip=[100, 170, 500, 490])]
    for k, (lo, la) in enumerate(((-64.6, -14.7), (-78.1, -2.3), (-67.8, -9.0), (-53.1, -12.2), (-60.0, -3.0))):
        x, y = v.p(lo, la)
        els += [rect(x - 6, y - 2, 12, 4, "#e6f3ff", "none", 0, 1, tl + .3 + .1 * k, fx="pop"), gl(x, y, 18, tl + .3 + .1 * k, .6, "glowb")]
    els += [lab(350, 720, "under 0.1% scanned (2023)", tl + .6, SCANC, 24)]
    G = 520
    els += [rect(680, G, 420, 200, "#6e5a3e", "none", 0, 0, td, fx="fade"), rect(800, G, 180, 120, "#2a2019", "#e2c27e", 1.5, 0, td + .1, fx="fade")]
    els += fig(760, G, 80, td + .2, "#e8d6b8", "hold", 1, hat=True) + [rect(900, G + 70, 40, 30, "#efe6d2", "#8a6a44", 1.5, 3, td + .4, fx="pop"), lab(890, 760, "dig and date", td + .5, BONE, 24)]
    els += [rect(1240, 470, 360, 70, "#2f6e8c", "none", 0, 0, tm, fx="fade"), rect(1240, 540, 360, 180, "#5a5048", "none", 0, 0, tm, fx="fade"),
            ln([(1420, 380), (1420, 690)], tm + .3, "#cfd6dc", 7, dur=.8), lab(1420, 760, "more lake cores", tm + .5, "#9fd0ff", 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== stubs while building
def _stub(name):
    def f():
        return {"base": "dark", "stars": 20, "cam": CAM, "els": [lab(889, 470, name, -1, DIM, 40, st="serif")]}
    return f


def _stub_add():
    return []


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "more than six thousand", "s2"), (1, "For centuries, explorers", "s3"), (1, "So who built", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(0, "The ceremony belonged", "s7")], {"chapter": "A river of villages"}),
    (1, 1, "collision", "s8", [(0, "Eight months later", "s9")], {}),
    (1, 2, "reversal", "s10", [(1, "He was honest", "s11")], {}),
    (1, 3, "tag", "s12", [], {}),
    (2, 0, "world", "s13", [], {"chapter": "The lost city of Z"}),
    (2, 1, "collision", "s14", [], {}),
    (2, 2, "reversal", "s15", [(0, "Most of it dates", "s16")], {}),
    (2, 3, "tag", "s17", [], {}),
    (3, 0, "world", "s18", [(1, "The forest keeps", "s19"), (1, "Burn the trees", "s20"), (1, "So, she argued", "s21")], {"chapter": "A counterfeit paradise?"}),
    (3, 1, "reversal", "s22", [(0, "It's full of", "s23"), (1, "And it's living", "s24")], {}),
    (3, 2, "collision", "s25", [(0, "Among them are", "s26")], {}),
    (3, 3, "tag", "s27", [], {}),
    (4, 0, "world", "s28", [], {"chapter": "Causeways in the floodplain"}),
    (4, 1, "collision", "s29", [], {}),
    (4, 2, "reversal", "s30", [(0, "At Cotoca, a cone", "s31"), (1, "From the towns", "s32"), (1, "Where the land", "s33")], {}),
    (4, 3, "cost", "s34", [], {}),
    (4, 4, "tag", "s35", [], {}),
    (5, 0, "world", "s36", [(0, "In {2015", "s37")], {"chapter": "The valley of straight roads"}),
    (5, 1, "collision", "s38", [(0, "And roads dug", "s39"), (0, "The team calls", "s40")], {}),
    (5, 2, "reversal", "s41", [(0, "The excavators saw", "s42")], {}),
    (5, 3, "collision", "s43", [(0, "Tiny plant fossils", "s44"), (1, "Then lidar went", "s45"), (1, "Its authors now", "s46")], {}),
    (5, 4, "tag", "s47", [], {}),
    (6, 0, "weigh", "s48", [(1, "Cities, or garden", "s49"), (1, "And what emptied", "s50"), (2, "El Dorado, or", "s51")], {"chapter": "The weighing"}),
    (6, 1, "test", "s52", [], {}),
    (6, 2, "close", "s53", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.32, 900, 620], "s2_add"), "s4": ("s1", [1, 889, 500], "s4_add"),
    "s11": ("s9", [1, 889, 500], "s11_add"),
    "s23": ("s22", [1.4, 1140, 480], "s23_add"),
    "s26": ("s25", [1, 889, 500], "s26_add"), "s27": ("s18", [1, 889, 500], "s27_add"),
    "s33": ("s32", [1, 889, 500], "s33_add"),
    "s40": ("s38", [1, 889, 500], "s40_add"),
    "s44": ("s43", [1, 889, 500], "s44_add"),
    "s47": ("s45", [1, 889, 500], "s47_add"),
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
    ep = {"id": "lf-amazon-cities", "code": "LF.29", "series": script["series"], "title": script["title"], "case": "amazon-cities",
          "verdict": "solid", "claim": "Did big, planned towns stand in the Amazon before Europeans, and were Carvajal, El Dorado and Z about them?",
          "mood": "mystery", "hook_text": "A city under the *trees*?", "beats": beats, "shots": shots,
          "sources": "Prumers et al. 2022 (doi:10.1038/s41586-022-04780-4) · Rostain et al. 2024 (doi:10.1126/science.adi6317) · "
                     "Parssinen et al. 2026 (doi:10.1038/s41586-026-10835-7) · Heckenberger et al. 2008 (doi:10.1126/science.1159769) · "
                     "Schmidt et al. 2023 (doi:10.1126/sciadv.adh8499) · Levis et al. 2017 (doi:10.1126/science.aal0157) · "
                     "Watling et al. 2017 (doi:10.1073/pnas.1614359114) · Bush et al. 2025 (doi:10.1038/s41467-025-62315-7) · "
                     "Lombardo et al. 2020 (doi:10.1038/s41586-020-2162-7) · Meggers 1971 · Carvajal 1542",
          "post": "Lasers fired through the Amazon rainforest found platforms, plazas and roads as straight as a ruler. Carvajal's crowded "
                  "banks, El Dorado, Fawcett's Z, the 'counterfeit paradise', the dark earths people made, the Casarabe towns of Bolivia, the "
                  "Upano valley of Ecuador and the geoglyphs of Acre, weighed.",
          "hashtags": ["#Amazon", "#LostCities", "#Lidar", "#Archaeology", "#ElDorado", "#WeighItYourself"],
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
    if os.environ.get("RC_STEPMAP"):
        _stepmap(ep, idx)
    return ep


def _stepmap(ep, idx):
    """Print which step shows which words, and write each step's narration length (for previews of chosen steps)."""
    seg, cur = {}, 0
    for bi, b in enumerate(ep["beats"]):
        text = "\n".join(b["lines"])
        parts = re.split(r"\[go:(\d+)[^\]]*\]", text)
        seg[cur] = seg.get(cur, "") + ("\n" if cur in seg else "") + parts[0]
        for k in range(1, len(parts), 2):
            cur = int(parts[k])
            seg[cur] = parts[k + 1]
    durs = {}
    for k in sorted(seg):
        durs[k] = round(_clock(seg[k].strip("\n"))[1], 1)
        print("step %2d %5.1fs:" % (k, durs[k]), re.sub(r"\[[^\]]*\]", "", seg[k]).strip()[:70])
    out = os.environ.get("RC_FILMS_OUT")
    if out:
        json.dump(durs, open(os.path.join(out, "stepdur.json"), "w"))


def EPISODES():
    return [film()]
