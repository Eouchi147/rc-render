"""LF.30 · Before Us · The Denisovans (16:9 long film, one wall).

The script is films/long/lf-denisovans/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s55; s5t, the title, is the intro card over
the panel of s5), drawn while it is said: a chip of finger bone the size of a ladybird on a fingertip, the people inside it, the
map of their genes today; Denisova Cave in the Altai, its layered floor, the lab, the lucky bone (70 in 100), two books letter by
letter, the family tree that changed in 2010, the colouring of 2012, the huge molar and a museum case with a faceless outline;
Denny's splinter, the collagen barcodes, her mother's mitochondria, two copies of her DNA, her parents at a hearth, her time,
the map from western Europe, two peoples meeting; a grid of a hundred parts and a trace in a thousand, the old edition, the
Ayta Magbukon and the two Denisovan groups, the thin air and thick blood of Tibet, the herder and his shadow; the Tibetan
jaw and its proteins, the cave floor with DNA in the dirt, the rib and the animals, a breath at 3,280 m; the Harbin bridge and
the well, eighty-five years, the skull and its date, the proteins of the inner ear and the tartar, the face at last; the giant
claim, the map of the finds, the Taiwan Strait and its net, the leg bones, the trousers, the lineup; the ledger, the open
questions, the tests and the outline of a body still mostly missing. Drawings are schematic and true to the numbers said:
solid = measured, dashed = inferred, dotted = claimed. Human remains are drawn plainly and with care.

Facts: the Shorts 'other-humans' and 'denisovan-giants' (f01.py, rewrite/other-humans.json, rewrite/denisovan-giants.json) and
the script's facts_added (Krause et al. 2010, Reich et al. 2010, Meyer et al. 2012, Bennett et al. 2019, Douka et al. 2019,
Jacobs Z. et al. 2019, Shreeve 2013, Brown et al. 2016, Slon et al. 2018, Prufer et al. 2014, Larena et al. 2021, Jacobs G. S.
et al. 2019, Browning et al. 2018, Huerta-Sanchez et al. 2014, Chen et al. 2019, Zhang D. et al. 2020, Xia et al. 2024, Zhang
X. L. et al. 2018, Ji et al. 2021, Shao et al. 2021, Fu et al. 2025 (Science and Cell), Demeter et al. 2022, Chang et al. 2015,
Tsutaya et al. 2025, Kaifu et al. 2026 (preprint), Peyregne et al. 2025 (preprint)).

Engine workaround (as in lf_first_americans.py and lf_roswell.py): the wall only adds elements to a panel on its first visit, at
a beat start or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose
zoom carries a tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets
the shot's additions as a panel item (kit.js builds them on that step's clock). Build-in times inside a sentence come from a
syllable clock (Clock). Elements cannot fade out: a dark veil drawn over a part of a panel stands in for a fade.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-denisovans/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-denisovans/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-denisovans RC_FILMS_EPS=/tmp/claude-0/sbx_lf-denisovans/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-denisovans/boards python3 films.py long.lf_denisovans
"""
import json, math, os, random, re
import films
from mural import remix, SENT
import illus as I
from illus import person, arrow, line, glow, label, dot, box, ring, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-denisovans", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, MUTED, DIM = "#f2c98e", "#e8c35a", "#cbbca8", "#9a8f80"
LAND, LAND_E, SEA_C = "#4a3d2f", "#c9ad85", "#173342"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c86a", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}
# the people of this film: Denisovans in blue, Neanderthals in amber, our species in gold; claims and unknowns in lilac
DEN, DEN_D, NEA, US = "#9fd0ff", "#5f8fb8", "#e8b87a", "#f2c98e"
BONEC, BONE_E, BONE_D = "#efe6d2", "#fff6e6", "#c9b99a"     # fossil bone: face, lit edge, shade
SKIN, SKIN_D, NAIL = "#d9a98a", "#a8765c", "#f1d2c0"         # the modern fingertip of the opening
ROCK, ROCK_D, ROCK_L = "#6e5f52", "#3d342d", "#a8988a"       # cave limestone and cliffs
SED = ["#7a6248", "#5f4c39", "#8a7258", "#6b553f", "#4f3f30", "#76604a"]   # sediment layers
FLAT = "#15110d"                                           # the dark ground (for veils)
BLOOD, BLOOD_D = "#c8504a", "#7d2a28"


# ================================================================== narration: the script's own lines, [go:] markers, a clock
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


TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # DNA: three letters
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
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Clock:
    """Estimated word times per beat (seconds from the beat's first word). A shot's step starts at its [go:] marker (or at the beat's
    first word; at a chapter beat's second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said,
    counted from the start of shot i's step."""
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
            self.start.setdefault(frm, (bi, sents[1] if b.get("chapter") and len(sents) > 1 else 0.0))
            self.words[bi] = ws

    def at(self, i, phrase, lo=.4, k=1):
        """phrase: words as spoken (numbers in words, hyphens as in the script)."""
        bi, t0 = self.start[i]
        want = [_norm(x) for x in phrase.split() if _norm(x)]
        ws = self.words[bi]
        hits = 0
        for q in range(len(ws)):
            if ws[q][1] >= t0 - 1e-6 and [w for w, _ in ws[q:q + len(want)]] == want:
                hits += 1
                if hits == k:
                    return round(max(lo, ws[q][1] - t0), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))


C = None                    # the clock, set in film()
IDX = {}                    # shot id -> ep shot index, set in film()


def T(sid, phrase, lead=0.0, k=1, lo=.4):
    """Seconds after shot sid's step starts at which `phrase` is said (its k-th occurrence), plus `lead`."""
    return round(C.at(IDX[sid], phrase, lo=lo, k=k) + lead, 2)


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


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


