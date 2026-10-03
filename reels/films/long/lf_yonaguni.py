"""LF.24 · Drowned Worlds · Yonaguni: The Steps Under the Sea (16:9 long film, one wall).

The script is films/long/lf-yonaguni/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s48; s4, the title, is the intro card over the
panel of s3), drawn while it is said: the stepped rock off Yonaguni under the sea (the hero, complete from the first frame), the
same rock dry in the Ice Age, the map of the Ryukyu chain and of the island, Kimura's survey and his reading of the hill (ring road,
walls, gate, channel, dents, finds, the face), rock-cut temples, Okinawan castles, the sandstone and mudstone laid down and lifted,
bedding and joints (iso models), the stack of paper, waves and fallen blocks, the coast of Sanninudai, Schoch's dives, the Ice Age
coast, the drowned stalactite cave, the sea-level band, the algae clock, Kimura's changing dates, the 2019 dugout crossing, what a
quarry leaves, the scorecard, the island's oldest traces, the mud nobody has dug, the ledger and the test. Drawings are schematic
and true to the numbers said: solid = measured or observed, dashed = inferred, dotted lilac = claimed (Kimura's readings).
The hero rock is about 25.6 units a metre (base 25 m down, top terrace about 5 m down, a diver 1.8 m long).

Facts: the Short 'yonaguni' (f04.py, rewrite/yonaguni.json) and the script's facts_added (Kimura 2000, 2004, Kimura et al. 2002,
2005, 2007; Ryall 2007; Schoch; Yazaki 1982; Ogata et al. 2020; Agency for Cultural Affairs 2024; Lambeck et al. 2014; Hijma et al.
2025; Hongo et al. 2015; Fujita et al. 2016; Nakagawa et al. 2010; Kaifu et al. 2020, 2025; Klemm & Klemm 2008; Pollard & Aydin
1988; Sunamura 1992). Short scenes adapted: yonaguni_m's crossing (canoe) and its sediment-nobody-dug picture, redrawn wide.

Engine workaround (as in lf_troy.py, lf_voynich.py and lf_atlantis.py): the wall only adds elements to a panel on its first visit,
at a beat start or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag
(+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item
(built on that step's clock). A speech clock estimates when each phrase is said, so build-ins follow the narration.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-yonaguni/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-yonaguni/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-yonaguni RC_FILMS_EPS=/tmp/claude-0/sbx_lf-yonaguni/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-yonaguni/boards python3 films.py long.lf_yonaguni
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-yonaguni", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, DIM, MUTED, ICE = "#f2c98e", "#cbbca8", "#bfb09c", "#cfe6ff"
SEA, SEAL, FOAM = "#2f6f8c", "#5fa8c9", "#bfe6f5"
# the rock under water (tinted blue-green) and in the open air (sunlit sandstone)
TOPW, FRONTW, SIDEW, EDGEW = "#a6a486", "#5d6355", "#454b45", "rgba(225,240,230,.38)"
TOPD, FRONTD, SIDED, EDGED = "#dcc7a0", "#a8895f", "#7b6449", "rgba(255,236,206,.5)"
SAND, SAND_D, MUD, MUD_D = "#d9c49a", "#b39a6e", "#7a6a58", "#5a4c3e"
WOOD, WOOD_D, SKIN, BLK = "#7a5536", "#4a3322", "#e8d6b8", "#1d2a30"
GRADE = {"established": "#8fd9b0", "plausible": "#7fd1d4", "open": "#f0b06a", "awaiting": "#c9c1ee"}


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


# ================================================================== small drawings (copied from lf_troy.py)
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
    return [rect(x0, y - h / 2, w, h, "rgba(14,16,18,.9)", c, 2.5, h / 2, at, fx="pop"),
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


def axis(x0, x1, y, ticks, at, t=None, below=True):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def balance(cx, py, L, base_y, at, left=None, right=None, drop=170, pan=230, c=BONE):
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


def rangle(x, y, at, s=22, c=GOLD, dx=1, dy=-1, w=3):
    """A small right-angle mark at a corner (x, y): two short legs along +-x and +-y."""
    return ln([(x + dx * s, y), (x + dx * s, y + dy * s), (x, y + dy * s)], at, c, w, dur=.35)


# ================================================================== the sea and the people in it
def underwater(top=122, rays=True, seed=7, dark=.55, floor=None):
    """Water over the whole panel: the surface just under `top`, light rays from the upper right, motes, the deep going dark."""
    els = [{"k": "water", "y": top, "h": 1000 - top + 40, "op": 1, "x0": -20, "x1": 1800, "in": -1},
           rect(-20, 430, 1820, 620, "url(#k-fadeup)", at=-1, op=dark)]
    if rays:
        for k, (x0, w, op) in enumerate(((1180, 70, .07), (1330, 110, .06), (1500, 60, .08), (1620, 90, .05), (960, 50, .045))):
            els.append(poly([(x0, top), (x0 + w, top), (x0 + w - 520, 900), (x0 - 560, 900)], "rgba(205,242,255,%.3f)" % op, at=-1))
    rnd = random.Random(seed)
    for k in range(46):
        x, y = rnd.uniform(20, 1760), rnd.uniform(top + 20, 790)
        els.append(dot(round(x, 1), round(y, 1), round(rnd.uniform(1, 2.6), 1), "#d9f2ff", -1, None, round(rnd.uniform(.12, .4), 2)))
    if floor is not None:
        els += sea_floor(floor)
    return els


def sea_floor(y0, x0=-20, x1=1800, seed=3):
    """Sand under water, with ripples."""
    pts = [(x0, y0 + 10)] + [(x, y0 + 6 * math.sin(x / 140.0) + 4) for x in range(int(x0), int(x1) + 1, 60)] + [(x1, y0 + 8), (x1, 1040), (x0, 1040)]
    els = [poly(pts, "#4f5446", "rgba(220,235,215,.3)", 1.5, -1)]
    rnd = random.Random(seed)
    for k in range(18):
        x, y = rnd.uniform(x0 + 40, x1 - 40), rnd.uniform(y0 + 22, y0 + 200)
        els.append(ln([(x - 30, y), (x, y - 4), (x + 30, y)], -1, "rgba(220,235,215,.18)", 2, draw=False, curve=True))
    return els


def surface_line(y, x0=-20, x1=1800, at=-1, c="#bfe6f5", w=2.5, op=.7):
    n = int((x1 - x0) / 40)
    return ln([[x0 + 20 * j, y - 5 * (j % 2)] for j in range(2 * n + 1)], at, c, w, curve=True, draw=False, op=op)


def diver(x, y, s, at, c=BLK, face=1, lamp=True, edge="#6a8a96"):
    """A swimming diver, nose at x + 52 s (face=1: facing right), body ~150 s long; y = the body's axis."""
    P = lambda a, b: (x + face * a * s, y + b * s)
    out = [poly([P(-60, -8), P(20, -14), P(40, -6), P(40, 6), P(20, 10), P(-60, 8)], c, edge, 1.2, at, fx="pop"),
           circ(*P(52, 0), 12 * s, c, edge, 1.2, at), rect(min(P(-30, -24)[0], P(20, -24)[0]), P(-30, -24)[1], 50 * s, 12 * s, "#c9a070", r=4, at=at),
           poly([P(-60, -6), P(-92, -18), P(-96, -8), P(-64, 4)], c, at=at), poly([P(-60, 6), P(-92, 16), P(-96, 6), P(-64, -2)], c, at=at)]
    if lamp:
        out.append(gl(*P(80, 10), 90 * max(.4, s), at, .9, "lamp"))
    return out


def bubbles(x, y, n, at, top=140, step=.18, seed=2):
    rnd = random.Random(seed)
    out, yy = [], y
    for k in range(n):
        yy -= rnd.uniform(28, 46)
        if yy < top:
            break
        out.append(circ(x + rnd.uniform(-8, 8), yy, rnd.uniform(2.5, 5), "rgba(220,245,255,.25)", "rgba(230,250,255,.7)", 1.2, round(at + step * k, 2), fx="pop"))
    return out


def fish(x, y, s, at, c="#9fc4d0", face=1, op=.75):
    P = lambda a, b: (x + face * a * s, y + b * s)
    return [poly([P(-10, 0), P(-4, -4), P(6, -3), P(10, 0), P(6, 3), P(-4, 4)], c, at=at, op=op, curve=True),
            poly([P(-10, 0), P(-16, -5), P(-15, 5)], c, at=at, op=op)]


def boat(x, y, w, at, c="#e9dccb", hull="#8a6a44"):
    """A small dive boat on the waterline y, centred on x."""
    h = w * .16
    return [poly([(x - w / 2, y - h), (x + w / 2, y - h * 1.2), (x + w / 2 - w * .12, y + h * .35), (x - w / 2 + w * .1, y + h * .35)], hull, c, 1.5, at, fx="pop"),
            rect(x - w * .18, y - h * 2.1, w * .3, h * .95, "#d8d2c4", "#8a7a66", 1.2, 3, at + .05, fx="pop"),
            ln([(x + w * .25, y - h * 1.2), (x + w * .25, y - h * 3.2)], at + .1, "#cbbca8", 2, draw=False),
            poly([(x + w * .25, y - h * 3.2), (x + w * .42, y - h * 2.9), (x + w * .25, y - h * 2.6)], "#e85a4a", at=at + .1, fx="pop")]


# ================================================================== the rock: terraces, under water, dry or on the coast
def jag(a, b, n, amp, rnd):
    """Points from a towards b (b excluded), the segment cut in n pieces whose inner points wander up to amp off the line."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    out = [a]
    for k in range(1, n):
        t = k / n
        d = rnd.uniform(-amp, amp)
        out.append((x0 + (x1 - x0) * t + nx * d, y0 + (y1 - y0) * t + ny * d))
    return out


# ---------------------------------------------------------------- terraces that recede: each tier set back in depth (the hero model)
TIERS = {"xa": [150, 262, 382, 474, 604], "z": [0, 60, 140, 200, 280], "h": [120, 210, 280, 370, 430], "Z": 420, "xb": 1250,
         "xbs": [1290, 1250, 1200, 1150, 1090], "fl": 770,
         "kx": .9, "ky": -.5, "joints": [250, 420, 560, 700, 880, 1050], "slot": 1110,
         "blocks": [(70, 0, -6, 76, 40, -10), (118, 14, -6, 50, 28, 12), (1310, 30, -6, 64, 34, 8), (1370, 70, -6, 44, 26, -12), (300, 30, 120, 50, 26, 6),
                    (430, 90, 210, 40, 22, -8)]}


def tpt(sp, x, z, h):
    """A point of the tiers (world x along the steps, z into the picture, h up) on the hero panel."""
    return (x + sp["kx"] * z, sp["fl"] - h + sp["ky"] * z)


def tread_front(sp, k, rnd=None, amp=0.0):
    """The front edge of tier k's tread, left to right (hero panel units), wandering a little."""
    a, b = tpt(sp, sp["xa"][k], sp["z"][k], sp["h"][k]), tpt(sp, sp["xb"], sp["z"][k], sp["h"][k])
    if not rnd:
        return [a, b]
    return jag(a, b, 12, amp, rnd) + [b]


def tiers(Tf=None, at=-1, mood="water", spec=None, seed=5, end=False, life=True, slot=True, fallen=True):
    """The rock as terraces that climb up and back (three-quarter view from the front right): each tier's riser faces us, its tread is
    seen from above, the treads run on out of frame (end=False) or stop at a stepped end face. Natural, not built: edges wander, corners
    are worn and chipped, joints run through all the tiers in line, the bedding runs along the risers, life grows on the treads (grass
    when dry), blocks that broke off lie at the foot and on the lower treads."""
    Tf = Tf or (lambda x, y: (x, y))
    sp = dict(TIERS)
    sp.update(spec or {})
    xa, zs, hs, Z = sp["xa"], sp["z"], sp["h"], sp["Z"]
    n = len(xa)
    xbs = list(sp.get("xbs") or [sp.get("end", 1450)] * n) if end else [sp["xb"]] * n
    xb = xbs[0]
    rnd = random.Random(seed)
    top, front, side, edge = {"water": ("#9aa38a", "#55605a", "#3f4a48", "rgba(220,238,230,.34)"),
                              "dry": (TOPD, FRONTD, SIDED, EDGED)}[mood]
    P = lambda pts: [Tf(x, y) for x, y in pts]
    Q = lambda x, z, h: tpt(sp, x, z, h)
    els = []
    fronts = {}
    for k in range(n):
        xb = xbs[k]
        fr = tread_front(dict(sp, xb=xb), k, rnd, 4.2)
        for _ in range(3 if k < n - 1 else 5):               # chips bitten out of the edge
            j = rnd.randrange(2, len(fr) - 3)
            (xa_, ya_), (xb_, yb_) = fr[j], fr[j + 1]
            d = rnd.uniform(7, 15)
            fr = fr[:j + 1] + [(xa_ + (xb_ - xa_) * .25, ya_ + d), (xa_ + (xb_ - xa_) * .75, ya_ + d * .8)] + fr[j + 1:]
        fronts[k] = fr
        bk = [Q(xb, Z, hs[k]), Q(xa[k], Z, hs[k])]
        bk = jag(bk[0], bk[1], 10, 4 if k == n - 1 else 2, rnd) + [bk[1]]
        lf = jag(Q(xa[k], Z, hs[k]), Q(xa[k], zs[k], hs[k]), 6, 6, rnd)
        els.append(poly(P(fr + bk + lf[1:]), top, edge, 1.0, at))
        lo = hs[k - 1] if k else -10
        base = jag(Q(xb, zs[k], lo), Q(xa[k], zs[k], lo), 10, 2, rnd) + [Q(xa[k], zs[k], lo)]
        lside = jag(Q(xa[k], zs[k], lo), fr[0], 4, 2.4, rnd)
        els.append(poly(P(fr + base[:-1] + lside), front, edge, 1.0, at))
        # bedding on the riser (one line on the short risers, two on the tall bottom one)
        for f in ((.33, .66) if (hs[k] - lo) > 90 else (.5,)):
            hh = lo + (hs[k] - lo) * f + rnd.uniform(-4, 4)
            pts = [Q(x, zs[k], hh + rnd.uniform(-1.5, 1.5)) for x in range(int(xa[k]) + 6, int(xb), 70)]
            els.append(ln(P(pts), at, "rgba(18,24,22,.36)" if mood == "water" else "rgba(70,48,28,.4)", rnd.choice((1.3, 1.8)), draw=False))
        # joints: one crack per joint plane, in line through the tiers: down the riser and back across the tread
        jt = "rgba(10,14,13,.66)" if mood == "water" else "rgba(55,36,20,.62)"
        for i, x in enumerate(sp["joints"]):
            if not (xa[k] + 15 < x < xb - 15):
                continue
            els.append(ln(P([Q(x, zs[k], hs[k]), Q(x + rnd.uniform(-3, 3), zs[k], (hs[k] + lo) / 2), Q(x, zs[k], lo + 2)]), at, jt, 2.6 if i % 3 == 1 else 1.8, draw=False))
            zend = zs[k + 1] if (k < n - 1 and xa[k + 1] <= x <= xbs[k + 1]) else Z
            els.append(ln(P([Q(x, zs[k], hs[k]), Q(x + rnd.uniform(-4, 4), (zs[k] + zend) / 2, hs[k]), Q(x, zend, hs[k])]), at, jt, 1.6, draw=False))
        if end:                                              # the end face of this tier: rough, its bedding running back
            ef = jag(Q(xb, zs[k], lo), Q(xb, zs[k], hs[k]), 3, 3, rnd) + jag(Q(xb, zs[k], hs[k]), Q(xb, Z, hs[k]), 6, 4, rnd)
            ef += jag(Q(xb, Z, hs[k]), Q(xb, Z, lo), 3, 5, rnd) + [Q(xb, Z, lo)]
            ef = [ef[0]] + [(x + rnd.uniform(-2, 2), y + rnd.uniform(-2, 2)) for x, y in ef[1:-1]] + [ef[-1]]
            els.append(poly(P(ef), side, edge, 1.2, at))
            for f in ((.33, .66) if (hs[k] - lo) > 90 else (.5,)):
                hh = lo + (hs[k] - lo) * f
                els.append(ln(P([Q(xb, zs[k] + 4, hh), Q(xb, Z - 4, hh)]), at, "rgba(18,24,22,.3)" if mood == "water" else "rgba(70,48,28,.35)", 1.4, draw=False))
        # life on the tread (crusts, weed) or grass (dry); stains or weathering pits on the riser
        zend_all = Z
        for j in range(10 if k < n - 1 else 18):
            x = rnd.uniform(xa[k] + 20, min(xb, 1900) - 20)
            zmax = zs[k + 1] if (k < n - 1 and xa[k + 1] <= x <= xbs[k + 1]) else zend_all
            z = rnd.uniform(zs[k] + 8, zmax - 8)
            gx, gy = Tf(*Q(x, z, hs[k]))
            if mood == "water" and life:
                c = rnd.choice(["#c58a96", "#7f9a66", "#b4a8c6", "#7f9a66", "#8a9a72"])
                els.append(poly(E(round(gx, 1), round(gy, 1), rnd.uniform(7, 16), rnd.uniform(2.5, 5), 10), c, at=at, op=.55))
                if rnd.random() < .25:
                    els.append(ln([(gx, gy), (gx - 4, gy - 13), (gx - 1, gy - 6), (gx + 3, gy - 15)], at, "#9cb07a", 2, draw=False, op=.8))
            elif mood == "dry":
                els.append(ln([(gx - 6, gy), (gx - 2, gy - 10), (gx, gy), (gx + 3, gy - 12), (gx + 6, gy)], at, "#7d9a52", 2, draw=False))
        for j in range(3):                                   # tone on the tread: pale sand pockets, darker mats
            x = rnd.uniform(xa[k] + 40, min(xb, 1900) - 60)
            zmax = zs[k + 1] if (k < n - 1 and xa[k + 1] <= x <= xbs[k + 1]) else Z
            gx, gy = Tf(*Q(x, rnd.uniform(zs[k] + 10, zmax - 10), hs[k]))
            c = rnd.choice(["#b9b796", "#7f8a6c", "#a9ad8e"]) if mood == "water" else rnd.choice(["#e8d6b0", "#c4ab7e"])
            els.append(poly(E(round(gx, 1), round(gy, 1), rnd.uniform(40, 90), rnd.uniform(8, 16), 14), c, at=at, op=.45, curve=True))
        for j in range(4):
            x = rnd.uniform(xa[k] + 30, min(xb, 1900) - 30)
            gx, gy = Tf(*Q(x, zs[k], lo + (hs[k] - lo) * rnd.uniform(.2, .8)))
            els.append(poly(E(round(gx, 1), round(gy, 1), rnd.uniform(5, 14), rnd.uniform(3, 6), 10), "#1c2422" if mood == "water" else "#5c4630", at=at, op=.4))
    if slot and sp.get("slot") and sp["slot"] < xbs[-1] - 40:  # the narrow trench along the top tier (a joint the sea has widened)
        x, k = sp["slot"], n - 1
        dark = "#16201f" if mood == "water" else "#3a2a1c"
        els += [poly(P([Q(x, zs[k], hs[k]), Q(x + 24, zs[k], hs[k]), Q(x + 24, Z, hs[k]), Q(x, Z, hs[k])]), dark, at=at),
                poly(P([Q(x, zs[k], hs[k]), Q(x + 24, zs[k], hs[k]), Q(x + 23, zs[k], hs[k] - 46), Q(x + 1, zs[k], hs[k] - 42)]), dark, at=at)]
    if mood == "water":                                      # sand drifted against the foot
        xe_ = xbs[0] if end else min(xbs[0], 1880)
        dr = [Tf(xa[0] - 60, sp["fl"] + 14)] + [Tf(x, sp["fl"] - 4 - 8 * abs(math.sin(x / 97.0)) - rnd.uniform(0, 5)) for x in range(int(xa[0]) - 40, int(xe_), 60)]
        dr += [Tf(xe_, sp["fl"] + 14)]
        els.append(poly(dr, "#4f5446", "rgba(220,235,215,.22)", 1.2, at, curve=True))
    if fallen:                                               # blocks that broke off along the joints: at the foot, and on the lower treads
        spots = sp.get("blocks", [(120, 0, -6, 70, 40, -10), (172, 10, -6, 46, 26, 12), (250, 30, hs[0], 52, 26, 6), (380, 110, hs[1], 40, 22, -8)])
        for (bx, bz, bh, bw, bt, a) in spots:
            x0, y0 = Q(bx, bz, bh)
            c_, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
            q = [(-bw / 2, -bt * .9), (bw * .1, -bt), (bw / 2, -bt * .8), (bw / 2 + 3, 0), (-bw / 2 - 2, 2)]
            q = [(x0 + (u * c_ - v * s_) + rnd.uniform(-2, 2), y0 + (u * s_ + v * c_) + rnd.uniform(-2, 2)) for u, v in q]
            els.append(poly(P(q), front, edge, 1.0, at))
            els.append(poly(P([q[0], q[1], q[2], (q[2][0] + 12, q[2][1] - 7), (q[0][0] + 12, q[0][1] - 7)]), top, edge, 1.0, at))
    return els


