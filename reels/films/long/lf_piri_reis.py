"""LF.20 · Unreadable · The Piri Reis Map: Antarctica Before the Ice? (16:9 long film, one wall).

The script is films/long/lf-piri-reis/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s51; s4, the title, is the intro card over the
panel of s3), drawn while it is said: the 1513 map on its gazelle skin (the hero, revisited six times: the southern coast, Saint
Brendan's whale, the corner where the coast turns, the snake and its note, the close), the voyage from Gallipoli to the Book of the
Sea and its charts, the map's long sleep and its finding in Topkapi, Piri's notes and their twenty sources, the Spanish sailor and
Columbus's fingerprints, the Antarctica claim from a 1956 radio panel and a 1960 Air Force letter to Hapgood's book, the Drake
Passage, the hide's curved corner, the coast of Brazil at 25 degrees south, the Portuguese map of 1519, the jigsaw, Bellingshausen's
wall of ice, the ice sheet in section, Bedmap2's measurements, the EPICA core and the sea-floor record, the football pitch, the
ledger and the tests. Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted = claimed
(the Antarctica claim is lilac and dotted throughout).

Facts: the Short 'piri-reis' (f12.py, rewrite/piri-reis.json) and the script's facts_added (Soucek 1992; McIntosh 2000; Kahle 1933;
Hapgood 1966 with the Ohlmeyer letter of 6 July 1960; Hancock 1995; Fretwell et al. 2013; Ruth et al. 2007; EPICA 2006;
DeConto & Pollard 2003; Hublin et al. 2017).

Engine workaround (as in lf_troy.py): the wall only adds elements to a panel on its first visit, at a beat start or a line start;
shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag, invisible);
after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that step's clock).
Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25 syllables a second).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-piri-reis/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-piri-reis/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-piri-reis RC_FILMS_EPS=/tmp/claude-0/sbx_lf-piri-reis/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-piri-reis/boards python3 films.py long.lf_piri_reis
"""
import json, math, os, random, re
import films as F
from films import View
from mural import remix
import illus as I
from illus import glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-piri-reis", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
PARCH, PARCH_D, PARCH_L = "#d9c29a", "#a88660", "#ead9b6"          # the gazelle skin
INK, RINK, GINK, BINK = "#3a2618", "#a8321f", "#3d6b44", "#2f5d7c"  # Piri's inks: black-brown, red, green, blue
LANDT = "rgba(122,86,48,.16)"                                      # land on the skin: a faint brown wash
ICE, ICE_D, ICE_S = "#eaf3f8", "#b9d2e2", "#8fb3cc"
ROCK, ROCK_D = "#5e5048", "#3a302b"
SEA_D = "#123247"
SKIN, WOOD, WOOD_D = "#e8d6b8", "#6b4a30", "#3a281a"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "open": "#f0b06a", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
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


def man(x, y, h, at, c=SKIN, fx="rise", turban=None, op=None):
    """A standing figure (the kit's person) with an optional turban (a light dome over the head)."""
    out = [{"k": "person", "x": round(x, 1), "y": round(y, 1), "h": round(h, 1), "t": False, "color": c, "in": round(at, 2), "fx": fx}]
    if op is not None:
        out[0].update(op=op, keepop=True)
    if turban:
        hy = y - h * .9
        out.append(poly(E(x, hy - h * .035, h * .085, h * .06, 16), turban, "rgba(0,0,0,.25)", 1, at, fx=fx))
    return out


def seated(x, y, h, at, c=SKIN, stool=True, face=1, turban=None):
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
    if turban:
        out.append(poly(E(X(.04 * h), y - .78 * h, .095 * h, .06 * h, 16), turban, "rgba(0,0,0,.25)", 1, at, fx="rise"))
    return out


def kadirga(x, y, w, at, c="#2a1d14", sail="#e8d6b8", face=1, op=None, fx=None, oars=True, cabin=True):
    """An Ottoman galley in side view: a long low hull, a raised stern, a lateen sail on a slanting yard, a row of oars; y = waterline."""
    f = face
    X = lambda a: x + f * a * w
    hull = [[X(-.5), y - .07 * w], [X(-.44), y - .02 * w], [X(.36), y - .02 * w], [X(.5), y - .06 * w], [X(.56), y - .05 * w], [X(.44), y + .015 * w],
            [X(-.4), y + .02 * w], [X(-.52), y - .03 * w]]
    out = [poly(hull, c, "rgba(255,226,190,.35)", 1, at, fx=fx, op=op)]
    if cabin:
        out.append(poly([[X(-.5), y - .07 * w], [X(-.36), y - .07 * w], [X(-.36), y - .12 * w], [X(-.5), y - .12 * w]], c, "rgba(255,226,190,.3)", 1, at, fx=fx, op=op))
    out += [
           ln([[X(.02), y - .03 * w], [X(.02), y - .36 * w]], at, c, max(2, .012 * w), draw=False, op=op),
           poly([[X(-.22), y - .1 * w], [X(.34), y - .44 * w], [X(.12), y - .08 * w]], sail, "rgba(60,40,20,.5)", 1, at, fx=fx, op=op),
           ln([[X(-.26), y - .07 * w], [X(.4), y - .48 * w]], at, c, max(2, .01 * w), draw=False, op=op)]
    if oars:
        out += [ln([[X(-.3 + .06 * k), y - .01 * w], [X(-.36 + .06 * k), y + .09 * w]], at, c, max(1.5, .006 * w), draw=False, op=op) for k in range(11)]
    return out


def caravel(x, y, s, at, c=INK, sail="#efe2c4", fx=None, op=None, face=1, red=RINK):
    """A small ship as Piri draws them: a round hull, two masts, square sails, a pennant; y = waterline, s = length."""
    f = face
    X = lambda a: x + f * a * s
    out = [poly([[X(-.5), y - .16 * s], [X(.5), y - .2 * s], [X(.36), y + .05 * s], [X(-.36), y + .05 * s]], c, "none", 0, at, fx=fx, op=op),
           ln([[X(-.08), y - .16 * s], [X(-.08), y - .95 * s]], at, c, max(1, .04 * s), draw=False, op=op),
           ln([[X(.26), y - .18 * s], [X(.26), y - .7 * s]], at, c, max(1, .035 * s), draw=False, op=op),
           poly([[X(-.3), y - .82 * s], [X(.14), y - .82 * s], [X(.18), y - .3 * s], [X(-.34), y - .3 * s]], sail, c, max(.8, .025 * s), at, fx=fx, op=op, curve=False),
           poly([[X(.12), y - .62 * s], [X(.4), y - .62 * s], [X(.42), y - .3 * s], [X(.1), y - .3 * s]], sail, c, max(.8, .025 * s), at, fx=fx, op=op),
           poly([[X(-.08), y - .95 * s], [X(.14), y - 1.0 * s], [X(-.08), y - 1.05 * s]], red, "none", 0, at, fx=fx, op=op)]
    return out


def glyph_block(x, y, w, h, at, rows=3, c=INK, seed=1, sw=2.0, red=False, op=None, fx=None):
    """A block of flowing script (Piri's notes): strokes in the kit's cursive glyphs, an optional red first line."""
    cols = max(2, int(w / 22))
    e = {"k": "glyphs", "x": round(x, 1), "y": round(y, 1), "w": round(w, 1), "h": round(h, 1), "rows": rows, "cols": cols, "kind": "hieratic", "c": c,
         "seed": seed, "sw": sw, "in": round(at, 2)}
    if red:
        e["red"] = True
    if op is not None:
        e.update(op=op)
    if fx:
        e["fx"] = fx
    return [e]


def mountains(pts, s, at, c=INK, fill="rgba(122,86,48,.28)", op=None):
    """Little peaked mountains as on the old charts, one at each point, size s."""
    out = []
    for k, (x, y) in enumerate(pts):
        out.append(poly([[x - s * .6, y], [x - s * .12, y - s * .95], [x + s * .1, y - s * .7], [x + s * .3, y - s * 1.05], [x + s * .65, y]], fill, c, max(.8, s * .07),
                        at, op=op))
    return out


def stars_rose(cx, cy, r, at, op=None, fx=None, n=16, cols=(GOLD, RINK, GINK, BINK)):
    """A compass rose: a ring, sixteen points in alternating inks, a centre."""
    out = [circ(cx, cy, r, "rgba(250,240,220,.35)", INK, max(.8, r * .04), at, op=op, fx=fx),
           circ(cx, cy, r * .78, "none", RINK, max(.6, r * .025), at, op=op, fx=fx)]
    for k in range(n):
        a = 2 * math.pi * k / n - math.pi / 2
        L = r * (.95 if k % 4 == 0 else .7 if k % 2 == 0 else .5)
        a1, a2 = a - math.pi / n * .8, a + math.pi / n * .8
        tip = (cx + L * math.cos(a), cy + L * math.sin(a))
        b1 = (cx + r * .16 * math.cos(a1), cy + r * .16 * math.sin(a1))
        b2 = (cx + r * .16 * math.cos(a2), cy + r * .16 * math.sin(a2))
        out.append(poly([b1, tip, b2, (cx, cy)], cols[k % len(cols)], INK, max(.5, r * .015), at, op=op, fx=fx))
    out.append(circ(cx, cy, r * .09, AU, INK, max(.5, r * .02), at, op=op, fx=fx))
    return out


# ================================================================== geometry helpers
def seg_hit(p, d, a, b):
    """Ray p + t d against segment a-b: t >= 0 or None."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    den = d[0] * ey - d[1] * ex
    if abs(den) < 1e-9:
        return None
    t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
    u = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
    return t if t > 1e-6 and 0 <= u <= 1 else None


def ray_exit(p, d, poly_):
    """Where a ray from inside a polygon first leaves it."""
    best = None
    for i in range(len(poly_)):
        t = seg_hit(p, d, poly_[i], poly_[(i + 1) % len(poly_)])
        if t is not None and (best is None or t < best):
            best = t
    return None if best is None else (p[0] + best * d[0], p[1] + best * d[1])


def clip_convex(subject, clipper):
    """Sutherland-Hodgman: a polygon clipped by a convex polygon (both lists of (x, y), the clipper counter-clockwise on screen)."""
    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) <= 0
    def inter(p, q, a, b):
        x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
        x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-12:
            return q
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    out = list(subject)
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i + 1) % len(clipper)]
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b):
                    out.append(inter(s, e, a, b))
                out.append(e)
            elif inside(s, a, b):
                out.append(inter(s, e, a, b))
            s = e
    return out


class Polar:
    """Azimuthal equidistant view centred on the South Pole: Greenwich up, east to the right (as Antarctica is usually drawn)."""
    def __init__(self, cx, cy, R, lat_edge):
        self.cx, self.cy, self.R, self.k = cx, cy, R, R / (90 + lat_edge)

    def p(self, lon, lat):
        r = (90 + lat) * self.k
        a = math.radians(lon)
        return (round(self.cx + r * math.sin(a), 1), round(self.cy - r * math.cos(a), 1))

    def disc(self, n=72):
        return [(self.cx + self.R * math.cos(2 * math.pi * k / n), self.cy - self.R * math.sin(2 * math.pi * k / n)) for k in range(n)]

    def land(self, tol=1.6):
        """Land rings south of the disc's edge, clipped to the disc, as SVG path strings."""
        out, clipper = [], self.disc()
        edge = 90 - self.R / self.k   # (unused) kept for clarity
        for poly_ in F._topo():
            ring = poly_[0]
            if min(q[1] for q in ring) > -90 + self.R / self.k + 1:
                continue
            pts, last = [], None
            for lo, la in ring:
                q = self.p(lo, la)
                if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                    continue
                pts.append(q); last = q
            if len(pts) < 4:
                continue
            cl = clip_convex(pts, clipper)
            if len(cl) > 3:
                out.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in cl) + "Z")
        return out


def drawn(pts, fill, c, w, at, dur=1.0, curve=False, style="known", op=None):
    """A filled shape that appears on cue: its outline draws itself and its fill fades in behind it (the kit's draw effect alone would
    show the fill from the start)."""
    return [poly(pts, fill, "none", 0, at + dur * .4, curve=curve, op=op, dur=max(.4, dur * .8)), poly(pts, "none", c, w, at, fx="draw", dur=dur, curve=curve, style=style)]


def view_path(v, lonlats):
    return [v.p(lo, la) for lo, la in lonlats]


# ================================================================== the 1513 map (the hero): one drawing in the skin's own units
# u, v in 0..1 across the skin (portrait, about 63 x 87 cm). Coasts are schematic, after the surviving fragment: Spain and West Africa
# down the right, the Caribbean at top left (Hispaniola large and upright, a mainland coast to its west), South America down the left,
# its coast turning east along the bottom; two compass roses with their lines of bearing; ships; Saint Brendan's whale; notes.
def _skin_outline():
    """The skin's outline: a ragged top, a torn right edge (the lost two thirds), an uneven bottom, the hide's rounded corner at bottom left."""
    r = random.Random(11)
    out = []
    u = .03
    while u < .93:                                           # top edge, left to right
        out.append((round(u, 4), round(.004 + r.uniform(0, .012), 4))); u += r.uniform(.05, .09)
    v, du = .02, 0.0
    while v < .965:                                          # the torn right edge, top to bottom: a wandering line with sharp little tears
        du = max(-.022, min(.022, du + r.uniform(-.012, .012)))
        out.append((round(.958 + du, 4), round(v, 4)))
        if r.random() < .35:
            out.append((round(.958 + du - r.uniform(.012, .028), 4), round(v + r.uniform(.006, .012), 4)))
        v += r.uniform(.022, .045)
    out += [(.968, .978), (.93, .99)]
    u = .9
    while u > .2:                                            # bottom edge, right to left
        out.append((round(u, 4), round(.982 + r.uniform(0, .014), 4))); u -= r.uniform(.05, .09)
    out += [(.2, .978), (.15, .962), (.105, .938), (.068, .906), (.04, .865), (.022, .815)]   # the rounded corner of the hide
    v = .78
    while v > .04:                                           # left edge, bottom to top
        out.append((round(.004 + r.uniform(0, .012), 4), round(v, 4))); v -= r.uniform(.06, .1)
    return out


SKIN_OUT = _skin_outline()
STAINS = [(.3, .2, .16, .09), (.7, .62, .2, .12), (.18, .78, .12, .07), (.62, .1, .1, .06)]
IBERIA_AFRICA = [(.815, .0), (.79, .018), (.755, .028), (.738, .05), (.742, .078), (.736, .1), (.748, .128), (.775, .136), (.8, .142),
                 (.818, .15), (.806, .17), (.79, .19), (.772, .215), (.758, .245), (.742, .27), (.728, .3), (.716, .33), (.706, .36), (.698, .39),
                 (.684, .42), (.69, .445), (.712, .465), (.736, .485), (.762, .505), (.79, .525), (.82, .54), (.852, .552), (.884, .556),
                 (.916, .552), (.948, .556)]
MAINLAND_W = [(.075, .0), (.09, .03), (.125, .058), (.142, .085), (.128, .11), (.148, .14), (.16, .165), (.138, .19), (.108, .205),
              (.078, .225), (.045, .245), (.012, .262)]
HISPANIOLA = [(.262, .045), (.282, .05), (.29, .068), (.302, .085), (.296, .105), (.308, .125), (.3, .148), (.31, .17), (.298, .195),
              (.282, .222), (.262, .232), (.248, .215), (.238, .19), (.244, .165), (.232, .14), (.24, .112), (.236, .085), (.246, .062)]
SOUTH_AM = [(.012, .325), (.05, .338), (.09, .332), (.13, .345), (.17, .356), (.21, .352), (.25, .366), (.29, .378), (.33, .392), (.36, .405),
            (.39, .426), (.418, .448), (.44, .47), (.436, .5), (.425, .53), (.41, .56), (.392, .59), (.372, .62), (.35, .65), (.326, .68),
            (.302, .708), (.276, .735), (.25, .76), (.222, .785), (.192, .806), (.16, .826), (.128, .845), (.1, .862)]
SOUTH_COAST = [(.1, .862), (.092, .882), (.108, .9), (.15, .906), (.2, .9), (.25, .908), (.3, .902), (.36, .91), (.42, .904), (.48, .912),
               (.54, .905), (.6, .913), (.66, .906), (.72, .914), (.78, .907), (.84, .915), (.9, .909), (.955, .914)]
ISLANDS = [  # (u, v, rx, ry, ink): the Atlantic and Caribbean islands, coloured as on the chart
    (.535, .085, .012, .006, RINK), (.555, .095, .009, .005, BINK), (.575, .088, .01, .005, GINK), (.52, .1, .008, .004, RINK), (.59, .1, .007, .004, BINK),
    (.668, .19, .01, .006, RINK), (.682, .225, .008, .005, GINK), (.7, .232, .01, .005, RINK), (.716, .238, .008, .005, BINK), (.73, .228, .007, .004, GINK),
    (.6, .44, .01, .006, RINK), (.618, .452, .009, .005, GINK), (.606, .468, .008, .005, BINK), (.628, .435, .007, .004, RINK),
    (.335, .07, .016, .009, RINK), (.348, .118, .022, .01, GINK), (.37, .1, .01, .006, BINK), (.325, .2, .014, .007, BINK), (.355, .175, .009, .006, RINK),
    (.2, .262, .02, .008, GINK), (.38, .262, .012, .007, RINK), (.395, .205, .008, .005, GINK), (.43, .15, .03, .02, GINK)]
ROSES = [(.47, .235, .085), (.6, .66, .095)]
SHIPS = [(.6, .13, .05, 1), (.66, .55, .055, -1), (.33, .54, .05, 1), (.47, .8, .05, -1)]


TILT = -2.2                                                 # degrees: the skin lies a little askew in its case


def SK(x0, y0, W, H, tilt=TILT):
    """The skin's local frame: u, v -> panel units (turned by `tilt` degrees about the skin's centre)."""
    ca, sa = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    cx, cy = x0 + W / 2, y0 + H / 2
    def P(u, v):
        dx, dy = (u - .5) * W, (v - .5) * H
        return (round(cx + dx * ca - dy * sa, 1), round(cy + dx * sa + dy * ca, 1))
    return P


