"""LF.28 · Under Giza · The Orion Correlation (16:9 long film, one wall).

The script is films/long/lf-orion/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s46; the title beat is the intro card over the
panel of s4), drawn while it is said: Giza at night seen from the north, looking south, with Orion's Belt over the three pyramids;
the shaft of the King's Chamber climbing at 45 degrees toward the belt of about 2500 BCE; Bauval's desert night; the plan and the
belt (the line and the offset), heights against brightness, the Nile against the Milky Way, the texts, the journal and the book,
the 2026 statistical test; the wobble of the Earth and the belt's crossing height (today and about 10,500 BCE), the claim and the
First Time, the turn the sky needs, the Egyptian facing south, the shape that keeps and the lean that misses (Fairall's ten
degrees, more than thirty in Khufu's day); the King's Chamber shafts in section, the slow clock of a fixed slope, the targets of
about 2500 BCE, Gantenbrink's robot and Bauval and Gilbert's four stars, the date on a time line, the builder's 45-degree slope and
the closed shafts; mortar and charcoal, the candle clock and the radiocarbon dates, Merer's papyri and his crossing from Tura, the
builders' town and its seals, the plan growing over three reigns; Unas's starry burial chamber, Sah and Sopdet, the Imperishable
Stars, two skies and two shafts, two centuries, the missing link; the ledger, the tests and the close.

Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted (lilac) = claimed. Star positions
are J2000 (Hipparcos); the belt's crossing heights and leans at Giza (lat. 29.98 N) were computed with the IAU long-term precession
model (ERFA ltp, Vondrak et al. 2011): Alnitak culminates at about 58 degrees today, about 45 degrees around 2500 BCE and about 9
to 10 degrees at its lowest (around 10,700 BCE); the belt's line lies about 53 degrees from the meridian today, about 50 around
10,500 BCE and about 73 around 2500 BCE, against the pyramids' 38 (Fairall 1999: 47 to 50 against 38; Legon 1995: more than 30
in about 2500 BC). Pyramid positions and sizes from scenes.GP (published site plans); the Great Pyramid section from giza.Section.

Facts: the Short 'orion' (f05.py, rewrite/orion.json) and the script's facts_added (Bauval 1989; Bauval & Gilbert 1994 a, b;
Malek 1994; Hancock & Bauval 1996; Krupp 1997; Legon 1995; Fairall 1999; Allan 2026; Badawy 1964; Trimble 1964; Bonani et al.
2001; Tallet & Marouard 2014; Tallet 2017; AERA; Lehner & Hawass 2017; Faulkner 1969; Kessler 1977; Shaw 2000).

Engine workaround (as in lf_sphinx.py and lf_troy.py): the wall only adds elements to a panel on its first visit, at a beat start
or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per
tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on
that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-orion/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-orion/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-orion RC_FILMS_EPS=/tmp/claude-0/sbx_lf-orion/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-orion/boards python3 films.py long.lf_orion
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse
from scenes import GP, NILE, ROSETTA, DAMIETTA
from giza import Section, BASE as GB, HEIGHT as GH, SLOPE

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-orion", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, DIM, MUTED = "#f2c98e", "#cbbca8", "#bfb09c"
STAR, STARW = "#fff6e6", "#cfd8ff"
FIG = "#a99cf0"                                                  # the constellation's figure lines
NILEC, MILKY = "#6fb6d6", "rgba(214,222,255,.16)"
STONE, STONE_L, STONE_D = "#d6bd92", "#ecd8b2", "#8c7152"
NIGHTP = "#8f8ea6"                                               # pyramids by starlight
INK = "#1a1511"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#b9e08f", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}


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


def E(cx, cy, rx, ry, n=36):
    return ellipse(cx, cy, rx, ry, n)[:-1]


def ring_(x, y, r, at, c=GOLD, w=3, style="known", dur=.8):
    return {"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r, 1), "fill": "none", "c": c, "w": w, "style": style, "in": round(at, 2), "fx": "draw", "dur": dur}


def chip(x, y, t, c, at, size=28, a="middle", z=1.0):
    """A pill with a coloured rim and its words (grades, dates). z: the camera zoom it will be seen at (the pill is drawn 1/z the size,
    so that it looks right next to its words, which keep their size against the zoom)."""
    w = (len(t) * size * .56 + 44) / z
    h = size * 1.7 / z
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5 / z, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36 / z, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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


def wipe(x, y, w, h, at, fill="#15110d", op=1.0, dur=.5, r=0):
    """A veil (op < 1) or a clean sheet (op 1) laid over part of a panel: what was there fades back."""
    e = rect(x, y, w, h, fill, "none", 0, r, at, op=op)
    e["dur"] = dur
    return e


def rot(p, c, a):
    """Rotate point p about c by a degrees (screen coordinates, y down: positive a turns clockwise on screen)."""
    s, k = math.sin(math.radians(a)), math.cos(math.radians(a))
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * k - y * s, c[1] + x * s + y * k)


# ================================================================== the stars (J2000, Hipparcos), as seen facing south: east to the left, north up
STARS = {"Alnitak": (85.190, -1.943, 1.77), "Alnilam": (84.053, -1.202, 1.69), "Mintaka": (83.002, -0.299, 2.23),
         "Betelgeuse": (88.793, 7.407, .45), "Rigel": (78.634, -8.202, .13), "Bellatrix": (81.283, 6.350, 1.64), "Saiph": (86.939, -9.670, 2.06),
         "Meissa": (83.784, 9.934, 3.39), "Sword": (83.82, -5.39, 2.9), "Sirius": (101.287, -16.716, -1.46)}
BELT = ("Alnitak", "Alnilam", "Mintaka")
FIGL = [("Betelgeuse", "Alnitak"), ("Bellatrix", "Mintaka"), ("Alnitak", "Saiph"), ("Mintaka", "Rigel"), ("Alnitak", "Alnilam"), ("Alnilam", "Mintaka"),
        ("Betelgeuse", "Meissa"), ("Meissa", "Bellatrix")]


def sky(n, cx, cy, k, tilt=0.0):
    """Frame point of star n: Alnilam at (cx, cy), k units a degree, the picture turned by tilt degrees (clockwise on screen)."""
    ra, dec, _ = STARS[n]
    ra0, dec0 = STARS["Alnilam"][:2]
    p = (cx - (ra - ra0) * math.cos(math.radians(dec)) * k, cy - (dec - dec0) * k)
    return rot(p, (cx, cy), tilt) if tilt else p


def star(x, y, mag, at, k=1.0, c=STAR, halo=True, op=None, fx="pop"):
    """A star as a dot with a soft halo, sized by its brightness (magnitude)."""
    r = max(2.2, (3.2 - .9 * mag)) * k + 1.6
    out = []
    if halo:
        out.append(gl(x, y, r * 7, at, .55 if op is None else op * .55))
    out.append(circ(x, y, r, c, "none", 0, at, fx=fx, op=op))
    return out


def orion(cx, cy, k, at, tilt=0.0, op=.6, names=(), belt_glow=True, fig=True, sword=True, c=FIG, style="known", w=1.5):
    """Orion as seen facing south (or turned by tilt): figure lines, its stars by brightness, the belt brighter."""
    P = {n: sky(n, cx, cy, k, tilt) for n in STARS if n != "Sirius"}
    out = []
    if fig:
        out += [ln([P[a], P[b]], at, c, w, style, draw=False, op=op) for a, b in FIGL]
    for n, (x, y) in P.items():
        if n == "Sword" and not sword:
            continue
        mag = STARS[n][2]
        if n in BELT:
            out += star(x, y, mag, at, 1.25, halo=belt_glow)
        else:
            out += star(x, y, mag, at, .9, c=STARW if n in ("Rigel", "Bellatrix") else ("#ffd2a8" if n == "Betelgeuse" else STAR), halo=n != "Sword", op=.85 if n == "Sword" else None)
    return out, P


# ================================================================== Giza from the north, looking south (isometric, true size and place)
PYRS = ("khufu", "khafre", "menkaure")
PH = {"khufu": 146.6, "khafre": 143.5, "menkaure": 65.5}


def giza_iso(x, y, s, at=-1, az=135, el=.3, c=NIGHTP, extra=(), spin=0.0, edge="rgba(225,230,255,.5)", shadows=True):
    items = []
    if shadows:                           # starlight from the south: soft shadows fall north, toward the viewer
        for kk in PYRS:
            (e, n), b = GP[kk]
            h = b / 2
            Z = -n
            items.append({"t": "flat", "pts": [[e - h, Z - h], [e + h, Z - h], [e + h * .55, Z - h - b * .55], [e - h * .55, Z - h - b * .55]],
                          "y": 0, "c": "#0d0b10", "op": .45, "edge": "rgba(0,0,0,0)"})
    for kk in PYRS:
        (e, n), b = GP[kk]
        items.append({"t": "pyr", "x": e, "z": -n, "y": 0, "b": b, "h": PH[kk], "c": c, "id": kk, "edge": edge})
    items += list(extra)
    return {"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": items, "in": at}


def iso_xy(e, n, h, x, y, s, az=135, el=.3):
    """Where a plateau point (metres east, north of Khufu's centre; h up) lands for giza_iso(x, y, s, az, el)."""
    a = math.radians(az)
    X, Z = e, -n
    rx, rz = X * math.cos(a) - Z * math.sin(a), X * math.sin(a) + Z * math.cos(a)
    return (x + (rx - rz) * math.cos(math.pi / 6) * s, y - h * s + (rx + rz) * el * s)


# ================================================================== COLD OPEN
HX, HY, HS, HEL, HAZ = 330, 718, 1.05, .24, 150   # the hero's isometric plateau: Khufu's centre on the frame, metres to units, elevation, azimuth
HZ = 468                               # the hero's horizon
HSK = dict(cx=1010, cy=308, k=16.0)    # Orion in the hero's southern sky (Alnilam at cx, cy; k units a degree)
DARKP, RIM = "#5c5664", "rgba(226,230,255,.5)"


def night_sky(hz, seed=11, n=170, at=-1, glow_x=1060):
    """Base fields and elements for a night sky over the desert, horizon at hz."""
    base = {"base": "sky", "tod": "night", "ground": hz, "sun": False, "groundc": "#211c18",
            "ridges": [{"y": hz - 6, "a": 7, "c": "#1b1922", "seed": 3}, {"y": hz - 1, "a": 3, "c": "#17151c", "seed": 9}]}
    els = [{"k": "stars", "n": n, "x0": -60, "x1": 1840, "y0": 96, "y1": hz - 12, "seed": seed, "in": at},
           gl(glow_x, hz - 30, 700, at, .07, "lamp")]
    for k in range(9):                    # faint lines across the desert floor: depth
        yy = hz + 6 + (k ** 1.75) * 8
        els.append(ln([(-60, yy), (1860, yy)], at, "rgba(220,210,255,.05)", 1.4, draw=False))
    return base, els


def milky_way(at=-1, x0=700, y0=110, x1=500, y1=462, n=16, r=120, op=.07):
    """The winter Milky Way: a soft band of light running down the sky east (left) of Orion to the horizon."""
    out = []
    for k in range(n):
        f = k / (n - 1)
        x = x0 + (x1 - x0) * f + 30 * math.sin(f * 5.0)
        y = y0 + (y1 - y0) * f
        out.append(gl(x, y, r * (1.0 + .25 * math.sin(f * 7.0)), at, op, "blue"))
    return out


def hero_base(at=-1):
    """Night over Giza from the north, looking south: the desert floor running to a far horizon, the three pyramids at true size
    and place (Khufu nearest, lower left; Menkaure small, upper right), dark against the sky with starlit edges; Orion above."""
    base, els = night_sky(HZ)
    o, P = orion(at=at, **HSK)
    els += o
    els = els[:3] + milky_way(at) + els[3:]
    els.append(giza_iso(HX, HY, HS, at, az=HAZ, el=HEL, c=DARKP, edge=RIM))
    for kk in PYRS:
        els += pyr_courses(kk, HX, HY, HS, HAZ, HEL, at)
    return base, els, P


def pyr_courses(kk, x, y, s, az, el, at=-1, n=11, c="rgba(24,20,30,.32)"):
    """Faint courses of stone across the two faces seen from the north-north-west (north and west faces) of pyramid kk."""
    (e, nn), b = GP[kk]
    h, H = b / 2, PH[kk]
    A = (e, nn, H)
    NW, NE, SW = (e - h, nn + h, 0.0), (e + h, nn + h, 0.0), (e - h, nn - h, 0.0)
    P_ = lambda q: iso_xy(q[0], q[1], q[2], x, y, s, az, el)
    out = []
    for k in range(1, n):
        f = k / n
        for c0, c1 in ((NW, NE), (NW, SW)):
            a = tuple(c0[i] + (A[i] - c0[i]) * f for i in range(3))
            b_ = tuple(c1[i] + (A[i] - c1[i]) * f for i in range(3))
            out.append(ln([P_(a), P_(b_)], at, c, 1.1, draw=False))
    return out


def pyr_pt(kk, f=.5):
    """A point on pyramid kk in the hero: its axis at fraction f of its height."""
    e, n = GP[kk][0]
    return iso_xy(e, n, PH[kk] * f, HX, HY, HS, az=HAZ, el=HEL)


def s1():
    """The hero image, complete from the first frame: Giza at night seen from the north, looking south, the three pyramids under
    Orion. On 'two giants in a line' a dashed gold line through the two big pyramids runs on past them; on 'stepped a little aside'
    Menkaure glows and a short arrow shows its step off the line."""
    base, els, P = hero_base()
    tl, ta = T("s1", "two giants"), T("s1", "stepped a little")
    a, b, m = pyr_pt("khufu", .35), pyr_pt("khafre", .35), pyr_pt("menkaure", .35)
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d)
    u = (d[0] / L, d[1] / L)
    reach = ((m[0] - a[0]) * u[0] + (m[1] - a[1]) * u[1])           # how far along the line Menkaure lies
    foot = (a[0] + u[0] * reach, a[1] + u[1] * reach)
    els += [ln([(a[0] - .2 * d[0], a[1] - .2 * d[1]), (a[0] + u[0] * (reach + 120), a[1] + u[1] * (reach + 120))], tl, GOLD, 3, "inferred", 1.2)]
    els += [gl(m[0], m[1], 130, ta, .6), arr([foot, (m[0] + (foot[0] - m[0]) * .18, m[1] + (foot[1] - m[1]) * .18)], ta + .2, GOLD, 3, "known", .5, False)]
    base.update(cam=CAM, els=els)
    return base


def s2_add():
    """The camera tilts up: the belt's three stars brighten, a dashed line through the two bright ones runs on, Mintaka steps aside."""
    _, P = orion(at=-1, **HSK)
    t1, t2 = T("s2", "two bright stars"), T("s2", "a fainter one")
    a, b, m = P["Alnitak"], P["Alnilam"], P["Mintaka"]
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d)
    u = (d[0] / L, d[1] / L)
    reach = ((m[0] - a[0]) * u[0] + (m[1] - a[1]) * u[1])
    foot = (a[0] + u[0] * reach, a[1] + u[1] * reach)
    out = [gl(a[0], a[1], 50, t1, .8), gl(b[0], b[1], 50, t1 + .1, .8),
           ln([(a[0] - .7 * d[0], a[1] - .7 * d[1]), (a[0] + u[0] * (reach + 26), a[1] + u[1] * (reach + 26))], t1 + .2, GOLD, 2.2, "inferred", 1.0)]
    out += [gl(m[0], m[1], 60, t2, .9), arr([foot, (m[0] + (foot[0] - m[0]) * .2, m[1] + (foot[1] - m[1]) * .2)], t2 + .2, GOLD, 2.2, "known", .5, False),
            lab(m[0] + 16, m[1] - 16, "Mintaka", t2 + .4, GOLD, 26, "start")]
    return out


def s4_add():
    """The question: a lilac '?' between belt and pyramids; on 'when' a dotted arc sweeps the belt down toward the horizon."""
    tq, tw = T("s4", "copy the sky"), T("s4", "when")
    _, P = orion(at=-1, **HSK)
    b = P["Alnilam"]
    out = qmark(680, 330, tq, 96)
    out += [arr([(b[0] + 50, b[1] + 6), (b[0] + 230, b[1] + 60), (b[0] + 330, HZ - 34)], tw - .3, LILAC, 3, "claimed", .8)]
    out += qmark(b[0] + 380, HZ - 30, tw + .6, 52, halo=False)
    return out


