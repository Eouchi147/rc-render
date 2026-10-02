"""LF.10 · Unreadable · The Voynich Manuscript: Message or Nonsense? (16:9 long film, one wall).

The script is films/long/lf-voynich/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s53; s5, the title, is the intro card
over the panel of s3/s4), drawn while it is said: a painted plant and lines of an unknown alphabet, a letter found inside
the book, the radiocarbon clock, a tour of its six kinds of pages, the word counts that look like language and the letter counts that look like nothing we know, a century of failed solutions
(Newbold's lens, Friedman's anagram, the modern parade), the hoax recipes (Rugg's table and grille, self-citation, volunteers'
gibberish, a dice-and-cards cipher) and the weighing. Drawings are schematic and true to the numbers said: solid = measured,
dashed = inferred, dotted = claimed. The Voynich words drawn are real EVA spellings (daiin, chedy, qokeedy...) written with a
small stroke alphabet of the script's letter shapes (VG below); no reading of them is implied.

Facts: the Shorts 'voynich' (f12.py, rewrite/voynich.json), 'lost-scripts' and 'unreadable-ledger', and the script's facts_added
(Hodgins 2011, Zandbergen voynich.nu, Manly 1931, Friedman 1959, Currier 1976, Bennett 1976, Reddy & Knight 2011, Montemurro &
Zanette 2013, Davis 2020, Lindemann & Bowern 2020, Rugg 2004, Rugg & Taylor 2016, Timm & Schinner 2020, Hauer & Kondrak 2016,
Gaskell & Bowern 2022, Greshko 2025, The Art Newspaper 2024).

Engine workaround (as in lf_atlantis.py): the wall only adds elements to a panel on its first visit, at a beat start or a line
start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a tiny
unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions
as a panel item (kit.js builds them on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-voynich/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-voynich/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-voynich RC_FILMS_EPS=/tmp/claude-0/sbx_lf-voynich/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-voynich/boards python3 films.py long.lf_voynich
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-voynich", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
VEL, VEL_E, VEL_D = "#e8d9b8", "#fff4dc", "#cdbb95"           # vellum, its lit edge, its shade
INK = "#4a3424"                                                # the scribes' brown ink
LEAF, LEAF_D, ROOT, STEM = "#7fa05a", "#5d8a3e", "#9a6a40", "#5f8a4a"
FLOWR, AZUR, OCHRE, VERD = "#c0503a", "#5b86c0", "#b0503a", "#5f9a6a"
POOL, POOL_E, SKIN = "#5f9a8a", "#9fd0c0", "#efd2b8"
WOOD, WOOD_D = "#6b4a30", "#3a281a"
GRADE = {"established": "#8fd9b0", "ruled": "#e98a8a", "awaiting": "#c9c1ee", "open": "#f0b06a"}
CA, CB = "#e8b87a", "#7fb6e6"                                 # Currier A and B
HI = "#c8401e"                                                 # a highlight that shows on vellum (vermilion)
WPS = 2.3                    # spoken words a second (the narrator's pace, pauses included)


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


def E(cx, cy, rx, ry, n=36):
    return ellipse(cx, cy, rx, ry, n)[:-1]


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
    x0 = x - w / 2 if a == "middle" else x
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
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def vbar(x, base, h, wd, c, at, op=None, fx="fill", dur=.5, style="known", edge="none"):
    """A vertical bar standing on `base`, growing up from it."""
    return rect(x - wd / 2, base - h, wd, h, c, edge, 1.5 if edge != "none" else 0, 3, at, fx=fx, op=op, dur=dur, style=style)


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


def padlock(x, y, s, at, c=LILAC, style="claimed", fill="rgba(201,193,238,.08)"):
    k = s / 100.
    return [rect(x - 55 * k, y - 20 * k, 110 * k, 84 * k, fill, c, 3, 12 * k, at, style=style),
            {"k": "line", "p": R([(x - 36 * k, y - 20 * k), (x - 34 * k, y - 56 * k), (x, y - 78 * k), (x + 34 * k, y - 56 * k), (x + 36 * k, y - 20 * k)]), "c": c, "w": 4,
             "style": style, "curve": True, "in": round(at, 2)},
            dot(x, round(y + 16 * k, 1), round(8 * k, 1), c, round(at + .3, 2))]


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


# ================================================================== the Voynich script: a small stroke alphabet (EVA letters)
# Each letter: (advance, [strokes]); x-height = 10 units, baseline y = 0, up is negative; gallows reach about -17.
_C = [(7.5, -8.2), (4.8, -9.8), (1.6, -7.0), (1.6, -2.6), (4.4, -0.1), (7.6, -1.6)]          # the 'c' shape of e, ch, sh, s


def _sh(pts, dx=0.0):
    return [(x + dx, y) for x, y in pts]


VG = {
    "o": (10.0, [E(5, -5, 4.2, 4.8, 14) + [E(5, -5, 4.2, 4.8, 14)[0]]]),
    "a": (11.5, [[(7.8, -8.2), (5.0, -9.8), (1.8, -7.5), (1.4, -3.0), (3.8, -0.2), (7.2, -1.6)], [(8.4, -9.6), (8.2, -3.0), (8.8, -0.4), (10.2, 0)]]),
    "e": (9.0, [_C]),
    "i": (5.0, [[(1.6, -9.5), (1.5, -3.0), (2.2, -0.4), (3.6, 0)]]),
    "n": (9.0, [[(1.6, -9.5), (1.5, -2.5), (2.6, -0.1), (5.0, -1.0), (7.0, -6.0), (7.4, -11.0), (6.0, -13.0)]]),
    "r": (8.5, [[(1.6, -9.0), (1.4, -1.0), (2.5, 0)], [(1.7, -6.5), (3.6, -9.8), (6.5, -9.6), (7.5, -8.0)]]),
    "l": (8.0, [[(6.0, -13.5), (3.5, -9.0), (2.4, -3.0), (3.6, -0.2), (6.8, -0.8)]]),
    "s": (9.0, [_C, [(1.6, -8.5), (3.0, -12.5), (6.5, -13.0)]]),
    "d": (10.5, [[(8.6, -15.0), (5.4, -14.2), (4.4, -11.5), (7.5, -9.0), (8.6, -5.0), (6.6, -0.6), (3.0, -0.4), (1.4, -3.6), (3.2, -6.8), (6.6, -7.0)]]),
    "y": (10.0, [[(7.6, -8.0), (4.8, -9.8), (1.8, -7.6), (2.2, -4.2), (5.0, -3.4), (7.6, -6.2), (7.8, -9.0), (7.6, -1.0), (5.6, 3.6), (2.0, 4.4), (0.6, 3.0)]]),
    "q": (11.0, [[(8.0, 1.0), (8.0, -12.0), (1.0, -4.0), (10.5, -4.5)]]),
    "k": (12.5, [[(2.0, 0.5), (2.2, -16.5)], [(2.2, -15.5), (5.8, -17.0), (9.4, -15.0), (8.8, -10.5), (5.2, -9.0), (2.4, -10.5)], [(9.2, -14.0), (9.6, 0.5)]]),
    "t": (13.0, [[(4.0, 0.5), (4.2, -16.5)], [(4.2, -11.0), (0.8, -13.6), (2.2, -17.0), (7.2, -15.4), (10.4, -10.0), (10.8, 0.5)]]),
    "ch": (16.5, [_C, _sh(_C, 7.5), [(4.4, -9.4), (13.2, -9.4)]]),
    "sh": (16.5, [_C, _sh(_C, 7.5), [(4.4, -9.4), (13.2, -9.4)], [(3.0, -10.5), (4.6, -14.6), (7.6, -15.0), (9.2, -12.6)]]),
}
VG["p"] = (VG["k"][0], VG["k"][1] + [[(-1.0, -15.8), (12.5, -15.8)]])
VG["f"] = (VG["t"][0], VG["t"][1] + [[(-0.5, -15.8), (13.5, -15.8)]])
_CURVE = {"q": False}


def _letters(word):
    out, i = [], 0
    while i < len(word):
        two = word[i:i + 2]
        if two in ("ch", "sh"):
            out.append(two); i += 2
        else:
            out.append(word[i] if word[i] in VG else "o"); i += 1
    return out


def vwidth(word, s=1.0, gap=0.6):
    return sum(VG[g][0] + gap for g in _letters(word)) * s


def vword(x, y, word, s=1.0, at=0, c=INK, w=2.2, fx="fade", dur=.3, op=None, style="known", hi=None, hic=AU, gap=0.6):
    """One Voynich word in EVA spelling at (x, baseline y), x-height 10*s. hi: indices of letters drawn in hic (a highlight)."""
    out, cx = [], x
    for k, g in enumerate(_letters(word)):
        adv, strokes = VG[g]
        col = hic if hi and k in hi else c
        for st in strokes:
            e = {"k": "line", "p": R([(cx + px * s, y + py * s) for px, py in st]), "c": col, "w": w, "curve": _CURVE.get(g, True) and len(st) > 2,
                 "in": round(at, 2), "style": style}
            if fx:
                e.update(fx=fx, dur=dur)
            if op is not None:
                e.update(op=op, keepop=True)
            out.append(e)
        cx += (adv + gap) * s
    return out


def vline(x, y, ws, s=1.0, at=0, c=INK, w=2.2, space=7.0, dt=.12, op=None, style="known", maxw=None, fx="fade"):
    """A line of Voynich words, each drawn dt after the last; returns (elements, end x)."""
    out, cx = [], x
    for k, wd in enumerate(ws):
        wdt = vwidth(wd, s)
        if maxw and cx + wdt > x + maxw:
            break
        out += vword(cx, y, wd, s, at + dt * k, c, w, fx, op=op, style=style)
        cx += wdt + space * s
    return out, cx


EVA = ["daiin", "chedy", "qokeedy", "ol", "shedy", "chol", "or", "aiin", "qokain", "dar", "chey", "okaiin", "shol", "otedy", "chor", "qokedy",
       "okal", "dy", "sheol", "ykeedy", "chdy", "qokal", "okeey", "dal", "shey", "otaiin", "ar", "cheol", "lchedy", "qoky", "sain", "dain", "okar", "cheey"]


def evas(n, seed):
    r = random.Random(seed)
    return [r.choice(EVA) for _ in range(n)]


def vtext(x0, y0, wdt, rows, s, at, lh=None, seed=1, c=INK, w=2.0, dt=.05, row_dt=.45, first=None, op=None, fx="fade"):
    """A block of Voynich text: rows of real EVA words filling the width, written row by row."""
    out, lh = [], lh or 26 * s
    for r in range(rows):
        ws = evas(12, seed * 31 + r)
        if first and r == 0:
            ws = list(first) + ws
        els, _ = vline(x0, y0 + r * lh, ws, s, at + row_dt * r, c, w, dt=dt, op=op, maxw=wdt, fx=fx)
        out += els
    return out


# ================================================================== pages and the six kinds of picture in the book
def page(x, y, w, h, at=-1, fx=None, shade=True, c=VEL, op=None):
    """A vellum page: a soft shadow, the sheet, a lit edge."""
    out = []
    if shade:
        out.append(rect(x + 8, y + 12, w, h, "rgba(0,0,0,.35)", r=6, at=at))
    out.append(rect(x, y, w, h, c, VEL_E, 1.2, 6, at, fx=fx, op=op))
    return out


def plant(cx, by, h, at, kind=0, s=None, flower=FLOWR, step=1.0):
    """A plant in the manner of the herbal pages, roots on by, h tall: a fat root with side tubers and tendrils, a wavy stem, alternate
    veined leaves, a flower head (kind 0 red, 1 berries, 2 blue rosette, 3 spiky). Everything builds from the roots up."""
    k = h / 400.
    w = (s or 1.0)
    P = lambda a, b: (cx + a * k, by + b * k)
    t = lambda d: round(at + d * step, 2)
    out = [poly([P(-70, -40), P(-36, -72), P(30, -74), P(72, -40), P(64, -4), P(22, 12), P(-26, 10), P(-66, -6)], ROOT, INK, 2, t(0), "pop", curve=True)]
    if kind in (0, 3):
        out.append(poly([P(56, -26), P(92, -40), P(112, -18), P(92, 4), P(62, -2)], "#a8784a", INK, 1.6, t(.05), "pop", curve=True))
    if kind in (1, 2):
        out.append(poly([P(-56, -24), P(-94, -36), P(-110, -14), P(-90, 4), P(-60, -2)], "#a8784a", INK, 1.6, t(.05), "pop", curve=True))
    out += [ln([P(-40 + 20 * j, -50 + 6 * (j % 2)), P(-30 + 20 * j, -30)], t(.1), "rgba(58,40,24,.55)", 1.4, draw=False) for j in range(4)]
    for dx, dy, ex, ey in ((-50, -2, -96, 40), (-20, 8, -40, 58), (18, 10, 44, 62), (52, -2, 100, 36), (0, 10, 4, 72)):
        out.append(ln([P(dx, dy), P((dx + ex) / 2 + 6, (dy + ey) / 2), P(ex, ey)], t(.15), INK, 2.2 * w, curve=True, dur=.4))
    top = -340 if kind != 2 else -300
    stem = [P(0, -70), P(-8, -140), P(6, -210), P(-4, -280), P(0, top)]
    out.append(ln(stem, t(.35), STEM, 7 * w, curve=True, dur=.6))
    if kind in (0, 3):
        lv = [(-120, .62, 1), (-150, .58, -1), (-190, .52, 1), (-220, .48, -1), (-255, .4, 1), (-280, .34, -1)]
    else:
        lv = [(-125, .52, -1), (-125, .52, 1), (-205, .44, -1), (-205, .44, 1)]
    for j, (yy, sc, sd) in enumerate(lv):
        L = 150 * sc
        base = P(sd * 4, yy)
        tipx, tipy = base[0] + sd * L * k * 1.0, base[1] - L * k * .35
        mid1 = (base[0] + sd * L * k * .45, base[1] - L * k * .44)
        mid2 = (base[0] + sd * L * k * .55, base[1] + L * k * .14)
        if kind == 1:
            leaf = [base, (base[0] + sd * L * k * .3, base[1] - L * k * .3), (tipx, tipy), (base[0] + sd * L * k * .7, base[1] + L * k * .05), (base[0] + sd * L * k * .25, base[1] + L * k * .06)]
        elif kind == 3:
            leaf = [base, (base[0] + sd * L * k * .3, base[1] - L * k * .34), (base[0] + sd * L * k * .45, base[1] - L * k * .2), (base[0] + sd * L * k * .65, base[1] - L * k * .42),
                    (tipx, tipy), (base[0] + sd * L * k * .6, base[1] + L * k * .1), (base[0] + sd * L * k * .3, base[1] + L * k * .08)]
        else:
            leaf = [base, mid1, (tipx, tipy), mid2]
        out.append(poly(leaf, LEAF if j % 2 else LEAF_D, INK, 1.6, t(.65 + .1 * j), "pop", curve=kind != 3))
        vx, vy = (base[0] + tipx) / 2, (base[1] + tipy) / 2 - 2 * k
        out.append(ln([base, (vx, vy), (tipx, tipy)], t(.72 + .1 * j), "rgba(40,50,20,.6)", 1.4, curve=True, draw=False))
        if h > 200:
            for q in (.35, .6):
                qx, qy = base[0] + (tipx - base[0]) * q, base[1] + (tipy - base[1]) * q
                out.append(ln([(qx, qy), (qx + sd * 10 * k, qy - 12 * k)], t(.72 + .1 * j), "rgba(40,50,20,.45)", 1.1, draw=False))
                out.append(ln([(qx, qy), (qx + sd * 12 * k, qy + 8 * k)], t(.72 + .1 * j), "rgba(40,50,20,.45)", 1.1, draw=False))
    fx_, fy_ = P(0, top)
    if kind == 2:
        for a in range(0, 360, 45):
            out.append(poly(E(fx_ + 22 * k * math.cos(math.radians(a)), fy_ + 22 * k * math.sin(math.radians(a)), 16 * k, 16 * k, 10), AZUR, INK, 1.4, t(1.25), "pop"))
        out.append(circ(fx_, fy_, 14 * k, "#e8c35a", INK, 1.4, t(1.35), "pop"))
    elif kind == 1:
        for j, (bx, by_) in enumerate(((-18, -14), (16, -20), (0, -40), (-30, -40), (28, -44))):
            out.append(circ(fx_ + bx * k, fy_ + by_ * k, 13 * k, "#b03a2a", INK, 1.3, t(1.2 + .05 * j), "pop"))
    else:
        pet = [(-50, -8), (-44, -40), (-26, -60), (-12, -46), (0, -78), (12, -46), (26, -60), (44, -40), (50, -8), (0, 8)] if kind != 3 else \
              [(-30, 4), (-40, -50), (-14, -40), (0, -80), (14, -40), (40, -50), (30, 4)]
        out.append(poly([(fx_ + a * k, fy_ + b * k) for a, b in pet], flower, INK, 1.8, t(1.25), "pop", curve=kind != 3))
        if kind == 0:
            out.append(poly([(fx_ + a * k * .55, fy_ + b * k * .5 - 6 * k) for a, b in pet], "#e07a5a", "none", 0, t(1.3), "pop", curve=True))
        out.append(poly([(fx_ - 28 * k, fy_ + 4 * k), (fx_ + 28 * k, fy_ + 4 * k), (fx_ + 12 * k, fy_ + 26 * k), (fx_ - 12 * k, fy_ + 26 * k)], LEAF_D, INK, 1.4, t(1.2), "pop"))
    if kind == 0 and h > 200:
        bx_, by2 = P(-4, -232)
        out += [ln([(bx_, by2), (bx_ - 40 * k, by2 - 40 * k), (bx_ - 58 * k, by2 - 76 * k)], t(1.0), STEM, 4 * w, curve=True, dur=.4),
                poly(E(bx_ - 60 * k, by2 - 86 * k, 10 * k, 15 * k, 12), flower, INK, 1.4, t(1.35), "pop")]
    return out


def star5(x, y, r, at, c=AU):
    pts = [(x + (r if k % 2 == 0 else r * .45) * math.sin(math.pi * k / 5), y - (r if k % 2 == 0 else r * .45) * math.cos(math.pi * k / 5)) for k in range(10)]
    return poly(pts, c, at=at)


def fish(x, y, s, at, c="#d8c9a6", face=1):
    k = s / 100.
    P = lambda a, b: (x + face * a * k, y + b * k)
    return [poly([P(-50, 0), P(-20, -22), P(26, -16), P(46, 0), P(26, 16), P(-20, 22)], c, INK, 1.5, at, "pop", curve=True),
            poly([P(-48, 0), P(-74, -20), P(-70, 0), P(-74, 20)], c, INK, 1.5, at, "pop")]


def zodiac(cx, cy, r, at, step=.04):
    """A zodiac roundel in the manner of the astronomical pages: rings, small figures each holding a star, two fish in the centre."""
    out = [circ(cx, cy, r, "rgba(91,134,192,.10)", INK, 2, at, "pop"), circ(cx, cy, r * .72, "none", INK, 1.6, at + .1), circ(cx, cy, r * .4, "rgba(232,195,90,.18)", INK, 1.6, at + .15)]
    for j in range(12):
        a = 2 * math.pi * j / 12
        sx, sy = cx + r * .86 * math.cos(a), cy + r * .86 * math.sin(a)
        out.append(star5(sx, sy, 6 * r / 110, at + .3 + step * j))
        px, py = cx + r * .56 * math.cos(a + .26), cy + r * .56 * math.sin(a + .26)
        out.append(circ(px, py - 6, 4.5 * r / 110, SKIN, INK, 1, at + .35 + step * j))
        out.append(ln([(px, py - 2), (px, py + 9 * r / 110)], at + .35 + step * j, SKIN, 3 * r / 110, draw=False))
    out += fish(cx - 12 * r / 110, cy - 10 * r / 110, 26 * r / 110, at + .9) + fish(cx + 12 * r / 110, cy + 12 * r / 110, 26 * r / 110, at + 1.0, face=-1)
    return out


def pools(x, y, w, h, at, n_fig=6):
    """Two green pools joined by pipes, small bathing figures (heads and shoulders above the water; no anatomical detail)."""
    out = []
    P1 = [(x + .05 * w, y + .35 * h), (x + .25 * w, y + .28 * h), (x + .5 * w, y + .32 * h), (x + .62 * w, y + .45 * h), (x + .5 * w, y + .58 * h), (x + .15 * w, y + .58 * h)]
    P2 = [(x + .3 * w, y + .72 * h), (x + .6 * w, y + .68 * h), (x + .95 * w, y + .74 * h), (x + .9 * w, y + .92 * h), (x + .45 * w, y + .95 * h), (x + .25 * w, y + .88 * h)]
    out.append(ln([(x + .55 * w, y + .08 * h), (x + .8 * w, y + .1 * h), (x + .88 * w, y + .3 * h), (x + .8 * w, y + .6 * h), (x + .72 * w, y + .72 * h)], at, POOL_E, max(4, w * .03), curve=True, dur=.6))
    out.append(ln([(x + .02 * w, y + .1 * h), (x + .2 * w, y + .12 * h), (x + .25 * w, y + .3 * h)], at + .1, POOL_E, max(4, w * .03), curve=True, dur=.5))
    out.append(ln([(x + .4 * w, y + .58 * h), (x + .42 * w, y + .7 * h)], at + .2, POOL_E, max(4, w * .03), dur=.3))
    out.append(poly(P1, POOL, INK, 1.6, at + .2, "pop", curve=True))
    out.append(poly(P2, POOL, INK, 1.6, at + .3, "pop", curve=True))
    figs = [(.2, .44), (.33, .41), (.46, .45), (.42, .8), (.58, .78), (.74, .82)][:n_fig]
    for j, (a, b) in enumerate(figs):
        fx_, fy_ = x + a * w, y + b * h
        k = w / 250.
        out += [poly([(fx_ - 9 * k, fy_ + 6 * k), (fx_ - 7 * k, fy_ - 10 * k), (fx_ + 7 * k, fy_ - 10 * k), (fx_ + 9 * k, fy_ + 6 * k)], SKIN, INK, 1, at + .5 + .08 * j, "rise"),
                circ(fx_, fy_ - 16 * k, 6 * k, SKIN, INK, 1, at + .5 + .08 * j, "rise")]
    out.append(poly([(P1[-1][0], y + .53 * h), (P1[3][0] - 6, y + .53 * h), (P1[3][0], P1[3][1]), (P1[4][0], P1[4][1]), (P1[5][0], P1[5][1])], POOL, "none", 0, at + .5 + .08 * 3, op=.85))
    return out


def rosettes(x, y, w, h, at):
    """The fold-out of nine rosettes, three by three, joined by causeways."""
    out = []
    cs = [(x + w * (.2 + .3 * (j % 3)), y + h * (.2 + .3 * (j // 3))) for j in range(9)]
    for a, b in ((0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 3), (3, 6), (2, 5), (5, 8), (1, 4), (4, 7)):
        out.append(ln([cs[a], cs[b]], at + .1, INK, 2.5, dur=.4))
    rr = min(w, h) * .11
    for j, (cx, cy) in enumerate(cs):
        tj = at + .3 + .08 * j
        out.append(circ(cx, cy, rr, "#d9c9a0" if j != 4 else "#e8c35a", INK, 1.6, tj, "pop"))
        out += [circ(cx + rr * .62 * math.cos(2 * math.pi * q / 6), cy + rr * .62 * math.sin(2 * math.pi * q / 6), rr * .22, "#c5b38a", INK, 1, tj + .05) for q in range(6)]
    return out


def jar(x, by, h, at, c=AZUR, band=AU):
    k = h / 100.
    P = lambda a, b: (x + a * k, by + b * k)
    return [poly([P(-18, 0), P(-22, -20), P(-16, -70), P(-20, -86), P(20, -86), P(16, -70), P(22, -20), P(18, 0)], c, INK, 1.6, at, "rise", curve=True),
            rect(x - 22 * k, by - 98 * k, 44 * k, 12 * k, OCHRE, INK, 1.2, 3 * k, at + .1, fx="rise"),
            ln([P(-20, -50), P(20, -50)], at + .1, band, 3 * k, draw=False)]


def jars_page(x, y, w, h, at):
    out = []
    for j, (fx_, c) in enumerate(((.18, AZUR), (.48, VERD), (.78, OCHRE))):
        out += jar(x + fx_ * w, y + .62 * h, .44 * h, at + .15 * j, c, AU)
        out += vword(x + fx_ * w - 16 * w / 250, y + .7 * h, ["otol", "dain", "okal"][j], .55 * w / 250, at + .5 + .1 * j, INK, 1.2)
    for j, fx_ in enumerate((.12, .4, .68)):
        bx, byy = x + fx_ * w + 20, y + .86 * h
        out.append(poly([(bx - 12, byy - 6), (bx + 10, byy - 10), (bx + 22, byy), (bx + 6, byy + 8), (bx - 10, byy + 6)], ROOT, INK, 1.2, at + .7 + .1 * j, "pop", curve=True))
        out.append(poly([(bx + 30, byy - 4), (bx + 46, byy - 18), (bx + 56, byy - 4), (bx + 44, byy + 4)], LEAF, INK, 1.2, at + .75 + .1 * j, "pop", curve=True))
    return out


def recipes_page(x, y, w, h, at, n=6, seed=9):
    out = []
    ph = (h - 30) / n
    for j in range(n):
        py = y + 24 + j * ph
        out.append(star5(x + 18, py + 6, 6 * w / 250, at + .12 * j, OCHRE))
        out += vtext(x + 34, py + 12, w - 50, 2, .48 * w / 250, at + .12 * j + .05, lh=13 * w / 250, seed=seed + j, w=1.1, dt=.01, row_dt=.06)
    return out


def herbal_page(x, y, w, h, at, kind=0, rows=4, seed=3):
    out = vtext(x + 16, y + 26, w - 32, rows, .5 * w / 250, at, lh=14 * w / 250, seed=seed, w=1.2, dt=.01, row_dt=.08)
    out += plant(x + w / 2, y + h - 46, h * .56, at + .3, kind, step=.6)
    return out


# ================================================================== props
def grille_card(x, y, w, h, at, wins=((.12, .25), (.45, .55), (.78, .2)), c="#2a221c", ww=.16, wh=.22, style="known", op=None):
    """A card with three windows cut in it (Rugg's grille): the windows drawn lit."""
    out = [rect(x, y, w, h, c, "#c9b48e", 2, 6, at, fx="pop", style=style, op=op)]
    for fx_, fy_ in wins:
        out.append(rect(x + fx_ * w, y + fy_ * h, ww * w, wh * h, "rgba(242,201,142,.25)", GOLD, 2, 3, at + .1, style=style))
    return out


def die(x, y, s, n, at, c="#f2e8d6"):
    pts = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
           5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
    return [rect(x - s / 2, y - s / 2, s, s, c, "#ffffff", 1.4, s * .16, at, fx="pop")] + [dot(round(x + a * s * .26, 1), round(y + b * s * .26, 1), round(s * .08, 1), "#1a1511", round(at + .1, 2), None) for a, b in pts]


def card(x, y, w, h, t, at, c="#9a2a1a"):
    return [rect(x - w / 2, y - h / 2, w, h, "#f2e8d6", "#ffffff", 1.4, w * .1, at, fx="pop"), lab(x, y + h * .18, t, at + .1, c, h * .42, st="serif", halo=False)]


def quill(x, y, s, at, c=LILAC, style="claimed"):
    k = s / 100.
    return [poly([(x, y), (x + 60 * k, y - 110 * k), (x + 86 * k, y - 150 * k), (x + 70 * k, y - 96 * k), (x + 10 * k, y - 6 * k)], "rgba(201,193,238,.12)", c, 2.5, at, style=style),
            ln([(x, y), (x + 76 * k, y - 132 * k)], at, c, 1.6, style, draw=False)]


def book_closed(x, y, w, h, at, c="#5a3a26", fx="pop"):
    return [rect(x, y, w, h, c, "#c9a06a", 2, 6, at, fx=fx), rect(x + w * .08, y + h * .1, w * .84, h * .8, "none", "rgba(232,184,122,.5)", 1.4, 4, at),
            rect(x + w, y + 4, 8, h - 8, VEL_D, at=at)]


def open_book(cx, y, pw, ph, at, fx="pop"):
    """An open book seen from above: two pages and a dark cover rim; returns elements (pages at cx-pw..cx and cx..cx+pw)."""
    return [rect(cx - pw - 14, y - 10, 2 * pw + 28, ph + 24, "#4a3020", "#8a6a48", 2, 10, at, fx=fx),
            rect(cx - pw, y, pw, ph, VEL, VEL_E, 1, 4, at, fx=fx), rect(cx, y, pw, ph, VEL, VEL_E, 1, 4, at, fx=fx),
            ln([(cx, y), (cx, y + ph)], at, "rgba(90,60,30,.6)", 3, draw=False)]


def lamp_glow(x, y, r, at, op=.35):
    return glow(round(x, 1), round(y, 1), round(r), round(at, 2), op, "lamp")


# ================================================================== cold open
BK = (889, 150, 590, 590)          # the open book of the opening: spine x, top y, page width, page height


def s1():
    """A painted plant draws itself from the roots up on the left page; around it, ten lines of Voynichese write themselves."""
    cx, y0, pw, ph = BK
    lx = cx - pw
    els = [lamp_glow(620, 450, 760, -1, .3)] + open_book(cx, y0, pw, ph, -1, fx=None)
    r = random.Random(17)
    els += [oval(round(r.uniform(lx + 40, cx + pw - 40), 1), round(r.uniform(y0 + 40, y0 + ph - 40), 1), round(r.uniform(20, 60), 1), round(r.uniform(14, 40), 1),
                 "#b89a6a", at=-1, op=.12) for _ in range(7)]
    # the right page: a second plant and its text, already there (seen in full when the camera pulls back)
    els += static(vtext(cx + 34, y0 + 52, pw - 70, 4, 1.0, -1, lh=30, seed=21, w=1.9))
    els += static(plant(cx + pw / 2, y0 + ph - 70, 300, -1, kind=2))
    els += static(vtext(cx + 34, y0 + ph - 150, 150, 3, .9, -1, lh=28, seed=22, w=1.8) + vtext(cx + pw - 185, y0 + ph - 150, 150, 3, .9, -1, lh=28, seed=23, w=1.8))
    # the left page: the plant first, then the writing around it
    els += plant(lx + 295, y0 + 540, 360, .3, kind=0, step=.9)
    ta = T("s1", "Around it", lead=.1)
    els += vtext(lx + 22, y0 + 46, pw - 44, 3, 1.05, ta, lh=32, seed=11, w=2.1, dt=.05, row_dt=.3, first=["fachys", "ykal", "ar", "ataiin"])
    els += vtext(lx + 400, y0 + 280, pw - 420, 4, 1.0, ta + .9, lh=30, seed=12, w=2.0, dt=.05, row_dt=.3)
    els += vtext(lx + 20, y0 + 420, 165, 3, 1.0, ta + 1.9, lh=30, seed=13, w=2.0, dt=.05, row_dt=.3)
    return {"base": "dark", "cam": [1.3, 684, 450], "els": els}


def s2_add():
    """Pull back: the whole open book, and beside it a pile of 24 leaves (each ten pages) growing to 240 pages."""
    t = T("s2", "two hundred")
    out = []
    for j in range(24):
        y = 742 - 14 * (j + 1)
        out.append(rect(108, y, 160, 10, VEL, VEL_E, 1, 2, t + .05 * j, fx="pop"))
    out += [lab(188, 380, "240 pages", t + 1.2, GOLD, 32, st="serif"), glow(188, 600, 160, t + 1.0, .35)]
    return out


EARTH = (889, 2350, 1750)          # the curve of the Earth in the opening: centre and radius (its top at y 600)


def arc_y(x):
    cx, cy, r = EARTH
    return cy - math.sqrt(r * r - (x - cx) ** 2)


def crowd(at):
    """Figures of every height standing along the curve of the Earth on either side of the book; many with a question mark."""
    r = random.Random(7)
    out, qs, k = [], [], 0
    x = 150.0
    while x < 1640:
        if not (760 < x < 1018):
            y = arc_y(x)
            hh = r.uniform(62, 104)
            c = r.choice(["#e8d6b8", "#d8c4a4", "#c9b394", "#efe0c6", "#b9a07e"])
            t = round(at + .25 + .045 * k + (0 if x < 889 else .02), 2)
            out.append(person(round(x, 1), round(y + 2, 1), round(hh, 1), t, c))
            if r.random() < .55:
                qs.append((round(x + 3, 1), round(y - hh - 14, 1), round(t + 1.2, 2), r.choice([26, 30, 34])))
            k += 1
        x += r.uniform(38, 58)
    out += [lab(x_, y_, "?", t_, LILAC, s_, st="serif", halo=False) for x_, y_, t_, s_ in qs]
    return out


def s3():
    """The book on a lectern at the top of the curve of the Earth, under the stars; along the curve, people of every height rise,
    many with a question mark."""
    cx, cy, rr = EARTH
    earth = [(cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a))) for a in range(232, 309)]
    els = [glow(889, 620, 760, -1, .18, "blue"),
           poly(earth + [(1900, 1100), (-120, 1100)], "#1c2e33", "rgba(159,208,255,.55)", 3, -1),
           ln(earth, -1, "rgba(159,208,255,.25)", 12, draw=False),
           lamp_glow(889, 480, 420, .2, .45),
           rect(856, 520, 66, 82, "#3a281a", "#8a6a48", 2, 4, .2, fx="rise"),
           poly([(826, 522), (952, 522), (936, 500), (842, 500)], "#4a3020", "#8a6a48", 2, .2, fx="rise")]
    els += open_book(889, 440, 82, 58, .3)
    els += plant(889 - 41, 492, 52, .5, kind=0, step=.3) + vtext(897, 452, 70, 4, .42, .6, lh=11, seed=3, w=1.0, dt=.0, row_dt=.05)
    els += crowd(.0)
    return {"base": "dark", "stars": 220, "cam": CAM, "els": els}