def piri_map(x0, y0, H, at=-1, detail=True, shadow=True, op=None, tilt=TILT):
    """The 1513 map on its gazelle skin, height H (width .724 H), top left at (x0, y0). Everything appears at `at` (-1: there from the
    first frame). Returns (elements, P) where P maps skin units to panel units."""
    W = .724 * H
    P = SK(x0, y0, W, H, tilt)
    S = H / 660.0                                          # line widths scale with the skin
    skin = [P(u, v) for u, v in SKIN_OUT]
    els = []
    if shadow:
        els += [poly([(x + 18 * S, y + 22 * S) for x, y in skin], "rgba(0,0,0,.42)", at=at, op=.42),
                poly([(x + 34 * S, y + 40 * S) for x, y in skin], "rgba(0,0,0,.2)", at=at, op=.2)]
    els += [poly(skin, "url(#k-papyrus)", "#7a5a38", 2.2 * S, at, op=op),
            poly(skin, "url(#k-speck)", "none", 0, at, op=op),
            poly(skin, "none", "rgba(110,72,36,.3)", 16 * S, at, op=op)]
    for (u, v, a, b) in STAINS:
        x, y = P(u, v)
        els.append(poly(E(x, y, a * W, b * H, 18), "rgba(120,80,40,.1)", at=at, curve=True, op=op))
    # land washes: South America (west of its coast and down to the southern land), Africa and Iberia (east of the coast), the mainland
    sa = [(0.012, .325)] + SOUTH_AM + SOUTH_COAST[1:] + [(.965, .975), (.9, .993), (.8, .985), (.68, .995), (.56, .986), (.44, .996), (.33, .988),
                                                          (.24, .982), (.165, .965), (.105, .938), (.06, .9), (.03, .855), (.014, .8), (.006, .72),
                                                          (.012, .62), (.004, .52), (.012, .42)]
    af = IBERIA_AFRICA + [(.97, .556), (.978, .5), (.982, .29), (.95, .2), (.952, .05), (.935, .012), (.88, .004)]
    mw = MAINLAND_W + [(.006, .2), (.006, .12), (.03, .02)]
    els += [poly([P(u, v) for u, v in sa], LANDT, at=at, op=op), poly([P(u, v) for u, v in af], LANDT, at=at, op=op),
            poly([P(u, v) for u, v in mw], LANDT, at=at, op=op)]
    # lines of bearing from the two roses, each to the edge of the skin (black, green and red, as on portolan charts)
    rng = random.Random(7)
    if detail:
        for (ru, rv, rr) in ROSES:
            c0 = P(ru, rv)
            for k in range(32):
                a = 2 * math.pi * k / 32
                d = (math.cos(a), math.sin(a))
                hit = ray_exit(c0, d, skin)
                if not hit:
                    continue
                col = INK if k % 4 == 0 else GINK if k % 2 == 0 else RINK
                start = (c0[0] + d[0] * rr * W * 1.02, c0[1] + d[1] * rr * W * 1.02)
                els.append(ln([start, (hit[0] - d[0] * 6 * S, hit[1] - d[1] * 6 * S)], at, col, .9 * S, draw=False, op=.42 if k % 4 == 0 else .3))
    # coasts in ink
    def coast(pts, w=2.0, c=INK, curve=True):
        return ln([P(u, v) for u, v in pts], at, c, w * S, draw=False, curve=curve, op=op)
    els += [coast(IBERIA_AFRICA), coast(MAINLAND_W), coast(SOUTH_AM), coast(SOUTH_COAST)]
    els.append(poly([P(u, v) for u, v in HISPANIOLA], "rgba(61,107,68,.45)", INK, 1.6 * S, at, curve=True, op=op))
    for (u, v, rx, ry, c) in ISLANDS:
        x, y = P(u, v)
        els.append(poly(E(x, y, rx * W, ry * H, 12), c, INK, .8 * S, at, curve=True, op=op))
    if detail:
        # names written along the coasts, perpendicular to them (tiny strokes inland), alternately black and red
        for pts, side in ((SOUTH_AM, 1), (IBERIA_AFRICA, -1), (SOUTH_COAST, 1)):
            for k in range(1, len(pts) - 1, 1):
                (ua, va), (ub, vb) = pts[k - 1], pts[k + 1]
                a, b = P(ua, va), P(ub, vb)
                dx, dy = b[0] - a[0], b[1] - a[1]
                L = math.hypot(dx, dy) or 1
                nx, ny = -dy / L * side, dx / L * side
                if pts is SOUTH_COAST:
                    nx, ny = 0, 1
                x, y = P(*pts[k])
                n = 2 if k % 2 else 3
                for j in range(n):
                    o = (j - (n - 1) / 2) * 3.2 * S
                    px, py = x + dx / L * o, y + dy / L * o
                    els.append(ln([(px + nx * 3 * S, py + ny * 3 * S), (px + nx * (11 + 4 * (j % 2)) * S, py + ny * (11 + 4 * (j % 2)) * S)], at,
                                  RINK if (k + j) % 3 == 0 else INK, .9 * S, draw=False, op=.75))
        # rivers of South America, mountains (the Andes along the west edge, hills inland), the southern land's hills
        els += [ln([P(u, v) for u, v in [(.1, .41), (.17, .4), (.24, .395), (.3, .392)]], at, BINK, 1.6 * S, curve=True, draw=False),
                ln([P(u, v) for u, v in [(.13, .58), (.2, .6), (.28, .62), (.36, .628)]], at, BINK, 1.4 * S, curve=True, draw=False),
                ln([P(u, v) for u, v in [(.12, .74), (.18, .75), (.25, .752)]], at, BINK, 1.2 * S, curve=True, draw=False)]
        els += [m for k in range(10) for m in mountains([P(.035 + .012 * ((k * 7) % 3 - 1), .38 + .045 * k + .008 * ((k * 5) % 3 - 1))], (13 + 4 * ((k * 3) % 2)) * S, at)]
        els += mountains([P(u, v) for u, v in [(.22, .44), (.27, .47), (.12, .66), (.3, .7), (.2, .8)]], 12 * S, at, op=.8)
        els += mountains([P(u, v) for u, v in [(.25, .955), (.4, .95), (.58, .958), (.72, .952)]], 11 * S, at, op=.85)
        els += mountains([P(u, v) for u, v in [(.86, .14), (.9, .3), (.88, .45), (.84, .38), (.9, .06)]], 12 * S, at, op=.8)
        # little castles in Africa and Spain (towns), red roofs
        for u, v in [(.8, .06), (.84, .21), (.8, .33), (.82, .5)]:
            x, y = P(u, v)
            els += [rect(x - 7 * S, y - 9 * S, 14 * S, 9 * S, "#efe2c4", INK, .8 * S, 0, at), poly([(x - 8 * S, y - 9 * S), (x, y - 16 * S), (x + 8 * S, y - 9 * S)], RINK, at=at)]
        # beasts: a monkey and a headless man in South America, a yale; a bonnacon and a snake on the southern land
        def beast(u, v, s, kind):
            x, y = P(u, v)
            s *= S
            if kind == "monkey":
                return [circ(x, y - 12 * s, 4 * s, INK, at=at), poly([(x - 4 * s, y - 9 * s), (x + 4 * s, y - 9 * s), (x + 3 * s, y), (x - 3 * s, y)], INK, at=at),
                        ln([(x + 3 * s, y - 2 * s), (x + 10 * s, y - 6 * s), (x + 9 * s, y - 13 * s)], at, INK, 1.2 * s, curve=True, draw=False)]
            if kind == "headless":
                return [poly([(x - 5 * s, y - 16 * s), (x + 5 * s, y - 16 * s), (x + 4 * s, y - 4 * s), (x - 4 * s, y - 4 * s)], "#8a5a3a", INK, .8 * s, at),
                        circ(x - 2 * s, y - 12 * s, 1 * s, INK, at=at), circ(x + 2 * s, y - 12 * s, 1 * s, INK, at=at),
                        ln([(x - 2 * s, y - 4 * s), (x - 3 * s, y + 2 * s)], at, INK, 1.4 * s, draw=False), ln([(x + 2 * s, y - 4 * s), (x + 3 * s, y + 2 * s)], at, INK, 1.4 * s, draw=False)]
            if kind == "quad":
                return [poly(E(x, y - 6 * s, 9 * s, 4.5 * s, 12), "#8a5a3a", INK, .8 * s, at, curve=True), circ(x + 9 * s, y - 10 * s, 3 * s, "#8a5a3a", INK, .6 * s, at),
                        ln([(x + 10 * s, y - 13 * s), (x + 13 * s, y - 18 * s)], at, INK, 1 * s, draw=False),
                        ln([(x - 6 * s, y - 3 * s), (x - 7 * s, y + 2 * s)], at, INK, 1.2 * s, draw=False), ln([(x + 6 * s, y - 3 * s), (x + 7 * s, y + 2 * s)], at, INK, 1.2 * s, draw=False)]
            if kind == "snake":
                return [ln([(x - 14 * s, y), (x - 9 * s, y - 5 * s), (x - 3 * s, y), (x + 3 * s, y - 5 * s), (x + 9 * s, y), (x + 13 * s, y - 4 * s)], at, "#5a7a3a", 2.4 * s,
                           curve=True, draw=False), circ(x + 14 * s, y - 4.5 * s, 2 * s, "#5a7a3a", at=at)]
            return []
        els += beast(.2, .5, 1.3, "monkey") + beast(.13, .56, 1.3, "headless") + beast(.24, .69, 1.3, "quad") + beast(.33, .6, 1.1, "monkey")
        els += beast(.46, .962, 1.2, "quad") + beast(.86, .955, 1.3, "snake")
        # notes: blocks of script, red headings; the colophon at centre left; the southern note beside the snake
        for (u, v, w, h, rows, red, seed) in [(.16, .515, .17, .05, 3, False, 3), (.53, .345, .14, .06, 4, True, 5), (.36, .02, .14, .04, 2, True, 8),
                                              (.71, .7, .16, .07, 4, True, 11), (.64, .925, .16, .045, 2, True, 13), (.13, .64, .1, .035, 2, False, 17),
                                              (.42, .52, .1, .04, 2, False, 19), (.05, .08, .07, .07, 3, False, 23)]:
            x, y = P(u, v)
            els += glyph_block(x, y, w * W, h * H, at, rows, INK, seed, 1.1 * S, red=red, op=.8)
        # the roses, the ships, Saint Brendan's whale (a fish with two men and a fire on its back, a ship beside it)
        for (ru, rv, rr) in ROSES:
            x, y = P(ru, rv)
            els += stars_rose(x, y, rr * W, at)
        for (u, v, s, f) in SHIPS:
            x, y = P(u, v)
            els += caravel(x, y, s * W, at, face=f)
        wx, wy = P(.585, .33)
        els += [poly(E(wx, wy, 24 * S, 7 * S, 16), "#5e6a72", INK, .9 * S, at, curve=True),
                poly([(wx + 22 * S, wy), (wx + 32 * S, wy - 7 * S), (wx + 30 * S, wy + 6 * S)], "#5e6a72", INK, .8 * S, at),
                circ(wx - 15 * S, wy - 2 * S, 1.3 * S, INK, at=at)]
        els += man(wx - 6 * S, wy - 6 * S, 12 * S, at, INK, fx=None) + man(wx + 8 * S, wy - 6 * S, 11 * S, at, INK, fx=None)
        els += [poly([(wx - 1 * S, wy - 6 * S), (wx + 1 * S, wy - 13 * S), (wx + 3 * S, wy - 6 * S)], "#e8892f", at=at)]
        els += caravel(wx - 44 * S, wy + 4 * S, 28 * S, at, face=1)
        # a scale bar (segments black and white) at top centre
        bx, by = P(.44, .075)
        els += [rect(bx + 9 * S * k, by, 9 * S, 4 * S, INK if k % 2 else "#efe2c4", INK, .6 * S, 0, at) for k in range(8)]
    return els, P


def p_on(P, pts):
    return [P(u, v) for u, v in pts]


# ================================================================== people (flat figures with a warm rim, so they read on the dark)
RIM = "rgba(255,236,206,.45)"
SKINC = "#d6b08a"


def figure(x, y, h, at, cloth="#7a5a3a", kind="robe", turban=None, face=1, arm=None, fx="rise", op=None, skin=SKINC, hair="#2a1f18"):
    """A standing person, feet on y, height h: a head, a turban (or hair), a long robe or a suit, arms (arm='point' raises the forward arm)."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    out = []
    if kind == "suit":
        out += [poly([(X(-.1), Y(.48)), (X(-.005), Y(.48)), (X(-.02), Y(0)), (X(-.09), Y(0))], cloth, RIM, 1, at, fx=fx, op=op),
                poly([(X(.005), Y(.48)), (X(.1), Y(.48)), (X(.09), Y(0)), (X(.02), Y(0))], cloth, RIM, 1, at, fx=fx, op=op),
                poly([(X(-.115), Y(.82)), (X(.115), Y(.82)), (X(.105), Y(.46)), (X(-.105), Y(.46))], cloth, RIM, 1, at, fx=fx, op=op),
                poly([(X(-.032), Y(.82)), (X(.032), Y(.82)), (X(0), Y(.7))], "#efe8dc", at=at, fx=fx, op=op),
                ln([(X(0), Y(.79)), (X(0), Y(.66))], at, "#6b2a2a", max(1.5, .014 * h), draw=False, op=op)]
    elif kind == "tunic":
        out += [poly([(X(-.1), Y(.82)), (X(.1), Y(.82)), (X(.12), Y(.4)), (X(-.12), Y(.4))], cloth, RIM, 1, at, fx=fx, op=op),
                ln([(X(-.05), Y(.42)), (X(-.06), Y(0))], at, "#3a2e26", .05 * h, draw=False, op=op), ln([(X(.05), Y(.42)), (X(.06), Y(0))], at, "#3a2e26", .05 * h, draw=False, op=op)]
    else:
        out += [poly([(X(-.1), Y(.82)), (X(.1), Y(.82)), (X(.13), Y(.55)), (X(.17), Y(.02)), (X(-.17), Y(.02)), (X(-.13), Y(.55))], cloth, RIM, 1, at, fx=fx, op=op),
                rect(min(X(-.125), X(.125)), Y(.57), .25 * h, .035 * h, "#c9a46a", at=at, fx=fx, op=op)]
    w = max(2, .05 * h)
    if arm == "point":
        out += [ln([(X(-.1), Y(.79)), (X(-.13), Y(.5))], at, cloth, w, draw=False, op=op), ln([(X(.1), Y(.79)), (X(.24), Y(.92)), (X(.33), Y(1.02))], at, cloth, w, draw=False, op=op)]
    elif arm == "fold":
        out += [ln([(X(-.1), Y(.79)), (X(-.05), Y(.6)), (X(.09), Y(.62))], at, cloth, w, draw=False, op=op)]
    else:
        out += [ln([(X(-.1), Y(.79)), (X(-.135), Y(.5))], at, cloth, w, draw=False, op=op), ln([(X(.1), Y(.79)), (X(.135), Y(.5))], at, cloth, w, draw=False, op=op)]
    out += [rect(x - .022 * h, Y(.87), .044 * h, .06 * h, skin, at=at, fx=fx, op=op),
            circ(X(.008), Y(.915), .062 * h, skin, RIM, 1, at, fx=fx, op=op)]
    if turban:
        out += [poly(E(X(.0), Y(.955), .088 * h, .052 * h, 18), turban, "rgba(0,0,0,.25)", 1, at, fx=fx, op=op, curve=True),
                circ(X(.0), Y(.99), .022 * h, "#c0392b", at=at, fx=fx, op=op)]
    else:
        out += [poly(E(X(-.004), Y(.95), .064 * h, .034 * h, 16)[8:] + [(X(.06), Y(.93)), (X(-.066), Y(.93))], hair, at=at, fx=fx, op=op)]
    return out


def bust(x, top, h, at, cloth="#3a3f4a", skin=SKINC, hair="#2a1f18", tie="#6b2a2a"):
    """Head and shoulders of a seated person behind a table whose top is at `top` (h = the standing height)."""
    return [poly([(x - .16 * h, top + 4), (x - .13 * h, top - .26 * h), (x + .13 * h, top - .26 * h), (x + .16 * h, top + 4)], cloth, RIM, 1, at, fx="rise", curve=False),
            poly([(x - .032 * h, top - .26 * h), (x + .032 * h, top - .26 * h), (x, top - .15 * h)], "#efe8dc", at=at, fx="rise"),
            ln([(x, top - .24 * h), (x, top - .1 * h)], at, tie, max(1.5, .014 * h), draw=False),
            rect(x - .022 * h, top - .32 * h, .044 * h, .07 * h, skin, at=at, fx="rise"),
            circ(x, top - .37 * h, .062 * h, skin, RIM, 1, at, fx="rise"),
            poly(E(x, top - .41 * h, .064 * h, .034 * h, 16)[8:] + [(x + .064 * h, top - .39 * h), (x - .064 * h, top - .39 * h)], hair, at=at, fx="rise")]


def sitter(x, y, h, at, cloth="#7a5a3a", face=1, turban=None, skin=SKINC, hair="#2a1f18", reach=True, stool=True):
    """A person seated in profile on a stool, facing `face`, feet on y; the forward arm reaches to a table if reach."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    out = []
    if stool:
        out.append(rect(min(X(-.14), X(.06)), Y(.27), .2 * h, .27 * h, "#3a2c20", "#8a6a48", 1.5, 3, at, fx="rise"))
    out += [poly([(X(-.12), Y(.27)), (X(.2), Y(.29)), (X(.22), Y(.22)), (X(-.12), Y(.2))], cloth, RIM, 1, at, fx="rise"),
            poly([(X(.15), Y(.27)), (X(.22), Y(.27)), (X(.21), Y(0)), (X(.15), Y(0))], cloth, RIM, 1, at, fx="rise"),
            poly([(X(-.1), Y(.27)), (X(.06), Y(.27)), (X(.1), Y(.62)), (X(-.06), Y(.66))], cloth, RIM, 1, at, fx="rise"),
            rect(min(X(.02), X(.06)), Y(.7), .04 * h, .06 * h, skin, at=at, fx="rise"),
            circ(X(.06), Y(.75), .062 * h, skin, RIM, 1, at, fx="rise")]
    if reach:
        out += [ln([(X(.06), Y(.6)), (X(.22), Y(.5)), (X(.36), Y(.47))], at, cloth, max(2, .05 * h), draw=False)]
    if turban:
        out += [poly(E(X(.055), Y(.795), .088 * h, .05 * h, 18), turban, "rgba(0,0,0,.25)", 1, at, fx="rise", curve=True)]
    else:
        out += [poly(E(X(.055), Y(.79), .064 * h, .034 * h, 16)[8:] + [(X(.12), Y(.77)), (X(-.01), Y(.77))], hair, at=at, fx="rise")]
    return out


# ================================================================== the hero placement (s1 and its returns s2, s19, s32, s37, s51)
HX, HY, HH = 850, 116, 690
HW = .724 * HH


def hero_P():
    return SK(HX, HY, HW, HH)


def coast_glow(pts, at, c, w=5, dur=2.0, style="known", op=.95):
    P = hero_P()
    return ln([P(u, v) for u, v in pts], at, c, w, style, dur=dur, curve=True, op=op)


def leader(x0, y0, x1, y1, at, c=DIM):
    return ln([(x0, y0), (x1, y1)], at, c, 1.6, dur=.5, op=.8)


# ================================================================== COLD OPEN
def s1():
    """The hero: the surviving third of the 1513 map, upright in a dark case under a lamp. Its South American coast traces in gold,
    then the southern coast in lilac (the claim's colour)."""
    tsk, t13, tsa, tbt = T("s1", "gazelle skin"), T("s1", "fifteen thirteen"), T("s1", "Down its left side"), T("s1", "along the bottom")
    P = hero_P()
    els = [gl(HX + HW * .5, HY + HH * .48, 860, -1, .3, "lamp"), gl(HX + HW * .3, HY + HH * .2, 420, -1, .16, "lamp")]
    mp, _ = piri_map(HX, HY, HH)
    els += mp
    els += [ln([(HX + 40, HY - 10), (HX + HW * .62, HY + HH + 20)], -1, "#fff6e8", 46, draw=False, op=.035),
            ln([(HX + HW * .62, HY - 10), (HX + HW * 1.05, HY + HH * .62)], -1, "#fff6e8", 18, draw=False, op=.03)]
    # labels at the left of the skin, each with a leader to what it names
    lx = HX - 46
    ex, ey = P(.012, .5)
    els += [lab(lx - 14, ey + 10, "gazelle skin", tsk, BONE, 32, "end", st="ital"), leader(lx, ey, ex - 6, ey, tsk)]
    els += chip(lx - 62, ey + 74, "1513", GOLD, t13, 30)
    sx, sy = P(.012, .325)
    els += [coast_glow(SOUTH_AM, tsa, GOLD, 4.5, 2.6), lab(lx - 14, sy + 10, "South America", tsa + .3, GOLD, 32, "end", st="ital"),
            leader(lx, sy, sx - 6, sy, tsa + .3, GOLD)]
    bx, by = P(.1, .87)
    els += [coast_glow(SOUTH_COAST, tbt, LILAC, 5.5, 1.8), gl(*P(.5, .905), 360, tbt + .6, .28, "lamp"),
            lab(lx - 14, by + 10, "the southern coast", tbt + .5, LILAC, 32, "end", st="ital"), leader(lx, by, bx - 10, by, tbt + .5, LILAC)]
    return {"base": "dark", "cam": CAM, "els": els}


def antarctica_rings(pol, minpts=12, tol=2.2, south=-60):
    """Antarctica's coast (and its biggest islands) as point lists in a polar view."""
    out = []
    for poly_ in F._topo():
        ring = poly_[0]
        if max(q[1] for q in ring) > south:
            continue
        pts, last = [], None
        for lo, la in ring:
            q = pol.p(lo, la)
            if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                continue
            pts.append(q); last = q
        if len(pts) >= minpts:
            out.append(pts)
    out.sort(key=len, reverse=True)
    return out


def qml_coast(pol, lo0=-20, lo1=45, tol=1.5):
    """The coast of Queen Maud Land (20 W to 45 E) on the main Antarctic ring, as one run of points."""
    ring = max((p[0] for p in F._topo() if max(q[1] for q in p[0]) < -60), key=len)
    runs, cur = [], []
    for lo, la in ring:
        if lo0 <= lo <= lo1 and la > -74:
            cur.append(pol.p(lo, la))
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    best = max(runs, key=len)
    out, last = [], None
    for q in best:
        if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
            continue
        out.append(q); last = q
    return out


