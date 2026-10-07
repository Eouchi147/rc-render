"""LF.34 · Underworlds · The Temple Builders of Malta (16:9 long film, one wall).

The script is films/long/lf-malta-temples/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s56; s4, the title, is the intro card over the hero),
drawn while it is said. The hero is the lower (South) temple of Mnajdra at dawn on the equinox, seen from its back niche down the
temple's axis: the inner doorway near and large, the first chamber, and far away the main doorway with the sun in it, a shaft of light
running the length of the floor. Maps of the Maltese islands use outlines drawn here from the coast (the 50 m land data has Malta and Gozo
as eight-point blobs); Sicily comes from the land data. Drawings are schematic and true to the numbers said: solid = measured, dashed =
inferred, dotted lilac = claimed. Gozo's tale of the giantess Sansuna is drawn as a storybook print, a tradition told with affection, not
a claim to weigh. The dead of the Hypogeum are drawn as quiet lights, never as bones.

Facts: the script's facts_added (Heritage Malta; UNESCO; Renfrew 1973, 1986; Evans 1971; Trump 1966, 1971, 2002; McLaughlin et al. 2020;
Malone et al. 2020; Stoddart et al. 2022; Groucutt et al. 2022; Ariano et al. 2022; Scerri et al. 2025; Rossi et al. 2025; Till 2017;
Wolfe, Swanson & Till 2020; Cook, Pajot & Leuchter 2008; Debertolis et al. 2015; Mottershead 2007; Mottershead et al. 2008; Groucutt 2022;
Furlani et al. 2013; Azzopardi 2007; Zammit 1910; Hancock 2002; Ancient Apocalypse 2022).

Engine workaround (as in lf_stonehenge.py, lf_troy.py and lf_antikythera.py): the wall only adds elements to a panel on its first visit,
at a beat start or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag
(+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item
(built on that step's clock). Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25
syllables a second). Two engine notes: a `band` given fx 'draw' shows at once (kit.js finds no path to trace), so bands here fade in; a
group's children have no build-ins of their own (the group's build-in governs), which the clipped groups (the print in s8, the magnifier in
s27, the broken statue in s48) rely on. Covers fake fades: s23's cover repeats the water's own flat bands, so the drowned 'temple' fades
cleanly off the seabed.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-malta-temples/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-malta-temples/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-malta-temples RC_FILMS_EPS=/tmp/claude-0/sbx_lf-malta-temples/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-malta-temples/boards python3 films.py long.lf_malta_temples
"""
import json, math, os, random, re
import films as _films
from films import View
from mural import remix
import illus as I
from illus import glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-malta-temples", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
GLOB, GLOB_L, GLOB_D = "#c9a978", "#ecd3a2", "#6f5a3e"      # globigerina limestone: honey, sunlit, shade
CORA, CORA_L, CORA_D = "#8f877a", "#cfc4ae", "#4a453e"      # coralline limestone: grey, sunlit, shade
OCHRE, OCHRE_L = "#b4452f", "#e0775a"                       # red ochre
CLAY, CLAY_L, CLAY_D = "#b98a5e", "#e2b98c", "#6e4a2c"      # fired clay
SEAC, SEAD, SEAL = "#3f86a8", "#173a4c", "#9fd0ff"          # sea, deep sea, light
NIGHT = "#0e0b09"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#c9e48f", "open": "#f0b06a", "awaiting": "#d9c26a", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # BCE, DNA: letters
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


def chip(x, y, t, c, at, size=28, a="middle", z=1.0):
    """A pill with a coloured rim and its words (grades, dates); z = the camera zoom it is seen at (the rim scales with the camera,
    the words keep their size)."""
    w = (len(t) * size * .56 + 44) / z
    h = size * 1.7 / z
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36 / z, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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
    """An irregular closed outline (a boulder, a crag, a cloud)."""
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


def mix(c1, c2, t):
    """Blend two #rrggbb colours (t = 0 gives c1)."""
    t = max(0.0, min(1.0, t))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[k] + (b[k] - a[k]) * t) for k in range(3))


# ================================================================== figures
def fig(x, y, h, at, c="#1a1410", arms=None, face=1, fx="rise", op=None, lean=0.0):
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up', 'pull' (both forward and low), 'lift'.
    lean > 0 tilts the body forward (hauling)."""
    f = face
    X = lambda a, b=0: x + f * (a * h + lean * b * h)
    Y = lambda b: y - b * h
    els = [circ(X(.01, .9), Y(.9), .085 * h, c, at=at),
           poly([(X(-.13, .78), Y(.78)), (X(.13, .78), Y(.78)), (X(.11, .44), Y(.44)), (X(-.11, .44), Y(.44))], c, at=at),
           poly([(X(-.11, .46), Y(.46)), (X(.11, .46), Y(.46)), (X(.085), Y(0)), (X(.025), Y(0)), (X(0, .3), Y(.3)), (X(-.025), Y(0)), (X(-.085), Y(0))], c, at=at)]
    aw = max(2.5, .045 * h)
    if arms is None:
        els += [ln([(X(-.12, .76), Y(.76)), (X(-.15, .46), Y(.46))], at, c, aw, draw=False), ln([(X(.12, .76), Y(.76)), (X(.15, .46), Y(.46))], at, c, aw, draw=False)]
    elif arms == "point":
        els += [ln([(X(-.12, .76), Y(.76)), (X(-.15, .46), Y(.46))], at, c, aw, draw=False), ln([(X(.1, .75), Y(.75)), (X(.42, .8), Y(.8))], at, c, aw, draw=False)]
    elif arms == "up":
        els += [ln([(X(-.12, .76), Y(.76)), (X(-.15, .46), Y(.46))], at, c, aw, draw=False), ln([(X(.1, .76), Y(.76)), (X(.2, 1.08), Y(1.08))], at, c, aw, draw=False)]
    elif arms == "pull":
        els += [ln([(X(-.1, .75), Y(.75)), (X(.3, .62), Y(.62))], at, c, aw, draw=False), ln([(X(.1, .75), Y(.75)), (X(.36, .6), Y(.6))], at, c, aw, draw=False)]
    elif arms == "lift":
        els += [ln([(X(-.1, .76), Y(.76)), (X(-.2, 1.06), Y(1.06))], at, c, aw, draw=False), ln([(X(.1, .76), Y(.76)), (X(.2, 1.06), Y(1.06))], at, c, aw, draw=False)]
    e = grp(els, at, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return [e]



# ==== SCENES ====

# ================================================================== shared drawings
def temple_icon(x, by, w, at, c=GLOB, edge=GLOB_D, fx="rise", style="known", lit=GLOB_L, op=None, door=True):
    """A Maltese temple facade in elevation: a long low wall of upright slabs with courses above, a trilithon doorway in the middle,
    a bench along its foot; width w, standing on by."""
    h = w * .34
    cl = style != "known"
    fill = "rgba(201,193,238,.16)" if cl else c
    ec = LILAC if cl else edge
    top = [(x - w / 2, by - h * .72), (x - w * .3, by - h * .9), (x - w * .1, by - h * .97), (x + w * .12, by - h), (x + w * .32, by - h * .9), (x + w / 2, by - h * .74)]
    els = [poly([(x - w / 2, by)] + top + [(x + w / 2, by)], fill, ec, 3 if cl else 2, 0, style=style)]
    if not cl:
        for k in range(1, 9):
            xx = x - w / 2 + w * k / 9
            if abs(xx - x) > w * .1:
                els += [ln([(xx, by), (xx, by - h * .5)], 0, edge, 1.4, draw=False, op=.7)]
        els += [ln([(x - w / 2, by - h * .5), (x + w / 2, by - h * .5)], 0, edge, 1.4, draw=False, op=.7),
                ln([(x - w / 2 + 4, by - h * .5), (x - w / 2 + 4, by - h * .7)], 0, lit, 2, draw=False, op=.6),
                rect(x - w / 2 - 6, by - 8, w + 12, 8, mix(c, "#000000", .25), at=0)]
    if door:
        dw, dh = w * .11, h * .52
        els += [rect(x - dw / 2, by - dh, dw, dh, "#140e0a" if not cl else "none", ec, 1.4, at=0, style=style),
                rect(x - dw * .9, by - dh - h * .1, dw * 1.8, h * .1, fill if cl else mix(c, "#ffffff", .12), ec, 1.4, at=0, style=style)]
    e = grp(els, at, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return [e]


def elephant(x, by, h, at, c="#9a938a", face=1, fx="pop"):
    """A standing elephant in profile, feet on by, height h (to the top of the back), facing `face`."""
    f = face
    X = lambda a: x + f * a * h
    Y = lambda b: by - b * h
    body = [(X(-.62), Y(.42)), (X(-.6), Y(.78)), (X(-.35), Y(.98)), (X(.15), Y(1.0)), (X(.5), Y(.9)), (X(.66), Y(.78)), (X(.78), Y(.6)),
            (X(.8), Y(.32)), (X(.86), Y(.1)), (X(.9), Y(0)), (X(.82), Y(.02)), (X(.72), Y(.3)), (X(.6), Y(.42)), (X(.5), Y(.4)), (X(.5), Y(0)),
            (X(.34), Y(0)), (X(.32), Y(.36)), (X(-.12), Y(.36)), (X(-.14), Y(0)), (X(-.3), Y(0)), (X(-.32), Y(.36)), (X(-.48), Y(.38)), (X(-.5), Y(0)),
            (X(-.62), Y(0))]
    ear = [(X(.36), Y(.86)), (X(.18), Y(.82)), (X(.14), Y(.5)), (X(.34), Y(.46)), (X(.46), Y(.62))]
    return [grp([poly(body, c, "rgba(255,240,220,.35)", 1.4, 0, curve=True), poly(ear, mix(c, "#000000", .18), "rgba(255,240,220,.25)", 1.2, 0, curve=True),
                 circ(X(.6), Y(.7), max(1.5, h * .025), "#1a1410", at=0), ln([(X(-.62), Y(.6)), (X(-.72), Y(.4))], 0, c, max(2, h * .03), draw=False)], at, fx)]


def wheel_icon(x, y, r, at, c=BONE):
    els = [circ(x, y, r, "none", c, 4, 0), circ(x, y, r * .18, c, at=0)]
    els += [ln([(x + r * math.cos(a) * .2, y + r * math.sin(a) * .2), (x + r * math.cos(a), y + r * math.sin(a))], 0, c, 3, draw=False)
            for a in [k * math.pi / 3 for k in range(6)]]
    return [grp(els, at, "pop")]


def axe_icon(x, y, s, at, c="#c9ccd2"):
    head = [(x - .1 * s, y - .42 * s), (x + .38 * s, y - .5 * s), (x + .44 * s, y - .2 * s), (x + .1 * s, y - .24 * s)]
    return [grp([ln([(x - .3 * s, y + .45 * s), (x + .05 * s, y - .38 * s)], 0, "#8a6a44", .1 * s, draw=False),
                 poly(head, c, "#ffffff", 1.5, 0)], at, "pop")]


def struck(x, y, r, at, c=RED):
    return [circ(x, y, r, "none", c, 4, at, fx="draw", dur=.4), ln([(x - r * .7, y + r * .7), (x + r * .7, y - r * .7)], at + .25, c, 4, dur=.3)]


# ---- the Maltese islands (schematic outlines drawn from the coast; lon, lat)
MALTA = [(14.329, 35.990), (14.342, 35.992), (14.357, 35.991), (14.372, 35.988), (14.378, 35.984), (14.371, 35.978), (14.360, 35.973),
         (14.356, 35.968), (14.366, 35.966), (14.380, 35.968), (14.396, 35.966), (14.398, 35.958), (14.392, 35.952), (14.400, 35.948),
         (14.414, 35.951), (14.424, 35.960), (14.428, 35.952), (14.421, 35.946), (14.432, 35.944), (14.452, 35.943), (14.470, 35.937),
         (14.484, 35.929), (14.492, 35.920), (14.503, 35.914), (14.513, 35.909), (14.508, 35.900), (14.513, 35.898), (14.520, 35.901),
         (14.516, 35.893), (14.503, 35.884), (14.512, 35.884), (14.523, 35.893), (14.533, 35.896), (14.550, 35.886), (14.567, 35.870),
         (14.560, 35.864), (14.570, 35.855), (14.566, 35.843), (14.563, 35.828), (14.553, 35.832), (14.545, 35.842), (14.538, 35.834),
         (14.530, 35.826), (14.534, 35.815), (14.528, 35.806), (14.505, 35.807), (14.478, 35.812), (14.455, 35.818), (14.440, 35.824),
         (14.420, 35.826), (14.400, 35.833), (14.382, 35.843), (14.372, 35.858), (14.360, 35.872), (14.340, 35.893), (14.334, 35.906),
         (14.338, 35.920), (14.343, 35.933), (14.337, 35.945), (14.340, 35.960), (14.330, 35.975), (14.324, 35.982)]
GOZO = [(14.191, 36.051), (14.200, 36.066), (14.219, 36.075), (14.236, 36.081), (14.249, 36.080), (14.259, 36.074), (14.272, 36.073),
        (14.285, 36.063), (14.300, 36.057), (14.318, 36.048), (14.333, 36.036), (14.320, 36.028), (14.300, 36.022), (14.283, 36.020),
        (14.268, 36.018), (14.248, 36.016), (14.228, 36.024), (14.215, 36.029), (14.203, 36.036), (14.192, 36.044)]
COMINO = [(14.323, 36.013), (14.333, 36.019), (14.346, 36.016), (14.350, 36.009), (14.338, 36.003), (14.326, 36.006)]
SITES = {"ggantija": (14.2692, 36.0473), "hagarqim": (14.4421, 35.8277), "mnajdra": (14.4361, 35.8267), "tarxien": (14.5124, 35.8691),
         "hypogeum": (14.5069, 35.8697), "skorba": (14.3812, 35.9208), "xaghra": (14.2655, 36.0490), "latnija": (14.352, 35.972),
         "stgeorge": (14.531, 35.826), "julians": (14.4956, 35.9326)}


def land_ex(v):
    """The land of the 50 m data, without its eight-point Malta and Gozo (drawn from our own outlines)."""
    lon0, lon1, lat0, lat1 = v.b
    out = []
    for poly_ in _films._topo():
        r = poly_[0]
        xs = [q[0] for q in r]; ys = [q[1] for q in r]
        if min(xs) > 14.1 and max(xs) < 14.7 and min(ys) > 35.7 and max(ys) < 36.15:
            continue
        if max(xs) < lon0 - 6 or min(xs) > lon1 + 6 or max(ys) < lat0 - 6 or min(ys) > lat1 + 6:
            continue
        pts_, last = [], None
        for lo, la in r:
            q = v.p(lo, la)
            if last and abs(q[0] - last[0]) < 1.2 and abs(q[1] - last[1]) < 1.2:
                continue
            pts_.append(q); last = q
        if len(pts_) > 3:
            out.append("M" + "L".join(f"{x} {y}" for x, y in pts_) + "Z")
    return out


def islands(v, at=-1, fill="#3a2f24", c="#c9ad85", w=1.6, op=None):
    return [poly([v.p(lo, la) for lo, la in isl], fill, c, w, at, op=op) for isl in (GOZO, COMINO, MALTA)]


def map_els(v, at=-1, malta=True):
    els = [{"k": "map", "land": land_ex(v), "in": at}]
    if malta:
        els += islands(v, at)
    return els


# ================================================================== the hero: Mnajdra's lower temple at dawn on the equinox
# A simple pinhole view down the temple's axis from its back niche: x across, y up, z along the axis (metres); eye 1 m above the floor.
VPX, VPY, FOC, EYE = 889.0, 420.0, 700.0, 1.0


def P3(x, y, z):
    """Screen point of the temple point (x, y, z)."""
    return (VPX + FOC * x / z, VPY - FOC * (y - EYE) / z)


ZF, ZN = 9.0, 2.4            # the main (far) doorway and the inner doorway, metres from the eye
DOOR_W, DOOR_H = .5, 2.2     # half-width and height of the main doorway's opening
SUN_EL = 5.0                 # the sun a few degrees up: its light lies along the floor
SUNP = (VPX, VPY - FOC * math.tan(math.radians(SUN_EL)))


def rough(p, seed, jit=3.0):
    """A stone's outline with slightly irregular corners (seeded)."""
    r = random.Random(seed)
    return [(x + r.uniform(-jit, jit), y + r.uniform(-jit, jit)) for x, y in p]


def pits(x0, y0, x1, y1, at, step=13, r=2.3, c="#0b0705", op=.55, seed=1, skip=.15):
    """Drilled-pit decoration: rows of small holes over a rectangle of a slab."""
    rr = random.Random(seed)
    out = []
    y = y0
    row = 0
    while y <= y1:
        x = x0 + (step / 2 if row % 2 else 0)
        while x <= x1:
            if rr.random() > skip:
                out.append(circ(x + rr.uniform(-1, 1), y + rr.uniform(-1, 1), r, c, at=at, op=op))
            x += step
        y += step * .86; row += 1
    return out


def beam_quad(z0, z1, w=DOOR_W):
    return [P3(-w, 0, z0), P3(w, 0, z0), P3(w, 0, z1), P3(-w, 0, z1)]


def hero_els(at=-1, beam=1.0, warm=1.0):
    """The whole picture, complete at `at` (static): sky and sun in the far doorway, the first chamber, the floor and its shaft of light,
    the inner doorway framing it all, the niche floor in the foreground."""
    els = [rect(-60, -60, 1900, 1120, "#150f0b", at=at)]
    (dl, dt), (dr, db) = P3(-DOOR_W, DOOR_H, ZF), P3(DOOR_W, 0, ZF)
    bx0, bx1 = P3(-4.5, 0, ZF)[0], P3(4.5, 0, ZF)[0]
    fy = P3(0, 0, ZF)[1]
    # --- the back wall of the first chamber (the facade's inner face): upright slabs, then corbelled courses stepping inwards
    els += [rect(bx0, 120, bx1 - bx0, fy - 118, "#2a2018", at=at), gl(VPX, fy - 90, 330, at, .32 * warm, "lamp")]
    slabsL = [(bx0, 640, 318), (640, 742, 296), (742, dl - 40, 320)]
    k = 0
    for x0, x1, top in slabsL:
        for sgn in (1, -1):
            a_, b_ = (x0, x1) if sgn == 1 else (2 * VPX - x1, 2 * VPX - x0)
            near = 1 - min(1, abs((a_ + b_) / 2 - VPX) / 360)
            pts_ = rough([(a_, fy + 3), (a_ + 2, top + 10), (a_ + (b_ - a_) * .3, top), (b_ - 3, top + 6), (b_, fy + 2)], 10 + k, 2.5)
            els += [poly(pts_, mix("#2c2219", "#4a3826", near * .8), "rgba(255,214,160,.14)", 1.2, at)]
            k += 1
    rows = [(300, 262, 0), (262, 224, 18), (224, 188, 36), (188, 152, 54), (152, 118, 72)]
    rr = random.Random(7)
    for j, (yb, yt, ins) in enumerate(rows):
        x = bx0 + ins
        while x < bx1 - ins - 10:
            w = rr.uniform(70, 130)
            x1 = min(x + w, bx1 - ins)
            near = 1 - min(1, abs((x + x1) / 2 - VPX) / 380)
            els += [poly(rough([(x, yb), (x + 1, yt), (x1 - 1, yt + 1), (x1, yb)], 50 + j * 13 + int(x), 2),
                         mix("#2b2119" if (j + int(x)) % 2 else "#261d16", "#46352a", near * .55), "rgba(255,214,160,.10)", 1, at)]
            x = x1 + 2
    # --- the sky, the land and the sun seen through the main doorway
    els += [rect(dl - 1, dt - 1, dr - dl + 2, db - dt + 2, "url(#k-sky-dawn)", at=at),
            poly([(dl - 1, VPY + 3), (dl + 18, VPY - 3), (dl + 44, VPY + 2), (dr - 16, VPY - 2), (dr + 1, VPY + 4), (dr + 1, db + 1), (dl - 1, db + 1)],
                 "#5a3c2c", at=at),
            poly([(dl - 1, VPY + 30), (dr + 1, VPY + 26), (dr + 1, db + 1), (dl - 1, db + 1)], "#3a2820", at=at),
            gl(SUNP[0], SUNP[1], 230 * warm, at, .95, "sun"), gl(SUNP[0], SUNP[1], 90, at, 1, "sun"),
            circ(SUNP[0], SUNP[1], 15, "#fff6e0", at=at),
            ln([(SUNP[0] - 120, SUNP[1]), (SUNP[0] + 120, SUNP[1])], at, "#fff1d2", 1.5, draw=False, op=.35)]
    # --- the main doorway: two jambs and a lintel, their inner edges lit
    jl = rough([(dl - 44, db + 4), (dl - 46, dt + 6), (dl, dt + 2), (dl, db)], 3, 1.5)
    jr = rough([(dr, db), (dr, dt + 2), (dr + 44, dt + 6), (dr + 46, db + 4)], 4, 1.5)
    els += [poly(jl, "#4a3826", "rgba(255,214,160,.25)", 1.2, at), poly(jr, "#4a3826", "rgba(255,214,160,.25)", 1.2, at),
            poly(rough([(dl - 58, dt - 34), (dr + 58, dt - 36), (dr + 62, dt + 2), (dl - 62, dt + 4)], 5, 2), "#4d3b2a", "rgba(255,214,160,.28)", 1.2, at),
            ln([(dl + 1, dt + 2), (dl + 1, db)], at, "#ffd9a0", 3, draw=False, op=.9), ln([(dr - 1, dt + 2), (dr - 1, db)], at, "#ffd9a0", 3, draw=False, op=.9),
            ln([(dl - 4, dt + 3), (dr + 4, dt + 3)], at, "#ffd9a0", 2, draw=False, op=.6)]
    # --- the side walls glimpsed between the back wall and the inner doorway
    ix0, ix1 = P3(-1.4, 0, ZN)[0], P3(1.4, 0, ZN)[0]
    zj = FOC * 4.5 / (VPX - ix0)
    for sgn in (-1, 1):
        a_, b_ = P3(sgn * 4.5, 3.0, zj), P3(sgn * 4.5, 3.0, ZF)
        c_, d_ = P3(sgn * 4.5, 0, ZF), P3(sgn * 4.5, 0, zj)
        els += [poly([a_, b_, c_, d_], "#211913", "rgba(255,214,160,.10)", 1, at)]
    # --- the floor of the first chamber, its joints, and the light lying along it
    ty = P3(0, 0, ZN)[1]
    els += [poly([(bx0, fy), (bx1, fy), (ix1, ty), (ix0, ty)], "#2e2319", at=at)]
    for xm in (-3.2, -2.2, -1.2, 1.2, 2.2, 3.2):
        els += [ln([P3(xm, 0, ZF), P3(xm * .62, 0, ZN)], at, "rgba(255,214,160,.08)", 1.2, draw=False)]
    for zz in (7.7, 6.5, 5.4, 4.4, 3.5, 2.8):
        els += [ln([P3(-4.6 * zz / ZF * 1.1, 0, zz), P3(4.6 * zz / ZF * 1.1, 0, zz)], at, "rgba(255,214,160,.07)", 1.2, draw=False)]
    els += [gl(VPX, fy + 40, 260, at, .45 * beam, "lamp"),
            poly(beam_quad(ZF, ZN), "#e9a85e", at=at, op=.38 * beam),
            poly(beam_quad(ZF, ZN, DOOR_W * .62), "#ffe2b0", at=at, op=.36 * beam)]
    # faint rays and dust in the air above the light
    rd = random.Random(21)
    for q in range(5):
        u = -1 + .5 * q
        a_ = P3(u * DOOR_W * .9, DOOR_H * (.25 + .15 * (q % 3)), ZF)
        b_ = P3(u * DOOR_W * .9, DOOR_H * (.25 + .15 * (q % 3)) - (ZF - ZN) * math.tan(math.radians(SUN_EL)), ZN)
        els += [ln([a_, b_], at, "#ffe7c0", 10, draw=False, op=.035 * beam)]
    for q in range(52):
        u, v = rd.uniform(.05, .95), rd.uniform(.05, .9)
        zz = ZN + .2 + (ZF - ZN - .2) * rd.random() ** 1.3
        hh = (DOOR_H - (ZF - zz) * math.tan(math.radians(SUN_EL))) * v
        x_, y_ = P3((u - .5) * 2 * DOOR_W, hh, zz)
        els += [circ(x_, y_, rd.uniform(.8, 2.4), "#fff1d2", at=at, op=rd.uniform(.25, .75) * beam)]
    # --- the inner doorway that frames the view: a threshold step, two great jambs (their inner faces in perspective), the lintel
    b1l, b1r = P3(-DOOR_W, 0, ZN), P3(DOOR_W, 0, ZN)
    els += [poly([(ix0 - 10, ty), (ix1 + 10, ty), (ix1 + 30, ty + 26), (ix0 - 30, ty + 26)], "#33271d", "rgba(255,214,160,.2)", 1.2, at),
            poly([(b1l[0] - 6, ty + 1), (b1r[0] + 6, ty + 1), (b1r[0] + 12, ty + 25), (b1l[0] - 12, ty + 25)], "#ffd09a", at=at, op=.6 * beam)]
    jw = 170
    for sgn in (-1, 1):
        x_in = P3(sgn * 1.4, 0, ZN)[0]
        x_back = P3(sgn * 1.4, 0, ZN + .55)[0]
        y_top_in, y_top_b = P3(0, 2.75, ZN)[1], P3(0, 2.75, ZN + .55)[1]
        y_bot_in, y_bot_b = P3(0, .15, ZN)[1], P3(0, .15, ZN + .55)[1]
        face = [(x_in, max(104, y_top_in)), (x_back, max(110, y_top_b)), (x_back, y_bot_b), (x_in, y_bot_in)]
        mid = [(x_in, (face[0][1] + face[3][1]) / 2), (x_back, (face[1][1] + face[2][1]) / 2), face[2], face[3]]
        els += [poly(face, "#271d16", "rgba(255,214,160,.16)", 1.2, at), poly(mid, "#3a2b1f", at=at, op=.8),
                poly([face[3], face[2], (x_back, face[2][1] - 60), (x_in, face[3][1] - 90)], "#e9a85e", at=at, op=.10 * beam)]
    JL = rough([(ix0 - jw - 30, ty + 40), (ix0 - jw, 92), (ix0 + 4, 104), (ix0, ty + 18)], 31, 3)
    JR = rough([(ix1, ty + 18), (ix1 - 4, 104), (ix1 + jw, 92), (ix1 + jw + 30, ty + 40)], 32, 3)
    els += [poly([(-60, -60), (ix0 - jw + 6, -60), (ix0 - jw - 26, 1060), (-60, 1060)], "#0e0a08", at=at),
            poly([(ix1 + jw - 6, -60), (1840, -60), (1840, 1060), (ix1 + jw + 26, 1060)], "#0e0a08", at=at),
            poly(JL, "#251c15", "rgba(255,214,160,.18)", 1.4, at), poly(JR, "#251c15", "rgba(255,214,160,.18)", 1.4, at)]
    els += pits(ix0 - jw + 26, 210, ix0 - 30, 600, at, seed=3) + pits(ix1 + 30, 210, ix1 + jw - 26, 600, at, seed=4)
    els += [ln([(ix0 + 1, 112), (ix0 + 2, ty + 14)], at, "#e9b878", 2.5, draw=False, op=.5 * beam),
            ln([(ix1 - 1, 112), (ix1 - 2, ty + 14)], at, "#e9b878", 2.5, draw=False, op=.5 * beam),
            poly(rough([(-60, -60), (1840, -60), (1840, 70), (ix1 + jw + 40, 104), (ix0 - jw - 40, 104), (-60, 70)], 33, 3), "#1b140f", "rgba(255,214,160,.16)", 1.4, at)]
    # --- the niche floor in the foreground: dark, the light running on towards us
    els += [poly([(ix0 - 30, ty + 26), (ix1 + 30, ty + 26), (ix1 + 120, 1060), (ix0 - 120, 1060)], "#1a130e", at=at),
            poly([(b1l[0] - 12, ty + 26), (b1r[0] + 12, ty + 26), P3(DOOR_W, 0, 1.2), P3(-DOOR_W, 0, 1.2)], "#e9a85e", at=at, op=.32 * beam),
            poly([(b1l[0] + 40, ty + 26), (b1r[0] - 40, ty + 26), P3(DOOR_W * .62, 0, 1.2), P3(-DOOR_W * .62, 0, 1.2)], "#ffe2b0", at=at, op=.26 * beam)]
    return els


