"""LF.23 · Unreadable · The Herculaneum Scrolls: The Library Vesuvius Kept (16:9 long film, one wall).

The script is films/long/lf-herculaneum/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s52; s5, the title, is the intro card over the
panel of s4), drawn while it is said: a carbonised roll on a museum cloth (the hero), the X-ray look inside it, Vesuvius over the
villa, the 2026 strip; the Bay of Naples, the well and the twenty metres of rock, the heat of the current, the villa's plan, the
tunnels and the statues, the black lumps, Paderni's letter, the count of rolls and books, the owner; a roll unrolled beside a
person, the knife, Piaggio's machine and its year for half a roll, the first roll (On Music), Philodemus from Gadara, the shelves,
infrared and the rolls still closed; the CT scanner, virtual unwrapping, the blank Paris scans, En-Gedi, black ink on a black page,
the synchrotron, the sniffer-dog model; the Vesuvius Challenge, the crackle, the first word, the second finder, the grand prize,
the balance of rare and plentiful, the first title in Oxford, Virgil; PHerc. 1667 as it was and as it is, its scan, its 31 turns
and 22 columns, the Stoa, its age, On Gods 8, faces in clouds and the three checks, the crushed rolls; the ledger, the villa's
lower floors and its boxes, the tests and the close. Drawings are schematic and true to the numbers said: solid = measured,
dashed = inferred, dotted = claimed. Greek on screen is drawn with a small stroke alphabet of book-hand capitals (GK below), as the
papyri have the words; no reading is invented.

Facts: the Short 'herculaneum-scrolls' (f12.py, rewrite/herculaneum-scrolls.json) and the script's facts_added (Angelotti et al.
2026; Vesuvius Challenge 2023, 2024, 2026; Nicolardi et al. 2024; Bodleian 2025; Seales et al. 2016; Mocella et al. 2015; Parker et
al. 2019; Parsons et al. 2023; Giordano et al. 2018; Paderni 1753; the letter of 1755; Sider 2005; Janko 2002, 2025; Moran 2024;
Delattre 2007; Woodward 2009; Scappaticcio 2010; McOsker & Fratantuono 2024; Blank 2019).

Engine workaround (as in lf_troy.py and lf_piri_reis.py): the wall only adds elements to a panel on its first visit, at a beat
start or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag
(+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel
item (built on that step's clock). Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at
about 4.25 syllables a second).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-herculaneum/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-herculaneum/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-herculaneum RC_FILMS_EPS=/tmp/claude-0/sbx_lf-herculaneum/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-herculaneum/boards python3 films.py long.lf_herculaneum
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-herculaneum", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
CHAR, CHAR2, CHAR3, CHAR_E = "#16110d", "#241b15", "#33281f", "#7a624c"      # charcoal: deep, body, highlight band, lit rim
SHEET, SHEET_E = "#2b221b", "#4e3f32"                                         # a flattened carbonised layer (on screen)
PAP, PAP_D, INKD = "#e9d6ad", "#c9ad7d", "#4a3828"                            # fresh papyrus, its shade, brown ink
CREAM = "#e9dccb"                                                             # recovered letters on a dark scan
STONE, STONE_D, MARBLE = "#c9a87a", "#8c7152", "#efe6d6"
ROCK, ROCK_D = "#5a544d", "#3c3833"
WOOD, WOOD_D = "#6b4a30", "#3a281a"
SKIN = "#e8d6b8"
PURPLE = "#8a3a8f"
SEAC = "#3f86a8"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c35a", "awaiting": "#c9c1ee"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # BCE, CE: one syllable a letter
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
    for li, ln in enumerate(text.split("\n")):
        if li:
            t += LGAP
        cuts = [0] + [m.start() for m in SENT.finditer(ln) if m.start() > 0] + [len(ln)]
        for a, z in zip(cuts, cuts[1:]):
            seg = ln[a:z]
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
    return ellipse(cx, cy, rx, ry, n, a0, a1)[:-1] if (a1 - a0) >= 360 else ellipse(cx, cy, rx, ry, n, a0, a1)


def chip(x, y, t, c, at, size=28, a="middle"):
    """A pill with a coloured rim and its words (grades, dates)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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
    out = [gl(x, y - size * .3, size * 1.1, at, .5)] if halo else []
    return out + [lab(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def bracket(x0, x1, y, at, t=None, c=BONE, up=True, size=26, ty=None, style="known"):
    d = -12 if up else 12
    out = [ln([[x0, y + d], [x0, y], [x1, y], [x1, y + d]], at, c, 2, style, dur=.6)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else (y - 16 if not up else y + 36), t, at + .3, c, size))
    return out


def dimv(x, y0, y1, at, t, c=GOLD, side=1, size=26, dur=.8):
    """A vertical dimension line with end bars and its words to one side."""
    return [ln([(x, y0), (x, y1)], at, c, 2, dur=dur), ln([(x - 10, y0), (x + 10, y0)], at, c, 2, draw=False),
            ln([(x - 10, y1), (x + 10, y1)], at + dur * .9, c, 2, draw=False),
            lab(x + side * 18, (y0 + y1) / 2 + 9, t, at + dur * .8, c, size, "start" if side > 0 else "end")]


def dimh(x0, x1, y, at, t, c=GOLD, size=26, dy=-16, dur=.8):
    """A horizontal dimension line with end bars and its words above (dy < 0) or below."""
    return [ln([(x0, y), (x1, y)], at, c, 2, dur=dur), ln([(x0, y - 10), (x0, y + 10)], at, c, 2, draw=False),
            ln([(x1, y - 10), (x1, y + 10)], at + dur * .9, c, 2, draw=False),
            lab((x0 + x1) / 2, y + dy + (0 if dy < 0 else size * .7), t, at + dur * .8, c, size)]


def axis(x0, x1, y, ticks, at, t=None, below=True):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def person(x, y, h, at, c=SKIN, fx="rise", **kw):
    e = I.person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    e.update(kw)
    return e


def seated(x, y, h, at, c=SKIN, stool=True, face=1):
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


def balance(cx, py, L, base_y, at, left=None, right=None, drop=170, pan=210, c=BONE):
    ends = [(cx - L / 2, py), (cx + L / 2, py)]
    out = [rect(cx - 80, base_y - 12, 160, 16, "#5a4836", "#8c7152", 1.5, 4, at), ln([(cx, base_y - 8), (cx, py)], at, "#8c7152", 9, draw=False),
           ln(ends, at, c, 6, draw=False), dot(cx, py, 11, GOLD, round(at, 2), None)]
    for (ex, ey), stuff in zip(ends, (left, right)):
        fy = ey + drop
        out += [ln([(ex, ey), (ex - pan / 2 + 10, fy)], at, MUTED, 1.6, draw=False), ln([(ex, ey), (ex + pan / 2 - 10, fy)], at, MUTED, 1.6, draw=False),
                poly([(ex - pan / 2, fy), (ex + pan / 2, fy), (ex + pan / 2 - 18, fy + 16), (ex - pan / 2 + 18, fy + 16)], "#6b5a48", "#cbb79a", 1.5, at)]
        if stuff:
            out += stuff(round(ex, 1), round(fy, 1))
    return out


def glyphs(x, y, w, h, at, rows=6, cols=8, c=CREAM, sw=2.2, kind=None, seed=1, op=None, **kw):
    """Running script as strokes (kit.js EL.glyphs): squiggles by default, 'latin' bars, 'cuneiform' wedges."""
    e = {"k": "glyphs", "x": round(x, 1), "y": round(y, 1), "w": round(w, 1), "h": round(h, 1), "rows": rows, "cols": cols, "c": c, "sw": sw,
         "seed": seed, "in": round(at, 2)}
    if kind:
        e["kind"] = kind
    if op is not None:
        e["op"] = op
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


# ================================================================== Greek book-hand capitals as strokes (cap height 14, baseline 0)
def _arc(cx, cy, rx, ry, a0, a1, n=10):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


_LUNATE = _arc(6.2, -7, 6.0, 7.0, -55, -305, 12)                 # the C of epsilon and of the lunate sigma
GK = {
    "Α": (12.5, [[(0, 0), (6, -14), (12, 0)], [(2.8, -5.4), (9.4, -5.4)]], False),
    "Δ": (12.5, [[(0, 0), (6, -14), (12, 0), (0, 0)]], False),
    "Ε": (10.5, [_LUNATE, [(1.2, -7), (7.4, -7)]], True),
    "Η": (12.0, [[(0, 0), (0, -14)], [(11, 0), (11, -14)], [(0, -7), (11, -7)]], False),
    "Θ": (12.5, [E(6, -7, 5.8, 7, 16) + [E(6, -7, 5.8, 7, 16)[0]], [(1.6, -7), (10.4, -7)]], True),
    "Ι": (4.5, [[(2, 0), (2, -14)]], False),
    "Κ": (11.5, [[(0, 0), (0, -14)], [(10, -14), (0.4, -6)], [(3.4, -8.6), (11, 0)]], False),
    "Λ": (12.5, [[(0, 0), (6, -14), (12, 0)]], False),
    "Μ": (15.0, [[(0, 0), (1.2, -14), (7, -4), (12.8, -14), (14, 0)]], False),
    "Ν": (12.0, [[(0, 0), (0, -14), (11, 0), (11, -14)]], False),
    "Ο": (12.5, [E(6, -7, 5.8, 7, 16) + [E(6, -7, 5.8, 7, 16)[0]]], True),
    "Π": (13.0, [[(1, 0), (1, -14)], [(11, 0), (11, -14)], [(-.4, -14), (12.4, -14)]], False),
    "Ρ": (11.0, [[(0, 3.5), (0, -14)], [(0, -14), (6, -14), (9.6, -11.6), (9.2, -8.6), (6, -7), (0, -7)]], True),
    "Σ": (10.5, [_LUNATE], True),
    "Υ": (12.5, [[(0, -14), (6, -6), (12, -14)], [(6, -6), (6, 0)]], False),
    "Φ": (13.5, [[(6.6, 4), (6.6, -17)], E(6.6, -7, 6.4, 5.4, 16) + [E(6.6, -7, 6.4, 5.4, 16)[0]]], True),
    "Ω": (15.0, [[(1.2, -12), (0, -6), (1.4, -1.4), (4, 0), (6.6, -2), (7.4, -6)], [(7.4, -6), (8.2, -2), (10.8, 0), (13.4, -1.4), (14.8, -6), (13.6, -12)]], True),
    " ": (7.0, [], False),
}


def gwidth(text, s=1.0, gap=2.2):
    return sum(GK[ch][0] + gap for ch in text) * s - gap * s


def gword(x, y, text, s=2.0, at=0, c=CREAM, w=3, dt=.12, fx="draw", dur=.3, op=None, style="known", a="start", gap=2.2, dashed=(), bar=False):
    """A Greek word in book-hand capitals at (x, baseline y), cap height 14*s, one letter every dt seconds.
    dashed: indices of letters drawn dashed (letters restored by the editors). bar: a stroke over the word (a numeral)."""
    tw = gwidth(text, s, gap)
    cx = x - tw / 2 if a == "middle" else (x - tw if a == "end" else x)
    x0 = cx
    out, k = [], 0
    for i, ch in enumerate(text):
        adv, strokes, curve = GK[ch]
        st = "inferred" if i in dashed else style
        for p in strokes:
            e = {"k": "line", "p": R([(cx + px * s, y + py * s) for px, py in p]), "c": c, "w": w, "curve": curve and len(p) > 2, "in": round(at + dt * k, 2), "style": st}
            if fx:
                e.update(fx=fx, dur=dur)
            if op is not None:
                e.update(op=op, keepop=True)
            out.append(e)
        if ch != " ":
            k += 1
        cx += (adv + gap) * s
    if bar:
        out.append(ln([(x0 - 2 * s, y - 17.5 * s), (x0 + tw + 2 * s, y - 17.5 * s)], at + dt * k, c, w, draw=True, dur=.3))
    return out


# ================================================================== the carbonised roll
def lumpy(x0, x1, y, amp, n, seed, phase=0.0):
    """An irregular edge from x0 to x1 around y (blisters and dents of a charred surface)."""
    r = random.Random(seed)
    out = []
    for k in range(n + 1):
        t = k / n
        out.append((x0 + (x1 - x0) * t, y + amp * (math.sin(t * 11.0 + phase) * .45 + r.uniform(-.55, .55))))
    return out


def roll_side(x0, x1, cy, H, at=-1, seed=3, fx=None, rim=True, end=True, cracks=True, op=None, c=CHAR2, spiral=True, bend=.06):
    """A carbonised roll seen from the side, lying from x0 to x1 (centre line cy, thickness H): a wrinkled black body with a
    slight bend, a ragged far end where layers flake off, a dull sheen, papery striations along its length, flaky patches and
    blisters, a few cracks, a lit rim, and at its left end the cut face with the wobbly spiral of its layers."""
    r = random.Random(seed)
    L = x1 - x0
    O = (lambda v: v) if op is None else (lambda v: v * op)
    n = max(12, int(L / 22))
    xa, xb = x0 + H * .1, x1 - H * .14
    yb = lambda t: -H * bend * math.sin(math.pi * t)
    top, bot = [], []
    for k in range(n + 1):
        t = k / n
        x = xa + (xb - xa) * t
        top.append((x, cy - H / 2 + yb(t) + H * (.025 * math.sin(t * 9 + seed) + .014 * math.sin(t * 37 + 2 * seed) + r.uniform(-.028, .028))))
        bot.append((x, cy + H / 2 + yb(t) + H * (.022 * math.sin(t * 7 + seed) + .012 * math.sin(t * 41) + r.uniform(-.025, .025))))
    rag = []                                                         # the ragged far end: layers that stick out and flake
    for k in range(9):
        t = k / 8
        y = cy - H / 2 + H * t
        rag.append((xb + H * (.06 + .1 * math.sin(t * math.pi)) + H * r.uniform(-.05, .07), y))
    body = top + rag + list(reversed(bot))
    out = [poly(E((x0 + x1) / 2, cy + H * .64, L * .55, H * .15, 30), "rgba(0,0,0,.5)", at=at, op=O(.55))]
    out.append(poly(body, c, "rgba(255,236,206,.10)", 1, at, fx=fx, op=op, curve=True))
    band = [(px, py + H * .13) for px, py in top[1:-1]] + [(px, py + H * .3) for px, py in reversed(top[1:-1])]
    out.append(poly(band, "#4b4037", at=at, op=O(.32), curve=True))
    for j in range(6):                                               # papery striations along the length
        y0 = -.34 + .13 * j + r.uniform(-.03, .03)
        t0, t1 = r.uniform(0, .3), r.uniform(.6, 1.0)
        pts = [(xa + (xb - xa) * t, cy + yb(t) + H * (y0 + .02 * math.sin(t * 17 + j))) for t in [t0 + (t1 - t0) * q / 10 for q in range(11)]]
        out.append(ln(pts, at, "#5d4d40" if j % 2 else "#0d0a08", 1.4, draw=False, curve=True, op=O(.55)))
    for k in range(int(L / 80)):                                     # flaky patches where an outer layer has peeled
        bx = xa + r.uniform(.05, .92) * (xb - xa)
        by = cy + yb((bx - xa) / (xb - xa)) + r.uniform(-H * .3, H * .3)
        w, h = r.uniform(14, 30), r.uniform(6, 12)
        out.append(poly([(bx - w, by), (bx - w * .4, by - h), (bx + w * .6, by - h * .8), (bx + w, by + h * .2), (bx + w * .2, by + h)], "#2c231d",
                        "rgba(170,140,110,.35)", 1, at, op=op))
    if cracks:
        for k in range(int(L / 200)):
            sx = xa + r.uniform(.08, .9) * (xb - xa)
            t = (sx - xa) / (xb - xa)
            pts = [(sx, cy + yb(t) - H * .46)]
            for j in range(2):
                pts.append((pts[-1][0] + r.uniform(-9, 9), pts[-1][1] + H * .24))
            out.append(ln(pts, at, "#060403", 1.6, draw=False, op=O(.75)))
    if rim:
        out.append(ln([(px, py + 2) for px, py in top[1:-1]], at, "#a0866a", 2.2, draw=False, op=O(.6), curve=True))
    if end:                                                          # the cut face: an ellipse with the wobbly spiral of layers
        ex, rx, ry = xa, H * .22, H / 2
        out.append(poly([(ex + rx * math.cos(a) * (1 + .05 * math.sin(5 * a)), cy + ry * math.sin(a) * (1 + .04 * math.cos(7 * a)))
                         for a in [2 * math.pi * k / 30 for k in range(30)]], "#2a211b", "rgba(200,170,140,.5)", 1.5, at, op=op, curve=True))
        if spiral:
            sp = []
            for k in range(160):
                t = k / 159
                a = t * 10 * 2 * math.pi
                w = 1 + .07 * math.sin(a * 2.3 + seed) + .04 * math.sin(a * 5.1)
                sp.append((ex + rx * .9 * t * w * math.cos(a), cy + ry * .9 * t * w * math.sin(a)))
            out.append(ln(sp, at, "#9a8470", 1.1, draw=False, op=O(.85), curve=True))
            out.append(poly(E(ex, cy, rx * .12, ry * .1, 10), "#0d0a08", at=at, op=op))
    return out


def roll_end(cx, cy, r, at, turns=7, c=CHAR2, line="#8a7360", fx="pop", op=None):
    """A roll seen end on: a dark disc with the spiral of its layers."""
    out = [circ(cx, cy, r, c, "rgba(200,170,140,.4)", 1.5, at, fx=fx, op=op)]
    sp = []
    n = turns * 18
    for k in range(n + 1):
        t = k / n
        a = t * turns * 2 * math.pi
        sp.append((cx + r * .9 * t * math.cos(a), cy + r * .9 * t * math.sin(a)))
    out.append(ln(sp, at, line, 1.1, draw=False, curve=True, op=.9 if op is None else op))
    return out


def roll_upright(cx, base, H, D, at, c=CHAR2, fx=None, op=None, style="known", edge="rgba(255,236,206,.18)"):
    """A roll standing on end: a lumpy black cylinder H tall, D across, its top an ellipse."""
    r = random.Random(int(cx + H))
    left = [(cx - D / 2 + r.uniform(-2, 2), base - H * t) for t in [k / 8 for k in range(9)]]
    right = [(cx + D / 2 + r.uniform(-2, 2), base - H * t) for t in [k / 8 for k in range(8, -1, -1)]]
    out = [poly(left + right, c, edge, 1.2, at, fx=fx, op=op, style=style)]
    out.append(poly(E(cx, base - H, D / 2, D * .2, 20), "#2e241c", "rgba(200,170,140,.4)", 1.2, at, fx=fx, op=op, style=style))
    out.append(ln([(cx - D * .22, base - H * .95), (cx - D * .25, base - H * .05)], at, CHAR_E, 2, draw=False, op=.5))
    return out


def strip(x0, x1, y0, h, at, ncols, step, c=SHEET, ink=CREAM, top_lost=0.0, edge=SHEET_E, seed=5, colw=.72, rows=6, op_ink=None):
    """A flattened layer of papyrus from x0 to x1 (top y0, height h) whose columns of writing appear one after another.
    top_lost: the fraction of the height lost at the top (drawn as dashed empty boxes)."""
    out = [rect(x0, y0, x1 - x0, h, c, edge, 1.5, 4, at)]
    pitch = (x1 - x0) / ncols
    for k in range(ncols):
        cx0 = x0 + pitch * k + pitch * (1 - colw) / 2
        cw = pitch * colw
        yy0 = y0 + h * (.08 + top_lost)
        hh = h * (.84 - top_lost)
        if top_lost:
            out.append(rect(cx0, y0 + h * .08, cw, h * top_lost - 6, "none", "rgba(233,220,203,.35)", 1.4, 3, at + .2 + step * k, style="inferred"))
        out.append(glyphs(cx0, yy0, cw, hh, at + .3 + step * k, rows=rows, cols=max(3, int(cw / 11)), c=ink, sw=1.8, seed=seed + k, op=op_ink))
    return out


def lamp_glow(x, y, r, at, op=.35):
    return [gl(x, y, r, at, op, "lamp"), gl(x, y, r * .45, at, op * .9, "lamp")]


# ================================================================== cold open
HERO = (700, 1520, 440, 180)          # the hero roll: x0, x1, centre line, thickness (about 20 cm on the ruler: 41 units a cm)


def cloth(y0, at=-1, c="#2a1a17"):
    """A dark velvet cloth under the roll, its top edge softly folded."""
    edge = [(x, y0 + 8 * math.sin(x / 140.0) + 5 * math.sin(x / 47.0)) for x in range(-40, 1840, 60)]
    return [poly(edge + [(1840, 1040), (-40, 1040)], c, at=at), ln(edge, at, "rgba(255,226,190,.10)", 2, draw=False, curve=True)]


def ruler(x0, x1, y, cm, at=-1):
    """A museum ruler in centimetres under the roll (numbers every 10 cm)."""
    u = (x1 - x0) / cm
    out = [rect(x0, y, x1 - x0, 30, "#d8c8a2", "#8a7a5a", 1, 3, at)]
    for k in range(cm + 1):
        h = 16 if k % 5 == 0 else 9
        out.append(ln([(x0 + k * u, y), (x0 + k * u, y + h)], at, "#4a3c2a", 1.6, draw=False))
    for k in (0, 10, 20):
        out.append(lab(x0 + k * u, y + 58, str(k), at, "#cbbca8", 24))
    out.append(lab(x1 + 26, y + 22, "cm", at, "#cbbca8", 24, "start"))
    return out


def s1():
    """HERO: a carbonised roll on a dark cloth under a museum lamp, a ruler in centimetres; a book; about 2,000 years; it crumbles."""
    x0, x1, cy, H = HERO
    tb, ty, tc = T("s1", "book"), T("s1", "two thousand years"), T("s1", "crumbles")
    els = lamp_glow(1110, 380, 640, -1, .30) + cloth(560) + [gl(1110, 600, 520, -1, .18, "lamp")]
    els += roll_side(x0, x1, cy, H, -1, seed=11)
    els += ruler(x0 + 14, x0 + 14 + 20 * 40, 600, 20)
    els += [ln([(680, cy), (590, cy)], tb, GOLD, 2, dur=.4), lab(575, cy + 14, "a book", tb + .2, GOLD, 46, "end", st="serif")]
    els += chip(1110, 700, "about 2,000 years", AMBER, ty, 26)
    r = random.Random(4)
    path = [(x1 - 10, cy - 20), (x1 + 14, cy + 30), (x1 + 34, cy + 70), (x1 + 50, cy + 104), (x1 + 62, cy + 128)]
    for k, (fx_, fy_) in enumerate(path):                                 # flakes break off the ragged end and fall to the cloth
        rx_, ry_ = r.uniform(12, 18), r.uniform(7, 11)
        els.append(poly([(fx_ - rx_, fy_), (fx_ - rx_ * .3, fy_ - ry_), (fx_ + rx_, fy_ - ry_ * .4), (fx_ + rx_ * .6, fy_ + ry_), (fx_ - rx_ * .5, fy_ + ry_ * .8)],
                        CHAR2, "rgba(200,170,140,.45)", 1.2, tc + .16 * k, fx="pop"))
    els += [poly(E(x1 + 70, 574, 46, 9, 16), "#2a211b", at=tc + .8, fx="pop", op=.9)]
    els += [dot(round(x1 + 30 + 8 * k + r.uniform(-4, 4), 1), round(568 + r.uniform(-7, 5), 1), round(r.uniform(2, 4), 1), "#4a3c31", round(tc + .8 + .03 * k, 2))
            for k in range(16)]
    els += [lab(x1 + 74, 520, "it crumbles", tc + .5, RED, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s2_add():
    """X-ray light over the roll: a few scan lines, the layers inside seen through, a few gold letters along one layer, a question."""
    x0, x1, cy, H = HERO
    els = [rect(x0 + 10, cy - H / 2 - 16, x1 - x0 - 20, H + 32, "rgba(159,208,255,.06)", "none", 0, 14, .2)]
    els += [ln([(x0 + 60 + 100 * k, cy - H / 2 - 30), (x0 + 60 + 100 * k, cy + H / 2 + 30)], .3 + .12 * k, BLUE, 1.4, dur=.3, op=.32) for k in range(8)]
    els += [gl((x0 + x1) / 2, cy, 400, .4, .3, "scan")]
    for j in range(6):                                                   # the layers inside, seen through
        yy = cy - H * .36 + j * H * .145
        els.append(ln([(x0 + 50 + 38 * k, yy + 5 * math.sin(k * .8 + j) - H * .05 * math.sin(math.pi * k / 20)) for k in range(21)], .9 + .08 * j, "#cfe6ff", 1.3,
                      dur=.6, curve=True, op=.5))
    els += gword(x0 + 250, cy + 10, "ΠΟΡΦΥΡΑΣ", 1.5, 1.7, AU, 2.4, dt=.07, dur=.2)
    els += [gl(x0 + 350, cy, 140, 1.7, .45, "lamp")]
    els += qmark(1110, 300, 2.3, 90)
    return els


def s3():
    """Dusk over the Bay of Naples: Vesuvius erupting at the right (a billowing column and its cloud spreading downwind, ash
    falling), the villa on the shore, a window into its library."""
    tv, tl, to = T("s3", "Vesuvius"), T("s3", "whole library"), T("s3", "only library")
    els = [{"k": "water", "y": 610, "h": 420, "x0": -100, "x1": 1100, "op": .85, "in": -1}]
    cone = [(880, 700), (1040, 560), (1180, 400), (1270, 300), (1300, 282), (1330, 296), (1362, 284), (1400, 310), (1500, 420), (1640, 570), (1800, 700)]
    els += [poly(cone + [(1800, 1040), (880, 1040)], "#2a2129", "rgba(255,200,170,.3)", 1.5, -1, curve=True)]
    r = random.Random(13)
    puffs = []
    for k in range(9):                                                   # the column: puffs widening as they rise
        t = k / 8
        puffs.append((1330 + 18 * math.sin(k * 1.7) + 30 * t, 270 - 190 * t, 26 + 34 * t))
    for k in range(16):                                                  # the cloud spreading downwind at the top
        t = k / 15
        puffs.append((1180 + 500 * t + r.uniform(-20, 20), 92 + 26 * math.sin(t * 7) + r.uniform(-12, 12) + 30 * t, 46 + 24 * math.sin(t * 3.1) + r.uniform(0, 14)))
    for k, (x, y, rr) in enumerate(puffs):
        els += [circ(x, y, rr, "#4c4243", "none", 0, .15 + .03 * k, fx="pop", op=.96)]
    for k, (x, y, rr) in enumerate(puffs):
        els += [circ(x - rr * .22, y - rr * .28, rr * .6, "#62575a", at=.25 + .03 * k, fx="pop", op=.5)]
    els += [gl(1330, 290, 180, .3, .62, "fire"), gl(1330, 250, 90, .3, .5, "fire"), gl(1400, 150, 260, .5, .18, "fire")]
    els += [dot(round(r.uniform(1150, 1700), 1), round(r.uniform(170, 470), 1), round(r.uniform(2, 3.4), 1), "#a89a96", round(.8 + .02 * k, 2), op=.75) for k in range(60)]
    shore = [(-100, 640), (200, 620), (520, 612), (800, 622), (900, 650), (1000, 700), (1000, 1040), (-100, 1040)]
    els += [poly(shore, "#2f2620", "rgba(255,226,190,.3)", 1.2, -1, curve=True)]
    els += [rect(240, 566, 600, 40, "#5a4a3c", "rgba(255,226,190,.4)", 1.2, 2, -1), poly([(230, 568), (850, 568), (820, 548), (260, 548)], "#7a5a40", at=-1)]
    els += [ln([(262 + 24 * k, 572), (262 + 24 * k, 604)], -1, "#cbb08a", 3, draw=False) for k in range(24)]
    els += [gl(330 + 120 * k, 590, 40, .4 + .15 * k, .7, "lamp") for k in range(5)]
    mx, my, mr = 540, 330, 130                                           # a window into the library room
    els += [circ(mx, my, mr, "#1d1611", "rgba(255,226,190,.55)", 2.5, tl, fx="pop"), ln([(mx + 30, my + mr), (560, 556)], tl, "rgba(255,226,190,.5)", 1.6, dur=.4)]
    for row in range(3):
        y = my - 70 + row * 62
        els.append(rect(mx - 100, y + 40, 200, 8, WOOD, at=tl + .1, fx="pop"))
        els += [circ(mx - 84 + 21 * j, y + 26, 9, PAP_D, "#8a6a3e", 1, tl + .2 + .02 * (row * 9 + j), fx="pop") for j in range(9) if (j + row) % 4 != 3]
    els += [lab(mx, my + mr + 46, "a library", tl + .4, GOLD, 34, st="serif")]
    els += chip(mx, my - mr - 34, "the only one left", AMBER, to, 26)
    els += [lab(1330, 650, "Vesuvius, 79 CE", tv, "#ffb09a", 30)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def s4():
    """2026: a small black core unrolls into a long strip whose 22 columns write themselves; read end to end, never opened."""
    td, ts, te, tn = T("s4", "twenty twenty-six"), T("s4", "what is left"), T("s4", "beginning to end"), T("s4", "without anyone")
    els = [gl(230, 450, 200, .1, .3, "lamp")] + roll_end(230, 450, 64, -1, turns=9)
    els += [ln([(300, 450), (360, 450)], ts, GOLD, 3, "claimed", .3), rect(370, 370, 1280, 170, "rgba(43,34,27,.5)", "rgba(78,63,50,.8)", 1.5, 4, .4, style="inferred")]
    els += strip(370, 1650, 370, 170, ts + .2, 22, .16, top_lost=.48, seed=21)
    els += chip(1010, 290, "2026", GOLD, td, 30)
    els += [lab(1010, 610, "read end to end", te, GOLD, 40, st="ital"), lab(1010, 672, "without opening it", tn, BONE, 30)]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


# ================================================================== 1. Books of charcoal
VN = View(13.62, 15.02, 40.5, 40.95, (90, 130, 1600, 660))
BAY_LAND = [(14.02, 41.05), (14.035, 40.92), (14.045, 40.87), (14.055, 40.835), (14.07, 40.80), (14.087, 40.776), (14.098, 40.792), (14.112, 40.812),
            (14.135, 40.822), (14.163, 40.809), (14.188, 40.797), (14.205, 40.81), (14.228, 40.83), (14.255, 40.838), (14.29, 40.84), (14.315, 40.826),
            (14.335, 40.813), (14.348, 40.805), (14.37, 40.788), (14.40, 40.772), (14.43, 40.757), (14.455, 40.742), (14.475, 40.722), (14.483, 40.70),
            (14.462, 40.679), (14.432, 40.663), (14.405, 40.645), (14.378, 40.63), (14.352, 40.613), (14.335, 40.59), (14.325, 40.573), (14.345, 40.578),
            (14.38, 40.593), (14.42, 40.607), (14.46, 40.62), (14.49, 40.628), (14.53, 40.632), (14.58, 40.633), (14.62, 40.64), (14.67, 40.652),
            (14.72, 40.665), (14.765, 40.675), (14.82, 40.643), (14.88, 40.597), (14.94, 40.55), (15.0, 40.505), (15.1, 40.42), (15.1, 41.05)]
BAY_ISLES = [[(13.86, 40.73), (13.875, 40.75), (13.91, 40.762), (13.95, 40.755), (13.965, 40.735), (13.955, 40.71), (13.92, 40.70), (13.88, 40.705)],
             [(14.005, 40.765), (14.02, 40.772), (14.033, 40.762), (14.022, 40.752), (14.008, 40.755)],
             [(14.195, 40.553), (14.21, 40.562), (14.235, 40.56), (14.255, 40.556), (14.265, 40.548), (14.245, 40.54), (14.215, 40.542)]]


def s6():
    """The Bay of Naples (coastline drawn by hand, schematic): Naples, Vesuvius, Herculaneum, Pompeii; a well at the villa site,
    1750, shown in a round window, and the floor of coloured marble it hit."""
    v = VN
    tw, tm = T("s6", "digging a well"), T("s6", "coloured marble")
    P = lambda lo, la: v.p(lo, la)
    nx, ny = P(14.25, 40.85)
    vx, vy = P(14.426, 40.821)
    hx, hy = P(14.348, 40.806)
    px, py = P(14.485, 40.749)
    bx, by = P(14.31, 40.70)
    els = [poly([P(lo, la) for lo, la in BAY_LAND], "#3a2f24", "#c9ad85", 1.8, -1, curve=True)]
    els += [poly([P(lo, la) for lo, la in isle], "#3a2f24", "#c9ad85", 1.6, -1, curve=True) for isle in BAY_ISLES]
    els += [lab(bx, by, "Bay of Naples", .3, "#9fd0ff", 36, st="ital"),
            {"k": "pin", "x": nx, "y": ny, "t": "Naples", "c": BONE, "in": .6, "a": "end", "lx": -20, "ly": -10},
            poly([(vx - 34, vy + 22), (vx - 6, vy - 26), (vx + 6, vy - 26), (vx + 34, vy + 22)], "#c0503a", "#ffb09a", 1.5, .9, fx="pop"),
            lab(vx + 46, vy - 2, "Vesuvius", 1.0, "#ffb09a", 30, "start"),
            {"k": "pin", "x": hx, "y": hy, "t": "Herculaneum", "c": GOLD, "in": 1.3, "a": "start", "lx": 16, "ly": 40},
            {"k": "pin", "x": px, "y": py, "t": "Pompeii", "c": BONE, "in": 1.7, "a": "start", "lx": 18, "ly": 30},
            {"k": "scale", "x": 140, "y": 740, "w": round(v.km(5), 1), "t": "5 km", "in": .4}]
    cx, cy, cr = P(14.0, 40.6)[0], P(14.0, 40.6)[1], 92                # a round window on the well at the villa site
    els += [ln([(hx - 6, hy + 6), (cx + cr * .7, cy - cr * .7)], tw, GOLD, 1.8, dur=.5), circ(cx, cy, cr, "#1d1611", GOLD, 2.5, tw + .2, fx="pop")]
    els += [rect(cx - 12, cy - 40, 24, 86, "#120e0b", "rgba(255,226,190,.4)", 1.2, 0, tw + .4, fx="fill"),
            ln([(cx - 34, cy - 40), (cx - 34, cy - 74)], tw + .3, "#c9a87a", 4, draw=False), ln([(cx + 34, cy - 40), (cx + 34, cy - 74)], tw + .3, "#c9a87a", 4, draw=False),
            ln([(cx - 42, cy - 74), (cx + 42, cy - 74)], tw + .35, "#c9a87a", 5, draw=False), ln([(cx, cy - 74), (cx, cy + 36)], tw + .5, BONE, 1.4, dur=.6)]
    els += chip(cx, cy - cr - 34, "1750", GOLD, tw + .3, 26) + [lab(cx, cy + cr + 44, "a well", tw + .5, GOLD, 30)]
    for k in range(9):                                                    # the floor of coloured marble at its bottom
        c = ["#b0503a", "#6f9a6a", "#efe6d6"][(k + k // 3) % 3]
        els.append(rect(cx - 66 + 15 * k, cy + 46, 14, 14, c, "rgba(0,0,0,.3)", 1, 1, tm + .04 * k, fx="pop"))
    els += [gl(cx, cy + 52, 70, tm, .55, "lamp")]
    return {"base": "map", "cam": CAM, "els": els}


SEC_G, SEC_F, SEC_M = 200, 600, 20          # the section of s7: ground surface, the villa's floor, units a metre (20 m of rock)


def pumice(x0, x1, y0, y1, n, seed, at=-1):
    """Specks of pumice and lapilli in a volcanic deposit."""
    r = random.Random(seed)
    return [dot(round(r.uniform(x0, x1), 1), round(r.uniform(y0, y1), 1), round(r.uniform(1.5, 4), 1), r.choice(["#8a8278", "#5a544c", "#a89c8c"]), at, None, .7)
            for _ in range(n)]


def town(x0, x1, g, at=-1, seed=2):
    """Today's town on the surface: small houses and trees in silhouette."""
    r = random.Random(seed)
    out, x = [], x0
    while x < x1:
        w, h = r.uniform(40, 70), r.uniform(26, 52)
        out += [rect(x, g - h, w, h, "#2c2530", "rgba(255,226,190,.25)", 1, 1, at), poly([(x - 4, g - h), (x + w / 2, g - h - 16), (x + w + 4, g - h)], "#3a2f38", at=at)]
        if r.random() < .5:
            out.append(rect(x + w * .3, g - h * .6, 8, 10, "#ffd89a", at=at, op=.6))
        x += w + r.uniform(8, 26)
        if r.random() < .35:
            out += [ln([(x, g), (x, g - 22)], at, "#2a2318", 3, draw=False), circ(x, g - 30, 12, "#2d3326", at=at)]
            x += 20
    return out


def villa_rooms(x0, x1, floor, at, c=STONE, step=.05, wall_h=60):
    """The villa's rooms in section on its floor: wall stubs, a colonnade, a doorway, and the marble floor."""
    out = []
    for k in range(int((x1 - x0) / 18)):
        col = ["#b0503a", "#6f9a6a", "#efe6d6", "#c9a87a"][k % 4]
        out.append(rect(x0 + 18 * k, floor - 6, 17, 8, col, at=at + step * .2 * k, fx="pop"))
    walls = [x0 + 20, x0 + (x1 - x0) * .22, x0 + (x1 - x0) * .4, x0 + (x1 - x0) * .78, x1 - 20]
    for k, wx in enumerate(walls):
        out.append(rect(wx - 5, floor - wall_h, 10, wall_h - 6, c, "rgba(0,0,0,.3)", 1, 1, at + step * k, fx="rise"))
    cx0, cx1 = x0 + (x1 - x0) * .44, x0 + (x1 - x0) * .74
    for k in range(7):
        xx = cx0 + (cx1 - cx0) * k / 6
        out += [rect(xx - 4, floor - wall_h + 6, 8, wall_h - 12, MARBLE, at=at + .3 + step * k, fx="rise"),
                rect(xx - 7, floor - wall_h, 14, 6, MARBLE, at=at + .3 + step * k, fx="rise")]
    out.append(rect(walls[1] + 30, floor - wall_h + 18, 34, wall_h - 24, "#1a1410", c, 1.5, 2, at + .4))
    return out


def s7():
    """The ground at the villa in section (20 units a metre): today's town on top, about 20 m of volcanic rock, the villa's floor
    and rooms at the bottom, the well that reached it."""
    tv, t20, th = T("s7", "Roman villa"), T("s7", "twenty metres"), T("s7", "Herculaneum")
    g, f = SEC_G, SEC_F
    layers = [{"d": 0, "c": "#4a443e", "t": ""}, {"d": 90, "c": "#403b36", "t": ""}, {"d": 200, "c": "#4a4239", "t": ""},
              {"d": 300, "c": "#3c3732", "t": ""}, {"d": f - g, "c": "#2a231d", "t": ""}]
    els = pumice(80, 1700, g + 10, f - 10, 160, 3) + town(880, 1680, g) + [person(330, g, 34, -1), lab(330, g - 52, "a person", .3, DIM, 24)]
    wx = 700                                                             # the well shaft, the digger, rope and bucket
    els += [rect(wx - 16, g, 32, f - g, "#140f0c", "rgba(255,226,190,.35)", 1.4, 0, .2, fx="fill"),
            ln([(wx - 32, g), (wx - 32, g - 50)], .2, "#c9a87a", 4, draw=False), ln([(wx + 32, g), (wx + 32, g - 50)], .2, "#c9a87a", 4, draw=False),
            ln([(wx - 40, g - 50), (wx + 40, g - 50)], .25, "#c9a87a", 5, draw=False), ln([(wx, g - 50), (wx, f - 28)], .5, BONE, 1.4, dur=.8),
            rect(wx - 10, f - 30, 20, 18, WOOD, "#c9a87a", 1, 2, 1.2, fx="pop"), person(wx + 62, g, 34, .3, "#d8c0a0")]
    els += villa_rooms(400, 1500, f, tv, wall_h=100)
    els += [gl(wx, f - 6, 120, tv, .55, "lamp"), lab(950, f + 56, "a Roman villa, 79 CE", tv + .6, GOLD, 32)]
    els += dimv(1590, g, f, t20, "about 20 m", GOLD, -1, 28)
    els += [arr([(1520, f + 130), (1660, f + 130)], th, BONE, 2.5, curve=False), lab(1500, f + 140, "to Herculaneum", th + .2, DIM, 26, "end")]
    return {"base": "section", "ground": g, "tod": "dusk", "layers": layers, "lx": 100, "cam": CAM, "els": els}


def oven(x, y, at, c="#cbbca8"):
    """A small kitchen oven, its dial turned to the maximum."""
    return [rect(x - 70, y - 60, 140, 120, "#3a3330", c, 2, 8, at, fx="pop"), rect(x - 50, y - 30, 100, 70, "#1a1512", c, 1.5, 6, at + .05, fx="pop"),
            gl(x, y + 5, 50, at + .1, .5, "fire"), circ(x - 40, y - 46, 8, "none", c, 2, at + .1), circ(x + 40, y - 46, 8, "none", c, 2, at + .1),
            ln([(x + 40, y - 46), (x + 46, y - 52)], at + .3, RED, 3, draw=False)]


def s8_add():
    """The current of gas and ash: the buried layers glow hot; about 350 °C; hotter than a kitchen oven."""
    tg, t350, to = T("s8", "gas and ash"), T("s8", "three hundred"), T("s8", "kitchen oven")
    g, f = SEC_G, SEC_F
    els = [rect(0, g + 4, 1778, f - g - 8, "rgba(255,110,50,.10)", at=tg, fx="pop")]
    els += [gl(240 + 260 * k, g + 150 + 70 * (k % 3), 250, tg + .12 * k, .5, "fire") for k in range(6)]
    els += [lab(300, g + 110, "gas and ash", tg + .4, "#ffb09a", 32)]
    els += chip(960, g + 120, "about 350 °C", "#ffb09a", t350, 32)
    els += oven(1260, g + 130, to) + [lab(1260, g + 236, "hotter than an oven", to + .3, BONE, 26)]
    return els


def s9():
    """The villa from above, after the 18th-century plan (schematic): the long garden court and pool, the square court, the
    atrium, rooms, the walk to the round belvedere; more than 250 m along the shore (5 units a metre)."""
    tl = T("s9", "two hundred and fifty")
    u = 5.0
    els = [{"k": "water", "y": 640, "h": 400, "op": .9, "in": -1},
           ln([(x, 640 + 6 * math.sin(x / 90.0)) for x in range(60, 1720, 40)], -1, "rgba(255,226,190,.5)", 2, draw=False, curve=True),
           lab(1500, 720, "the sea", .3, "#9fd0ff", 28, st="ital")]
    S = STONE
    fill = "rgba(201,168,122,.14)"
    els += [rect(1000, 360, 100 * u, 37 * u, fill, S, 3, 2, .3, fx="pop"), rect(1030, 390, 100 * u - 60, 37 * u - 60, "rgba(111,154,106,.18)", "rgba(201,168,122,.5)", 1.5, 2, .5),
            rect(1250 - 33 * u, 453, 66 * u, 7 * u, "#4f93b3", "#bfe6f5", 1.5, 2, .7, fx="pop"),
            rect(800, 380, 30 * u, 30 * u, fill, S, 3, 2, .9, fx="pop"), rect(820, 400, 30 * u - 40, 30 * u - 40, "rgba(111,154,106,.18)", "rgba(201,168,122,.5)", 1.5, 2, 1.0),
            rect(680, 400, 20 * u, 22 * u, fill, S, 3, 2, 1.1, fx="pop"), rect(718, 436, 24, 36, "#4f93b3", "none", 0, 2, 1.2)]
    els += [rect(500 + 30 * k, 410 + (k % 2) * 6, 28, 100, fill, S, 2, 1, 1.3 + .04 * k, fx="pop") for k in range(6)]
    els += [rect(262, 470, 238, 18, fill, S, 2, 2, 1.6, fx="pop")] + [dot(270 + 14 * k, 479, 2.6, S, round(1.7 + .02 * k, 2)) for k in range(17)]
    els += [circ(230, 479, 28, fill, S, 3, 1.9, fx="pop"), circ(230, 479, 14, "none", "rgba(201,168,122,.6)", 1.5, 2.0)]
    els += [lab(889, 600, "the villa", .6, GOLD, 36, st="serif")]
    els += dimh(202, 1500, 300, tl, "more than 250 m", GOLD, 30, -18, 1.4)
    els += [ln([(260, 760), (510, 760)], .5, BONE, 3, draw=False), ln([(260, 750), (260, 770)], .5, BONE, 2, draw=False), ln([(510, 750), (510, 770)], .5, BONE, 2, draw=False),
            lab(385, 742, "50 m", .6, BONE, 24)]
    return {"base": "plan", "north": False, "cam": CAM, "els": els}


def statue(x, y, h, at, c):
    """A small statue on its plinth."""
    return [rect(x - h * .24, y, h * .48, h * .16, "#6b5a48", at=at, fx="pop"), person(x, y, h, at, c, fx="pop")]


def s10():
    """Tunnels through hard volcanic rock by torchlight, bad air in a dead end; then about ninety statues, bronze and marble."""
    tt, tf, ta, ts = T("s10", "tunnels"), T("s10", "torchlight"), T("s10", "poisonous air"), T("s10", "ninety statues")
    rock = [(90, 190), (360, 170), (640, 186), (900, 172), (920, 440), (906, 740), (600, 760), (300, 748), (86, 760)]
    els = [poly(rock, "#2c2925", "rgba(255,226,190,.2)", 1.5, -1, curve=True)] + pumice(110, 890, 200, 730, 90, 7)
    paths = [[(110, 470), (300, 452), (500, 466), (700, 440), (890, 452)], [(300, 452), (280, 330), (310, 250)], [(500, 466), (540, 600), (470, 700)],
             [(700, 440), (750, 320), (850, 250)], [(700, 440), (750, 590), (840, 690)]]
    for k, p in enumerate(paths):
        els.append(ln(p, tt + .25 * k, "#0c0907", 34, dur=.9, curve=True))
    for k, (x, y) in enumerate([(220, 462), (420, 458), (620, 452), (820, 450), (530, 610), (770, 330)]):
        els += [gl(x, y - 6, 66, tf + .12 * k, .85, "fire"), person(x + 14, y + 14, 36, tf + .12 * k, "#d9b88f")]
    els += [circ(310, 250, 72, "rgba(143,217,176,.18)", at=ta, fx="pop"), circ(310, 250, 40, "rgba(143,217,176,.22)", at=ta + .1, fx="pop"),
            lab(310, 196, "bad air", ta + .3, GREEN, 28)]
    els += [lab(500, 800 - 20, "hard volcanic rock", .4, DIM, 26)]
    for row in range(6):
        for col in range(15):
            k = row * 15 + col
            c = "#b07d45" if (row + col) % 3 else MARBLE
            els += statue(985 + 46 * col, 250 + 82 * row, 56, ts + .012 * k, c)
    els += [lab(1307, 790 - 20, "about 90 statues", ts + 1.2, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def lump(cx, cy, L, H, at, seed, fx="pop"):
    """One charred lump: a short lumpy black cylinder with a lit rim."""
    r = random.Random(seed)
    top = lumpy(cx - L / 2, cx + L / 2, cy - H / 2, H * .12, 7, seed)
    bot = lumpy(cx + L / 2, cx - L / 2, cy + H / 2, H * .1, 7, seed + 3)
    return [poly(top + [(cx + L / 2 + H * .2, cy)] + bot + [(cx - L / 2 - H * .2, cy)], CHAR2, "rgba(200,170,140,.3)", 1.2, at, fx=fx, curve=True),
            ln([(x, y + 3) for x, y in top[1:-1]], at, CHAR_E, 1.6, draw=False, curve=True, op=.6)]


def s11():
    """A tunnel by torchlight: a heap of black lumps (1752); logs? fishing nets? then one breaks open: writing inside."""
    t52, tlog, tnet, tb, tw = T("s11", "seventeen fifty-two"), T("s11", "burnt logs"), T("s11", "fishing nets"), T("s11", "broke open"), T("s11", "writing")
    ceil = [(-40, -40), (1820, -40), (1820, 150)] + [(x, 150 + 40 * math.sin(x / 170.0) + 18 * math.sin(x / 53.0)) for x in range(1820, -60, -60)]
    floor = [(x, 650 + 14 * math.sin(x / 140.0) + 8 * math.sin(x / 41.0)) for x in range(-60, 1840, 60)] + [(1840, 1040), (-60, 1040)]
    els = [poly(ceil, "#2a2622", "rgba(255,226,190,.18)", 1.2, -1, curve=True), poly(floor, "#2e2620", "rgba(255,226,190,.2)", 1.2, -1, curve=True),
           gl(170, 430, 300, -1, .55, "fire"), gl(170, 430, 90, -1, .8, "fire"), ln([(150, 470), (170, 412)], -1, WOOD, 6, draw=False)]
    els += pumice(0, 1778, 0, 170, 40, 4) + pumice(0, 1778, 670, 1000, 40, 5)
    r = random.Random(12)
    spots = [(560, 630), (650, 642), (740, 634), (830, 646), (600, 596), (700, 590), (790, 600), (650, 558), (745, 556), (880, 620), (520, 650), (920, 652)]
    for k, (x, y) in enumerate(spots):
        els += lump(x, y, r.uniform(60, 96), r.uniform(26, 34), .3 + .05 * k, 30 + k)
    els += chip(889, 250, "1752", GOLD, t52, 30)
    logx, logy = 520, 380                                                  # the guesses, in dotted lilac
    els += [rect(logx - 130, logy - 34, 260, 68, "rgba(201,193,238,.06)", LILAC, 2.5, 34, tlog, style="claimed"),
            circ(logx - 130, logy, 34, "none", LILAC, 2, tlog + .1, style="claimed"), circ(logx - 130, logy, 18, "none", LILAC, 1.5, tlog + .2, style="claimed")]
    els += [ln([(logx - 90 + 40 * k, logy - 30), (logx - 70 + 40 * k, logy + 30)], tlog + .2, LILAC, 1.5, "claimed", .3) for k in range(5)]
    els += [lab(logx, logy + 76, "logs?", tlog + .3, LILAC, 30)]
    nx, ny = 1120, 380
    net = []
    for k in range(7):
        net.append(ln([(nx - 150 + 50 * k, ny - 50 + 6 * math.sin(k)), (nx - 100 + 50 * k, ny + 50)], tnet + .03 * k, LILAC, 1.6, "claimed", .3))
        net.append(ln([(nx - 100 + 50 * k, ny - 50 + 6 * math.sin(k)), (nx - 150 + 50 * k, ny + 50)], tnet + .03 * k, LILAC, 1.6, "claimed", .3))
    els += net + [ln([(nx - 160, ny - 52), (nx + 160, ny - 44)], tnet, LILAC, 2, "claimed", .4), lab(nx, ny + 92, "fishing nets?", tnet + .3, LILAC, 30)]
    sx, sy = 1360, 590                                                    # the lump that broke: two halves, layers and writing
    els += [poly(E(sx - 74, sy, 62, 38, 24), CHAR2, "rgba(200,170,140,.4)", 1.4, tb, fx="pop"),
            poly(E(sx + 74, sy + 6, 62, 38, 24), CHAR2, "rgba(200,170,140,.4)", 1.4, tb + .1, fx="pop")]
    els += roll_end(sx - 22, sy, 32, tb + .2, turns=6) + roll_end(sx + 24, sy + 6, 32, tb + .25, turns=6)
    els += [gl(sx, sy - 10, 130, tw, .6, "lamp"), glyphs(sx - 60, sy - 92, 120, 40, tw, rows=2, cols=6, c=AU, sw=2.2, seed=3)]
    els += [lab(sx, sy + 100, "writing", tw + .4, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s12():
    """Paderni's letter, Naples, 18 November 1752: 'a sort of charcoal'; a black roll crumbles to ash beside it; to London."""
    tq, tb, tl = T("s12", "a sort of charcoal"), T("s12", "so brittle"), T("s12", "to London")
    px, py, pw, ph = 230, 150, 500, 600
    els = [rect(px + 12, py + 16, pw, ph, "rgba(0,0,0,.45)", at=-1), rect(px, py, pw, ph, "#efe3c8", "#cdbb95", 1.5, 4, -1),
           lab(px + pw / 2, py + 52, "Naples, 18 November 1752", .3, INKD, 25, halo=False),
           glyphs(px + 40, py + 90, pw - 80, 230, .5, rows=9, cols=12, c="#5a4330", sw=2.0, seed=4),
           rect(px + 24, py + 352, pw - 48, 66, "rgba(242,201,142,.35)", GOLD, 2, 6, tq, fx="pop"),
           lab(px + pw / 2, py + 397, "a sort of charcoal", tq + .2, INKD, 38, st="ital", halo=False),
           glyphs(px + 40, py + 440, pw - 80, 130, tq + .5, rows=5, cols=12, c="#5a4330", sw=2.0, seed=9)]
    els += [arr([(px + pw + 10, py + 120), (860, 170), (960, 150)], tl, BONE, 2, "claimed", .8), lab(980, 160, "to London", tl + .3, BONE, 28, "start")]
    els += cloth(560, -1, "#241715") + roll_side(930, 1500, 430, 150, -1, seed=5)
    r = random.Random(9)
    path = [(1500, 400), (1522, 440), (1540, 480), (1556, 515), (1568, 545), (1578, 566)]
    for k, (fx_, fy_) in enumerate(path):
        rx_, ry_ = r.uniform(11, 17), r.uniform(6, 10)
        els.append(poly([(fx_ - rx_, fy_), (fx_ - rx_ * .3, fy_ - ry_), (fx_ + rx_, fy_ - ry_ * .4), (fx_ + rx_ * .6, fy_ + ry_), (fx_ - rx_ * .5, fy_ + ry_ * .8)],
                        CHAR2, "rgba(200,170,140,.45)", 1.2, tb + .15 * k, fx="pop"))
    els += [poly(E(1590, 578, 60, 10, 16), "#3a302a", at=tb + .9, fx="pop", op=.9)]
    els += [dot(round(1540 + 7 * k + r.uniform(-4, 4), 1), round(572 + r.uniform(-6, 4), 1), round(r.uniform(2, 3.6), 1), "#5a4e46", round(tb + .9 + .03 * k, 2))
            for k in range(16)]
    els += [lab(1560, 660, "a touch, and ash", tb + 1.2, RED, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s13():
    """About 1,800 inventory items (180 tiles of 10), many scraps of the same roll (gold links); separate books 700 to 1,100."""
    ti, ts, t7, t11 = T("s13", "eighteen hundred"), T("s13", "scraps of the same"), T("s13", "seven hundred"), T("s13", "eleven hundred")
    x0, y0, p, sz = 150, 210, 44, 38
    els = [lab(546, 180, "about 1,800 items", ti, GOLD, 32)] + qmark(1340, 700, .4, 90, LILAC)
    els += [rect(x0 + p * (k % 18), y0 + p * (k // 18), sz, sz, "none", "rgba(138,115,96,.55)", 1.2, 4, .3) for k in range(180)]
    els += [rect(x0 + p * (k % 18), y0 + p * (k // 18), sz, sz, "#3a2e25", "#8a7360", 1.2, 4, ti + .1 + .006 * k, fx="pop") for k in range(180)]
    els += [lab(546, 700, "each tile: 10 items", ti + 1.2, DIM, 24)]
    r = random.Random(3)
    for k in range(16):
        row, col = r.randint(0, 9), r.randint(0, 14)
        n = r.randint(2, 4)
        cy_ = y0 + p * row + sz / 2
        els.append(ln([(x0 + p * col + sz / 2, cy_), (x0 + p * (col + n - 1) + sz / 2, cy_)], ts + .06 * k, AU, 5, dur=.3))
        els += [dot(round(x0 + p * (col + j) + sz / 2, 1), round(cy_, 1), 5, AU, round(ts + .06 * k, 2)) for j in range(n)]
    bx, kk = 1060, 560 / 1800.0
    els += [lab(bx, 268, "inventory", ti + .4, DIM, 26, "start"), rect(bx, 290, 1800 * kk, 40, AU, "none", 0, 4, ti + .4, fx="pop", op=.85)]
    els += [lab(bx, 420, "separate books", t7, DIM, 26, "start"),
            rect(bx, 442, 700 * kk, 40, "rgba(232,184,122,.55)", AMBER, 2, 4, t7, fx="pop", style="inferred"),
            rect(bx + 700 * kk, 442, 400 * kk, 40, "rgba(232,184,122,.2)", AMBER, 2, 4, t11, fx="pop", style="inferred")]
    els += bracket(bx + 700 * kk, bx + 1100 * kk, 500, t11 + .2, "700 to 1,100", AMBER, True, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def bust(cx, top, s, at, c=LILAC, style="claimed"):
    """A Roman portrait bust in outline (dotted lilac: the owner is a guess)."""
    head = E(cx, top + 85 * s, 62 * s, 80 * s, 24)
    neck = [(cx - 26 * s, top + 150 * s), (cx + 26 * s, top + 150 * s), (cx + 30 * s, top + 190 * s), (cx - 30 * s, top + 190 * s)]
    body = [(cx - 130 * s, top + 300 * s), (cx - 120 * s, top + 220 * s), (cx - 60 * s, top + 186 * s), (cx + 60 * s, top + 186 * s), (cx + 120 * s, top + 220 * s),
            (cx + 130 * s, top + 300 * s)]
    fold = [(cx - 90 * s, top + 214 * s), (cx - 10 * s, top + 290 * s), (cx + 60 * s, top + 206 * s)]
    return [poly(head, "rgba(201,193,238,.07)", c, 2.5, at, style=style), poly(neck, "rgba(201,193,238,.05)", c, 2, at + .1, style=style),
            poly(body, "rgba(201,193,238,.07)", c, 2.5, at + .2, style=style, curve=True), ln(fold, at + .3, c, 2, style, .5, True),
            rect(cx - 70 * s, top + 300 * s, 140 * s, 40 * s, "rgba(201,193,238,.05)", c, 2, 3, at + .3, style=style)]


def s14():
    """Whose villa? A dotted bust 'Piso?', Caesar's father-in-law; a gold link to Philodemus' rolls ('his friend'); a good guess."""
    tp, tc, tm, tg = T("s14", "Piso"), T("s14", "father-in-law"), T("s14", "the man who wrote"), T("s14", "good guess")
    els = [gl(560, 400, 300, .1, .25, "lamp")] + bust(560, 180, 1.0, .3) + qmark(700, 250, .8, 70)
    els += [lab(560, 590, "Piso?", tp, LILAC, 46, st="serif")] + tag(560, 660, "Caesar's father-in-law", tc, LILAC, 26, "claimed")
    k = 0
    for row, n in enumerate([5, 4, 3, 2, 1]):
        for j in range(n):
            els += roll_end(1250 + (j - (n - 1) / 2) * 56, 560 - row * 50, 26, tm + .04 * k, turns=4, c="#3a2e24", line=AU)
            k += 1
    els += [lab(1250, 650, "Philodemus", tm + .5, GOLD, 34, st="serif")]
    els += [ln([(1180, 420), (1000, 300), (820, 300), (690, 360)], tm + .8, GOLD, 3, curve=True, dur=.8), lab(905, 280, "his friend", tm + 1.2, GOLD, 28)]
    els += chip(905, 760, "a good guess", LILAC, tg, 28)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== 2. Opening the unopenable
def s15():
    """One roll unrolled, to scale (130 units a metre): a thin strip of papyrus longer than ten metres beside a person, 1.7 m;
    a round window shows its columns of writing close up."""
    tl, t10 = T("s15", "one long sheet"), T("s15", "more than ten")
    u, x0, y = 120.0, 230, 450
    L = 10.5 * u
    els = [gl(889, 440, 700, .1, .15, "lamp")] + roll_end(x0 - 26, y + 15, 22, .3, turns=5)
    els += [ln([(x0, y + 15), (x0 + L, y + 15)], tl, "#5a4636", 28, dur=2.4)]
    els += [glyphs(x0 + 6 + L / 6 * k, y + 5, L / 6 - 12, 20, tl + .4 * k + .2, rows=2, cols=40, c=CREAM, sw=1.4, seed=3 + k) for k in range(6)]
    mx, my, mr = 640, 250, 110                                            # a round window on a stretch of the strip
    els += [ln([(mx + 40, my + mr - 6), (700, y)], tl + 1.0, "rgba(242,201,142,.6)", 1.6, dur=.4), circ(mx, my, mr, SHEET, GOLD, 2.5, tl + 1.0, fx="pop")]
    els += [glyphs(mx - 90 + 64 * j, my - 70, 50, 140, tl + 1.2 + .1 * j, rows=8, cols=5, c=CREAM, sw=1.8, seed=70 + j) for j in range(3)]
    els += [lab(mx + mr + 30, my - 20, "columns of writing", tl + 1.4, CREAM, 28, "start")]
    els += [lab(x0 + L / 2 + 200, y - 40, "one book, unrolled", tl + .6, GOLD, 32)]
    els += [ln([(x0, 540), (x0 + L, 540)], tl + .4, BONE, 2, dur=1.4)]
    els += [ln([(x0 + u * k, 532), (x0 + u * k, 548)], tl + .4 + .12 * k, BONE, 2, draw=False) for k in range(11)]
    els += [lab(x0, 580, "0", tl + .5, DIM, 24), lab(x0 + 5 * u, 580, "5 m", tl + 1.0, DIM, 24), lab(x0 + 10 * u, 580, "10 m", t10, GOLD, 28)]
    els += [person(x0 + L + 70, 690, 1.7 * u, .4), lab(x0 + L + 70, 730, "a person, 1.7 m", .6, DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s16():
    """The first tries: a roll sliced in half; the exposed layer copied by hand, then scraped away to reach the next."""
    ts, tc, tsc, td = T("s16", "sliced in half"), T("s16", "copied by hand"), T("s16", "scraped away"), T("s16", "you destroyed it")
    els = roll_side(150, 690, 300, 110, .2, seed=21)
    els += [ln([(150, 300), (700, 300)], ts, RED, 3, "inferred", .7), lab(420, 205, "sliced in half", ts + .3, RED, 30)]
    fx0, fy0 = 160, 450                                                  # the half-roll, its inside face exposed
    els += [poly([(fx0, fy0), (fx0 + 520, fy0), (fx0 + 540, fy0 + 60), (fx0 + 520, fy0 + 130), (fx0, fy0 + 130), (fx0 - 20, fy0 + 60)], "#3a2e25", "rgba(200,170,140,.4)", 1.5,
                 ts + .4, fx="pop")]
    els += [ln([(fx0 + 10, fy0 + 20 + 22 * j), (fx0 + 510, fy0 + 20 + 22 * j)], ts + .5, "#5a4838", 1.2, draw=False) for j in range(5)]
    els += [glyphs(fx0 + 40, fy0 + 30, 440, 70, ts + .7, rows=3, cols=18, c="#a08a70", sw=1.6, seed=7)]
    els += [rect(900, 150, 520, 380, "#efe3c8", "#cdbb95", 1.5, 4, .6, fx="pop"), glyphs(940, 200, 440, 280, tc + .3, rows=9, cols=16, c="#5a4330", sw=2.0, seed=7),
            lab(1160, 580, "copied by hand", tc + .5, BONE, 28)] + seated(1500, 520, 200, .7, SKIN, face=-1)
    els += [rect(fx0 + 60, fy0 + 10, 230, 110, "#4a3c31", "none", 0, 4, tsc, fx="pop", op=.95),
            glyphs(fx0 + 70, fy0 + 30, 210, 70, tsc + .5, rows=3, cols=9, c="#a08a70", sw=1.6, seed=31)]
    r = random.Random(5)
    els += [dot(round(fx0 + 60 + r.uniform(0, 230), 1), round(fy0 + 140 + r.uniform(0, 30), 1), round(r.uniform(2, 4), 1), "#5a4a3c", round(tsc + .2 + .02 * k, 2)) for k in range(22)]
    els += [rect(fx0 + 300, fy0 - 40, 16, 70, "#9a9a9a", "#d8d8d8", 1, 2, tsc, fx="pop"), lab(fx0 + 180, fy0 + 200, "scraped away", tsc + .3, BONE, 28)]
    els += [lab(889, 760, "read it, destroy it", td, RED, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s17():
    """Piaggio's machine (schematic): a frame with turning pegs, silk threads gummed to the back of the papyrus rising from the roll
    in its cradle, a lining as thin as onion skin; Piaggio at the side with a fine blade."""
    t53, tp, tth, tbl, tli = T("s17", "seventeen fifty-three"), T("s17", "Antonio Piaggio"), T("s17", "threads"), T("s17", "fine blade"), T("s17", "onion's")
    els = [gl(820, 420, 600, -1, .22, "lamp")]
    els += [rect(380, 640, 900, 26, WOOD, "#8a6a48", 1.5, 3, .1), rect(410, 666, 22, 120, WOOD_D, at=.1), rect(1230, 666, 22, 120, WOOD_D, at=.1),
            rect(440, 200, 22, 440, WOOD, "#8a6a48", 1.5, 2, .2), rect(1200, 200, 22, 440, WOOD, "#8a6a48", 1.5, 2, .2),
            rect(426, 186, 810, 28, WOOD, "#8a6a48", 1.5, 3, .3)]
    els += [circ(520 + 70 * k, 200, 10, "#c9a87a", "#5a4030", 1.5, .4 + .04 * k, fx="pop") for k in range(10)]
    els += [poly(E(820, 610, 190, 34, 24, 0, 180), "#4a3626", "#8a6a48", 1.5, .3)] + roll_side(670, 970, 598, 64, .2, seed=8, spiral=False)
    els += [rect(700, 300, 260, 270, SHEET, SHEET_E, 1.5, 2, .5), glyphs(718, 320, 224, 220, .7, rows=8, cols=10, c="#9a846c", sw=1.6, seed=12)]
    els += [ln([(520 + 70 * k, 210), (708 + 27 * k, 302)], tth + .05 * k, BONE, 1.2, dur=.5, op=.8) for k in range(10)]
    els += [lab(560, 270, "threads", tth + .4, BONE, 26, "end")]
    els += seated(1390, 640, 210, tp, "#7a6a5e", face=-1)
    els += [ln([(1330, 520), (1150, 552), (975, 566)], tbl, "#dcdcdc", 2.5, dur=.6), lab(1150, 600, "a fine blade", tbl + .3, BONE, 26)]
    els += [rect(700, 300, 260, 270, "rgba(239,230,214,.16)", "rgba(239,230,214,.6)", 1.5, 2, tli, fx="pop"), lab(985, 430, "a thin lining", tli + .2, PAP, 26, "start")]
    els += chip(830, 150, "1753", GOLD, t53, 28) + [lab(1390, 690, "Antonio Piaggio", tp + .3, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s18():
    """A whole year (twelve squares filling) for half of one roll; February 1755."""
    tw, th, tf = T("s18", "whole year"), T("s18", "half of one"), T("s18", "February")
    els = []
    for k in range(12):
        x, y = 210 + 96 * (k % 4), 250 + 96 * (k // 4)
        els += [rect(x, y, 84, 84, "none", "rgba(242,201,142,.5)", 2, 6, .3 + .02 * k), rect(x + 4, y + 4, 76, 76, "rgba(232,195,90,.75)", at=tw + .16 * k, fx="pop")]
    els += [lab(398, 590, "one year", tw + 1.9, GOLD, 34)]
    els += [rect(900, 400, 420, 90, SHEET, SHEET_E, 1.5, 3, .4), glyphs(915, 412, 390, 66, .6, rows=3, cols=20, c="#9a846c", sw=1.5, seed=2)]
    els += roll_end(1360, 445, 50, .5, turns=6)
    els += [rect(1410, 400, 230, 90, "rgba(255,255,255,.02)", "rgba(233,220,203,.5)", 2, 3, th, style="inferred"), lab(1525, 455, "to go", th + .3, DIM, 26)]
    els += [lab(1110, 560, "half a roll", th + .2, GOLD, 34)]
    els += chip(1110, 300, "Feb 1755", GOLD, tf, 26)
    return {"base": "dark", "cam": CAM, "els": els}


def mask(cx, cy, s, at, c=LILAC, style="claimed"):
    """A theatre mask in outline."""
    return [poly(E(cx, cy, 70 * s, 90 * s, 24), "rgba(201,193,238,.05)", c, 2.5, at, style=style),
            poly(E(cx - 26 * s, cy - 18 * s, 16 * s, 10 * s, 12), "#1a1612", c, 2, at + .1, style=style),
            poly(E(cx + 26 * s, cy - 18 * s, 16 * s, 10 * s, 12), "#1a1612", c, 2, at + .1, style=style),
            ln(_arc(cx, cy + 22 * s, 30 * s, 22 * s, 200, 340, 8), at + .2, c, 2.5, style, .4, True)]


def lyre(cx, base, s, at, c=LILAC, style="claimed", w=2.5):
    """A lyre: two curved arms, a crossbar, a sound box, strings."""
    L = [(cx - 40 * s, base), (cx - 62 * s, base - 70 * s), (cx - 46 * s, base - 140 * s), (cx - 60 * s, base - 170 * s)]
    Rr = [(cx + 40 * s, base), (cx + 62 * s, base - 70 * s), (cx + 46 * s, base - 140 * s), (cx + 60 * s, base - 170 * s)]
    out = [ln(L, at, c, w, style, .5, True), ln(Rr, at, c, w, style, .5, True), ln([(cx - 54 * s, base - 140 * s), (cx + 54 * s, base - 140 * s)], at + .2, c, w, style, .3),
           poly(E(cx, base, 46 * s, 16 * s, 16), "rgba(201,193,238,.05)" if style != "known" else "#6b4a2e", c, w, at + .1, style=style)]
    out += [ln([(cx - 18 * s + 12 * s * k, base - 4 * s), (cx - 18 * s + 12 * s * k, base - 138 * s)], at + .3, c, 1.2, style, .3) for k in range(4)]
    return out


def s19():
    """Hopes, in dotted lilac: lost poems, lost plays; the first roll out of the machine: On Music, and its claim: music
    cannot change your character (the arrow from the lyre to a person struck through)."""
    tpo, tpl, tf, tc = T("s19", "lost poems"), T("s19", "lost plays"), T("s19", "first roll"), T("s19", "cannot change")
    els = lyre(330, 470, 1.1, tpo) + [lab(330, 560, "lost poems?", tpo + .3, LILAC, 30)]
    els += mask(640, 360, 1.1, tpl) + [lab(640, 560, "lost plays?", tpl + .3, LILAC, 30)]
    els += [rect(180, 140, 640, 460, "rgba(13,11,9,.62)", at=tf, fx="pop")]
    els += [rect(960, 150, 600, 290, SHEET, SHEET_E, 1.5, 4, tf + .2, fx="pop"), glyphs(990, 175, 540, 240, tf + .4, rows=8, cols=22, c="#a89070", sw=1.6, seed=14)]
    els += tag(1260, 490, "On Music", tf + .6, GOLD, 30)
    els += lyre(1080, 690, .6, tc, AU, "known", 2)
    els += [arr([(1150, 640), (1330, 640)], tc + .2, BONE, 3, curve=False), person(1400, 700, 110, tc + .3, SKIN),
            ln([(1200, 600), (1290, 680)], tc + .6, RED, 5, dur=.3), lab(1240, 760, "music cannot change your character", tc + .5, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


VM = View(2.0, 61.0, 27.0, 47.0, (90, 120, 1600, 680))


def s20():
    """Philodemus: from Gadara (today's Jordan) to the Bay of Naples; a follower of Epicurus (calm pleasure, friends);
    44 of the 75 works identified are his."""
    tph, tga, tjo, tep, tw, th = (T("s20", "Philodemus"), T("s20", "Gadara"), T("s20", "Jordan"), T("s20", "Epicurus"), T("s20", "Of the works"),
                                 T("s20", "more than half"))
    v = VM
    gx, gy = v.p(35.68, 32.65)
    nx, ny = v.p(14.25, 40.85)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += [{"k": "pin", "x": gx, "y": gy, "t": "Gadara", "c": GOLD, "in": tga, "a": "end", "lx": -20, "ly": -14},
            lab(gx - 20, gy + 40, "today's Jordan", tjo, DIM, 24, "end"),
            {"k": "pin", "x": nx, "y": ny, "t": "Naples", "c": GOLD, "in": tph + .4, "a": "end", "lx": -18, "ly": -14}]
    els += [arr([(gx - 6, gy - 6), ((gx + nx) / 2, min(gy, ny) - 110), (nx + 10, ny + 4)], tga + .6, GOLD, 3, "claimed", 1.4)]
    els += [lab((gx + nx) / 2, min(gy, ny) - 150, "Philodemus", tph, GOLD, 44, st="serif")]
    els += [rect(1190, 150, 500, 630, "rgba(18,13,10,.88)", "rgba(255,236,206,.25)", 1.5, 16, tep - .5, fx="pop")]
    for k in range(75):
        x, y = 1230 + 28 * (k % 15), 200 + 28 * (k // 15)
        els.append(rect(x, y, 22, 22, "#3a2e25", "#6b5644", 1, 3, tw + .01 * k, fx="pop"))
        if k < 44:
            els.append(rect(x, y, 22, 22, AU, at=th + .02 * k, fx="pop"))
    els += [lab(1440, 382, "his: 44 of 75 identified", th + .9, GOLD, 28)]
    tx, ty = 1290, 560                                                    # Epicurus' garden: friends at a table under a tree
    els += [lab(1440, 450, "Epicurus' way", tep, AMBER, 30)]
    els += [ln([(tx, ty + 130), (tx, ty + 20)], tep + .1, "#5a4030", 10, draw=False), circ(tx, ty - 10, 66, "#2f4a2a", "#6f9a6a", 1.5, tep + .1, fx="pop"),
            rect(1410, ty + 80, 160, 12, WOOD, at=tep + .2, fx="pop")]
    els += seated(1400, ty + 130, 110, tep + .3, SKIN, False, 1) + seated(1580, ty + 130, 110, tep + .4, SKIN, False, -1)
    els += [person(1490, ty + 130, 100, tep + .5), lab(1440, ty + 180, "calm pleasure, friends", tep + .8, DIM, 26)]
    return {"base": "map", "cam": CAM, "els": els}


def s21():
    """The shelves, coloured by author as they are named: Philodemus (most), Epicurus, the rival Stoics, a few in Latin;
    one Latin roll slides out: a poem on the battle of Actium."""
    te, ts, tl, ta = T("s21", "Epicurus"), T("s21", "Stoics"), T("s21", "Latin"), T("s21", "Actium")
    x0, y0, cw, ch, nc, nr = 260, 170, 100, 92, 8, 6
    els = [rect(x0 - 20, y0 - 20, cw * nc + 40, ch * nr + 40, WOOD_D, WOOD, 3, 6, -1)]
    r = random.Random(8)
    cells = list(range(nc * nr))
    r.shuffle(cells)
    who = {}
    for k, c in enumerate(cells):
        who[c] = "P" if k < 28 else "E" if k < 34 else "S" if k < 39 else "L" if k < 42 else "-"
    col = {"P": AU, "E": AMBER, "S": BLUE, "L": GREEN, "-": "#4a3c31"}
    at = {"P": .4, "E": te, "S": ts, "L": tl, "-": .4}
    for c in range(nc * nr):
        cx, cy = x0 + cw * (c % nc), y0 + ch * (c // nc)
        els.append(rect(cx + 4, cy + 4, cw - 8, ch - 8, "#1a130e", "#5a4030", 1.2, 2, -1))
        for j in range(3):
            rx, ry = cx + 24 + 26 * j, cy + 48 + (6 if j == 1 else 0)
            els.append(circ(rx, ry, 12, "#3a2e24", "#6b5644", 1, -1))
            if who[c] != "-":
                els.append(circ(rx, ry, 12, col[who[c]], "rgba(0,0,0,.4)", 1, at[who[c]] + .02 * (c % 9) + .03 * j, fx="pop", op=.92))
    legend = [("Philodemus", AU, .5), ("Epicurus", AMBER, te), ("Stoics", BLUE, ts), ("Latin", GREEN, tl)]
    for k, (t, c, a) in enumerate(legend):
        els += [circ(1190, 230 + 64 * k, 13, c, at=a, fx="pop"), lab(1218, 240 + 64 * k, t, a + .1, c, 30, "start")]
    els += roll_side(1150, 1430, 610, 44, ta - .6, seed=6, c="#3a3a2a") + [gl(1290, 610, 120, ta - .4, .4, "lamp")]
    gx, gy = 1520, 560                                                    # a war galley, for the poem on Actium
    els += [poly([(gx - 90, gy), (gx + 80, gy), (gx + 100, gy - 22), (gx + 60, gy + 18), (gx - 70, gy + 18)], "#5a4030", GOLD, 1.5, ta, fx="pop"),
            ln([(gx, gy), (gx, gy - 80)], ta + .1, GOLD, 2, draw=False), poly([(gx + 2, gy - 76), (gx + 50, gy - 40), (gx + 2, gy - 30)], "rgba(242,201,142,.5)", GOLD, 1, ta + .2, fx="pop")]
    els += [ln([(gx - 70 + 16 * k, gy + 18), (gx - 80 + 16 * k, gy + 40)], ta + .2, GOLD, 1.2, draw=False) for k in range(9)]
    els += [lab(1420, 690, "a poem on Actium", ta + .3, GREEN, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s22():
    """Infrared: an opened fragment's letters come up dark under a red-violet light. Hundreds never opened: estimates from about
    270 to more than 600 (bars on one scale, 1 unit a roll)."""
    ti, tn, t270, t600 = T("s22", "Infrared"), T("s22", "never opened"), T("s22", "two hundred and seventy"), T("s22", "six hundred")
    frag = [(170, 330), (330, 300), (520, 318), (690, 350), (700, 470), (660, 600), (480, 620), (300, 610), (180, 560), (160, 450)]
    els = [poly(frag, SHEET, "rgba(200,170,140,.4)", 1.5, -1), glyphs(210, 360, 450, 220, -1, rows=7, cols=18, c="#33281f", sw=2.0, seed=17)]
    els += [rect(360, 150, 120, 70, "#2b2b30", "#9a9aa8", 1.5, 8, ti, fx="pop"), circ(420, 232, 26, "#1a1a20", "#9a9aa8", 2, ti + .1, fx="pop"),
            poly([(400, 250), (440, 250), (720, 600), (140, 600)], "rgba(220,90,170,.10)", at=ti + .3, fx="pop")]
    els += [poly(frag, "rgba(196,170,140,.62)", at=ti + .6, fx="pop"), glyphs(210, 360, 450, 220, ti + .9, rows=7, cols=18, c="#1a110b", sw=2.4, seed=17)]
    els += [lab(430, 680, "infrared", ti + .6, "#e0a0d0", 30)]
    els += [rect(950, 230, 690, 18, WOOD, at=-1), rect(950, 360, 690, 18, WOOD, at=-1)]
    els += [c for k in range(12) for c in roll_end(990 + 56 * k, 200, 26, .3 + .03 * k, turns=5)]
    els += [c for k in range(12) for c in roll_end(990 + 56 * k, 330, 26, .4 + .03 * k, turns=5)]
    els += [lab(1295, 430, "never opened", tn, BONE, 30)]
    els += [lab(960, 500, "about 270", t270, AMBER, 28, "start"), rect(960, 512, 270, 34, "rgba(232,184,122,.45)", AMBER, 2, 4, t270, fx="pop", style="inferred")]
    els += [lab(960, 600, "more than 600", t600, AMBER, 28, "start"), rect(960, 612, 600, 34, "rgba(232,184,122,.25)", AMBER, 2, 4, t600, fx="pop", style="inferred"),
            arr([(1566, 629), (1640, 629)], t600 + .3, AMBER, 3, "inferred", .4, curve=False)]
    els += [lab(1260, 700, "still closed, by two counts", t600 + .6, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 3. Unwrapping without touching
def spiral_pts(cx, cy, r, turns, n_per=24, squash=1.0, r0=.06):
    out = []
    n = int(turns * n_per)
    for k in range(n + 1):
        t = k / n
        a = t * turns * 2 * math.pi
        rr = r * (r0 + (1 - r0) * t)
        out.append((cx + rr * math.cos(a), cy + rr * squash * math.sin(a)))
    return out


def s23():
    """A CT scanner ring with a roll on its stand; slices stack through it; a screen shows one slice, a pale spiral; Brent Seales."""
    tb, th, tsl = T("s23", "Brent Seales"), T("s23", "hospital scanner"), T("s23", "slice by slice")
    els = [circ(600, 420, 200, "none", "#8d8f94", 48, .2, fx="pop"), circ(600, 420, 176, "none", "#c9cbd0", 2, .3), circ(600, 420, 224, "none", "#5a5c62", 2, .3),
           poly([(470, 600), (730, 600), (780, 720), (420, 720)], "#5a5c62", "#8d8f94", 1.5, .2)]
    els += [rect(330, 410, 540, 14, "#6a6c72", at=.4)] + roll_side(500, 700, 396, 44, .5, seed=2)
    els += [lab(600, 170, "like a hospital CT", th, BLUE, 28)]
    els += [poly(E(512 + 16 * k, 396, 6, 54, 12), "rgba(159,208,255,.12)", BLUE, 1.2, tsl + .1 * k, fx="pop") for k in range(12)]
    els += [rect(1060, 190, 500, 360, "#101418", "#6a6c72", 3, 10, tb, fx="pop"), rect(1130, 210, 360, 320, "#05070a", at=tb + .1)]
    els += [ln(spiral_pts(1310, 370, 140, 8, 20), tsl + .6, "#d8e6f0", 1.8, dur=1.6, curve=True)]
    els += [rect(1040, 560, 540, 20, WOOD, at=tb + .1), rect(1290, 550, 40, 10, "#4a4a50", at=tb + .1)]
    els += seated(1660, 720, 200, tb + .2, "#8a8fa0", face=-1)
    els += [lab(1310, 630, "Brent Seales", tb + .4, GOLD, 30), lab(1310, 672, "University of Kentucky", tb + .6, DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def wool(cx, cy, r, at, c="#7a5a6a", hi=AU, th=None):
    """A ball of wool: wrapped strands, one strand traced in gold and running out of it."""
    out = [circ(cx, cy, r, "#3a2a33", "#9a7a8a", 2, at, fx="pop")]
    rr = random.Random(5)
    for k in range(9):
        a = rr.uniform(0, math.pi)
        p = [(cx + r * .95 * math.cos(a + t) * math.cos(t * .9), cy + r * .95 * math.sin(t * 1.3 + k)) for t in [j * .3 for j in range(11)]]
        out.append(ln(p, at + .05 * k, c, 3, dur=.3, curve=True))
    g = [(cx - r * .7, cy - r * .2), (cx - r * .2, cy - r * .6), (cx + r * .4, cy - r * .3), (cx + r * .5, cy + r * .4), (cx - r * .1, cy + r * .6),
         (cx - r * .6, cy + r * .2), (cx - r * .3, cy - r * .1), (cx + r * .2, cy + r * .1), (cx + r * 1.2, cy + r * .9), (cx + r * 1.7, cy + r * .7)]
    out.append(ln(g, th if th is not None else at + .5, hi, 4, dur=1.2, curve=True))
    return out


def s24():
    """Virtual unwrapping in three pictures: follow one sheet through the slices (one turn traced in gold), like a strand of wool;
    then flatten it on the screen, like unrolling a carpet."""
    tf, tw, tfl = T("s24", "Follow one sheet"), T("s24", "ball of wool"), T("s24", "flatten it")
    els = [rect(110, 230, 380, 320, "#05070a", "#6a6c72", 2, 8, -1), ln(spiral_pts(300, 390, 140, 8, 20), -1, "#d8e6f0", 1.6, draw=False, curve=True)]
    sp = spiral_pts(300, 390, 140, 8, 20)
    els += [ln(sp[60:100], tf + .2, AU, 4, dur=1.0, curve=True), lab(300, 610, "follow one sheet", tf + .4, AU, 28)]
    els += [arr([(510, 390), (640, 390)], tw - .2, BONE, 3, curve=False)]
    els += wool(820, 390, 110, tw, th=tw + .4) + [lab(820, 610, "like a strand of wool", tw + .5, DIM, 26)]
    els += [arr([(1010, 390), (1120, 390)], tfl - .2, BONE, 3, curve=False)]
    els += roll_side(1150, 1260, 460, 70, tfl, seed=4, c="#7a3a2a", rim=False, cracks=False)
    els += [ln([(1260, 470), (1660, 470)], tfl + .3, "#9a4a32", 64, dur=1.4), ln([(1270, 470), (1650, 470)], tfl + .6, AU, 4, dur=1.2, op=.8),
            rect(1270, 260, 380, 150, "rgba(232,195,90,.18)", AU, 2.5, 4, tfl + .9, fx="pop"), lab(1460, 610, "flatten it", tfl + .9, AU, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s25():
    """Paris, 2009: two rolled scrolls scanned; every layer shows, and the flattened page is blank."""
    tp, tl, tn = T("s25", "Paris"), T("s25", "every layer"), T("s25", "single letter")
    els = roll_upright(300, 560, 260, 70, .2) + roll_upright(470, 560, 230, 64, .3) + [rect(220, 560, 330, 16, "#4a4a50", at=.2)]
    els += chip(385, 640, "Paris, 2009", GOLD, tp, 28)
    els += [arr([(540, 400), (700, 400)], tl - .3, BONE, 3, curve=False)]
    els += [rect(720, 190, 900, 400, "#0a0c10", "#6a6c72", 3, 10, .4)]
    els += [ln(spiral_pts(900, 390, 150, 9, 20), tl, "#d8e6f0", 1.6, dur=1.2, curve=True), lab(900, 640, "every layer", tl + .3, BLUE, 28)]
    els += [rect(1110, 240, 460, 300, SHEET, SHEET_E, 1.5, 3, tl + .8, fx="pop")]
    els += [ln([(1120, 252 + 13 * j), (1560, 254 + 13 * j)], tl + .9, "#3e3229", 1.4, draw=False) for j in range(22)]
    els += qmark(1340, 440, tn, 100) + [lab(1340, 640, "no letters", tn + .2, LILAC, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s26():
    """En-Gedi: the Dead Sea shore (schematic), the synagogue's charred scroll (found 1970, burned about 600 CE); in 2015 the
    unwrapped text came back on screen: Leviticus 1 to 2 (writing drawn as strokes)."""
    t15, t70, t600, tt, tlv = T("s26", "twenty fifteen"), T("s26", "nineteen seventy"), T("s26", "six hundred"), T("s26", "text came back"), T("s26", "Leviticus")
    mx0, my0, mw, mh = 100, 180, 560, 470
    lon0, lon1, lat0, lat1 = 34.95, 35.85, 30.95, 31.95
    P = lambda lo, la: (mx0 + (lo - lon0) / (lon1 - lon0) * mw, my0 + (lat1 - la) / (lat1 - lat0) * mh)
    sea = [P(35.53, 31.78), P(35.58, 31.70), P(35.58, 31.50), P(35.55, 31.30), P(35.50, 31.12), P(35.45, 31.08), P(35.40, 31.18),
           P(35.40, 31.36), P(35.40, 31.55), P(35.45, 31.72)]
    ex, ey = P(35.39, 31.46)
    jx, jy = P(35.21, 31.78)
    els = [rect(mx0, my0, mw, mh, "#3a2f24", "#c9ad85", 1.6, 8, -1), poly(sea, "#2f6f8c", "#9fd0ff", 1.5, -1, curve=True),
           lab(P(35.5, 31.0)[0], P(35.5, 31.0)[1] + 4, "Dead Sea", .3, "#9fd0ff", 26, st="ital"),
           {"k": "pin", "x": round(jx, 1), "y": round(jy, 1), "t": "Jerusalem", "c": BONE, "in": .4, "a": "start", "lx": 16, "ly": -10},
           {"k": "pin", "x": round(ex, 1), "y": round(ey, 1), "t": "En-Gedi", "c": GOLD, "in": .6, "a": "end", "lx": -18, "ly": 8}]
    els += chip(380, 700, "found 1970", GOLD, t70, 26) + chip(380, 760, "burned c. 600 CE", "#ffb09a", t600, 26)
    els += chip(1330, 160, "2015", GOLD, t15, 26)
    els += lump(860, 420, 120, 64, .5, 77) + [lab(860, 520, "charred, unopened", .7, DIM, 24)]
    els += [arr([(940, 420), (1020, 420)], tt - .3, BONE, 3, curve=False)]
    els += [rect(1040, 210, 580, 360, "#d8ccb4", "#8a7a5a", 1.5, 4, tt, fx="pop")]
    els += [glyphs(1070 + 280 * j, 240, 240, 300, tt + .3 + .3 * j, rows=11, cols=12, c="#2a2118", sw=2.4, kind="latin", seed=40 + j) for j in range(2)]
    els += [lab(1330, 620, "Leviticus 1 to 2", tlv, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s27():
    """X-ray views of a sheet: at En-Gedi the ink shines (metal); at Herculaneum carbon ink on carbonised papyrus is the same grey;
    then black on black."""
    tm, tc, tb = T("s27", "traces of metal"), T("s27", "almost pure carbon"), T("s27", "Black ink")
    els = []
    for k, (x0, title, at) in enumerate([(150, "En-Gedi", tm), (950, "Herculaneum", tc)]):
        els += [rect(x0, 200, 680, 380, "#0b0b0d", "#6a6c72", 2, 10, at - .2, fx="pop"), lab(x0 + 340, 250, title, at, BONE, 32, st="serif")]
        els += [poly([(x0 + 40, 420), (x0 + 640, 410), (x0 + 640, 470), (x0 + 40, 480)], "#6a6764" if k == 0 else "#55524e", at=at + .2)]
        r = random.Random(3 + k)
        for j in range(16):
            sx = x0 + 70 + 34 * j + r.uniform(-4, 4)
            col = "#ffffff" if k == 0 else "#5d5a56"
            els.append(rect(sx, 388 + r.uniform(-3, 3), r.uniform(10, 22), r.uniform(18, 30), col, at=at + .4 + .04 * j, fx="pop", op=.95 if k == 0 else .9))
        if k == 0:
            els += [gl(x0 + 340, 400, 260, at + .6, .35, "scan"), lab(x0 + 340, 640, "metal in the ink", at + .8, BLUE, 30)]
        else:
            els += [lab(x0 + 340, 640, "carbon on carbon", at + .8, DIM, 30)]
    els += [rect(950, 200, 680, 380, "rgba(5,4,3,.72)", at=tb, fx="pop"), lab(1290, 710, "black on black", tb + .3, BONE, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s28():
    """A synchrotron: a ring of magnets hundreds of metres around, a particle racing round it, a beamline to a hutch where a roll
    stands in the beam; Grenoble, 2015: Greek letters glint inside the roll."""
    tr, tl, tg = T("s28", "rings of magnets"), T("s28", "speed of light"), T("s28", "Grenoble")
    cx, cy, rx, ry = 650, 430, 420, 150
    els = [poly(E(cx, cy, rx + 18, ry + 10, 48), "none", "#3a3c40", 22, .3, op=.6), lab(cx, 200, "two ideas", .5, DIM, 28),
           poly(E(cx, cy, rx + 18, ry + 10, 48), "none", "#5a5c62", 22, tr - .3, fx="pop"), poly(E(cx, cy, rx + 18, ry + 10, 48), "none", "#9a9ca4", 2, tr - .2),
           poly(E(cx, cy, rx - 60, ry - 40, 36), "#14161a", "#5a5c62", 1.5, tr - .2)]
    els += [rect(cx + rx * math.cos(math.radians(a)) - 12, cy + ry * math.sin(math.radians(a)) - 9, 24, 18, "#3a6ea5", "#9fd0ff", 1, 2, tr + .02 * j, fx="pop")
            for j, a in enumerate(range(0, 360, 20))]
    els += [lab(cx, 680, "a ring hundreds of metres around", tr + .5, BONE, 28)]
    trail = E(cx, cy, rx + 18, ry + 10, 48, 20, 70)
    els += [ln(trail, tl, AU, 5, dur=.6, curve=True), circ(trail[-1][0], trail[-1][1], 9, "#fff6e0", at=tl + .5, fx="pop"), gl(trail[-1][0], trail[-1][1], 70, tl + .5, .7)]
    bx, by = cx + rx * math.cos(math.radians(10)) + 20, cy + ry * math.sin(math.radians(10))
    els += [ln([(bx, by), (1420, 520)], tl + .3, BLUE, 4, dur=.8), rect(1400, 430, 240, 170, "#2a2c30", "#8d8f94", 2, 6, tl + .2, fx="pop")]
    els += roll_upright(1520, 580, 110, 34, tl + .5) + [gl(1520, 530, 90, tl + .8, .5, "scan")]
    els += [lab(1520, 400, "Grenoble, 2015", tg, GOLD, 28), glyphs(1508, 520, 26, 40, tg + .4, rows=3, cols=2, c=AU, sw=2, seed=8)]
    els += [lab(1520, 650, "letters inside", tg + .6, AU, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


DOG = [(-36, -40), (-8, -44), (24, -46), (40, -42), (50, -58), (56, -62), (54, -50), (46, -36), (44, -18), (47, 0), (39, 0), (35, -16), (8, -20), (-18, -18),
       (-20, 0), (-28, 0), (-31, -18), (-40, -26), (-50, -18), (-66, -6), (-72, -2), (-70, 3), (-60, 2), (-48, -8), (-46, -30), (-52, -44), (-44, -48), (-40, -42)]


def s29():
    """A model trained on broken fragments whose ink shows in infrared photos (cream letters), like a sniffer dog trained on known
    samples; then it finds faint traces (gold) inside a closed roll's flattened surface."""
    td, tf, th = T("s29", "sniffer dog"), T("s29", "broken fragments"), T("s29", "hunts")
    els = [poly([(1090 + 1.6 * x, 720 + 1.6 * y) for x, y in DOG], "#cbbca8", "rgba(255,236,206,.4)", 1, td, fx="pop"),
           lab(1090, 770, "like a sniffer dog", td + .3, DIM, 26)]
    frs = [[(150, 230), (330, 210), (480, 236), (500, 320), (300, 350), (160, 330)], [(130, 400), (300, 380), (470, 410), (480, 500), (250, 520), (140, 490)],
           [(170, 570), (380, 560), (520, 590), (500, 670), (300, 690), (180, 660)]]
    for k, f in enumerate(frs):
        xs, ys = [p[0] for p in f], [p[1] for p in f]
        els += [poly(f, SHEET, "rgba(200,170,140,.4)", 1.5, tf + .2 * k, fx="pop"),
                glyphs(min(xs) + 25, min(ys) + 20, max(xs) - min(xs) - 60, max(ys) - min(ys) - 40, tf + .2 * k + .2, rows=3, cols=10, c=CREAM, sw=1.8, seed=50 + k)]
    els += [lab(330, 740, "ink visible", tf + .6, CREAM, 26)]
    nodes = [[(760, 300 + 70 * j) for j in range(4)], [(860, 265 + 70 * j) for j in range(5)], [(960, 335 + 70 * j) for j in range(3)]]
    nt = .4
    for a, b in zip(nodes, nodes[1:]):
        els += [ln([p, q], nt + .2, "rgba(159,208,255,.35)", 1.2, draw=False) for p in a for q in b]
    els += [circ(x, y, 14, "#1c2a38", BLUE, 2, nt + .05 * k, fx="pop") for k, (x, y) in enumerate([p for layer in nodes for p in layer])]
    els += [arr([(520, 450), (730, 420)], tf + .6, BONE, 2.5), lab(860, 620, "a model", nt + .4, BLUE, 28)]
    els += [arr([(990, 420), (1080, 420)], th - .3, BONE, 2.5, curve=False), rect(1100, 220, 540, 380, SHEET, SHEET_E, 1.5, 4, th - .3, fx="pop")]
    els += [ln([(1110, 236 + 14 * j), (1630, 238 + 14 * j)], th - .2, "#3e3229", 1.2, draw=False) for j in range(25)]
    els += [glyphs(1140 + 160 * j, 270, 130, 280, th + .2 + .3 * j, rows=7, cols=6, c=AU, sw=2, seed=60 + j, op=.75) for j in range(3)]
    els += [lab(1370, 650, "inside the closed ones", th + .8, AU, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 4. A word in the dark
VW_ = View(-170.0, 180.0, -56.0, 74.0, (90, 150, 1600, 600))
CITIES = [(-122.4, 37.8), (-74.0, 40.7), (-79.4, 43.7), (-99.1, 19.4), (-46.6, -23.5), (-58.4, -34.6), (-0.1, 51.5), (13.4, 52.5), (2.35, 48.86),
          (8.5, 47.4), (12.5, 41.9), (14.25, 40.85), (31.2, 30.0), (3.4, 6.5), (36.8, -1.3), (28.0, -26.2), (37.6, 55.8), (29.0, 41.0), (51.4, 35.7),
          (72.9, 19.1), (77.2, 28.6), (77.6, 13.0), (103.8, 1.35), (106.8, -6.2), (116.4, 39.9), (121.5, 31.2), (127.0, 37.6), (139.7, 35.7),
          (151.2, -33.9), (145.0, -37.8), (174.8, -36.8), (-77.0, -12.0), (-70.7, -33.4), (-74.1, 4.7), (-9.1, 38.7), (-3.7, 40.4), (-87.6, 41.9),
          (-118.2, 34.1), (18.1, 59.3), (24.9, 60.2)]


def s30():
    """The Vesuvius Challenge, March 2023: the scans (a glowing data cube) and prizes at the centre; lines run to people on every
    continent, who light up."""
    tl, tp, to = T("s30", "launch the Vesuvius"), T("s30", "prizes"), T("s30", "online for anyone")
    v = VW_
    els = [{"k": "map", "land": v.land(), "in": -1}]
    cx, cy = 889, 420
    els += [gl(cx, cy, 160, tl, .55, "scan"), poly([(cx - 40, cy - 20), (cx, cy - 40), (cx + 40, cy - 20), (cx, cy)], "#3a6ea5", BLUE, 1.5, tl, fx="pop"),
            poly([(cx - 40, cy - 20), (cx, cy), (cx, cy + 46), (cx - 40, cy + 26)], "#24507e", BLUE, 1.5, tl, fx="pop"),
            poly([(cx + 40, cy - 20), (cx, cy), (cx, cy + 46), (cx + 40, cy + 26)], "#1c3f66", BLUE, 1.5, tl, fx="pop"),
            lab(cx, cy - 66, "the scans", tl + .3, BLUE, 28)]
    els += [circ(cx + 110, cy + 10, 30, AU, "#fff1c8", 2, tp, fx="pop"), lab(cx + 110, cy + 22, "$", tp + .1, "#5a4330", 34, st="serif", halo=False),
            lab(cx + 110, cy + 74, "prizes", tp + .2, AU, 26)]
    r = random.Random(2)
    for k, (lo, la) in enumerate(CITIES):
        x, y = v.p(lo, la)
        at = to + .06 * k
        els += [ln([(cx, cy), ((cx + x) / 2, (cy + y) / 2 - 40), (x, y)], at, "rgba(159,208,255,.45)", 1.3, dur=.5, curve=True),
                dot(x, y, 5, "#fff1c8", round(at + .4, 2)), gl(x, y, 26, at + .4, .6, "lamp")]
    els += chip(889, 175, "March 2023", GOLD, .5, 28) + [lab(889, 700, "the Vesuvius Challenge", tl + .2, GOLD, 32, st="serif")]
    return {"base": "map", "cam": CAM, "els": els}


SURF = (80, 140, 1620, 680)               # the flattened layer of s31 / s32 (x, y, w, h)


def fibres(x, y, w, h, at, seed=1, n=46):
    r = random.Random(seed)
    out = [ln([(x + 6, y + h * (k + .5) / n + r.uniform(-2, 2)), (x + w - 6, y + h * (k + .5) / n + r.uniform(-2, 2))], at, "#3e3229", 1.2, draw=False, op=.8) for k in range(n)]
    out += [ln([(x + w * (k + .5) / 30 + r.uniform(-4, 4), y + 6), (x + w * (k + .5) / 30 + r.uniform(-4, 4), y + h - 6)], at, "#33291f", 1, draw=False, op=.6) for k in range(30)]
    return out


def crackle(boxes, at, seed=3, step=.05, c="#a08a70"):
    """A crackle of fine cracks filling the given boxes (the strokes of a letter), like cracked mud."""
    r = random.Random(seed)
    out = []
    k = 0
    for (x, y, w, h) in boxes:
        for j in range(int(h / 18)):
            yy = y + 9 + 18 * j
            out.append(ln([(x + 2, yy + r.uniform(-3, 3)), (x + w * .5, yy + r.uniform(-4, 4)), (x + w - 2, yy + r.uniform(-3, 3))], at + step * k, c, 1.4, dur=.25))
            k += 1
        for j in range(int(w / 18)):
            xx = x + 9 + 18 * j
            out.append(ln([(xx + r.uniform(-3, 3), y + 2), (xx + r.uniform(-4, 4), y + h * .5), (xx + r.uniform(-3, 3), y + h - 2)], at + step * k, c, 1.4, dur=.25))
            k += 1
    return out


PI_BOXES = [(760, 290, 290, 46), (790, 336, 46, 240), (974, 336, 46, 240)]


def s31():
    """Close on a flattened layer (cam z 1.3): fibres; a crackle like cracked mud draws itself in the shape of a letter; it was ink."""
    tc, ti = T("s31", "faint texture"), T("s31", "It was ink")
    x, y, w, h = SURF
    els = [rect(x, y, w, h, SHEET, SHEET_E, 1.5, 4, -1)] + fibres(x, y, w, h, -1, 3)
    els += [circ(905, 440, 260, "none", "rgba(242,201,142,.5)", 2.5, .5, style="inferred"), lab(560, 240, "Casey Handmer", T("s31", "Casey Handmer"), GOLD, 30)]
    els += crackle(PI_BOXES, tc, 3, .025)
    els += [lab(905, 640, "crackle, like cracked mud", tc + .8, "#d8c4a8", 30)]
    els += [rect(bx, by, bw, bh, "rgba(232,195,90,.42)", at=ti + .05 * k, fx="pop") for k, (bx, by, bw, bh) in enumerate(PI_BOXES)]
    els += [gl(905, 430, 220, ti, .5, "lamp"), lab(905, 250, "ink", ti + .2, AU, 40, st="serif")]
    return {"base": "dark", "cam": [1.3, 905, 455], "els": els}


def s32_add():
    """Wider: a student at a laptop, night after night; more crackle patches light up along the line as the model learns."""
    ts, tn = T("s32", "twenty-one-year-old"), T("s32", "night after night")
    els = seated(220, 720, 190, ts, "#9a8a7e", face=1) + [rect(250, 560, 120, 12, "#2a2c30", "#9a9ca4", 1, 2, ts + .1),
                                                           poly([(262, 560), (356, 560), (370, 488), (276, 488)], "#1c2a38", "#9a9ca4", 1, ts + .1),
                                                           gl(320, 524, 70, ts + .3, .6, "scan")]
    els += [lab(240, 770, "Luke Farritor, 21", ts + .4, GOLD, 28)]
    for k, cx in enumerate([1150, 1290, 1420, 1540]):
        bx = [(cx - 50, 300, 100, 40), (cx - 20, 340, 40, 160)] if k % 2 else [(cx - 50, 320, 100, 170)]
        els += crackle(bx, tn + .5 * k, 20 + k, .02)
        els += [gl(cx, 400, 90, tn + .5 * k + .4, .5, "lamp")]
    els += [lab(1350, 610, "night after night", tn + .2, DIM, 28)]
    return els


def s33():
    """The first word: eight Greek capitals rise out of the dark, ΠΟΡΦΥΡΑΣ; porphyras; purple."""
    tl, tfw, tp, tpu = T("s33", "Letters rose"), T("s33", "first word"), T("s33", "porphyras"), T("s33", "Purple")
    els = [rect(150, 290, 1478, 250, SHEET, SHEET_E, 1.5, 6, -1)] + fibres(150, 290, 1478, 250, -1, 9, 18)
    word = "ΠΟΡΦΥΡΑΣ"
    s = 6.2
    x0 = 889 - gwidth(word, s) / 2
    cx = x0
    for k, ch in enumerate(word):
        adv = GK[ch][0]
        els.append(gl(cx + adv * s / 2, 420, 90, tl + .35 * k, .55, "lamp"))
        cx += (adv + 2.2) * s
    els += gword(889, 470, word, s, tl + .1, CREAM, 6, dt=.35, dur=.35, a="middle")
    els += [lab(889, 240, "the first word", tfw, DIM, 28)]
    els += [lab(889, 620, "porphyras", tp, BONE, 46, st="ital")]
    els += [circ(800, 690, 20, PURPLE, "#d9a0dd", 2, tpu, fx="pop"), lab(836, 704, "purple", tpu + .1, AU, 44, "start", st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def screen(x, y, w, h, at):
    return [rect(x, y, w, h, "#101418", "#6a6c72", 3, 10, at, fx="pop"), rect(x + w / 2 - 30, y + h, 60, 30, "#4a4a50", at=at),
            rect(x + w / 2 - 80, y + h + 28, 160, 10, "#4a4a50", at=at)]


def s34():
    """Two screens, two methods: 'Farritor' and 'Nader' show the same word in the same place; a green tick."""
    ta, tb, ts = T("s34", "Youssef Nader"), T("s34", "same word"), T("s34", "different method")
    els = screen(200, 230, 600, 320, .2) + screen(980, 230, 600, 320, ta)
    els += [rect(230, 330, 540, 120, SHEET, at=.3)] + gword(500, 420, "ΠΟΡΦΥΡΑΣ", 2.6, .4, "#cbb8a0", 3, dt=.03, dur=.2, a="middle", op=.8)
    els += [rect(1010, 330, 540, 120, SHEET, at=ta + .1)] + gword(1280, 420, "ΠΟΡΦΥΡΑΣ", 2.6, ta + .2, CREAM, 3.4, dt=.05, dur=.2, a="middle")
    els += [lab(500, 640, "Farritor", .5, BONE, 30), lab(1280, 640, "Nader", ta + .2, BONE, 30)]
    els += [tick(889, 390, tb, GREEN, 1.6, 7), lab(889, 730, "same word, same place", tb + .3, GREEN, 30), lab(1280, 690, "another method", ts, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """February 2024: the grand prize, $700,000; about 15 columns appear on a long strip; more than 2,000 letters; about 5% of
    the whole scroll (a bar)."""
    tf, tg, tl, t5 = T("s35", "February"), T("s35", "grand prize"), T("s35", "two thousand"), T("s35", "five percent")
    els = strip(100, 1680, 250, 240, tf + .4, 15, .16, seed=33, rows=10)
    els += chip(889, 180, "$700,000", AU, tg, 34)
    els += [lab(889, 552, "more than 2,000 letters", tl, CREAM, 32)]
    els += [rect(100, 600, 1580, 28, "#2a2420", "#8a7360", 1.5, 6, t5 - .3), rect(100, 600, 79, 28, AU, "none", 0, 6, t5, fx="pop")]
    els += [lab(100, 670, "about 5% of the scroll", t5 + .2, AU, 30, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def fig(x, y):
    """A small fig, glowing: the rare thing."""
    return [poly([(x, y - 46), (x + 14, y - 30), (x + 26, y - 8), (x + 20, y + 10), (x, y + 16), (x - 20, y + 10), (x - 26, y - 8), (x - 14, y - 30)], "#a06a3a",
                 "#f2c98e", 1.5, .6, fx="pop", curve=True), gl(x, y - 14, 80, .7, .6, "lamp")]


def heap(x, y):
    """Loaves and olives: the plentiful things."""
    out = []
    r = random.Random(4)
    for k in range(7):
        bx, by = x - 70 + 24 * (k % 6) + (12 if k >= 6 else 0), y - 10 - 22 * (k // 6)
        out.append(poly(E(bx, by, 26, 14, 14), "#c9a06a", "#7a5a30", 1.2, .6 + .04 * k, fx="pop"))
    out += [poly(E(x - 60 + r.uniform(0, 120), y - 36 + r.uniform(-14, 6), 7, 5, 10), "#3a4a2a", "#6f8a5a", 1, round(.8 + .03 * k, 2), fx="pop") for k in range(14)]
    return out


def s36():
    """A balance: a single rare fig against a heap of loaves and olives; more pleasant? not necessarily. On pleasure, probably
    Philodemus."""
    tpl, tph, tq, tn = T("s36", "about pleasure"), T("s36", "Philodemus"), T("s36", "rare things"), T("s36", "Not necessarily")
    els = balance(889, 330, 660, 660, .3, left=lambda x, y: fig(x, y - 4), right=lambda x, y: heap(x, y - 4), drop=190, pan=240)
    els += tag(260, 190, "on pleasure", tpl, AMBER, 28) + tag(260, 250, "probably Philodemus", tph, GOLD, 26, "inferred")
    els += [lab(559, 600, "rare", tq + .3, GOLD, 30), lab(1219, 600, "plentiful", tq + .6, BONE, 30)]
    els += [lab(889, 230, "more pleasant?", tq + .9, LILAC, 36, st="serif")]
    els += [lab(889, 740, "not necessarily", tn, GOLD, 40, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def dome(cx, base, s, at):
    """A domed library building in silhouette (Oxford)."""
    return [rect(cx - 90 * s, base - 90 * s, 180 * s, 90 * s, "#3a3340", "rgba(255,236,206,.4)", 1.5, 2, at),
            rect(cx - 70 * s, base - 150 * s, 140 * s, 60 * s, "#443c4a", "rgba(255,236,206,.4)", 1.5, 2, at),
            poly(E(cx, base - 150 * s, 70 * s, 60 * s, 20, 180, 360), "#4c4352", "rgba(255,236,206,.5)", 1.5, at),
            rect(cx - 8 * s, base - 226 * s, 16 * s, 20 * s, "#4c4352", at=at)] + \
           [ln([(cx - 70 * s + 20 * s * k, base - 90 * s), (cx - 70 * s + 20 * s * k, base - 6 * s)], at, "rgba(255,236,206,.35)", 2, draw=False) for k in range(8)]


def s37():
    """2025: two teams, working separately, read a title in a sealed roll kept in Oxford: ΦΙΛΟΔΗΜΟΥ ΠΕΡΙ ΚΑΚΙΩΝ Α,
    Philodemus, On Vices, Book 1."""
    tt, to, tp = T("s37", "two teams"), T("s37", "Oxford"), T("s37", "Philodemus")
    els = dome(220, 560, .9, to) + [lab(220, 610, "Oxford", to + .2, BONE, 30)]
    els += roll_upright(600, 560, 250, 74, .3) + [rect(540, 560, 120, 14, "#4a4a50", at=.3)]
    for k, (tx, ty) in enumerate(((420, 300), (780, 300))):
        els += [person(tx - 14, ty + 30, 54, tt + .2 * k, "#d9c7a6"), person(tx + 14, ty + 30, 50, tt + .2 * k, "#d9c7a6"),
                arr([(tx + (40 if k == 0 else -40), ty + 10), (600 + (-50 if k == 0 else 50), ty + 120)], tt + .3 + .2 * k, BLUE, 2.5, "known", .6)]
    els += [lab(600, 220, "two teams, separately", tt + .6, DIM, 26)]
    els += [rect(900, 190, 760, 360, SHEET, SHEET_E, 1.5, 6, tp - .6, fx="pop")]
    els += gword(1280, 300, "ΦΙΛΟΔΗΜΟΥ", 3.3, tp - .3, CREAM, 3.6, dt=.09, dur=.25, a="middle")
    els += gword(1280, 400, "ΠΕΡΙ ΚΑΚΙΩΝ", 3.3, tp + .6, CREAM, 3.6, dt=.09, dur=.25, a="middle")
    els += gword(1280, 500, "Α", 3.3, tp + 1.6, CREAM, 3.6, dt=.09, dur=.25, a="middle", bar=True)
    els += [lab(1280, 620, "Philodemus, On Vices, Book 1", tp + 1.2, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s38():
    """Philodemus' students, named in other rolls: Plotius, Varius, Virgil, Quintilius; rolls on slander, envy and greed;
    Virgil lights gold with a laurel wreath."""
    tn, tv = T("s38", "by name"), T("s38", "Virgil")
    els = seated(420, 680, 220, .3, "#d9c7a6", face=1) + [lab(420, 730, "Philodemus", .5, GOLD, 28)]
    names = ["Plotius", "Varius", "Virgil", "Quintilius"]
    for k, x in enumerate([700, 860, 1020, 1180]):
        els += [person(x, 680, 170, .4 + .1 * k, "#cbbca8")]
        els += [lab(x, 730, names[k], tn + .2 * k, GOLD if k == 2 else DIM, 26 if k != 2 else 30)]
    for k, (x, t) in enumerate([(760, "slander"), (1000, "envy"), (1240, "greed")]):
        els += [rect(x - 80, 230, 160, 40, PAP_D, "#8a6a3e", 1.5, 8, .6 + .2 * k, fx="pop"), circ(x - 80, 250, 22, PAP, "#8a6a3e", 1.5, .6 + .2 * k, fx="pop"),
                circ(x + 80, 250, 22, PAP, "#8a6a3e", 1.5, .6 + .2 * k, fx="pop"), lab(x, 210, t, .8 + .2 * k, AMBER, 28)]
        els += [ln([(x, 272), (700 + 160 * j, 460)], tn + .1 * k, "rgba(232,184,122,.35)", 1.2, "claimed", .5) for j in range(4) if abs(700 + 160 * j - x) < 300]
    els += [gl(1020, 560, 160, tv, .6, "lamp"), ln(_arc(1020, 530, 18, 12, 200, 340, 8), tv + .2, "#6f9a6a", 4, dur=.4, curve=True),
            ln(_arc(1020, 530, 22, 16, 200, 340, 8), tv + .3, "#8fd9b0", 2, dur=.4, curve=True), lab(1020, 772, "a young poet", tv + .4, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 5. The first whole scroll
U1667 = 30.0                     # 1 cm = 30 units for PHerc. 1667
R1667 = (620, 720)              # its centre x and base y


def s39():
    """PHerc. 1667 to scale: the roll as it was (dashed: about 20 cm tall, 4.9 cm across) and the core that survives (8 cm, 2 cm);
    flakes come off at each attempt: 1800s, 1969, 1980s; written off as unreadable."""
    t1, t2, t3, tu = T("s39", "eighteen hundreds"), T("s39", "nineteen sixty-nine"), T("s39", "nineteen eighties"), T("s39", "unreadable")
    cx, b = R1667
    H0, D0, H1, D1 = 20 * U1667, 4.9 * U1667, 8 * U1667, 2 * U1667
    els = [gl(cx, b - 200, 360, .1, .25, "lamp"), rect(cx - D0 / 2, b - H0, D0, H0, "rgba(255,255,255,.03)", "rgba(233,220,203,.6)", 2, 18, .2, style="inferred"),
           poly(E(cx, b - H0, D0 / 2, D0 * .18, 20), "none", "rgba(233,220,203,.6)", 2, .3, style="inferred")]
    els += roll_upright(cx, b, H1, D1, .4)
    els += [lab(520, b - 20, "PHerc. 1667", .6, DIM, 26, "end")]
    r = random.Random(16)
    for k, (t, txt, yy) in enumerate([(t1, "1800s", 230), (t2, "1969", 380), (t3, "1980s", 530)]):
        for j in range(5):
            fx_, fy_ = cx - D0 / 2 - 10 - r.uniform(0, 40), yy + 20 * j + r.uniform(-6, 6)
            els.append(poly(E(fx_, fy_, r.uniform(8, 13), r.uniform(4, 7), 8), CHAR2, "rgba(200,170,140,.4)", 1, t + .1 * j, fx="pop"))
        els += [ln([(cx - D0 / 2 - 64, yy + 40), (420, yy + 40)], t, RED, 1.6, dur=.3), lab(405, yy + 50, txt, t + .2, "#ffb09a", 30, "end")]
    els += tag(1250, 330, "unreadable", tu, LILAC, 34, "claimed")
    return {"base": "dark", "cam": CAM, "els": els}


def s40_add():
    """Closer on the core: about 8 cm of a roll once about 20 cm tall, as thick as a thumb; scanned in Grenoble (the beam from
    above), detail a few thousandths of a millimetre."""
    t8, t20, tth, tg, tf = T("s40", "eight centimetres"), T("s40", "twenty centimetres"), T("s40", "thumb"), T("s40", "Grenoble"), T("s40", "thousandths")
    cx, b = R1667
    H0, D0, H1, D1 = 20 * U1667, 4.9 * U1667, 8 * U1667, 2 * U1667
    els = dimv(cx + D1 / 2 + 22, b - H1, b, t8, "about 8 cm", GOLD, 1, 28)
    els += dimv(cx + D0 / 2 + 26, b - H0, b, t20, "about 20 cm", "rgba(233,220,203,.85)", 1, 26)
    tx = cx + 330
    els += [rect(tx - 32, b - 190, 64, 190, "rgba(232,214,184,.12)", SKIN, 2, 30, tth, fx="pop"), rect(tx - 20, b - 182, 40, 46, "rgba(255,240,220,.15)", SKIN, 1.5, 14, tth + .1),
            lab(tx, b - 210, "a thumb", tth + .2, SKIN, 28)]
    els += [ln([(cx - 24 + 8 * k, 170), (cx - 24 + 8 * k, b - H1 - 6)], tg + .05 * k, BLUE, 1.6, dur=.5, op=.55) for k in range(7)]
    els += [gl(cx, b - 110, 120, tg + .4, .45, "scan"), lab(cx + 120, 290, "scanned in Grenoble", tg + .1, BLUE, 28, "start")]
    els += [lab(1120, 470, "detail: a few thousandths of a mm", tf, BLUE, 24)]
    return els


def s41():
    """The reading: a spiral of 31 turns unwinds into a strip nearly 1.5 m long (to scale, about 900 units a metre) with 22
    columns; only the lower part of each survives (solid), the upper parts are lost (dashed); gaps."""
    t31, t22, tm, tlo, tg = T("s41", "thirty-one turns"), T("s41", "twenty-two columns"), T("s41", "one and a half"), T("s41", "lower part"), T("s41", "gaps")
    els = [circ(220, 430, 152, "#1a1410", "rgba(200,170,140,.35)", 1.5, .2), ln(spiral_pts(220, 430, 148, 31, 16, 1.0, .06), .3, "#c8b8a0", .8, dur=1.6, curve=True, op=.75)]
    els += chip(220, 640, "31 turns", GOLD, t31, 28)
    els += [ln([(375, 470), (392, 470)], .9, GOLD, 3, "claimed", .3)]
    els += strip(400, 1650, 280, 270, 1.0, 22, .15, top_lost=.55, seed=41, rows=4)
    els += chip(1025, 220, "22 columns", GOLD, t22, 28)
    els += dimh(400, 1650, 600, tm, "nearly 1.5 m", GOLD, 30, 18, 1.2)
    els += [lab(1025, 330, "lost", tlo, "rgba(233,220,203,.8)", 26), lab(1025, 700, "lower part survives", tlo + .3, CREAM, 28)]
    r = random.Random(4)
    for k in range(9):
        gx = 430 + r.uniform(0, 1180)
        els.append(rect(gx, 440 + r.uniform(0, 60), r.uniform(20, 40), r.uniform(20, 36), SHEET, at=tg + .06 * k, fx="pop"))
    return {"base": "dark", "cam": CAM, "els": els}


def stoa(x0, x1, base, top, at, n=8):
    """A Greek stoa: a long colonnade under a roof, on a step."""
    out = [rect(x0 - 20, base, x1 - x0 + 40, 22, "#8c7a62", "#c9b896", 1.5, 2, at), rect(x0 - 30, top - 40, x1 - x0 + 60, 40, "#9a8668", "#d8c7a6", 1.5, 2, at),
           poly([(x0 - 40, top - 40), (x1 + 40, top - 40), (x1 + 10, top - 80), (x0 - 10, top - 80)], "#6b5a48", "#c9b896", 1.5, at)]
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1)
        out += [rect(x - 12, top, 24, base - top, "#e8dcc4", "#a8977c", 1, 2, at + .04 * k, fx="rise"), rect(x - 18, top - 8, 36, 10, "#e8dcc4", at=at + .04 * k)]
    return out


def s42():
    """Stoic ethics: a stoa with people talking under it; human nature, impulse, moral progress; the text names Aristocreon,
    nephew of the great Stoic Chrysippus."""
    ts, tn, ti, tp, ta, tc = (T("s42", "Stoic ethics"), T("s42", "human nature"), T("s42", "impulse"), T("s42", "moral progress"), T("s42", "Aristocreon"),
                              T("s42", "Chrysippus"))
    els = [lab(550, 160, "the rival camp", .4, DIM, 28)] + stoa(170, 930, 560, 320, .3)
    els += [person(420, 560, 110, .8, "#cbbca8"), person(470, 560, 104, .9, "#cbbca8"), person(640, 560, 112, 1.0, "#cbbca8")]
    els += [lab(550, 640, "Stoic ethics", ts, GOLD, 36, st="serif")]
    els += tag(330, 720, "human nature", tn, AMBER, 26) + tag(560, 720, "impulse", ti, AMBER, 26) + tag(780, 720, "moral progress", tp, AMBER, 26)
    els += [rect(1180, 470, 340, 80, "rgba(242,201,142,.12)", GOLD, 2, 12, ta, fx="pop"), lab(1350, 522, "Aristocreon", ta + .1, GOLD, 34, st="serif"),
            gl(1350, 510, 160, ta + .2, .4, "lamp")] + tag(1350, 610, "named in the text", ta + .4, GOLD, 26)
    els += [rect(1200, 250, 300, 70, "rgba(245,236,220,.06)", BONE, 2, 12, tc, fx="pop"), lab(1350, 296, "Chrysippus", tc + .1, BONE, 32, st="serif"),
            ln([(1350, 320), (1350, 470)], tc + .3, BONE, 2, dur=.5), lab(1370, 405, "his nephew", tc + .5, DIM, 24, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def XT(yr):
    return round(170 + (yr + 300) / 2326.0 * 1440, 1)


def s43():
    """Its age: copied in the 2nd century BCE (a gold band), buried in 79 CE, read in 2026; already about 200 years old when
    buried; author and title lost."""
    tc, tb, tl = T("s43", "second century"), T("s43", "already an antique"), T("s43", "author and its title")
    ticks = [(XT(-300), "300 BCE"), (XT(1), "1 CE"), (XT(500), "500"), (XT(1000), "1000"), (XT(1500), "1500"), (XT(2000), "2000")]
    els = [axis(170, 1610, 460, ticks, .2)]
    els += [{"k": "band", "x0": XT(-200), "x1": XT(-101), "y": 404, "h": 20, "c": GOLD, "t": "copied", "tc": GOLD, "in": tc}]
    els += [ln([(XT(79), 380), (XT(79), 460)], tb - .4, RED, 4, dur=.3), lab(XT(79) + 10, 360, "buried, 79 CE", tb - .3, "#ffb09a", 26, "start")]
    els += [ln([(XT(2026), 380), (XT(2026), 460)], tb - .2, BLUE, 4, dur=.3), lab(XT(2026), 360, "read, 2026", tb - .1, BLUE, 26, "end")]
    els += bracket(XT(-150), XT(79), 560, tb + .2, None, AMBER, False)
    els += [lab((XT(-150) + XT(79)) / 2, 610, "already about 200 years old", tb + .4, AMBER, 28)]
    els += [rect(XT(-150) - 30, 230, 60, 90, "rgba(201,193,238,.06)", LILAC, 2, 10, tl, style="claimed"), lab(XT(-150), 290, "?", tl + .2, LILAC, 44, st="serif"),
            lab(XT(-150) + 60, 260, "author? title?", tl + .3, LILAC, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s44():
    """Another sealed roll: its title, ΦΙΛΟΔΗΜΟΥ ΠΕΡΙ ΘΕΩΝ Η (three letters restored, dashed): Philodemus, On Gods, Book 8;
    eight rolls, the first known, the eighth new: at least 8 books."""
    tt, tp, t8 = T("s44", "a title"), T("s44", "Philodemus"), T("s44", "first sign")
    els = roll_upright(250, 600, 260, 70, .2) + [rect(190, 600, 120, 14, "#4a4a50", at=.2)]
    els += [rect(430, 190, 720, 360, SHEET, SHEET_E, 1.5, 6, tt, fx="pop")]
    els += gword(790, 300, "ΦΙΛΟΔΗΜΟΥ", 3.3, tt + .3, CREAM, 3.6, dt=.09, dur=.25, a="middle", dashed=(2, 3, 4))
    els += gword(790, 400, "ΠΕΡΙ ΘΕΩΝ", 3.3, tt + 1.2, CREAM, 3.6, dt=.09, dur=.25, a="middle")
    els += gword(790, 500, "Η", 3.3, tt + 2.1, CREAM, 3.6, dt=.09, dur=.25, a="middle", bar=True)
    els += [lab(790, 620, "Philodemus, On Gods, Book 8", tp + .4, GOLD, 32)]
    for k in range(8):
        x = 1250 + 56 * k
        if k == 0:
            els += roll_end(x, 420, 22, t8, turns=4, c="#3a2e24", line=BONE)
        elif k == 7:
            els += roll_end(x, 420, 22, t8 + .8, turns=4, c="#3a2e24", line=AU) + [gl(x, 420, 70, t8 + .8, .6, "lamp")]
        else:
            els += [circ(x, 420, 22, "none", "rgba(233,220,203,.5)", 1.5, t8 + .1 * k, style="inferred")]
    els += [lab(1250, 480, "Book 1", t8 + .1, BONE, 26), lab(1642, 480, "Book 8", t8 + .9, AU, 26)]
    els += bracket(1228, 1664, 360, t8 + 1.1, None, AMBER, True) + [lab(1446, 330, "at least 8 books", t8 + 1.3, AMBER, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s45():
    """Faces in clouds? A dotted face in a cloud. Three checks: separate teams, papyrologists, the ink seen directly in the scan."""
    tf, t1, t2, t3 = T("s45", "faces in"), T("s45", "Separate teams"), T("s45", "Papyrologists"), T("s45", "newest scans")
    cl = []
    for k in range(5):
        cl += [(500 + 70 * k + 30 * math.cos(math.radians(a)), 210 - 30 * math.sin(math.radians(a)) - (14 if k in (1, 3) else 24 if k == 2 else 0)) for a in range(180, -1, -45)]
    Z = lambda x, y: (889 + (x - 650) * 1.6, 230 + (y - 220) * 1.6)
    els = [poly([Z(480, 240)] + [Z(x, y) for x, y in cl] + [Z(800, 240)], "#3a3a48", "rgba(220,220,240,.4)", 1.5, .2, curve=True, op=.85),
           gl(889, 200, 260, .2, .25, "scan")]
    els += [circ(*Z(610, 205), 10, LILAC, at=tf), circ(*Z(690, 205), 10, LILAC, at=tf),
            ln([Z(x, y) for x, y in _arc(650, 218, 26, 14, 20, 160, 8)], tf + .1, LILAC, 3.5, "claimed", .4, True),
            lab(1190, 236, "faces in clouds?", tf + .3, LILAC, 30, "start")]
    boxes = [(150, t1, "separate teams"), (670, t2, "papyrologists"), (1190, t3, "ink seen directly")]
    for k, (x0, t, txt) in enumerate(boxes):
        els += [rect(x0, 330, 440, 330, "rgba(245,236,220,.04)", "rgba(245,236,220,.35)", 2, 14, t - .2, fx="pop"), lab(x0 + 220, 630, txt, t + .2, BONE, 28),
                tick(x0 + 400, 368, t + .6, GREEN, 1.2)]
    els += [rect(180, 380, 180, 90, "#101418", "#6a6c72", 2, 6, t1), rect(400, 380, 180, 90, "#101418", "#6a6c72", 2, 6, t1)]
    els += gword(270, 438, "ΠΟΡ", 1.6, t1 + .2, CREAM, 2.4, dt=.05, dur=.2, a="middle") + gword(490, 438, "ΠΟΡ", 1.6, t1 + .3, CREAM, 2.4, dt=.05, dur=.2, a="middle")
    els += seated(760, 590, 160, t2, SKIN, face=1) + [rect(800, 520, 150, 60, "#efe3c8", at=t2 + .1, fx="pop"), circ(900, 470, 30, "rgba(159,208,255,.15)", BONE, 3, t2 + .2, fx="pop"),
                                                      ln([(880, 492), (850, 530)], t2 + .2, BONE, 5, draw=False)]
    r = random.Random(8)
    els += [rect(1230, 380, 360, 200, "#2a2a2c", "#6a6c72", 2, 4, t3)]
    els += [dot(round(1240 + r.uniform(0, 340), 1), round(390 + r.uniform(0, 180), 1), round(r.uniform(1, 2.5), 1), "#4a4a4e", round(t3 + .05, 2), None) for _ in range(60)]
    els += gword(1410, 505, "ΠΟΡ", 2.6, t3 + .3, "#ffffff", 3.4, dt=.08, dur=.2, a="middle")
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s46():
    """The limit: a roll whose layers stand apart reads well; a crushed one, its layers pressed together and hazy, may not; not
    guaranteed."""
    tc, tb, tn = T("s46", "crushed so tight"), T("s46", "layers blur"), T("s46", "not guaranteed")
    els = [rect(170, 220, 480, 400, "#05070a", "#6a6c72", 2, 10, .2), ln(spiral_pts(410, 420, 160, 7, 22), .4, "#d8e6f0", 2, dur=1.2, curve=True),
           lab(410, 670, "layers apart", .8, BLUE, 28)]
    els += [rect(830, 220, 780, 400, "#05070a", "#6a6c72", 2, 10, tc - .2)]
    els += [ln(spiral_pts(1220, 420, 300, 14, 26, .22, .02), tc, "#c8d0d8", 1.6, dur=1.2, curve=True)]
    els += [gl(1150 + 90 * k, 420 + (12 if k % 2 else -10), 140, tb + .15 * k, .45, "scan") for k in range(4)]
    els += [poly(E(1220, 420, 300, 70, 30), "rgba(200,205,215,.18)", at=tb + .2, fx="pop"), lab(1220, 670, "crushed layers", tb, DIM, 28)]
    els += tag(889, 750, "not guaranteed", tn, AMBER, 30, "inferred")
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 6. The weighing
LROWS = [215, 395, 525, 655]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1150, y, grade, gc, gt, 28, "start")
    return out


def pic_roll(x, y, at):
    return roll_side(x - 56, x + 56, y, 40, at, seed=9, fx="pop", cracks=False) + [glyphs(x - 30, y - 12, 60, 24, at + .1, rows=2, cols=5, c=AU, sw=1.6, seed=2)]


def pic_strip(x, y, at):
    return [rect(x - 60, y - 34, 120, 68, SHEET, SHEET_E, 1, 3, at, fx="pop")] + \
           [rect(x - 54 + 30 * j, y - 28, 22, 26, "none", "rgba(233,220,203,.5)", 1, 2, at + .05, style="inferred") for j in range(4)] + \
           [glyphs(x - 54 + 30 * j, y + 2, 22, 24, at + .1, rows=2, cols=3, c=CREAM, sw=1.4, seed=j) for j in range(4)]


def pic_villa(x, y, at):
    return [rect(x - 60, y - 40, 120, 80, ROCK_D, "rgba(255,226,190,.3)", 1, 3, at, fx="pop"), ln([(x - 56, y - 6), (x + 10, y - 6)], at + .1, STONE, 3, draw=False),
            rect(x - 4, y + 2, 56, 26, "none", STONE, 1.5, 2, at + .1, style="inferred"), rect(x - 40, y - 24, 22, 14, WOOD, "#c9a87a", 1, 2, at + .2)]


def pic_latin(x, y, at):
    return [rect(x - 50, y - 18, 100, 36, "rgba(201,193,238,.06)", LILAC, 2, 18, at, style="claimed"), lab(x, y + 12, "L", at + .1, LILAC, 32, st="serif")]


def s47():
    """The ledger, row 1: reading sealed scrolls, Established; three reasons tick in: same letters, read by specialists, the ink itself."""
    tr, tg, t1, t2, t3 = T("s47", "Can we read"), T("s47", "Established"), T("s47", "Independent teams"), T("s47", "specialists"), T("s47", "newest scans")
    els = [rect(110, 130, 1560, 600, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, tr, pic_roll, "reading sealed scrolls", "Established", tg, GRADE["established"])
    for k, (x, txt, t) in enumerate([(330, "same letters, separate teams", t1), (820, "read by specialists", t2), (1200, "the ink itself", t3)]):
        els += [tick(x, 300, t, GREEN, .8), lab(x + 30, 310, txt, t + .2, DIM, 25, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s48_add():
    """Row 2: a whole scroll, what survives of it, Strong evidence; the gap: an outside check."""
    tr, tg, to = T("s48", "A whole scroll"), T("s48", "Strong evidence"), T("s48", "outside scholars")
    return lrow(1, tr, pic_strip, "a whole scroll, what survives", "Strong evidence", tg, GRADE["strong"]) + tag(1540, LROWS[1], "outside check", to, AMBER, 24, "inferred")


def s49():
    """More books in the villa? The site in section (15 units a metre): today's town, about 20 m of rock, the villa's main floor
    (explored by tunnels) and two lower floors down to the old shore, dashed and still full of rock; boxes of rolls in a colonnade,
    as if being carried out; Plausible."""
    tp, tl, tb, tc = T("s49", "Plausible"), T("s49", "lower floors"), T("s49", "packed in boxes"), T("s49", "carrying them out")
    g, f = 170, 470
    layers = [{"d": 0, "c": "#45403a", "t": ""}, {"d": 100, "c": "#3c3833", "t": ""}, {"d": 200, "c": "#433c35", "t": ""}, {"d": f - g, "c": "#2f2a25", "t": ""}]
    els = pumice(80, 1700, g + 10, 790, 150, 9) + town(860, 1680, g, -1, 5)
    els += villa_rooms(200, 1000, f, .3, step=.03, wall_h=80)
    for k, (x0, x1, fl) in enumerate([(880, 1320, 570), (1130, 1600, 670)]):
        els += [rect(x0, fl - 80, x1 - x0, 80, "rgba(12,10,8,.55)", STONE, 2.5, 2, tl + .3 * k, fx="pop", style="inferred"),
                ln([(x0, fl), (x1, fl)], tl + .3 * k, STONE, 4, "inferred", .5)]
        els += [rect(x0 + 40 + 90 * j, fl - 70, 10, 64, "none", "rgba(201,168,122,.7)", 1.4, 1, tl + .3 * k + .1, style="inferred") for j in range(int((x1 - x0) / 90))]
    els += [lab(1300, 740, "lower floors, still full of rock", tl + .5, STONE, 28)] + qmark(1180, 560, tl + .9, 80)
    for k in range(3):
        bx = 560 + 86 * k
        els += [rect(bx, f - 44, 72, 42, WOOD, "#c9a87a", 1.5, 2, tb + .15 * k, fx="pop")]
        els += [circ(bx + 14 + 22 * j, f - 30, 8, PAP_D, "#8a6a3e", 1, tb + .15 * k + .1, fx="pop") for j in range(3)]
    els += [gl(680, f - 24, 120, tb, .45, "lamp"), lab(690, f + 44, "packed in boxes", tb + .3, GOLD, 30),
            arr([(548, f - 22), (440, f - 22), (360, f - 40)], tc, GOLD, 2.5, "claimed", .8)]
    els += chip(1450, 330, "Plausible", GRADE["plausible"], tp, 32)
    return {"base": "section", "ground": g, "tod": "night", "layers": layers, "lx": 100, "cam": CAM, "els": els}


def s50_add():
    """Rows 3 and 4: more books in the villa, Plausible; a great Latin library, Awaiting evidence."""
    tr4, tg4 = T("s50", "A great lost"), T("s50", "Awaiting evidence")
    els = lrow(2, .4, pic_villa, "more books in the villa", "Plausible", .9, GRADE["plausible"])
    els += lrow(3, tr4, pic_latin, "a great Latin library", "Awaiting evidence", tg4, GRADE["awaiting"])
    return els


def s51():
    """What would change our minds: outside scholars finding the same text; the method working scroll after scroll; a dig into the
    lower floors that finds a room of books."""
    t1, t2, t3 = T("s51", "Outside scholars"), T("s51", "The method working"), T("s51", "And a dig")
    els = [{"k": "cap", "x": 889, "y": 180, "t": "wanted", "c": BLUE, "in": .3}]
    for k, (x0, t, txt) in enumerate([(109, t1, "the same text"), (649, t2, "scroll after scroll"), (1189, t3, "a room of books")]):
        els += [rect(x0, 220, 480, 420, "rgba(159,208,255,.05)", BLUE, 2.5, 18, t - .2, fx="pop", style="inferred"), lab(x0 + 240, 610, txt, t + .3, BLUE, 28)]
    for k, x in enumerate((230, 470)):
        els += [person(x, 560, 150, t1 + .2 * k, SKIN), rect(x - 34, 440, 68, 48, "#efe3c8", "#8a7a5a", 1, 3, t1 + .3 + .2 * k, fx="pop"),
                glyphs(x - 26, 448, 52, 32, t1 + .4 + .2 * k, rows=3, cols=4, c="#5a4330", sw=1.6, seed=7)]
    els += [ln([(335, 458), (365, 458)], t1 + .8, GOLD, 3, draw=False), ln([(335, 472), (365, 472)], t1 + .8, GOLD, 3, draw=False)]
    for k in range(6):
        x = 700 + 76 * k
        els += roll_end(x, 430, 26, t2 + .1 * k, turns=5) + [tick(x, 360, t2 + .4 + .25 * k, GREEN, .8)]
    els += [rect(1209, 300, 440, 270, ROCK_D, "rgba(255,226,190,.3)", 1.5, 4, t3 - .1), ln([(1209, 300), (1649, 300)], t3, "rgba(255,226,190,.6)", 2, draw=False),
            poly([(1380, 300), (1460, 300), (1450, 470), (1390, 470)], "#120e0b", at=t3 + .2, fx="fill"),
            rect(1320, 470, 200, 80, "#1a130e", STONE, 2, 3, t3 + .6, fx="pop"), rect(1335, 500, 170, 6, WOOD, at=t3 + .7), rect(1335, 530, 170, 6, WOOD, at=t3 + .7)]
    els += [circ(1350 + 22 * j, 490 if j % 2 else 520, 8, AU, at=t3 + .8 + .04 * j, fx="pop") for j in range(8)] + [gl(1420, 510, 90, t3 + .9, .55, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


def s52():
    """The close: night in the villa's colonnade by the sea; three wooden boxes of rolls on the floor, one open, in lamp light."""
    gy = 690
    els = [{"k": "water", "y": 540, "h": 160, "op": .85, "in": -1}]
    els += [rect(250, 250, 1280, 42, "#7a7062", "#b8ab94", 1.5, 2, -1), rect(240, 236, 1300, 16, "#5a5248", at=-1)]
    for k in range(6):
        x = 320 + 228 * k
        els += [rect(x - 18, 292, 36, gy - 292, "#9a9080", "#c9bca4", 1, 2, -1), rect(x - 26, 282, 52, 12, "#a89c88", at=-1), rect(x - 24, gy - 10, 48, 10, "#a89c88", at=-1)]
    els += [gl(889, 640, 380, .2, .55, "lamp"), poly([(860, 676), (920, 676), (930, 664), (870, 660)], "#c9a06a", "#7a5a30", 1, .2), gl(905, 652, 46, .3, .95, "fire")]
    for k, bx in enumerate((540, 990, 1200)):
        els += [rect(bx, gy - 84, 170, 84, WOOD, "#c9a87a", 2, 3, .4 + .1 * k)]
        els += [ln([(bx + 6, gy - 42), (bx + 164, gy - 42)], .4 + .1 * k, "#4a3020", 2, draw=False)]
        if k == 1:
            els += [poly([(bx, gy - 84), (bx + 170, gy - 84), (bx + 192, gy - 146), (bx + 22, gy - 146)], "#7a5a3a", "#c9a87a", 1.5, .5)]
            els += [circ(bx + 22 + 25 * j, gy - 66 + (8 if j % 2 else 0), 12, PAP_D, "#8a6a3e", 1.2, .6 + .05 * j, fx="pop") for j in range(6)]
            els += [gl(bx + 85, gy - 64, 130, .8, .55, "lamp")]
    return {"base": "sky", "tod": "night", "ground": gy, "sun": False, "moon": [1520, 180, 26], "ridges": [], "groundc": "#2e2721", "cam": CAM, "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "So how do you", "s2"), (1, "Vesuvius buried a whole", "s3"), (1, "And in {2026", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "It belonged to", "s7"), (1, "The current of gas", "s8")], {"chapter": "Books of charcoal"}),
    (1, 1, "collision", "s9", [(0, "The king's men", "s10")], {}),
    (1, 2, "reversal", "s11", [(1, "That November", "s12")], {}),
    (1, 3, "cost", "s13", [], {}),
    (1, 4, "tag", "s14", [], {}),
    (2, 0, "world", "s15", [(1, "The first tries", "s16")], {"chapter": "Opening the unopenable"}),
    (2, 1, "collision", "s17", [(1, "It worked", "s18")], {}),
    (2, 2, "reversal", "s19", [(1, "His name was", "s20")], {}),
    (2, 3, "tag", "s21", [(1, "Infrared cameras", "s22")], {}),
    (3, 0, "world", "s23", [(1, "Follow one sheet", "s24")], {"chapter": "Unwrapping without touching"}),
    (3, 1, "collision", "s25", [(1, "Then, in {2015", "s26")], {}),
    (3, 2, "cost", "s27", [], {}),
    (3, 3, "reversal", "s28", [(1, "Second, teach", "s29")], {}),
    (4, 0, "world", "s30", [], {"chapter": "A word in the dark"}),
    (4, 1, "collision", "s31", [(1, "A twenty-one-year-old", "s32"), (2, "Letters rose", "s33"), (3, "Another contestant", "s34")], {}),
    (4, 2, "reversal", "s35", [(1, "It is about", "s36")], {}),
    (4, 3, "tag", "s37", [(1, "Other rolls", "s38")], {}),
    (5, 0, "world", "s39", [], {"chapter": "The first whole scroll"}),
    (5, 1, "collision", "s40", [(1, "Then they read", "s41")], {}),
    (5, 2, "reversal", "s42", [(1, "Its handwriting", "s43")], {}),
    (5, 3, "tag", "s44", [(1, "But could a computer", "s45"), (2, "It doesn't work", "s46")], {}),
    (6, 0, "weigh", "s47", [(1, "A whole scroll", "s48"), (2, "More books", "s49"), (3, "A great lost", "s50")], {"chapter": "The weighing"}),
    (6, 1, "test", "s51", [], {}),
    (6, 2, "close", "s52", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.15, 1005, 470], "s2_add"),
    "s8": ("s7", [1, 889, 500], "s8_add"),
    "s32": ("s31", [1, 889, 500], "s32_add"),
    "s40": ("s39", [1.3, 760, 500], "s40_add"),
    "s48": ("s47", [1, 889, 500], "s48_add"),
    "s50": ("s47", [1, 889, 500], "s50_add"),
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
    ep = {"id": "lf-herculaneum", "code": "LF.23", "series": script["series"], "title": script["title"], "case": "herculaneum-scrolls",
          "verdict": "solid", "claim": "Can we read ancient books that would crumble if anyone tried to open them?", "mood": "mystery",
          "hook_text": "How do you read *charcoal*?", "beats": beats, "shots": shots,
          "sources": "Angelotti et al. 2026 (arXiv:2606.29085) · Vesuvius Challenge 2023, 2024, 2026 · Nicolardi et al. 2024 (Cronache Ercolanesi 54) · "
                     "Seales et al. 2016 (doi:10.1126/sciadv.1601247) · Mocella et al. 2015 (doi:10.1038/ncomms6895) · Parker et al. 2019 (doi:10.1371/journal.pone.0215775) · "
                     "Giordano et al. 2018 (doi:10.1016/j.epsl.2018.03.023) · Paderni 1753 (Phil. Trans. 48) · Sider 2005 · Janko 2002 · Moran 2024 (doi:10.1017/S2058631023000703)",
          "post": "A Roman library baked into charcoal by Vesuvius, and the long effort to read it: the tunnels of the 1750s, Piaggio's unrolling machine, "
                  "Philodemus, X-ray scans and the En-Gedi scroll, black ink on a black page, the Vesuvius Challenge and its first word, and the first "
                  "scroll read end to end, weighed.",
          "hashtags": ["#Herculaneum", "#Vesuvius", "#VesuviusChallenge", "#AncientRome", "#Archaeology", "#WeighItYourself"],
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