def s2_add():
    """Some say it is Antarctica: a ghost of Antarctica, seen from above the South Pole, draws itself in lilac dots at the left."""
    ta, tp, ti = T("s2", "Antarctica"), T("s2", "South Pole"), T("s2", "before the ice")
    pol = Polar(430, 455, 250, -58)
    rings = antarctica_rings(pol)
    els = [gl(430, 455, 330, ta - .2, .14, "lamp")]
    els += drawn(rings[0], "rgba(201,193,238,.07)", LILAC, 2.6, ta, 1.8, style="claimed")
    els += [poly(r, "rgba(201,193,238,.05)", LILAC, 1.6, ta + .6, style="claimed") for r in rings[1:6]]
    els += [dot(430, 455, 6, LILAC, tp), lab(430, 492, "South Pole", tp + .1, LILAC, 24, st="small")]
    P = hero_P()
    sx, sy = P(.3, .92)
    els += [arr([(sx, sy + 8), (760, 820), (560, 760)], ta + .8, LILAC, 3, "claimed", 1.2)]
    els += [lab(430, 184, "Antarctica?", ta + .4, LILAC, 44, st="serif"), lab(430, 740, "before the ice?", ti, LILAC, 32, st="ital")]
    return els


def XT3(yr):
    return round(200 + (yr - 1500) / 350 * 1380, 1)


def s3():
    """A timeline from 1500 to 1850: the map in 1513, the first sighting of Antarctica in 1820, about 300 years between, a question."""
    tn, t3, ty = T("s3", "nobody would see"), T("s3", "three hundred"), T("s3", "years")
    y = 560
    els = [gl(889, 470, 640, -1, .16, "lamp"), axis(200, 1580, y, [(XT3(v), str(v)) for v in (1500, 1600, 1700, 1800)], -1, "years CE")]
    x1, x2 = XT3(1513), XT3(1820)
    mp, _ = piri_map(x1 - 34, y - 190, 96, at=.4, detail=False, shadow=False)
    els += [dot(x1, y, 11, GOLD, .3)] + mp + [lab(x1 + 46, y - 120, "1513, the map", .7, GOLD, 30, "start")]
    els += [dot(x2, y, 11, ICE, tn)] + caravel(x2, y - 70, 90, tn, ICE_D, ICE, fx="pop") + [lab(x2, y - 186, "1820, first seen", tn + .2, ICE, 30)]
    els += bracket(x1, x2, y + 50, t3, "about 300 years", BONE, up=False, size=30, ty=y + 100)
    els += qmark((x1 + x2) / 2, y - 210, ty + .3, 120)
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


