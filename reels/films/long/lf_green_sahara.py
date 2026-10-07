"""LF.33 · When the Sahara Was Green (16:9 long film, one wall).

The script is films/long/lf-green-sahara/script.json: its lines are read from there, untouched, and only [go:N|t] markers are
added at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s60; s4t, the title, is the intro card
over the panel of s4), drawn while it is said: a hippo surfacing in a green lake under a Saharan cliff, the fishers around it and
the dunes that cover them today, the desert turning green on a map; Lake Mega-Chad beside the Caspian at the same scale, its
shorelines seen from orbit, fossils in a dry lake bed, pollen and a rain gauge ten times fuller, a paler green with one giant
lake, the orbit's slow wobble, a sea breeze the size of a continent, the loop of plants and rain, a crocodile in a desert pool;
Gobero's graves beside a shallow lake, its middens, the lake that fills, empties and fills again, an embrace drawn only as light,
two peoples and their teeth; the swimmers of Wadi Sura, the long wall of the Cave of Beasts, a stencil that was a reptile's foot,
two readings and a gap of thousands of years, painted herds and a giant with a round head; Takarkori in a green valley, the dry
air, typos on two branches, 93 squares in 100, Taforalt eight thousand years earlier, an idea passed hand to hand and milk in a
pot, two lit faces in a crowd; Nabta Playa's playa and ring, its gates to the north and the midsummer sunrise, a cattle chamber
and dragged stones, Stonehenge eighteen centuries later, a star map that drifts and a reply of fifteen hundred years; the rain
belt retreating, mud read like a diary, a cliff here and a ramp there, the end coming later further south, Mega-Chad shrinking
to the Bodele and its dust, herders sooner or later, the move to the highlands, the oases, the south and the Nile, a balance for Egypt's
spark, the Garamantes' town and foggara and the water table that sank; two ledgers, three tests and the buried lake under the
dunes. Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted = claimed. Human remains
are never drawn: the buried are shown only as light.

Facts: the Shorts of 'When the Sahara Was Green' (f16.py: nabta-playa, takarkori, tassili, green-sahara, gobero, wadi-sura,
garamantes, sahara-ledger; rewrite/<id>.json) and 'capsian' (f15.py), and the script's facts_added (Drake & Bristow 2006, Armitage
et al. 2015, deMenocal et al. 2000, deMenocal & Tierney 2012, Tierney et al. 2017, Quade et al. 2018, Claussen et al. 1999, Brito
et al. 2011, Sereno et al. 2008, Stojanowski, Irish & Sereno 2026, Kuper 2013, Honore et al. 2016, Le Quellec 2005 and 2009, Dunne
et al. 2012, Salem et al. 2025, Malville et al. 1998 and 2008, Malville 2015, Wendorf & Schild 1998, Kropelin et al. 2008, Shanahan
et al. 2015, Wright 2017, Brierley et al. 2018, Kuper & Kropelin 2006, Wengrow et al. 2014, Mattingly & Sterry 2013, Sterry,
Mattingly & Wilson 2022).

Round 7, after the 00:20 restart: chapters 2 to 7 (s15 to s60) drawn, and the chapter 1 maps redrawn so their land and tints
never show a clipping edge or spill over the sea.

Engine workaround (as in lf_denisovans.py): the wall only adds elements to a panel on its first visit, at a beat start or a line
start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a tiny unique
tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel
item (kit.js builds them on that step's clock). Build-in times inside a sentence come from a syllable clock (Clock). Elements
cannot fade out: a veil (or a dune) drawn over a part of a panel stands in for a fade.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-green-sahara/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-green-sahara/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-green-sahara RC_FILMS_EPS=/tmp/claude-0/sbx_lf-green-sahara/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-green-sahara/boards python3 films.py long.lf_green_sahara
"""
import json, math, os, random, re
import films
from mural import remix, SENT
import illus as I
from illus import person, arrow, line, glow, label, dot, box, ring, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-green-sahara", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, MUTED, DIM = "#f2c98e", "#e8c35a", "#cbbca8", "#9a8f80"
LAND, LAND_E, SEA_C = "#4a3d2f", "#c9ad85", "#173342"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c86a", "mixed": "#d8c7a8", "open": "#f0b06a", "awaiting": "#c9c1ee",
         "ruled": "#e98a8a"}
# the palette of this film: lake water, grass and leaves, sand, the sandstone of the cliffs, painted ochre
LAKE, LAKE_D, LAKE_L = "#3f7f9c", "#244f63", "#7fb6c8"
GRASS, GRASS_D, LEAF = "#6f8a4c", "#4b6234", "#7d9a5a"
SAND, SAND_D, SAND_L = "#c9a46e", "#9c7a4e", "#e2c48e"
ROCK, ROCK_D, ROCK_L = "#a8693f", "#5e3a26", "#d89a62"
OCHRE_P = "#a8402a"                                         # the red-brown of the paintings
BONEC, BONE_E, BONE_D = "#efe6d2", "#fff6e6", "#c9b99a"     # bone: face, lit edge, shade
FLAT = "#15110d"                                           # the dark ground (for veils)
HIPPO, HIPPO_D, HIPPO_L = "#6e5a63", "#4a3b42", "#a08c96"   # wet hippo skin: body, shade, sheen


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


def gl(x, y, r, at, op=.6, kind="lamp"):
    return glow(round(x, 1), round(y, 1), round(r), round(at, 2), op, kind)


def E(cx, cy, rx, ry, n=36, a0=0, a1=360):
    return ellipse(cx, cy, rx, ry, n, a0, a1)[:-1] if (a1 - a0) >= 360 else ellipse(cx, cy, rx, ry, n, a0, a1)


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
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
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
    out = [gl(x, y - size * .3, size * 1.1, at, .5)] if halo else []
    return out + [lab(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def bracket(x0, x1, y, at, t=None, c=BONE, up=True, size=26, ty=None, style="known"):
    d = -12 if up else 12
    out = [ln([[x0, y + d], [x0, y], [x1, y], [x1, y + d]], at, c, 2, style, dur=.6)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else (y - 14 if not up else y + 34), t, at + .3, c, size))
    return out


def arc_br(x0, x1, y, h, at, t=None, c=BONE, size=28, style="known", ty=None, dur=.9):
    """A curved arrow over a gap (from x0 to x1, peaking h above y) with its words above it."""
    out = [arrow(R([[x0, y], [(x0 + x1) / 2, y - h], [x1, y]]), round(at, 2), c, 3, style, dur)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else y - h - 18, t, at + .4, c, size))
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


def balance(cx, py, L, ang, base_y, at, left=None, right=None, drop=170, pan=200, c=BONE):
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


