"""LF.18 · Myths That Came True · Knossos: The Palace Behind the Myth (16:9 long film, one wall).

The script is films/long/lf-knossos/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at the
sentence where the picture changes (see BEATS). One scene per script shot (s1..s57; s5, the title, is the intro card over the panel
of s4), drawn while it is said: the Bull-Leaping Fresco as the hero image, the myth as black-figure friezes and a maze, the dates of the
written versions on one axis, Philochorus's general Taurus, Thucydides' sea of Minos, Kalokairinos's jars and Evans's seal stones, the
Throne Room and the first tablets, the palace as a model and as a plan beside three football pitches, timber and 1920s concrete sorted
from what is Minoan, the repainted griffins and dolphins, a jigsaw, a balance, the bulls (the fresco closer, a bull's-head vessel,
horns of consecration, the leap as moments), the double axe and the word chain labrys > labyrinthos with its doubts, Linear A and a
Finnish menu, the schoolboy Ventris, Kober's endings and the BBC, the Mycenaeans at Knossos, the honey tablet KN Gg 702, the
inverted tribute, the Minoan reach and the Keftiu, Thera erupting, Greater London under 20 m of rock, the radiocarbon and archaeology
windows, the fires of about 1450 BCE, the coins of Knossos, the ledger, the broken chain and the tests. Drawings are schematic and true
to the numbers said: solid = found, dashed = inferred or rebuilt, dotted = claimed (the story is lilac and dotted throughout).

Facts: the Short 'knossos' (f11.py, rewrite/knossos.json) and the script's facts_added (Evans 1901, 1921-1935; MacGillivray 2000;
Castleden 1990; Ventris & Chadwick 1953, 1956; Chadwick 1958; Kerenyi 1976; Manning et al. 2006; Pearson et al. 2018; Plutarch,
Thucydides, Ovid, Homer; Heraklion Archaeological Museum; British School at Athens).

Engine workaround (as in lf_troy.py): the wall only adds elements to a panel on its first visit, at a beat start or a line start;
shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag, invisible); after
the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-knossos/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-knossos/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-knossos RC_FILMS_EPS=/tmp/claude-0/sbx_lf-knossos/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-knossos/boards python3 films.py long.lf_knossos
"""
import json, math, os, random, re
from films import View, _topo
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-knossos", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
TERRA, TERRA_D, BLK = "#c46d3a", "#9c4f26", "#1d130d"        # black-figure: clay and slip
STONE, STONE_D, GYPS = "#d6c49c", "#8c7656", "#e6dccb"        # limestone, its shade, gypsum
CONC, CONC_D = "#9aa3ab", "#6c757d"                            # 1920s concrete
COLRED, COLCAP = "#b0301e", "#1a1511"                          # the red columns and their black capitals
FIRE, ASH, CHAR = "#ff7a4a", "#4a1d12", "#160d09"
SKIN, WOOD, WOOD_D = "#e8d6b8", "#6b4a30", "#3a281a"
CLAY, CLAY_D, INK = "#b08e64", "#8a6a48", "#4a3522"
BRONZE, HONEY, SILVER = "#c98a4a", "#d9902e", "#c9ccd1"
SEAC = "#3f86a8"
FIELD, SKIN_W, SKIN_R, HAIR = "#a9cbd5", "#f1e2cb", "#b4552e", "#1c130d"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c35a", "open": "#f0b06a", "ruled": "#e98a8a"}


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


def grp(els, at, fx=None, op=None, dur=None, tr=None):
    """A group: its children appear together, on the group's own clock (fx draw traces every path in it at once)."""
    e = {"k": "group", "els": els, "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    if dur:
        e["dur"] = dur
    if tr:
        e["tr"] = tr
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def E(cx, cy, rx, ry, n=36):
    return ellipse(cx, cy, rx, ry, n)[:-1]


def chip(x, y, t, c, at, size=28, a="middle"):
    """A pill with a coloured rim and its words (grades, dates)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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


def crown(x, y, s, at, c=GOLD, fx="pop"):
    return poly([[x - s, y], [x - s, y - s * 1.1], [x - s * .5, y - s * .5], [x, y - s * 1.2], [x + s * .5, y - s * .5], [x + s, y - s * 1.1], [x + s, y]], c, at=at, fx=fx)


def balance(cx, py, L, base_y, at, left=None, right=None, drop=170, pan=200, c=BONE):
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


def flame(x, y, s, at, c=FIRE):
    """A small flame glyph standing on y."""
    return [poly([[x, y], [x - .45 * s, y - .35 * s], [x - .25 * s, y - .8 * s], [x - .05 * s, y - .55 * s], [x + .05 * s, y - 1.1 * s], [x + .35 * s, y - .6 * s],
                  [x + .45 * s, y - .3 * s]], c, "#ffd08a", 1.5, at, fx="pop", curve=True), gl(x, y - .5 * s, 1.6 * s, at, .5, "fire")]


def scroll(x, y, w, h, at, c="#e9d6ad", fx="pop"):
    """A small rolled scroll seen from the side, partly open."""
    return [rect(x, y, w, h, c, "#8a6a3e", 1.5, 3, at, fx=fx), {"k": "glyphs", "x": round(x + w * .12, 1), "y": round(y + h * .15, 1), "w": round(w * .76, 1),
            "h": round(h * .7, 1), "rows": 4, "cols": 5, "kind": "latin", "c": "#6a5a44", "in": round(at + .1, 2)},
            rect(x - 8, y - 6, 16, h + 12, "#c9ad7d", "#8a6a3e", 1.5, 8, at, fx=fx), rect(x + w - 8, y - 6, 16, h + 12, "#c9ad7d", "#8a6a3e", 1.5, 8, at, fx=fx)]


def meander(x0, x1, y, h, at, c=BLK, u=46, w=4):
    """A running Greek key between x0 and x1, height h, top at y."""
    out = [ln([[x0, y + h], [x1, y + h]], at, c, w, draw=False), ln([[x0, y - 6], [x1, y - 6]], at, c, w * .6, draw=False)]
    x = x0
    while x + u <= x1 + .1:
        out.append(ln([[x, y + h], [x, y], [x + .72 * u, y], [x + .72 * u, y + .66 * h], [x + .3 * u, y + .66 * h], [x + .3 * u, y + .34 * h]], at, c, w, draw=False))
        x += u
    return out


def galley(x, y, w, at, c=BLK, face=-1, sail=None):
    """A ship in silhouette, bow towards `face`; y = the waterline; `sail` = a sail colour on the mast."""
    f = face
    X = lambda a: x + f * a * w
    hull = [[X(-.52), y + .01 * w], [X(-.42), y + .045 * w], [X(.3), y + .045 * w], [X(.46), y - .02 * w], [X(.5), y - .12 * w], [X(.47), y - .2 * w], [X(.43), y - .19 * w],
            [X(.45), y - .12 * w], [X(.4), y - .05 * w], [X(-.4), y - .05 * w], [X(-.46), y - .11 * w], [X(-.5), y - .1 * w], [X(-.47), y - .03 * w]]
    out = [poly(hull, c, at=at, curve=False), ln([[X(.02), y - .05 * w], [X(.02), y - .5 * w]], at, c, max(2, .012 * w), draw=False)]
    if sail:
        out.append(poly([[X(-.16), y - .47 * w], [X(.2), y - .47 * w], [X(.17), y - .2 * w], [X(-.13), y - .2 * w]], sail, "rgba(255,236,206,.35)", 1.2, at, curve=False))
    else:
        out.append(ln([[X(-.16), y - .44 * w], [X(.2), y - .44 * w]], at, c, max(2, .01 * w), draw=False))
    out += [ln([[X(-.34 + .07 * k), y + .02 * w], [X(-.39 + .07 * k), y + .1 * w]], at, c, max(1.5, .007 * w), draw=False) for k in range(10)]
    return out


def woman(x, y, h, at, c=BLK, fx=None):
    """A standing woman in a long robe, in silhouette."""
    return [poly([[x - .07 * h, y - .78 * h], [x + .07 * h, y - .78 * h], [x + .19 * h, y], [x - .19 * h, y]], c, at=at, fx=fx),
            circ(x, y - .87 * h, .075 * h, c, at=at, fx=fx), poly([[x - .02 * h, y - .97 * h], [x + .1 * h, y - .9 * h], [x + .14 * h, y - .6 * h], [x + .07 * h, y - .62 * h]], c, at=at, fx=fx)]


def bullhead(X, Y, at, c, edge, ew, fx=None, style="known", op=None, k=1.0):
    """A bull's head in profile (facing +x through X), horns curving up and forward; X/Y map the figure's units."""
    head = [(X(-.07), Y(.80)), (X(-.08), Y(.9)), (X(-.02), Y(.97)), (X(.06), Y(.97)), (X(.14), Y(.93)), (X(.24), Y(.86)), (X(.29), Y(.82)), (X(.28), Y(.77)),
            (X(.2), Y(.76)), (X(.08), Y(.78))]
    hornA = [(X(.0), Y(.95)), (X(-.05), Y(1.04)), (X(-.01), Y(1.13)), (X(.08), Y(1.17)), (X(.03), Y(1.1)), (X(.02), Y(1.03)), (X(.05), Y(.96))]
    hornB = [(X(-.05), Y(.93)), (X(-.12), Y(1.0)), (X(-.11), Y(1.09)), (X(-.05), Y(1.14)), (X(-.07), Y(1.06)), (X(-.04), Y(1.0)), (X(-.01), Y(.94))]
    ear = [(X(-.05), Y(.9)), (X(-.15), Y(.93)), (X(-.06), Y(.86))]
    return [poly(hornB, c, edge, ew, at, fx=fx, style=style, op=op, curve=True), poly(head, c, edge, ew, at, fx=fx, style=style, curve=True, op=op),
            poly(hornA, c, edge, ew, at, fx=fx, style=style, op=op, curve=True), poly(ear, c, edge, ew, at, fx=fx, style=style, op=op)]


def minotaur(x, y, h, at, c=BLK, fx=None, style="known", face=1, op=None, edge="none", ew=0):
    """The Minotaur in silhouette: a man's body and a bull's head with horns; feet on y, facing `face`."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    legs = [[(X(-.12), Y(0)), (X(-.04), Y(0)), (X(.0), Y(.46)), (X(-.1), Y(.46))], [(X(.05), Y(0)), (X(.14), Y(0)), (X(.08), Y(.46)), (X(-.02), Y(.46))]]
    kilt = [(X(-.12), Y(.4)), (X(.12), Y(.4)), (X(.1), Y(.52)), (X(-.1), Y(.52))]
    torso = [(X(-.1), Y(.5)), (X(.1), Y(.5)), (X(.16), Y(.78)), (X(-.14), Y(.8))]
    arms = [[(X(-.12), Y(.76)), (X(-.22), Y(.58)), (X(-.18), Y(.42))], [(X(.13), Y(.76)), (X(.27), Y(.66)), (X(.34), Y(.74))]]
    out = [poly(L, c, edge, ew, at, fx=fx, style=style, op=op) for L in legs]
    out += [poly(kilt, c, edge, ew, at, fx=fx, style=style, op=op), poly(torso, c, edge, ew, at, fx=fx, style=style, op=op, curve=False)]
    out += [ln(a, at, c if c != "none" else edge, max(3, .055 * h), style, draw=False, op=op) for a in arms]
    out += bullhead(X, Y, at, c, edge, ew, fx, style, op)
    return out


def soldier(x, y, h, at, c="#d8c9ae", face=1, fx="rise", op=None, bull=False, edge="none", ew=0, style="known"):
    """A soldier standing in profile: helmet and crest, cloak, short tunic, an upright spear; feet on y. bull=True gives him a bull's head
    (his shadow as the monster)."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    P = lambda pts: [(X(a), Y(b)) for a, b in pts]
    out = [poly(P([(-.03, .76), (-.2, .3), (-.08, .34)]), c, edge, ew, at, fx=fx, op=op, style=style),
           poly(P([(-.07, 0), (.0, 0), (.02, .45), (-.08, .45)]), c, edge, ew, at, fx=fx, op=op, style=style),
           poly(P([(.05, 0), (.12, 0), (.06, .45), (-.02, .45)]), c, edge, ew, at, fx=fx, op=op, style=style),
           poly(P([(-.1, .38), (.1, .38), (.09, .52), (-.09, .52)]), c, edge, ew, at, fx=fx, op=op, style=style),
           poly(P([(-.09, .5), (.08, .5), (.1, .78), (-.1, .78)]), c, edge, ew, at, fx=fx, op=op, style=style),
           ln(P([(.07, .74), (.16, .62), (.2, .66)]), at, c if c != "none" else edge, max(3, .045 * h), style, draw=False, op=op),
           ln(P([(.2, -.02), (.2, 1.12)]), at, c if c != "none" else edge, max(2.5, .022 * h), style, draw=False, op=op),
           poly(P([(.2, 1.12), (.17, 1.04), (.23, 1.04)]), c, edge, ew, at, fx=fx, op=op, style=style)]
    if bull:
        out += bullhead(X, Y, at, c, edge, ew, fx, style, op)
    else:
        out += [poly(P([(-.02, .78), (.04, .78), (.04, .82), (-.02, .82)]), c, edge, ew, at, fx=fx, op=op, style=style),
                circ(X(.02), Y(.87), .065 * h, c, edge, ew, at, fx=fx, op=op, style=style),
                poly(P([(-.07, .87), (-.06, .93), (.0, .96), (.07, .93), (.08, .87)]), c, edge, ew, at, fx=fx, op=op, style=style, curve=True),
                poly(P([(.05, .95), (.0, 1.04), (-.12, 1.03), (-.18, .9), (-.1, .97), (-.02, .97)]), c, edge, ew, at, fx=fx, op=op, style=style, curve=True)]
    return out


def king(x, y, h, at, c=BLK, face=1, fx=None, sceptre=True):
    """A seated king on a throne, in silhouette, crowned; feet on y."""
    f = face
    X = lambda a: x + f * a * h
    out = [poly([(X(-.32), y), (X(-.28), y), (X(-.28), y - .32 * h), (X(.05), y - .32 * h), (X(.05), y), (X(.1), y), (X(.1), y - .38 * h), (X(-.24), y - .38 * h),
                 (X(-.26), y - .9 * h), (X(-.32), y - .9 * h)], c, at=at, fx=fx),
           poly([(X(-.2), y - .36 * h), (X(.02), y - .36 * h), (X(.0), y - .72 * h), (X(-.16), y - .72 * h)], c, at=at, fx=fx),
           poly([(X(-.04), y - .38 * h), (X(.2), y - .38 * h), (X(.2), y - .3 * h), (X(.16), y), (X(.1), y), (X(.12), y - .3 * h), (X(-.04), y - .3 * h)], c, at=at, fx=fx),
           circ(X(-.08), y - .8 * h, .075 * h, c, at=at, fx=fx), crown(X(-.08), y - .86 * h, .06 * h, at, c, fx=fx)]
    if sceptre:
        out.append(ln([(X(.12), y - .02 * h), (X(.18), y - .95 * h)], at, c, max(2.5, .02 * h), draw=False))
        out.append(ln([(X(-.02), y - .62 * h), (X(.15), y - .55 * h)], at, c, max(3, .05 * h), draw=False))
    return out


def warrior(x, y, h, at, face=1, c=BLK, inc=TERRA, fx=None):
    """A soldier in silhouette: crested helmet, round shield, spear; feet on y, facing `face`."""
    f = face
    X = lambda a: x + f * a
    out = [ln([[X(0), y - .46 * h], [X(-.12 * h), y]], at, c, .07 * h, draw=False), ln([[X(0), y - .46 * h], [X(.12 * h), y]], at, c, .07 * h, draw=False),
           poly([[X(-.09 * h), y - .46 * h], [X(.09 * h), y - .46 * h], [X(.12 * h), y - .8 * h], [X(-.1 * h), y - .8 * h]], c, at=at, fx=fx),
           circ(X(.02 * h), y - .88 * h, .075 * h, c, at=at, fx=fx),
           poly([[X(-.05 * h), y - .95 * h], [X(-.02 * h), y - 1.04 * h], [X(-.22 * h), y - 1.0 * h], [X(-.3 * h), y - .86 * h], [X(-.12 * h), y - .93 * h]], c, at=at, curve=True, fx=fx),
           ln([[X(-.32 * h), y - .2 * h], [X(.5 * h), y - 1.12 * h]], at, c, .03 * h, draw=False),
           circ(X(.16 * h), y - .62 * h, .19 * h, c, at=at, fx=fx),
           circ(X(.16 * h), y - .62 * h, .13 * h, "none", inc, 1.5, at, op=.7)]
    return out


# ================================================================== the fresco: the Bull-Leaping Fresco of Knossos (schematic, its known layout)
BULL_BODY = [(-314, 44), (-306, 62), (-276, 60), (-246, 44), (-222, 66), (-196, 86), (-160, 96), (-110, 88), (-40, 74), (40, 66), (110, 56), (150, 44),
             (190, 50), (232, 34), (252, 0), (246, -34), (205, -56), (120, -62), (20, -66), (-80, -80), (-130, -94), (-176, -80), (-214, -56), (-246, -28),
             (-276, -6), (-298, 18)]
BULL_LEGS = [[(-170, 64), (-235, 104), (-314, 108)], [(-138, 76), (-210, 118), (-284, 130)], [(200, 26), (266, 64), (342, 64)], [(170, 40), (234, 92), (310, 104)]]
BULL_HORNS = [[(-250, -30), (-262, -66), (-282, -104), (-278, -132), (-262, -148)], [(-236, -38), (-246, -78), (-258, -114), (-246, -142)]]
BULL_TAIL = [(244, -30), (276, -66), (300, -108), (292, -142)]
BULL_PATCH = [[(-182, -62), (-124, -84), (-96, -42), (-118, 2), (-160, 12), (-192, -24)],
              [(-34, -60), (48, -62), (72, -28), (44, 2), (-8, -4), (-42, -30)],
              [(118, -54), (202, -54), (226, -18), (196, 16), (142, 12), (114, -20)],
              [(-96, 52), (-44, 46), (-30, 66), (-82, 76)], [(-262, -12), (-236, -16), (-226, 14), (-256, 22)]]


def _dense(pts, n=6):
    """A Catmull-Rom curve through pts, n steps a segment."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)
                             for j in range(2)))
    out.append(tuple(pts[-1]))
    return out


def taper(pts, w0, w1, c, at, edge="none", ew=0, op=None, style="known", power=1.0, fx=None):
    """A smooth limb, horn or tail: a curve through pts whose width runs from w0 (start) to w1 (end), one filled outline."""
    d = _dense(pts, 6)
    L = [0.0]
    for (x0, y0), (x1, y1) in zip(d, d[1:]):
        L.append(L[-1] + math.hypot(x1 - x0, y1 - y0))
    tot = L[-1] or 1
    left, right = [], []
    for i, (x, y) in enumerate(d):
        a_ = d[max(0, i - 1)]; b_ = d[min(len(d) - 1, i + 1)]
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
        n_ = math.hypot(dx, dy) or 1
        nx, ny = -dy / n_, dx / n_
        t = L[i] / tot
        w = (w1 + (w0 - w1) * (1 - t) ** power) / 2
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    return poly(left + right[::-1], c, edge, ew, at, fx=fx, curve=False, style=style, op=op)


def _leg(p, w, at, c, style="known", op=None):
    """A leg or an arm as one smooth tapered shape: (top, joint, end), widths w = (top, joint, end) as half widths."""
    return [taper(p, 2 * w[0], 2 * w[2], c, at, "rgba(46,32,22,.45)", 1.0, op, style, power=1.4)]


