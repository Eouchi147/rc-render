"""LF.13 · Unreadable · The Library of Alexandria: What Really Happened (16:9 long film, one wall).

The script is films/long/lf-alexandria/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s48; s5, the title, is the intro card over
the panel of s4), drawn while it is said: Caesar's burning harbour and the library of the legend, the five endings on one
timeline, the city and its Museum, the books taken from ships and borrowed from Athens, the Tables of Callimachus, what each
ancient witness says burned in 48 BCE (the later the writer, the bigger the fire), the size claims against Bagnall's count, the
alibis, the purge of 145 BCE, papyrus that crumbles unless it is copied, the palace quarter wrecked in the 270s, the Serapeum and
its fall, Hypatia (with care: her death belongs to the city's story, not the library's), the caliph story written down some 560
years late, the ledger of endings, the tests, and what was lost and what survived.

Drawings are schematic and true to the numbers said: solid = evidence, dashed = inferred, dotted (lilac) = claimed. The hall of
scrolls is how the legend pictures the library (no trace of its building has been identified); it is drawn as an image of the
story, never as a record.

Facts: the Short 'alexandria-library' (f12.py, rewrite/alexandria-library.json) and the script's facts_added (Bagnall 2002,
El-Abbadi 1990, Fraser 1972, Canfora 1989, MacLeod 2000, Strabo 17.1.8, Caesar BC 3.111, Seneca Tranq. 9.5, Plutarch Caes. 49,
Gellius 7.17, Dio 42.38, Ammianus 22.16, Galen in Hipp. Epid. III, Athenaeus, Suetonius, Orosius 6.15, Lewis 1990, Witty 1958,
McKenzie et al. 2004, Toomer 1990, Parsons 2007).

Engine workaround (as in lf_voynich.py and lf_atlantis.py): the wall only adds elements to a panel on its first visit, at a beat
start or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom
carries a tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the
shot's additions as a panel item (kit.js builds them on that step's clock). Elements cannot be removed from the wall, so a
picture that must empty or dim is covered (a dark cell over a pigeonhole, a veil over a lit room).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-alexandria/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-alexandria/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-alexandria RC_FILMS_EPS=/tmp/claude-0/sbx_lf-alexandria/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-alexandria/boards python3 films.py long.lf_alexandria
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-alexandria", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
PAPY, PAPY_E, PAPY_D = "#e9d6ad", "#fff1d2", "#c9ad7d"       # papyrus, its lit edge, its shade
SPIRAL = "#8a6a44"                                           # the rolled layers seen at a scroll's end
WOOD, WOOD_D, WOOD_E = "#6b4a30", "#3a281a", "#8a6a48"
STONE, STONE_L, STONE_D = "#d9c29a", "#efe0c0", "#8c7152"
FIRE, FIRE_L, FIRE_D = "#ff9a3a", "#ffd36a", "#e0602a"
SILVER, SILVER_E = "#c9ccd2", "#f2f4f8"
NIGHT = "#0d1220"
GRADE = {"established": "#8fd9b0", "strong": "#b6e08a", "open": "#f0b06a", "ruled": "#e98a8a", "awaiting": "#c9c1ee"}
WPS = 2.5                    # spoken words a second (the narrator's pace, pauses included: LF.10 ran 1,489 words in 582 s)


# ================================================================== narration: the script's own lines, timing
def words(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", s)
    s = re.sub(r"@\w+", "", s).replace("-", " ")
    return [w for w in (re.sub(r"[^\w']", "", x).lower() for x in s.split()) if w]


SAY = {}                     # shot id -> the narration spoken while its step is on screen (set in film())


def T(sid, phrase, lead=.35, k=1):
    """Seconds after the shot's step starts at which `phrase` is said (its k-th occurrence)."""
    ws, ps = words(SAY[sid]), words(phrase)
    hits = [i for i in range(len(ws)) if ws[i:i + len(ps)] == ps]
    assert len(hits) >= k, (sid, phrase, SAY[sid])
    return round(lead + hits[k - 1] / WPS, 2)


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


def gl(x, y, r, at, op=.6, kind="lamp"):
    return glow(round(x, 1), round(y, 1), round(r), round(at, 2), op, kind)


def E(cx, cy, rx, ry, n=36, a0=0, a1=360):
    return [[round(x, 1), round(y, 1)] for x, y in ellipse(cx, cy, rx, ry, n, a0, a1)]


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", scl=True, fx="pop")]


def chip_w(t, size=28):
    return len(t) * size * .56 + 44


def tag(x, y, t, at, c=AMBER, size=26, style="known", a="middle"):
    """A small rounded tag with a few words (dashed for an inference, dotted for a claim)."""
    w = len(t) * size * .55 + 30
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - size * .95, w, size * 1.55, "rgba(18,13,10,.82)", c, 2, size * .7, at, fx="pop", style=style),
            lab(x0 + w / 2, y + size * .2, t, at + .1, c, size, halo=False)]


def tick(x, y, at, c=GREEN, s=1.0, w=6):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": w, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cross(x, y, at, c=RED, s=1.0, w=6):
    return [ln([(x - 14 * s, y - 14 * s), (x + 14 * s, y + 14 * s)], at, c, w, dur=.25), ln([(x + 14 * s, y - 14 * s), (x - 14 * s, y + 14 * s)], at + .15, c, w, dur=.25)]


