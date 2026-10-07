"""LF.32 · The Method · An Ancient Nuclear War? (16:9 long film, one wall).

The script is films/long/lf-nuclear-war/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s50; s5t, the title, is the intro card over
the panel of s5; s46 is a lower framing of the ledger of s45), drawn while it is said: Tutankhamun's pectoral with its scarab of
yellow-green glass, the same glass on the sand of the Great Sand Sea, the dotted mushroom of the modern claim, the five clues on one
map; Clayton's glass field, the dunes a hundred metres high, silica, Trinity's green glass, fission tracks counted like tally marks,
twenty-nine million years against the first humans, the shock mineral, the melt and the shocked quartz, impact or airburst and
Kebira, the chalcedony card struck out, the scarab beside a raw lump; Philby's crossing to Wabar, the caravan and the craters, a
crater beside a football pitch and the Camel's Hump beside a car, two equal flashes (Wabar and Hiroshima), what the ground holds,
sand grains as batteries, a dune burying a crater, a fallen star; Mohenjo-daro from above, the claim in dotted lines, the
excavators' plan with numbered groups (never bodies), the layers like pages, the documents, three empty boxes, the Indus plain
emptying over generations; a Scottish hill fort, fused rock and a thermometer, the 1937 wall at Plean and its fire, the wall cut open,
the 1980 wall and its three kilograms, three open answers and a wood fire; Oklo and two billion years, a thousand atoms, the dotted
plant against an empty early Earth, the hourglass and the fuel band, groundwater and neutrons, the pulse, Kuroda's sixteen years,
the diary; the ledger, the verdict, the fingerprint (plutonium in lake mud and ice, a decay curve), the test, and the pectoral at night.
Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted = claimed. Human remains are never
drawn: the excavated groups appear only as numbered discs.

Facts: the Shorts 'desert-glass' (f16.py), 'wabar' (f14.py), 'oklo' and 'ooparts' (f00.py), their narrations in films/rewrite/, and the
script's facts_added (Clayton & Spencer 1934, Roe et al. 1982, Cavosie & Koeberl 2019, Koeberl & Ferriere 2019, Kovaleva et al. 2023,
Boslough & Crawford 2008, Longinelli et al. 2011, de Michele 1998, Carter 1933 and the Griffith Institute records, Eby et al. 2010,
Parekh et al. 2006, Philby 1933, Wynn & Shoemaker 1998, Prescott et al. 2004, Gnos et al. 2013, Marshall 1931, Mackay 1938, Wheeler
1947, Dales 1964, Kenoyer 1998, Giosan et al. 2012, Childe & Thorneycroft 1938, Ralston 1986, McCloy et al. 2021, Kuroda 1956,
Gauthier-Lafaye et al. 1996, Meshik et al. 2004, Bentridi et al. 2011, Shlyakhter 1976, Damour & Dyson 1996, McCarthy et al. 2023,
Arienzo et al. 2016).

Engine workaround (as in lf_denisovans.py): the wall only adds elements to a panel on its first visit, at a beat start or a line start;
a shot that adds to a panel it returns to mid-line is an alias of that panel with a camera whose zoom carries a tiny unique tag
(+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item.
Build-in times inside a sentence come from a syllable clock (Clock). Elements cannot fade out: a dark veil drawn over a part of a
panel stands in for a fade.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-nuclear-war/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-nuclear-war/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-nuclear-war RC_FILMS_EPS=/tmp/claude-0/sbx_lf-nuclear-war/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-nuclear-war/boards python3 films.py long.lf_nuclear_war
"""
import json, math, os, random, re
import films
from mural import remix, SENT
import illus as I
from illus import person, arrow, line, glow, label, dot, box, ring, strike, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-nuclear-war", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, MUTED, DIM = "#f2c98e", "#e8c35a", "#cbbca8", "#9a8f80"
LAND, LAND_E = "#4a3d2f", "#c9ad85"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#e8c86a", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}
# the desert glass, the jewel, the deserts, the bomb
GLASS, GLASS_E, GLASS_D, GLASS_H = "#d8df7c", "#f4f7c6", "#9fa84c", "#eef2b0"
GOLDJ, GOLDJ_E, GOLDJ_D = "#d9a93a", "#ffe7a0", "#8a6420"          # the jeweller's gold: face, lit edge, shade
LAPIS, TURQ, CARN, SILVER = "#2f5aa6", "#3fb4ad", "#c4482e", "#dfe5ec"
SAND, SAND_L, SAND_D = "#c9a36c", "#e2c08a", "#8a6b45"
BLACKG = "#1b1714"
PU = "#e86a50"                                               # plutonium, the fingerprint
TRIN = "#6fae6a"                                             # trinitite green
FLAT = "#15110d"                                             # the dark ground (for veils)
BRICK, BRICK_D, BRICK_L = "#b4704a", "#7a4630", "#d89a6e"
ROCK, ROCK_D, ROCK_L = "#6e5f52", "#3d342d", "#a8988a"
WATER = "#5fa8c9"


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
        return len(a)
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


# ================================================================== small drawings (as in lf_denisovans.py)
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


def arc(cx, cy, rx, ry, a0, a1, n=24):
    """Points on an elliptical arc, angles in degrees (0 = right, 90 = down)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


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
    out = []
    for e in els:
        e = dict(e)
        e["in"] = -1
        e.pop("fx", None)
        out.append(e)
    return out


def later(els, dt):
    out = []
    for e in els:
        e = dict(e)
        if isinstance(e.get("in"), (int, float)) and e["in"] >= 0:
            e["in"] = round(e["in"] + dt, 2)
        out.append(e)
    return out


def figure(x, y, h, at, c="#e8d6b8", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def walker(x, y, h, at, c="#2a221b", face=1, fx="rise", op=None, stride=.22):
    """A walking figure (legs apart), facing right (face=1) or left, feet on y."""
    w = h * .26
    X = lambda a: x + face * a
    body = [(X(-w * .48), y - h * .78), (X(w * .48), y - h * .78), (X(w * .42), y - h * .42), (X(w * .2 + stride * h * .5), y), (X(w * .02 + stride * h * .5), y),
            (X(0), y - h * .36), (X(-w * .02 - stride * h * .5), y), (X(-w * .2 - stride * h * .5), y), (X(-w * .42), y - h * .42)]
    return [group([circ(X(w * .06), y - h * .9, h * .085, c), poly(body, c)], at, fx, op=op)]


def mix(c, bg="#241c16", t=.5):
    """The colour c faded towards the background bg (t = how much of c is kept)."""
    a, b = c.lstrip("#"), bg.lstrip("#")
    ca, cb = [int(a[i:i + 2], 16) for i in (0, 2, 4)], [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(cb[i] + (ca[i] - cb[i]) * t) for i in range(3))


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


# ================================================================== maps (as in lf_denisovans.py)
def _unwrap(ring_):
    out, prev = [], None
    for lo, la in ring_:
        if prev is not None:
            while lo - prev > 180:
                lo -= 360
            while lo - prev < -180:
                lo += 360
        out.append((lo, la)); prev = lo
    return out


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
    """An equirectangular map of a lon/lat box fitted in a frame rectangle (like films.View); land rings clipped to it."""
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

    def land(self, pad=40.0, tol=1.4, minpts=4):
        lon0, lon1, lat0, lat1 = self.b
        out = []
        for poly_ in films._topo():
            ring0 = _unwrap(poly_[0])
            if max(q[1] for q in ring0) < lat0 - pad or min(q[1] for q in ring0) > lat1 + pad:
                continue
            cl = []
            for sh in (-360, 0, 360):          # a ring cut at the antimeridian unwraps to lon -377..-170 (Afro-Eurasia): shift it home
                ring_ = [(lo + sh, la) for lo, la in ring0]
                xs = [q[0] for q in ring_]
                if max(xs) < lon0 - pad or min(xs) > lon1 + pad:
                    continue
                c_ = _clip(ring_, lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad)
                if len(c_) > len(cl):
                    cl = c_
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


def pin(x, y, t, at, c=AMBER, a="start", lx=None, ly=None, r=9, tc=None):
    e = {"k": "pin", "x": round(x, 1), "y": round(y, 1), "t": t, "c": c, "a": a, "r": r, "in": round(at, 2)}
    if lx is not None:
        e["lx"] = lx
    if ly is not None:
        e["ly"] = ly
    if tc:
        e["tc"] = tc
    return e


def window(x, y, w, h, els, at=-1, sea="#12202a", edge="rgba(255,236,206,.35)"):
    """A small picture (a locator map) in a rounded window."""
    return [{"k": "group", "clip": [round(x, 1), round(y, 1), round(w, 1), round(h, 1), 14], "bg": sea, "in": round(at, 2), "els": els},
            rect(x, y, w, h, "none", edge, 2, 14, at)]


# the Nile (lon, lat), from Lake Nasser to the delta, and the coast lines are from the topo data
NILE = [(31.6, 22.0), (32.4, 22.6), (32.9, 23.9), (32.9, 24.6), (32.6, 25.7), (32.7, 26.1), (32.2, 26.5), (31.6, 26.9), (31.2, 27.2), (30.8, 28.1),
        (30.9, 29.0), (31.25, 30.05), (31.0, 30.6), (30.6, 31.3)]
INDUS = [(80.0, 32.9), (77.6, 34.2), (75.4, 35.6), (73.9, 35.1), (72.6, 34.0), (71.6, 33.2), (71.3, 31.8), (70.9, 30.5), (70.4, 29.2), (69.6, 28.3),
         (68.6, 27.6), (68.1, 27.0), (68.3, 26.1), (68.3, 25.2), (67.8, 24.3), (67.4, 23.9)]


# ================================================================== the jewel and the glass
def glass_lump(x, y, s, at, seed=1, fx="pop", glow_=True, c=GLASS, op=None):
    """A raw lump of desert glass lying on the ground at (x, y) (its base), about 60 x 34 units at s = 1: irregular, translucent,
    a pale highlight and a few dark pits; a soft glow when lit."""
    r = random.Random(seed)
    n = 11
    pts = []
    for k in range(n):
        a = math.pi + math.pi * k / (n - 1)
        rr = r.uniform(.78, 1.1)
        pts.append((x + 30 * s * rr * math.cos(a), y + 30 * s * rr * math.sin(a) * .95))
    pts += [(x + 26 * s, y + 2 * s), (x - 26 * s, y + 2 * s)]
    pts = pts[:n] + [(x + 30 * s, y), (x - 30 * s, y)]
    hl = [(x - 14 * s, y - 20 * s), (x + 2 * s, y - 25 * s), (x + 12 * s, y - 18 * s), (x - 4 * s, y - 13 * s)]
    els = [poly(pts, c, GLASS_E, 1.4, curve=True), poly(hl, GLASS_H, at=-1, curve=True, op=.75),
           circ(x + 13 * s, y - 15 * s, 1.7 * s, "#fbf6c8", at=-1, op=.75), circ(x - 17 * s, y - 3 * s, 1.3 * s, GLASS_D, at=-1, op=.45)]   # a bubble, a speck (not a pair of eyes)
    out = [group(els, at, fx, op=op)]
    if glow_:
        out.insert(0, glow(round(x, 1), round(y - 14 * s, 1), round(70 * s), round(at, 2), .55, "lamp"))
    return out


def scarab(cx, cy, s, at=-1, fx=None, glow_=True, legs=True):
    """The glass scarab of the pectoral seen from above, head up: body centre (cx, cy), about 150 x 230 units at s = 1."""
    P = lambda a, b: (cx + a * s, cy + b * s)
    els = []
    if legs:
        for sx in (-1, 1):
            els += [ln([P(sx * 32, -70), P(sx * 52, -100), P(sx * 58, -138)], -1, GOLDJ, 6 * s, draw=False),     # front legs up to the boat
                    ln([P(sx * 40, 70), P(sx * 52, 104), P(sx * 46, 128)], -1, GOLDJ, 6 * s, draw=False)]       # hind legs down to the flowers
    body = E(cx, cy + 6 * s, 72 * s, 92 * s, 40)
    els += [poly(body, GLASS, GLASS_E, 2.2 * s, curve=True),
            poly(E(cx - 8 * s, cy - 14 * s, 44 * s, 56 * s, 30), GLASS_H, at=-1, curve=True, op=.55),                  # the light inside the glass
            poly(E(cx + 22 * s, cy + 40 * s, 26 * s, 34 * s, 24), GLASS_D, at=-1, curve=True, op=.35),
            ln([P(-62, -40), P(-30, -50), P(0, -52), P(30, -50), P(62, -40)], -1, GLASS_D, 2.6 * s, draw=False, curve=True),   # pronotum
            ln([P(0, -50), P(0, 96)], -1, GLASS_D, 2.4 * s, draw=False),                                              # wing cases
            poly([P(-40, -82), P(-30, -100), P(-14, -108), P(0, -110), P(14, -108), P(30, -100), P(40, -82), P(20, -76), P(-20, -76)],
                 "#cdd476", GLASS_E, 1.6 * s, at=-1, curve=True),                                                     # head
            ln([P(-12, -106), P(-6, -114), P(0, -108), P(6, -114), P(12, -106)], -1, GLASS_D, 1.8 * s, draw=False),   # the clypeus teeth
            ln([P(-44, -16), P(-30, -30), P(-10, -36)], -1, "#ffffff", 2 * s, draw=False, curve=True, op=.6)]
    out = [group(els, at, fx)]
    if glow_:
        out.insert(0, glow(round(cx, 1), round(cy, 1), round(190 * s), round(at, 2) if at >= 0 else -1, .55, "lamp"))
    return out


def _wing(cx, cy, s, sx):
    """One falcon wing of the pectoral (sx = 1 right, -1 left): three bands of inlaid feathers in gold cloisons."""
    P = lambda a, b: (cx + sx * a * s, cy + b * s)
    top = [(58, -78), (110, -104), (170, -112), (228, -100), (272, -70), (296, -24), (300, 30), (292, 96)]
    m1 = [(62, -52), (112, -74), (168, -82), (222, -72), (258, -46), (278, -8), (280, 40), (272, 100)]
    m2 = [(64, -26), (114, -44), (166, -50), (214, -40), (244, -18), (258, 16), (256, 60), (250, 104)]
    bot = [(66, 10), (112, -6), (160, -10), (204, -2), (226, 22), (234, 56), (230, 96), (226, 108)]
    out = []
    cols = [(LAPIS, TURQ), (TURQ, LAPIS), (CARN, LAPIS, TURQ)]
    for bi, (a, b) in enumerate(((top, m1), (m1, m2), (m2, bot))):
        for k in range(len(a) - 1):
            q = [P(*a[k]), P(*a[k + 1]), P(*b[k + 1]), P(*b[k])]
            cc = cols[bi][k % len(cols[bi])]
            out.append(poly(q, cc, GOLDJ, 1.6 * s, at=-1))
    out.append(ln([P(*q) for q in top], -1, GOLDJ_E, 2.2 * s, draw=False, curve=True))
    out.append(ln([P(*q) for q in bot], -1, GOLDJ, 2.2 * s, draw=False, curve=True))
    return out


def _uraeus(x, y, s, sx, at=-1):
    """A rearing cobra seen from the front-side, base at (x, y), with a red sun disc on its head."""
    P = lambda a, b: (x + sx * a * s, y + b * s)
    return [poly([P(-6, 0), P(8, 0), P(10, -14), P(6, -26), P(12, -40), P(8, -50), P(-2, -52), P(-8, -44), P(-4, -30), P(-8, -16)], GOLDJ, GOLDJ_E, 1.2 * s, at=at, curve=True),
            poly(E(*P(2, -44), 9 * s, 12 * s, 14), TURQ, GOLDJ, 1.2 * s, at=at),
            circ(*P(2, -62), 7 * s, CARN, GOLDJ, 1.2 * s, at)]


def pectoral(cx, cy, s, at=-1, fx=None, lit=True):
    """Tutankhamun's pectoral with the glass scarab (Cairo JE 61884), redrawn: centre of the scarab at (cx, cy); about 600 x 540
    units at s = 1 (moon disc on top, fringe of pendants at the bottom)."""
    P = lambda a, b: (cx + a * s, cy + b * s)
    els = []
    if lit:
        els.append(glow(round(cx, 1), round(cy - 30 * s, 1), round(420 * s), -1, .32, "lamp"))
    # the base bar with its plants, and the fringe of pendants
    els += [rect(*P(-262, 128), 524 * s, 22 * s, GOLDJ, GOLDJ_E, 1.6 * s, 3 * s, -1)]
    for k in range(9):
        x = -232 + 58 * k
        els += [poly([P(x - 10, 132), P(x + 10, 132), P(x + 6, 146), P(x - 6, 146)], (LAPIS, CARN, TURQ)[k % 3], GOLDJ_E, 1 * s, at=-1)]
    for k in range(13):
        x = -240 + 40 * k
        kind = k % 3
        els.append(circ(*P(x, 158), 4 * s, GOLDJ, at=-1))
        if kind == 0:     # a lotus flower
            els.append(poly([P(x - 14, 164), P(x + 14, 164), P(x + 8, 196), P(x, 204), P(x - 8, 196)], LAPIS, GOLDJ, 1.4 * s, at=-1))
            els.append(poly([P(x - 6, 192), P(x + 6, 192), P(x, 204)], "#e9e2d0", at=-1))
        elif kind == 1:   # a poppy seed head
            els.append(poly(E(*P(x, 184), 11 * s, 18 * s, 16), CARN, GOLDJ, 1.4 * s, at=-1))
        else:             # a papyrus umbel
            els.append(poly([P(x - 4, 164), P(x + 4, 164), P(x + 15, 196), P(x - 15, 196)], TURQ, GOLDJ, 1.4 * s, at=-1))
    # the wings
    for sx in (-1, 1):
        els += _wing(cx, cy, s, sx)
    # lotus (left) and papyrus (right) held by the hind legs
    els += [poly([P(-60, 126), P(-84, 104), P(-74, 98), P(-60, 112), P(-46, 98), P(-36, 104)], LAPIS, GOLDJ, 1.4 * s, at=-1),
            poly([P(60, 126), P(40, 100), P(80, 100)], TURQ, GOLDJ, 1.4 * s, at=-1)]
    # the boat with the eye of Horus and two cobras, the crescent and the moon disc
    boat = [P(-150, -176), P(-128, -160), P(-60, -150), P(60, -150), P(128, -160), P(150, -176), P(140, -150), P(100, -134), P(-100, -134), P(-140, -150)]
    els += [poly(boat, GOLDJ, GOLDJ_E, 1.8 * s, at=-1, curve=True), ln([P(-112, -146), P(0, -142), P(112, -146)], -1, LAPIS, 5 * s, draw=False, curve=True)]
    eye = [P(-34, -172), P(-12, -184), P(14, -184), P(36, -172), P(14, -162), P(-12, -162)]
    els += [poly(eye, "#f3ecdc", LAPIS, 3 * s, at=-1, curve=True), circ(*P(2, -173), 8 * s, "#1a1716", at=-1),
            ln([P(-38, -192), P(0, -198), P(38, -190)], -1, LAPIS, 5 * s, draw=False, curve=True),
            ln([P(-8, -162), P(-12, -150)], -1, LAPIS, 4 * s, draw=False), ln([P(10, -162), P(24, -152), P(34, -156)], -1, LAPIS, 4 * s, draw=False, curve=True)]
    els += _uraeus(*P(-76, -152), s, -1) + _uraeus(*P(76, -152), s, 1)
    els += [poly([(cx + 70 * s * math.cos(math.radians(a)), cy - 252 * s + 70 * s * math.sin(math.radians(a))) for a in range(15, 166, 10)] +
                 [(cx + 54 * s * math.cos(math.radians(a)), cy - 252 * s + 54 * s * math.sin(math.radians(a))) for a in range(165, 14, -10)],
                 GOLDJ, GOLDJ_E, 1.6 * s, at=-1, curve=True),
            circ(*P(0, -256), 54 * s, SILVER, GOLDJ, 2.4 * s, -1),
            circ(*P(-14, -270), 22 * s, "#ffffff", at=-1, op=.35)]
    for k, dx in enumerate((-20, 0, 20)):          # the king between two gods, tiny, in gold on the silver disc
        h = 34 if k == 1 else 38
        els += [circ(*P(dx, -262 - h * .45), 4.4 * s, GOLDJ, at=-1), poly([P(dx - 5, -262 - h * .32), P(dx + 5, -262 - h * .32), P(dx + 6, -238), P(dx - 6, -238)], GOLDJ, at=-1)]
    # the scarab last, on top
    els += scarab(cx, cy, s, -1, glow_=False)
    out = [group(els, at, fx)] if at >= 0 else els
    if lit:
        out.insert(0, glow(round(cx, 1), round(cy, 1), round(230 * s), at if at >= 0 else -1, .5, "lamp"))
    return out


# ------------------------------------------------------------------ deserts, dunes, sky
def dune_band(y, amp, seed, c, at=-1, x0=-60, x1=1840, n=9, op=None, edge=None, taper=None):
    """A band of dunes: smooth crests along y (amp = crest height), filled down to the bottom of the panel. taper = (left, right):
    a y the band's end crest comes down to (the floor line), so a band that stops mid-panel slopes away instead of ending in a cliff."""
    r = random.Random(seed)
    pts = [(x0, 1100)]
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        yy = y - amp * (.35 + .65 * abs(math.sin(k * 1.3 + seed))) * r.uniform(.8, 1.05)
        if taper and k == 0 and taper[0] is not None:
            yy = taper[0]
        if taper and k == n and taper[1] is not None:
            yy = taper[1]
        pts.append((x, yy))
    pts.append((x1, 1100))
    return poly(pts, c, edge or "none", 1.2 if edge else 0, at, curve=True, op=op)