def hero_base():
    return {"base": "dark", "cam": CAM}


def s1():
    """The hero image, complete from the first frame: inside Mnajdra's lower temple at dawn on the equinox, down the axis from the back
    niche to the main doorway, the sun in it; the shaft of light on the floor. The place name after the hook title clears."""
    els = hero_els()
    els += [lab(1560, 772, "Mnajdra, Malta", 3.6, GOLD, 30, "end", fx="pop")]
    st = hero_base(); st.update(els=els)
    return st


def s1z_add():
    """The light runs the length of the floor to the niche where we stand: bands of brighter light pop along it from the doorway to us;
    'equinox sunrise' over the doorway, 'to the niche' at our feet."""
    tr = T("s1z", "It runs down")
    (dl, dt) = P3(-DOOR_W, DOOR_H, ZF)
    zs = [ZF - (ZF - 1.6) * k / 12 for k in range(13)]
    els = [poly(beam_quad(z0, z1, DOOR_W * .8), "#fff1d2", at=round(tr + .25 + .16 * k, 2), op=.30) for k, (z0, z1) in enumerate(zip(zs, zs[1:]))]
    els += [gl(VPX, 780, 170, tr + 2.3, .5, "lamp"),
            lab(VPX, dt - 50, "equinox sunrise", tr + .5, GOLD, 30, fx="pop"),
            lab(VPX + 250, 770, "to the niche", tr + 2.4, GOLD, 28, "start", fx="pop"),
            arr([(VPX + 240, 762), (VPX + 150, 776)], tr + 2.4, GOLD, 2.5, dur=.4, curve=False)]
    return els

# ================================================================== cold open: older than the pyramids; the questions
def XT(yr, x0=180, k=.7, y0=4000):
    return round(x0 + (y0 - yr) * k, 1)


def s2():
    """A time line from 4000 to 2000 BCE drawn as a horizon: Mnajdra's lower temple (about 3000 BCE), then Ġgantija (about 3600 BCE),
    then the Great Pyramid (about 2560 BCE); a bracket 'about 1,000 years'."""
    tm, to, tg = T("s2", "This temple"), T("s2", "temples older still"), T("s2", "pyramids of Giza")
    G = 640
    els = [axis(XT(4000), XT(2000), 700, [(XT(y), "%d BCE" % y if y in (4000, 2000) else "%d" % y) for y in (4000, 3500, 3000, 2500, 2000)], .2)]
    els += temple_icon(XT(3000), G, 250, tm + .2) + [lab(XT(3000), G - 118, "Mnajdra", tm + .5, GOLD, 30, fx="pop"),
                                                   ln([(XT(3000), G + 2), (XT(3000), 690)], tm + .4, GOLD, 2, draw=False)]
    els += temple_icon(XT(3600), G, 300, to + .1, c=CORA, edge=CORA_D, lit=CORA_L) + [lab(XT(3600), G - 140, "Ġgantija", to + .4, GOLD, 30, fx="pop"),
                                                                                    ln([(XT(3600), G + 2), (XT(3600), 690)], to + .3, GOLD, 2, draw=False)]
    els += [{"k": "pyramid", "x": XT(2560), "y": G, "w": 330, "in": tg, "fx": "rise"}, gl(XT(2560), G - 120, 220, tg + .2, .25, "lamp"),
            lab(XT(2560), G - 250, "the Great Pyramid", tg + .4, BONE, 30, fx="pop"), ln([(XT(2560), G + 2), (XT(2560), 690)], tg + .3, BONE, 2, draw=False)]
    els += bracket(XT(3600), XT(2560), 330, tg + 1.0, None, GOLD, up=False) + [lab((XT(3600) + XT(2560)) / 2, 312, "about 1,000 years", tg + 1.3, GOLD, 30)]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1560, 560, 22], "ridges": [{"y": G - 12, "a": 16, "c": "#33293a", "seed": 5}], "groundc": "#3a3024",
            "cam": CAM, "els": els}


def s3_add():
    """The questions over the hero: the light dims a little; 'who?', 'when?', 'why?' rise in lilac; then 'the Ice Age?' (claimed)."""
    tw, tn, ty, ti = T("s3", "Who built them"), T("s3", "when"), T("s3", "Why did they"), T("s3", "Ice Age")
    return [rect(-60, -60, 1900, 1120, "rgba(10,8,20,.32)", at=max(0, tw - .3)),
            lab(620, 214, "who?", tw + .2, LILAC, 52, st="serif", fx="pop"), lab(889, 172, "when?", tn, LILAC, 52, st="serif", fx="pop"),
            lab(1158, 214, "why?", ty + .2, LILAC, 52, st="serif", fx="pop")] + chip(889, 610, "the Ice Age?", LILAC, ti - .3, 30)


# ================================================================== CHAPTER 1 · A place of giants
def megawall(x0, x1, base, top, at, seed=5, sunx=-1, c=CORA, cl=CORA_L, cd=CORA_D):
    """A wall of huge rough blocks in elevation, as at Ġgantija: a lower tier of great uprights and blocks, smaller courses above, the
    top ragged; lit from the side `sunx` (-1 left)."""
    r = random.Random(seed)
    els = []
    x = x0
    tier1 = base - (base - top) * .55
    while x < x1 - 20:
        w = r.uniform(70, 150)
        xb = min(x1, x + w)
        hh = (base - tier1) * r.uniform(.85, 1.25) if r.random() < .55 else (base - tier1) * r.uniform(.5, .7)
        yt = base - hh
        pts_ = rough([(x, base), (x + 3, yt + 6), (x + (xb - x) * .5, yt), (xb - 2, yt + 5), (xb, base)], int(x) + seed, 3)
        tone = mix(c, cd, r.uniform(0, .45))
        els += [poly(pts_, tone, "rgba(20,16,12,.5)", 1.4, at)]
        lx = x + 3 if sunx < 0 else xb - 3
        els += [ln([(lx, base - 6), (lx, yt + 8)], at, cl, 3, draw=False, op=.55)]
        for _ in range(4):
            els += [circ(r.uniform(x + 8, xb - 8), r.uniform(yt + 10, base - 10), r.uniform(1.5, 3.5), cd, at=at, op=.5)]
        if hh < (base - tier1) * .75:
            w2 = (xb - x)
            els += [poly(rough([(x + 2, yt - 2), (x + 4, yt - (base - tier1) * .4), (xb - 4, yt - (base - tier1) * .42), (xb - 2, yt - 2)], int(x) + 99, 3),
                         mix(c, cd, r.uniform(.1, .5)), "rgba(20,16,12,.5)", 1.4, at)]
        x = xb + 2
    y = tier1
    row = 0
    while y > top + 20:
        hh = r.uniform(45, 70)
        x = x0 + r.uniform(0, 30)
        while x < x1 - 20:
            w = r.uniform(80, 150)
            xb = min(x1, x + w)
            ragged = top + (r.uniform(-10, 40) if row > 2 else 0)
            yt = max(ragged, y - hh)
            if yt < y - 12:
                els += [poly(rough([(x, y), (x + 2, yt), (xb - 2, yt + 2), (xb, y)], int(x * 3 + y), 2.5), mix(c, cd, r.uniform(.05, .5)),
                             "rgba(20,16,12,.45)", 1.2, at)]
            x = xb + 2
        y -= hh + 2
        row += 1
    return els


def s5():
    """Ġgantija's great back wall in golden evening light, about 6 m high: rough coralline blocks, a person at its foot for scale; a gold
    dimension '6 m'; then a two-storey house in dashed outline beside it, the same height."""
    th, tt = T("s5", "six metres"), T("s5", "two-storey")
    G, K = 700, 60.0
    top = G - 6 * K
    els = megawall(380, 1400, G, top, -1, seed=5)
    els += [gl(380, 520, 300, -1, .25, "sun")]
    els += fig(1320, G, 1.7 * K, -1, "#1d1611", fx=None)
    els += [{"k": "dim", "x1": 330, "y1": G, "x2": 330, "y2": top, "t": "6 m", "c": GOLD, "in": th, "fx": "draw", "lx": -14},
            lab(880, top - 46, "Ġgantija, Gozo", .6, GOLD, 32)]
    hx0, hx1 = 1480, 1660
    els += [rect(hx0, top + 40, hx1 - hx0, 6 * K - 40, "rgba(245,236,220,.05)", BONE, 2.5, 2, tt, style="inferred", fx="pop"),
            poly([(hx0 - 10, top + 42), ((hx0 + hx1) / 2, top), (hx1 + 10, top + 42)], "none", BONE, 2.5, tt, style="inferred", fx="pop"),
            rect(hx0 + 20, top + 80, 40, 50, "none", BONE, 2, 2, tt + .2, style="inferred"), rect(hx1 - 60, top + 80, 40, 50, "none", BONE, 2, 2, tt + .2, style="inferred"),
            rect(hx0 + 20, top + 230, 40, 50, "none", BONE, 2, 2, tt + .3, style="inferred"), rect(hx1 - 60, G - 100, 40, 100, "none", BONE, 2, 2, tt + .3, style="inferred"),
            ln([(hx0, top + 190), (hx1, top + 190)], tt + .3, BONE, 2, "inferred", draw=False),
            lab((hx0 + hx1) / 2, G + 44, "two storeys", tt + .5, BONE, 28)]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [170, 560, 30], "groundc": "#3c3424",
            "ridges": [{"y": G - 20, "a": 26, "c": "#3a3040", "seed": 2}, {"y": G - 4, "a": 12, "c": "#2e2a22", "seed": 6}], "cam": CAM, "els": els}


VMT = View(14.12, 14.62, 35.77, 36.10, (150, 130, 1480, 640))


