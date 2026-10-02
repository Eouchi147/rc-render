"""LF.12 · Fallen Worlds · The Sea Peoples and the End of the Bronze Age (16:9 long film, one wall; see films/long/LONG_ENGINE.md).

The script is films/long/lf-sea-peoples/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s65; s5, the title hold, is the panel of s4
under the intro card), drawn while it is said: the sea battle carved at Medinet Habu, the burning palaces, the last letters of Ugarit,
the Philistines and the DNA of Ashkelon, Hattusa emptied before it burned, Pylos, Cyprus, then the other suspects (lake pollen, the
tree rings of Gordion, the grain letters, the earthquake storm and its test, the Uluburun ship and the sea lanes, trouble from within,
the perfect storm) and the weighing, one grade per suspect.

Drawings are schematic and true to the numbers said: the Medinet Habu reliefs as carved sandstone (bird-head stems and sterns,
feathered crowns, horned helmets, the rowed Egyptian ships, a capsized ship, a grappling hook, ox carts with women and children);
solid = measured or documented, dashed = inferred or wanted, dotted = claimed (Egypt's boast, the name links, Drews' proposal, the
earthquake storm). Human remains with care: the infants of Ashkelon are a lamp-lit hollow under a floor, no bones; the fallen at
Mycenae are fallen stones and a lamp; the palace plot is an empty throne. No people is the villain.

Reused from the Short 'sea-peoples' (f11.py sea_peoples / sea_peoples_m): its palace map with fires, its nine helmeted warriors, its
tree rings, its web of six causes and its timeline, all redrawn wide for 16:9.

Engine workaround (as in lf_atlantis.py and lf_derinkuyu.py): the wall only adds elements to a panel on its first visit, at a beat
start or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a
tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as
a panel item (kit.js builds them on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-sea-peoples/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-sea-peoples/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-sea-peoples RC_FILMS_EPS=/tmp/claude-0/sbx_lf-sea-peoples/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-sea-peoples/boards python3 films.py long.lf_sea_peoples
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, ellipse, question

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-sea-peoples", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, GOLD, BLUE, LILAC, RED, GREEN, AU = I.BONE, I.AMBER, "#f2c98e", I.BLUE, I.LILAC, I.RED, I.GREEN, I.AU
DIM, DARK, SEA, FIRE = "#cbbca8", "#1a1511", "#3f86b0", "#ff9a4a"
COPPER, TIN, GRAIN, CLAY, CLAYD = "#d9894a", "#b9bfc6", "#e8c35a", "#c79a6a", "#8a6440"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c86a", "open": "#f0b06a", "mixed": "#d8c7a8",
         "awaiting": "#c9c1ee", "ruled": "#e98a8a"}
WPS = 2.5                    # spoken words a second (the narrator's measured pace in the rendered films: about 2.6, pauses included)

# the carved sandstone of Medinet Habu
WALL, WALL2, CUT, CUT2, EDGE_D, EDGE_L = "#b8946a", "#ad8a60", "#80603e", "#6c4d30", "#2e1d0c", "#f8e2ba"
CROWN = "#5d7391"            # a trace of the blue crown's paint


# ================================================================== narration: the script's own lines, timing
def words(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", s)
    s = re.sub(r"@\w+", "", s).replace("-", " ")
    return [w for w in (re.sub(r"[^\w']", "", x).lower().strip("'") for x in s.split()) if w]


SAY = {}                     # shot id -> the narration spoken while its step is on screen (set in film())


def T(sid, phrase, lead=.35, k=1):
    """Seconds after the shot's step starts at which `phrase` is said (its k-th occurrence)."""
    ws, ps = words(SAY[sid]), words(phrase)
    hits = [i for i in range(len(ws)) if ws[i:i + len(ps)] == ps]
    assert len(hits) >= k, (sid, phrase, SAY[sid])
    return round(lead + hits[k - 1] / WPS, 2)


def dur(sid):
    return round(len(words(SAY[sid])) / WPS, 2)


def _find(line_, phrase):
    """Index in the raw line where `phrase` starts, ignoring the ^ stress marks."""
    keep = [i for i, ch in enumerate(line_) if ch != "^"]
    flat = "".join(line_[i] for i in keep)
    assert flat.count(phrase) == 1, (phrase, line_)
    return keep[flat.index(phrase)]


def _mark(line_, phrase, tag):
    """Insert `tag` at the start of the sentence that begins with `phrase`: before its [p:]/[act:]/[sfx:]/[tune:]/[gap:] tags,
    after a [d:] mood tag."""
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


def E(cx, cy, rx, ry, n=36, a0=0, a1=360):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + (0 if a1 - a0 >= 360 else 1))]


def poly(p, fill, c="none", w=0, at=0, fx=None, op=None, curve=False, style="known", **kw):
    e = {"k": "poly", "p": R(p), "fill": fill, "c": c, "w": w, "curve": curve, "in": round(at, 2) if at is not None else None}
    if style != "known":
        e["style"] = style
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(round(x, 1), round(y, 1), round(w, 1), round(h, 1), fill, c, sw, r, round(at, 2), op, fx, **kw)


def lab(x, y, t, at, c=BONE, size=28, a="middle", st="lab", **kw):
    return label(round(x, 1), round(y, 1), t, round(at, 2), c, size, a, st, **kw)


def ln(p, at, c=BONE, w=3, style="known", dur=None, curve=False, draw=True, op=None):
    return line(R(p), round(at, 2), c, w, style, dur, curve, draw, op)


def arr(p, at, c=AMBER, w=3, style="known", dur=1.0, curve=True):
    return arrow(R(p), round(at, 2), c, w, style, dur, curve)


def circ(x, y, r, fill, c="none", w=0, at=0, fx=None, op=None, style="known"):
    e = {"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r, 1), "fill": fill, "c": c, "w": w, "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    if style != "known":
        e["style"] = style
    return e


def chip(x, y, t, at, c, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, "pop"),
            lab(x0 + w / 2, y + size * .36, t, at + .05, c, size, halo=False)]


def tick(x, y, at, c=GREEN, s=1.0):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cover(x, y, w, h, at, fill, op=1.0, dur=.6, r=0):
    """A sheet laid over part of a panel in its background colour: what was there fades away (op 1) or dims (op < 1)."""
    e = rect(x, y, w, h, fill, r=r, at=at, op=op)
    e["dur"] = dur
    return e