def mushroom(cx, base, h, at, c=LILAC, w=3, style="claimed", fill="rgba(201,193,238,.04)"):
    """A mushroom cloud drawn only as an outline: a column and a rounded cap (h = total height, base at y = base)."""
    s = h / 600
    P = lambda a, b: (cx + a * s, base + b * s)
    col = [P(-40, 0), P(-34, -200), P(-46, -330), P(46, -330), P(34, -200), P(40, 0)]
    cap = [P(-60, -330), P(-170, -350), P(-230, -400), P(-220, -470), P(-160, -530), P(-60, -570), P(60, -570), P(160, -530), P(220, -470),
           P(230, -400), P(170, -350), P(60, -330)]
    skirt = [P(-120, -380), P(-60, -360), P(0, -356), P(60, -360), P(120, -380)]
    return [poly(col, fill, c, w, at, curve=True, style=style, fx="rise"), poly(cap, fill, c, w, at + .3, curve=True, style=style, fx="rise"),
            ln(skirt, at + .6, c, w * .8, style, dur=.6, curve=True)]


def atom_icon(x, y, r, at, c=GOLD, fx="pop"):
    """A small atom: a nucleus and three orbits."""
    els = [circ(x, y, r * .22, c, at=-1)]
    for k in range(3):
        a = math.radians(60 * k)
        pts = [(x + r * math.cos(t) * math.cos(a) - r * .38 * math.sin(t) * math.sin(a), y + r * math.cos(t) * math.sin(a) + r * .38 * math.sin(t) * math.cos(a))
               for t in [2 * math.pi * q / 24 for q in range(25)]]
        els.append(ln(pts, -1, c, 2, draw=False, curve=True))
    return group(els, at, fx)


def ring_crater(x, y, r, at, fx="pop", c=BLACKG):
    """A small crater seen from above, with a dark rim of glass beads (an icon)."""
    return group([circ(x, y, r, "#8a6b45", "#e8d3a8", 2), circ(x, y, r * .72, "#5a4632", at=-1), circ(x, y, r, "none", c, 4, -1, style="claimed")], at, fx)


def city_icon(x, y, s, at, fx="pop"):
    els = [rect(x - 30 * s, y - 30 * s, 60 * s, 60 * s, "#5a3a2a", BRICK_L, 1.6, 4)]
    for k in range(1, 3):
        els += [ln([(x - 30 * s + 20 * k * s, y - 30 * s), (x - 30 * s + 20 * k * s, y + 30 * s)], -1, BRICK_L, 2, draw=False),
                ln([(x - 30 * s, y - 30 * s + 20 * k * s), (x + 30 * s, y - 30 * s + 20 * k * s)], -1, BRICK_L, 2, draw=False)]
    return group(els, at, fx)


def wall_icon(x, y, s, at, fx="pop"):
    els = []
    for row in range(3):
        for k in range(3):
            xx = x - 36 * s + k * 24 * s + (12 * s if row % 2 else 0)
            els.append(rect(xx, y - 10 * s - row * 14 * s, 22 * s, 12 * s, "#6a6056", "#b8aa98", 1, 2))
    els.append(rect(x - 36 * s, y - 40 * s, 84 * s, 10 * s, BLACKG, "#5b6b74", 1, 3))
    return group(els, at, fx)


# ================================================================== cold open
PECT = (1190, 470, 1.04)          # the pectoral of the opening: scarab centre and scale