def tread_edges(Tf, at, c=GOLD, w=4, step=.25, ks=range(5), sp=None, x1=None):
    """Gold traces along the front edges of the treads (up to x1 in world units, default the frame's edge)."""
    sp = dict(TIERS, **(sp or {}))
    out = []
    for i, k in enumerate(ks):
        xe = x1 or sp["xbs"][k] - 4
        out.append(ln([Tf(*tpt(sp, sp["xa"][k] + 8, sp["z"][k], sp["h"][k])), Tf(*tpt(sp, xe, sp["z"][k], sp["h"][k]))], at + step * i, c, w, dur=.6))
    return out


def wall_edges(Tf, at, c=GOLD, w=4, step=.22, ks=range(5), sp=None):
    """Gold traces down the left ends of the risers."""
    sp = dict(TIERS, **(sp or {}))
    out = []
    for i, k in enumerate(ks):
        lo = sp["h"][k - 1] if k else 0
        out.append(ln([Tf(*tpt(sp, sp["xa"][k], sp["z"][k], sp["h"][k] - 4)), Tf(*tpt(sp, sp["xa"][k], sp["z"][k], lo))], at + step * i, c, w, dur=.45))
    return out


def corner(sp, k):
    """Where the tread meets the riser at the left end of tier k (a right angle)."""
    return tpt(sp, sp["xa"][k], sp["z"][k], sp["h"][k])


ID = lambda x, y: (x, y)


# ================================================================== COLD OPEN
def far_ridge(top=122, at=-1):
    """Farther rock beyond the terraces, bluer (the water between): the reef running on to the right."""
    return [poly([(1380, 330), (1480, 290), (1600, 276), (1700, 262), (1800, 258), (1800, 780), (1380, 780)], "#34505c", "rgba(200,230,240,.16)", 1.2, at),
            poly([(1560, 470), (1640, 430), (1720, 420), (1800, 418), (1800, 780), (1560, 780)], "#2c4550", at=at)]


def s1():
    """The hero image, complete from the first frame: terraces climbing up and back under the sea, a farther mass behind, a diver with a
    lamp beside them (1.8 m to scale); treads, walls and right angles trace in gold as they are named."""
    sp = TIERS
    els = underwater(122, floor=770) + far_ridge() + tiers(ID, -1, "water", end=True)
    els += [rect(-20, 560, 1820, 480, "url(#k-fadeup)", at=-1, op=.28)]
    els += diver(400, 400, .32, -1, face=-1) + bubbles(386, 392, 6, -1, top=300)
    els += fish(250, 520, 1.4, -1) + fish(282, 546, 1.2, -1) + fish(306, 512, 1.3, -1) + fish(1300, 140, 1.1, -1, face=-1) + fish(1330, 132, 1.0, -1, face=-1)
    tf, tw, ta = T("s1", "Flat terraces"), T("s1", "Sheer walls"), T("s1", "right angles")
    els += tread_edges(ID, tf)
    els += wall_edges(ID, tw)
    els += [rangle(*corner(sp, k), ta + .25 * i, 24, GOLD, 1, 1) for i, k in enumerate((2, 3, 4))]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s2():
    """'Some call it a drowned pyramid': the same terraces seen dimly, smaller, ending at a rough stepped face; a lilac dotted stepped
    pyramid traced over their steps and mirrored on the far side (a reading, not a find). 'Who carved...?': a question mark."""
    tp, tq = T("s2", "drowned pyramid"), T("s2", "Who carved")
    sp = dict(TIERS)
    k_, xm = .66, 1000
    Tm = lambda x, y: (889 + (x - xm) * k_, 720 - (770 - y) * k_)
    els = underwater(122, rays=True, seed=2, dark=.65, floor=720)
    els += tiers(Tm, -1, "water", sp, seed=5, end=True, fallen=False, life=False)
    els += [rect(-20, 120, 1820, 900, "#0b1c26", at=-1, op=.3)]
    left = []
    for k in range(5):
        left += [tpt(sp, sp["xa"][k], sp["z"][k], sp["h"][k - 1] if k else 0), corner(sp, k)]
    right = [(2 * xm - x, y) for x, y in left[::-1]]
    path = [Tm(x, y) for x, y in left + right]
    els += [ln(path, tp, LILAC, 4.5, "claimed", 2.0), gl(889, 470, 420, tp, .25, "lamp"),
            lab(889, 300, "a drowned pyramid?", tp + 1.0, LILAC, 40, st="ital")]
    els += qmark(1450, 300, tq, 110)
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s3():
    """The same terraces in the open air at dusk: the Ice Age coast, the sea far off at the horizon; a lilac figure on the top terrace
    (a question, not a find); the clocks of the sea, and the mud on the steps."""
    tq, tc, tm = T("s3", "last dry land"), T("s3", "sea's own clocks"), T("s3", "buried in the mud")
    sp = TIERS
    els = [poly([(-20, 590), (900, 586), (900, 604), (-20, 610)], "#3f6f8a", at=-1), surface_line(590, -20, 900, -1, "rgba(255,226,190,.55)", 1.5, .8)]
    els += tiers(ID, -1, "dry", seed=7, end=True)
    px, py = tpt(sp, 1000, 360, sp["h"][4])
    els += [person(px, py, 44, -1, LILAC, None) | {"op": .9, "keepop": True}]
    els += qmark(720, 240, tq, 110)
    cx, cy = 300, 470
    els += [circ(cx, cy, 34, "rgba(20,30,40,.6)", ICE, 3, tc, fx="pop"), ln([(cx, cy), (cx, cy - 22)], tc + .1, ICE, 3, draw=False),
            ln([(cx, cy), (cx + 16, cy + 6)], tc + .1, ICE, 3, draw=False), gl(cx, cy, 80, tc, .5, "blue")]
    for k in range(4):
        x0 = sp["xa"][k + 1] + 60
        zm = (sp["z"][k] + sp["z"][k + 1]) / 2
        pts = [tpt(sp, x0 + dx_, zm + dz_, sp["h"][k]) for dx_, dz_ in ((-60, -18), (90, -22), (110, 16), (-40, 22))]
        els += [poly(pts, "#6b4a2e", "rgba(255,200,140,.6)", 2, tm + .15 * k, fx="pop", curve=True)]
    rnd = random.Random(33)
    for k in range(16):                                      # shrubs and low trees on the coastal plain and the treads
        x = rnd.choice([rnd.uniform(-10, 140), rnd.uniform(1330, 1790)])
        y = 772 + rnd.uniform(-4, 10)
        r = rnd.uniform(16, 34)
        els += [poly(E(x, y - r * .7, r, r * .7, 14), rnd.choice(["#2f3b28", "#3a4a2e", "#283222"]), at=-1, curve=True)]
    for k, (x, z) in enumerate(((330, 30), (560, 100), (900, 170), (1180, 120), (720, 240))):
        tier = max(i for i in range(5) if sp["z"][i] <= z)
        gx, gy = tpt(sp, x, z, sp["h"][tier])
        els += [poly(E(gx, gy - 12, 22, 14, 12), "#3a4a2e", at=-1, curve=True)]
    return {"base": "sky", "tod": "dusk", "ground": 770, "sun": [180, 556, 26], "groundc": "#3a3a2a",
            "ridges": [{"y": 600, "a": 30, "c": "#2f3428", "seed": 4}, {"y": 644, "a": 20, "c": "#262b22", "seed": 8}], "cam": CAM, "els": els}


# ================================================================== CHAPTER 1 · Ruins Point
VM = View(118.0, 131.5, 22.6, 29.6, (90, 120, 1600, 680))
YON = [(122.934, 24.449), (122.938, 24.455), (122.947, 24.459), (122.957, 24.462), (122.970, 24.465), (122.985, 24.468), (123.000, 24.470),
       (123.015, 24.468), (123.030, 24.464), (123.040, 24.460), (123.047, 24.455), (123.043, 24.449), (123.035, 24.445), (123.025, 24.441),
       (123.013, 24.437), (123.000, 24.434), (122.985, 24.436), (122.975, 24.440), (122.965, 24.437), (122.952, 24.438), (122.942, 24.442),
       (122.936, 24.446)]                                # Yonaguni, schematic outline (about 11.5 by 4 km); the 50 m coast lacks it