# ================================================================== CHAPTER 1 · The admiral and his book
def s5():
    """Gallipoli on the Dardanelles: the Ottoman navy's great base; Piri born there around 1470, probably."""
    v = View(22.0, 31.0, 37.4, 42.4, (90, 120, 1600, 680))
    tg, td, tb = T("s5", "Gallipoli"), T("s5", "Dardanelles"), T("s5", "born around")
    gx, gy = v.p(26.67, 40.41)
    ix, iy = v.p(28.98, 41.01)
    strait = [v.p(lo, la) for lo, la in [(26.15, 40.03), (26.3, 40.1), (26.4, 40.2), (26.52, 40.31), (26.67, 40.41), (26.85, 40.5)]]
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(24.6, 38.6), "Aegean Sea", .6, "#9fd0ff", 34, st="ital"),
           ln(strait, td, GOLD, 10, dur=1.0, curve=True, op=.75), gl(*v.p(26.4, 40.2), 110, td, .45, "lamp"),
           lab(v.p(26.35, 40.15)[0] - 30, v.p(26.35, 40.15)[1] + 40, "Dardanelles", td + .3, GOLD, 30, "end"),
           {"k": "pin", "x": gx, "y": gy, "t": "Gallipoli", "c": GOLD, "in": tg, "a": "end", "lx": -22, "ly": -22},
           dot(ix, iy, 8, DIM, .9), lab(ix + 14, iy - 14, "Istanbul", .9, DIM, 28, "start")]
    els += kadirga(*v.p(27.35, 40.62), 120, tg + .4, "#efe2c4", "#cbbca8", 1, cabin=False)
    els += chip(1420, 700, "born about 1470", GOLD, tb, 30)
    els += [{"k": "scale", "x": 160, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def s6():
    """Dusk at sea: a galley under its lateen sail; on the stern, the uncle, Kemal Reis, and young Piri, in kaftans and turbans."""
    tu, tk, t81 = T("s6", "his uncle"), T("s6", "Kemal Reis"), T("s6", "fourteen eighty-one")
    els = [{"k": "water", "y": 600, "h": 500, "op": .92, "in": -1}, gl(1450, 520, 260, -1, .35, "fire")]
    els += kadirga(860, 640, 820, -1, "#241910", "#e3cfa8", 1, cabin=False)
    deck = 640 - .02 * 820
    els += figure(500, deck, 178, tu, "#6b2f24", turban="#efe2c4") + figure(578, deck, 140, tu + .5, "#2f4a5a", turban="#efe2c4")
    els += [lab(470, 450, "Kemal Reis", tk, BONE, 32, "end"), lab(612, 476, "young Piri", tk + .6, BONE, 32, "start")]
    els += chip(1380, 230, "from about 1481", GOLD, t81, 30)
    return {"base": "sky", "tod": "dusk", "ground": 1300, "sun": [1450, 520, 30], "cam": CAM, "els": els}


VM = View(-10.0, 36.5, 30.0, 46.8, (90, 120, 1600, 680))


def storm(x, y, s, at):
    """A dark storm cloud with slanting rain."""
    out = [poly(E(x, y, s * .9, s * .32, 18), "#2b2f36", "rgba(200,210,220,.4)", 1.5, at, curve=True, fx="pop"),
           poly(E(x - s * .45, y + s * .05, s * .5, s * .26, 14), "#353a42", "none", 0, at, curve=True, fx="pop"),
           poly(E(x + s * .5, y + s * .04, s * .48, s * .25, 14), "#30353c", "none", 0, at, curve=True, fx="pop")]
    out += [ln([(x - s * .6 + s * .2 * k, y + s * .3), (x - s * .7 + s * .2 * k, y + s * .7)], at + .2 + .04 * k, "#9fc8e0", 2, dur=.3) for k in range(7)]
    return out


def swords(x, y, s, at, c=BONE):
    return [ln([(x - s, y - s), (x + s, y + s)], at, c, 4, dur=.3), ln([(x + s, y - s), (x - s, y + s)], at + .15, c, 4, dur=.3),
            ln([(x - s * .7, y - s * .35), (x - s * .35, y - s * .7)], at + .3, c, 3, draw=False), ln([(x + s * .7, y - s * .35), (x + s * .35, y - s * .7)], at + .3, c, 3, draw=False)]


def s7():
    """The uncle's wars: the Venetian fleets (Zonchio, 1499), the coasts of Spain (1501), and the storm of 1511 in the Aegean."""
    v = VM
    tv, ts, tst = T("s7", "Venetian fleets"), T("s7", "coasts of Spain"), T("s7", "storm")
    gx, gy = v.p(26.67, 40.41)
    zx, zy = v.p(21.67, 36.95)
    sx, sy = v.p(-0.4, 38.6)
    mx, my = v.p(26.8, 37.7)
    els = [{"k": "map", "land": v.land(), "in": -1}, dot(gx, gy, 9, GOLD, -1), lab(gx + 14, gy - 14, "Gallipoli", .4, GOLD, 26, "start"),
           lab(*v.p(15.5, 34.2), "Mediterranean Sea", .6, "#9fd0ff", 30, st="ital")]
    els += [arr([(gx - 8, gy + 6), v.p(24.0, 38.9), (zx + 12, zy - 8)], tv - .3, AMBER, 3, "inferred", 1.0)] + swords(zx, zy, 15, tv + .5)
    els += [lab(zx - 26, zy + 52, "Venetian fleets, 1499", tv + .7, BONE, 28, "end")]
    els += [arr([(zx - 14, zy), v.p(15.0, 37.0), v.p(6.0, 37.8), (sx + 18, sy)], ts - .3, AMBER, 3, "inferred", 1.2)]
    els += [poly([(sx, sy + 4), (sx - 9, sy - 10), (sx - 4, sy - 20), (sx + 1, sy - 12), (sx + 5, sy - 26), (sx + 11, sy - 10)], "#ff7a4a", "#ffd08a", 1.5, ts + .9, curve=True, fx="pop"),
            gl(sx, sy - 10, 50, ts + .9, .6, "fire"), lab(sx - 20, sy - 40, "coasts of Spain, 1501", ts + 1.0, BONE, 28, "middle")]
    els += storm(mx, my - 34, 58, tst) + kadirga(mx, my + 10, 56, tst + .3, "#2a1d14", "#cbbca8", 1, op=.6)
    rx, ry = v.p(28.6, 35.4)
    els += [lab(rx, ry, "1511: a storm", tst + .5, RED, 28, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def open_book(cx, top, pw, ph, at, page=PARCH_L, fx=None):
    """An open book seen from above: two pages with a slight curl and a dark spine; returns (elements, left page box, right page box)."""
    L = [(cx - pw - 6, top + 14), (cx - pw * .5, top), (cx - 4, top + 10), (cx - 4, top + ph + 10), (cx - pw * .5, top + ph), (cx - pw - 6, top + ph + 14)]
    Rr = [(cx + 4, top + 10), (cx + pw * .5, top), (cx + pw + 6, top + 14), (cx + pw + 6, top + ph + 14), (cx + pw * .5, top + ph), (cx + 4, top + ph + 10)]
    els = [poly([(x + 14, y + 18) for x, y in L + Rr], "rgba(0,0,0,.45)", at=at, op=.45),
           poly([(cx - pw - 16, top + 22), (cx + pw + 16, top + 22), (cx + pw + 16, top + ph + 30), (cx - pw - 16, top + ph + 30)], "#5a3a22", "#2a1a10", 2, at, fx=fx),
           poly(L, page, "#8a6a48", 1.4, at, fx=fx, curve=False), poly(Rr, page, "#8a6a48", 1.4, at, fx=fx),
           poly(L, "url(#k-speck)", at=at), poly(Rr, "url(#k-speck)", at=at),
           ln([(cx, top + 8), (cx, top + ph + 12)], at, "#3a281a", 3, draw=False)]
    return els, (cx - pw + 20, top + 30, pw - 50, ph - 60), (cx + 30, top + 30, pw - 50, ph - 60)


def s8():
    """The Book of the Sea, open by lamplight: script on the left page, a coastal chart with its signs on the right."""
    tk, tb = T("s8", "Kitab i"), T("s8", "the Book of the Sea")
    els = [gl(889, 380, 700, -1, .28, "lamp")]
    bk, lp, rp = open_book(889, 150, 470, 470, -1)
    els += bk
    x, y, w, h = lp
    els += [ln([(x + 10, y + 20), (x + w * .6, y + 20)], .3, RINK, 5, dur=.6)] + glyph_block(x + 10, y + 50, w - 20, h - 70, .5, 11, INK, 4, 2.2)
    x, y, w, h = rp
    coast = [(x + w * .62, y), (x + w * .58, y + h * .12), (x + w * .66, y + h * .25), (x + w * .52, y + h * .38), (x + w * .47, y + h * .55),
             (x + w * .58, y + h * .7), (x + w * .5, y + h * .85), (x + w * .56, y + h)]
    els += [poly(coast + [(x + w, y + h), (x + w, y)], LANDT, at=.5), ln(coast, .5, INK, 3, dur=1.2, curve=True)]
    els += stars_rose(x + w * .24, y + h * .3, 46, .9)
    els += [circ(x + w * .4 + 9 * (k % 4), y + h * .52 + 9 * (k // 4), 2.2, INK, at=1.3 + .02 * k) for k in range(12)]
    for k in range(4):
        cx_, cy_ = x + w * .36 + 22 * k, y + h * .78 + 10 * (k % 2)
        els += [ln([(cx_ - 6, cy_ - 6), (cx_ + 6, cy_ + 6)], 1.5 + .05 * k, RINK, 2.2, draw=False), ln([(cx_ + 6, cy_ - 6), (cx_ - 6, cy_ + 6)], 1.5 + .05 * k, RINK, 2.2, draw=False)]
    tx, ty = x + w * .78, y + h * .46
    els += [rect(tx - 12, ty - 14, 24, 14, "#efe2c4", INK, 1.2, 0, 1.1), poly([(tx - 14, ty - 14), (tx, ty - 28), (tx + 14, ty - 14)], RINK, at=1.1)]
    els += [ln([(1430, 600), (1600, 420)], .2, "#c9a46a", 5, draw=False), ln([(1430, 600), (1418, 616)], .2, INK, 4, draw=False)]
    els += [lab(889, 700, "Kitab-ı Bahriye", tk, GOLD, 46, st="serif"), lab(889, 760, "Book of the Sea", tb, BONE, 34, st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


ROUTE = [(26.3, 40.05), (25.4, 39.4), (24.3, 38.6), (23.5, 37.6), (22.9, 36.6), (22.2, 36.5), (21.4, 37.4), (20.9, 38.6), (19.8, 39.8), (19.2, 41.2),
         (18.2, 42.4), (16.4, 43.4), (14.6, 44.8), (13.4, 45.4), (12.6, 44.6), (13.4, 43.6), (14.8, 42.4), (16.6, 41.5), (18.3, 40.3), (17.6, 39.9),
         (16.8, 39.3), (16.3, 38.4), (15.5, 38.0), (15.4, 39.4), (14.6, 40.4), (13.4, 41.2), (12.0, 41.8), (10.8, 42.8), (10.0, 43.9), (8.6, 44.2),
         (6.6, 43.0), (4.6, 43.2), (3.2, 42.8), (2.6, 41.6), (1.0, 40.9), (0.2, 39.8), (-0.3, 38.6), (-1.2, 37.4), (-2.6, 36.6), (-4.6, 36.3),
         (-5.4, 36.0), (-4.2, 35.4), (-2.0, 35.3), (0.6, 36.1), (3.2, 36.9), (6.6, 37.2), (9.4, 37.4), (10.6, 37.0), (11.0, 36.0), (10.4, 34.6),
         (11.6, 33.4), (13.6, 32.9), (15.6, 32.0), (17.8, 31.0), (19.8, 31.3), (20.2, 32.3), (21.8, 33.0), (24.0, 32.2), (26.0, 31.7), (28.6, 31.1),
         (30.4, 31.6), (32.4, 31.4), (34.2, 31.8), (34.8, 33.0), (35.6, 34.6), (35.8, 36.0), (34.6, 36.5), (32.6, 36.2), (30.4, 36.4), (28.6, 36.6),
         (27.4, 37.2), (26.9, 38.2), (26.4, 39.1), (26.2, 39.8)]


def s9():
    """The book's tour: from the Dardanelles all the way round the Mediterranean, counter-clockwise, a chart for each stretch."""
    v = VM
    tsf, tar, tch = T("s9", "It sets off"), T("s9", "all the way round"), T("s9", "a chart for each")
    pts = [v.p(lo, la) for lo, la in ROUTE]
    dx, dy = v.p(26.4, 40.2)
    dur = 5.2
    els = [{"k": "map", "land": v.land(), "in": -1}, {"k": "pin", "x": dx, "y": dy, "t": "start", "c": GOLD, "in": tsf, "lx": 18, "ly": -16}]
    els += [ln(pts, tsf + .3, AMBER, 4, dur=dur, curve=True, op=.95)]
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    tot = L[-1]
    for k in range(0, len(pts), 4):
        x, y = pts[k]
        t = tsf + .3 + dur * (L[k] / tot)
        els += [rect(x - 13, y - 10, 26, 20, PARCH_L, "#8a6a48", 1.2, 2, max(t, tch - .6) if k > 0 else t, fx="pop")]
    els += [lab(*v.p(18.0, 34.2), "all the way round", tar, AMBER, 34, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def s10():
    """One chart, large: a harbour with a moored ship, a spring of fresh water, dots for shallows, crosses for hidden rocks."""
    th, tw, tsh, trk = T("s10", "harbours"), T("s10", "fresh water"), T("s10", "dots for shallows"), T("s10", "crosses for hidden rocks")
    x0, y0, w, h = 250, 140, 1280, 620
    sheet = [(x0, y0 + 8), (x0 + w * .3, y0), (x0 + w * .7, y0 + 6), (x0 + w, y0), (x0 + w - 6, y0 + h), (x0 + w * .6, y0 + h - 6), (x0 + w * .25, y0 + h), (x0 + 6, y0 + h - 4)]
    els = [gl(889, 450, 800, -1, .22, "lamp"), poly([(x + 16, y + 20) for x, y in sheet], "rgba(0,0,0,.4)", at=-1, op=.4),
           poly(sheet, "url(#k-papyrus)", "#7a5a38", 2, -1), poly(sheet, "url(#k-speck)", at=-1)]
    coast = [(x0 + w * .52, y0), (x0 + w * .5, y0 + h * .18), (x0 + w * .58, y0 + h * .3), (x0 + w * .74, y0 + h * .34), (x0 + w * .78, y0 + h * .48),
             (x0 + w * .64, y0 + h * .56), (x0 + w * .55, y0 + h * .7), (x0 + w * .6, y0 + h * .86), (x0 + w * .66, y0 + h)]
    land = coast + [(x0 + w, y0 + h), (x0 + w, y0)]
    els += [poly(land, LANDT, at=-1), ln(coast, -1, INK, 3.4, curve=True, draw=False)]
    for k in range(9):
        a = math.radians(-100 + 25 * k)
        els.append(ln([(x0 + w * .22, y0 + h * .55), (x0 + w * .22 + 900 * math.cos(a), y0 + h * .55 + 900 * math.sin(a))], -1, GINK if k % 2 else RINK, 1, draw=False, op=.25))
    els += stars_rose(x0 + w * .22, y0 + h * .55, 70, -1)
    hx, hy = x0 + w * .66, y0 + h * .36
    els += caravel(hx - 30, hy + 18, 70, th, fx="pop") + [lab(hx - 40, hy + 92, "harbour", th + .3, BONE, 32, "end")]
    ax_, ay_ = hx + 30, hy + 10
    els += [circ(ax_, ay_ - 16, 5, "none", INK, 2.4, th + .2), ln([(ax_, ay_ - 11), (ax_, ay_ + 12)], th + .2, INK, 2.4, draw=False),
            ln([(ax_ - 10, ay_ + 4), (ax_ - 6, ay_ + 12), (ax_, ay_ + 14), (ax_ + 6, ay_ + 12), (ax_ + 10, ay_ + 4)], th + .2, INK, 2.4, curve=True, draw=False)]
    wx, wy = x0 + w * .86, y0 + h * .2
    els += [circ(wx, wy, 16, "#7fb6d6", BINK, 2, tw, fx="pop")] + [ln([(wx - 30 + 14 * k, wy + 28), (wx - 24 + 14 * k, wy + 22), (wx - 18 + 14 * k, wy + 28)], tw + .1, BINK, 2, draw=False) for k in range(5)]
    els += [lab(wx, wy - 34, "fresh water", tw + .2, BONE, 32)]
    sx, sy = x0 + w * .43, y0 + h * .64
    els += [circ(sx + 15 * (k % 6) - 10 * (k // 6), sy + 13 * (k // 6), 3.2, INK, at=tsh + .03 * k, fx="pop") for k in range(24)]
    els += [lab(sx + 30, sy - 26, "shallows", tsh + .3, BONE, 32)]
    rx, ry = x0 + w * .5, y0 + h * .86
    for k in range(5):
        cx_, cy_ = rx - 70 + 32 * k, ry + 10 * (k % 2)
        els += [ln([(cx_ - 9, cy_ - 9), (cx_ + 9, cy_ + 9)], trk + .08 * k, RINK, 3.4, dur=.2), ln([(cx_ + 9, cy_ - 9), (cx_ - 9, cy_ + 9)], trk + .08 * k + .1, RINK, 3.4, dur=.2)]
    els += [lab(rx - 100, ry + 12, "hidden rocks", trk + .4, BONE, 32, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def spine(x, base, w, h, at, c, fx="pop"):
    return [rect(x, base - h, w, h, c, "rgba(255,226,190,.35)", 1, 2, at, fx=fx), rect(x + 2, base - h * .78, w - 4, 4, AU, at=at, fx=fx, op=.7),
            rect(x + 2, base - h * .3, w - 4, 3, AU, at=at, fx=fx, op=.5)]


def s11():
    """The numbers: the 1526 version with 210 charts; more than forty copies survive (spines fill a shelf); over 5,700 maps among them."""
    t26, t40, t57 = T("s11", "fifteen twenty-six"), T("s11", "More than forty copies"), T("s11", "five thousand seven hundred")
    els = [gl(889, 420, 760, -1, .22, "lamp")]
    # the big book of 1526, lying open at left
    bk, lp, rp = open_book(330, 300, 170, 230, -1)
    els += bk + glyph_block(lp[0], lp[1], lp[2], lp[3] * .8, -1, 6, INK, 31, 1.6) + [ln([(rp[0] + 10, rp[1] + 30), (rp[0] + 60, rp[1] + 80), (rp[0] + 40, rp[1] + 140), (rp[0] + 90, rp[1] + 190)], -1, INK, 2.4, curve=True, draw=False)]
    els += chip(330, 640, "1526: 210 charts", GOLD, t26, 30)
    # a shelf of copies
    base = 560
    els += [rect(640, base, 980, 16, WOOD, "#8a6a48", 1.5, 2, -1), rect(640, base - 250, 980, 10, WOOD_D, "none", 0, 2, -1, op=.6)]
    rr = random.Random(5)
    x = 652
    cols = ["#6b3a2a", "#3e4a32", "#5a4630", "#2f3d4a", "#6a5232", "#4a2f2a"]
    for k in range(44):
        w = rr.uniform(15, 21); h = rr.uniform(150, 210)
        els += spine(round(x, 1), base, round(w, 1), round(h, 1), t40 + .035 * k, cols[k % len(cols)])
        x += w + 1.2
    els += [lab(1130, 620, "40+ copies", t40 + 1.0, BONE, 34)]
    # 5,700 maps: 57 tiles of 100 maps each, above the shelf
    for k in range(57):
        gx, gy = 700 + 30 * (k % 29), 190 + 34 * (k // 29)
        els.append(rect(gx, gy, 24, 26, PARCH_L, "#8a6a48", 1, 2, t57 + .018 * k, fx="pop"))
    els += [lab(1130, 290, "5,700+ maps", t57 + 1.1, GOLD, 40, st="serif"), lab(1130, 172, "1 tile: 100 maps", t57 + .2, DIM, 24, st="small")]
    return {"base": "dark", "cam": CAM, "els": els}


def s12():
    """At around eighty, still at sea: the Ottoman fleet from Suez down the Red Sea to Aden, Muscat and Hormuz (1547 to 1552)."""
    v = View(30.0, 62.0, 10.0, 32.0, (90, 120, 1600, 680))
    ta, ti, to = T("s12", "admiral"), T("s12", "Indian Ocean"), T("s12", "around eighty")
    route = [(32.55, 29.6), (33.6, 27.9), (35.2, 25.6), (37.4, 22.0), (39.6, 18.4), (41.6, 15.4), (43.4, 12.7), (45.03, 12.6), (48.0, 13.6), (51.0, 15.0),
             (54.4, 16.6), (57.0, 18.6), (58.9, 21.4), (59.2, 23.0), (58.6, 23.7), (57.4, 25.2), (56.5, 26.6)]
    pts = [v.p(*q) for q in route]
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(53.0, 13.4), "Indian Ocean", ti, "#9fd0ff", 32, st="ital")]
    els += [ln(pts, ta - .2, AMBER, 3, "inferred", dur=3.2, curve=True)]
    for name, lo, la, at, a in (("Suez", 32.55, 29.97, .5, "end"), ("Aden", 45.03, 12.8, ta + 1.4, "end"), ("Hormuz", 56.46, 27.1, ta + 2.6, "end")):
        x, y = v.p(lo, la)
        els += [dot(x, y, 8, BONE, at), lab(x + (-14 if a == "end" else 14), y - 12, name, at + .1, BONE, 28, a)]
    for k, f in enumerate((.12, .3, .5, .7, .88)):
        x, y = pts[int(f * (len(pts) - 1))]
        els += kadirga(x, y, 40, ta + .5 * k, "#e8d6b8", "#cbbca8", 1, oars=False)
    fx_, fy_ = v.p(36.6, 23.4)
    els += kadirga(fx_ + 60, fy_ + 6, 120, to - .4, "#e8d6b8", GOLD, 1) + [lab(fx_ + 120, fy_ + 52, "Piri Reis, around 80", to, GOLD, 30, "start")]
    els += chip(330, 250, "1547 to 1552", GOLD, ta, 30)
    return {"base": "map", "cam": CAM, "els": els}


def s13():
    """Gallipoli, 1513: Piri seated at a slanted desk under a lamp, a skin lying on it; about twenty charts pinned in a fan on the wall,
    threads running from them to the skin."""
    t13, tw = T("s13", "fifteen eleven"), T("s13", "the whole world")
    els = [gl(1000, 470, 520, -1, .22, "lamp")]
    desk = [(650, 560), (1120, 528), (1170, 572), (700, 610)]
    els += [poly(desk, WOOD, "#8a6a48", 2, -1), poly([(700, 610), (1170, 572), (1170, 584), (700, 622)], WOOD_D, at=-1),
            ln([(720, 618), (720, 770)], -1, WOOD_D, 9, draw=False), ln([(1150, 582), (1150, 770)], -1, WOOD_D, 9, draw=False)]
    els += sitter(560, 770, 340, -1, "#6b2f24", 1, turban="#efe2c4")
    els += skin_flat(905, 566, 300, 300, t13 - .3)
    els += [gl(1170, 500, 240, -1, .75, "fire"), poly([(1160, 498), (1172, 470), (1184, 498)], "#ffd08a", at=-1), rect(1150, 498, 44, 30, "#5a4630", "#8a6a48", 1, 3, -1)]
    for k in range(20):
        a = math.pi * (.1 + .8 * k / 19)
        x, y = 1080 - 430 * math.cos(a), 430 - 270 * math.sin(a)
        col = k == 0
        els += [rect(x - 26, y - 19, 52, 38, "none" if col else PARCH_L, LILAC if col else "#8a6a48", 1.4, 3, .4 + .06 * k, fx="pop", style="claimed" if col else "known"),
                ln([(x - 14, y + 4), (x + 6, y - 8), (x + 14, y + 6)], .45 + .06 * k, LILAC if col else INK, 1.4, draw=False, op=.8),
                ln([(x, y + 19), (905, 560)], tw - .8 + .03 * k, GOLD, 1.2, "inferred", .8, op=.4)]
    els += chip(330, 240, "begun about 1511", GOLD, t13, 30)
    return {"base": "dark", "floor": 770, "cam": CAM, "els": els}


def hero_panel(cam, els_add=(), south=True):
    """A fresh copy of the hero (the same skin, light and glass as s1) on its own panel, so a return to the map carries only its own
    marks; the southern coast stays in lilac (the claim's colour) when south."""
    els = [gl(HX + HW * .5, HY + HH * .48, 860, -1, .3, "lamp"), gl(HX + HW * .3, HY + HH * .2, 420, -1, .16, "lamp")]
    mp, _ = piri_map(HX, HY, HH)
    els += mp
    els += [ln([(HX + 40, HY - 10), (HX + HW * .62, HY + HH + 20)], -1, "#fff6e8", 46, draw=False, op=.035),
            ln([(HX + HW * .62, HY - 10), (HX + HW * 1.05, HY + HH * .62)], -1, "#fff6e8", 18, draw=False, op=.03)]
    if south:
        P = hero_P()
        els.append(ln([P(u, v) for u, v in SOUTH_COAST], -1, LILAC, 5.5, curve=True, draw=False, op=.9))
    return {"base": "dark", "cam": list(cam), "els": els + list(els_add)}


def skin_flat(cx, cy, W, H, at, sk=.38, shear=.22):
    """The skin lying flat on a desk, seen from above at a slant: its outline and its main coasts, foreshortened."""
    def Q(u, v):
        return (round(cx + (u - .5) * W + (v - .5) * H * shear, 1), round(cy + (v - .5) * H * sk, 1))
    els = [poly([Q(u, v) for u, v in SKIN_OUT], "url(#k-papyrus)", "#7a5a38", 1.4, at), poly([Q(u, v) for u, v in SKIN_OUT], "url(#k-speck)", at=at)]
    for pts in (IBERIA_AFRICA, SOUTH_AM, SOUTH_COAST, MAINLAND_W):
        els.append(ln([Q(u, v) for u, v in pts], at, INK, 1.4, curve=True, draw=False))
    els.append(poly([Q(u, v) for u, v in HISPANIOLA], "rgba(61,107,68,.5)", INK, 1, at, curve=True))
    return els


def s19():
    """Back on the map, close on the ocean: Saint Brendan's whale, the fire on its back glowing; its name."""
    tw, ti = T("s19", "whale"), T("s19", "island")
    P = hero_P()
    wx, wy = P(.585, .33)
    add = [gl(wx, wy - 4, 70, tw - .3, .8, "fire", pulse=True), gl(wx, wy, 150, tw, .25, "lamp"), lab(wx, wy + 74, "Saint Brendan's whale", ti, GOLD, 30, st="ital")]
    return hero_panel([2.0, 1140, 372], add, south=False)


def s32():
    """Back on the map, close on its bottom left corner: the coast runs on from South America round the corner and along the bottom,
    no gap."""
    tr = T("s32", "runs straight on")
    P = hero_P()
    tail = SOUTH_AM[-9:] + SOUTH_COAST[1:9]
    cx, cy = P(.1, .88)
    add = [ln([P(u, v) for u, v in tail], tr, GOLD, 7, dur=2.0, curve=True), gl(*P(.12, .87), 170, tr + 1.0, .5, "lamp"),
           lab(cx - 70, cy - 70, "no gap", tr + 1.2, GOLD, 36, "end", st="serif"), ln([(cx - 60, cy - 66), (cx - 8, cy - 14)], tr + 1.2, GOLD, 2, dur=.4)]
    return hero_panel([1.8, 1000, 620], add)


def s37():
    """Back on the map, close on its bottom right: the snake and Piri's red note glow; beside the skin, three words: barren,
    great snakes, very hot."""
    tn, tb, ts, th = T("s37", "own note"), T("s37", "barren"), T("s37", "great snakes"), T("s37", "very hot")
    P = hero_P()
    sx, sy = P(.86, .955)
    nx, ny = P(.64, .925)
    add = [rect(nx - 10, ny - 12, .16 * HW + 20, .045 * HH + 24, "rgba(242,201,142,.15)", GOLD, 2.5, 6, tn, fx="pop"), gl(nx + 40, ny + 14, 120, tn, .4, "lamp"),
           gl(sx, sy - 4, 70, ts, .7, "red", pulse=True)]
    bx, by = 1430, 560
    add += [lab(bx, by, "barren", tb, BONE, 32, "start"), lab(bx, by + 52, "great snakes", ts + .2, "#9fd89a", 32, "start"),
            lab(bx, by + 104, "very hot", th, "#ffb27a", 34, "start"), gl(bx + 150, by + 92, 40, th, .8, "sun"),
            ln([(bx - 12, by + 40), (sx + 30, sy - 10)], ts + .3, "#9fd89a", 1.6, dur=.5, op=.7)]
    return hero_panel([1.8, 1150, 620], add)


def s51():
    """The close: the map in quiet light; twenty faint lines converge on it from the dark; its Caribbean corner glows gold."""
    tp, tc = T("s51", "pieced together"), T("s51", "Columbus")
    P = hero_P()
    cx, cy = P(.5, .5)
    add = []
    for k in range(20):
        a = math.radians(110 + 140 * k / 19)
        x, y = cx + 900 * math.cos(a), cy - 640 * math.sin(a)
        x, y = max(90, min(1690, x)), max(120, min(800, y))
        add.append(ln([(x, y), (cx, cy)], tp + .06 * k, GOLD, 1.2, "inferred", .9, op=.35))
    car = [P(0, 0), P(.48, 0), P(.48, .33), P(0, .33)]
    add += drawn(car, "rgba(242,201,142,.12)", GOLD, 3, tc, 1.0) + [gl(*P(.24, .16), 200, tc, .45, "lamp")]
    return hero_panel([1.04, 889, 500], add)


# ================================================================== CHAPTER 2 · Twenty charts and Columbus
def XT14(yr):
    return round(160 + (yr - 1500) / 450 * 1460, 1)


def s14():
    """1513, drawn; 1517, to Sultan Selim; then a long lilac gap to 1929: lost for four centuries."""
    t4, tse, tva, tfc = T("s14", "Four years later"), T("s14", "Sultan Selim"), T("s14", "vanished"), T("s14", "four centuries")
    y = 580
    els = [gl(889, 470, 640, -1, .14, "lamp"), axis(160, 1620, y, [(XT14(v), str(v)) for v in (1500, 1600, 1700, 1800, 1900)], -1)]
    x13, x17, x29 = XT14(1513), XT14(1517), XT14(1929)
    mp, _ = piri_map(x13 - 40, y - 250, 110, at=-1, detail=False, shadow=False)
    els += [dot(x13, y, 10, GOLD, -1)] + mp + [lab(x13 + 50, y - 190, "1513, finished", -1, GOLD, 30, "start")]
    els += [dot(x17, y, 10, GOLD, t4), ln([(x17, y + 12), (x17, y + 70)], t4, GOLD, 2, dur=.4),
            lab(x17 + 10, y + 104, "1517, to Sultan Selim", tse, GOLD, 30, "start")]
    els += [{"k": "band", "x0": x17 + 40, "x1": x29, "y": y - 92, "h": 18, "c": LILAC, "op": .35, "in": tva, "dur": 1.6},
            ln([(x17 + 40, y - 83), (x29, y - 83)], tva, LILAC, 3, "claimed", dur=2.2),
            lab((x17 + x29) / 2 + 60, y - 124, "lost for four centuries", tfc, LILAC, 34, st="ital"),
            dot(x29, y, 9, DIM, tfc + .3), lab(x29, y + 104, "1929", tfc + .3, DIM, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s15():
    """Topkapi Palace, 1929: a library at night, shelves, a low table under a lamp, a bundle tied with cord; the skin rises out of it;
    the director beside it."""
    tt, td, tb = T("s15", "Topkapi Palace"), T("s15", "its director"), T("s15", "forgotten bundle")
    els = []
    wx, wy = 300, 170
    arch = [(wx, wy + 330), (wx, wy + 110)] + [(wx + 110 + 110 * math.cos(math.radians(a)), wy + 110 - 110 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(wx + 220, wy + 330)]
    els += [poly(arch, "#16243a", "#8a6a48", 4, -1), circ(wx + 140, wy + 90, 22, "#efe8da", at=-1), circ(wx + 152, wy + 84, 20, "#16243a", at=-1)]
    els += [dot(wx + 40 + 37 * k % 150, wy + 150 + (k * 53) % 140, 1.8, "#fff6e8", -1, op=.7) for k in range(9)]
    rr = random.Random(9)
    for s in range(3):
        y = 280 + 150 * s
        els.append(rect(620, y, 1000, 12, WOOD, "#8a6a48", 1, 2, -1))
        x = 630
        while x < 1600:
            w = rr.uniform(16, 30); h = rr.uniform(70, 120)
            els.append(rect(round(x, 1), round(y - h, 1), round(w, 1), round(h, 1), rr.choice(["#4a2f2a", "#3a3a2a", "#5a4630", "#2f3a44", "#5e3a28"]),
                            "rgba(255,226,190,.25)", 1, 2, -1, op=.85))
            x += w + 2
    els += [rect(560, 650, 640, 22, WOOD, "#8a6a48", 2, 3, -1), rect(590, 672, 18, 110, WOOD_D, at=-1), rect(1152, 672, 18, 110, WOOD_D, at=-1),
            gl(880, 520, 340, -1, .55, "lamp"), ln([(820, 112), (820, 400)], -1, "#8a6a48", 2, draw=False),
            poly([(790, 400), (850, 400), (836, 430), (804, 430)], "#c9a46a", at=-1), gl(820, 440, 120, -1, .7, "lamp")]
    for k in range(5):
        els.append(rect(760 + 6 * (k % 2), 610 - 9 * k, 240 - 10 * k, 12, ["#cbb48c", "#b89f78", "#d9c7a6", "#a88c66", "#c4ad85"][k], "#6b5a48", 1, 2, -1))
    els += [ln([(880, 566), (880, 650)], -1, "#8a5a3a", 3, draw=False), ln([(760, 610), (1000, 610)], -1, "#8a5a3a", 3, draw=False)]
    mp, _ = piri_map(842, 330, 230, at=tb, detail=False, shadow=True, tilt=6)
    for e in mp:
        e["fx"] = "rise"
    els += mp + [gl(925, 450, 220, tb + .4, .35, "lamp")]
    els += figure(1320, 782, 260, td, "#3a3f4a", kind="suit", face=-1, arm="fold")
    els += [lab(410, 580, "Topkapı Palace, 1929", tt, GOLD, 34, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def s16():
    """The whole world map, reconstructed in outline: its lost two thirds a lilac dotted frame; the surviving western third in solid skin."""
    tw, ta = T("s16", "western third"), T("s16", "Atlantic")
    x0, y0, H = 270, 170, 560
    W = .724 * H
    X1 = x0 + 3 * W
    els = [gl(889, 450, 760, -1, .16, "lamp"),
           rect(x0, y0, X1 - x0, H, "rgba(201,193,238,.04)", LILAC, 2.5, 6, -1, style="claimed"),
           lab(x0 + 2 * W, y0 + H * .52, "lost", .5, LILAC, 52, st="serif")]
    mp, P = piri_map(x0, y0, H, at=-1, detail=True, shadow=False, tilt=0)
    els += mp
    els += [rect(x0 - 6, y0 - 6, W + 12, H + 12, "none", GOLD, 3, 8, tw, fx="draw", dur=1.2), lab(x0 + W / 2, y0 + H + 52, "what survives", tw + .3, GOLD, 32)]
    els += [lab(*P(.52, .5), "the Atlantic", ta, BONE, 30, st="ital")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def school_page(x, y, w, h, at, lines=5, head="References", t_lines=None):
    els = [rect(x + 10, y + 14, w, h, "rgba(0,0,0,.4)", at=at, op=.4), rect(x, y, w, h, "#f3ead8", "#cbbca8", 1.5, 4, at, fx="pop")]
    els += [ln([(x + 10, y + 110 + 46 * k), (x + w - 10, y + 110 + 46 * k)], at, "#9fc0dd", 1.4, draw=False, op=.7) for k in range(int((h - 130) / 46))]
    els += [ln([(x + 60, y + 8), (x + 60, y + h - 8)], at, "#e09090", 1.6, draw=False, op=.8),
            lab(x + w / 2, y + 74, head, at + .2, "#3a2a1c", 36, st="serif", halo=False)]
    t0 = t_lines if t_lines is not None else at + .5
    for k in range(lines):
        yy = y + 102 + 46 * k
        els += [lab(x + 44, yy, "%d." % (k + 1), t0 + .35 * k, "#3a2a1c", 24, "end", halo=False),
                ln([(x + 72, yy - 8), (x + 72 + (w - 120) * (.55 + .4 * ((k * 7) % 5) / 5), yy - 8)], t0 + .35 * k, "#3a3a5a", 3, dur=.5)]
    return els


def s17():
    """Piri's notes on the skin, glowing one by one; beside them, a school exercise page headed References, five lines writing themselves."""
    tn, tl, tr = T("s17", "notes in Piri's own words"), T("s17", "He lists his sources"), T("s17", "references")
    x0, y0, w, h = 140, 150, 760, 600
    sheet = [(x0, y0 + 14), (x0 + w * .4, y0), (x0 + w * .8, y0 + 10), (x0 + w, y0 + 2), (x0 + w - 8, y0 + h * .5), (x0 + w, y0 + h), (x0 + w * .5, y0 + h - 8), (x0 + 10, y0 + h)]
    els = [gl(520, 450, 560, -1, .22, "lamp"), poly([(x + 14, y + 18) for x, y in sheet], "rgba(0,0,0,.4)", at=-1, op=.4),
           poly(sheet, "url(#k-papyrus)", "#7a5a38", 2, -1), poly(sheet, "url(#k-speck)", at=-1),
           ln([(x0 + 40, y0 + 470), (x0 + 200, y0 + 430), (x0 + 330, y0 + 520), (x0 + 420, y0 + 590)], -1, INK, 3, curve=True, draw=False, op=.7)]
    blocks = [(x0 + 60, y0 + 60, 300, 120, 4), (x0 + 420, y0 + 80, 280, 150, 5), (x0 + 80, y0 + 250, 330, 140, 5), (x0 + 450, y0 + 300, 250, 110, 4), (x0 + 470, y0 + 450, 230, 100, 3)]
    for k, (bx, by, bw, bh, rows) in enumerate(blocks):
        els += [ln([(bx, by - 6), (bx + bw * .5, by - 6)], -1, RINK, 4, draw=False, op=.85)] + glyph_block(bx, by, bw, bh, -1, rows, INK, 40 + k, 2.2)
        els += [rect(bx - 12, by - 22, bw + 24, bh + 30, "rgba(242,201,142,.12)", GOLD, 2.4, 8, tn + .45 * k, fx="pop"), gl(bx + bw / 2, by + bh / 2, 160, tn + .45 * k, .3, "lamp")]
    els += [lab(x0 + w / 2, y0 + h + 46, "his notes", tn + .2, GOLD, 32)]
    els += [arr([(x0 + w + 20, 450), (1000, 430)], tl, AMBER, 4, dur=.6)]
    els += school_page(1040, 170, 540, 560, tl + .3, 5, "References", tr)
    return {"base": "dark", "cam": CAM, "els": els}


def s18():
    """The sources fan: twenty charts in an arc, each tied to the map; eight from Alexander's day, an Arab map of India,
    four Portuguese maps, and Columbus's map, lost (lilac dots)."""
    ta, tal, tar, tpo, tco = T("s18", "About twenty"), T("s18", "Alexander"), T("s18", "Arab map"), T("s18", "Portuguese"), T("s18", "Columbus")
    cx, cy = 889, 690
    mx, my = 889, 660
    els = [gl(889, 600, 420, -1, .3, "lamp")]
    mp, _ = piri_map(mx - 52, my - 70, 144, at=-1, detail=False, shadow=True, tilt=0)
    els += mp
    for k in range(20):
        a = math.pi * (.06 + .88 * k / 19)
        x, y = cx - 470 * math.cos(a), cy - 420 * math.sin(a)
        grp = "col" if k == 0 else "por" if k <= 4 else "alx" if k <= 12 else "arab" if k == 13 else "other"
        at = ta + .06 * k
        style = "claimed" if grp == "col" else "known"
        fill = "none" if grp == "col" else PARCH_L
        els += [rect(x - 30, y - 22, 60, 44, fill, "#8a6a48" if grp != "col" else LILAC, 1.6, 4, at if grp != "col" else tco, fx="pop", style=style)]
        if grp != "col":
            els += [ln([(x - 18, y + 6), (x - 4, y - 10), (x + 8, y + 2), (x + 20, y - 8)], at, INK, 1.6, curve=True, draw=False)]
        els += [ln([(x, y + 22), (mx, my - 64)], at + .1 if grp != "col" else tco + .2, LILAC if grp == "col" else "#cbbca8", 1.4, "claimed" if grp == "col" else "inferred", .7, op=.6)]
        if grp == "alx":
            els += [rect(x - 34, y - 26, 68, 52, "none", AU, 2.4, 6, tal + .08 * (k - 5), fx="pop")]
        elif grp == "arab":
            els += [rect(x - 34, y - 26, 68, 52, "rgba(232,184,122,.25)", AMBER, 3, 6, tar, fx="pop")]
        elif grp == "por":
            els += [rect(x - 34, y - 26, 68, 52, "rgba(217,137,74,.2)", "#d9894a", 3, 6, tpo + .12 * (k - 1), fx="pop")]
    els += [lab(889, 236, "Alexander's day", tal + .3, AU, 30, st="ital")]
    x13 = cx - 470 * math.cos(math.pi * (.06 + .88 * 13 / 19)); y13 = cy - 420 * math.sin(math.pi * (.06 + .88 * 13 / 19))
    els += [lab(x13 + 52, y13 + 10, "Arab map of India", tar + .3, AMBER, 28, "start")]
    els += [lab(cx - 470 * math.cos(math.pi * .2) - 52, cy - 420 * math.sin(math.pi * .2), "4 Portuguese maps", tpo + .5, "#e8a26a", 28, "end")]
    x0_, y0_ = cx - 470 * math.cos(math.pi * .06), cy - 420 * math.sin(math.pi * .06)
    els += [lab(x0_ - 44, y0_ + 10, "Columbus (lost)", tco + .3, LILAC, 30, "end")]
    els += [lab(1350, 680, "about 20 charts", ta + 1.2, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


VAT = View(-88.0, 30.0, 5.0, 47.0, (90, 120, 1600, 680))


def s20():
    """The Spanish sailor: three voyages with Columbus across the Atlantic; captured by Kemal Reis's galley off Spain."""
    v = VAT
    tq, tc, ts, tt = T("s20", "How does"), T("s20", "captured"), T("s20", "Spanish sailor"), T("s20", "three times")
    px, py = v.p(-6.9, 37.2)
    hx, hy = v.p(-70.5, 19.0)
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(-45.0, 22.0), "Atlantic Ocean", .5, "#9fd0ff", 32, st="ital")]
    for k in range(3):
        mid = v.p(-38.0, 33.0 + 3.2 * k)
        els += [arr([(px - 8, py + 6), mid, (hx + 14, hy - 10 + 6 * k)], tt - .9 + .35 * k, LILAC, 2.6, "inferred", 1.0)]
        mx_, my_ = v.p(-38.0, 33.6 + 3.2 * k)
        els += [lab(mx_, my_ - 6, str(k + 1), tt - .5 + .35 * k, LILAC, 26)]
    els += [lab(*v.p(-38.0, 44.2), "three voyages with Columbus", tt + .4, LILAC, 30)]
    els += figure(px + 6, py - 2, 56, ts, "#5a6a7a", kind="tunic")
    els += [lab(px - 14, py + 46, "a Spanish sailor", ts + .2, BONE, 28, "end")]
    kx, ky = v.p(3.0, 38.4)
    els += kadirga(kx, ky, 90, tq + .6, "#e8d6b8", GOLD, 1, oars=False, cabin=False) + [lab(kx + 10, ky - 54, "Kemal Reis", tq + .8, GOLD, 28)]
    els += [arr([(kx - 30, ky + 6), v.p(-2.5, 36.6), (px + 22, py)], tc, AMBER, 3, dur=.7), lab(*v.p(-2.0, 34.6), "captured", tc + .4, AMBER, 26)]
    return {"base": "map", "cam": CAM, "els": els}


def s21():
    """Two Caribbeans: Piri's (Hispaniola huge and upright, Cuba drawn as a mainland coast, Ornofay on it) beside today's map in a window."""
    th, tj, tcu, tas, tor = T("s21", "Hispaniola"), T("s21", "Japan"), T("s21", "Cuba"), T("s21", "Asia"), T("s21", "Ornofay")
    x0, y0, w, h = 110, 150, 760, 620
    sheet = [(x0, y0 + 8), (x0 + w * .5, y0), (x0 + w, y0 + 10), (x0 + w - 6, y0 + h), (x0 + w * .5, y0 + h - 6), (x0 + 6, y0 + h)]
    els = [poly(sheet, "url(#k-papyrus)", "#7a5a38", 2, -1), poly(sheet, "url(#k-speck)", at=-1)]
    sx, sy = w / .48, h / .33
    Q = lambda u, v: (round(x0 + u * sx, 1), round(y0 + v * sy, 1))
    mw = [Q(u, v) for u, v in MAINLAND_W]
    hi = [Q(u, v) for u, v in HISPANIOLA]
    els += [poly(mw + [Q(0, .262), Q(0, 0)], LANDT, at=-1), ln(mw, -1, INK, 3, curve=True, draw=False),
            poly(hi, "rgba(61,107,68,.45)", INK, 2.4, -1, curve=True)]
    for (u, v, rx, ry, c) in ISLANDS:
        if u < .46 and v < .32:
            x, y = Q(u, v)
            els.append(poly(E(x, y, rx * sx, ry * sy, 14), c, INK, 1.2, -1, curve=True))
    els += [lab(x0 + w / 2, y0 - 12, "Piri, 1513", -1, GOLD, 24, st="cap")]
    win = [930, 170, 740, 560]
    v = View(-86.0, -64.0, 16.0, 25.0, (930, 170, 740, 560))
    els += [rect(win[0], win[1], win[2], win[3], "#10202b", "none", 0, 14, -1),
            {"k": "group", "clip": win + [14], "els": [{"k": "map", "land": v.land()}], "in": -1},
            rect(win[0], win[1], win[2], win[3], "none", "rgba(255,236,206,.35)", 2, 14, -1), lab(1300, y0 + 8, "today", -1, DIM, 24, st="cap")]
    hisp = [v.p(lo, la) for lo, la in [(-74.4, 19.9), (-72.8, 19.95), (-71.6, 19.9), (-70.0, 19.7), (-68.9, 18.95), (-68.5, 18.4), (-70.0, 18.2), (-71.4, 17.6),
                                       (-72.2, 18.1), (-73.6, 18.0), (-74.45, 18.4), (-72.8, 18.95)]]
    cuba = [v.p(lo, la) for lo, la in [(-84.95, 21.85), (-83.2, 22.95), (-81.5, 23.2), (-79.6, 22.9), (-77.6, 21.9), (-75.6, 21.0), (-74.15, 20.25), (-75.9, 19.9),
                                       (-77.7, 19.85), (-77.25, 20.6), (-78.5, 21.6), (-80.6, 21.85), (-82.4, 22.2), (-84.4, 21.6)]]
    els += drawn(hisp, "rgba(242,201,142,.25)", GOLD, 3, th, .8, curve=True) + [poly(hi, "none", GOLD, 4, th, curve=True, fx="draw", dur=1.0),
            lab(*v.p(-71.4, 21.2), "Hispaniola", th + .3, GOLD, 28), lab(Q(.27, .14)[0] + 64, Q(.27, .14)[1] + 10, "Japan?", tj, LILAC, 34, "start", st="ital")]
    els += drawn(cuba, "rgba(242,201,142,.18)", GOLD, 3, tcu, 1.0, curve=True) + [ln(mw, tcu, GOLD, 5, dur=1.2, curve=True),
            lab(*v.p(-79.0, 24.0), "Cuba", tcu + .3, GOLD, 28), lab(Q(.06, .26)[0] + 20, Q(.06, .26)[1] + 52, "part of Asia?", tas, LILAC, 32, "start", st="ital")]
    ox, oy = Q(.142, .15)
    els += [{"k": "pin", "x": ox, "y": oy, "t": "Ornofay", "c": GOLD, "in": tor, "lx": 18, "ly": 8}]
    return {"base": "dark", "cam": CAM, "els": els}


def XC(yr):
    return round(200 + (yr - 1490) / 16 * 1380, 1)


def s22():
    """Columbus's four voyages as arcs on a timeline; McIntosh's study; the second voyage (1493 to 1496) lights gold."""
    tm, ts, t93 = T("s22", "McIntosh"), T("s22", "second voyage"), T("s22", "fourteen ninety-three")
    y = 600
    els = [gl(889, 470, 640, -1, .14, "lamp"), axis(200, 1580, y, [(XC(v), str(v)) for v in (1490, 1495, 1500, 1505)], -1, "years CE")]
    vs = [(1492.6, 1493.2, "1st"), (1493.73, 1496.45, "2nd"), (1498.4, 1500.85, "3rd"), (1502.36, 1504.85, "4th")]
    for k, (a, b, name) in enumerate(vs):
        xa, xb = XC(a), XC(b)
        hgt = 120 + 40 * (xb - xa) / 200
        pts = [(xa, y - 6), ((xa + xb) / 2, y - 6 - hgt), (xb, y - 6)]
        gold = k == 1
        els += [ln(pts, -1, DIM, 3, curve=True, draw=False, op=.55), lab((xa + xb) / 2, y - 24 - hgt * .55, name, -1, DIM, 26)]
        if gold:
            els += [ln(pts, ts, GOLD, 6, curve=True, dur=1.2), gl((xa + xb) / 2, y - 6 - hgt * .6, 220, ts + .5, .4, "lamp")]
            els += chip((xa + xb) / 2, y + 120, "1493 to 1496", GOLD, t93, 30)
    # the scholar: a book, open, with a pen: McIntosh 2000
    bk, lp, rp = open_book(1330, 170, 120, 130, tm, fx="pop")
    els += bk + glyph_block(lp[0], lp[1], lp[2], lp[3], tm + .2, 4, INK, 61, 1.4) + glyph_block(rp[0], rp[1], rp[2], rp[3], tm + .3, 4, INK, 62, 1.4)
    els += [lab(1330, 360, "McIntosh: the second voyage", ts + .5, GOLD, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s23():
    """Columbus's chart is lost (an empty lilac frame); the only known copy, in part, lives in the map's Caribbean (gold)."""
    tl, tc = T("s23", "lost"), T("s23", "only known copy")
    els = [gl(1200, 450, 520, -1, .2, "lamp")]
    els += [rect(200, 260, 420, 300, "rgba(201,193,238,.05)", LILAC, 3, 8, -1, style="claimed"), lab(410, 430, "?", tl, LILAC, 90, st="big", fx="pop"),
            lab(410, 620, "Columbus's chart: lost", tl + .2, LILAC, 32)]
    mp, P = piri_map(1010, 160, 560, at=-1, detail=True, shadow=True, tilt=-2)
    els += mp
    car = [P(0, 0), P(.48, 0), P(.48, .33), P(0, .33)]
    els += drawn(car, "rgba(242,201,142,.16)", GOLD, 4, tc, .9) + [gl(*P(.24, .16), 220, tc + .3, .4, "lamp"),
            arr([(630, 410), (820, 330), P(-.02, .16)], tc - .3, GOLD, 4, dur=.8),
            lab(760, 280, "the only known copy", tc + .4, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · A coast under the ice?
def mic(x, y, s, at):
    return [ln([(x, y), (x, y - 70 * s)], at, "#8a8f96", 4 * s, draw=False), poly(E(x, y - 84 * s, 13 * s, 18 * s, 14), "#5a5f66", "#c9ced4", 1.5, at, curve=True),
            rect(x - 22 * s, y - 4, 44 * s, 8, "#3a3d42", at=at)]


def s24():
    """A 1950s radio panel: a long table, three microphones, three panellists; radio waves from a mast; Arlington Mallery lit."""
    tg, tm, ts = T("s24", "Georgetown University"), T("s24", "Arlington Mallery"), T("s24", "startling suggestion")
    els = []
    for k, (x, c) in enumerate(((520, "#3a3f4a"), (800, "#4a4036"), (1080, "#2f3a44"))):
        els += bust(x, 560, 320, -1, c)
    els += [rect(380, 560, 860, 30, WOOD, "#8a6a48", 2, 4, -1), rect(400, 590, 820, 150, WOOD_D, "#5a4330", 1.5, 2, -1)]
    for x in (580, 860, 1140):
        els += mic(x, 560, 1.0, -1)
    els += [gl(800, 430, 220, tm, .5, "lamp"), lab(800, 790, "Arlington Mallery", tm + .2, GOLD, 32)]
    mx = 1480
    els += [ln([(mx - 50, 720), (mx, 200), (mx + 50, 720)], -1, "#8a8f96", 4, draw=False), ln([(mx - 30, 520), (mx + 30, 520)], -1, "#8a8f96", 3, draw=False),
            ln([(mx - 40, 620), (mx + 40, 620)], -1, "#8a8f96", 3, draw=False), dot(mx, 200, 8, RED, -1)]
    for k in range(4):
        r = 50 + 50 * k
        els += [ln([(mx - r * .7, 200 - r * .7), (mx - r, 200), (mx - r * .7, 200 + r * .7)], .4 + .5 * k, BLUE, 2.6, curve=True, dur=.5, op=.7 - .12 * k),
                ln([(mx + r * .7, 200 - r * .7), (mx + r, 200), (mx + r * .7, 200 + r * .7)], .4 + .5 * k, BLUE, 2.6, curve=True, dur=.5, op=.7 - .12 * k)]
    els += [lab(800, 190, "Georgetown radio, 1956", tg, BONE, 34, st="serif")]
    els += qmark(800, 330, ts + .3, 70, AU, halo=False)
    return {"base": "dark", "cam": CAM, "els": els}


PQ = Polar(700, 610, 500, -52)


def s25():
    """Antarctica from above the South Pole, Africa's tip at the top, South America's at upper left: Queen Maud Land's coast glows gold;
    a lilac dotted arrow from the map's southern coast: the claim."""
    tq, tafr, tma = T("s25", "Queen Maud Land"), T("s25", "south of Africa"), T("s25", "mapped before")
    pol = Polar(720, 640, 470, -40)
    paths = []
    for poly_ in F._topo():
        ring = poly_[0]
        if min(q[1] for q in ring) > -20:
            continue
        pts, last = [], None
        for lo, la in ring:
            q = pol.p(lo, la)
            if last and abs(q[0] - last[0]) < 2 and abs(q[1] - last[1]) < 2:
                continue
            pts.append(q); last = q
        if len(pts) > 3:
            paths.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
    els = [{"k": "map", "land": paths, "in": -1, "landc": "#3d3a36"}]
    ant = antarctica_rings(pol)
    els += [poly(ant[0], "rgba(234,243,248,.5)", ICE_D, 1.6, -1)] + [poly(r, "rgba(234,243,248,.4)", ICE_D, 1.2, -1) for r in ant[1:8]]
    els += [dot(720, 640, 6, BONE, .4), lab(720, 676, "South Pole", .5, DIM, 24, st="small")]
    qc = qml_coast(pol)
    els += [ln(qc, tq, GOLD, 6, dur=1.6, curve=True), gl(*qc[len(qc) // 2], 200, tq + .4, .45, "lamp"),
            lab(qc[len(qc) // 2][0] + 10, qc[len(qc) // 2][1] - 56, "Queen Maud Land", tq + .3, GOLD, 32)]
    ax_, ay_ = pol.p(24, -31)
    els += [lab(ax_ + 30, max(160, ay_ + 30), "Africa", tafr, BONE, 30, "start")]
    sx_, sy_ = pol.p(-68, -50)
    els += [lab(sx_ - 10, sy_ - 30, "South America", .8, DIM, 26, "end")]
    mp, P = piri_map(1380, 190, 300, at=.3, detail=False, shadow=True, tilt=0)
    els += mp + [coast_line(P, SOUTH_COAST, .3, LILAC, 4)]
    tx, ty = P(.4, .92)
    els += [arr([(tx, ty + 10), (1240, 640), (qc[len(qc) // 2][0] + 40, qc[len(qc) // 2][1] + 20)], tma, LILAC, 3, "claimed", 1.2),
            lab(1300, 700, "the claim", tma + .4, LILAC, 32, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def coast_line(P, pts, at, c, w, style="known"):
    return ln([P(u, v) for u, v in pts], at, c, w, style, curve=True, draw=False)


def s26():
    """Hapgood's class: a blackboard with the map's outline and a grid in chalk; the teacher pointing at it; students at desks."""
    th, tst = T("s26", "Charles Hapgood"), T("s26", "students")
    els = [rect(280, 160, 1000, 420, "#24332a", "#6b4a30", 12, 4, -1), poly([(280, 160), (1280, 160), (1280, 580), (280, 580)], "url(#k-speck)", at=-1)]
    S_ = 360
    Q = SK(380, 190, .724 * S_, S_, 0)
    chalk = "rgba(240,236,226,.85)"
    els += [ln([Q(u, v) for u, v in SKIN_OUT] + [Q(*SKIN_OUT[0])], .4, chalk, 2.2, dur=1.6)]
    for pts in (IBERIA_AFRICA, MAINLAND_W, SOUTH_AM, SOUTH_COAST):
        els.append(ln([Q(u, v) for u, v in pts], 1.0, chalk, 2, dur=1.4, curve=True))
    for k in range(5):
        els += [ln([(720, 210 + 80 * k), (1220, 210 + 80 * k)], 1.8 + .1 * k, chalk, 1.4, "inferred", .6, op=.6),
                ln([(740 + 110 * k, 200), (760 + 110 * k, 550)], 2.2 + .1 * k, chalk, 1.4, "inferred", .6, op=.6)]
    els += figure(1420, 780, 320, th - .6, "#3a3f4a", kind="suit", face=-1, arm="point")
    els += [lab(1470, 380, "Charles Hapgood", th, GOLD, 32)]
    for k, (x, c) in enumerate(((330, "#5a4a3a"), (560, "#3a4a5a"), (790, "#6b3a2a"), (1020, "#3a5a4a"))):
        els += sitter(x, 790, 200, tst + .15 * k, c, 1) + [rect(x + 50, 680, 120, 14, WOOD, "#8a6a48", 1, 2, tst + .15 * k, fx="rise"),
                                                          rect(x + 150, 694, 10, 96, WOOD_D, at=tst + .15 * k, fx="rise")]
    els += [lab(1470, 170, "Keene State College", .6, DIM, 24, st="cap")]
    return {"base": "dark", "floor": 790, "cam": CAM, "els": els}


def s27():
    """The letter of 6 July 1960 on a lamp-lit desk: letterhead, typed lines, a signature; one line glows."""
    tl, tc, tr = T("s27", "a letter arrived"), T("s27", "Its commander"), T("s27", "agreed remarkably well")
    x, y, w, h = 690, 128, 470, 650
    els = [gl(925, 430, 620, -1, .3, "lamp"), rect(x + 16, y + 20, w, h, "rgba(0,0,0,.45)", at=-1, op=.45), rect(x, y, w, h, "#f1ece0", "#cbbca8", 1.5, 3, -1)]
    els += [circ(x + 60, y + 60, 28, "none", "#3a4a6a", 3, -1), circ(x + 60, y + 60, 12, "#3a4a6a", at=-1),
            {"k": "glyphs", "x": x + 110, "y": y + 40, "w": 320, "h": 44, "rows": 2, "cols": 14, "kind": "latin", "c": "#3a4a6a", "in": -1},
            lab(x + w - 30, y + 140, "6 July 1960", -1, "#2a2a2a", 24, "end", st="mono", halo=False)]
    for k in range(11):
        yy = y + 190 + 34 * k
        ww = w - 80 if k % 4 != 3 else (w - 80) * .6
        els.append({"k": "glyphs", "x": x + 40, "y": yy, "w": ww, "h": 20, "rows": 1, "cols": int(ww / 16), "kind": "latin", "c": "#3a3a3a", "in": -1})
        if k == 5:
            els += [rect(x + 30, yy - 8, w - 60, 36, "rgba(242,201,142,.35)", GOLD, 2.5, 4, tr, fx="pop")]
    els += [ln([(x + 50, y + 600), (x + 90, y + 580), (x + 120, y + 606), (x + 160, y + 584), (x + 200, y + 600)], .3, "#2a3a6a", 2.4, curve=True, dur=.8)]
    els += [lab(560, 300, "US Air Force, 1960", tl, BONE, 32, "end"), lab(560, 640, "Lt Col Harold Ohlmeyer", tc, GOLD, 30, "end"),
            leader(570, 630, x + 40, y + 596, tc, GOLD)]
    return {"base": "dark", "cam": CAM, "els": els}


# the coast of Queen Maud Land in section (s28 for the claim; s40 to s42 for the real ice)
def section_parts(sea_y=470):
    bed = [(-30, 774), (80, 770), (240, 760), (360, 752), (520, 735), (700, 720), (820, 700), (950, 640), (1060, 700), (1160, 690), (1250, 560), (1310, 440), (1360, 430),
           (1420, 520), (1500, 610), (1600, 640), (1700, 615), (1810, 600)]
    surf = [(700, sea_y - 60), (800, sea_y - 100), (900, 360), (1030, 300), (1150, 262), (1300, 228), (1450, 205), (1600, 190), (1700, 186), (1810, 183)]
    shelf_top = [(360, sea_y - 28), (500, sea_y - 36), (620, sea_y - 48), (700, sea_y - 60)]
    shelf_bot = [(700, sea_y + 230), (600, sea_y + 160), (480, sea_y + 112), (360, sea_y + 86)]
    return bed, surf, shelf_top, shelf_bot


def bed_y(x, bed):
    for (x0, y0), (x1, y1) in zip(bed, bed[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return bed[-1][1]


def ice_section(at=-1, sea_y=470, ice_op=1.0):
    bed, surf, st, sb = section_parts(sea_y)
    grounded = surf + [(1810, bed_y(1810, bed))] + [(x, y) for x, y in reversed(bed) if 700 <= x <= 1810] + [(700, bed_y(700, bed))]
    shelf = st + sb
    els = [{"k": "water", "y": sea_y, "h": 700, "x0": -100, "x1": 760, "op": .95, "in": at},
           poly(bed + [(1810, 1100), (-30, 1100)], ROCK, "#8a7a6a", 1.6, at),
           poly(bed + [(1810, 1100), (-30, 1100)], "url(#k-speck)", at=at),
           poly(grounded, ICE, "#ffffff", 1.4, at, op=ice_op), poly(shelf, "#dbe9f2", "#ffffff", 1.4, at, op=ice_op)]
    els += [ln([(x, y + 14 + 18 * k) for x, y in surf[2:]], at, ICE_S, 1, draw=False, curve=True, op=.35) for k in range(5)]
    return els


def s28():
    """The claim in section: the sea, the ice shelf and the ice sheet over its rock; the 1949 seismic profile traced along the rock
    (dots); a lilac arrow from a tiny copy of the map's coast: mapped before the ice? About a mile of ice."""
    tm, ti = T("s28", "mapped before the ice"), T("s28", "about a mile")
    bed, surf, st, sb = section_parts()
    els = ice_section(-1)
    prof = [(x, bed_y(x, bed) - 6) for x in range(760, 1680, 40)]
    els += [ln(prof, .5, BLUE, 3, "claimed", dur=2.0), lab(1560, 780, "seismic profile, 1949", 1.2, BLUE, 26)]
    mp, P = piri_map(140, 150, 200, at=.2, detail=False, shadow=True, tilt=0)
    els += mp + [coast_line(P, SOUTH_COAST, .2, LILAC, 3.5)]
    els += [arr([P(.6, .95), (700, 340), (980, 610)], tm, LILAC, 3, "claimed", 1.2), lab(560, 260, "mapped before the ice?", tm + .4, LILAC, 32, "start", st="ital")]
    yb, yt = bed_y(1230, bed) - 4, 250
    els += [ln([(1230, yb), (1230, yt)], ti, GOLD, 2.5, dur=.8), ln([(1218, yb), (1242, yb)], ti, GOLD, 2.5, draw=False), ln([(1218, yt), (1242, yt)], ti, GOLD, 2.5, draw=False),
            lab(1214, (yb + yt) / 2 + 10, "about a mile", ti + .3, GOLD, 30, "end")]
    els += [lab(200, 640, "sea", .3, "#bfe6f5", 30, st="ital"), lab(330, 800, "rock", .3, DIM, 24, st="small")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def book_cover(x, y, w, h, at, c, lines, tc=AU, fx="pop", size=30):
    els = [rect(x + 14, y + 18, w, h, "rgba(0,0,0,.45)", at=at, op=.45), rect(x, y, w, h, c, "rgba(255,226,190,.4)", 2, 6, at, fx=fx),
           rect(x, y, 22, h, "rgba(0,0,0,.35)", at=at), rect(x + 40, y + 60, w - 70, 6, tc, at=at, op=.8)]
    for k, t in enumerate(lines):
        els.append(lab(x + w / 2 + 10, y + 130 + k * (size + 14), t, at + .1, tc, size, st="serif", halo=False))
    els.append(rect(x + 40, y + h - 70, w - 70, 6, tc, at=at, op=.8))
    return els


def s29():
    """Hapgood's book (1966) standing in lamplight; behind it, in lilac dots, a ghost globe sailed by ancient ships, copies of charts
    leading from it to the 1513 map: a lost seafaring people?"""
    tb, tt, tan = T("s29", "Maps of the Ancient Sea Kings"), T("s29", "His theory"), T("s29", "Antarctica included")
    els = [gl(1220, 450, 520, -1, .3, "lamp")]
    els += book_cover(1060, 190, 330, 470, tb - .6, "#2c4a3a", ["Maps of the", "Ancient", "Sea Kings"], AU, size=34)
    els += chip(1225, 720, "1966", GOLD, tb, 30)
    gx_, gy_, gr = 470, 400, 210
    els += [circ(gx_, gy_, gr, "rgba(201,193,238,.05)", LILAC, 2.5, tt, style="claimed", fx="draw", dur=1.2)]
    els += [poly(E(gx_, gy_, gr * f, gr, 30), "none", LILAC, 1.4, tt + .2, style="claimed", op=.6) for f in (.35, .7)]
    els += [ln([(gx_ - gr, gy_), (gx_ + gr, gy_)], tt + .2, LILAC, 1.4, "claimed", .6, op=.6)]
    for k, a in enumerate((200, 300, 40)):
        x = gx_ + (gr + 34) * math.cos(math.radians(a)); y = gy_ + (gr + 34) * math.sin(math.radians(a))
        els += [poly([(x - 30, y - 6), (x + 30, y - 10), (x + 22, y + 8), (x - 22, y + 8)], "none", LILAC, 2, tt + .5 + .2 * k, style="claimed"),
                poly([(x - 4, y - 8), (x + 2, y - 44), (x + 20, y - 12)], "none", LILAC, 2, tt + .5 + .2 * k, style="claimed")]
    for k in range(4):
        cx_, cy_ = 720 + 80 * k, 600 - 20 * k
        s_ = 70 - 10 * k
        els += [rect(cx_ - s_ / 2, cy_ - s_ * .36, s_, s_ * .72, "none", LILAC, 2, 4, tt + 1.0 + .25 * k, style="claimed", fx="pop")]
    pol = Polar(gx_, gy_ + gr * .78, 52, -60)
    ring = antarctica_rings(pol, tol=1.2)[0]
    els += [poly(ring, "rgba(201,193,238,.3)", LILAC, 2, tan, fx="pop"), gl(gx_, gy_ + gr * .78, 90, tan, .45, "lamp")]
    els += [lab(gx_, gy_ + gr + 80, "a lost seafaring people?", tt + .8, LILAC, 32, st="ital")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def scissors(x, y, s, at, c=BONE):
    return [circ(x - 14 * s, y + 18 * s, 9 * s, "none", c, 3 * s, at, fx="pop"), circ(x + 14 * s, y + 18 * s, 9 * s, "none", c, 3 * s, at, fx="pop"),
            ln([(x - 10 * s, y + 10 * s), (x + 16 * s, y - 34 * s)], at, c, 3 * s, draw=False), ln([(x + 10 * s, y + 10 * s), (x - 16 * s, y - 34 * s)], at, c, 3 * s, draw=False)]


def s30():
    """Hapgood's reading: on the real outline of South America and the Antarctic Peninsula, a stretch of coast cut out (about 1,400 km)
    and the Drake Passage cut out, in red dashes: his explanations, not the map's."""
    v = View(-84.0, -24.0, -70.0, 6.0, (90, 120, 1600, 680))
    tc, td, ts = T("s30", "fourteen hundred kilometres"), T("s30", "Drake Passage"), T("s30", "Slips")
    els = [{"k": "group", "clip": [0, 0, 1778, 830, 0], "els": [{"k": "map", "land": v.land()}], "in": -1},
           lab(*v.p(-58.0, -8.0), "South America", .4, DIM, 28, st="ital"), lab(*v.p(-50.0, -67.6), "Antarctica", .4, DIM, 26, st="ital")]
    a = [v.p(lo, la) for lo, la in [(-48.4, -26.0), (-48.9, -28.6), (-50.6, -31.0), (-52.6, -33.4), (-54.4, -34.8), (-57.0, -35.8), (-56.8, -37.5)]]
    off = [(x + 40, y) for x, y in a]
    els += [ln(off, tc, RED, 4, "inferred", dur=1.2, curve=True), ln([a[0], off[0]], tc, RED, 2, draw=False), ln([a[-1], off[-1]], tc + 1.0, RED, 2, draw=False)]
    els += scissors(off[3][0] + 50, off[3][1], 1.0, tc + .4)
    els += [lab(off[3][0] + 90, off[3][1] + 10, "1,400 km left out?", tc + .6, RED, 28, "start")]
    cx_, cy_ = v.p(-67.27, -55.98)
    px_, py_ = v.p(-61.0, -63.0)
    els += drawn([(cx_ - 30, cy_ + 10), (cx_ + 60, cy_ + 20), (px_ + 50, py_ - 10), (px_ - 40, py_ - 20)], "rgba(255,138,122,.12)", RED, 2.5, td, 1.0, style="inferred") + [
            lab(px_ + 70, (cy_ + py_) / 2 + 10, "Drake Passage left out?", td + .3, RED, 28, "start")]
    els += [lab(889, 160, "Hapgood's explanations", ts, LILAC, 26, st="cap")]
    return {"base": "map", "cam": CAM, "els": els}


def s31():
    """Hancock's bestseller (1995), open: on its first page, the 1960 letter; copies of the book standing in the dark behind."""
    tb, tl, tf = T("s31", "Graham Hancock"), T("s31", "that Air Force letter"), T("s31", "famous ever since")
    els = [gl(889, 430, 600, -1, .26, "lamp")]
    for k in range(16):
        x = 150 + 80 * (k % 8) + (1000 if k % 8 >= 4 else 0) - (0 if k % 8 < 4 else 320)
        y = 230 + 300 * (k // 8)
        els += [rect(x, y, 58, 86, "#3a2a24", "rgba(255,226,190,.3)", 1, 3, tf - .6 + .05 * k, fx="pop", op=.6),
                rect(x + 8, y + 16, 42, 4, AU, at=tf - .6 + .05 * k, fx="pop", op=.5), rect(x + 8, y + 62, 42, 3, AU, at=tf - .6 + .05 * k, fx="pop", op=.4)]
    bk, lp, rp = open_book(889, 230, 320, 400, tb - .4)
    els += bk + [lab(lp[0] + lp[2] / 2, lp[1] + 90, "1", tb, "#3a2a1c", 64, st="serif", halo=False),
                 rect(lp[0] + 40, lp[1] + 130, lp[2] - 80, 3, "#8a6a48", at=tb, op=.8)] + glyph_block(lp[0] + 20, lp[1] + 170, lp[2] - 40, 150, tb, 5, INK, 71, 1.6)
    lx, ly = rp[0] + 30, rp[1] + 20
    els += [rect(lx, ly, rp[2] - 60, rp[3] - 40, "#f1ece0", "#8a7a6a", 1.2, 2, tl, fx="pop"), circ(lx + 24, ly + 24, 10, "none", "#3a4a6a", 2, tl)]
    els += [{"k": "glyphs", "x": lx + 16, "y": ly + 60 + 18 * k, "w": rp[2] - 100, "h": 12, "rows": 1, "cols": 12, "kind": "latin", "c": "#4a4a4a", "in": round(tl + .1, 2)} for k in range(9)]
    els += [lab(889, 190, "Fingerprints of the Gods", tb, BONE, 34, st="ital")] + chip(470, 330, "1995", GOLD, tb + .2, 28)
    els += [lab(rp[0] + rp[2] / 2, rp[1] + rp[3] + 64, "chapter 1: the letter", tl + .3, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}




# ================================================================== CHAPTER 4 · Why the coast bends
def gc_km(a, b):
    (lo1, la1), (lo2, la2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(d))


def s33():
    """The real gap: Cape Horn and the Antarctic Peninsula with the Drake Passage between them, about 800 km; the same length from
    Paris to Barcelona."""
    v = View(-96.0, -34.0, -66.5, -50.5, (90, 120, 1600, 600))
    td, t8, tp = T("s33", "No Drake"), T("s33", "eight hundred"), T("s33", "Paris")
    ch = (-67.27, -55.98)
    sh = (-61.0, -62.75)
    km = gc_km(ch, sh)
    cx_, cy_ = v.p(*ch)
    sx_, sy_ = v.p(*sh)
    els = [{"k": "map", "land": v.land(), "in": -1},
           dot(cx_, cy_, 7, BONE, .3), lab(cx_ - 14, cy_ - 12, "Cape Horn", .4, BONE, 28, "end"),
           lab(*v.p(-66.0, -65.8), "Antarctica", .4, ICE, 28, "end"),
           lab(*v.p(-56.5, -58.6), "Drake Passage", td, "#9fd0ff", 34, "start", st="ital"),
           {"k": "dim", "x1": cx_ + 6, "y1": cy_ + 8, "x2": sx_ - 4, "y2": sy_ - 8, "t": "about 800 km", "c": GOLD, "fx": "draw", "dur": 1.0, "in": t8, "lx": -70, "ly": 10}]
    L = v.km(km)
    bx, by = 1180, 640
    els += [ln([(bx, by), (bx + L, by)], tp, AMBER, 10, dur=1.0, op=.9), dot(bx, by, 9, AMBER, tp), dot(bx + L, by, 9, AMBER, tp + .9),
            lab(bx, by - 26, "Paris", tp + .2, AMBER, 28), lab(bx + L, by - 26, "Barcelona", tp + 1.0, AMBER, 28)]
    return {"base": "map", "cam": CAM, "els": els}


def hide_outline(cx, cy, s):
    """A gazelle hide laid flat (schematic): body, four legs, a neck."""
    pts = [(-.38, -.32), (-.62, -.62), (-.52, -.66), (-.3, -.42), (-.1, -.44), (.1, -.44), (.3, -.42), (.5, -.66), (.6, -.62), (.38, -.3), (.44, -.08),
           (.58, -.04), (.66, .06), (.56, .1), (.44, .08), (.4, .3), (.62, .6), (.52, .64), (.3, .4), (.1, .44), (-.1, .44), (-.3, .4), (-.52, .64), (-.62, .6),
           (-.4, .3), (-.44, .0)]
    return [(cx + x * s, cy + y * s * .82) for x, y in pts]


def s34():
    """Clue one, the skin: a whole hide laid flat, the map's piece cut from its shoulder, its rounded corner glowing; a coast runs down the
    piece's edge and turns along the curve. Then handwriting that runs out of page and turns down the margin."""
    tsh, tco, tma, thw = T("s34", "shoulder of a hide"), T("s34", "curves at one corner"), T("s34", "turned a coast"), T("s34", "Like handwriting")
    cx, cy, s = 470, 440, 560
    hide = hide_outline(cx, cy, s)
    els = [gl(470, 440, 480, -1, .2, "lamp"), poly(hide, "url(#k-papyrus)", "#7a5a38", 2, -1, curve=True), poly(hide, "url(#k-speck)", at=-1, curve=True)]
    # the piece: the skin outline at small size, set on the right shoulder of the hide
    Hp = 300
    Q = SK(cx + 40, cy - 190, .724 * Hp, Hp, 0)
    piece = [Q(u, v) for u, v in SKIN_OUT]
    els += drawn(piece, "rgba(242,201,142,.18)", GOLD, 3, tsh, 1.2) + [lab(cx, 112 + 34, "a hide's shoulder", tsh + .3, GOLD, 30)]
    cu = [Q(u, v) for u, v in [(.2, .978), (.15, .962), (.105, .938), (.068, .906), (.04, .865), (.022, .815)]]
    els += [ln(cu, tco, AU, 7, dur=.8, curve=True), gl(*cu[2], 90, tco, .5, "lamp")]
    co = [Q(u, v) for u, v in [(.07, .4), (.06, .6), (.05, .75), (.06, .86), (.1, .91), (.18, .935), (.4, .93), (.7, .935), (.92, .93)]]
    els += [ln(co, tma, LILAC, 4, dur=1.6, curve=True), lab(cx, 780, "turned to fit", tma + .8, LILAC, 28, st="ital")]
    # handwriting that runs out of page and turns down the margin
    px, py, pw, ph = 1060, 200, 500, 520
    els += [rect(px + 12, py + 16, pw, ph, "rgba(0,0,0,.4)", at=-1, op=.4), rect(px, py, pw, ph, "#f3ead8", "#cbbca8", 1.5, 4, -1)]
    for k in range(5):
        yy = py + 70 + 60 * k
        els += [{"k": "glyphs", "x": px + 40, "y": yy - 16, "w": pw - 80, "h": 22, "rows": 1, "cols": 16, "kind": "latin", "c": "#3a3a5a", "in": -1}]
    w0 = py + 70 + 60 * 5
    wave = [(px + 40 + 10 * k, w0 - 8 + 5 * math.sin(k * 1.3)) for k in range(44)]
    down = [(px + pw - 20 + 5 * math.sin(k * 1.3), w0 + 8 * k) for k in range(1, 18)]
    els += [ln(wave + down, thw, "#3a3a5a", 3, dur=1.8, curve=True), lab(px + pw / 2, py + ph + 50, "out of page", thw + 1.4, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s35():
    """Clue two: the real coast of Brazil, solid to about 25 degrees south (Cabo Frio, Cananeia); beyond, the map's coast swings east,
    drawn from guesses and reports."""
    v = View(-76.0, -4.0, -44.0, 1.0, (90, 120, 1600, 680))
    tl, t25, tg = T("s35", "The last place"), T("s35", "twenty-five degrees"), T("s35", "guesses and reports")
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(-52.0, -10.0), "Brazil", .4, DIM, 30, st="ital")]
    y25 = v.p(-40, -25)[1]
    els += [rect(-20, y25, 1820, 1100 - y25, "rgba(10,8,6,.5)", at=t25 + .2, op=.5),
            ln([(90, y25), (1690, y25)], t25, GOLD, 2.4, "inferred", dur=1.2), lab(1680, y25 - 14, "25° S", t25 + .3, GOLD, 30, "end")]
    fx_, fy_ = v.p(-42.0, -22.9)
    kx_, ky_ = v.p(-47.93, -25.01)
    els += [{"k": "pin", "x": fx_, "y": fy_, "t": "Cabo Frio", "c": GOLD, "in": tl, "lx": 18, "ly": -6},
            {"k": "pin", "x": kx_, "y": ky_, "t": "Cananéia", "c": GOLD, "in": tl + .6, "a": "end", "lx": -18, "ly": -14}]
    curve = [v.p(lo, la) for lo, la in [(-47.93, -25.01), (-46.0, -27.6), (-41.0, -30.6), (-32.0, -32.2), (-20.0, -32.6), (-8.0, -32.0)]]
    els += [ln(curve, tg - .6, LILAC, 4, "claimed", dur=1.6, curve=True), lab(*v.p(-25.0, -36.4), "guesses and reports", tg + .3, LILAC, 32, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def s36():
    """Clue three: a world map in the manner of the Portuguese atlas of 1519 (schematic): an oval world, the known lands round the
    ocean, and a great southern land drawn east from the tip of South America to Asia, closing the sea (dashed: imagined)."""
    tg, t19, tb = T("s36", "great land"), T("s36", "fifteen nineteen"), T("s36", "bends the unknown tip")
    cx, cy, rx, ry = 889, 445, 700, 320
    oval = E(cx, cy, rx, ry, 72)
    els = [gl(889, 450, 760, -1, .18, "lamp"), poly(oval, "#ebdfc4", "#8a6a48", 4, -1, curve=True), poly(oval, "url(#k-speck)", at=-1, curve=True),
           poly(E(cx, cy, rx - 16, ry - 14, 72), "none", "#8a6a48", 1.4, -1, curve=True)]
    for k in range(16):
        a = 2 * math.pi * k / 16
        hit = ray_exit((cx, cy), (math.cos(a), math.sin(a)), E(cx, cy, rx - 18, ry - 16, 72))
        if hit:
            els.append(ln([(cx, cy), hit], -1, RINK if k % 2 else GINK, 1, draw=False, op=.3))
    landc, ink = "#cdb28a", "#5a4330"
    am = [(cx - 560, cy - 250), (cx - 470, cy - 290), (cx - 400, cy - 250), (cx - 430, cy - 170), (cx - 390, cy - 110), (cx - 420, cy - 80), (cx - 360, cy - 40),
          (cx - 300, cy + 10), (cx - 310, cy + 80), (cx - 360, cy + 130), (cx - 400, cy + 170), (cx - 450, cy + 150), (cx - 470, cy + 60), (cx - 520, cy - 10),
          (cx - 470, cy - 90), (cx - 560, cy - 130), (cx - 620, cy - 170)]
    eu = [(cx - 120, cy - 270), (cx - 20, cy - 296), (cx + 90, cy - 280), (cx + 110, cy - 220), (cx + 20, cy - 200), (cx - 60, cy - 190), (cx - 130, cy - 210)]
    af = [(cx - 150, cy - 170), (cx - 30, cy - 175), (cx + 60, cy - 160), (cx + 150, cy - 80), (cx + 130, cy + 10), (cx + 60, cy + 90), (cx + 20, cy + 150),
          (cx - 20, cy + 120), (cx - 60, cy + 30), (cx - 140, cy - 40), (cx - 180, cy - 110)]
    asia = [(cx + 130, cy - 280), (cx + 360, cy - 290), (cx + 560, cy - 230), (cx + 640, cy - 120), (cx + 600, cy - 30), (cx + 520, cy + 10), (cx + 430, cy - 20),
            (cx + 360, cy + 60), (cx + 320, cy - 10), (cx + 240, cy - 40), (cx + 160, cy - 150), (cx + 120, cy - 210)]
    els += [poly(am, landc, ink, 2, -1, curve=True), poly(eu, landc, ink, 2, -1, curve=True), poly(af, landc, ink, 2, -1, curve=True), poly(asia, landc, ink, 2, -1, curve=True)]
    south = [(cx - 400, cy + 170), (cx - 300, cy + 200), (cx - 150, cy + 190), (cx, cy + 200), (cx + 150, cy + 190), (cx + 300, cy + 160), (cx + 430, cy + 110),
             (cx + 540, cy + 60), (cx + 600, cy - 20), (cx + 650, cy + 60), (cx + 600, cy + 160), (cx + 420, cy + 250), (cx + 150, cy + 296), (cx - 150, cy + 300),
             (cx - 380, cy + 270), (cx - 470, cy + 220)]
    els += drawn(south, "rgba(205,178,138,.75)", ink, 2.4, tb, 2.0, curve=True, style="inferred") + [
            poly(south, "url(#k-hatch)", at=tb + 1.2, curve=True, op=.5), gl(cx, cy + 240, 300, tb + 1.2, .3, "lamp")]
    els += [lab(cx + 60, cy + 258, "a great southern land", tg, "#4a2e1a", 32, st="ital", halo=False)]
    els += chip(1450, 150, "a Portuguese map, 1519", GOLD, t19, 26)
    els += [lab(cx - 20, cy - 10, "Africa", .5, "#4a2e1a", 24, st="small", halo=False), lab(cx - 470, cy - 30, "Americas", .5, "#4a2e1a", 24, st="small", halo=False),
            lab(cx + 400, cy - 150, "Asia", .5, "#4a2e1a", 24, st="small", halo=False)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s38():
    """The jigsaw: a board with one hole; a piece too big for it; scissors trim it along a dashed line; the trimmed piece drops in."""
    tt, tm = T("s38", "trim any piece"), T("s38", "will match")
    x0, y0, s = 520, 220, 150
    els = [gl(889, 460, 640, -1, .25, "lamp"), rect(x0 - 20, y0 - 20, 4 * s + 40, 3 * s + 40, WOOD_D, "#8a6a48", 2, 8, -1)]
    cols = ["#b98d5c", "#a87b4f", "#c49a68", "#9c7146"]
    for i in range(4):
        for j in range(3):
            if (i, j) == (2, 1):
                els += [rect(x0 + i * s + 3, y0 + j * s + 3, s - 6, s - 6, "#120e0a", "rgba(255,226,190,.3)", 1.5, 6, -1)]
                continue
            els += [rect(x0 + i * s + 3, y0 + j * s + 3, s - 6, s - 6, cols[(i + j) % 4], "rgba(40,26,14,.8)", 1.5, 6, -1),
                    circ(x0 + i * s + s / 2, y0 + j * s + 3, 16, cols[(i + 2 * j) % 4], "rgba(40,26,14,.8)", 1.5, -1)]
    hx, hy = x0 + 2 * s, y0 + s
    big = (hx - 20, 120, s + 60, s + 30)
    els += [rect(big[0], big[1], big[2], big[3], "#d6a96c", "#5a3a22", 2, 8, .5, fx="pop"), circ(big[0] + big[2] / 2, big[1], 18, "#d6a96c", "#5a3a22", 2, .5, fx="pop")]
    els += [rect(big[0] + 26, big[1] + 14, s - 6, s - 6, "none", RED, 3, 6, tt, style="inferred", fx="draw", dur=1.0)]
    els += scissors(big[0] + big[2] + 50, big[1] + 60, 1.4, tt + .2, BONE)
    els += [rect(hx + 3, hy + 3, s - 6, s - 6, "#d6a96c", "#5a3a22", 2, 6, tm, fx="pop"), gl(hx + s / 2, hy + s / 2, 140, tm, .45, "lamp")]
    els += [lab(1320, 380, "trim to fit?", tt + .6, LILAC, 34, "start", st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · Beneath the ice
def sloop(x, y, s, at, c="#2a2a30", sail="#eef2f4", face=1, fx=None):
    """A three-masted sailing ship of 1820 in side view; y = waterline, s = length."""
    f = face
    X = lambda a: x + f * a * s
    out = [poly([[X(-.5), y - .1 * s], [X(.5), y - .12 * s], [X(.42), y + .04 * s], [X(-.42), y + .04 * s]], c, "rgba(255,255,255,.3)", 1, at, fx=fx),
           ln([[X(.5), y - .12 * s], [X(.7), y - .2 * s]], at, c, max(1.5, .012 * s), draw=False)]
    for k, (mx, mh) in enumerate(((-.28, .62), (.02, .78), (.3, .6))):
        out.append(ln([[X(mx), y - .1 * s], [X(mx), y - mh * s]], at, c, max(1.5, .014 * s), draw=False))
        for j in range(3):
            top = y - (mh - .06 - j * .17) * s
            out.append(poly([[X(mx - .1), top], [X(mx + .1), top], [X(mx + .11), top + .14 * s], [X(mx - .11), top + .14 * s]], sail, "rgba(60,60,70,.5)", 1, at, fx=fx))
    return out


def s39():
    """January 1820: two Russian sloops under sail before a long low wall of ice on the horizon: Queen Maud Land, first seen."""
    tj, tb, tq, ti = T("s39", "January"), T("s39", "Bellingshausen"), T("s39", "Queen Maud Land"), T("s39", "What they saw was ice")
    sea_y = 560
    els = [{"k": "water", "y": sea_y, "h": 500, "op": .95, "in": -1}]
    wall = [(470, sea_y + 2), (480, sea_y - 52), (700, sea_y - 56), (980, sea_y - 50), (1250, sea_y - 58), (1520, sea_y - 52), (1700, sea_y - 55), (1780, sea_y - 52), (1780, sea_y + 2)]
    els += [poly(wall, ICE, "#ffffff", 1.4, -1), poly([(480, sea_y - 52), (1780, sea_y - 52), (1780, sea_y - 44), (480, sea_y - 44)], "#ffffff", at=-1, op=.6)]
    els += [ln([(520 + 46 * k, sea_y - 46), (522 + 46 * k, sea_y)], -1, ICE_S, 1.2, draw=False, op=.5) for k in range(28)]
    els += [poly([(470, sea_y + 2), (1780, sea_y + 2), (1780, sea_y + 16), (470, sea_y + 12)], ICE_S, at=-1, op=.4)]
    els += sloop(300, sea_y + 90, 230, -1) + sloop(620, sea_y + 70, 170, .3)
    els += [lab(300, sea_y + 160, "Vostok", .8, DIM, 26), lab(620, sea_y + 130, "Mirny", 1.0, DIM, 26)]
    els += chip(330, 190, "January 1820", GOLD, tj, 30) + [lab(330, 262, "Bellingshausen", tb, BONE, 30)]
    els += [lab(1130, sea_y - 120, "Queen Maud Land", tq, ICE, 36, st="serif"), gl(1130, sea_y - 30, 520, ti, .35, "lamp"), lab(1130, sea_y - 74, "ice", ti + .3, "#ffffff", 30, st="ital")]
    return {"base": "sky", "tod": "dusk", "ground": 1300, "sun": [1600, 470, 26], "cam": CAM, "els": els}


SEA_Y = 470


def s40():
    """The margin of Queen Maud Land in section (heights exaggerated): the ice cliff over the sea, the ice sheet rising to a plateau, the
    rock below, partly under sea level; a sledge sends radar and sound down to the rock, as an ultrasound looks inside a body."""
    tw, tp, tu, tr, tus = T("s40", "wall of ice"), T("s40", "plateau"), T("s40", "underneath"), T("s40", "radar"), T("s40", "ultrasound")
    els = ice_section(-1, SEA_Y)
    els += [ln([(80, SEA_Y), (1700, SEA_Y)], -1, "#9fd0ff", 1.4, "inferred", op=.5), lab(96, SEA_Y - 12, "sea level", .3, "#9fd0ff", 24, "start", st="small")]
    els += [lab(400, SEA_Y - 150, "ice wall", tw, BONE, 30, "start"), lab(400, SEA_Y - 116, "20 to 30 m high", tw + .3, DIM, 26, "start"), leader(400, SEA_Y - 108, 364, SEA_Y - 36, tw)]
    els += [lab(1480, 168, "high plateau", tp, BONE, 30)]
    els += qmark(1050, 760, tu, 70, LILAC, halo=False)
    sx, sy = 1150, 262
    els += [rect(sx - 26, sy - 14, 52, 12, "#6b4a30", at=tr - .3, fx="pop")] + figure(sx + 34, sy, 40, tr - .3, "#c0392b", kind="tunic")
    els += [{"k": "fan", "x": sx, "y": sy, "a0": 62, "a1": 118, "r": 430, "n": 11, "c": "#2f6f92", "in": tr, "fx": "fade", "dur": 1.0}]
    els += [lab(sx + 60, sy + 140, "radar and sound", tr + .4, "#9fd0ff", 28, "start")]
    ux, uy = 250, 230
    els += [poly(E(ux, uy + 40, 110, 50, 24)[12:] + [(ux - 110, uy + 40)], "#c9a48a", "#e8cdb6", 1.5, tus, curve=True, fx="pop"),
            rect(ux - 12, uy - 54, 24, 56, "#d9dde2", "#8a8f96", 1.2, 8, tus, fx="pop"),
            {"k": "fan", "x": ux, "y": uy + 2, "a0": 65, "a1": 115, "r": 80, "n": 7, "c": BLUE, "in": tus + .2},
            lab(ux, uy - 76, "like an ultrasound", tus + .3, DIM, 24, st="small")]
    els += [lab(1690, 790, "heights exaggerated", .6, DIM, 24, "end", st="small")]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


def antarctica_ice(pol, at=-1, fill=ICE, edge=ICE_D):
    rings = antarctica_rings(pol, tol=1.6)
    return [poly(rings[0], fill, edge, 1.6, at)] + [poly(r, fill, edge, 1.2, at) for r in rings[1:10]], rings[0]


def s41():
    """Bedmap2 (2013): Antarctica criss-crossed by survey lines (25 million measurements); a column of ice about 2 km high beside the
    Eiffel Tower; 100 squares of the rock under the grounded ice, 45 of them sea blue: below sea level."""
    tsc, t25, t2, th = T("s41", "scientists brought"), T("s41", "twenty-five million"), T("s41", "two kilometres"), T("s41", "almost half")
    pol = Polar(450, 470, 300, -60)
    ice, ring = antarctica_ice(pol, -1)
    els = [gl(450, 470, 380, -1, .18, "lamp")] + ice
    rr = random.Random(21)
    cx, cy, R = 450, 470, 260
    for k in range(34):
        a = rr.uniform(0, math.pi)
        o = rr.uniform(-R * .8, R * .8)
        dx, dy = math.cos(a), math.sin(a)
        px, py = cx - dy * o, cy + dx * o
        half = math.sqrt(max(0, R * R - o * o))
        els.append(ln([(px - dx * half, py - dy * half), (px + dx * half, py + dy * half)], tsc + .07 * k, BLUE, 1.3, dur=.6, op=.55))
    els += [lab(450, 808 - 40, "25 million measurements", t25, BLUE, 30)] + chip(450, 150, "Bedmap2, 2013", GOLD, tsc, 28)
    # a column of ice to scale beside the Eiffel Tower (0.2 units per metre)
    base = 700
    els += [rect(900, base - 400, 90, 400, ICE, "#ffffff", 1.5, 2, t2, fx="fill", dur=1.4), lab(945, base - 420, "about 2 km", t2 + .4, ICE, 30)]
    tx = 1040
    tower = [(tx - 14, base), (tx - 4, base - 40), (tx - 1, base - 66), (tx + 1, base - 66), (tx + 4, base - 40), (tx + 14, base)]
    els += [poly(tower, "#c9a46a", "#8a6a48", 1, t2 + .8, fx="pop"), lab(tx + 22, base - 20, "Eiffel Tower", t2 + 1.0, DIM, 24, "start", st="small"),
            ln([(860, base), (1100, base)], t2, "#8a7a6a", 2, draw=False)]
    gx, gy, c = 1250, 260, 40
    order = list(range(100))
    random.Random(3).shuffle(order)
    blue = set(order[:45])
    for k in range(100):
        i, j = k % 10, k // 10
        els.append(rect(gx + i * c + 2, gy + j * c + 2, c - 4, c - 4, ROCK, "#8a7a6a", 1, 3, -1 if k not in blue else -1))
    for n, k in enumerate(sorted(blue)):
        i, j = k % 10, k // 10
        els.append(rect(gx + i * c + 2, gy + j * c + 2, c - 4, c - 4, "#3f86a8", "#9fd0ff", 1, 3, th + .02 * n, fx="pop"))
    els += [lab(gx + 200, gy - 24, "the rock beneath", .4, DIM, 24, st="small"), lab(gx + 200, gy + 10 * c + 48, "below sea level", th + 1.0, "#9fd0ff", 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def XL(t):
    return round(160 + (math.log10(t) - 2) / 6 * 1460, 1)


def s43():
    """When was this coast last free of ice? A log timeline of years ago (100 to 100 million): 'thousands' struck through in red,
    then a band of ice blue from millions of years ago."""
    tth, tmi = T("s43", "Not thousands"), T("s43", "Millions")
    y = 560
    ticks = [(XL(10 ** k), lbl) for k, lbl in zip(range(2, 9), ("100", "1,000", "10,000", "100,000", "1 million", "10 million", "100 million"))]
    els = [gl(889, 470, 640, -1, .14, "lamp"), axis(160, 1620, y, ticks, -1, "years ago")]
    x5 = XL(513)
    els += [dot(x5, y, 9, GOLD, .3), lab(x5, y - 28, "1513", .4, GOLD, 26)]
    a, b = XL(1000), XL(10000)
    els += bracket(a, b, y - 90, tth, "thousands of years?", LILAC, up=False, size=30, ty=y - 116, style="claimed") + [strike(a - 10, y - 150, b + 10, y - 70, tth + 1.0, RED, 5)]
    m1, m34 = XL(1e6), XL(3.4e7)
    els += [{"k": "band", "x0": m1, "x1": m34, "y": y - 110, "h": 40, "c": ICE, "op": .85, "in": tmi, "dur": 1.2}, gl((m1 + m34) / 2, y - 90, 260, tmi + .3, .35, "lamp"),
            lab((m1 + m34) / 2, y - 140, "millions of years", tmi + .4, ICE, 34, st="serif")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s44():
    """The EPICA core at Kohnen station, Queen Maud Land: a tall core of thin layers like the pages of a diary, reaching ice 150,000 years
    old at 2,417 m; the record unbroken."""
    td, tp, tn = T("s44", "drilled more than"), T("s44", "pages in a diary"), T("s44", "unbroken")
    top, k_ = 200, .2
    y = lambda m: top + m * k_
    x0, x1 = 600, 1560
    els = [poly([(x0, top + 8), (889, top - 10), (1200, top - 6), (x1, top + 6), (x1, 800), (x0, 800)], ICE, "#ffffff", 1.4, -1),
           poly([(x0, top + 8), (x1, top + 6), (x1, 800), (x0, 800)], "url(#k-speck)", at=-1),
           poly([(x0, 770), (700, 760), (800, 772), (950, 756), (1100, 768), (1250, 752), (1400, 766), (x1, 758), (x1, 820), (x0, 820)], ROCK, "#8a7a6a", 1.4, -1)]
    els += [ln([(x0, y(m)), (x1, y(m) + 4)], -1, ICE_S, 1, draw=False, op=.35) for m in range(300, 2900, 300)]
    els += [rect(860, top - 34, 60, 34, "#c0392b", "#7a2a20", 1.5, 3, -1), poly([(856, top - 34), (890, top - 58), (924, top - 34)], "#e05a48", at=-1),
            lab(940, top - 12, "Kohnen station", .3, BONE, 28, "start")]
    els += [rect(872, top, 36, 0.2 * 2774, "rgba(185,210,226,.5)", "#8fb3cc", 1.5, 3, td, fx="fill", dur=1.6)]
    m = 6.0
    while m < 2417:
        els.append(ln([(874, y(m)), (906, y(m))], tp + .9 * (m / 2417), "#5a7a94", 1.2, draw=False, op=.8))
        m += max(14.0, 24 - m / 160)
    for mm, t in ((1000, "1,000 m"), (2000, "2,000 m")):
        els += [ln([(930, y(mm)), (960, y(mm))], td + .3, BONE, 2, draw=False), lab(970, y(mm) + 8, t, td + .4, "#4a6a84", 24, "start", halo=False)]
    els += [ln([(840, y(2417)), (1000, y(2417))], tn - .4, GOLD, 4, dur=.5), gl(890, y(2417), 120, tn - .2, .6, "lamp"),
            lab(1010, y(2417) + 10, "150,000 years", tn - .2, GOLD, 32, "start"), lab(1010, y(2417) + 44, "at 2,417 m", tn, DIM, 24, "start", halo=False), lab(850, 520, "unbroken", tn, "#4a6a84", 34, "end", st="ital", halo=False)]
    bk, lp, rp = open_book(330, 360, 120, 150, tp, fx="pop")
    els += bk + [ln([(lp[0], lp[1] + 18 * k), (lp[0] + lp[2], lp[1] + 18 * k)], tp + .1, "#8a7a6a", 1.2, draw=False, op=.7) for k in range(6)]
    els += [lab(330, 580, "pages in a diary", tp + .3, DIM, 28, st="ital")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def foram(x, y, s, at):
    out = []
    for k in range(7):
        a = k * .9
        r = s * (.32 + .1 * k)
        out.append(circ(x + r * math.cos(a), y + r * math.sin(a), s * (.18 + .05 * k), "#efe6d2", "#8a7a66", 1.2, at + .03 * k, fx="pop"))
    return out


def s45():
    """Sea-floor mud: a core lying across, banded; tiny shells magnified; above, the curve of ice through time, rising in a step about
    34 million years ago."""
    tm, ts, t34 = T("s45", "mud on the ocean floor"), T("s45", "tiny shells"), T("s45", "thirty-four million")
    els = [gl(889, 420, 700, -1, .15, "lamp")]
    cols = ["#6b5640", "#7d6648", "#5e4a38", "#8a7354", "#6f5a44"]
    for k in range(30):
        x = 160 + 48.6 * k
        els.append(rect(x, 700, 49, 64, cols[k % 5], "none", 0, 0, -1))
    els += [rect(160, 700, 1458, 64, "none", "#cbb79a", 2, 30, -1), lab(160, 800, "sea-floor mud", tm, BONE, 28, "start")]
    mx, my = 330, 470
    els += [circ(mx, my, 100, "rgba(20,30,40,.6)", "#cbbca8", 3, ts, fx="pop"), ln([(mx + 40, my + 92), (400, 700)], ts, "#cbbca8", 2, dur=.4)]
    els += foram(mx - 40, my - 20, 34, ts + .2) + foram(mx + 38, my + 30, 26, ts + .3) + [lab(mx, my - 118, "tiny shells", ts + .4, BONE, 28)]
    X = lambda ma: round(1620 - ma / 60 * 1060, 1)
    els += [axis(560, 1620, 560, [(X(60), "60"), (X(40), "40"), (X(20), "20"), (X(0), "0")], -1), lab(X(30), 650, "million years ago", -1, DIM, 24, st="small")]
    pts = [(X(60), 520), (X(50), 524), (X(40), 516), (X(35), 518), (X(34), 470), (X(33.5), 420), (X(28), 410), (X(20), 404), (X(16), 420), (X(14), 380), (X(8), 370),
           (X(3), 350), (X(0), 330)]
    els += [ln(pts, tm + .6, ICE, 4, dur=2.4, curve=True), lab(X(60) + 10, 500, "little ice", tm + .6, DIM, 24, "start", st="small"),
            ln([(X(34), 560), (X(34), 300)], t34, GOLD, 2, "inferred", dur=.6), gl(X(34), 440, 160, t34, .4, "lamp"),
            lab(X(34) + 16, 290, "ice sheets begin", t34 + .2, GOLD, 30, "start"), lab(X(34), 606, "34", t34 + .2, GOLD, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s46():
    """A football pitch, 100 m, for 34 million years: our species fills the last 0.9 m; magnified, the last metre; and the five centuries
    since 1513, about 1.5 mm, the thickness of a coin."""
    tp, tsp, tc = T("s46", "football pitch"), T("s46", "Our whole species"), T("s46", "thickness of a coin")
    x0, x1, y = 130, 1650, 690
    m = (x1 - x0) / 100.0
    els = [rect(x0 - 20, y - 6, x1 - x0 + 40, 40, "#2f5a2f", "#6aa06a", 1.5, 3, -1), ln([((x0 + x1) / 2, y - 6), ((x0 + x1) / 2, y + 34)], -1, "#e8f0e8", 2, draw=False),
           rect(x0 - 6, y - 52, 8, 46, "none", "#e8f0e8", 3, 1, -1), rect(x1 - 2, y - 52, 8, 46, "none", "#e8f0e8", 3, 1, -1)]
    els += [ln([(x0, y - 70), (x1, y - 70)], tp, ICE, 16, dur=2.0), lab((x0 + x1) / 2, y - 96, "34 million years", tp + .6, ICE, 30),
            lab(x0, y + 74, "0 m", -1, DIM, 24, st="small"), lab(x1, y + 74, "100 m", -1, DIM, 24, st="small")]
    sp = .9 * m
    els += [ln([(x1 - sp, y - 70), (x1, y - 70)], tsp, AMBER, 16, dur=.4)] + man(x1 - 8, y - 6, 1.75 * m, tsp, BONE)
    # magnified: the last metre (circle), and in it a coin seen edge on (1.5 mm)
    cx, cy, R = 1260, 330, 170
    els += [circ(cx, cy, R, "rgba(14,12,10,.85)", "#cbbca8", 3, tsp + .3, fx="pop"), ln([(x1 - m, y - 80), (cx - R * .7, cy + R * .7)], tsp + .3, "#cbbca8", 1.6, dur=.4),
            ln([(x1, y - 80), (cx + R * .7, cy + R * .7)], tsp + .3, "#cbbca8", 1.6, dur=.4)]
    els += [rect(cx - R * .8, cy - 14, R * 1.6 * .1, 28, ICE, at=tsp + .6, fx="pop"), rect(cx - R * .8 + R * 1.6 * .1, cy - 14, R * 1.6 * .9, 28, AMBER, at=tsp + .7, fx="pop"),
            lab(cx, cy - 40, "the last metre", tsp + .6, BONE, 26), lab(cx, cy + 62, "our species", tsp + .9, AMBER, 30)]
    kx, ky = 560, 300
    els += [circ(kx, ky, 120, "rgba(14,12,10,.85)", "#cbbca8", 3, tc - .8, fx="pop"), ln([(cx + R * .8, cy), (kx + 120, ky)], tc - .8, "#cbbca8", 1.6, dur=.4),
            rect(kx - 90, ky - 9, 180, 18, AU, "#8a6a2a", 1.5, 4, tc - .5, fx="pop"), gl(kx, ky, 140, tc - .3, .45, "lamp"),
            lab(kx, ky - 40, "since 1513: 1.5 mm", tc - .4, GOLD, 28), lab(kx, ky + 60, "a coin, edge on", tc, DIM, 24, st="small")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s42():
    """The same section again: the edge of the ice (the cliff, red) and the edge of the rock (where it rises above the sea, gold) far
    apart; then the ice becomes a ghost, the sea floods the low rock, and a dashed new bed rises: the land would rise."""
    te, tr, tf, tu = T("s42", "edge of the ice"), T("s42", "edge of the rock"), T("s42", "freed of all"), T("s42", "slowly rise")
    bed, surf, st, sb = section_parts(SEA_Y)
    els = ice_section(-1, SEA_Y) + [ln([(80, SEA_Y), (1700, SEA_Y)], -1, "#9fd0ff", 1.4, "inferred", op=.5), lab(96, SEA_Y - 12, "sea level", -1, "#9fd0ff", 24, "start", st="small"),
                                    lab(1690, 790, "heights exaggerated", -1, DIM, 24, "end", st="small")]
    rx = 1290
    marks = [ln([(360, SEA_Y - 80), (360, SEA_Y + 40)], te, RED, 4, dur=.4), lab(360, SEA_Y - 94, "edge of the ice", te + .2, RED, 30),
             ln([(rx, SEA_Y - 150), (rx, bed_y(rx, bed))], tr, GOLD, 4, dur=.5), lab(rx, SEA_Y - 164, "edge of the rock", tr + .2, GOLD, 30)]
    grounded = surf + [(1810, bed_y(1810, bed))] + [(x, y) for x, y in reversed(bed) if 700 <= x <= 1810] + [(700, bed_y(700, bed))]
    els += [poly(grounded, "rgba(14,12,10,.82)", at=tf, op=.82), poly(st + sb, "rgba(14,12,10,.82)", at=tf, op=.82),
            poly(grounded, "none", ICE, 2, tf, style="inferred", op=.7), poly(st + sb, "none", ICE, 2, tf, style="inferred", op=.7)]
    low = [(x, y) for x, y in bed if 700 <= x <= rx]
    flood = [(700, SEA_Y)] + [(rx - 40, SEA_Y)] + list(reversed(low))
    els += [poly(flood, "rgba(63,134,168,.55)", "none", 0, tf + .6, fx="fill", dur=1.2)]
    up = [(x, y - 70) for x, y in bed if x >= 700]
    els += [ln(up, tu, AMBER, 3, "inferred", dur=1.4, curve=True)]
    els += [arr([(x, bed_y(x, bed) - 10), (x, bed_y(x, bed) - 60)], tu + .3 + .1 * k, AMBER, 3, dur=.4, curve=False) for k, x in enumerate((900, 1100, 1450, 1600))]
    els += marks + [lab(1560, 660, "the land would rise", tu + .6, AMBER, 32, st="ital")]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


# ================================================================== CHAPTER 6 · The weighing
LROWS = [205, 320, 435, 550]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 48, 1500, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1190, y, grade, gc, gt, 28, "start")
    return out


def pic_map(x, y, at):
    mp, _ = piri_map(x - 26, y - 36, 72, at=at, detail=False, shadow=False, tilt=0)
    return mp


def pic_columbus(x, y, at):
    return [rect(x - 40, y - 30, 50, 40, "none", LILAC, 2, 4, at, style="claimed", fx="pop"), arr([(x + 2, y - 4), (x + 30, y + 14)], at, GOLD, 2.5, dur=.3),
            rect(x + 14, y + 4, 30, 26, PARCH_L, "#8a6a48", 1, 2, at, fx="pop")]


def pic_corner(x, y, at):
    return [poly([(x - 40, y - 34), (x + 40, y - 34), (x + 40, y + 34), (x - 20, y + 34), (x - 40, y + 14)], PARCH, "#7a5a38", 1.5, at, fx="pop"),
            ln([(x - 30, y - 30), (x - 32, y + 4), (x - 12, y + 18), (x + 38, y + 18)], at, LILAC, 3, curve=True, draw=False)]


def pic_ant(x, y, at):
    pol = Polar(x, y, 40, -60)
    ring = antarctica_rings(pol, tol=1.2)[0]
    return [poly(ring, "rgba(201,193,238,.25)", LILAC, 1.5, at, fx="pop")]


def s47():
    """The ledger: drawn in 1513 from about twenty sources (Established); part of a lost Columbus chart (Strong evidence)."""
    t1 = T("s47", "Established")
    t2, g2 = T("s47", "That its Caribbean"), T("s47", "Strong evidence")
    els = [rect(110, 128, 1560, 610, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, -1)]
    els += lrow(0, t1 - .2, pic_map, "1513, from 20 sources", "Established", t1 + .3, GRADE["established"])
    els += lrow(1, t2, pic_columbus, "a lost Columbus chart", "Strong evidence", g2, GRADE["strong"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s48_add():
    """Row 3: what the southern coast was drawn from: Open question."""
    tr, tg = T("s48", "What exactly"), T("s48", "Open question")
    return lrow(2, tr, pic_corner, "the southern coast's source", "Open question", tg, GRADE["open"])


def s49_add():
    """Row 4: Antarctica before the ice: Ruled out, the pictogram struck; three reasons beneath it."""
    tr, tg = T("s49", "And Antarctica"), T("s49", "Ruled out")
    t1, t2, t3 = T("s49", "no sea between"), T("s49", "hot"), T("s49", "millions of years old")
    y = LROWS[3]
    els = lrow(3, tr, pic_ant, "Antarctica before the ice", "Ruled out", tg, GRADE["ruled"]) + [strike(175, y + 34, 255, y - 34, tg + .2, RED, 5)]
    for k, (t, txt) in enumerate(((t1, "no sea between"), (t2, "said to be hot"), (t3, "ice: millions of years"))):
        x = 300 + 440 * k
        els += [dot(x, 668, 7, GRADE["ruled"], t), lab(x + 18, 677, txt, t + .1, BONE, 28, "start")]
    return els


def s50():
    """What would change our minds: a core with one band of open sky in it; an older chart with the real Antarctic coast; an archive shelf
    with a rolled chart: Columbus's lost map."""
    tc, tch, tco = T("s50", "A core of ice"), T("s50", "A chart older"), T("s50", "his lost map")
    els = [gl(889, 450, 760, -1, .18, "lamp")] + [ln([(170 + 520 * k, 700), (530 + 520 * k, 700)], -1, "#5a4836", 3, draw=False, op=.6) for k in range(3)]
    els += [rect(130 + 520 * k + (0 if k else 0), 190, 440, 480, "rgba(201,193,238,.03)", "rgba(201,193,238,.35)", 1.5, 18, -1, style="inferred") for k in range(3)]
    els += [lab(889, 160, "wanted", .3, LILAC, 24, st="cap")]
    cx = 350
    els += [rect(cx - 40, 220, 80, 460, "rgba(201,193,238,.08)", LILAC, 2.5, 30, tc, style="claimed", fx="pop")]
    els += [ln([(cx - 36, 240 + 30 * k), (cx + 36, 240 + 30 * k)], tc + .2, LILAC, 1.2, draw=False, op=.5) for k in range(15)]
    els += [rect(cx - 38, 520, 76, 34, "rgba(159,208,255,.4)", BLUE, 2, 4, tc + .5, fx="pop"), gl(cx, 537, 90, tc + .6, .5, "sun"),
            lab(cx, 740, "open sky, recently?", tc + .7, LILAC, 28)]
    ox, oy = 889, 450
    els += [rect(ox - 190, oy - 200, 380, 400, "rgba(201,193,238,.06)", LILAC, 2.5, 6, tch, style="claimed", fx="pop")]
    pol = Polar(ox, oy + 10, 150, -60)
    ring = antarctica_rings(pol, tol=1.4)[0]
    els += drawn(ring, "rgba(234,243,248,.12)", LILAC, 2, tch + .3, 1.2, style="claimed") + [lab(ox, 740, "an older chart", tch + .5, LILAC, 28)]
    ax_ = 1430
    els += [rect(ax_ - 190, 300, 380, 16, WOOD, "#8a6a48", 1.5, 2, tco - .3), rect(ax_ - 190, 500, 380, 16, WOOD, "#8a6a48", 1.5, 2, tco - .3)]
    els += [rect(ax_ - 120, 420, 240, 70, "rgba(201,193,238,.12)", LILAC, 2.5, 34, tco, style="claimed", fx="pop"),
            ln([(ax_ - 30, 420), (ax_ - 30, 490)], tco + .2, LILAC, 2, draw=False), ln([(ax_ + 30, 420), (ax_ + 30, 490)], tco + .2, LILAC, 2, draw=False),
            lab(ax_, 740, "Columbus's lost map", tco + .4, LILAC, 28)]
    els += [rect(ax_ - 170 + 26 * k, 220, 20, 80, "#4a3a2e", at=-1, op=.6) for k in range(13)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "Some say this", "s2"), (1, "But how could", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(0, "From about {1481", "s6"), (1, "Together they", "s7")], {"chapter": "The admiral and his book"}),
    (1, 1, "collision", "s8", [(1, "It sets off", "s9"), (1, "It notes the", "s10"), (2, "Its second version", "s11")], {}),
    (1, 2, "tag", "s12", [(0, "But his first great", "s13")], {}),
    (2, 0, "world", "s14", [(1, "In {1929", "s15"), (1, "Only a piece", "s16")], {"chapter": "Twenty charts and Columbus"}),
    (2, 1, "collision", "s17", [(1, "About twenty charts", "s18"), (2, "He mixed in", "s19")], {}),
    (2, 2, "reversal", "s20", [(1, "And the map carries", "s21"), (2, "The historian Gregory", "s22")], {}),
    (2, 3, "tag", "s23", [], {}),
    (3, 0, "world", "s24", [(0, "That bottom coast", "s25"), (1, "A history professor", "s26")], {"chapter": "A coast under the ice?"}),
    (3, 1, "collision", "s27", [(1, "The coast, he wrote", "s28")], {}),
    (3, 2, "reversal", "s29", [(1, "He even faced", "s30")], {}),
    (3, 3, "tag", "s31", [], {}),
    (4, 0, "world", "s32", [(0, "No Drake", "s33")], {"chapter": "Why the coast bends"}),
    (4, 1, "collision", "s34", [(1, "Clue two", "s35"), (2, "Clue three", "s36")], {}),
    (4, 2, "reversal", "s37", [], {}),
    (4, 3, "tag", "s38", [], {}),
    (5, 0, "world", "s39", [], {"chapter": "Beneath the ice"}),
    (5, 1, "collision", "s40", [(1, "In {2013", "s41"), (2, "So the edge", "s42")], {}),
    (5, 2, "reversal", "s43", [(1, "In the heart", "s44"), (2, "And mud on", "s45")], {}),
    (5, 3, "tag", "s46", [], {}),
    (6, 0, "weigh", "s47", [(1, "What exactly", "s48"), (2, "And Antarctica, drawn", "s49")], {"chapter": "The weighing"}),
    (6, 1, "test", "s50", [], {}),
    (6, 2, "close", "s51", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1, 889, 500], "s2_add"),
    "s48": ("s47", [1, 889, 500], "s48_add"),
    "s49": ("s47", [1, 889, 500], "s49_add"),
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
    ep = {"id": "lf-piri-reis", "code": "LF.20", "series": script["series"], "title": script["title"], "case": "piri-reis",
          "verdict": "debunked", "claim": "Does a map from 1513 show Antarctica's coast free of ice?", "mood": "mystery",
          "hook_text": "Antarctica, drawn before the *ice*?", "beats": beats, "shots": shots,
          "sources": "Piri Reis 1513 (Topkapı Palace) · McIntosh 2000 · Soucek 1992 · Kahle 1933 (doi:10.2307/209247) · Hapgood 1966, with the Ohlmeyer letter of 1960 · "
                     "Fretwell et al. 2013 (doi:10.5194/tc-7-375-2013) · Ruth et al. 2007 (doi:10.5194/cp-3-475-2007) · DeConto & Pollard 2003 (doi:10.1038/nature01290) · "
                     "Hublin et al. 2017 (doi:10.1038/nature22336)",
          "post": "A map drawn on gazelle skin in 1513 by the Ottoman admiral Piri Reis, and a coast along its bottom that some call Antarctica before the ice. "
                  "His notes, his twenty sources and a lost chart by Columbus; a 1960 Air Force letter and Hapgood's book; the hide, the habits of the age, "
                  "and the real coast beneath the ice of Queen Maud Land, weighed.",
          "hashtags": ["#PiriReis", "#Antarctica", "#Maps", "#Columbus", "#History", "#WeighItYourself"],
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