def s1():
    """THE HERO IMAGE, whole from the first frame: Tutankhamun's pectoral under a spotlight, its yellow-green glass scarab glowing.
    Labels after the hook title has gone."""
    tt, tb = T("s1", "Tutankhamun"), T("s1", "a beetle")
    cx, cy, s = PECT
    els = light_shaft(1040, 1340, -40, 880, 1500, 820, -1, .045)
    els += [poly(E(cx, 800, 360, 34, 30), "#000000", at=-1, op=.35)]
    els += pectoral(cx, cy, s, -1)
    els += [lab(760, 392, "Tutankhamun's pectoral", max(tt, 3.2), BONE, 32, "end"),
            ln([(772, 548), (980, 520), (cx - 70, cy + 6)], max(tb, 3.6), GLASS_E, 2, dur=.7, curve=True),
            lab(760, 560, "a scarab of yellow-green glass", max(tb, 3.6) + .3, GLASS_E, 30, "end")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def sand_sea(at_lumps, seed=7, dusk=False):
    """The Great Sand Sea seen from a rock corridor: dune ridges in layers (back ones dim) and the pale rock floor in front."""
    if dusk:
        cols = ["#3c2c33", "#5a3e36", "#7a5440", "#9a6c4c"]
        floor = "#6e5844"
    else:
        cols = ["#6a5260", "#94705c", "#b98a5e", "#d3a26a"]
        floor = "#c8ab84"
    els = [dune_band(452, 60, seed, cols[0]), dune_band(500, 90, seed + 3, cols[1]), dune_band(560, 120, seed + 6, cols[2], n=7),
           dune_band(612, 70, seed + 9, cols[3], x0=-60, x1=860, n=5, taper=(None, 646)),
           dune_band(606, 80, seed + 11, cols[3], x0=1100, x1=1840, n=4, taper=(646, None))]
    els += [poly([(-60, 640), (1840, 640), (1840, 1100), (-60, 1100)], floor, at=-1),
            ln([(-60, 640), (1840, 640)], -1, "rgba(255,236,206,.35)", 1.5, draw=False)]
    r = random.Random(seed + 40)
    for k in range(26):                                   # flat stones and cracks of the corridor floor
        x, y = r.uniform(40, 1740), r.uniform(660, 790)
        els.append(poly(E(x, y, r.uniform(16, 44), r.uniform(4, 9), 12), mix(floor, "#000000", .8), at=-1, op=.5))
    return els


def s2():
    """The same glass on the sand: the Great Sand Sea at dawn, glass lumps catching the light one after another on the rock corridor;
    a walker for scale; a locator map of Egypt with the Nile and the glass field."""
    tg = T("s2", "glass")
    els = sand_sea(tg)
    spots = [(330, 700, 1.1), (520, 742, .8), (690, 690, .7), (905, 760, 1.25), (1110, 706, .75), (1290, 738, .95), (1480, 700, .7), (210, 760, .9)]
    for k, (x, y, s) in enumerate(spots):
        els += glass_lump(x, y, s, round(tg + .15 * k, 2), seed=k + 3)
    els += walker(1560, 676, 60, .3, "#3a2a20", -1)
    m = Map(23.0, 35.5, 21.0, 32.0, rect=(1342, 132, 330, 280))
    nile = m.path(NILE)
    els += window(1330, 126, 356, 300, [land_el(m.land(), -1, "#7a6248"), ln(nile, -1, "#6fb6d6", 4, draw=False, curve=True),
                                         circ(*m.p(25.5, 25.4), 13, GOLD, "#fff3c8", 2, .3), glow(*m.p(25.5, 25.4), 40, .3, .7, "lamp")], at=.2, sea="#173342")
    els += [lab(1508, 470, "EGYPT", .4, MUTED, 24), lab(890, 214, "the Great Sand Sea, Egypt", 1.0, BONE, 32)]
    return {"base": "sky", "tod": "dawn", "ground": 640, "sun": [430, 470, 34], "ridges": [], "cam": CAM, "els": els}


def s3():
    """The same dunes at dusk: a mushroom cloud rises over the far ridges, drawn only in dotted lilac (the modern claim, not a find)."""
    tm, tw = T("s3", "Some modern"), T("s3", "and read")
    sea = sand_sea(-1, seed=7, dusk=True)
    # the claimed cloud rises from beyond the far ridge: drawn after the farthest band, before the nearer ones
    els = sea[:1] + [glow(1000, 340, 260, tm, .25, "blue")] + mushroom(1000, 520, 380, tm, LILAC, 3) + sea[1:]
    els += [glass_lump(x, y, s, -1, seed=k + 3, glow_=True)[1] for k, (x, y, s) in enumerate([(330, 700, 1.1), (905, 760, 1.25), (1290, 738, .95)])]
    els += [lab(1300, 210, "an atomic blast?", tm + .8, LILAC, 32, "start")]
    els += tag(560, 300, "a modern reading", tw, LILAC, 28, "claimed")
    return {"base": "sky", "tod": "dusk", "ground": 640, "sun": [300, 520, 26], "ridges": [], "cam": CAM, "els": els}


MAP5 = (-14.0, 80.0, -6.0, 61.0)
CLUES = {"glass": (25.5, 25.4), "wabar": (50.47, 21.5), "mohenjo": (68.14, 27.33), "scotland": (-3.6, 57.0), "oklo": (13.16, -1.39)}


def s4():
    """The five clues on one map, from Scotland to the Indus and down to Gabon: the glass field glows; four pins pop as named, each
    with a small icon."""
    m = Map(*MAP5, rect=(160, 130, 1460, 660))
    tw, tm, ts, to = T("s4", "Arabia"), T("s4", "Indus"), T("s4", "melted"), T("s4", "Africa")
    els = [land_el(m.land(), -1, "#4f4131")]
    gx, gy = m.p(*CLUES["glass"])
    els += [glow(gx, gy, 70, -1, .8, "lamp"), circ(gx, gy, 11, GOLD, "#fff3c8", 2, -1), lab(gx - 20, gy + 50, "Great Sand Sea", .3, GOLD, 28, "end")]
    for key, t, name, side in (("wabar", tw, "Wabar", "start"), ("mohenjo", tm, "Mohenjo-daro", "start"), ("scotland", ts, "Scotland", "start"), ("oklo", to, "Oklo", "start")):
        x, y = m.p(*CLUES[key])
        els += [glow(x, y, 50, t, .6, "lamp"), pin(x, y, name, t, GOLD, side, lx=22, ly=10)]
    wx, wy = m.p(*CLUES["wabar"]); mx, my = m.p(*CLUES["mohenjo"]); sx, sy = m.p(*CLUES["scotland"]); ox, oy = m.p(*CLUES["oklo"])
    els += [ring_crater(wx + 18, wy + 52, 16, tw + .3), city_icon(mx + 26, my + 54, .45, tm + .3), wall_icon(sx - 76, sy + 30, .7, ts + .3),
            atom_icon(ox - 48, oy + 4, 22, to + .3)]
    return {"base": "map", "cam": CAM, "els": els}


def s5():
    """The question: the scarab small and glowing on dark ground, five faint lights around it, the dotted mushroom faint behind, a big
    lilac question mark. (The title card comes over this panel.)"""
    tq = T("s5", "So was there", .3)
    els = [glow(889, 520, 520, -1, .2, "lamp")]
    els += mushroom(889, 700, 520, -1, mix(LILAC, t=.45), 2.5)
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        x, y = 889 + 330 * math.cos(a), 470 + 230 * math.sin(a)
        els += [glow(round(x, 1), round(y, 1), 60, .2 + .1 * k, .55, "lamp"), dot(round(x, 1), round(y, 1), 6, GOLD, .2 + .1 * k)]
    els += scarab(889, 500, .78, -1)
    els += qmark(889, 270, tq, 150)
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


# ================================================================== chapter 1: the yellow glass
EG = (21.0, 34.0, 21.0, 32.0)


def s6():
    """Egypt and eastern Libya: the Nile, the Great Sand Sea as north-south dune lines, the Gilf Kebir; the glass field drawn to scale,
    at least 80 by 25 km; a pin for Clayton's find of December 1932; a 200 km scale bar."""
    m = Map(*EG, rect=(220, 130, 1340, 660))
    tp, tl = T("s6", "Pale"), T("s6", "eighty")
    els = [land_el(m.land(), -1, "#5a4834")]
    r = random.Random(12)
    for k in range(26):                                              # the dune lines of the Great Sand Sea (schematic)
        lo = 24.3 + 3.0 * k / 25 + r.uniform(-.05, .05)
        la0, la1 = 24.6 + r.uniform(0, .6), 29.6 - r.uniform(0, 1.2)
        els.append(ln([m.p(lo, la0), m.p(lo + .15, (la0 + la1) / 2), m.p(lo + .05, la1)], -1, "#a88a62", 2, draw=False, curve=True, op=.55))
    els += [ln(m.path(NILE), -1, "#6fb6d6", 5, draw=False, curve=True),
            ln([m.p(25.0, 21.8), m.p(25.0, 31.5)], -1, "rgba(255,236,206,.35)", 2, "inferred", draw=False)]
    gk = [m.p(lo, la) for lo, la in ((25.6, 23.0), (26.4, 23.1), (26.7, 23.7), (26.3, 24.2), (25.7, 24.1), (25.4, 23.6))]
    els += [poly(gk, "#6e5844", "#c9ad85", 1.5, -1, curve=True, op=.9)]
    cx, cy = m.p(25.5, 25.4)
    ry, rx = m.km(40), m.km(12.5)
    els += [glow(cx, cy, 90, tp, .7, "lamp"), poly(E(cx, cy, rx, ry, 30), "rgba(216,223,124,.55)", GLASS_E, 2.5, tp, curve=True, fx="pop"),
            pin(cx, cy - ry - 4, "Clayton, December 1932", tp + .6, GOLD, "start", lx=24, ly=-6)]
    els += [ln([(cx + rx + 18, cy - ry), (cx + rx + 34, cy - ry), (cx + rx + 34, cy + ry), (cx + rx + 18, cy + ry)], tl, BONE, 2.2, dur=.6),
            lab(cx + rx + 50, cy + 10, "at least 80 km", tl + .3, BONE, 28, "start")]
    nx, ny = m.p(30.85, 29.4)                                        # just west of the river, on land (it runs at about 31.0 E here)
    els += [lab(nx - 6, ny + 10, "the Nile", .4, "#9fd0ff", 28, "end"), lab(*m.p(28.3, 27.2), "Great Sand Sea", .6, SAND_L, 30),
            lab(*m.p(26.0, 22.5), "Gilf Kebir", .8, MUTED, 26), lab(*m.p(30.5, 23.2), "EGYPT", .3, MUTED, 26), lab(*m.p(22.6, 23.4), "LIBYA", .3, MUTED, 26),
            {"k": "scale", "x": 260, "y": 770, "w": round(m.km(200), 1), "t": "200 km", "in": .5}]
    return {"base": "map", "cam": CAM, "els": els}


def s7():
    """A cut across the dunes: two ridges 100 m high with the rock corridor between them, a person at true scale (tiny), lumps of glass
    glinting; a close-up of one big lump: up to 4.5 kg."""
    th, tb, tr = T("s7", "hundred metres"), T("s7", "heavier"), T("s7", "bare rock")
    gy = 700
    u = 4.6                                                      # units per metre, up and down: dunes 100 m high, a person 1.7 m
    top = gy - 100 * u                                           # the crests, 460 units above the rock floor
    # two long dune ridges seen end on (the corridor between them is kilometres wide in reality: squeezed here), then the bedrock
    lp = [(-60, gy - 150), (40, gy - 250), (150, top + 70), (230, top + 12), (290, top), (345, top + 20), (420, gy - 300), (500, gy - 170), (580, gy - 60),
          (650, gy - 6)]
    rp = [(1010, gy - 6), (1080, gy - 70), (1170, gy - 220), (1260, top + 60), (1330, top + 8), (1380, top), (1440, top + 26), (1540, gy - 280), (1660, gy - 160),
          (1760, gy - 100), (1840, gy - 80)]
    els = [poly(lp + [(650, 1100), (-60, 1100)], "#c9955f", "rgba(255,236,206,.35)", 1.5, -1, curve=True),
           poly(rp + [(1840, 1100), (1010, 1100)], "#b98a5e", "rgba(255,236,206,.35)", 1.5, -1, curve=True),
           poly([(-60, gy), (1840, gy), (1840, 1100), (-60, 1100)], "#8a7458", at=-1),             # the bare sandstone under it all
           ln([(-60, gy), (1840, gy)], -1, "rgba(255,236,206,.45)", 1.5, draw=False)]
    for k in range(4):                                                                             # faint bedding in the rock
        els.append(ln([(-60, gy + 26 + 24 * k), (1840, gy + 32 + 24 * k)], -1, "rgba(20,14,10,.22)", 1.5, draw=False))
    els += [lab(830, gy + 60, "bare rock", tr, "#e8d9bf", 28)]
    # the height, measured on the left ridge
    els += [ln([(110, gy), (110, top)], th, BONE, 2.2, dur=.6), ln([(96, top), (290, top)], th, BONE, 1.4, "inferred", dur=.4),
            ln([(96, gy), (124, gy)], th, BONE, 2, draw=False), lab(128, gy - 50 * u + 10, "100 m", th + .3, BONE, 30, "start")]
    # a person at about true height (drawn 1.4 times taller to be seen), and lumps of glass on the corridor
    els += [figure(760, gy, 1.7 * u * 1.4, .5, "#2a1d14"), circ(760, gy - 6, 26, "none", BONE, 1.6, .7, style="inferred"),
            lab(760, gy - 46, "a person", .9, BONE, 26)]
    for k, (x, s) in enumerate(((690, .26), (850, .22), (930, .3), (975, .2), (720, .2))):
        els += glass_lump(x, gy + 2, s, .3 + .1 * k, seed=20 + k)
    # one big lump, close up, in a lens over the corridor
    els += [circ(830, 330, 112, "rgba(18,13,10,.82)", BONE, 2.5, tb, fx="pop"), ln([(860, 442), (928, gy - 8)], tb, BONE, 1.4, "inferred", dur=.5)]
    els += glass_lump(830, 368, 2.1, tb + .2, seed=31)
    els += [lab(830, 482, "up to 4.5 kg", tb + .6, GLASS_E, 30)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": [1620, 190, 30], "ridges": [], "cam": CAM, "els": els}


def s8():
    """Silica, three ways: a heap of sand, a pane of window glass, a lump of the desert glass; one word joins them; about 98% silica."""
    ts, tw, tg = T("s8", "silica"), T("s8", "sand"), T("s8", "window")
    els = [rect(160, 600, 1460, 22, "#3a2f24", "rgba(255,236,206,.3)", 1.5, 6, -1), glow(889, 520, 640, -1, .16, "lamp")]
    # "It" is the desert glass: on the shelf from the start; then silica, then sand and window glass as they are named
    els += glass_lump(1340, 600, 3.0, .3, seed=9) + [lab(1340, 680, "desert glass", .6, GLASS_E, 30)]
    r = random.Random(5)
    heap = [(280, 600), (330, 560), (390, 520), (450, 505), (510, 522), (570, 562), (620, 600)]
    els += [poly(heap, SAND, SAND_L, 1.5, tw, curve=True, fx="rise")]
    els += [dot(round(r.uniform(320, 580), 1), round(r.uniform(560, 598), 1), 2.2, "#f0d8a8", tw + .1, op=.8) for _ in range(30)]
    els += [group([poly([(780, 600), (800, 330), (990, 330), (1010, 600)], "rgba(190,225,240,.18)", "#cfe8f4", 3),
                   ln([(830, 370), (860, 360)], -1, "#ffffff", 3, draw=False, op=.7), ln([(820, 420), (900, 395)], -1, "#ffffff", 2, draw=False, op=.5)], tg, "rise")]
    els += [lab(450, 680, "sand", tw + .2, SAND_L, 30), lab(895, 680, "window glass", tg + .2, "#cfe8f4", 30)]
    # one word over all three, above the pane
    els += [ln([(450, 470), (450, 280), (1340, 280), (1340, 470)], ts, BONE, 2, dur=.8), ln([(895, 280), (895, 250)], ts, BONE, 2, dur=.3),
            lab(895, 232, "silica", ts + .1, GOLD, 40, st="lab")]
    els += tag(1340, 752, "about 98% silica", ts + .6, GLASS_E, 26)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def tower(x, gy, h, at=-1, c="#3a3a40", e="rgba(220,230,240,.5)"):
    """The Trinity test tower: a steel lattice tower, a small cabin on top."""
    w0, w1 = h * .28, h * .08
    els = [ln([(x - w0, gy), (x - w1, gy - h)], -1, c, 5, draw=False), ln([(x + w0, gy), (x + w1, gy - h)], -1, c, 5, draw=False)]
    for k in range(6):
        t0, t1 = k / 6, (k + 1) / 6
        xa0, xa1 = x - (w0 + (w1 - w0) * t0), x - (w0 + (w1 - w0) * t1)
        xb0, xb1 = x + (w0 + (w1 - w0) * t0), x + (w0 + (w1 - w0) * t1)
        ya, yb = gy - h * t0, gy - h * t1
        els += [ln([(xa0, ya), (xb1, yb)], -1, c, 2, draw=False), ln([(xb0, ya), (xa1, yb)], -1, c, 2, draw=False), ln([(xa1, yb), (xb1, yb)], -1, c, 2.5, draw=False)]
    els.append(rect(x - h * .12, gy - h - h * .1, h * .24, h * .1, "#4a4a52", e, 1.2, 2))
    return group(els, at)


def s9():
    """New Mexico at dawn: the Trinity tower, a flash at its top; around its foot the sand turns to a crust of green glass, spreading."""
    tb, ty, tt, tg = T("s9", "nuclear blast"), T("s9", "in nineteen"), T("s9", "turned the sand"), T("s9", "green glass")
    gy = 640
    els = [poly([(-60, gy), (1840, gy), (1840, 1100), (-60, 1100)], "#9a7a58", at=-1)]
    els += [poly([(-60, gy - 10), (200, gy - 60), (420, gy - 40), (700, gy - 90), (980, gy - 50), (1300, gy - 80), (1560, gy - 30), (1840, gy - 60), (1840, gy), (-60, gy)],
                 "#4d3c40", at=-1, curve=True)]
    els += [tower(889, gy, 230), glow(889, gy - 250, 260, tb + .2, .9, "sun"), glow(889, gy - 250, 500, tb + .4, .35, "fire")]
    els += [lab(889, 240, "Trinity, New Mexico, 1945", ty, BONE, 32)]
    els += [poly(E(889, gy + 40, 340, 52, 40), "rgba(111,174,106,.75)", "#a8e0a0", 2, tt, curve=True, fx="pop"),
            poly(E(889, gy + 40, 220, 34, 30), "rgba(150,210,140,.5)", at=tt + .3, curve=True)]
    els += [lab(1300, gy + 140, "green glass: trinitite", tg + .3, "#a8e0a0", 30, "start"),
            ln([(1290, gy + 128), (1180, gy + 70)], tg + .3, "#a8e0a0", 1.6, dur=.4)]
    return {"base": "sky", "tod": "dawn", "ground": 1100, "sun": False, "ridges": [], "cam": CAM, "els": els}


def s10():
    """Fission tracks: a magnifier over the glass; uranium atoms split one by one, two fragments fly apart, a straight dark scratch is
    left each time; tally marks gather in fives at the right; about 29 million years."""
    ts, tc, ta = T("s10", "split"), T("s10", "Count"), T("s10", "About twenty-nine")
    cx, cy, R_ = 640, 470, 300
    els = [circ(cx, cy, R_ + 18, "#2a221a", "#cbbca8", 6, -1), circ(cx, cy, R_, "#c9cf72", at=-1),
           circ(cx - 90, cy - 110, 150, "#e6ea9e", at=-1, op=.35), ln([(cx + R_ * .7, cy + R_ * .7), (cx + R_ * 1.05, cy + R_ * 1.05)], -1, "#cbbca8", 22, draw=False)]
    r = random.Random(3)
    atoms = [(cx - 160, cy - 60), (cx + 40, cy - 170), (cx + 150, cy + 20), (cx - 60, cy + 140), (cx + 60, cy + 90), (cx - 190, cy + 60), (cx + 190, cy - 110)]
    els += [circ(x, y, 9, GOLD, "#fff3c8", 1.5, -1) for x, y in atoms]
    for k, (x, y) in enumerate(atoms):
        t = round(ts + .35 * k, 2)
        a = r.uniform(0, math.pi)
        L = r.uniform(70, 110)
        p0, p1 = (x - L * math.cos(a), y - L * math.sin(a)), (x + L * math.cos(a), y + L * math.sin(a))
        els += [ln([(x, y), p0], t, "#3b3418", 4, dur=.35), ln([(x, y), p1], t, "#3b3418", 4, dur=.35), dot(round(p0[0], 1), round(p0[1], 1), 5, AMBER, t + .3),
                dot(round(p1[0], 1), round(p1[1], 1), 5, AMBER, t + .3)]
    els += [lab(cx, 130, "inside the glass, magnified", .3, MUTED, 28)]
    # tally marks
    tx0, ty = 1120, 360
    for k in range(12):
        g, j = divmod(k, 5)
        t = round(tc + .18 * k, 2)
        if j < 4:
            x = tx0 + g * 150 + j * 26
            els.append(ln([(x, ty), (x, ty + 120)], t, BONE, 6, dur=.2))
        else:
            els.append(ln([(tx0 + g * 150 - 14, ty + 100), (tx0 + g * 150 + 92, ty + 20)], t, BONE, 6, dur=.2))
    els += [lab(1290, 300, "count the tracks", tc, BONE, 30)]
    els += chip(1290, 610, "about 29 million years", GOLD, ta, 32)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s11():
    """A time line of 30 million years: the glass at 29 million (an atom icon: it keeps time with its uranium); the first humans at about
    2.8 million, near the right end; a bracket between them: more than 20 million years."""
    tk, th = T("s11", "keeps time"), T("s11", "first humans")
    x0, x1 = 200, 1580
    X = lambda ma: round(x0 + (30 - ma) / 30 * (x1 - x0), 1)
    els = [axis(x0, x1, 560, [(X(30), "30"), (X(20), "20"), (X(10), "10"), (X(0), "today")], .2, "million years ago")]
    gx = X(29)
    els += [glow(gx, 470, 120, .6, .6, "lamp")] + glass_lump(gx, 500, 1.2, .6, seed=41, glow_=False)
    els += [ln([(gx, 520), (gx, 560)], .8, GOLD, 3, dur=.3), lab(gx, 400, "the yellow glass", .9, GLASS_E, 30), atom_icon(gx + 100, 470, 26, tk)]
    hx = X(2.8)
    els += [ln([(hx, 520), (hx, 560)], th, BONE, 3, dur=.3), figure(hx, 512, 70, th, BONE), lab(hx, 410, "the first humans", th + .2, BONE, 28, "end")]
    els += bracket(gx, hx, 320, th + .9, "more than 20 million years", GOLD, up=False, size=30, ty=296)     # above the line, clear of its title
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def clip_seg(p0, p1, pts, shrink=1.0):
    """The part of segment p0-p1 inside the convex polygon pts (shrunk towards its centre by `shrink`), or None (Cyrus-Beck)."""
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    q = [(cx + (x - cx) * shrink, cy + (y - cy) * shrink) for x, y in pts]
    area = sum(q[i - 1][0] * q[i][1] - q[i][0] * q[i - 1][1] for i in range(len(q)))          # shoelace: > 0 when the interior is left of each edge
    t0, t1 = 0.0, 1.0
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    for i in range(len(q)):
        a, b = q[i - 1], q[i]
        nx, ny = (a[1] - b[1], b[0] - a[0]) if area > 0 else (b[1] - a[1], a[0] - b[0])     # the inward normal
        num = nx * (p0[0] - a[0]) + ny * (p0[1] - a[1])
        den = nx * dx + ny * dy
        if abs(den) < 1e-9:
            if num < 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return (p0[0] + t0 * dx, p0[1] + t0 * dy), (p0[0] + t1 * dx, p0[1] + t1 * dy)


def zircon(x, y, s, at, fx="pop"):
    """A zircon crystal: a long square prism with pyramid ends, seen from the side, its inside grainy with tiny bright specks."""
    P = lambda a, b: (x + a * s, y + b * s)
    body = [P(0, -120), P(36, -80), P(36, 80), P(0, 120), P(-36, 80), P(-36, -80)]
    els = [poly(body, "#d9b48a", "#fff0d8", 2), poly([P(0, -120), P(36, -80), P(36, 80), P(0, 120)], "#b8916a", at=-1, op=.6),
           ln([P(-36, -80), P(0, -60), P(36, -80)], -1, "#fff0d8", 1.4, draw=False), ln([P(-36, 80), P(0, 100), P(36, 80)], -1, "#fff0d8", 1.4, draw=False),
           ln([P(0, -60), P(0, 100)], -1, "#fff0d8", 1.2, draw=False, op=.6)]
    r = random.Random(4)
    for k in range(40):
        a, b = r.uniform(-30, 30), r.uniform(-70, 70)
        els.append(circ(*P(a, b), r.uniform(1.6, 3.2) * s, "#fffbe8", at=-1, op=.85))
    return group(els, at, fx)


def s12():
    """Three clues in turn: a zircon crystal under a lens with tiny bright specks (a shock mineral); a thermometer rising past lava (about
    1,200 degrees) to the melt (over 2,750); a grain of quartz crossed by fine parallel lines (shocked quartz)."""
    tz, tm, tq = T("s12", "Tiny zircon"), T("s12", "The melt"), T("s12", "the bedrock")
    els = [circ(330, 420, 190, "rgba(18,13,10,.6)", BONE, 3, tz, fx="pop"), zircon(330, 420, 1.15, tz + .3), lab(330, 690, "a shock mineral", tz + 1.0, GOLD, 30)]
    tx, ty0, ty1 = 889, 640, 200
    els += [rect(tx - 22, ty1 - 10, 44, ty0 - ty1 + 30, "rgba(245,236,220,.06)", BONE, 2.5, 22, tm, fx="pop"), circ(tx, ty0 + 30, 40, "#e05a3a", BONE, 2.5, tm, fx="pop")]
    yl, ym = ty0 - (ty0 - ty1) * 1200 / 3000, ty0 - (ty0 - ty1) * 2750 / 3000
    els += [rect(tx - 10, ym, 20, ty0 - ym + 10, "#e05a3a", at=tm + .4, fx="fill", dur=1.4),
            ln([(tx + 26, yl), (tx + 60, yl)], tm + .9, AMBER, 2.5, draw=False), lab(tx + 72, yl + 10, "lava, about 1,200 °C", tm + .9, AMBER, 26, "start"),
            ln([(tx + 26, ym), (tx + 60, ym)], tm + 1.6, "#ff8a6a", 2.5, draw=False), lab(tx + 72, ym + 10, "the melt, over 2,750 °C", tm + 1.6, "#ff9a7a", 28, "start")]
    gx, gy = 1440, 420
    grain = [(gx - 120, gy - 40), (gx - 70, gy - 120), (gx + 40, gy - 130), (gx + 130, gy - 60), (gx + 120, gy + 70), (gx + 20, gy + 130), (gx - 100, gy + 90)]
    els += [poly(grain, "#e8e2d6", "#ffffff", 2, tq, curve=True, fx="pop")]
    for k in range(9):                                       # planar deformation features: fine parallel lines, kept inside the grain
        d = -40 + 25 * k
        seg = clip_seg((gx - 200 + d * .3, gy - 126 + d), (gx + 200 + d * .3, gy - 4 + d), grain, .86)
        if seg:
            els.append(ln(list(seg), round(tq + .3 + .06 * k, 2), "#7a6a58", 2, dur=.3))
    els += [lab(gx, 690, "shocked quartz", tq + .8, GOLD, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s13():
    """Two ways to melt a desert over one ground line: left, a rock falling into a crater drawn dashed (an impact, its crater worn away);
    right, a fireball in the sky with heat rays and glowing sand beneath (an airburst). Over both: no crater confirmed; Kebira crossed."""
    tk, ta, ti = T("s13", "Kebira"), T("s13", "airburst"), T("s13", "The shocked")
    gy = 640
    els = [poly([(-60, gy), (1840, gy), (1840, 1100), (-60, 1100)], "#7a6046", at=-1), ln([(-60, gy), (1840, gy)], -1, "rgba(255,236,206,.4)", 1.5, draw=False),
           ln([(889, 160), (889, 760)], -1, "rgba(255,236,206,.18)", 2, "inferred", draw=False)]
    # the glass field itself, on the ground from the first second: the melt is real, its cause is the question
    for k, (x, s) in enumerate(((680, .5), (760, .65), (840, .45), (940, .6), (1000, .45), (1050, .38))):
        els += glass_lump(x, gy + 18 + 10 * (k % 2), s, .2 + .08 * k, seed=60 + k)
    els += [lab(889, 140 + 12, "no crater confirmed", .4, BONE, 32)]
    # Kebira: a ring with a red cross, small, at the left top
    els += [circ(200, 300, 46, "none", MUTED, 3, tk, style="inferred", fx="pop"), lab(200, 380, "Kebira", tk + .1, MUTED, 26)] + cross(200, 300, tk + .5, RED, 1.6)
    # the airburst, right
    fx, fy = 1330, 300
    els += [glow(fx, fy, 160, ta, .9, "sun"), glow(fx, fy, 320, ta + .2, .4, "fire")]
    for k in range(7):
        a = math.radians(60 + 10 * k)
        els.append(ln([(fx + 60 * math.cos(a), fy + 60 * math.sin(a)), (fx + 380 * math.cos(a) * 1.0, fy + (gy - fy) * 1.0)], round(ta + .3 + .05 * k, 2), "#ffcf8a", 2.2, "inferred", dur=.5))
    els += [poly(E(fx, gy + 12, 260, 22, 30), "rgba(255,160,80,.5)", "#ffcf8a", 1.5, ta + .8, curve=True, fx="pop"), lab(fx, 820 - 30, "an airburst?", ta + .5, BONE, 30)]
    # the impact, left: a rock falling into a crater that erosion has worn away (dashed)
    els += [ln([(260, 160 + 40), (470, gy - 30)], ti, "#ffe2b4", 4, dur=.5), glow(470, gy - 20, 120, ti + .4, .8, "fire"),
            poly([(300, gy), (360, gy + 60), (470, gy + 90), (580, gy + 60), (640, gy)], "rgba(90,70,50,.6)", "#ffe2b4", 2.5, ti + .6, curve=True, style="inferred", fx="pop"),
            lab(470, 820 - 30, "an impact, crater worn away?", ti + .8, BONE, 30)]
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": False, "ridges": [], "cam": CAM, "els": els}


def s14():
    """The pectoral again, closer; a museum card on a pin, 'chalcedony', struck through in red; a gold tag replaces it: desert glass, 1990s."""
    tc, tm, ta = T("s14", "chalcedony"), T("s14", "In the"), T("s14", "hundred years ago", .2)
    cx, cy, s = 700, 500, 1.18
    els = light_shaft(560, 840, -40, 380, 1020, 900, -1, .04) + pectoral(cx, cy, s, -1)
    els += tag(1330, 210, "about 3,300 years ago", ta, GOLD, 28)
    els += [glow(1330, 380, 260, tc, .25, "lamp"), rect(1150, 300, 360, 140, "#efe6d2", "#fff6e6", 2, 6, tc, fx="pop"),
            lab(1330, 360, "Carter's card", tc + .1, "#3a3029", 26, halo=False), lab(1330, 410, "chalcedony", tc + .2, "#3a3029", 34, halo=False),
            ln([(1050, 380), (cx + 90 * s, cy - 10)], tc + .2, MUTED, 1.6, "inferred", dur=.4)]
    els += [ln([(1190, 400), (1470, 396)], tm + .6, "#d0402e", 6, dur=.4)]
    els += chip(1330, 540, "desert glass, 1990s", GOLD, tm + 1.6, 32)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s15():
    """The landing: the glass scarab glows at the left; a raw lump of the same glass on sand at the right catches the same light; a gold
    line between them; their ages."""
    tp, tk = T("s15", "A pharaoh"), T("s15", "millions")
    els = [glow(560, 470, 420, -1, .25, "lamp"), glow(1240, 560, 420, -1, .2, "lamp")]
    els += scarab(560, 470, 1.2, -1)
    els += [poly(E(1240, 640, 320, 40, 30), "#a8865c", at=-1, op=.9)] + glass_lump(1240, 640, 3.6, -1, seed=12)
    els += [ln([(700, 470), (1080, 560)], tp + .3, GOLD, 2.5, "inferred", dur=.8),
            lab(560, 800 - 40, "about 3,300 years ago", tp + .6, BONE, 28), lab(1240, 760, "29 million years old", tk, GLASS_E, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== chapter 2: black glass in Arabia
AR = (35.0, 60.0, 12.0, 31.0)
WABAR = (50.474, 21.503)


def s16():
    """Arabia: the Empty Quarter shaded as sand, Riyadh, the Wabar pin; Philby's crossing as a dotted line (schematic); a dotted lilac tag
    for the lost city of the guides' stories."""
    m = Map(*AR, rect=(200, 130, 1380, 660))
    tg, tw = T("s16", "His guides"), T("s16", "Wabar")
    els = [land_el(m.land(), -1, "#5a4834")]
    eq = [(44.5, 20.5), (46.5, 22.4), (49.0, 23.4), (52.0, 23.4), (55.2, 22.3), (56.0, 20.0), (54.0, 18.0), (51.0, 17.0), (47.5, 17.2), (45.0, 18.3)]
    els += [poly(m.path(eq), "rgba(226,192,138,.42)", SAND_L, 1.5, -1, curve=True, style="inferred"), lab(*m.p(48.6, 19.0), "the Empty Quarter", .3, SAND_L, 30)]
    rx, ry = m.p(46.71, 24.69)
    els += [dot(rx, ry, 7, BONE, .2), lab(rx - 16, ry - 14, "Riyadh", .3, MUTED, 26, "end")]
    route = [(49.6, 25.4), (49.7, 24.2), (50.0, 22.9), WABAR, (50.6, 20.2), (49.3, 19.2), (47.5, 19.8), (45.6, 20.46)]
    els += [ln(m.path(route), .5, GOLD, 3, "inferred", dur=2.0, curve=True), lab(*m.p(52.9, 25.2), "Philby, 1932 (route schematic)", .9, GOLD, 26)]
    wx, wy = m.p(*WABAR)
    els += [glow(wx, wy, 60, tw, .7, "lamp"), pin(wx, wy, "Wabar", tw, GOLD, "start", lx=24, ly=8)]
    els += tag(wx + 170, wy - 70, "a lost city?", tw + .6, LILAC, 28, "claimed")
    els += [{"k": "scale", "x": 260, "y": 770, "w": round(m.km(300), 1), "t": "300 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


def camel(x, y, s, at, face=1, c="#2a1d14", rider=True, fx="rise"):
    """A camel in silhouette (one hump), feet on y; s = 1 is about 200 units long; with a rider."""
    P = lambda a, b: (x + face * a * s, y + b * s)
    body = [P(-90, -110), P(-60, -150), P(-20, -170), P(20, -150), P(50, -126), P(70, -128), P(92, -170), P(108, -186), P(128, -182), P(132, -170),
            P(114, -162), P(100, -120), P(78, -94), P(70, -50), P(62, 0), P(54, 0), P(54, -50), P(40, -84), P(-40, -84), P(-52, -50), P(-48, 0), P(-56, 0),
            P(-66, -50), P(-78, -86), P(-92, -96)]
    els = [poly(body, c, "rgba(255,226,190,.3)", 1, curve=True)]
    if rider:
        els += [poly([P(-36, -160), P(-14, -160), P(-12, -190), P(-24, -214), P(-36, -194)], c, at=-1), circ(*P(-24, -224), 11 * s, c, at=-1)]
    return [group(els, at, fx)]


def s17():
    """Dunes at dusk: three camels with riders arrive along a crest; a ruined city drawn only in dotted lilac over the far dunes (the
    legend) fades under a veil on 'no city'; in front, two shallow craters with dark rims of black glass appear; 'a volcano?'."""
    tn, tc, tv = T("s17", "He found no"), T("s17", "craters"), T("s17", "volcano")
    els = [dune_band(470, 70, 3, "#3a2a2e"), dune_band(520, 90, 6, "#5a3e36")]
    city = []
    for k, (x, w, h) in enumerate(((560, 70, 90), (650, 50, 140), (720, 90, 70), (830, 60, 120), (900, 110, 60), (1030, 50, 100), (1100, 80, 80))):
        city.append(poly([(x, 470), (x, 470 - h), (x + w * .3, 470 - h - 14), (x + w * .6, 470 - h), (x + w, 470 - h), (x + w, 470)], "rgba(201,193,238,.04)", LILAC, 2.2,
                         .3 + .05 * k, style="claimed"))
    els += city + [lab(830, 290, "Wabar, a lost city?", .7, LILAC, 30)]
    # "He found no city": the legend is struck out (elements cannot fade, and a veil over a gradient sky shows as a box)
    els += [ln([(676, 280), (984, 280)], tn + .2, RED, 4, dur=.4)] + cross(830, 400, tn + .4, RED, 2.6, 7)
    els += [dune_band(600, 80, 9, "#7a5440", n=6), poly([(-60, 650), (1840, 650), (1840, 1100), (-60, 1100)], "#9a6c4c", at=-1)]
    els += camel(160, 600, .55, .2) + camel(290, 604, .55, .35) + camel(420, 600, .55, .5)
    for k, (cx, cy, rx, ry) in enumerate(((960, 704, 240, 44), (1450, 692, 124, 28))):
        t = round(tc + .3 * k, 2)
        els += [poly(E(cx, cy, rx, ry, 40), "#5a4430", "#2a2018", 2, t, curve=True, fx="pop"), poly(E(cx, cy + 6, rx * .7, ry * .6, 30), "#4a3828", at=t + .1, curve=True)]
        r = random.Random(k + 5)
        for q in range(38):
            a = r.uniform(0, 2 * math.pi)
            d = r.uniform(1.0, 1.25)
            els.append(dot(round(cx + rx * d * math.cos(a), 1), round(cy + ry * d * math.sin(a), 1), r.uniform(3, 5.5), BLACKG, round(t + .3 + .01 * q, 2)))
    els += [lab(960, 790, "craters, ringed with black glass", tc + .5, BONE, 30)]
    els += tag(1450, 612, "a volcano?", tv, LILAC, 28, "claimed")
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": [1500, 420, 26], "ridges": [], "cam": CAM, "els": els}


def car(x, y, s, at, c="#5d6670", fx="rise"):
    """A big car in side view, wheels on y; s = 1 is about 4.8 m at 50 units a metre (240 units long)."""
    P = lambda a, b: (x + a * s, y + b * s)
    body = [P(-120, -20), P(-118, -46), P(-90, -52), P(-60, -78), P(40, -80), P(76, -54), P(116, -48), P(120, -20)]
    els = [poly(body, c, "#c9d2da", 1.5, curve=False), poly([P(-52, -74), P(-8, -74), P(-8, -54), P(-72, -54)], "#9fb3c4", at=-1, op=.7),
           poly([P(0, -74), P(36, -74), P(64, -54), P(0, -54)], "#9fb3c4", at=-1, op=.7),
           circ(*P(-74, -14), 16 * s, "#1a1716", "#8a8a8a", 2, -1), circ(*P(74, -14), 16 * s, "#1a1716", "#8a8a8a", 2, -1)]
    return group(els, at, fx)


def s18():
    """The crater from above beside a football pitch at the same scale: an iron meteorite streaks in, the crater opens, 116 m across; the
    pitch (about 105 m) laid beside it. At the right, the Camel's Hump beside a car: about 2 tonnes."""
    tf, tb, th = T("s18", "falling iron"), T("s18", "biggest crater"), T("s18", "Camel's Hump")
    u = 3.6                                                          # units per metre for the plan
    cx, cy = 560, 470
    els = [rect(110, 150, 960, 640, "#9a7a52", "rgba(255,236,206,.25)", 1.5, 14, -1), lab(1040, 196, "the site, from above", .4, "#3a2c20", 28, "end", halo=False)]
    r = random.Random(8)
    for k in range(60):
        els.append(dot(round(r.uniform(130, 1050), 1), round(r.uniform(170, 770), 1), r.uniform(1.5, 3), "#b8956a", -1, op=.6))
    els += [ln([(140, 140), (cx - 20, cy - 20)], tf, "#ffe2b4", 6, dur=.4), glow(cx, cy, 200, tf + .4, .9, "fire")]
    R_ = 58 * u
    els += [circ(cx, cy, R_ * 1.12, "rgba(27,23,20,.55)", at=tf + .6, fx="pop"), circ(cx, cy, R_, "#6a5034", "#e8d3a8", 2.5, tf + .6, fx="pop"),
            circ(cx, cy, R_ * .7, "#5a4430", at=tf + .7)]
    els += [ln([(cx - R_, cy + R_ + 30), (cx + R_, cy + R_ + 30)], tb, BONE, 2.5, dur=.6), ln([(cx - R_, cy + R_ + 18), (cx - R_, cy + R_ + 42)], tb, BONE, 2, draw=False),
            ln([(cx + R_, cy + R_ + 18), (cx + R_, cy + R_ + 42)], tb, BONE, 2, draw=False), lab(cx, cy + R_ + 76, "116 m", tb + .2, BONE, 32)]
    pw, ph = 105 * u, 68 * u
    px = cx - pw / 2
    py = cy - ph / 2
    els += [rect(px, py, pw, ph, "none", "#ffffff", 2.5, 2, tb + .8, fx="pop", style="inferred"), ln([(cx, py), (cx, py + ph)], tb + .9, "#ffffff", 2, "inferred", dur=.3),
            circ(cx, cy, 9.15 * u, "none", "#ffffff", 2, tb + 1.0, style="inferred"), lab(cx, py - 18, "a football pitch, same scale", tb + 1.1, "#ffffff", 26)]
    # the Camel's Hump and a big car, side view at 50 units a metre: about 1.3 m of iron (iron is dense) beside a 4.8 m car
    gy = 640
    els += [ln([(1130, gy), (1690, gy)], th, "rgba(255,236,206,.4)", 2, draw=False)]
    hump = [(1183, gy), (1187, gy - 14), (1199, gy - 26), (1218, gy - 31), (1237, gy - 25), (1247, gy - 11), (1250, gy)]
    els += [group([poly(hump, "#4a4642", "#9a9590", 2, curve=True), ln([(1200, gy - 22), (1222, gy - 28)], -1, "#bdb6ae", 2, draw=False, op=.6)], th, "rise"),
            car(1480, gy, 1.0, th + .4), lab(1216, gy + 50, "the Camel's Hump", th + .2, BONE, 28), lab(1480, gy + 50, "a car", th + .5, MUTED, 26),
            lab(1400, 520, "about 2 tonnes each", th + .9, GOLD, 30)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s19():
    """Two equal flashes on a dark ground: Wabar, a falling iron; Hiroshima, 1945; an equals sign; about the same energy."""
    ta, th = T("s19", "energy"), T("s19", "Hiroshima")
    els = [ln([(160, 620), (1620, 620)], -1, "rgba(255,236,206,.25)", 2, draw=False)]
    for x, t, name in ((520, .4, "Wabar, a falling iron"), (1260, th, "Hiroshima, 1945")):
        els += [glow(x, 480, 300, t, .95, "fire"), glow(x, 480, 130, t + .1, .9, "sun"), lab(x, 700, name, t + .3, BONE, 32)]
    els += [ln([(570, 410), (380, 210)], .3, "#ffe2b4", 5, dur=.4)]
    els += [lab(889, 500, "=", th + .6, GOLD, 90, st="big"), lab(889, 230, "about the same energy", ta + .3, GOLD, 34)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s20():
    """What the ground holds, under a lens: a bead of black glass with sand grains in it; tiny bright droplets of iron and nickel inside;
    a block of white 'instant rock' (sand shocked into stone); a green tick by each; a falling iron explains it."""
    tg, td, ts, tn = T("s20", "Black glass"), T("s20", "droplets"), T("s20", "shocked"), T("s20", "Nothing")
    xs, ly, R_ = (400, 889, 1378), 400, 175
    els = []
    for k, x in enumerate(xs):                                  # three lenses, empty at first: what the ground holds, one find in each
        els += [circ(x, ly, R_, "rgba(18,13,10,.6)", BONE, 3, round(.3 + .15 * k, 2), fx="pop")]
    r = random.Random(7)
    # 1. black glass: a glossy bead of melted dune sand and meteorite iron, sand grains caught in it
    x = xs[0]
    els += [poly(E(x, ly, 120, 96, 40), "#241e1a", "#a4a4b4", 3, tg, curve=True, fx="pop"), poly(E(x - 40, ly - 40, 40, 22, 20), "#9a9aa8", at=tg + .1, op=.4, curve=True)]
    for k in range(12):
        a, d = r.uniform(0, 2 * math.pi), r.uniform(.15, .78)
        els.append(circ(round(x + 120 * d * math.cos(a), 1), round(ly + 96 * d * math.sin(a), 1), r.uniform(6, 10), "#c9a36c", at=round(tg + .3 + .03 * k, 2), op=.85))
    # 2. droplets of iron and nickel metal, bright beads in the glass
    x = xs[1]
    els += [poly(E(x, ly, 130, 104, 40), "#1d1916", "#5a5a64", 2, td - .3, curve=True, fx="pop")]
    for k, (dx, dy, rr) in enumerate(((-60, -30, 16), (10, -50, 11), (55, 10, 20), (-20, 40, 13), (-80, 30, 9), (80, -40, 9), (20, 70, 8))):
        t = round(td + .08 * k, 2)
        els += [glow(x + dx, ly + dy, rr * 3, t, .6, "lamp"), circ(x + dx, ly + dy, rr, "#d9dde2", "#ffffff", 1.2, t, fx="pop"),
                circ(x + dx - rr * .35, ly + dy - rr * .35, rr * .3, "#ffffff", at=t, op=.8)]
    # 3. sand shocked into rock: a pale block with fine shock lines
    x = xs[2]
    blk = [(x - 100, ly - 70), (x + 40, ly - 104), (x + 110, ly - 20), (x + 80, ly + 96), (x - 60, ly + 100), (x - 112, ly + 20)]
    els += [poly(blk, "#ece6d8", "#ffffff", 2, ts, fx="pop")]
    for k in range(7):
        d = -80 + 26 * k
        seg = clip_seg((x - 160, ly + d - 40), (x + 160, ly + d + 10), blk, .9)
        if seg:
            els.append(ln(list(seg), round(ts + .2 + .05 * k, 2), "#b8ae9c", 2, dur=.3))
    # the names, each with its tick
    for x, t, name, c in ((xs[0], tg, "black glass", BONE), (xs[1], td, "iron-nickel droplets", "#e8ecf0"), (xs[2], ts, "sand shocked into rock", BONE)):
        w = len(name) * 28 * .55
        els += [lab(x + 18, 640, name, t + .4, c, 28), tick(x + 18 - w / 2 - 28, 632, t + .7)]
    els += [lab(889, 740, "a falling iron explains it", tn, GOLD, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s21():
    """Sand grains as batteries: a grain beside a gauge that fills in the dark; a flash empties it at once; it refills slowly; a time line
    from 1600 to today with a gold band about 1670 to 1750: about 300 years ago."""
    tb, te, tr = T("s21", "batteries"), T("s21", "emptied"), T("s21", "From the charge")
    els = [poly(E(330, 360, 150, 118, 40), SAND, BONE, 2, .3, curve=True, fx="pop"), lab(330, 540, "a grain of sand", .6, BONE, 30)]
    els += [rect(560, 180, 110, 360, "rgba(18,13,10,.55)", BONE, 2.5, 10, .5, fx="pop"), rect(590, 154, 50, 26, BONE, r=4, at=.5)]
    seg = lambda k, at, c: rect(574, 520 - 40 * (k + 1), 82, 32, c, r=5, at=at, fx="pop")
    els += [seg(k, round(tb + .25 * k, 2), "#8fd9b0") for k in range(8)]
    els += [lab(720, 300, "charging in the dark", tb + .3, GREEN, 28, "start")]
    els += [glow(330, 360, 260, te, .95, "fire"), rect(568, 186, 94, 344, "#171310", r=8, at=te + .2, fx="pop"), lab(720, 360, "the impact: empty", te + .3, AMBER, 28, "start")]
    els += [seg(k, round(te + 1.0 + .35 * k, 2), AU) for k in range(3)]
    X = lambda yr: round(240 + (yr - 1600) / (2025 - 1600) * 1300, 1)
    els += [axis(X(1600), X(2025), 680, [(X(1600), "1600"), (X(1700), "1700"), (X(1800), "1800"), (X(1900), "1900"), (X(2000), "2000")], tr - .6),
            band(X(1672), X(1748), 640, 16, AU, tr, "about 300 years ago", AU)]          # 290 +/- 38 years before about 2000
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s22():
    """The sand sheet from the side with two craters; a big dune creeps in from the left (dunes move 1 to 2 m a year) and covers the
    smaller crater; 2008: buried."""
    tm, tb = T("s22", "moving"), T("s22", "vanished")
    gy = 620
    surf = [(-60, gy), (300, gy), (360, gy + 40), (520, gy + 60), (680, gy + 40), (740, gy), (1000, gy), (1080, gy + 60), (1300, gy + 90), (1520, gy + 60),
            (1600, gy), (1840, gy)]
    els = [poly(surf + [(1840, 1100), (-60, 1100)], "#a8825a", "rgba(255,236,206,.4)", 1.5, -1, curve=True),
           lab(530, gy + 140, "a crater", .3, BONE, 26), lab(1300, gy + 170, "the biggest crater", .4, BONE, 26)]
    dune = [(-60, gy), (-60, gy - 220), (120, gy - 250), (330, gy - 180), (560, gy - 60), (720, gy - 10), (760, gy)]
    els += [poly(dune, "#c99a66", "rgba(255,236,206,.5)", 1.5, tm, curve=True, fx="rise", dur=2.2),
            arrow([[180, gy - 300], [460, gy - 300]], tm + .3, BONE, 3, dur=.6), lab(320, gy - 330, "dunes move 1 to 2 m a year", tm + .5, BONE, 28)]
    els += [poly([(280, gy), (360, gy + 40), (520, gy + 60), (680, gy + 40), (760, gy), (700, gy - 30), (520, gy - 50), (360, gy - 30)], "#c99a66", at=tb, curve=True, fx="rise", dur=1.0)]
    els += tag(530, gy - 120, "2008: buried", tb + .5, BLUE, 28)
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": [1500, 220, 30], "ridges": [], "cam": CAM, "els": els}


def s23():
    """Night over the Empty Quarter: stars; a shooting star streaks down to the dunes; a small camp fire with two figures and a camel; the
    crater rim catches the starlight."""
    ts = T("s23", "Philby went")
    els = [dune_band(560, 80, 4, "#1d1820"), dune_band(620, 70, 8, "#2a2228"), poly([(-60, 660), (1840, 660), (1840, 1100), (-60, 1100)], "#2e2520", at=-1)]
    els += [poly(E(1180, 700, 230, 40, 40), "#1a1512", "#6a5a6a", 2, -1, curve=True)]
    els += [ln([(260, 150), (980, 560)], ts, "#fff6e0", 3, dur=.9), glow(980, 560, 60, ts + .8, .8, "lamp"), glow(980, 560, 160, ts + .9, .3, "blue")]
    els += [glow(420, 690, 120, -1, .7, "fire"), circ(420, 700, 10, "#ffcf6a", at=-1)]
    els += [person(370, 702, 70, -1, "#151012"), person(470, 704, 64, -1, "#151012")] + camel(560, 704, .45, -1, -1, "#151012", rider=False)
    els += [lab(889, 800 - 40, "a fallen star", ts + 1.2, GOLD, 32)]
    return {"base": "sky", "tod": "night", "ground": 1100, "sun": False, "moon": [1500, 200, 22], "ridges": [], "cam": CAM, "els": els}


# ================================================================== chapter 3: the skeletons of Mohenjo-daro
def iso_p(x, y, z, ox, oy, S, az=-30, el=.5):
    """The screen point of an iso world point (as kit.js EL.iso draws it, with no spin)."""
    a = math.radians(az)
    ca, sa = math.cos(a), math.sin(a)
    rx, rz = x * ca - z * sa, x * sa + z * ca
    c30 = math.cos(math.pi / 6)
    return (round(ox + (rx - rz) * c30 * S, 1), round(oy - y * S + (rx + rz) * el * S, 1))


CITY = dict(ox=820, oy=430, S=5.2, az=-30, el=.5)


def s24():
    """Mohenjo-daro from above at an angle: a grid of straight streets between blocks of brick houses with courtyards; the citadel mound
    behind; wells and a covered drain pop as named; small people; a locator map: the Indus to the sea, Mohenjo-daro in Pakistan."""
    tb, tw, td, tp = T("s24", "fired"), T("s24", "wells"), T("s24", "covered"), T("s24", "people")
    items = [{"t": "slab", "x0": -70, "x1": 70, "z0": -60, "z1": 70, "y": 0, "c": "#8a6a4a"}]
    r = random.Random(5)
    for bx in range(-3, 3):
        for bz in range(-2, 3):
            x0, z0 = bx * 20 + 2, bz * 22 + 2
            for q in range(2):
                for p in range(2):
                    w, d = r.uniform(6, 8), r.uniform(7, 9.5)
                    h = r.uniform(2.2, 4.4)
                    items.append({"t": "box", "x": x0 + 4 + p * 9, "z": z0 + 4.5 + q * 10, "y": 0, "w": w, "d": d, "h": h, "c": "#b4774e", "edge": "rgba(255,226,190,.35)"})
    items.append({"t": "box", "x": -8, "z": -56, "y": 0, "w": 70, "d": 14, "h": 9, "c": "#9a6a48", "edge": "rgba(255,226,190,.3)"})   # the citadel mound
    items.append({"t": "box", "x": -8, "z": -56, "y": 9, "w": 16, "d": 8, "h": 1.2, "c": "#6fa8c0", "edge": "rgba(255,236,206,.5)"})   # its great bath
    o = CITY
    els = [{"k": "iso", "x": o["ox"], "y": o["oy"], "s": o["S"], "az": o["az"], "el": o["el"], "items": items, "in": -1}]
    P = lambda x, z, y=0: iso_p(x, y, z, o["ox"], o["oy"], o["S"], o["az"], o["el"])
    # the streets run between the house blocks, at x = 20k + 0.5 and z = 22k + 0.5 (box x, z are centres): wells and people stand in them
    for k, (x, z) in enumerate(((-39.5, 10), (0.5, -11), (20.5, 32), (-48, 0.5), (40.5, -10), (-10, 44.5))):
        px, py = P(x, z)
        els += [circ(px, py, 9, "#2a4652", "#9fd0ff", 2.5, round(tw + .12 * k, 2), fx="pop")]
    d0, d1 = P(-62, 22.5), P(62, 22.5)
    els += [ln([d0, d1], td, "#6a5a4a", 9, dur=1.0), ln([d0, d1], td + .1, "#c9b08a", 3, "inferred", dur=1.0)]
    for k, (x, z) in enumerate(((-39.5, -4), (2, 22.5), (20.5, -22), (-18, 44.5), (40.5, 44), (-58, -21.5))):
        px, py = P(x, z)
        els.append(figure(px, py, 18, round(tp + .08 * k, 2), "#f0e2c8"))
    wx, wy = P(40.5, -10)                                         # the labelled well, and the drain's end, with labels outside the city
    dx, dy = P(62, 22.5)
    els += [lab(270, 760, "houses of fired brick", tb, BONE, 28, "start"),
            ln([(wx + 12, wy - 4), (1392, 398)], tw + .3, "#9fd0ff", 1.6, dur=.4), lab(1404, 408, "wells", tw + .4, BLUE, 30, "start"),
            ln([(dx + 8, dy + 4), (1392, 590)], td + .4, "#e8d3a8", 1.6, dur=.4), lab(1404, 600, "covered drains", td + .5, "#e8d3a8", 30, "start")]
    m = Map(62.0, 80.0, 22.0, 36.0, rect=(110, 132, 300, 250))
    mx, my = m.p(68.14, 27.33)
    els += window(100, 126, 320, 262, [land_el(m.land(), -1, "#6a5a44"), ln(m.path(INDUS), -1, "#6fb6d6", 4, draw=False, curve=True),
                                       circ(mx, my, 10, GOLD, "#fff3c8", 2, .3)], at=.2, sea="#173342")
    els += [lab(260, 420, "Mohenjo-daro, Pakistan", .4, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def book(x, y, w, h, at, c="#5a4a60", style="claimed", edge=LILAC, rot=0):
    els = [rect(x, y, w, h, "rgba(201,193,238,.05)", edge, 2.2, 4, style=style), ln([(x + 14, y + 6), (x + 14, y + h - 6)], -1, edge, 1.6, style, draw=False)]
    return group(els, at, "pop", tr="rotate(%d %.1f %.1f)" % (rot, x + w / 2, y + h / 2) if rot else None)


def trefoil(cx, cy, r, at, c=LILAC, style="claimed"):
    """The radiation sign, drawn as an outline: three blades and a hub."""
    els = [circ(cx, cy, r * .18, "none", c, 2.4, style=style)]
    for k in range(3):
        a0 = math.radians(-90 + 120 * k - 30)
        a1 = math.radians(-90 + 120 * k + 30)
        pts = [(cx + r * .3 * math.cos(a0), cy + r * .3 * math.sin(a0))] + [(cx + r * math.cos(a0 + (a1 - a0) * q / 8), cy + r * math.sin(a0 + (a1 - a0) * q / 8)) for q in range(9)] + \
              [(cx + r * .3 * math.cos(a1), cy + r * .3 * math.sin(a1))]
        els.append(poly(pts, "rgba(201,193,238,.05)", c, 2.4, style=style))
    return group(els, at, "pop")


def s25():
    """The claim, drawn only in dotted lilac: the same street at night, a stack of paperback books, the story told online, a dotted
    radiation sign with a question mark. No bodies are drawn."""
    ts, tr = T("s25", "skeletons"), T("s25", "radioactive")
    els = []
    gl = 660                                                          # a street of brick house fronts, drawn only in dotted lines (the claim)
    for k, (x, w, h) in enumerate(((400, 150, 170), (565, 190, 215), (770, 160, 150), (945, 205, 195), (1165, 165, 235))):
        t = round(.2 + .08 * k, 2)
        els += [rect(x, gl - h, w, h, "rgba(201,193,238,.04)", LILAC, 2, 2, t, style="claimed"),
                rect(x + w / 2 - 22, gl - 76, 44, 76, "none", LILAC, 2, 2, t, style="claimed"),                      # a doorway
                rect(x + w / 2 - 18, gl - h + 30, 36, 24, "none", LILAC, 1.6, 2, t, style="claimed")]              # a small window
    els += [ln([(330, gl), (1400, gl)], .4, LILAC, 2, "claimed", dur=.8)]
    for k in range(4):
        els.append(book(150, 330 - 34 * k, 190, 30, round(.5 + .1 * k, 2)))
    els += [lab(245, 400, "popular books", .9, LILAC, 26)]
    els += tag(880, 330, "the story told online", ts, LILAC, 30, "claimed")
    els += [trefoil(1440, 300, 80, tr), lab(1440, 430, "radioactive?", tr + .3, LILAC, 32)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def disc(x, y, n, at, r=34, c=BONE, fill="rgba(245,236,220,.1)", size=30):
    return [circ(x, y, r, fill, c, 2.5, at, fx="pop"), lab(x, y + size * .36, str(n), at + .1, c, size, halo=False)]


def s26():
    """The excavators' plan, schematic: three quarters lettered HR, DK, VS; the groups appear only as numbered discs, where Dales (1964)
    places them: in HR, 14 in a room of House V, 3 in a courtyard, 1 in Deadman Lane; in DK, 9 in Block 10A (at least 5 children) and 2 on
    a well room's stairs; in VS, 6 in a lane. The small groups pop on 'small groups'. A field notebook: 1922 to 1931, about 37."""
    tf, tg, t14, t9 = T("s26", "Between"), T("s26", "small groups"), T("s26", "Fourteen"), T("s26", "Nine")
    els = [rect(110, 150, 1080, 640, "#2b2219", "rgba(255,236,206,.3)", 2, 12, -1)]
    # three quarters of the city as tidy grids of rooms (schematic), with lanes between some of them
    quarters = {"HR": ((170, 210, 420, 300), [(186, 88), (282, 88), (408, 82), (498, 80)], [(258, 78), (344, 74), (426, 70)]),
                "DK": ((640, 190, 490, 330), [(656, 104), (768, 104), (880, 104), (992, 120)], [(244, 82), (334, 82), (424, 82)]),
                "VS": ((300, 540, 440, 220), [(316, 96), (420, 96), (524, 96), (628, 96)], [(592, 64), (690, 60)])}
    for name, ((x, y, w, h), cols, rows) in quarters.items():
        els += [rect(x, y, w, h, "rgba(245,236,220,.03)", "rgba(245,236,220,.35)", 1.5, 4, -1)]
        for cx_, cw in cols:
            for ry_, rh in rows:
                if name == "HR" and ry_ == 258 and cx_ == 186:
                    continue                                             # the corner kept clear for the quarter's name
                els.append(rect(cx_, ry_, cw, rh, "none", "rgba(245,236,220,.2)", 1.2, 2, -1))
        els.append(lab(x + 20, y + 36, name, .3, MUTED, 30, "start"))
    # the groups, never bodies: numbered discs where Dales (1964) places them
    els += disc(326, 381, 14, t14, 32)                                   # HR, a room of House V
    els += disc(538, 381, 3, tg, 24, size=24) + disc(389, 300, 1, tg + .15, 22, size=24)    # HR: a courtyard; Deadman Lane (the lane at x 370 to 408)
    els += disc(820, 465, 9, t9, 32) + [lab(890, 558, "at least 5 children", t9 + .5, "#e8d3c4", 24)]   # DK, Block 10A
    els += disc(1052, 285, 2, tg + .3, 22, size=24)                     # DK, the stairs of a well room
    els += disc(470, 673, 6, tg + .45, 26, size=26)                     # VS, a lane
    nb = [rect(1260, 230, 380, 480, "#e9dfca", "#fff6e6", 2, 6, tf, fx="pop"), ln([(1450, 236), (1450, 704)], tf, "#b9ab94", 2, draw=False)]
    for k in range(8):
        nb.append(ln([(1290, 300 + 46 * k), (1430, 300 + 46 * k)], tf, "#9a8c78", 2, draw=False))
        nb.append(ln([(1470, 300 + 46 * k), (1610, 300 + 46 * k)], tf, "#9a8c78", 2, draw=False))
    els += nb + [lab(1450, 200, "field records", tf + .2, MUTED, 26), lab(1355, 420, "1922 to 1931", tf + .4, "#3a3029", 26, halo=False),
                 lab(1545, 420, "about 37", tf + .9, "#3a3029", 30, halo=False)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s27():
    """The mound cut open, schematic: debris on top, the later city with its broken walls, the earlier city below. The numbered groups sit
    at different depths, as Dales (1964) reads the records: 6 in a lane, 14 partly over a ruined wall, 3 and 1 in the debris of places
    already in ruins; the 9 dashed (Mackay doubted its date). An open book whose pages turn back: different levels, different times."""
    tn, tb, tp, tr = T("s27", "not all found"), T("s27", "Digging"), T("s27", "different pages"), T("s27", "rubble")
    x0, x1 = 560, 1680
    # the mound cut open: debris on top, the later city, the earlier city below (schematic); ruined walls stand up into the debris
    layers = [(220, "#7c6a58", "debris"), (330, "#6e5440", "later"), (500, "#5a4434", "earlier"), (660, "#46362a", "")]
    els = []
    for k, (y, c, name) in enumerate(layers):
        h = (layers[k + 1][0] if k + 1 < len(layers) else 800) - y
        els.append(rect(x0, y, x1 - x0, h, c, at=round(.2 + .15 * k, 2), fx="fill", dur=.5))
        if k:
            els.append(ln([(x0, y), (x1, y)], round(.2 + .15 * k, 2), "rgba(255,226,190,.25)", 1.5, "inferred", draw=False))
        if name:
            els.append(lab(x1 - 20, y + 36, name, round(.4 + .15 * k, 2), BONE, 26, "end"))
    for k, (x, top) in enumerate(((700, 262), (960, 300), (1180, 250), (1420, 286))):              # brick walls of the later city, broken off
        els.append(rect(x, top, 34, 500 - top, BRICK_D, BRICK_L, 1.5, 2, round(.5 + .1 * k, 2), fx="fill", dur=.4))
    # the groups at different depths: 6 in a lane between walls, 14 partly over a ruined wall, the 9 lower and dashed (its date is doubtful)
    els += disc(830, 410, 6, tn, 28) + disc(977, 268, 14, tn + .25, 30)
    els += [circ(1300, 450, 30, "rgba(245,236,220,.06)", BONE, 2.5, tn + .5, fx="pop", style="inferred"), lab(1300, 461, "9", tn + .6, BONE, 30, halo=False)]
    # and some in the rubble of houses already in ruins
    els += disc(1300, 262, 3, tr, 24, size=24) + disc(1530, 250, 1, tr + .2, 22, size=24)
    # the book
    bx, by = 300, 470
    els += [poly([(bx - 200, by - 120), (bx, by - 100), (bx, by + 160), (bx - 200, by + 140)], "#e9dfca", "#fff6e6", 2, tb, fx="pop"),
            poly([(bx, by - 100), (bx + 200, by - 120), (bx + 200, by + 140), (bx, by + 160)], "#e9dfca", "#fff6e6", 2, tb, fx="pop")]
    for k in range(4):
        t = round(tb + .6 + .35 * k, 2)
        els.append(poly([(bx, by - 100), (bx - 160 + 30 * k, by - 128 + 6 * k), (bx - 160 + 30 * k, by + 132 + 6 * k), (bx, by + 160)], "#d8ccb2", "#fff6e6", 1.5, t, fx="pop"))
    els += [lab(bx, by + 210, "turning back the pages", tb + .4, BONE, 26)]
    els += tag(1120, 760 - 20, "different levels, different times", tp + 1.0, GOLD, 28)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def paper(x, y, w, h, at, title=None, lines=6, c="#e9dfca", fx="pop", rot=0, seed=1, l0=50, tsize=24):
    """A sheet of paper with ruled lines (the first at y + l0) and an optional title on top."""
    r = random.Random(seed)
    els = [rect(x, y, w, h, c, "#fff6e6", 1.5, 4)]
    for k in range(lines):
        yy = y + l0 + (h - l0 - 20) * k / max(1, lines)
        els.append(ln([(x + 20, yy), (x + 20 + (w - 40) * r.uniform(.55, 1), yy)], -1, "#9a8c78", 3, draw=False))
    out = [group(els, at, fx, tr="rotate(%d %.1f %.1f)" % (rot, x + w / 2, y + h / 2) if rot else None)]
    if title:
        out.append(lab(x + w / 2, y + 34, title, at + .1, "#3a3029", tsize, halo=False))
    return out


def stamp(x, y, t, at, c="#c84a3a", size=30, rot=-6):
    w = len(t) * size * .6 + 40
    els = [rect(x - w / 2, y - size, w, size * 1.6, "rgba(200,74,58,.08)", c, 3, 6), lab(x, y + size * .2, t, -1, c, size, scl=True, halo=False)]
    return group(els, at, "pop", tr="rotate(%d %.1f %.1f)" % (rot, x, y))


def s28():
    """Documents on a desk under a lamp: a 1940s report with a dotted 'a massacre?'; two field notebooks, 'a tragedy' and 'buried quickly';
    then Dales's 1964 paper slides in front: a dashed note (a couple killed in place) and two stamps (no destruction layer, no great fire)."""
    tw, ta, tb, td = T("s28", "Mortimer"), T("s28", "tragedy"), T("s28", "buried"), T("s28", "George")
    tc, tl, tf = T("s28", "couple"), T("s28", "layer of destruction"), T("s28", "great fire")
    els = [glow(889, 300, 600, -1, .3, "lamp"), rect(100, 560, 1580, 260, "#2a2018", at=-1, op=.9)]
    els += paper(160, 210, 330, 420, .4, "1940s report", seed=3, rot=-3, tsize=26) + tag(325, 690, "a massacre?", tw + .5, LILAC, 28, "claimed")
    els += paper(620, 240, 270, 340, ta - .4, "a tragedy", seed=4, l0=80, tsize=28)
    els += paper(930, 240, 270, 340, tb - .3, "buried quickly", seed=5, l0=80, tsize=28)
    els += [lab(910, 630, "the first excavators", ta + .3, MUTED, 26)]
    els += paper(1260, 200, 330, 430, td, "Dales, 1964", seed=6, rot=4, lines=3, l0=70, tsize=26)
    els += tag(1425, 700, "a couple killed in place?", tc, BONE, 24, "inferred")
    els += [stamp(1425, 430, "no destruction layer", tl, "#d0402e", 24, -5), stamp(1425, 540, "no great fire", tf, "#d0402e", 24, -5)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s29():
    """Three dashed boxes, empty, labelled as said (laboratory, sample, number), each with a faint lilac question mark; above them a
    radiation counter whose needle rests at zero; no measurement published."""
    tl, ts, tn = T("s29", "laboratory"), T("s29", "sample"), T("s29", "number")
    els = []
    for k, (x, t, name) in enumerate(((330, tl, "laboratory"), (889, ts, "sample"), (1448, tn, "number"))):
        els += [rect(x - 190, 420, 380, 300, "rgba(201,193,238,.04)", LILAC, 2.5, 14, round(.3 + .1 * k, 2), style="inferred", fx="pop"),
                lab(x, 770, name, t, BONE, 30), lab(x, 610, "?", t + .2, mix(LILAC, t=.6), 110, st="big")]
    cx, cy = 889, 250
    els += [rect(cx - 150, cy - 90, 300, 170, "#2c2620", "#cbbca8", 2.5, 12, .2, fx="pop"), poly(arc(cx, cy + 40, 110, 100, 200, 340, 20) + [(cx, cy + 40)], "#e9e2d0", at=.3),
            ln([(cx, cy + 40), (cx - 96, cy - 6)], .5, "#c84a3a", 4, draw=False), lab(cx + 220, cy + 10, "no measurement published", .7, BONE, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s30():
    """The Indus plain at dusk, the river, the lights of old towns. Across the sky, the monsoon rains as a line through time, steady and
    then falling from about 3,900 years ago; the old towns' lights go out one by one while others appear further east, over generations;
    in front, a family walks away along the river bank, a child holding a hand."""
    tf, tm, tg, tp = T("s30", "From about"), T("s30", "monsoon"), T("s30", "generations"), T("s30", "These were")
    els = [poly([(-60, 560), (1840, 540), (1840, 1100), (-60, 1100)], "#5a4a38", at=-1)]
    river = [(-60, 700), (300, 680), (700, 690), (1100, 670), (1500, 680), (1840, 660)]
    els += [ln(river, -1, "#4f93b3", 22, draw=False, curve=True)]
    # the monsoon rains, drawn across the sky as a line through time: steady, then falling from about 3,900 years ago
    x0, xb, x1 = 200, 700, 1560
    rain = [(x0, 210), (450, 206), (xb, 210)] + [(xb + (x1 - xb) * k / 8, 210 + 92 * (1 - math.cos(math.pi * k / 8)) / 2) for k in range(1, 9)]
    els += [ln([(x0, 320), (x1, 320)], .3, "rgba(255,236,206,.25)", 1.5, draw=False),
            ln([(xb, 180), (xb, 320)], tf, BONE, 2, "inferred", dur=.4), lab(xb, 356, "about 3,900 years ago", tf + .2, BONE, 28),
            lab(x0, 182, "monsoon rains", tm - .4, BLUE, 28, "start"), ln(rain, tm, BLUE, 4, dur=2.2, curve=True)]
    for k, x in enumerate((200, 420, 640)):                             # the old towns' lights go out, one by one (veils match the plain)
        els += [glow(x, 600, 40, -1, .7, "lamp"), veil(x - 40, 560, 80, 80, round(tg - .6 + .3 * k, 2), .85, "#5a4a38", 40, 1.0)]
    for k, x in enumerate((1180, 1380, 1580)):
        els += [glow(x, 590, 40, round(tg + .4 * k, 2), .7, "lamp")]
    els += [arrow([[760, 520], [1100, 520]], tg, BONE, 2.5, dur=.8), lab(930, 490, "over generations, eastward", tg + .3, BONE, 26)]
    els += walker(760, 782, 120, tp, "#1e1712", 1) + walker(840, 784, 112, tp + .1, "#1e1712", 1) + walker(808, 790, 70, tp + .2, "#1e1712", 1)
    els += [ln([(828, 742), (842, 728)], tp + .3, "#1e1712", 5, draw=False)]
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": [1460, 470, 26], "ridges": [], "cam": CAM, "els": els}


# ================================================================== chapter 4: walls of melted stone
def hills(seed, y, amp, c, at=-1, n=8):
    r = random.Random(seed)
    pts = [(-60, 1100)] + [(-60 + 1900 * k / n, y - amp * (.5 + .5 * math.sin(k * 1.1 + seed)) * r.uniform(.7, 1.1)) for k in range(n + 1)] + [(1840, 1100)]
    return poly(pts, c, at=at, curve=True)


def s31():
    """A Scottish hill at dusk in layers of dim ridges; on its top the low ring of a ruined rampart, patches of it glinting like dark glass;
    a walker for scale; about 200 vitrified forts in Europe."""
    tv, tn = T("s31", "vitrified"), T("s31", "two hundred")
    els = [hills(2, 520, 90, "#2c2a3a"), hills(5, 580, 120, "#363040")]
    hill = [(-60, 1100), (-60, 760), (300, 700), (620, 520), (820, 430), (1000, 420), (1180, 470), (1450, 620), (1840, 720), (1840, 1100)]
    els += [poly(hill, "#3f3a34", "rgba(255,226,190,.2)", 1.5, -1, curve=True)]
    ramp = arc(910, 432, 200, 34, 180, 360, 30)
    els += [ln(ramp, -1, "#6e6458", 16, draw=False, curve=True), ln(arc(910, 436, 200, 40, 0, 180, 30), -1, "#5a5248", 12, draw=False, curve=True)]
    r = random.Random(4)
    for k in range(14):
        a = r.uniform(180, 360)
        x, y = 910 + 200 * math.cos(math.radians(a)), 432 + 34 * math.sin(math.radians(a))
        els += [poly(E(x, y, r.uniform(10, 20), r.uniform(4, 7), 10), "#1e2428", "#8fb0c0", 1.2, round(tv + .06 * k, 2), op=.95), glow(round(x, 1), round(y, 1), 26, round(tv + .06 * k, 2), .35, "blue")]
    els += walker(1260, 520, 44, .4, "#1a1614", -1)
    els += [lab(910, 330, "a vitrified fort", tv + .2, BONE, 30)]
    els += tag(1380, 230, "about 200 in Europe", tn, GOLD, 30)
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": [300, 470, 22], "ridges": [], "cam": CAM, "els": els}


def s32():
    """Close on a chunk of the rampart: stones fused together by dark glass with bubbles and drips; a thermometer climbs to about 1,000
    degrees and a clock face reads for hours; then a dotted lilac flash: an atomic flash?"""
    tt, th, ta = T("s32", "thousand"), T("s32", "hours"), T("s32", "atomic")
    r = random.Random(9)
    els = [glow(560, 470, 420, -1, .18, "lamp")]
    for k in range(9):
        x, y = 360 + (k % 3) * 150 + r.uniform(-20, 20), 330 + (k // 3) * 130 + r.uniform(-15, 15)
        els.append(poly(E(x, y, r.uniform(60, 80), r.uniform(44, 58), 14), "#7a7066", "#b8aa98", 1.5, -1, curve=True))
    glassy = [(300, 300), (420, 280), (560, 300), (700, 290), (760, 400), (720, 560), (760, 640), (600, 680), (420, 660), (300, 600), (280, 450)]
    els += [poly(glassy, "rgba(30,38,44,.75)", "#8fb0c0", 2, -1, curve=True, op=.9)]
    for k in range(12):
        els.append(circ(round(r.uniform(320, 720), 1), round(r.uniform(320, 640), 1), r.uniform(3, 8), "none", "#9fc0d0", 1.4, -1, op=.7))
    for k in range(5):
        x = 360 + 80 * k
        els.append(poly([(x - 8, 660), (x + 8, 660), (x + 3, 700), (x, 712), (x - 3, 700)], "#2a3238", "#8fb0c0", 1.2, -1))
    els += [lab(530, 760, "stones fused by glass", .4, BONE, 28)]
    tx, ty0, ty1 = 1050, 640, 220
    els += [rect(tx - 20, ty1 - 10, 40, ty0 - ty1 + 30, "rgba(245,236,220,.06)", BONE, 2.5, 20, tt - .4, fx="pop"), circ(tx, ty0 + 28, 36, "#e05a3a", BONE, 2.5, tt - .4, fx="pop"),
            rect(tx - 9, ty1 + 40, 18, ty0 - ty1 - 30, "#e05a3a", at=tt, fx="fill", dur=1.0), lab(tx + 40, ty1 + 56, "about 1,000 °C", tt + .6, AMBER, 28, "start")]
    cx, cy = 1260, 520
    els += [circ(cx, cy, 70, "rgba(245,236,220,.05)", BONE, 3, th - .3, fx="pop"), ln([(cx, cy), (cx, cy - 52)], th, BONE, 4, draw=False),
            ln([(cx, cy), (cx + 40, cy + 14)], th, BONE, 4, draw=False), ln(arc(cx, cy, 82, 82, -90, 200, 24), th, GOLD, 4, dur=1.2, curve=True),
            lab(cx, cy + 116, "for hours", th + .3, GOLD, 28)]
    els += [glow(1500, 260, 140, ta, .3, "blue"), poly([(1500, 150), (1530, 230), (1610, 240), (1540, 280), (1570, 360), (1500, 310), (1430, 360), (1460, 280), (1390, 240),
                                                        (1470, 230)], "rgba(201,193,238,.04)", LILAC, 2.5, ta, style="claimed", fx="pop"),
            lab(1500, 410, "an atomic flash?", ta + .3, LILAC, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


TW = dict(x0=520, x1=1220, gy=680, h=340)       # the 1937 wall, 3.7 m by 1.8 m at about 190 units a metre


def timber_wall(x0, x1, gy, h, at, rows=4, brick=True, step=.12, beam_c="#7a5a3a", core="#6a645c", face="#b07a5a"):
    """A timber-laced wall seen from the side, cut away: brick or stone faces, a rubble core, beams running through it; built course by
    course from the ground."""
    els = []
    rows_h = h / rows
    r = random.Random(3)
    for k in range(rows):
        y1 = gy - k * rows_h
        y0 = y1 - rows_h
        t = round(at + step * k, 2)
        els.append(rect(x0, y0, x1 - x0, rows_h, core, "rgba(255,236,206,.15)", 1, 0, t, fx="fill", dur=.3))
        for q in range(int((x1 - x0) / 34)):
            els.append(circ(round(x0 + 20 + q * 34 + r.uniform(-8, 8), 1), round(y0 + rows_h * r.uniform(.25, .75), 1), r.uniform(7, 12), "#8a8278", "#b8ae9c", 1, t, op=.9))
        if k % 2 == 1:
            els.append(rect(x0 - 16, y0 + rows_h * .4, x1 - x0 + 32, 16, beam_c, "#c9a06a", 1.5, 3, t + .05))
        if brick:
            for side in (x0, x1 - 40):
                for b in range(3):
                    els.append(rect(side, y0 + b * rows_h / 3, 40, rows_h / 3 - 2, face, "#e0a888", 1, 1, t))
    return els


def flames(x0, x1, gy, h, at, n=9, seed=2):
    r = random.Random(seed)
    out = [glow(round((x0 + x1) / 2, 1), round(gy - h * .5, 1), round((x1 - x0) * .7), at, .8, "fire")]
    for k in range(n):
        x = x0 + (x1 - x0) * (k + .5) / n + r.uniform(-14, 14)
        hh = h * r.uniform(.5, 1.0)
        out.append(poly([(x - 30, gy), (x - 18, gy - hh * .5), (x - 4, gy - hh), (x + 8, gy - hh * .6), (x + 22, gy - hh * .75), (x + 30, gy)], "#ff9a40",
                        "#ffd08a", 1.5, round(at + .06 * k, 2), curve=True, fx="rise", op=.85))
    return out


def s33():
    """A colliery yard by day (the fire was lit at 11 a.m.), a pit headframe dim behind; Childe and Thorneycroft, named as they are said,
    at the wall's scale; the 1937 wall, 3.7 m by 1.8 m: brick faces, rubble core, timber beams laced through it, built course by course;
    rubble laced with timber; on 'set it on fire', flames climb it."""
    tc, tt, tb, tr, tf = T("s33", "Gordon Childe"), T("s33", "Wallace"), T("s33", "built"), T("s33", "rubble"), T("s33", "set it on fire")
    o = TW
    els = [poly([(-60, o["gy"]), (1840, o["gy"]), (1840, 1100), (-60, 1100)], "#4a3e34", at=-1), ln([(-60, o["gy"]), (1840, o["gy"])], -1, "rgba(255,236,206,.3)", 1.5, draw=False)]
    hx, hy = 1620, o["gy"]                                           # the pit headframe, dim behind
    els += [group([ln([(hx - 80, hy), (hx - 20, hy - 360)], -1, "#3a3a44", 8, draw=False), ln([(hx + 80, hy), (hx + 20, hy - 360)], -1, "#3a3a44", 8, draw=False),
                   ln([(hx - 60, hy - 120), (hx + 60, hy - 120)], -1, "#3a3a44", 5, draw=False), ln([(hx - 40, hy - 240), (hx + 40, hy - 240)], -1, "#3a3a44", 5, draw=False),
                   circ(hx, hy - 372, 34, "none", "#4a4a54", 6, -1)], -1, op=.6)]
    els += [lab(870, 200, "Plean colliery, 1937", .3, BONE, 32)]
    # the archaeologist and the mining engineer, at the wall's scale (190 units a metre), named as they are said
    els += [figure(o["x0"] - 110, o["gy"], 1.75 * 190, tc, "#262a32"), lab(o["x0"] - 110, o["gy"] - 1.75 * 190 - 24, "Childe", tc + .2, BONE, 28),
            figure(o["x1"] + 210, o["gy"], 1.72 * 190, tt, "#262a32"), lab(o["x1"] + 210, o["gy"] - 1.72 * 190 - 24, "Thorneycroft", tt + .2, BONE, 28)]
    els += timber_wall(o["x0"], o["x1"], o["gy"], o["h"], tb)
    els += [lab(870, 300, "rubble laced with timber", tr, BONE, 28)]
    els += [ln([(o["x1"] + 40, o["gy"]), (o["x1"] + 40, o["gy"] - o["h"])], tb + .6, BONE, 2, dur=.4), lab(o["x1"] + 54, o["gy"] - o["h"] / 2 + 10, "1.8 m", tb + .8, BONE, 26, "start"),
            ln([(o["x0"], o["gy"] + 40), (o["x1"], o["gy"] + 40)], tb + .6, BONE, 2, dur=.4), lab(870, o["gy"] + 84, "3.7 m", tb + .8, BONE, 26)]
    els += flames(o["x0"] - 20, o["x1"] + 20, o["gy"], 260, tf)
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "ridges": [], "cam": CAM, "els": els}


def s34():
    """The same wall after the fire, cut open: a clock runs to 20 hours; the core has fused into dark glass with hollow casts where the
    beams were and black specks of charcoal; labels."""
    tc, tg, tt = T("s34", "twenty"), T("s34", "fused"), T("s34", "casts")
    o = TW
    els = [poly([(-60, o["gy"]), (1840, o["gy"]), (1840, 1100), (-60, 1100)], "#3a3029", at=-1)]
    els += static(timber_wall(o["x0"], o["x1"], o["gy"], o["h"], 0, beam_c="#2a201a", core="#4a443e"))
    cx, cy = 300, 330
    els += [circ(cx, cy, 90, "rgba(245,236,220,.05)", BONE, 3, .3, fx="pop"), ln([(cx, cy), (cx, cy - 64)], .3, BONE, 4, draw=False),
            ln(arc(cx, cy, 104, 104, -90, 270, 36), tc - .3, GOLD, 5, dur=1.4, curve=True), lab(cx, cy + 150, "20 hours later", tc, GOLD, 30)]
    core = [(o["x0"] + 60, o["gy"] - 40), (o["x0"] + 140, o["gy"] - 260), (o["x0"] + 320, o["gy"] - 300), (o["x1"] - 160, o["gy"] - 280), (o["x1"] - 60, o["gy"] - 120),
            (o["x1"] - 100, o["gy"] - 30)]
    els += [poly(core, "rgba(40,28,22,.92)", "#c98a4a", 2.5, tg, curve=True, fx="pop"), glow(870, o["gy"] - 170, 300, tg, .35, "fire")]
    for k in range(10):
        r = random.Random(k)
        els.append(poly(E(r.uniform(o["x0"] + 160, o["x1"] - 160), r.uniform(o["gy"] - 250, o["gy"] - 70), r.uniform(20, 40), r.uniform(8, 14), 12), "rgba(255,190,110,.25)",
                        at=round(tg + .2 + .05 * k, 2)))
    for k, y in enumerate((o["gy"] - 112, o["gy"] - 282)):
        els += [rect(o["x0"] + 100, y, o["x1"] - o["x0"] - 200, 16, "#0f0b09", "#e8b87a", 2, 3, round(tt + .2 * k, 2), fx="pop", style="inferred")]
    r = random.Random(11)
    els += [dot(round(r.uniform(o["x0"] + 140, o["x1"] - 140), 1), round(r.uniform(o["gy"] - 240, o["gy"] - 60), 1), 4, "#050403", round(tt + 1.0 + .03 * k, 2)) for k in range(24)]
    els += [lab(1410, 330, "fused into glass", tg + .4, AMBER, 30, "start"), ln([(1400, 322), (o["x1"] - 80, o["gy"] - 200)], tg + .4, AMBER, 1.6, dur=.4),
            lab(1410, 420, "casts of timber", tt + .4, "#e8b87a", 28, "start"), ln([(1400, 412), (o["x1"] - 100, o["gy"] - 104)], tt + .4, "#e8b87a", 1.6, dur=.4),
            lab(1410, 500, "charcoal", tt + 1.2, BONE, 28, "start")]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s35():
    """A longer timber-laced wall (9.4 m long, 2.45 m high) burning; then, small beside it, a hand-sized heap of glass on a scale, about 3 kg;
    1980, near Aberdeen; three small icons pop as named: a stone, a draught of air, a flame."""
    tw, tk, ts, td, tf = T("s35", "A bigger"), T("s35", "three kilograms"), T("s35", "stone"), T("s35", "draught"), T("s35", "fierce")
    gy = 600
    u = 110                                                     # units a metre: 9.4 m = 1034 units, 2.45 m = 270
    x0, x1 = 130, 130 + 9.4 * u
    els = [poly([(-60, gy), (1840, gy), (1840, 1100), (-60, 1100)], "#3a3029", at=-1)]
    els += timber_wall(x0, x1, gy, 2.45 * u, tw, rows=4, brick=False, step=.08, face="#6a645c")
    els += flames(x0, x1, gy, 200, tw + .6, n=12)
    els += [lab((x0 + x1) / 2, 240, "1980, near Aberdeen", tw + .2, BONE, 30), ln([(x0, gy + 30), (x1, gy + 30)], tw + .4, BONE, 2, dur=.6),
            lab((x0 + x1) / 2, gy + 70, "9.4 m", tw + .6, BONE, 26)]
    sx, sy = 1460, 380                                         # the yield, on a scale: about 3 kg
    els += [rect(sx - 110, sy, 220, 24, "#5a5248", "#b8aa98", 1.5, 4, tk, fx="pop"), rect(sx - 10, sy + 24, 20, 60, "#5a5248", at=tk),
            rect(sx - 80, sy + 84, 160, 16, "#5a5248", at=tk)]
    for k, (dx, dy) in enumerate(((-30, -14), (0, -22), (28, -12), (-10, -34), (18, -30))):
        els += [poly(E(sx + dx, sy + dy, 16, 10, 10), "#1e2428", "#8fb0c0", 1.2, round(tk + .1 + .05 * k, 2), fx="pop")]
    els += [lab(sx, sy + 150, "about 3 kg of glass", tk + .4, GOLD, 30)]
    # what it takes, named in turn: the right stone, the right draught, a long fierce fire
    for x, t, name in ((1300, ts, "stone"), (1460, td, "draught"), (1620, tf, "fire")):
        if name == "stone":
            els.append(poly(E(x, 690, 34, 22, 12), "#7a7066", "#b8aa98", 1.5, t, fx="pop"))
        elif name == "draught":
            els += [ln([(x - 40, 680), (x, 672), (x + 40, 682)], t, BLUE, 3, dur=.3, curve=True), ln([(x - 30, 700), (x + 10, 694), (x + 44, 702)], t + .1, BLUE, 3, dur=.3, curve=True)]
        else:
            els.append(poly([(x - 20, 712), (x - 10, 682), (x, 662), (x + 8, 684), (x + 20, 712)], "#ff9a40", "#ffd08a", 1.5, t, curve=True, fx="pop"))
        els.append(lab(x, 752, name, t + .2, MUTED, 24))
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s36():
    """Three dashed tags with small pictures pop as named: an attack? (torches at a gate), a ritual? (a ring of fire), builders? (a trowel);
    below them, logs glow in a fire: the fuel, wood."""
    ta, tr, tb, tw = T("s36", "attack"), T("s36", "ritual"), T("s36", "builders"), T("s36", "wood")
    els = []
    xs = [400, 889, 1378]
    for x, t, name in zip(xs, (ta, tr, tb), ("an attack?", "a ritual?", "builders?")):
        els += [rect(x - 200, 170, 400, 320, "rgba(240,176,106,.04)", "#f0b06a", 2.5, 14, round(.3 + .12 * xs.index(x), 2), fx="pop", style="inferred"),
                lab(x, 540, name, t + .2, "#f0b06a", 30)]
    x = xs[0]
    els += [rect(x - 60, 300, 120, 160, "#3a3029", "#8a7a66", 2, 4, ta + .2), poly([(x - 60, 300), (x, 250), (x + 60, 300)], "#3a3029", "#8a7a66", 2, ta + .2)]
    for dx in (-110, 110):
        els += [ln([(x + dx, 470), (x + dx * .9, 360)], ta + .3, "#8a6a48", 6, draw=False), glow(x + dx * .9, 350, 50, ta + .3, .8, "fire")]
    x = xs[1]
    els += [glow(x, 360, 150, tr + .2, .5, "fire")] + [poly(E(x + 110 * math.cos(math.radians(a)), 360 + 50 * math.sin(math.radians(a)), 12, 22, 10), "#ff9a40", at=round(tr + .2 + .02 * q, 2))
                                                       for q, a in enumerate(range(0, 360, 30))]
    x = xs[2]
    els += [group([poly([(x - 70, 330), (x + 50, 290), (x + 70, 330), (x - 50, 370)], "#b8b0a4", "#e8e2d6", 2), ln([(x + 60, 310), (x + 110, 280), (x + 120, 250)], -1, "#8a6a48", 10, draw=False)],
                  tb + .2, "pop")]
    lx, ly = 889, 700
    els += [glow(lx, ly, 260, tw - .2, .7, "fire")]
    for k, (dx, a) in enumerate(((-120, -8), (-40, 6), (40, -6), (120, 8))):
        els.append(group([rect(lx + dx - 70, ly - 14, 140, 28, "#6a4a30", "#c9a06a", 2, 12)], round(tw - .2 + .05 * k, 2), "pop", tr="rotate(%d %d %d)" % (a, lx + dx, ly)))
    els += flames(lx - 180, lx + 180, ly - 6, 120, tw, n=6, seed=5)
    els += [lab(lx, 772, "the fuel: wood", tw + .3, GOLD, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== chapter 5: a reactor in Gabon
OKLO = (13.16, -1.39)


def s37():
    """Left, in a window: a map from France to Gabon, a gold pin for Oklo and one for Pierrelatte, joined by a dashed line (uranium ore,
    1972). Right, on the dark: a time line of 2.5 billion years; a gold glow at about 2 billion: the reactor; the first animals near 0.6."""
    tr = T("s37", "two billion")
    # left: the map in its own window (land clipped to it); the pins and the ore's journey drawn over it with their own timing
    wx, wy, ww, wh = 90, 140, 620, 640
    m = Map(-12.0, 28.0, -8.0, 52.0, rect=(wx, wy, ww, wh))
    ox, oy = m.p(*OKLO)
    px, py = m.p(4.73, 44.35)
    els = window(wx, wy, ww, wh, [land_el(m.land(), -1, "#5a4834")], at=-1, sea="#173342")
    els += [glow(ox, oy, 60, .3, .7, "lamp"), pin(ox, oy, "Oklo, Gabon", .3, GOLD, "start", lx=22, ly=10),
            pin(px, py, "Pierrelatte", .5, BLUE, "start", lx=22, ly=10), ln([(ox, oy), (px, py)], .6, GOLD, 2.5, "inferred", dur=1.0, curve=False),
            lab(m.p(2.0, 22.0)[0], m.p(2.0, 22.0)[1], "uranium ore, 1972", .9, GOLD, 26)]
    # right: two and a half billion years, the reactor at about two billion, the first animals much later
    X = lambda ga: round(820 + (2.5 - ga) / 2.5 * 820, 1)
    els += [axis(X(2.5), X(0), 560, [(X(2.5), "2.5"), (X(2.0), "2"), (X(1.0), "1"), (X(0), "today")], .4, "billion years ago")]
    els += [glow(X(1.95), 500, 90, tr, .9, "lamp"), circ(X(1.95), 500, 12, GOLD, "#fff3c8", 2, tr), lab(X(1.95), 440, "the reactor", tr + .2, GOLD, 30),
            ln([(X(.6), 520), (X(.6), 560)], tr + .8, MUTED, 2, draw=False), lab(X(.6), 500, "first animals", tr + .9, MUTED, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def dot_grid(x0, y0, cols, rows, step, r, at, lit, c_off="#5a5048", c_on=GOLD, dt=.0015):
    out = []
    for k in range(cols * rows):
        x, y = x0 + step * (k % cols), y0 + step * (k // cols)
        on = k in lit
        out.append(circ(x, y, r * (1.6 if on else 1), c_on if on else c_off, at=round(at + (0 if on else dt * k), 2), fx="pop" if on else None))
    return out


def s38():
    """Two grids of 1,000 dots (40 by 25): anywhere on Earth, 7 light gold; Oklo, only 4; about 7 in 1,000."""
    tk, tw, ta, to = T("s38", "two main kinds"), T("s38", "Anywhere"), T("s38", "seven"), T("s38", "Oklo's")
    step, r = 15, 4.2
    lit_a = [83, 246, 391, 512, 640, 777, 903]
    lit_b = [150, 433, 701, 880]
    ax_, bx = 170, 1000
    els = []
    # two samples of a thousand uranium atoms each, on screen from the start
    els += dot_grid(ax_, 250, 40, 25, step, r, .3, [], dt=.001) + dot_grid(bx, 250, 40, 25, step, r, .5, [], dt=.001)
    # the two kinds: the common one (dim) and the rare one that splits (gold)
    els += [circ(640, 172, 6, "#5a5048", at=tk, fx="pop"), lab(656, 181, "common kind", tk + .1, MUTED, 26, "start"),
            circ(940, 172, 7.5, GOLD, at=tk + .5, fx="pop"), glow(940, 172, 24, tk + .5, .8, "lamp"), lab(956, 181, "rare kind: splits", tk + .6, GOLD, 26, "start")]
    els += [lab(ax_ + 20 * step - 10, 228, "anywhere on Earth", tw, BONE, 30)]
    els += [circ(ax_ + step * (k % 40), 250 + step * (k // 40), r * 1.8, GOLD, at=round(ta + .1 * q, 2), fx="pop") for q, k in enumerate(lit_a)]
    els += [glow(ax_ + step * (k % 40), 250 + step * (k // 40), 26, round(ta + .1 * q, 2), .8, "lamp") for q, k in enumerate(lit_a)]
    els += [lab(bx + 20 * step - 10, 228, "Oklo", to, GOLD, 32)]
    els += [circ(bx + step * (k % 40), 250 + step * (k // 40), r * 1.8, GOLD, at=round(to + .1 * q, 2), fx="pop") for q, k in enumerate(lit_b)]
    els += [glow(bx + step * (k % 40), 250 + step * (k // 40), 26, round(to + .1 * q, 2), .8, "lamp") for q, k in enumerate(lit_b)]
    els += chip(470, 690, "about 7 in 1,000", GOLD, ta + .8, 30) + chip(1300, 690, "fewer", "#e98a8a", to + .5, 30)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def tower_cooling(x, gy, h, at, c=LILAC, style="claimed"):
    w = h * .62
    pts = [(x - w / 2, gy), (x - w * .34, gy - h * .55), (x - w * .3, gy - h), (x + w * .3, gy - h), (x + w * .34, gy - h * .55), (x + w / 2, gy)]
    return poly(pts, "rgba(201,193,238,.04)", c, 2.5, at, curve=True, style=style, fx="rise")


def s39():
    """A dotted lilac power plant with cooling towers in a jungle (an ancient plant?); beside it, the real scene: a bare coast two billion
    years ago under a hazy sky, low domes of microbial mats in the shallows, not one animal."""
    tp, tn = T("s39", "nuclear plant"), T("s39", "no animals")
    gy = 600
    # left: a jungle at night, clipped to its frame; the claimed plant drawn over it in dotted lilac, as it is said
    jungle = [poly(E(160 + 80 * k, 640, 70, 120, 16), "#1c3024", at=-1, curve=True) for k in range(9)]
    els = window(110, 150, 740, 650, jungle, at=-1, sea="#13201a", edge="rgba(255,236,206,.2)")
    els += [tower_cooling(330, gy, 230, tp), tower_cooling(520, gy, 260, tp + .2), poly([(600, gy), (600, gy - 120), (780, gy - 120), (780, gy)], "rgba(201,193,238,.04)", LILAC, 2.5,
                                                                                          tp + .4, style="claimed", fx="rise")]
    els += [lab(480, 270, "an ancient plant?", tp + .6, LILAC, 30)]
    # right: the real scene two billion years ago, a bare coast under a hazy sky, low microbial mats in the shallows, clipped to its frame
    x0 = 930
    coast = [rect(x0, 150, 740, 330, "#6a6060", at=-1), glow(x0 + 520, 300, 180, -1, .5, "sun"),
             poly([(x0, 480), (x0 + 740, 470), (x0 + 740, 800), (x0, 800)], "#3f5a62", at=-1),
             poly([(x0 - 40, 560), (x0 + 330, 540), (x0 + 520, 600), (x0 + 780, 620), (x0 + 780, 840), (x0 - 40, 840)], "#5a4a3c", at=-1, curve=True)]
    coast += [poly(arc(x, 548 + k * 6, w, 34, 180, 360, 12), "#7a7a5a", "#b8b48a", 1.5, -1) for k, (x, w) in enumerate(((x0 + 120, 60), (x0 + 220, 80), (x0 + 330, 50), (x0 + 430, 70)))]
    els += window(x0, 150, 740, 650, coast, at=tn - .8, sea="#3a3436", edge="rgba(255,236,206,.2)")
    els += [lab(x0 + 370, 720, "two billion years ago", tn - .5, BONE, 28)]
    els += tag(x0 + 370, 230, "no animals yet", tn + .2, GOLD, 30)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def hourglass(x, y, h, at):
    w = h * .5
    els = [rect(x - w * .62, y - h / 2 - 16, w * 1.24, 16, "#6a4a30", "#c9a06a", 1.5, 4), rect(x - w * .62, y + h / 2, w * 1.24, 16, "#6a4a30", "#c9a06a", 1.5, 4),
           poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + 8, y - 6), (x + 8, y + 6), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - 8, y + 6), (x - 8, y - 6)],
                "rgba(190,225,240,.1)", "#cfe8f4", 2.5)]
    return group(els, at, "pop")


def s40():
    """An hourglass with gold sand at the left; a chart at the right: the share of the rare uranium falls from about 3.6% two billion years
    ago to 0.72% today; a pale band of modern reactor fuel (3 to 5%); the two-billion point sits inside it."""
    th, tf, tx, tm = T("s40", "hourglass"), T("s40", "shrinking"), T("s40", "five times"), T("s40", "modern reactor")
    hx, hy, hh = 300, 470, 380
    els = [hourglass(hx, hy, hh, th)]
    els += [poly([(hx - 70, hy - 120), (hx + 70, hy - 120), (hx + 6, hy - 10), (hx - 6, hy - 10)], AU, at=th + .2), poly([(hx - 30, hy + 190), (hx, hy + 120), (hx + 30, hy + 190)], AU, at=th + .3),
            ln([(hx, hy - 10), (hx, hy + 150)], tf, AU, 3, dur=1.0)]
    X = lambda ga: round(620 + (2.0 - ga) / 2.0 * 1000, 1)
    Y = lambda p: round(700 - p / 5.0 * 500, 1)
    els += [axis(X(2.0), X(0), 720, [(X(2.0), "2 billion"), (X(1.0), "1"), (X(0), "today")], th + .4),
            ln([(X(2.0) - 20, Y(0)), (X(2.0) - 20, Y(5))], th + .4, MUTED, 2, draw=False)]
    for p in (1, 2, 3, 4, 5):
        els.append(lab(X(2.0) - 30, Y(p) + 9, "%d%%" % p, th + .5, MUTED, 24, "end"))
    l235, l238 = math.log(2) / 0.7038, math.log(2) / 4.468
    pts = []
    for k in range(41):
        ga = 2.0 * (1 - k / 40)
        rr = 0.0072566 * math.exp(ga * (l235 - l238))
        pts.append((X(ga), Y(100 * rr / (1 + rr))))
    els += [rect(X(2.0), Y(5), X(0) - X(2.0), Y(3) - Y(5), "rgba(143,217,176,.12)", "rgba(143,217,176,.5)", 1.5, 4, tm - .4, fx="pop"),
            lab(X(0.75), Y(4.0) + 10, "modern reactor fuel, 3 to 5%", tm, GREEN, 28),
            ln(pts, tf, GOLD, 5, dur=2.0, curve=True), circ(*pts[0], 12, GOLD, "#fff3c8", 2, tx), lab(pts[0][0] + 26, pts[0][1] - 10, "about 3.6%", tx + .2, GOLD, 28, "start"),
            lab(pts[-1][0] - 10, pts[-1][1] - 22, "0.72% today", tf + 1.8, BONE, 26, "end")]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s41():
    """A cut through the ground: a dark seam of uranium ore between sandstone layers; blue groundwater seeps down into it; in a lens, a fast
    neutron slows in the water, hits an atom that splits and throws out two more; the seam glows: critical."""
    tw, ts, tc = T("s41", "groundwater"), T("s41", "Water slows"), T("s41", "critical")
    els = [rect(80, 160, 860, 160, "#8a7458", at=-1), rect(80, 320, 860, 90, "#2a2420", "#6a5a4a", 1.5, 0, -1), rect(80, 410, 860, 380, "#7a644c", at=-1),
           lab(110, 300, "sandstone", .3, BONE, 26, "start"), lab(110, 378, "uranium ore", .4, GOLD, 26, "start")]
    for k in range(6):                                          # groundwater seeps down into the seam, right of the labels
        x = 380 + 100 * k
        els.append(ln([(x, 160), (x + 10, 240), (x - 6, 320), (x + 4, 380)], round(tw + .1 * k, 2), WATER, 4, "inferred", dur=1.0, curve=True))
    els += [lab(110, 214, "groundwater", tw + .4, BLUE, 28, "start")]
    cx, cy, R_ = 1300, 450, 300
    els += [circ(cx, cy, R_, "rgba(40,90,120,.35)", BONE, 3, ts - .2, fx="pop"), ln([(940, 365), (cx - R_ * .8, cy - R_ * .5)], ts - .2, BONE, 1.6, "inferred", dur=.4)]
    els += [ln([(cx - 260, cy - 120), (cx - 170, cy - 60)], ts, "#ff7a6a", 5, dur=.3), lab(cx - 210, cy - 150, "fast", ts, "#ff9a8a", 24),
            ln([(cx - 170, cy - 60), (cx - 140, cy - 30), (cx - 120, cy - 50), (cx - 96, cy - 18), (cx - 70, cy - 36), (cx - 40, cy - 6)], ts + .4, BLUE, 3, dur=.8),
            lab(cx - 120, cy + 30, "slowed", ts + .6, BLUE, 24)]
    ax, ay = cx + 30, cy + 10
    els += [circ(ax, ay, 30, GOLD, "#fff3c8", 2, ts + 1.0, fx="pop"), glow(ax, ay, 90, ts + 1.6, .9, "fire"),
            circ(ax + 50, ay - 40, 20, AMBER, at=ts + 1.8, fx="pop"), circ(ax + 40, ay + 50, 18, AMBER, at=ts + 1.8, fx="pop")]
    for k, (dx, dy) in enumerate(((150, -110), (160, 60), (120, 150))):
        els.append(ln([(ax + 30, ay), (ax + dx, ay + dy)], round(ts + 2.0 + .1 * k, 2), "#ff7a6a", 3, dur=.3))
    els += [glow(510, 365, 300, tc, .8, "fire"), lab(510, 470, "critical", tc + .2, GOLD, 34)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s42():
    """A chart that draws itself along a time axis in hours: glowing blocks 30 minutes long (on) separated by gaps 2.5 hours long (off); a
    blue water level falls during each block and refills in each gap; puffs of steam."""
    tb, to, tf = T("s42", "boiled"), T("s42", "thirty minutes"), T("s42", "two and a half")
    u = 1300 / 9.0                                            # units an hour, over 9 hours
    x0, yb = 220, 600
    els = [axis(x0, x0 + 9 * u, yb + 40, [(x0 + h * u, "%d h" % h) for h in range(0, 10, 3)], tb - .6, "time")]
    t0 = tb
    wl = [(x0, 300)]
    for c in range(3):
        a = x0 + c * 3 * u
        t = round(t0 + 1.0 * c, 2)
        els += [rect(a, 420, .5 * u, 180, "rgba(255,160,80,.55)", "#ffcf8a", 2, 4, t, fx="fill"), glow(round(a + .25 * u, 1), 470, 60, t, .7, "fire"),
                circ(round(a + .25 * u, 1), 390, 10, "#ffffff", at=t + .2, op=.3, fx="pop")]
        wl += [(a, 300), (a + .5 * u, 380), (a + 3 * u, 300)]
    els += [ln(wl, t0 + .2, WATER, 4, dur=3.0), lab(x0 + 9 * u + 10, 300, "water", t0 + 1.2, BLUE, 26, "start")]
    # "on" beside the first glowing block; "off" across the first gap, at mid height, clear of the water line and the axis
    els += [lab(x0 + .5 * u + 14, 470, "on: 30 min", to, "#ffcf8a", 28, "start")]
    a1, a2 = x0 + .5 * u, x0 + 3 * u
    els += [ln([(a1 + 6, 560), (a2 - 6, 560)], tf, BLUE, 2.5, dur=.6), ln([(a1 + 6, 548), (a1 + 6, 572)], tf, BLUE, 2.5, draw=False),
            ln([(a2 - 6, 548), (a2 - 6, 572)], tf, BLUE, 2.5, draw=False), lab((a1 + a2) / 2, 594, "off: 2.5 h", tf + .3, BLUE, 28)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s43():
    """A short time line 1950 to 1975: a paper pops at 1956 (Kuroda's prediction), the Oklo find at 1972; a bracket between them: 16 years."""
    tk, ts = T("s43", "In nineteen"), T("s43", "Sixteen")
    X = lambda yr: round(250 + (yr - 1950) / 25 * 1280, 1)
    els = [axis(X(1950), X(1975), 600, [(X(1950), "1950"), (X(1956), "1956"), (X(1965), "1965"), (X(1972), "1972"), (X(1975), "1975")], .3)]
    els += paper(X(1956) - 110, 220, 220, 280, tk, "Kuroda, 1956", seed=8) + [lab(X(1956), 540, "a prediction", tk + .4, BONE, 28)]
    els += [glow(X(1972), 420, 110, ts - .6, .8, "lamp"), atom_icon(X(1972), 420, 40, ts - .6), lab(X(1972), 520, "Oklo, found", ts - .4, GOLD, 28)]
    els += bracket(X(1956), X(1972), 680, ts, "16 years", GOLD, up=False, size=32, ty=740)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s44():
    """An open notebook glowing over the ore seam; two tags rise as named: a constant of nature, steady to 1 in 10 million (a level line);
    waste, stayed close by (dots that barely spread from the seam); then a gold signature stroke draws itself across the seam."""
    td, tc, tw, ts = T("s44", "diary"), T("s44", "constant"), T("s44", "waste"), T("s44", "signs")
    els = [rect(80, 600, 1620, 70, "#2a2420", "#6a5a4a", 1.5, 0, -1), rect(80, 670, 1620, 140, "#7a644c", at=-1), rect(80, 520, 1620, 80, "#8a7458", at=-1)]
    els += [glow(889, 330, 300, td, .4, "lamp"), poly([(689, 420), (889, 380), (889, 220), (689, 260)], "#e9dfca", "#fff6e6", 2, td, fx="pop"),
            poly([(889, 380), (1089, 420), (1089, 260), (889, 220)], "#e9dfca", "#fff6e6", 2, td, fx="pop")]
    for k in range(5):
        els += [ln([(710, 280 + 26 * k), (870, 246 + 26 * k)], td + .2, "#9a8c78", 2.5, draw=False), ln([(908, 246 + 26 * k), (1068, 280 + 26 * k)], td + .2, "#9a8c78", 2.5, draw=False)]
    els += tag(400, 250, "a constant of nature: steady", tc, GOLD, 26) + [ln([(250, 320), (550, 320)], tc + .4, GOLD, 4, dur=.6), lab(400, 360, "to about 1 in 10 million", tc + .6, GOLD, 24)]
    r = random.Random(6)
    els += tag(1390, 250, "waste: stayed close by", tw, GREEN, 26)
    els += [dot(round(1390 + r.uniform(-60, 60), 1), round(632 + r.uniform(-24, 24), 1), 5, GREEN, round(tw + .3 + .04 * k, 2)) for k in range(16)]
    sig = [(300, 640), (380, 610), (430, 650), (480, 600), (560, 660), (640, 615), (720, 645), (820, 620), (900, 640), (1000, 612), (1100, 648), (1200, 625), (1320, 640)]
    els += [ln(sig, ts, AU, 6, dur=1.4, curve=True), glow(820, 630, 220, ts + .6, .45, "lamp")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== the weighing
LROWS = [210, 320, 430, 540, 650]


def pic_glass(x, y, at):
    return glass_lump(x, y + 18, 1.0, at, seed=50, glow_=False)


def pic_crater(x, y, at):
    return [ring_crater(x, y, 30, at)]


def pic_city(x, y, at):
    return [city_icon(x, y, .7, at)]


def pic_wall(x, y, at):
    return [wall_icon(x - 6, y + 26, .9, at)]


def pic_atom(x, y, at):
    return [atom_icon(x, y, 30, at)]


def lrow(y, at, pic, text, lit=True, size=30, h=92):
    fill, edge = ("rgba(242,201,142,.08)", "rgba(242,201,142,.3)") if lit else ("rgba(242,201,142,.03)", "rgba(242,201,142,.14)")
    out = [rect(140, y - h / 2, 1500, h, fill, edge, 1.5, 12, at, fx="pop"), lab(290, y + 11, text, at + .1, BONE if lit else DIM, size, "start")]
    out += pic(215, y, at + .1)
    return out


CHIP_R = 1616                                                    # the right edge every grade chip of the ledger ends on


def chip_r(xr, y, t, c, at, size=28):
    """A grade chip whose right end is at xr (same width rule as chip())."""
    return chip(xr - (len(t) * size * .56 + 44), y, t, c, at, size, "start")


ROWS = [("the yellow glass, a cosmic impact", pic_glass), ("Wabar, an iron meteorite", pic_crater), ("Mohenjo-daro", pic_city),
        ("melted walls, burnt timber", pic_wall), ("Oklo, a natural reactor", pic_atom)]


def s45():
    """The ledger: five rows, each with a small picture; the first two light as named and their chips pop (Strong evidence, Established);
    the last three wait."""
    els = [rect(110, 150, 1560, 570, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    t1, t2 = T("s45", "The yellow glass"), T("s45", "Wabar")
    g1, g2 = T("s45", "Strong evidence"), T("s45", "Established")
    for k, (text, pic) in enumerate(ROWS):
        els += lrow(LROWS[k], .4 + .1 * k, pic, text, lit=False)
    els += lrow(LROWS[0], t1, ROWS[0][1], ROWS[0][0]) + chip_r(CHIP_R, LROWS[0], "Strong evidence", GRADE["strong"], g1)
    els += lrow(LROWS[1], t2, ROWS[1][1], ROWS[1][0]) + chip_r(CHIP_R, LROWS[1], "Established", GRADE["established"], g2)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s46_add():
    """The camera lower on the ledger: row three (Mohenjo-daro) gets two chips, one per claim (one blast: Ruled out; bones: Awaiting
    evidence); row four Established, with a second chip for why they burned (Open question); row five Established. All inline."""
    t3, g3a, g3b = T("s46", "The skeletons"), T("s46", "Ruled out"), T("s46", "Awaiting evidence")
    t4, g4, g4b = T("s46", "Melted walls"), T("s46", "Established", k=1), T("s46", "open question")
    t5, g5 = T("s46", "Oklo"), T("s46", "Established", k=2)
    b = "bones: Awaiting evidence"
    els = lrow(LROWS[2], t3, ROWS[2][1], ROWS[2][0])
    els += chip_r(CHIP_R - (len(b) * 26 * .56 + 44) - 16, LROWS[2], "one blast: Ruled out", GRADE["ruled"], g3a, 26) + chip_r(CHIP_R, LROWS[2], b, GRADE["awaiting"], g3b, 26)
    w = "why: Open question"
    els += lrow(LROWS[3], t4, ROWS[3][1], ROWS[3][0])
    els += chip_r(CHIP_R - (len(w) * 26 * .56 + 44) - 16, LROWS[3], "Established", GRADE["established"], g4, 26) + chip_r(CHIP_R, LROWS[3], w, GRADE["open"], g4b, 26)
    els += lrow(LROWS[4], t5, ROWS[4][1], ROWS[4][0]) + chip_r(CHIP_R, LROWS[4], "Established", GRADE["established"], g5)
    return els


def s47():
    """The five pictures in a row, each joined by its real cause (a falling rock, an iron meteorite, time and a weakening monsoon, a wood
    fire, groundwater); above them the dotted mushroom and the chip Ruled out; an empty dashed box: the fingerprint."""
    tw, tv, tc, tf = T("s47", "And an ancient"), T("s47", "Ruled out"), T("s47", "Each clue"), T("s47", "fingerprint")
    els = mushroom(889, 470, 300, tw, mix(LILAC, t=.7), 2.5)
    els += chip(889, 160 + 10, "Ruled out", GRADE["ruled"], tv, 34)
    xs = [260, 575, 889, 1203, 1518]
    pics = [pic_glass, pic_crater, pic_city, pic_wall, pic_atom]
    causes = ["a cosmic impact", "a meteorite", "time and climate", "a wood fire", "groundwater"]
    for k, (x, pic, cause) in enumerate(zip(xs, pics, causes)):
        t = round(tc + .3 * k, 2)
        els += pic(x, 560, t) + [lab(x, 640, cause, t + .2, GREEN, 26)]
    els += [rect(1300, 300, 360, 120, "rgba(232,106,80,.05)", PU, 2.5, 12, tf, style="inferred", fx="pop"), lab(1480, 372, "the fingerprint?", tf + .2, PU, 28)]
    els += [lab(889, 760, "glass, stone, bone and atoms", tc + 2.6, MUTED, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s48():
    """Left: a lake-mud core in fine yearly layers with a thin red band near the top (1950s: plutonium), and an ice core with the same band.
    Right: a decay curve for plutonium halving every 24,000 years; a marker at 4,000 years: still there."""
    tb, tl, ti, tn, th, tw = T("s48", "bomb tests"), T("s48", "lake mud"), T("s48", "polar ice"), T("s48", "thin layer"), T("s48", "loses half"), T("s48", "A war")
    # "What fingerprint?": the empty dashed box of the verdict, here from the first word
    els = [rect(120, 150, 560, 80, "rgba(232,106,80,.05)", PU, 2.5, 12, .3, style="inferred", fx="pop"), lab(400, 202, "the fingerprint", .5, PU, 30)]
    # the bomb tests of the 1950s, a real event: a small solid outline (not the dotted style of a claim)
    els += [glow(1500, 230, 120, tb, .35, "fire")] + mushroom(1500, 330, 190, tb, MUTED, 2.2, "known", "rgba(203,188,168,.06)") + \
           [lab(1500, 372, "1950s bomb tests", tb + .5, MUTED, 26)]
    cx, ctop, cbot = 230, 280, 740
    els += [rect(cx - 60, ctop, 120, cbot - ctop, "#4a3a2c", "#c9ad85", 2, 30, tl - .3, fx="pop")]
    for k in range(25):
        y = ctop + 14 + k * 18
        els.append(ln([(cx - 56, y), (cx + 56, y)], tl - .2, "#7a6248" if k % 2 else "#2e2419", 3, draw=False))
    els += [lab(cx, cbot + 34, "lake mud", tl, MUTED, 26)]
    ix = 560
    els += [rect(ix - 50, ctop + 30, 100, cbot - ctop - 30, "rgba(200,230,250,.18)", "#cfe8f4", 2, 26, ti, fx="pop"), lab(ix, cbot + 34, "polar ice", ti + .1, MUTED, 26)]
    # the bomb tests' thin layer, in both, labelled between them
    els += [rect(cx - 58, ctop + 52, 116, 14, PU, at=tn, fx="pop"), glow(cx, ctop + 60, 80, tn, .6, "red"),
            rect(ix - 48, ctop + 82, 96, 12, PU, at=tn + .2, fx="pop"), glow(ix, ctop + 88, 70, tn + .2, .6, "red"),
            ln([(cx + 62, ctop + 59), (ix - 52, ctop + 88)], tn + .3, PU, 1.6, "inferred", dur=.4), lab(395, ctop + 140, "1950s:", tn + .4, PU, 26),
            lab(395, ctop + 172, "plutonium", tn + .5, PU, 26)]
    X = lambda yr: round(860 + yr / 50000 * 760, 1)
    Y = lambda f: round(700 - f * 440, 1)
    els += [axis(X(0), X(50000), 720, [(X(0), "0"), (X(24000), "24,000"), (X(48000), "48,000")], th - .4, "years"), ln([(X(0) - 10, Y(0)), (X(0) - 10, Y(1))], th - .4, MUTED, 2, draw=False)]
    pts = [(X(t), Y(0.5 ** (t / 24110))) for t in range(0, 50001, 2000)]
    els += [ln(pts, th, PU, 5, dur=1.6, curve=True), lab(X(26000), Y(.5) - 20, "half every 24,000 years", th + .6, PU, 26, "start")]
    m = (X(4000), Y(0.5 ** (4000 / 24110)))
    els += [ln([(m[0], Y(0)), m], tw, GOLD, 2.5, "inferred", dur=.4), circ(m[0], m[1], 12, GOLD, "#fff3c8", 2, tw + .3, fx="pop"),
            lab(m[0] + 24, m[1] - 24, "4,000 years: still there", tw + .5, GOLD, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s49():
    """Three dashed boxes (tests not yet passed) fill as named: plutonium (an atom and its fragments); a layer of lake mud or ice a few
    thousand years old, with a red band in it; two independent labs (two flasks)."""
    tp, tl, ty, ti = T("s49", "Plutonium"), T("s49", "a layer"), T("s49", "a few thousand"), T("s49", "two independent")
    xs = [330, 889, 1448]
    names = ("plutonium", "in lake mud or ice", "two independent labs")
    els = []
    for k, x in enumerate(xs):
        els += [rect(x - 240, 210, 480, 400, "rgba(159,208,255,.05)", BLUE, 2.5, 14, .3 + .15 * k, style="inferred", fx="pop")]
    x = xs[0]
    els += [atom_icon(x, 400, 70, tp)] + [circ(x + 120, 300, 16, AMBER, at=tp + .4, fx="pop"), circ(x - 110, 490, 14, AMBER, at=tp + .5, fx="pop")]
    x = xs[1]
    for k, c in enumerate(("#7a6248", "#5f4c39", "#cfe0ea", "#6b553f")):
        els.append(rect(x - 200, 300 + 70 * k, 400, 70, c, at=round(tl + .1 * k, 2), fx="fill", dur=.4, op=.9 if k == 2 else None))
    els += [rect(x - 200, 440, 400, 14, PU, at=tl + .6, fx="pop", op=.85)] + tag(x, 262, "a few thousand years old", ty, BONE, 24)
    x = xs[2]
    els += [group([poly([(x - 120, 520), (x - 90, 420), (x - 90, 330), (x - 70, 330), (x - 70, 420), (x - 40, 520)], "rgba(159,208,255,.12)", BLUE, 2.5),
                   poly([(x + 40, 520), (x + 70, 420), (x + 70, 330), (x + 90, 330), (x + 90, 420), (x + 120, 520)], "rgba(159,208,255,.12)", BLUE, 2.5)], ti, "pop")]
    for k, (x, nm) in enumerate(zip(xs, names)):
        els.append(lab(x, 670, nm, (tp, tl, ti)[k] + .3, BONE, 28))
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s50():
    """Night: the pectoral on a plinth, the scarab glowing softly; behind it, faint dunes under the stars."""
    els = [dune_band(600, 90, 4, "#1d1820", op=.9), dune_band(660, 60, 8, "#241e22", op=.9)]
    els += [rect(840, 700, 540, 120, "#1a1512", "#5a4a3a", 2, 6, -1), glow(1110, 460, 520, -1, .22, "lamp")]
    els += pectoral(1110, 450, .84, -1)
    return {"base": "sky", "tod": "night", "ground": 1100, "sun": False, "moon": [380, 210, 24], "ridges": [], "cam": CAM, "els": els}


# ================================================================== the film: beats (script lines + markers), aliases, the wall
def _todo(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 480, sid, .3, MUTED, 60)]}


# (chapter, beat, role, the beat's panel, [(line, the phrase that opens the sentence, shot)], extra beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "The same glass", "s2"), (1, "Something melted", "s3"), (2, "They point", "s4"), (3, "So was there", "s5")], {}),
    (0, 1, "title", "s5", [], {"intro": True}),
    (1, 0, "world", "s6", [(0, "Some were heavier", "s7"), (1, "It is almost", "s8"), (1, "And a nuclear", "s9")], {"chapter": "The yellow glass"}),
    (1, 1, "collision", "s10", [(1, "So the glass", "s11")], {}),
    (1, 2, "reversal", "s12", [(1, "But no crater", "s13")], {}),
    (1, 3, "tag", "s14", [(1, "A pharaoh wore", "s15")], {}),
    (2, 0, "world", "s16", [(1, "He found no", "s17")], {"chapter": "Black glass in Arabia"}),
    (2, 1, "collision", "s18", [(0, "The blast released", "s19"), (1, "So what does", "s20")], {}),
    (2, 2, "reversal", "s21", [(1, "And the dunes", "s22")], {}),
    (2, 3, "tag", "s23", [], {}),
    (3, 0, "world", "s24", [(1, "Online, you'll", "s25")], {"chapter": "The skeletons of Mohenjo-daro"}),
    (3, 1, "collision", "s26", [(1, "But they were", "s27")], {}),
    (3, 2, "reversal", "s28", [(1, "And the radioactivity", "s29")], {}),
    (3, 3, "tag", "s30", [], {}),
    (4, 0, "world", "s31", [(1, "To melt rock", "s32")], {"chapter": "Walls of melted stone"}),
    (4, 1, "collision", "s33", [(1, "Twenty hours", "s34")], {}),
    (4, 2, "reversal", "s35", [], {}),
    (4, 3, "tag", "s36", [], {}),
    (5, 0, "world", "s37", [(1, "Uranium comes", "s38")], {"chapter": "A reactor in Gabon"}),
    (5, 1, "collision", "s39", [(1, "The real answer", "s40")], {}),
    (5, 2, "reversal", "s41", [(1, "And it pulsed", "s42")], {}),
    (5, 3, "tag", "s43", [(1, "And physicists", "s44")], {}),
    (6, 0, "weigh", "s45", [(1, "The skeletons of", "s46")], {"chapter": "The weighing"}),
    (6, 1, "weigh", "s47", [], {}),
    (6, 2, "test", "s48", [(1, "What would change", "s49")], {}),
    (6, 3, "close", "s50", [], {}),
]

# alias shots: (the panel's shot, the camera on that panel, the additions built when the camera arrives)
ALIASES = {
    "s46": ("s45", [1.1, 889, 560], "s46_add"),
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
    ep = {"id": "lf-nuclear-war", "code": "LF.32", "series": script["series"], "title": script["title"], "case": "desert-glass",
          "verdict": "debunked", "claim": "Was there a nuclear war before history?", "mood": "mystery",
          "hook_text": "An ancient *nuclear* war?", "beats": beats, "shots": shots,
          "sources": "Cavosie & Koeberl 2019 (doi:10.1130/G45974.1) · Koeberl & Ferriere 2019 (doi:10.1111/maps.13250) · "
                     "Prescott et al. 2004 (doi:10.1029/2003JE002136) · Gnos et al. 2013 (doi:10.1111/maps.12218) · Dales 1964, Expedition 6(3) · "
                     "Childe & Thorneycroft 1938, PSAS 72 · McCloy et al. 2021 (doi:10.1038/s41598-020-80485-w) · "
                     "Gauthier-Lafaye et al. 1996 (doi:10.1016/S0016-7037(96)00245-1) · Meshik et al. 2004 (doi:10.1103/PhysRevLett.93.182302) · "
                     "McCarthy et al. 2023 (doi:10.1177/20530196221149281)",
          "post": "A scarab of yellow-green glass on a jewel made for Tutankhamun, black glass in Arabia's Empty Quarter, skeletons at Mohenjo-daro, "
                  "Scotland's melted forts and a reactor in Gabon two billion years old: the clues people cite for a nuclear war before history, "
                  "weighed one by one, and the fingerprint any such war would leave.",
          "hashtags": ["#AncientMysteries", "#Archaeology", "#Tutankhamun", "#MohenjoDaro", "#Oklo", "#Meteorite", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": script["intro_title"], "yt_title": script["yt_title"], "description": desc, "end_line": script["end_line"]}
    ep = remix(ep, alias=alias, cams=cams)
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