def s5():
    """The map: Taiwan, the Ryukyu chain, Yonaguni at its western end; 110 km to Taiwan, visible on a clear day."""
    v = VM
    t1, t2, t3 = T("s5", "Yonaguni is"), T("s5", "southern chain"), T("s5", "a hundred and ten")
    tc = T("s5", "clear day")
    yx, yy = v.p(123.0, 24.45)
    tx, ty = v.p(121.86, 24.55)
    mx, my = v.p(121.2, 23.9)
    chain = [v.p(129.5, 28.3), v.p(128.4, 27.3), v.p(127.8, 26.4), v.p(126.6, 25.6), v.p(125.3, 24.8), v.p(124.15, 24.4), (yx + 10, yy - 2)]
    els = map_base(v) + [
           arr([v.p(129.8, 28.9), v.p(130.6, 29.5)], .8, AMBER, 3, dur=.6, curve=False),
           lab(*v.p(130.2, 28.6), "to mainland Japan", 1.0, AMBER, 26, "end"),
           {"k": "pin", "x": yx, "y": yy, "t": "Yonaguni", "c": GOLD, "lx": 18, "ly": 36, "in": t1},
           ln(chain, t2, AMBER, 3, "inferred", 1.4, curve=True),
           ln([(tx + 4, ty), (yx - 12, yy)], t3, BONE, 3, dur=.6),
           lab((tx + yx) / 2, ty - 34, "110 km", t3 + .3, BONE, 28),
           ln([(yx - 10, yy + 8), (mx + 10, my - 4)], tc, ICE, 2.5, "claimed", .6),
           lab(yx + 4, yy + 92, "Taiwan visible on a clear day", tc + .3, ICE, 24, "start", st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def map_base(v):
    """The chain map as it stands once drawn: coasts, Yonaguni (schematic), names, the scale."""
    return [{"k": "map", "land": v.land(), "in": -1},
            poly([v.p(lo, la) for lo, la in YON], "#3a2f24", "#c9ad85", 1.6, -1),
            lab(*v.p(120.75, 23.35), "Taiwan", .3, "#cbbca8", 32),
            lab(*v.p(127.75, 26.95), "Okinawa", .6, "#cbbca8", 26),
            lab(*v.p(124.6, 27.7), "East China Sea", .9, "#9fd0ff", 30, st="ital"),
            lab(*v.p(128.6, 24.0), "Pacific Ocean", 1.1, "#9fd0ff", 30, st="ital"),
            {"k": "scale", "x": 140, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": 1.2}]


VI = View(122.915, 123.065, 24.415, 24.485, (90, 110, 1600, 480))


def s6():
    """Yonaguni in plan (schematic): the dive boat off the south-east coast in 1986; a magnifier shows a diver over giant steps; the pin."""
    v = VI
    tb, tm, tn = T("s6", "nineteen eighty-six"), T("s6", "Beneath him"), T("s6", "Ruins Point")
    sx, sy = v.p(123.0114, 24.4352)
    els = [poly([v.p(lo, la) for lo, la in YON], "#4a5a3a", "#c9d79a", 2.5, -1, curve=True),
           poly([v.p(lo, la) for lo, la in ((122.952, 24.452), (122.975, 24.458), (122.995, 24.459), (123.010, 24.455), (122.995, 24.448), (122.965, 24.446))],
                "#5c6e44", at=-1, curve=True, op=.8),
           poly([v.p(lo, la) for lo, la in ((123.015, 24.452), (123.030, 24.456), (123.040, 24.452), (123.028, 24.446))], "#5c6e44", at=-1, curve=True, op=.8)]
    els += [lab(*v.p(122.99, 24.4625), "Yonaguni", .2, "#efe6d2", 40, st="serif"),
            lab(v.p(122.934, 24.449)[0] - 18, v.p(122.934, 24.449)[1] + 8, "Cape Irizaki", .5, "#cbbca8", 24, "end"),
            lab(*v.p(122.958, 24.427), "south coast", .7, "#9fd0ff", 26, st="ital"),
            {"k": "scale", "x": 150, "y": 520, "w": round(v.km(2), 1), "t": "2 km", "in": .9}]
    els += boat(sx + 6, sy + 30, 64, tb)
    els += chip(sx - 70, sy + 34, "1986", AMBER, tb + .2, 26, "end")
    cx, cy, r = sx - 40, 664, 118                            # the magnifier: what lies beneath the boat
    els += [ln([(sx + 10, sy + 44), (cx + r * .6, cy - r * .8)], tm, "rgba(207,230,255,.7)", 2, dur=.4),
            ln([(sx - 10, sy + 44), (cx - r * .6, cy - r * .8)], tm, "rgba(207,230,255,.7)", 2, dur=.4)]
    sp = dict(TIERS)
    Tm = lambda x, y: (cx - 120 + (x - 150) * .2, cy + 88 + (y - 770) * .2)
    inner = [rect(cx - r, cy - r, 2 * r, 2 * r, "url(#k-water)", at=-1)] + tiers(Tm, -1, "water", sp, seed=9, end=True, fallen=False, life=False)
    inner += diver(cx - 70, cy - 60, .26, -1, face=1) + bubbles(cx - 60, cy - 66, 3, -1, top=cy - r + 8)
    els += [{"k": "group", "clip": [cx - r, cy - r, 2 * r, 2 * r, r], "els": inner, "in": tm, "fx": "pop"},
            circ(cx, cy, r, "none", ICE, 3, tm, fx="pop")]
    els += [{"k": "pin", "x": sx, "y": sy, "t": "Iseki Point", "t2": "Ruins Point", "c": GOLD, "lx": 26, "ly": 2, "in": tn}]
    return {"base": "map", "cam": CAM, "els": els}


def s7():
    """The survey (from 1992): the terraces in three-quarter view, smaller; a boat sends a sonar fan down; sonar dots land along the
    steps and join into their outline; two divers stretch a tape on the top terrace; a small robot with a lamp on the floor."""
    tf, tsn, trb = T("s7", "They mapped it"), T("s7", "sonar"), T("s7", "underwater robots")
    sea = 258
    sp = TIERS
    Tm = lambda x, y: (560 + .72 * (x - 150), 760 - .72 * (770 - y))
    els = underwater(sea, rays=True, seed=3, floor=760) + tiers(Tm, -1, "water", sp, seed=11, end=True)
    els += boat(760, sea, 150, .3) + chip(250, 200, "from 1992", AMBER, .6, 26)
    els += [{"k": "fan", "x": 760, "y": sea + 14, "a0": 70, "a1": 120, "r": 430, "c": BLUE, "in": tsn - .2}, lab(560, 400, "sonar", tsn + .3, BLUE, 28)]
    prof = []
    for k in range(5):
        prof += [tpt(sp, sp["xa"][k], sp["z"][k], sp["h"][k - 1] if k else 0), corner(sp, k)]
    prof += [tpt(sp, sp["xbs"][4], sp["z"][4], sp["h"][4])]
    pts = [Tm(x, y) for x, y in prof]
    for k, (x, y) in enumerate(pts):
        els.append(dot(x, y, 6, BLUE, round(tsn + .1 + .08 * k, 2)))
    els.append(ln(pts, tsn + 1.2, BLUE, 3, "inferred", 1.2))
    a, b = Tm(*tpt(sp, 760, 330, sp["h"][4])), Tm(*tpt(sp, 1000, 330, sp["h"][4]))
    els += diver(a[0], a[1] - 22, .32, tf, face=1, lamp=False) + diver(b[0], b[1] - 22, .32, tf + .2, face=-1, lamp=False)
    els += [ln([(a[0] + 18, a[1] - 16), (b[0] - 18, b[1] - 16)], tf + .5, GOLD, 2.5, dur=.6), lab((a[0] + b[0]) / 2, a[1] - 54, "divers", tf + .7, GOLD, 26)]
    els += [{"k": "robot", "x": 430, "y": 752, "s": 1.5, "in": trb}, gl(470, 716, 120, trb + .1, .7, "lamp"), lab(430, 690, "robot", trb + .3, BONE, 26)]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s8():
    """To scale (4 units a metre): the shore, 100 m of sea, the main mass 270 m long rising from 25 m down almost to the surface; the
    Titanic's outline (269 m) on the surface above it, the same length."""
    tm, tt = T("s8", "starts about"), T("s8", "Titanic")
    th = T("s8", "rises twenty-five")
    K, SL = 4.0, 430
    x0 = 200 + 100 * K                                       # the mass starts 100 m from the shore
    x1 = x0 + 270 * K
    base = SL + 25 * K
    prof = [(x0, base), (x0 + 30, base - 14), (x0 + 120, base - 14), (x0 + 120, base - 30), (x0 + 260, base - 30), (x0 + 260, base - 48),
            (x0 + 420, base - 48), (x0 + 420, base - 66), (x0 + 560, base - 66), (x0 + 560, base - 82), (x0 + 700, base - 82), (x0 + 700, base - 96),
            (x0 + 900, base - 96), (x0 + 960, base - 60), (x1 - 40, base - 40), (x1, base)]
    els = [poly([(-20, 120), (1800, 120), (1800, SL), (-20, SL)], "#26384a", at=-1, op=.8),
           poly([(-20, SL), (1800, SL), (1800, 820), (-20, 820)], "url(#k-water)", at=-1)]
    els += [poly([(-20, 300), (120, 304), (170, 330), (200, SL), (230, base + 30), (-20, base + 40)], "#5c4c3a", "#c9b48c", 2, -1),
            poly([(-20, base + 20), (1800, base + 4), (1800, 820), (-20, 820)], "#3b3d33", at=-1),
            surface_line(SL, 200, 1800, -1), lab(100, 280, "shore", .3, "#cbbca8", 26)]
    els += [poly(prof, "#7f8b7a", "rgba(230,240,230,.6)", 2, .2, fx="rise")]
    els += [{"k": "dim", "x1": 200, "y1": SL + 30, "x2": x0, "y2": SL + 30, "t": "100 m", "c": ICE, "in": tm, "lx": 0, "ly": 34},
            {"k": "dim", "x1": x0, "y1": base + 44, "x2": x1, "y2": base + 44, "t": "270 m", "c": GOLD, "in": tm + 1.2, "ly": 40},
            {"k": "dim", "x1": x1 + 30, "y1": SL, "x2": x1 + 30, "y2": base, "t": "25 m", "c": ICE, "in": th, "lx": -64, "upright": True}]
    hull = [(x0, SL), (x0 + 30, SL - 70), (x0 + 40, SL - 74), (x1 - 60, SL - 74), (x1 - 8, SL - 70), (x1 - 30, SL)]
    sup = [(x0 + 170, SL - 74), (x0 + 170, SL - 104), (x1 - 250, SL - 104), (x1 - 250, SL - 74)]
    els += [poly(hull, "rgba(245,236,220,.05)", BONE, 2.5, tt, style="inferred", fx="rise"), poly(sup, "none", BONE, 2, tt + .2, style="inferred", fx="rise")]
    for k in range(4):
        fx_ = x0 + 290 + k * 190
        els.append(poly([(fx_, SL - 104), (fx_ + 6, SL - 168), (fx_ + 44, SL - 168), (fx_ + 50, SL - 104)], "none", BONE, 2, round(tt + .35 + .1 * k, 2),
                        style="inferred", fx="rise"))
    els += [lab((x0 + x1) / 2, SL - 196, "Titanic, 269 m", tt + .8, BONE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s9():
    """Close on the upper terraces (the hero drawn 1.5 times larger): the treads, the walls and the trench light up; 'it looks built':
    lilac dotted joints on the risers as if they were courses of blocks."""
    tf, td, tg, tb = T("s9", "flat as a"), T("s9", "straight down"), T("s9", "like a gutter"), T("s9", "looks built")
    sp = TIERS
    K, cx, cy = 1.5, 1000, 333
    Tm = lambda x, y: (889 + (x - cx) * K, 500 + (y - cy) * K)
    els = underwater(Tm(0, 122)[1], rays=True, seed=9) + [poly([Tm(x, y) for x, y in q["p"]], q["fill"], q.get("c", "none"), q.get("w", 0), -1) for q in far_ridge()]
    els += tiers(Tm, -1, "water", sp, seed=5, end=True)
    els += tread_edges(Tm, tf, GOLD, 5, .2, (2, 3, 4)) + wall_edges(Tm, td, GOLD, 5, .2, (2, 3, 4))
    x, k = sp["slot"], 4
    q = [tpt(sp, x - 4, sp["z"][k], sp["h"][k]), tpt(sp, x + 28, sp["z"][k], sp["h"][k]), tpt(sp, x + 28, sp["Z"], sp["h"][k]), tpt(sp, x - 4, sp["Z"], sp["h"][k])]
    els += [poly([Tm(*p_) for p_ in q], "none", AMBER, 4, tg, fx="draw"), gl(*Tm(*tpt(sp, x + 12, 350, sp["h"][k])), 130, tg, .5, "lamp"),
            lab(*Tm(1300, 150), "a trench", tg + .2, AMBER, 30, "end")]
    for k in (2, 3, 4):
        lo = sp["h"][k - 1]
        for j in range(5):
            xx = sp["xa"][k] + 90 + j * 110
            if xx < sp["xbs"][k] - 30:
                els.append(ln([Tm(*tpt(sp, xx, sp["z"][k], sp["h"][k] - 3)), Tm(*tpt(sp, xx, sp["z"][k], lo + 3))], round(tb + .05 * j, 2), LILAC, 2.5, "claimed", .3))
    els += [lab(*Tm(560, 470), "built?", tb + .4, LILAC, 34, st="ital")]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s10():
    """A balance, level: a lilac dotted monument against rock and sea."""
    tk, tg = T("s10", "Kimura would"), T("s10", "Other geologists")

    def mono(x, y):
        out = []
        for j in range(4):
            w = 150 - j * 34
            out.append(rect(x - w / 2, y - 26 * (j + 1), w, 26, "rgba(201,193,238,.08)", LILAC, 2.5, 2, tk + .3 + .1 * j, style="claimed"))
        return out

    def nat(x, y):
        out = [rect(x - 80, y - 90, 160, 90, FRONTW, EDGEW, 1.5, 3, tg)]
        out += [ln([(x - 78, y - 90 + 22 * j), (x + 78, y - 90 + 22 * j)], tg + .1, "rgba(20,24,20,.45)", 1.6, draw=False) for j in (1, 2, 3)]
        out += [ln([(x - 30, y - 90), (x - 28, y)], tg + .2, "rgba(10,14,12,.7)", 2.4, dur=.3), ln([(x + 36, y - 90), (x + 34, y)], tg + .3, "rgba(10,14,12,.7)", 2.4, dur=.3)]
        out += [ln([[x - 90 + 12 * j, y - 112 - 6 * (j % 2)] for j in range(16)], tg + .5, FOAM, 3, curve=True, dur=.6)]
        return out
    els = [gl(889, 420, 600, .1, .2, "lamp")] + balance(889, 300, 760, 700, .2, mono, nat, drop=210, pan=260)
    els += [lab(509, 640, "Kimura: a monument", tk + .6, LILAC, 30), lab(1269, 640, "others: rock and sea", tg + .7, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 2 · The case for a monument
def hill_rings():
    """The main hill from above, schematic: five nested terraces, elongated east to west (270 by 120 m), the top towards the east."""
    rings = []
    for k in range(5):
        cx, cy = 820 + 70 * k, 440 - 6 * k
        rx, ry = 560 - 92 * k, 230 - 34 * k
        pts = []
        for j in range(16):
            a = 2 * math.pi * j / 16
            ca, sa = math.cos(a), math.sin(a)
            # squarish (superellipse), with a slight wobble: terraces, not a perfect shape
            px = cx + rx * (abs(ca) ** .35) * (1 if ca >= 0 else -1) * (1 + .03 * math.sin(3 * a + k))
            py = cy + ry * (abs(sa) ** .35) * (1 if sa >= 0 else -1) * (1 + .03 * math.cos(2 * a + k))
            pts.append((px, py))
        rings.append(pts)
    return rings


def s11():
    """Kimura's reading of the main hill, in plan (schematic): nested terraces; a ring road with blocks set aside, walls, a gate with
    paving, a drainage channel, all lilac dotted (claimed)."""
    tr, tw, tg, tc = T("s11", "ring road"), T("s11", "Retaining walls"), T("s11", "A gate"), T("s11", "drainage channel")
    rings = hill_rings()
    shades = ["#6c6a55", "#7d7a60", "#8f8a6c", "#a09a78", "#b3ab86"]
    els = [poly(r, shades[k], "rgba(240,236,220,.35)", 1.5, .2 + .12 * k, fx="pop") for k, r in enumerate(rings)]
    # the ring road: a dotted loop just outside the base, blocks along its outer edge
    road = [(820 + 610 * math.cos(2 * math.pi * j / 40), 440 + 268 * math.sin(2 * math.pi * j / 40)) for j in range(40)]
    els.append(poly(road, "none", LILAC, 5, tr, style="claimed", fx="draw", dur=1.4))
    rnd = random.Random(6)
    for j in range(0, 40, 3):
        a = 2 * math.pi * j / 40
        x, y = 820 + 650 * math.cos(a), 440 + 296 * math.sin(a)
        if 120 < y < 770 and 110 < x < 1670:
            els.append(rect(x - 11, y - 9, 22, 18, "rgba(201,193,238,.15)", LILAC, 2, 3, round(tr + .8 + .04 * j, 2), fx="pop", style="claimed"))
    els += [lab(1460, 182, "ring road", tr + .6, LILAC, 30, st="ital")]
    for k, (a0, a1) in enumerate(((200, 235), (300, 330), (20, 50))):
        pts = [(820 + 70 + 470 * math.cos(math.radians(a)), 434 + 196 * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 5)]
        els.append(ln(pts, tw + .2 * k, LILAC, 9, "claimed", .5, curve=True))
    els += [lab(330, 300, "walls", tw + .5, LILAC, 30, st="ital")]
    gx, gy = 820, 440 + 268
    els += [rect(gx - 50, gy - 26, 18, 40, "rgba(201,193,238,.2)", LILAC, 2, 2, tg, fx="pop", style="claimed"),
            rect(gx + 32, gy - 26, 18, 40, "rgba(201,193,238,.2)", LILAC, 2, 2, tg + .1, fx="pop", style="claimed")]
    els += [rect(gx - 60 + 30 * (j % 4), gy + 24 + 26 * (j // 4), 24, 20, "rgba(201,193,238,.12)", LILAC, 1.5, 2, round(tg + .3 + .05 * j, 2), fx="pop", style="claimed")
            for j in range(8)]
    els += [lab(gx + 150, gy + 30, "gate", tg + .5, LILAC, 30, "start", st="ital")]
    ch = [(1090, 300), (1190, 330), (1300, 360), (1400, 392)]
    els += [ln(ch, tc, LILAC, 7, "claimed", .8), lab(1450, 440, "channel", tc + .4, LILAC, 30, "start", st="ital")]
    els += [lab(140, 770, "after Kimura, schematic", .4, DIM, 24, "start")]
    return {"base": "plan", "bg": "#1e2a30", "cam": CAM, "els": els}


def corner_block(x, y, w, h, d, at, c_top=TOPW, c_front=FRONTW, c_side=SIDEW, edge=EDGEW, beds=3):
    """A block in three-quarter view: front face (x..x+w, y-h..y), top and right faces receding by d."""
    dx, dy = d, -d * .45
    out = [poly([(x, y - h), (x + w, y - h), (x + w + dx, y - h + dy), (x + dx, y - h + dy)], c_top, edge, 1.2, at),
           poly([(x + w, y - h), (x + w + dx, y - h + dy), (x + w + dx, y + dy), (x + w, y)], c_side, edge, 1.2, at),
           poly([(x, y - h), (x + w, y - h), (x + w, y), (x, y)], c_front, edge, 1.2, at)]
    for j in range(1, beds + 1):
        yy = y - h + h * j / (beds + 1)
        out.append(ln([(x + 2, yy), (x + w - 2, yy)], at, "rgba(20,24,20,.35)", 1.6, draw=False))
    return out


def s12():
    """Left: a step corner with three dents ringed lilac (read as wedge and lever marks). Right, drawn solid as an illustration of the
    method: a quarry block with a row of wedge slots, a worker with a hammer, the split running along the row."""
    tdn, tw, tq = T("s12", "pointed to dents"), T("s12", "wedges"), T("s12", "quarry workers")
    els = underwater(122, rays=False, seed=12, dark=.45)
    els += corner_block(170, 690, 470, 380, 160, -1)
    for k, (x, y) in enumerate(((618, 340), (600, 420), (624, 500))):
        els += [poly(E(x, y, 10, 7, 14), "#232a28", at=-1), circ(x, y, 26, "none", LILAC, 3, round(tdn + .25 * k, 2), style="claimed", fx="pop")]
    els += [lab(500, 230, "dents?", tdn + .8, LILAC, 32, st="ital")]
    els += [ln([(889, 160), (889, 760)], .2, "rgba(255,236,206,.18)", 2, draw=False)]
    bx, by, bw, bh = 1030, 690, 520, 300
    els += [rect(950, 140, 790, 660, "rgba(30,24,18,.86)", at=-1, r=18)]
    els += corner_block(bx, by, bw, bh, 120, .8, "#cdbb95", "#a88a62", "#7b6449", EDGED, beds=0)
    for k in range(5):
        x = bx + 70 + k * 95
        els.append(poly([(x - 14, by - bh), (x + 14, by - bh), (x + 6, by - bh + 40), (x - 6, by - bh + 40)], "#3a2a1c", at=round(tw + .15 * k, 2), fx="pop"))
    els += [ln([(bx + 70 + k * 95, by - bh + 40) for k in range(5)] + [(bx + bw, by - bh + 52)], tq, "#2a1c10", 3, dur=1.0),
            person(bx + 150, by - bh - 2, 120, tq - .3, SKIN),
            ln([(bx + 168, by - bh - 80), (bx + 230, by - bh - 118)], tq - .1, WOOD, 6, draw=False),
            rect(bx + 216, by - bh - 134, 34, 22, "#8a8580", at=tq - .1, r=3),
            lab(1345, 770, "how wedges split stone", tq + .4, BONE, 28)]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def animal(x, y, s, at, c=LILAC):
    P = lambda a, b: (x + a * s, y + b * s)
    body = [P(-.5, -.1), P(-.2, -.3), P(.3, -.28), P(.5, -.4), P(.62, -.36), P(.56, -.2), P(.4, -.08), P(.3, .2), P(.2, .2), P(.18, 0),
            P(-.25, 0), P(-.3, .2), P(-.4, .2), P(-.42, -.02)]
    return [poly(body, "none", c, 2.5, at, style="claimed", curve=True)]


def s13():
    """The reported finds, lilac dotted (reported, not published): an incised slab; the 1994 typhoon; a round stone, 70 cm across, carved
    with an animal."""
    ts, tt, tr, ta = T("s13", "stone slab"), T("s13", "typhoon"), T("s13", "round stone"), T("s13", "carved with")
    els = [gl(889, 430, 620, .1, .18, "lamp")]
    els += [poly([(200, 260), (560, 236), (600, 560), (240, 590)], "rgba(201,193,238,.06)", LILAC, 3, ts, style="claimed", fx="pop")]
    rnd = random.Random(3)
    for k in range(9):
        y = 300 + 30 * k
        x0 = 250 + rnd.uniform(0, 30)
        els.append(ln([(x0, y), (x0 + rnd.uniform(140, 260), y + rnd.uniform(-8, 8))], round(ts + .3 + .08 * k, 2), LILAC, 2, "claimed", .3))
    els += [lab(400, 650, "incised slab", ts + .6, LILAC, 30, st="ital")]
    sp = []
    for j in range(60):
        a = j * .32
        r = 6 + j * 1.25
        sp.append((880 + r * math.cos(a), 370 + r * math.sin(a)))
    els += [ln(sp, tt, ICE, 3, dur=1.0, curve=True)] + chip(880, 520, "1994", AMBER, tt + .5, 28)
    cx, cy, r = 1360, 410, 150
    els += [circ(cx, cy, r, "rgba(201,193,238,.06)", LILAC, 3, tr, style="claimed", fx="pop")] + animal(cx, cy + 10, 200, ta)
    els += [{"k": "dim", "x1": cx - r, "y1": cy + r + 30, "x2": cx + r, "y2": cy + r + 30, "t": "70 cm", "c": DIM, "in": tr + .4, "ly": 40},
            lab(cx, 690, "carved stone", ta + .5, LILAC, 30, st="ital")]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s14():
    """Further out: a stadium and a turtle (small, lilac dotted, as named); a rock about 7 m tall (50 units a metre) beside a 1.8 m diver;
    a face drawn over its side in lilac dots, and a feathered hat over its top."""
    ts, ttu, tr, tf, tk = T("s14", "stadium"), T("s14", "giant turtle"), T("s14", "about seven"), T("s14", "human face"), T("s14", "feathered hat")
    base = 760
    els = underwater(122, seed=14, floor=base)
    rk = [(722, base), (712, 650), (688, 606), (704, 588), (700, 544), (672, 522), (698, 494), (704, 474), (686, 446), (716, 422), (770, 410), (900, 404),
          (958, 424), (984, 520), (1000, 640), (1016, base)]
    els += [poly(rk, "#55605a", "rgba(220,238,230,.34)", 1.5, -1), poly([(900, 404), (958, 424), (984, 520), (1000, 640), (1016, base), (960, base), (930, 560), (910, 440)],
                                                                            "#3f4a48", at=-1, op=.85)]
    els += [ln([(716 + 3 * j, 470 + 48 * j), (930 - 2 * j, 466 + 48 * j)], -1, "rgba(18,24,22,.36)", 1.6, draw=False) for j in range(6)]
    rnd = random.Random(14)
    els += [poly(E(rnd.uniform(740, 940), rnd.uniform(430, 740), rnd.uniform(10, 26), rnd.uniform(4, 9), 10), rnd.choice(["#c58a96", "#7f9a66", "#2a3432"]), at=-1, op=.55)
            for _ in range(14)]
    els += [{"k": "dim", "x1": 1060, "y1": base, "x2": 1060, "y2": base - 350, "t": "7 m", "c": ICE, "in": tr, "lx": 36, "upright": True}]
    els += diver(1190, base - 200, .6, tr + .3, face=-1)
    face = [(716, 424), (690, 446), (708, 474), (698, 494), (668, 522), (700, 546), (704, 588), (686, 606), (712, 650)]
    els += [ln(face, tf, LILAC, 4, "claimed", 1.0, curve=True), poly(E(722, 478, 13, 7, 12), "none", LILAC, 3, tf + .5, style="claimed"),
            lab(560, 470, "a face?", tf + .7, LILAC, 32, st="ital")]
    hat = [(716, 420), (740, 360), (770, 404), (800, 340), (830, 402), (860, 330), (890, 400), (920, 350), (950, 418)]
    els += [ln(hat, tk, LILAC, 3, "claimed", .8), lab(840, 300, "a feathered hat?", tk + .4, LILAC, 28, st="ital")]
    st_ = [poly(E(330, 620 - 22 * j, 150 - 26 * j, 50 - 8 * j, 24), "rgba(201,193,238,.05)", LILAC, 2.5, round(ts + .12 * j, 2), style="claimed") for j in range(4)]
    els += st_ + [lab(330, 500, "stadium?", ts + .5, LILAC, 28, st="ital")]
    tu = [poly(E(1500, 650, 140, 70, 28), "rgba(201,193,238,.05)", LILAC, 3, ttu, style="claimed"), poly(E(1660, 640, 34, 24, 16), "none", LILAC, 2.5, ttu + .1, style="claimed"),
          ln([(1440, 610), (1500, 585), (1560, 610)], ttu + .2, LILAC, 2, "claimed", .3), ln([(1460, 660), (1540, 660)], ttu + .2, LILAC, 2, "claimed", .3)]
    els += tu + [lab(1500, 550, "turtle?", ttu + .5, LILAC, 28, st="ital")]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s15():
    """Left: the formation cut open, its layers unbroken from end to end: one piece of bedrock. Right: rock-cut monuments, Petra and Ellora."""
    tb, tp, te = T("s15", "one solid piece"), T("s15", "Petra"), T("s15", "Ellora")
    prof = [(120, 700), (120, 610), (220, 610), (220, 520), (330, 520), (330, 430), (440, 430), (440, 340), (560, 340), (640, 360), (700, 700)]
    els = [poly(prof, FRONTW, EDGEW, 1.5, -1)]
    for j in range(1, 13):
        y = 340 + 30 * j
        xs = [x for x, yy in [(120, 610), (220, 520), (330, 430), (440, 340)] if yy <= y] or [440]
        els.append(ln([(min(xs) + 2, y), (680 if y > 380 else 600 + (y - 340) * .4, y)], tb + .05 * j, GOLD, 2, dur=.6, op=.8))
    els += [lab(410, 760, "one piece of bedrock", tb + .8, GOLD, 30)]
    els += [ln([(889, 160), (889, 760)], .2, "rgba(255,236,206,.18)", 2, draw=False)]
    # Petra: a facade carved into a rose cliff
    els += [poly([(960, 760), (960, 220), (1010, 180), (1250, 170), (1300, 230), (1300, 760)], "#a4604a", "#e2a888", 1.5, tp - .3)]
    fx0 = 1030
    els += [rect(fx0, 330, 200, 300, "#b8705a", "#f0c0a0", 1.5, 2, tp, fx="rise")]
    els += [rect(fx0 + 14 + 44 * k, 400, 16, 230, "#cf8a72", at=round(tp + .1 + .05 * k, 2), fx="rise") for k in range(5)]
    els += [poly([(fx0 - 6, 400), (fx0 + 100, 350), (fx0 + 206, 400)], "#cf8a72", "#f0c0a0", 1.5, tp + .4, fx="pop"),
            rect(fx0 + 85, 250, 30, 90, "#cf8a72", at=tp + .5, fx="rise"), rect(fx0 + 85, 560, 30, 70, "#3a1e16", at=tp + .5),
            lab(1130, 780, "Petra, Jordan", tp + .6, "#f0c0a0", 28)]
    # Ellora: a temple standing in its own pit, cut down into the hill
    els += [poly([(1340, 760), (1340, 300), (1720, 300), (1720, 760)], "#5e5248", "#b8a894", 1.5, te - .3),
            rect(1380, 340, 300, 420, "#2c2622", at=te - .2)]
    els += [poly([(1430, 760), (1430, 560), (1470, 520), (1530, 400), (1590, 520), (1630, 560), (1630, 760)], "#8a7b6a", "#d8c8b0", 1.5, te, fx="rise"),
            rect(1450, 600, 160, 160, "#7a6b5a", at=te + .1, fx="rise"), lab(1530, 780, "Ellora, India", te + .4, "#d8c8b0", 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s16():
    """Left: an old Okinawan stone castle on its hill: walls of fitted stone following the hilltop, upturned corners, an arched gate,
    an inner wall above. Right: the terraces with a lilac dotted wall traced along their edges. Then a paper notice with a red seal."""
    tc, tn = T("s16", "old stone castles"), T("s16", "nineteen ninety-eight")
    hill = [(40, 780), (130, 700), (230, 640), (360, 604), (520, 596), (660, 620), (780, 690), (880, 780)]
    els = [poly(hill, "#46563a", "#9fb070", 1.5, -1, curve=True)]
    hs_ = lambda x: 604 - 8 * math.sin(math.pi * (x - 200) / 560) if 200 <= x <= 760 else 640
    lo = [(x, hs_(x) + (x - 480) ** 2 / 4200) for x in range(200, 761, 20)]
    hi = [(x, y - 92) for x, y in lo]
    hi[0] = (hi[0][0] - 8, hi[0][1] - 18); hi[-1] = (hi[-1][0] + 8, hi[-1][1] - 18)        # the upturned corners
    els += [poly(lo + hi[::-1], "url(#k-blocks)", "rgba(255,236,206,.6)", 1.5, tc, fx="rise"), ln(hi, tc + .2, "#f0e0c0", 3, dur=.8)]
    lo2 = [(x, y - 120) for x, y in lo[6:-6]]
    hi2 = [(x, y - 70) for x, y in lo2]
    els += [poly(lo2 + hi2[::-1], "url(#k-blocks)", "rgba(255,236,206,.5)", 1.2, tc + .2, fx="rise", op=.85)]
    gx, gy = 480, lo[14][1]
    els += [poly([(gx - 28, gy), (gx - 28, gy - 46), (gx - 16, gy - 62), (gx, gy - 68), (gx + 16, gy - 62), (gx + 28, gy - 46), (gx + 28, gy)], "#1e1812", at=tc + .4, fx="pop"),
            lab(480, 330, "Okinawan castle", tc + .5, BONE, 30)]
    sp = TIERS
    Tm = lambda x, y: (940 + (x - 150) * .5, 720 - (770 - y) * .5)
    els += tiers(Tm, -1, "water", sp, seed=16, end=True, fallen=False)
    for i, k in enumerate(range(5)):
        els.append(ln([Tm(*tpt(sp, sp["xa"][k] + 6, sp["z"][k], sp["h"][k] + 14)), Tm(*tpt(sp, sp["xbs"][k] - 6, sp["z"][k], sp["h"][k] + 14))],
                      round(tc + 1.0 + .15 * i, 2), LILAC, 6, "claimed", .4))
    els += [lab(1290, 290, "a castle?", tc + 1.6, LILAC, 32, st="ital")]
    els += [rect(1300, 560, 260, 170, "#efe6d2", "#8a7a66", 2, 6, tn, fx="pop")]
    els += [ln([(1326, 594 + 24 * j), (1326 + 150 + 40 * (j % 2), 594 + 24 * j)], tn + .2, "#8a7a66", 3, draw=False) for j in range(4)]
    els += [circ(1514, 694, 26, "#c0392b", "#7a1a10", 2, tn + .4, fx="pop"), lab(1430, 780, "1998: filed as a site", tn + .5, BONE, 28)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · Flat layers, straight cracks
def s17():
    """An ancient sea floor: sand and mud from the Asian mainland settle layer on layer (they fill from the bottom); 15 to 20 million
    years ago. Right: the stack lifted above a new sea line."""
    t0, tl = T("s17", "sandstone and mudstone"), T("s17", "pushed up")
    tm = T("s17", "Asian mainland")
    els = [poly([(-20, 130), (980, 130), (980, 760), (-20, 760)], "url(#k-water)", at=-1), surface_line(140, -20, 980)]
    cols = ["#d4c08e", "#6f6150"] * 4
    y = 760
    for k in range(8):
        h = 44 if k % 2 == 0 else 26
        els.append(rect(80, y - h, 860, h, cols[k], "rgba(255,236,206,.25)", 1, 0, round(t0 + .35 * k, 2), fx="fill", dur=.5))
        y -= h
    els += [lab(990, 676, "sandstone", t0 + 1.0, "#e8d8b0", 26, "start"), lab(990, 712, "mudstone", t0 + .6, "#cbbca8", 26, "start")]
    els += [arr([(40, 260), (300, 320), (560, 380)], tm, AMBER, 4, dur=1.0), lab(60, 230, "from the Asian mainland", tm + .3, AMBER, 26, "start")]
    rnd = random.Random(8)
    els += [dot(round(rnd.uniform(200, 900), 1), round(rnd.uniform(300, 420), 1), 3, "#e8d8b0", round(tm + .5 + .05 * k, 2), op=.8) for k in range(24)]
    els += chip(510, 430, "15 to 20 million years ago", GOLD, t0 + 2.6, 26)
    # lifted
    els += [poly([(1120, 650), (1680, 650), (1680, 760), (1120, 760)], "url(#k-water)", at=tl), surface_line(650, 1120, 1680, tl)]
    yy = 600
    for k in range(8):
        h = 30 if k % 2 == 0 else 18
        els.append(rect(1200, yy - h, 400, h, cols[k], "rgba(255,236,206,.25)", 1, 0, round(tl + .2, 2), fx="rise"))
        yy -= h
    els += [arr([(1400, 740), (1400, 640)], tl + .3, GOLD, 5, dur=.6, curve=False), lab(1400, 340, "lifted", tl + .6, GOLD, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


C30 = math.cos(math.pi / 6)


def P3(e, p, t=0.0):
    """Where a world point (x, y, z) of an iso element lands on the panel at local time t."""
    az = math.radians(e.get("az", 35) + e.get("spin", 0) * t)
    ca, sa = math.cos(az), math.sin(az)
    x, y, z = p
    rx, rz = x * ca - z * sa, x * sa + z * ca
    S, el = e["s"], e.get("el", .32)
    return [round(e["x"] + (rx - rz) * C30 * S, 1), round(e["y"] - y * S + (rx + rz) * el * S, 1)]


def ibox(x, z, y, w, d, h, c, e="rgba(0,0,0,.3)", **kw):
    b = {"t": "box", "x": x, "z": z, "y": y, "w": w, "d": d, "h": h, "c": c, "edge": e}
    b.update(kw)
    return b


def slab_items(w=12, d=7, layers=6, lh=.55, cols=("#cdbb95", "#7a6b58")):
    items, y = [], 0
    for k in range(layers):
        items.append(ibox(0, 0, y, w, d, lh, cols[k % 2], "rgba(30,20,10,.35)"))
        y += lh
    top = y
    jc = "#1e1610"
    for x in (-3.6, -1.2, 1.2, 3.6):                       # joints along z (and down the front and the back)
        items += [{"t": "line", "p": [[x, top, -d / 2], [x, top, d / 2]], "c": jc, "w": 2.6}, {"t": "line", "p": [[x, 0, d / 2], [x, top, d / 2]], "c": jc, "w": 2.6}]
    for z in (-1.75, 1.75):                                # the cross set, along x (and down the right face)
        items += [{"t": "line", "p": [[-w / 2, top, z], [w / 2, top, z]], "c": jc, "w": 2.6}, {"t": "line", "p": [[w / 2, 0, z], [w / 2, top, z]], "c": jc, "w": 2.6}]
    return items, top


def s18():
    """Iso model, slowly turning: a slab of the rock, sandstone and mudstone layers, cut by two sets of joints at right angles."""
    tl, tj = T("s18", "flat layers"), T("s18", "joints")
    items, top = slab_items()
    iso_ = {"k": "iso", "x": 889, "y": 560, "s": 64, "az": -32, "spin": .5, "el": .32, "items": items, "in": -1}
    t = tl
    fp = P3(iso_, (-6, 1.6, 3.5), t)
    jp = P3(iso_, (1.2, top, 0), tj)
    ra = P3(iso_, (1.2, top, 1.75), tj)
    els = [gl(889, 520, 560, .1, .2, "lamp"), iso_,
           ln([(fp[0] - 10, fp[1]), (fp[0] - 150, fp[1] + 90)], tl, GOLD, 2, dur=.4), lab(fp[0] - 160, fp[1] + 126, "flat layers", tl + .2, GOLD, 30, "end"),
           ln([(jp[0], jp[1] - 6), (jp[0] + 120, jp[1] - 170)], tj, GOLD, 2, dur=.4), lab(jp[0] + 130, jp[1] - 186, "joints", tj + .2, GOLD, 32, "start"),
           circ(ra[0], ra[1], 16, "none", GOLD, 3, tj + .8, fx="pop"), lab(ra[0] + 26, ra[1] + 50, "right angles", tj + 1.0, GOLD, 26, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def paper_items(cols, rows, heights, sz=1.6, sheet=.12, white="#efe9dc"):
    """Columns of stacked paper (a grid cols x rows of blocks sz wide), each with its own height; sheet edges as lines."""
    items = []
    x0, z0 = -cols * sz / 2 + sz / 2, -rows * sz / 2 + sz / 2
    for i in range(cols):
        for j in range(rows):
            h = heights[i][j]
            if h <= 0:
                continue
            x, z = x0 + i * sz, z0 + j * sz
            items.append(ibox(x, z, 0, sz, sz, h, white, "rgba(60,50,40,.55)"))
    return items


def s19():
    """Two iso models of paper: a thick stack cut in a grid; the same stack with blocks lifted out: a staircase."""
    tp, tl = T("s19", "stack of paper"), T("s19", "Lift out")
    ttr, tsw, tra = T("s19", "flat treads"), T("s19", "sheer walls"), T("s19", "right angles")
    full = [[3.2] * 3 for _ in range(4)]
    step = [[0.8, 0.8, 0.8], [1.6, 1.6, 1.6], [2.4, 2.4, 2.4], [3.2, 3.2, 3.2]]
    a = {"k": "iso", "x": 470, "y": 580, "s": 62, "az": -30, "spin": 0, "el": .32, "items": paper_items(4, 3, full), "in": tp, "fx": "rise"}
    b = {"k": "iso", "x": 1300, "y": 580, "s": 62, "az": -30, "spin": 0, "el": .32, "items": paper_items(4, 3, step), "in": tl, "fx": "rise"}
    els = [gl(889, 520, 640, .1, .2, "lamp"), a, b]
    for k in range(1, 16):                                   # sheet lines on the full stack's front, faint
        y = k * .2
        els.append(ln([P3(a, (-3.2, y, 2.4)), P3(a, (3.2, y, 2.4))], tp + .05, "rgba(90,80,70,.35)", 1, draw=False))
    for i in (-1.6, 0, 1.6):                                 # the knife's grid on top of the full stack
        els.append(ln([P3(a, (i, 3.2, -2.4)), P3(a, (i, 3.2, 2.4)), P3(a, (i, 0, 2.4))], tp + .8, RED, 2.5, dur=.6))
    for j in (-.8, .8):
        els.append(ln([P3(a, (-3.2, 3.2, j)), P3(a, (3.2, 3.2, j)), P3(a, (3.2, 0, j))], tp + 1.2, RED, 2.5, dur=.6))
    els += [arr([(800, 250), (1000, 250)], tl - .2, AMBER, 4, dur=.6, curve=False), lab(900, 226, "lift out", tl, AMBER, 26)]
    q1, q2, q3 = P3(b, (-2.4, .8, 0)), P3(b, (-.8, 1.2, 2.4)), P3(b, (0, 2.4, 2.4))
    els += [lab(q1[0] - 60, q1[1] - 110, "flat treads", ttr, GOLD, 30, "end"), ln([(q1[0] - 56, q1[1] - 100), (q1[0], q1[1])], ttr, GOLD, 2, dur=.3),
            lab(q2[0] - 30, q2[1] + 150, "sheer walls", tsw, GOLD, 30, "end"), ln([(q2[0] - 40, q2[1] + 120), (q2[0], q2[1] + 10)], tsw, GOLD, 2, dur=.3),
            circ(q3[0], q3[1], 16, "none", GOLD, 3, tra, fx="pop"), lab(q3[0] + 30, q3[1] - 196, "right angles", tra + .2, GOLD, 30, "start"),
            ln([(q3[0] + 30, q3[1] - 186), (q3[0] + 8, q3[1] - 14)], tra + .2, GOLD, 2, dur=.3)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s20():
    """A stepped rocky coast in section, layers and joints: waves hit the face; a block between two joints loosens and lies tumbled at the
    foot; the soft mudstone is cut back under the sandstone above it."""
    tw, tb, tt, tm = T("s20", "the waves"), T("s20", "pry loose"), T("s20", "tumble them"), T("s20", "softer mudstone")
    SL = 330
    els = [poly([(-20, 120), (1800, 120), (1800, SL), (-20, SL)], "#2c3c4c", at=-1),
           poly([(-20, SL), (1800, SL), (1800, 820), (-20, 820)], "url(#k-water)", at=-1), surface_line(SL)]
    steps = [(1700, 200), (1300, 200), (1300, 330), (1040, 330), (1040, 460), (780, 460), (780, 590), (520, 590), (520, 720), (200, 720), (200, 800)]
    body = steps + [(1800, 800), (1800, 200)]
    els += [poly(body, "#9a8a68", "rgba(255,236,206,.4)", 1.5, -1)]
    for y in range(230, 800, 26):                         # alternating beds: sandstone (pale) and mudstone (dark) bands
        xs = [x for x, yy in [(1300, 200), (1040, 330), (780, 460), (520, 590), (200, 720)] if yy <= y]
        x0 = min(xs) if xs else 1300
        if (y // 26) % 2:
            els.append(rect(x0, y, 1800 - x0, 13, "#6c5e4c", at=-1, op=.85))
    for x in (1160, 900, 650, 380, 1500):                 # joints
        yt = min(yy for xx, yy in [(1300, 200), (1040, 330), (780, 460), (520, 590), (200, 720)] if xx <= x + 1)
        els.append(ln([(x, yt), (x, 800)], -1, "#2a2016", 2.5, draw=False))
    # waves
    for k in range(3):
        y = SL + 60 + 60 * k
        els.append(arr([(240 + 30 * k, y + 120), (440 + 20 * k, y + 60), (500 + 10 * k, y + 10)], round(tw + .2 * k, 2), FOAM, 4, dur=.5))
    els += [lab(300, 420, "waves", tw + .4, FOAM, 30)]
    # the block between two joints: outlined, then tumbled at the foot
    els += [rect(650, 460, 130, 64, "none", AMBER, 4, 0, tb, style="inferred", fx="draw"),
            arr([(720, 520), (640, 650), (420, 750)], tt, AMBER, 3, "inferred", .8)]
    q = [(330, 770), (450, 740), (470, 790), (350, 812)]
    els += [poly(q, "#9a8a68", "rgba(255,236,206,.5)", 1.5, tt + .6, fx="pop"),
            poly([(250, 790), (300, 776), (312, 806), (262, 816)], "#9a8a68", "rgba(255,236,206,.5)", 1.5, tt + .7, fx="pop"),
            lab(380, 700, "fallen blocks", tt + .9, AMBER, 28)]
    # undercut: the mudstone notch under a sandstone ledge
    els += [poly([(1040, 330 + 26), (996, 330 + 32), (996, 330 + 52), (1040, 330 + 58)], "#0e2430", "rgba(255,236,206,.5)", 1.5, tm, fx="pop"),
            poly([(1300, 200 + 52), (1256, 200 + 58), (1256, 200 + 78), (1300, 200 + 84)], "#0e2430", "rgba(255,236,206,.5)", 1.5, tm + .2, fx="pop"),
            ln([(972, 396), (998, 380)], tm + .4, "#cbbca8", 2, dur=.3),
            lab(966, 414, "mudstone wears faster", tm + .4, "#cbbca8", 28, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


COAST = {"xa": [80, 240, 360, 520, 640, 800], "z": [0, 50, 110, 160, 220, 270], "h": [70, 140, 230, 290, 370, 430], "Z": 380, "xb": 2200, "fl": 790,
         "kx": .9, "ky": -.5, "joints": [190, 330, 470, 610, 760, 930, 1120, 1300], "slot": None,
         "blocks": [(30, 0, -14, 70, 36, -14), (60, 20, -18, 46, 26, 10), (160, 10, 70, 44, 24, 8)]}


def s21():
    """The south-east coast of Yonaguni in daylight: sandstone stepping down to the sea in ledges and sheer walls, layered and cracked,
    grass and shrubs on top, surf at the foot, a person on a ledge (1.7 m)."""
    tc = T("s21", "south-east coast")
    sp = COAST
    els = [poly([(-20, 744), (1800, 744), (1800, 1040), (-20, 1040)], "#3f7f9c", at=-1), surface_line(744, -20, 1800, -1, FOAM, 3, .9)]
    els += tiers(ID, -1, "dry", sp, seed=21)
    rnd = random.Random(21)
    for k in range(18):                                      # shrubs along the top
        x = rnd.uniform(900, 1780)
        gx, gy = tpt(sp, x - 60, rnd.uniform(300, 370), sp["h"][-1])
        r = rnd.uniform(14, 28)
        els.append(poly(E(gx, gy - r * .5, r, r * .6, 12), rnd.choice(["#4a6a3a", "#3e5a30", "#5a7a44"]), at=-1, curve=True))
    for k in range(7):                                       # surf at the foot
        x = 40 + 70 * k
        els.append(ln([(x, 742), (x + 30, 730), (x + 60, 742)], -1, "rgba(255,255,255,.75)", 3, draw=False, curve=True))
    px, py = tpt(sp, 700, 190, sp["h"][3])
    els += [person(px, py, 44, -1, "#2a2016", None)]
    els += [lab(1300, 160, "Yonaguni, south-east coast", tc, BONE, 30)]
    return {"base": "sky", "tod": "day", "sun": [1560, 150, 30], "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s22_add():
    """The citation: the coast's bedding and its straight cracks trace in gold; a round seal, Natural Monument 2024; the name, Sanninudai."""
    tn, tr = T("s22", "national natural monument"), T("s22", "The citation")
    sp = COAST
    els = []
    for i, k in enumerate(range(1, 6)):
        lo = sp["h"][k - 1]
        hh = (lo + sp["h"][k]) / 2
        els.append(ln([tpt(sp, sp["xa"][k] + 8, sp["z"][k], hh), tpt(sp, 1600, sp["z"][k], hh)], round(tr + .12 * i, 2), GOLD, 2.5, dur=.5))
    for i, x in enumerate((610, 760, 930, 1120)):
        k = max(j for j in range(6) if sp["xa"][j] <= x)
        els.append(ln([tpt(sp, x, sp["z"][k], sp["h"][k]), tpt(sp, x, sp["z"][k], sp["h"][k - 1] if k else 0)], round(tr + .8 + .1 * i, 2), GOLD, 3, dur=.4))
    els += [circ(260, 330, 92, "rgba(120,20,14,.85)", "#f2c98e", 4, tn, fx="pop"), circ(260, 330, 76, "none", "#f2c98e", 2, tn + .1, fx="pop"),
            lab(260, 322, "Natural", tn + .2, "#f2c98e", 26), lab(260, 352, "Monument", tn + .2, "#f2c98e", 26), lab(260, 386, "2024", tn + .3, "#f2c98e", 24),
            lab(260, 478, "Sanninudai", tn + .5, BONE, 32, st="serif")]
    return els


def rock_face(x0, y0, x1, y1, at, seed, top=None):
    """A natural face of the rock under water: an uneven top edge, wavy bedding, joints, crusts and stains."""
    rnd = random.Random(seed)
    tp = top or [(x, y0 + rnd.uniform(-8, 8)) for x in range(int(x0), int(x1) + 1, 60)]
    els = [poly(tp + [(x1, y1), (x0, y1)], "#55605a", "rgba(220,238,230,.34)", 1.5, at)]
    for y in range(int(y0) + 40, int(y1), 44):
        els.append(ln([(x, y + rnd.uniform(-2.5, 2.5)) for x in range(int(x0) + 4, int(x1), 70)], at, "rgba(18,24,22,.34)", rnd.choice((1.3, 1.8)), draw=False))
    for x in range(int(x0) + 140, int(x1) - 40, 230):
        xx = x + rnd.uniform(-40, 40)
        els.append(ln([(xx, y0 + 6), (xx + rnd.uniform(-4, 4), (y0 + y1) / 2), (xx + rnd.uniform(-3, 3), y1)], at, "rgba(10,14,13,.6)", 2.4, draw=False))
    for k in range(10):
        els.append(poly(E(rnd.uniform(x0 + 30, x1 - 30), rnd.uniform(y0 + 30, y1 - 30), rnd.uniform(10, 28), rnd.uniform(4, 10), 10),
                        rnd.choice(["#c58a96", "#7f9a66", "#2a3432", "#6f7a70"]), at=at, op=.5))
    return els


def s23():
    """Under water beside a sheer wall of the rock: a diver with hammer and chisel at its face, chips falling, a sample bag; his hope,
    a lilac dotted stepped monument in a thought above him. Right: the room for his verdict."""
    tdv, th = T("s23", "dozens of dives"), T("s23", "Ice Age")
    els = underwater(122, seed=23, floor=780)
    top = [(80, 300), (200, 296), (330, 302), (470, 298), (520, 300), (530, 170), (640, 166), (760, 172), (900, 168)]
    els += rock_face(80, 166, 900, 790, -1, 23, top)
    els += diver(1040, 440, .9, .2, face=-1)
    els += [ln([(960, 430), (912, 420)], .5, "#c9c9c0", 5, draw=False), rect(990, 446, 40, 34, "#d8c08a", "#8a6a3e", 1.5, 4, .6, fx="pop")]
    els += [dot(905 - 6 * k, 440 + 26 * k, 4, "#a6a486", round(.8 + .2 * k, 2)) for k in range(5)]
    els += chip(1360, 240, "dozens of dives", AMBER, tdv, 28)
    els += [circ(1090 - 16 * j, 360 - 30 * j, 6 + 3 * j, "none", LILAC, 2, round(th + .1 * j, 2), style="claimed", fx="pop") for j in range(3)]
    els += [rect(1000 + 24 * j, 220 - 22 * j, 200 - 48 * j, 22, "rgba(201,193,238,.06)", LILAC, 2.5, 2, round(th + .4 + .1 * j, 2), style="claimed", fx="pop") for j in range(4)]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s24_add():
    """Primarily natural: a bar of 100 cells, 95 sandstone, 5 lilac dotted (touched up?); the same breaks under water and on land."""
    tn, tt, tl = T("s24", "natural structure"), T("s24", "touched up"), T("s24", "under water and on land")
    x0, y0, cw = 1185, 500, 5.0
    els = [rect(1175, 340, 530, 250, "rgba(12,16,18,.82)", "rgba(255,236,206,.3)", 2, 14, tn, fx="pop")]
    for k in range(100):
        nat = k < 95
        els.append(rect(x0 + 10 + k * cw, y0, cw - 1.2, 54, SAND if nat else "rgba(201,193,238,.2)", "none" if nat else LILAC, 0 if nat else 1,
                        0, round((tn + .01 * k) if nat else (tt + .05 * (k - 95)), 2), fx="pop"))
    els += [lab(1195, 470, "primarily natural", tn + .4, SAND, 30, "start"), lab(1690, 584, "touched up?", tt + .3, LILAC, 26, "end", st="ital")]
    els += [ln([[1480 + 12 * j, 410 - 6 * (j % 2)] for j in range(8)], tl, FOAM, 3, curve=True, dur=.4),
            circ(1640, 390, 15, "#ffe2a8", at=tl + .3, fx="pop"), poly([(1600, 430), (1618, 404), (1662, 404), (1682, 430)], SAND_D, at=tl + .3, fx="pop")]
    return els


# ================================================================== CHAPTER 4 · When the rock was dry
def s25():
    """The Ice Age coast in section (vertical to scale, 3 units a metre): today's sea line dashed, the Ice Age sea about 120 m lower;
    the steps, 5 to 25 m below today's line, stand high and dry."""
    t1, t2 = T("s25", "so much water"), T("s25", "sea stood far lower")
    K, SL = 3.0, 200
    ice = SL + 120 * K
    slope = [(-20, 150), (180, 160), (300, SL), (420, SL + 5 * K), (560, SL + 25 * K), (720, SL + 50 * K), (900, SL + 85 * K), (1100, ice - 10),
             (1300, ice + 30), (1800, ice + 140), (1800, 1040), (-20, 1040)]
    els = [poly(slope, "#5b4a38", "#e3c99c", 2, -1, curve=True)]
    els += [poly([(1060, ice), (1800, ice), (1800, 1040), (1060, 1040)], "url(#k-water)", at=t2, fx="fill", dur=1.0), surface_line(ice, 1080, 1800, t2 + .4)]
    els += [ln([(240, SL), (1700, SL)], t1, ICE, 3, "inferred", .8), lab(1660, SL - 18, "sea today", t1 + .3, ICE, 28, "end")]
    els += [{"k": "dim", "x1": 1500, "y1": SL, "x2": 1500, "y2": ice, "t": "about 120 m", "c": GOLD, "in": t2 + .4, "lx": 44}]
    els += [lab(1440, ice + 50, "Ice Age sea", t2 + .6, BLUE, 28, "end")]
    Tm = lambda x, y: (420 + (x - 150) * .1, SL + 5 * K + (y - 130) * (20 * K / 640))
    els += tiers(Tm, -1, "dry", TIERS, seed=25, end=True, fallen=False, slot=False)
    els += [lab(520, SL + 80 * K, "the steps", .6, GOLD, 28), ln([(510, SL + 72 * K), (490, SL + 26 * K)], .6, GOLD, 2, dur=.3)]
    return {"base": "sky", "tod": "day", "sun": [1400, 140, 24], "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s26():
    """Under water, in section: a cliff of the island's rock with a cave running into it 17 m down (25 units a metre); stalactites hang
    from its roof, the sea fills it now."""
    tc, ts, tt = T("s26", "seventeen metres"), T("s26", "stalactites"), T("s26", "tens of thousands")
    K, SL = 25, 140
    cy = SL + 17 * K
    els = underwater(SL, seed=26, floor=790)
    cliff = [(-20, SL + 26), (520, SL + 34), (760, SL + 60), (900, SL + 130), (960, 380), (1000, 520), (1060, 700), (1100, 800), (-20, 800)]
    els += [poly(cliff, "#55605a", "rgba(220,238,230,.34)", 1.5, -1)]
    els += [ln([(0, y), (min(1100, 880 + (y - 200) * .4), y + 3)], -1, "rgba(18,24,22,.32)", 1.6, draw=False) for y in range(220, 790, 44)]
    cave = [(1000, cy - 64), (860, cy - 78), (700, cy - 70), (560, cy - 52), (470, cy - 20), (450, cy + 30), (520, cy + 62), (700, cy + 74), (880, cy + 70), (1020, cy + 58)]
    els += [poly(cave, "#163844", "rgba(220,238,230,.4)", 2, -1, curve=True), gl(760, cy, 260, -1, .22, "blue")]
    rnd = random.Random(26)
    for k in range(16):
        x = 500 + 30 * k + rnd.uniform(-6, 6)
        if x > 990:
            break
        yt = cy - 52 - 22 * math.sin(math.pi * (x - 450) / 560)
        h = rnd.uniform(14, 46) * (1 if k % 3 else 1.5)
        els.append(poly([(x - 5, yt - 4), (x + 5, yt - 4), (x + 1.2, yt + h), (x, yt + h + 5), (x - 1.2, yt + h)], "#d8d0bc", "#8a8270", 1, round(ts + .05 * k, 2), fx="pop"))
    els += [{"k": "dim", "x1": 1160, "y1": SL, "x2": 1160, "y2": cy, "t": "17 m", "c": ICE, "in": tc, "lx": 40}]
    els += [lab(740, cy + 130, "a drowned cave", tc + .4, BONE, 30), lab(740, cy - 140, "stalactites", ts + .5, GOLD, 30),
            ln([(740, cy - 128), (740, cy - 70)], ts + .5, GOLD, 2, dur=.3)]
    els += chip(1420, cy + 40, "tens of thousands of years old", GOLD, tt + .2, 26)
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s27():
    """Two small panels: in air a stalactite grows drop by drop; under the sea, none (a dashed outline struck through); then a gold tick."""
    ta, tu, td = T("s27", "drip by drip"), T("s27", "Under the sea"), T("s27", "dry land")
    els = [rect(140, 170, 680, 560, "#2a2018", "rgba(255,236,206,.3)", 2, 18, -1), rect(958, 170, 680, 560, "#0f2a36", "rgba(255,236,206,.3)", 2, 18, -1)]
    els += [rect(140, 170, 680, 90, "#5b4a38", at=-1, r=18), rect(958, 170, 680, 90, "#5b4a38", at=-1, r=18)]
    els += [poly([(958, 260), (1638, 260), (1638, 730), (958, 730)], "url(#k-water)", at=-1)]
    els += [poly([(460, 260), (500, 260), (486, 420), (480, 446), (474, 420)], "#d8d0bc", "#8a8270", 1.2, ta - .2, fx="pop")]
    els += [circ(480, 470 + 40 * k, 7, "#bfe6f5", at=round(ta + .3 + .35 * k, 2), fx="pop") for k in range(4)]
    els += [poly(E(480, 712, 50, 10, 16), "#d8d0bc", at=ta + 1.6, fx="pop")]
    els += [lab(480, 790, "in air: they grow", ta + .4, BONE, 30)]
    els += [poly([(1278, 260), (1318, 260), (1304, 420), (1298, 446), (1292, 420)], "none", DIM, 2.5, tu, style="inferred"),
            strike(1220, 300, 1380, 430, tu + .4, RED, 6), lab(1298, 790, "under the sea: they don't", tu + .3, BONE, 30)]
    els += [tick(700, 230, td, GREEN, 1.6)]
    return {"base": "dark", "stars": 15, "cam": CAM, "els": els}


# the sea-level chart: years ago 12,000 (x 230) to 5,000 (x 1530); metres from +5 (y 150) to -55 (y 750), 10 units a metre
CX = lambda ka: round(230 + (11.5 - ka) * (1300 / 6.5), 1)
CY = lambda m: round(165 - m * 9, 1)
BAND = [(11.5, -42, -56), (11.0, -37, -50), (10.0, -27, -38), (9.5, -22, -32), (9.0, -18, -26), (8.5, -13, -21), (8.0, -9, -16), (7.5, -4, -11),
        (7.0, 0, -6), (6.5, 1.5, -3), (6.0, 2, -2), (5.0, 2, -1)]       # a schematic envelope of published curves (see facts_added)


def _cross(depth, which):
    """Years ago (ka) where the band's upper (which=1) or lower (2) edge crosses a depth (m, negative)."""
    for a, b in zip(BAND, BAND[1:]):
        if (a[which] - depth) * (b[which] - depth) <= 0 and a[which] != b[which]:
            return a[0] + (b[0] - a[0]) * (depth - a[which]) / (b[which] - a[which])
    return None


def s28():
    """Chart: a shaded band of sea-level curves rises; the rock's foot (25 m) and top (about 5 m); where the band crosses them."""
    tb, tf, tt = T("s28", "Then the ice"), T("s28", "rock's foot"), T("s28", "By about seven")
    up = [(CX(k), CY(u)) for k, u, l in BAND]
    lo = [(CX(k), CY(l)) for k, u, l in BAND]
    els = [axis(230, 1530, 700, [(CX(11), "11,000"), (CX(9), "9,000"), (CX(7), "7,000"), (CX(5), "5,000")], .1), lab(1530, 776, "years ago", .2, AMBER, 24, "end", st="cap")]
    els += [ln([(222, CY(0)), (222, CY(-50))], .1, "#e9dccb", 2, draw=False),
            lab(208, CY(0) + 8, "0 m", .2, DIM, 24, "end"), lab(208, CY(-25) + 8, "25 m", .2, DIM, 24, "end"), lab(208, CY(-50) + 8, "50 m", .2, DIM, 24, "end"),
            ln([(230, CY(0)), (1530, CY(0))], .2, "rgba(207,230,255,.35)", 1.5, "inferred", draw=False), lab(1540, CY(0) + 8, "today's sea level", .3, ICE, 22, "start")]
    els += [poly(up + lo[::-1], "rgba(95,168,201,.35)", "none", 0, tb, fx="fade", dur=1.2),
            ln(up, tb, SEAL, 3, dur=2.0, curve=True), ln(lo, tb + .2, SEAL, 3, dur=2.0, curve=True), lab(CX(10.8), CY(-30), "sea level", tb + 1.6, SEAL, 28)]
    els += [rect(CX(5.0) + 4, CY(-5), 60, CY(-25) - CY(-5), "rgba(217,196,154,.35)", SAND, 2, 3, tf - .3)]
    els += [ln([(230, CY(-25)), (1530, CY(-25))], tf, SAND, 2.5, dur=.8), lab(1600, CY(-25) + 8, "foot, 25 m", tf + .3, SAND, 26, "start"),
            ln([(230, CY(-5)), (1530, CY(-5))], tt - 1.0, SAND, 2.5, dur=.8), lab(1600, CY(-5) + 8, "top, 5 m", tt - .7, SAND, 26, "start")]
    a, b = _cross(-25, 1), _cross(-25, 2)
    els += bracket(CX(a), CX(b), CY(-25) + 34, tf + 1.2, "9,000 to 10,000 years ago", GOLD, up=False, ty=CY(-25) + 80)
    c, d = _cross(-5, 1), _cross(-5, 2)
    els += [ln([(CX(c), CY(-5)), (CX(d), CY(-5))], tt, GOLD, 8, dur=.4), lab((CX(c) + CX(d)) / 2, CY(-5) - 22, "about 7,000", tt + .2, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s29_add():
    """The spread: two dashed curves at the band's edges, labelled; small up-down arrows at the right: the land can move too."""
    td, tl = T("s29", "Specialists"), T("s29", "rise or sink")
    up = [(CX(k), CY(u)) for k, u, l in BAND]
    lo = [(CX(k), CY(l)) for k, u, l in BAND]
    els = [ln(up, td, GOLD, 3, "inferred", 1.0, curve=True), ln(lo, td + .2, GOLD, 3, "inferred", 1.0, curve=True),
           lab(CX(9.6), CY(-46), "curves differ", td + .6, GOLD, 26)]
    els += [arr([(CX(5.0) + 110, CY(-15)), (CX(5.0) + 110, CY(-6))], tl, AMBER, 3, dur=.4, curve=False),
            arr([(CX(5.0) + 140, CY(-14)), (CX(5.0) + 140, CY(-23))], tl + .2, AMBER, 3, dur=.4, curve=False),
            lab(1440, CY(-38), "the land can move too", tl + .4, AMBER, 26)]
    return els


def crust(x, y, r, at, rnd, c="#c98a9a", edge="#e8b8c4"):
    """A patch of pink coralline crust: a lumpy blob."""
    pts = []
    for j in range(14):
        a = 2 * math.pi * j / 14
        rr = r * rnd.uniform(.7, 1.15)
        pts.append((x + rr * math.cos(a), y + rr * .55 * math.sin(a)))
    return poly(pts, c, edge, 1.2, at, fx="pop", curve=True)


def s30():
    """Close on the rock face under water: pink coralline crusts and small corals growing on it; a chisel takes a sample: about 6,200
    years."""
    tc, ts, td = T("s30", "corals and algae"), T("s30", "only live"), T("s30", "six thousand two hundred")
    els = underwater(122, rays=True, seed=30, dark=.4)
    els += [poly([(-20, 210), (1800, 196), (1800, 820), (-20, 820)], "#55605a", "rgba(220,238,230,.34)", 1.5, -1)]
    els += [ln([(-20, y), (1800, y - 6)], -1, "rgba(18,24,22,.32)", 2, draw=False) for y in range(262, 820, 58)]
    els += [ln([(x, 204), (x + 6, 820)], -1, "rgba(10,14,13,.6)", 3, draw=False) for x in (420, 1120)]
    rnd = random.Random(30)
    for k in range(18):
        els.append(crust(rnd.uniform(100, 1700), rnd.uniform(260, 760), rnd.uniform(26, 62), round(tc + .05 * k, 2), rnd))
    for k in range(8):                                       # small coral heads and branches
        x, y = rnd.uniform(140, 1640), rnd.uniform(300, 740)
        if rnd.random() < .5:
            els += [circ(x, y, rnd.uniform(14, 22), "#d9c48a", "#a8925a", 1.5, round(tc + .6 + .06 * k, 2), fx="pop")]
        else:
            els += [ln([(x, y), (x + rnd.uniform(-24, 24), y - rnd.uniform(28, 50))], round(tc + .6 + .06 * k, 2), "#e0c890", 5, dur=.3),
                    ln([(x, y - 14), (x + rnd.uniform(-30, 30), y - rnd.uniform(36, 60))], round(tc + .7 + .06 * k, 2), "#e0c890", 4, dur=.3)]
    els += [lab(889, 170, "they grow only in the sea", ts, ICE, 30)]
    cx, cy = 1180, 470
    els += [ln([(cx + 40, cy), (cx + 170, cy - 40)], td - .8, "#c9c9c0", 8, draw=False), rect(cx + 160, cy - 70, 70, 40, "#8a8580", at=td - .8, r=6),
            circ(cx, cy + 6, 34, "none", GOLD, 3, td - .4, fx="pop")]
    els += chip(cx, cy + 90, "about 6,200 years", GOLD, td, 28)
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


XT = lambda ka: round(160 + (12.0 - ka) * (700 / 12.0), 1)        # the estimates timeline: years ago 12,000 (x 160) to today (x 860)


def s31():
    """Left: Kimura's estimates on a time axis (lilac dotted): 2004, about 10,000 or more; 2007, 2,000 to 3,000. Right: a coast section
    with the terraces drawn at sea level, lilac dashed: built on land?"""
    t4, t7, tl = T("s31", "two thousand and four"), T("s31", "two thousand and seven"), T("s31", "built on land")
    X = lambda ka: round(120 + (12.0 - ka) * (760 / 12.0), 1)
    els = [axis(120, 880, 600, [(X(12), "12,000"), (X(8), "8,000"), (X(4), "4,000"), (X(0), "today")], .1, "years ago")]
    els += [ln([(X(10), 470), (X(12), 470)], t4, LILAC, 7, "claimed", .6), circ(X(10), 470, 12, LILAC, at=t4, fx="pop"),
            lab(X(10.2), 420, "2004: about 10,000 or more", t4 + .3, LILAC, 30, "start", st="ital")]
    els += [rect(X(3), 330, X(2) - X(3), 26, "rgba(201,193,238,.25)", LILAC, 2, 5, t7, style="claimed", fx="pop"),
            lab(X(2.5) - 10, 290, "2007: 2,000 to 3,000", t7 + .3, LILAC, 30, "end", st="ital")]
    SL = 420
    els += [poly([(1000, SL), (1720, SL), (1720, 800), (1000, 800)], "url(#k-water)", at=-1), surface_line(SL, 1000, 1720),
            poly([(1000, 300), (1150, 310), (1190, 800), (1000, 800)], "#5b4a38", "#e3c99c", 2, -1), lab(1075, 280, "coast", .3, DIM, 24)]
    blk = [(1240, SL), (1240, SL - 40), (1320, SL - 40), (1320, SL - 70), (1410, SL - 70), (1410, SL - 96), (1540, SL - 96), (1580, SL)]
    els += [poly(blk, "rgba(201,193,238,.08)", LILAC, 3, tl, style="inferred", fx="rise"), lab(1410, SL - 130, "built on land?", tl + .4, LILAC, 28, st="ital")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s32_add():
    """The drop that would be needed (25 m, lilac dashed, an arrow down), and the north shore marker (solid): within a few metres."""
    td, tn = T("s32", "drop some"), T("s32", "north shore")
    SL, K = 420, 12.0
    blk = [(1240, SL), (1240, SL - 40), (1320, SL - 40), (1320, SL - 70), (1410, SL - 70), (1410, SL - 96), (1540, SL - 96), (1580, SL)]
    low = [(x, y + 25 * K) for x, y in blk]
    els = [poly(low, "rgba(201,193,238,.12)", LILAC, 3, td + .4, style="inferred", fx="pop"),
           arr([(1620, SL - 40), (1620, SL + 25 * K - 40)], td, LILAC, 4, "inferred", .8, curve=False),
           {"k": "dim", "x1": 1680, "y1": SL, "x2": 1680, "y2": SL + 25 * K, "t": "25 m", "c": LILAC, "in": td + .5, "lx": -50, "upright": True}]
    els += [rect(1010, SL - 8, 150, 16, GOLD, at=tn, fx="pop", r=4), ln([(1085, SL - 10), (1085, 216)], tn + .2, GOLD, 2, dur=.4),
            lab(1085, 166, "north shore: within a few m", tn + .4, GOLD, 28), lab(1085, 200, "for 6,500 years", tn + .5, GOLD, 26)]
    return els


def s33_add():
    """If carved, before this: the dry region of the rock's depths, left of where the band closes over them, shaded amber."""
    tw = T("s33", "while it was")
    pts = [(CX(11.5), CY(-5)), (CX(_cross(-5, 1)), CY(-5))]
    for k, u, l in BAND:
        m = (u + l) / 2
        if -25 <= m <= -5:
            pts.append((CX(k), CY(m)))
    pts += [(CX(_cross(-25, 1) - .2), CY(-25)), (CX(11.5), CY(-25))]
    return [poly(pts, "rgba(232,184,122,.28)", AMBER, 2, tw, fx="fade", dur=.8), lab(CX(10.6), CY(-15), "if carved: before this", tw + .5, AMBER, 30)]


# ================================================================== CHAPTER 5 · What a quarry leaves
def s34():
    """People in the islands: the chain map again, pins on Okinawa (Sakitari Cave) and Ishigaki (Shiraho); over 30,000 years ago."""
    tp = T("s34", "Humans reached")
    v = VM
    ox, oy = v.p(127.77, 26.14)
    ix, iy = v.p(124.25, 24.36)
    yx, yy = v.p(123.0, 24.45)
    els = map_base(v) + [{"k": "pin", "x": yx, "y": yy, "t": "Yonaguni", "c": GOLD, "lx": -16, "ly": 36, "a": "end", "in": .4},
                         {"k": "pin", "x": ox, "y": oy, "t": "Sakitari Cave", "c": AMBER, "lx": 18, "ly": 36, "in": tp},
                         {"k": "pin", "x": ix, "y": iy, "t": "Shiraho", "c": AMBER, "lx": 16, "ly": 40, "in": tp + .4}]
    els += chip(1250, 560, "over 30,000 years ago", AMBER, tp + .9, 28)
    return {"base": "map", "cam": CAM, "els": els}


def canoe(x, y, w, at, n=5):
    """A dugout canoe with paddlers, centred on x, waterline y (adapted from f04.py yonaguni_m)."""
    out = [poly([[x - w / 2, y - 10], [x + w / 2, y - 14], [x + w / 2 - 20, y + 10], [x - w / 2 + 16, y + 10]], "#7a4a2a", "#c9905a", 2, at, fx="pop")]
    for k in range(n):
        px = x - w / 2 + 34 + k * (w - 68) / max(1, n - 1)
        out += [person(round(px, 1), y - 8, 46, round(at + .15 + .08 * k, 2), SKIN), ln([[round(px + 8, 1), y - 30], [round(px - 14, 1), y + 14]], round(at + .3 + .08 * k, 2), "#cbbca8", 3, draw=False)]
    return out


def s35():
    """Open sea between Taiwan and Yonaguni: a dugout with five paddlers crosses; 225 km; two days and a night (two suns and a moon);
    steering by sun, stars and swell."""
    tc, tst, tn = T("s35", "five paddlers"), T("s35", "steering by"), T("s35", "Two hundred")
    th = T("s35", "forty-five hours")
    SL = 540
    els = [poly([(-20, SL), (1800, SL), (1800, 1040), (-20, 1040)], "url(#k-water)", at=-1), surface_line(SL, -20, 1800, -1, FOAM, 3, .8)]
    els += [poly([(-20, SL), (-20, 300), (80, 270), (190, 330), (260, 420), (320, SL)], "#56663e", "#c9d79a", 2, -1, curve=True),
            lab(120, SL + 60, "Taiwan", .3, "#c9d79a", 32),
            poly([(1520, SL), (1560, SL - 50), (1630, SL - 62), (1690, SL - 30), (1720, SL)], "#56663e", "#c9d79a", 2, -1, curve=True),
            lab(1620, SL + 60, "Yonaguni", .5, "#c9d79a", 32)]
    els += canoe(860, SL + 6, 300, tc)
    els += [arr([(330, SL - 60), (860, SL - 170), (1500, SL - 70)], tn, AMBER, 3, "inferred", 1.4), lab(860, SL - 200, "225 km", tn + .6, AMBER, 40, st="serif")]
    els += [{"k": "stars", "n": 40, "x0": 600, "x1": 1100, "y0": 140, "y1": 300, "in": tst}, circ(560, 210, 22, "#ffe2a8", at=tst - .2, fx="pop"),
            gl(560, 210, 70, tst - .2, .8, "sun"), poly([(1160, 380), (1220, 360), (1280, 380)], "none", FOAM, 3, tst + .4, curve=True)]
    for k, (kind, x) in enumerate((("sun", 300), ("moon", 650), ("sun", 1000))):
        at = round(th + .3 * k, 2)
        if kind == "sun":
            els += [circ(x + 400, 160, 20, "#ffe2a8", at=at, fx="pop"), gl(x + 400, 160, 60, at, .7, "sun")]
        else:
            els += [circ(x + 400, 160, 20, "#efe8da", at=at, fx="pop"), circ(x + 410, 154, 20, "#2a3040", at=at, fx="pop")]
    els += [lab(1100, 240, "about 45 hours", th + 1.0, BONE, 30)]
    return {"base": "sky", "tod": "dusk", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def s36():
    """The everyday picture: a carpenter's workshop, swept clean in the middle; sawdust still glows in the corners."""
    tq, ts = T("s36", "A quarry is"), T("s36", "sawdust")
    els = [rect(100, 150, 1578, 640, "#3a2a1c", at=-1, r=10), rect(100, 560, 1578, 230, "#6b4a30", at=-1)]
    els += [ln([(100, 600 + 40 * j), (1678, 600 + 40 * j)], -1, "#4a3322", 2, draw=False) for j in range(5)]
    els += [rect(600, 430, 520, 40, WOOD, "#c9a070", 1.5, 3, -1), rect(630, 470, 24, 110, WOOD_D, at=-1), rect(1066, 470, 24, 110, WOOD_D, at=-1),
            ln([(1300, 580), (1420, 300)], -1, "#c9a070", 6, draw=False), poly([(1270, 580), (1330, 580), (1320, 640), (1280, 640)], "#b8a070", at=-1)]
    els += [gl(860, 250, 300, .1, .35, "lamp"), circ(860, 250, 14, "#ffe2a8", at=-1)]
    rnd = random.Random(36)
    for corner in ((150, 760), (1630, 760), (150, 590), (1630, 590)):
        for k in range(14):
            x = corner[0] + rnd.uniform(-30, 30) + (20 if corner[0] < 500 else -20)
            y = corner[1] + rnd.uniform(-14, 14)
            els.append(dot(round(x, 1), round(y, 1), round(rnd.uniform(2, 4), 1), "#e8c88a", round(ts + .03 * k, 2), op=.9))
        els.append(gl(corner[0] + (40 if corner[0] < 500 else -40), corner[1], 70, ts + .3, .6, "lamp"))
    els += [lab(889, 230, "sawdust in the corners", ts + .6, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s37():
    """What a quarry leaves, drawn solid as an illustration: wedge slots in a row along a split, chips and a broken tool, a block
    abandoned half cut, a hearth with shells and bones, a soil layer sealing them with a date tag."""
    tw, tc, tb, th, td = T("s37", "matching slots"), T("s37", "chips"), T("s37", "half cut"), T("s37", "hearths"), T("s37", "can be dated")
    G = 640
    els = [poly([(-20, 160), (1800, 160), (1800, G), (-20, G)], "#2a2420", at=-1),
           poly([(80, G), (80, 240), (700, 220), (760, G)], "#b9a27a", "rgba(255,236,206,.5)", 1.5, -1)]
    els += [ln([(82, 260 + 50 * j), (730, 250 + 50 * j)], -1, "rgba(80,60,40,.35)", 1.6, draw=False) for j in range(8)]
    els += [poly([(x - 12, 330), (x + 12, 330), (x + 5, 368), (x - 5, 368)], "#3a2a1c", at=round(tw + .12 * k, 2), fx="pop") for k, x in enumerate(range(150, 700, 90))]
    els += [ln([(140, 368), (700, 370)], tw + .9, "#2a1c10", 3, dur=.8), lab(420, 300, "wedge slots", tw + .6, GOLD, 28)]
    rnd = random.Random(37)
    for k in range(26):
        x, y = rnd.uniform(780, 990), G - rnd.uniform(0, 60) * (1 - abs(rnd.uniform(-1, 1)))
        els.append(poly([(x, y), (x + rnd.uniform(6, 14), y - rnd.uniform(4, 10)), (x + rnd.uniform(10, 18), y)], "#c9b48c", at=round(tc + .03 * k, 2), fx="pop"))
    els += [rect(900, G - 26, 50, 18, "#8a8580", at=tc + .6, r=4), rect(960, G - 22, 40, 16, "#8a8580", at=tc + .7, r=4), ln([(946, G - 22), (958, G - 16)], tc + .8, "#3a3530", 3, draw=False)]
    els += [lab(900, G - 110, "chips", tc + .4, GOLD, 28)]
    els += [poly([(1060, G), (1060, G - 120), (1260, G - 120), (1260, G - 60), (1180, G - 60), (1180, G)], "#b9a27a", "rgba(255,236,206,.5)", 1.5, tb, fx="rise"),
            ln([(1180, G - 60), (1180, G)], tb + .3, "#2a1c10", 3, "inferred", .4)]
    els += [poly(E(1450, G - 10, 70, 14, 20), "#2a1a12", at=th, fx="pop"), gl(1450, G - 26, 90, th + .1, .8, "fire")]
    els += [poly(E(1380 + 30 * k, G - 6, 10, 6, 10), "#efe6d2", at=round(th + .3 + .1 * k, 2), fx="pop") for k in range(3)]
    els += [ln([(1500, G - 4), (1560, G - 14)], th + .6, "#efe6d2", 6, draw=False), lab(1450, G - 90, "hearth", th + .5, GOLD, 28)]
    els += [rect(760, G, 1000, 70, "#6b5a44", "rgba(255,236,206,.3)", 1, 0, td - .4, fx="fill", dur=.6), rect(-20, G + 70, 1820, 300, "#4a3c2e", at=-1)]
    els += chip(1300, G + 36, "dated layer", AMBER, td, 26)
    return {"base": "dark", "cam": CAM, "els": els}


def s38():
    """What nature leaves: terraces whose edges follow the bedding and the joints (gold dashed along the cracks), and fallen blocks lying at
    the foot."""
    tf, tb = T("s38", "follow the rock's"), T("s38", "fallen blocks")
    sp = TIERS
    Tm = lambda x, y: (x * .9 + 120, y * .92 + 30)
    els = underwater(122, rays=True, seed=38, dark=.45, floor=Tm(0, 770)[1]) + tiers(Tm, -1, "water", sp, seed=38, end=True)
    els += [ln([Tm(*q) for q in (corner(sp, k), tpt(sp, sp["xbs"][k] - 6, sp["z"][k], sp["h"][k]))], round(tf + .15 * k, 2), GOLD, 3, "inferred", .4) for k in range(5)]
    for i, x in enumerate(sp["joints"][:4]):
        k = max(j for j in range(5) if sp["xa"][j] <= x)
        els.append(ln([Tm(*tpt(sp, x, sp["z"][k], sp["h"][k])), Tm(*tpt(sp, x, sp["z"][k], sp["h"][k - 1] if k else 0))], round(tf + .8 + .1 * i, 2), GOLD, 3, "inferred", .4))
    els += [lab(*Tm(700, 130), "follows the cracks", tf + .6, GOLD, 30)]
    bx, by = Tm(*tpt(sp, 90, 5, 10))
    els += [circ(bx, by, 76, "none", AMBER, 3, tb, fx="pop"), lab(bx + 20, by - 96, "fallen blocks", tb + .3, AMBER, 30)]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


SROWS = [300, 410, 520, 630]


def srow(k, at, left, right=None, rt=None, rc=BONE, q=False):
    y = SROWS[k]
    out = [rect(150, y - 44, 1480, 88, "rgba(242,201,142,.07)", "rgba(242,201,142,.28)", 1.5, 12, at, fx="pop"), lab(190, y + 10, left, at + .1, BONE, 30, "start")]
    if right:
        out += [lab(1000, y + 10, right, rt, rc, 30, "start", st="ital" if q else "lab")]
        if q:
            out += [lab(1560, y + 18, "?", rt + .2, LILAC, 54, st="serif")]
    return out


def s39():
    """A scorecard: expected if carved against found so far; rows 1 and 2: wedge slots (dents, disputed), debris (moved or fallen?)."""
    ts, td, tb = T("s39", "So what has"), T("s39", "Dents that"), T("s39", "Blocks he")
    els = [rect(110, 150, 1560, 560, "rgba(14,16,18,.78)", "rgba(255,236,206,.3)", 2, 18, .1),
           lab(190, 215, "expected if carved", .3, AMBER, 28, "start", st="cap"), lab(1000, 215, "found so far", ts, AMBER, 28, "start", st="cap"),
           ln([(960, 180), (960, 690)], .3, "rgba(255,236,206,.2)", 2, draw=False)]
    els += srow(0, .5, "wedge slots in rows", "dents, disputed", td + .2, LILAC, True)
    els += srow(1, .8, "debris, broken tools", "blocks: moved or fallen?", tb + .2, LILAC, True)
    els += srow(2, 1.1, "finds in dated layers") + srow(3, 1.4, "an official site")
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s40_add():
    """Rows 3 and 4: reported, not published; not recognised."""
    tf, tr = T("s40", "the incised slab"), T("s40", "Japan's cultural")
    return [lab(1000, SROWS[2] + 10, "reported, not published", tf, MUTED, 30, "start", st="ital"),
            lab(1000, SROWS[3] + 10, "not recognised", tr, MUTED, 30, "start", st="ital")]


def s41():
    """Timeline: the sea closes over the steps (about 10,000 to 7,000 years ago); the oldest dated traces on Yonaguni at about 4,400;
    before 10,000, a lilac dotted zone: older camps, now under the sea?"""
    to, tg, tc = T("s41", "oldest dated"), T("s41", "long after"), T("s41", "older camp")
    X = lambda ka: round(170 + (12.0 - ka) * (1440 / 12.0), 1)
    els = [axis(170, 1610, 620, [(X(12), "12,000"), (X(10), "10,000"), (X(8), "8,000"), (X(6), "6,000"), (X(4), "4,000"), (X(2), "2,000"), (X(0), "today")], .1, "years ago")]
    els += [rect(X(10), 500, X(7) - X(10), 44, "rgba(95,168,201,.55)", SEAL, 2, 8, .5, fx="pop"), lab((X(10) + X(7)) / 2, 470, "the sea closes over the steps", .8, SEAL, 28)]
    els += [circ(X(4.41), 590, 14, GOLD, at=to, fx="pop"), gl(X(4.41), 590, 70, to, .6, "lamp"), ln([(X(4.41), 576), (X(4.41), 400)], to + .2, GOLD, 2, dur=.4),
            lab(X(4.41), 334, "oldest dated traces on Yonaguni", to + .4, GOLD, 28), lab(X(4.41), 372, "Tuguru-hama, about 4,400", to + .5, DIM, 26)]
    els += bracket(X(7), X(4.41), 680, tg, "thousands of years", AMBER, up=False, ty=730)
    els += [rect(X(12) + 4, 500, X(10) - X(12) - 12, 44, "rgba(201,193,238,.08)", LILAC, 2.5, 8, tc, style="claimed", fx="pop"),
            lab((X(12) + X(10)) / 2, 404, "older camps?", tc + .3, LILAC, 28, st="ital"), lab((X(12) + X(10)) / 2, 440, "under the sea", tc + .4, LILAC, 26, st="ital")]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s42():
    """Close on a terrace under water: mud and sand fill the hollows of the tread; a dashed amber rectangle where a trench would go: no
    published dig (adapted from f04.py yonaguni_m, the sediment nobody has dug)."""
    tn, to = T("s42", "controlled dig"), T("s42", "Not once")
    sp = TIERS
    cx0, cy0 = tpt(sp, 560, 170, sp["h"][2])
    Tm = lambda x, y: (889 + (x - cx0) * 2.4, 470 + (y - cy0) * 2.4)
    els = underwater(122, rays=True, seed=42, dark=.4) + tiers(Tm, -1, "water", sp, seed=42, end=True, fallen=False, slot=False)
    rnd = random.Random(42)
    mud = [tpt(sp, x, z, sp["h"][2]) for x, z in ((470, 150), (560, 146), (690, 152), (760, 166), (720, 186), (600, 192), (480, 186), (440, 168))]
    els += [poly([Tm(*q) for q in mud], MUD, "rgba(255,236,206,.25)", 1.5, -1, curve=True)]
    for k in range(50):
        x, z = rnd.uniform(470, 740), rnd.uniform(152, 186)
        gx, gy = Tm(*tpt(sp, x, z, sp["h"][2]))
        els.append(dot(round(gx, 1), round(gy, 1), round(rnd.uniform(2, 4.5), 1), rnd.choice(["#b8a888", "#8a7a62", "#cbb898"]), -1, None, .75))
    a, b = Tm(*tpt(sp, 520, 158, sp["h"][2])), Tm(*tpt(sp, 680, 180, sp["h"][2]))
    els += [rect(min(a[0], b[0]), min(a[1], b[1]) - 20, abs(b[0] - a[0]), abs(b[1] - a[1]) + 40, "none", AMBER, 4, 4, tn, style="inferred", fx="draw"),
            lab((a[0] + b[0]) / 2, min(a[1], b[1]) - 50, "no published dig", tn + .3, AMBER, 32)]
    els += [gl((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 140, to, .35, "lamp")]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


# ================================================================== CHAPTER 6 · The weighing
LROWS = [205, 315, 425, 535, 645]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(130, y - 48, 1520, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 28, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1240, y, grade, gc, gt, 26, "start")
    return out


def pic_rock(x, y, at):
    return corner_block(x - 50, y + 32, 70, 60, 26, at)


def pic_wave(x, y, at):
    return [poly([(x - 50, y + 30), (x - 50, y + 10), (x - 20, y + 10), (x - 20, y - 10), (x + 10, y - 10), (x + 10, y - 28), (x + 50, y - 28), (x + 50, y + 30)],
                 FRONTW, EDGEW, 1, at, fx="pop"), ln([[x - 54 + 9 * j, y - 36 - 5 * (j % 2)] for j in range(13)], at, FOAM, 3, curve=True, dur=.3)]


def pic_people(x, y, at):
    return [person(x - 20, y + 34, 56, at, SKIN), person(x + 16, y + 34, 50, at + .05, SKIN), ln([(x - 56, y + 34), (x + 56, y + 34)], at, SAND, 3, draw=False)]


def pic_q(x, y, at):
    return [lab(x, y + 22, "?", at, LILAC, 64, st="serif")]


def pic_mono(x, y, at):
    return [rect(x - 50 + 12 * j, y + 24 - 18 * (j + 1), 100 - 24 * j, 18, "rgba(201,193,238,.08)", LILAC, 2, 2, at, style="claimed", fx="pop") for j in range(4)]


def s43():
    """The ledger: row 1, the island's own bedrock: Established."""
    t1, g1 = T("s43", "Established"), T("s43", "the island's own")
    els = [rect(100, 135, 1580, 575, "rgba(14,16,18,.78)", "rgba(255,236,206,.3)", 2, 18, .1)]
    els += lrow(0, t1, pic_rock, "the island's own bedrock, in layers", "Established", g1 + .6, GRADE["established"])
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s44_add():
    t2, t3, t4 = T("s44", "Established too"), T("s44", "Plausible"), T("s44", "Open: whether")
    els = lrow(1, t2, pic_wave, "dry in the Ice Age, drowned 10,000 to 7,000 years ago", "Established", t2 + .4, GRADE["established"])
    els += lrow(2, t3, pic_people, "people could have walked on it", "Plausible", t3 + .3, GRADE["plausible"])
    els += lrow(3, t4, pic_q, "whether anyone shaped it", "Open question", t4 + .3, GRADE["open"])
    return els


def s45_add():
    tm, tv = T("s45", "A monument carved"), T("s45", "Awaiting")
    els = lrow(4, tm, pic_mono, "a monument carved by people", "Awaiting evidence", tv, GRADE["awaiting"])
    els += [gl(1400, LROWS[4], 220, tv, .4, "lamp")]
    return els


def s46():
    """The test: a stepped trench (inferred) through the mud of a terrace to the rock; lilac dotted, wanted: a stone tool, a hearth, a
    broken wedge sealed against a cut face; then a row of identical marks across the natural cracks."""
    tt, tf, tm = T("s46", "A trench through"), T("s46", "stone tool"), T("s46", "Tool marks in rows")
    G = 330
    els = underwater(122, rays=True, seed=46, dark=.35)
    els += [rect(-20, G, 1820, 700, FRONTW, at=-1), rect(-20, G, 1820, 110, MUD, at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,236,206,.4)", 2, draw=False)]
    els += [ln([(-20, y), (1800, y)], -1, "rgba(20,24,20,.3)", 2, draw=False) for y in range(G + 150, 820, 50)]
    els += [ln([(x, G + 110), (x, 820)], -1, "rgba(12,16,14,.6)", 3, draw=False) for x in (360, 1340)]
    tr = [(560, G), (560, G + 60), (620, G + 60), (620, G + 130), (1060, G + 130), (1060, G + 60), (1120, G + 60), (1120, G)]
    els += [poly(tr, "rgba(15,40,52,.85)", BLUE, 3, tt, style="inferred", fx="draw")]
    els += [person(700, G + 130, 70, tt + .4, "#2a3a40"), person(980, G + 130, 70, tt + .5, "#2a3a40")]
    els += [poly([(760, G + 126), (790, G + 104), (812, G + 126)], "none", LILAC, 3, tf, style="claimed"),
            poly(E(860, G + 122, 30, 8, 14), "none", LILAC, 3, tf + .3, style="claimed"), gl(860, G + 116, 50, tf + .3, .5, "fire"),
            poly([(920, G + 112), (956, G + 112), (948, G + 126), (928, G + 126)], "none", LILAC, 3, tf + .6, style="claimed"),
            lab(840, G - 40, "sealed finds, wanted", tf + .8, LILAC, 28, st="ital")]
    els += [poly([(x - 10, 600), (x + 10, 600), (x + 4, 630), (x - 4, 630)], "none", GOLD, 3, round(tm + .1 * k, 2), style="inferred") for k, x in enumerate(range(240, 1600, 130))]
    els += [lab(889, 690, "marks across the cracks", tm + 1.2, GOLD, 28)]
    return {"base": "sky", "tod": "day", "sun": False, "ground": 1300, "ridges": [], "cam": CAM, "els": els}


def flask(x, y, at, c=ICE):
    return [poly([(x - 14, y - 90), (x + 14, y - 90), (x + 14, y - 50), (x + 46, y), (x - 46, y), (x - 14, y - 50)], "rgba(159,208,255,.12)", c, 2.5, at, fx="pop"),
            poly([(x - 36, y - 14), (x + 36, y - 14), (x + 46, y), (x - 46, y)], "rgba(159,208,255,.45)", at=at + .1, fx="pop")]


def s47():
    """Three labs, matching dates; a journal page with a green tick; two divers, gold and blue, side by side."""
    tl, tp, tb = T("s47", "more than one lab"), T("s47", "published"), T("s47", "Best of all")
    els = [gl(889, 430, 640, .1, .2, "lamp")]
    for k in range(3):
        x = 260 + 210 * k
        els += flask(x, 520, round(tl + .2 * k, 2))
        els += chip(x, 590, "same date", GREEN, round(tl + .5 + .2 * k, 2), 22)
    els += [rect(930, 260, 240, 320, "#efe6d2", "#8a7a66", 2, 6, tp, fx="pop")]
    els += [ln([(960, 300 + 24 * j), (1140 - 30 * (j % 3), 300 + 24 * j)], tp + .2, "#8a7a66", 3, draw=False) for j in range(9)]
    els += [tick(1130, 540, tp + .5, GREEN, 1.4), lab(1050, 640, "published", tp + .6, GREEN, 28)]
    els += diver(1360, 360, .7, tb, AMBER, face=1, lamp=False) + diver(1500, 470, .7, tb + .2, BLUE, face=-1, lamp=False)
    els += [lab(1430, 640, "rivals, side by side", tb + .6, BONE, 28)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s48_add():
    """The close: the hero terraces at dusk blue; one lamp glows on the mud of a terrace."""
    x, y = tpt(TIERS, 700, 230, TIERS["h"][3])
    return [rect(-20, 100, 1820, 940, "#0a1a2a", at=.4, op=.38, dur=2.0), gl(x, y, 120, 1.4, .8, "lamp"), circ(x, y, 6, "#ffe2a8", at=1.4, fx="pop")]


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "Some call it", "s2"), (1, "And when was", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "In {1986", "s6")], {"chapter": "Ruins Point"}),
    (1, 1, "collision", "s7", [(1, "By his measure", "s8")], {}),
    (1, 2, "reversal", "s9", [], {}),
    (1, 3, "tag", "s10", [], {}),
    (2, 0, "world", "s11", [], {"chapter": "The case for a monument"}),
    (2, 1, "collision", "s12", [(1, "His team reported", "s13"), (2, "Further out", "s14")], {}),
    (2, 2, "reversal", "s15", [], {}),
    (2, 3, "tag", "s16", [], {}),
    (3, 0, "world", "s17", [], {"chapter": "Flat layers, straight cracks"}),
    (3, 1, "collision", "s18", [(1, "Think of a", "s19"), (2, "Here, the lifting", "s20")], {}),
    (3, 2, "cost", "s21", [(0, "In {2024", "s22")], {}),
    (3, 3, "reversal", "s23", [(1, "He concluded that", "s24")], {}),
    (3, 4, "tag", "s24", [], {}),
    (4, 0, "world", "s25", [], {"chapter": "When the rock was dry"}),
    (4, 1, "collision", "s26", [(1, "Stalactites grow", "s27")], {}),
    (4, 2, "cost", "s28", [(1, "Those dates are", "s29"), (2, "There's a second", "s30")], {}),
    (4, 3, "reversal", "s31", [(1, "That would need", "s32")], {}),
    (4, 4, "tag", "s33", [], {}),
    (5, 0, "world", "s34", [(1, "In {2019", "s35")], {"chapter": "What a quarry leaves"}),
    (5, 1, "collision", "s36", [(1, "Splitting stone", "s37"), (2, "Nature leaves", "s38")], {}),
    (5, 2, "reversal", "s39", [(1, "As far as", "s40")], {}),
    (5, 3, "cost", "s41", [], {}),
    (5, 4, "tag", "s42", [], {}),
    (6, 0, "weigh", "s43", [(1, "Established too", "s44"), (2, "A monument carved", "s45")], {"chapter": "The weighing"}),
    (6, 1, "test", "s46", [(0, "Dates from that", "s47")], {}),
    (6, 2, "close", "s48", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s22": ("s21", [1, 889, 500], "s22_add"), "s24": ("s23", [1.3, 1100, 480], "s24_add"),
    "s29": ("s28", [1, 889, 500], "s29_add"), "s32": ("s31", [1, 889, 500], "s32_add"), "s33": ("s28", [1, 889, 500], "s33_add"),
    "s40": ("s39", [1, 889, 500], "s40_add"),
    "s44": ("s43", [1, 889, 500], "s44_add"), "s45": ("s43", [1, 889, 500], "s45_add"),
    "s48": ("s1", [1.08, 900, 470], "s48_add"),
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
    ep = {"id": "lf-yonaguni", "code": "LF.24", "series": script["series"], "title": script["title"], "case": "yonaguni",
          "verdict": "unsupported", "claim": "Is the Yonaguni formation a monument carved by people?", "mood": "mystery",
          "hook_text": "Who carved these *steps*?", "beats": beats, "shots": shots,
          "sources": "Kimura 2000 (doi:10.3759/tropics.10.5) · Kimura 2004, Ocean Newsletter 103 · Kimura et al. 2002, 2005, 2007 (Nagoya AMS reports) · "
                     "Schoch & McNally 1999 · Yazaki 1982 (GSJ) · Ogata et al. 2020 (doi:10.4157/ejgeo.15.44) · Lambeck et al. 2014 (doi:10.1073/pnas.1411762111) · "
                     "Hijma et al. 2025 (doi:10.1038/s41586-025-08769-7) · Fujita et al. 2016 (doi:10.1073/pnas.1607857113) · Kaifu et al. 2025 (doi:10.1126/sciadv.adv5507)",
          "post": "Giant stone steps under the sea off Japan's westernmost island, called a drowned pyramid. Kimura's case at its strongest, the sandstone "
                  "that splits into steps by itself, the sea-level clocks that date when it went under, what a quarry would have left, and the dig that has never been published.",
          "hashtags": ["#Yonaguni", "#Japan", "#Underwater", "#Geology", "#Archaeology", "#WeighItYourself"],
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
