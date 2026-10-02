"""LF.17 · Myths That Came True · Vinland: The Vikings Before Columbus (16:9 long film, one wall).

The script is films/long/lf-vinland/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at the
sentence where the picture changes (see BEATS). One scene per script shot (s1..s56; s5, the title, is the intro card over the panel
of s4), drawn while it is said: dusk at the tip of Newfoundland (turf halls, a Norse ship, an axe at a tree), a tree slice stamped by
the Sun, the North Atlantic, Erik's Greenland and the three lands of the sagas, the sagas themselves as illuminated vellum pages,
two books that disagree, eight generations of retelling, Adam of Bremen, the grassy bumps of 1960 and the dig, the plan of the site,
hall F against a tennis court, the pin, the whorl and the smithy, bog iron, boat rivets, women's work, a clock with an hour hand,
fifty-five dates, a door frame, the Sun's burst of 993, three pieces of wood counted to the bark, the circle around the globe, the
butternuts and the map of the Gulf, the meadow's six thousand years, the peoples of the region, the lost other side, the Vinland
Map, a plastic bottle in a grave, the Kensington stone and its 'okay', Point Rosee, the ledger, the tests and the land of grapes.
Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted = claimed (the story is lilac and
dotted throughout; the sagas are ink on vellum).

Facts: the Short 'vinland' (f11.py, rewrite/vinland.json) and the script's facts_added (Kuitems et al. 2021/2022; Miyake et al. 2013;
Mekhaldi et al. 2015; Ledger et al. 2019; Wallace 2003, 2006; Parks Canada; Ingstad & Stine Ingstad 2000; the two sagas; Adam of
Bremen; Yale 2021; Brown & Clark 2002; Williams 2012; Wahlgren 1958; Parcak & Mumford 2017).

Engine workaround (as in lf_troy.py and lf_mkultra.py): the wall only adds elements to a panel on its first visit, at a beat start
or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag,
invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that
step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-vinland/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-vinland/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-vinland RC_FILMS_EPS=/tmp/claude-0/sbx_lf-vinland/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-vinland/boards python3 films.py long.lf_vinland
"""
import json, math, os, random, re
import films
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-vinland", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN, INK = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN, I.INK
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
SEAC = "#3f86a8"
TURF, TURF_D, TURF_L = "#46502e", "#2f3622", "#8a9a5b"          # sod roofs, the dark terrace, grass in the light
WOOD, WOOD_D, WOOD_L = "#5b3d27", "#3a281a", "#c99a68"          # ship timber, its shade, its lit edge
SAIL_R, SAIL_C = "#a8322a", "#e9dcc0"                          # the striped sail
VEL, VEL_E, VEL_D = "#eadcbd", "#b99d72", "#cdb78f"            # vellum, its edge, its shade
IK, IK_R = "#5a4330", "#a8322a"                                # brown ink, red ink
FIRC, FIRC_D = "#1f2a1c", "#141b12"                            # firs at dusk
GRAPE, NUT = "#8e5aa8", "#8c6a48"
SKIN = "#e8d6b8"
GRADE = {"established": "#8fd9b0", "ruled": "#e98a8a", "open": "#f0b06a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # OK: two letters
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
    want = [_norm(p) for p in phrase.replace("-", " ").split() if _norm(p)]
    hits = [i for i in range(len(ws)) if [w for w, _ in ws[i:i + len(want)]] == want]
    assert len(hits) >= k, (sid, phrase, SAY[sid][:200])
    return round(lead + ws[hits[k - 1]][1], 2)


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


def grp(els, at, fx="pop", tr=None, **kw):
    """A group that builds in as one piece (its children have no build-ins of their own); tr = an SVG transform."""
    if tr:
        els = [{"k": "group", "tr": tr, "els": els}]
    e = {"k": "group", "els": els, "in": round(at, 2)}
    if fx:
        e["fx"] = fx
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


def chip(x, y, t, c, at, size=28, a="middle"):
    """A pill with a coloured rim and its words (grades, dates)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


def tick(x, y, at, c=GREEN, s=1.0, w=6):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": w, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cross(x, y, at, c=RED, s=1.0, w=6):
    return [ln([(x - 16 * s, y - 16 * s), (x + 16 * s, y + 16 * s)], at, c, w, dur=.25), ln([(x + 16 * s, y - 16 * s), (x - 16 * s, y + 16 * s)], at + .15, c, w, dur=.25)]


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


def pin(x, y, t, at, c=AMBER, a="start", lx=None, ly=None, st="lab", tc=None):
    e = {"k": "pin", "x": round(x, 1), "y": round(y, 1), "t": t, "c": c, "a": a, "in": round(at, 2), "st": st}
    if lx is not None:
        e["lx"] = lx
    if ly is not None:
        e["ly"] = ly
    if tc:
        e["tc"] = tc
    return e


def mapland(v, at=-1, landc=None, keep=None):
    """The land of a View as one map element; keep(ring) filters the outer rings (lon, lat) first (e.g. no Antarctica)."""
    if keep is None:
        land = v.land()
    else:
        lon0, lon1, lat0, lat1 = v.b
        land = []
        for pl in films._topo():
            r = pl[0]
            if not keep(r):
                continue
            xs = [q[0] for q in r]; ys = [q[1] for q in r]
            if max(xs) < lon0 - 6 or min(xs) > lon1 + 6 or max(ys) < lat0 - 6 or min(ys) > lat1 + 6:
                continue
            pts, last, plo, subs = [], None, None, []
            for lo, la in r:
                if plo is not None and abs(lo - plo) > 180:
                    subs.append(pts); pts, last = [], None
                plo = lo
                q = v.p(lo, la)
                if last and abs(q[0] - last[0]) < 1.2 and abs(q[1] - last[1]) < 1.2:
                    continue
                pts.append(q); last = q
            subs.append(pts)
            d = "".join("M" + "L".join(f"{x} {y}" for x, y in sp) + "Z" for sp in subs if len(sp) > 3)
            if d:
                land.append(d)
    e = {"k": "map", "land": land, "in": at}
    if landc:
        e["landc"] = landc
    return e


def ortho_land(cx, cy, R, lon0, lat0, at=-1, fill="#4a5a3a", edge="rgba(200,220,170,.5)", tol=2.5):
    """The world's land on a globe (orthographic, centred on lon0, lat0) of radius R at (cx, cy); the far side folds onto the rim."""
    p0, l0 = math.radians(lat0), math.radians(lon0)
    out = []
    for pl in films._topo():
        r = pl[0]
        pts, vis, last = [], 0, None
        for lo, la in r:
            p, l = math.radians(la), math.radians(lo)
            x = R * math.cos(p) * math.sin(l - l0)
            y = R * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0))
            c = math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)
            if c < 0:
                d = math.hypot(x, y) or 1
                x, y = x * R / d, y * R / d
            else:
                vis += 1
            q = (cx + x, cy - y)
            if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                continue
            pts.append(q); last = q
        if vis >= 3 and len(pts) >= 4:
            out.append(poly(pts, fill, edge, 1, at))
    return out


# ================================================================== figures
def fig(x, y, h, at, c="#1a1410", arms=None, face=1, fx="rise", op=None, rim=None):
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up' (one arm raised), 'hold' (both forward), 'lift' (both up)."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    sh = (X(0), Y(.77))
    els = [circ(X(.01), Y(.9), .085 * h, c, at=at),
           poly([(X(-.13), Y(.78)), (X(.13), Y(.78)), (X(.11), Y(.44)), (X(-.11), Y(.44))], c, at=at),
           poly([(X(-.11), Y(.46)), (X(.11), Y(.46)), (X(.085), Y(0)), (X(.025), Y(0)), (X(0), Y(.3)), (X(-.025), Y(0)), (X(-.085), Y(0))], c, at=at)]
    aw = max(2.5, .045 * h)
    if arms is None:
        els += [ln([(X(-.12), Y(.76)), (X(-.15), Y(.46))], at, c, aw, draw=False), ln([(X(.12), Y(.76)), (X(.15), Y(.46))], at, c, aw, draw=False)]
    elif arms == "point":
        els += [ln([(X(-.12), Y(.76)), (X(-.15), Y(.46))], at, c, aw, draw=False), ln([(X(.1), Y(.75)), (X(.42), Y(.8))], at, c, aw, draw=False)]
    elif arms == "up":
        els += [ln([(X(-.12), Y(.76)), (X(-.15), Y(.46))], at, c, aw, draw=False), ln([(X(.1), Y(.76)), (X(.2), Y(1.08))], at, c, aw, draw=False)]
    elif arms == "hold":
        els += [ln([(X(-.1), Y(.75)), (X(.22), Y(.56))], at, c, aw, draw=False), ln([(X(.1), Y(.75)), (X(.28), Y(.6))], at, c, aw, draw=False)]
    elif arms == "lift":
        els += [ln([(X(-.1), Y(.76)), (X(-.2), Y(1.06))], at, c, aw, draw=False), ln([(X(.1), Y(.76)), (X(.2), Y(1.06))], at, c, aw, draw=False)]
    if rim:
        els.append(ln([(X(.13), Y(.78)), (X(.11), Y(.44))], at, rim, 1.5, draw=False))
    return [grp(els, at, fx, op=op) if op is not None else grp(els, at, fx)]


