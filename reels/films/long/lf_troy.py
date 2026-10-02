"""LF.11 · Myths That Came True · Troy: The City Behind the Poem (16:9 long film, one wall).

The script is films/long/lf-troy/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at the
sentence where the picture changes (see BEATS). One scene per script shot (s1..s56; s5, the title, is the intro card over the panel
of s4), drawn while it is said: the hill of nine cities cut open with its layer of fire, the story as a black-figure frieze, Calvert's
mound, a doormat of letters for the strata, Schliemann's trench and the gold of Troy II, the walls of Troy VI to scale, Korfmann's
magnetometers, ditch and lower town, Kolb's reading, the Hittite archive and the treaty of Alaksandu, the spring cave, Ahhiyawa and the
quarrel over Wilusa, the poem's heirlooms (a boar's tusk helmet, the ships, the epithets) and its own additions (chariots as taxis,
iron, no Hittites), the earthquake and the fire, the sling stones, the ancient dates, the collapse around it, tree rings, the four
suspects, the ledger and the tests. Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred,
dotted = claimed (the story is lilac and dotted throughout).

Facts: the Short 'troy' (f11.py, rewrite/troy.json) and the script's facts_added (Blegen 1963; Schliemann 1875; Allen 1999; Korfmann
2004; Jablonka & Rose 2004; Kolb 2004, 2005; Easton et al. 2002; Beckman 1999; Beckman, Bryce & Cline 2011; Frank et al. 2002;
Hawkins & Easton 1996; Everson 2004; Hope Simpson & Lazenby 1970; Lord 1960; Finley 1954; Manning et al. 2023; Cline 2013, 2014).

Engine workaround (as in lf_voynich.py and lf_atlantis.py): the wall only adds elements to a panel on its first visit, at a beat start
or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag,
invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that
step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-troy/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-troy/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-troy RC_FILMS_EPS=/tmp/claude-0/sbx_lf-troy/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-troy/boards python3 films.py long.lf_troy
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-troy", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
TERRA, TERRA_D, BLK = "#c46d3a", "#9c4f26", "#1d130d"        # the black-figure frieze: clay and slip
STONE, STONE_D, MUD = "#d6c49c", "#8c7656", "#a8774e"         # limestone, its shade, mudbrick
FIRE, ASH, CHAR = "#ff7a4a", "#4a1d12", "#160d09"
SKIN, WOOD, WOOD_D = "#e8d6b8", "#6b4a30", "#3a281a"
BRONZE, IRON = "#c98a4a", "#5a5650"
SEAC = "#3f86a8"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "open": "#f0b06a", "ruled": "#e98a8a"}


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


def crown(x, y, s, at, c=GOLD):
    return poly([[x - s, y], [x - s, y - s * 1.1], [x - s * .5, y - s * .5], [x, y - s * 1.2], [x + s * .5, y - s * .5], [x + s, y - s * 1.1], [x + s, y]], c, at=at, fx="pop")


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


def tablet(x, y, w, h, at, c="#a8865e", rows=7, cols=6, ink="#4a3522", fx="pop", op=None, seed=1, edge="#e9dccb"):
    """A clay tablet with cuneiform."""
    out = [rect(x, y, w, h, c, edge, 1.5, min(w, h) * .12, at, fx=fx, op=op)]
    out.append({"k": "glyphs", "x": round(x + w * .1, 1), "y": round(y + h * .08, 1), "w": round(w * .8, 1), "h": round(h * .84, 1), "rows": rows, "cols": cols,
                "kind": "cuneiform", "c": ink, "seed": seed, "in": round(at + .1, 2)})
    return out


def scroll(x, y, w, h, at, c="#e9d6ad", fx="pop"):
    """A small rolled scroll seen from the side, partly open."""
    return [rect(x, y, w, h, c, "#8a6a3e", 1.5, 3, at, fx=fx), {"k": "glyphs", "x": round(x + w * .12, 1), "y": round(y + h * .15, 1), "w": round(w * .76, 1),
            "h": round(h * .7, 1), "rows": 4, "cols": 5, "kind": "latin", "c": "#6a5a44", "in": round(at + .1, 2)},
            rect(x - 8, y - 6, 16, h + 12, "#c9ad7d", "#8a6a3e", 1.5, 8, at, fx=fx), rect(x + w - 8, y - 6, 16, h + 12, "#c9ad7d", "#8a6a3e", 1.5, 8, at, fx=fx)]


def flame(x, y, s, at, c=FIRE):
    """A small flame glyph standing on y."""
    return [poly([[x, y], [x - .45 * s, y - .35 * s], [x - .25 * s, y - .8 * s], [x - .05 * s, y - .55 * s], [x + .05 * s, y - 1.1 * s], [x + .35 * s, y - .6 * s],
                  [x + .45 * s, y - .3 * s]], c, "#ffd08a", 1.5, at, fx="pop", curve=True), gl(x, y - .5 * s, 1.6 * s, at, .5, "fire")]


def stones(cx, base, n, at, r=7, seed=3, c="#9a958c", step=.03, width=None):
    """A heap of round sling stones, built bottom up."""
    rnd = random.Random(seed)
    out, k, row = [], 0, 0
    width = width or n * r * .55
    while k < n:
        m = max(1, int((width - row * r * 1.6) / (2 * r)))
        for j in range(m):
            if k >= n:
                break
            x = cx + (j - (m - 1) / 2) * 2.05 * r + rnd.uniform(-1.5, 1.5)
            y = base - r - row * 1.65 * r + rnd.uniform(-1, 1)
            out.append(circ(x, y, r * rnd.uniform(.85, 1.1), c, "#5a554e", 1.2, at + step * k, fx="pop"))
            k += 1
        row += 1
    return out


# ================================================================== black-figure silhouettes (the story, s3)
def warrior(x, y, h, at, face=1, c=BLK, inc=TERRA):
    """A hoplite in silhouette: crested helmet, round shield, spear; feet on y, facing `face`."""
    f = face
    X = lambda a: x + f * a
    out = [ln([[X(0), y - .46 * h], [X(-.16 * h), y]], at, c, .07 * h, draw=False), ln([[X(0), y - .46 * h], [X(.16 * h), y]], at, c, .07 * h, draw=False),
           poly([[X(-.09 * h), y - .46 * h], [X(.09 * h), y - .46 * h], [X(.12 * h), y - .8 * h], [X(-.1 * h), y - .8 * h]], c, at=at),
           circ(X(.02 * h), y - .88 * h, .075 * h, c, at=at),
           poly([[X(-.05 * h), y - .95 * h], [X(-.02 * h), y - 1.04 * h], [X(-.22 * h), y - 1.0 * h], [X(-.3 * h), y - .86 * h], [X(-.12 * h), y - .93 * h]], c, at=at, curve=True),
           ln([[X(-.32 * h), y - .2 * h], [X(.5 * h), y - 1.12 * h]], at, c, .03 * h, draw=False),
           circ(X(.16 * h), y - .62 * h, .19 * h, c, at=at),
           circ(X(.16 * h), y - .62 * h, .13 * h, "none", inc, 1.5, at, op=.7)]
    return out


def galley(x, y, w, at, c=BLK, face=-1):
    """A Greek warship in silhouette, bow (ram) towards `face`; y = the waterline."""
    f = face
    X = lambda a: x + f * a * w
    hull = [[X(-.52), y + .01 * w], [X(-.42), y + .045 * w], [X(.3), y + .045 * w], [X(.46), y - .02 * w], [X(.5), y - .12 * w], [X(.47), y - .2 * w], [X(.43), y - .19 * w],
            [X(.45), y - .12 * w], [X(.4), y - .05 * w], [X(-.4), y - .05 * w], [X(-.46), y - .11 * w], [X(-.5), y - .1 * w], [X(-.47), y - .03 * w]]
    out = [poly(hull, c, at=at, curve=False), ln([[X(.02), y - .05 * w], [X(.02), y - .42 * w]], at, c, max(2, .012 * w), draw=False),
           ln([[X(-.16), y - .38 * w], [X(.2), y - .38 * w]], at, c, max(2, .01 * w), draw=False)]
    out += [ln([[X(-.34 + .07 * k), y + .02 * w], [X(-.39 + .07 * k), y + .1 * w]], at, c, max(1.5, .007 * w), draw=False) for k in range(10)]
    return out


def woman(x, y, h, at, c=BLK):
    """A standing woman in a long robe, in silhouette."""
    return [poly([[x - .07 * h, y - .78 * h], [x + .07 * h, y - .78 * h], [x + .19 * h, y], [x - .19 * h, y]], c, at=at),
            circ(x, y - .87 * h, .075 * h, c, at=at), poly([[x - .02 * h, y - .97 * h], [x + .1 * h, y - .9 * h], [x + .14 * h, y - .6 * h], [x + .07 * h, y - .62 * h]], c, at=at)]


def walled_city(x0, x1, base, top, at, c=BLK, style="known", fill=None, w=0, gate=True):
    """Walls with towers and battlements between x0 and x1, standing on `base`, walls up to `top` (towers higher)."""
    pts, n = [], 7
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    for k in range(n):
        a, b = xs[k], xs[k + 1]
        tw = k % 3 == 0
        tt = top - (base - top) * (.45 if tw else 0)
        seg = [[a, tt]]
        m = 4
        for j in range(m):
            u0, u1 = a + (b - a) * j / m, a + (b - a) * (j + .5) / m
            seg += [[u0, tt], [u0, tt - 10], [u1, tt - 10], [u1, tt]]
        seg.append([b, tt])
        pts += seg
    shape = [[x0, base]] + pts + [[x1, base]]
    out = [poly(shape, fill if fill is not None else c, c if fill is not None else "none", w, at, style=style)]
    if gate:
        gx = (x0 + x1) / 2
        out.append(poly([[gx - 24, base], [gx - 24, base - 50], [gx, base - 70], [gx + 24, base - 50], [gx + 24, base]], TERRA if fill is None else "rgba(0,0,0,.25)",
                        "none" if fill is None else c, w, at + .05, style=style))
    return out


def meander(x0, x1, y, h, at, c=BLK, u=46, w=4):
    """A running Greek key between x0 and x1, height h, top at y."""
    out = [ln([[x0, y + h], [x1, y + h]], at, c, w, draw=False), ln([[x0, y - 6], [x1, y - 6]], at, c, w * .6, draw=False)]
    x = x0
    while x + u <= x1 + .1:
        out.append(ln([[x, y + h], [x, y], [x + .72 * u, y], [x + .72 * u, y + .66 * h], [x + .3 * u, y + .66 * h], [x + .3 * u, y + .34 * h]], at, c, w, draw=False))
        x += u
    return out


# ================================================================== the hill (s1, s4, s7, s10, s56): one geometry, three moods
MCX, MHW, MG, MH, MPL = 900, 640, 700, 330, .42              # centre, half width, ground, height, plateau (fraction of half width)
TB = [0.0, .16, .29, .40, .47, .54, .60, .75, .85, .93, 1.0]   # stratum boundaries (fraction of height at the centre): rock, I..IX
TCOL = ["#5c574c", "#6f5a44", "#8a7250", "#755f40", "#927c5a", "#7a6446", "#ad8f66", "#7f6245", "#9d8464", "#b49c77"]
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]


def surf(x, h=MH, g=MG, cx=MCX, hw=MHW, pl=MPL):
    u = abs(x - cx) / hw
    if u >= 1:
        return g
    s = 1.0 if u < pl else .5 * (1 + math.cos(math.pi * (u - pl) / (1 - pl)))
    bump = 4 * math.sin(x / 41.0) * (1 if u < pl else 0) + 3 * math.sin(x / 23.0 + 1) * s
    return g - h * s + bump


def yb(k, x):
    """The floor of stratum k (k = 1..9: Troy I..IX; k = 10: the surface)."""
    if k >= 10:
        return surf(x)
    u = (x - MCX) / MHW
    return MG - MH * TB[k] * (1 - .10 * u * u)


def stratum(k, step=8):
    """The polygon of stratum k (0 = the rock), clipped by the slope of the mound."""
    top, bot = [], []
    x = MCX - MHW
    while x <= MCX + MHW + .1:
        s, lo = surf(x), yb(k, x)
        hi = yb(k + 1, x) if k + 1 < 10 else s
        if s < lo - .5:
            top.append((x, max(hi, s))); bot.append((x, lo))
        x += step
    return top + bot[::-1]


def mid(k, x):
    return (yb(k, x) + max(yb(k + 1, x) if k + 1 < 10 else surf(x), surf(x))) / 2


def flank(k, side):
    """x where the slope crosses the floor of stratum k, on the left (side -1) or right (+1)."""
    x = MCX
    while abs(x - MCX) < MHW and surf(x) < yb(k, x) - .5:
        x += side * 2
    return x


def hill_section(at=-1, day=False, trench=False):
    """The mound of Hisarlik cut open: the back of the hill behind the cut, the rock, nine strata with wall stubs, Troy VI's wall at the
    flanks, Roman columns on the summit."""
    rnd = random.Random(11)
    back = [(MCX - MHW * 1.04 + 18, MG)] + [(x + 18, surf(x - 18, MH * 1.06, MG, MCX, MHW * 1.04) - 10) for x in range(int(MCX - MHW * 1.04), int(MCX + MHW * 1.04) + 1, 10)] + [(MCX + MHW * 1.04 + 18, MG)]
    els = [poly(back, "#4a4232" if day else "#3a3326", "#7d8a52" if day else "#5f6a40", 2.5, at)]
    for k in range(10):
        els.append(poly(stratum(k), TCOL[k], "rgba(30,20,12,.35)", 1, at))
    # wall stubs: foundations standing on the floor of each stratum
    for k in range(1, 10):
        for j in range(5):
            x = MCX + rnd.uniform(-.62, .62) * MHW
            lo = yb(k, x); hi = max(yb(k + 1, x) if k + 1 < 10 else surf(x), surf(x))
            t = lo - hi
            if t < 14:
                continue
            ww = rnd.uniform(9, 17); hh = t * rnd.uniform(.4, .65)
            els.append(rect(x - ww / 2, lo - hh, ww, hh, STONE, "rgba(40,30,20,.5)", 1, 1, at, op=.85))
    # Troy VI's wall where the stratum meets the slope, both sides (a stone wedge, its outer face battered)
    for side in (-1, 1):
        xa = flank(6, side) - side * 6
        xb = flank(7, side)
        ya, yt = yb(6, xa), yb(7, xb) + 2
        out_foot = xa - side * 4
        els.append(poly([(out_foot, ya), (xb + side * 2, yt), (xb - side * 26, yt), (xa - side * 40, ya)], "url(#k-blocks)", "rgba(255,236,206,.5)", 1, at))
    # the summit: Troy IX's columns and a fallen drum
    for cx_ in (812, 858):
        s = surf(cx_)
        els += [rect(cx_ - 7, s - 52, 14, 52, "#efe6d2", "rgba(40,30,20,.4)", 1, 1, at), rect(cx_ - 10, s - 57, 20, 6, "#efe6d2", "none", 0, 1, at)]
    els.append(poly(E(930, surf(930) - 6, 14, 7, 18), "#e2d8c2", "rgba(40,30,20,.4)", 1, at))
    els.append(ln([(x, surf(x)) for x in range(MCX - MHW, MCX + MHW + 1, 8)], at, "rgba(255,226,190,.75)" if not day else "rgba(240,248,220,.8)", 2, draw=False))
    if trench:
        tx0, tx1, tb = 788, 1012, 642
        poly_ = [(tx0, surf(tx0))] + [(x, surf(x) - 2) for x in range(tx0 + 8, tx1, 8)][:0] + [(tx0 + 46, tb), (tx1 - 46, tb), (tx1, surf(tx1))]
        els.append(poly(poly_, "#2a2019", "rgba(255,226,190,.45)", 1.5, at))
    return els


def cypress(x, y, h, at, c="#1f241a"):
    return [poly(E(x, y - h * .5, h * .14, h * .5, 20), c, at=at), ln([[x, y], [x, y - h * .1]], at, "#2a2016", 3, draw=False)]


# ================================================================== COLD OPEN
def s1():
    """The hero image, complete from the first frame: the hill of Hisarlik at dusk, cut open, nine cities stacked; the numerals I to IX
    pop on 'nine', up the right side, each tied to its layer."""
    els = [poly([(-40, 684), (300, 684), (300, 700), (-40, 700)], "#3f6f8a", "none", 0, -1),
           ln([(-40, 686), (280, 686)], -1, "rgba(255,226,190,.55)", 1.5, draw=False)]
    els += cypress(196, 702, 66, -1) + cypress(228, 704, 50, -1) + cypress(1738, 704, 60, -1)
    els += hill_section(-1)
    els += [gl(900, 560, 600, -1, .22, "lamp"), person(1010, round(surf(1010), 1), 22, -1, "#f2e4c8", None) | {"in": -1}]
    tn = T("s1", "nine")
    for k in range(1, 10):
        y = 668 - (k - 1) * 37
        if k < 9:
            xm = (flank(k, 1) + flank(k + 1, 1)) / 2
            ym = surf(xm) + 7
        else:
            xm = flank(9, 1) - 40
            ym = mid(9, xm)
        at = tn + .22 * (k - 1)
        els += [ln([(xm + 4, ym), (1548, y - 8)], at, "rgba(245,236,220,.55)", 1.2, dur=.3),
                lab(1560, y, ROMAN[k], at + .1, BONE, 26, "start", st="serif", fx="pop")]
    return {"base": "sky", "tod": "dusk", "ground": 700, "sun": [140, 642, 22],
            "ridges": [{"y": 674, "a": 46, "c": "#3b3140", "seed": 3}, {"y": 702, "a": 16, "c": "#2a2229", "seed": 9}], "cam": CAM, "els": els}


def s2_add():
    """Zoom on Troy VII: its lower part (VIIa) chars and glows; burnt walls, beams, heaps of sling stones; the date."""
    tf, td, ts = T("s2", "layer of fire"), T("s2", "houses burnt"), T("s2", "sling stones")
    pts_lo = [(x, yb(7, x)) for x in range(int(flank(7, -1)) + 4, int(flank(7, 1)) - 3, 8)]
    pts_hi = [(x, yb(7, x) - (yb(7, x) - max(yb(8, x), surf(x))) * .55) for x, _ in pts_lo]
    els = [poly(pts_hi + pts_lo[::-1], ASH, "rgba(255,138,90,.6)", 1.5, tf, op=.95)]
    rnd = random.Random(5)
    for k, x in enumerate((640, 760, 880, 1000, 1120, 1240)):
        els.append(gl(x, yb(7, x) - 8, 70, tf + .1 * k, .55, "fire", pulse=True))
    for k in range(34):
        x = rnd.uniform(560, 1300); y0 = yb(7, x); y1 = y0 - (y0 - max(yb(8, x), surf(x))) * .5
        els.append(dot(round(x, 1), round(rnd.uniform(y1, y0 - 2), 1), round(rnd.uniform(1.6, 3), 1), "#ffb070", round(tf + .3 + .02 * k, 2)))
    for k, x in enumerate((690, 820, 950, 1080, 1190)):
        y0 = yb(7, x)
        els.append(poly([(x - 8, y0), (x - 8, y0 - 15), (x - 3, y0 - 19), (x + 2, y0 - 13), (x + 8, y0 - 17), (x + 8, y0)], CHAR, "rgba(255,150,90,.5)", 1, td + .15 * k, fx="rise"))
    for k, x in enumerate((735, 905, 1135)):
        y0 = yb(7, x)
        els.append(ln([(x - 22, y0 - 3), (x + 20, y0 - 15)], td + .4 + .15 * k, "#1a0f0a", 3.5, dur=.3))
    els += stones(780, yb(7, 780) - 1, 14, ts, 3.2, 4, step=.03, width=30) + stones(1040, yb(7, 1040) - 1, 16, ts + .3, 3.2, 6, step=.03, width=34)
    els += [gl(965, yb(7, 965) - 6, 26, ts + 1.4, .7, "lamp")]
    els += [ln([(1090, yb(7, 1090) + 2), (1124, 556)], td - .1, RED, 1.5, dur=.3)] + chip(1150, 580, "about 1180 BCE", RED, td - .2, 26)
    return els


def s3():
    """The story as a black-figure frieze: Troy on its hill, the Greek ships and warriors, ten years, Helen on the wall."""
    tt, tk, ty, th = T("s3", "Troy"), T("s3", "Greek kings"), T("s3", "ten years"), T("s3", "Helen")
    y0, y1 = 200, 650
    els = [rect(88, y0 - 20, 1602, y1 - y0 + 40, "#2a1a10", "none", 0, 18, -1),
           rect(100, y0, 1578, y1 - y0, TERRA, "rgba(255,226,190,.35)", 2, 10, .2, fx="fade"),
           rect(100, y0, 1578, 28, TERRA_D, "none", 0, 0, .25, op=.6), rect(100, y1 - 28, 1578, 28, TERRA_D, "none", 0, 0, .25, op=.6),
           gl(889, 420, 760, .2, .18, "lamp")]
    els += meander(120, 1660, y0 + 18, 30, .3) + meander(120, 1660, y1 - 54, 30, .3)
    els += [poly([(130, 594), (200, 524), (320, 474), (480, 470), (560, 512), (630, 594)], BLK, at=tt, curve=True)]
    els += walled_city(190, 590, 488, 398, tt + .1)
    els += woman(432, 398, 72, th)
    els.append(ln([(660, 598)] + [(660 + 12 * k, 598 + (4 if k % 2 else -4)) for k in range(1, 85)], tk, BLK, 3, draw=False))
    for k, x in enumerate((800, 960, 1120, 1280, 1440, 1600)):
        els += galley(x, 586 - (k % 2) * 8, 150, tk + .12 * k)
    for k, x in enumerate((650, 715, 780)):
        els += warrior(x, 596, 118, tk + .5 + .15 * k, face=-1)
    for k in range(10):
        x = 1010 + 30 * k
        els.append(ln([(x, 300), (x - 6, 352)], ty + .12 * k, BLK, 7, dur=.15))
    els += [lab(400, 282, "Troy", tt + .2, LILAC, 40, st="ital"), lab(1145, 270, "ten years", ty + .3, LILAC, 34, st="ital"),
            lab(528, 352, "Helen", th + .2, LILAC, 32, st="ital", a="start")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def story_city(at, op=.9):
    """The story's city, floating above the hill: lilac and dotted (a claim, not a find)."""
    out = walled_city(600, 1200, 305, 218, at, LILAC, "claimed", "rgba(201,193,238,.06)", 3)
    for e in out:
        e.update(op=op, keepop=True)
    return out