def s6():
    """Map of Gozo, Comino and Malta: pins for the temples named in the film (Ġgantija; Ħaġar Qim and Mnajdra; Tarxien and the Hypogeum;
    Skorba); 'about 30 temples'; a 5 km scale."""
    v = VMT
    t0 = T("s6", "Malta and Gozo")
    els = map_els(v)
    els += [lab(*v.p(14.245, 36.103), "Gozo", .2, DIM, 30), lab(*v.p(14.44, 35.905), "Malta", .2, DIM, 40, st="serif"),
            lab(*v.p(14.40, 36.03), "Comino", .3, DIM, 24, "start"),
            lab(*v.p(14.6, 36.02), "Mediterranean Sea", .3, SEAL, 28, st="ital")]
    px = lambda k: v.p(*SITES[k])
    els += [pin(*px("ggantija"), "Ġgantija", t0 + .2, GOLD, "end", -20, 8),
            pin(*px("skorba"), "Skorba", t0 + .5, GOLD, "end", -20, 8),
            pin(*px("hagarqim"), "Ħaġar Qim, Mnajdra", t0 + .8, GOLD, "end", -20, 30),
            pin(*px("tarxien"), "Tarxien, the Hypogeum", t0 + 1.1, GOLD, "start", 20, 8)]
    els += chip(1380, 690, "about 30 temples", GOLD, t0 + 1.6, 30)
    els += [{"k": "scale", "x": 520, "y": 760, "w": round(v.km(5), 1), "t": "5 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


def s7():
    """Ħaġar Qim's facade in honey-coloured stone with its trilithon doorway; one great slab outlined in gold, 'close to 20 t'; three
    elephants pop beside it ('3 big elephants'); then 'no metal' and 'no wheels', struck through."""
    tt, te, tm, tw = T("s7", "close to twenty"), T("s7", "three big"), T("s7", "No metal"), T("s7", "No wheels")
    G = 690
    r = random.Random(3)
    els = []
    # the facade: a row of tall uprights with a trilithon doorway, a bench along the foot, courses above
    xs = [170, 245, 330, 410, 470]
    for k, (a, b) in enumerate(zip(xs, xs[1:])):
        h = r.uniform(230, 280)
        els += [poly(rough([(a, G), (a + 2, G - h), (b - 2, G - h + 8), (b, G)], 40 + k, 3), mix(GLOB, GLOB_D, r.uniform(.05, .35)), "rgba(60,40,20,.5)", 1.4, -1),
                ln([(a + 3, G - 6), (a + 3, G - h + 6)], -1, GLOB_L, 3, draw=False, op=.6)]
    els += [rect(470, G - 300, 30, 300, mix(GLOB, GLOB_D, .2), "rgba(60,40,20,.5)", 1.4, 0, -1), rect(560, G - 300, 30, 300, mix(GLOB, GLOB_D, .2), "rgba(60,40,20,.5)", 1.4, 0, -1),
            rect(500, G - 270, 60, 270, "#1a120c", at=-1), rect(455, G - 340, 150, 42, GLOB_L, "rgba(60,40,20,.5)", 1.4, 2, -1)]
    xs = [590, 660, 745, 820]
    for k, (a, b) in enumerate(zip(xs, xs[1:])):
        h = r.uniform(230, 280)
        els += [poly(rough([(a, G), (a + 2, G - h), (b - 2, G - h + 8), (b, G)], 60 + k, 3), mix(GLOB, GLOB_D, r.uniform(.05, .35)), "rgba(60,40,20,.5)", 1.4, -1),
                ln([(a + 3, G - 6), (a + 3, G - h + 6)], -1, GLOB_L, 3, draw=False, op=.6)]
    big = rough([(825, G), (830, G - 5.2 * 52), (990, G - 5.2 * 52 + 12), (996, G)], 77, 3)
    els += [poly(big, mix(GLOB, GLOB_D, .15), "rgba(60,40,20,.5)", 1.4, -1), ln([(829, G - 8), (832, G - 260)], -1, GLOB_L, 3, draw=False, op=.6),
            rect(160, G - 24, 840, 24, mix(GLOB, GLOB_D, .45), "rgba(60,40,20,.5)", 1.2, 2, -1),
            lab(560, G - 380, "Ħaġar Qim", .5, GOLD, 32)]
    els += [ln(big + big[:1], tt, AU, 5, dur=.8), gl(910, G - 140, 170, tt + .3, .35, "lamp")] + chip(910, G - 330, "close to 20 t", AU, tt + .4, 28)
    els += [lab(1060, G - 150, "≈", te, BONE, 64, st="big", fx="pop")]
    for k in range(3):
        els += elephant(1190 + 165 * k, G, 112, te + .2 + .25 * k, "#9a938a")
    els += [lab(1355, G + 50, "3 big elephants", te + .9, BONE, 28)]
    els += axe_icon(1250, 250, 110, tm) + struck(1260, 230, 72, tm + .3) + [lab(1260, 345, "no metal", tm + .5, BONE, 28)]
    els += wheel_icon(1520, 230, 52, tw) + struck(1520, 230, 72, tw + .3) + [lab(1520, 345, "no wheels", tw + .5, BONE, 28)]
    return {"base": "sky", "tod": "day", "ground": G, "sun": False, "groundc": "#5a4a34",
            "ridges": [{"y": G - 16, "a": 18, "c": "#6f7a7c", "seed": 3}], "cam": CAM, "els": els}


def giantess(x, by, h, at, robe="#9c4a2e", scarf="#efe1c2", skin="#d8a77c", ink="#3a2414"):
    """Sansuna as a folk print: a tall woman walking right in a long robe and headscarf, a great block balanced on her head, a baby in her
    left arm. Height h to the top of the head."""
    X = lambda a: x + a * h
    Y = lambda b: by - b * h
    robe_p = [(X(-.13), Y(.0)), (X(-.1), Y(.35)), (X(-.09), Y(.62)), (X(-.07), Y(.74)), (X(.07), Y(.76)), (X(.1), Y(.62)), (X(.14), Y(.3)),
              (X(.2), Y(.0))]
    els = [poly(robe_p, robe, ink, 3, 0, curve=True),
           poly([(X(-.02), Y(.0)), (X(.06), Y(.32)), (X(.12), Y(.0))], mix(robe, "#000000", .25), ink, 2, 0),
           circ(X(.0), Y(.84), .07 * h, skin, ink, 3, 0),
           poly([(X(-.085), Y(.8)), (X(-.06), Y(.92)), (X(.03), Y(.94)), (X(.08), Y(.86)), (X(.07), Y(.78)), (X(.03), Y(.86)), (X(-.04), Y(.86)),
                 (X(-.07), Y(.74))], scarf, ink, 2.5, 0, curve=True),
           ln([(X(.06), Y(.7)), (X(.13), Y(.84)), (X(.1), Y(.95))], 0, skin, .028 * h, draw=False)]
    return [grp(els, at, "rise")]


def s8():
    """Sansuna, as a storybook print (the tale, told with affection): a giantess walks across Gozo's terraced hills towards the temple, a
    great block on her head and her baby in her arm; tiny houses for scale. 'Ġgantija: the giants' place'."""
    tp, tg, tb, tc = T("s8", "They called the place"), T("s8", "told of a giantess"), T("s8", "carried the stones"), T("s8", "with her baby")
    X0, Y0, W0, H0 = 300, 130, 1178, 660
    ink = "#3a2414"
    els = [rect(X0 - 14, Y0 - 14, W0 + 28, H0 + 28, "#e9d6ad", "#8a6a3e", 3, 8, -1),
           rect(X0, Y0, W0, H0, "#f2d39a", ink, 2, 2, -1),
           rect(X0, Y0, W0, H0 * .45, "#f6e2b4", at=-1),
           circ(X0 + W0 - 170, Y0 + 120, 46, "#f8c87a", ink, 2, -1)]
    hills = [([(X0, Y0 + 420), (X0 + 260, Y0 + 330), (X0 + 560, Y0 + 380), (X0 + 860, Y0 + 300), (X0 + W0, Y0 + 360), (X0 + W0, Y0 + H0), (X0, Y0 + H0)], "#b7a067"),
             ([(X0, Y0 + 500), (X0 + 330, Y0 + 450), (X0 + 700, Y0 + 500), (X0 + 1000, Y0 + 440), (X0 + W0, Y0 + 470), (X0 + W0, Y0 + H0), (X0, Y0 + H0)], "#8f8a52"),
             ([(X0, Y0 + 590), (X0 + 420, Y0 + 560), (X0 + 820, Y0 + 600), (X0 + W0, Y0 + 570), (X0 + W0, Y0 + H0), (X0, Y0 + H0)], "#6f7a45")]
    land = []
    for k, (pts_, c) in enumerate(hills):
        land += [poly(pts_, c, ink, 2, -1, curve=True)]
    for k in range(5):
        y = Y0 + 470 + 22 * k
        land += [ln([(X0 + 40 + 30 * k, y), (X0 + 380 - 20 * k, y - 18)], -1, ink, 1.4, draw=False, op=.4)]
    for k, (hx, hy) in enumerate(((X0 + 840, Y0 + 330), (X0 + 880, Y0 + 322), (X0 + 920, Y0 + 316), (X0 + 120, Y0 + 520), (X0 + 160, Y0 + 512))):
        land += [rect(hx, hy - 22, 30, 22, "#f6efdf", ink, 1.6, 1, -1), rect(hx + 11, hy - 12, 8, 12, ink, at=-1)]
    els += [grp(land, -1, None, clip=[X0, Y0, W0, H0])]
    tx, ty_ = X0 + 1000, Y0 + 300
    els += [poly([(tx - 70, ty_), (tx - 66, ty_ - 44), (tx + 66, ty_ - 48), (tx + 70, ty_)], "#d9c08e", ink, 2, -1),
            rect(tx - 10, ty_ - 30, 20, 30, ink, at=-1), lab(tx, ty_ + 36, "the temple", .4, ink, 24, st="ital", halo=False)]
    els += [lab(X0 + W0 / 2, Y0 + 62, "Ġgantija: the giants' place", tp - .2, ink, 38, st="serif", fx="pop", halo=False)]
    gx, gby, gh = X0 + 520, Y0 + 620, 430
    els += giantess(gx, gby, gh, tg)
    els += [grp([poly(rough([(gx - 70, gby - .94 * gh), (gx - 74, gby - 1.08 * gh), (gx + 76, gby - 1.1 * gh), (gx + 72, gby - .94 * gh)], 9, 3),
                      "#a59f92", ink, 3, 0)], tb, "pop"),
            grp([poly(E(gx + .1 * gh, gby - .62 * gh, .055 * gh, .085 * gh, 18), "#f6efdf", ink, 2.5, 0, curve=True),
                 circ(gx + .1 * gh, gby - .68 * gh, .028 * gh, "#d8a77c", ink, 2, 0)], tc, "pop"),
            lab(gx - 150, gby - 40, "Sansuna", tg + .6, ink, 32, "end", st="serif", fx="pop", halo=False),
            lab(X0 + W0 - 24, Y0 + H0 - 20, "a tale from Gozo", .6, ink, 24, "end", st="ital", halo=False)]
    return {"base": "dark", "cam": CAM, "els": els}


def boat(x, y, w, at, c="#7a5434", fx="pop"):
    """A small boat with a mast-less hull and paddlers (a Neolithic crossing, schematic)."""
    h = w * .16
    hull = [(x - w / 2, y - h * .6), (x - w * .38, y + h * .3), (x + w * .38, y + h * .3), (x + w / 2, y - h * .7), (x + w * .3, y - h * .2), (x - w * .3, y - h * .2)]
    els = [poly(hull, c, "#e7c99a", 1.5, 0, curve=True)]
    for k in range(3):
        px = x - w * .2 + w * .2 * k
        els += [circ(px, y - h * .9, h * .26, "#1d1611", at=0), ln([(px, y - h * .65), (px, y - h * .15)], 0, "#1d1611", h * .3, draw=False),
                ln([(px + h * .2, y - h * .6), (px + h * .9, y + h * .8)], 0, "#c9a070", 2, draw=False)]
    return [grp(els, at, fx)]


def hut(x, y, w, at, fx="pop"):
    h = w * .55
    return [grp([poly(E(x, y - h * .45, w / 2, h * .5, 20), "#8a6a44", "#e7c99a", 1.5, 0, curve=True),
                 poly(E(x, y - h * .82, w * .36, h * .22, 16), "#a88a5c", "#e7c99a", 1.2, 0, curve=True),
                 rect(x - w * .08, y - h * .45, w * .16, h * .45, "#1a120c", at=0)], at, fx)]


def pot(x, y, h, at, c=CLAY, fx="pop"):
    return [{"k": "vase", "x": x, "y": y, "h": h, "w": h * .7, "tone": c, "in": at, "fx": fx,
             "profile": [[0, .32], [.08, .36], [.3, .5], [.6, .5], [.85, .36], [1, .22]]}]


def s9():
    """Left: a boat crossing from south-east Sicily to Malta ('from Sicily'); below, a village of oval huts and pots. Right: a great slab
    sliding on stone balls, people hauling and levering; an inset tray on marbles (dashed: 'may have')."""
    tf, tv, tb, tm = T("s9", "farmers whose"), T("s9", "the villages"), T("s9", "stone balls"), T("s9", "like marbles")
    v = View(13.9, 15.4, 35.72, 37.05, (90, 140, 640, 400))
    els = [rect(80, 130, 660, 420, "rgba(14,24,32,.9)", "rgba(159,208,255,.25)", 2, 14, -1)]
    els += [{"k": "map", "land": land_ex(v), "in": -1}] + islands(v)
    els += [lab(*v.p(14.6, 37.0), "Sicily", .3, DIM, 26), lab(*v.p(14.05, 35.9), "Malta", .3, DIM, 26)]
    a_, b_ = v.p(14.75, 36.72), v.p(14.42, 36.02)
    els += [arr([a_, ((a_[0] + b_[0]) / 2 - 30, (a_[1] + b_[1]) / 2), b_], tf, GOLD, 3, "inferred", 1.2)]
    els += boat((a_[0] + b_[0]) / 2 - 30, (a_[1] + b_[1]) / 2 - 10, 80, tf + .6)
    els += [lab((a_[0] + b_[0]) / 2 + 60, (a_[1] + b_[1]) / 2 - 40, "from Sicily", tf + .8, GOLD, 28, "start")]
    G1 = 760
    els += [ln([(110, G1), (720, G1)], tv - .2, "#8c7152", 3, draw=False)]
    for k, (hx, w) in enumerate(((180, 110), (300, 130), (430, 100))):
        els += hut(hx, G1, w, tv + .2 * k)
    els += pot(560, G1, 60, tv + .7) + pot(630, G1, 46, tv + .9, CLAY_D)
    els += [lab(400, 600, "villages and pottery", tv + 1.0, BONE, 26)]
    # the slab on its rollers
    G = 690
    els += [ln([(780, G + 2), (1700, G + 2)], -1, "#8c7152", 3, draw=False)]
    els += [circ(880 + 62 * k, G - 22, 22, "#cbbca8", "#6f5a44", 2, -1, op=.3) for k in range(7)]
    els += [poly(rough([(840, G - 44), (850, G - 160), (1300, G - 170), (1310, G - 44)], 12, 4), mix(CORA, CORA_D, .2), "rgba(20,16,12,.6)", 2, -1, op=.3)]
    for k in range(7):
        els += [circ(880 + 62 * k, G - 22, 22, "#cbbca8", "#6f5a44", 2, tb + .1 * k, fx="pop")]
    els += [poly(rough([(840, G - 44), (850, G - 160), (1300, G - 170), (1310, G - 44)], 12, 4), mix(CORA, CORA_D, .2), "rgba(20,16,12,.6)", 2, tb + .7, fx="rise")]
    for k in range(5):
        els += fig(1380 + 58 * k, G, 92, tb + 1.0 + .12 * k, "#1d1611", arms="pull", lean=.12)
    els += [ln([(1310, G - 110), (1360 + 58 * 4 + 20, G - 60)], tb + 1.0, "#c9a070", 3, draw=False)]
    els += fig(800, G, 92, tb + 1.4, "#1d1611", arms="pull", face=1) + [ln([(780, G - 20), (850, G - 120)], tb + 1.4, "#8a6a44", 6, draw=False)]
    bx, by_ = 1370, 160
    els += [rect(bx, by_, 300, 190, "rgba(18,13,10,.85)", BONE, 2, 12, tm - .2, style="inferred", fx="pop"),
            rect(bx + 50, by_ + 60, 200, 40, "#8a6a44", BONE, 2, 4, tm, style="inferred")] + \
           [circ(bx + 70 + 32 * k, by_ + 116, 13, "#cbbca8", BONE, 1.5, tm + .1, style="inferred") for k in range(6)] + \
           [arr([(bx + 120, by_ + 40), (bx + 200, by_ + 40)], tm + .4, BONE, 2.5, "inferred", .5, False),
            lab(bx + 150, by_ + 168, "may have", tm + .6, BONE, 24, st="ital")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def apse(cx, cy, rx, ry, a0, a1, at, c=GLOB_L, w=16):
    return ln(E(cx, cy, rx, ry, 30, a0, a1), at, c, w, dur=.7, curve=True)


def s10():
    """Plan of Ġgantija's south temple from above: the concave facade and doorway at the bottom, the central passage, five rounded rooms
    opening off it, one pair at a time; a faint clover drawn over it in gold dashes; a 10 m scale."""
    t0, tc = T("s10", "Inside, rounded"), T("s10", "clover")
    cx = 889
    els = [poly([(560, 760), (700, 712), (889, 700), (1078, 712), (1218, 760)], "none", GLOB_L, 16, .2, curve=True),
           rect(860, 600, 58, 120, "#2b2219", at=.3), ln([(860, 712), (860, 600)], .3, GLOB_L, 12, draw=False), ln([(918, 712), (918, 600)], .3, GLOB_L, 12, draw=False)]
    els += [apse(760, 560, 150, 90, 70, 300, t0 + .3), apse(1018, 560, 150, 90, -120, 110, t0 + .3),
            apse(760, 390, 150, 95, 60, 300, t0 + 1.0), apse(1018, 390, 150, 95, -120, 120, t0 + 1.0),
            apse(889, 250, 110, 80, 160, 380, t0 + 1.6)]
    els += [ln([(cx, 700), (cx, 270)], t0 + .2, GOLD, 3, "inferred", .8),
            lab(1240, 470, "five rounded rooms", t0 + 2.0, BONE, 30, "start")]
    clover = []
    for k, ang in enumerate((-90, -18, 54, 126, 198)):
        a = math.radians(ang)
        clover += [poly(E(cx + 150 * math.cos(a), 470 + 150 * math.sin(a), 100, 100, 24), "rgba(242,201,142,.05)", GOLD, 2.5, tc, style="inferred", curve=True)]
    els += clover + [lab(560, 200, "like a clover", tc + .3, GOLD, 30, "end")]
    els += [{"k": "scale", "x": 1280, "y": 740, "w": 150, "t": "about 10 m", "in": .6}, dot(889, 650, 7, BONE, .6)]
    return {"base": "plan", "bg": "#2b2219", "north": [1640, 200], "cam": CAM, "els": els}


def spiral(cx, cy, r, turns, at, c, w=6, rot=0.0, dur=1.0, flip=1):
    pts_ = []
    n = int(36 * turns)
    for k in range(n + 1):
        t = k / n
        a = rot + flip * 2 * math.pi * turns * t
        rr = r * (1 - t) + 4
        pts_.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return ln(pts_, at, c, w, dur=dur, curve=True)


def goat(x, y, s, at, c, face=1):
    f = face
    X = lambda a: x + f * a * s
    Y = lambda b: y - b * s
    p = [(X(-.5), Y(.35)), (X(-.45), Y(.6)), (X(.3), Y(.62)), (X(.45), Y(.8)), (X(.6), Y(.82)), (X(.62), Y(.7)), (X(.48), Y(.55)), (X(.4), Y(.3)),
         (X(.38), Y(0)), (X(.3), Y(0)), (X(.26), Y(.28)), (X(-.3), Y(.28)), (X(-.34), Y(0)), (X(-.42), Y(0)), (X(-.46), Y(.3))]
    horn = [(X(.46), Y(.8)), (X(.36), Y(1.0)), (X(.24), Y(.98))]
    return [poly(p, c, "rgba(60,40,20,.6)", 1.6, at), ln(horn, at, c, max(2, s * .05), curve=True, draw=False)]


def seated(x, by, h, at, c=GLOB, edge=GLOB_D, fx="rise", head=False):
    """A seated temple figure: vast rounded hips and thighs, legs folded to one side, a pleated skirt, small feet; the neck ends in a
    socket where a separate head fitted."""
    X = lambda a: x + a * h
    Y = lambda b: by - b * h
    body = [(X(-.5), Y(.05)), (X(-.55), Y(.3)), (X(-.42), Y(.46)), (X(-.18), Y(.52)), (X(-.15), Y(.78)), (X(-.08), Y(.9)), (X(.08), Y(.9)),
            (X(.15), Y(.78)), (X(.2), Y(.52)), (X(.46), Y(.44)), (X(.58), Y(.26)), (X(.52), Y(.05))]
    els = [rect(X(-.62), Y(.05), 1.24 * h, .1 * h, mix(c, edge, .4), "rgba(60,40,20,.6)", 1.4, 6, 0),
           poly(body, c, "rgba(60,40,20,.7)", 2, 0, curve=True)]
    for k in range(7):
        xx = -.4 + .13 * k
        els += [ln([(X(xx), Y(.46 - .02 * abs(k - 3))), (X(xx + .02), Y(.08))], 0, edge, 1.6, draw=False, op=.7)]
    els += [poly(E(X(-.02), Y(.6), .1 * h, .12 * h, 14), mix(c, "#ffffff", .1), "rgba(60,40,20,.5)", 1.2, 0, curve=True),
            ln([(X(.14), Y(.72)), (X(.2), Y(.52)), (X(.06), Y(.46))], 0, edge, 2.2, curve=True, draw=False),
            poly(E(X(.42), Y(.08), .07 * h, .035 * h, 12), mix(c, edge, .2), "rgba(60,40,20,.6)", 1.2, 0, curve=True),
            poly(E(X(.0), Y(.9), .055 * h, .02 * h, 12), "#140e0a", "rgba(60,40,20,.6)", 1.2, 0, curve=True)]
    return [grp(els, at, fx)]


def s11():
    """Three carvings lit by lamps: a slab of running spirals in relief (Tarxien), a frieze of goats and pigs, and a seated figure with
    vast rounded hips and a socket for its head ('seated figure'); a lilac 'man or woman?'."""
    ts, ta, tf, tq = T("s11", "carved spirals"), T("s11", "and animals"), T("s11", "seated figures"), T("s11", "no clear sign")
    els = [gl(360, 420, 300, -1, .35, "lamp"), gl(880, 440, 300, -1, .3, "lamp"), gl(1420, 460, 320, -1, .35, "lamp")]
    els += [rect(160, 300, 400, 250, mix(GLOB, GLOB_D, .25), "rgba(60,40,20,.7)", 2, 6, ts - .3, fx="pop")]
    for k, (cx, cy, fl) in enumerate(((260, 425, 1), (360, 425, -1), (460, 425, 1))):
        els += [spiral(cx + 3, cy + 3, 46, 2.2, ts + .2 * k, GLOB_D, 9, k * 1.4, .9, fl), spiral(cx, cy, 46, 2.2, ts + .2 * k, GLOB_L, 6, k * 1.4, .9, fl)]
    els += [lab(360, 600, "spirals", ts + .5, BONE, 28)]
    els += [rect(640, 360, 480, 170, mix(GLOB, GLOB_D, .25), "rgba(60,40,20,.7)", 2, 6, ta - .3, fx="pop")]
    for k, x in enumerate((720, 840, 960, 1070)):
        els += [grp(goat(x, 500, 92, 0, GLOB_L, 1), ta + .15 * k, "pop")]
    els += [lab(880, 600, "animals", ta + .5, BONE, 28)]
    els += seated(1420, 700, 360, tf)
    els += [lab(1420, 750, "seated figure", tf + .4, BONE, 28), lab(1640, 280, "man or woman?", tq, LILAC, 30, "end", st="serif", fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s12_add():
    """At Ġgantija's wall again: a row of people gathers along its foot, hands raised to the stones."""
    th = T("s12", "by ordinary")
    els = [gl(880, 640, 380, th - .5, .3, "sun")]
    for k in range(9):
        x = 450 + 100 * k
        els += fig(x, 700, 100 + (k % 3) * 4, round(th - .4 + .12 * k, 2), "#1d1611", arms="lift" if k % 2 == 0 else "up", face=1 if k % 2 else -1)
    return els


# ================================================================== CHAPTER 2 · Older than the pyramids
VMED = View(10.2, 25.2, 33.6, 40.6, (90, 150, 1600, 610))


def spiral_pair(cx, cy, r, at, c, w=6, shade=None, dur=.9):
    """A Tarxien-style pair of opposed spirals joined by an S stem (relief): left curls one way, right the other."""
    out = []
    if shade:
        out += [spiral(cx - r * 1.05 + 3, cy + 3, r, 2.1, at, shade, w + 3, 0.0, dur, 1), spiral(cx + r * 1.05 + 3, cy + 3, r, 2.1, at + .15, shade, w + 3, math.pi, dur, 1)]
    out += [spiral(cx - r * 1.05, cy, r, 2.1, at, c, w, 0.0, dur, 1), spiral(cx + r * 1.05, cy, r, 2.1, at + .15, c, w, math.pi, dur, 1)]
    return out


def s13():
    """The old view: a map from Malta to Greece; a Tarxien spiral slab by Malta and a Mycenae grave stele with spirals by Greece, joined by
    '≈'; 'about 1600 BCE'; then lilac dotted arrows from the east to Malta and a lilac 'about 2000 BCE?'."""
    v = VMED
    ts, tm, td, tl = T("s13", "Their carved spirals"), T("s13", "royal graves at"), T("s13", "from about"), T("s13", "So the last")
    els = map_els(v, malta=False) + islands(v)
    els += [lab(*v.p(14.0, 37.75), "Sicily", -1, DIM, 26), lab(*v.p(22.2, 39.4), "Greece", -1, DIM, 26)]
    mx, my = v.p(14.45, 35.88)
    kx, ky = v.p(22.756, 37.731)
    els += [circ(mx, my, 9, GOLD, "#1d1611", 2, -1), circ(kx, ky, 9, BONE, "#1d1611", 2, -1)]
    # Tarxien: a honey stone slab with a pair of spirals, lower left by Malta
    X1, Y1 = 150, 560
    els += [rect(X1, Y1, 330, 150, mix(GLOB, GLOB_D, .2), "rgba(60,40,20,.7)", 2, 6, ts - .2, fx="pop")]
    els += spiral_pair(X1 + 165, Y1 + 75, 44, ts + .1, GLOB_L, 6, GLOB_D)
    els += [lab(X1 + 165, Y1 + 196, "Tarxien, Malta", ts + .4, GOLD, 28), ln([(X1 + 330, Y1 + 40), (mx - 12, my + 6)], ts + .3, GOLD, 1.5, "inferred", .5)]
    # Mycenae: a grave stele (grey) with running spirals, upper right by Greece
    X2, Y2 = 1350, 170
    els += [rect(X2, Y2, 300, 230, "#7d7a74", "rgba(20,18,16,.7)", 2, 6, tm - .2, fx="pop")]
    for k in range(2):
        els += spiral_pair(X2 + 150, Y2 + 70 + 92 * k, 30, tm + .1 + .2 * k, "#cfcac0", 5, "#4a4743", .8)
    els += [lab(X2 + 150, Y2 + 268, "Mycenae, Greece", tm + .4, BONE, 28), ln([(X2, Y2 + 200), (kx + 10, ky - 8)], tm + .3, BONE, 1.5, "inferred", .5),
            ln([(X1 + 300, Y1 - 10), (760, 330), (X2 - 20, Y2 + 120)], tm + .6, GOLD, 2.5, "inferred", 1.0, curve=True),
            lab(830, 318, "≈", tm + 1.2, GOLD, 64, st="big", fx="pop")]
    els += chip(X2 + 150, Y2 + 320, "about 1600 BCE", BONE, td + .2, 28)
    # the old view: influence from the east (claimed), and the date it gave Malta
    ex = [v.p(22.4, 36.6), v.p(25.0, 35.2), v.p(20.6, 34.4)]
    for k, (a_x, a_y) in enumerate(ex):
        els += [arr([(a_x, a_y), ((a_x + mx) / 2, (a_y + my) / 2 - 40 + 30 * k), (mx + 18, my - 4 + 8 * (k - 1))], tl + .1 + .25 * k, LILAC, 3, "claimed", 1.0)]
    els += chip(mx, my + 64, "about 2000 BCE?", LILAC, tl + .9, 28)
    return {"base": "map", "cam": CAM, "els": els}


def s18_add():
    """The arrows from the east struck; Malta glows gold: 'invented here'."""
    v = VMED
    t0, ti = T("s18", "Not copies"), T("s18", "invented")
    mx, my = v.p(14.45, 35.88)
    els = []
    for k, (lo, la) in enumerate(((18.5, 36.2), (19.4, 35.5), (17.6, 35.1))):
        x, y = v.p(lo, la)
        els += cross(x, y, t0 + .2 + .2 * k, RED, 1.2, 5)
    els += [ln([(mx - 110, my + 74), (mx + 110, my + 50)], t0 + .5, RED, 5, dur=.3),
            gl(mx, my, 220, ti - .4, .8, "sun"), circ(mx, my, 14, AU, "#fff1d2", 2, ti - .3, fx="pop"),
            lab(mx + 30, my - 34, "invented here", ti, AU, 32, "start", st="serif", fx="pop")]
    return els


def hourglass_outline(cx, top, bot, w, at, c=BONE):
    mid = (top + bot) / 2
    L_ = [(cx - w / 2, top), (cx - w / 2, top + 30), (cx - 26, mid - 18), (cx - 26, mid + 18), (cx - w / 2, bot - 30), (cx - w / 2, bot)]
    R_ = [(2 * cx - x, y) for x, y in L_]
    return [poly(L_ + R_[::-1], "rgba(200,225,240,.06)", c, 3, at, curve=False),
            rect(cx - w / 2 - 30, top - 22, w + 60, 22, "#6e4a2c", "#c9a070", 2, 4, at), rect(cx - w / 2 - 30, bot, w + 60, 22, "#6e4a2c", "#c9a070", 2, 4, at)]


def s14():
    """Radiocarbon as an hourglass: a living branch holds glowing radiocarbon; after death the sand runs down at a steady pace (top strips
    vanish, the pile grows); a piece of charcoal and a bone are measured: 'years since death'."""
    t0, tl, ta, th, tm = T("s14", "Then came"), T("s14", "Every living"), T("s14", "after death"), T("s14", "like sand"), T("s14", "Measure")
    tw = T("s14", "when it died")
    els = [lab(889, 180, "radiocarbon", t0 + .1, GOLD, 40, st="serif", fx="pop")]
    # left: a living olive branch with radiocarbon specks
    bx, by_ = 300, 640
    branch = [ln([(bx - 140, by_), (bx - 40, by_ - 120), (bx + 40, by_ - 260), (bx + 110, by_ - 360)], -1, "#8a6a44", 12, draw=False, curve=True),
              ln([(bx - 40, by_ - 120), (bx - 130, by_ - 230)], -1, "#8a6a44", 7, draw=False), ln([(bx + 40, by_ - 260), (bx + 140, by_ - 250)], -1, "#8a6a44", 6, draw=False)]
    leaves = []
    rr = random.Random(4)
    for k in range(22):
        t = k / 21
        x = bx - 120 + 250 * t + rr.uniform(-40, 40)
        y = by_ - 80 - 300 * t + rr.uniform(-40, 40)
        leaves.append(poly(E(x, y, 26, 9, 12), "#6f8a4a", "#a8c27a", 1, -1, curve=True))
    els += branch + leaves
    for k in range(16):
        x, y = bx - 100 + rr.uniform(0, 230), by_ - 60 - rr.uniform(0, 300)
        els += [circ(x, y, 6, AU, at=tl + .1 + .06 * k, fx="pop"), gl(x, y, 18, tl + .1 + .06 * k, .7, "sun")]
    els += [lab(bx, by_ + 50, "alive: takes in carbon", tl + .4, BONE, 26)]
    # centre: the hourglass, draining after death
    cx, top, bot, w = 889, 250, 720, 230
    mid = (top + bot) / 2
    els += hourglass_outline(cx, top, bot, w, -1)
    strips = 10
    for k in range(strips):            # the top sand, in strips from the neck up
        y0 = mid - 22 - (k + 1) * 17
        hw = 26 + (w / 2 - 30) * min(1, (mid - 18 - y0) / (mid - 18 - top - 30))
        els += [rect(cx - hw + 4, y0, 2 * hw - 8, 17.5, "#e2b98c", at=-1)]
    for k in range(strips):            # ...vanishing from the top down, steadily
        y0 = mid - 22 - (strips - k) * 17
        hw = 26 + (w / 2 - 30) * min(1, (mid - 18 - y0) / (mid - 18 - top - 30))
        els += [rect(cx - hw + 2, y0 - 1, 2 * hw - 4, 19.5, "#18120e", at=round(ta + .1 + .45 * k, 2))]
    for k in range(strips):            # the pile below grows
        hh = 14 * (k + 1)
        els += [poly([(cx - w / 2 + 6, bot - 2), (cx - 6 - 60 * (1 - k / strips), bot - hh), (cx + 6 + 60 * (1 - k / strips), bot - hh), (cx + w / 2 - 6, bot - 2)],
                     "#e2b98c", at=round(ta + .1 + .45 * k, 2))]
    els += [ln([(cx, mid - 18), (cx, bot - 4)], ta, "#e2b98c", 3, dur=.4, op=.8), lab(cx, bot + 62, "after death: a steady pace", ta + .3, BONE, 26)]
    els += [gl(cx, mid, 260, th, .3, "lamp")]
    # right: charcoal and bone, measured
    els += [poly(blob(1330, 470, 70, 40, 14, .2, 3), "#1a1714", "#6a625a", 2, tm, fx="pop"),
            poly([(1440, 520), (1460, 500), (1600, 470), (1625, 480), (1630, 455), (1652, 470), (1640, 495), (1612, 495), (1470, 530), (1450, 548)], "#efe6d2", "#b8a888", 2, tm + .2, fx="pop"),
            lab(1330, 560, "charcoal", tm + .3, DIM, 26), lab(1545, 590, "bone", tm + .4, DIM, 26)]
    els += [circ(1450, 330, 70, "rgba(18,13,10,.9)", BONE, 3, tm + .5, fx="pop"), ln([(1450, 330), (1490, 290)], tm + .9, AU, 4, dur=.4)]
    els += chip(1450, 690, "how long since it died", AU, tw - .2, 28)
    return {"base": "dark", "stars": 24, "cam": CAM, "els": els}


def coin(x, y, r, at):
    return [circ(x, y, r, "#e8c35a", "#8a6a2a", 2, at, fx="pop"), circ(x, y, r * .62, "none", "#8a6a2a", 1.5, at)]


def s15():
    """Sealed under the floor: a cross-section of a temple floor with its wall; below it charcoal and bone, 'sealed below: older'; a paving
    stone lifted on a coin; then at Skorba the oval footings of an older village under the temple wall."""
    t0, to, tc, tk, tv = T("s15", "anything sealed"), T("s15", "is older than"), T("s15", "like a coin"), T("s15", "At Skorba"), T("s15", "older village")
    G = 400
    els = [rect(-60, G, 1900, 140, "#6e573f", at=-1), rect(-60, G + 140, 1900, 140, "#4f3f2e", at=-1), rect(-60, G + 280, 1900, 200, "#352a20", at=-1),
           ln([(-60, G + 140), (1840, G + 140)], -1, "rgba(255,226,190,.18)", 1.2, draw=False), ln([(-60, G + 280), (1840, G + 280)], -1, "rgba(255,226,190,.18)", 1.2, draw=False)]
    # the floor and the wall standing on it
    for k in range(9):
        x = 360 + 120 * k
        els += [poly(rough([(x, G - 2), (x + 116, G - 2), (x + 116, G + 18), (x, G + 18)], 70 + k, 1.5), mix(GLOB, GLOB_L, .3), "rgba(60,40,20,.6)", 1.2, t0, fx="rise")]
    for k, (x, h) in enumerate(((420, 250), (530, 270), (640, 240))):
        els += [poly(rough([(x, G - 2), (x + 3, G - h), (x + 100, G - h + 6), (x + 104, G - 2)], 90 + k, 3), mix(GLOB, GLOB_D, .2), "rgba(60,40,20,.6)", 1.4, t0 + .3, fx="rise")]
    els += [lab(1000, G - 30, "temple floor", t0 + .5, BONE, 28)]
    # charcoal and bone sealed below
    rr = random.Random(8)
    for k in range(14):
        x, y = rr.uniform(780, 1340), rr.uniform(G + 40, G + 120)
        els += [circ(x, y, rr.uniform(4, 8), "#151210", at=round(to + .05 * k, 2), fx="pop")]
    els += [poly([(900, G + 90), (960, G + 80), (1000, G + 92), (950, G + 100)], "#efe6d2", "#b8a888", 1.5, to + .4, fx="pop"),
            gl(1060, G + 80, 200, to + .3, .5, "lamp"),
            lab(1060, G + 170, "sealed below: older", to + .6, AU, 30),
            arr([(1240, G + 60), (1240, G - 10)], to + .8, AU, 3, dur=.5, curve=False)]
    # the coin under a paving stone (inset)
    ix, iy = 1380, 150
    els += [rect(ix, iy, 300, 200, "rgba(18,13,10,.9)", BONE, 2, 12, tc - .2, fx="pop"),
            poly([(ix + 60, iy + 120), (ix + 240, iy + 104), (ix + 244, iy + 82), (ix + 64, iy + 98)], "#9a8a72", "#e9dccb", 1.5, tc, fx="pop"),
            ln([(ix + 30, iy + 150), (ix + 270, iy + 150)], tc, "#8c7152", 2, draw=False)] + coin(ix + 150, iy + 140, 14, tc + .3) + \
           [lab(ix + 150, iy + 186, "a coin under a stone", tc + .4, BONE, 24)]
    # Skorba: the older village beneath
    els += [lab(220, G + 200, "Skorba", tk, GOLD, 32, "start", st="serif", fx="pop")]
    for k, (x, rx) in enumerate(((620, 90), (860, 110), (1130, 80))):
        els += [ln(E(x, G + 330, rx, 26, 26, 180, 360), tk + .3 + .25 * k, "#cbbca8", 9, dur=.6, curve=True),
                ln(E(x, G + 330, rx, 26, 26, 0, 180), tk + .35 + .25 * k, "#8c7a64", 6, dur=.6, curve=True, op=.7)]
    els += [lab(1250, G + 342, "an older village", tv, GOLD, 30, "start", fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def s16():
    """The flaw and the fix: the air's radiocarbon changing over the ages (a wavy line); a tree trunk whose rings light up one a year from
    the bark inwards, 'thousands of years'; a clock hand turned back, 'corrected'."""
    tf, ta, tr, tc, tk = T("s16", "had a flaw"), T("s16", "the amount of"), T("s16", "Tree rings"), T("s16", "counted back"), T("s16", "correct the clock")
    els = [ln([(160, 330), (1640, 330)], -1, "rgba(245,236,220,.25)", 2, draw=False),
           lab(160, 190, "radiocarbon in the air", ta, AMBER, 28, "start")]
    pts = [(160 + 1480 * k / 120, 300 - 55 * math.sin(k / 9.0) - 25 * math.sin(k / 3.7 + 1)) for k in range(121)]
    els += [ln(pts, ta + .2, AMBER, 4, dur=2.4, curve=True)]
    els += [lab(900, 250, "?", tf, LILAC, 54, st="big", fx="pop")]
    # the trunk
    cx, cy = 560, 590
    els += [poly(blob(cx, cy, 200, 170, 30, .04, 2), "#8a6a44", "#c9a070", 3, tr - .2, fx="pop")]
    for k in range(26):
        rx, ry = 190 - 7 * k, 160 - 5.8 * k
        els += [ln(E(cx, cy, rx, ry, 40), round(tr + .1 + .1 * k, 2), "#e2c08c" if k % 4 == 0 else "#a8845a", 2.2 if k % 4 == 0 else 1.4, dur=.25, curve=True)]
    els += [lab(cx, 420 - 10 + 10, "one ring a year", tr + .6, BONE, 28), lab(cx, cy + 210, "counted back thousands of years", tc, BONE, 26)]
    # the clock, turned back
    kx, ky = 1300, 590
    els += [circ(kx, ky, 150, "rgba(18,13,10,.9)", BONE, 4, tk - .4, fx="pop")]
    for k in range(12):
        a = 2 * math.pi * k / 12
        els += [ln([(kx + 128 * math.cos(a), ky + 128 * math.sin(a)), (kx + 142 * math.cos(a), ky + 142 * math.sin(a))], tk - .3, BONE, 3, draw=False)]
    els += [ln([(kx, ky), (kx + 96, ky - 30)], tk - .2, BONE, 6, draw=False),
            arr([(kx + 150 * math.cos(-.5), ky + 150 * math.sin(-.5)), (kx + 175 * math.cos(-1.6), ky + 175 * math.sin(-1.6)), (kx + 170 * math.cos(-2.6), ky + 170 * math.sin(-2.6))], tk + .1, AU, 4, dur=.8),
            lab(kx, ky + 205, "corrected", tk + .6, AU, 30, fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def lion_gate(x, by, s, at):
    """Mycenae's Lion Gate, schematic: two jambs, a lintel, the relieving triangle with two rampant lions and a column."""
    c, e = "#9a948a", "#3a3530"
    els = [rect(x - .5 * s, by - .62 * s, .2 * s, .62 * s, c, e, 1.4, 1, 0), rect(x + .3 * s, by - .62 * s, .2 * s, .62 * s, c, e, 1.4, 1, 0),
           rect(x - .56 * s, by - .74 * s, 1.12 * s, .12 * s, c, e, 1.4, 1, 0), rect(x - .3 * s, by - .62 * s, .6 * s, .62 * s, "#120e0b", at=0),
           poly([(x - .42 * s, by - .74 * s), (x, by - 1.12 * s), (x + .42 * s, by - .74 * s)], mix(c, "#ffffff", .1), e, 1.4, 0),
           ln([(x, by - .76 * s), (x, by - 1.02 * s)], 0, e, 3, draw=False),
           poly([(x - .3 * s, by - .76 * s), (x - .08 * s, by - .98 * s), (x - .04 * s, by - .8 * s)], mix(c, "#000000", .2), at=0),
           poly([(x + .3 * s, by - .76 * s), (x + .08 * s, by - .98 * s), (x + .04 * s, by - .8 * s)], mix(c, "#000000", .2), at=0)]
    return [grp(els, at, "rise")]


def tiny_trilithon(x, by, s, at, c="#a39a8c"):
    e = "rgba(30,25,20,.6)"
    return [grp([rect(x - .42 * s, by - s, .26 * s, s, c, e, 1.4, 2, 0), rect(x + .16 * s, by - s, .26 * s, s, c, e, 1.4, 2, 0),
                 rect(x - .5 * s, by - 1.16 * s, s, .17 * s, mix(c, "#ffffff", .08), e, 1.4, 2, 0),
                 rect(x - 1.0 * s, by - .8 * s, .3 * s, .8 * s, mix(c, "#000000", .15), e, 1.2, 2, 0, op=.8),
                 rect(x + .7 * s, by - .8 * s, .3 * s, .8 * s, mix(c, "#000000", .15), e, 1.2, 2, 0, op=.8)], at, "rise")]


def XR(yr):
    return round(160 + (4000 - yr) * .5615, 1)


def s17():
    """Renfrew, 1973: a time line from 4000 to 1400 BCE; the old guess ('2000 BCE?', lilac) struck; the band of Malta's temples as dated
    today, 3600 to 2500 BCE; then, as named, Mycenae (1600), Stonehenge's great stones (about 2500) and the Great Pyramid (about 2560),
    each on a leader to its date; 'about 1,000 years' from 3600 to the pyramid."""
    t0, tt, tb, tm, ts, tp = (T("s17", "the archaeologist"), T("s17", "as dated today"), T("s17", "began around"), T("s17", "before Mycenae"),
                              T("s17", "great stones"), T("s17", "thousand years"))
    A = 690
    els = [axis(XR(4000), XR(1400), A, [(XR(y), "%d BCE" % y if y in (4000, 1500) else "%d" % y) for y in (4000, 3500, 3000, 2500, 2000, 1500)], -1)]
    els += [ln([(XR(2000), A - 4), (XR(2000), 560)], -1, LILAC, 2.5, "claimed", draw=False), lab(XR(2000), 545, "2000 BCE?", -1, LILAC, 26)]
    els += chip(330, 200, "1973: Colin Renfrew", BONE, t0 + .2, 28)
    els += [ln([(XR(2000) - 70, 552), (XR(2000) + 70, 530)], tt, RED, 4, dur=.3)]
    els += [{"k": "band", "x0": XR(3600), "x1": XR(2500), "y": 620, "h": 22, "c": AU, "in": tb, "dur": .8}]
    els += temple_icon(XR(3600), 470, 190, tb + .2, c=GLOB, edge=GLOB_D, lit=GLOB_L) + \
           [lab(XR(3600), 515, "Malta's temples", tb + .5, AU, 30, fx="pop"), ln([(XR(3600), 476), (XR(3600), 616)], tb + .4, AU, 2, draw=False)]
    # leaders
    for x_icon, yr, t_, c_ in ((1470, 1600, tm, BONE), (1180, 2500, ts, BONE)):
        els += [ln([(x_icon, 480), (x_icon, 520), (XR(yr), 600), (XR(yr), A - 6)], t_ + .2, c_, 1.6, "inferred", .5)]
    els += lion_gate(1470, 470, 190, tm) + [lab(1470, 236, "Mycenae", tm + .3, BONE, 28, fx="pop")]
    els += tiny_trilithon(1180, 470, 130, ts) + [lab(1180, 285, "Stonehenge", ts + .3, BONE, 28, fx="pop")]
    els += [{"k": "pyramid", "x": 900, "y": 470, "w": 250, "in": tp - .6, "fx": "rise"}, lab(900, 285, "the Great Pyramid", tp - .3, BONE, 28, fx="pop"),
            ln([(900, 480), (900, 520), (XR(2560), 600), (XR(2560), A - 6)], tp - .4, BONE, 1.6, "inferred", .5)]
    els += bracket(XR(3600), XR(2560), 590, tp + .2, None, AU, up=False) + [lab((XR(3600) + XR(2560)) / 2 + 30, 576, "about 1,000 years", tp + .5, AU, 28)]
    return {"base": "dark", "stars": 26, "cam": CAM, "els": els}


# ================================================================== CHAPTER 3 · Temples under the sea?
VSM = View(12.6, 16.4, 35.55, 37.3, (90, 130, 1600, 660))
# The Ice Age land (schematic, dashed = inferred): the Malta Plateau above the sea about 20,000 years ago, Malta joined to Sicily
# (after Rossi et al. 2025 and Furlani et al. 2013; its eastern coast is uncertain). The outline closes inside Sicily, whose land is
# drawn over it.
ICE = [(13.9, 37.25), (13.85, 37.0), (14.15, 36.88), (14.33, 36.62), (14.24, 36.32), (14.08, 36.1), (14.1, 35.9), (14.3, 35.72),
       (14.6, 35.68), (14.86, 35.8), (14.96, 36.1), (15.06, 36.4), (15.24, 36.58), (15.36, 36.84), (15.4, 37.1), (15.05, 37.31),
       (14.5, 37.33)]


def ice_pts(v):
    return [v.p(lo, la) for lo, la in ICE]


def s19():
    """The Ice Age map: today's coasts of Sicily and the Maltese islands; the Ice Age coast fades in, a dashed bright line well outside
    them, and the land between, pale (the land bridge); 'Ice Age coast'; chips 'about 20,000 years ago' and 'sea about 120 m lower'."""
    v = VSM
    els = [poly(ice_pts(v), "rgba(226,200,150,.20)", "#ffe2b0", 2.5, .4, style="inferred", dur=1.0)]
    els += map_els(v)
    els += [lab(*v.p(14.15, 37.2), "Sicily", -1, DIM, 30, st="serif"), lab(*v.p(14.62, 35.76), "Malta", -1, DIM, 28, "start"),
            lab(*v.p(14.2, 36.47), "Ice Age coast", 1.0, "#ffe2b0", 28, "end", fx="pop")]
    els += chip(1430, 440, "about 20,000 years ago", GOLD, 1.5, 28) + chip(1430, 520, "sea about 120 m lower", SEAL, 2.0, 28)
    els += [{"k": "scale", "x": 150, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": -1}]
    return {"base": "map", "cam": CAM, "els": els}


def s20_add():
    """The sea floods back over the land bridge (a translucent sea over it, today's land drawn again on top); small lilac dotted temple
    outlines appear on the drowned land; a lilac question mark."""
    v = VSM
    tt, tu = T("s20", "Could the temples"), T("s20", "under the sea")
    els = [poly(ice_pts(v), SEAC, at=.3, op=.5, dur=1.4), {"k": "map", "land": land_ex(v), "in": .3}] + islands(v, .3)
    for k, (lo, la) in enumerate(((14.47, 36.74), (14.66, 36.44), (14.78, 36.16))):
        x, y = v.p(lo, la)
        els += temple_icon(x, y, 150, tt + .6 + .3 * k, style="claimed", fx="pop")
    els += qmark(1110, 600, tu, 90)
    return els


# ---- under the sea off Malta (s21, s22, s23)
WBANDS = [(130 + 36 * k, mix("#1d5266", "#0a2129", k / 19)) for k in range(20)]     # the water: 20 flat bands, so a cover can match it
SANDY = 650


def water_bg(x0=-60, x1=1840):
    els = [rect(x0, -60, x1 - x0, 192, "#0a1216", at=-1)]
    els += [rect(x0, y0, x1 - x0, 37, c, at=-1) for y0, c in WBANDS]
    els += [ln([(x, 130) for x in (x0, x1)], -1, "#bfe6f5", 2, draw=False, op=.5)]
    # light from the surface, in two groups (kept clear of the middle, where s23's cover lies)
    for k, (xa, xb) in enumerate(((130, 260), (300, 420), (470, 560), (1290, 1380), (1440, 1560), (1600, 1700))):
        els += [poly([(xa, 132), (xb, 132), (xb + 120, 600), (xa + 150, 600)], "#bfe6f5", at=-1, op=.045)]
    return els


def seabed(x0, x1, y, seed, at=-1, flat=(600, 1300)):
    """The sandy seabed from y down, flat between flat[0] and flat[1]."""
    r = random.Random(seed)
    top = []
    for k in range(25):
        x = x0 + (x1 - x0) * k / 24
        top.append((x, y if flat[0] <= x <= flat[1] else y + r.uniform(-14, 10)))
    els = [poly(top + [(x1, 1060), (x0, 1060)], "#56584a", at=at)]
    for _ in range(60):
        els += [circ(r.uniform(x0 + 10, x1 - 10), r.uniform(y + 12, 790), r.uniform(1.5, 3), "#76786a", at=at, op=.6)]
    return els


BOULDERS = [(760, 634, 50, 30, 1), (842, 642, 36, 22, 2), (925, 628, 64, 36, 3), (1020, 640, 42, 26, 4), (1102, 632, 54, 32, 5),
            (1168, 644, 26, 16, 6), (705, 646, 24, 14, 7)]


def boulders(at=-1, fx=None, dx=0, dy=0, s=1.0):
    els = []
    for x, y, rx, ry, sd in BOULDERS:
        x, y = dx + 950 + (x - 950) * s, dy + SANDY + (y - SANDY) * s
        els += [poly(blob(x, y, rx * s, ry * s, 14, .14, sd), "#4d5c63", "#93a9b2", 1.4, at, fx=fx, curve=True),
                ln([(x - rx * s * .6, y - ry * s * .78), (x + rx * s * .3, y - ry * s * .9)], at, "#a9c2cc", 2, draw=False, op=.45)]
    return els


def diver(x, y, s, at, ang=24.0, c="#0c171c", rim="#7fb3c7"):
    """A diver swimming head first to the right, body length about s, turned ang degrees head-down; a torch held forward, its beam ahead."""
    def P(pts):
        return rot([(x + a * s, y + b * s) for a, b in pts], x, y, ang)
    torso = P([(-.3, 0), (-.22, -.07), (.1, -.085), (.28, -.05), (.32, .02), (.12, .08), (-.2, .07)])
    tank = P([(-.24, -.1), (.1, -.13), (.13, -.08), (-.22, -.05)])
    legs = [P([(-.28, -.02), (-.62, -.06)]), P([(-.27, .04), (-.6, .07)])]
    fins = [P([(-.6, -.1), (-.78, -.15), (-.74, -.03), (-.62, -.03)]), P([(-.58, .03), (-.76, .04), (-.7, .13), (-.6, .1)])]
    arm = P([(.16, .03), (.44, .09)])
    torch = P([(.43, .06), (.5, .07), (.5, .12), (.43, .11)])
    beam = P([(.5, .07), (.95, -.02), (.98, .26), (.5, .12)])
    head = P([(.38, -.01)])[0]
    mask = P([(.42, -.04), (.47, -.03), (.47, .02), (.42, .01)])
    els = [poly(beam, "#e9f6ff", at=0, op=.12)]
    els += [ln(l, 0, c, .06 * s, draw=False) for l in legs] + [poly(f, c, rim, 1.2, 0) for f in fins]
    els += [poly(torso, c, rim, 1.4, 0, curve=True), poly(tank, "#3d4f57", rim, 1.2, 0), circ(head[0], head[1], .065 * s, c, rim, 1.4, 0),
            poly(mask, "#9fd0ff", at=0, op=.8), ln(arm, 0, c, .05 * s, draw=False), poly(torch, "#c9ccd2", at=0)]
    for k in range(4):
        bx, by_ = P([(.4 - .02 * k, -.15 - .12 * k)])[0]
        els += [circ(bx, by_ - 10 * k, 3 + k, "none", "#bfe6f5", 1.2, 0, op=.7)]
    return [grp(els, at, "pop")]


def book_icon(x, y, at, year, title=None):
    els = [rect(x - 70, y - 95, 140, 190, "#5a3a2a", "#e2b98c", 2, 6, 0), rect(x - 70, y - 95, 18, 190, "#3e281c", at=0),
           ln([(x - 40, y - 60), (x + 50, y - 60)], 0, "#e2b98c", 1.5, draw=False, op=.6)]
    if title:
        els += [lab(x + 9, y - 10, title, 0, "#f2dcb4", 24, st="serif")]
    return [grp(els, at, "pop"), lab(x, y + 140, year, at + .2, BONE, 30, fx="pop")]


def screen_icon(x, y, at, year):
    els = [rect(x - 100, y - 62, 200, 124, "#10181c", "#9fd0ff", 2.5, 8, 0), poly([(x - 16, y - 22), (x + 24, y), (x - 16, y + 22)], "#9fd0ff", at=0, op=.8),
           ln([(x, y + 62), (x, y + 86)], 0, "#9fd0ff", 3, draw=False), ln([(x - 44, y + 88), (x + 44, y + 88)], 0, "#9fd0ff", 3, draw=False)]
    return [grp(els, at, "pop"), lab(x, y + 140, year, at + .2, BONE, 30, fx="pop")]


def s21():
    """Under the sea off Malta's east coast: water lit from above, a sandy seabed with boulders; a book (2002, Underworld) and a screen
    (2022) at the left; a diver swims down with a torch; a lilac dotted temple outline over the boulders (the drowned temple sought);
    a lilac chip 'Ice Age temples?'."""
    tb, td, tt, tn, ti = T("s21", "book Underworld"), T("s21", "described diving"), T("s21", "drowned temple"), T("s21", "Netflix series"), T("s21", "Ice Age")
    els = water_bg() + seabed(-60, 1840, SANDY, 4) + boulders()
    els += book_icon(250, 330, tb - .3, "2002", "Underworld") + screen_icon(250, 600, tn - .2, "2022")
    els += diver(650, 330, 300, td, 26)
    els += temple_icon(950, 646, 460, tt, style="claimed", fx="pop")
    els += chip(1440, 230, "Ice Age temples?", LILAC, ti - .1, 30)
    return {"base": "dark", "cam": CAM, "els": els}


def s23_add():
    """Back on the seabed: a curator's dive (a small second diver); the lilac temple outline fades (covered by the water's own bands)
    and the boulders stay, plain grey: 'boulders, not a temple'."""
    tc, tn, tt = T("s23", "A curator"), T("s23", "not convinced"), T("s23", "were a temple")
    els = diver(1330, 420, 200, tc, 34)
    y0, y1, x0, x1 = 484, 649, 700, 1200
    cov = []
    for yb, c in WBANDS:
        a, b = max(yb, y0), min(yb + 37, y1)
        if a < b:
            cov.append(rect(x0, a, x1 - x0, b - a, c, at=0))
    els += [grp(cov, tn, fx=None, dur=1.2)] + boulders(tn)
    els += [lab(950, 735, "boulders, not a temple", tt, BONE, 30, fx="pop")]
    return els


def hourglass_small(cx, top, bot, w, at, c=BONE):
    return [grp(hourglass_outline(cx, top, bot, w, 0, c) + [poly([(cx - w / 2 + 6, top + 4), (cx + w / 2 - 6, top + 4), (cx, (top + bot) / 2)], "#e2b98c", at=0, op=.8),
                                                         poly([(cx, (top + bot) / 2 + 6), (cx + w / 2 - 6, bot - 2), (cx - w / 2 + 6, bot - 2)], "#e2b98c", at=0, op=.5)], at, "pop")]


def stone_block(x, y, w, h, at, c=GLOB, fx="pop"):
    d = w * .22
    return [grp([poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h), (x - w / 2, y - h)], c, "rgba(60,40,20,.7)", 2, 0),
                 poly([(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2 + d, y - h - d * .6), (x - w / 2 + d, y - h - d * .6)], GLOB_L, "rgba(60,40,20,.7)", 2, 0),
                 poly([(x + w / 2, y), (x + w / 2 + d, y - d * .6), (x + w / 2 + d, y - h - d * .6), (x + w / 2, y - h)], GLOB_D, "rgba(60,40,20,.7)", 2, 0)], at, fx)]


def tplan(cx, cy, s, kind, at, c=GLOB_L, w=9, style="known", fx="pop"):
    """A temple or tomb plan, entrance at the bottom: 'tomb' (a shaft and lobed chambers cut in rock), 'three' (trefoil), 'five'
    (five apses), 'four' (four apses and a niche). s = half its height."""
    els = []
    A = lambda ax, ay, rx, ry, a0, a1: ln(E(cx + ax * s, cy + ay * s, rx * s, ry * s, 30, a0, a1), 0, c, w, style, curve=True, draw=False)
    if kind == "tomb":
        els += [rect(cx - 1.05 * s, cy - 1.0 * s, 2.1 * s, 2.0 * s, mix(GLOB_D, "#000000", .1), "rgba(255,226,190,.25)", 1.5, 10, 0),
                circ(cx, cy + .62 * s, .2 * s, "#120c08", c, 2, 0),
                poly(E(cx - .42 * s, cy - .15 * s, .4 * s, .32 * s, 20), "#120c08", c, 2, 0, curve=True),
                poly(E(cx + .4 * s, cy - .3 * s, .36 * s, .3 * s, 20), "#120c08", c, 2, 0, curve=True),
                poly([(cx - .1 * s, cy + .5 * s), (cx + .1 * s, cy + .5 * s), (cx + .14 * s, cy - .05 * s), (cx - .14 * s, cy - .05 * s)], "#120c08", at=0)]
        return [grp(els, at, fx)]
    els += [ln([(cx - .95 * s, cy + 1.0 * s), (cx - .4 * s, cy + .9 * s), (cx, cy + .88 * s), (cx + .4 * s, cy + .9 * s), (cx + .95 * s, cy + 1.0 * s)], 0, c, w, style,
               curve=True, draw=False),
            ln([(cx - .12 * s, cy + .9 * s), (cx - .12 * s, cy + .5 * s)], 0, c, w * .8, style, draw=False),
            ln([(cx + .12 * s, cy + .9 * s), (cx + .12 * s, cy + .5 * s)], 0, c, w * .8, style, draw=False)]
    if kind == "three":
        els += [A(-.45, .15, .4, .34, 60, 300), A(.45, .15, .4, .34, -120, 120), A(0, -.45, .34, .3, 160, 380)]
    elif kind == "five":
        els += [A(-.45, .3, .4, .26, 70, 300), A(.45, .3, .4, .26, -120, 110), A(-.45, -.22, .4, .27, 60, 300), A(.45, -.22, .4, .27, -120, 120),
                A(0, -.68, .3, .24, 160, 380)]
    elif kind == "four":
        els += [A(-.45, .3, .4, .26, 70, 300), A(.45, .3, .4, .26, -120, 110), A(-.45, -.22, .4, .27, 60, 300), A(.45, -.22, .4, .27, -120, 120),
                A(0, -.56, .12, .1, 160, 380)]
    return [grp(els, at, fx)]


def mini_seabed(cx, y, w, at, seed=3):
    """A strip of seabed with a few boulders, for a card."""
    r = random.Random(seed)
    els = [poly([(cx - w / 2, y), (cx + w / 2, y), (cx + w / 2, y + 60), (cx - w / 2, y + 60)], "#3f4c47", at=0)]
    for k in range(6):
        bx = cx - w * .38 + w * .76 * k / 5 + r.uniform(-8, 8)
        els += [poly(blob(bx, y - 4, r.uniform(18, 30), r.uniform(12, 18), 12, .15, k + seed), "#4d5c63", "#93a9b2", 1.2, 0, curve=True)]
    return [grp(els, at, "pop")]


def s22():
    """His case, three points in three cards as named: a stone block with a radiocarbon hourglass struck through ('stone can't be
    dated', true, so solid); a five-apse plan appearing whole in lilac dashes ('no learning curve?'); seabed boulders with a lilac dotted
    temple outline over them and a lilac chip '1999'."""
    t1, t2, t9, td, tt = T("s22", "stone can't"), T("s22", "without a learning"), T("s22", "nineteen ninety-nine"), T("s22", "divers had reported"), T("s22", "sunken temple")
    xs = (340, 889, 1438)
    els = [lab(889, 196, "his case", -1, GOLD, 26, st="cap")]
    for x in xs:
        els += [rect(x - 225, 250, 450, 420, "rgba(18,13,10,.82)", "rgba(255,236,206,.22)", 2, 18, -1)]
    x = xs[0]
    els += stone_block(x - 10, 600, 200, 130, t1) + hourglass_small(x, 300, 420, 80, t1 + .3) + [strike(x - 70, 430, x + 70, 290, t1 + .7, RED, 6)]
    els += [lab(x, 720, "stone can't be dated", t1 + .5, BONE, 28)]
    x = xs[1]
    els += tplan(x, 450, 150, "five", t2, LILAC, 6, "inferred")
    els += [lab(x, 720, "no learning curve?", t2 + .4, LILAC, 28)]
    x = xs[2]
    els += chip(x, 320, "1999", LILAC, t9 - .1, 28)
    els += mini_seabed(x, 560, 380, td)
    els += temple_icon(x, 556, 300, tt, style="claimed", fx="pop")
    els += [lab(x, 720, "a sunken temple?", tt + .4, LILAC, 28)]
    return {"base": "dark", "stars": 16, "cam": CAM, "els": els}


def s24():
    """Under a temple, in section: the temple's wall and floor on top; below, the farmers' layer, where a hearth, potsherds and charcoal
    glow ('farmers'); older ground and bedrock below, empty; a lilac dotted 'Ice Age layer?' box at the bottom, crossed in red."""
    tb, th, tp, tf, ti = T("s24", "what lies beneath"), T("s24", "hearths"), T("s24", "pottery"), T("s24", "of farmers"), T("s24", "nothing from the Ice")
    G = 380
    els = [rect(-60, G, 1900, 110, "#5e4631", at=-1), rect(-60, G + 110, 1900, 100, "#46372a", at=-1), rect(-60, G + 210, 1900, 500, "#5a4c3a", at=-1),
           ln([(-60, G + 110), (1840, G + 110)], -1, "rgba(255,226,190,.16)", 1.2, draw=False),
           ln([(-60, G + 210), (1840, G + 210)], -1, "rgba(255,226,190,.16)", 1.2, draw=False)]
    rr = random.Random(12)
    for k in range(14):
        x = rr.uniform(60, 1720); y = rr.uniform(G + 240, 780)
        els += [ln([(x, y), (x + rr.uniform(-40, 40), y + rr.uniform(20, 50))], -1, "#45392b", 2, draw=False, op=.7)]
    els += megawall(420, 1220, G - 12, 150, -1, seed=11, c=GLOB, cl=GLOB_L, cd=GLOB_D)
    for k in range(10):
        x = 330 + 112 * k
        els += [poly(rough([(x, G - 14), (x + 108, G - 14), (x + 108, G + 4), (x, G + 4)], 200 + k, 1.5), mix(GLOB, GLOB_L, .3), "rgba(60,40,20,.6)", 1.2, -1)]
    els += [lab(150, G + 330, "bedrock", -1, DIM, 26, "start")]
    els += [gl(860, G + 55, 420, tb, .35, "lamp")]
    hx = 560
    for k in range(9):
        a = 2 * math.pi * k / 9
        els += [circ(hx + 46 * math.cos(a), G + 62 + 16 * math.sin(a), 10, "#8c7a64", "#cbbca8", 1.2, th + .03 * k, fx="pop")]
    els += [gl(hx, G + 58, 90, th + .2, .9, "fire"), circ(hx, G + 60, 14, "#ff9a4a", at=th + .25, fx="pop")]
    for k in range(9):
        els += [circ(rr.uniform(400, 1300), rr.uniform(G + 30, G + 100), rr.uniform(4, 7), "#151210", at=th + .4 + .05 * k, fx="pop")]
    for k, (x, y, a) in enumerate(((880, G + 64, 10), (960, G + 80, -20), (1040, G + 58, 30), (1120, G + 82, 5))):
        sh = rot([(x - 28, y), (x - 10, y - 12), (x + 14, y - 12), (x + 30, y), (x + 20, y + 6), (x - 20, y + 6)], x, y, a)
        els += [poly(sh, CLAY, CLAY_L, 1.5, tp + .15 * k, fx="pop")]
    els += [lab(1330, G + 68, "farmers", tf, GOLD, 32, "start", fx="pop")]
    bx, by_ = 700, G + 270
    els += [rect(bx, by_, 380, 120, "rgba(201,193,238,.08)", LILAC, 2.5, 10, ti, style="claimed", fx="pop"),
            lab(bx + 190, by_ + 70, "Ice Age layer?", ti + .2, LILAC, 28, fx="pop")] + cross(bx + 420, by_ + 60, ti + .8, RED, 1.4, 6)
    return {"base": "dark", "cam": CAM, "els": els}


def s25():
    """A learning curve in four plans, left to right, each popping as the line goes: a lobed tomb cut in rock, a three-lobed temple, a
    five-apse temple, a four-apse temple with a niche; arrows between; 'step by step'."""
    tl, ts, tt = T("s25", "learning curve"), T("s25", "step by step"), T("s25", "older tombs")
    xs = (290, 680, 1090, 1490)
    els = [tplan(xs[0], 450, 140, "tomb", .4)[0]]
    els += tplan(xs[1], 450, 140, "three", tl - .2) + tplan(xs[2], 450, 140, "five", tl + .5) + tplan(xs[3], 450, 140, "four", tl + 1.2)
    for k, (a, b) in enumerate(zip(xs, xs[1:])):
        els += [arr([(a + 165, 450), (b - 165, 450)], tl - .2 + .7 * k, GOLD, 3, dur=.4, curve=False)]
    els += [lab(xs[0], 665, "rock-cut tomb", ts, BONE, 26, fx="pop"), lab(xs[1], 665, "three lobes", tl, DIM, 26), lab(xs[2], 665, "five apses", tl + .7, DIM, 26),
            lab(xs[3], 665, "four apses", tl + 1.4, DIM, 26), lab(889, 220, "step by step", ts, GOLD, 34, st="serif", fx="pop")]
    return {"base": "plan", "bg": "#2b2219", "north": False, "cam": CAM, "els": els}


# ---- the cart ruts
VPR = (1500, 280)


def rut_pt(x0, t):
    return (x0 + (VPR[0] - x0) * t, 800 + (VPR[1] - 800) * t)


def cart(x, y, s, at):
    """A two-wheeled cart seen from a little above and behind, its wheels in the grooves at x and x + s (ground y)."""
    r = s * .36
    els = []
    for wx in (x, x + s):
        els += [poly(E(wx, y - r, r * .78, r, 24), "none", "#c9a070", 5, 0), circ(wx, y - r, r * .14, "#8a6a44", at=0)]
        for a in range(6):
            aa = math.pi * a / 3
            els += [ln([(wx, y - r), (wx + r * .7 * math.cos(aa), y - r + r * .92 * math.sin(aa))], 0, "#8a6a44", 3, draw=False)]
    els += [ln([(x, y - r), (x + s, y - r)], 0, "#6e4a2c", 7, draw=False),
            poly([(x - 20, y - r * 1.25), (x + s + 20, y - r * 1.25), (x + s + 50, y - r * 2.0), (x + 10, y - r * 2.0)], "#7a5434", "#c9a070", 2, 0),
            ln([(x + s * .5, y - r * 1.3), (x + s * .5 + 160, y - r * 1.05)], 0, "#6e4a2c", 6, draw=False)]
    return [grp(els, at, "rise")]


def s26():
    """The cart ruts: a bare limestone shore on a grey wet day; two grooves run across the rock in perspective and on into the sea; a
    two-wheeled cart rolls along them in the rain, its wheels sinking into the wet rock ('wet limestone'); then, on 'When is still
    debated', a lilac time bar from the temple builders to Roman quarrymen, with a question mark."""
    tc, tw, tq = T("s26", "And the cart ruts"), T("s26", "worn by cart"), T("s26", "When is still")
    tl = T("s26", "wet, soft")
    els = [rect(-60, 300, 1900, 760, "#3d5a68", at=-1)]
    shore = [(-60, 300), (640, 300), (760, 330), (900, 380), (1060, 440), (1260, 520), (1480, 610), (1700, 700), (1840, 760), (1840, 1060), (-60, 1060)]
    els += [poly(shore, "#7a7466", at=-1)]
    rr = random.Random(5)
    for k in range(40):
        x, y = rr.uniform(0, 1500), rr.uniform(330, 790)
        if y > 300 + (x - 640) * .45:
            els += [circ(x, y, rr.uniform(2, 5), "#625d52", at=-1, op=.8)]
    els += [ln([(x, y) for x, y in shore[1:9]], -1, "#e9f6ff", 2.5, draw=False, op=.6)]
    # the two grooves, wider near us; under the water they go on, faint
    for x0, te in ((250, .655), (470, .615)):
        a, b = rut_pt(x0, 0), rut_pt(x0, te)
        els += [poly([(a[0] - 12, a[1]), (a[0] + 12, a[1]), (b[0] + 3, b[1]), (b[0] - 3, b[1])], "#4a4236", at=-1),
                ln([(a[0] + 12, a[1]), (b[0] + 3, b[1])], -1, "#d9cfb8", 2, draw=False, op=.6),
                ln([rut_pt(x0, te), rut_pt(x0, te + .14)], -1, "#2c4652", 5, draw=False, op=.8)]
    els += [lab(965, 590, "cart ruts", tc + .6, GOLD, 32, "start", fx="pop")]
    # the cart in the rain
    p1, p2 = rut_pt(250, .17), rut_pt(470, .17)
    els += cart(p1[0], p1[1], p2[0] - p1[0], tw)
    for x0 in (250, 470):
        p = rut_pt(x0, .17)
        els += [poly(E(p[0], p[1] - 2, 16, 6, 14), "#2e281f", at=tw + .5, fx="pop")]
    rain = []
    for k in range(70):
        x, y = rr.uniform(40, 1740), rr.uniform(140, 760)
        rain.append(ln([(x, y), (x - 10, y + 34)], 0, "#bfe6f5", 1.6, draw=False, op=.45))
    els += [grp(rain, tl - .4, fx=None, dur=1.0), lab(720, 735, "wet limestone", tl + .3, BONE, 30, "start", fx="pop")]
    # the debate over the date
    x0, x1, y = 150, 760, 210
    els += [{"k": "band", "x0": x0, "x1": x1, "y": y - 9, "h": 18, "c": LILAC, "op": .55, "in": tq, "dur": .8},
            lab(x0, y + 48, "temple builders", tq + .3, LILAC, 26, "start", fx="pop"), lab(x1, y + 48, "Roman quarrymen", tq + .6, LILAC, 26, "end", fx="pop"),
            lab((x0 + x1) / 2, y - 22, "?", tq + .9, LILAC, 54, st="big", fx="pop")]
    return {"base": "sky", "tod": "dusk", "ground": 300, "sun": False, "ridges": [], "groundc": "#3d5a68", "cam": CAM, "els": els}


def s27():
    """Depth, to scale: the shore in section, sea level across; the ruts end about 2 m down (a magnifier shows it: '2 m', a person for
    scale); the seabed runs on down to the Ice Age shore at about 120 m (a blue mark); a gauge, and 'more than 100 m deeper'."""
    tu, tg, t2, ti, th = T("s27", "under the sea"), T("s27", "go down"), T("s27", "two metres"), T("s27", "The Ice Age shore"), T("s27", "hundred metres")
    SL, K = 232, 4.2                     # sea level; units a metre
    els = [rect(-60, -60, 1900, SL + 60, "#1a1d22", at=-1)]
    bed = [(640, SL + 9), (760, SL + 40), (980, SL + 160), (1200, SL + 300), (1430, SL + 120 * K), (1520, SL + 120 * K + 14), (1840, SL + 120 * K + 24)]
    rock = [(-60, SL - 26), (420, SL - 12), (560, SL - 4)] + bed + [(1840, 1060), (-60, 1060)]
    els += [poly(rock, "#7d6c52", "#cbbca8", 2, -1), poly([(560, SL), (1840, SL)] + bed[::-1], "#1f5a74", at=-1, op=.6),
            ln([(560, SL), (1840, SL)], -1, "#bfe6f5", 2.5, draw=False), lab(1700, SL - 16, "sea level", -1, SEAL, 26, "end")]
    # the gauge
    gx = 1600
    els += [ln([(gx, SL), (gx, SL + 120 * K)], -1, BONE, 2.5, draw=False)]
    for m in range(0, 121, 20):
        els += [ln([(gx - 10, SL + m * K), (gx + 10, SL + m * K)], -1, BONE, 2, draw=False)]
    els += [lab(gx + 18, SL + 120 * K + 9, "120 m", -1, DIM, 24, "start")]
    # the ruts and their end, magnified
    els += [ln([(300, SL - 15), (560, SL - 4), (640, SL + 9)], tu, "#3a3128", 6, dur=.6), circ(640, SL + 9, 26, "none", GOLD, 3, tu + .4, fx="pop")]
    mx, my, mr = 420, 520, 175
    inner = [circ(mx, my, mr, "#1a1d22", at=0)]
    k2 = 60.0                              # units a metre inside the magnifier
    sy = my - 10
    inner += [poly([(mx - mr + 6, sy - .3 * k2), (mx - 10, sy - .1 * k2), (mx + 40, sy + .4 * k2), (mx + 100, sy + 2 * k2), (mx + 100, my + mr * .8), (mx - mr * .8, my + mr * .8)],
                   "#7d6c52", "#cbbca8", 2, 0),
              poly([(mx - 10, sy), (mx + mr - 6, sy), (mx + mr - 30, my + mr * .7), (mx + 100, my + mr * .7), (mx + 100, sy + 2 * k2), (mx + 40, sy + .4 * k2)], "#1f5a74", at=0, op=.6),
              ln([(mx - 10, sy), (mx + mr - 8, sy)], 0, "#bfe6f5", 2.5, draw=False),
              ln([(mx - mr + 10, sy - .25 * k2), (mx - 10, sy - .08 * k2), (mx + 40, sy + .4 * k2), (mx + 98, sy + 2 * k2)], 0, "#3a3128", 9, draw=False)]
    inner += fig(mx - 60, sy - .2 * k2 + 4, 1.7 * k2, 0, "#e9dccb", fx=None)
    els += [grp([grp(inner, 0, None, clip=[mx - mr, my - mr, 2 * mr, 2 * mr, mr]), circ(mx, my, mr, "none", GOLD, 3, 0)], tg, "pop"),
            ln([(640, SL + 9), (mx + mr * .7, my - mr * .7)], tg, GOLD, 1.5, "inferred", .4, op=.7),
            {"k": "dim", "x1": mx + 122, "y1": sy, "x2": mx + 122, "y2": sy + 2 * k2, "t": "", "c": GOLD, "in": t2, "fx": "draw"},
            lab(mx + 186, sy + k2 + 10, "2 m", t2 + .2, GOLD, 32, "start", fx="pop")]
    # the Ice Age shore
    els += [ln([(1430, SL + 120 * K), (1580, SL + 120 * K)], ti, "#9fd0ff", 3, "inferred", .6), circ(1430, SL + 120 * K, 9, "#9fd0ff", at=ti + .2, fx="pop"),
            lab(1405, SL + 120 * K + 10, "Ice Age shore", ti + .3, "#9fd0ff", 28, "end", fx="pop")]
    els += [ln([(gx - 40, SL + 2 * K), (gx - 52, SL + 2 * K), (gx - 52, SL + 120 * K), (gx - 40, SL + 120 * K)], th, GOLD, 2.5, dur=.7),
            lab(gx - 70, SL + 62 * K, "more than", th + .4, GOLD, 30, "end", fx="pop"), lab(gx - 70, SL + 62 * K + 40, "100 m deeper", th + .5, GOLD, 30, "end", fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def canoe(x, y, w, at, c="#6e4a2c", fx="pop"):
    """A dugout canoe with two paddlers."""
    h = w * .12
    els = [poly([(x - w / 2, y - h * .4), (x - w * .42, y + h * .5), (x + w * .42, y + h * .5), (x + w / 2, y - h * .5)], c, "#e2b98c", 1.5, 0, curve=True)]
    for k in (-1, 1):
        px = x + k * w * .2
        els += [circ(px, y - h * 1.5, h * .42, "#1d1611", at=0), ln([(px, y - h * 1.1), (px, y - h * .1)], 0, "#1d1611", h * .5, draw=False),
                ln([(px + h * .4, y - h * 1.0), (px + h * 1.4, y + h * 1.4)], 0, "#c9a070", 2, draw=False)]
    return [grp(els, at, fx)]


def snail(x, y, r, at):
    return [grp([poly(E(x, y, r, r * .8, 16), "#e9dccb", "#8a7a66", 1.2, 0, curve=True), spiral(x, y, r * .8, 1.6, 0, "#8a7a66", 1.4, 0, .1)], at, "pop")]


def s28():
    """The first sailors: the map of Sicily and Malta (today's coasts); Malta glows; an inset of the cave at Latnija (a hearth glowing,
    stone tools, sea-snail shells); a pin 'Latnija'; chip 'about 8,500 years ago'; then a dugout canoe crosses from Sicily along a dashed
    route, 'about 100 km'."""
    v = VSM
    tr, th, ts, tl, t8, tk = (T("s28", "people reached Malta"), T("s28", "hearths"), T("s28", "sea snails"), T("s28", "Latnija"),
                              T("s28", "eighty-five hundred"), T("s28", "hundred kilometres"))
    els = map_els(v) + [lab(*v.p(14.15, 37.2), "Sicily", -1, DIM, 30, st="serif"), lab(*v.p(14.62, 35.76), "Malta", -1, DIM, 28, "start")]
    mx, my = v.p(14.44, 35.9)
    els += [gl(mx, my, 160, tr, .6, "sun")]
    lx, ly = v.p(*SITES["latnija"])
    # the inset: a cave mouth with a hearth, tools and shells
    ix, iy, iw, ih = 1190, 380, 470, 330
    els += [rect(ix, iy, iw, ih, "rgba(18,13,10,.92)", BONE, 2, 14, th - .4, fx="pop")]
    cave = [grp([poly([(ix + 10, iy + ih - 10), (ix + 10, iy + 20), (ix + iw - 10, iy + 20), (ix + iw - 10, iy + ih - 10)], "#6e5a40", at=0),
                 poly([(ix + 70, iy + ih - 10), (ix + 90, iy + 120), (ix + 170, iy + 60), (ix + 300, iy + 56), (ix + 390, iy + 110), (ix + 410, iy + ih - 10)],
                      "#120c08", "#a8916e", 2, 0, curve=True)], th - .3, "pop")]
    els += cave + [gl(ix + 240, iy + ih - 60, 120, th, .9, "fire"), circ(ix + 240, iy + ih - 52, 12, "#ff9a4a", at=th + .1, fx="pop")]
    for k in range(7):
        a = math.pi * (k / 6)
        els += [circ(ix + 240 + 40 * math.cos(a), iy + ih - 40 + 6 * math.sin(a), 8, "#8c7a64", "#cbbca8", 1, th + .05 * k, fx="pop")]
    for k, (x, y) in enumerate(((ix + 120, iy + ih - 34), (ix + 150, iy + ih - 50), (ix + 330, iy + ih - 36), (ix + 360, iy + ih - 54), (ix + 300, iy + ih - 30))):
        els += snail(x, y, 12, ts + .12 * k)
    for k, (x, y) in enumerate(((ix + 190, iy + ih - 26), (ix + 290, iy + ih - 24))):
        els += [poly([(x - 14, y), (x - 4, y - 10), (x + 14, y - 6), (x + 8, y + 4)], "#c9ccd2", "#ffffff", 1, th + .3 + .1 * k, fx="pop")]
    els += [lab(ix + iw / 2, iy + ih + 40, "hearths and cooked sea snails", ts + .4, BONE, 24, fx="pop")]
    els += [pin(lx, ly, "Latnija", tl, GOLD, "end", -20, 8), ln([(lx + 8, ly - 4), (ix, iy + ih / 2)], tl + .2, GOLD, 1.5, "inferred", .6)]
    els += chip(ix + iw / 2, iy - 50, "about 8,500 years ago", GOLD, t8, 28)
    a_, b_ = v.p(14.86, 36.74), (lx + 14, ly - 14)
    mid = ((a_[0] + b_[0]) / 2 + 40, (a_[1] + b_[1]) / 2)
    els += [arr([a_, mid, b_], tk - .3, GOLD, 3, "inferred", 1.4)] + canoe(mid[0] + 6, mid[1] - 4, 90, tk + .3)
    els += [lab(mid[0] - 50, mid[1] + 14, "about 100 km", tk + .8, GOLD, 30, "end", fx="pop")]
    return {"base": "map", "cam": CAM, "els": els}


def XS(yr):
    return round(160 + (7000 - yr) * .292, 1)


def sheaf(x, y, h, at, c=AU):
    els = []
    for k in range(-3, 4):
        tip = (x + k * h * .09, y - h)
        els += [ln([(x + k * h * .02, y), tip], 0, c, 3, draw=False),
                poly(E(tip[0], tip[1] - h * .06, h * .035, h * .1, 10), c, at=0, curve=True)]
    els += [ln([(x - h * .1, y - h * .35), (x + h * .1, y - h * .35)], 0, "#8a6a44", 5, draw=False)]
    return [grp(els, at, "pop")]


def s29():
    """A time line from 7000 to 2000 BCE: a canoe at about 6500 BCE ('hunter-gatherers'), a sheaf of grain at about 5500 BCE
    ('farmers'), a bracket 'about 1,000 years'; the gold band of the temples from 3600 to 2500 BCE; far left, off the line, a lilac
    'Ice Age temples' struck through."""
    tf, tt = T("s29", "the farmers"), T("s29", "no temples")
    A = 640
    els = [axis(XS(7000), XS(2000), A, [(XS(y), "%d BCE" % y if y in (7000, 2000) else "%d" % y) for y in (7000, 6000, 5000, 4000, 3000, 2000)], -1)]
    els += [{"k": "band", "x0": XS(3600), "x1": XS(2500), "y": A - 34, "h": 20, "c": AU, "in": -1}, lab((XS(3600) + XS(2500)) / 2, A - 56, "temples", -1, AU, 28)]
    els += temple_icon((XS(3600) + XS(2500)) / 2, 470, 220, -1)
    els += canoe(XS(6500), 560, 150, .3) + [ln([(XS(6500), 590), (XS(6500), A - 6)], .5, BONE, 2, draw=False),
                                         lab(XS(6500), 480, "hunter-gatherers", .6, BONE, 28, fx="pop")]
    els += sheaf(XS(5500), 590, 120, tf - .3) + [ln([(XS(5500), 594), (XS(5500), A - 6)], tf - .2, AU, 2, draw=False),
                                              lab(XS(5500), 440, "farmers", tf, AU, 28, fx="pop")]
    els += bracket(XS(6500), XS(5500), 360, tf + .4, None, GOLD, up=False) + [lab((XS(6500) + XS(5500)) / 2, 340, "about 1,000 years", tf + .6, GOLD, 28, fx="pop")]
    els += chip(330, 210, "Ice Age temples", LILAC, tt - .3, 28) + [strike(160, 236, 500, 184, tt + .2, RED, 5)]
    return {"base": "dark", "stars": 24, "cam": CAM, "els": els}


# ================================================================== CHAPTER 4 · The city of the dead
HG = 250                                 # the street; the Hypogeum's rock below it (about 49 units a metre: 10 m = 490)
HROOMS = {1: [(560, 300, 200, 92), (790, 306, 170, 80), (990, 306, 140, 78)],
          2: [(470, 426, 170, 118), (670, 420, 230, 130), (925, 440, 85, 92), (1040, 432, 150, 112)],
          3: [(700, 592, 180, 140), (905, 600, 135, 118)]}


def room(x, y, w, h, at, fill="#140e0a", rim=GLOB_L, fx=None):
    return [poly(rough([(x, y + h), (x - 4, y + h * .4), (x + w * .1, y + 4), (x + w * .5, y - 2), (x + w * .9, y + 4), (x + w + 4, y + h * .4), (x + w, y + h)], int(x + y), 3),
                 fill, rim, 2, at, fx=fx, curve=True)]


def stairs(x, y0, y1, at, n=5, w=40, c=GLOB_L):
    pts_ = []
    for k in range(n + 1):
        y = y0 + (y1 - y0) * k / n
        pts_ += [(x + w * k / n, y), (x + w * (k + 1) / n, y)]
    return [ln(pts_[:-1], at, c, 3, dur=.5)]


def s30():
    """The Hypogeum in section: a street of flat-roofed houses on the surface, a new cistern under one of them and a workman with a pick
    breaking into a dark chamber below (chip '1902', 'Paola'); below, in the rock, the chambers on three levels, linked by passages and
    stairs, built in level by level ('the Hypogeum', 'under the earth', 'three levels'); a person in the top chamber for scale; a
    dimension 'about 10 m'."""
    tb, tu, tr, tl, tm = T("s30", "Below lay"), T("s30", "under the earth"), T("s30", "Rooms, passages"), T("s30", "three levels"), T("s30", "ten metres")
    tp = T("s30", "Paola")
    els = [rect(-60, HG, 1900, 820, "#4f4130", at=-1)]
    rr = random.Random(30)
    for k in range(9):
        y = HG + 60 + 62 * k
        els += [ln([(-60, y + rr.uniform(-6, 6)), (1840, y + rr.uniform(-6, 6))], -1, "rgba(255,226,190,.07)", 1.2, draw=False)]
    for k in range(13):
        x = 110 + 122 * k
        h = 66 + 24 * ((k * 7) % 3)
        els += [rect(x, HG - h, 112, h, "#4e4234", "#8c7a64", 1.5, 2, -1), rect(x + 44, HG - 36, 22, 36, "#1d1611", at=-1),
                rect(x + 14, HG - h + 16, 18, 14, "#2a2219", at=-1), rect(x + 80, HG - h + 16, 18, 14, "#2a2219", at=-1)]
    els += [ln([(-60, HG), (1840, HG)], -1, "#cbbca8", 2, draw=False)]
    els += chip(330, 196, "1902", GOLD, .4, 28) + [lab(1500, 200, "Paola", tp, BONE, 30, fx="pop")]
    # the cistern and the workman breaking through
    cx = 660
    els += [poly([(cx - 34, HG), (cx - 44, HG + 30), (cx - 40, HG + 52), (cx + 40, HG + 52), (cx + 44, HG + 30), (cx + 34, HG)], "#1d1611", "#cbbca8", 1.5, .3, fx="pop")]
    els += fig(cx - 6, HG + 50, 40, .5, "#e9dccb", arms="up", fx="pop") + [ln([(cx + 2, HG + 6), (cx + 20, HG + 2), (cx + 26, HG + 12)], .5, "#c9ccd2", 3, draw=False)]
    # the chambers, level by level
    for lev, at in ((1, tb), (2, tr), (3, tl)):
        for k, (x, y, w, h) in enumerate(HROOMS[lev]):
            els += room(x, y, w, h, at + .15 * k, fx="pop")
    els += [ln([(cx - 10, HG + 52), (cx - 4, HG + 47), (cx + 4, HG + 56), (cx + 10, HG + 50)], tb, "#ffe2b0", 2, dur=.3)]
    els += stairs(735, 392, 420, tr + .3) + stairs(880, 550, 592, tl + .3) + stairs(960, 384, 440, tr + .5, 4, 30)
    els += [ln([(640, 485), (670, 485)], tr + .4, GLOB_L, 6, draw=False), ln([(900, 486), (925, 486)], tr + .4, GLOB_L, 6, draw=False),
            ln([(1010, 486), (1040, 486)], tr + .5, GLOB_L, 6, draw=False), ln([(880, 666), (905, 666)], tl + .4, GLOB_L, 6, draw=False)]
    els += fig(640, 392, 83, tb + .5, "#e9dccb", fx="pop")
    els += [gl(860, 480, 340, tb + .2, .22, "lamp"), lab(1250, 340, "the Hypogeum", tb + .3, GOLD, 36, "start", st="serif", fx="pop"),
            lab(1252, 382, "under the earth", tu, DIM, 26, "start", st="ital", fx="pop")]
    # three levels, about 10 m
    for k, (y0, y1) in enumerate(((300, 392), (420, 550), (592, 740))):
        els += [ln([(1220, y0), (1232, y0), (1232, y1), (1220, y1)], tl + .25 * k, GOLD, 2, dur=.4)]
    els += [lab(1252, 480, "three levels", tl + .4, GOLD, 30, "start", fx="pop")]
    els += [ln([(1630, HG), (1630, 740)], tm, BONE, 2.5, dur=.8), ln([(1618, HG), (1642, HG)], tm, BONE, 2.5, draw=False),
            ln([(1618, 740), (1642, 740)], tm + .6, BONE, 2.5, draw=False), lab(1608, 640, "about 10 m", tm + .5, BONE, 30, "end", fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def s31_add():
    """The street fades; the chambers fill with a soft warm glow; chip '4000 to 2500 BCE'; 70 quiet lights, one for every hundred people
    (no bones drawn), and 'about 7,000 people'."""
    tf, tr, ts = T("s31", "From around"), T("s31", "resting place"), T("s31", "seven thousand")
    els = [rect(-60, -60, 1900, HG + 61, "#0e0b09", at=.2, op=.8, dur=1.4)]
    for lev in (1, 2, 3):
        for x, y, w, h in HROOMS[lev]:
            els += [gl(x + w / 2, y + h * .6, max(w, h) * .7, tr + .1 * lev, .5, "lamp")]
    els += chip(262, 330, "4000 to 2500 BCE", GOLD, tf, 28)
    for k in range(70):
        r_, c_ = divmod(k, 10)
        x, y = 112 + 34 * c_, 410 + 34 * r_
        els += [circ(x, y, 6, "#ffd9a0", at=round(ts - .4 + .02 * k, 2), fx="pop", op=.9)]
    els += [gl(265, 512, 220, ts, .25, "lamp")] + chip(262, 680, "about 7,000 people", GOLD, ts + 1.0, 28) + \
           [lab(262, 736, "one light, a hundred people", ts + 1.3, DIM, 24, fx="pop")]
    return els


def counter(x, y, vals, t0, dt, c=BONE, size=64):
    """A number that counts up: each value pops on its own dark plate, over the one before."""
    out = []
    for k, v_ in enumerate(vals):
        at = round(t0 + dt * k, 2)
        w = len(str(v_)) * size * .62 + 30
        out += [rect(x - w / 2, y - size * .95, w, size * 1.2, "#16110d", at=at), lab(x, y, str(v_), at, c, size, st="big")]
    return out


def leg_figure(x, y, h, at, c="#2a211a", rim="#cbbca8"):
    """A standing person, front view, simple; the right knee (on the viewer's left) circled in gold."""
    els = [circ(x, y - .9 * h, .07 * h, c, rim, 2, 0),
           poly([(x - .14 * h, y - .8 * h), (x + .14 * h, y - .8 * h), (x + .12 * h, y - .5 * h), (x - .12 * h, y - .5 * h)], c, rim, 2, 0),
           poly([(x - .12 * h, y - .52 * h), (x - .01 * h, y - .52 * h), (x - .03 * h, y), (x - .1 * h, y)], c, rim, 2, 0),
           poly([(x + .01 * h, y - .52 * h), (x + .12 * h, y - .52 * h), (x + .1 * h, y), (x + .03 * h, y)], c, rim, 2, 0),
           ln([(x - .14 * h, y - .78 * h), (x - .19 * h, y - .5 * h)], 0, c, .045 * h, draw=False), ln([(x + .14 * h, y - .78 * h), (x + .19 * h, y - .5 * h)], 0, c, .045 * h, draw=False)]
    return [grp(els, at, "rise")]


def s32():
    """Zammit's count: a block of earth 3 m by 1 m by 1 m in three-quarter view; 119 small pale kneecap marks pop inside it in quick
    succession while a counter runs to 119; a standing figure with the right knee circled ('one each'); then 'the whole site' and the
    chip 'about 7,000'."""
    tq, tz, tc, to, ts = T("s32", "How can anyone"), T("s32", "Themistocles Zammit"), T("s32", "counted"), T("s32", "only one"), T("s32", "Scaled up")
    x0, y0, w, h, d = 180, 360, 600, 200, 120
    els = [poly([(x0, y0), (x0 + w, y0), (x0 + w + d, y0 - d * .6), (x0 + d, y0 - d * .6)], "#7a6148", "#cbbca8", 2, -1),
           poly([(x0 + w, y0), (x0 + w + d, y0 - d * .6), (x0 + w + d, y0 + h - d * .6), (x0 + w, y0 + h)], "#4e3d2c", "#cbbca8", 2, -1),
           rect(x0, y0, w, h, "#5e4631", "#cbbca8", 2, 0, -1)]
    rr = random.Random(32)
    for k in range(5):
        els += [ln([(x0 + 10, y0 + 30 + 36 * k + rr.uniform(-5, 5)), (x0 + w - 10, y0 + 30 + 36 * k + rr.uniform(-5, 5))], -1, "rgba(255,226,190,.08)", 1.2, draw=False)]
    els += [lab(x0 + w / 2 + 40, y0 + h + 56, "3 m × 1 m × 1 m", .5, BONE, 28, fx="pop")]
    els += chip(480, 200, "Themistocles Zammit", GOLD, tz - .2, 28)
    for k in range(119):
        r_, c_ = divmod(k, 17)
        x = x0 + 22 + (w - 44) * c_ / 16 + rr.uniform(-5, 5)
        y = y0 + 22 + (h - 44) * r_ / 6 + rr.uniform(-5, 5)
        els += [poly(E(x, y, 8, 6.5, 10), "#efe6d2", "#b8a888", 1, round(tc + .025 * k, 2), fx="pop", curve=True)]
    els += counter(1060, 330, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 119], tc + .2, .25)
    els += leg_figure(1440, 690, 420, to - .6)
    els += [circ(1440 - .065 * 420, 690 - .27 * 420, 26, "none", AU, 4, to, fx="draw", dur=.5), lab(1440, 230, "one each", to + .3, AU, 30, fx="pop")]
    els += [arr([(920, 470), (1000, 520), (1060, 560)], ts, GOLD, 3, dur=.6), lab(1060, 470, "the whole site", ts + .3, GOLD, 28, "start", fx="pop")]
    els += chip(1110, 620, "about 7,000", GOLD, ts + 1.2, 30)
    return {"base": "dark", "stars": 14, "cam": CAM, "els": els}


def couch_lady(x, y, L, at):
    """The Sleeping Lady, schematic: a woman lying on her right side on a low couch with a sagging top, her head on her arm at the left,
    vast rounded hips, a pleated skirt over her folded legs. x, y: the couch's top left; L: her length."""
    X = lambda a: x + a * L
    Y = lambda b: y + b * L
    clay, dark, light = "#b0643c", "#6e3a20", "#e39a68"
    els = [poly([(X(-.04), Y(.0)), (X(.5), Y(.035)), (X(1.04), Y(.0)), (X(1.04), Y(.06)), (X(.5), Y(.095)), (X(-.04), Y(.06))], mix(clay, dark, .35), dark, 2, 0, curve=True)]
    for a in (.0, .3, .7, 1.0):
        els += [rect(X(a) - .02 * L, Y(.06), .04 * L, .07 * L, mix(clay, dark, .45), dark, 1.5, 2, 0)]
    body = [(X(.06), Y(-.02)), (X(.12), Y(-.13)), (X(.22), Y(-.16)), (X(.36), Y(-.13)), (X(.47), Y(-.27)), (X(.62), Y(-.3)), (X(.74), Y(-.22)),
            (X(.8), Y(-.12)), (X(.93), Y(-.1)), (X(.98), Y(-.04)), (X(.95), Y(.0)), (X(.5), Y(.03))]
    els += [poly(body, clay, dark, 2.5, 0, curve=True)]
    for k in range(9):
        a = .42 + .055 * k
        els += [ln([(X(a), Y(-.2 + .04 * abs(k - 4) / 4)), (X(a + .02), Y(.01))], 0, dark, 1.8, draw=False, op=.7)]
    els += [poly(E(X(.05), Y(-.12), .055 * L, .06 * L, 16), clay, dark, 2.5, 0, curve=True),
            ln([(X(.0), Y(-.04)), (X(.08), Y(-.06)), (X(.16), Y(-.05))], 0, mix(clay, dark, .2), .035 * L, curve=True, draw=False),
            ln([(X(.2), Y(-.14)), (X(.28), Y(-.08)), (X(.34), Y(-.06))], 0, mix(clay, dark, .15), .028 * L, curve=True, draw=False),
            ln([(X(.48), Y(-.26)), (X(.62), Y(-.29)), (X(.72), Y(-.22))], 0, light, 3, curve=True, draw=False, op=.7)]
    return [grp(els, at, "rise")]


def s33():
    """Grave goods and the Sleeping Lady: beads, two small pots and a small figure pop on a dark ground; then the Sleeping Lady large in
    warm clay, lying on her side on a couch; a ruler beneath, '12 cm'; three small lilac words drift above: 'asleep?', 'dreaming?',
    'at rest?'."""
    tb, tp, tf, ts, tc = T("s33", "beads"), T("s33", "pots"), T("s33", "small figures"), T("s33", "Sleeping Lady"), T("s33", "twelve centimetres")
    ta, td, tr = T("s33", "asleep"), T("s33", "dreaming"), T("s33", "at rest")
    els = [gl(380, 560, 300, -1, .3, "lamp"), gl(1150, 520, 480, -1, .25, "lamp"), ln([(110, 640), (650, 640)], -1, "#3a2c20", 3, draw=False)]
    for k in range(11):
        a = math.pi * (.15 + .7 * k / 10)
        els += [circ(260 + 120 * math.cos(a), 470 + 50 * math.sin(a), 9, ["#d9b26a", "#8fd9b0", "#e0775a"][k % 3], "#2a2219", 1, tb + .04 * k, fx="pop")]
    els += pot(440, 640, 90, tp) + pot(540, 640, 64, tp + .2, CLAY_D)
    els += seated(250, 640, 90, tf, CLAY, CLAY_D)
    els += couch_lady(780, 560, 760, ts - .4)
    els += [lab(1160, 205, "the Sleeping Lady", ts, GOLD, 36, st="serif", fx="pop")]
    els += [ln([(780, 680), (1540, 680)], tc, BONE, 2.5, dur=.6)] + [ln([(780 + 760 * k / 12, 680), (780 + 760 * k / 12, 692 if k % 6 else 700)], tc + .3, BONE, 2, draw=False)
                                                                 for k in range(13)]
    els += [lab(1160, 740, "12 cm", tc + .4, BONE, 30, fx="pop")]
    els += [lab(900, 300, "asleep?", ta, LILAC, 30, st="serif", fx="rise"), lab(1160, 272, "dreaming?", td, LILAC, 30, st="serif", fx="rise"),
            lab(1420, 300, "at rest?", tr, LILAC, 30, st="serif", fx="rise")]
    return {"base": "dark", "cam": CAM, "els": els}


def honeycomb(x0, y0, cols, rows, r, at, c=OCHRE):
    out = []
    for i in range(rows):
        for j in range(cols):
            cx = x0 + j * r * 1.75 + (r * .87 if i % 2 else 0)
            cy = y0 + i * r * 1.5
            hexa = [(cx + r * math.cos(math.radians(60 * k + 30)), cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
            out.append(poly(hexa, OCHRE if (i + j) % 3 == 0 else "none", c, 3, 0, op=.85))
    return [grp(out, at, None, dur=1.2)]


def s34():
    """A rock-cut ceiling seen from below, lit by one lamp: red ochre spirals paint themselves across it one curl at a time, then a
    honeycomb pattern; 'red ochre'; the chip 'Malta's only prehistoric wall paintings'."""
    tsp, to, tn = T("s34", "painted spirals"), T("s34", "red ochre"), T("s34", "the only prehistoric")
    els = [poly(E(889, 430, 820, 360, 48), "#5e4a36", at=-1)]
    for k in range(5):
        els += [poly(E(889, 470 + 12 * k, 760 - 120 * k, 320 - 50 * k, 40), mix("#7a6448", "#d9c29a", k / 4), at=-1, op=.85, curve=True)]
    els += [gl(889, 820, 520, -1, .55, "lamp")]
    for k, (x, y, r, fl) in enumerate(((520, 360, 70, 1), (700, 270, 58, -1), (889, 330, 80, 1), (1080, 270, 58, -1), (1260, 360, 70, 1))):
        els += [spiral(x, y, r, 2.4, tsp + .45 * k, OCHRE, 9, k * 1.1, 1.0, fl)]
        els += [ln([(x + r * .9 * fl, y + r * .4), (x + r * 1.6 * fl, y + r * .9), (x + r * 1.9 * fl, y + r * .5)], tsp + .45 * k + .6, OCHRE, 6, curve=True, dur=.5)]
    els += [circ(610, 470, 16, OCHRE, at=tsp + 1.6, fx="pop"), circ(1170, 470, 16, OCHRE, at=tsp + 1.8, fx="pop")]
    els += honeycomb(1160, 520, 5, 3, 26, tsp + 2.4)
    els += [lab(500, 560, "red ochre", to, OCHRE, 34, st="serif", fx="pop", halo=False)]
    els += chip(889, 720, "Malta's only prehistoric wall paintings", GOLD, tn, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def trilithon_door(x, by, s, at, c=GLOB, edge="rgba(60,40,20,.7)", inner="#140e0a", fx="pop"):
    """A built trilithon doorway: two uprights, a lintel, the dark way through; flanking slabs."""
    els = [poly(rough([(x - 1.25 * s, by), (x - 1.2 * s, by - .95 * s), (x - .62 * s, by - 1.0 * s), (x - .6 * s, by)], int(x) + 1, 4), mix(c, GLOB_D, .25), edge, 2, 0),
           poly(rough([(x + .6 * s, by), (x + .62 * s, by - 1.0 * s), (x + 1.2 * s, by - .95 * s), (x + 1.25 * s, by)], int(x) + 2, 4), mix(c, GLOB_D, .25), edge, 2, 0),
           rect(x - .58 * s, by - 1.12 * s, .3 * s, 1.12 * s, c, edge, 2, 2, 0), rect(x + .28 * s, by - 1.12 * s, .3 * s, 1.12 * s, c, edge, 2, 2, 0),
           rect(x - .28 * s, by - 1.12 * s, .56 * s, 1.12 * s, inner, at=0),
           rect(x - .7 * s, by - 1.36 * s, 1.4 * s, .26 * s, GLOB_L, edge, 2, 2, 0),
           ln([(x - .56 * s, by - 1.1 * s), (x - .56 * s, by - .05 * s)], 0, GLOB_L, 3, draw=False, op=.6)]
    return [grp(els, at, fx)]


def carved_door(x, by, s, at, fx="pop"):
    """The Hypogeum's 'Holy of Holies', schematic: in the rock face, a porthole doorway within a trilithon, framed by larger trilithons,
    with corbelled courses above, all cut from one mass of rock."""
    face, cut, rim = "#8a7352", "#5e4a36", "#e9d4ae"
    els = [rect(x - 1.5 * s, by - 1.95 * s, 3.0 * s, 1.95 * s, face, at=0)]
    for k in range(3):
        y = by - (1.55 + .12 * k) * s
        els += [poly([(x - (1.25 - .1 * k) * s, y), (x + (1.25 - .1 * k) * s, y), (x + (1.15 - .1 * k) * s, y - .1 * s), (x - (1.15 - .1 * k) * s, y - .1 * s)],
                     mix(face, "#000000", .12 * (k + 1)), rim, 1.2, 0, op=.9)]
    for k, (hw, top, sh) in enumerate(((1.1, 1.5, .25), (.78, 1.25, .38), (.48, 1.0, .5))):
        els += [rect(x - hw * s, by - top * s, 2 * hw * s, top * s, mix(cut, "#000000", sh), rim, 1.6, 2, 0)]
    els += [rect(x - .3 * s, by - .8 * s, .6 * s, .8 * s, mix(face, "#ffffff", .05), rim, 1.6, 2, 0),
            rect(x - .14 * s, by - .62 * s, .28 * s, .36 * s, "#0d0907", rim, 1.4, 6, 0)]
    return [grp(els, at, fx)]


def s35():
    """Two doorways side by side: left, a temple's trilithon doorway built of stones above ground, sky behind; right, the Hypogeum's
    'Holy of Holies' carved from solid rock in the same form; a gold dashed line joins them, 'the same form'."""
    tc, ta = T("s35", "And they carved"), T("s35", "temples above")
    els = [rect(140, 210, 640, 450, "url(#k-sky-dawn)", "rgba(255,236,206,.25)", 2, 14, -1), rect(140, 600, 640, 60, "#4a3c2c", at=-1)]
    els += trilithon_door(460, 600, 190, .3)
    els += [lab(460, 712, "built, above ground", .6, BONE, 28, fx="pop")]
    els += [rect(990, 210, 600, 450, "#5e4a36", "rgba(255,236,206,.25)", 2, 14, -1)]
    els += carved_door(1290, 640, 190, tc)
    els += [lab(1290, 712, "carved, below ground", tc + .4, BONE, 28, fx="pop")]
    els += [ln([(460, 330), (700, 230), (1050, 230), (1290, 300)], ta - .4, GOLD, 3, "inferred", 1.0, curve=True),
            lab(875, 200, "the same form", ta, GOLD, 32, st="serif", fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s36_add():
    """On the carved doorway: a small lamp glows inside it; the built one fades into the dark; quiet."""
    return [rect(-60, -60, 1900, 1120, "#0e0b09", at=.3, op=.62, dur=1.6)] + carved_door(1290, 640, 190, .3, fx=None) + \
           [gl(1290, 540, 240, .6, .7, "lamp"), gl(1290, 560, 90, .8, .9, "fire"), circ(1290, 572, 7, "#ffd9a0", at=1.0, fx="pop")]


# ================================================================== CHAPTER 5 · The room that sings
NICHE = (650, 470)


def rings(cx, cy, at, radii, c=GOLD, w=3, dt=.35, a0=-80, a1=80, op=.8):
    """Rings of sound spreading from (cx, cy): arcs from angle a0 to a1 (degrees, 0 = right), drawn one after another."""
    return [ln(E(cx, cy, r, r * .82, 28, a0, a1), at + dt * k, c, max(1.5, w - .25 * k), dur=.5, curve=True, op=max(.25, op - .08 * k))
            for k, r in enumerate(radii)]


def s37():
    """The Oracle Room in cut-away: a small rock-cut chamber, red ochre spirals on its ceiling, an oval niche in its wall; a person bends
    to the niche and speaks; gold rings of sound spread out of the chamber into the rooms next to it ('main hall'); on '1920', a lilac
    chip '1920: magnified a hundred times?'."""
    ts, tv, tr, t9 = T("s37", "Speak into"), T("s37", "your voice"), T("s37", "rooms around"), T("s37", "nineteen twenty")
    els = [rect(-60, 120, 1900, 940, "#4a3a2a", at=-1)]
    rr = random.Random(37)
    for k in range(30):
        x, y = rr.uniform(0, 1780), rr.uniform(140, 790)
        els += [circ(x, y, rr.uniform(2, 5), "#3a2c20", at=-1, op=.7)]
    # rooms either side, dimmer
    els += room(120, 330, 380, 300, -1, "#1a130e", "rgba(233,212,174,.4)") + room(1260, 360, 380, 260, -1, "#1a130e", "rgba(233,212,174,.4)")
    els += [rect(495, 560, 90, 50, "#1a130e", at=-1), rect(1175, 540, 90, 50, "#1a130e", at=-1)]
    # the Oracle Room
    ch = [(580, 640), (585, 380), (640, 300), (889, 268), (1140, 300), (1190, 380), (1195, 640)]
    els += [poly(ch, "#241a12", GLOB_L, 3, -1, curve=True), gl(889, 560, 300, -1, .3, "lamp")]
    for k, (x, y) in enumerate(((720, 318), (889, 296), (1058, 318))):
        els += [spiral(x, y + 8, 22, 2.0, -1, OCHRE, 4, k * 1.3, .1, 1 if k % 2 else -1)]
    els += [poly(E(NICHE[0], NICHE[1], 40, 62, 24), "#0d0907", GLOB_L, 2.5, -1, curve=True),
            ln(E(NICHE[0], NICHE[1], 40, 62, 16, 100, 260), -1, "#e9d4ae", 2, curve=True, draw=False, op=.5)]
    els += [lab(889, 220, "the Oracle Room", -1, GOLD, 34, st="serif")]
    els += fig(735, 640, 170, ts - .4, "#d9c8a0", arms="point", face=-1, lean=.18)
    els += [lab(NICHE[0] + 10, 576, "niche", ts + .4, BONE, 26, fx="pop")]
    els += rings(NICHE[0] + 6, NICHE[1], tv, [70, 150, 250, 365, 480], GOLD, 4, .3, -55, 55)
    els += rings(NICHE[0] - 6, NICHE[1], tv + .3, [90, 200, 320, 430], GOLD, 3, .3, 125, 235, .6)
    els += [lab(310, 300, "main hall", tr, BONE, 28, fx="pop")]
    els += chip(889, 735, "1920: magnified a hundred times?", LILAC, t9, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def HZ(f):
    return round(160 + 5 * f, 1)


def peak(f, h, at, c, style="known", w=4, base=650, width=9.0):
    pts_ = [(HZ(f + width * u / 3), base - h * math.exp(-u * u / 2)) for u in [x / 4 for x in range(-12, 13)]]
    return ln(pts_, at, c, w, style, dur=.7, curve=True)


def brain(x, y, s, at, c=LILAC, style="claimed"):
    """A brain in profile, schematic: a rounded outline and a few folds."""
    out = [(x - .5 * s, y + .05 * s), (x - .45 * s, y - .25 * s), (x - .2 * s, y - .42 * s), (x + .15 * s, y - .42 * s), (x + .42 * s, y - .28 * s),
           (x + .52 * s, y - .02 * s), (x + .4 * s, y + .22 * s), (x + .1 * s, y + .3 * s), (x - .12 * s, y + .26 * s), (x - .36 * s, y + .26 * s)]
    els = [poly(out, "rgba(201,193,238,.07)", c, 3, 0, curve=True, style=style),
           ln([(x - .3 * s, y - .1 * s), (x - .1 * s, y - .22 * s), (x + .05 * s, y - .08 * s), (x + .25 * s, y - .2 * s)], 0, c, 2.5, style, curve=True, draw=False),
           ln([(x - .3 * s, y + .1 * s), (x - .05 * s, y + .02 * s), (x + .15 * s, y + .14 * s), (x + .38 * s, y + .02 * s)], 0, c, 2.5, style, curve=True, draw=False),
           ln([(x + .02 * s, y + .3 * s), (x + .06 * s, y + .48 * s)], 0, c, 6, style, draw=False)]
    return [grp(els, at, "pop")]


def s38():
    """A frequency scale from 0 to 200 hertz; the range of a man's speaking voice as a soft band; a lilac dotted peak rises at 110 Hz
    (claimed); then a brain outline with lilac dotted waves ('changes the brain?')."""
    tg, tp, tv, tb = T("s38", "the claims"), T("s38", "hundred and ten"), T("s38", "man's voice"), T("s38", "changes how")
    els = [axis(HZ(0), HZ(200), 650, [(HZ(f), "%d Hz" % f if f in (0, 200) else "%d" % f) for f in (0, 50, 100, 150, 200)], -1)]
    els += [ln([(HZ(f), 650 - 14 - 10 * abs(math.sin(f * .37)) - 6 * abs(math.sin(f * 1.3))) for f in range(0, 201, 4)], -1, "rgba(245,236,220,.35)", 2, curve=True, draw=False)]
    els += [lab(889, 190, "the claims", tg, LILAC, 28, st="cap", fx="pop")]
    els += [rect(HZ(85), 285, HZ(155) - HZ(85), 365, "rgba(242,201,142,.10)", at=tv - .3, dur=.8),
            lab((HZ(85) + HZ(155)) / 2, 262, "a man's voice", tv, GOLD, 28, fx="pop")]
    els += [peak(110, 300, tp, LILAC, "claimed", 4), lab(HZ(110), 330, "110 Hz?", tp + .5, LILAC, 30, fx="pop")]
    els += brain(1440, 300, 300, tb)
    for k in range(3):
        y = 470 + 26 * k
        els += [ln([(1290 + 12 * j, y + 9 * math.sin(j * 1.1 + k)) for j in range(26)], tb + .4 + .15 * k, LILAC, 2, "claimed", .6, curve=True)]
    els += [lab(1440, 590, "changes the brain?", tb + .6, LILAC, 28, fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def seated_head(x, y, s, at, c="#1d1611", cap=True):
    """A small seated person seen from the front: head (with a cap of sensors), shoulders, the chair back behind."""
    els = [rect(x - .5 * s, y - .2 * s, s, .9 * s, "#3a2f26", at=0), poly(E(x, y + .35 * s, .42 * s, .3 * s, 14), c, "#cbbca8", 1.2, 0, curve=True),
           circ(x, y - .05 * s, .24 * s, c, "#cbbca8", 1.2, 0)]
    if cap:
        els += [circ(x + .16 * s * math.cos(a), y - .05 * s - .16 * s * abs(math.sin(a)) - .06 * s, .045 * s, "#9fd0ff", at=0)
                for a in (math.pi * k / 5 for k in range(6))]
    return [grp(els, at, "pop")]


def speaker(x, y, s, at, c="#cbbca8"):
    return [grp([rect(x - .4 * s, y - .6 * s, .8 * s, 1.2 * s, "#2a211a", c, 2, 8, 0), circ(x, y - .22 * s, .2 * s, "none", c, 2, 0),
                 circ(x, y + .25 * s, .28 * s, "none", c, 2.5, 0), circ(x, y + .25 * s, .08 * s, c, at=0)], at, "pop")]


def s39():
    """The study behind the brain claim: a laboratory in California, 2008: thirty seated volunteers wearing caps of sensors, a loudspeaker
    playing tones ('90 to 130 Hz'); a monitor whose trace shifts at 110; at the right, a small map of Malta with a grey 'not here'."""
    tc, tv, tt, tsh, tm = T("s39", "California"), T("s39", "thirty volunteers"), T("s39", "heard tones"), T("s39", "shifted"), T("s39", "done in Malta")
    els = [rect(120, 240, 800, 490, "rgba(160,190,200,.06)", "rgba(200,225,240,.35)", 2, 16, -1)]
    els += chip(520, 190, "California, 2008", BONE, tc - .3, 28)
    for k in range(30):
        r_, c_ = divmod(k, 6)
        els += seated_head(400 + 92 * c_, 330 + 82 * r_, 56, -1)
    els += speaker(210, 470, 110, -1)
    els += rings(240, 450, tt, [50, 90, 130], "#9fd0ff", 3, .25, -50, 50, .7)
    els += [lab(220, 600, "90 to 130 Hz", tt + .3, "#9fd0ff", 26, fx="pop"), lab(660, 768, "30 volunteers", tv + .8, BONE, 26, fx="pop")]
    # the monitor
    mx0, my0, mw, mh = 1000, 300, 420, 250
    els += [rect(mx0, my0, mw, mh, "#0d1418", "#9fd0ff", 2.5, 10, -1), ln([(mx0 + mw / 2, my0 + mh), (mx0 + mw / 2, my0 + mh + 40)], -1, "#9fd0ff", 4, draw=False),
            ln([(mx0 + mw / 2 - 70, my0 + mh + 42), (mx0 + mw / 2 + 70, my0 + mh + 42)], -1, "#9fd0ff", 4, draw=False)]
    sx = mx0 + mw * .58
    trace = [(mx0 + 20 + j * 6, my0 + mh / 2 + (14 if mx0 + 20 + j * 6 < sx else 34) * math.sin(j * (.9 if mx0 + 20 + j * 6 < sx else .55))) for j in range(64)]
    els += [ln(trace, tt + .6, "#8fd9b0", 2.5, dur=2.0, curve=True), ln([(sx, my0 + 16), (sx, my0 + mh - 16)], tsh, AU, 2, "inferred", .4),
            lab(sx, my0 + mh + 90, "110 Hz", tsh + .2, AU, 28, fx="pop")]
    # Malta, not here
    v = View(14.15, 14.6, 35.78, 36.1, (1440, 560, 230, 170))
    els += [grp(islands(v, 0, "#3a2f24", "#c9ad85", 1.4), tm - .4, "pop"), lab(1555, 760, "Malta: not here", tm, DIM, 26, fx="pop")]
    return {"base": "dark", "stars": 12, "cam": CAM, "els": els}


def micro(x, y, s, at, c=BONE):
    return [grp([circ(x, y - .3 * s, .16 * s, "#2a211a", c, 2, 0), ln([(x, y - .14 * s), (x, y + .3 * s)], 0, c, 2.5, draw=False),
                 ln([(x - .2 * s, y + .3 * s), (x + .2 * s, y + .3 * s)], 0, c, 2.5, draw=False)], at, "pop")]


def s40():
    """Till's test, 2014: the Oracle Room in plan, a loudspeaker in the chamber, microphones out in the main hall; a tone sweeps from low to
    high ('20 Hz to 20,000 Hz'); then a long decaying wave across a 0 to 16 second axis ('up to 16 s, at 63 Hz')."""
    t4, tsw, tr, ts = T("s40", "In twenty fourteen"), T("s40", "swept from"), T("s40", "ring on"), T("s40", "sixteen seconds")
    els = [rect(110, 230, 680, 520, "#3a2e22", "rgba(255,236,206,.25)", 2, 18, -1)]
    els += [poly(E(300, 380, 85, 68, 30), "#140e0a", GLOB_L, 3, -1, curve=True), rect(330, 430, 60, 60, "#140e0a", at=-1),
            poly(rough([(260, 500), (300, 470), (480, 462), (700, 500), (730, 620), (650, 700), (420, 712), (250, 660)], 41, 6), "#140e0a", GLOB_L, 3, -1, curve=True)]
    els += [lab(300, 290, "Oracle Room", -1, GOLD, 28, fx=None), lab(470, 735, "main hall", -1, BONE, 26)]
    els += chip(450, 180, "2014: Rupert Till", BONE, t4 - .2, 28)
    els += speaker(300, 384, 70, t4 + .4) + micro(470, 600, 70, t4 + .9) + micro(600, 580, 70, t4 + 1.1) + micro(560, 660, 70, t4 + 1.3)
    els += [ln([(300, 384), (470, 600)], t4 + 1.4, GOLD, 1.5, "inferred", .4, op=.7)]
    # the sweep
    sw = []
    xx, ph = 880.0, 0.0
    while xx < 1640:
        u = (xx - 880) / 760
        ph += .06 + .55 * u ** 2.2
        sw.append((round(xx, 1), round(330 - 46 * math.sin(ph), 1)))
        xx += 3
    els += [ln(sw, tsw, AU, 2.5, dur=2.4), lab(1260, 420, "20 Hz to 20,000 Hz", tsw + 1.0, AU, 28, fx="pop")]
    # the decay
    A0 = 690
    els += [axis(880, 1640, A0, [(880, "0 s"), (1640, "16 s")], -1)]
    dec = [(880 + j * 2.5, A0 - 130 - 110 * math.exp(-j * 2.5 / 760 * 3.2) * math.sin(j * .5)) for j in range(305)]
    els += [ln(dec, tr, GOLD, 2.5, dur=3.0), lab(1300, 486, "up to 16 s, at 63 Hz", ts, GOLD, 30, fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def couple(x, y, h, at):
    """A woman and a man, small, side by side, each with an equal gold bar."""
    els = []
    for k, dx in enumerate((-70, 70)):
        cx = x + dx
        els += [circ(cx, y - .88 * h, .1 * h, "#2a211a", "#cbbca8", 2, 0)]
        if k == 0:
            els += [poly([(cx - .12 * h, y - .75 * h), (cx + .12 * h, y - .75 * h), (cx + .2 * h, y - .2 * h), (cx - .2 * h, y - .2 * h)], "#2a211a", "#cbbca8", 2, 0)]
        else:
            els += [poly([(cx - .13 * h, y - .75 * h), (cx + .13 * h, y - .75 * h), (cx + .11 * h, y - .2 * h), (cx - .11 * h, y - .2 * h)], "#2a211a", "#cbbca8", 2, 0)]
        els += [ln([(cx - .06 * h, y - .2 * h), (cx - .06 * h, y)], 0, "#cbbca8", 4, draw=False), ln([(cx + .06 * h, y - .2 * h), (cx + .06 * h, y)], 0, "#cbbca8", 4, draw=False),
                rect(cx - 50, y + 22, 100, 14, AU, at=0)]
    return [grp(els, at, "pop")]


def s41_add():
    """Back on the frequency scale: solid gold peaks rise at 41, 72 and 76 Hz ('about 40 and 75 Hz'); the lilac 110 Hz peak is struck
    through; the brain claim dims; a woman and a man with equal bars ('equally clear')."""
    tl, tn, tw = T("s41", "strongest resonances"), T("s41", "not a hundred"), T("s41", "women's and men's")
    els = [peak(41, 330, tl + .3, AU, w=5), peak(72, 260, tl + .6, AU, w=5, width=4.5), peak(76, 240, tl + .75, AU, w=5, width=4.5),
           lab(HZ(58), 290, "about 40 and 75 Hz", tl + 1.0, AU, 28, fx="pop"), strike(HZ(110) - 60, 600, HZ(110) + 60, 360, tn, RED, 6)]
    els += [rect(1240, 150, 420, 470, "#120e0b", "rgba(255,236,206,.14)", 1.5, 24, tw - .6, op=.78, dur=.8)]
    els += couple(1440, 560, 170, tw) + [lab(1440, 650, "equally clear", tw + .5, AU, 28, fx="pop")]
    return els


def s42():
    """Tuned? 2020: nine gold peaks between about 37 and 93 Hz rise in a row; under them a strip of keys lights every other key, a whole-
    tone scale, the peaks lining up with it (chip '2020'); then a chamber wall with '± 10 to 25 cm'; then a pair of dice in lilac dashes
    ('chance?')."""
    t0, tn, tsc, tw, tch = T("s42", "In twenty twenty"), T("s42", "deepest notes"), T("s42", "musical scale"), T("s42", "walls shaped"), T("s42", "chance alone")
    f0, r = 37.2, (92.5 / 37.2) ** (1 / 8)
    X = lambda f: round(170 + 860 * math.log(f / 35) / math.log(100 / 35), 1)
    A = 520
    els = [ln([(X(35), A), (X(100), A)], -1, BONE, 2, draw=False), lab(X(35), A + 40, "35 Hz", -1, DIM, 24, "start"), lab(X(100), A + 40, "100 Hz", -1, DIM, 24, "end")]
    els += chip(300, 196, "2020", BONE, t0, 28)
    for k in range(9):
        f = f0 * r ** k
        h = 170 + 60 * abs(math.sin(k * 1.7))
        x = X(f)
        els += [ln([(x - 26, A), (x - 10, A - h * .3), (x, A - h), (x + 10, A - h * .3), (x + 26, A)], tn + .25 * k, AU, 4, dur=.5, curve=True)]
    # the strip of keys: semitones from f0 up, every other one lit
    for n in range(17):
        f = f0 * r ** (n / 2)
        x, w = X(f), (X(f0 * r ** .25) - X(f0)) * 1.9
        black = n % 12 in (1, 4, 6, 8, 11)
        els += [rect(x - w / 2, 580, w, 110, "#2a2420" if black else "#e9e1d0", "#6a5e50", 1.2, 3, -1)]
        if n % 2 == 0:
            els += [rect(x - w / 2 + 3, 583, w - 6, 104, AU, at=round(tsc + .1 * n / 2, 2), op=.75)]
    els += [lab((X(35) + X(100)) / 2, 740, "a whole-tone scale", tsc + 1.0, AU, 28, fx="pop")]
    # the wall, shaped within 10 to 25 cm
    wx, wy = 1425, 470
    vault = E(wx, wy, 205, 190, 30, 180, 360)
    els += [grp([rect(wx - 245, 240, 490, 250, "#5e4a36", "rgba(255,236,206,.25)", 1.5, 10, 0),
                 poly(vault + [(wx + 205, wy + 20), (wx - 205, wy + 20)], "#140e0a", GLOB_L, 3, 0)], tw - .4, "pop"),
            ln(E(wx, wy, 187, 172, 30, 180, 360), tw + .2, AU, 2.5, "inferred", .8, curve=True),
            ln([(wx, wy - 190), (wx, wy - 172)], tw + .6, AU, 3, dur=.2), lab(wx, wy - 40, "± 10 to 25 cm", tw + .5, AU, 30, fx="pop")]
    # the dice
    dx, dy = 1430, 600
    for k, (ox, oy, pips) in enumerate(((-70, 0, 3), (60, 18, 5))):
        x0, y0 = dx + ox - 45, dy + oy - 45
        dice = [rect(x0, y0, 90, 90, "rgba(201,193,238,.06)", LILAC, 2.5, 12, 0, style="inferred")]
        spots = {3: [(.25, .25), (.5, .5), (.75, .75)], 5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)]}[pips]
        dice += [circ(x0 + 90 * u, y0 + 90 * v_, 7, LILAC, at=0) for u, v_ in spots]
        els += [grp(dice, tch + .2 * k, "pop")]
    els += [lab(dx, dy + 120, "chance?", tch + .5, LILAC, 30, fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def chladni16(n=3, m=5, N=52, x0=230, y0=270, W=400, at=0.0):
    """Sand on a vibrating square plate: dots where cos(n x)cos(m y) - cos(m x)cos(n y) is near zero (a textbook Chladni figure), building
    out from the centre (after the Short cymatic-temples)."""
    out = []
    for i in range(N + 1):
        for j in range(N + 1):
            x, y = math.pi * i / N, math.pi * j / N
            f = math.cos(n * x) * math.cos(m * y) - math.cos(m * x) * math.cos(n * y)
            if abs(f) < .09:
                out.append(circ(x0 + W * i / N, y0 + W * j / N, 3.2, "#f2e8d6", at=round(at + (abs(i - N / 2) + abs(j - N / 2)) * .02, 2)))
    return out


def note_icon(x, y, s, at, c=BONE):
    return [grp([poly(E(x, y, .28 * s, .2 * s, 14), c, at=0, curve=True), ln([(x + .26 * s, y - .02 * s), (x + .26 * s, y - 1.0 * s)], 0, c, 4, draw=False),
                 ln([(x + .26 * s, y - 1.0 * s), (x + .55 * s, y - .78 * s), (x + .5 * s, y - .6 * s)], 0, c, 4, curve=True, draw=False)], at, "pop")]


def s43():
    """Pictures of sound? Left: a square metal plate whose sand gathers into a symmetrical Chladni figure, a note above it. Right: one of
    the Hypogeum's red ochre spirals. Between them a lilac dotted '='; then a chip 'no published test'."""
    tsp, tp, tl, tn = T("s43", "painted spirals"), T("s43", "pictures of sound"), T("s43", "patterns sand makes"), T("s43", "no published study")
    els = [rect(222, 262, 416, 416, "#2a2d31", "#9fb0c0", 2.5, 4, -1)]
    els += note_icon(420, 220, 70, tp) + chladni16(at=tl)
    els += [lab(430, 730, "sand on a singing plate", tl + .6, BONE, 26, fx="pop")]
    els += [rect(1130, 262, 416, 416, "#8a7352", "rgba(255,236,206,.3)", 2, 18, -1), gl(1338, 470, 260, -1, .25, "lamp")]
    els += [spiral(1338, 470, 150, 3.0, tsp, OCHRE, 12, .4, 1.4), ln([(1338 + 150, 470), (1338 + 190, 420), (1338 + 180, 360)], tsp + 1.2, OCHRE, 9, curve=True, dur=.4)]
    els += [lab(1338, 730, "red ochre, the Hypogeum", tsp + .4, BONE, 26, fx="pop")]
    els += [lab(884, 500, "=", tl + .8, LILAC, 90, st="big", fx="pop"), lab(889, 400, "?", tl + 1.1, LILAC, 54, st="big", fx="pop")]
    els += chip(889, 610, "no published test", LILAC, tn, 28)
    return {"base": "dark", "stars": 14, "cam": CAM, "els": els}


def s44_add():
    """Back in the Oracle Room: the gold rings spread once more from the niche; a lilac question mark rises beside it."""
    tw = T("s44", "Whether it was")
    return rings(NICHE[0] + 6, NICHE[1], .3, [80, 170, 280, 390, 480], AU, 4, .3, -55, 55, .9) + qmark(1000, 470, tw, 90)


# ================================================================== CHAPTER 6 · The end of the temples
def terraces(pts, at, c="#5f6a3c", edge="#3a3a24", n=5):
    """Terrace walls on a slope: short level steps along the polyline pts (top to bottom)."""
    out = []
    for k in range(1, n + 1):
        u = k / (n + 1)
        i = min(len(pts) - 2, int(u * (len(pts) - 1)))
        f = u * (len(pts) - 1) - i
        x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f
        y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
        out += [ln([(x - 40, y), (x + 40, y)], at, "#d9c8a0", 2.5, draw=False, op=.55)]
    return out


def s45():
    """A Maltese valley in section at dusk: terraced hills either side, a stream at the bottom, the valley's fill of mud in layers; a drill
    lowers a core tube into it; the core comes up and lies across the panel, its layers like pages ('older', 'younger'); then, as named:
    soil slides down the hills ('soil lost'), the stream dries ('streams dry up'), and the pollen grains thin out towards the young end
    of the core ('less cereal pollen')."""
    td, tl, tpg, ts, tst, tp, tdr = (T("s45", "drilled cores"), T("s45", "in layers"), T("s45", "pages of a diary"), T("s45", "losing their soil"),
                                     T("s45", "streams drying"), T("s45", "less cereal"), T("s45", "turned drier"))
    G = 430
    left = [(-60, 240), (160, 250), (330, 300), (520, 380), (700, G - 6), (780, G)]
    right = [(1000, G), (1080, G - 8), (1250, 370), (1440, 300), (1620, 260), (1840, 250)]
    els = [poly(left + [(780, 620), (-60, 620)], "#5c5236", "#8c7a5a", 2, -1, curve=True), poly(right + [(1840, 620), (1000, 620)], "#5c5236", "#8c7a5a", 2, -1, curve=True)]
    els += terraces(left[:5], -1) + terraces(right[1:], -1)
    for k, y in enumerate((G, G + 34, G + 70, G + 104, G + 140)):
        els += [poly([(760 - 40 * k, y), (1020 + 40 * k, y), (1060 + 40 * k, y + 36), (720 - 40 * k, y + 36)], mix("#6e5a40", "#3e3226", k / 4), at=-1)]
    els += [rect(-60, 620, 1900, 440, "#2e261d", at=-1)]
    els += [poly(E(890, G + 4, 46, 10, 16, 0, 180), "#3f86a8", at=-1, op=.9, curve=True), ln([(845, G), (935, G)], -1, "#9fd0ff", 3, draw=False)]
    # the drill and the core tube
    els += [grp([ln([(840, G), (890, 260)], 0, "#c9ccd2", 4, draw=False), ln([(940, G), (890, 260)], 0, "#c9ccd2", 4, draw=False),
                 ln([(890, 260), (890, G)], 0, "#c9ccd2", 3, draw=False), rect(870, 280, 40, 26, "#8a6a44", at=0)], td - .3, "pop"),
            ln([(890, G), (890, G + 175)], td + .4, "#e9e1d0", 6, dur=1.0)]
    for k, y in enumerate((G + 34, G + 70, G + 104, G + 140)):
        els += [ln([(760 - 40 * k, y), (1020 + 40 * k, y)], tl + .15 * k, "#e9d4ae", 2, dur=.5, op=.7)]
    # the core, lying across the panel
    cx0, cx1, cy = 260, 1520, 690
    core = [rect(cx0, cy - 28, cx1 - cx0, 56, "#5e4a36", "#e9d4ae", 2, 28, 0)]
    rr = random.Random(45)
    x = cx0 + 20
    while x < cx1 - 20:
        w = rr.uniform(14, 40)
        core.append(rect(x, cy - 26, min(w, cx1 - 20 - x), 52, mix("#7a6448", "#3e3226", rr.random()), at=0))
        x += w + 2
    els += [grp(core, tpg - .6, "rise"), lab(cx0 - 16, cy + 9, "older", tpg, DIM, 24, "end", fx="pop"), lab(cx1 + 16, cy + 9, "younger", tpg + .2, DIM, 24, "start", fx="pop")]
    # soil lost, streams dry, less pollen
    els += [arr([(330, 285), (470, 345), (600, 400)], ts, CLAY_L, 4, dur=.6), arr([(1440, 290), (1300, 345), (1160, 400)], ts + .2, CLAY_L, 4, dur=.6),
            lab(300, 210, "soil lost", ts + .4, CLAY_L, 30, "start", fx="pop")]
    els += [poly(E(890, G + 4, 48, 12, 16, 0, 180), "#5e4a36", at=tst, curve=True, dur=1.2), ln([(843, G), (937, G)], tst, "#8c7a5a", 3, draw=False, dur=1.2),
            lab(1080, 520, "streams dry up", tst + .4, "#9fd0ff", 28, "start", fx="pop")]
    for k in range(46):
        u = (k + .5) / 46
        x = cx0 + 40 + (cx1 - cx0 - 80) * (u ** 1.8)
        els += [circ(x, cy + rr.uniform(-16, 16), 5, AU, at=round(tp + .02 * k, 2), fx="pop")]
    els += [lab(1220, 630, "less cereal pollen", tp + .6, AU, 28, fx="pop")]
    els += [rect(-60, -60, 1900, 680, "#c8792e", at=tdr, op=.10, dur=1.5)]
    return {"base": "sky", "tod": "dusk", "ground": 620, "sun": [1540, 200, 26], "ridges": [], "groundc": "#2e261d", "cam": CAM, "els": els}


def helix(x, y0, y1, at, amp=60, turns=3.0, c1=AU, c2="#9fd0ff"):
    n = 80
    a = [(x + amp * math.sin(2 * math.pi * turns * k / n), y0 + (y1 - y0) * k / n) for k in range(n + 1)]
    b = [(x - amp * math.sin(2 * math.pi * turns * k / n), y0 + (y1 - y0) * k / n) for k in range(n + 1)]
    els = [ln(a, at, c1, 4, dur=1.4, curve=True), ln(b, at + .2, c2, 4, dur=1.4, curve=True)]
    for k in range(0, n + 1, 4):
        els += [ln([a[k], b[k]], at + .6 + .01 * k, "rgba(245,236,220,.5)", 2, dur=.2)]
    return els


def s46():
    """Malta and Gozo small in a wide dark sea; a DNA double helix draws itself beside them ('three genomes'); a small family tree whose two
    branches meet again at one child (gold), 'parents related'; 'small, isolated'."""
    ta, ts, tc = T("s46", "Ancient DNA"), T("s46", "small, isolated"), T("s46", "close relatives")
    v = View(12.9, 15.9, 35.25, 37.45, (80, 130, 760, 660))
    els = [{"k": "map", "land": land_ex(v), "in": -1}] + islands(v)
    mx, my = v.p(14.35, 35.95)
    els += [gl(mx, my, 120, -1, .35, "lamp"), lab(*v.p(14.4, 35.62), "Malta", -1, DIM, 28)]
    els += helix(940, 200, 700, ta) + chip(940, 160, "three genomes", AU, ta + .6, 28)
    els += [circ(mx, my, 70, "none", AU, 2.5, ts, fx="draw", dur=.6), lab(mx, my - 92, "small, isolated", ts + .3, AU, 28, fx="pop")]
    # the family tree
    tx, ty = 1380, 230
    tree = [circ(tx, ty, 16, "#2a211a", "#cbbca8", 2, 0), ln([(tx, ty + 16), (tx, ty + 40)], 0, "#cbbca8", 2, draw=False),
            ln([(tx - 130, ty + 40), (tx + 130, ty + 40)], 0, "#cbbca8", 2, draw=False),
            ln([(tx - 130, ty + 40), (tx - 130, ty + 210)], 0, "#cbbca8", 2, "inferred", draw=False),
            ln([(tx + 130, ty + 40), (tx + 130, ty + 210)], 0, "#cbbca8", 2, "inferred", draw=False),
            circ(tx - 130, ty + 230, 20, "#2a211a", "#cbbca8", 2, 0), circ(tx + 130, ty + 230, 20, "#2a211a", "#cbbca8", 2, 0),
            ln([(tx - 110, ty + 230), (tx + 110, ty + 230)], 0, "#cbbca8", 2, draw=False), ln([(tx, ty + 230), (tx, ty + 300)], 0, "#cbbca8", 2, draw=False)]
    els += [grp(tree, tc - 1.0, "pop"), circ(tx, ty + 324, 24, AU, "#fff1d2", 2, tc, fx="pop"), gl(tx, ty + 324, 90, tc, .5, "sun"),
            lab(tx, ty + 410, "parents related", tc + .4, AU, 30, fx="pop")]
    return {"base": "map", "cam": CAM, "els": els}


def XE(yr):
    return round(160 + (3000 - yr) * 1.2167, 1)


def s47():
    """A time line from 3000 to 1800 BCE: the temples' band fades out by about 2350 BCE; a sandy band 'drought' from about 2200 BCE comes
    after it; a gentle decline line starts well before it; a lilac dotted 'plague?' chip floats over the decline."""
    tg, td, tpl = T("s47", "great drought"), T("s47", "decline seems"), T("s47", "A plague")
    A = 660
    els = [axis(XE(3000), XE(1800), A, [(XE(y), "%d BCE" % y if y in (3000, 2000) else "%d" % y) for y in (3000, 2500, 2000)], -1)]
    els += [{"k": "band", "x0": XE(3000), "x1": XE(2450), "y": A - 60, "h": 20, "c": AU, "in": -1}]
    for k in range(5):
        els += [rect(XE(2450 - 20 * k), A - 60, XE(2430 - 20 * k) - XE(2450 - 20 * k) + 1, 20, AU, at=-1, op=.7 - .13 * k)]
    els += [lab(XE(2750), A - 80, "the temples", -1, AU, 28)]
    els += [rect(XE(2200), 250, XE(1900) - XE(2200), A - 270, "rgba(214,170,100,.16)", "rgba(214,170,100,.5)", 2, 6, tg, dur=.8),
            lab((XE(2200) + XE(1900)) / 2, 300, "drought", tg + .3, "#e2b98c", 32, fx="pop"),
            lab((XE(2200) + XE(1900)) / 2, 340, "about 2200 BCE", tg + .5, "#e2b98c", 26, fx="pop")]
    dl = [(XE(3000), 330), (XE(2800), 332), (XE(2700), 345), (XE(2600), 380), (XE(2500), 440), (XE(2400), 520), (XE(2330), 560)]
    els += [ln(dl, td, BONE, 4, dur=1.6, curve=True), lab(XE(2600) + 20, 360, "decline", td + 1.0, BONE, 30, "start", fx="pop")]
    els += chip(540, 268, "plague?", LILAC, tpl, 28)
    return {"base": "dark", "stars": 18, "cam": CAM, "els": els}


def broken_statue(x, by, h, at):
    """A seated stone figure, broken: the same seated figure as in chapter one, cut in two: its lower body tilted where it lies, its upper
    body fallen on its side beside it, small fragments around."""
    lower = {"k": "group", "tr": "rotate(-12 %.1f %.1f)" % (x, by), "clip": [round(x - .7 * h, 1), round(by - .5 * h, 1), round(1.4 * h, 1), round(.62 * h, 1)],
             "els": seated(x, by, h, 0, fx=None)}
    upper = {"k": "group", "tr": "translate(%.1f %.1f) rotate(84 %.1f %.1f)" % (.78 * h, .31 * h, x, by - .5 * h),
             "clip": [round(x - .7 * h, 1), round(by - 1.0 * h, 1), round(1.4 * h, 1), round(.5 * h, 1)], "els": seated(x, by, h, 0, fx=None)}
    els = [lower, upper]
    rr = random.Random(48)
    for k in range(8):
        fx_ = x + rr.uniform(-.75, 1.25) * h
        els += [poly(blob(fx_, by - 7, rr.uniform(7, 15), rr.uniform(5, 10), 7, .3, k), mix(GLOB, GLOB_D, rr.random() * .5), "rgba(60,40,20,.7)", 1.2, 0)]
    return [grp(els, at, "pop")]


def s48():
    """Left: the fragments of a stone seated figure, lying broken ('Xagħra Circle, Gozo'). Right: a section at Tarxien: the temple's floor
    slabs and the foot of a carved wall; over them a pale layer of soil fills in ('no trace of people')."""
    tx, tsm, tt, tl, tn = T("s48", "Xaghra Circle"), T("s48", "smashed"), T("s48", "At Tarxien"), T("s48", "a layer of soil"), T("s48", "no trace")
    els = [gl(400, 600, 330, -1, .3, "lamp"), ln([(110, 640), (760, 640)], -1, "#3a2c20", 3, draw=False)]
    els += broken_statue(380, 640, 230, tsm - .2)
    els += [lab(440, 712, "Xagħra Circle, Gozo", tx, GOLD, 32, st="serif", fx="pop")]
    # Tarxien in section
    x0, x1, F = 900, 1680, 560
    els += [rect(x0, F + 30, x1 - x0, 210, "#6e5a40", "rgba(255,236,206,.2)", 1.5, 8, -1)]
    for k in range(6):
        xx = x0 + 10 + 130 * k
        els += [poly(rough([(xx, F), (xx + 126, F), (xx + 126, F + 30), (xx, F + 30)], 300 + k, 1.5), mix(GLOB, GLOB_L, .25), "rgba(60,40,20,.6)", 1.2, -1)]
    els += [poly(rough([(x0 + 10, F), (x0 + 12, F - 220), (x0 + 160, F - 228), (x0 + 166, F)], 310, 3), mix(GLOB, GLOB_D, .2), "rgba(60,40,20,.6)", 1.6, -1)]
    for k in range(2):
        els += [spiral(x0 + 52 + 64 * k, F - 120, 26, 2.0, -1, GLOB_L, 4, k * 1.4, .1, 1 if k else -1)]
    els += [lab(1380, 250, "Tarxien", tt, GOLD, 32, st="serif", fx="pop")]
    els += [rect(x0 + 168, F - 84, x1 - x0 - 178, 84, "#d9c8a0", "rgba(255,236,206,.5)", 1.5, 4, tl, fx="fill", dur=1.6)]
    els += [lab(1420, F - 32, "no trace of people", tn, "#3a2414", 30, fx="pop", halo=False)]
    return {"base": "dark", "stars": 12, "cam": CAM, "els": els}


def urn(x, by, h, at, c=CLAY, fx="pop"):
    return [{"k": "vase", "x": x, "y": by, "h": h, "w": h * .8, "tone": c, "in": at, "fx": fx,
             "profile": [[0, .34], [.1, .38], [.35, .5], [.7, .46], [.9, .32], [1, .24]]}]


def s49_add():
    """The Tarxien section again, at night: over the pale layer, urns appear one by one with a small bronze dagger and axe beside them
    ('urns, ashes, bronze'); at the top left a small boat arrives, chip 'about 2000 BCE'."""
    tn, tb, tu = T("s49", "newcomers arrived"), T("s49", "burned their dead"), T("s49", "in urns")
    F = 560
    els = [rect(-60, -60, 1900, 1120, "#06081a", at=.2, op=.45, dur=1.4)]
    els += boat(640, 330, 150, tn) + chip(640, 240, "about 2000 BCE", GOLD, tn + .4, 28)
    for k, x in enumerate((1170, 1280, 1390, 1500)):
        els += urn(x, F - 84, 76, tu + .3 * k)
    els += [gl(1340, F - 140, 360, tb, .35, "lamp")]
    els += [grp([ln([(1592, F - 86), (1592, F - 150)], 0, "#8a6a44", 5, draw=False), poly([(1584, F - 150), (1600, F - 150), (1592, F - 196)], "#d99a5a", "#ffd9a0", 1, 0),
                 ln([(1574, F - 150), (1610, F - 150)], 0, "#c98a4a", 4, draw=False)], tb + .6, "pop")]
    els += axe_icon(1636, F - 96, 70, tb + .8, "#d99a5a")
    els += [lab(1360, F - 230, "urns, ashes, bronze", tu + 1.4, BONE, 30, fx="pop")]
    return els


def s50():
    """Malta and Gozo at dusk, low and small on a wide, calm sea; one temple light on Gozo; the dusk deepens into night (the light dims
    with it), and the first stars come out."""
    H = 560
    els = [{"k": "water", "y": H, "h": 520, "x0": -60, "x1": 1840, "op": .85, "in": -1}]
    gozo = [(600, H), (630, H - 10), (690, H - 18), (760, H - 14), (800, H)]
    malta = [(880, H), (930, H - 12), (1040, H - 22), (1150, H - 26), (1240, H - 14), (1300, H)]
    els += [poly(gozo, "#1a1714", at=-1, curve=True), poly([(820, H), (836, H - 6), (852, H)], "#1a1714", at=-1),
            poly(malta, "#1a1714", at=-1, curve=True)]
    els += [gl(700, H - 18, 70, -1, .9, "fire"), circ(700, H - 18, 3.5, "#ffe2b0", at=-1)]
    els += [rect(-60, -60, 1900, 1120, "#05060f", at=.8, op=.5, dur=4.0)]
    els += [{"k": "stars", "n": 60, "x0": 60, "x1": 1720, "y0": 130, "y1": 470, "seed": 50, "in": 2.6, "dur": 2.0}]
    return {"base": "sky", "tod": "dusk", "ground": H, "sun": False, "ridges": [], "groundc": "#163447", "cam": CAM, "els": els}


# ================================================================== CHAPTER 7 · The weighing
LROWS = [270, 390, 510, 630]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1200, y, grade, gc, gt, 28, "start")
    return out


def ledger(title, at):
    return [rect(110, 170, 1560, 530, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, at), lab(140, 195, title, at + .2, GOLD, 26, "start", st="cap")]


def pic_temple(x, y, at):
    return temple_icon(x, y + 22, 110, at, fx="pop")


def pic_drowned(x, y, at):
    return [grp(temple_icon(x, y + 26, 100, 0, style="claimed", fx=None) +
                [ln([(x - 54 + 12 * k, y - 18 + (4 if k % 2 else -4)) for k in range(10)], 0, "#9fd0ff", 3, curve=True, draw=False)], at, "pop")]


def pic_ruts(x, y, at):
    return [grp([ln([(x - 40, y + 30), (x - 6, y - 30)], 0, "#4a4236", 7, draw=False), ln([(x + 6, y + 30), (x + 24, y - 30)], 0, "#4a4236", 7, draw=False),
                 ln([(x - 36, y + 30), (x - 3, y - 30)], 0, "#d9cfb8", 2, draw=False), ln([(x + 10, y + 30), (x + 27, y - 30)], 0, "#d9cfb8", 2, draw=False)], at, "pop")]


def pic_rings(x, y, at):
    return [grp([circ(x - 26, y, 7, AU, at=0)] + [ln(E(x - 26, y, r, r, 14, -50, 50), 0, AU, 3, curve=True, draw=False, op=.9 - .2 * k) for k, r in enumerate((20, 38, 56))], at, "pop")]


def pic_spiral(x, y, at):
    return [grp([spiral(x, y, 30, 2.2, 0, OCHRE, 5, 0, .1)], at, "pop")]


def pic_urn(x, y, at):
    return [grp(urn(x, y + 34, 64, 0, fx=None), at, "pop")]


def pic_stalk(x, y, at):
    return [grp([ln([(x - 4, y + 34), (x, y - 6), (x + 18, y - 26), (x + 30, y - 18)], 0, "#b8a060", 4, curve=True, draw=False),
                 poly(E(x + 32, y - 12, 7, 14, 10), "#b8a060", at=0, curve=True), ln([(x, y + 6), (x - 20, y - 4)], 0, "#b8a060", 3, draw=False)], at, "pop")]


def s51():
    """The ledger, panel one (who built them, and when): built by Malta's own farmers, from about 3600 BCE: Established."""
    tr, tg = T("s51", "Built by"), T("s51", "Established")
    els = ledger("Who built them, and when", .2)
    els += lrow(0, tr, pic_temple, "built by Malta's farmers, from 3600 BCE", "Established", tg, GRADE["established"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s52_add():
    t2, g2, t3, g3 = T("s52", "Temples from the Ice"), T("s52", "Ruled out"), T("s52", "Cart ruts as"), T("s52", "Ruled out", k=2)
    els = lrow(1, t2, pic_drowned, "Ice Age temples under the sea", "Ruled out", g2, GRADE["ruled"])
    els += [strike(170, LROWS[1] + 30, 262, LROWS[1] - 30, g2 + .2, RED, 5)]
    els += lrow(2, t3, pic_ruts, "cart ruts as Ice Age roads", "Ruled out", g3, GRADE["ruled"])
    els += [strike(170, LROWS[2] + 30, 262, LROWS[2] - 30, g3 + .2, RED, 5)]
    return els


def s53():
    """The ledger, panel two (sound, and the end): the Hypogeum carved to sing: Open question; 110 Hz brains and sound spirals: Awaiting
    evidence."""
    t1, g1, t2, g2 = T("s53", "A Hypogeum carved"), T("s53", "Open question"), T("s53", "A brain-changing"), T("s53", "Awaiting evidence")
    els = ledger("Sound, and the end", .2)
    els += lrow(0, t1, pic_rings, "the Hypogeum carved to sing", "Open question", g1, GRADE["open"])
    els += lrow(1, t2, pic_spiral, "110 Hz brains, sound spirals", "Awaiting evidence", g2, GRADE["awaiting"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s54_add():
    t3, g3, t4, g4 = T("s54", "Newcomers who burned"), T("s54", "Strong evidence"), T("s54", "And why the temple"), T("s54", "open question")
    els = lrow(2, t3, pic_urn, "newcomers who burned their dead", "Strong evidence", g3, GRADE["strong"])
    els += lrow(3, t4, pic_stalk, "why the temple world ended", "Open question", g4, GRADE["open"])
    return els


def s55():
    """What would change our minds: four wanted items in lilac dashes, as named: a temple floor with a glowing 'Ice Age' layer beneath; a
    survey ship over the drowned land with a sonar fan; dice beside a spectrum; an archive box of the few surviving skulls with a DNA
    helix rising from it."""
    t0, ti, ts, tc, td = (T("s55", "What would change"), T("s55", "Something from the Ice"), T("s55", "A sunken temple"), T("s55", "A test of"),
                          T("s55", "And ancient DNA"))
    els = [lab(889, 190, "what would change our minds", t0, GOLD, 30, st="cap")]
    xs = (290, 690, 1090, 1490)
    FL = "rgba(201,193,238,.12)"
    x = xs[0]
    els += [grp([rect(x - 165, 360, 330, 34, FL, LILAC, 3, 4, 0, style="inferred")] +
                [ln([(x - 165 + 66 * k, 360), (x - 165 + 66 * k, 394)], 0, LILAC, 2, "inferred", draw=False) for k in range(1, 5)], ti, "pop"),
            gl(x, 500, 190, ti + .3, .45, "lamp"),
            rect(x - 150, 440, 300, 120, FL, LILAC, 3, 10, ti + .3, style="inferred", fx="pop"),
            lab(x, 512, "Ice Age", ti + .5, LILAC, 30, st="serif", fx="pop"), lab(x, 650, "Ice Age, under a floor", ti + .7, LILAC, 28, fx="pop")]
    x = xs[1]
    els += [ln([(x - 175, 380), (x + 175, 380)], ts, "#9fd0ff", 2.5, "inferred", .4),
            grp([poly([(x - 85, 380), (x - 70, 340), (x + 80, 340), (x + 95, 380)], FL, LILAC, 3, 0, style="inferred"),
                 rect(x - 30, 306, 70, 34, FL, LILAC, 2.5, 4, 0, style="inferred")], ts + .1, "pop"),
            {"k": "fan", "x": x, "y": 386, "a0": 62, "a1": 118, "r": 200, "c": LILAC, "in": ts + .4},
            ln([(x - 175, 590), (x - 80, 572), (x + 20, 594), (x + 175, 578)], ts + .6, LILAC, 3, "inferred", .6, curve=True),
            lab(x, 650, "a sunken temple", ts + .8, LILAC, 28, fx="pop")]
    x = xs[2]
    for k, (ox, oy) in enumerate(((-95, -10), (-15, 24))):
        x0, y0 = x + ox - 42, 440 + oy
        spots = [(.25, .25), (.5, .5), (.75, .75)] if k == 0 else [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)]
        els += [grp([rect(x0, y0, 84, 84, FL, LILAC, 3, 12, 0, style="inferred")] + [circ(x0 + 84 * u, y0 + 84 * v_, 7, LILAC, at=0) for u, v_ in spots],
                    tc + .15 * k, "pop")]
    els += [ln([(x + 50, 560), (x + 72, 560), (x + 84, 450), (x + 96, 560), (x + 116, 500), (x + 128, 560), (x + 160, 560)], tc + .4, LILAC, 3, "inferred", .6),
            lab(x, 650, "a test against chance", tc + .6, LILAC, 28, fx="pop")]
    x = xs[3]
    els += [rect(x - 120, 470, 240, 110, FL, LILAC, 3, 10, td, style="inferred", fx="pop"),
            lab(x, 534, "skulls", td + .2, LILAC, 26, fx="pop")] + helix(x, 290, 455, td + .4, 28, 1.6, LILAC, "#e9e4ff")
    els += [lab(x, 650, "DNA from the skulls", td + .6, LILAC, 28, fx="pop")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s56():
    """The close: the hero again on its own panel, the beam already lying the length of the floor to the niche, warmer and higher; the
    light slowly fills the chamber."""
    els = hero_els(beam=1.2, warm=1.15)
    zs = [ZF - (ZF - 1.6) * k / 12 for k in range(13)]
    els += [poly(beam_quad(z0, z1, DOOR_W * .8), "#fff1d2", at=-1, op=.3) for z0, z1 in zip(zs, zs[1:])]
    els += [gl(VPX, 780, 170, -1, .5, "lamp"), gl(VPX, 520, 700, .6, .35, "lamp", dur=4.0), gl(SUNP[0], SUNP[1], 320, 1.0, .5, "sun", dur=3.0)]
    st = hero_base(); st.update(els=els)
    return st


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
    (0, 0, "hook", "s1", [(0, "It runs down", "s1z"), (1, "This temple", "s2"), (2, "Who built them", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "Malta and Gozo hold", "s6"), (1, "At Hagar", "s7")], {"chapter": "A place of giants"}),
    (1, 1, "collision", "s8", [], {}),
    (1, 2, "reversal", "s9", [(1, "Inside, rounded", "s10"), (1, "There, these farmers", "s11")], {}),
    (1, 3, "tag", "s12", [], {}),
    (2, 0, "world", "s13", [], {"chapter": "Older than the pyramids"}),
    (2, 1, "collision", "s14", [(1, "And anything sealed", "s15")], {}),
    (2, 2, "reversal", "s16", [(1, "In {1973", "s17")], {}),
    (2, 3, "tag", "s18", [], {}),
    (3, 0, "world", "s19", [(1, "Could the temples", "s20"), (1, "In his {2002", "s21"), (2, "His case", "s22")], {"chapter": "Temples under the sea?"}),
    (3, 1, "collision", "s23", [(0, "And while stone", "s24"), (1, "And the plans", "s25")], {}),
    (3, 2, "cost", "s26", [(0, "But under the sea", "s27")], {}),
    (3, 3, "reversal", "s28", [(1, "Sailors, a thousand", "s29")], {}),
    (4, 0, "world", "s30", [(2, "From around {4000", "s31")], {"chapter": "The city of the dead"}),
    (4, 1, "collision", "s32", [], {}),
    (4, 2, "reversal", "s33", [(1, "On some walls", "s34"), (1, "And they carved", "s35")], {}),
    (4, 3, "tag", "s36", [], {}),
    (5, 0, "world", "s37", [], {"chapter": "The room that sings"}),
    (5, 1, "collision", "s38", [(1, "That second idea", "s39")], {}),
    (5, 2, "reversal", "s40", [(1, "But its strongest", "s41")], {}),
    (5, 3, "cost", "s42", [], {}),
    (5, 4, "tag", "s43", [(1, "The room does", "s44")], {}),
    (6, 0, "world", "s45", [], {"chapter": "The end of the temples"}),
    (6, 1, "collision", "s46", [(1, "A great drought", "s47")], {}),
    (6, 2, "reversal", "s48", [(1, "Then, around {2000", "s49")], {}),
    (6, 3, "tag", "s50", [], {}),
    (7, 0, "weigh", "s51", [(1, "Temples from the Ice", "s52"), (2, "A Hypogeum carved", "s53"), (3, "Newcomers who burned", "s54")], {"chapter": "The weighing"}),
    (7, 1, "test", "s55", [], {}),
    (7, 2, "close", "s56", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s1z": ("s1", [1.22, 889, 560], "s1z_add"),
    "s3": ("s1", [1, 889, 500], "s3_add"),
    "s12": ("s5", [1, 889, 500], "s12_add"),
    "s18": ("s13", [1, 889, 500], "s18_add"),
    "s20": ("s19", [1, 889, 500], "s20_add"),
    "s23": ("s21", [1, 889, 500], "s23_add"),
    "s31": ("s30", [1, 889, 500], "s31_add"),
    "s36": ("s35", [1.6, 1222, 450], "s36_add"),
    "s41": ("s38", [1, 889, 500], "s41_add"),
    "s44": ("s37", [1, 889, 500], "s44_add"),
    "s49": ("s48", [1, 889, 500], "s49_add"),
    "s52": ("s51", [1, 889, 500], "s52_add"),
    "s54": ("s53", [1, 889, 500], "s54_add"),
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
    ep = {"id": "lf-malta-temples", "code": "LF.34", "series": script["series"], "title": script["title"], "case": "malta-temples",
          "verdict": "solid", "claim": "Who built Malta's megalithic temples, and when: before the pyramids, or in the Ice Age?", "mood": "mystery",
          "hook_text": "Who built this, and *when*?", "beats": beats, "shots": shots,
          "sources": "Scerri et al. 2025 (doi:10.1038/s41586-025-08780-y) · Groucutt et al. 2022 (doi:10.3389/feart.2021.771683) · "
                     "Ariano et al. 2022 (doi:10.1016/j.cub.2022.04.069) · Till 2017 (doi:10.15184/aqy.2016.258) · "
                     "Wolfe, Swanson & Till 2020 (doi:10.1016/j.jasrep.2020.102623) · Cook et al. 2008 (doi:10.2752/175169608783489099) · "
                     "Mottershead et al. 2008 (doi:10.1017/S0003598X00097787) · Rossi et al. 2025 (doi:10.1002/esp.6061) · "
                     "Stoddart et al. 2022 (doi:10.17863/CAM.91914) · Renfrew 1973, Before Civilization (Jonathan Cape)",
          "post": "Malta's stone temples are older than the pyramids of Giza. The equinox light at Mnajdra, Ġgantija and the giantess of "
                  "Gozo's tales, the radiocarbon revolution, the Ice Age and drowned-temple claims, the cart ruts, the Hypogeum and its "
                  "Oracle Room, and the end of the temple builders, weighed.",
          "hashtags": ["#Malta", "#Megaliths", "#Ggantija", "#Hypogeum", "#Archaeology", "#Underworlds"],
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