def group(els, at=0, fx=None, tr=None, op=None, **kw):
    """Elements built together as one (one build-in for all of them); tr = an SVG transform for the children."""
    inner = {"k": "group", "els": els, "in": -1}
    if tr:
        inner["tr"] = tr
    e = {"k": "group", "els": [inner], "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


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
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
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
    e = {"k": "axis", "x0": round(x0, 1), "x1": round(x1, 1), "y": round(y, 1), "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def band(x0, x1, y, h, c, at, t=None, tc=None, dur=1.0, op=None):
    e = {"k": "band", "x0": round(x0, 1), "x1": round(x1, 1), "y": round(y, 1), "h": h, "c": c, "in": round(at, 2), "dur": dur}
    if t:
        e.update(t=t, tc=tc or c)
    if op is not None:
        e["op"] = op
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


def later(els, dt):
    """The same elements, built dt seconds later."""
    out = []
    for e in els:
        e = dict(e)
        if isinstance(e.get("in"), (int, float)) and e["in"] >= 0:
            e["in"] = round(e["in"] + dt, 2)
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


def seated(x, y, h, at, c="#e8d6b8", face=1, op=None):
    """A figure seated on the ground facing right (face=1) or left, h = standing height (a plain silhouette)."""
    X = lambda a: x + face * a
    out = [poly([[X(-.08 * h), y - .58 * h], [X(.1 * h), y - .58 * h], [X(.12 * h), y - .12 * h], [X(-.12 * h), y - .1 * h]], c, at=at, fx="rise", op=op),
           poly([[X(-.06 * h), y - .14 * h], [X(.34 * h), y - .14 * h], [X(.36 * h), y], [X(-.14 * h), y]], c, at=at, fx="rise", op=op),
           circ(X(.01 * h), y - .67 * h, .075 * h, c, at=at, fx="rise", op=op)]
    return out



def figure(x, y, h, at, c="#e8d6b8", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e



def conifer(x, y, h, at, c="#1d2620", fx="pop", edge="rgba(255,226,190,.18)", **kw):
    w = h * .42
    pts = [[x, y - h], [x + w * .32, y - h * .62], [x + w * .2, y - h * .62], [x + w * .45, y - h * .32], [x + w * .3, y - h * .32], [x + w * .5, y - h * .08],
           [x + w * .08, y - h * .08], [x + w * .08, y], [x - w * .08, y], [x - w * .08, y - h * .08], [x - w * .5, y - h * .08], [x - w * .3, y - h * .32],
           [x - w * .45, y - h * .32], [x - w * .2, y - h * .62], [x - w * .32, y - h * .62]]
    e = poly(pts, c, edge, 1, at, fx=fx)
    e.update(kw)
    return e


def helix(x0, y0, x1, y1, at, n=16, amp=18, c1=GOLD, c2=BLUE, w=3, dur=1.0):
    """A DNA double helix drawn as two crossing waves with rungs (after f16.helix)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    P = lambda t, ph: [round(x0 + ux * L * t + nx * amp * math.sin(t * n + ph), 1), round(y0 + uy * L * t + ny * amp * math.sin(t * n + ph), 1)]
    ts = [k / 40 for k in range(41)]
    out = [{"k": "line", "p": [P(t, 0) for t in ts], "c": c1, "w": w, "curve": True, "in": round(at, 2), "fx": "draw", "dur": dur},
           {"k": "line", "p": [P(t, math.pi) for t in ts], "c": c2, "w": w, "curve": True, "in": round(at + .1, 2), "fx": "draw", "dur": dur}]
    out += [{"k": "line", "p": [P(t, 0), P(t, math.pi)], "c": "#e9dccb", "w": 1.5, "op": .5, "keepop": True, "in": round(at + dur * .8, 2)} for t in [k / 10 + .05 for k in range(10)]]
    return out


def flask(x, y, s, at, c=BLUE):
    """A lab flask (chemistry), base at y."""
    P = lambda a, b: (x + a * s, y + b * s)
    return [poly([P(-10, -70), P(10, -70), P(10, -40), P(36, 0), P(-36, 0), P(-10, -40)], "rgba(159,208,255,.12)", c, 2.5, at, fx="pop"),
            poly([P(-26, -12), P(26, -12), P(32, -2), P(-32, -2)], "rgba(143,217,176,.6)", at=at + .1)]


# ================================================================== maps
def _unwrap(ring):
    out, prev = [], None
    for lo, la in ring:
        if prev is not None:
            while lo - prev > 180:
                lo -= 360
            while lo - prev < -180:
                lo += 360
        out.append((lo, la)); prev = lo
    return out


def _clip(ring, x0, x1, y0, y1):
    """Sutherland-Hodgman: a closed ring clipped to a lon/lat box."""
    def cut(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia:
                    out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return out
    def ix(xc):
        return lambda a, b: (xc, a[1] + (b[1] - a[1]) * (xc - a[0]) / ((b[0] - a[0]) or 1e-9))
    def iy(yc):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yc - a[1]) / ((b[1] - a[1]) or 1e-9), yc)
    pts = list(ring)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not pts:
            break
        pts = cut(pts, inside, inter)
    return pts


class Map:
    """An equirectangular map of a lon/lat box fitted in a frame rectangle (like films.View), whose longitudes may run past 180
    (lon0 160, lon1 250: the North Pacific in one piece); land rings are unwrapped, shifted into the box and clipped to it."""
    def __init__(self, lon0, lon1, lat0, lat1, rect=(90, 120, 1600, 680)):
        self.b = (lon0, lon1, lat0, lat1)
        k = math.cos(math.radians((lat0 + lat1) / 2))
        w, h = (lon1 - lon0) * k, (lat1 - lat0)
        s = min(rect[2] / w, rect[3] / h)
        self.s, self.k = s, k
        self.ox = rect[0] + (rect[2] - w * s) / 2
        self.oy = rect[1] + (rect[3] - h * s) / 2

    def p(self, lon, lat):
        lon0, lon1, lat0, lat1 = self.b
        while lon < lon0 - 180:
            lon += 360
        while lon > lon1 + 180:
            lon -= 360
        return (round(self.ox + (lon - lon0) * self.k * self.s, 1), round(self.oy + (lat1 - lat) * self.s, 1))

    def km(self, km):
        return km / 111.32 * self.s

    def land(self, pad=70.0, tol=1.4, minpts=4):
        lon0, lon1, lat0, lat1 = self.b
        out = []
        for poly_ in films._topo():
            ring = _unwrap(poly_[0])
            xs = [q[0] for q in ring]
            for sh in (-360, 0, 360):
                if max(xs) + sh < lon0 - pad or min(xs) + sh > lon1 + pad:
                    continue
                if max(q[1] for q in ring) < lat0 - pad or min(q[1] for q in ring) > lat1 + pad:
                    continue
                cl = _clip([(q[0] + sh, q[1]) for q in ring], lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad)
                if len(cl) < minpts:
                    continue
                pts, last = [], None
                for lo, la in cl:
                    q = self.p(lo, la)
                    if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                        continue
                    pts.append(q); last = q
                if len(pts) >= minpts:
                    out.append("M" + "L".join(f"{x} {y}" for x, y in pts) + "Z")
        return out

    def path(self, lonlats):
        return [self.p(lo, la) for lo, la in lonlats]


class Globe:
    """An orthographic globe centred on (lon0, lat0), radius R at (cx, cy); land on the far side is pressed onto the limb."""
    def __init__(self, lon0, lat0, R, cx, cy):
        self.l0, self.p0, self.R, self.cx, self.cy = math.radians(lon0), math.radians(lat0), R, cx, cy

    def xyz(self, lon, lat):
        l, p = math.radians(lon), math.radians(lat)
        cosc = math.sin(self.p0) * math.sin(p) + math.cos(self.p0) * math.cos(p) * math.cos(l - self.l0)
        x = math.cos(p) * math.sin(l - self.l0)
        y = math.cos(self.p0) * math.sin(p) - math.sin(self.p0) * math.cos(p) * math.cos(l - self.l0)
        return x, y, cosc

    def p(self, lon, lat):
        x, y, c = self.xyz(lon, lat)
        if c < 0:
            d = math.hypot(x, y) or 1
            x, y = x / d, y / d
        return (round(self.cx + self.R * x, 1), round(self.cy - self.R * y, 1))

    def land(self, tol=1.6, minpts=4):
        out = []
        for poly_ in films._topo():
            ring = poly_[0]
            vis = [self.xyz(lo, la)[2] > 0 for lo, la in ring]
            if not any(vis):
                continue
            pts, last = [], None
            for lo, la in ring:
                q = self.p(lo, la)
                if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                    continue
                pts.append(q); last = q
            if len(pts) >= minpts:
                out.append("M" + "L".join(f"{x} {y}" for x, y in pts) + "Z")
        return out


def land_el(paths, at=-1, landc=LAND):
    return {"k": "map", "land": paths, "landc": landc, "in": at}


def pin(x, y, t, at, c=AMBER, a="start", lx=None, ly=None, r=9, tc=None, size=None):
    e = {"k": "pin", "x": round(x, 1), "y": round(y, 1), "t": t, "c": c, "a": a, "r": r, "in": round(at, 2)}
    if lx is not None:
        e["lx"] = lx
    if ly is not None:
        e["ly"] = ly
    if tc:
        e["tc"] = tc
    return e




# ================================================================== drawings of this film
def veil(x, y, w, h, at, op=.82, fill=FLAT, r=10, dur=.6):
    """A dark veil over part of a panel: stands in for a fade-out (elements cannot fade out)."""
    e = rect(x, y, w, h, fill, at=at, r=r, op=op)
    e["dur"] = dur
    return e


def light_shaft(x0a, x0b, y0, x1a, x1b, y1, at=-1, op=.05):
    """A soft shaft of light: two nested quads, brighter inside."""
    mid = lambda a, b, t: a + (b - a) * t
    return [poly([(x0a, y0), (x0b, y0), (x1b, y1), (x1a, y1)], "rgba(255,228,180,1)", at=at, op=op),
            poly([(mid(x0a, x0b, .25), y0), (mid(x0a, x0b, .75), y0), (mid(x1a, x1b, .7), y1), (mid(x1a, x1b, .3), y1)], "rgba(255,236,200,1)", at=at, op=op * .9)]


def fingertip(tx, ty, s, at=-1, prints=True):
    """A modern human finger seen from the side, palm up, pointing left: the tip of the pad at (tx, ty) (where it meets the top edge),
    s = scale (1: the finger is about 220 units thick, as at the opening). It runs off to the right."""
    P = lambda a, b: (tx + a * s, ty + b * s)
    top = [P(1500, 26), P(1100, 24), P(800, 20), P(600, 16), P(430, 10), P(290, 4), P(180, 0), P(90, -2), P(40, 4), P(8, 18)]
    tip = [P(-14, 40), P(-24, 70), P(-26, 104), P(-18, 138), P(0, 168), P(28, 192), P(66, 208)]
    bot = [P(140, 218), P(300, 224), P(500, 226), P(720, 226), P(1100, 228), P(1500, 230)]
    body = top + tip + bot
    out = [poly(body, "#b98468", at=at, curve=True),
           poly(top + [P(30, 30), P(160, 44), P(400, 52), P(700, 56), P(1100, 60), P(1500, 62)], "#e2b394", at=at, curve=True, op=.75),
           poly([P(40, 190), P(160, 206), P(400, 214), P(700, 216), P(1100, 218), P(1500, 220)] + list(reversed(bot)), "#6e4634", at=at, curve=True, op=.55),
           ln(top + tip[:3], at, "#ffe0c4", 2.5, draw=False, curve=True, op=.7),
           ln(tip[2:] + bot[:2], at, "#8a5a44", 2, draw=False, curve=True, op=.6)]
    for cx in (260, 560):                                         # joint creases on the palm side
        out.append(ln([P(cx - 6, 12), P(cx + 4, 36), P(cx + 8, 64)], at, "#7a4c38", 2.2, draw=False, curve=True, op=.45))
        out.append(ln([P(cx + 14, 10), P(cx + 22, 34), P(cx + 24, 58)], at, "#7a4c38", 1.6, draw=False, curve=True, op=.3))
    if prints:                                                    # the ridges of the fingerprint, on the pad
        for k in range(7):
            r = 26 + 17 * k
            pts = [P(70 + r * math.cos(math.radians(a)) * 1.35, 66 - r * math.sin(math.radians(a)) * .42) for a in range(20, 170, 10)]
            out.append(ln(pts, at, "#9a6a50", 1.4, draw=False, curve=True, op=.32))
    return out


def bone_chip(cx, cy, s, at, fx="pop", glow_=True, c=BONEC):
    """The chip of finger bone (Denisova 3): an irregular pale fragment with a broken, porous face; base centre (cx, cy), about
    100 x 46 units at s = 1."""
    P = lambda a, b: (cx + a * s, cy + b * s)
    out = []
    if glow_:
        out.append(glow(round(cx, 1), round(cy - 22 * s, 1), round(130 * s), round(at, 2), .7, "lamp"))
    shape = [P(-50, 0), P(-47, -9), P(-41, -15), P(-37, -26), P(-26, -31), P(-19, -40), P(-5, -45), P(6, -41), P(15, -47), P(28, -43), P(37, -32),
             P(45, -25), P(51, -11), P(48, 0), P(30, 4), P(0, 6), P(-30, 4)]
    broken = [P(22, -44), P(30, -42), P(38, -31), P(46, -24), P(51, -11), P(48, 0), P(36, 2), P(30, -12), P(26, -26)]
    pores = [circ(*P(a, b), r * s, "#8a7458", at=-1, op=.85) for a, b, r in ((36, -24, 2.6), (42, -14, 2.2), (32, -8, 1.8), (40, -4, 2), (30, -30, 1.6), (45, -20, 1.4))]
    cracks = [ln([P(-28, -26), P(-16, -18), P(-6, -22)], -1, "#b9a888", 1.4 * s, draw=False, op=.8),
              ln([P(2, -36), P(8, -24), P(4, -12)], -1, "#b9a888", 1.2 * s, draw=False, op=.7)]
    lit = ln([P(-46, -10), P(-38, -24), P(-20, -38), P(-4, -44), P(14, -46)], -1, "#ffffff", 1.6 * s, draw=False, op=.55)
    out.append(group([poly(shape, c, BONE_E, 1.6), poly(broken, "#c4ae8c", at=-1, op=.95), lit] + cracks + pores +
                     [circ(*P(-14, -22), 2.2 * s, "#b9a888", at=-1), circ(*P(-30, -10), 1.8 * s, "#b9a888", at=-1)], at, fx))
    return out


def ladybird(cx, cy, s, at, fx="pop", face=-1):
    """A ladybird standing on a surface at (cx, cy) (its feet), about 95 units long at s = 1, head towards face (-1 = left)."""
    f = face
    P = lambda a, b: (cx + f * a * s, cy + b * s)
    legs = [ln([P(x0, -8), P(x0 + 10 * d, 2)], -1, "#1a1410", 3 * s, draw=False) for x0, d in ((-20, -1), (0, 1), (20, 1))]
    shell = [P(-44, -6)] + [P(48 * math.cos(math.radians(a)) - 2, -6 - 50 * math.sin(math.radians(a))) for a in range(170, -1, -10)] + [P(46, -6)]
    head = [P(-60 + 14 * math.cos(math.radians(a)), -12 - 14 * math.sin(math.radians(a))) for a in range(0, 360, 30)]
    prono = [P(-50, -6), P(-50, -26), P(-40, -40), P(-30, -44), P(-30, -6)]
    spots = [(-8, -34, 7), (16, -36, 7.5), (-14, -16, 6), (12, -15, 6.5), (34, -20, 6), (-26, -24, 5)]
    els = legs + [poly(head, "#14100d", at=-1, curve=True), poly(shell, "#d0342a", "#ff8a70", 1.2, at=-1, curve=True),
                  poly(prono, "#14100d", at=-1, curve=True), circ(*P(-42, -30), 4 * s, "#f5ecdc", at=-1), circ(*P(-36, -14), 3.5 * s, "#f5ecdc", at=-1),
                  ln([P(-30, -44), P(-30, -6)], -1, "#7a1a14", 1.6 * s, draw=False)]
    els += [circ(*P(a, b), r * s, "#14100d", at=-1) for a, b, r in spots]
    els += [poly(E(*P(4, -40), 16 * s, 6 * s, 16), "#ffffff", at=-1, op=.35)]
    return [group(els, at, fx)]


def hand_bones(x, y, s, at, lit=True, c="#cdbf9f", op=.75):
    """A schematic right hand skeleton seen from the back, fingers up, wrist at (x, y): the tip bone of the little finger lit gold."""
    P = lambda a, b: (x + a * s, y + b * s)
    rays = {"thumb": [(-70, -60), (-140, -150), (-178, -210), (-200, -250)],
            "index": [(-30, -70), (-50, -210), (-60, -300), (-64, -355), (-66, -395)],
            "middle": [(0, -76), (5, -228), (8, -328), (10, -388), (11, -430)],
            "ring": [(30, -70), (60, -210), (75, -305), (82, -360), (86, -400)],
            "little": [(55, -60), (115, -185), (140, -260), (152, -305), (160, -340)]}
    out = []
    for k in range(5):                                               # the wrist bones
        out.append(circ(*P(-44 + 22 * k, -34 + 12 * (k % 2)), 13 * s, "rgba(205,191,159,.35)", c, 1.5, at, op=op))
    for k in range(3):
        out.append(circ(*P(-30 + 30 * k, -8), 12 * s, "rgba(205,191,159,.35)", c, 1.5, at, op=op))
    for name, pts in rays.items():
        for j in range(len(pts) - 1):
            (a0, b0), (a1, b1) = pts[j], pts[j + 1]
            d = math.hypot(a1 - a0, b1 - b0); ux, uy = (a1 - a0) / d, (b1 - b0) / d
            q0, q1 = P(a0 + ux * 7, b0 + uy * 7), P(a1 - ux * 7, b1 - uy * 7)
            w = (17 if j == 0 else 14 if j == 1 else 11 if j == 2 else 9) * s
            tipb = name == "little" and j == len(pts) - 2
            if tipb and lit:
                continue
            out.append(ln([q0, q1], at, c, w, draw=False, op=op))
    lx0, ly0 = rays["little"][-2]; lx1, ly1 = rays["little"][-1]
    tip_a, tip_b = P(lx0 + 3, ly0 - 6), P(lx1 - 2, ly1 + 4)
    if lit:
        out += [glow(*P(lx1 - 4, ly1 + 8), round(70 * s), at + .6, .9, "lamp"), ln([tip_a, tip_b], at + .6, GOLD, 9 * s, draw=False)]
    return out, P(lx1, ly1)


def mix(c, bg="#241c16", t=.5):
    """The colour c faded towards the background bg (t = how much of c is kept): person and group elements ignore opacity."""
    a, b = c.lstrip("#"), bg.lstrip("#")
    ca, cb = [int(a[i:i + 2], 16) for i in (0, 2, 4)], [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(cb[i] + (ca[i] - cb[i]) * t) for i in range(3))


def ghosts(x0, x1, gy, n, at, dt=.12, c=LILAC, op=.5, seed=4, hmin=95, hmax=150, kids=True):
    """A row of faceless figures (people known only from their DNA), standing on a line at gy (op: how much of their colour shows)."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * k / max(1, n - 1) + r.uniform(-14, 14)
        h = r.uniform(hmin, hmax) if (not kids or k % 4) else r.uniform(.55, .7) * hmax
        out.append(figure(x, gy, h, round(at + dt * k, 2), mix(c, t=op), "rise"))
    return out


HEAD = [(-120, 70), (-112, -10), (-80, -70), (-20, -96), (50, -88), (100, -50), (118, 10), (126, 40), (156, 92), (132, 104), (136, 128), (128, 146),
        (132, 166), (120, 196), (90, 226), (60, 236), (54, 290), (120, 330), (170, 380), (190, 450), (-200, 450), (-176, 380), (-120, 330), (-56, 290),
        (-60, 236), (-100, 196), (-122, 130)]


def head_outline(cx, cy, s, at, c=LILAC, style="claimed", w=3.5, fill="rgba(201,193,238,.05)", face=1, fx=None):
    """A head and shoulders in profile, facing right (face=1) or left, drawn only as an outline (nose at about (cx + 156 s, cy + 92 s))."""
    pts = [(cx + face * a * s, cy + b * s) for a, b in HEAD]
    return poly(pts, fill, c, w, at, curve=True, style=style, fx=fx)


def name_plate(x, y, w, h, at, fx="pop"):
    """A museum name plate on a little stand, its line blank."""
    els = [rect(x, y, w, h, "#2f261d", "#c9a96e", 3, 8), rect(x + 14, y + 14, w - 28, h - 28, "none", "rgba(201,169,110,.45)", 1.5, 5),
           ln([(x + w * .18, y + h * .66), (x + w * .82, y + h * .66)], -1, "#8a7a62", 3, draw=False, style="claimed"),
           ln([(x + w * .5, y + h), (x + w * .5, y + h + 46)], -1, "#8a6a48", 8, draw=False), rect(x + w * .3, y + h + 44, w * .4, 12, "#5a4632", r=4)]
    return group(els, at, fx)


# ------------------------------------------------------------------ teeth, jaws, skulls, bones (schematic, true to their shapes)
def molar_top(cx, cy, r, at, fill=BONEC, fx="pop", style="known", c=BONE_E, grooves=True, op=None):
    """A lower molar's chewing surface from above: a rounded rectangle with five cusps and a Y-shaped groove; r = half width."""
    P = lambda a, b: (cx + a * r, cy + b * r)
    out_ = [P(-1, -.55), P(-.85, -.92), P(-.3, -1.02), P(.35, -1.0), P(.9, -.85), P(1.04, -.2), P(.98, .55), P(.7, .95), P(.1, 1.02), P(-.55, .98),
            P(-.95, .7), P(-1.05, .1)]
    els = [poly(out_, fill, c, 2, curve=True, style=style)]
    if grooves and style == "known":
        els += [ln([P(-.62, -.18), P(-.05, .02), P(.6, -.12)], -1, BONE_D, 3, draw=False, curve=True),
                ln([P(-.05, .02), P(.02, .62)], -1, BONE_D, 3, draw=False), ln([P(-.05, .02), P(-.1, -.7)], -1, BONE_D, 2.4, draw=False),
                ln([P(.3, .05), P(.55, .6)], -1, BONE_D, 2, draw=False)]
        els += [circ(*P(a, b), r * .1, "rgba(255,255,255,.35)", at=-1) for a, b in ((-.55, -.55), (.3, -.6), (.65, .2), (.4, .65), (-.5, .45))]
    return group(els, at, fx, op=op)


def molar_side(cx, cy, s, at, fill=BONEC, fx="pop", roots=True, c=BONE_E):
    """A molar from the side: a crown with cusps (its chewing edge at cy - 60 s) and two roots; (cx, cy) the neck of the tooth."""
    P = lambda a, b: (cx + a * s, cy + b * s)
    crown = [P(-46, 0), P(-50, -30), P(-42, -54), P(-30, -62), P(-18, -54), P(-6, -63), P(8, -56), P(20, -64), P(34, -56), P(46, -48), P(50, -24), P(46, 0)]
    els = [poly(crown, fill, c, 2, curve=True)]
    if roots:
        els += [poly([P(-40, -2), P(-6, -2), P(-12, 40), P(-20, 74), P(-30, 76), P(-38, 40)], "#d8ccb2", c, 1.6, curve=True),
                poly([P(4, -2), P(40, -2), P(36, 40), P(28, 72), P(18, 74), P(10, 40)], "#d8ccb2", c, 1.6, curve=True)]
    els.append(ln([P(-40, -40), P(-10, -46), P(30, -44)], -1, "#ffffff", 2, draw=False, curve=True, op=.4))
    return group(els, at, fx)


def half_jaw(cx, cy, s, at, fx="pop", teeth=2, c=BONEC, edge=BONE_E, broken=True):
    """The right half of a lower jaw seen from the side, front to the left (the Tibetan jaw keeps its body, two molars and the root of
    the rising branch): (cx, cy) the middle of its lower edge; teeth: molars in place."""
    P = lambda a, b: (cx + a * s, cy + b * s)
    body = [P(-196, -30), P(-170, -6), P(-80, 4), P(40, 2), P(120, -8), P(150, -26), P(176, -70), P(190, -130), P(184, -176), P(172, -170), P(166, -186),
            P(152, -176), P(146, -150), P(132, -118), P(112, -102), P(-60, -100), P(-130, -102)]
    if broken:
        body += [P(-150, -104), P(-168, -92), P(-160, -80), P(-184, -70), P(-178, -56), P(-200, -46)]
    else:
        body += [P(-176, -104), P(-204, -80), P(-208, -48)]
    els = [poly(body, c, edge, 2, curve=True),
           poly([P(-170, -20), P(-60, -8), P(60, -10), P(140, -26), P(150, -40), P(60, -32), P(-60, -28)], BONE_D, curve=True, op=.55),
           poly([P(140, -100), P(170, -150), P(176, -110), P(160, -60)], BONE_D, curve=True, op=.45),
           circ(*P(-128, -56), 6 * s, "#5a4a3a", at=-1, op=.8)]
    if teeth:
        for tx in (-118, -80):                                                      # empty sockets of the premolars
            els.append(rect(P(tx, -104)[0] - 9 * s, P(tx, -104)[1] - 2 * s, 18 * s, 12 * s, "#6a5a48", r=3 * s, at=-1))
        for k, tx in enumerate((-22, 56)[:teeth]):
            els.append(molar_side(cx + tx * s, cy - 100 * s, .78 * s, -1, roots=False, fx=None))
    return group(els, at, fx)


SKULL_H = [(-6, 78), (-12, 56), (-15, 40), (-10, 22), (-4, 10), (0, 0), (-10, -12), (-12, -22), (-2, -30), (22, -46), (58, -66), (100, -78),
           (140, -80), (176, -70), (204, -50), (220, -24), (226, 2), (220, 22), (204, 34), (176, 44), (160, 54), (146, 44), (118, 42), (94, 40),
           (70, 48), (58, 72), (44, 82), (16, 84)]
SKULL_M = [(-2, 64), (-8, 46), (-10, 32), (-6, 18), (-2, 8), (0, 0), (-5, -9), (-3, -20), (6, -46), (26, -74), (60, -96), (102, -104),
           (140, -96), (168, -74), (184, -44), (188, -12), (182, 12), (166, 28), (144, 40), (126, 34), (100, 34), (78, 36), (60, 44), (50, 62),
           (36, 70), (12, 70)]


def harbin_skull(x, y, s, at, face=-1, fx="pop", lit=True, op=None):
    """The Harbin cranium in profile (no lower jaw): long and low, a heavy brow, a big, almost square eye socket, one molar left.
    (x, y) is the root of the nose (nasion); s: units per millimetre (about 230 mm long); face -1 = facing left."""
    f = -face
    P = lambda a, b: (x + f * a * s, y + b * s)
    els = [poly([P(a, b) for a, b in SKULL_H], "#e6dac2", BONE_E, 2.2, curve=True)]
    els.append(poly([P(150, -78), P(190, -64), P(214, -38), P(222, -6), P(214, 18), P(190, 34), P(160, 50), P(146, 40), P(170, 20), P(180, -10), P(170, -48)],
                    "#b9a888", at=-1, curve=True, op=.55))                                   # shade on the back of the vault
    els.append(poly([P(-12, -16), P(-10, -28), P(10, -36), P(40, -36), P(52, -26), P(40, -18), P(10, -18)], "#f6eedd", at=-1, curve=True))   # the brow ridge
    els.append(ln([P(-10, -30), P(14, -38), P(46, -36)], -1, "#ffffff", 2, draw=False, curve=True, op=.6))
    els.append(poly([P(2, -12), P(36, -14), P(42, 6), P(40, 26), P(6, 28), P(0, 8)], "#231c17", at=-1, curve=True))   # the eye socket
    els.append(poly([P(-14, 26), P(-6, 22), P(-6, 46), P(-14, 48)], "#231c17", at=-1, curve=True))                    # the nose opening
    els.append(poly([P(36, 30), P(70, 30), P(108, 34), P(108, 42), P(70, 40), P(40, 44)], "#d0c2a6", at=-1, curve=True))   # cheek and arch
    els.append(circ(*P(122, 28), 5.5 * s, "#231c17", at=-1))                                                         # the ear opening
    els.append(poly([P(146, 44), P(160, 54), P(152, 66), P(140, 54)], "#d8ccb2", "#b9a888", 1, at=-1, curve=True))     # mastoid
    els += [ln([P(64, -68), P(70, -30), P(84, 4)], -1, "#b9a888", 1.4, draw=False, curve=True, op=.6),                 # coronal suture
            ln([P(30, -40), P(80, -50), P(130, -42), P(160, -20)], -1, "#b9a888", 1.2, draw=False, curve=True, op=.45)]  # temporal line
    for k in range(5):                                                                                               # empty sockets
        els.append(rect(min(P(-2 + 9 * k, 78)[0], P(4 + 9 * k, 78)[0]), P(0, 78)[1] - 2 * s, 6 * s, 5 * s, "#5a4a3a", r=1.5 * s, at=-1))
    els.append(group([poly([P(44, 78), P(58, 78), P(60, 88), P(52, 94), P(44, 90)], "#efe6d2", BONE_E, 1.4, curve=True)], -1))   # the one molar
    if lit:
        els.append(ln([P(-10, -24), P(40, -40), P(100, -78), P(150, -80)], -1, "#fff6e6", 2.4, draw=False, curve=True, op=.55))
    return group(els, at, fx, op=op)


def modern_skull(x, y, s, at, face=-1, c=GOLD, style="inferred", fx=None):
    """A modern human skull's outline (dashed), at the same scale and nasion as harbin_skull: higher, rounder, shorter."""
    f = -face
    return poly([(x + f * a * s, y + b * s) for a, b in SKULL_M], "rgba(242,201,142,.04)", c, 3, at, curve=True, style=style, fx=fx)


def long_bone(x0, y0, x1, y1, w, at, kind="femur", c=BONEC, fx="pop", glow_=False):
    """A thigh bone (femur: a head on a neck at the top end) or a shin bone (tibia: a broad top), from (x0, y0) (top end) to (x1, y1)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    Q = lambda t, d: (x0 + ux * L * t + nx * w * d, y0 + uy * L * t + ny * w * d)
    if kind == "femur":
        shape = [Q(.02, -.9), Q(.1, -.75), Q(.16, -.5), Q(.5, -.42), Q(.86, -.55), Q(.95, -1.0), Q(1.0, -.7), Q(1.0, .7), Q(.95, 1.0), Q(.86, .55),
                 Q(.5, .44), Q(.14, .5), Q(.08, .9), Q(.0, .75), Q(-.02, .2)]
        head = poly(E(*Q(-.01, -.95), w * .62, w * .62, 18), c, BONE_E, 1.6, curve=True)
        extra = [head]
    else:
        shape = [Q(0, -1.05), Q(.04, -1.1), Q(.1, -.7), Q(.22, -.45), Q(.6, -.38), Q(.9, -.45), Q(.97, -.7), Q(1.0, -.55), Q(1.0, .55), Q(.96, .7),
                 Q(.9, .45), Q(.6, .38), Q(.22, .45), Q(.1, .7), Q(.04, 1.1), Q(0, 1.05)]
        extra = []
    els = extra + [poly(shape, c, BONE_E, 1.8, curve=True), ln([Q(.12, -.25), Q(.88, -.22)], -1, "#ffffff", 2, draw=False, op=.35)]
    out = [group(els, at, fx)]
    if glow_:
        out.insert(0, glow(round((x0 + x1) / 2, 1), round((y0 + y1) / 2, 1), round(L * .45), at, .45, "lamp"))
    return out


def rib_piece(x, y, s, at, fx="pop", c=BONEC):
    """A broken piece of rib: a flat, gently curved strip with ragged ends."""
    P = lambda a, b: (x + a * s, y + b * s)
    top = [P(-130, 10), P(-60, -22), P(20, -34), P(100, -30), P(134, -20)]
    bot = [P(136, -2), P(100, -10), P(20, -14), P(-60, -2), P(-126, 30)]
    shape = top + [P(140, -12), P(132, -8)] + bot + [P(-134, 22), P(-124, 18)]
    return group([poly(shape, c, BONE_E, 1.8, curve=True), ln([P(-100, 6), P(-20, -16), P(90, -20)], -1, "#ffffff", 1.8, draw=False, curve=True, op=.4)], at, fx)


def splinter(x, y, L, ang, at, c=BONEC, fx="pop", seed=1):
    """A small splinter of bone, about L long, pointing at `ang` degrees."""
    r = random.Random(seed)
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    w = L * r.uniform(.16, .24)
    ts = [0, .18, .4, .62, .82, 1]
    up = [(x + ux * L * t + nx * w * r.uniform(.3, .55) * (1 if 0 < t < 1 else .3), y + uy * L * t + ny * w * r.uniform(.3, .55) * (1 if 0 < t < 1 else .3)) for t in ts]
    dn = [(x + ux * L * t - nx * w * r.uniform(.3, .55), y + uy * L * t - ny * w * r.uniform(.3, .55)) for t in reversed(ts[1:-1])]
    return poly(up + dn, c, BONE_E, 1.4, at, fx=fx)


def beads(x0, y, n, step, r, at, cols, dt=.05, label_=None, lc=BONE, line_c="#8a7a66"):
    """A protein: a chain of n coloured beads on a string from x0, at y (cols: a list of colours, used in turn)."""
    out = [ln([(x0, y), (x0 + step * (n - 1), y)], at, line_c, 3, dur=.5)]
    out += [circ(x0 + step * k, y, r, cols[k % len(cols)], "rgba(255,255,255,.35)", 1.2, round(at + dt * k, 2), fx="pop") for k in range(n)]
    if label_:
        out.append(lab(x0 - 22, y + 10, label_, at, lc, 28, "end"))
    return out


PROT = ["#e8b87a", "#9fd0ff", "#8fd9b0", "#c9c1ee", "#efe6d2", "#e98a8a"]
SEQ = [0, 2, 1, 3, 4, 1, 0, 2, 4, 3, 1, 2, 5, 0, 3]


def grid(x0, y0, n, cols, cell, step, at, c, dt=.004, op=None, r=4):
    return [rect(x0 + step * (k % cols), y0 + step * (k // cols), cell, cell, c, r=r, at=round(at + dt * k, 3), op=op) for k in range(n)]


def cellbox(x0, y0, k, cols, cell, step, at, c, fx="pop", style="known", fill=None, sw=3):
    x, y = x0 + step * (k % cols), y0 + step * (k // cols)
    if style == "known":
        return rect(x, y, cell, cell, c, r=4, at=at, fx=fx)
    return rect(x - 3, y - 3, cell + 6, cell + 6, fill or "none", c, sw, 6, at, fx=fx, style=style)


def figure_c(x, y, h, at, c, fx="rise", op=None):
    return figure(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx, op)


def walker(x, y, h, at, c="#2a221b", face=1, fx="rise", op=None, stride=.22):
    """A walking figure (legs apart), facing right (face=1) or left, feet on y."""
    w = h * .26
    X = lambda a: x + face * a
    body = [(X(-w * .48), y - h * .78), (X(w * .48), y - h * .78), (X(w * .42), y - h * .42), (X(w * .2 + stride * h * .5), y), (X(w * .02 + stride * h * .5), y),
            (X(0), y - h * .36), (X(-w * .02 - stride * h * .5), y), (X(-w * .2 - stride * h * .5), y), (X(-w * .42), y - h * .42)]
    return [group([circ(X(w * .06), y - h * .9, h * .085, c), poly(body, c)], at, fx, op=op)]


def seated_fig(x, y, h, at, c, face=1, op=None):
    return [group(seated(x, y, h, -1, c, face), at, "rise", op=op)]


def yak(x, y, s, at, c="#3a302a", face=1, fx="rise", op=None):
    """A yak in silhouette, feet on y: a shaggy body with a hump, a low head and horns; s = 1 is about 160 units long."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    body = [P(-80, -60), P(-60, -92), P(-20, -104), P(20, -112), P(46, -100), P(64, -80), P(84, -70), P(96, -52), P(92, -36), P(78, -30), P(72, -14), P(66, -12),
            P(60, -30), P(52, 0), P(42, 0), P(40, -30), P(-40, -30), P(-44, 0), P(-54, 0), P(-56, -28), P(-66, -26), P(-70, 0), P(-80, 0), P(-82, -30), P(-88, -40)]
    horn = [P(80, -78), P(92, -96), P(104, -98), P(96, -88)]
    fringe = [P(-60, -34), P(-50, -14), P(-30, -26), P(-10, -12), P(10, -26), P(30, -14), P(44, -28)]
    return [group([poly(body, c, "rgba(255,226,190,.35)", 1.2, curve=True), poly(horn, "#cfc6b4", at=-1, curve=True), ln(fringe, -1, c, 6 * s, draw=False, curve=True)], at, fx, op=op)]


def bharal(x, y, s, at, c="#5e6878", face=1, fx="rise", op=None):
    """A blue sheep (bharal) in silhouette, feet on y, curved horns sweeping back; s = 1 is about 130 units long."""
    P = lambda a, b: (x + face * a * s, y + b * s)
    body = [P(-60, -70), P(-20, -76), P(30, -76), P(54, -84), P(66, -100), P(80, -102), P(90, -92), P(84, -82), P(70, -76), P(64, -56), P(52, -46), P(50, 0),
            P(42, 0), P(38, -40), P(-36, -40), P(-40, 0), P(-48, 0), P(-50, -42), P(-62, -50)]
    horn = [P(68, -100), P(56, -112), P(40, -110), P(36, -96), P(44, -100), P(56, -102)]
    return [group([poly(body, c, "rgba(200,215,235,.35)", 1, curve=True), poly(horn, "#d9cfba", at=-1, curve=True)], at, fx, op=op)]


def woolly_rhino(x, y, s, at, c="#5a4a3e", face=1, fx="rise", op=None):
    """A woolly rhinoceros in silhouette, feet on y, two horns; s = 1 is about 190 units long."""
    P = lambda a, b: (x + face * a * s, y + b * s)
    body = [P(-96, -56), P(-80, -84), P(-30, -100), P(20, -104), P(54, -96), P(76, -80), P(98, -60), P(112, -46), P(118, -30), P(104, -24), P(86, -30), P(70, -26),
            P(66, 0), P(52, 0), P(48, -26), P(-46, -26), P(-50, 0), P(-64, 0), P(-68, -28), P(-90, -36)]
    horn1 = [P(108, -48), P(130, -96), P(118, -44)]
    horn2 = [P(94, -66), P(102, -88), P(98, -62)]
    return [group([poly(body, c, "rgba(255,226,190,.4)", 1.2, curve=True), poly(horn1, "#cfc0a4", at=-1), poly(horn2, "#cfc0a4", at=-1)], at, fx, op=op)]


def eagle(x, y, s, at, c="#5a4330", fx="pop", op=None):
    """A golden eagle with its wings spread, seen from below, centre (x, y); s = 1 is about 300 units across."""
    P = lambda a, b: (x + a * s, y + b * s)
    wingL = [P(-10, -6), P(-60, -26), P(-110, -36), P(-150, -30), P(-142, -20), P(-150, -10), P(-136, -4), P(-140, 6), P(-120, 6), P(-90, 10), P(-40, 14), P(-8, 14)]
    wingR = [(2 * x - a, b) for a, b in wingL]
    body = [P(-10, -24), P(0, -36), P(10, -24), P(12, 20), P(22, 44), P(0, 40), P(-22, 44), P(-12, 20)]
    head = [P(-7, -30), P(0, -46), P(7, -30)]
    return [group([poly(wingL, c, "rgba(255,226,190,.3)", 1, curve=True), poly(wingR, c, "rgba(255,226,190,.3)", 1, curve=True), poly(body, "#6e5238", curve=True),
                   poly(head, "#c9a25a", at=-1)], at, fx, op=op)]


def monk(x, y, h, at, c="#7a2f2a", fx="rise", op=None):
    """A robed figure standing, feet on y (a plain silhouette in a monk's maroon robe)."""
    w = h * .3
    robe = [(x - w * .42, y - h * .8), (x + w * .42, y - h * .8), (x + w * .55, y - h * .45), (x + w * .62, y), (x - w * .62, y), (x - w * .55, y - h * .45)]
    sash = [(x - w * .4, y - h * .78), (x - w * .1, y - h * .78), (x + w * .5, y - h * .3), (x + w * .3, y - h * .25)]
    return [group([poly(robe, c), poly(sash, "#c98a2e", op=.85), circ(x, y - h * .89, h * .085, "#3a2a22")], at, fx, op=op)]


def cloud_dots(cx, cy, rx, ry, n, at, c="#cfe6ff", seed=3, dur=.03, edge="rgba(207,230,255,.6)"):
    """A breath of air: a soft cloud outline holding n oxygen dots."""
    r = random.Random(seed)
    out = [poly(E(cx, cy, rx, ry, 30), "rgba(207,230,255,.06)", edge, 2.2, at, curve=True, style="inferred", fx="pop")]
    pts = []
    while len(pts) < n:
        a, b = r.uniform(-1, 1), r.uniform(-1, 1)
        if a * a + b * b < .72 and all((a - p) ** 2 + (b - q) ** 2 > .045 for p, q in pts):
            pts.append((a, b))
    out += [circ(cx + a * rx, cy + b * ry, 7, c, at=round(at + .2 + dur * k, 2), fx="pop") for k, (a, b) in enumerate(pts)]
    return out


def vessel(cx, cy, R_, n, at, seed=2, dur=.06, crowd=False):
    """A blood vessel in cross-section, holding n red cells (discs with a pale centre)."""
    r = random.Random(seed)
    out = [circ(cx, cy, R_ + 14, "#3a1d1c", "#8a4a44", 3, at, fx="pop"), circ(cx, cy, R_, "#2a1312", at=at)]
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        a, b = r.uniform(-1, 1), r.uniform(-1, 1)
        if a * a + b * b < .78 and all((a - p) ** 2 + (b - q) ** 2 > (.035 if crowd else .05) for p, q in pts):
            pts.append((a, b))
    for k, (a, b) in enumerate(pts):
        x, y = cx + a * R_, cy + b * R_
        t = round(at + .3 + dur * k, 2)
        out += [group([circ(x, y, 17, BLOOD, "#ff9a90", 1), circ(x, y, 7, BLOOD_D)], t, "pop")]
    return out


def museum_case(x, y, w, h, at, fx="pop", lit=True):
    """A glass museum case on a plinth: (x, y) top left of the glass."""
    els = [rect(x - 20, y + h, w + 40, 150, "#2c241c", "#6a5a48", 2, 6), rect(x, y, w, h, "rgba(159,208,255,.06)", "rgba(220,235,255,.55)", 2.5, 4),
           ln([(x + 20, y + 20), (x + w * .3, y + 20)], -1, "#ffffff", 3, draw=False, op=.35), rect(x + w * .25, y + h - 24, w * .5, 24, "#4a3d2f", r=4)]
    out = [group(els, at, fx)]
    if lit:
        out.insert(0, glow(x + w / 2, y + h * .55, round(w * .8), at, .35, "lamp"))
    return out


def page(x, y, w, h, at, nlines=7, hl=(), hc=BLUE, c="#e9dfca", seed=1, fx="pop", op=None):
    """A sheet of paper with grey lines; hl: the lines highlighted (a passage)."""
    r = random.Random(seed)
    els = [rect(x, y, w, h, c, "#fff6e6", 1.5, 4)]
    for k in range(nlines):
        yy = y + h * (k + 1.2) / (nlines + 1.4)
        x1 = x + w * .12 + (w * .76) * (r.uniform(.6, 1) if k < nlines - 1 else .5)
        if k in hl:
            els.append(rect(x + w * .1, yy - 9, x1 - x - w * .1 + 6, 18, hc, r=4, op=.55))
        els.append(ln([(x + w * .12, yy), (x1, yy)], -1, "#8a7a62", 3, draw=False))
    return group(els, at, fx, op=op)


def stamp(x, y, t, at, c="#c84a3a", size=30, rot=-6):
    w = len(t) * size * .6 + 40
    els = [rect(x - w / 2, y - size, w, size * 1.6, "rgba(200,74,58,.08)", c, 3, 6), lab(x, y + size * .2, t, -1, c, size, scl=True, halo=False)]
    return group(els, at, "pop", tr="rotate(%d %.1f %.1f)" % (rot, x, y))


def preprint(x, y, w, h, at, fx="rise"):
    els = [rect(x, y, w, h, "#ece3cf", "#fff6e6", 1.5, 4), rect(x + w * .1, y + h * .08, w * .8, 14, "#3a3029", r=3),
           rect(x + w * .1, y + h * .16, w * .55, 10, "#7a6a58", r=3)]
    r = random.Random(7)
    for k in range(9):
        yy = y + h * (.28 + .07 * k)
        els.append(ln([(x + w * .1, yy), (x + w * (.1 + .8 * r.uniform(.6, 1)), yy)], -1, "#9a8c78", 3, draw=False))
    return group(els, at, fx)


def bag(x, y, w, h, at, fx="pop", n=0, seed=2, c="rgba(220,235,255,.10)"):
    """A clear sample bag with a zip line at the top, holding n splinters."""
    els = [rect(x, y, w, h, c, "rgba(230,240,255,.6)", 2, 10), ln([(x + 8, y + 18), (x + w - 8, y + 18)], -1, "#e98a8a", 3, draw=False)]
    r = random.Random(seed)
    for k in range(n):
        els.append(splinter(x + r.uniform(.12, .7) * w, y + r.uniform(.35, .85) * h, r.uniform(.12, .26) * w, r.uniform(-40, 40), -1, seed=seed * 31 + k))
    return group(els, at, fx)


def cave_arch(x0, x1, top, base, at=-1, c=ROCK_D, inner=FLAT):
    """The dark rock of a cave around an arched opening: the view from inside, looking at the floor (an arch from x0 to x1)."""
    cx = (x0 + x1) / 2
    arch = [(x0, base)] + [(cx + (x1 - x0) / 2 * math.cos(math.radians(a)), base - (base - top) * math.sin(math.radians(a))) for a in range(180, -1, -10)] + [(x1, base)]
    outer = [(-60, -60), (1840, -60), (1840, base), (x1, base)] + list(reversed(arch[1:-1])) + [(x0, base), (-60, base)]
    return [poly(outer, c, at=at), ln(arch, at, "rgba(255,226,190,.22)", 2, draw=False, curve=True)]


def strata(x0, x1, y0, hs, at, cols=SED, dt=.25, fx="fill", lines=True):
    """Sediment layers from y0 downwards, hs = their heights; each fills in turn."""
    out, y = [], y0
    for k, h in enumerate(hs):
        out.append(rect(x0, y, x1 - x0, h, cols[k % len(cols)], at=round(at + dt * k, 2), fx=fx, dur=.5))
        if lines and k:
            out.append(ln([(x0, y), (x1, y)], round(at + dt * k, 2), "rgba(255,226,190,.2)", 1.4, draw=False, style="inferred"))
        y += h
    return out


def ruler(x, y, L, at, cm=3, c=BONE):
    """A ruler L long marked in centimetres (cm marks, mm ticks)."""
    out = [rect(x, y, L, 46, "#d8c9a2", "#8a7a62", 1.5, 4, at, fx="pop")]
    step = L / (cm * 10)
    for k in range(cm * 10 + 1):
        hh = 22 if k % 10 == 0 else 14 if k % 5 == 0 else 8
        out.append(ln([(x + k * step, y), (x + k * step, y + hh)], at, "#3a3029", 2 if k % 10 == 0 else 1.2, draw=False))
    out += [lab(x + k * step * 10, y + 76, "%d cm" % k, at, c, 24) for k in range(cm + 1)]
    return out


def chips_axis(x0, x1, y, ya0, ya1, ticks, at, t=None):
    """A time axis of years ago (older at the left): returns (axis element, X function)."""
    X = lambda ya: round(x0 + (ya0 - ya) / (ya0 - ya1) * (x1 - x0), 1)
    return axis(x0, x1, y, [(X(v), lbl) for v, lbl in ticks], at, t), X


def asia_map(lon0=55, lon1=165, lat0=-22, lat1=62, rect_=(90, 120, 1600, 680), landc=LAND):
    m = Map(lon0, lon1, lat0, lat1, rect_)
    return m, land_el(m.land(), -1, landc)


def inset_map(m, x, y, w, h, at=-1, sea="#12202a", edge="#3c4a58", landc="#4a3d2f"):
    """A small map in a rounded window (m: a Map fitted to the window's rectangle)."""
    return {"k": "group", "clip": [x, y, w, h, 14], "bg": sea, "in": at, "els": [land_el(m.land(), -1, landc)]}


# ================================================================== cold open
CHIP = (1080, 559)            # the chip on the fingertip of the opening (base centre)


def s1():
    """THE HERO IMAGE, whole from the first frame: a modern fingertip in a shaft of light, holding a chip of bone and a ladybird of the same
    size (true scale: both about 7 mm). Then a hand skeleton draws itself and the tip of its little finger lights: where the chip comes from."""
    tc, tl, tt, ts = T("s1", "A chip of bone", .3), T("s1", "ladybird"), T("s1", "The tip of"), T("s1", "Siberia")
    els = light_shaft(1170, 1420, -40, 990, 1300, 600, -1, .045)
    els += [glow(1150, 520, 520, -1, .22, "lamp")]
    els += fingertip(930, 560, 1.0, -1)
    els += bone_chip(CHIP[0], CHIP[1], 1.0, -1, glow_=True)
    els += ladybird(1236, 566, 1.0, -1, face=1)
    els += [lab(1080, 462, "a chip of finger bone", tc, "#fff3dc", 32), lab(1300, 500, "a ladybird, for scale", tl + .4, "#f0c8b8", 28, "start")]
    hb, tip = hand_bones(430, 762, .95, tt)
    els += hb
    els += [ln([(tip[0] + 6, tip[1] + 8), (840, 470), (CHIP[0] - 44, CHIP[1] - 30)], tt + 1.0, GOLD, 2.5, "inferred", dur=1.0, curve=True),
            lab(tip[0] + 30, tip[1] - 46, "the tip of a little finger", tt + .8, GOLD, 30, "start"),
            lab(1660, 196, "Denisova Cave, Siberia, 2008", ts, BONE, 30, "end")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s2():
    """The chip glows at the lower left; a double helix unwinds out of it and climbs; where it rises, a long line of faceless figures appears
    one by one along a low horizon: a people nobody knew."""
    td, tp, tn = T("s2", "DNA"), T("s2", "people"), T("s2", "nobody knew")
    els = [glow(330, 640, 260, -1, .35, "lamp")] + bone_chip(330, 652, 1.3, -1, glow_=True)
    els += [ln([(700, 600), (1700, 600)], .2, "#8a7a66", 2, draw=False, op=.5), glow(1200, 600, 560, .3, .18, "blue")]
    els += helix(380, 626, 780, 520, td, n=11, amp=20, c1=GOLD, c2=DEN, w=3.2, dur=1.4)
    els += ghosts(830, 1640, 600, 14, tp, dt=.14, op=.6, seed=6)
    els += [lab(1236, 330, "a people nobody knew", tn, LILAC, 34)]
    return {"base": "dark", "stars": 70, "cam": CAM, "els": els}


def s3():
    """A head and shoulders in profile, drawn only as a dotted outline: no face, a question mark where the features would be. Then an empty
    museum name plate with a question mark."""
    tf, tn = T("s3", "face"), T("s3", "Nobody knew")
    els = [glow(640, 470, 420, .1, .22, "blue"), head_outline(620, 330, 1.0, .2, LILAC, "claimed", 3.5, face=1)]
    els += qmark(640, 520, tf, 150)
    els += [lab(620, 180, "their face", tf + .3, LILAC, 32)]
    els += [name_plate(1080, 360, 470, 160, tn), lab(1315, 470, "?", tn + .3, LILAC, 96, st="big", fx="pop"), lab(1315, 310, "their name", tn + .4, LILAC, 32)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


MAP_A = (40, 180, -12, 50)


def s4():
    """A dark map of Asia and the western Pacific: blue light pools where Denisovan DNA runs strongest today (New Guinea brightest, the
    Philippines, then a faint wash over East and South Asia); then the Tibetan Plateau lifts, pale: the roof of the world."""
    m = Map(*MAP_A, rect=(90, 150, 1600, 650))
    tg, tw = T("s4", "genes"), T("s4", "roof of the world", -.3)
    P = m.p
    els = [land_el(m.land(), -1, "#4f4131")]
    pools = [((112, 33), 260, .28, 0), ((79, 22), 190, .24, .15), ((121, 14), 90, .75, .5), ((143, -6), 130, .95, .8)]
    for (lo, la), r, op, dt in pools:
        x, y = P(lo, la)
        els.append(glow(x, y, r, round(tg + dt, 2), op, "blue"))
    ng, ph = P(143, -6), P(121, 15)
    els += [dot(ng[0], ng[1], 9, DEN, tg + .8), lab(ng[0] + 26, ng[1] + 52, "Papua New Guinea", tg + 1.0, DEN, 30, "start"),
            dot(ph[0], ph[1], 7, DEN, tg + .5), lab(ph[0] + 26, ph[1] + 8, "the Philippines", tg + .7, DEN, 30, "start")]
    tib = [P(lo, la) for lo, la in ((78, 35), (82, 36.5), (90, 36), (97, 35.5), (101, 33), (99, 29), (92, 28), (85, 28.5), (79, 31))]
    tb = P(89, 33)
    els += [poly(tib, "rgba(245,236,220,.42)", "#f5ecdc", 2, tw, curve=True, fx="pop"), glow(tb[0], tb[1], 120, tw, .45, "lamp"),
            ln([(tb[0] - 30, tb[1] - 34), (tb[0] - 120, tb[1] - 150)], tw + .2, BONE, 1.6, draw=False, op=.8),
            lab(tb[0] - 120, tb[1] - 166, "the roof of the world", tw + .3, BONE, 30)]
    els += [lab(1640, 200, "their DNA, today", tg + .2, DEN, 32, "end")]
    return {"base": "map", "cam": CAM, "els": els}


def s5():
    """The fingertip and its chip again; far behind them in the dark, the line of faceless figures stands dimmed; a large question mark
    rises over the chip. (The title card comes over this panel.)"""
    tq = T("s5", "So who were", .3)
    els = [ln([(100, 320), (1700, 320)], -1, "#8a7a66", 1.5, draw=False, op=.3)] + ghosts(140, 1660, 320, 24, .2, dt=.04, op=.22, seed=9, hmin=70, hmax=105)
    els += [glow(880, 540, 460, -1, .25, "lamp")] + light_shaft(760, 980, -40, 700, 1000, 600, -1, .04)
    els += fingertip(640, 590, 1.0, -1)
    els += bone_chip(790, 589, 1.0, -1, glow_=True)
    els += qmark(790, 492, tq, 170)
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


# ================================================================== chapter 1: a cave in Siberia
def body_outline(x, y, h, at, c=LILAC, style="claimed", w=3, fill="rgba(201,193,238,.04)", q=True):
    """A whole standing person drawn only as an outline (the same proportions as the plain figures), feet on y, with a question mark
    for a face."""
    bw = h * .26
    body = [(x - bw * .5, y - h * .78), (x + bw * .5, y - h * .78), (x + bw * .42, y - h * .42), (x + bw * .3, y), (x + bw * .08, y), (x, y - h * .36),
            (x - bw * .08, y), (x - bw * .3, y), (x - bw * .42, y - h * .42)]
    out = [circ(x, y - h * .9, h * .085, fill, c, w, at, style=style), poly(body, fill, c, w, at, style=style)]
    if q:
        out.append(lab(x, y - h * .87, "?", at + .3, c, round(h * .12), st="big", fx="pop"))
    return out


def mountains(seed, y, amp, n, c, at=-1, x0=-40, x1=1820, rough=.5):
    r = random.Random(seed)
    pts = [(x0, y + 320)]
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        pts.append((x, y - amp * (.55 + .45 * math.sin(k * 1.7 + seed)) - amp * rough * r.uniform(0, .6)))
    pts.append((x1, y + 320))
    return poly(pts, c, at=at)


def s6():
    """Denisova Cave at dawn: forested Altai ridges, a pale cliff with a tall dark arched mouth above a little river; a locator map; a tiny
    figure with a staff at the mouth for the hermit Denis."""
    th = T("s6", "hermit")
    tr_ = T("s6", "river")
    els = [mountains(3, 360, 120, 16, "#4c5468"), mountains(7, 470, 110, 14, "#38404a")]
    els += [conifer(120 + 46 * k + (k % 3) * 9, 560 - 30 * math.sin(k * .9), 70 + 22 * (k % 4), -1, "#1d2620") for k in range(15)]
    cliff = [(820, 640), (840, 420), (900, 300), (960, 240), (1080, 205), (1210, 190), (1360, 200), (1500, 222), (1640, 260), (1820, 300), (1820, 700), (820, 700)]
    els += [poly(cliff, "#8a7b6c", "rgba(255,236,206,.35)", 1.5, -1, curve=True),
            poly([(820, 640), (840, 420), (900, 300), (960, 240), (1010, 226), (980, 330), (950, 470), (930, 640)], "#a99a88", at=-1, curve=True, op=.7),
            poly([(1450, 222), (1640, 260), (1820, 300), (1820, 700), (1500, 700), (1560, 520), (1520, 360)], "#6a5c4f", at=-1, curve=True, op=.85)]
    r = random.Random(5)
    for k in range(9):                                                   # bedding planes and cracks in the limestone
        y0 = 250 + 44 * k + r.uniform(-8, 8)
        x0 = 900 + (k % 3) * 40
        els.append(ln([(x0, y0), (x0 + 140, y0 + 6), (x0 + 260, y0 + 2)], -1, "#5f5246", 2, draw=False, curve=True, op=.5))
        els.append(ln([(1360 + 60 * (k % 4), y0 - 10), (1500 + 50 * (k % 4), y0 + 4), (1640, y0 + 10)], -1, "#54483d", 2, draw=False, curve=True, op=.45))
    for k, (a, b) in enumerate(((900, 360), (980, 300), (1420, 300), (1540, 380), (1660, 330), (1050, 420), (1400, 470))):
        els.append(ln([(a, b), (a + 26, b + 60), (a + 14, b + 120)], -1, "#4f443a", 2.2, draw=False, op=.6))
    els += [conifer(1010 + 130 * k + 20 * (k % 2), 232 - 4 * (k % 3), 34 + 8 * (k % 3), -1, "#2c3a2c") for k in range(5)]
    mouth = [(1110, 610), (1100, 520), (1112, 430), (1150, 368), (1205, 340), (1262, 352), (1302, 400), (1318, 480), (1314, 560), (1320, 612)]
    els += [poly([(1090, 616), (1080, 520), (1094, 420), (1140, 350), (1205, 318), (1272, 334), (1320, 390), (1338, 480), (1334, 570), (1342, 616)], "#5c5046", at=-1, curve=True),
            poly(mouth, "#140f0c", "rgba(255,226,190,.25)", 2, -1, curve=True), glow(1210, 520, 110, -1, .25, "lamp"),
            poly([(1000, 700), (1080, 612), (1350, 612), (1500, 700)], "#6f6154", at=-1, curve=True)]
    els += [conifer(1560 + 40 * k, 330 + 30 * k, 60 + 10 * k, -1, "#26302a") for k in range(4)]
    river = [(-40, 742), (200, 724), (420, 736), (640, 716), (880, 728), (1120, 716), (1400, 732), (1820, 720)]
    els += [poly([(-40, 690), (1820, 680), (1820, 1040), (-40, 1040)], "#2a2a24", at=-1),
            ln(river, -1, "#4f7f96", 26, draw=False, curve=True), ln(river, -1, "#9fc6dc", 3, draw=False, curve=True, op=.5)]
    els += [ln([(300 + 160 * k, 727), (360 + 160 * k, 727)], -1, "#e9f2fb", 2, draw=False, op=.5) for k in range(6)]
    m = Map(40, 140, 18, 72, (120, 140, 400, 250))
    px, py = m.p(84.68, 51.4)
    els += [inset_map(m, 120, 140, 400, 250, .3), rect(120, 140, 400, 250, "none", "rgba(255,236,206,.4)", 2, 14, .3),
            {"k": "pin", "x": px, "y": py, "c": GOLD, "r": 7, "in": .6}, lab(px, py - 22, "Altai", .8, GOLD, 26)]
    els += [lab(1210, 300, "Denisova Cave", .6, "#fff3dc", 34), lab(560, 778, "a little river", tr_, "#cfe6ff", 26)]
    els += [glow(1150, 600, 60, th, .9, "fire"), figure(1150, 612, 54, th, "#2a2018"), ln([(1168, 560), (1176, 612)], th, "#5a4632", 3, draw=False),
            lab(1000, 560, "Denis, 18th century", th + .3, BONE, 26, "end")]
    return {"base": "sky", "tod": "dawn", "ground": 1300, "sun": [300, 400, 24], "ridges": [], "cam": CAM, "els": els}


def s7():
    """Inside the cave: the floor in cross-section under the dark rock, layers filling one by one; two diggers at a trench with a lamp;
    a shaft of light from the hole in the roof; stone tools, animal bones and a tooth pop in the layers as named."""
    tl, tt, tb, to = T("s7", "layer by layer"), T("s7", "stone tools"), T("s7", "animal bones"), T("s7", "tooth")
    GY = 430
    els = cave_arch(80, 1700, 120, GY, -1) + light_shaft(1160, 1260, 110, 1060, 1340, GY, -1, .07)
    els += [rect(80, GY, 1620, 50, SED[0], at=-1)] + strata(80, 1700, GY + 50, [62, 70, 70, 64, 64], tl, dt=.22, cols=SED[1:])
    els += [rect(640, GY, 420, 190, "#1e1712", at=tl + 1.4, op=.85), ln([(640, GY), (640, GY + 190), (1060, GY + 190), (1060, GY)], tl + 1.4, "#e3c99c", 2, draw=False, style="inferred")]
    els += [glow(860, GY - 30, 330, .3, .5, "lamp")]
    els += seated_fig(600, GY, 150, .3, "#6a5846", face=1) + seated_fig(1100, GY, 146, .4, "#6a5846", face=-1)
    els += [ln([(648, GY - 70), (690, GY + 30)], .4, "#8a6a48", 5, draw=False), ln([(1052, GY - 68), (1010, GY + 30)], .5, "#8a6a48", 5, draw=False),
            rect(846, GY - 40, 28, 38, "#5a4632", "#e3c99c", 1.5, 4, .3), glow(860, GY - 30, 60, .3, .95, "lamp")]
    tools = [(420, 520), (1320, 510)]
    for k, (x, y) in enumerate(tools):
        els.append(poly([(x - 30, y), (x - 6, y - 26), (x + 30, y - 12), (x + 22, y + 12), (x - 18, y + 14)], "#8f9aa6", "#e1e8ee", 1.5, round(tt + .2 * k, 2), fx="pop"))
    for k, (x, y, a) in enumerate(((300, 610, 10), (1450, 600, -15), (1220, 650, 5))):
        els += long_bone(x - 60, y - 10 * (a / 15), x + 60, y + 10 * (a / 15), 13, round(tb + .2 * k, 2), "femur" if k == 1 else "tibia", "#ddd0b6")
    els += [molar_side(860, 720, .55, to, roots=True)]
    els += [lab(420, 470, "stone tools", tt + .3, "#dfe8f2", 28), lab(320, 680, "animal bones", tb + .4, BONE, 28), lab(860, 790, "a tooth", to + .3, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s8():
    """The chip in a sealed sample bag tagged 2008; a dotted route across a small map of Eurasia from the Altai to Germany; an ancient
    DNA lab: a figure in a white suit at a clean bench, a sequencer with coloured bars."""
    t8, tp, tl = T("s8", "In two thousand and eight"), T("s8", "Part of it"), T("s8", "laboratory")
    els = [bag(170, 310, 270, 330, t8, n=0)] + bone_chip(305, 545, 1.15, t8 + .2, glow_=True)
    els += tag(305, 690, "2008", t8 + .4, GOLD, 30)
    m = Map(-12, 120, 30, 70, (540, 230, 640, 380))
    els += [inset_map(m, 540, 230, 640, 380, tp - .6), rect(540, 230, 640, 380, "none", "rgba(255,236,206,.4)", 2, 14, tp - .6)]
    dx, dy = m.p(84.68, 51.4)
    gx, gy = m.p(12.4, 51.3)
    els += [{"k": "pin", "x": dx, "y": dy, "c": GOLD, "r": 7, "in": round(tp - .4, 2)}, {"k": "pin", "x": gx, "y": gy, "c": DEN, "r": 7, "in": round(tp + .9, 2)},
            arrow([[dx - 8, dy - 6], [(dx + gx) / 2, dy - 120], [gx + 12, gy - 8]], tp, GOLD, 3, "known", 1.2),
            lab(dx, dy + 44, "Denisova Cave", tp - .3, GOLD, 26), lab(gx, gy + 44, "Germany", tp + 1.0, DEN, 26)]
    LX = 1250
    els += [rect(LX, 560, 420, 26, "#5a5650", "#a8a49c", 1.5, 4, tl - .3), rect(LX + 30, 586, 16, 120, "#3a3834", at=tl - .3), rect(LX + 374, 586, 16, 120, "#3a3834", at=tl - .3),
            rect(LX + 200, 340, 200, 220, "rgba(207,230,255,.08)", "rgba(220,235,255,.6)", 2, 6, tl - .2),
            rect(LX + 230, 470, 140, 80, "#2c3036", "#9fb0c0", 1.5, 6, tl), rect(LX + 246, 486, 108, 40, "#0f1418", at=tl)]
    els += [rect(LX + 252 + 14 * k, 520 - h, 10, h, c, at=round(tl + .3 + .06 * k, 2), fx="fill") for k, (h, c) in enumerate(((24, GOLD), (14, DEN), (30, GREEN), (18, LILAC), (26, GOLD), (10, DEN), (22, GREEN)))]
    els += [figure(LX + 110, 560, 230, tl - .1, "#e9eef2"), rect(LX + 96, 560 - 230 * .9 - 6, 28, 16, "#9fb0c0", r=6, at=tl - .1)]
    els += [lab(LX + 210, 760, "an ancient DNA lab", tl + .4, BONE, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s9():
    """Two grids of a hundred squares: a typical ancient bone (bacteria crowd it, a few squares of the owner's DNA) and this bone, where
    seventy of the hundred turn gold."""
    t0, ta, tb, t70 = .3, T("s9", "In most ancient bones"), T("s9", "In this one"), T("s9", "seventy percent")
    els = bone_chip(889, 215, .9, t0, glow_=True) + [lab(889, 275, "a lucky bone", t0 + .4, GOLD, 30)]
    LX0, RX0, Y0, ST, CE = 250, 1130, 320, 40, 32
    gold_l = {33, 58, 71}
    els += [lab(LX0 + 200, Y0 - 30, "a typical ancient bone", ta, MUTED, 28), lab(RX0 + 200, Y0 - 30, "this bone", tb, GOLD, 30)]
    els += [rect(LX0 + ST * (k % 10), Y0 + ST * (k // 10), CE, CE, GOLD if k in gold_l else "#56604a", r=4, at=round(ta + .2 + .006 * k, 3)) for k in range(100)]
    r = random.Random(11)
    for k in range(26):
        x, y = LX0 + r.uniform(10, 380), Y0 + r.uniform(10, 380)
        a = r.uniform(0, math.pi)
        els.append(ln([(x, y), (x + 16 * math.cos(a), y + 16 * math.sin(a))], round(ta + .8 + .02 * k, 2), "#a6c08a", 6, draw=False, op=.8))
    els += [rect(RX0 + ST * (k % 10), Y0 + ST * (k // 10), CE, CE, "#56604a", r=4, at=round(tb + .2 + .004 * k, 3)) for k in range(100)]
    els += [rect(RX0 + ST * (k % 10), Y0 + ST * (k // 10), CE, CE, GOLD, r=4, at=round(t70 - .2 + .02 * k, 2), fx="pop") for k in range(70)]
    els += [lab(LX0 + 200, Y0 + 440, "a tiny fraction", ta + 1.2, MUTED, 30), lab(RX0 + 200, Y0 + 446, "70 in 100", t70 + 1.2, GOLD, 40, st="serif"),
            glow(RX0 + 200, Y0 + 140, 280, t70 + .6, .3, "lamp")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


BASEC = {"A": "#e8b87a", "C": "#9fd0ff", "G": "#8fd9b0", "T": "#c9c1ee"}
SEQ1 = "ATGCGTACCTAGGATCCGTAAGCT"


def s10():
    """Two long open books become two rows of letters (A, C, G, T); a highlight runs along them letter by letter and rings the three that
    differ; few differences, close family."""
    tr_, tf = T("s10", "letter by letter", -.2), T("s10", "the fewer")
    seq2 = list(SEQ1)
    diffs = (5, 13, 19)
    for k in diffs:
        seq2[k] = {"A": "G", "G": "A", "C": "T", "T": "C"}[SEQ1[k]]
    X0, STP, W, H = 400, 48, 40, 56
    rows = ((330, SEQ1, "copy 1"), (500, "".join(seq2), "copy 2"))
    els = []
    for j, (y, sq, nm) in enumerate(rows):
        bx = 170
        els += [group([poly([(bx - 80, y - 40), (bx - 4, y - 46), (bx - 4, y + 46), (bx - 80, y + 40)], "#efe3c8", "#fff6e6", 1.5),
                       poly([(bx + 4, y - 46), (bx + 80, y - 40), (bx + 80, y + 40), (bx + 4, y + 46)], "#efe3c8", "#fff6e6", 1.5)] +
                      [ln([(bx - 70, y - 26 + 13 * q), (bx - 14, y - 28 + 13 * q)], -1, "#8a7a62", 2, draw=False) for q in range(5)] +
                      [ln([(bx + 14, y - 28 + 13 * q), (bx + 70, y - 26 + 13 * q)], -1, "#8a7a62", 2, draw=False) for q in range(5)], .3 + .2 * j, "pop"),
                lab(bx, y + 84, nm, .5 + .2 * j, MUTED, 24)]
        for k, ch in enumerate(sq):
            x = X0 + STP * k
            t = round(.6 + .2 * j + .02 * k, 2)
            els += [rect(x, y - H / 2, W, H, BASEC[ch], r=5, at=t), lab(x + W / 2, y + 10, ch, t, "#1a1511", 26, halo=False)]
    for k in range(24):
        els.append(rect(X0 + STP * k - 4, 330 - H / 2 - 8, W + 8, 170 + 16 + H - 56, "rgba(242,201,142,.10)", "rgba(242,201,142,.5)", 1.5, 6, round(tr_ + .07 * k, 2), fx="pop", dur=.25))
    for q, k in enumerate(diffs):
        x = X0 + STP * k + W / 2
        t = round(tr_ + .07 * k + .1, 2)
        els += [circ(x, 330, 38, "none", RED, 3.5, t, fx="draw", dur=.35), circ(x, 500, 38, "none", RED, 3.5, t, fx="draw", dur=.35)]
    els += [lab(889, 660, "3 differences in 24 letters", tf - .4, RED, 30), lab(889, 720, "the fewer differences, the closer the family", tf + .4, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


TREE = {"root": (889, 780), "fork": (889, 560), "us": (520, 250), "nea": (1240, 250), "dfork": (1046, 420), "den": (1500, 270), "deep": (889, 700), "old": (1470, 540)}


def s11():
    """A family tree growing upward: 'us' and 'Neanderthals' fork near the top; lower down, an older dashed branch splits off: the first,
    small reading of 2010 (a loop of mitochondrial DNA beside it)."""
    tb, to = T("s11", "pointed to a branch"), T("s11", "even older")
    Tr = TREE
    els = [ln([Tr["root"], Tr["fork"]], .2, BONE, 8, dur=.6), ln([Tr["fork"], (720, 420), Tr["us"]], .7, US, 7, dur=.7, curve=True),
           ln([Tr["fork"], Tr["dfork"], Tr["nea"]], .8, NEA, 7, dur=.7, curve=True),
           dot(*Tr["us"], 12, US, 1.4), lab(Tr["us"][0], Tr["us"][1] - 30, "us", 1.4, US, 32),
           dot(*Tr["nea"], 12, NEA, 1.5), lab(Tr["nea"][0], Tr["nea"][1] - 30, "Neanderthals", 1.5, NEA, 32),
           ln([(250, 300), (250, 740)], .4, MUTED, 2, draw=False, op=.7), arrow([[250, 640], [250, 742]], .4, MUTED, 2, "known", .4), lab(250, 790, "older", .5, MUTED, 26)]
    els += [ln([Tr["deep"], (1200, 660), Tr["old"]], tb, LILAC, 5, "claimed", dur=1.0, curve=True), dot(*Tr["old"], 10, LILAC, tb + .9),
            circ(Tr["old"][0] - 170, Tr["old"][1] + 176, 22, "none", LILAC, 4, to), lab(Tr["old"][0] - 134, Tr["old"][1] + 186, "a loop of DNA", to + .2, LILAC, 26, "start")]
    els += tag(Tr["old"][0], Tr["old"][1] - 44, "first reading, 2010", tb + 1.0, LILAC, 26, "claimed")
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s12_add():
    """The whole genome: the first reading is struck through; a new solid blue branch grows from the Neanderthal branch as its sister:
    the Denisovans."""
    tg, tc, tn = T("s12", "the whole genome"), T("s12", "cousins"), T("s12", "the Denisovans")
    Tr = TREE
    ox, oy = Tr["old"]
    els = [strike(ox - 140, oy - 44, ox + 140, oy - 44, tg + .3)]
    els += [ln([Tr["dfork"], (1260, 360), Tr["den"]], tc, DEN, 8, dur=.9, curve=True), glow(*Tr["den"], 130, tn, .7, "blue"), dot(*Tr["den"], 14, DEN, tn),
            lab(Tr["den"][0] + 10, Tr["den"][1] - 34, "Denisovans", tn, DEN, 36, st="serif"),
            lab(Tr["dfork"][0] + 150, Tr["dfork"][1] + 24, "cousins", tc + .4, BONE, 26, "start")]
    els += tag(1330, 160, "the whole genome, 2010", tg, DEN, 26)
    return els


def s13():
    """2012, a sharper genome: a head and shoulders drawn only in dashes beside a strand of DNA; colour swatches pop as named (dark skin,
    brown hair, brown eyes), each linked to its place."""
    tg, ts, th, te = T("s13", "a sharper reading"), T("s13", "dark skin"), T("s13", "brown hair"), T("s13", "brown eyes")
    cx, cy, s_ = 720, 330, .95
    els = helix(200, 560, 470, 560, .3, n=8, amp=18, w=3, dur=.9) + [head_outline(cx, cy, s_, .2, BONE, "inferred", 3, "rgba(245,236,220,.04)", face=1)]
    els += tag(330, 230, "2012: a sharper genome", tg, DEN, 26)
    spots = ((ts, (cx + 70 * s_, cy + 136 * s_), 560, "#6b4430", "dark skin"), (th, (cx - 20 * s_, cy - 78 * s_), 260, "#3e2a1c", "brown hair"),
             (te, (cx + 98 * s_, cy + 58 * s_), 410, "#5a3a22", "brown eyes"))
    for t, (hx, hy), sy, col, name in spots:
        els += [dot(hx, hy, 8, BONE, t), ln([(hx + 10, hy), (1150, sy)], t, BONE, 1.6, draw=False, op=.7),
                circ(1190, sy, 36, col, "#f5ecdc", 2.5, t + .1, fx="pop"), lab(1250, sy + 10, name, t + .2, BONE, 30, "start")]
    els += [circ(1190, 410, 12, "#1a1511", at=te + .2), circ(1186, 405, 4, "#f5ecdc", at=te + .2)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s14():
    """Two molars seen from above: ours, and the Denisova molar with about twice the chewing area (1.4 times as wide); ours laid over it in
    dashes; a tag: the same DNA as the finger."""
    tm, td, th, tt = .4, T("s14", "same kind of DNA"), T("s14", "huge"), T("s14", "twice the size")
    els = [glow(560, 470, 200, tm, .25, "lamp"), molar_top(560, 470, 95, tm), lab(560, 640, "ours", tm + .2, US, 30)]
    els += tag(1150, 196, "the same DNA as the finger", td, DEN, 26)
    els += [glow(1150, 470, 280, th, .3, "lamp"), molar_top(1150, 470, 134, th), lab(1150, 690, "the Denisova molar", th + .3, BONE, 30),
            molar_top(1150, 470, 95, tt, fill="none", c=GOLD, style="inferred", fx="pop"), lab(1150, 300, "about twice the area", tt + .4, GOLD, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s15():
    """A museum case on a lit plinth with the chip and the big molar inside; behind it a full-height person drawn only as a dashed outline,
    a question mark for a face; the plinth label: known from DNA."""
    tk = T("s15", "known from its DNA")
    els = [glow(889, 250, 260, .1, .25, "lamp")] + light_shaft(820, 960, -40, 700, 1080, 640, -1, .05)
    els += body_outline(889, 760, 620, .3, LILAC, "claimed", 3)
    els += museum_case(700, 400, 380, 260, .2)
    els += bone_chip(800, 640, .75, .4, glow_=False) + [molar_side(975, 640, .55, .5, roots=False)]
    els += helix(780, 740, 1000, 740, tk, n=6, amp=10, w=2.5, dur=.6) + [lab(889, 790, "known from DNA", tk + .3, DEN, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== chapter 2: two peoples, one girl
def s16():
    """A splinter of bone beside a ruler (2.5 cm); a dashed arrow carries it into a sample bag already full of splinters; shelves of
    bags behind: thousands of splinters."""
    tn, tb = T("s16", "Nothing marked", -.2), T("s16", "it went into a bag")
    els = ruler(200, 430, 300, .3, cm=3) + [splinter(212, 392, 250, -3, .2, seed=4)]
    els += [lab(338, 330, "2.5 cm", .5, GOLD, 30), lab(338, 270, "human?", tn + .3, LILAC, 30)]
    for row in range(3):
        for k in range(6):
            els.append(bag(1150 + 85 * k, 200 + 175 * row, 70, 120, round(tb + .5 + .04 * (row * 6 + k), 2), n=5, seed=row * 7 + k + 3, c="rgba(220,235,255,.05)"))
        els.append(rect(1130, 330 + 175 * row, 540, 10, "#4a3d2f", "#7a6a58", 1, 3, round(tb + .5, 2)))
    els += [bag(640, 260, 380, 440, tb, n=42, seed=9), arrow([[480, 380], [560, 330], [700, 420]], tb - .4, GOLD, 3, "inferred", .7),
            lab(1400, 790, "thousands of splinters", tb + 1.2, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


BARS = [3, 1, 2, 1, 3, 1, 1, 2, 3, 1, 2]


def barcode(x, y, w, h, at, seed, c="#efe6d2", fx="pop"):
    r = random.Random(seed)
    els, xx = [rect(x - 6, y - 6, w + 12, h + 12, "#1b1612", "rgba(255,236,206,.3)", 1, 4)], x
    while xx < x + w - 2:
        bw = r.choice((2, 3, 5))
        els.append(rect(xx, y, bw, h, c))
        xx += bw + r.choice((2, 3, 4))
    return group(els, at, fx)


def s17():
    """A conveyor of splinters under a scanner; above each a barcode pops with the animal it belongs to; a counter reads 2,315; one barcode
    lights gold: human."""
    tc, tw, tb, th = T("s17", "collagen"), T("s17", "two thousand three hundred"), T("s17", "barcode"), T("s17", "One scrap")
    els = [rect(110, 680, 1560, 46, "#3a3029", "#7a6a58", 2, 23, .2), circ(140, 703, 20, "#5a4a3a", "#9a8a78", 2, .2), circ(1640, 703, 20, "#5a4a3a", "#9a8a78", 2, .2)]
    els += [ln([(150 + 40 * k, 690), (170 + 40 * k, 716)], .2, "#5a4a3a", 2, draw=False, op=.7) for k in range(38)]
    names = ["bison", "horse", "deer", "hyena", "bear", "horse", "human", "deer", "wolf"]
    for k, nm in enumerate(names):
        x = 210 + 170 * k
        t = round(tb + .22 * k, 2)
        hum = nm == "human"
        els += [splinter(x - 40, 676 - (k % 2) * 3, 88, -4 + 3 * (k % 3), .3 + .03 * k, seed=20 + k, c="#f3e6c6" if hum else BONEC)]
        els += [barcode(x - 42, 540, 84, 62, t, seed=40 + k, c=GOLD if hum else "#efe6d2"), lab(x, 510, nm, t + .1, GOLD if hum else MUTED, 28 if hum else 25)]
        if hum:
            els += [glow(x, 590, 150, th, .8, "lamp"), figure(x, 480, 70, th, GOLD), rect(x - 54, 526, 108, 90, "none", GOLD, 3, 8, th, fx="pop")]
    els += [rect(820, 250, 140, 70, "#2c2620", "#cbbca8", 2, 10, .3), poly([(860, 320), (920, 320), (1010, 676), (770, 676)], "rgba(255,90,80,.10)", at=.4),
            ln([(890, 320), (890, 676)], .4, "#ff6a5a", 2, draw=False, op=.8)]
    els += [lab(1640, 230, "2,315 splinters", tw, GOLD, 34, "end"), lab(140, 230, "collagen: the protein of bone", tc, BONE, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s18():
    """A mother and a child; a small amber ring (mitochondrial DNA) passes along a curved arrow from her to the child; the tag: Neanderthal."""
    tm, tn = T("s18", "from mother to child"), T("s18", "was Neanderthal")
    GY = 720
    els = [ln([(260, GY), (1520, GY)], .1, "#8a7a66", 2, draw=False, op=.6), glow(560, 500, 260, .2, .3, "lamp"),
           figure(560, GY, 380, .2, "#c9965e"), figure(1200, GY, 230, .4, "#cdb594")]
    els += [circ(560, 440, 26, "none", NEA, 6, .7, fx="pop"), arrow([[600, 440], [880, 300], [1170, 520]], tm, NEA, 3, "known", 1.2),
            circ(1200, 540, 22, "none", NEA, 6, tm + 1.1, fx="pop"), glow(1200, 540, 70, tm + 1.1, .7, "lamp")]
    els += [lab(889, 240, "mitochondrial DNA: from the mother only", .6, BONE, 30)]
    els += tag(1200, 420, "Neanderthal", tn, NEA, 30)
    els += [lab(560, 770, "mother", .6, MUTED, 26), lab(1200, 770, "child", .7, MUTED, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s19():
    """2018, her whole genome: two long bars, the two copies of her DNA under a mother and a father; the top one fills amber (Neanderthal),
    the bottom one blue (Denisovan); a row of sites shows one of each, almost everywhere."""
    tg, tw, tn, td, te = T("s19", "whole genome"), T("s19", "We each carry"), T("s19", "Neanderthal"), T("s19", "the other Denisovan"), T("s19", "almost everywhere")
    X0, X1 = 420, 1240
    els = tag(889, 200, "2018: her whole genome", tg, DEN, 28)
    els += [figure(250, 400, 170, .4, "#c9965e"), lab(250, 440, "mother", .6, NEA, 26), figure(1560, 400, 186, .6, "#6f93b5"), lab(1560, 440, "father", .8, DEN, 26)]
    for y, t, c, fill_t, nm in ((480, tw + .4, NEA, tn, "from her Neanderthal mother"), (600, tw + .6, DEN, td, "from her Denisovan father")):
        els += [rect(X0, y - 24, X1 - X0, 48, "none", c, 2.5, 24, t, style="inferred", fx="pop"),
                ln([(X0 + 22, y), (X1 - 22, y)], fill_t, c, 40, dur=1.4), lab((X0 + X1) / 2, y + 10, nm, fill_t + 1.0, "#1a1511", 28, halo=False)]
    els += [arrow([[290, 470], [350, 500], [X0 - 10, 482]], tw + .5, NEA, 2.5, "known", .6), arrow([[1530, 470], [1420, 600], [X1 + 10, 604]], tw + .7, DEN, 2.5, "known", .6)]
    for k in range(14):
        x = X0 + 40 + k * (X1 - X0 - 80) / 13
        t = round(te + .06 * k, 2)
        els += [dot(x, 700, 9, NEA, t), dot(x, 730, 9, DEN, t)]
    els += [lab(250, 724, "one of each", te + .4, BONE, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def flames(x, y, s, at):
    out = [glow(x, y - 30 * s, round(300 * s), at, .85, "fire")]
    out += [ln([(x - 46 * s, y + 6), (x + 40 * s, y - 8)], at, "#4a3220", 12 * s, draw=False), ln([(x - 40 * s, y - 8), (x + 46 * s, y + 6)], at, "#3a2618", 12 * s, draw=False)]
    for k, (dx, h, c) in enumerate(((-18, 70, "#e8743a"), (10, 90, "#f2a23a"), (-2, 54, "#ffd27a"), (22, 50, "#ffb24a"))):
        out.append(poly([(x + (dx - 18) * s, y - 4), (x + dx * s, y - h * s), (x + (dx + 18) * s, y - 4)], c, at=at, curve=True, op=.9))
    return out


def s20():
    """A hearth inside the cave: the fire in the middle, a Neanderthal woman lit amber, a Denisovan man lit blue, and between them a girl."""
    tm, tf = T("s20", "Her mother"), T("s20", "Her father")
    GY = 700
    els = cave_arch(80, 1700, 150, GY + 4, -1) + [rect(-40, GY, 1860, 340, "#1e1813", at=-1)]
    els += flames(1000, GY, 1.0, .2)
    els += seated_fig(620, GY, 280, .3, "#a8784a", face=1) + seated_fig(1360, GY, 300, .5, "#5d7f9e", face=-1) + seated_fig(830, GY, 200, .4, "#c8ad86", face=1)
    els += [lab(600, 440, "mother: Neanderthal", tm, NEA, 32), lab(1380, 420, "father: Denisovan", tf, DEN, 32), lab(830, 790, "their daughter", tm + .6, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s21():
    """A time axis from 200,000 years ago to today: at about 100,000 a gold mark and a girl: Denny, at least 13; her dating range below."""
    t13, td = T("s21", "at least thirteen"), T("s21", "Denny")
    ax, X = chips_axis(200, 1580, 600, 200000, 0, [(200000, "200,000"), (150000, "150,000"), (100000, "100,000"), (50000, "50,000"), (0, "today")], .2, "years ago")
    xd = X(100000)
    els = [ax, dot(xd, 600, 12, GOLD, t13), glow(xd, 520, 160, t13, .45, "lamp"), figure(xd, 588, 150, t13, "#cdb594"),
           lab(xd + 40, 470, "at least 13", t13 + .3, BONE, 28, "start"), lab(xd, 400, "Denny", td, GOLD, 48, st="serif", fx="pop")]
    els += bracket(X(140000), X(80000), 700, t13 + .8, None, GOLD, up=True, style="inferred") + [lab(xd, 750, "dated 140,000 to 80,000 years ago", t13 + 1.0, MUTED, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s22():
    """Eurasia: Denisova Cave; the Neanderthals of western Europe (amber); a dashed amber arc from Europe to the Altai: her mother's people;
    by the cave a small family tree: the father's blue line with one amber twig; a dim amber dot: an earlier Neanderthal of the same cave."""
    tf, tm, tw, te = T("s22", "Her father had"), T("s22", "her mother's people"), T("s22", "western Europe"), T("s22", "earlier in the same cave")
    m = Map(-12, 130, 30, 70, (90, 160, 1600, 600))
    cx, cy = m.p(84.68, 51.4)
    ex, ey = m.p(8, 47.5)
    els = [land_el(m.land(), -1), {"k": "pin", "x": cx, "y": cy, "c": GOLD, "r": 9, "in": .3}, lab(cx, cy + 50, "Denisova Cave", .4, GOLD, 28)]
    tx, ty = cx + 130, cy - 120
    els += [ln([(tx, ty + 110), (tx, ty)], tf, DEN, 5, dur=.5), ln([(tx, ty + 60), (tx + 40, ty + 26)], tf + .4, NEA, 4, dur=.4),
            ln([(tx, ty + 30), (tx - 30, ty - 4)], tf + .3, DEN, 4, dur=.4), lab(tx + 30, ty - 20, "her father's family", tf + .5, DEN, 26, "start")]
    els += [glow(ex, ey, 170, tw - .4, .55, "lamp"), dot(ex, ey, 10, NEA, tw - .4), lab(ex, ey + 56, "Neanderthals of western Europe", tw, NEA, 28),
            arrow([[ex + 20, ey - 10], [(ex + cx) / 2, ey - 170], [cx - 22, cy - 12]], tm, NEA, 3.5, "inferred", 1.4),
            lab((ex + cx) / 2, ey - 196, "her mother's people", tm + .6, NEA, 30)]
    els += [dot(cx - 26, cy + 14, 8, mix(NEA, t=.55), te), lab(cx - 40, cy + 100, "an earlier Neanderthal here", te + .2, MUTED, 24, "end")]
    return {"base": "map", "cam": CAM, "els": els}


def s23():
    """Dusk on a plain: two small groups walk towards each other, amber from the left and blue from the right; where they meet, two small
    children appear between them in a warm light."""
    tc = T("s23", "children")
    GY = 690
    els = [mountains(11, 610, 70, 12, "#2c2630"), rect(-40, GY, 1860, 360, "#2a221d", at=-1), ln([(-40, GY), (1820, GY)], -1, "rgba(255,226,190,.35)", 1.5, draw=False)]
    for k in range(4):
        els += walker(330 + 70 * k, GY, 190 - 14 * (k % 2) - (60 if k == 3 else 0), round(.3 + .15 * k, 2), "#8a6a48", face=1)
        els += walker(1450 - 70 * k, GY, 200 - 16 * (k % 2) - (60 if k == 3 else 0), round(.4 + .15 * k, 2), "#4f6a85", face=-1)
    els += [glow(889, 600, 300, tc, .6, "lamp")] + walker(855, GY, 110, tc, "#cdb594", face=1, stride=.12) + walker(925, GY, 96, tc + .2, "#cdb594", face=-1, stride=.12)
    return {"base": "sky", "tod": "dusk", "ground": 1300, "sun": [889, 560, 30], "ridges": [], "cam": CAM, "els": els}


# ================================================================== chapter 3: their genes in us
def s24():
    """A person (Papua New Guinea) beside a grid of a hundred squares: four turn solid blue, two more get a dashed rim (4 to 6 in 100);
    then a field of a thousand tiny squares where just two light up: mainland Asia, 2 in 1,000."""
    tg, t4, ta, t2 = T("s24", "Split a person's"), T("s24", "four to six"), T("s24", "Across mainland Asia"), T("s24", "two parts in a thousand")
    X0, Y0, ST, CE = 420, 230, 44, 38
    els = [figure(230, 680, 320, .2, "#c9b49a"), lab(230, 736, "Papua New Guinea", .4, BONE, 28)]
    els += grid(X0, Y0, 100, 10, CE, ST, tg, "#4e463c", dt=.006)
    els += [cellbox(X0, Y0, k, 10, CE, ST, round(t4 + .2 * j, 2), DEN) for j, k in enumerate((96, 97, 98, 99))]
    els += [cellbox(X0, Y0, k, 10, CE, ST, round(t4 + 1.0 + .2 * j, 2), DEN, style="inferred") for j, k in enumerate((94, 95))]
    els += [lab(X0 + 218, 720, "4 to 6 in 100", t4 + .6, DEN, 34)]
    F0, FY, FS, FC = 1010, 250, 16, 12
    els += [rect(F0 + FS * (k % 40), FY + FS * (k // 40), FC, FC, "#4e463c", r=2, at=round(ta + .0012 * k, 3)) for k in range(1000)]
    els += [rect(F0 + FS * (k % 40) - 3, FY + FS * (k // 40) - 3, FC + 6, FC + 6, DEN, r=3, at=round(t2 + .2 * j, 2), fx="pop") for j, k in enumerate((987, 988))]
    els += [glow(F0 + FS * 27.5, FY + FS * 24.5, 70, t2 + .2, .8, "blue"), lab(F0 + 316, 720, "mainland Asia: 2 in 1,000", t2 + .4, DEN, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def open_book_(cx, cy, w, h, at, c="#cfe0f2", hl=(1, 2), hc=DEN):
    L = [(cx - w, cy - h * .45), (cx - 6, cy - h * .5), (cx - 6, cy + h * .5), (cx - w, cy + h * .55)]
    Rr = [(cx + 6, cy - h * .5), (cx + w, cy - h * .45), (cx + w, cy + h * .55), (cx + 6, cy + h * .5)]
    els = [poly(L, c, "#fff6e6", 1.5), poly(Rr, c, "#fff6e6", 1.5), ln([(cx, cy - h * .5), (cx, cy + h * .52)], -1, "#8a7a62", 3, draw=False)]
    for k in range(6):
        yy = cy - h * .32 + k * h * .13
        for x0, x1 in ((cx - w + 16, cx - 22), (cx + 22, cx + w - 16)):
            if k in hl and x0 > cx:
                els.append(rect(x0 - 4, yy - 8, x1 - x0 + 8, 16, hc, r=4, op=.6))
            els.append(ln([(x0, yy), (x1, yy)], -1, "#6a5a48", 2.5, draw=False))
    return group(els, at, "pop")


def s25():
    """A row of hand-copied pages, generation after generation, each with the same passage highlighted blue; above them a rare old edition
    with that passage; thin lines tie the passages word for word; a tick."""
    tc, to, tm, tf = T("s25", "Think of a long text"), T("s25", "a rare old edition"), T("s25", "word for word"), T("s25", "that's where it came from")
    els = qmark(305, 420, .4, 90)
    for k in range(5):
        x = 210 + 290 * k
        els.append(page(x, 470, 190, 250, round(.5 if k == 0 else tc + .3 * k, 2), 8, hl=(3, 4), seed=k + 2))
        if k:
            els.append(arrow([[x - 92, 595], [x - 10, 595]], round(tc + .3 * k - .1, 2), MUTED, 2.5, "known", .3))
    els += [lab(889, 790, "copied by hand, generation after generation", tc + 1.4, MUTED, 28)]
    els += [open_book_(889, 250, 210, 150, to), lab(889, 150, "a rare old edition", to + .2, DEN, 30)]
    for k in range(5):
        x = 210 + 290 * k + 95
        els.append(ln([(940, 262), (x, 470 + 250 * 4.6 / 9.4 - 8)], round(tm + .1 * k, 2), DEN, 1.8, "inferred", dur=.5))
    els += [tick(1150, 250, tf, GREEN, 1.4)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s26():
    """Island Southeast Asia and New Guinea: Luzon (the Ayta Magbukon) and the New Guinea highlands glow blue; two bars: the Ayta Magbukon's
    about a third taller than the Papuan Highlanders'."""
    ta, tt = T("s26", "The Ayta Magbukon"), T("s26", "about a third")
    m = Map(95, 155, -12, 22, (90, 150, 1040, 620))
    ax_, ay_ = m.p(120.5, 14.9)
    px, py = m.p(145, -6)
    els = [land_el(m.land(), -1), glow(ax_, ay_, 130, ta, .9, "blue"), glow(px, py, 130, ta + .4, .7, "blue"),
           {"k": "pin", "x": ax_, "y": ay_, "c": DEN, "r": 8, "in": ta}, lab(ax_ - 20, ay_ - 26, "Ayta Magbukon, Luzon", ta + .2, DEN, 26, "end"),
           {"k": "pin", "x": px, "y": py, "c": DEN, "r": 8, "in": ta + .4}, lab(px, py + 52, "Papuan Highlanders", ta + .5, DEN, 26)]
    BY = 700
    els += [rect(1180, 180, 500, 590, "rgba(18,13,10,.72)", "rgba(255,236,206,.25)", 1.5, 14, ta - .2),
            ln([(1220, BY), (1640, BY)], ta, MUTED, 2, draw=False),
            rect(1260, BY - 300, 120, 300, DEN_D, at=ta + .5, fx="fill", dur=.8), rect(1480, BY - 405, 120, 405, DEN, at=tt, fx="fill", dur=1.0),
            lab(1320, BY + 40, "Papuan", ta + .6, MUTED, 26), lab(1320, BY + 70, "Highlanders", ta + .6, MUTED, 26),
            lab(1540, BY + 40, "Ayta", tt + .2, DEN, 26), lab(1540, BY + 70, "Magbukon", tt + .2, DEN, 26),
            lab(1540, BY - 430, "about a third more", tt + .8, DEN, 28)]
    return {"base": "map", "cam": CAM, "els": els}


def s27():
    """A family tree running from older (left) to recent (right): the Denisovan trunk splits early into two branches, group 1 and group 2,
    far apart; both send thin lines into one figure: Papua New Guinea."""
    tg, ta = T("s27", "at least two"), T("s27", "hundreds of thousands")
    els = [ln([(160, 470), (480, 470)], .2, DEN, 9, dur=.6), lab(300, 440, "Denisovans", .5, DEN, 30),
           ln([(480, 470), (700, 300), (1180, 280)], tg, DEN, 7, dur=1.0, curve=True), ln([(480, 470), (700, 640), (1180, 660)], tg + .2, DEN_D, 7, dur=1.0, curve=True),
           lab(1050, 250, "group 1", tg + .9, DEN, 30), lab(1050, 710, "group 2", tg + 1.0, DEN_D, 30)]
    els += [ln([(1180, 280), (1330, 380), (1490, 470)], tg + 1.3, DEN, 2.5, dur=.6, curve=True), ln([(1180, 660), (1330, 560), (1490, 490)], tg + 1.4, DEN_D, 2.5, dur=.6, curve=True),
            figure(1540, 640, 260, tg + 1.6, "#c9b49a"), lab(1540, 690, "Papua New Guinea", tg + 1.8, BONE, 26)]
    els += [ln([(640, 330), (640, 610)], ta, GOLD, 2, "inferred", dur=.5), lab(660, 480, "hundreds of thousands", ta + .3, GOLD, 26, "start"),
            lab(660, 512, "of years apart", ta + .3, GOLD, 26, "start")]
    els += [ln([(160, 790), (1500, 790)], .3, MUTED, 1.5, draw=False, op=.5), lab(160, 770, "older", .4, MUTED, 24, "start"), lab(1500, 770, "recent", .4, MUTED, 24, "end")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s28():
    """Thin air: a breath at sea level holds 30 oxygen dots, a breath high up 20; then a blood vessel in cross-section fills with red cells
    until it is crowded: thick blood."""
    tb, tc, tt = T("s28", "every breath"), T("s28", "extra red blood cells"), T("s28", "thick")
    mt = [(40, 820), (180, 700), (300, 620), (390, 560), (470, 520), (520, 500), (560, 512), (640, 560), (760, 640), (880, 720), (960, 820)]
    els = [poly(mt, "#4a4238", at=-1), poly([(390, 560), (470, 520), (520, 500), (560, 512), (640, 560), (590, 568), (548, 548), (500, 560), (450, 548)], "#e9eef2", at=-1, op=.8),
           poly([(520, 500), (560, 512), (640, 560), (760, 640), (880, 720), (960, 820), (700, 820), (620, 640), (560, 560)], "#3a332b", at=-1, op=.8)]
    els += walker(500, 504, 70, .2, "#1e1813", face=1)
    els += cloud_dots(300, 270, 130, 80, 30, tb - .2, seed=4) + [lab(300, 400, "sea level", tb - .1, MUTED, 26)]
    els += cloud_dots(650, 330, 130, 80, 20, tb + .4, seed=6) + [lab(650, 460, "high up", tb + .5, "#cfe6ff", 26)]
    els += vessel(1270, 450, 210, 46, tc, seed=3, dur=.05, crowd=True) + [lab(1270, 740, "thick blood", tt, BLOOD, 32)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s29():
    """Two vessels side by side, high up: most people (crowded) and most Tibetans (far fewer cells); below, a DNA strand with one segment
    glowing blue (EPAS1), and a dashed blue line from it to a Denisovan figure: 2014, a Denisovan version."""
    tm, tl, tt = T("s29", "Most Tibetans"), T("s29", "thickens far less"), T("s29", "traced that version")
    els = vessel(470, 340, 150, 40, .2, seed=5, dur=.03, crowd=True) + [lab(470, 540, "most people, high up", .5, MUTED, 28)]
    els += vessel(1000, 340, 150, 19, tl - .6, seed=8, dur=.05) + [lab(1000, 540, "most Tibetans", tl - .4, GOLD, 30)]
    els += helix(230, 680, 1230, 680, tm, n=26, amp=16, c1=GOLD, c2="#8a8378", w=3, dur=1.2)
    els += [rect(650, 650, 150, 60, "rgba(159,208,255,.25)", DEN, 2.5, 10, tm + .9, fx="pop"), glow(725, 680, 110, tm + .9, .6, "blue"), lab(725, 760, "EPAS1", tm + 1.1, DEN, 30)]
    els += [ln([(800, 668), (1200, 560), (1440, 560)], tt, DEN, 2.5, "inferred", dur=1.0, curve=True), figure(1520, 720, 300, tt + .6, "#6f93b5"),
            glow(1520, 600, 180, tt + .6, .45, "blue")]
    els += tag(1500, 330, "2014: a Denisovan version", tt + .8, DEN, 26)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def snowpeaks(at=-1):
    pk = [(-40, 520), (120, 420), (230, 380), (360, 300), (470, 360), (600, 280), (730, 340), (860, 250), (990, 330), (1120, 270), (1260, 340), (1400, 290),
          (1540, 350), (1680, 300), (1820, 380), (1820, 640), (-40, 640)]
    out = [poly(pk, "#5b6070", at=at)]
    for (x, y) in ((360, 300), (600, 280), (860, 250), (1120, 270), (1400, 290), (1680, 300)):
        out.append(poly([(x - 60, y + 56), (x, y), (x + 60, y + 50), (x + 26, y + 44), (x - 8, y + 58), (x - 34, y + 46)], "#eef2f7", at=at, op=.9))
    return out


def s30():
    """Dawn on the Tibetan Plateau: snow peaks, a herder walking with two yaks, his breath a small cloud in the cold; behind him a tall faint
    dotted figure walks in step like a shadow, a thin blue thread between them."""
    GY = 650
    els = snowpeaks(-1) + [poly([(-40, GY - 30), (400, GY - 50), (900, GY - 36), (1400, GY - 52), (1820, GY - 30), (1820, 1040), (-40, 1040)], "#5a5236", at=-1, curve=True),
                           poly([(-40, GY + 40), (600, GY + 20), (1200, GY + 36), (1820, GY + 18), (1820, 1040), (-40, 1040)], "#4a4430", at=-1, curve=True)]
    els += yak(1100, GY + 40, 1.0, .3, "#1c1714", face=1) + yak(1330, GY + 30, .9, .4, "#241d18", face=1)
    els += walker(880, GY + 40, 170, .2, "#2a221b", face=1)
    els += [poly(E(940, GY - 118, 22, 12, 12), "#ffffff", at=1.0, curve=True, op=.35), poly(E(966, GY - 128, 16, 9, 12), "#ffffff", at=1.3, curve=True, op=.25)]
    els += body_outline(720, GY + 40, 200, 1.2, DEN, "claimed", 3, "rgba(159,208,255,.05)", q=False)
    els += [ln([(740, GY - 100), (800, GY - 80), (860, GY - 96)], 1.8, DEN, 2, "inferred", dur=.8, curve=True), lab(889, 200, "the roof of the world", .6, BONE, 32)]
    return {"base": "sky", "tod": "dawn", "ground": 1300, "sun": [1500, 330, 26], "ridges": [], "cam": CAM, "els": els}


# ================================================================== chapter 4: the roof of the world
def university(x, y, s, at, c="#cbbca8"):
    """A small university building: a pediment on four columns."""
    P = lambda a, b: (x + a * s, y + b * s)
    els = [poly([P(-70, -90), P(0, -126), P(70, -90)], "#3a3029", c, 2), rect(*P(-66, -92), 132 * s, 12 * s, "#4a3d2f", c, 1.5)]
    els += [rect(*P(-56 + 34 * k, -80), 12 * s, 74 * s, "#5a4a3a", c, 1.2) for k in range(4)]
    els += [rect(*P(-74, -8), 148 * s, 10 * s, "#4a3d2f", c, 1.5)]
    return group(els, at, "pop")


def s31():
    """The Tibetan Plateau under a high, cold sky: snow peaks, a broad grassy valley, a pale cliff with a cave mouth; a small robed figure at
    the mouth holds half a jaw that glows; an altitude bar climbs to 3,280 m; a dashed path to a small university building."""
    ta, tu = T("s31", "three thousand two hundred"), T("s31", "university")
    els = snowpeaks(-1) + [poly([(-40, 600), (500, 586), (1000, 596), (1820, 580), (1820, 1040), (-40, 1040)], "#6e6a44", at=-1, curve=True),
                           poly([(-40, 690), (700, 676), (1300, 690), (1820, 672), (1820, 1040), (-40, 1040)], "#5a5638", at=-1, curve=True)]
    cliff = [(760, 610), (790, 470), (850, 390), (960, 350), (1080, 350), (1190, 380), (1260, 450), (1290, 610)]
    els += [poly(cliff, "#9a8f80", "rgba(255,236,206,.35)", 1.5, -1, curve=True),
            poly([(1080, 350), (1190, 380), (1260, 450), (1290, 610), (1170, 610), (1190, 470)], "#7c7264", at=-1, curve=True, op=.85)]
    els += [ln([(820 + 70 * k, 420 + 8 * (k % 2)), (870 + 70 * k, 440), (900 + 70 * k, 436)], -1, "#6a6054", 2, draw=False, op=.6) for k in range(6)]
    els += [poly([(930, 610), (930, 540), (960, 486), (1010, 470), (1060, 490), (1084, 548), (1086, 610)], "#16110d", "rgba(255,226,190,.3)", 2, -1, curve=True)]
    els += monk(900, 640, 120, .3) + [glow(926, 560, 60, .6, .9, "lamp"), group([half_jaw(926, 572, .14, -1, fx=None)], .6, "pop")]
    els += [lab(1010, 310, "Baishiya Karst Cave", .5, "#fff3dc", 32), lab(160, 200, "the Tibetan Plateau", .8, BONE, 30, "start")]
    AX, Y0, Y1 = 1600, 760, 200
    Ya = lambda m_: Y0 - (Y0 - Y1) * m_ / 3500
    els += [ln([(AX, Y0), (AX, Y1)], .4, BONE, 2.5, draw=False)] + [ln([(AX - 10, Ya(v)), (AX + 10, Ya(v))], .4, BONE, 2, draw=False) for v in (0, 1000, 2000, 3000)]
    els += [lab(AX + 20, Ya(v) + 8, "%s m" % ("{:,}".format(v)), .5, MUTED, 24, "start") for v in (0, 1000, 2000)]
    els += [ln([(AX, Y0), (AX, Ya(3280))], ta, GOLD, 8, dur=1.0), dot(AX, Ya(3280), 12, GOLD, ta + 1.0), lab(AX - 20, Ya(3280) + 8, "3,280 m", ta + 1.0, GOLD, 32, "end")]
    els += [university(300, 560, 1.0, tu), arrow([[870, 600], [620, 520], [390, 520]], tu - .5, BONE, 2.5, "inferred", .8), lab(300, 610, "a university", tu + .3, BONE, 26)]
    return {"base": "sky", "tod": "day", "ground": 1300, "sun": False, "ridges": [], "cam": CAM, "els": els}


def s32():
    """The half jaw drawn large, its two big molars; a crossed-out DNA helix: no DNA; from one molar a chain of coloured beads unspools to
    the right: a protein, its order like a family signature."""
    tn, tp, tb, ts = T("s32", "No DNA", -.2), T("s32", "proteins can outlast"), T("s32", "a chain of tiny beads"), T("s32", "family signature")
    els = [glow(760, 520, 360, .1, .3, "lamp"), half_jaw(760, 660, 1.9, .2)]
    els += helix(160, 230, 420, 230, tn, n=8, amp=16, w=3, dur=.6) + [strike(150, 270, 430, 190, tn + .6), lab(290, 320, "no DNA", tn + .7, RED, 30)]
    els += [lab(760, 760, "the jaw from the cave", .5, BONE, 28)]
    x0 = 1150
    els += [ln([(920, 440), (1010, 360), (x0, 330)], tp, MUTED, 2.5, "inferred", dur=.6, curve=True)]
    els += beads(x0, 330, 10, 52, 17, tb, [PROT[i] for i in SEQ], dt=.08)
    els += [lab(x0 + 234, 270, "a protein", tb + .4, BONE, 30), lab(x0 + 234, 420, "a family signature", ts, GOLD, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s33():
    """Two bead chains, the jaw's and the Denisovans', line up; green lines drop between them bead by bead: a match, 2019. Then a pale crust
    on the jaw glows: at least 160,000 years."""
    tm, ty, tc = T("s33", "matched"), T("s33", "In twenty nineteen"), T("s33", "A crust")
    x0, st = 560, 64
    cols = [PROT[i] for i in SEQ]
    els = beads(x0, 300, 12, st, 19, .3, cols, dt=.05, label_="the jaw") + beads(x0, 420, 12, st, 19, .6, cols, dt=.05, label_="Denisovans", lc=DEN)
    els += [ln([(x0 + st * k, 322), (x0 + st * k, 398)], round(tm + .06 * k, 2), GREEN, 3, dur=.25) for k in range(12)]
    els += tag(1460, 360, "2019: a match", ty, GREEN, 28)
    els += [half_jaw(889, 720, .95, tc - 1.2), poly([(889 - 150, 690), (889 - 40, 676), (889 + 70, 688), (889 + 120, 712), (889 - 120, 716)], "rgba(242,226,170,.75)",
                                                    "#fff6e6", 1.5, tc, curve=True, fx="pop"), glow(889, 700, 150, tc, .6, "lamp"),
            lab(889 + 260, 640, "a crust: at least 160,000 years", tc + .3, GOLD, 30, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s34():
    """The cave floor cut open under the dark rock: stacked layers with their ages; blue DNA helices glow in the layers about 100,000 and
    60,000 years old, a dashed one in a layer perhaps 45,000; 2020: DNA in the dirt."""
    td, t1, t4 = T("s34", "Denisovan DNA turned up"), T("s34", "a hundred thousand"), T("s34", "perhaps")
    GY = 330
    hs = [70, 74, 76, 76, 78, 82]
    els = cave_arch(80, 1700, 130, GY, -1) + strata(80, 1700, GY, hs, -1, dt=0, fx=None)
    ys = [GY + sum(hs[:k]) + hs[k] / 2 for k in range(6)]
    els += [lab(240, ys[1] + 9, "45,000?", t4, MUTED, 26, "end"), lab(240, ys[2] + 9, "60,000", t1 + .6, BONE, 26, "end"),
            lab(240, ys[4] + 9, "100,000", t1, BONE, 26, "end"), lab(240, ys[0] + 9, "younger", .4, MUTED, 24, "end"), lab(240, ys[5] + 9, "older", .4, MUTED, 24, "end")]
    for k, (y, t, sty) in enumerate(((ys[4], t1, "known"), (ys[2], t1 + .6, "known"), (ys[1], t4, "inferred"))):
        for x in (520, 980, 1400):
            if sty == "known":
                els += helix(x - 90, y, x + 90, y, round(t + .1 * (x // 500), 2), n=6, amp=10, c1=DEN, c2=DEN_D, w=3, dur=.6)
                els += [glow(x, y, 70, t, .55, "blue")]
            else:
                els += [ln([(x - 90, y), (x + 90, y)], round(t + .1 * (x // 500), 2), DEN, 3, "claimed", dur=.6)]
    els += tag(1300, 220, "2020: DNA in the dirt", td, DEN, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """A broken rib glows: 48,000 to 32,000 years; then the animals pop in a row as named: a blue sheep, a wild yak, a woolly rhino, and a
    golden eagle with its wings spread."""
    tr_, tb, ts, ty, tw, te = (T("s35", p) for p in ("broken rib", "butchered", "Blue sheep", "Wild yaks", "Woolly rhinos", "Even a golden"))
    GY = 700
    tr_ = min(tr_, .8)
    els = tag(330, 220, "2024", .3, GOLD, 28) + [glow(330, 400, 220, tr_, .45, "lamp"), rib_piece(330, 410, 1.3, tr_)] + tag(330, 520, "48,000 to 32,000 years", tr_ + .6, GOLD, 26)
    els += [ln([(560, GY), (1700, GY)], tb, "#8a7a66", 2, draw=False, op=.6)]
    els += [glow(700, GY - 60, 130, ts, .35, "lamp"), glow(960, GY - 60, 140, ty, .35, "lamp"), glow(1250, GY - 60, 160, tw, .35, "lamp"), glow(1530, 360, 160, te, .35, "lamp")]
    els += bharal(700, GY, 1.15, ts) + [lab(700, GY + 46, "blue sheep", ts + .2, BONE, 28)]
    els += yak(960, GY, 1.0, ty, c="#4c4036") + [lab(960, GY + 46, "wild yak", ty + .2, BONE, 28)]
    els += woolly_rhino(1250, GY, 1.0, tw, c="#6e5e50") + [lab(1250, GY + 46, "woolly rhino", tw + .2, BONE, 28)]
    els += eagle(1530, 360, .75, te, c="#6a5038") + [lab(1530, 470, "golden eagle", te + .2, GOLD, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s36():
    """Two breaths: at sea level 30 oxygen dots, at 3,280 m 20: about a third less. Below, a time axis: the Denisovans on the plateau from
    at least 160,000 years ago; our species up there from about 40,000."""
    tb, tl = T("s36", "every breath"), T("s36", "long before")
    els = cloud_dots(450, 290, 150, 92, 30, tb - .2, seed=12) + [lab(450, 430, "sea level", tb, MUTED, 28)]
    els += cloud_dots(1000, 290, 150, 92, 20, tb + .3, seed=13) + [lab(1000, 430, "3,280 m", tb + .4, "#cfe6ff", 28)]
    els += [lab(1250, 300, "about a third", tb + 1.2, "#cfe6ff", 30, "start"), lab(1250, 340, "less oxygen", tb + 1.2, "#cfe6ff", 30, "start")]
    ax, X = chips_axis(200, 1580, 680, 200000, 0, [(200000, "200,000"), (150000, "150,000"), (100000, "100,000"), (50000, "50,000"), (0, "today")], tl - .8, "years ago")
    els += [ax, band(X(160000), X(32000), 600, 26, DEN, tl - .4, dur=1.4), lab(X(96000), 580, "Denisovans on the plateau", tl, DEN, 28),
            band(X(40000), X(0), 630, 18, GOLD, tl + 1.2, dur=.8), lab(X(20000), 548, "our species", tl + 1.4, GOLD, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== chapter 5: a face from a well
def truss_bridge(x0, x1, deck, at=-1, c="#2a2622", rim="rgba(255,226,190,.35)", piers=(), river_y=640):
    out = [rect(x0, deck - 8, x1 - x0, 16, c, rim, 1.2, 2, at)]
    n = int((x1 - x0) / 70)
    top = deck - 90
    zig = []
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        zig.append((x, deck if k % 2 == 0 else top))
    out += [ln(zig, at, c, 6, draw=False), ln([(x0 + (x1 - x0) / n, top), (x1 - (x1 - x0) / n, top)], at, c, 7, draw=False), ln(zig, at, rim, 1, draw=False, op=.6)]
    for px in piers:
        out.append(rect(px - 22, deck + 8, 44, river_y + 60 - deck, "#3a3430", rim, 1, 3, at))
    return out


def s37():
    """Harbin, 1933, at dusk: a steel railway bridge being built over a wide river, workers small on the deck. Right: an old stone well in
    cross-section; a wrapped skull goes down on a rope and settles at the bottom in the dark."""
    th = T("s37", "he hid it")
    els = [rect(-40, 560, 1000, 480, "#24343e", at=-1), ln([(-40, 560), (960, 560)], -1, "rgba(207,230,255,.4)", 2, draw=False)]
    els += [ln([(60 + 140 * k, 600 + 22 * (k % 3)), (140 + 140 * k, 600 + 22 * (k % 3))], -1, "#9fc6dc", 2, draw=False, op=.4) for k in range(6)]
    els += truss_bridge(-40, 900, 470, -1, piers=(120, 380, 640, 880))
    els += [figure(260 + 90 * k, 462, 40, .3 + .1 * k, "#1c1714") for k in range(3)] + [ln([(560, 462), (560, 300), (660, 300)], .3, "#2a2622", 6, draw=False)]
    els += [lab(160, 220, "Harbin, 1933", .3, BONE, 32, "start")]
    GY = 420
    els += [rect(960, GY, 860, 640, "#3a3026", at=-1), ln([(960, GY), (1820, GY)], -1, "rgba(255,226,190,.4)", 2, draw=False)]
    for k in range(9):
        y = GY + 40 * k
        els += [rect(1230, y, 40, 38, "#6a5d50", "#2a221b", 1.5, 3, -1), rect(1410, y, 40, 38, "#6a5d50", "#2a221b", 1.5, 3, -1)]
    els += [rect(1270, GY, 140, 370, "#0d0a08", at=-1), rect(1210, GY - 50, 60, 50, "#7a6d60", "#2a221b", 1.5, 4, -1), rect(1410, GY - 50, 60, 50, "#7a6d60", "#2a221b", 1.5, 4, -1),
            ln([(1240, GY - 120), (1440, GY - 120)], -1, "#5a4a3a", 6, draw=False), ln([(1250, GY - 120), (1250, GY - 50)], -1, "#5a4a3a", 5, draw=False),
            ln([(1430, GY - 120), (1430, GY - 50)], -1, "#5a4a3a", 5, draw=False)]
    els += [ln([(1340, GY - 120), (1340, 726)], th, "#cbbca8", 2, dur=1.4), group([harbin_skull(1312, 740, .42, -1, fx=None)], th + 1.3, "pop"),
            glow(1340, 740, 70, th + 1.3, .45, "lamp"), lab(1560, 560, "an old well", th + .6, BONE, 30, "start"), figure(1150, GY, 130, th - .5, "#2a221b")]
    return {"base": "sky", "tod": "dusk", "ground": 1300, "sun": [700, 520, 26], "ridges": [], "cam": CAM, "els": els}


def s38():
    """A time line from 1933 to 2018: a dark bar, hidden, about 85 years; an old man and his family near its end; then a lit museum case
    with the skull."""
    to, tm = T("s38", "Decades later"), T("s38", "museum")
    X = lambda yr: round(200 + (yr - 1930) / 90 * 1100, 1)
    els = [axis(200, 1300, 600, [(X(v), str(v)) for v in (1933, 1950, 1975, 2000, 2018)], .2)]
    els += [ln([(X(1933), 560), (X(2018), 560)], .4, "#5a4a3a", 22, dur=1.6), lab(X(1975), 520, "hidden in the well: about 85 years", 1.2, BONE, 30)]
    els += [figure(X(2003), 600 - 30, 120, to, "#9a8a78"), figure(X(2009), 570, 150, to + .2, "#cbbca8"), figure(X(2014), 570, 110, to + .3, "#cbbca8"),
            lab(X(2008), 330, "he told his family", to + .5, MUTED, 26)]
    els += museum_case(1380, 290, 270, 280, tm) + [group([harbin_skull(1450, 470, .55, -1, fx=None)], tm + .3, "pop"), lab(1515, 760, "a museum", tm + .4, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s39():
    """The Harbin skull drawn large in profile: long and low, a heavy brow, a big almost square eye socket, one molar left; a modern skull's
    dashed outline laid over it (higher and rounder); labels pop as named."""
    tl, tb, tw, te = T("s39", "largest"), T("s39", "A brain"), T("s39", "heavy"), T("s39", "eye")
    NX, NY, S_ = 640, 430, 2.9
    els = [glow(1000, 430, 520, .1, .3, "lamp"), harbin_skull(NX, NY, S_, .2)]
    els += [modern_skull(NX, NY, S_, tl, fx="pop"), lab(1090, 760, "a modern skull (dashed)", tl + .3, GOLD, 26)]
    els += [ln([(1190, 300), (1322, 262)], tb, BONE, 1.6, draw=False, op=.8), lab(1335, 272, "a brain about 1.4 litres", tb + .1, BONE, 30, "start"), ln([(NX - 10, NY - 90), (520, 300)], tw, BONE, 1.6, draw=False, op=.8), lab(500, 290, "a heavy brow", tw + .1, BONE, 30, "end"),
            ln([(NX + 30, NY + 30), (520, 560)], te, BONE, 1.6, draw=False, op=.8), lab(500, 580, "a big, almost square eye socket", te + .1, BONE, 28, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s40():
    """A time axis: a gold mark at 146,000 years with an arrow pointing older: at least. A name plate pops: Homo longi, 'Dragon Man', 2021."""
    td, tn = T("s40", "Dating of the bone", .3), T("s40", "Its describers")
    ax, X = chips_axis(200, 1580, 640, 300000, 0, [(300000, "300,000"), (200000, "200,000"), (146000, "146,000"), (100000, "100,000"), (0, "today")], .2, "years ago")
    els = [ax, dot(X(146000), 640, 12, GOLD, td), ln([(X(146000), 640), (X(146000), 520)], td, GOLD, 3, dur=.4),
           arrow([[X(146000), 520], [X(250000), 520]], td + .4, GOLD, 3, "inferred", .8), lab(X(146000) + 20, 490, "at least 146,000 years", td + .3, GOLD, 32, "start")]
    els += [group([rect(560, 180, 660, 190, "#2f261d", "#c9a96e", 3, 10), rect(574, 194, 632, 162, "none", "rgba(201,169,110,.45)", 1.5, 6),
                   lab(890, 270, "Homo longi", -1, "#f2dcae", 52, st="ital", scl=True, halo=False), lab(890, 330, "'Dragon Man', 2021", -1, "#cbbca8", 30, scl=True, halo=False)], tn, "pop")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s41():
    """The skull again at the left, the dense bone around its inner ear glowing; 95 small bead chains fan out to the right; three of them
    light blue: known only from Denisovans. 2025, Beijing."""
    ty, ti, tp, t3 = T("s41", "In twenty twenty-five"), T("s41", "inner"), T("s41", "ninety-five"), T("s41", "three carried")
    NX, NY, S_ = 200, 470, 1.65
    ex, ey = NX + 118 * S_, NY + 22 * S_
    els = [harbin_skull(NX, NY, S_, .2)] + tag(400, 200, "2025: a team in Beijing", ty, DEN, 26)
    els += [glow(ex, ey, 90, ti, .9, "lamp"), circ(ex, ey, 30, "none", GOLD, 4, ti, fx="draw", dur=.5), lab(ex - 20, ey + 150, "around the inner ear", ti + .3, GOLD, 26)]
    els += [ln([(ex + 34, ey - 8), (860, 420)], ti + .4, GOLD, 2, "inferred", dur=.5)]
    G0, GY0 = 880, 230
    blue = {23, 51, 77}
    for k in range(95):
        cx, cy = G0 + 40 * (k % 19), GY0 + 80 * (k // 19)
        t = round(tp + .012 * k, 3)
        els.append(group([ln([(cx - 10, cy), (cx + 10, cy + 10), (cx - 6, cy + 22)], -1, "#8a7a66", 1.5, draw=False, curve=True)] +
                         [circ(cx - 10 + 10 * q, cy + 6 * q, 5, PROT[(k + q) % 5]) for q in range(3)], t, "pop"))
    for j, k in enumerate(sorted(blue)):
        cx, cy = G0 + 40 * (k % 19), GY0 + 80 * (k // 19)
        els += [circ(cx, cy + 10, 26, "rgba(159,208,255,.25)", DEN, 3, round(t3 + .25 * j, 2), fx="pop"), glow(cx, cy + 10, 60, round(t3 + .25 * j, 2), .7, "blue")]
    els += [lab(1260, 690, "95 proteins", tp + .6, BONE, 30)] + tag(1260, 760, "3 known only from Denisovans", t3 + .8, DEN, 26)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s42():
    """Close on the one molar left in the upper jaw, a pale crust of tartar on it; a small loop of DNA rises from the crust and matches a blue
    loop: Denisovan, the mother's line."""
    tt, tl, td = T("s42", "tartar"), T("s42", "a trace of DNA"), T("s42", "Denisovan too")
    MX, MY = 640, 380
    els = [rect(260, 120, 760, 230, "#d8ccb2", "#fff6e6", 2, 30, .2), lab(400, 200, "the upper jaw", .4, "#5a4a3a", 26, halo=False)]
    els += [group([molar_side(MX, MY, 3.0, -1, fx=None)], .3, "pop", tr="rotate(180 %d %d)" % (MX, MY))]
    els += [poly([(MX - 150, MY + 60), (MX - 120, MY + 40), (MX - 60, MY + 52), (MX - 10, MY + 46), (MX - 20, MY + 92), (MX - 90, MY + 104), (MX - 140, MY + 96)],
                  "#d6c47c", "#f2e2a0", 1.5, tt, curve=True, fx="pop"), glow(MX - 80, MY + 74, 90, tt, .6, "lamp"),
            ln([(MX - 160, MY + 80), (380, 640)], tt + .2, BONE, 1.6, draw=False, op=.8), lab(380, 676, "tartar", tt + .3, "#f2e2a0", 30)]
    els += [arrow([[MX - 70, MY + 110], [800, 560], [1000, 520]], tl, GOLD, 2.5, "inferred", .8), circ(1060, 520, 34, "none", GOLD, 6, tl + .6, fx="draw", dur=.6),
            lab(1060, 600, "a trace of DNA", tl + .8, GOLD, 26), lab(1060, 640, "from the mother's line", tl + .9, MUTED, 24)]
    els += [circ(1400, 520, 34, "none", DEN, 6, td - .4, fx="draw", dur=.6), lab(1400, 600, "Denisovan", td - .2, DEN, 28), tick(1230, 520, td, GREEN, 1.2)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s43():
    """The faceless profile of the opening returns at the left; at the right three blue markers and a small loop on a thin thread lead to it,
    and a faint crowd stands beyond: a whole people. If it holds, the Harbin skull settles into the empty head: a face."""
    tn, tt, tw, th = T("s43", "Not everyone"), T("s43", "a thin thread"), T("s43", "a whole people"), T("s43", "if it holds")
    els = [head_outline(600, 300, 1.0, .2, LILAC, "claimed", 3.5, face=1)]
    els += [ln([(1500, 420), (1150, 440), (790, 430)], tt, GOLD, 1.6, "inferred", dur=1.0, curve=True)]
    els += [circ(1240 + 36 * k, 440 - 2 * k, 13, DEN, "#ffffff", 1.2, round(tt + .3 + .15 * k, 2), fx="pop") for k in range(3)] + [circ(1380, 432, 16, "none", GOLD, 4, tt + .8, fx="pop")]
    els += [lab(1320, 380, "three markers, a trace of DNA", tt + .9, BONE, 26)]
    els += ghosts(1180, 1660, 720, 9, tw, dt=.06, op=.35, seed=21, hmin=110, hmax=160) + [lab(1420, 770, "a whole people", tw + .4, MUTED, 26)]
    els += [glow(650, 420, 300, th, .5, "lamp"), harbin_skull(722, 332, 1.1, th, face=1),
            lab(600, 200, "a face, if it holds", th + 1.0, GOLD, 32)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== chapter 6: how big were they?
MH = 200                       # units per metre in the lineups


def leg_glow(x, gy, h, at, side=1):
    """The thigh and shin bones glowing inside a standing figure's leg (figure feet on gy, height h)."""
    xl = x + side * h * .26 * .2
    return [glow(xl, gy - h * .25, round(h * .22), at, .6, "lamp"), ln([(xl, gy - h * .46), (xl, gy - h * .27)], at, "#fff6e6", max(4, h * .02), draw=False),
            ln([(xl, gy - h * .25), (xl, gy - h * .05)], at + .1, "#fff6e6", max(4, h * .018), draw=False)]


def trousers(x, gy, h, at, c="#3f5f7a", e="#9fd0ff"):
    w = h * .26
    return poly([(x - w * .44, gy - h * .44), (x + w * .44, gy - h * .44), (x + w * .32, gy), (x + w * .07, gy), (x, gy - h * .34), (x - w * .07, gy), (x - w * .32, gy)],
                c, e, 1.5, at, fx="pop", op=.75)


def s44():
    """A lineup on a ground line: us, 1.72 m; beside us a dotted giant three metres tall with a question mark ('a giant?'); a dotted claim
    card; in front, the real bones laid out small on a cloth: teeth, a jaw, the skull."""
    to, tb = T("s44", "Online"), T("s44", "certainly big")
    GY = 740
    els = [ln([(160, GY), (960, GY)], .1, "#8c7152", 2, draw=False), figure(380, GY, 1.72 * MH, .3, US), lab(380, GY + 40, "us, 1.72 m", .4, US, 26)]
    els += [glow(700, GY - 300, 300, to, .25, "blue")] + body_outline(700, GY, 3.0 * MH, to, LILAC, "claimed", 3.5) + [lab(700, GY + 40, "a giant?", to + .3, LILAC, 28)]
    els += [rect(1060, 190, 560, 150, "rgba(201,193,238,.06)", LILAC, 2.5, 14, to + .2, style="claimed", fx="pop"), lab(1340, 282, "'Denisovan giants'", to + .4, LILAC, 34)]
    els += [rect(1040, 640, 600, 90, "#3a2c22", "#6a5a48", 1.5, 10, tb - .3)]
    els += [molar_side(1120, 690, .55, tb, roots=False), half_jaw(1300, 712, .42, tb + .2), harbin_skull(1440, 664, .52, tb + .4)]
    els += [lab(1120, 772, "teeth", tb + .2, BONE, 26), lab(1300, 772, "a jaw", tb + .4, BONE, 26), lab(1520, 772, "the skull", tb + .6, BONE, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


SITES = {"denisova": (84.68, 51.4), "baishiya": (102.57, 35.45), "harbin": (126.63, 45.75), "laos": (103.4, 20.2), "penghu": (119.6, 23.4), "png": (145.0, -6.0)}


def s45():
    """A map of East and Southeast Asia: Denisova Cave, the Tibetan cave and Harbin already pinned; then a new gold pin: Cobra Cave, Laos,
    a small molar, about 150,000 years; a dashed line to the Tibetan jaw: the same shape."""
    tm, ts = T("s45", "A child's molar", .2), T("s45", "is shaped like")
    m = Map(62, 148, 8, 56, (90, 140, 1600, 640))
    els = [land_el(m.land(), -1)]
    for k, (key, name, dy) in enumerate((("denisova", "Denisova Cave", -24), ("baishiya", "Tibetan jaw", -24), ("harbin", "Harbin skull", -24))):
        x, y = m.p(*SITES[key])
        els += [{"k": "pin", "x": x, "y": y, "c": DEN, "r": 7, "in": -1}, lab(x, y + dy, name, -1, DEN, 24)]
    lx, ly = m.p(*SITES["laos"])
    bx, by = m.p(*SITES["baishiya"])
    els += [glow(lx, ly, 120, tm, .7, "lamp"), {"k": "pin", "x": lx, "y": ly, "c": GOLD, "r": 9, "in": tm}, lab(lx - 24, ly + 8, "Cobra Cave, Laos", tm + .2, GOLD, 30, "end"),
            molar_side(lx + 90, ly + 40, .5, tm + .4, roots=True), lab(lx + 90, ly + 120, "about 150,000 years", tm + .6, GOLD, 26)]
    els += [ln([(lx + 4, ly - 12), (bx + 4, by + 14)], ts, GOLD, 2.5, "inferred", dur=.8), lab((lx + bx) / 2 + 26, (ly + by) / 2, "same shape", ts + .6, GOLD, 26, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def s46():
    """The Taiwan Strait in cross-section: a fishing boat drags its net along the floor 60 to 120 m down; a dashed line far below today's sea
    marks the Ice Age sea, the floor then dry land with grass; the jaw rises in the net and glows; 2025: Denisovan, male."""
    tf, td, tp = T("s46", "Fishermen dragged"), T("s46", "dry land"), T("s46", "its proteins named it")
    SY, K = 300, 3.0                                   # sea level today and units per metre of depth
    floor = [(80, SY + 60 * K), (420, SY + 70 * K), (760, SY + 112 * K), (1060, SY + 120 * K), (1380, SY + 90 * K), (1700, SY + 62 * K)]
    els = [rect(-40, SY, 1860, 700, "#173342", at=-1), ln([(-40, SY), (1820, SY)], -1, "#9fc6dc", 2.5, draw=False),
           poly(floor + [(1700, 1040), (80, 1040)], "#4a3d2f", "#c9ad85", 1.5, -1, curve=True), rect(-40, SY + 60 * K, 120, 500, "#4a3d2f", at=-1)]
    els += [ln([(140, SY), (140, SY + 120 * K)], -1, MUTED, 2, draw=False)] + [lab(160, SY + d * K + 8, "%d m" % d, -1, MUTED, 24, "start") for d in (0, 60, 120)]
    els += [poly([(400, SY - 34), (640, SY - 34), (610, SY + 14), (430, SY + 14)], "#5a3a32", "#e7c99a", 1.5, .2), rect(470, SY - 84, 90, 50, "#d8d2c6", "#fff6e6", 1.2, 4, .2),
            rect(484, SY - 72, 22, 16, "#3a5568", at=.2), rect(516, SY - 72, 22, 16, "#3a5568", at=.2), ln([(590, SY - 34), (590, SY - 130)], .2, "#cbbca8", 4, draw=False),
            ln([(590, SY - 126), (650, SY - 40)], .2, "#cbbca8", 3, draw=False), glow(520, SY - 70, 60, .2, .5, "lamp"),
            ln([(600, SY - 4), (820, SY + 160), (990, SY + 330)], tf, "#cbbca8", 2, dur=.8, curve=True),
            ln([(560, SY - 4), (780, SY + 170), (940, SY + 342)], tf, "#cbbca8", 2, dur=.8, curve=True),
            poly([(930, SY + 330), (1010, SY + 320), (1040, SY + 352), (990, SY + 372), (930, SY + 360)], "rgba(203,188,168,.25)", "#cbbca8", 1.5, tf + .6, style="inferred", fx="pop")]
    els += [glow(985, SY + 346, 70, tf + 1.0, .9, "lamp"), group([half_jaw(985, SY + 356, .16, -1, fx=None)], tf + 1.0, "pop")]
    els += [ln([(80, SY + 122 * K), (1700, SY + 122 * K)], td, DEN, 2.5, "inferred", dur=1.0), lab(1660, SY + 122 * K + 40, "Ice Age sea level, about 120 m lower", td + .3, DEN, 26, "end")]
    for k in range(16):
        x = 140 + 95 * k
        y = next(y0 + (y1 - y0) * (x - x0) / (x1 - x0) for (x0, y0), (x1, y1) in zip(floor, floor[1:]) if x0 <= x <= x1) if 80 <= x <= 1700 else SY + 60 * K
        els += [ln([(x - 8, y - 2), (x - 12, y - 18)], round(td + .4 + .03 * k, 2), "#8fae6a", 2.5, draw=False), ln([(x, y - 2), (x + 2, y - 22)], round(td + .4 + .03 * k, 2), "#8fae6a", 2.5, draw=False)]
    els += [lab(1250, SY + 76 * K, "then: dry land", td + .8, "#8fae6a", 26)]
    els += tag(985, 230, "2025: Denisovan, male", tp, DEN, 28)
    els += [lab(260, 220, "Taiwan Strait", .3, BONE, 30, "start")]
    return {"base": "sky", "tod": "dusk", "ground": 1300, "sun": False, "ridges": [], "cam": CAM, "els": els}


def s47():
    """A museum drawer with two long bones, a thigh bone and a shin bone, pale and large; a bead chain beside them with one bead turning blue:
    a Denisovan marker, 2026."""
    tl, tm = T("s47", "two leg"), T("s47", "Denisovan marker")
    els = [rect(200, 300, 1000, 400, "#3a2c20", "#8a6a48", 3, 10, .2), rect(220, 320, 960, 360, "#2a2018", at=.2)]
    els += long_bone(300, 420, 1060, 448, 40, tl, "femur") + long_bone(320, 590, 960, 572, 34, tl + .3, "tibia")
    els += [lab(680, 380, "thigh bone", tl + .3, BONE, 28), lab(640, 650, "shin bone", tl + .6, BONE, 28), lab(700, 760, "Penghu Channel, Taiwan", .5, MUTED, 26)]
    cols = [PROT[i] for i in SEQ][:8]
    els += beads(1280, 300, 8, 48, 15, .6, cols, dt=.05)
    els += [circ(1280 + 48 * 5, 300, 16, DEN, "#ffffff", 2, tm, fx="pop"), circ(1280 + 48 * 5, 300, 30, "none", DEN, 3, tm, fx="draw", dur=.5), glow(1280 + 48 * 5, 300, 70, tm, .8, "blue")]
    els += tag(1450, 400, "2026: a Denisovan marker", tm + .3, DEN, 26)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


LX = {"us": 600, "d18": 860, "d19": 1110}


def s48():
    """Three figures to scale on a ground line: us, 1.72 m; then two Denisovan men, 1.8 m and 1.9 m, each with its leg bone glowing inside
    the leg and trousers drawn over it; a tag on the shin: about 45,000 years."""
    tt, t8, t9, tr_ = T("s48", "trousers"), T("s48", "one metre eighty"), T("s48", "and one metre ninety"), T("s48", "Radiocarbon")
    GY = 760
    els = [ln([(400, GY), (1300, GY)], .1, "#8c7152", 2, draw=False), figure(LX["us"], GY, 1.72 * MH, .2, US), lab(LX["us"], GY + 36, "us, 1.72 m", .3, US, 26)]
    for key, hm, t in (("d18", 1.8, .4), ("d19", 1.9, .6)):
        x, h = LX[key], hm * MH
        els += [figure(x, GY, h, t, "#8aa3be")] + leg_glow(x, GY, h, t + .4)
        els.append(trousers(x, GY, h, tt + (.2 if key == "d19" else 0)))
    els += [lab(LX["d18"], GY - 1.9 * MH - 24, "1.8 m", t8, DEN, 32), lab(LX["d19"], GY - 1.9 * MH - 24, "1.9 m", t9, DEN, 32)]
    els += [lab(LX["d19"], GY - 1.9 * MH - 64, "about 45,000 years old", tr_, GOLD, 24)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s49_add():
    """Tall, not giants: a tall man of today joins at the left (2 m) with a dashed line at the height of a tall man; the dotted giant of three
    metres stands at the right with its question mark; a preprint page stamped 'not yet peer reviewed', 'two bones'; a molar, 'chewing'."""
    tg, tm, t2, tb, tc = T("s49", "Giants"), T("s49", "tall man today"), T("s49", "pass two metres"), T("s49", "two bones"), T("s49", "chewing")
    GY = 760
    els = body_outline(1330, GY, 3.0 * MH, tg, LILAC, "claimed", 3) + [lab(1330, GY + 36, "3 m?", tg + .3, LILAC, 26)]
    els += [ln([(380, GY - 1.9 * MH), (1180, GY - 1.9 * MH)], tm, BONE, 1.8, "inferred", dur=.8)]
    els += [figure(330, GY, 2.0 * MH, t2, "#e8d6b8"), lab(330, GY + 36, "today, 2 m", t2 + .2, BONE, 26)]
    els += [preprint(1470, 190, 200, 250, tb - .3), group([rect(1490, 330, 160, 70, "rgba(200,74,58,.10)", "#c84a3a", 3, 8)], tb, "pop", tr="rotate(-8 1570 365)"),
            lab(1570, 480, "not yet peer reviewed", tb + .1, "#e0705e", 24), lab(1570, 520, "two bones", tb + .3, BONE, 26)]
    els += [molar_side(1580, 640, .55, tc, roots=False), lab(1580, 712, "chewing,", tc + .2, GOLD, 24), lab(1580, 740, "not height", tc + .3, GOLD, 24)]
    return els


def s50():
    """The last lineup in warm light: a tall man of today, the two Denisovan men and us, all within the human range; where the giant stood,
    only a faint dotted ring on the ground."""
    tn = T("s50", "Not giants")
    GY = 740
    els = [glow(889, 520, 640, .1, .35, "lamp"), ln([(360, GY), (1500, GY)], .1, "#8c7152", 2, draw=False)]
    for k, (x, hm, c, name) in enumerate(((520, 2.0, "#e8d6b8", "today, 2 m"), (760, 1.9, "#8aa3be", "1.9 m"), (990, 1.8, "#8aa3be", "1.8 m"), (1210, 1.72, US, "us, 1.72 m"))):
        els += [figure(x, GY, hm * MH, .2 + .15 * k, c), lab(x, GY + 36, name, .3 + .15 * k, c if c != US else US, 26)]
    els += [poly(E(1430, GY + 4, 70, 14, 24), "none", LILAC, 2.5, tn - .4, curve=True, style="claimed")]
    els += chip(1430, 640, "not giants", LILAC, tn, 28)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== the weighing
LROWS = [195, 295, 395, 495, 595, 695]


def pic_dna(x, y, at):
    return bone_chip(x - 26, y + 14, .45, at, glow_=False) + helix(x - 2, y, x + 46, y - 4, at, n=4, amp=7, w=2, dur=.4)


def pic_jaws(x, y, at):
    return [half_jaw(x - 16, y + 22, .2, at), half_jaw(x + 30, y + 26, .16, at + .05)]


def pic_skull(x, y, at):
    return [harbin_skull(x - 30, y - 4, .3, at)]


def pic_molar(x, y, at):
    return [molar_side(x, y + 26, .42, at, roots=False)]


def pic_legs(x, y, at):
    return long_bone(x - 50, y - 12, x + 50, y - 8, 9, at, "femur") + long_bone(x - 46, y + 14, x + 44, y + 12, 8, at, "tibia")


def pic_giant(x, y, at):
    return body_outline(x, y + 38, 84, at, LILAC, "claimed", 2, q=False)


def lrow(y, at, pic, text, grade=None, gt=None, gc=None, size=30, h=86, lit=True):
    fill, edge = ("rgba(242,201,142,.08)", "rgba(242,201,142,.3)") if lit else ("rgba(242,201,142,.03)", "rgba(242,201,142,.14)")
    out = [rect(140, y - h / 2, 1500, h, fill, edge, 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE if lit else DIM, size, "start")]
    if lit:
        out += pic(215, y, at + .1)
    if grade:
        out += chip(1180, y, grade, gc, gt, 30, "start")
    return out


ROWS = [("a people known first from its DNA", pic_dna, "Established", "established"),
        ("the jaws from Tibet and Taiwan", pic_jaws, "Strong evidence", "strong"),
        ("the Harbin skull as a Denisovan face", pic_skull, "Strong evidence", "strong"),
        ("the molar from Laos", pic_molar, "Plausible", "plausible"),
        ("tall: about 1.8 to 1.9 m", pic_legs, "Plausible", "plausible"),
        ("giants", pic_giant, "Awaiting evidence", "awaiting")]


def s51():
    """The ledger: six rows, each with a small picture; the first three light as named and their chips pop (Established, Strong evidence,
    Strong evidence); the last three wait, unlit."""
    keys = [("A distinct human group", "Established"), ("The jaws from Tibet", "from their proteins"), ("The Harbin skull", "with a few careful")]
    els = [rect(110, 140, 1560, 610, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    for k, (text, pic, grade, g) in enumerate(ROWS):
        if k < 3:
            els += lrow(LROWS[k], .4 + .1 * k, pic, text, lit=False)
            t1 = T("s51", keys[k][0])
            tg = T("s51", "Strong evidence", k=1 if k == 1 else 2) if k else T("s51", "Established")
            els += lrow(LROWS[k], t1, pic, text, grade, tg, GRADE[g])
        else:
            els += lrow(LROWS[k], .4 + .1 * k, pic, text, lit=False)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s52_add():
    """The camera lower on the ledger: rows four to six light and their chips pop: Plausible, Plausible, Awaiting evidence."""
    keys = [("The tooth from Laos", "Plausible", 1), ("Tall people", "Plausible", 2), ("Giants", "Awaiting evidence", 1)]
    els = []
    for j, k in enumerate((3, 4, 5)):
        text, pic, grade, g = ROWS[k]
        t1 = T("s52", keys[j][0])
        tg = T("s52", keys[j][1], k=keys[j][2])
        els += lrow(LROWS[k], t1, pic, text, grade, tg, GRADE[g])
    return els


def s53():
    """The open questions: the finds pinned on a map of Asia (Denisova Cave, the Tibetan cave, Harbin, Laos, Taiwan) inside a solid outline,
    and a dashed reach to New Guinea, 'the islands?'; two branches, 'how many groups?'; below, a time axis with the youngest bones (the rib,
    48,000 to 32,000; the shin, about 45,000) and a dashed bar for the genes to about 30,000; then 'Open question'."""
    tr_, ti, tg, tv, ty, tn, to, tu = (T("s53", p) for p in ("How far they", "the islands beyond", "How many groups", "vanished", "The youngest bones",
                                                              "the genes hint", "Open question", "into us"))
    m = Map(68, 160, -12, 56, (90, 120, 1600, 470))
    els = [land_el(m.land(), -1)]
    pts = {k: m.p(*v) for k, v in SITES.items()}
    for k, key in enumerate(("denisova", "baishiya", "harbin", "laos", "penghu")):
        els.append({"k": "pin", "x": pts[key][0], "y": pts[key][1], "c": DEN, "r": 7, "in": round(.2 + .1 * k, 2)})
    hull = [pts["denisova"], pts["harbin"], pts["penghu"], pts["laos"], pts["baishiya"]]
    els += [poly(hull, "rgba(159,208,255,.08)", DEN, 2.5, tr_, curve=True, fx="pop"), lab(pts["baishiya"][0] - 30, pts["baishiya"][1] + 50, "the finds", tr_ + .3, DEN, 26, "end")]
    els += [poly([pts["laos"], pts["penghu"], (pts["png"][0] + 40, pts["png"][1] - 10), (pts["png"][0] - 30, pts["png"][1] + 30)], "rgba(159,208,255,.04)", DEN, 2.5, ti,
                 curve=True, style="inferred", fx="pop"), lab(pts["png"][0] + 50, pts["png"][1] + 8, "the islands?", ti + .3, DEN, 26, "start")]
    els += [ln([(1440, 230), (1500, 230)], tg, DEN, 5, dur=.3), ln([(1500, 230), (1580, 180)], tg + .2, DEN, 4, dur=.4), ln([(1500, 230), (1580, 280)], tg + .2, DEN_D, 4, dur=.4),
            ln([(1580, 280), (1620, 300)], tg + .4, DEN_D, 4, "inferred", dur=.3), lab(1540, 340, "how many groups?", tg + .4, DEN, 26)]
    els += [rect(-40, 600, 1860, 460, "#1b1611", at=-1), ln([(-40, 600), (1820, 600)], -1, "rgba(255,236,206,.25)", 1.5, draw=False)]
    ax, X = chips_axis(260, 1400, 720, 60000, 20000, [(60000, "60,000"), (50000, "50,000"), (40000, "40,000"), (30000, "30,000"), (20000, "20,000")], tv, "years ago")
    els += [ax, band(X(48000), X(32000), 632, 22, DEN, ty, dur=.8), lab(X(48000) - 14, 650, "a rib, Tibet", ty + .2, DEN, 24, "end"),
            band(X(45000), X(43000), 668, 22, DEN, ty + .5, dur=.4), lab(X(43000) + 14, 686, "a shin, Taiwan", ty + .6, DEN, 24, "start"),
            ln([(X(32000), 643), (X(30000), 643)], tn, DEN, 6, "inferred", dur=.6), lab(X(30000) - 15, 684, "genes: until about 30,000?", tn + .3, DEN, 24, "start")]
    els += chip(1380, 634, "Open question", GRADE["open"], to, 30, "start")
    els += [figure(1600, 790, 80, tu, US), lab(1600, 700, "into us?", tu + .2, US, 24)]
    return {"base": "map", "cam": CAM, "els": els}


def s54():
    """Three blue dashed boxes (tests not yet done) fill as named: a whole skeleton; ancient DNA from a bone on the islands; a clock over a
    time axis marked 'the last of them'."""
    t1, t2, t3 = T("s54", "A Denisovan skeleton"), T("s54", "Ancient DNA"), T("s54", "a firm date")
    xs = [140, 640, 1140]
    names = ("a whole skeleton", "DNA from the islands", "a date for the last")
    els = []
    for x, t, nm in zip(xs, (t1, t2, t3), names):
        els += [rect(x, 200, 480, 420, "rgba(159,208,255,.05)", BLUE, 2.5, 14, .4 + .15 * xs.index(x), style="inferred", fx="pop"), lab(x + 240, 680, nm, t + .3, BLUE, 28)]
    x = xs[0] + 240
    els += body_outline(x, 590, 340, t1, BONE, "inferred", 2.5, "rgba(245,236,220,.04)", q=False)
    els += [ln([(x, 300), (x, 420)], t1 + .3, BONE, 4, "inferred", dur=.4)] + [ln([(x - 30, 330 + 22 * q), (x + 30, 330 + 22 * q)], round(t1 + .4 + .05 * q, 2), BONE, 3, "inferred", dur=.3) for q in range(4)]
    x = xs[1]
    for k, (cx, cy, rx, ry) in enumerate(((x + 120, 520, 70, 26), (x + 250, 500, 50, 20), (x + 360, 540, 80, 30))):
        els.append(poly(E(cx, cy, rx, ry, 18), "#4a3d2f", "#c9ad85", 1.5, round(t2 + .1 * k, 2), curve=True, fx="pop"))
    els += helix(x + 90, 330, x + 390, 330, t2 + .4, n=10, amp=18, w=3, dur=.8) + [glow(x + 240, 330, 120, t2 + .4, .4, "blue")]
    x = xs[2]
    els += [circ(x + 240, 330, 80, "rgba(245,236,220,.06)", BONE, 3, t3, fx="pop"), ln([(x + 240, 330), (x + 240, 276)], t3 + .2, BONE, 4, draw=False),
            ln([(x + 240, 330), (x + 284, 344)], t3 + .2, BONE, 4, draw=False), ln([(x + 60, 520), (x + 420, 520)], t3 + .3, BONE, 2.5, dur=.5),
            dot(x + 330, 520, 12, GOLD, t3 + .6), lab(x + 330, 570, "the last of them", t3 + .7, GOLD, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s55():
    """Night: a whole human outline drawn only in dashes under the stars; the few known Denisovan pieces glow in their places (a fingertip,
    the skull, a jaw, molars, a rib, a thigh bone and a shin); the rest of the body empty, waiting."""
    X0, GY, H = 889, 790, 640
    s = H / 640
    P = lambda a, b: (X0 + a * s, GY - H + b * s)
    body = [P(-38, 92), P(-52, 108), P(-118, 124), P(-140, 150), P(-152, 290), P(-150, 380), P(-134, 384), P(-124, 300), P(-110, 180), P(-96, 230), P(-92, 330),
            P(-74, 470), P(-66, 630), P(-24, 636), P(-14, 470), P(-4, 360), P(4, 360), P(14, 470), P(24, 636), P(66, 630), P(74, 470), P(92, 330), P(96, 230),
            P(110, 180), P(124, 300), P(134, 384), P(150, 380), P(152, 290), P(140, 150), P(118, 124), P(52, 108), P(38, 92)]
    els = [glow(X0, GY - H / 2, 480, -1, .18, "blue"), circ(*P(0, 50), 50 * s, "rgba(245,236,220,.03)", BONE, 2.5, -1, style="inferred"),
           poly(body, "rgba(245,236,220,.03)", BONE, 2.5, -1, curve=True, style="inferred")]
    hx, hy = P(0, 50)
    pieces = [glow(hx, hy, 80, .4, .5, "lamp"), harbin_skull(hx - 32, hy - 6, .29, .4), half_jaw(hx - 6, hy + 44, .13, .7),
              glow(*P(132, 384), 40, .8, .9, "lamp"), dot(*P(134, 384), 7, GOLD, .8),
              glow(*P(-40, 220), 60, 1.2, .5, "lamp"), rib_piece(P(-30, 220)[0], P(-30, 220)[1], .3, 1.2)]
    pieces += long_bone(*P(44, 380), *P(54, 470), 9, 1.6, "femur") + long_bone(*P(48, 500), *P(52, 600), 8, 1.9, "tibia")
    els += pieces
    return {"base": "dark", "stars": 160, "cam": CAM, "els": els}


# ================================================================== a placeholder (only while a scene is being drawn)
def _todo(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 480, sid, .3, MUTED, 60)]}


# ================================================================== the film: beats (script lines + markers), aliases, the wall
# (chapter, beat, role, the beat's panel, [(line, the phrase that opens the sentence, shot)], extra beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "Inside it was", "s2"), (1, "Nobody had seen", "s3"), (1, "Yet their genes", "s4"), (2, "So who were", "s5")], {}),
    (0, 1, "title", "s5", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "For decades", "s7"), (1, "In {2008", "s8")], {"chapter": "A cave in Siberia"}),
    (1, 1, "collision", "s9", [(1, "Reading DNA", "s10")], {}),
    (1, 2, "reversal", "s11", [(0, "By the end of", "s12")], {}),
    (1, 3, "tag", "s13", [(1, "A molar from", "s14"), (1, "A whole human", "s15")], {}),
    (2, 0, "world", "s16", [], {"chapter": "Two peoples, one girl"}),
    (2, 1, "collision", "s17", [], {}),
    (2, 2, "reversal", "s18", [(0, "Then, in {2018", "s19"), (1, "Her mother", "s20")], {}),
    (2, 3, "tag", "s21", [(0, "Her father had", "s22"), (0, "When these peoples", "s23")], {}),
    (3, 0, "world", "s24", [(1, "How can anyone", "s25")], {"chapter": "Their genes in us"}),
    (3, 1, "collision", "s26", [(0, "And the Denisovan passages", "s27")], {}),
    (3, 2, "reversal", "s28", [(1, "Most Tibetans", "s29")], {}),
    (3, 3, "tag", "s30", [], {}),
    (4, 0, "world", "s31", [], {"chapter": "The roof of the world"}),
    (4, 1, "collision", "s32", [(0, "In {2019", "s33")], {}),
    (4, 2, "reversal", "s34", [(1, "In {2024", "s35")], {}),
    (4, 3, "tag", "s36", [], {}),
    (5, 0, "world", "s37", [(0, "Decades later", "s38")], {"chapter": "A face from a well"}),
    (5, 1, "collision", "s39", [(0, "Dating of the bone", "s40")], {}),
    (5, 2, "reversal", "s41", [(0, "And from the tartar", "s42")], {}),
    (5, 3, "tag", "s43", [], {}),
    (6, 0, "world", "s44", [(1, "A child's molar", "s45"), (1, "Fishermen dragged", "s46")], {"chapter": "How big were they?"}),
    (6, 1, "collision", "s47", [(0, "A longer leg", "s48")], {}),
    (6, 2, "reversal", "s49", [], {}),
    (6, 3, "tag", "s50", [], {}),
    (7, 0, "weigh", "s51", [(1, "The tooth from", "s52")], {"chapter": "The weighing"}),
    (7, 1, "weigh", "s53", [(0, "The youngest bones", "s53b")], {}),
    (7, 2, "test", "s54", [], {}),
    (7, 3, "close", "s55", [], {}),
]

# alias shots: (the panel's shot, the camera on that panel, the additions built when the camera arrives)
ALIASES = {
    "s12": ("s11", CAM, "s12_add"),
    "s49": ("s48", CAM, "s49_add"),
    "s52": ("s51", [1.1, 889, 560], "s52_add"),
    "s53b": ("s53", [1.2, 950, 600], None),          # a push-in on the time line of the open questions (no additions)
}


def film():
    global C
    script = json.load(open(SCRIPT, encoding="utf-8"))
    g = globals()
    order = []
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in order and sid not in ALIASES:
                order.append(sid)
    ids = order + list(ALIASES)
    IDX.clear(); IDX.update({s: i for i, s in enumerate(ids)})
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % IDX[sid])
        beats.append(B(role, IDX[frm], lines, **kw))
    C = Clock(beats)
    shots = [(g[sid]() if sid in g else _todo(sid)) for sid in order] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[IDX[sid]] = IDX[root]
        cams[IDX[sid]] = [z] + list(cam[1:])
        tags[z] = g[fn]() if fn and fn in g else []
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-denisovans", "code": "LF.30", "series": script["series"], "title": script["title"], "case": "other-humans",
          "verdict": "solid", "claim": "Who were the Denisovans, the people first known from a fingertip?", "mood": "awe",
          "hook_text": "Who were the *fingertip* people?", "beats": beats, "shots": shots,
          "sources": "Krause et al. 2010 (doi:10.1038/nature08976) · Reich et al. 2010 (doi:10.1038/nature09710) · "
                     "Meyer et al. 2012 (doi:10.1126/science.1224344) · Slon et al. 2018 (doi:10.1038/s41586-018-0455-x) · "
                     "Huerta-Sanchez et al. 2014 (doi:10.1038/nature13408) · Chen et al. 2019 (doi:10.1038/s41586-019-1139-x) · "
                     "Fu et al. 2025 (doi:10.1126/science.adu9677; doi:10.1016/j.cell.2025.05.040) · "
                     "Tsutaya et al. 2025 (doi:10.1126/science.ads3888) · Kaifu et al. 2026, preprint (doi:10.64898/2026.08.07.743438)",
          "post": "A chip of finger bone the size of a ladybird, from a cave in Siberia, held the DNA of a people nobody knew: the Denisovans. "
                  "Denny's two peoples, the genes in Papua New Guinea and the Philippines, the gene that helps Tibetans at altitude, the jaw "
                  "from the roof of the world, the Harbin skull from a well, the teeth of Laos and Taiwan, the leg bones and the giants "
                  "claim, weighed.",
          "hashtags": ["#Denisovans", "#HumanEvolution", "#AncientDNA", "#Prehistory", "#Archaeology", "#WeighItYourself"],
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