def punch_card(x, y, s, at, c="#efe3c8"):
    k = s / 100.
    out = [poly([(x - 75 * k, y - 40 * k), (x + 60 * k, y - 40 * k), (x + 75 * k, y - 25 * k), (x + 75 * k, y + 40 * k), (x - 75 * k, y + 40 * k)], c, "#b9a77f", 1.5, at, "pop")]
    r = random.Random(3)
    for row in range(4):
        for col in range(12):
            if r.random() < .45:
                out.append(rect(x - 66 * k + col * 11 * k, y - 30 * k + row * 17 * k, 5 * k, 9 * k, "#3a2c20", at=at + .1))
    return out


def computer(x, y, s, at):
    k = s / 100.
    return [rect(x - 80 * k, y - 60 * k, 160 * k, 105 * k, "#2a2622", "#c9c1b3", 2, 8 * k, at, fx="pop"),
            rect(x - 68 * k, y - 50 * k, 136 * k, 82 * k, "#10201a", at=at + .05),
            poly([(x - 20 * k, y + 45 * k), (x + 20 * k, y + 45 * k), (x + 30 * k, y + 65 * k), (x - 30 * k, y + 65 * k)], "#2a2622", "#c9c1b3", 1.5, at, "pop")] + \
           [ln([(x - 58 * k, y - 36 * k + 14 * k * j), (x - 58 * k + (40 + 50 * ((j * 7) % 3)) * k, y - 36 * k + 14 * k * j)], at + .2 + .08 * j, "#8fd9b0", 2.5, dur=.3) for j in range(5)]