def qmark(x, y, at, size=90, c=LILAC, halo=True):
    out = [gl(x, y - size * .3, size * 1.1, at, .5)] if halo else []
    return out + [lab(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def bracket(x0, x1, y, at, t=None, c=BONE, up=True, size=26, ty=None, style="known"):
    d = -12 if up else 12
    out = [ln([[x0, y + d], [x0, y], [x1, y], [x1, y + d]], at, c, 2, style, dur=.6)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else (y - 14 if not up else y + 34), t, at + .3, c, size))
    return out


def axis(x0, x1, y, ticks, at, t=None, below=True):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def vbar(x, base, h, wd, c, at, op=None, fx="fill", dur=.5, style="known", edge="none", sw=0):
    """A vertical bar standing on `base`, growing up from it."""
    return rect(x - wd / 2, base - h, wd, h, c, edge, sw or (1.5 if edge != "none" else 0), 3, at, fx=fx, op=op, dur=dur, style=style)


def seated(x, y, h, at, c="#e8d6b8", stool=True, face=1):
    """A figure seated on a stool facing right (face=1) or left; feet on y, h = standing height."""
    f = face
    X = lambda a: x + f * a
    out = []
    if stool:
        out.append(rect(min(X(-.13 * h), X(.07 * h)), y - .25 * h, .2 * h, .25 * h, "#3a2c20", "#8a6a48", 1.5, 3, at, fx="rise"))
    out += [poly([[X(-.07 * h), y - .63 * h], [X(.11 * h), y - .63 * h], [X(.1 * h), y - .29 * h], [X(-.1 * h), y - .29 * h]], c, at=at, fx="rise"),
            poly([[X(-.1 * h), y - .33 * h], [X(.25 * h), y - .33 * h], [X(.26 * h), y - .25 * h], [X(-.1 * h), y - .24 * h]], c, at=at, fx="rise"),
            poly([[X(.19 * h), y - .27 * h], [X(.26 * h), y - .27 * h], [X(.27 * h), y], [X(.18 * h), y]], c, at=at, fx="rise"),
            circ(X(.04 * h), y - .72 * h, .075 * h, c, at=at, fx="rise"),
            ln([[X(.06 * h), y - .58 * h], [X(.2 * h), y - .5 * h], [X(.3 * h), y - .44 * h]], at, c, max(3, .05 * h), draw=False)]
    return out


def crown(x, y, s, at, c=GOLD):
    return poly([[x - s, y], [x - s, y - s * 1.1], [x - s * .5, y - s * .5], [x, y - s * 1.2], [x + s * .5, y - s * .5], [x + s, y - s * 1.1], [x + s, y]], c, at=at, fx="pop")


def shift(els, dy, dx=0):
    """The same elements moved by (dx, dy) (to re-centre a finished composition)."""
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


def static(els):
    """The same elements already in place when the camera arrives (no build-in)."""
    out = []
    for e in els:
        e = dict(e)
        e["in"] = -1
        e.pop("fx", None)
        out.append(e)
    return out


def retime(els, at):
    """The same elements, all appearing at `at` (keeping their effects)."""
    out = []
    for e in els:
        e = dict(e)
        e["in"] = round(at, 2)
        out.append(e)
    return out


def dotrow(x0, x1, y, at, c=LILAC, w=5, gap=12, op=None, style=None):
    """A row of dots as one dashed line (round caps): many marks for the price of one element."""
    e = {"k": "line", "p": R([(x0, y), (x1, y)]), "c": c, "w": w, "dash": "0.1 %s" % gap, "in": round(at, 2)}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


# ------------------------------------------------------------------ scrolls, shelves, books
def scroll_end(x, y, r, at, c=PAPY, fx="pop", op=None, tag_=False):
    """A rolled scroll seen end-on: a disc with its spiral of layers (and, sometimes, the little title tag hanging from it)."""
    out = [circ(x, y, r, c, "#5a4330", 1.2, at, fx, op)]
    sp = []
    for k in range(9):
        a = k * .9
        rr = r * (.15 + .09 * k)
        sp.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    out.append(ln(sp, at, SPIRAL, 1.2, curve=True, draw=False, op=op if op is not None else .8))
    if tag_:
        out += [ln([(x + r * .5, y + r * .7), (x + r * .7, y + r * 1.7)], at, "#5a4330", 1.2, draw=False),
                rect(x + r * .45, y + r * 1.6, r * .8, r * .55, "#c9905a", "#5a4330", 1, 1, at, fx=fx)]
    return out


def scroll_side(x, y, w, h, at, c=PAPY, style="known", fx="pop", op=None, edge="#7a5a36", ink=False):
    """A rolled scroll seen from the side: a long cylinder (x, y = its left end centre), its end disc on the right."""
    if style != "known":
        return [rect(x, y - h / 2, w, h, "rgba(201,193,238,.06)", c, 2.2, h / 2, at, fx=fx, style=style, op=op),
                circ(x + w - h / 2, y, h / 2 - 1, "none", c, 2, at, style=style)]
    out = [rect(x, y - h / 2, w, h, c, edge, 1.2, h / 2, at, fx=fx, op=op),
           rect(x + h * .3, y - h / 2 + 2, w - h * .6, h * .22, PAPY_E, at=at, fx=fx, op=.55 if op is None else op * .55),
           circ(x + w - h / 2, y, h / 2 - 1, PAPY_D, edge, 1, at, fx, op),
           circ(x + w - h / 2, y, h / 5, "none", SPIRAL, 1, at, fx, op)]
    if ink:
        out.append(ln([(x + h * .6, y + h * .18), (x + w - h * 1.1, y + h * .18)], at, "#6a4a30", 1.2, draw=False, op=.6))
    return out


def sheet(x, y, w, h, at, c=PAPY, rows=6, ink="#6a4a30", fx="pop", op=None, seed=1, lw=1.6, gap=None):
    """An open sheet of papyrus with lines of writing (schematic strokes)."""
    out = [rect(x, y, w, h, c, PAPY_E, 1.2, 4, at, fx=fx, op=op)]
    r = random.Random(seed)
    g = gap or h / (rows + 1)
    for k in range(rows):
        yy = y + g * (k + 1)
        xx = x + w * .08
        while xx < x + w * .9:
            L = r.uniform(.06, .2) * w
            L = min(L, x + w * .92 - xx)
            if L > 6:
                out.append(ln([(xx, yy), (xx + L, yy)], at + .05, ink, lw, draw=False, op=.75))
            xx += L + r.uniform(.02, .04) * w
    return out


def pigeonholes(x0, y0, cols, rows, cw, ch, at, fill=1.0, seed=3, step=.0, wood=WOOD, back="#24180f", tags=.2, op=None, order="row"):
    """A wall of wooden pigeonholes, each holding a few scrolls end-on. fill: the share of cells filled; step: seconds between cells
    (row by row, left to right). Returns (elements, list of (cx, cy) cell centres in fill order)."""
    r = random.Random(seed)
    els = [rect(x0 - 10, y0 - 10, cols * cw + 20, rows * ch + 20, wood, WOOD_E, 2, 4, at)]
    els += [rect(x0 + c * cw + 4, y0 + k * ch + 4, cw - 8, ch - 8, back, at=at) for k in range(rows) for c in range(cols)]
    cells = [(c, k) for k in range(rows) for c in range(cols)] if order == "row" else [(c, k) for c in range(cols) for k in range(rows)]
    n = int(round(len(cells) * fill))
    centres = []
    for j, (c, k) in enumerate(cells[:n]):
        cx, cy = x0 + c * cw + cw / 2, y0 + k * ch + ch / 2
        centres.append((cx, cy))
        t = at + .2 + step * j
        rr = min(cw, ch) * .17
        spots = [(-1.1, .55), (0, .55), (1.1, .55), (-.55, -.4), (.55, -.4), (0, -1.3)]
        m = r.randint(3, 6)
        for q, (dx, dy) in enumerate(spots[:m]):
            pc = r.choice([PAPY, "#e2cc9e", "#efdcb4", "#d8c095"])
            els += scroll_end(cx + dx * rr * 1.02, cy + dy * rr * 1.02 + rr * .3, rr, t, pc, op=op, tag_=(q == 0 and r.random() < tags))
    return els, centres


def column(x, base, h, w, at, c=STONE, fx="rise", op=None, ionic=True, flutes=True):
    """A Greek column, feet on `base`: base moulding, a slightly tapering shaft with flutes, an Ionic (or plain) capital."""
    bw, sh = w * 1.3, h * .07
    out = [rect(x - bw / 2, base - sh, bw, sh, c, STONE_D, 1, 2, at, fx=fx, op=op),
           poly([(x - w / 2, base - sh), (x + w / 2, base - sh), (x + w * .42, base - h * .88), (x - w * .42, base - h * .88)], c, STONE_D, 1, at, fx, op)]
    if flutes:
        for k in (-.22, 0, .22):
            out.append(ln([(x + k * w, base - sh - 4), (x + k * w * .85, base - h * .88 + 4)], at, STONE_D, 1, draw=False, op=.5))
    out.append(rect(x - w * .62, base - h, w * 1.24, h * .12, STONE_L, STONE_D, 1, 2, at, fx=fx, op=op))
    if ionic:
        out += [circ(x - w * .55, base - h * .93, w * .17, STONE_L, STONE_D, 1, at, fx, op), circ(x + w * .55, base - h * .93, w * .17, STONE_L, STONE_D, 1, at, fx, op)]
    return out


def flame(x, y, h, at, style="known", c=FIRE, inner=FIRE_L, op=None, fx="pop", seed=0):
    """A flame standing on (x, y), h tall; dotted lilac outline when it is a claim."""
    r = random.Random(seed)
    w = h * .42
    pts = [(x - w, y), (x - w * .9, y - h * .3), (x - w * .45, y - h * .55), (x - w * .55, y - h * .75), (x - w * .1, y - h * .62),
           (x + w * .05 * r.uniform(-1, 1), y - h), (x + w * .3, y - h * .66), (x + w * .6, y - h * .8), (x + w * .55, y - h * .5),
           (x + w * .95, y - h * .28), (x + w, y)]
    if style != "known":
        return [poly(pts, "rgba(201,193,238,.07)", LILAC if c == FIRE else c, 2.2, at, fx, op, curve=True, style=style)]
    inn = [(x - w * .5, y), (x - w * .45, y - h * .3), (x - w * .1, y - h * .5), (x + w * .02, y - h * .66), (x + w * .2, y - h * .45), (x + w * .5, y - h * .25), (x + w * .5, y)]
    return [poly(pts, c, FIRE_D, 1.2, at, fx, op, curve=True), poly(inn, inner, at=at, fx=fx, op=op, curve=True)]


def fire(x, y, h, at, seed=0, n=3, spread=None, glow_r=None, op=.85):
    """A small blaze: a glow and a few flames."""
    r = random.Random(seed)
    sp = spread or h * .7
    out = [gl(x, y - h * .4, glow_r or h * 2.2, at, op, "fire")]
    for k in range(n):
        dx = (k - (n - 1) / 2) * sp / max(1, n - 1) * 1.2 + r.uniform(-.1, .1) * h
        out += flame(x + dx, y, h * r.uniform(.65, 1.0), at + .08 * k, seed=seed + k)
    return out


def smoke(x, y, s, at, seed=0, n=3, c="#3a3438", op=.55):
    r = random.Random(seed)
    return [oval(round(x + r.uniform(-.3, .3) * s + .25 * s * k, 1), round(y - .7 * s * k, 1), round(s * (.5 + .18 * k), 1), round(s * (.32 + .1 * k), 1), c,
                 at=round(at + .25 * k, 2), op=op * (1 - .18 * k)) for k in range(n)]


def galley(x, y, L, at, face=1, c="#4a3426", sail=None, op=None, fx="pop", oars=True):
    """A Hellenistic war galley on the water line y, L long, bow to the right (face=1): ram, curved stern, oars, a mast and a furled sail."""
    f = face
    P = lambda a, b: (x + f * a * L, y + b * L)
    hull = [P(-.5, -.1), P(-.56, -.2), P(-.52, -.26), P(-.46, -.12), P(.34, -.12), P(.47, -.16), P(.5, -.06), P(.56, .0), P(.44, .01), P(.36, .05), P(-.4, .05)]
    out = [poly(hull, c, "#c9a06a", 1.4, at, fx, op)]
    out.append(ln([P(-.42, -.12), P(.36, -.12)], at, "#c9a06a", 1.2, draw=False, op=.7 if op is None else op))
    if oars:
        for k in range(9):
            a = -.32 + k * .075
            out.append(ln([P(a, -.03), P(a - .05, .1)], at, "#2a1c12", 2, draw=False, op=op))
    out.append(ln([P(.0, -.12), P(.0, -.62)], at, "#2a1c12", 3, draw=False, op=op))
    out.append(ln([P(-.2, -.56), P(.2, -.56)], at, "#5a4030", 3, draw=False, op=op))
    if sail:
        out.append(poly([P(-.19, -.56), P(.19, -.56), P(.16, -.5), P(-.16, -.5)], sail, at=at, fx=fx, op=op))
    return out


def merchantman(x, y, L, at, face=1, c="#5a4030", sail="#efe3c8", op=None, fx="pop"):
    """A round-hulled merchant ship with a square sail set."""
    f = face
    P = lambda a, b: (x + f * a * L, y + b * L)
    hull = [P(-.5, -.16), P(-.42, -.1), P(.38, -.1), P(.5, -.2), P(.46, -.04), P(.3, .06), P(-.36, .06), P(-.48, -.04)]
    return [poly(hull, c, "#c9a06a", 1.4, at, fx, op, curve=False),
            ln([P(.0, -.1), P(.0, -.78)], at, "#2a1c12", 3, draw=False, op=op),
            poly([P(-.24, -.72), P(.24, -.72), P(.27, -.24), P(-.27, -.24)], sail, "#b9a77f", 1.2, at, fx, op),
            ln([P(-.26, -.72), P(.26, -.72)], at, "#5a4030", 3, draw=False, op=op)]


def wreath_head(x, y, s, at, c="#e8d6b8", face=1, leaf=GREEN):
    """A profile head with a laurel wreath (Caesar, a Roman): head circle, neck, nose, the wreath's leaves."""
    f = face
    out = [circ(x, y, s, c, at=at, fx="pop"), poly([(x - .45 * s, y + .7 * s), (x + .35 * s, y + .75 * s), (x + .3 * s, y + 1.5 * s), (x - .5 * s, y + 1.5 * s)], c, at=at, fx="pop"),
           poly([(x + f * .95 * s, y - .1 * s), (x + f * 1.22 * s, y + .22 * s), (x + f * .92 * s, y + .3 * s)], c, at=at, fx="pop")]
    for k in range(7):
        a = math.radians(200 + 22 * k) if f > 0 else math.radians(-20 - 22 * k)
        lx, ly = x + 1.02 * s * math.cos(a), y + 1.02 * s * math.sin(a)
        out.append(oval(round(lx, 1), round(ly, 1), round(s * .2, 1), round(s * .1, 1), leaf, at=round(at + .1, 2)))
    return out


def coin(x, y, r, at, c=AU, rim="#fff1c0", head=True, op=None):
    out = [circ(x, y, r, c, rim, 1.5, at, "pop", op)]
    if head:
        out += [circ(x - r * .1, y - r * .1, r * .38, "none", "#8a6a20", 1.4, at, "pop", op), ln([(x - r * .4, y + r * .45), (x + r * .25, y + r * .45)], at, "#8a6a20", 1.4, draw=False, op=op)]
    return out


def silver_bar(x, y, w, at, op=None):
    h, d = w * .3, w * .28
    return [poly([(x, y), (x + w, y), (x + w + d * .5, y - d * .4), (x + d * .5, y - d * .4)], SILVER_E, "#ffffff", 1, at, "pop", op),
            rect(x, y, w, h, SILVER, SILVER_E, 1, 2, at, fx="pop", op=op),
            poly([(x + w, y), (x + w + d * .5, y - d * .4), (x + w + d * .5, y + h - d * .4), (x + w, y + h)], "#8f949c", at=at, fx="pop", op=op)]


def mask(x, y, s, at, c="#efe3c8", eye="#1a120c", op=None, fx="pop"):
    """A theatre mask, face on: the face, two eye holes, an open mouth."""
    return [poly(E(x, y, s, s * 1.12, 20), c, "none", 0, at, fx, op, curve=True),
            oval(round(x - s * .38, 1), round(y - s * .18, 1), round(s * .2, 1), round(s * .12, 1), eye, at=round(at, 2)),
            oval(round(x + s * .38, 1), round(y - s * .18, 1), round(s * .2, 1), round(s * .12, 1), eye, at=round(at, 2)),
            oval(round(x, 1), round(y + s * .5, 1), round(s * .3, 1), round(s * .16, 1), eye, at=round(at, 2))]


def quill(x, y, s, at, c=LILAC, style="claimed"):
    """A quill, nib at (x, y), feather up and to the right: a shaft and a leaf-shaped vane."""
    k = s / 100.
    vane = [(x + 14 * k, y - 22 * k), (x + 8 * k, y - 46 * k), (x + 22 * k, y - 76 * k), (x + 52 * k, y - 104 * k), (x + 82 * k, y - 112 * k),
            (x + 76 * k, y - 88 * k), (x + 58 * k, y - 60 * k), (x + 34 * k, y - 34 * k)]
    fill = "rgba(201,193,238,.16)" if style != "known" else "rgba(245,236,220,.22)"
    return [poly(vane, fill, c, 2.2, at, "pop", curve=True, style=style),
            ln([(x, y), (x + 80 * k, y - 110 * k)], at, c, 2.2, style, draw=False),
            poly([(x - 3 * k, y - 6 * k), (x + 3 * k, y - 10 * k), (x, y + 4 * k)], c, at=at, fx="pop")]


def book(x, y, w, h, at, c="#7a4a2a", edge="#c9a06a", fx="pop", op=None, pages=True):
    """A closed codex standing upright (cover facing us)."""
    out = [rect(x, y, w, h, c, edge, 1.5, 4, at, fx=fx, op=op)]
    if pages:
        out += [ln([(x + w * .18, y + 4), (x + w * .18, y + h - 4)], at, "rgba(255,236,206,.35)", 1.5, draw=False, op=op),
                rect(x + w * .35, y + h * .2, w * .45, h * .12, "rgba(255,236,206,.25)", at=at, fx=fx, op=op)]
    return out


def open_codex(cx, y, pw, ph, at, page="#efe3c8", fx="pop", op=None):
    return [rect(cx - pw - 8, y - 6, 2 * pw + 16, ph + 14, "#4a3020", "#8a6a48", 2, 6, at, fx=fx, op=op),
            rect(cx - pw, y, pw, ph, page, "#fff6e6", 1, 3, at, fx=fx, op=op), rect(cx, y, pw, ph, page, "#fff6e6", 1, 3, at, fx=fx, op=op),
            ln([(cx, y), (cx, y + ph)], at, "rgba(90,60,30,.6)", 2, draw=False, op=op)]


def scribe(x, y, h, at, c="#e8d6b8", face=1, desk=True):
    """A scribe seated at a low desk, writing on a sheet (x, y = feet)."""
    out = seated(x, y, h, at, c, face=face)
    if desk:
        f = face
        dx = x + f * .42 * h
        out += [rect(min(dx - .2 * h, dx + .2 * h), y - .42 * h, .4 * h, .05 * h, WOOD, WOOD_E, 1, 2, at, fx="rise"),
                ln([(dx - .16 * h, y - .37 * h), (dx - .16 * h, y)], at, WOOD, 3, draw=False), ln([(dx + .16 * h, y - .37 * h), (dx + .16 * h, y)], at, WOOD, 3, draw=False),
                rect(dx - .15 * h, y - .46 * h, .3 * h, .04 * h, PAPY, at=at, fx="rise")]
    return out


def lamp(x, y, s, at, op=.6, fx="pop"):
    """An oil lamp on a stand: the stand, the lamp, its flame and glow (x, y = foot of the stand)."""
    return [ln([(x, y), (x, y - s)], at, "#8a6a48", max(2, s * .03), draw=False), rect(x - s * .12, y - 6, s * .24, 6, "#8a6a48", at=at, fx=fx),
            poly([(x - s * .14, y - s), (x + s * .16, y - s), (x + s * .1, y - s * 1.07), (x - s * .1, y - s * 1.07)], "#b88a4a", at=at, fx=fx),
            poly([(x + s * .08, y - s * 1.07), (x + s * .12, y - s * 1.22), (x + s * .16, y - s * 1.07)], FIRE_L, at=at, fx=fx, curve=True),
            gl(x + s * .12, y - s * 1.12, s * 1.6, at, op)]


def figure(x, y, h, at, c="#e8d6b8", fx="rise", op=None):
    p = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        p.update(op=op, keepop=True)
    return p


def iso_proj(az, el, s, ox, oy):
    """Python twin of kit.js EL.iso's projection (spin 0): world (x, y up, z) -> panel point."""
    a = math.radians(az)
    ca, sa, c30 = math.cos(a), math.sin(a), math.cos(math.pi / 6)

    def P(x, y, z):
        xr, zr = x * ca - z * sa, x * sa + z * ca
        return (round(ox + (xr - zr) * c30 * s, 1), round(oy - y * s + (xr + zr) * el * s, 1))
    return P


# ================================================================== cold open: the burning harbour, the hall of the legend, five endings
LIB_X = (60, 700)            # the colonnaded hall of the legend on the hill at the left of the harbour (s1, s2)


def lighthouse(x, base, at, op=None, fx=None, s=1.0, lit=True):
    """The Pharos: a square tapering base tier, an octagonal middle, a round top with its beacon and a statue (x = axis, base = foot)."""
    k = s
    out = [poly([(x - 55 * k, base), (x + 55 * k, base), (x + 47 * k, base - 230 * k), (x - 47 * k, base - 230 * k)], "#bfae92", at=at, fx=fx, op=op),
           poly([(x + 6 * k, base), (x + 55 * k, base), (x + 47 * k, base - 230 * k), (x + 5 * k, base - 230 * k)], "#8f7e66", at=at, fx=fx, op=op),
           rect(x - 56 * k, base - 242 * k, 112 * k, 14 * k, "#d8c8aa", "#6b5a44", 1, 2, at, fx=fx, op=op),
           poly([(x - 33 * k, base - 242 * k), (x + 33 * k, base - 242 * k), (x + 29 * k, base - 342 * k), (x - 29 * k, base - 342 * k)], "#c9b89a", at=at, fx=fx, op=op),
           poly([(x + 10 * k, base - 242 * k), (x + 33 * k, base - 242 * k), (x + 29 * k, base - 342 * k), (x + 9 * k, base - 342 * k)], "#958468", at=at, fx=fx, op=op),
           ln([(x - 14 * k, base - 242 * k), (x - 12 * k, base - 342 * k)], at, "#6b5a44", 1, draw=False, op=op),
           rect(x - 36 * k, base - 352 * k, 72 * k, 10 * k, "#d8c8aa", "#6b5a44", 1, 2, at, fx=fx, op=op),
           rect(x - 18 * k, base - 398 * k, 36 * k, 46 * k, "#c9b89a", "#6b5a44", 1, 3, at, fx=fx, op=op),
           poly([(x - 20 * k, base - 398 * k), (x + 20 * k, base - 398 * k), (x, base - 412 * k)], "#a89676", at=at, fx=fx, op=op),
           figure(x, base - 412 * k, 34 * k, at, "#a89676", None, op)]
    for row in range(3):
        for j in (-1, 1):
            out.append(rect(x + j * 16 * k - 5 * k, base - (60 + 60 * row) * k, 10 * k, 18 * k, "#2a2018", at=at, fx=fx, op=op))
    if lit:
        out += [rect(x - 12 * k, base - 390 * k, 24 * k, 26 * k, FIRE_L, at=at, fx=fx, op=op), gl(x, base - 378 * k, 170 * k, at, .85, "fire"),
                gl(x, base - 378 * k, 420 * k, at, .22, "lamp")]
    return out


def hall_front(x0, x1, base, at, n=10, lit=True, fx=None, op=None):
    """The library as the legend pictures it: a long colonnaded hall on a stepped podium, shelves of scrolls glowing behind the columns."""
    w = x1 - x0
    h = 170
    out = []
    if lit:
        out += [rect(x0 + 20, base - h - 2, w - 40, h + 2, "#3a2414", at=at, fx=fx, op=op)]
        els, _ = pigeonholes(x0 + 34, base - h + 22, 22, 4, (w - 68) / 22, 30, at, fill=.92, seed=8, wood="#5a3a22", back="#2a1a10", tags=0, op=op)
        out += [dict(e, **{"in": at}) for e in els if e.get("in") is not None]
        out += [gl(x0 + w * f, base - h * .45, 150, at, .45) for f in (.2, .5, .8)]
    for k in range(3):
        out.append(rect(x0 - 10 * k, base + 13 * k, w + 20 * k, 14, "#b8a586" if k == 0 else "#a39072", "#6b5a44", 1, 1, at, fx=fx, op=op))
    pitch = (w - 60) / (n - 1)
    for j in range(n):
        out += column(x0 + 30 + j * pitch, base, h, 22, at, "#cdb994", fx=fx, op=op)
    out += [rect(x0 + 4, base - h - 30, w - 8, 30, "#d8c4a0", "#6b5a44", 1, 2, at, fx=fx, op=op),
            ln([(x0 + 4, base - h - 18), (x1 - 4, base - h - 18)], at, "#8c7152", 1.2, draw=False, op=op)]
    mx = (x0 + x1) / 2
    out.append(poly([(mx - w * .3, base - h - 30), (mx + w * .3, base - h - 30), (mx, base - h - 90)], "#d8c4a0", "#6b5a44", 1.2, at, fx, op))
    out.append(poly([(mx - w * .24, base - h - 36), (mx + w * .24, base - h - 36), (mx, base - h - 80)], "#bda884", at=at, fx=fx, op=op))
    return out


def warehouse(x, base, w, h, at, c="#4a3a30"):
    return [rect(x, base - h, w, h, c, "#7a6450", 1.2, 2, at), poly([(x - 6, base - h), (x + w + 6, base - h), (x + w / 2, base - h - h * .4)], "#5a463a", "#7a6450", 1.2, at),
            rect(x + w * .4, base - h * .55, w * .2, h * .55, "#1a120c", at=at)]


QUAY = (620, 1300, 602)      # x0, x1 and top of the stone quay of the harbour (s1)
GALLEYS = [(690, 1), (870, -1), (1050, 1), (1230, -1)]


def s1():
    """THE HERO IMAGE, drawn from the first frame: Alexandria's harbour at night, the Pharos on the right, war galleys at the quay,
    warehouses, and on the hill at the left the colonnaded hall of the legend. The galleys catch fire one by one; then the docks."""
    els = [rect(-10, -10, 1800, 1020, "url(#k-sky-night)", at=-1),
           {"k": "stars", "n": 150, "x0": 0, "x1": 1778, "y0": 0, "y1": 500, "seed": 5, "in": -1},
           circ(1190, 170, 24, "#efe8da", at=-1), gl(1190, 170, 120, -1, .3)]
    r = random.Random(11)
    sky = [(-10, 590)]
    x = -10
    while x < 1800:
        hh = r.uniform(20, 60)
        sky += [(x, 590 - hh), (x + r.uniform(40, 90), 590 - hh)]
        x = sky[-1][0]
    sky += [(1800, 590)]
    els.append(poly(sky, "#191521", at=-1))
    for _ in range(26):
        wx, wy = r.uniform(740, 1340), r.uniform(548, 580)
        els.append(rect(wx, wy, 6, 8, AMBER, at=-1, op=.45))
    els.append(poly([(-20, 470), (180, 500), (420, 520), (640, 548), (760, 600), (760, 640), (-20, 640)], "#1c1712", at=-1))
    els += hall_front(LIB_X[0], LIB_X[1], 560, -1)
    els += [rect(-10, 612, 1800, 420, "url(#k-sea)", at=-1), rect(-10, 612, 1800, 120, "#2a4a5e", at=-1, op=.35),
            {"k": "water", "y": 612, "h": 6, "op": .6, "in": -1}]
    els += [ln([(1190, 640), (1190, 990)], -1, "#efe8da", 22, draw=False, op=.07), ln([(380, 640), (380, 940)], -1, AMBER, 60, draw=False, op=.06)]
    x0, x1, qy = QUAY
    els += [rect(x0, qy, x1 - x0, 22, "#6b5a44", "#a08a6a", 1.2, 2, -1), rect(x0, qy + 22, x1 - x0, 10, "#3a3028", at=-1)]
    els += [ln([(xx, qy + 2), (xx, qy + 20)], -1, "#4a3e32", 1.2, draw=False) for xx in range(x0 + 40, x1, 60)]
    for k in range(6):
        els += warehouse(x0 + 20 + k * 112, qy, 92, 58, -1, "#3e3229" if k % 2 else "#463a30")
    isle = [(1330, 650), (1360, 616), (1430, 606), (1500, 602), (1600, 604), (1690, 612), (1760, 626), (1800, 640), (1800, 680), (1330, 680)]
    els.append(poly(isle, "#2a2420", "#4a3e34", 1.2, -1))
    els += lighthouse(1540, 606, -1)
    els += [ln([(1540, 640), (1540, 980)], -1, "#ffd36a", 16, draw=False, op=.16)]
    els += [ln([(x, y), (x + r.uniform(30, 70), y)], -1, "#9fd0e0", 1.5, draw=False, op=.22) for x, y in
            [(r.uniform(0, 1700), r.uniform(720, 980)) for _ in range(40)]]
    for gx, f in GALLEYS:
        els += galley(gx, 694, 178, -1, f, c="#3e2c20", sail="#a08c70")
    t0, t1 = T("s1", "sets the ships"), T("s1", "spread to the docks")
    for k, (gx, f) in enumerate(GALLEYS):
        t = round(t0 + .1 + .4 * k, 2)
        els += fire(gx, 676, 84, t, seed=k, n=3, glow_r=200) + [ln([(gx, 712), (gx, 960)], t + .2, FIRE, 46, draw=False, op=.16), gl(gx, 780, 130, t + .2, .3, "fire")]
        els += smoke(gx + 14, 520, 70, t + 1.0, seed=k, n=3, c="#8a7a78", op=.2)
    for k in range(6):
        t = round(t1 + .25 * k, 2)
        els += fire(x0 + 66 + k * 112, qy - 50, 46, t, seed=10 + k, n=2, glow_r=120)
    return {"base": "dark", "cam": CAM, "els": els}


def s2_add():
    """The legend: dotted lilac flames climb over the hall; a tag 'the story'."""
    tb = T("s2", "story goes")
    tg = T("s2", "burned to the ground")
    out = tag(380, 650, "the story goes", tb, LILAC, 28, "claimed")
    spots = [(150, 392, 100), (260, 382, 130), (380, 302, 92), (500, 384, 128), (610, 394, 100), (320, 372, 112), (440, 372, 118)]
    for k, (x, y, h) in enumerate(spots):
        f = flame(x, y, h, round(tg - .6 + .18 * k, 2), style="claimed", seed=20 + k)
        f[0]["w"] = 3.2
        out += f
    out.append(gl(380, 330, 380, tg - .3, .25, "blue"))
    return out


HALL = (330, 160, 10, 5, 112, 84)    # pigeonhole wall of the hall: x0, y0, cols, rows, cell w, cell h


def hall_room(at=-1, fill=1.0, seed=3, lit=True):
    """The hall of scrolls as the legend imagines it: two great columns, a wall of pigeonholes, a floor in perspective, a reading table."""
    x0, y0, cols, rows, cw, ch = HALL
    els = [rect(-10, -10, 1800, 1020, "#2a1d14", at=at), rect(-10, 640, 1800, 380, "#1e150f", at=at)]
    for x in range(-1300, 3100, 190):
        t = (1000 - 640) / (1000 - 380)
        els.append(ln([(x, 1000), (x + (889 - x) * t, 640)], at, "#3a2a1c", 2, draw=False))
    for y in (668, 712, 776, 860):
        els.append(ln([(-10, y), (1790, y)], at, "#3a2a1c", 2, draw=False))
    if lit:
        els.append(gl(889, 420, 900, at, .3))
    wall, cells = pigeonholes(x0, y0, cols, rows, cw, ch, at, fill=fill, seed=seed)
    els += wall
    for x in (210, 1568):
        els += column(x, 640, 530, 74, at, "#cdb994", fx=None)
    els += [rect(120, 96, 1538, 22, "#cdb994", "#6b5a44", 1, 2, at)]
    return els, cells


def s3():
    """Inside the legend's hall: the wall of scrolls empties cell by cell as the question is asked; five small flames, each with a
    question mark, pop across the empty wall on 'which fire?'."""
    els, cells = hall_room(-1)
    els += [rect(780, 628, 220, 12, WOOD, WOOD_E, 1, 2, -1), ln([(800, 640), (800, 700)], -1, WOOD, 5, draw=False), ln([(980, 640), (980, 700)], -1, WOOD, 5, draw=False)]
    els += static(seated(735, 700, 150, -1, "#d8c4a4", face=1) + seated(1045, 700, 150, -1, "#cdb894", face=-1))
    els += static(scroll_side(812, 616, 90, 16, -1) + scroll_side(905, 618, 70, 14, -1))
    els += static(lamp(890, 628, 46, -1))
    x0, y0, cols, rows, cw, ch = HALL
    tq, tw = T("s3", "lose a whole library"), T("s3", "which fire")
    order = list(range(len(cells)))
    random.Random(5).shuffle(order)
    for j, i in enumerate(order):
        cx, cy = cells[i]
        els.append(rect(cx - cw / 2 + 3, cy - ch / 2 + 3, cw - 6, ch - 6, "#160e09", at=round(tq - .5 + .034 * j, 2), dur=.3))
    for k, x in enumerate((452, 646, 840, 1034, 1228)):
        t = round(tw + .1 * k, 2)
        els += fire(x + cw / 2 - 56, 470, 70, t, seed=30 + k, n=2, glow_r=110) + [lab(x + cw / 2 - 56, 360, "?", t + .2, LILAC, 54, st="big", fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def XM(yr):
    """The master timeline: 300 BCE to 1300 CE across the panel."""
    return round(140 + (yr + 300) * 1500 / 1600, 1)


def ruin_icon(x, y, s, at, c=STONE):
    """A broken wall: three blocks standing, one fallen, a crack."""
    return [rect(x - s, y - s * .9, s * .6, s * .9, c, STONE_D, 1, 2, at, fx="pop"), rect(x - s * .35, y - s * .55, s * .55, s * .55, c, STONE_D, 1, 2, at, fx="pop"),
            poly([(x + s * .3, y), (x + s * .95, y - s * .1), (x + s * 1.0, y - s * .45), (x + s * .35, y - s * .38)], c, STONE_D, 1, at, "pop"),
            ln([(x - s * .7, y - s * .9), (x - s * .55, y - s * .5), (x - s * .75, y - s * .2)], at, "#3a2a1c", 2, draw=False)]


def temple_icon(x, y, s, at, c=STONE, style="known", op=None):
    out = [rect(x - s, y - s * .14, s * 2, s * .14, c, STONE_D, 1, 1, at, fx="pop", op=op)]
    for k in range(4):
        out.append(rect(x - s * .8 + k * s * .5 - s * .08, y - s * 1.0, s * .16, s * .86, c, at=at, fx="pop", op=op))
    out.append(poly([(x - s * 1.05, y - s), (x + s * 1.05, y - s), (x, y - s * 1.45)], c, STONE_D, 1, at, "pop", op))
    return out


def endings_row(y, at, gap=.3, tags=True, k=1.0):
    """The five endings on the master timeline: icons above the axis at y, dates below in two rows."""
    marks = [(-145, "145 BCE", 0), (-48, "48 BCE", 1), (272, "270s", 0), (391, "391", 1), (642, "642", 0)]
    out = []
    for k, (yr, t, row) in enumerate(marks):
        x = XM(yr)
        a = round(at + gap * k, 2)
        out.append(ln([(x, y - 8), (x, y + 8)], a, GOLD, 3, draw=False))
        if k == 0:
            out += [crown(x, y - 40, 26, a), gl(x, y - 60, 70, a, .4)]
        elif k == 1:
            out += fire(x, y - 22, 70, a, seed=3, n=2, glow_r=110)
        elif k == 2:
            out += ruin_icon(x, y - 22, 40, a)
        elif k == 3:
            out += temple_icon(x, y - 24, 36, a)
        else:
            out += flame(x, y - 22, 84, a, style="claimed")
        if tags:
            out.append(lab(x, y + 48 + 36 * row, t, a + .1, GOLD if k < 4 else LILAC, 26))
    return out


def s4():
    """The master timeline, 300 BCE to 1300 CE: five endings pop; a bracket, nearly 800 years; a dotted arc from 642 to about 1200,
    where a quill pops: first written."""
    ay = 610
    t5, t8, t1, t6 = T("s4", "five endings"), T("s4", "nearly eight hundred"), T("s4", "One of them"), T("s4", "six hundred years later")
    els = [axis(110, 1670, ay, [], .2)] + [ln([(XM(yr), ay - 6), (XM(yr), ay + 6)], .2, MUTED, 1.5, draw=False, op=.6) for yr in range(-300, 1301, 100)]
    els += endings_row(ay, t5)
    els += bracket(XM(-145), XM(642), ay - 170, t8, "nearly 800 years", GOLD, up=False, size=30, ty=ay - 194)
    arc = [(XM(642) + 10, ay - 110), (XM(800), ay - 280), (XM(1000), ay - 310), (XM(1203) - 10, ay - 80)]
    els += [ln(arc, t1, LILAC, 3, "claimed", dur=1.6, curve=True), *quill(XM(1203), ay - 18, 70, t6), lab(XM(1203), ay + 48, "first written, c. 1200", t6 + .2, LILAC, 26),
            gl(XM(1203), ay - 40, 120, t6, .45, "blue")]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}



# ================================================================== chapter 1: every book in the world
V6 = View(12, 42, 29.5, 41.5, rect=(90, 130, 1600, 660))


def nile(v, at, c="#6fb6d6"):
    trunk = [v.p(31.3, 29.5), v.p(31.25, 29.9), v.p(31.15, 30.15)]
    ros = [v.p(31.15, 30.15), v.p(30.85, 30.6), v.p(30.55, 31.05), v.p(30.4, 31.45)]
    dam = [v.p(31.15, 30.15), v.p(31.3, 30.6), v.p(31.6, 31.05), v.p(31.82, 31.45)]
    return [ln(q, at, c, 3, curve=True, draw=False) for q in (trunk, ros, dam)]


def s6():
    """Map of the eastern Mediterranean: Alexander's route from Macedonia to Egypt (dotted, schematic), Alexandria founded in
    331 BCE, and a crown for Ptolemy, king of Egypt."""
    v = V6
    ta, tf, tk = T("s6", "Alexander the Great"), T("s6", "founded Alexandria"), T("s6", "made himself king")
    route = [v.p(22.5, 40.76), v.p(26.4, 40.25), v.p(31.0, 39.2), v.p(36.1, 36.9), v.p(35.25, 33.3), v.p(34.4, 31.5), v.p(32.4, 30.9), v.p(31.25, 29.9), v.p(30.4, 30.7), v.p(29.92, 31.2)]
    ax, ay = v.p(29.92, 31.2)
    px, py = v.p(22.5, 40.76)
    ex, ey = v.p(31.0, 29.9)
    els = [{"k": "map", "land": v.land(), "in": -1}] + nile(v, -1)
    els += [lab(px - 10, py - 22, "Macedonia", .5, MUTED, 28, st="ital"), dot(round(px, 1), round(py, 1), 7, MUTED, .5)]
    els += [ln(route, ta, GOLD, 3, "claimed", dur=2.4, curve=True)]
    els += [{"k": "pin", "x": ax, "y": ay, "t": "Alexandria", "c": GOLD, "in": tf, "lx": -24, "ly": -18, "a": "end"},
            lab(ax - 24, ay + 22, "331 BCE", tf + .3, GOLD, 26, "end"), gl(ax, ay, 140, tf, .6)]
    els += [crown(ex + 40, ey - 6, 26, tk), lab(ex + 80, ey + 4, "Ptolemy, king of Egypt", tk + .25, GOLD, 30, "start"), gl(ex + 40, ey - 20, 110, tk, .5)]
    els += [{"k": "scale", "x": 140, "y": 770, "w": round(v.km(300), 1), "t": "300 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


# the city plan (s7), drawn in panel units (1 km = 120 units), schematic but true to the real layout
COAST7 = [(-20, 650), (150, 606), (330, 566), (500, 526), (650, 484), (760, 456), (820, 446), (866, 452), (923, 424), (980, 384), (1038, 340),
          (1078, 298), (1096, 248), (1108, 230), (1124, 256), (1186, 298), (1289, 332), (1461, 378), (1632, 430), (1800, 470)]
PHAROS7 = [(500, 423), (557, 357), (649, 303), (740, 250), (792, 206), (815, 217), (797, 263), (706, 330), (603, 397), (534, 443)]
HEPTA7 = [(716, 318), (736, 306), (830, 444), (812, 452)]
LAKE7 = [(-20, 790), (200, 768), (450, 728), (700, 698), (950, 680), (1200, 678), (1450, 698), (1650, 728), (1800, 748)]
WALL7 = [(565, 660), (565, 512), (650, 484), (760, 456), (820, 446), (866, 452), (923, 424), (980, 384), (1038, 340), (1078, 298), (1096, 248),
         (1108, 236), (1124, 258), (1186, 298), (1289, 332), (1350, 348), (1350, 646), (1100, 656), (850, 662)]
PALACE7 = [(930, 420), (980, 384), (1038, 340), (1078, 298), (1096, 248), (1108, 236), (1124, 258), (1186, 298), (1252, 320), (1262, 470), (1100, 500), (950, 482)]
SERAP7 = (904, 636)


def coast_y(x):
    for (x0, y0), (x1, y1) in zip(COAST7, COAST7[1:]):
        if x0 <= x <= x1 and x1 > x0:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 470


def tf7(pts, k=1.0, c=(0, 0), o=(0, 0)):
    """A zoom of the city plan: points scaled by k about c, then put at o."""
    return [(o[0] + (x - c[0]) * k, o[1] + (y - c[1]) * k) for x, y in pts]


def city(at=-1, k=1.0, c=(0, 0), o=(0, 0), streets=True, walls=True, palace_fill=None):
    """The ancient city, schematic: land, Pharos island and its causeway, the walled city with its street grid and main street,
    Lake Mareotis."""
    F = lambda pts: tf7(pts, k, c, o)
    land = F(COAST7) + [(1800 if k == 1 else o[0] + (1800 - c[0]) * k, 2400), (-400, 2400)]
    els = [poly(land, "#3a2f24", "#c9ad85", 1.6, at), poly(F(PHAROS7), "#3a2f24", "#c9ad85", 1.6, at), poly(F(HEPTA7), "#3a2f24", "#c9ad85", 1.2, at)]
    lake = F(LAKE7) + [(F([(1800, 0)])[0][0], 2400), (F([(-20, 0)])[0][0], 2400)]
    els.append(poly(lake, "#1f3c3a", "#6fb6a6", 1.5, at))
    r = random.Random(7)
    blocks = []
    for gy in (474, 522, 570, 614):
        for gx in range(572, 1346, 62):
            if coast_y(gx + 31) + 18 < gy and gy + 40 < 660:
                for q in range(2):
                    bw, bh = r.uniform(18, 26), r.uniform(12, 18)
                    bx, by = gx + 6 + q * 28, gy + 6 + r.uniform(0, 14)
                    blocks.append(poly(F([(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh)]), "#5a4a3a", at=at, op=.75 if k == 1 else .45))
    els += blocks
    if streets:
        g = []
        for y in (500, 548, 596, 640):
            xs = [x for x in range(570, 1346, 4) if coast_y(x) + 14 < y]
            if xs:
                g.append([(xs[0], y), (xs[-1], y)])
        for x in range(600, 1346, 62):
            y0 = coast_y(x) + 14
            if y0 < 640:
                g.append([(x, y0), (x, 652)])
        els += [ln(F(q), at, "#c9ad85", 1.1 * max(1, k * .7), draw=False, op=.28) for q in g]
        els.append(ln(F([(570, 578), (1345, 520)]), at, "#e2cfa8", 3 * max(1, k * .6), draw=False, op=.75))
    if walls:
        els.append(ln(F(WALL7), at, "#d8c4a0", 3 * max(1, k * .6), draw=False, op=.7))
        for (wx, wy) in (WALL7[0], WALL7[1], WALL7[16], WALL7[17], (565, 590), (1350, 500)):
            (tx, ty), = F([(wx, wy)])
            els.append(rect(tx - 5 * k, ty - 5 * k, 10 * k, 10 * k, "#d8c4a0", at=at, op=.8))
        for d in ((870, 452, 846, 420), (930, 420, 912, 392), (985, 380, 968, 352)):
            els.append(ln(F([(d[0], d[1]), (d[2], d[3])]), at, "#a89070", 4 * max(1, k * .6), draw=False))
    if palace_fill:
        els.append(poly(F(PALACE7), palace_fill, GOLD, 2.5, at))
    return els


def s7():
    """The city plan: the Great Harbour glows, the lighthouse rises on Pharos, the palace quarter fills with gold."""
    th, tl, tp = T("s7", "great harbour"), T("s7", "lighthouse"), T("s7", "palace quarter")
    els = city(-1)
    els += [gl(955, 330, 230, th, .5, "blue"), lab(965, 345, "Great Harbour", th + .2, BLUE, 30, st="ital")]
    els += lighthouse(792, 214, tl, fx="rise", s=.2) + [gl(792, 140, 120, tl + .2, .6, "fire"), lab(700, 190, "Pharos", tl + .3, GOLD, 30, "end")]
    els += [poly(PALACE7, "rgba(242,201,142,.28)", GOLD, 2.5, tp, "fill", dur=.8),
            lab(1150, 420, "palace quarter", tp + .3, GOLD, 30)]
    els += [lab(1210, 745, "Lake Mareotis", .6, BLUE, 26, st="ital"), {"k": "scale", "x": 140, "y": 772, "w": 120, "t": "1 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


# the Mouseion as a model (iso): a courtyard ringed by a colonnade, a hall with a half-circle of seats, a dining hall
MUS = dict(x=930, y=540, s=10.6, az=-32, el=.42)
MP = iso_proj(MUS["az"], MUS["el"], MUS["s"], MUS["x"], MUS["y"])


def mouseion_items(tint=None):
    stone = tint or "#d8c4a0"
    roof = tint or "#b0805a"
    it = [{"t": "slab", "x0": -30, "x1": 30, "z0": -24, "z1": 24, "y": 0, "c": "#4a3a2a"},
          {"t": "flat", "pts": [[-17, -11], [17, -11], [17, 11], [-17, 11]], "y": .05, "c": "#c8b48e"}]
    for x in range(-16, 17, 4):
        for z in (-12.5, 12.5):
            it.append({"t": "cyl", "x": x, "z": z, "y": 0, "r": .45, "h": 4.6, "c": stone, "n": 10})
    for z in range(-8, 9, 4):
        for x in (-18.5, 18.5):
            it.append({"t": "cyl", "x": x, "z": z, "y": 0, "r": .45, "h": 4.6, "c": stone, "n": 10})
    it += [{"t": "box", "x": 0, "z": -15, "y": 4.6, "w": 40, "d": 5, "h": .8, "c": roof},
           {"t": "box", "x": 0, "z": 15, "y": 4.6, "w": 40, "d": 5, "h": .8, "c": roof},
           {"t": "box", "x": -21, "z": 0, "y": 4.6, "w": 5, "d": 25, "h": .8, "c": roof},
           {"t": "box", "x": 21, "z": 0, "y": 4.6, "w": 5, "d": 25, "h": .8, "c": roof},
           {"t": "box", "x": 0, "z": -17.8, "y": 0, "w": 40, "d": .8, "h": 4.6, "c": "#bfa882"}]
    ex = [[6 * math.cos(math.radians(a)), -22 + 6 * math.sin(math.radians(a))] for a in range(180, 361, 20)]
    it += [{"t": "prism", "pts": ex, "y": 0, "h": 4.2, "c": stone, "cw": True},
           {"t": "box", "x": 24.5, "z": 0, "y": 0, "w": 8, "d": 20, "h": 6, "c": stone},
           {"t": "ext", "prof": [[-4.6, 0], [4.6, 0], [0, 3.2]], "d": 21, "x": 24.5, "y": 6, "axis": "z", "at": 0, "c": roof}]
    return it


def mouseion(at=.1, tint=None, light=None):
    els = [{"k": "iso", "items": mouseion_items(tint), "spin": 0, "in": at, **MUS}]
    if light:
        els.insert(0, gl(889, 470, 820, at, light, "lamp"))
    return els


def s8():
    """The Mouseion builds as a model; its name in gold, then the word it gave us."""
    tm, tw = T("s8", "Mouseion"), T("s8", "our word museum")
    els = mouseion(.15, light=.22)
    els += [lab(250, 250, "Mouseion", tm, GOLD, 52, st="serif", fx="pop"), lab(250, 292, "shrine of the Muses", tm + .6, MUTED, 26, st="ital"),
            ln([(250, 316), (250, 366)], tw - .2, MUTED, 2, dur=.3), lab(250, 404, "museum", tw, BONE, 38, st="ital", fx="type", dur=.9)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s9_add():
    """Scholars on the walk and in the hall; gold coins (royal salaries); a long table (free meals); two scholars arguing; then a
    great birdcage of gold bars over the whole building, a bird on its ring."""
    ts, tm, tw, tb = T("s9", "royal salaries"), T("s9", "free meals"), T("s9", "for arguing"), T("s9", "birdcage")
    out = []
    spots = [(-12, 14), (-4, 14), (4, 14), (-18.5, 3), (18.5, -5), (-2, -22.5), (2, -22.5)]
    cs = []
    for j, (x, z) in enumerate(spots):
        px, py = MP(x, 0, z)
        cs.append((px, py))
        out.append(figure(px, py, 50, ts - .6 + .1 * j, "#f6e8cc"))
        out += coin(px, py - 70, 12, ts + .12 * j)
    out += [lab(300, 610, "royal salaries", ts + .9, AU, 28), ln([(340, 584), (cs[3][0] - 14, cs[3][1] - 80)], ts + 1.0, AU, 1.5, "inferred", dur=.4)]
    tx, ty = MP(24.5, 0, 12)
    out += [rect(tx - 80, ty - 22, 160, 12, WOOD, WOOD_E, 1, 2, tm), circ(tx - 46, ty - 30, 10, "#c9905a", at=tm + .1, fx="pop"), circ(tx, ty - 31, 11, PAPY, at=tm + .2, fx="pop"),
            circ(tx + 44, ty - 30, 10, "#c9905a", at=tm + .3, fx="pop"), lab(tx + 10, ty + 34, "free meals", tm + .3, MUTED, 26)]
    ax, ay = MP(9, 0, 15.5)
    bx, by = MP(13, 0, 15.5)
    out += [figure(ax, ay, 52, tw - .3, "#f6e8cc"), figure(bx, by, 52, tw - .2, "#f6e8cc"),
            ln([(ax + 6, ay - 66), (ax + 16, ay - 78), (ax + 24, ay - 64), (ax + 34, ay - 78), (bx - 6, ay - 66)], tw, AMBER, 3, dur=.4)]
    cx, base, top, rx = 930, 700, 200, 560
    for j in range(17):
        f = -1 + 2 * j / 16
        out.append(ln([(cx + rx * f, base), (cx + rx * .64 * f, top + 170), (cx + rx * .22 * f, top + 30), (cx, top)], round(tb + .03 * j, 2), AU, 2.4, curve=True, dur=.7, op=.85))
    out += [ln(E(cx, base, rx, 30, 40, 0, 180), tb, AU, 3, dur=.8, op=.85), ln(E(cx, top + 170, rx * .64, 18, 30, 0, 360), tb + .3, AU, 2, dur=.8, op=.6),
            circ(cx, top - 16, 15, "none", AU, 3, tb + .6, "pop"), lab(1500, 300, "the birdcage", tb + .4, AU, 32, st="ital"), lab(1500, 340, "of the Muses", tb + .5, AU, 32, st="ital")]
    out += [poly([(cx - 16, top - 34), (cx + 6, top - 46), (cx + 20, top - 38), (cx + 30, top - 46), (cx + 26, top - 34), (cx + 6, top - 28)], AU, at=tb + .8, fx="pop")]
    return out


def s10():
    """The library: a long wall of pigeonholes under a colonnade; scrolls pop into the cells row by row until about half are full;
    a gold question mark over the empty half."""
    tl, tq = T("s10", "a library meant"), T("s10", "How do you fill")
    els = [rect(-10, -10, 1800, 1020, "#3a2a1c", at=-1), rect(-10, 650, 1800, 380, "#2a1d14", at=-1), gl(889, 380, 900, -1, .25)]
    for y in (690, 740, 810):
        els.append(ln([(-10, y), (1790, y)], -1, "#3e2c1e", 2, draw=False))
    wall, cells = pigeonholes(250, 190, 12, 6, 106, 72, -1, fill=0.0, seed=12)
    els += wall
    full, _ = pigeonholes(250, 190, 12, 6, 106, 72, tl, fill=.5, seed=12, step=.05, tags=.25)
    els += [e for e in full if e.get("k") != "rect" or e.get("w", 0) < 100]
    for x in (150, 1628):
        els += column(x, 650, 560, 70, -1, "#cdb994", fx=None)
    els += [rect(80, 70, 1618, 24, "#cdb994", "#6b5a44", 1, 2, -1)]
    els += [lab(889, 700, "the library", tl + .5, GOLD, 34, st="serif")] + qmark(1200, 470, tq, 130, GOLD)
    els += [ln([(560, 650), (640, 330)], tl, WOOD_E, 5, draw=False), ln([(610, 650), (690, 330)], tl, WOOD_E, 5, draw=False)]
    els += [ln([(560 + 80 * f, 650 - 320 * f), (610 + 80 * f, 650 - 320 * f)], tl, WOOD_E, 3, draw=False) for f in (.15, .3, .45, .6, .75, .9)]
    els += [figure(652, 470, 120, tl + .2, "#f0e0c4")] + scroll_side(668, 372, 60, 14, tl + .6)
    return {"base": "dark", "cam": CAM, "els": els}


def s11():
    """The quay by day: a merchant ship docks; its scroll goes to a scribe, who copies it; the fresh copy goes back to the ship,
    the original goes into the library, tagged 'from the ships'."""
    tb, tc, tk, to, tlab = T("s11", "Books on any ship"), T("s11", "taken and copied"), T("s11", "kept the originals"), T("s11", "the owners got"), T("s11", "labelled")
    els = [rect(-10, -10, 1800, 610, "url(#k-sky-day)", at=-1), {"k": "water", "y": 600, "h": 440, "op": .9, "in": -1},
           rect(560, 556, 1240, 44, "#8c7a5e", "#b8a586", 1.2, 2, -1), rect(560, 600, 1240, 22, "#5a4a3a", at=-1)]
    els += [ln([(x, 560), (x, 596)], -1, "#6b5a44", 1.2, draw=False) for x in range(600, 1790, 70)]
    els += hall_front(1150, 1720, 556, -1, n=9)
    els += merchantman(300, 646, 440, -1, sail="#efe3c8")
    els += [ln([(470, 600), (580, 566)], -1, WOOD, 8, draw=False)]
    els += scroll_side(250, 570, 110, 26, tb, PAPY_D, edge="#5a4030") + [lab(300, 712, "from a ship", tb + .2, MUTED, 28)]
    els += scribe(840, 556, 200, tb + .5, face=1)
    els += [arrow([[370, 556], [560, 470], [880, 470]], tb + .7, PAPY_D, 4, dur=.8)]
    els += scroll_side(900, 452, 110, 24, tc, PAPY_D, edge="#5a4030") + scroll_side(900, 490, 110, 24, tc + .9, "#fffaf0", edge="#b9a77f") + \
           [ln([(912, 506), (950, 499), (990, 507), (1012, 499)], tc + .5, "#6a4a30", 2.5, dur=.6)]
    els += [arrow([[1020, 440], [1170, 360], [1300, 420]], tk, PAPY_D, 4, dur=.9), gl(1370, 446, 150, tk + .7, .6)]
    els += scroll_side(1312, 450, 110, 24, tk + .8, PAPY_D, edge="#5a4030") + [lab(1366, 414, "original", tk + .9, GOLD, 28)]
    els += [arrow([[900, 530], [700, 640], [380, 610]], to, "#fffaf0", 4, dur=.8)] + scroll_side(250, 606, 110, 24, to + .7, "#fffaf0", edge="#b9a77f") + \
           [lab(420, 642, "copy", to + .8, "#fffaf0", 28, "start")]
    els += tag(1366, 690, "from the ships", tlab, GOLD, 30)
    return {"base": "dark", "cam": CAM, "els": els}


V12 = View(14, 40, 29.8, 39.6, rect=(90, 130, 1600, 660))


def s12():
    """Map Athens to Alexandria: three scrolls named for the three playwrights at Athens; 15 silver bars as the deposit; the originals
    sail to Alexandria and stay there (glowing), fresh copies sail back."""
    v = V12
    tc, ta, ts, te, td, tk, tsb, tsv = (T("s12", p) for p in ("official copies", "Aeschylus", "Sophocles", "Euripides", "fifteen talents", "He kept", "sent back", "keep the silver"))
    xa, ya = v.p(23.73, 37.98)
    xx, yx = v.p(29.92, 31.2)
    route = [(xa + 20, ya + 20), v.p(25.2, 36.9), v.p(27.2, 35.3), v.p(28.8, 33.6), (xx - 4, yx - 18)]
    back = [(xx - 26, yx - 6), v.p(27.6, 33.2), v.p(25.6, 35.0), v.p(24.3, 36.6), (xa + 4, ya + 26)]
    els = [{"k": "map", "land": v.land(), "in": -1},
           {"k": "pin", "x": xx, "y": yx, "t": "Alexandria", "c": GOLD, "in": .4, "lx": 22, "ly": 8},
           {"k": "pin", "x": xa, "y": ya, "t": "Athens", "c": GOLD, "in": tc, "lx": 20, "ly": -14}]
    names = [("Aeschylus", ta), ("Sophocles", ts), ("Euripides", te)]
    for j, (nm, t) in enumerate(names):
        y = ya - 30 + 40 * j
        els += scroll_side(xa - 250, y, 84, 20, t, PAPY_D, edge="#5a4030") + [lab(xa - 260, y + 9, nm, t + .1, BONE, 28, "end")]
    for j in range(15):
        row, col = divmod(j, 5)
        els += silver_bar(xa - 60 + col * 34 - row * 8, ya - 72 - row * 16, 30, round(td + .05 * j, 2))
    els += [lab(xa + 40, ya - 132, "15 talents, about 390 kg", td + .8, SILVER_E, 28)]
    els += [ln(route, tk, GOLD, 3, dur=1.4, curve=True)]
    for j in range(3):
        els += scroll_side(xx + 30, yx - 140 + 34 * j, 84, 20, tk + 1.2 + .15 * j, PAPY_D, edge="#5a4030")
    els += [gl(xx + 72, yx - 106, 160, tk + 1.4, .7), lab(xx + 72, yx - 168, "the originals", tk + 1.6, GOLD, 28)]
    els += [ln(back, tsb, "#fffaf0", 2.5, "inferred", dur=1.4, curve=True)]
    for j in range(3):
        els += scroll_side(xa - 150 + 14 * j, ya + 74 + 22 * j, 74, 16, tsb + 1.2 + .12 * j, "#fffaf0", edge="#b9a77f")
    els += [gl(xa + 10, ya - 100, 170, tsv, .5, "lamp")]
    return {"base": "map", "cam": CAM, "els": els}


SUBJ = ["#d9b87a", "#c98f5a", "#a6b87a", "#8fb0c9", "#c9a0b8", "#d8c4a0", "#b8a0d0", "#9ac0a8", "#d0a070", "#a8b0b8"]
TAB = (720, 170, 930, 470)     # the open sheet of the Tables: x, y, w, h


def s13():
    """The Tables: 120 scrolls in a block coloured by subject; a sheet unrolls with four columns that fill in turn: author (in
    alphabetical order), life, first words, lines."""
    tc, tt, t120, tsub, talp, tlife, tfirst, tlines = (T("s13", p) for p in ("Callimachus", "Tables", "a hundred and twenty", "by subject", "alphabetical",
                                                                              "a line on their life", "first words", "length in lines"))
    els = [gl(889, 430, 900, -1, .18)]
    for row in range(10):
        for col in range(12):
            t = round(t120 + .04 * row + .01 * col, 2)
            els += scroll_end(160 + col * 34, 200 + row * 36, 14, t, SUBJ[row])
    els += [lab(347, 584, "120 scrolls", t120 + .6, GOLD, 30)]
    els += [rect(140, 186 + 36 * r, 410, 30, "none", SUBJ[r], 2, 15, round(tsub + .08 * r, 2), op=.7) for r in range(10)]
    els += scribe(330, 720, 130, tc, face=1) + [lab(470, 700, "Callimachus", tc + .3, BONE, 28, "start")]
    x, y, w, h = TAB
    els += [rect(x - 10, y - 4, 20, h + 8, PAPY_D, "#7a5a36", 1.5, 8, tt), rect(x + w - 10, y - 4, 20, h + 8, PAPY_D, "#7a5a36", 1.5, 8, tt),
            rect(x, y, w, h, PAPY, PAPY_E, 1.2, 4, tt + .2, fx="pop")]
    cols = [("author", x + 70, talp), ("life", x + 290, tlife), ("first words", x + 560, tfirst), ("lines", x + 840, tlines)]
    for nm, cx, t in cols:
        els.append(lab(cx, y + 50, nm, t, "#5a3a20", 26, halo=False))
    els += [ln([(x + 20, y + 66), (x + w - 20, y + 66)], tt + .4, "#8a6a44", 1.5, draw=False)]
    r = random.Random(4)
    for k in range(7):
        yy = y + 112 + 50 * k
        els.append(lab(x + 40, yy + 8, "ABCDEFG"[k], round(talp + .15 * k, 2), "#5a3a20", 26, st="serif", halo=False))
        els.append(ln([(x + 70, yy), (x + 70 + r.uniform(70, 120), yy)], round(talp + .15 * k + .05, 2), "#6a4a30", 2, draw=False))
        els.append(ln([(x + 210, yy), (x + 210 + r.uniform(130, 190), yy)], round(tlife + .12 * k, 2), "#6a4a30", 2, draw=False))
        els.append(ln([(x + 450, yy), (x + 450 + r.uniform(170, 230), yy)], round(tfirst + .12 * k, 2), "#6a4a30", 2, draw=False))
        els.append(ln([(x + 810, yy), (x + 870, yy)], round(tlines + .1 * k, 2), "#6a4a30", 2, draw=False))
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s14b_add():
    """Back to the whole sheet and the 120 scrolls: their subject bands light up in turn, author by author."""
    t = T("s14b", "author by author")
    return [rect(140, 186 + 36 * r, 410, 30, "rgba(232,195,90,.18)", AU, 2, 15, round(t - .4 + .12 * r, 2)) for r in range(10)] + [gl(347, 380, 320, t - .4, .3)]


def s14_add():
    """One row of the Tables lights up: a little book about dinner parties, its first words and its length, 375 lines."""
    tl, t375 = T("s14", "dinner parties"), T("s14", "three hundred")
    x, y, w, h = TAB
    yy = y + 112 + 50 * 3
    out = [rect(x + 12, yy - 26, w - 24, 46, "rgba(232,195,90,.22)", AU, 2, 6, tl)]
    out += [circ(x + 140, yy - 2, 14, "#f0ece0", "#8a6a44", 1.5, tl + .2, "pop"), circ(x + 140, yy - 2, 7, "none", "#8a6a44", 1.2, tl + .2),
            rect(x + 168, yy - 14, 12, 18, "#c9905a", "#8a6a44", 1, 2, tl + .3, fx="pop")]
    out += [rect(x + 440, yy - 22, 362, 38, PAPY, at=tl + .1), lab(x + 446, yy + 7, "Since you have often written to me", tl + .4, "#5a3a20", 24, "start", st="ital", halo=False),
            rect(x + 800, yy - 22, 100, 38, PAPY, at=t375 - .1), lab(x + 845, yy + 9, "375", t375, "#9a5a10", 30, st="serif", halo=False, fx="pop")]
    return out



# ================================================================== chapter 2: Caesar's fire
Z15 = dict(k=2.0, c=(1000, 360), o=(889, 520))


def F15(pts):
    return tf7(pts, **Z15)


def s15():
    """The harbour and the palace quarter, close: Caesar besieged in the palace quarter (a red ring), the enemy pressing in from the
    city, enemy galleys in the harbour; the galleys burn and the docks catch."""
    tt, tw, tf, tb = T("s15", "is trapped"), T("s15", "caught in a war"), T("s15", "enemy fleet"), T("s15", "burns the ships")
    els = city(-1, palace_fill="rgba(242,201,142,.22)", **Z15)
    (lx, ly), = F15([(792, 206)])
    els += lighthouse(lx, ly + 8, -1, s=.25) + [gl(lx, ly - 86, 90, -1, .6, "fire"), lab(lx - 40, ly - 30, "Pharos", .5, MUTED, 26, "end")]
    (px, py), = F15([(1120, 360)])
    els += [lab(px, py - 40, "palace quarter", .5, GOLD, 30), lab(700, 300, "Great Harbour", .6, BLUE, 30, st="ital")]
    ring = [(px + 250 * math.cos(math.radians(a)), py + 30 + 210 * math.sin(math.radians(a))) for a in range(0, 361, 10)]
    els += [ln(ring, tt, RED, 4, "inferred", dur=1.2, curve=True), lab(px + 270, py - 210, "Caesar, 48 BCE", tt + .5, RED, 32)]
    els += [arrow([[520, 760], [640, 720], [780, 690]], tw, "#d07a5a", 5, dur=.8), arrow([[700, 790], [800, 760], [880, 740]], tw + .3, "#d07a5a", 5, dur=.8)]
    ships = [(560, 560, 1), (660, 500, -1), (760, 440, 1), (600, 420, -1), (840, 380, 1)]
    for k, (x, y, f) in enumerate(ships):
        els += galley(x, y, 92, round(tf + .15 * k, 2), f, c="#3e2c20", sail="#a08c70", fx="pop")
    for k, (x, y, f) in enumerate(ships):
        els += fire(x, y - 10, 46, round(tb + .25 * k, 2), seed=40 + k, n=2, glow_r=120)
    dock = F15([(820, 446), (866, 452), (923, 424), (980, 384)])
    els += [gl(x, y - 10, 140, round(tb + 1.2 + .2 * j, 2), .7, "fire") for j, (x, y) in enumerate(dock)]
    els += [{"k": "scale", "x": 130, "y": 300, "w": 240, "t": "1 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


def X16(yrs):
    return round(300 + yrs * 5.0, 1)


def pawn(x, y, s, at, c="#e8d6b8"):
    """A tiny person as one shape (head and shoulders), s = head radius, y = bottom."""
    pts = [(x + s * math.cos(math.radians(a)), y - 2.1 * s + s * math.sin(math.radians(a))) for a in range(120, 421, 30)]
    pts += [(x + 1.15 * s, y - .9 * s), (x + 1.3 * s, y), (x - 1.3 * s, y), (x - 1.15 * s, y - .9 * s)]
    return poly(pts, c, at=at, fx="pop")


def claim_bar(x, base, h, wd, at, c=LILAC, op=.16):
    return [rect(x - wd / 2, base - h, wd, h, "rgba(201,193,238,%.2f)" % op, c, 2.4, 4, at, fx="fill", style="claimed", dur=.7)]


def s16():
    """A witness timeline in years after the fire: at year 0 Caesar's own account (a head with a laurel wreath): ships burned, and a
    book in a red ring: no books."""
    tc, tn = T("s16", "Caesar himself"), T("s16", "Not a word")
    els = [axis(240, 1580, 690, [[X16(100), "100"], [X16(200), "200"]], .2, t="years after the fire")]
    els += [ln([(X16(0), 682), (X16(0), 698)], .2, BONE, 2, draw=False)]
    els = shift(els, -30)
    els += wreath_head(300, 380, 44, tc, leaf="#a8c070") + [lab(300, 290, "Caesar", tc + .2, BONE, 30)]
    els += galley(300, 612, 120, tc + .5, 1, c="#3e2c20", sail="#a08c70") + fire(300, 600, 40, tc + .7, seed=60, n=2, glow_r=90)
    els += book(420, 526, 50, 64, tn, "#7a4a2a") + [ring(445, 558, 52, tn + .2, RED, 3, "inferred", .6), strike(405, 598, 485, 518, tn + .5, RED, 5)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s17_add():
    """The later witnesses, as claims (dotted): 40,000 books (Seneca after Livy, about a century on); the great library (Plutarch);
    700,000 (Aulus Gellius, two centuries on). Bar heights true to the numbers."""
    t1, t2, t3 = T("s17", "forty thousand"), T("s17", "the great library"), T("s17", "seven hundred thousand")
    k = 450 / 700000
    out = claim_bar(X16(97), 660, 40000 * k, 90, t1) + [lab(X16(97), 610, "40,000", t1 + .3, LILAC, 30)]
    out += temple_icon(X16(155), 650, 40, t2, LILAC, op=.9) + [lab(X16(155), 530, "the great library", t2 + .3, LILAC, 30)]
    out += claim_bar(X16(225), 660, 700000 * k, 90, t3) + [lab(X16(225), 190, "700,000", t3 + .5, LILAC, 34)]
    return out


def s18_add():
    """The later the writer, the bigger the fire: a dashed gold arrow climbs over the bars; dotted flames grow on each."""
    t = T("s18", "The later the writer")
    out = [arrow([[X16(97) + 60, 570], [X16(160), 440], [X16(225) - 70, 240]], t, GOLD, 4, "inferred", dur=1.0)]
    out += flame(X16(97), 632, 34, t + .3, style="claimed", seed=70) + flame(X16(155), 580, 70, t + .6, style="claimed", seed=71) + \
           flame(X16(225), 208, 110, t + .9, style="claimed", seed=72)
    return out


def sack(x, y, s, at, c="#c9a878"):
    return [poly(E(x, y, s, s * .7, 16), c, "#8a6a48", 1.2, at, "pop", curve=True), ln([(x - s * .3, y - s * .62), (x + s * .3, y - s * .62)], at, "#8a6a48", 2, draw=False)]


def s19():
    """A cutaway of the quay at night: two warehouses, grain sacks in one, crates of scrolls in the other, both burning; Cassius Dio's
    quill; a dashed question to the library hall inland."""
    td, tdk, tgr, tbk, tst, tsh = (T("s19", p) for p in ("Cassius Dio", "the docks", "warehouses of grain", "of books", "stored by the harbour", "own shelves"))
    els = [rect(-10, -10, 1800, 640, "url(#k-sky-night)", at=-1), {"k": "stars", "n": 70, "x0": 0, "x1": 1778, "y0": 0, "y1": 400, "seed": 9, "in": -1},
           rect(-10, 640, 1800, 400, "url(#k-sea)", at=-1), rect(-10, 640, 1800, 110, "#2a4a5e", at=-1, op=.35), {"k": "water", "y": 640, "h": 6, "op": .6, "in": -1},
           rect(-10, 600, 1300, 40, "#6b5a44", "#a08a6a", 1.2, 2, -1)]
    els.append(poly([(1180, 640), (1260, 560), (1400, 530), (1800, 520), (1800, 640)], "#1c1712", at=-1))
    els += hall_front(1260, 1720, 520, -1, n=8)
    for j, (x0, kind) in enumerate(((240, "grain"), (640, "books"))):
        els += [rect(x0, 380, 340, 220, "#2a1f17", "#7a6450", 2, 2, -1), poly([(x0 - 14, 380), (x0 + 354, 380), (x0 + 170, 316)], "#4a3a30", "#7a6450", 2, -1)]
        if kind == "grain":
            for r_ in range(3):
                for c_ in range(5 - r_):
                    els += sack(x0 + 60 + c_ * 56 + r_ * 28, 570 - r_ * 46, 26, round(tgr + .05 * (r_ * 5 + c_), 2))
        else:
            for r_ in range(3):
                for c_ in range(4):
                    bx, by = x0 + 30 + c_ * 74, 540 - r_ * 62
                    t = round(tbk + .05 * (r_ * 4 + c_), 2)
                    els += [rect(bx, by, 64, 52, "#6b4a30", "#a07a50", 1.2, 2, t, fx="pop")] + scroll_end(bx + 18, by + 26, 9, t + .1) + scroll_end(bx + 44, by + 26, 9, t + .1)
        els += [lab(x0 + 170, 680, kind, (tgr if kind == "grain" else tbk) + .4, BONE, 30)]
    els += fire(410, 382, 90, tdk, seed=80, n=3, glow_r=260) + fire(810, 382, 100, tdk + .4, seed=83, n=3, glow_r=260)
    els += fire(410, 600, 70, tdk + .8, seed=86, n=3, glow_r=160) + fire(810, 600, 80, tdk + 1.0, seed=89, n=3, glow_r=160)
    els += [ln([(x, 660), (x, 900)], tdk + .6, FIRE, 60, draw=False, op=.14) for x in (410, 810)] + [gl(x, 720, 150, tdk + .6, .3, "fire") for x in (410, 810)]
    els += quill(120, 230, 80, td, GOLD, "known") + [lab(210, 210, "Cassius Dio, about 230 CE", td + .3, GOLD, 28, "start")]
    els += tag(610, 270, "stored for shelving or shipping?", tst, AMBER, 26, "inferred")
    els += [arrow([[990, 420], [1150, 360], [1330, 380]], tsh, LILAC, 3, "claimed", 1.0)] + qmark(1180, 330, tsh + .4, 70, LILAC, halo=False) + \
           [lab(1490, 600, "or the library's shelves?", tsh + .6, LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s20():
    """The ancient claims for the whole library, as dotted bars true to the numbers; then a scroll is not a book: one long history in
    40 scrolls, and spare copies."""
    tf, th, tc = T("s20", "Ancient figures"), T("s20", "one long history"), T("s20", "spare copies")
    k = 450 / 700000
    els = [ln([(150, 650), (830, 650)], .2, BONE, 2, draw=False)]
    for j, (x, n, t) in enumerate(((230, 54800, "54,800"), (400, 200000, "200,000"), (570, 490000, "490,000"), (740, 700000, "700,000"))):
        a = round(tf + .45 * j, 2)
        els += claim_bar(x, 650, n * k, 120, a) + [lab(x, 650 - n * k - 22, t, a + .3, LILAC, 30)]
    els += [lab(490, 712, "ancient claims", tf + .3, MUTED, 26)]
    for r_ in range(4):
        for c_ in range(10):
            els += scroll_side(960 + c_ * 62, 270 + r_ * 32, 52, 14, round(th + .3 + .015 * (r_ * 10 + c_), 2))
    els += bracket(950, 1580, 236, th, None, GOLD, up=False) + [lab(1265, 214, "one history, 40 scrolls", th + .3, GOLD, 30)]
    els += scroll_side(1010, 520, 170, 34, tc) + scroll_side(1290, 520, 170, 34, tc + .3) + [lab(1235, 532, "=", tc + .5, BONE, 44, st="serif"),
                                                                                            lab(1265, 610, "spare copies", tc + .6, BONE, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s21():
    """Bagnall's count: 625 known Greek writers to about 200 BCE, fifty scrolls each: about 31,000, a solid bar beside the dotted
    700,000 (heights true: 1 to 22)."""
    tc, tf, t31, tl = T("s21", "counted every Greek"), T("s21", "fifty scrolls"), T("s21", "thirty one thousand"), T("s21", "far smaller")
    els = []
    for row in range(25):
        for col in range(25):
            els.append(pawn(160 + col * 20, 226 + row * 20, 5.6, round(tc + .03 * row, 2)))
    els += [lab(400, 740, "625 known writers", tc + .9, BONE, 30), lab(400, 180, "Bagnall 2002", tc + .2, MUTED, 24)]
    els += [arrow([[650, 430], [850, 470], [1000, 610]], tf, GOLD, 4, dur=.7), lab(840, 430, "50 scrolls each", tf + .2, GOLD, 28)]
    k = 470 / 700000
    els += [rect(975, 660 - 31250 * k, 130, 31250 * k, "rgba(232,195,90,.55)", GOLD, 2.5, 3, t31, fx="fill", style="inferred", dur=.6),
            lab(1040, 620, "about 31,000", t31 + .3, GOLD, 34)]
    els += claim_bar(1300, 660, 700000 * k, 130, t31 + .8) + [lab(1300, 172, "700,000", t31 + 1.0, LILAC, 32)]
    els += [ln([(960, 660), (1400, 660)], .2, BONE, 2, draw=False), gl(1040, 640, 160, tl, .55)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s22():
    """The Museum again, with Strabo at its gate; the walk, the hall and the dining hall glow as named; two coins: Julius Caesar
    (dimmed), then Augustus, the Caesar of Strabo's day."""
    ts, tw, th, td, tc, tdc = (T("s22", p) for p in ("the geographer", "covered walk", "great hall", "dining together", "appointed by Caesar", "A different Caesar"))
    els = mouseion(.1, light=.18)
    sx, sy = MP(-26, 0, 20)
    els += [figure(sx, sy, 70, ts, "#f0e0c4"), rect(sx + 10, sy - 50, 18, 24, PAPY, "#8a6a44", 1, 2, ts + .2, fx="pop"), lab(sx - 20, sy + 40, "Strabo, about 25 BCE", ts + .3, BONE, 28)]
    els += [gl(*MP(x, 3, z), 70, round(tw + .08 * j, 2), .55) for j, (x, z) in enumerate([(-16, 12.5), (-8, 12.5), (0, 12.5), (8, 12.5), (16, 12.5), (-18.5, 0), (18.5, 0)])]
    els += [gl(*MP(0, 3, -22), 110, th, .7), gl(*MP(24.5, 3, 0), 120, td, .7)]
    els += coin(1240, 180, 36, tc, "#b89a5a", "#e0c890") + [lab(1240, 252, "Julius Caesar", tc + .2, MUTED, 26)]
    els += [arrow([[1290, 180], [1330, 170], [1380, 180]], tdc, GOLD, 3, dur=.4)] + coin(1440, 180, 40, tdc + .2) + [lab(1440, 252, "Augustus", tdc + .4, GOLD, 28), gl(1440, 180, 110, tdc + .3, .5)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


V23 = View(8, 34, 29.5, 45, rect=(90, 130, 1600, 660))


def s23():
    """Map Rome to Alexandria: Claudius' new wing beside the Museum; Rome's burned libraries; scribes sail from Rome to Alexandria and
    back with copies; the library still at work."""
    v = V23
    tcl, tro, tsc, tcp, tend = (T("s23", p) for p in ("Claudius", "Rome's own libraries", "sent scribes", "to copy its books", "It didn't end"))
    rx, ry = v.p(12.5, 41.9)
    ax, ay = v.p(29.92, 31.2)
    route = [(rx + 10, ry + 16), v.p(14.3, 40.3), v.p(15.7, 38.0), v.p(19.5, 35.4), v.p(25.0, 33.4), (ax - 12, ay - 12)]
    back = [(ax - 30, ay + 6), v.p(24.0, 32.6), v.p(18.0, 34.6), v.p(15.0, 37.6), v.p(13.4, 40.0), (rx - 4, ry + 24)]
    els = [{"k": "map", "land": v.land(), "in": -1},
           {"k": "pin", "x": ax, "y": ay, "t": "Alexandria", "c": GOLD, "in": .3, "lx": 22, "ly": 34},
           {"k": "pin", "x": rx, "y": ry, "t": "Rome", "c": GOLD, "in": .5, "lx": 20, "ly": -16}]
    els += temple_icon(ax + 70, ay - 30, 30, .4) + [rect(ax + 110, ay - 66, 46, 36, STONE, STONE_D, 1, 2, tcl, fx="pop"), gl(ax + 133, ay - 50, 90, tcl, .6),
                                                     lab(ax + 160, ay - 90, "a new wing, Claudius", tcl + .3, GOLD, 28, "start")]
    els += temple_icon(rx - 70, ry - 20, 28, tro) + smoke(rx - 70, ry - 70, 26, tro + .3, seed=5, n=3, c="#8a7a78", op=.5) + \
           [lab(rx - 70, ry - 136, "Rome's libraries burned", tro + .4, MUTED, 26)]
    els += [ln(route, tsc, BONE, 3, "inferred", dur=1.6, curve=True)] + [figure(*v.p(lo, la), 26, round(tsc + .4 + .3 * j, 2), "#f0e0c4") for j, (lo, la) in enumerate(((16.6, 37.0), (20.5, 35.2), (24.4, 33.8)))]
    els += [lab(*v.p(19.0, 34.0), "scribes", tsc + 1.2, BONE, 26)]
    els += [ln(back, tcp + .6, PAPY_D, 3, "inferred", dur=1.6, curve=True)] + scroll_side(ax - 120, ay + 40, 70, 16, tcp) + scroll_side(ax - 110, ay + 62, 70, 16, tcp + .2)
    els += [gl(ax + 70, ay - 40, 200, tend, .6)] + tag(ax + 80, ay + 100, "still at work", tend + .2, GREEN, 30)
    return {"base": "map", "cam": CAM, "els": els}



# ================================================================== chapter 3: the slow fires
def spearman(x, y, h, at, c="#9a8a7a", face=1):
    return [figure(x, y, h, at, c), ln([(x + face * h * .18, y - h * .05), (x + face * h * .22, y - h * 1.25)], at, "#c9b89a", 2.5, draw=False),
            poly([(x + face * h * .22 - 5, y - h * 1.22), (x + face * h * .22 + 5, y - h * 1.22), (x + face * h * .22, y - h * 1.36)], "#d8d0c0", at=at, fx="pop")]


def s24():
    """The Museum in a red dusk: soldiers with spears in front of it, a crowned king at the gate (Ptolemy VIII, 145 BCE), scholars
    leaving to the left."""
    tk, tt = T("s24", "a new king"), T("s24", "turned on")
    els = [gl(930, 480, 1000, -1, .5, "red")] + mouseion(-1, light=None) + [rect(-10, -10, 1800, 1020, "rgba(120,30,20,.18)", at=-1)]
    kx, ky = MP(-27, 0, 17)
    els += [figure(kx, ky, 118, tk, "#e8cc90"), crown(kx, ky - 118 * .99 + 8, 18, tk + .2), gl(kx, ky - 60, 120, tk, .5), lab(kx - 10, ky + 46, "Ptolemy VIII, 145 BCE", tk + .4, GOLD, 32)]
    for j in range(6):
        sx, sy = MP(-14 + 6 * j, 0, 24)
        els += spearman(sx, sy, 70, round(tt + .15 * j, 2), "#b0a090")
    for j in range(5):
        x0, y0 = MP(-16 + 4 * j, 0, -8)
        els.append(figure(x0, y0, 40, -1, "#f0e0c4"))
    els += [arrow([[520, 470], [400, 450], [280, 460]], tt + .8, BONE, 3, "inferred", .8)]
    els += [figure(250 - 50 * j, 500 + 8 * j, 64, round(tt + 1.0 + .2 * j, 2), "#f0e0c4") for j in range(3)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def icon_compass(x, y, s, at, c=BONE):
    return [ln([(x, y - s), (x - s * .6, y + s * .8)], at, c, 3, draw=False), ln([(x, y - s), (x + s * .6, y + s * .8)], at, c, 3, draw=False), circ(x, y - s, 4, c, at=at, fx="pop")]


def icon_staff(x, y, s, at, c=BONE):
    return [ln([(x, y - s), (x, y + s)], at, c, 3, draw=False), ln([(x - 6, y + s * .7), (x + 7, y + s * .4), (x - 7, y + s * .05), (x + 7, y - s * .3), (x - 4, y - s * .6)], at, GREEN, 2.5, curve=True, draw=False)]


def icon_brush(x, y, s, at, c=BONE):
    return [ln([(x - s * .6, y + s * .8), (x + s * .4, y - s * .4)], at, c, 3, draw=False), poly([(x + s * .3, y - s * .5), (x + s * .7, y - s * .9), (x + s * .5, y - s * .3)], AMBER, at=at, fx="pop")]


def s25():
    """Map of the eastern Mediterranean: Aristarchus sails to Cyprus; scholars fan out to Rhodes, Athens, Pergamon and Antioch with
    their crafts (scroll, compass, healer's staff, brush); then soft lights glow across the whole map."""
    v = V6
    ta, tg, tx, ti = T("s25", "Aristarchus"), T("s25", "Grammarians"), T("s25", "driven out"), T("s25", "teachers")
    ax, ay = v.p(29.92, 31.2)
    els = [{"k": "map", "land": v.land(), "in": -1}, {"k": "pin", "x": ax, "y": ay, "t": "Alexandria", "c": GOLD, "in": .3, "lx": -20, "ly": 34, "a": "end"},
           lab(ax - 20, ay + 64, "145 BCE", .5, GOLD, 26, "end")]
    cy = v.p(32.9, 34.9)
    els += [arrow([(ax + 10, ay - 10), v.p(31.6, 33.2), (cy[0] - 10, cy[1] + 14)], ta, GOLD, 3, "inferred", 1.0)]
    els += merchantman(cy[0] - 60, cy[1] + 50, 60, ta + .6, sail=PAPY) + [lab(cy[0] + 10, cy[1] + 110, "Aristarchus, to Cyprus", ta + .8, GOLD, 28, "start")]
    # where some of Aristarchus' pupils went (Pfeiffer 1968): Dionysius Thrax to Rhodes, Apollodorus to Pergamon and later Athens;
    # the crafts named in the ancient list ride the arrows (their own destinations are not recorded)
    dests = [(28.2, 36.4), (27.2, 39.1), (23.73, 37.98)]
    crafts = [icon_compass, icon_staff, icon_brush]
    for j, (lo, la) in enumerate(dests):
        x, y = v.p(lo, la)
        t = round(tg + .45 * j, 2)
        mx, my = (ax + x) / 2 + 20, (ay + y) / 2
        els += [arrow([(ax, ay - 14), (mx, my), (x, y + 12)], t, BONE, 2.5, "inferred", .9), dot(round(x, 1), round(y, 1), 8, GOLD, t + .8),
                circ(mx, my, 32, "rgba(18,13,10,.85)", GOLD, 2, t + .5, "pop")] + crafts[j](mx, my, 18, t + .6)
    for j, (lo, la) in enumerate(((14.3, 40.8), (12.5, 41.9), (15.2, 37.1), (19.8, 41.3), (22.9, 40.6), (26.5, 39.6), (33.5, 37.0), (35.5, 33.9), (25.1, 35.3), (20.1, 32.1), (31.0, 39.8))):
        x, y = v.p(lo, la)
        els.append(gl(x, y, 70, round(ti + .12 * j, 2), .55))
    els += [lab(*v.p(19.0, 33.4), "teachers of Greeks and foreigners", ti + .9, GOLD, 30, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def aged_sheet(x, y, w, h, at, stage, seed=1):
    """A sheet of papyrus at an age: 0 fresh, 1 yellowed, 2 brown and frayed, 3 holed and flaking."""
    cols = ["#f1e2c0", "#e2c690", "#b8915c", "#8a6a44"]
    r = random.Random(seed)
    jag = 2 + 7 * stage
    top = [(x + w * k / 10, y + r.uniform(-1, 1) * jag) for k in range(11)]
    right = [(x + w + r.uniform(-1, 1) * jag, y + h * k / 10) for k in range(1, 11)]
    bot = [(x + w * k / 10, y + h + r.uniform(-1, 1) * jag) for k in range(9, -1, -1)]
    left = [(x + r.uniform(-1, 1) * jag, y + h * k / 10) for k in range(9, 0, -1)]
    out = [poly(top + right + bot + left, cols[stage], "#5a4330", 1.2, at, "pop")]
    for k in range(6):
        yy = y + 30 + k * (h - 50) / 5
        out.append(ln([(x + 22, yy), (x + w - 26 - r.uniform(0, 50), yy)], at + .1, "#6a4a30", 2, draw=False, op=max(.15, .75 - .18 * stage)))
    for k in range(stage * 3):
        out.append(poly(E(x + r.uniform(.2, .8) * w, y + r.uniform(.2, .85) * h, r.uniform(6, 16), r.uniform(5, 12), 10), "#1a120c", at=at + .2, curve=True))
    if stage == 3:
        out += [circ(x + r.uniform(0, w), y + h + r.uniform(8, 40), r.uniform(2, 5), "#8a6a44", at=at + .3, fx="pop") for _ in range(10)]
    return out


def s26():
    """One sheet of papyrus at 0, 100, 200 and 300 years: fresh, yellowed, frayed, crumbling; damp sea air drifts in; then the
    city's own soil, with no ancient papyri in it."""
    tt, tl, td, tn = T("s26", "Papyrus is tough"), T("s26", "might last a century"), T("s26", "is damp"), T("s26", "Not one ancient")
    xs = [300, 680, 1060, 1440]
    els = [axis(220, 1560, 600, [[x, str(100 * j)] for j, x in enumerate(xs)], tt, t="years")]
    for j, x in enumerate(xs):
        els += aged_sheet(x - 120, 300, 240, 250, round((tt if j == 0 else tl) + .6 * j, 2), j, seed=3 + j)
    els += [lab(140, 250, "sea air", td, BLUE, 28, st="ital")]
    r = random.Random(2)
    els += [circ(r.uniform(120, 1600), r.uniform(220, 560), r.uniform(3, 6), BLUE, at=round(td + .03 * k, 2), fx="pop", op=.55) for k in range(40)]
    els += [rect(160, 680, 1460, 110, "#4a3a2a", "#8a6a48", 1.5, 6, tn), {"k": "rect", "x": 160, "y": 680, "w": 1460, "h": 110, "fill": "url(#k-speck)", "c": "none", "sw": 0, "in": round(tn, 2)},
            lab(889, 744, "ancient papyri found in Alexandria's soil: none", tn + .4, RED, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def phone(x, y, w, h, at, tiles=True, c="#2a2622"):
    out = [rect(x, y, w, h, c, "#c9c1b3", 2, 14, at, fx="pop"), rect(x + 8, y + 18, w - 16, h - 36, "#10201a", at=at)]
    if tiles:
        for k in range(9):
            r_, c_ = divmod(k, 3)
            out.append(rect(x + 14 + c_ * (w - 28) / 3, y + 26 + r_ * (h - 56) / 3, (w - 28) / 3 - 6, (h - 56) / 3 - 6, ["#c98f5a", "#8fb0c9", "#a6b87a"][k % 3], at=at + .1, fx="pop"))
    return out


def s27():
    """Two chains of copies: one copied in time, each fresh copy made before the old one crumbles (it lives); one where the copying
    stops and the last copy turns to dust (gone); below, an old phone passing its photos to a new one, and an empty shelf."""
    tc, tp, ts = T("s27", "copied it before"), T("s27", "like photos"), T("s27", "When the copying stops")
    els = [lab(170, 200, "copied", tc, GREEN, 30, "start"), lab(170, 420, "not copied", ts, RED, 30, "start")]
    for j in range(5):
        x = 200 + 300 * j
        t = round(tc + .5 * j, 2)
        els += aged_sheet(x, 230, 150, 110, t, max(0, min(3, 3 - j)) if j < 4 else 0, seed=20 + j)
        if j < 4:
            els += [arrow([[x + 160, 285], [x + 220, 280], [x + 285, 285]], t + .3, BONE, 2.5, dur=.4), ln([(x + 212, 262), (x + 230, 246)], t + .3, AMBER, 3, draw=False)]
    els += [tick(1690, 285, tc + 2.6, GREEN, 1.2)]
    for j in range(3):
        x = 200 + 300 * j
        t = round(ts - .2 + .5 * j, 2)
        if j < 2:
            els += aged_sheet(x, 450, 150, 110, t, 1 + j, seed=40 + j)
        else:
            els += [rect(x, 450, 150, 110, "none", "#8a6a44", 2, 4, t, style="claimed")] + [circ(x + 20 + 12 * k, 560 + (k % 3) * 6, 3, "#8a6a44", at=t + .2, fx="pop") for k in range(10)]
    els += [arrow([[360, 505], [420, 500], [485, 505]], ts + .3, BONE, 2.5, dur=.4)] + cross(710, 505, ts + .8)
    els += [arrow([[860, 505], [1050, 500], [1280, 505]], ts + 1.0, MUTED, 2.5, "inferred", .6), rect(1300, 440, 180, 130, "#24180f", WOOD, 6, 4, ts + 1.2),
            lab(1390, 610, "an empty shelf", ts + 1.4, RED, 28)]
    els += phone(860, 600, 84, 150, tp) + [arrow([[960, 675], [1010, 670], [1060, 675]], tp + .4, BONE, 3, dur=.4)] + phone(1075, 600, 84, 150, tp + .8)
    els += [lab(902, 780, "old phone", tp + .3, MUTED, 24), lab(1117, 780, "new phone", tp + 1.0, MUTED, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s28():
    """The palace quarter, close, in the 270s CE: fighting crosses the city; most of the quarter turns to ruin and fire; the wall
    breaks."""
    tw, tr = T("s28", "war and revolt"), T("s28", "largely destroyed")
    els = city(-1, palace_fill="rgba(242,201,142,.22)", **Z15)
    (px, py), = F15([(1120, 360)])
    els += [lab(px, py - 40, "palace quarter", .4, GOLD, 30), lab(px - 330, py - 300, "270s CE", tw, RED, 34)]
    for j, (a, b) in enumerate((((300, 760), (700, 640)), ((520, 800), (860, 700)), ((1500, 760), (1250, 640)), ((1600, 560), (1380, 520)), ((900, 820), (1000, 660)))):
        els.append(arrow([list(a), [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 30], list(b)], round(tw + .2 * j, 2), "#e07a5a", 5, dur=.7))
    ruin = F15([(960, 470), (990, 382), (1040, 340), (1080, 300), (1096, 252), (1124, 262), (1186, 300), (1250, 322), (1258, 470), (1100, 498)])
    els += [poly(ruin, "rgba(30,20,14,.82)", "#5a3a2a", 2, tr, fx="pop"), lab(px, py - 40, "palace quarter", tr + .2, GOLD, 30)]
    r = random.Random(3)
    for k in range(26):
        x, y = r.uniform(820, 1380), r.uniform(320, 760)
        els.append(rect(x, y, r.uniform(10, 22), r.uniform(8, 16), "#6a5040", at=round(tr + .2 + .02 * k, 2), fx="pop", op=.9))
    els += fire(1010, 560, 70, tr + .3, seed=90, n=3, glow_r=200) + fire(1250, 470, 60, tr + .5, seed=93, n=2, glow_r=180) + fire(1150, 700, 60, tr + .6, seed=96, n=2, glow_r=180)
    return {"base": "map", "cam": CAM, "els": els}


def s29():
    """The master timeline again: the palace library as a gold band from about 285 BCE that fades out at the 270s CE; a Roman
    historian's quill at about 390; a question mark where the band ends."""
    tr, tn, tm = T("s29", "A Roman historian"), T("s29", "no writer describes"), T("s29", "Nobody wrote down")
    ay = 540
    els = [axis(110, 1670, ay, [[XM(0), "1 CE"], [XM(1200), "1200"]], .2)]
    x0, x1 = XM(-285), XM(272)
    n = 16
    for k in range(n):
        a, b = x0 + (x1 - x0) * k / n, x0 + (x1 - x0) * (k + 1) / n
        els.append(rect(a, ay - 96, b - a + 1, 40, GOLD, at=round(.4 + .05 * k, 2), op=round(max(.06, .95 - .055 * k * (1 if k < 11 else 1.5)), 2)))
    els += [lab((x0 + x1) / 2 - 60, ay - 122, "the palace library", .6, GOLD, 32), lab(x1, ay + 48, "270s", .8, RED, 30)]
    els += quill(XM(390), ay - 16, 70, tr, BONE, "known") + [lab(XM(390) + 20, ay + 48, "a Roman historian, about 390", tr + .3, BONE, 28, "start"),
                                                             arrow([[XM(390) - 6, ay - 100], [XM(340), ay - 170], [x1 + 24, ay - 110]], tr + .6, BONE, 2.5, "inferred", .7)]
    els += qmark(x1 + 40, ay - 200, tn, 80, LILAC, halo=True) + [lab(x1 + 40, ay - 300, "no record of its end", tm, LILAC, 30)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}



# ================================================================== chapter 4: a temple and a legend
def hill(at=-1):
    return [poly([(80, 800), (300, 700), (520, 560), (560, 545), (1240, 545), (1290, 560), (1500, 700), (1720, 800), (1720, 1020), (80, 1020)], "#4a3a2c", "#8a6a48", 1.5, at, curve=False),
            poly([(80, 800), (300, 700), (520, 560), (560, 545), (1240, 545), (1290, 560), (1500, 700), (1720, 800), (1720, 1020), (80, 1020)], "url(#k-speck)", at=at)]


SER_COLS = [560 + 44 * j for j in range(16)]


def stoa(at=-1, base=545, h=104, fx=None):
    els = [rect(536, base - h - 22, 708, 22, "#cdb994", "#6b5a44", 1, 2, at, fx=fx), rect(536, base - 6, 708, 8, "#b8a586", at=at)]
    for x in SER_COLS:
        els += column(x, base, h, 14, at, "#cdb994", fx=fx, ionic=False, flutes=False)
    return els


def serapeum(at=-1, ruined=False):
    els = [rect(-10, -10, 1800, 1020, "url(#k-sky-dusk)", at=at)] + hill(at)
    els += [poly([(800, 800), (980, 800), (950, 548), (830, 548)], "#6b5a44", "#a08a6a", 1, at)] + [ln([(800 + 6 * k, 800 - 26 * k), (980 - 6 * k, 800 - 26 * k)], at, "#8a7458", 1.2, draw=False) for k in range(9)]
    if not ruined:
        els += stoa(at)
        els += [rect(730, 400, 320, 40, "#bda884", "#6b5a44", 1, 2, at), rect(746, 386, 288, 16, "#cdb994", at=at)]
        for j in range(6):
            els += column(760 + 52 * j, 386, 150, 22, at, "#d8c4a0", fx=None)
        els += [rect(740, 222, 300, 18, "#d8c4a0", "#6b5a44", 1, 2, at), poly([(732, 224), (1048, 224), (890, 168)], "#d8c4a0", "#6b5a44", 1.2, at),
                poly([(752, 220), (1028, 220), (890, 178)], "#bda884", at=at)]
    return els


def s30():
    """The Serapeum on its hill: a temple on a high podium inside a colonnaded court, a broad stair; in a cutaway under the hill, the
    foundation plaques of Ptolemy III pop, gold, silver, bronze, faience, glass and mud brick, inscribed in Greek and in hieroglyphs."""
    ts, tp = T("s30", "the Serapeum"), T("s30", "foundation plaques")
    els = serapeum(-1) + [gl(890, 330, 600, -1, .25)]
    els += [lab(889, 140, "Serapeum", ts, GOLD, 50, st="serif", fx="pop")]
    els += [rect(1384, 606, 300, 150, "#1a120c", "#8a6a48", 2, 4, tp - .4), lab(1534, 556, "foundation plaques", tp + .9, GOLD, 28),
            lab(1534, 590, "of Ptolemy III", tp + 1.0, GOLD, 28), ln([(1384, 640), (1180, 560)], tp - .4, "#8a6a48", 1.5, "inferred", dur=.5)]
    cols = ["#e8c35a", "#c9ccd2", "#c08a50", "#5fa89a", "#3e6a5a", "#8a6a48"]
    for j, c in enumerate(cols):
        x, y = 1398 + (j % 3) * 92, 620 + (j // 3) * 66
        t = round(tp + .15 * j, 2)
        els += [rect(x, y, 78, 52, c, "#fff6e6", 1, 3, t, fx="pop")]
        if j % 2 == 0:
            els += [ln([(x + 10, y + 16 + 10 * q), (x + 66, y + 16 + 10 * q)], t + .1, "#2a1c12", 1.5, draw=False, op=.7) for q in range(3)]
        else:
            els += [circ(x + 18 + 16 * q, y + 26, 4, "none", "#2a1c12", 1.5, t + .1, op=.7) for q in range(3)] + [ln([(x + 14, y + 40), (x + 64, y + 40)], t + .1, "#2a1c12", 1.5, draw=False, op=.7)]
    return {"base": "dark", "cam": CAM, "els": els}


def s31_add():
    """The colonnade, close: rooms of books light up behind it, small readers; 'the daughter library'; then the late claim of 42,800
    scrolls, dotted."""
    td, tv, tn = T("s31", "daughter of the first"), T("s31", "rooms of books"), T("s31", "forty two thousand")
    out = [rect(540, 445, 700, 94, "#2a1a10", at=tv)]
    wall, _ = pigeonholes(548, 452, 24, 2, 28.5, 40, tv, fill=1.0, seed=31, step=.012, wood="#5a3a22", back="#1e140c", tags=0)
    out += wall + [gl(620 + 120 * k, 490, 110, tv + .4, .5) for k in range(6)]
    out += stoa(tv + .01)
    out += [figure(600 + 130 * k, 540, 46, round(tv + .6 + .15 * k, 2), "#f0e0c4") for k in range(5)]
    out += [lab(760, 600, "the daughter library", td, GOLD, 32)] + tag(1050, 330, "42,800 scrolls?", tn, LILAC, 28, "claimed")
    return out


def ruins(at=-1):
    r = random.Random(5)
    els = []
    for j, x in enumerate(SER_COLS):
        h = r.uniform(14, 60) if j % 3 else r.uniform(30, 90)
        els += [rect(x - 7, 545 - h, 14, h, "#cdb994", "#6b5a44", 1, 1, at)]
    for k in range(14):
        x, y = r.uniform(560, 1240), r.uniform(560, 700)
        els.append(poly(E(x, y, r.uniform(16, 26), r.uniform(9, 13), 14), "#cdb994", "#6b5a44", 1, at, curve=True))
    els += [rect(730, 420, 320, 20, "#bda884", "#6b5a44", 1, 2, at)] + [rect(760 + 52 * j - 11, 420 - h, 22, h, "#d8c4a0", "#6b5a44", 1, 1, at) for j, h in enumerate((70, 20, 46, 12, 34, 58))]
    return els


def s32():
    """The hill again, the temple a ruin (no people hurt): fallen drums, broken columns, a settling dust cloud. Four account scrolls;
    out of them pop what they describe: the building, the statue, the soldiers; the slot for books stays empty."""
    tt, tw, tb, tst, tso, tn = (T("s32", p) for p in ("torn", "writers alike", "the building", "the great statue", "the soldiers", "Not one of them"))
    els = serapeum(-1, ruined=True) + ruins(-1)
    els += [oval(890 + 60 * (k % 2), 470 - 40 * k, 380 - 50 * k, 80 - 10 * k, "#b0a090", at=round(tt + .25 * k, 2), op=.16) for k in range(5)]
    els += [lab(760, 150, "391 CE", tt, RED, 44, st="serif")]
    x0 = 1250
    els += [rect(x0, 160, 440, 470, "rgba(18,13,10,.82)", "rgba(255,236,206,.25)", 2, 16, tw - .3), lab(x0 + 220, 206, "four accounts of its fall", tw, BONE, 26)]
    for j in range(4):
        els += scroll_side(x0 + 140, 252 + 34 * j, 160, 22, round(tw + .15 * j, 2))
    icons = [("building", tb, lambda x, y, a: [rect(x - 30, y - 8, 60, 16, STONE, STONE_D, 1, 2, a, fx="pop"), rect(x - 8, y - 50, 16, 42, STONE, STONE_D, 1, 1, a, fx="pop")]),
             ("statue", tst, lambda x, y, a: [circ(x, y - 22, 22, "#cdb994", STONE_D, 1.5, a, "pop"), ln([(x - 14, y - 34), (x + 14, y - 34)], a, STONE_D, 2, draw=False)]),
             ("soldiers", tso, lambda x, y, a: [poly([(x - 24, y), (x - 20, y - 30), (x, y - 40), (x + 20, y - 30), (x + 24, y)], "#b0a090", "#6b5a44", 1.5, a, "pop"),
                                                ln([(x, y - 40), (x, y - 56)], a, RED, 4, draw=False)])]
    for j, (nm, t, ic) in enumerate(icons):
        x = x0 + 60 + 106 * j
        els += [rect(x - 46, 430, 92, 110, "rgba(255,236,206,.06)", GREEN, 2, 10, t, fx="pop")] + ic(x, 510, t + .1) + [lab(x, 574, nm, t + .2, BONE, 24), tick(x + 28, 440, t + .3, GREEN, .7, 4)]
    x = x0 + 60 + 106 * 3
    els += [rect(x - 46, 430, 92, 110, "none", LILAC, 2.5, 10, tn, style="claimed"), lab(x, 504, "?", tn + .2, LILAC, 54, st="big"), lab(x, 574, "books", tn + .3, LILAC, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def chest(x, y, w, h, at, c="#6b4a30"):
    """An open wooden book chest, empty: the box, its dark inside, the lid standing open behind."""
    return [poly([(x + 6, y - h * .25), (x + w - 6, y - h * .25), (x + w - 14, y - h * 1.0), (x + 14, y - h * 1.0)], "#5a3e28", "#a07a50", 1.5, at, "pop"),
            rect(x, y - h * .25, w, h, c, "#a07a50", 1.5, 3, at, fx="pop"), rect(x + 8, y - h * .25 + 6, w - 16, h * .32, "#1a120c", at=at + .1, fx="pop"),
            ln([(x, y + h * .35), (x + w, y + h * .35)], at, "#a07a50", 1.5, draw=False)]


def s33():
    """Two kinds of evidence: a historian writing just before 391 who puts the libraries in the past tense; a historian a generation
    later who saw empty book chests in temples, how many and where unsaid."""
    tp, to, th = T("s33", "past tense"), T("s33", "Yet a generation"), T("s33", "How many books")
    els = [rect(886, 160, 6, 600, "rgba(255,236,206,.12)", at=.2)]
    els += sheet(200, 250, 520, 250, tp - .8, rows=4, seed=12) + [rect(240, 330, 440, 54, PAPY, at=tp - .3), lab(460, 368, "there were libraries", tp, "#5a3a20", 34, st="ital", halo=False)]
    els += [arrow([[620, 560], [460, 610], [300, 560]], tp + .5, GOLD, 3.5, dur=.7), lab(460, 660, "about 390, past tense", tp + .7, GOLD, 28)]
    els += [poly([(1030, 760), (1030, 330), (1060, 270), (1310, 210), (1560, 270), (1590, 330), (1590, 760)], "#241a12", "#6b5a44", 2, to - .3)]
    els += chest(1110, 600, 170, 110, to + .2) + chest(1340, 600, 170, 110, to + .5) + [gl(1310, 520, 260, to + .3, .3)]
    els += [lab(1310, 700, "empty book chests, about 417", to + .8, BONE, 28)] + qmark(1310, 400, th, 90, LILAC) + [lab(1310, 300, "how many? where?", th + .3, LILAC, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def robed(x, y, h, at, c="#e8d6b8"):
    """A standing figure in a long robe (x, y = feet)."""
    return [poly([(x - h * .16, y - h * .78), (x + h * .16, y - h * .78), (x + h * .24, y), (x - h * .24, y)], c, at=at, fx="rise"),
            circ(x, y - h * .88, h * .085, c, at=at, fx="rise"), ln([(x + h * .12, y - h * .7), (x + h * .34, y - h * .62)], at, c, max(3, h * .05), draw=False)]


def s34():
    """Lamplight: Hypatia teaching at a board with a cone and its cut curves, students of every height around her; the lamp gently
    dims. Below: 391 and 415 on a short timeline, 24 years apart, and a struck dashed link to the library: no source links them."""
    th, tr, tn = T("s34", "Hypatia"), T("s34", "A real tragedy"), T("s34", "no ancient source")
    els = [rect(-10, -10, 1800, 1020, "#22180f", at=-1), gl(760, 300, 700, -1, .3)]
    els += [rect(560, 150, 420, 260, "#1f2e28", "#8a6a48", 4, 6, -1)]
    els += [ln([(770, 180), (680, 370), (860, 370), (770, 180)], th, "#e8e4dc", 2.5, dur=1.0), ln(E(770, 370, 90, 18, 30), th + .4, "#e8e4dc", 2, dur=.8),
            ln(E(770, 300, 52, 11, 30), th + .7, AMBER, 2.5, dur=.8), ln([(724, 330), (800, 250), (840, 340)], th + 1.0, BLUE, 2.5, curve=True, dur=.8)]
    els += robed(1040, 520, 190, th) + [lab(1040, 286, "Hypatia", th + .3, GOLD, 32)]
    seats = [(470, 520, 120, 1), (330, 520, 140, 1), (1240, 520, 130, -1), (1380, 520, 150, -1), (190, 520, 110, 1), (1520, 520, 120, -1)]
    cols = ["#d8c4a4", "#e6d2b0", "#cdb894", "#efe0c6", "#c9b394", "#e0caa8"]
    for j, (x, y, h, f) in enumerate(seats):
        els += seated(x, y, h, round(th + .2 + .1 * j, 2), cols[j], face=f)
    els += lamp(900, 520, 90, -1, .65)
    els += [rect(-10, -10, 1800, 560, "#0d0b09", at=tr, op=.5, dur=1.6), lab(1040, 286, "Hypatia", tr + 1.0, GOLD, 32)]
    ay = 680
    els += [ln([(240, ay), (1540, ay)], tn - .4, BONE, 2, draw=False)]
    x1, x2 = 520, 860
    els += temple_icon(x1, ay - 10, 26, tn - .3) + [lab(x1, ay + 44, "391", tn - .2, GOLD, 28)]
    els += [circ(x2, ay - 26, 12, FIRE_L, at=tn, fx="pop"), gl(x2, ay - 26, 50, tn, .6), lab(x2, ay + 44, "415", tn + .1, GOLD, 28)]
    els += bracket(x1, x2, ay - 70, tn + .3, "24 years", BONE, up=False, size=26, ty=ay - 84)
    els += [ln([(x2 + 30, ay - 30), (1200, ay - 30)], tn + .8, LILAC, 2.5, "inferred", dur=.6)] + temple_icon(1260, ay - 10, 26, tn + .9, LILAC, op=.9) + cross(1230, ay - 40, tn + 1.3)
    els += [lab(1260, ay + 44, "no source links them", tn + 1.5, LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """Plan of the lecture halls found in the city: about twenty horseshoe-shaped rooms in two rows along a street, benches along their
    walls, a raised seat at the end, a few students for scale."""
    t = T("s35", "some twenty lecture halls")
    els = [rect(160, 455, 1460, 70, "rgba(245,236,220,.08)", "rgba(245,236,220,.3)", 1.5, 4, .2)]
    k = 0
    for row, (y0, f) in enumerate(((440, -1), (540, 1))):
        for j in range(10):
            x = 210 + j * 142
            a = round(t - .3 + .07 * k, 2)
            k += 1
            pts = [(x - 52, y0)] + [(x + 52 * math.cos(math.radians(aa)), y0 + f * (150 - 52 + 52 * math.sin(math.radians(aa)))) for aa in range(180, 361, 15)][::-1 if f < 0 else 1] + [(x + 52, y0)]
            outer = [(x - 56, y0), (x - 56, y0 + f * 100), (x + 56, y0 + f * 100), (x + 56, y0)]
            els += [poly([(x - 56, y0), (x - 56, y0 + f * 110)] + [(x + 56 * math.cos(math.radians(aa)), y0 + f * (110 + 46 * math.sin(math.radians(aa)))) for aa in range(180, -1, -15)] + [(x + 56, y0 + f * 110), (x + 56, y0)],
                         "#5a4a3a", "#e2cfa8", 2, a, "pop")]
            els += [ln([(x - 40, y0 + f * 12), (x - 40, y0 + f * 110)], a + .1, "#c9b394", 4, draw=False), ln([(x + 40, y0 + f * 12), (x + 40, y0 + f * 110)], a + .1, "#c9b394", 4, draw=False),
                    circ(x, y0 + f * 140, 9, GOLD, at=a + .15, fx="pop")]
            if j % 3 == 1:
                els += [circ(x - 30, y0 + f * (40 + 20 * q), 5, BONE, at=a + .3, fx="pop") for q in range(3)]
    els += [lab(889, 230, "about 20 lecture halls", t + .8, GOLD, 34), lab(889, 800 - 30, "in use from the 400s to the 600s CE", t + 1.2, MUTED, 26)]
    return {"base": "plan", "cam": CAM, "els": els}


def s36():
    """The story, all in dotted lilac: a bathhouse furnace fed with scrolls; a field of 4,000 dots for the bathhouses; six months
    ticking off."""
    tc, tf, tb, tm = T("s36", "Arab armies"), T("s36", "ordered its books"), T("s36", "four thousand bathhouses"), T("s36", "six months")
    els = tag(250, 190, "the story", tc, LILAC, 30, "claimed")
    els += [poly([(180, 640), (180, 470), (240, 400), (340, 380), (440, 400), (500, 470), (500, 640)], "rgba(201,193,238,.06)", LILAC, 2.5, tf, style="claimed"),
            poly([(250, 640), (250, 540), (290, 500), (340, 490), (390, 500), (430, 540), (430, 640)], "rgba(201,193,238,.05)", LILAC, 2, tf + .1, style="claimed")]
    els += flame(340, 630, 110, tf + .3, style="claimed", seed=101)
    for j in range(5):
        els += scroll_side(560, 600 - 30 * j, 110, 22, round(tf + .5 + .1 * j, 2), LILAC, style="claimed")
    els += [arrow([[570, 470], [520, 500], [450, 560]], tf + 1.0, LILAC, 3, "claimed", .6)]
    for r_ in range(50):
        els.append(dotrow(780, 1730 - 11, 210 + r_ * 8.6, round(tb + .02 * r_, 2), LILAC, 4.2, 11.9, op=.85))
    els += [lab(1250, 190, "4,000 bathhouses", tb + .4, LILAC, 30)]
    for j in range(6):
        x = 800 + 74 * j
        els += [rect(x, 680, 60, 52, "none", LILAC, 2.2, 6, round(tm - .2 + .15 * j, 2), style="claimed"), circ(x + 30, 706, 7, LILAC, at=round(tm - .1 + .15 * j, 2), fx="pop", op=.8)]
    els += [lab(1290, 716, "six months", tm + .5, LILAC, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def X37(yr):
    return round(150 + (yr - 450) * 1470 / 1580, 1)


def s37():
    """A timeline to today: 642, then a dotted arc to about 1200 (about 560 years) where a quill writes the story first; below, the
    same gap from 1466 to today."""
    tf, tl = T("s37", "first appears"), T("s37", "Like a first report")
    ay = 470
    els = [ln([(120, ay), (1660, ay)], .2, BONE, 2, draw=False)]
    els += [dot(X37(642), ay, 11, GOLD, .4), lab(X37(642) - 16, ay - 22, "642", .5, GOLD, 30, "end")]
    arc = [(X37(642), ay - 12), (X37(800), ay - 170), (X37(1050), ay - 190), (X37(1200), ay - 24)]
    els += [ln(arc, tf, LILAC, 3.5, "claimed", dur=1.4, curve=True), lab(X37(922), ay - 214, "about 560 years", tf + .8, LILAC, 32)]
    els += quill(X37(1203), ay - 6, 70, tf + 1.2) + [lab(X37(1203), ay + 46, "c. 1200", tf + 1.3, LILAC, 30)]
    by = 640
    els += [ln([(X37(1466), by), (X37(2026), by)], tl, GOLD, 8, dur=1.2), lab((X37(1466) + X37(2026)) / 2, by - 24, "the same gap", tl + .8, GOLD, 30),
            lab(X37(1466), by + 46, "1466", tl + .2, BONE, 28), lab(X37(2026) - 10, by + 46, "today", tl + 1.2, BONE, 28, "end")]
    els += merchantman(X37(1466) - 70, by - 6, 70, tl + .3, sail=PAPY) + phone(X37(2026) - 26, by - 96, 44, 72, tl + 1.2, tiles=False)
    els += [ln([(X37(1466), by - 10), (X37(1466), ay + 70)], tl, MUTED, 1.5, "inferred", draw=False), ln([(X37(2026) - 4, by - 100), (X37(2026) - 4, ay + 10)], tl, MUTED, 1.5, "inferred", draw=False)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s38_add():
    """John the Grammarian's life ends about 570, decades before 642; earlier histories sit silent along the gap; a lilac stamp:
    legend."""
    tj, td, te, tg = T("s38", "John the"), T("s38", "decades before"), T("s38", "earlier histories"), T("s38", "a legend")
    ay = 470
    out = [rect(X37(490), ay - 70, X37(570) - X37(490), 18, BONE, at=tj, op=.8, fx="pop"), figure(X37(530), ay - 78, 60, tj, "#f0e0c4"),
           lab(X37(530), ay - 160, "John the Grammarian", tj + .3, BONE, 28)]
    out += bracket(X37(570), X37(642), ay + 24, td, None, BONE, up=True)
    for j, yr in enumerate((690, 800, 900, 1000, 1100)):
        x = X37(yr)
        t = round(te + .3 * j, 2)
        out += scroll_side(x - 34, ay + 110, 60, 16, t) + flame(x, ay + 170, 34, t + .1, style="claimed", c=MUTED)
    out += [lab(X37(895), ay + 230, "earlier histories: silent", te + 1.6, MUTED, 28)]
    out += chip(X37(922), ay - 290, "legend", LILAC, tg, 34)
    return out


# ================================================================== chapter 5: the weighing
LEDGER = [200, 315, 430, 545, 660]
ROWS = ["Caesar's fire: books burned", "the purge of 145 BCE", "the palace quarter wrecked, 270s", "the Serapeum torn down", "the caliph's fire, 642"]


def lpic(k, x, y, at):
    if k == 0:
        return galley(x, y + 20, 80, at, 1, c="#3e2c20", sail="#a08c70") + fire(x, y + 10, 30, at, seed=110, n=2, glow_r=60)
    if k == 1:
        return [figure(x, y + 36, 64, at, "#e8cc90"), crown(x, y + 36 - 63, 10, at)]
    if k == 2:
        return ruin_icon(x, y + 26, 30, at)
    if k == 3:
        return temple_icon(x, y + 26, 28, at)
    return flame(x, y + 30, 58, at, style="claimed")


def lrow(k, at, bright=False):
    y = LEDGER[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)" if bright else "rgba(242,201,142,.03)", "rgba(242,201,142,.35)" if bright else "rgba(242,201,142,.12)", 1.5, 12, at, fx="pop" if bright else None)]
    out += lpic(k, 205, y - 10, at)
    out.append(lab(270, y + 11, ROWS[k], at + .1, BONE if bright else MUTED, 30, "start", op=None if bright else .55))
    return out


def s39():
    """The ledger of endings: five rows, each with its picture, dim; row 1 lights and its two chips pop as the grades are said."""
    t1, g1, t2, g2 = T("s39", "Caesar's fire"), T("s39", "Strong evidence"), T("s39", "The end of"), T("s39", "Ruled out")
    els = [rect(110, 140, 1560, 580, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    for k in range(5):
        els += lrow(k, .3 + .1 * k)
    els += lrow(0, t1, True)
    y = LEDGER[0]
    els += chip(830, y, "Strong evidence", GRADE["strong"], g1 + .5, 26, "start") + [lab(1120, y + 9, "the end?", t2, BONE, 26, "start")] + \
           chip(1250, y, "Ruled out", GRADE["ruled"], g2 + .5, 26, "start")
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s40_add():
    t2, g2, t3, g3 = T("s40", "The purge"), T("s40", "Strong evidence"), T("s40", "The palace quarter"), T("s40", "Strong evidence", k=2)
    return lrow(1, t2, True) + chip(830, LEDGER[1], "Strong evidence", GRADE["strong"], g2 + .5, 26, "start") + \
        lrow(2, t3, True) + chip(830, LEDGER[2], "Strong evidence", GRADE["strong"], g3 + .5, 26, "start")


def s41_add():
    t4, g4, tb, gb, t5, g5 = (T("s41", p) for p in ("The Serapeum", "Established", "A library lost", "Open question", "The caliph's", "Ruled out"))
    return lrow(3, t4, True) + chip(830, LEDGER[3], "Established", GRADE["established"], g4 + .5, 26, "start") + [lab(1066, LEDGER[3] + 9, "books too?", tb, BONE, 26, "start")] + \
        chip(1230, LEDGER[3], "Open question", GRADE["open"], gb + .5, 26, "start") + \
        lrow(4, t5, True) + chip(830, LEDGER[4], "Ruled out", GRADE["ruled"], g5 + .5, 26, "start")


def s42():
    """The verdict on the master timeline: one great dotted flame at a single date ('one great fire') is struck through, a large
    'Ruled out' chip; then a long gold band fades from about 285 BCE to about 400 CE: a long decline."""
    to, tr, td = T("s42", "one great fire"), T("s42", "Ruled out"), T("s42", "a long decline")
    ay = 600
    els = [axis(110, 1670, ay, [[XM(0), "1 CE"], [XM(600), "600"], [XM(1200), "1200"]], .2)]
    els += flame(XM(-48), ay - 10, 230, to, style="claimed", seed=120) + [lab(XM(-48), ay - 270, "one great fire", to + .3, LILAC, 32)]
    els += [strike(XM(-48) - 120, ay - 30, XM(-48) + 120, ay - 250, tr + .4, RED, 7)] + chip(XM(-48) + 380, ay - 170, "Ruled out", GRADE["ruled"], tr + .6, 40)
    x0, x1 = XM(-285), XM(420)
    n = 18
    for k in range(n):
        a, b = x0 + (x1 - x0) * k / n, x0 + (x1 - x0) * (k + 1) / n
        els.append(rect(a, ay + 70, b - a + 1, 30, GOLD, at=round(td + .05 * k, 2), op=round(max(.06, .95 - .05 * k), 2)))
    els += [dot(XM(yr), ay + 85, 7, "#2a1d14", round(td + .6 + .1 * j, 2)) for j, yr in enumerate((-145, -48, 272, 391))]
    els += [lab(XM(70), ay + 140, "a long decline, over centuries", td + .8, GOLD, 32)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s43():
    """Three dashed test boxes fill as named: a dig under the modern city reaching an ancient room of scroll niches; a page of the
    catalogue; an account written in the 640s with a flame and a tick."""
    t1, t2, t3 = T("s43", "own rooms"), T("s43", "A page of its"), T("s43", "an account of the conquest")
    xs = [120, 650, 1180]
    els = []
    for x, t, nm in zip(xs, (t1, t2, t3), ("the library's own rooms", "a page of its catalogue", "an account from the 640s")):
        els += [rect(x, 180, 480, 460, "rgba(159,208,255,.05)", BLUE, 2.5, 14, t - .2, style="inferred"), lab(x + 240, 690, nm, t + .3, BLUE, 28)]
    x = xs[0]
    els += [rect(x + 20, 330, 440, 290, "#4a3a2a", at=t1), rect(x + 20, 330, 300, 6, "#8a6a48", at=t1)]
    els += [rect(x + 40 + 70 * j, 330 - h, 56, h, "#5a6470", "#9aa4b0", 1, 2, t1, fx="rise") for j, h in enumerate((90, 130, 70, 110))]
    els += [{"k": "water", "x0": x + 330, "x1": x + 460, "y": 380, "h": 240, "op": .9, "in": round(t1, 2)}]
    els += [ln([(x + 200, 340), (x + 200, 500)], t1 + .5, BLUE, 3, "inferred", dur=.6), rect(x + 100, 500, 210, 100, "#2a1a10", "#8a6a48", 2, 4, t1 + .8)]
    w, _ = pigeonholes(x + 112, 512, 6, 2, 31, 36, t1 + 1.0, fill=1.0, seed=43, wood="#5a3a22", back="#1e140c", tags=0)
    els += w + [lab(x + 380, 300, "?", t1 + 1.2, BLUE, 50, st="big")]
    x = xs[1]
    els += [rect(x + 60, 220, 360, 380, PAPY, PAPY_E, 1.2, 4, t2, fx="pop")]
    els += [ln([(x + 80, 262), (x + 400, 262)], t2 + .2, "#8a6a44", 1.5, draw=False)] + [ln([(x + cx, 240), (x + cx, 580)], t2 + .2, "#8a6a44", 1, draw=False, op=.5) for cx in (150, 240, 340)]
    els += [ln([(x + 84 + c * 90, 300 + 36 * k), (x + 84 + c * 90 + 50, 300 + 36 * k)], round(t2 + .3 + .03 * k, 2), "#6a4a30", 2, draw=False) for k in range(8) for c in range(4)]
    x = xs[2]
    els += sheet(x + 80, 250, 320, 270, t3, rows=6, seed=50) + [rect(x + 180, 268, 120, 40, PAPY, at=t3 + .2), lab(x + 240, 298, "640s", t3 + .3, "#5a3a20", 32, st="serif", halo=False)]
    els += flame(x + 330, 500, 50, t3 + .6, seed=130) + [tick(x + 400, 580, t3 + 1.0, GREEN, 1.3)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s44():
    """About 300 plays as theatre masks, by playwright; 33 light up gold (7, 7 and 19 survive); then the Tables of Callimachus crumble
    to a few dozen fragments."""
    tp, ts, tt = T("s44", "three hundred plays"), T("s44", "Thirty three survive"), T("s44", "Even the Tables")
    bands = [("Aeschylus", 80, 7), ("Sophocles", 123, 7), ("Euripides", 97, 19)]
    els = [lab(630, 170, "about 300 plays", tp + .2, BONE, 32)]
    k = 0
    r = random.Random(9)
    for bi, (nm, n, sv) in enumerate(bands):
        idx = list(range(k, k + n))
        keep = set(r.sample(idx, sv))
        for i in idx:
            row, col = divmod(i, 20)
            x, y = 180 + col * 46, 230 + row * 33
            els += mask(x, y, 13, round(tp + .02 * row, 2), "#efe3c8", op=.4)
            if i in keep:
                els += mask(x, y, 13, round(ts + .3 * bi + .02 * (i - k), 2), AU) + [gl(x, y, 30, round(ts + .3 * bi, 2), .5)]
        mid = (k + n / 2) // 20
        els.append(lab(1130, 230 + mid * 33 + 10, "%s: %d" % (nm, sv), ts + .3 * bi + .3, AU, 28, "start"))
        k += n
    els += [lab(630, 760 - 20, "33 survive", ts + 1.2, AU, 34)]
    els += scroll_side(1350, 640, 260, 40, tt - 1.0) + [lab(1480, 590, "the Tables", tt - .8, BONE, 28)]
    els += [rect(1340, 610, 280, 64, "#2a1f17", at=tt + .4, dur=.8)]
    els += [poly(E(r.uniform(1350, 1610), r.uniform(615, 690), r.uniform(4, 9), r.uniform(3, 7), 8), PAPY, at=round(tt + .5 + .03 * q, 2), fx="pop") for q in range(26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s45():
    """Euclid's first proposition draws itself (two circles and the triangle on their centres); then a chain of copies: papyrus,
    Greek, Arabic, Latin, print."""
    te, tc = T("s45", "Euclid's geometry"), T("s45", "copied and recopied")
    A, B, r_ = (800, 380), (980, 380), 180
    C = (890, 380 - 156)
    els = [ln(E(A[0], A[1], r_, r_, 60), te, GOLD, 2.5, dur=1.0, op=.85), ln(E(B[0], B[1], r_, r_, 60), te + .4, GOLD, 2.5, dur=1.0, op=.85),
           ln([A, B, C, A], te + 1.0, BONE, 4, dur=.9), dot(A[0], A[1], 7, BONE, te), dot(B[0], B[1], 7, BONE, te + .2), dot(C[0], C[1], 7, BONE, te + 1.6),
           lab(1220, 260, "Euclid, about 300 BCE", te + .3, GOLD, 30, "start"), gl(890, 330, 300, te + 1.4, .3)]
    steps = [("papyrus, about 100", lambda x, y, a: aged_sheet(x - 40, y - 46, 80, 70, a, 2, seed=77)),
             ("Greek, 800s", lambda x, y, a: book(x - 30, y - 50, 60, 80, a, "#5a3a26")),
             ("Arabic, 800s", lambda x, y, a: book(x - 30, y - 50, 60, 80, a, "#2f4a3a")),
             ("Latin, 1100s", lambda x, y, a: book(x - 30, y - 50, 60, 80, a, "#6a2a22")),
             ("printed, 1482", lambda x, y, a: book(x - 34, y - 56, 68, 90, a, "#3a3a52"))]
    for j, (nm, ic) in enumerate(steps):
        x, y = 250 + 320 * j, 660
        t = round(tc + .45 * j, 2)
        els += ic(x, y, t) + [lab(x, y + 64, nm, t + .2, BONE, 24)]
        if j < 4:
            els.append(arrow([[x + 60, y - 10], [x + 160, y - 18], [x + 255, y - 10]], t + .25, MUTED, 2.5, dur=.4))
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


V46 = View(24, 50, 26.5, 38.5, rect=(90, 130, 1600, 660))


def s46():
    """Map Alexandria to Baghdad: a gold arrow; at Baghdad a manuscript in a flowing script and a cone diagram that glows: found only
    in Arabic."""
    tb, tn = T("s46", "translators in"), T("s46", "found nowhere else")
    v = V46
    ax, ay = v.p(29.92, 31.2)
    bx, by = v.p(44.37, 33.31)
    els = [{"k": "map", "land": v.land(), "in": -1}, {"k": "pin", "x": ax, "y": ay, "t": "Alexandria", "c": GOLD, "in": .3, "lx": -18, "ly": 34, "a": "end"},
           {"k": "pin", "x": bx, "y": by, "t": "Baghdad", "c": GOLD, "in": tb, "lx": 18, "ly": 36}]
    els += [arrow([(ax + 10, ay - 10), ((ax + bx) / 2, min(ay, by) - 150), (bx - 12, by - 14)], tb, GOLD, 4, dur=1.4), lab((ax + bx) / 2, min(ay, by) - 170, "800s", tb + .6, GOLD, 28)]
    cx, cy = bx + 60, by - 330
    els += open_codex(cx, cy, 130, 170, tb + 1.0) + [{"k": "glyphs", "x": cx - 116, "y": cy + 20, "w": 104, "h": 130, "rows": 7, "cols": 5, "kind": "hieratic", "c": "#3a2a1c",
                                                     "sw": 2.2, "in": round(tb + 1.3, 2)}]
    els += [ln([(cx + 64, cy + 24), (cx + 22, cy + 150), (cx + 106, cy + 150), (cx + 64, cy + 24)], tn - .3, "#3a2a1c", 2, dur=.6), ln(E(cx + 64, cy + 150, 42, 9, 24), tn, "#3a2a1c", 2, dur=.5),
            ln(E(cx + 64, cy + 105, 26, 13, 24), tn + .2, "#9a5a10", 2.5, dur=.5), gl(cx + 64, cy + 100, 160, tn + .3, .5)]
    els += [lab(cx, cy + 230, "found only in Arabic", tn + .5, GOLD, 30)]
    return {"base": "map", "cam": CAM, "els": els}


def s47():
    """A cross-section of a desert rubbish mound beside a town: its layers packed with hundreds of small papyrus scraps; two diggers
    with baskets on top; about 500,000 pieces; a few scraps glow: lost works."""
    th, tc, tl = T("s47", "rubbish dumps"), T("s47", "half a million"), T("s47", "lost works")
    els = [rect(-10, -10, 1800, 600, "url(#k-sky-day)", at=-1), rect(-10, 560, 1800, 460, "url(#k-sand)", at=-1)]
    els += [rect(1420 + 60 * j, 480 - 30 * (j % 2), 54, 80 + 30 * (j % 2), "#a8906a", "#7a6448", 1, 2, -1) for j in range(5)]
    mound = [(220, 600), (360, 470), (520, 380), (700, 330), (900, 320), (1080, 350), (1250, 430), (1380, 560), (1400, 600)]
    els += [poly(mound + [(1400, 760), (220, 760)], "#8a7050", "#c9ad85", 1.5, th, fx="rise")]
    bands = ["#7a6248", "#8e7556", "#6e573f", "#9a8060", "#7f6649"]
    for j in range(5):
        y0 = 380 + 76 * j
        els.append(poly([(x, max(y, y0)) for x, y in mound] + [(1400, y0 + 76), (220, y0 + 76)], bands[j], at=round(th + .2 + .1 * j, 2), op=.9))
    r = random.Random(47)
    for q in range(170):
        x = r.uniform(300, 1320)
        top = min(y for xx, y in mound if abs(xx - x) < 200) + 30
        y = r.uniform(max(top, 360), 740)
        els.append(poly(E(x, y, r.uniform(5, 11), r.uniform(3, 7), 6), "#efe3c8", at=round(tc + .006 * q, 2), op=.85, fx="pop"))
    els += [figure(760, 336, 70, th + .6, "#f0e0c4"), figure(980, 330, 66, th + .8, "#e6d2b0"), poly(E(800, 318, 22, 12, 10), "#6b4a30", at=th + .9, fx="pop")]
    els += [lab(1440, 200, "about 500,000 pieces", tc + .8, GOLD, 34), lab(1440, 244, "Oxyrhynchus", tc + 1.0, MUTED, 26, st="ital")]
    for j, (x, y) in enumerate(((520, 560), (860, 640), (1180, 600))):
        els += [gl(x, y, 70, round(tl - .2 + .25 * j, 2), .9), poly(E(x, y, 12, 8, 6), AU, at=round(tl - .2 + .25 * j, 2), fx="pop")]
    els += [lab(860, 790 - 40, "lost works", tl + .5, AU, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s48():
    """Night: the hall of pigeonholes from the opening, now mostly empty; one scribe at a desk under a lamp copies a scroll."""
    els, cells = hall_room(-1, fill=.18, seed=21, lit=False)
    els += [rect(-10, -10, 1800, 1020, "rgba(8,10,20,.35)", at=-1)]
    els += scribe(840, 730, 200, .4, "#e8d6b8", face=1)
    els += lamp(1010, 640, 60, .8, .8) + [gl(980, 600, 520, 1.0, .35)]
    els += [ln([(910, 640), (930, 636), (950, 641), (968, 636)], 2.0, "#6a4a30", 2.5, dur=1.6)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "That, the story", "s2"), (1, "But how do you", "s3"), (1, "Historians weigh", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "His family built", "s7")], {"chapter": "Every book in the world"}),
    (1, 1, "collision", "s8", [(1, "But it was less", "s9")], {}),
    (1, 2, "cost", "s10", [(0, "Books on any ship", "s11"), (1, "The third Ptolemy", "s12")], {}),
    (1, 3, "reversal", "s13", [(1, "Even a little", "s14"), (1, "A map of Greek", "s14b")], {}),
    (2, 0, "world", "s15", [], {"chapter": "Caesar's fire"}),
    (2, 1, "collision", "s16", [(1, "About a century", "s17"), (2, "The later the", "s18"), (3, "One more witness", "s19")], {}),
    (2, 2, "cost", "s20", [(1, "So the historian", "s21")], {}),
    (2, 3, "reversal", "s22", [(1, "Decades later", "s23")], {}),
    (3, 0, "world", "s24", [(1, "The head of the", "s25")], {"chapter": "The slow fires"}),
    (3, 1, "collision", "s26", [(1, "A book survived", "s27")], {}),
    (3, 2, "cost", "s28", [(0, "A Roman historian", "s29")], {}),
    (4, 0, "world", "s30", [(1, "An ancient writer", "s31")], {"chapter": "A temple and a legend"}),
    (4, 1, "collision", "s32", [(1, "A Roman historian", "s33")], {}),
    (4, 2, "cost", "s34", [(1, "And teaching went", "s35")], {}),
    (4, 3, "reversal", "s36", [(1, "That story first", "s37"), (1, "Its hero", "s38")], {}),
    (5, 0, "weigh", "s39", [(1, "The purge of", "s40"), (2, "The Serapeum torn", "s41"), (3, "So,", "s42")], {"chapter": "The weighing"}),
    (5, 1, "test", "s43", [], {}),
    (5, 2, "close", "s44", [(1, "But some came", "s45"), (1, "Alexandrian science", "s46"), (1, "And from Egypt", "s47"), (2, "Libraries don't", "s48")], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.4, 600, 450], "s2_add"),
    "s9": ("s8", [1, 889, 500], "s9_add"),
    "s14": ("s13", [1.5, 1185, 400], "s14_add"), "s14b": ("s13", [1, 889, 500], "s14b_add"),
    "s17": ("s16", [1, 889, 500], "s17_add"), "s18": ("s16", [1, 889, 500], "s18_add"),
    "s31": ("s30", [1.5, 760, 430], "s31_add"),
    "s38": ("s37", [1, 889, 500], "s38_add"),
    "s40": ("s39", [1, 889, 500], "s40_add"), "s41": ("s39", [1, 889, 500], "s41_add"),
}


def _placeholder(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 460, sid, .2, GOLD, 60, st="serif")]}


def _segments(script):
    """The narration each shot has on screen, from the beats with their markers (a chapter beat's first sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[@%s]" % sid)
        text = " ".join(lines)
        parts = re.split(r"\[@([\w]+)\]", text)
        head = parts[0]
        if kw.get("chapter"):
            acts = [m.start() for m in re.finditer(r"\[act:", head)]
            if len(acts) > 1:
                head = head[acts[1]:]
        if role != "title":
            say[frm] = say.get(frm, "") + " " + head if frm in say else head
        for k in range(1, len(parts), 2):
            say[parts[k]] = parts[k + 1]
    return say


def film():
    script = json.load(open(SCRIPT, encoding="utf-8"))
    SAY.clear(); SAY.update(_segments(script))
    g = globals()
    panels = {}
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in ALIASES and sid not in panels:
                panels[sid] = g[sid]() if sid in g else _placeholder(sid)
    ids = list(panels) + [a for a in ALIASES]
    idx = {s: i for i, s in enumerate(ids)}
    shots = [panels[s] for s in panels] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[idx[sid]] = idx[root]
        cams[idx[sid]] = [z] + list(cam[1:])
        tags[z] = (g[fn]() if fn in g else []) if fn else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-alexandria", "code": "LF.13", "series": script["series"], "title": script["title"], "case": "alexandria-library",
          "verdict": "debunked", "claim": "Was the Library of Alexandria destroyed in one great fire?", "mood": "mystery",
          "hook_text": "How do you lose a whole *library*?", "beats": beats, "shots": shots,
          "sources": "Bagnall 2002 (Proc. Am. Philos. Soc. 146: 348-362) · El-Abbadi 1990 · Fraser 1972 · Canfora 1989 · MacLeod (ed.) 2000 · "
                     "Strabo 17.1.8 · Seneca Tranq. 9.5 · Plutarch Caes. 49 · Dio 42.38 · Ammianus 22.16 · Lewis 1990 · "
                     "Witty 1958 (doi:10.1086/618523) · McKenzie, Gibson & Reyes 2004 (doi:10.2307/4135011) · Toomer 1990 (doi:10.1007/978-1-4613-8985-9)",
          "post": "Everyone knows the Library of Alexandria burned. Five endings across nearly eight centuries, what each ancient witness actually says, "
                  "a caliph story written down 560 years late, and the slower way great libraries really die, weighed.",
          "hashtags": ["#LibraryOfAlexandria", "#AncientEgypt", "#History", "#Books", "#Unreadable", "#WeighItYourself"],
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