def thick(p, w):
    """A polyline drawn as a closed outline of width w (mitred), for limbs, posts and oars that are carved, not stroked."""
    L, Rt = [], []
    n = len(p)
    for i in range(n):
        if i == 0:
            dx, dy = p[1][0] - p[0][0], p[1][1] - p[0][1]
        elif i == n - 1:
            dx, dy = p[-1][0] - p[-2][0], p[-1][1] - p[-2][1]
        else:
            dx, dy = p[i + 1][0] - p[i - 1][0], p[i + 1][1] - p[i - 1][1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d * w / 2, dx / d * w / 2
        L.append((p[i][0] + nx, p[i][1] + ny)); Rt.append((p[i][0] - nx, p[i][1] - ny))
    return L + Rt[::-1]


def tablet(x, y, w, h, at, rows=7, cols=7, fx="pop", c=CLAY, ink="#4a3522", seed=1):
    """A clay tablet face on, wedges in rows (cuneiform)."""
    return [rect(x + 8, y + 10, w, h, "rgba(0,0,0,.45)", r=w * .12, at=at, fx=fx),
            rect(x, y, w, h, c, "#e9cfa6", 2, w * .12, at, fx),
            {"k": "glyphs", "x": round(x + w * .1, 1), "y": round(y + h * .08, 1), "w": round(w * .8, 1), "h": round(h * .84, 1), "rows": rows, "cols": cols,
             "kind": "cuneiform", "c": ink, "seed": seed, "in": round(at + .15, 2)}]


def flame(x, y, s, at, op=.95):
    """A small flame with its glow, base on (x, y)."""
    f1 = [(x - .5 * s, y), (x - .55 * s, y - .5 * s), (x - .2 * s, y - 1.05 * s), (x - .05 * s, y - .65 * s), (x + .15 * s, y - 1.35 * s),
          (x + .5 * s, y - .6 * s), (x + .48 * s, y)]
    f2 = [(x - .25 * s, y), (x - .25 * s, y - .4 * s), (x + .05 * s, y - .85 * s), (x + .25 * s, y - .4 * s), (x + .22 * s, y)]
    return [glow(round(x, 1), round(y - .5 * s, 1), round(2.6 * s, 1), round(at, 2), .8, "fire"),
            poly(f1, "#e8692a", at=at, fx="rise", op=op, curve=True), poly(f2, "#ffd27a", at=at + .1, fx="rise", op=op, curve=True)]


def ship_icon(x, y, s, at, c=BONE, face=1, op=None, style="known", fill=None):
    """A small Sea Peoples ship for maps: a crescent hull, a bird's head on the stem and the stern, a mast."""
    f = face
    hull = [(x - .5 * s * f, y - .32 * s), (x - .44 * s * f, y + .02 * s), (x + .44 * s * f, y + .02 * s), (x + .5 * s * f, y - .32 * s),
            (x + .42 * s * f, y - .1 * s), (x - .42 * s * f, y - .1 * s)]
    out = [poly(hull, fill or c, c if fill else "none", 1.5 if fill else 0, at, "pop", op=op, style=style),
           ln([(x, y - .1 * s), (x, y - .7 * s)], at, c, max(2, s * .05), style, draw=False, op=op)]
    for sx in (-1, 1):
        bx, by = x + sx * .5 * s * f, y - .36 * s
        out.append(circ(bx, by, .07 * s, c, at=at, fx="pop", op=op))
        out.append(poly([(bx + sx * .05 * s * f, by - .03 * s), (bx + sx * .2 * s * f, by + .01 * s), (bx + sx * .05 * s * f, by + .04 * s)], c, at=at, fx="pop", op=op))
    return out


def ingot(x, y, s, at, c=COPPER, fx="pop", op=None):
    """An oxhide copper ingot seen from above: a slab with four drawn-out corners."""
    pts = [(x - .5 * s, y - .32 * s), (x - .3 * s, y - .2 * s), (x + .3 * s, y - .2 * s), (x + .5 * s, y - .32 * s), (x + .42 * s, y),
           (x + .5 * s, y + .32 * s), (x + .3 * s, y + .2 * s), (x - .3 * s, y + .2 * s), (x - .5 * s, y + .32 * s), (x - .42 * s, y)]
    return poly(pts, c, "#ffd2a8", 1.5, at, fx, op=op)


def jar(x, y, h, at, c="#b8875a", level=None, lvl_at=None):
    """A storage jar (pithos) standing on y; an optional grain level (0..1) that is drawn as a fill."""
    w = h * .62
    pts = [(x - .18 * w, y - h), (x - .2 * w, y - .93 * h), (x - .5 * w, y - .72 * h), (x - .52 * w, y - .45 * h), (x - .3 * w, y - .08 * h), (x - .14 * w, y),
           (x + .14 * w, y), (x + .3 * w, y - .08 * h), (x + .52 * w, y - .45 * h), (x + .5 * w, y - .72 * h), (x + .2 * w, y - .93 * h), (x + .18 * w, y - h)]
    out = [poly(pts, c, "#f0d2a6", 2, at, "rise", curve=True)]
    out.append(ln([(x - .2 * w, y - h), (x + .2 * w, y - h)], at, "#f0d2a6", 3, draw=False))
    return out


def figure(x, y, h, at, c="#e8d6b8", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def qm(x, y, at, size=90, c=LILAC):
    return [glow(round(x, 1), round(y - size * .3, 1), round(size * 1.3, 1), round(at, 2), .5), lab(x, y, "?", at, c, size, st="big", fx="pop")]


# ================================================================== the relief: carved sandstone, Medinet Habu
def carve(p, at=-1, fill=CUT, w=2.2, curve=False, op=None, lit=True):
    """A shape cut into the stone: a darker sunk face, a shadow edge, and a lit edge offset down and right."""
    out = []
    if lit:
        out.append(poly([(x + 2.4, y + 2.4) for x, y in p], "none", EDGE_L, 1.7, at, curve=curve, op=.6))
    out.append(poly(p, fill, EDGE_D, w, at, curve=curve, op=op))
    return out


def cut(p, at=-1, w=3, op=None, curve=False):
    """A line cut into the stone (a shadow groove with a lit lip)."""
    return [ln([(x + 2, y + 2) for x, y in p], at, EDGE_L, max(1.4, w * .5), curve=curve, draw=False, op=.55),
            ln(p, at, EDGE_D, w, curve=curve, draw=False, op=op)]


def limb(p, w, at=-1, fill=CUT):
    return carve(thick(p, w), at, fill)


def wall_bg(at=-1, x0=0, y0=0, x1=W_, y1=H_, seed=3):
    """A wall of sandstone blocks: courses, staggered joints, a few blocks a shade darker, raking light from the upper left."""
    rr = random.Random(seed)
    out = [rect(x0 - 20, y0 - 20, x1 - x0 + 40, y1 - y0 + 40, WALL, at=at)]
    ch = 150
    y = y0 - 40
    row = 0
    while y < y1:
        x = x0 - 40 - (row % 2) * 110
        while x < x1:
            w = rr.choice((210, 240, 260, 290))
            if rr.random() < .35:
                out.append(rect(x + 2, y + 2, w - 4, ch - 4, WALL2, at=at, op=round(rr.uniform(.35, .8), 2)))
            out.append(ln([(x, y), (x, y + ch)], at, "#7a5c3c", 1.2, draw=False, op=.45))
            x += w
        out.append(ln([(x0 - 20, y), (x1 + 20, y)], at, "#7a5c3c", 1.4, draw=False, op=.5))
        y += ch
        row += 1
    out += [glow(300, 160, 1000, at, .4, "lamp"), rect(x0 - 20, y1 - 230, x1 - x0 + 40, 300, "rgba(20,12,6,.3)", at=at)]
    return out


GL = {}                      # hieroglyph shapes in a unit cell (x, y in 0..1), drawn as cut lines


def _glyphs():
    GL["water"] = [[(0, .5), (.15, .38), (.3, .5), (.45, .38), (.6, .5), (.75, .38), (.9, .5)]]
    GL["bread"] = [[(.15, .62), (.25, .4), (.5, .32), (.75, .4), (.85, .62), (.15, .62)]]
    GL["reed"] = [[(.5, .95), (.42, .6), (.45, .25), (.55, .05), (.6, .3), (.56, .65), (.5, .95)]]
    GL["sun"] = [[(.5 + .32 * math.cos(a / 8 * math.pi), .5 + .32 * math.sin(a / 8 * math.pi)) for a in range(17)], [(.48, .5), (.52, .5)]]
    GL["bird"] = [[(.1, .55), (.3, .35), (.55, .38), (.68, .2), (.8, .22), (.72, .4), (.85, .75), (.55, .7), (.3, .72), (.1, .55)], [(.45, .72), (.42, .95)], [(.6, .72), (.62, .95)]]
    GL["arm"] = [[(.1, .45), (.6, .45), (.9, .25)], [(.1, .55), (.62, .55), (.92, .38)]]
    GL["viper"] = [[(.05, .7), (.3, .6), (.6, .62), (.8, .5), (.9, .35)], [(.85, .38), (.95, .2)]]
    GL["stroke"] = [[(.5, .1), (.5, .9)]]
    GL["house"] = [[(.2, .85), (.2, .2), (.8, .2), (.8, .85)]]
    GL["ankh"] = [[(.5, .45), (.35, .3), (.4, .1), (.6, .1), (.65, .3), (.5, .45)], [(.5, .45), (.5, .95)], [(.25, .55), (.75, .55)]]


_glyphs()


def hiero(x0, y0, cols, colw, rows, rowh, at=-1, seed=5, op=.75):
    """Columns of hieroglyphs between cut column lines (decorative: no real text is claimed)."""
    rr = random.Random(seed)
    names = list(GL)
    out = []
    for c in range(cols + 1):
        out += cut([(x0 + c * colw, y0), (x0 + c * colw, y0 + rows * rowh)], at, 2, op=op)
    for c in range(cols):
        for r in range(rows):
            g = GL[rr.choice(names)]
            cx, cy, s = x0 + c * colw + colw * .15, y0 + r * rowh + rowh * .1, min(colw, rowh) * .7
            for stroke_ in g:
                out += cut([(cx + u * s, cy + v * s) for u, v in stroke_], at, 2.2, op=op)
    return out


def water(x0, x1, y0, rows, dy=26, at=-1, seg=22, op=.85):
    """Egyptian water: rows of zigzags."""
    out = []
    for k in range(rows):
        y = y0 + k * dy
        pts, x, up = [], x0 + (k % 2) * seg / 2, False
        while x <= x1:
            pts.append((x, y - (9 if up else 0)))
            up = not up
            x += seg / 2
        out += cut(pts, at, 2, op=op)
    return out


def bust(x, y, s, at=-1, head="feather", face=1, shield=True, spear=None):
    """A Sea Peoples warrior from the waist up, standing behind a ship's rail at y; s is waist-to-crown height."""
    f = face
    hx, hy, r = x + .02 * s * f, y - .72 * s, .11 * s
    out = []
    if spear:                                     # a spear held upright, behind the body
        out += cut([(x - .14 * s * f, y + .05 * s), (x - .14 * s * f, y - 1.18 * s)], at, 2.6)
    torso = [(x - .19 * s, y), (x - .22 * s, y - .42 * s), (x - .1 * s, y - .58 * s), (x + .1 * s, y - .58 * s), (x + .22 * s, y - .42 * s), (x + .19 * s, y)]
    out += carve(torso, at)
    neck = [(hx - .04 * s, y - .62 * s), (hx + .04 * s, y - .62 * s), (hx + .04 * s, y - .56 * s), (hx - .04 * s, y - .56 * s)]
    out += carve(neck, at)
    face_ = [(hx - r, hy - .2 * r), (hx - .6 * r, hy - r), (hx + .4 * r, hy - r), (hx + r, hy - .3 * r), (hx + 1.25 * r * f if f > 0 else hx + r, hy + .05 * r),
             (hx + r, hy + .5 * r), (hx + .3 * r, hy + r), (hx - .6 * r, hy + .8 * r)]
    if f < 0:
        face_ = [(2 * hx - px, py) for px, py in face_]
    out += carve(face_, at)
    if head == "feather":                         # a headband and a crown of upright feathers or reeds
        band = [(hx - 1.08 * r, hy - .55 * r), (hx + 1.08 * r, hy - .55 * r), (hx + 1.12 * r, hy - .95 * r), (hx - 1.12 * r, hy - .95 * r)]
        out += carve(band, at, CUT2)
        for k in range(7):
            u = -1 + 2 * k / 6
            bx = hx + u * r * 1.0
            out += cut([(bx, hy - .95 * r), (bx + u * r * .45, hy - 2.5 * r)], at, 2.8)
        out += cut([(hx - 1.5 * r, hy - 2.5 * r), (hx + 1.5 * r, hy - 2.5 * r)], at, 1.6, op=.6, curve=False)
    elif head == "horn":                          # a domed helmet, two horns curving out, a disc between them
        dome = E(hx, hy - .35 * r, 1.12 * r, .95 * r, 16, 180, 360)
        out += carve(dome + [(hx + 1.12 * r, hy - .2 * r), (hx - 1.12 * r, hy - .2 * r)], at, CUT2)
        for sx in (-1, 1):
            out += cut([(hx + sx * .8 * r, hy - .9 * r), (hx + sx * 1.6 * r, hy - 1.5 * r), (hx + sx * 1.75 * r, hy - 2.2 * r)], at, 3.4, curve=True)
        out += carve(E(hx, hy - 1.75 * r, .42 * r, .42 * r, 12), at, CUT2)
        out += cut([(hx, hy - 1.3 * r), (hx, hy - 1.33 * r)], at, 2)
    else:                                         # a plain cap
        out += carve(E(hx, hy - .45 * r, 1.05 * r, .8 * r, 14, 180, 360), at, CUT2)
    if shield:                                    # a round shield held in front
        sx_, sy_ = x + .2 * s * f, y - .3 * s
        out += carve(E(sx_, sy_, .2 * s, .2 * s, 20), at, CUT2)
        out += carve(E(sx_, sy_, .05 * s, .05 * s, 10), at, CUT)
    return out


def sp_ship(cx, wy, L, at=-1, crew=("feather", "feather", "horn", "feather"), face=1, capsized=False, mast=True):
    """A Sea Peoples ship of the relief: a crescent hull with a bird's head on the stem and on the stern, a mast with a crow's nest
    and the sail furled on its yard, warriors behind the rail. wy = the waterline. capsized: the hull upside down."""
    out = []
    flip = (lambda p: [(x, 2 * wy - y + .02 * L) for x, y in p]) if capsized else (lambda p: p)
    rail = wy - .085 * L
    if not capsized:
        if mast:
            out += cut([(cx, rail), (cx, wy - .42 * L)], at, 3.2)
            out += carve([(cx - .035 * L, wy - .42 * L), (cx + .035 * L, wy - .42 * L), (cx + .03 * L, wy - .47 * L), (cx - .03 * L, wy - .47 * L)], at, CUT2)
            yard = [(cx - .3 * L, wy - .38 * L), (cx + .3 * L, wy - .38 * L)]
            out += cut(yard, at, 3)
            sail = [(cx - .29 * L + k * .58 * L / 10, wy - .38 * L + (7 if k % 2 else 15)) for k in range(11)]
            out += cut(sail, at, 3.4, curve=True)
            out += cut([(cx - .28 * L, wy - .38 * L), (cx - .42 * L, rail - 4)], at, 1.4, op=.7)
            out += cut([(cx + .28 * L, wy - .38 * L), (cx + .42 * L, rail - 4)], at, 1.4, op=.7)
        n = len(crew)
        for k, hd in enumerate(crew):
            bx = cx - .28 * L + k * .56 * L / max(1, n - 1)
            out += bust(bx, rail + 6, .2 * L, at, hd, face=(-1 if (k % 2 and face > 0) else face), shield=(k % 2 == 0), spear=(k == 1))
    hull = [(cx - .47 * L, wy - .17 * L), (cx - .42 * L, wy - .02 * L), (cx - .3 * L, wy + .035 * L), (cx + .3 * L, wy + .035 * L), (cx + .42 * L, wy - .02 * L),
            (cx + .47 * L, wy - .17 * L), (cx + .44 * L, wy - .17 * L), (cx + .38 * L, rail), (cx - .38 * L, rail), (cx - .44 * L, wy - .17 * L)]
    out += carve(flip(hull), at, CUT)
    out += cut(flip([(cx - .4 * L, rail + .03 * L), (cx + .4 * L, rail + .03 * L)]), at, 1.6, op=.7)
    heads = []
    for sx in (-1, 1):                            # the bird-head posts, looking outwards
        px = cx + sx * .455 * L
        out += cut(flip([(px, wy - .16 * L), (px + sx * .005 * L, wy - .26 * L)]), at, 4.2)
        hx, hy = px + sx * .012 * L, wy - .285 * L
        head = E(hx, hy, .032 * L, .028 * L, 14)
        beak = [(hx + sx * .025 * L, hy - .012 * L), (hx + sx * .085 * L, hy + .002 * L), (hx + sx * .085 * L, hy + .01 * L), (hx + sx * .025 * L, hy + .016 * L)]
        out += carve(flip(head), at, CUT2) + carve(flip(beak), at, CUT2)
        out += [circ(*flip([(hx + sx * .008 * L, hy - .006 * L)])[0], 2.6, EDGE_D, at=at)]
        heads.append(flip([(hx + sx * .02 * L, hy)])[0])
    return out, heads


def eg_ship(cx, wy, L, at=-1, face=-1, archers=2, oars=9):
    """An Egyptian warship of the relief: a long low hull with a lion's head on the prow, a bank of oars, rowers' heads, archers,
    a mast with a crow's nest. face = the side the prow points to."""
    f = face
    out = []
    rail = wy - .07 * L
    out += cut([(cx, rail), (cx, wy - .4 * L)], at, 3.2)
    out += carve([(cx - .03 * L, wy - .4 * L), (cx + .03 * L, wy - .4 * L), (cx + .025 * L, wy - .45 * L), (cx - .025 * L, wy - .45 * L)], at, CUT2)
    out += cut([(cx - .26 * L, wy - .36 * L), (cx + .26 * L, wy - .36 * L)], at, 3)
    out += cut([(cx - .25 * L + k * .5 * L / 10, wy - .36 * L + (6 if k % 2 else 13)) for k in range(11)], at, 3.2, curve=True)
    for k in range(oars):                         # rowers' heads above the rail
        ox_ = cx - .3 * L + k * .6 * L / (oars - 1)
        out += carve(E(ox_, rail - .03 * L, .018 * L, .02 * L, 10), at, CUT2)
    for k in range(archers):                      # archers standing at bow and stern, bows bent forward
        ax = cx + (.3 if k == 0 else -.33) * L * f
        out += bust(ax, rail, .2 * L, at, "cap", face=f, shield=False)
        bx = ax + .1 * L * f
        out += cut([(bx, rail - .25 * L), (bx + .035 * L * f, rail - .16 * L), (bx, rail - .07 * L)], at, 2.6, curve=True)
        out += cut([(bx, rail - .25 * L), (bx, rail - .07 * L)], at, 1.2, op=.8)
    hull = [(cx - .5 * L * f, wy - .1 * L), (cx - .44 * L * f, wy + .03 * L), (cx + .38 * L * f, wy + .03 * L), (cx + .46 * L * f, wy - .03 * L),
            (cx + .47 * L * f, rail), (cx - .48 * L * f, rail - .02 * L)]
    out += carve(hull, at, CUT)
    out += cut([(cx - .44 * L * f, rail + .025 * L), (cx + .42 * L * f, rail + .025 * L)], at, 1.6, op=.7)
    for k in range(oars):                         # the oars, across the hull and down into the water
        ox_ = cx - .3 * L + k * .6 * L / (oars - 1)
        out += cut([(ox_ + .02 * L * f, rail - .015 * L), (ox_ - .07 * L * f, wy + .1 * L)], at, 2.8)
    # the lion's head on the prow
    px, py = cx + .47 * L * f, rail - .04 * L
    mane = E(px, py, .05 * L, .055 * L, 16)
    out += carve(mane, at, CUT2)
    snout = [(px + .03 * L * f, py - .02 * L), (px + .085 * L * f, py - .005 * L), (px + .085 * L * f, py + .02 * L), (px + .03 * L * f, py + .035 * L)]
    out += carve(snout, at, CUT2)
    out += cut([(px - .01 * L * f, py - .045 * L), (px + .015 * L * f, py - .07 * L)], at, 3)
    out += [circ(px + .045 * L * f, py - .006 * L, 2.6, EDGE_D, at=at)]
    return out, (px + .06 * L * f, py)


def pharaoh(x, y, h, at=-1):
    """The pharaoh drawn huge in Egyptian profile, facing left, drawing his bow: the blue crown, broad shoulders, a pleated kilt
    with its apron, legs in stride, the quiver on his back. Feet on y. Returns (elements, bow hand, arrow tip)."""
    P = lambda u, v: (x + u * h, y - v * h)
    out = []
    # quiver behind the back
    out += carve([P(.07, .79), P(.12, .81), P(.2, .55), P(.15, .53)], at, CUT2)
    # back leg and front leg (both feet point forward, to the left)
    out += limb([P(.045, .34), P(.075, .045), P(.012, .0)], .045 * h, at)
    out += limb([P(-.01, .34), P(-.085, .045), P(-.165, .0)], .048 * h, at)
    # kilt with the projecting apron
    out += carve([P(-.05, .56), P(.07, .56), P(.085, .44), P(.075, .33), P(-.02, .33), P(-.13, .36), P(-.075, .5)], at, CUT2)
    for k in range(4):
        out += cut([P(-.03 + k * .025, .55), P(-.07 + k * .03, .37)], at, 1.4, op=.6)
    out += carve([P(-.055, .575), P(.075, .575), P(.07, .545), P(-.05, .545)], at, CUT)
    # torso, shoulders square to us
    out += carve([P(-.02, .81), P(.03, .815), P(.115, .785), P(.12, .755), P(.085, .66), P(.07, .575), P(-.05, .575), P(-.06, .66), P(-.1, .76), P(-.095, .785)], at)
    out += cut([P(-.085, .765), P(-.02, .735), P(.05, .735), P(.105, .765)], at, 2.4, curve=True)
    out += cut([P(-.075, .745), P(-.01, .705), P(.04, .705), P(.095, .745)], at, 1.6, curve=True, op=.7)
    # the bow arm, straight out to the left; the drawing arm bent back to the cheek
    hand = P(-.33, .755)
    out += limb([P(-.085, .77), P(-.21, .762), hand], .04 * h, at)
    out += limb([P(.1, .775), P(.175, .79), P(.06, .8), P(-.015, .8)], .034 * h, at)
    out += carve(E(hand[0], hand[1], .022 * h, .03 * h, 12), at, CUT2)
    # head in profile under the blue crown (with the rearing cobra at its brow)
    out += carve([P(-.05, .878), P(-.058, .862), P(-.078, .85), P(-.062, .842), P(-.064, .834), P(-.056, .826), P(-.05, .814), P(-.03, .806), P(-.005, .806), P(.022, .812),
                  P(.034, .84), P(.04, .872)], at)
    crown = [P(-.05, .875), P(-.057, .92), P(-.045, .97), P(-.012, 1.012), P(.04, 1.032), P(.085, 1.018), P(.112, .978), P(.118, .93), P(.104, .893), P(.075, .874)]
    out += carve(crown, at, CROWN, curve=True)
    out += cut([P(-.05, .893), P(.105, .9)], at, 2.2, op=.8)
    for k in range(9):
        u, v = -.028 + (k % 3) * .045 + (k // 3 % 2) * .02, .93 + (k // 3) * .03
        out += [circ(P(u, v)[0], P(0, v)[1], 2.4, "#cfd8e3", at=at, op=.5)]
    out += cut([P(-.058, .9), P(-.075, .925), P(-.066, .945)], at, 3, curve=True)
    out += [circ(P(-.038, .856)[0], P(0, .856)[1], 3.4, EDGE_D, at=at)]
    out += cut([P(-.05, .862), P(-.022, .861)], at, 1.6, op=.8)
    out += cut([P(-.03, .84), P(.0, .826)], at, 1.4, op=.6)
    # the bow, its string drawn to the cheek, the arrow
    top, bot = P(-.3, 1.03), P(-.3, .47)
    bow = [top, P(-.345, .9), P(-.365, .755), P(-.345, .6), bot]
    out += cut(bow, at, 4.4, curve=True)
    nock = P(-.02, .8)
    out += cut([top, nock, bot], at, 1.5, op=.9)
    tip = P(-.43, .772)
    out += cut([nock, tip], at, 2.2)
    out += carve([tip, (tip[0] + .02 * h, tip[1] - .01 * h), (tip[0] + .02 * h, tip[1] + .01 * h)], at, CUT2)
    return out, hand, tip


def arrow_fly(p0, p1, at=-1, w=2.2):
    """An arrow in flight: a cut shaft and a little head, from p0 to p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    head = [p1, (p1[0] - 12 * ux + 5 * uy, p1[1] - 12 * uy - 5 * ux), (p1[0] - 12 * ux - 5 * uy, p1[1] - 12 * uy + 5 * ux)]
    return cut([p0, p1], at, w) + carve(head, at, CUT2, 1.4)


def cart(x, y, s, at=-1, people=(("woman", 0), ("child", 1))):
    """A two-wheeled ox cart of the land-battle relief: a box on solid wheels, a pair of humped oxen yoked in front (to the left),
    women and children standing in the box. s = the cart's length."""
    out = []
    # oxen (two, slightly offset), humped, facing left
    for k, dx in enumerate((0, .08 * s)):
        ox, oy = x - .62 * s + dx, y
        body = [(ox - .32 * s, oy - .32 * s), (ox - .28 * s, oy - .44 * s), (ox - .12 * s, oy - .47 * s), (ox - .05 * s, oy - .56 * s), (ox + .04 * s, oy - .47 * s),
                (ox + .22 * s, oy - .46 * s), (ox + .27 * s, oy - .34 * s), (ox + .25 * s, oy - .22 * s), (ox + .22 * s, oy), (ox + .18 * s, oy), (ox + .16 * s, oy - .2 * s),
                (ox - .15 * s, oy - .2 * s), (ox - .18 * s, oy), (ox - .22 * s, oy), (ox - .24 * s, oy - .24 * s)]
        head = [(ox - .3 * s, oy - .42 * s), (ox - .45 * s, oy - .38 * s), (ox - .48 * s, oy - .28 * s), (ox - .4 * s, oy - .26 * s), (ox - .3 * s, oy - .3 * s)]
        out += carve(body, at, CUT if k else CUT2) + carve(head, at, CUT if k else CUT2)
        out += cut([(ox - .36 * s, oy - .42 * s), (ox - .32 * s, oy - .54 * s), (ox - .4 * s, oy - .58 * s)], at, 2.6, curve=True)
    # the pole and yoke
    out += cut([(x - .35 * s, y - .3 * s), (x - .84 * s, y - .46 * s)], at, 3)
    # the cart box with people standing in it: women in long headscarves, children beside them
    for name, k in people:
        px = x - .12 * s + k * .2 * s
        hh = .6 * s if name == "woman" else .38 * s
        by = y - .3 * s
        sh = by - hh * .62
        out += carve([(px - .1 * hh, by), (px - .17 * hh, sh + .05 * hh), (px - .1 * hh, sh - .02 * hh), (px + .1 * hh, sh - .02 * hh), (px + .17 * hh, sh + .05 * hh),
                      (px + .1 * hh, by)], at)
        hx, hy = px + .02 * hh, sh - .14 * hh
        out += carve([(hx - .09 * hh, hy - .04 * hh), (hx - .06 * hh, hy - .1 * hh), (hx + .04 * hh, hy - .11 * hh), (hx + .1 * hh, hy - .03 * hh), (hx + .13 * hh, hy + .01 * hh),
                      (hx + .1 * hh, hy + .04 * hh), (hx + .09 * hh, hy + .09 * hh), (hx - .02 * hh, hy + .12 * hh), (hx - .08 * hh, hy + .08 * hh)], at)
        if name == "woman":                        # the headscarf falling to the shoulders
            out += carve([(hx - .1 * hh, hy - .02 * hh), (hx - .05 * hh, hy - .13 * hh), (hx + .06 * hh, hy - .14 * hh), (hx + .09 * hh, hy - .07 * hh), (hx - .02 * hh, hy - .06 * hh),
                          (hx - .08 * hh, hy + .1 * hh), (hx - .16 * hh, sh + .12 * hh), (hx - .2 * hh, sh + .1 * hh)], at, CUT2)
    out += carve([(x - .3 * s, y - .32 * s), (x + .3 * s, y - .32 * s), (x + .3 * s, y - .12 * s), (x - .3 * s, y - .12 * s)], at, CUT2)
    for k in range(5):
        out += cut([(x - .3 * s + k * .15 * s, y - .32 * s), (x - .3 * s + k * .15 * s, y - .12 * s)], at, 1.4, op=.7)
    for wx in (x - .14 * s, x + .14 * s):        # solid wheels
        out += carve(E(wx, y - .1 * s, .1 * s, .1 * s, 18), at, CUT2)
        out += carve(E(wx, y - .1 * s, .025 * s, .025 * s, 8), at, CUT)
    return out


# ================================================================== maps
EM = View(19, 41, 29.5, 42.5, (90, 120, 1600, 680))          # the eastern Mediterranean, Greece to Syria


def P(v, lon, lat):
    return v.p(lon, lat)


SITES = {"Mycenae": (22.756, 37.731), "Tiryns": (22.800, 37.599), "Pylos": (21.698, 37.028), "Hattusa": (34.615, 40.020), "Ugarit": (35.785, 35.602),
         "Gibala": (35.940, 35.370), "Enkomi": (33.880, 35.150), "Kition": (33.630, 34.920), "Carchemish": (38.013, 36.830), "Ashkelon": (34.551, 31.664),
         "Medinet Habu": (32.601, 25.720), "Gordion": (31.990, 39.650), "Midea": (22.840, 37.649), "Uluburun": (29.683, 36.130), "Galilee": (35.590, 32.820),
         "Larnaca": (33.620, 34.900), "Thebes": (32.640, 25.700), "Babylon": (44.420, 32.540), "Assur": (43.260, 35.460), "Gaza": (34.466, 31.502),
         "Ashdod": (34.655, 31.754), "Ekron": (34.851, 31.778), "Gath": (34.849, 31.700), "Lycia": (29.6, 36.6), "Sardinia": (9.0, 40.1), "Sicily": (14.2, 37.5)}


def map_base(v, at=-1, landc="#3d3226", night=False):
    """The land of a View; at night the land is darker and the sea (base param "sea") nearly black."""
    return [{"k": "map", "land": v.land(), "landc": "#2e261d" if night else landc, "in": at}]


def site(v, name):
    return v.p(*SITES[name])


# ================================================================== cold open
def s1():
    """HERO (fully drawn from frame 0): the sea battle carved at Medinet Habu, in raking light. The pharaoh drawn huge at the
    right, bow bent; three Sea Peoples ships (bird's heads at both ends, feathered crowns and horned helmets), one capsized; a
    rowed Egyptian ship with a lion's head on the prow; arrows in flight; zigzag water. Highlights follow the words."""
    sid = "s1"
    t_bird, t_crown = T(sid, "Strange ships"), T(sid, "Warriors in feathered")
    els = wall_bg()
    els += hiero(70, 128, 15, 66, 3, 60, seed=7, op=.6)          # text columns along the top (behind the hook title)
    els += cut([(60, 322), (1180, 322)], -1, 3)                 # the register line over the battle
    els += cut([(1180, 322), (1180, 800)], -1, 2, op=.5)
    els += water(70, 1170, 575, 8, 27)                           # the sea, under the ships
    AX, AY, AL = 300, 505, 380
    shipA, headsA = sp_ship(AX, AY, AL, -1, ("feather", "feather", "horn", "feather"))
    shipC, _ = sp_ship(705, 572, 280, -1, (), capsized=True)
    shipB, headsB = sp_ship(320, 742, 370, -1, ("horn", "feather", "horn"))
    shipD, prow = eg_ship(935, 742, 430, -1, face=-1)
    els += shipA + shipB + shipC
    els += [rect(575, 604, 260, 62, WALL, at=-1, op=.6)] + water(565, 845, 606, 3, 26)
    els += shipD
    # two warriors tumbling from the capsized ship
    els += [{"k": "group", "tr": "rotate(-38 588 566)", "els": bust(588, 566, 58, -1, "feather", face=-1, shield=False), "in": -1},
            {"k": "group", "tr": "rotate(34 826 560)", "els": bust(826, 560, 54, -1, "horn", face=1, shield=False), "in": -1}]
    # the grappling hook from the Egyptian ship to the enemy's rail
    gx, gy = 505, 707
    els += cut([(prow[0] - 6, prow[1] - 24), ((prow[0] + gx) / 2, gy - 34), (gx, gy)], -1, 1.8, curve=True)
    els += cut([(gx + 10, gy - 12), (gx, gy), (gx + 12, gy + 10)], -1, 2.6)
    # the pharaoh and his arrows
    ph, hand, tip = pharaoh(1510, 800, 560)
    els += cut([(1190, 800), (1700, 800)], -1, 3)
    els += ph
    for (a, b) in [((1180, 470), (1100, 480)), ((1030, 430), (950, 445)), ((760, 410), (690, 428)), ((1120, 540), (1040, 552)), ((640, 470), (575, 490))]:
        els += arrow_fly(a, b)
    els += [glow(1450, 420, 420, -1, .12, "lamp")]
    # the words: the bird heads, then a feathered crown and a horned helmet
    for k, (hx, hy) in enumerate(headsA):
        els += [ring(round(hx, 1), round(hy, 1), 34, round(t_bird + .5 + .35 * k, 2), GOLD, 3.5, dur=.6), glow(round(hx, 1), round(hy, 1), 70, round(t_bird + .5 + .35 * k, 2), .55)]
    for k, dt in ((0, .3), (2, 1.1)):                            # a feathered crown, then a horned helmet, on ship A
        bx = AX - .28 * AL + k * .56 * AL / 3
        hy = AY - .085 * AL + 6 - .72 * .2 * AL - 14
        els += [glow(round(bx, 1), round(hy, 1), 70, round(t_crown + dt, 2), .65), ring(round(bx, 1), round(hy, 1), 34, round(t_crown + dt, 2), GOLD, 3, dur=.6)]
    return {"base": "dark", "cam": CAM, "els": els}


def s2():
    """Night map of the eastern Mediterranean: small fires at Pylos, Tiryns and on Cyprus first, then Mycenae, Hattusa, Ugarit
    flare as they are tolled. Three labels."""
    sid = "s2"
    t_my, t_ha, t_ug = T(sid, "Mycenae"), T(sid, "The Hittite capital"), T(sid, "The great port")
    v = EM
    els = map_base(v, night=True)
    for k, nm in enumerate(("Pylos", "Tiryns", "Enkomi")):
        x, y = site(v, nm)
        els += flame(x, y, 20, .8 + .5 * k, .85)
    for nm, t, a in (("Mycenae", t_my, "end"), ("Hattusa", t_ha, "start"), ("Ugarit", t_ug, "start")):
        x, y = site(v, nm)
        els += flame(x, y, 40, t - .15)
        els.append(lab(x + (-38 if a == "end" else 38), y + 12, nm, t + .1, GOLD, 34, a))
    els += [lab(*v.p(26.5, 34.4), "Mediterranean", .2, "#9fd0ff", 26, st="ital"), lab(*v.p(24.5, 39.2), "Greece", .4, DIM, 24, st="ital"),
            lab(*v.p(37.5, 34.2), "Syria", .5, DIM, 24, st="ital")]
    return {"base": "map", "sea": "#0b1822", "cam": CAM, "els": els}


def lamp_room(at=-1, win=(1000, 170, 600, 420)):
    """A dark room with a table and a window on the sea at dusk."""
    wx, wy, ww, wh = win
    els = [rect(-20, -20, W_ + 40, H_ + 40, "#140e0a", at=at),
           rect(wx - 14, wy - 14, ww + 28, wh + 28, "#3a2a1c", "#6b5236", 3, 8, at),
           rect(wx, wy, ww, wh * .42, "#2e3350", at=at), rect(wx, wy + wh * .42, ww, wh * .2, "#9a5a44", at=at, op=.8),
           rect(wx, wy + wh * .62, ww, wh * .38, "#13304a", at=at)]
    els += [ln([(wx, wy + wh * .62), (wx + ww, wy + wh * .62)], at, "#f0b27a", 2.4, draw=False, op=.7), ln([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], at, "#3a2a1c", 12, draw=False),
            glow(wx + ww * .8, wy + wh * .58, 140, at, .45, "sun")]
    els += [rect(60, 660, 1660, 60, "#4d3626", "#7a5a3a", 2, 4, at), rect(60, 718, 1660, 140, "#24180f", at=at)]
    return els


def big_tablet(x, y, w, h, at, seed=4, rows=9, per=8):
    """A large clay letter lit by a lamp: a cushion of fired clay with a raised rim, lines of cuneiform signs (2 to 4 wedges each)."""
    out = [rect(x + 14, y + 18, w, h, "rgba(0,0,0,.55)", r=w * .14, at=at),
           rect(x, y, w, h, "#b9875a", "#e7c597", 3, w * .14, at),
           rect(x + 10, y + 10, w - 20, h - 20, "#c89664", r=w * .1, at=at, op=.7)]
    rr = random.Random(seed)
    rh = (h - 70) / rows
    for r in range(rows):
        yb = y + 36 + r * rh
        out.append(ln([(x + 26, yb + rh - 3), (x + w - 26, yb + rh - 3)], at, "#8a5e38", 1.2, draw=False, op=.45))
        cx = x + 32
        while cx < x + w - 48:
            sw = rr.choice((18, 24, 30))
            for m in range(rr.choice((2, 3, 3, 4))):
                px, py = cx + rr.uniform(0, sw - 12), yb + rr.uniform(3, rh - 22)
                if rr.random() < .62:
                    out.append(poly([(px, py), (px + 13, py - 5), (px + 13, py + 5)], "#4a2e18", at=at))
                else:
                    out.append(poly([(px, py), (px - 5, py + 13), (px + 5, py + 13)], "#4a2e18", at=at))
            cx += sw + rr.uniform(6, 12)
    return out


def s3():
    """Lamplight on a clay letter on a table; through the window a dusk sea where dark ships slide in from the left, and fire
    rises on the shore at 'burned'."""
    sid = "s3"
    t_ships, t_burn = T(sid, "The enemy's ships"), T(sid, "My cities")
    els = lamp_room()
    els += big_tablet(330, 250, 400, 440, -1)
    els += [glow(230, 600, 320, -1, .75, "lamp"), poly([(205, 660), (215, 630), (262, 628), (275, 645), (255, 660)], "#c88b4a", "#f0c08a", 1.5, -1),
            poly([(256, 628), (262, 600), (268, 628)], "#ffe2a8", at=-1, curve=True)]
    for k in range(4):
        x = 1060 + 125 * k
        els += ship_icon(x, 448 + 6 * (k % 2), 78, t_ships + .3 + .45 * k, "#0c0a0a", 1)
    els += [poly([(1000, 432), (1150, 418), (1300, 430), (1600, 424), (1600, 440), (1000, 440)], "#1e1a17", at=-1)]
    els += flame(1120, 424, 30, t_burn + .2) + flame(1370, 427, 36, t_burn + .6) + flame(1530, 425, 24, t_burn + 1.0)
    return {"base": "dark", "cam": CAM, "els": els}


SIX = ["ship", "drought", "hunger", "quake", "trade", "revolt"]


def icon(kind, x, y, s, at, c=BONE, op=None, fx="pop"):
    """The six suspects as small pictures (no words): a ship, a sun over cracked earth, an empty jar, a cracked wall, an ingot, a fist."""
    out = []
    if kind == "ship":
        out += ship_icon(x, y + .3 * s, s, at, c, op=op)
    elif kind == "drought":
        out += [circ(x, y - .25 * s, .2 * s, "none", c, 3, at, fx, op)]
        for k in range(8):
            a = k * math.pi / 4
            out.append(ln([(x + .28 * s * math.cos(a), y - .25 * s + .28 * s * math.sin(a)), (x + .38 * s * math.cos(a), y - .25 * s + .38 * s * math.sin(a))], at, c, 3, draw=False, op=op))
        out += [ln([(x - .45 * s, y + .25 * s), (x + .45 * s, y + .25 * s)], at, c, 3, draw=False, op=op),
                ln([(x - .2 * s, y + .25 * s), (x - .12 * s, y + .38 * s), (x - .18 * s, y + .48 * s)], at, c, 2, draw=False, op=op),
                ln([(x + .15 * s, y + .25 * s), (x + .22 * s, y + .4 * s)], at, c, 2, draw=False, op=op)]
    elif kind == "hunger":
        w = .55 * s
        out += [poly([(x - .14 * w, y - .5 * s), (x - .5 * w, y - .25 * s), (x - .5 * w, y + .2 * s), (x - .15 * w, y + .45 * s), (x + .15 * w, y + .45 * s),
                      (x + .5 * w, y + .2 * s), (x + .5 * w, y - .25 * s), (x + .14 * w, y - .5 * s)], "none", c, 3, at, fx, op, curve=True)]
    elif kind == "quake":
        out += [rect(x - .45 * s, y - .4 * s, .9 * s, .8 * s, "none", c, 3, 2, at, fx, op),
                ln([(x - .05 * s, y - .4 * s), (x + .08 * s, y - .15 * s), (x - .06 * s, y + .05 * s), (x + .1 * s, y + .4 * s)], at, c, 3, draw=False, op=op),
                ln([(x - .45 * s, y), (x - .05 * s, y)], at, c, 1.5, draw=False, op=op), ln([(x + .05 * s, y - .2 * s), (x + .45 * s, y - .2 * s)], at, c, 1.5, draw=False, op=op)]
    elif kind == "trade":
        e = ingot(x, y, s * .95, at, "none", fx, op)
        e["c"], e["w"] = c, 3
        out.append(e)
    elif kind == "revolt":
        out += [rect(x - .25 * s, y - .25 * s, .5 * s, .55 * s, "none", c, 3, .12 * s, at, fx, op)]
        for k in range(4):
            out.append(ln([(x - .25 * s + k * .125 * s + .06 * s, y - .25 * s), (x - .25 * s + k * .125 * s + .06 * s, y - .08 * s)], at, c, 2, draw=False, op=op))
        out += [ln([(x - .1 * s, y + .3 * s), (x - .1 * s, y + .5 * s)], at, c, 3, draw=False, op=op), ln([(x + .1 * s, y + .3 * s), (x + .1 * s, y + .5 * s)], at, c, 3, draw=False, op=op)]
    return out


def s4():
    """The question: the night map, dimmer and wider; the six suspects pop round the sea as small pictures, a lilac question mark
    glows over it. No labels. (The title beat holds here under the intro card.)"""
    sid = "s4"
    v = View(17, 43, 28.5, 43.0, (90, 120, 1600, 680))
    els = map_base(v, night=True)
    for nm in ("Mycenae", "Hattusa", "Ugarit", "Pylos", "Enkomi"):
        x, y = site(v, nm)
        els += flame(x, y, 24, -1, .8)
    pos = [(330, 240), (1450, 240), (1580, 520), (1180, 690), (560, 690), (210, 500)]
    for k, (kind, (x, y)) in enumerate(zip(SIX, pos)):
        els += [circ(x, y, 74, "rgba(18,13,10,.8)", "rgba(255,236,206,.45)", 2.5, .3 + .25 * k, "pop")] + icon(kind, x, y, 84, .4 + .25 * k, BONE)
    els += qm(889, 500, .2, 170)
    return {"base": "map", "sea": "#0b1822", "cam": CAM, "els": els}


# ================================================================== 1 Raiders from the sea
EGV = View(24, 40, 24.3, 37.2, (90, 120, 1600, 680))         # Egypt and the Levant


def cart_icon(x, y, s, at, c=AMBER, op=None):
    """A small two-wheeled ox cart for maps (line drawing)."""
    return [rect(x - .3 * s, y - .35 * s, .6 * s, .25 * s, "none", c, 2.5, 2, at, "pop", op),
            circ(x - .15 * s, y - .05 * s, .1 * s, "none", c, 2.5, at, "pop", op), circ(x + .15 * s, y - .05 * s, .1 * s, "none", c, 2.5, at, "pop", op),
            ln([(x - .3 * s, y - .25 * s), (x - .62 * s, y - .32 * s)], at, c, 2.5, draw=False, op=op),
            poly([(x - .95 * s, y - .3 * s), (x - .62 * s, y - .42 * s), (x - .58 * s, y - .2 * s), (x - .9 * s, y - .12 * s)], c, at=at, fx="pop", op=op)]


def s6():
    """Egypt and the Levant: the Nile, Medinet Habu at Thebes (gold); Egypt's account of the invaders drawn dotted (claimed): one
    arrow down the Levant coast with an ox cart (by land), one across the sea with ships to the delta mouths (by sea)."""
    sid = "s6"
    t_mh, t_land, t_sea = T(sid, "Ramesses"), T(sid, "by land"), T(sid, "and by sea")
    v = EGV
    els = map_base(v)
    nile = [v.p(32.65, 25.4), v.p(32.75, 26.3), v.p(32.2, 26.9), v.p(31.4, 27.6), v.p(31.0, 28.6), v.p(31.25, 29.6), v.p(31.2, 30.1)]
    els += [ln(nile, -1, "#6fb6d6", 4, curve=True, draw=False), ln([v.p(31.2, 30.1), v.p(30.7, 30.8), v.p(30.4, 31.45)], -1, "#6fb6d6", 3, curve=True, draw=False),
            ln([v.p(31.2, 30.1), v.p(31.5, 30.8), v.p(31.8, 31.5)], -1, "#6fb6d6", 3, curve=True, draw=False),
            lab(*v.p(30.3, 28.0), "Nile", .4, "#9fd0ff", 26, st="ital")]
    mx, my = site(v, "Medinet Habu")
    els += [{"k": "pin", "x": mx, "y": my, "t": "Medinet Habu", "c": GOLD, "in": t_mh, "a": "start", "lx": 22}, glow(mx, my, 70, t_mh, .6)]
    land = [v.p(36.4, 36.3), v.p(35.9, 34.6), v.p(35.2, 33.0), v.p(34.2, 31.6), v.p(32.6, 31.0)]
    els += [arr(land, t_land, AMBER, 4, "claimed", 1.8, True), lab(*v.p(37.6, 33.2), "by land", t_land + .7, AMBER, 32)]
    els += cart_icon(*v.p(36.25, 32.6), 64, t_land + 1.0)
    sea = [v.p(25.6, 35.7), v.p(27.6, 34.0), v.p(29.6, 32.4), v.p(31.2, 31.75)]
    els += [arr(sea, t_sea, BLUE, 4, "claimed", 1.8, True), lab(*v.p(26.4, 33.0), "by sea", t_sea + .7, BLUE, 32)]
    for k, (lo, la) in enumerate(((26.6, 35.1), (28.2, 33.85))):
        els += ship_icon(*v.p(lo, la), 46, t_sea + .9 + .3 * k, BLUE)
    return {"base": "map", "cam": CAM, "els": els}


def walker(x, y, s, at=-1, head="feather", face=1, shield=True, spear=False):
    """A whole warrior of the relief walking (feet on y, s = height): legs in stride, a kilt, the bust above."""
    f = face
    out = limb([(x - .02 * s * f, y - .48 * s), (x - .14 * s * f, y - .02 * s), (x - .2 * s * f, y)], .055 * s, at)
    out += limb([(x + .03 * s * f, y - .48 * s), (x + .13 * s * f, y - .02 * s), (x + .2 * s * f, y)], .055 * s, at)
    out += carve([(x - .1 * s, y - .62 * s), (x + .1 * s, y - .62 * s), (x + .13 * s, y - .42 * s), (x - .13 * s, y - .42 * s)], at, CUT2)
    out += bust(x, y - .6 * s, .45 * s, at, head, face, shield, spear)
    return out


def s7():
    """The land-battle relief in carved sandstone: two ox carts on solid wheels, each pulled by a pair of humped oxen, women and
    children standing in them, warriors in feathered crowns walking beside; a light settles on a mother and child."""
    sid = "s7"
    t_fam = T(sid, "families on the")
    els = wall_bg(seed=8)
    els += cut([(60, 210), (1720, 210)], -1, 3) + cut([(60, 770), (1720, 770)], -1, 3)
    els += hiero(80, 122, 25, 64, 1, 80, seed=11, op=.45)
    els += cart(660, 760, 430, .2, (("woman", 0), ("child", 1.1)))
    els += cart(1360, 760, 430, .9, (("woman", 0), ("woman", 1), ("child", 2.0)))
    els += walker(140, 760, 300, .5, "feather", 1, True, True) + walker(860, 760, 290, 1.2, "feather", 1, True, True) + walker(1640, 760, 300, 1.6, "horn", -1, True, False)
    els += [glow(660 - .12 * 430, 760 - .3 * 430 - .45 * 430, 150, t_fam, .55), glow(1360 + .2 * 430, 760 - .55 * 430, 130, t_fam + .5, .45)]
    return {"base": "dark", "cam": CAM, "els": els}


def s8():
    """The sea battle closer: an Egyptian ship rowing in from the left, archers loosing; a Sea Peoples ship heeling under a grappling
    hook; another tipping over at the right, half under the water; arrows fly as said, the rope draws, a ring at 'tip ... over'."""
    sid = "s8"
    t_arch, t_hook, t_tip = T(sid, "packed with archers"), T(sid, "Sailors throw"), T(sid, "tip the enemy")
    els = wall_bg(seed=9)
    els += water(60, 1720, 640, 7, 26)
    egy, prow = eg_ship(470, 670, 680, -1, face=1, archers=2, oars=11)
    els += egy
    en, _ = sp_ship(1130, 650, 480, -1, ("feather", "horn", "feather", "feather"))
    els += [{"k": "group", "tr": "rotate(-14 1130 650)", "els": en, "in": -1}]
    cap, _ = sp_ship(1505, 690, 340, -1, ("feather", "horn", "feather"))
    els += [{"k": "group", "tr": "rotate(150 1505 660)", "els": cap, "in": -1}]
    els += water(1330, 1720, 716, 3, 26)
    for k, (a, b) in enumerate([((640, 440), (860, 400)), ((660, 480), (900, 470)), ((250, 430), (470, 345)), ((560, 410), (790, 350))]):
        els += [{"k": "group", "els": arrow_fly(a, b), "in": round(t_arch + .35 * k, 2)}]
    rope = [(prow[0] - 20, prow[1] - 50), (900, 500), (946, 640)]
    els += [ln(rope, t_hook, EDGE_D, 2.8, curve=True, dur=.8), ln([(934, 628), (946, 640), (958, 626)], t_hook + .8, EDGE_D, 3.6, dur=.3)]
    els += [glow(1505, 640, 200, t_tip, .45, "lamp"), ring(1505, 640, 160, t_tip + .2, GOLD, 3, dur=.8)]
    return {"base": "dark", "cam": CAM, "els": els}


def pylon(cx, gy, at, h=430):
    """The first pylon of Medinet Habu: two battered towers with a cornice and torus, a gateway between them, flagstaff grooves,
    and on each tower the king carved huge, arm raised (the smiting scene)."""
    out = []
    tw, gw = 470, 170
    for sx in (-1, 1):
        x0 = cx + sx * gw / 2
        x1 = cx + sx * (gw / 2 + tw)
        lo, hi = (x0, x1) if sx > 0 else (x1, x0)
        bat = 34
        top_lo, top_hi = (lo, hi - bat) if sx > 0 else (lo + bat, hi)
        out.append(poly([(lo, gy), (hi, gy), (top_hi, gy - h), (top_lo, gy - h)], "#c9a878", "#f2dcb4", 2, at, "rise"))
        out.append(poly([(top_lo - 8, gy - h), (top_hi + 8, gy - h), (top_hi + 14, gy - h - 30), (top_lo - 14, gy - h - 30)], "#b8946a", "#f2dcb4", 1.5, at + .1, "rise"))
        for k in range(2):                         # flagstaff grooves
            gx = (lo + 60 + k * 70) if sx > 0 else (hi - 60 - k * 70)
            out.append(rect(gx - 9, gy - h + 12, 18, h - 12, "#9a7a52", at=at + .2, op=.7))
        # the smiting king, carved (a giant figure with the mace raised), facing the gate
        kx = (lo + hi) / 2 + sx * 30
        f = -sx
        fig = [(kx - 30, gy - 40), (kx - 34, gy - 210), (kx - 46, gy - 260), (kx - 20, gy - 290), (kx + 20, gy - 290), (kx + 44, gy - 260), (kx + 32, gy - 210), (kx + 28, gy - 40)]
        out.append(poly(fig, "none", "#6b5032", 3, at + .6, op=.85))
        out.append(poly(E(kx + 4 * f, gy - 312, 18, 22, 14), "none", "#6b5032", 3, at + .6, op=.85))
        out.append(ln([(kx - 40 * f, gy - 270), (kx - 70 * f, gy - 340), (kx - 60 * f, gy - 368)], at + .7, "#6b5032", 4, draw=False, op=.85))
        out.append(poly(E(kx - 60 * f, gy - 378, 12, 12, 10), "#6b5032", at=at + .7, op=.85))
        for j in range(3):                         # the enemies he grips, small and kneeling
            ex = kx + (60 + 34 * j) * f
            out.append(poly([(ex - 14, gy - 60), (ex + 14, gy - 60), (ex + 10, gy - 130), (ex - 10, gy - 130)], "none", "#6b5032", 2, at + .8, op=.7))
            out.append(poly(E(ex, gy - 145, 12, 14, 10), "none", "#6b5032", 2, at + .8, op=.7))
    out.append(rect(cx - gw / 2 + 20, gy - 250, gw - 40, 250, "#2b2016", at=at + .2))
    out.append(rect(cx - gw / 2 + 6, gy - 290, gw - 12, 40, "#c9a878", "#f2dcb4", 1.5, 0, at + .2))
    return out


def s9():
    """Dawn at Medinet Habu: the temple's first pylon in elevation (two battered towers, a gateway, flagstaff grooves), the king
    carved huge on each tower; the long outer wall with bands of battle scenes runs off to the right; two visitors for scale."""
    sid = "s9"
    gy = 745
    els = [rect(1380, gy - 300, 500, 300, "#bb9a6e", "#f2dcb4", 2, 0, .2, "rise")]
    for k in range(3):
        els.append(ln([(1395, gy - 250 + 80 * k), (1790, gy - 250 + 80 * k)], .9 + .2 * k, "#7a5c3c", 2, draw=False, op=.7))
        for j in range(10):
            els.append(ln([(1400 + 38 * j, gy - 230 + 80 * k), (1418 + 38 * j, gy - 200 + 80 * k)], 1.0 + .2 * k, "#6b5032", 2.5, draw=False, op=.6))
    els += pylon(760, gy, .3)
    els += [figure(700, gy, 36, 1.4, "#2a1f17"), figure(735, gy, 33, 1.5, "#2a1f17")]
    els += [lab(760, gy - 500, "Medinet Habu", .8, GOLD, 34, st="serif")]
    return {"base": "sky", "tod": "dawn", "ground": gy, "sun": [180, 380, 40], "cam": CAM, "els": els}


CLV = View(25, 42, 28.8, 41.8, (90, 120, 1600, 680))


def s10():
    """Egypt's boast drawn in the claimed (dotted) style: from Egypt, dotted lilac lines fan out to Hatti, Cyprus and Carchemish, each
    ringed and crossed as named. At 'winner's version' Carchemish turns solid green with a small crown: its kings ruled on."""
    sid = "s10"
    t_q, t_ha, t_cy, t_ca, t_win, t_on = (T(sid, "No land"), T(sid, "the Hittites"), T(sid, "Cyprus and"), T(sid, "Carchemish"), T(sid, "winner's version"),
                                          T(sid, "the kings ruled"))
    v = CLV
    els = map_base(v)
    ex, ey = v.p(31.0, 30.2)
    els += [{"k": "pin", "x": ex, "y": ey, "t": "Egypt", "c": GOLD, "in": .3, "a": "start", "lx": 20}, lab(ex, ey - 420, "Egypt's claim", t_q, LILAC, 32, st="ital")]
    for nm, (lo, la), t in (("Hatti", (33.6, 39.6), t_ha), ("Cyprus", (33.1, 35.05), t_cy), ("Carchemish", (38.0, 36.83), t_ca)):
        x, y = v.p(lo, la)
        els += [ln([(ex, ey - 8), ((ex + x) / 2 - 30, (ey + y) / 2), (x, y + 30)], t - .2, LILAC, 2.5, "claimed", .8, curve=True),
                circ(x, y, 34, "rgba(201,193,238,.12)", LILAC, 3, t, "pop", style="claimed"),
                ln([(x - 16, y - 16), (x + 16, y + 16)], t + .3, LILAC, 4, dur=.3), ln([(x + 16, y - 16), (x - 16, y + 16)], t + .45, LILAC, 4, dur=.3),
                lab(x + 50, y + 10, nm, t + .1, BONE, 30, "start")]
    cx, cy = v.p(38.0, 36.83)
    els += [circ(cx, cy, 36, "#2f4a3a", GREEN, 4, t_win + .4, "pop"),
            poly([(cx - 22, cy - 46), (cx - 22, cy - 66), (cx - 11, cy - 56), (cx, cy - 70), (cx + 11, cy - 56), (cx + 22, cy - 66), (cx + 22, cy - 46)], GOLD, at=t_on - .2, fx="pop"),
            lab(cx + 50, cy + 46, "ruled on", t_on, GREEN, 30, "start")]
    return {"base": "map", "cam": CAM, "els": els}


NINE = [("Sherden", "horn"), ("Shekelesh", "cap"), ("Ekwesh", "cap"), ("Lukka", "cap"), ("Teresh", "cap"), ("Peleset", "feather"), ("Tjeker", "feather"),
        ("Denyen", "feather"), ("Weshesh", "cap")]


def portrait(x, y, s, at=-1, head="feather"):
    """A head and shoulders in carved profile, facing right (y = the foot of the shoulders, s = shoulders to crown)."""
    r = .2 * s
    hx, hy = x, y - s + r
    out = carve([(x - 2.0 * r, y), (x - 1.9 * r, y - 1.2 * r), (x - 1.3 * r, y - 1.75 * r), (x - .4 * r, y - 1.95 * r), (x + .6 * r, y - 1.95 * r), (x + 1.4 * r, y - 1.7 * r),
                  (x + 1.85 * r, y - 1.1 * r), (x + 1.95 * r, y)], at, CUT, curve=False)
    out += cut([(x - 1.5 * r, y - 1.55 * r), (x - .3 * r, y - 1.25 * r), (x + .9 * r, y - 1.25 * r), (x + 1.55 * r, y - 1.5 * r)], at, 2, curve=True, op=.7)
    face = [(hx - .55 * r, hy + 1.5 * r), (hx - .62 * r, hy + .75 * r), (hx - 1.0 * r, hy - .05 * r), (hx - .55 * r, hy - .95 * r), (hx + .45 * r, hy - .82 * r),
            (hx + .82 * r, hy - .3 * r), (hx + .86 * r, hy - .05 * r), (hx + 1.18 * r, hy + .2 * r), (hx + .88 * r, hy + .33 * r), (hx + .94 * r, hy + .5 * r),
            (hx + .84 * r, hy + .62 * r), (hx + .8 * r, hy + .86 * r), (hx + .3 * r, hy + 1.02 * r), (hx + .3 * r, hy + 1.5 * r)]
    out += carve(face, at, CUT)
    out += cut([(hx + .38 * r, hy - .12 * r), (hx + .6 * r, hy - .1 * r)], at, 2.6)
    out += cut([(hx - .25 * r, hy + .05 * r), (hx - .38 * r, hy + .22 * r), (hx - .25 * r, hy + .42 * r)], at, 2, curve=True)
    if head == "feather":
        out += carve([(hx - 1.02 * r, hy - .35 * r), (hx + .75 * r, hy - .55 * r), (hx + .7 * r, hy - .85 * r), (hx - 1.02 * r, hy - .7 * r)], at, CUT2)
        for k in range(9):
            u = k / 8
            bx, by = hx - .95 * r + u * 1.6 * r, hy - .72 * r - .14 * r * (1 - abs(u - .5) * 2)
            out += cut([(bx, by), (bx + (u - .5) * .5 * r, by - 1.55 * r)], at, 3.2)
        out += cut([(hx - 1.25 * r, hy - 2.25 * r), (hx + .95 * r, hy - 2.25 * r)], at, 2, op=.55)
    elif head == "horn":
        out += carve(E(hx - .1 * r, hy - .45 * r, 1.05 * r, .72 * r, 18, 180, 360) + [(hx + .95 * r, hy - .4 * r), (hx - 1.15 * r, hy - .4 * r)], at, CUT2)
        out += cut([(hx - .8 * r, hy - .9 * r), (hx - 1.55 * r, hy - 1.35 * r), (hx - 1.7 * r, hy - 2.1 * r)], at, 5, curve=True)
        out += cut([(hx + .6 * r, hy - .95 * r), (hx + 1.3 * r, hy - 1.45 * r), (hx + 1.35 * r, hy - 2.2 * r)], at, 5, curve=True)
        out += carve(E(hx - .1 * r, hy - 1.75 * r, .38 * r, .38 * r, 14), at, CUT2)
        out += cut([(hx - .1 * r, hy - 1.15 * r), (hx - .1 * r, hy - 1.38 * r)], at, 3)
    else:
        out += carve([(hx - 1.02 * r, hy - .2 * r), (hx - .9 * r, hy - .75 * r), (hx - .4 * r, hy - 1.05 * r), (hx + .35 * r, hy - 1.0 * r), (hx + .72 * r, hy - .62 * r),
                      (hx + .7 * r, hy - .45 * r), (hx - .95 * r, hy - .05 * r)], at, CUT2, curve=True)
        out += cut([(hx - .98 * r, hy - .3 * r), (hx + .72 * r, hy - .52 * r)], at, 2.2)
    return out


def s11():
    """Nine warriors in carved profile on a stone frieze, counted in one by one; the three named take labels as said, the Peleset
    glowing gold."""
    sid = "s11"
    tn = {nm: T(sid, nm) for nm in ("Sherden", "Shekelesh", "Peleset")}
    els = wall_bg(seed=12, y0=170, y1=720)
    els += [rect(-20, 120, W_ + 40, 60, "#140e0a", at=-1), rect(-20, 720, W_ + 40, 300, "#140e0a", at=-1)]
    els += cut([(40, 200), (1740, 200)], -1, 3) + cut([(40, 690), (1740, 690)], -1, 3)
    for k, (nm, hd) in enumerate(NINE):
        x = 160 + k * 182
        els += [{"k": "group", "els": portrait(x, 688, 300, -1, hd), "in": round(.3 + .3 * k, 2), "fx": "pop"}]
        if nm in tn:
            c = GOLD if nm == "Peleset" else BONE
            els.append(lab(x, 770, nm, tn[nm], c, 32))
            if nm == "Peleset":
                els += [glow(x, 470, 170, tn[nm], .55), ring(x, 470, 125, tn[nm] + .1, GOLD, 3, dur=.7)]
    return {"base": "dark", "cam": CAM, "els": els}


def s12():
    """A timeline 1220 to 1170 BCE: Ramesses III's year 8 (about 1177) is already there; Merneptah's battle (about 1208) pops in, with
    five helmeted heads and a Libyan king beside it. Then a small notebook of the 1800s opens on 'peuples de la mer'."""
    sid = "s12"
    t_m, t_l, t_name, t_18 = T(sid, "about thirty"), T(sid, "allies of"), T(sid, "Sea Peoples isn't"), T(sid, "French scholars")
    X = lambda yr: round(160 + (1222 - yr) / 54 * 900, 1)
    y, gy = 620, 540
    els = [{"k": "axis", "x0": 160, "x1": 1060, "y": y, "ticks": [[X(1220), "1220"], [X(1200), "1200"], [X(1180), "1180"]], "t": "BCE", "in": .1},
           ln([(140, gy), (1080, gy)], .1, "#5a4634", 2, draw=False)]
    els += [ln([(X(1177), y), (X(1177), 270)], .3, GOLD, 3, dur=.5), lab(X(1177), 250, "Ramesses III", .4, GOLD, 30)]
    els += [ln([(X(1208), y), (X(1208), 270)], t_m, GOLD, 3, dur=.5), lab(X(1208), 250, "Merneptah", t_m + .2, GOLD, 30)]
    for k in range(5):
        hx = 455 + 66 * k
        els += [{"k": "group", "els": portrait(hx, gy, 110, -1, ("horn", "cap", "cap", "cap", "cap")[k]), "in": round(t_m + .7 + .2 * k, 2), "fx": "pop"}]
    els += [figure(820, gy, 150, t_l, "#d9c7a6"), lab(820, gy + 50, "a Libyan king", t_l + .3, DIM, 26)]
    bx, by = 1180, 290
    els += [rect(bx + 8, by + 12, 470, 330, "rgba(0,0,0,.5)", r=8, at=t_name), rect(bx, by, 470, 330, "#e9dcc0", "#8a7458", 2, 8, t_name, "pop"),
            ln([(bx + 235, by + 10), (bx + 235, by + 320)], t_name + .1, "#8a7458", 2, draw=False),
            {"k": "glyphs", "x": bx + 24, "y": by + 30, "w": 190, "h": 270, "rows": 10, "cols": 6, "kind": "latin", "c": "#6b5a44", "in": round(t_name + .2, 2), "op": .6},
            lab(bx + 352, by + 150, "peuples", t_name + .4, "#3a2a1a", 34, st="ital", halo=False), lab(bx + 352, by + 192, "de la mer", t_name + .7, "#3a2a1a", 34, st="ital", halo=False),
            lab(bx + 235, by + 390, "the 1800s", t_18, AMBER, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


MV = View(5, 33, 33.5, 45.5, (90, 120, 1600, 680))


def s13():
    """The Mediterranean from Sardinia to Lycia: each name is linked to a place that sounds like it, in the claimed (dotted) style:
    Lukka to Lycia, Sherden to Sardinia (?), Shekelesh to Sicily (?). Then a magnifying glass: a clue, not a passport."""
    sid = "s13"
    t_lu, t_sh, t_sk, t_clue = T(sid, "the Lukka"), T(sid, "the Sherden"), T(sid, "the Shekelesh"), T(sid, "a clue")
    v = MV
    els = map_base(v)
    for nm, place, t, (dx, dy), q in (("Lukka", "Lycia", t_lu, (-60, -150), False), ("Sherden", "Sardinia", t_sh, (40, -170), True), ("Shekelesh", "Sicily", t_sk, (120, -150), True)):
        x, y = site(v, place)
        cx_, cy_ = x + dx, y + dy
        els += chip(cx_, cy_, nm, t, LILAC, 28)
        els += [ln([(cx_, cy_ + 24), (x, y - 12)], t + .3, LILAC, 2.5, "claimed", .6), dot(x, y, 9, LILAC, t + .5),
                lab(x + 16, y + 34, place, t + .6, BONE, 28, "start")]
        if q:
            els.append(lab(x - 26, y + 6, "?", t + .8, LILAC, 56, st="serif"))
    els += [circ(889, 560, 70, "rgba(255,255,255,.06)", BONE, 6, t_clue, "pop"), ln([(938, 610), (1010, 690)], t_clue + .1, BONE, 12, draw=False)]
    return {"base": "map", "cam": CAM, "els": els}


def horse(x, y, s, at, c, face=-1, op=None):
    """A horse in side view (silhouette), facing left by default; s = body length, hooves on y."""
    pts = [(.42, -.62), (.2, -.66), (-.15, -.66), (-.3, -.72), (-.38, -.9), (-.44, -1.06), (-.5, -1.12), (-.62, -1.02), (-.66, -.96), (-.6, -.92), (-.5, -.94),
           (-.46, -.84), (-.42, -.68), (-.36, -.5), (-.34, -.28), (-.38, 0), (-.32, 0), (-.27, -.3), (-.2, -.4), (.2, -.4), (.26, -.28), (.24, 0), (.3, 0),
           (.33, -.3), (.38, -.42), (.48, -.5), (.56, -.42), (.6, -.3), (.62, -.36), (.56, -.56)]
    f = -1 if face < 0 else 1
    return poly([(x - f * px * s if f > 0 else x + px * s, y + py * s) for px, py in pts], c, at=at, fx="rise", op=op, curve=False)


def chariot(x, y, s, at, c="#2a2018", face=-1):
    """A war chariot of the age, facing left: two horses, the pole, a light box on a six-spoked wheel, a driver and an archer."""
    out = [horse(x - .62 * s, y, .6 * s, at, "#3a2c20"), horse(x - .52 * s, y, .6 * s, at + .05, c)]
    out += [ln([(x - .3 * s, y - .3 * s), (x - .05 * s, y - .28 * s)], at, c, 5, draw=False),
            poly([(x - .1 * s, y - .46 * s), (x - .06 * s, y - .48 * s), (x + .14 * s, y - .44 * s), (x + .14 * s, y - .25 * s), (x - .1 * s, y - .25 * s)], c, at=at, fx="rise"),
            circ(x + .04 * s, y - .17 * s, .17 * s, "none", c, 6, at, "rise")]
    for k in range(6):
        a = k * math.pi / 3
        out.append(ln([(x + .04 * s, y - .17 * s), (x + .04 * s + .17 * s * math.cos(a), y - .17 * s + .17 * s * math.sin(a))], at, c, 3.5, draw=False))
    out += [figure(x - .02 * s, y - .25 * s, .42 * s, at + .1, c), figure(x + .09 * s, y - .25 * s, .43 * s, at + .15, c)]
    out.append(ln([(x - .1 * s, y - .72 * s), (x - .17 * s, y - .56 * s), (x - .1 * s, y - .4 * s)], at + .2, c, 4, curve=True))
    return out


def runner(x, y, h, at, c="#2a2018", face=1, sword=False):
    """A foot soldier running: a body in stride, a round shield, a javelin raised (or a long sword)."""
    f = face
    out = [figure(x, y, h, at, c)]
    out.append(circ(x + .18 * h * f, y - .55 * h, .17 * h, c, "#8a6a48", 2, at, "rise"))
    if sword:
        out.append(ln([(x - .05 * h * f, y - .6 * h), (x + .45 * h * f, y - .95 * h)], at, "#9aa0a8", 4, draw=False))
    else:
        out.append(ln([(x - .3 * h * f, y - .5 * h), (x + .4 * h * f, y - 1.15 * h)], at, "#8a6a48", 3, draw=False))
    return out


def s14():
    """A plain at dusk: a chariot (the great kingdoms' army) on the right; from the left a loose swarm of foot soldiers with round
    shields, javelins and long swords; dotted lilac javelin arcs (Drews' proposal) fly at the horses."""
    sid = "s14"
    t_ch, t_sw, t_cut = T(sid, "fought from"), T(sid, "swarms of foot"), T(sid, "cut them")
    gy = 700
    els = chariot(1350, gy, 420, t_ch) + [lab(1330, 300, "chariots", t_ch + .3, BONE, 32)]
    rr = random.Random(14)
    for k in range(9):
        x = 160 + 70 * k + rr.uniform(-20, 20)
        yy = gy - rr.uniform(0, 40)
        els += runner(x, yy, rr.uniform(105, 125), t_sw + .1 * k, sword=(k % 3 == 1))
    els += [lab(450, 420, "foot soldiers", t_sw + .6, BONE, 32)]
    for k in range(4):
        x0 = 380 + 90 * k
        els.append(arr([(x0, gy - 150), ((x0 + 1050) / 2, gy - 330 + 20 * k), (1030 + 25 * k, gy - 190)], t_cut - .6 + .25 * k, LILAC, 3, "claimed", .8))
    els += [lab(889, 230, "Drews: a new way of fighting?", t_cut + .4, LILAC, 28, st="ital")]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1500, 520, 30], "cam": CAM, "els": els}


PV = View(31.5, 36.8, 30.6, 34.6, (90, 120, 1600, 680))


def s15():
    """The southern Levant coast: ships come in from the west (dotted); five Philistine city dots pop along the coast and inland,
    Ashkelon in gold; a soft label 'Philistine cities'."""
    sid = "s15"
    t_ph, t_ash = T(sid, "Philistines"), T(sid, "Ashkelon")
    v = PV
    els = map_base(v) + [lab(*v.p(35.6, 31.3), "Canaan", .3, DIM, 30, st="ital"), lab(*v.p(32.6, 33.6), "Mediterranean", .3, "#9fd0ff", 28, st="ital")]
    for k in range(3):
        y0 = 330 + 90 * k
        els += [ln([(120, y0), (500, y0 + 60), (860, 560 + 25 * k)], .4 + .3 * k, BLUE, 2.5, "claimed", 1.2, curve=True)]
        els += ship_icon(500, y0 + 50, 52, .9 + .3 * k, BLUE)
    for k, nm in enumerate(("Gaza", "Ashdod", "Ekron", "Gath")):
        x, y = site(v, nm)
        els.append(dot(x, y, 8, AMBER, t_ph + .3 + .2 * k))
    ax, ay = site(v, "Ashkelon")
    els += [dot(ax, ay, 11, GOLD, t_ash), glow(ax, ay, 70, t_ash, .7), lab(ax - 24, ay + 8, "Ashkelon", t_ash + .1, GOLD, 32, "end"),
            lab(1110, 690, "Philistine cities", t_ph + 1.0, AMBER, 30, st="ital"), ln([(1110, 660), (1010, 618)], t_ph + 1.0, AMBER, 2, dur=.5)]
    return {"base": "map", "cam": CAM, "els": els}


ASHB = [(430, "Bronze Age", 3), (900, "early Iron Age", 4), (1370, "later Iron Age", 3)]


def s16():
    """Ashkelon in three bands of time: three people of the Bronze Age, four infants of the early Iron Age, three people of the
    later Iron Age, popping as counted; a gold tick 'the Philistines arrive' between the first two."""
    sid = "s16"
    t_ten = T(sid, "ten people")
    els = [ln([(160, 470), (1640, 470)], .2, "#8c7152", 3, dur=1.0)]
    k = 0
    for cx, name, n in ASHB:
        els += [rect(cx - 210, 470, 420, 6, AMBER, r=3, at=.3, op=.5), lab(cx, 520, name, .5, DIM, 28)]
        for j in range(n):
            h = 66 if n == 4 else 130
            x = cx + (j - (n - 1) / 2) * (80 if n == 4 else 95)
            els.append(figure(x, 465, h, round(t_ten + .25 * k, 2), "#e8d6b8"))
            k += 1
    els += [ln([(665, 200), (665, 470)], .8, GOLD, 3, "inferred", .6), lab(665, 180, "the Philistines arrive", 1.0, GOLD, 28)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def card(x, y, w, at, c, rot=0, op=None, fx="pop"):
    """A playing card (rounded, with a small pip), rotated about its foot."""
    h = w * 1.45
    e = {"k": "group", "in": round(at, 2), "fx": fx, "els": [{"k": "group", "tr": "rotate(%g %g %g)" % (rot, x, y), "els": [
        rect(x - w / 2, y - h, w, h, c, "#2a2018", 2, w * .12, -1), circ(x, y - h * .5, w * .16, "rgba(26,21,17,.45)", at=-1)]}]}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def fan(cx, cy, cols, at, w=70, spread=11, step=.08):
    n = len(cols)
    return [card(cx, cy, w, at + step * k, c, (k - (n - 1) / 2) * spread) for k, c in enumerate(cols)]


SANDC, AMBC, BLUEC = "#d8c3a0", "#d9a066", "#7fb7e6"


def s17():
    """The deck of cards: two fans (mother, father) slide in and a new fan, a mix of both, forms in the middle (you)."""
    sid = "s17"
    t_sh = T(sid, "shuffled together")
    els = fan(330, 600, [AMBC] * 6, .3, 110, 10) + [lab(330, 680, "mother", .6, DIM, 30)]
    els += fan(1450, 600, [SANDC] * 6, .6, 110, 10) + [lab(1450, 680, "father", .9, DIM, 30)]
    els += [arr([(520, 380), (680, 320), (770, 360)], t_sh, AMBER, 3, dur=.6), arr([(1260, 380), (1100, 320), (1010, 360)], t_sh, AMBER, 3, dur=.6)]
    els += fan(889, 640, [AMBC, SANDC, AMBC, SANDC, SANDC, AMBC, AMBC, SANDC], t_sh + .6, 120, 8) + [lab(889, 720, "you", t_sh + 1.2, GOLD, 34)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s18():
    """A house in section at dusk with a small lamp-lit hollow under its floor (no bones: care); beside it a fan of amber cards with
    a few blue ones; a dotted blue arrow comes in from the west: southern Europe?"""
    sid = "s18"
    t_inf, t_new, t_eu = T(sid, "Four infants"), T(sid, "new deck"), T(sid, "southern Europe")
    gy = 560
    els = [rect(-20, gy, W_ + 40, 460, "#3b2d22", at=-1), rect(-20, gy, W_ + 40, 8, "#6b5238", at=-1)]
    els += [rect(220, gy - 230, 520, 230, "rgba(201,168,120,.18)", "#c9a878", 3, 2, .2), rect(220, gy - 250, 560, 24, "#8a6a48", at=.2),
            rect(420, gy - 140, 70, 140, "#1a120c", at=.3)]
    els += [oval(480, gy + 70, 70, 32, "#4a3a2c", "#c9a878", 2, 1, t_inf), glow(480, gy + 66, 110, t_inf + .2, .7, "lamp"),
            oval(480, gy + 70, 36, 14, "#e8d6b8", at=t_inf + .4, op=.85)]
    els += [lab(480, gy + 160, "under the floor", t_inf + .8, DIM, 26)]
    els += fan(1250, 640, [AMBC, AMBC, BLUEC, AMBC, BLUEC, AMBC, AMBC], t_new, 90, 10)
    els += [arr([(120, 190), (700, 120), (1180, 300)], t_eu - .4, BLUE, 3.5, "claimed", 1.2), lab(380, 210, "southern Europe?", t_eu, BLUE, 30)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1600, 380, 26], "cam": CAM, "els": els}


def s19_add():
    """On the Ashkelon timeline: card fans under each band (all amber; amber with blue; blue fading back to amber) and a bracket
    'within two centuries' between the early and later Iron Age."""
    sid = "s19"
    t_two, t_mix = T(sid, "Within two"), T(sid, "local mix")
    els = fan(430, 760, [AMBC] * 5, .3, 60, 10) + fan(900, 760, [AMBC, BLUEC, AMBC, BLUEC, AMBC], .6, 60, 10)
    els += [card(1370 + (k - 2) * 0, 760, 60, t_mix - .4 + .08 * k, AMBC if k != 2 else "#b9c8cf", (k - 2) * 10) for k in range(5)]
    els += [line([[900, 260], [900, 240], [1370, 240], [1370, 260]], round(t_two, 2), BONE, 2, dur=.6), lab(1135, 225, "within two centuries", t_two + .3, BONE, 28)]
    return els


def s20():
    """A coast at dusk: a ship with bird-head posts pulled up on the beach; a family walks up from it to flat-roofed houses with a
    hearth glow; a new house rises at 'stayed'."""
    sid = "s20"
    t_fam, t_stay = T(sid, "families"), T(sid, "stayed")
    gy = 640
    els = [{"k": "water", "y": gy + 10, "h": 400, "x0": -100, "x1": 760, "op": .85, "in": -1},
           poly([(620, gy + 60), (780, gy + 6), (1800, gy - 6), (1800, 1100), (620, 1100)], "#5a4634", at=-1)]
    els += ship_icon(470, gy + 40, 380, -1, "#2a2018", 1)
    for k, (x, h) in enumerate(((860, 150), (920, 140), (968, 92))):
        els.append(figure(x, gy, h, round(t_fam + .2 * k, 2), "#1d1611"))
    for k, x in enumerate((1120, 1320)):
        els += [rect(x, gy - 150, 180, 150, "#9a7a56", "#d8c3a0", 2, 2, .3 + .3 * k, "rise"), rect(x + 72, gy - 76, 36, 76, "#2a1f17", at=.4 + .3 * k)]
    els += [glow(1220, gy - 40, 120, .8, .65, "fire"), glow(1410, gy - 40, 90, 1.0, .5, "lamp")]
    els += [rect(1530, gy - 130, 170, 130, "#9a7a56", "#d8c3a0", 2, 2, t_stay, "rise"), rect(1600, gy - 66, 32, 66, "#2a1f17", at=t_stay + .2)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [250, 470, 34], "cam": CAM, "els": els}


# ================================================================== 2 A world on fire
NEV = View(19, 50, 24, 42.5, (90, 120, 1600, 680))          # the Near East of the great kingdoms


def kingdom(v, lon, lat, rx, ry, at, c, name, lx=0, ly=0, size=30):
    x, y = v.p(lon, lat)
    return [poly(E(x, y, rx, ry, 30), c, c, 1.5, at, "pop", op=.28, curve=True), lab(x + lx, y + ly + 10, name, at + .15, BONE, size)]


def s21():
    """The great kingdoms as soft coloured areas, filling in as named (Egypt, the Hittites, Babylon, Assyria, the Mycenaean Greeks,
    Cyprus); amber trade lines draw between them with gold, grain and horse marks gliding along; Egypt and Hatti's line glows at
    'brother'."""
    sid = "s21"
    t = {k: T(sid, k) for k in ("Egypt", "the Hittites", "Babylon", "Assyria", "Mycenaean", "Cyprus close", "They traded", "gold", "grain", "horses", "brother")}
    v = NEV
    els = map_base(v)
    els += kingdom(v, 30.8, 27.6, 95, 130, t["Egypt"], "#e8c86a", "Egypt")
    els += kingdom(v, 33.4, 39.4, 160, 70, t["the Hittites"], "#d9894a", "Hittites")
    els += kingdom(v, 44.6, 32.4, 80, 70, t["Babylon"], "#8fd9b0", "Babylon")
    els += kingdom(v, 43.3, 36.2, 70, 50, t["Assyria"], "#9fd0ff", "Assyria")
    els += kingdom(v, 22.4, 37.9, 60, 70, t["Mycenaean"], "#c9c1ee", "Mycenaeans", 0, 0, 28)
    els += kingdom(v, 33.2, 35.1, 40, 18, t["Cyprus close"], "#e8b87a", "Cyprus", 0, 34, 26)
    hubs = {"eg": v.p(31.2, 29.8), "ha": v.p(33.2, 38.6), "ba": v.p(44.2, 32.8), "as": v.p(43.0, 36.0), "my": v.p(22.9, 37.4), "cy": v.p(33.3, 35.0)}
    routes = [("eg", "ha"), ("eg", "cy"), ("cy", "my"), ("eg", "ba"), ("ha", "as"), ("my", "eg")]
    for k, (a, b) in enumerate(routes):
        (x0, y0), (x1, y1) = hubs[a], hubs[b]
        mx, my = (x0 + x1) / 2 + (y1 - y0) * .12, (y0 + y1) / 2 - (x1 - x0) * .12
        els.append(ln([(x0, y0), (mx, my), (x1, y1)], t["They traded"] + .15 * k, AMBER, 3, "inferred", .8, curve=True))
    for k, (kind, at) in enumerate((("gold", t["gold"]), ("grain", t["grain"]), ("horse", t["horses"]))):
        (x0, y0), (x1, y1) = hubs[routes[k][0]], hubs[routes[k][1]]
        mx, my = (x0 + x1) / 2 + (y1 - y0) * .12 * .5, (y0 + y1) / 2 - (x1 - x0) * .12 * .5
        if kind == "gold":
            els += [circ(mx, my, 13, AU, "#fff3c8", 2, at, "pop")]
        elif kind == "grain":
            els += [poly([(mx - 12, my + 14), (mx - 14, my - 6), (mx - 6, my - 16), (mx + 6, my - 16), (mx + 14, my - 6), (mx + 12, my + 14)], GRAIN, at=at, fx="pop", curve=True)]
        else:
            els += [horse(mx, my + 14, 40, at, BONE)]
    (x0, y0), (x1, y1) = hubs["eg"], hubs["ha"]
    els += [ln([(x0, y0), ((x0 + x1) / 2 + (y1 - y0) * .12, (y0 + y1) / 2 - (x1 - x0) * .12), (x1, y1)], t["brother"], GOLD, 6, curve=True, dur=.8),
            glow((x0 + x1) / 2, (y0 + y1) / 2, 90, t["brother"] + .3, .5)]
    return {"base": "map", "cam": CAM, "els": els}


def merchant(x, y, s, at, c, kind="aegean", face=1):
    """A merchant ship of the age, sails set: a hull, a mast with a square sail; kind changes the stem (Egypt: a papyrus-flower
    stern; Aegean: a straight raked stem; Cyprus: a plain curve)."""
    f = face
    hull = [(x - .5 * s * f, y - .14 * s), (x - .42 * s * f, y + .03 * s), (x + .4 * s * f, y + .03 * s), (x + .5 * s * f, y - .12 * s), (x + .44 * s * f, y - .06 * s), (x - .44 * s * f, y - .06 * s)]
    out = [poly(hull, c, at=at, fx="rise"), ln([(x, y - .06 * s), (x, y - .7 * s)], at, c, 3, draw=False),
           poly([(x - .26 * s, y - .66 * s), (x + .26 * s, y - .66 * s), (x + .24 * s, y - .2 * s), (x - .24 * s, y - .2 * s)], "#d8c3a0", c, 1.5, at, "rise", op=.9)]
    if kind == "egypt":
        out.append(ln([(x - .5 * s * f, y - .14 * s), (x - .58 * s * f, y - .32 * s), (x - .52 * s * f, y - .36 * s)], at, c, 4, draw=False, curve=True))
    elif kind == "aegean":
        out.append(ln([(x + .5 * s * f, y - .12 * s), (x + .6 * s * f, y - .3 * s)], at, c, 4, draw=False))
    return out


def s22():
    """Ugarit at dusk from the sea: the city on its low mound, walls and the palace, lamps lit; three merchant ships come in on dotted
    wakes (Egypt, Cyprus, the Aegean); a lit doorway with shelves of clay tablets."""
    sid = "s22"
    t_ug, t_ships, t_clay = T(sid, "Ugarit"), T(sid, "ships from Egypt"), T(sid, "clay")
    gy = 600
    els = [{"k": "water", "y": gy + 20, "h": 400, "x0": -100, "x1": 1900, "op": .85, "in": -1}]
    els += [poly([(780, gy + 30), (900, gy - 40), (1000, gy - 120), (1500, gy - 130), (1640, gy - 60), (1800, gy - 10), (1800, gy + 200), (780, gy + 200)], "#5a4634", "#8a6a48", 2, -1, curve=True)]
    els += [rect(1000, gy - 220, 520, 100, "#9a7a56", "#d8c3a0", 2, 2, t_ug, "rise")]
    for k in range(7):
        els.append(rect(1030 + 70 * k, gy - 290 + (k % 2) * 20, 52, 70 - (k % 2) * 20, "#b08a60", "#e8d0a8", 1.5, 2, t_ug + .15 * k, "rise"))
    els += [rect(1150, gy - 340, 240, 120, "#c9a878", "#f2dcb4", 2, 2, t_ug + .5, "rise"), rect(1240, gy - 300, 60, 80, "#3a2a1c", at=t_ug + .7)]
    els += [rect(1170 + 46 * k, gy - 325, 22, 26, "#3a2a1c", at=t_ug + .7) for k in range(5) if k != 2]
    els += [glow(1100 + 90 * k, gy - 180, 50, t_ug + .8 + .1 * k, .7, "lamp") for k in range(5)]
    els += [lab(1265, gy - 360, "Ugarit", t_ug + .3, GOLD, 34, st="serif")]
    for k, (kind, x, y, c) in enumerate((("egypt", 330, gy + 70, "#3a2c20"), ("plain", 560, gy + 130, "#2e241c"), ("aegean", 140, gy + 150, "#3a2c20"))):
        at = t_ships + .5 * k
        els += [ln([(x - 260, y + 30), (x - 120, y + 10), (x - 50, y)], at, BONE, 2, "claimed", .6, curve=True)] + merchant(x, y, 170, at + .3, c, kind)
    cx, cy = 560, 300
    els += [circ(cx, cy, 130, "#1d140e", GOLD, 3, t_clay, "pop"), glow(cx, cy, 150, t_clay + .1, .5, "lamp")]
    for r in range(3):
        els.append(ln([(cx - 95, cy - 50 + 50 * r), (cx + 95, cy - 50 + 50 * r)], t_clay + .2, "#8a6a48", 4, draw=False))
        for j in range(6):
            els.append(rect(cx - 88 + 30 * j, cy - 82 + 50 * r, 22, 30, CLAY, "#e9cfa6", 1, 4, t_clay + .2 + .02 * (r * 6 + j)))
    els += [lab(cx, cy + 165, "clay letters", t_clay + .4, BONE, 28)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [200, 420, 30], "cam": CAM, "els": els}


def s23():
    """The clay letter again, close: Ammurapi, Ugarit's last king; a warm line runs along the wedges as if being read."""
    sid = "s23"
    t_am, t_on = T(sid, "He was Ammurapi"), T(sid, "goes on")
    els = lamp_room(win=(1240, 170, 400, 380))
    els += big_tablet(420, 160, 560, 600, -1, seed=9, rows=10)
    els += [glow(330, 560, 340, -1, .75, "lamp"), poly([(300, 660), (310, 630), (357, 628), (370, 645), (350, 660)], "#c88b4a", "#f0c08a", 1.5, -1),
            poly([(351, 628), (357, 600), (363, 628)], "#ffe2a8", at=-1, curve=True)]
    els += [lab(1440, 640, "Ammurapi", t_am, GOLD, 34, st="serif"), lab(1440, 680, "the last king of Ugarit", t_am + .4, DIM, 26)]
    for k in range(3):
        y = 160 + 36 + (k + 3) * (530 / 10) + 20
        els.append(ln([(460, y), (940, y)], t_on + .3 * k, GOLD, 3, dur=.9, op=.7))
    return {"base": "dark", "cam": CAM, "els": els}


UGV = View(26, 39.5, 32.3, 41.6, (90, 120, 1600, 680))


def s24():
    """Map: Ugarit glows; chariot marks march into Hatti, ship marks sail west to Lukka (south-west Turkey); Ugarit is left with a
    dim, empty ring."""
    sid = "s24"
    t_tr, t_ha, t_sh, t_lu = T(sid, "All my troops"), T(sid, "land of Hatti"), T(sid, "all my ships"), T(sid, "land of Lukka")
    v = UGV
    els = map_base(v)
    ux, uy = site(v, "Ugarit")
    els += [{"k": "pin", "x": ux, "y": uy, "t": "Ugarit", "c": GOLD, "in": .3, "a": "start", "lx": 22}, glow(ux, uy, 90, .3, .6)]
    hx, hy = v.p(33.6, 39.4)
    els += [lab(hx, hy, "Hatti", t_ha, BONE, 34, st="serif"), arr([(ux - 10, uy - 20), (ux - 120, uy - 160), (hx + 60, hy + 40)], t_tr + .3, AMBER, 3.5, dur=1.4)]
    for k in range(3):
        els += cart_icon(ux - 90 - 70 * k, uy - 120 - 60 * k, 40, t_tr + .8 + .25 * k, AMBER)
    lx, ly = site(v, "Lycia")
    els += [lab(lx, ly - 40, "Lukka", t_lu, BONE, 34, st="serif"), arr([(ux - 20, uy + 10), ((ux + lx) / 2, uy + 70), (lx + 30, ly + 20)], t_sh + .2, BLUE, 3.5, dur=1.4)]
    for k in range(3):
        els += ship_icon(ux - 220 - 170 * k, uy + 60 + 8 * k, 46, t_sh + .7 + .25 * k, BLUE)
    els += [circ(ux, uy, 46, "none", DIM, 2.5, t_lu + 1.0, "pop", style="inferred")]
    return {"base": "map", "cam": CAM, "els": els}


def s25():
    """Ugarit's coast at night seen from the sea: seven dark ships with bird-head posts pop in one by one, fires rise on the shore
    behind them; a tally '7'."""
    sid = "s25"
    t_7, t_seven = T(sid, "The seven ships"), T(sid, "Seven ships", k=1)
    gy = 520
    els = [{"k": "water", "y": gy, "h": 600, "x0": -100, "x1": 1900, "op": .9, "in": -1},
           poly([(-20, gy), (300, gy - 40), (700, gy - 60), (1100, gy - 50), (1500, gy - 70), (1800, gy - 40), (1800, gy + 4), (-20, gy + 4)], "#1c1712", at=-1, curve=True)]
    for k, x in enumerate((260, 620, 980, 1340)):
        els += flame(x, gy - 40, 34, t_7 + 1.2 + .3 * k)
    for k in range(7):
        x = 220 + 205 * k
        els += ship_icon(x, gy + 140 + 30 * (k % 2), 130, t_7 + .4 + .35 * k, "#0c0a0a", 1)
        els.append(lab(x, gy + 210 + 30 * (k % 2), str(k + 1), t_7 + .5 + .35 * k, DIM, 24))
    els += [lab(1600, 300, "7", t_seven, GOLD, 120, st="big", fx="pop")]
    return {"base": "sky", "tod": "night", "ground": 1300, "sun": False, "moon": [300, 200, 26], "cam": CAM, "els": els}


def s26():
    """Charred seeds and olive stones on dark ground beside an hourglass whose sand runs down; a bar 'carbon left' shrinks in step."""
    sid = "s26"
    t_seed, t_glass = T(sid, "Burnt seeds"), T(sid, "like sand")
    rr = random.Random(26)
    els = [oval(510, 600, 330, 70, "#2b2016", "#5a4634", 2, 1, .2), glow(510, 520, 380, .2, .35, "lamp")]
    for k in range(16):
        x, y = 280 + rr.uniform(0, 460), 600 + rr.uniform(-34, 30)
        big = k % 4 == 0
        els.append(oval(round(x, 1), round(y, 1), round(rr.uniform(30, 40) if big else rr.uniform(16, 24), 1), round(rr.uniform(18, 24) if big else rr.uniform(10, 14), 1),
                        "#3a2a1e" if big else "#241810", "#b08a60", 2, 1, round(t_seed + .06 * k, 2), fx="pop"))
    els += [lab(510, 720, "burnt seeds and olive stones", t_seed + .6, DIM, 28)]
    gx, gy = 1180, 470
    glass = [(gx - 110, gy - 230), (gx + 110, gy - 230), (gx + 12, gy), (gx + 110, gy + 230), (gx - 110, gy + 230), (gx - 12, gy)]
    els += [poly(glass, "rgba(159,208,255,.08)", BLUE, 3, t_glass - .3, "pop"),
            poly([(gx - 90, gy - 200), (gx + 90, gy - 200), (gx, gy - 20)], "#e8c35a", at=t_glass, op=.9),
            poly([(gx - 70, gy + 225), (gx + 70, gy + 225), (gx, gy + 150)], "#e8c35a", at=t_glass + 1.5, op=.9),
            ln([(gx, gy), (gx, gy + 200)], t_glass + .3, "#e8c35a", 3, dur=1.0)]
    els += [rect(1380, 300, 60, 340, "rgba(255,236,206,.08)", BONE, 2, 6, t_glass), rect(1384, 304, 52, 332, AMBER, r=4, at=t_glass + .2, op=.85),
            cover(1384, 304, 52, 200, t_glass + 1.2, "#20170f", 1.0, 2.0), lab(1410, 680, "carbon left", t_glass + .4, AMBER, 26)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s27():
    """The mound of Gibala cut open on the left: layers, with a thick burnt layer that glows; samples are taken from it and carried
    to a timeline on the right, where a band settles around 1190 BCE; then a row of clay tablets marching along the timeline stops."""
    sid = "s27"
    t_gib, t_clock, t_1190, t_stop = T(sid, "At Gibala"), T(sid, "that clock"), T(sid, "around"), T(sid, "Then Ugarit's letters")
    top = [(90, 520), (180, 380), (330, 300), (560, 290), (700, 360), (790, 520)]
    els = [poly(top + [(790, 760), (90, 760)], "#6f5a44", "#c9b08a", 2, .2, curve=False)]
    bands = [(330, "#8a7458"), (400, "#7a6248"), (470, "#2a1a12"), (520, "#7a6248"), (600, "#5a4632")]
    for k, (y, c) in enumerate(bands):
        els.append(rect(96 + (y < 380) * 80, y, 690 - (y < 380) * 150, 70 if k != 2 else 50, c, at=.3 + .1 * k))
    els += [rect(96, 470, 690, 50, "#3a1a10", at=t_gib + .2), glow(440, 495, 300, t_gib + .4, .55, "fire"),
            lab(440, 260, "Gibala", t_gib, GOLD, 34, st="serif"), lab(440, 504, "burnt layer", t_gib + .8, "#ffcf9a", 28)]
    X = lambda yr: round(980 + (1250 - yr) / 100 * 640, 1)
    for k, x in enumerate((170, 240, 640, 710)):
        els += [dot(x, 495, 8, "#ffcf9a", t_clock + .1 * k)]
    els += [arr([(700, 470), (850, 380), (X(1190), 610)], t_clock + .4, "#ffcf9a", 2.5, "inferred", 1.0)]
    els += [{"k": "axis", "x0": 980, "x1": 1620, "y": 650, "ticks": [[X(1250), "1250"], [X(1200), "1200"], [X(1150), "1150"]], "t": "BCE", "in": t_clock - .2},
            rect(X(1196), 615, X(1186) - X(1196), 24, AMBER, r=12, at=t_1190, fx="pop"), lab(X(1190), 590, "about 1190 BCE", t_1190 + .2, AMBER, 30)]
    for k in range(9):
        yr = 1246 - 6 * k
        if yr < 1194:
            break
        els += tablet(X(yr) - 15, 440, 30, 38, t_stop - 1.4 + .15 * k, 3, 3, "pop", seed=k)
    for k in range(3):
        els.append(rect(X(1182 - 9 * k) - 15, 440, 30, 38, "none", DIM, 1.5, 4, t_stop + .3 + .2 * k, style="inferred"))
    els += [lab(X(1222), 420, "letters", t_stop - 1.2, DIM, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def hattusa(at, gy=640, lights=True):
    """Hattusa on its ridge at dusk: the land rising to the right, a wall with towers along the crest, a temple in the lower city,
    the citadel on its crag at the top right."""
    ridge = [(-20, gy), (300, gy - 30), (700, gy - 90), (1100, gy - 190), (1350, gy - 260), (1480, gy - 330), (1560, gy - 340), (1640, gy - 300), (1800, gy - 260), (1800, 1100), (-20, 1100)]
    out = [poly(ridge, "#4a3b2c", "#8a6a48", 2, at, curve=True)]
    crest = lambda x: gy - 60 - (x - 520) * .27 if x < 1350 else gy - 284
    wall = [(x, crest(x) - 30) for x in range(520, 1440, 20)]
    out.append(poly([(520, crest(520) + 4)] + wall + [(1430, crest(1430) + 4)], "#8a7458", "#c9b08a", 1.5, at))
    for k in range(9):
        x = 560 + 105 * k
        out.append(rect(x - 24, crest(x) - 66, 48, 66, "#9a8462", "#d8c3a0", 1.5, 2, at))
        out.append(poly([(x - 24, crest(x) - 66), (x - 16, crest(x) - 76), (x + 16, crest(x) - 76), (x + 24, crest(x) - 66)], "#9a8462", "#d8c3a0", 1.5, at))
    out += [poly([(1440, gy - 330), (1450, gy - 410), (1600, gy - 420), (1620, gy - 340)], "#9a8462", "#d8c3a0", 2, at),
            rect(1462, gy - 480, 140, 70, "#a8906a", "#e8d0a8", 2, 2, at), rect(1505, gy - 455, 50, 45, "#3a2a1c", at=at)]
    out += [rect(360, gy - 110, 230, 74, "#8a7458", "#c9b08a", 1.5, 2, at), rect(390, gy - 140, 170, 30, "#9a8462", "#c9b08a", 1.5, 2, at),
            rect(455, gy - 90, 40, 54, "#3a2a1c", at=at)]
    if lights:
        for k, (x, y) in enumerate(((475, gy - 70), (880, gy - 150), (1180, gy - 230), (1530, gy - 440), (700, gy - 110))):
            out.append(glow(x, y, 52, at, .75, "lamp"))
    return out


def s28():
    """Hattusa at dusk on its ridge. A line of small figures with carts and baskets of tablets leaves through a gate and walks off
    to the left along a dashed road; the city dims behind them."""
    sid = "s28"
    t_ha, t_emp, t_gone = T(sid, "Hattusa"), T(sid, "emptied"), T(sid, "the royal court")
    gy = 640
    els = hattusa(-1, lights=False)
    els += [lab(1000, 190, "Hattusa", t_ha, GOLD, 36, st="serif")]
    els += [ln([(560, gy - 70), (300, gy - 20), (40, gy + 10)], t_emp, DIM, 2.5, "inferred", 1.2)]
    for k in range(8):
        x = 520 - 60 * k
        y = gy - 62 + 9 * k
        if k % 3 == 1:
            els += cart_icon(x, y + 6, 40, t_gone + .2 * k, "#e8d6b8")
        else:
            els.append(figure(x, y, 52, t_gone + .2 * k, "#e8d6b8"))
    els += [lab(330, gy + 70, "the court leaves", t_gone + 1.0, DIM, 28)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [260, 360, 26], "cam": CAM, "els": els}


def s29_add():
    """The empty city burns: fire takes the citadel and the temple roofs; lilac dotted figures with torches come down from the northern
    hills ('Kaska?'); far left a ship in the claimed style with a cross: no raiders from the sea here."""
    sid = "s29"
    t_fire, t_kas, t_sea = T(sid, "Whoever lit"), T(sid, "Kaska"), T(sid, "no sign")
    gy = 640
    els = flame(1530, gy - 470, 60, t_fire) + flame(480, gy - 145, 40, t_fire + .4) + flame(1150, gy - 270, 44, t_fire + .7)
    els += [lab(1000, 250, "a ghost town", t_fire + 1.0, DIM, 28, st="ital")]
    for k in range(5):
        x = 1660 - 50 * k
        els += [figure(x, gy - 300 + 24 * k, 46, t_kas + .2 * k, LILAC, op=.6), glow(x + 10, gy - 352 + 24 * k, 26, t_kas + .2 * k, .6, "fire")]
    els += [lab(1640, gy - 410, "Kaska?", t_kas + .6, LILAC, 30)]
    els += ship_icon(170, gy - 160, 110, t_sea, LILAC, 1, op=.7, style="claimed", fill="none")
    els += [ln([(110, gy - 230), (230, gy - 110)], t_sea + .4, RED, 5, dur=.4), ln([(230, gy - 230), (110, gy - 110)], t_sea + .55, RED, 5, dur=.4)]
    return els


PELV = View(20.6, 24.4, 36.3, 38.6, (90, 120, 1600, 680))


def s30():
    """Map of the Peloponnese: Mycenae, Tiryns and Pylos flare as named; 'around 1200 BCE'."""
    sid = "s30"
    t_my, t_ti, t_py, t_12 = T(sid, "Mycenae"), T(sid, "Tiryns"), T(sid, "Pylos"), T(sid, "around")
    v = PELV
    els = map_base(v)
    for nm, t, a in (("Mycenae", t_my, "start"), ("Tiryns", t_ti, "start"), ("Pylos", t_py, "end")):
        x, y = site(v, nm)
        els += flame(x, y, 34, t) + [lab(x + (42 if a == "start" else -42), y + (-6 if nm == "Mycenae" else 26), nm, t + .1, GOLD, 32, a)]
    els += [lab(1250, 720, "around 1200 BCE", t_12, AMBER, 32), lab(*v.p(24.1, 37.9), "Aegean", .3, "#9fd0ff", 26, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def leaf_tablet(x, y, w, at, c, op=None):
    """A Linear B 'palm-leaf' tablet: long and narrow, rounded ends, a few signs."""
    out = [poly(E(x, y, w / 2, w * .12, 18), c, "#3a2a1a", 1.2, at, op=op, curve=True)]
    return out


def s31():
    """The archive room of the palace at Pylos in section: shelves of pale unbaked tablets; the fire's glow sweeps in and the
    tablets turn baked orange, one shelf after another."""
    sid = "s31"
    t_fire, t_rec, t_pw = T(sid, "the fire baked"), T(sid, "clay records"), T(sid, "paperwork")
    els = [rect(260, 160, 1260, 600, "#2a2018", "#8a6a48", 3, 4, -1), rect(240, 140, 1300, 26, "#5a4634", at=-1)]
    rr = random.Random(31)
    for r in range(4):
        y = 260 + 130 * r
        els.append(rect(300, y + 22, 1180, 14, "#6b5238", at=-1))
        for j in range(12):
            x = 350 + 96 * j + rr.uniform(-8, 8)
            els += leaf_tablet(x, y + 6, 80, -1, "#9a958c")
            els += leaf_tablet(x, y + 6, 80, t_rec + .25 * r + .03 * j, "#c8743c")
    els += [glow(1450, 600, 420, t_fire, .55, "fire"), glow(1100, 450, 600, t_fire + .5, .3, "fire")]
    els += [lab(889, 790, "Linear B tablets", t_rec + .4, BONE, 30), lab(1300, 215, "baked by the fire", t_pw, "#ffcf9a", 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def letters_ab(x, y, s, at, c=BONE):
    """Four early Greek letters drawn as strokes (alpha, beta, gamma, delta)."""
    out = [ln([(x, y), (x + .3 * s, y - s), (x + .6 * s, y)], at, c, 4, draw=False), ln([(x + .14 * s, y - .42 * s), (x + .46 * s, y - .42 * s)], at, c, 4, draw=False)]
    bx = x + .9 * s
    out += [ln([(bx, y), (bx, y - s), (bx + .3 * s, y - s), (bx + .42 * s, y - .76 * s), (bx + .3 * s, y - .52 * s), (bx, y - .52 * s), (bx + .36 * s, y - .5 * s), (bx + .46 * s, y - .25 * s), (bx + .34 * s, y), (bx, y)], at + .1, c, 4, draw=False)]
    gx = x + 1.65 * s
    out += [ln([(gx, y), (gx, y - s), (gx + .4 * s, y - s)], at + .2, c, 4, draw=False)]
    dx = x + 2.3 * s
    out += [ln([(dx, y), (dx + .3 * s, y - s), (dx + .6 * s, y), (dx, y)], at + .3, c, 4, draw=False)]
    return out


def s32():
    """A timeline 1400 to 700 BCE: a band of Linear B signs runs up to about 1200 and stops; a long empty grey gap with a bracket
    'about 400 years'; at about 800 the first letters of the Greek alphabet begin."""
    sid = "s32"
    t_van, t_four = T(sid, "writing vanished"), T(sid, "four hundred")
    X = lambda yr: round(160 + (1400 - yr) / 700 * 1460, 1)
    y = 560
    els = [{"k": "axis", "x0": 160, "x1": 1620, "y": y, "ticks": [[X(1400), "1400"], [X(1200), "1200"], [X(1000), "1000"], [X(800), "800"]], "t": "BCE", "in": .1}]
    els += [rect(X(1400), y - 70, X(1200) - X(1400), 40, "rgba(232,184,122,.25)", AMBER, 2, 8, .2), lab((X(1400) + X(1200)) / 2, y - 95, "Linear B", .4, AMBER, 30)]
    rr = random.Random(32)
    names = list(GL)
    for k in range(9):
        g = GL[rr.choice(names)]
        gx = X(1390) + 44 * k
        for stroke_ in g:
            els.append(ln([(gx + u * 30, y - 66 + v * 32) for u, v in stroke_], .4 + .05 * k, BONE, 2.2, draw=False))
    els += [rect(X(1200), y - 70, X(800) - X(1200), 40, "rgba(160,160,160,.08)", "#8a8378", 2, 8, t_van, style="inferred"),
            lab((X(1200) + X(800)) / 2, y - 95, "no writing", t_van + .4, DIM, 30)]
    els += [ln([(X(1200), y - 150), (X(1200), y - 170), (X(800), y - 170), (X(800), y - 150)], t_four, BONE, 2.5, dur=.8), lab((X(1200) + X(800)) / 2, y - 190, "about 400 years", t_four + .4, BONE, 32)]
    els += [rect(X(800), y - 70, X(700) - X(800), 40, "rgba(143,217,176,.2)", GREEN, 2, 8, t_four + .4)] + letters_ab(X(795), y - 38, 28, t_four + .5, GREEN)
    els += [lab((X(800) + X(700)) / 2, y + 100, "alphabet", t_four + .7, GREEN, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


CYV = View(32.1, 34.7, 34.4, 35.75, (90, 120, 1600, 680))


def s33():
    """Cyprus: a copper ingot; small town dots, two with fires and one fading to an empty ring; Kition glows gold as a temple outline
    and a wall draw themselves bigger than the old."""
    sid = "s33"
    t_cop, t_some, t_ki, t_gr = T(sid, "the island of"), T(sid, "Some of its"), T(sid, "Kition"), T(sid, "grander")
    v = CYV
    els = map_base(v) + [lab(*v.p(33.0, 35.25), "Cyprus", .3, DIM, 40, st="serif")]
    els += [ingot(300, 250, 110, t_cop), lab(300, 330, "copper", t_cop + .2, COPPER, 28)]
    for k, (lo, la, kind) in enumerate(((33.88, 35.15, "fire"), (33.30, 34.77, "empty"), (33.35, 34.73, "empty"))):
        x, y = v.p(lo, la)
        if kind == "fire":
            els += flame(x, y, 26, t_some + .4 * k)
        else:
            els += [dot(x, y, 9, DIM, t_some + .4 * k), circ(x, y, 22, "none", DIM, 2.5, t_some + .4 * k + .5, "pop", style="inferred")]
    kx, ky = site(v, "Kition")
    els += [dot(kx, ky, 11, GOLD, t_ki), lab(kx + 30, ky + 50, "Kition", t_ki + .1, GOLD, 32, "start")]
    els += [rect(kx - 36, ky - 74, 72, 44, "none", "#c9b08a", 2, 2, t_ki + .3, style="inferred"),
            ln([(kx - 115, ky - 10), (kx - 95, ky - 115), (kx, ky - 150), (kx + 95, ky - 115), (kx + 115, ky - 10)], t_gr, GOLD, 4, curve=True, dur=1.0),
            rect(kx - 70, ky - 130, 140, 90, "rgba(242,201,142,.18)", GOLD, 3, 2, t_gr + .4, "pop"), rect(kx - 18, ky - 90, 36, 50, "#3a2a1c", at=t_gr + .5),
            rect(kx - 84, ky - 146, 168, 16, GOLD, at=t_gr + .5, op=.8), glow(kx, ky - 90, 180, t_gr + .3, .5),
            lab(kx + 170, ky - 110, "rebuilt", t_gr + .7, GREEN, 30, "start")]
    return {"base": "map", "cam": CAM, "els": els}


RIPV = View(19, 41, 29.5, 42.5, (90, 200, 1600, 600))


def s34():
    """The eastern Mediterranean with a small timeline along the bottom (about 1225 to about 1150 BCE): its marker slides while fires
    light across the map, not in one sweep but scattered over the decades; Egypt, Carchemish and Kition stay lit in green."""
    sid = "s34"
    t_rip, t_not = T(sid, "a ripple"), T(sid, "not everyone")
    v = RIPV
    els = map_base(v)
    els += [rect(360, 150, 1060, 90, "rgba(10,20,30,.7)", r=12, at=.2), ln([(420, 180), (1360, 180)], .2, "#e9dccb", 2, draw=False),
            lab(420, 222, "about 1225", .3, DIM, 26), lab(1360, 222, "about 1150 BCE", .3, DIM, 26),
            circ(420, 180, 10, GOLD, at=t_rip - .4), {"k": "line", "p": [[420, 180], [1360, 180]], "c": GOLD, "w": 6, "fx": "draw", "dur": 4.0, "in": round(t_rip - .3, 2)}]
    order = ["Pylos", "Ugarit", "Mycenae", "Gibala", "Hattusa", "Tiryns", "Enkomi"]
    for k, nm in enumerate(order):
        x, y = site(v, nm)
        els += flame(x, y, 22, t_rip - .2 + .55 * k, .9)
    for k, (lo, la, nm) in enumerate(((31.3, 30.4, "Egypt"), (38.0, 36.83, "Carchemish"), (33.63, 34.92, "Kition"))):
        x, y = v.p(lo, la)
        els += [circ(x, y, 18, "rgba(143,217,176,.35)", GREEN, 3, t_not + .3 * k, "pop"), lab(x + (34 if nm == "Egypt" else 0), y + (8 if nm == "Egypt" else 44), nm, t_not + .3 * k + .1, GREEN, 26, "start" if nm == "Egypt" else "middle")]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== 3 Drought, hunger and quakes
def pollen(x, y, r, at, kind="tree", op=None, fx="pop"):
    """A pollen grain: round with a ring (a tree), or spiky (a dry-land plant)."""
    if kind == "tree":
        return [circ(x, y, r, "#e8c35a", "#fff1c8", 1.5, at, fx, op), circ(x, y, r * .45, "none", "#8a6a2a", 1.2, at, fx, op)]
    out = [circ(x, y, r * .8, "#c9c1ee", "#efeaff", 1.2, at, fx, op)]
    for k in range(8):
        a = k * math.pi / 4
        out.append(ln([(x + r * .8 * math.cos(a), y + r * .8 * math.sin(a)), (x + r * 1.35 * math.cos(a), y + r * 1.35 * math.sin(a))], at, "#c9c1ee", 2, draw=False, op=op))
    return out


def tree(x, gy, h, at, c="#4f6a3c"):
    return [rect(x - h * .04, gy - h * .45, h * .08, h * .45, "#5a4430", at=at, fx="rise"), poly(E(x, gy - h * .68, h * .26, h * .3, 18), c, at=at, fx="rise", curve=True)]


def shrub(x, gy, h, at, c="#8a8a52"):
    return [poly(E(x, gy - h * .35, h * .5, h * .35, 14, 180, 360) + [(x + h * .5, gy), (x - h * .5, gy)], c, at=at, fx="rise", curve=True)]


def s35():
    """A lake in section: trees on one shore, low dry-land shrubs on the other; pollen drifts down and settles in thin layers on the
    bottom; a core pulls a column out beside it, where the round tree pollen thins towards the top and spiky dry-land pollen takes over."""
    sid = "s35"
    t_lake, t_pol, t_layer, t_tree, t_dry, t_drying = (T(sid, "Lake mud"), T(sid, "pollen from"), T(sid, "layer on"), T(sid, "When tree"), T(sid, "dry-land"),
                                                        T(sid, "the land is drying"))
    gy = 330
    els = [poly([(-20, gy), (200, gy), (330, gy + 40), (360, gy + 60), (900, gy + 60), (940, gy + 40), (1080, gy), (1120, gy), (1120, 900), (-20, 900)], "#4a3b2c", "#8a6a48", 2, -1)]
    els += [poly([(330, gy + 40), (360, gy + 60), (900, gy + 60), (940, gy + 40), (930, gy + 330), (350, gy + 330)], "#1d4a66", at=-1, op=.9)]
    els += tree(120, gy, 170, .2) + tree(230, gy, 140, .3) + tree(60, gy, 120, .4)
    els += shrub(1000, gy, 60, .5) + shrub(1070, gy, 50, .6)
    rr = random.Random(35)
    for k in range(14):
        x = 380 + rr.uniform(0, 520)
        y = gy + 80 + rr.uniform(0, 200)
        els += pollen(x, y, 7, t_pol + .07 * k, "tree" if k % 4 else "dry", op=.85)
    for k in range(6):
        y = gy + 330 - 14 * k
        els.append(rect(352, y - 14, 576, 13, "#7a6248" if k % 2 else "#5a4632", at=round(t_layer + .2 * k, 2), fx="fill"))
    els += [lab(640, gy + 410, "layer on layer", t_layer + 1.0, DIM, 26)]
    cx = 1380
    els += [rect(cx - 70, 170, 140, 560, "#3a2c20", "#c9b08a", 3, 10, t_tree - .4, "pop")]
    for k in range(10):
        y = 700 - 52 * k
        nt = max(0, 5 - (k - 4)) if k >= 4 else 5
        nd = 0 if k < 5 else (k - 4)
        for j in range(nt):
            els += pollen(cx - 45 + j * 22, y - 18 + (j % 2) * 10, 7, round(t_tree + .08 * k, 2), "tree")
        for j in range(nd):
            els += pollen(cx - 40 + j * 26, y - 10 - (j % 2) * 10, 7, round(t_dry + .1 * k, 2), "dry")
    els += pollen(1490, 650, 9, t_tree + .4, "tree") + [lab(1508, 658, "tree pollen", t_tree + .5, GRAIN, 24, "start")]
    els += pollen(1490, 300, 9, t_dry + .3, "dry") + [lab(1508, 308, "dry-land plants", t_dry + .4, LILAC, 24, "start")]
    els += [arr([(1250, 700), (1250, 230)], t_drying, "#ffcf9a", 4, dur=.8, curve=False), lab(1235, 200, "drying", t_drying + .3, "#ffcf9a", 30, "end")]
    return {"base": "sky", "tod": "day", "ground": 1300, "sun": [1600, 160, 26], "cam": CAM, "els": els}


CORV = View(31.4, 38.2, 31.4, 36.7, (90, 120, 1600, 680))


def spark(x, y, at, drop_at):
    """A small chart box: a moisture line that runs level, then drops at a gold tick (about 1200 BCE)."""
    pts = [(x + 10, y + 40), (x + 50, y + 34), (x + 90, y + 42), (x + 130, y + 36), (x + 150, y + 40), (x + 170, y + 75), (x + 200, y + 82), (x + 230, y + 78)]
    return [rect(x, y, 240, 110, "rgba(18,13,10,.85)", "rgba(255,236,206,.3)", 2, 8, at, "pop"),
            ln(pts, drop_at, "#9fd0ff", 3, dur=1.2), ln([(x + 160, y + 12), (x + 160, y + 100)], drop_at + .6, GOLD, 2.5, "inferred", .4)]


def s36():
    """Map of the eastern shore: three core pins pop as named (a salt lake on Cyprus, the Syrian coast, the Sea of Galilee), each
    with a small chart whose moisture line drops at a gold tick, about 1200 BCE."""
    sid = "s36"
    t_cy, t_sy, t_ga, t_1200 = T(sid, "a salt lake"), T(sid, "the Syrian coast"), T(sid, "Sea of Galilee"), T(sid, "a long dry")
    v = CORV
    els = map_base(v)
    for nm, (lo, la), t, (bx, by), name in (("Larnaca", (33.62, 34.9), t_cy, (230, 470), "salt lake, Cyprus"), ("Gibala", (35.94, 35.37), t_sy, (1180, 220), "Syrian coast"),
                                            ("Galilee", (35.59, 32.82), t_ga, (1250, 560), "Sea of Galilee")):
        x, y = v.p(lo, la)
        els += [{"k": "pin", "x": x, "y": y, "t": name, "c": BLUE, "in": t, "a": "end" if bx < x else "start", "lx": -20 if bx < x else 20}]
        ex_, ey_ = (bx + 240, by + 55) if bx < x else (bx, by + 55)
        els += [ln([(x, y + 12), (ex_, ey_)], t + .2, BLUE, 1.6, "inferred", .5, op=.7)]
        els += spark(bx, by, t + .3, t_1200 if t_1200 > t else t + .8)
    els += [lab(889, 760, "around 1200 BCE", t_1200 + .6, GOLD, 32)]
    return {"base": "map", "cam": CAM, "els": els}


def rings_disc(cx, cy, R_, at, n=22, seed=37, step=.04):
    """A trunk's cut face: rings drawn from the centre out, some wide (wet years), some thin (dry years)."""
    rr = random.Random(seed)
    widths = [rr.choice((1.0, 1.1, .5, 1.3, .45, 1.0, .9)) for _ in range(n)]
    tot = sum(widths)
    out = [circ(cx, cy, R_ + 10, "#6b4a2c", "#3a2614", 3, at, "pop"), circ(cx, cy, R_, "#c8a070", at=at, fx="pop")]
    r = 0
    radii = []
    for k, w in enumerate(widths):
        r += w / tot * R_
        radii.append(r)
        out.append(circ(cx, cy, round(r, 1), "none", "#7a5530", 2.2 if w > .6 else 3.2, round(at + .3 + step * k, 2), "pop"))
    return out, radii, widths


def s37():
    """A sawn juniper trunk face on, its rings drawing out from the centre (a wide wet ring and a thin dry ring pointed out); then a
    strip from the bark to the centre unrolls to the right into a long barcode of years."""
    sid = "s37"
    t_ring, t_wet, t_dry, t_bar = T(sid, "A tree grows"), T(sid, "wide in a wet"), T(sid, "thin in a dry"), T(sid, "barcode")
    cx, cy, R_ = 470, 470, 260
    disc, radii, widths = rings_disc(cx, cy, R_, t_ring - .3)
    els = disc
    kw = next(k for k, w in enumerate(widths) if w >= 1.3)
    kd = next(k for k, w in enumerate(widths) if w <= .45 and k > 4)
    els += [arr([(cx + 330, cy - 200), (cx + (radii[kw] + radii[kw - 1]) / 2 * .7, cy - (radii[kw] + radii[kw - 1]) / 2 * .7)], t_wet, "#9fd0ff", 3, dur=.6),
            lab(cx + 340, cy - 215, "wet year", t_wet + .2, "#9fd0ff", 30, "start"),
            arr([(cx + 330, cy + 220), (cx + radii[kd] * .72, cy + radii[kd] * .69)], t_dry, "#ffcf9a", 3, dur=.6),
            lab(cx + 340, cy + 250, "dry year", t_dry + .2, "#ffcf9a", 30, "start")]
    x = 980
    for k, w in enumerate(widths[::-1] * 2):
        bw = 8 + 14 * w
        els.append(rect(x, 330, bw - 4, 260, "#c8a070", at=round(t_bar - .4 + .04 * k, 2), op=.95))
        x += bw
        if x > 1640:
            break
    els += [lab(1310, 640, "a barcode of years", t_bar + .5, BONE, 30)]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


GV = View(29.5, 36.6, 38.2, 41.6, (90, 120, 1600, 330))


def s38():
    """Central Turkey: Gordion and Hattusa pins with the distance between them; below, the barcode of the Gordion junipers, where three
    thin bars in a row turn red at about 1198 to 1196 BCE, give or take three years."""
    sid = "s38"
    t_gor, t_three, t_date, t_hit = T(sid, "Gordion"), T(sid, "three drought"), T(sid, "around"), T(sid, "Hittite empire")
    v = GV
    els = map_base(v)
    gx, gy_ = site(v, "Gordion")
    hx, hy = site(v, "Hattusa")
    els += [{"k": "pin", "x": gx, "y": gy_, "t": "Gordion", "c": GOLD, "in": t_gor, "a": "end", "lx": -20},
            {"k": "pin", "x": hx, "y": hy, "t": "Hattusa", "c": BONE, "in": t_hit, "a": "start", "lx": 20},
            ln([(gx + 12, gy_), (hx - 12, hy)], t_gor + .6, DIM, 2.5, "inferred", .8), lab((gx + hx) / 2, (gy_ + hy) / 2 - 22, "230 km", t_gor + 1.0, DIM, 26)]
    els += [rect(60, 470, 1660, 300, "#140e0a", at=-1)]
    rr = random.Random(38)
    x, k = 140, 0
    red = []
    while x < 1620:
        if 760 <= x < 850 and len(red) < 3:
            bw = 14
            red.append(x)
        else:
            bw = rr.choice((18, 26, 34, 14, 30))
        els.append(rect(x, 520, bw - 5, 170, "#c8a070", at=round(t_three - 1.2 + .02 * k, 2), op=.9))
        x += bw
        k += 1
    for j, xr in enumerate(red):
        els.append(rect(xr, 520, 9, 170, RED, at=round(t_three + .3 + .3 * j, 2), fx="pop"))
    x0, x1 = red[0] - 6, red[-1] + 15
    els += [ln([(x0, 505), (x0, 492), (x1, 492), (x1, 505)], t_date, GOLD, 2.5, dur=.5), lab((x0 + x1) / 2, 478, "1198 to 1196 BCE", t_date + .2, GOLD, 32),
            lab((x0 + x1) / 2, 735, "give or take 3 years", t_date + 1.2, DIM, 26)]
    return {"base": "map", "cam": CAM, "els": els}


def store_jar(x, gy, h, at, t_empty, label_t=None, name=None):
    """A storage jar cut open: grain inside in four layers; t_empty: when the layers are eaten, top first."""
    w = h * .62
    pts = [(x - .18 * w, gy - h), (x - .2 * w, gy - .93 * h), (x - .5 * w, gy - .72 * h), (x - .52 * w, gy - .45 * h), (x - .3 * w, gy - .08 * h), (x - .14 * w, gy),
           (x + .14 * w, gy), (x + .3 * w, gy - .08 * h), (x + .52 * w, gy - .45 * h), (x + .5 * w, gy - .72 * h), (x + .2 * w, gy - .93 * h), (x + .18 * w, gy - h)]
    out = [poly(pts, "#2a1f17", "#c9a878", 3, at, "rise", curve=True)]
    for k in range(4):
        y0 = gy - .12 * h - k * .16 * h
        ww = w * (.5 if k == 0 else .82 if k < 3 else .7)
        out.append(rect(x - ww / 2, y0 - .15 * h, ww, .15 * h, GRAIN, r=6, at=at + .1, op=.9))
    if t_empty is not None:
        for k in range(4):
            y0 = gy - .12 * h - (3 - k) * .16 * h
            ww = w * (.5 if 3 - k == 0 else .82 if 3 - k < 3 else .7)
            out.append(cover(x - ww / 2 - 2, y0 - .15 * h - 2, ww + 4, .15 * h + 4, round(t_empty + .25 * k, 2), "#2a1f17", 1.0, .3, 6))
    if name:
        out.append(lab(x, gy + 46, name, label_t if label_t is not None else at, DIM, 28))
    return out


def s39():
    """Three storage jars of grain in a storeroom, a dry sun over each year: the first empties (one bad year: the store covers it), then
    the second and the third: all three stand empty, 'famine'."""
    sid = "s39"
    t_one, t_three, t_fam = T(sid, "one bad"), T(sid, "Three in a"), T(sid, "famine")
    gy = 640
    els = [rect(140, gy, 1500, 16, "#5a4634", at=-1)]
    for k, x in enumerate((480, 889, 1300)):
        te = t_one + .3 if k == 0 else t_three + .2 + .4 * (k - 1)
        els += store_jar(x, gy, 330, .2 + .15 * k, te, .4 + .15 * k, "year %d" % (k + 1))
        els += [circ(x, 210, 30, "none", "#ffcf9a", 3, te - .2, "pop")] + [ln([(x + 40 * math.cos(a), 210 + 40 * math.sin(a)), (x + 54 * math.cos(a), 210 + 54 * math.sin(a))], te - .1, "#ffcf9a", 3, draw=False)
                                                                       for a in [j * math.pi / 4 for j in range(8)]]
    els += [lab(889, 760, "famine", t_fam, RED, 36, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


GRV = View(27, 39, 25.8, 41.2, (90, 120, 1600, 680))


def grain_ship(x, y, s, at, c="#2a2018", face=1):
    out = merchant(x, y, s, at, c, "plain", face)
    for k in range(3):
        out.append(poly([(x - .2 * s + k * .16 * s - .06 * s, y - .06 * s), (x - .2 * s + k * .16 * s - .07 * s, y - .16 * s), (x - .2 * s + k * .16 * s, y - .2 * s),
                         (x - .2 * s + k * .16 * s + .07 * s, y - .16 * s), (x - .2 * s + k * .16 * s + .06 * s, y - .06 * s)], GRAIN, "#8a6a2a", 1, at + .1, "pop", curve=True))
    return out


def letter_icon(x, y, at, c=CLAY):
    return tablet(x - 16, y - 20, 32, 40, at, 3, 3, "pop")


def s40():
    """The grain map: a clay letter travels from Hatti to Ugarit and a ship with sacks of grain sails from the Syrian coast towards the
    Hittite coast; then a second letter travels from Ugarit to Egypt."""
    sid = "s40"
    t_ask, t_ship, t_life, t_eg = T(sid, "A Hittite king"), T(sid, "a ship of grain"), T(sid, "life or"), T(sid, "Ugarit's king writes")
    v = GRV
    els = map_base(v)
    hx, hy = v.p(33.4, 39.3)
    ux, uy = site(v, "Ugarit")
    ex, ey = v.p(31.3, 30.3)
    els += [lab(hx, hy, "Hatti", .3, BONE, 40, st="serif"), {"k": "pin", "x": ux, "y": uy, "t": "Ugarit", "c": GOLD, "in": .4, "a": "start", "lx": 22},
            lab(ex - 30, ey + 30, "Egypt", .5, BONE, 40, st="serif")]
    els += [arr([(hx + 20, hy + 20), (hx + 120, hy + 130), (ux - 20, uy - 20)], t_ask, CLAY, 3, "inferred", 1.0)] + letter_icon(hx + 110, hy + 110, t_ask + .4)
    sx, sy = v.p(35.2, 36.2)
    els += [arr([(ux - 30, uy + 10), (sx - 40, sy + 30), v.p(34.0, 36.35)], t_ship, GRAIN, 3, "known", 1.2)] + grain_ship(sx, sy + 10, 90, t_ship + .4)
    els += [glow(ux, uy, 120, t_life, .6, "fire")]
    els += [arr([(ux - 10, uy + 30), (ux - 120, uy + 220), (ex + 30, ey - 30)], t_eg, CLAY, 3, "inferred", 1.0)] + letter_icon(ux - 110, uy + 200, t_eg + .4)
    return {"base": "map", "cam": CAM, "els": els}


def s41_add():
    """Grain ships sail from the delta north to the Hittite coast; then the three letters stack up as clay tablets beside a wheat ear."""
    sid = "s41"
    t_mer, t_down = T(sid, "boasts of sending"), T(sid, "People wrote")
    v = GRV
    ex, ey = v.p(31.3, 30.9)
    tx, ty = v.p(33.6, 36.3)
    els = [arr([(ex, ey - 20), ((ex + tx) / 2 - 80, (ey + ty) / 2), (tx, ty + 30)], t_mer, GRAIN, 3.5, "known", 1.4)]
    for k in range(3):
        f = .3 + .25 * k
        els += grain_ship(ex + (tx - ex) * f - 60 * (1 - f), ey + (ty - ey) * f, 80, t_mer + .5 + .4 * k)
    els += [rect(1240, 300, 400, 330, "rgba(18,13,10,.88)", "rgba(255,236,206,.35)", 2, 14, t_down - .2, "pop"), lab(1440, 600, "written down", t_down + .8, BONE, 28)]
    for k in range(3):
        els += tablet(1290 + 100 * k, 360 + 30 * (k % 2), 80, 100, t_down + .2 * k, 4, 3, "pop", seed=40 + k)
    els += [poly([(1580, 540), (1584, 470), (1576, 440), (1588, 400), (1600, 440), (1592, 470), (1596, 540)], GRAIN, at=t_down + .6, fx="rise")]
    return els


AEV = View(19.5, 30.5, 34.0, 41.2, (90, 120, 1600, 680))


def s42():
    """The Aegean: the arc where the African plate dives under the Aegean drawn as a toothed line south of Crete; quake rings pulse
    along it and across the Aegean."""
    sid = "s42"
    t_q, t_pl = T(sid, "quake country"), T(sid, "two plates")
    v = AEV
    els = map_base(v) + [lab(*v.p(25.2, 38.6), "Aegean", .3, "#9fd0ff", 30, st="ital")]
    arc = [v.p(20.2, 38.6), v.p(21.0, 36.6), v.p(22.6, 35.4), v.p(24.8, 34.6), v.p(27.0, 34.8), v.p(28.8, 35.6)]
    els += [ln(arc, t_pl, RED, 4, dur=1.4, curve=True)]
    for k in range(len(arc) - 1):
        (x0, y0), (x1, y1) = arc[k], arc[k + 1]
        for j in range(3):
            u = (j + .5) / 3
            px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            dx, dy = x1 - x0, y1 - y0
            d = math.hypot(dx, dy)
            nx, ny = -dy / d, dx / d
            els.append(poly([(px - dx / d * 10, py - dy / d * 10), (px + dx / d * 10, py + dy / d * 10), (px - nx * 16, py - ny * 16)], RED, at=round(t_pl + .5 + .1 * (3 * k + j), 2), fx="pop"))
    els += [lab(*v.p(23.5, 34.3), "plates meet", t_pl + 1.0, RED, 30)]
    rr = random.Random(42)
    for k in range(7):
        lo, la = rr.uniform(21.0, 28.5), rr.uniform(35.4, 39.8)
        x, y = v.p(lo, la)
        els.append(ring(round(x, 1), round(y, 1), round(rr.uniform(18, 34), 1), round(t_q + .3 * k, 2), "#ffcf9a", 2.5, dur=.5))
    return {"base": "map", "cam": CAM, "els": els}


def lion_gate(cx, gy, at, s=1.0):
    """The Lion Gate of Mycenae: two great jambs and a lintel, the relieving triangle with two lions rearing at a central column,
    walls of huge blocks on either side."""
    out = []
    rr = random.Random(43)
    for side in (-1, 1):
        x0 = cx + side * 150 * s
        x = x0
        for row in range(4):
            y = gy - row * 110 * s
            xx = x0
            while abs(xx - x0) < 620 * s:
                w = rr.uniform(120, 190) * s
                xa, xb = (xx, xx + w) if side > 0 else (xx - w, xx)
                out.append(poly([(xa + 3, y - 3), (xb - 3, y - 6 + rr.uniform(-4, 4)), (xb - 2, y - 108 * s), (xa + 2, y - 104 * s + rr.uniform(-6, 6))], "#a8906a", "#4a3a2a", 2, at))
                xx += w * side
    out += [rect(cx - 150 * s, gy - 330 * s, 300 * s, 330 * s, "#1a120c", at=at),
            rect(cx - 170 * s, gy - 330 * s, 60 * s, 330 * s, "#b8a07a", "#4a3a2a", 2, 0, at), rect(cx + 110 * s, gy - 330 * s, 60 * s, 330 * s, "#b8a07a", "#4a3a2a", 2, 0, at),
            rect(cx - 210 * s, gy - 400 * s, 420 * s, 72 * s, "#b8a07a", "#4a3a2a", 2, 0, at),
            poly([(cx - 190 * s, gy - 400 * s), (cx + 190 * s, gy - 400 * s), (cx, gy - 620 * s)], "#c9b08a", "#4a3a2a", 2, at)]
    out += [rect(cx - 14 * s, gy - 560 * s, 28 * s, 150 * s, "#8a7458", at=at), rect(cx - 40 * s, gy - 420 * s, 80 * s, 18 * s, "#8a7458", at=at),
            rect(cx - 34 * s, gy - 575 * s, 68 * s, 16 * s, "#8a7458", at=at)]
    for f in (-1, 1):                              # two lions rearing at the column, forepaws on the altar, hind legs on the lintel
        L = lambda u, v: (cx + f * u * s, gy - v * s)
        lion = [L(36, 404), L(112, 404), L(128, 420), L(150, 470), L(146, 482), L(132, 474), L(118, 446), L(104, 452), L(98, 480), L(92, 512),
                L(80, 540), L(66, 556), L(54, 560), L(40, 548), L(30, 532), L(26, 520), L(40, 518), L(52, 508), L(46, 470), L(40, 440)]
        out.append(poly(lion, "#8a7458", "#4a3a2a", 2, at))
        out.append(ln([L(132, 474), L(162, 500), L(170, 532), L(160, 548)], at, "#4a3a2a", 4, draw=False, curve=True))
    return out


def s43():
    """The Lion Gate of Mycenae at dusk: the lions over the lintel, the huge blocks of the walls; to one side a stretch of wall has
    slumped and stones lie fallen, a small lamp glow over them (no bodies drawn)."""
    sid = "s43"
    t_found = T(sid, "people were")
    gy = 720
    els = lion_gate(760, gy, .2, .95)
    rr = random.Random(44)
    for k in range(9):
        x, y = 1340 + rr.uniform(-140, 220), gy - rr.uniform(0, 60)
        w = rr.uniform(70, 130)
        els.append({"k": "group", "tr": "rotate(%d %d %d)" % (rr.uniform(-25, 25), x, y), "in": round(t_found + .1 * k, 2), "fx": "pop",
                    "els": [poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 6, y - w * .6), (x - w / 2 + 4, y - w * .55)], "#a8906a", "#4a3a2a", 2, -1)]})
    els += [glow(1380, gy - 40, 140, t_found + .6, .6, "lamp"), lab(1250, 230, "Mycenae", .5, GOLD, 36, st="serif"), lab(1250, 270, "the Lion Gate", .7, DIM, 26)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1600, 420, 28], "cam": CAM, "els": els}


def s44():
    """An earthquake storm, drawn in the claimed style: on a dark table a row of dominoes along a fault line tip over one after another
    while a quake ring pops beside each; a small timeline '1225 to 1175 BCE' under it."""
    sid = "s44"
    t_nur, t_storm, t_dom = T(sid, "the geophysicist"), T(sid, "earthquake storm"), T(sid, "like dominoes")
    els = [rect(80, 470, 1620, 230, "#241a12", "rgba(255,236,206,.2)", 2, 12, .2)]
    fault = [(140, 640), (500, 610), (900, 640), (1300, 600), (1640, 630)]
    els += [ln(fault, t_storm, RED, 3, "claimed", 1.2, curve=True), lab(889, 230, "an earthquake storm?", t_storm + .3, LILAC, 34, st="ital")]
    n = 9
    for k in range(n):
        x = 220 + 165 * k
        y = 610 + 15 * math.sin(k * .9)
        els.append(rect(x - 14, y - 110, 28, 110, "#e9dccb", "#2a2018", 2, 3, .4 + .05 * k))
        t = round(t_dom + .14 * k, 2)
        els.append(cover(x - 18, y - 114, 36, 118, t, "#241a12", 1.0, .15))
        els.append({"k": "group", "in": t, "els": [{"k": "group", "tr": "rotate(62 %g %g)" % (x + 14, y), "els": [rect(x - 14, y - 110, 28, 110, "#e9dccb", "#2a2018", 2, 3, -1)]}]})
        els.append(ring(x, y - 140, 28, round(t + .1, 2), "#ffcf9a", 2.5, dur=.4))
    els += [ln([(400, 770 - 20), (1380, 770 - 20)], t_storm + .5, "#e9dccb", 2, draw=False), lab(400, 790 - 10, "1225", t_storm + .6, DIM, 24), lab(1380, 790 - 10, "1175 BCE", t_storm + .6, DIM, 24),
            lab(889, 330, "Nur and Cline, 2000", t_nur, DIM, 26)]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


def s45():
    """A Mycenaean wall in section with a tilt, at Tiryns: a seismometer trace and a scanner beam measure it; three other causes pop
    beside it (a sagging foundation, fire, slow decay); a chip 'quake: unlikely'; then a new top course of blocks rises (rebuilt)."""
    sid = "s45"
    t_test, t_other, t_unl, t_reb = T(sid, "put Tiryns"), T(sid, "other causes"), T(sid, "unlikely"), T(sid, "usually rebuild")
    gy = 690
    els = [rect(80, gy, 1620, 120, "#3b2d22", at=-1), lab(470, 190, "Tiryns", .3, GOLD, 34, st="serif")]
    rr = random.Random(45)
    for row in range(4):
        x = 240
        while x < 700:
            w = rr.uniform(90, 140)
            y = gy - row * 90
            els.append({"k": "group", "in": -1, "els": [{"k": "group", "tr": "rotate(%g 470 %g)" % (-1.6 * row, gy), "els": [
                poly([(x + 2, y - 2), (x + w - 2, y - 4), (x + w - 2, y - 88), (x + 2, y - 86)], "#a8906a", "#4a3a2a", 2, -1)]}]})
            x += w
    els += [rect(860, gy - 120, 130, 120, "#2a2018", "#9fd0ff", 2, 6, t_test, "pop"),
            ln([(872, gy - 60), (895, gy - 90), (915, gy - 30), (935, gy - 80), (955, gy - 50), (975, gy - 60)], t_test + .3, "#9fd0ff", 2.5, dur=.6),
            ln([(1000, 300), (720, 380)], t_test + .6, "#ff8a7a", 2, dur=.4), poly([(1000, 300), (1030, 270), (1060, 300), (1030, 330)], "#9aa0a8", at=t_test + .5, fx="pop"),
            lab(925, gy + 50, "the test", t_test + .8, "#9fd0ff", 28)]
    for k, (kind, x) in enumerate((("sag", 1200), ("fire", 1380), ("decay", 1560))):
        t = t_other + .35 * k
        if kind == "sag":
            els += [arr([(x, gy - 160), (x, gy - 60)], t, AMBER, 4, dur=.5, curve=False), rect(x - 50, gy - 50, 100, 40, "#5a4632", at=t, fx="pop")]
        elif kind == "fire":
            els += flame(x, gy - 60, 50, t)
        else:
            els += [dot(x - 30 + 15 * j, gy - 30 - 10 * (j % 3), 7, "#a8906a", t + .05 * j) for j in range(5)]
    els += [lab(1380, 470, "other causes", t_other + .2, AMBER, 30)]
    els += chip(925, 470, "quake: unlikely", t_unl, GRADE["ruled"], 28)
    for k in range(4):
        els.append(rect(250 + 112 * k, gy - 448, 108, 84, "#bba27c", "#4a3a2a", 2, 2, round(t_reb + .2 * k, 2), "rise"))
    els += [lab(470, 760, "rebuilt", t_reb + .8, GREEN, 28)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


# ================================================================== 4 A web of failures
def tin_bun(x, y, s, at, fx="pop"):
    return poly(E(x, y, .5 * s, .26 * s, 16), TIN, "#eef2f5", 1.5, at, fx, curve=True)


def s46():
    """The recipe, in the order it is said: a bronze blade rises from a glowing crucible ('Bronze is a recipe'); ten copper ingots pop
    into two rows (counted); one small tin ingot; arrows lead both into the crucible."""
    sid = "s46"
    t_br, t_ten, t_one = T(sid, "Bronze is"), T(sid, "about ten parts"), T(sid, "one part")
    cx, cy = 1320, 600
    els = [poly([(cx - 130, cy - 90), (cx + 130, cy - 90), (cx + 100, cy + 40), (cx - 100, cy + 40)], "#3a2c20", "#c9a878", 3, t_br, "pop"),
           poly(E(cx, cy - 90, 120, 20, 18), "#ffb060", at=t_br + .1, op=.95, curve=True), glow(cx, cy - 100, 200, t_br + .1, .7, "fire")]
    blade = [(cx - 14, cy - 140), (cx + 14, cy - 140), (cx + 18, cy - 360), (cx, cy - 420), (cx - 18, cy - 360)]
    els += [poly(blade, "#d6a256", "#ffe2a8", 2, t_br + .4, "rise"), rect(cx - 50, cy - 150, 100, 18, "#8a5a2a", r=4, at=t_br + .4, fx="rise"),
            lab(cx + 160, cy - 300, "bronze", t_br + .7, AU, 34, "start", st="serif")]
    for k in range(10):
        x, y = 200 + 110 * (k % 5), 300 + 130 * (k // 5)
        els.append(ingot(x, y, 100, round(t_ten + .1 * k, 2)))
    els += [lab(420, 520, "10 parts copper", t_ten + .6, COPPER, 32)]
    els += [tin_bun(860, 360, 90, t_one), lab(860, 520, "1 part tin", t_one + .2, TIN, 32),
            arr([(700, 360), (1000, 330), (cx - 110, cy - 110)], t_one + .2, COPPER, 3, dur=.6), arr([(910, 370), (1100, 400), (cx - 60, cy - 110)], t_one + .3, TIN, 3, dur=.6)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


WIDE = View(18, 74, 22, 46, (90, 120, 1600, 680))


def s47():
    """A wide map: Cyprus glows copper-red; a long dashed grey route draws from Central Asia across Iran and Mesopotamia to the coast."""
    sid = "s47"
    t_cop, t_tin, t_ca = T(sid, "Copper came"), T(sid, "tin from"), T(sid, "Central Asia")
    v = WIDE
    els = map_base(v)
    cx, cy = v.p(33.2, 35.1)
    els += [glow(cx, cy, 90, t_cop, .8, "fire"), lab(cx - 20, cy + 70, "Cyprus", t_cop + .1, BONE, 30), ingot(cx - 10, cy - 70, 70, t_cop + .3), lab(cx - 10, cy - 120, "copper", t_cop + .4, COPPER, 28)]
    route = [v.p(69.0, 38.6), v.p(64.0, 36.5), v.p(58.0, 34.5), v.p(52.0, 33.8), v.p(46.0, 33.6), v.p(41.0, 35.4), v.p(37.0, 35.8)]
    els += [ln(route, t_tin, TIN, 4, "inferred", 2.2, curve=True), tin_bun(*v.p(69.0, 38.6), 60, t_ca), lab(*v.p(67.5, 41.5), "Central Asia", t_ca + .2, TIN, 30),
            lab(*v.p(55.0, 31.0), "tin", t_tin + 1.0, TIN, 30)]
    return {"base": "map", "cam": CAM, "els": els}


def s48():
    """Underwater: the Uluburun wreck on a rocky slope, rows of four-handled copper ingots, a pile of tin ingots and storage jars; a
    diver with a lamp for scale; tallies as said."""
    sid = "s48"
    t_ulu, t_cop, t_tin, t_both = T(sid, "Uluburun"), T(sid, "ten tonnes"), T(sid, "a tonne of tin"), T(sid, "Almost no kingdom")
    els = [rect(-20, -20, W_ + 40, H_ + 40, "#0d2633", at=-1), glow(900, -100, 900, -1, .25, "lamp")]
    for k in range(6):
        x = 300 + 240 * k
        els.append(poly([(x, 0), (x + 60, 0), (x + 220, 700), (x + 180, 700)], "rgba(200,230,255,.05)", at=-1))
    els += [poly([(-20, 760), (300, 690), (700, 640), (1200, 660), (1600, 600), (1800, 620), (1800, 1020), (-20, 1020)], "#2d2a24", "#5a5040", 2, -1, curve=True)]
    els += [poly([(420, 660), (1280, 640), (1300, 600), (440, 615)], "#3a2c20", "#6b5238", 2, .2, op=.8)]
    for r in range(3):
        for j in range(8):
            x, y = 520 + 92 * j + 18 * r, 600 - 46 * r
            els.append(ingot(x, y, 84, round(.4 + .03 * (r * 8 + j), 2), "#b06a3a"))
    for j in range(7):
        els.append(tin_bun(1120 + 38 * (j % 4), 560 - 26 * (j // 4), 46, round(.9 + .05 * j, 2)))
    for j in range(3):
        x = 380 - 60 * j
        els.append(poly([(x - 18, 650), (x - 30, 590), (x - 22, 540), (x - 8, 528), (x + 8, 528), (x + 22, 540), (x + 30, 590), (x + 18, 650)], "#8a6440", "#c9a878", 1.5, 1.0 + .1 * j, curve=True))
    els += [figure(1450, 470, 140, .8, "#c8d6dc"), glow(1400, 420, 120, .9, .6, "lamp")]
    els += [lab(889, 180, "Uluburun, about 1300 BCE", t_ulu, GOLD, 32, st="serif"), lab(760, 760, "about 10 tonnes of copper", t_cop, COPPER, 32),
            lab(1250, 470, "about 1 tonne of tin", t_tin, TIN, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s49_add():
    """On the wide map: small ingot dots pass along the sea lanes; a red strike cuts one lane, then another, and the dots stop."""
    sid = "s49"
    t_raid, t_pay, t_stop = T(sid, "Raiders on"), T(sid, "a buyer"), T(sid, "the bronze stops")
    v = WIDE
    lanes = [[v.p(33.2, 35.1), v.p(28.0, 35.8), v.p(23.0, 37.4)], [v.p(33.2, 35.1), v.p(32.6, 33.0), v.p(31.6, 31.4)], [v.p(33.2, 35.1), v.p(34.6, 35.4), v.p(35.8, 35.6)]]
    els = []
    for k, lane in enumerate(lanes):
        els.append(ln(lane, .2 + .2 * k, COPPER, 3, "inferred", .8, curve=True))
        for j in range(5):
            u = (j + .5) / 5
            (x0, y0), (x1, y1), (x2, y2) = lane
            x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * x1 + u * u * x2
            y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * y1 + u * u * y2
            stop = (k == 0 and j > 1) or (k == 1 and j > 2)
            els.append(dot(round(x, 1), round(y, 1), 7, COPPER, round(.6 + .25 * j + .1 * k, 2) if not stop else 99))
    for k, (lane, t) in enumerate(((lanes[0], t_raid), (lanes[1], t_pay))):
        (x0, y0), (x1, y1), (x2, y2) = lane
        mx, my = .25 * x0 + .5 * x1 + .25 * x2, .25 * y0 + .5 * y1 + .25 * y2
        els += [strike(round(mx - 22, 1), round(my - 22, 1), round(mx + 22, 1), round(my + 22, 1), round(t + .3, 2)),
                strike(round(mx + 22, 1), round(my - 22, 1), round(mx - 22, 1), round(my + 22, 1), round(t + .45, 2))]
    els += [lab(889, 230, "the bronze stops", t_stop, RED, 32, st="serif")]
    return els


def s50():
    """Two coasts across a strip of sea (Cyprus left, Ugarit right): a clay letter sails from Cyprus to Ugarit; then Ugarit's own ships,
    in Ugarit's amber, turn round in dotted arcs towards their own coast."""
    sid = "s50"
    t_off, t_own = T(sid, "A senior official"), T(sid, "your own")
    els = [{"k": "water", "y": 300, "h": 700, "x0": -100, "x1": 1900, "op": .9, "in": -1},
           poly([(-20, 260), (260, 300), (420, 420), (380, 600), (220, 760), (-20, 800)], "#4a3b2c", "#8a6a48", 2, -1, curve=True),
           poly([(1800, 220), (1500, 260), (1380, 420), (1420, 620), (1560, 780), (1800, 820)], "#4a3b2c", "#8a6a48", 2, -1, curve=True),
           lab(200, 500, "Cyprus", .3, BONE, 34, st="serif"), lab(1600, 500, "Ugarit", .3, GOLD, 34, st="serif")]
    els += [arr([(440, 400), (889, 320), (1360, 400)], t_off, CLAY, 3, "inferred", 1.2)] + tablet(870, 280, 40, 50, t_off + .6, 3, 3, "pop", seed=50)
    for k in range(3):
        x, y = 1100 - 130 * k, 610 + 24 * k
        els += ship_icon(x, y, 90, t_own - .2 + .2 * k, AMBER, -1)
        els.append(arr([(x - 60, y + 6), (x - 110, y + 40), (x + 40, y + 56), (1380, y + 10)], t_own + .4 + .2 * k, AMBER, 3, "claimed", 1.0))
    els += [lab(960, 760, "your own ships?", t_own + 1.0, AMBER, 32, st="ital")]
    return {"base": "sky", "tod": "day", "ground": 1300, "sun": False, "cam": CAM, "els": els}


def squat(x, gy, h, at, c="#2a1f17"):
    """A person sitting on the ground, knees up, facing right (h = standing height)."""
    out = [circ(x, gy - .62 * h, .085 * h, c, at=at, fx="rise"),
           poly([(x - .12 * h, gy - .52 * h), (x + .08 * h, gy - .52 * h), (x + .06 * h, gy - .2 * h), (x - .14 * h, gy - .02 * h), (x - .16 * h, gy - .3 * h)], c, at=at, fx="rise"),
           poly([(x - .12 * h, gy - .02 * h), (x + .02 * h, gy - .24 * h), (x + .26 * h, gy - .26 * h), (x + .3 * h, gy), (x + .22 * h, gy), (x + .2 * h, gy - .14 * h), (x + .02 * h, gy - .06 * h)], c, at=at, fx="rise")]
    return out


def s51():
    """The Theban cliffs at dusk, a temple wall; the royal tomb builders sit down in its shade, chisels and mallets laid on the ground;
    an empty grain basket glows."""
    sid = "s51"
    t_tools, t_hungry, t_first = T(sid, "put down"), T(sid, "We are"), T(sid, "first strike")
    gy = 660
    els = [poly([(-20, 400), (200, 330), (500, 300), (800, 340), (1100, 280), (1400, 320), (1800, 300), (1800, gy), (-20, gy)], "#7a5a3a", "#b08a60", 2, -1, curve=True),
           rect(980, 380, 600, gy - 380, "#c9a878", "#f2dcb4", 2, 0, .2), rect(980, 360, 620, 26, "#b8946a", at=.2)]
    for k in range(6):
        x = 1020 + 92 * k
        els.append(ln([(x, 420), (x, gy - 30)], .4, "#8a6a48", 3, draw=False, op=.5))
    for k, x in enumerate((420, 520, 620, 720, 820)):
        els += squat(x, gy, 96, t_tools + .15 * k, "#2a1f17")
    for k in range(4):
        x = 460 + 110 * k
        els += [ln([(x, gy + 18), (x + 40, gy + 6)], t_tools + .8 + .1 * k, "#cbd2d8", 4, draw=False), rect(x + 40, gy, 22, 14, "#8a6a48", r=3, at=t_tools + .8 + .1 * k)]
    els += [poly([(860, gy + 30), (960, gy + 30), (944, gy - 30), (876, gy - 30)], "#8a6440", "#e8c35a", 2, t_hungry, "pop"), glow(910, gy, 100, t_hungry, .6, "lamp"),
            lab(910, gy + 80, "no grain", t_hungry + .2, GRAIN, 28), lab(620, gy + 80, "tomb builders", t_tools + .4, DIM, 28),
            lab(1280, 330, "the first strike on record", t_first, BONE, 30, st="ital")]
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1650, 240, 26], "cam": CAM, "els": els}


def s52():
    """A dark palace hall: an empty throne with the blue crown resting on it; a lamp beside it gutters and dims."""
    sid = "s52"
    t_plot = T(sid, "palace")
    gy = 700
    els = [rect(-20, gy, W_ + 40, 300, "#1a120c", at=-1)]
    for k in range(4):
        x = 300 + 400 * k
        els.append(rect(x - 30, 160, 60, gy - 160, "#2a2018", "#4a3a2a", 2, 0, -1))
    els += [rect(780, gy - 260, 230, 30, "#7a5a3a", "#c9a878", 2, 4, .2), rect(800, gy - 230, 190, 230, "#5a4030", "#c9a878", 2, 4, .2),
            rect(790, gy - 470, 40, 240, "#6a4c34", "#c9a878", 2, 4, .2)]
    crown = [(860, gy - 270), (850, gy - 320), (870, gy - 370), (905, gy - 392), (945, gy - 380), (965, gy - 340), (960, gy - 290), (950, gy - 270)]
    els += [poly(crown, CROWN, "#cfd8e3", 2, .5, "pop", curve=True)]
    els += [glow(1180, gy - 240, 200, .3, .55, "lamp"), rect(1170, gy - 210, 20, 210, "#5a4030", at=-1), poly([(1170, gy - 230), (1180, gy - 262), (1190, gy - 230)], "#ffe2a8", at=.3, curve=True),
            cover(1100, gy - 330, 160, 140, t_plot + .6, "#120c08", .55, 1.6)]
    return {"base": "dark", "cam": CAM, "els": els}


WEB_N = [("drought", "drought"), ("hunger", "hunger"), ("quakes", "quake"), ("raiders", "ship"), ("revolt", "revolt"), ("trade", "trade")]


def web_nodes(cx=889, cy=470, rx=430, ry=230):
    return [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * k / 6), cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * k / 6)) for k in range(6)]


def s53():
    """A web of six nodes, every node linked to every other by thin threads (a perfect storm, a systems collapse); one thread snaps and
    the web holds; four more snap and it sags apart; then the six causes light as they are named, and all glow at once."""
    sid = "s53"
    t_storm, t_one, t_five, t_tears = T(sid, "perfect storm"), T(sid, "cut one"), T(sid, "cut five"), T(sid, "it tears")
    names = {nm: T(sid, w) for nm, w in (("drought", "Drought"), ("hunger", "hunger"), ("quakes", "quakes"), ("raiders", "raiders"), ("revolt", "revolt and"), ("trade", "broken trade"))}
    t_once = T(sid, "not all at")
    nodes = web_nodes()
    els = []
    pairs = [(a, b) for a in range(6) for b in range(a + 1, 6)]
    for k, (a, b) in enumerate(pairs):
        els.append(ln([nodes[a], nodes[b]], round(t_storm + .05 * k, 2), "#8a8378", 2, dur=.6))
    for k, ((nm, kind), (x, y)) in enumerate(zip(WEB_N, nodes)):
        els += [circ(x, y, 58, "#1d1611", "rgba(255,236,206,.45)", 2.5, t_storm + .2 + .1 * k, "pop")] + icon(kind, x, y, 66, t_storm + .3 + .1 * k, BONE)
        side = abs(x - 889) < 10
        lx, ly, la = (x + 82, y + 10, "start") if side else (x, y + (96 if y > 470 else -80), "middle")
        els += [ring(round(x, 1), round(y, 1), 66, round(names[nm], 2), GOLD, 4, dur=.4), lab(lx, ly, nm, names[nm] + .1, GOLD, 30, la)]
    cuts = [(0, 3), (1, 4), (2, 5), (0, 2), (3, 5)]
    for j, (a, b) in enumerate(cuts):
        (x0, y0), (x1, y1) = nodes[a], nodes[b]
        mx, my = (x0 + x1) / 2 + (j - 2) * 16, (y0 + y1) / 2 + (j - 2) * 10
        t = t_one + .4 if j == 0 else t_five + .3 + .2 * (j - 1)
        els += [strike(round(mx - 16, 1), round(my - 16, 1), round(mx + 16, 1), round(my + 16, 1), round(t, 2)), strike(round(mx + 16, 1), round(my - 16, 1), round(mx - 16, 1), round(my + 16, 1), round(t + .1, 2))]
    els += [lab(889, 470, "holds", t_one + .9, GREEN, 30), cover(800, 440, 180, 50, t_five + .2, "#1d1611", 1.0, .3), lab(889, 470, "tears", t_tears, RED, 34, st="serif")]
    els += [glow(x, y, 120, round(t_once, 2), .45, "fire") for x, y in nodes]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


MOS = [("Pylos", "fire"), ("Mycenae", "fire"), ("Tiryns", "fire"), ("Hattusa", "empty"), ("Ugarit", "fire"), ("Gibala", "fire"), ("Enkomi", "fire"), ("Kition", "rebuilt"),
       ("Carchemish", "survived")]


def fate(x, y, kind, at):
    if kind == "fire":
        return flame(x, y, 24, at)
    if kind == "empty":
        return [circ(x, y, 18, "none", DIM, 3, at, "pop", style="inferred")]
    if kind == "survived":
        return [circ(x, y, 16, "rgba(143,217,176,.35)", GREEN, 3, at, "pop")]
    return [circ(x, y, 16, "rgba(232,195,90,.35)", AU, 3, at, "pop")]


def s54():
    """The catch: a storm of everything explains anything (a swirl and a question). Then the eastern Mediterranean as a mosaic of fates,
    each site with its own mark (burned, abandoned, survived, rebuilt) and a small key."""
    sid = "s54"
    t_catch, t_any, t_km = T(sid, "The catch"), T(sid, "almost anything"), T(sid, "Bernard Knapp")
    v = RIPV
    els = map_base(v)
    els += [poly(E(300, 250, 90, 60, 20), "none", LILAC, 3, t_catch, "draw", curve=True), poly(E(300, 250, 55, 34, 16), "none", LILAC, 3, t_catch + .2, "draw", curve=True)]
    els += qm(300, 280, t_any, 90)
    els += [lab(300, 380, "explains anything?", t_any + .3, LILAC, 28, st="ital")]
    for k, (nm, kind) in enumerate(MOS):
        x, y = site(v, nm)
        els += fate(x, y, kind, round(t_km + .3 * k, 2))
    x, y = v.p(31.3, 30.6)
    els += fate(x, y, "survived", round(t_km + .3 * len(MOS), 2))
    kx, ky = 1320, 600
    els += [rect(kx - 30, ky - 50, 360, 190, "rgba(10,20,30,.75)", "rgba(255,236,206,.3)", 2, 12, t_km)]
    for k, (kind, nm) in enumerate((("fire", "burned"), ("empty", "abandoned"), ("survived", "survived"))):
        yy = ky + 55 * k
        els += fate(kx + 20, yy + (12 if kind == "fire" else 0), kind, t_km + .2 + .2 * k) + [lab(kx + 60, yy + 9, nm, t_km + .3 + .2 * k, BONE, 28, "start")]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== 5 The weighing
def ledger(rows, t_rows):
    """A ledger board of three rows: (picture kind, row words, grade text, grade colour key), each lighting as its time comes."""
    els = [rect(110, 150, 1560, 600, "rgba(18,13,10,.8)", "rgba(255,236,206,.3)", 2, 18, .2)]
    for k, ((kind, words_, grade, gk), (t_row, t_grade)) in enumerate(zip(rows, t_rows)):
        y = 260 + 180 * k
        els += [rect(140, y - 70, 1500, 140, "rgba(242,201,142,.06)", "rgba(242,201,142,.25)", 1.5, 14, .3 + .1 * k),
                rect(140, y - 70, 1500, 140, "rgba(242,201,142,.10)", "rgba(242,201,142,.5)", 1.5, 14, t_row, "pop")]
        els += icon(kind, 250, y, 80, t_row + .05, BONE)
        els += [lab(360, y + 12, words_, t_row + .1, BONE, 36, "start")]
        els += chip(1430, y, grade, t_grade, GRADE[gk], 32)
    return els


def s55():
    """The ledger, first half: raiders and migrants (Established), drought (Strong evidence), hunger (Strong evidence), each chip
    popping as its grade is said."""
    sid = "s55"
    t = [(T(sid, "Raiders and migrants"), T(sid, "established")), (T(sid, "Drought"), T(sid, "strong evidence")), (T(sid, "Hunger"), T(sid, "strong evidence", k=2))]
    rows = [("ship", "raiders and migrants", "Established", "established"), ("drought", "drought", "Strong evidence", "strong"), ("hunger", "hunger", "Strong evidence", "strong")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": ledger(rows, t)}


def s56():
    """The ledger, second half: earthquakes (Open question), broken trade (Plausible), revolt from within (Awaiting evidence)."""
    sid = "s56"
    t = [(T(sid, "Earthquakes"), T(sid, "open question")), (T(sid, "Broken trade"), T(sid, "plausible")), (T(sid, "Revolt from"), T(sid, "awaiting evidence"))]
    rows = [("quake", "earthquakes", "Open question", "open"), ("trade", "broken trade", "Plausible", "plausible"), ("revolt", "revolt from within", "Awaiting evidence", "awaiting")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": ledger(rows, t)}


def s57_add():
    """On the web of six: a chip 'Plausible' at the centre, 'hard to test' under it."""
    sid = "s57"
    t_pl, t_hard = T(sid, "plausible"), T(sid, "hard to test")
    return [cover(760, 430, 260, 70, t_pl - .3, "#1d1611", 1.0, .3)] + chip(889, 470, "Plausible", t_pl, GRADE["plausible"], 34) + [lab(889, 540, "hard to test", t_hard, DIM, 28)]


def s58_add():
    """On the mosaic map: one dotted lilac arrow tries to tie every fire to a single ship, and a chip 'Ruled out' pops over it."""
    sid = "s58"
    t_one, t_ro = T(sid, "One culprit"), T(sid, "ruled out")
    v = RIPV
    sx, sy = 889, 640
    els = ship_icon(sx, sy, 90, t_one, LILAC, 1, style="claimed", fill="none")
    for k, (nm, kind) in enumerate(MOS):
        if kind != "fire":
            continue
        x, y = site(v, nm)
        els.append(ln([(sx, sy - 40), (x, y + 10)], round(t_one + .2 + .1 * k, 2), LILAC, 2, "claimed", .6))
    els += chip(889, 300, "Ruled out", t_ro, GRADE["ruled"], 36)
    return els


def s59():
    """The verdict: the bird-head ship of the relief in the centre of a dim ring of the other five causes; a large chip 'Mixed record'
    pops at the verdict; at 'like a fever' a thermometer at the side fills red while the ring behind the ship glows warmer."""
    sid = "s59"
    t_q, t_mixed, t_real, t_one, t_fever = T(sid, "So, did"), T(sid, "Mixed record"), T(sid, "They were real"), T(sid, "one cause among"), T(sid, "like a fever")
    els = [rect(470, 250, 840, 420, WALL, "rgba(255,236,206,.3)", 2, 18, .2)]
    ship, _ = sp_ship(889, 520, 420, .3, ("feather", "horn", "feather", "feather"))
    els += [{"k": "group", "els": ship, "in": .3}]
    nodes = [(889 + 620 * math.cos(a), 460 + 260 * math.sin(a)) for a in [math.radians(d) for d in (150, 180, 210, 330, 30)]]
    for k, ((kind), (x, y)) in enumerate(zip(["drought", "hunger", "quake", "trade", "revolt"], nodes)):
        els += [circ(x, y, 52, "#1d1611", "rgba(255,236,206,.3)", 2, t_one + .15 * k, "pop")] + icon(kind, x, y, 58, t_one + .1 + .15 * k, DIM)
    els += chip(889, 210, "Mixed record", t_mixed, GRADE["mixed"], 40)
    els += [lab(889, 740, "one cause among several", t_one + .8, BONE, 30)]
    tx, ty = 1660, 560
    els += [rect(tx - 16, ty - 220, 32, 230, "rgba(255,255,255,.08)", BONE, 2, 16, t_fever), circ(tx, ty + 30, 30, RED, BONE, 2, t_fever, "pop"),
            rect(tx - 9, ty - 190, 18, 210, RED, r=9, at=t_fever + .3, fx="fill"), glow(889, 460, 520, t_fever + .4, .3, "fire")]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


COLS = ["Pylos", "Mycenae", "Hattusa", "Ugarit", "Gibala", "Enkomi"]


def s60():
    """Six small site columns side by side, each with a burnt layer; dashed lines drop from each burnt layer to a timeline below
    (1220 to 1170 BCE), where dashed dots line up in an order not yet known."""
    sid = "s60"
    t_q, t_dec, t_first = T(sid, "What would settle"), T(sid, "Destruction layers"), T(sid, "who fell first")
    rr = random.Random(60)
    els = []
    for k, nm in enumerate(COLS):
        x = 230 + 265 * k
        els += [rect(x - 60, 220, 120, 260, "#5a4632", "#8a7458", 2, 6, t_dec + .12 * k, "rise")]
        for j in range(4):
            els.append(rect(x - 58, 240 + 58 * j, 116, 20, "#7a6248" if j % 2 else "#6b5540", at=t_dec + .12 * k + .1))
        by = 300 + rr.choice((0, 30, 60, 90))
        els += [rect(x - 58, by, 116, 22, "#3a1a10", at=t_dec + .12 * k + .2), glow(x, by + 10, 70, t_dec + .12 * k + .3, .5, "fire"),
                lab(x, 520, nm, t_dec + .12 * k + .3, DIM, 24), ln([(x, by + 30), (x, 650)], t_dec + .8 + .1 * k, "#ffcf9a", 2, "inferred", .6)]
        els += [circ(x, 650, 12, "none", "#ffcf9a", 2.5, t_first + .1 * k, "pop", style="inferred")]
    els += [ln([(160, 650), (1620, 650)], t_dec + .6, "#e9dccb", 2, draw=False), lab(889, 720, "who fell first?", t_first + .6, "#ffcf9a", 32, st="ital")]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


def ring_icon(x, y, r, at, solid=True, c="#c8a070"):
    out = [circ(x, y, r, "rgba(200,160,112,.25)" if solid else "none", c, 2.5, at, "pop", style="known" if solid else "inferred")]
    for k in range(1, 4):
        out.append(circ(x, y, round(r * k / 4, 1), "none", c, 1.5, at + .05, "pop", style="known" if solid else "inferred"))
    return out


def s61():
    """The eastern Mediterranean: a solid tree-ring icon at Gordion; dashed ring icons pop at the coasts (Greece, Cyprus, the Levant):
    records still wanted."""
    sid = "s61"
    t_coast, t_tur = T(sid, "from the coasts"), T(sid, "central Turkey")
    v = RIPV
    els = map_base(v)
    gx, gy_ = site(v, "Gordion")
    els += ring_icon(gx, gy_, 34, .3) + [lab(gx, gy_ - 50, "Gordion", .4, GOLD, 28)]
    for k, nm in enumerate(("Mycenae", "Enkomi", "Ugarit", "Ashkelon")):
        x, y = v.p(*SITES[nm]) if nm != "Ashkelon" else v.p(34.4, 31.7)
        els += ring_icon(x, y, 30, t_coast + .25 * k, False, "#ffcf9a")
    els += [lab(889, 760, "wanted", t_coast + 1.0, "#ffcf9a", 32, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def helix(x0, x1, y, amp, at, c=BLUE):
    n = 40
    out = []
    for ph in (0, math.pi):
        out.append(ln([(x0 + (x1 - x0) * k / n, y + amp * math.sin(k * .5 + ph)) for k in range(n + 1)], at, c, 3.5, dur=1.0, curve=True))
    for k in range(0, n, 3):
        x = x0 + (x1 - x0) * k / n
        out.append(ln([(x, y + amp * math.sin(k * .5)), (x, y + amp * math.sin(k * .5 + math.pi))], at + .5, c, 1.5, draw=False, op=.6))
    return out


def s62():
    """A DNA helix draws itself; on a small map dashed arrows link the Aegean and the Philistine coast; a tooth beside it glows with
    layered bands (the chemistry that remembers where a child grew up)."""
    sid = "s62"
    t_dna, t_ae, t_teeth = T(sid, "More ancient DNA"), T(sid, "Aegean"), T(sid, "the chemistry")
    els = helix(160, 760, 300, 60, t_dna) + [lab(460, 410, "DNA", t_dna + .4, BLUE, 32)]
    v = View(20, 37, 30.5, 40.5, (160, 470, 640, 300))
    els += [{"k": "group", "clip": [150, 460, 660, 320, 12], "bg": "#0d1b26", "in": round(t_dna + .3, 2), "els": [{"k": "map", "land": v.land(), "landc": "#3d3226"}]},
            rect(150, 460, 660, 320, "none", "rgba(255,236,206,.3)", 2, 12, t_dna + .3)]
    a, b = v.p(24.5, 37.5), v.p(34.4, 31.7)
    els += [arr([a, ((a[0] + b[0]) / 2, a[1] - 40), b], t_ae, BLUE, 3, "inferred", 1.0)]
    tx, ty = 1280, 470
    tooth = [(tx - 90, ty - 160), (tx + 90, ty - 160), (tx + 110, ty - 60), (tx + 80, ty + 40), (tx + 60, ty + 230), (tx + 20, ty + 240), (tx, ty + 90), (tx - 20, ty + 240), (tx - 60, ty + 230),
             (tx - 80, ty + 40), (tx - 110, ty - 60)]
    els += [poly(tooth, "#efe6d2", "#b8a888", 2, t_teeth, "pop", curve=True)]
    for k in range(5):
        els.append(ln([(tx - 80 + 6 * k, ty - 120 + 34 * k), (tx + 80 - 6 * k, ty - 120 + 34 * k)], t_teeth + .3 + .15 * k, ("#9fd0ff", "#8fd9b0", "#e8c86a", "#9fd0ff", "#c9c1ee")[k], 4, dur=.4, curve=False))
    els += [lab(tx, ty + 300, "teeth", t_teeth + .5, BONE, 30)]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


def s63():
    """A storeroom by lamplight: shelves of boxes holding small clay tablets that pop in by the dozen to about a hundred; one glows."""
    sid = "s63"
    t_100, t_read = T(sid, "a hundred tablets"), T(sid, "waiting")
    els = [rect(200, 160, 1380, 600, "#20170f", "#5a4634", 3, 6, -1), glow(300, 300, 300, -1, .5, "lamp")]
    k = 0
    for r in range(4):
        y = 230 + 140 * r
        els.append(rect(230, y + 92, 1320, 14, "#5a4634", at=-1))
        for j in range(25):
            if k >= 100:
                break
            x = 260 + 52 * j
            els += tablet(x, y + 30, 36, 60, round(t_100 + .02 * k, 2), 3, 2, "pop", seed=k)
            k += 1
    els += [glow(260 + 52 * 12 + 18, 230 + 140 * 2 + 60, 80, t_read, .7, "lamp"), lab(889, 790 - 10, "about 100 tablets, still unpublished", t_100 + 1.0, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s64():
    """The trade map of the great kingdoms at night: its glowing routes break one after another, faster towards the end, and the
    whole map darkens."""
    sid = "s64"
    t_rich, t_fall, t_once = T(sid, "A connected world"), T(sid, "fall faster"), T(sid, "fail at")
    v = NEV
    els = map_base(v, night=True)
    hubs = {"eg": v.p(31.2, 29.8), "ha": v.p(33.2, 38.6), "ba": v.p(44.2, 32.8), "as": v.p(43.0, 36.0), "my": v.p(22.9, 37.4), "cy": v.p(33.3, 35.0), "ug": v.p(35.8, 35.6)}
    routes = [("eg", "ha"), ("eg", "cy"), ("cy", "my"), ("eg", "ba"), ("ha", "as"), ("my", "eg"), ("ug", "cy"), ("ug", "ha"), ("ug", "ba"), ("my", "ha")]
    for k, (a, b) in enumerate(routes):
        (x0, y0), (x1, y1) = hubs[a], hubs[b]
        mx, my = (x0 + x1) / 2 + (y1 - y0) * .12, (y0 + y1) / 2 - (x1 - x0) * .12
        els.append(ln([(x0, y0), (mx, my), (x1, y1)], round(.2 + .1 * k, 2), GOLD, 3, curve=True, dur=.6, op=.9))
        tb = t_fall + 2.2 * (1 - (1 - k / len(routes)) ** .5)
        els += [strike(round(mx - 14, 1), round(my - 14, 1), round(mx + 14, 1), round(my + 14, 1), round(tb, 2), RED, 4)]
    for nm, (x, y) in hubs.items():
        els.append(glow(x, y, 60, .3, .7, "lamp"))
    els += [cover(-20, -20, W_ + 40, H_ + 40, t_once + .2, "#05070a", .55, 1.5)]
    return {"base": "map", "sea": "#0b1822", "cam": CAM, "els": els}


PHOEN = [
    [[(.9, .1), (.2, .5), (.9, .9)], [(.6, .02), (.42, .98)]],
    [[(.25, 1.0), (.62, .62), (.62, .12), (.2, .12), (.2, .62), (.62, .62)]],
    [[(.25, 1.0), (.55, .1), (.82, .42)]],
    [[(.3, .95), (.3, .1), (.82, .5), (.3, .95)]],
    [[(.8, .1), (.25, .1)], [(.8, .4), (.25, .4)], [(.8, .7), (.25, .7)], [(.25, .1), (.25, .95)]],
    [[(.5, 1.0), (.5, .35)], [(.2, .1), (.5, .35), (.8, .1)]],
    [[(.2, .2), (.8, .2)], [(.5, .2), (.5, .8)], [(.2, .8), (.8, .8)]],
    [[(.25, .1), (.25, .92)], [(.75, .1), (.75, .92)], [(.25, .38), (.75, .3)], [(.25, .62), (.75, .55)]],
    [[(.5 + .38 * math.cos(a / 8 * math.pi), .5 + .38 * math.sin(a / 8 * math.pi)) for a in range(17)], [(.3, .3), (.7, .7)], [(.7, .3), (.3, .7)]],
    [[(.3, .2), (.7, .4), (.3, .6), (.7, .8)]],
    [[(.5, 1.0), (.5, .4)], [(.2, .1), (.5, .4), (.8, .1)]],
    [[(.32, .1), (.32, .75), (.78, .95)]],
    [[(.08, .3), (.28, .1), (.5, .3), (.72, .1), (.92, .3)], [(.92, .3), (.72, 1.0)]],
    [[(.3, .1), (.62, .42), (.42, 1.0)]],
    [[(.5, .1), (.5, 1.0)], [(.2, .25), (.8, .25)], [(.2, .5), (.8, .5)], [(.2, .75), (.8, .75)]],
    [[(.5 + .35 * math.cos(a / 8 * math.pi), .5 + .35 * math.sin(a / 8 * math.pi)) for a in range(17)]],
    [[(.6, 1.0), (.6, .4), (.3, .18)]],
    [[(.2, .1), (.5, .5), (.8, .1)], [(.5, .5), (.5, 1.0)], [(.5, .62), (.82, .82)]],
    [[(.5 + .25 * math.cos(a / 8 * math.pi), .35 + .25 * math.sin(a / 8 * math.pi)) for a in range(17)], [(.5, .1), (.5, 1.0)]],
    [[(.32, 1.0), (.32, .1), (.72, .26), (.32, .46)]],
    [[(.08, .2), (.3, .82), (.5, .3), (.7, .82), (.92, .2)]],
    [[(.2, .2), (.8, .8)], [(.8, .2), (.2, .8)]],
]


def s65():
    """Dawn over the sea off the Levant coast; a small ship sails; twenty-two simple letters draw themselves one by one along its wake;
    the first, an ox-head aleph, is echoed by a capital A. The camera holds still for the end card."""
    sid = "s65"
    t_ruins, t_22, t_anc, t_now = T(sid, "Yet in the ruins"), T(sid, "twenty-two"), T(sid, "the likely ancestor"), T(sid, "reading now")
    gy = 560
    els = [{"k": "water", "y": gy, "h": 500, "x0": -100, "x1": 1900, "op": .9, "in": -1},
           poly([(1500, gy + 4), (1600, gy - 50), (1700, gy - 70), (1800, gy - 80), (1800, gy + 4)], "#2b2328", at=-1, curve=True)]
    els += merchant(1460, gy + 30, 150, .3, "#1d1611", "plain", -1)
    els += [ln([(1380, gy + 40), (1000, gy + 70), (500, gy + 80), (100, gy + 70)], t_ruins, "#e8d8b8", 2, "inferred", 1.6, curve=True, op=.6)]
    x0, y0, cw = 120, 300, 66
    for k, g in enumerate(PHOEN):
        x = 1560 - 140 - k * cw if False else x0 + k * cw
        t = round(t_22 - .8 + .12 * k, 2)
        for stroke_ in g:
            els.append(ln([(x + u * 46, y0 + v * 62) for u, v in stroke_], t, "#f2dcb4", 4, dur=.3))
    els += [lab(889, 230, "22 letters", t_22 + .4, DIM, 28)]
    els += [ring(x0 + 23, y0 + 31, 46, t_anc, GOLD, 3, dur=.5), arr([(x0 + 23, y0 + 90), (x0 + 23, y0 + 160)], t_anc + .3, GOLD, 3, dur=.4, curve=False),
            lab(x0 + 23, y0 + 245, "A", t_anc + .6, GOLD, 90, st="serif", fx="pop")]
    els += [glow(760, 500, 500, t_now, .35, "sun")]
    return {"base": "sky", "tod": "dawn", "ground": 1300, "sun": [760, 500, 36], "cam": CAM, "els": els}


# ================================================================== placeholders for the shots still to draw
def _todo(sid):
    return {"base": "dark", "stars": 20, "cam": CAM, "els": [lab(889, 500, sid, .2, DIM, 60, st="big")]}


for _k in range(6, 66):
    if "s%d" % _k not in globals():
        globals()["s%d" % _k] = (lambda k: (lambda: _todo("s%d" % k)))(_k)


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "In those same decades", "s2"), (2, "Its king wrote", "s3"), (3, "So who brought", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "On land", "s7"), (1, "At sea", "s8"), (2, "His temple", "s9"), (2, "'No land", "s10")], {"chapter": "Raiders from the sea"}),
    (1, 1, "collision", "s11", [(0, "Some had come", "s12"), (1, "So where were", "s13"), (2, "And could raiders", "s14")], {}),
    (1, 2, "reversal", "s15", [(0, "In {2019", "s16"), (1, "Think of your DNA", "s17"), (1, "Four infants", "s18"), (1, "Within two centuries", "s19"),
                               (2, "Raiders, yes", "s20")], {}),
    (2, 0, "world", "s21", [(1, "At the crossroads", "s22")], {"chapter": "A world on fire"}),
    (2, 1, "collision", "s23", [(0, "'All my troops", "s24"), (1, "'The seven ships", "s25")], {}),
    (2, 2, "cost", "s26", [(0, "At Gibala", "s27")], {}),
    (2, 3, "reversal", "s28", [(0, "Whoever lit", "s29"), (1, "In Greece", "s30"), (1, "At Pylos", "s31"), (1, "Then writing", "s32")], {}),
    (2, 4, "tag", "s33", [(0, "Not one crash", "s34")], {}),
    (3, 0, "world", "s35", [(1, "Cores from a salt", "s36")], {"chapter": "Drought, hunger and quakes"}),
    (3, 1, "collision", "s37", [(1, "Juniper timbers", "s38"), (2, "Farmers kept", "s39")], {}),
    (3, 2, "cost", "s40", [(1, "And Pharaoh Merneptah", "s41")], {}),
    (3, 3, "reversal", "s42", [(0, "At Mycenae, Tiryns", "s43"), (0, "In {2000", "s44"), (1, "In {2018", "s45")], {}),
    (4, 0, "world", "s46", [(0, "Copper came from", "s47"), (1, "Around {1300", "s48"), (2, "Raiders on those", "s49")], {"chapter": "A web of failures"}),
    (4, 1, "collision", "s50", [(1, "Even in Egypt", "s51"), (1, "A few years later", "s52")], {}),
    (4, 2, "reversal", "s53", [(1, "The catch?", "s54")], {}),
    (5, 0, "weigh", "s55", [(1, "Earthquakes: an", "s56"), (1, "And the perfect", "s57"), (2, "One culprit", "s58"), (2, "So, did the Sea", "s59")], {"chapter": "The weighing"}),
    (5, 1, "test", "s60", [(0, "Tree rings from", "s61"), (0, "More ancient DNA", "s62"), (0, "And about a hundred", "s63")], {}),
    (5, 2, "close", "s64", [(0, "Yet in the ruins", "s65")], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s19": ("s16", [1, 889, 500], "s19_add"), "s29": ("s28", [1, 889, 500], "s29_add"), "s41": ("s40", [1, 889, 500], "s41_add"),
    "s49": ("s47", [1, 889, 500], "s49_add"), "s57": ("s53", [1, 889, 500], "s57_add"), "s58": ("s54", [1, 889, 500], "s58_add"),
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
            say[frm] = say[frm] + " " + head if frm in say else head
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
        tags[z] = g[fn]() if fn and fn in g else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-sea-peoples", "code": "LF.12", "series": script["series"], "title": script["title"], "case": "sea-peoples",
          "verdict": "mixed", "claim": "Did the invading Sea Peoples bring down the Bronze Age world?",
          "mood": "mystery", "hook_text": "Who brought down the Bronze Age *world*?", "beats": beats, "shots": shots,
          "sources": "Cline 2014 and 2021, 1177 B.C. · Knapp & Manning 2016 (doi:10.3764/aja.120.1.0099) · Kaniewski et al. 2011 (doi:10.1371/journal.pone.0020232) · "
                     "Kaniewski et al. 2013 (doi:10.1371/journal.pone.0071004) · Manning et al. 2023 (doi:10.1038/s41586-022-05693-y) · "
                     "Feldman et al. 2019 (doi:10.1126/sciadv.aax0061) · Drews 1993 · Epigraphic Survey 1930, Medinet Habu I",
          "post": "Around 1177 BCE, Ramesses III carved a sea battle on his temple. In the same decades, palaces from Greece to Syria burned or "
                  "emptied. Did the Sea Peoples bring down the Bronze Age world? Six suspects weighed: raiders, drought, hunger, earthquakes, "
                  "broken trade and revolt, with the letters of Ugarit, the tree rings of Gordion and the DNA of Ashkelon.",
          "hashtags": ["#SeaPeoples", "#BronzeAge", "#AncientEgypt", "#Archaeology", "#WeighItYourself"],
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