def woman(x, y, h, at, c="#1a1410", face=1, fx="rise", baby=False, spin=False):
    """A standing woman in a long dress; baby: a swaddled child in her arms; spin: a drop spindle hanging from her hand."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    els = [circ(X(.01), Y(.9), .085 * h, c, at=at),
           poly([(X(-.11), Y(.78)), (X(.11), Y(.78)), (X(.2), Y(0)), (X(-.2), Y(0))], c, at=at),
           poly([(X(-.04), Y(.97)), (X(-.13), Y(.9)), (X(-.13), Y(.72)), (X(-.06), Y(.78))], c, at=at)]
    aw = max(2.5, .045 * h)
    if baby:
        els += [ln([(X(-.1), Y(.74)), (X(.12), Y(.6))], at, c, aw, draw=False), ln([(X(.1), Y(.74)), (X(.2), Y(.62))], at, c, aw, draw=False)]
    elif spin:
        els += [ln([(X(.1), Y(.76)), (X(.26), Y(.86))], at, c, aw, draw=False), ln([(X(-.1), Y(.76)), (X(.08), Y(.62))], at, c, aw, draw=False),
                ln([(X(.26), Y(.86)), (X(.3), Y(.4))], at, "rgba(233,220,192,.8)", 1.4, draw=False),
                ln([(X(.3), Y(.4)), (X(.3), Y(.2))], at, c, 2.5, draw=False), circ(X(.3), Y(.37), .035 * h, "#8a8a7a", "#e9dcc0", 1, at)]
    else:
        els += [ln([(X(-.1), Y(.76)), (X(-.14), Y(.44))], at, c, aw, draw=False), ln([(X(.1), Y(.76)), (X(.14), Y(.44))], at, c, aw, draw=False)]
    return [grp(els, at, fx)]


def axeman(x, y, h, at, c="#140f0c", rim="rgba(255,190,130,.55)"):
    """A figure mid-swing, facing right, the axe head at (x + .62h, y - .58h)."""
    X = lambda a: x + a * h
    Y = lambda b: y - b * h
    els = [poly([(X(-.16), Y(0)), (X(-.09), Y(0)), (X(.0), Y(.36)), (X(.08), Y(0)), (X(.16), Y(0)), (X(.09), Y(.46)), (X(-.06), Y(.46))], c, at=at),
           poly([(X(-.07), Y(.46)), (X(.1), Y(.46)), (X(.2), Y(.78)), (X(.02), Y(.8))], c, at=at),
           circ(X(.15), Y(.88), .085 * h, c, at=at),
           ln([(X(.16), Y(.74)), (X(.33), Y(.62)), (X(.42), Y(.6))], at, c, .05 * h, draw=False),
           ln([(X(.06), Y(.74)), (X(.26), Y(.64)), (X(.38), Y(.6))], at, c, .05 * h, draw=False),
           ln([(X(.3), Y(.6)), (X(.62), Y(.58))], at, "#4a3424", .028 * h, draw=False),
           poly([(X(.58), Y(.62)), (X(.66), Y(.65)), (X(.68), Y(.53)), (X(.6), Y(.55))], "#7d8590", "#d8dde2", 1, at),
           ln([(X(.2), Y(.78)), (X(.09), Y(.46))], at, rim, 1.6, draw=False)]
    return els


def fir(x, base, h, at=-1, c=FIRC, w=None, op=None, rim=None):
    """A spruce or fir in silhouette: tiers of boughs on a short trunk."""
    w = w or h * .36
    pts = [(x, base - h)]
    n = 7
    for k in range(1, n + 1):
        yy = base - h + h * .9 * k / n
        ww = w / 2 * (k / n) ** .9
        pts.append((x + ww, yy))
        if k < n:
            pts.append((x + ww * .45, yy + 4))
    right = pts[:]
    left = [(2 * x - px, py) for px, py in right[1:]][::-1]
    shape = right + [(x + 5, base - h * .1), (x + 5, base), (x - 5, base), (x - 5, base - h * .1)] + left
    els = [poly(shape, c, "none", 0, at, op=op)]
    if rim:
        els.append(ln(right[:9], at, rim, 1.4, draw=False))
    return els


def hall_side(x0, x1, b, h, at=-1, c=TURF, door=True, smoke=True, op=None, door_at=None):
    """A Norse turf hall in side view: a long low sod mound, a timber gable end at the left with a glowing door, smoke from the roof."""
    pts = [(x0, b), (x0 + 5, b - h * .55), (x0 + 18, b - h * .88), (x0 + 38, b - h), (x1 - 38, b - h), (x1 - 18, b - h * .88), (x1 - 5, b - h * .55), (x1, b)]
    els = [poly(pts, c, "rgba(196,206,150,.32)", 1.2, at, curve=True, op=op),
           ln([(x0 + 20, b - h * .9), (x0 + 40, b - h * .99), (x1 - 40, b - h * .99), (x1 - 20, b - h * .9)], at, "rgba(170,186,120,.45)", 2, draw=False, curve=True),
           poly([(x0 - 2, b), (x0 + 6, b - h * .6), (x0 + 20, b - h * .62), (x0 + 22, b)], WOOD_D, "rgba(255,200,150,.25)", 1, at)]
    for k in (1, 2, 3):
        yy = b - h * .16 * k
        els.append(ln([(x0 + 24, yy), (x1 - 6, yy)], at, "rgba(20,24,12,.45)", 1.4, draw=False))
    if door:
        dh = min(26, h * .5)
        els += [rect(x0 + 7, b - dh, 11, dh, "#ffcf8a", at=door_at if door_at is not None else at, op=.9),
                gl(x0 + 12, b - dh * .5, dh * 1.8, door_at if door_at is not None else at, .55)]
    if smoke:
        mx = x0 + (x1 - x0) * .55
        els.append(ln([(mx, b - h), (mx + 8, b - h - 30), (mx - 4, b - h - 62), (mx + 14, b - h - 96)], at, "rgba(214,204,196,.28)", 7, curve=True, draw=False))
    return els


def ship(cx, wl, L, at=-1, sail=True, fx=None, op=None, refl=True, stripes=6):
    """A Norse ship in side view: clinker hull with curled stem and stern, mast, yard, a square sail in red and cream stripes.
    cx = middle, wl = waterline, L = length (units). Returns elements (static when at < 0)."""
    P = lambda a, b: (cx + a * L, wl + b * L)
    hull = [P(-.5, -.25), P(-.475, -.17), P(-.44, -.08), P(-.37, .012), P(-.2, .036), P(0, .042), P(.2, .036), P(.37, .012), P(.44, -.08), P(.475, -.17),
            P(.5, -.25), P(.465, -.19), P(.42, -.105), P(.3, -.078), P(0, -.07), P(-.3, -.078), P(-.42, -.105), P(-.465, -.19)]
    els = []
    if refl:
        rh = [(x, 2 * wl - y + 4) for x, y in hull]
        els.append(poly(rh, "rgba(20,14,10,.35)", "none", 0, at, curve=True))
    els += [poly(hull, WOOD, WOOD_L, 1.6, at, curve=True),
            ln([P(-.43, -.06), P(-.2, -.025), P(0, -.02), P(.2, -.025), P(.43, -.06)], at, "rgba(233,190,140,.55)", 1.6, curve=True, draw=False),
            ln([P(-.39, -.01), P(-.2, .012), P(0, .016), P(.2, .012), P(.39, -.01)], at, "rgba(233,190,140,.4)", 1.4, curve=True, draw=False),
            circ(*P(-.505, -.262), .018 * L, "none", WOOD_L, 2.2, at), circ(*P(.505, -.262), .018 * L, "none", WOOD_L, 2.2, at)]
    for k in range(7):
        sx = -.34 + k * .1
        els.append(circ(*P(sx, -.088), .011 * L, "#3a2a1e", "rgba(233,190,140,.45)", 1, at))
    if sail:
        mx = cx - .02 * L
        top, bot, hw = wl - .6 * L, wl - .3 * L, .24 * L
        els += [ln([(mx, wl - .07 * L), (mx, wl - .66 * L)], at, WOOD_D, max(3, .011 * L), draw=False),
                ln([(mx, wl - .66 * L), P(-.49, -.24)], at, "rgba(230,210,180,.35)", 1.2, draw=False),
                ln([(mx, wl - .66 * L), P(.49, -.24)], at, "rgba(230,210,180,.35)", 1.2, draw=False)]
        for k in range(stripes):
            a0, a1 = k / stripes, (k + 1) / stripes
            xt0, xt1 = mx - hw + 2 * hw * a0, mx - hw + 2 * hw * a1
            xb0, xb1 = mx - hw * 1.06 + 2 * hw * 1.06 * a0, mx - hw * 1.06 + 2 * hw * 1.06 * a1
            bulge = 6 * math.sin(math.pi * (a0 + a1) / 2)
            els.append(poly([(xt0, top), (xt1, top), (xb1 + 0, bot + bulge), (xb0, bot + bulge)], SAIL_R if k % 2 == 0 else SAIL_C, "none", 0, at))
        els += [ln([(mx - hw - 10, top), (mx + hw + 10, top)], at, WOOD_D, max(3, .01 * L), draw=False),
                ln([(mx - hw * 1.06, bot + 2), (mx + hw * 1.06, bot + 2)], at, "rgba(60,30,20,.6)", 1.5, draw=False)]
    if fx:
        return [grp(els, at, fx)]
    return els


def ship_icon(x, y, s, at, c=AU, fx="pop", sail=True):
    """A small Norse ship pictogram (s = its length)."""
    P = lambda a, b: (x + a * s, y + b * s)
    els = [poly([P(-.5, -.22), P(-.4, .02), P(0, .06), P(.4, .02), P(.5, -.22), P(.38, -.06), P(0, -.04), P(-.38, -.06)], c, "none", 0, at, curve=True)]
    if sail:
        els += [ln([P(0, -.04), P(0, -.62)], at, c, max(1.5, s * .025), draw=False),
                poly([P(-.22, -.58), P(.22, -.58), P(.24, -.18), P(-.24, -.18)], c, "none", 0, at, op=.85)]
    return [grp(els, at, fx)]


def grapes(x, y, s, at, c=GRAPE, fx="pop", style="known", leaf=True):
    """A bunch of grapes (s = height), hanging from (x, y)."""
    els = [ln([(x, y), (x + s * .06, y + s * .14)], at, "#6b8f3a", max(1.5, s * .05), draw=False)]
    if leaf:
        els.append(poly([(x + s * .04, y + s * .08), (x + s * .3, y - s * .04), (x + s * .42, y + s * .14), (x + s * .26, y + s * .26)], "#6b8f3a", "none", 0, at, curve=True))
    rows = [(0, 3), (1, 3), (2, 2), (3, 2), (4, 1)]
    for r, n in rows:
        for j in range(n):
            gx = x + s * .06 + (j - (n - 1) / 2) * s * .2
            gy = y + s * .24 + r * s * .16
            els.append(circ(gx, gy, s * .1, c, "rgba(255,230,255,.35)", 1, at, style=style))
    return [grp(els, at, fx)]


def vellum(x, y, w, h, at=-1, seed=3, fx=None):
    """A sheet of vellum: warm cream, a soft shade, a ragged darker edge."""
    rnd = random.Random(seed)
    n = 18
    top = [(x + w * k / n, y + rnd.uniform(-3, 3)) for k in range(n + 1)]
    rgt = [(x + w + rnd.uniform(-3, 3), y + h * k / 8) for k in range(1, 9)]
    bot = [(x + w * k / n, y + h + rnd.uniform(-3, 3)) for k in range(n, -1, -1)]
    lft = [(x + rnd.uniform(-3, 3), y + h * k / 8) for k in range(7, 0, -1)]
    shape = top + rgt + bot + lft
    els = [rect(x + 10, y + 14, w, h, "#000", at=at, op=.45),
           poly(shape, VEL, VEL_E, 2, at, fx=fx),
           rect(x + 6, y + 6, w - 12, h - 12, "none", "rgba(150,110,70,.25)", 6, 6, at)]
    return els


def initial(x, y, t, at, size=70):
    """A red illuminated initial on a vellum page."""
    return [rect(x - size * .55, y - size * .95, size * 1.1, size * 1.15, "rgba(168,50,42,.12)", IK_R, 2, 4, at),
            lab(x, y, t, at, IK_R, size, st="serif", halo=False)]


def inkfig(x, y, h, at, arms=None, face=1, c=IK, fx="pop"):
    """A figure drawn in brown ink on vellum."""
    return fig(x, y, h, at, c, arms, face, fx)


def inkline(p, at, w=3, c=IK, curve=True, dur=.8, **kw):
    return ln(p, at, c, w, curve=curve, dur=dur, **kw)


def booth(x, y, w, h, at, c=IK):
    """A saga booth (a small tent of turf and cloth) in ink."""
    return [poly([(x - w / 2, y), (x, y - h), (x + w / 2, y)], "rgba(90,67,48,.18)", c, 2.5, at), ln([(x, y - h), (x, y)], at, c, 2, draw=False)]


def nut(x, y, s, at, fx="pop", rot=0):
    """A butternut: oblong, ridged, pointed at one end (s = length)."""
    a = math.radians(rot)
    P = lambda u, v: (x + u * s * math.cos(a) - v * s * math.sin(a), y + u * s * math.sin(a) + v * s * math.cos(a))
    shape = [P(-.5, 0), P(-.4, -.2), P(-.1, -.25), P(.25, -.2), P(.5, 0), P(.25, .2), P(-.1, .25), P(-.4, .2)]
    els = [poly(shape, NUT, "#e9dccb", 1.5, at, curve=True)]
    for v in (-.12, 0, .12):
        els.append(ln([P(-.4, v * .8), P(-.1, v * 1.1), P(.3, v * .8)], at, "#4a3424", 1.5, curve=True, draw=False))
    return [grp(els, at, fx)]


# ================================================================== COLD OPEN
VNA = View(-92, 22, 20, 70, (90, 110, 1600, 700))          # the North Atlantic
LAM = (-55.53, 51.6)
AX_X, AX_Y, AX_H = 1505, 792, 160                         # the axeman's feet and height


def s1():
    """The hero image, complete from the first frame: dusk at the tip of Newfoundland, the bay, a Norse ship at anchor, three turf halls
    on the terrace, firs, and a man cutting a tree; on 'metal blade' the axe glints and a chip flies."""
    tb = T("s1", "metal blade")
    els = [{"k": "water", "y": 616, "h": 260, "x0": -100, "x1": 1900, "op": .94, "in": -1}]
    # the sun's path on the water
    els += [ln([(330 - 60 + 9 * k, 628 + 9 * k), (330 + 40 - 6 * k, 628 + 9 * k)], -1, "rgba(255,214,160,.45)", 2, draw=False) for k in range(7)]
    # the terrace, the shore, the far firs
    terr = [(890, 820), (955, 760), (1030, 712), (1120, 680), (1240, 664), (1420, 658), (1600, 652), (1800, 648), (1800, 820)]
    els += [poly(terr, TURF_D, "none", 0, -1), ln(terr[1:8], -1, "rgba(255,214,160,.4)", 2, draw=False, curve=True),
            ln([(900, 812), (962, 758), (1032, 712)], -1, "rgba(230,214,180,.45)", 3, draw=False)]
    for x, h in ((1640, 170), (1700, 210), (1760, 180), (1590, 120), (1460, 90), (1410, 70)):
        els += fir(x, 658, h, -1, "#18211a", op=.95)
    # three turf halls on the terrace, the far one dimmer
    els += hall_side(1250, 1400, 662, 40, -1, "#3d4628", smoke=True)
    els += hall_side(1040, 1250, 690, 58, -1)
    els += hall_side(1290, 1460, 676, 46, -1, door=False)
    els += [fig(1270, 700, 30, -1, "#120d0a", "point")[0] | {"in": -1}]
    # the ship at anchor, the anchor line
    els += ship(600, 700, 430, -1)
    els += [ln([(803, 694), (850, 730)], -1, "rgba(230,210,180,.35)", 1.4, draw=False)]
    # the foreground: a slope of grass, the fir being cut, the axeman
    fg = [(1330, 820), (1380, 800), (1480, 790), (1600, 786), (1800, 784), (1800, 820)]
    els += [poly(fg, "#1c2316", "none", 0, -1)]
    tx = AX_X + .68 * AX_H - 2
    els += fir(tx + 12, 790, 470, -1, FIRC_D, w=230)
    els += [rect(tx, 630, 24, 160, "#2a1d14", at=-1), poly([(tx, 688), (tx + 16, 698), (tx, 710)], "#e8c89a", "none", 0, -1)]
    els += static(axeman(AX_X, AX_Y, AX_H, -1))
    ax, ay = AX_X + .64 * AX_H, AX_Y - .59 * AX_H
    els += [gl(ax, ay, 70, tb, .95, "lamp"), circ(ax + 2, ay - 2, 5, "#fff6e0", at=tb, fx="pop"),
            poly([(ax - 6, ay - 26), (ax + 10, ay - 30), (ax + 4, ay - 18)], "#e8c89a", "none", 0, tb + .1, fx="pop"),
            poly([(ax - 24, ay - 46), (ax - 12, ay - 52), (ax - 14, ay - 42)], "#d8b88a", "none", 0, tb + .25, fx="pop")]
    els += [gl(1100, 640, 520, -1, .12, "fire")]
    return {"base": "sky", "tod": "dusk", "ground": 876, "groundc": "#141a12", "sun": [330, 600, 24],
            "ridges": [{"y": 612, "a": 9, "c": "#2a2333", "seed": 4}, {"y": 900, "a": 0, "c": "#1a1418", "seed": 2}], "cam": CAM, "els": els}


def s2_add():
    """Close on the cut: clean facets, 'a metal blade'; then 'no local metal tools'."""
    tb, tn = T("s2", "At the time"), T("s2", "no metal tools")
    ax, ay = AX_X + .64 * AX_H, AX_Y - .59 * AX_H
    tx = AX_X + .68 * AX_H - 2
    return [ln([(tx, 690), (tx + 16, 698)], tb, "#fff4dc", 3, dur=.3), ln([(tx, 708), (tx + 16, 699)], tb + .2, "#fff4dc", 3, dur=.3),
            ln([(ax - 30, ay - 40), (1420, 520)], tb + .3, GOLD, 1.6, dur=.4), lab(1410, 510, "a metal blade", tb + .4, GOLD, 32, "end"),
            lab(940, 430, "no local metal tools", tn, BONE, 34, st="ital")]


def s3():
    """A slice of a tree; the Sun's burst marks one ring; the last ring under the bark is 1021; 471 years before Columbus."""
    ts, ty, tc = T("s3", "storm on the Sun"), T("s3", "the year"), T("s3", "Four hundred")
    cx, cy, Rb = 560, 450, 300
    nr, r0, r1 = 40, 22, 284
    sp = (r1 - r0) / nr
    els = [gl(cx, cy, 520, -1, .18, "lamp"), circ(cx, cy, Rb, "#4a3322", "#2a1d14", 3, -1), circ(cx, cy, r1 + 2, "#c9a370", "none", 0, -1)]
    for k in range(nr + 1):
        r = r0 + k * sp
        els.append(circ(cx, cy, r, "none", "#7a5636" if k % 2 else "#8c6a48", 2.6, -1))
    els += [circ(cx, cy, 8, "#7a5636", at=-1)]
    rnd = random.Random(7)
    for k in range(9):
        a = rnd.uniform(0, 2 * math.pi)
        els.append(ln([(cx + 12 * math.cos(a), cy + 12 * math.sin(a)), (cx + (r1 - 6) * math.cos(a), cy + (r1 - 6) * math.sin(a))], -1, "rgba(90,60,35,.35)", 1.2, draw=False))
    r993 = r1 - 28 * sp
    sx, sy = 1400, 250
    els += [gl(sx, sy, 160, -1, .85, "sun"), circ(sx, sy, 34, "#ffe2b4", at=-1),
            gl(sx, sy, 300, ts, .9, "sun")]
    path = [(sx - 40, sy + 20), (1100, 300), (860, 360), (cx + r993 * .82, cy - r993 * .57)]
    els += [arr(path, ts + .2, AU, 4, "known", 1.0)]
    els += [dot(round(1300 - 70 * k, 1), round(270 + 14 * k + 6 * math.sin(k), 1), 4.5, "#fff0c8", round(ts + .15 + .06 * k, 2)) for k in range(7)]
    els += [circ(cx, cy, r993, "none", AU, 6, ts + 1.1, fx="draw", dur=.8), gl(cx + r993 * .82, cy - r993 * .57, 60, ts + 1.2, .8),
            lab(cx + 30, cy - r993 - 18, "993", ts + 1.4, AU, 34, st="serif")]
    els += [circ(cx, cy, r1, "none", GOLD, 6, ty, fx="draw", dur=.9), lab(cx + Rb + 30, cy + 22, "1021", ty + .5, GOLD, 72, "start", st="serif", fx="pop")]
    X = lambda yr: round(1010 + (yr - 1000) * 660 / 500, 1)
    els += [ln([(X(1000), 700), (X(1500), 700)], tc - .2, DIM, 3, dur=.6)]
    els += [circ(X(1021), 700, 10, AU, at=tc, fx="pop"), circ(X(1492), 700, 10, BONE, at=tc + 1.0, fx="pop"),
            arr([(X(1021), 680), ((X(1021) + X(1492)) / 2, 600), (X(1492), 680)], tc + .2, AMBER, 4, dur=1.2),
            lab((X(1021) + X(1492)) / 2, 580, "471 years", tc + .9, AMBER, 40, st="serif"),
            lab(X(1492), 750, "Columbus, 1492", tc + 1.1, BONE, 28, "end")]
    els += ship_icon(X(1021) + 4, 668, 46, tc + .1)
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s4():
    """The North Atlantic: Norway, Iceland, Greenland, Newfoundland; the Norse route and Columbus's; a question; 'Vinland?'."""
    tq, tc, tv = T("s4", "really reach"), T("s4", "Columbus"), T("s4", "Vinland")
    v = VNA
    no, ic, gr, nf = v.p(5.3, 60.4), v.p(-21.9, 64.1), v.p(-45.5, 61.15), v.p(*LAM)
    els = [mapland(v)]
    els += [pin(no[0], no[1], "Norway", -1, BONE, "start", 16, -14), pin(ic[0], ic[1], "Iceland", -1, BONE, "start", 16, -14),
            pin(gr[0], gr[1], "Greenland", -1, BONE, "end", -16, -14), pin(nf[0], nf[1], "Newfoundland", -1, GOLD, "end", -18, 8)]
    route = [no, v.p(-5, 62.5), ic, v.p(-33, 62.5), gr, v.p(-52, 57), nf]
    els += [ln(route, .5, GOLD, 3.5, "inferred", 2.0, True)]
    co = [v.p(-6.9, 37.2), v.p(-15.4, 28.1), v.p(-40, 26), v.p(-74.5, 24.1)]
    els += [ln(co, tc, BONE, 2.5, "inferred", 1.6, True), lab(v.p(-40, 26)[0], v.p(-40, 26)[1] + 46, "Columbus, 1492", tc + .8, BONE, 28)]
    els += qmark(nf[0] + 40, nf[1] - 50, tq, 80)
    vx, vy = v.p(-63.5, 46.2)
    els += [poly(E(vx, vy, 120, 56), "rgba(201,193,238,.12)", LILAC, 2.5, tv, style="claimed", curve=True, fx="draw", dur=.8),
            gl(vx, vy, 140, tv, .4)] + grapes(vx - 20, vy - 34, 52, tv + .3, GRAPE) + [lab(vx - 150, vy + 12, "Vinland?", tv + .4, LILAC, 32, "end")]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== 1. TWO SAGAS, ONE LAND
VGR = View(-56, -12, 58.5, 67.5, (90, 120, 1600, 680))     # Greenland and Iceland
VLD = View(-72, -42, 45.5, 66, (90, 120, 1600, 680))       # west of Greenland: the three lands