def bull(cx, cy, s, at, face=-1, body="#f1e6cf", patch="#4a3022", edge="#2e2016", fx=None, style="known", detail=True, op=None):
    """The bull of the fresco in flying gallop: legs stretched fore and aft, head low, long horns. face=-1 runs left (as painted)."""
    m = 1 if face == -1 else -1
    P = lambda q: (cx + m * q[0] * s, cy + q[1] * s)
    out = []
    shade = "#d2c3a4" if detail else body
    for lg in BULL_LEGS[1::2]:
        out += _leg([P(q) for q in lg], (25 * s, 11 * s, 7 * s), at, shade, style, op)
    for lg in BULL_LEGS[0::2]:
        out += _leg([P(q) for q in lg], (28 * s, 12 * s, 7.5 * s), at, body, style, op)
    out.append(poly([P(q) for q in BULL_BODY], body, edge, max(1.5, 2.6 * s), at, fx=fx, curve=True, style=style, op=op))
    for lg in BULL_LEGS:
        hx, hy = P(lg[-1])
        out.append(poly(E(hx - m * 4 * s, hy, 11 * s, 7 * s, 12), edge, at=at, op=op))
    if detail:
        for pt in BULL_PATCH:
            out.append(poly([P(q) for q in pt], patch, at=at, curve=True, op=.9 if op is None else op))
        out.append(circ(*P((-268, 4)), 5 * s, "#f7efe0", "#1a120c", 1.5 * s, at))
        out.append(circ(*P((-268, 4)), 2.6 * s, "#1a120c", at=at))
        out.append(poly([P((-238, -24)), P((-212, -20)), P((-228, -8))], body, edge, 1.2 * s, at))
        out.append(ln([P((-310, 50)), P((-300, 52))], at, edge, 2 * s, draw=False))
    for hn in BULL_HORNS:
        pts = [P(q) for q in hn]
        out.append(taper(pts, 18 * s, 4 * s, "#f4ecdc" if detail else body, at, edge if detail else "none", 1.6 * s if detail else 0, op, style))
    out.append(taper([P(q) for q in BULL_TAIL], 6 * s, 3 * s, edge if detail else body, at, "none", 0, op, style))
    out.append(poly(E(*P(BULL_TAIL[-1]), 9 * s, 14 * s, 12), edge if detail else body, at=at, op=op))
    return out


# figure joints (bull frame of reference, facing left): head, shoulder, hip, near arm (elbow, hand), far arm, near leg (knee, foot), far leg
FIG_GRIP = dict(head=(-356, -106), sh=(-345, -80), hip=(-372, 14), elA=(-312, -104), haA=(-278, -114), elB=(-310, -90), haB=(-266, -100),
                knA=(-350, 66), ftA=(-326, 112), knB=(-392, 62), ftB=(-418, 104), face=1)
FIG_VAULT = dict(head=(-6, -102), sh=(2, -122), hip=(28, -207), elA=(-26, -98), haA=(-34, -74), elB=(26, -96), haB=(30, -73),
                 knA=(78, -240), ftA=(116, -216), knB=(58, -258), ftB=(40, -298), face=-1)
FIG_CATCH = dict(head=(368, -100), sh=(362, -74), hip=(374, 22), elA=(332, -66), haA=(296, -76), elB=(336, -54), haB=(300, -56),
                 knA=(354, 70), ftA=(338, 116), knB=(388, 70), ftB=(410, 114), face=-1)