def s4_add():
    """The story above, the ground below, and the question between."""
    tw = T("s4", "Trojan War")
    els = story_city(.5) + [lab(1230, 250, "the story", 1.0, LILAC, 32, "start", st="ital"),
                            ln([(404, 552), (438, 556)], 1.4, DIM, 1.5, dur=.3), lab(398, 560, "the ground", 1.5, BONE, 28, "end")]
    els += qmark(1420, 300, tw, 120)
    return els


# ================================================================== CHAPTER 1 · A hill of nine cities
def s6():
    """Where: the Dardanelles between the Aegean and the Sea of Marmara, the way to the Black Sea; Hisarlik at its mouth."""
    v = View(24.6, 29.4, 39.35, 41.35, (90, 120, 1600, 680))
    strait = [(26.17, 40.0), (26.26, 40.06), (26.40, 40.13), (26.45, 40.2), (26.53, 40.3), (26.66, 40.4), (26.85, 40.48)]
    route = [(25.4, 39.88), (26.1, 39.98), (26.4, 40.14), (26.66, 40.4), (27.3, 40.62), (28.3, 40.8), (28.98, 41.0), (29.08, 41.2)]
    hx, hy = v.p(26.2389, 39.9575)
    t0 = T("s6", "narrow strait")
    els = [{"k": "map", "land": v.land(), "in": -1},
           ln([v.p(*q) for q in strait], t0, "#bfe6f5", 8, dur=1.0, curve=True, op=.9),
           arr([v.p(*q) for q in route], t0 + .9, AMBER, 4, dur=1.8),
           lab(*v.p(29.25, 41.27), "to the Black Sea", t0 + 2.4, AMBER, 28, "end"),
           {"k": "pin", "x": hx, "y": hy, "t": "Hisarlik", "c": GOLD, "a": "end", "lx": -20, "ly": 30, "in": .6},
           lab(*v.p(25.25, 39.62), "Aegean Sea", .9, "#9fd0ff", 34, st="ital"),
           lab(*v.p(28.05, 40.66), "Sea of Marmara", 1.2, "#9fd0ff", 30, st="ital"),
           lab(*v.p(26.62, 40.1), "Dardanelles", t0 + .5, BONE, 26, "start"),
           {"k": "scale", "x": 160, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": 1.4}]
    return {"base": "map", "cam": CAM, "els": els}


def calvert_mound(at=-1, cx=760, hw=560, h=300):
    pts = [(x, surf(x, h, MG, cx, hw)) for x in range(cx - hw, cx + hw + 1, 8)]
    rnd = random.Random(31)
    out = [poly([(cx - hw, MG)] + pts + [(cx + hw, MG)], "#5f6a3e", "#9fb06a", 2, at),
           poly([(x, y + 26) for x, y in pts[6:-6]], "none", "rgba(255,255,255,.06)", 2, at)]
    for k in range(16):
        x = cx + rnd.uniform(-.85, .85) * hw
        y = surf(x, h, MG, cx, hw) + rnd.uniform(14, 60)
        out.append(poly(E(x, y, rnd.uniform(14, 26), rnd.uniform(6, 10), 14), "#4f5a32", at=at, op=.8))
    return out


def s7():
    """Calvert's mound in the 1860s: his part of the hill, two trial trenches, and his hunch."""
    t1, t2, th = T("s7", "owned part"), T("s7", "trial trenches"), T("s7", "He was sure")
    cx, hw, h = 760, 560, 300
    S_ = lambda x: surf(x, h, MG, cx, hw)
    xb = 880
    east = [(xb, S_(xb))] + [(x, S_(x)) for x in range(xb + 8, cx + hw + 1, 8)] + [(cx + hw, MG), (xb, MG)]
    els = calvert_mound(-1, cx, hw, h)
    els += [poly(east, "rgba(232,184,122,.18)", "none", 0, t1), ln([(xb, S_(xb) - 6), (xb, MG)], t1, AMBER, 2.5, "inferred", dur=.8),
            lab(1090, 620, "Calvert's land", t1 + .4, AMBER, 30)]
    for k, (x, d, yr) in enumerate(((1010, 38, "1863"), (1150, 30, "1865"))):
        s = S_(x)
        els += [poly([(x - 20, s - 2), (x + 20, s - 2), (x + 16, s + d), (x - 16, s + d)], "#2a2019", "rgba(255,226,190,.5)", 1.2, t2 + .5 * k, fx="pop"),
                lab(x, s - 26, yr, t2 + .5 * k + .1, BONE, 24)]
    els += [person(1390, 700, 68, t1 - .3, SKIN), ln([(1415, 700), (1434, 640)], t1 - .1, "#8a6a48", 4, draw=False),
            poly([(1408, 703), (1422, 703), (1419, 716), (1411, 716)], "#9aa0a8", at=t1 - .1),
            lab(1390, 604, "Frank Calvert", t1, BONE, 26)]
    els += walled_city(500, 1020, 600, 520, th, LILAC, "claimed", "rgba(201,193,238,.05)", 2.2, gate=False)
    els += [lab(cx, 372, "Hisarlik", .8, BONE, 34, st="serif")]
    return {"base": "sky", "tod": "day", "ground": 700, "sun": [300, 230, 30], "cam": CAM, "els": els}


def s8_add():
    """Schliemann arrives: money, and a great hurry."""
    tn, tm, th = T("s8", "Heinrich Schliemann"), T("s8", "money"), T("s8", "great hurry")
    x = 1590
    els = [person(x, 700, 70, tn - .4, "#cbbca8"), rect(x - 13, 616, 26, 15, "#1a1511", at=tn - .4, fx="rise"), rect(x - 19, 629, 38, 4, "#1a1511", at=tn - .4, fx="rise"),
           lab(x, 548, "Heinrich", tn, BONE, 26), lab(x, 580, "Schliemann", tn + .05, BONE, 26), lab(x, 512, "1868", tn + .3, AMBER, 24)]
    for k in range(6):
        els.append(poly(E(1488, 692 - 9 * k, 20, 6, 18), AU, "#7a5a1a", 1.2, tm + .06 * k, fx="pop"))
    els += [circ(1496, 610, 22, "#e8dcc2", "#8a6a3e", 3, th, fx="pop"), ln([(1496, 610), (1496, 595)], th + .2, "#3a2a1a", 3, dur=.2),
            ln([(1496, 610), (1508, 616)], th + .3, "#3a2a1a", 3, dur=.2), ln([(1496, 588), (1496, 580)], th, "#8a6a3e", 3, draw=False)]
    return els


def s9():
    """Post on a doormat: the first letter ends at the bottom. The mound the same way: oldest at the base, where Schliemann looked."""
    tp, tf, tb, th = T("s9", "post piles up"), T("s9", "the first letters"), T("s9", "Homer's Troy"), T("s9", "near the base")
    els = [gl(420, 470, 420, .2, .22, "lamp"),
           rect(250, 170, 250, 520, WOOD, "#8a6a48", 2, 6, .2), rect(272, 196, 206, 210, "none", "rgba(255,226,190,.25)", 2, 4, .3),
           rect(272, 430, 206, 230, "none", "rgba(255,226,190,.25)", 2, 4, .3), rect(320, 400, 110, 20, GOLD, "#7a5a1a", 1.5, 4, .4),
           circ(462, 470, 8, GOLD, at=.4), rect(190, 690, 370, 24, "#7a5236", "#a87a52", 1.5, 6, .5),
           ln([(120, 714), (650, 714)], .1, "#6a5a48", 2, draw=False)]
    rnd = random.Random(2)
    for k in range(8):
        x = 375 + rnd.uniform(-22, 22); y = 682 - 15 * k
        at = tp + .35 * k
        els += [rect(x - 50, y - 28, 100, 30, "#efe3c8", "#8a7a66", 1.5, 3, at, fx="pop"),
                ln([(x - 48, y - 26), (x, y - 10), (x + 48, y - 26)], at + .05, "#8a7a66", 1.2, draw=False),
                lab(x + 36, y - 6, str(k + 1), at + .05, "#6a4a2a", 18, halo=False)]
    els += [lab(560, 676, "first", tf, AMBER, 26, "start"), lab(560, 560, "last", tf + .4, AMBER, 26, "start")]
    # the mound, the same rule
    x0, x1, base, top = 940, 1420, 690, 290
    cols = TCOL[1:]
    for k in range(9):
        ya = base - (base - top) * k / 9; yb_ = base - (base - top) * (k + 1) / 9
        els.append(rect(x0, yb_, x1 - x0, ya - yb_, cols[k], "rgba(30,20,12,.4)", 1, 0, .6 + .08 * k, fx="fill", dur=.4))
    els += [arr([(1460, 680), (1460, 300)], tf, AMBER, 3, dur=.9, curve=False), lab(1480, 690, "oldest", tf + .2, AMBER, 26, "start"),
            lab(1480, 310, "youngest", tf + .8, AMBER, 26, "start"),
            ln([(640, 670), (920, 670)], tf + .3, DIM, 1.5, "inferred", dur=.6), ln([(640, 545), (920, 330)], tf + .7, DIM, 1.5, "inferred", dur=.6)]
    els += [rect(970, 624, 420, 58, "rgba(201,193,238,.12)", LILAC, 2.5, 8, th, style="claimed"), lab(1180, 664, "Homer's Troy?", th + .1, LILAC, 30, st="ital"),
            arr([(1180, 560), (1180, 618)], tb, LILAC, 3, "claimed", .5, False)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def worker(x, y, at, h=20, c="#2a2018"):
    return [person(x, y, h, at, c, "rise")]


def s10():
    """The great trench through the heart of the hill (from 1871), workmen and spoil; then thirty Olympic pools of earth."""
    tt, tn, tp = T("s10", "drove a vast trench"), T("s10", "eighty thousand"), T("s10", "Olympic swimming pools")
    els = [poly([(1540, 700), (1590, 670), (1650, 664), (1710, 690), (1740, 700)], "#8a7458", "#b39a75", 1.5, tt + .8, fx="rise"),
           poly([(70, 700), (120, 674), (190, 668), (250, 700)], "#8a7458", "#b39a75", 1.5, tt + 1.0, fx="rise")]
    els += hill_section(.0, day=True)
    tx0, tx1, tb = 790, 1010, 642
    trench = [(tx0, surf(tx0) - 1), (tx0 + 44, tb), (tx1 - 44, tb), (tx1, surf(tx1) - 1)]
    els += [poly(trench, "#2a2019", "rgba(255,240,210,.6)", 1.5, tt, fx="fill", dur=1.4)]
    for k, (x, y) in enumerate(((850, tb), (884, tb), (930, tb), (958, tb), (770, surf(770)), (1030, surf(1030)))):
        els += [person(x, round(y, 1), 22, tt + 1.2 + .12 * k, "#2a2018")]
    els += [ln([(1040, surf(1040)), (1560, 690)], tt + 1.5, "rgba(255,240,210,.5)", 1.5, "inferred", dur=1.0)]
    els += chip(400, 240, "1871", AMBER, tt + .3, 28)
    for k in range(30):
        cx_, cy_ = 1384 + 53 * (k % 6), 150 + 33 * (k // 6)
        at = tp - .3 + .05 * k
        els += [rect(cx_, cy_, 46, 24, "#3f86a8", "#bfe6f5", 1.2, 3, at, fx="pop"), ln([(cx_ + 5, cy_ + 12), (cx_ + 41, cy_ + 12)], at + .05, "rgba(255,255,255,.55)", 1, draw=False)]
    els += [lab(1700, 350, "about 80,000 cubic metres", tn, BONE, 26, "end"), lab(1700, 384, "30 Olympic pools", tp + .3, BLUE, 26, "end")]
    return {"base": "sky", "tod": "day", "ground": 700, "sun": [300, 200, 30],
            "ridges": [{"y": 676, "a": 40, "c": "#59607a", "seed": 3}, {"y": 702, "a": 14, "c": "#4a4f60", "seed": 9}], "cam": CAM, "els": els}


def diadem(cx, y, at, s=1.0):
    """The great diadem of 'Priam's treasure': a band, a fringe of short chains of tiny leaves, two long side pendants."""
    els = [ln([(cx - 300 * s + 20 * s * k, y + 14 * s * math.sin(math.pi * k / 30) * -1 + 10 * s) for k in range(31)], at, AU, 6 * s, dur=.8, curve=True)]
    for k in range(48):
        x = cx - 270 * s + 11.5 * s * k
        y0 = y + 10 * s - 14 * s * math.sin(math.pi * (x - (cx - 300 * s)) / (600 * s))
        L = (120 + 40 * math.sin(k * .7)) * s
        a = at + .5 + .012 * k
        els.append(ln([(x, y0), (x, y0 + L)], a, "#c9a040", 1.4, dur=.3))
        els += [dot(round(x, 1), round(y0 + L * j / 4, 1), round(2.6 * s, 1), AU, round(a + .05 * j, 2)) for j in range(1, 5)]
    for side in (-1, 1):
        x = cx + side * 296 * s
        for j in range(5):
            xx = x + side * 7 * s * j
            a = at + 1.1 + .05 * j
            els.append(ln([(xx, y + 14 * s), (xx, y + 300 * s)], a, "#c9a040", 1.6, dur=.4))
            els += [poly(E(xx, y + (40 + 52 * m) * s, 5 * s, 9 * s, 12), AU, "#7a5a1a", .8, round(a + .06 * m, 2), fx="pop") for m in range(5)]
    return els


def s11():
    """The great diadem from 'Priam's treasure' (1873), glinting; the claim struck on 'Wrong city'."""
    tg, tp, tw = T("s11", "he found gold"), T("s11", "treasure of Priam"), T("s11", "Wrong city")
    els = [gl(889, 380, 520, .2, .35, "lamp")] + diadem(889, 230, tg) + [gl(700, 300, 60, tg + 1.2, .6, "lamp"), gl(1080, 320, 50, tg + 1.4, .6, "lamp")]
    els += [lab(889, 172, "Priam's treasure?", tp, LILAC, 34, st="ital"), strike(752, 160, 872, 160, tw, RED, 6),
            lab(1300, 190, "1873", tg + .2, AMBER, 28)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def XT(yr, x0=300, x1=1480, a=-2600, b=-1100):
    return round(x0 + (x1 - x0) * (yr - a) / (b - a), 1)


def s12_add():
    """Below the gold: Troy II against the war's dates, a thousand years apart."""
    t2, tw, tb = T("s12", "Troy Two"), T("s12", "any date for the war"), T("s12", "more than a thousand")
    y = 700
    ticks = [[XT(v), lab_] for v, lab_ in ((-2500, "2500 BCE"), (-2000, "2000"), (-1500, "1500"), (-1100, "1100"))]
    return [axis(300, 1480, y, ticks, .3),
            {"k": "band", "x0": XT(-2550), "x1": XT(-2300), "y": y - 50, "h": 18, "c": AU, "t": "Troy II", "tc": AU, "in": t2},
            {"k": "band", "x0": XT(-1250), "x1": XT(-1180), "y": y - 50, "h": 18, "c": LILAC, "t": "the war?", "tc": LILAC, "in": tw, "op": .9}] + \
        bracket(XT(-2300), XT(-1250), y - 100, tb, "over 1,000 years", BONE, up=False, size=28)


def s13_add():
    """The trench, close: the strata of Troy VI and VII as red ghosts across the gap."""
    tc = T("s13", "cut away")
    els = []
    for k in (6, 7):
        y0, y1 = yb(k, 790), yb(k + 1, 790)
        els += [ln([(800, y0), (1000, yb(k, 1000))], .5 + .3 * (k - 6), RED, 2.5, "inferred", dur=.6),
                ln([(800, y1), (1000, yb(k + 1, 1000))], .6 + .3 * (k - 6), RED, 2.5, "inferred", dur=.6)]
        for j in range(4):
            x = 820 + 50 * j
            els.append(rect(x, yb(k, x) - 12, 12, 12, "none", RED, 1.5, 1, .9 + .3 * (k - 6) + .08 * j, style="inferred"))
    els += [lab(1050, 410, "Troy VI and VII,", tc - .4, RED, 26, "start"), lab(1050, 442, "cut away", tc, RED, 26, "start")]
    return els


def s14():
    """Critics and admirers on one balance: destruction against a hill worth digging. Level."""
    td, tw, tb = T("s14", "destruction"), T("s14", "worth digging"), T("s14", "Both are right")

    def ruin(x, y):
        # a block of layers with a trench gouged through them, the cut outlined in red
        w, h = 156, 92
        cols = ["#b39b74", "#8f7656", "#a68c66", "#7a6248"]
        out = [rect(x - w / 2, y - h + 23 * j, w, 23, cols[j], "rgba(0,0,0,.25)", 1, 0, td, fx="pop") for j in range(4)]
        out += [poly([(x - 40, y - h), (x + 40, y - h), (x + 15, y - 12), (x - 15, y - 12)], "#241a14", RED, 3.5, td + .3, fx="pop"),
                lab(x, y + 64, "destruction", td + .2, RED, 30)]
        return out

    def lamp(x, y):
        return [ln([(x - 40, y), (x + 14, y - 120)], tw, "#8a6a48", 7, draw=False), poly([(x - 58, y + 2), (x - 24, y + 2), (x - 28, y - 30), (x - 52, y - 30)], "#9aa0a8", at=tw),
                poly(E(x + 46, y - 20, 24, 18, 16), GOLD, "#7a5a1a", 1.2, tw + .2, fx="pop"), gl(x + 46, y - 28, 100, tw + .2, .8, "lamp"),
                lab(x, y + 64, "worth digging", tw + .2, GOLD, 30)]
    els = balance(889, 330, 820, 720, .3, ruin, lamp, drop=210, pan=260) + [gl(889, 330, 170, tb, .55, "lamp")]
    els += [lab(479, 290, "his critics", td - .4, DIM, 26), lab(1299, 290, "his admirers", tw - .6, DIM, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== CHAPTER 2 · The walls and the lower town
def citadel_items():
    """The Troy VI citadel as a toy model: the hill top, a ring of wall with towers and a gate, terraces of houses, Schliemann's trench."""
    rnd = random.Random(7)
    n, R0 = 18, 30
    items = [{"t": "flat", "pts": [[R0 * 1.25 * math.cos(2 * math.pi * k / 24) * (1 + .06 * math.sin(3 * k)), R0 * 1.05 * math.sin(2 * math.pi * k / 24)] for k in range(24)],
              "y": -3, "c": "#7d6a4c"},
             {"t": "flat", "pts": [[R0 * .98 * math.cos(2 * math.pi * k / n), R0 * .8 * math.sin(2 * math.pi * k / n)] for k in range(n)], "y": 0, "c": "#9c8a6a"},
             {"t": "flat", "pts": [[-4.5, -R0 * .78], [4.5, -R0 * .78], [3.5, R0 * .78], [-3.5, R0 * .78]], "y": .05, "c": "#2a2019"}]
    for k in range(n):
        if k == 13:
            continue                                    # the south gate
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        P = lambda a, r: [r * math.cos(a), r * .8 * math.sin(a)]
        items.append({"t": "prism", "pts": [P(a0, R0), P(a1, R0), P(a1, R0 * .89), P(a0, R0 * .89)], "y": 0, "h": 4.2, "c": STONE, "edge": "rgba(0,0,0,.3)"})
    for k in (2, 7, 12, 14):
        a = 2 * math.pi * (k + .5) / n
        items.append({"t": "box", "x": R0 * .97 * math.cos(a), "z": R0 * .8 * .97 * math.sin(a), "y": 0, "w": 5.5, "d": 5.5, "h": 6.8, "c": "#cbb891", "edge": "rgba(0,0,0,.3)"})
    j = 0
    while j < 44:
        r = rnd.uniform(.25, .8) * R0; a = rnd.uniform(0, 2 * math.pi)
        x, z = r * math.cos(a), r * .8 * math.sin(a)
        if abs(x) < 6:
            continue
        items.append({"t": "box", "x": x, "z": z, "y": 0, "w": rnd.uniform(2.6, 4.6), "d": rnd.uniform(2.4, 3.8), "h": rnd.uniform(1.8, 3.2), "c": "#b8a57c", "edge": "rgba(0,0,0,.25)"})
        j += 1
    return items


def s15():
    """The walls Dörpfeld found: the citadel of Troy VI as a slowly turning model, Schliemann's trench across it."""
    td, tv = T("s15", "his architect"), T("s15", "Troy Six")
    els = [gl(889, 560, 620, .1, .22, "lamp"),
           {"k": "iso", "x": 889, "y": 540, "s": 12, "az": -24, "spin": .9, "el": .42, "items": citadel_items(), "in": .2},
           lab(889, 190, "Troy VI", tv, GOLD, 44, st="serif"), lab(1430, 720, "Dörpfeld, 1893", td + .5, DIM, 26)]
    return {"base": "dark", "stars": 70, "cam": CAM, "els": els}


def s16():
    """The wall to scale (40 units = 1 m): a battered stone base 5 m thick, mudbrick to 9 m; a person, a car, a three-storey house."""
    tc, t5, t9, tcar, th = T("s16", "A citadel of"), T("s16", "five metres"), T("s16", "nine metres"), T("s16", "car is long"), T("s16", "three-storey house")
    g = 700
    stone = [(560, g), (760, g), (760, g - 240), (610, g - 240)]
    els = [ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False), gl(700, 520, 420, .2, .2, "lamp"),
           poly(stone, "url(#k-blocks)", "rgba(255,236,206,.6)", 1.5, t5 - .6, fx="rise"),
           rect(640, g - 360, 120, 120, MUD, "rgba(255,236,206,.45)", 1.5, 0, t9 - .4, fx="fill", dur=.6)]
    els += [ln([(640, g - 360 + 20 * k), (760, g - 360 + 20 * k)], t9 - .1, "rgba(60,30,15,.45)", 1, draw=False) for k in range(1, 6)]
    els += [{"k": "dim", "x1": 560, "y1": g + 28, "x2": 760, "y2": g + 28, "t": "5 m", "c": AMBER, "ly": 34, "fx": "draw", "dur": .6, "in": t5},
            {"k": "dim", "x1": 520, "y1": g, "x2": 520, "y2": g - 360, "t": "about 9 m", "c": AMBER, "lx": -30, "fx": "draw", "dur": .8, "in": t9},
            lab(700, g - 380, "mudbrick", t9 + .4, MUD, 26),
            person(840, g, 68, .6, SKIN)]
    els += chip(330, 180, "about 1700 to 1300 BCE", GOLD, tc, 26)
    # the car: 4.5 m = 180 units, beside the wall, under a copy of the 5 m bar
    cx_ = 930
    els += [rect(cx_, g - 46, 180, 34, "#8a939c", "none", 0, 12, tcar, fx="pop"),
            poly([(cx_ + 34, g - 46), (cx_ + 58, g - 76), (cx_ + 130, g - 76), (cx_ + 156, g - 46)], "#6f777f", at=tcar, fx="pop"),
            circ(cx_ + 36, g - 10, 13, "#2a2622", at=tcar + .05, fx="pop"), circ(cx_ + 146, g - 10, 13, "#2a2622", at=tcar + .05, fx="pop"),
            ln([(cx_ - 10, g - 100), (cx_ + 190, g - 100)], tcar + .3, AMBER, 4, dur=.5), lab(cx_ + 90, g - 112, "5 m", tcar + .4, AMBER, 24),
            lab(cx_ + 90, g + 40, "a car, 4.5 m", tcar + .2, DIM, 24)]
    # a three-storey house, the wall's height
    hx = 1260
    els += [rect(hx, g - 360, 260, 360, "rgba(245,236,220,.05)", BONE, 2, 2, th, style="inferred")]
    els += [ln([(hx, g - 120 * k), (hx + 260, g - 120 * k)], th + .2, BONE, 1.5, "inferred", dur=.3) for k in (1, 2)]
    els += [rect(hx + 40 + 90 * j, g - 120 * k + 30, 46, 56, "rgba(255,226,168,.25)", "none", 0, 2, th + .3 + .05 * (3 * k + j), fx="pop") for k in (1, 2, 3) for j in range(2)]
    els += [lab(hx + 130, g + 40, "3 storeys", th + .4, BONE, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s17():
    """1988: Korfmann's team sweeps the fields outside the walls with magnetometers; a pencil rubbing brings out a hidden coin."""
    tk, tm, tc = T("s17", "Manfred Korfmann"), T("s17", "magnetometers"), T("s17", "pencil rubbed")
    g = 640
    els = [poly([(150, g + 2), (220, g - 34), (330, g - 52), (470, g - 50), (560, g - 26), (620, g + 2)], "#6a6a48", "rgba(255,255,255,.3)", 1.5, -1, curve=True)]
    # the citadel walls on the hill, far off: a band of wall with towers, roofs behind
    els += [rect(300 + 34 * j, g - 74 - 6 * (j % 3), 26, 18, "#9c8c70", at=-1) for j in range(5)]
    els += [rect(262, g - 62, 236, 16, "#b9a888", "rgba(60,50,40,.4)", 1, 1, -1)] + \
           [rect(tx_, g - 80, 20, 34, "#c8b796", "rgba(60,50,40,.4)", 1, 1, -1) for tx_ in (268, 372, 470)] + [lab(385, g - 100, "the citadel", .6, DIM, 24)]
    for k in range(7):
        xb = 560 + 150 * k
        els.append(ln([(xb, 812), (900 + (xb - 900) * .28, g + 4)], tm + .1 + .12 * k, "rgba(255,240,210,.35)", 2, "inferred", dur=1.0))
    for k, (x, y, h) in enumerate(((760, 760, 120), (1090, 700, 92))):
        a = tm - .2 + .4 * k
        xt = x + h * .42                                     # a gradiometer: an upright tube held in front, its foot just above the soil
        els += [person(x, y, h, a, SKIN), ln([(x + h * .1, y - h * .52), (xt, y - h * .56)], a + .1, "#d8d0c0", 4, draw=False),
                rect(xt - h * .04, y - h * .8, h * .08, h * .7, "#e8e0d0", "rgba(60,50,40,.5)", 1, 3, a + .1),
                rect(xt - h * .055, y - h * .84, h * .11, h * .08, "#4a5a6a", at=a + .1), rect(xt - h * .055, y - h * .14, h * .11, h * .08, "#4a5a6a", at=a + .1),
                ln([(x - h * .12, y - h * .74), (x + h * .1, y - h * .92), (xt, y - h * .84)], a + .1, "#4a5a6a", 2, draw=False, curve=True),
                rect(x - h * .2, y - h * .78, h * .16, h * .22, "#4a5a6a", at=a + .1)]
    els += chip(260, 200, "1988", AMBER, tk, 28) + [lab(260, 256, "Korfmann's team", tk + .2, BONE, 28)]
    els += [lab(830, 600, "magnetometer", tm + .4, BONE, 26), ln([(816, 610), (812, 652)], tm + .4, "rgba(255,240,210,.6)", 1.5, dur=.3)]
    px, py, pw, ph = 1260, 170, 380, 300
    els += [rect(px, py, pw, ph, "#efe6d2", "#8a7a66", 2, 6, tc - .3, fx="pop")]
    zz = []
    for k in range(26):
        x = px + 30 + 12.4 * k
        zz += [(x, py + 40), (x + 6, py + ph - 40)]
    els += [ln(zz, tc + .2, "#4a4440", 2.2, dur=2.2, op=.6),
            circ(px + pw / 2, py + ph / 2, 82, "none", "#2a2622", 4, tc + 1.6, op=.85),
            circ(px + pw / 2, py + ph / 2, 64, "none", "#2a2622", 1.5, tc + 1.9, op=.6),
            poly([(px + pw / 2 - 20, py + ph / 2 + 40), (px + pw / 2 - 30, py + ph / 2 - 5), (px + pw / 2 - 5, py + ph / 2 - 42), (px + pw / 2 + 25, py + ph / 2 - 30),
                  (px + pw / 2 + 20, py + ph / 2 + 10), (px + pw / 2 + 5, py + ph / 2 + 40)], "rgba(42,38,34,.35)", "#2a2622", 1.5, tc + 2.1, curve=True),
            poly([(px + pw - 40, py + 70), (px + pw + 10, py + 30), (px + pw + 22, py + 42), (px + pw - 28, py + 82)], "#e8c35a", "#7a5a1a", 1.2, tc, fx="pop"),
            lab(px + pw / 2, py + ph + 44, "a hidden coin", tc + 1.9, BONE, 28)]
    return {"base": "sky", "tod": "day", "ground": g, "sun": [1060, 170, 26], "cam": CAM, "els": els}


# the plan of Troy (s18, s19, s20): 100 m = 90 units; the citadel about 180 m across, the ditch about 400 m to the south
PX, PY, PU = 820, 250, .9                                    # citadel centre, units per metre


def plan_xy(xm, ym):
    return (round(PX + xm * PU, 1), round(PY + ym * PU, 1))


def citadel_ring(at, c=BONE, w=3, s=1.0, dx=0, dy=0):
    pts = [((PX + dx) + 100 * s * math.cos(2 * math.pi * k / 30) * (1 + .05 * math.sin(4 * k)), (PY + dy) + 80 * s * math.sin(2 * math.pi * k / 30)) for k in range(30)]
    return poly(pts, "rgba(214,196,156,.18)", c, w, at, curve=True)


def ditch_pts(s=1.0, dx=0, dy=0):
    pts = []
    for k in range(25):
        a = math.pi * (.08 + .84 * k / 24)
        pts.append(((PX + dx) + 380 * s * math.cos(a) * -1, (PY + dy) + 470 * s * math.sin(a) * .88))
    return pts


def s18():
    """The magnetic map: a dark line draws across it, the ditch about 400 m south of the citadel; a section of the ditch cut in bedrock."""
    td, tw, t4 = T("s18", "a ditch"), T("s18", "four metres"), T("s18", "four hundred metres")
    rnd = random.Random(9)
    els = []
    for i in range(26):
        for j in range(12):
            x, y = 380 + 36 * i, 330 + 36 * j
            v = int(rnd.uniform(90, 150))
            els.append(rect(x, y, 35, 35, "rgb(%d,%d,%d)" % (v, v - 4, v - 10), "none", 0, 0, .1 + .004 * (i + j), op=.55))
    els += [citadel_ring(.3), lab(PX, PY + 8, "citadel", .5, BONE, 26)]
    dp = ditch_pts()
    els += [ln(dp, td, "#1a120c", 13, dur=1.6, curve=True), ln(dp, td + .2, "rgba(255,160,100,.55)", 2, dur=1.6, curve=True),
            lab(dp[16][0] + 26, dp[16][1] + 42, "ditch", td + 1.4, GOLD, 28, "start")]
    els += [{"k": "dim", "x1": PX, "y1": PY + 82, "x2": PX, "y2": round(PY + 470 * .88 * .99, 1), "t": "about 400 m", "c": AMBER, "lx": 34, "fx": "draw", "dur": .8, "in": t4}]
    els += [{"k": "scale", "x": 400, "y": 300, "w": 90, "t": "100 m", "in": .8}]
    # the ditch in section: bedrock, a U 4 m wide (30 units = 1 m), a person for scale
    sx, sy = 1360, 470
    els += [rect(sx, sy, 300, 150, "#8d8576", "rgba(255,236,206,.35)", 1.5, 6, tw - .5, fx="pop"),
            poly([(sx + 90, sy), (sx + 96, sy + 44), (sx + 120, sy + 60), (sx + 180, sy + 60), (sx + 204, sy + 44), (sx + 210, sy)], "#2a2019", at=tw - .3),
            {"k": "dim", "x1": sx + 90, "y1": sy - 18, "x2": sx + 210, "y2": sy - 18, "t": "4 m", "c": AMBER, "fx": "draw", "dur": .5, "in": tw},
            person(sx + 255, sy, 51, tw + .2, SKIN), lab(sx + 150, sy + 190, "cut into bedrock", tw + .4, DIM, 24)]
    return {"base": "plan", "cam": CAM, "els": els}


def s19_add():
    """The lower town between citadel and ditch: houses excavated (solid) and inferred (dashed); about 30 hectares; 5,000 to 10,000 people."""
    tl, th, tp = T("s19", "a lower town"), T("s19", "thirty hectares"), T("s19", "five to ten thousand")
    rnd = random.Random(4)
    els = []
    dug = [(-150, 160), (70, 180), (180, 120), (-60, 300), (130, 300)]
    k = 0
    for i in range(90):
        a = rnd.uniform(.12, .88) * math.pi; r = rnd.uniform(.32, .93)
        x, y = PX - 380 * r * math.cos(a), PY + 470 * .88 * r * math.sin(a)
        if math.hypot((x - PX) / 110, (y - PY) / 92) < 1.08 or abs(x - PX) < 30:
            continue
        near = any(math.hypot(x - (PX + dx), y - (PY + dy)) < 70 for dx, dy in dug)
        els.append(rect(x - 11, y - 8, 22, 16, "rgba(232,184,122,.55)" if near else "rgba(232,184,122,.06)", AMBER, 1.5, 2, tl - .2 + .015 * k,
                        style="known" if near else "inferred", fx="pop"))
        k += 1
    els += [lab(PX - 210, PY + 250, "lower town", tl + .4, AMBER, 32), lab(PX + 230, PY + 330, "about 30 hectares", th, BONE, 26)]
    for i in range(100):
        x, y = 150 + 24 * (i % 10), 470 + 24 * (i // 10)
        solid = i < 50
        els.append(circ(x, y, 7, BONE if solid else "none", BONE, 1.5, tp + .006 * i, fx="pop", style="known" if solid else "inferred"))
    els += [lab(258, 450, "5,000 to 10,000", tp + .5, BONE, 26), lab(258, 732, "people", tp + .6, BONE, 26)]
    return els


def mini_plan(cx, cy, at, dense, c=AMBER, s=.85):
    """A small copy of the plan centred at (cx, cy): citadel, ditch, houses (dense or sparse)."""
    pts = [(cx + 100 * s * math.cos(2 * math.pi * k / 30) * (1 + .05 * math.sin(4 * k)), cy + 80 * s * math.sin(2 * math.pi * k / 30)) for k in range(30)]
    dp = [(cx - 380 * s * math.cos(a), cy + 470 * .88 * s * math.sin(a)) for a in [math.pi * (.08 + .84 * k / 24) for k in range(25)]]
    els = [poly(pts, "rgba(214,196,156,.18)", BONE, 2.5, at, curve=True), ln(dp, at + .2, "#1a120c", 9, dur=.9, curve=True)]
    rnd = random.Random(12)
    n = 0
    for i in range(220):
        a = rnd.uniform(.12, .88) * math.pi; r = rnd.uniform(.3, .92)
        x, y = cx - 380 * s * r * math.cos(a), cy + 470 * .88 * s * r * math.sin(a)
        if math.hypot((x - cx) / (100 * s + 10), (y - cy) / (80 * s + 8)) < 1.1:
            continue
        if not dense and i % 9:
            continue
        els.append(rect(x - 7, y - 5, 14, 11, c, "none", 0, 1, at + .4 + .005 * n, fx="pop", op=.85))
        n += 1
    return els, dp, (cx, cy)


def s20():
    """Two readings of one plan: Korfmann's dense town; Kolb's princely seat with a few houses and a water channel; the 2002 debate."""
    tk, tt, tw, tp, td = T("s20", "Frank Kolb"), T("s20", "thinly built"), T("s20", "water channel"), T("s20", "princely seat"), T("s20", "public debate")
    left, _, (lcx, lcy) = mini_plan(440, 300, .4, True)
    right, dp, (rcx, rcy) = mini_plan(1340, 300, tt - .4, False)
    els = left + right + [lab(lcx, 170, "Korfmann", .6, AMBER, 36, st="serif"), lab(rcx, 170, "Kolb", tk, LILAC, 36, st="serif")]
    els += [ln(dp, tw, BLUE, 6, dur=1.0, curve=True)] + [arr([dp[k], dp[k + 1]], tw + .3 + .1 * k, "#bfe6f5", 2.5, dur=.3, curve=False) for k in (4, 10, 16)]
    els += [lab(rcx, 700, "water channel?", tw + .4, BLUE, 28), crown(rcx, rcy - 78, 18, tp), lab(rcx + 64, rcy - 82, "princely seat", tp + .2, LILAC, 26, "start")]
    # the debate, between the two plans
    els += [person(889, 680, 84, td, "#cbbca8"), rect(862, 628, 54, 52, "#3a2c20", "#8a6a48", 1.5, 4, td + .1, fx="pop"),
            person(836, 680, 50, td + .3, "rgba(245,236,220,.6)"), person(942, 680, 50, td + .35, "rgba(245,236,220,.6)")] + chip(889, 540, "2002", AMBER, td + .3, 24)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s21_add():
    """Four specialists answer: 'considerably exaggerated'. Kolb stays unconvinced."""
    tf, tk = T("s21", "Four specialists"), T("s21", "never convinced")
    els = [person(360 + 54 * k, 640, 60, tf + .15 * k, GREEN) for k in range(4)]
    els += chip(440, 700, "considerably exaggerated", GREEN, tf + 1.2, 24)
    els += [person(1520, 380, 70, tk - .3, LILAC), lab(1520, 418, "unconvinced", tk + .2, LILAC, 24)]
    return els


def s22():
    """The Troad: Troy as the hub of its region (even Kolb agrees); two rings, small and large: how big?"""
    v = View(25.85, 26.95, 39.45, 40.3, (90, 120, 1600, 680))
    tx, ty = v.p(26.2389, 39.9575)
    tc, tq = T("s22", "political and military"), T("s22", "size of the")
    rnd = random.Random(21)
    vil = []
    while len(vil) < 14:
        lo, la = rnd.uniform(26.2, 26.75), rnd.uniform(39.62, 40.05)
        if math.hypot(lo - 26.2389, la - 39.9575) < .06:
            continue
        x, y = v.p(lo, la)
        vil.append((x, y))
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for k, (x, y) in enumerate(vil):
        els += [ln([(tx, ty), (x, y)], tc + .05 * k, "rgba(232,184,122,.55)", 1.5, dur=.5), dot(x, y, 6, DIM, tc + .3 + .05 * k)]
    els += [gl(tx, ty, 140, tc, .7, "lamp"), dot(tx, ty, 13, GOLD, .4), lab(tx - 20, ty - 26, "Troy", .5, GOLD, 32, "end", st="serif"),
            lab(*v.p(26.6, 39.68), "the Troad", .8, DIM, 32, st="ital"),
            circ(tx, ty, 26, "none", BONE, 2.5, tq, fx="draw"), circ(tx, ty, 70, "none", AMBER, 2.5, tq + .6, style="inferred"),
            lab(tx + 84, ty + 86, "how big?", tq + 1.0, AMBER, 30, "start"),
            {"k": "scale", "x": 160, "y": 760, "w": round(v.km(10), 1), "t": "10 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · A name in Hittite clay
VA = View(19.5, 37.5, 34.5, 42.6, (90, 120, 1600, 680))


def s23():
    """Anatolia: the Hittite heartland around Hattusa, about 700 km east of Troy."""
    v = VA
    th, tt = T("s23", "Hattusa"), T("s23", "Hittites")
    heart = [(32.4, 41.4), (34.0, 41.9), (35.7, 41.6), (37.0, 40.6), (36.8, 39.2), (35.4, 38.3), (33.6, 38.2), (32.3, 39.0)]
    hx, hy = v.p(34.615, 40.02)
    tx, ty = v.p(26.2389, 39.9575)
    els = [{"k": "map", "land": v.land(), "in": -1},
           poly([v.p(*q) for q in heart], "rgba(232,184,122,.16)", AMBER, 2, tt - .2, curve=True, style="inferred"),
           {"k": "pin", "x": hx, "y": hy, "t": "Hattusa", "c": GOLD, "in": th, "ly": -20},
           lab(*v.p(35.0, 39.0), "the Hittites", tt + .2, AMBER, 34, st="ital"),
           {"k": "pin", "x": tx, "y": ty, "t": "Troy", "c": BONE, "in": .5, "a": "end", "lx": -20},
           ln([(tx + 14, ty), (hx - 14, hy)], th + .6, BONE, 2, "inferred", dur=1.4),
           lab((tx + hx) / 2, ty - 18, "about 700 km", th + 1.6, BONE, 28),
           lab(*v.p(24.6, 38.3), "Aegean", .8, "#9fd0ff", 30, st="ital"),
           {"k": "scale", "x": 160, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def s24():
    """The archive: shelves of clay tablets (about 25,000); one comes forward, and a name glows on it: Wilusa, in the west."""
    ta, tw = T("s24", "twenty-five thousand"), T("s24", "Wilusa")
    els = [gl(640, 420, 620, .1, .3, "lamp")]
    for s in range(3):
        y = 330 + 175 * s
        els += [rect(150, y, 960, 18, WOOD, "#8a6a48", 1.5, 2, .2 + .1 * s)]
        for j in range(19):
            if (s, j) == (1, 9):
                continue
            x = 170 + 49 * j
            h = 70 + (j * 7 + s * 5) % 22
            els += tablet(x, y - h, 38, h, ta - .6 + .02 * (j + 19 * s), "#a8865e" if (j + s) % 3 else "#987654", 5, 3, seed=j + 7 * s)
    els += [lab(630, 760, "about 25,000 tablets", ta + .3, BONE, 30)]
    bx, by = 1300, 230
    els += tablet(bx, by, 250, 320, tw - 2.2, "#b08e64", 10, 6, seed=33) + [rect(bx + 70, by + 150, 110, 34, "none", AU, 3, 4, tw - .4, fx="pop"),
                                                                          gl(bx + 125, by + 167, 90, tw - .4, .6, "lamp")]
    els += [lab(bx + 125, by + 410, "Wilusa", tw, BONE, 56, st="serif"), arr([(bx + 20, by + 470), (bx - 110, by + 470)], tw + .5, AMBER, 4, dur=.5, curve=False),
            lab(bx - 130, by + 478, "west", tw + .8, AMBER, 28, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s25():
    """The name travels: Wilusa, then Wilios with its W glowing, then the W fades and Ilios remains."""
    tw, tv, ti = T("s25", "W sound"), T("s25", "Wilios"), T("s25", "Homer's Ilios")
    y = 480
    els = tablet(250, 200, 160, 150, .3, seed=5) + scroll(1360, 230, 170, 100, ti - .3)
    els += [lab(330, y, "Wilusa", .6, BONE, 64, st="serif"),
            arr([(470, y - 20), (650, y - 20)], tv - .6, AMBER, 4, dur=.5, curve=False),
            lab(850, y, "W", tw, AU, 72, "end", st="serif"), lab(850, y, "ilios", tv - .2, BONE, 64, "start", st="serif"),
            gl(815, y - 24, 70, tw, .6, "lamp"),
            rect(782, y - 64, 70, 82, "none", LILAC, 2.5, 8, ti + .8, style="claimed"), lab(817, y + 64, "the lost W", ti + 1.0, LILAC, 26, st="ital"),
            arr([(1060, y - 20), (1240, y - 20)], ti + .2, AMBER, 4, dur=.5, curve=False),
            lab(1445, y, "Ilios", ti + .5, BONE, 64, st="serif"),
            lab(330, y + 60, "Hittite", .9, DIM, 24), lab(1445, y + 60, "Homer", ti + .7, DIM, 24)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s26():
    """The treaty of Alaksandu (about 1280 BCE), read aloud three times a year; Paris's other name, Alexandros; a century before the fire."""
    ta, t3, tp, tc = T("s26", "Alaksandu", k=1), T("s26", "three times"), T("s26", "Alexandros"), T("s26", "a century before")
    f = 640
    els = [ln([(110, f), (1680, f)], -1, "#8c7152", 3, draw=False), gl(420, 470, 360, .2, .25, "lamp"),
           rect(250, f - 120, 150, 120, WOOD, "#8a6a48", 1.5, 6, .3), rect(250, f - 250, 26, 140, WOOD, "#8a6a48", 1.5, 4, .3)]
    els += seated(320, f, 200, ta - .4, SKIN, stool=False) + [crown(326, f - 160, 14, ta)]
    els += [person(560, f, 180, ta + .4, "#cbbca8"), rect(500, f - 128, 40, 52, "#a8865e", "#e9dccb", 1.5, 5, ta + .6, fx="pop")]
    els += [ln([(486 - 22 * k, f - 128 - 10 * k), (470 - 30 * k, f - 100), (486 - 22 * k, f - 72 + 10 * k)], t3 - .6 + .2 * k, AMBER, 2.5, dur=.3, curve=True) for k in range(3)]
    els += [lab(330, f + 44, "Alaksandu", ta + .2, BONE, 34, st="serif")]
    cx, cy, r = 990, 360, 120
    els += [circ(cx, cy, r, "none", "#8c7152", 4, t3 - .5, fx="draw")]
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        els.append(ln([(cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a)), (cx + (r + 8) * math.cos(a), cy + (r + 8) * math.sin(a))], t3 - .4, "#8c7152", 2, draw=False))
    for k, a in enumerate((-math.pi / 2, math.pi / 6, 5 * math.pi / 6)):
        els += [gl(cx + r * math.cos(a), cy + r * math.sin(a), 46, t3 + .3 * k, .8, "lamp"), dot(round(cx + r * math.cos(a), 1), round(cy + r * math.sin(a), 1), 15, AU, round(t3 + .3 * k, 2))]
    els += [lab(cx, cy + 10, "1 year", t3 - .3, DIM, 26), lab(cx, cy + r + 54, "3 times a year", t3 + 1.0, AU, 30)]
    els += [person(1460, f, 170, tp - .2, LILAC), lab(1460, f + 44, "Alexandros", tp + .2, LILAC, 34, st="serif"),
            ln([(430, f + 30), (900, f + 62), (1350, f + 30)], tp + .5, LILAC, 2.5, "claimed", dur=1.0, curve=True)]
    y2 = 760
    els += [ln([(560, y2), (1240, y2)], tc, DIM, 2, dur=.6), dot(560, y2, 8, BONE, tc), lab(560, y2 - 16, "about 1280 BCE", tc + .1, BONE, 24)] + \
        flame(1240, y2 + 6, 26, tc + .5) + [lab(1240, y2 - 32, "fire, about 1180", tc + .6, FIRE, 24), lab(900, y2 - 16, "a century", tc + .9, AMBER, 24)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s27():
    """The treaty's divine witnesses: Appaliuna (Apollo?) and the underground watercourse of the land of Wilusa light up as named."""
    ta, tp, tu = T("s27", "Appaliuna"), T("s27", "early Apollo"), T("s27", "underground watercourse")
    tx, ty, tw, th = 230, 170, 560, 560
    els = [gl(510, 450, 520, .1, .25, "lamp"), rect(tx, ty, tw, th, "#b08e64", "#e9dccb", 2, 26, .2),
           {"k": "glyphs", "x": tx + 50, "y": ty + 40, "w": tw - 100, "h": 330, "rows": 11, "cols": 9, "kind": "cuneiform", "c": "#4a3522", "seed": 4, "in": .3}]
    gy = ty + th - 90
    icons = []
    for k in range(6):
        x = tx + 70 + 84 * k
        icons.append((x, gy))
        els.append(circ(x, gy, 32, "rgba(74,53,34,.18)", "#4a3522", 2, .5 + .05 * k))
    (x0, _), (x1, _), (x2, _), (x3, _), (x4, _), (x5, _) = icons
    els += [circ(x0, gy, 12, "none", "#4a3522", 3, .6), ln([(x1 - 14, gy + 10), (x1 - 2, gy - 12), (x1 + 4, gy), (x1 + 14, gy - 14)], .6, "#4a3522", 3, draw=False),
            ln([(x2 - 10, gy - 18), (x2 + 8, gy), (x2 - 10, gy + 18)], .6, "#4a3522", 3, draw=False, curve=True), ln([(x2 - 10, gy - 18), (x2 - 10, gy + 18)], .6, "#4a3522", 2, draw=False),
            poly([(x3 - 16, gy + 14), (x3, gy - 16), (x3 + 16, gy + 14)], "none", "#4a3522", 3, .6),
            ln([(x4 - 18, gy - 6), (x4 - 9, gy - 12), (x4, gy - 6), (x4 + 9, gy - 12), (x4 + 18, gy - 6)], .6, "#4a3522", 3, draw=False, curve=True),
            ln([(x4 - 18, gy + 6), (x4 - 9, gy), (x4, gy + 6), (x4 + 9, gy), (x4 + 18, gy + 6)], .6, "#4a3522", 3, draw=False, curve=True),
            poly([(x5, gy - 16), (x5 + 5, gy - 5), (x5 + 16, gy - 4), (x5 + 7, gy + 4), (x5 + 10, gy + 15), (x5, gy + 8), (x5 - 10, gy + 15), (x5 - 7, gy + 4),
                  (x5 - 16, gy - 4), (x5 - 5, gy - 5)], "none", "#4a3522", 2.5, .6)]
    els += [gl(x2, gy, 70, ta, .9, "lamp"), circ(x2, gy, 34, "none", AU, 4, ta, fx="draw", dur=.5),
            arr([(x2 + 10, gy - 40), (900, 300), (980, 290)], ta + .3, AU, 3, dur=.7), lab(1000, 300, "Appaliuna", ta + .6, AU, 40, "start", st="serif"),
            arr([(1290, 290), (1380, 290)], tp, LILAC, 3, "claimed", .5, False), lab(1400, 300, "Apollo?", tp + .3, LILAC, 40, "start", st="ital")]
    els += [gl(x4, gy, 70, tu, .9, "glowb"), circ(x4, gy, 34, "none", BLUE, 4, tu, fx="draw", dur=.5),
            arr([(x4 + 20, gy + 30), (900, 560), (980, 540)], tu + .3, BLUE, 3, dur=.7), lab(1000, 552, "underground watercourse", tu + .6, BLUE, 34, "start")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s28():
    """Troy's spring cave in section: tunnels cut in the rock, four shafts, water; over 100 m; a crust of minerals older than the treaty."""
    tt, t1, tc = T("s28", "tunnels cut"), T("s28", "more than a hundred"), T("s28", "already centuries old")
    g = 300
    surface = [(-20, g + 4), (240, g - 2), (330, g + 70), (360, g + 92), (420, g + 98), (560, g + 40), (760, g + 14), (1100, g + 4), (1500, g - 6), (1800, g)]

    def sy(x):
        for (x0, y0), (x1, y1) in zip(surface, surface[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return g
    els = [poly(surface + [(1800, 1010), (-20, 1010)], "#8d8170", "rgba(255,236,206,.5)", 2, -1)]
    els += [ln([(-20, g + 150 + 70 * k + 10 * math.sin(k)), (1800, g + 160 + 70 * k)], -1, "rgba(60,50,40,.35)", 2, "inferred", draw=False) for k in range(6)]
    els += [person(392, g + 96, 24, .4, SKIN), gl(392, g + 80, 50, .5, .6, "lamp")]
    main = [(420, g + 100), (700, g + 150), (1000, g + 180), (1300, g + 200), (1500, g + 205)]
    els += [ln(main, tt, "#1e1813", 30, dur=1.6, curve=True), ln([(900, g + 170), (1100, g + 250), (1300, g + 280)], tt + .8, "#1e1813", 22, dur=1.0, curve=True),
            ln([(820, g + 165), (1000, g + 110), (1180, g + 105)], tt + 1.0, "#1e1813", 18, dur=1.0, curve=True),
            ln(main, tt + 1.4, "#5fa8c9", 3, dur=1.6, curve=True, op=.8)]
    for k, x in enumerate((640, 900, 1150, 1380)):
        els.append(ln([(x, sy(x) + 1), (x, g + 140 + 20 * k)], tt + 1.6 + .2 * k, "#1e1813", 10, dur=.4))
    els += [{"k": "dim", "x1": 420, "y1": g + 300, "x2": 1500, "y2": g + 300, "t": "over 100 m", "c": AMBER, "ly": 36, "fx": "draw", "dur": .9, "in": t1},
            lab(380, g - 40, "spring cave", .6, BONE, 30), lab(1010, g - 40, "4 shafts", tt + 2.0, DIM, 26)]
    # a magnifier on the tunnel wall: the mineral crust, layer on layer
    mx, my, mr = 1610, 640, 84
    els += [circ(mx, my, mr, "#2a221a", AU, 3, tc - .2, fx="pop")]
    for k in range(7):
        q = [(-80 + 6 * k, 60 - 12 * k), (-20, 40 - 14 * k), (50, 50 - 16 * k), (80 - 4 * k, 30 - 14 * k)]
        els.append(ln([(mx + .74 * a, my + .74 * b) for a, b in q], tc + .1 * k, ["#e8dcc2", "#c9b28a"][k % 2], 6, dur=.3, curve=True))
    els += [ln([(1502, g + 214), (1556, my - 64)], tc, AU, 2, "inferred", dur=.5), lab(mx + mr, my + mr + 36, "older than the treaty", tc + .6, AU, 26, "end")]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def s29_add():
    """Ahhiyawa: a western power, most likely the Mycenaean Greeks (Homer's Achaeans); a letter crosses the Aegean."""
    v = VA
    ta, tm, tc = T("s29", "Ahhiyawa"), T("s29", "Mycenaean Greeks"), T("s29", "Achaeans")
    greece = [(21.2, 38.6), (22.6, 39.8), (24.0, 40.2), (24.4, 39.0), (23.9, 38.0), (23.2, 36.5), (22.4, 36.4), (21.6, 37.1), (21.1, 37.8)]
    hx, hy = v.p(34.615, 40.02)
    mx, my = v.p(22.756, 37.731)
    gx, gy = v.p(22.6, 38.6)
    return [poly([v.p(*q) for q in greece], "rgba(201,193,238,.12)", LILAC, 2.5, ta, curve=True, style="claimed"),
            lab(gx, gy - 70, "Ahhiyawa", ta + .3, LILAC, 34, st="ital"),
            {"k": "pin", "x": mx, "y": my, "t": "Mycenae", "c": LILAC, "in": tm, "a": "end", "lx": -18},
            lab(gx, gy - 36, "Achaeans?", tc, LILAC, 26),
            arr([(hx - 14, hy + 16), ((hx + gx) / 2 + 60, 470), (gx + 60, gy - 20)], ta + .4, AMBER, 3, "inferred", 1.6)] + \
        tablet((hx + gx) / 2 + 40, 446, 36, 44, ta + 1.2, seed=3)


def s30():
    """A Hittite king writes to the king of Ahhiyawa, 'my brother', about Wilusa: once hostile, now at peace."""
    tb, tw, th, tp = T("s30", "brother"), T("s30", "matter of"), T("s30", "hostile"), T("s30", "made peace")
    f = 620
    els = [ln([(110, f), (1680, f)], -1, "#8c7152", 3, draw=False), gl(889, 420, 600, .1, .2, "lamp")]
    els += [person(330, f, 200, .3, "#cbbca8"), crown(330, f - 192, 16, .5), lab(330, f + 44, "Hittite king", .7, BONE, 28),
            person(1450, f, 200, .5, LILAC), crown(1450, f - 192, 16, .7, LILAC), lab(1450, f + 44, "king of Ahhiyawa", .9, LILAC, 28)]
    els += chip(889, 175, "about 1250 BCE", AMBER, .8, 26)
    els += [arr([(440, 300), (889, 250), (1340, 300)], tb - .8, AMBER, 3, dur=1.2)] + tablet(855, 210, 68, 80, tb - .4, seed=8) + \
           [lab(889, 330, "brother", tb + .2, AU, 34, st="ital")]
    els += [lab(889, 590, "Wilusa", tw, BONE, 48, st="serif")]
    sx = 760
    els += [ln([(sx - 60, 400), (sx + 60, 500)], th, RED, 5, dur=.3), ln([(sx + 60, 400), (sx - 60, 500)], th + .15, RED, 5, dur=.3),
            poly([(sx - 72, 392), (sx - 54, 386), (sx - 58, 404)], RED, at=th + .1), poly([(sx + 72, 392), (sx + 54, 386), (sx + 58, 404)], RED, at=th + .25),
            arr([(840, 450), (930, 450)], tp - .3, DIM, 3, dur=.4, curve=False)]
    ox = 1020
    els += [ln([(ox - 70, 480), (ox, 450), (ox + 70, 420)], tp, GREEN, 4, dur=.5, curve=True)]
    for k in range(5):
        x = ox - 50 + 26 * k; y = 472 - 13 * k
        els += [poly(E(x, y - 12, 7, 14, 12), GREEN, at=tp + .3 + .08 * k, fx="pop"), poly(E(x + 8, y + 10, 7, 14, 12), GREEN, at=tp + .35 + .08 * k, fx="pop")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s31():
    """'Hostile' splits: angry letters, or war; the letter does not say. A magnifier crosses the tablets: no attack on record."""
    th, tw, tn = T("s31", "angry letters"), T("s31", "or war"), T("s31", "no Hittite text")
    els = [gl(889, 360, 520, .1, .2, "lamp"), lab(889, 190, "hostile", .4, RED, 44, st="ital"),
           arr([(820, 220), (560, 300)], th - .3, DIM, 2.5, "inferred", .5), arr([(960, 220), (1220, 300)], tw - .3, DIM, 2.5, "inferred", .5)]
    for k in range(4):
        els += tablet(430 + 18 * k, 320 - 10 * k, 120, 150, th + .1 * k, seed=20 + k, op=.9) + [ln([(450 + 18 * k, 360 - 10 * k), (530 + 18 * k, 400 - 10 * k)], th + .2 + .1 * k, RED, 3, dur=.2)]
    els += [lab(520, 540, "angry letters", th + .5, BONE, 28)]
    els += [ln([(1150, 470), (1300, 320)], tw, "#d8dce0", 6, dur=.3), ln([(1300, 470), (1150, 320)], tw + .15, "#d8dce0", 6, dur=.3),
            rect(1140, 455, 30, 10, BRONZE, at=tw + .1), rect(1280, 455, 30, 10, BRONZE, at=tw + .25), lab(1225, 540, "war", tw + .4, BONE, 28)]
    els += qmark(889, 430, tw + .6, 90)
    for k in range(9):
        els += tablet(330 + 128 * k, 620, 64, 80, tn - .6 + .04 * k, "#987654", 5, 3, seed=40 + k, op=.85)
    els += [circ(330, 662, 52, "rgba(159,208,255,.08)", BLUE, 3, tn, fx="pop"), ln([(368, 700), (410, 742)], tn, BLUE, 6, draw=False),
            ln([(330, 662), (1400, 662)], tn + .3, "rgba(159,208,255,.3)", 2, "inferred", dur=2.0),
            lab(889, 770, "no attack on record", tn + 2.0, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s32():
    """A later letter: Walmu, king of Wilusa, driven out; the Hittite king wants him back on his throne."""
    tl, tw, tb = T("s32", "a later letter"), T("s32", "Walmu"), T("s32", "back on his")
    f = 640
    tx = 1080
    els = [ln([(110, f), (1680, f)], -1, "#8c7152", 3, draw=False), gl(tx, 460, 360, .1, .25, "lamp")]
    # a throne in side view: legs, seat, high back, an armrest
    els += [rect(tx - 90, f - 150, 14, 150, WOOD, "#8a6a48", 1.5, 3, .3), rect(tx + 70, f - 150, 14, 150, WOOD, "#8a6a48", 1.5, 3, .3),
            rect(tx - 100, f - 170, 200, 30, WOOD, "#c9a46a", 2, 6, .3), rect(tx + 70, f - 400, 34, 260, WOOD, "#c9a46a", 2, 8, .3),
            rect(tx - 100, f - 240, 30, 74, WOOD_D, "#8a6a48", 1.5, 4, .3), rect(tx - 104, f - 250, 120, 16, WOOD, "#c9a46a", 1.5, 6, .3),
            circ(tx + 87, f - 412, 16, AU, at=.35), lab(tx, f + 44, "Wilusa's throne", .6, DIM, 26)]
    els += [crown(tx - 10, f - 280, 24, tw - .4, GOLD), ln([(tx - 10, f - 300), (tx - 40, f - 340)], tw - .3, GOLD, 2, "inferred", dur=.3)]
    els += tablet(240, 180, 90, 110, tl - .2, seed=12) + [lab(285, 330, "a later letter", tl + .2, BONE, 26)]
    els += [person(560, f, 180, tw - .2, SKIN), lab(560, f + 44, "Walmu", tw + .2, BONE, 34, st="serif"),
            arr([(640, f - 230), (840, f - 320), (980, f - 220)], tb, AMBER, 3.5, "inferred", 1.0),
            lab(820, f - 350, "back on the throne?", tb + .5, AMBER, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s33_add():
    """In the archive, an empty slot: if a Trojan War was written down, it has not been found."""
    tn = T("s33", "hasn't been found")
    x, y = 170 + 49 * 9, 330 + 175 * 1
    return [rect(x - 6, y - 104, 50, 100, "rgba(201,193,238,.12)", LILAC, 2.5, 6, tn - 1.2, style="claimed")] + qmark(x + 19, y - 30, tn - .8, 56) + \
        [lab(x + 19, y + 60, "not found", tn, LILAC, 28)]


# ================================================================== CHAPTER 4 · What Homer remembered
def XH(yr):
    return round(160 + (1620 - 160) * (yr + 1300) / 700, 1)


def s34():
    """From the fire (about 1180 BCE) to the Iliad (about 700 BCE): almost 500 years, most of them without writing in Greece."""
    tf, ti, t5, tw = T("s34", "Troy Seven A"), T("s34", "The Iliad"), T("s34", "almost five hundred"), T("s34", "without writing")
    y = 640
    ticks = [[XH(v), t] for v, t in ((-1300, "1300 BCE"), (-1100, "1100"), (-900, "900"), (-700, "700"))]
    els = [axis(160, 1620, y, ticks, .2)]
    els += flame(XH(-1180), y - 40, 50, tf - .4) + [lab(XH(-1180), y - 120, "Troy VIIa burns", tf, FIRE, 28)]
    els += scroll(XH(-700) - 60, y - 96, 120, 56, ti - .2) + [lab(XH(-700), y - 130, "the Iliad", ti + .2, GOLD, 30)]
    els += bracket(XH(-1180), XH(-700), 400, t5, None, BONE, up=False) + [lab((XH(-1180) + XH(-700)) / 2, 380, "almost 500 years", t5 + .3, BONE, 30)]
    els += [{"k": "band", "x0": XH(-1200), "x1": XH(-800), "y": 250, "h": 18, "c": LILAC, "t": "no writing in Greece", "tc": LILAC, "in": tw, "op": .8}]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def gusle(x, y, s, at, c="#8a5a36"):
    """A one-string fiddle held upright: a pear-shaped body, a long neck, a carved head."""
    return [poly(E(x, y, 26 * s, 40 * s, 24), c, "#d8b88a", 1.5, at, fx="pop"), rect(x - 5 * s, y - 130 * s, 10 * s, 96 * s, c, "#d8b88a", 1.2, 3, at),
            poly(E(x, y - 140 * s, 12 * s, 14 * s, 14), c, "#d8b88a", 1.2, at), ln([(x, y - 128 * s), (x, y + 30 * s)], at, "#efe3c8", 1.2, draw=False)]


def s35():
    """Avdo Medjedovic sings with his gusle; Milman Parry records; his song (12,311 lines) stacks as high as the Odyssey."""
    ta, tp, t12, to = T("s35", "Avdo"), T("s35", "Milman Parry"), T("s35", "twelve thousand"), T("s35", "Odyssey")
    f = 640
    els = [ln([(110, f), (1680, f)], -1, "#8c7152", 3, draw=False), gl(520, 440, 420, .1, .3, "lamp")]
    els += seated(470, f, 210, ta - .5, SKIN) + gusle(560, f - 110, 1.0, ta - .3) + [ln([(520, f - 150), (640, f - 60)], ta, "#d8c8a8", 2.5, draw=False)]
    els += [lab(470, f + 44, "Avdo Medjedovic", ta + .3, BONE, 30)]
    els += [rect(760, f - 120, 220, 120, WOOD, "#8a6a48", 2, 4, tp - 1.0), rect(790, f - 190, 150, 70, "#3a3530", "#a8a090", 2, 6, tp - .8),
            poly(E(865, f - 196, 60, 12, 24), "#1a1714", "#8a8478", 1.5, tp - .7), circ(865, f - 196, 5, GOLD, at=tp - .6),
            person(1040, f, 176, tp - .4, "#cbbca8"), lab(1040, f + 44, "Milman Parry", tp + .2, BONE, 30), lab(865, f - 230, "1930s", tp + .4, AMBER, 26)]
    for j, (x, t_) in enumerate(((1250, t12), (1470, to))):
        for k in range(14):
            els.append(rect(x, f - 22 * (k + 1), 150, 20, "#efe6d2" if j == 0 else "#e2d6b8", "#8a7a66", 1, 2, t_ + .05 * k, fx="pop"))
    els += [lab(1325, f + 40, "his song", t12 + .5, BONE, 26), lab(1325, f + 72, "12,311 lines", t12 + .7, AU, 26),
            lab(1545, f + 40, "the Odyssey", to + .4, BONE, 26, st="lab"), lab(1545, f + 72, "about 12,100", to + .6, DIM, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s36():
    """Formulas as bricks: a wall builds itself, three bricks carry stock phrases."""
    tb = T("s36", "ready-made phrases")
    rows, y0, bh = 7, 690, 62
    text = {(1, 1): "swift-footed Achilles", (3, 2): "rosy-fingered Dawn", (5, 1): "wine-dark sea"}
    els = [gl(889, 420, 600, .1, .25, "lamp"), ln([(260, y0 + 4), (1520, y0 + 4)], .1, "#6a5a48", 3, draw=False)]
    k = 0
    for r in range(rows):
        x = 280 + (60 if r % 2 else 0)
        j = 0
        while x < 1480:
            w = 360 if (r, j) in text else 150
            if x + w > 1500:
                break
            t = text.get((r, j))
            at = tb - .6 + .03 * k
            els.append(rect(x, y0 - bh * (r + 1), w - 8, bh - 8, "#9a5f3c" if not t else "#b4744a", GOLD if t else "#5a3624", 2.5 if t else 1.5, 4, at, fx="pop"))
            if t:
                els.append(lab(x + (w - 8) / 2, y0 - bh * (r + 1) + 38, t, at + .2, "#fff4dc", 26, st="ital"))
            x += w; j += 1; k += 1
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def helmet(cx, top, H, at, plate="#efe6d2", body="#6b4a2e", rim="#c9a46a", step=.02):
    """A boar's tusk helmet: a cone of rows of curved tusk plates laid flat, curving one way in one row and the other way in the next,
    cheek pieces, a knob on top."""
    els = [poly([(cx - .48 * H, top + .95 * H), (cx - .5 * H, top + .55 * H), (cx - .36 * H, top + .2 * H), (cx, top + .02 * H), (cx + .36 * H, top + .2 * H),
                 (cx + .5 * H, top + .55 * H), (cx + .48 * H, top + .95 * H)], body, rim, 2, at, curve=True)]
    for r in range(5):
        yr = top + (.27 + .15 * r) * H
        half = (.24 + .06 * r) * H
        n = 4 + r
        d = -1 if r % 2 else 1
        w = 2 * half / n
        for j in range(n):
            x0 = cx - half + w * j + w * .06
            x1 = x0 + w * .88
            hh = .045 * H
            arc_top = [(x0 + (x1 - x0) * t, yr - d * hh * math.sin(math.pi * t)) for t in [k / 8 for k in range(9)]]
            arc_bot = [(x0 + (x1 - x0) * t, yr + .05 * H - d * hh * .55 * math.sin(math.pi * t)) for t in [k / 8 for k in range(9)]][::-1]
            els.append(poly(arc_top + arc_bot, plate, "#8a7a66", 1, at + .3 + .08 * r + step * j, fx="pop"))
    for side in (-1, 1):
        els.append(poly([(cx + side * .44 * H, top + .9 * H), (cx + side * .5 * H, top + 1.25 * H), (cx + side * .34 * H, top + 1.3 * H), (cx + side * .3 * H, top + .95 * H)],
                        body, rim, 1.5, at + .9))
    els += [circ(cx, top + .02 * H, .05 * H, rim, at=at + .9), ln([(cx, top - .02 * H), (cx, top - .12 * H)], at + .9, rim, 3, draw=False)]
    return els


def boar(x, y, s, at, c="#cbbca8"):
    return [poly([(x - 16 * s, y), (x - 18 * s, y - 9 * s), (x - 10 * s, y - 15 * s), (x + 8 * s, y - 15 * s), (x + 16 * s, y - 10 * s), (x + 22 * s, y - 6 * s),
                  (x + 18 * s, y - 2 * s), (x + 12 * s, y), (x + 10 * s, y + 6 * s), (x + 6 * s, y + 6 * s), (x + 4 * s, y), (x - 8 * s, y), (x - 10 * s, y + 6 * s),
                  (x - 14 * s, y + 6 * s)], c, at=at, fx="pop"),
            ln([(x + 17 * s, y - 4 * s), (x + 21 * s, y - 11 * s)], at, "#fff4dc", 1.6, draw=False)]


def s37():
    """A boar's tusk helmet (a Bronze Age type that vanished around the time Troy burned); each needed the tusks of 40 to 50 boars."""
    th, tb, t40 = T("s37", "helmet covered"), T("s37", "Bronze Age type"), T("s37", "forty or fifty")
    els = [gl(560, 420, 420, .1, .35, "lamp")] + helmet(560, 190, 380, th - .5) + [lab(560, 730, "boar's tusk helmet", th + .5, BONE, 30)]
    els += chip(560, 140, "in use about 1700 to 1150 BCE", AMBER, tb + .4, 24)
    for k in range(45):
        x, y = 1000 + 66 * (k % 9), 260 + 74 * (k // 9)
        els += boar(x, y, 1.2, t40 - .5 + .04 * k)
    els += [lab(1265, 680, "40 to 50 boars", t40 + 1.4, AU, 32)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s38():
    """The Catalogue of Ships: 1,186 ships from the coasts of Greece; Eutresis, named in it, lay empty in Homer's day."""
    v = View(19.6, 28.6, 35.0, 40.9, (90, 120, 1600, 680))
    ts, te, td = T("s38", "more than a thousand"), T("s38", "Eutresis"), T("s38", "lay empty")
    spots = [(22.9, 40.6), (22.6, 39.6), (23.2, 38.9), (23.9, 38.4), (23.5, 38.2), (23.8, 37.9), (23.5, 37.8), (22.8, 37.6), (22.4, 36.8), (21.7, 36.9),
             (21.4, 37.6), (21.3, 38.3), (20.7, 38.4), (21.0, 38.9), (24.3, 37.5), (24.9, 37.2), (25.3, 35.3), (24.4, 35.3), (25.8, 35.2), (27.9, 36.3),
             (26.9, 36.6), (27.2, 36.9), (26.1, 39.4), (24.6, 38.6), (22.1, 37.9), (21.9, 38.6), (23.0, 39.2), (22.0, 39.3), (20.3, 39.5)]
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for k, (lo, la) in enumerate(spots):
        x, y = v.p(lo, la)
        els += galley(x, y + 6, 42, ts - .4 + .07 * k, "#efe3c8", -1)
    ex, ey = v.p(23.183, 38.267)
    lx, ly = 560, 560                                        # the labels sit in the open Ionian Sea, tied to Eutresis by a leader
    els += [lab(1440, 230, "1,186 ships", ts + 2.0, BONE, 36, st="serif"),
            gl(ex, ey, 40, te, .6, "lamp"), dot(ex, ey, 9, LILAC, te), ln([(ex - 8, ey + 6), (lx + 14, ly - 14)], te + .1, LILAC, 1.5, dur=.4),
            lab(lx, ly, "Eutresis", te + .2, LILAC, 30, "end", st="serif"),
            lab(lx, ly + 34, "empty in Homer's day", td, LILAC, 26, "end", st="ital"),
            {"k": "scale", "x": 160, "y": 760, "w": round(v.km(100), 1), "t": "100 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def s39():
    """Homer's Troy in his own words: a gold-line city on its hill, well-walled, with a wide street to its gate, and windy."""
    tw, ts, ty = T("s39", "fine walls"), T("s39", "wide streets"), T("s39", "strong winds")
    els = [gl(889, 430, 560, .1, .25, "lamp"),
           poly([(300, 640), (420, 560), (600, 500), (1180, 500), (1360, 560), (1480, 640)], "rgba(242,201,142,.06)", GOLD, 2.5, .2, curve=True)]
    els += walled_city(560, 1220, 500, 380, tw - .5, AU, "known", "rgba(232,195,90,.08)", 3)
    els += [ln([(840, 640), (866, 500)], ts - .2, AU, 3, dur=.5), ln([(940, 640), (914, 500)], ts - .2, AU, 3, dur=.5)]
    els += [ln([(820 + 22 * k, 600 - 8 * k), (960 - 22 * k, 600 - 8 * k)], ts + .2 + .1 * k, "rgba(232,195,90,.5)", 1.5, draw=False) for k in range(4)]
    for k in range(6):
        y = 240 + 70 * k
        els.append(ln([(140, y), (480, y - 26), (900, y + 8), (1300, y - 18), (1660, y)], ty - .2 + .12 * k, "rgba(245,236,220,.35)", 2, dur=1.4, curve=True))
    els += [lab(450, 340, "well-walled", tw, LILAC, 40, st="ital"), lab(1300, 700, "wide streets", ts, LILAC, 40, st="ital"),
            lab(1380, 300, "windy", ty, LILAC, 40, st="ital")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def horse(x, y, s, at, c="#d9c7a6", face=1):
    f = face
    X = lambda a: x + f * a * s
    body = [(X(-42), y - 50 * s), (X(-10), y - 56 * s), (X(18), y - 56 * s), (X(30), y - 66 * s), (X(40), y - 86 * s), (X(52), y - 96 * s), (X(62), y - 92 * s),
            (X(66), y - 82 * s), (X(56), y - 78 * s), (X(46), y - 64 * s), (X(36), y - 46 * s), (X(30), y - 34 * s), (X(28), y), (X(22), y), (X(19), y - 32 * s),
            (X(-22), y - 34 * s), (X(-24), y), (X(-30), y), (X(-34), y - 38 * s), (X(-44), y - 40 * s), (X(-56), y - 24 * s), (X(-52), y - 44 * s)]
    return [poly(body, c, "rgba(30,20,12,.5)", 1, at, fx="rise", curve=True)]


def s40():
    """Homer's chariot: drive to the fight, step down, fight on foot; behind, faint, the massed chariots of the Bronze Age."""
    tc, ts, tf = T("s40", "ride a chariot"), T("s40", "step down"), T("s40", "fight on")
    g = 640
    els = []
    for k in range(4):
        x0 = 300 + 330 * k
        els += [poly([(x0 - 34, g - 150), (x0 + 30, g - 150), (x0 + 34, g - 116), (x0 - 30, g - 116)], "none", GOLD, 1.5, .4 + .1 * k, op=.45, style="inferred"),
                circ(x0, g - 110, 22, "none", GOLD, 1.5, .4 + .1 * k, op=.45, style="inferred")] + \
               [e | {"op": .3, "keepop": True, "fill": "none", "c": GOLD, "w": 1.5, "style": "inferred"} for e in horse(x0 - 90, g - 88, .8, .4 + .1 * k)]
    els += horse(420, g, 1.6, tc - .4) + horse(450, g + 6, 1.6, tc - .3, "#c9b28e")
    els += [ln([(450 + 48, g - 150), (600, g - 100)], tc - .2, "#8a6a48", 4, draw=False),
            poly([(600, g - 60), (600, g - 120), (690, g - 120), (700, g - 60)], WOOD, "#d8b88a", 2, tc - .2),
            circ(650, g - 30, 34, "none", "#d8b88a", 4, tc - .1, fx="pop")] + \
           [ln([(650, g - 30), (650 + 34 * math.cos(a), g - 30 + 34 * math.sin(a))], tc - .1, "#d8b88a", 2, draw=False) for a in [k * math.pi / 3 for k in range(6)]]
    els += [person(660, g - 60, 96, tc, "#cbbca8"), lab(640, g + 50, "chariot", tc + .4, BONE, 28)]
    els += warrior(1120, g, 180, ts, 1, "#e8d6b8", "#7a5a3a") + [lab(1160, g + 50, "fights on foot", tf + .2, BONE, 28)]
    els += [arr([(760, g - 200), (1000, g - 220)], ts + .2, AMBER, 3, "inferred", .8)]
    return {"base": "sky", "tod": "dusk", "ground": g, "sun": [1450, 380, 26], "cam": CAM, "els": els}


def s41():
    """Homer's world prizes iron; and the Hittite empire next door is missing from the poem."""
    ti, th = T("s41", "prize iron"), T("s41", "the superpower")
    v = View(25.5, 41.5, 35.2, 42.6, (900, 200, 760, 420))
    heart = [(32.4, 41.4), (34.0, 41.9), (35.7, 41.6), (37.0, 40.6), (36.8, 39.2), (35.4, 38.3), (33.6, 38.2), (32.3, 39.0)]
    els = [gl(450, 470, 300, .1, .25, "lamp"),
           rect(330, 560, 240, 80, WOOD, "#c9a46a", 2, 6, ti - .5), rect(310, 548, 280, 16, "#8a6a48", "#c9a46a", 1.5, 4, ti - .5),
           poly([(372, 548), (392, 500), (440, 478), (500, 486), (532, 512), (526, 548)], IRON, "#b0aca4", 2, ti, fx="pop", curve=True),
           poly([(410, 512), (450, 498), (480, 506)], "none", "rgba(255,255,255,.35)", 2, ti + .1),
           gl(452, 512, 140, ti + .2, .6, "lamp"), lab(450, 700, "iron, a prize", ti + .4, BONE, 30)]
    els += [rect(900, 200, 760, 420, "#1d3a4a", "rgba(255,236,206,.2)", 2, 16, th - .7),
            {"k": "group", "clip": [900, 200, 760, 420, 16], "in": th - .6, "els": [{"k": "map", "land": v.land(), "landc": "#3a2f24"}]},
            poly([v.p(*q) for q in heart], "rgba(201,193,238,.08)", LILAC, 2.5, th, curve=True, style="claimed"),
            lab(*v.p(34.6, 40.0), "the Hittites", th + .3, LILAC, 30, st="ital"),
            lab(1280, 700, "not in the poem", th + .8, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s42():
    """The Iliad as a chest of heirlooms: Bronze Age pieces (gold outlines) and Homer's own (lilac)."""
    tc, tb, to = T("s42", "chest of"), T("s42", "Bronze Age"), T("s42", "added on")
    els = [gl(889, 450, 560, .1, .3, "lamp"),
           poly([(540, 470), (1240, 470), (1270, 250), (570, 250)], WOOD_D, "#a87a52", 2, tc - .3),
           rect(520, 470, 740, 230, WOOD, "#a87a52", 2.5, 8, tc - .4), rect(520, 520, 740, 14, "#8a6a48", at=tc - .3), rect(860, 480, 60, 50, GOLD, "#7a5a1a", 1.5, 6, tc - .2)]
    els += helmet(660, 290, 130, tb, "rgba(242,201,142,.9)", "rgba(242,201,142,.12)", GOLD, .01) + galley(830, 446, 140, tb + .3, GOLD, -1)
    els += [poly([(985, 446), (1005, 404), (1052, 392), (1090, 410), (1086, 446)], "rgba(201,193,238,.2)", LILAC, 2.5, to, fx="pop", curve=True, style="claimed")]
    cx = 1175
    els += [circ(cx, 428, 30, "none", LILAC, 2.5, to + .2, style="claimed"), poly([(cx - 40, 400), (cx + 34, 400), (cx + 34, 362), (cx - 30, 362)], "none", LILAC, 2.5, to + .2, style="claimed")] + \
           [ln([(cx, 428), (cx + 30 * math.cos(a), 428 + 30 * math.sin(a))], to + .2, LILAC, 1.5, draw=False) for a in [k * math.pi / 3 for k in range(6)]]
    els += [lab(740, 760, "Bronze Age", tb + .4, GOLD, 30), lab(1080, 760, "Homer's own", to + .4, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · The fire and the fall
def s43():
    """About 1300 BCE: an earthquake shakes Troy VI apart (cracks, fallen blocks, a seismograph); Troy VIIa rebuilt, crowded."""
    te, tr = T("s43", "earthquake"), T("s43", "rebuilt")
    g = 660
    els = [ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False),
           poly([(160, g), (330, g), (330, g - 230), (200, g - 230)], "url(#k-blocks)", "rgba(255,236,206,.5)", 1.5, .2),
           rect(470, g - 200, 260, 200, "#b8a57c", "rgba(255,236,206,.5)", 1.5, 2, .3), rect(790, g - 170, 240, 170, "#b8a57c", "rgba(255,236,206,.5)", 1.5, 2, .4)]
    seis = [(140 + 12 * k, 210 + (math.sin(k * 1.7) * (4 + 34 * max(0, 1 - abs(k - 40) / 26)))) for k in range(110)]
    els += [ln(seis, te - .8, AMBER, 2.5, dur=1.8)]
    els += [ln([(250, g - 230), (236, g - 170), (262, g - 120), (240, g - 60), (256, g)], te, RED, 3, dur=.5),
            ln([(560, g - 200), (590, g - 140), (566, g - 90), (600, g - 30)], te + .2, RED, 3, dur=.5),
            ln([(900, g - 170), (884, g - 110), (912, g - 60)], te + .35, RED, 3, dur=.5)]
    rnd = random.Random(6)
    for k in range(9):
        x = rnd.uniform(340, 1040)
        els.append(poly([(x, g), (x + 26, g - 4), (x + 30, g - 22), (x + 4, g - 20)], "#b8a57c", "rgba(255,236,206,.4)", 1, te + .5 + .06 * k, fx="pop"))
    els += chip(330, 140, "about 1300 BCE", AMBER, te - .6, 26) + [lab(760, 300, "earthquake?", te + .4, RED, 32)]
    for k in range(9):
        x = 1100 + 62 * k
        hh = 60 + 18 * (k % 3)
        els.append(rect(x, g - hh, 56, hh, "#9c8a6a", "rgba(255,236,206,.5)", 1.5, 2, tr + .1 * k, fx="rise"))
    els += [lab(1380, g - 130, "Troy VIIa", tr + 1.0, GOLD, 34, st="serif")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def pithos(x, top, h, at):
    return [poly([(x - .16 * h, top), (x + .16 * h, top), (x + .34 * h, top + .25 * h), (x + .32 * h, top + .7 * h), (x + .14 * h, top + h), (x - .14 * h, top + h),
                  (x - .32 * h, top + .7 * h), (x - .34 * h, top + .25 * h)], "#b0704a", "#e0a070", 1.5, at, curve=True, fx="pop"),
            poly(E(x, top, .17 * h, .04 * h, 16), "#2a1a10", "#e0a070", 1.2, at)]


def s44():
    """Blegen, 1930s: a Troy VIIa house in section, six big storage jars sunk to their rims in the floor; a person for scale."""
    tb, tj, ts = T("s44", "Carl Blegen's"), T("s44", "storage jars"), T("s44", "laying in supplies")
    fl = 500
    els = [rect(160, fl, 1460, 300, "#6b5640", "none", 0, 0, -1), ln([(160, fl), (1620, fl)], -1, "rgba(255,226,190,.6)", 2, draw=False),
           rect(160, 200, 40, 300, "#9c8a6a", "rgba(255,236,206,.4)", 1.5, 0, .2), rect(1580, 200, 40, 300, "#9c8a6a", "rgba(255,236,206,.4)", 1.5, 0, .2),
           ln([(140, 200), (1640, 200)], .3, WOOD, 10, draw=False), gl(889, 380, 520, .2, .25, "lamp")]
    for k in range(6):
        els += pithos(330 + 180 * k, fl - 2, 150, tj - .4 + .15 * k)
    els += [person(1450, fl, 170, .6, SKIN)] + chip(330, 150, "Blegen, 1930s", AMBER, tb, 24) + \
           [lab(780, 700, "storage jars", tj + .6, BONE, 30), lab(800, 300, "laying in supplies?", ts, LILAC, 32, st="ital")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def house(x, w, g, h, at, c="none", edge="#cbb891"):
    return [poly([(x, g), (x, g - h), (x + w * .5, g - h - 40), (x + w, g - h), (x + w, g)], c, edge, 3, at)]


def s45():
    """About 1180 BCE: fire. Three houses burn, a burnt layer forms below, bronze arrowheads in the ash; a small lamp for the dead."""
    tf, tb, ta = T("s45", "fire"), T("s45", "Burnt houses"), T("s45", "bronze arrowheads")
    g = 560
    els = [ln([(110, g), (1680, g)], -1, "#8c7152", 3, draw=False), rect(110, g, 1570, 440, "#4a3a2c", at=-1)]
    for k, x in enumerate((260, 680, 1100)):
        els += house(x, 360, g, 200, .2 + .1 * k)
        els += [gl(x + 180, g - 110, 190, tf + .2 * k, .9, "fire", pulse=True), gl(x + 120, g - 60, 120, tf + .3 + .2 * k, .8, "red")]
        els += flame(x + 110, g - 200, 60, tf + .2 + .2 * k) + flame(x + 250, g - 200, 48, tf + .35 + .2 * k)
        els += [ln([(x + 40, g - 200), (x + 230, g - 20)], tb + .2 * k, CHAR, 7, dur=.4)]
    els += [rect(110, g + 10, 1570, 60, ASH, "rgba(255,138,90,.5)", 1.5, 0, tb, fx="fill", dur=1.0)]
    rnd = random.Random(8)
    for k in range(14):
        x = rnd.uniform(160, 1620); y = rnd.uniform(g + 22, g + 60)
        els.append(I.tri(round(x, 1), round(y, 1), 10, rnd.uniform(150, 220), "#d9a060", round(ta + .07 * k, 2)))
    els += [gl(900, g + 4, 30, ta + 1.4, .8, "lamp")]
    els += chip(889, 150, "about 1180 BCE", RED, tf - .3, 30) + [lab(889, g + 140, "bronze arrowheads", ta + .6, "#d9a060", 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s46():
    """Sling stones in heaps: a sling; a dashed hand that would gather them; never gathered up."""
    ts, tg, tn = T("s46", "sling stones"), T("s46", "gather up"), T("s46", "never gathered")
    g = 640
    els = [rect(110, g, 1570, 160, ASH, at=-1), ln([(110, g), (1680, g)], -1, "rgba(255,138,90,.5)", 2, draw=False), gl(800, g - 40, 380, .1, .25, "fire")]
    els += stones(620, g, 46, ts - .3, 13, 2, step=.02) + stones(980, g, 38, ts, 12, 5, step=.02)
    els += [ln([(1230, g - 160), (1280, g - 60), (1330, g - 30), (1380, g - 60), (1430, g - 160)], ts + 1.0, "#c9b28a", 3, dur=.8, curve=True),
            poly(E(1330, g - 32, 26, 12, 16), "#8a6a48", "#c9b28a", 1.5, ts + 1.4, fx="pop"), lab(1330, g + 50, "a sling", ts + 1.5, DIM, 26)]
    bx, by = 1240, 230                                     # a basket the winners would fill: dotted, empty
    els += [poly([(bx - 90, by), (bx + 90, by), (bx + 70, by + 110), (bx - 70, by + 110)], "rgba(201,193,238,.06)", LILAC, 2.5, tg - .2, style="claimed"),
            ln([(bx - 90, by), (bx - 60, by - 50), (bx + 60, by - 50), (bx + 90, by)], tg - .2, LILAC, 2.5, "claimed", dur=.5, curve=True),
            arr([(990, 520), (1060, 380), (1140, 300)], tg, LILAC, 3, "claimed", .8), lab(bx, by + 160, "gather up?", tg + .4, LILAC, 30, st="ital")]
    els += [lab(800, 760, "never gathered up", tn + .4, RED, 32), lab(500, 300, "sling stones", ts + .3, BONE, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s47():
    """The excavators' judgement: Blegen (Homer's Troy), Korfmann ('more likely than not'); the digging goes on: sling stones, 2025."""
    tb, tk, t25 = T("s47", "Blegen believed"), T("s47", "more likely than"), T("s47", "twenty twenty")
    g = 300
    els = [rect(-20, g, 1820, 720, "#4a3a2c", at=-1), ln([(-20, g), (1800, g)], -1, "rgba(255,226,190,.6)", 2, draw=False)]
    # layers in the trench wall: three later fills, the thin burnt layer, older ground below
    els += [rect(-20, g + 120 * k, 1820, 120, ["#7a6248", "#8a7050", "#6f5a44"][k], at=-1) for k in range(3)]
    els += [rect(-20, g + 360, 1820, 58, "#5a2a1c", at=-1), ln([(-20, g + 389), (1800, g + 391)], -1, "rgba(240,120,60,.35)", 3, draw=False),
            lab(250, g + 398, "burnt layer", .4, "#f3d2b0", 24)]
    tr = [(520, g), (560, g + 120), (600, g + 120), (640, g + 400), (1140, g + 400), (1180, g + 120), (1220, g + 120), (1260, g)]
    els += [poly(tr, "#241a14", "rgba(255,226,190,.5)", 2, .2)]
    els += [ln([(640 + 100 * k, g + 400), (640 + 100 * k, g + 120)], .4, "rgba(255,255,255,.18)", 1, "inferred", draw=False) for k in range(1, 5)]
    els += [person(740, g + 400, 110, .5, SKIN), person(980, g + 400, 100, .6, SKIN), gl(860, g + 330, 200, .6, .3, "lamp")]
    els += [lab(340, 190, "Blegen:", tb, LILAC, 28), lab(340, 226, "the Troy of the war", tb + .2, LILAC, 28, st="ital")]
    els += chip(1430, 190, "more likely than not", GOLD, tk, 26) + [lab(1430, 246, "Korfmann, 2004", tk + .3, DIM, 24)]
    els += stones(1060, g + 400, 16, t25 + .4, 8, 9, step=.04) + chip(1060, g + 300, "2025", AMBER, t25, 26) + [gl(1060, g + 380, 70, t25 + .6, .7, "lamp")]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def XA(yr):
    return round(180 + (1600 - 180) * (yr + 1350) / 250, 1)


def s48():
    """Ancient dates for the fall: counted back through kings, spread over two centuries; Eratosthenes, 1184 BCE; then the fire, about 1180."""
    tg, ts, te, tf = T("s48", "generations of"), T("s48", "two centuries"), T("s48", "Eratosthenes"), T("s48", "beside the fire")
    y = 650
    ticks = [[XA(v), t] for v, t in ((-1350, "1350 BCE"), (-1300, "1300"), (-1250, "1250"), (-1200, "1200"), (-1150, "1150"), (-1100, "1100"))]
    els = [axis(180, 1600, y, ticks, .2)]
    for k, v in enumerate((-1334, -1250, -1209, -1184, -1135)):
        els.append(circ(XA(v), 450, 14, LILAC, "none", 0, tg + .35 * k, fx="pop", op=.85))
        els.append(ln([(XA(v), y - 14), (XA(v), y)], tg + .35 * k, LILAC, 3, dur=.2))
    els += bracket(XA(-1334), XA(-1135), 380, ts, None, LILAC, up=False) + [lab((XA(-1334) + XA(-1135)) / 2, 360, "two centuries of guesses", ts + .3, LILAC, 28)]
    els += [circ(XA(-1184), 450, 22, AU, "#fff4dc", 2, te, fx="pop"), gl(XA(-1184), 450, 80, te, .6, "lamp"),
            lab(XA(-1184), 512, "Eratosthenes: 1184", te + .3, AU, 28)]
    els += [{"k": "band", "x0": XA(-1190), "x1": XA(-1170), "y": 580, "h": 18, "c": FIRE, "in": tf}] + flame(XA(-1180), 574, 26, tf) + \
           [lab(XA(-1170) + 30, 596, "the fire, about 1180", tf + .3, FIRE, 26, "start")]
    # a family tree: kings counted back, generation by generation
    tx, ty = 300, 170
    nodes = [(tx, ty), (tx - 50, ty + 50), (tx + 50, ty + 50), (tx - 75, ty + 100), (tx - 25, ty + 100), (tx + 25, ty + 100), (tx + 75, ty + 100)]
    links = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    els += [ln([nodes[a], nodes[b]], tg - .3 + .1 * k, DIM, 2, dur=.2) for k, (a, b) in enumerate(links)]
    els += [dot(x, y_, 8, DIM, tg - .3 + .06 * k) for k, (x, y_) in enumerate(nodes)]
    els += [lab(tx, ty + 150, "kings, counted back", tg + .4, DIM, 24)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s49():
    """The eastern Mediterranean in the same few decades: Hattusa emptied then burned, Ugarit and Pylos burned, Egypt fights invaders from the sea."""
    v = View(19.0, 37.5, 29.6, 42.4, (90, 120, 1600, 680))
    th, tu, tp, te = T("s49", "Hittite capital"), T("s49", "Ugarit"), T("s49", "Pylos"), T("s49", "Egypt")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    tx, ty = v.p(26.2389, 39.9575)
    els += [gl(tx, ty, 70, .3, .7, "fire", pulse=True), dot(tx, ty, 9, RED, .3), lab(tx - 18, ty - 18, "Troy", .5, RED, 28, "end")]
    for k, (name, lo, la, at, a) in enumerate((("Hattusa", 34.615, 40.02, th, "start"), ("Ugarit", 35.782, 35.602, tu, "end"), ("Pylos", 21.695, 37.028, tp, "end"))):
        x, y = v.p(lo, la)
        els += flame(x, y + 8, 30, at) + [lab(x + (22 if a == "start" else -22), y - 14, name, at + .2, BONE, 28, a)]
    dx, dy = v.p(30.9, 31.2)
    els += [lab(dx - 30, dy + 70, "Egypt", te + .2, BONE, 30, "end")]
    for k, (lo, la) in enumerate(((29.2, 32.6), (30.4, 32.8), (31.6, 32.5))):
        x, y = v.p(lo, la)
        els += galley(x, y, 54, te + .15 * k, "#e8d6b8", 1)
    els += [arr([v.p(27.5, 33.6), v.p(29.8, 32.2), v.p(30.8, 31.75)], te + .4, RED, 3, dur=.8)]
    els += [{"k": "scale", "x": 160, "y": 760, "w": round(v.km(300), 1), "t": "300 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def s50():
    """Tree rings as a diary: wide in wet years, thin in dry; three thin rings in a row around 1198 BCE (junipers, central Turkey)."""
    tw, tt, t3 = T("s50", "wide ring"), T("s50", "thin one"), T("s50", "three thin rings")
    cx, cy, R0 = 420, 440, 250
    els = [gl(cx, cy, 360, .1, .25, "lamp"), circ(cx, cy, R0 + 12, "#5a3e26", "#2a1c10", 3, .2)]
    rr, widths = 0, []
    rnd = random.Random(3)
    while rr < R0:
        w = rnd.uniform(5, 14)
        widths.append(w); rr += w
    rr = 0
    for k, w in enumerate(widths):
        rr += w
        els.append(circ(cx, cy, min(rr, R0), "none", "#7a5636" if k % 2 else "#a07a50", 2.2, .3 + .02 * k, fx="draw", dur=.25))
    els += [poly([(cx, cy), (cx + R0 * math.cos(-.18), cy + R0 * math.sin(-.18)), (cx + R0 * math.cos(.18), cy + R0 * math.sin(.18))], "rgba(242,201,142,.12)", GOLD, 2, tw - .5)]
    sx, sy, sw, sh = 820, 320, 800, 240
    els += [rect(sx, sy, sw, sh, "#c9a370", "#5a3e26", 3, 6, tw - .3), ln([(cx + R0 * math.cos(-.18), cy + R0 * math.sin(-.18)), (sx, sy)], tw - .3, GOLD, 1.5, "inferred", dur=.4),
            ln([(cx + R0 * math.cos(.18), cy + R0 * math.sin(.18)), (sx, sy + sh)], tw - .3, GOLD, 1.5, "inferred", dur=.4)]
    pattern = [34, 30, 12, 36, 28, 10, 32, 38, 26, 30, 8, 8, 8, 34, 30, 28, 36, 12, 30, 32, 28, 36, 14, 30, 34, 26, 32, 12, 30]
    x = sx + 12
    xs = []
    for k, w in enumerate(pattern):
        if x + w > sx + sw - 8:
            break
        dry = w < 15
        els.append(rect(x, sy + 12, w - 3, sh - 24, "#7a4a2a" if dry else "#e0b884", "none", 0, 1, tw + .03 * k, op=.95))
        if 10 <= k <= 12:
            els.append(rect(x - 1, sy + 6, w - 1, sh - 12, "none", RED, 3, 1, t3 + .2 * (k - 10), fx="pop"))
        xs.append((x, w))
        x += w
    (wx, ww), (dx_, dw) = xs[1], xs[5]
    els += [ln([(wx + ww / 2, sy + 8), (wx + ww / 2, sy - 8)], tw + .3, "#e0b884", 2, dur=.2), lab(wx + ww / 2, sy - 18, "wet year", tw + .3, "#e0b884", 26),
            ln([(dx_ + dw / 2, sy + sh - 8), (dx_ + dw / 2, sy + sh + 10)], tt, "#c08060", 2, dur=.2), lab(dx_ + dw / 2, sy + sh + 40, "dry year", tt, "#c08060", 26),
            lab(xs[11][0] + 4, sy - 18, "about 1198 BCE", t3 + .6, RED, 28), lab(cx, cy + R0 + 56, "juniper, central Turkey", t3, DIM, 24)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s51():
    """Four suspects for the fire: Greeks? raiders? a rival? collapse? Below, the burnt layer with its blank signature."""
    t1, t2, t3, t4, tg, ts = (T("s51", p) for p in ("Greeks", "Sea raiders", "A rival", "a world coming", "ground records", "sign the name"))
    xs = [140, 545, 950, 1355]
    els = []
    for k, (x, at, name) in enumerate(zip(xs, (t1, t2, t3, t4), ("Greeks?", "raiders?", "a rival?", "collapse?"))):
        els += [rect(x, 170, 300, 300, "rgba(245,236,220,.05)", LILAC, 2.5, 18, at - .1, fx="pop", style="claimed"), lab(x + 150, 520, name, at + .2, LILAC, 32, st="ital")]
    els += warrior(xs[0] + 150, 440, 230, t1, 1, "#e8d6b8", "#7a5a3a")
    els += galley(xs[1] + 150, 390, 230, t2, "#e8d6b8", -1) + [ln([(xs[1] + 30, 400), (xs[1] + 270, 400)], t2, BLUE, 3, draw=False)]
    els += [person(xs[2] + 150, 440, 230, t3, "#9fb0c0"), ln([(xs[2] + 200, 250), (xs[2] + 230, 450)], t3, "#9fb0c0", 4, draw=False)]
    els += [circ(xs[3] + 150, 320, 110, "rgba(232,184,122,.15)", AMBER, 3, t4, fx="pop"),
            ln([(xs[3] + 120, 215), (xs[3] + 150, 290), (xs[3] + 132, 330), (xs[3] + 170, 380), (xs[3] + 150, 430)], t4 + .2, RED, 4, dur=.5)]
    els += [rect(140, 600, 1500, 70, ASH, "rgba(255,138,90,.5)", 1.5, 6, tg - .4, fx="fill", dur=.6), gl(889, 635, 400, tg, .45, "fire")]
    els += [ln([(1260, 640), (1560, 640)], ts, BONE, 2.5, dur=.5), lab(1270, 628, "signed:", ts + .2, DIM, 24, "start"), lab(1580, 650, "?", ts + .6, LILAC, 54, "start", st="serif")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 6 · The weighing
LROWS = [190, 300, 410, 520, 630]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 48, 1500, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1190, y, grade, gc, gt, 28, "start")
    return out


def pic_strata(x, y, at):
    return [rect(x - 46, y - 36 + 9 * k, 92, 9, TCOL[9 - k], "none", 0, 0, at, fx="pop") for k in range(8)]


def pic_wall(x, y, at):
    return [poly([(x - 46, y + 34), (x + 10, y + 34), (x + 10, y - 30), (x - 30, y - 30)], "url(#k-blocks)", "rgba(255,236,206,.5)", 1, at, fx="pop"),
            rect(x - 18, y - 52, 28, 22, MUD, at=at, fx="pop")]


def pic_diadem(x, y, at):
    return [ln([(x - 40, y - 26), (x + 40, y - 26)], at, AU, 4, draw=False)] + [ln([(x - 34 + 9 * k, y - 26), (x - 34 + 9 * k, y + 10 + 6 * (k % 2))], at, AU, 1.5, draw=False) for k in range(9)]


def pic_fire(x, y, at):
    return [rect(x - 46, y + 6, 92, 22, ASH, at=at, fx="pop")] + flame(x, y + 6, 40, at)


def pic_frieze(x, y, at):
    return [rect(x - 50, y - 38, 100, 76, TERRA, "none", 0, 6, at, fx="pop")] + galley(x, y + 18, 70, at + .05) + [ln([(x - 30, y - 16), (x + 30, y - 16)], at, BLK, 3, draw=False)]


def s52():
    """The ledger: nine cities (Established), a citadel and seat of power (Established), Priam's treasure (Ruled out)."""
    t1, g1 = T("s52", "Established"), T("s52", "Roman times")
    t2, g2 = T("s52", "Established", k=2), T("s52", "seat of power")
    t3, g3 = T("s52", "Schliemann's gold"), T("s52", "Ruled out")
    els = [rect(110, 128, 1560, 570, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, t1, pic_strata, "nine cities, 3000 BCE to Roman times", "Established", g1, GRADE["established"])
    els += lrow(1, t2, pic_wall, "a strong citadel, seat of power", "Established", g2, GRADE["established"])
    els += lrow(2, t3, pic_diadem, "the gold as Priam's treasure", "Ruled out", g3, GRADE["ruled"]) + [strike(170, 425, 262, 392, g3 + .2, RED, 5)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s53_add():
    """Row 4: a real, rich city burnt about 1180 BCE: Strong evidence; three reasons converge on the chip."""
    tr, tg, tw = T("s53", "A real, rich"), T("s53", "Strong evidence"), T("s53", "The walls")
    y = LROWS[3]
    els = lrow(3, tr, pic_fire, "a rich city, burnt about 1180 BCE", "Strong evidence", tg, GRADE["strong"])
    els += [gl(1330, y, 200, tg, .35, "lamp")]
    return els


def s54_add():
    """Row 5: the war as Homer tells it: Open question; a quarrel on record (tick), a Greek siege not (question)."""
    tr, tg, tq, ts = T("s54", "the war as Homer"), T("s54", "Open question"), T("s54", "A quarrel over"), T("s54", "A Greek siege")
    els = lrow(4, tr, pic_frieze, "the war as Homer tells it", "Open question", tg, GRADE["open"])
    els += [tick(470, 728, tq, GREEN, .8), lab(500, 738, "a quarrel over Wilusa", tq + .2, BONE, 26, "start"),
            lab(1010, 744, "?", ts, LILAC, 40, st="serif"), lab(1040, 738, "a Greek siege", ts + .2, BONE, 26, "start")]
    return els


def s55():
    """What would settle it: a tablet with the attacker's name, an archive from Troy (one seal so far), the chemistry and DNA of the dead."""
    tt, ta, td = T("s55", "A tablet that"), T("s55", "A palace archive"), T("s55", "chemistry and DNA")
    els = [gl(889, 420, 640, .1, .2, "lamp")]
    els += [rect(240, 230, 220, 280, "rgba(201,193,238,.08)", LILAC, 2.5, 22, tt, fx="pop", style="claimed"),
            {"k": "glyphs", "x": 270, "y": 260, "w": 160, "h": 130, "rows": 5, "cols": 5, "kind": "cuneiform", "c": "rgba(201,193,238,.6)", "in": tt + .2},
            rect(280, 420, 140, 50, "none", AU, 2.5, 6, tt + .4, style="inferred"), lab(350, 454, "?", tt + .5, AU, 36, st="serif"),
            lab(350, 580, "a name", tt + .6, LILAC, 30)]
    els += [rect(720, 240, 340, 18, "none", LILAC, 2, 2, ta, style="claimed"), rect(720, 380, 340, 18, "none", LILAC, 2, 2, ta + .1, style="claimed"),
            rect(720, 520, 340, 18, "none", LILAC, 2, 2, ta + .2, style="claimed")]
    els += [rect(740 + 48 * k, 290 + 140 * (k % 2), 36, 86, "none", LILAC, 1.5, 4, ta + .3 + .05 * k, style="claimed") for k in range(6)]
    els += [circ(980, 352, 20, BRONZE, "#fff4dc", 2, ta + .9, fx="pop"), gl(980, 352, 60, ta + .9, .6, "lamp"), lab(890, 600, "1 seal so far", ta + 1.1, AU, 30)]
    hx = 1400
    a1 = [(hx - 50 + 40 * math.sin(k * .5), 230 + 14 * k) for k in range(22)]
    a2 = [(hx - 50 - 40 * math.sin(k * .5), 230 + 14 * k) for k in range(22)]
    els += [ln(a1, td, LILAC, 3, "claimed", 1.0, True), ln(a2, td + .1, LILAC, 3, "claimed", 1.0, True)]
    els += [ln([a1[k], a2[k]], td + .4 + .03 * k, "rgba(201,193,238,.6)", 1.5, draw=False) for k in range(1, 22, 2)]
    els += [poly([(hx + 70, 330), (hx + 110, 330), (hx + 118, 380), (hx + 104, 450), (hx + 92, 400), (hx + 84, 400), (hx + 76, 450), (hx + 62, 380)], "rgba(239,230,210,.2)",
                  LILAC, 2, td + .6, style="claimed"), circ(hx + 90, 395, 70, "none", AU, 2, td + .9, style="inferred"),
            lab(hx + 20, 580, "where from?", td + 1.1, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s56_add():
    """The close: the hill at dusk again, its fire layer glowing low, the story's city glimmering above."""
    return [gl(900, 440, 260, .4, .35, "fire"), gl(900, 270, 320, 1.2, .3, "lamp")]


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "High in the stack", "s2"), (1, "Homer's poems", "s3"), (1, "Was this the", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "In the {1860s", "s7")], {"chapter": "A hill of nine cities"}),
    (1, 1, "collision", "s8", [(1, "A mound like", "s9"), (2, "From {1871", "s10")], {}),
    (1, 2, "reversal", "s11", [(1, "The gold came", "s12"), (1, "And on the way", "s13")], {}),
    (1, 3, "tag", "s14", [], {}),
    (2, 0, "world", "s15", [(1, "A citadel of", "s16")], {"chapter": "The walls and the lower town"}),
    (2, 1, "collision", "s17", [(0, "A line appeared", "s18"), (1, "Inside it", "s19")], {}),
    (2, 2, "reversal", "s20", [(1, "Four specialists", "s21")], {}),
    (2, 3, "tag", "s22", [], {}),
    (3, 0, "world", "s23", [(1, "Its archives", "s24")], {"chapter": "A name in Hittite clay"}),
    (3, 1, "collision", "s25", [(1, "Around {1280", "s26"), (2, "Among the gods", "s27"), (2, "At Troy, there", "s28")], {}),
    (3, 2, "reversal", "s29", [(0, "Around {1250", "s30"), (1, "Hostile could", "s31"), (2, "In a later", "s32")], {}),
    (3, 3, "tag", "s33", [], {}),
    (4, 0, "world", "s34", [], {"chapter": "What Homer remembered"}),
    (4, 1, "collision", "s35", [(0, "Singers like", "s36")], {}),
    (4, 2, "reversal", "s37", [(1, "A list of", "s38"), (1, "And a Troy of", "s39")], {}),
    (4, 3, "cost", "s40", [(0, "They prize", "s41")], {}),
    (4, 4, "tag", "s42", [], {}),
    (5, 0, "world", "s43", [(1, "In the {1930s", "s44")], {"chapter": "The fire and the fall"}),
    (5, 1, "collision", "s45", [(0, "And sling stones", "s46"), (1, "Blegen believed", "s47")], {}),
    (5, 2, "reversal", "s48", [(1, "But look at", "s49"), (2, "Trees keep", "s50")], {}),
    (5, 3, "tag", "s51", [], {}),
    (6, 0, "weigh", "s52", [(1, "A real, rich", "s53"), (2, "And the war as", "s54")], {"chapter": "The weighing"}),
    (6, 1, "test", "s55", [], {}),
    (6, 2, "close", "s56", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.75, 900, 470], "s2_add"), "s4": ("s1", [1, 889, 500], "s4_add"),
    "s8": ("s7", [1.25, 1067, 560], "s8_add"), "s12": ("s11", [1, 889, 500], "s12_add"), "s13": ("s10", [2.0, 900, 500], "s13_add"),
    "s19": ("s18", [1, 889, 500], "s19_add"), "s21": ("s20", [1, 889, 500], "s21_add"),
    "s29": ("s23", [1, 889, 500], "s29_add"), "s33": ("s24", [1.6, 556, 384], "s33_add"),
    "s53": ("s52", [1, 889, 500], "s53_add"), "s54": ("s52", [1, 889, 500], "s54_add"),
    "s56": ("s1", [1.05, 900, 480], "s56_add"),
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
    ep = {"id": "lf-troy", "code": "LF.11", "series": script["series"], "title": script["title"], "case": "troy",
          "verdict": "strong", "claim": "Was Homer's Troy a real city, and did it fall in a real war?", "mood": "mystery",
          "hook_text": "Was there really a *Trojan* War?", "beats": beats, "shots": shots,
          "sources": "Blegen 1963 · Korfmann 2004 (Archaeology 57.3) · Jablonka & Rose 2004 (doi:10.3764/aja.108.4.615) · Kolb 2004 (doi:10.3764/aja.108.4.577) · "
                     "Easton et al. 2002 (doi:10.2307/3643078) · Latacz 2004 · Beckman 1999 · Beckman, Bryce & Cline 2011 · "
                     "Frank et al. 2002 (doi:10.1111/1475-4754.t01-1-00062) · Bowra 1960 (doi:10.2307/628372) · Manning et al. 2023 (doi:10.1038/s41586-022-05693-y)",
          "post": "A low hill in Turkey holds nine cities, and high in the stack, a layer of fire from around 1180 BCE. Schliemann's trench, the walls of Troy VI, "
                  "Korfmann's lower town and its critics, a kingdom called Wilusa in Hittite clay, what Homer remembered and what he added, weighed.",
          "hashtags": ["#Troy", "#TrojanWar", "#Homer", "#Iliad", "#Archaeology", "#WeighItYourself"],
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
