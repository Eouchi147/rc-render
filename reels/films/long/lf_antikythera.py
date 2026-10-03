"""LF.25 · Sky Watchers · The Antikythera Mechanism: A Cosmos in Bronze (16:9 long film, one wall).

The script is films/long/lf-antikythera/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s59; s4, the title, is the intro card over the panel
of s3), drawn while it is said: the main fragment with its four-spoked wheel (the hero; its X-ray look; again at night for the close), the
night sea of the wreck, the sponge boats' route, the divers and the salvage, the storeroom, the lump that split in 1902 and who saw it,
Price's desk and his jet plane in a tomb, gamma rays and a dentist's X-ray, the 127 teeth and the Moon's 254 laps, Wright's tomography,
spirals and Moon ball, the eight-tonne scanner, the loaf and the coin, the machine's gear train, the Moon's uneven pace, the pin and
slot riding on its nine-year wheel, the back spirals and their eclipse signs, the games dial, the inscriptions, eclipse colours and
winds, the shoebox, the planets' rings, the third that survives, 462 and 442, Venus's rosette, the 69 gears, read versus inferred,
the jam, the timeline of dates, the Corinthian map, the out-of-place claim, the Greek evidence, the hand-cut teeth, the workshop,
Cicero's spheres, the melting pot, the thousand-year gap, the ledger, the tests and the hero at night. Drawings are schematic and true
to the numbers said: solid = measured, dashed = inferred, dotted = claimed (the out-of-place claim and the lost spheres are lilac).

Facts: the script's facts_added (Price 1959, 1974; Jones 2017, 2018, 2020; Wright 1995, 2006, 2007; Freeth et al. 2006, 2008, 2021;
Freeth & Jones 2012; Freeth 2014; Carman & Evans 2014; Anastasiou et al. 2016; Iversen 2017; Voulgaris et al. 2023; Szigety & Arenas
2025; Zapheiropoulou 2012; Ramsey 2012; Hilts 2014; Cicero; the Science Museum and the History of Science Museum, Oxford).

Engine workaround (as in lf_troy.py): the wall only adds elements to a panel on its first visit, at a beat start or a line start;
shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag, invisible); after
the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that step's clock). Build-ins
inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25 syllables a second).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-antikythera/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-antikythera/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-antikythera RC_FILMS_EPS=/tmp/claude-0/sbx_lf-antikythera/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-antikythera/boards python3 films.py long.lf_antikythera
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-antikythera", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
VERD, VERD_L, VERD_D, VERD_DD = "#4f8a78", "#86b8a2", "#2c4f45", "#1b302a"     # corroded bronze: verdigris, its light, its shade
CRUST, CRUST_L = "#6b5a44", "#8d7a5c"                                         # brown crust
BRZ, BRZ_L, BRZ_D = "#b9824a", "#e2b27a", "#6e4a2a"                           # clean bronze (replicas, reconstructions)
WOOD, WOOD_L, WOOD_D = "#6b4a30", "#9a7048", "#3a281a"
SEA_T, SEA_D = "#2d6f8f", "#0f2f40"
XR, XR_L = "#7fc4ff", "#cfe9ff"                                               # X-ray blue
SKIN, CLOTH = "#e8d6b8", "#2a2a33"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#c9e48f", "open": "#f0b06a", "ruled": "#e98a8a"}


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


def E(cx, cy, rx, ry, n=36, a0=0, a1=360):
    pts = ellipse(cx, cy, rx, ry, n, a0, a1)
    return pts[:-1] if (a0, a1) == (0, 360) else pts


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


def blob(cx, cy, rx, ry, n=22, jit=.18, seed=1, rot=0):
    """An irregular closed outline (a lump, a patch of corrosion)."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + rot
        f = 1 + r.uniform(-jit, jit)
        out.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return out


