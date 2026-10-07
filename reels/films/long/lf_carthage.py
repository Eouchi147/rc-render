"""LF.35 · Carthage and Before · Carthage: Salt and Ashes (16:9 long film, one wall).

The script is films/long/lf-carthage/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at the
sentence where the picture changes (see BEATS). One scene per script shot (s1..s55; s4, the title, is the intro card over the hero),
drawn while it is said. The hero is the legend itself, drawn in full in the first frame: a plough and its oxen cutting a furrow across
burned ground below the smoking Byrsa, a hand above scattering white grains, the round war harbour in the last light, and the small
standing stones of the tophet in the foreground. Then the rise and fall (Tyre to the New City, Dido's ox hide, 814 BCE against the
radiocarbon of the oldest layers, a map of the rivalry, ten warships against 170 ship sheds, the three streets to the Byrsa, the
survivors, the ten senators), the salt traced upstream like a river (ancient silence, a jurist's plough, al-Bakri, 1299, the
encyclopaedias, 1930, Ridley), the city under the city (a section of the Byrsa: the Punic houses, the burnt layer of 146 BCE, the summit
cut down, the Roman fill and forum; Appian's 'beside' against the digging's 'on top'; 6,000 settlers in 122 BCE; Roman Carthage; grain
for Rome), the tophet (the harbour quarter, urns in layers and 200 marks of 100, a stele with its vow, the writers, the same rite for
lambs and children, the substitution stelae), the bones (two age profiles back to back on one axis, a calendar with its last page torn
out, Zita, a level balance, lamps at dusk), Kerkouane (Cap Bon, the town plan, the DNA of 27 people) and Dougga (the mausoleum, the
bilingual, 22 of 24 signs, Tifinagh, GLD and agellid), the ledger, the test and a night close. Drawings are schematic and true to the
numbers said: solid = measured or recorded, dashed = inferred, dotted lilac = claimed. The infants' remains are never drawn: urns,
stelae, hands and light only. Libyan signs are schematic; the Tifinagh panel uses only shapes the two scripts share (circle, cross, two
bars, one bar), and the word for king is shown as scholars transliterate it (GLD), not as invented glyphs.

Facts: the script's facts_added (Docter et al. 2008; Justin 18.5; Ridley 1986; Stevens 1988; Visona 1988; Warmington 1988; Saladin 2026; Digest 7.4.21; Appian,
Punica 96, 127-136 and Civil Wars 1.24; Polybius 15.18; Florus 1.31; Orosius 4.23; Diodorus 20.14; Hurst & Stager 1978; Hurst 1994,
2010; Goiran et al. 2025; Lancel 1995; Stager & Wolff 1984; Schwartz et al. 2010, 2012, 2017; Smith et al. 2011, 2013; Xella et al.
2013; Cerezo-Roman et al. 2024; Pilkington 2023; Garnand & Greene 2023; Amadasi Guzzo & Zamora 2013; Carcopino 1932; Ringbauer et
al. 2025; UNESCO WHC 332; Fantar 1984-86; British Museum 1852,0305.1-2; de Saulcy 1843; Josephus, Jewish War 2.383).

Engine workaround (as in lf_stonehenge.py, lf_troy.py and lf_antikythera.py): the wall only adds elements to a panel on its first
visit, at a beat start or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique
tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item
(built on that step's clock). Build-ins inside a sentence are timed with a speech clock (T(): the script's own words at about 4.25
syllables a second).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-carthage/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-carthage/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-carthage RC_FILMS_EPS=/tmp/claude-0/sbx_lf-carthage/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-carthage/boards python3 films.py long.lf_carthage
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-carthage", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
PUNIC = "#b85a3c"            # terracotta: Punic Carthage
ROMAN = "#d0564a"            # Roman red
SEAC, SEAL = "#3f86b0", "#9fd0ff"
SALT = "#f5f1e6"
ASH, ASH2 = "#17110d", "#2a1f17"
EMBER, FIRE = "#ff8a4a", "#ffb35c"
LIME, LIME_L, LIME_D = "#d8c9a8", "#f0e4c8", "#8f7f66"     # limestone: mid, lit, shade
CLAY, CLAY_L, CLAY_D = "#b88b5e", "#e0c49a", "#6e4c2e"     # urns
EARTH, EARTH_D = "#5a4632", "#3a2c1f"
WOOD, WOOD_D = "#7a5434", "#46301e"
SKIN = "#e8d6b8"
PURPLE = "#8a4fb0"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#f2c98e", "open": "#c9c1ee", "mixed": "#e8b87a",
         "awaiting": "#9fd0ff", "ruled": "#ff8a7a"}


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


def chip(x, y, t, c, at, size=28, a="middle", z=1.0, style="known"):
    """A pill with a coloured rim and its words (grades, dates); z = the camera zoom it is seen at (the rim scales with the camera,
    the words keep their size)."""
    w = (len(t) * size * .56 + 44) / z
    h = size * 1.7 / z
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    rim = rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop")
    if style != "known":
        rim["style"] = style
    return [rim, label(round(x0 + w / 2, 1), round(y + size * .36 / z, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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


def xf(pts, x, y, s, fl=1):
    """Unit-shape points to the panel: (u, v) -> (x + fl*u*s, y + v*s)."""
    return [(x + fl * u * s, y + v * s) for u, v in pts]


# ================================================================== figures
def fig(x, y, h, at, c="#1a1410", arms=None, face=1, fx="rise", op=None, lean=0.0, robe=False):
    """A standing figure, feet on y, facing `face`: arms None (down), 'point', 'up', 'pull' (both forward and low), 'lift', 'hold'
    (forearms forward, carrying). lean > 0 tilts the body forward. robe=True draws a long garment to the ankles (a toga)."""
    f = face
    X = lambda a, b=0: x + f * (a * h + lean * b * h)
    Y = lambda b: y - b * h
    els = [circ(X(.01, .9), Y(.9), .085 * h, c, at=at),
           poly([(X(-.13, .78), Y(.78)), (X(.13, .78), Y(.78)), (X(.11, .44), Y(.44)), (X(-.11, .44), Y(.44))], c, at=at)]
    if robe:
        els += [poly([(X(-.12, .46), Y(.46)), (X(.12, .46), Y(.46)), (X(.16), Y(.02)), (X(-.16), Y(.02))], c, at=at)]
    else:
        els += [poly([(X(-.11, .46), Y(.46)), (X(.11, .46), Y(.46)), (X(.085), Y(0)), (X(.025), Y(0)), (X(0, .3), Y(.3)), (X(-.025), Y(0)), (X(-.085), Y(0))], c, at=at)]
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
    elif arms == "hold":
        els += [ln([(X(-.08, .76), Y(.76)), (X(.0, .55), Y(.55)), (X(.2, .56), Y(.56))], at, c, aw, draw=False),
                ln([(X(.1, .76), Y(.76)), (X(.14, .56), Y(.56)), (X(.26, .58), Y(.58))], at, c, aw, draw=False)]
    e = grp(els, at, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return [e]


def soldier(x, y, h, at, face=1, c="#1a1410", fx="rise"):
    """A Roman soldier in silhouette: a figure with a crested helmet (red crest), a round-topped shield and a spear."""
    f = face
    els = fig(x, y, h, at, c, "point", face, fx=None)[0]["els"]
    els += [poly([(x + f * (-.07 * h), y - .97 * h), (x + f * (.0 * h), y - 1.05 * h), (x + f * (.09 * h), y - .97 * h), (x + f * (.0 * h), y - .93 * h)], ROMAN, at=at),
            poly(E(x + f * .16 * h, y - .55 * h, .09 * h, .2 * h, 16), "#5a2a22", "#c86a52", 1.2, at),
            ln([(x + f * .3 * h, y - .2 * h), (x + f * .42 * h, y - 1.15 * h)], at, "#cbbca8", max(1.5, .02 * h), draw=False)]
    return [grp(els, at, fx)]


def capsule(x0, y0, x1, y1, w0, w1=None, n=6):
    """A tapered rounded stroke from (x0, y0) (width w0) to (x1, y1) (width w1) as a closed outline (fingers, horns, legs)."""
    w1 = w0 if w1 is None else w1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    a = math.atan2(dy, dx)
    pts = [(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2)]
    for k in range(1, n):
        t = a + math.pi / 2 - math.pi * k / n
        pts.append((x1 + math.cos(t) * w1 / 2, y1 + math.sin(t) * w1 / 2))
    pts += [(x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)]
    for k in range(1, n):
        t = a - math.pi / 2 - math.pi * k / n
        pts.append((x0 + math.cos(t) * w0 / 2, y0 + math.sin(t) * w0 / 2))
    return pts


def ox(x, y, s, at=-1, face=-1, c="#120d0a", rim="rgba(255,176,112,.65)", belly="rgba(255,150,90,.18)"):
    """An ox in side view, hooves on y, facing `face` (-1 = left); s = body length (tail to muzzle). A hump at the withers, a dewlap,
    horns curving forward, four jointed legs; warm rim light along the back."""
    f = face
    P = lambda u, v: (x + f * u * s, y - v * s)
    body = [P(-.55, .6), P(-.3, .63), P(0, .63), P(.18, .66), P(.28, .73), P(.37, .72), P(.47, .64), P(.58, .6), P(.66, .57), P(.74, .46),
            P(.79, .36), P(.77, .31), P(.7, .3), P(.62, .34), P(.54, .37), P(.46, .34), P(.4, .27), P(.32, .25), P(.15, .27), P(-.1, .26),
            P(-.32, .28), P(-.47, .31), P(-.56, .42)]
    els = [poly(body, c, at=at, curve=True)]
    for (u0, v0, u1, v1) in ((.37, .3, .36, .0), (.28, .28, .29, .0), (-.36, .32, -.37, .0), (-.46, .34, -.45, .0)):
        km = (u0 + u1) / 2 + (.02 if u0 > 0 else -.025)
        els += [poly(capsule(*P(u0, v0), *P(km, .13), .075 * s, .045 * s), c, at=at), poly(capsule(*P(km, .13), *P(u1, v1 + .02), .042 * s, .034 * s), c, at=at),
                rect(P(u1, 0)[0] - .025 * s, y - .03 * s, .05 * s, .03 * s, "#050403", at=at)]
    els += [poly(capsule(*P(.63, .58), *P(.75, .67), .045 * s, .02 * s), "#d9c7a6", at=at),
            poly(capsule(*P(.75, .67), *P(.79, .74), .022 * s, .01 * s), "#efe2c8", at=at),
            poly([P(.58, .57), P(.53, .62), P(.6, .6)], c, at=at),
            poly(capsule(*P(-.55, .55), *P(-.6, .2), .025 * s, .018 * s), c, at=at), poly(E(*P(-.6, .17), .02 * s, .04 * s, 10), c, at=at)]
    els += [ln([P(-.55, .6), P(-.3, .63), P(0, .63), P(.18, .66), P(.28, .73), P(.37, .72), P(.47, .64), P(.58, .6), P(.66, .57)], at, rim, max(1.5, .012 * s), curve=True, draw=False),
            ln([P(.4, .27), P(.32, .25), P(.15, .27), P(-.1, .26)], at, belly, max(1.5, .01 * s), curve=True, draw=False),
            circ(*P(.7, .47), max(1.2, .009 * s), "#ffcf9a", at=at, op=.8)]
    return els


def ard(sx, sy, yx, yy, at=-1, face=-1, c=WOOD, rim="rgba(255,200,140,.6)", hl=None):
    """A Roman ard (scratch plough) in side view: the share in the soil at (sx, sy), a straight beam up to the yoke at (yx, yy), the
    handle rising behind the share (away from the oxen) to height hl."""
    hl = hl or abs(yx - sx) * .55
    f = face
    hx, hy = sx - f * hl * .42, sy - hl
    return [ln([(sx, sy - 6), (yx, yy)], at, "#3a2616", 9, draw=False), ln([(sx, sy - 8), (yx, yy - 3)], at, rim, 1.6, draw=False),
            poly([(sx + f * 26, sy + 4), (sx - f * 22, sy - 10), (sx - f * 16, sy + 6)], "#9a948a", "#e8e2d8", 1, at),
            ln([(sx - f * 6, sy - 4), (hx, hy)], at, "#3a2616", 8, draw=False), ln([(sx - f * 6, sy - 6), (hx, hy - 2)], at, rim, 1.4, draw=False),
            ln([(hx, hy), (hx - f * 26, hy + 6)], at, "#3a2616", 7, draw=False)]


def hand_down(x, y, s, at=-1, c="#e0bb92", shade="#a8784e", sleeve="#6e3226", fx=None):
    """A hand reaching in from the upper right, palm down, fingers parted, scattering grains; (x, y) = under the fingertips; s = hand
    length. Skin lit warm from below by the fires, a tunic sleeve over the forearm."""
    P = lambda u, v: (x + u * s, y + v * s)
    fore = capsule(*P(1.9, -1.2), *P(.7, -.34), .46 * s, .32 * s)
    sl = [P(3.4, -2.6), P(1.2, -.92), P(1.02, -.58), P(1.28, -.42), P(3.6, -2.1)]
    palm = [P(.12, -.1), P(.3, -.3), P(.52, -.46), P(.78, -.46), P(.9, -.26), P(.74, -.04), P(.52, .05), P(.28, .06), P(.12, .02)]
    els = [poly(fore, c, "rgba(120,80,50,.4)", 1.2, at), poly(sl, sleeve, "rgba(255,200,150,.45)", 1.4, at),
           ln([P(1.02, -.58), P(1.28, -.42)], at, "rgba(255,210,170,.55)", 3, draw=False),
           ln([P(1.5, -1.2), P(1.62, -.98), P(1.66, -.8)], at, "rgba(0,0,0,.3)", 2.4, curve=True, draw=False),
           ln([P(1.95, -1.52), P(2.1, -1.3), P(2.12, -1.14)], at, "rgba(0,0,0,.28)", 2.4, curve=True, draw=False),
           poly(palm, c, "rgba(120,80,50,.5)", 1.2, at, curve=True)]
    for (u0, v0, u1, v1, w0, w1) in ((.16, .0, -.06, .22, .13, .085), (.29, .04, .16, .35, .13, .09), (.42, .05, .36, .37, .125, .088), (.55, .03, .55, .27, .11, .078)):
        els.append(poly(capsule(*P(u0, v0), *P(u1, v1), w0 * s, w1 * s), c, "rgba(120,80,50,.45)", 1, at))
    els += [poly(capsule(*P(.78, -.1), *P(.76, .14), .15 * s, .1 * s), c, "rgba(120,80,50,.45)", 1, at),
            ln([P(.2, .03), P(.48, .06), P(.7, -.02)], at, shade, 2.4, curve=True, draw=False, op=.6),
            ln([P(.36, -.3), P(.64, -.44), P(1.0, -.6)], at, "rgba(255,236,214,.6)", 2, curve=True, draw=False)]
    return [grp(els, at, fx)] if fx else els


def urn(x, y, h, at=-1, c=CLAY, fx="pop", lid=True, rim=CLAY_L):
    """A small tophet urn standing on y (a round body, a short neck, two small handles, often a lid); h = its height."""
    P = lambda u, v: (x + u * h, y - v * h)
    body = [P(-.06, 0), P(.06, 0), P(.2, .1), P(.28, .3), P(.26, .52), P(.17, .66), P(.11, .74), P(.12, .82), P(-.12, .82), P(-.11, .74),
            P(-.17, .66), P(-.26, .52), P(-.28, .3), P(-.2, .1)]
    els = [poly(body, c, rim, 1.2, at, curve=True)]
    els += [ln([P(.17, .66), P(.26, .7), P(.24, .58)], at, rim, 1.6, draw=False, curve=True), ln([P(-.17, .66), P(-.26, .7), P(-.24, .58)], at, rim, 1.6, draw=False, curve=True)]
    if lid:
        els += [poly([P(-.14, .82), P(.14, .82), P(.1, .9), P(-.1, .9)], mix(c, "#000000", .15), rim, 1, at)]
    els += [ln([P(-.2, .36), P(.2, .36)], at, "rgba(60,30,15,.35)", 1.4, draw=False)]
    return [grp(els, at, fx)] if fx else els


def tanit(x, y, s, at=-1, c=LIME_L, w=None, fx=None):
    """The sign of Tanit: a triangle (the body), a bar with raised ends (the arms) and a disc (the head); (x, y) = the foot centre,
    s = its height."""
    w = w or max(2.5, s * .06)
    els = [poly([(x, y - .62 * s), (x - .3 * s, y), (x + .3 * s, y)], c, at=at),
           ln([(x - .34 * s, y - .5 * s), (x - .3 * s, y - .62 * s), (x + .3 * s, y - .62 * s), (x + .34 * s, y - .5 * s)], at, c, w, draw=False),
           circ(x, y - .8 * s, .13 * s, c, at=at)]
    return [grp(els, at, fx)] if fx else els


def raised_hand(x, y, s, at=-1, c=LIME_L, fx=None):
    """An open right hand raised, palm forward (carved on many stelae): (x, y) = the wrist, s = its height."""
    P = lambda u, v: (x + u * s, y - v * s)
    palm = [P(-.2, 0), P(.2, 0), P(.24, .42), P(-.24, .42)]
    els = [poly(palm, c, at=at, curve=False)]
    for k, (u, L) in enumerate(((-.18, .38), (-.06, .46), (.06, .44), (.17, .36))):
        els.append(ln([P(u, .4), P(u, .4 + L)], at, c, max(3, .1 * s), draw=False))
    els.append(ln([P(.22, .14), P(.38, .34)], at, c, max(3, .1 * s), draw=False))
    return [grp(els, at, fx)] if fx else els


def punic_letters(x0, y, n, at, c=LIME_D, s=18, seed=3, w=2.2, step=None):
    """A line of schematic Punic letters (strokes, not real text), right to left from x0+n*step to x0."""
    r = random.Random(seed)
    step = step or s * 1.05
    shapes = [[(-.4, -.5), (.3, -.2), (-.3, .1), (.3, .5)], [(-.35, -.45), (.35, -.45), (.35, 0), (-.2, 0), (.15, .5)], [(0, -.5), (0, .3), (-.35, .5)],
              [(-.4, -.25), (-.15, .15), (.1, -.25), (.35, .15), (.35, .5)], [(-.35, -.5), (-.35, .5), (.3, .5)], [(.3, -.5), (-.3, -.1), (.3, .3)],
              [(-.3, -.5), (.3, -.5), (0, .5)], [(-.3, .5), (0, -.5), (.3, .5)]]
    out = []
    for k in range(n):
        sh = shapes[r.randrange(len(shapes))]
        cx = x0 + (n - 1 - k) * step
        out.append(ln([(cx + u * s, y + v * s) for u, v in sh], at, c, w, draw=False))
    return out


def libyan_sign(kind, x, y, s, at, c=BONE, w=3.2):
    """A geometric sign in the manner of the Libyco-Berber letters (schematic): circle, bars, cross, square, dots, angle, two dots."""
    if kind == 0:
        return [circ(x, y, s * .45, "none", c, w, at)]
    if kind == 1:
        return [ln([(x - s * .5, y - s * .18), (x + s * .5, y - s * .18)], at, c, w, draw=False), ln([(x - s * .5, y + s * .18), (x + s * .5, y + s * .18)], at, c, w, draw=False)]
    if kind == 2:
        return [ln([(x - s * .45, y), (x + s * .45, y)], at, c, w, draw=False), ln([(x, y - s * .45), (x, y + s * .45)], at, c, w, draw=False)]
    if kind == 3:
        return [rect(x - s * .38, y - s * .38, s * .76, s * .76, "none", c, w, 2, at)]
    if kind == 4:
        return [circ(x, y - s * .32, s * .08, c, at=at), circ(x, y, s * .08, c, at=at), circ(x, y + s * .32, s * .08, c, at=at)]
    if kind == 5:
        return [ln([(x - s * .4, y + s * .4), (x, y - s * .4), (x + s * .4, y + s * .4)], at, c, w, draw=False)]
    if kind == 6:
        return [ln([(x, y - s * .5), (x, y + s * .5)], at, c, w, draw=False)]
    if kind == 8:
        return [ln([(x - s * .18, y - s * .5), (x - s * .18, y + s * .5)], at, c, w, draw=False), ln([(x + s * .18, y - s * .5), (x + s * .18, y + s * .5)], at, c, w, draw=False)]
    return [circ(x - s * .2, y, s * .08, c, at=at), circ(x + s * .2, y, s * .08, c, at=at)]


def stele(x, y, w, h, at=-1, c=LIME, rim=LIME_L, sign=True, hand=False, crescent=True, lines=2, fx="rise", seed=1, op=None, glow_=False):
    """A tophet stele standing on y: a limestone slab with a pointed top (pediment), carved with the sign of Tanit, optionally a raised
    hand, a crescent over a disc, and lines of schematic letters. w x h = its size."""
    top = y - h
    shape = [(x - w / 2, y), (x - w / 2, top + w * .5), (x, top), (x + w / 2, top + w * .5), (x + w / 2, y)]
    els = [poly(shape, c, rim, max(1, w * .02), at)]
    els += [poly([(x - w / 2, y), (x - w / 2, top + w * .5), (x - w * .38, top + w * .5 + w * .06), (x - w * .38, y)], "rgba(0,0,0,.18)", at=at)]
    cy = top + w * .62
    if crescent:
        els += [circ(x, cy, w * .07, LIME_D, at=at), ln([(x - w * .14, cy - w * .1), (x, cy + w * .05), (x + w * .14, cy - w * .1)], at, LIME_D, max(1.5, w * .025), draw=False, curve=True)]
        cy += w * .25
    if hand:
        els += raised_hand(x, cy + w * .48, w * .45, at, LIME_D)
        cy += w * .55
    if sign:
        els += tanit(x, cy + w * .55, w * .5, at, LIME_D)
        cy += w * .62
    for k in range(lines):
        yy = cy + w * .12 + k * w * .2
        if yy < y - w * .1:
            els += punic_letters(x - w * .36, yy, 5, at, LIME_D, w * .11, seed + k, max(1.2, w * .02), step=w * .16)
    e = grp(els, at, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return [e]


def lamp(x, y, s, at, glow_op=.6, fx="pop"):
    """A small clay oil lamp on y with its flame and a warm glow."""
    els = [poly(E(x, y - s * .18, s * .5, s * .2, 18), CLAY_D, CLAY_L, 1, at), poly([(x + s * .4, y - s * .28), (x + s * .62, y - s * .32), (x + s * .5, y - s * .18)], CLAY_D, at=at),
           poly([(x + s * .56, y - s * .34), (x + s * .5, y - s * .62), (x + s * .64, y - s * .44)], FIRE, at=at, curve=True)]
    return [gl(x + s * .56, y - s * .45, s * 3.2, at, glow_op, "fire"), grp(els, at, fx)]


def galley(x, y, w, at=-1, c="#5a3c26", oars=True, fx="pop", rim="#e7c99a"):
    """A war galley in side view on the waterline y, bow to the left: a long hull with a bronze ram, an eye at the bow, a curling stern
    post, a row of shields along the rail and a bank of oars."""
    h = w * .13
    hull = [(x - w * .5, y - h * .1), (x - w * .62, y + h * .2), (x - w * .46, y + h * .45), (x + w * .36, y + h * .4), (x + w * .48, y - h * .2),
            (x + w * .54, y - h * 1.5), (x + w * .5, y - h * 1.9), (x + w * .45, y - h * 1.4), (x + w * .4, y - h * .7), (x - w * .4, y - h * .7), (x - w * .5, y - h * .5)]
    els = [poly(hull, c, rim, 1.2, at), poly([(x - w * .62, y + h * .2), (x - w * .72, y + h * .25), (x - w * .6, y + h * .38)], "#c99a4a", at=at),
           circ(x - w * .43, y - h * .25, max(1.5, h * .14), "#efe2c8", at=at)]
    if oars:
        for k in range(11):
            ox_ = x - w * .34 + k * w * .066
            els.append(ln([(ox_, y - h * .2), (ox_ - w * .05, y + h * 1.3)], at, rim, max(1.2, w * .007), draw=False))
    for k in range(9):
        els.append(circ(x - w * .3 + k * w * .075, y - h * .72, max(2, h * .2), "#8a5a36", rim, 1, at))
    return [grp(els, at, fx)] if fx else els


def scroll(x, y, w, at, c=LIME_L, fx="pop", lines=3, open_=True):
    """A scroll (an ancient book) seen from the front: two rollers and a sheet with text lines."""
    h = w * .62
    els = []
    if open_:
        els += [rect(x - w / 2, y - h / 2, w, h, c, "#8a7a66", 1.5, 3, at)]
        for k in range(lines):
            els.append(ln([(x - w * .36, y - h * .25 + k * h * .22), (x + w * .36 - (k % 2) * w * .12, y - h * .25 + k * h * .22)], at, "#8a7a66", 2, draw=False))
    els += [rect(x - w / 2 - w * .08, y - h * .62, w * .1, h * 1.24, WOOD, "#e7c99a", 1, w * .05, at), rect(x + w / 2 - w * .02, y - h * .62, w * .1, h * 1.24, WOOD, "#e7c99a", 1, w * .05, at)]
    return [grp(els, at, fx)] if fx else els


def book(x, y, w, at, c="#6d4a2e", page="#efe4cc", fx="pop", thick=False):
    """A closed or open codex seen from the front: (x, y) = its centre."""
    h = w * 1.3
    els = [rect(x - w / 2, y - h / 2, w, h, c, "#e7c99a", 1.5, 4, at), rect(x - w / 2 + w * .08, y - h / 2, w * .06, h, "rgba(0,0,0,.25)", at=at)]
    els += [ln([(x - w * .25, y - h * .3), (x + w * .3, y - h * .3)], at, GOLD, 2, draw=False), ln([(x - w * .25, y - h * .22), (x + w * .2, y - h * .22)], at, GOLD, 1.5, draw=False)]
    if thick:
        els += [rect(x + w / 2, y - h / 2 + 4, w * .1, h - 8, page, at=at)]
    return [grp(els, at, fx)] if fx else els


def flame(x, y, s, at, fx="pop"):
    els = [poly([(x - s * .3, y), (x - s * .38, y - s * .4), (x - s * .1, y - s * .7), (x, y - s), (x + s * .12, y - s * .62), (x + s * .36, y - s * .42), (x + s * .3, y)], "#ff7a3a", "#ffd08a", 1.2, at, curve=True),
           poly([(x - s * .14, y), (x - s * .12, y - s * .32), (x, y - s * .55), (x + s * .12, y - s * .3), (x + s * .14, y)], "#ffd27a", at=at, curve=True)]
    return [gl(x, y - s * .4, s * 1.6, at, .5, "fire"), grp(els, at, fx)]


def broken_wall(x, y, s, at, c=LIME_D, fx="pop"):
    els = [poly([(x - s * .5, y), (x - s * .5, y - s * .6), (x - s * .3, y - s * .52), (x - s * .2, y - s * .8), (x, y - s * .55), (x + s * .1, y - s * .7),
                 (x + s * .28, y - s * .4), (x + s * .5, y - s * .45), (x + s * .5, y)], c, "#d8c9a8", 1.2, at)]
    for k in range(3):
        els.append(ln([(x - s * .5, y - s * (.15 + .18 * k)), (x + s * .5, y - s * (.15 + .18 * k))], at, "rgba(30,20,10,.5)", 1.2, draw=False))
    return [grp(els, at, fx)]


def barred_gate(x, y, s, at, c=GOLD, fx="pop"):
    els = [ln([(x - s * .45, y), (x - s * .45, y - s * .7), (x, y - s * .95), (x + s * .45, y - s * .7), (x + s * .45, y)], at, c, max(3, s * .05), draw=False)]
    els += [ln([(x + u * s, y - s * .02), (x + u * s, y - s * (.78 - abs(u) * .4))], at, c, max(2, s * .03), draw=False) for u in (-.25, 0, .25)]
    els += [ln([(x - s * .45, y - s * .4), (x + s * .45, y - s * .4)], at, c, max(2, s * .03), draw=False)]
    return [grp(els, at, fx)]


def salt_pinch(x, y, s, at, c=SALT, n=9, seed=5, fx="pop"):
    r = random.Random(seed)
    els = [circ(x + r.uniform(-s, s), y + r.uniform(-s * .5, s * .5), r.uniform(2.2, 3.6), c, at=at) for _ in range(n)]
    return [grp(els, at, fx)]


def plough_icon(x, y, s, at, c=GOLD, fx="pop"):
    els = [ln([(x - s * .5, y + s * .15), (x + s * .1, y - s * .05), (x + s * .55, y - s * .3)], at, c, max(3, s * .07), draw=False),
           poly([(x - s * .62, y + s * .2), (x - s * .38, y + s * .12), (x - s * .42, y + s * .26)], c, at=at),
           ln([(x - s * .5, y + s * .15), (x - s * .62, y - s * .3)], at, c, max(3, s * .06), draw=False)]
    return [grp(els, at, fx)]


# ================================================================== 0 · cold open: the legend, drawn in full
HERO_GROUND = 560


def byrsa_hill():
    """The Byrsa in silhouette at dusk: a flat-topped hill (x 150..1060, top near y 290) with the citadel wall and a broken temple on
    the summit, burned houses in terraces down its slopes, and the lower city spreading towards the harbour."""
    hill = [(140, 568), (210, 540), (300, 470), (380, 400), (450, 340), (520, 306), (600, 294), (700, 292), (790, 300), (850, 326), (910, 384),
            (970, 450), (1030, 520), (1080, 568)]
    els = [poly(hill, "#251b16", "rgba(255,170,110,.4)", 1.6, -1, curve=True)]
    # the citadel wall along the summit, crenellated
    wall = [(505, 312)]
    for k in range(18):
        x = 505 + k * 17
        top = 286 if k % 2 == 0 else 293
        wall += [(x, top), (x + 17, top)]
    wall += [(811, 312)]
    els.append(poly(wall, "#2e231d", "rgba(255,190,130,.5)", 1.2, -1))
    # the temple on the summit: a podium and broken columns
    els += [rect(580, 270, 170, 18, "#30251f", "rgba(255,190,130,.5)", 1, 2, -1)]
    for k, hgt in enumerate((58, 44, 62, 20, 54, 32)):
        els.append(rect(592 + k * 28, 270 - hgt, 10, hgt, "#33281f", "rgba(255,200,140,.55)", 1, 1, -1))
    els.append(poly([(586, 212), (640, 196), (690, 214)], "#33281f", "rgba(255,200,140,.4)", 1, -1))
    r = random.Random(11)
    # burned houses in terraces down the slopes, windows lit by the fires inside
    for k in range(34):
        x = r.uniform(230, 1020)
        top = 300 + max(0, abs(x - 650) - 120) ** 1.45 * .05 + 16
        w, h = r.uniform(24, 46), r.uniform(26, 56)
        y1 = top + r.uniform(10, 70)
        if y1 > 560 or y1 - h < 300:
            continue
        brk = [(x, y1), (x, y1 - h), (x + w * .3, y1 - h - r.uniform(-6, 8)), (x + w * .55, y1 - h + r.uniform(4, 14)), (x + w * .8, y1 - h - r.uniform(0, 6)),
               (x + w, y1 - h + r.uniform(6, 12)), (x + w, y1)]
        els.append(poly(brk, "#1b1411", "rgba(255,160,100,.3)", 1, -1))
        if k % 3 == 0:
            els.append(rect(x + w * .3, y1 - h * .55, w * .2, h * .28, "#ff9a4a", at=-1, op=.8))
    # the lower city on the plain, burned, towards the harbour
    for k in range(16):
        x = 960 + k * 26 + r.uniform(-6, 6)
        h = r.uniform(16, 38)
        els.append(poly([(x, 566), (x, 566 - h), (x + 9, 566 - h - 6), (x + 16, 566 - h + 4), (x + 22, 566 - h), (x + 22, 566)], "#1d1512", "rgba(255,160,100,.3)", 1, -1))
        if k % 4 == 1:
            els.append(rect(x + 7, 566 - h * .6, 6, 7, "#ff9a4a", at=-1, op=.75))
    return els


def smoke(path, r0, r1, seed, op=.6):
    """A billowing plume of smoke along `path` (bottom to top): overlapping puffs growing from r0 to r1, lit orange at the bottom."""
    r = random.Random(seed)
    els = []
    n = 14
    for k in range(n):
        t = k / (n - 1)
        i = min(len(path) - 2, int(t * (len(path) - 1)))
        u = t * (len(path) - 1) - i
        x = path[i][0] + (path[i + 1][0] - path[i][0]) * u + r.uniform(-10, 10)
        y = path[i][1] + (path[i + 1][1] - path[i][1]) * u + r.uniform(-6, 6)
        rad = r0 + (r1 - r0) * t ** .9
        c = mix("#7a4a34", "#4a4446", min(1, t * 2.2))
        els.append(circ(x, y, rad, c, at=-1, op=round(op * (1 - .45 * t), 2)))
        if t < .4:
            els.append(circ(x - rad * .2, y + rad * .2, rad * .6, "#c8683a", at=-1, op=round(.25 * (1 - t / .4), 2)))
    return els


def harbour_far(cx=1460, cy=600):
    """The round war harbour seen low across the plain at dusk: its outer quay, the ring of water holding the last light, the island
    with the admiral's tower, ship sheds as pale ticks round the far rim; the channel to the sea."""
    els = [poly(E(cx, cy, 206, 36, 60), "#1d1611", "rgba(255,210,160,.35)", 1, -1),
           poly(E(cx, cy, 186, 29, 60), "#3a2f30", at=-1),
           poly(E(cx, cy - 6, 172, 19, 60, 180, 360), "rgba(255,190,130,.55)", at=-1),
           poly(E(cx, cy + 4, 172, 22, 60, 0, 180), "rgba(120,90,90,.6)", at=-1),
           poly(E(cx, cy, 52, 9, 30), "#2a201a", "rgba(255,210,160,.55)", 1, -1),
           rect(cx - 8, cy - 26, 16, 22, "#2a201a", "rgba(255,210,160,.6)", 1, 1, -1)]
    for k in range(46):
        a = math.pi + math.pi * k / 45
        x0, y0 = cx + 188 * math.cos(a), cy + 30 * math.sin(a)
        els.append(ln([(x0, y0), (x0, y0 - 7)], -1, "rgba(255,224,180,.55)", 1.4, draw=False))
    els += [poly([(cx + 150, cy + 20), (cx + 178, cy + 16), (cx + 300, cy - 30), (cx + 290, cy - 36)], "rgba(255,186,120,.35)", at=-1)]
    return els