def figure(J, skin, at, s, ox, oy, mirror=False, cloth="#d6a84e", hair=HAIR, style="known", op=None):
    """A Minoan youth in the fresco's manner: narrow waist, long dark hair, a loincloth; joints in the bull's frame (see FIG_*)."""
    m = -1 if mirror else 1
    P = lambda q: (ox + m * q[0] * s, oy + q[1] * s)
    sh, hip, hd = P(J["sh"]), P(J["hip"]), P(J["head"])
    dx, dy = hip[0] - sh[0], hip[1] - sh[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    wa = (sh[0] + .6 * dx, sh[1] + .6 * dy)
    hipw, waw, shw = 14 * s, 8 * s, 19 * s
    torso = [(sh[0] + nx * shw, sh[1] + ny * shw), (wa[0] + nx * waw, wa[1] + ny * waw), (hip[0] + nx * hipw, hip[1] + ny * hipw),
             (hip[0] - nx * hipw, hip[1] - ny * hipw), (wa[0] - nx * waw, wa[1] - ny * waw), (sh[0] - nx * shw, sh[1] - ny * shw)]
    kilt = [(wa[0] + nx * 11 * s, wa[1] + ny * 11 * s), (hip[0] + nx * 18 * s + dx / L * 14 * s, hip[1] + ny * 18 * s + dy / L * 14 * s),
            (hip[0] - nx * 18 * s + dx / L * 14 * s, hip[1] - ny * 18 * s + dy / L * 14 * s), (wa[0] - nx * 11 * s, wa[1] - ny * 11 * s)]
    shade = "#cdbb9f" if skin == SKIN_W else "#8f4224"
    out = []
    out += _leg([sh, P(J["elB"]), P(J["haB"])], (6 * s, 5 * s, 4 * s), at, shade, style, op)
    out += _leg([hip, P(J["knB"]), P(J["ftB"])], (9 * s, 7 * s, 5 * s), at, shade, style, op)
    out += [poly(torso, skin, "rgba(40,24,14,.5)", 1.2 * s, at, curve=True, style=style, op=op), poly(kilt, cloth, "rgba(40,24,14,.6)", 1.2 * s, at, style=style, op=op),
            ln([(wa[0] + nx * 9 * s, wa[1] + ny * 9 * s), (wa[0] - nx * 9 * s, wa[1] - ny * 9 * s)], at, "#2a6aa0", 3.2 * s, style, draw=False, op=op)]
    out += _leg([hip, P(J["knA"]), P(J["ftA"])], (9.5 * s, 7 * s, 5 * s), at, skin, style, op)
    out += _leg([sh, P(J["elA"]), P(J["haA"])], (6.5 * s, 5 * s, 4 * s), at, skin, style, op) + [circ(sh[0], sh[1], 8 * s, skin, at=at, style=style, op=op)]
    out += [ln([sh, hd], at, skin, 9 * s, style, draw=False, op=op), circ(hd[0], hd[1], 14 * s, skin, "rgba(40,24,14,.5)", 1.2 * s, at, style=style, op=op)]
    f = J["face"] * m
    hx0, hy0 = hd[0] - f * 8 * s, hd[1] - 9 * s
    for k in range(3):
        out.append(ln([(hx0 + f * k * 2 * s, hy0), (hd[0] - f * (16 + 4 * k) * s, hd[1] + 14 * s), (hd[0] - f * (10 + 6 * k) * s, hd[1] + (34 + 8 * k) * s),
                       (hd[0] - f * (20 + 5 * k) * s, hd[1] + (52 + 10 * k) * s)], at, hair, 3.6 * s, style, draw=False, curve=True, op=op))
    out.append(poly(E(hd[0] - f * 3 * s, hd[1] - 6 * s, 13 * s, 9 * s, 14), hair, at=at, curve=True, op=op))
    out.append(circ(hd[0] + f * 7 * s, hd[1] - 2 * s, 2.2 * s, "#1a120c", at=at, op=op))
    return out


FW, FH, FCX, FCY, FS = 884, 660, 448, 382, .92        # the fresco's size, its composition centre (from its top left) and scale
FB = 30                                                 # the border band's width


def fresco(ox, oy, k=1.0, at=-1, edge=True):
    """The Bull-Leaping Fresco (about 1450 BCE, Heraklion Museum), schematic: a banded border, a pale blue field, the bull in flying
    gallop and three youths: one grips the horns, one vaults over the back, one waits behind with arms out. Top left at (ox, oy)."""
    S = lambda x, y: (ox + x * k, oy + y * k)
    out = []
    if edge:
        out += [rect(ox + 10 * k, oy + 16 * k, FW * k, FH * k, "#000", at=at, op=.4),
                rect(ox, oy, FW * k, FH * k, "#25303b", "#0f1418", 2, 6 * k, at)]
        bx0, by0, bw, bh, t = 8, 8, FW - 16, FH - 16, FB
        out.append(rect(ox + bx0 * k, oy + by0 * k, bw * k, bh * k, "#eadcbf", at=at))
        cols = ["#2f6d9c", "#d99a36", "#b4482a", "#2f6d9c", "#e2c25e", "#b4482a"]
        n = 0
        for side in range(4):                          # 'veined stone' scales running round the band
            if side in (0, 2):
                y = by0 + t / 2
                y = y if side == 0 else by0 + bh - t / 2
                pts_ = [(bx0 + 14 + 20 * j, y) for j in range(int((bw - 18) / 20))]
            else:
                x = bx0 + t / 2 if side == 3 else bx0 + bw - t / 2
                pts_ = [(x, by0 + t + 6 + 20 * j) for j in range(int((bh - 2 * t - 4) / 20))]
            for (x_, y_) in pts_:
                c_ = cols[n % len(cols)]
                n += 1
                out.append(poly([S(x_ + 12 * math.cos(a), y_ + 12 * math.sin(a)) for a in [2 * math.pi * j / 14 for j in range(14)]], c_, "rgba(30,20,12,.35)", .8, at, op=.92))
        out += [rect(ox + (bx0 + t) * k, oy + (by0 + t) * k, (bw - 2 * t) * k, (bh - 2 * t) * k, "#1d2a38", at=at),
                rect(ox + (bx0 + t + 3) * k, oy + (by0 + t + 3) * k, (bw - 2 * t - 6) * k, (bh - 2 * t - 6) * k, "#c0552e", at=at),
                rect(ox + (bx0 + t + 7) * k, oy + (by0 + t + 7) * k, (bw - 2 * t - 14) * k, (bh - 2 * t - 14) * k, "#e2c25e", at=at)]
    fi = 8 + FB + 10
    out.append(rect(ox + fi * k, oy + fi * k, (FW - 2 * fi) * k, (FH - 2 * fi) * k, FIELD, at=at))
    # plaster losses: the painting survives in pieces (restored), shown as faint paler patches
    for (x, y, rx, ry, sd) in ((150, 150, 52, 34, 1), (720, 540, 64, 40, 2), (760, 150, 40, 26, 3)):
        rr = random.Random(sd)
        pts_ = [S(x + rx * (1 + .3 * rr.uniform(-1, 1)) * math.cos(a), y + ry * (1 + .3 * rr.uniform(-1, 1)) * math.sin(a)) for a in [2 * math.pi * j / 9 for j in range(9)]]
        out.append(poly(pts_, "#c6d9de", "rgba(60,80,90,.3)", 1, at, curve=False, op=.5))
    cx, cy, s = ox + FCX * k, oy + FCY * k, FS * k
    out += figure(FIG_CATCH, SKIN_W, at, s, cx, cy)
    out += bull(cx, cy, s, at)
    out += figure(FIG_GRIP, SKIN_W, at, s, cx, cy)
    out += figure(FIG_VAULT, SKIN_R, at, s, cx, cy)
    return out


def fresco_pt(ox, oy, k, q):
    """Where a point of the bull's frame (FIG_* / BULL_*) lands in the panel for a fresco at (ox, oy) scaled by k."""
    return (ox + FCX * k + q[0] * FS * k, oy + FCY * k + q[1] * FS * k)


# ================================================================== the story's maze: a square labyrinth with one way to the centre
def maze(n=9, seed=4):
    """A perfect maze on an n x n grid, carved from the centre; the entrance at the middle of the bottom edge.
    Returns (walls as [(x0, y0, x1, y1)] in cell units, the path from the entrance to the centre as cells, a dead-end detour)."""
    rnd = random.Random(seed)
    c0 = (n // 2, n // 2)
    seen, stack, open_ = {c0}, [c0], set()
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop(); continue
        q = rnd.choice(nb)
        open_.add(frozenset(((x, y), q))); seen.add(q); stack.append(q)
    walls = []
    for x in range(n):
        for y in range(n):
            if y == 0:
                walls.append((x, 0, x + 1, 0))
            if x == 0:
                walls.append((0, y, 0, y + 1))
            if x + 1 < n and frozenset(((x, y), (x + 1, y))) not in open_:
                walls.append((x + 1, y, x + 1, y + 1))
            elif x + 1 == n:
                walls.append((n, y, n, y + 1))
            if y + 1 < n and frozenset(((x, y), (x, y + 1))) not in open_:
                walls.append((x, y + 1, x + 1, y + 1))
            elif y + 1 == n and x != n // 2:
                walls.append((x, n, x + 1, n))
    start = (n // 2, n - 1)
    prev, todo = {start: None}, [start]
    while todo:
        c = todo.pop(0)
        x, y = c
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q not in prev and frozenset((c, q)) in open_:
                prev[q] = c; todo.append(q)
    path, c = [], c0
    while c is not None:
        path.append(c); c = prev[c]
    path = path[::-1]
    # a detour into a dead end: the longest branch leaving the path within its first half
    on = set(path)
    best = []
    for i, c in enumerate(path[:max(2, len(path) // 2)]):
        x, y = c
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q in on or frozenset((c, q)) not in open_:
                continue
            br, cur, last = [c, q], q, c
            while True:
                nxt = [r for r in ((cur[0] + 1, cur[1]), (cur[0] - 1, cur[1]), (cur[0], cur[1] + 1), (cur[0], cur[1] - 1))
                       if r != last and r not in on and frozenset((cur, r)) in open_]
                if not nxt:
                    break
                last, cur = cur, nxt[0]; br.append(cur)
            if len(br) > len(best):
                best = (i, br)
    return walls, path, best


MZ = maze(9, 4)


def maze_els(x0, y0, cs, at, c=GOLD, w=6, style="known", fx="draw", dur=1.6, op=None, n=9, walls=None):
    """The maze's walls as one group (fx draw: every wall traces itself at once)."""
    ws = walls if walls is not None else MZ[0]
    segs = [ln([(x0 + a * cs, y0 + b * cs), (x0 + c_ * cs, y0 + d * cs)], 0, c, w, style, draw=False) for a, b, c_, d in ws]
    return [grp(segs, at, fx, op, dur)]


def cell_pts(x0, y0, cs, cells):
    return [(x0 + (cx + .5) * cs, y0 + (cy + .5) * cs) for cx, cy in cells]


# ================================================================== the palace plan (metres; x east, y south; origin at the court's centre)
COURT = (-14, -26.5, 14, 26.5)                       # about 28 x 53 m


def _plan_rooms():
    """Rooms around the court, schematic: long storerooms on the west, a corridor, rooms of many sizes, a long north entrance."""
    rr = random.Random(23)
    rooms = []
    for j in range(18):                                # the west magazines: long narrow rooms off a north-south corridor
        y = -40 + j * 4.3
        rooms.append((-68 + (3 if j % 5 == 0 else 0), y, -47, y + 3.6))
    rooms.append((-46.5, -42, -43.5, 38))                # the long corridor
    def fill(x0, y0, x1, y1, mn=5.0, mx=11.0):
        y = y0
        while y < y1 - 2:
            h = min(rr.uniform(mn, mx), y1 - y)
            x = x0
            while x < x1 - 2:
                w = min(rr.uniform(mn, mx), x1 - x)
                rooms.append((round(x, 1), round(y, 1), round(x + w - .8, 1), round(y + h - .8, 1)))
                x += w
            y += h
    fill(-42, -40, -16, 36, 4.5, 9)                      # the west wing between the corridor and the court (the throne room block)
    fill(16, -48, 62, -6, 5, 10)                         # north-east: magazines and workshops
    fill(16, -4, 64, 40, 4, 9)                           # the east wing: staircases, halls, the domestic quarter
    fill(-40, -66, -5, -44, 5, 10)                       # north-west
    fill(5, -66, 40, -50, 5, 10)                         # north-east corner
    fill(-12, 30, 40, 58, 5, 11)                         # south
    fill(-60, 40, -16, 60, 5, 10)                        # south-west
    rooms.append((-3.5, -70, 3.5, -28))                  # the north entrance passage
    return rooms


PLAN_ROOMS = _plan_rooms()
PLAN_FOOT = [(-76, -52), (-48, -75), (48, -73), (72, -54), (76, -6), (72, 50), (48, 66), (-12, 70), (-70, 68), (-78, 40)]


def _area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2


PLAN_AREA = _area(PLAN_FOOT)                             # about 20,000 square metres (checked in film())


def plan_els(cx, cy, s, at, c=BONE, w=1.6, foot=True, court=True, fx="draw", dur=1.6, op=None, style="known", fill=None):
    """The palace in plan at (cx, cy), s units a metre: the outer line, the court, the rooms (one group: they trace at once)."""
    P = lambda x, y: (cx + x * s, cy + y * s)
    out = []
    if foot:
        out.append(poly([P(*q) for q in PLAN_FOOT], fill or "rgba(232,210,170,.07)", c, w * 1.6, at, curve=False, style=style, op=op))
    segs = []
    for (x0, y0, x1, y1) in PLAN_ROOMS:
        if x1 <= x0 or y1 <= y0:
            continue
        segs.append({"k": "rect", "x": round(cx + x0 * s, 1), "y": round(cy + y0 * s, 1), "w": round((x1 - x0) * s, 1), "h": round((y1 - y0) * s, 1),
                     "r": 0, "fill": "none", "c": c, "sw": w, "style": style})
    out.append(grp(segs, at, "fade" if fx == "draw" else fx, op, dur))
    if court:
        a, b, c2, d = COURT
        out.append(rect(cx + a * s, cy + b * s, (c2 - a) * s, (d - b) * s, "rgba(232,195,90,.10)", AU, w * 1.4, 0, at, op=op))
    return out


# ================================================================== Linear script, schematic: stroke signs in a unit box (y down)
def _ring(cx, cy, r, n=10):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]


SIGNS = [
    [_ring(.5, .5, .42), [(.5, .08), (.5, .92)], [(.08, .5), (.92, .5)]],
    [[(.5, 0), (.5, 1)], [(.15, .3), (.85, .3)], [(.25, .62), (.75, .62)]],
    [[(.5, 1), (.5, .08)], [(.5, .35), (.15, .12)], [(.5, .55), (.85, .3)], [(.5, .76), (.18, .56)]],
    [[(.15, .2), (.85, .2), (.85, .78), (.15, .78), (.15, .2)], [(.15, .78), (.85, .2)], [(.5, .78), (.5, 1)]],
    [[(.3, 1), (.3, 0)], [(.3, .05), (.85, .25), (.3, .45)]],
    [[(.15, 1), (.5, .15), (.85, 1)], [(.28, .62), (.72, .62)], [(.5, .15), (.5, 0)]],
    [[(.5, 1), (.5, .5)], [(.5, .5), (.2, .2)], [(.5, .5), (.85, .15)], _ring(.17, .17, .13, 8)],
    [[(.5, 1), (.5, .3)], [(.15, .04), (.15, .4), (.85, .4), (.85, .04)], [(.5, .04), (.5, .4)]],
    [[(.4, 1), (.4, .3)], [(.4, .3), (.45, .12), (.65, .08), (.78, .2), (.7, .36), (.55, .32)]],
    [[(.5, 0), (.8, .3), (.5, .6), (.2, .3), (.5, 0)], [(.5, .6), (.5, 1)], [(.3, .85), (.7, .85)]],
    [[(.2, 1), (.2, .4), (.5, .1), (.8, .4), (.8, 1)], _ring(.5, .62, .09, 8)],
    [[(.3, 0), (.3, 1)], [(.3, .15), (.7, .2), (.82, .45), (.7, .7), (.3, .75)]],
]


def sign_row(x, y, h, n, at, c=INK, w=2.4, seed=1, gap=.32, op=None, div=True):
    """n schematic syllabic signs in a row (Linear A/B style strokes, not real readings), top left at (x, y), each h tall, with a word divider
    after every 2 to 4 signs; returns (elements, the row's end x)."""
    rr = random.Random(seed)
    segs = []
    x0 = x
    nxt = rr.randint(2, 4)
    for j in range(n):
        sg = SIGNS[rr.randrange(len(SIGNS))]
        for st in sg:
            segs.append(ln([(x0 + u * h * .8, y + v * h) for u, v in st], 0, c, w, draw=False))
        x0 += h * (.8 + gap)
        nxt -= 1
        if div and nxt == 0 and j < n - 1:
            segs.append(ln([(x0 + h * .05, y + h * .72), (x0 + h * .05, y + h)], 0, c, w, draw=False))
            x0 += h * .3
            nxt = rr.randint(2, 4)
    return [grp(segs, at, "fade", op)], x0


def jar_sign(x, y, h, at, c=INK, w=2.4, fx="pop"):
    """The jar ideogram at the end of a line of a tablet (a two-handled jar), top left (x, y), h tall."""
    k = h
    body = [(x + .25 * k, y + .18 * k), (x + .55 * k, y + .18 * k), (x + .72 * k, y + .5 * k), (x + .58 * k, y + k), (x + .22 * k, y + k), (x + .08 * k, y + .5 * k)]
    return [grp([poly(body, "none", c, w, 0, curve=True), ln([(x + .3 * k, y), (x + .5 * k, y)], 0, c, w, draw=False),
                 ln([(x + .27 * k, y + .04 * k), (x + .27 * k, y + .2 * k)], 0, c, w, draw=False), ln([(x + .53 * k, y + .04 * k), (x + .53 * k, y + .2 * k)], 0, c, w, draw=False),
                 ln([(x + .14 * k, y + .3 * k), (x - .02 * k, y + .22 * k), (x + .1 * k, y + .55 * k)], 0, c, w, draw=False, curve=True),
                 ln([(x + .66 * k, y + .3 * k), (x + .82 * k, y + .22 * k), (x + .7 * k, y + .55 * k)], 0, c, w, draw=False, curve=True)], at, fx)]


def clay_tablet(x, y, w, h, at, c=CLAY, fx="pop", op=None, edge="#e9dccb", seed=1):
    """A flat clay tablet: an irregular baked edge, a darker thickness below, a crack, a speckle."""
    rr = random.Random(seed)
    r = min(w, h) * .18
    pts = []
    for (cx, cy, a0) in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for j in range(5):
            a = math.radians(a0 + 22.5 * j)
            k = 1 + rr.uniform(-.08, .08)
            pts.append((cx + r * k * math.cos(a), cy + r * k * math.sin(a)))
    thick = [(px + 5, py + 9) for px, py in pts]
    out = [poly(thick, "#5a4430", at=at, fx=fx, op=.9 if op is None else op, curve=True),
           poly(pts, c, edge, 1.4, at, fx=fx, curve=True, op=op)]
    if w > 120:
        out.append(poly(pts, "url(#k-speck)", at=at, curve=True, op=.5))
        cx0 = x + w * rr.uniform(.6, .8)
        out.append(ln([(cx0, y + 3), (cx0 - 8, y + h * .2), (cx0 + 4, y + h * .32)], at, "rgba(60,40,24,.6)", 1.4, draw=False))
    return out


def honey_jar(x, y, s, at, glow_=True, fx="pop"):
    """A clay jar of honey (a stirrup jar's simple cousin): body, neck, two handles, an amber glow."""
    body = [(x - 40 * s, y - 60 * s), (x + 40 * s, y - 60 * s), (x + 56 * s, y - 18 * s), (x + 34 * s, y + 40 * s), (x - 34 * s, y + 40 * s), (x - 56 * s, y - 18 * s)]
    out = [poly(body, "#9a5a32", "#e9c58a", 1.6, at, fx=fx, curve=True), rect(x - 22 * s, y - 84 * s, 44 * s, 28 * s, "#8a4e2a", "#e9c58a", 1.4, 5 * s, at, fx=fx),
           ln([(x - 40 * s, y - 56 * s), (x - 62 * s, y - 64 * s), (x - 50 * s, y - 26 * s)], at, "#8a4e2a", 6 * s, draw=False, curve=True),
           ln([(x + 40 * s, y - 56 * s), (x + 62 * s, y - 64 * s), (x + 50 * s, y - 26 * s)], at, "#8a4e2a", 6 * s, draw=False, curve=True),
           poly([(x - 30 * s, y - 70 * s), (x + 30 * s, y - 70 * s), (x + 22 * s, y - 50 * s), (x - 22 * s, y - 50 * s)], HONEY, at=at + .1, op=.9)]
    if glow_:
        out.insert(0, gl(x, y - 20 * s, 150 * s, at, .55, "lamp"))
    return out


def maze_room(n=9, seed=4):
    """The maze with a small open room at its centre (3 x 3 cells) for the monster; same entrance and path logic as maze()."""
    walls, path, det = maze(n, seed)
    c0, c1 = n // 2 - 1, n // 2 + 1
    keep = []
    for (a, b, c_, d) in walls:
        inner = (c0 < a < c1 + 1 and c0 <= b <= c1 + 1 and a == c_ and c0 <= min(b, d) and max(b, d) <= c1 + 1) or \
                (c0 < b < c1 + 1 and c0 <= a <= c1 + 1 and b == d and c0 <= min(a, c_) and max(a, c_) <= c1 + 1)
        if not inner:
            keep.append((a, b, c_, d))
    return keep, path, det


MZR = maze_room(9, 4)


def ring_of(lon, lat, maxpts=2000):
    """The land ring (lon, lat) that contains a point: an island's outline from the 50 m land data."""
    best = None
    for poly_ in _topo():
        r = poly_[0]
        if len(r) > maxpts:
            continue
        xs = [q[0] for q in r]; ys = [q[1] for q in r]
        if min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys):
            if best is None or len(r) > len(best):
                best = r
    return best


CRETE = ring_of(24.9, 35.25)
THERA = ring_of(25.43, 36.41, 200)

# sites (lon, lat)
KNOSSOS, THERA_P, AKROTIRI, ATHENS = (25.1631, 35.298), (25.43, 36.41), (25.403, 36.351), (23.727, 37.984)
MYCENAE, PYLOS, KYTHERA, RHODES = (22.756, 37.731), (21.668, 37.028), (22.99, 36.25), (28.13, 36.41)
PHAISTOS, MALIA, ZAKROS, HTRIADA = (24.814, 35.051), (25.492, 35.293), (26.261, 35.098), (24.793, 35.059)


def island(v, ring, at, fill="#5b4a37", c="rgba(255,226,190,.55)", w=1.6, curve=True, op=None, fx=None):
    return poly([v.p(*q) for q in ring], fill, c, w, at, curve=curve, op=op, fx=fx)


# ================================================================== COLD OPEN
FX0, FY0 = 508, 128          # the fresco's top left on the opening panel


def s1():
    """The hero image, complete from the first frame: the Bull-Leaping Fresco in lamp light; the acrobat's flight traces on 'flying'."""
    tf = T("s1", "flying")
    a, b, c = fresco_pt(FX0, FY0, 1, (-282, -150)), fresco_pt(FX0, FY0, 1, (12, -330)), fresco_pt(FX0, FY0, 1, (300, -130))
    els = [gl(950, 430, 760, -1, .2, "lamp")] + fresco(FX0, FY0) + [gl(700, 260, 420, -1, .1, "lamp")]
    arc = ln([a, b, c], tf, AU, 3.5, "inferred", 1.0, curve=True)
    arc["fx"] = "fade"                                   # a fade, not a draw: an undrawn path shows a stray round cap at its start
    els += [arc, dot(c[0], c[1], 6, AU, tf + .9)]
    els += chip(300, 712, "Knossos, about 1450 BCE", GOLD, tf + 1.0, 26)
    return {"base": "dark", "stars": 16, "cam": CAM, "els": els}


def bf_ground(y0=150, y1=760, at=-1):
    """A black-figure frieze: terracotta between two running meanders, as on a Greek vase."""
    els = [rect(88, y0 - 20, 1602, y1 - y0 + 40, "#2a1a10", "none", 0, 18, at),
           rect(100, y0, 1578, y1 - y0, TERRA, "rgba(255,226,190,.35)", 2, 10, at),
           rect(100, y0, 1578, 26, TERRA_D, at=at, op=.6), rect(100, y1 - 26, 1578, 26, TERRA_D, at=at, op=.6), gl(889, 450, 760, at, .16, "lamp")]
    els += meander(120, 1660, y0 + 16, 28, at) + meander(120, 1660, y1 - 50, 28, at)
    return els


def s2():
    """The story as the Greeks painted it: King Minos enthroned, a maze, and at its heart the Minotaur, half man, half bull."""
    tk, tm, th = T("s2", "a king"), T("s2", "maze"), T("s2", "half man")
    x0, y0, cs = 860, 226, 48
    els = bf_ground()
    els += king(400, 620, 320, tk - .2, BLK, face=1, fx="rise") + [lab(400, 668, "Minos", tk + .3, "#2a1a10", 34, st="ital", halo=False)]
    els += maze_els(x0, y0, cs, tm - .3, BLK, 6.5, walls=MZR[0], dur=1.4)
    els += minotaur(x0 + 4.5 * cs, y0 + 5.9 * cs, 118, th, BLK, fx="pop")
    els += [lab(x0 + 9 * cs + 40, y0 + 4.6 * cs, "the Minotaur", th + .4, "#2a1a10", 34, "start", st="ital", halo=False)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def tablet_KN(x, y, w, h, at, glow2=None, rows=(5, 7), sh=54):
    """The honey tablet, schematic: two lines of signs, each ending in the jar sign (the measure of honey)."""
    out = clay_tablet(x, y, w, h, at)
    out += [ln([(x + 26, y + h / 2), (x + w - 26, y + h / 2)], at + .05, "rgba(74,53,34,.5)", 1.5, draw=False)]
    for j, n in enumerate(rows):
        yy = y + 20 + j * (h / 2)
        row, xe = sign_row(x + 40, yy, sh, n, at + .15 + .1 * j, INK, 3, seed=11 + 5 * j)
        out += row + jar_sign(x + w - 40 - sh * .9, yy - 2, sh * 1.05, at + .3 + .1 * j, INK, 3)
    if glow2 is not None:
        out += [rect(x + 22, y + h / 2 + 8, w - 44, h / 2 - 22, "rgba(232,195,90,.22)", AU, 2.5, 8, glow2, fx="pop"),
                gl(x + w / 2, y + h * .75, w * .5, glow2, .4, "lamp")]
    return out


def s3():
    """A clay tablet from the same palace: honey, and on its second line, the Mistress of the Labyrinth."""
    th, tm = T("s3", "honey"), T("s3", "Mistress")
    els = [gl(760, 380, 640, .1, .28, "lamp")]
    els += tablet_KN(330, 250, 860, 250, .2, glow2=tm - .2)
    els += honey_jar(1420, 480, 1.25, th - .2)
    els += [lab(760, 572, "a tablet from Knossos", .7, DIM, 28), lab(760, 660, "the Mistress of the Labyrinth", tm + .2, GOLD, 44, st="serif", fx="rise")]
    return {"base": "dark", "stars": 24, "cam": CAM, "els": els}


def s4():
    """The story above, the ground below: the dotted maze of the myth floating over the plan of the palace, and the question."""
    tq = T("s4", "real place")
    cs = 30
    mx, my = 790, 140
    els = plan_els(889, 612, 2.25, .2, BONE, 1.6)
    els += [gl(889, 612, 420, .2, .14, "lamp"), gl(mx + 4.5 * cs, my + 4.5 * cs, 300, .5, .14, "lamp")]
    els += maze_els(mx, my, cs, .5, LILAC, 3.5, "claimed", "fade", .8, walls=MZR[0])
    els += [lab(mx - 40, my + 4.5 * cs + 10, "the story", .9, LILAC, 34, "end", st="ital"), lab(889 - 220, 620, "the ground", 1.1, BONE, 32, "end")]
    els += qmark(1330, 430, tq, 160)
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


# ================================================================== CHAPTER 1 · A monster in a maze
def waves(x0, x1, y, rows, at, c=BLK, w=4, amp=10, step=46):
    out = []
    for r in range(rows):
        yy = y + r * 26
        pts = []
        x = x0 + (r % 2) * step / 2
        while x <= x1:
            pts += [(x, yy), (x + step * .25, yy - amp), (x + step * .5, yy), (x + step * .75, yy + amp * .3)]
            x += step
        out.append(ln(pts, at, c, w, draw=False, curve=True))
    return out


def s6():
    """Black-figure: a snow-white bull rises from the waves; Minos at his altar; he keeps the bull, and the altar fire goes out."""
    tb, tk = T("s6", "snow-white bull"), T("s6", "kept it")
    els = bf_ground()
    els += bull(520, 470, .62, tb - .2, face=1, body="#f6efe2", edge="#2a1a10", fx="rise", detail=False)
    els += [rect(110, 548, 820, 152, TERRA, at=-1)] + waves(120, 920, 560, 5, -1)
    alt = (1240, 620)
    els += [rect(alt[0] - 60, alt[1] - 110, 120, 110, BLK, at=-1), rect(alt[0] - 74, alt[1] - 124, 148, 18, BLK, at=-1)]
    els += [poly([(alt[0] - 14, alt[1] - 124), (alt[0] - 26, alt[1] - 160), (alt[0] - 6, alt[1] - 150), (alt[0], alt[1] - 196), (alt[0] + 10, alt[1] - 150),
                  (alt[0] + 26, alt[1] - 166), (alt[0] + 16, alt[1] - 124)], BLK, at=-1, curve=True)]
    tm = T("s6", "sacrifice")
    els += [arr([(760, 420), (980, 380), (alt[0] - 30, alt[1] - 200)], tm - .3, "#2a1a10", 3, "claimed", .8), strike(900, 330, 1010, 420, tk + .3, "#2a1a10", 5)]
    kx = 1460
    els += woman(kx, 620, 300, .3, BLK) + [crown(kx, 348, 22, .3, BLK, fx=None), ln([(kx - 50, 450), (kx - 74, 320)], .3, BLK, 6, draw=False)]
    els += [lab(kx, 668, "Minos", .6, "#2a1a10", 34, st="ital", halo=False), lab(520, 236, "bull from the sea", tb + .6, "#2a1a10", 32, st="ital", halo=False)]
    els += [ln([(kx - 60, 480), (1150, 560), (900, 520), (780, 470)], tk + .6, "#f6efe2", 3, "claimed", 1.2, curve=True)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s7():
    """Black-figure: the queen, Pasiphae, and her son, the Minotaur: a man's body and a bull's head."""
    tq, tm = T("s7", "Pasiphae"), T("s7", "half man")
    els = bf_ground()
    els += bull(300, 500, .42, .2, face=1, body="#f6efe2", edge="#2a1a10", detail=False)
    els += woman(760, 620, 330, tq - .3, BLK, fx="rise") + [lab(760, 668, "Pasiphae", tq + .2, "#2a1a10", 34, st="ital", halo=False)]
    els += minotaur(1220, 620, 340, tm - .2, BLK, fx="rise") + [lab(1220, 668, "the Minotaur", tm + .5, "#2a1a10", 34, st="ital", halo=False)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


MX8, MY8, MC8 = 640, 158, 58          # the maze of s8 / s10: top left and cell size


def daedalus(x, y, h, at):
    out = [person(x, y, h, at, "#d9c7a6")]
    out += [ln([(x + .2 * h, y - .62 * h), (x + .36 * h, y - .62 * h), (x + .36 * h, y - .5 * h)], at, AU, 4, draw=False)]
    return out


def s8():
    """The Labyrinth in plan, in gold ink: Daedalus beside it with his square; a dotted path wanders in, doubles back, and stops at a '?'."""
    td, tc = T("s8", "Daedalus"), T("s8", "barely find")
    els = [gl(MX8 + 4.5 * MC8, MY8 + 4.5 * MC8, 560, .1, .22, "lamp")]
    els += maze_els(MX8, MY8, MC8, .3, GOLD, 6, walls=MZR[0], dur=1.6)
    els += daedalus(500, 690, 150, td - .3) + [lab(500, 740, "Daedalus", td + .2, BONE, 28)]
    i0, br = MZR[2]
    path = [(MX8 + 4.5 * MC8, MY8 + 9 * MC8 + 30)] + cell_pts(MX8, MY8, MC8, MZR[1][:i0 + 1] + br[1:])
    els += [ln(path, tc - .8, LILAC, 3.5, "claimed", 2.2)] + qmark(*cell_pts(MX8, MY8, MC8, [br[-1]])[0], tc + 1.2, 60)
    els += [lab(1460, 700, "in Ovid's telling", tc + .4, DIM, 26)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s10_add():
    """Ariadne's thread: Theseus walks it to the monster at the centre, a flash, and follows it back out."""
    tt, ta, tk, to = T("s10", "Theseus"), T("s10", "Ariadne"), T("s10", "killed"), T("s10", "back out")
    cx, cy = MX8 + 4.5 * MC8, MY8 + 4.5 * MC8
    ex, ey = MX8 + 4.5 * MC8, MY8 + 9 * MC8
    path = [(ex, ey + 40)] + cell_pts(MX8, MY8, MC8, MZR[1])
    back = [(x + 7, y + 7) for x, y in path[::-1]]
    els = minotaur(cx, cy + 50, 96, .4, "#2a2032", edge=LILAC, ew=2)
    els += soldier(ex + 70, 760, 110, tt - .2, "#d8c9ae", -1, "rise") + [lab(ex + 160, 720, "Theseus", tt + .2, LILAC, 28, "start", st="ital")]
    els += woman(ex - 90, 760, 110, ta - .2, "#d8c9ae", fx="rise") + [lab(ex - 160, 720, "Ariadne", ta + .2, LILAC, 28, "end", st="ital"),
                                                                       circ(ex - 70, 700, 11, RED, "#ffd0c0", 1.5, ta + .3, fx="pop")]
    els += [ln(path, ta + 1.0, RED, 3.5, dur=2.4), gl(cx, cy, 160, tk, .8, "fire"), ln(back, to - .4, "#ffb09a", 2.5, "inferred", 2.0)]
    return els


def s9():
    """The tribute: a ship with a black sail from Athens to Crete; seven and seven young people pop on its deck."""
    t7, t9, t1, tm = T("s9", "seven young men"), T("s9", "every nine years"), T("s9", "every year"), T("s9", "monster")
    els = [{"k": "water", "y": 560, "h": 300, "op": .9, "in": -1},
           poly([(80, 560), (80, 470), (180, 440), (300, 470), (360, 520), (390, 560)], "#2b2328", "rgba(255,226,190,.35)", 1.2, -1, curve=True),
           poly([(1460, 560), (1520, 500), (1610, 470), (1720, 480), (1720, 560)], "#2b2328", "rgba(255,226,190,.35)", 1.2, -1, curve=True),
           lab(230, 420, "Athens", .4, BONE, 30), lab(1600, 440, "Crete", .4, BONE, 30), gl(889, 420, 600, .1, .14, "lamp")]
    els += galley(889, 566, 560, .2, "#1a120c", face=1, sail="#0d0b09")
    for k in range(14):
        x = 889 - 210 + k * 30 + (14 if k >= 7 else 0)
        c = "#e8d6b8" if k < 7 else "#d9c7e8"
        els += [circ(x, 520, 8, c, at=t7 + .12 * k, fx="pop"), rect(x - 7, 526, 14, 18, c, r=4, at=t7 + .12 * k, fx="pop")]
    els += [lab(889 - 105, 470, "7", t7 + .9, BONE, 30, st="serif"), lab(889 + 119, 470, "7", t7 + 1.7, BONE, 30, st="serif")]
    els += [lab(560, 250, "every 9 years?", t9, LILAC, 32, st="ital"), lab(1220, 250, "every year?", t1, LILAC, 32, st="ital"),
            arr([(1200, 620), (1440, 580)], tm - .2, LILAC, 3, "claimed", .8)]
    return {"base": "dark", "stars": 70, "cam": CAM, "els": els}


def XT(yr):
    """The axis of s11/s12: 1500 BCE to 2100 CE across x 150..1630."""
    return round(150 + (yr + 1500) / 3600 * 1480, 1)


def vase(x, y, h, at, c=TERRA, fig=BLK, fx="pop"):
    """A black-figure amphora: body, neck, handles, a dark frieze band."""
    k = h
    body = [(x - .16 * k, y - k), (x + .16 * k, y - k), (x + .12 * k, y - .86 * k), (x + .3 * k, y - .6 * k), (x + .26 * k, y - .2 * k), (x + .1 * k, y - .04 * k),
            (x + .14 * k, y), (x - .14 * k, y), (x - .1 * k, y - .04 * k), (x - .26 * k, y - .2 * k), (x - .3 * k, y - .6 * k), (x - .12 * k, y - .86 * k)]
    return [poly(body, c, "#2a1a10", 1.5, at, fx=fx, curve=True), rect(x - .26 * k, y - .62 * k, .52 * k, .22 * k, fig, at=at + .05, fx=fx),
            ln([(x - .14 * k, y - .95 * k), (x - .3 * k, y - .9 * k), (x - .26 * k, y - .7 * k)], at, "#2a1a10", max(2, .03 * k), draw=False, curve=True),
            ln([(x + .14 * k, y - .95 * k), (x + .3 * k, y - .9 * k), (x + .26 * k, y - .7 * k)], at, "#2a1a10", max(2, .03 * k), draw=False, curve=True)]


def dancers(cx, cy, r, n, at, c=DIM):
    out = [poly(E(cx, cy + 6, r + 26, (r + 26) * .32, 30), "rgba(232,195,90,.12)", "rgba(232,195,90,.5)", 1.5, at, curve=True)]
    for k in range(n):
        a = 2 * math.pi * k / n
        x, y = cx + r * math.cos(a), cy + r * .3 * math.sin(a)
        out.append(person(round(x, 1), round(y, 1), 30, at + .04 * k, c))
    return out


def s11():
    """One axis from 1500 BCE to today: Homer around 700 BCE knows Minos and a dancing floor at Knossos; no maze, no monster."""
    th, tf, tn = T("s11", "Homer"), T("s11", "dancing floor"), T("s11", "Not a word")
    y = 560
    ticks = [[XT(v), t] for v, t in ((-1500, "1500 BCE"), (-500, "500 BCE"), (500, "500 CE"), (1500, "1500 CE"))]
    els = [axis(150, 1630, y, ticks, .2), gl(XT(-700), 420, 300, th - .3, .25, "lamp")]
    els += scroll(XT(-700) - 56, y - 92, 112, 60, min(th - .3, .8)) + [lab(XT(-700), y - 118, "Homer", min(th, 1.0), GOLD, 36)]
    els += dancers(XT(-700), 330, 70, 8, tf - .3) + [lab(XT(-700) + 140, 300, "a dancing floor", tf + .3, DIM, 26, "start")]
    els += [lab(XT(-700) + 140, 210, "maze? monster?", tn - 1.6, LILAC, 30, "start", st="ital"), strike(XT(-700) + 130, 214, XT(-700) + 360, 194, tn, RED, 4)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s12_add():
    """The painters by about 550 BCE; Plutarch about 100 CE; the palace's last fire about 1350 BCE; over 14 centuries between;
    and the same span again, from the fall of Rome (476) to today."""
    tv, tp, tf, tr = T("s12", "Vase painters"), T("s12", "Plutarch"), T("s12", "last great"), T("s12", "fall of Rome")
    y = 560
    els = vase(XT(-550) + 40, y - 18, 64, tv)
    els += scroll(XT(100) - 40, y - 74, 80, 44, tp - .3) + [lab(XT(100), y - 96, "Plutarch", tp, GOLD, 30)]
    els += flame(XT(-1350), y - 8, 46, tf - .3) + [lab(XT(-1350), y - 80, "last fire", tf, FIRE, 26)]
    els += [ln([(XT(-1350), y + 70), (XT(100), y + 70)], tf + .5, RED, 14, dur=1.2), lab((XT(-1350) + XT(100)) / 2, y + 118, "over 14 centuries", tf + 1.2, RED, 30),
            ln([(XT(476), y + 70), (XT(2026), y + 70)], tr - .2, BLUE, 14, dur=1.2), lab((XT(476) + XT(2026)) / 2, y + 118, "Rome's fall to today", tr + .5, BLUE, 30)]
    return els


def s13():
    """Philochorus's version, in Plutarch: the Labyrinth a prison; the 'monster' a hated general, Taurus; a lamp throws his shadow, with horns."""
    tp, tg, tt, tb = T("s13", "prison"), T("s13", "hated general"), T("s13", "Taurus"), T("s13", "Greek for bull")
    g = 700
    els = [rect(140, 150, 1500, g - 150, "url(#k-blocks)", "rgba(255,236,206,.25)", 1.5, 6, -1, op=.55), ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False),
           gl(700, 560, 520, .1, .3, "lamp")]
    dx, dw = 260, 260
    els += [poly([(dx, g), (dx, 330), (dx + dw / 2, 250), (dx + dw, 330), (dx + dw, g)], "#120d0a", "#8c7656", 3, .3)]
    els += [ln([(dx + 30 + 40 * k, g), (dx + 30 + 40 * k, 290 + abs(k - 2.5) * 14)], tp - .2 + .06 * k, "#6c757d", 7, draw=False) for k in range(6)]
    els += [lab(dx + dw / 2, 760, "a prison", tp + .2, BONE, 30)]
    # a small oil lamp on the floor; the general; his shadow on the wall, taller, with a bull's head
    els += [poly(E(700, g - 10, 34, 12, 16), "#8a6a48", "#d8b88a", 1.5, .3), poly([(730, g - 16), (752, g - 20), (736, g - 8)], "#8a6a48", at=.3),
            gl(748, g - 34, 60, .3, .9, "fire"), poly([(744, g - 22), (740, g - 40), (748, g - 56), (756, g - 40), (752, g - 22)], "#ffd08a", at=.3, curve=True)]
    els += soldier(1400, g, 440, tt - .5, "rgba(16,10,6,.6)", -1, "rise", bull=True)
    els += soldier(980, g, 300, tg - .3, "#d8c9ae", -1, "rise") + [lab(980, 760, "Taurus", tt + .2, LILAC, 32, st="ital")]
    els += chip(760, 220, "tauros = bull", GOLD, tb, 28)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


VAE = View(21.5, 29.5, 34.6, 39.6, (90, 120, 1600, 680))


def s14():
    """Thucydides' Minos: a fleet fanning out from Crete over the Cyclades; master of the sea, as he tells it."""
    v = VAE
    tt, tn, ts = T("s14", "Thucydides"), T("s14", "navy"), T("s14", "Greek sea")
    kx, ky = v.p(*KNOSSOS)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += [lab(*v.p(24.6, 35.05), "Crete", .5, "#c9ad85", 34, st="ital"), lab(*v.p(25.0, 37.95), "Cyclades", .8, "#9fd0ff", 30, st="ital"),
            {"k": "pin", "x": v.p(*ATHENS)[0], "y": v.p(*ATHENS)[1], "t": "Athens", "c": BONE, "a": "end", "lx": -18, "in": .6}]
    for k, q in enumerate(((25.38, 37.08), (24.42, 36.72), (25.27, 37.42), (26.4, 36.85), (23.4, 36.9))):
        tx, ty = v.p(*q)
        els += [ln([(kx, ky - 10), ((kx + tx) / 2 + 30, (ky + ty) / 2), (tx, ty)], tn - .4 + .2 * k, LILAC, 2.5, "claimed", .9, curve=True)]
        els += galley(tx, ty, 70, tn + .4 + .2 * k, "#e8d6b8", face=1 if tx > kx else -1)
    els += [gl(*v.p(25.3, 36.8), 420, ts - .3, .25, "lamp"), lab(*v.p(27.6, 37.55), "master of the sea?", ts, LILAC, 34, st="ital")]
    els += chip(1360, 640, "Thucydides, 400s BCE", GOLD, tt, 26)
    els += [{"k": "pin", "x": kx, "y": ky, "t": "", "c": GOLD, "in": .4}, {"k": "scale", "x": 160, "y": 760, "w": round(v.km(100), 1), "t": "100 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def spade(x, y, at, s=1.0):
    return [ln([(x, y - 170 * s), (x, y - 40 * s)], at, "#8a6a48", 7 * s, draw=False), ln([(x - 22 * s, y - 170 * s), (x + 22 * s, y - 170 * s)], at, "#8a6a48", 7 * s, draw=False),
            poly([(x - 26 * s, y - 44 * s), (x + 26 * s, y - 44 * s), (x + 22 * s, y + 6 * s), (x, y + 22 * s), (x - 22 * s, y + 6 * s)], "#9aa0a8", "#e9dccb", 1.5, at)]


def s15_add():
    """The story fades to a ghost (a feathered veil); the ground plan brightens; a spade bites into the ground."""
    td = T("s15", "dig under")
    veil = [rect(760 - 14 * k, 112 - 14 * k, 330 + 28 * k, 330 + 28 * k, "#0f0c0a", r=40 + 10 * k, at=.3, op=.16) for k in range(6)]
    return veil + [gl(889, 612, 420, .5, .38, "lamp"), grp(spade(1180, 760, 0, 1.0), td - .4, "rise", dur=.7)]


# ================================================================== CHAPTER 2 · Digging for Minos
def olive(x, y, h, at, c="#4f6a3e"):
    return [ln([(x, y), (x - .04 * h, y - .4 * h)], at, "#5a4632", max(3, .07 * h), draw=False),
            poly(E(x - .05 * h, y - .62 * h, .42 * h, .3 * h, 16), c, "rgba(30,40,20,.4)", 1, at, curve=True),
            poly(E(x + .16 * h, y - .52 * h, .28 * h, .2 * h, 14), "#5d7a48", at=at, curve=True, op=.9)]


def pithos(x, base, h, at, fx="rise"):
    """A tall storage jar (pithos) with rope bands."""
    w = .42 * h
    body = [(x - .3 * w, base - h), (x + .3 * w, base - h), (x + .52 * w, base - .75 * h), (x + .46 * w, base - .25 * h), (x + .22 * w, base), (x - .22 * w, base),
            (x - .46 * w, base - .25 * h), (x - .52 * w, base - .75 * h)]
    out = [poly(body, "#b07c52", "#e9c58a", 1.5, at, fx=fx, curve=True)]
    out += [ln([(x - .5 * w, base - f * h), (x + .5 * w, base - f * h)], at + .1, "#7a4e2e", 3, draw=False) for f in (.62, .45, .3)]
    out += [rect(x - .34 * w, base - h - 8, .68 * w, 10, "#9a6a44", r=4, at=at, fx=fx)]
    return out


def s16():
    """Kephala hill by day, the sea beyond; Minos Kalokairinos, 1878, opens a trench and finds storerooms of giant jars."""
    tm, tj = T("s16", "Minos Kalokairinos"), T("s16", "storerooms")
    g = 650
    hill = [(560, g), (700, 590), (860, 556), (1060, 540), (1260, 548), (1440, 586), (1600, g)]
    els = [{"k": "water", "y": 600, "h": 52, "x0": 0, "x1": 520, "op": .85, "in": -1},
           poly(hill, "#7a7048", "rgba(240,248,220,.6)", 2, -1, curve=True)]
    for k, (x, h) in enumerate(((620, 90), (760, 110), (1450, 100), (1540, 84), (300, 70), (420, 80), (1660, 90))):
        els += olive(x, g + 4 if x < 560 or x > 1590 else g - 10, h, -1)
    tx0, tx1, tb = 980, 1240, 640
    els += [poly([(tx0, 548), (tx1, 550), (tx1 - 10, tb), (tx0 + 10, tb)], "#3a2a1e", "rgba(255,226,190,.5)", 1.5, tm - .2, fx="pop")]
    for k, x in enumerate((1020, 1080, 1140, 1200)):
        els += pithos(x, tb, 74, tj + .25 * k)
    kx = 1330
    els += [person(kx, g, 112, tm - .4, SKIN), ln([(kx + 26, g), (kx + 40, g - 96)], tm - .3, "#8a6a48", 4, draw=False),
            lab(kx + 10, 700, "Minos Kalokairinos", tm + .2, BONE, 28), lab(1110, 500, "storerooms", tj + .8, AMBER, 28)]
    els += chip(kx + 10, 470, "1878", GOLD, tm + .5, 26)
    # a locator: Crete, the hill near its north coast
    v = View(23.4, 26.4, 34.8, 35.75, (1330, 160, 330, 100))
    els += [rect(1310, 130, 370, 200, "rgba(18,24,30,.82)", "rgba(255,236,206,.45)", 1.5, 12, -1), island(v, CRETE, -1, "#6b5b44", "rgba(255,236,206,.6)", 1.2, curve=True),
            dot(*v.p(*KNOSSOS), 7, GOLD, -1), lab(1495, 310, "Crete", -1, DIM, 24)]
    return {"base": "sky", "tod": "day", "ground": g, "sun": [1180, 230, 30], "cam": CAM, "els": els}


def seal(x, y, r, at, c, seed=1):
    """A lentoid seal stone with small engraved signs."""
    out = [poly(E(x, y, r, r * .92, 28), c, "rgba(255,236,206,.6)", 2, at, curve=True, fx="pop"), poly(E(x - r * .3, y - r * .35, r * .35, r * .18, 12), "#ffffff", at=at, op=.18)]
    row, _ = sign_row(x - r * .55, y - r * .28, r * .52, 2, at + .2, "rgba(30,18,10,.8)", 3.2, seed=seed, gap=.5)
    return out + row


def s17():
    """1900: Arthur Evans, Keeper of the Ashmolean, comes hunting a script; three seal stones engraved with signs."""
    te, ts = T("s17", "Arthur Evans"), T("s17", "seal stones")
    g = 700
    els = [gl(500, 420, 520, .1, .3, "lamp"), ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False),
           rect(140, g - 120, 300, 120, WOOD, "#8a6a48", 1.5, 4, .2), rect(170, g - 150, 90, 30, "#d9c9a6", "#8a7a66", 1, 2, .3)]
    ex = 560
    els += [person(ex, g, 330, te - .5, "#cbbca8"), rect(ex - 30, g - 352, 60, 24, "#1a1511", r=6, at=te - .5, fx="rise"),
            rect(ex - 44, g - 332, 88, 8, "#1a1511", r=3, at=te - .5, fx="rise"), ln([(ex + 64, g), (ex + 82, g - 200)], te - .4, "#8a6a48", 6, draw=False)]
    els += [lab(ex, 760, "Arthur Evans", te + .2, BONE, 30)] + chip(ex, 200, "March 1900", GOLD, te - .2, 26)
    for k, (x, c) in enumerate(((1060, "#b5523a"), (1290, "#7f9e8c"), (1520, "#c9a46a"))):
        els += seal(x, 420, 92, ts - .2 + .25 * k, c, seed=3 + k) + [gl(x, 420, 160, ts + .25 * k, .3, "lamp")]
    els += [lab(1290, 590, "seal stones", ts + .6, AMBER, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def throne(x, base, h, at, fx="pop", c=GYPS):
    """The gypsum throne of Knossos in elevation: a high back with a wavy edge, a seat, set against the wall."""
    k = h
    back = [(x - .2 * k, base - .42 * k), (x - .2 * k, base - .7 * k), (x - .26 * k, base - .82 * k), (x - .18 * k, base - .9 * k), (x - .22 * k, base - 1.0 * k),
            (x - .08 * k, base - 1.08 * k), (x, base - 1.0 * k), (x + .08 * k, base - 1.08 * k), (x + .22 * k, base - 1.0 * k), (x + .18 * k, base - .9 * k),
            (x + .26 * k, base - .82 * k), (x + .2 * k, base - .7 * k), (x + .2 * k, base - .42 * k)]
    seat = [(x - .3 * k, base - .42 * k), (x + .3 * k, base - .42 * k), (x + .26 * k, base - .34 * k), (x + .22 * k, base), (x - .22 * k, base), (x - .26 * k, base - .34 * k)]
    return [poly(back, c, "#8c7f6c", 2, at, fx=fx, curve=True), poly(seat, c, "#8c7f6c", 2, at, fx=fx, curve=False)]


def griffin(x, y, s, at, c="#e8d2a0", edge="#5a3a22", style="known", op=None, w=2, face=-1):
    """A couchant griffin as in the Throne Room, facing `face`: a lion's body lying, forelegs out, a long raised neck, an eagle's hooked
    beak, a crest of curling plumes; (x, y) the middle of its belly line."""
    m = 1 if face == -1 else -1
    P = lambda a, b: (x + m * a * s, y + b * s)
    body = [P(-70, 0), P(-80, -30), P(-60, -58), P(0, -66), P(70, -62), P(120, -56), P(150, -40), P(160, -10), P(150, 6), P(110, 10), P(40, 8), P(-30, 8)]
    neck = [P(-60, -50), P(-84, -96), P(-96, -140), P(-90, -168), P(-66, -170), P(-58, -140), P(-40, -96), P(-30, -60)]
    head = [P(-90, -168), P(-110, -172), P(-132, -166), P(-140, -152), P(-128, -156), P(-116, -150), P(-96, -146), P(-80, -152), P(-66, -170)]
    fore = [P(-70, 2), P(-150, 6), P(-170, 0), P(-150, -8), P(-80, -12)]
    hind = [P(110, 8), P(70, 14), P(30, 12), P(60, 0), P(120, -2)]
    tail = ln([P(156, -30), P(200, -50), P(214, -90), P(196, -110)], at, edge, w, style, draw=False, curve=True, op=op)
    crest = [ln([P(-70, -168), P(-40, -196), P(-10, -196), P(-4, -178), P(-20, -174)], at, edge, w, style, draw=False, curve=True, op=op),
             ln([P(-64, -156), P(-30, -168), P(0, -160), P(4, -144), P(-12, -144)], at, edge, w, style, draw=False, curve=True, op=op),
             ln([P(-56, -140), P(-26, -138), P(-6, -126), P(-10, -112), P(-24, -116)], at, edge, w, style, draw=False, curve=True, op=op)]
    return [poly(body, c, edge, w, at, curve=True, style=style, op=op), poly(hind, c, edge, w, at, curve=True, style=style, op=op),
            poly(fore, c, edge, w, at, curve=True, style=style, op=op), poly(neck, c, edge, w, at, curve=True, style=style, op=op),
            poly(head, c, edge, w, at, curve=True, style=style, op=op), tail] + crest + [circ(*P(-104, -160), 3.5 * s, edge, at=at, op=op)]


def lily(x, y, h, at, c="#f1e4c4", edge="#5a3a22", style="known", op=None, w=2):
    return [ln([(x, y), (x + 4, y - h)], at, edge, w, style, draw=False, op=op),
            poly([(x + 4, y - h), (x - 16, y - h - 22), (x - 4, y - h - 10), (x + 4, y - h - 30), (x + 12, y - h - 10), (x + 24, y - h - 22)], c, edge, w * .8, at, style=style, op=op)]


def s18():
    """April 1900: a box of clay tablets; and a stone seat against a painted wall, the room Evans called the Throne Room."""
    tt, ts, tr = T("s18", "tablets"), T("s18", "stone seat"), T("s18", "Throne Room")
    g = 690
    els = [gl(420, 520, 360, .1, .25, "lamp"), ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False)]
    bx = 220
    els += [rect(bx, g - 120, 360, 120, WOOD, "#8a6a48", 2, 4, .3), rect(bx - 10, g - 132, 380, 18, WOOD_D, "#8a6a48", 1.5, 3, .3),
            rect(bx + 20, g - 240, 300, 110, WOOD_D, "#8a6a48", 1.5, 3, .35, op=.8)]
    for k in range(9):
        x = bx + 30 + 36 * k
        els += clay_tablet(x, g - 112 - (k % 3) * 8, 30, 90, tt - .3 + .08 * k, CLAY)
    els += [lab(bx + 180, 740, "clay tablets", tt + .4, BONE, 28)] + chip(bx + 180, 420, "April 1900", GOLD, tt + .2, 26)
    # the Throne Room: red wall, griffins among lilies (dim), benches, the throne
    rx0, rx1 = 760, 1640
    els += [rect(rx0, 220, rx1 - rx0, g - 220, "#7e2c1c", "rgba(255,236,206,.25)", 1.5, 4, .2), rect(rx0, g - 60, rx1 - rx0, 60, "#d8cdb8", "#8c7f6c", 1.5, 0, .3),
            ln([(rx0, 300), (rx1, 300)], .3, "rgba(255,236,206,.3)", 2, draw=False)]
    for gx_, f in ((1010, -1), (1390, 1)):
        els += griffin(gx_, 560, .95, .5, "#e3c98e", "#3a1a10", op=.55, face=f)
    els += sum([lily(x, 600, 70, .5, op=.5) for x in (860, 940, 1490, 1570)], [])
    els += [rect(rx0 + 20, g - 50, 260, 50, GYPS, "#8c7f6c", 1.5, 2, ts - .2), rect(rx1 - 280, g - 50, 260, 50, GYPS, "#8c7f6c", 1.5, 2, ts - .2)]
    els += throne(1200, g, 250, ts) + [gl(1200, g - 160, 200, ts, .35, "lamp")]
    els += [lab(1200, 196, "the Throne Room", tr, BONE, 32), lab(1200, 760, "Evans's name", tr + .4, DIM, 24)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def _room_h(x0, y0, x1, y1):
    r = random.Random(int(abs(x0 * 7 + y0 * 13)))
    if x1 < -46.5:
        return 4.0                                         # the west storerooms: one high storey
    if x0 > 14 and y0 > -6:
        return r.choice([7.0, 10.5, 10.5, 14.0])           # the east wing, cut into the slope: up to four storeys
    return r.choice([3.5, 7.0, 7.0, 10.5])


def iso_palace():
    items = [{"t": "flat", "pts": [list(q) for q in PLAN_FOOT], "y": -.2, "c": "#6b5a42"}]
    a, b, c_, d = COURT
    items.append({"t": "flat", "pts": [[a, b], [c_, b], [c_, d], [a, d]], "y": .05, "c": "#e2cf9e"})
    for (x0, y0, x1, y1) in PLAN_ROOMS:
        if x1 - x0 < 1 or y1 - y0 < 1:
            continue
        h = _room_h(x0, y0, x1, y1)
        col = random.Random(int(x0 * 3 + y1 * 5)).choice(["#d9c9a6", "#cbb893", "#e2d3b0", "#d2bf98"])
        items.append({"t": "box", "x": (x0 + x1) / 2, "z": (y0 + y1) / 2, "y": 0, "w": x1 - x0, "d": y1 - y0, "h": h, "c": col, "edge": "rgba(40,30,20,.35)"})
    items.append({"t": "line", "p": [[c_ + 2, 0.2, b], [c_ + 2, 0.2, d]], "c": AU, "w": 3})
    items.append({"t": "label", "x": 0, "y": 0, "z": 0, "text": "central court", "st": "lab", "c": GOLD, "dy": 8})
    return items


def s19():
    """The maze Evans uncovered, as a model: hundreds of rooms on several storeys around a central court about 50 m long."""
    tc, ts = T("s19", "central court"), T("s19", "several storeys")
    els = [gl(889, 520, 640, .1, .22, "lamp"),
           {"k": "iso", "x": 889, "y": 470, "s": 4.6, "az": -32, "spin": .7, "el": .5, "items": iso_palace(), "in": .2, "fx": "rise", "dur": 1.0}]
    els += [lab(889, 770, "about 50 m long", tc + .3, AU, 30), lab(1480, 220, "several storeys", ts, DIM, 28)]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


PL20 = (470, 430, 2.9)       # the plan of s20/s21: centre and units a metre


def pitch(x, y, w, h, at):
    """A football pitch from above (105 x 68 m), lines drawn on green."""
    return [grp([rect(x, y, w, h, "#3f6b3a", "#e9f0e0", 2, 2, 0), ln([(x + w / 2, y), (x + w / 2, y + h)], 0, "#e9f0e0", 2, draw=False),
                 circ(x + w / 2, y + h / 2, h * .13, "none", "#e9f0e0", 2, 0), rect(x, y + h * .3, w * .15, h * .4, "none", "#e9f0e0", 2, 0, 0),
                 rect(x + w * .85, y + h * .3, w * .15, h * .4, "none", "#e9f0e0", 2, 0, 0)], at, "pop", dur=.5)]


def s20():
    """One scale: the palace's footprint (about 20,000 square metres) beside three football pitches (105 x 68 m each)."""
    ta, tp = T("s20", "twenty thousand"), T("s20", "three football")
    cx, cy, s = PL20
    els = plan_els(cx, cy, s, .2, BONE, 1.4) + [gl(cx, cy, 360, .2, .12, "lamp")]
    pw, ph = 105 * s, 68 * s
    for k in range(3):
        els += pitch(1000, 152 + k * (ph + 14), pw, ph, tp - .2 + .4 * k)
    els += [lab(cx, 690, "about 20,000 m²", ta, GOLD, 32), lab(1000 + pw + 24, 152 + 1.5 * ph + 14, "3 pitches", tp + 1.0, "#bfe3a8", 30, "start"),
            {"k": "scale", "x": cx - 72, "y": 750, "w": round(50 * s, 1), "t": "50 m", "in": .8}]
    return {"base": "plan", "north": [1660, 220], "cam": CAM, "els": els}


def s21_add():
    """Close on the plan: a tiny walker turns and turns through the rooms, lost; the footprint glimmers lilac: Evans's Labyrinth?"""
    tg, te = T("s21", "Get lost"), T("s21", "Evans believed")
    cx, cy, s = PL20
    P = lambda x, y: (cx + x * s, cy + y * s)
    walk = [P(-3, -72), P(-3, -42), P(-12, -36), P(-12, -30), P(-30, -30), P(-30, -12), P(-20, -12), P(-20, 4), P(-36, 4), P(-36, 20), P(-24, 22), P(-24, 34)]
    els = [ln(walk, tg - .3, AU, 3.5, "claimed", 2.4), person(*walk[-1], 24, tg + 1.8, "#f2e4c8")] + qmark(walk[-1][0] + 18, walk[-1][1] - 28, tg + 2.2, 40, halo=False)
    els += [poly([P(*q) for q in PLAN_FOOT], "none", LILAC, 4, te, style="claimed", fx="draw", dur=1.4), gl(cx, cy, 300, te, .2, "lamp"),
            lab(cx + 120, cy - 120, "the Labyrinth?", te + .6, LILAC, 30, "start", st="ital")]
    return els


def wall_blocks(x, y, w, h, at, c="url(#k-blocks)", edge="rgba(255,236,206,.45)", fx=None, op=None):
    return rect(x, y, w, h, c, edge, 1.2, 1, at, fx=fx, op=op)


def column(x, top, base, at, c=COLRED, cap=COLCAP, w0=30, w1=40, fx="rise", style="known", edge="#e9dccb", op=None):
    """A Minoan column: wider at the top (w1) than at the foot (w0), a dark cushion capital and base."""
    return [poly([(x - w0 / 2, base - 10), (x + w0 / 2, base - 10), (x + w1 / 2, top + 26), (x - w1 / 2, top + 26)], c, edge, 1.5, at, fx=fx, style=style, op=op),
            rect(x - w1 / 2 - 8, top, w1 + 16, 26, cap, edge, 1.2, 10, at, fx=fx, op=op), rect(x - w0 / 2 - 4, base - 12, w0 + 8, 12, cap, edge, 1, 3, at, fx=fx, op=op)]


S22_G = 700
S22_COLS = (1060, 1210, 1360, 1510)


def s22():
    """As found in 1900, then propped with timber; then rebuilt in the 1920s in reinforced concrete: walls, columns, roofs, upper floors."""
    tf, tt, tc = T("s22", "much of what"), T("s22", "timber"), T("s22", "reinforced concrete")
    tw, tcol, tr, tu = T("s22", "walls"), T("s22", "columns"), T("s22", "roofs"), T("s22", "upper floors")
    g = S22_G
    els = [ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False), gl(400, 560, 320, .1, .2, "lamp"), gl(1240, 480, 520, .1, .16, "lamp")]
    # left: the ruin as found, then timber props
    for k, (x, w, h) in enumerate(((150, 90, 110), (270, 70, 70), (380, 110, 130), (520, 80, 60))):
        els.append(wall_blocks(x, g - h, w, h, .2 + .05 * k))
    els += chip(360, 368, "1900", GOLD, .5, 26)
    for k, x in enumerate((210, 330, 470)):
        els.append(rect(x - 8, g - 250, 16, 250, WOOD, "#c9a46a", 1.2, 2, tt - .3 + .15 * k, fx="rise"))
    els += [rect(150, g - 262, 420, 16, WOOD, "#c9a46a", 1.2, 2, tt + .2, fx="pop"), rect(180, g - 300, 360, 38, "#9c8a6a", "rgba(255,236,206,.4)", 1.2, 2, tt + .4, fx="pop")]
    els += [lab(360, 760, "timber", tt + .5, "#c9a46a", 28)]
    # right: the building: Minoan lower walls with the stone seat, then concrete
    x0, x1 = 900, 1660
    els += [wall_blocks(x0, g - 190, 120, 190, .3), wall_blocks(x1 - 140, g - 190, 140, 190, .3), wall_blocks(x0 + 120, g - 40, x1 - x0 - 260, 40, .3)]
    els += throne(1180, g - 40, 130, .5) + [rect(1260, g - 40 - 26, 220, 26, GYPS, "#8c7f6c", 1.2, 2, .5)]
    els += [rect(x0, g - 230, 120, 40, CONC, CONC_D, 1.5, 0, tw, fx="rise"), rect(x1 - 140, g - 230, 140, 40, CONC, CONC_D, 1.5, 0, tw + .1, fx="rise"),
            rect(x0 - 10, g - 250, x1 - x0 + 20, 22, CONC, CONC_D, 1.5, 0, tw + .3, fx="pop")]
    for k, x in enumerate(S22_COLS):
        els += column(x, g - 430, g - 250, tcol + .2 * k)
    els += [rect(x0 - 20, g - 452, x1 - x0 + 40, 24, CONC, CONC_D, 1.5, 0, tr, fx="pop"),
            rect(x0 - 10, g - 600, x1 - x0 + 20, 148, "rgba(154,163,171,.06)", CONC, 2.5, 0, tu, style="inferred"),
            ln([(x0 + 250, g - 600), (x0 + 250, g - 452)], tu + .2, CONC, 2, "inferred", .4), ln([(x0 + 520, g - 600), (x0 + 520, g - 452)], tu + .3, CONC, 2, "inferred", .4)]
    els += chip(1280, 140 + 26, "1920s: concrete", "#b9c4cc", tc, 26)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s23_add():
    """Sorted: the stone seat and lower walls glow gold (Minoan); the columns are 1920s concrete copies of wooden ones wider at the top."""
    tm, tc = T("s23", "Minoan", k=2), T("s23", "red columns")
    g = S22_G
    els = [rect(900 - 6, g - 196, 132, 202, "none", AU, 4, 6, tm - .3, fx="pop"), rect(1520 - 6, g - 196, 152, 202, "none", AU, 4, 6, tm - .2, fx="pop"),
           gl(1180, g - 110, 200, tm - .2, .45, "lamp"), lab(1180, 778, "Minoan", tm, AU, 32)]
    for k, x in enumerate(S22_COLS):
        els += [rect(x - 34, g - 440, 68, 196, "none", BLUE, 2.5, 6, tc + .15 * k, style="inferred", fx="pop")]
    els += [lab(1556, 404, "copies", tc + .7, BLUE, 30, "start")]
    # the Minoan original: a tree trunk, wider at the top than at the foot
    els += [poly([(250, 318), (282, 318), (296, 166), (236, 166)], "#8a5a36", "#d8b88a", 1.5, tc + 1.4, fx="rise"),
            rect(226, 148, 80, 20, "#5a3a22", "#d8b88a", 1.2, 8, tc + 1.4, fx="rise"), lab(318, 252, "Minoan: wood", tc + 1.8, "#d8b88a", 26, "start")]
    return els


def fragments(pts_list, at, c="#e8c35a", step=.25):
    return [poly(p, c, "#fff3dc", 1.5, at + step * k, fx="pop") for k, p in enumerate(pts_list)]


def dolphin(x, y, s, at, c="#4f7fa6", edge=LILAC, style="claimed", op=None, w=2, face=1):
    """A leaping dolphin as on the Queen's Hall fresco: an arched body, a short beak, a small swept-back fin, flukes, a yellow side stripe."""
    m = face
    def P(a, b):
        return (x + m * a * s, y + (b + .0042 * a * a) * s)       # the body arches: the ends lower than the middle
    body = [P(-110, 4), P(-80, -16), P(-30, -28), P(30, -30), P(80, -20), P(112, -8), P(132, -4), P(134, 3), P(112, 8), P(76, 18), P(20, 24), P(-40, 20), P(-90, 12)]
    fin = [P(-14, -27), P(-4, -52), P(18, -54), P(14, -26)]
    flip = [P(46, 16), P(30, 38), P(62, 22)]
    tail = [P(-108, 4), P(-140, -18), P(-128, 4), P(-142, 26)]
    return [poly(tail, c, edge, w, at, style=style, op=op, curve=True), poly(fin, c, edge, w, at, style=style, op=op, curve=True), poly(body, c, edge, w, at, curve=True, style=style, op=op),
            poly(flip, c, edge, w, at, style=style, op=op), ln([P(-70, 8), P(10, 12), P(96, 4)], at, "#f2c25e", 3 * s, style, draw=False, curve=True, op=op),
            ln([P(-60, 15), P(20, 20), P(100, 8)], at, "#efe9dc", 2.5 * s, style, draw=False, curve=True, op=op), circ(*P(104, -6), 3.2 * s, "#1a1511", at=at, op=op)]


def s24():
    """Repainted: the griffins of the Throne Room, mostly modern paint over a few pieces; the dolphins, rebuilt from a handful of fragments."""
    tg, td = T("s24", "griffins"), T("s24", "dolphin fresco")
    els = [rect(150, 190, 700, 460, "#8a3424", "rgba(255,236,206,.3)", 2, 8, -1), rect(930, 190, 700, 460, "#d8e4e6", "rgba(255,236,206,.3)", 2, 8, -1)]
    els += griffin(520, 520, 1.25, .3, "rgba(232,210,160,.25)", LILAC, "claimed", w=2.5) + sum([lily(x, 600, 90, .3, "rgba(241,228,196,.2)", LILAC, "claimed") for x in (230, 300, 760)], [])
    els += fragments([[(372, 362), (410, 350), (420, 392), (380, 400)], [(560, 470), (630, 460), (640, 508), (566, 512)], [(700, 420), (742, 418), (736, 452)]], tg + .3)
    els += [lab(500, 710, "griffins: repainted", tg + .4, BONE, 30)]
    for k, (x, y, s) in enumerate(((1130, 330, 1.05), (1420, 420, 1.15), (1180, 540, .95))):
        els += dolphin(x, y, s, .4 + .1 * k, face=1 if k != 1 else -1)
    for k in range(6):
        x, y = 1000 + 100 * k, 600 - 30 * (k % 2)
        els += [poly([(x, y), (x + 26, y - 8), (x + 40, y), (x + 26, y + 8)], "rgba(240,200,120,.25)", LILAC, 1.5, .6, style="claimed")]
    els += fragments([[(1180, 312), (1214, 306), (1220, 336), (1186, 340)], [(1400, 410), (1436, 402), (1440, 430)], [(1166, 548), (1196, 544), (1192, 568)]], td + .3, "#6fb0d0")
    els += [lab(1280, 710, "dolphins: a few fragments", td + .5, BONE, 30)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def piece(x, y, s, fill, edge, at, style="known", fx="pop", tabs=(1, 0, 0, 1)):
    """A jigsaw piece: a square with round tabs (right, bottom, left, top flags)."""
    out = [rect(x, y, s, s, fill, edge, 2.5, 10, at, fx=fx, style=style)]
    r = s * .14
    spots = [(x + s, y + s / 2), (x + s / 2, y + s), (x, y + s / 2), (x + s / 2, y)]
    for f, (cx, cy) in zip(tabs, spots):
        if f:
            out.append(circ(cx, cy, r, fill, edge, 2.5, at, fx=fx, style=style))
    return out


def s25():
    """A jigsaw: five real pieces; a brush paints in the rest (dashed)."""
    tp = T("s25", "painting in")
    s, x0, y0 = 170, 549, 175
    real = {(0, 0), (2, 0), (1, 1), (3, 1), (0, 2)}
    els = [gl(889, 430, 520, .1, .2, "lamp")]
    k = 0
    for j in range(3):
        for i in range(4):
            x, y = x0 + i * s, y0 + j * s
            tabs = (i < 3 and (i + j) % 2 == 0, j < 2 and (i + j) % 2 == 1, 0, 0)
            if (i, j) in real:
                els += piece(x + 6, y + 6, s - 12, "#c9a370", "#fff3dc", .3 + .15 * k, tabs=tabs)
                els += [ln([(x + 30, y + 60 + 12 * (i % 3)), (x + s - 40, y + 50 + 10 * (j % 2))], .5 + .15 * k, "#7a4e2e", 5, draw=False, curve=True)]
                k += 1
            else:
                els += piece(x + 6, y + 6, s - 12, "rgba(201,193,238,.12)", LILAC, tp + .1 * ((i + j * 4) % 7), "claimed", tabs=tabs)
    bx, by = x0 + 4 * s + 70, y0 + 2.2 * s
    els += [ln([(bx, by), (bx + 120, by - 160)], tp - .3, "#8a6a48", 9, draw=False), poly([(bx - 14, by - 6), (bx + 8, by + 12), (bx - 20, by + 50), (bx - 36, by + 30)], LILAC, at=tp - .3)]
    els += [lab(x0 - 30, y0 + 70, "found", .9, GOLD, 30, "end"), lab(x0 + 4 * s + 40, y0 + 2.75 * s, "painted in", tp + .6, LILAC, 30, "start", st="ital")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s26():
    """Critics and admirers on one balance: guesses set in stone, against a ruin anyone can read. Level."""
    tc, ta, tb = T("s26", "set his guesses"), T("s26", "His admirers"), T("s26", "Both have")

    def block(x, y):
        return [rect(x - 80, y - 110, 160, 110, CONC, CONC_D, 2, 4, tc, fx="pop"), lab(x, y - 40, "?", tc + .3, LILAC, 54, st="serif"),
                lab(x, y + 64, "guesses set in stone", tc + .4, BONE, 28)]

    def visit(x, y):
        out = column(x + 60, y - 170, y, ta + .2, fx="pop")
        out += [person(x - 70 + 34 * j, y, 60 - 8 * (j % 2), ta + .3 + .1 * j, "#d9c7a6") for j in range(3)]
        return out + [lab(x, y + 64, "readable for all", ta + .5, BONE, 28)]
    els = balance(889, 330, 860, 720, .3, block, visit, drop=230, pan=280) + [gl(889, 330, 170, tb, .55, "lamp")]
    els += [lab(459, 290, "his critics", tc - .4, DIM, 26), lab(1319, 290, "his admirers", ta - .2, DIM, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · Bulls and double axes
K27 = 1.3
OX27, OY27 = 889 - FCX * K27, 520 - FCY * K27


def s27():
    """The fresco again, closer: three young people and a bull at full gallop; 1 grips the horns, 2 vaults over, 3 waits behind."""
    t1, t2, t3 = T("s27", "grips the"), T("s27", "vaults over"), T("s27", "waits behind")
    els = fresco(OX27, OY27, K27, -1, edge=True) + [gl(889, 300, 600, -1, .12, "lamp")]
    pts = [fresco_pt(OX27, OY27, K27, FIG_GRIP["head"]), fresco_pt(OX27, OY27, K27, FIG_VAULT["knA"]), fresco_pt(OX27, OY27, K27, FIG_CATCH["head"])]
    spots = [(250, 330), (1110, 230), (1530, 330)]
    labs_ = [(250, 284, "grips the horns", "middle"), (1150, 240, "vaults over", "start"), (1530, 284, "waits behind", "middle")]
    for k, ((px, py), (sx, sy), (lx, ly, t, a), at) in enumerate(zip(pts, spots, labs_, (t1, t2, t3))):
        els += [ln([(sx, sy), (px, py)], at - .2, AU, 2.5, dur=.4), circ(sx, sy, 26, "rgba(18,13,10,.9)", AU, 3, at - .3, fx="pop"),
                lab(sx, sy + 11, str(k + 1), at - .25, AU, 30, st="serif"), lab(lx, ly, t, at, BONE, 30, a)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def rhyton(x, y, s, at):
    """The bull's-head vessel of the Little Palace (dark stone, white inlay round the nostrils, a crystal eye, gilded horns), in profile facing left."""
    P = lambda a, b: (x + a * s, y + b * s)
    head = [P(70, -96), P(20, -104), P(-40, -82), P(-92, -40), P(-128, 8), P(-150, 46), P(-148, 74), P(-126, 92), P(-80, 92), P(-30, 76), P(20, 70), P(70, 64),
            P(96, 30), P(100, -30), P(92, -76)]
    out = [gl(x, y, 300 * s, at, .3, "lamp"), poly(head, "#2c2724", "#9a8f84", 2, at, fx="pop", curve=True)]
    out += [poly([P(-150, 46), P(-148, 74), P(-126, 92), P(-104, 86), P(-112, 60), P(-130, 40)], "#efe6d2", at=at + .1, curve=True)]
    out += [poly(E(*P(-132, 64), 9 * s, 6 * s, 10), "#1a1511", at=at + .1)]
    out += [poly(E(*P(-30, -40), 17 * s, 12 * s, 16), "#f4f0e8", "#b0301e", 3 * s, at + .2, curve=True), circ(*P(-33, -40), 6 * s, "#1a1511", at=at + .2)]
    out += [circ(*P(20 + 16 * (j % 4), -86 + 14 * (j // 4)), 5 * s, "none", "#6a625a", 1.5, at + .2) for j in range(8)]
    out += [ln([P(30, -96), P(10, -150), P(-40, -186), P(-96, -186)], at + .3, "#8a6a1a", 15 * s, draw=False, curve=True),
            ln([P(30, -96), P(10, -150), P(-40, -186), P(-96, -186)], at + .3, AU, 9 * s, draw=False, curve=True),
            ln([P(64, -88), P(70, -140), P(52, -184), P(10, -206)], at + .3, "#8a6a1a", 13 * s, draw=False, curve=True),
            ln([P(64, -88), P(70, -140), P(52, -184), P(10, -206)], at + .3, "#c9a43a", 7 * s, draw=False, curve=True)]
    out += [poly([P(86, -60), P(132, -78), P(112, -40)], "#2c2724", "#9a8f84", 1.5, at, curve=True)]
    return out


def horns_unit(x, base, w, at, fx="rise", c=STONE):
    """A pair of 'horns of consecration': a block base with two upward horns."""
    h = w * .9
    return [poly([(x - w / 2, base), (x + w / 2, base), (x + w / 2, base - .25 * h), (x + .36 * w, base - .25 * h), (x + .46 * w, base - h), (x + .3 * w, base - h * .96),
                  (x + .16 * w, base - .3 * h), (x - .16 * w, base - .3 * h), (x - .3 * w, base - h * .96), (x - .46 * w, base - h), (x - .36 * w, base - .25 * h),
                  (x - w / 2, base - .25 * h)], c, "#fff3dc", 1.5, at, fx=fx, curve=False)]


def s28():
    """Bulls everywhere: a stone vessel carved as a bull's head; and stone horns along the rooftops, Evans's 'horns of consecration'."""
    tv, th = T("s28", "stone vessels"), T("s28", "stone horns")
    els = rhyton(470, 430, 1.55, tv - .3) + [lab(470, 720, "bull's-head vessel", tv + .5, BONE, 30)]
    g, top = 720, 520
    els += [rect(960, top, 700, g - top, "url(#k-blocks)", "rgba(255,236,206,.4)", 1.5, 2, .3, op=.8), rect(940, top - 22, 740, 26, STONE_D, "#fff3dc", 1.2, 2, .3),
            gl(1310, 430, 420, .3, .2, "lamp")]
    for k, x in enumerate((1020, 1170, 1320, 1470, 1620)):
        els += horns_unit(x, top - 22, 96, th - .2 + .2 * k)
    els += [lab(1310, 330, "horns of consecration", th + .8, BONE, 30), lab(1310, 366, "Evans's name", th + 1.1, DIM, 24)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


LEAP = [(dict(FIG_GRIP), "grip"), (dict(FIG_VAULT), "vault"),
        (dict(head=(330, 10), sh=(326, 34), hip=(330, 116), elA=(360, 16), haA=(390, 2), elB=(300, 20), haB=(276, 6),
              knA=(312, 166), ftA=(330, 212), knB=(352, 168), ftB=(372, 214), face=-1), "land")]


def s29():
    """The leap as three moments (grip, vault, land), a dashed arc through them and a '?'; then the three in one picture."""
    th, ts = T("s29", "exactly how"), T("s29", "several moments")
    fs = .42
    els = [gl(889, 300, 700, .1, .14, "lamp")]
    centres = []
    for k, (J, nm) in enumerate(LEAP):
        fx0 = 150 + k * 520
        at = .3 + .45 * k
        els += [rect(fx0, 150, 440, 230, "rgba(169,203,213,.18)", "rgba(255,236,206,.35)", 2, 10, at, fx="pop")]
        cx, cy = fx0 + 220, 290
        els += bull(cx, cy, fs, at + .1, detail=False, body="#efe2c4", edge="#2e2016")
        els += figure(J, SKIN_R if k == 1 else SKIN_W, at + .2, fs, cx, cy)
        els += [lab(fx0 + 26, 186, str(k + 1), at + .2, AU, 30, st="serif")]
        centres.append((cx + J["hip"][0] * fs, cy + J["hip"][1] * fs - 20))
    els += [ln(centres, th - .4, AU, 3, "inferred", 1.4, curve=True)] + qmark(889, 140 + 40, th + .4, 60, halo=False)
    # all three moments in one painting
    els += [rect(560, 430, 660, 340, "rgba(169,203,213,.25)", "rgba(255,236,206,.45)", 2, 10, ts - .3, fx="pop")]
    s = .66
    cx, cy = 890, 640
    els += bull(cx, cy, s, ts - .2, detail=True)
    for k, (J, nm) in enumerate(LEAP[:2]):
        els += figure(J, SKIN_R if k == 1 else SKIN_W, ts + .2 * k, s, cx, cy)
    els += figure(FIG_CATCH, SKIN_W, ts + .4, s, cx, cy)
    els += [lab(540, 610, "several moments in one?", ts + .6, LILAC, 30, "end", st="ital")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s30_add():
    """A tempting thought: a dotted arrow from the leap to the story's maze and its monster, with a '?'."""
    tt = T("s30", "tempting thought")
    mx, my, cs = 1370, 520, 26
    els = [arr([(1225, 640), (1300, 600), (1360, 590)], .3, LILAC, 3, "claimed", 1.0)]
    els += maze_els(mx, my, cs * 7 / 9, .6, LILAC, 2.5, "claimed", "fade", .6, walls=MZR[0])
    els += minotaur(mx + 4.5 * cs * 7 / 9, my + 5.2 * cs * 7 / 9, 50, .8, "#2a2032", edge=LILAC, ew=1.5)
    els += qmark(1300, 560, 1.0, 50, halo=False) + [lab(1460, 760, "a tempting thought", tt, LILAC, 28, st="ital")]
    return els


def labrys(cx, cy, s, at, c=BRONZE, edge="#ffe2b4", fx="pop", shaft=True, w=2):
    """A Minoan double axe: two slender blades with concave edges and flaring curved cutting edges, on a long shaft."""
    P = lambda a, b: (cx + a * s, cy + b * s)
    bl = [P(-12, -26), P(-50, -50), P(-96, -96), P(-120, -112), P(-112, -60), P(-108, 0), P(-112, 60), P(-120, 112), P(-96, 96), P(-50, 50), P(-12, 26)]
    br = [(2 * cx - x, y) for x, y in bl]
    out = []
    if shaft:
        out += [ln([P(0, -120), P(0, 320)], at, "#6b4a30", 12 * s, draw=False), circ(*P(0, -124), 9 * s, "#6b4a30", at=at)]
    out += [poly(bl, c, edge, w, at, fx=fx, curve=True), poly(br, c, edge, w, at, fx=fx, curve=True), rect(*P(-14, -34), 28 * s, 68 * s, c, edge, w, 4, at, fx=fx)]
    out += [ln([P(-112, -86), P(-106, 0), P(-112, 86)], at + .1, "#ffe9c2", 2.5, draw=False, curve=True, op=.7),
            ln([P(112, -86), P(106, 0), P(112, 86)], at + .1, "#ffe9c2", 2.5, draw=False, curve=True, op=.7)]
    return out


def labrys_sign(x, y, s, at, c="#3a2a1e", w=3):
    """The double axe as a mason's sign cut in a block: two triangles meeting on a stroke."""
    return [ln([(x - 30 * s, y - 24 * s), (x + 30 * s, y + 24 * s), (x + 30 * s, y - 24 * s), (x - 30 * s, y + 24 * s), (x - 30 * s, y - 24 * s)], at, c, w, dur=.5),
            ln([(x, y - 40 * s), (x, y + 40 * s)], at + .2, c, w, dur=.3)]


def s31():
    """The double axe: a great bronze labrys; small ones left as offerings in numbers; the shape again and again on the walls."""
    to, tw = T("s31", "offerings"), T("s31", "palace walls")
    els = [gl(560, 380, 380, .1, .35, "lamp")] + labrys(560, 300, 1.6, .3) + [lab(560, 770, "the labrys", .9, AMBER, 32)]
    els += [rect(900, 650, 760, 18, WOOD, "#8a6a48", 1.5, 3, to - .4)]
    for k in range(9):
        x = 950 + 82 * k
        els += labrys(x, 590, .32, to + .1 * k, BRONZE, "#ffe2b4", "pop", True, 1.2)
    els += [lab(1280, 718, "offerings", to + .9, BONE, 28)]
    for k, x in enumerate((960, 1220, 1480)):
        els += [rect(x, 200, 230, 150, "url(#k-blocks)", "rgba(255,236,206,.45)", 1.5, 2, tw - .3 + .2 * k, op=.85), rect(x, 200, 230, 150, STONE, at=tw - .3 + .2 * k, op=.55)]
        els += labrys_sign(x + 115, 275, 1.0, tw + .2 * k)
    els += [lab(1335, 400, "on the walls", tw + .8, BONE, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s32():
    """The word chain: labrys (Lydian for axe, says Plutarch) > 1892 > labyrinthos > Evans's 'house of the double axe'."""
    tl, t9, te = T("s32", "labrys", k=1), T("s32", "eighteen ninety-two"), T("s32", "Evans took")
    y = 470
    els = [gl(889, 420, 700, .1, .16, "lamp")] + labrys(330, 230, .55, .3, BRONZE, "#ffe2b4", "pop", False) + scroll(250, 300, 160, 60, .5)
    els += [lab(330, y + 80, "labrys", 1.0, BONE, 60, st="serif"), lab(330, y + 130, "Lydian, says Plutarch", tl - .2, DIM, 24)]
    els += [arr([(500, y + 50), (640, y + 30), (780, y + 50)], t9 - .3, LILAC, 3.5, "claimed", .9)] + chip(640, y - 30, "1892", GOLD, t9, 26)
    els += [lab(1000, y + 80, "labyrinthos", t9 + .9, BONE, 60, st="serif")]
    px, py = 1450, 380
    els += [poly([(px - 140, py + 80), (px + 140, py + 80), (px + 140, py - 30), (px, py - 110), (px - 140, py - 30)], "rgba(232,195,90,.08)", LILAC, 3, te - .2, style="claimed", fx="pop"),
            rect(px - 34, py + 10, 68, 70, "#120d0a", LILAC, 2, 4, te - .1, style="claimed")] + labrys(px, py - 40, .3, te + .2, AU, "#ffe2b4", "pop", False, 1.2)
    els += [lab(px, py + 150, "house of the double axe", te + .5, LILAC, 32, st="ital"), lab(px, py + 190, "Evans", te + .8, DIM, 24)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s33():
    """Three doubts: an older, pre-Greek word of uncertain meaning; double axes in other palaces too; the oldest spelling begins with D."""
    to, tp, td = T("s33", "older than Greek"), T("s33", "other Cretan"), T("s33", "oldest spelling")
    els = [rect(110 + 540 * k, 170, 480, 560, "rgba(245,236,220,.04)", "rgba(255,236,206,.25)", 1.5, 14, .3 + .1 * k) for k in range(3)]
    els += [lab(350, 360, "labyrinthos", .6, BONE, 52, st="serif")] + qmark(350, 520, to + .3, 100) + [lab(350, 660, "older than Greek", to + .5, BONE, 30)]
    v = View(23.4, 26.5, 34.8, 35.75, (680, 300, 420, 160))
    els += [island(v, CRETE, tp - .4, "#6b5b44", "rgba(255,236,206,.6)", 1.2)]
    for k, q in enumerate((KNOSSOS, PHAISTOS, MALIA, ZAKROS)):
        x, y = v.p(*q)
        els += labrys(x, y - 10, .17, tp + .2 * k, AU, "#ffe2b4", "pop", False, 1)
    els += [lab(890, 660, "other palaces too", tp + .9, BONE, 30)]
    els += [lab(1312, 380, "da", td, AU, 48, "end", st="serif"), lab(1312, 380, "-pu₂-ri-to-jo", td + .2, BONE, 48, "start", st="serif"),
            gl(1285, 362, 70, td + .2, .5, "lamp"), lab(1430, 660, "D, not L", td + .8, AU, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s34_add():
    """Still only an idea: a '?' on the dotted link between the words, and a note under it."""
    return qmark(640, 548, .5, 56, halo=True) + [lab(640, 620, "still only an idea", .9, LILAC, 30, st="ital")]


# ================================================================== CHAPTER 4 · Honey for the Labyrinth
def tablet_signed(x, y, w, h, at, rows=3, n=6, seed=1, c=CLAY, ink=INK, sh=None):
    """A clay tablet with rows of schematic signs."""
    sh = sh or min(46, (h - 30) / rows * .62)
    out = clay_tablet(x, y, w, h, at, c)
    for j in range(rows):
        row, _ = sign_row(x + 22, y + 16 + j * (h - 24) / rows, sh, n, at + .1 + .05 * j, ink, 2.6, seed=seed + 3 * j)
        out += row
    return out


def s35():
    """Shelves of clay tablets fill; two come forward: Linear A and Linear B."""
    tt, tb = T("s35", "thousands"), T("s35", "Linear B")
    els = [gl(560, 430, 560, .1, .28, "lamp")]
    for s_ in range(3):
        y = 330 + 160 * s_
        els += [rect(140, y, 820, 16, WOOD, "#8a6a48", 1.5, 2, .2 + .1 * s_)]
        for j in range(16):
            h = 62 + (j * 7 + s_ * 5) % 22
            els += clay_tablet(160 + 49 * j, y - h, 38, h, max(.3, tt - .8) + .015 * (j + 16 * s_), CLAY if (j + s_) % 3 else "#9a7854")
    els += [lab(550, 760, "thousands of tablets", tt + .6, BONE, 30)]
    els += tablet_signed(1060, 250, 260, 300, tb - 1.6, 4, 4, seed=5, c="#b89b72") + [lab(1190, 610, "Linear A", tb - 1.2, AMBER, 32)]
    els += tablet_signed(1380, 250, 260, 300, tb - .3, 4, 4, seed=9) + [lab(1510, 610, "Linear B", tb, GOLD, 32)]
    return {"base": "dark", "stars": 16, "cam": CAM, "els": els}


def s36():
    """Linear A, about 1800 to 1450 BCE, still unread: its signs can be sounded out, their meaning cannot; a Finnish menu read aloud."""
    tu, ts, tl, tf = T("s36", "still unread"), T("s36", "sound out"), T("s36", "language"), T("s36", "Finnish menu")
    els = [gl(480, 400, 460, .1, .26, "lamp")] + tablet_signed(200, 200, 560, 300, .3, 3, 7, seed=21, c="#b89b72")
    els += chip(480, 160, "about 1800 to 1450 BCE", GOLD, .6, 24)
    for k in range(7):
        x = 236 + k * 62
        els += [ln([(x, 540), (x + 8, 532), (x + 16, 540), (x + 24, 532)], ts + .08 * k, BLUE, 2.5, draw=False, curve=True)]
    els += qmark(480, 650, tl, 80) + [lab(480, 740, "still unread", tu, BONE, 30)]
    mx, my = 1010, 220
    els += [rect(mx, my, 340, 400, "#f1e7d3", "#8a7a66", 2, 10, tf - .4, fx="pop")]
    for k, t in enumerate(("Lohikeitto", "Karjalanpiirakka", "Korvapuusti")):
        els += [lab(mx + 170, my + 110 + 100 * k, t, tf - .2 + .15 * k, "#2a2219", 30, st="serif", halo=False)]
    px = 1500
    els += [person(px, 700, 190, tf - .2, "#d9c7a6")] + [ln([(px - 44 - 14 * k, 520 - 10 * k), (px - 56 - 18 * k, 540), (px - 44 - 14 * k, 560 + 10 * k)], tf + .4 + .15 * k, BLUE, 2.5, dur=.3, curve=True)
                                                       for k in range(3)]
    els += [poly(E(1380, 700, 60, 14, 20), "#e9dccb", "#8a7a66", 1.5, tf + .5)] + qmark(1380, 670, tf + 1.0, 56, halo=False)
    els += [lab(1180, 760, "sound, not sense", tf + 1.4, BLUE, 30)]
    return {"base": "dark", "stars": 16, "cam": CAM, "els": els}


def s37():
    """1936, London: Evans holds up a tablet before a hall of listeners; in the front row a schoolboy of fourteen lights up."""
    tv, tl = T("s37", "Michael Ventris"), T("s37", "London")
    g = 720
    els = [gl(1260, 360, 420, .1, .3, "lamp"), ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False),
           rect(1150, g - 170, 110, 170, WOOD, "#8a6a48", 1.5, 4, .2), rect(1130, g - 186, 150, 20, WOOD_D, "#8a6a48", 1.5, 3, .2)]
    els += [person(1340, g, 230, .3, "#cbbca8"), ln([(1318, g - 150), (1290, g - 200)], .4, "#cbbca8", 9, draw=False),
            rect(1258, g - 262, 50, 64, CLAY, "#e9dccb", 1.5, 6, .5, fx="pop"), gl(1283, g - 230, 80, .5, .5, "lamp"), lab(1340, 772, "Arthur Evans", .8, BONE, 28)]
    for r in range(3):
        for j in range(9):
            x = 170 + j * 92 + (r % 2) * 46
            y = g - 30 - r * 70
            if (r, j) == (0, 4):
                continue
            els += [circ(x, y - 40, 16, "#3a3430", at=.2 + .02 * (j + 9 * r)), rect(x - 26, y - 22, 52, 34, "#3a3430", r=10, at=.2 + .02 * (j + 9 * r))]
    bx, by = 170 + 4 * 92, g - 30
    els += [circ(bx, by - 34, 13, "#e8c35a", at=.3), rect(bx - 20, by - 19, 40, 28, "#e8c35a", r=9, at=.3), gl(bx, by - 30, 90, tv - .2, .7, "lamp"),
            lab(bx, by - 110, "Michael Ventris, 14", tv, AU, 30)]
    els += chip(560, 200, "London, 1936", GOLD, tl, 26)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s38():
    """Alice Kober's endings (three forms of one word, last signs glowing); Ventris's grid fills; 1952, the BBC: 'but Greek nevertheless'."""
    tk, tc, tb, tn = T("s38", "Alice Kober"), T("s38", "cracked"), T("s38", "BBC radio"), T("s38", "but Greek")
    els = [gl(380, 300, 380, .1, .25, "lamp")]
    for j in range(3):
        y = 190 + j * 70
        row, xe = sign_row(150, y, 46, 3, .3 + .1 * j, BONE, 3, seed=40)
        end, _ = sign_row(xe, y, 46, 1, tk + .2 + .3 * j, AU, 3, seed=50 + j)
        els += row + end + [rect(xe - 8, y - 8, 54, 62, "none", AU, 2, 6, tk + .2 + .3 * j, fx="pop")]
    els += [lab(330, 450, "Alice Kober: changing endings", tk + .9, BONE, 26)]
    gx, gy, cs = 700, 180, 52
    els += [rect(gx + cs * i, gy + cs * j, cs - 4, cs - 4, "none", "rgba(232,195,90,.35)", 1.2, 4, .6) for j in range(5) for i in range(6)]
    els += [rect(gx + cs * i, gy + cs * j, cs - 4, cs - 4, "rgba(232,195,90,.18)", "rgba(232,195,90,.7)", 1.5, 4, tc - 1.6 + .04 * (i + 6 * j), fx="pop")
            for j in range(5) for i in range(6)]
    els += [lab(gx + 3 * cs, gy + 5 * cs + 44, "Ventris's grid", tc - .8, BONE, 26)]
    rx, ry = 1250, 230
    els += [rect(rx, ry, 300, 200, "#5a3a22", "#c9a46a", 2, 20, tb - .3, fx="pop"), rect(rx + 24, ry + 30, 150, 140, "#2a1a10", "#c9a46a", 1.5, 70, tb - .2),
            circ(rx + 230, ry + 70, 22, "#c9a46a", at=tb - .2), circ(rx + 230, ry + 140, 22, "#c9a46a", at=tb - .2)]
    els += [ln([(rx + 330 + 22 * k, ry + 60 - 14 * k), (rx + 350 + 26 * k, ry + 100), (rx + 330 + 22 * k, ry + 140 + 14 * k)], tb + .2 * k, AMBER, 3, dur=.3, curve=True) for k in range(3)]
    els += [lab(rx + 150, ry + 300, "BBC, 1952", tb + .2, DIM, 24), lab(rx + 170, ry + 400, "but Greek nevertheless", tn - .1, GOLD, 40, st="ital")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s39_add():
    """Greek: the word stamps over the grid; two thoughts, 'not Greek', struck through."""
    tg, te = T("s39", "Greek", k=1), T("s39", "Evans had")
    els = [gl(856, 310, 260, tg - .2, .6, "lamp"), lab(856, 350, "Greek", tg - .1, AU, 96, st="serif", fx="pop")]
    for k, (x, y) in enumerate(((300, 640), (620, 690))):
        at = te + .5 * k
        els += [poly(E(x, y, 120, 42, 24), "rgba(245,236,220,.08)", BONE, 2, at, curve=True, fx="pop"), circ(x - 90, y + 56, 8, "none", BONE, 2, at),
                lab(x, y + 10, "not Greek", at + .1, BONE, 28), strike(x - 100, y + 20, x + 100, y - 14, at + 1.4, RED, 4)]
    return els


VGC = View(20.0, 27.8, 34.5, 38.6, (90, 120, 1600, 680))


def s40():
    """The Mycenaeans of the mainland: an arrow from Mycenae and Pylos down to Knossos, where the tablets glow; after about 1450 BCE."""
    v = VGC
    tg, tk = T("s40", "Greek speakers"), T("s40", "ruling")
    kx, ky = v.p(*KNOSSOS)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += [{"k": "pin", "x": v.p(*MYCENAE)[0], "y": v.p(*MYCENAE)[1], "t": "Mycenae", "c": BONE, "in": .4, "a": "end", "lx": -18},
            {"k": "pin", "x": v.p(*PYLOS)[0], "y": v.p(*PYLOS)[1], "t": "Pylos", "c": BONE, "in": .6, "a": "end", "lx": -18},
            {"k": "pin", "x": kx, "y": ky, "t": "Knossos", "c": GOLD, "in": .8, "ly": 36}]
    els += [arr([v.p(22.9, 37.4), v.p(23.6, 36.4), (kx - 24, ky - 30)], tg - .2, AU, 5, dur=1.4), lab(*v.p(23.9, 37.2), "Mycenaean Greeks", tg + .4, AU, 32, "start")]
    els += [rect(kx + 26 + 22 * j, ky - 70 - 8 * (j % 2), 18, 40, CLAY, "#fff3dc", 1, 3, tk - .4 + .1 * j, fx="pop") for j in range(4)] + [gl(kx + 60, ky - 50, 110, tk - .2, .6, "lamp")]
    els += chip(1330, 220, "after about 1450 BCE", GOLD, tk, 26) + [{"k": "scale", "x": 160, "y": 760, "w": round(v.km(100), 1), "t": "100 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


TB41 = (330, 170, 1120, 250)


def s41():
    """KN Gg 702: honey for all the gods; the same again for da-pu2-ri-to-jo po-ti-ni-ja, the Mistress of the Labyrinth (the usual reading)."""
    th, tg, tm, ts, tr = T("s41", "offerings of"), T("s41", "all the"), T("s41", "Mistress"), T("s41", "the same again"), T("s41", "usual reading")
    x, y, w, h = TB41
    els = [gl(890, 300, 700, .1, .25, "lamp")] + chip(x + 90, 138, "KN Gg 702", GOLD, .4, 24)
    els += tablet_KN(x, y, w, h, .2, glow2=tm - .3, rows=(6, 8), sh=58)
    els += [rect(x + 22, y + 14, w - 44, h / 2 - 22, "rgba(245,236,220,.12)", BONE, 2, 8, tg - .3, fx="pop")]
    els += honey_jar(1590, 250, .52, tg) + honey_jar(1590, 380, .52, ts)
    els += [lab(890, 470, "honey: all the gods", tg, BONE, 32), lab(890, 524, "da-pu₂-ri-to-jo po-ti-ni-ja", tm - .2, DIM, 30, st="serif"),
            lab(890, 590, "the Mistress of the Labyrinth", tm + .3, GOLD, 44, st="serif", fx="rise"), lab(1500, 470, "the usual reading", tr, LILAC, 28, st="ital")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s43_add():
    """Centuries before Homer: a short strip from the tablet (about 1400 BCE) to Homer (about 700 BCE); what did it name?"""
    tc, tw = T("s43", "centuries"), T("s43", "What it named")
    y = 742
    els = [ln([(360, y), (1120, y)], tc - .4, DIM, 2, draw=False), clay_tablet(334, y - 40, 36, 44, tc - .4)[1], scroll(1110, y - 38, 70, 40, tc)[0]]
    els += [lab(740, y - 14, "centuries before Homer", tc + .2, BONE, 28)]
    els += qmark(1430, 760, tw, 60, halo=False) + [lab(1470, 752, "named what?", tw + .2, LILAC, 28, "start", st="ital")]
    return els


def s42():
    """The inversion: in the myth, Athens sends tribute to a crowned Crete; in the tablets, Greek speakers rule at Knossos."""
    tm, tt = T("s42", "In the myth"), T("s42", "In the tablets")
    els = [gl(889, 300, 600, .1, .14, "lamp"), ln([(140, 470), (1640, 470)], .1, "rgba(255,236,206,.2)", 2, draw=False)]
    # the myth (lilac)
    els += [lab(140, 196, "the myth", tm, LILAC, 30, "start", st="ital"), poly([(260, 420), (320, 330), (420, 316), (500, 360), (520, 420)], "#2b2328", LILAC, 2, tm, curve=True),
            lab(390, 452, "Athens", tm + .1, BONE, 26), poly([(1180, 420), (1260, 380), (1420, 372), (1560, 398), (1600, 420)], "#2b2328", LILAC, 2, tm, curve=True),
            lab(1390, 452, "Crete", tm + .1, BONE, 26)] + [crown(1390, 350, 28, tm + .4, LILAC)]
    els += galley(820, 400, 200, tm + .3, "#d9c7e8", face=1, sail="#120d0a") + [arr([(560, 410), (700, 418)], tm + .4, LILAC, 3, "claimed", .6, curve=False)]
    # the tablets (gold)
    els += [lab(140, 540, "the tablets", tt, GOLD, 30, "start"), poly([(260, 730), (320, 640), (420, 626), (500, 670), (520, 730)], "#3a3026", AU, 2, tt, curve=True),
            lab(390, 762, "Greeks", tt + .1, BONE, 26), poly([(1180, 730), (1260, 690), (1420, 682), (1560, 708), (1600, 730)], "#3a3026", AU, 2, tt, curve=True),
            lab(1390, 762, "Knossos", tt + .1, BONE, 26), arr([(560, 690), (1150, 682)], tt + .3, AU, 4, dur=.9, curve=False)]
    els += [person(1390, 682, 90, tt + .6, "#e8d6b8")] + [crown(1390, 586, 18, tt + .9, AU)] + [rect(1450 + 18 * j, 650 - 6 * (j % 2), 14, 30, CLAY, "#fff3dc", 1, 3, tt + .8 + .1 * j, fx="pop")
                                                                                             for j in range(3)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · The volcano next door
VSA = View(21.6, 29.2, 34.6, 37.7, (90, 120, 1600, 680))


def s44():
    """Crete looks out to sea: from Knossos, gold arcs to Kythera, Thera and Rhodes, where Minoan-style towns and goods turn up."""
    v = VSA
    tm = T("s44", "Minoan-style")
    kx, ky = v.p(*KNOSSOS)
    els = [{"k": "map", "land": v.land(), "in": -1},
           {"k": "pin", "x": kx, "y": ky, "t": "Knossos", "c": GOLD, "in": .5, "ly": 40, "lx": 0, "a": "middle"}]
    for k, (q, nm, a, lx) in enumerate(((KYTHERA, "Kythera", "end", -18), (THERA_P, "Thera", "start", 18), (RHODES, "Rhodes", "start", 18))):
        x, y = v.p(*q)
        els += [ln([(kx, ky - 8), ((kx + x) / 2, min(ky, y) - 60), (x, y)], tm - .2 + .35 * k, AU, 3, "inferred", .9, curve=True),
                circ(x, y, 9, AU, "#fff3dc", 2, tm + .5 + .35 * k, fx="pop"), lab(x + lx, y + 9, nm, tm + .6 + .35 * k, BONE, 28, a)]
    els += [lab(*v.p(27.4, 37.3), "Minoan reach", tm + 1.6, AU, 32, st="ital"), {"k": "scale", "x": 160, "y": 760, "w": round(v.km(100), 1), "t": "100 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def keftiu(x, y, h, at, gift, c=SKIN_R):
    """A gift bearer as Egyptian painters drew Aegean visitors: striding, long hair, a patterned kilt; carrying a gift."""
    out = [ln([(x, y - .48 * h), (x - .14 * h, y)], at, c, .06 * h, draw=False), ln([(x, y - .48 * h), (x + .14 * h, y)], at, c, .06 * h, draw=False),
           poly([(x - .1 * h, y - .52 * h), (x + .1 * h, y - .52 * h), (x + .13 * h, y - .36 * h), (x - .13 * h, y - .36 * h)], "#e8dcc2", "#6a3a22", 1.2, at),
           ln([(x - .1 * h, y - .46 * h), (x + .1 * h, y - .46 * h)], at, "#2a5a8a", 3, draw=False),
           poly([(x - .08 * h, y - .52 * h), (x + .08 * h, y - .52 * h), (x + .1 * h, y - .82 * h), (x - .1 * h, y - .82 * h)], c, at=at),
           circ(x + .01 * h, y - .9 * h, .07 * h, c, at=at), ln([(x - .02 * h, y - .96 * h), (x - .08 * h, y - .82 * h), (x - .06 * h, y - .66 * h)], at, HAIR, .03 * h, draw=False, curve=True)]
    if gift == "jar":
        out += [ln([(x + .06 * h, y - .78 * h), (x + .16 * h, y - .74 * h)], at, c, .04 * h, draw=False)] + honey_jar(x + .24 * h, y - .74 * h, .3 * h / 100, at, False, None)
    elif gift == "bull":
        out += [ln([(x + .06 * h, y - .74 * h), (x + .2 * h, y - .7 * h)], at, c, .04 * h, draw=False)]
        out += [poly(E(x + .28 * h, y - .72 * h, .09 * h, .07 * h, 14), "#2a2622", "#8a7f74", 1, at, curve=True),
                ln([(x + .24 * h, y - .78 * h), (x + .2 * h, y - .86 * h)], at, AU, .025 * h, draw=False), ln([(x + .32 * h, y - .78 * h), (x + .36 * h, y - .86 * h)], at, AU, .025 * h, draw=False)]
    elif gift == "cup":
        out += [ln([(x + .06 * h, y - .74 * h), (x + .18 * h, y - .78 * h)], at, c, .04 * h, draw=False),
                poly([(x + .14 * h, y - .86 * h), (x + .3 * h, y - .86 * h), (x + .27 * h, y - .74 * h), (x + .17 * h, y - .74 * h)], AU, "#7a5a1a", 1, at)]
    else:                                                # a tall jug carried on the shoulder
        out += [ln([(x + .06 * h, y - .76 * h), (x + .14 * h, y - .9 * h)], at, c, .04 * h, draw=False),
                poly([(x + .1 * h, y - 1.16 * h), (x + .16 * h, y - 1.16 * h), (x + .2 * h, y - 1.06 * h), (x + .22 * h, y - .94 * h), (x + .16 * h, y - .86 * h),
                      (x + .06 * h, y - .86 * h), (x + .02 * h, y - .96 * h), (x + .06 * h, y - 1.08 * h)], "#c9a46a", "#5a3a1a", 1.2, at, curve=True),
                ln([(x + .16 * h, y - 1.16 * h), (x + .22 * h, y - 1.2 * h)], at, "#5a3a1a", 3, draw=False)]
    return out


def s45():
    """An Egyptian tomb painting (15th century BCE): Cretan-looking visitors, the Keftiu, bring gifts: a jar, a bull's-head vessel, a cup, a jug."""
    tk = T("s45", "Keftiu")
    els = [rect(120, 150, 1250, 600, "#e6d8bc", "rgba(90,60,30,.6)", 2, 6, -1), rect(120, 150, 1250, 600, "url(#k-speck)", at=-1, op=.6),
           ln([(140, 196), (1350, 196)], -1, "#8a4a2a", 4, draw=False), ln([(140, 700), (1350, 700)], -1, "#8a4a2a", 4, draw=False),
           {"k": "glyphs", "x": 170, "y": 230, "w": 120, "h": 440, "rows": 9, "cols": 2, "kind": "hieroglyph", "c": "#3a5a7a", "in": .3}]
    for k, (x, gift) in enumerate(((430, "jar"), (660, "bull"), (890, "cup"), (1120, "jug"))):
        els += keftiu(x, 690, 400, .4 + .3 * k, gift)
    els += [lab(1530, 420, "the Keftiu", tk, AMBER, 36, st="ital")] + chip(1530, 490, "Egypt, 1400s BCE", GOLD, tk + .4, 24)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s46_add():
    """Closer on Crete and Thera: a dashed line from Knossos, about 110 km; Thera's pin pulses red."""
    v = VSA
    td = T("s46", "a hundred kilometres")
    kx, ky = v.p(*KNOSSOS)
    tx, ty = v.p(*THERA_P)
    return [ln([(kx, ky - 12), (tx, ty + 10)], td - .4, BONE, 3, "inferred", 1.0), lab((kx + tx) / 2 + 16, (ky + ty) / 2 + 6, "about 110 km", td + .3, BONE, 28, "start"),
            gl(tx, ty, 110, td, .9, "red", pulse=True), circ(tx, ty, 16, "none", RED, 3, td, fx="draw")]


def s47():
    """Thera erupts: a billowing column of ash rises and spreads into a wide cloud, ash falls; the town of Akrotiri disappears under grey ash."""
    te, ta = T("s47", "exploded"), T("s47", "vanished")
    g = 660
    els = [{"k": "water", "y": g, "h": 400, "op": .9, "in": -1},
           poly([(240, g), (420, 600), (640, 540), (800, 470), (880, 452), (980, 470), (1160, 560), (1400, 600), (1560, g)], "#3d3128", "rgba(255,226,190,.4)", 1.5, -1, curve=True)]
    for k, (x, w, h) in enumerate(((1180, 46, 30), (1236, 38, 24), (1286, 52, 34), (1346, 40, 26), (1396, 48, 30), (1222, 34, 20), (1320, 30, 18))):
        y = g - 50 - (k % 2) * 16 if k < 5 else g - 84
        els += [rect(x, y - h, w, h, "#d8c4a0", "#6a5644", 1.2, 1, .2), rect(x + w * .3, y - h * .6, w * .25, h * .35, "#3a2c22", at=.2)]
    els += [lab(1290, 740, "Akrotiri", .6, BONE, 28)]
    cx = 880
    els += [gl(cx, 452, 220, te - .3, .95, "fire", pulse=True)]
    rnd = random.Random(8)
    col = [(cx - 40, 452), (cx - 64, 400), (cx - 96, 330), (cx - 140, 260), (cx - 190, 210), (cx + 190, 210), (cx + 140, 260), (cx + 100, 330), (cx + 66, 400), (cx + 40, 452)]
    els.append(poly(col, "#6f6963", "none", 0, te - .3, fx="fill", dur=1.0, curve=True))      # the column, one smooth body
    for k in range(10):                                 # billows along its edges
        t_ = k / 9
        yy = 440 - 230 * t_
        half = 44 + 150 * t_ * t_
        for side in (-1, 1):
            r_ = 26 + 40 * t_
            els.append(poly(E(cx + side * half * .85 + rnd.uniform(-8, 8), yy, r_, r_ * .8, 18), ("#6c6660", "#7a746c", "#77716b")[k % 3], "none", 0,
                            te - .2 + .08 * k, fx="pop", curve=True))
    for k, (dx, dy, rx, ry) in enumerate(((0, 0, 230, 70), (-230, 26, 200, 62), (230, 22, 210, 64), (-430, 52, 170, 50), (440, 46, 180, 52), (-120, -40, 170, 56), (140, -44, 160, 54))):
        els.append(poly(E(cx + dx, 170 + dy, rx, ry, 26), "#77716a" if k % 2 else "#827c74", "rgba(255,236,206,.2)", 1, te + .9 + .15 * k, fx="pop", curve=True))
    els += [ln([(cx - 380 + 90 * k, 230), (cx - 340 + 90 * k + 30, 440)], te + 1.8 + .05 * k, "rgba(160,150,140,.55)", 3, "inferred", .8) for k in range(10)]
    els += [gl(cx, 330, 260, te + .2, .45, "red")]
    els += [poly([(1130, 560), (1200, 528), (1300, 536), (1400, 552), (1470, 596), (1520, g + 2), (1130, g + 2)], "#8a847c", "rgba(255,236,206,.25)", 1, ta - .2, fx="fill", dur=1.4,
                  op=.9, curve=True)]
    els += [lab(560, 470, "Thera", .5, BONE, 34, st="serif"), lab(1520, 520, "ash", ta + .8, "#cfcac2", 30, "start")]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def s48():
    """To scale (5.5 units a metre): a row of London houses and the Elizabeth Tower (96 m); a 20 m layer of grey rock fills over them."""
    tr, td = T("s48", "thirty to forty"), T("s48", "twenty metres")
    g, k = 720, 5.5
    els = [ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False), gl(1300, 360, 500, .1, .18, "lamp")]
    for j in range(10):
        x = 170 + j * 56
        els += [rect(x, g - 9 * k, 54, 9 * k, "#8a6a52", "#c9a98a", 1.2, 0, .2 + .03 * j), poly([(x - 2, g - 9 * k), (x + 27, g - 12 * k), (x + 56, g - 9 * k)], "#4a3a32", at=.2 + .03 * j),
                rect(x + 8, g - 7 * k, 12, 14, "#ffdca0", at=.3, op=.6), rect(x + 32, g - 7 * k, 12, 14, "#ffdca0", at=.3, op=.6)]
    tx, tw = 1300, 64
    th = 96 * k
    els += [rect(tx - tw / 2, g - th * .74, tw, th * .74, "#c8b48a", "#6a5644", 1.5, 0, .2), rect(tx - tw / 2 - 6, g - th * .82, tw + 12, th * .08, "#d6c49c", "#6a5644", 1.5, 0, .2),
            circ(tx, g - th * .78, 22, "#f4ecd8", "#6a5644", 2, .2), poly([(tx - tw / 2, g - th * .82), (tx + tw / 2, g - th * .82), (tx, g - th)], "#5a6a6a", "#3a4444", 1.5, .2)]
    els += [lab(tx + 60, g - th + 30, "Big Ben, 96 m", .6, BONE, 28, "start")]
    els += [rect(130, g - 20 * k, 1450, 20 * k, "#8a847c", "none", 0, 0, td - .6, fx="fill", dur=1.2, op=.72),
            ln([(130, g - 20 * k), (1580, g - 20 * k)], td + .5, "#d8d2ca", 2.5, draw=False)]
    els += [{"k": "dim", "x1": 1610, "y1": g, "x2": 1610, "y2": g - 20 * k, "t": "", "c": AMBER, "fx": "draw", "dur": .6, "in": td},
            lab(1600, g - 20 * k - 24, "about 20 m", td + .2, AMBER, 30, "end"), lab(450, g - 20 * k - 24, "all of Greater London", td + .5, BONE, 30)]
    els += chip(420, 230, "30 to 40 km³ of rock", "#cfcac2", tr, 26)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def XD(yr):
    """The dating axis: 1700 to 1300 BCE across x 160..1620."""
    return round(160 + (yr + 1700) / 400 * 1460, 1)


def tree_wedge(x, y, r, at):
    out = [poly([(x, y)] + [(x + r * math.cos(a), y - r * math.sin(a)) for a in [math.radians(40 + 2.5 * j) for j in range(41)]], "#8a6a48", "#d8b88a", 1.5, at, fx="pop")]
    for j in range(1, 9):
        rr = r * j / 9 + (4 if j in (5, 6) else 0)
        out.append(ln([(x + rr * math.cos(a), y - rr * math.sin(a)) for a in [math.radians(40 + 5 * q) for q in range(21)]], at + .1, "#5a3a22", 1.5, draw=False, curve=True))
    return out


def s49():
    """When? Radiocarbon (blue) in the late 1600s BCE; archaeology (amber) about a century later; in 2018 tree rings move the radiocarbon dates towards the 1500s."""
    tr, ta, tt = T("s49", "Radiocarbon"), T("s49", "pottery"), T("s49", "tree rings")
    y = 560
    ticks = [[XD(v), t] for v, t in ((-1700, "1700 BCE"), (-1600, "1600"), (-1500, "1500"), (-1400, "1400"), (-1300, "1300"))]
    els = [axis(160, 1620, y, ticks, .2)]
    els += [{"k": "band", "x0": XD(-1660), "x1": XD(-1600), "y": 470, "h": 22, "c": BLUE, "t": "radiocarbon", "tc": BLUE, "in": tr - .2}]
    els += [{"k": "band", "x0": XD(-1560), "x1": XD(-1460), "y": 390, "h": 22, "c": AMBER, "t": "archaeology", "tc": AMBER, "in": ta - .2}]
    els += tree_wedge(1300, 300, 110, tt - .3) + chip(1300, 160 + 186, "2018", GOLD, tt, 24)
    els += [{"k": "band", "x0": XD(-1600), "x1": XD(-1540), "y": 470, "h": 22, "c": BLUE, "op": .4, "in": tt + .8},
            arr([(XD(-1630), 512), (XD(-1560), 520)], tt + .6, BLUE, 3, dur=.6, curve=False)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


VCR = View(23.4, 26.5, 34.75, 35.75, (90, 150, 1600, 600))


def s50():
    """About 1450 BCE: fires at palace after palace across Crete; Knossos flickers but keeps its light, now with Greek-speaking masters."""
    v = VCR
    tf, tk = T("s50", "fires swept"), T("s50", "Greek-speaking")
    els = [poly([v.p(*q) for q in CRETE], "#5b4a37", "rgba(255,226,190,.55)", 2, -1, curve=True)]
    kx, ky = v.p(*KNOSSOS)
    for k, q in enumerate((KNOSSOS, PHAISTOS, MALIA, ZAKROS)):
        x, y = v.p(*q)
        els += [circ(x, y, 11, AU, "#fff3dc", 2, .3 + .1 * k, fx="pop"), gl(x, y, 70, .3 + .1 * k, .5, "lamp")]
    for k, q in enumerate((PHAISTOS, MALIA, ZAKROS, HTRIADA)):
        x, y = v.p(*q)
        els += flame(x + (14 if q == HTRIADA else 0), y - 14, 46, tf + .3 * k)
    els += flame(kx - 10, ky - 14, 26, tf + 1.2) + [gl(kx, ky, 150, tf + 1.6, .8, "lamp")]
    els += [lab(kx, ky + 50, "Knossos", .6, GOLD, 30), lab(*v.p(24.9, 35.6), "fires across Crete", tf + 1.0, FIRE, 30)] + chip(300, 230, "about 1450 BCE", GOLD, tf - .3, 26)
    hx, hy = kx + 170, ky - 120
    els += [poly([(hx - 34, hy + 36), (hx - 36, hy), (hx - 22, hy - 32), (hx, hy - 44), (hx + 22, hy - 32), (hx + 36, hy), (hx + 34, hy + 36)], "#6b4a2e", "#c9a46a", 1.5, tk - .2,
                  fx="pop", curve=True), circ(hx, hy - 50, 7, "#c9a46a", at=tk - .2, fx="pop"),
            poly([(hx + 30, hy + 30), (hx + 46, hy + 40), (hx + 40, hy + 64), (hx + 26, hy + 50)], "#6b4a2e", "#c9a46a", 1.2, tk - .2, fx="pop")]
    for j in range(4):
        yy = hy + 26 - 18 * j
        half = 32 - 5 * j
        for q in range(-3, 4):
            x0 = hx + q * half / 3.4
            d = 1 if j % 2 == 0 else -1
            els.append(ln([(x0 - 5 * d, yy + 5), (x0, yy - 4), (x0 + 5 * d, yy + 5)], tk, "#efe6d2", 3, draw=False, curve=True))
    els += [lab(hx + 50, hy + 8, "Greek-speaking masters", tk + .3, BONE, 28, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def s51_add():
    """The palace runs on past the eruption windows; fires about 1450 and about 1350 BCE; the last date dashed and debated."""
    tl, td = T("s51", "last great fire"), T("s51", "debated")
    els = [ln([(160, 650), (XD(-1350), 650)], .3, AU, 12, dur=1.4), lab(180, 690, "the palace", .6, AU, 28, "start")]
    els += flame(XD(-1450), 640, 40, .9) + flame(XD(-1350), 640, 48, tl)
    els += [rect(XD(-1400), 610, XD(-1300) - XD(-1400), 80, "none", LILAC, 2.5, 10, td - .3, style="claimed", fx="pop")] + qmark(XD(-1350) + 110, 700, td, 56, halo=False)
    els += [lab(XD(-1300) + 20, 760, "debated", td + .3, LILAC, 28, "end", st="ital")]
    return els


def labyrinth_square(cx, cy, s, at, c="#4d5056", w=7):
    """A square labyrinth as on the coins of Knossos: nested square walls with gaps, a centre square."""
    segs = []
    for r, gap in ((5, "b"), (4, "t"), (3, "b"), (2, "t"), (1, "b")):
        a = r * s
        if gap == "b":
            pts = [(cx - .3 * s, cy + a), (cx - a, cy + a), (cx - a, cy - a), (cx + a, cy - a), (cx + a, cy + a), (cx + .3 * s, cy + a)]
        else:
            pts = [(cx + .3 * s, cy - a), (cx + a, cy - a), (cx + a, cy + a), (cx - a, cy + a), (cx - a, cy - a), (cx - .3 * s, cy - a)]
        segs.append(ln(pts, 0, c, w, draw=False))
    segs.append(rect(cx - .45 * s, cy - .45 * s, .9 * s, .9 * s, c, at=0))
    return [grp(segs, at, "draw", dur=1.2)]


def coin(cx, cy, r, at):
    return [gl(cx, cy, r * 1.8, at, .25, "lamp"), circ(cx, cy, r, SILVER, "#7c8088", 4, at, fx="pop"), circ(cx, cy, r * .9, "none", "#9a9ea6", 2, at + .1),
            poly(E(cx - r * .35, cy - r * .4, r * .4, r * .22, 14), "#ffffff", at=at + .1, op=.25)] + \
           [circ(cx + r * .82 * math.cos(2 * math.pi * j / 36), cy + r * .82 * math.sin(2 * math.pi * j / 36), r * .025, "#8d9198", at=at + .1) for j in range(36)]


def s52():
    """Coins of Knossos, from the 400s BCE: a labyrinth on one, the Minotaur inside a half ring of dots on another."""
    tc, tl, tm = T("s52", "Greek city"), T("s52", "labyrinth"), T("s52", "Minotaur")
    els = coin(600, 430, 230, tc - .3) + coin(1180, 430, 230, tm - .5)
    els += labyrinth_square(600, 430, 34, tl)
    els += minotaur(1180, 560, 230, tm, "#7a7e86", edge="#e8eaee", ew=1.2)
    els += [circ(1180 + 160 * math.cos(math.radians(a)), 470 + 160 * math.sin(math.radians(a)), 9, "#7a7e86", "#e8eaee", 1, tm + .3 + .02 * j, fx="pop")
            for j, a in enumerate(range(200, 341, 20))]
    els += [lab(889, 735, "coins of Knossos", tc + .2, BONE, 30)] + chip(889, 160, "from the 400s BCE", GOLD, tl - .3, 26)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 6 · The weighing
LROWS = [200, 310, 420, 530, 640]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 48, 1500, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1190, y, grade, gc, gt, 28, "start")
    return out


def pic_palace(x, y, at):
    return plan_els(x, y, .5, at, BONE, 1.2, fx="pop", dur=.4)


def pic_bull(x, y, at):
    return [poly(E(x, y + 6, 26, 22, 18), "#efe2c4", "#2e2016", 1.5, at, fx="pop", curve=True),
            ln([(x - 20, y - 8), (x - 40, y - 26), (x - 34, y - 42)], at, "#f4ecdc", 5, draw=False, curve=True), ln([(x + 20, y - 8), (x + 40, y - 26), (x + 34, y - 42)], at, "#f4ecdc", 5, draw=False, curve=True)]


def pic_tablet(x, y, at):
    out = [rect(x - 48, y - 30, 96, 60, CLAY, "#e9dccb", 1.2, 8, at, fx="pop")]
    row, _ = sign_row(x - 38, y - 18, 22, 3, at + .05, INK, 2, seed=70)
    return out + row


def pic_maze(x, y, at):
    return maze_els(x - 36, y - 36, 8, at, LILAC, 1.6, "claimed", "fade", .4, walls=MZR[0])


def pic_mino(x, y, at):
    return minotaur(x, y + 40, 76, at, "#2a2032", edge=LILAC, ew=1.2)


def s53():
    """The ledger: the palace (Established), the bulls (Established), the word labyrinth in its records (Strong evidence)."""
    t1, g1 = T("s53", "Established"), T("s53", "puts Minos")
    t2, g2 = T("s53", "Established", k=2), T("s53", "and ritual")
    t3, g3 = T("s53", "Strong evidence"), T("s53", "usual reading")
    els = [rect(110, 136, 1560, 560, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, t1 - .2, pic_palace, "a great palace", "Established", t1, GRADE["established"])
    els += lrow(1, t2 - .2, pic_bull, "a bull cult", "Established", t2, GRADE["established"])
    els += lrow(2, t3 - .2, pic_tablet, "the word labyrinth", "Strong evidence", t3, GRADE["strong"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s54():
    """The verdict: a chain from the palace (about 1450 BCE) to the Greek storytellers, its middle links missing; Plausible."""
    tq, tp, tc = T("s54", "remember a real"), T("s54", "Plausible"), T("s54", "chain of memory")
    y = 500
    els = [gl(889, 300, 600, .1, .2, "lamp")] + plan_els(260, y, 1.0, .3, BONE, 1.2, fx="pop") + [lab(260, y + 110, "the palace", .6, BONE, 28)]
    els += scroll(1460, y - 40, 150, 80, .5) + [lab(1535, y + 110, "Greek storytellers", .8, BONE, 28)]
    for j in range(9):
        x = 420 + 112 * j
        known = j < 2 or j > 6
        els += [poly(E(x, y, 46, 22, 20), "none", AU if known else LILAC, 6 if known else 3, tc - .4 + .12 * j, style="known" if known else "claimed", curve=True)]
    els += [lab(889, y + 80, "can't be traced", tc + 1.2, LILAC, 30, st="ital")]
    els += [gl(889, 250, 220, tp, .5, "lamp")] + chip(889, 250, "Plausible", GRADE["plausible"], tp, 40)
    els += [lab(889, 160, "palace, bull cult, sea power", tq, DIM, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s55_add():
    """Row 4: the palace itself as the Labyrinth, Open question (a cave beside it); row 5: a living Minotaur, Ruled out (struck)."""
    tw, to, tcv, tm, tr = T("s55", "Was the palace"), T("s55", "Open question"), T("s55", "caves"), T("s55", "And a Minotaur"), T("s55", "Ruled out")
    els = lrow(3, tw - .2, pic_maze, "the palace as Labyrinth", "Open question", to, GRADE["open"])
    els += [poly([(1520, 560), (1540, 520), (1580, 506), (1620, 520), (1636, 560)], "#120d0a", DIM, 2, tcv, curve=True, fx="pop"), lab(1580, 490, "caves?", tcv + .2, DIM, 24)]
    els += lrow(4, tm - .2, pic_mino, "a living Minotaur", "Ruled out", tr, GRADE["ruled"]) + [strike(178, 670, 252, 610, tr + .2, RED, 5)]
    return els


def s56():
    """What would settle it: Linear A read at last (their own name), a tablet with a place (where?), a firm date (how far?)."""
    tl, tt, td = T("s56", "Linear A"), T("s56", "A tablet that"), T("s56", "firm date")
    els = [gl(889, 420, 640, .1, .2, "lamp")]
    els += [rect(200, 240, 300, 220, "rgba(201,193,238,.08)", LILAC, 2.5, 18, tl, fx="pop", style="claimed")]
    row, _ = sign_row(230, 270, 40, 5, tl + .2, "rgba(201,193,238,.75)", 2.5, seed=31)
    els += row + [poly(E(470, 200, 110, 50, 24), "rgba(245,236,220,.08)", LILAC, 2, tl + .5, curve=True, style="claimed", fx="pop"), lab(470, 210, "their own name", tl + .6, LILAC, 26),
                  lab(350, 560, "Linear A, read", tl + .8, LILAC, 30)]
    els += [rect(740, 240, 300, 220, "rgba(201,193,238,.08)", LILAC, 2.5, 18, tt, fx="pop", style="claimed")]
    row, _ = sign_row(770, 270, 40, 5, tt + .2, "rgba(201,193,238,.75)", 2.5, seed=37)
    els += row + [{"k": "pin", "x": 1000, "y": 420, "t": "", "c": AU, "in": tt + .5}, lab(890, 560, "where?", tt + .8, LILAC, 30)]
    els += [ln([(1240, 420), (1600, 420)], td, DIM, 2, draw=False)] + flame(1270, 412, 50, td + .2) + scroll(1500, 360, 90, 50, td + .4)
    els += [{"k": "dim", "x1": 1270, "y1": 470, "x2": 1545, "y2": 470, "t": "", "c": AMBER, "fx": "draw", "dur": .7, "in": td + .7}, lab(1420, 560, "how far?", td + 1.0, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s57_add():
    """The close: the fresco again, the lamp lower and warmer, the story's maze glimmering faintly over the wall."""
    return [gl(950, 470, 520, .4, .28, "fire"), gl(260, 300, 260, 1.0, .2, "lamp")] + maze_els(150, 170, 24, 1.2, LILAC, 2.2, "claimed", "fade", 1.6, op=.45, walls=MZR[0])


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "Centuries later", "s2"), (1, "And a clay tablet", "s3"), (1, "So was the", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "As punishment", "s7"), (1, "The craftsman", "s8")], {"chapter": "A monster in a maze"}),
    (1, 1, "collision", "s9", [(1, "Until the Athenian", "s10")], {}),
    (1, 2, "reversal", "s11", [(1, "Vase painters", "s12"), (2, "And even the ancients", "s13"), (3, "And the careful", "s14")], {}),
    (1, 3, "tag", "s15", [], {}),
    (2, 0, "world", "s16", [(1, "Then, in March", "s17")], {"chapter": "Digging for Minos"}),
    (2, 1, "collision", "s18", [(1, "Within months", "s19"), (1, "The whole complex", "s20"), (2, "Get lost", "s21")], {}),
    (2, 2, "cost", "s22", [(1, "So what is Minoan", "s23"), (1, "The griffins", "s24"), (2, "It's like", "s25")], {}),
    (2, 3, "tag", "s26", [], {}),
    (3, 0, "world", "s27", [(1, "There are stone", "s28")], {"chapter": "Bulls and double axes"}),
    (3, 1, "collision", "s29", [(1, "Did a tale", "s30")], {}),
    (3, 2, "reversal", "s31", [(1, "Plutarch, again", "s32"), (2, "Many linguists", "s33")], {}),
    (3, 3, "tag", "s34", [], {}),
    (4, 0, "world", "s35", [(1, "Linear A, used", "s36")], {"chapter": "Honey for the Labyrinth"}),
    (4, 1, "collision", "s37", [(1, "Building on", "s38")], {}),
    (4, 2, "reversal", "s39", [(0, "So when these", "s40"), (1, "And among those", "s41"), (2, "In the myth", "s42")], {}),
    (4, 3, "tag", "s43", [], {}),
    (5, 0, "world", "s44", [(0, "and Egyptian tomb", "s45"), (1, "And a little over", "s46"), (2, "Some time in", "s47"), (2, "The eruption threw", "s48")],
     {"chapter": "The volcano next door"}),
    (5, 1, "collision", "s49", [], {}),
    (5, 2, "reversal", "s50", [(1, "Its last great", "s51")], {}),
    (5, 3, "tag", "s52", [], {}),
    (6, 0, "weigh", "s53", [(1, "So does", "s54"), (2, "Was the palace", "s55")], {"chapter": "The weighing"}),
    (6, 1, "test", "s56", [], {}),
    (6, 2, "close", "s57", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s10": ("s8", [1, 889, 500], "s10_add"), "s12": ("s11", [1, 889, 500], "s12_add"), "s15": ("s4", [1.2, 889, 560], "s15_add"),
    "s21": ("s20", [1.9, 470, 430], "s21_add"), "s23": ("s22", [1, 889, 500], "s23_add"), "s30": ("s29", [1, 889, 500], "s30_add"),
    "s34": ("s32", [1, 889, 500], "s34_add"), "s39": ("s38", [1, 889, 500], "s39_add"), "s43": ("s41", [1, 889, 500], "s43_add"),
    "s46": ("s44", [1.35, 820, 470], "s46_add"), "s51": ("s49", [1, 889, 500], "s51_add"), "s55": ("s53", [1, 889, 500], "s55_add"),
    "s57": ("s1", [1.06, 950, 470], "s57_add"),
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
    assert 19000 < PLAN_AREA < 21000, PLAN_AREA            # the plan's footprint: about 20,000 square metres, as said
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
    ep = {"id": "lf-knossos", "code": "LF.18", "series": script["series"], "title": script["title"], "case": "knossos",
          "verdict": "plausible", "claim": "Does the Minotaur's Labyrinth remember a real place?", "mood": "mystery",
          "hook_text": "Was the Labyrinth a *real* place?", "beats": beats, "shots": shots,
          "sources": "Evans 1921-1935 (The Palace of Minos) · Evans 1901 (doi:10.2307/623870) · MacGillivray 2000 · Castleden 1990 · "
                     "Ventris & Chadwick 1953 (doi:10.2307/628239) · Chadwick 1958 · Ventris & Chadwick 1956 (KN Gg 702) · "
                     "Manning et al. 2006 (doi:10.1126/science.1125682) · Pearson et al. 2018 (doi:10.1126/sciadv.aar8241) · Plutarch, Theseus · Thucydides 1.4",
          "post": "A young acrobat flying over a charging bull, painted at Knossos about 1450 BCE, and a clay tablet from the same palace that sends honey to "
                  "the Mistress of the Labyrinth. The myth of Minos and the Minotaur, Evans's dig and his concrete, the bulls and the double axes, Linear B "
                  "read as Greek, the eruption of Thera and the fall of the palaces, weighed.",
          "hashtags": ["#Knossos", "#Minotaur", "#Labyrinth", "#Crete", "#Archaeology", "#WeighItYourself"],
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