def figure(x, y, h, at, c="#e8d6b8", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def mix(c, bg="#241c16", t=.5):
    """The colour c faded towards the background bg (t = how much of c is kept): person and group elements ignore opacity."""
    a, b = c.lstrip("#"), bg.lstrip("#")
    ca, cb = [int(a[i:i + 2], 16) for i in (0, 2, 4)], [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(cb[i] + (ca[i] - cb[i]) * t) for i in range(3))


def helix(x0, y0, x1, y1, at, n=16, amp=18, c1=GOLD, c2=BLUE, w=3, dur=1.0, style="known"):
    """A DNA double helix drawn as two crossing waves with rungs (after f16.helix)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    P = lambda t, ph: [round(x0 + ux * L * t + nx * amp * math.sin(t * n + ph), 1), round(y0 + uy * L * t + ny * amp * math.sin(t * n + ph), 1)]
    ts = [k / 40 for k in range(41)]
    out = [{"k": "line", "p": [P(t, 0) for t in ts], "c": c1, "w": w, "curve": True, "in": round(at, 2), "fx": "draw", "dur": dur, "style": style},
           {"k": "line", "p": [P(t, math.pi) for t in ts], "c": c2, "w": w, "curve": True, "in": round(at + .1, 2), "fx": "draw", "dur": dur, "style": style}]
    out += [{"k": "line", "p": [P(t, 0), P(t, math.pi)], "c": "#e9dccb", "w": 1.5, "op": .5, "keepop": True, "in": round(at + dur * .8, 2)} for t in [k / 10 + .05 for k in range(10)]]
    return out


def veil(x, y, w, h, at, op=.82, fill=FLAT, r=10, dur=.6):
    """A dark veil over part of a panel: stands in for a fade-out (elements cannot fade out)."""
    e = rect(x, y, w, h, fill, at=at, r=r, op=op)
    e["dur"] = dur
    return e


# ================================================================== maps
def _clip(ring_, x0, x1, y0, y1):
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
    pts = list(ring_)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not pts:
            break
        pts = cut(pts, inside, inter)
    return pts


class Map:
    """An equirectangular map of a lon/lat box fitted in a frame rectangle (like films.View); land rings are clipped to the box."""
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
        return (round(self.ox + (lon - lon0) * self.k * self.s, 1), round(self.oy + (lat1 - lat) * self.s, 1))

    def km(self, km):
        return km / 111.32 * self.s

    def land(self, pad=8.0, tol=1.4, minpts=4):
        lon0, lon1, lat0, lat1 = self.b
        out = []
        for poly_ in films._topo():
            ring_ = poly_[0]
            xs = [q[0] for q in ring_]
            if max(xs) < lon0 - pad or min(xs) > lon1 + pad:
                continue
            if max(q[1] for q in ring_) < lat0 - pad or min(q[1] for q in ring_) > lat1 + pad:
                continue
            cl = _clip(ring_, lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad)
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


def inset_map(m, x, y, w, h, at=-1, sea="#12202a", landc="#4a3d2f", extra=()):
    """A small map in a rounded window (m: a Map fitted to the window's rectangle), with extra elements inside it."""
    return {"k": "group", "clip": [x, y, w, h, 14], "bg": sea, "in": at, "els": [land_el(m.land(pad=30), -1, landc)] + list(extra)}


# North Africa, schematic outlines (lon, lat)
SAHARA = [(-17, 21), (-16, 24.5), (-13.5, 27.3), (-9.5, 29), (-5, 30.6), (0, 31.6), (5, 32.6), (9, 33), (10.5, 32), (12.5, 31.2), (16, 30.8),
          (20, 30.4), (25, 30.2), (29, 29.6), (32, 28.6), (34.5, 26.5), (35.5, 23.5), (37, 19.5), (35, 16.5), (31, 15.8), (26, 15.4), (21, 15.2),
          (16, 15), (11, 15.2), (6, 15.6), (1, 15.4), (-4, 15.6), (-9, 16), (-13, 16.2), (-16.4, 16.8)]
NILE = [(31.2, 30.6), (31.0, 29.4), (30.9, 28.0), (31.3, 26.8), (32.6, 25.8), (32.9, 24.1), (32.0, 21.9), (30.8, 20.3), (30.4, 19.6), (32.5, 18.0),
        (33.9, 17.8), (32.5, 15.6)]
MEGA = [(12.0, 16.2), (12.6, 17.7), (15.4, 18.5), (18.6, 18.0), (19.6, 16.2), (19.2, 13.6), (17.2, 11.6), (14.6, 10.9), (12.8, 11.9), (11.9, 13.9)]
CHAD = [(13.3, 13.0), (14.0, 13.7), (14.5, 13.4), (14.3, 12.7), (13.7, 12.6)]
CASPIAN = [(46.7, 44.9), (47.6, 45.9), (49.2, 46.6), (51.8, 47.0), (53.2, 46.4), (53.1, 45.3), (51.3, 44.6), (50.3, 44.4), (51.2, 43.0), (52.6, 42.2),
           (52.9, 41.0), (53.0, 40.0), (53.9, 39.0), (54.0, 37.4), (53.0, 36.9), (51.0, 36.8), (49.6, 37.5), (48.9, 38.4), (49.0, 39.5), (49.5, 40.3),
           (48.6, 41.8), (47.6, 42.8), (47.2, 43.8)]


def _scaled(P, k):
    cx, cy = sum(a for a, b in P) / len(P), sum(b for a, b in P) / len(P)
    return [(round(cx + (a - cx) * k, 3), round(cy + (b - cy) * k, 3)) for a, b in P]


MEGA_A = _scaled(MEGA, .814)        # the Short's schematic outline scaled to the c. 360,000 km2 of Armitage et al. 2015 (as in f16.switchoff_m)


# ================================================================== drawings of this film: land, water, plants, animals, people, things
def acacia(x, y, h, at=-1, c="#2f3b22", trunk="#3a2a1c", fx=None, op=None):
    """A flat-topped acacia: a short trunk that forks, and a wide flat crown (h = height to the top of the crown)."""
    w = h * 1.5
    els = [ln([(x, y), (x - h * .04, y - h * .45), (x - h * .3, y - h * .78)], -1, trunk, max(2, h * .07), draw=False, curve=True),
           ln([(x - h * .04, y - h * .45), (x + h * .26, y - h * .8)], -1, trunk, max(2, h * .06), draw=False, curve=True),
           poly([(x - w * .5, y - h * .8), (x - w * .3, y - h * .97), (x - w * .05, y - h), (x + w * .25, y - h * .98), (x + w * .5, y - h * .82),
                 (x + w * .3, y - h * .74), (x - w * .3, y - h * .74)], c, at=-1, curve=True),
           poly([(x - w * .42, y - h * .84), (x - w * .1, y - h * .97), (x + w * .3, y - h * .95), (x + w * .1, y - h * .9)], "rgba(255,226,170,.16)", at=-1, curve=True)]
    return group(els, at, fx, op=op)


def tufts(x0, x1, y, n, at=-1, c="#5f7a3e", h=22, seed=3, op=None):
    """A row of grass tufts on the line y."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * (k + r.uniform(.1, .9)) / n
        hh = h * r.uniform(.6, 1.3)
        out += [ln([(x, y), (x + r.uniform(-4, 4) - hh * .3, y - hh)], -1, c, 2, draw=False, op=op),
                ln([(x, y), (x + r.uniform(-2, 2), y - hh * 1.15)], -1, c, 2, draw=False, op=op),
                ln([(x, y), (x + hh * .32, y - hh * .9)], -1, c, 2, draw=False, op=op)]
    return [group(out, at)] if at != -1 else out


def reeds(x0, x1, y, n, at=-1, c="#2b3820", h=120, seed=5):
    """Tall reeds in the foreground (a dark frame for the lake)."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * k / max(1, n - 1) + r.uniform(-12, 12)
        hh = h * r.uniform(.6, 1.2)
        bend = r.uniform(-.25, .25) * hh
        out.append(ln([(x, y), (x + bend * .3, y - hh * .5), (x + bend, y - hh)], -1, c, r.uniform(3, 6), draw=False, curve=True))
        if k % 3 == 0:
            out.append(poly(E(x + bend, y - hh - 14, 5, 16, 12), "#4a3a22", at=-1))
    return out


def mesas(y, at=-1, c="#5d5470", seed=2, x0=-40, x1=1820, h=70, n=5):
    """Flat-topped hills on a horizon (y), in haze."""
    r = random.Random(seed)
    out, x = [], x0
    while x < x1:
        w = r.uniform(120, 300)
        hh = h * r.uniform(.4, 1.0)
        out.append(poly([(x, y), (x + w * .12, y - hh), (x + w * .2, y - hh * 1.02), (x + w * .78, y - hh * .98), (x + w * .9, y - hh * .9), (x + w, y)], c, at=at))
        x += w * r.uniform(.8, 1.3)
    return out


def cliff(x0, top, base, at=-1, x1=1840, seed=7, shelter=True, lit="#d4935a", face="#b4703f", shade="#7a4429", dark="#4a2a1a"):
    """A sandstone massif filling a panel from x0 to the right: a lit, fluted front, a rounded skyline of buttes, faint bedding,
    dark streaks of desert varnish, a talus at its foot and (shelter) a low rock shelter cut into its base."""
    r = random.Random(seed)
    H = base - top
    front = [(x0 - 10, base + 20), (x0 + 14, base - .14 * H), (x0 + 4, base - .26 * H), (x0 + 30, base - .38 * H), (x0 + 22, base - .5 * H),
             (x0 + 48, base - .63 * H), (x0 + 44, base - .74 * H), (x0 + 70, base - .86 * H), (x0 + 100, top + 14)]
    sky = [(x0 + 130, top), (x0 + 210, top - 8), (x0 + 300, top - 4), (x0 + 340, top + 22), (x0 + 400, top + 18), (x0 + 470, top - 14),
           (x0 + 560, top - 18), (x0 + 600, top + 8), (x1, top + 4)]
    body = front + sky + [(x1, base + 80), (x0 - 10, base + 80)]
    els = [poly(body, face, at=-1),
           poly(front + [(x0 + 130, top), (x0 + 170, top + 40), (x0 + 150, base - .2 * H), (x0 + 120, base + 20)], lit, at=-1),
           poly([(x0 + 300, top - 4), (x0 + 340, top + 22), (x0 + 330, base - .1 * H), (x0 + 270, base)], shade, at=-1, op=.35)]
    for k in range(7):                                               # flutes: soft vertical shade bands down the face
        xx = x0 + 170 + k * (x1 - x0 - 180) / 7 + r.uniform(-20, 20)
        ww = r.uniform(18, 46)
        els.append(poly([(xx, top + 20), (xx + ww, top + 30), (xx + ww * .8, base - 30), (xx - ww * .2, base - 40)], shade, at=-1, op=round(r.uniform(.18, .32), 2)))
    for k in range(5):                                               # desert varnish: dark streaks from the rim
        xx = x0 + 150 + k * (x1 - x0 - 160) / 5 + r.uniform(-20, 20)
        y0 = top + 34
        els.append(poly([(xx, y0), (xx + 14, y0 + 2), (xx + 10, top + r.uniform(.3, .55) * H), (xx + 2, top + r.uniform(.25, .45) * H)], dark, at=-1, op=.3))
    for k in range(5):                                               # faint bedding planes
        yy = top + H * (k + 1) / 6
        pts = [(x0 + 40 + 6 * k, yy)] + [(x0 + 40 + j * (x1 - x0) / 6, yy + r.uniform(-7, 7)) for j in range(1, 7)]
        els.append(ln(pts, -1, dark, 1.6, draw=False, op=.28, curve=True))
    if shelter:                                                      # a low rock shelter: an overhanging lip over a dark recess
        sx, sw, sh = x0 + 190, 300, .26 * H
        els += [poly([(sx - 10, base + 6), (sx + 4, base - sh * .55), (sx + 40, base - sh * .92), (sx + sw * .55, base - sh), (sx + sw - 20, base - sh * .86),
                      (sx + sw, base - sh * .4), (sx + sw + 10, base + 6)], "#26170e", at=-1, curve=True),
                poly([(sx - 30, base - sh * 1.02), (sx + sw * .6, base - sh * 1.14), (sx + sw + 40, base - sh * .94), (sx + sw + 30, base - sh * .82),
                      (sx + sw * .6, base - sh * .98), (sx - 10, base - sh * .9)], lit, at=-1, op=.55, curve=True)]
    els.append(poly([(x0 - 90, base + 40), (x0 - 20, base - 24), (x0 + 120, base - 36), (x0 + 200, base - 10), (x1, base - 4), (x1, base + 80), (x0 - 90, base + 80)],
                    shade, at=-1, op=.9, curve=True))
    for k in range(14):                                              # boulders on the talus
        bx, by = x0 - 60 + r.uniform(0, 420), base - r.uniform(0, 26)
        els.append(poly(E(bx, by, r.uniform(6, 16), r.uniform(4, 9), 10), r.choice([face, shade, dark]), at=-1, op=.9))
    return els


def dunes(y, h, at, lit, shade, base, seed=1, n=5, x0=-60, x1=1840, fx="fill", dur=1.2):
    """A row of dunes on the line y (crests up to h above it): gentle lit windward slopes, steep shaded slip faces, and the sand
    below them down to the bottom of the panel, built as one group that rises from below."""
    r = random.Random(seed)
    els = [rect(x0, y - 4, x1 - x0, 1100 - y, base, at=-1)]
    w = (x1 - x0) / n
    for k in range(n):
        cx = x0 + w * (k + r.uniform(.3, .7))
        ww = w * r.uniform(1.0, 1.5)
        hh = h * r.uniform(.6, 1.0)
        crest = (cx + ww * .12, y - hh)
        els += [poly([(cx - ww * .6, y + 2), (cx - ww * .2, y - hh * .55), crest, (cx + ww * .2, y - hh * .82), (cx + ww * .42, y + 2)], lit, at=-1, curve=True),
                poly([crest, (cx + ww * .2, y - hh * .82), (cx + ww * .42, y + 2), (cx + ww * .16, y + 2)], shade, at=-1, curve=True, op=.85),
                ln([(cx - ww * .2, y - hh * .55), crest], -1, "rgba(255,240,214,.5)", 1.6, draw=False, curve=True)]
    g = group(els, at, fx)
    g["dur"] = dur
    return g


def ripples(cx, cy, at, n=3, rx=150, ry=20, c="#e9f2f8", dt=.5, op=.55, dur=1.2):
    """Rings of ripples spreading on water (ellipses that draw themselves, fainter outwards)."""
    out = []
    for k in range(n):
        e = poly(E(cx, cy, rx * (1 + .5 * k), ry * (1 + .5 * k), 48), "none", c, round(2.4 - .5 * k, 1), at + dt * k, fx="draw", op=round(op - .12 * k, 2), curve=True)
        e["dur"] = dur
        out.append(e)
    return out


def hippo_head(x, y, s, at=-1, face=-1, reflect=True):
    """A hippo surfacing, seen from the side: the top of its head above the water line y, snout towards face (-1 = left):
    the nostril bump on the snout, the raised eye, small round ears, a wet sheen, its reflection broken below (about 340 s long)."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    dome = [P(172, 0), P(178, -12), P(172, -28), P(156, -42), P(136, -42), P(116, -33), P(92, -31), P(70, -40), P(52, -60), P(36, -78), P(14, -82),
            P(-6, -75), P(-26, -63), P(-52, -60), P(-100, -58), P(-132, -46), P(-158, -26), P(-172, -8), P(-174, 0)]
    els = [poly(dome, HIPPO, "#2a2026", 1.6, at=-1, curve=True),
           poly([P(170, -14), P(160, -36), P(136, -38), P(118, -30), P(92, -27), P(110, -14), P(150, -6)], "#b4838a", at=-1, curve=True, op=.6),
           poly([P(150, -40), P(132, -40), P(114, -31), P(90, -29), P(70, -38), P(50, -58), P(34, -76), P(12, -80), P(-8, -72), P(-30, -60),
                 P(-80, -56), P(-30, -54), P(20, -62), P(60, -42), P(120, -34)], HIPPO_L, at=-1, curve=True, op=.6)]
    els.append(poly(E(*P(146, -42), 9 * s, 4.5 * s, 12), "#22161b", at=-1))                 # the nostril
    ex, ey = P(20, -74)
    els += [poly(E(ex, ey, 18 * s, 11 * s, 16), "#7e6a74", at=-1),                          # the eye on its raised socket
            circ(ex + f * 3 * s, ey - 1 * s, 6.5 * s, "#140c10", at=-1), circ(ex + f * 1 * s, ey - 3.5 * s, 2.2 * s, "#ffffff", at=-1, op=.9)]
    for k, (a, hh) in enumerate(((-60, 26), (-78, 22))):                                   # two small round ears
        bx, by = P(a, -60)
        els.append(poly([(bx - 8 * s, by + 4 * s), (bx - 9 * s, by - hh * s * .6), (bx - 2 * s, by - hh * s), (bx + 7 * s, by - hh * s * .7),
                         (bx + 8 * s, by + 4 * s)], HIPPO_D if k else "#7a6670", "#2a2026", 1, at=-1, curve=True))
    els += [ln([P(-150, -26), P(-80, -50), P(-10, -66)], -1, "#f2ecf2", 2.2 * s, draw=False, curve=True, op=.55),
            ln([P(30, -76), P(60, -56)], -1, "#f2ecf2", 1.6 * s, draw=False, op=.45),
            ln([P(-174, 0), P(176, 0)], -1, "#d8eef8", 2.6, draw=False, op=.85)]
    if reflect:
        refl = [(px, y + (y - py) * .5) for px, py in dome]
        els.append(poly(refl, "#3c3644", at=-1, curve=True, op=.42))
        for k in range(5):
            yy = y + 7 + 8 * k
            els.append(ln([(x - 170 * s + 24 * k, yy), (x + 170 * s - 30 * k, yy)], -1, LAKE_L, 2, draw=False, op=.3))
    return [group(els, at, "rise" if at > 0 else None)]


def hippo_side(x, y, s=1.0, at=0, c="#8a7a86", fx="pop"):
    """A hippo standing, side view facing right, feet on y (about 260 s long)."""
    P = lambda a, b: (x + a * s, y + b * s)
    body = [P(-120, -30), P(-126, -70), P(-100, -104), P(-40, -118), P(30, -116), P(76, -104), P(100, -84), P(116, -96), P(150, -98), P(176, -80),
            P(184, -54), P(170, -42), P(140, -44), P(110, -40), P(90, -26), P(60, -22), P(-60, -20)]
    els = [poly(body, c, "rgba(255,236,206,.3)", 1.2, curve=True)]
    for a in (-96, -64, 46, 74):
        els.append(rect(*P(a - 11, -36), 22 * s, 36 * s, c, r=6 * s))
    els += [circ(*P(146, -88), 4 * s, "#1a1215"), poly(E(*P(132, -104), 7 * s, 9 * s, 10), c),
            ln([P(-110, -60), P(-40, -96), P(40, -100)], -1, "#ffffff", 2, draw=False, curve=True, op=.25)]
    return group(els, at, fx)


def croc(x, y, s=1.0, at=0, c="#6f8452", fx="pop", face=1):
    """A crocodile lying flat, side view (about 260 s long), snout towards face."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    body = [P(-130, -4), P(-90, -12), P(-40, -20), P(20, -24), P(60, -20), P(90, -16), P(132, -12), P(140, -6), P(132, -2), P(90, 0), P(40, 4),
            P(-40, 4), P(-90, 2)]
    els = [poly(body, c, "rgba(255,236,206,.3)", 1, curve=True)]
    els += [poly([P(a, -20 + (abs(a) // 60)), P(a + 6, -28 + (abs(a) // 60)), P(a + 12, -20 + (abs(a) // 60))], "#56683e") for a in range(-60, 60, 18)]
    for a in (-30, 40):
        els.append(ln([P(a, 2), P(a - 8, 14), P(a + 6, 16)], -1, c, 7 * s, draw=False))
    els.append(circ(*P(92, -20), 3.5 * s, "#d8c86a"))
    return group(els, at, fx)


def fish(x, y, s=1.0, at=0, c="#cfe6ff", kind="fish", fx="pop", face=1):
    """A fish, side view facing face: kind 'perch' (deep body, spiny fin) or 'catfish' (long, whiskers), else a small fish."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    if kind == "perch":
        body = [P(-80, 0), P(-50, -26), P(0, -38), P(50, -30), P(80, -8), P(84, 0), P(80, 8), P(50, 26), P(0, 34), P(-50, 24)]
        tail = [P(-76, 0), P(-110, -28), P(-104, 0), P(-110, 28)]
        fin = [P(-30, -30), P(-10, -54), P(10, -50), P(30, -34)]
    elif kind == "catfish":
        body = [P(-100, 0), P(-60, -16), P(0, -22), P(60, -20), P(92, -10), P(98, 0), P(92, 10), P(60, 18), P(0, 18), P(-60, 12)]
        tail = [P(-96, 0), P(-124, -18), P(-120, 0), P(-124, 18)]
        fin = [P(-10, -20), P(10, -36), P(26, -22)]
    else:
        body = [P(-30, 0), P(-10, -12), P(20, -10), P(32, 0), P(20, 10), P(-10, 12)]
        tail = [P(-28, 0), P(-46, -12), P(-44, 0), P(-46, 12)]
        fin = [P(-6, -11), P(4, -18), P(12, -10)]
    els = [poly(tail, c, at=-1), poly(fin, c, at=-1, op=.8), poly(body, c, "rgba(255,255,255,.35)", 1, at=-1, curve=True),
           circ(*P(64 if kind != "fish" else 20, -6), 3.5 * s, "#1a1512")]
    if kind == "catfish":
        els += [ln([P(96, 0), P(120, 10), P(132, 26)], -1, c, 1.6, draw=False, curve=True), ln([P(96, 4), P(116, 22), P(118, 40)], -1, c, 1.6, draw=False, curve=True)]
    return group(els, at, fx)


def cow(x, y, s=1.0, at=0, fill="#d8c7ae", op=None, lying=False, flip=False, horns=None, spots=None):
    """A cow in profile (feet on y), facing right (flip: left): a body, legs, a head and horns (after f16.cow); spots: a piebald coat."""
    f = -1 if flip else 1
    X = lambda a: round(x + f * a * s, 1)
    Y = lambda b: round(y + b * s, 1)
    w = max(2.0, 9 * s)
    if lying:
        body = [[X(85 * math.cos(t)), Y(-34 + 30 * math.sin(t))] for t in [2 * math.pi * k / 24 for k in range(24)]]
        head = [[X(56), Y(-50)], [X(84), Y(-86)], [X(104), Y(-84)], [X(118), Y(-64)], [X(104), Y(-56)], [X(80), Y(-40)]]
        e = [{"k": "poly", "p": body, "fill": fill, "c": "none", "w": 0, "in": at, "curve": True},
             {"k": "poly", "p": head, "fill": fill, "c": "none", "w": 0, "in": at},
             {"k": "line", "p": [[X(40), Y(-6)], [X(76), Y(-4)]], "c": fill, "w": w, "in": at},
             {"k": "line", "p": [[X(-84), Y(-44)], [X(-98), Y(-12)]], "c": fill, "w": w * .4, "in": at}]
        hx, hy = 92, -86
    else:
        body = [[X(70 * math.cos(t)), Y(-64 + 28 * math.sin(t))] for t in [2 * math.pi * k / 24 for k in range(24)]]
        head = [[X(50), Y(-80)], [X(80), Y(-102)], [X(100), Y(-96)], [X(108), Y(-74)], [X(92), Y(-66)], [X(62), Y(-52)]]
        e = [{"k": "poly", "p": body, "fill": fill, "c": "none", "w": 0, "in": at, "curve": True},
             {"k": "poly", "p": head, "fill": fill, "c": "none", "w": 0, "in": at}] + \
            [{"k": "line", "p": [[X(a), Y(-50)], [X(a), Y(0)]], "c": fill, "w": w, "in": at} for a in (-50, -34, 38, 54)] + \
            [{"k": "line", "p": [[X(-68), Y(-76)], [X(-82), Y(-30)]], "c": fill, "w": w * .4, "in": at}]
        hx, hy = 84, -100
        if spots:
            e += [{"k": "poly", "p": R(E(X(a), Y(b), rx * s, ry * s, 14)), "fill": spots, "c": "none", "w": 0, "in": at, "curve": True}
                  for a, b, rx, ry in ((-30, -70, 20, 13), (14, -58, 16, 11), (40, -78, 12, 9))]
    if horns == "forward":
        e += [{"k": "line", "p": [[X(hx - 6), Y(hy)], [X(hx + 22), Y(hy - 10)], [X(hx + 46), Y(hy + 18)], [X(hx + 50), Y(hy + 54)]], "c": "#efe6d2", "w": w * .45, "in": at, "curve": True}]
    elif horns == "lyre":
        e += [{"k": "line", "p": [[X(hx - 4), Y(hy)], [X(hx - 22), Y(hy - 20)], [X(hx - 12), Y(hy - 44)]], "c": "#efe6d2", "w": w * .45, "in": at, "curve": True},
              {"k": "line", "p": [[X(hx + 6), Y(hy)], [X(hx + 24), Y(hy - 22)], [X(hx + 16), Y(hy - 46)]], "c": "#efe6d2", "w": w * .45, "in": at, "curve": True}]
    else:
        e += [{"k": "line", "p": [[X(hx - 6), Y(hy)], [X(hx - 16), Y(hy - 18)]], "c": "#efe6d2", "w": w * .45, "in": at},
              {"k": "line", "p": [[X(hx + 6), Y(hy)], [X(hx + 16), Y(hy - 18)]], "c": "#efe6d2", "w": w * .45, "in": at}]
    if op is not None:
        for q in e:
            q.update(op=op, keepop=True)
    return e


def cowg(x, y, s, at, fill="#d8c7ae", flip=False, horns="lyre", spots=None, fx="rise"):
    """A cow as one group (one build-in)."""
    return group(static(cow(x, y, s, 0, fill, flip=flip, horns=horns, spots=spots)), at, fx)


def giraffe(x, y, h, at=-1, c="#2e2a26", face=1, fx=None):
    """A giraffe silhouette (h = height to the top of the head), feet on y, facing face."""
    f = face
    P = lambda a, b: (x + f * a * h, y + b * h)
    els = [poly([P(-.26, -.5), P(-.2, -.6), P(.04, -.63), P(.16, -.62), P(.22, -.56), P(.2, -.47), P(.04, -.45), P(-.2, -.45)], c, at=-1, curve=True),
           poly([P(.1, -.6), P(.18, -.63), P(.31, -.93), P(.27, -.96), P(.2, -.82), P(.08, -.57)], c, at=-1),
           poly([P(.25, -.95), P(.3, -.99), P(.43, -.95), P(.43, -.91), P(.31, -.92)], c, at=-1, curve=True),
           ln([P(.28, -.98), P(.28, -1.03)], -1, c, max(1.2, h * .018), draw=False), ln([P(.31, -.98), P(.32, -1.03)], -1, c, max(1.2, h * .018), draw=False),
           ln([P(-.25, -.5), P(-.31, -.36)], -1, c, max(1, h * .01), draw=False)]
    els += [ln([P(a, -.48), P(a + d, -.24), P(a, 0)], -1, c, max(1.5, h * .022), draw=False) for a, d in ((-.18, .01), (-.12, -.01), (.12, .01), (.17, -.01))]
    return group(els, at, fx)


def antelope(x, y, h, at=-1, c="#3a3029", face=1, fx=None):
    f = face
    P = lambda a, b: (x + f * a * h, y + b * h)
    els = [poly([P(-.4, -.55), P(-.3, -.72), P(.25, -.74), P(.42, -.6), P(.3, -.5), P(-.35, -.48)], c, at=-1, curve=True),
           poly([P(.3, -.7), P(.42, -.95), P(.55, -.92), P(.5, -.82), P(.42, -.62)], c, at=-1),
           ln([P(.46, -.94), P(.36, -1.25), P(.46, -1.4)], -1, c, max(1.2, h * .03), draw=False, curve=True)]
    els += [ln([P(a, -.52), P(a + .03, 0)], -1, c, max(1.2, h * .035), draw=False) for a in (-.32, -.22, .2, .3)]
    return group(els, at, fx)


def fisher(x, y, h, at, c="#2a2018", face=1, harpoon=True, fx="rise"):
    """A person standing in the shallows with a harpoon raised (feet hidden at y)."""
    f = face
    els = [static([figure(x, y, h, 0, c, None)])[0]]
    if harpoon:
        els.append(ln([(x - f * h * .25, y - h * .35), (x + f * h * .55, y - h * 1.15)], -1, "#e8dcc6", max(2, h * .03), draw=False))
        els.append(poly([(x + f * h * .55, y - h * 1.15), (x + f * h * .5, y - h * 1.06), (x + f * h * .61, y - h * 1.08)], "#efe6d2", at=-1))
    return group(els, at, fx)


def swimmer(x, y, s=1.0, at=.3, c="#f0d8b0", fx="pop"):
    """A painted 'swimmer' of Wadi Sura: a round head, a tapered body held flat, arms and legs bent and spread as if swimming."""
    P = lambda a, b: (x + a * s, y + b * s)
    w = 4.6 * s
    els = [circ(*P(31, -9), 8 * s, c),
           poly([P(22, -12), P(24, -2), P(-14, 4), P(-16, -4)], c, curve=True),
           ln([P(20, -10), P(32, -24), P(46, -23)], -1, c, w, draw=False, curve=True),
           ln([P(18, -3), P(29, 9), P(43, 12)], -1, c, w, draw=False, curve=True),
           ln([P(-13, -2), P(-29, -14), P(-45, -10)], -1, c, w, draw=False, curve=True),
           ln([P(-13, 2), P(-28, 13), P(-46, 11)], -1, c, w, draw=False, curve=True)]
    return group(els, at, fx)


def beast(x, y, s=1.0, at=0, c="#e8d6b8", fx="pop"):
    """A headless beast, as painted at Wadi Sura (after f16.beast): a body, legs and a tail, no head."""
    body = [(x - 52 * s, y - 52 * s), (x - 30 * s, y - 66 * s), (x + 10 * s, y - 62 * s), (x + 40 * s, y - 74 * s), (x + 60 * s, y - 70 * s), (x + 62 * s, y - 50 * s),
            (x + 44 * s, y - 34 * s), (x - 40 * s, y - 32 * s)]
    els = [poly(body, c, at=-1, curve=True)] + \
          [ln([(x + a_ * s, y - 38 * s), (x + (a_ + b_) * s, y - 18 * s), (x + (a_ + b_ / 2) * s, y)], -1, c, 6 * s, draw=False) for a_, b_ in ((-36, -8), (-22, 8), (30, -6), (44, 10))] + \
          [ln([(x - 50 * s, y - 50 * s), (x - 70 * s, y - 40 * s), (x - 78 * s, y - 16 * s)], -1, c, 3 * s, draw=False, curve=True),
           ln([(x + 58 * s, y - 70 * s), (x + 70 * s, y - 82 * s)], -1, c, 12 * s, draw=False)]
    return group(els, at, fx)


HAND = [[-50, 90], [-50, -60], [-35, -65], [-25, 20], [-18, -90], [-2, -92], [4, 15], [14, -80], [30, -78], [32, 25], [44, -40], [60, -34], [54, 90]]


def stencil(x, y, s, at, c="#f0d8b0", spray="#a8402a", seed=6, fx="pop"):
    """A hand stencil: the outline of a hand left in a cloud of sprayed red paint."""
    r = random.Random(seed)
    els = [circ(x + r.uniform(-95, 95) * s, y + r.uniform(-115, 115) * s, r.uniform(3, 8) * s, spray, at=-1, op=round(r.uniform(.4, .85), 2)) for _ in range(46)]
    els.append(poly(E(x, y, 92 * s, 112 * s, 24), spray, at=-1, curve=True, op=.35))
    els.append(poly([(x + a * s, y + b * s) for a, b in HAND], c, at=-1))
    return group(els, at, fx)


def roundhead(cx, base, h, c="#d8c7ae", fill="#b0643c", op=1.0, at=.3, fx="pop"):
    """A Round Head figure (after f16.roundhead): a smooth round head, a body, raised arms."""
    hr = h * .15
    body = [(cx - h * .09, base - h * .72), (cx + h * .09, base - h * .72), (cx + h * .12, base - h * .42), (cx + h * .07, base - h * .02),
            (cx + h * .02, base - h * .02), (cx, base - h * .3), (cx - h * .02, base - h * .02), (cx - h * .07, base - h * .02), (cx - h * .12, base - h * .42)]
    arm = lambda sx: ln([(cx + sx * h * .08, base - h * .66), (cx + sx * h * .24, base - h * .78), (cx + sx * h * .3, base - h * .95)], -1, fill, h * .045,
                        draw=False, curve=True)
    els = [arm(-1), arm(1), poly(body, fill, c, 1.5, at=-1, curve=True), circ(cx, base - h * .72 - hr * .9, hr, fill, c, 1.5, at=-1)]
    return group(els, at, fx, op=op if op < 1 else None)


def ufo(x, y, at, c="#c9c1ee", s=1.0):
    """A flying saucer, drawn dotted: the claim, not a thing (after f16.ufo)."""
    return [poly(E(x, y, 90 * s, 22 * s, 36), "none", c, 3, at, style="claimed"),
            poly(ellipse(x, y - 22 * s, 40 * s, 26 * s, 18, 180, 360)[:-1] + [[x + 40 * s, y - 22 * s]], "none", c, 3, at + .2, style="claimed")]


def palm(x, y, h=80, at=0, c="#6f8a4c", trunk="#6a4a30"):
    """A date palm (after f16.palm)."""
    top = (x + h * .08, y - h)
    e = [ln([(x, y), (x + h * .06, y - h * .5), top], -1, trunk, max(3, h * .07), draw=False, curve=True)]
    for k in range(7):
        a = math.pi * (1.05 + .9 * k / 6)
        e.append(ln([top, (top[0] + math.cos(a) * h * .3, top[1] + math.sin(a) * h * .22 - 6), (top[0] + math.cos(a) * h * .48, top[1] + math.sin(a) * h * .1 + 10)],
                    -1, c, max(2, h * .05), draw=False, curve=True))
    return group(e, at, "rise" if at > 0 else None)


def trilithon(x, y, at=0, c="#cbbca8", s=1.0):
    return [rect(x - 38 * s, y - 84 * s, 20 * s, 84 * s, c, r=3, at=at, fx="rise"), rect(x + 18 * s, y - 84 * s, 20 * s, 84 * s, c, r=3, at=at, fx="rise"),
            rect(x - 46 * s, y - 102 * s, 92 * s, 18 * s, c, r=3, at=at + .3, fx="pop")]


def pot(x, y, s, at, c="#9a6a48", e="#d8a878", fx="rise"):
    """A round-bottomed clay pot, its mouth at y."""
    P = lambda a, b: (x + a * s, y + b * s)
    els = [poly([P(-70, 0), P(70, 0), P(78, 20), P(100, 100), P(84, 200), P(30, 236), P(-30, 236), P(-84, 200), P(-100, 100), P(-78, 20)], c, e, 3, curve=True),
           ln([P(-90, 70), P(90, 70)], -1, "#7a4e34", 2, draw=False, style="inferred"), ln([P(-96, 110), P(96, 110)], -1, "#7a4e34", 2, draw=False, style="inferred")]
    return group(els, at, fx)


def harpoon(x, y, L, ang, at, c=BONEC, fx="pop"):
    """A barbed bone harpoon point, L long, at an angle (degrees, 0 = pointing right)."""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    P = lambda t, o: (x + ux * L * t + nx * o, y + uy * L * t + ny * o)
    shaft = [P(0, -7), P(.92, -5), P(1, 0), P(.92, 5), P(0, 7)]
    els = [poly(shaft, c, BONE_E, 1.2)]
    for t in (.25, .45, .65, .82):
        els.append(poly([P(t, -6), P(t - .08, -20), P(t + .03, -6)], c, BONE_E, 1))
    return group(els, at, fx)


def hook(x, y, s, at, c=BONEC, fx="pop"):
    """A bone fish hook (a J)."""
    els = [ln([(x, y - 60 * s), (x, y + 20 * s), (x + 8 * s, y + 38 * s), (x + 30 * s, y + 40 * s), (x + 40 * s, y + 22 * s), (x + 38 * s, y + 6 * s)], -1, c,
              8 * s, draw=False, curve=True),
           poly([(x + 38 * s, y + 6 * s), (x + 30 * s, y - 2 * s), (x + 46 * s, y - 4 * s)], c, at=-1),
           circ(x, y - 64 * s, 6 * s, "none", c, 3 * s, at=-1)]
    return group(els, at, fx)


def molar_top(cx, cy, r, at, fill=BONEC, fx="pop", c=BONE_E):
    """A molar's chewing surface from above: a rounded square with five cusps and a Y-shaped groove (after lf_denisovans)."""
    P = lambda a, b: (cx + a * r, cy + b * r)
    out_ = [P(-1, -.55), P(-.85, -.92), P(-.3, -1.02), P(.35, -1.0), P(.9, -.85), P(1.04, -.2), P(.98, .55), P(.7, .95), P(.1, 1.02), P(-.55, .98),
            P(-.95, .7), P(-1.05, .1)]
    els = [poly(out_, fill, c, 2, curve=True),
           ln([P(-.62, -.18), P(-.05, .02), P(.6, -.12)], -1, BONE_D, 3, draw=False, curve=True),
           ln([P(-.05, .02), P(.02, .62)], -1, BONE_D, 3, draw=False), ln([P(-.05, .02), P(-.1, -.7)], -1, BONE_D, 2.4, draw=False)]
    return group(els, at, fx)


def tooth_side(x, y, h, at, fx="pop", c=BONEC):
    """A molar from the side (crown and two roots), its crown top at y."""
    P = lambda a, b: (x + a * h, y + b * h)
    els = [poly([P(-.4, .02), P(-.44, -.1), P(-.3, -.2), P(-.16, -.12), P(0, -.22), P(.16, -.12), P(.3, -.2), P(.44, -.1), P(.4, .02), P(.38, .42),
                 P(-.38, .42)], c, BONE_E, 1.5, curve=True),
           poly([P(-.34, .4), P(-.04, .4), P(-.1, .82), P(-.24, .9)], "#d8ccb2", BONE_E, 1.2, curve=True),
           poly([P(.04, .4), P(.34, .4), P(.24, .9), P(.1, .82)], "#d8ccb2", BONE_E, 1.2, curve=True)]
    return group(els, at, fx)


def cloud(x, y, w, at, c="#cfd8e0", op=.95, fx=None, dark=False):
    cc = "#7d8794" if dark else c
    els = [poly(E(x, y, w * .5, w * .16, 24), cc, at=-1, curve=True), poly(E(x - w * .22, y - w * .07, w * .22, w * .14, 18), cc, at=-1, curve=True),
           poly(E(x + w * .14, y - w * .1, w * .26, w * .17, 18), cc, at=-1, curve=True)]
    return group(els, at, fx, op=op)


def rain(x0, x1, y0, y1, n, at, c=BLUE, dt=.05, w=2.5, op=.8):
    r = random.Random(int(x0 + y0))
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * (k + r.uniform(.2, .8)) / n
        yy = y0 + r.uniform(0, 30)
        out.append(ln([(x, yy), (x - 10, min(y1, yy + (y1 - y0) * .55))], at + dt * k, c, w, draw=False, op=op))
    return out


def sun(x, y, r, at, kind="sun", op=.85):
    return [gl(x, y, r * 4.2, at, op, "sun"), circ(x, y, r, "#fff1d2", at=at, fx="pop")]


def dune_band(y, amp, at, fill, edge="rgba(255,236,206,.35)", seed=1, x0=-60, x1=1840, dur=1.2, n=7):
    """A ridge of dunes from y down to the bottom of the panel, rising from below ('fill')."""
    r = random.Random(seed)
    pts = [(x0, 1080)]
    for k in range(n + 1):
        xx = x0 + (x1 - x0) * k / n
        pts.append((xx, y - amp * (.4 + .6 * r.random())))
        if k < n:
            pts.append((xx + (x1 - x0) / n * .55, y + amp * .15 * r.random()))
    pts.append((x1, 1080))
    e = poly(pts, fill, edge, 1.5, at, fx="fill", curve=True)
    e["dur"] = dur
    return e


def town(x, y, s, at, c="#a88660", fx="rise"):
    """A small mud-brick oasis town: walls, flat-roofed houses, a gate."""
    els = [rect(x, y - 70 * s, 360 * s, 70 * s, c, "#e8d6b0", 1.5, 3)]
    for k in range(6):
        hh = (34 + 18 * (k % 3)) * s
        els.append(rect(x + (20 + 54 * k) * s, y - 70 * s - hh, 46 * s, hh, "#b8956a" if k % 2 else "#9c7a52", "#e8d6b0", 1, 2))
        els.append(rect(x + (34 + 54 * k) * s, y - 70 * s - hh * .6, 12 * s, 14 * s, "#3a2a1c", at=-1))
    els += [rect(x + 160 * s, y - 44 * s, 40 * s, 44 * s, "#3a2a1c"), ln([(x, y - 70 * s), (x + 360 * s, y - 70 * s)], -1, "#e8d6b0", 1.4, draw=False)]
    return group(els, at, fx)


def mud_pyramid(x, y, w, at, c="#b89266", fx="rise"):
    """A small mud-brick pyramid tomb on a low platform (its base centre at x, y)."""
    h = w * .9
    els = [rect(x - w * .62, y - w * .12, w * 1.24, w * .12, "#a88660", "#e8d6b0", 1.2, 2),
           poly([(x - w / 2, y - w * .12), (x, y - w * .12 - h), (x + w / 2, y - w * .12)], c, "#e8d6b0", 1.4),
           poly([(x, y - w * .12 - h), (x + w / 2, y - w * .12), (x + w * .12, y - w * .12)], "#8a6a46", at=-1, op=.6)]
    return group(els, at, fx)


# ================================================================== cold open: the hippo, the fishers, the sand, the question
HERO_CAM = [1.25, 820, 600]
SHORE = [(-40, 642), (200, 636), (420, 640), (640, 633), (860, 638), (1040, 634), (1180, 644), (1260, 652)]
HX, HY = 780, 716             # the hippo's head on the water line


def _valley(at=-1, lake=True):
    """The green valley of the opening: far mesas in haze, the far shore with grass and acacias, the cliff on the right, the lake."""
    els = []
    els += [gl(360, 470, 640, -1, .42, "sun")]
    els += mesas(606, -1, "#8b8fa6", seed=3, h=58) + mesas(612, -1, "#6f7486", seed=8, h=34)
    els += [poly([(-40, 600), (1300, 596), (1300, 660), (-40, 660)], "#55703a", at=-1)]
    els += tufts(-20, 1180, 640, 60, -1, "#6f8a48", 20, seed=4)
    els += [acacia(140, 628, 74), acacia(470, 622, 92), acacia(980, 626, 66), acacia(1110, 630, 50)]
    els += cliff(1160, 176, 652, -1, seed=11)
    if lake:
        water = [(-40, 1040)] + SHORE + [(1300, 662), (1500, 676), (1840, 690), (1840, 1040)]
        els += [poly(water, LAKE, at=-1),
                poly([(-40, 690)] + SHORE + [(1300, 662), (1500, 676), (1840, 690), (1840, 720)], "#8fb6c4", at=-1, op=.45, curve=True),
                poly([(1170, 662), (1840, 690), (1840, 900), (1300, 860), (1180, 760)], "#6a3e26", at=-1, op=.22, curve=True),
                poly([(-40, 860), (1840, 860), (1840, 1040), (-40, 1040)], LAKE_D, at=-1, op=.55)]
        r = random.Random(9)
        els += [ln([(x, y), (x + r.uniform(30, 80), y)], -1, "#ffe9c4", 2.2, draw=False, op=round(r.uniform(.35, .8), 2))
                for x, y in [(300 + r.uniform(-90, 90), 670 + 14 * k + r.uniform(-4, 4)) for k in range(12)]]
        els += [ln([(x, y), (x + r.uniform(60, 140), y)], -1, "#cfe6ff", 1.6, draw=False, op=.3) for x, y in
                [(r.uniform(40, 1300), r.uniform(690, 990)) for _ in range(26)]]
    return els


def s1():
    """THE HERO: a hippo surfacing in a green lake under a Saharan cliff, in the morning; ripples spread; drawn from the first frame."""
    els = _valley()
    els += ripples(HX, HY + 4, .2, 3, 230, 26, dt=.6, op=.6, dur=1.4)
    els += hippo_head(HX, HY, 1.2, -1)
    els += [circ(HX - 60 + 30 * k, HY - 96 - 14 * (k % 2), 3.5, "#e9f2f8", at=.3 + .1 * k, fx="pop", op=.8) for k in range(4)]
    els += reeds(-30, 260, 1040, 14, -1, "#1f2a18", 230, seed=2) + reeds(1380, 1820, 1040, 16, -1, "#1f2a18", 210, seed=7)
    els += [ln([(980 + 34 * k, 330 + 12 * (k % 2)), (990 + 34 * k, 324 + 12 * (k % 2)), (1000 + 34 * k, 331 + 12 * (k % 2))], -1, "#2a2522", 2.2, draw=False) for k in range(3)]
    els += [lab(330, 336, "about 9,000 years ago", 3.4, BONE, 30, "start")]
    return {"base": "sky", "tod": "day", "ground": 600, "groundc": "#55703a", "sun": [360, 470, 30], "ridges": [], "cam": HERO_CAM, "els": els}


def s2_add():
    """Pull back: the grassland and its animals, and three fishers with bone harpoons in the shallows."""
    tl, tg, tp = T("s2", "a lake"), T("s2", "wide grassland"), T("s2", "people fishing")
    out = [gl(640, 760, 260, tl, .35, "lamp")]
    out += [giraffe(640, 628, 118, tg, "#2b2a24", 1, "rise"), giraffe(700, 630, 96, tg + .2, "#2b2a24", -1, "rise"),
            antelope(820, 632, 30, tg + .4, "#2e2620", 1, "rise"), antelope(870, 634, 26, tg + .5, "#2e2620", -1, "rise"),
            antelope(905, 633, 28, tg + .6, "#2e2620", 1, "rise")]
    for k, (x, h, f) in enumerate(((250, 132, 1), (360, 124, 1), (470, 118, -1))):
        out.append(fisher(x, 790, h, tp + .25 * k, "#1d1712", f))
        out.append(poly(E(x, 790, 46, 8, 20), "none", "#cfe6ff", 2, tp + .25 * k, op=.6, curve=True))
    out += [fish(560, 742, .8, tp + 1.2, "#e9f2f8", "fish", "pop", -1), fish(160, 760, .7, tp + 1.5, "#e9f2f8", "fish", "pop", 1)]
    return out


def s3_add():
    """The same place today: the sky pales, rows of dunes rise over the lake, the grass and the people; only the cliff stands."""
    t0 = T("s3", "Today")
    out = [rect(-40, -20, 1860, 660, "#efd9b2", at=t0, op=.45, dur=1.4), gl(360, 470, 260, t0 + .2, .7, "sun"),
           rect(290, 280, 490, 90, "#d6d0c2", at=t0 + .1, op=.75, r=40), rect(310, 290, 450, 70, "#d6d0c2", at=t0 + .1, op=.9, r=34)]
    out += [dunes(560, 100, t0 + .3, "#e0bf86", "#b8925c", "#d4b07a", seed=3, n=6, dur=1.4),
            dunes(700, 90, t0 + .9, "#d4ac72", "#a8824e", "#c49c64", seed=5, n=5, dur=1.2),
            dunes(850, 80, t0 + 1.5, "#c49a60", "#94703f", "#b48a54", seed=8, n=4, dur=1.1)]
    out.append(lab(535, 338, "the same place today", t0 + .6, "#3a2a1c", 32, halo=False))
    return out


AF = (-30, 48, 2, 37)          # North Africa


def s4():
    """The question on a map: the Sahara, a green wash and a question mark; then three dotted roads out of it, each to a '?'."""
    m = Map(*AF, rect=(90, 130, 1600, 640))
    sah = m.path(SAHARA)
    cx, cy = m.p(16, 24.5)
    ends = [m.p(31.0, 26.2), m.p(15.2, 13.4), m.p(8.9, 18.6)]
    tg, tq = T("s4", "turn green"), T("s4", "where did")
    els = [wide_land(m),
           poly(sah, "#c9a46e", "rgba(255,226,190,.4)", 1.5, -1, op=.62, curve=True),
           ln(m.path(NILE), -1, "#6fb6d6", 3.2, draw=False, curve=True),
           lab(*m.p(2, 27.2), "the Sahara", .4, BONE, 36, st="serif"),
           poly(sah, "#7d9a5a", "none", 0, tg, op=.62, curve=True, dur=1.4)]
    els += qmark(cx - 40, cy + 40, tg + .6, 120)
    mx, my = ends[2]
    els += [poly([(mx - 34, my + 30), (mx - 12, my - 6), (mx + 4, my + 10), (mx + 20, my - 14), (mx + 44, my + 30)], "#6a5a48", "#cbb79a", 1.5, -1)]
    els += [arrow(R([(cx + 50, cy), ((cx + ends[0][0]) / 2, cy - 50), (ends[0][0] - 16, ends[0][1])]), tq + .3, LILAC, 3.5, "claimed", 1.0),
            arrow(R([(cx, cy + 50), (cx + 40, (cy + ends[1][1]) / 2), (ends[1][0], ends[1][1] - 20)]), tq + .6, LILAC, 3.5, "claimed", 1.0),
            arrow(R([(cx - 40, cy + 30), ((cx + mx) / 2 - 20, (cy + my) / 2 - 30), (mx + 30, my - 24)]), tq + .9, LILAC, 3.5, "claimed", .9)]
    els += [lab(ends[0][0] + 30, ends[0][1] + 14, "?", tq + 1.3, LILAC, 54, st="big", fx="pop"),
            lab(ends[1][0], ends[1][1] + 46, "?", tq + 1.6, LILAC, 54, st="big", fx="pop"),
            lab(mx - 56, my + 18, "?", tq + 1.8, LILAC, 54, st="big", fx="pop")]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== chapter 1: a lake as big as a sea
CHAD_M = (2, 32, 6, 22)                     # the Chad basin map (lon0, lon1, lat0, lat1), shared by s5 and its return s49
CHAD_R = (90, 130, 1600, 660)
TIBESTI = [(16.6, 21.4), (17.6, 22.4), (19.0, 22.0), (19.6, 20.8), (18.8, 19.8), (17.4, 19.7), (16.5, 20.4)]
ENNEDI = [(21.6, 17.6), (22.7, 18.2), (23.6, 17.4), (23.0, 16.4), (21.9, 16.6)]
AIR = [(7.8, 19.6), (8.8, 20.1), (9.6, 19.0), (9.3, 17.6), (8.4, 17.1), (7.9, 18.0)]
BODELE = [(16.4, 17.6), (17.4, 18.0), (18.6, 17.5), (18.5, 16.6), (17.3, 16.4), (16.5, 16.8)]


def _casp(m):
    """The Caspian Sea drawn at the same scale as the map m, beside Mega-Chad (centred near 25.4 E, 15.0 N; widths corrected for latitude)."""
    k15 = math.cos(math.radians(15.0))
    return [m.p(25.4 + (a - 50.5) * math.cos(math.radians(42)) / k15, 15.0 + (b - 42)) for a, b in _scaled(CASPIAN, .974)]


def _chad_base(m, at=-1):
    """The Chad basin: land, the Sahara's sand to the north, the Sahel greener to the south, the Tibesti, Ennedi and Air uplands."""
    sahel = [m.p(lo, 8.4) for lo in range(-10, 43, 2)] + [m.p(lo, 15.0 + .5 * math.sin(lo / 3)) for lo in range(42, -11, -2)]
    up = lambda P: poly(m.path(P), "#5e4a38", "#8a7058", 1.2, at, curve=True, op=.75)
    return [land_el(m.land(pad=30), at, "#4a3d2f"), poly(m.path(SAHARA), "#b8945e", "none", 0, at, op=.34, curve=True),
            poly(sahel, "#6f7a44", at=at, op=.26, curve=True), up(TIBESTI), up(ENNEDI), up(AIR)]


def s5():
    """Lake Mega-Chad: the basin today with its small lake; the giant lake fills out from it; the Caspian Sea, at the same scale, slides in."""
    m = Map(*CHAD_M, rect=CHAD_R)
    tL, tM = T("s5", "largest lake"), T("s5", "Lake Mega-Chad")
    mega = m.path(MEGA_A)
    casp = _casp(m)
    cx = sum(p[0] for p in casp) / len(casp)
    els = _chad_base(m)
    lc = m.p(14.0, 13.2)
    els += [poly(m.path(CHAD), LAKE, "#9fd0ff", 1.5, -1),
            ln([(lc[0] - 10, lc[1] + 14), (lc[0] - 90, lc[1] + 120)], .3, MUTED, 1.6, dur=.4), lab(lc[0] - 96, lc[1] + 150, "Lake Chad today", .5, "#cfe6ff", 26, "end")]
    els += [poly(mega, "rgba(63,127,156,.86)", "#9fd0ff", 2, .6, fx="fill", curve=True, dur=1.6), gl(*m.p(15.6, 14.6), 260, .9, .28, "blue")]
    els += [poly(casp, "rgba(159,208,255,.10)", BLUE, 2.5, tL, fx="rise", curve=True, style="inferred", dur=1.0),
            lab(cx, max(p[1] for p in casp) + 42, "Caspian Sea, to scale", tL + .4, BLUE, 26),
            lab(cx, min(p[1] for p in casp) - 22, "largest lake today", tL + .9, MUTED, 24)]
    els += [lab(905, 610, "Lake Mega-Chad", tM, BONE_E, 34, st="serif", fx="pop"),
            {"k": "scale", "x": 150, "y": 770, "w": round(m.km(500), 1), "t": "500 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


def s6():
    """From orbit: a satellite's scan over a dry basin; old shorelines draw themselves one after another as rings of beach ridges."""
    CX, CY = 760, 640
    els = [poly([(-40, 400), (1840, 400), (1840, 1040), (-40, 1040)], "#b48a54", at=-1),
           poly([(-40, 400), (1840, 400), (1840, 470), (-40, 470)], "#d8b884", at=-1, op=.5),
           rect(-40, 330, 1860, 80, "#f0c08a", at=-1, op=.18, r=40)]
    r = random.Random(4)
    els += [ln([(x, y), (x + r.uniform(30, 90), y + r.uniform(-2, 2))], -1, "#8c6a40", 1.4, draw=False, op=.5) for x, y in
            [(r.uniform(-20, 1780), r.uniform(420, 1000)) for _ in range(40)]]
    els += [poly(E(CX, CY, 150, 44, 36), "#9c7a4e", "#7a5a38", 1.5, -1, curve=True)]
    for k, rx in enumerate((210, 300, 400, 500, 610)):
        ry = rx * .3
        e = poly(E(CX, CY + 6 * k, rx, ry, 60), "none", "#f6e2b8", 3.2 - .3 * k, .4 + .35 * k, fx="draw", curve=True, op=round(.85 - .1 * k, 2))
        e["dur"] = .9
        els += [e, poly(E(CX, CY + 6 * k + 5, rx, ry, 60), "none", "#7a5a38", 1.8, .4 + .35 * k, curve=True, op=.45)]
    sx, sy = 1440, 210
    els += [poly([(sx - 6, sy + 20), (CX - 520, CY + 40), (CX + 640, CY + 40)], "rgba(159,208,255,.10)", at=.8, op=.9),
            ln([(sx - 6, sy + 20), (CX - 520, CY + 40)], .8, BLUE, 1.5, "inferred", dur=.5), ln([(sx - 6, sy + 20), (CX + 640, CY + 40)], .8, BLUE, 1.5, "inferred", dur=.5),
            group([rect(sx - 26, sy - 18, 52, 36, "#cbbca8", "#fff6e6", 1.5, 4), rect(sx - 120, sy - 12, 86, 24, "#2f5f7a", "#9fd0ff", 1.5, 2),
                   rect(sx + 34, sy - 12, 86, 24, "#2f5f7a", "#9fd0ff", 1.5, 2), ln([(sx - 34, sy), (sx + 34, sy)], -1, "#cbbca8", 2, draw=False),
                   circ(sx, sy + 22, 8, "#1a1512", "#fff6e6", 1.5)], .2, "pop")]
    els += [lab(CX + 300, CY - 190, "old shorelines", 1.6, BONE_E, 32), lab(sx, sy + 86, "seen from space", 1.9, BLUE, 26)]
    return {"base": "dark", "stars": 70, "cam": CAM, "els": els}


def _fish_bones(x, y, s, at):
    """A fossil fish skeleton: a spine, ribs, a skull and a tail fan, in pale bone."""
    els = [ln([(x - 90 * s, y), (x + 70 * s, y)], -1, BONEC, 4 * s, draw=False),
           poly([(x + 66 * s, y - 22 * s), (x + 110 * s, y - 6 * s), (x + 112 * s, y + 8 * s), (x + 66 * s, y + 22 * s)], BONEC, at=-1, curve=True),
           circ(x + 92 * s, y - 4 * s, 4 * s, "#3a2e24", at=-1),
           poly([(x - 88 * s, y), (x - 124 * s, y - 26 * s), (x - 116 * s, y), (x - 124 * s, y + 26 * s)], "none", BONEC, 2.4, -1)]
    for k in range(9):
        xx = x - 70 * s + k * 16 * s
        hh = (26 - abs(k - 4) * 2.6) * s
        els += [ln([(xx, y), (xx + 6 * s, y - hh)], -1, BONEC, 2, draw=False), ln([(xx, y), (xx + 6 * s, y + hh * .8)], -1, BONEC, 2, draw=False)]
    return group(els, at, "pop")


def _hippo_jaw(x, y, s, at):
    """A hippo's lower jaw in side view: the long bone, molars along it and the great curved tusk at the front."""
    els = [poly([(x - 120 * s, y - 10 * s), (x - 100 * s, y - 34 * s), (x + 60 * s, y - 30 * s), (x + 110 * s, y - 20 * s), (x + 116 * s, y + 10 * s),
                 (x + 60 * s, y + 26 * s), (x - 60 * s, y + 24 * s), (x - 116 * s, y + 18 * s)], BONEC, BONE_E, 1.5, -1, curve=True),
           poly([(x - 118 * s, y - 8 * s), (x - 130 * s, y - 70 * s), (x - 112 * s, y - 64 * s), (x - 100 * s, y - 20 * s)], BONEC, BONE_E, 1.2, -1, curve=True)]
    els += [rect(x - 70 * s + 26 * k * s, y - 44 * s, 20 * s, 16 * s, "#e8dcc2", BONE_D, 1, 3 * s) for k in range(5)]
    els += [ln([(x + 96 * s, y - 14 * s), (x + 132 * s, y - 50 * s), (x + 140 * s, y - 96 * s), (x + 124 * s, y - 128 * s)], -1, "#f6efe0", 14 * s, draw=False, curve=True),
            ln([(x + 96 * s, y - 14 * s), (x + 132 * s, y - 50 * s), (x + 140 * s, y - 96 * s), (x + 124 * s, y - 128 * s)], -1, BONE_D, 2, draw=False, curve=True, op=.6)]
    return group(els, at, "pop")


def _croc_jaw(x, y, s, at):
    """A crocodile's long jaw from the side, a row of conical teeth."""
    els = [poly([(x - 140 * s, y), (x - 120 * s, y - 16 * s), (x + 130 * s, y - 10 * s), (x + 150 * s, y - 2 * s), (x + 130 * s, y + 10 * s), (x - 120 * s, y + 16 * s)],
                BONEC, BONE_E, 1.5, -1, curve=True),
           poly([(x - 150 * s, y + 4 * s), (x - 176 * s, y + 30 * s), (x - 130 * s, y + 20 * s)], BONEC, BONE_E, 1.2, -1)]
    els += [poly([(x - 100 * s + 22 * k * s, y - 12 * s), (x - 92 * s + 22 * k * s, y - 34 * s), (x - 84 * s + 22 * k * s, y - 12 * s)], "#f6efe0", BONE_D, 1, -1) for k in range(10)]
    return group(els, at, "pop")


def _ghost(els):
    """An animal as a faint dashed ghost: outlines only, in the 'inferred' style."""
    out = []
    for e in els:
        e = dict(e)
        if e.get("k") == "group":
            e["els"] = _ghost(e["els"])
        elif e.get("k") in ("poly", "circle"):
            e.update(fill="none", c="#9fd0ff", w=2, style="inferred")
        elif e.get("k") == "line":
            e.update(c="#9fd0ff", style="inferred", w=min(e.get("w", 2), 3))
        elif e.get("k") == "rect":
            e.update(fill="none", c="#9fd0ff", sw=2, style="inferred")
        out.append(e)
    return out


def s7():
    """A dry lake bed cut open: sand over pale lake mud; a fish, a hippo jaw and a crocodile jaw pop in the mud as named; above each the living
    animal swims as a dashed ghost in the old water."""
    tf, th, tc, tw = T("s7", "fish"), T("s7", "hippos"), T("s7", "crocodiles"), T("s7", "water all year")
    GY = 420
    els = [rect(-40, GY, 1860, 620, "#7a6248", at=-1)]
    for k, (y0, c) in enumerate(((GY, "#c9a46e"), (GY + 60, "#d8cdb6"), (GY + 110, "#bfb39a"), (GY + 170, "#e2d8c2"), (GY + 240, "#b0a48a"), (GY + 300, "#d0c4aa"),
                                  (GY + 360, "#a89a7e"))):
        els.append(poly([(-40, y0 + (5 if k else 0))] + [(x, y0 + 6 * math.sin(x / 140 + k)) for x in range(0, 1841, 120)] + [(1840, 1040), (-40, 1040)], c, at=-1, op=.95))
    els += [ln([(-40, GY), (1840, GY)], -1, "rgba(255,226,190,.7)", 2, draw=False),
            lab(150, GY + 44, "sand", .3, "#3a2a1c", 26, "start", halo=False), lab(150, GY + 104, "old lake mud", .5, "#3a2a1c", 26, "start", halo=False)]
    els += [rect(-40, 210, 1860, GY - 210, "rgba(63,127,156,.16)", at=.6, op=.9), ln([(-40, 210), (1840, 210)], .6, "#9fd0ff", 2, "inferred", dur=.8),
            lab(1660, 196, "the old water line", .9, "#9fd0ff", 26, "end")]
    els += [_fish_bones(470, 620, 1.2, tf), group(_ghost([fish(470, 300, 1.2, -1, "#9fd0ff", "perch", None)]), tf + .4, "rise"),
            lab(470, 712, "fish", tf + .2, "#3a2a1c", 28, halo=False)]
    els += [_hippo_jaw(900, 660, 1.15, th), group(_ghost([hippo_side(860, 360, .62, -1, "#9fd0ff", None)]), th + .4, "rise"),
            lab(900, 752, "hippo", th + .2, "#3a2a1c", 28, halo=False)]
    els += [_croc_jaw(1330, 600, 1.1, tc), group(_ghost([croc(1330, 330, 1.2, -1, "#9fd0ff", None)]), tc + .4, "rise"),
            lab(1330, 690, "crocodile", tc + .2, "#3a2a1c", 28, halo=False)]
    els += [gl(900, 300, 520, tw, .3, "blue"), lab(889, 160, "water all year round", tw + .2, BONE_E, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def _pollen_grass(x, y, r, at):
    return group([circ(x, y, r, "#e8d070", "#fff1b8", 2), circ(x, y, r * .62, "none", "#c9b04a", 1.5), circ(x + r * .35, y - r * .3, r * .16, "#7a6a2a", "#fff1b8", 1)], at, "pop")


def _pollen_tree(x, y, r, at):
    """A three-furrowed grain: a rounded triangle with three slits."""
    pts = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    els = [poly(pts, "#d8c070", "#fff1b8", 2, curve=True)]
    els += [ln([(x + .25 * (px - x), y + .25 * (py - y)), (x + .75 * (px - x), y + .75 * (py - y))], -1, "#6a5a2a", 3, draw=False) for px, py in pts]
    return group(els, at, "pop")


def s8():
    """Pollen under a lens, each grain tied to its plant (a grass, an acacia); two rain gauges, today's thin, then ten times fuller."""
    tg, tt, ts, tr = T("s8", "grass"), T("s8", "trees"), T("s8", "only sand"), T("s8", "ten times")
    LX, LY, LR = 470, 400, 190
    els = [circ(LX, LY, LR + 18, "#2a2018", "#cbbca8", 6, .2, fx="pop"), circ(LX, LY, LR, "#5e4a34", at=.2, fx="pop"),
           poly(E(LX - 20, LY + 20, 150, 90, 24), "#7a6248", at=.3, op=.8, curve=True), ln([(LX + 140, LY + 140), (LX + 250, LY + 250)], .2, "#cbbca8", 16, draw=False),
           lab(LX, LY - LR - 30, "pollen in the mud", .5, BONE, 28)]
    els += [_pollen_grass(LX - 70, LY - 10, 46, tg), _pollen_tree(LX + 80, LY + 40, 54, tt)]
    GY = 760
    els += [ln([(80, GY), (900, GY)], .3, "#8c7152", 2, draw=False)]
    els += tufts(160, 360, GY, 6, tg + .3, "#7d9a5a", 46, seed=8)
    els += [ln([(LX - 70, LY + 36), (260, GY - 70)], tg + .2, "#e8d070", 2, "inferred", dur=.5), lab(260, GY + 34, "grass", tg + .4, GREEN, 26)]
    els += [acacia(810, GY, 170, tt + .3, fx="rise"), ln([(LX + 100, LY + 90), (790, GY - 150)], tt + .2, "#e8d070", 2, "inferred", dur=.5),
            lab(810, GY + 34, "trees", tt + .4, GREEN, 26)]
    els += [rect(80, GY + 46, 820, 4, SAND, at=ts, op=.9), lab(490, GY + 40, "where there's sand today", ts + .2, SAND_L, 24)]
    # two rain gauges: today 1 unit, then 10
    for k, (x, n, name) in enumerate(((1170, 1, "today"), (1450, 10, "then"))):
        els += [rect(x - 60, 300, 120, 440, "rgba(245,236,220,.06)", "#cbbca8", 2.5, 10, .4 + .1 * k), lab(x, 790, name, .5 + .1 * k, BONE, 30)]
        els += [ln([(x - 60, 740 - 40 * q), (x - 44, 740 - 40 * q)], -1, "#cbbca8", 1.5, draw=False) for q in range(1, 11)]
    els += [rect(1112, 702, 116, 36, BLUE, at=tr - .2, fx="fill", dur=.5)]
    e = rect(1392, 342, 116, 396, BLUE, at=tr + .3, fx="fill")
    e["dur"] = 1.6
    els += [e, lab(1310, 250, "10 times the rain", tr + 1.6, BLUE, 30), gl(1450, 540, 220, tr + 1.4, .35, "blue")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


NAF = (-18, 38, 8, 37)          # North Africa, for the Sahara-wide maps


def s9():
    """A paler green: the Sahara in pale green-grey, dotted with small lakes and marshes; the other proposed giant lakes only dotted, with
    question marks; Mega-Chad alone solid."""
    m = Map(*NAF, rect=(90, 150, 1600, 640))
    tp, tl, tg = T("s9", "paler green"), T("s9", "scattered lakes"), T("s9", "one true giant")
    sah = m.path(SAHARA)
    els = [wide_land(m), poly(sah, "#c9a46e", "rgba(255,226,190,.4)", 1.5, -1, op=.55, curve=True),
           ln(m.path(NILE), -1, "#6fb6d6", 3.2, draw=False, curve=True),
           poly(sah, "#9aab7e", "none", 0, tp, op=.55, curve=True, dur=1.2), lab(*m.p(4, 33.6), "a paler green?", tp + .5, "#cfe0b0", 34, st="serif")]
    r = random.Random(11)
    pts = []
    while len(pts) < 34:
        lo, la = r.uniform(-14, 33), r.uniform(15.5, 29.5)
        if any(abs(lo - a) < 2.2 and abs(la - b) < 1.6 for a, b in pts):
            continue
        if 11 < lo < 20 and la < 18.8:
            continue
        pts.append((lo, la))
    for k, (lo, la) in enumerate(pts):
        x, y = m.p(lo, la)
        rx = r.uniform(5, 13)
        els.append(poly(E(x, y, rx, rx * r.uniform(.45, .7), 12), "#5d9ab4" if k % 3 else "#6f8f5a", "#9fd0ff" if k % 3 else "none", 1, tl + .04 * k, fx="pop", curve=True))
    for k, (lo0, lo1, la0, la1, name) in enumerate(((11, 16, 24.6, 28.2, None), (0.5, 4.8, 24.8, 27.6, None), (6.2, 10.8, 33.0, 34.6, None))):
        c = [m.p(lo0 + (lo1 - lo0) * (.5 + .5 * math.cos(t)), la0 + (la1 - la0) * (.5 + .5 * math.sin(t))) for t in [2 * math.pi * q / 24 for q in range(24)]]
        cx_, cy_ = m.p((lo0 + lo1) / 2, (la0 + la1) / 2)
        els += [poly(c, "rgba(201,193,238,.06)", LILAC, 2.5, tg + .5 + .3 * k, curve=True, style="claimed"), lab(cx_, cy_ + 12, "?", tg + .7 + .3 * k, LILAC, 40, st="serif")]
    mega = m.path(MEGA_A)
    els += [poly(mega, "rgba(63,127,156,.9)", "#9fd0ff", 2, tg, fx="pop", curve=True), gl(*m.p(15.6, 14.6), 140, tg, .5, "blue"),
            lab(*m.p(15.6, 10.6), "Mega-Chad", tg + .3, "#cfe6ff", 28)]
    return {"base": "map", "cam": CAM, "els": els}


def _earth(x, y, r, tilt, at, solid=True, lit_africa=False, fx="pop"):
    """Earth as a disc with its axis tilted by `tilt` degrees (positive = north pole leaning right), the equator, and (lit_africa) a lit
    patch where North Africa is in summer."""
    t = math.radians(tilt)
    ux, uy = math.sin(t), -math.cos(t)                    # the axis direction (north)
    nx, ny = -uy, ux
    style = "known" if solid else "inferred"
    els = [circ(x, y, r, "#2f5f7a" if solid else "rgba(47,95,122,.15)", "#9fd0ff", 2.5, style=style)]
    if solid:
        els.append(poly([(x - r * .5 * nx + r * .1 * ux - r * .2 * ux, y - r * .5 * ny), (x + r * .3 * nx + r * .35 * ux, y + r * .3 * ny + r * .35 * uy),
                         (x + r * .55 * nx + r * .05 * ux, y + r * .55 * ny + r * .05 * uy), (x + r * .2 * nx - r * .3 * ux, y + r * .2 * ny - r * .3 * uy),
                         (x - r * .3 * nx - r * .2 * ux, y - r * .3 * ny - r * .2 * uy)], "#7d9a5a", at=-1, curve=True, op=.85))
    els += [ln([(x - r * 1.0 * nx, y - r * 1.0 * ny), (x + r * 1.0 * nx, y + r * 1.0 * ny)], -1, "#cfe6ff", 1.5, style, draw=False, op=.7),
            ln([(x - ux * r * 1.35, y - uy * r * 1.35), (x + ux * r * 1.35, y + uy * r * 1.35)], -1, BONE, 3, style, draw=False),
            lab(x + ux * r * 1.55, y + uy * r * 1.55 + 8, "N", -1, BONE, 24)]
    if lit_africa:
        ax, ay = x + ux * r * .42 - nx * r * .25, y + uy * r * .42 - ny * r * .25
        els += [gl(ax, ay, r * .8, -1, .8, "lamp"), poly(E(ax, ay, r * .3, r * .2, 16), "#e8c35a", at=-1, curve=True, op=.85)]
    return group(els, at, fx)


def s10():
    """Why: the Sun and Earth's orbit (shape exaggerated) with its closest point; the slow wobble, about 20,000 years; at the closest point,
    the north tilted away today, towards the Sun 10,000 years ago; summer sunshine over North Africa about 7 percent stronger."""
    tw, tc, tt, ts = T("s10", "slow wobble"), T("s10", "closest to"), T("s10", "Ten thousand years ago"), T("s10", "Summer sunshine")
    SX, SY = 430, 326
    els = [gl(SX, SY, 260, .2, .8, "sun"), circ(SX, SY, 46, "#ffe2a8", "#fff6e6", 2, .2, fx="pop"), lab(SX, SY + 90, "the Sun", .5, GOLD, 26)]
    orb = poly(E(820, SY, 520, 140, 72), "none", "#8c7152", 2.5, .6, curve=True, fx="draw", style="inferred")
    orb["dur"] = 1.2
    els += [orb, circ(300, SY, 14, "#2f5f7a", "#9fd0ff", 2, 1.0, fx="pop"), circ(1340, SY, 10, "#2f5f7a", "#9fd0ff", 2, 1.1, fx="pop")]
    els += [arrow(R([(700, SY - 158), (900, SY - 170), (1100, SY - 156)]), tw, GOLD, 3, "known", 1.0), lab(900, SY - 190, "about 20,000 years", tw + .5, GOLD, 28),
            lab(830, SY + 104, "orbit, shape exaggerated", tw + .2, MUTED, 24)]
    els += [ring(300, SY, 34, tc, AMBER, 3, dur=.5), lab(300, SY - 62, "closest", tc + .3, AMBER, 26)]
    # the two Earths at the closest point: sunlight from the left
    for k in range(3):
        els.append(arrow(R([(120, 520 + 70 * k), (300, 520 + 70 * k)], ), tt, "#ffd28a", 3, "known", .5, curve=False))
    els += [_earth(560, 600, 95, 23, tt + .2, solid=False), lab(560, 760, "today: north away", tt + .4, MUTED, 26)]
    els += [_earth(950, 600, 95, -23, tt + 1.0, solid=True, lit_africa=True), lab(950, 760, "10,000 years ago", tt + 1.2, GOLD, 26)]
    # summer sunshine over North Africa: today 100, then 107
    BX = 1230
    els += [lab(BX, 470, "summer sun, North Africa", ts, BONE, 26, "start"),
            rect(BX, 520, 360, 44, "#9a8f80", at=ts + .3, fx="fill", r=6), lab(BX - 14, 552, "today", ts + .3, MUTED, 24, "end"),
            rect(BX, 600, 385, 44, GOLD, at=ts + .8, fx="fill", r=6), lab(BX - 14, 632, "then", ts + .8, GOLD, 24, "end"),
            lab(BX + 400, 632, "+7%", ts + 1.4, GOLD, 34, "start", st="serif")]
    return {"base": "dark", "stars": 90, "cam": CAM, "els": els}


def s11():
    """A beach on a summer afternoon in section: the sea and the sand, the sun high, a parasol for scale; warm air rises off the sand, cool
    damp air blows in from the sea and rises, a small cloud forms over the land."""
    tw, tr, tc = T("s11", "the sand heats"), T("s11", "warm air rises"), T("s11", "cool, damp air")
    GY = 640
    els = [rect(-40, GY, 860, 400, "#2f6f8c", at=-1), rect(-40, GY, 860, 26, "#4f8fac", at=-1, op=.8),
           poly([(800, GY + 20), (860, GY - 4), (1840, GY - 10), (1840, 1040), (800, 1040)], "#d8b884", at=-1),
           ln([(-40, GY), (820, GY)], -1, "#bfe6f5", 2, draw=False, op=.8)]
    els += [ln([(x, GY + 10), (x + 30, GY + 6), (x + 60, GY + 10)], -1, "#cfe6ff", 1.6, draw=False, op=.5, curve=True) for x in range(40, 760, 110)]
    els += sun(1380, 200, 44, .2)
    els += [ln([(1180, GY - 6), (1196, GY - 190)], -1, "#e8dcc6", 4, draw=False),
            poly([(1100, GY - 180), (1196, GY - 230), (1300, GY - 182), (1200, GY - 196)], "#c84a3a", "#f2c98e", 1.5, -1, curve=True),
            figure(1250, GY - 4, 120, .3, "#2a2018"), lab(1250, GY + 44, "person, 1.7 m", .5, "#3a2a1c", 24, halo=False)]
    els += [gl(1300, GY - 10, 360, tw, .55, "red"), lab(1500, GY + 110, "warm land", tw + .3, "#5a2a1a", 30, halo=False),
            lab(380, GY + 110, "cooler sea", tw + .3, "#cfe6ff", 30)]
    els += [arrow(R([(900 + 150 * k, GY - 30), (910 + 150 * k, GY - 170), (890 + 150 * k, GY - 300)]), tr + .2 * k, "#ff9a6a", 4, "known", .8) for k in range(5)]
    els += [arrow(R([(160, GY - 60 - 26 * k), (520, GY - 70 - 26 * k), (900, GY - 70 - 26 * k)]), tc + .25 * k, BLUE, 4, "known", .9, curve=False) for k in range(2)]
    els += [arrow(R([(900, GY - 130), (980, GY - 200), (1030, GY - 330)]), tc + .8, BLUE, 3, "known", .7)]
    els += [lab(450, GY - 150, "cool, damp air", tc + .3, BLUE, 30), cloud(1060, 300, 300, tc + 1.4, "#e8eef2", .95, "pop")]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "ridges": [], "cam": CAM, "els": els}


MON = (-20, 32, 0, 30)          # West and North Africa, for the monsoon


def s12():
    """The West African monsoon on a map: broad blue arrows from the Atlantic; the rain belt over the Sahel today; then the belt slides north,
    deep into the Sahara, and green spreads behind it, with rain."""
    m = Map(*MON, rect=(90, 130, 1600, 660))
    tm, tt, tr = T("s12", "West African monsoon"), T("s12", "More sun"), T("s12", "pushed deep")
    sah = m.path(SAHARA)
    els = [wide_land(m), poly(sah, "#c9a46e", "rgba(255,226,190,.4)", 1.5, -1, op=.55, curve=True),
           lab(*m.p(-18.2, 4.0), "Atlantic", .3, "#9fd0ff", 28, st="ital")]
    for k, lo in enumerate((-12, -5, 2, 9, 16)):
        els.append(arrow(R([m.p(lo - 3, 0.5), m.p(lo - .5, 6.5), m.p(lo + 1.2, 11.5)]), tm + .2 * k, BLUE, 7, "known", .9))
    els += [lab(*m.p(-8.9, 7.0), "monsoon", tm + .6, BLUE, 30)]
    belt = lambda la, at, op: poly([m.p(lo, la + 1.6 * math.sin(math.radians(lo * 9))) for lo in range(-15, 31, 2)] +
                                   [m.p(lo, la - 3.0 + 1.6 * math.sin(math.radians(lo * 9))) for lo in range(29, -16, -2)], "rgba(159,208,255,.30)", BLUE, 2, at,
                                   fx="pop", curve=True, op=op)
    els += [belt(13.6, tm + 1.0, .9), lab(*m.p(28, 9.2), "rain belt: today", tm + 1.3, "#cfe6ff", 26, "end")]
    green = [m.p(lo, 11.0) for lo in range(-15, 33, 4)] + [m.p(lo, 22.5 + 1.6 * math.sin(lo / 5)) for lo in range(31, -16, -4)]
    els += [poly(green, "#7d9a5a", at=tt + .6, op=.55, curve=True, fx="fill", dur=1.8), belt(22.8, tt + .2, .95),
            lab(*m.p(4, 25.6), "then", tt + .5, BLUE, 34, st="serif")]
    els += rain(m.p(-10, 21)[0], m.p(28, 21)[0], m.p(0, 21)[1], m.p(0, 16)[1], 26, tr, BLUE, .05, 2.5, .8)
    return {"base": "map", "cam": CAM, "els": els}


def s13():
    """Green made more green: on the left bare sand bounces the sunlight back; on the right grass, trees and a pond take it in and breathe
    water up into a cloud that rains back on them; a loop arrow closes round them."""
    tj, td, tb, tg = T("s13", "joined in"), T("s13", "darkened the ground"), T("s13", "breathed water"), T("s13", "Green made")
    GY = 640
    els = [rect(-40, GY, 1860, 400, "#4a3a2c", at=-1), poly([(80, GY), (800, GY), (800, 1040), (80, 1040)], "#e2c48e", at=-1),
           lab(440, GY + 70, "bare sand", .3, "#3a2a1c", 28, halo=False)]
    els += [arrow(R([(260 + 130 * k, 170), (330 + 130 * k, GY - 8)]), .3 + .1 * k, "#ffd28a", 3, "known", .5, curve=False) for k in range(4)]
    els += [arrow(R([(340 + 130 * k, GY - 10), (430 + 130 * k, 230)]), .9 + .1 * k, "#ffd28a", 3, "inferred", .5, curve=False) for k in range(4)]
    els += [lab(440, 160, "sunlight bounces back", .9, "#ffd28a", 26)]
    els += [poly([(940, GY), (1700, GY), (1700, 1040), (940, 1040)], "#3f4f2a", at=td, fx="fill", dur=.8),
            poly(E(1290, GY + 34, 160, 26, 24), "#2f5f7a", "#9fd0ff", 1.5, td + .3, curve=True, fx="pop")]
    els += tufts(960, 1700, GY, 18, td + .2, "#7d9a5a", 30, seed=12)
    els += [acacia(1040, GY, 150, td + .4, fx="rise"), acacia(1560, GY, 130, td + .5, fx="rise"), lab(1320, GY + 110, "plants and lakes", td + .5, "#cfe0b0", 28)]
    els += [arrow(R([(980 + 130 * k, 170), (1050 + 130 * k, GY - 30)]), td + .7 + .1 * k, "#ffd28a", 3, "known", .5, curve=False) for k in range(5)]
    els += [ln([(1040 + 110 * k, GY - 40), (1030 + 110 * k, GY - 90), (1050 + 110 * k, GY - 140), (1036 + 110 * k, GY - 190)], tb + .15 * k, "#cfe6ff", 2.5, "inferred",
               dur=.7, curve=True) for k in range(6)]
    els += [cloud(1300, 230, 380, tb + .9, "#cfd8e0", .95, "pop")] + rain(1150, 1460, 270, 420, 12, tb + 1.6, BLUE, .05, 2.5, .8)
    loop = [(1300 + 330 * math.cos(math.radians(a)), 410 + 230 * math.sin(math.radians(a))) for a in range(200, 520, 20)]
    els += [arrow(R(loop), tg - .3, GREEN, 4, "known", 1.2), lab(1300, 790, "more plants, more rain", tg + .3, GREEN, 30)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": [880, 120, 30], "ridges": [], "cam": CAM, "els": els}


def s14():
    """Dusk in a rocky desert canyon: a dark guelta at the foot of the cliffs, a crocodile basking on a ledge at its edge, its reflection;
    a locator map with Mauritania."""
    tc, tm, ts = T("s14", "A few crocodiles"), T("s14", "Mauritania"), T("s14", "survivors")
    PY = 650
    els = [poly([(-40, 220), (120, 210), (260, 260), (380, 330), (470, 470), (520, 560), (560, PY), (-40, PY + 40)], "#5e3a26", at=-1, curve=True),
           poly([(-40, 300), (180, 290), (330, 360), (430, 480), (470, 600), (-40, 640)], "#7a4a2e", at=-1, curve=True, op=.7),
           poly([(1840, 200), (1560, 220), (1420, 280), (1320, 380), (1260, 500), (1220, PY), (1840, PY + 40)], "#5e3a26", at=-1, curve=True),
           poly([(1840, 280), (1600, 300), (1460, 390), (1380, 520), (1840, 620)], "#8a5634", at=-1, curve=True, op=.6),
           poly([(470, 520), (700, 470), (900, 490), (1100, 460), (1280, 520), (1240, PY), (520, PY)], "#c99a62", at=-1, curve=True, op=.75)]
    els += [poly([(380, PY), (1400, PY), (1460, 760), (1200, 840), (640, 850), (330, 770)], "#1c2a30", "#4a6a76", 1.5, -1, curve=True),
            poly([(420, PY + 6), (1360, PY + 6), (1300, 690), (500, 690)], "#c98a5a", at=-1, op=.18, curve=True),
            poly([(330, PY - 10), (520, PY - 40), (760, PY - 30), (820, PY - 4), (700, PY + 10), (420, PY + 12)], "#6a4430", at=-1, curve=True)]
    els += [croc(600, PY - 22, 1.15, tc, "#6f8452", "rise", 1),
            group([croc(600, PY + 30, 1.15, -1, "#3a4a32", None, 1)], tc + .3, None, tr="translate(0 %d) scale(1 -0.5) translate(0 %d)" % (PY + 30, -(PY + 30)))]
    els += [gl(900, 470, 420, -1, .22, "lamp")]
    m = Map(-18, 12, 10, 28, rect=(1330, 140, 330, 220))
    px, py = m.p(-11.5, 17.3)
    els += [inset_map(m, 1330, 140, 330, 220, .3, extra=[pin(px, py, "", tm, AMBER)]), lab(1495, 395, "Mauritania", tm + .2, AMBER, 26)]
    els += [lab(889, 820 - 30, "guelta: a rock pool", tc + .8, BONE, 28)]
    els += [lab(889, 180, "green Sahara survivors", ts, "#cfe0b0", 30)]
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": [880, 300, 26], "ridges": [], "cam": CAM, "els": els}


# ================================================================== chapter 2: the lake at Gobero
def bgd(x, y):
    """The colour of the 'dark' base at panel point (x, y) (its radial gradient), so that a veil over part of a dark panel does not show."""
    t = min(1.0, math.hypot((x - 889) / 2470, (y - 468) / 3420))
    a, b = (0x3d, 0x2f, 0x22), (0x0d, 0x0b, 0x09)
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def dveil(x, y, w, h, at, op=.98, r=0, dur=.6):
    """A veil the colour of the dark base under it, built of narrow vertical strips that follow the base's gradient (one uniform veil shows
    as a lighter box at its edges): stands in for a fade-out on a 'dark' panel."""
    n = max(1, int(math.ceil(w / 50)))
    sw = w / n
    return group([rect(x + k * sw - .5, y, sw + 1, h, bgd(x + (k + .5) * sw, y + h / 2), at=-1, r=r) for k in range(n)], at, op=op, dur=dur)


def kneeler(x, y, h, at=-1, c="#2a2018", face=-1, fx=None):
    """A person kneeling (h = standing height), facing face, knees on the line y, one arm reaching down with a brush."""
    f = face
    P = lambda a, b: (x + f * a * h, y + b * h)
    els = [circ(*P(.16, -.66), h * .085, c),
           poly([P(-.1, -.56), P(.12, -.58), P(.2, -.36), P(.02, -.24), P(-.14, -.26)], c),
           ln([P(-.1, -.27), P(-.32, -.2), P(-.34, 0)], -1, c, h * .07, draw=False),
           ln([P(-.04, -.25), P(.18, -.04), P(.04, 0)], -1, c, h * .07, draw=False),
           ln([P(.12, -.5), P(.3, -.3), P(.42, -.12)], -1, c, h * .05, draw=False),
           ln([P(.42, -.12), P(.52, -.04)], -1, "#c9a36c", h * .04, draw=False)]
    return group(els, at, fx)


def femur(x0, y0, x1, y1, w, at=-1, c=BONEC, fx=None):
    """A big leg bone from (x0, y0) to (x1, y1): a shaft and two knobbed ends (w = shaft width)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    P = lambda t, o: (x0 + ux * L * t + nx * o, y0 + uy * L * t + ny * o)
    shaft = [P(.1, -w * .5), P(.5, -w * .42), P(.9, -w * .5), P(.9, w * .5), P(.5, w * .42), P(.1, w * .5)]
    els = [poly(shaft, c, BONE_E, 1.2, curve=True),
           poly(E(*P(.06, -w * .45), w * .62, w * .55, 14), c, BONE_E, 1.2, curve=True), poly(E(*P(.07, w * .5), w * .5, w * .45, 14), c, BONE_E, 1.2, curve=True),
           poly(E(*P(.95, -w * .4), w * .55, w * .5, 14), c, BONE_E, 1.2, curve=True), poly(E(*P(.95, w * .42), w * .55, w * .5, 14), c, BONE_E, 1.2, curve=True),
           ln([P(.15, -w * .2), P(.85, -w * .25)], -1, "#ffffff", 2, draw=False, op=.35)]
    return group(els, at, fx)


def flag(x, y, at=-1, c="#e8743a", fx=None):
    """A small marker flag on a thin pole standing on y."""
    return group([ln([(x, y), (x, y - 64)], -1, "#e8dcc6", 2.5, draw=False), poly([(x, y - 64), (x + 30, y - 55), (x, y - 46)], c)], at, fx)


NIGER = [(0.2, 14.9), (1.3, 15.3), (3.6, 15.6), (4.2, 16.9), (4.3, 19.1), (5.8, 19.4), (11.9, 23.5), (13.6, 23.0), (15.9, 21.5), (15.7, 20.0), (15.5, 16.9),
         (13.9, 13.6), (13.5, 13.1), (12.4, 13.1), (10.0, 13.3), (8.5, 13.0), (7.2, 13.1), (4.1, 13.5), (3.6, 11.7), (2.8, 12.2), (2.1, 11.9), (1.0, 13.0),
         (0.3, 13.9)]
GOBERO = (9.52, 17.08)


def s15():
    """Gobero, 2000: dunes in hard light; a field team on a crest, one kneeling with a brush by a huge dinosaur leg bone; a marker flag where the
    first graves showed, drawn only as a soft light; a locator map of Niger with the Air and the Tenere."""
    tp = T("s15", "palaeontologist")
    els = [poly([(-40, 520), (200, 482), (420, 508), (640, 472), (900, 505), (1150, 466), (1400, 500), (1650, 476), (1840, 505), (1840, 600), (-40, 600)],
                "#e2c48e", at=-1, curve=True, op=.9),
           poly([(-40, 760), (300, 690), (700, 620), (1050, 590), (1350, 572), (1600, 590), (1840, 640), (1840, 1040), (-40, 1040)], "#d8b27a", at=-1, curve=True),
           poly([(1420, 574), (1600, 590), (1840, 640), (1840, 760), (1560, 700), (1460, 610)], "#b48a54", at=-1, curve=True, op=.85)]
    r = random.Random(15)
    els += [ln([(x, y), (x + r.uniform(40, 110), y - r.uniform(2, 8))], -1, "#b8925c", 1.6, draw=False, op=.5) for x, y in
            [(r.uniform(0, 1700), r.uniform(700, 980)) for _ in range(26)]]
    # the dinosaur bone, half out of the sand, a kneeling digger with a brush, two more of the team
    els += [femur(960, 642, 1170, 590, 32, -1),
            poly([(930, 668), (1010, 632), (1090, 616), (1170, 612), (1220, 622), (1236, 664)], "#d8b27a", at=-1, curve=True),
            kneeler(1232, 604, 176, -1, "#2a2018", -1), figure(1330, 588, 182, -1, "#2a2018", None), figure(1430, 594, 172, -1, "#3a2a1c", None),
            ln([(1430 + 26, 594 - 100), (1430 + 60, 594 - 56)], -1, "#3a2a1c", 6, draw=False)]
    # where the first human graves showed: no remains drawn, only a marker flag and a soft light in the sand
    els += [flag(640, 634, -1), gl(628, 640, 110, .6, .75, "lamp"), gl(598, 650, 56, .9, .6, "lamp")]
    m = Map(3, 15, 13, 23, rect=(100, 140, 380, 270))
    gx, gy = m.p(*GOBERO)
    ax, ay = m.p(8.7, 18.6)
    tx, ty = m.p(11.9, 18.4)
    els += [inset_map(m, 100, 140, 380, 270, -1, extra=[poly(m.path(NIGER), "rgba(201,164,110,.16)", "#cbbca8", 1.5, -1, style="inferred"),
                                                        poly(m.path(AIR), "#5e4a38", "#8a7058", 1.2, -1, curve=True),
                                                        lab(ax, ay + 8, "Aïr", -1, "#e8dcc6", 24), lab(tx, ty + 8, "Ténéré", -1, "#e8dcc6", 24, "start"),
                                                        pin(gx, gy, "", .5, GOLD)])]
    els += [lab(290, 458, "Gobero, Niger, 2000", .7, BONE_E, 32, st="serif"), lab(1070, 716, "a dinosaur bone", tp, "#4a3220", 26, halo=False)]
    return {"base": "sky", "tod": "day", "ground": 600, "groundc": "#d8b27a", "sun": [1480, 190, 34], "ridges": [], "cam": CAM, "els": els}


def s16():
    """Plan: about two hundred graves pop on a dune ridge; beside it a vanished lake fills, 3 km across; then the lake in section, no more than
    3 m deep, a person for scale."""
    tg, tl, tk, td = T("s16", "about two hundred"), T("s16", "a lake that"), T("s16", "three kilometres"), T("s16", "no more than")
    cx, cy, rx, ry, rot = 400, 470, 300, 118, math.radians(-28)
    rot_ = lambda a, b: (cx + a * math.cos(rot) - b * math.sin(rot), cy + a * math.sin(rot) + b * math.cos(rot))
    ridge = [rot_(rx * math.cos(t) * (1 + .06 * math.sin(3 * t)), ry * math.sin(t)) for t in [2 * math.pi * k / 40 for k in range(40)]]
    els = [poly(ridge, "#c9a46e", "#e8d0a0", 2, -1, curve=True), poly([rot_(a * .8, b * .55) for a, b in [(rx * math.cos(t), ry * math.sin(t)) for t in
                                                                                                        [2 * math.pi * k / 30 for k in range(30)]]],
                                                                      "#d8b884", at=-1, curve=True, op=.6)]
    r = random.Random(16)
    pts = []
    while len(pts) < 200:
        a, b = r.uniform(-1, 1), r.uniform(-1, 1)
        if a * a + b * b < .9 and all(abs(a - p) > .045 or abs(b - q) > .09 for p, q in pts[-30:]):
            pts.append((a, b))
    pts.sort(key=lambda p: p[0])
    for k, (a, b) in enumerate(pts):
        x, y = rot_(a * (rx - 26), b * (ry - 16))
        els.append(poly(E(x, y, 6.5, 4, 10), "#4a3424", "#f0dcb4", 1, round(tg + .0115 * k, 2), fx="pop"))
    els += [lab(330, 690, "about 200 graves", tg + 1.2, BONE_E, 30)]
    # the vanished lake, 3 km across
    LX, LY, LR = 900, 450, 230
    lake = [(LX + LR * math.cos(t) * (1 + .05 * math.sin(2 * t)), LY + .86 * LR * math.sin(t) * (1 + .04 * math.cos(3 * t))) for t in
            [2 * math.pi * k / 36 for k in range(36)]]
    e = poly(lake, "rgba(63,127,156,.62)", "#9fd0ff", 2.5, tl, fx="fill", curve=True, style="inferred")
    e["dur"] = 1.4
    els += [e, lab(LX, LY + 14, "a vanished lake", tl + 1.0, "#e3f2fa", 30)]
    els += [ln([(LX - LR, 218), (LX + LR, 218)], tk, BONE, 3, dur=.6), ln([(LX - LR, 204), (LX - LR, 232)], tk, BONE, 3, draw=False),
            ln([(LX + LR, 204), (LX + LR, 232)], tk, BONE, 3, draw=False), lab(LX, 196, "3 km", tk + .3, BONE, 32)]
    # the lake in section: no more than 3 m deep (a person, 1.7 m, for scale)
    SX, SY = 1190, 470
    D = 180                                          # 3 m
    basin = [(SX + 30, SY), (SX + 120, SY + D * .55), (SX + 250, SY + D), (SX + 380, SY + D * .6), (SX + 470, SY)]
    els += [rect(SX - 40, 330, 560, 440, "rgba(18,13,10,.55)", "rgba(255,236,206,.25)", 1.5, 16, td - .3, fx="pop"),
            poly([(SX - 40, SY)] + basin + [(SX + 520, SY), (SX + 520, SY + 280), (SX - 40, SY + 280)], "#7a6248", at=td - .2, op=.95),
            poly(basin, LAKE, "#9fd0ff", 2, td + .2, fx="fill", curve=True),
            ln([(SX + 250, SY), (SX + 250, SY + D)], td + .9, BONE, 3, dur=.4), ln([(SX + 238, SY + D), (SX + 262, SY + D)], td + .9, BONE, 3, draw=False),
            lab(SX + 270, SY + D * .62, "3 m", td + 1.0, BONE, 32, "start"),
            figure(SX - 4, SY, D * 1.7 / 3, td + .6, "#e8d6b8")]
    return {"base": "plan", "bg": "#2e241a", "cam": CAM, "els": els}


def s17():
    """A rubbish heap in section, shells and ash; out of it rise, as named, a Nile perch, a catfish and a hippo; then bone harpoons and a bone hook,
    large and pale like museum pieces."""
    tp, tc, th, th2 = T("s17", "Nile perch"), T("s17", "catfish"), T("s17", "hippos"), T("s17", "harpoons")
    GY, X0, X1, MH = 640, 120, 1210, 190
    hump = lambda f, k: (X0 + (X1 - X0) * (.5 + (k / 24 - .5) * (.55 + .45 * f)), GY - MH * f * math.sin(math.pi * k / 24) ** .7)
    els = [rect(-40, GY, 1880, 400, "#241c15", at=-1), ln([(-40, GY), (1840, GY)], -1, "rgba(255,226,190,.35)", 1.5, draw=False)]
    for f, c in ((1.0, "#7a6c60"), (.8, "#5e5248"), (.62, "#9a8c7c"), (.42, "#4e443c"), (.24, "#8a7d70")):
        els.append(poly([hump(f, k) for k in range(25)], c, "rgba(255,236,206,.25)" if f == 1.0 else "none", 1.5, -1, curve=True))
    r = random.Random(17)
    for _ in range(46):
        k = r.uniform(3, 21)
        x, ytop = hump(1.0, k)
        y = r.uniform(ytop + 14, GY - 8)
        els.append(poly(E(x, y, r.uniform(5, 9), r.uniform(3, 5), 10), "#efe6d2", at=-1, op=round(r.uniform(.5, .9), 2)))
    els += [lab(665, GY + 52, "a rubbish heap", .5, MUTED, 28)]
    els += [fish(300, 330, 1.7, tp, "#d9e6ec", "perch", "rise"), lab(300, 430, "Nile perch", tp + .2, BONE, 30)]
    els += [fish(690, 290, 1.6, tc, "#c9d6c8", "catfish", "rise"), lab(690, 370, "catfish", tc + .2, BONE, 30)]
    els += [hippo_side(980, 420, 1.15, th, "#9a8a96", "rise"), lab(1040, 470, "hippo", th + .2, BONE, 30)]
    # the bone tools, like museum pieces
    els += [rect(1290, 190, 400, 460, "rgba(18,13,10,.7)", "rgba(255,236,206,.3)", 1.5, 14, th2 - .4, fx="pop"),
            harpoon(1325, 320, 330, -6, th2), harpoon(1325, 420, 290, -3, th2 + .3), hook(1500, 545, 1.4, th2 + .9),
            lab(1490, 246, "bone harpoons, a hook", th2 + .5, BONE_E, 28), gl(1490, 420, 280, th2, .25, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


GOB_X = lambda yr: 150 + 1480 * (yr + 8000) / 6000          # 8000 to 2000 BCE across the Gobero panel
GOB_AY, GOB_LT = 640, 480                                     # the time axis; the top of the lake


def s18():
    """Gobero's two phases on a time line: graves on the dune (Kiffian, in blue); from 7700 BCE the lake fills and a fisher stands in it with a
    harpoon; from 6200 BCE the lake drains to cracked mud; a thousand years without graves."""
    tb, tk, t77, tf, td, te, ta, tn = (T("s18", p) for p in ("buried here", "Kiffian", "seventy-seven", "fished the lake", "long dry spell", "lake emptied",
                                                            "about a thousand", "no one was"))
    X, AY, LT = GOB_X, GOB_AY, GOB_LT
    els = [axis(150, 1630, AY, [(X(-6000), "6000 BCE"), (X(-4000), "4000 BCE"), (X(-2000), "2000 BCE")], -1),
           rect(150, 410, 1480, 50, "#c9a46e", at=-1, op=.35, r=20),
           ln([(150, AY - 10), (1630, AY - 10)], -1, "#5a4a3a", 2, draw=False, style="inferred", op=.6)]
    els += [poly(E(X(-7600) + 40 * k, 434 + 7 * (k % 2), 8, 5, 10), "#9fd0ff", "#e3f2fa", 1, round(tb + .12 * k, 2), fx="pop") for k in range(9)]
    els += [lab(X(-6950), 384, "Kiffian", tk, BLUE, 32)]
    els += [ln([(X(-7700), AY - 12), (X(-7700), AY + 12)], t77, BONE, 2.5, draw=False), lab(X(-7700), AY + 46, "7700 BCE", t77 + .1, BONE, 26)]
    e = rect(X(-7700), LT, X(-6200) - X(-7700), AY - 12 - LT, LAKE, at=tf, fx="fill", r=6)
    e["dur"] = 1.0
    els += [e, fisher(330, 580, 104, tf + .6, "#1d1712", 1), poly(E(330, 580, 40, 7, 18), "none", "#cfe6ff", 2, tf + .6, op=.7, curve=True),
            fish(470, 590, .7, tf + 1.0, "#e9f2f8", "fish", "pop", -1)]
    mud = [(X(-6200), AY - 12), (X(-6200), AY - 44), (X(-5200), AY - 44), (X(-5200), AY - 12)]
    els += [poly(mud, "#8a6a46", "#c9a36c", 1.5, td, fx="fill")]
    els += [ln([(x, AY - 42), (x + 14, AY - 30), (x + 6, AY - 14)], td + .4, "#4a3424", 2, draw=False) for x in range(int(X(-6200)) + 20, int(X(-5200)) - 10, 40)]
    els += [lab((X(-6200) + X(-5200)) / 2, AY - 64, "dry", td + .5, "#e8b87a", 30),
            arrow(R([(X(-6200) - 10, LT + 20), (X(-6200) - 10, AY - 24)]), te, BONE, 3, "known", .5, curve=False)]
    els += arc_br(X(-6200) + 6, X(-5200) - 6, 372, 50, ta, "about 1,000 years", BONE, 28)
    els += [rect(X(-6200) + 8, 416, X(-5200) - X(-6200) - 16, 38, "none", MUTED, 2, 14, tn, style="inferred", fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def s19_add():
    """The lake fills again from 5200 BCE; new graves (gold, a different shape); the Tenerians; a herder and cattle at the shore."""
    tw, tb, tdf, tt, tc = T("s19", "came back"), T("s19", "burials"), T("s19", "different"), T("s19", "Tenerians"), T("s19", "cattle")
    X, AY, LT = GOB_X, GOB_AY, GOB_LT
    e = rect(X(-5200), LT, X(-2500) - X(-5200), AY - 12 - LT, LAKE, at=tw, fx="fill", r=6)
    e["dur"] = 1.2
    els = [e]
    els += [rect(X(-5100) + 34 * k - 7, 428 + 6 * (k % 2), 14, 11, GOLD, "#fff1d2", 1, 3, round(tb + .1 * k, 2), fx="pop") for k in range(10)]
    els += [ring(X(-5100) + 34 * 2, 434, 22, tdf, AMBER, 3, dur=.4), ring(X(-7600) + 40 * 3, 441, 22, tdf + .2, AMBER, 3, dur=.4)]
    els += [lab(X(-4400), 384, "Tenerian", tt, GOLD, 32)]
    els += [cowg(1340, 464, .5, tc, "#e8dcc6", horns="lyre", spots="#6a4a30"), cowg(1450, 466, .46, tc + .25, "#cbb8a0", flip=True),
            figure(1258, 464, 78, tc + .1, "#f2c98e")]
    return els


def s20():
    """The embrace, drawn only as light: about 3300 BCE; three soft lights of different sizes close together in one grave seen from above, soft
    loops of light around them; a lens with clumps of pollen; pink and white wool-flower plumes around the lights."""
    td, tw, tg, ti, tp, tf, tl = (T("s20", p) for p in ("fifty-three hundred", "a woman", "one grave", "intertwined", "Clumps of pollen", "wild flowers",
                                                       "were laid with"))
    GX, GY_ = 760, 480
    els = [rect(-80, -80, 1940, 1160, "#3a2e22", at=-1, op=.5), gl(GX, GY_, 560, -1, .12, "lamp")]
    r = random.Random(20)
    els += [poly(E(r.uniform(60, 1700), r.uniform(140, 790), r.uniform(2, 4), r.uniform(1.5, 3), 8), "#8a7052", at=-1, op=.6) for _ in range(60)]
    els += [lab(GX, 718, "about 3300 BCE", td, BONE, 30)]
    L = [(712, 482, 190, 13), (852, 436, 124, 9), (842, 550, 118, 8.5)]
    for k, (x, y, rr, d) in enumerate(L):
        els += [gl(x, y, rr, tw + .3 * k, .9, "lamp"), circ(x, y, d, "#fff6e0", at=tw + .3 * k, fx="pop", op=.9)]
    els += [poly(E(GX, GY_, 300, 172, 40), "none", BONE, 2.5, tg, fx="draw", curve=True, style="inferred")]
    els += [gl(790, 490, 300, ti, .55, "lamp"), gl(790, 490, 170, ti + .3, .45, "lamp")]
    # pollen, under a lens
    LX, LY, LR = 1370, 380, 150
    els += [circ(LX, LY, LR + 14, "#241c16", "#cbbca8", 6, tp, fx="pop"), circ(LX, LY, LR, "#4a3a2a", at=tp, fx="pop"),
            ln([(LX - 110, LY + 110), (LX - 190, LY + 190)], tp, "#cbbca8", 14, draw=False)]
    for k, (x, y) in enumerate(((LX - 50, LY - 40), (LX - 18, LY - 62), (LX - 14, LY - 22), (LX + 58, LY + 40), (LX + 30, LY + 60), (LX + 70, LY + 10))):
        els.append(group([circ(x, y, 19, "#e8b8c8", "#fff0f4", 1.5)] + [circ(x + 9 * math.cos(q), y + 9 * math.sin(q), 2.4, "#9a5a6a") for q in
                                                                      [2 * math.pi * j / 6 for j in range(6)]], round(tp + .5 + .1 * k, 2), "pop"))
    els += [lab(LX, LY + LR + 56, "pollen clumps", tp + .9, "#f0c8d4", 28)]
    # wool-flower plumes, pink and white, laid around the lights
    for k in range(18):
        a = 2 * math.pi * k / 18 + r.uniform(-.12, .12)
        x, y = GX + 252 * math.cos(a) * r.uniform(.84, 1.02), GY_ + 140 * math.sin(a) * r.uniform(.84, 1.02)
        c = "#e8a0b8" if k % 3 else "#f5ecdc"
        els.append(group([ln([(x, y + 14), (x + 2, y - 6)], -1, "#6f8a4c", 2.5, draw=False), poly([(x - 6, y - 2), (x, y - 26), (x + 6, y - 2)], c, curve=True),
                          poly([(x - 4, y - 8), (x, y - 20), (x + 4, y - 8)], "#ffffff", op=.4)], round(tl - .2 + .06 * k, 2), "pop"))
    els += [lab(1090, 650, "flowers", tf + .4, "#f0c8d4", 28, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s21():
    """Two peoples in 2008 (three blue figures, Kiffian; three gold, Tenerian; a wall between them); teeth run in families like noses (a molar
    with its cusps ringed, three profiles with one nose); a newer study: two rows of teeth alike, and the wall turns to dashes."""
    t8, tr_, tt, tn, tst, tap = (T("s21", p) for p in ("two thousand eight", "two different peoples", "teeth run", "shape of a nose", "newer study",
                                                       "hard to tell"))
    FY = 470
    els = [figure(x, FY, 150, .4 + .12 * k, BLUE) for k, x in enumerate((230, 320, 410))] + \
          [figure(x, FY, 150, .8 + .12 * k, GOLD) for k, x in enumerate((1370, 1460, 1550))]
    els += [lab(320, 528, "Kiffian", 1.0, BLUE, 30), lab(1460, 528, "Tenerian", 1.2, GOLD, 30)]
    els += [ln([(889, 230), (889, FY)], tr_, BONE, 5, dur=.6)] + tag(889, 196, "2008: two peoples", tr_ + .3, BONE, 28)
    # teeth run in families, like the shape of a nose
    MX, MY = 889, 660
    els += [molar_top(MX, MY, 64, tt)]
    els += [ring(MX + a * 64, MY + b * 64, 15, round(tt + .4 + .25 * k, 2), AMBER, 3, dur=.3) for k, (a, b) in
            enumerate(((-.55, -.6), (.5, -.6), (-.62, .42), (.56, .5), (0, .72)))]
    els += [lab(MX + 100, MY - 30, "teeth run in families", tt + .8, AMBER, 28, "start")]
    for k, x in enumerate((560, 650, 740)):
        y, s = MY + 10, 1.0 - .12 * k
        els.append(group([circ(x, y, 26 * s, "#d8c7ae"), poly([(x + 22 * s, y - 8 * s), (x + 42 * s, y + 10 * s), (x + 20 * s, y + 12 * s)], "#d8c7ae"),
                          circ(x + 8 * s, y - 6 * s, 3 * s, "#2a2018")], round(tn + .2 * k, 2), "pop"))
    # the newer study: their teeth alike; the wall turns to dashes
    els += [dveil(470, 556, 910, 244, tst - .2)]
    els += [tooth_side(x, 600, 70, round(tst + .3 + .1 * k, 2)) for k, x in enumerate((230, 320, 410))]
    els += [tooth_side(x, 600, 70, round(tst + .7 + .1 * k, 2)) for k, x in enumerate((1370, 1460, 1550))]
    els += [lab(889, 676, "≈", tap, GREEN, 96, st="big", fx="pop"), gl(889, 640, 140, tap, .5, "blue"), lab(889, 760, "newer study: alike", tap + .4, GREEN, 30)]
    els += [dveil(876, 224, 26, 252, tap + .2, .97, 4), ln([(889, 232), (889, FY)], tap + .5, BONE, 4, "inferred", dur=.5)]
    return {"base": "dark", "cam": CAM, "els": els}


def s22_add():
    """Back at the embrace: a dashed double helix and a question mark hover over the grave; a hot sun glows above; the three lights brighten."""
    td, tq, th, tl = T("s22", "Ancient DNA"), T("s22", "settle it"), T("s22", "the heat"), T("s22", "someone loved")
    els = helix(540, 262, 980, 262, td, n=12, amp=22, w=3, dur=.9, style="inferred") + [lab(760, 214, "ancient DNA?", td + .5, BLUE, 28)]
    els += qmark(1052, 290, tq, 80)
    els += [gl(330, 190, 340, th, .75, "sun"), circ(330, 190, 30, "#fff1d2", at=th, fx="pop")]
    els += [ln([(230 + 60 * k, 300), (240 + 60 * k, 286), (230 + 60 * k, 272), (240 + 60 * k, 258)], th + .3 + .1 * k, "#ffd9a0", 2, dur=.4, curve=True, op=.7)
            for k in range(4)]
    for k, (x, y, rr) in enumerate(((712, 482, 280), (852, 436, 180), (842, 550, 170))):
        els.append(gl(x, y, rr, tl + .2 * k, .75, "lamp"))
    els += [gl(760, 480, 460, tl + .6, .3, "lamp")]
    return els


# ================================================================== chapter 3: swimmers in the desert
WALL, WALL_D, WALL_L = "#c39a6c", "#a07a52", "#dcb88a"          # the pale sandstone of the painted walls


def _rockwall(y0=-60, y1=1060, seed=23, c=WALL, d=WALL_D, l=WALL_L):
    """A smooth pale sandstone wall: soft darker patches, a few cracks and faint bedding (static)."""
    r = random.Random(seed)
    els = [rect(-60, y0, 1900, y1 - y0, c, at=-1)]
    for _ in range(18):
        x, y = r.uniform(0, 1780), r.uniform(y0 + 40, y1 - 40)
        els.append(poly(E(x, y, r.uniform(80, 240), r.uniform(30, 90), 20), r.choice((d, l)), at=-1, curve=True, op=round(r.uniform(.12, .25), 2)))
    for _ in range(6):
        x, y = r.uniform(60, 1720), r.uniform(y0 + 60, y1 - 200)
        els.append(ln([(x, y), (x + r.uniform(-30, 30), y + r.uniform(60, 120)), (x + r.uniform(-50, 50), y + r.uniform(150, 260))], -1, "#7a5a3c", 1.6,
                      draw=False, op=.35, curve=True))
    return els


def _overhang(y0, y1, seed=5, c="#5a4030", lit="#8a6444"):
    """A sandstone overhang across the top of a panel, its lip waving at y1 (static)."""
    r = random.Random(seed)
    lip = [(x, y1 + r.uniform(-14, 14) + 18 * math.sin(x / 260)) for x in range(-60, 1901, 120)]
    return [poly([(-60, y0)] + [(1900, y0)] + lip[::-1], c, at=-1, curve=True),
            ln(lip, -1, lit, 4, draw=False, curve=True, op=.7),
            poly([(p[0], p[1] + 2) for p in lip] + [(1900, y1 + 70), (-60, y1 + 70)], "#2a1c12", at=-1, curve=True, op=.28)]


def rot_swimmer(x, y, s, at, c=OCHRE_P, ang=0, fx="pop", op=None):
    """A painted swimmer turned by ang degrees."""
    return group([swimmer(x, y, s, -1, c, None)], at, fx, tr="rotate(%d %.1f %.1f)" % (ang, x, y), op=op)


EGYPT_GILF = [(25.4, 24.4), (26.3, 24.2), (26.7, 23.4), (26.2, 22.7), (25.4, 23.0), (25.2, 23.6)]
WADI_SURA = (25.2335, 23.5947)


def s23():
    """The Cave of Swimmers: under a low sandstone overhang, a smooth pale wall where small red-brown swimmers appear one by one; a soft light;
    a locator map of Egypt with the Gilf Kebir in the far south-west (in place while the card holds the first sentence)."""
    tf = T("s23", "little painted")
    els = _rockwall(200) + _overhang(-60, 250, 7) + [gl(980, 520, 640, -1, .3, "lamp")]
    pos = [(760, 430, -8), (900, 470, 6), (1060, 420, -4), (1190, 470, 10), (840, 560, 2), (1000, 590, -10), (1150, 560, 4), (700, 540, 12), (1290, 400, -6)]
    els += [rot_swimmer(x, y, 2.1, round(tf + .3 * k, 2), OCHRE_P, a) for k, (x, y, a) in enumerate(pos)]
    m = Map(24, 37, 21, 32, rect=(100, 140, 330, 250))
    wx, wy = m.p(*WADI_SURA)
    els += [inset_map(m, 100, 140, 330, 250, -1, extra=[ln(m.path(NILE), -1, "#6fb6d6", 3, draw=False, curve=True),
                                                        poly(m.path(EGYPT_GILF), "#6a5440", "#9a8064", 1.2, -1, curve=True),
                                                        lab(*m.p(29.8, 27.4), "Egypt", -1, "#e8dcc6", 28), pin(wx, wy, "", -1, GOLD)])]
    return {"base": "dark", "cam": CAM, "els": els}


def s24_add():
    """The camera moves in on the swimmers: 'the Cave of Swimmers'."""
    tc = T("s24", "Cave of Swimmers")
    return [lab(980, 300, "the Cave of Swimmers", tc, BONE_E, 36, st="serif"), gl(980, 500, 420, tc, .25, "lamp")]


def s25():
    """The Cave of Beasts: a long low shelter, an overhanging lip over a wide pale wall; about 17 m, three people for scale; thousands of tiny
    painted marks spread over the wall; about 8,000 figures, about 8,000 years old."""
    ts, tb, t18, tf, ty = T("s25", "second shelter"), T("s25", "Cave of Beasts"), T("s25", "seventeen metres"), T("s25", "eight thousand figures"), \
        T("s25", "eight thousand years")
    X0, X1, GY = 140, 1640, 690
    M = (X1 - X0) / 18                                   # units per metre
    r0 = random.Random(31)
    top = [(X0 + (X1 - X0) * k / 16, 318 + r0.uniform(-10, 10)) for k in range(17)]
    els = [poly([(-60, 280), (1900, 280), (1900, 1060), (-60, 1060)], "#5a4030", at=-1),
           poly([(X0 - 60, GY + 6), (X0 - 10, 420), (X0 + 10, 330)] + top + [(X1 - 10, 330), (X1 + 10, 420), (X1 + 60, GY + 6)], "#3a2a1e", at=-1, curve=True),
           poly([(X0 + 10, GY)] + top + [(X1 - 10, GY)], WALL, at=-1),
           poly([(X0 + 10, GY), (X0 + 10, GY - 40), (X1 - 10, GY - 40), (X1 - 10, GY)], WALL_D, at=-1, op=.35)]
    els += _overhang(-60, 300, 11, "#4e3828", "#7a5a3c")
    els += [rect(-60, GY, 1960, 400, "#c9a46e", at=-1), ln([(-60, GY), (1900, GY)], -1, "rgba(255,236,206,.5)", 1.5, draw=False)]
    els += [gl(889, 500, 700, ts, .28, "lamp"), lab(889, 158, "the Cave of Beasts, 2002", tb, BONE_E, 34, st="serif")]
    els += [figure(X1 - 170 + 52 * k, GY, 1.7 * M, round(.4 + .15 * k, 2), "#2a2018") for k in range(3)]
    els += [ln([(X0, 732), (X1, 732)], t18, BONE, 3, dur=.8), ln([(X0, 718), (X0, 746)], t18, BONE, 3, draw=False),
            ln([(X1, 718), (X1, 746)], t18, BONE, 3, draw=False), lab(889, 772, "about 17 m", t18 + .3, BONE, 30)]
    r = random.Random(25)
    for k in range(380):
        x, y = r.uniform(X0 + 50, X1 - 60), r.uniform(350, GY - 40)
        if x > X1 - 230 and y > GY - 1.9 * M:
            continue
        els.append(circ(x, y, r.uniform(2.6, 4.6), r.choice((OCHRE_P, "#f0e2c8", "#8a3a22", "#e0b070")), at=round(tf + .004 * k, 2), fx="pop"))
    els += [lab(520, 266, "about 8,000 figures", tf + .7, BONE_E, 30), lab(1250, 266, "about 8,000 years old", ty, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def lizard_foot(x, y, s, at=-1, c="#6f8a4c", fx=None, style="known", w=None):
    """A lizard's front foot from above: a small palm and five long thin splayed toes with claws."""
    els = [poly(E(x, y + 10 * s, 18 * s, 22 * s, 14), c if style == "known" else "none", c, 2, curve=True, style=style)]
    for a, L in ((-150, 42), (-118, 62), (-90, 70), (-62, 62), (-30, 44)):
        t = math.radians(a)
        p0 = (x + 12 * s * math.cos(t), y + 12 * s * math.sin(t))
        p1 = (x + L * s * math.cos(t), y + L * s * math.sin(t))
        p2 = (p1[0] + 9 * s * math.cos(t + .5), p1[1] + 9 * s * math.sin(t + .5))
        els += [ln([p0, p1], -1, c, w or 7 * s, style, draw=False), ln([p1, p2], -1, c, (w or 7 * s) * .5, style, draw=False)]
    return group(els, at, fx)


def baby_hand(x, y, s, at=-1, c=BONE, fx=None):
    """A newborn's hand, outline dashed: a chubby palm, four short fingers, a thumb."""
    els = [poly([(x - 34 * s, y + 70 * s), (x - 40 * s, y), (x - 30 * s, y - 24 * s), (x + 30 * s, y - 24 * s), (x + 40 * s, y), (x + 34 * s, y + 70 * s)], "none", c, 2.5,
                curve=True, style="inferred")]
    for k, (dx, L) in enumerate(((-24, 40), (-8, 48), (8, 46), (24, 38))):
        els.append(rect(x + (dx - 7) * s, y - (24 + L) * s, 14 * s, (L + 6) * s, "none", c, 2.5, 7 * s, style="inferred"))
    els.append(poly([(x - 40 * s, y + 6 * s), (x - 68 * s, y - 16 * s), (x - 72 * s, y - 4 * s), (x - 44 * s, y + 26 * s)], "none", c, 2.5, curve=True, style="inferred"))
    return group(els, at, fx)


def s26():
    """Close on the wall: a hand stencil, a swimmer and a headless beast pop as named; then a tiny stencil is ringed; a newborn's hand (dashed) does
    not match it (a red cross); a lizard's front foot does (a green tick), and a little lizard."""
    th, tsw, tb, tt, tl, tm, tr, tz = (T("s26", p) for p in ("Hands", "swimmers", "headless beasts", "tiny hand stencils", "like a baby's",
                                                            "Measured against", "feet of a reptile", "perhaps a lizard"))
    els = _rockwall(-60, 1060, 26) + _overhang(-60, 170, 3)
    els += [stencil(270, 420, 1.25, th + .4, "#d8b88c", OCHRE_P, 6), lab(270, 600, "hands", th + .6, "#2a1a10", 28, halo=False)]
    els += [rot_swimmer(560, 420, 2.8, tsw + .4, OCHRE_P, -6), lab(560, 600, "swimmers", tsw + .6, "#2a1a10", 28, halo=False)]
    els += [beast(830, 470, 1.8, tb + .3, "#8a3a22"), lab(800, 600, "headless beasts", tb + .5, "#2a1a10", 28, halo=False)]
    # the comparison
    els += [rect(990, 210, 700, 520, "rgba(30,20,14,.82)", "rgba(255,236,206,.35)", 2, 18, tt - .2, fx="pop")]
    r = random.Random(7)
    spray = [circ(1100 + r.uniform(-62, 62), 430 + r.uniform(-74, 64), r.uniform(2, 5), OCHRE_P, op=round(r.uniform(.4, .85), 2)) for _ in range(60)]
    els += [group(spray + [poly(E(1100, 420, 62, 70, 20), OCHRE_P, op=.3, curve=True), lizard_foot(1100, 450, .9, -1, WALL_L)], tt + .1, "pop"),
            ring(1100, 420, 92, tt + .5, AMBER, 3, dur=.5), lab(1100, 580, "tiny stencils", tt + .6, AMBER, 26)]
    els += [baby_hand(1330, 470, 1.15, tl, BONE, "pop"), lab(1330, 580, "a baby's hand?", tl + .3, BONE, 26)] + cross(1330, 420, tm + 1.6, RED, 2.2, 7)
    els += [lizard_foot(1560, 450, .9, tr, "#8fbf6a", "pop"), lab(1560, 580, "a reptile's foot", tr + .3, GREEN, 26), tick(1600, 330, tr + .8, GREEN, 1.4)]
    lz = [poly([(1500, 660), (1540, 648), (1590, 650), (1630, 658), (1590, 666), (1540, 668)], "#8fbf6a", curve=True),
          ln([(1500, 660), (1470, 666), (1440, 676)], -1, "#8fbf6a", 5, draw=False, curve=True)] + \
         [ln([(x0, y0), (x0 + dx, y0 + dy)], -1, "#8fbf6a", 4, draw=False) for x0, y0, dx, dy in ((1530, 650, -8, -16), (1530, 666, -8, 16), (1585, 651, 8, -16),
                                                                                                    (1585, 665, 8, 16))]
    els += [group(lz, tz, "pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def nun_sign(x, y, s, at, c=GOLD):
    """The water sign: three zigzag lines."""
    return group([ln([(x - 60 * s + 15 * s * j, y + 18 * s * k + (6 * s if j % 2 else -6 * s)) for j in range(9)], -1, c, 3, draw=False) for k in range(3)], at, "pop")


def s27():
    """Two readings, side by side: a bright lake with a grassy shore and the red swimmers floating in it, 'a real lake?'; deep dark water with
    faint points of light, the same figures drifting pale and still, a low mound rising from the water, 'the waters before creation?'."""
    tq, ta, tw, to, tfl, td, te = (T("s27", p) for p in ("really swimming", "showed a real lake", "wetter time", "Others see", "floating", "dark waters",
                                                        "later Egyptian"))
    els = [rot_swimmer(889, 214, 2.2, .4, "#c8643c", 0), lab(1040, 240, "?", tq, LILAC, 60, st="big", fx="pop")]
    # a real lake
    L0, L1, T0, B0 = 130, 830, 330, 700
    els += [rect(L0, T0, L1 - L0, B0 - T0, "#8aa3b8", "rgba(255,236,206,.4)", 2, 14, ta - .2, fx="pop"),
            rect(L0, T0 + 120, L1 - L0, B0 - T0 - 120, "#3f7f9c", at=ta, r=0, fx="fill"),
            poly([(L0, T0 + 120), (L0 + 230, T0 + 112), (L0 + 340, T0 + 126), (L0, T0 + 140)], GRASS, at=ta, curve=True),
            gl(L0 + 560, T0 + 50, 120, ta, .7, "sun")]
    els += tufts(L0 + 10, L0 + 300, T0 + 122, 8, ta + .1, "#7d9a5a", 18, seed=27)
    els += [rot_swimmer(x, y, 2.0, round(ta + .5 + .25 * k, 2), "#b04a2a", a) for k, (x, y, a) in enumerate(((330, 560, -4), (520, 610, 6), (680, 540, -8)))]
    els += [ln([(x, y), (x + 40, y)], tw, "#e9f2f8", 2, draw=False, op=.5) for x, y in ((280, 580), (470, 632), (640, 562), (360, 660))]
    els += [lab((L0 + L1) / 2, 752, "a real lake?", tw, "#cfe6ff", 30)]
    # the waters before creation
    R0, R1 = 950, 1650
    els += [rect(R0, T0, R1 - R0, B0 - T0, "#0d1a26", "#2a4a5a", 2, 14, to, fx="pop")]
    r = random.Random(27)
    els += [circ(r.uniform(R0 + 20, R1 - 20), r.uniform(T0 + 20, B0 - 20), r.uniform(1.2, 2.6), "#9fd0ff", at=round(to + .3 + .03 * k, 2), op=round(r.uniform(.3, .7), 2))
            for k in range(26)]
    els += [rot_swimmer(x, y, 2.0, round(tfl + .3 * k, 2), "#c8b8a8", a, op=.75) for k, (x, y, a) in enumerate(((1080, 470, 24), (1230, 560, -18), (1110, 630, 8)))]
    els += [gl(1180, 540, 200, tfl + .4, .25, "lamp")]
    els += [poly([(1380, B0 - 2), (1440, 600), (1500, 572), (1570, 584), (1636, B0 - 2)], "#6a5440", "#c9ad85", 2, td, fx="rise", curve=True),
            nun_sign(1508, 420, .9, te, GOLD)]
    els += [lab((R0 + R1) / 2, 752, "the waters before creation?", td + .6, "#e8b87a", 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s28():
    """The gap: a time line from 7000 BCE to today; the paintings (6500 to 4400 BCE) and the Egyptian texts (about 2400 to 1100 BCE), a long
    dashed arc between them, 'thousands of years'; then a Roman mosaic (about 1 CE) and a book of today, about 2,000 years apart."""
    tt, tg, tm, tb = T("s28", "Egyptian texts"), T("s28", "thousands of years"), T("s28", "Roman mosaic"), T("s28", "book written")
    X = lambda yr: 150 + 1480 * (yr + 7000) / 9026
    AY = 600
    els = [axis(150, 1630, AY, [(X(-7000), "7000 BCE"), (X(-5000), "5000"), (X(-3000), "3000"), (X(-1000), "1000 BCE"), (X(1000), "1000 CE")], -1)]
    els += [band(X(-6500), X(-4400), AY - 12, 24, "#c8643c", .3, dur=.6), rot_swimmer((X(-6500) + X(-4400)) / 2, 530, 1.6, .5, "#c8643c", 0),
            lab((X(-6500) + X(-4400)) / 2, 470, "paintings", .6, "#e8a070", 30)]
    xt = (X(-2400) + X(-1100)) / 2
    els += [band(X(-2400), X(-1100), AY - 12, 24, "#e8dcc2", tt, dur=.5),
            group([rect(xt - 34, 500, 68, 60, "#e8dcc2", "#8a7a66", 2, 4), ln([(xt - 20, 518), (xt + 20, 518)], -1, "#8a7a66", 2, draw=False),
                   ln([(xt - 20, 532), (xt + 16, 532)], -1, "#8a7a66", 2, draw=False), ln([(xt - 20, 546), (xt + 20, 546)], -1, "#8a7a66", 2, draw=False)], tt + .2, "pop"),
            lab(xt, 470, "Egyptian texts", tt + .3, "#e8dcc2", 30)]
    els += arc_br(X(-4400) + 8, X(-2400) - 8, 440, 80, tg, "thousands of years", BONE, 30, style="inferred", dur=1.0)
    xm = X(1)
    els += [group([rect(xm - 36 + 18 * (k % 4), 498 + 18 * (k // 4), 16, 16, ["#c8643c", "#e8dcc2", "#3f7f9c", "#e8b87a"][(k + k // 4) % 4], r=1) for k in range(16)],
                  tm, "pop"), lab(xm, 470, "Roman mosaic", tm + .2, "#e8dcc2", 30)]
    xb = X(2026)
    els += [group([rect(xb - 46, 494, 44, 66, "#8fb5a0", "#e8dcc2", 2, 3), ln([(xb - 38, 506), (xb - 38, 552)], -1, "#e8dcc2", 2, draw=False)], tb, "pop"),
            lab(xb + 30, 470, "a book today", tb + .2, "#cbbca8", 30, "end")]
    els += bracket(xm, xb - 24, 690, tb + .4, None, AMBER, False) + [lab((xm + xb) / 2, 744, "about 2,000 years", tb + .7, AMBER, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


PAINT_W = "#7a5a42"                       # a darker painted rock wall (Tassili)


def s29():
    """A long rock wall: on the right a painted herd (piebald cattle in a line, herders, someone milking); on the left, larger and older, a giant
    Round Head with raised arms, a modern person for scale; the 1950s nickname; then the claim drawn dotted: a saucer and a helmet."""
    th, tc, tm, tg, tn, tl, tlit = (T("s29", p) for p in ("whole herds", "cattle", "milking", "older giants", "nineteen fifties", "nicknamed",
                                                         "took the name"))
    els = _rockwall(-60, 1060, 29, PAINT_W, "#5a4030", "#9a7a5a")
    for k in range(5):
        els.append(cowg(1060 + 115 * k, 450, .62, round(th + .2 * k, 2), "#f0e6d4", horns="lyre", spots="#8a3a22"))
    els += [figure(960, 450, 96, th + .2, "#a8402a", "pop"), figure(1650, 450, 92, th + 1.2, "#a8402a", "pop")]
    els += [cowg(1300, 690, .7, tm, "#f0e6d4", horns="lyre", spots="#8a3a22"), kneeler(1238, 690, 110, tm + .2, "#a8402a", 1, "pop"),
            group([poly(E(1262, 678, 16, 12, 12), "#c9774a")], tm + .4, "pop"), cowg(1480, 690, .6, tm + .3, "#e8dcc8", flip=True, horns="lyre", spots="#6a3020")]
    els += [lab(1300, 286, "herds and milking", tm + .3, "#f5ecdc", 30)]
    # the giant, older and larger, and a modern person for scale
    els += [roundhead(430, 760, 600, "#d8c7ae", "#b0643c", .9, tg, "pop"), figure(760, 760, 178, tg + .6, "#1a1511")]
    els += [lab(612, 214, "1950s nickname", tl + .4, "#f5ecdc", 30, "start")]
    hy = 760 - 600 * .72 - 600 * .15 * .9
    els += [circ(430, hy, 600 * .15 * 1.35, "none", LILAC, 3, tlit, style="claimed", fx="draw"),
            ln([(430 - 84, hy + 10), (430 + 84, hy + 10)], tlit + .3, LILAC, 3, "claimed", dur=.3)] + ufo(176, 214, tlit + .6, LILAC, .75)
    return {"base": "dark", "cam": CAM, "els": els}


def s30():
    """Three Round Heads: a dotted helmet struck out in red ('a way of painting'), a pale mask over a face, a soft glow (a spirit); then a small
    red swimmer with a lilac question mark."""
    tbh, twp, tm, ts, tsw = T("s30", "blank head"), T("s30", "way of painting"), T("s30", "a mask"), T("s30", "a spirit"), T("s30", "The swimmers")
    els = _rockwall(-60, 1060, 30, PAINT_W, "#5a4030", "#9a7a5a")
    H, BY = 440, 700
    xs = (330, 700, 1070)
    hy = BY - H * .72 - H * .15 * .9
    els += [roundhead(x, BY, H, "#d8c7ae", "#b0643c", 1.0, round(.3 + .15 * k, 2), "pop") for k, x in enumerate(xs)]
    els += [ring(700, hy, H * .15 * 1.5, tbh, AMBER, 3, dur=.5)]
    els += [lab(700, 172, "a way of painting", twp + .2, "#f5ecdc", 32)]
    x3 = xs[2]
    els += [circ(x3, hy, H * .15 * 1.35, "none", LILAC, 3, twp, style="claimed", fx="draw"), ln([(x3, hy - 88), (x3, hy - 130)], twp + .2, LILAC, 3, "claimed", dur=.3),
            ln([(x3 - 120, hy + 110), (x3 + 120, hy - 150)], twp + .7, RED, 6, dur=.4)]
    els += [group([poly(E(xs[0], hy + 4, H * .13, H * .16, 20), "#efe6d2", "#fff6e6", 1.5, curve=True), circ(xs[0] - 14, hy - 4, 5, "#2a2018"),
                   circ(xs[0] + 14, hy - 4, 5, "#2a2018"), ln([(xs[0] - 10, hy + 26), (xs[0] + 10, hy + 26)], -1, "#2a2018", 2, draw=False)], tm, "pop"),
            lab(xs[0], 760, "a mask?", tm + .2, "#f5ecdc", 30)]
    els += [gl(xs[1], BY - H * .5, 300, ts, .75, "lamp"), gl(xs[1], hy, 140, ts + .2, .8, "lamp"), lab(xs[1], 760, "a spirit?", ts + .3, "#f5ecdc", 30)]
    els += [rot_swimmer(1450, 520, 2.4, tsw, OCHRE_P, -4)] + qmark(1450, 430, tsw + .6, 90)
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 4: a lineage no one knew
TAKARKORI = (10.333, 24.883)
TAFORALT = (-2.40, 34.81)
W2 = "#f2c98e"                                   # the two women, drawn only as warm lights


def ghost_person(x, y, h, at=-1, c=BLUE, fx=None):
    """A person drawn only as a dashed outline (someone not yet sampled)."""
    w = h * .26
    body = [(x - w * .5, y - h * .78), (x + w * .5, y - h * .78), (x + w * .42, y - h * .42), (x + w * .3, y), (x + w * .08, y), (x, y - h * .36),
            (x - w * .08, y), (x - w * .3, y), (x - w * .42, y - h * .42)]
    return group([circ(x, y - h * .9, h * .085, "none", c, 2, style="inferred"), poly(body, "rgba(159,208,255,.05)", c, 2, style="inferred")], at, fx)


def s31():
    """Takarkori, about 7,000 years ago: a green valley under a sandstone cliff with a rock shelter; two small warm lights under the overhang (no
    remains drawn); a lake, grass, cattle and herders; a locator map of Libya."""
    th, tc, tl, tg = T("s31", "herders lived"), T("s31", "their cattle"), T("s31", "beside lakes"), T("s31", "grassland")
    GY = 640
    els = [gl(760, 300, 600, -1, .3, "sun")]
    els += mesas(600, -1, "#8b8fa6", seed=31, h=50, x1=980) + [poly([(-40, 596), (1000, 592), (1000, 650), (-40, 650)], "#55703a", at=-1)]
    els += [acacia(160, 614, 70), acacia(380, 608, 54), acacia(760, 612, 62)]
    els += cliff(940, 200, GY, -1, seed=31)
    els += [gl(1240, 610, 120, -1, .7, "lamp"), circ(1220, 612, 7, "#fff1d2", op=.9), circ(1286, 616, 7, "#fff1d2", op=.9), gl(1286, 616, 70, -1, .6, "lamp")]
    els += [poly([(60, 700), (300, 682), (560, 690), (640, 716), (520, 770), (200, 778), (40, 750)], LAKE, "#9fd0ff", 1.5, -1, curve=True),
            gl(320, 724, 200, tl, .45, "blue")] + [ln([(x, 714 + 10 * (k % 3)), (x + 50, 714 + 10 * (k % 3))], tl + .1 * k, "#e9f2f8", 2, draw=False, op=.5)
                                                   for k, x in enumerate((150, 280, 400, 210))]
    els += tufts(-20, 900, GY + 6, 34, tg, "#7d9a5a", 22, seed=32)
    els += [figure(470, 668, 104, th, "#2a2018"), figure(880, 662, 100, th + .3, "#2a2018"),
            cowg(600, 672, .62, tc, "#e8dcc6", horns="lyre", spots="#6a4a30"), cowg(730, 676, .56, tc + .25, "#cbb8a0", flip=True, horns="lyre"),
            cowg(820, 664, .5, tc + .45, "#d8c7ae", horns="lyre", spots="#4a3424")]
    m = Map(0, 25, 15, 34, rect=(100, 140, 320, 240))
    tx, ty = m.p(*TAKARKORI)
    els += [inset_map(m, 100, 140, 320, 240, -1, extra=[lab(*m.p(17, 27.5), "Libya", -1, "#e8dcc6", 26), pin(tx, ty, "", -1, GOLD)])]
    els += [lab(660, 448, "Takarkori, about 7,000 years ago", .5, BONE_E, 32, st="serif")]
    return {"base": "sky", "tod": "day", "ground": GY, "groundc": "#55703a", "sun": [760, 300, 30], "ridges": [], "cam": CAM, "els": els}


def s32_add():
    """The desert returns: the sky pales, sand rises over the grass, the lake and the herds; heat shimmers over the shelter; the two lights stay."""
    t0, tw, tm = T("s32", "dry air"), T("s32", "two women"), T("s32", "natural mummies")
    out = [rect(-60, -60, 1960, 660, "#efd9b2", at=t0, op=.42, dur=1.2), gl(760, 300, 260, t0 + .1, .8, "sun")]
    haze = poly([(-60, 1060), (-60, 560), (980, 560), (1010, 640), (1180, 700), (1500, 720), (1900, 720), (1900, 1060)], "#d8b27a", at=t0 + .2, op=.9)
    haze["dur"] = 1.4
    out += [haze]
    r = random.Random(32)
    out += [ln([(x, y), (x + r.uniform(60, 140), y - r.uniform(2, 6))], round(t0 + .8 + .02 * k, 2), "#b8925c", 2, draw=False, op=.6)
            for k, (x, y) in enumerate([(r.uniform(0, 1700), r.uniform(600, 980)) for _ in range(24)]) if not (900 < x < 1500 and y < 700)]
    out += [ln([(1180 + 40 * k + 8 * math.sin(j), 500 - 18 * j) for j in range(6)], round(t0 + .8 + .15 * k, 2), "#ffd9a0", 2.5, dur=.6, curve=True, op=.7)
            for k in range(4)]
    out += [gl(1220, 612, 90, tw, .9, "lamp"), gl(1286, 616, 90, tw + .2, .9, "lamp"), lab(1250, 460, "natural mummies", tm, BONE_E, 30)]
    return out


def s33():
    """DNA read in 2025: a strip of letters as coloured blocks; a typo; then one line splits into two branches, different typos pile up on each,
    and a bracket between the tips: more typos, longer apart."""
    t25, tr_, tg, tt, tc, tf, tl = (T("s33", p) for p in ("twenty twenty-five", "read their DNA", "Each generation", "tiny typos", "Count the typos",
                                                         "family lines", "how long"))
    BASES = ["#e8b87a", "#9fd0ff", "#8fd9b0", "#ff8a7a"]
    r = random.Random(33)
    cols = [BASES[int(r.random() * 4)] for _ in range(20)]
    els = [gl(250, 204, 90, -1, .7, "lamp"), circ(236, 204, 7, "#fff6e0", at=-1), circ(264, 204, 7, "#fff6e0", at=-1),
           lab(250, 274, "2025", t25, GOLD, 34, st="serif")]
    els += [rect(360 + 52 * k, 180, 44, 48, cols[k], at=round(tr_ + .06 * k, 2), r=6, fx="pop") for k in range(20)]
    els += [rect(360 + 52 * 11 - 4, 176, 52, 56, "none", RED, 4, 8, tt, fx="pop"), rect(360 + 52 * 11, 180, 44, 48, RED, at=tt + .2, r=6, fx="pop"),
            lab(360 + 52 * 11 + 22, 274, "a typo", tt + .4, RED, 28)]
    S, U, D = (520, 540), (1400, 380), (1400, 700)
    els += [ln([(200, 540), S], tg, "#cbbca8", 6, dur=.6)] + [circ(240 + 66 * k, 540, 6, "#cbbca8", at=round(tg + .2 + .12 * k, 2), fx="pop") for k in range(5)]
    els += [ln([S, U], tc, GOLD, 6, dur=1.0), ln([S, D], tc + .2, "#cbbca8", 6, dur=1.0)]
    pt = lambda A, f: (S[0] + (A[0] - S[0]) * f, S[1] + (A[1] - S[1]) * f)
    for k, f in enumerate((.3, .55, .8)):
        x, y = pt(U, f)
        els.append(ln([(x - 7, y - 18), (x + 7, y + 18)], round(tf + .4 * k, 2), RED, 5, draw=False, fx="pop"))
    for k, f in enumerate((.22, .45, .68, .9)):
        x, y = pt(D, f)
        els.append(ln([(x - 7, y - 18), (x + 7, y + 18)], round(tf + .2 + .4 * k, 2), RED, 5, draw=False, fx="pop"))
    els += [ln([(1450, 380), (1470, 380), (1470, 700), (1450, 700)], tl, BONE, 3, dur=.6), lab(1490, 552, "more typos,", tl + .3, BONE, 28, "start"),
            lab(1490, 590, "longer apart", tl + .4, BONE, 28, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s34():
    """93 squares in 100 gold (a North African line), 7 lilac; a family tree on a time axis: the trunk splits about 50,000 years ago into the
    lineages south of the Sahara, those outside Africa and the gold North African one, which runs on alone to Takarkori."""
    tm, tn, ts, tsa, to, tf, ta = (T("s34", p) for p in ("Most of the", "North African line", "It split", "south of the Sahara", "outside Africa",
                                                        "fifty thousand", "stayed apart"))
    els = []
    for k in range(100):
        i, j = k // 10, k % 10
        c = GOLD if k < 93 else LILAC
        els.append(rect(150 + 38 * j, 210 + 38 * i, 33, 33, c, at=round(.3 + .012 * k, 2), r=4, fx="pop", op=.92))
    els += [lab(340, 640, "93 in 100", tm + .8, GOLD, 44, st="serif"), lab(340, 692, "from a North African line", tn, GOLD, 26)]
    Tx = lambda ya: 640 + 1000 * (60000 - ya) / 60000
    AY, NY = 740, 470
    els += [axis(640, 1640, AY, [(Tx(50000), "50,000 years ago"), (Tx(0), "today")], ts - .3)]
    nx = Tx(50000)
    els += [ln([(640, NY), (nx, NY)], ts, "#cbbca8", 6, dur=.5), circ(nx, NY, 9, "#e9dccb", at=ts + .4, fx="pop"),
            ln([(nx, NY), (1100, 600), (1640, 640)], tsa, "#cbbca8", 5, dur=1.0, curve=True), lab(1640, 680, "south of the Sahara", tsa + .6, MUTED, 26, "end"),
            ln([(nx, NY), (1100, 330), (1640, 300)], to, "#cbbca8", 5, dur=1.0, curve=True), lab(1640, 268, "outside Africa", to + .6, MUTED, 26, "end"),
            ln([(nx, NY), (1150, NY)], to + .3, GOLD, 7, dur=.8), lab(1010, NY - 26, "North Africa", to + .7, GOLD, 26),
            ln([(nx, NY), (nx, AY - 10)], tf, BONE, 2, "inferred", dur=.4), gl(nx, NY, 80, tf, .6, "lamp")]
    tk = Tx(7000)
    els += [ln([(1150, NY), (tk, NY)], ta, GOLD, 7, dur=.6), gl(tk, NY, 70, ta + .5, .8, "lamp"), circ(tk - 8, NY, 6, "#fff6e0", at=ta + .5, fx="pop"),
            circ(tk + 8, NY, 6, "#fff6e0", at=ta + .6, fx="pop"), lab(tk, NY - 30, "Takarkori", ta + .6, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """Their nearest known relatives: a map of North Africa with Takarkori and the Taforalt cave in Morocco, a dashed arc between them; below, a
    time line: Taforalt about 15,000 years ago, Takarkori about 7,000, about 8,000 years apart."""
    tr_, th, tmo, t15 = T("s35", "nearest known"), T("s35", "Hunters"), T("s35", "Morocco"), T("s35", "fifteen thousand")
    m = Map(-18, 36, 18, 38, rect=(90, 120, 1600, 680))
    kx, ky = m.p(*TAKARKORI)
    fx_, fy_ = m.p(*TAFORALT)
    els = [wide_land(m), pin(kx, ky, "Takarkori, Libya", -1, GOLD, "start", 16, 8), gl(kx, ky, 60, -1, .6, "lamp")]
    els += [pin(fx_, fy_, "Taforalt cave, Morocco", tmo, BLUE, "start", 16, 8), gl(fx_, fy_, 50, tmo + .1, .6, "blue")]
    els += [arrow(R([(kx - 10, ky - 10), ((kx + fx_) / 2, min(ky, fy_) - 70), (fx_ + 12, fy_ + 6)]), th, GOLD, 3, "inferred", 1.0)]
    X = lambda ya: 300 + 1200 * (20000 - ya) / 20000
    AY = 690
    els += [rect(200, 600, 1400, 190, "rgba(14,11,9,.82)", "rgba(255,236,206,.25)", 1.5, 18, -1),
            axis(260, 1540, AY, [(X(20000), "20,000 years ago"), (X(15000), "15,000"), (X(7000), "7,000"), (X(0), "today")], -1)]
    els += [circ(X(7000), AY, 12, GOLD, at=.4, fx="pop"), circ(X(15000), AY, 12, BLUE, at=t15, fx="pop")]
    els += bracket(X(15000), X(7000), AY - 40, t15 + .8, None, BONE, False) + [lab((X(15000) + X(7000)) / 2, AY - 56, "about 8,000 years apart", t15 + 1.1, BONE, 28)]
    return {"base": "map", "cam": CAM, "els": els}


def s36():
    """Mostly local: a row of five people; a cow passes from hand to hand along it; below, a wave of newcomers drawn dotted and struck out; then a clay
    pot with a pale glow of milk fat in its wall."""
    tl, tc, tp, tn, tpo, tf = (T("s36", p) for p in ("mostly local", "Cattle and milk", "passed from", "wave of newcomers", "Their pots", "earliest milk"))
    xs = [200, 400, 600, 800, 1000]
    FY = 520
    els = [ln([(120, FY), (1080, FY)], -1, "#8c7152", 3, draw=False)] + [figure(x, FY, 150, round(.3 + .1 * k, 2), W2) for k, x in enumerate(xs)]
    els += [lab(600, 200, "mostly local", tl, W2, 34, st="serif")]
    els += [cowg(xs[0] + 6, 340, .36, tc, "#e8dcc6", horns="lyre", spots="#6a4a30")]
    for k in range(4):
        els += [arrow(R([(xs[k] + 40, 300), ((xs[k] + xs[k + 1]) / 2, 260), (xs[k + 1] - 40, 300)]), round(tp + .35 * k, 2), AMBER, 3, "known", .4),
                cowg(xs[k + 1] + 6, 340, .36, round(tp + .35 * k + .3, 2), "#e8dcc6", horns="lyre", spots="#6a4a30")]
    els += [lab(600, 580, "neighbour to neighbour", tp + 1.6, AMBER, 28)]
    els += [group([figure(140 + 54 * k, 740, 84, -1, "#5e5850", None) for k in range(7)], tn, "rise"),
            arrow(R([(520, 700), (700, 690), (860, 700)]), tn + .3, "#8a8178", 3, "claimed", .6), ln([(110, 750), (880, 630)], tn + 1.0, RED, 6, dur=.4)]
    els += [pot(1400, 380, 1.15, tpo), gl(1400, 520, 170, tf, .7, "lamp"),
            ln([(1300, 470), (1290, 540), (1310, 600), (1360, 630)], tf + .2, "#fff6e8", 9, dur=.6, curve=True, op=.8),
            ln([(1500, 470), (1510, 540), (1490, 600), (1440, 630)], tf + .3, "#fff6e8", 9, dur=.6, curve=True, op=.8),
            lab(1400, 720, "milk fat in the clay", tf + .6, BONE_E, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s37():
    """Two women are not a whole people: a crowd of grey figures, two lit gold in its middle; a map strip: teeth from Gobero point to roots near the
    Nile (a dashed arrow, a tooth); empty dashed outlines wait for their genomes."""
    tw, tt, tn, tm, tg = T("s37", "two women"), T("s37", "Teeth from"), T("s37", "near the Nile"), T("s37", "People moved"), T("s37", "more genomes")
    els = []
    for row in range(5):
        for j in range(8):
            x, y = 170 + 82 * j + 20 * (row % 2), 300 + 92 * row
            if (row, j) in ((2, 3), (2, 4)):
                continue
            els.append(figure(x, y, 72, round(.2 + .015 * (row * 8 + j), 2), "#7a7268", None))
    els += [gl(170 + 82 * 3.5 + 20 * 0, 300 + 92 * 2 - 36, 110, tw, .7, "lamp"), figure(170 + 82 * 3, 484, 72, tw, W2, "pop"), figure(170 + 82 * 4, 484, 72, tw + .1, W2, "pop"),
            lab(477, 760, "two women", tw + .3, W2, 30)]
    m = Map(4, 36, 11, 25, rect=(900, 150, 780, 330))
    gx, gy = m.p(*GOBERO)
    nx, ny = m.p(32.4, 16.6)
    els += [inset_map(m, 900, 150, 780, 330, -1, extra=[ln(m.path(NILE), -1, "#6fb6d6", 3.5, draw=False, curve=True), lab(nx + 20, ny + 74, "the Nile", -1, "#9fd0ff", 26, "start"),
                                                        pin(gx, gy, "Gobero", -1, GOLD, "end", -16, 8)])]
    els += [arrow(R([(nx - 16, ny), ((nx + gx) / 2, ny - 60), (gx + 18, gy)]), tn, BLUE, 4, "inferred", 1.2), I.tooth((nx + gx) / 2, ny - 48, 40, tt + .4)]
    els += [arrow(R([(gx + 30, gy + 40), ((nx + gx) / 2, ny + 40), (nx - 20, ny + 30)]), tm, BLUE, 3, "inferred", 1.0)]
    els += [ghost_person(1000 + 110 * k, 700, 120, round(tg + .1 * k, 2), BLUE, "pop") for k in range(6)]
    els += [lab(1275, 762, "more genomes", tg + .5, BLUE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 5: stones that watched the sun
NABTA, ABU_SIMBEL = (30.7256, 22.508), (31.6258, 22.3372)
NASSER = [(32.9, 24.0), (32.95, 23.6), (32.6, 23.1), (32.2, 22.7), (31.7, 22.3), (31.3, 21.8), (31.15, 21.9), (31.5, 22.4), (32.0, 22.9), (32.5, 23.4), (32.8, 23.9)]
RING_C, RING_R = (889, 470), 230                              # the ring in plan: about 4 m across
SUNRISE = (math.sin(math.radians(64)), -math.cos(math.radians(64)))   # the midsummer sunrise azimuth at Nabta, about 64 degrees east of north


def s38():
    """Left: southern Egypt, the Nile and Lake Nasser, Nabta Playa about 100 km west of Abu Simbel (in place while the card holds). Right: a playa
    in section, a dry hollow; rain falls, it fills with a seasonal lake, herders and cattle come to its edge."""
    tp, tr_, ts, th = T("s38", "dry lake bed"), T("s38", "only after rain"), T("s38", "summer rains"), T("s38", "herders came")
    m = Map(28.6, 34.6, 20.2, 25.6, rect=(100, 150, 560, 470))
    nx, ny = m.p(*NABTA)
    ax, ay = m.p(*ABU_SIMBEL)
    els = [inset_map(m, 100, 150, 560, 470, -1, extra=[poly(m.path(NASSER), "#3f7f9c", "#9fd0ff", 1.2, -1, curve=True), ln(m.path(NILE), -1, "#6fb6d6", 3, draw=False, curve=True),
                                                       pin(nx, ny, "Nabta Playa", -1, GOLD, "end", -16, 40), pin(ax, ay, "Abu Simbel", -1, BLUE, "start", 14, 40),
                                                       lab(*m.p(30.0, 24.6), "Egypt", -1, "#e8dcc6", 28)])]
    els += [arrow(R([(ax - 10, ay - 16), ((ax + nx) / 2, ay - 52), (nx + 12, ny - 14)]), .4, AMBER, 3, "known", .7), lab((ax + nx) / 2, ay - 66, "100 km", .8, AMBER, 26)]
    GY, X0, X1 = 500, 760, 1680
    hollow = [(X0, GY), (930, GY), (990, GY + 50), (1080, GY + 74), (1360, GY + 74), (1450, GY + 50), (1510, GY), (X1, GY)]
    els += [poly(hollow + [(X1, 800), (X0, 800)], "#9c7e58", "rgba(255,226,190,.6)", 2, -1),
            rect(X0, GY + 110, X1 - X0, 190, "#7a6248", at=-1, op=.8),
            poly([(992, GY + 52), (1080, GY + 70), (1360, GY + 70), (1448, GY + 52)], "#b8956a", at=-1, op=.6, curve=True)]
    els += [ln([(x, GY + 56), (x + 18, GY + 64), (x + 8, GY + 70)], -1, "#6a4a30", 2, draw=False, op=.7) for x in range(1020, 1420, 46)]
    els += [lab(1220, GY + 150, "a playa: a dry lake bed", tp, "#f5ecdc", 30)]
    els += [cloud(1120, 210, 300, tr_ - .3, "#9aa6b0", .95, "pop"), cloud(1380, 240, 240, tr_, "#8a96a2", .95, "pop")]
    els += rain(990, 1480, 260, 470, 22, tr_ + .4, BLUE, .04, 2.5, .8)
    w = poly([(996, GY + 6), (1080, GY + 68), (1360, GY + 68), (1444, GY + 6)], LAKE, "#9fd0ff", 2, ts + .2, fx="fill", curve=True)
    w["dur"] = 1.2
    els += [w, lab(1220, 300, "summer rains", ts, BLUE, 28)]
    els += [figure(880, GY, 110, th, "#2a2018"), cowg(800, GY, .5, th + .2, "#e8dcc6", horns="lyre", spots="#6a4a30"),
            cowg(1580, GY, .5, th + .4, "#cbb8a0", flip=True, horns="lyre"), figure(1640, GY, 104, th + .5, "#2a2018")]
    return {"base": "sky", "tod": "day", "ground": GY, "groundc": "#9c7e58", "sun": [1600, 170, 28], "ridges": [], "cam": CAM, "els": els}


def _gate_slabs(dx, dy, at, w=34, c="#d9c39a"):
    """A pair of upright slabs on the ring, either side of the gap facing (dx, dy)."""
    cx, cy = RING_C[0] + RING_R * dx, RING_C[1] + RING_R * dy
    out = []
    for side in (-1, 1):
        px, py = cx - side * 38 * dy, cy + side * 38 * dx
        out.append(rect(px - w / 2, py - w / 2, w, w, c, "#fff0d0", 1.5, 4, at, fx="pop"))
    return out


def s39():
    """The ring in plan: small stones in a circle about 4 m across; four pairs of upright slabs pop as gates; a blue dashed sightline through two
    gates runs north to south; a gold one through the other pair points to the midsummer sunrise."""
    tg, tl, tn, ts = T("s39", "four pairs"), T("s39", "Look through"), T("s39", "north to south"), T("s39", "sun rose")
    cx, cy = RING_C
    els = [circ(cx, cy, RING_R + 60, "#3a2e22", at=-1, op=.5), gl(cx, cy, 380, -1, .18, "lamp")]
    els += [circ(round(cx + RING_R * math.cos(2 * math.pi * k / 30), 1), round(cy + RING_R * math.sin(2 * math.pi * k / 30), 1), 10, "#9a8466", "#cbb79a", 1, -1)
            for k in range(30)]
    els += [ln([(cx - RING_R, 748), (cx + RING_R, 748)], -1, BONE, 2.5, draw=False), ln([(cx - RING_R, 734), (cx - RING_R, 762)], -1, BONE, 2.5, draw=False),
            ln([(cx + RING_R, 734), (cx + RING_R, 762)], -1, BONE, 2.5, draw=False), lab(cx + RING_R + 20, 758, "4 m", -1, BONE, 30, "start")]
    for j, (dx, dy) in enumerate(((0, -1), (0, 1), SUNRISE, (-SUNRISE[0], -SUNRISE[1]))):
        els += _gate_slabs(dx, dy, round(tg + .3 * j, 2))
    els += [lab(cx - RING_R - 34, cy + 64, "like gateposts", tg + 1.4, "#e8dcc6", 28, "end")]
    els += [ln([(cx, cy + RING_R + 50), (cx, 170)], tl + .4, BLUE, 4, "inferred", dur=1.2), lab(cx + 22, 196, "north to south", tn, BLUE, 28, "start")]
    sx, sy = cx + 600 * SUNRISE[0], cy + 600 * SUNRISE[1]
    els += [ln([(cx - 330 * SUNRISE[0], cy - 330 * SUNRISE[1]), (cx + 520 * SUNRISE[0], cy + 520 * SUNRISE[1])], ts - .4, GOLD, 4, "inferred", dur=1.2),
            gl(sx, sy, 170, ts + .4, .85, "sun"), circ(sx, sy, 24, "#ffe2a8", at=ts + .5, fx="pop"), lab(sx - 40, sy - 44, "midsummer sunrise", ts + .8, GOLD, 30, "end")]
    return {"base": "plan", "bg": "#2e241a", "cam": CAM, "els": els}


def s40():
    """In section: a chamber lined with clay and roofed, a cow lying in it, a soft light; a team hauls a slab on a rope across the sand; four standing
    stones up to 3 m tall, a person for scale."""
    tc, tl, ts, td = T("s40", "cattle were buried"), T("s40", "clay-lined"), T("s40", "stones nearly"), T("s40", "dragged across")
    GY = 560
    P = 150 / 1.7                                   # units per metre (a person is 1.7 m)
    els = [rect(-60, GY, 1960, 520, "#9c7e58", at=-1), rect(-60, GY + 170, 1960, 360, "#7a6248", at=-1, op=.8),
           ln([(-60, GY), (1900, GY)], -1, "rgba(255,226,190,.7)", 2, draw=False)]
    els += [poly([(150, GY + 6), (170, GY + 210), (560, GY + 210), (580, GY + 6)], "#2e2219", "#c9774a", 8, tc, fx="draw"),
            rect(130, GY - 16, 470, 22, "#b9a27e", "#e8d6b0", 1.5, 4, tl + .3, fx="pop"),
            gl(365, GY + 120, 170, tc + .4, .35, "lamp")] + [group(static(cow(370, GY + 196, 1.25, 0, "#d8c7ae", lying=True)), tc + .3, "pop")]
    els += [lab(365, GY - 52, "clay-lined chamber", tl + .2, "#5a2a14", 28, halo=False)]
    H = [2.9, 2.6, 2.8, 2.5]
    for k, h in enumerate(H):
        x = 1120 + 110 * k
        els.append(rect(x - 34, GY - h * P, 68, h * P, "#b9a27e", "#e8d6b0", 1.5, 8, round(ts + .25 * k, 2), fx="rise"))
    els += [ln([(1560, GY), (1560, GY - 3 * P)], ts + 1.2, BONE, 3, dur=.5), ln([(1546, GY - 3 * P), (1574, GY - 3 * P)], ts + 1.2, BONE, 3, draw=False),
            lab(1546, GY - 1.4 * P, "3 m", ts + 1.4, BONE, 32, "end"), figure(1630, GY, 150, ts + 1.0, "#2a2018")]
    els += [poly([(700, GY - 4), (700, GY - 50), (960, GY - 58), (968, GY - 4)], "#b9a27e", "#e8d6b0", 1.5, td, fx="rise"),
            ln([(968, GY - 30), (1010, GY - 70), (1060, GY - 76)], td + .3, "#e8d6b8", 3, dur=.4)]
    els += [figure(x, GY, 140, round(td + .4 + .15 * k, 2), "#2a2018") for k, x in enumerate((1010, 1060))]
    els += [arrow(R([(760, GY - 120), (880, GY - 160), (1000, GY - 170)]), td + .8, AMBER, 4, "known", .9), lab(860, GY - 190, "dragged into lines", td + 1.0, AMBER, 28)]
    return {"base": "sky", "tod": "day", "ground": GY, "groundc": "#9c7e58", "sun": [300, 200, 30], "ridges": [], "cam": CAM, "els": els}


def s41():
    """A time line from 6000 BCE to today: the Nabta ring about 4800 BCE or earlier (a dashed tail back); the first Stonehenge about 3000 BCE (a
    circular ditch and bank); at least eighteen centuries between them."""
    tf, tl = T("s41", "first Stonehenge"), T("s41", "at least")
    X = lambda yr: 200 + 1400 * (yr + 6000) / 8026
    AY = 580
    els = [axis(200, 1600, AY, [(X(-6000), "6000 BCE"), (X(-4000), "4000 BCE"), (X(-2000), "2000 BCE"), (X(0), "1 CE"), (X(2026), "today")], -1)]
    nx = X(-4800)
    els += [ln([(X(-5700), AY - 10), (nx, AY - 10)], -1, GOLD, 6, "inferred", draw=False), circ(nx, AY, 10, GOLD, at=-1),
            group([circ(nx + 30 * math.cos(2 * math.pi * k / 14), AY - 110 + 14 * math.sin(2 * math.pi * k / 14), 5, "#cbb79a") for k in range(14)] +
                  [rect(nx - 4, AY - 132, 8, 12, "#e8d6b0"), rect(nx - 4, AY - 100, 8, 12, "#e8d6b0")], -1),
            lab(nx, AY - 160, "the Nabta ring", -1, GOLD, 30), lab(X(-5700), AY - 30, "or earlier", -1, GOLD, 24, "start")]
    sx = X(-3000)
    els += [group([poly(E(sx, AY - 110, 52, 16, 30), "none", "#cbbca8", 4, curve=True), poly(E(sx, AY - 110, 40, 12, 30), "#5f7a3e", "none", 0, curve=True, op=.7)],
                  tf, "pop"), circ(sx, AY, 10, "#cbbca8", at=tf, fx="pop"), lab(sx, AY - 160, "the first Stonehenge", tf + .2, "#cbbca8", 30)]
    els += bracket(nx, sx, AY - 210, tl, None, AMBER) + [lab((nx + sx) / 2, AY - 240, "1,800 years or more", tl + .3, AMBER, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


ORION = [(700, 170), (900, 190), (780, 300), (812, 288), (844, 276), (720, 410), (880, 400)]   # Betelgeuse, Bellatrix, the belt, Saiph, Rigel
ORING_C = (780, 650)


def _orion_stone(k):
    x, y = ORION[k]
    return (ORING_C[0] + (x - 790) * .9, ORING_C[1] + (y - 290) * .22)


def s42():
    """Night over the ring: the stars of Orion above, dotted lines down to stones in the ring (the claim, 'a map of Orion?'); then the stars drift along
    an arc (precession) and the lines no longer meet their stones."""
    ts, to, tl, td, tm = T("s42", "little ring"), T("s42", "stars of Orion"), T("s42", "laid out"), T("s42", "stars drift"), T("s42", "one moment")
    cx, cy = ORING_C
    els = [poly(E(cx, cy, 320, 86, 48), "#2e241b", "#6a5640", 2, -1, curve=True)]
    els += [circ(round(cx + 300 * math.cos(2 * math.pi * k / 32), 1), round(cy + 76 * math.sin(2 * math.pi * k / 32), 1), 6, "#9a8466", at=-1) for k in range(32)]
    els += [gl(cx, cy, 300, ts, .25, "lamp")]
    els += [circ(x, y, 5.5, "#fff6e8", at=-1, op=.75) for x, y in ORION] + [gl(x, y, 30, -1, .45, "lamp") for x, y in ORION]
    els += [ln([ORION[a], ORION[b]], -1, "#cfc6e8", 1.2, draw=False, op=.35) for a, b in ((0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6))]
    for k, (x, y) in enumerate(ORION):
        els += [gl(x, y, 46, round(to + .1 * k, 2), .9, "lamp"), circ(x, y, 7 if k in (0, 6) else 5.5, "#fff6e8", at=round(to + .1 * k, 2), fx="pop")]
    els += [ln([ORION[a], ORION[b]], to + .8, "#cfc6e8", 1.5, dur=.5) for a, b in ((0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6))]
    for k in range(7):
        sx, sy = _orion_stone(k)
        els += [rect(sx - 9, sy - 9, 18, 18, "#b9a27e", "#e8d6b0", 1.2, 3, round(tl + .08 * k, 2), fx="pop"),
                ln([ORION[k], (sx, sy - 12)], round(tl + .3 + .1 * k, 2), LILAC, 2.2, "claimed", dur=.6)]
    els += [lab(1260, 220, "a map of Orion?", to + .6, LILAC, 34, st="serif")]
    D = (70, 34)
    for k, (x, y) in enumerate(ORION):
        els += [ring(x, y, 12, round(td + .1 * k, 2), "#cfc6e8", 2, "inferred", .3),
                arrow(R([(x + 10, y + 5), (x + D[0] - 10, y + D[1] - 5)]), round(td + .3 + .08 * k, 2), "#cfc6e8", 2.2, "known", .4, curve=False),
                circ(x + D[0], y + D[1], 6, "#fff6e8", at=round(td + .6 + .08 * k, 2), fx="pop")]
    els += [lab(1260, 290, "stars drift over the centuries", td + .8, "#cfc6e8", 28), lab(1260, 340, "a line fits one moment", tm, "#cfc6e8", 28)]
    return {"base": "dark", "stars": 140, "cam": CAM, "els": els}


def s43_add():
    """The excavators' reply: a short time line, the star dates and, about 1,500 years later, the big stones; one stone's old place dashed and a red
    arrow to where it lies now, 'moved?'."""
    te, tsd, tbs, tmv = T("s43", "excavators"), T("s43", "star dates"), T("s43", "big stones"), T("s43", "may have moved")
    els = [rect(1170, 470, 500, 200, "rgba(14,11,9,.8)", "rgba(255,236,206,.25)", 1.5, 14, te, fx="pop"),
           ln([(1220, 590), (1620, 590)], te + .2, "#8c7152", 3, dur=.5), circ(1250, 590, 10, LILAC, at=tsd, fx="pop"), lab(1250, 636, "star dates", tsd + .2, LILAC, 26),
           circ(1590, 590, 10, GOLD, at=tbs, fx="pop"), lab(1590, 636, "big stones", tbs + .2, GOLD, 26)]
    els += arc_br(1262, 1578, 570, 46, tbs + .3, "1,500 years", BONE, 28)
    sx, sy = _orion_stone(6)
    els += [rect(sx - 9, sy - 9, 18, 18, "none", "#e8d6b0", 1.5, 3, tmv, style="inferred", fx="pop"),
            rect(sx + 52, sy + 18, 18, 18, "#b9a27e", "#e8d6b0", 1.2, 3, tmv + .3, fx="pop"),
            arrow(R([(sx + 10, sy + 4), (sx + 48, sy + 22)]), tmv + .2, RED, 3, "known", .4, curve=False), lab(sx + 70, sy + 76, "moved?", tmv + .5, RED, 28)]
    return els


def s44_add():
    """Back at the ring: the midsummer sun glows at its gate; a grey rain cloud drifts in; a small dotted Orion in the corner is struck out."""
    tw, tr_, tsm = T("s44", "watch the sun"), T("s44", "ask for rain"), T("s44", "star maps")
    cx, cy = RING_C
    sx, sy = cx + 600 * SUNRISE[0], cy + 600 * SUNRISE[1]
    els = [gl(sx, sy, 300, tw, .7, "sun"), gl(cx, cy, 300, tw + .3, .3, "lamp")]
    els += [cloud(470, 200, 280, tr_, "#7d8794", .95, "pop")] + rain(380, 570, 240, 330, 9, tr_ + .4, BLUE, .05, 2.5, .8) + \
        [lab(470, 400, "and ask for rain?", tr_ + .4, BLUE, 28)]
    mini = [(210, 560), (290, 572), (238, 622), (250, 618), (262, 614), (218, 680), (282, 676)]
    els += [group([circ(x, y, 5, "#fff6e8", "none", 0, style="claimed") for x, y in mini] +
                  [ln([mini[a], mini[b]], -1, LILAC, 1.6, "claimed", draw=False) for a, b in ((0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6))], tsm, "pop"),
            lab(250, 730, "star maps", tsm + .2, LILAC, 26), ln([(170, 700), (330, 540)], tsm + .6, RED, 6, dur=.4)]
    return els


# ================================================================== chapter 6: when the rain stopped
def wide_land(m, at=-1, landc=LAND):
    """The land of map m drawn well beyond its box (no clipping edge shows in a 16:9 panel)."""
    return land_el(m.land(pad=30), at, landc)


def s45():
    """The map of the monsoon after the retreat (the card has said it): the green back in the Sahel, its old reach dashed, the rain belt in the
    south, the monsoon arrows shorter; then a big light switch over the desert, 'overnight?'."""
    tq = T("s45", "switch off")
    m = Map(*MON, rect=(90, 130, 1600, 660))
    sah = m.path(SAHARA)
    els = [wide_land(m), poly(sah, "#c9a46e", "rgba(255,226,190,.4)", 1.5, -1, op=.55, curve=True)]
    old = [m.p(lo, 11.0) for lo in range(-15, 33, 4)] + [m.p(lo, 22.5 + 1.6 * math.sin(lo / 5)) for lo in range(31, -16, -4)]
    now = [m.p(lo, 8.6) for lo in range(-12, 31, 3)] + [m.p(lo, 14.0 + .8 * math.sin(lo / 5)) for lo in range(30, -16, -3)] + [m.p(-15.5, 11.5)]
    els += [poly(old, "none", "#9fbf7a", 2.5, -1, curve=True, style="inferred"), poly(now, "#7d9a5a", at=-1, op=.55, curve=True)]
    els += [poly([m.p(lo, 13.2 + 1.2 * math.sin(math.radians(lo * 9))) for lo in range(-15, 31, 2)] +
                 [m.p(lo, 10.4 + 1.2 * math.sin(math.radians(lo * 9))) for lo in range(29, -16, -2)], "rgba(159,208,255,.30)", BLUE, 2, -1, curve=True)]
    for k, lo in enumerate((-12, -5, 2, 9, 16)):
        els.append(arrow(R([m.p(lo - 3, 0.5), m.p(lo - 1.5, 4.0), m.p(lo - .5, 7.5)]), -1, BLUE, 6, "known", .1))
    for lo in (-6, 6, 18):
        els.append(arrow(R([m.p(lo, 21.5), m.p(lo, 16.0)]), -1, "#9fbf7a", 3, "inferred", .1, curve=False))
    cx, cy = m.p(8, 22.5)
    els += [group([rect(cx - 70, cy - 105, 140, 210, "#efe6d2", "#8a7a66", 3, 18), rect(cx - 30, cy - 60, 60, 120, "#2a2018", r=10),
                   rect(cx - 24, cy + 4, 48, 50, "#cbbca8", "#fff6e6", 1.5, 8)], tq, "pop"),
            lab(cx + 120, cy + 10, "?", tq + .4, LILAC, 90, st="big", fx="pop"), lab(cx, cy + 160, "overnight?", tq + .5, LILAC, 34, st="serif")]
    return {"base": "map", "cam": CAM, "els": els}


def s46():
    """Water in section: specks of mud and dust fall and settle on the bottom in thin layers, year after year, like the pages of a diary (an open
    book); a hollow tube is pushed down through the layers: a sediment core."""
    tm, tb, ty, td = T("s46", "Mud and dust"), T("s46", "bottom of seas"), T("s46", "year after year"), T("s46", "pages of a diary")
    W0, W1, T0, B0 = 180, 900, 170, 700
    els = [rect(W0, T0, W1 - W0, B0 - T0, "#1f4d62", "rgba(159,208,255,.4)", 2, 0, -1), rect(W0, T0, W1 - W0, 24, "#3f7f9c", at=-1, op=.8),
           rect(W0, B0, W1 - W0, 80, "#4a3a2c", at=-1)]
    r = random.Random(46)
    els += [circ(r.uniform(W0 + 20, W1 - 20), r.uniform(T0 + 40, B0 - 120), r.uniform(2, 4), r.choice(("#c9a46e", "#e2c48e", "#a8977c")),
                 at=round(tm + .05 * k, 2), fx="pop", op=.85) for k in range(40)]
    cols = ("#8a7050", "#c9b48e", "#6f5a44", "#b9ab94", "#5a4632", "#a8977c", "#7a6248")
    for k, c in enumerate(cols):
        e = rect(W0, B0 - 20 * (k + 1), W1 - W0, 20, c, at=round(tb + .5 + .5 * k, 2), fx="fill")
        e["dur"] = .5
        els.append(e)
    els += [lab(W0 + 30, B0 - 160, "mud and dust", tb + .4, "#e2c48e", 28, "start")]
    BX, BY = 1300, 420
    pages = [poly([(BX - 230, BY - 130), (BX - 10, BY - 110), (BX - 10, BY + 140), (BX - 230, BY + 120)], "#efe6d2", "#8a7a66", 2, curve=False),
             poly([(BX + 230, BY - 130), (BX + 10, BY - 110), (BX + 10, BY + 140), (BX + 230, BY + 120)], "#f5ecdc", "#8a7a66", 2)]
    pages += [ln([(BX - 200, BY - 80 + 30 * j), (BX - 40, BY - 66 + 30 * j)], -1, "#a8977c", 2, draw=False) for j in range(7)]
    pages += [ln([(BX + 40, BY - 66 + 30 * j), (BX + 200, BY - 80 + 30 * j)], -1, "#a8977c", 2, draw=False) for j in range(7)]
    els += [group(pages, td - .2, "pop"), lab(BX, BY + 210, "like a diary", td + .2, BONE_E, 30)]
    els += [rect(520, 120, 46, 600, "rgba(245,236,220,.08)", BONE, 3, 6, td + .9, fx="draw"), arrow(R([(543, 90), (543, 150)]), td + .9, BONE, 3, "known", .3, curve=False)]
    return {"base": "dark", "cam": CAM, "els": els}


def s47():
    """Two records: a map strip with the dust core off Mauritania and Lake Yoa in Chad; a graph from 8,000 to 3,000 years ago: the dust record drops
    like a cliff about 5,500 years ago, within decades to centuries; Lake Yoa slopes down slowly, its trees thinning over thousands of years."""
    tm, tj, tw, ty, tt = T("s47", "coast of Mauritania"), T("s47", "jumps about"), T("s47", "within decades"), T("s47", "called Yoa"), T("s47", "trees thin")
    m = Map(-24, 34, 14, 22, rect=(100, 130, 1580, 230))
    mx, my = m.p(-18.58, 20.75)
    yx, yy = m.p(20.52, 19.05)
    els = [inset_map(m, 100, 130, 1580, 230, -1, extra=[poly(m.path(SAHARA), "#c9a46e", "none", 0, -1, op=.35, curve=True),
                                                        pin(mx, my, "off Mauritania", tm, RED, "start", 14, 8), pin(yx, yy, "Lake Yoa, Chad", ty, GREEN, "start", 14, 8)])]
    X = lambda ya: 280 + 1300 * (8000 - ya) / 5000
    WET, DRY, AY = 420, 680, 730
    els += [axis(280, 1580, AY, [(X(8000), "8,000 years ago"), (X(5500), "5,500"), (X(3000), "3,000")], -1),
            lab(250, WET + 10, "wet", -1, GREEN, 30, "end"), lab(250, DRY + 10, "dry", -1, "#e8b87a", 30, "end"),
            ln([(280, WET), (1580, WET)], -1, "#5a4a3a", 1.5, "inferred", draw=False), ln([(280, DRY), (1580, DRY)], -1, "#5a4a3a", 1.5, "inferred", draw=False)]
    els += [ln([(X(8000), WET), (X(5560), WET), (X(5440), DRY), (X(3000), DRY)], tj, RED, 6, dur=2.0),
            lab(X(5440) - 26, (WET + DRY) / 2 + 70, "within decades to centuries", tw, RED, 28, "end")]
    els += [ln([(X(8000), WET + 14), (X(6000), WET + 26), (X(4500), WET + 160), (X(3000), DRY - 14)], ty + .4, GREEN, 6, dur=2.2, curve=True)]
    els += [lab(X(4300) + 30, WET + 150, "its trees thin out", tt, GREEN, 28, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def _step_icon(x, y, at, c=RED, s=1.0):
    return [ln([(x - 34 * s, y - 20 * s), (x - 4 * s, y - 20 * s), (x + 4 * s, y + 20 * s), (x + 34 * s, y + 20 * s)], at, c, 5, dur=.5)]


def _ramp_icon(x, y, at, c=GREEN, s=1.0):
    return [ln([(x - 34 * s, y - 20 * s), (x + 34 * s, y + 20 * s)], at, c, 5, dur=.5)]


def s48():
    """The best answer so far, on a map: sudden in some places (cliff icons off Mauritania and at Lake Mega-Chad), slow in others (a ramp at Lake
    Yoa), and later the further south you go (a broad arrow from north to south, 'earlier', 'later')."""
    ts, tl, tg = T("s48", "sudden in some"), T("s48", "slow in others"), T("s48", "later the further")
    m = Map(*NAF, rect=(90, 130, 1600, 640))
    els = [wide_land(m), poly(m.path(SAHARA), "#c9a46e", "rgba(255,226,190,.4)", 1.5, -1, op=.5, curve=True), ln(m.path(NILE), -1, "#6fb6d6", 3, draw=False, curve=True)]
    for k, (lo, la) in enumerate(((-18.58, 20.75), (14.5, 13.6))):
        x, y = m.p(lo, la)
        els += [circ(x, y, 46, "rgba(18,13,10,.75)", RED, 2.5, round(ts + .3 * k, 2), fx="pop")] + _step_icon(x, y, round(ts + .3 * k + .1, 2), RED, .9)
    els += [lab(m.p(-18.58, 20.75)[0], m.p(-18.58, 20.75)[1] + 82, "sudden", ts + .4, RED, 28)]
    x, y = m.p(20.52, 19.05)
    els += [circ(x, y, 46, "rgba(18,13,10,.75)", GREEN, 2.5, tl, fx="pop")] + _ramp_icon(x, y, tl + .1, GREEN, .9) + [lab(x, y + 82, "slow", tl + .3, GREEN, 28)]
    ax0, ay0 = m.p(3.5, 33.0)
    ax1, ay1 = m.p(3.5, 11.0)
    els += [poly([(ax0 - 34, ay0), (ax0 + 34, ay0), (ax1 + 34, ay1 - 70), (ax1 + 70, ay1 - 70), (ax1, ay1), (ax1 - 70, ay1 - 70), (ax1 - 34, ay1 - 70)],
                 "rgba(232,184,122,.25)", AMBER, 2.5, tg, fx="pop"),
            lab(ax0 + 54, ay0 + 24, "earlier", tg + .3, AMBER, 30, "start"), lab(ax1 + 84, ay1 - 40, "later", tg + .6, AMBER, 30, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def s49_add():
    """Back at the Mega-Chad map: the big lake falls (its bed left pale), today's Lake Chad and a smaller lake in the Bodele basin remain, about 5,000
    years ago; then the Bodele dries, about 1,000 years ago, and dust blows out of it to the west and south-west: the biggest dust source on Earth."""
    tf, t5, tb, t1, td = T("s49", "fell fast"), T("s49", "five thousand"), T("s49", "the Bodélé"), T("s49", "a thousand years"), T("s49", "biggest single")
    m = Map(*CHAD_M, rect=CHAD_R)
    bed = poly(m.path(MEGA_A), "#8c7a5c", "#b8a47e", 1.5, tf, op=.94, curve=True)
    bed["dur"] = 1.4
    els = [bed, poly(m.path(CHAD), LAKE, "#9fd0ff", 1.5, tf + .5), poly(m.path(BODELE), LAKE, "#9fd0ff", 1.5, tf + .5, curve=True)]
    els += [lab(*m.p(9.3, 11.8), "about 5,000 years ago", t5, BONE, 28, "end")]
    bx, by = m.p(17.5, 17.2)
    els += [gl(bx, by, 90, tb, .6, "blue"), lab(bx + 70, by - 40, "the Bodélé", tb, "#cfe6ff", 28, "start")]
    els += [poly(m.path(BODELE), "#d8c8a0", "#efe0c0", 1.5, t1 + .2, curve=True, fx="pop"), lab(*m.p(14.6, 19.9), "about 1,000 years ago", t1 + .4, GOLD, 28, "end")]
    for k, (dx, dy) in enumerate(((-310, -28), (-350, 32), (-320, 92))):
        els.append(arrow(R([(bx - 20, by + 6 * k), (bx + dx * .5, by + dy * .4 + 10), (bx + dx, by + dy)]), round(td + .25 * k, 2), "#e2c48e", 5, "inferred", 1.0))
    els += [gl(bx - 200, by + 60, 220, td + .3, .35, "lamp"), lab(362, 283, "the biggest dust source", td + .8, "#e2c48e", 28),
            lab(362, 316, "on Earth", td + .9, "#e2c48e", 28)]
    return els


def s50():
    """Herders and cattle on a strip of grass; above them a time bar of the green Sahara's end (about 5,000 years ago); a dashed red arrow pulls the
    end earlier, 'sooner?'; a green arrow pushes it about 500 years later."""
    ts, tm, t5 = T("s50", "sped up"), T("s50", "One model"), T("s50", "five hundred")
    X = lambda ya: 300 + 1200 * (8000 - ya) / 5000
    BY = 330
    els = [axis(300, 1500, 400, [(X(8000), "8,000 years ago"), (X(5000), "5,000"), (X(3000), "3,000")], -1),
           band(X(8000), X(5000), BY - 13, 26, GREEN, -1, dur=.1), lab((X(8000) + X(5000)) / 2, BY - 30, "the green Sahara", -1, GREEN, 28),
           ln([(X(5000), BY - 40), (X(5000), BY + 40)], -1, BONE, 4, draw=False), lab(X(5000) + 14, BY - 52, "its end", -1, BONE, 26, "start")]
    els += [arrow(R([(X(5000) - 6, 480), (X(5000) - 96, 480)]), ts, RED, 5, "inferred", .5, curve=False), lab(X(5000) - 60, 526, "sooner?", ts + .3, RED, 28)]
    els += [arrow(R([(X(5000) + 6, 480), (X(4500), 480)]), tm + .6, GREEN, 5, "known", .5, curve=False),
            lab(X(4500) + 20, 490, "later: about 500 years?", t5, GREEN, 28, "start")]
    GY = 700
    els += [rect(160, GY - 6, 1460, 46, "#55703a", at=-1, r=20)] + tufts(180, 1600, GY, 30, -1, "#7d9a5a", 20, seed=50)
    els += [cowg(560 + 140 * k, GY, .5, -1, ("#e8dcc6", "#cbb8a0", "#d8c7ae")[k % 3], flip=bool(k % 2), horns="lyre", spots="#6a4a30" if k % 2 == 0 else None)
            for k in range(5)]
    els += [figure(440, GY, 110, -1, "#2a2018", None), figure(1300, GY, 104, -1, "#2a2018", None)]
    return {"base": "dark", "cam": CAM, "els": els}


DAKHLA, KHARGA, UWEINAT = (29.0, 25.5), (30.55, 25.45), (25.0, 21.9)


def s51():
    """The eastern Sahara: herders' camps; as the rains fail, arrows lead away: to the highlands of the Gilf Kebir and Jebel Uweinat, to the oases of
    Dakhla and Kharga, south towards the Sahel, and east to the Nile, which glows."""
    tl, th, to, ts, tn = T("s51", "herders left"), T("s51", "highlands"), T("s51", "oases"), T("s51", "the south"), T("s51", "the Nile")
    m = Map(21, 37, 17.5, 28.5, rect=(90, 120, 1600, 680))
    els = [wide_land(m), ln(m.path(NILE), -1, "#6fb6d6", 4, draw=False, curve=True)]
    r = random.Random(51)
    camps = []
    while len(camps) < 14:
        lo, la = r.uniform(26.6, 30.4), r.uniform(20.6, 24.8)
        if all(abs(lo - a_) > .5 or abs(la - b_) > .5 for a_, b_ in camps):
            camps.append((lo, la))
    cx, cy = m.p(28.5, 22.7)
    els += [gl(cx, cy, 240, -1, .3, "lamp")] + [circ(*m.p(lo, la), 8, "#f2c98e", at=-1, op=.9) for lo, la in camps]
    els += [lab(cx - 110, cy + 130, "herders' camps", -1, "#f2c98e", 28, "end")]
    els += [poly(m.path(EGYPT_GILF), "#6a5440", "#9a8064", 1.5, -1, curve=True), poly(E(*m.p(*UWEINAT), 30, 26, 14), "#6a5440", "#9a8064", 1.5, -1, curve=True)]
    gx, gy = m.p(25.9, 23.5)
    ux, uy = m.p(*UWEINAT)
    els += [arrow(R([(cx - 40, cy - 10), (gx + 34, gy + 4)]), th, AMBER, 4, "known", .5), arrow(R([(cx - 30, cy + 20), (ux + 30, uy - 6)]), th + .2, AMBER, 4, "known", .5),
            lab(gx - 44, gy - 30, "highlands", th + .4, AMBER, 30, "end")]
    dx, dy = m.p(*DAKHLA)
    kx, ky = m.p(*KHARGA)
    els += [circ(dx, dy, 12, GREEN, at=to, fx="pop"), circ(kx, ky, 12, GREEN, at=to + .1, fx="pop"),
            arrow(R([(cx - 6, cy - 34), (dx, dy + 20)]), to, AMBER, 4, "known", .5), arrow(R([(cx + 20, cy - 30), (kx - 8, ky + 18)]), to + .2, AMBER, 4, "known", .5),
            lab((dx + kx) / 2, dy - 30, "oases", to + .4, GREEN, 30)]
    sx, sy = m.p(28.0, 18.2)
    els += [arrow(R([(cx - 6, cy + 40), (sx, sy)]), ts, AMBER, 4, "known", .6), lab(sx + 24, sy + 26, "south", ts + .3, AMBER, 30, "start")]
    nx, ny = m.p(32.7, 23.4)
    els += [arrow(R([(cx + 40, cy + 6), (nx - 16, ny + 6)]), tn, AMBER, 5, "known", .6), ln(m.path(NILE), tn + .3, "#bfe6ff", 7, dur=1.0, curve=True, op=.7),
            gl(nx, ny, 170, tn + .4, .55, "blue"), lab(nx + 30, ny - 10, "the Nile", tn + .5, "#cfe6ff", 30, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def _herd_pan(drought):
    def f(ex, fy, at):
        if drought:
            return [poly([(ex - 150, fy), (ex + 150, fy), (ex + 124, fy - 26), (ex - 124, fy - 26)], "#c9a46e", at=at),
                    cowg(ex + 40, fy - 4, .6, at, "#e8dcc6", horns="lyre", spots="#6a4a30"), figure(ex - 60, fy - 4, 104, at, "#2a2018", None),
                    arrow(R([(ex - 300, fy - 170), (ex - 210, fy - 150), (ex - 110, fy - 100)]), at + .3, AMBER, 3, "inferred", .6)]
        return [poly([(ex - 150, fy), (ex + 150, fy), (ex + 124, fy - 26), (ex - 124, fy - 26)], "#55703a", at=at), ln([(ex - 140, fy - 36), (ex + 140, fy - 42)], at, "#6fb6d6", 7, draw=False),
                cowg(ex - 40, fy - 4, .58, at, "#d8c7ae", horns="lyre"), cowg(ex + 70, fy - 4, .52, at, "#e8dcc6", flip=True, horns="lyre", spots="#4a3424")]
    return f


def s52():
    """A balance: left pan, a herder and cattle arriving from the desert on a dashed arrow, 'pushed by drought'; right pan, cattle already on a green
    strip by the blue Nile, 'already on the Nile'. It tilts one way, then settles level: Egypt's first kingdoms?"""
    tt, tk, to, tn = T("s52", "Some archaeologists"), T("s52", "first kingdoms"), T("s52", "Others say"), T("s52", "along the Nile")
    cx, py, L, BY = 889, 300, 980, 760
    els = balance(cx, py, L, -7, BY, tt, _herd_pan(True), None, 200, 330)
    els += [lab(cx, 160, "Egypt's first kingdoms?", tk, BONE_E, 34, st="serif")]
    els += [dveil(80, 196, 1640, 600, to - .2, .99)]
    els += balance(cx, py, L, 0, BY, to + .1, _herd_pan(True), _herd_pan(False), 200, 330)
    lx, rx = cx - L / 2, cx + L / 2
    els += [lab(lx, py + 270, "pushed by drought", to + .3, AMBER, 30), lab(rx, py + 270, "already on the Nile", tn, BLUE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


GARAMA = (12.78, 26.55)
FEZZAN = [(10, 28.3), (13, 28.6), (16, 27.6), (16.2, 25.2), (14, 24.2), (11, 24.4), (9.6, 26)]


def s53():
    """Left: a map of Libya, Fezzan outlined, Garama pinned. Right: a mud-brick oasis town at dusk, date palms and fields, a small mud-brick pyramid tomb
    beside it."""
    tf, tg, tt = T("s53", "Libya's Fezzan"), T("s53", "the Garamantes"), T("s53", "first towns")
    m = Map(8, 26, 19, 34, rect=(100, 150, 480, 430))
    gx, gy = m.p(*GARAMA)
    fx_, fy_ = m.p(12.8, 25.4)
    els = [inset_map(m, 100, 150, 480, 430, -1, extra=[lab(*m.p(20, 29.5), "Libya", -1, "#e8dcc6", 28),
                                                       poly(m.path(FEZZAN), "rgba(232,184,122,.18)", "#e8b87a", 2.5, -1, curve=True, style="inferred"),
                                                       lab(fx_, fy_ + 50, "Fezzan", -1, "#e8b87a", 26), pin(gx, gy, "Garama", -1, GOLD, "start", 14, 8)])]
    els += [gl(gx, gy, 70, tf, .7, "lamp")]
    GY = 650
    els += [town(820, GY, 1.25, -1)] + [palm(760 + 100 * k + (40 if k > 2 else 0), GY + 2, 110 + 14 * (k % 2), -1) for k in range(6)]
    els += [rect(700 + 150 * k, GY + 22, 130, 26, "#55703a", "#7d9a5a", 1, 4, -1) for k in range(6)]
    els += [mud_pyramid(1500, GY, 130, -1), gl(1100, 560, 420, -1, .25, "lamp")]
    els += [lab(1130, 300, "the Garamantes", tg, BONE_E, 38, st="serif"), lab(1130, 760, "the first towns of the central Sahara", tt, GOLD, 30)]
    return {"base": "sky", "tod": "dusk", "ground": GY, "groundc": "#6a5038", "sun": [1560, 470, 30], "ridges": [], "cam": CAM, "els": els}


FOG_SURF = [(-60, 360), (300, 380), (700, 450), (1100, 540), (1420, 640), (1900, 680)]


def _surf_y(x):
    for (x0, y0), (x1, y1) in zip(FOG_SURF, FOG_SURF[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return FOG_SURF[-1][1]


FOG_TUN = lambda x: 610 + 40 * (x - 300) / 1120         # the tunnel: a gentle slope from the groundwater to the oasis
AQ_EDGE = [(600, 660), (660, 720), (720, 800), (800, 900), (880, 1060)]    # the aquifer's downslope edge (below the water table's end)
FOG_SHAFTS = [440, 580, 720, 860, 1000, 1140, 1280]


def s54():
    """A cut through a gentle slope: grey clouds of long ago rain into the ground, which holds it as groundwater; a tunnel slopes gently from it to fields
    and palms at the foot; a line of shafts from the surface down to the tunnel, a digger in one: a foggara."""
    tr_, tw, tt, ts, tf = T("s54", "fallen as rain"), T("s54", "thousands of years"), T("s54", "They reached"), T("s54", "hand-dug"), T("s54", "called foggaras")
    els = [poly(FOG_SURF + [(1900, 1060), (-60, 1060)], "#8a6b45", "rgba(255,226,190,.5)", 2, -1), poly([(-60, 760), (1900, 860), (1900, 1060), (-60, 1060)], "#6a5238", at=-1, op=.7)]
    WT = [(-60, 560), (520, 620)]
    els += [poly(WT + AQ_EDGE + [(-60, 1060)], "rgba(79,147,179,.55)", at=-1), ln(WT, -1, BLUE, 3, "inferred", draw=False),
            lab(130, 790, "groundwater", -1, "#cfe6ff", 28, "start")]
    els += [cloud(230, 170, 260, tr_ - .3, "#8a96a2", .8, "pop"), cloud(470, 150, 220, tr_, "#7d8794", .8, "pop")]
    els += [ln([(150 + 40 * j, 230), (140 + 40 * j, 330)], round(tr_ + .3 + .05 * j, 2), BLUE, 2.5, "inferred", dur=.4) for j in range(9)]
    els += [arrow(R([(200 + 140 * j, 410), (210 + 140 * j, 540)]), round(tr_ + .9 + .2 * j, 2), BLUE, 3, "inferred", .5, curve=False) for j in range(3)]
    els += [lab(640, 230, "rain, thousands of years ago", tw, "#cfe6ff", 28, "start")]
    els += [ln([(300, FOG_TUN(300)), (1420, FOG_TUN(1420))], tt, "#2a2019", 14, draw=False), ln([(300, FOG_TUN(300)), (1420, FOG_TUN(1420))], tt + .5, BLUE, 5, dur=1.4)]
    els += [rect(1430, 640, 280, 14, "#55703a", at=tt + 1.0, r=4, fx="pop")] + [palm(1470 + 70 * k, 642, 96 - 10 * (k % 2), tt + 1.1 + .1 * k) for k in range(4)]
    for k, x in enumerate(FOG_SHAFTS):
        at = round(ts + .2 * k, 2)
        els += [ln([(x, _surf_y(x)), (x, FOG_TUN(x))], at, "#2a2019", 9, draw=False), poly(E(x, _surf_y(x) - 4, 22, 8, 12), "#a88a5c", at=at, fx="pop")]
    els += [figure(720, FOG_TUN(720) - 4, 44, tf - .4, "#e8d6b8"), lab(900, 760, "a foggara", tf, BONE_E, 32)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": [1600, 220, 28], "ridges": [], "cam": CAM, "els": els}


def s55_add():
    """A savings account with no deposits: a glass jar of water in the sky, a coin slot struck out, its level falling; the water table sinks below the
    tunnel; the tunnel runs dry; the fields turn brown."""
    tf, ta, tn, tw, tc = T("s55", "fossil water"), T("s55", "savings account"), T("s55", "no new deposits"), T("s55", "water table sank"), T("s55", "canals ran dry")
    JX, JY = 1220, 170
    els = [rect(JX, JY, 160, 210, "rgba(159,208,255,.10)", "#e9f2f8", 3, 20, ta - .2, fx="pop"), rect(JX + 8, JY + 70, 144, 132, BLUE, at=ta, r=14, op=.85),
           ln([(JX + 50, JY - 4), (JX + 110, JY - 4)], ta + .2, "#e9f2f8", 7, draw=False), circ(JX + 80, JY - 30, 16, GOLD, "#fff1d2", 1.5, ta + .3, fx="pop")]
    els += [ln([(JX + 30, JY + 20), (JX + 130, JY - 40)], tn, RED, 6, dur=.4), lab(JX + 190, JY + 40, "no new deposits", tn + .2, RED, 28, "start")]
    els += [rect(JX + 8, JY + 70, 144, 74, "#8aa3b8", at=tn + .6, r=10, op=.96)]
    WT2 = [(-60, 700), (600, 790)]
    els += [poly([(-62, 548), (522, 606), (606, 652), (668, 714), (724, 798), (600, 790), (-62, 700)], "#8a6b45", at=tw, op=1.0),
            ln(WT2, tw + .4, BLUE, 3, "inferred", dur=.8)]
    els += [arrow(R([(x, 580 + .1 * x), (x, 680 + .1 * x)]), round(tw + .2 + .2 * k, 2), BLUE, 3, "known", .4, curve=False) for k, x in enumerate((60, 220, 380))]
    els += [ln([(300, FOG_TUN(300)), (1420, FOG_TUN(1420))], tc, "#7a6248", 7, dur=1.4), rect(1430, 640, 280, 14, "#a88a5c", at=tc + 1.2, r=4, fx="pop")]
    return els


def s56_add():
    """Dusk: the sky reddens over the dry foggara; the last drop of blue at the outlet goes out; the empty shafts stand in a row."""
    t0 = T("s56", "last gift")
    sky = [(-60, -60), (1900, -60), (1900, 680)] + FOG_SURF[::-1]
    return [poly(sky, "#b8503a", at=t0, op=.42), circ(1428, 646, 9, BLUE, at=-1), circ(1428, 646, 11, "#a88a5c", at=t0 + 1.2, fx="pop"),
            gl(1428, 640, 90, t0 + .2, .4, "red")] + [gl(x, _surf_y(x) - 6, 40, round(t0 + .5 + .1 * k, 2), .5, "lamp") for k, x in enumerate(FOG_SHAFTS)]


# ================================================================== the weighing
LROWS = [222, 332, 442, 552, 662]


def lrow(y, at, pic, text, grade=None, gt=None, gc=None, size=30, h=94, lit=True):
    """A row of the ledger: a small picture, the claim, and (when it is graded) its chip."""
    fill, edge = ("rgba(242,201,142,.08)", "rgba(242,201,142,.3)") if lit else ("rgba(242,201,142,.03)", "rgba(242,201,142,.14)")
    out = [rect(140, y - h / 2, 1500, h, fill, edge, 1.5, 12, at, fx="pop"), lab(310, y + 11, text, at + .1, BONE if lit else DIM, size, "start")]
    if lit:
        out += pic(220, y, at + .1)
    if grade:
        out += chip(1080, y, grade, gc, gt, 30, "start")
    return out


def pic_lake(x, y, at):
    return [poly(E(x, y + 18, 62, 20, 24), LAKE, "#9fd0ff", 1.5, at, curve=True, fx="pop")] + hippo_head(x + 6, y + 18, .3, at, -1, False)


def pic_orbit(x, y, at):
    return [group([circ(x - 40, y, 13, "#ffe2a8"), poly(E(x + 4, y, 56, 20, 30), "none", "#8c7152", 2, curve=True, style="inferred"), circ(x + 58, y + 4, 8, "#2f5f7a", "#9fd0ff", 1.5)],
                  at, "pop")]


def pic_dna(x, y, at):
    return helix(x - 56, y - 10, x + 56, y - 10, at, n=7, amp=11, w=2.5, dur=.4) + [gl(x - 12, y + 26, 30, at + .2, .8, "lamp"), gl(x + 14, y + 26, 30, at + .2, .8, "lamp")]


def pic_ring(x, y, at):
    return [group([circ(x - 8 + 30 * math.cos(2 * math.pi * k / 12), y + 6 + 22 * math.sin(2 * math.pi * k / 12), 4, "#cbb79a") for k in range(12)] +
                  [circ(x + 50, y - 22, 10, "#ffe2a8")], at, "pop"), gl(x + 50, y - 22, 40, at, .7, "sun")]


def pic_cliff_ramp(x, y, at):
    return [ln([(x - 66, y - 18), (x - 30, y - 18), (x - 24, y + 22), (x - 2, y + 22)], at, RED, 4, dur=.4),
            ln([(x + 14, y - 18), (x + 70, y + 22)], at + .2, GREEN, 4, dur=.4)]


def pic_groups(x, y, at):
    return [figure(x - 50 + 22 * k, y + 34, 60, at, BLUE if k < 2 else GOLD, "pop") for k in range(2)] + \
           [figure(x + 20 + 22 * k, y + 34, 60, at, GOLD, "pop") for k in range(2)]


def pic_swimmer(x, y, at):
    return [rot_swimmer(x, y + 4, 1.3, at, "#c8643c", -4)]


def pic_nile(x, y, at):
    return [ln([(x - 70, y - 14), (x - 30, y - 4), (x + 10, y - 16), (x + 70, y - 6)], at, "#6fb6d6", 5, dur=.4, curve=True),
            cowg(x + 20, y + 34, .34, at, "#e8dcc6", horns="lyre"), figure(x - 36, y + 34, 54, at, "#e8d6b8", "pop")]


def pic_shaft(x, y, at):
    surf = [(x - 72, y - 20), (x + 72, y + 14)]
    return [group([poly(surf + [(x + 72, y + 42), (x - 72, y + 42)], "#a8865a"), ln(surf, -1, "#efe0c0", 1.5, draw=False)] +
                  [ln([(x + dx, y - 20 + 34 * (dx + 72) / 144), (x + dx, y + 30)], -1, "#2a2019", 4, draw=False) for dx in (-46, -10, 26)] +
                  [ln([(x - 64, y + 30), (x + 70, y + 34)], -1, "#2a2019", 4, draw=False), ln([(x - 64, y + 30), (x - 20, y + 31)], -1, BLUE, 3, draw=False)],
                  at, "pop")]


def pic_roundhead(x, y, at):
    return [roundhead(x, y + 44, 92, "#d8c7ae", "#b0643c", 1.0, at, "pop"), circ(x, y + 44 - 92 * .72 - 92 * .15 * .9, 18, "none", LILAC, 2, at + .1, style="claimed", fx="pop")]


def s57():
    """The ledger: five rows, each with a small picture, lit as named, its grade chip popping: Established, Established (the plants still debated),
    Strong evidence (two women), Plausible, Mixed record (sudden in places, slow in others)."""
    t = {p: T("s57", p, k=k) for p, k in (("Lakes", 1), ("Established", 1), ("Paced", 1), ("plants added", 1), ("A North African", 1), ("Strong evidence", 1),
                                           ("two women", 1), ("Nabta's stones", 1), ("Plausible", 1), ("The Sahara switching", 1), ("Mixed record", 1),
                                           ("sudden in places", 1))}
    t["Established2"] = T("s57", "Established", k=2)
    rows = [("lakes, hippos and herders", pic_lake, "Lakes", "Established", "Established", "established"),
            ("paced by the orbit and the monsoon", pic_orbit, "Paced", "Established2", "Established", "established"),
            ("a North African lineage nobody knew", pic_dna, "A North African", "Strong evidence", "Strong evidence", "strong"),
            ("Nabta's stones watching the sun", pic_ring, "Nabta's stones", "Plausible", "Plausible", "plausible"),
            ("switched off overnight?", pic_cliff_ramp, "The Sahara switching", "Mixed record", "Mixed record", "mixed")]
    els = [rect(110, 150, 1560, 580, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, -1)]
    for k, (text, pic, key, gk, grade, g) in enumerate(rows):
        els += lrow(LROWS[k], .3 + .1 * k, pic, text, lit=False)
        els += lrow(LROWS[k], max(.4, t[key]), pic, text, grade, t[gk], GRADE[g])
    els += [lab(1400, LROWS[1] + 9, "plants: debated", t["plants added"], MUTED, 26, "start"),
            lab(1440, LROWS[2] + 9, "two women", t["two women"], MUTED, 26, "start"),
            gl(220, LROWS[4], 90, t["sudden in places"], .45, "lamp")] + pic_cliff_ramp(220, LROWS[4], t["sudden in places"])
    return {"base": "dark", "cam": CAM, "els": els}


def s58():
    """The second ledger: Gobero one people or two, the swimmers alive or dead, drought as Egypt's spark: Open question, all three; the Garamantes undone by
    their fossil water: Plausible; astronauts on the rocks: Ruled out, the dotted helmet struck."""
    tg, ts, td, to, tga, tp, ta, tr_ = (T("s58", p) for p in ("Gobero's", "the swimmers", "and drought", "Open question", "The Garamantes", "Plausible", "And astronauts",
                                                             "Ruled out"))
    rows = [("Gobero: one people or two?", pic_groups, tg, "Open question", to, "open"),
            ("the swimmers: alive or dead?", pic_swimmer, ts, "Open question", to + .3, "open"),
            ("drought as Egypt's spark?", pic_nile, td, "Open question", to + .6, "open"),
            ("the Garamantes and their fossil water", pic_shaft, tga, "Plausible", tp, "plausible"),
            ("astronauts on the rocks", pic_roundhead, ta, "Ruled out", tr_, "ruled")]
    els = [rect(110, 150, 1560, 580, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, -1)]
    for k, (text, pic, at, grade, gt, g) in enumerate(rows):
        els += lrow(LROWS[k], .3 + .1 * k, pic, text, lit=False)
        els += lrow(LROWS[k], max(.4, at), pic, text, grade, gt, GRADE[g])
    els += [ln([(170, LROWS[4] + 30), (270, LROWS[4] - 40)], tr_ + .3, RED, 5, dur=.3)]
    return {"base": "dark", "cam": CAM, "els": els}


def s59():
    """What would change our minds: three dashed blue boxes (tests not yet done) fill as named: DNA from Gobero's graves (a helix over a grave with three
    lights); more genomes (a row of people, each with a helix); new lake cores (a rig over a dry basin, a core coming up, dots for places)."""
    t1, t2, t3, t4 = T("s59", "Ancient DNA"), T("s59", "More genomes"), T("s59", "new lake cores"), T("s59", "place by place")
    xs = [140, 640, 1140]
    els = []
    for k, (x, t, nm) in enumerate(zip(xs, (t1, t2, t3), ("DNA from Gobero", "more genomes", "new lake cores"))):
        els += [rect(x, 200, 480, 430, "rgba(159,208,255,.05)", BLUE, 2.5, 14, .4 + .15 * k, style="inferred", fx="pop"), lab(x + 240, 690, nm, t + .3, BLUE, 30)]
    x = xs[0] + 240
    els += [poly(E(x, 520, 150, 70, 30), "none", BONE, 2, t1, curve=True, style="inferred", fx="pop")]
    els += [gl(x - 30, 520, 70, t1 + .2, .9, "lamp"), gl(x + 30, 505, 50, t1 + .3, .9, "lamp"), gl(x + 26, 540, 46, t1 + .4, .9, "lamp")]
    els += helix(x - 150, 330, x + 150, 330, t1 + .5, n=9, amp=18, w=3, dur=.8)
    x = xs[1]
    for k in range(5):
        px = x + 70 + 85 * k
        els += [figure(px, 590, 130, round(t2 + .15 * k, 2), W2 if k % 2 else "#e8d6b8", "pop")] + helix(px - 26, 380, px + 26, 380, round(t2 + .3 + .15 * k, 2), n=4, amp=9, w=2.2, dur=.3)
    x = xs[2]
    els += [poly([(x + 40, 560), (x + 140, 520), (x + 340, 520), (x + 440, 560), (x + 440, 610), (x + 40, 610)], "#c9a46e", "#efe0c0", 1.5, t3, fx="rise"),
            ln([(x + 200, 300), (x + 240, 240), (x + 280, 300)], t3 + .3, BONE, 5, draw=False), ln([(x + 180, 520), (x + 240, 240), (x + 300, 520)], t3 + .3, BONE, 4, draw=False),
            rect(x + 228, 300, 24, 250, "#7a6248", BONE, 2, 6, t3 + .6, fx="rise")]
    els += [rect(x + 230, 330 + 36 * j, 20, 30, c, at=round(t3 + .9 + .1 * j, 2), r=3) for j, c in enumerate(("#c9b48e", "#6f5a44", "#b9ab94", "#5a4632", "#a8977c", "#7a6248"))]
    els += [circ(x + 80 + 70 * k, 260 + 30 * (k % 2), 9, GOLD, at=round(t4 + .15 * k, 2), fx="pop") for k in range(5)]
    return {"base": "dark", "cam": CAM, "els": els}


def s60():
    """Dusk over the dunes of the opening view, the cliff on the right; under the sand, cut open, the old lake bed in pale layers holding a hippo jaw, a
    bone harpoon, a pollen grain and a potsherd, and a dashed line where the water once stood; the first stars come out."""
    tg, tw = T("s60", "the green Sahara"), T("s60", "waiting to be")
    GY = 400
    els = cliff(1260, 150, GY, -1, seed=60, shelter=False)
    els += [poly([(-60, GY + 10), (200, GY - 22), (420, GY - 6), (700, GY - 34), (980, GY - 8), (1240, GY - 26), (1500, GY - 4), (1900, GY - 20), (1900, GY + 60), (-60, GY + 60)],
                  "#c9a46e", at=-1, curve=True), poly([(-60, GY + 40), (1900, GY + 40), (1900, 1060), (-60, 1060)], "#a8865a", at=-1)]
    for k, (y0, c) in enumerate(((GY + 120, "#c9bfa8"), (GY + 190, "#b4a88e"), (GY + 260, "#d2c8b0"), (GY + 330, "#a89a80"))):
        els.append(poly([(-60, y0)] + [(x, y0 + 6 * math.sin(x / 150 + k)) for x in range(0, 1901, 150)] + [(1900, 1060), (-60, 1060)], c, at=-1, op=.92))
    els += [ln([(-60, GY + 112), (1900, GY + 112)], -1, "rgba(255,236,206,.35)", 1.5, draw=False)]
    els += [_hippo_jaw(420, GY + 230, .8, .5), harpoon(760, GY + 300, 220, -8, .9), _pollen_grass(1080, GY + 240, 30, 1.3),
            group([poly([(1280, GY + 300), (1400, GY + 286), (1420, GY + 330), (1300, GY + 344)], "#9a6a48", "#d8a878", 2, curve=True),
                   ln([(1300, GY + 312), (1400, GY + 302)], -1, "#7a4e34", 2, draw=False, style="inferred")], 1.7, "pop")]
    els += [ln([(-60, GY + 150), (1900, GY + 150)], tg, BLUE, 3, "inferred", dur=1.4), gl(889, GY + 260, 520, tg + .4, .18, "blue")]
    r = random.Random(60)
    els += [circ(r.uniform(60, 1700), r.uniform(130, 320), r.uniform(1.4, 2.6), "#fff6e8", at=round(tw + .12 * k, 2), fx="pop", op=round(r.uniform(.5, .95), 2)) for k in range(18)]
    return {"base": "sky", "tod": "dusk", "ground": GY + 40, "groundc": "#a8865a", "sun": [420, GY - 60, 26], "ridges": [], "cam": CAM, "els": els}


# ================================================================== a placeholder (only while a scene is being drawn)
def _todo(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 480, sid, .3, MUTED, 60)]}


# ================================================================== the film: beats (script lines + markers), aliases, the wall
# (chapter, beat, role, the beat's panel, [(line, the phrase that opens the sentence, shot)], extra beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "Around it", "s2"), (1, "Today there's", "s3"), (2, "So how did", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "Its old beaches", "s6"), (1, "And across the Sahara", "s7")], {"chapter": "A lake as big as a sea"}),
    (1, 1, "collision", "s8", [(0, "Some geologists", "s9")], {}),
    (1, 2, "reversal", "s10", [(1, "On a summer", "s11"), (1, "The West African", "s12")], {}),
    (1, 3, "tag", "s13", [(1, "A few crocodiles", "s14")], {}),
    (2, 0, "world", "s15", [(1, "It was a", "s16"), (1, "In the rubbish", "s17")], {"chapter": "The lake at Gobero"}),
    (2, 1, "collision", "s18", [(1, "When the water", "s19")], {}),
    (2, 2, "cost", "s20", [], {}),
    (2, 3, "reversal", "s21", [], {}),
    (2, 4, "tag", "s22", [], {}),
    (3, 0, "world", "s23", [(0, "He called it", "s24")], {"chapter": "Swimmers in the desert"}),
    (3, 1, "collision", "s25", [(1, "Hands,", "s26")], {}),
    (3, 2, "reversal", "s27", [(1, "But those Egyptian", "s28")], {}),
    (3, 3, "cost", "s29", [], {}),
    (3, 4, "tag", "s30", [], {}),
    (4, 0, "world", "s31", [(1, "The dry air", "s32")], {"chapter": "A lineage no one knew"}),
    (4, 1, "collision", "s33", [], {}),
    (4, 2, "reversal", "s34", [(1, "Their nearest", "s35")], {}),
    (4, 3, "cost", "s36", [], {}),
    (4, 4, "tag", "s37", [], {}),
    (5, 0, "world", "s38", [], {"chapter": "Stones that watched the sun"}),
    (5, 1, "collision", "s39", [(1, "Nearby, cattle", "s40"), (1, "The ring is older", "s41")], {}),
    (5, 2, "reversal", "s42", [(1, "The excavators", "s43")], {}),
    (5, 3, "tag", "s44", [], {}),
    (6, 0, "world", "s45", [], {"chapter": "When the rain stopped"}),
    (6, 1, "collision", "s46", [(0, "Off the coast", "s47")], {}),
    (6, 2, "reversal", "s48", [(1, "Lake Mega-Chad fell", "s49")], {}),
    (6, 3, "cost", "s50", [(0, "As the rains", "s51"), (1, "Some archaeologists", "s52")], {}),
    (6, 4, "collision", "s53", [(0, "Their water had", "s54"), (1, "But fossil water", "s55")], {}),
    (6, 5, "tag", "s56", [], {}),
    (7, 0, "weigh", "s57", [], {"chapter": "The weighing"}),
    (7, 1, "weigh", "s58", [], {}),
    (7, 2, "test", "s59", [], {}),
    (7, 3, "close", "s60", [], {}),
]

# alias shots: (the panel's shot, the camera on that panel, the additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", CAM, "s2_add"),
    "s3": ("s1", CAM, "s3_add"),
    "s19": ("s18", CAM, "s19_add"),
    "s22": ("s20", [1.08, 889, 520], "s22_add"),
    "s24": ("s23", [1.3, 980, 520], "s24_add"),
    "s32": ("s31", CAM, "s32_add"),
    "s43": ("s42", CAM, "s43_add"),
    "s44": ("s39", CAM, "s44_add"),
    "s49": ("s5", CAM, "s49_add"),
    "s55": ("s54", CAM, "s55_add"),
    "s56": ("s54", [1.12, 889, 520], "s56_add"),
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
    ep = {"id": "lf-green-sahara", "code": "LF.33", "series": script["series"], "title": script["title"], "case": "green-sahara",
          "verdict": "solid", "claim": "Was the Sahara once green, with lakes, hippos and herders, and how fast did the rain stop?", "mood": "awe",
          "hook_text": "How did the Sahara turn *green*?", "beats": beats, "shots": shots,
          "sources": "Drake & Bristow 2006 (doi:10.1191/0959683606hol981rr) · Armitage et al. 2015 (doi:10.1073/pnas.1417655112) · "
                     "deMenocal et al. 2000 (doi:10.1016/S0277-3791(99)00081-5) · Tierney et al. 2017 (doi:10.1126/sciadv.1601503) · "
                     "Sereno et al. 2008 (doi:10.1371/journal.pone.0002995) · Salem et al. 2025 (doi:10.1038/s41586-025-08793-7) · "
                     "Malville et al. 1998 (doi:10.1038/33131) · Kropelin et al. 2008 (doi:10.1126/science.1154913) · "
                     "Shanahan et al. 2015 (doi:10.1038/ngeo2329) · Kuper & Kropelin 2006 (doi:10.1126/science.1130989) · "
                     "Mattingly & Sterry 2013 (doi:10.1017/S0003598X00049097)",
          "post": "About nine thousand years ago, hippos swam in lakes in the middle of what is now the Sahara. Lake Mega-Chad and the wobble "
                  "of Earth's orbit, the embrace at Gobero, the painted swimmers of Wadi Sura, the ancient DNA of Takarkori, the stone ring "
                  "of Nabta Playa, the end of the rains and the move to the Nile, and the Garamantes' fossil water, weighed.",
          "hashtags": ["#Sahara", "#GreenSahara", "#AncientDNA", "#Prehistory", "#Archaeology", "#WeighItYourself"],
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