def hero_els():
    els = []
    # far sea along the horizon at the right, the sun's haze, the haze of the fires over the plain
    els += [poly([(1060, 563), (1778, 563), (1778, 575), (1060, 570)], "rgba(255,190,130,.3)", at=-1),
            gl(1600, 520, 460, -1, .35, "sun"), rect(0, 548, W_, 40, "#f08a4a", at=-1, op=.07)]
    els += smoke([(670, 300), (730, 244), (810, 198), (900, 160)], 22, 70, 3, .7)
    els += smoke([(760, 318), (830, 260), (920, 210), (1040, 170)], 26, 80, 5, .65)
    els += smoke([(900, 410), (980, 340), (1080, 270), (1200, 220)], 20, 70, 7, .5)
    els += byrsa_hill()
    for x, y, r_, op in ((620, 300, 90, .75), (740, 310, 100, .8), (520, 340, 70, .6), (880, 400, 80, .65), (420, 410, 70, .55), (990, 500, 80, .6),
                         (330, 480, 60, .45), (1150, 545, 70, .5)):
        els.append(gl(x, y, r_, -1, op, "fire", pulse=True))
    els += harbour_far()
    # the burned plain: ash, charred debris, embers
    r = random.Random(21)
    for k in range(30):
        x, y = r.uniform(90, 1700), r.uniform(605, 800)
        els.append(poly(E(x, y, r.uniform(24, 80), r.uniform(4, 9), 14), "rgba(70,60,56,.28)" if k % 3 == 0 else "rgba(6,4,3,.5)", at=-1))
    for k in range(22):
        x, y = r.uniform(120, 1680), r.uniform(600, 795)
        els.append(rect(x, y, r.uniform(8, 22), r.uniform(3, 6), "#2b1d14", at=-1))
    for k in range(46):
        x, y = r.uniform(100, 1700), r.uniform(330, 795)
        els.append(circ(x, y, r.uniform(1.4, 2.8), "#ff9a4a", at=-1, op=round(r.uniform(.4, .95), 2)))
    # the furrow behind the plough, running back towards the viewer
    fur = [(880, 728), (1040, 740), (1220, 758), (1400, 784), (1600, 812), (1740, 830)]
    els += [ln([(x, y + 7) for x, y in fur], -1, "#060403", 20, draw=False, curve=True), ln([(x, y - 5) for x, y in fur], -1, "#6a5038", 3, draw=False, curve=True),
            ln([(x, y + 17) for x, y in fur], -1, "#3a2b1e", 2, draw=False, curve=True)]
    # the tophet's small stones in the left foreground, two tiny lamps
    for k, (x, y, h, tilt) in enumerate(((140, 794, 62, -3), (196, 800, 48, 2), (240, 790, 70, 0), (300, 798, 44, 4), (350, 788, 58, -2), (178, 770, 40, 0))):
        st = stele(x, y, h * .44, h, -1, "#3d332b", "rgba(255,210,160,.4)", sign=(k % 2 == 0), crescent=False, lines=0, fx=None)
        els.append({"k": "group", "tr": "rotate(%d %d %d)" % (tilt, x, y), "els": st, "in": -1})
    for x, y in ((214, 796), (326, 796)):
        els += [gl(x, y - 4, 46, -1, .6, "fire", pulse=True), circ(x, y - 4, 3.2, "#ffd27a", at=-1)]
    # the plough team: two oxen, the yoke, the ard and the ploughman (moving left)
    els += [gl(660, 610, 330, -1, .38, "fire"), poly(E(700, 640, 330, 70, 30), "rgba(255,150,90,.07)", at=-1)]
    els += ox(704, 706, 212, -1, -1, "#140e0b", "rgba(255,170,110,.5)")
    els += ard(880, 728, 528, 566, -1, -1, hl=110)
    els += ox(640, 720, 232, -1, -1, "#2c1e15", "rgba(255,196,130,.95)", "rgba(255,170,110,.35)")
    els += [ln([(496, 566), (512, 554), (548, 552), (562, 562)], -1, "#4a3020", 9, curve=True, draw=False), ln([(498, 562), (512, 551), (548, 549), (560, 558)], -1, "rgba(255,200,140,.7)", 1.6, curve=True, draw=False)]
    els += [lab(300, 640, "Carthage, 146 BCE", 1.0, GOLD, 30)]
    els += fig(986, 734, 172, -1, "#21170f", "pull", -1, fx=None, lean=.06)
    els += [ln([(986 + .14 * 172, 734 - .78 * 172), (986 + .12 * 172, 734 - .45 * 172), (986 + .09 * 172, 734)], -1, "rgba(255,180,120,.5)", 2, draw=False)]
    els += [ln([(986 - .02 * 172, 734 - .9 * 172 - 14), (986 + .03 * 172, 734 - .9 * 172 - 16)], -1, "rgba(255,190,130,.5)", 2, draw=False)]
    # the hand above the furrow, scattering salt
    els += hand_down(1290, 336, 140, -1)
    r = random.Random(7)
    for k in range(90):
        t = r.random()
        x = 1290 - 26 * t + r.uniform(-14, 14) * (.25 + t)
        y = 372 + t * 392
        els.append(circ(x, y, round(r.uniform(1.6, 3.2), 1), SALT, at=-1, op=round(r.uniform(.55, 1), 2)))
    els += [gl(1268, 760, 80, -1, .35, "lamp"), ln([(1190, 754), (1350, 776)], -1, "#efe6d2", 4, draw=False, curve=True, op=.7)]
    return els


def s1():
    """HERO: the legend, fully drawn at once: dusk over burned ground, the smoking Byrsa, the round harbour in the last light, the plough
    and its oxen cutting a furrow, a hand scattering white grains into it, the tophet's small stones in the foreground. More grains
    keep falling while the line is said, and a white streak spreads along the furrow on 'sowed the earth with salt'."""
    ts = T("s1", "sowed the earth with salt")
    r = random.Random(9)
    fall = []
    for k in range(60):
        t = (k % 12) / 12
        x = 1290 - 26 * t + r.uniform(-12, 12) * (.25 + t)
        fall.append(circ(x, 372 + t * 392, round(r.uniform(1.8, 3.0), 1), SALT, at=round(.4 + k * .16, 2), fx="pop"))
    els = hero_els() + fall + [ln([(1190, 756), (1040, 742), (890, 730)], ts, "#f5f1e6", 3.5, dur=1.6, curve=True, op=.75),
                                gl(1040, 742, 120, ts + .4, .3, "lamp")]
    return {"base": "sky", "tod": "dusk", "ground": HERO_GROUND, "sun": [1600, 515, 22], "groundc": "#1b130e",
            "ridges": [{"y": 520, "a": 34, "c": "#2c222a", "seed": 4}, {"y": 548, "a": 18, "c": "#221a1e", "seed": 8}],
            "cam": CAM, "els": els}


def s2():
    """Under the same city: the ground in section below a field of small standing stones: rows of small clay urns in three layers,
    lamps at the stones' feet. No remains drawn. On 'sacrificed', the writers' claim in a lilac dotted chip."""
    tc = T("s2", "sacrificed")
    els = [rect(0, 300, W_, 700, EARTH_D, at=-1), rect(0, 300, W_, 150, "#4a3a2a", at=-1, op=.9), rect(0, 450, W_, 160, "#3f3124", at=-1, op=.9),
           rect(0, 610, W_, 400, "#33271c", at=-1, op=.9), ln([(0, 300), (W_, 300)], -1, "#8a6a48", 3, draw=False),
           rect(0, 230, W_, 70, "#211913", at=-1)]
    r = random.Random(3)
    xs = [150 + 118 * k for k in range(13)]
    for k, x in enumerate(xs):
        h = r.uniform(70, 112)
        els += stele(x + r.uniform(-14, 14), 300, h * .42, h, round(.2 + .05 * k, 2), LIME, LIME_L, sign=(k % 2 == 0), crescent=(k % 3 == 0), lines=0, fx="rise")
    for x in xs[1::3]:
        els += lamp(x + 34, 300, 22, .9 + .1 * (x % 5))
    for row, (y0, n, s, at0) in enumerate(((440, 13, 60, 1.0), (590, 14, 56, 1.8), (740, 15, 52, 2.6))):
        for k in range(n):
            x = 120 + (1540 / (n - 1)) * k + r.uniform(-20, 20)
            els += urn(x, y0 + r.uniform(-14, 10), s * r.uniform(.85, 1.1), round(at0 + .04 * k, 2), mix(CLAY, "#3a2a1e", row * .22), rim=mix(CLAY_L, "#5a4a3a", row * .3))
    els += [gl(889, 540, 700, .8, .15, "lamp"), lab(1520, 215, "thousands of urns", 2.6, GOLD, 32)]
    els += chip(889, 175, "sacrificed?", LILAC, tc, 30, style="claimed")
    return {"base": "dark", "cam": CAM, "els": els}


def s3_add():
    """The two questions over the hero: the grains turn lilac (claimed) under a question mark; a second one by the small stones."""
    t2 = T("s3", "And what happened")
    r = random.Random(7)
    els = []
    for k in range(40):
        t = r.random()
        x = 1290 - 26 * t + r.uniform(-14, 14) * (.25 + t)
        els.append(circ(x, 372 + t * 392, 3.2, "none", LILAC, 1.6, round(.3 + .015 * k, 2), style="claimed"))
    els += qmark(1170, 330, .6, 100) + [lab(1170, 380, "salt?", 1.0, LILAC, 32)]
    els += qmark(440, 716, t2, 70) + [lab(440, 770, "the children?", t2 + .4, LILAC, 30)]
    return els