def rot(pts, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


# ================================================================== gears
def teeth_pts(cx, cy, r, n, h=None, a0=0.0, a1=None, phase=0.0, jitter=0.0, seed=1):
    """The outline of triangular teeth on a circle of radius r (pitch radius), n teeth on the full turn; between angles a0..a1 (degrees,
    clockwise from 3 o'clock) when a1 is given (an open zigzag), else the whole closed outline. h = tooth height."""
    h = h if h is not None else max(2.0, min(r * .12, 2 * math.pi * r / n * .9))
    rnd = random.Random(seed)
    p = 360.0 / n
    pts = []
    if a1 is None:
        ks = range(n)
    else:
        k0 = math.ceil((a0 - phase) / p)
        k1 = math.floor((a1 - phase) / p)
        ks = range(k0, k1 + 1)
    for k in ks:
        a = phase + k * p + (rnd.uniform(-jitter, jitter) * p if jitter else 0)
        ar, at_ = math.radians(a - p / 2), math.radians(a)
        pts.append((cx + (r - h / 2) * math.cos(ar), cy + (r - h / 2) * math.sin(ar)))
        pts.append((cx + (r + h / 2) * math.cos(at_), cy + (r + h / 2) * math.sin(at_)))
    if a1 is not None and ks:
        a = phase + ks[-1] * p + p / 2
        pts.append((cx + (r - h / 2) * math.cos(math.radians(a)), cy + (r - h / 2) * math.sin(math.radians(a))))
    return pts


def gear(cx, cy, r, n, at, fill=BRZ, edge=BRZ_L, w=1.4, hole=None, spokes=0, hub=.16, sw=None, h=None, style="known", fx=None, op=None,
         phase=0.0, spoke_rot=0.0, ring=.22):
    """A gear wheel: toothed disc (n teeth), a hub; with spokes, the disc is a rim (ring = its width as a fraction of r) and the openings
    between spokes are painted `hole`. Returns a list of elements (one group when fx is given)."""
    els = [poly(teeth_pts(cx, cy, r, n, h, phase=phase), fill, edge, w, at, style=style)]
    if spokes:
        hc = hole or "#120e0b"
        els.append(circ(cx, cy, r * (1 - ring), hc, "rgba(0,0,0,.4)", 1, at))
        sw = sw or r * .14
        for k in range(spokes):
            a = math.radians(spoke_rot + 360 * k / spokes)
            ux, uy = math.cos(a), math.sin(a)
            vx, vy = -uy, ux
            r0, r1 = r * hub * .8, r * (1 - ring) + 2
            els.append(poly([(cx + ux * r0 + vx * sw * .62, cy + uy * r0 + vy * sw * .62), (cx + ux * r1 + vx * sw * .45, cy + uy * r1 + vy * sw * .45),
                             (cx + ux * r1 - vx * sw * .45, cy + uy * r1 - vy * sw * .45), (cx + ux * r0 - vx * sw * .62, cy + uy * r0 - vy * sw * .62)],
                            fill, edge, w * .8, at, style=style))
        els.append(circ(cx, cy, r * hub, fill, edge, w, at, style=style))
    else:
        els.append(circ(cx, cy, r * hub, "rgba(0,0,0,.35)", edge, w * .8, at, style=style))
    els.append(circ(cx, cy, max(2.5, r * hub * .38), "#120e0b", "none", 0, at))
    if fx:
        e = grp(els, at, fx)
        if op is not None:
            e.update(op=op, keepop=True)
        return [e]
    if op is not None:
        for e in els:
            e.update(op=op, keepop=True)
    return els


def gear_ring(cx, cy, r, n, at, c=XR, w=2, style="known", dur=.8, h=None, phase=0.0, hub=True, op=None):
    """A gear drawn as an outline only (an X-ray trace, a dashed reconstruction): it traces itself."""
    els = [ln(teeth_pts(cx, cy, r, n, h, phase=phase) + teeth_pts(cx, cy, r, n, h, phase=phase)[:1], at, c, w, style, dur=dur, op=op)]
    if hub:
        els.append(circ(cx, cy, max(5, r * .14), "none", c, w * .8, at + dur * .6, fx="draw", dur=.4, style=style, op=op))
    return els


# ================================================================== the main fragment (Fragment A): the hero
FA0 = (1070, 492)                # the wheel's centre in the design coordinates below
FA = (900, 492)                  # where the wheel sits on the panel (the hook title clears above y 180, so the hero can be centred)
FR = 262                         # the wheel's pitch radius (units)
SLAB0 = [(712, 300), (760, 236), (850, 214), (960, 205), (1080, 196), (1190, 214), (1290, 232), (1368, 268), (1420, 330), (1452, 420), (1470, 520),
         (1462, 610), (1430, 690), (1366, 742), (1270, 770), (1160, 778), (1050, 772), (950, 760), (868, 734), (800, 690), (748, 630), (712, 560),
         (700, 470), (700, 380)]


def _jag(pts, amp=11, seed=21):
    """A chipped outline: a displaced point between each pair (the broken edge of a corroded plate)."""
    r = random.Random(seed)
    out = []
    n = len(pts)
    for k in range(n):
        (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % n]
        out.append((x0, y0))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        L = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = (y1 - y0) / L, -(x1 - x0) / L
        d = r.uniform(-amp, amp)
        out.append((mx + nx * d, my + ny * d))
    return out


SLAB0J = _jag(SLAB0)


def FS(p, scale=1.0, dx=0.0, dy=0.0):
    """A design point of the fragment, placed on the panel."""
    return (FA[0] + (p[0] - FA0[0]) * scale + dx, FA[1] + (p[1] - FA0[1]) * scale + dy)


SLAB = [FS(p) for p in SLAB0J]


def frag_a(at=-1, scale=1.0, dx=0.0, dy=0.0, glint=None, lamp=True):
    """The main fragment as it lies in the museum: a slab of corroded bronze, the great four-spoked wheel set in it with its rim of fine
    triangular teeth (223 on the full turn, only the surviving arcs drawn), two smaller gears at the lower right, a sliver of wood,
    cracks, crust and pitting; lit by a lamp from the upper left. scale/dx/dy re-place it. Returns elements (static when at < 0)."""
    S = lambda p: FS(p, scale, dx, dy)
    cx, cy = S(FA0)
    r = FR * scale
    rnd = random.Random(7)
    slab = [S(p) for p in SLAB0J]
    els = [poly([(x + 16 * scale, y + 24 * scale) for x, y in slab], "rgba(0,0,0,.6)", at=at),
           poly(slab, VERD_D, "rgba(170,210,190,.35)", 2, at)]
    # crust and verdigris patches on the plate (kept well inside the outline)
    for k, (px, py, rx, ry, c, o) in enumerate([(820, 330, 70, 48, CRUST, .6), (1330, 330, 60, 70, CRUST, .55), (1240, 700, 110, 46, VERD, .55),
                                                (830, 600, 60, 70, VERD_L, .3), (1390, 560, 40, 90, CRUST_L, .45), (960, 250, 90, 26, VERD_L, .3),
                                                (900, 700, 70, 34, CRUST, .5), (1180, 250, 80, 24, CRUST, .45)]):
        q = blob(*S((px, py)), rx * scale, ry * scale, 18, .22, seed=k + 3)
        els.append(poly(q, c, "none", 0, at, curve=True, op=o))
    # the wheel: the dark well between the spokes, the rim, the teeth that survive, four spokes in a cross, the hub
    els.append(circ(cx, cy, r * .80, VERD_DD, "rgba(0,0,0,.5)", 1.5, at))
    for k in range(9):
        q = blob(cx + rnd.uniform(-.55, .55) * r, cy + rnd.uniform(-.55, .55) * r, rnd.uniform(18, 46) * scale, rnd.uniform(12, 30) * scale, 14, .25, seed=40 + k)
        els.append(poly(q, rnd.choice([VERD_D, "#24423a", CRUST]), "none", 0, at, curve=True, op=.6))
    rim_out = r * .985
    els.append(circ(cx, cy, r * .885, "none", "#3f7464", r * .17, at))                    # the rim as a thick band
    els.append(circ(cx, cy, r * .80, "none", "rgba(200,235,215,.3)", 1.4, at))          # its inner edge
    tooth_h = 2 * math.pi * r / 223 * .95
    for a0, a1 in ((-158, 52), (64, 118)):                                                 # the arcs of teeth that survive
        z = teeth_pts(cx, cy, rim_out, 223, tooth_h, a0, a1, jitter=.12, seed=a0 + 300)
        els.append(ln(z, at, "#7fae98", 1.6, draw=False))
    els.append(circ(cx, cy, r * .965, "none", "rgba(225,245,232,.22)", 1.2, at))
    for k in range(4):
        a = math.radians(-78 + 90 * k)
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        r0, r1 = r * .1, r * .81
        w0, w1 = 30 * scale, 21 * scale
        els.append(poly([(cx + ux * r0 + vx * w0, cy + uy * r0 + vy * w0), (cx + ux * r1 + vx * w1, cy + uy * r1 + vy * w1),
                         (cx + ux * r1 - vx * w1, cy + uy * r1 - vy * w1), (cx + ux * r0 - vx * w0, cy + uy * r0 - vy * w0)],
                        "#477f6d", "rgba(210,240,225,.4)", 1.2, at))
    hub = [(cx - 34 * scale, cy - 30 * scale), (cx + 32 * scale, cy - 34 * scale), (cx + 36 * scale, cy + 30 * scale), (cx - 30 * scale, cy + 34 * scale)]
    els += [poly(hub, "#5f9a86", "rgba(230,250,240,.45)", 1.2, at), circ(cx, cy, 12 * scale, VERD_DD, "none", 0, at)]
    # corrosion over the wheel: crusts that bury parts of the rim and the spokes
    for k, (px, py, rx, ry, c, o) in enumerate([(1180, 300, 44, 22, CRUST, .7), (1250, 520, 30, 52, CRUST, .6), (960, 560, 52, 30, VERD_D, .7),
                                                (1110, 690, 60, 20, CRUST_L, .5), (1020, 330, 26, 16, VERD_L, .35), (860, 440, 22, 40, CRUST, .55)]):
        els.append(poly(blob(*S((px, py)), rx * scale, ry * scale, 16, .25, seed=70 + k), c, "none", 0, at, curve=True, op=o))
    # the broken lower left: the slab's crust over the rim
    els.append(poly([S(p) for p in [(780, 640), (840, 610), (900, 660), (960, 700), (1010, 756), (950, 762), (868, 736), (800, 690)]], CRUST, "none", 0, at, curve=True, op=.85))
    # two smaller gears at the lower right, half buried
    for (gx, gy, gr, gn, ph) in ((1356, 650, 66, 38, 3), (1262, 718, 44, 24, 8)):
        x_, y_ = S((gx, gy))
        els.append(ln(teeth_pts(x_, y_, gr * scale, gn, None, -170, 20, phase=ph), at, "#7fae98", 1.6, draw=False))
        els.append(circ(x_, y_, gr * scale * .78, "none", "rgba(160,205,185,.45)", 1.4, at))
        els.append(circ(x_, y_, gr * scale * .16, VERD_L, "none", 0, at, op=.8))
    # a sliver of the wooden case at the left edge
    wood = [S(p) for p in [(704, 400), (724, 392), (736, 520), (724, 600), (708, 560)]]
    els.append(poly(wood, WOOD, "rgba(220,170,120,.35)", 1, at))
    for k in range(4):
        y_ = 420 + 40 * k
        els.append(ln([S((710, y_)), S((728, y_ + 18))], at, "rgba(40,25,15,.6)", 1.2, draw=False))
    # pitting and cracks
    for k in range(46):
        x_, y_ = S((rnd.uniform(730, 1440), rnd.uniform(230, 750)))
        els.append(dot(round(x_, 1), round(y_, 1), round(rnd.uniform(1.2, 3.2) * scale, 1), "rgba(10,18,15,.55)", at, None))
    for pts_ in ([(760, 260), (800, 300), (812, 360)], [(1400, 380), (1430, 450), (1452, 470)], [(1180, 760), (1210, 720), (1260, 706)],
                 [(990, 210), (1000, 240), (985, 262)], [(1290, 240), (1272, 286), (1300, 330)]):
        els.append(ln([S(p) for p in pts_], at, "rgba(10,14,12,.85)", 2.2 * scale, draw=False))
    # the light: a highlight from the upper left fading to shade at the lower right, a warm lamp, a rim light on the upper edges
    els.append(poly(slab, "url(#k-shade)", "none", 0, at))
    if lamp:
        els += [gl(cx - .55 * r, cy - .55 * r, 420 * scale, at, .26, "lamp"), ln(slab[:17], at, "rgba(255,236,206,.5)", 2, draw=False)]
    if glint is not None:                                      # the teeth catch the light, one by one along the upper rim
        for k, a in enumerate(range(-150, 40, 6)):
            ar = math.radians(a)
            els.append(dot(round(cx + rim_out * math.cos(ar), 1), round(cy + rim_out * math.sin(ar), 1), round(3.4 * scale, 1), "#ffe9b0",
                           round(glint + .035 * k, 2)))
        els.append(gl(cx + .2 * r, cy - .95 * r, 240 * scale, glint + .2, .35, "lamp"))
    return els


# ================================================================== figures
def fig(x, y, h, at, c="#1a1410", arms=None, face=1, fx="rise", op=None, rim=None, hat=False, coat=False):
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up', 'hold' (both forward), 'lift' (both up)."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: y - b * h
    els = [circ(X(.01), Y(.9), .085 * h, c, at=at),
           poly([(X(-.13), Y(.78)), (X(.13), Y(.78)), (X(.11), Y(.44)), (X(-.11), Y(.44))], c, at=at),
           poly([(X(-.11), Y(.46)), (X(.11), Y(.46)), (X(.085), Y(0)), (X(.025), Y(0)), (X(0), Y(.3)), (X(-.025), Y(0)), (X(-.085), Y(0))], c, at=at)]
    if coat:
        els.append(poly([(X(-.13), Y(.76)), (X(.13), Y(.76)), (X(.16), Y(.3)), (X(-.16), Y(.3))], c, at=at))
    if hat:
        els += [rect(X(-.07) if f > 0 else X(.07) - .14 * h, Y(1.06), .14 * h, .1 * h, c, at=at), rect(X(-.11) if f > 0 else X(.11) - .22 * h, Y(.97), .22 * h, .025 * h, c, at=at)]
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
    e = grp(els, at, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return [e]


def seated(x, y, h, at, c=SKIN, stool=True, face=1, fx="rise"):
    """A figure seated on a stool facing right (face=1) or left, arms forward to a bench; feet on y, h = standing height."""
    f = face
    X = lambda a: x + f * a
    out = []
    if stool:
        out.append(rect(min(X(-.13 * h), X(.07 * h)), y - .25 * h, .2 * h, .25 * h, "#3a2c20", "#8a6a48", 1.5, 3, at))
    out += [poly([[X(-.07 * h), y - .63 * h], [X(.11 * h), y - .63 * h], [X(.1 * h), y - .29 * h], [X(-.1 * h), y - .29 * h]], c, at=at),
            poly([[X(-.1 * h), y - .33 * h], [X(.25 * h), y - .33 * h], [X(.26 * h), y - .25 * h], [X(-.1 * h), y - .24 * h]], c, at=at),
            poly([[X(.19 * h), y - .27 * h], [X(.26 * h), y - .27 * h], [X(.27 * h), y], [X(.18 * h), y]], c, at=at),
            circ(X(.06 * h), y - .72 * h, .075 * h, c, at=at),
            ln([[X(.06 * h), y - .58 * h], [X(.22 * h), y - .5 * h], [X(.34 * h), y - .46 * h]], at, c, max(3, .05 * h), draw=False)]
    return [grp(out, at, fx)]


def helmet_diver(x, y, h, at, c="#2a2622", fx="rise"):
    """A diver in standard dress (1900): a round metal helmet with a window, a heavy suit, weighted boots; feet on y."""
    X = lambda a: x + a * h
    Y = lambda b: y - b * h
    els = [poly([(X(-.16), Y(.74)), (X(.16), Y(.74)), (X(.17), Y(.36)), (X(-.17), Y(.36))], c, "rgba(220,200,170,.35)", 1, at),
           poly([(X(-.16), Y(.38)), (X(.16), Y(.38)), (X(.13), Y(.04)), (X(.03), Y(.04)), (X(0), Y(.28)), (X(-.03), Y(.04)), (X(-.13), Y(.04))], c, "rgba(220,200,170,.3)", 1, at),
           rect(X(-.15), Y(.06), .12 * h, .06 * h, "#111", at=at), rect(X(.03), Y(.06), .12 * h, .06 * h, "#111", at=at),
           ln([(X(-.15), Y(.72)), (X(-.22), Y(.44))], at, c, .07 * h, draw=False), ln([(X(.15), Y(.72)), (X(.24), Y(.5))], at, c, .07 * h, draw=False),
           circ(X(0), Y(.88), .14 * h, "#b98a52", "#f0cf98", 1.5, at), circ(X(.04), Y(.89), .065 * h, "#2a3a44", "#f0cf98", 1.2, at),
           rect(X(-.13), Y(.77), .26 * h, .05 * h, "#9a7040", at=at)]
    return [grp(els, at, fx)]


def amphora(x, y, h, at, c="#a8693e", tilt=0, fx=None):
    """An amphora (base point at (x, y)), lying at `tilt` degrees."""
    body = [(x, y), (x - .14 * h, y - .25 * h), (x - .18 * h, y - .55 * h), (x - .12 * h, y - .78 * h), (x - .05 * h, y - .84 * h), (x - .05 * h, y - .95 * h),
            (x + .05 * h, y - .95 * h), (x + .05 * h, y - .84 * h), (x + .12 * h, y - .78 * h), (x + .18 * h, y - .55 * h), (x + .14 * h, y - .25 * h)]
    body = rot(body, x, y, tilt)
    hl = rot([(x - .05 * h, y - .9 * h), (x - .14 * h, y - .88 * h), (x - .12 * h, y - .74 * h)], x, y, tilt)
    hr = rot([(x + .05 * h, y - .9 * h), (x + .14 * h, y - .88 * h), (x + .12 * h, y - .74 * h)], x, y, tilt)
    els = [poly(body, c, "rgba(255,220,180,.35)", 1.2, at, curve=True), ln(hl, at, c, max(2, .03 * h), draw=False), ln(hr, at, c, max(2, .03 * h), draw=False)]
    return [grp(els, at, fx)] if fx else els


def statue_lying(x, y, L, at, c, edge, face=1, fx=None, op=None):
    """A statue lying on its back on the seabed (side view): head, torso, legs; (x, y) = its middle on the ground, L = length."""
    f = face
    X = lambda a: x + f * a * L
    els = [poly([(X(-.5), y - .06 * L), (X(-.38), y - .1 * L), (X(-.05), y - .11 * L), (X(.12), y - .08 * L), (X(.48), y - .05 * L), (X(.5), y), (X(-.5), y)],
                c, edge, 1.2, at, curve=True),
           circ(X(-.56), y - .07 * L, .065 * L, c, edge, 1.2, at),
           ln([(X(-.3), y - .1 * L), (X(-.12), y - .2 * L), (X(.0), y - .17 * L)], at, c, .05 * L, draw=False)]
    if fx:
        e = grp(els, at, fx)
        if op is not None:
            e.update(op=op, keepop=True)
        return [e]
    return els


def moonball(x, y, r, at, phase=.5, fx="pop", rot_=0):
    """The Moon-phase ball: half white, half black; `phase` 0..1 = how much of the white half faces us (0 new, .5 half, 1 full)."""
    els = [circ(x, y, r, "#14110f", "rgba(255,240,215,.7)", 1.6, at)]
    if phase > .02:
        k = math.cos(math.pi * phase)                     # the terminator: an ellipse of half-width k*r (k > 0 a crescent, k < 0 gibbous)
        pts = E(x, y, r, r, 36, -90, 90) + [(x + k * r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(90, -91, -10)]
        els.append(poly(rot(pts, x, y, rot_), "#f3ead6", "none", 0, at))
    els.append(circ(x, y, r, "none", "rgba(255,240,215,.7)", 1.4, at))
    return [grp(els, at, fx)] if fx else els


# ================================================================== COLD OPEN
def s1():
    """The hero image, complete from the first frame: the main fragment on a dark museum ground, the great four-spoked wheel set in its
    corroded bronze; on 'with teeth', the teeth of the upper rim catch the light one by one."""
    tg = T("s1", "with teeth")
    els = [rect(560, 760, 1060, 40, "rgba(255,236,206,.04)", "none", 0, 18, -1),
           gl(1090, 470, 760, -1, .16, "lamp")]
    els += frag_a(-1, glint=tg)
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s2_add():
    """The X-ray look: the slab darkens to a radiograph; the great wheel and hidden gear wheels trace themselves inside it (the ones behind
    dimmer), a count of thirty; rows of tiny letters, and a magnifier on three of them (2 mm)."""
    tx, tl = T("s2", "X-rays"), T("s2", "thousands of Greek")
    cx, cy = FA
    els = [poly(SLAB, "rgba(6,18,38,.82)", "rgba(159,208,255,.7)", 2, tx, fx="fade", dur=.8),
           gl(cx, cy, 560, tx + .3, .22, "glowb")]
    els += gear_ring(cx, cy, FR * .985, 223, tx + .4, XR_L, 1.6, dur=1.0, h=4.5, hub=False)
    for k in range(4):
        a = math.radians(-78 + 90 * k)
        els.append(ln([(cx + 26 * math.cos(a), cy + 26 * math.sin(a)), (cx + FR * .8 * math.cos(a), cy + FR * .8 * math.sin(a))], tx + .6, XR_L, 2, dur=.5))
    hidden = [((1070, 492), 150, 64, .55), ((860, 340), 62, 38, 1), ((1290, 400), 84, 48, .55), ((880, 600), 52, 24, 1), ((1240, 640), 72, 38, 1),
              ((1160, 300), 44, 32, .55), ((1000, 690), 40, 20, .55), ((1380, 540), 46, 30, 1), ((790, 470), 40, 22, .55), ((1100, 610), 34, 15, 1),
              ((1356, 650), 66, 38, 1), ((960, 400), 30, 15, .55)]
    for k, (p, r, n, o) in enumerate(hidden):
        x, y = FS(p)
        els += gear_ring(x, y, r, n, tx + 1.0 + .22 * k, XR_L if o == 1 else XR, 2 if o == 1 else 1.6, dur=.6, op=o)
    els += [lab(1470, 262, "30 gear wheels", tx + 3.6, XR_L, 32, "start", fx="pop"), ln([(1460, 274), (1330, 330)], tx + 3.6, XR_L, 1.4, dur=.3)]
    x0, y0 = FS((880, 712))
    els += [{"k": "glyphs", "x": round(x0, 1), "y": round(y0, 1), "w": 420, "h": 46, "rows": 3, "cols": 22, "kind": "latin", "c": XR_L, "in": round(tl, 2), "op": .95},
            ln([(x0 - 6, y0 + 30), (420, 660)], tl + .5, XR_L, 1.6, dur=.4),
            circ(330, 640, 96, "rgba(12,24,40,.94)", XR_L, 3, tl + .7, fx="pop"),
            lab(330, 666, "KAI", tl + .9, XR_L, 64, st="serif", fx="pop"),
            ln([(280, 708), (380, 708)], tl + 1.2, GOLD, 3, dur=.3),
            lab(330, 770, "2 mm", tl + 1.3, GOLD, 26)]
    return els


def roman_ship(cx, wl, L, at=-1, tilt=0.0, c="#1c1612", sail="#cdb48a"):
    """A Roman-era merchant ship in side view: a deep rounded hull, a stern post curling up, one mast and a square sail."""
    P = lambda a, b: (cx + a * L, wl + b * L)
    hull = [P(-.5, -.16), P(-.46, -.02), P(-.36, .07), P(0, .1), P(.36, .07), P(.47, -.02), P(.52, -.12), P(.48, -.2), P(.45, -.12), P(.4, -.06), P(-.42, -.06)]
    mast = [P(-.02, -.06), P(-.02, -.66)]
    sl = [P(-.24, -.6), P(.2, -.6), P(.22, -.22), P(-.26, -.22)]
    pts = lambda q: rot(q, cx, wl, tilt)
    return [poly(pts(hull), c, "rgba(255,226,190,.35)", 1.4, at, curve=True), ln(pts(mast), at, c, max(3, .014 * L), draw=False),
            poly(pts(sl), sail, "rgba(60,40,20,.5)", 1.2, at, op=.85), ln(pts([P(-.27, -.6), P(.23, -.6)]), at, c, max(3, .01 * L), draw=False)]


def ghost_machine(x, y, s, at, c=LILAC, style="claimed", op=1.0):
    """The machine as a guess (lilac, dotted): a case with a round front dial and pointers, and behind it the back plate with its two
    spirals, glimpsed."""
    bx, by = x + 40 * s, y - 30 * s
    els = [rect(bx, by, 300 * s, 230 * s, "rgba(201,193,238,.04)", c, 2, 8 * s, at, style=style, op=op * .7),
           ln(spiral_pts(bx + 230 * s, by + 60 * s, 8 * s, 40 * s, 3, n=120), at, c, 1.6, style, draw=False, op=op * .7),
           ln(spiral_pts(bx + 230 * s, by + 160 * s, 8 * s, 36 * s, 3, n=120), at, c, 1.6, style, draw=False, op=op * .7),
           rect(x, y, 300 * s, 230 * s, "rgba(201,193,238,.08)", c, 3, 8 * s, at, style=style, op=op),
           circ(x + 150 * s, y + 115 * s, 86 * s, "none", c, 3, at, style=style, op=op),
           circ(x + 150 * s, y + 115 * s, 62 * s, "none", c, 2, at, style=style, op=op),
           ln([(x + 150 * s, y + 115 * s), (x + 210 * s, y + 70 * s)], at, c, 3, style, draw=False, op=op),
           ln([(x + 150 * s, y + 115 * s), (x + 110 * s, y + 175 * s)], at, c, 3, style, draw=False, op=op),
           circ(x + 300 * s, y + 115 * s, 10 * s, "none", c, 2.5, at, style=style, op=op)]
    return [grp(els, at, "pop")]


def s3():
    """The night sea: a merchant ship settles at the surface, a dashed fall to the seabed where the green lump lies among amphorae
    (about 60 BCE); the machine appears as a lilac guess above it; a question."""
    t0, tc, tw = T("s3", "The ship sank"), T("s3", "A computer"), T("s3", "what did it do")
    els = [{"k": "water", "y": 380, "h": 700, "op": .92, "in": -1},
           poly([(-40, 790), (300, 760), (620, 778), (900, 760), (1200, 772), (1500, 752), (1820, 776), (1820, 1000), (-40, 1000)], "#3a3226", "rgba(255,226,190,.3)", 1.4, -1, curve=True)]
    els += roman_ship(470, 380, 300, -1, tilt=-7)
    els += [ln([(500, 410), (560, 520), (660, 640), (760, 742)], t0 + .2, "rgba(232,184,122,.8)", 2.5, "inferred", dur=1.4, curve=True)]
    els += amphora(690, 770, 60, t0 + 1.0, tilt=78) + amphora(840, 768, 54, t0 + 1.1, tilt=-96) + amphora(900, 772, 50, t0 + 1.2, tilt=104)
    els += [poly(blob(770, 748, 40, 22, 16, .2, 5), VERD, "rgba(190,230,210,.6)", 1.5, t0 + 1.4, fx="pop"),
            gl(770, 742, 90, t0 + 1.5, .45, "lamp")]
    els += chip(1010, 700, "about 60 BCE", GOLD, t0 + .6, 28)
    els += [ln([(800, 735), (1000, 640), (1170, 560)], tc, "rgba(201,193,238,.7)", 2, "claimed", dur=.8, curve=True)]
    els += ghost_machine(1170, 420, 1.0, tc + .4)
    els += qmark(1610, 560, tw, 120)
    return {"base": "sky", "tod": "night", "ground": 1200, "sun": False, "moon": [1460, 200, 30], "cam": CAM, "els": els}


def s59():
    """The close: the hero again, at night, on its own panel: stars over the slab, the teeth of the great wheel glowing in a slow sweep as
    'someone cut those teeth by hand' is said, a soft breathing lamp."""
    tt = T("s59", "someone cut")
    els = [rect(380, 760, 1020, 40, "rgba(255,236,206,.04)", "none", 0, 18, -1), gl(900, 470, 760, -1, .14, "lamp")]
    els += frag_a(-1)
    for k, a in enumerate(range(-150, 40, 5)):
        ar = math.radians(a)
        els.append(dot(round(FA[0] + FR * .985 * math.cos(ar), 1), round(FA[1] + FR * .985 * math.sin(ar), 1), 3.6, "#ffd98a", round(tt + .06 * k, 2)))
    els += [gl(FA[0], FA[1] - 40, 520, tt + .4, .3, "lamp", pulse=True)]
    return {"base": "dark", "stars": 120, "cam": CAM, "els": els}


# ================================================================== CHAPTER 1 · A wreck full of statues
VMED = View(8.5, 29.5, 31.0, 40.0, (90, 120, 1600, 680))


def storm(x, y, s, at):
    """A storm cloud with slanting rain."""
    els = [poly(blob(x, y, 70 * s, 34 * s, 18, .16, 9), "#5b6470", "rgba(230,236,245,.5)", 1.4, at, curve=True),
           poly(blob(x - 40 * s, y + 10 * s, 46 * s, 26 * s, 14, .15, 4), "#4a525e", "none", 0, at, curve=True)]
    els += [ln([(x - 50 * s + 22 * s * k, y + 30 * s), (x - 64 * s + 22 * s * k, y + 70 * s)], at, "rgba(159,208,255,.75)", 2, draw=False) for k in range(6)]
    return [grp(els, at, "pop")]


def boat_icon(x, y, s, at, c=GOLD, fx="pop"):
    """A small sailing boat pictogram (s = its length)."""
    P = lambda a, b: (x + a * s, y + b * s)
    els = [poly([P(-.5, -.12), P(-.38, .06), P(.38, .06), P(.5, -.12)], c, at=at),
           ln([P(0, -.1), P(0, -.62)], at, c, max(1.5, s * .03), draw=False),
           poly([P(.02, -.58), P(.3, -.16), P(.02, -.16)], c, at=at, op=.85)]
    return [grp(els, at, fx)]


def s5():
    """Where: Tunisian waters to Symi; the storm at Antikythera, between Kythera and Crete, where the sponge boats sheltered."""
    v = VMED
    t0, ts = T("s5", "Sponge divers"), T("s5", "shelter from a storm")
    route = [(11.4, 34.5), (13.5, 34.4), (16, 34.6), (19, 35.1), (21.6, 35.6), (23.1, 35.85)]
    home = [(23.5, 35.95), (25.2, 36.1), (26.6, 36.4), (27.75, 36.58)]
    ax, ay = v.p(23.3, 35.87)
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(9.6, 33.4), "Tunisia", .6, "#cbbca8", 30),
           lab(*v.p(22.0, 39.4), "Greece", .8, "#cbbca8", 30),
           lab(*v.p(24.9, 34.75), "Crete", 1.0, "#cbbca8", 28),
           pin(*v.p(27.84, 36.6), "Symi", t0 + .2, AMBER, "start", 18, -14),
           ln([v.p(*q) for q in route], t0 + .6, GOLD, 4, "claimed", dur=2.0, curve=True),
           ln([v.p(*q) for q in home], t0 + 2.4, "rgba(242,201,142,.5)", 3, "claimed", dur=1.0, curve=True)]
    els += boat_icon(ax - 52, ay - 2, 56, t0 + 2.6)
    els += storm(ax + 20, ay - 92, .85, ts)
    els += [pin(ax, ay, "Antikythera", ts + .6, GOLD, "end", -20, 40),
            {"k": "scale", "x": 150, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": 1.4}]
    return {"base": "map", "cam": CAM, "els": els}


def bronze_arm(x, y, s, at, ang=-60, fx="rise"):
    """A larger-than-life bronze arm, bent at the elbow, with its hand: the shoulder end at (x, y), raised at `ang` degrees (s = its length)."""
    pts = [(0, -.09), (.42, -.07), (.5, -.1), (.58, -.16), (.86, -.3), (.92, -.3), (.98, -.36), (1.05, -.4), (1.07, -.36), (1.0, -.3), (1.06, -.27),
           (1.02, -.22), (.94, -.2), (.88, -.18), (.62, -.04), (.52, .05), (.4, .08), (0, .08)]
    pts = rot([(x + px * s, y + py * s) for px, py in pts], x, y, ang)
    els = [poly(pts, "#56634a", "rgba(230,215,170,.65)", 1.6, at, curve=True),
           ln(rot([(x + .06 * s, y - .04 * s), (x + .44 * s, y - .03 * s), (x + .84 * s, y - .25 * s)], x, y, ang), at, "rgba(235,220,180,.45)", 2.5, draw=False, curve=True)]
    return [grp(els, at, fx)]


def s6():
    """Under the boat: a diver in a metal helmet goes down the line, more than forty metres, to a wreck heaped with bronze and marble
    statues; a bronze arm, larger than life, comes up."""
    t0, tw, ts, ta = T("s6", "One of them"), T("s6", "finds a wreck"), T("s6", "bronze and marble"), T("s6", "bronze arm")
    sea_y, bed = 220, 700
    els = [{"k": "water", "y": sea_y, "h": 820, "op": .95, "in": -1},
           poly([(-40, bed - 40), (400, bed - 20), (800, bed), (1200, bed + 30), (1820, bed + 60), (1820, 1000), (-40, 1000)], "#4a4032", "rgba(255,226,190,.25)", 1.4, -1, curve=True)]
    # the sponge boat at the surface and the diver's line
    els += [poly([(260, sea_y - 6), (300, sea_y + 18), (430, sea_y + 18), (470, sea_y - 8), (440, sea_y - 2), (290, sea_y - 2)], "#2a1e16", "rgba(255,226,190,.4)", 1.2, -1),
            ln([(370, sea_y - 2), (370, sea_y - 90)], -1, "#2a1e16", 4, draw=False),
            poly([(374, sea_y - 86), (440, sea_y - 20), (374, sea_y - 20)], "#cdb48a", "none", 0, -1, op=.85),
            ln([(420, sea_y + 14), (470, 330), (520, 420)], t0, "rgba(233,220,192,.7)", 2, dur=.8, curve=True)]
    els += helmet_diver(520, 520, 110, t0 + .3)
    els += [lab(600, 460, "Elias Stadiatis", t0 + .6, BONE, 28, "start")]
    # the depth bar
    els += [ln([(170, sea_y + 4), (170, bed - 34)], t0 + .9, GOLD, 2.5, dur=.9),
            ln([(158, sea_y + 4), (182, sea_y + 4)], t0 + .9, GOLD, 2.5, draw=False), ln([(158, bed - 34), (182, bed - 34)], t0 + 1.6, GOLD, 2.5, draw=False),
            lab(190, 452, "more than 40 m", t0 + 1.6, GOLD, 28, "start")]
    # the wreck: timbers, amphorae, statues in heaps
    els += [ln([(860, bed + 6), (1120, bed + 26)], tw, "#3a2a1e", 9, dur=.5), ln([(940, bed - 4), (1300, bed + 30)], tw + .2, "#3a2a1e", 7, dur=.5),
            ln([(1240, bed + 14), (1520, bed + 40)], tw + .3, "#3a2a1e", 8, dur=.5)]
    els += amphora(1000, bed + 8, 70, tw + .4, tilt=86) + amphora(1420, bed + 30, 64, tw + .5, tilt=-80) + amphora(1580, bed + 44, 60, tw + .6, tilt=96)
    for k, (x, y, L, c, e) in enumerate([(1080, bed + 4, 200, "#4f5a44", "rgba(220,200,150,.6)"), (1300, bed + 16, 180, "#d9d2c2", "rgba(255,250,240,.6)"),
                                         (1190, bed - 26, 170, "#e3dccd", "rgba(255,250,240,.6)"), (1450, bed + 18, 150, "#4f5a44", "rgba(220,200,150,.6)")]):
        els += statue_lying(x, y, L, ts + .3 * k, c, e, face=1 if k % 2 else -1, fx="rise")
    els += [lab(1250, bed - 110, "bronze and marble statues", ts + 1.0, BONE, 28)]
    els += bronze_arm(640, 380, 190, ta, ang=-58) + [gl(720, 300, 160, ta + .3, .4, "lamp"), lab(800, 250, "a bronze arm", ta + .5, GOLD, 30, "start")]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [1540, 110, 22], "cam": CAM, "els": els}


def steamship(cx, wl, L, at=-1):
    """A grey navy steamship of 1900 in side view: a long hull, a deckhouse, a funnel with smoke, two masts."""
    P = lambda a, b: (cx + a * L, wl + b * L)
    els = [poly([P(-.5, -.08), P(-.46, .04), P(.42, .04), P(.5, -.1), P(.44, -.06), P(-.44, -.06)], "#3c4148", "rgba(230,236,245,.4)", 1.2, at),
           rect(*P(-.18, -.14), .34 * L, .08 * L, "#4d535b", "rgba(230,236,245,.3)", 1, 2, at),
           rect(*P(-.04, -.26), .06 * L, .14 * L, "#2b2f35", "rgba(230,236,245,.3)", 1, 2, at),
           ln([P(-.34, -.06), P(-.34, -.4)], at, "#2b2f35", 3, draw=False), ln([P(.3, -.06), P(.3, -.36)], at, "#2b2f35", 3, draw=False)]
    els += [poly(blob(*P(-.08 - .06 * k, -.32 - .05 * k), (.04 + .015 * k) * L, (.025 + .01 * k) * L, 12, .2, k + 5), "rgba(120,110,105,.5)", at=at, curve=True) for k in range(3)]
    return els


def s7():
    """The salvage, November 1900 to September 1901: a navy steamship and the sponge boat, the air pump turned by two men, hoses down to
    a diver in a metal helmet; five minutes on the bottom; a single lamp on the water for the diver who died."""
    t0, th, t5, td = T("s7", "From November"), T("s7", "metal helmets"), T("s7", "five minutes"), T("s7", "One diver dies")
    wl = 430
    els = [{"k": "water", "y": wl, "h": 640, "op": .95, "in": -1}]
    els += steamship(1220, wl, 620, -1)
    # the sponge boat with its pump
    els += [poly([(330, wl - 8), (370, wl + 22), (650, wl + 22), (700, wl - 10), (660, wl - 2), (360, wl - 2)], "#3a2a1e", "rgba(255,226,190,.4)", 1.2, -1),
            ln([(520, wl - 2), (520, wl - 150)], -1, "#2a1e16", 4, draw=False)]
    els += [circ(560, wl - 44, 30, "none", "#c9a46a", 4, t0 + .4, fx="draw", dur=.5)] + \
           [ln([(560 - 28 * math.cos(math.radians(a)), wl - 44 - 28 * math.sin(math.radians(a))), (560 + 28 * math.cos(math.radians(a)), wl - 44 + 28 * math.sin(math.radians(a)))], t0 + .6, "#c9a46a", 2.5, draw=False) for a in (0, 60, 120)]
    els += fig(500, wl - 4, 66, t0 + .7, "#1a1410", arms="hold") + fig(626, wl - 4, 66, t0 + .8, "#1a1410", arms="hold", face=-1)
    els += chip(889, 170, "Nov 1900 to Sept 1901", GOLD, t0 + .2, 28)
    # hoses down to the diver
    els += [ln([(580, wl - 20), (600, wl + 60), (650, 560), (700, 640)], th - .4, "#d8c9a8", 2.2, dur=.8, curve=True),
            ln([(590, wl - 18), (614, wl + 60), (668, 560), (712, 642)], th - .3, "#a89a7a", 1.6, dur=.8, curve=True)]
    els += helmet_diver(720, 772, 120, th)
    els += [lab(800, 690, "metal helmets", th + .4, BONE, 28, "start")]
    els += [circ(980, 560, 38, "rgba(18,13,10,.85)", BONE, 2.5, t5, fx="pop"),
            poly([(980, 560), (980, 522)] + [(980 + 38 * math.sin(math.radians(a)), 560 - 38 * math.cos(math.radians(a))) for a in range(0, 31, 5)], AMBER, at=t5 + .2, fx="pop"),
            lab(1030, 570, "five minutes", t5 + .3, AMBER, 28, "start")]
    els += [gl(250, wl - 6, 90, td, .7, "lamp", pulse=True), dot(250, wl - 8, 5, "#ffe2a8", td),
            lab(250, wl + 64, "one died, two paralysed", td + .4, DIM, 26)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [1600, 360, 26], "cam": CAM, "els": els}


def amph_up(x, y, h, at, c="#a8693e"):
    return amphora(x, y, h, at, c, 0)


def plinth(x, y, w, at, c="#5a4a3a"):
    return rect(x - w / 2, y - 22, w, 22, c, "rgba(255,236,206,.3)", 1.2, 2, at)


def s8():
    """The storeroom in Athens: the bronze youth on his plinth, damaged marble figures, amphorae and glass; on a shelf, three shapeless
    green lumps."""
    t0, tl = T("s8", "Up come"), T("s8", "shapeless lumps")
    fl = 720
    els = [rect(80, fl, 1620, 10, "#3a2c20", at=-1), gl(889, 420, 900, -1, .14, "lamp")]
    # the bronze youth: standing on a plinth, the right arm raised
    els += [plinth(400, fl, 130, t0), gl(410, 470, 220, t0 + .2, .28, "lamp")]
    els += fig(400, fl - 22, 330, t0, "#56634a", arms="up", rim="rgba(240,220,170,.75)")
    els += [lab(400, 300, "bronze", t0 + .5, GOLD, 26)]
    # marble figures, damaged: one headless, one without its arms
    els += [plinth(640, fl, 100, t0 + .6), plinth(800, fl, 100, t0 + .8)]
    m1 = fig(640, fl - 22, 250, t0 + .6, "#ddd5c4", arms="hold", rim="rgba(255,255,255,.7)")
    m1[0]["els"] = m1[0]["els"][1:]                     # headless
    m2 = fig(800, fl - 22, 236, t0 + .8, "#d6cdbb", rim="rgba(255,255,255,.7)")
    m2[0]["els"] = [e for e in m2[0]["els"] if e.get("k") != "line" or e.get("c") != "#d6cdbb"]   # armless
    els += m1 + m2 + [lab(720, 420, "marble", t0 + 1.0, BONE, 26)]
    els += amph_up(940, fl, 110, t0 + 1.2) + amph_up(1010, fl, 96, t0 + 1.3) + amph_up(1070, fl, 104, t0 + 1.4)
    for k, x in enumerate((1160, 1225)):
        els += [poly(E(x, fl - 24, 30, 22, 18, 0, 180), "rgba(159,208,255,.25)", "rgba(200,230,255,.8)", 1.6, t0 + 1.6 + .1 * k, fx="pop")]
    els += [lab(1050, 570, "glass and pottery", t0 + 1.8, BONE, 26)]
    # the shelf of lumps
    els += [rect(1300, 540, 330, 12, "#5a4430", at=-1), rect(1310, 552, 10, 168, "#3a2c20", at=-1), rect(1610, 552, 10, 168, "#3a2c20", at=-1)]
    for k, (x, rx) in enumerate([(1360, 44), (1460, 52), (1565, 38)]):
        els.append(poly(blob(x, 540 - 26, rx, 26, 16, .25, 11 + k), VERD_D, "rgba(170,210,190,.5)", 1.4, tl + .2 * k, fx="pop"))
    els += [lab(1465, 450, "bronze and wood lumps", tl + .8, GOLD, 28)]
    els += chip(1465, 200, "Athens", AMBER, tl + 1.5, 28)
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


LUMP0 = [(640, 470), (690, 380), (790, 330), (900, 318), (1010, 330), (1110, 372), (1160, 450), (1150, 540), (1080, 600), (960, 622), (840, 616), (730, 584), (668, 530)]
LUMP = _jag([(900 + (x - 900) * 1.25, 470 + (y - 470) * 1.25) for x, y in LUMP0], 10, 5)
CRACK = [(905, 282), (884, 352), (916, 420), (882, 486), (910, 556), (888, 662)]


def s9():
    """May 1902: one lump on a museum tray; as its wood dries and shrinks, the lump splits: a dark gap opens along a crack, and in it a
    gear wheel's teeth glint; a line of tiny letters glows on the broken face."""
    t0, ts, tg, tl = T("s9", "May"), T("s9", "the lump splits"), T("s9", "a gear wheel"), T("s9", "tiny Greek letters")
    els = [rect(470, 680, 860, 24, "#4a3a2c", "rgba(255,226,190,.3)", 1.5, 6, -1), gl(889, 440, 660, -1, .2, "lamp"),
           poly([(x + 12, y + 18) for x, y in LUMP], "rgba(0,0,0,.55)", at=-1),
           poly(LUMP, VERD_D, "rgba(170,210,190,.45)", 2, -1)]
    for k, (px, py, rx, ry, c, o) in enumerate([(730, 410, 86, 48, CRUST, .55), (1080, 540, 96, 48, VERD, .5), (930, 360, 74, 26, VERD_L, .3),
                                                (790, 580, 62, 32, CRUST, .5), (1110, 380, 50, 30, CRUST_L, .45)]):
        els.append(poly(blob(px, py, rx, ry, 16, .22, 30 + k), c, "none", 0, -1, curve=True, op=o))
    els.append(poly(LUMP, "url(#k-shade)", "none", 0, -1))
    # the wood inside, at the broken left edge: four strips that shrink and darken
    els += [ln([(600, 520 - 18 * k), (680, 514 - 18 * k)], -1, "rgba(170,125,80,.9)", 4, draw=False) for k in range(4)]
    els += chip(889, 170, "May 1902", GOLD, t0 + .1, 28)
    els += [lab(586, 470, "wood", t0 + .8, "#d9b080", 26, "end")]
    els += [ln([(600, 520 - 18 * k), (650, 517 - 18 * k)], ts - 1.0, "rgba(60,40,25,.95)", 4.6, dur=.4) for k in range(4)]
    # the split: a dark gap opens along the crack
    left = [(x - 3, y) for x, y in CRACK]
    gap = [(x - 4 - 14 * math.sin(math.pi * k / (len(CRACK) - 1)), y) for k, (x, y) in enumerate(CRACK)] + \
          [(x + 4 + 16 * math.sin(math.pi * k / (len(CRACK) - 1)), y) for k, (x, y) in enumerate(CRACK)][::-1]
    els += [ln(left, ts - .2, "#0b0f0d", 6, dur=.6), poly(gap, "#07090a", "rgba(200,235,215,.4)", 1.2, ts + .4, fx="fade", dur=.6)]
    # in the gap: the gear's toothed edge, glinting; letters on the broken face
    z = teeth_pts(1060, 470, 168, 110, 8, 150, 212, seed=2)
    els += [ln(z, tg, AU, 2.8, dur=.8), gl(900, 470, 150, tg + .3, .6, "lamp"),
            ln([(905, 430), (1120, 300), (1200, 300)], tg + .6, BONE, 1.4, dur=.4), lab(1216, 308, "a gear wheel", tg + .8, GOLD, 30, "start")]
    els += [{"k": "glyphs", "x": 730, "y": 450, "w": 130, "h": 54, "rows": 3, "cols": 8, "kind": "latin", "c": "#e9f3ea", "in": round(tl, 2), "op": .9},
            ln([(740, 510), (640, 620), (590, 620)], tl + .4, BONE, 1.4, dur=.4), lab(576, 628, "Greek letters", tl + .6, BONE, 28, "end")]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s10():
    """Who noticed first: Spyridon Stais, a former education minister (the old reports), or his cousin Valerios, an archaeologist (many
    later books)."""
    t0, tv = T("s10", "The first to notice"), T("s10", "Many books")
    els = [rect(760, 560, 260, 16, "#4a3a2c", at=-1), gl(889, 470, 360, -1, .18, "lamp"),
           poly([(x * .27 + 657, y * .27 + 382) for x, y in LUMP], VERD_D, "rgba(170,210,190,.45)", 1.5, -1),
           ln([(x * .27 + 657, y * .27 + 382) for x, y in CRACK], -1, "#0b0f0d", 5, draw=False)]
    els += [gl(500, 520, 200, t0 + .3, .25, "lamp")] + fig(500, 640, 260, t0 + .3, "#4a4350", coat=True, hat=True, rim="rgba(240,225,200,.7)")
    els += [lab(500, 700, "Spyridon Stais", t0 + .6, BONE, 30), lab(500, 740, "former minister", t0 + .9, DIM, 24)]
    # the old reports: a stack of papers, solid arrow
    els += [rect(170 + 6 * k, 520 - 14 * k, 120, 80, "#e9dcc0", "#8a7a5c", 1.2, 2, t0 + 1.2 + .1 * k, fx="pop") for k in range(3)]
    els += [{"k": "glyphs", "x": 196, "y": 500, "w": 90, "h": 50, "rows": 5, "cols": 5, "kind": "latin", "c": "#5a4a36", "in": round(t0 + 1.6, 2)},
            lab(240, 640, "old reports", t0 + 1.7, DIM, 24), arr([(310, 470), (380, 430), (430, 420)], t0 + 1.9, GOLD, 3, dur=.5)]
    els += [gl(1280, 520, 200, tv, .25, "lamp")] + fig(1280, 640, 250, tv, "#4a4350", coat=True, face=-1, rim="rgba(240,225,200,.7)")
    els += [lab(1280, 700, "Valerios Stais", tv + .3, BONE, 30), lab(1280, 740, "archaeologist", tv + .5, DIM, 24)]
    els += [rect(1490, 560 - 30 * k, 130, 26, c, "rgba(255,236,206,.4)", 1, 3, tv + .8 + .1 * k, fx="pop") for k, c in enumerate(("#7a3a2a", "#2f4f6a", "#6a5a2a"))]
    els += [lab(1555, 640, "many books", tv + 1.1, DIM, 24), arr([(1480, 480), (1420, 440), (1370, 430)], tv + 1.3, LILAC, 3, "inferred", dur=.5)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s11_add():
    """Not a statue, not treasure (struck through): a machine (the gear glows). Then the guesses, lilac: an astrolabe? a ship's instrument?
    And half a century with no answer."""
    tn, tm, th = T("s11", "Not a statue"), T("s11", "A machine"), T("s11", "For half a century")
    els = fig(250, 380, 150, tn, "#ddd5c4", arms="up") + [ln([(180, 380), (330, 230)], tn + .5, RED, 5, dur=.3)]
    els += [circ(250, 500, 44, AU, "#fff1c8", 2, tn + .7, fx="pop"), circ(250, 500, 30, "none", "#a07a28", 2, tn + .75, fx="pop"),
            ln([(196, 548), (304, 452)], tn + 1.0, RED, 5, dur=.3)]
    els += [gl(895, 470, 260, tm, .6, "lamp", pulse=True)]
    els += [lab(1460, 540, "astrolabe?", th + .3, LILAC, 32, st="ital"), lab(1460, 600, "ship's instrument?", th + .8, LILAC, 32, st="ital")]
    els += [ln([(560, 760), (1220, 760)], th + .2, "rgba(201,193,238,.7)", 2.5, "claimed", dur=1.0)]
    els += qmark(890, 752, th + 1.4, 60, halo=False)
    return els


# ================================================================== CHAPTER 2 · Counting the teeth
def desk_lamp(x, y, at, s=1.0):
    """A desk lamp standing on y: a base, an arm, a shade, and its pool of light."""
    els = [rect(x - 30 * s, y - 8 * s, 60 * s, 8 * s, "#2a2420", "rgba(255,236,206,.3)", 1, 2, at),
           ln([(x, y - 8 * s), (x + 20 * s, y - 120 * s), (x + 70 * s, y - 150 * s)], at, "#2a2420", 5 * s, draw=False),
           poly([(x + 50 * s, y - 170 * s), (x + 100 * s, y - 150 * s), (x + 108 * s, y - 118 * s), (x + 56 * s, y - 132 * s)], "#3a332c", "rgba(255,236,206,.4)", 1, at)]
    return els


def s12():
    """Derek de Solla Price at a desk in Athens, 1958: the fragments on a cloth, a magnifier, a lamp; then the magazine of 1959 with a gear
    on its cover and the words 'An Ancient Greek Computer'."""
    ts, tm, tc = T("s12", "he studied"), T("s12", "Scientific American"), T("s12", "ancient Greek computer")
    tab = 600
    els = [rect(160, tab, 860, 16, "#4a3826", "rgba(255,226,190,.35)", 1.2, 3, -1), rect(190, tab + 16, 14, 150, "#3a2c20", at=-1), rect(976, tab + 16, 14, 150, "#3a2c20", at=-1)]
    els += desk_lamp(860, tab, -1) + [gl(820, tab - 70, 300, -1, .45, "lamp")]
    els += seated(380, tab + 166, 330, ts, "#d9c7a6")
    els += [rect(560, tab - 10, 300, 10, "#8a3a2a", at=ts + .3)]
    for k, (x, rx, ry) in enumerate([(610, 34, 22), (690, 46, 26), (770, 28, 18)]):
        els.append(poly(blob(x, tab - 30, rx, ry, 14, .25, 50 + k), VERD_D, "rgba(170,210,190,.5)", 1.2, ts + .4 + .15 * k, fx="pop"))
    els += [circ(700, tab - 92, 34, "rgba(200,230,255,.15)", "#d8dde2", 3, ts + .9, fx="pop"), ln([(724, tab - 68), (760, tab - 36)], ts + .9, "#5a4a3a", 6, draw=False)]
    els += [lab(380, 455, "Derek de Solla Price", ts + .6, BONE, 30)]
    els += chip(400, 200, "1958", GOLD, ts + .2, 30)
    # the magazine
    mx, my, mw, mh = 1180, 190, 400, 450
    els += [rect(mx + 10, my + 14, mw, mh, "rgba(0,0,0,.5)", at=tm), rect(mx, my, mw, mh, "#e9e2d2", "#8a7a5c", 1.5, 4, tm, fx="pop"),
            rect(mx, my, mw, 64, "#1f3f5a", at=tm + .1, fx="pop"), lab(mx + mw / 2, my + 44, "SCIENTIFIC AMERICAN", tm + .2, "#f2ead8", 22, st="cap")]
    els += gear(mx + mw / 2, my + 250, 110, 32, tm + .4, BRZ, BRZ_L, 1.4, hole="#e9e2d2", spokes=4, fx="pop")
    els += [lab(mx + mw / 2, my + 410, "An Ancient Greek Computer", tc, "#2a2018", 23, st="lab", fx="pop", halo=False)]
    els += [lab(mx + mw / 2, my + mh + 50, "June 1959", tm + .6, DIM, 26)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def jet(x, y, s, at, c=LILAC, style="claimed"):
    """A jet airliner in side view, drawn as a dotted outline (a figure of speech)."""
    P = lambda a, b: (x + a * s, y + b * s)
    body = [P(-.5, 0), P(-.44, -.05), P(.36, -.06), P(.48, -.03), P(.52, 0), P(.48, .03), P(.36, .05), P(-.44, .05)]
    wing = [P(-.06, .02), P(.16, .02), P(-.14, .32), P(-.24, .32)]
    tail = [P(-.42, -.04), P(-.5, -.3), P(-.42, -.3), P(-.3, -.05)]
    stab = [P(-.44, .02), P(-.52, .12), P(-.46, .12), P(-.36, .03)]
    return [poly(body, "rgba(201,193,238,.06)", c, 3, at, style=style), poly(wing, "none", c, 3, at, style=style),
            poly(tail, "none", c, 3, at, style=style), poly(stab, "none", c, 2.5, at, style=style)]


def s13():
    """'Like finding a jet plane in Tutankhamun's tomb': a lamp-lit burial chamber in section, the gilded coffin in its stone
    sarcophagus, and a jet plane drawn in lilac dots across the chamber (a figure of speech, not a find)."""
    tq = T("s13", "like finding")
    els = [rect(160, 200, 1460, 560, "url(#k-blocks)", "rgba(255,236,206,.35)", 2, 6, -1, op=.55),
           rect(160, 200, 1460, 560, "rgba(20,12,6,.45)", at=-1),
           rect(160, 700, 1460, 60, "#5a4630", at=-1),
           gl(500, 520, 520, -1, .35, "lamp"), gl(1300, 520, 420, -1, .2, "lamp")]
    # the sarcophagus and the gilded coffin
    els += [rect(300, 520, 420, 180, "#8d7a64", "rgba(255,236,206,.45)", 1.6, 4, -1),
            poly([(330, 520), (338, 480), (372, 452), (420, 446), (450, 462), (640, 470), (690, 486), (700, 520)], AU, "#fff1c8", 1.4, -1, curve=True),
            circ(392, 476, 24, "#c9962a", "#fff1c8", 1.2, -1), ln([(430, 470), (660, 470)], -1, "#a07a28", 2, draw=False)]
    els += jet(1100, 420, 640, tq)
    els += [lab(1100, 640, "like a jet plane", tq + .8, LILAC, 34, st="ital")]
    els += chip(1440, 250, "Price, 1958", GOLD, tq + .4, 26)
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s14():
    """Gamma rays and X-rays through the fragments, 1971 (Karakalos): a source, a fan of rays, the fragment, a film on which gear rings
    appear; beside it, a dentist's X-ray: a tooth seen through the gum."""
    t0, tm, td = T("s14", "But the gears"), T("s14", "So in"), T("s14", "the way a dentist")
    els = [poly(blob(560, 470, 110, 80, 18, .2, 61), VERD_D, "rgba(170,210,190,.5)", 1.6, -1, curve=True)]
    els += [gl(560, 470, 140, t0, .25, "lamp")]
    els += [rect(140, 400, 120, 140, "#2a2f36", "rgba(200,220,240,.5)", 1.6, 6, -1), gl(258, 470, 90, tm + .2, .8, "glowb"),
            {"k": "fan", "x": 262, "y": 470, "a0": -18, "a1": 18, "r": 560, "c": XR, "n": 11, "in": round(tm + .4, 2)},
            rect(830, 340, 26, 260, "#0d1a26", "rgba(159,208,255,.7)", 1.6, 2, -1)]
    els += [circ(843, 430 + 40 * k, 22 - 4 * k, "none", XR_L, 2, tm + 1.2 + .25 * k, fx="draw", dur=.4) for k in range(3)]
    els += fig(200, 640, 120, tm + .8, "#4a4350", rim="rgba(240,225,200,.6)")
    els += [lab(200, 690, "Karakalos", tm + 1.0, BONE, 26), lab(560, 330, "gamma rays and X-rays", tm + 1.4, XR_L, 28)]
    els += chip(560, 200, "1971", GOLD, tm + .2, 28)
    # the dentist's X-ray
    fx_, fy = 1200, 300
    els += [rect(fx_, fy, 360, 330, "#0b1620", "rgba(159,208,255,.6)", 2, 12, td, fx="pop"),
            poly([(fx_ + 30, fy + 120), (fx_ + 120, fy + 80), (fx_ + 240, fy + 80), (fx_ + 330, fy + 120), (fx_ + 330, fy + 300), (fx_ + 30, fy + 300)],
                 "rgba(255,150,160,.18)", "rgba(255,170,180,.5)", 1.5, td + .3, curve=True),
            poly([(fx_ + 140, fy + 60), (fx_ + 220, fy + 60), (fx_ + 236, fy + 140), (fx_ + 222, fy + 290), (fx_ + 196, fy + 300), (fx_ + 184, fy + 180),
                  (fx_ + 176, fy + 180), (fx_ + 164, fy + 300), (fx_ + 138, fy + 290), (fx_ + 124, fy + 140)], "rgba(230,240,255,.85)", XR_L, 1.6, td + .6, curve=True, fx="fade"),
            lab(fx_ + 180, fy + 380, "a dentist's X-ray", td + 1.0, BONE, 28)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s15():
    """The count: a radiograph on a light box, a big gear ring; its teeth are ticked off one by one until the count reaches 127."""
    t0, tn = T("s15", "Then they counted"), T("s15", "a hundred and twenty")
    cx, cy, r = 760, 470, 250
    els = [rect(420, 160, 680, 620, "#dfe9f2", "rgba(255,255,255,.7)", 2, 10, -1, op=.9), rect(450, 190, 620, 560, "#0e1a26", at=-1),
           gl(760, 470, 520, -1, .2, "glowb")]
    els += [ln(teeth_pts(cx, cy, r, 127, 9, phase=-90) + teeth_pts(cx, cy, r, 127, 9, phase=-90)[:1], -1, XR_L, 1.6, draw=False, op=.85),
            circ(cx, cy, r * .82, "none", "rgba(207,233,255,.45)", 1.4, -1), circ(cx, cy, 30, "none", "rgba(207,233,255,.5)", 1.4, -1)]
    span = max(1.2, tn + .8 - (t0 + .6))
    for k in range(127):
        a = math.radians(-90 + 360 * k / 127)
        els.append(dot(round(cx + (r + 18) * math.cos(a), 1), round(cy + (r + 18) * math.sin(a), 1), 3.2, AU, round(t0 + .6 + span * k / 127, 2)))
    els += [lab(1340, 450, "127", tn + .7, AU, 120, st="big", fx="pop"), lab(1340, 520, "teeth", tn + .9, BONE, 34, st="serif")]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def small_train(x, y, s, at, c=AU):
    """A small train of three meshing gears (an icon), glowing."""
    els = []
    for (dx, dy, r, n) in ((0, 0, 40, 24), (66, -10, 28, 16), (112, 22, 22, 12)):
        els += gear(x + dx * s, y + dy * s, r * s, n, at, c, "#fff1c8", 1.2, hub=.2)
    return [grp(els, at, "pop")]


def s16():
    """Double it: 127 x 2 = 254, the Moon's laps of the sky in 19 years: nineteen columns fill with Moon dots, 13 or 14 a year, 254 in all;
    on 'astronomer's cycle', a small gear train glows."""
    t0, tm, tn, tc = T("s16", "Double it"), T("s16", "the Moon goes"), T("s16", "nineteen years"), T("s16", "astronomer's cycle")
    els = [lab(640, 220, "127 x 2 = 254", t0 + .3, AU, 54, st="serif", fx="pop")]
    x0, dx, yb = 200, 46, 640
    els += [axis(x0, x0 + 19 * dx, yb + 20, [[x0 + dx * (k + .5), str(k + 1)] for k in (0, 4, 9, 14, 18)], .2)]
    span = max(1.5, tn + .6 - tm)
    for k in range(19):
        n_k = math.floor((k + 1) * 254 / 19) - math.floor(k * 254 / 19)
        for j in range(n_k):
            els.append(dot(x0 + dx * (k + .5), yb - 12 - 22 * j, 7, "#efe8da", round(tm + span * (k + j / n_k) / 19, 2)))
    els += [lab(x0 + 19 * dx / 2, yb + 100, "19 years", tn, BONE, 30),
            lab(x0 + 19 * dx + 40, 360, "254 laps", tn + .4, "#efe8da", 34, "start", st="serif"),
            lab(x0 + 19 * dx + 40, 404, "of the Moon", tn + .6, DIM, 28, "start")]
    els += small_train(1160, 600, 1.2, tc)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s17_add():
    """1974: the book, 'Gears from the Greeks'."""
    t0 = T("s17", "he published")
    bx, by, bw, bh = 1380, 240, 250, 340
    els = [rect(bx + 10, by + 14, bw, bh, "rgba(0,0,0,.5)", at=t0), rect(bx, by, bw, bh, "#2f4a3a", "#cfe0c8", 1.6, 4, t0, fx="pop")]
    els += gear(bx + bw / 2, by + 150, 70, 24, t0 + .2, BRZ, BRZ_L, 1.2, hole="#2f4a3a", spokes=4, fx="pop")
    els += [lab(bx + bw / 2, by + 270, "Gears from", t0 + .3, "#f2ead8", 28, st="serif", fx="pop"), lab(bx + bw / 2, by + 306, "the Greeks", t0 + .35, "#f2ead8", 28, st="serif", fx="pop")]
    els += chip(bx + bw / 2, by + bh + 50, "1974", GOLD, t0 + .5, 28)
    return els


def s18():
    """Price misread how some gears connected (his plan, one link struck in red); the fix: Michael Wright of the Science Museum and the
    computer scientist Allan Bromley."""
    t0, tw = T("s18", "But Price"), T("s18", "The fix came")
    G = [(300, 360, 90, 48), (440, 300, 50, 24), (420, 520, 110, 64), (600, 440, 60, 32)]
    els = [rect(140, 180, 640, 520, "rgba(233,220,192,.06)", "rgba(233,220,192,.35)", 1.5, 10, -1)]
    for k, (x, y, r, n) in enumerate(G):
        els += gear(x, y, r, n, -1, "#5a6a5a", "#c9d8c8", 1.2, hub=.2)
    els += [ln([(300, 360), (440, 300)], -1, BONE, 2.5, draw=False), ln([(440, 300), (600, 440)], -1, BONE, 2.5, draw=False),
            ln([(420, 520), (600, 440)], t0 + .4, RED, 4, "inferred", dur=.5)] + cross(510, 480, t0 + 1.0) + \
           [lab(560, 680, "misread", t0 + 1.3, RED, 30, "start"), lab(460, 230, "Price's plan", t0 + .2, DIM, 26)]
    # the Science Museum's front and the two men
    els += [grp(portico(990, 1450, 700, 340, 0, ncol=5, c="#6a6258", edge="rgba(240,230,215,.45)"), tw, "fade")]
    els += fig(1090, 700, 230, tw + .3, "#4a4350", rim="rgba(240,225,200,.7)") + fig(1370, 700, 220, tw + .6, "#4a4350", face=-1, rim="rgba(240,225,200,.7)")
    els += [lab(1090, 750, "Michael Wright", tw + .5, BONE, 28), lab(1370, 750, "Allan Bromley", tw + 2.2, BONE, 28),
            lab(1220, 230, "Science Museum", tw + 1.4, GOLD, 28)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s19():
    """Linear tomography, 1990s: the X-ray tube slides one way and the film the other, so one layer of the fragment stays sharp while the
    layers above and below blur."""
    t0 = T("s19", "they took")
    o = 150
    els = chip(1520, 200, "1990s", GOLD, t0, 28)
    els += [rect(700 + o, 160, 180, 70, "#2a2f36", "rgba(200,220,240,.5)", 1.6, 6, -1), gl(790 + o, 230, 70, t0 + .3, .7, "glowb"),
            arr([(860 + o, 140), (640 + o, 140)], t0 + .8, BONE, 3, dur=.5, curve=False), lab(600 + o, 196, "tube", t0 + 1.0, BONE, 26, "end"),
            rect(600 + o, 690, 380, 26, "#0d1a26", "rgba(159,208,255,.7)", 1.6, 2, -1),
            arr([(720 + o, 748), (940 + o, 748)], t0 + .8, BONE, 3, dur=.5, curve=False), lab(1000 + o, 712, "film", t0 + 1.0, BONE, 26, "start")]
    # rays converging through one plane
    for k in range(5):
        x = 640 + 70 * k + o
        els.append(ln([(790 + o, 232), (x, 690)], t0 + 1.2, "rgba(159,208,255,.35)", 1.4, draw=False))
    for k, (y, sharp) in enumerate([(380, False), (450, True), (520, False)]):
        if sharp:
            els += [rect(560 + o, y - 18, 460, 36, "rgba(80,140,120,.6)", XR_L, 2, t0 + 1.6), lab(1050 + o, y + 8, "one sharp layer", t0 + 2.0, XR_L, 28, "start")]
            els += [circ(650 + 90 * j + o, y, 12, "none", XR_L, 2, t0 + 1.8 + .1 * j) for j in range(4)]
        else:
            for d in (-6, 0, 6):
                els.append(rect(560 + d + o, y - 18 + d * .5, 460, 36, "rgba(80,140,120,.18)", "rgba(159,208,255,.25)", 1, at=t0 + 1.6, op=.6))
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def spiral_pts(cx, cy, r0, r1, turns, a0=-90, n=None):
    """An Archimedean spiral from radius r0 to r1 over `turns` turns, starting at angle a0 (degrees)."""
    n = n or int(turns * 72)
    return [(cx + (r0 + (r1 - r0) * k / n) * math.cos(math.radians(a0 + 360 * turns * k / n)),
             cy + (r0 + (r1 - r0) * k / n) * math.sin(math.radians(a0 + 360 * turns * k / n))) for k in range(n + 1)]


def replica(x, y, s, at, fx="pop"):
    """A bronze replica of the machine, front view: a case, a round dial with zodiac ticks, pointers, a knob on the side."""
    els = [rect(x - 120 * s, y - 160 * s, 240 * s, 320 * s, BRZ_D, BRZ_L, 2, 8 * s, at),
           circ(x, y, 100 * s, "#8a5a30", BRZ_L, 2, at), circ(x, y, 80 * s, "none", BRZ_L, 1.2, at)]
    els += [ln([(x + 80 * s * math.cos(math.radians(a)), y + 80 * s * math.sin(math.radians(a))), (x + 100 * s * math.cos(math.radians(a)), y + 100 * s * math.sin(math.radians(a)))],
               at, BRZ_L, 1.2, draw=False) for a in range(0, 360, 30)]
    els += [ln([(x, y), (x + 70 * s, y - 40 * s)], at, AU, 3, draw=False), ln([(x, y), (x - 30 * s, y + 66 * s)], at, "#efe8da", 3, draw=False),
            circ(x + 70 * s, y - 40 * s, 7 * s, AU, at=at), circ(x, y, 8 * s, BRZ_L, at=at),
            rect(x + 120 * s, y - 14 * s, 26 * s, 28 * s, BRZ_D, BRZ_L, 1.5, 4, at), circ(x + 150 * s, y, 12 * s, BRZ, BRZ_L, 1.5, at)]
    return [grp(els, at, fx)]


def s20():
    """Wright's three findings, built as named: a back dial whose scale is a five-turn spiral; a little ball, half pale, half dark,
    turning through the Moon's phases; and a working bronze replica."""
    ts, tm, tr = T("s20", "spirals"), T("s20", "a little ball"), T("s20", "working replicas")
    els = [rect(170, 230, 380, 440, "rgba(110,74,42,.35)", BRZ_L, 2, 10, -1), circ(865, 520, 84, "none", "rgba(255,240,215,.25)", 1.5, -1),
           rect(1400 - 126, 450 - 168, 252, 336, "none", "rgba(226,178,122,.25)", 1.5, 8, -1)]
    els.append(ln(spiral_pts(360, 450, 40, 170, 5, n=360), ts - .1, AU, 3, dur=1.6))
    els += [lab(360, 720, "spiral dials", ts + .6, GOLD, 30)]
    for k, ph in enumerate((0, .25, .5, .75)):
        els += moonball(700 + 110 * k, 330 + (40 if k % 2 else 0), 40, tm + .3 * k, phase=ph if ph <= .5 else 1 - ph, rot_=0 if ph <= .5 else 180)
    els += [moonball(865, 520, 84, tm + 1.3, phase=.5)[0], lab(865, 680, "Moon phase", tm + 1.6, BONE, 30)]
    els += replica(1400, 450, 1.05, tr) + [lab(1400, 720, "working replicas", tr + .4, GOLD, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def mini_frag(x, y, s, at, c=VERD_D):
    """The fragment's outline, small (for the three ways of seeing)."""
    return poly([(x + (px - FA[0]) * s, y + (py - FA[1]) * s) for px, py in SLAB], c, "rgba(170,210,190,.45)", 1.4, at)


def s21():
    """Each new way of seeing found more: three views of the fragment, by eye (1902), on film (1971), in layers (1990s), each showing more
    gear rings; then an eight-tonne crate slides in."""
    t0, t8 = T("s21", "Each new way"), T("s21", "eight tonnes")
    els = []
    for k, (x, tag, n) in enumerate([(300, "1902, by eye", 1), (720, "1971, on film", 5), (1140, "1990s, in layers", 10)]):
        at = t0 + .3 + .9 * k
        els += [rect(x - 190, 260, 380, 360, "rgba(255,236,206,.04)", "rgba(255,236,206,.3)", 1.5, 10, at, fx="pop"), mini_frag(x, 440, .42, at)]
        rnd = random.Random(k + 4)
        for j in range(n):
            gx, gy = x + rnd.uniform(-90, 90), 440 + rnd.uniform(-70, 70)
            els += gear_ring(gx, gy, rnd.uniform(16, 40), 16, at + .3 + .08 * j, AU if k == 0 else XR_L, 1.6, dur=.4, hub=False)
        els += [lab(x, 670, tag, at + .2, BONE, 26)]
    els += [rect(1390, 380, 270, 240, "#5a4430", "#c9a070", 2, 6, t8, fx="rise"),
            ln([(1390, 450), (1660, 450)], t8 + .1, "#3a2a1a", 3, draw=False), ln([(1390, 550), (1660, 550)], t8 + .1, "#3a2a1a", 3, draw=False),
            lab(1525, 520, "8 tonnes", t8 + .3, GOLD, 34, st="serif", fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · Eight tonnes of X-rays
def portico(x0, x1, base, top, at, ncol=6, c="#cfc3ad", edge="rgba(255,240,220,.6)", fx=None):
    """A neoclassical front: steps, a row of columns, an entablature and a low pediment."""
    w = x1 - x0
    els = [rect(x0 - 20, base - 16, w + 40, 16, c, edge, 1, 0, at), rect(x0 - 10, base - 30, w + 20, 14, c, edge, 1, 0, at)]
    for k in range(ncol):
        cx = x0 + 30 + (w - 60) * k / (ncol - 1)
        els += [rect(cx - 13, top + 30, 26, base - 30 - (top + 30), c, edge, 1, 0, at), rect(cx - 18, top + 22, 36, 10, c, edge, 1, 0, at)]
    els += [rect(x0 - 10, top - 10, w + 20, 34, c, edge, 1, 0, at),
            poly([(x0 - 20, top - 10), (x0 + w / 2, top - 70), (x1 + 20, top - 10)], c, edge, 1, at)]
    return [grp(els, at, fx)] if fx else els


def scanner(x, y, s, at):
    """A CT scanner in side view: an X-ray source, a turntable carrying a fragment, a flat detector; the cone of rays between."""
    els = [rect(x - 260 * s, y - 50 * s, 110 * s, 100 * s, "#2a2f36", "rgba(200,220,240,.5)", 1.6, 6, at),
           gl(x - 150 * s, y, 60 * s, at, .8, "glowb"),
           poly([(x - 150 * s, y), (x + 230 * s, y - 150 * s), (x + 230 * s, y + 150 * s)], "rgba(127,196,255,.12)", "rgba(127,196,255,.4)", 1, at),
           rect(x + 230 * s, y - 160 * s, 24 * s, 320 * s, "#0d1a26", "rgba(159,208,255,.8)", 1.6, 2, at),
           rect(x - 40 * s, y + 70 * s, 120 * s, 16 * s, "#4a5058", "rgba(220,230,240,.5)", 1, 3, at),
           ln([(x + 20 * s, y + 70 * s), (x + 20 * s, y + 160 * s)], at, "#4a5058", 6 * s, draw=False),
           poly(blob(x + 20 * s, y + 20 * s, 54 * s, 44 * s, 14, .2, 77), VERD_D, "rgba(170,210,190,.6)", 1.4, at, curve=True)]
    return els


def s22():
    """Athens, 2005: the museum's columned front; an eight-tonne crate rolls up to its steps; inside, the CT scanner: source, turntable
    with a fragment, detector, a cone of rays."""
    t0, t8, tx = T("s22", "The fragments"), T("s22", "eight-tonne"), T("s22", "X-ray scanner")
    els = portico(170, 690, 640, 330, -1)
    els += [lab(430, 240, "National Archaeological Museum", .4, DIM, 24)]
    els += chip(430, 170, "2005", GOLD, .3, 28)
    els += [rect(720, 520, 230, 104, "#5a4430", "#c9a070", 2, 6, t8, fx="rise"), ln([(720, 556), (950, 556)], t8, "#3a2a1a", 3, draw=False),
            rect(700, 624, 280, 14, "#2a2420", at=t8), circ(740, 646, 16, "#1a1612", "#8a7a6a", 2, t8), circ(940, 646, 16, "#1a1612", "#8a7a6a", 2, t8),
            lab(835, 590, "8 tonnes", t8 + .3, GOLD, 30, st="serif", fx="pop")]
    els += [rect(1060, 200, 600, 520, "rgba(159,208,255,.04)", "rgba(159,208,255,.35)", 1.5, 14, tx - .2, fx="pop")]
    els += [grp(scanner(1360, 450, 1.0, tx), tx, "pop"), lab(1360, 690, "X-ray CT", tx + .5, XR_L, 28)]
    return {"base": "sky", "tod": "dusk", "ground": 640, "sun": [140, 560, 18], "cam": CAM, "els": els}


def s23():
    """CT, like slicing a loaf without a knife: a loaf whose slices fan apart; beside it the fragment as a stack of thin translucent slices,
    each showing gear rings in cross-section."""
    t0 = T("s23", "It sliced")
    tl = T("s23", "like slicing")
    # the fragment as slices (left), the loaf (right)
    for k in range(7):
        x = 300 + 70 * k
        y = 470 - 14 * k
        els_k = [poly(blob(x, y, 70, 120, 16, .12, 90 + k), "rgba(80,140,120,.35)", "rgba(159,208,255,.7)", 1.5, t0 + .3 + .18 * k, fx="pop")]
        rnd = random.Random(k)
        for j in range(2):
            els_k += [circ(x + rnd.uniform(-30, 30), y + rnd.uniform(-60, 60), rnd.uniform(14, 26), "none", XR_L, 1.6, t0 + .5 + .18 * k)]
        if k == 0:
            els = els_k
        else:
            els += els_k
    els += [lab(510, 680, "CT slices", t0 + 1.8, XR_L, 30)]
    lx, ly = 1260, 470
    loaf = [(lx - 230, ly + 90), (lx - 236, ly + 10), (lx - 200, ly - 60), (lx - 100, ly - 100), (lx + 100, ly - 100), (lx + 200, ly - 60), (lx + 236, ly + 10), (lx + 230, ly + 90)]
    els += [poly(loaf, "#b9824a", "#f0c890", 2, tl, curve=True, fx="pop")]
    for k in range(7):
        x = lx - 180 + 60 * k
        els.append(ln([(x, ly - 96 + abs(k - 3) * 8), (x - 8, ly + 90)], tl + .4 + .12 * k, "#5a3a1a", 3, dur=.3))
    els += [lab(lx, ly + 190, "like slicing a loaf", tl + 1.0, BONE, 30)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s24():
    """Reflectance imaging: a metre-wide dome of fifty flashbulbs over a fragment, a camera at its top; and a worn coin under a lamp, its
    letters brought up by raking light."""
    t0, tc = T("s24", "And a metre-wide"), T("s24", "the way you tilt")
    cx, cy, R_ = 520, 640, 330
    els = [poly(E(cx, cy, R_, R_ * .9, 48, 180, 360), "rgba(233,220,192,.05)", "rgba(233,220,192,.6)", 2, t0 + .2, fx="pop"),
           ln([(cx - R_ - 20, cy), (cx + R_ + 20, cy)], t0 + .2, "rgba(233,220,192,.6)", 2, draw=False),
           poly(blob(cx, cy - 26, 70, 26, 14, .2, 88), VERD_D, "rgba(170,210,190,.6)", 1.4, t0 + .3),
           rect(cx - 22, cy - R_ * .9 - 30, 44, 34, "#2a2622", "rgba(255,236,206,.5)", 1.4, 4, t0 + .4)]
    rnd = random.Random(3)
    k = 0
    for ring_, n in ((.95, 18), (.78, 14), (.6, 10), (.42, 8)):
        for j in range(n):
            a = math.radians(180 + 180 * (j + .5) / n)
            x = cx + R_ * ring_ * math.cos(a) * (1 if ring_ > .5 else 1)
            y = cy + R_ * .9 * math.sin(a) * (1 - (1 - ring_) * .2)
            els.append(dot(round(x, 1), round(y, 1), 5, "#ffe9b0", round(t0 + .8 + .03 * k, 2)))
            k += 1
    els += [gl(cx - 200, cy - 200, 120, t0 + 2.6, .8, "lamp"), gl(cx + 180, cy - 240, 120, t0 + 3.0, .8, "lamp"),
            lab(cx, 210, "50 flashes", t0 + 1.8, GOLD, 30)]
    # the coin under a lamp
    ox, oy = 1300, 560
    els += [circ(ox, oy, 120, "#a88a5a", "#e8cf98", 2, tc, fx="pop"), circ(ox, oy, 100, "none", "rgba(80,60,30,.5)", 2, tc)]
    els += desk_lamp(1520, 700, tc + .3, 1.1)
    els += [gl(1430, 520, 260, tc + .8, .4, "lamp"),
            {"k": "glyphs", "x": ox - 70, "y": oy - 26, "w": 140, "h": 52, "rows": 2, "cols": 6, "kind": "latin", "c": "#4a3418", "in": round(tc + 1.2, 2), "op": .9},
            lab(ox, 760, "a worn coin", tc + .6, BONE, 28)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


ZOD = (889, 470)


def s25():
    """How it works: turn a knob on the side; the four-spoked wheel goes round once a year; the turning flows through a chain of gears to
    the front dial (zodiac and calendar rings) and its pointers: the Sun with a golden sphere, the Moon with a half-dark ball, the date."""
    tt, ty, tf, ts, tm, td = (T("s25", "Turn it by hand"), T("s25", "once a year"), T("s25", "Its turning"), T("s25", "the Sun's place"),
                              T("s25", "the Moon's"), T("s25", "and the date"))
    cx, cy = ZOD
    els = [rect(cx - 330, cy - 300, 660, 600, "rgba(110,74,42,.25)", BRZ_L, 1.6, 12, -1, op=.7)]
    els += gear(cx, cy, 250, 120, -1, "#7a5a3a", "#d8a870", 1.2, hole="#2a1e14", spokes=4, ring=.12, spoke_rot=-12, op=.9)
    els += [rect(cx + 330, cy - 22, 50, 44, BRZ_D, BRZ_L, 1.5, 6, tt), circ(cx + 400, cy, 22, BRZ, BRZ_L, 2, tt, fx="pop"),
            lab(cx + 400, cy - 50, "by hand", tt + .3, GOLD, 28)]
    els += [arr(E(cx, cy, 290, 290, 40, -150, -30), ty, AU, 4, dur=1.0), lab(cx, cy - 330, "once a year", ty + .4, AU, 30)]
    # the chain of gears lights up behind, then the front dial
    for k, (dx, dy, r, n) in enumerate([(-150, 120, 46, 24), (-60, 170, 34, 18), (40, 150, 40, 20), (130, 110, 30, 15)]):
        els += gear_ring(cx + dx, cy + dy, r, n, tf + .2 + .2 * k, AU, 2, dur=.4)
    els += [circ(cx, cy, 230, "rgba(30,22,14,.88)", "#e8cf98", 2.5, tf + 1.2, fx="fade"),
            circ(cx, cy, 190, "none", "#e8cf98", 1.6, tf + 1.3)]
    els += [ln([(cx + 190 * math.cos(math.radians(a)), cy + 190 * math.sin(math.radians(a))), (cx + 230 * math.cos(math.radians(a)), cy + 230 * math.sin(math.radians(a)))],
               tf + 1.4, "#e8cf98", 1.4, draw=False) for a in range(0, 360, 30)]
    els += [ln([(cx, cy), (cx + 170 * math.cos(math.radians(-60)), cy + 170 * math.sin(math.radians(-60)))], ts, AU, 4, dur=.4),
            circ(cx + 150 * math.cos(math.radians(-60)), cy + 150 * math.sin(math.radians(-60)), 14, AU, "#fff1c8", 1.5, ts + .3, fx="pop"),
            lab(cx + 230, cy - 230, "Sun", ts + .4, AU, 30, "start")]
    mx, my = cx + 120 * math.cos(math.radians(200)), cy + 120 * math.sin(math.radians(200))
    els += [ln([(cx, cy), (cx + 160 * math.cos(math.radians(200)), cy + 160 * math.sin(math.radians(200)))], tm, "#efe8da", 4, dur=.4)]
    els += moonball(mx, my, 20, tm + .3, phase=.5) + [lab(cx - 300, cy - 20, "Moon", tm + .4, "#efe8da", 30, "end")]
    els += [ln([(cx, cy), (cx + 200 * math.cos(math.radians(110)), cy + 200 * math.sin(math.radians(110)))], td, BONE, 3, dur=.4),
            lab(cx + 40, cy + 270, "date", td + .3, BONE, 28, "start"), circ(cx, cy, 10, BRZ_L, at=tf + 1.4)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def kepler(e, M):
    E_ = M
    for _ in range(30):
        E_ = E_ - (E_ - e * math.sin(E_) - M) / (1 - e * math.cos(E_))
    return E_


def s26():
    """The Moon's uneven pace (orbit exaggerated): the Earth off centre in an ellipse; Moon dots at equal time steps, far apart on the near
    side, bunched on the far side; long and short arrows."""
    t0, tn, tf = T("s26", "But the Moon"), T("s26", "nearer to us"), T("s26", "slows down")
    cx, cy, a, b = 889, 470, 460, 260
    c = math.sqrt(a * a - b * b)
    e = c / a
    ex = cx - c
    els = [poly(E(cx, cy, a, b, 72), "none", "rgba(233,220,192,.45)", 2, t0 + .2, fx="draw", dur=1.0) | {"style": "inferred"},
           circ(ex, cy, 30, "#3f7fa8", "#bfe6f5", 2, t0 + .1, fx="pop"), gl(ex, cy, 60, t0 + .2, .4, "glowb"), lab(ex, cy + 70, "Earth", t0 + .3, "#bfe6f5", 26)]
    n = 14
    for k in range(n):
        M = 2 * math.pi * k / n
        E_ = kepler(e, M)
        x = cx - (a * math.cos(E_))          # perigee on the left, near the Earth
        y = cy + b * math.sin(E_)
        near = math.cos(E_) > 0
        els.append(circ(x, y, 13, "#efe8da", "rgba(255,255,255,.6)", 1, tn - .6 + .12 * k if near else tf - .4 + .12 * (k - n // 2), fx="pop"))
    els += [arr([(cx - a - 40, cy - 150), (cx - a - 70, cy), (cx - a - 40, cy + 150)], tn + .2, AU, 4, dur=.5),
            lab(cx - a + 100, cy - 300, "nearer: faster", tn + .4, AU, 30),
            arr([(cx + a + 50, cy - 40), (cx + a + 58, cy), (cx + a + 50, cy + 40)], tf + .2, "#9fd0ff", 4, dur=.5),
            lab(cx + a - 120, cy - 300, "farther: slower", tf + .4, "#9fd0ff", 30)]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


def s27():
    """The pin and slot: two gears of fifty teeth, their centres a hair apart (drawn large: about 1 mm); a pin on the back gear rides in a
    slot of the front one; as the pin goes round evenly, the slot's angle bunches and spreads: fast, then slow."""
    t0, tp, tf = T("s27", "The machine copies"), T("s27", "A pin on one"), T("s27", "runs fast")
    c1, c2, R1 = (850, 470), (910, 470), 230
    els = gear(c1[0], c1[1], R1, 50, t0 + .2, "#6e5a3e", "#d8b880", 1.2, fx="pop")
    els += [grp([poly(teeth_pts(c2[0], c2[1], R1 - 6, 50, None, phase=3.6), "rgba(200,150,90,.32)", "#f0c890", 1.6, 0),
                 circ(c2[0], c2[1], 16, "#3a2a1a", "#f0c890", 1.5, 0)], t0 + .7, "pop")]
    els += [ln([(c1[0], c1[1] + 80), (c1[0], c1[1] + 290)], t0 + 1.2, BONE, 1.2, "inferred", draw=False),
            ln([(c2[0], c2[1] + 80), (c2[0], c2[1] + 290)], t0 + 1.2, BONE, 1.2, "inferred", draw=False),
            {"k": "dim", "x1": c1[0], "y1": c1[1] + 270, "x2": c2[0], "y2": c2[1] + 270, "t": "", "c": GOLD, "in": round(t0 + 1.4, 2)},
            lab(c2[0] + 50, c1[1] + 278, "about 1 mm, enlarged", t0 + 1.6, GOLD, 26, "start")]
    # the pin on the back gear, the slot of the front gear
    pr = 150
    pa = math.radians(-60)
    px, py = c1[0] + pr * math.cos(pa), c1[1] + pr * math.sin(pa)
    sa = math.atan2(py - c2[1], px - c2[0])
    els += [ln([(c2[0] + 40 * math.cos(sa), c2[1] + 40 * math.sin(sa)), (c2[0] + 215 * math.cos(sa), c2[1] + 215 * math.sin(sa))], tp, "#1a120a", 14, dur=.4),
            ln([(c2[0] + 40 * math.cos(sa), c2[1] + 40 * math.sin(sa)), (c2[0] + 215 * math.cos(sa), c2[1] + 215 * math.sin(sa))], tp, "#f0c890", 1.2, draw=False, op=.7),
            circ(px, py, 9, AU, "#fff1c8", 2, tp + .4, fx="pop"), lab(px - 26, py + 10, "pin", tp + .6, AU, 28, "end"),
            lab(c2[0] + 250 * math.cos(sa) + 16, c2[1] + 250 * math.sin(sa) - 4, "slot", tp + .8, "#f0c890", 28, "start")]
    # ghost positions round the turn: even steps of the pin, uneven steps of the slot
    for k in range(12):
        a = math.radians(-60 + 30 * (k + 1))
        gx, gy = c1[0] + pr * math.cos(a), c1[1] + pr * math.sin(a)
        s_ = math.atan2(gy - c2[1], gx - c2[0])
        els += [circ(gx, gy, 6, "rgba(232,195,90,.6)", at=tf - .6 + .1 * k, fx="pop"),
                ln([(c2[0], c2[1]), (c2[0] + 222 * math.cos(s_), c2[1] + 222 * math.sin(s_))], tf - .6 + .1 * k, "rgba(240,200,144,.45)", 1.4, draw=False)]
    # where the pin passes close to the slot's centre the second gear races; on the far side it lags
    els += [arr(E(c2[0], c2[1], 300, 300, 16, -40, 40), tf + .4, AU, 5, dur=.5), lab(c2[0] + 330, c2[1] + 12, "fast", tf + .6, AU, 34, "start", st="serif"),
            arr(E(c2[0], c2[1], 330, 330, 8, 172, 188), tf + 1.2, "#9fd0ff", 5, dur=.4), lab(c2[0] - 360, c2[1] + 12, "slow", tf + 1.4, "#9fd0ff", 34, "end", st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def epicycle(cx, cy, R1, r2, at, c=LILAC, a=-40):
    """Hipparchus' idea, schematic: a circle carried on a circle, the Moon on the small one."""
    ex, ey = cx + R1 * math.cos(math.radians(a)), cy + R1 * math.sin(math.radians(a))
    return [circ(cx, cy, R1, "none", c, 2.5, at, style="inferred"), circ(cx, cy, 14, "#3f7fa8", "#bfe6f5", 1.5, at),
            ln([(cx, cy), (ex, ey)], at, c, 1.6, "inferred", draw=False),
            circ(ex, ey, r2, "none", c, 2.5, at + .3, style="inferred"), circ(ex + r2 * .7, ey - r2 * .7, 11, "#efe8da", at=at + .5, fx="pop")]


def s28():
    """The pair rides on the big wheel of 223 teeth, which turns once in about nine years; beside it, Hipparchus' circles on circles."""
    t0, th, tb = T("s28", "And that pair"), T("s28", "Hipparchus"), T("s28", "cut in bronze")
    cx, cy, R_ = 640, 470, 270
    els = gear(cx, cy, R_, 223, -1, "#6e5a3e", "#d8b880", 1.2, hole="#1a120a", spokes=6, ring=.1, h=5)
    kx, ky = cx + 120, cy - 70
    els += gear(kx, ky, 64, 50, t0, "#8a6a42", "#f0c890", 1.2, fx="pop") + gear(kx + 10, ky, 58, 50, t0 + .2, "rgba(200,150,90,.5)", "#f0c890", 1.2, fx="pop")
    els += [lab(kx + 90, ky - 70, "pin and slot", t0 + .4, GOLD, 26, "start"),
            arr(E(cx, cy, R_ + 40, R_ + 40, 40, 200, 320), t0 + 1.0, AU, 4, dur=1.4),
            lab(cx, cy + R_ + 80, "about 9 years", t0 + 1.6, AU, 30)]
    els += epicycle(1350, 450, 170, 60, th)
    els += [lab(1350, 700, "circles on circles", th + .6, LILAC, 30, st="ital"), lab(1350, 230, "Hipparchus", th + .3, DIM, 26)]
    els += [gl(cx, cy, 340, tb, .35, "lamp"), gl(1350, 450, 240, tb + .2, .3, "lamp")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


UP, LO = (889, 300), (889, 625)        # the two spirals of the back plate


def spiral_cells(c, r0, r1, turns, n, at, dur, col, w=1.4):
    """n cell divisions across a spiral band (radial ticks), popping in along the spiral over `dur` seconds."""
    els = []
    for k in range(n):
        f = (k + .5) / n
        a = math.radians(-90 + 360 * turns * f)
        r = r0 + (r1 - r0) * f
        els.append(ln([(c[0] + (r - 7) * math.cos(a), c[1] + (r - 7) * math.sin(a)), (c[0] + (r + 7) * math.cos(a), c[1] + (r + 7) * math.sin(a))],
                      round(at + dur * f, 2), col, w, draw=False))
    return els


def s29():
    """The back plate: an upper spiral of five turns, 235 cells (19 years of months), and a lower spiral of four turns, 223 cells (the
    eclipse cycle)."""
    t0, tu, tl = T("s29", "On the back"), T("s29", "The upper counts"), T("s29", "The lower counts")
    els = [rect(620, 125, 538, 690, "rgba(110,74,42,.4)", BRZ_L, 2, 10, -1)]
    els += [ln(spiral_pts(UP[0], UP[1], 50, 160, 5, n=400), t0 + .2, AU, 2.2, dur=1.2),
            ln(spiral_pts(LO[0], LO[1], 50, 150, 4, n=320), t0 + .6, AU, 2.2, dur=1.2)]
    els += spiral_cells(UP, 50, 160, 5, 235, tu + .2, 2.4, "#f0d8a0")
    els += spiral_cells(LO, 50, 150, 4, 223, tl + .2, 2.4, "#f0d8a0")
    els += [lab(580, 290, "235 months", tu + .6, GOLD, 30, "end"), lab(580, 330, "= 19 years", tu + 1.0, BONE, 28, "end")]
    els += moonball(520, 220, 26, tu + .8, phase=.3)
    els += [lab(580, 610, "223 months:", tl + .6, GOLD, 30, "end"), lab(580, 650, "eclipses", tl + 1.0, BONE, 28, "end"),
            circ(520, 545, 26, "#14110f", "rgba(255,200,150,.9)", 2, tl + .8, fx="pop"), gl(520, 545, 60, tl + .9, .45, "sun")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def sigma(x, y, s, at, c):
    return ln([(x + .5 * s, y - .5 * s), (x - .4 * s, y - .5 * s), (x + .1 * s, y), (x - .4 * s, y + .5 * s), (x + .5 * s, y + .5 * s)], at, c, max(2, .12 * s), dur=.4)


def eta(x, y, s, at, c):
    return [ln([(x - .35 * s, y - .5 * s), (x - .35 * s, y + .5 * s)], at, c, max(2, .12 * s), dur=.2), ln([(x + .35 * s, y - .5 * s), (x + .35 * s, y + .5 * s)], at + .1, c, max(2, .12 * s), dur=.2),
            ln([(x - .35 * s, y), (x + .35 * s, y)], at + .2, c, max(2, .12 * s), dur=.2)]


def s30_add():
    """Close on the lower spiral: in two cells of its outer turn, eclipse signs pop: a Sigma by a reddened Moon (Selene), an Eta by a
    darkened Sun (Helios), and small hour marks."""
    ts, th, tr = T("s30", "an S for Selene"), T("s30", "an H for Helios"), T("s30", "the hour")
    cell = lambda f: (LO[0] + (50 + 100 * f) * math.cos(math.radians(-90 + 1440 * f)), LO[1] + (50 + 100 * f) * math.sin(math.radians(-90 + 1440 * f)))
    p1, p2 = cell(.7917), cell(.826)
    els = [rect(p1[0] - 18, p1[1] - 18, 36, 36, "rgba(20,14,10,.9)", AU, 1.4, 5, ts - .2, fx="pop"), sigma(p1[0], p1[1], 22, ts, "#ffd9a0"),
           circ(1100, 520, 20, "#8a2a1a", "#ffb08a", 1.5, ts + .3, fx="pop"), gl(1100, 520, 46, ts + .4, .5, "red"),
           ln([(p1[0] + 20, p1[1] - 6), (1078, 520)], ts + .3, BONE, 1.2, dur=.3), lab(1130, 528, "Selene, the Moon", ts + .5, BONE, 26, "start")]
    els += [rect(p2[0] - 18, p2[1] - 18, 36, 36, "rgba(20,14,10,.9)", AU, 1.4, 5, th - .2, fx="pop")] + eta(p2[0], p2[1], 22, th, "#ffd9a0") + \
           [circ(1100, 700, 20, "#14110f", "#ffcf8a", 2, th + .3, fx="pop"), gl(1100, 700, 46, th + .4, .5, "sun"),
            ln([(p2[0] + 20, p2[1] + 4), (1078, 700)], th + .3, BONE, 1.2, dur=.3), lab(1130, 708, "Helios, the Sun", th + .5, BONE, 26, "start")]
    els += [ln([(p1[0] + 24, p1[1] + 26 + 7 * k), (p1[0] + 40, p1[1] + 26 + 7 * k)], tr + .1 * k, AU, 2, dur=.15) for k in range(3)]
    els += [lab(1130, 618, "the hour", tr + .3, AU, 26, "start"), ln([(p1[0] + 44, p1[1] + 36), (1120, 610)], tr + .3, BONE, 1.2, dur=.3)]
    return els


def runner(x, y, h, at, c="#1d130d", rim=None):
    """A Greek runner in black-figure style: leaning forward, arms swinging, legs apart; feet near y."""
    X = lambda a: x + a * h
    Y = lambda b: y - b * h
    els = [circ(X(.1), Y(.9), .08 * h, c, at=at),
           poly([(X(-.02), Y(.8)), (X(.14), Y(.82)), (X(.06), Y(.45)), (X(-.08), Y(.46))], c, at=at),
           ln([(X(.0), Y(.48)), (X(.28), Y(.3)), (X(.22), Y(0))], at, c, .06 * h, draw=False),
           ln([(X(-.04), Y(.48)), (X(-.22), Y(.26)), (X(-.42), Y(.14))], at, c, .06 * h, draw=False),
           ln([(X(.1), Y(.76)), (X(.32), Y(.62)), (X(.42), Y(.72))], at, c, .045 * h, draw=False),
           ln([(X(.02), Y(.76)), (X(-.2), Y(.62)), (X(-.3), Y(.5))], at, c, .045 * h, draw=False)]
    if rim:
        els.append(ln([(X(.14), Y(.82)), (X(.06), Y(.45))], at, rim, 1.5, draw=False))
    return [grp(els, at, "rise")]


def s31():
    """The games dial: a small dial in four quarters (four years), the names popping as said, Olympia first; a runner beside it."""
    t0, tg, to = T("s31", "And a small dial"), T("s31", "naming the games"), T("s31", "the Olympics")
    cx, cy, r = 700, 470, 230
    els = [circ(cx, cy, r + 30, "rgba(110,74,42,.4)", BRZ_L, 2, t0, fx="pop"), circ(cx, cy, r - 70, "none", BRZ_L, 1.4, t0 + .1)]
    els += [ln([(cx + (r - 70) * math.cos(math.radians(a)), cy + (r - 70) * math.sin(math.radians(a))), (cx + (r + 30) * math.cos(math.radians(a)), cy + (r + 30) * math.sin(math.radians(a)))],
               t0 + .2, BRZ_L, 2, draw=False) for a in (-90, 0, 90, 180)]
    els += [ln([(cx, cy), (cx + (r - 90) * math.cos(math.radians(-45)), cy + (r - 90) * math.sin(math.radians(-45)))], t0 + .4, AU, 4, dur=.4), circ(cx, cy, 10, AU, at=t0 + .4)]
    els += [lab(cx, cy + r + 80, "four years", t0 + .6, GOLD, 30)]
    for k, (name, a) in enumerate([("Olympia", -45), ("Isthmia", 45), ("Nemea", 135), ("Pythia", 225)]):
        at = to if k == 0 else to + .7 + .35 * k
        x, y = cx + (r - 20) * math.cos(math.radians(a)), cy + (r - 20) * math.sin(math.radians(a)) + 9
        els.append(lab(x, y, name, at, AU if k == 0 else BONE, 26, st="lab", fx="pop"))
    els += [gl(1300, 480, 260, to, .25, "lamp"), rect(1060, 640, 480, 10, "#c46d3a", at=to, op=.8)]
    els += runner(1300, 640, 300, to + .2, "#1d130d", rim="rgba(255,200,150,.5)")
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s32():
    """The back cover: rows of tiny letters, half of them dim until the scans double them; a magnifier shows the little golden sphere and
    the ball half black, half white."""
    t0, td, tb, tg, tm = (T("s32", "The scans doubled"), T("s32", "doubled"), T("s32", "The back cover"), T("s32", "little golden sphere"),
                          T("s32", "half black"))
    px, py, pw, ph = 170, 180, 720, 560
    els = [rect(px, py, pw, ph, "rgba(110,74,42,.55)", BRZ_L, 2, 8, -1)]
    for k in range(12):
        y = py + 30 + 42 * k
        bright = k % 2 == 0
        els.append({"k": "glyphs", "x": px + 30, "y": y, "w": pw - 60, "h": 24, "rows": 1, "cols": 26, "kind": "latin",
                    "c": "#f2e2c0", "in": -1 if bright else round(td + .1 * k, 2), "op": .9 if bright else .9})
    els += [lab(px + pw / 2, py + ph + 50, "the back cover", tb, DIM, 28)]
    els += [circ(1240, 460, 220, "rgba(20,14,10,.9)", "#e8cf98", 3, tg - .6, fx="pop"), ln([(890, 420), (1020, 440)], tg - .6, "#e8cf98", 3, dur=.3),
            circ(1160, 400, 40, AU, "#fff1c8", 2, tg, fx="pop"), gl(1160, 400, 90, tg + .1, .6, "lamp"),
            lab(1240, 230, "a little golden sphere", tg + .3, AU, 28)]
    els += moonball(1320, 540, 44, tm, phase=.5) + [lab(1240, 740, "half black, half white", tm + .4, BONE, 28)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def s33():
    """Eclipse colours and winds: two full Moons in a night sky; as the colours are named, one darkens to black, the other to a fiery red;
    four winds blow in; a ring of letters: the sky as the Greeks read it."""
    tc, tw, tg = T("s33", "notes their colour"), T("s33", "and the wind"), T("s33", "That's the sky")
    els = [circ(640, 460, 100, "#efe8da", "rgba(255,255,255,.7)", 2, -1), gl(640, 460, 170, -1, .25, "lamp"),
           circ(1140, 460, 100, "#efe8da", "rgba(255,255,255,.7)", 2, -1), gl(1140, 460, 170, -1, .25, "lamp"),
           circ(640, 460, 100, "#0d0b0a", "rgba(255,240,215,.5)", 2, tc, fx="fade", dur=1.0), lab(640, 620, "black", tc + .4, BONE, 30),
           circ(1140, 460, 100, "#8a2a1a", "#ffb08a", 2, tc + .8, fx="fade", dur=1.0), gl(1140, 460, 190, tc + .9, .6, "red"),
           lab(1140, 620, "fiery red", tc + 1.2, "#ffb08a", 30)]
    for k, (p, q) in enumerate([((180, 300), (360, 380)), ((1600, 300), (1420, 380)), ((180, 640), (360, 560)), ((1600, 640), (1420, 560))]):
        els.append(arr([p, ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - 20), q], tw + .15 * k, "#bfe6f5", 3, dur=.5))
    els += [lab(889, 230, "the wind", tw + .5, "#bfe6f5", 30)]
    for k in range(48):
        a = math.radians(360 * k / 48)
        x, y = 889 + 560 * math.cos(a), 470 + 300 * math.sin(a)
        els.append(ln([(x - 6, y), (x + 6, y)], tg + .02 * k, "rgba(242,226,192,.45)", 3, draw=False))
    return {"base": "sky", "tod": "night", "ground": 1200, "sun": False, "cam": CAM, "els": els}


def s34():
    """A calendar, an eclipse predictor and a games timetable (three icons), in a box the size of a shoebox: the case, upright, beside a
    shoebox; about 32 cm."""
    tc, te, tg, tb = T("s34", "A calendar"), T("s34", "an eclipse predictor"), T("s34", "games timetable"), T("s34", "in a box")
    els = [rect(240, 170, 110, 120, "#e9e2d2", "#8a7a5c", 1.5, 4, tc, fx="pop"), rect(240, 170, 110, 28, "#a83a2a", at=tc + .05, fx="pop")]
    els += [rect(256 + 22 * (k % 4), 210 + 20 * (k // 4), 14, 12, "#5a4a36", at=tc + .1, fx="pop") for k in range(12)]
    els += [circ(470, 230, 46, "#14110f", "#ffcf8a", 2, te, fx="pop"), gl(470, 230, 90, te + .1, .5, "sun")]
    els += [ln(E(620, 240, 52, 52, 12, 100, 260), tg, "#8fbf6a", 5, dur=.4), ln(E(620, 240, 52, 52, 12, -80, 80), tg + .1, "#8fbf6a", 5, dur=.4)]
    # the case and the shoebox (the case: about 315 x 190 x 100 mm; 1.4 units a mm)
    k_ = 1.4
    h, w, d = 315 * k_, 190 * k_, 100 * k_
    x0, yb = 820, 780
    dx, dy = d * .55, -d * .35
    case = [rect(x0, yb - h, w, h, WOOD, WOOD_L, 2, 4, tb, fx="pop"),
            poly([(x0 + w, yb), (x0 + w + dx, yb + dy), (x0 + w + dx, yb - h + dy), (x0 + w, yb - h)], WOOD_D, WOOD_L, 1.5, tb, fx="pop"),
            poly([(x0, yb - h), (x0 + w, yb - h), (x0 + w + dx, yb - h + dy), (x0 + dx, yb - h + dy)], "#8a6040", WOOD_L, 1.5, tb, fx="pop"),
            circ(x0 + w / 2, yb - h * .55, w * .36, BRZ, BRZ_L, 2, tb + .2, fx="pop"), circ(x0 + w / 2, yb - h * .55, w * .26, "none", BRZ_L, 1.2, tb + .2),
            ln([(x0 + w / 2, yb - h * .55), (x0 + w / 2 + w * .22, yb - h * .55 - w * .14)], tb + .3, AU, 3, draw=False)]
    sx = 1260
    shoe = [rect(sx, yb - h, w, h, "#b8946a", "#e8cfa0", 2, 4, tb + .5, fx="pop"),
            poly([(sx + w, yb), (sx + w + dx, yb + dy), (sx + w + dx, yb - h + dy), (sx + w, yb - h)], "#8a6c4a", "#e8cfa0", 1.5, tb + .5, fx="pop"),
            poly([(sx, yb - h), (sx + w, yb - h), (sx + w + dx, yb - h + dy), (sx + dx, yb - h + dy)], "#c9a87a", "#e8cfa0", 1.5, tb + .5, fx="pop"),
            rect(sx - 4, yb - h, w + 8, 40, "#a8845a", "#e8cfa0", 1.2, 3, tb + .6, fx="pop")]
    els += case + shoe
    els += [{"k": "dim", "x1": 770, "y1": yb, "x2": 770, "y2": yb - h, "t": "about 32 cm", "c": GOLD, "in": round(tb + .9, 2), "lx": -10},
            lab(x0 + w / 2, yb - h - 70, "the case", tb + .4, BONE, 26), lab(sx + w / 2, yb - h - 70, "a shoebox", tb + .8, BONE, 26)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


# ================================================================== CHAPTER 4 · The lost planets
COS = (889, 480)
RINGS = [("Moon", 74), ("Mercury", 110), ("Venus", 146), ("the Sun", 182), ("Mars", 218), ("Jupiter", 254), ("Saturn", 290)]


def s35():
    """The front display as the texts describe it: the Earth at the centre, rings outward (dashed: their layout is inferred), a little
    sphere on each, in order: Moon, Mercury, Venus, the Sun, Mars, Jupiter, Saturn; pointers from the centre."""
    t0, tr, tp, ts = T("s35", "The texts name"), T("s35", "Mercury to"), T("s35", "a pointer"), T("s35", "in order outward")
    cx, cy = COS
    els = [circ(cx, cy, 26, "#3f7fa8", "#bfe6f5", 2, t0, fx="pop"), gl(cx, cy, 70, t0 + .1, .45, "glowb"), lab(cx, cy + 62, "Earth", t0 + .3, "#bfe6f5", 26)]
    angs = [-30, 200, 120, -70, 40, 250, 160]
    for k, ((name, r), a) in enumerate(zip(RINGS, angs)):
        els.append(circ(cx, cy, r, "none", "rgba(201,193,238,.6)", 2, tr - .4 + .22 * k, fx="draw", dur=.5, style="inferred"))
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        els.append(ln([(cx, cy), (x, y)], tp + .15 * k, "rgba(242,226,192,.55)", 2, dur=.3))
        if name == "Moon":
            els += moonball(x, y, 13, ts + .2 * k, phase=.5)
        elif name == "the Sun":
            els += [circ(x, y, 15, AU, "#fff1c8", 1.5, ts + .2 * k, fx="pop"), gl(x, y, 40, ts + .2 * k, .6, "lamp")]
        else:
            els.append(circ(x, y, 11, "#efe8da", "rgba(255,255,255,.7)", 1.2, ts + .2 * k, fx="pop"))
    # labels: four of them, at the rings' outer side
    els += [lab(cx + 110 * math.cos(math.radians(200)) - 20, cy + 110 * math.sin(math.radians(200)) - 22, "Mercury", tr, BONE, 26, "end"),
            lab(cx + 290 * math.cos(math.radians(160)) - 24, cy + 290 * math.sin(math.radians(160)) + 8, "Saturn", tr + .9, BONE, 26, "end"),
            lab(cx + 182 * math.cos(math.radians(-70)) + 28, cy + 182 * math.sin(math.radians(-70)) - 6, "the Sun", ts + .7, AU, 26, "start")]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


SURV = [(-60, -80, 120, 95, 3), (70, -20, 70, 55, 5), (-90, 90, 60, 40, 7), (60, 120, 50, 40, 8), (130, -120, 36, 30, 9), (-150, 10, 34, 26, 11)]


def s36():
    """The gears that moved the planets are gone: the case outline (dashed), the surviving fragments in solid green filling about a third of
    it, the rings fading; a bar of three parts, one solid."""
    tg, tt = T("s36", "But the gears"), T("s36", "Only about a third")
    cx, cy = 760, 470
    w, h = 380, 600
    els = [rect(cx - w / 2, cy - h / 2, w, h, "rgba(201,193,238,.04)", "rgba(201,193,238,.7)", 2.5, 10, -1, style="inferred")]
    els += [circ(cx, cy, r, "none", "rgba(201,193,238,.35)", 1.6, -1, style="inferred") for r in (60, 100, 140, 175)]
    for k, (dx, dy, rx, ry, sd) in enumerate(SURV):
        els.append(poly(blob(cx + dx, cy + dy, rx, ry, 16, .22, sd), VERD_D, "rgba(170,210,190,.6)", 1.6, tt + .15 * k, fx="pop"))
    els += [lab(cx, cy - h / 2 - 30, "gears gone", tg + .4, LILAC, 30)]
    bx, by = 1180, 470
    els += [rect(bx, by - 30, 120, 60, VERD, "rgba(190,230,210,.8)", 2, 6, tt + .6, fx="pop"),
            rect(bx + 130, by - 30, 120, 60, "none", "rgba(201,193,238,.7)", 2, 6, tt + .7, style="inferred"),
            rect(bx + 260, by - 30, 120, 60, "none", "rgba(201,193,238,.7)", 2, 6, tt + .8, style="inferred"),
            lab(bx + 190, by + 90, "about a third survives", tt + 1.0, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def xi(x, y, s, at, c):
    """The Greek letter Xi, as three bars."""
    return [ln([(x - .4 * s, y + d * s), (x + .4 * s, y + d * s)], at, c, max(2, .1 * s), draw=False) for d in (-.45, 0, .45)]


def s37():
    """The front cover's text: rows of tiny letters; two spots light up gold, the Greek numerals for 462 (Venus) and 442 (Saturn)."""
    tv, ts = T("s37", "four hundred and sixty"), T("s37", "four hundred and forty")
    px, py, pw, ph = 230, 170, 1320, 360
    els = [rect(px, py, pw, ph, "rgba(70,52,34,.75)", BRZ_L, 2, 10, -1)]
    for k in range(7):
        els.append({"k": "glyphs", "x": px + 30, "y": py + 26 + 46 * k, "w": pw - 60, "h": 22, "rows": 1, "cols": 44, "kind": "latin", "c": "#d9c7a0", "in": -1, "op": .55})
    v = (620, py + 26 + 46 * 3 + 11)
    s_ = (1160, py + 26 + 46 * 5 + 11)
    for (x, y), t in ((v, tv), (s_, ts)):
        els += [rect(x - 90, y - 34, 180, 68, "rgba(232,195,90,.18)", AU, 2, 8, t, fx="pop"), gl(x, y, 120, t + .1, .5, "lamp")]
    els += [lab(v[0] - 40, v[1] + 16, "Y", tv + .2, AU, 46, st="serif", fx="pop")] + xi(v[0], v[1], 30, tv + .25, AU) + [lab(v[0] + 40, v[1] + 16, "B", tv + .3, AU, 46, st="serif", fx="pop")]
    els += [lab(s_[0], s_[1] + 16, "YMB", ts + .2, AU, 46, st="serif", fx="pop")]
    els += [ln([v, (v[0], 640)], tv + .5, AU, 1.6, dur=.3), lab(v[0], 690, "Venus: 462 years", tv + .7, AU, 32),
            ln([s_, (s_[0], 640)], ts + .5, AU, 1.6, dur=.3), lab(s_[0], 690, "Saturn: 442 years", ts + .7, AU, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s38():
    """Venus's dance with the Sun, seen from the Earth: a looping rosette draws itself round the centre and closes on its start: back in
    step after 462 years."""
    t0, tb = T("s38", "They're cycles"), T("s38", "almost exactly")
    cx, cy = 889, 470
    pts = []
    for k in range(721):
        t = 2 * math.pi * k / 720
        r = 210 + 80 * math.cos(13 * t / 1)
        a = t
        pts.append((cx + r * math.cos(a), cy + .85 * r * math.sin(a)))
    els = [circ(cx, cy, 18, AU, "#fff1c8", 1.5, t0, fx="pop"), gl(cx, cy, 60, t0 + .1, .6, "lamp"),
           ln(pts, t0 + .4, "#f4f0e0", 2.2, dur=max(1.5, tb - t0 - .2)),
           circ(pts[0][0], pts[0][1], 11, "#f4f0e0", "#ffffff", 1.4, t0 + .4, fx="pop"),
           gl(pts[0][0], pts[0][1], 50, tb, .7, "lamp", pulse=True)]
    els += chip(889, 150, "462 years", GOLD, t0 + .3, 28)
    els += [lab(pts[0][0] + 40, pts[0][1] - 30, "back in step", tb + .2, BONE, 28, "start")]
    return {"base": "dark", "stars": 80, "cam": CAM, "els": els}


def s39():
    """The 2021 model: a grid of 69 gears, the 30 that survive solid, the rest dashed (inferred); then a workbench: the next step is to build it."""
    t0, ti, tb = T("s39", "In"), T("s39", "more than half"), T("s39", "The team said")
    cols, x0, y0, d = 12, 200, 240, 82
    els = chip(x0 + d * 5.5, 160, "2021: 69 gears", GOLD, t0 + .2, 28)
    for k in range(69):
        x, y = x0 + d * (k % cols), y0 + d * (k // cols)
        if k < 30:
            els += gear(x, y, 30, 14, t0 + .6 + .03 * k, BRZ, BRZ_L, 1, hub=.25)
        else:
            els += gear_ring(x, y, 30, 14, ti - .4 + .02 * (k - 30), LILAC, 1.6, "inferred", dur=.3, hub=False)
    els += [lab(x0 + d * 2.5, y0 + d * 5 + 90, "30 survive", t0 + 1.8, BRZ_L, 28), lab(x0 + d * 8, y0 + d * 5 + 90, "inferred", ti + .4, LILAC, 28)]
    # the workbench
    bx = 1330
    els += [rect(bx, 600, 330, 18, "#5a4430", "#c9a070", 1.5, 3, tb), rect(bx + 20, 618, 14, 140, "#3a2c20", at=tb), rect(bx + 296, 618, 14, 140, "#3a2c20", at=tb),
            rect(bx + 90, 470, 150, 130, "none", LILAC, 2.5, 6, tb + .3, style="inferred"),
            ln([(bx + 20, 590), (bx + 70, 560)], tb + .5, "#d8dde2", 5, draw=False), rect(bx + 260, 572, 50, 24, "#6b4a30", at=tb + .5),
            lab(bx + 165, 420, "next: build it", tb + .7, GOLD, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s40():
    """The line: on the left, solid and lit, what is read in the bronze (a gear, a spiral dial, a strip of letters); on the right, lilac and
    dashed, what is inferred (the planets' gear train, the rings of the display)."""
    t0, tr, ti = T("s40", "So here's"), T("s40", "Read in the bronze"), T("s40", "Inferred")
    els = [ln([(889, 150), (889, 780)], t0 + .2, BONE, 3, dur=.6)]
    els += gear(330, 400, 90, 40, tr + .3, BRZ, BRZ_L, 1.4, spokes=4, hole="#1a120a", fx="pop")
    els += [ln(spiral_pts(600, 400, 20, 90, 3, n=200), tr + .7, AU, 2.5, dur=.6),
            {"k": "glyphs", "x": 260, "y": 560, "w": 420, "h": 50, "rows": 2, "cols": 18, "kind": "latin", "c": "#f2e2c0", "in": round(tr + 1.1, 2)},
            lab(470, 720, "read in the bronze", tr + .2, GREEN, 32)]
    for k, (x, y, r, n) in enumerate([(1100, 360, 60, 30), (1190, 330, 34, 16), (1250, 400, 44, 20), (1170, 460, 30, 14)]):
        els += gear_ring(x, y, r, n, ti + .2 + .15 * k, LILAC, 2, "inferred", dur=.4)
    els += [circ(1480, 400, r, "none", "rgba(201,193,238,.7)", 2, ti + .6 + .1 * j, style="inferred") for j, r in enumerate((40, 70, 100))]
    els += [lab(1290, 720, "inferred", ti + .2, LILAC, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s41():
    """Did it run smoothly? Two meshing gears with triangular teeth, a little uneven; where two teeth clash, a red flash: 'jam' (a 2025
    simulation); then corrosion spreads over the teeth: corrosion?"""
    t0, tj, tc = T("s41", "And did it"), T("s41", "it would jam"), T("s41", "They doubt")
    c1, r1, n1 = (560, 470), 250, 40
    c2, r2, n2 = (560 + 250 + 130 + 10, 470), 130, 21
    els = gear(c1[0], c1[1], r1, n1, -1, "#6e5a3e", "#d8b880", 1.4, h=26)
    els += gear(c2[0], c2[1], r2, n2, -1, "#8a6a42", "#f0c890", 1.4, h=26, phase=360 / n2 / 2)
    mx = c1[0] + r1 + 4
    els += chip(889, 160, "simulation, 2025", GOLD, t0 + 1.2, 26)
    els += [gl(mx, 470, 90, tj, .9, "red"), lab(mx + 10, 640, "jam", tj + .2, RED, 40, st="serif", fx="pop"),
            ln([(mx - 30, 430), (mx + 30, 510)], tj + .1, RED, 5, dur=.2), ln([(mx + 30, 430), (mx - 30, 510)], tj + .2, RED, 5, dur=.2)]
    rnd = random.Random(12)
    for k in range(14):
        a = math.radians(rnd.uniform(-60, 60))
        x, y = c1[0] + (r1 + rnd.uniform(-20, 10)) * math.cos(a), c1[1] + (r1 + rnd.uniform(-20, 10)) * math.sin(a)
        els.append(poly(blob(x, y, rnd.uniform(14, 30), rnd.uniform(10, 20), 12, .3, 200 + k), VERD, "none", 0, tc + .08 * k, curve=True, op=.75, fx="pop"))
    els += [lab(400, 180, "corrosion?", tc + 1.0, VERD_L, 32)] + qmark(1420, 300, tc + 1.4, 90)
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s42_add():
    """The planets are the boldest part: the rings glow lilac; one small solid gear sits apart (the fewest surviving gears)."""
    tb, tf = T("s42", "boldest part"), T("s42", "fewest surviving")
    cx, cy = COS
    els = [gl(cx, cy, 380, tb, .3, "glowb", pulse=True)]
    els += [circ(cx, cy, r, "none", LILAC, 3, tb + .1 * k, fx="draw", dur=.5, style="inferred") for k, (_, r) in enumerate(RINGS)]
    els += [lab(cx + 420, 210, "boldest part", tb + .4, LILAC, 32, st="ital")]
    els += gear(1420, 640, 50, 63, tf, VERD, VERD_L, 1.2, h=4, fx="pop") + [lab(1420, 740, "fewest surviving gears", tf + .3, VERD_L, 26)]
    return els


# ================================================================== CHAPTER 5 · Out of its time?
XT = lambda yr: round(200 + (yr + 250) / 250 * 1380, 1)        # 250 BCE to the year 1 (BCE years negative)


def coin(x, y, r, at, c=AU):
    return [grp([circ(x, y, r, c, "#fff1c8", 1.5, 0), circ(x, y, r * .72, "none", "rgba(120,80,20,.6)", 1.2, 0),
                 {"k": "glyphs", "x": round(x - r * .5, 1), "y": round(y - r * .25, 1), "w": round(r, 1), "h": round(r * .5, 1), "rows": 1, "cols": 3,
                  "kind": "latin", "c": "#7a5418", "in": 0}], at, "pop")]


def s43():
    """When: a timeline from 250 BCE to the year 1: the ship's coins and the wreck, about 70 to 60 BCE; the lettering's style, the second
    century BCE, with a dashed tail towards the wreck (or a little later)."""
    t0, tc, tl = .2, T("s43", "The ship's coins"), T("s43", "the style of its lettering")
    ay = 560
    els = [axis(200, 1580, ay, [(XT(-250), "250"), (XT(-200), "200"), (XT(-150), "150"), (XT(-100), "100"), (XT(-50), "50"), (XT(0), "1 CE")], t0 + .2, "years BCE")]
    els += coin(1200, 370, 30, tc + .2)
    els += [{"k": "band", "x0": XT(-70), "x1": XT(-60), "y": 430, "h": 22, "c": "#9fb6c8", "in": round(tc + .5, 2), "dur": .6},
            lab(1200, 494, "the wreck", tc + .7, "#9fb6c8", 28)]
    els += [{"k": "band", "x0": XT(-150), "x1": XT(-100), "y": 430, "h": 22, "c": AMBER, "in": round(tl, 2), "dur": .8},
            ln([(XT(-100), 441), (XT(-70), 441)], tl + .6, AMBER, 4, "inferred", dur=.6),
            lab((XT(-150) + XT(-100)) / 2, 494, "the lettering", tl + .4, AMBER, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def card(x, y, w, h, at, c="#e9dcc0", ink="#5a4a36", fx="pop", rows=4):
    return [rect(x, y, w, h, c, "#8a7a5c", 1.2, 3, at, fx=fx),
            {"k": "glyphs", "x": round(x + w * .12, 1), "y": round(y + h * .18, 1), "w": round(w * .76, 1), "h": round(h * .64, 1), "rows": rows, "cols": 5,
             "kind": "latin", "c": ink, "in": round(at + .1, 2)}]


def s44_add():
    """The dials' starting point: a gold marker at 205 BCE, a dashed one at 178; then a printed timetable at 205 and a copy of it much later,
    a dashed arrow between: a start date isn't a birth date."""
    t5, t8, tt = T("s44", "two hundred and five"), T("s44", "one hundred and seventy"), T("s44", "a timetable")
    els = [ln([(XT(-205), 250), (XT(-205), 560)], t5, AU, 3, dur=.6)] + chip(XT(-205), 220, "205 BCE?", AU, t5 + .3, 26)
    els += [ln([(XT(-178), 300), (XT(-178), 560)], t8, AU, 2.5, "inferred", dur=.5)] + chip(XT(-178) + 40, 290, "or 178?", AU, t8 + .3, 24, "start")
    els += card(XT(-205) - 150, 300, 110, 90, tt)
    els += card(XT(-100) - 55, 270, 110, 90, tt + .8)
    els += [arr([(XT(-205) - 40, 300), (XT(-150), 250), (XT(-100) - 60, 290)], tt + .5, BONE, 2.5, "inferred", dur=.7),
            lab(XT(-100), 240, "a later copy?", tt + 1.1, BONE, 26)]
    return els


VGR = View(12, 30, 33.5, 41.8, (90, 120, 1600, 680))


def s45():
    """Where: the calendar of Corinth and its colonies, Syracuse in Sicily and Epirus in the northwest (dashed arcs); a festival of Rhodes
    on the games dial; the wreck at Antikythera as a small marker."""
    v = VGR
    tc, tr = T("s45", "a calendar of"), T("s45", "a festival of")
    co, sy, ep, rh, an = v.p(22.93, 37.91), v.p(15.29, 37.08), v.p(20.99, 39.16), v.p(28.22, 36.43), v.p(23.3, 35.87)
    els = [{"k": "map", "land": v.land(), "in": -1},
           pin(*co, "Corinth", tc, GOLD, "start", 20, 34),
           arr([co, ((co[0] + sy[0]) / 2, (co[1] + sy[1]) / 2 - 90), sy], tc + .6, AMBER, 3, "inferred", dur=1.0),
           pin(*sy, "Syracuse", tc + 1.4, AMBER, "end", -20, 8),
           arr([co, ((co[0] + ep[0]) / 2 + 30, (co[1] + ep[1]) / 2 - 20), ep], tc + 1.0, AMBER, 3, "inferred", dur=.8),
           pin(*ep, "Epirus", tc + 1.8, AMBER, "end", -20, -10),
           pin(*rh, "Rhodes", tr, "#e8c35a", "start", 18, 8),
           gl(rh[0], rh[1], 70, tr + .2, .5, "lamp"),
           circ(an[0], an[1], 7, "#9fb6c8", at=-1), lab(an[0], an[1] + 38, "the wreck", .6, "#9fb6c8", 24),
           {"k": "scale", "x": 150, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": 1.2}]
    return {"base": "map", "cam": CAM, "els": els}


def saucer(x, y, s, at, c=LILAC):
    """A flying saucer, drawn as a dotted outline (a claim)."""
    els = [poly(E(x, y, 150 * s, 34 * s, 40), "rgba(201,193,238,.06)", c, 3, at, style="claimed"),
           poly(E(x, y - 30 * s, 60 * s, 40 * s, 30, 180, 360), "none", c, 3, at, style="claimed"),
           ln([(x - 60 * s, y + 30 * s), (x - 200 * s, y + 330 * s)], at, c, 2.5, "claimed", draw=False),
           ln([(x + 60 * s, y + 30 * s), (x + 200 * s, y + 330 * s)], at, c, 2.5, "claimed", draw=False)]
    return [grp(els, at, "pop")]


def s46():
    """The claim at its strongest: the fragment, small, ringed by a lilac dotted halo (out of place?); a dotted saucer lowers a dotted beam
    onto it (visitors?)."""
    tb, to, tv = T("s46", "Now, the boldest"), T("s46", "out-of-place"), T("s46", "a gift from visitors")
    els = frag_a(-1, scale=.5, dx=-11, dy=130, lamp=False)
    els += [gl(889, 620, 300, tb, .25, "lamp"),
            circ(889, 625, 250, "none", LILAC, 3, to, fx="draw", dur=.8, style="claimed"),
            lab(1180, 790 - 40, "out of place?", to + .6, LILAC, 32, "start", st="ital")]
    els += saucer(889, 230, 1.0, tv)
    els += [lab(1110, 210, "visitors?", tv + .5, LILAC, 32, "start", st="ital")]
    return {"base": "dark", "stars": 80, "cam": CAM, "els": els}


XL = lambda yr: round(160 + (yr + 400) / 1900 * 1460, 1)       # 400 BCE to 1500 CE


def clock_tower(x, y, h, at, c="#cbbca8"):
    els = [rect(x - .14 * h, y - h, .28 * h, h, "#3a3229", c, 1.5, 2, at), poly([(x - .2 * h, y - h), (x, y - 1.3 * h), (x + .2 * h, y - h)], "#3a3229", c, 1.5, at),
           circ(x, y - .75 * h, .1 * h, "none", AU, 2, at), ln([(x, y - .75 * h), (x + .05 * h, y - .8 * h)], at, AU, 2, draw=False)]
    return [grp(els, at, "pop")]


def s47():
    """Nothing this complex survives again for over a thousand years: a long timeline, the mechanism glowing near 100 BCE, then a dark
    empty stretch to the first great astronomical clocks of the 14th century; Price's jet plane glides across the gap in lilac dots."""
    t0, tj = T("s47", "And it's true"), T("s47", "Remember")
    ay = 600
    els = [axis(160, 1620, ay, [(XL(-400), "400 BCE"), (XL(0), "1 CE"), (XL(500), "500"), (XL(1000), "1000"), (XL(1500), "1500")], t0)]
    mx = XL(-100)
    els += gear(mx, ay - 40, 26, 14, t0 + .4, VERD, VERD_L, 1.2, fx="pop") + [gl(mx, ay - 40, 80, t0 + .5, .6, "lamp"), lab(mx, 420, "the mechanism", t0 + .6, GOLD, 26)]
    els += [rect(XL(-50), ay - 60, XL(1300) - XL(-50), 50, "rgba(0,0,0,.35)", at=t0 + .8),
            ln([(XL(-60), ay + 80), (XL(-60), ay + 96), (XL(1340), ay + 96), (XL(1340), ay + 80)], t0 + 1.0, BONE, 2, dur=.8),
            lab((XL(-60) + XL(1340)) / 2, ay + 140, "over 1,000 years", t0 + 1.4, BONE, 28)]
    els += clock_tower(XL(1350), ay - 6, 110, t0 + 1.8) + [lab(XL(1350), 420, "astronomical clocks", t0 + 2.0, BONE, 26)]
    els += [grp(jet(XL(500), 330, 230, 0), tj, "fade") | {"op": .8, "keepop": True}]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s48():
    """Look at what's on it: four evidence cards pop as named (Greek words, a Corinthian calendar, Greek games, Greek astronomy), then its
    limits under them: the Earth at the centre, eclipse times off by an hour or two, eclipse colours."""
    tb, tw, tc, tg, ta = T("s48", "But look"), T("s48", "Greek words"), T("s48", "A Corinthian calendar"), T("s48", "Greek games"), T("s48", "And Greek astronomy")
    tl = T("s48", "the Earth at the centre")
    th, tco = T("s48", "an hour or two"), T("s48", "eclipse colours")
    xs = [290, 690, 1090, 1490]
    els = []
    for k, (x, t) in enumerate(zip(xs, (tw, tc, tg, ta))):
        els += [rect(x - 170, 200, 340, 300, "rgba(255,236,206,.05)", "rgba(255,236,206,.35)", 1.5, 12, -1)]
    els += [{"k": "glyphs", "x": xs[0] - 120, "y": 300, "w": 240, "h": 80, "rows": 3, "cols": 10, "kind": "latin", "c": "#f2e2c0", "in": round(tw, 2)},
            lab(xs[0], 470, "Greek words", tw + .2, BONE, 28)]
    els += [circ(xs[1], 340, 90, "none", BRZ_L, 2.5, tc, fx="draw", dur=.5)] + \
           [ln([(xs[1] + 70 * math.cos(math.radians(a)), 340 + 70 * math.sin(math.radians(a))), (xs[1] + 90 * math.cos(math.radians(a)), 340 + 90 * math.sin(math.radians(a)))], tc + .2, BRZ_L, 2, draw=False) for a in range(0, 360, 30)] + \
           [lab(xs[1], 470, "Corinthian calendar", tc + .3, BONE, 28)]
    els += runner(xs[2], 420, 200, tg, "#d9c7a6") + [lab(xs[2], 470, "Greek games", tg + .2, BONE, 28)]
    els += [circ(xs[3], 340, 16, "#3f7fa8", "#bfe6f5", 1.5, ta, fx="pop")] + [circ(xs[3], 340, r, "none", "rgba(242,226,192,.6)", 1.6, ta + .1 * j) for j, r in enumerate((40, 65, 90))] + \
           [lab(xs[3], 470, "Greek astronomy", ta + .3, BONE, 28)]
    # the limits, under the cards
    els += [circ(600, 650, 14, "#3f7fa8", "#bfe6f5", 1.5, tl, fx="pop"), circ(600, 650, 36, "none", "rgba(242,226,192,.6)", 1.6, tl + .1),
            circ(889, 650, 44, "rgba(18,13,10,.85)", BONE, 2.5, th, fx="pop"),
            poly([(889, 650), (889, 606)] + [(889 + 44 * math.sin(math.radians(a)), 650 - 44 * math.cos(math.radians(a))) for a in range(0, 61, 10)], AMBER, at=th + .2, fx="pop"),
            lab(960, 660, "an hour or two", th + .3, AMBER, 26, "start"),
            circ(1250, 650, 30, "#8a2a1a", "#ffb08a", 1.5, tco, fx="pop"), gl(1250, 650, 60, tco + .1, .5, "red")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s49():
    """Close on a gear's rim (drawn large): triangular teeth cut by hand, about 1.5 mm apart, each slightly different; then the dotted saucer
    faint above and 'the same mistakes'."""
    t0, tv, tm = T("s49", "Its teeth"), T("s49", "If visitors"), T("s49", "the same mistakes")
    cx, cy, R_ = 889, 1700, 1100
    z = teeth_pts(cx, cy, R_, 100, 58, -134, -46, jitter=.16, seed=5)
    body = [(z[0][0], 1000)] + z + [(z[-1][0], 1000)]
    els = [poly(body, "#6e5a3e", "#e8c890", 2, -1), poly(body, "url(#k-shade)", "none", 0, -1),
           circ(cx, cy, R_ - 140, "none", "rgba(232,200,144,.35)", 2, -1)]
    tips = [p for i, p in enumerate(z) if i % 2 == 1]
    m = len(tips) // 2
    a, b = tips[m], tips[m + 1]
    els += [{"k": "dim", "x1": a[0], "y1": a[1] - 40, "x2": b[0], "y2": b[1] - 40, "t": "", "c": GOLD, "in": round(t0 + 1.2, 2)},
            lab((a[0] + b[0]) / 2, a[1] - 74, "about 1.5 mm", t0 + 1.4, GOLD, 28), lab(889, 760, "drawn large", t0 + 1.4, DIM, 24)]
    els += [ln([(p[0], p[1] - 10), (p[0], p[1] - 24)], t0 + 2.0 + .05 * k, "rgba(255,138,122,.8)", 2, draw=False) for k, p in enumerate(tips[1:-1])]
    els += [lab(889, 300, "not quite even", t0 + 2.4, RED, 28)]
    els += saucer(1460, 190, .5, tv) + [lab(889, 190, "the same mistakes", tm, BONE, 32, st="serif", fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s50():
    """What it shows and doesn't: a craftsman at a bench by lamp light, working on a gear wheel; a row of five dashed boxes with a question
    mark: how many?"""
    t0, tn = T("s50", "It shows"), T("s50", "It can't tell us")
    els = [rect(200, 600, 620, 16, "#5a4430", "#c9a070", 1.5, 3, -1), rect(220, 616, 14, 150, "#3a2c20", at=-1), rect(786, 616, 14, 150, "#3a2c20", at=-1)]
    els += desk_lamp(760, 600, -1) + [gl(700, 520, 300, -1, .45, "lamp")]
    els += seated(330, 766, 300, t0, "#d9c7a6")
    els += gear(560, 560, 60, 30, t0 + .4, BRZ, BRZ_L, 1.2, spokes=4, hole="#3a2c20", fx="pop")
    els += [ln([(620, 596), (680, 560)], t0 + .6, "#d8dde2", 4, draw=False), lab(500, 420, "one Greek workshop", t0 + .5, GOLD, 28)]
    for k in range(5):
        els.append(rect(1000 + 130 * k, 430, 100, 150, "none", LILAC, 2.5, 6, tn + .2 + .15 * k, style="inferred"))
    els += qmark(1320, 380, tn + 1.0, 80) + [lab(1320, 650, "how many?", tn + 1.2, LILAC, 32, st="ital")]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def armillary(x, y, r, at, c=LILAC, style="claimed"):
    """A sphere of rings (a lost geared sphere, known only from texts): dotted rings, the Sun and the Moon on them."""
    els = [circ(x, y, r, "none", c, 2.5, at, style=style), poly(E(x, y, r, r * .32, 40), "none", c, 2, at, style=style),
           poly(rot(E(x, y, r, r * .32, 40), x, y, 60), "none", c, 2, at, style=style), poly(rot(E(x, y, r, r * .32, 40), x, y, -60), "none", c, 2, at, style=style),
           circ(x, y, 10, "#3f7fa8", at=at), circ(x + r * .8, y - r * .3, 9, AU, at=at), circ(x - r * .6, y + r * .25, 8, "#efe8da", at=at)]
    return [grp(els, at, "pop")]


def toga(x, y, h, at, c="#e9dcc0"):
    """A figure in a toga holding a scroll, facing right."""
    X = lambda a: x + a * h
    Y = lambda b: y - b * h
    els = [circ(X(.02), Y(.9), .085 * h, "#d9c7a6", at=at),
           poly([(X(-.14), Y(.8)), (X(.14), Y(.8)), (X(.2), Y(0)), (X(-.2), Y(0))], c, "rgba(120,100,70,.6)", 1.2, at),
           ln([(X(-.14), Y(.78)), (X(.16), Y(.2))], at, "rgba(150,120,80,.7)", 3, draw=False),
           rect(X(.14), Y(.6), .1 * h, .2 * h, "#e9d6ad", "#8a6a3e", 1.2, 3, at)]
    return [grp(els, at, "rise")]


def s51():
    """Cicero's spheres: Cicero with his scroll; a sphere of dotted rings for Archimedes' (taken to Rome in 212 BCE, showing the Sun, the
    Moon, the planets, eclipses); a second for Posidonius'. Lilac: known only from texts."""
    tc, ta, tp, te = T("s51", "The Roman writer"), T("s51", "made by Archimedes"), T("s51", "And another"), T("s51", "even eclipses")
    els = static(toga(280, 700, 300, 0)) + [lab(280, 750, "Cicero", tc + .3, BONE, 28), gl(280, 500, 220, -1, .2, "lamp"),
                                         circ(800, 440, 170, "none", "rgba(201,193,238,.18)", 2, -1, style="claimed"), circ(1350, 440, 150, "none", "rgba(201,193,238,.18)", 2, -1, style="claimed")]
    els += armillary(800, 440, 170, ta) + [lab(800, 680, "Archimedes", ta + .4, LILAC, 30)]
    els += chip(800, 200, "212 BCE", GOLD, ta + 1.2, 26)
    els += [circ(800 - 102, 440 + 42, 12, "#8a2a1a", "#ffb08a", 1.5, te, fx="pop"), gl(800 - 102, 440 + 42, 46, te + .1, .6, "red")]
    els += armillary(1350, 440, 150, tp) + [lab(1350, 680, "Posidonius", tp + .4, LILAC, 30)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def flame(x, y, s, at, c="#ff7a4a"):
    return [poly([[x, y], [x - .45 * s, y - .35 * s], [x - .25 * s, y - .8 * s], [x - .05 * s, y - .55 * s], [x + .05 * s, y - 1.1 * s], [x + .35 * s, y - .6 * s],
                  [x + .45 * s, y - .3 * s]], c, "#ffd08a", 1.5, at, fx="pop", curve=True), gl(x, y - .5 * s, 1.6 * s, at, .5, "fire")]


def s52():
    """Why so few: a crucible over a fire, molten bronze glowing; a statue's arm, a bowl and a gear slide in one by one; at the right the
    sea in section, and one green lump sinks to the seabed."""
    tw, tp, ts = T("s52", "Bronze was worth"), T("s52", "into the pot"), T("s52", "This one survived")
    cx = 560
    els = [poly([(cx - 170, 400), (cx + 170, 400), (cx + 130, 620), (cx - 130, 620)], "#4a3a30", "#c9a070", 2, -1),
           poly([(cx - 160, 420), (cx + 160, 420), (cx + 150, 470), (cx - 150, 470)], "#ff9a4a", "none", 0, tw, fx="fade"), gl(cx, 440, 220, tw, .7, "fire", pulse=True)]
    els += flame(cx - 80, 680, 70, tw + .2) + flame(cx, 690, 90, tw + .3) + flame(cx + 80, 680, 70, tw + .4)
    els += bronze_arm(cx - 330, 260, 150, tw + .6, ang=20, fx="rise") + [arr([(cx - 200, 300), (cx - 100, 380)], tw + .8, BONE, 2.5, dur=.4)]
    els += [poly(E(cx + 300, 280, 50, 22, 18, 0, 180), "#7a5a3a", "#d8b880", 1.5, tw + 1.2, fx="rise"), arr([(cx + 260, 320), (cx + 120, 390)], tw + 1.4, BONE, 2.5, dur=.4)]
    els += gear(cx + 40, 230, 34, 18, tw + 1.8, BRZ, BRZ_L, 1.2, fx="rise") + [arr([(cx + 40, 280), (cx + 20, 380)], tw + 2.0, BONE, 2.5, dur=.4)]
    els += [lab(cx, 170, "the melting pot", tp, "#ffb070", 30)]
    # the sea, and the lump that sank
    sx = 1060
    els += [rect(sx, 260, 560, 520, "rgba(45,111,143,.55)", "rgba(159,208,255,.5)", 1.5, 10, ts - .2, fx="fade"),
            poly([(sx, 720), (sx + 200, 700), (sx + 400, 716), (sx + 560, 704), (sx + 560, 780), (sx, 780)], "#4a4032", at=ts - .1),
            arr([(sx + 280, 300), (sx + 290, 480), (sx + 280, 660)], ts + .2, "#bfe6f5", 2.5, "inferred", dur=.8),
            poly(blob(sx + 280, 690, 34, 18, 14, .2, 5), VERD, "rgba(190,230,210,.6)", 1.5, ts + .9, fx="pop"),
            lab(sx + 280, 236, "it sank", ts + .6, "#bfe6f5", 30)]
    return {"base": "dark", "stars": 0, "cam": CAM, "els": els}


def sundial_icon(x, y, r, at):
    return [grp([circ(x, y, r, "#a88a5a", "#e8cf98", 1.5, 0), circ(x, y, r * .6, "none", "rgba(80,60,30,.6)", 1.2, 0),
                 ln([(x, y), (x, y - r * .9)], 0, "#3a2a1a", 3, draw=False)], at, "pop")]


def astrolabe_icon(x, y, r, at):
    els = [circ(x, y, r, "#c9a050", "#fff1c8", 1.5, 0), circ(x, y, r * .75, "none", "#7a5418", 1.2, 0), ln([(x - r, y), (x + r, y)], 0, "#7a5418", 1.2, draw=False),
           ln([(x, y - r), (x, y + r)], 0, "#7a5418", 1.2, draw=False), circ(x, y - r - 8, 7, "none", "#c9a050", 3, 0)]
    return [grp(els, at, "pop")]


def s53_add():
    """The survivors on the long timeline: a Byzantine sundial with a few gears, about 500 CE; a geared astrolabe from Isfahan, 1221."""
    tb, ti = T("s53", "a Byzantine sundial"), T("s53", "an astrolabe made")
    ay = 600
    els = sundial_icon(XL(500), ay - 40, 26, tb) + [gl(XL(500), ay - 40, 70, tb + .1, .5, "lamp"), lab(XL(500), 500, "Byzantine sundial", tb + .3, BONE, 26)]
    els += astrolabe_icon(XL(1221), ay - 44, 26, ti) + [gl(XL(1221), ay - 44, 70, ti + .1, .5, "lamp"), lab(XL(1221) - 40, 500, "Isfahan, 1221", ti + .3, BONE, 26)]
    return els


def s54_add():
    """A craft mostly lost: a gold thread joins the survivors, solid at each, dotted across the long gaps."""
    t0 = T("s54", "Not a machine")
    ay = 600
    xs = [XL(-100), XL(500), XL(1221), XL(1350)]
    els = []
    for k in range(len(xs) - 1):
        els.append(ln([(xs[k] + 30, ay - 40), (xs[k + 1] - 30, ay - 40)], t0 + .4 + .5 * k, AU, 2.5, "claimed", dur=.5))
    els += [gl(XL(-100), ay - 40, 120, t0 + .2, .7, "lamp", pulse=True), lab(889, 250, "a craft mostly lost", t0 + 1.6, GOLD, 32, st="serif")]
    return els


# ================================================================== CHAPTER 6 · The weighing
LROWS = [200, 315, 430, 545, 660]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1180, y, grade, gc, gt, 28, "start")
    return out


def pic_gear(x, y, at):
    return gear(x, y, 34, 20, at, VERD, VERD_L, 1.2, spokes=4, hole="#1a120a", fx="pop")


def pic_rings(x, y, at):
    return [grp([circ(x, y, r, "none", LILAC, 1.6, 0, style="inferred") for r in (14, 26, 38)] + [circ(x, y, 6, "#3f7fa8", at=0), circ(x + 26, y - 6, 5, AU, at=0)], at, "pop")]


def pic_grid(x, y, at):
    els = []
    for k in range(6):
        gx, gy = x - 30 + 30 * (k % 3), y - 14 + 28 * (k // 3)
        els += gear(gx, gy, 11, 8, 0, BRZ if k < 2 else "none", BRZ_L if k < 2 else LILAC, 1, hub=.3)
    return [grp(els, at, "pop")]


def pic_pin(x, y, at):
    return [grp([poly([(x, y + 30), (x - 20, y - 4), (x - 20, y - 18), (x, y - 34), (x + 20, y - 18), (x + 20, y - 4)], "#f0b06a", "#fff1c8", 1.2, 0, curve=True),
                 circ(x, y - 12, 7, "#2a1e14", at=0)], at, "pop")]


def pic_saucer(x, y, at):
    return [grp([poly(E(x, y + 4, 44, 12, 24), "none", LILAC, 2, 0, style="claimed"), poly(E(x, y - 6, 18, 14, 16, 180, 360), "none", LILAC, 2, 0, style="claimed")], at, "pop")]


def s55():
    """The ledger, row 1: a geared calculator of the sky: Established."""
    tr, tg = T("s55", "A Greek calculator"), T("s55", "Established")
    els = [rect(110, 130, 1560, 600, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, tr, pic_gear, "a geared calculator of the sky", "Established", tg, GRADE["established"])
    els += [gl(1330, LROWS[0], 200, tg, .35, "lamp")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s56_add():
    """Rows 2 and 3: a display of five planets: Strong evidence; the 2021 model, gear by gear: Plausible."""
    t2, g2, t3, g3 = T("s56", "A display of"), T("s56", "Strong evidence"), T("s56", "The twenty twenty-one"), T("s56", "Plausible")
    els = lrow(1, t2, pic_rings, "a display of five planets", "Strong evidence", g2, GRADE["strong"])
    els += lrow(2, t3, pic_grid, "the 2021 model, gear by gear", "Plausible", g3, GRADE["plausible"])
    return els


def s57_add():
    """Rows 4 and 5: who made it, and where: Open question; out of its time, or from elsewhere: Ruled out (the saucer struck through)."""
    t4, g4, t5, g5 = T("s57", "Who made it"), T("s57", "Open question"), T("s57", "A machine out"), T("s57", "Ruled out")
    els = lrow(3, t4, pic_pin, "who made it, and where", "Open question", g4, GRADE["open"])
    els += lrow(4, t5, pic_saucer, "out of its time, or from elsewhere", "Ruled out", g5, GRADE["ruled"])
    els += [strike(170, LROWS[4] + 28, 262, LROWS[4] - 28, g5 + .2, RED, 5)]
    return els


def diver2(x, y, s, at, face=1):
    """A modern diver swimming (rebreather on the back), seen from the side."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    els = [poly([P(-.5, -.04), P(.3, -.08), P(.42, -.02), P(.3, .05), P(-.5, .06)], "#1a1f26", "rgba(200,230,255,.5)", 1.2, 0, curve=True),
           circ(*P(.46, -.03), .08 * s, "#1a1f26", "rgba(200,230,255,.5)", 1.2, 0),
           rect(P(-.25, -.2)[0] - (0 if f > 0 else .4 * s), P(-.25, -.2)[1], .4 * s, .12 * s, "#c9a050", "#fff1c8", 1, 4, 0),
           poly([P(-.5, -.02), P(-.78, -.12), P(-.74, .1)], "#2a3a4a", at=0), gl(*P(.55, -.03), .3 * s, 0, .4, "glowb")]
    return [grp(els, at, "rise")]


def s58():
    """What would change our minds: divers over the wreck, the hull's planks and frames on the seabed (2024); then the wanted items in lilac
    dashes: new pieces, a second mechanism, a line of text with a name, and an impossible part."""
    t0, tp, tm, tn, ti = (T("s58", "What would change"), T("s58", "New pieces"), T("s58", "A second mechanism"), T("s58", "A few more lines"),
                          T("s58", "And for the last"))
    sea = 200
    els = [{"k": "water", "y": sea, "h": 820, "op": .95, "in": -1},
           poly([(-40, 640), (500, 620), (1000, 640), (1820, 620), (1820, 1000), (-40, 1000)], "#4a4032", "rgba(255,226,190,.25)", 1.4, -1, curve=True)]
    hull = [(220, 628), (330, 596), (520, 584), (720, 590), (860, 612), (840, 640), (520, 650), (240, 646)]
    els += [poly(hull, "#5a3a22", "rgba(230,190,140,.6)", 1.6, tp - .6, curve=True, fx="rise")]
    els += [ln([(300 + 60 * k, 600 - 2 * (4 - abs(k - 4))), (300 + 60 * k, 646)], tp - .3 + .05 * k, "#8a6040", 4, dur=.25) for k in range(9)]
    els += [ln([(260, 620), (520, 604), (820, 616)], tp - .1, "rgba(230,190,140,.7)", 2, dur=.6, curve=True)]
    els += diver2(420, 470, 140, t0 + .3) + diver2(720, 400, 120, t0 + .6, face=-1)
    els += chip(540, 720 - 20, "2024", GOLD, tp + .2, 26) + [lab(540, 560, "the hull", tp + .4, BONE, 26)]
    # the wanted items
    els += [poly(blob(1060, 330, 70, 50, 14, .25, 9), "rgba(201,193,238,.08)", LILAC, 2.5, tp + 1.0, style="inferred", fx="pop"),
            lab(1060, 430, "new pieces", tp + 1.2, LILAC, 26),
            rect(1250, 270, 120, 150, "rgba(201,193,238,.06)", LILAC, 2.5, 6, tm, style="inferred", fx="pop"),
            circ(1310, 345, 40, "none", LILAC, 2, tm + .1, style="inferred"),
            lab(1310, 460, "a second mechanism", tm + .3, LILAC, 26),
            rect(1480, 290, 190, 80, "rgba(201,193,238,.06)", LILAC, 2.5, 6, tn, style="inferred", fx="pop"),
            {"k": "glyphs", "x": 1495, "y": 305, "w": 100, "h": 50, "rows": 2, "cols": 5, "kind": "latin", "c": "rgba(201,193,238,.8)", "in": round(tn + .2, 2)},
            rect(1605, 310, 50, 40, "none", AU, 2, 4, tn + .3, style="inferred"), lab(1575, 410, "a name", tn + .4, LILAC, 26)]
    els += [poly([(1180, 600), (1230, 560), (1290, 600), (1250, 660), (1200, 650)], "rgba(201,193,238,.08)", LILAC, 2.5, ti, style="claimed", fx="pop")] + \
           qmark(1236, 618, ti + .3, 44, halo=False) + [lab(1420, 620, "impossible part?", ti + .5, LILAC, 26, "start")]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [1600, 110, 20], "cam": CAM, "els": els}


# ================================================================== the film
def _stub(name):
    def f():
        return {"base": "dark", "stars": 20, "cam": CAM, "els": [lab(889, 470, name, -1, DIM, 40, st="serif")]}
    return f


def _stub_add():
    return []


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "X-rays of its", "s2"), (1, "The ship sank", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "One of them", "s6")], {"chapter": "A wreck full of statues"}),
    (1, 1, "collision", "s7", [(1, "Up come", "s8")], {}),
    (1, 2, "reversal", "s9", [(1, "The first to notice", "s10")], {}),
    (1, 3, "tag", "s11", [], {}),
    (2, 0, "world", "s12", [(1, "He said it", "s13")], {"chapter": "Counting the teeth"}),
    (2, 1, "collision", "s14", [(1, "Then they counted", "s15"), (1, "Double it", "s16"), (2, "In {1974", "s17")], {}),
    (2, 2, "reversal", "s18", [(1, "In the {1990s", "s19"), (1, "Wright showed", "s20")], {}),
    (2, 3, "tag", "s21", [], {}),
    (3, 0, "world", "s22", [(1, "It sliced", "s23"), (1, "And a metre-wide", "s24")], {"chapter": "Eight tonnes of X-rays"}),
    (3, 1, "collision", "s25", [(1, "But the Moon", "s26"), (1, "The machine copies", "s27"), (2, "And that pair", "s28")], {}),
    (3, 2, "reversal", "s29", [(1, "In its cells", "s30"), (1, "And a small dial", "s31"), (2, "The scans doubled", "s32"), (2, "Around the eclipse", "s33")], {}),
    (3, 3, "tag", "s34", [], {}),
    (4, 0, "world", "s35", [(1, "But the gears", "s36")], {"chapter": "The lost planets"}),
    (4, 1, "collision", "s37", [(0, "They're", "s38"), (1, "In {2021", "s39")], {}),
    (4, 2, "reversal", "s40", [(1, "And did it", "s41")], {}),
    (4, 3, "tag", "s42", [], {}),
    (5, 0, "world", "s43", [(1, "And its dials", "s44"), (2, "As for", "s45")], {"chapter": "Out of its time?"}),
    (5, 1, "collision", "s46", [(1, "And it's true", "s47")], {}),
    (5, 2, "reversal", "s48", [(1, "Its teeth", "s49"), (2, "It shows", "s50")], {}),
    (5, 3, "cost", "s51", [(1, "So why so few", "s52"), (2, "The next geared", "s53")], {}),
    (5, 4, "tag", "s54", [], {}),
    (6, 0, "weigh", "s55", [(1, "A display of", "s56"), (2, "Who made it", "s57")], {"chapter": "The weighing"}),
    (6, 1, "test", "s58", [], {}),
    (6, 2, "close", "s59", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1, 889, 500], "s2_add"),
    "s11": ("s9", [1, 889, 500], "s11_add"),
    "s17": ("s16", [1, 889, 500], "s17_add"),
    "s30": ("s29", [1.7, 900, 640], "s30_add"),
    "s42": ("s35", [1, 889, 500], "s42_add"),
    "s44": ("s43", [1, 889, 500], "s44_add"),
    "s53": ("s47", [1, 889, 500], "s53_add"),
    "s54": ("s47", [1, 889, 500], "s54_add"),
    "s56": ("s55", [1, 889, 500], "s56_add"),
    "s57": ("s55", [1, 889, 500], "s57_add"),
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
    ep = {"id": "lf-antikythera", "code": "LF.25", "series": script["series"], "title": script["title"], "case": "antikythera",
          "verdict": "solid", "claim": "Is the Antikythera mechanism a Greek calculator of the sky, or a machine out of its time?", "mood": "mystery",
          "hook_text": "A computer, 2,000 years *old*?", "beats": beats, "shots": shots,
          "sources": "Price 1974 (doi:10.2307/1006146) · Freeth et al. 2006 (doi:10.1038/nature05357) · Freeth et al. 2008 (doi:10.1038/nature07130) · "
                     "Freeth 2014 (doi:10.1371/journal.pone.0103275) · Carman & Evans 2014 (doi:10.1007/s00407-014-0145-5) · Anastasiou et al. 2016 (Almagest 7.1) · "
                     "Iversen 2017 (doi:10.2972/hesperia.86.1.0129) · Freeth et al. 2021 (doi:10.1038/s41598-021-84310-w) · Wright 2007 (doi:10.1179/030801807X163670) · "
                     "Jones 2017, 2018, 2020",
          "post": "A lump of green bronze from a Roman-era shipwreck turned out to hold thirty gear wheels and thousands of tiny Greek letters. The sponge "
                  "divers of 1900, Price's radiographs, Wright's tomography, the 2005 X-ray scans, the Moon's pin and slot, the eclipse spiral, the games "
                  "dial, the lost planets and the out-of-place claim, weighed.",
          "hashtags": ["#Antikythera", "#AntikytheraMechanism", "#AncientGreece", "#Astronomy", "#Archaeology", "#WeighItYourself"],
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