def papers(x, y, s, at, c=LILAC):
    k = s / 100.
    return [rect(x - 70 * k + 14 * k * j, y - 50 * k - 10 * k * j, 120 * k, 90 * k, "rgba(201,193,238,.08)", c, 2.5, 4, at + .1 * j, style="claimed") for j in range(3)]


def s4_add():
    """Three things that tried and failed, popping as they are named; then a large question mark over the book."""
    t1, t2, t3 = T("s4", "codebreakers"), T("s4", "computers"), T("s4", "claimed solutions")
    out = punch_card(470, 200, 110, t1) + [lab(470, 285, "codebreakers", t1 + .2, MUTED, 26)]
    out += computer(889, 195, 110, t2) + [lab(889, 285, "computers", t2 + .2, MUTED, 26)]
    out += papers(1308, 212, 110, t3) + [lab(1308, 285, "claimed solutions", t3 + .3, LILAC, 26), strike(1220, 250, 1400, 130, round(t3 + .7, 2))]
    out += qmark(889, 425, T("s4", "Is there"), 120, GOLD)
    return out


# ================================================================== chapter 1: a letter inside the book
def s6():
    """A shelf of old manuscripts; one glows and comes forward as an open book; a folded letter rises out of it."""
    r = random.Random(21)
    els = [lamp_glow(889, 420, 760, -1, .22), rect(130, 520, 1520, 20, WOOD, "#8a6a48", 1.5, 3, .1), rect(130, 540, 1520, 30, "rgba(0,0,0,.35)", at=.1)]
    x, k, pick = 160, 0, None
    while x < 1600:
        w = r.uniform(40, 60)
        h = r.uniform(210, 290)
        c = r.choice(["#5a3a26", "#6b4a30", "#4a3020", "#7a5236", "#5f4030", "#3f2a1c"])
        els.append(rect(x, 520 - h, w, h, c, "#2a1c12", 1.5, 3, round(.2 + .035 * k, 2), fx="rise"))
        els.append(ln([(x + 6, 520 - h * .8), (x + w - 6, 520 - h * .8)], round(.25 + .035 * k, 2), "rgba(232,184,122,.45)", 2, draw=False))
        if pick is None and x > 860:
            pick = (x, w, h)
        x += w + r.uniform(2, 6); k += 1
    px, pw_, ph_ = pick
    t1 = T("s6", "One of them")
    els += [rect(px - 4, 516 - ph_, pw_ + 8, ph_ + 8, "none", GOLD, 3, 4, t1 + .2, fx="draw"), glow(px + pw_ / 2, 520 - ph_ / 2, 140, t1 + .2, .7)]
    els += open_book(700, 600, 150, 150, t1 + .9, fx="rise")
    els += plant(625, 735, 120, t1 + 1.2, kind=1, step=.4) + vtext(712, 630, 125, 6, .55, t1 + 1.3, lh=18, seed=8, w=1.2, dt=.0, row_dt=.05)
    ta = T("s6", "a letter")
    els += [poly([(985, 600), (1245, 590), (1252, 760), (990, 768)], "#efe3c8", "#fff6e6", 1.5, ta, "rise"),
            ln([(988, 680), (1248, 672)], ta + .1, "rgba(120,90,60,.5)", 1.5, draw=False),
            {"k": "glyphs", "x": 1010, "y": 612, "w": 210, "h": 140, "rows": 8, "cols": 7, "kind": "latin", "c": "#6a4a30", "sw": 3, "op": .75, "in": round(ta + .3, 2)},
            ln([(890, 650), (960, 660), (982, 668)], ta, GOLD, 2.5, "inferred", dur=.5),
            lab(1275, 690, "Prague, c. 1665", T("s6", "Prague"), GOLD, 30, "start"),
            lab(889, 190, "Jesuits, near Rome, 1912", .6, MUTED, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


V7 = View(-2, 30, 39.5, 52.5, rect=(90, 130, 1600, 640))


def s7():
    """Map: the book's journey from Marci in Prague over the Alps to Kircher in Rome."""
    v = V7
    px, py = v.p(14.42, 50.08)
    rx, ry = v.p(12.5, 41.9)
    tp, tk = T("s7", "Marci"), T("s7", "Kircher")
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(10.0, 48.6), "the Alps", .5, "#9fb6c8", 24, st="ital"),
           {"k": "pin", "x": px, "y": py, "t": "Prague", "c": GOLD, "in": tp}, lab(px + 18, py + 40, "Marci", tp + .2, MUTED, 26, "start"),
           ln([(px, py), v.p(14.8, 47.6), v.p(13.6, 44.6), (rx, ry)], T("s7", "sending"), GOLD, 3, "inferred", dur=2.2, curve=True),
           {"k": "pin", "x": rx, "y": ry, "t": "Rome", "c": GOLD, "in": tk}, lab(rx + 18, ry + 40, "Kircher", tk + .2, MUTED, 26, "start"),
           rect(rx + 30, ry - 66, 34, 44, "#5a3a26", "#c9a06a", 1.5, 3, T("s7", "in Rome"), fx="pop"),
           glow(rx, ry, 120, T("s7", "sure that"), .7),
           {"k": "scale", "x": 140, "y": 760, "w": round(v.km(300), 1), "t": "300 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


def gold_bar(x, y, w, at):
    h, d = w * .32, w * .3
    return [poly([(x, y), (x + w, y), (x + w + d * .5, y - d * .4), (x + d * .5, y - d * .4)], "#ffe08a", "#fff1c0", 1.2, at, "pop"),
            rect(x, y, w, h, AU, "#fff1c0", 1.2, 2, at, fx="pop"), poly([(x + w, y), (x + w + d * .5, y - d * .4), (x + w + d * .5, y + h - d * .4), (x + w, y + h)], "#b8922e", at=at, fx="pop")]


def s8():
    """The emperor, the book, 600 gold ducats in a block, about 2 kg of gold; then the dotted chain of tellers: second-hand."""
    te, t6, tg, tc = T("s8", "Emperor"), T("s8", "six hundred"), T("s8", "two kilos"), T("s8", "Second hand")
    els = [lamp_glow(889, 460, 700, -1, .18),
           person(250, 650, 240, te), crown(252, 650 - 240 * .99 + 6, 24, te + .2), lab(250, 700, "Rudolf II", te + .3, GOLD, 28),
           ]
    els += book_closed(470, 330, 120, 160, .3)
    for row in range(20):
        for col in range(30):
            els.append(circ(722 + col * 13, 300 + row * 13, 5.2, AU, "#fff1c0", .8, round(t6 + .07 * row, 2)))
    els += [glow(917, 430, 260, t6 + 1.4, .4), lab(917, 600, "600 ducats", t6 + .6, GOLD, 32),
            arrow([[712, 420], [660, 420], [600, 410]], t6 + 1.0, GOLD, 3, dur=.6, curve=False)]
    els += gold_bar(1230, 470, 120, tg) + gold_bar(1300, 520, 120, tg + .25) + [lab(1365, 610, "about 2 kg of gold", tg + .4, AU, 30)]
    # the chain of tellers (dotted: a claim passed on, not a record)
    chain = [(268, 380), (430, 700), (560, 712), (690, 700), (790, 660)]
    els += [ln(chain, tc, LILAC, 3, "claimed", dur=1.2, curve=True)]
    for j, (x, y) in enumerate(chain[1:4]):
        p = person(x, y + 70, 74, round(tc + .3 + .2 * j, 2), LILAC)
        p.update(op=.75, keepop=True)
        els.append(p)
    els += [poly([(780, 640), (840, 636), (842, 690), (782, 694)], "#efe3c8", "#fff6e6", 1.2, tc + 1.0, "pop"),
            lab(560, 600, "second-hand", tc + 1.1, LILAC, 30, st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


def s9():
    """The first page under an ultraviolet lamp: at its foot, a faded name glows into view."""
    tu, tn = T("s9", "ultraviolet"), T("s9", "faded name")
    els = page(560, 140, 660, 650, .2)
    els += vtext(600, 200, 580, 13, 1.15, .3, lh=36, seed=31, w=2.0, dt=.0, row_dt=.04, op=.6)
    els += [poly([(1500, 170), (1590, 170), (1570, 240), (1520, 240)], "#3a3150", "#b8a8ff", 2, tu, "pop"),
            ln([(1545, 120), (1545, 170)], tu, "#8a7a9a", 3, draw=False),
            poly([(1522, 240), (1568, 240), (1230, 800), (640, 800)], "rgba(150,110,255,.14)", at=tu + .3, fx="fade"),
            glow(1545, 250, 90, tu + .1, .8, "blue"), glow(860, 745, 260, tu + .8, .5, "blue"),
            lab(860, 752, "Jacobj à Tepenecz", tn, "#e6dcff", 30, st="ital"),
            lab(1250, 700, "the emperor's distiller", T("s9", "distiller"), BONE, 28, "start"),
            ln([(1060, 742), (1240, 704)], T("s9", "distiller"), MUTED, 1.6, dur=.4)]
    return {"base": "dark", "cam": CAM, "els": els}


TL0, TL1, TLX0, TLX1 = 1350, 2050, 170, 1610


def XT(yr):
    return round(TLX0 + (yr - TL0) / (TL1 - TL0) * (TLX1 - TLX0), 1)


def s10():
    """The book's known life on a timeline: the 1639 letter, then Prague, Rome, Voynich, Yale."""
    ta = T("s10", "sixteen thirty nine")
    els = [axis(TLX0, TLX1, 600, [(XT(y), str(y)) for y in (1400, 1500, 1600, 1700, 1800, 1900, 2000)], .3)]
    els += [poly([(XT(1639) - 26, 400), (XT(1639) + 26, 396), (XT(1639) + 28, 436), (XT(1639) - 24, 440)], "#efe3c8", "#fff6e6", 1.2, ta, "pop"),
            ln([(XT(1639), 444), (XT(1639), 590)], ta + .2, MUTED, 1.6, "inferred", dur=.4),
            lab(XT(1639), 372, "1639 letter to Kircher", ta + .3, BONE, 26)]
    for (y0, y1, name, ly, c, phrase) in ((1600, 1665, "Prague", 540, AMBER, "Prague then"), (1665, 1912, "Rome", 540, AMBER, "then Rome"),
                                          (1912, 1969, "Voynich", 500, AMBER, "then Voynich"), (1969, 2026, "Yale, MS 408", 540, GOLD, "Since")):
        t = T("s10", phrase)
        els += [{"k": "band", "x0": XT(y0), "x1": XT(y1), "y": 556, "h": 16, "c": c, "in": round(t, 2), "dur": .6},
                lab((XT(y0) + XT(y1)) / 2, ly, name, t + .2, c, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s11_add():
    """The doubt, drawn as a claim: 'forged by Voynich?' over 1912."""
    t = T("s11", "suspected")
    return quill(XT(1912) - 20, 470, 90, t) + [lab(XT(1912), 320, "forged by Voynich?", T("s11", "forging"), LILAC, 30, st="ital"),
                                               ln([(XT(1912), 340), (XT(1912), 480)], T("s11", "forging"), LILAC, 2, "claimed", dur=.4)]


def s14_add():
    """The radiocarbon answer: four samples drop onto a gold band 1404 to 1438; the forgery claim is struck."""
    t = T("s14", "Between")
    out = []
    for j in range(4):
        x = XT(1404) + 12 + j * 14
        out += [dot(x, 230, 7, BLUE, round(t + .1 * j, 2)), ln([(x, 240), (x, 548)], t + .2 + .1 * j, BLUE, 1.6, "inferred", dur=.5)]
    out += [{"k": "band", "x0": XT(1404), "x1": XT(1438), "y": 552, "h": 22, "c": GOLD, "in": round(t + .7, 2), "fx": "pop"},
            glow((XT(1404) + XT(1438)) / 2, 560, 120, t + .8, .7),
            lab((XT(1404) + XT(1438)) / 2 + 10, 500, "1404 to 1438", t + .9, GOLD, 30),
            lab((XT(1404) + XT(1438)) / 2 + 10, 200, "radiocarbon", t + .3, BLUE, 26),
            strike(XT(1912) - 140, 330, XT(1912) + 140, 296, T("s14", "Not a modern fake"))]
    return out


def s12():
    """Four page edges, a scalpel, four slivers each 1 by 6 mm, lifted onto a tray beside a grain of rice (20 units a millimetre)."""
    tc, ts, tr = T("s12", "cut four"), T("s12", "edges"), T("s12", "grain of rice")
    els = []
    for j in range(4):
        y = 170 + 140 * j
        xr = 640 - 34 * j
        els += [rect(-40, y + 10, xr + 40, 150, "rgba(0,0,0,.3)", r=4, at=-1), rect(-40, y, xr + 40, 150, VEL, VEL_E, 1.2, 4, -1)]
        els += [{"k": "glyphs", "x": 40, "y": y + 30, "w": xr - 120, "h": 90, "rows": 3, "cols": 8, "c": INK, "sw": 1.6, "op": .3, "in": -1}]
        els += [rect(xr - 20, y + 15, 20, 120, "#17120e", at=tc + .25 + .15 * j, fx="pop"), ln([(xr - 20, y + 15), (xr - 20, y + 135)], tc + .1 + .15 * j, RED, 1.6, dur=.2)]
    els += [poly([(700, 150), (780, 120), (800, 132), (712, 176)], "#cfd6dc", "#ffffff", 1.2, tc - .2, "pop"),
            rect(780, 112, 70, 22, "#6b4a30", r=4, at=tc - .2, fx="pop"), lab(760, 230, "Arizona, 2009", T("s12", "University of Arizona"), BLUE, 26)]
    els += [rect(930, 300, 640, 360, "#121516", "#5a6a70", 2, 14, ts - .2), lab(1250, 280, "four slivers", ts + .4, BONE, 28)]
    for j in range(4):
        els.append(rect(990, 360 + 46 * j, 120, 20, VEL, VEL_E, 1, 3, ts + .2 + .15 * j, fx="pop"))
    els += [{"k": "dim", "x1": 990, "y1": 340, "x2": 1110, "y2": 340, "t": "6 mm", "c": GOLD, "dur": .5, "in": round(ts + .9, 2)},
            oval(1350, 420, 66, 25, "#f4efe2", "#ffffff", 1.2, at=tr, fx="pop"), lab(1350, 500, "a grain of rice", tr + .2, BONE, 28),
            lab(1250, 620, "same scale", tr + .5, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


CALF = [(-140, -150), (-118, -166), (-40, -160), (60, -164), (100, -172), (128, -204), (136, -222), (150, -210), (166, -200), (188, -162), (176, -146),
        (144, -150), (116, -118), (112, 0), (98, 0), (94, -84), (70, -86), (66, 0), (52, 0), (48, -90), (-78, -92), (-84, 0), (-98, 0), (-104, -88),
        (-118, -92), (-126, 0), (-140, 0), (-146, -110)]


def candle(x, base, h, at, w=56):
    return [rect(x - w / 2, base - h, w, h, "#efe6d2", "#fff6e6", 1.2, 5, at, fx="fill", dur=.5),
            ln([(x, base - h), (x, base - h - 14)], at + .3, "#3a2c20", 3, draw=False),
            poly([(x, base - h - 44), (x + 10, base - h - 22), (x, base - h - 12), (x - 10, base - h - 22)], "#ffd27a", at=at + .35, curve=True, fx="pop"),
            glow(x, base - h - 26, 60, at + .35, .9)]


def s13():
    """The carbon clock: a calf with its carbon, then candles burning down in step with the carbon that fades; a ruler on what is left."""
    tl, tf, tm, tk = T("s13", "radioactive carbon"), T("s13", "fades after death"), T("s13", "measure"), T("s13", "you know")
    els = [poly([(250 + a, 690 + b) for a, b in CALF], "#c9a77f", "#efe0c6", 1.5, .3, "pop"), ln([(110, 540), (92, 600), (96, 630)], .3, "#c9a77f", 4, draw=False, curve=True),
           circ(408, 498, 4, "#3a2c20", at=.4)]
    r = random.Random(4)
    for j in range(16):
        els.append(dot(round(r.uniform(150, 340), 1), round(r.uniform(560, 590), 1), 6, BLUE, round(tl + .05 * j, 2)))
    els += [lab(250, 735, "a living calf", .5, MUTED, 26)]
    base = 690
    for j, (x, h, n) in enumerate(((600, 340, 16), (840, 240, 8), (1080, 150, 4), (1320, 70, 2))):
        t = tf + .7 * j
        els += candle(x, base, h, t)
        for q in range(n):
            els.append(dot(round(x - 24 + (q % 4) * 16, 1), round(base - h - 80 - (q // 4) * 16, 1), 5, BLUE, round(t + .3 + .02 * q, 2)))
    els += [arrow([[560, 740], [1400, 740]], tf + .5, AMBER, 3, dur=2.4, curve=False), lab(980, 780, "time since death", tf + 1.2, AMBER, 26)]
    els += [{"k": "dim", "x1": 1400, "y1": base, "x2": 1400, "y2": base - 70, "t": "", "c": GOLD, "dur": .5, "in": round(tm, 2)},
            lab(1430, 600, "what's left", tm + .2, GOLD, 28, "start"), lab(1430, 640, "tells the date", tk, GOLD, 28, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def bowl(x, y, w, c, at):
    return [poly(E(x, y, w / 2, w * .16, 24), c, "#fff6e6", 1.2, at, "pop"),
            poly([(x - w / 2, y), (x + w / 2, y), (x + w * .36, y + w * .32), (x - w * .36, y + w * .32)], "#8a7a66", "#cbb79a", 1.2, at, "pop")]


def s15():
    """The skin is dated, the ink is not; three pots of period pigments."""
    ts, ti, tp = T("s15", "skin"), T("s15", "not the ink"), T("s15", "paints")
    els = [poly([(170, 230), (420, 196), (630, 236), (650, 420), (560, 486), (330, 500), (190, 440)], VEL, VEL_E, 1.5, ts - .2, "pop", curve=True),
           {"k": "band", "x0": 300, "x1": 520, "y": 340, "h": 18, "c": GOLD, "in": round(ts + .2, 2), "dur": .5},
           lab(410, 325, "1404 to 1438", ts + .3, "#6a4a20", 26, halo=False), tick(600, 250, ts + .4),
           lab(410, 550, "the skin: dated", ts + .3, BONE, 30)]
    els += [poly([(1150, 470), (1140, 380), (1180, 330), (1300, 330), (1340, 380), (1330, 470)], "rgba(26,21,17,.6)", BLUE, 2.5, ti, "pop", style="inferred"),
            rect(1200, 300, 80, 34, "rgba(26,21,17,.6)", BLUE, 2.5, 6, ti, style="inferred")] + quill(1290, 330, 90, ti + .2, MUTED, "known") + \
           qmark(1390, 300, ti + .4, 70, LILAC, halo=False) + [lab(1240, 550, "the ink: not dated", ti + .3, BONE, 30)]
    for j, (x, c, name) in enumerate(((600, AZUR, "azurite blue"), (889, OCHRE, "red ochre"), (1178, VERD, "copper green"))):
        t = tp + .4 * j
        els += bowl(x, 670, 130, c, t) + [lab(x, 750, name, t + .1, MUTED, 24), tick(x + 90, 660, t + .3, s=.8)]
    els += [lab(889, 625, "pigments of the period", tp + 1.4, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


PX = [89 + 269 * j for j in range(6)]
PY, PW, PH = 230, 255, 360
GROUP = {0: GREEN, 1: BLUE, 2: AMBER, 3: BLUE, 4: GREEN, 5: AMBER}


def s16():
    """Six blank pages in a row; the first two fill as they are named: plants, then stars and the zodiac."""
    els = [lamp_glow(889, 420, 900, -1, .16)]
    for x in PX:
        els += page(x, PY, PW, PH, -1)
    tp, tz = T("s16", "Plants"), T("s16", "Circles of stars")
    els += herbal_page(PX[0], PY, PW, PH, tp) + [lab(PX[0] + PW / 2, 630, "plants", tp + .2, BONE, 26),
                                                 lab(PX[0] + PW / 2, 662, "about half the book", T("s16", "about half"), MUTED, 24)]
    els += vtext(PX[1] + 18, PY + 30, PW - 36, 2, .5, tz, lh=14, seed=5, w=1.2, dt=.01, row_dt=.08)
    els += zodiac(PX[1] + PW / 2, PY + 200, 108, tz + .2) + [lab(PX[1] + PW / 2, 630, "stars", tz + .2, BONE, 26)]
    return {"base": "dark", "cam": [2.0, 444, 430], "els": els}


def s17_add():
    tb, tr = T("s17", "Small bathing"), T("s17", "fold out")
    return pools(PX[2] + 8, PY + 40, PW - 16, PH - 60, tb) + [lab(PX[2] + PW / 2, 630, "pools", tb + .3, BONE, 26)] + \
        rosettes(PX[3] + 6, PY + 40, PW - 12, PH - 70, tr) + [lab(PX[3] + PW / 2, 630, "rosettes", tr + .3, BONE, 26)]


def s18_add():
    tj, tr = T("s18", "Jars"), T("s18", "And pages")
    return jars_page(PX[4] + 5, PY + 20, PW - 10, PH - 30, tj) + [lab(PX[4] + PW / 2, 630, "jars", tj + .3, BONE, 26)] + \
        recipes_page(PX[5], PY, PW, PH, tr) + [lab(PX[5] + PW / 2, 630, "recipes", tr + .3, BONE, 26)]


def s19_add():
    """Herbs, heavens, healing: a coloured rule under each page and three words; then the little labels glow, unread."""
    out = []
    words_ = (("herbs", GREEN, 560, "herbs"), ("heavens", BLUE, 889, "heavens"), ("healing", AMBER, 1218, "healing"))
    for name, c, x, ph in words_:
        t = T("s19", ph)
        out += [rect(PX[j] + 20, 600, PW - 40, 6, c, r=3, at=t, fx="draw") for j in GROUP if GROUP[j] == c]
        out += [dot(x - 70, 744, 8, c, t), lab(x - 56, 753, name, t + .1, c, 30, "start")]
    tl = T("s19", "the labels")
    spots = [(PX[4] + 5 + .18 * (PW - 10), PY + 20 + .7 * (PH - 30) - 4), (PX[4] + 5 + .48 * (PW - 10), PY + 20 + .7 * (PH - 30) - 4),
             (PX[4] + 5 + .78 * (PW - 10), PY + 20 + .7 * (PH - 30) - 4), (PX[1] + PW / 2, PY + 200), (PX[3] + PW * .5, PY + 40 + .5 * (PH - 70))]
    for j, (x, y) in enumerate(spots):
        out += [ring(round(x, 1), round(y, 1), 22, round(tl + .12 * j, 2), GOLD, 2.5, dur=.4)]
    out += [lab(PX[2] + PW / 2, 210, "?", tl + .3, LILAC, 54, st="serif"), lab(PX[4] + PW / 2, 210, "?", tl + .5, LILAC, 54, st="serif"),
            lab(PX[0] + PW / 2, 210, "?", tl + .7, LILAC, 54, st="serif")]
    return out


# ================================================================== chapter 2: counting the unreadable
def s20():
    """380 word tiles (each 100 words) pop in, row by row: about 38,000 words; then 80 turn gold: about 8,000 different ones."""
    tc, tw, td = T("s20", "You count"), T("s20", "thirty eight thousand"), T("s20", "eight thousand different")
    els = []
    for row in range(19):
        for col in range(20):
            els.append(rect(140 + 46 * col, 200 + 24 * row, 40, 16, "#b9ab94", "#8a7a66", 1, 6, round(tc + .1 * row, 2), op=.7))
    r = random.Random(12)
    cells = r.sample(range(380), 80)
    for j, c in enumerate(sorted(cells, key=lambda q: (q % 20) + (q // 20) * .3)):
        els.append(rect(140 + 46 * (c % 20), 200 + 24 * (c // 20), 40, 16, AU, "#fff1c0", 1, 6, round(td + .012 * j, 2), fx="pop"))
    els += [lab(1110, 330, "about 38,000 words", tw, BONE, 34, "start"), lab(1110, 372, "each tile: 100 words", tw + .4, MUTED, 24, "start"),
            lab(1110, 520, "about 8,000 different", td + .4, AU, 34, "start"), glow(600, 430, 600, tc, .15)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": shift(els, 40)}


def stair(x0, base, hmax, at, n=10, pitch=62, wd=40, c=GREEN, step=.12, ats=None, op=.9, style="known", curve_at=None, edge="none"):
    out = []
    for k in range(n):
        h = hmax / (k + 1)
        t = ats[k] if ats and k < len(ats) else at + step * k
        out.append(vbar(x0 + pitch * k, base, h, wd, c, t, op=op, style=style, edge=edge))
    if curve_at is not None:
        pts = [(x0 + pitch * k, base - hmax / (k + 1) - 14) for k in range(n)]
        out.append(ln(pts, curve_at, GOLD, 2.5, "inferred", dur=1.0, curve=True))
    return out


def s21():
    """Two word staircases, English and this book: each bar 1/rank of the first (Zipf's law, schematic)."""
    t1, t2, t3, t4, t5, tb = (T("s21", p) for p in ("most common", "the second", "the third", "and so on", "smooth staircase", "This book"))
    els = [ln([(140, 640), (820, 640)], .3, MUTED, 2, draw=False), ln([(960, 640), (1640, 640)], .3, MUTED, 2, draw=False),
           lab(480, 735, "English", .5, BONE, 32), lab(1300, 735, "this book", tb, GOLD, 32)]
    els += stair(190, 640, 380, t4, ats=[t1, t2, t3] + [round(t4 + .12 * k, 2) for k in range(7)], c="#cbbca8", curve_at=t5)
    els += [lab(190 + 62 * k, 676, w, [t1, t2, t3][k] + .1, MUTED, 24) for k, w in enumerate(("the", "of", "and"))]
    els += [lab(190 + 62 * k, 260 + 380 * (1 - 1 / (k + 1)) - 26, ("1st", "2nd", "3rd")[k], [t1, t2, t3][k] + .2, BONE, 24) for k in range(3)]
    els += stair(1010, 640, 380, tb + .2, step=.12, c=GOLD, op=.85, curve_at=tb + 1.5)
    for k, w in enumerate(("daiin", "ol", "chedy")):
        els += vword(1010 + 62 * k - vwidth(w, 1.3) / 2, 686 + 14 * (k % 2), w, 1.3, tb + .4 + .12 * k, BONE, 2.0)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def minipages(x0, y0, n, cols, pw, ph, gap, at, step=.03, c=VEL, op=.85):
    return [rect(x0 + (pw + gap) * (j % cols), y0 + (ph + gap) * (j // cols), pw, ph, c, VEL_E, 1, 3, round(at + step * j, 2), op=op) for j in range(n)]


def s22():
    """Right: the book as sixteen small pages, two words clustering in their own sections. Left: a cookbook where oven and flour crowd the baking pages."""
    tc, tw, to, t13, tl, tg = (T("s22", p) for p in ("crowd into one section", "the way oven", "oven and flour", "twenty thirteen", "just like real", "genuine message"))
    els = [lab(1310, 175, "this book", .4, GOLD, 30)] + minipages(980, 230, 16, 8, 64, 92, 14, .5)
    secs = [(0, 8, "plants"), (8, 10, "stars"), (10, 14, "pools"), (14, 16, "recipes")]
    for a, b, name in secs:
        x0, x1 = 980 + 78 * (a % 8), 980 + 78 * ((b - 1) % 8) + 64
        y = 214 if a // 8 == 0 else 230 + 106 + 92 + 30
        els += [lab((x0 + x1) / 2, y, name, .9, MUTED, 24)]
    r = random.Random(5)
    for j in range(40):
        pg_ = r.choice([10, 11, 12, 13]) if j < 30 else r.randrange(16)
        x = 980 + 78 * (pg_ % 8) + r.uniform(10, 54); y = 230 + 106 * (pg_ // 8) + r.uniform(12, 80)
        els.append(dot(round(x, 1), round(y, 1), 5.5, AU, round(tc + .02 * j, 2)))
    for j in range(36):
        pg_ = r.choice([2, 3, 4, 5]) if j < 27 else r.randrange(16)
        x = 980 + 78 * (pg_ % 8) + r.uniform(10, 54); y = 230 + 106 * (pg_ // 8) + r.uniform(12, 80)
        els.append(dot(round(x, 1), round(y, 1), 5.5, BLUE, round(tc + .5 + .02 * j, 2)))
    els += [lab(480, 175, "a cookbook", tw, BONE, 30)] + minipages(140, 230, 12, 6, 92, 120, 22, tw)
    for j in range(34):
        pg_ = r.choice([7, 8, 9, 10]) if j < 26 else r.randrange(12)
        x = 140 + 114 * (pg_ % 6) + r.uniform(12, 80); y = 230 + 142 * (pg_ // 6) + r.uniform(14, 106)
        els.append(dot(round(x, 1), round(y, 1), 6, AMBER if j % 2 else "#f4efe2", round(to + .02 * j, 2)))
    els += [dot(300, 560, 8, AMBER, to), lab(318, 569, "oven", to + .1, AMBER, 26, "start"), dot(480, 560, 8, "#f4efe2", to + .3), lab(498, 569, "flour", to + .4, "#f4efe2", 26, "start")]
    els += [lab(1310, 520, "Montemurro and Zanette, 2013", t13, MUTED, 24), lab(1310, 572, "clustered like real languages", tl, GREEN, 28)]
    els += tag(1310, 650, "a genuine message?", tg, GREEN, 26, "inferred")
    return {"base": "dark", "cam": CAM, "els": els}


STRIP_N, STRIP_X0, STRIP_P, STRIP_W, STRIP_Y, STRIP_H = 48, 121, 32, 26, 300, 60


def dialect(j):
    if j < 18:
        return "A"
    if j < 24:
        return "B"
    if j < 29:
        return None
    if j < 36:
        return "B"
    if j < 37:
        return None
    if j < 42:
        return "A"
    return "B"


def s23():
    """A strip of 48 page tiles: they turn amber (dialect A) or blue (B); each dialect's favourite words pop above it."""
    td, ta, tb, tf = T("s23", "two dialects"), T("s23", "A and"), T("s23", "and B"), T("s23", "favourite words")
    els = [lab(889, 400, "Currier, 1976", .5, MUTED, 26)]
    for j in range(STRIP_N):
        x = STRIP_X0 + STRIP_P * j
        els.append(rect(x, STRIP_Y, STRIP_W, STRIP_H, VEL, VEL_E, 1, 3, round(.3 + .01 * j, 2), op=.85))
        d = dialect(j)
        if d:
            els.append(rect(x, STRIP_Y, STRIP_W, STRIP_H, CA if d == "A" else CB, "#fff6e6", 1, 3, round(td + .02 * j, 2), fx="pop"))
    els += chip(210, 190, "A", CA, ta, 32) + chip(1000, 190, "B", CB, tb, 32)
    for k, w in enumerate(("chol", "chor", "daiin")):
        els += vword(270 + 110 * k, 205, w, 2.0, tf + .15 * k, CA, 2.4)
    for k, w in enumerate(("chedy", "qokeedy", "shedy")):
        els += vword(1060 + 160 * k, 205, w, 2.0, tf + .3 + .15 * k, CB, 2.4)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def gallows(cx, by, s, j, at, c=BONE, w=4):
    """The gallows letter k as five scribes might write it: loop size, stem slant, crossbar curve and foot length vary."""
    loop = [1.0, 1.25, .85, 1.1, .95][j]
    slant = [0, 1.2, -.6, .4, 0][j]
    foot = [0, 3, 0, 1.5, 4][j]
    bend = [0, 0, 1.5, -1.0, .8][j]
    P = lambda x, y: (cx + (x + slant * (-y) / 16) * s, by + y * s)
    st1 = [P(2, .5), P(2.2, -16.5)]
    lp = [P(2.2, -15.5), P(2.2 + 3.6 * loop, -17 - bend), P(2.2 + 7.2 * loop, -15), P(2.2 + 6.6 * loop, -10.5), P(2.2 + 3 * loop, -9), P(2.4, -10.5)]
    st2 = [P(2.2 + 7.0 * loop, -14), P(2.2 + 7.4 * loop, .5), P(2.2 + 7.4 * loop + foot, .5 + foot * .2)]
    return [ln(st1, at, c, w, draw=False), ln(lp, at + .2, c, w, curve=True, draw=False), ln(st2, at + .4, c, w, curve=True, draw=False)]


def s24_add():
    """The same letter written five ways, one per scribe."""
    t = T("s24", "five scribes")
    out = [lab(889, 518, "Davis, 2020", T("s24", "Lisa Fagin Davis"), MUTED, 24)]
    for j in range(5):
        x = 450 + 220 * j
        out += gallows(x - 40, 722, 9.5, j, round(t - 1.4 + .3 * j, 2), BONE, 4.5)
        out += [lab(x, 765, "scribe %d" % (j + 1), round(t - 1.2 + .3 * j, 2), MUTED, 24)]
    out += [lab(889, 484, "five scribes", t, GOLD, 34)]
    return out


def s25_add():
    """Where the dialects live: A under the plant pages, B under the bathing pools."""
    ta, tb = T("s25", "Dialect A"), T("s25", "dialect B")
    xa = STRIP_X0 + STRIP_P * 9 + STRIP_W / 2
    xb = STRIP_X0 + STRIP_P * 32 + STRIP_W / 2
    out = plant(xa - 40, 286, 64, ta, kind=0, step=.25) + [lab(xa + 10, 268, "plant pages: A", ta + .3, CA, 26, "start")]
    out += [poly(E(xb - 40, 270, 34, 12, 18), POOL, INK, 1.2, tb, "pop"), circ(xb - 46, 258, 5, SKIN, INK, 1, tb + .1), circ(xb - 30, 260, 5, SKIN, INK, 1, tb + .1),
            lab(xb + 6, 278, "bathing pools: B", tb + .3, CB, 26, "start")]
    out += [rect(STRIP_X0 - 4, STRIP_Y - 4, STRIP_P * 18 - 2, STRIP_H + 8, "none", CA, 3, 4, ta + .2), rect(STRIP_X0 + STRIP_P * 29 - 4, STRIP_Y - 4, STRIP_P * 7 - 2, STRIP_H + 8, "none", CB, 3, 4, tb + .2)]
    return out


def s26():
    """Guess the next letter: after q, English bets on u; after t, many choices; in this book, one or two likely letters."""
    tg, tq, tu, tm, tb = (T("s26", p) for p in ("guess the next", "after a q", "bet on a u", "most letters", "In this book"))
    els = [lab(889, 160, "guess the next letter", tg, GOLD, 32)]

    def row(y, at, head, bars, lbls, glyph=False, who="English"):
        out = []
        if glyph:
            out += vword(240, y + 20, head, 6.0, at, BONE, 4.5)
        else:
            out.append(lab(270, y + 30, head, at, BONE, 90, st="serif"))
        out += [arrow([[350, y], [440, y]], at + .2, AMBER, 3, dur=.3, curve=False), ln([(470, y + 60), (1100, y + 60)], at + .2, MUTED, 1.5, draw=False)]
        for k, (h, l) in enumerate(zip(bars, lbls)):
            x = 500 + 70 * k
            out.append(vbar(x, y + 60, max(4, h), 40, GOLD if k == 0 and h > 80 else "#cbbca8", round(at + .4 + .08 * k, 2), op=.9))
            if glyph:
                out += vword(x - vwidth(l, 1.4) / 2, y + 96, l, 1.4, at + .4 + .08 * k, MUTED, 2)
            else:
                out.append(lab(x, y + 92, l, at + .4 + .08 * k, MUTED, 24))
        out.append(lab(1160, y + 40, who, at + .3, GOLD if glyph else BONE, 30, "start"))
        return out
    els += row(250, tq, "q", [120, 0, 0, 0, 0, 0, 0, 0], ["u", "a", "e", "i", "o", "r", "s", "t"])
    els += [ring(500, 240, 52, tu, GOLD, 3, dur=.4)]
    els += row(440, tm, "t", [110, 62, 46, 36, 30, 25, 20, 15], ["h", "o", "e", "i", "a", "r", "s", "u"])
    els += row(630, tb, "a", [118, 44, 30, 6, 4, 0, 0, 0], ["i", "r", "l", "n", "m", "s", "d", "o"], glyph=True, who="this book")
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s27():
    """Surprise per letter: European languages about 3 (3.0 to 3.4), this book about 2 (2.2); 294 languages, no match."""
    te, tb, ty, tn = T("s27", "European languages"), T("s27", "This book scores"), T("s27", "A Yale team"), T("s27", "matched none")
    Y = lambda b: 700 - 100 * b
    els = [ln([(230, 700), (230, 280)], .3, MUTED, 2, draw=False), ln([(230, 700), (880, 700)], .3, MUTED, 2, draw=False),
           lab(230, 250, "surprise per letter (bits)", .4, BONE, 26, "start")]
    els += [lab(212, Y(b) + 8, str(b), .4, MUTED, 24, "end") for b in range(5)] + [ln([(222, Y(b)), (238, Y(b))], .4, MUTED, 2, draw=False) for b in range(1, 5)]
    els += [vbar(450, 700, 301, 170, AMBER, te, op=.85), rect(365, Y(3.37), 170, 36, "rgba(232,184,122,.35)", AMBER, 1.5, 3, te + .4, style="inferred"),
            lab(450, Y(3.37) - 16, "3.0 to 3.4", te + .5, AMBER, 26), lab(450, 740, "European languages", te + .2, AMBER, 26)]
    els += [vbar(720, 700, 222, 170, GOLD, tb), glow(720, Y(2.2), 140, tb + .4, .6), lab(720, Y(2.22) - 18, "2.2", tb + .4, GOLD, 30), lab(720, 740, "this book", tb + .2, GOLD, 26)]
    els += [lab(1190, 268, "294 languages", ty + .2, BONE, 28)]
    for k in range(294):
        x, y = 960 + 22 * (k % 21), 300 + 22 * (k // 21)
        els.append(rect(x, y, 16, 16, "#8fa6b8", r=3, at=round(ty + .003 * k, 3), op=.85))
    els += [rect(1560, 440, 26, 26, GOLD, "#fff1c0", 1.5, 4, tn - .3, fx="pop"), glow(1573, 453, 70, tn - .3, .6),
            lab(1573, 420, "this book", tn - .2, GOLD, 24), lab(1573, 510, "no match", tn, RED, 28)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s28():
    """A line of Voynich script with the same word three times in a row, each copy ringed; beside it a record whose needle skips back."""
    tr, ts, tk = T("s28", "strange runs"), T("s28", "the same word"), T("s28", "stuck record")
    els = [rect(110, 250, 1030, 240, VEL, VEL_E, 1.2, 8, .2)]
    ws = ["chol", "qokedy", "qokedy", "qokedy", "dal", "shedy"]
    x, spots = 140, []
    for k, w in enumerate(ws):
        wd = vwidth(w, 2.6)
        els += vword(x, 400, w, 2.6, round(tr - .8 + .25 * k, 2), INK, 3.2)
        spots.append((x + wd / 2, wd))
        x += wd + 22
    for j, k in enumerate((1, 2, 3)):
        cx, wd = spots[k]
        els.append({"k": "poly", "p": E(round(cx, 1), 382, wd / 2 + 14, 52, 30), "fill": "rgba(232,184,122,.08)", "c": AMBER, "w": 3, "curve": True, "in": round(ts + .35 * j, 2), "fx": "pop"})
    els += [lab(spots[2][0], 560, "one word, three times", ts + 1.1, AMBER, 28)]
    rx, ry = 1400, 470
    els += [circ(rx, ry, 190, "#121010", "#3a3330", 2, tk - .3, "pop")] + [circ(rx, ry, r_, "none", "#2c2826", 1.5, tk - .2) for r_ in (170, 150, 130, 110, 90)]
    els += [circ(rx, ry, 52, OCHRE, "#f4b27a", 1.5, tk - .2, "pop"), circ(rx, ry, 6, "#121010", at=tk - .2),
            ln([(1630, 250), (1580, 300), (1500, 360)], tk, BONE, 7, dur=.4), rect(1480, 350, 34, 22, "#cbd2d8", r=3, at=tk + .3, fx="pop"),
            {"k": "arrow", "p": R([(1505, 395), (1530, 470), (1500, 530), (1450, 470), (1480, 405)]), "c": AMBER, "w": 3, "fx": "draw", "dur": .8, "in": round(tk + .5, 2), "curve": True},
            lab(rx, 720, "a stuck record", tk + .3, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": shift(els, 60)}


def s29():
    """Two cards: words that behave like a language (the staircase, ticked); letters like none we know (the lone short bar, a question mark)."""
    tw, tl = T("s29", "Word by word"), T("s29", "Letter by letter")
    els = [rect(260, 220, 540, 440, "rgba(18,13,10,.75)", GREEN, 2.5, 18, tw, fx="pop"), lab(530, 300, "words", tw + .2, BONE, 44, st="serif")]
    els += stair(350, 590, 220, tw + .4, n=7, pitch=50, wd=30, c=GREEN, step=.06, curve_at=tw + .9) + [tick(730, 290, tw + .9)]
    els += [lab(530, 710, "like a language", tw + 1.0, GREEN, 30)]
    els += [rect(978, 220, 540, 440, "rgba(18,13,10,.75)", LILAC, 2.5, 18, tl, fx="pop"), lab(1248, 300, "letters", tl + .2, BONE, 44, st="serif")]
    els += [vbar(1160, 590, 210, 90, AMBER, tl + .4, op=.85), vbar(1330, 590, 155, 90, GOLD, tl + .6)] + qmark(1450, 320, tl + .9, 80, LILAC, halo=False)
    els += [lab(1160, 625, "languages", tl + .5, MUTED, 24), lab(1330, 625, "this book", tl + .7, GOLD, 24), lab(1248, 710, "like none we know", tl + 1.0, LILAC, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": shift(els, 60)}


# ================================================================== chapter 3: a century of solutions
LENS = (760, 470, 190)


def s30():
    """One big letter of the script on vellum; a lens slides over it; inside the lens, tiny strokes (dotted: the claim)."""
    tn, tt, ts = T("s30", "William Newbold"), T("s30", "tiny strokes"), T("s30", "seen only")
    lx, ly, lr = LENS
    els = [rect(260, 150, 1040, 640, VEL, VEL_E, 1.5, 10, .2), lamp_glow(760, 470, 600, .2, .2)]
    els += vword(560, 650, "k", 21, .4, INK, 15, dur=1.2)
    els += vline(330, 230, ["daiin", "chol", "or"], 2.4, .6, INK, 3.2)[0] + vline(330, 730, ["shol", "dy"], 2.4, .7, INK, 3.2)[0]
    els += [lab(1000, 250, "Newbold, 1921", tn, BONE, 30, "start")]
    els += [circ(lx, ly, lr, "rgba(220,235,255,.10)", BONE, 8, tt - .4, "pop"), ln([(lx + lr * .72, ly + lr * .72), (lx + lr * 1.35, ly + lr * 1.35)], tt - .3, "#8a6a44", 18, dur=.3)]
    r = random.Random(8)
    pts = [(560 + px * 21, 650 + py * 21) for st_ in VG["k"][1] for px, py in st_]
    k = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for q in range(3):
            u = (q + .5) / 3
            x, y = ax + (bx - ax) * u + r.uniform(-4, 4), ay + (by - ay) * u + r.uniform(-4, 4)
            if math.hypot(x - lx, y - ly) < lr - 20:
                els.append(ln([(x - 6, y - 5), (x + 7, y + 4)], round(tt + .03 * k, 2), "#5a3aa0", 4.5, draw=False)); k += 1
    els += [lab(1000, 300, "hidden shorthand?", ts, LILAC, 32, "start", st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


def s32_add():
    """Closer: the strokes are cracks in the dried ink (solid); the claim is struck."""
    tm, tc = T("s32", "John Manly"), T("s32", "cracks")
    lx, ly, lr = LENS
    r = random.Random(3)
    out = [lab(1000, 640, "Manly, 1931", tm, BONE, 28, "start"), circ(lx, ly, lr - 5, VEL, at=tc - .5, dur=.5)] + vword(560, 650, "k", 21, tc - .4, INK, 15, fx=None, dur=.5) + \
        [circ(lx, ly, lr, "rgba(220,235,255,.10)", BONE, 8, tc - .4, dur=.5)]
    pts = [(560 + px * 21, 650 + py * 21) for st_ in VG["k"][1] for px, py in st_]
    k = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for q in range(4):
            u = (q + .5) / 4
            x, y = ax + (bx - ax) * u, ay + (by - ay) * u
            if math.hypot(x - lx, y - ly) < lr - 30:
                a = r.uniform(0, math.pi)
                p = [(x, y)]
                for _ in range(3):
                    a += r.uniform(-.7, .7)
                    x, y = x + 9 * math.cos(a), y + 9 * math.sin(a)
                    p.append((x, y))
                out.append(ln(p, tc + .02 * k, "#fff3dc", 2.4, dur=.3)); k += 1
    out += [strike(990, 312, 1290, 282, round(tc + .2, 2)), lab(1000, 690, "cracks in the ink", tc + .4, BONE, 32, "start")]
    return out


def microscope(x, by, s, at, c=LILAC, style="claimed"):
    k = s / 100.
    return [rect(x - 45 * k, by - 12 * k, 90 * k, 12 * k, "rgba(201,193,238,.08)", c, 2.5, 3, at, style=style),
            ln([(x + 22 * k, by - 12 * k), (x + 30 * k, by - 70 * k), (x + 16 * k, by - 128 * k)], at, c, 3, style, draw=False, curve=True),
            ln([(x - 34 * k, by - 62 * k), (x + 30 * k, by - 62 * k)], at, c, 3, style, draw=False),
            ln([(x - 22 * k, by - 176 * k), (x + 4 * k, by - 72 * k)], at, c, 12, style, draw=False),
            ln([(x - 30 * k, by - 196 * k), (x - 20 * k, by - 170 * k)], at, c, 7, style, draw=False)]


FRIAR = [(-.08, -.99), (.06, -1.0), (.14, -.9), (.13, -.78), (.21, -.62), (.25, -.3), (.31, 0), (-.31, 0), (-.25, -.3), (-.21, -.62), (-.14, -.8), (-.13, -.92)]


def s31():
    """All dotted (claimed): a hooded friar labelled Roger Bacon, a microscope, a telescope, and a spiral drawn in the sky: a galaxy?"""
    tb, tm, tt, tg, tc = (T("s31", p) for p in ("Roger Bacon", "microscope", "telescope", "spiral", "centuries before"))
    els = [poly([(400 + a * 300, 740 + b * 300) for a, b in FRIAR], "rgba(201,193,238,.10)", LILAC, 3, tb, "fade", style="claimed", curve=True),
           poly(E(402, 740 - .86 * 300, 26, 30, 16), "rgba(18,13,10,.6)", "none", 0, tb, "fade"),
           lab(400, 410, "Roger Bacon?", tb + .2, LILAC, 30, st="ital")]
    els += microscope(640, 740, 110, tm)
    els += [ln([(790, 740), (850, 640), (910, 740)], tt, LILAC, 3, "claimed", draw=False), ln([(820, 650), (1000, 520)], tt, LILAC, 14, "claimed", draw=False)]
    sp = [(1300 + 9 * t * math.cos(t), 330 + 6.2 * t * math.sin(t)) for t in [q * .25 for q in range(0, 66)]]
    els += [glow(1300, 330, 200, tg - .2, .35, "blue"), ln(sp, tg, LILAC, 3, "claimed", dur=1.6, curve=True), lab(1300, 520, "a galaxy?", tg + 1.0, LILAC, 30, st="ital"),
            lab(1300, 600, "centuries too early", tc, BONE, 30)]
    return {"base": "dark", "stars": 140, "cam": CAM, "els": els}


def tile(x, y, ch, at, s=90, c=VEL):
    return [rect(x - s / 2, y - s / 2, s, s, c, VEL_E, 1.5, 8, at, fx="pop"), lab(x, y + s * .22, ch, at + .05, INK, round(s * .6), st="serif", halo=False)]


def s33():
    """Four letter tiles, ROMA, re-formed row after row into other Latin words: same letters, any message."""
    rows = [("ROMA", .3), ("AMOR", T("s33", "shuffle letters")), ("MORA", T("s33", "Latin came")), ("ORAM", T("s33", "Shuffle freely")), ("RAMO", T("s33", "Shuffle freely") + .8)]
    els = []
    for k, (w, t) in enumerate(rows):
        y = 200 + 120 * k
        for j, ch in enumerate(w):
            els += tile(720 + 110 * j - 165, y, ch, round(t + .08 * j, 2), c=VEL if k == 0 else "#efe3c8")
        if k:
            els.append(arrow([[500, y - 120], [470, y - 60], [500, y]], t - .1, AMBER, 2.5, dur=.4))
    tl = T("s33", "almost anything")
    els += [lab(1080, 430, "same letters,", tl, AMBER, 34, "start"), lab(1080, 480, "any message", tl + .3, AMBER, 34, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def machine(x, y, w, h, at):
    d = w * .3
    return [rect(x, y, w, h, "#5a5248", "#c9c1b3", 2, 4, at, fx="rise"),
            poly([(x, y), (x + w, y), (x + w + d * .6, y - d * .4), (x + d * .6, y - d * .4)], "#7a7266", "#c9c1b3", 1.5, at, "rise"),
            poly([(x + w, y), (x + w + d * .6, y - d * .4), (x + w + d * .6, y + h - d * .4), (x + w, y + h)], "#3a342e", "#c9c1b3", 1.5, at, "rise"),
            rect(x + w * .15, y + h * .2, w * .7, 10, "#1a1511", at=at + .2), glow(x + w * .5, y + h * .2 + 5, 60, at + .4, .7)] + \
           [dot(round(x + w * .2 + 22 * j, 1), round(y + h * .5, 1), 6, "#ffcf6a" if j % 2 else "#8fd9b0", round(at + .5 + .1 * j, 2)) for j in range(5)]


def s34():
    """Wartime codebreakers at their desks; punched cards stack up beside a tabulating machine; the book stays locked."""
    tp, tf, tw, tc, tm, tn = (T("s34", p) for p in ("professionals", "nineteen forty four", "wartime cryptanalysts", "punched onto cards", "machines", "never cracked"))
    els = [lamp_glow(700, 520, 700, -1, .16), rect(120, 718, 1000, 8, "#5a4836", at=.2)]
    for j in range(5):
        x = 210 + 190 * j
        els += [rect(x + 40, 610, 120, 12, WOOD, "#8a6a48", 1, 2, round(tp + .1 * j, 2), fx="rise"), ln([(x + 60, 622), (x + 60, 718)], round(tp + .1 * j, 2), WOOD, 4, draw=False),
                ln([(x + 140, 622), (x + 140, 718)], round(tp + .1 * j, 2), WOOD, 4, draw=False)]
        els += seated(x, 718, 170, round(tw + .15 * j, 2))
        els += [rect(x + 70, 596, 50, 14, "#efe3c8", at=round(tc + .1 * j, 2), fx="pop")]
    els += [lab(600, 230, "Friedman's study group", tw - .3, BONE, 32), lab(600, 275, "from 1944", tf, MUTED, 28)]
    for j in range(22):
        els.append(rect(1180, 712 - 8 * j, 170, 6, "#efe3c8", "#b9a77f", .8, 1, round(tc + .05 * j, 2), fx="pop"))
    els += punch_card(1265, 450, 150, tc + .3)
    els += machine(1420, 520, 200, 190, tm)
    els += book_closed(1460, 210, 90, 120, tn - .5) + padlock(1505, 290, 70, tn, AMBER, "known", "rgba(232,184,122,.15)")
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """A journal page; its footnote types itself: the anagram. A sealed envelope, opened after his death; the solution types itself."""
    tf, tb, tu, ta = T("s35", "footnote"), T("s35", "It began"), T("s35", "Unscrambled"), T("s35", "an early attempt")
    els = [rect(160, 150, 720, 630, "#f3ead8", "#fff6e6", 1.5, 6, .3),
           {"k": "glyphs", "x": 210, "y": 200, "w": 620, "h": 340, "rows": 12, "cols": 8, "kind": "latin", "c": "#7a6a58", "sw": 4, "op": .6, "in": .4},
           lab(520, 182, "Philological Quarterly, 1959", .6, "#7a6a58", 24, halo=False),
           ln([(210, 585), (430, 585)], tf, "#7a6a58", 2, dur=.4), lab(196, 590, "*", tf, "#7a6a58", 28, halo=False)]
    for k, s in enumerate(("I put no trust in anagrammatic acrostic", "cyphers, for they are of little real value,", "a waste, and may prove nothing. Finis.")):
        els.append(lab(212, 628 + 38 * k, s, round(tb + 1.1 * k, 2), "#3a2a1c", 26, "start", st="body", halo=False, fx="type", dur=1.1))
    els += [rect(1000, 200, 580, 300, "#e9dcc0", "#fff6e6", 1.5, 6, tu, fx="pop"), ln([(1000, 200), (1290, 380), (1580, 200)], tu + .1, "#b9a77f", 2, dur=.5),
            circ(1290, 380, 32, "#9a2a1a", "#c94a3a", 2, tu + .3, "pop"), lab(1290, 545, "opened after his death", tu + .5, MUTED, 26)]
    for k, s in enumerate(("The Voynich MSS was an early attempt", "to construct an artificial or universal", "language of the a priori type.")):
        els.append(lab(1290, 610 + 40 * k, s, round(ta + 1.0 * k, 2), GOLD, 30, st="ital", fx="type", dur=1.0))
    return {"base": "dark", "cam": CAM, "els": els}


def s36():
    """A tree of categories (dotted: the idea), each branch ending in a word whose first letter glows; below, the vellum and Wilkins's
    philosophical language of 1668, two centuries apart."""
    tl, tw, tc, tb, ts, t2 = (T("s36", p) for p in ("pure logic", "letters of each word", "category", "But the first", "sixteen hundreds", "two centuries"))
    els = [lab(889, 180, "everything", tl, LILAC, 30, st="ital")]
    for k, (x, name, w) in enumerate(((480, "plants", "chol"), (889, "stars", "okal"), (1300, "bodies", "qokedy"))):
        els += [ln([(889, 196), (x, 262)], tl + .3 + .15 * k, LILAC, 2.5, "claimed", dur=.4), lab(x, 290, name, tl + .5 + .15 * k, LILAC, 28, st="ital")]
        wd = vwidth(w, 3.0)
        els += vword(x - wd / 2, 380, w, 3.0, tw + .2 * k, BONE, 3.4, hi=[0], hic=GOLD)
        els.append(rect(x - wd / 2 - 18, 318, wd + 36, 84, "none", LILAC, 2, 8, tc + .1 * k, style="claimed"))
    X = lambda yr: round(200 + (yr - 1350) / 400 * 1380, 1)
    els += [axis(200, 1580, 650, [(X(y), str(y)) for y in (1400, 1500, 1600, 1700)], tb),
            {"k": "band", "x0": X(1404), "x1": X(1438), "y": 606, "h": 18, "c": GOLD, "in": round(t2 - .3, 2), "fx": "pop"}, lab((X(1404) + X(1438)) / 2, 586, "the vellum", t2 - .2, GOLD, 26),
            ln([(X(1668), 560), (X(1668), 650)], ts, LILAC, 3, dur=.4), lab(X(1668) + 14, 600, "Wilkins, 1668", ts + .2, BONE, 26, "start")]
    els += bracket(X(1438) + 8, X(1668) - 8, 520, t2, "two centuries", AMBER, up=False, ty=505)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


CLAIMS = ["Hebrew", "Latin", "Turkish", "lost Romance"]


def claim_card(x, y, w, h, name, at, s=1.0, word="daiin"):
    out = [rect(x - w / 2, y - h / 2, w, h, "rgba(201,193,238,.07)", LILAC, 2.5, 10, at, fx="pop", style="claimed")]
    wd = vwidth(word, 1.8 * s)
    out += vword(x - wd / 2, y - h * .18, word, 1.8 * s, at + .1, BONE, 2.4)
    out += [arrow([[x, y - h * .1], [x, y + h * .08]], at + .2, LILAC, 2, "claimed", dur=.3, curve=False), lab(x, y + h * .34, name, at + .3, LILAC, round(30 * s), st="ital")]
    return out


def s37():
    """A fan of claim cards, each a Voynich word arrowed to a language, popping as named."""
    els = [lab(889, 210, "claimed solutions", T("s37", "solutions keep coming"), MUTED, 28)]
    for k, (name, w) in enumerate(zip(CLAIMS, ("daiin", "okal", "chedy", "qokain"))):
        x = 290 + 380 * k
        els += claim_card(x, 400 + (18 if k % 2 else 0), 300, 200, name, T("s37", name.split()[-1] if k < 3 else "lost Romance"), 1.0, w)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s38():
    """A screen rearranges a word's letters; through a translator, the sentence types itself; a historian with a question."""
    tc, tr, th, to, ts, tj = (T("s38", p) for p in ("computer program", "letters rearranged", "guessed Hebrew", "Through an online", "she made", "historians of Hebrew"))
    els = [rect(140, 200, 560, 370, "#2a2622", "#c9c1b3", 2, 14, tc - .3, fx="pop"), rect(160, 220, 520, 330, "#10161a", at=tc - .2),
           poly([(380, 570), (460, 570), (480, 640), (360, 640)], "#2a2622", "#c9c1b3", 1.5, tc - .3, "pop"), rect(300, 640, 240, 14, "#2a2622", "#c9c1b3", 1.5, 4, tc - .3)]
    word = ["o", "k", "a", "i", "n"]
    order = [2, 3, 4, 1, 0]
    for j, g in enumerate(word):
        x = 230 + 95 * j
        els += [rect(x - 34, 260, 68, 70, "#1e2a30", "#9fd0ff", 1.5, 6, round(tc + .1 * j, 2), fx="pop")] + vword(x - vwidth(g, 3.0) / 2, 310, g, 3.0, tc + .1 * j + .1, BONE, 3.2)
    for j, src in enumerate(order):
        x = 230 + 95 * j
        g = word[src]
        els += [rect(x - 34, 400, 68, 70, "rgba(201,193,238,.1)", LILAC, 1.5, 6, round(tr + .1 * j, 2), fx="pop", style="claimed")] + vword(x - vwidth(g, 3.0) / 2, 450, g, 3.0, tr + .1 * j + .1, LILAC, 3.2)
        els.append(ln([(230 + 95 * src, 332), (x, 398)], tr + .05 * j, LILAC, 1.6, "claimed", dur=.4))
    els += [lab(420, 528, "Hebrew?", th, LILAC, 30, st="ital")]
    els += [arrow([[710, 380], [780, 380]], to, AMBER, 3, dur=.3, curve=False), lab(1225, 214, "through an online translator", to + .2, MUTED, 24),
            rect(800, 250, 850, 210, "#f2e8d6", "#ffffff", 1.5, 16, to + .2, fx="pop")]
    els += [lab(1225, 335, "she made recommendations to the priest,", ts, "#3a2a1c", 34, st="body", halo=False, fx="type", dur=1.6),
            lab(1225, 395, "man of the house and me and people", ts + 1.7, "#3a2a1c", 34, st="body", halo=False, fx="type", dur=1.6)]
    els += [person(1520, 760, 170, tj), rect(1545, 650, 40, 30, "#5a3a26", "#c9a06a", 1, 3, tj + .2, fx="pop"),
            lab(1460, 700, "historians of Hebrew", tj + .2, BONE, 26, "end")] + qmark(1540, 560, tj + .5, 64, LILAC, halo=False)
    return {"base": "dark", "cam": CAM, "els": els}


def s39():
    """The test in three boxes (fixed rules, every page, a stranger gets the same); below, the claim cards, each struck."""
    tr, tp, ts, ta = (T("s39", p) for p in ("fixed rules", "every page", "same text", "applies the rules"))
    els = []
    for k, x in enumerate((380, 889, 1398)):
        t = (tr, tp, ts)[k]
        els.append(rect(x - 220, 170, 440, 300, "rgba(159,208,255,.05)", BLUE, 2.5, 14, t - .2, style="inferred"))
    els += book_closed(320, 230, 110, 150, tr) + [ln([(340, 270 + 22 * j), (410, 270 + 22 * j)], tr + .2, "rgba(232,184,122,.6)", 2, draw=False) for j in range(4)]
    els += [lab(380, 440, "fixed rules", tr + .2, BLUE, 28)]
    for j in range(5):
        x = 800 + 32 * j
        els += [rect(x, 215 + 10 * j, 110, 150, VEL, VEL_E, 1, 4, round(tp + .1 * j, 2), fx="pop"), tick(x + 70, 250 + 10 * j, round(tp + .4 + .1 * j, 2), s=.7, w=4)]
    els += [lab(889, 440, "every page", tp + .3, BLUE, 28)]
    els += [person(1300, 400, 150, ts), person(1500, 400, 150, ts + .2), rect(1330, 300, 50, 64, VEL, VEL_E, 1, 3, ts + .4, fx="pop"),
            rect(1420, 300, 50, 64, VEL, VEL_E, 1, 3, ts + .5, fx="pop"), lab(1355, 290, "=", ts + .6, GOLD, 40, st="serif"),
            lab(1398, 440, "anyone gets the same", ts + .4, BLUE, 26)]
    for k, name in enumerate(CLAIMS):
        x = 380 + 340 * k
        els += [rect(x - 120, 560, 240, 90, "rgba(201,193,238,.07)", LILAC, 2, 10, round(.4 + .1 * k, 2), fx="pop", style="claimed"),
                lab(x, 616, name, .5 + .1 * k, LILAC, 28, st="ital"), strike(x - 110, 640, x + 110, 570, round(ta + .3 * k, 2))]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": shift(els, 110)}


# ================================================================== chapter 4: beautiful nonsense?
def s40():
    """One person at a desk under a lamp, writing; beside him a pile of vellum grows into a whole book."""
    tr, tf, to = T("s40", "Gordon Rugg"), T("s40", "fill a book"), T("s40", "one person")
    els = [lamp_glow(760, 430, 520, -1, .35), rect(560, 560, 600, 16, WOOD, "#8a6a48", 1.5, 3, .2), ln([(600, 576), (600, 760)], .2, WOOD, 6, draw=False),
           ln([(1120, 576), (1120, 760)], .2, WOOD, 6, draw=False), rect(80, 760, 1620, 6, "#3a2c20", at=.2)]
    els += seated(470, 760, 230, .4)
    els += [rect(650, 470, 190, 90, VEL, VEL_E, 1.2, 4, .5)] + vline(668, 505, ["qokeey", "dal"], 1.4, .8, INK, 1.8)[0] + vline(668, 535, ["chedy", "ol"], 1.4, 1.4, INK, 1.8)[0]
    els += [rect(900, 560 - 230, 200, 230, VEL, VEL_E, 1.2, 4, tf, fx="fill", dur=2.4)] + [ln([(902, 560 - 9 * j), (1098, 560 - 9 * j)], tf + .1 * j, "rgba(120,90,60,.35)", 1.2, draw=False) for j in range(1, 25)]
    els += [lab(889, 200, "Gordon Rugg, 2004", tr, BONE, 32), lab(470, 470, "one person", to, AMBER, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


TAB = [["qo", "o", "ch", "sh", "d", "y"], ["t", "l", "ke", "k", "te", "ee"], ["edy", "aiin", "ol", "ar", "dy", "y"]]
TX, TY, TW, TH = (220, 480, 740), 200, 240, 66


def table_cells(at, step=.02, c="#2a221c"):
    out = []
    for ci, col in enumerate(TAB):
        for ri, syl in enumerate(col):
            x, y = TX[ci], TY + TH * ri
            out.append(rect(x, y, TW - 8, TH - 8, c, "#5a4a3a", 1.2, 4, round(at + step * (ri + 6 * ci), 2)))
            out += vword(x + (TW - 8) / 2 - vwidth(syl, 2.2) / 2, y + 42, syl, 2.2, at + step * (ri + 6 * ci), BONE, 2.6, fx=None)
    return out


def grille_at(row0, at):
    """The card laid on rows row0..row0+3, windows at (col 0, row0), (col 1, row0+2), (col 2, row0): the three syllables shine through."""
    out = [rect(TX[0] - 14, TY + TH * row0 - 10, TX[2] + TW - TX[0] + 20, TH * 4 + 12, "#3a2e24", "#c9b48e", 2.5, 8, at, fx="pop", op=.94)]
    for ci, ro in ((0, 0), (1, 2), (2, 0)):
        x, y = TX[ci], TY + TH * (row0 + ro)
        syl = TAB[ci][row0 + ro]
        out += [rect(x, y, TW - 8, TH - 8, "#2a221c", GOLD, 3, 4, at + .1)] + vword(x + (TW - 8) / 2 - vwidth(syl, 2.2) / 2, y + 42, syl, 2.2, at + .15, GOLD, 2.8, fx=None)
    return out


def s41():
    """Rugg's table and grille: three columns of syllables; a card with three windows; slide it, copy again; out comes Voynich-like text."""
    tt, tb, tm, te, tc, tw, ts, ta, to = (T("s41", p) for p in ("table of meaningless", "beginnings", "middles", "ends", "Lay a card", "copy what shows", "Slide the card", "copy again", "Out comes"))
    els = [lab(TX[0] + TW / 2, 180, "beginnings", tb, CA, 28), lab(TX[1] + TW / 2, 180, "middles", tm, CA, 28), lab(TX[2] + TW / 2, 180, "ends", te, CA, 28)]
    els += table_cells(tt)
    els += grille_at(0, tc)
    els += [rect(1110, 190, 560, 440, VEL, VEL_E, 1.5, 8, tt + .5), lab(1390, 680, "Voynich-like", to + .4, GOLD, 30)]
    els += [arrow([[990, 250], [1060, 250], [1120, 256]], tw - .2, GOLD, 3, dur=.4)] + vword(1140, 270, "qokeedy", 2.4, tw, INK, 3)
    els += table_cells(ts, step=0) + grille_at(1, ts + .1)
    els += [arrow([[990, 320], [1060, 330], [1120, 336]], ta - .2, GOLD, 3, dur=.4)] + vword(1140, 340, "okaiin", 2.4, ta, INK, 3)
    for k in range(4):
        els += vline(1140, 410 + 56 * k, evas(6, 40 + k), 2.0, to + .3 * k, INK, 2.6, maxw=500)[0]
    els += [lab(600, 640, "table and grille", .6, MUTED, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s42():
    """Left: Rugg's claim, dotted: the grille mimics the staircase too. Right: Timm and Schinner's page: a word copied down the page, a letter changed each time."""
    tm, tt, ts, tc, tg, tr, tq = (T("s42", p) for p in ("mimic the word staircase", "Torsten Timm", "a simpler one", "copy a word", "change a letter", "carry on", "mimics many"))
    els = [lab(350, 230, "the staircase too?", tm + .2, LILAC, 30, st="ital"), ln([(140, 560), (580, 560)], tm, MUTED, 2, draw=False)]
    els += stair(180, 560, 260, tm, n=7, pitch=60, wd=36, c="rgba(201,193,238,.25)", step=.08, style="claimed", edge=LILAC)
    els += [lab(350, 610, "Rugg and Taylor, 2016", tm + .4, MUTED, 24)]
    els += [rect(700, 200, 960, 480, VEL, VEL_E, 1.5, 8, tt - .2), lab(1180, 170, "Timm and Schinner, 2019", tt, BONE, 28)]
    chain = [("qokedy", 920, None), ("qokeedy", 1150, [4]), ("okeedy", 980, None), ("okedy", 1230, None), ("otedy", 1010, [1])]
    fill = [evas(8, 70 + k) for k in range(5)]
    pos = []
    for k, (w, x, hi) in enumerate(chain):
        y = 270 + 90 * k
        els += vline(730, y, fill[k], 1.6, ts + .1 * k, INK, 2.0, maxw=x - 760)[0]
        tk = tc if k == 0 else (tg if k == 1 else tr + .5 * (k - 2))
        els += vword(x, y, w, 2.2, tk, INK, 2.8, hi=hi, hic=HI)
        els.append(rect(x - 10, y - 38, vwidth(w, 2.2) + 20, 52, "none", AMBER, 2, 6, tk, style="inferred"))
        if k:
            px_, py_ = pos[-1]
            els.append(arrow([[px_, py_ + 18], [(px_ + x) / 2 + 40, (py_ + y) / 2], [x + 20, y - 40]], tk - .2, AMBER, 2.5, dur=.5))
        pos.append((x + vwidth(w, 2.2) / 2, y))
    els += [lab(1180, 730, "copy, change, carry on", tr, AMBER, 28), tick(1600, 230, tq)]
    return {"base": "dark", "cam": CAM, "els": els}


def s43():
    """Three objections: the grille is a century younger than the vellum; a sliding card has no reason to crowd words by topic; five scribes
    keeping two dialects apart, for a joke?"""
    t1, t2, t3, t4 = (T("s43", p) for p in ("A card with windows", "Critics doubt", "And five scribes", "a joke"))
    X = lambda yr: round(160 + (yr - 1400) / 200 * 420, 1)
    els = [axis(140, 600, 560, [(X(1400), "1400"), (X(1500), "1500"), (X(1600), "1600")], t1),
           {"k": "band", "x0": X(1404), "x1": X(1438), "y": 520, "h": 18, "c": GOLD, "in": round(t1 + .3, 2), "fx": "pop"}, lab(X(1421), 500, "vellum", t1 + .4, GOLD, 24)]
    els += grille_card(X(1550) - 55, 300, 110, 80, t1 + .8) + [ln([(X(1550), 384), (X(1550), 556)], t1 + .9, BONE, 2, dur=.4), lab(X(1550), 285, "c. 1550", t1 + 1.0, BONE, 26)]
    els += bracket(X(1438) + 6, X(1550) - 6, 470, t1 + 1.6, "a century", AMBER, up=False, ty=455)
    els += minipages(690, 280, 8, 4, 80, 100, 14, t2) + [lab(889, 550, "words by topic", t2 + .4, BONE, 26)]
    r = random.Random(14)
    for j in range(16):
        pg_ = 5 if j < 8 else 6
        x = 690 + 94 * (pg_ % 4) + r.uniform(12, 68); y = 280 + 114 * (pg_ // 4) + r.uniform(12, 88)
        els.append(dot(round(x, 1), round(y, 1), 5.5, AU, round(t2 + .3 + .02 * j, 2)))
    els += grille_card(780, 600, 110, 80, t2 + 1.2) + qmark(960, 680, t2 + 1.5, 60, LILAC, halo=False)
    for j in range(5):
        x = 1260 + 70 * j
        c = CA if j % 2 == 0 else CB
        els += [ln([(x, 300), (x + 18, 430)], round(t3 + .15 * j, 2), BONE, 6, dur=.3), poly([(x + 14, 425), (x + 24, 425), (x + 22, 450)], c, at=round(t3 + .15 * j, 2), fx="pop"),
                rect(x - 12, 470, 40, 54, c, "#fff6e6", 1, 3, round(t3 + .3 + .15 * j, 2), fx="pop")]
    els += [lab(1400, 570, "five scribes, two dialects", t3 + .5, BONE, 26)] + tag(1400, 650, "a joke?", t4, LILAC, 28, "claimed")
    return {"base": "dark", "stars": 25, "cam": CAM, "els": shift(els, 80)}


def s44():
    """42 volunteers, each with a page of invented nonsense; two meters, predictable and repetitive, put them beside the book."""
    ty, tv, tp = T("s44", "Yale team"), T("s44", "forty two volunteers"), T("s44", "predictable and repetitive")
    els = [lab(530, 200, "Yale, 2022: 42 volunteers", ty, BONE, 30)]
    for k in range(42):
        c_, r_ = k % 7, k // 7
        x, y = 190 + 112 * c_, 320 + 82 * r_
        t = round(tv + .03 * k, 2)
        els += [person(x, y, 62, t), rect(x + 16, y - 46, 22, 30, VEL, VEL_E, .8, 2, t + .1, fx="pop"),
                ln([(x + 19, y - 38), (x + 34, y - 38)], t + .3, INK, 1.4, draw=False), ln([(x + 19, y - 30), (x + 31, y - 30)], t + .3, INK, 1.4, draw=False)]
    for j, (name, y, xb, xv, xl) in enumerate((("predictable", 380, 1540, 1500, 1180), ("repetitive", 600, 1520, 1550, 1200))):
        t = tp + .8 * j
        els += [lab(1060, y - 50, name, t, BONE, 30, "start"), ln([(1060, y), (1640, y)], t, "#5a5048", 14, dur=.5),
                ln([(xl, y - 16), (xl, y + 16)], t + .2, MUTED, 3, draw=False), dot(xb, y, 13, GOLD, t + .4), poly([(xv - 12, y - 34), (xv + 12, y - 34), (xv, y - 14)], AMBER, at=t + .6, fx="pop")]
        if j == 0:
            els += [lab(xl, y + 46, "languages", t + .2, MUTED, 24), lab(xb + 20, y + 46, "this book", t + .4, GOLD, 24), lab(xv - 20, y - 44, "volunteers", t + .6, AMBER, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s45():
    """Left: in the book, certain letters sit tight at the start and end of words (glowing columns); the volunteers' words do not.
    Right: a cipher that merges two sounds into one sign makes text as predictable as the book."""
    t1, t2, t3 = T("s45", "nobody packed"), T("s45", "the same team"), T("s45", "just as predictable")
    els = [lab(330, 200, "this book", t1, GOLD, 30), lab(690, 200, "volunteers", t1 + .3, AMBER, 30)]
    vws = ["qokeedy", "qokedy", "qotedy", "qoky"]
    for k, w in enumerate(vws):
        n = len(_letters(w))
        els += vword(190, 290 + 85 * k, w, 2.6, t1 + .15 * k, BONE, 3.2, hi=[0, n - 1], hic=GOLD)
    els += [rect(182, 240, 46, 330, "rgba(242,201,142,.08)", GOLD, 2, 6, t1 + .8, style="inferred")]
    for k, w in enumerate(("ralimen", "tosk", "beliran", "omuta")):
        els.append(lab(600, 300 + 85 * k, w, round(t1 + .3 + .15 * k, 2), MUTED, 40, "start", st="serif"))
    els += [lab(450, 640, "tight word edges", t1 + 1.4, BONE, 26)]
    els += [lab(1300, 200, "merging sounds", t2, BONE, 28)]
    els += [circ(1080, 300, 44, "rgba(245,236,220,.06)", BONE, 2.5, t2 + .4, "pop"), lab(1080, 318, "b", t2 + .45, BONE, 52, st="serif"),
            circ(1080, 440, 44, "rgba(245,236,220,.06)", BONE, 2.5, t2 + .6, "pop"), lab(1080, 458, "p", t2 + .65, BONE, 52, st="serif"),
            arrow([[1130, 310], [1250, 360]], t2 + 1.0, AMBER, 3, dur=.4, curve=False), arrow([[1130, 430], [1250, 380]], t2 + 1.0, AMBER, 3, dur=.4, curve=False),
            circ(1320, 370, 56, "rgba(242,201,142,.08)", GOLD, 2.5, t2 + 1.3, "pop")] + vword(1300, 392, "d", 3.6, t2 + 1.4, GOLD, 4)
    els += [ln([(1440, 720), (1660, 720)], t3 - .3, MUTED, 2, draw=False), vbar(1490, 720, 224, 70, "rgba(232,184,122,.25)", t3, style="inferred", edge=AMBER, fx="fade"),
            vbar(1610, 720, 154, 70, GOLD, t3 + .5), arrow([[1530, 520], [1600, 556]], t3 + .7, BONE, 2.5, dur=.3, curve=False),
            lab(1490, 760, "plain", t3, MUTED, 24), lab(1610, 760, "merged", t3 + .5, GOLD, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s46():
    """Greshko's cipher: dice and a playing card; a Latin line cut into pieces of one or two letters; one of six tables lights for
    each piece; out comes a strip of Voynich-like words."""
    tn, td, tc, tf, tr, tp, tk, tt, to = (T("s46", p) for p in ("Michael Greshko", "dice", "playing cards", "fifteenth century", "A roll of the die", "pieces of one",
                                                                 "a card picks", "six tables", "Out comes"))
    els = [lab(330, 190, "Greshko, 2025", tn, BONE, 30)]
    els += die(250, 300, 100, 5, td) + die(345, 330, 70, 2, td + .2) + card(470, 310, 90, 130, "7", tc)
    els += [lab(360, 430, "15th-century tools", tf, MUTED, 24)]
    els += [rect(640, 220, 1000, 90, "#e9d6ad", "#fff4dc", 1.2, 6, tr), lab(1140, 282, "VENI VIDI VICI", tr + .2, "#5a4330", 46, st="serif", halo=False, fx="type", dur=.9)]
    pieces = ["VE", "N", "I", "VI", "D", "I", "VI", "CI"]
    widths = [92 if len(p_) == 2 else 62 for p_ in pieces]
    x = 1140 - (sum(widths) + 14 * 7) / 2
    cxs = []
    for j, (p_, w) in enumerate(zip(pieces, widths)):
        t = round(tp + .12 * j, 2)
        els += [rect(x, 360, w, 70, "#efe3c8", "#fff6e6", 1.2, 6, t, fx="pop"), lab(x + w / 2, 410, p_, t + .05, "#5a4330", 36, st="serif", halo=False)]
        cxs.append(x + w / 2); x += w + 14
    els += [arrow([[1140, 318], [1140, 352]], tp - .1, AMBER, 2.5, dur=.3, curve=False)]
    for j in range(6):
        gx, gy = 220 + 92 * (j % 3), 520 + 76 * (j // 3)
        t = round(tk + .08 * j, 2)
        els += [rect(gx, gy, 78, 62, "#2a221c", "#8a7a66", 1.2, 4, t, fx="pop")] + [ln([(gx + 6, gy + 14 + 12 * q), (gx + 72, gy + 14 + 12 * q)], t, "#6a5a48", 1, draw=False) for q in range(4)]
    els += [rect(220 + 92 - 4, 520 - 4, 86, 70, "none", GOLD, 3.5, 6, tt + .3), glow(220 + 92 + 39, 551, 90, tt + .3, .6), lab(350, 700, "six tables", tt, MUTED, 24),
            arrow([[470, 380], [400, 470], [360, 512]], tk, AMBER, 2.5, "inferred", dur=.5)]
    els += [rect(700, 560, 900, 110, VEL, VEL_E, 1.5, 8, to - .4)]
    outw = ["or", "y", "o", "aiin", "d", "ar", "ol", "chy"]
    for j, (w, cx) in enumerate(zip(outw, cxs)):
        t = round(to + .15 * j, 2)
        els += [ln([(cx, 436), (cx, 556)], t - .15, "rgba(232,184,122,.5)", 1.6, "inferred", dur=.3)] + vword(cx - vwidth(w, 2.2) / 2, 632, w, 2.2, t, INK, 2.8)
    els += [lab(1150, 720, "Voynich-like", to + 1.3, GOLD, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s47():
    """A balance with the book at its foot: the grille card (nonsense) on one pan, dice and card (cipher) on the other; the beam level."""
    tn, td, tq, tc = (T("s47", p) for p in ("Not a solution", "decodes no", "Nonsense can", "So can a cipher"))
    left = lambda x, y, at: grille_card(x - 60, y - 90, 120, 86, tq)
    right = lambda x, y, at: die(x - 30, y - 34, 60, 3, at + .3) + card(x + 36, y - 46, 56, 84, "7", at + .4)
    els = balance(889, 270, 780, 0, 720, .3, left, right, drop=200, pan=210)
    els += book_closed(990, 630, 100, 80, .5)
    els += [lab(499, 540, "nonsense", tq + .2, LILAC, 30), lab(1279, 540, "cipher", tc, BLUE, 30), glow(889, 270, 160, tc + .3, .5)]
    els += [ln([(1279, 486), (1279, 600)], tn, LILAC, 2, "claimed", dur=.4)] + tag(1279, 640, "not a solution", tn + .3, LILAC, 26, "claimed")
    els += [rect(1420, 600, 70, 92, VEL, VEL_E, 1, 3, td, fx="pop")] + cross(1455, 646, td + .3, RED, 1.2)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== chapter 5: the weighing
LROWS = [220, 350, 480, 610]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 55, 1500, 110, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 32, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1180, y, grade, gc, gt, 30, "start")
    return out


def pic_book(x, y, at):
    return book_closed(x - 34, y - 44, 64, 88, at) + [rect(x - 26, y + 8, 52, 10, GOLD, r=3, at=at + .2, fx="pop")]


def pic_quill(x, y, at):
    return quill(x - 30, y + 40, 70, at)


def pic_claims(x, y, at):
    return [rect(x - 46 + 10 * j, y - 30 - 8 * j, 70, 52, "rgba(201,193,238,.08)", LILAC, 2, 4, at + .05 * j, style="claimed") for j in range(3)] + [strike(x - 50, y + 26, x + 50, y - 46, at + .3)]


def pic_tree(x, y, at):
    return [ln([(x, y - 34), (x - 40, y + 10)], at, LILAC, 2.5, "claimed", draw=False), ln([(x, y - 34), (x, y + 10)], at, LILAC, 2.5, "claimed", draw=False),
            ln([(x, y - 34), (x + 40, y + 10)], at, LILAC, 2.5, "claimed", draw=False)] + [dot(x + dx, y + 18, 6, LILAC, at) for dx in (-40, 0, 40)] + [dot(x, y - 38, 7, LILAC, at)]


def s48():
    """The ledger board: four rows light as they are named; their grade chips pop as the grades are said."""
    t1, t2, t3 = T("s48", "Established"), T("s48", "A modern fake"), T("s48", "Already solved")
    g1, g2, g3 = T("s48", "painted with"), T("s48", "Ruled out"), T("s48", "Ruled out", k=2)
    els = [rect(110, 140, 1560, 560, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, t1, pic_book, "a real book, 1400s", "Established", g1 + .6, GRADE["established"])
    els += lrow(1, t2, pic_quill, "a modern fake", "Ruled out", g2, GRADE["ruled"])
    els += lrow(2, t3, pic_claims, "already solved", "Ruled out", g3, GRADE["ruled"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s49_add():
    tl, ta = T("s49", "A language invented"), T("s49", "Awaiting evidence")
    return lrow(3, tl, pic_tree, "a language of logic", "Awaiting evidence", ta, GRADE["awaiting"])


def s50():
    """The main contest on a balance: a language in cipher against meaningless text; both chips 'Open question'; the verdict chip; then the
    reasons pop: the staircase, the lone short bar, the die and the grille."""
    tl, tm, tb, to, tw, tx, tf = (T("s50", p) for p in ("A real language", "Or meaningless", "Both", "Open question", "The words behave", "the letters", "fifteenth century tools"))
    left = lambda x, y, at: padlock(x, y - 40, 90, tl, AMBER, "known", "rgba(232,184,122,.12)") + [rect(x - 70, y - 120, 60, 80, VEL, VEL_E, 1, 3, tl - .1, fx="pop")]
    right = lambda x, y, at: grille_card(x - 60, y - 90, 120, 86, tm)
    els = balance(889, 300, 820, 0, 740, .3, left, right, drop=200, pan=220)
    els += [lab(479, 570, "language in cipher", tl + .3, AMBER, 30), lab(1299, 570, "meaningless", tm + .3, LILAC, 30)]
    els += chip(479, 630, "Open question", GRADE["open"], tb + .3, 26) + chip(1299, 630, "Open question", GRADE["open"], tb + .5, 26)
    els += chip(889, 180, "Open question", GRADE["open"], to + .4, 40) + [glow(889, 180, 260, to + .4, .4)]
    els += stair(160, 470, 120, tw, n=5, pitch=28, wd=18, c=GREEN, step=.06) + [tick(330, 360, tw + .5, s=.8)]
    els += [vbar(1560, 470, 96, 34, AMBER, tx, op=.8), vbar(1610, 470, 66, 34, GOLD, tx + .2)] + qmark(1660, 380, tx + .4, 50, LILAC, halo=False)
    els += die(780, 700, 50, 4, tf) + grille_card(930, 672, 80, 58, tf + .2) + [lab(889, 770, "either way", tf + .4, MUTED, 24)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s51():
    """Four test boxes (dashed: not yet done) fill as named: a bilingual sign, a reading that fits every page, a second book, a method
    that matches every statistic at once."""
    t1, t2, t3, t4 = (T("s51", p) for p in ("A key", "A reading that", "A second book", "Or a medieval"))
    xs = [110, 506, 902, 1298]
    els = []
    for k, (x, t, name) in enumerate(zip(xs, (t1, t2, t3, t4), ("a bilingual", "a reading that fits", "a second book", "a matching method"))):
        els += [rect(x, 200, 370, 420, "rgba(159,208,255,.05)", BLUE, 2.5, 14, t - .2, style="inferred"), lab(x + 185, 670, name, t + .3, BLUE, 28)]
    x = xs[0]
    els += [ln([(x + 120, 600), (x + 120, 470)], t1, "#8a8a8a", 6, draw=False), ln([(x + 250, 600), (x + 250, 470)], t1, "#8a8a8a", 6, draw=False),
            rect(x + 40, 270, 290, 200, "#1d2a33", "#5a6a70", 2, 10, t1, fx="pop")]
    els += vline(x + 64, 330, ["qokeedy", "dal"], 1.7, t1 + .3, "#ffd36a", 2.4)[0]
    els += [{"k": "glyphs", "x": x + 64, "y": 380, "w": 230, "h": 60, "rows": 2, "cols": 6, "kind": "latin", "c": "#ffd36a", "sw": 5, "in": round(T("s51", "a script we can"), 2)},
            lab(x + 185, 255, "✈", T("s51", "airport"), "#ffd36a", 40, halo=False)]
    x = xs[1]
    for j in range(3):
        px_ = x + 30 + 110 * j
        t = round(t2 + .4 * j, 2)
        els += [rect(px_, 300, 96, 150, VEL, VEL_E, 1, 4, t, fx="pop")] + plant(px_ + 48, 440, 90, t + .1, kind=j % 4, step=.2)
        els += [rect(px_ + 10, 310, 76, 22, "rgba(242,201,142,.3)", GOLD, 2, 4, t + .5), tick(px_ + 48, 480, t + .6, s=.7, w=4)]
    x = xs[2]
    for j in range(2):
        bx = x + 40 + 160 * j
        els += [rect(bx, 280, 140, 200, VEL, VEL_E, 1, 6, t3 + .2 * j, fx="pop")] + vtext(bx + 12, 316, 116, 4, 1.0, t3 + .2 * j + .1, lh=30, seed=60 + 7 * j, w=1.6)
        els += vword(bx + 22, 455, "qokedy", 1.8, t3 + .5, HI, 2.6)
    x = xs[3]
    els += die(x + 70, 300, 60, 4, t4) + card(x + 140, 300, 50, 74, "7", t4 + .1)
    for j, name in enumerate(("letters", "words", "topics")):
        y = 400 + 62 * j
        t = round(t4 + .6 + .4 * j, 2)
        els += [lab(x + 30, y + 8, name, t, BONE, 24, "start"), ln([(x + 130, y), (x + 340, y)], t, "#5a5048", 10, dur=.3),
                dot(x + 300, y, 10, GOLD, t + .1), poly([(x + 290, y - 30), (x + 310, y - 30), (x + 300, y - 12)], AMBER, at=t + .3, fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": shift(els, 50)}


def s52():
    """The first page again: coloured scan bands sweep down it; three faint columns of letters glow in its right margin, two in our
    alphabet and one in the book's; a dashed tag: Marci's key?"""
    tc, ti, tl, tm = T("s52", "keeps giving"), T("s52", "images released"), T("s52", "columns of letters"), T("s52", "probably Marci's")
    els = page(470, 140, 780, 650, .2) + vtext(510, 205, 570, 14, 1.15, .3, lh=37, seed=31, w=2.0, dt=.0, row_dt=.04, op=.6)
    cols = ["#ff6a5a", "#ffb04a", "#ffe46a", "#7ad48a", "#6ab4ff", "#a88aff"]
    for j, c in enumerate(cols):
        els.append(rect(470, 140 + 108 * j, 780, 108, c, at=round(T("s52", "twenty twenty four") + .2 * j, 2), op=.09))
    els += [lab(300, 420, "2024 images", ti, BONE, 30)]
    for j in range(9):
        y = 230 + 42 * j
        t = round(tl + .06 * j, 2)
        els += [lab(1128, y, "abcdefghi"[j], t, "#6a3a20", 26, st="serif", halo=False), lab(1168, y, "klmnopqrs"[j], t + .1, "#6a3a20", 26, st="serif", halo=False)]
        g = ["o", "a", "e", "d", "y", "k", "ch", "l", "r"][j]
        els += vword(1200, y, g, 1.5, t + .2, "#6a3a20", 2.2)
    els += [rect(1108, 196, 140, 400, "rgba(232,184,122,.1)", AMBER, 2, 8, tl + .6, style="inferred")]
    els += tag(1420, 330, "Marci's key?", tm, AMBER, 28, "inferred", "start") + [ln([(1418, 330), (1252, 380)], tm, AMBER, 2, "inferred", dur=.4)]
    return {"base": "dark", "cam": [1.3, 1094, 470], "els": els}


def s53():
    """Night: the open book on a desk by a starry window; the lamp; the plants on its pages glow one after another; an empty chair."""
    tp = T("s53", "its plants")
    els = [rect(1180, 150, 440, 340, "#0e1626", "#6b4a30", 10, 6, -1), {"k": "stars", "n": 70, "x0": 1190, "x1": 1610, "y0": 160, "y1": 480, "seed": 9, "in": -1},
           ln([(1400, 150), (1400, 490)], -1, "#6b4a30", 8, draw=False), ln([(1180, 320), (1620, 320)], -1, "#6b4a30", 8, draw=False),
           circ(1520, 230, 26, "#f4ecd8", at=-1), glow(1520, 230, 90, -1, .4)]
    els += [rect(-40, 640, 1860, 18, WOOD, "#8a6a48", 1.5, 2, -1), rect(-40, 658, 1860, 400, WOOD_D, at=-1)] + \
           [ln([(-40, 690 + 30 * k), (1820, 694 + 30 * k)], -1, "rgba(0,0,0,.25)", 2, draw=False) for k in range(4)]
    els += [poly([(200, 640), (300, 640), (280, 624), (220, 624)], "#3a2c20", at=-1), ln([(250, 624), (250, 430)], -1, "#5a4836", 6, draw=False),
            poly([(180, 440), (320, 440), (290, 360), (210, 360)], "#7a5a36", "#c9a06a", 1.5, -1), lamp_glow(250, 470, 620, -1, .5)]
    # the open book, lying on the desk, seen at a slant
    els += [poly([(420, 452), (1080, 452), (1140, 640), (360, 640)], "#4a3020", "#8a6a48", 2, -1),
            poly([(436, 460), (750, 466), (752, 630), (382, 630)], VEL, VEL_E, 1, -1), poly([(754, 466), (1066, 460), (1120, 630), (756, 630)], VEL, VEL_E, 1, -1),
            ln([(752, 466), (754, 630)], -1, "rgba(90,60,30,.5)", 3, draw=False)]
    for j, (x, kind) in enumerate(((590, 0), (930, 2))):
        els += static(plant(x, 600, 130, -1, kind=kind))
        els.append(glow(x, 540, 130, round(tp + .9 * j, 2), .55))
    els += static(vtext(460, 488, 250, 2, .7, -1, lh=20, seed=41, w=1.4, op=.8) + vtext(790, 488, 250, 2, .7, -1, lh=20, seed=42, w=1.4, op=.8))
    # an empty chair beside the desk, its back above the desk top
    els += [ln([(1300, 420), (1310, 640)], -1, "#5a4030", 10, draw=False), ln([(1420, 420), (1410, 640)], -1, "#5a4030", 10, draw=False),
            ln([(1302, 440), (1418, 440)], -1, "#5a4030", 8, draw=False), ln([(1304, 500), (1416, 500)], -1, "#5a4030", 6, draw=False)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "And two hundred", "s2"), (1, "Can a book", "s3"), (1, "This one has", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [], {"chapter": "A letter inside the book"}),
    (1, 1, "collision", "s7", [(1, "He passed on", "s8"), (1, "But under ultraviolet", "s9"), (2, "And in Kircher's", "s10")], {}),
    (1, 2, "cost", "s11", [(1, "In {2009", "s12"), (1, "Living things", "s13"), (2, "Between about", "s14"), (2, "That dates", "s15")], {}),
    (1, 3, "reversal", "s16", [(0, "Small bathing", "s17"), (0, "Jars beside", "s18"), (1, "It looks like", "s19")], {}),
    (2, 0, "world", "s20", [], {"chapter": "Counting the unreadable"}),
    (2, 1, "collision", "s21", [(1, "And some words", "s22"), (2, "In {1976", "s23"), (2, "In {2020", "s24"), (2, "Dialect A", "s25")], {}),
    (2, 2, "cost", "s26", [(1, "On a standard", "s27"), (2, "And words repeat", "s28")], {}),
    (2, 3, "tag", "s29", [], {}),
    (3, 0, "world", "s30", [(1, "His reading", "s31")], {"chapter": "A century of solutions"}),
    (3, 1, "reversal", "s32", [(0, "And Newbold's method", "s33")], {}),
    (3, 2, "cost", "s34", [(1, "In {1959", "s35"), (2, "A language built", "s36")], {}),
    (3, 3, "tag", "s37", [(0, "In {2016", "s38"), (1, "Here's the test", "s39")], {}),
    (4, 0, "world", "s40", [], {"chapter": "Beautiful nonsense?"}),
    (4, 1, "collision", "s41", [(1, "Later, he argued", "s42")], {}),
    (4, 2, "cost", "s43", [], {}),
    (4, 3, "reversal", "s44", [(1, "Except in one", "s45")], {}),
    (4, 4, "tag", "s46", [(1, "Not a solution", "s47")], {}),
    (5, 0, "weigh", "s48", [(1, "A language invented", "s49"), (2, "A real language", "s50")], {"chapter": "The weighing"}),
    (5, 1, "test", "s51", [(1, "And the book keeps", "s52")], {}),
    (5, 2, "close", "s53", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1, 889, 500], "s2_add"), "s4": ("s3", [1, 889, 500], "s4_add"),
    "s11": ("s10", [1, 889, 500], "s11_add"), "s14": ("s10", [1, 889, 500], "s14_add"),
    "s17": ("s16", [2.0, 889, 430], "s17_add"), "s18": ("s16", [2.0, 1334, 430], "s18_add"), "s19": ("s16", [1, 889, 500], "s19_add"),
    "s24": ("s23", [1.5, 889, 600], "s24_add"), "s25": ("s23", [1, 889, 500], "s25_add"),
    "s32": ("s30", [1.6, 760, 470], "s32_add"), "s49": ("s48", [1.15, 889, 560], "s49_add"),
}


def _segments(script):
    """The narration each shot has on screen, from the beats with their markers (a chapter beat's first sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            if sid in ALIASES and ALIASES[sid][2] is None:
                continue
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
                panels[sid] = g[sid]()
    ids = list(panels) + [a for a in ALIASES]
    idx = {s: i for i, s in enumerate(ids)}
    shots = [panels[s] for s in panels] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[idx[sid]] = idx[root]
        cams[idx[sid]] = [z] + list(cam[1:])
        tags[z] = g[fn]() if fn else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-voynich", "code": "LF.10", "series": script["series"], "title": script["title"], "case": "voynich",
          "verdict": "contested", "claim": "Does the Voynich manuscript hide a real language, or nothing at all?", "mood": "mystery",
          "hook_text": "Can a book exist that *nobody* can read?", "beats": beats, "shots": shots,
          "sources": "Beinecke MS 408 · Hodgins 2011 (University of Arizona radiocarbon) · Manly 1931 (doi:10.2307/2848508) · Currier 1976 · "
                     "Montemurro & Zanette 2013 (doi:10.1371/journal.pone.0066344) · Davis 2020 (doi:10.1353/mns.2020.0011) · "
                     "Bowern & Lindemann 2021 (doi:10.1146/annurev-linguistics-011619-030613) · Rugg 2004 (doi:10.1080/0161-110491892755) · "
                     "Timm & Schinner 2020 (doi:10.1080/01611194.2019.1596999) · Gaskell & Bowern 2022 (CEUR-WS 3313) · Greshko 2025 (doi:10.1080/01611194.2025.2566408)",
          "post": "Two hundred and forty pages in an alphabet nobody can read, on calfskin from the early 1400s. Why its words behave like a language, "
                  "why its letters behave like nothing we know, the solutions that failed, the hoax recipes, and a dice-and-cards cipher, weighed.",
          "hashtags": ["#Voynich", "#VoynichManuscript", "#Cipher", "#History", "#Unreadable", "#WeighItYourself"],
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