# ================================================================== 1 · the rise and fall of Carthage
VMED = View(0.5, 21.5, 34.2, 43.2, (90, 120, 1600, 680))
VWIDE = View(-6, 37, 29, 46, (90, 120, 1600, 680))
CARTHAGE, ROME_, ZAMA, TYRE = (10.323, 36.853), (12.496, 41.903), (9.40, 36.10), (35.195, 33.271)


def phoen(kind, x, y, s, at, c=GOLD, w=3.2):
    """One Phoenician (Punic) letter in schematic strokes, s = its height: qoph, resh, taw, heth, dalet, shin."""
    P = lambda u, v: (x + u * s, y + v * s)
    L = lambda pts: ln([P(u, v) for u, v in pts], at, c, w, draw=False)
    if kind == "q":
        return [L([(0, -.5), (0, .5)]), circ(*P(0, -.24), .2 * s, "none", c, w, at)]
    if kind == "r":
        return [L([(.14, -.5), (.14, .5)]), L([(.14, -.5), (-.2, -.3), (.14, -.1)])]
    if kind == "t":
        return [L([(-.26, -.42), (.26, .34)]), L([(.26, -.42), (-.26, .34)])]
    if kind == "h":
        return [L([(-.2, -.5), (-.2, .5)]), L([(.2, -.5), (.2, .5)])] + [L([(-.2, v), (.2, v)]) for v in (-.24, 0, .24)]
    if kind == "d":
        return [L([(.14, -.5), (-.22, -.2), (.14, -.08), (.14, -.5)]), L([(.14, -.08), (.1, .5)])]
    return [L([(-.32, -.3), (-.16, .32), (0, -.2), (.16, .32), (.32, -.3)])]          # shin


def merchant(x, y, w, at, c="#6a4a30", fx="pop", sail=True):
    """A round-hulled trading ship on the waterline y, bow to the left: a horse-head prow, a square sail."""
    h = w * .22
    hull = [(x - w * .5, y - h * .55), (x - w * .4, y + h * .3), (x + w * .38, y + h * .3), (x + w * .52, y - h * .6), (x + w * .4, y - h * .4), (x - w * .36, y - h * .4)]
    els = [poly(hull, c, "#e7c99a", 1.2, at, curve=True), circ(x - w * .52, y - h * .7, h * .22, c, "#e7c99a", 1, at)]
    if sail:
        els += [ln([(x, y - h * .4), (x, y - w * .62)], at, "#3a2616", max(1.5, w * .03), draw=False),
                poly([(x - w * .26, y - w * .58), (x + w * .26, y - w * .58), (x + w * .24, y - w * .2), (x - w * .24, y - w * .2)], "#efe2c8", "#8a7a66", 1, at)]
    return [grp(els, at, fx)] if fx else els