def s3():
    """The Great Pyramid in section at night (north on the left): the King's Chamber glows, the southern shaft draws itself out at 45
    degrees to the south face and carries on as a dotted line into the sky, to the belt at that height; chip 'about 2500 BCE'."""
    S = Section(s=3.0, cx=560, gy=770)
    base, els = night_sky(770, seed=5, n=150, glow_x=1300)
    els += [dict(S.body(), **{"in": -1}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": -1}]
    els += [dict(e, **{"in": -1, "op": .5}) for e in S.els(which=("asc", "gg", "qc", "kc", "reliev"))]
    sh = kc_shafts(S)
    kx, ky = sh["kc"]
    ts, tb = T("s3", "narrow shaft"), T("s3", "four and a half")
    els += [gl(kx, ky, 70, .3, .9), lab(kx - 34, ky + 50, "King's Chamber", .5, BONE, 26, "end")]
    els += [ln(sh["south"], ts, GOLD, 3.4, dur=1.2)]
    fx_, fy_ = sh["sface"]
    D = 470
    bx, by = fx_ + D * math.cos(math.radians(45)), fy_ - D * math.sin(math.radians(45))
    els += [ln([(fx_, fy_), (bx - 30, by + 30)], ts + 1.1, GOLD, 2.2, "claimed", 1.2)]
    for n in BELT:
        x, y = sky(n, bx, by, 30.0)
        els += star(x, y, STARS[n][2], ts + 1.8, 1.5)
    els += [gl(bx, by, 120, ts + 2.0, .55), lab(bx + 70, by - 40, "Orion's Belt", ts + 2.2, GOLD, 28, "start")]
    els += chip(bx + 150, by + 70, "about 2500 BCE", AMBER, tb, 26)
    base.update(cam=CAM, els=els)
    return base


def kc_shafts(S):
    """The King's Chamber shafts in section (metres): the southern at 45 degrees from the chamber to the south face, the northern at
    about 32.5 degrees with two kinks (schematic), after Gantenbrink's survey (via Legon 1995) and Lehner & Hawass 2017."""
    R_ = S.rooms()
    kx, kh = R_["kc"]
    h0 = kh + 1.0
    s0 = (kx + 2.6, h0)
    s1_ = (kx + 2.6 + 4.0, h0)
    t = math.tan(SLOPE)
    # south face: h = (GB - x) * t ; ray from s1_ at 45 deg: h = h0 + (x - s1_x)
    xs = (GB * t - h0 + s1_[0]) / (1 + t)
    sface = (xs, h0 + xs - s1_[0])
    n0 = (kx - 2.6, h0)
    n1 = (kx - 2.6 - 3.0, h0)
    a = math.radians(32.6)
    n2 = (n1[0] - 14 * math.cos(a), n1[1] + 14 * math.sin(a))
    b = math.radians(45)
    n3 = (n2[0] - 6 * math.cos(b), n2[1] + 6 * math.sin(b))
    # north face: h = x * t ; ray from n3 going north at 32.6 deg: h = n3h + (n3x - x) tan a
    xn = (n3[1] + n3[0] * math.tan(a)) / (t + math.tan(a))
    nface = (xn, xn * t)
    return {"kc": S.P(kx, kh + 2.9), "south": [S.P(*s0), S.P(*s1_), S.P(*sface)], "north": [S.P(*n0), S.P(*n1), S.P(*n2), S.P(*n3), S.P(*nface)],
            "sface": S.P(*sface), "nface": S.P(*nface)}


# ================================================================== CHAPTER 1 · Three stars, three pyramids
def plan_xy(kk, x0, y0, k, south_up=False):
    """Frame point of pyramid kk's centre on a plan: Khufu at (x0, y0), k units a metre; north up (or south up: turned 180 degrees)."""
    e, n = GP[kk][0]
    return (x0 - e * k, y0 + n * k) if south_up else (x0 + e * k, y0 - n * k)


def plan_sq(kk, x0, y0, k, at, fill="rgba(220,191,148,.55)", edge="#f2dcb4", w=1.8, south_up=False, op=None, fx=None):
    """A pyramid seen from above: its square base and the four faces meeting at the apex (two lit, two in shade)."""
    cx, cy = plan_xy(kk, x0, y0, k, south_up)
    h = GP[kk][1] / 2 * k
    a, b, c, d = (cx - h, cy - h), (cx + h, cy - h), (cx + h, cy + h), (cx - h, cy + h)
    ap = (cx, cy)
    out = [poly([a, b, ap], fill, "none", 0, at, fx=fx, op=op), poly([b, c, ap], "rgba(120,96,70,.6)", "none", 0, at, fx=fx, op=op),
           poly([c, d, ap], "rgba(90,72,52,.7)", "none", 0, at, fx=fx, op=op), poly([d, a, ap], "rgba(236,214,176,.7)", "none", 0, at, fx=fx, op=op),
           poly([a, b, c, d], "none", edge, w, at, fx=fx, op=op)]
    return out


def north(x, y, at, up=True, c="#e9dccb"):
    """A small north arrow (pointing up, or down for a map turned south up)."""
    s = -1 if up else 1
    return [ln([(x, y - 30 * s), (x, y + 30 * s)], at, c, 2.2, draw=False), ln([(x - 9, y + 12 * s), (x, y + 30 * s), (x + 9, y + 12 * s)], at, c, 2.2, draw=False),
            lab(x, y + (62 if up else -44), "N", at, c, 24)]


def foot_of(a, b, m):
    """The foot of the perpendicular from m to the line through a and b."""
    d = (b[0] - a[0], b[1] - a[1]); L = math.hypot(*d); u = (d[0] / L, d[1] / L)
    r = (m[0] - a[0]) * u[0] + (m[1] - a[1]) * u[1]
    return (a[0] + u[0] * r, a[1] + u[1] * r), u, r


def s5():
    """Desert night outside Riyadh: dunes, a tent and a campfire, two figures; one raises an arm to Orion over the dunes; the belt
    flares; on 'the plan of the pyramids' three small gold squares (the plan of Giza) fade in beside the belt, a dotted link."""
    gy = 610
    base = {"base": "sky", "tod": "night", "ground": gy, "sun": False, "groundc": "#1d1915",
            "ridges": [{"y": gy - 30, "a": 38, "c": "#2b241f", "seed": 5}, {"y": gy - 6, "a": 16, "c": "#231d19", "seed": 8}]}
    els = [{"k": "stars", "n": 170, "x0": -60, "x1": 1840, "y0": 96, "y1": gy - 60, "seed": 21, "in": -1}]
    els += milky_way(-1, 980, 110, 900, gy - 40, 14, 110, .05)
    o, P = orion(1240, 322, 17.0, -1, op=.55)
    els += o
    # the camp
    els += [poly([(230, gy), (330, gy - 110), (440, gy)], "#3b3129", "rgba(255,190,130,.35)", 1.5, -1),
            poly([(315, gy), (332, gy - 52), (350, gy)], "#140f0c", "none", 0, -1),
            gl(540, gy - 20, 150, -1, .55, "fire"), gl(540, gy - 10, 60, -1, .9, "fire"),
            poly([(522, gy), (530, gy - 26), (538, gy - 14), (544, gy - 40), (551, gy - 16), (558, gy - 28), (564, gy)], "rgba(255,170,90,.9)", "none", 0, -1),
            poly([(531, gy), (540, gy - 18), (549, gy)], "rgba(255,228,170,.95)", "none", 0, -1),
            ln([(505, gy + 4), (575, gy - 2)], -1, "#3a2416", 6, draw=False), ln([(510, gy - 3), (572, gy + 5)], -1, "#3a2416", 6, draw=False)]
    tf, tb, tp = T("s5", "a friend who"), T("s5", "belt of Orion"), T("s5", "plan of the pyramids")
    els += [person(640, gy, 150, -1, "#241a14") | {"in": -1}, person(715, gy, 140, -1, "#2a1f17") | {"in": -1}]
    sh = (640 + 150 * .13, gy - 150 * .74)
    hand = (sh[0] + 80, sh[1] - 86)
    els += [ln([sh, hand], tf, "#241a14", 9, dur=.4), circ(hand[0], hand[1], 5, "#241a14", at=tf + .3)]
    els += [ln([(hand[0] + 10, hand[1] - 10), (P["Alnitak"][0] - 26, P["Alnitak"][1] + 16)], tb - .3, GOLD, 2, "claimed", 1.0, op=.8)]
    for n in BELT:
        els.append(gl(P[n][0], P[n][1], 60, tb, .85))
    els += [lab(P["Alnilam"][0] - 40, P["Alnilam"][1] - 44, "Orion's Belt", tb + .4, GOLD, 26, "end")]
    k = .2
    x0, y0 = 1480, 440
    for j, kk in enumerate(PYRS):
        els += plan_sq(kk, x0, y0, k, tp + .15 * j, "rgba(242,201,142,.75)", GOLD, 1.6, south_up=True)
    els += [ln([(P["Mintaka"][0] + 20, P["Mintaka"][1]), (x0 - 40, y0 - 60)], tp - .2, GOLD, 2, "claimed", .8, op=.8),
            lab(x0 + 60, y0 + 90, "the plan of Giza", tp + .5, GOLD, 26)]
    base.update(cam=CAM, els=els)
    return base


S6 = dict(x0=620, y0=205, k=.62)          # the plan of Giza in s6 and s12 (north up)
S6B = dict(cx=1250, cy=470, k=150.0)      # the belt in s6 and s12, as seen facing south


def s6():
    """Plan of Giza from above, north up, true size and place: a dashed line through Khufu's and Khafre's centres runs on to the
    south-west; Menkaure sits off it to the east (arrow). At right the belt as seen in the sky, the same construction; 'Mintaka'."""
    x0, y0, k = S6["x0"], S6["y0"], S6["k"]
    els = []
    for kk in PYRS:
        els += plan_sq(kk, x0, y0, k, -1)
    pk = {kk: plan_xy(kk, x0, y0, k) for kk in PYRS}
    els += north(800, 200, -1)
    els += [lab(pk["khufu"][0] + 92, pk["khufu"][1] + 8, "Khufu", .3, DIM, 26, "start"), lab(pk["khafre"][0] + 86, pk["khafre"][1] + 8, "Khafre", .5, DIM, 26, "start"),
            lab(pk["menkaure"][0] + 56, pk["menkaure"][1] + 8, "Menkaure", .7, DIM, 26, "start")]
    t1, t2, t3, t4 = T("s6", "Khufu's and"), T("s6", "Menkaure's"), T("s6", "In the belt"), T("s6", "Mintaka")
    a, b, m = pk["khufu"], pk["khafre"], pk["menkaure"]
    f, u, r = foot_of(a, b, m)
    els += [ln([(a[0] - u[0] * 80, a[1] - u[1] * 80), (a[0] + u[0] * (r + 70), a[1] + u[1] * (r + 70))], t1, GOLD, 3, "inferred", 1.2)]
    els += [gl(m[0], m[1], 80, t2, .5), arr([f, (m[0] - 26, m[1] - 4)], t2 + .3, GOLD, 4, "known", .5, False), lab(m[0] - 10, m[1] + 76, "a little east", t2 + .6, GOLD, 26)]
    # the belt
    P = {n: sky(n, **S6B) for n in BELT}
    els += [lab(S6B["cx"], 250, "the belt, facing south", .4, DIM, 26)]
    for n in BELT:
        els += star(P[n][0], P[n][1], STARS[n][2], -1, 2.6, op=.55)
    els += [circ(P[n][0], P[n][1], 9, STAR, at=t3 + .1 * j, fx="pop") for j, n in enumerate(BELT)]
    a2, b2, m2 = P["Alnitak"], P["Alnilam"], P["Mintaka"]
    f2, u2, r2 = foot_of(a2, b2, m2)
    els += [ln([(a2[0] - u2[0] * 70, a2[1] - u2[1] * 70), (a2[0] + u2[0] * (r2 + 70), a2[1] + u2[1] * (r2 + 70))], t3 + .3, GOLD, 3, "inferred", 1.0)]
    els += [gl(m2[0], m2[1], 70, t4, .7), arr([f2, (m2[0] + 8, m2[1] + 10)], t4 + .2, GOLD, 3, "known", .5, False), lab(m2[0] + 30, m2[1] - 22, "Mintaka", t4, GOLD, 28, "start")]
    return {"base": "plan", "north": False, "bg": "#1d1814", "cam": CAM, "els": els}


def s12_add():
    """The belt's stars, turned to fit, settle onto the three pyramids in gold; a quiet lilac '?'."""
    x0, y0, k = S6["x0"], S6["y0"], S6["k"]
    pk = {kk: complex(*plan_xy(kk, x0, y0, k)) for kk in PYRS}
    P = {n: complex(*sky(n, **S6B)) for n in BELT}
    kk_ = (pk["menkaure"] - pk["khufu"]) / (P["Mintaka"] - P["Alnitak"]); t0 = pk["khufu"] - kk_ * P["Alnitak"]
    t = .5
    out = []
    for j, n in enumerate(BELT):
        z = kk_ * P[n] + t0
        out += [gl(z.real, z.imag, 60, t + .2 * j, .9), circ(z.real, z.imag, 9, STAR, GOLD, 2, t + .2 * j, fx="pop")]
    out += [arr([(1150, 600), (1000, 700), (760, 640)], t - .3, GOLD, 2.5, "inferred", 1.0)]
    out += qmark(1000, 420, T("s12", "what it means"), 90)
    return out


def s7():
    """The three pyramids side by side in profile to one scale (2 units a metre: 146.6, 143.5 and 65.5 m); above each its star, a disc
    and halo sized by brightness (two nearly equal, Mintaka smaller); heights and 'faintest' as they are said."""
    gy, sc = 720, 2.0
    els = [rect(-60, gy, 1920, 300, "#211b16", at=-1), ln([(-60, gy), (1860, gy)], -1, "rgba(255,226,190,.35)", 1.5, draw=False)]
    spec = [("khufu", 330, "Alnitak", "146 m"), ("khafre", 860, "Alnilam", "143 m"), ("menkaure", 1390, "Mintaka", "65 m")]
    tt, ts, tm, tf = T("s7", "almost twins"), T("s7", "shine almost"), T("s7", "less than half"), T("s7", "the faintest")
    for j, (kk, x, sn, ht) in enumerate(spec):
        b, h = GP[kk][1] * sc, PH[kk] * sc
        tri = [(x - b / 2, gy), (x, gy - h), (x + b / 2, gy)]
        at = tt + .4 * j if j < 2 else tm
        els += [poly(tri, "#3a3129", "rgba(255,236,206,.25)", 1.5, -1),
                poly(tri, "url(#k-stoneC)", "rgba(255,236,206,.6)", 1.5, at, fx="fade"),
                poly([(x, gy - h), (x + b / 2, gy), (x + b * .12, gy)], "rgba(60,44,30,.35)", "none", 0, at, fx="fade"),
                lab(x, gy - h - 22, ht, at + .4, GOLD, 30)]
        # its star: flux 10^(-0.4 m); radius by the square root of the flux
        mag = STARS[sn][2]
        rr = 22 * math.sqrt(10 ** (-.4 * (mag - 1.69)))
        sy = 230
        sat = ts + .3 * j if j < 2 else tf
        els += [circ(x, sy, rr, "none", "rgba(255,246,230,.25)", 1.5, -1, style="inferred"),
                gl(x, sy, rr * 5.5, sat, .55), circ(x, sy, rr, STAR, at=sat, fx="pop"),
                ln([(x, sy + rr + 12), (x, gy - h - 60)], sat + .2, "rgba(255,246,230,.6)", 1.6, "claimed", .6)]
    els += [lab(1390 + 40, 236, "Mintaka: faintest", tf + .4, GOLD, 26, "start")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s8():
    """Split panel: left, the plateau from above (south up, as in the book: the north arrow points down) with the Nile's band to its
    east and the three pyramids just west of it; right, the night sky with the Milky Way's pale band and the belt just west of it;
    'west' arrows under both; a lilac dotted link between the two triads."""
    els = [rect(80, 140, 760, 640, "#251f19", "rgba(255,236,206,.25)", 1.5, 16, -1), rect(80, 140, 760, 640, "url(#k-speck)", at=-1, r=16, op=.6),
           rect(938, 140, 760, 640, "#0d1020", "rgba(200,210,255,.25)", 1.5, 16, -1)]
    els += [{"k": "stars", "n": 110, "x0": 950, "x1": 1690, "y0": 150, "y1": 770, "seed": 31, "in": -1}]
    # the Nile, east of the plateau: on a map with south at the top, east is on the left
    riv = [(250 + 26 * math.sin(y / 70.0), y) for y in range(172, 750, 18)]
    els += [ln(riv, -1, NILEC, 44, draw=False, curve=True, op=.75), ln(riv, -1, "#9fd6ee", 3, draw=False, curve=True, op=.6)]
    tn, tw = T("s8", "the river"), T("s8", "Milky Way")
    k = .42
    x0, y0 = 450, 600
    for j, kk in enumerate(PYRS):
        els += plan_sq(kk, x0, y0, k, -1, south_up=True)
    els += north(780, 700, -1, up=False)
    els += [lab(300, 200, "Nile", tn - .4, "#bfe6f5", 30, "start")]
    els += milky_way(-1, 1080, 230, 1040, 700, 12, 80, .10)
    P = {n: sky(n, 1360, 460, 52.0) for n in BELT}
    for n in BELT:
        els += star(P[n][0], P[n][1], STARS[n][2], -1, 1.6)
    els += [lab(1060, 190, "Milky Way", tw, "#d8def5", 30)]
    els += [arr([(470, 740), (650, 740)], tn + .2, GOLD, 3, "known", .5, False), lab(560, 728, "west", tn + .3, GOLD, 24),
            arr([(1290, 740), (1470, 740)], tw + .3, GOLD, 3, "known", .5, False), lab(1380, 728, "west", tw + .4, GOLD, 24)]
    els += [ln([(720, 420), (889, 380), (1280, 440)], tw + .8, LILAC, 2.5, "claimed", 1.0, curve=True)]
    return {"base": "dark", "cam": CAM, "els": els}


def carved_wall(x, y, w, h, at, c="#2e5a64", seed=3, cols=13, rows=12, fx="draw"):
    """A limestone wall carved with columns of signs (schematic strokes)."""
    out = [rect(x, y, w, h, "#cdb48e", "rgba(255,236,206,.5)", 1.5, 6, -1), rect(x, y, w, h, "url(#k-speck)", at=-1, r=6, op=.7)]
    cw = w / cols
    for q in range(1, cols):
        out.append(ln([(x + q * cw, y + 10), (x + q * cw, y + h - 10)], -1, "rgba(80,60,40,.35)", 1.2, draw=False))
    g = {"k": "glyphs", "x": x + 8, "y": y + 12, "w": w - 16, "h": h - 24, "rows": rows, "cols": cols, "c": c, "seed": seed, "sw": 3.2, "op": .9, "in": round(at, 2)}
    if fx:
        g.update(fx=fx, dur=2.4)
    out.append(g)
    return out


def s9():
    """A carved wall in warm lamplight, columns of signs; a small figure of the king rises out of it along a dotted gold path to the
    constellation of Orion, whose belt glows."""
    tt, tk, to = T("s9", "In texts carved"), T("s9", "the dead king"), T("s9", "to join")
    els = [gl(420, 460, 520, -1, .22, "lamp")]
    els += carved_wall(110, 170, 560, 590, tt)
    o, P = orion(1290, 360, 17.0, -1, op=.5)
    els += o
    path = [(640, 300), (820, 220), (1010, 260), (1180, 330)]
    els += [ln(path, tk + .3, GOLD, 2.5, "claimed", 1.6, curve=True), gl(700, 290, 70, tk, .8)]
    els += [gl(700, 290, 110, tk, .6), person(700, 340, 96, tk, "#f6d9a6") | {"fx": "rise"}]
    for n in BELT:
        els.append(gl(P[n][0], P[n][1], 60, to, .9))
    els += [lab(1290, 600, "Orion", to + .2, GOLD, 30)]
    return {"base": "dark", "stars": 70, "cam": CAM, "els": els}


def s10():
    """A short time line: on '1989' a journal page pops (title bar, two columns, a little diagram of three dots and three squares),
    chip 'Discussions in Egyptology'; on '1994' a closed book rises with three stars over three pyramids on its cover, chip 'The
    Orion Mystery, 1994', label 'Bauval and Gilbert'."""
    X = lambda yr: 200 + (yr - 1985) * 115
    t1, t2 = T("s10", "nineteen eighty-nine"), T("s10", "nineteen ninety-four")
    els = [ln([(X(1985), 700), (X(1997), 700)], .2, "#8c7152", 3, dur=.8)]
    els += [ln([(X(yr), 690), (X(yr), 710)], .4, "#8c7152", 2, draw=False) for yr in range(1985, 1998)]
    els += [circ(X(1989), 700, 10, AMBER, at=t1, fx="pop"), lab(X(1989), 750, "1989", t1, AMBER, 28),
            circ(X(1994), 700, 10, AMBER, at=t2, fx="pop"), lab(X(1994), 750, "1994", t2, AMBER, 28)]
    # the journal page
    px, py, pw, ph = X(1989) - 170, 210, 340, 420
    els += [rect(px + 8, py + 10, pw, ph, "rgba(0,0,0,.45)", at=t1 + .1, fx="pop"), rect(px, py, pw, ph, "url(#k-paper)", "#fff6e6", 1.5, 4, t1 + .1, fx="pop"),
            rect(px + 24, py + 22, pw - 48, 28, "#5a4a3a", at=t1 + .2, fx="pop")]
    els += [{"k": "glyphs", "x": px + 24, "y": py + 66, "w": 136, "h": 330, "rows": 16, "cols": 1, "kind": "latin", "c": "#6a5a4a", "in": round(t1 + .3, 2)},
            {"k": "glyphs", "x": px + 180, "y": py + 200, "w": 136, "h": 196, "rows": 9, "cols": 1, "kind": "latin", "c": "#6a5a4a", "in": round(t1 + .3, 2)}]
    for j, (dx, dy) in enumerate(((210, 170), (245, 135), (282, 92))):
        els += [rect(px + dx - 9, py + dy - 9, 18, 18, "none", "#5a4a3a", 1.5, 0, t1 + .5), circ(px + dx - 16 + 30, py + dy - 34 - 6 * j, 4, "#5a4a3a", at=t1 + .6)]
    els += chip(X(1989), 170, "Discussions in Egyptology", AMBER, t1 + .4, 24)
    # the book
    bx, by, bw, bh = X(1994) - 150, 230, 290, 390
    els += [poly([(bx + bw, by), (bx + bw + 34, by + 22), (bx + bw + 34, by + bh + 22), (bx + bw, by + bh)], "#e9dcc4", "#fff6e6", 1.2, t2 + .1, fx="rise"),
            poly([(bx, by + bh), (bx + bw, by + bh), (bx + bw + 34, by + bh + 22), (bx + 34, by + bh + 22)], "#d9c9ad", "#fff6e6", 1.2, t2 + .1, fx="rise"),
            rect(bx, by, bw, bh, "#1d2440", "#c9b98f", 2, 3, t2 + .1, fx="rise")]
    for j, (sx_, sy_) in enumerate(((bx + 96, by + 120), (bx + 145, by + 100), (bx + 196, by + 72))):
        els += [gl(sx_, sy_, 30, t2 + .4, .8), circ(sx_, sy_, 5, STAR, at=t2 + .4 + .1 * j, fx="pop")]
    for j, (cx_, w_) in enumerate(((bx + 90, 90), (bx + 160, 84), (bx + 222, 44))):
        els += [poly([(cx_ - w_ / 2, by + 330), (cx_, by + 330 - w_ * .64), (cx_ + w_ / 2, by + 330)], "#c9ad85", "none", 0, t2 + .5 + .1 * j, fx="pop")]
    els += chip(X(1994), 170, "The Orion Mystery, 1994", AMBER, t2 + .4, 24) + [lab(X(1994) + 225, 440, "Bauval and Gilbert", t2 + .7, BONE, 26, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s11():
    """A field of 162 bright stars; thin triangles flicker between random trios, faster and faster; a counter '695,520 trios'. Then a
    tall ranked column (best fit at the top) with its top magnified: Orion's Belt at 1,717th, '1,716 fit better' above it."""
    tt, tn, tb = T("s11", "every trio"), T("s11", "nearly seven hundred"), T("s11", "Orion's Belt fitted")
    els = [rect(100, 150, 760, 600, "#0d1020", "rgba(200,210,255,.25)", 1.5, 16, -1)]
    rnd = random.Random(162)
    pts = []
    while len(pts) < 162:
        x, y = rnd.uniform(130, 830), rnd.uniform(180, 720)
        if all(math.hypot(x - a, y - b) > 22 for a, b in pts):
            pts.append((x, y))
    for j, (x, y) in enumerate(pts):
        r = rnd.choice((2.2, 2.6, 3.2, 3.8, 4.6))
        els.append(circ(x, y, r, STAR, at=-1, op=round(.5 + .1 * r, 2)))
    at = tt
    for j in range(26):
        tri = rnd.sample(pts, 3)
        els.append(poly(tri, "none", LILAC, 1.6, at, op=.45))
        at += max(.07, .32 - .012 * j)
    els += [lab(480, 205, "695,520 trios", tn, GOLD, 40, st="serif", fx="pop")]
    # the ranked column
    cx, top, bot = 1060, 180, 750
    els += [rect(cx - 12, top, 24, bot - top, "rgba(201,193,238,.25)", "rgba(201,193,238,.6)", 1.5, 6, tb - .6, fx="fill"),
            lab(cx - 30, top + 12, "best fit", tb - .4, DIM, 24, "end"), lab(cx - 30, bot, "worst", tb - .4, DIM, 24, "end")]
    zx, zt, zb = 1420, 210, 710
    y_belt = zt + (zb - zt) * 1717 / 3500
    els += [ln([(cx + 12, top), (zx - 14, zt)], tb + .2, "rgba(242,201,142,.6)", 1.5, "inferred", .5), ln([(cx + 12, top + 3), (zx - 14, zb)], tb + .2, "rgba(242,201,142,.6)", 1.5, "inferred", .5),
            rect(zx - 14, zt, 28, zb - zt, "rgba(242,201,142,.12)", "rgba(242,201,142,.6)", 1.5, 6, tb + .4, fx="fill"),
            lab(zx + 30, zb, "the top 3,500", tb + .5, DIM, 24, "start")]
    els += [gl(zx, y_belt, 70, tb + 1.2, .8), ln([(zx - 30, y_belt), (zx + 30, y_belt)], tb + 1.2, GOLD, 5, draw=False),
            lab(zx + 40, y_belt - 14, "Orion's Belt", tb + 1.3, GOLD, 28, "start"), lab(zx + 40, y_belt + 24, "1,717th", tb + 1.4, GOLD, 28, "start")]
    els += [ln([(zx - 44, zt + 4), (zx - 56, zt + 4), (zx - 56, y_belt - 8), (zx - 44, y_belt - 8)], tb + 2.0, BONE, 2, dur=.5),
            lab(zx - 66, (zt + y_belt) / 2 + 8, "1,716 fit better", tb + 2.2, BONE, 26, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== CHAPTER 2 · A sky from 10,500 BCE?
LAT = 29.98
DEC = {"today": -1.94, "2500": -15.06, "6000": -34.26, "10500": -50.82}   # Alnitak's declination (ERFA ltp, Vondrak et al. 2011)


def star_arc(dec, n=48):
    """(azimuth, altitude) in degrees along a star's path above the horizon at Giza, east to west."""
    ph, de = math.radians(LAT), math.radians(dec)
    c = -math.tan(ph) * math.tan(de)
    H0 = math.acos(max(-1.0, min(1.0, c)))
    out = []
    for k in range(n + 1):
        H = -H0 + 2 * H0 * k / n
        sa = math.sin(ph) * math.sin(de) + math.cos(ph) * math.cos(de) * math.cos(H)
        alt = math.degrees(math.asin(max(-1.0, min(1.0, sa))))
        az = math.degrees(math.atan2(math.sin(H), math.cos(H) * math.sin(ph) - math.tan(de) * math.cos(ph))) + 180.0
        out.append((az, max(0.0, alt)))
    return out


SG = dict(x0=1260, gy=740, kx=4.4, ky=6.0)     # the southern sky gauge of s13/s14: south at x0, horizon at gy, units a degree


def sg(az, alt):
    return (SG["x0"] + (az - 180.0) * SG["kx"], SG["gy"] - alt * SG["ky"])


def s13():
    """Left: the Earth spinning on its tilted axis, the axis tracing a slow dotted circle: 'about 26,000 years'. Right: the southern
    sky over Giza as a gauge (horizon, south, altitude marks): the belt's daily path at four ages, the high one today and the low
    one around 10,500 BCE; on 'climbs and sinks' a double arrow on the meridian."""
    tw, tc, tp = T("s13", "slowly wobbles"), T("s13", "twenty-six thousand"), T("s13", "climbs and sinks")
    cx, cy, r = 400, 500, 150
    tilt = math.radians(23.4)
    top = (cx + 240 * math.sin(tilt), cy - 240 * math.cos(tilt)); bot = (cx - 240 * math.sin(tilt), cy + 240 * math.cos(tilt))
    els = [gl(cx, cy, 260, -1, .25, "blue"), circ(cx, cy, r, "#24485e", "#9fd0ff", 2, -1),
           poly(E(cx - 20, cy - 10, 120, 70, 24), "rgba(120,170,110,.35)", "none", 0, -1, curve=True),
           poly(E(cx + 60, cy + 70, 60, 40, 18), "rgba(120,170,110,.3)", "none", 0, -1, curve=True),
           ln([bot, top], -1, "#f5ecdc", 3, draw=False)]
    els += [arr([(cx - 70, cy - r - 6), (cx, cy - r - 22), (cx + 70, cy - r - 6)], .4, BLUE, 2.5, "known", .6),
            lab(cx - 150, cy + r + 50, "spins once a day", .6, BLUE, 24)]
    ex, ey, rx = cx, top[1], top[0] - cx
    els += [{"k": "line", "p": R(E(ex, ey, rx, 20, 40) + [E(ex, ey, rx, 20, 40)[0]]), "c": GOLD, "w": 3, "style": "inferred", "curve": True, "in": tw, "fx": "draw", "dur": 2.4},
            ln([(ex, ey), top], tw, GOLD, 1.5, "inferred", .4, op=.7), circ(top[0], top[1], 6, GOLD, at=tw, fx="pop")]
    els += [lab(cx, ey - 50, "about 26,000 years", tc, GOLD, 30)]
    # the southern sky gauge
    x0, gy = SG["x0"], SG["gy"]
    els += [rect(800, 150, 900, gy - 150, "#0d1020", at=-1, r=10), {"k": "stars", "n": 90, "x0": 810, "x1": 1690, "y0": 160, "y1": gy - 10, "seed": 41, "in": -1},
            rect(800, gy, 900, 60, "#211b16", at=-1), ln([(800, gy), (1700, gy)], -1, "rgba(255,226,190,.5)", 2, draw=False)]
    for k_, (pxx, w_) in enumerate(((x0 - 120, 70), (x0, 64), (x0 + 95, 34))):
        els += [poly([(pxx - w_ / 2, gy), (pxx, gy - w_ * .62), (pxx + w_ / 2, gy)], "#2c2620", "rgba(226,230,255,.35)", 1.2, -1)]
    els += [ln([(x0, gy), (x0, 170)], -1, "rgba(245,236,220,.35)", 1.5, "inferred", draw=False), lab(x0, gy + 42, "south", -1, DIM, 24),
            lab(820, gy + 42, "east", -1, DIM, 24, "start"), lab(1690, gy + 42, "west", -1, DIM, 24, "end")]
    for a in (30, 60):
        y = gy - a * SG["ky"]
        els += [ln([(x0 - 10, y), (x0 + 10, y)], -1, DIM, 2, draw=False), lab(x0 - 16, y + 8, f"{a}\u00b0", -1, DIM, 24, "end")]
    for j, key in enumerate(("10500", "6000", "2500", "today")):
        arc = [sg(az, al) for az, al in star_arc(DEC[key])]
        bright = key in ("today", "10500")
        els.append(ln(arc, round(.6 + .25 * j, 2), STAR if bright else "rgba(255,246,230,.5)", 2.6 if bright else 1.6, "known" if bright else "inferred", 1.2, curve=True, op=.85 if bright else .5))
    hi, lo = sg(180, 90 - LAT + DEC["today"]), sg(180, 90 - LAT + DEC["10500"])
    els += [arr([(x0 + 40, hi[1] + 30), (x0 + 40, lo[1] - 16)], tp, GOLD, 3, "known", .8, False), arr([(x0 + 40, lo[1] - 16), (x0 + 40, hi[1] + 30)], tp + .4, GOLD, 3, "known", .8, False)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s14_add():
    """Closer on the gauge: the belt marked 'today', high (about 58 degrees from Giza), above the halfway mark; faint belts step down
    the meridian to 'about 10,500 BCE', low over the horizon (about 9 to 10 degrees); 'the bottom of its swing'."""
    x0, gy = SG["x0"], SG["gy"]
    tt, tl, tb = T("s14", "These days"), T("s14", "Around ten thousand"), T("s14", "the bottom of")
    hi, lo = sg(180, 90 - LAT + DEC["today"]), sg(180, 90 - LAT + DEC["10500"])
    half = sg(180, 45)
    out = [ln([(x0 - 60, half[1]), (x0 + 60, half[1])], tt, BONE, 2, "inferred", .5), lab(x0 - 70, half[1] + 8, "halfway up", tt + .2, BONE, 24, "end")]
    for n in BELT:
        x, y = sky(n, hi[0], hi[1], 13.0)
        out += star(x, y, STARS[n][2], tt + .3, 1.2)
    out += [lab(hi[0] + 76, hi[1] - 6, "today", tt + .5, GOLD, 28, "start")]
    for k, key in enumerate(("2500", "6000")):
        p = sg(180, 90 - LAT + DEC[key])
        for n in BELT:
            x, y = sky(n, p[0], p[1], 13.0)
            out.append(circ(x, y, 3, "rgba(255,246,230,.55)", at=round(tl - .6 + .3 * k, 2), fx="pop"))
    for n in BELT:
        x, y = sky(n, lo[0], lo[1] - 6, 13.0)
        out += star(x, y, STARS[n][2], tl, 1.2)
    out += [gl(lo[0], lo[1], 90, tl, .55), lab(lo[0] - 70, lo[1] - 6, "about 10,500 BCE", tl + .3, GOLD, 26, "end")]
    out += bracket(lo[0] + 60, lo[0] + 300, lo[1] - 40, tb, None, BONE, up=False) + [lab(lo[0] + 180, lo[1] - 62, "the bottom of its swing", tb + .3, BONE, 24)]
    return out


def s15():
    """The claim, as drawn for it: above, the night sky with the belt low over the southern horizon beside the Milky Way; below,
    the plan of Giza (south up) with the Nile beside it; lilac dotted links join star to pyramid and river to river; chip 'about
    10,450 BCE'; italic 'the First Time'."""
    hz = 430
    els = [rect(-60, -60, 1920, hz + 60, "#0b0e1c", at=-1), {"k": "stars", "n": 140, "x0": -40, "x1": 1820, "y0": 100, "y1": hz - 10, "seed": 51, "in": -1},
           rect(-60, hz, 1920, 700, "#221c17", at=-1), rect(-60, hz, 1920, 700, "url(#k-speck)", at=-1, op=.5), ln([(-60, hz), (1860, hz)], -1, "rgba(255,226,190,.45)", 1.5, draw=False)]
    tc, tf = T("s15", "they wrote"), T("s15", "the First Time")
    # sky: the Milky Way at left, the belt to its right, low
    els += milky_way(-1, 640, 110, 560, hz - 6, 12, 110, .09)
    B = {n: sky(n, 1000, 300, 105.0) for n in BELT}
    for n in BELT:
        els += star(B[n][0], B[n][1], STARS[n][2], -1, 2.0)
    # ground: the Nile at left, the plan (south up) to its right, laid out like the stars above
    riv = [(560 + 30 * math.sin((y - hz) / 90.0), y) for y in range(hz, 801, 20)]
    els += [ln(riv, -1, "rgba(120,170,110,.35)", 90, draw=False, curve=True), ln(riv, -1, NILEC, 34, draw=False, curve=True, op=.8), ln(riv, -1, "#9fd6ee", 3, draw=False, curve=True, op=.5)]
    pk = {kk: complex(*plan_xy(kk, 0, 0, 1, south_up=True)) for kk in PYRS}
    zb = {n: complex(*B[n]) for n in BELT}
    kk_ = (zb["Mintaka"] - zb["Alnitak"]) / (pk["menkaure"] - pk["khufu"])
    for j, kk in enumerate(PYRS):
        z = ((pk[kk] - pk["khafre"]) * kk_ * 1.6) + zb["Alnilam"] + complex(0, 360)
        h = GP[kk][1] / 2 * abs(kk_) * 1.6
        els += [poly([(z.real - h, z.imag - h), (z.real + h, z.imag - h), (z.real + h, z.imag + h), (z.real - h, z.imag + h)], "rgba(220,191,148,.6)", "#f2dcb4", 1.6, -1),
                ln([(z.real - h, z.imag - h), (z.real + h, z.imag + h)], -1, "#8c7152", 1, draw=False), ln([(z.real + h, z.imag - h), (z.real - h, z.imag + h)], -1, "#8c7152", 1, draw=False)]
        n = BELT[j]
        els += [ln([(B[n][0], B[n][1] + 16), (z.real, z.imag - h - 8)], round(tc + .25 * j, 2), LILAC, 2.2, "claimed", .8)]
    els += [ln([(570, hz - 30), (566, hz + 40)], tc + .9, LILAC, 2.2, "claimed", .6), lab(430, hz + 100, "Nile", -1, "#bfe6f5", 28, "end"), lab(450, hz - 60, "Milky Way", -1, "#d8def5", 28, "end")]
    els += chip(1380, 250, "about 10,450 BCE", LILAC, tc + 1.2, 28) + [lab(1380, 330, "the First Time", tf, LILAC, 40, st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


def s16():
    """The hero view again, but with the sky of about 10,500 BCE: Orion low over the southern horizon behind the pyramids (its feet
    below the horizon), lilac dotted links from the three belt stars down to the three pyramids; chip 'about 10,500 BCE', label 'a
    memory set in stone'."""
    base, els = night_sky(HZ, seed=12)
    els += milky_way(-1, 640, 110, 760, HZ - 4, 14, 120, .07)
    cx, cy, k = 1010, HZ - 46, 17.0
    P = {n: sky(n, cx, cy, k) for n in STARS if n != "Sirius"}
    vis = {n for n, (x, y) in P.items() if y < HZ - 8}
    els += [ln([P[a], P[b]], -1, FIG, 1.5, draw=False, op=.55) for a, b in FIGL if a in vis and b in vis]
    for n in vis:
        els += star(P[n][0], P[n][1], STARS[n][2], -1, 1.25 if n in BELT else .9)
    els.append(giza_iso(HX, HY, HS, -1, az=HAZ, el=HEL, c=DARKP, edge=RIM))
    for kk in PYRS:
        els += pyr_courses(kk, HX, HY, HS, HAZ, HEL, -1)
    tl, tm = T("s16", "Bauval read"), T("s16", "a memory")
    for j, (n, kk) in enumerate(zip(BELT, PYRS)):
        q = pyr_pt(kk, 1.0)
        els += [ln([(P[n][0], P[n][1] + 10), (q[0], q[1] - 8)], round(tl + .3 * j, 2), LILAC, 2.2, "claimed", .9, op=.9)]
    els += chip(1420, 200, "about 10,500 BCE", LILAC, tl + .8, 28) + [lab(1420, 280, "a memory set in stone", tm, LILAC, 34, st="ital")]
    base.update(cam=CAM, els=els)
    return base


def s17():
    """Left: Orion as seen facing south. Right: the Giza plan, north up. In the middle, the same picture of Orion turned through about
    165 degrees ('nearly upside down', a curved amber arrow): only then do its belt stars fall on the pyramids (dotted links, gold
    stars on the squares). Then a page of the book with its north arrow pointing down ('south at the top'), and a small copy of our
    opening view: 'looking south'."""
    tt, tk, to = T("s17", "has to be turned"), T("s17", "Krupp"), T("s17", "So did our")
    oc = (365, 400)
    o, P = orion(oc[0], oc[1], 20.0, -1, op=.5)
    els = [rect(90, 150, 560, 520, "#0d1020", "rgba(200,210,255,.2)", 1.5, 14, -1), {"k": "stars", "n": 60, "x0": 100, "x1": 640, "y0": 160, "y1": 660, "seed": 61, "in": -1}]
    els += o + [lab(370, 712, "the sky, facing south", -1, DIM, 24)]
    x0, y0, k = 1390, 200, .40
    for kk in PYRS:
        els += plan_sq(kk, x0, y0, k, -1)
    els += north(1640, 230, -1) + [lab(1560, 420, "Giza, from above", -1, DIM, 24)]
    pk = {kk: complex(*plan_xy(kk, x0, y0, k)) for kk in PYRS}
    zs = {n: complex(*P[n]) for n in BELT}
    K = (pk["menkaure"] - pk["khufu"]) / (zs["Mintaka"] - zs["Alnitak"])
    ang = math.degrees(math.atan2(K.imag, K.real))                 # about 165 degrees: the turn the sky needs
    mc = (905, 380)
    o2, P2 = orion(mc[0], mc[1], 19.0, tt + .6, tilt=ang, op=.7, c=GOLD)
    els += [rect(700, 150, 410, 460, "rgba(242,201,142,.05)", "rgba(242,201,142,.35)", 1.5, 14, tt + .5, fx="pop")] + o2
    arcp = [(mc[0] + 235 * math.cos(math.radians(a_)), mc[1] - 30 + 235 * math.sin(math.radians(a_))) for a_ in range(205, 336, 10)]
    els += [arr(arcp, tt + .2, AMBER, 3.5, "known", 1.2), lab(905, 650, "nearly upside down", tt + 1.0, AMBER, 30)]
    for j, n in enumerate(BELT):
        z = pk[PYRS[j]]
        els += [ln([(P2[n][0] + 10, P2[n][1]), (z.real - 12, z.imag)], round(tt + 1.4 + .15 * j, 2), GOLD, 1.8, "claimed", .7, op=.8),
                gl(z.real, z.imag, 50, tt + 1.8, .9), circ(z.real, z.imag, 8, STAR, GOLD, 2, tt + 1.8, fx="pop")]
    # the book's map, south at the top
    bx, by = 840, 735
    els += [rect(bx - 60, by - 70, 120, 140, "url(#k-paper)", "#fff6e6", 1.5, 4, tk, fx="pop")]
    for kk in PYRS:
        q = plan_xy(kk, bx - 26, by + 30, .075, south_up=True)
        h = GP[kk][1] / 2 * .075
        els.append(rect(q[0] - h, q[1] - h, 2 * h, 2 * h, "#8c7152", at=tk + .2, fx="pop"))
    els += [ln([(bx + 38, by - 50), (bx + 38, by - 12)], tk + .4, "#5a4a3a", 2.5, draw=False), ln([(bx + 31, by - 22), (bx + 38, by - 10), (bx + 45, by - 22)], tk + .4, "#5a4a3a", 2.5, draw=False),
            lab(bx + 38, by - 56, "N", tk + .4, "#5a4a3a", 20, halo=False), lab(bx + 80, by + 10, "south at the top", tk + .6, BONE, 26, "start")]
    # a small copy of our opening view
    ix, iy, iw, ih = 1220, 470, 360, 200
    els += [rect(ix, iy, iw, ih, "#0b0e1c", "rgba(226,230,255,.4)", 1.5, 8, to, fx="pop"), rect(ix, iy + ih * .55, iw, ih * .45, "#211c18", at=to, r=0, fx="pop")]
    els.append(giza_iso(ix + 85, iy + 165, .25, to + .1, az=HAZ, el=HEL, c=DARKP, edge=RIM, shadows=False))
    oo, _ = orion(ix + 230, iy + 66, 4.5, to + .2, op=.5)
    els += oo + [arr([(ix + iw - 40, iy + ih + 52), (ix + iw - 40, iy + ih + 10)], to + .4, GOLD, 3, "known", .5, False), lab(ix + iw - 54, iy + ih + 50, "looking south", to + .6, GOLD, 26, "end")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s18():
    """A person seen from behind, standing by the Nile and facing south, upstream; the river flows toward them; on their right hand
    'west', on the left 'east'; label 'west: right'."""
    hz = 470
    base = {"base": "sky", "tod": "dusk", "ground": hz, "sun": False, "groundc": "#3d3226",
            "ridges": [{"y": hz - 18, "a": 16, "c": "#4a3c42", "seed": 4}, {"y": hz - 4, "a": 6, "c": "#3a2f30", "seed": 7}]}
    riv = [(889 - 18, hz), (889 + 18, hz), (889 + 330, 800), (889 - 330, 800)]
    els = [poly(riv, "url(#k-water)", "none", 0, -1), poly([(889 - 12, hz + 2), (889 + 12, hz + 2), (889 + 90, 800), (889 - 90, 800)], "rgba(255,226,180,.25)", "none", 0, -1)]
    els += [ln([(889 - 160 + 40 * k, 560 + 50 * k), (889 - 80 + 40 * k, 560 + 50 * k)], -1, "rgba(220,240,255,.25)", 2, draw=False) for k in range(4)]
    ts, tw = T("s18", "Egyptians faced"), T("s18", "their word")
    px, py = 620, 790
    rim = "rgba(255,226,190,.5)"
    els += [rect(px - 34, py - 120, 26, 120, "#1f1813", rim, 1.2, 4, -1), rect(px + 8, py - 120, 26, 120, "#1f1813", rim, 1.2, 4, -1),
            poly([(px - 58, py - 112), (px + 58, py - 112), (px + 46, py - 196), (px - 46, py - 196)], "#d9cfbd", rim, 1.2, -1),
            poly([(px - 46, py - 196), (px + 46, py - 196), (px + 66, py - 300), (px + 40, py - 318), (px - 40, py - 318), (px - 66, py - 300)], "#241c16", rim, 1.2, -1),
            rect(px - 12, py - 338, 24, 22, "#241c16", at=-1), circ(px, py - 362, 32, "#1a1410", rim, 1.2, -1),
            ln([(px - 62, py - 296), (px - 74, py - 200), (px - 66, py - 130)], -1, "#241c16", 18, draw=False), ln([(px + 62, py - 296), (px + 74, py - 200), (px + 66, py - 130)], -1, "#241c16", 18, draw=False)]
    els += [gl(120, hz - 30, 360, -1, .18, "lamp"), arr([(px + 30, py - 410), (880, hz + 30)], ts, GOLD, 3, "inferred", .9), lab(889, hz - 70, "south, upstream", ts + .4, GOLD, 28)]
    els += [arr([(px + 70, py - 230), (px + 330, py - 230)], tw, BONE, 3, "known", .6, False), lab(px + 340, py - 222, "west: 'right'", tw + .3, BONE, 28, "start"),
            arr([(px - 70, py - 230), (px - 300, py - 230)], tw + .5, BONE, 3, "known", .6, False), lab(px - 310, py - 222, "east: 'left'", tw + .8, BONE, 28, "end")]
    base.update(cam=CAM, els=els)
    return base


def s19():
    """Two belts, today and about 10,500 BCE, the same shape ('the same shape'); a sky gauge: the belt with a height arrow from the
    horizon and a lean arc from the meridian; then the plan on flat ground (isometric): the line of the pyramids and its lean from
    the meridian carry over; a height arrow over it stays dotted: 'no height'."""
    t1, t2, t3 = T("s19", "the shape of"), T("s19", "how high"), T("s19", "A plan on flat")
    els = [rect(90, 150, 640, 230, "#0d1020", "rgba(200,210,255,.2)", 1.5, 12, -1)]
    for j, (cx, key, c) in enumerate(((240, "today", GOLD), (580, "about 10,500 BCE", LILAC))):
        P = {n: sky(n, cx, 255, 46.0) for n in BELT}
        for n in BELT:
            els += star(P[n][0], P[n][1], STARS[n][2], t1 + .3 * j, 1.3)
        els += [poly([P[n] for n in BELT], "none", c, 1.6, t1 + .3 * j + .2, style="inferred"), lab(cx, 352, key, t1 + .3 * j + .2, c, 24)]
    els += [lab(410, 272, "=", t1 + .9, BONE, 44, st="serif"), lab(410, 412, "the same shape", t1 + 1.1, BONE, 26)]
    # the sky gauge: height and lean
    gx, hz = 330, 720
    els += [rect(90, 450, 640, 320, "#0d1020", "rgba(200,210,255,.2)", 1.5, 12, -1), ln([(100, hz), (720, hz)], -1, "rgba(255,226,190,.5)", 2, draw=False),
            ln([(gx, hz), (gx, 470)], -1, "rgba(245,236,220,.35)", 1.5, "inferred", draw=False), lab(gx - 12, 498, "south", -1, DIM, 24, "end")]
    P = {n: sky(n, gx, 560, 50.0) for n in BELT}
    for n in BELT:
        els += star(P[n][0], P[n][1], STARS[n][2], -1, 1.3)
    a, m = P["Alnitak"], P["Mintaka"]
    els += [arr([(560, hz - 4), (560, 566)], t2, GOLD, 3, "known", .6, False), lab(576, 650, "height", t2 + .2, GOLD, 26, "start")]
    la = math.degrees(math.atan2(-(m[1] - a[1]), m[0] - a[0]))
    els += [ln([(a[0] - (m[0] - a[0]) * .7, a[1] - (m[1] - a[1]) * .7), (m[0] + (m[0] - a[0]) * .6, m[1] + (m[1] - a[1]) * .6)], t2 + .6, LILAC, 2, "inferred", .5)]
    arc = [(gx + 80 * math.cos(math.radians(90 - d)), 560 - 80 * math.sin(math.radians(90 - d))) for d in range(0, int(90 - la) + 1, 4)]
    els += [ln(arc, t2 + .9, LILAC, 3, dur=.5, curve=True), lab(gx + 60, 486, "lean", t2 + 1.0, LILAC, 26, "start")]
    # the plan on flat ground
    IX, IY, IS, IAZ, IEL = 1460, 330, .52, 330, .5
    items = [{"t": "slab", "x0": -820, "x1": 300, "z0": -260, "z1": 960, "y": 0, "c": "#2e2620"}]
    for kk in PYRS:
        (e, n), bb = GP[kk]; h = bb / 2
        items.append({"t": "flat", "pts": [[e - h, -n - h], [e + h, -n - h], [e + h, -n + h], [e - h, -n + h]], "y": .5, "c": "#dcbf94"})
    items.append({"t": "line", "p": [[0, 1, -250], [0, 1, 950]], "c": "rgba(245,236,220,.55)", "w": 2, "style": "inferred", "ground": True})
    els += [{"k": "iso", "x": IX, "y": IY, "s": IS, "az": IAZ, "el": IEL, "items": items, "in": -1}]
    d = (-581.0, 738.0)
    els += [{"k": "iso", "x": IX, "y": IY, "s": IS, "az": IAZ, "el": IEL, "in": round(t3, 2),
             "items": [{"t": "line", "p": [[-.15 * d[0], 2, .15 * d[1]], [1.25 * d[0], 2, 1.25 * d[1]]], "c": GOLD, "w": 3, "style": "inferred"}]},
            {"k": "iso", "x": IX, "y": IY, "s": IS, "az": IAZ, "el": IEL, "in": round(t3 + .6, 2),
             "items": [{"t": "line", "p": [[-300 * math.sin(math.radians(q)), 2, 300 * math.cos(math.radians(q))] for q in range(0, 39, 3)], "c": LILAC, "w": 4}]}]
    lp = iso_xy(-300 * math.sin(math.radians(20)), -300 * math.cos(math.radians(20)), 0, IX, IY, IS, IAZ, IEL)
    els += [lab(lp[0] + 70, lp[1] + 96, "lean: kept", t3 + .8, LILAC, 28, "start")]
    top = iso_xy(-348, -345, 0, IX, IY, IS, IAZ, IEL)
    els += [ln([(top[0], top[1] - 10), (top[0], top[1] - 250)], t3 + 1.2, GOLD, 3, "claimed", .6),
            ln([(top[0] - 22, top[1] - 150), (top[0] + 22, top[1] - 110)], t3 + 1.7, LILAC, 4, dur=.3), ln([(top[0] - 22, top[1] - 110), (top[0] + 22, top[1] - 150)], t3 + 1.8, LILAC, 4, dur=.3),
            lab(top[0] + 36, top[1] - 200, "no height", t3 + 1.9, LILAC, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


S20 = dict(x0=1150, y0=185, k=.6)


def s20():
    """The plan (north up) with the north-south line through Khufu: the pyramids' line at about 38 degrees from it (gold); the belt's
    line around 10,500 BCE at about 48 to 50 degrees, the gap filled, 'about 10 degrees' (Fairall 1999); then the belt around 2500
    BCE at about 73 degrees, 'more than 30 degrees' (Legon 1995)."""
    x0, y0, k = S20["x0"], S20["y0"], S20["k"]
    els = []
    for kk in PYRS:
        els += plan_sq(kk, x0, y0, k, -1)
    els += north(1650, 190, -1)
    tf, tl, tk = T("s20", "worked out"), T("s20", "the belt leaned"), T("s20", "In Khufu's own")
    a = plan_xy("khufu", x0, y0, k)
    L = 600
    D = lambda deg: (a[0] - L * math.sin(math.radians(deg)), a[1] + L * math.cos(math.radians(deg)))
    els += [ln([a, (a[0], a[1] + L)], -1, "rgba(245,236,220,.5)", 2, "inferred", draw=False), lab(a[0] + 16, a[1] + L - 10, "north to south", -1, DIM, 24, "start")]
    m = plan_xy("menkaure", x0, y0, k)
    pa = math.degrees(math.atan2(a[0] - m[0], m[1] - a[1]))     # about 38 degrees
    els += [ln([a, D(pa)], -1, GOLD, 3.5, draw=False), lab(D(pa)[0] + 20, D(pa)[1] + 30, "the pyramids", -1, GOLD, 26, "start")]
    b10 = pa + 10.3
    wedge = [a] + [D(pa + (b10 - pa) * f / 10) for f in range(11)]
    els += [ln([a, D(b10)], tl, LILAC, 3.5, dur=.8), poly(wedge, "rgba(201,193,238,.25)", "none", 0, tl + .6, fx="fade"),
            lab(D(b10)[0] - 16, D(b10)[1] + 6, "the belt, about 10,500 BCE", tl + .3, LILAC, 26, "end")]
    mid = D(pa + 5.1)
    els += [lab(mid[0] - 150, mid[1] + 110, "about 10\u00b0", tl + .9, LILAC, 34, "end"), ln([(mid[0] - 145, mid[1] + 92), (mid[0] - 14, mid[1] + 8)], tl + .9, LILAC, 1.5, dur=.4)]
    els += chip(mid[0] - 290, mid[1] + 46, "Fairall, 1999", LILAC, tf, 24)
    b30 = pa + 35.2
    arcp = [(a[0] - 200 * math.sin(math.radians(d)), a[1] + 200 * math.cos(math.radians(d))) for d in [pa + (b30 - pa) * f / 12 for f in range(13)]]
    els += [ln([a, D(b30)], tk, LILAC, 3, "inferred", .8), ln(arcp, tk + .5, BONE, 2.5, dur=.6, curve=True),
            lab(D(b30)[0] - 12, D(b30)[1] - 14, "the belt, about 2500 BCE", tk + .3, LILAC, 26, "end"), lab(a[0] - 250, a[1] + 66, "more than 30\u00b0", tk + .8, BONE, 30, "end")]
    return {"base": "plan", "north": False, "bg": "#1d1814", "cam": CAM, "els": els}


def s21():
    """The landing: at left the plan with the turned belt on it and a green tick, 'shape'; at right a lilac dotted chip 'about
    10,500 BCE' with a '?', 'date'."""
    ts, td = T("s21", "The shape"), T("s21", "The date")
    els = []
    x0, y0, k = 520, 300, .42
    for kk in PYRS:
        els += plan_sq(kk, x0, y0, k, -1)
        z = plan_xy(kk, x0, y0, k)
        els += [gl(z[0], z[1], 40, ts - .2, .8), circ(z[0], z[1], 7, STAR, GOLD, 2, ts - .2, fx="pop")]
    els += [tick(560, 690, ts + .3, GREEN, 2.0, 9), lab(640, 700, "shape", ts + .4, GREEN, 34, "start")]
    els += [rect(1050, 330, 480, 120, "rgba(201,193,238,.06)", LILAC, 2.5, 60, td, fx="pop", style="claimed"), lab(1290, 405, "about 10,500 BCE", td + .1, LILAC, 34, fx="pop")]
    els += qmark(1290, 600, td + .4, 90) + [lab(1290, 700, "date", td + .5, LILAC, 34)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · Shafts aimed at the stars
S22 = Section(s=3.4, cx=889, gy=760)


def qc_shafts(S):
    """The Queen's Chamber shafts in section (metres): the southern straight at about 39.6 degrees, the northern with a bend; each
    stops at a little stone door short of the faces (schematic, after Lehner & Hawass 2017 and the Under Giza film)."""
    R_ = S.rooms(); qx, qh = R_["qc"]
    a = math.radians(39.6)
    s0, s1_ = (qx + 2.6, qh + .9), (qx + 4.4, qh + .9)
    s2 = (s1_[0] + 60 * math.cos(a), s1_[1] + 60 * math.sin(a))
    n0, n1 = (qx - 2.6, qh + .9), (qx - 4.4, qh + .9)
    n2 = (n1[0] - 22 * math.cos(a), n1[1] + 22 * math.sin(a))
    b = math.radians(46)
    n3 = (n2[0] - 9 * math.cos(b), n2[1] + 9 * math.sin(b))
    n4 = (n3[0] - 27 * math.cos(a), n3[1] + 27 * math.sin(a))
    return {"south": [S.P(*s0), S.P(*s1_), S.P(*s2)], "north": [S.P(*n0), S.P(*n1), S.P(*n2), S.P(*n3), S.P(*n4)], "sdoor": S.P(*s2), "ndoor": S.P(*n4),
            "qc": S.P(qx, qh + 2.6)}


def section_base(S, at=-1, op=.45, which=("asc", "gg", "qc", "kc", "reliev")):
    return [dict(S.body(), **{"in": at}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": at}] + \
           [dict(e, **{"in": at, "op": op}) for e in S.els(which=which)]


def s22():
    """The Great Pyramid in section at night (to scale, north on the left): the King's Chamber glows; its two shafts draw themselves
    out to the faces, the northern at about 32.5 degrees with its kinks, the southern at 45; 'north', 'south'; on 'air shafts' faint
    dotted breeze arrows; on '1964' a chip 'Badawy and Trimble, 1964' and a lilac '?' at each shaft's mouth."""
    S = S22
    base, els = night_sky(760, seed=71, n=150, glow_x=889)
    els += section_base(S)
    sh = kc_shafts(S)
    kx, ky = sh["kc"]
    tc, ta, t64, tq = T("s22", "They climb"), T("s22", "air shafts"), T("s22", "nineteen sixty-four"), T("s22", "what did they point")
    els += [gl(kx, ky, 80, -1, .9), lab(kx + 4, ky + 66, "King's Chamber", -1, BONE, 24)]
    els += [ln(sh["south"], tc, GOLD, 3.4, dur=1.2), ln(sh["north"], tc + .3, GOLD, 3.4, dur=1.4)]
    sf, nf = sh["sface"], sh["nface"]
    els += [lab(sf[0] + 26, sf[1] + 8, "south", tc + 1.2, GOLD, 26, "start"), lab(nf[0] - 26, nf[1] + 8, "north", tc + 1.4, GOLD, 26, "end")]
    for j, (p0, p1) in enumerate(((sh["south"][1], sf), (sh["north"][2], nf))):
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        els += [arr([(mx - 30 * (1 if j == 0 else -1), my + 30), (mx + 18 * (1 if j == 0 else -1), my - 16)], ta + .2 * j, BLUE, 2, "inferred", .5, False)]
    els += [lab(450, 640, "air shafts?", ta + .3, BLUE, 28, "end")]
    els += chip(889, 178, "Badawy and Trimble, 1964", AMBER, t64, 26)
    els += qmark(sf[0] + 70, sf[1] - 60, tq, 56, halo=False) + qmark(nf[0] - 70, nf[1] - 60, tq + .2, 56, halo=False)
    base.update(cam=CAM, els=els)
    return base


def s24_add():
    """The southern shaft extended as a gold dotted line to the belt at 45 degrees, 'about 2500 BCE'; the northern to the pole, a small
    dotted circle round it with Thuban on it."""
    sh = kc_shafts(S22)
    sf, nf = sh["sface"], sh["nface"]
    t45, t25, tn = T("s24", "forty-five"), T("s24", "Around"), T("s24", "The northern")
    D = 300
    bx, by = sf[0] + D * math.cos(math.radians(45)), sf[1] - D * math.sin(math.radians(45))
    out = [ln([sf, (bx - 22, by + 22)], t45, GOLD, 2.4, "claimed", .9), lab(sf[0] + 60, sf[1] + 54, "45\u00b0", t45 + .3, GOLD, 30, "start")]
    for n in BELT:
        x, y = sky(n, bx, by, 26.0)
        out += star(x, y, STARS[n][2], t25, 1.4)
    out += [gl(bx, by, 90, t25, .5), lab(bx + 40, by - 44, "Orion's Belt", t25 + .3, GOLD, 28, "start")] + chip(bx + 120, by + 56, "about 2500 BCE", AMBER, t25 + .6, 26)
    a = math.radians(32.6)
    px, py = nf[0] - D * math.cos(a), nf[1] - D * math.sin(a)
    out += [ln([nf, (px + 24, py + 16)], tn, GOLD, 2.4, "claimed", .9), ring_(px, py - 26, 30, tn + .6, BONE, 2, "inferred", .8),
            ln([(px - 8, py - 26), (px + 8, py - 26)], tn + .6, BONE, 2, draw=False), ln([(px, py - 34), (px, py - 18)], tn + .6, BONE, 2, draw=False)]
    out += star(px, py - 56, 3.7, tn + .9, 1.6) + [lab(px - 40, py - 70, "Thuban", tn + 1.1, GOLD, 28, "end"), lab(px + 46, py - 18, "the pole", tn + 1.1, DIM, 24, "start")]
    return out


def s28_add():
    """Both King's Chamber shafts glow toward their stars of about 2500 BCE: 'the builders' own sky'."""
    sh = kc_shafts(S22)
    t = T("s28", "the sky of")
    out = [ln(sh["south"], t - .4, "#ffe2a8", 6, draw=False, op=.8), ln(sh["north"], t - .4, "#ffe2a8", 6, draw=False, op=.8),
           gl(sh["sface"][0], sh["sface"][1], 70, t - .2, .7), gl(sh["nface"][0], sh["nface"][1], 70, t - .2, .7)]
    out += [lab(889, 244, "the builders' own sky", t + .2, GOLD, 32, st="ital")]
    return out


def s23():
    """The southern sky as a gauge, seen from the side: a fixed shaft at 45 degrees from a block of stone; one star's crossing point
    steps up the sky millennium by millennium (dates under the dots); where it meets the shaft, about 2500 BCE, a glow; a small clock
    face with a very slow hand."""
    ox, oy, Rr = 250, 720, 600
    tn, tc, tw, tl = T("s23", "Each night"), T("s23", "creeps up"), T("s23", "clock"), T("s23", "a few centuries")
    els = [rect(-60, oy, 1920, 300, "#211b16", at=-1), ln([(-60, oy), (1860, oy)], -1, "rgba(255,226,190,.4)", 1.5, draw=False),
           {"k": "stars", "n": 110, "x0": -40, "x1": 1820, "y0": 110, "y1": oy - 20, "seed": 81, "in": -1}]
    bw = 200
    els += [poly([(ox - bw, oy), (ox - bw, oy - 130), (ox + 20, oy - 130), (ox + 20, oy)], "url(#k-blocks)", "#f2dcb4", 1.5, -1)]
    sx, sy = ox + 20, oy - 70
    els += [poly([(ox - 110, oy - 4 - 160 + 160), (ox - 96, oy - 18), (sx, sy - 14), (sx, sy + 8)], "#0d0b09", "none", 0, -1)]
    arc = [(ox + Rr * math.cos(math.radians(a)), oy - Rr * math.sin(math.radians(a))) for a in range(5, 86, 2)]
    els += [ln(arc, -1, "rgba(245,236,220,.25)", 1.5, "inferred", draw=False), lab(ox + Rr + 16, oy - 10, "south", -1, DIM, 24, "start")]
    ray = [(sx, sy), (ox + (Rr + 90) * math.cos(math.radians(45)), oy - (Rr + 90) * math.sin(math.radians(45)))]
    els += [ln(ray, tn, GOLD, 3, "inferred", .9), lab(ray[1][0] + 14, ray[1][1] + 4, "the shaft's line", tn + .4, GOLD, 26, "start")]
    dates = [(37.1, "4000 BCE", (24, 34), "start"), (42.4, None, None, None), (45.0, "2500 BCE", (30, 40), "start"), (47.3, None, None, None), (51.5, "1000 BCE", (-24, -14), "end")]
    for j, (alt, t, off, anc) in enumerate(dates):
        x, y = ox + Rr * math.cos(math.radians(alt)), oy - Rr * math.sin(math.radians(alt))
        at = round(tc + .45 * j, 2)
        hit = abs(alt - 45.0) < .1
        els += [circ(x, y, 10 if hit else 6, STAR if hit else "rgba(255,246,230,.7)", at=at, fx="pop")]
        if t:
            els += [lab(x + off[0], y + off[1], t, at + .1, GOLD if hit else DIM, 26 if hit else 24, anc)]
    hx, hy = ox + Rr * math.cos(math.radians(45)), oy - Rr * math.sin(math.radians(45))
    els += [gl(hx, hy, 80, tl, .9), ring_(hx, hy, 24, tl, GOLD, 3)]
    els += [lab(ox + Rr * .5, oy - 30, "one star, century by century", tc + .2, DIM, 24)]
    # the slow clock
    cx, cy, r = 1380, 380, 120
    els += [circ(cx, cy, r, "rgba(18,13,10,.8)", BONE, 2.5, tw, fx="pop")]
    for k in range(12):
        a = math.radians(k * 30)
        els.append(ln([(cx + (r - 18) * math.sin(a), cy - (r - 18) * math.cos(a)), (cx + (r - 6) * math.sin(a), cy - (r - 6) * math.cos(a))], tw + .1, BONE, 3, draw=False))
    els += [ln([(cx, cy), (cx + 70 * math.sin(math.radians(28)), cy - 70 * math.cos(math.radians(28)))], tw + .3, "rgba(242,201,142,.35)", 6, draw=False),
            ln([(cx, cy), (cx + 70 * math.sin(math.radians(36)), cy - 70 * math.cos(math.radians(36)))], tw + 1.3, GOLD, 6, draw=False), circ(cx, cy, 8, GOLD, at=tw + .3),
            lab(cx, cy + r + 46, "a very slow hand", tw + .6, BONE, 26)]
    els += [lab(hx - 40, hy + 76, "a few centuries", tl + .3, GOLD, 30, "end")]
    return {"base": "sky", "tod": "night", "ground": 700, "sun": False, "groundc": "#211b16", "ridges": [{"y": 694, "a": 5, "c": "#1b1922", "seed": 3}], "cam": CAM, "els": els}


def s25():
    """A small tracked robot climbs a square stone shaft, its lamp on, its cable behind it ('early 1990s'); then the pyramid in section
    with all four shafts, each ending at its star as it is named: 'Orion's Belt' and 'Sirius' in the south, two near the pole in the
    north; chip 'about 2450 BCE'."""
    tg, ts, tn, td = T("s25", "Gantenbrink's robots"), T("s25", "Two stars in the south"), T("s25", "Two near the pole"), T("s25", "All around")
    # the shaft, seen up its length
    cx, cy = 420, 440
    els = [rect(90, 150, 660, 600, "#15110d", "rgba(255,236,206,.25)", 1.5, 14, -1)]
    for k in range(7):
        f = .86 ** k
        w = 520 * f
        els.append(rect(cx - w / 2, cy - w / 2 + 40 * (1 - f), w, w, "none", "rgba(214,190,150,%.2f)" % (.55 * f + .1), 2, 2, -1))
    els += [poly([(cx - 260, cy + 260 + 0), (cx + 260, cy + 260), (cx + 60, cy + 40), (cx - 60, cy + 40)], "#3a3129", "none", 0, -1),
            gl(cx, cy + 60, 160, tg, .45), {"k": "robot", "x": cx, "y": cy + 210, "s": 2.8, "in": round(tg, 2), "fx": "rise"},
            ln([(cx - 30, cy + 220), (cx - 120, cy + 300)], tg + .3, "#e9dccb", 3, dur=.5)]
    els += chip(cx, 190, "early 1990s", AMBER, tg + .2, 26)
    # the section with four shafts
    S = Section(s=2.6, cx=1260, gy=740)
    els += section_base(S, op=.4)
    k, q = kc_shafts(S), qc_shafts(S)
    els += [ln(k["south"], tg + .6, GOLD, 2.6, dur=.8), ln(k["north"], tg + .7, GOLD, 2.6, dur=.8), ln(q["south"], tg + .8, GOLD, 2.6, dur=.8), ln(q["north"], tg + .9, GOLD, 2.6, dur=.8)]
    def ext(p0, ang, d, side):
        return (p0[0] + side * d * math.cos(math.radians(ang)), p0[1] - d * math.sin(math.radians(ang)))
    ks, qs = ext(k["sface"], 45, 300, 1), ext(q["sdoor"], 39.6, 250, 1)
    kn, qn = ext(k["nface"], 32.6, 190, -1), ext(q["ndoor"], 39.1, 330, -1)
    els += [ln([k["sface"], ks], ts, GOLD, 2, "claimed", .6), ln([q["sdoor"], qs], ts + .5, GOLD, 2, "claimed", .6)]
    els += star(ks[0], ks[1], 1.7, ts + .2, 1.4) + [lab(ks[0] - 20, ks[1] - 16, "Orion's Belt", ts + .3, GOLD, 26, "end")]
    els += star(qs[0], qs[1], -1.4, ts + .7, 1.2) + [lab(qs[0] + 22, qs[1] + 34, "Sirius", ts + .8, GOLD, 26, "start")]
    els += [ln([k["nface"], kn], tn, GOLD, 2, "claimed", .6), ln([q["ndoor"], qn], tn + .3, GOLD, 2, "claimed", .6)]
    els += star(kn[0], kn[1], 3.7, tn + .2, 1.4) + star(qn[0], qn[1], 2.1, tn + .5, 1.4)
    els += [lab((kn[0] + qn[0]) / 2 - 30, min(kn[1], qn[1]) - 40, "near the pole", tn + .6, GOLD, 26, "end")]
    els += chip(1260, 200, "about 2450 BCE", AMBER, td, 30)
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s26():
    """A time line from 11,000 BCE to 2000 BCE: a lilac dot far left 'about 10,500 BCE'; at the right end the shafts' date 'about
    2450 BCE' (gold) beside an amber band 'the pyramid builders' (about 2600 to 2500 BCE); a gold tick."""
    X = lambda yr: round(150 + (11000 - yr) / 9000 * 1480, 1)
    tn, tp = T("s26", "Notice the"), T("s26", "own sums")
    ticks = [(X(y), "%s BCE" % format(y, ",") if y in (11000, 2000) else format(y, ",")) for y in (11000, 10000, 8000, 6000, 4000, 2000)]
    els = [axis(150, 1630, 560, ticks, -1)]
    els += [circ(X(10500), 560, 12, "none", LILAC, 3, -1, style="claimed"), circ(X(10500), 560, 5, LILAC, at=-1),
            lab(X(10500) + 10, 500, "about 10,500 BCE", -1, LILAC, 26, "start")]
    els += [{"k": "band", "x0": X(2600), "x1": X(2500), "y": 466, "h": 24, "c": AMBER, "in": round(tn, 2)}, lab(X(2550) - 20, 484, "the pyramid builders", tn + .2, AMBER, 26, "end")]
    els += [gl(X(2450), 560, 60, tp, .8), circ(X(2450), 560, 9, GOLD, at=tp, fx="pop"), lab(X(2450) - 26, 532, "the shafts' stars, about 2450 BCE", tp + .2, GOLD, 26, "end"),
            tick(X(2450) + 50, 390, tp + .8, GREEN, 1.4, 7)]
    els += [arr([(X(10500) + 20, 640), (X(6500), 730), (X(2450) - 30, 664)], tp + .5, "rgba(245,236,220,.5)", 2, "inferred", 1.2),
            lab(X(6500), 770, "about 8,000 years apart", tp + 1.0, BONE, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s27():
    """A staircase of equal blocks drawing a 45-degree line ('one up, one along'); then a small section of the pyramid: the King's
    northern shaft with its kinks (a straight sight line along its first leg hits stone: 'no straight view'); the two Queen's Chamber
    shafts climb and stop at little stone doors short of the faces: 'closed'."""
    t45, tb, tq = T("s27", "Forty-five degrees"), T("s27", "The northern shaft"), T("s27", "And the Queen's")
    x0, y0, st = 150, 700, 80
    els = [ln([(x0 - 40, y0), (x0 + 6 * st + 60, y0)], -1, "rgba(255,226,190,.4)", 2, draw=False)]
    for j in range(6):
        for i in range(j + 1):
            els.append(rect(x0 + j * st, y0 - (i + 1) * st, st - 3, st - 3, "#cdb184", "rgba(40,28,18,.6)", 1.2, 2, round(t45 - .3 + .05 * (j * (j + 1) / 2 + i), 2), fx="pop"))
    els += [ln([(x0, y0), (x0 + 6 * st, y0 - 6 * st)], t45 + 1.2, GOLD, 4, dur=1.0), lab(x0 + 2 * st, y0 - 3.4 * st, "45\u00b0", t45 + 1.6, GOLD, 34, "end")]
    els += [arr([(x0 + 2 * st, y0 + 40), (x0 + 3 * st, y0 + 40)], t45 + 1.8, BONE, 2.5, "known", .4, False), lab(x0 + 3.5 * st, y0 + 48, "one along", t45 + 1.9, BONE, 24, "start"),
            arr([(x0 + 6.5 * st, y0 - 2 * st), (x0 + 6.5 * st, y0 - 3 * st)], t45 + 2.1, BONE, 2.5, "known", .4, False), lab(x0 + 6.5 * st + 14, y0 - 2.5 * st, "one up", t45 + 2.2, BONE, 24, "start")]
    S = Section(s=3.4, cx=1270, gy=760)
    els += section_base(S, op=.4)
    k, q = kc_shafts(S), qc_shafts(S)
    els += [ln(k["north"], tb, GOLD, 3, dur=.9)]
    n1, n2 = k["north"][1], k["north"][2]
    d = (n2[0] - n1[0], n2[1] - n1[1])
    far = (n1[0] + d[0] * 2.4, n1[1] + d[1] * 2.4)
    els += [ln([n1, far], tb + .8, BONE, 2, "claimed", .6), ln([(far[0] - 12, far[1] - 12), (far[0] + 12, far[1] + 12)], tb + 1.3, LILAC, 4, dur=.2),
            ln([(far[0] - 12, far[1] + 12), (far[0] + 12, far[1] - 12)], tb + 1.4, LILAC, 4, dur=.2), lab(860, 300, "no straight view", tb + 1.5, LILAC, 26, "end"),
            ln([(866, 306), (far[0] - 14, far[1] - 10)], tb + 1.5, LILAC, 1.5, dur=.4)]
    els += [ln(q["south"], tq, AMBER, 3, dur=.8), ln(q["north"], tq + .2, AMBER, 3, dur=.8)]
    for p_ in (q["sdoor"], q["ndoor"]):
        els += [rect(p_[0] - 7, p_[1] - 7, 14, 14, GOLD, "#fff0c8", 1.5, 2, tq + .9, fx="pop")]
    els += [lab(q["sdoor"][0] + 26, q["sdoor"][1] + 10, "closed", tq + 1.1, GOLD, 26, "start"), lab(860, q["ndoor"][1] + 60, "closed", tq + 1.2, GOLD, 26, "end"),
            ln([(866, q["ndoor"][1] + 52), (q["ndoor"][0] - 10, q["ndoor"][1] + 6)], tq + 1.2, GOLD, 1.5, dur=.4)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================== CHAPTER 4 · What the builders left
MORTAR = "#c9a39a"


def s29():
    """Close on the joint between two great limestone blocks: pinkish mortar in the gap, black flecks in it; an inset fire burns
    under a heap of stone for the mortar, its smoke and ash drifting toward the joint; 'mortar', 'charcoal'."""
    tb, tf = T("s29", "burned wood"), T("s29", "bits of the fire")
    els = [rect(80, 140, 760, 650, "#cdb184", "rgba(255,236,206,.5)", 1.5, 6, -1), rect(80, 140, 760, 650, "url(#k-speck)", at=-1, r=6, op=.8),
           rect(912, 140, 790, 650, "#d4ba8e", "rgba(255,236,206,.5)", 1.5, 6, -1), rect(912, 140, 790, 650, "url(#k-speck)", at=-1, r=6, op=.8),
           poly([(840, 140), (912, 140), (908, 790), (846, 790)], MORTAR, "rgba(255,236,206,.4)", 1.2, -1),
           rect(840, 140, 72, 650, "url(#k-speck)", at=-1, op=.9), gl(420, 420, 600, -1, .12, "lamp")]
    rnd = random.Random(29)
    flecks = [(rnd.uniform(854, 898), 170 + 23.5 * j + rnd.uniform(-6, 6)) for j in range(26)]
    for j, (x, y) in enumerate(flecks):
        els += [poly([(x - 4, y - 3), (x + 3, y - 5), (x + 6, y + 1), (x + 1, y + 5), (x - 5, y + 3)], "#1a1410", "none", 0, -1)]
        if j % 4 == 0:
            els += [gl(x, y, 26, round(tf + .06 * j, 2), .8, "fire")]
    els += [lab(960, 300, "mortar", -1, BONE, 28, "start"), ln([(954, 292), (904, 280)], -1, BONE, 1.5, draw=False)]
    els += [lab(800, 520, "charcoal", tf + .4, GOLD, 28, "end"), ln([(806, 512), (858, 500)], tf + .4, GOLD, 1.5, dur=.3)]
    # the fire for the mortar
    ix, iy, iw, ih = 1150, 380, 480, 330
    els += [rect(ix, iy, iw, ih, "rgba(18,13,10,.92)", "rgba(255,236,206,.35)", 1.5, 14, tb, fx="pop")]
    hx, hy = ix + 240, iy + 250
    els += [poly([(hx - 150, hy), (hx - 90, hy - 80), (hx, hy - 110), (hx + 90, hy - 80), (hx + 150, hy)], "#bdb3a3", "rgba(255,246,230,.6)", 1.5, tb + .2, fx="rise", curve=True),
            gl(hx, hy + 20, 160, tb + .4, .8, "fire")]
    for k in range(5):
        x = hx - 100 + 50 * k
        els.append(poly([(x - 16, hy + 40), (x - 6, hy + 4), (x + 2, hy + 20), (x + 10, hy - 6), (x + 18, hy + 40)], "rgba(255,170,90,.85)", "none", 0, round(tb + .4 + .05 * k, 2), fx="pop"))
    els += [ln([(hx - 40, hy - 120), (hx - 70, hy - 170), (hx - 30, hy - 210), (hx - 90, hy - 250)], tb + .8, "rgba(220,214,200,.6)", 3, "claimed", 1.0, curve=True),
            lab(ix + iw / 2, iy + 40, "a fire for the mortar", tb + .5, GOLD, 26),
            arr([(ix - 10, iy + 120), (960, 520)], tf - .2, "rgba(242,201,142,.8)", 2.5, "inferred", .7)]
    return {"base": "dark", "cam": CAM, "els": els}


def candle(x, by, h, at, flame=True):
    out = [rect(x - 16, by - h, 32, h, "#efe4cf", "rgba(255,246,230,.6)", 1.2, 4, at, fx="pop"), ln([(x, by - h), (x, by - h - 10)], at, "#3a2a1c", 2, draw=False)]
    if flame:
        out += [gl(x, by - h - 22, 40, at, .9, "fire"), poly([(x - 7, by - h - 10), (x, by - h - 38), (x + 7, by - h - 10)], "#ffd08a", "none", 0, at, fx="pop", curve=True)]
    return out


def s30():
    """A tree, then a lump of charcoal; beside it candles that burn down as a clock; then rows of small sample vials pop by the
    hundred, chips '1984' and '1995'."""
    tt, tc, tk, ty, tn = T("s30", "Charcoal keeps"), T("s30", "living tree"), T("s30", "like a candle"), T("s30", "nineteen eighty-four"), T("s30", "hundreds of")
    gy = 680
    els = [ln([(80, gy), (960, gy)], -1, "rgba(255,226,190,.35)", 2, draw=False)]
    els += [rect(186, gy - 200, 28, 200, "#6b4a30", at=-1), circ(200, gy - 260, 90, "#3f6a3a", "rgba(200,240,190,.4)", 1.5, -1),
            circ(150, gy - 220, 60, "#4a7a44", at=-1), circ(250, gy - 215, 62, "#3a6236", at=-1), gl(200, gy - 240, 160, tc - .3, .35, "lamp")]
    els += [arr([(300, gy - 120), (380, gy - 120)], tt + .4, BONE, 2.5, "known", .4, False),
            poly([(420, gy), (430, gy - 46), (470, gy - 64), (520, gy - 40), (540, gy)], "#1d1915", "rgba(255,246,230,.4)", 1.5, tt + .5, fx="pop"),
            lab(480, gy + 40, "charcoal", tt + .6, BONE, 24)]
    els += [arr([(560, gy - 120), (620, gy - 120)], tk - .3, BONE, 2.5, "known", .4, False)]
    for j, h in enumerate((230, 185, 140, 95, 50)):
        els += candle(670 + 62 * j, gy, h, round(tk + .25 * j, 2))
    els += [lab(794, gy + 40, "a steady clock", tk + 1.2, GOLD, 26)]
    # the samples
    els += chip(1170, 200, "1984", AMBER, ty, 26) + chip(1430, 200, "1995", AMBER, ty + .6, 26)
    for i in range(140):
        r_, c_ = divmod(i, 14)
        x, y = 1010 + 46 * c_, 270 + 44 * r_
        at = round(tn - .6 + .012 * i, 3)
        els += [rect(x, y, 16, 30, "rgba(220,230,240,.25)", "rgba(220,230,240,.7)", 1.2, 3, at, fx="pop"), rect(x, y + 18, 16, 12, "#2a2420", at=at, fx="pop")]
    els += [lab(1330, 740, "hundreds of samples", tn + 1.2, BONE, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s31():
    """A time line 11,000 BCE to 2000 BCE with a magnified window over 3100 to 2400 BCE: Khufu's reign in the history books (amber)
    and the radiocarbon dates one to four centuries older (gold dots), 'one to four centuries'; an old beam reused in a fire ('old
    wood'); far to the left, about 10,000 BCE, an empty stretch with a lilac ring: 'no dates here'."""
    X = lambda yr: round(150 + (11000 - yr) / 9000 * 1480, 1)
    to, tw, tn = T("s31", "The dates came"), T("s31", "Builders probably"), T("s31", "None came")
    ticks = [(X(y), "%s BCE" % format(y, ",") if y in (11000, 2000) else format(y, ",")) for y in (11000, 10000, 8000, 6000, 4000, 2000)]
    els = [axis(150, 1630, 700, ticks, -1)]
    # the window
    wx0, wx1, wy0, wy1 = 960, 1640, 170, 470
    Z = lambda yr: round(wx0 + 40 + (3100 - yr) / 700 * (wx1 - wx0 - 80), 1)
    els += [rect(wx0, wy0, wx1 - wx0, wy1 - wy0, "rgba(18,13,10,.85)", "rgba(255,236,206,.35)", 1.5, 12, -1),
            ln([(X(3100), 690), (wx0, wy1)], -1, "rgba(255,236,206,.25)", 1.2, "inferred", draw=False), ln([(X(2400), 690), (wx1, wy1)], -1, "rgba(255,236,206,.25)", 1.2, "inferred", draw=False),
            rect(X(3100), 680, X(2400) - X(3100), 20, "rgba(255,236,206,.12)", at=-1)]
    els += [axis(wx0 + 40, wx1 - 40, wy1 - 70, [(Z(y), format(y, ",")) for y in (3000, 2800, 2600, 2400)], -1)]
    els += [{"k": "band", "x0": Z(2589), "x1": Z(2566), "y": wy1 - 130, "h": 18, "c": AMBER, "in": -1}, lab(Z(2577), wy1 - 152, "history books", -1, AMBER, 24)]
    rnd = random.Random(31)
    for j in range(16):
        yr = rnd.uniform(2577 + 100, 2577 + 400)
        els.append(circ(Z(yr), round(wy1 - 200 + rnd.uniform(-34, 34), 1), 6, GOLD, at=round(to + .1 * j, 2), fx="pop"))
    els += bracket(Z(2577 + 400), Z(2577 + 100), wy0 + 50, to + 1.5, None, GOLD, up=False) + [lab((Z(2977) + Z(2677)) / 2, wy0 + 36, "one to four centuries", to + 1.7, GOLD, 24)]
    # old wood
    bx, by = 640, 360
    els += [rect(bx - 150, by - 26, 260, 52, "#7a5a3c", "rgba(255,236,206,.45)", 1.5, 10, tw, fx="pop")]
    els += [ring_(bx + 110, by, r, round(tw + .2 + .05 * k, 2), "#c9a27a", 1.5, dur=.3) for k, r in enumerate((6, 12, 18, 24))]
    els += [gl(bx + 20, by + 70, 90, tw + .5, .8, "fire"), lab(bx - 20, by - 50, "old wood", tw + .4, BONE, 28)]
    # no dates near 10,000 BCE
    els += [ring_(X(10000), 680, 44, tn, LILAC, 3, "claimed", .8), lab(X(10000), 610, "no dates here", tn + .4, LILAC, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


VM = View(30.2, 33.4, 27.9, 30.6, (90, 130, 1100, 650))


def s32():
    """Map of northern Egypt: Giza, Tura, the Nile, and the Red Sea harbour at Wadi al-Jarf; a papyrus sheet unrolls with lines of
    script in black and red: 'the diary of Merer'."""
    v = VM
    th, tp, td = T("s32", "ancient harbour"), T("s32", "uncovered"), T("s32", "a work")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for path in (NILE, ROSETTA, DAMIETTA):
        els.append(ln([v.p(lo, la) for lo, la in path], -1, NILEC, 6, draw=False, curve=True, op=.9))
    gx, gyy = v.p(31.134, 29.979); tx, ty_ = v.p(31.28, 29.93); wx, wy = v.p(32.658, 28.892)
    els += [{"k": "pin", "x": gx, "y": gyy, "t": "Giza", "c": GOLD, "in": -1, "a": "end", "lx": -20, "ly": 8},
            {"k": "pin", "x": tx, "y": ty_, "t": "Tura", "c": "#cbbca8", "in": -1, "r": 6, "a": "start", "lx": 16, "ly": -14},
            {"k": "pin", "x": wx, "y": wy, "t": "a Red Sea harbour", "c": AMBER, "in": round(th, 2), "a": "end", "lx": -20, "ly": 40},
            lab(v.p(30.7, 28.3)[0], v.p(30.7, 28.3)[1], "Nile", -1, "#9fd0ff", 26, st="ital"),
            lab(v.p(33.05, 28.35)[0], v.p(33.05, 28.35)[1], "Red Sea", -1, "#9fc4d8", 26, st="ital"),
            {"k": "scale", "x": 140, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": -1}]
    # the papyrus
    px, py, pw, ph = 1250, 190, 420, 520
    els += [rect(px + 8, py + 12, pw, ph, "rgba(0,0,0,.45)", at=tp, fx="pop"), rect(px, py, pw, ph, "url(#k-papyrus)", "#f0dfba", 1.5, 3, tp, fx="pop"),
            rect(px - 22, py - 8, 26, ph + 16, "#c9ad7d", "#f0dfba", 1.5, 12, tp, fx="pop")]
    els += [{"k": "glyphs", "x": px + 30, "y": py + 40, "w": pw - 60, "h": ph - 80, "rows": 11, "cols": 9, "c": "#2a1d10", "red": True, "seed": 7, "sw": 3, "in": round(td, 2), "fx": "draw", "dur": 2.2}]
    els += [lab(px + pw / 2, py + ph + 50, "the diary of Merer", td + .6, GOLD, 30)]
    return {"base": "map", "cam": CAM, "els": els}


def s33():
    """Across the Nile in flood: boats carry white blocks from the Tura cliffs on the east bank (left) across the water toward Giza on
    the west (right), where the Great Pyramid stands in its white casing; chip 'year 27 of Khufu'; label 'the Horizon of Khufu'."""
    gy = 600
    base = {"base": "sky", "tod": "dawn", "ground": gy, "sun": [330, 210, 26], "groundc": "#5a4630",
            "ridges": [{"y": gy - 20, "a": 10, "c": "#6a5040", "seed": 4}]}
    tc, ty, tf, th = T("s33", "his crew ferried"), T("s33", "twenty-seventh"), T("s33", "across the"), T("s33", "Horizon of")
    els = [{"k": "water", "y": gy - 4, "h": 460, "op": .95, "x0": -60, "x1": 1860, "in": -1}]
    # Tura: white cliffs and quarry steps, east bank (left)
    els += [poly([(-60, gy + 200), (-60, 360), (120, 340), (250, 380), (330, gy - 10), (330, gy + 200)], "#e8dfcc", "rgba(255,246,230,.7)", 1.5, -1),
            poly([(150, 420), (240, 420), (240, 470), (300, 470), (300, 530)], "none", "rgba(120,100,80,.6)", 2, -1),
            lab(150, 320, "Tura", -1, BONE, 28)]
    # Giza: the plateau and the Great Pyramid in white casing, west bank (right)
    els += [poly([(1300, gy + 200), (1340, gy - 10), (1440, 520), (1860, 510), (1860, gy + 200)], "#8a6a48", "rgba(255,236,206,.5)", 1.5, -1),
            poly([(1440, 520), (1590, 330), (1740, 520)], "#f4ede0", "rgba(255,255,255,.9)", 1.5, -1), poly([(1590, 330), (1740, 520), (1630, 520)], "#cfc4b2", "none", 0, -1)]
    els += [lab(1690, 290, "the Horizon of Khufu", th, GOLD, 30, "end")]
    els += chip(889, 190, "year 27 of Khufu", AMBER, ty, 28)
    for j, (bx, by) in enumerate(((560, 660), (840, 690), (1110, 660))):
        at = round(tc + .4 * j, 2)
        els += [{"k": "boat", "x": bx, "y": by, "w": 200, "in": at, "fx": "rise"}]
        for q in range(3):
            els.append(rect(bx - 56 + 38 * q, by - 52, 34, 22, "#f4ede0", "rgba(80,60,40,.6)", 1.2, 2, at + .1, fx="pop"))
    els += [ln([(330, 610), (600, 650), (900, 700), (1150, 650), (1340, 600)], tf, GOLD, 2.4, "inferred", 1.6, curve=True)]
    base.update(cam=CAM, els=els)
    return base


def s34():
    """Plan of the builders' town south of the Sphinx, beyond its great stone wall: long galleries, bakeries with bread moulds,
    storerooms, drawing in as named; clay sealings pop with the names of Khafre and Menkaure; up the slope, small tombs."""
    tg, tb, ts, tk, tt = T("s34", "the town"), T("s34", "bakeries"), T("s34", "storerooms"), T("s34", "Clay seals"), T("s34", "Nearby lie")
    els = [rect(260, 210, 1000, 26, "#bba383", "rgba(255,236,206,.6)", 1.5, 3, -1), lab(760, 190, "the great stone wall", -1, DIM, 24),
           arr([(1240, 196), (1240, 130)], -1, BONE, 2.5, "known", .4, False), lab(1260, 150, "to the Sphinx", -1, DIM, 24, "start")]
    els += north(1640, 250, -1)
    for gset in range(4):
        gx0, gy0 = 360 + 170 * gset, 300
        for i in range(7):
            els.append(rect(gx0 + 20 * i, gy0, 12, 230, "#b88a64", "rgba(255,226,190,.35)", 1, 1, round(tg + .1 + .03 * (gset * 7 + i), 2), fx="pop"))
    els += [lab(640, 580, "long galleries", tg + .8, BONE, 26)]
    for i in range(4):
        x, y = 1080 + 52 * (i % 2), 300 + 52 * (i // 2)
        els += [rect(x, y, 44, 44, "#7a5a46", "rgba(255,226,190,.4)", 1.2, 2, round(tb + .1 * i, 2), fx="pop")]
        els += [circ(x + 12 + 18 * (q % 2), y + 12 + 18 * (q // 2), 6, "#c0503a", at=round(tb + .1 * i + .1, 2), fx="pop") for q in range(4)]
    els += [lab(1130, 440, "bakeries", tb + .5, BONE, 26)]
    for i in range(9):
        x, y = 1050 + 46 * (i % 3), 480 + 40 * (i // 3)
        els.append(rect(x, y, 38, 32, "#9c7a5a", "rgba(255,226,190,.35)", 1, 2, round(ts + .05 * i, 2), fx="pop"))
    els += [lab(1120, 640, "storerooms", ts + .5, BONE, 26)]
    for j, (sx, sy, name) in enumerate(((1440, 380, "Khafre"), (1440, 560, "Menkaure"))):
        at = round(tk + .5 * j, 2)
        els += [circ(sx, sy, 70, "#8a6a52", "rgba(255,226,190,.6)", 2, at, fx="pop"), poly(E(sx, sy, 50, 26, 24), "none", GOLD, 2, at + .1, fx="pop"),
                lab(sx, sy + 9, name, at + .2, GOLD, 24)]
    els += [lab(1440, 670, "clay seals", tk + .9, GOLD, 26)]
    for i in range(10):
        x, y = 110 + 52 * (i % 3) + 12 * (i // 3), 330 + 90 * (i // 3)
        els.append(rect(x, y, 40, 26, "#a88a64", "rgba(255,236,206,.4)", 1, 2, round(tt + .05 * i, 2), fx="pop"))
    els += [ring_(166, 613, 32, tt + .7, GOLD, 2), lab(80, 300, "workers' tombs", tt + .5, BONE, 26, "start"),
            lab(80, 690, "overseer of the side", tt + 1.0, GOLD, 26, "start")]
    return {"base": "plan", "north": False, "bg": "#241d17", "cam": CAM, "els": els}


def s35():
    """The plan of Giza builds in time order: Khufu's square first, then Khafre's beside it, then Menkaure's; beside it a strip with
    three reigns one after another, 'father', 'son', 'grandson'; dotted links: each placed beside the ones already there."""
    tf, ts, tg, tp = T("s35", "a father"), T("s35", "his son"), T("s35", "grandson"), T("s35", "find its place")
    x0, y0, k = 620, 200, .5
    els = []
    times = {"khufu": tf, "khafre": ts, "menkaure": tg}
    for kk in PYRS:
        q = plan_xy(kk, x0, y0, k); h = GP[kk][1] / 2 * k
        els.append(rect(q[0] - h, q[1] - h, 2 * h, 2 * h, "none", "rgba(242,220,180,.35)", 1.5, 0, -1, style="inferred"))
    for kk in PYRS:
        els += plan_sq(kk, x0, y0, k, round(times[kk], 2), fx="pop")
    els += north(840, 230, -1)
    pk = {kk: plan_xy(kk, x0, y0, k) for kk in PYRS}
    els += [ln([pk["khafre"], pk["khufu"]], tp, GOLD, 2, "inferred", .5), ln([pk["menkaure"], pk["khafre"]], tp + .4, GOLD, 2, "inferred", .5)]
    X = lambda yr: round(960 + (2600 - yr) / 110 * 680, 1)
    els += [axis(X(2600), X(2490), 620, [(X(y), "%d" % y) for y in (2600, 2550, 2500)], -1), lab(X(2490) + 10, 680, "BCE", -1, DIM, 24, "start")]
    for j, (name, a, b, rel, t) in enumerate((("Khufu", 2589, 2566, "father", tf), ("Khafre", 2558, 2532, "son", ts), ("Menkaure", 2532, 2503, "grandson", tg))):
        y = 540 - 70 * j
        els += [{"k": "band", "x0": X(a), "x1": X(b), "y": y, "h": 18, "c": AMBER, "in": round(t, 2)}, lab((X(a) + X(b)) / 2, y - 14, name, t + .1, AMBER, 24),
                lab((X(a) + X(b)) / 2, y - 44, rel, t + .3, BONE, 26)]
    return {"base": "plan", "north": False, "bg": "#1d1814", "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · Sah, the king's star
def star5(x, y, r, at, c=GOLD, op=None):
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        rr = r if k % 2 == 0 else r * .42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return poly(pts, c, "none", 0, at, op=op)


def lerp2(a, b, f):
    return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)


def quadpt(q, u, v):
    """A point inside quad q (four corners in order) at parameters u (along the first edge) and v (toward the opposite edge)."""
    return lerp2(lerp2(q[0], q[1], u), lerp2(q[3], q[2], u), v)


def s36():
    """Unas's burial chamber, seen from its doorway: a gabled ceiling painted with rows of five-pointed stars, walls filled with columns
    of signs (blue-green), the dark sarcophagus at the end; lamplight."""
    tt, ts = T("s36", "Pyramid Texts"), T("s36", "into the")
    bw = [(620, 360), (1158, 360), (1158, 690), (620, 690)]
    lw = [(80, 250), (620, 360), (620, 690), (80, 800)]
    rw = [(1698, 250), (1158, 360), (1158, 690), (1698, 800)]
    lc = [(80, 250), (889, 118), (889, 262), (620, 360)]
    rc = [(1698, 250), (889, 118), (889, 262), (1158, 360)]
    fl = [(80, 800), (620, 690), (1158, 690), (1698, 800)]
    WALL = "#cbb38c"
    els = [poly(lc, "#16213b", "rgba(255,236,206,.3)", 1.2, -1), poly(rc, "#1a2643", "rgba(255,236,206,.3)", 1.2, -1),
           poly(lw, WALL, "rgba(40,28,18,.5)", 1.2, -1), poly(rw, "#c3aa82", "rgba(40,28,18,.5)", 1.2, -1),
           poly(bw + [(889, 262)][:0], "#d2bb94", "rgba(40,28,18,.5)", 1.2, -1), poly([(620, 360), (889, 262), (1158, 360)], "#1d2a48", "rgba(255,236,206,.3)", 1.2, -1),
           poly(fl, "#6b5843", "none", 0, -1)]
    # columns of signs on the walls
    def columns(q, n, at, c="#2e5a64"):
        out = []
        for i in range(n):
            u0 = (i + .5) / n
            out.append(ln([quadpt(q, u0, .06), quadpt(q, u0, .94)], -1, "rgba(80,60,40,.25)", 1, draw=False))
            pts = []
            for j in range(16):
                a = quadpt(q, u0 - .25 / n, .08 + j * .054); b = quadpt(q, u0 + .25 / n, .08 + j * .054 + .02)
                out.append(ln([a, b], round(at + .02 * i, 2), c, 2.6, dur=.2))
        return out
    els += columns([lw[0], lw[1], lw[2], lw[3]], 9, tt - .4)
    els += columns([rw[1], rw[0], rw[3], rw[2]], 9, tt - .2)
    els += [{"k": "glyphs", "x": 650, "y": 380, "w": 480, "h": 200, "rows": 6, "cols": 12, "c": "#2e5a64", "seed": 5, "sw": 2.6, "in": round(tt, 2), "fx": "draw", "dur": 1.6}]
    # stars on the ceiling
    for q, k0 in ((lc, 0), (rc, 1)):
        for i in range(6):
            for j in range(4):
                p_ = quadpt(q, (i + .5) / 6, (j + .5) / 4)
                els.append(star5(p_[0], p_[1], 9 - 1.2 * j, round(ts + .03 * (i * 4 + j) + .2 * k0, 2), "#f2d58e"))
    els += [poly([(780, 690), (1000, 690), (1000, 610), (780, 610)], "#2a2a30", "rgba(220,220,230,.4)", 1.5, -1), poly([(780, 610), (1000, 610), (980, 596), (800, 596)], "#3a3a42", "none", 0, -1),
            gl(889, 560, 520, -1, .18, "lamp")]
    els += chip(889, 724, "the Pyramid Texts", AMBER, tt + .6, 30) + [lab(889, 782, "tomb of Unas, about 2350 BCE", tt + 1.0, BONE, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s37():
    """Orion's stars with the striding figure of Sah drawn through them (schematic), 'Sah, linked with Osiris'; lower left Sirius
    flares, 'Sopdet, linked with Isis'; then a new bright star pops beside the belt, a dotted ring round it, 'the companion of Orion'."""
    cx, cy, k = 1080, 360, 20.0
    o, P = orion(cx, cy, k, -1, op=.35)
    els = [{"k": "stars", "n": 120, "x0": -40, "x1": 1820, "y0": 100, "y1": 800, "seed": 91, "in": -1}] + o
    th, ts, tc = T("s37", "They speak of Sah"), T("s37", "Sopdet"), T("s37", "the companion")
    belt = P["Alnilam"]
    els += [ln([P[a], P[b]], round(th + .1 * j, 2), GOLD, 2.6, dur=.5) for j, (a, b) in enumerate(FIGL)]
    els += [gl(cx, cy, 260, th, .25), lab(cx + 200, cy - 150, "Sah, linked with Osiris", th + .6, GOLD, 30, "start")]
    si = sky("Sirius", cx, cy, k)
    els += [gl(si[0], si[1], 120, ts, .8, "blue"), circ(si[0], si[1], 9, "#eaf2ff", at=ts, fx="pop"), lab(si[0] + 30, si[1] + 8, "Sopdet, linked with Isis", ts + .3, "#cfe0ff", 28, "start")]
    nx, ny = belt[0] + 120, belt[1] - 20
    els += [gl(nx, ny, 70, tc, .9), circ(nx, ny, 8, STAR, at=tc, fx="pop"), ring_(nx, ny, 26, tc + .2, GOLD, 2, "claimed", .6),
            lab(nx + 40, ny + 64, "the companion of Orion", tc + .4, GOLD, 32, "start", st="ital")]
    return {"base": "sky", "tod": "night", "ground": 1100, "sun": False, "ridges": [], "cam": CAM, "els": els}


def s38():
    """The northern sky: star trails circling the pole, none touching the horizon, 'the Imperishable Stars'; then both skies over the
    pyramid in section, its two shafts glowing, one toward each."""
    tn, t2, tb = T("s38", "They speak of the north"), T("s38", "Two skies"), T("s38", "point to")
    hz = 700
    els = [{"k": "stars", "n": 140, "x0": -40, "x1": 1820, "y0": 100, "y1": hz - 10, "seed": 93, "in": -1}]
    px, py = 420, hz - 30 * 9.0
    rnd = random.Random(38)
    for j, r in enumerate((36, 70, 110, 150, 190, 228, 262)):
        a0 = rnd.uniform(0, 360)
        arcp = [(px + r * math.cos(math.radians(a0 + d)), py + r * math.sin(math.radians(a0 + d))) for d in range(0, 251, 10)]
        els += [ln(arcp, round(tn + .12 * j, 2), "rgba(255,246,230,.75)", 2, dur=1.2, curve=True), circ(arcp[-1][0], arcp[-1][1], 3.4, STAR, at=round(tn + 1.2 + .12 * j, 2))]
    els += [circ(px, py, 4, GOLD, at=tn), lab(px, 150, "the Imperishable Stars", tn + .6, GOLD, 30)]
    o, P = orion(1340, 300, 12.0, -1, op=.5)
    els += o
    S = Section(s=1.6, cx=889, gy=hz)
    els += section_base(S, op=.5)
    sh = kc_shafts(S)
    els += [ln(sh["south"], tb, "#ffe2a8", 3, dur=.5), ln(sh["north"], tb, "#ffe2a8", 3, dur=.5)]
    els += [ln([sh["nface"], (px + 40, py + 20)], tb + .4, GOLD, 2.4, "claimed", 1.0), ln([sh["sface"], (P["Alnitak"][0] - 20, P["Alnitak"][1] + 14)], tb + .4, GOLD, 2.4, "claimed", 1.0)]
    els += [lab(889, 380, "two skies", t2, BONE, 34, st="serif"), lab(260, hz + 46, "north", -1, DIM, 24), lab(1500, hz + 46, "south", -1, DIM, 24)]
    return {"base": "sky", "tod": "night", "ground": hz, "sun": False, "groundc": "#1d1915", "ridges": [{"y": hz - 4, "a": 4, "c": "#1b1922", "seed": 3}], "cam": CAM, "els": els}


def s39():
    """A time strip: Khufu (about 2570 BCE) and Unas (about 2350 BCE), 'about two centuries'; above, the section with a dotted gold path
    of the king's spirit rising up the southern shaft into the sky."""
    tt, ts = T("s39", "These texts"), T("s39", "a road")
    S = Section(s=2.2, cx=889, gy=560)
    base, els = night_sky(560, seed=94, n=110, glow_x=889)
    els += section_base(S, op=.45)
    sh = kc_shafts(S)
    els += [ln(sh["south"], -1, GOLD, 2.6, draw=False, op=.7)]
    p0 = sh["south"][0]
    sf = sh["sface"]
    end = (sf[0] + 240, sf[1] - 240)
    path = [p0, sh["south"][1], sf, end]
    for j in range(9):
        f = j / 8
        if f < .5:
            q = lerp2(sh["south"][1], sf, f * 2)
        else:
            q = lerp2(sf, end, (f - .5) * 2)
        els += [gl(q[0], q[1], 30, round(ts + .18 * j, 2), .9), circ(q[0], q[1], 5, "#fff3d6", at=round(ts + .18 * j, 2), fx="pop", op=round(.4 + .07 * j, 2))]
    els += star(end[0] + 20, end[1] - 20, 1.7, ts + 1.6, 1.4) + [lab(end[0] + 50, end[1] + 30, "a road for the spirit", ts + 1.8, GOLD, 28, "start")]
    X = lambda yr: round(300 + (2650 - yr) / 350 * 1180, 1)
    y = 690
    els += [axis(X(2650), X(2300), y, [(X(v), format(v)) for v in (2600, 2500, 2400, 2300)], -1), lab(X(2300) + 44, y + 46, "BCE", -1, DIM, 24, "start")]
    els += [circ(X(2577), y, 10, AMBER, at=tt, fx="pop"), lab(X(2577), y - 26, "Khufu", tt, AMBER, 28),
            circ(X(2360), y, 10, GOLD, at=tt + .6, fx="pop"), lab(X(2360), y - 26, "Unas, the texts", tt + .6, GOLD, 28)]
    els += bracket(X(2577), X(2360), y - 70, tt + 1.0, None, BONE, up=False) + [lab((X(2577) + X(2360)) / 2, y - 92, "about two centuries", tt + 1.2, BONE, 26)]
    base.update(cam=CAM, els=els)
    return base


def s40():
    """The three pyramids and the three stars facing each other across the panel; a dotted line starts to join them and stops halfway at
    a lilac '?'; below, a papyrus with columns of text, blank where that line would be: 'no such text yet'."""
    t0 = T("s40", "What no Egyptian")
    gy = 560
    els = [ln([(80, gy), (760, gy)], -1, "rgba(255,226,190,.4)", 2, draw=False)]
    for x, w in ((230, 230), (440, 215), (620, 105)):
        els += [poly([(x - w / 2, gy), (x, gy - w * .636), (x + w / 2, gy)], "url(#k-stoneC)", "rgba(255,236,206,.6)", 1.5, -1),
                poly([(x, gy - w * .636), (x + w / 2, gy), (x + w * .1, gy)], "rgba(60,44,30,.35)", "none", 0, -1)]
    P = {n: sky(n, 1360, 300, 80.0) for n in BELT}
    for n in BELT:
        els += star(P[n][0], P[n][1], STARS[n][2], -1, 1.6)
    els += [ln([(660, 420), (900, 380)], t0 + .2, LILAC, 3, "claimed", .8)] + qmark(970, 400, t0 + 1.0, 80)
    px, py, pw, ph = 660, 600, 600, 190
    els += [rect(px, py, pw, ph, "url(#k-papyrus)", "#f0dfba", 1.5, 3, -1),
            {"k": "glyphs", "x": px + 20, "y": py + 20, "w": 200, "h": ph - 40, "rows": 5, "cols": 6, "c": "#2a1d10", "seed": 3, "sw": 2.6, "in": -1},
            {"k": "glyphs", "x": px + pw - 220, "y": py + 20, "w": 200, "h": ph - 40, "rows": 5, "cols": 6, "c": "#2a1d10", "seed": 9, "sw": 2.6, "in": -1},
            rect(px + 240, py + 24, pw - 480, ph - 48, "none", LILAC, 2, 6, t0 + .6, style="claimed"), lab(px + pw / 2, py + ph / 2 + 9, "?", t0 + .8, LILAC, 40, st="serif")]
    els += [lab(1290, 700, "no such text, so far", t0 + 1.2, LILAC, 28, "start")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s41():
    """Dawn over the pyramids seen from the east (north to the right): Orion low in the west above them; a small gold star rises from
    the Great Pyramid toward the belt; then faint lilac dotted lines from the belt down to the pyramids, and a small '?'."""
    gy = 640
    base = {"base": "sky", "tod": "dawn", "ground": gy, "sun": False, "groundc": "#3a2e24",
            "ridges": [{"y": gy - 10, "a": 8, "c": "#3a2f36", "seed": 4}]}
    tj, td = T("s41", "hoped to"), T("s41", "drew it on")
    els = [{"k": "stars", "n": 80, "x0": -40, "x1": 1820, "y0": 100, "y1": 420, "seed": 95, "in": -1}]
    o, P = orion(860, 260, 14.0, -1, tilt=-25, op=.45)
    els += o
    pyr = [(560, gy, 190), (900, gy - 8, 390), (1270, gy, 420)]           # from the east: Menkaure (south) left, Khafre, Khufu (north) right
    for x, y, w in pyr:
        els += [{"k": "pyramid", "x": x, "y": y, "w": w, "courses": False, "light": "right", "in": -1}]
    apex = (1270 + 420 * .18 * .35, gy - 420 * .636)
    tgt = (P["Alnitak"][0] + 30, P["Alnitak"][1] + 24)
    mid = (1180, 330)
    els += [ln([apex, mid, tgt], tj, GOLD, 2.4, "claimed", 1.6, curve=True)]
    for j, f in enumerate((.2, .5, .8)):
        q = lerp2(lerp2(apex, mid, f), lerp2(mid, tgt, f), f)
        els += [gl(q[0], q[1], 30, round(tj + .5 * j, 2), .9), circ(q[0], q[1], 5, "#fff3d6", at=round(tj + .5 * j, 2), fx="pop")]
    for j, (n, (x, y, w)) in enumerate(zip(BELT, pyr[::-1])):
        els += [ln([(P[n][0], P[n][1] + 10), (x, y - w * .636 - 6)], round(td + .2 * j, 2), LILAC, 1.8, "claimed", .8, op=.7)]
    els += qmark(700, 400, td + .9, 56, halo=False)
    base.update(cam=CAM, els=els)
    return base


# ================================================================== CHAPTER 6 · The weighing
LROWS = [200, 330, 460, 590]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 52, 1500, 104, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(320, y + 10, text, at + .1, BONE, 30, "start")]
    out += pic(225, y, at + .1)
    if grade:
        out += chip(1200, y, grade, gc, gt, 28, "start")
    return out


def pic_pyrs(x, y, at):
    out = []
    for dx, w in ((-38, 40), (0, 38), (34, 20)):
        out.append(poly([(x + dx - w / 2, y + 26), (x + dx, y + 26 - w * .8), (x + dx + w / 2, y + 26)], "#dcc497", "rgba(255,236,206,.6)", 1.2, at, fx="pop"))
    return out


def pic_shaft(x, y, at):
    return [poly([(x - 46, y + 28), (x - 6, y - 26), (x + 34, y + 28)], "#dcc497", "rgba(255,236,206,.6)", 1.2, at, fx="pop"),
            ln([(x - 6, y + 8), (x + 30, y - 22)], at, GOLD, 2, draw=False), ln([(x + 30, y - 22), (x + 50, y - 40)], at, GOLD, 2, "claimed", draw=False),
            circ(x + 54, y - 44, 4, STAR, at=at, fx="pop")]


def pic_plan(x, y, at):
    out = []
    for dx, dy, h in ((22, -22, 14), (2, -2, 13), (-12, 20, 7)):
        out += [rect(x + dx - h, y + dy - h, 2 * h, 2 * h, "#dcc497", at=at, fx="pop"), circ(x + dx, y + dy, 3.4, STAR, at=at + .05, fx="pop")]
    return out


def pic_date(x, y, at):
    return [rect(x - 50, y - 20, 100, 40, "rgba(201,193,238,.08)", LILAC, 2, 20, at, fx="pop", style="claimed"), lab(x, y + 9, "?", at, LILAC, 30, st="serif")]


def s42():
    """The ledger fills row by row: 'built by three kings, about 2500 BCE' Established; 'shafts aimed at the stars of that age'
    Plausible (small tag 'or builders' slopes')."""
    t1, g1 = T("s42", "Three pyramids built"), T("s42", "established")
    t2, g2, td = T("s42", "Shafts aimed"), T("s42", "Plausible"), T("s42", "Simple builders'")
    els = [rect(110, 135, 1560, 530, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, t1, pic_pyrs, "built by three kings, about 2500 BCE", "Established", g1, GRADE["established"])
    els += lrow(1, t2, pic_shaft, "shafts aimed at the stars of that age", "Plausible", g2, GRADE["plausible"])
    els += [lab(1200, LROWS[1] + 46, "or builders' simple slopes", td, DIM, 24, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s43_add():
    """Row 3: 'a plan copied from Orion's Belt' Open question; small tags for and against."""
    t3, g3, tf, ta = T("s43", "A plan copied"), T("s43", "Open question"), T("s43", "The likeness is"), T("s43", "But the plan")
    els = lrow(2, t3, pic_plan, "a plan copied from Orion's Belt", "Open question", g3, GRADE["open"])
    els += [lab(320, LROWS[2] + 46, "for: a real likeness, Sah", tf, GREEN, 24, "start"), lab(760, LROWS[2] + 46, "against: three reigns, a turned sky, no text", ta, RED, 24, "start")]
    return els


def s44_add():
    """Row 4: 'a map of the sky of 10,500 BCE' Awaiting evidence, glowing; small tags."""
    t4, g4, tx = T("s44", "And a map"), T("s44", "Awaiting evidence"), T("s44", "The claimed match")
    els = lrow(3, t4, pic_date, "a map of the sky of 10,500 BCE", "Awaiting evidence", g4, GRADE["awaiting"])
    els += [gl(1330, LROWS[3], 230, g4, .35), lab(320, LROWS[3] + 46, "about 10\u00b0 off; nothing built then is dated", tx, LILAC, 24, "start")]
    return els


def s45():
    """Three 'wanted' cards in lilac dashed outline, popping as named: a papyrus with three squares and three stars; three survey pegs
    and a cord on bare rock; a hearth and the foot of a wall with a sample tag 'about 10,500 BCE?'."""
    t1, t2, t3 = T("s45", "An Egyptian text"), T("s45", "Signs that"), T("s45", "Or anything")
    els = [gl(889, 420, 700, .1, .18, "lamp")]
    els += [rect(x - 220, 190, 440, 440, "rgba(201,193,238,.03)", "rgba(201,193,238,.5)", 1.8, 18, -1, style="claimed") for x in (370, 889, 1408)]
    def card(x, at, title):
        return [rect(x - 220, 190, 440, 440, "rgba(201,193,238,.06)", LILAC, 2.5, 18, at, fx="pop", style="claimed"), lab(x, 690, title, at + .4, LILAC, 28)]
    xs = (370, 889, 1408)
    els += card(xs[0], t1, "a text or a plan")
    els += [rect(xs[0] - 150, 260, 300, 300, "url(#k-papyrus)", "#f0dfba", 1.5, 3, t1 + .1, fx="pop")]
    for j, (dx, dy) in enumerate(((-60, 120), (-15, 75), (20, 20))):
        els += [rect(xs[0] + dx - 14, 260 + dy + 130, 28, 28, "#8c7152", at=t1 + .3 + .1 * j, fx="pop"), circ(xs[0] + dx + 60, 260 + dy + 40, 6, "#2a1d10", at=t1 + .4 + .1 * j, fx="pop")]
    els += [ln([(xs[0] - 50, 520), (xs[0] + 75, 330)], t1 + .7, "#8a2a1a", 2, "claimed", .6)]
    els += card(xs[1], t2, "marked out together")
    els += [rect(xs[1] - 170, 420, 340, 140, "#8c7152", "rgba(255,236,206,.4)", 1.5, 6, t2 + .1, fx="pop")]
    pegs = [(xs[1] - 110, 470), (xs[1] - 10, 430), (xs[1] + 80, 380)]
    for j, (x, y) in enumerate(pegs):
        els += [ln([(x, y + 60), (x, y)], round(t2 + .3 + .15 * j, 2), "#e9dcc4", 6, dur=.3), circ(x, y, 7, AMBER, at=round(t2 + .4 + .15 * j, 2), fx="pop")]
    els += [ln([pegs[0], pegs[1], pegs[2]], t2 + .9, AMBER, 2, dur=.6)]
    els += card(xs[2], t3, "a dated building")
    hx = xs[2]
    els += [rect(hx - 170, 470, 340, 90, "#6d5a46", at=t3 + .1, fx="pop"), rect(hx + 30, 380, 130, 90, "#b89a70", "rgba(40,28,18,.6)", 1.2, 2, t3 + .2, fx="pop"),
            gl(hx - 70, 460, 80, t3 + .3, .8, "fire"), poly([(hx - 100, 470), (hx - 85, 430), (hx - 70, 452), (hx - 58, 420), (hx - 44, 470)], "rgba(255,170,90,.85)", "none", 0, t3 + .3, fx="pop")]
    els += chip(hx, 300, "about 10,500 BCE?", LILAC, t3 + .6, 24)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s46():
    """The close: the three pyramids at night seen from the north, Orion's Belt high in the south (about 58 degrees); lower down, a
    faint gold ghost of the belt where it crossed in Khufu's day (about 45 degrees): 'in Khufu's day', 'tonight'."""
    hz = 700
    base, els = night_sky(hz, seed=99, n=180, glow_x=889)
    els += milky_way(-1, 700, 110, 600, hz - 4, 14, 120, .06)
    ky = 7.0
    bx, by = 1010, hz - 58 * ky
    gy_ = hz - 45 * ky
    for n in BELT:
        x, y = sky(n, bx, by, 26.0)
        els += star(x, y, STARS[n][2], -1, 1.4)
    for n in ("Betelgeuse", "Rigel"):
        x, y = sky(n, bx, by, 26.0)
        els += star(x, y, STARS[n][2], -1, .9, op=.6)
    tq = T("s46", "higher than")
    for n in BELT:
        x, y = sky(n, bx, gy_, 26.0)
        els += [circ(x, y, 12, "none", GOLD, 2.6, tq, style="claimed", fx="pop"), circ(x, y, 3, GOLD, at=tq, fx="pop", op=.6)]
    els += [arr([(bx + 110, gy_ - 10), (bx + 110, by + 30)], tq + .4, GOLD, 2.5, "inferred", .6, False),
            lab(bx - 90, gy_ + 26, "in Khufu's day", tq + .3, GOLD, 28, "end"), lab(bx - 90, by + 22, "tonight", tq + .5, BONE, 28, "end")]
    for x, w in ((560, 300), (820, 280), (1060, 140)):
        els += [poly([(x - w / 2, hz), (x, hz - w * .62), (x + w / 2, hz)], "#1d1a22", "rgba(226,230,255,.45)", 1.4, -1)]
    base.update(cam=[1.03, 889, 500], els=els)
    return base


def _todo(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 500, sid, .2, DIM, 60, st="serif")]}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "Now look", "s2"), (2, "And inside", "s3"), (3, "Did Egypt's", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "Khufu's and", "s6")], {"chapter": "Three stars, three pyramids"}),
    (1, 1, "collision", "s7", [(1, "And the", "s8")], {}),
    (1, 2, "reversal", "s9", [(1, "In {1989", "s10")], {}),
    (1, 3, "tag", "s11", [(1, "A real likeness", "s12")], {}),
    (2, 0, "world", "s13", [(1, "These days", "s14")], {"chapter": "A sky from 10,500 BCE?"}),
    (2, 1, "collision", "s15", [(1, "Later, with", "s16")], {}),
    (2, 2, "cost", "s17", [(1, "In fairness", "s18")], {}),
    (2, 3, "reversal", "s19", [(1, "In {1999", "s20")], {}),
    (2, 4, "tag", "s21", [], {}),
    (3, 0, "world", "s22", [], {"chapter": "Shafts aimed at the stars"}),
    (3, 1, "collision", "s23", [(1, "The southern shaft", "s24")], {}),
    (3, 2, "cost", "s25", [(1, "Notice the", "s26")], {}),
    (3, 3, "reversal", "s27", [], {}),
    (3, 4, "tag", "s28", [], {}),
    (4, 0, "world", "s29", [], {"chapter": "What the builders left"}),
    (4, 1, "collision", "s30", [(1, "The dates came", "s31")], {}),
    (4, 2, "cost", "s32", [(1, "In the twenty-seventh", "s33")], {}),
    (4, 3, "reversal", "s34", [], {}),
    (4, 4, "tag", "s35", [], {}),
    (5, 0, "world", "s36", [(1, "They speak of Sah", "s37")], {"chapter": "Sah, the king's star"}),
    (5, 1, "collision", "s38", [], {}),
    (5, 2, "reversal", "s39", [(1, "What no Egyptian", "s40")], {}),
    (5, 3, "tag", "s41", [], {}),
    (6, 0, "weigh", "s42", [(2, "A plan copied", "s43"), (3, "And a map", "s44")], {"chapter": "The weighing"}),
    (6, 1, "test", "s45", [], {}),
    (6, 2, "close", "s46", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.75, 1010, 330], "s2_add"),
    "s4": ("s1", [1, 889, 500], "s4_add"),
    "s12": ("s6", [1, 889, 500], "s12_add"),
    "s14": ("s13", [1.3, 1150, 470], "s14_add"),
    "s24": ("s22", [1, 889, 500], "s24_add"),
    "s28": ("s22", [1, 889, 500], "s28_add"),
    "s43": ("s42", [1, 889, 500], "s43_add"),
    "s44": ("s42", [1, 889, 500], "s44_add"),
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
                panels[sid] = g[sid]() if sid in g else _todo(sid)
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
    ep = {"id": "lf-orion", "code": "LF.28", "series": script["series"], "title": script["title"], "case": "orion-correlation",
          "verdict": "unsupported", "claim": "Do the Giza pyramids copy Orion's Belt, and does the sky point to 10,500 BCE?", "mood": "mystery",
          "hook_text": "A map of the *stars*?", "beats": beats, "shots": shots,
          "sources": "Bauval 1989 (Discussions in Egyptology 13) · Krupp 1997 (Sky & Telescope) · Legon 1995 (Discussions in Egyptology 33) · "
                     "Fairall 1999 (doi:10.1093/astrog/40.3.3.4) · Allan 2026 (doi:10.3724/SP.J.1440-2807.2026.02.06) · "
                     "Bonani et al. 2001 (doi:10.1017/S0033822200038558) · Tallet & Marouard 2014 (doi:10.5615/neareastarch.77.1.0004) · "
                     "Vondrak et al. 2011 (doi:10.1051/0004-6361/201117274) · Faulkner 1969",
          "post": "Three pyramids, three stars. Is Giza a map of Orion's Belt, and does the sky point to 10,500 BCE? The claim at its strongest, "
                  "the turn the map needs, the lean that misses, the shafts' stars of about 2500 BCE, Merer's diary and the Pyramid Texts, weighed.",
          "hashtags": ["#Orion", "#Giza", "#Pyramids", "#AncientEgypt", "#Astronomy", "#WeighItYourself"],
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