def s6():
    """Erik's Greenland: Norse farms in the south-western fjords, his farm at Brattahlid, the crossing from Iceland round Cape Farewell."""
    tf, te = T("s6", "Norse farmers"), T("s6", "Erik the Red")
    v = VGR
    els = [mapland(v)]
    gx, gy = v.p(-42.5, 64.8)
    els += [lab(gx, gy, "Greenland", -1, DIM, 44, st="ital"), lab(*v.p(-18.5, 65.0), "Iceland", -1, DIM, 34, st="ital")]
    route = [v.p(-22.8, 64.5), v.p(-30, 63.4), v.p(-38.5, 60.6), v.p(-43.6, 59.25), v.p(-47.2, 59.9), v.p(-46.6, 60.65)]
    els += [arr(route, .5, GOLD, 3, "inferred", 2.0), lab(*v.p(-31, 62.2), "from Iceland", 1.2, GOLD, 28)]
    farms = [(-45.5, 61.15), (-45.4, 60.99), (-46.05, 60.82), (-45.9, 61.05), (-45.2, 61.3), (-46.3, 61.0), (-44.9, 60.7), (-45.7, 60.6),
             (-47.0, 61.2), (-44.6, 60.35), (-46.6, 60.75), (-50.9, 64.15), (-50.6, 64.3), (-51.2, 64.5), (-50.3, 64.05)]
    for k, (lo, la) in enumerate(farms):
        x, y = v.p(lo, la)
        els.append(circ(x, y, 7, GOLD, "#3a2a1e", 1.5, tf + .07 * k, fx="pop"))
    els += [gl(*v.p(-45.8, 60.95), 110, tf, .45), lab(*v.p(-48.3, 60.75), "Norse farms", tf + .6, GOLD, 30, "end")]
    bx, by = v.p(-45.5, 61.15)
    els += [ln([(bx, by), (bx + 40, by - 80)], te, AU, 2, dur=.4), lab(bx + 46, by - 92, "Erik the Red's farm", te + .2, AU, 30, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def slabs(x, y, at, s=1.0):
    """Flat stones: the slabs of Helluland."""
    P = lambda a, b: (x + a * s, y + b * s)
    return [poly([P(-46, 0), P(-6, -14), P(34, -6), P(-4, 8)], "#9a958c", "#e9e4da", 1.2, at, fx="pop"),
            poly([P(-10, 18), P(34, 4), P(70, 14), P(28, 30)], "#8a857c", "#e9e4da", 1.2, at + .1, fx="pop"),
            poly([P(-60, 26), P(-20, 14), P(6, 26), P(-32, 38)], "#a39d92", "#e9e4da", 1.2, at + .2, fx="pop")]


def forest(x, y, at, n=5, h=54, c="#1f3a24", dx=28):
    out = []
    for k in range(n):
        out += fir(x - (n - 1) * dx / 2 + k * dx, y + (k % 2) * 8, h * (.8 + .2 * (k % 3) / 2), at + .06 * k, c, rim="rgba(180,220,160,.35)")
    for e in out:
        e["fx"] = "rise"
    return out


def s7():
    """Leif sails west: Helluland (flat stones), Markland (forests), Vinland (wine, where it lies unknown)."""
    tl, th, tm, tv = T("s7", "Leif"), T("s7", "Helluland"), T("s7", "Markland"), T("s7", "Vinland")
    v = VLD
    els = [mapland(v)]
    sx, sy = v.p(-50.5, 60.0)
    els += ship_icon(sx, sy, 70, .3) + [lab(sx + 10, sy + 56, "Leif Eriksson", tl, GOLD, 30)]
    route = [v.p(-51.5, 60.6), v.p(-57.5, 63.0), v.p(-62.2, 62.3), v.p(-60.3, 57.5), v.p(-57.6, 54.2), v.p(-55.9, 52.1)]
    els += [ln(route, tl + .3, GOLD, 3.5, "inferred", 2.4, True)]
    hx, hy = v.p(-67.5, 63.6)
    els += slabs(hx, hy, th, 1.5) + [lab(hx, hy - 50, "Helluland", th + .1, BONE, 34)]
    mx, my = v.p(-63.8, 54.6)
    els += forest(mx, my + 30, tm, 6, 84, dx=34) + [lab(mx, my - 76, "Markland", tm + .1, BONE, 34)]
    vx, vy = v.p(-62.3, 47.0)
    els += [ln([v.p(-55.9, 52.1), v.p(-57.6, 49.8), (vx + 40, vy - 60)], tv - .2, LILAC, 3, "claimed", 1.0, True)]
    els += [gl(vx, vy, 130, tv, .35)] + grapes(vx - 16, vy - 56, 92, tv + .2, GRAPE, style="claimed") + [lab(vx - 70, vy + 80, "Vinland?", tv + .3, LILAC, 34, "end")]
    return {"base": "map", "cam": CAM, "els": els}


PAGE = (300, 140, 1180, 640)      # a vellum page: x, y, w, h


def page_frame(at=-1, seed=3, letter="V", rows=2):
    """A saga page: vellum, a red initial, two lines of script, an inked frame round the picture."""
    x, y, w, h = PAGE
    els = vellum(x, y, w, h, at, seed)
    els += initial(x + 80, y + 104, letter, at, 70)
    els += [{"k": "glyphs", "x": x + 140, "y": y + 34, "w": w - 200, "h": 70, "rows": rows, "cols": 16, "kind": "latin", "c": "rgba(90,67,48,.75)", "seed": seed, "in": at}]
    els += [rect(x + 40, y + 140, w - 80, h - 180, "none", IK_R, 2.5, 6, at), rect(x + 50, y + 150, w - 100, h - 200, "none", "rgba(90,67,48,.6)", 1.2, 4, at)]
    for cx_, cy_ in ((x + 40, y + 140), (x + w - 40, y + 140), (x + 40, y + h - 40), (x + w - 40, y + h - 40)):
        els.append(circ(cx_, cy_, 7, IK_R, VEL, 1.5, at))
    return els


GY = PAGE[1] + PAGE[3] - 80        # the ground line inside the page's frame


def vine_tree(x, base, h, at, seed, c=IK):
    """A manuscript tree: an inked trunk, a lobed crown tinted green, a vine climbing it."""
    top = base - h
    els = [inkline([(x, base), (x - 3, base - h * .5), (x + 2, top + 40)], at, 5, curve=True, draw=False)]
    for dx, dy, r in ((-46, 10, 42), (40, 8, 44), (0, -22, 50), (-20, 30, 34), (26, 32, 36)):
        els.append(circ(x + dx, top + dy, r, "rgba(107,143,58,.28)", c, 2.2, at))
    vine = [(x + 10 * math.sin(k * 1.1 + seed), base - k * (h - 50) / 10) for k in range(11)]
    els.append(ln(vine, at, "#4f7a2a", 2.6, curve=True, draw=False))
    for k in (2, 5, 8):
        px, py = vine[k]
        els.append(ln([(px, py), (px + 14, py - 6), (px + 18, py + 4), (px + 10, py + 6)], at, "#4f7a2a", 1.8, curve=True, draw=False))
    return els


def s8():
    """The saga as an illuminated page: a camp at the forest's edge; Tyrkir comes out of the trees with grapes."""
    tt, tg = T("s8", "Tyrkir"), T("s8", "grapes")
    x, y, w, h = PAGE
    gy = GY
    els = page_frame(-1, 3, "V")
    els += [inkline([(x + 60, gy), (x + 600, gy - 4), (x + w - 60, gy)], -1, 3, draw=False)]
    els += booth(x + 140, gy, 100, 92, -1) + booth(x + 255, gy, 86, 78, -1)
    els += [poly([(x + 330, gy), (x + 342, gy - 30), (x + 354, gy)], IK_R, "none", 0, -1), gl(x + 342, gy - 16, 56, -1, .45, "fire")]
    els += static(inkfig(x + 410, gy, 116, -1, None, 1)) + static(inkfig(x + 480, gy, 110, -1, "point", 1))
    trees = [(x + 760, 300), (x + 880, 330), (x + 995, 310), (x + 1080, 290)]
    for k, (tx_, th_) in enumerate(trees):
        els += vine_tree(tx_, gy, th_, -1, k)
    hang = [(x + 735, gy - 250), (x + 905, gy - 268), (x + 970, gy - 230), (x + 1104, gy - 236)]
    for k, (hx, hy) in enumerate(hang):
        els += grapes(hx, hy, 60, -1, GRAPE, leaf=k % 2 == 0)
    els += inkfig(x + 640, gy, 130, tt, "up", -1)
    hx, hy = x + 640 + .2 * 130 * -1, gy - 1.08 * 130
    els += grapes(hx - 16, hy - 8, 58, tt + .2, GRAPE) + [lab(x + 560, gy - 200, "Tyrkir", tt + .3, IK, 34, st="serif", halo=False)]
    for k, (gx_, gy_) in enumerate(hang + [(hx - 12, hy)]):
        els.append(gl(gx_ + 6, gy_ + 40, 56, tg + .1 * k, .6, "lamp"))
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def ink_ship(cx, wl, L, at, fx="rise", load=None, face=1):
    """A Norse ship drawn in ink: an opaque hull, strakes, mast, a striped sail in red hatching; `load`: people and beasts aboard."""
    P = lambda a, b: (cx + face * a * L, wl + b * L)
    hull = [P(-.5, -.25), P(-.44, -.08), P(-.3, .02), P(0, .04), P(.3, .02), P(.44, -.08), P(.5, -.25), P(.42, -.1), P(0, -.07), P(-.42, -.1)]
    els = [ln([P(0, -.07), P(0, -.62)], at, IK, 3, draw=False),
           poly([P(-.22, -.6), P(.22, -.6), P(.24, -.28), P(-.24, -.28)], "#e4c9b0", IK, 2, at)]
    for k in range(1, 6):
        a = -.22 + .088 * k
        els.append(ln([P(a, -.6), P(a * 1.08, -.28)], at, IK_R, 2.4, draw=False))
    if load:
        els += load
    els += [poly(hull, "#d8c39c", IK, 2.5, at, curve=True), ln([P(-.4, -.04), P(0, -.01), P(.4, -.04)], at, IK, 1.5, curve=True, draw=False),
            circ(*P(-.5, -.26), .014 * L, "none", IK, 2, at), circ(*P(.5, -.26), .014 * L, "none", IK, 2, at)]
    return [grp(els, at, fx)]


def cow(x, y, s, at, c=IK):
    """A small beast in ink (cattle), facing right, feet on y."""
    return [poly([(x - s * .5, y - s * .55), (x + s * .35, y - s * .58), (x + s * .4, y - s * .3), (x - s * .5, y - s * .3)], "#cdb48c", c, 2, at),
            poly([(x + s * .32, y - s * .6), (x + s * .58, y - s * .66), (x + s * .6, y - s * .46), (x + s * .38, y - s * .42)], "#cdb48c", c, 2, at),
            ln([(x + s * .4, y - s * .64), (x + s * .46, y - s * .78)], at, c, 2, draw=False)] + \
           [ln([(x + dx * s, y - s * .3), (x + dx * s, y)], at, c, 2, draw=False) for dx in (-.42, -.3, .22, .32)]


def sheep(x, y, s, at, c=IK):
    return [poly(E(x, y - s * .45, s * .42, s * .26), "#f1e6cc", c, 2, at, curve=True), circ(x + s * .45, y - s * .5, s * .12, c, at=at)] + \
           [ln([(x + dx * s, y - s * .25), (x + dx * s, y)], at, c, 2, draw=False) for dx in (-.25, -.1, .12, .26)]


def s9():
    """Karlsefni's ship with people and beasts; Karlsefni and Gudrid on the shore; Snorri in her arms; a bishop's crozier in the margin."""
    tk, tg, ts, tb = T("s9", "Karlsefni"), T("s9", "Gudrid"), T("s9", "Snorri"), T("s9", "bishop")
    x, y, w, h = PAGE
    gy = GY
    els = page_frame(-1, 5, "K")
    for k in range(4):
        yy = gy - 12 - 30 * k
        els.append(inkline([(x + 70, yy), (x + 160, yy - 8), (x + 250, yy), (x + 340, yy - 8), (x + 430, yy), (x + 520, yy - 8), (x + 600, yy)], -1, 1.6, draw=False))
    els += [inkline([(x + 610, gy), (x + 680, gy - 40), (x + 800, gy - 56), (x + w - 60, gy - 60)], -1, 3, draw=False)]
    wl = gy - 50
    load = cow(x + 225, wl - 30, 56, .3) + sheep(x + 310, wl - 28, 48, .3) + [fig(x + 380, wl - 28, 62, .3, IK)[0], fig(x + 420, wl - 28, 58, .3, IK)[0]]
    els += ink_ship(x + 320, wl, 480, .3, "rise", load)
    kx = x + 790
    els += inkfig(kx, gy - 56, 136, tk, "point", 1) + [lab(kx, gy - 56 - 160, "Thorfinn Karlsefni", tk + .2, IK, 30, st="serif", halo=False)]
    wx = x + 960
    els += woman(wx, gy - 58, 126, tg, IK, -1) + [lab(wx, gy + 36, "Gudrid", tg + .2, IK, 30, st="serif", halo=False)]
    bx, by = wx - .12 * 126, gy - 58 - .66 * 126
    els += [poly(E(bx + 2, by, 24, 13), VEL, IK, 2.5, ts, curve=True, fx="pop"), circ(bx - 18, by - 5, 9, VEL, IK, 2, ts, fx="pop"),
            gl(bx - 4, by, 100, ts, .6), lab(wx + 70, by - 10, "Snorri", ts + .2, IK, 30, "start", st="serif", halo=False)]
    mx, my = x + w - 130, y + 190
    els += [ln([(mx, my + 200), (mx, my + 40), (mx + 4, my + 20), (mx + 18, my + 12), (mx + 28, my + 22), (mx + 22, my + 34)], tb, IK_R, 4, curve=True, dur=.6),
            poly([(mx - 66, my + 112), (mx - 68, my + 76), (mx - 56, my + 46), (mx - 41, my + 22), (mx - 26, my + 46), (mx - 14, my + 76), (mx - 16, my + 112)],
                 "rgba(168,50,42,.3)", IK_R, 2.5, tb + .3, fx="pop", curve=True),
            ln([(mx - 41, my + 30), (mx - 41, my + 110)], tb + .3, IK_R, 2, draw=False), ln([(mx - 66, my + 98), (mx - 16, my + 98)], tb + .3, IK_R, 2, draw=False)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def canoe(x, y, L, at, c=IK):
    return [poly([(x - L / 2, y - L * .14), (x - L * .38, y), (x + L * .38, y), (x + L / 2, y - L * .14), (x + L * .3, y - L * .05), (x - L * .3, y - L * .05)],
                 "#d8c39c", c, 2.5, at, curve=True)]


def s10():
    """A shore: Norse with red cloth (their ship behind them), the people of the land with furs, their boats drawn up; the trade; a quarrel;
    the Norse sail away."""
    tt, tf, th = T("s10", "They trade"), T("s10", "Then they"), T("s10", "sail home")
    x, y, w, h = PAGE
    gy = GY
    els = page_frame(-1, 7, "S")
    for k in range(3):
        yy = gy - 10 - 24 * k
        els.append(inkline([(x + 60, yy), (x + 110, yy - 6), (x + 170, yy), (x + 230, yy - 6), (x + 280, yy)], -1, 1.5, draw=False))
    els += [inkline([(x + 280, gy), (x + 700, gy - 6), (x + w - 60, gy)], -1, 3, draw=False)]
    els += static(ink_ship(x + 180, gy - 30, 220, -1, None))
    for k, dx in enumerate((340, 410, 470)):
        els += static(inkfig(x + dx, gy, 112 - 6 * k, -1, "hold" if k == 2 else None, 1))
    els += [rect(x + 494, gy - 74, 54, 24, IK_R, IK, 2, 3, -1)]
    for k, dx in enumerate((760, 830, 900)):
        els += static(inkfig(x + dx, gy, 110 - 4 * k, -1, "hold" if k == 0 else None, -1))
    els += canoe(x + 1010, gy - 2, 190, -1) + canoe(x + 1000, gy - 34, 170, -1)
    els += [poly(E(x + 712, gy - 66, 30, 16), "#6b4a2e", IK, 2, -1, curve=True), poly(E(x + 700, gy - 88, 26, 13), "#7d5a38", IK, 2, -1, curve=True)]
    els += [arr([(x + 700, gy - 250), (x + 615, gy - 290), (x + 530, gy - 250)], tt, IK, 3, dur=.7), lab(x + 615, gy - 305, "furs", tt + .2, IK, 32, st="serif", halo=False),
            arr([(x + 530, gy - 210), (x + 615, gy - 176), (x + 700, gy - 210)], tt + .6, IK_R, 3, dur=.7), lab(x + 615, gy - 140, "red cloth", tt + .8, IK_R, 32, st="serif", halo=False)]
    els += [ln([(x + 616, gy - 118), (x + 600, gy - 90), (x + 632, gy - 64), (x + 598, gy - 36), (x + 622, gy - 6)], tf, IK_R, 5, dur=.5)]
    els += ink_ship(x + 120, gy - 52, 120, th, "rise", face=-1) + [arr([(x + 240, gy - 40), (x + 170, gy - 50)], th + .2, IK, 2.5, "inferred", .5)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


XS = lambda yr: round(200 + (yr - 950) / 500 * 1380, 1)        # the sagas' time line, 950 to 1450 CE


def book(x, y, w, h, at, c=VEL, fx="pop", open_=False):
    if not open_:
        return [grp([rect(x, y, w, h, "#6b3a26", "#c99a68", 2, 4, at), rect(x + 6, y + 6, w - 12, h - 12, "none", "rgba(233,190,140,.5)", 1.5, 3, at)], at, fx)]
    return [grp([poly([(x, y + 10), (x + w / 2, y), (x + w / 2, y + h), (x, y + h + 10)], c, VEL_E, 2, at),
                 poly([(x + w / 2, y), (x + w, y + 10), (x + w, y + h + 10), (x + w / 2, y + h)], c, VEL_E, 2, at),
                 ln([(x + w / 2, y), (x + w / 2, y + h)], at, VEL_E, 2, draw=False)], at, fx)]


def s11():
    """The voyages about 1000 to 1025; the sagas written in the 1200s; about 200 years between; they disagree."""
    tw, td = T("s11", "written down"), T("s11", "don't agree")
    ticks = [(XS(y), str(y)) for y in (1000, 1100, 1200, 1300, 1400)]
    els = [axis(200, 1580, 560, ticks, -1)]
    els += [{"k": "band", "x0": XS(1000), "x1": XS(1025), "y": 470, "h": 22, "c": GOLD, "t": "the voyages", "tc": GOLD, "in": -1}]
    els += [{"k": "band", "x0": XS(1200), "x1": XS(1300), "y": 470, "h": 22, "c": LILAC, "t": "written down", "tc": LILAC, "in": tw, "dur": .8}]
    els += book(XS(1220) - 30, 340, 60, 80, tw + .4) + book(XS(1280) - 30, 340, 60, 80, tw + .6)
    els += bracket(XS(1012), XS(1250), 704, tw + 1.0, "about 200 years", BONE, up=False, size=30, ty=756)
    els += qmark(XS(1250), 320, td, 76)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def coast_page(x0, x1, ytop, ybot, at, side="left"):
    """A coast drawn on a book page: a wavy shoreline down the page edge."""
    xs = x0 + 40 if side == "left" else x1 - 40
    pts = [(xs + 14 * math.sin(k * 1.3) * (1 if side == "left" else -1), ytop + (ybot - ytop) * k / 8) for k in range(9)]
    return [ln(pts, at, IK, 3, curve=True, draw=False)] + [ln([(px - 16 if side == "left" else px + 16, py), (px - 34 if side == "left" else px + 34, py + 10)], at, IK, 1.5, draw=False) for px, py in pts[1:-1:2]]


def curl(x, y, r, at, c=IK, face=1):
    """A curling wind arrow."""
    pts = [(x + face * r * (1 - k / 10) * math.cos(k * .7), y + r * (1 - k / 10) * math.sin(k * .7)) for k in range(11)]
    return [arr(pts[::-1], at, c, 2.5, dur=.6)]


def s12():
    """Two books: in the Greenlanders' saga Bjarni sights the land first and Leif follows; in Erik's saga Leif finds it himself, coming from Norway."""
    tb, tl, te, tn = T("s12", "Bjarni"), T("s12", "Leif follows"), T("s12", "Erik the Red's"), T("s12", "Norway")
    els = []
    for bx, title in ((170, "the Greenlanders"), (960, "Erik the Red's Saga")):
        els += [poly([(bx, 190), (bx + 320, 176), (bx + 320, 520), (bx, 534)], VEL, VEL_E, 2.5, -1),
                poly([(bx + 320, 176), (bx + 640, 190), (bx + 640, 534), (bx + 320, 520)], VEL, VEL_E, 2.5, -1),
                ln([(bx + 320, 176), (bx + 320, 520)], -1, VEL_E, 3, draw=False),
                lab(bx + 320, 154, title, -1, BONE, 32, st="serif")]
        els += coast_page(bx, bx + 320, 210, 500, -1, "left")
    L0 = 170
    els += ink_ship(L0 + 470, 300, 120, tb, "pop") + curl(L0 + 560, 270, 40, tb + .2) + [lab(L0 + 470, 350, "Bjarni", tb + .3, IK, 28, st="serif", halo=False)]
    els += [inkline([(L0 + 410, 300), (L0 + 300, 290), (L0 + 130, 280)], tb + .8, 2, curve=True, dur=.8, style="inferred")]
    els += ink_ship(L0 + 470, 470, 110, tl, "pop") + [inkline([(L0 + 415, 470), (L0 + 280, 450), (L0 + 120, 420)], tl + .3, 2, curve=True, dur=.8, style="inferred"),
                                                      lab(L0 + 560, 476, "Leif", tl + .3, IK, 28, "start", st="serif", halo=False)]
    R0 = 960
    els += [lab(R0 + 600, 250, "Norway", tn, IK, 28, "end", st="serif", halo=False)]
    els += ink_ship(R0 + 470, 380, 130, te, "pop") + curl(R0 + 560, 350, 44, te + .3) + [lab(R0 + 470, 450, "Leif", te + .3, IK, 28, st="serif", halo=False)]
    els += [inkline([(R0 + 590, 270), (R0 + 540, 330), (R0 + 480, 360)], tn, 2, curve=True, dur=.6, style="inferred"),
            inkline([(R0 + 405, 380), (R0 + 280, 375), (R0 + 120, 360)], te + 1.0, 2, curve=True, dur=.8, style="inferred")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def tiny(x, y, at, c=BONE, h=24, style=None):
    """A very small figure for counts."""
    e = person(round(x, 1), round(y, 1), h, round(at, 2), c, "pop")
    if style:
        e["style"] = style
    return e


def s13_add():
    """Sixty-five people under one book, over a hundred under the other."""
    t1, t2 = T("s13", "sixty-five"), T("s13", "The other")
    els = [lab(490, 600, "65", t1, GOLD, 34, st="serif")]
    for k in range(65):
        els.append(tiny(250 + 40 * (k % 13), 650 + 30 * (k // 13), t1 + .015 * k, GOLD, 26))
    els += [lab(1280, 600, "over 100", t2 + .6, AMBER, 34, st="serif")]
    for k in range(100):
        els.append(tiny(1000 + 28 * (k % 20), 650 + 30 * (k // 20), t2 + .01 * k, AMBER, 24))
    els += [rect(1572, 628, 70, 120, "none", AMBER, 2, 8, t2 + 1.1, style="inferred"), lab(1607, 702, "+", t2 + 1.2, AMBER, 44, st="serif")]
    return els


def s14():
    """Eight generations retell the story: the names (gold) stay, the details (lilac) drift."""
    t8, tn, td = T("s14", "eight generations"), T("s14", "names survive"), T("s14", "details drift")
    els = [ln([(170, 712), (1600, 712)], -1, DIM, 2, draw=False)]
    for k in range(8):
        x = 220 + k * 190
        els += fig(x, 700, 120 - 3 * k, -1 if k == 0 else .2 + .12 * k, SKIN if k % 2 == 0 else "#cbbca8", "point" if k < 7 else None, 1, "pop")
        bx, by = x + 34, 430
        els += [rect(bx - 72, by - 66, 150, 116, "rgba(245,236,220,.08)", DIM, 2, 22, .2 + .12 * k, fx="pop"),
                poly([(bx - 46, by + 50), (bx - 24, by + 50), (bx - 40, by + 82)], "rgba(245,236,220,.08)", DIM, 2, .2 + .12 * k, fx="pop")]
        els += ship_icon(bx - 28, by - 4, 56, .3 + .12 * k, AU)
        n = 1 + (k * 3) // 4
        for j in range(min(n, 4)):
            els += grapes(bx + 24 + 14 * j - 6 * min(n, 4), by - 48 + 10 * (j % 2), 26, td + .12 * k, LILAC, style="claimed", leaf=False)
        if k in (3, 4, 5):
            els += ship_icon(bx + 32, by + 32, 30, td + .12 * k, LILAC)
    els += [lab(889, 770, "eight generations", t8, DIM, 30),
            lab(150, 300, "names survive", tn, AU, 32, "start"), ln([(250, 310), (232, 410)], tn + .1, AU, 2, dur=.4),
            lab(1640, 300, "details drift", td + .2, LILAC, 32, "end"), ln([(1560, 310), (1590, 380)], td + .3, LILAC, 2, dur=.4)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def lectern(x, y, h, at, c="#3a2a1e"):
    return [poly([(x - 10, y), (x + 10, y), (x + 6, y - h * .55), (x - 6, y - h * .55)], c, "#8a6a48", 1.5, at),
            poly([(x - 40, y - h * .55), (x + 40, y - h * .55), (x + 30, y - h * .7), (x - 44, y - h * .62)], VEL, VEL_E, 1.5, at)]


def s15_add():
    """On the time line: Adam of Bremen writes about 1075, about 50 years after the voyages; a king beside him; a vine on the page."""
    ta, tk, tv = T("s15", "Adam of"), T("s15", "king of Denmark"), T("s15", "vines")
    x75 = XS(1075)
    els = [ln([(XS(1021), 560), (x75, 560)], ta, AU, 7, dur=.6), circ(x75, 560, 10, AU, at=ta + .5, fx="pop"),
           lab((XS(1021) + x75) / 2, 650, "about 50 years", ta + .6, AU, 28)]
    els += fig(x75 + 40, 390, 120, ta, "#9a8f84", "hold", -1) + lectern(x75 - 30, 390, 120, ta)
    els += [lab(x75 + 20, 230, "Adam of Bremen", ta + .3, BONE, 30)]
    kx = x75 + 210
    els += fig(kx, 390, 124, tk, "#8a7a6a", "point", -1) + [poly([(kx - 14, 266), (kx - 14, 250), (kx - 6, 258), (kx, 246), (kx + 6, 258), (kx + 14, 250), (kx + 14, 266)], AU, at=tk, fx="pop"),
                                                       lab(kx + 26, 230, "king of Denmark", tk + .2, BONE, 28, "start")]
    els += [ln([(x75 - 80, 330), (x75 - 60, 300), (x75 - 76, 270), (x75 - 50, 250)], tv, "#6b8f3a", 3, curve=True, dur=.6)] + grapes(x75 - 56, 252, 40, tv + .3, GRAPE)
    return els


def s16_add():
    """No Norse house beyond Greenland: Greenland's ruins glow; across the sea, nothing found."""
    tr, tn = T("s16", "the story was"), T("s16", "No one had")
    v = VNA
    els = []
    for k, (lo, la) in enumerate(((-45.5, 61.15), (-46.1, 60.8), (-45.0, 60.6), (-50.9, 64.2), (-51.3, 64.5), (-44.6, 60.2))):
        x, y = v.p(lo, la)
        els.append(circ(x, y, 7, GOLD, "#3a2a1e", 1.5, tr + .08 * k, fx="pop"))
    gx, gy = v.p(-50.5, 63.5)
    els += [gl(*v.p(-47, 62), 100, tr, .5), lab(gx - 26, gy - 10, "Norse ruins", tr + .4, GOLD, 30, "end")]
    lx, ly = v.p(-61, 54.5)
    els += [circ(lx, ly, 86, "rgba(245,236,220,.04)", BONE, 2.5, tn, style="inferred", fx="pop"), lab(lx - 96, ly - 4, "nothing found", tn + .4, BONE, 30, "end")]
    return els


# ================================================================== 2. BUMPS IN THE GRASS
VBI = View(-60.5, -52.5, 49.6, 53.2, (90, 120, 1600, 680))   # the Strait of Belle Isle


def s17():
    """1960: a boat comes up the coast of Newfoundland's Great Northern Peninsula to its tip; L'Anse aux Meadows."""
    tb = T("s17", "Benedicte")
    v = VBI
    els = [mapland(v)]
    els += [lab(*v.p(-55.6, 49.95), "Newfoundland", -1, DIM, 40, st="ital"), lab(*v.p(-58.6, 52.75), "Labrador", -1, DIM, 36, st="ital")]
    els += chip(260, 180, "1960", GOLD, .3, 32)
    route = [v.p(-58.3, 49.75), v.p(-57.75, 50.55), v.p(-57.05, 51.15), v.p(-56.45, 51.45), v.p(-55.85, 51.68), v.p(-55.5, 51.66)]
    els += ship_icon(route[0][0], route[0][1] + 6, 46, .2, BONE)
    els += [ln(route, .5, BONE, 3, "inferred", 3.0, True)]
    els += [lab(route[2][0] - 40, route[2][1] - 34, "Helge and Benedicte Ingstad", .9, BONE, 28, "end")]
    lx, ly = v.p(*LAM)
    els += ship_icon(lx - 10, ly - 18, 46, tb - .4, BONE) + [pin(lx, ly, "L'Anse aux Meadows", tb, GOLD, "start", 18, 44), gl(lx, ly, 90, tb, .55)]
    els += [{"k": "scale", "x": 1380, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": -1}]
    return {"base": "map", "cam": CAM, "els": els}


BUMPS = [(930, 640, 250, 46), (1210, 652, 210, 40), (1050, 700, 300, 50)]     # the grassy mounds: centre x, y, length, depth


def s18():
    """The meadow by day: a terrace above a shallow bay, a fishing village on the far shore, grassy bumps and ridges; George Decker leads
    the Ingstads to them; a dashed outline traces the old walls; Ingstad's thought: a large salmon on the line."""
    tr, ts = T("s18", "ridges"), T("s18", "salmon")
    els = [{"k": "water", "y": 566, "h": 320, "x0": -100, "x1": 1900, "op": .9, "in": -1}]
    far = [(-60, 572), (-60, 548), (140, 542), (420, 538), (700, 546), (760, 568)]
    els += [poly(far, "#55684a", "none", 0, -1, curve=True)]
    for k, (hx, hc) in enumerate(((60, "#e9e2d2"), (130, "#c94a3a"), (200, "#e9e2d2"), (300, "#d8cfbd"), (380, "#e9e2d2"))):
        yb = 548 - 2 * (k % 2)
        els += [rect(hx, yb - 22, 34, 22, hc, "rgba(40,30,20,.4)", 1, 2, -1), poly([(hx - 4, yb - 22), (hx + 17, yb - 36), (hx + 38, yb - 22)], "#5a4a3a", at=-1)]
    for cx, cy, rx in ((300, 230, 110), (520, 190, 80), (1180, 250, 130)):
        els += [poly(E(cx, cy, rx, rx * .28, 24), "rgba(255,255,255,.55)", "none", 0, -1, curve=True), poly(E(cx + rx * .3, cy - rx * .12, rx * .55, rx * .22, 20), "rgba(255,255,255,.6)", "none", 0, -1, curve=True)]
    terr = [(500, 880), (540, 660), (620, 612), (800, 594), (1100, 588), (1400, 582), (1800, 576), (1800, 880)]
    els += [poly(terr, "#5f7040", "none", 0, -1), ln(terr[1:7], -1, "rgba(240,248,220,.55)", 2.5, draw=False, curve=True)]
    rnd = random.Random(8)
    for k in range(80):
        x = rnd.uniform(560, 1760); y = rnd.uniform(610, 800)
        els.append(ln([(x, y), (x + rnd.uniform(-3, 3), y - rnd.uniform(6, 12))], -1, "rgba(40,60,20,.5)", 1.4, draw=False))
    for x, y, r in ((700, 760, 16), (1580, 700, 12), (640, 700, 10)):
        els.append(poly(E(x, y, r * 1.4, r, 12), "#8a8a80", "rgba(255,255,255,.3)", 1, -1, curve=True))
    for cx, cy, L, d in BUMPS:
        els += [poly(E(cx, cy, L / 2, d / 2, 28), "#6f8248", "rgba(230,240,200,.45)", 1.5, -1, curve=True),
                poly(E(cx, cy - d * .14, L / 2 - 26, d / 2 - 12, 28), "#80975a", "none", 0, -1, curve=True)]
        els.append(rect(cx - L / 2 + 30, cy - 4, L - 60, 8, "rgba(40,50,20,.4)", at=-1, r=4))
    for cx, cy, L, d in BUMPS:
        els.append(rect(cx - L / 2 + 18, cy - d / 2 + 6, L - 36, d - 12, "none", AU, 2.5, 4, tr, style="inferred"))
    els += fig(1380, 650, 120, -1, "#2a2420", "point", -1, rim="rgba(255,250,230,.5)") + fig(1480, 660, 124, -1, "#2a2420", None, -1) + \
           fig(1540, 664, 104, -1, "#3a3028", None, -1)
    els += [lab(1380, 700, "George Decker", .4, BONE, 30), lab(1515, 712, "the Ingstads", .9, BONE, 30, "start")]
    # Ingstad's thought: as if he had hooked a large salmon
    bx, by = 1490, 380
    els += [circ(1484, 516, 7, "rgba(255,255,255,.85)", at=ts, fx="pop"), circ(1488, 486, 11, "rgba(255,255,255,.85)", at=ts + .1, fx="pop"),
            poly(E(bx, by, 150, 80, 30), "rgba(255,255,255,.88)", "rgba(40,60,80,.5)", 2, ts + .2, fx="pop", curve=True)]
    fx_, fy_ = bx + 10, by + 10
    fish = [(fx_ - 60, fy_ + 6), (fx_ - 20, fy_ - 16), (fx_ + 30, fy_ - 14), (fx_ + 60, fy_), (fx_ + 30, fy_ + 14), (fx_ - 20, fy_ + 16)]
    els += [ln([(fx_ + 58, fy_ - 4), (fx_ + 96, fy_ - 46), (fx_ + 120, fy_ - 70)], ts + .4, "#3a4a5a", 1.6, curve=True, dur=.3),
            poly(fish, "#8fa4b2", "#3a4a5a", 1.5, ts + .4, fx="pop", curve=True),
            poly([(fx_ - 58, fy_ + 4), (fx_ - 86, fy_ - 14), (fx_ - 84, fy_ + 22)], "#7f94a2", "#3a4a5a", 1.5, ts + .4, fx="pop"),
            circ(fx_ + 36, fy_ - 4, 3, INK, at=ts + .4, fx="pop"),
            lab(bx, by - 100, "a large salmon", ts + .5, BONE, 32, st="ital")]
    return {"base": "sky", "tod": "day", "ground": 880, "groundc": "#4a5a32", "sun": [1680, 200, 26],
            "ridges": [{"y": 900, "a": 0, "c": "#3f6f8a", "seed": 4}], "cam": CAM, "els": els}


def s19_add():
    """The dig, 1961 to 1968: a grid of pegs and strings over the mounds, diggers kneeling with trowels, Anne Stine Ingstad with her plan."""
    ta, ty = T("s19", "Anne Stine"), T("s19", "eight years")
    els = []
    for k in range(7):
        x = 760 + 110 * k
        els.append(ln([(x, 604), (x - 20, 760)], ta - .4 + .05 * k, "rgba(255,244,220,.55)", 1.5, dur=.4))
    for k in range(4):
        y = 612 + 40 * k
        els.append(ln([(760 - 5 * k, y), (1420 - 5 * k, y)], ta - .2 + .05 * k, "rgba(255,244,220,.55)", 1.5, dur=.5))
    for k, (x, y) in enumerate(((880, 690), (1000, 650), (1120, 720), (1250, 670))):
        els += [grp([circ(x, y - 30, 9, "#2a2420", at=ta), poly([(x - 14, y - 22), (x + 10, y - 22), (x + 16, y), (x - 20, y)], "#2a2420", at=ta),
                     ln([(x + 8, y - 16), (x + 26, y - 4)], ta, "#2a2420", 4, draw=False), poly([(x + 24, y - 6), (x + 34, y - 2), (x + 28, y + 4)], "#c9c4b8", at=ta)], ta + .15 * k, "rise")]
    els += woman(700, 640, 118, ta, "#2a2420", 1) + [rect(718, 558, 40, 30, VEL, "#6b5a44", 1.5, 2, ta), lab(700, 690, "Anne Stine Ingstad", ta + .3, BONE, 30)]
    for k in range(8):
        els.append(ln([(1020 + 34 * k, 140), (1020 + 34 * k, 196)], ty + .12 * k, AU, 6, dur=.2))
    els += chip(1155, 240, "1961 to 1968", AU, ty + 1.0, 30)
    return els


# the plan of the site (schematic): sea at left, Black Duck Brook, the bog, the terrace with three halls and their huts, the smithy
HALLS = {"F": (800, 170, 288, 156), "D": (820, 382, 204, 116), "A": (790, 560, 232, 140)}
HUTS = {"G": (1112, 206, 62, 52), "E": (1046, 404, 56, 46), "B": (1046, 572, 50, 44), "C": (1046, 646, 56, 50)}
SMITHY = (322, 472, 58, 48)


def s20():
    """The plan of the site, schematic: eight buildings draw themselves (three halls, huts, the smithy across the brook); an inset of a wall:
    sod laid round a wooden frame."""
    tb, tw = T("s20", "eight buildings"), T("s20", "walls of sod")
    sea = [(40, 100), (250, 100), (232, 250), (252, 420), (226, 600), (246, 820), (40, 820)]
    els = [poly(sea, "rgba(63,134,168,.5)", "rgba(159,208,255,.6)", 2, -1, curve=True)]
    brook = [(600, 820), (552, 690), (486, 560), (420, 430), (336, 280), (244, 172)]
    bog = [(455, 300), (540, 410), (612, 560), (676, 700), (700, 800), (622, 800), (560, 640), (480, 470), (404, 330)]
    els += [poly(bog, "rgba(120,128,64,.42)", "rgba(190,200,120,.35)", 1.5, -1, curve=True)]
    rnd = random.Random(2)
    for k in range(26):
        x = rnd.uniform(470, 660); y = rnd.uniform(380, 770)
        if (y - 300) * .45 + 420 < x < (y - 300) * .45 + 520:
            els.append(ln([(x - 6, y), (x, y - 9), (x + 6, y)], -1, "rgba(200,210,140,.55)", 1.4, draw=False))
    els += [ln(brook, -1, "#6fb6d6", 6, curve=True, draw=False), ln([(740, 140), (760, 400), (735, 800)], -1, "rgba(245,236,220,.25)", 2, "inferred", curve=True, draw=False)]
    els += [lab(130, 720, "the sea", -1, "#bfe6f5", 28, st="ital")]
    for x, y, w, h in list(HALLS.values()) + list(HUTS.values()):
        els.append(rect(x + 4, y + 4, w - 8, h - 8, "rgba(120,140,80,.18)", "rgba(200,210,150,.28)", 1.5, 16, -1, style="inferred"))
    for k, (n, (x, y, w, h)) in enumerate(HALLS.items()):
        els.append(rect(x, y, w, h, "rgba(201,163,112,.22)", BONE, 3, 18, tb + .25 * k, fx="draw", dur=.6))
        els.append(ln([(x + w * .35, y + 8), (x + w * .35, y + h - 8)], tb + .25 * k + .3, "rgba(245,236,220,.45)", 1.5, draw=False))
        els.append(ln([(x + w * .7, y + 8), (x + w * .7, y + h - 8)], tb + .25 * k + .3, "rgba(245,236,220,.45)", 1.5, draw=False))
    for k, (n, (x, y, w, h)) in enumerate(HUTS.items()):
        els.append(rect(x, y, w, h, "rgba(201,163,112,.22)", BONE, 2.5, 12, tb + .8 + .12 * k, fx="draw", dur=.4))
    x, y, w, h = SMITHY
    els += [rect(x, y, w, h, "rgba(255,138,90,.25)", "#ff9a6a", 2.5, 12, tb + 1.4, fx="draw", dur=.4), gl(x + w / 2, y + h / 2, 60, tb + 1.5, .7, "fire"),
            lab(x + w / 2, y - 18, "smithy", tb + 1.5, "#ffb48a", 28)]
    els += [lab(905, 752, "eight buildings", tb + .3, BONE, 32), lab(560, 772, "the bog", .4, "#d6dca0", 28)]
    # inset: a wall in section, sod laid round a wooden frame
    ix, iy, iw, ih = 1236, 150, 440, 330
    els += [rect(ix, iy, iw, ih, "rgba(18,13,10,.82)", "rgba(245,236,220,.35)", 2, 14, tw - .2, fx="pop")]
    g = iy + ih - 50
    inset = [ln([(ix + 20, g), (ix + iw - 20, g)], tw, DIM, 2, draw=False)]
    for side in (-1, 1):
        cx = ix + iw / 2 + side * 140
        for j in range(6):
            yy = g - 22 * (j + 1)
            inset.append(rect(cx - 40 + (j % 2) * 6 - (side < 0) * 6, yy, 74, 20, "#5d5a32" if j % 2 else "#6e6a3c", "rgba(30,26,12,.6)", 1, 3, tw))
        inset.append(rect(cx - side * 52 - 7, g - 150, 14, 150, WOOD_L, "#3a281a", 1.2, 2, tw + .3))
    apex = (ix + iw / 2, iy + 46)
    inset += [ln([(ix + iw / 2 - 196, g - 150), apex, (ix + iw / 2 + 196, g - 150)], tw + .5, WOOD_L, 8, dur=.6),
              poly([(ix + iw / 2 - 214, g - 146), (apex[0], apex[1] - 22), (ix + iw / 2 + 214, g - 146), (ix + iw / 2 + 190, g - 136), (apex[0], apex[1] - 2), (ix + iw / 2 - 190, g - 136)],
                   "#5d5a32", "rgba(30,26,12,.6)", 1, tw + .9, fx="pop")]
    els += inset + [lab(ix + iw / 2, iy + ih - 16, "sod on a frame", tw + 1.0, BONE, 28)]
    return {"base": "plan", "cam": CAM, "els": els}


M = 20                                   # units per metre on the scale drawings of hall F (s21, s25)
HF = (160, 230, 28.8 * M, 15.6 * M)      # hall F, 28.8 by 15.6 m


def s21():
    """Hall F to scale beside a tennis court: about 29 m against 24 m; three people, 1.7 m each, for scale."""
    th, tc = T("s21", "biggest hall"), T("s21", "tennis court")
    x, y, w, h = HF
    els = [rect(x, y, w, h, "rgba(201,163,112,.2)", BONE, 3, 26, -1)]
    for fx_ in (.24, .47, .7):
        els.append(ln([(x + w * fx_, y + 10), (x + w * fx_, y + h - 10)], -1, "rgba(245,236,220,.4)", 1.5, draw=False))
    els += [lab(x + w / 2, y + h / 2 + 12, "hall F", -1, BONE, 34, st="serif")]
    els += [{"k": "dim", "x1": x, "y1": y + h + 40, "x2": x + w, "y2": y + h + 40, "t": "about 29 m", "c": GOLD, "fx": "draw", "dur": 1.0, "in": th, "ly": 40}]
    for k in range(3):
        els += [person(x + 44 + 26 * k, y + h - 14, 1.7 * M, th + .6 + .15 * k, SKIN)]
    cw, chh = 23.77 * M, 10.97 * M
    cx, cy = 1040, y + (h - chh) / 2
    court = [rect(cx, cy, cw, chh, "#2f6b4a", "#f5f5f0", 3, 2, tc)]
    sw = 8.23 * M
    for yy in (cy + (chh - sw) / 2, cy + (chh + sw) / 2):
        court.append(ln([(cx, yy), (cx + cw, yy)], tc, "#f5f5f0", 2, draw=False))
    for xx in (cx + cw / 2 - 6.4 * M, cx + cw / 2 + 6.4 * M):
        court.append(ln([(xx, cy + (chh - sw) / 2), (xx, cy + (chh + sw) / 2)], tc, "#f5f5f0", 2, draw=False))
    court += [ln([(cx + cw / 2 - 6.4 * M, cy + chh / 2), (cx + cw / 2 + 6.4 * M, cy + chh / 2)], tc, "#f5f5f0", 2, draw=False),
              ln([(cx + cw / 2, cy - 6), (cx + cw / 2, cy + chh + 6)], tc, "#d8d8d0", 4, draw=False)]
    els += [grp(court, tc, "pop"), lab(cx + cw / 2, cy - 30, "a tennis court", tc + .2, BONE, 30)]
    els += [{"k": "dim", "x1": cx, "y1": y + h + 40, "x2": cx + cw, "y2": y + h + 40, "t": "24 m", "c": "#a8d8b8", "fx": "draw", "dur": .8, "in": tc + .4, "ly": 40}]
    return {"base": "plan", "cam": CAM, "els": els}


def plinth(x, base, w, at):
    return [rect(x - w / 2, base, w, 26, "#3a2e24", "#8a6a48", 1.5, 3, at), rect(x - w / 2 - 14, base + 26, w + 28, 18, "#2a2018", "#6a5240", 1.5, 3, at)]


def s22():
    """Three Norse objects on lit plinths, popping as named: a bronze ring-headed cloak pin, a stone spindle whorl, a smithy with its furnace."""
    tp, tw, ts = T("s22", "bronze cloak"), T("s22", "spindle"), T("s22", "smithy")
    base = 600
    els = []
    for x in (420, 889, 1360):
        els += plinth(x, base, 220, -1) + [gl(x, base - 120, 260, -1, .22, "lamp")]
    px = 420
    els += [grp([ln([(px, base - 12), (px, base - 250)], 0, "#c98a4a", 7, draw=False), ln([(px + 2, base - 20), (px + 2, base - 240)], 0, "#f0c088", 2, draw=False),
                 circ(px, base - 278, 26, "none", "#c98a4a", 7), circ(px, base - 278, 26, "none", "#f0c088", 1.5),
                 poly([(px - 9, base - 256), (px + 9, base - 256), (px + 6, base - 240), (px - 6, base - 240)], "#c98a4a", "#f0c088", 1)], tp, "rise"),
            gl(px, base - 270, 70, tp + .2, .6), lab(px, base + 90, "bronze cloak pin", tp + .2, "#f0c088", 30)]
    wx = 889
    els += [grp([ln([(wx, base - 230), (wx, base - 12)], 0, "#8a6a48", 6, draw=False),
                 poly(E(wx, base - 70, 64, 24), "#7d8a7a", "#d8e0d0", 2, curve=True), poly(E(wx, base - 76, 64, 20), "#94a090", "#d8e0d0", 1.5, curve=True),
                 circ(wx, base - 76, 8, "#3a2e24")], tw, "rise"), lab(wx, base + 90, "spindle whorl", tw + .2, "#d8e0d0", 30)]
    sx = 1360
    hut = hall_side(sx - 110, sx + 110, base, 120, 0, TURF, door=False, smoke=True)
    els += [grp(hut + [rect(sx - 40, base - 64, 80, 64, "#1a110c", "#8a6a48", 1.5, 6), circ(sx, base - 26, 22, "#ff8a4a")], ts, "rise"),
            gl(sx, base - 30, 110, ts + .2, .8, "fire"), lab(sx, base + 90, "smithy", ts + .2, "#ffb48a", 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s23():
    """Bog iron: the bog beside the halls with lumps of ore in the wet peat; like rust in a puddle; roast, smelt with charcoal: iron and slag."""
    tp, tr, ti, ts = T("s23", "rust stains"), T("s23", "Roast it"), T("s23", "out comes"), T("s23", "slag")
    bx, by, bw, bh = 560, 380, 420, 300
    els = [rect(bx, by, bw, bh, "#2c2216", "rgba(245,236,220,.3)", 2, 10, -1)]
    for k, c in enumerate(("#3a2c1c", "#33281a", "#2a2014")):
        els.append(rect(bx + 4, by + 40 + 80 * k, bw - 8, 80, c, at=-1))
    els += [{"k": "water", "y": by + 60, "h": 40, "x0": bx + 4, "x1": bx + bw - 4, "op": .35, "in": -1}]
    rnd = random.Random(5)
    for k in range(16):
        x = rnd.uniform(bx + 24, bx + bw - 24); y = rnd.uniform(by + 110, by + bh - 24)
        els.append(poly(E(x, y, rnd.uniform(10, 18), rnd.uniform(7, 11), 10), "#b8682a", "#e8a060", 1.2, -1, curve=True))
    for k in range(12):
        x = bx + 20 + k * 34
        els.append(ln([(x, by + 40), (x + 4, by + 22), (x + 9, by + 40)], -1, "#8a9a5b", 2, draw=False))
    els += [lab(bx + bw / 2, by - 24, "bog iron", -1, "#e8a060", 32)]
    # like rust in a puddle
    px, py = 250, 560
    els += [poly(E(px, py, 150, 48), "rgba(63,134,168,.6)", "rgba(200,230,245,.6)", 2, tp, fx="pop", curve=True),
            poly(E(px - 30, py - 4, 70, 18), "rgba(200,100,40,.55)", "none", 0, tp + .4, fx="pop", curve=True),
            poly(E(px + 50, py + 10, 46, 12), "rgba(200,100,40,.45)", "none", 0, tp + .6, fx="pop", curve=True),
            lab(px, py + 90, "rust in a puddle", tp + .3, BONE, 28, st="ital")]
    # the furnace: roast, smelt with charcoal
    fx_, fb = 1220, 680
    els += [arr([(bx + bw - 10, by + 150), (1110, 330), (fx_ - 10, 300)], tr, "#e8a060", 3, dur=.6)]
    furn = [poly([(fx_ - 70, fb), (fx_ - 44, fb - 330), (fx_ + 44, fb - 330), (fx_ + 70, fb)], "#8a5a3a", "#d8a070", 2),
            rect(fx_ - 30, fb - 70, 60, 60, "#1a0f0a", "#d8a070", 1.5, 8), circ(fx_, fb - 40, 20, "#ff8a3a")]
    for k in range(9):
        furn.append(circ(fx_ - 28 + 7 * k, fb - 300 + 26 * (k % 3), 7, "#1a1612" if k % 2 else "#b8682a", "none", 0))
    els += [grp(furn, tr + .3, "rise"), gl(fx_, fb - 40, 120, tr + .6, .85, "fire"), lab(fx_, 330, "furnace", tr + .5, "#ffb48a", 30)]
    # out comes iron, and slag
    els += [arr([(fx_ + 74, fb - 30), (1440, fb - 120)], ti, BONE, 3, dur=.4),
            poly([(1440, fb - 150), (1480, fb - 176), (1530, fb - 168), (1556, fb - 140), (1530, fb - 112), (1470, fb - 108)], "#8a8f96", "#e0e4e8", 2, ti + .2, fx="pop", curve=True),
            lab(1500, fb - 200, "iron", ti + .3, "#e0e4e8", 32)]
    els += [arr([(fx_ + 74, fb - 6), (1440, fb + 20)], ts - .2, BONE, 3, dur=.4),
            poly([(1440, fb + 10), (1500, fb - 6), (1560, fb + 6), (1580, fb + 34), (1520, fb + 50), (1456, fb + 40)], "#1e1a24", "#7a6a8a", 2, ts, fx="pop", curve=True),
            lab(1640, fb + 34, "slag", ts + .1, "#b8a8c8", 32, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s24():
    """A few kilograms from one smelting, on a balance; enough to mend a boat: a hull on stocks, rivets cut out; about 100 nails in a tray."""
    tk, tb, tn, tc = T("s24", "few kilograms"), T("s24", "mend a boat"), T("s24", "hundred broken"), T("s24", "cut the way")
    els = []
    bx, by = 260, 470
    els += [grp([rect(bx - 70, by + 150, 140, 16, "#5a4836", "#8c7152", 1.5, 4), ln([(bx, by + 150), (bx, by - 40)], 0, "#8c7152", 8, draw=False),
                 ln([(bx - 120, by - 40), (bx + 120, by - 40)], 0, BONE, 5, draw=False), circ(bx, by - 40, 9, GOLD),
                 ln([(bx - 120, by - 40), (bx - 160, by + 40)], 0, MUTED, 1.5, draw=False), ln([(bx - 120, by - 40), (bx - 80, by + 40)], 0, MUTED, 1.5, draw=False),
                 ln([(bx + 120, by - 40), (bx + 80, by + 40)], 0, MUTED, 1.5, draw=False), ln([(bx + 120, by - 40), (bx + 160, by + 40)], 0, MUTED, 1.5, draw=False),
                 poly([(bx - 170, by + 40), (bx - 70, by + 40), (bx - 84, by + 54), (bx - 156, by + 54)], "#6b5a48", "#cbb79a", 1.5),
                 poly([(bx + 70, by + 40), (bx + 170, by + 40), (bx + 156, by + 54), (bx + 84, by + 54)], "#6b5a48", "#cbb79a", 1.5)], -1, None)]
    els += [poly([(bx - 150, by + 40), (bx - 140, by + 12), (bx - 108, by + 4), (bx - 84, by + 18), (bx - 92, by + 40)], "#8a8f96", "#e0e4e8", 2, tk, fx="pop", curve=True)]
    els += chip(bx, by - 120, "a few kilograms", "#e0e4e8", tk + .3, 28)
    # the hull on stocks, its rivets
    hx, hw, hy = 1060, 760, 400
    hull = [(hx - hw / 2, hy - 120), (hx - hw * .42, hy - 30), (hx - hw * .3, hy + 20), (hx, hy + 36), (hx + hw * .3, hy + 20), (hx + hw * .42, hy - 30), (hx + hw / 2, hy - 120),
            (hx + hw * .4, hy - 60), (hx, hy - 44), (hx - hw * .4, hy - 60)]
    els += [poly(hull, WOOD, WOOD_L, 2, -1, curve=True)]
    for j in range(3):
        f = .3 + .23 * j
        els.append(ln([(hx - hw * .44, hy - 56 + 30 * j), (hx - hw * .25, hy - 40 + 34 * j), (hx, hy - 36 + 34 * j * f + 10 * j), (hx + hw * .25, hy - 40 + 34 * j), (hx + hw * .44, hy - 56 + 30 * j)],
                      -1, "rgba(233,190,140,.5)", 1.6, curve=True, draw=False))
    rivets = []
    for j in range(3):
        for k in range(13):
            x = hx - hw * .36 + k * hw * .06
            y = hy - 44 + 30 * j + 10 * math.sin(math.pi * (k + 1) / 14) * (j + 1) * .6
            rivets.append((x, y))
    for (x, y) in rivets:
        els.append(circ(x, y, 4, "#9aa0a8", "#3a2a1e", 1, -1))
    for k in (3, 9, 17, 22, 30):
        x, y = rivets[k]
        els += [circ(x, y, 7, "#ff7a4a", at=tc, fx="pop"), ln([(x, y + 8), (x - 6 + 3 * (k % 3), 560)], tc + .2, "#9aa0a8", 2, "inferred", dur=.5)]
    for x in (hx - 260, hx, hx + 260):
        els.append(poly([(x - 30, 520), (x + 30, 520), (x + 16, hy + 26), (x - 16, hy + 26)], "#3a281a", "#8a6a48", 1.5, -1))
    els += [lab(hx, 200, "boat repair", tb, BONE, 32)]
    # the tray of nails
    tx0, ty0 = 640, 610
    els += [rect(tx0 - 20, ty0 - 16, 860, 186, "rgba(18,13,10,.7)", "rgba(245,236,220,.3)", 2, 10, tn - .2, fx="pop")]
    for k in range(100):
        x = tx0 + 10 + (k % 20) * 41
        y = ty0 + 8 + (k // 20) * 32
        els.append(ln([(x, y), (x + 14, y + 22)], tn + .012 * k, "#9aa0a8", 3.5, draw=False, fx="pop"))
        els.append(ln([(x - 4, y + 2), (x + 6, y - 4)], tn + .012 * k, "#c8ccd2", 3, draw=False, fx="pop"))
    els += [lab(tx0 - 40, ty0 + 90, "about 100 nails", tn + 1.2, BONE, 30, "end")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s25_add():
    """Hall F's lean-to shed lights at its east end; a spindle whorl and a needle whetstone pop inside it; a woman spins wool beside the plan."""
    tw, tt = T("s25", "spindle whorl"), T("s25", "women's work")
    x, y, w, h = HF
    sx, sy, sw, sh = x + w, y + h * .22, 74, h * .56
    els = [rect(sx, sy, sw, sh, "rgba(242,201,142,.2)", GOLD, 2.5, 10, tw - .3, fx="pop"), gl(sx + sw / 2, sy + sh / 2, 170, tw - .2, .45),
           lab(sx + sw / 2, sy - 22, "the shed", tw, GOLD, 28)]
    els += [grp([poly(E(sx + sw / 2, sy + sh * .3, 22, 9), "#7d8a7a", "#d8e0d0", 1.5, curve=True), circ(sx + sw / 2, sy + sh * .3, 3, "#3a2e24")], tw + .2, "pop"),
            grp([poly([(sx + 18, sy + sh * .62), (sx + 52, sy + sh * .58), (sx + 56, sy + sh * .7), (sx + 22, sy + sh * .74)], "#8a8478", "#e0dcd2", 1.5)], tw + .8, "pop")]
    els += woman(900, 664, 150, tt, "#cbbca8", -1, spin=True) + [lab(900, 708, "women's work", tt + .3, BONE, 30)]
    return els


def s26_add():
    """No shelters for animals (a struck byre); ship repair and exploring; 70 to 90 people."""
    tn, tb, tp = T("s26", "No shelters"), T("s26", "mending ships"), T("s26", "seventy to ninety")
    els = [rect(560, 140, 120, 70, "none", BONE, 2, 6, tn, style="inferred", fx="pop")]
    els += cow(620, 196, 44, tn, BONE) + [ln([(548, 132), (694, 220)], tn + .4, RED, 5, dur=.3)]
    els += [lab(620, 248, "no animal shelters", tn + .5, BONE, 26)]
    els += ship_icon(150, 520, 70, tb, AU) + [lab(150, 570, "ship repair", tb + .2, AU, 26)]
    els += [arr([(150, 480), (120, 360), (180, 190)], tb + .6, AU, 3, "inferred", .8), lab(140, 150, "exploring", tb + .8, AU, 26)]
    for k in range(90):
        x = 1262 + (k % 15) * 27
        y = 600 + (k // 15) * 30
        e = person(round(x, 1), round(y, 1), 24, round(tp + .012 * k, 2), GOLD if k < 70 else "none", "pop")
        if k >= 70:
            e.update(color="rgba(242,201,142,.35)")
        els.append(e)
    els += [lab(1450, 560, "70 to 90 people", tp + .5, GOLD, 30)]
    return els


# ================================================================== 3. A STORM IN THE TREE RINGS
def s27():
    """Radiocarbon is a clock with only an hour hand: it tells you roughly when, not the year."""
    th, tr = T("s27", "hour hand"), T("s27", "roughly when")
    cx, cy, r = 889, 440, 250
    els = [gl(cx, cy, 520, -1, .2, "lamp"), circ(cx, cy, r + 14, "#3a2e24", "#8a6a48", 3, -1), circ(cx, cy, r, "#efe6d2", "#cbbca8", 2, -1)]
    for k in range(12):
        a = math.radians(30 * k)
        L = 26 if k % 3 == 0 else 14
        els.append(ln([(cx + (r - 12) * math.sin(a), cy - (r - 12) * math.cos(a)), (cx + (r - 12 - L) * math.sin(a), cy - (r - 12 - L) * math.cos(a))], -1, "#3a2e24", 5 if k % 3 == 0 else 3, draw=False))
    a = math.radians(312)
    hx, hy = cx + 150 * math.sin(a), cy - 150 * math.cos(a)
    els += [ln([(cx, cy), (hx, hy)], th, "#2a2018", 14, dur=.7), circ(cx, cy, 16, "#2a2018", at=th, fx="pop")]
    els += [ln([(cx + (r - 50) * math.sin(math.radians(d)), cy - (r - 50) * math.cos(math.radians(d))) for d in range(282, 343, 4)], tr, LILAC, 26, "known", .8, True, op=.55)]
    els += [lab(cx, 140, "radiocarbon dating", -1, AMBER, 34), lab(cx + r + 60, cy - 30, "only an hour hand", th + .3, BONE, 30, "start"),
            lab(cx - r - 50, cy - 150, "roughly when", tr + .3, LILAC, 32, "end")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


XR = lambda yr: round(200 + (yr - 600) / 600 * 1380, 1)          # 600 to 1200 CE


def s28():
    """Fifty-five radiocarbon dates from the Norse layers, each a range; together they span the whole Viking Age, 793 to 1066, and more."""
    tn, tv = T("s28", "fifty-five"), T("s28", "Viking Age")
    ticks = [(XR(y), str(y)) for y in (600, 700, 800, 900, 1000, 1100, 1200)]
    els = [axis(200, 1580, 690, ticks, -1)]
    els += [rect(XR(793), 168, XR(1066) - XR(793), 500, "rgba(242,201,142,.12)", GOLD, 2, 6, tv, fx="pop"),
            lab((XR(793) + XR(1066)) / 2, 150, "the Viking Age", tv + .2, GOLD, 30),
            lab(XR(793), 650, "793", tv + .3, GOLD, 26, "end"), lab(XR(1066) + 8, 650, "1066", tv + .3, GOLD, 26, "start")]
    rnd = random.Random(55)
    for k in range(55):
        c = rnd.gauss(990, 52)
        half = rnd.uniform(60, 150)
        a, b = max(660, c - half), min(1190, c + half)
        y = 186 + k * 8.6
        els.append(ln([(XR(a), y), (XR(b), y)], tn + .03 * k, "#e8d8c0", 4.2, dur=.25))
    els += [lab(240, 440, "55 dates", tn + .4, BONE, 36, "start", st="serif")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s29():
    """A child grows against a door frame, a pencil mark a year; a tree grows a ring a year."""
    tm, tr = T("s29", "pencil marks"), T("s29", "one ring")
    els = [poly([(250, 780), (250, 180), (560, 180), (560, 780), (520, 780), (520, 216), (290, 216), (290, 780)], "#6b4a30", "#c99a68", 2, -1)]
    els += [rect(290, 216, 230, 564, "rgba(255,236,206,.05)", at=-1)]
    els += [person(430, 780, 300, -1, "#cbbca8", None)]
    for k in range(9):
        y = 760 - 12 - 26 * k - (100 if k > 3 else 0) * 0
        y = 740 - 34 * k
        if y < 440:
            break
        els += [ln([(504, y), (532, y)], tm + .25 * k, "#2a2018", 3, dur=.2)]
    els += [lab(400, 160, "a mark a year", tm, BONE, 28)]
    cx, cy = 1180, 470
    els += [circ(cx, cy, 300, "#4a3322", "#2a1d14", 3, tr - .3, fx="pop"), circ(cx, cy, 286, "#c9a370", at=tr - .3, fx="pop")]
    for k in range(24):
        els.append(circ(cx, cy, 16 + 11 * k, "none", "#7a5636" if k % 2 else "#8c6a48", 3, tr + .1 * k, fx="draw", dur=.25))
    els += [lab(cx, 800 - 30, "one ring a year", tr + 1.0, GOLD, 32)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def tiny_fir(x, y, h, ang, at, c="#2f5a34"):
    """A small fir standing on a globe's surface at (x, y), leaning by `ang` degrees."""
    a = math.radians(ang)
    P = lambda u, v: (x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a))
    return poly([P(0, -h), P(h * .3, -h * .1), P(-h * .3, -h * .1)], c, "none", 0, at)


def s30():
    """The Sun flares; a stream of particles reaches the Earth; trees all round the globe blink; one ring in a slice turns gold: 993."""
    tb, te, tw = T("s30", "burst of particles"), T("s30", "Every tree"), T("s30", "date stamp")
    sx, sy = 250, 380
    els = [gl(sx, sy, 260, -1, .9, "sun"), circ(sx, sy, 70, "#ffe2b4", at=-1)]
    gx, gy, R_ = 1220, 470, 230
    els += [gl(gx, gy, R_ + 90, -1, .25, "lamp"), circ(gx, gy, R_ + 18, "rgba(159,208,255,.12)", "rgba(159,208,255,.4)", 3, -1),
            circ(gx, gy, R_, "#1d3a4a", "#9fd0ff", 2, -1)]
    els += ortho_land(gx, gy, R_, -40, 32, -1)
    els += [gl(sx, sy, 420, tb, .8, "sun")]
    rnd = random.Random(3)
    for k in range(26):
        y0 = sy + rnd.uniform(-90, 90)
        t0 = tb + .1 + .05 * k
        y1 = gy + rnd.uniform(-150, 150)
        els.append(ln([(sx + 80, y0), ((sx + gx) / 2, (y0 + y1) / 2 + rnd.uniform(-40, 40)), (gx - R_ - 20, y1)], t0, "#ffe8b0", 2, "claimed", .9, True))
    els += [lab((sx + gx) / 2 - 40, 220, "the Sun's burst", tb + .4, AU, 32), lab(sx, sy + 150, "993", tb + .2, AU, 52, st="serif")]
    for k in range(14):
        ang = -80 + k * (160 / 13)
        a = math.radians(ang - 90)
        x, y = gx + R_ * math.cos(a), gy + R_ * math.sin(a)
        els.append(tiny_fir(x, y, 30, ang, -1))
        els.append(circ(x + 28 * math.cos(a), y + 28 * math.sin(a), 6, AU, at=te + .06 * k, fx="pop"))
    els += [lab(gx, gy + R_ + 70, "every tree, that year", te + .6, AU, 30)]
    ix, iy = 1560, 210
    els += [circ(ix, iy, 92, "#c9a370", "#4a3322", 8, -1)]
    for k in range(8):
        els.append(circ(ix, iy, 10 + 10 * k, "none", "#8c6a48", 2, -1))
    els += [circ(ix, iy, 50, "none", AU, 6, tw - .6, fx="draw", dur=.6), gl(ix, iy, 120, tw - .4, .6)]
    return {"base": "dark", "stars": 80, "cam": CAM, "els": els}


def s31_add():
    """Radiocarbon in tree rings, year by year: flat, then a sharp step at 993; found in 2013."""
    tf = T("s31", "found that stamp")
    X = lambda yr: round(140 + (yr - 980) * 22, 1)
    els = [rect(110, 570, 620, 200, "rgba(18,13,10,.88)", "rgba(245,236,220,.3)", 2, 10, .3, fx="pop"),
           ln([(X(980), 740), (X(1004), 740)], .4, DIM, 2, dur=.4), lab(X(980), 764, "980", .5, DIM, 24, "start"), lab(X(1004), 764, "1005", .5, DIM, 24, "end"),
           lab(130, 604, "radiocarbon in tree rings", .5, DIM, 26, "start")]
    pts = [(X(y), 716 - (3 * math.sin(y) if y < 993 else 62 - 3 * math.sin(y))) for y in range(981, 1004)]
    els += [ln(pts[:12], .6, BONE, 3, dur=.6), ln(pts[11:13], 1.2, AU, 5, dur=.2), ln(pts[12:], 1.4, BONE, 3, dur=.5),
            gl(X(993), 680, 60, 1.3, .7), lab(X(993) - 12, 650, "993", 1.3, AU, 30, "end", st="serif")]
    els += chip(600, 700, "found 2013", AU, tf, 26)
    return els


WOODS = [(330, 330, 320, 110, "#b98a5a"), (780, 470, 340, 120, "#a8784c"), (1240, 330, 300, 104, "#c49a6a")]   # x, y, length, girth, colour


def piece(x, y, L, d, col, at):
    """A piece of wood lying on its side: grain, a clean angled cut at the left end, the bark round it, the end face at the right."""
    els = [poly([(x + 40, y - d / 2), (x + L, y - d / 2), (x + L, y + d / 2), (x, y + d / 2)], col, "rgba(255,236,206,.4)", 1.5, at)]
    for k in range(4):
        yy = y - d / 2 + d * (k + 1) / 5
        els.append(ln([(x + 30 - 8 * k, yy), (x + L * .4, yy + 3), (x + L - 10, yy - 2)], at, "rgba(60,40,20,.45)", 1.5, curve=True, draw=False))
    els.append(poly(E(x + L, y, d * .22, d / 2, 28), "#3a281a", "none", 0, at, curve=True))
    els.append(poly(E(x + L, y, d * .19, d / 2 - 7, 28), "#d8b48a", "none", 0, at, curve=True))
    for k in range(1, 6):
        els.append(poly(E(x + L, y, d * .19 * k / 6, (d / 2 - 7) * k / 6, 20), "none", "#8c6a48", 1.2, at, curve=True))
    return els


def s32():
    """Three pieces of Norse wood from three trees: clean metal cuts at their ends; the bark edge and the last ring traced."""
    tm, tb = T("s32", "metal blade"), T("s32", "bark")
    els = [rect(140, 210, 1500, 470, "rgba(30,22,16,.6)", "rgba(245,236,220,.12)", 2, 18, -1), gl(889, 420, 700, -1, .18, "lamp")]
    for x, y, L, d, col in WOODS:
        els += piece(x, y, L, d, col, -1)
    for x, y, L, d, col in WOODS:
        els += [ln([(x + 40, y - d / 2), (x, y + d / 2)], tm, "#fff6e0", 4, dur=.3), ln([(x + 28, y - d / 2 + 14), (x + 6, y + d / 2 - 12)], tm + .15, "#fff6e0", 2, dur=.3),
                gl(x + 20, y, 70, tm, .55)]
        els += [poly(E(x + L, y, d * .22, d / 2, 28), "none", "#1a120c", 4, tb, curve=True, fx="draw", dur=.5),
                poly(E(x + L, y, d * .19, d / 2 - 7, 28), "none", AU, 3, tb + .3, curve=True, fx="draw", dur=.5)]
    els += [lab(889, 180, "three trees", .4, BONE, 32), lab(330, 430, "metal cuts", tm + .3, "#fff6e0", 28, "start"),
            lab(1560, 420, "last ring", tb + .5, AU, 28, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s33():
    """One slice, counted: the 993 ring glows; 28 more rings to the bark, a dot each; 1021 at the bark; three strips line up on the same marks."""
    ts, tc, ty, t3 = T("s33", "sits in one ring"), T("s33", "twenty-eight more"), T("s33", "Nine ninety-three"), T("s33", "in all three")
    cx, cy = 520, 440
    sp, r1 = 7.6, 300
    r993 = r1 - 28 * sp
    els = [gl(cx, cy, 520, -1, .16, "lamp"), circ(cx, cy, r1 + 14, "#4a3322", "#2a1d14", 3, -1), circ(cx, cy, r1, "#c9a370", at=-1)]
    k = 0
    r = r993 - 7 * sp
    while r <= r1 + .1:
        els.append(circ(cx, cy, r, "none", "#7a5636" if k % 2 else "#8c6a48", 2.6, -1))
        r += sp; k += 1
    els += [circ(cx, cy, r993, "none", AU, 6, ts, fx="draw", dur=.8), gl(cx - r993 * .7, cy - r993 * .7, 60, ts, .7), lab(cx - r993 * .7 - 10, cy - r993 * .7 - 26, "993", ts + .2, AU, 36, "end", st="serif")]
    for j in range(1, 29):
        rr = r993 + j * sp
        els.append(circ(cx + rr, cy, 3.2, AU, at=tc + .07 * j, fx="pop"))
    els += [lab(cx + (r993 + r1) / 2, cy - 54, "28 more rings", tc + .6, AU, 28)]
    els += [circ(cx, cy, r1, "none", GOLD, 6, ty + .6, fx="draw", dur=.7), lab(cx + r1 + 24, cy + 60, "1021", ty + 1.2, GOLD, 56, "start", st="serif", fx="pop")]
    # three strips, one per tree, lined up on the spike and the bark
    sx0, sx1 = 1080, 1620
    x993, x21 = sx1 - 28 * 13, sx1
    for j, (yy, col) in enumerate(((300, "#b98a5a"), (420, "#a8784c"), (540, "#c49a6a"))):
        els += [rect(sx0, yy - 34, sx1 - sx0, 68, col, "rgba(255,236,206,.35)", 1.5, 4, -1)]
        for q in range(int((sx1 - sx0) / 13)):
            xq = sx1 - 13 * q
            els.append(ln([(xq, yy - 30), (xq, yy + 30)], -1, "rgba(80,50,25,.55)", 1.6, draw=False))
        els += [rect(sx1 - 4, yy - 36, 10, 72, "#2a1d14", at=-1),
                ln([(x993, yy - 32), (x993, yy + 32)], ts + .3, AU, 6, dur=.3), tick(sx1 + 34, yy, t3 + .25 * j, GOLD, .9)]
    els += [lab(x993, 240, "993", ts + .4, AU, 30, st="serif"), lab(x21, 240, "1021", ty + 1.3, GOLD, 30, "end", st="serif")]
    els += [lab(1350, 650, "993 + 28 = 1021", ty + .3, GOLD, 40, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s34_add():
    """Seasons: one piece cut in spring (a budding twig), another in summer or autumn (a sun and a falling leaf); the year 1021 under them."""
    tsp, tsu, ty = T("s34", "spring"), T("s34", "summer or"), T("s34", "more than one season")
    (x1, y1, L1, d1, _), (x2, y2, L2, d2, _), _ = WOODS
    els = [ln([(x1 + L1 * .5, y1 - d1 / 2 - 6), (x1 + L1 * .5 + 10, y1 - d1 / 2 - 56)], tsp, "#6b8f3a", 4, dur=.3),
           poly(E(x1 + L1 * .5 + 24, y1 - d1 / 2 - 60, 18, 9, 12), "#8fd06a", "none", 0, tsp + .2, fx="pop", curve=True),
           lab(x1 + L1 * .5, y1 - d1 / 2 - 84, "spring", tsp + .2, "#a8e08a", 30)]
    sx, sy = x2 + L2 * .5, y2 + d2 / 2 + 70
    els += [circ(sx - 40, sy, 18, "#ffd27a", at=tsu, fx="pop"), gl(sx - 40, sy, 50, tsu, .6),
            poly([(sx + 10, sy - 14), (sx + 34, sy - 6), (sx + 28, sy + 14), (sx + 6, sy + 6)], "#d8843a", "none", 0, tsu + .2, fx="pop"),
            lab(sx + 60, sy + 10, "summer or autumn", tsu + .3, "#f0b06a", 30, "start")]
    bx0, bx1, by_ = 300, 1500, 750
    els += [rect(bx0, by_ - 10, bx1 - bx0, 20, "rgba(245,236,220,.1)", DIM, 1.5, 10, ty - .4, fx="pop"),
            rect(bx0 + (bx1 - bx0) * 2 / 12, by_ - 10, (bx1 - bx0) * 3 / 12, 20, "rgba(143,208,106,.6)", at=ty - .2, fx="pop"),
            rect(bx0 + (bx1 - bx0) * 5 / 12, by_ - 10, (bx1 - bx0) * 6 / 12, 20, "rgba(240,176,106,.55)", at=ty, fx="pop"),
            lab(bx0 - 16, by_ + 9, "1021", ty - .4, GOLD, 28, "end", st="serif")]
    return els


VW = View(-180, 180, -58, 80, (90, 120, 1600, 680))         # the world


def s35():
    """Humans had spread east through Asia into the Americas, and west into Europe; in Newfoundland, in 1021, the circle closed."""
    tg, te, tw, tc = T("s35", "circled the globe"), T("s35", "spread east"), T("s35", "west, into"), T("s35", "the circle")
    v = VW
    els = [mapland(v, keep=lambda r: max(q[1] for q in r) > -55)]
    nx0, ny0 = v.p(*LAM)
    els += [gl(nx0, ny0, 90, -1, .35), ln([(100, ny0), (1680, ny0)], tg, GOLD, 2.5, "claimed", 1.8, op=.55),
            lab(1670, ny0 - 18, "around the world", tg + .6, GOLD, 28, "end")]
    east1 = [v.p(36, 4), v.p(48, 28), v.p(72, 40), v.p(102, 44), v.p(132, 54), v.p(158, 62), v.p(179, 66)]
    east2 = [v.p(-179, 66), v.p(-160, 63), v.p(-138, 59), v.p(-122, 50), v.p(-100, 44), v.p(-80, 45.5), v.p(-62, 49), v.p(-56.5, 51.2)]
    west = [v.p(30, 6), v.p(33, 30), v.p(20, 46), v.p(6, 56), v.p(-12, 62), v.p(-22, 64.5), v.p(-36, 63), v.p(-46, 60.6), v.p(-55.2, 51.9)]
    els += [ln(east1, te, AMBER, 4, "inferred", 1.6, True), arr(east2, te + 1.4, AMBER, 4, "inferred", 1.8),
            lab(*v.p(100, 30), "east, through Asia", te + .5, AMBER, 30)]
    els += [arr(west, tw, GOLD, 4, "inferred", 1.8), lab(v.p(-4, 70)[0], v.p(-4, 70)[1], "west, into Europe", tw + .5, GOLD, 30)]
    nx, ny = v.p(*LAM)
    els += [circ(nx, ny, 26, "none", GOLD, 5, tc, fx="draw", dur=.6), gl(nx, ny, 140, tc, .8)] + chip(nx - 10, ny + 70, "1021", GOLD, tc + .3, 30)
    els += [lab(*v.p(24, -12), "Africa", -1, DIM, 28, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== 4. NUTS FROM THE SOUTH
def burl(x, y, s, at):
    """A knobbly lump of butternut wood with one clean, flat cut face."""
    rnd = random.Random(9)
    pts = []
    for k in range(18):
        a = 2 * math.pi * k / 18
        r = s * (1 + .12 * math.sin(3 * a) + rnd.uniform(-.06, .06))
        pts.append((x + r * math.cos(a) * 1.2, y + r * math.sin(a) * .8))
    return [poly(pts, "#9a6e42", "#e9cfa8", 1.5, at, curve=True, fx="pop"),
            poly([(x + s * .3, y - s * .7), (x + s * 1.16, y - s * .2), (x + s * 1.1, y + s * .36), (x + s * .4, y - s * .1)], "#e8c89a", "#fff4dc", 1.5, at + .05, fx="pop")]


def s36():
    """Waterlogged wood chips on dark peat; three butternuts among them; a lump of butternut wood with a clean knife cut."""
    tn, tb, tk = T("s36", "three butternuts"), T("s36", "a lump"), T("s36", "metal knife")
    els = [rect(120, 150, 1540, 620, "#1e1810", "rgba(245,236,220,.15)", 2, 22, -1)]
    els += [{"k": "water", "y": 520, "h": 250, "x0": 124, "x1": 1656, "op": .25, "in": -1}]
    rnd = random.Random(12)
    for k in range(60):
        x = rnd.uniform(170, 1610); y = rnd.uniform(200, 730)
        L = rnd.uniform(26, 70); a = rnd.uniform(0, math.pi)
        dx, dy = L * math.cos(a) / 2, L * math.sin(a) / 2
        els.append(poly([(x - dx, y - dy), (x + dx, y + dy), (x + dx + 6, y + dy + 8), (x - dx + 6, y - dy + 8)], rnd.choice(("#b08a5a", "#c49a6a", "#8a6a44")), "rgba(255,236,206,.25)", 1, -1))
    for k in range(14):
        x = rnd.uniform(200, 1600); y = rnd.uniform(220, 720)
        els.append(ln([(x, y), (x + 14, y - 10), (x + 26, y - 2), (x + 20, y + 8), (x + 10, y + 4)], -1, "#d8b88a", 2.5, curve=True, draw=False))
    els += [gl(889, 460, 640, -1, .14, "lamp")]
    for k, (x, y, rot) in enumerate(((560, 380, -20), (700, 470, 15), (590, 560, 40))):
        els += [gl(x, y, 90, tn + .25 * k, .5)] + nut(x, y, 120, tn + .25 * k, rot=rot)
    els += [lab(640, 690, "3 butternuts", tn + .8, GOLD, 34)]
    els += [gl(1180, 430, 160, tb, .45)] + burl(1180, 430, 110, tb)
    els += [gl(1260, 400, 70, tk, .8), lab(1180, 580, "cut with a knife", tk + .2, "#fff4dc", 32)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


VGF = View(-71, -52, 43.5, 52.5, (90, 120, 1600, 680))       # the Gulf of St Lawrence
BUTTER = [(-71, 47.2), (-69.5, 47.6), (-68, 47.4), (-66.8, 47.2), (-65.6, 47.05), (-64.9, 46.6), (-64.7, 46.0), (-66, 45.3), (-67.5, 45.1), (-69, 44.6), (-71, 44.3)]
GRAPES = [(-70.5, 46.9), (-66.5, 47.12), (-65.0, 46.95), (-64.25, 46.3), (-64.5, 45.6), (-66.5, 45.0), (-69.5, 44.55), (-70.8, 45.4)]
MIRA = (-65.6, 47.0)


def s37():
    """The Gulf of St Lawrence: no butternuts in Newfoundland; butternut country south of about 47 degrees north in New Brunswick; almost 900 km
    in a straight line from L'Anse aux Meadows; there and back."""
    tn, tl, tk, tb = T("s37", "don't grow"), T("s37", "The nearest"), T("s37", "nine hundred"), T("s37", "came back")
    v = VGF
    els = [mapland(v)]
    lx, ly = v.p(*LAM)
    els += [pin(lx, ly, "L'Anse aux Meadows", -1, GOLD, "end", -50, -18), lab(*v.p(-67.6, 51.0), "Quebec", -1, DIM, 28, st="ital")]
    nx, ny = v.p(-56.3, 48.7)
    els += cross(nx, ny, tn, RED, 1.6, 7) + [lab(nx, ny + 64, "no butternuts", tn + .3, "#ffb4a8", 28)]
    bp = [v.p(lo, la) for lo, la in BUTTER]
    els += [poly(bp, "rgba(143,217,176,.22)", GREEN, 2.5, tl, curve=True, style="inferred", fx="pop"),
            lab(*v.p(-67.4, 45.9), "butternut country", tl + .4, GREEN, 30)]
    mx, my = v.p(*MIRA)
    els += [circ(mx, my, 9, GREEN, at=tl + .3, fx="pop"), ln([(lx, ly), (mx, my)], tk - .3, BONE, 2.5, "inferred", .9)]
    dx, dy = mx - lx, my - ly
    L = math.hypot(dx, dy)
    px, py = -dy / L, dx / L                      # the perpendicular towards the south-east
    if py < 0:
        px, py = -px, -py
    ax, ay = (lx + mx) / 2, (ly + my) / 2
    kx, ky = mx + .3 * (lx - mx), my + .3 * (ly - my)
    els += [lab(kx + 70 * px, ky + 70 * py + 10, "about 900 km", tk + .2, BONE, 30, "start")]
    els += [arr([(lx - 12, ly + 4), (ax - 40 * px, ay - 40 * py), (mx + 12, my - 10)], tb - .6, AMBER, 4, "known", .9),
            arr([(mx + 14, my + 8), (ax + 40 * px, ay + 40 * py), (lx - 4, ly + 16)], tb + .1, AMBER, 4, "known", .9)]
    return {"base": "map", "cam": CAM, "els": els}


def s38_add():
    """Wild grapes along the southern shores of the Gulf, overlapping butternut country; grapes and butternuts side by side."""
    tg, ts = T("s38", "wild grapes"), T("s38", "side by")
    v = VGF
    gp = [v.p(lo, la) for lo, la in GRAPES]
    els = [poly(gp, "rgba(142,90,168,.26)", "#c9a0e0", 2.5, tg, curve=True, style="claimed", fx="pop"), lab(*v.p(-69.0, 44.0), "wild grapes", tg + .4, "#d8b0f0", 30)]
    mx, my = v.p(*MIRA)
    els += grapes(mx - 96, my - 96, 50, ts, GRAPE) + nut(mx - 20, my - 56, 54, ts + .2, rot=20)
    return els


def s39_add():
    """Wallace's reading: this meadow a gateway; Vinland a whole region around the Gulf of St Lawrence."""
    tg, tv = T("s39", "gateway"), T("s39", "whole region")
    v = VGF
    lx, ly = v.p(*LAM)
    gulf = [v.p(lo, la) for lo, la in ((-66.8, 50.2), (-62.5, 50.4), (-58.6, 51.2), (-57.6, 49.6), (-59.5, 47.4), (-60.8, 45.6), (-63.6, 45.4), (-65.6, 46.4), (-66.4, 48.2))]
    els = [circ(lx, ly, 34, "none", GOLD, 5, tg, fx="draw", dur=.5), gl(lx, ly, 120, tg, .7), lab(lx + 44, ly + 40, "the gateway", tg + .3, GOLD, 30, "start")]
    els += [poly(gulf, "rgba(201,193,238,.08)", LILAC, 3, tv, curve=True, style="claimed", fx="draw", dur=1.2), lab(*v.p(-62.0, 50.95), "Vinland?", tv + .6, LILAC, 36, st="serif")]
    return els


XP = lambda yr: round(200 + (yr + 4000) / 5500 * 1380, 1)           # 4000 BCE to 1500 CE
XZ = lambda yr: round(300 + (yr - 600) / 900 * 1200, 1)             # zoom: 600 to 1500 CE
PEOPLES = [(-4000, -1000, "#8a7a5a"), (-1000, -500, "#9a8466"), (400, 750, "#7a8a8a"), (800, 850, "#a08a6a"), (1200, 1500, "#8a6a5a")]


def s40():
    """Six thousand years on the meadow: five earlier camps and one later, each its own colour; the Norse alone in a gap around 1000 CE."""
    tp, tn = T("s40", "five or six"), T("s40", "though none")
    ticks = [(XP(-4000), "6,000 years ago"), (XP(-2000), "2000 BCE"), (XP(0), "1 CE"), (XP(1500), "1500")]
    els = [axis(200, 1580, 330, ticks, -1)]
    for a, b, c in PEOPLES:
        els.append(rect(XP(a), 282, max(6, XP(b) - XP(a)), 26, "rgba(245,236,220,.06)", "rgba(245,236,220,.22)", 1, 6, -1, style="inferred"))
    for k, (a, b, c) in enumerate(PEOPLES):
        els.append(rect(XP(a), 282, max(6, XP(b) - XP(a)), 26, c, "rgba(245,236,220,.4)", 1, 6, tp + .2 * k, fx="pop"))
    els += [rect(XP(1000) - 3, 276, 6, 38, GOLD, at=.3, fx="pop"), lab(889, 230, "five or six peoples", tp + .4, BONE, 32)]
    # the zoom: 600 to 1500 CE
    els += [poly([(XP(600), 345), (XP(1500), 345), (1500, 560), (300, 560)], "rgba(242,201,142,.05)", "rgba(242,201,142,.3)", 1.5, tp + .9, style="inferred")]
    zt = [(XZ(y), str(y)) for y in (600, 800, 1000, 1200, 1400)]
    els += [axis(300, 1500, 640, zt, tp + 1.0)]
    for a, b, c in PEOPLES[2:]:
        a2, b2 = max(a, 600), b
        els.append(rect(XZ(a2), 580, XZ(b2) - XZ(a2), 34, c, "rgba(245,236,220,.4)", 1, 8, tp + 1.2, fx="pop"))
    els += [rect(XZ(1000), 572, XZ(1025) - XZ(1000), 50, GOLD, "#fff4dc", 1.5, 6, tn - .4, fx="pop"), gl(XZ(1012), 597, 90, tn - .3, .6),
            lab(XZ(1012), 736, "the Norse", tn - .2, GOLD, 30)]
    els += bracket(XZ(850) + 8, XZ(1200) - 8, 548, tn + .3, None, BONE, up=True) + [lab((XZ(850) + XZ(1200)) / 2, 532, "none at that time", tn + .5, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


VPE = View(-72, -50, 44, 62, (90, 120, 1600, 680))            # the peoples of the region


def s41():
    """Who were they? Soft glows on the homelands of the peoples named, labels in open space with leaders: Beothuk, Innu, Mi'kmaq ancestors;
    far north, perhaps Dorset."""
    tq, tb, ti, tm, td = T("s41", "So who were"), T("s41", "Beothuk"), T("s41", "Innu"), T("s41", "Mi'kmaq"), T("s41", "Dorset")
    v = VPE
    els = [mapland(v)]
    lx, ly = v.p(*LAM)
    els += [circ(lx, ly, 8, GOLD, at=-1), gl(lx, ly, 50, -1, .5)]
    els += qmark(*v.p(-52.6, 53.2), tq, 76)
    for t0, (lo, la), name, c, (tx, ty, a) in ((tb, (-56.0, 48.7), "Beothuk ancestors", "#f0d0a0", (1300, 640, "start")),
                                              (ti, (-62.5, 52.4), "Innu ancestors", "#f0d0a0", (470, 400, "end")),
                                              (tm, (-64.9, 46.1), "Mi'kmaq ancestors", "#f0d0a0", (470, 640, "end")),
                                              (td, (-63.4, 58.4), "Dorset, perhaps", "#c9c1ee", (1300, 210, "start"))):
        x, y = v.p(lo, la)
        ex = tx - 14 if a == "start" else tx + 14
        els += [gl(x, y, 150, t0, .45, "lamp"), circ(x, y, 7, c, at=t0, fx="pop"),
                ln([(x, y), (ex, ty - 10)], t0 + .1, c, 1.6, "claimed" if c == "#c9c1ee" else "known", .4),
                lab(tx, ty, name, t0 + .2, c, 34, a, st="serif")]
    return {"base": "map", "cam": CAM, "els": els}


def s42():
    """Two pages: the Norse stories, full of script; the other side, an empty dashed page: no surviving account."""
    tl, tn = T("s42", "only one side"), T("s42", "the Norse stories")
    els = vellum(260, 170, 560, 520, -1, 11)
    els += [{"k": "glyphs", "x": 380, "y": 214, "w": 400, "h": 290, "rows": 8, "cols": 8, "kind": "latin", "c": "rgba(90,67,48,.8)", "seed": 4, "in": -1}]
    els += initial(326, 276, "S", -1, 60) + static(ink_ship(560, 660, 190, -1, None))
    els += [lab(540, 750, "the Norse stories", tn, BONE, 30)]
    els += [rect(960, 170, 560, 520, "rgba(245,236,220,.03)", "rgba(245,236,220,.55)", 2.5, 8, tl, style="inferred", fx="pop"),
            lab(1240, 750, "the other side?", tl + .3, LILAC, 30)]
    els += qmark(890, 470, tl + .6, 70)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


XH = lambda yr: round(240 + (yr - 990) / 140 * 1300, 1)            # 990 to 1130 CE


def s43():
    """How long did they stay? Wallace: years, not decades (a short gold bar); the 2019 study: up to a century (a long lilac dashed bar)."""
    tw, t19, td = T("s43", "Wallace reads"), T("s43", "But in"), T("s43", "don't agree")
    ticks = [(XH(y), str(y)) for y in (1000, 1025, 1050, 1075, 1100, 1125)]
    els = [axis(240, 1540, 640, ticks, -1), circ(XH(1021), 640, 12, AU, at=-1), lab(XH(1021), 600, "1021", -1, AU, 30, st="serif")]
    els += [rect(XH(1000), 400, XH(1025) - XH(1000), 34, GOLD, "#fff4dc", 1.5, 10, tw, fx="pop"), lab(XH(1000), 380, "years, not decades", tw + .2, GOLD, 30, "start"),
            lab(XH(1000) - 20, 426, "Wallace", tw + .3, DIM, 26, "end")]
    els += [rect(XH(1000), 490, XH(1100) - XH(1000), 34, "rgba(201,193,238,.18)", LILAC, 2.5, 10, t19, style="inferred", fx="pop"),
            lab(XH(1100), 470, "up to a century?", t19 + .4, LILAC, 30, "end"), lab(XH(1000) - 20, 516, "2019 study", t19 + .3, DIM, 26, "end")]
    els += qmark(XH(1112), 440, td, 80)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== 5. TOO GOOD TO BE TRUE
SHEET = (330, 160, 1120, 530)        # the Vinland Map's parchment: x, y, w, h


def blob(cx, cy, rx, ry, n=28, jit=.12, seed=1, rot=0):
    """An irregular coast round (cx, cy): an ellipse with seeded wobbles."""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        f = 1 + jit * (math.sin(3 * a + seed) * .6 + rnd.uniform(-.5, .5))
        x, y = rx * f * math.cos(a), ry * f * math.sin(a)
        c, s_ = math.cos(rot), math.sin(rot)
        out.append((cx + x * c - y * s_, cy + x * s_ + y * c))
    return out


def vmap_lines():
    """The Vinland Map's ink drawing, schematic: an oval world, Europe and Asia, Africa, Iceland and Greenland, and far to the west a large
    island with two inlets (Vinland). Returns (known lines, the Vinland coast)."""
    x, y, w, h = SHEET
    cx, cy = x + w * .56, y + h * .52
    world = E(cx, cy, w * .36, h * .38, 40)
    eurasia = blob(cx + 100, cy - 80, 230, 110, 34, .16, 3, -.08)
    africa = blob(cx + 30, cy + 110, 110, 90, 24, .18, 5, .3)
    iceland = blob(cx - 230, cy - 160, 40, 22, 14, .15, 7)
    green = blob(cx - 330, cy - 160, 60, 70, 18, .2, 9, .4)
    vin = [(x + 80, y + 140), (x + 170, y + 120), (x + 220, y + 170), (x + 190, y + 220), (x + 230, y + 260), (x + 200, y + 330), (x + 130, y + 360),
           (x + 160, y + 300), (x + 120, y + 270), (x + 150, y + 230), (x + 90, y + 210), (x + 70, y + 170)]
    return [world, eurasia, africa, iceland, green], vin


def s44():
    """The Vinland Map on a desk under a lamp: an oval world in brown ink, Greenland, and far to the west, Vinland (lilac); Yale, 1965;
    said to be 15th century; about $300,000."""
    ty, tv, td = T("s44", "Yale University"), T("s44", "with Vinland"), T("s44", "three hundred thousand")
    x, y, w, h = SHEET
    els = [gl(889, 420, 760, -1, .22, "lamp")] + vellum(x, y, w, h, -1, 21)
    known, vin = vmap_lines()
    for k, pts in enumerate(known):
        els.append(poly(pts, "rgba(90,67,48,.08)", IK, 2.5, -1, curve=True))
    els += [{"k": "glyphs", "x": x + 640, "y": y + 40, "w": 380, "h": 50, "rows": 2, "cols": 8, "kind": "latin", "c": "rgba(90,67,48,.7)", "seed": 8, "in": -1}]
    els += [poly(vin, "rgba(201,193,238,.18)", "#7a5aa8", 3, tv, curve=True, style="claimed", fx="pop"), gl(x + 160, y + 240, 140, tv, .35),
            lab(x + 150, y + 410, "Vinland", tv + .2, "#7a5aa8", 34, st="serif", halo=False)]
    els += chip(x + w - 130, y + h + 46, "Yale, 1965", BONE, ty, 30) + [lab(x + 20, y + h + 56, "claimed: 15th century", ty + .6, DIM, 28, "start")]
    bx, by = x + w + 70, y + 300
    els += [grp([rect(bx - 60, by + 26 - 14 * k, 120, 56, "#6f8a5a", "#d8e8c8", 1.5, 4) for k in range(4)] +
                [circ(bx, by - 2 - 14 * 3 + 54, 14, "none", "#d8e8c8", 1.5)], td, "rise")]
    els += chip(bx, by - 60, "about $300,000", "#d8e8c8", td + .3, 26)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s45_add():
    """A lens over an ink line: a yellowish band dotted with rounded white crystals, anatase, first made in the 1920s; experts argued."""
    ta, t20, tg = T("s45", "anatase"), T("s45", "first made"), T("s45", "experts argued")
    x, y, w, h = SHEET
    lx, ly, r = x + 720, y + 190, 130
    rnd = random.Random(14)
    lens = [circ(lx, ly, r, "#efe0b8", "none", 0),
            ln([(lx - r + 10, ly + 30), (lx - 40, ly - 10), (lx + 50, ly + 20), (lx + r - 10, ly - 20)], 0, "#c8a860", 34, curve=True, draw=False)]
    for k in range(26):
        u = rnd.uniform(-.9, .9)
        px = lx + u * (r - 20)
        py = ly + 30 * math.sin(u * 2) * .2 + (-.18 * (px - lx)) * 0 + rnd.uniform(-12, 12) + (10 if px < lx - 40 else -4 if px < lx + 50 else 0)
        lens.append(circ(px, py, rnd.uniform(3.5, 6), "#fbfbf6", "rgba(120,110,90,.6)", 1))
    els = [grp(lens, ta - .3, "pop"), circ(lx, ly, r, "none", "#2a2420", 10, ta - .3, fx="pop"), ln([(lx + r * .7, ly + r * .7), (lx + r * 1.25, ly + r * 1.25)], ta - .3, "#2a2420", 16, draw=False, fx="pop")]
    els += [lab(lx - r - 24, ly + 10, "anatase", ta + .2, "#fbfbf6", 32, "end")]
    els += chip(lx - 90, ly + r + 44, "first made 1920s", "#fbfbf6", t20, 26)
    els += [tick(x + 110, y + 64, tg, GREEN, 1.1), lab(x + 170, y + 72, "or", tg + .3, IK, 28, halo=False)] + cross(x + 230, y + 64, tg + .5, RED, 1.0, 6)
    return els


def s46_add():
    """Yale 2021: a scanner sweeps; titanium dots pop all along every ink line; the inscription on the back turns blue; a red FAKE stamp."""
    tt, tb, tf = T("s46", "titanium throughout"), T("s46", "an inscription"), T("s46", "is a fake")
    x, y, w, h = SHEET
    known, vin = vmap_lines()
    els = [rect(x - 40, y - 60, 120, 40, "#3a3f46", "#c8d0d8", 1.5, 6, tt - .4, fx="pop"), ln([(x + 20, y - 20), (x + 20, y + h - 40)], tt - .3, "rgba(159,208,255,.6)", 3, dur=1.6)]
    rnd = random.Random(21)
    k = 0
    for pts in known + [vin]:
        for j in range(0, len(pts), 2):
            px, py = pts[j]
            els.append(circ(px, py, 5, "#cfe8ff", "#5a8ab8", 1, tt + .02 * k, fx="pop"))
            k += 1
    els += [lab(x + w / 2, y - 30, "titanium in every line", tt + .5, BLUE, 30)]
    cxp, cyp = x + w - 40, y + h - 40
    els += [poly([(cxp - 170, cyp + 40), (cxp + 40, cyp + 40), (cxp + 40, cyp - 120)], "#cdb78f", VEL_E, 2, tb, fx="pop"),
            ln([(cxp - 120, cyp + 22), (cxp + 10, cyp - 70)], tb + .3, "#5a8ab8", 4, dur=.5), ln([(cxp - 80, cyp + 30), (cxp + 22, cyp - 40)], tb + .5, "#5a8ab8", 4, dur=.5),
            lab(cxp - 60, cyp - 70, "rewritten", tb + .6, BLUE, 28, "end")]
    sx, sy = x + w * .36, y + h * .62
    els += [grp([rect(sx - 170, sy - 62, 340, 124, "rgba(184,50,42,.08)", "#c0392b", 7, 10), lab(sx, sy + 26, "FAKE", 0, "#c0392b", 84, st="serif", halo=False)],
                tf, "pop", tr=f"rotate(-9 {sx} {sy})")]
    return els


def s47():
    """A Viking grave mound cut open: a sword, two oval brooches, a string of beads, and a plastic bottle among them, glowing."""
    tg, tb = T("s47", "a Viking"), T("s47", "plastic bottle")
    g = 330
    els = [rect(80, g, 1620, 470, "#2a2016", at=-1), poly([(340, g), (520, g - 120), (889, g - 170), (1260, g - 120), (1440, g)], "#3a2c1c", "rgba(245,236,220,.35)", 2, -1, curve=True)]
    for k, c in enumerate(("#352818", "#2e2214", "#271c10")):
        els.append(rect(80, g + 40 + 140 * k, 1620, 140, c, at=-1))
    els += [poly([(520, g + 160), (1260, g + 160), (1240, g + 330), (540, g + 330)], "rgba(80,60,40,.5)", "rgba(245,236,220,.25)", 1.5, -1, style="inferred")]
    els += [grp([ln([(600, g + 230), (900, g + 230)], 0, "#b8bec6", 12, draw=False), ln([(600, g + 230), (900, g + 230)], 0, "#e8eef2", 3, draw=False),
                 rect(900, g + 214, 14, 32, "#8a6a48"), ln([(914, g + 230), (980, g + 230)], 0, "#6b4a30", 12, draw=False), circ(986, g + 230, 12, "#c99a4a")], tg, "pop")]
    els += [grp([poly(E(1060, g + 210, 34, 22), "#c99a4a", "#f0d8a0", 2, curve=True), poly(E(1150, g + 214, 34, 22), "#c99a4a", "#f0d8a0", 2, curve=True)], tg + .2, "pop")]
    els += [grp([circ(1040 + 22 * k, g + 290 + 6 * math.sin(k), 8, ("#3a6ab0", "#c0392b", "#e8c35a", "#3a8a5a")[k % 4]) for k in range(8)], tg + .4, "pop")]
    bx, by = 720, g + 300
    els += [gl(bx, by - 30, 150, tb, .7, "lamp"),
            grp([rect(bx - 26, by - 100, 52, 110, "rgba(200,230,255,.55)", "#e8f4ff", 2, 14), rect(bx - 12, by - 124, 24, 26, "#3a7ad8", "#cfe0ff", 1.5, 4),
                 ln([(bx - 14, by - 80), (bx - 14, by - 10)], 0, "rgba(255,255,255,.7)", 3, draw=False)], tb, "pop")]
    els += [lab(889, g - 200, "a Viking grave", tg, BONE, 32), lab(bx - 60, by + 60, "a plastic bottle", tb + .3, BLUE, 30, "end")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


VNM = View(-128, -50, 24, 60, (90, 150, 760, 560))       # North America (left half)
KEN = (-95.68, 45.81)


def runes(x, y, w, rows, at, c="#2a2420", seed=3):
    """Rows of rune-like strokes cut in stone."""
    rnd = random.Random(seed)
    out = []
    for r in range(rows):
        xx = x
        yy = y + r * 34
        while xx < x + w:
            k = rnd.randint(0, 4)
            st = [(xx, yy), (xx, yy + 24)]
            out.append(ln(st, at, c, 3, draw=False))
            if k == 1:
                out.append(ln([(xx, yy + 4), (xx + 9, yy + 12)], at, c, 3, draw=False))
            elif k == 2:
                out.append(ln([(xx, yy + 6), (xx + 9, yy), ], at, c, 3, draw=False))
                out.append(ln([(xx, yy + 14), (xx + 9, yy + 8)], at, c, 3, draw=False))
            elif k == 3:
                out.append(ln([(xx - 6, yy + 6), (xx + 6, yy + 16)], at, c, 3, draw=False))
            elif k == 4:
                out.append(circ(xx + 5, yy + 8, 4, "none", c, 2.4, at))
            xx += 18
    return out


def s48():
    """Minnesota: a map of North America with Kensington deep inland, about 3,000 km from L'Anse aux Meadows; the stone slab with its runes,
    tangled in a tree's roots; Olof Ohman with a spade, 1898; dated 1362; the roots glow."""
    to, t13, tr = T("s48", "Olof"), T("s48", "the year"), T("s48", "those roots")
    v = VNM
    els = [rect(80, 140, 780, 600, "#173040", "rgba(245,236,220,.25)", 2, 14, -1), {"k": "group", "clip": [80, 140, 780, 600, 14], "els": [mapland(v)], "in": -1},
           rect(80, 140, 780, 600, "none", "rgba(245,236,220,.25)", 2, 14, -1)]
    kx, ky = v.p(*KEN)
    lx, ly = v.p(*LAM)
    els += [circ(lx, ly, 8, GOLD, at=-1), ln([(lx, ly), (kx, ky)], .5, "rgba(201,193,238,.8)", 2.5, "claimed", 1.0),
            pin(kx, ky, "Kensington, Minnesota", .3, LILAC, "end", -16, 40), lab((lx + kx) / 2 + 10, (ly + ky) / 2 - 20, "about 3,000 km", .9, BONE, 26)]
    # the stone in the roots
    sx, sy = 1260, 560
    stone = [(sx - 110, sy + 90), (sx - 120, sy - 200), (sx + 90, sy - 230), (sx + 120, sy + 70)]
    els += [poly([(900, 640), (1700, 640), (1700, 800), (900, 800)], "#2a2016", at=-1), ln([(900, 640), (1700, 640)], -1, "rgba(245,236,220,.3)", 2, draw=False)]
    els += [poly(stone, "#8a8c88", "#d8dcd6", 2, -1)]
    els += runes(sx - 90, sy - 180, 180, 7, -1, "#3a3a36", 5)
    trunk = [(1480, 640), (1480, 300), (1500, 300), (1500, 640)]
    els += [poly(trunk, "#4a3424", at=-1), poly(E(1490, 260, 90, 80), "#2f3a24", "none", 0, -1, curve=True)]
    roots = [[(1480, 600), (1400, 610), (1340, 560), (1290, 520), (1240, 530)], [(1482, 630), (1420, 660), (1350, 700), (1260, 690), (1180, 650)],
             [(1484, 620), (1400, 640), (1310, 600), (1240, 600), (1170, 560)], [(1500, 640), (1560, 700), (1620, 720)]]
    for k, r in enumerate(roots):
        els.append(ln(r, -1, "#5a4030", 9 - k, curve=True, draw=False))
    els += [gl(1320, 600, 150, tr, .6, "lamp")] + [ln(r, tr, "#e8b87a", 3, curve=True, dur=.8) for r in roots[:3]]
    els += fig(1010, 640, 150, to, "#2a2420", "hold", 1) + [ln([(1052, 560), (1080, 660)], to, "#6b4a30", 5, draw=False), poly([(1072, 650), (1092, 650), (1088, 680), (1076, 680)], "#9aa0a8", at=to)]
    els += [lab(1010, 710, "Olof Ohman, 1898", to + .3, BONE, 28)]
    els += chip(sx, 230, "dated 1362", LILAC, t13, 30)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s49():
    """A letter dated 1362 that signs off 'OK!': a red circle; Swedish of the 1800s."""
    tl, to = T("s49", "Swedish of"), T("s49", "signs off")
    els = vellum(520, 150, 740, 600, -1, 31)
    els += [lab(600, 236, "1362", -1, IK, 46, "start", st="serif", halo=False)]
    els += [{"k": "glyphs", "x": 600, "y": 280, "w": 580, "h": 300, "rows": 9, "cols": 10, "kind": "latin", "c": "rgba(90,67,48,.75)", "seed": 12, "in": -1}]
    els += [lab(1040, 670, "OK!", -1, IK, 56, st="ital", halo=False)]
    els += [circ(1050, 650, 74, "none", "#c0392b", 6, to, fx="draw", dur=.6)]
    els += [lab(1460, 420, "Swedish of", tl, BONE, 32, "start"), lab(1460, 462, "the 1800s", tl + .1, BONE, 32, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def inside(pt, poly_):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in zip(poly_, poly_[1:] + poly_[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


ROSEE = [(80, 130), (1160, 130), (1210, 200), (1180, 300), (1230, 380), (1150, 470), (1080, 560), (960, 620), (860, 700), (700, 760), (520, 800), (80, 800)]


def s50():
    """Point Rosee from above, as a satellite sees it: a grassy headland, a pale shore, waves; lilac dashed outlines of a long house shape and a
    patch of 'bog iron'; an inset map of Newfoundland with the spot."""
    tt, ti = T("s50", "turf wall"), T("s50", "bog")
    sat = [poly(ROSEE, "#4f6a3a", "none", 0, -1), ln(ROSEE[1:11], -1, "#d8d0b0", 6, draw=False), ln(ROSEE[1:11], -1, "#f0ead8", 2, draw=False)]
    for k in range(4):
        off = 26 + 24 * k
        sat.append(ln([(px + off * .8, py + off * .6) for px, py in ROSEE[1:11]], -1, "rgba(230,240,250,%.2f)" % (.35 - .07 * k), 2, curve=True, draw=False))
    els = [rect(80, 130, 1620, 670, "#24485a", at=-1), {"k": "group", "clip": [80, 130, 1620, 670, 4], "els": sat, "in": -1}]
    rnd = random.Random(30)
    for k in range(260):
        p = (rnd.uniform(90, 1220), rnd.uniform(140, 795))
        if inside(p, ROSEE):
            els.append(circ(p[0], p[1], rnd.uniform(3, 11), rnd.choice(("#5a7a42", "#46623a", "#62824a", "#3e5a34")), at=-1, op=.85))
    for k in range(19):
        els.append(ln([(80, 150 + 34 * k), (1700, 150 + 34 * k)], -1, "rgba(200,230,255,.04)", 2, draw=False))
    for (cx_, cy_, dx, dy) in ((100, 150, 1, 1), (1680, 150, -1, 1), (100, 780, 1, -1), (1680, 780, -1, -1)):
        els.append(ln([(cx_ + 40 * dx, cy_), (cx_, cy_), (cx_, cy_ + 40 * dy)], -1, "rgba(220,240,255,.6)", 2, draw=False))
    hx, hy, M2 = 520, 400, 12
    els += [rect(hx, hy, 22 * M2, 7 * M2, "rgba(201,193,238,.12)", LILAC, 3, 8, tt - .4, style="claimed", fx="pop"),
            lab(hx + 11 * M2, hy - 24, "turf wall?", tt, LILAC, 32)]
    els += [circ(hx + 380, hy + 150, 44, "rgba(201,193,238,.12)", LILAC, 3, ti, style="claimed", fx="pop"), lab(hx + 380, hy + 230, "bog iron?", ti + .2, LILAC, 32)]
    els += [lab(260, 220, "Point Rosee", -1, BONE, 36, st="serif")]
    v = View(-60, -52, 46.5, 52, (1420, 520, 260, 240))
    els += [rect(1410, 510, 280, 260, "rgba(10,20,30,.92)", "rgba(245,236,220,.4)", 2, 10, -1),
            {"k": "group", "clip": [1410, 510, 280, 260, 10], "els": [mapland(v)], "in": -1}, rect(1410, 510, 280, 260, "none", "rgba(245,236,220,.4)", 2, 10, -1)]
    px, py = v.p(-59.33, 47.65)
    els += [circ(px, py, 9, LILAC, at=-1), gl(px, py, 40, -1, .5)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s51_add():
    """They dug again: trenches across the outlines; the outlines grey out: natural; a report page, 2017, no evidence; a green tick."""
    td, tr, tw = T("s51", "dug"), T("s51", "report found"), T("s51", "meant to")
    hx, hy, M2 = 520, 400, 12
    els = [rect(hx + 216, hy - 40, 40, 170, "#3a2a1c", "#c8a87a", 1.5, 2, td, fx="pop"), rect(hx + 320, hy + 136, 130, 30, "#3a2a1c", "#c8a87a", 1.5, 2, td + .2, fx="pop"),
           rect(hx - 10, hy + 28, 290, 30, "#3a2a1c", "#c8a87a", 1.5, 2, td + .4, fx="pop")]
    els += [rect(hx, hy, 22 * M2, 7 * M2, "rgba(120,120,120,.2)", "#a8a8a8", 3, 8, tr - .3, fx="pop"), circ(hx + 380, hy + 150, 44, "rgba(120,120,120,.2)", "#a8a8a8", 3, tr - .3, fx="pop"),
           lab(hx + 140, hy + 300, "natural", tr, BONE, 34)]
    rx, ry = 1440, 170
    els += [grp([rect(rx, ry, 220, 290, "#efe6d2", "#cdbf9f", 2, 6), lab(rx + 110, ry + 54, "2017", 0, INK, 34, st="serif", halo=False),
                 {"k": "glyphs", "x": rx + 24, "y": ry + 80, "w": 172, "h": 120, "rows": 5, "cols": 5, "kind": "latin", "c": "rgba(40,30,25,.6)", "seed": 3},
                 lab(rx + 110, ry + 250, "no evidence", 0, "#a03024", 26, st="lab", halo=False)], tr + .2, "rise")]
    els += [tick(rx - 70, ry + 150, tw, GREEN, 2.0, 9)]
    return els


# ================================================================== 6. THE WEIGHING
LROWS = [262, 372, 482, 592, 702]


def lrow(k, at, pics, text, grade=None, gt=None, gc=None, size=30):
    y = LROWS[k]
    out = [rect(130, y - 46, 1520, 92, "rgba(242,201,142,.07)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(330, y + 11, text, at + .1, BONE, size, "start")]
    out += pics
    if grade:
        out += chip(1250, y, grade, gc, gt, 28, "start")
    return out


def pic_book(x, y, at):
    return [grp([poly([(x - 30, y - 18), (x, y - 24), (x, y + 20), (x - 30, y + 26)], VEL, VEL_E, 1.5), poly([(x, y - 24), (x + 30, y - 18), (x + 30, y + 26), (x, y + 20)], VEL, VEL_E, 1.5),
                 ln([(x - 22, y - 8), (x - 6, y - 11)], 0, IK, 1.5, draw=False), ln([(x + 6, y - 11), (x + 22, y - 8)], 0, IK, 1.5, draw=False)], at, "pop")]


def pic_hall(x, y, at):
    return [grp(hall_side(x - 34, x + 34, y + 22, 34, 0, TURF, door=True, smoke=False), at, "pop")]


def pic_slice(x, y, at):
    return [grp([circ(x, y, 24, "#c9a370", "#4a3322", 4)] + [circ(x, y, 6 + 5 * k, "none", "#8c6a48", 1.2) for k in range(3)] + [circ(x, y, 21, "none", GOLD, 2.5)], at, "pop")]


def pic_map(x, y, at):
    return [grp([rect(x - 34, y - 24, 68, 48, VEL, VEL_E, 1.5, 3), poly(E(x + 8, y, 16, 12, 12), "none", IK, 1.5, curve=True),
                 poly(E(x - 20, y - 2, 8, 12, 10), "rgba(201,193,238,.4)", "#7a5aa8", 1.5, curve=True)], at, "pop")]


def pic_stone(x, y, at):
    return [grp([poly([(x - 22, y + 26), (x - 26, y - 26), (x + 20, y - 30), (x + 26, y + 22)], "#8a8c88", "#d8dcd6", 1.5)] +
                [ln([(x - 14 + 9 * j, y - 18), (x - 14 + 9 * j, y + 14)], 0, "#3a3a36", 2, draw=False) for j in range(4)], at, "pop")]


def pic_glass(x, y, at):
    return [grp([poly([(x - 20, y - 28), (x + 20, y - 28), (x + 3, y), (x + 20, y + 28), (x - 20, y + 28), (x - 3, y)], "rgba(242,201,142,.15)", GOLD, 2),
                 poly([(x - 10, y + 24), (x + 10, y + 24), (x, y + 12)], GOLD)], at, "pop")]


def pic_grapes(x, y, at):
    return grapes(x - 8, y - 26, 44, at, GRAPE) + [lab(x + 26, y + 12, "?", at, LILAC, 32, st="serif")]


def s52():
    """The ledger, row 1: the sagas (a book), Norse buildings (a turf hall), wood cut in 1021 (a ring slice): the Norse at L'Anse aux Meadows,
    about 1021; the sagas' outline (a coast, a spindle, grapes) ticked; Established."""
    ts, tb, tw, to, te = T("s52", "The sagas tell"), T("s52", "Norse buildings"), T("s52", "wood cut"), T("s52", "outline right"), T("s52", "Established")
    els = [rect(110, 128, 1560, 640, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, -1)]
    els += [lab(889, 190, "the weighing", -1, AMBER, 30, st="cap")]
    els += [rect(130, y_ - 46, 1520, 92, "rgba(242,201,142,.03)", "rgba(242,201,142,.26)", 1.5, 12, -1, style="inferred") for y_ in LROWS]
    y = LROWS[0]
    els += lrow(0, ts, pic_book(175, y, ts) + pic_hall(240, y, tb) + pic_slice(300, y + 2, tw), "", None)
    els += [lab(350, y + 11, "the Norse at L'Anse aux Meadows, about 1021", tb + .2, BONE, 30, "start")]
    ox = 1040
    for k, (dx, kind) in enumerate(((0, "coast"), (60, "spin"), (120, "grape"))):
        x = ox + dx
        if kind == "coast":
            els.append(ln([(x - 16, y - 18), (x - 6, y - 4), (x - 14, y + 8), (x - 2, y + 20)], to + .2 * k, "#e9dccb", 3, curve=True, dur=.3))
        elif kind == "spin":
            els += [ln([(x, y - 22), (x, y + 18)], to + .2 * k, "#8a6a48", 3, draw=False), poly(E(x, y + 8, 14, 5, 10), "#7d8a7a", "#d8e0d0", 1.2, to + .2 * k, curve=True, fx="pop")]
        else:
            els += grapes(x - 4, y - 22, 34, to + .2 * k, GRAPE, leaf=False)
        els.append(tick(x + 2, y + 34, to + .2 * k + .2, GOLD, .55, 4))
    els += chip(1250, y, "Established", GRADE["established"], te, 28, "start") + [gl(1400, y, 200, te, .3, "lamp")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s53_add():
    """Rows 2 and 3: the Vinland Map, Ruled out (a modern ink); the Kensington Runestone, Ruled out (a modern language)."""
    tm, tr1, tk, tr2 = T("s53", "Vinland Map"), T("s53", "Ruled out"), T("s53", "Kensington"), T("s53", "Ruled out", k=2)
    els = lrow(1, tm, pic_map(215, LROWS[1], tm), "the Vinland Map", "Ruled out", tr1, GRADE["ruled"])
    els += [lab(760, LROWS[1] + 11, "modern ink", tr1 + .4, "#e98a8a", 26, "start")]
    els += lrow(2, tk, pic_stone(215, LROWS[2], tk), "the Kensington Runestone", "Ruled out", tr2, GRADE["ruled"])
    els += [lab(760, LROWS[2] + 11, "modern language", tr2 + .4, "#e98a8a", 26, "start")]
    return els


def s54_add():
    """Rows 4 and 5: how long they stayed (an hourglass), where Vinland was (grapes and a question): both Open question."""
    th, tw, tq = T("s54", "How long"), T("s54", "where exactly"), T("s54", "Open question")
    els = lrow(3, th, pic_glass(215, LROWS[3], th), "how long they stayed", "Open question", tq, GRADE["open"])
    els += lrow(4, tw, pic_grapes(205, LROWS[4], tw), "where Vinland was", "Open question", tq + .3, GRADE["open"])
    return els


def s55():
    """What would settle the rest: on the Gulf map, a second Norse camp (dashed, with a question) in butternut and grape country, dated by the
    993 signal in its wood; at L'Anse aux Meadows, more pieces of wood with their years still blank."""
    tc, ts, tm = T("s55", "A second"), T("s55", "same signal"), T("s55", "more Norse wood")
    v = VGF
    els = [mapland(v)]
    lx, ly = v.p(*LAM)
    els += [circ(lx, ly, 10, GOLD, at=-1), gl(lx, ly, 70, -1, .6), lab(lx - 20, ly - 26, "L'Anse aux Meadows", -1, GOLD, 28, "end")]
    bp = [v.p(lo, la) for lo, la in BUTTER]
    gp = [v.p(lo, la) for lo, la in GRAPES]
    els += [poly(bp, "rgba(143,217,176,.16)", GREEN, 2, -1, curve=True, style="inferred"), poly(gp, "rgba(142,90,168,.18)", "#c9a0e0", 2, -1, curve=True, style="claimed")]
    hx, hy = v.p(-66.2, 46.6)
    els += [grp(hall_side(hx - 70, hx + 70, hy + 30, 50, 0, "rgba(201,193,238,.25)", door=False, smoke=False), tc, "pop"),
            poly([(hx - 74, hy + 32), (hx - 66, hy - 22), (hx + 66, hy - 22), (hx + 74, hy + 32)], "none", LILAC, 2.5, tc, style="claimed", fx="pop"),
            lab(hx, hy - 50, "a second camp?", tc + .3, LILAC, 32)]
    sx, sy = hx + 150, hy + 10
    els += [grp([circ(sx, sy, 40, "#c9a370", "#4a3322", 5)] + [circ(sx, sy, 8 + 7 * k, "none", "#8c6a48", 1.3) for k in range(4)], ts - .3, "pop"),
            circ(sx, sy, 22, "none", AU, 4, ts, fx="draw", dur=.5), gl(sx, sy, 70, ts, .7), lab(sx, sy + 70, "993", ts + .2, AU, 28, st="serif")]
    for k in range(3):
        x = lx + 70 + 70 * k
        els += [grp([circ(x, ly + 110, 30, "#c9a370", "#4a3322", 4)] + [circ(x, ly + 110, 7 + 6 * j, "none", "#8c6a48", 1.2) for j in range(3)], tm + .2 * k, "pop"),
                rect(x - 30, ly + 152, 60, 30, "none", BONE, 2, 6, tm + .2 * k + .1, style="inferred", fx="pop"), lab(x, ly + 174, "?", tm + .2 * k + .2, BONE, 24)]
    els += [lab(lx + 140, ly + 230, "other years?", tm + .8, BONE, 30)]
    return {"base": "map", "cam": CAM, "els": els}


VCL = View(-77, -50, 39, 54, (90, 120, 1600, 680))          # the close: Newfoundland to New England


def s56():
    """The close at night: L'Anse aux Meadows glows; two dotted lilac zones, the Gulf of St Lawrence shores and the New England coast, each with
    grapes; a small Norse ship between them."""
    tg, tn, ts = T("s56", "Perhaps the shores"), T("s56", "New England"), T("s56", "The sagas remember")
    v = VCL
    els = [mapland(v, landc="#241d16"), rect(-100, -100, 2000, 1200, "rgba(5,8,16,.35)", at=-1)]
    els += [gl(1500, 190, 160, -1, .35, "lamp"), circ(1500, 190, 22, "#efe8da", at=-1)]
    lx, ly = v.p(*LAM)
    els += [circ(lx, ly, 10, GOLD, at=-1), gl(lx, ly, 110, -1, .8), lab(lx + 20, ly - 24, "L'Anse aux Meadows", -1, GOLD, 28, "start")]
    gulf = [v.p(lo, la) for lo, la in ((-66.6, 49.6), (-62.5, 50.2), (-59.4, 50.0), (-59.8, 47.4), (-61.2, 45.6), (-64.0, 45.3), (-66.2, 46.4))]
    newe = [v.p(lo, la) for lo, la in ((-71.4, 43.6), (-69.0, 44.6), (-67.6, 44.3), (-69.6, 41.4), (-71.2, 41.2), (-72.8, 41.0), (-71.8, 42.6))]
    gx, gy = v.p(-63.2, 47.6)
    nx, ny = v.p(-70.4, 42.6)
    els += [poly(gulf, "rgba(201,193,238,.1)", LILAC, 3, tg, style="claimed", curve=True, fx="draw", dur=1.0), gl(gx, gy, 160, tg + .3, .3)]
    els += grapes(gx - 20, gy - 40, 60, tg + .5, GRAPE, style="claimed") + [lab(gx - 160, gy - 90, "Gulf of St Lawrence?", tg + .6, LILAC, 30, "end")]
    els += [poly(newe, "rgba(201,193,238,.1)", LILAC, 3, tn, style="claimed", curve=True, fx="draw", dur=1.0), gl(nx, ny, 150, tn + .3, .3)]
    els += grapes(nx - 20, ny - 40, 56, tn + .5, GRAPE, style="claimed") + [lab(nx + 100, ny + 60, "New England?", tn + .6, LILAC, 30, "start")]
    sx, sy = v.p(-64.0, 43.0)
    els += ship_icon(sx, sy, 60, ts, AU) + [ln([(sx - 80, sy + 20), (sx - 30, sy + 6)], ts + .2, "rgba(242,201,142,.5)", 2, "inferred", .6)]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== stubs (replaced chapter by chapter)
def _stub(name):
    def f():
        return {"base": "dark", "stars": 20, "cam": CAM, "els": [lab(889, 470, name, -1, DIM, 40, st="serif")]}
    return f


def _stub_add():
    return []


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "At the time", "s2"), (1, "And the wood", "s3"), (2, "So did Vikings", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(1, "His son", "s7"), (2, "In one saga", "s8")], {"chapter": "Two sagas, one land"}),
    (1, 1, "collision", "s9", [(1, "They meet the people", "s10")], {}),
    (1, 2, "reversal", "s11", [(1, "In the Saga of the", "s12"), (2, "One saga gives", "s13"), (3, "Think of a family", "s14")], {}),
    (1, 3, "tag", "s15", [(1, "Still, for nine", "s16")], {}),
    (2, 0, "world", "s17", [(1, "At the fishing", "s18")], {"chapter": "Bumps in the grass"}),
    (2, 1, "collision", "s19", [(1, "Under the turf", "s20"), (1, "The biggest hall", "s21"), (2, "And the objects", "s22")], {}),
    (2, 2, "reversal", "s23", [(1, "Here, just a few", "s24"), (2, "That spindle whorl", "s25")], {}),
    (2, 3, "tag", "s26", [], {}),
    (3, 0, "world", "s27", [(1, "The site has", "s28")], {"chapter": "A storm in the tree rings"}),
    (3, 1, "collision", "s29", [(1, "And in {993", "s30"), (2, "A Japanese team", "s31")], {}),
    (3, 2, "reversal", "s32", [(1, "In each, the spike", "s33"), (2, "One was cut", "s34")], {}),
    (3, 3, "tag", "s35", [], {}),
    (4, 0, "world", "s36", [(1, "Butternut trees", "s37")], {"chapter": "Nuts from the south"}),
    (4, 1, "collision", "s38", [(1, "So the archaeologist", "s39")], {}),
    (4, 2, "reversal", "s40", [(1, "So who were", "s41"), (2, "Which of them", "s42")], {}),
    (4, 3, "tag", "s43", [], {}),
    (5, 0, "world", "s44", [(1, "In the {1970s", "s45")], {"chapter": "Too good to be true"}),
    (5, 1, "collision", "s46", [(1, "It's like finding", "s47")], {}),
    (5, 2, "reversal", "s48", [(1, "But its language", "s49")], {}),
    (5, 3, "tag", "s50", [(1, "They dug", "s51")], {}),
    (6, 0, "weigh", "s52", [(2, "The Vinland", "s53"), (3, "How long", "s54")], {"chapter": "The weighing"}),
    (6, 1, "test", "s55", [], {}),
    (6, 2, "close", "s56", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.6, 1222, 600], "s2_add"),
    "s13": ("s12", [1, 889, 500], "s13_add"), "s15": ("s11", [1, 889, 500], "s15_add"), "s16": ("s4", [1.5, 780, 330], "s16_add"),
    "s19": ("s18", [1, 889, 500], "s19_add"), "s25": ("s21", [1.6, 556, 440], "s25_add"), "s26": ("s20", [1, 889, 500], "s26_add"),
    "s31": ("s30", [1, 889, 500], "s31_add"), "s34": ("s32", [1, 889, 500], "s34_add"),
    "s38": ("s37", [1, 889, 500], "s38_add"), "s39": ("s37", [1, 889, 500], "s39_add"),
    "s45": ("s44", [1.6, 830, 398], "s45_add"), "s46": ("s44", [1, 889, 500], "s46_add"),
    "s51": ("s50", [1, 889, 500], "s51_add"),
    "s53": ("s52", [1, 889, 500], "s53_add"), "s54": ("s52", [1, 889, 500], "s54_add"),
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
                panels[sid] = (g.get(sid) or _stub(sid))()
    ids = list(panels) + [a for a in ALIASES]
    idx = {s: i for i, s in enumerate(ids)}
    shots = [panels[s] for s in panels] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[idx[sid]] = idx[root]
        cams[idx[sid]] = [z] + list(cam[1:])
        tags[z] = (g.get(fn) or _stub_add)() if fn else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-vinland", "code": "LF.17", "series": script["series"], "title": script["title"], "case": "vinland",
          "verdict": "solid", "claim": "Did the Norse reach America five centuries before Columbus?", "mood": "mystery",
          "hook_text": "Did Vikings reach America before *Columbus*?", "beats": beats, "shots": shots,
          "sources": "Kuitems et al. 2022 (doi:10.1038/s41586-021-03972-8) · Miyake et al. 2013 (doi:10.1038/ncomms2783) · "
                     "Mekhaldi et al. 2015 (doi:10.1038/ncomms9611) · Ledger et al. 2019 (doi:10.1073/pnas.1907986116) · "
                     "Ingstad & Stine Ingstad 2000 · Wallace 2003, 2006 · Parks Canada · Adam of Bremen c. 1075 · Yale 2021 · "
                     "Brown & Clark 2002 (doi:10.1021/ac025610r) · Williams 2012 · Parcak & Mumford 2017",
          "post": "A thousand years ago someone cut wood with a metal blade at the tip of Newfoundland, and a storm on the Sun gives us the year: 1021. "
                  "The two sagas and where they disagree, the Ingstads' dig, the butternuts from the south, the peoples the Norse met, and the "
                  "Vinland Map, the Kensington Runestone and Point Rosee, weighed.",
          "hashtags": ["#Vikings", "#Vinland", "#Newfoundland", "#LAnseAuxMeadows", "#Archaeology", "#WeighItYourself"],
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