def s5():
    """Map of the whole Mediterranean: Tyre on the Levant coast (today's Lebanon); a trading ship leaves it and a dotted route draws
    west past Cyprus, Crete and Sicily to Carthage; at Carthage the name pops: 'New City', with the letters of Qart-hadasht above it
    (QRT HDST, right to left, schematic strokes)."""
    v = VWIDE
    tt, tl, tn = T("s5", "sailed from Tyre"), T("s5", "today's Lebanon"), T("s5", "New City")
    cx, cy = v.p(*CARTHAGE)
    tx, ty = v.p(*TYRE)
    els = [{"k": "map", "land": v.land(), "in": -1}, gl(cx, cy, 110, .2, .45, "lamp"), pin(cx, cy, "Carthage", .3, GOLD, "end", -22, 34)]
    els += [{"k": "scale", "x": 150, "y": 760, "w": round(v.km(500), 1), "t": "500 km", "in": .5}]
    els += [pin(tx, ty, "Tyre", tt, AMBER, "end", -20, -18), lab(tx + 24, ty - 40, "Lebanon", tl, DIM, 26, "start")]
    els += merchant(tx - 92, ty + 6, 58, tt + .2)
    route = [v.p(*q) for q in ((34.0, 33.4), (32.0, 34.15), (28.0, 34.4), (24.6, 34.55), (21.0, 35.5), (17.2, 36.2), (14.6, 36.45), (12.4, 37.05),
                               (10.9, 37.05))]
    els += [ln(route, tt + .4, AMBER, 3, "claimed", dur=3.2, curve=True)]
    for k, (lon, lat, name) in enumerate(((33.2, 35.1, "Cyprus"), (24.9, 35.25, "Crete"), (14.2, 38.35, "Sicily"))):
        x, y = v.p(lon, lat)
        els.append(lab(x, y - 26, name, tt + .9 + .9 * k, "#c9ad85", 24, st="ital"))
    els += merchant(*v.p(11.45, 37.2), 52, tt + 3.4)
    # the name: New City, and its letters (right to left), on the land south of the city
    nx, ny = cx, cy + 215
    for k, kind in enumerate("qrthdst"):
        els += phoen(kind, nx + 120 - 40 * k, ny - 78, 34, tn + .1 + .06 * k, GOLD)
    els += chip(nx, ny, "New City", GOLD, tn + .2, 30) + [lab(nx, ny + 62, "Qart-hadasht", tn + .8, DIM, 26, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def ox_hide(cx, cy, s, at, c="#a8794e", rim=LILAC, style="claimed"):
    """A flattened ox hide seen from above: a rough oblong with four leg flaps, a neck and a tail; s = its length."""
    P = lambda u, v: (cx + u * s, cy + v * s)
    pts = [P(-.5, -.12), P(-.62, -.3), P(-.42, -.24), P(-.2, -.3), P(.2, -.3), P(.4, -.24), P(.6, -.34), P(.55, -.14), P(.62, -.02), P(.55, .12),
           P(.6, .34), P(.4, .26), P(.2, .32), P(-.2, .32), P(-.42, .26), P(-.62, .32), P(-.5, .12), P(-.66, 0)]
    e = poly(pts, c, rim, 2.5, at, fx="pop", curve=True)
    e["style"] = style
    return [e, ln([P(-.4, -.05), P(-.1, .04), P(.25, -.03), P(.45, .05)], at, "rgba(60,36,20,.45)", 3, curve=True, draw=False)]


def s6():
    """The legend of the ox hide, at dawn: a low hill by the sea seen at a slant; Queen Dido, a robed figure; one ox hide laid flat in
    front of it; a knife line spirals through the hide and one long thin strip draws itself round the whole hill (lilac, dotted: the
    legend); 'the Byrsa' on the hill."""
    td, th, tc, tr, tb = (T("s6", "Queen Dido"), T("s6", "one ox hide"), T("s6", "She cut the hide"), T("s6", "circled a whole hill"), T("s6", "the Byrsa"))
    els = [{"k": "water", "y": 470, "h": 110, "op": .85, "in": -1}]
    hill = [(560, 640), (640, 560), (760, 470), (880, 420), (1000, 400), (1120, 410), (1240, 450), (1340, 520), (1420, 600), (1460, 640)]
    els += [poly([(0, 560), (1778, 560), (1778, 1000), (0, 1000)], "#3a2c22", at=-1),
            poly(hill, "#4a3828", "rgba(255,214,170,.55)", 2, -1, curve=True),
            poly([(1000, 400), (1120, 410), (1240, 450), (1340, 520), (1420, 600), (1460, 640), (1180, 640)], "rgba(0,0,0,.18)", at=-1, curve=True),
            ln([(640, 560), (760, 470), (880, 420), (1000, 400)], -1, "rgba(255,206,160,.5)", 3, curve=True, draw=False)]
    r = random.Random(6)
    for k in range(26):
        x, y = r.uniform(620, 1400), r.uniform(470, 630)
        if y > 400 + abs(x - 1000) * .42:
            els.append(poly(E(x, y, r.uniform(6, 14), r.uniform(3, 5), 10), "rgba(120,140,80,.35)", at=-1))
    els += fig(250, 790, 170, td, "#1d1612", None, 1, robe=True) + [lab(250, 600, "Queen Dido", td + .3, LILAC, 28)]
    hx, hy = 470, 730
    els += ox_hide(hx, hy, 230, th) + [lab(hx, 650, "one ox hide", th + .3, LILAC, 28)]
    sp = [(hx + (4 + 13 * t) * math.cos(t * 1.15), hy + (2 + 6 * t) * math.sin(t * 1.15)) for t in [i * .25 for i in range(40)]]
    els += [ln(sp, tc, "#f5e6c8", 2.4, dur=1.6, curve=True, op=.9)]
    ring = E(1010, 612, 470, 70, 60, 120, 480)
    els += [ln([(hx + 120, hy - 8), (560, 690), ring[0]], tr - .2, LILAC, 3, "claimed", dur=.7, curve=True),
            ln(ring, tr + .3, LILAC, 3.5, "claimed", dur=1.8, curve=True), gl(1010, 612, 300, tr + 1.6, .25, "lamp")]
    els += [lab(1010, 360, "the Byrsa", tb, GOLD, 32)]
    return {"base": "sky", "tod": "dawn", "ground": 560, "sun": [1600, 440, 26], "cam": CAM, "els": els}


XF = lambda yr: round(200 + (900 - yr) / 200 * 1380, 1)        # 900 to 700 BCE (years BCE, positive)


def s7():
    """The founding date: a timeline from 900 to 700 BCE; 'a legend' (the hide, lilac) at the left; the Greek writers' date as a scroll
    pinned at 814 BCE; below, the earliest layers of Carthage in a small section with a bone sample glowing in the lowest; the radiocarbon
    range, about 835 to 800 BCE, fills on the line and meets the scroll's pin in a soft green glow."""
    tg, tr = T("s7", "Greek writers"), T("s7", "radiocarbon dates")
    ay = 420
    els = [axis(XF(900), XF(700), ay, [(XF(900), "900 BCE"), (XF(850), "850"), (XF(800), "800"), (XF(750), "750"), (XF(700), "700 BCE")], .2)]
    els += ox_hide(260, 230, 110, .3) + [lab(260, 300, "a legend", .5, LILAC, 26)]
    x8 = XF(814)
    els += scroll(x8, 270, 96, tg) + [ln([(x8, 312), (x8, ay - 4)], tg + .2, GOLD, 2.5, dur=.4), lab(x8, 190, "Greek writers: 814 BCE", tg + .3, GOLD, 30)]
    # the oldest layers, in a small section
    sx0, sx1, sy0 = 560, 1010, 600
    for k, (c, h) in enumerate((("#6f5a44", 40), ("#5d4a37", 44), ("#4d3d2e", 46), ("#3e3125", 50))):
        y0 = sy0 + sum(hh for _, hh in (("", 40), ("", 44), ("", 46), ("", 50))[:k])
        els.append(rect(sx0, y0, sx1 - sx0, h, c, "rgba(255,226,190,.18)", 1, 0, tr - .6 + .1 * k))
    bx, by = 790, sy0 + 40 + 44 + 46 + 25
    els += [poly([(bx - 26, by + 5), (bx - 14, by - 6), (bx + 16, by - 4), (bx + 26, by + 6), (bx + 12, by + 10), (bx - 12, by + 9)], "#efe2c8", "#ffffff", 1, tr, fx="pop"),
            gl(bx, by, 70, tr + .1, .7, "lamp"), lab(sx1 + 24, by + 9, "oldest layer", tr - .2, DIM, 24, "start")]
    els += [ln([(bx, by - 14), (bx, 470)], tr + .5, "#8fd9b0", 2, "inferred", dur=.5)]
    els += [rect(XF(835), ay + 64, XF(800) - XF(835), 22, "#8fd9b0", at=tr + .9, fx="fill", r=11),
            lab(XF(800) + 26, ay + 84, "radiocarbon: about 835 to 800 BCE", tr + 1.2, "#8fd9b0", 28, "start")]
    els += [gl(x8, ay + 30, 120, tr + 2.0, .55, "lamp"), ln([(x8, ay + 4), (x8, ay + 60)], tr + 2.0, GOLD, 2.5, "inferred", dur=.4)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s8():
    """Map of the central Mediterranean: Carthage on the African coast beside Tunis, Rome in Italy, Sicily between; trading ships
    sail out on dotted routes as it grows rich on the sea; Rome pops and the arc of rivalry draws, 264 to 146 BCE."""
    v = VMED
    tp, tr = T("s8", "rich on the sea"), T("s8", "Rome's great rival")
    tc = tr - .2
    cx, cy = v.p(*CARTHAGE)
    rx, ry = v.p(*ROME_)
    els = [{"k": "map", "land": v.land(), "in": -1}, gl(cx, cy, 120, .2, .45, "lamp")]
    els += [pin(cx, cy, "Carthage", .3, GOLD, "start", 22, 34), lab(cx + 22, cy + 70, "beside today's Tunis", .7, DIM, 24, "start")]
    sx, sy = v.p(14.2, 37.45)
    els += [lab(sx, sy, "Sicily", .5, "#c9ad85", 26, st="ital")]
    routes = [[(cx, cy), v.p(9.5, 38.6), v.p(8.6, 40.4)], [(cx, cy), v.p(12.6, 37.0), v.p(15.6, 36.4)], [(cx, cy), v.p(6.0, 37.6), v.p(2.0, 38.3)]]
    for k, rt in enumerate(routes):
        els.append(ln(rt, tp - .2 + .2 * k, AMBER, 2.4, "inferred", dur=1.0, curve=True))
        x, y = rt[-1]
        els += merchant(x, y + 8, 50, tp + .7 + .2 * k)
    els += [pin(rx, ry, "Rome", tr, ROMAN, "start", 22, 8), gl(rx, ry, 110, tr, .4, "red")]
    mx, my = (cx + rx) / 2 + 150, (cy + ry) / 2
    els += [ln([(cx + 8, cy - 10), (mx, my), (rx + 10, ry + 8)], tc, GOLD, 3, dur=1.0, curve=True),
            ln([(cx + 14, cy - 4), (mx + 12, my + 4), (rx + 16, ry + 14)], tc + .2, ROMAN, 3, dur=1.0, curve=True)]
    els += chip(mx + 30, my, "264 to 146 BCE", GOLD, tc + .5, 28, "start")
    els += [{"k": "scale", "x": 140, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


def s9():
    """After Zama, 202 BCE: ten oared warships on a dark sea, popping in two rows of five; the count, and the date."""
    tz, tk, tw = T("s9", "Zama"), T("s9", "allowed to keep"), T("s9", "ten warships")
    els = [{"k": "water", "y": 470, "h": 560, "op": .85, "in": -1}, gl(889, 470, 700, -1, .18, "lamp")]
    els += [lab(889, 190, "after the defeat at Zama", .3, AMBER, 32)] + chip(889, 250, "202 BCE", AMBER, tz, 30)
    for k in range(10):
        x = 330 + 280 * (k % 5)
        y = 470 + 170 * (k // 5)
        els += galley(x, y, 230, round(tk + .14 * k, 2), "#5a3c26")
    els += [lab(889, 790, "ten warships allowed", tw + .2, BONE, 36, st="serif")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


HX, HY, HR, HI = 889, 450, 300, 96          # the round war harbour (plan): centre, outer radius (325 m across), island radius


def harbour_plan():
    """The round war harbour from above, true to the plan: about 325 m across, an island in the middle, a channel to the rectangular
    trading harbour (dim)."""
    els = [poly(E(HX, HY, HR + 34, HR + 34, 72), "#6f5c44", at=-1), poly([(HX - 46, HY + HR + 10), (HX + 46, HY + HR + 10), (HX + 40, 1000), (HX - 40, 1000)], SEAC, at=-1, op=.85),
           poly([(HX - 520, HY + HR + 60), (HX - 70, HY + HR + 60), (HX - 70, 1000), (HX - 520, 1000)], SEAC, at=-1, op=.35)]
    return els


def s10():
    """The round war harbour from above: water ring, island, the 325 m dimension; ship sheds draw themselves as radial slots round
    the rim and round the island, 170 in all; label 'about 170 ship sheds'."""
    td, tsh = T("s10", "about three hundred"), T("s10", "with sheds")
    els = harbour_plan()
    els += [poly(E(HX, HY, HR, HR, 72), SEAC, SEAL, 2, .3, fx="pop"), poly(E(HX, HY, HI, HI, 48), "#8f7a5c", "#e0cfa8", 2, .8, fx="pop"),
            gl(HX, HY, 340, .4, .18, "lamp"), lab(HX, 128, "a round war harbour", .5, GOLD, 32)]
    els += [arr([(HX - HR, HY), (HX + HR, HY)], td, BONE, 2.5, dur=.8, curve=False), arr([(HX + HR, HY), (HX - HR, HY)], td, BONE, 2.5, dur=.8, curve=False),
            rect(HX - 120, HY - 2 - 40, 240, 44, "rgba(18,13,10,.75)", at=td + .3), lab(HX, HY - 10, "325 m", td + .4, BONE, 32)]
    sheds = []
    n_out, n_in = 136, 34
    for k in range(n_out):
        a = math.pi / 2 + 2 * math.pi * k / n_out
        if abs(math.cos(a)) < .04 and math.sin(a) > 0:
            continue
        sheds.append(ln([(HX + (HR - 30) * math.cos(a), HY + (HR - 30) * math.sin(a)), (HX + HR * math.cos(a), HY + HR * math.sin(a))], round(tsh + .02 * k, 2), "#e6d4a8", 3, draw=False))
    for k in range(n_in):
        a = 2 * math.pi * k / n_in
        sheds.append(ln([(HX + HI * math.cos(a), HY + HI * math.sin(a)), (HX + (HI + 22) * math.cos(a), HY + (HI + 22) * math.sin(a))], round(tsh + 2.8 + .03 * k, 2), "#e6d4a8", 3, draw=False))
    els += sheds + [lab(1380, 300, "about 170", tsh + 3.6, "#e6d4a8", 34, "start"), lab(1380, 345, "ship sheds", tsh + 3.7, "#e6d4a8", 30, "start"),
                    ln([(1370, 320), (HX + HR * .78, HY - HR * .5)], tsh + 3.8, "#e6d4a8", 2, dur=.5)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s11_add():
    """For a fleet of ten: ten sheds light gold with a small ship in each; the other 160 stay empty."""
    els = [poly(E(HX, HY, HR + 2, HR + 2, 72), "rgba(10,8,6,.35)", at=.1)]
    for j, k in enumerate(range(4, 136, 13)):
        if j >= 10:
            break
        a = math.pi / 2 + 2 * math.pi * k / 136
        x0, y0 = HX + (HR - 30) * math.cos(a), HY + (HR - 30) * math.sin(a)
        x1, y1 = HX + HR * math.cos(a), HY + HR * math.sin(a)
        els += [ln([(x0, y0), (x1, y1)], round(.2 + .07 * j, 2), AU, 8, draw=False), gl((x0 + x1) / 2, (y0 + y1) / 2, 30, round(.2 + .07 * j, 2), .6)]
    els += [lab(1330, 640, "a fleet of ten", .6, AU, 36, "start", st="serif")]
    return els


def tall_house(x, y, w, h, at, c="#2a201a", lit="#ff9a4a", floors=6, seed=1, fx="pop", rim="rgba(255,190,130,.4)"):
    """A tall narrow house in elevation: `floors` storeys of small windows, some lit by fire."""
    r = random.Random(seed)
    els = [rect(x, y - h, w, h, c, rim, 1, 2, at)]
    fh = h / floors
    for f in range(floors):
        for k in range(2):
            wx = x + w * (.22 + .4 * k)
            wy = y - h + fh * f + fh * .3
            els.append(rect(wx, wy, w * .18, fh * .4, lit if r.random() < .35 else "#120d0a", at=at, op=.85))
    return [grp(els, at, fx)] if fx else els


def s12():
    """The last assault, in plan: the Byrsa hill with its citadel at the left, the forum by the harbours at the lower right, three
    streets climbing between them lined with tall houses; Roman arrows advance up the three streets as fires spread; at the right,
    one six-storey house in elevation with a person for scale."""
    tb, tf, t6, th = T("s12", "Rome came back"), T("s12", "six days and nights"), T("s12", "six-storey"), T("s12", "towards the citadel")
    els = [poly(E(390, 390, 300, 230, 48), "#3a2d22", "rgba(255,226,190,.2)", 1.5, -1, curve=True),
           poly(E(390, 380, 200, 150, 40), "#463628", "rgba(255,226,190,.2)", 1, -1, curve=True),
           poly(E(380, 370, 110, 82, 32), "#55422f", GOLD, 2.5, -1, curve=True)]
    for k in range(16):
        a = 2 * math.pi * k / 16
        els.append(rect(380 + 110 * math.cos(a) - 6, 370 + 82 * math.sin(a) - 6, 12, 12, "#6f5a44", "#e0cfa8", 1, 1, -1))
    els += [rect(350, 345, 60, 44, "#7a6248", "#e0cfa8", 1.5, 2, -1), lab(380, 270, "the Byrsa", .4, GOLD, 30)]
    els += [rect(1000, 600, 160, 110, "#5a4836", "#e0cfa8", 1.5, 3, -1), lab(1080, 745, "the forum", .6, DIM, 26)]
    streets = [[(1010, 610), (840, 540), (660, 470), (480, 410)], [(1040, 600), (880, 500), (700, 420), (490, 352)], [(1080, 600), (940, 470), (760, 375), (470, 300)]]
    for si, st_ in enumerate(streets):
        els.append(ln(st_, -1, "#7d6a52", 12, draw=False, curve=True))
        for k in range(len(st_) - 1):
            (x0, y0), (x1, y1) = st_[k], st_[k + 1]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            nx, ny = -dy / L, dx / L
            ang = math.degrees(math.atan2(dy, dx))
            for j in range(5):
                t = (j + .5) / 5
                for side in (-1, 1):
                    hx, hy = x0 + dx * t + nx * 17 * side, y0 + dy * t + ny * 17 * side
                    els.append({"k": "group", "tr": "rotate(%.1f %.1f %.1f)" % (ang, hx, hy), "in": -1,
                                "els": [rect(hx - 15, hy - 6, 30, 12, "#2a201a", "rgba(255,200,140,.4)", 1, 1, -1)]})
    els += [lab(760, 610, "three streets", 1.0, BONE, 28)] + chip(230, 150, "149 BCE", ROMAN, tb, 28)
    for si, st_ in enumerate(streets):
        els.append(arr(st_, round(tf + .3 * si, 2), ROMAN, 6, dur=3.6, curve=True))
        for j, (x, y) in enumerate(st_[:-1]):
            els.append(gl(x, y, 70, round(tf + .5 + 1.0 * j + .2 * si, 2), .7, "fire", pulse=True))
    els += chip(1080, 540, "6 days and nights", ROMAN, tf + .4, 28)
    els += [rect(1300, 140, 380, 560, "rgba(18,13,10,.6)", "rgba(255,236,206,.2)", 1.5, 14, t6 - .2)]
    els += tall_house(1420, 640, 140, 460, t6, "#33271f", seed=3)
    els += fig(1600, 640, 78, t6 + .4, "#e8d6b8", fx="rise")
    els += [ln([(1650, 640), (1650, 180)], t6 + .6, BONE, 2, dur=.6), lab(1490, 680, "six storeys", t6 + .5, BONE, 28)]
    els += [gl(380, 370, 170, th, .6, "fire", pulse=True)]
    return {"base": "dark", "cam": CAM, "els": els}


def s13():
    """The survivors: a narrow gate in the citadel wall, a long line of small figures walking out and away (50 figures, 1 = 1,000
    people), drawn with care; behind them the city burns; a row of 17 day-marks lights one by one (dashed: the later writers' figure)."""
    tf, t17 = T("s13", "The city burned"), T("s13", "seventeen")
    els = []
    r = random.Random(8)
    for k in range(30):
        x = 80 + k * 56 + r.uniform(-10, 10)
        h = r.uniform(90, 220)
        els.append(poly([(x, 470), (x, 470 - h), (x + 18, 470 - h - r.uniform(0, 20)), (x + 30, 470 - h + 14), (x + 50, 470 - h + r.uniform(-10, 10)), (x + 50, 470)],
                        "#1d1512", "rgba(255,160,100,.3)", 1, -1))
    els += [rect(0, 470, W_, 530, "#211812", at=-1), ln([(0, 470), (W_, 470)], -1, "rgba(255,200,140,.4)", 1.5, draw=False)]
    els += [rect(140, 330, 260, 140, "#2e241e", "rgba(255,200,140,.5)", 1.5, 2, -1), poly([(230, 470), (230, 400), (270, 370), (310, 400), (310, 470)], "#0c0907", "rgba(255,200,140,.6)", 1.5, -1)]
    path = [(270, 480), (520, 560), (900, 610), (1300, 650), (1680, 690)]
    els.append(ln(path, -1, "#3a2c20", 26, draw=False, curve=True))
    for k in range(50):
        t = k / 49
        i = min(3, int(t * 4)); u = t * 4 - i
        x = path[i][0] + (path[i + 1][0] - path[i][0]) * u
        y = path[i][1] + (path[i + 1][1] - path[i][1]) * u
        els += fig(x + r.uniform(-8, 8), y + r.uniform(-6, 6), 34 + 16 * t, round(.3 + .08 * k, 2), "#d9c7a6", fx="rise")
    els += [lab(1200, 730, "about 50,000", 2.6, BONE, 34, st="serif"), lab(1200, 768, "1 figure = 1,000 people", 3.0, DIM, 24)]
    for k in range(9):
        els.append(gl(100 + k * 200, 380, 140, round(tf + .2 * k, 2), .7, "fire", pulse=True))
    for k in range(17):
        x = 640 + 56 * k
        els += [rect(x, 160, 40, 40, "none", AMBER, 2, 6, round(t17 + .06 * k, 2), style="inferred"), rect(x + 6, 166, 28, 28, "#ff8a4a", at=round(t17 + .06 * k + .05, 2), op=.8)]
    els += [lab(620, 192, "17 days?", t17 + .3, AMBER, 30, "end")]
    return {"base": "sky", "tod": "night", "ground": 470, "sun": False, "cam": CAM, "els": els}


def s14():
    """Scipio and Polybius on a rise in the foreground, seen from behind, rim-lit by the fires; the burning city beyond; in the smoke
    above it a faint dotted ghost of another walled city appears: Troy."""
    tt, tp = T("s14", "remembering Troy"), T("s14", "His friend")
    els = [poly([(0, 700), (240, 660), (520, 650), (720, 690), (860, 760), (900, 1000), (0, 1000)], "#0d0907", at=-1, curve=True)]
    r = random.Random(12)
    for k in range(30):
        x = 560 + k * 40 + r.uniform(-8, 8)
        h = r.uniform(50, 170)
        els.append(poly([(x, 600), (x, 600 - h), (x + 14, 600 - h - r.uniform(0, 14)), (x + 26, 600 - h + 10), (x + 36, 600 - h), (x + 36, 600)], "#1b1310", "rgba(255,150,90,.45)", 1, -1))
    for k in range(11):
        els.append(gl(600 + k * 100, 560, 120, -1, .75, "fire", pulse=True))
    els += smoke([(820, 540), (870, 430), (950, 330), (1040, 250)], 30, 100, 2, .55) + smoke([(1380, 560), (1420, 450), (1500, 350), (1580, 270)], 26, 90, 6, .5)
    for x, h, name, at, c in ((360, 230, "Scipio", .6, GOLD), (500, 214, "Polybius", tp, DIM)):
        els += fig(x, 668, h, -1, "#0a0706", None, 1, fx=None)
        els += [ln([(x + .13 * h, 668 - .78 * h), (x + .11 * h, 668 - .44 * h), (x + .085 * h, 668)], -1, "rgba(255,170,110,.7)", 2.5, draw=False),
                circ(x + .01 * h, 668 - .9 * h, .085 * h, "none", "rgba(255,170,110,.6)", 2, -1)]
        els += [lab(x, 720, name, at, c, 30)]
    troy = [(1000, 330), (1000, 240), (1040, 240), (1040, 210), (1080, 210), (1080, 240), (1150, 240), (1150, 190), (1190, 165), (1230, 190), (1230, 240),
            (1300, 240), (1300, 212), (1340, 212), (1340, 240), (1380, 240), (1380, 330)]
    els += [poly(troy, "rgba(201,193,238,.08)", LILAC, 3, tt, style="claimed", fx="draw", dur=1.4),
            poly([(1165, 330), (1165, 290), (1190, 272), (1215, 290), (1215, 330)], "none", LILAC, 2.5, tt + .4, style="claimed", fx="draw", dur=.6),
            gl(1190, 260, 160, tt, .25, "lamp"), lab(1190, 140, "Troy", tt + .6, LILAC, 32)]
    return {"base": "sky", "tod": "night", "ground": 600, "sun": False, "groundc": "#160f0b", "cam": CAM, "els": els}


def s15():
    """Ten senators with a scroll; Rome's two orders pop beside them; then three icons ticked as named: fire, ruin, a ban; 'what the
    ancient writers agree on'."""
    to1, to2, tfire, truin, tban, tag = (T("s15", "destroy whatever"), T("s15", "let no one"), T("s15", "Fire, ruin"), T("s15", "ruin and"), T("s15", "a ban"),
                                         T("s15", "That much"))
    els = [lab(400, 170, "ten senators", .4, GOLD, 30)]
    for k in range(10):
        x = 130 + 58 * k
        els += fig(x, 470, 150 + (k % 3) * 8, round(.3 + .08 * k, 2), "#e9dfcc", None, 1, robe=True)
    els += scroll(780, 330, 120, 1.2, LIME_L)
    els += chip(1250, 220, "destroy what is left", ROMAN, to1, 30) + chip(1250, 300, "no one to live there", ROMAN, to2, 30)
    els += [rect(140, 560, 1500, 210, "rgba(18,13,10,.6)", "rgba(255,236,206,.25)", 1.5, 16, tfire - .3)]
    els += flame(450, 720, 110, tfire) + [tick(520, 660, tfire + .3)]
    els += broken_wall(890, 720, 120, truin) + [tick(960, 660, truin + .3)]
    els += barred_gate(1330, 720, 120, tban) + [tick(1400, 660, tban + .3)]
    els += [lab(450, 600, "fire", tfire + .1, AMBER, 28), lab(890, 600, "ruin", truin + .1, AMBER, 28), lab(1330, 600, "a ban", tban + .1, AMBER, 28),
            lab(889, 800, "what the ancient writers agree on", tag, GOLD, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== 2 · where the salt came from
XA = lambda yr: round(170 + (yr + 160) / 620 * 1440, 1)       # 160 BCE to 460 CE (BCE negative)
ACC = [(-146, "Polybius", "an eyewitness"), (-30, "Diodorus", None), (160, "Appian", None), (417, "Orosius", None)]


def s16():
    """The ancient accounts on a timeline from 160 BCE to 460 CE: Polybius, Diodorus, Appian, Orosius pop at their dates as scrolls
    and books; a salt pinch in a lilac dotted ring hovers over them and finds nothing: 'no salt'."""
    els = [axis(XA(-160), XA(460), 640, [(XA(-150), "150 BCE"), (XA(0), "1 CE"), (XA(150), "150 CE"), (XA(300), "300"), (XA(450), "450")], .2)]
    els += [poly([(XA(-146) - 10, 600), (XA(-146) + 10, 600), (XA(-146), 626)], ROMAN, at=.3), lab(XA(-146), 590, "the fire", .4, ROMAN, 24)]
    for k, (yr, name, _) in enumerate(ACC):
        x = XA(yr)
        at = round(.6 + .35 * k, 2)
        els += (scroll(x, 470, 90, at) if yr < 0 else book(x, 470, 70, at))
        els += [ln([(x, 530), (x, 632)], at, DIM, 1.5, draw=False), lab(x, 390 if k % 2 == 0 else 370, name, at + .1, BONE, 28)]
    els += [circ(1560, 200, 62, "rgba(201,193,238,.05)", LILAC, 2.5, 2.2, style="claimed", fx="draw", dur=.8)] + salt_pinch(1560, 200, 26, 2.3, n=12)
    els += [ln([(1500, 262), (1620, 138)], 3.0, RED, 5, dur=.3), lab(1560, 305, "no salt", 3.2, RED, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s17_add():
    """Polybius' scroll glows with a small flame ('an eyewitness'); Appian's book raises three icons as named (fire, ruins, a ban);
    a law book about 230 CE: a plough draws one ritual furrow round a small city outline ('a rite, in law'); not one grain of salt."""
    tp, ta, tb, tl, tn = (T("s17", "Polybius saw"), T("s17", "the burning"), T("s17", "the ban"), T("s17", "One Roman lawyer"), T("s17", "But not one grain"))
    x0, x1, x2 = XA(-146), XA(160), XA(230)
    els = flame(x0, 330, 50, tp) + [lab(x0, 290 - 40, "an eyewitness", tp + .3, AMBER, 26)]
    els += flame(x1 - 70, 300, 44, ta) + broken_wall(x1, 300, 60, ta + .5) + barred_gate(x1 + 72, 300, 56, tb)
    els += book(x2, 470, 70, tl, "#3e5a4a") + [ln([(x2, 530), (x2, 632)], tl, DIM, 1.5, draw=False), lab(x2, 390, "a lawyer", tl + .1, BONE, 28)]
    cx, cy = 1250, 245
    els += [ln([(x2, 420), (cx - 40, cy + 70)], tl + .4, DIM, 1.5, dur=.4),
            poly([(cx - 50, cy + 32), (cx - 50, cy - 8), (cx - 25, cy - 24), (cx, cy - 8), (cx + 25, cy - 28), (cx + 50, cy - 8), (cx + 50, cy + 32)], "#4a3a2c", "#cbbca8", 1.5, tl + .6),
            circ(cx, cy + 4, 78, "none", GOLD, 3, tl + 1.2, style="inferred", fx="draw", dur=1.6)] + plough_icon(cx + 78, cy + 4, 40, tl + 2.6)
    els += [lab(cx, cy - 98, "a rite, in law", tl + 2.2, GOLD, 26)]
    els += [rect(560, 690, 660, 90, "rgba(18,13,10,.85)", RED, 2.5, 18, tn, fx="pop"), lab(889, 748, "not one grain of salt", tn + .1, RED, 34, st="serif")]
    return els


RIVER = [(1710, 600), (1560, 560), (1430, 596), (1310, 628), (1180, 616), (1070, 592), (960, 540), (850, 486), (740, 420), (650, 368)]


def s18():
    """The story as a river: it winds from its mouth at the right ('today') back to a spring at the left; an arrow travels upstream;
    'upstream, to the source'."""
    tu = T("s18", "upstream")
    els = [poly([(p[0], p[1] + 16) for p in RIVER] + [(p[0], p[1] - 16) for p in RIVER[::-1]], "#2f6f96", at=-1, curve=True),
           ln(RIVER, -1, SEAL, 2.5, curve=True, draw=False, op=.7), circ(650, 368, 22, "#4fa3d0", SEAL, 2, -1)]
    r = random.Random(4)
    for k in range(40):
        x, y = r.uniform(120, 1700), r.uniform(150, 790)
        els.append(circ(x, y, r.uniform(1, 2.2), "#8a7a66", at=-1, op=.5))
    els += [lab(1690, 660, "today", .3, BONE, 28), lab(720, 340, "the source?", .6, SEAL, 26, "start")]
    els += [arr(RIVER[1:], tu - .6, GOLD, 4, dur=2.4, curve=True), lab(1240, 300, "upstream, to the source", tu, GOLD, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s19_add():
    """Pins pop up the river as named: 1986, Ridley; 1930, an influential history; the 1800s, encyclopaedias; 1299, Palestrina (a hill
    town, a plough and white grains). Each carries a small white grain."""
    t1, t2, t3, t4 = T("s19", "the historian Ronald"), T("s19", "to an influential"), T("s19", "nineteenth-century"), T("s19", "Palestrina")
    els = []
    # (pin on the river, icon centre, label y, label, time, kind)
    for (px, py), (ix, iy), ly, t, at, kind in (((1560, 560), (1560, 470), 405, "1986, Ridley", t1, "journal"),
                                                 ((1310, 628), (1310, 706), 784, "1930, a history book", t2, "book"),
                                                 ((1070, 592), (1070, 500), 435, "1800s, encyclopaedias", t3, "book")):
        els += [ln([(px, py), (ix, iy + (40 if iy < py else -40))], at, DIM, 1.5, dur=.4), circ(px, py, 9, SALT, "#ffffff", 1.5, at, fx="pop")]
        els += book(ix, iy, 46 if kind == "journal" else 52, at + .1, "#4a5a6a" if kind == "journal" else "#6d4a2e", thick=(kind == "book"))
        els += [lab(ix, ly, t, at + .2, BONE, 26)]
    x, y = 860, 640
    els += [ln([(850, 486), (850, y - 50)], t4, DIM, 1.5, dur=.4), circ(850, 486, 9, SALT, "#ffffff", 1.5, t4, fx="pop"),
            poly([(x - 80, y + 30), (x - 50, y - 10), (x - 20, y - 26), (x + 20, y - 30), (x + 60, y - 6), (x + 90, y + 30)], "#4a3a2c", "#cbbca8", 1.5, t4),
            rect(x - 30, y - 50, 18, 26, "#5a4836", at=t4), rect(x + 6, y - 58, 16, 32, "#5a4836", at=t4)] + plough_icon(x - 20, y + 66, 40, t4 + .4) + salt_pinch(x + 50, y + 62, 18, t4 + .7, n=10)
    els += [lab(x, y + 130, "1299, Palestrina", t4 + .2, BONE, 26)]
    return els


def s20_add():
    """The spring at the far left: a medieval geographer's manuscript page glows (al-Bakri, 11th century; a 2026 study); beyond it the
    dry bed runs back to a small fire at 146 BCE; a bracket spans the gap: about 1,200 years."""
    tl, tg = T("s20", "salt, in a local tale"), T("s20", "Some twelve hundred")
    x, y = 400, 250
    els = [rect(x - 150, y - 90, 300, 180, "#e9dcc0", "#8a7a66", 2, 6, .4, fx="pop")]
    for k in range(5):
        els.append(ln([(x - 125 + (k % 2) * 30, y - 60 + k * 26), (x + 10 + (k % 3) * 20, y - 60 + k * 26)], .5, "#6a5a48", 2.4, draw=False))
    els += [circ(x + 88, y - 10, 46, "#cbb68e", "#6a5a48", 2, .6), ln([(x + 50, y - 10), (x + 126, y - 10)], .7, "#3f86b0", 2, draw=False),
            ln([(x + 88, y - 52), (x + 88, y + 32)], .7, "#6a5a48", 1.5, draw=False), gl(x, y, 230, .5, .3, "lamp"),
            ln([(x + 150, y + 40), (630, 356)], .6, DIM, 1.5, dur=.4)]
    els += [lab(x, y + 130, "al-Bakri, 11th century", tl, GOLD, 30)] + chip(x, y + 180, "2026 study", GOLD, tl + .5, 24)
    els += [ln([(632, 380), (520, 470), (360, 530), (200, 560)], .8, "#6a5a48", 6, "inferred", dur=1.2, curve=True)]
    els += flame(180, 590, 56, 1.6) + [lab(180, 640, "146 BCE", 1.8, ROMAN, 28)]
    els += bracket(200, 630, 690, tg, "about 1,200 years", AMBER, up=False, size=30, ty=740)
    return els


def s21():
    """An open book on a dark table: a hand above pinches white grains that fall onto its pages ('the story'); below, the dark ploughed
    soil stays clean and a small green shoot rises ('the soil')."""
    ts, tso = T("s21", "sprinkled on the story"), T("s21", "not on the soil")
    els = [rect(0, 640, W_, 360, "#2a1e15", at=-1)]
    for k in range(9):
        y = 662 + k * 15
        els.append(ln([(80, y), (1700, y + (k % 2) * 4)], -1, "#1a120c", 4, draw=False, op=.8))
    bx, by = 889, 470
    els += [poly([(bx - 380, by + 90), (bx - 360, by - 120), (bx - 10, by - 100), (bx - 10, by + 110)], "#efe4cc", "#8a7a66", 2, .2),
            poly([(bx + 380, by + 90), (bx + 360, by - 120), (bx + 10, by - 100), (bx + 10, by + 110)], "#efe4cc", "#8a7a66", 2, .2),
            ln([(bx, by - 104), (bx, by + 112)], .2, "#8a7a66", 2, draw=False)]
    for k in range(6):
        if k >= 3:
            els.append(ln([(bx - 330, by - 70 + k * 28), (bx - 60, by - 64 + k * 28)], .3, "#a8977c", 2.2, draw=False))
        els.append(ln([(bx + 60, by - 64 + k * 28), (bx + 330 - (k % 3) * 40, by - 70 + k * 28)], .3, "#a8977c", 2.2, draw=False))
    els += [lab(bx - 190, by - 52, "To be taken with", .5, "#5a4a38", 32, st="serif"), lab(bx - 190, by - 10, "a pinch of salt", .5, "#5a4a38", 32, st="serif"),
            rect(bx - 340, by - 90, 300, 4, "#5a4a38", at=.5)]
    els += hand_down(1080, 170, 110, .3, fx="rise")
    r = random.Random(3)
    for k in range(60):
        t = (k % 15) / 15
        els.append(circ(1066 - 20 * t + r.uniform(-14, 14) * (.3 + t), 200 + t * 260, round(r.uniform(1.8, 3.0), 1), SALT, at=round(.8 + .05 * k, 2), fx="pop"))
    els += [lab(bx + 230, by + 150, "the story", ts, GOLD, 30)]
    els += [ln([(600, 760), (602, 720), (596, 690)], tso, "#7fc46a", 4, dur=.6, curve=True), poly([(598, 712), (568, 694), (580, 716)], "#7fc46a", at=tso + .4, fx="pop"),
            poly([(600, 700), (628, 684), (618, 708)], "#8fd47a", at=tso + .5, fx="pop"), lab(600, 795, "the soil", tso + .3, "#9fd890", 28)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 3 · the city under the city
BG3 = "#16110d"                       # the night behind the Byrsa section (flat, so covers can hide what Rome cut away)
EARTH3 = "#4a3a2a"
BYRSA_S = [(0, 400), (90, 350), (166, 300), (260, 248), (360, 214), (460, 200), (560, 210), (640, 240), (712, 300)]
TERR = [(712, 872, 372), (888, 1048, 452), (1090, 1250, 532)]          # the three terraces of the Punic quarter: x0, x1, floor y
SLOPE = [(1250, 532), (1320, 562), (1420, 600), (1560, 640), (1700, 668), (1778, 680)]
WALLC, WALLR = "#c9b08a", "#f0dfbf"


def byrsa_section():
    """The south slope of the Byrsa in section (schematic, heights exaggerated): the hill, three terraces cut into the slope, a house on each
    (walls, a plaster floor, a partition), a street with a shop's open front, a bottle-shaped cistern under a floor."""
    surf = BYRSA_S + [(712, 372), (872, 372), (888, 372), (888, 452), (1048, 452), (1090, 452), (1090, 532)] + SLOPE
    els = [rect(0, 0, W_, 1000, BG3, at=-1),
           poly(surf + [(1778, 1000), (0, 1000)], EARTH3, at=-1), ln(surf, -1, "rgba(255,214,170,.45)", 2.5, draw=False)]
    for k, (y0, dy) in enumerate(((620, 50), (700, 60), (780, 70))):
        els.append(ln([(0, y0 - 40), (500, y0 - 20), (1000, y0 + 10), (1778, y0 + dy)], -1, "rgba(20,14,10,.55)", 3, curve=True, draw=False))
    for (x0, x1, fy) in TERR:
        els += [rect(x0, fy - 4, x1 - x0, 6, "#d8c9a8", at=-1),
                rect(x0, fy - 64, 14, 60, WALLC, WALLR, 1, 1, -1), rect(x0 + (x1 - x0) * .48, fy - 44, 10, 40, WALLC, WALLR, 1, 1, -1)]
        if x0 == 888:                                            # the shop: its front open on the street, two jars inside
            els += [rect(x1 - 14, fy - 60, 14, 18, WALLC, WALLR, 1, 1, -1)]
            for k in range(2):
                els += [poly([(x1 - 64 + 24 * k, fy - 4), (x1 - 72 + 24 * k, fy - 26), (x1 - 64 + 24 * k, fy - 40), (x1 - 56 + 24 * k, fy - 26)], CLAY, CLAY_L, 1, -1)]
        else:
            els += [rect(x1 - 14, fy - 60, 14, 56, WALLC, WALLR, 1, 1, -1)]
    # the cistern under the middle house
    els += [rect(950, 448, 22, 34, "#120c09", "#d8c9a8", 1.5, 2, -1), poly(E(961, 548, 50, 64, 36), "#120c09", "#d8c9a8", 1.5, -1)]
    return els


def s22():
    """The Byrsa in section (schematic): the hill, the Punic quarter on its south slope, houses on three terraces, a shop open on the
    street, a cistern under a floor; on '1970s', two excavators on the slope; the cistern fills blue on 'water cisterns'."""
    t70, tq, tg, tsh, tc = (T("s22", "In the nineteen seventies"), T("s22", "whole quarter"), T("s22", "on a grid"), T("s22", "with shops"),
                            T("s22", "water cisterns"))
    els = byrsa_section()
    els += [lab(230, 214, "the Byrsa", .4, GOLD, 32)]
    els += chip(1620, 584, "1970s", GOLD, t70, 28)
    for k, (x, y) in enumerate(((1440, 604), (1508, 624))):
        els += fig(x, y, 62, t70 + .3 + .2 * k, SKIN, "point", -1, lean=.12)
    els += [gl(980, 380, 210, tq, .3, "lamp"), lab(800, 282, "Punic houses", tq + .2, BONE, 30)]
    for k, (x0, x1, fy) in enumerate(TERR):
        els.append(rect(x0, fy - 66, x1 - x0, 66, "none", GOLD, 2, 3, tg + .25 * k, fx="draw"))
    els += [gl(1060, 430, 60, tsh, .5, "lamp")]
    els += [poly(E(961, 566, 44, 44, 30), SEAC, SEAL, 1.5, tc, fx="fill"), lab(961, 676, "a cistern", tc + .3, SEAL, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s23_add():
    """Over the floors: a dark band of burnt debris fills on each terrace, embers glowing in it; '146 BCE: burnt debris'."""
    els = []
    r = random.Random(14)
    for k, (x0, x1, fy) in enumerate(TERR):
        at = round(.4 + .25 * k, 2)
        els.append(rect(x0 + 14, fy - 30, x1 - x0 - 28, 26, "#120b08", at=at, fx="fill"))
        for j in range(9):
            els.append(circ(r.uniform(x0 + 22, x1 - 22), r.uniform(fy - 26, fy - 8), r.uniform(2, 3.6), EMBER, at=round(at + .3 + .05 * j, 2), op=round(r.uniform(.5, .95), 2)))
        els.append(gl((x0 + x1) / 2, fy - 16, 90, at + .3, .45, "fire", pulse=True))
    els += [ln([(1290, 470), (1200, 512)], 1.3, ROMAN, 2, dur=.4), lab(1300, 462, "146 BCE: burnt debris", 1.2, EMBER, 28, "start")]
    return els


def s24_add():
    """Rome buried them: the summit is cut down (the old crest stays as a dashed outline), a flat platform is laid at its new level with a
    retaining wall over the slope, the forum rises on top; then rubble fills the space over the burnt houses and piers drive into them.
    Stale labels (the cistern, the 1970s) are covered."""
    tcut, tpl, tfo, tru = T("s24", "cut down the top"), T("s24", "great flat platform"), T("s24", "for its forum"), T("s24", "the rubble sealed")
    dome = [(166, 300)] + [p for p in BYRSA_S if p[1] < 300] + [(712, 300)]
    els = [poly(dome, BG3, at=tcut, dur=1.0), ln(dome[1:-1], tcut + .2, DIM, 2.5, "inferred", dur=1.0, curve=True),
           rect(884, 650, 156, 36, EARTH3, at=tcut), rect(1544, 548, 180, 72, BG3, at=tcut)]
    els += [ln([(150, 301), (1262, 301)], tpl, LIME_L, 9, dur=1.2), rect(1250, 300, 24, 250, LIME, LIME_L, 1.2, 1, tpl + 1.0, fx="fill")]
    cols = [380 + 46 * k for k in range(7)]
    els += [rect(360, 286, 320, 10, LIME, LIME_L, 1, 1, tfo, fx="pop")]
    for k, x in enumerate(cols):
        els.append(rect(x - 7, 232, 14, 54, LIME_L, "#fff4dc", 1, 1, round(tfo + .1 + .06 * k, 2), fx="fill"))
    els += [rect(364, 220, 312, 12, LIME, LIME_L, 1, 1, tfo + .6, fx="pop"), poly([(364, 220), (520, 186), (676, 220)], LIME, LIME_L, 1.2, tfo + .7, fx="pop"),
            gl(520, 250, 200, tfo + .7, .3, "lamp"), lab(520, 160, "the Roman forum", tfo + .8, GOLD, 30)]
    fill_ = [(712, 306), (1250, 306), (1250, 532), (1090, 532), (1090, 452), (888, 452), (888, 372), (712, 372)]
    els += [poly(fill_, "#7a6450", at=tru, fx="fill", op=.8)]
    r = random.Random(24)
    for k in range(46):
        x, y = r.uniform(720, 1240), r.uniform(312, 520)
        if (x < 888 and y > 366) or (x < 1090 and y > 446):
            continue
        els.append(poly(blob(x, y, r.uniform(5, 10), r.uniform(4, 7), 7, .3, k), "#5a4836", at=round(tru + .6, 2), op=.8))
    for k, (x, fy) in enumerate(((800, 372), (1000, 452), (1180, 532))):
        els.append(ln([(x, 308), (x, fy - 2)], round(tru + 1.0 + .3 * k, 2), LIME, 14, dur=.5, draw=True))
    els += [lab(1150, 350, "rubble", tru + .5, "#e6d4b4", 30)] + chip(830, 340, "sealed", GOLD, tru + 1.8, 26)
    return els


def s25():
    """Beside, or on top? A plan from above: the Punic city's outline (warm brown) with the Byrsa and its two harbours by the sea; a lilac
    dotted Roman city drawn beside it ('Appian: beside'); then the Roman street grid draws in solid gold right over the Punic city."""
    tb, td = T("s25", "beside the old one"), T("s25", "The digging says")
    coast = [(1240, 0), (1210, 160), (1250, 300), (1190, 470), (1130, 620), (1180, 800), (1150, 1000)]
    els = [poly(coast + [(1778, 1000), (1778, 0)], "#2a5a78", at=-1), ln(coast, -1, "#c9ad85", 2, curve=True, draw=False)]
    city = [(560, 230), (760, 190), (960, 220), (1150, 300), (1170, 470), (1110, 620), (930, 690), (720, 680), (560, 600), (500, 420)]
    els += [poly(city, "rgba(184,90,60,.32)", PUNIC, 3, .2, curve=True), lab(830, 160, "the Punic city", .4, PUNIC, 28),
            circ(760, 420, 46, "#5a4632", GOLD, 2, .3), lab(760, 492, "the Byrsa", .5, DIM, 24),
            circ(1060, 600, 34, SEAC, "#9fd0ff", 2, .3), rect(1010, 650, 70, 40, SEAC, "#9fd0ff", 2, 2, .3)]
    els += [rect(130, 300, 300, 330, "rgba(201,193,238,.06)", LILAC, 3, 8, tb, fx="draw", style="claimed"), lab(280, 270, "Appian: beside", tb + .3, LILAC, 28)]
    grid = []
    for k in range(7):
        x = 560 + 95 * k
        grid.append(ln([(x, 220), (x, 690)], round(td + .1 * k, 2), GOLD, 3, dur=.7))
    for k in range(5):
        y = 260 + 100 * k
        grid.append(ln([(520, y), (1160, y)], round(td + .4 + .1 * k, 2), GOLD, 3, dur=.7))
    els += grid + [lab(840, 770, "the digging: on top", td + 1.0, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s26():
    """The land around the ruins, from above: 122 BCE; a grid of square fields draws itself across it and green crops appear; 6,000
    settlers as 60 small figures (1 = 100)."""
    t122, tv, ts, tf = T("s26", "In one twenty-two"), T("s26", "Rome voted"), T("s26", "six thousand settlers"), T("s26", "farm the land")
    els = [rect(0, 0, W_, 1000, "#3d3324", at=-1), poly([(1400, 0), (1778, 0), (1778, 300), (1560, 210)], "#2a5a78", at=-1, curve=True)]
    els += [poly(blob(1450, 200, 170, 90, 18, .25, 3), "#211812", "rgba(255,160,100,.35)", 2, -1), lab(1450, 330, "the ruins", -1, DIM, 26)]
    r = random.Random(26)
    for k in range(14):
        els.append(rect(r.uniform(1320, 1560), r.uniform(150, 250), r.uniform(10, 24), r.uniform(8, 14), "#120c09", at=-1))
    els += chip(260, 180, "122 BCE", GOLD, t122, 30) + [lab(260, 240, "24 years after the fire", t122 + .4, DIM, 24)]
    gx0, gy0, gs, nx, ny = 90, 300, 96, 13, 4
    for k in range(nx + 1):
        els.append(ln([(gx0 + gs * k, gy0), (gx0 + gs * k, gy0 + gs * ny)], round(tv + .05 * k, 2), "#d8c9a8", 2.5, dur=.6))
    for k in range(ny + 1):
        els.append(ln([(gx0, gy0 + gs * k), (gx0 + gs * nx, gy0 + gs * k)], round(tv + .3 + .08 * k, 2), "#d8c9a8", 2.5, dur=.9))
    for k in range(nx * ny):
        i, j = k % nx, k // nx
        if r.random() < .8:
            els.append(rect(gx0 + gs * i + 8, gy0 + gs * j + 8, gs - 16, gs - 16, "rgba(127,196,106,.55)", at=round(tf - .8 + .012 * k, 2), fx="pop", r=3))
    for k in range(60):
        x = 140 + 26 * (k % 30) + (k // 30) * 13
        els += fig(x, 740 + 42 * (k // 30), 34, round(ts + .03 * k, 2), SKIN, fx="rise")
    els += [lab(1000, 744, "6,000 settlers", ts + .6, BONE, 32, "start", st="serif"), lab(1000, 784, "1 figure = 100", ts + .8, DIM, 24, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s27():
    """Roman Carthage rises, about a century after the fire: the forum platform on the Byrsa, a temple, an aqueduct coming in from the
    hills, a theatre, great baths by the sea and the round harbour, in daylight."""
    tc, tr, tw = T("s27", "About a century"), T("s27", "a Roman Carthage rose"), T("s27", "great cities")
    G = 640
    els = [poly([(0, G), (230, 560), (420, 520), (560, 540), (640, G)], "#5a6a4a", at=-1, curve=True)]
    hill = [(560, G), (640, 560), (720, 470), (800, 430), (1000, 430), (1080, 470), (1160, 560), (1240, G)]
    els += [poly(hill, "#8a7458", "rgba(255,236,206,.5)", 1.5, -1), rect(780, 418, 240, 14, LIME, LIME_L, 1, 1, -1)]
    els += chip(260, 180, "about 100 years later", GOLD, tc, 28)
    for k in range(6):
        els.append(rect(818 + 34 * k, 362, 12, 56, LIME_L, "#fff4dc", 1, 1, round(tr + .05 * k, 2), fx="fill"))
    els += [rect(806, 352, 190, 12, LIME, LIME_L, 1, 1, tr + .4, fx="pop"), poly([(806, 352), (901, 326), (996, 352)], LIME, LIME_L, 1, tr + .5, fx="pop")]
    # aqueduct from the hills
    els += [poly([(1180, 600), (1778, 600), (1778, G), (1180, G)], "#3f86b0", at=-1), ln([(1180, 600), (1778, 600)], -1, "#9fd0ff", 1.5, draw=False, op=.6)]
    for k in range(9):
        x, top = 120 + 52 * k, 520 - k * 2
        arch = [(x + 44 - 18 * (1 - math.cos(math.pi * j / 8)), top + 40 - 18 * math.sin(math.pi * j / 8)) for j in range(9)]
        els.append(poly([(x, G - 6), (x, top), (x + 52, top), (x + 52, G - 6), (x + 44, G - 6)] + arch + [(x + 8, G - 6)], "#b39a74", "#e6d4b4", 1,
                        round(tr + .6 + .08 * k, 2), fx="rise"))
    # theatre (cavea in elevation), baths by the sea, the round harbour
    els += [poly([(1200, G), (1210, 540), (1530, 540), (1540, G)], "#a8916c", "#efe2c8", 1.2, tr + 1.2, fx="rise")]
    for row, y0 in enumerate((598, 566)):
        for k in range(10):
            x = 1222 + 31 * k
            els.append(poly([(x, y0 + 30 - row * 4)] + E(x + 11, y0 + 8, 11, 12, 8, 180, 360) + [(x + 22, y0 + 30 - row * 4)], "#5a4632", at=round(tr + 1.3, 2)))
    els += [rect(1560, 520, 180, 120, "#c4ad86", "#efe2c8", 1.2, 4, tr + 1.6, fx="rise"),
            poly(E(1600, 520, 34, 30, 20, 180, 360), "#d8c9a8", "#efe2c8", 1, tr + 1.8, fx="pop"), poly(E(1690, 520, 34, 30, 20, 180, 360), "#d8c9a8", "#efe2c8", 1, tr + 1.9, fx="pop")]
    els += [poly([(0, G), (1778, G), (1778, 1000), (0, 1000)], "#4a4030", at=-1)]
    els += [poly([(0, 712), (1778, 690), (1778, 724), (0, 750)], "#6a5a44", at=-1), ln([(0, 712), (1778, 690)], -1, "rgba(255,236,206,.3)", 2, draw=False)]
    for k, x in enumerate((70, 420, 1130, 1470)):
        els += [poly([(x - 14, 700), (x, 600), (x + 14, 700)], "#2f3a24", at=-1, curve=True)]
    for k in range(6):
        els += fig(980 + 40 * k, G, 26, round(tw + .1 * k, 2), "#3a2c20")
    for k in range(9):
        els += fig(200 + 150 * k + (k % 2) * 40, 716 - k * 2.6, 46, round(tw + .3 + .08 * k, 2), "#2a1f17", None, 1 if k % 3 else -1)
    els += [lab(900, 290, "Roman Carthage", tr + .3, GOLD, 32), lab(1370, 500, "a theatre", tr + 1.6, "#efe2c8", 24), lab(1650, 470, "baths", tr + 2.0, "#efe2c8", 24)]
    return {"base": "sky", "tod": "day", "ground": G, "sun": [1450, 180, 30], "cam": CAM, "els": els}


def sheaf(x, y, s, at, c="#e8c35a"):
    """A wheat sheaf standing on y: stalks fanning out above and below a tie, ears at the top."""
    els = []
    for k in range(-3, 4):
        els.append(ln([(x + k * s * .03, y), (x, y - s * .45), (x + k * s * .09, y - s)], at, c, max(1.5, s * .025), curve=True, draw=False))
        els.append(poly(E(x + k * s * .09, y - s - s * .06, s * .035, s * .1, 10), c, at=at))
    els.append(rect(x - s * .08, y - s * .5, s * .16, s * .07, "#a8784e", at=at))
    return [grp(els, at, "rise")]


def s28():
    """Grain for Rome: the central Mediterranean again; a gold route from Carthage to Rome with grain ships along it; wheat sheaves rise
    on the African coast; on 'salted earth', a lilac dotted 'salted?' over the fields, struck through."""
    v = VMED
    tg, tf, ts = T("s28", "granaries"), T("s28", "fed Rome"), T("s28", "for salted earth")
    cx, cy = v.p(*CARTHAGE)
    rx, ry = v.p(*ROME_)
    els = [{"k": "map", "land": v.land(), "in": -1}, pin(cx, cy, "Carthage", .3, GOLD, "start", 22, 34), pin(rx, ry, "Rome", .3, ROMAN, "start", 22, 8)]
    route = [(cx + 10, cy - 12), v.p(11.4, 38.6), v.p(11.6, 40.4), (rx - 6, ry + 10)]
    els += [ln(route, .5, GOLD, 4, dur=1.6, curve=True)]
    for k, (lon, lat) in enumerate(((10.9, 37.7), (11.1, 39.0), (11.5, 40.3))):
        x, y = v.p(lon, lat)
        els += merchant(x + 30, y, 54, round(.9 + .4 * k, 2))
    for k, (lon, lat) in enumerate(((7.4, 35.55), (8.1, 35.3), (8.8, 35.6), (9.5, 35.35), (10.1, 35.65))):
        x, y = v.p(lon, lat)
        els += sheaf(x, y + 30, 70, round(tg + .15 * k, 2))
    sx, sy = v.p(4.6, 35.95)
    els += [lab(sx, sy, "grain for Rome", tf, GOLD, 32)]
    els += chip(sx, sy + 62, "salted?", LILAC, ts, 28, style="claimed") + [strike(sx - 85, sy + 80, sx + 85, sy + 44, ts + .5, RED, 5)]
    return {"base": "map", "cam": CAM, "els": els}


# ================================================================== 4 · urns and vows
def s29():
    """The harbour quarter in plan: the round war harbour and the rectangular trading harbour by the sea; just west of them a small walled
    enclosure fills with tiny standing stones ('the tophet'), in today's Salammbo; a time bar fills from about 750 BCE to the fire of 146."""
    tu, tf = T("s29", "seven fifty"), T("s29", "Roman fire")
    coast = [(1330, 0), (1300, 200), (1330, 380), (1290, 560), (1340, 760), (1310, 1000)]
    els = [rect(0, 0, W_, 1000, "#3a3024", at=-1), poly(coast + [(1778, 1000), (1778, 0)], "#2a5a78", at=-1), ln(coast, -1, "#c9ad85", 2, curve=True, draw=False)]
    els += [poly(E(1060, 250, 120, 120, 48), SEAC, SEAL, 2, -1), poly(E(1060, 250, 38, 38, 24), "#8f7a5c", "#e0cfa8", 1.5, -1),
            rect(1046, 368, 28, 52, SEAC, at=-1), rect(960, 420, 200, 120, SEAC, SEAL, 2, 3, -1), rect(1160, 462, 160, 30, SEAC, at=-1),
            lab(1060, 108, "the old harbours", .3, DIM, 26)]
    tx, ty, tw, th = 620, 400, 230, 180
    els += [rect(tx, ty, tw, th, "rgba(184,139,94,.18)", GOLD, 3, 10, .4, fx="draw")]
    r = random.Random(29)
    for k in range(56):
        x, y = tx + 18 + (k % 11) * 18.5 + r.uniform(-3, 3), ty + 22 + (k // 11) * 30 + r.uniform(-3, 3)
        els.append(rect(x, y, 7, 12, LIME_L, at=round(.6 + .015 * k, 2), r=2))
    els += [gl(tx + tw / 2, ty + th / 2, 170, .7, .35, "lamp"), lab(tx + tw / 2, ty - 26, "the tophet", .6, GOLD, 32),
            lab(tx + tw / 2, ty + th + 60, "Salammbo", .9, "#c9ad85", 30, st="ital")]
    X = lambda yr: round(300 + (800 - yr) / 700 * 900, 1)
    els += [rect(X(800), 700, X(100) - X(800), 18, "rgba(255,255,255,.06)", "rgba(255,236,206,.25)", 1, 9, .3)]
    els += [rect(X(750), 700, X(146) - X(750), 18, PUNIC, at=tu, fx="fill", r=9), lab(X(750), 680, "750 BCE", tu, BONE, 26),
            lab(X(146), 680, "146 BCE", tf, ROMAN, 26), lab((X(750) + X(146)) / 2, 760, "about six centuries", tf + .3, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


TS0, TL = 300, [(300, 430), (430, 570), (570, 720)]           # the tophet section: ground, and its three layers (older below)
TSX = [150 + 118 * k for k in range(8)]                        # where the stones stand


def s30():
    """The tophet in section: three layers of earth, older below, each with small clay urns under narrow stones; lamps glow among the stones
    on the surface; no remains drawn. At the right, 200 marks fill row by row (1 mark = 100 urns): up to 20,000 urns, 400 to 200 BCE,
    about 100 a year."""
    tl, te, tc, ty = T("s30", "layers of small clay urns"), T("s30", "twenty thousand urns"), T("s30", "two of those centuries"), T("s30", "a hundred every year")
    els = [rect(60, TS0, 960, 440, EARTH_D, at=-1)]
    for k, (y0, y1) in enumerate(TL):
        els += [rect(60, y0, 960, y1 - y0, ("#4a3a2a", "#3f3124", "#33271c")[k], at=-1), ln([(60, y0), (1020, y0)], -1, "rgba(255,226,190,.25)" if k else "#8a6a48", 2, draw=False)]
    r = random.Random(30)
    for k, (y0, y1) in enumerate(TL):
        for j in range(8):
            x = 120 + 118 * j + r.uniform(-16, 16) + (k % 2) * 50
            if x > 1000:
                continue
            at = round(tl + .3 * (2 - k) + .05 * j, 2) if k else round(tl + .9 + .05 * j, 2)
            els += urn(x, y1 - 18, 46, at, mix(CLAY, "#3a2a1e", k * .22), rim=mix(CLAY_L, "#5a4a3a", k * .3))
            if k:
                els += stele(x + 30, y1 - 22, 22, 56, at, mix(LIME, "#3a2a1e", .3 + .15 * k), LIME_D, sign=False, crescent=False, lines=0, fx="pop")
    for j, x in enumerate(TSX):
        h = 92 + 18 * (j % 3)
        els += stele(x + 30, TS0, h * .42, h, -1, LIME, LIME_L, sign=(j % 2 == 0), crescent=(j % 3 == 0), lines=0, fx=None)
    for x in TSX[::2]:
        els += [gl(x + 70, TS0 - 10, 70, -1, .45, "fire"), circ(x + 70, TS0 - 12, 3, "#ffd27a", at=-1)]
    els += [arr([(1068, 330), (1068, 700)], tl + 1.6, DIM, 2.5, dur=.6, curve=False), lab(1068, 746, "older below", tl + 1.8, DIM, 24)]
    # 200 marks of 100 urns
    bx0, by0 = 1120, 250
    for k in range(200):
        i, j = k % 20, 9 - k // 20
        els.append(rect(bx0 + 26 * i, by0 + 26 * j, 20, 20, CLAY, at=round(te + .1 * (k // 20) + .004 * i, 3), fx="pop", r=7))
    els += [lab(bx0 + 257, by0 - 30, "up to 20,000 urns", te + .2, BONE, 34, st="serif"), lab(bx0 + 257, by0 + 300, "1 mark = 100 urns", te + 1.2, DIM, 24)]
    els += chip(bx0 + 257, by0 + 356, "400 to 200 BCE", GOLD, tc, 28) + [lab(bx0 + 257, by0 + 440, "about 100 a year", ty, AMBER, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


STL = (700, 790, 300, 600)                     # the big stele: centre x, foot y, width, height


def big_stele(at=-1):
    x, y, w, h = STL
    top = y - h
    shape = [(x - w / 2, y), (x - w / 2, top + w * .42), (x, top), (x + w / 2, top + w * .42), (x + w / 2, y)]
    return [poly(shape, LIME, LIME_L, 2, at, fx="rise"), poly([(x - w / 2, y), (x - w / 2, top + w * .42), (x - w * .4, top + w * .46), (x - w * .4, y)], "rgba(0,0,0,.16)", at=at, fx="rise"),
            ln([(x - w / 2 + 16, top + w * .42 + 10), (x, top + 18), (x + w / 2 - 16, top + w * .42 + 10)], at, "rgba(120,100,70,.5)", 2, draw=False)]


def s31():
    """One stele drawn large in lamp light, its carvings appearing as named: the sign of Tanit, a raised hand, three lines of a short
    dedication: a vow to Baal Hammon and Tanit; behind it a dim field of small stelae (thousands of them)."""
    ts, tt, th, td, tb, tv = (T("s31", "called stelae"), T("s31", "goddess Tanit"), T("s31", "a raised hand"), T("s31", "a short dedication"),
                              T("s31", "Baal Hammon"), T("s31", "heard the giver's voice"))
    x, y, w, h = STL
    els = []
    r = random.Random(31)
    for k in range(22):
        sx, sh = 100 + 75 * k + r.uniform(-10, 10), r.uniform(60, 110)
        if 160 < sx < 930:
            continue
        els += stele(sx, 700 + (k % 3) * 22, sh * .42, sh, -1, "#5a4c3c", "rgba(255,226,190,.25)", sign=(k % 2 == 0), crescent=False, lines=0, fx=None, op=.6)
    els += [rect(0, 760, W_, 240, "#211912", at=-1), gl(x, 760, 420, -1, .35, "fire")]
    els += big_stele(.2) + lamp(x + 210, 790, 40, .4, .7)
    top = y - h
    els += [circ(x, top + 62, 13, LIME_D, at=ts), ln([(x - 32, top + 74), (x, top + 102), (x + 32, top + 74)], ts, LIME_D, 4, curve=True, draw=False)]
    els += raised_hand(x, 400, 110, th, LIME_D, fx="pop")
    els += tanit(x, 600, 150, tt, LIME_D, fx="pop")
    for k in range(3):
        els += punic_letters(x - 110, 646 + 36 * k, 9, round(td + .2 * k, 2), LIME_D, 22, 7 + k, 3, step=27)
    els += [gl(x, 680, 160, tv, .45, "lamp")]
    els += [ln([(x + 90, 520), (1010, 470)], tt + .2, GOLD, 2, dur=.4), lab(1022, 478, "the sign of Tanit", tt + .3, GOLD, 30, "start"),
            ln([(x + 60, 340), (1010, 300)], th + .2, GOLD, 2, dur=.4), lab(1022, 308, "a raised hand", th + .3, GOLD, 30, "start"),
            ln([(x + 130, 680), (1010, 660)], td + .3, AMBER, 2, dur=.4), lab(1022, 668, "a vow", td + .4, AMBER, 32, "start"),
            lab(1022, 712, "to Baal Hammon and Tanit", tb, DIM, 26, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s32_add():
    """The same stele: the first line of the dedication (the giver's name) glows green, 'the giver's name'; beside it a lilac dotted empty
    box, 'no child's name'; then a lilac question mark."""
    tn, tc, tq = T("s32", "They name the person"), T("s32", "not the"), T("s32", "If these were")
    x = STL[0]
    els = [rect(x - 122, 626, 244, 34, "rgba(143,217,176,.18)", GREEN, 2.5, 8, tn + .2, fx="pop"), gl(x, 643, 120, tn + .2, .4, "lamp"),
           ln([(x - 124, 643), (500, 570)], tn + .4, GREEN, 2, dur=.4), lab(500, 556, "the giver's name", tn + .5, GREEN, 30, "end")]
    els += [rect(340, 624, 190, 40, "rgba(201,193,238,.05)", LILAC, 2.5, 8, tc, fx="draw", style="claimed"), lab(435, 704, "no child's name", tc + .3, LILAC, 28)]
    els += qmark(330, 400, tq, 110)
    return els


XD = lambda yr: round(150 + (yr + 400) / 650 * 1500, 1)        # 400 BCE to 250 CE (BCE negative)


def s33():
    """What the writers said: a timeline from 400 BCE to 250 CE; Diodorus, a writer with a scroll, about 30 BCE; a crisis ringed at 310 BCE;
    an arrow between them, about 280 years; his claim drawn back to the ring in lilac dots; then many small books pop along the line
    (many writers, mostly outsiders)."""
    tdi, t280, tcr, tsac, tout, tmany = (T("s33", "Diodorus"), T("s33", "two hundred and eighty years"), T("s33", "a single crisis"), T("s33", "sacrificed"),
                                         T("s33", "Most were outsiders"), T("s33", "many of them"))
    ay = 560
    els = [axis(XD(-400), XD(250), ay, [(XD(-400), "400 BCE"), (XD(-200), "200 BCE"), (XD(0), "1 CE"), (XD(200), "200 CE")], .2)]
    xd = XD(-30)
    els += fig(xd, ay - 8, 150, tdi, BONE, "hold", -1) + scroll(xd - 52, ay - 74, 50, tdi + .3) + [lab(xd, ay - 190, "Diodorus", tdi + .2, AMBER, 32)]
    xc = XD(-310)
    els += [circ(xc, ay, 40, "none", PUNIC, 3.5, tcr, fx="draw"), circ(xc, ay, 9, PUNIC, at=tcr + .2)] + chip(xc, ay - 150, "a crisis, 310 BCE", PUNIC, tcr + .3, 28)
    els += [arr([(xc + 40, ay + 86), (xd - 10, ay + 86)], t280, AMBER, 3, dur=1.0, curve=False), lab((xc + xd) / 2, ay + 130, "about 280 years later", t280 + .5, AMBER, 30)]
    els += [ln([(xd - 70, ay - 80), ((xc + xd) / 2 + 40, ay - 250), (xc + 44, ay - 14)], max(tsac, tcr + .5), LILAC, 3, "claimed", dur=1.2, curve=True)]
    for k, yr in enumerate((-340, -280, 50, 95, 125, 200)):
        x = XD(yr)
        els += book(x, ay - 44, 30, round(tout + .9 + .15 * k, 2), "#5a4a6a")
    els += [lab(XD(110), ay - 120, "many writers", tmany, LILAC, 30), lab(XD(110), ay - 84, "mostly outsiders", tmany + .2, DIM, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def lamb(x, y, s, at, c=LIME_D, fx="pop"):
    """A small lamb in side view, facing left, standing on y; s = its body length."""
    P = lambda u, v: (x + u * s, y - v * s)
    els = [poly(E(*P(0, .42), .5 * s, .22 * s, 20), c, at=at), poly(E(*P(-.5, .62), .16 * s, .11 * s, 14, 0, 360), c, at=at),
           poly([P(-.42, .7), P(-.3, .8), P(-.34, .64)], c, at=at)]
    for u in (-.32, -.18, .2, .34):
        els.append(ln([P(u, .3), P(u, 0)], at, c, max(2, s * .06), draw=False))
    return [grp(els, at, fx)] if fx else els


def s34():
    """The same rite: two identical urns under two identical stones, one stone marked with a small lamb, the other with a soft light, as
    named: the same fire, the same urns, the same stones. Then a Roman stele from Algeria (about 200 CE) with a lamb in its niche rises at
    the right; 'life for life' glows on it; 'for a child?' in lilac dashes."""
    tsame, tfi, tur, tst, tcen, tlamb, tlife = (T("s34", "the same rite"), T("s34", "the same fire"), T("s34", "the same urns"), T("s34", "the same stones"),
                                                T("s34", "Centuries later"), T("s34", "a lamb offered"), T("s34", "life for life"))
    G = 560
    els = [rect(0, G, 1000, 440, "#3a2c20", at=-1), ln([(0, G), (1000, G)], -1, "#8a6a48", 2.5, draw=False)]
    for k, x in enumerate((480, 720)):
        els += stele(x, G, 120, 230, .3, LIME, LIME_L, sign=True, crescent=True, lines=1, fx="rise", seed=3)
        els += urn(x, G + 150, 74, .5)
    els += lamb(480, G - 150, 50, tsame + .3, LIME_D) + [circ(720, G - 168, 16, "#fff1d0", at=tsame + .3), gl(720, G - 168, 60, tsame + .3, .6, "lamp")]
    els += flame(600, 250, 70, tfi) + [lab(120, 236, "the same fire", tfi + .1, AMBER, 30, "start"), ln([(330, 228), (555, 228)], tfi + .2, AMBER, 2, "inferred", dur=.4)]
    els += [lab(120, 700, "the same urns", tur, AMBER, 30, "start"), ln([(320, 692), (430, 692)], tur + .1, AMBER, 2, "inferred", dur=.4),
            lab(120, 460, "the same stones", tst, AMBER, 30, "start"), ln([(340, 452), (414, 452)], tst + .1, AMBER, 2, "inferred", dur=.4)]
    # the Roman stele from N'Gaous
    rx, ry, rw, rh = 1330, 760, 250, 470
    els += [rect(1010, 120, 2, 640, "rgba(255,236,206,.18)", at=tcen)]
    els += [poly([(rx - rw / 2, ry), (rx - rw / 2, ry - rh + rw / 2)] + E(rx, ry - rh + rw / 2, rw / 2, rw / 2, 16, 180, 360)[1:] + [(rx + rw / 2, ry)], LIME, LIME_L, 2, tcen, fx="rise"),
            rect(rx - 90, ry - rh + 70, 180, 120, "rgba(0,0,0,.2)", LIME_D, 1.5, 6, tcen + .1)]
    els += chip(rx, 160, "Roman Algeria, about 200 CE", GOLD, tcen + .3, 26)
    els += lamb(rx + 5, ry - rh + 172, 90, tlamb, LIME_D)
    for k in range(4):
        els.append(ln([(rx - 90, ry - 230 + 34 * k), (rx + 90 - (k % 2) * 30, ry - 230 + 34 * k)], tlamb + .2, "rgba(110,90,62,.8)", 3, draw=False))
    els += [gl(rx, ry - 70, 150, tlife, .5, "lamp"), lab(rx, ry - 58, "life for life", tlife, GOLD, 34, st="serif")]
    els += [arr([(rx - 40, ry - rh + 84), (rx - 40, 262)], tlamb + .9, LILAC, 3, "inferred", dur=.5, curve=False), lab(rx - 40, 246, "for a child?", tlamb + 1.2, LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s35_add():
    """Read this way: small lamps light one by one along the stones of the tophet section; 'an offering, a promise kept' (one reading)."""
    tu, tk = T("s35", "each urn"), T("s35", "a promise kept")
    els = []
    for j, x in enumerate(TSX):
        els += lamp(x + 70 if j % 2 else x - 6, TS0, 20, round(.3 + .18 * j, 2), .55)
    for j in range(8):
        els.append(gl(120 + 118 * j, 400, 60, round(tu + .08 * j, 2), .35, "lamp"))
    els += [lab(560, 150, "an offering, a promise kept", tk, AMBER, 32), lab(560, 192, "one reading", tk + .3, DIM, 24)]
    return els


# ================================================================== 5 · what the bones say
def bench(x0, x1, y, at, c, face=1):
    """A lab bench seen from the front with a scientist behind it and a microscope on it."""
    els = [rect(x0, y, x1 - x0, 16, "#6a5a48", "#cbbca8", 1.2, 3, at), rect(x0 + 16, y + 16, 12, 120, "#4a3e32", at=at), rect(x1 - 28, y + 16, 12, 120, "#4a3e32", at=at)]
    mx = x0 + (x1 - x0) * (.7 if face > 0 else .3)
    els += [rect(mx - 30, y - 8, 60, 8, "#8a8f96", at=at), ln([(mx - 10, y - 8), (mx - 4, y - 70), (mx + 18, y - 96)], at, "#aeb4bb", 7, draw=False),
            ln([(mx + 10, y - 104), (mx + 26, y - 88)], at, "#d8dde2", 9, draw=False), circ(mx - 4, y - 40, 6, c, at=at)]
    fx_ = x0 + (x1 - x0) * (.35 if face > 0 else .65)
    els += fig(fx_, y + 4, 150, at, "#d8d2c8", "hold", face, fx=None)[0]["els"]
    els += [rect(x0, y - 2, x1 - x0, 4, c, at=at, op=.7)]
    return [grp(els, at, "rise")]


def s36():
    """Two lab benches facing each other, the same row of small urns between them ('team one' in blue, 'team two' in amber); then a wall
    calendar with weekly pages: 'an age in weeks'. No remains are drawn."""
    tc, tw = T("s36", "like a calendar"), T("s36", "an age in weeks")
    els = [rect(0, 640, W_, 360, "#1e1712", at=-1)]
    els += bench(120, 560, 560, .3, BLUE, 1) + bench(1218, 1658, 560, .5, AMBER, -1)
    els += [lab(340, 760, "team one", .6, BLUE, 30), lab(1438, 760, "team two", .8, AMBER, 30)]
    els += [rect(640, 600, 500, 14, "#5a4a3a", "#cbbca8", 1, 3, .4)]
    for k in range(7):
        els += urn(680 + 70 * k, 600, 50, round(.5 + .06 * k, 2))
    cx, cy, cw, ch = 890, 330, 330, 230
    els += [rect(cx - cw / 2, cy - ch / 2, cw, ch, "#efe4cc", "#8a7a66", 2, 6, tc, fx="pop"), rect(cx - cw / 2, cy - ch / 2, cw, 40, PUNIC, at=tc + .05, r=6)]
    for k in range(4):
        els.append(circ(cx - 120 + 80 * k, cy - ch / 2, 8, "#cbbca8", "#5a4a3a", 1.5, tc + .05))
    for r_ in range(4):
        for c_ in range(7):
            els.append(rect(cx - 140 + 40 * c_, cy - 62 + 42 * r_, 32, 32, "#d8c9a8", at=round(tc + .2 + .015 * (r_ * 7 + c_), 3), r=3))
    els += [rect(cx - 146, cy - 66 + 42, 284, 40, "rgba(143,217,176,.35)", GREEN, 2.5, 6, tw, fx="pop"), lab(cx, cy + 160, "an age in weeks", tw + .2, GREEN, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


AX0, AX1, AYT, AYB = 260, 1560, 462, 498          # the shared age axis: x from 2 months before birth to 6 months, the two baselines
XM = lambda m: round(AX0 + (m + 2) / 8 * (AX1 - AX0), 1)
BINW = (AX1 - AX0) / 16
SCHW = [.25, .4, .55, .7, .95, .85, .75, .62, .52, .45, .38, .3, .25, .2, .14, .1]      # schematic: at least a fifth before birth
SMITH = [.01, .02, .03, .04, .08, .22, 1.0, .2, .1, .06, .04, .03, .02, .02, .01, .01]   # schematic: most at 1 to 1.5 months
NAT = [(XM(-1), 330), (XM(-.4), 262), (XM(0), 238), (XM(.7), 284), (XM(1.6), 340), (XM(3), 396), (XM(4.5), 430), (XM(6), 446)]


def s37():
    """The first team's ages (schematic, after Schwartz et al. 2010, 348 urns): a shared age axis, before birth to 6 months, the birth line;
    blue bars rise above it, most around birth and in the first months, the block before birth shaded (at least 1 in 5); then a pale dashed
    curve of natural infant deaths (high at birth, falling) lays over them."""
    ts, tm, tb, tn = T("s37", "Jeffrey Schwartz"), T("s37", "Most of the babies"), T("s37", "before they were born"), T("s37", "natural deaths")
    els = [ln([(AX0, AYT), (AX1, AYT)], .2, "#cbbca8", 2.5, draw=False), ln([(AX0, AYB), (AX1, AYB)], .2, "#cbbca8", 2.5, draw=False),
           ln([(XM(0), 200), (XM(0), 770)], .3, BONE, 2, "inferred", dur=.6), lab(XM(0), 488, "birth", .4, BONE, 24), lab(AX1, 488, "6 months", .5, DIM, 24, "end")]
    els += [lab(AX0, 168, "Schwartz et al. 2010, 348 urns", ts, BLUE, 28, "start")]
    for k, v in enumerate(SCHW):
        els.append(rect(AX0 + BINW * k + 4, AYT - v * 230, BINW - 8, v * 230, BLUE, at=round(tm + .08 * k, 2), fx="fill", r=3))
    els += [rect(AX0, 226, XM(0) - AX0, AYT - 226, "rgba(159,208,255,.12)", BLUE, 2, 6, tb, fx="draw", style="inferred"),
            lab((AX0 + XM(0)) / 2, 214, "at least 1 in 5 before birth", tb + .3, BLUE, 26)]
    els += [ln(NAT, tn, "#f5ead2", 3, "inferred", dur=1.4, curve=True), lab(XM(4.4), 400, "natural deaths", tn + 1.0, "#f5ead2", 26, "start")]
    els += [lab(AX1, 788, "schematic", .6, "#8a7a66", 22, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s38_add():
    """The second team (schematic, after Smith et al. 2011) on the same axis: amber bars hang below it with a sharp peak at 1 to 1.5 months;
    the natural-deaths curve, mirrored, does not follow the peak: 'too sharp?'."""
    tt, tp, tsh = T("s38", "Patricia Smith"), T("s38", "one and a half months"), T("s38", "a peak too sharp")
    els = [lab(AX1, 560, "Smith et al. 2011", tt, AMBER, 28, "end")]
    for k, v in enumerate(SMITH):
        y0 = AYB + 2
        els.append(rect(AX0 + BINW * k + 4, y0, BINW - 8, v * 230, AMBER, at=round(tp - 1.2 + .06 * k, 2), fx="pop", r=3))
    pk = AX0 + BINW * 6
    els += [rect(pk, AYB, BINW, 236, "none", GOLD, 2.5, 6, tp, fx="draw"), lab(pk + BINW + 18, 716, "a peak at 1 to 1.5 months", tp + .2, AMBER, 28, "start")]
    els += [ln([(x, 960 - y) for x, y in NAT], tsh, "#f5ead2", 3, "inferred", dur=1.2, curve=True), lab(pk - 18, 640, "too sharp?", tsh + .8, LILAC, 28, "end")]
    return els


def s39():
    """The catch: a calendar whose pages flip; one day lights green ('when'); beside it, the last page torn away, a lilac dotted outline
    where it was, with a question mark ('why')."""
    ta, tc, tt, twh, twy = (T("s39", "can show age"), T("s39", "cause of"), T("s39", "torn out"), T("s39", "tells you when"), T("s39", "never why"))
    cx, cy, cw, ch = 640, 450, 380, 330
    els = []
    for k in range(4):
        els.append(rect(cx - cw / 2 + 10 - 4 * k, cy - ch / 2 + 12 - 4 * k, cw, ch, "#d8cbb0" if k < 3 else "#efe4cc", "#8a7a66", 2, 8, round(.2 + .15 * k, 2), fx="pop"))
    x0, y0 = cx - cw / 2 - 2, cy - ch / 2 - 2
    els += [rect(x0, y0, cw, 50, PUNIC, at=.8, r=8)]
    for k in range(5):
        els.append(circ(x0 + 50 + 70 * k, y0, 9, "#cbbca8", "#5a4a3a", 1.5, .8))
    for r_ in range(5):
        for c_ in range(7):
            els.append(rect(x0 + 22 + 50 * c_, y0 + 72 + 48 * r_, 40, 38, "#d8c9a8", at=round(.9 + .01 * (r_ * 7 + c_), 3), r=4))
    gx, gy = x0 + 22 + 50 * 3, y0 + 72 + 48 * 2
    els += [rect(gx, gy, 40, 38, GREEN, at=ta, fx="pop", r=4), gl(gx + 20, gy + 19, 70, ta, .6, "lamp")]
    px = 1140
    els += [rect(px - cw / 2, cy - ch / 2, cw, ch, "rgba(201,193,238,.04)", LILAC, 3, 8, tc, fx="draw", style="claimed")]
    tear = [(px - cw / 2 + 14 * k, cy - ch / 2 + (10 if k % 2 else 0)) for k in range(int(cw / 14) + 1)]
    els += [ln(tear, tt, "#efe4cc", 3, dur=.6), rect(px - cw / 2, cy - ch / 2 - 22, cw, 22, "#efe4cc", "#8a7a66", 1.5, 4, tt)]
    els += qmark(px, cy + 50, tc + .4, 120)
    els += [lab(cx, cy + ch / 2 + 60, "when", twh, GREEN, 36, st="serif"), lab(px, cy + ch / 2 + 60, "why", twy, LILAC, 36, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


VTUN = View(7.4, 12.2, 32.3, 37.6, (90, 140, 600, 620))
ZITA = (11.1, 33.52)


def arm_hold(x, y, s, side, at):
    """A forearm and hand reaching down from above to hold something at (x, y) from one side (side -1 = from the left)."""
    P = lambda u, v: (x + side * u * s, y + v * s)
    els = [poly(capsule(*P(1.6, -2.4), *P(.42, -.5), .42 * s, .3 * s), SKIN, "rgba(120,80,50,.4)", 1.2, at),
           poly(capsule(*P(.48, -.6), *P(.18, .12), .34 * s, .26 * s), "#e0bb92", "rgba(120,80,50,.45)", 1.2, at),
           poly([P(1.9, -3.0), P(.62, -1.0), P(.86, -.84), P(2.1, -2.7)], "#5a4a6a", at=at)]
    return els


def s40():
    """Zita: a small map of Tunisia with Carthage and Zita pinned (about 50 BCE to 100 CE); at the right, two hands lower a small urn onto
    a bed of sand in a pit, a lamp glowing beside it; four findings pop as named. No remains drawn."""
    tz, t12, til, tca, tin, tcl = (T("s40", "At Zita"), T("s40", "twelve infants"), T("s40", "signs of illness"), T("s40", "burials were careful"),
                                   T("s40", "no sign of injury"), T("s40", "A clue"))
    v = VTUN
    els = [rect(0, 0, W_, 1000, "#16110d", at=-1), rect(80, 130, 620, 640, "#2a5a78", at=-1), {"k": "map", "land": v.land(), "in": -1},
           rect(0, 0, W_, 130, "#16110d", at=-1), rect(0, 0, 80, 1000, "#16110d", at=-1), rect(0, 770, W_, 230, "#16110d", at=-1),
           rect(80, 130, 620, 640, "none", "rgba(255,236,206,.25)", 1.5, 0, -1)]
    cx, cy = v.p(*CARTHAGE)
    zx, zy = v.p(*ZITA)
    els += [pin(cx, cy, "Carthage", .3, GOLD, "end", -20, -14), pin(zx, zy, "Zita", tz, AMBER, "end", -20, -14)]
    els += chip(zx - 60, zy + 70, "about 50 BCE to 100 CE", AMBER, tz + .4, 24)
    els += [rect(700, 0, 1078, 1000, "#16110d", at=-1)]
    G = 520
    els += [rect(760, G, 960, 280, "#3a2c20", at=-1), ln([(760, G), (1720, G)], -1, "#8a6a48", 2.5, draw=False),
            poly([(960, G), (1240, G), (1210, 690), (990, 690)], "#120c09", "#8a6a48", 2, -1), rect(992, 660, 216, 30, "#d8c49a", at=.4, fx="fill")]
    ux, uy = 1100, 662
    els += urn(ux, uy, 84, .6) + arm_hold(ux - 26, uy - 46, 46, -1, .6) + arm_hold(ux + 26, uy - 46, 46, 1, .6)
    els += lamp(1290, G, 34, .8, .7)
    for k, (t, at, c) in enumerate((("12 infants and children", t12, BONE), ("illness in most", til, AMBER), ("careful burials", tca, GREEN), ("no injury seen", tin, GREEN))):
        els += [lab(1330, 200 + 66 * k, t, at, c, 30, "start")]
    els += [gl(zx, zy, 90, tcl, .5, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


def s41():
    """Specialists divided: a balance; on the left pan a small stele and a scroll ('vows and texts', 'offered, at times'); on the right pan
    an urn with a lamp ('a resting place'); the beam rests almost level; at the pivot an age chart with a lilac question mark: 'the bones:
    not settled'."""
    tv, to, tr, tb = T("s41", "Many read the vows"), T("s41", "children offered here"), T("s41", "Others see a resting place"), T("s41", "The bones alone")
    px, py = 889, 300
    a = 0.0
    L = 330
    lx, ly = px - L * math.cos(a), py + L * math.sin(a)
    rx, ry = px + L * math.cos(a), py - L * math.sin(a)
    els = [rect(px - 10, py, 20, 420, "#8a7458", "#e0cfa8", 1.5, 3, .2), poly([(px - 140, 740), (px + 140, 740), (px + 90, 712), (px - 90, 712)], "#6a5a44", "#e0cfa8", 1.5, .2),
           ln([(lx, ly), (rx, ry)], .3, "#e0cfa8", 8, draw=False), circ(px, py, 14, GOLD, at=.3)]
    for (x, y) in ((lx, ly), (rx, ry)):
        els += [ln([(x, y), (x - 90, y + 170)], .4, "#cbbca8", 2, draw=False), ln([(x, y), (x + 90, y + 170)], .4, "#cbbca8", 2, draw=False),
                poly(E(x, y + 176, 110, 18, 30, 0, 180) + [(x - 110, y + 176)], "#8a7458", "#e0cfa8", 1.5, .4)]
    els += stele(lx - 30, ly + 172, 44, 100, tv, LIME, LIME_L, sign=True, crescent=False, lines=0, fx="pop") + scroll(lx + 40, ly + 140, 60, tv + .2)
    els += [lab(lx, ly - 40, "vows and texts", tv + .3, AMBER, 30), lab(lx, ly + 250, "offered, at times", to, AMBER, 28)]
    els += urn(rx, ry + 172, 70, tr) + lamp(rx + 60, ry + 172, 24, tr + .2, .6) + [lab(rx, ry - 40, "a resting place", tr + .3, BLUE, 30)]
    els += [rect(px - 60, 166, 120, 80, "rgba(18,13,10,.9)", "#cbbca8", 1.5, 8, tb, fx="pop")]
    for k, v_ in enumerate((.3, .7, .5, .9, .4)):
        els.append(rect(px - 48 + 20 * k, 236 - 60 * v_, 14, 60 * v_, "#cbbca8", at=tb + .1, r=2))
    els += qmark(px + 110, 250, tb + .5, 80) + [lab(px, 140, "the bones: not settled", tb + .7, LILAC, 28)]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s42():
    """The tophet at dusk: a field of small stelae among trees, small lamps glowing one by one at their feet; a hand sets down a last lamp."""
    tm = T("s42", "someone mourned")
    G = 520
    els = [poly([(0, G), (1778, G), (1778, 1000), (0, 1000)], "#241a14", at=-1)]
    for x, h in ((160, 260), (300, 200), (1480, 280), (1620, 220), (1380, 170)):
        els += [poly([(x - 24, G + 6), (x - 30, G - h * .4), (x - 10, G - h * .9), (x, G - h), (x + 10, G - h * .9), (x + 30, G - h * .4), (x + 24, G + 6)], "#151b12", at=-1, curve=True)]
    els += [poly(blob(560, G - 120, 130, 80, 16, .2, 4), "#1a2216", at=-1), rect(552, G - 60, 16, 66, "#1a1410", at=-1)]
    rows = [(G + 20, .55, 15, 70), (G + 80, .72, 12, 96), (G + 160, .9, 10, 122), (G + 250, 1.1, 8, 150)]
    r = random.Random(42)
    k = 0
    lamps = []
    for ri, (y, s, n, dx) in enumerate(rows):
        for j in range(n):
            x = 889 + (j - (n - 1) / 2) * dx * 1.35 + r.uniform(-10, 10)
            if not 90 < x < 1690:
                continue
            h = r.uniform(70, 100) * s
            els += stele(x, y, h * .42, h, -1, mix("#6a5c4a", "#cbbca8", s - .5), "rgba(255,226,190,.3)", sign=(j % 2 == 0), crescent=False, lines=0, fx=None)
            if ri >= 1 and j % 2 == 1:
                lamps.append((x + h * .3, y, 14 * s))
    for i, (x, y, s_) in enumerate(lamps):
        els += lamp(x, y, s_, round(.3 + .09 * i, 2), .6)
    els += lamp(900, 790, 22, tm + .5, .8) + hand_down(918, 742, 70, tm, fx="rise")
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1300, 470, 20], "cam": CAM, "els": els}


# ================================================================== 6 · Kerkouane and Dougga
VCAP = View(8.9, 11.9, 35.7, 37.4, (90, 120, 1600, 680))
KERK, KELIBIA = (11.0992, 36.9464), (11.09, 36.85)


def s43():
    """Cap Bon: Kerkouane pinned gold near the tip, Kelibia beside it, Carthage to the west across the gulf; a red arrow from the sea to
    Kelibia (256 BCE, a Roman army lands); 'left, about 250 BCE' at Kerkouane; scale bar 20 km."""
    tw, tl, tb = T("s43", "Rome's first war"), T("s43", "its people left"), T("s43", "never came back")
    v = VCAP
    els = [{"k": "map", "land": v.land(), "in": -1}, {"k": "scale", "x": 150, "y": 760, "w": round(v.km(20), 1), "t": "20 km", "in": .4}]
    cx, cy = v.p(*CARTHAGE)
    kx, ky = v.p(*KERK)
    lx, ly = v.p(*KELIBIA)
    els += [pin(cx, cy, "Carthage", .3, BONE, "end", -22, 8), pin(kx, ky, "Kerkouane", .3, GOLD, "end", -22, -14), gl(kx, ky, 110, .3, .5, "lamp")]
    cbx, cby = v.p(10.55, 36.58)
    els += [lab(cbx, cby, "Cap Bon", .6, "#c9ad85", 32, st="ital")]
    els += [pin(lx, ly, "Kelibia", tw, DIM, "end", -22, 30), arr([(lx + 330, ly + 120), (lx + 140, ly + 60), (lx + 18, ly + 6)], tw + .2, ROMAN, 5, dur=1.0, curve=True)]
    els += chip(lx + 300, ly + 160, "256 BCE", ROMAN, tw + .5, 28) + [lab(lx + 300, ly + 226, "a Roman army lands", tw + .7, ROMAN, 26)]
    els += chip(kx + 40, ky - 110, "left, about 250 BCE", GOLD, tl, 28) + [gl(kx, ky, 60, tb, .6, "red")]
    return {"base": "map", "cam": CAM, "els": els}


def s44():
    """Kerkouane from above (schematic plan): streets draw in a grid; houses pop round courtyards, a blue well in each; a small red seated
    bath in each house; then a sea snail's shell spirals at the right and a drop of purple falls from it."""
    tg, th, twl, tba, tp = (T("s44", "a grid"), T("s44", "houses round courtyards"), T("s44", "own wells"), T("s44", "a seated bath"), T("s44", "purple dye"))
    x0, y0, w, h = 110, 150, 1180, 620
    els = [rect(x0, y0, w, h, "#9c8a6a", at=-1, r=6), rect(x0, y0, w, h, "none", "#cbbca8", 1.5, 6, -1)]
    streets = [rect(x0, 436, w, 44, "#cbb891", at=tg, fx="draw", r=2)] + [rect(sx, y0, 44, h, "#cbb891", at=round(tg + .2 + .15 * k, 2), fx="draw", r=2)
                                                                    for k, sx in enumerate((390, 680, 970))]
    els += streets
    blocks = [(x0 + 14, y0 + 14, 262, 268), (434, y0 + 14, 242, 268), (724, y0 + 14, 242, 268), (1014, y0 + 14, 262, 268),
              (x0 + 14, 494, 262, 262), (434, 494, 242, 262), (724, 494, 242, 262), (1014, 494, 262, 262)]
    for k, (bx, by, bw, bh) in enumerate(blocks):
        at = round(th + .1 * k, 2)
        els += [rect(bx, by, bw, bh, "#d6c49c", "#8a6a44", 2.5, 4, at, fx="pop"), rect(bx + bw * .3, by + bh * .3, bw * .42, bh * .42, "#b3a07c", "#8a6a44", 1.5, 3, at)]
        els += [circ(bx + bw * .51, by + bh * .51, 15, "#3f86b0", "#9fd0ff", 2, round(twl + .08 * k, 2), fx="pop")]
        els += [rect(bx + 18, by + 18, 54, 34, "#b0442c", "#ffb09a", 1.5, 14, round(tba + .1 * k, 2), fx="pop"), rect(bx + 20, by + 20, 18, 30, "#7a2e1e", at=round(tba + .1 * k + .05, 2), r=5)]
    els += [ln([(702, 152), (790, 128)], tg + .5, GOLD, 2, dur=.4), lab(800, 132, "a grid", tg + .6, GOLD, 28, "start")]
    els += [ln([(x0 + 14 + 131, y0 + 14 + 137), (x0 + 330, 128)], twl + .3, "#9fd0ff", 2, dur=.4), lab(x0 + 340, 122, "a well", twl + .4, "#9fd0ff", 28, "start")]
    els += [lab(1014 + 131, 128, "a seated bath", tba + .5, "#ffb09a", 28), ln([(1014 + 60, y0 + 50), (1014 + 120, 136)], tba + .5, "#ffb09a", 2, dur=.4)]
    # the snail and its purple
    sx, sy = 1500, 360
    spiral = [(sx + (5 + 3.4 * t) * math.cos(t), sy + (5 + 3.4 * t) * math.sin(t)) for t in [i * .3 for i in range(44)]]
    els += [poly(blob(sx, sy, 64, 56, 18, .12, 2), "#e8dcc6", "#fff6e6", 2, tp - .6, fx="pop"), ln(spiral, tp - .4, "#8a7a66", 3, dur=.8, curve=True)]
    els += [poly([(sx + 40, sy + 40), (sx + 92, sy + 92), (sx + 70, sy + 104)], "#e8dcc6", "#fff6e6", 1.5, tp - .5, fx="pop")]
    els += [poly([(sx + 80, sy + 150), (sx + 100, sy + 190), (sx + 92, sy + 216), (sx + 68, sy + 216), (sx + 60, sy + 190)], "#7b3fa0", "#d9b0f0", 1.5, tp + .3, fx="pop", curve=True),
            gl(sx + 80, sy + 196, 100, tp + .4, .5, "lamp"), lab(sx + 80, sy + 290, "purple dye", tp + .5, "#d9b0f0", 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def s45():
    """Ancient DNA from 27 people at Kerkouane (Ringbauer et al. 2025): the Mediterranean; 27 small figures in a block, all filling gold as
    'Sicily and the Aegean' is said, 17 of them taking a green band (North African ancestry); a strong gold arrow from Sicily and the Aegean,
    a green one from inland North Africa, and only a faint dotted thread from the Levant."""
    t27, tsa, tna, tlv = T("s45", "twenty-seven people"), T("s45", "Sicily and the Aegean"), T("s45", "North African roots"), T("s45", "the Levant")
    v = VWIDE
    kx, ky = v.p(*KERK)
    els = [{"k": "map", "land": v.land(), "in": -1}, pin(kx, ky, "Kerkouane", .3, GOLD, "end", -22, -16), gl(kx, ky, 100, .3, .45, "lamp")]
    els += [lab(1690, 780, "Ringbauer et al. 2025", .6, DIM, 24, "end")]
    bx0, by0 = 330, 650
    green = set(random.Random(45).sample(range(27), 17))
    for k in range(27):
        x, y = bx0 + 31 * (k % 9), by0 + 50 * (k // 9)
        els += fig(x, y + 40, 36, round(t27 + .03 * k, 2), "#3a3028", fx="pop")
        els += fig(x, y + 40, 36, round(tsa + .02 * k, 2), GOLD, fx="pop")
        if k in green:
            els.append(rect(x - 6, y + 22, 12, 16, "#7fc46a", at=round(tna + .03 * k, 2), fx="fill", r=2))
    els += [lab(bx0 + 124, by0 - 20, "27 people", t27 + .3, BONE, 28)]
    gsrc = [v.p(25.5, 37.6), v.p(19.0, 37.4), v.p(14.0, 37.25), (kx + 14, ky - 4)]
    els += [ln(gsrc, tsa, GOLD, 6, "inferred", dur=1.2, curve=True), lab(*v.p(27.0, 38.9), "Sicily and the Aegean", tsa + .4, GOLD, 28)]
    nsrc = [v.p(4.0, 32.4), v.p(7.6, 34.2), (kx - 18, ky + 12)]
    els += [ln(nsrc, tna, "#7fc46a", 5, "inferred", dur=1.0, curve=True), lab(bx0 + 310, by0 + 64, "17: North African roots", tna + .4, "#9fd890", 26, "start")]
    lsrc = [v.p(35.0, 33.3), v.p(28.0, 33.0), v.p(18.0, 34.0), (kx + 10, ky + 14)]
    els += [ln(lsrc, tlv, LILAC, 1.6, "claimed", dur=1.4, curve=True, op=.6), lab(*v.p(34.6, 32.0), "the Levant", tlv + .5, LILAC, 26)]
    return {"base": "map", "cam": CAM, "els": els}


DG = (520, 700)                                   # the mausoleum of Dougga: centre x, ground y; 21 m = 520 units


def mausoleum(at=-1):
    x, G = DG
    m = 520 / 21
    els = []
    for k in range(5):
        w = 330 - 12 * k
        els.append(rect(x - w / 2, G - 12 * (k + 1), w, 12, "#b8a582", "#efe2c8", 1, 1, at))
    t1 = (G - 60 - 5 * m, G - 60)                 # tier 1: about 5 m
    els += [rect(x - 125, t1[0], 250, t1[1] - t1[0], "#c9b48c", "#efe2c8", 1.2, 1, at)]
    for sx in (x - 125, x + 109):
        els += [rect(sx, t1[0], 16, t1[1] - t1[0], "#d8c49c", at=at), rect(sx - 4, t1[0], 24, 10, "#e6d4b0", at=at)]
    els += [rect(x - 135, t1[0] - 14, 270, 14, "#d8c49c", "#efe2c8", 1, 1, at)]
    t2 = (t1[0] - 14 - 5 * m, t1[0] - 14)
    els += [rect(x - 110, t2[0], 220, t2[1] - t2[0], "#c4ae86", "#efe2c8", 1.2, 1, at)]
    for k in range(4):
        cx_ = x - 90 + 60 * k
        els += [rect(cx_ - 7, t2[0] + 8, 14, t2[1] - t2[0] - 8, "#e0cca6", at=at), rect(cx_ - 11, t2[0] + 4, 22, 6, "#efe2c8", at=at)]
    els += [rect(x - 122, t2[0] - 14, 244, 14, "#d8c49c", "#efe2c8", 1, 1, at)]
    t3 = (t2[0] - 14 - 3 * m, t2[0] - 14)
    els += [rect(x - 96, t3[0], 192, t3[1] - t3[0], "#c9b48c", "#efe2c8", 1.2, 1, at)]
    for sx in (x - 96, x + 84):
        els += [rect(sx - 4, t3[0] - 18, 20, 18, "#b8a582", at=at)]
    els += [poly([(x - 100, t3[0]), (x + 100, t3[0]), (x, G - 520)], "#d2bf98", "#efe2c8", 1.2, at), ln([(x, G - 520), (x + 100, t3[0])], at, "rgba(0,0,0,.15)", 6, draw=False)]
    els += [rect(x - 50, t1[0] + 30, 100, 60, "#8f7a5c", "#efe2c8", 1, 2, at)]          # the inscription panel
    return els, t1


def s46():
    """The Libyco-Punic mausoleum of Dougga at dusk: three tiers on a stepped base, pilasters and columns, a pyramid on top, a person at its
    foot (21 m); the inscription panel glows; the frieze enlarged beside it: Libyco-Berber signs on the left, Punic letters on the right."""
    t21, tin, tpu, tli = T("s46", "twenty-one metres"), T("s46", "an inscription in two"), T("s46", "One was Punic"), T("s46", "Libyco-Berber")
    x, G = DG
    els, t1 = mausoleum(-1)
    els = [poly([(0, G), (1778, G), (1778, 1000), (0, 1000)], "#2e241c", at=-1)] + els
    els += [lab(x, 150, "Dougga", .4, GOLD, 30)]
    els += fig(x - 205, G, 42, t21, SKIN) + [ln([(x - 250, G), (x - 250, G - 520)], t21 + .2, BONE, 2, dur=.6), lab(x - 266, G - 250, "21 m", t21 + .4, BONE, 30, "end")]
    els += [gl(x, t1[0] + 60, 120, tin, .6, "lamp"), rect(x - 50, t1[0] + 30, 100, 60, "none", GOLD, 2.5, 2, tin, fx="draw")]
    fx0, fy0, fw, fh = 900, 300, 760, 260
    els += [ln([(x + 50, t1[0] + 60), (fx0, fy0 + fh / 2)], tin + .3, GOLD, 2, "inferred", dur=.6),
            rect(fx0, fy0, fw, fh, "#cdbb95", "#fff3dc", 2, 4, tin + .5, fx="pop"), ln([(fx0 + fw / 2, fy0 + 16), (fx0 + fw / 2, fy0 + fh - 16)], tin + .6, "#8a7a66", 2, draw=False)]
    r = random.Random(46)
    for row in range(4):
        for k in range(8):
            els += libyan_sign(r.randrange(8), fx0 + 40 + 40 * k, fy0 + 50 + 54 * row, 26, round(tli + .02 * (row * 8 + k), 2), "#5a4632", 3)
        els += punic_letters(fx0 + fw / 2 + 30, fy0 + 50 + 54 * row, 9, round(tpu + .05 * row, 2), "#5a4632", 22, 11 + row, 2.6, step=36)
    els += [lab(fx0 + fw / 4, fy0 + fh + 46, "Libyco-Berber", tli + .2, BLUE, 30), lab(fx0 + 3 * fw / 4, fy0 + fh + 46, "Punic", tpu + .2, AMBER, 30)]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1500, 640, 22], "cam": CAM, "els": els}


def s47_add():
    """1842: the inscribed blocks are pulled out (a dark gap, the block lying on the ground), part of the tiers breaks and blocks tumble;
    then a name in the Punic half and the same name in the Libyan half light up, green lines join them letter to letter; 24 small sign
    tiles below, 22 turning green: '22 of 24 signs read'."""
    tp, tw, tn, tm, t22 = (T("s47", "pulled out"), T("s47", "wrecking the tomb"), T("s47", "names sound alike"), T("s47", "matching them"),
                           T("s47", "twenty-two of the twenty-four"))
    x, G = DG
    _, t1 = mausoleum(-1)
    els = chip(x - 200, 150, "1842", ROMAN, .3, 30)
    els += [rect(x - 50, t1[0] + 30, 100, 60, "#120c09", at=tp), rect(x + 150, G - 40, 100, 40, "#8f7a5c", "#efe2c8", 1, 2, tp + .2, fx="rise")]
    dmg = [(x + 40, G - 520 + 130), (x + 110, t1[0] - 240), (x + 120, t1[0] - 140), (x + 70, t1[0] - 90), (x + 30, t1[0] - 130), (x + 50, t1[0] - 220)]
    els += [poly(dmg, "#2a1f17", at=tw, fx="pop")]
    r = random.Random(47)
    for k in range(7):
        bx, by = x + 150 + r.uniform(-30, 120), G - r.uniform(8, 30)
        els.append({"k": "group", "tr": "rotate(%d %d %d)" % (r.randint(-25, 25), bx, by), "in": tw + .3,
                    "els": [rect(bx - 18, by - 12, 36, 24, "#c4ae86", "#efe2c8", 1, 1, tw + .3 + .05 * k, fx="pop")]})
    fx0, fy0, fw, fh = 900, 300, 760, 260
    els += [rect(fx0 + 22, fy0 + 24, 150, 52, "rgba(143,217,176,.2)", GREEN, 2.5, 6, tn, fx="pop"),
            rect(fx0 + fw - 22 - 210, fy0 + 24, 210, 52, "rgba(143,217,176,.2)", GREEN, 2.5, 6, tn + .2, fx="pop")]
    for k in range(3):
        els.append(ln([(fx0 + 60 + 40 * k, fy0 + 76), (fx0 + 330, fy0 + 140 + 10 * k), (fx0 + fw - 60 - 70 * k, fy0 + 76)], round(tm + .25 * k, 2), GREEN, 2, dur=.7, curve=True))
    for k in range(24):
        tx, ty = fx0 + 8 + 31.5 * k, 640
        els.append(rect(tx, ty, 26, 34, "#3a3028", "#8a7a66", 1.2, 4, round(t22 - .6 + .02 * k, 2), fx="pop"))
        if k not in (9, 17):
            els.append(rect(tx, ty, 26, 34, "#7fc46a", at=round(t22 + .06 * k, 2), fx="pop", r=4))
    els += [lab(fx0 + fw / 2, 724, "22 of 24 signs read", t22 + 1.2, GREEN, 30)]
    return els


SHARED = ((0, "r"), (2, "t"), (8, "l"), (6, "n"))           # shapes both scripts share: circle, cross, two bars, one bar


def s48():
    """Still mostly silent: a stone with ancient Libyan signs at the left ('the language: mostly silent'); an arrow; the same shapes as
    Tifinagh letters at the right ('Tifinagh, the Tuareg script'); below, the Libyan word for king as scholars write it, GLD, and a
    dashed arrow to 'agellid, king' (a proposed link)."""
    ts, ttf, ttu, tk, tag = (T("s48", "still mostly"), T("s48", "Tifinagh"), T("s48", "Tuareg script"), T("s48", "word for king"), T("s48", "agellid"))
    els = [poly([(150, 170), (640, 150), (660, 470), (140, 486)], "#a39070", "#e6d4b4", 2, .2, fx="pop")]
    for k, (kind, _) in enumerate(SHARED * 2):
        els += libyan_sign(kind, 210 + 120 * (k % 4), 240 + 140 * (k // 4), 70, round(.4 + .08 * k, 2), "#4a3a2a", 6)
    els += [lab(400, 540, "the language: mostly silent", ts + .3, LILAC, 28)]
    els += [arr([(700, 320), (1060, 320)], ttf - .3, GOLD, 4, dur=.8, curve=False)]
    els += [rect(1100, 170, 480, 300, "#2d5a8a", "#e6eef8", 3, 10, ttf, fx="pop")]
    for k, (kind, _) in enumerate(SHARED * 2):
        els += libyan_sign(kind, 1160 + 120 * (k % 4), 240 + 140 * (k // 4), 70, round(ttf + .2 + .06 * k, 2), "#f5f1e6", 6)
    els += [lab(1340, 540, "Tifinagh", ttf + .4, GOLD, 32), lab(1340, 580, "the Tuareg script", ttu, DIM, 26)]
    els += [rect(330, 640, 180, 90, "#a39070", "#e6d4b4", 2, 6, tk, fx="pop"), lab(420, 702, "GLD", tk + .2, "#3a2c20", 44, st="serif", halo=False),
            lab(420, 772, "king, in Libyan", tk + .4, DIM, 24)]
    els += [arr([(540, 685), (1000, 685)], tag - .2, LILAC, 3, "inferred", dur=.8, curve=False), lab(1030, 697, "agellid, king", tag + .3, LILAC, 34, "start", st="serif"),
            lab(1030, 740, "in Berber today?", tag + .6, DIM, 24, "start")]
    return {"base": "dark", "stars": 25, "cam": CAM, "els": els}


def s49():
    """How it died, how it lived: on the left in dim red, a scroll with flames behind it; on the right in warm light, the ground of
    everyday life: a courtyard house with its well and bath, a stele, a line of Libyan letters, ships in the round harbour."""
    td, tg, tl = T("s49", "how Carthage died"), T("s49", "The ground tells"), T("s49", "how it lived")
    els = [rect(0, 0, 889, 1000, "rgba(120,30,20,.18)", at=-1), ln([(889, 140), (889, 780)], -1, "rgba(255,236,206,.2)", 2, draw=False)]
    els += flame(380, 560, 230, .2) + flame(540, 570, 180, .3) + scroll(450, 580, 180, .4, "#e6d4b4")
    els += [lab(445, 730, "how it died", td, "#ff9a8a", 34, st="serif")]
    els += [gl(1330, 430, 420, tg, .3, "lamp")]
    hx, hy = 1010, 250
    els += [rect(hx, hy, 180, 160, "#d6c49c", "#8a6a44", 2.5, 4, tg, fx="pop"), rect(hx + 54, hy + 50, 76, 64, "#b3a07c", at=tg),
            circ(hx + 92, hy + 82, 12, "#3f86b0", "#9fd0ff", 2, tg + .1), rect(hx + 12, hy + 12, 44, 28, "#b0442c", "#ffb09a", 1.5, 10, tg + .1)]
    els += stele(1300, 420, 66, 160, tg + .3, LIME, LIME_L, sign=True, crescent=True, lines=1, fx="rise")
    for k, kind in enumerate((0, 2, 1, 5, 3, 6, 4)):
        els += libyan_sign(kind, 1420 + 36 * k, 300, 28, round(tg + .5 + .05 * k, 2), BONE, 3.5)
    els += [poly(E(1240, 560, 150, 40, 40), SEAC, SEAL, 2, tg + .7, fx="pop"), poly(E(1240, 560, 44, 12, 20), "#8f7a5c", "#e0cfa8", 1.5, tg + .75, fx="pop")]
    els += galley(1180, 560, 90, tg + .9, "#5a3c26", oars=False) + galley(1320, 566, 80, tg + 1.0, "#5a3c26", oars=False)
    els += [lab(1330, 690, "how it lived", tl, GOLD, 34, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================== 7 · the weighing
LROWS = [270, 390, 510, 630]


def ledger(title, at):
    return [rect(110, 170, 1560, 530, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, at), lab(140, 195, title, at + .2, GOLD, 26, "start", st="cap")]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1200, y, grade, gc, gt, 28, "start")
    return out


def pic_fire(x, y, at):
    return flame(x, y + 32, 64, at)


def pic_plough(x, y, at):
    return plough_icon(x, y, 70, at, GOLD)


def pic_salt(x, y, at):
    return [circ(x, y, 34, "rgba(201,193,238,.06)", LILAC, 2.5, at, style="claimed", fx="pop")] + salt_pinch(x, y, 16, at + .05, n=10)


def pic_stele(x, y, at):
    return stele(x, y + 40, 34, 80, at, LIME, LIME_L, sign=True, crescent=False, lines=0, fx="pop")


def pic_urnstele(x, y, at):
    return [grp(urn(x - 20, y + 38, 44, at, fx=None) + stele(x + 18, y + 38, 26, 66, at, LIME, LIME_L, sign=True, crescent=False, lines=0, fx=None), at, "pop")]


def pic_bath(x, y, at):
    return [grp([rect(x - 38, y - 22, 76, 44, "#b0442c", "#ffb09a", 2, 16, at), rect(x - 34, y - 18, 26, 36, "#7a2e1e", at=at, r=6)], at, "pop")]


def pic_tile(x, y, at):
    return [grp([rect(x - 26, y - 32, 52, 64, "#7fc46a", at=at, r=6)] + libyan_sign(0, x, y - 8, 26, at, "#1f3a1a", 4) + libyan_sign(1, x, y + 18, 22, at, "#1f3a1a", 4), at, "pop")]


def s50():
    """The ledger, panel one (the end of Carthage): burned, razed and banned: Established."""
    tr, tg = T("s50", "Rome burned Carthage"), T("s50", "Established")
    els = ledger("The end of Carthage", .2)
    els += lrow(0, tr, pic_fire, "burned, razed, banned", "Established", tg, GRADE["established"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s51_add():
    t2, g2, t3, g3 = T("s51", "A plough drawn"), T("s51", "Plausible"), T("s51", "And the salt"), T("s51", "Ruled out")
    els = lrow(1, t2, pic_plough, "a plough drawn, as a rite", "Plausible", g2, GRADE["plausible"])
    els += lrow(2, t3, pic_salt, "salted earth", "Ruled out", g3, GRADE["ruled"])
    els += [strike(170, LROWS[2] + 32, 262, LROWS[2] - 32, g3 + .2, RED, 5), strike(296, LROWS[2] + 2, 476, LROWS[2] + 2, g3 + .4, RED, 4)]
    return els


def s52():
    """The ledger, panel two: a sanctuary where infants and young animals were burned and buried under vows: Established; were the children
    sacrificed?: Open question."""
    t1, g1, t2, g2 = T("s52", "A sanctuary"), T("s52", "Established"), T("s52", "Were the children"), T("s52", "Open question")
    els = ledger("The tophet, Kerkouane, Dougga", .2)
    els += lrow(0, t1, pic_stele, "a sanctuary of urns and vows", "Established", g1, GRADE["established"])
    els += lrow(1, t2, pic_urnstele, "were the children sacrificed?", "Open question", g2, GRADE["open"])
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s53_add():
    t3, g3, t4, g4, tm = (T("s53", "Kerkouane, left"), T("s53", "Strong evidence"), T("s53", "The sounds of Dougga's"), T("s53", "Established"),
                          T("s53", "A Mixed record"))
    els = lrow(2, t3, pic_bath, "Kerkouane, left, never rebuilt", "Strong evidence", g3, GRADE["strong"])
    els += lrow(3, t4, pic_tile, "Dougga's letters, read", "Established", g4, GRADE["established"])
    els += [rect(330, 722, 1118, 62, "rgba(18,13,10,.92)", GRADE["mixed"], 3, 31, tm - .2, fx="pop"),
            lab(889, 764, "Rome's story of the end: Mixed record", tm, GRADE["mixed"], 32, st="serif")]
    return els


def s54():
    """What would change our minds: three wanted items in lilac dashes, as named: a Roman-era text with salt in it; the same urns aged blind
    by both teams with one method; a new, careful dig with a fresh urn on a recording grid."""
    t0, tt, tb, tn = T("s54", "What would change"), T("s54", "A text from Roman"), T("s54", "Both teams"), T("s54", "And new urns")
    els = [lab(889, 180, "what would change our minds", t0, GOLD, 30, st="cap")]
    xs = (330, 889, 1450)
    x = xs[0]
    els += [rect(x - 120, 360, 240, 170, "rgba(201,193,238,.05)", LILAC, 2.5, 6, tt, fx="draw", style="inferred"),
            rect(x - 140, 340, 24, 210, "rgba(201,193,238,.08)", LILAC, 2, 8, tt + .2, style="inferred"), rect(x + 116, 340, 24, 210, "rgba(201,193,238,.08)", LILAC, 2, 8, tt + .2, style="inferred")]
    for k in range(3):
        els.append(ln([(x - 90, 400 + 34 * k), (x + 50 - 30 * (k % 2), 400 + 34 * k)], tt + .4, LILAC, 2.5, "inferred", draw=False))
    els += salt_pinch(x + 70, 490, 14, tt + .7, n=8) + [lab(x, 620, "a Roman-era text", tt + .9, LILAC, 28)]
    x = xs[1]
    els += [grp(urn(x, 540, 120, tb, fx=None), tb, "pop"), poly([(x - 150, 330), (x + 150, 330), (x + 150, 366), (x - 150, 366)], "rgba(201,193,238,.12)", LILAC, 2.5, tb + .5, fx="pop", style="inferred"),
            ln([(x + 150, 348), (x + 196, 330)], tb + .6, LILAC, 3, "inferred", draw=False), ln([(x + 150, 348), (x + 192, 376)], tb + .6, LILAC, 3, "inferred", draw=False),
            circ(x - 210, 440, 22, BLUE, at=tb + .3), circ(x + 210, 440, 22, AMBER, at=tb + .3),
            lab(x, 620, "aged blind, one method", tb + .9, LILAC, 28)]
    x = xs[2]
    els += [poly([(x - 150, 380), (x + 150, 380), (x + 120, 540), (x - 120, 540)], "#1a120c", LILAC, 2.5, tn, fx="pop", style="inferred")]
    for k in range(5):
        els.append(ln([(x - 130 + 52 * k + 13, 384), (x - 104 + 52 * k * .8 + 13, 536)], tn + .3, "rgba(201,193,238,.5)", 1.5, "inferred", draw=False))
    els += urn(x, 530, 70, tn + .6) + [lab(x, 620, "new, careful digs", tn + .9, LILAC, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s55():
    """The close, at night: the Byrsa under stars with the Roman forum on top; a cut-away in its flank shows the burned Punic houses glowing
    faintly in their dark layer; the round harbour holds the moon; in the foreground the small stones of the tophet, each with a tiny lamp."""
    th, ts, tw = T("s55", "burned houses"), T("s55", "the small stones"), T("s55", "Weigh it")
    hill = [(140, 568), (210, 540), (300, 470), (380, 400), (450, 340), (520, 306), (600, 294), (700, 292), (790, 300), (850, 326), (910, 384),
            (970, 450), (1030, 520), (1080, 568)]
    els = [poly(hill, "#1c1a22", "rgba(200,214,255,.35)", 1.6, -1, curve=True)]
    els += [rect(470, 282, 380, 14, "#3a3a48", "rgba(220,230,255,.45)", 1, 1, -1)]
    for k in range(8):
        els.append(rect(510 + 40 * k, 232, 12, 50, "#4a4a5a", "rgba(220,230,255,.4)", 1, 1, -1))
    els += [rect(498, 222, 316, 12, "#3a3a48", "rgba(220,230,255,.4)", 1, 1, -1), poly([(498, 222), (656, 192), (814, 222)], "#3a3a48", "rgba(220,230,255,.45)", 1, -1)]
    cut = blob(720, 440, 150, 62, 18, .1, 5)
    els += [poly(cut, "#0e0a08", "rgba(255,190,130,.5)", 2, .3, fx="pop"), rect(590, 452, 260, 22, "#1a0f0a", at=.3)]
    for k, (x0, w) in enumerate(((610, 70), (700, 60), (780, 54))):
        els += [rect(x0, 412, 10, 40, WALLC, at=th), rect(x0 + w, 416, 10, 36, WALLC, at=th)]
    els += [gl(720, 455, 150, th, .5, "fire", pulse=True)]
    r = random.Random(55)
    for k in range(14):
        els.append(circ(r.uniform(600, 840), r.uniform(455, 472), r.uniform(1.6, 3), EMBER, at=round(th + .2 + .05 * k, 2), op=round(r.uniform(.4, .9), 2)))
    els += harbour_far()
    els += [poly(E(1460, 596, 160, 14, 40), "rgba(200,220,255,.18)", at=-1), poly(E(1500, 594, 24, 5, 16), "rgba(240,246,255,.85)", at=-1)]
    for k, (x, y, h) in enumerate(((160, 790, 66), (240, 778, 52), (320, 792, 72), (400, 780, 50), (470, 794, 62), (110, 770, 44), (540, 784, 48))):
        els += stele(x, y, h * .44, h, -1, "#3d3a40", "rgba(220,230,255,.35)", sign=(k % 2 == 0), crescent=False, lines=0, fx=None)
        els += lamp(x + h * .34, y, 14, round(ts + .15 * k, 2), .7)
    els += [gl(889, 500, 900, tw, .12, "lamp")]
    return {"base": "sky", "tod": "night", "ground": HERO_GROUND, "groundc": "#120f12", "sun": False, "moon": [1500, 170, 26],
            "ridges": [{"y": 520, "a": 34, "c": "#1c1a24", "seed": 4}, {"y": 548, "a": 18, "c": "#17151c", "seed": 8}], "cam": CAM, "els": els}


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
    (0, 0, "hook", "s1", [(1, "Under that same", "s2"), (2, "Did Rome really", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "Legend says", "s6"), (2, "A legend", "s7")], {"chapter": "The rise and fall of Carthage"}),
    (1, 1, "collision", "s8", [(0, "After its defeat", "s9"), (1, "Yet excavations", "s10"), (2, "For a fleet", "s11")], {}),
    (1, 2, "cost", "s12", [(1, "Then about fifty", "s13")], {}),
    (1, 3, "tag", "s14", [(1, "Then ten senators", "s15")], {}),
    (2, 0, "world", "s16", [(1, "Polybius saw", "s17")], {"chapter": "Where the salt came from"}),
    (2, 1, "collision", "s18", [(1, "In {1986", "s19"), (2, "And in {2026", "s20")], {}),
    (2, 2, "tag", "s21", [], {}),
    (3, 0, "world", "s22", [(1, "Over their floors", "s23")], {"chapter": "The city under the city"}),
    (3, 1, "collision", "s24", [(1, "Appian says", "s25")], {}),
    (3, 2, "reversal", "s26", [(0, "About a century", "s27")], {}),
    (3, 3, "tag", "s28", [], {}),
    (4, 0, "world", "s29", [(1, "Under its stones", "s30")], {"chapter": "Urns and vows"}),
    (4, 1, "collision", "s31", [(1, "They name", "s32")], {}),
    (4, 2, "reversal", "s33", [(1, "And children and", "s34")], {}),
    (4, 3, "tag", "s35", [], {}),
    (5, 0, "world", "s36", [(1, "In {2010", "s37")], {"chapter": "What the bones say"}),
    (5, 1, "collision", "s38", [(1, "And here's the", "s39")], {}),
    (5, 2, "reversal", "s40", [(1, "Specialists are", "s41")], {}),
    (5, 3, "tag", "s42", [], {}),
    (6, 0, "world", "s43", [(1, "So its streets", "s44")], {"chapter": "Kerkouane and Dougga"}),
    (6, 1, "collision", "s45", [], {}),
    (6, 2, "reversal", "s46", [(1, "In {1842", "s47"), (2, "The language", "s48")], {}),
    (6, 3, "tag", "s49", [], {}),
    (7, 0, "weigh", "s50", [(1, "A plough drawn", "s51"), (2, "A sanctuary", "s52"), (3, "Kerkouane, left", "s53")], {"chapter": "The weighing"}),
    (7, 1, "test", "s54", [], {}),
    (7, 2, "close", "s55", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s3": ("s1", [1, 889, 500], "s3_add"),
    "s11": ("s10", [1.25, 889, 560], "s11_add"),
    "s17": ("s16", [1, 889, 500], "s17_add"),
    "s19": ("s18", [1, 889, 500], "s19_add"),
    "s20": ("s18", [1.2, 741, 500], "s20_add"),
    "s23": ("s22", [1, 889, 500], "s23_add"),
    "s24": ("s22", [1, 889, 500], "s24_add"),
    "s32": ("s31", [1, 889, 500], "s32_add"),
    "s35": ("s30", [1, 889, 500], "s35_add"),
    "s38": ("s37", [1, 889, 500], "s38_add"),
    "s47": ("s46", [1, 889, 500], "s47_add"),
    "s51": ("s50", [1, 889, 500], "s51_add"),
    "s53": ("s52", [1, 889, 500], "s53_add"),
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
        sb = script["chapters"][c]["beats"][b]
        assert sb["role"] == role, (c, b, role, sb["role"])
        assert kw.get("chapter") in (None, script["chapters"][c]["title"]), (c, kw.get("chapter"), script["chapters"][c]["title"])
        lines = list(sb["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-carthage", "code": "LF.35", "series": script["series"], "title": script["title"], "case": "carthage",
          "verdict": "mixed", "claim": "Did Rome sow Carthage with salt, and were the children of the tophet sacrificed?", "mood": "mystery",
          "hook_text": "Did Rome *salt* Carthage?", "beats": beats, "shots": shots,
          "sources": "Ridley 1986 (doi:10.1086/366973) · Warmington 1988 (doi:10.1086/367123) · Saladin 2026 (doi:10.1086/739931) · "
                     "Stevens 1988 (doi:10.1086/367078) · Schwartz et al. 2010 (doi:10.1371/journal.pone.0009177) · "
                     "Smith et al. 2011 (doi:10.1017/S0003598X00068368) · Xella et al. 2013 (doi:10.1017/S0003598X00049966) · "
                     "Schwartz et al. 2017 (doi:10.15184/aqy.2016.270) · Cerezo-Roman et al. 2024 (doi:10.15184/aqy.2024.85) · "
                     "Ringbauer et al. 2025 (doi:10.1038/s41586-025-08913-3) · Appian, Punica 127-136 · Digest 7.4.21",
          "post": "Did Rome really plough Carthage under and sow it with salt? Were the children of the tophet sacrificed? The last siege, "
                  "the salt traced from a 1930 history book back to the Middle Ages, the burned houses sealed under the Roman forum, the vows "
                  "on the tophet's stones, two bone studies with opposite answers, and the Carthage Rome's story hid, weighed.",
          "hashtags": ["#Carthage", "#Tunisia", "#AncientRome", "#Archaeology", "#CarthageAndBefore", "#WeighItYourself"],
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
