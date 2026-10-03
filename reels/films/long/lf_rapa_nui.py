"""LF.27 · Fallen Worlds · Rapa Nui: Stone Giants and the Last Tree (16:9 long film, one wall).

The script is films/long/lf-rapa-nui/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s45; s4t, the title, is the intro card over the
panel of s4), drawn while it is said: the heads on the slope of Rano Raraku and their buried bodies, the speck in the Pacific, the
famous story in dotted lines; the landing at Anakena, a crater lake's diary of pollen, the giant palms and their stumps, fire, rats
and a model of rats; Paro to scale, the sledge of 1998, the old roads and the statues lying beside them, the walking replica of
2012, the dished road and the fall-off from the quarry; the bestseller's crash curve, charcoal dates and platforms built after 1722,
rock gardens seen from space and the 3,000 they could feed, the critics; fifteen ancestors and their genomes, beads through a
bottleneck, a voyage to the Americas and home; the Dutch ships of 1722, the statues falling, the raids of 1862, smallpox, 110 left,
the sheep ranch; rongorongo, its turning rows, the quill of 1770, four tablets dated in Rome, a brick and a log from southern
Africa, the inventions of writing; the ledgers, the tests and the slope at night. Drawings are schematic and true to the numbers
said: solid = on the record, dashed = inferred or missing, dotted = claimed. People and the dead are drawn with care: no bodies,
lights that dim.

Facts: the script's facts_added (Moreno-Mayar et al. 2024; Davis et al. 2024; Ferrara et al. 2024; Lastilla et al. 2022; Lipo & Hunt
2025; Lipo, Hunt & Rapu Haoa 2013; Hunt & Lipo 2025; Mieth & Bork 2010; Hunt 2007; Hunt & Lipo 2006; DiNapoli et al. 2019, 2020,
2021; Stevenson et al. 2015; Fehren-Schmitz et al. 2017; Flenley & King 1984; Dransfield et al. 1984; Diamond 2005; Van Tilburg
1994; Fischer 2005; Maude 1981; Metraux 1940; Routledge 1919).

Engine workaround (as in lf_roswell.py and lf_antikythera.py): the wall adds elements to a panel on its first visit, at a beat start
or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a
tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's
additions as a panel item (kit.js builds them on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-rapa-nui/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-rapa-nui/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-rapa-nui RC_FILMS_EPS=/tmp/claude-0/sbx_lf-rapa-nui/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-rapa-nui/boards python3 films.py long.lf_rapa_nui
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-rapa-nui", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN, INK = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN, I.INK
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
FLAT = "#15110d"                                               # flat panel background (for veils)
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "plausible": "#f2c98e", "open": "#c9c1ee", "mixed": "#e8b87a",
         "awaiting": "#9fd0ff", "ruled": "#ff8a7a"}
# the island
TUFF, TUFF_L, TUFF_D, TUFF_E = "#8e8170", "#c8b598", "#4c443b", "rgba(255,236,206,.35)"   # Rano Raraku tuff: mid, lit, shadow, rim
SCORIA = "#9a4a34"                                             # the red topknots
GRASS, GRASS_D, GRASS_L = "#4e5a33", "#2f3a22", "#76804a"
SEA, SEA_D = "#1d4a5e", "#0f2a38"
PALM, PALM_D, PALM_L, TRUNK = "#3f6a3a", "#22401f", "#6f9a5a", "#6a5e50"
SOIL, SOIL_D = "#5a4330", "#3a2a1e"
CHAR = "#1a1512"
RAT = "#8a7a68"
WOOD, WOOD_D, WOOD_L = "#5a3e28", "#3a2618", "#8a6440"
SAIL = "#efe3c8"
SAND_E = "#c9ad85"
SIL = "#120e0b"


# ================================================================== narration: the script's own lines, and when each word is said
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")     # a sentence opens with [act:] (and its tags)
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma
SAY, CLK, DUR = {}, {}, {}           # shot key -> its narration, its word clock, its estimated length (set in film())


def END(sid, back=.5):
    return round(max(.5, DUR[sid] - back), 2)


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # DNA: letter by letter
    w = a.lower()
    if not w:
        return 2 if re.search(r"\d", a) else 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def _spoken(seg):
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", re.sub(r"\[[^\]]*\]", " ", seg))
    return re.sub(r"@\w+!?", "", s.replace("^", "").replace("*", "")).split()


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def _clock(text):
    """[(word, seconds from the start of `text`)]: lines joined by newlines, sentences opened by [act:]."""
    out, t = [], 0.0
    for li, ln_ in enumerate(text.split("\n")):
        if li:
            t += LGAP
        cuts = [m.start() for m in SENT.finditer(ln_)]
        cuts = sorted(set([0] + cuts + [len(ln_)]))
        for a, z in zip(cuts, cuts[1:]):
            seg = ln_[a:z]
            if not _spoken(seg):
                continue
            p = re.search(r"\[p:([\d.]+)\]", seg)
            r = RATE * (float(p.group(1)) if p else 1.0)
            g = re.search(r"\[gap:([\d.]+)\]", seg)
            if g:
                t += float(g.group(1))
            for w in _spoken(seg):
                out.append((_norm(w), round(t, 2)))
                t += _syl(w) / r
                if w[-1] in ",:;":
                    t += CGAP
            t += SGAP
    return out, round(t, 2)


def T(sid, phrase, k=1, lead=.3):
    """Seconds after the shot's step starts at which `phrase` is said (its k-th occurrence)."""
    ws = CLK[sid]
    ps = [_norm(x) for x in phrase.split()]
    hits = [i for i in range(len(ws)) if [w for w, _ in ws[i:i + len(ps)]] == ps]
    assert len(hits) >= k, (sid, phrase, " ".join(w for w, _ in ws))
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


# ================================================================== drawing helpers
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


def arr(p, at, c=AMBER, w=3, style="known", dur=.8, curve=False, **kw):
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


def grp(els, at, fx="pop", tr=None, clip=None, **kw):
    """A group that builds in as one piece (its children have no build-ins of their own); tr = an SVG transform; clip = [x, y, w, h, r]."""
    if tr:                                   # the build-in sets the outer group's transform: the turn lives on an inner group
        els = [{"k": "group", "tr": tr, "els": els}]
    e = {"k": "group", "els": static(els), "in": round(at, 2)}
    if clip:
        e["clip"] = [round(v, 1) for v in clip]
    if fx:
        e["fx"] = fx
    e.update(kw)
    return e


def static(els):
    """The same elements already in place when their group arrives (no build-in of their own)."""
    out = []
    for e in els:
        e = dict(e)
        e["in"] = -1
        e.pop("fx", None)
        if e.get("els"):
            e["els"] = static(e["els"])
        out.append(e)
    return out


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words (scales with the picture, like a plaque)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.92)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", scl=True, fx="pop")]


def tag(x, y, t, at, c=AMBER, size=26, style="known", a="middle"):
    """A small rounded tag with a few words (dashed for an inference, dotted for a claim)."""
    w = len(t) * size * .55 + 30
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - size * .95, w, size * 1.55, "rgba(18,13,10,.85)", c, 2, size * .7, at, fx="pop", style=style),
            lab(x0 + w / 2, y + size * .2, t, at + .1, c, size, halo=False)]


def tick(x, y, at, c=GREEN, s=1.0, w=6):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": w, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cross(x, y, at, c=RED, s=1.0, w=6):
    return [ln([(x - 14 * s, y - 14 * s), (x + 14 * s, y + 14 * s)], at, c, w, dur=.25), ln([(x + 14 * s, y - 14 * s), (x - 14 * s, y + 14 * s)], at + .15, c, w, dur=.25)]


def qmark(x, y, at, size=90, c=LILAC, halo=True):
    out = [gl(x, y - size * .3, size * 1.1, at, .5)] if halo else []
    return out + [lab(x, y, "?", at, c, size, st="big", fx="pop", dur=.8)]


def axis(x0, x1, y, ticks, at, t=None, below=True):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def veil(x, y, w, h, at, fill, op=1.0, dur=.5, r=0):
    """A sheet of the background's own colour laid over something: what was there fades away."""
    e = rect(x, y, w, h, fill, r=r, at=at, op=op)
    e["dur"] = dur
    return e


def ppl(x, y, h, at, c="#9a9288", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def bar(x0, x1, y, h, at, c=AMBER, dur=1.0, op=None):
    """A bar growing left to right (a thick line that draws itself)."""
    return ln([(x0, y), (x1, y)], at, c, h, dur=dur, op=op)


def vbar(x, y0, y1, w, at, c=AMBER, dur=.6, op=None):
    """A bar growing bottom to top (y0 the base, y1 the top)."""
    return ln([(x, y0), (x, y1)], at, c, w, dur=dur, op=op)


def balance(cx, py, L, ang, base_y, at, left=None, right=None, drop_=170, pan=190, c=BONE):
    a = math.radians(ang)
    ends = [(cx - L / 2 * math.cos(a), py - L / 2 * math.sin(a)), (cx + L / 2 * math.cos(a), py + L / 2 * math.sin(a))]
    out = [rect(cx - 80, base_y - 10, 160, 14, "#5a4836", "#8c7152", 1.5, 4, at), ln([(cx, base_y - 8), (cx, py)], at, "#8c7152", 8, draw=False),
           ln(ends, at, c, 6, draw=False), dot(cx, py, 10, GOLD, round(at, 2), None)]
    for (ex, ey), stuff in zip(ends, (left, right)):
        fy = ey + drop_
        out += [ln([(ex, ey), (ex - pan / 2 + 10, fy)], at, MUTED, 1.6, draw=False), ln([(ex, ey), (ex + pan / 2 - 10, fy)], at, MUTED, 1.6, draw=False),
                poly([(ex - pan / 2, fy), (ex + pan / 2, fy), (ex + pan / 2 - 18, fy + 16), (ex - pan / 2 + 18, fy + 16)], "#6b5a48", "#cbb79a", 1.5, at)]
        if stuff:
            out += stuff(round(ex, 1), round(fy, 1), at)
    return out


def rot_pts(pts, cx, cy, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def mirror(pts, cx):
    return [(2 * cx - x, y) for x, y in pts]


# ================================================================== the moai
# Front view. The head (top to chin) is HEAD_H of the statue's height and 2*HEAD_W wide; f runs across the head (-1..1 at the brow),
# g down it (0 at the top, 1 at the chin). Lit from the left by default (light=-1): the right side planes fall in shadow.
HEAD_H, HEAD_W = .425, .132
MO_HEAD = [(0, 0), (.82, 0), (.95, .02), (1.0, .08), (1.0, .17), (1.07, .21), (1.09, .32), (1.08, .57), (1.02, .65), (.92, .74), (.76, .86),
           (.56, .95), (.40, .985), (.36, 1.0)]
MO_BODY = [(.088, -.565), (.120, -.537), (.172, -.515), (.188, -.495), (.192, -.45), (.188, -.20), (.183, 0)]   # x, y in statue units


def _front_outline(cx, by, h):
    hx = lambda f: cx + f * HEAD_W * h
    hy = lambda g: by + (-1.0 + g * HEAD_H) * h
    half = [(hx(f), hy(g)) for f, g in MO_HEAD] + [(cx + x * h, by + y * h) for x, y in MO_BODY]
    return half + mirror(half[::-1], cx)[:-1]


def moai(cx, by, h, at, fx=None, op=None, eyes=False, pukao=False, light=-1, tone=TUFF, lit=TUFF_L, shade=TUFF_D, rim=TUFF_E, body=True,
         lichen=0, seed=1, style="known"):
    """A moai seen from the front, base on by, h tall (the whole statue): long head, heavy brow over deep sockets, long nose flared at
    its base, pouting lips, a jutting chin, long ears; arms down the sides and long fingers over the belly. light=-1: lit from the left.
    eyes: the white coral eyes of a platform statue. pukao: the red topknot. A claimed or inferred statue is an outline only."""
    if style != "known":
        return [poly(_front_outline(cx, by, h), "rgba(201,193,238,.06)" if style == "claimed" else "rgba(245,236,220,.05)",
                     LILAC if style == "claimed" else BONE, 2.6, at, fx=fx, op=op, style=style)]
    s = -light                               # +1: the shadow is on the right
    hx = lambda f: cx + s * f * HEAD_W * h
    hy = lambda g: by + (-1.0 + g * HEAD_H) * h
    X = lambda u: cx + s * u * h
    Y = lambda v: by + v * h
    o = (lambda k: k if op is None else op * k)
    P = lambda pts: [(hx(f), hy(g)) for f, g in pts]
    els = [poly(_front_outline(cx, by, h), tone, rim, 1.4, at, fx=fx, op=op)]
    # the side planes in shadow: the right cheek and jaw down to the chin, and the right side of the body
    els.append(poly(P([(.80, .17), (1.0, .17), (1.07, .21), (1.09, .32), (1.08, .57), (1.02, .65), (.92, .74), (.76, .86), (.56, .95), (.40, .985),
                       (.36, 1.0), (.30, .93), (.52, .80), (.66, .60), (.74, .36)]), shade, at=at, fx=fx, op=o(.62)))
    els.append(poly([(X(.13), Y(-.53)), (X(.172), Y(-.515)), (X(.188), Y(-.495)), (X(.192), Y(-.45)), (X(.188), Y(-.20)), (X(.183), Y(0)), (X(.10), Y(0)),
                     (X(.11), Y(-.30))], shade, at=at, fx=fx, op=o(.55)))
    # the lit forehead plane and the brow's edge
    els.append(poly(P([(-.92, .02), (.70, .02), (.80, .15), (-.98, .15)]), lit, at=at, fx=fx, op=o(.28)))
    els.append(ln(P([(-1.0, .17), (-.5, .165), (0, .165), (.5, .165), (1.0, .17)]), at, lit, max(1.5, .006 * h), draw=False, op=o(.9)))
    # the deep eye sockets under the brow
    for sg in (-1, 1):
        els.append(poly(P([(sg * .12, .172), (sg * .92, .172), (sg * .85, .236), (sg * .56, .272), (sg * .24, .262), (sg * .14, .232)]),
                        "#231d18", at=at, fx=fx, op=o(.86)))
        if eyes:
            els.append(poly([(hx(sg * .54) + d * HEAD_W * h * .26, hy(.235) + e * HEAD_H * h * .035) for d, e in
                             [(-1, 0), (-.7, -.8), (0, -1), (.7, -.8), (1, 0), (.7, .8), (0, 1), (-.7, .8)]], "#f2eee4", at=at, fx=fx, op=op, curve=True))
            els.append(circ(hx(sg * .50), hy(.235), .03 * HEAD_W * h * 4, "#1a1410", at=at, fx=fx, op=op))
    # the nose: a long wedge from the brow, its base flared into nostril lobes; the shadow side darker, the underside dark
    els.append(poly(P([(-.13, .17), (.13, .17), (.22, .48), (.32, .52), (.30, .575), (.12, .585), (-.12, .585), (-.30, .575), (-.32, .52), (-.22, .48)]),
                    lit, at=at, fx=fx, op=o(.75)))
    els.append(poly(P([(.0, .17), (.13, .17), (.22, .48), (.32, .52), (.30, .575), (.12, .585), (.02, .585)]), shade, at=at, fx=fx, op=o(.7)))
    for sg in (-1, 1):
        els.append(ln(P([(sg * .16, .47), (sg * .27, .50), (sg * .28, .55), (sg * .17, .565)]), at, "#3a3129", max(1.2, .004 * h), draw=False, op=o(.8), curve=True))
    els.append(poly(P([(-.24, .582), (.24, .582), (.18, .60), (-.18, .60)]), "#2a231d", at=at, fx=fx, op=o(.8)))
    # the mouth: a pouting upper lip, the line between the lips turned down a little at the corners, a short lower lip, the chin
    els.append(poly(P([(-.40, .655), (-.20, .628), (0, .622), (.20, .628), (.40, .655), (.30, .662), (-.30, .662)]), lit, at=at, fx=fx, op=o(.6)))
    els.append(ln(P([(-.44, .672), (-.30, .662), (0, .660), (.30, .662), (.44, .672)]), at, "#231d18", max(1.6, .006 * h), draw=False, op=o(.95), curve=True))
    els.append(poly(P([(-.26, .675), (.26, .675), (.20, .71), (-.20, .71)]), tone, at=at, fx=fx, op=op))
    els.append(ln(P([(-.22, .722), (0, .728), (.22, .722)]), at, "#2a231d", max(1.2, .004 * h), draw=False, op=o(.7), curve=True))
    els.append(poly(P([(-.34, .80), (.30, .80), (.24, .92), (-.26, .92)]), lit, at=at, fx=fx, op=o(.22)))
    # the long ears
    for sg in (-1, 1):
        els.append(poly(P([(sg * .99, .21), (sg * 1.07, .22), (sg * 1.08, .56), (sg * 1.02, .62), (sg * .98, .56), (sg * .97, .26)]),
                        lit if sg < 0 else shade, at=at, fx=fx, op=o(.55)))
        els.append(ln(P([(sg * 1.02, .27), (sg * 1.03, .52)]), at, "#2a231d", max(1.1, .0035 * h), draw=False, op=o(.6)))
    if body:
        # arms along the sides, forearms bending in, long fingers over the belly; the hami belt below
        for sg in (-1, 1):
            Xs = lambda u: cx + sg * u * h
            els.append(ln([(Xs(.170), Y(-.50)), (Xs(.168), Y(-.30)), (Xs(.160), Y(-.215)), (Xs(.120), Y(-.195)), (Xs(.040), Y(-.190))],
                          at, "#3a332b", max(2, .009 * h), draw=False, op=op, curve=True))
            for k in range(4):
                yy = -.205 + k * .011
                els.append(ln([(Xs(.105), Y(yy)), (Xs(.03), Y(yy + .004))], at, "#3a332b", max(1.1, .0035 * h), draw=False, op=o(.8)))
        els.append(ln([(X(-.11), Y(-.12)), (X(0), Y(-.105)), (X(.11), Y(-.12))], at, "#3a332b", max(1.4, .005 * h), draw=False, op=o(.8), curve=True))
    if lichen:
        rnd = random.Random(seed)
        for _ in range(lichen):
            f, g = rnd.uniform(-.8, .6), rnd.uniform(.0, .12)
            els.append(circ(hx(f), hy(g), rnd.uniform(.004, .009) * h, rnd.choice(["#b8903c", "#a8823a", "#c8b070"]), at=at, fx=fx, op=o(.45)))
    if pukao:
        els.append(poly([(hx(-.86), hy(.0)), (hx(.86), hy(.0)), (hx(.96), hy(-.17)), (hx(.76), hy(-.24)), (hx(-.76), hy(-.24)), (hx(-.96), hy(-.17))],
                        SCORIA, "rgba(255,200,170,.35)", 1.2, at, fx=fx, op=op))
        els.append(poly([(hx(-.6), hy(-.24)), (hx(.6), hy(-.24)), (hx(.5), hy(-.3)), (hx(-.5), hy(-.3))], "#7a3626", at=at, fx=fx, op=op))
    return els


# Side view (facing right), units of the statue's height, x forward from the back line, y up from the base.
MO_SIDE = [(-.10, 0), (-.106, -.30), (-.100, -.55), (-.094, -.62), (-.092, -.80), (-.090, -.95), (-.078, -1.0), (.060, -1.0), (.084, -.985),
           (.104, -.93), (.136, -.894), (.146, -.880), (.104, -.862), (.112, -.84), (.150, -.78), (.198, -.722), (.206, -.708), (.186, -.700),
           (.148, -.698), (.150, -.684), (.170, -.674), (.150, -.662), (.162, -.650), (.140, -.636), (.140, -.618), (.162, -.600), (.170, -.584),
           (.150, -.570), (.090, -.560), (.066, -.545), (.066, -.52), (.096, -.47), (.118, -.36), (.124, -.22), (.118, -.10), (.110, 0)]


def moai_side(x, by, h, at, fx=None, op=None, lean=0.0, face=1, base=None, sockets=True, tone=TUFF, lit=TUFF_L, shade=TUFF_D, rim=TUFF_E,
              style="known", pivot=None):
    """A moai in profile facing right (face=1) or left, base on by at x (the middle of its base), h tall. lean: degrees forward.
    base: 'D' for the wide forward base of a road statue. sockets: the eye socket under the brow."""
    pts = list(MO_SIDE)
    if base == "D":
        pts = [(-.13, 0), (-.122, -.12)] + pts[1:-2] + [(.128, -.12), (.14, 0)]
    P = [(x + face * u * h, by + v * h) for u, v in pts]
    pv = pivot or (x + face * (.104 if base != "D" else .14) * h, by)
    if lean:
        P = rot_pts(P, pv[0], pv[1], face * lean)
    if style != "known":
        return [poly(P, "rgba(201,193,238,.06)" if style == "claimed" else "rgba(245,236,220,.05)", LILAC if style == "claimed" else BONE, 2.6, at,
                     fx=fx, op=op, style=style)]
    els = [poly(P, tone, rim, 1.4, at, fx=fx, op=op)]

    def Q(u, v):
        q = (x + face * u * h, by + v * h)
        return rot_pts([q], pv[0], pv[1], face * lean)[0] if lean else q
    # the back half in shadow
    els.append(poly([Q(-.10, 0), Q(-.105, -.30), Q(-.098, -.55), Q(-.090, -.80), Q(-.086, -1.0), Q(-.02, -1.0), Q(-.035, -.55), Q(-.04, 0)],
                    shade, at=at, fx=fx, op=.5 if op is None else op * .5))
    # the ear, the brow's lit top, the socket, the arm and hand
    els.append(poly([Q(-.012, -.86), Q(.012, -.86), Q(.016, -.70), Q(-.006, -.69), Q(-.016, -.72)], lit, at=at, fx=fx, op=.55 if op is None else op * .55))
    els.append(ln([Q(.06, -1.0), Q(.09, -.93), Q(.115, -.885)], at, lit, max(1.5, .008 * h), draw=False, op=op))
    if sockets:
        els.append(poly([Q(.140, -.878), Q(.104, -.862), Q(.110, -.842), Q(.080, -.848), Q(.084, -.874)], "#231d18", at=at, fx=fx, op=op))
    els.append(poly([Q(.136, -.890), Q(.146, -.880), Q(.104, -.866), Q(.10, -.88)], lit, at=at, fx=fx, op=.8 if op is None else op * .8))
    els.append(ln([Q(.150, -.663), Q(.124, -.660)], at, "#231d18", max(1.5, .006 * h), draw=False, op=op))
    els.append(ln([Q(.170, -.703), Q(.150, -.700)], at, "#231d18", max(1.5, .006 * h), draw=False, op=op))
    els.append(ln([Q(.150, -.570), Q(.100, -.562), Q(.070, -.548)], at, "#2a231d", max(1.5, .005 * h), draw=False, op=op))
    els.append(ln([Q(-.03, -.50), Q(-.025, -.30), Q(-.01, -.21), Q(.06, -.19), Q(.10, -.19)], at, "#3a332b", max(2, .01 * h), draw=False, op=op, curve=True))
    return els


def mound(cx, gy, w, depth, at, c=GRASS, rim=GRASS_L, seed=1, op=None, tufts=5):
    """A low hump of grass laid over the base of a buried statue: its top edge rises a little round the statue, no hard outline."""
    rnd = random.Random(seed)
    top = [(cx - w, gy + 14), (cx - w * .55, gy + 2), (cx - w * .2, gy - 4), (cx + w * .2, gy - 4), (cx + w * .55, gy + 2), (cx + w, gy + 14)]
    els = [poly(top + [(cx + w, gy + depth), (cx - w, gy + depth)], c, at=at, op=op, curve=False)]
    els.append(ln(top, at, rim, 1.6, draw=False, op=.45 if op is None else op * .45, curve=True))
    for k in range(tufts):
        tx = cx + rnd.uniform(-w * .8, w * .8)
        ty = gy + 4 + rnd.uniform(0, 10)
        els.append(ln([(tx - 6, ty + 2), (tx - 2, ty - 9), (tx, ty + 2), (tx + 4, ty - 11), (tx + 7, ty + 2)], at, rim, 1.5, draw=False,
                      op=.75 if op is None else op * .75))
    return els


def buried(cx, gy, h, vis, at, light=-1, eyes=False, tilt=0.0, seed=1, op=None, fx=None, lichen=6, c=GRASS):
    """A statue on the slope, buried to the chest: h = its whole height, vis = the part that shows above the ground at gy (0..1).
    A contact shadow, then a hump of grass laid over the rest."""
    by = gy + (1 - vis) * h
    els = moai(cx, by, h, at, fx=fx, op=op, eyes=eyes, light=light, body=True, lichen=lichen, seed=seed)
    if tilt:
        els = [grp(els, at, fx or None, tr="rotate(%s %s %s)" % (tilt, round(cx, 1), round(gy, 1)))]
    w = .30 * h
    shadow = [poly(E(cx, gy + 4, .17 * h, .012 * h + 4, 20), "#1a2012", at=at, op=.35)]
    return els + shadow + mound(cx, gy, w, (1 - vis) * h + 30, at, c, rim=GRASS_L if c == GRASS else "#344028", seed=seed)


# ================================================================== the island and the ocean
RN = [(-109.224, -27.104), (-109.232, -27.115), (-109.250, -27.121), (-109.268, -27.124), (-109.280, -27.128), (-109.296, -27.137),
      (-109.318, -27.150), (-109.340, -27.160), (-109.362, -27.168), (-109.385, -27.174), (-109.405, -27.178), (-109.420, -27.188),
      (-109.433, -27.199), (-109.447, -27.197), (-109.452, -27.187), (-109.447, -27.172), (-109.437, -27.160), (-109.432, -27.148),
      (-109.428, -27.135), (-109.424, -27.118), (-109.418, -27.100), (-109.408, -27.084), (-109.394, -27.071), (-109.378, -27.063),
      (-109.360, -27.062), (-109.343, -27.067), (-109.325, -27.071), (-109.307, -27.075), (-109.290, -27.083), (-109.272, -27.088),
      (-109.255, -27.088), (-109.238, -27.093)]
RN_PLACES = {"Rano Raraku": (-109.289, -27.121), "Anakena": (-109.323, -27.073), "Hanga Roa": (-109.428, -27.150), "Rano Kau": (-109.434, -27.186),
             "Terevaka": (-109.380, -27.085), "Poike": (-109.245, -27.100), "Tongariki": (-109.277, -27.126), "Vinapu": (-109.400, -27.177)}
# platform sites round the coast (schematic: the coastline carried a ring of image platforms)
RN_AHU = [(-109.277, -27.126), (-109.300, -27.140), (-109.330, -27.156), (-109.355, -27.166), (-109.386, -27.172), (-109.412, -27.181),
          (-109.430, -27.152), (-109.427, -27.137), (-109.421, -27.112), (-109.409, -27.088), (-109.365, -27.064), (-109.324, -27.073),
          (-109.300, -27.079), (-109.262, -27.090), (-109.240, -27.112)]


def island(v, at=-1, fill="#56653a", c="#c9d29a", w=2, op=None, volcanoes=True, shade=True):
    """Rapa Nui in a View: the coast (schematic), its three volcanoes, a soft shore line."""
    P = [v.p(lo, la) for lo, la in RN]
    els = [poly(P, fill, c, w, at, op=op, curve=False)]
    if shade:
        cx, cy = v.p(-109.33, -27.12)
        els.append(gl(cx, cy, v.km(8), at, .18 if op is None else .18 * op, "lamp"))
    if volcanoes:
        for nm, rr in (("Rano Kau", 0.8), ("Rano Raraku", 0.42), ("Terevaka", 0.6), ("Poike", 0.55)):
            x, y = v.p(*RN_PLACES[nm])
            r = v.km(rr)
            els.append(circ(x, y, r, "rgba(20,30,15,.35)" if nm != "Rano Kau" else "rgba(40,80,90,.55)", "rgba(220,230,170,.5)", 1.5, at, op=op))
    return els


PAC = View(-150.0, -64.0, -48.0, -6.0, (90, 120, 1600, 680))


def pacific_land(v, at=-1, landc="#3a3024", op=None):
    e = {"k": "map", "land": v.land(), "landc": landc, "in": at}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


# ================================================================== plants, animals, boats, people
def palm(x, y, h, at, fx=None, op=None, lean=0.0, seed=1, c=PALM, cd=PALM_D, cl=PALM_L, trunk=TRUNK, fronds=13):
    """A giant palm (the Rapa Nui palm, a cousin of the Chilean wine palm): a thick grey trunk swelling a little at its foot, leaf-scar
    rings, a round crown of long arching fronds. Base on (x, y), h tall to the crown."""
    rnd = random.Random(seed)
    tw0, tw1 = h * .11, h * .085
    top = (x + math.sin(math.radians(lean)) * h, y - h)
    trunk_p = [(x - tw0 / 2, y), (x - tw0 * .44, y - h * .3), (top[0] - tw1 / 2, top[1]), (top[0] + tw1 / 2, top[1]), (x + tw0 * .44, y - h * .3), (x + tw0 / 2, y)]
    els = [poly(trunk_p, trunk, "rgba(255,236,206,.18)", 1, at, fx=fx, op=op)]
    els.append(poly([(x + tw0 * .05, y), (x + tw0 * .1, y - h * .3), (top[0] + tw1 * .1, top[1]), (top[0] + tw1 / 2, top[1]), (x + tw0 * .44, y - h * .3),
                     (x + tw0 / 2, y)], "#3e3830", at=at, fx=fx, op=.6 if op is None else op * .6))
    for k in range(1, 9):
        t = k / 9
        cxk = x + (top[0] - x) * t
        wk = tw0 + (tw1 - tw0) * t
        els.append(ln([(cxk - wk / 2, y - h * t), (cxk, y - h * t + 3), (cxk + wk / 2, y - h * t)], at, "#4a4238", 1.4, draw=False,
                      op=.7 if op is None else op * .7, curve=True))
    cx, cy = top
    for k in range(fronds):
        ang = -180 + 180 * (k + .5) / fronds + rnd.uniform(-6, 6)
        a = math.radians(ang)
        L = h * rnd.uniform(.42, .55)
        droop = h * .22 * abs(math.cos(a))
        tip = (cx + math.cos(a) * L, cy + math.sin(a) * L * .55 + droop)
        mid = (cx + math.cos(a) * L * .55, cy + math.sin(a) * L * .55 * .9 - h * .04)
        nx, ny = -math.sin(a), math.cos(a)
        wd = h * .05
        blade = [(cx, cy), (mid[0] + nx * wd, mid[1] + ny * wd * .5), (tip[0], tip[1]), (mid[0] - nx * wd, mid[1] - ny * wd * .5)]
        col = cd if k % 3 == 0 else c
        els.append(poly(blade, col, at=at, fx=fx, op=op, curve=True))
        els.append(ln([(cx, cy), mid, tip], at, cl, 1.3, draw=False, op=.7 if op is None else op * .7, curve=True))
    els.append(circ(cx, cy + 2, tw1 * .55, cd, at=at, fx=fx, op=op))
    return els


def stump(x, y, w, at, fx=None, op=None, burnt=False):
    h = w * .7
    els = [poly([(x - w / 2, y), (x - w * .42, y - h), (x - w * .1, y - h * 1.12), (x + w * .2, y - h * .92), (x + w * .44, y - h * 1.05), (x + w / 2, y)],
                "#2a221c" if burnt else "#5a5046", "rgba(255,236,206,.25)", 1, at, fx=fx, op=op)]
    if burnt:
        els.append(gl(x, y - h * .5, w * 1.2, at, .25 if op is None else .25 * op, "fire"))
    return els


def nut(x, y, r, at, fx="pop", op=None, gnawed=False, charred=False, ang=0, seed=1):
    """A palm nut (the hard round shell, its three pores near one end); gnawed: a ragged hole in its side; charred: black."""
    fill = "#1d1916" if charred else "#7a5636"
    rim = "rgba(255,180,120,.35)" if charred else "rgba(255,226,180,.45)"
    els = [poly(E(x, y, r, r * .9, 24), fill, rim, 1.2, at, fx=fx, op=op)]
    if not charred:
        els.append(poly(E(x - r * .25, y - r * .25, r * .45, r * .32, 14), "#9a744a", at=at, fx=fx, op=.55 if op is None else op * .55))
        a0 = math.radians(ang + 90)
        px, py = x + math.cos(a0) * r * .55, y - math.sin(a0) * r * .5
        for k in range(3):
            a = math.radians(ang + 120 * k)
            els.append(circ(px + math.cos(a) * r * .14, py - math.sin(a) * r * .12, max(1.5, r * .07), "#3a2616", at=at, fx=fx, op=op))
    if gnawed:
        rnd = random.Random(seed)
        a = math.radians(ang - 40)
        hx, hy = x + math.cos(a) * r * .32, y - math.sin(a) * r * .28
        hole = [(hx + math.cos(math.radians(t)) * r * rnd.uniform(.34, .46), hy + math.sin(math.radians(t)) * r * rnd.uniform(.28, .40))
                for t in range(0, 360, 24)]
        els.append(poly(hole, "#1e140c", "#d8b888", 1.4, at, fx=fx, op=op))
    return els


def rat(x, y, s, at, face=1, fx="pop", op=None, c=RAT):
    """A Polynesian rat in profile facing right (face=1): a rounded back, pointed snout, small ear, eye, whiskers, long tail;
    (x, y) its feet, s its body length (nose to rump)."""
    f = face
    X = lambda u: x + f * u * s
    Y = lambda v: y + v * s
    body = [(X(-.42), Y(-.02)), (X(-.50), Y(-.20)), (X(-.40), Y(-.36)), (X(-.15), Y(-.44)), (X(.10), Y(-.42)), (X(.28), Y(-.33)), (X(.42), Y(-.24)),
            (X(.56), Y(-.14)), (X(.60), Y(-.10)), (X(.52), Y(-.07)), (X(.30), Y(-.05)), (X(.10), Y(-.01)), (X(-.20), Y(0))]
    els = [poly(body, c, "rgba(255,236,206,.4)", 1.2, at, fx=fx, op=op, curve=True),
           poly([(X(-.35), Y(-.30)), (X(-.12), Y(-.40)), (X(.10), Y(-.38)), (X(-.10), Y(-.30))], "#a49280", at=at, fx=fx, op=.5 if op is None else op * .5, curve=True),
           poly(E(X(.22), Y(-.38), .055 * s, .07 * s, 14), "#6e5e50", "rgba(255,236,206,.35)", 1, at, fx=fx, op=op),
           poly(E(X(.22), Y(-.38), .03 * s, .042 * s, 12), "#c89a8a", at=at, fx=fx, op=op),
           circ(X(.36), Y(-.25), .02 * s, "#0e0a08", at=at, fx=fx, op=op),
           circ(X(.595), Y(-.105), .016 * s, "#4a3028", at=at, fx=fx, op=op),
           ln([(X(-.44), Y(-.08)), (X(-.70), Y(-.03)), (X(-.98), Y(-.08)), (X(-1.18), Y(-.22))], at, "#9a8474", max(1.5, .022 * s), draw=False, op=op, curve=True)]
    for k in (-1, 0, 1):
        els.append(ln([(X(.55), Y(-.11)), (X(.74), Y(-.11 + .04 * k))], at, "rgba(255,236,206,.55)", 1, draw=False, op=op))
    for u in (.18, -.22):
        els.append(ln([(X(u), Y(-.04)), (X(u + .04), Y(.0))], at, "#4a3a30", max(2, .02 * s), draw=False, op=op))
    return els


def vaka(x, y, s, at, fx="rise", op=None, face=1, crew=4):
    """A double-hulled voyaging canoe in side view: two hulls (the far one darker), a deck with a small shelter, a mast and a crab-claw
    sail (a V of two spars, its top edge curved in); (x, y) the waterline at its middle, s its length."""
    f = face
    X = lambda u: x + f * u * s
    Y = lambda v: y + v * s
    far = [(X(-.47), Y(-.10)), (X(-.42), Y(-.02)), (X(.40), Y(-.02)), (X(.50), Y(-.12)), (X(.44), Y(-.075)), (X(-.42), Y(-.07))]
    near = [(X(-.52), Y(-.09)), (X(-.45), Y(.02)), (X(.42), Y(.02)), (X(.55), Y(-.11)), (X(.47), Y(-.06)), (X(-.45), Y(-.05))]
    els = [poly([(px + f * 18, py - 10) for px, py in far], WOOD_D, at=at, fx=fx, op=op),
           poly(near, WOOD, "rgba(255,226,180,.4)", 1.2, at, fx=fx, op=op),
           ln([(X(-.45), Y(-.04)), (X(.46), Y(-.04))], at, "#c9a86a", max(1.2, .005 * s), draw=False, op=op),
           rect(min(X(-.32), X(.32)), Y(-.095), .64 * s, .035 * s, "#6a4a30", "rgba(255,226,180,.3)", 1, 2, at, fx=fx, op=op),
           poly([(X(-.26), Y(-.095)), (X(-.26), Y(-.16)), (X(-.18), Y(-.20)), (X(-.10), Y(-.16)), (X(-.10), Y(-.095))], "#7a5a38", "rgba(255,226,180,.3)", 1, at,
                fx=fx, op=op)]
    mx, my = X(.06), Y(-.095)
    tip1, tip2 = (X(-.20), Y(-.78)), (X(.34), Y(-.70))
    inner = (X(.07), Y(-.46))
    els += [poly([(mx, my), tip1, (X(-.10), Y(-.62)), inner, (X(.20), Y(-.58)), tip2], SAIL, "rgba(150,110,70,.6)", 1.2, at, fx=fx, op=op, curve=False),
            poly([(mx, my), inner, (X(.20), Y(-.58)), tip2], "#d8c8a6", at=at, fx=fx, op=.6 if op is None else op * .6),
            ln([(mx, my), tip1], at, "#5a3e28", max(2, .008 * s), draw=False, op=op),
            ln([(mx, my), tip2], at, "#5a3e28", max(2, .008 * s), draw=False, op=op),
            ln([(X(.0), my), (X(.02), Y(-.40))], at, "#3a2a1e", max(2, .01 * s), draw=False, op=op)]
    for k in range(crew):
        els.append(ppl(X(-.36 + .16 * k + (.1 if k > 1 else 0)), Y(-.095), .12 * s, at, "#2a2018", fx or "rise", op))
    return els


def ship(x, y, s, at, fx="rise", op=None, face=1, masts=3, c="#3a2a1e", sail=SAIL, flag=None, sails=True):
    """A sailing ship of the 1700s or 1800s in side view: hull, masts, square sails; (x, y) the waterline at its middle, s its length."""
    f = face
    X = lambda u: x + f * u * s
    Y = lambda v: y + v * s
    els = [poly([(X(-.5), Y(-.16)), (X(-.44), Y(.03)), (X(.40), Y(.03)), (X(.52), Y(-.12)), (X(.30), Y(-.10)), (X(-.30), Y(-.12))], c,
                "rgba(255,226,180,.35)", 1.2, at, fx=fx, op=op),
           ln([(X(-.46), Y(-.08)), (X(.44), Y(-.06))], at, "#c9a86a", max(1.5, .008 * s), draw=False, op=op),
           ln([(X(.52), Y(-.12)), (X(.70), Y(-.20))], at, "#2a1e14", max(1.5, .008 * s), draw=False, op=op)]
    xs = [-.28, .02, .30][:masts] if masts == 3 else ([-.15, .18] if masts == 2 else [0])
    hs = [.62, .78, .58]
    for k, u in enumerate(xs):
        hh = hs[k % 3]
        els.append(ln([(X(u), Y(-.10)), (X(u), Y(-.10 - hh))], at, "#2a1e14", max(1.5, .01 * s), draw=False, op=op))
        if sails:
            for j, (v0, v1, w) in enumerate(((-.16, -.34, .19), (-.38, -.52, .16), (-.55, -.64, .11))):
                if -v1 > hh + .08:
                    continue
                els.append(poly([(X(u - w / 2), Y(v0 - .1 + .1)), (X(u + w / 2), Y(v0)), (X(u + w / 2 - .01), Y(v1)), (X(u - w / 2 + .01), Y(v1))],
                                sail, "rgba(120,90,60,.5)", 1, at, fx=fx, op=op, curve=False))
    if flag:
        u = xs[-1]
        els.append(poly([(X(u), Y(-.10 - hs[(len(xs) - 1) % 3])), (X(u + .08), Y(-.10 - hs[(len(xs) - 1) % 3] + .02)), (X(u), Y(-.10 - hs[(len(xs) - 1) % 3] + .045))],
                        flag, at=at, fx=fx, op=op))
    return els


def ship_icon(x, y, s, at, c=BONE, fx="pop", op=None):
    """A tiny ship mark for time lines and maps."""
    return [poly([(x - s * .5, y - s * .12), (x - s * .42, y + s * .05), (x + s * .4, y + s * .05), (x + s * .52, y - s * .12)], c, at=at, fx=fx, op=op),
            ln([(x, y - s * .12), (x, y - s * .7)], at, c, 2, draw=False, op=op),
            poly([(x - s * .2, y - s * .2), (x + s * .22, y - s * .22), (x + s * .18, y - s * .62), (x - s * .16, y - s * .6)], c, at=at, fx=fx,
                 op=.75 if op is None else op * .75)]


def waves_band(x0, x1, y, at, n=12, c="#bfe6f5", op=.35, seed=1):
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        xx = rnd.uniform(x0, x1)
        yy = y + rnd.uniform(0, 60)
        out.append(ln([(xx - 18, yy), (xx - 6, yy - 4), (xx + 6, yy), (xx + 18, yy - 3)], at, c, 1.5, draw=False, op=op, curve=True))
    return out


def sky_wash(kind="dawn", y0=-140, y1=560, at=-1):
    """The base's sky gradient laid again over the visible sky so its warm end sits at the horizon (the base spreads it over 2,400 units)."""
    return [rect(-40, y0, 1860, y1 - y0, "url(#k-sky-%s)" % kind, at=at)]


# ================================================================== cold open
def slope_y(x):
    """The surface of the outer slope of Rano Raraku (front grass), rising from the plain at the left to the crater at the right."""
    pts = [(-20, 548), (300, 530), (600, 482), (900, 404), (1150, 336), (1400, 300), (1800, 306)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def slope(at=-1, night=False):
    """The outer slope of Rano Raraku: the crater rim behind, grass falling to the plain at the left, the sea far off."""
    gc, gd, gl_ = (GRASS, GRASS_D, GRASS_L) if not night else ("#1f2618", "#141a10", "#344028")
    back = [(560, 520), (760, 400), (980, 300), (1200, 226), (1380, 186), (1520, 180), (1660, 196), (1800, 226), (1800, 700), (560, 700)]
    front = [(x, slope_y(x)) for x in range(-20, 1801, 60)] + [(1800, 1020), (-20, 1020)]
    els = [poly(back, gd, at=at, curve=True), poly(front, gc, at=at, curve=False)]
    els.append(ln([(x, slope_y(x)) for x in range(-20, 1801, 60)], at, gl_, 2, draw=False, op=.35))
    rnd = random.Random(7)
    for k in range(70):
        x = rnd.uniform(0, 1780)
        y = rnd.uniform(slope_y(x) + 20, 990)
        els.append(ln([(x - 5, y + 2), (x - 1, y - 9), (x + 1, y + 2), (x + 5, y - 10)], at, gl_, 1.4, draw=False, op=.5))
    return els


HERO_HEADS = [  # (cx, ground y, whole height, part visible, tilt, seed)
    (600, 498, 240, .36, -3, 2), (762, 456, 250, .36, 4, 3), (905, 420, 228, .35, -6, 4), (1032, 392, 214, .35, 2, 5),
    (520, 606, 360, .38, 3, 6), (726, 580, 390, .38, -2, 7), (962, 530, 330, .37, 5, 8)]


def sc_hero(night=False):
    """s1, the hero image, fully drawn from the first frame: the outer slope of Rano Raraku at golden light, seven heads in the grass
    at different heights and tilts, the nearest one large at the right; the sea far off at the left; two small people for scale.
    The top left (x < 960, y < 180) is sky only, for the hook title."""
    els = sky_wash("dawn" if not night else "night", -140 if not night else -300, 560)
    els += [rect(-20, 450, 1820, 140, SEA_D if not night else "#0b1a24", at=-1)]
    if not night:
        els += [gl(250, 468, 420, -1, .28, "sun")]
    els += waves_band(0, 620, 462, -1, 14, op=.22 if not night else .12)
    els += slope(night=night)
    mc = GRASS if not night else "#1f2618"
    for (cx, gy, h, vis, tilt, seed) in HERO_HEADS:
        els += buried(cx, gy, h, vis, -1, -1, tilt=tilt, seed=seed, lichen=3, c=mc)
    els += [ppl(400, 660, 66, -1, "#1d1813", None), ppl(424, 662, 60, -1, "#1d1813", None)]
    # the nearest head, large, lit from the left by the low sun
    els += buried(1300, 800, 1060, .485, -1, -1, tilt=-2, seed=11, lichen=0, c=mc)
    if not night:
        els += [gl(1160, 430, 320, -1, .16, "sun")]
    return els


def sc_hero_scene():
    els = sc_hero()
    els += [gl(250, 452, 160, -1, .55, "sun"), circ(250, 452, 24, "#ffe2b4", at=-1)]
    tr = T("hero", "old volcano")
    els += [lab(1560, 168, "Rano Raraku", tr, GOLD, 32)]
    return {"base": "sky", "tod": "dawn", "ground": 1100, "sun": [250, 452, 26], "cam": CAM, "els": els}


def add_dig():
    """s2 (on the hero panel, the camera in on a head on the slope): the ground in front of it opens as a trench, a digger at its edge,
    and the buried body shows inside it, arms along the sides and long fingers over the belly; 'buried by soil'."""
    cx, gy, h, vis, tilt, seed = HERO_HEADS[5]
    by = gy + (1 - vis) * h
    x0, x1, y0 = cx - .30 * h, cx + .30 * h, gy + 8
    y1 = by + 16
    body = moai(cx, by, h, -1, light=-1, lichen=0)
    rnd = random.Random(4)
    edge = [(x0 - 10 + (x1 - x0 + 20) * k / 12, y0 + rnd.uniform(-4, 4)) for k in range(13)]
    els = [poly([(x0 - 10, y0)] + edge + [(x1 + 10, y0), (x1 - 4, y1), (x0 + 4, y1)], SOIL_D, "rgba(255,226,190,.45)", 1.5, .3, op=.97),
           poly([(x0 - 10, y0)] + edge + [(x1 + 10, y0), (x1 - 4, y1), (x0 + 4, y1)], "url(#k-speck)", at=.3)]
    for k in range(1, 4):
        yy = y0 + (y1 - y0) * k / 4
        els.append(ln([(x0 + 2, yy), (x1 - 2, yy + 6)], .4, "rgba(255,226,190,.22)", 1.4, "inferred", draw=False))
    els.append(grp([{"k": "group", "tr": "rotate(%s %s %s)" % (tilt, cx, gy), "els": body}], .7, "fade", clip=[x0 + 4, y0, x1 - x0 - 8, y1 - y0, 3], dur=1.2))
    # the spoil heap and a digger with a digging stick at the edge
    els += [poly([(x1 + 6, y0 + 4), (x1 + 40, y0 - 22), (x1 + 90, y0 - 10), (x1 + 110, y0 + 6)], SOIL, "rgba(255,226,190,.3)", 1, .4, fx="rise"),
            ppl(x1 + 52, y0 - 14, 86, .5, "#1d1813"), ln([(x1 + 40, y0 - 70), (x1 - 6, y0 + 20)], .6, WOOD_L, 3, draw=False)]
    tb = T("dig", "buried")
    els += [ln([(x1 + 16, (y0 + y1) / 2 + 40), (x1 + 56, (y0 + y1) / 2 + 40)], tb, GOLD, 2, dur=.4),
            lab(x1 + 68, (y0 + y1) / 2 + 49, "buried by soil", tb, GOLD, 28, "start")]
    return els


RNV_IN = View(-109.47, -109.20, -27.215, -27.045, (150, 175, 420, 300))


def moai_mark(x, y, s, at, c=TUFF_L, op=None):
    """A tiny standing statue for maps: a long head on a short body (front view silhouette)."""
    return poly([(x - .16 * s, y), (x - .17 * s, y - .5 * s), (x - .13 * s, y - .58 * s), (x - .13 * s, y - 1.0 * s), (x + .13 * s, y - 1.0 * s),
                 (x + .13 * s, y - .58 * s), (x + .17 * s, y - .5 * s), (x + .16 * s, y)], c, at=at, op=op, fx="pop")


def sc_pacific():
    """s3: the south-east Pacific: South America at the right, Rapa Nui a glowing speck in open ocean; a window at the left shows the
    island enlarged with tiny statues sprinkling round it ('nearly 1,000 moai') and its length ('24 km'); then a dashed arrow from the
    speck to the coast of Chile, '3,500 km'."""
    v = PAC
    els = [pacific_land(v), lab(*v.p(-60.0, -17.0), "South America", -1, SAND_E, 30, st="ital"),
           lab(*v.p(-96.0, -41.0), "Pacific Ocean", -1, "#8fb8cc", 30, st="ital")]
    rx, ry = v.p(-109.35, -27.12)
    els += [gl(rx, ry, 90, -1, .7), circ(rx, ry, 7, GOLD, "#fff6e6", 2, -1), lab(rx, ry - 26, "Rapa Nui", -1, GOLD, 28)]
    wx, wy, ww, wh = 110, 360, 470, 380
    iv = View(-109.47, -109.20, -27.215, -27.045, (wx + 30, wy + 30, ww - 60, wh - 110))
    els += [rect(wx, wy, ww, wh, "#10232e", "rgba(255,236,206,.35)", 2, 10, .2),
            ln([(wx + ww, wy + 40), (rx - 12, ry + 6)], .3, "rgba(255,236,206,.35)", 1.5, "inferred", .6)]
    els += island(iv, .3)
    tn, tl = T("pacific", "Nearly a thousand"), T("pacific", "twenty-four")
    rnd = random.Random(5)
    pts = [iv.p(lo, la) for lo, la in RN_AHU]
    rr = iv.p(*RN_PLACES["Rano Raraku"])
    marks = []
    for (x, y) in pts:
        for j in range(2):
            marks.append((x + rnd.uniform(-6, 6), y + rnd.uniform(-4, 4)))
    for k in range(16):
        a = rnd.uniform(0, 2 * math.pi)
        marks.append((rr[0] + math.cos(a) * rnd.uniform(4, 18), rr[1] + math.sin(a) * rnd.uniform(3, 12)))
    for k in range(10):
        marks.append(iv.p(rnd.uniform(-109.40, -109.30), rnd.uniform(-27.15, -27.09)))
    for k, (x, y) in enumerate(marks):
        els.append(moai_mark(x, y, 12, round(tn + .02 * k, 2)))
    els += [lab(wx + ww / 2, wy + wh - 24, "nearly 1,000 moai", tn + .4, GOLD, 28)]
    a_, b_ = iv.p(-109.452, -27.192), iv.p(-109.224, -27.104)
    els += [{"k": "dim", "x1": a_[0], "y1": a_[1] + 30, "x2": b_[0], "y2": b_[1] + 30, "t": "24 km", "c": BONE, "in": tl, "fx": "draw", "dur": .7, "ly": 34}]
    tc = T("pacific", "three and a half")
    cx_, cy_ = v.p(-71.0, -27.1)
    els += [arr([(rx + 16, ry), ((rx + cx_) / 2, ry - 50), (cx_ - 12, cy_)], tc, AMBER, 3, "inferred", 1.2, curve=True),
            lab((rx + cx_) / 2, ry - 76, "3,500 km", tc + .6, AMBER, 32)]
    return {"base": "map", "cam": CAM, "els": els}


def palm_outline(x, y, h, at, ang=0, c=LILAC, style="claimed", w=2.6):
    """A palm in outline (a claim): trunk lines and a fan of fronds, turned by ang degrees about its foot."""
    pts_t = [(x - h * .04, y), (x - h * .03, y - h), (x + h * .03, y - h), (x + h * .04, y)]
    fr = []
    for k in range(7):
        a = math.radians(-170 + 160 * k / 6)
        fr.append([(x, y - h), (x + math.cos(a) * h * .3, y - h + math.sin(a) * h * .18 - 6), (x + math.cos(a) * h * .45, y - h + math.sin(a) * h * .1 + h * .12)])
    els = [ln(pts_t, -1, c, w, style, draw=False)] + [ln(f, -1, c, w, style, draw=False, curve=True) for f in fr]
    return [grp(els, at, "pop", tr="rotate(%s %s %s)" % (ang, x, y))]


def adze(x, y, s, at, c=LILAC, style="claimed"):
    """A stone adze on its haft (outline)."""
    return [ln([(x, y), (x + .7 * s, y - .7 * s)], at, c, 3, style, draw=False),
            poly([(x + .55 * s, y - .85 * s), (x + .95 * s, y - .62 * s), (x + .88 * s, y - .5 * s), (x + .5 * s, y - .72 * s)], "rgba(201,193,238,.08)", c, 2.4, at,
                 style=style, fx="pop")]


def basket(x, y, s, at, c=LILAC, style="claimed"):
    """An empty food basket (outline): a bowl with a weave line."""
    return [poly([(x - s, y - .5 * s), (x + s, y - .5 * s), (x + .7 * s, y + .2 * s), (x - .7 * s, y + .2 * s)], "rgba(201,193,238,.06)", c, 2.6, at, style=style, fx="pop"),
            ln([(x - .85 * s, y - .2 * s), (x + .85 * s, y - .2 * s)], at + .1, c, 2, style, draw=False)]


def spear(x0, y0, x1, y1, at, c=LILAC, style="claimed"):
    a = math.atan2(y1 - y0, x1 - x0)
    hx, hy = x1 + math.cos(a) * 28, y1 + math.sin(a) * 28
    nx, ny = -math.sin(a) * 9, math.cos(a) * 9
    return [ln([(x0, y0), (x1, y1)], at, c, 3, style, draw=False),
            poly([(x1 + nx, y1 + ny), (hx, hy), (x1 - nx, y1 - ny)], "rgba(201,193,238,.1)", c, 2.2, at, style=style, fx="pop")]


def sc_story():
    """s4: the famous story as a strip of four small scenes on one dusk horizon, in lilac dotted lines (a claim), built as named: a palm
    falling to an adze, an empty basket, two crossed spears, a statue toppled on its face; at the right a ship on the horizon, '1722';
    on the question, a large lilac question mark."""
    G = 660
    els = sky_wash("dusk", -200, 700)
    els += [rect(-20, G, 1820, 400, "#1c1a16", at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,226,190,.3)", 1.5, draw=False)]
    els += [rect(-20, G - 70, 1820, 70, "#1b2a33", at=-1, op=.9)] + waves_band(1360, 1780, G - 64, -1, 8, op=.2)
    els += [poly([(-20, G - 66), (160, G - 120), (420, G - 150), (700, G - 128), (900, G - 160), (1120, G - 118), (1300, G - 66)], "#1a1c16", at=-1, curve=True)]
    rnd_ = random.Random(2)
    for k in range(18):
        x = 40 + k * 70 + rnd_.uniform(-14, 14)
        els += palm(x, G - 70 - max(0, 80 - abs(x - 700) * .1), rnd_.uniform(46, 70), -1, seed=80 + k, c="#1c2418", cd="#151b12", cl="#2a3424", trunk="#1c1a16")
    tt, ts, tf, tl, te, tq = (T("story", "every tree"), T("story", "starved"), T("story", "fought"), T("story", "and fell"),
                              T("story", "before any European"), T("story", "Did they"))
    xs = [230, 600, 970, 1330]
    els += palm_outline(xs[0] - 40, G, 340, tt - .3, ang=26) + adze(xs[0] + 60, G - 40, 120, tt) + [lab(xs[0], G + 60, "every tree", tt, LILAC, 30)]
    els += basket(xs[1], G - 70, 100, ts) + [lab(xs[1], G + 60, "starved", ts, LILAC, 30)]
    els += spear(xs[2] - 120, G - 10, xs[2] + 90, G - 270, tf) + spear(xs[2] + 120, G - 10, xs[2] - 90, G - 270, tf + .15) + [lab(xs[2], G + 60, "fought", tf, LILAC, 30)]
    els += lying(xs[3], G - 4, 300, tl, up=False, style="claimed")
    els += [lab(xs[3], G + 60, "fell", tl, LILAC, 30)]
    els += ship(1640, G - 66, 170, te, "rise", c="#2a2018", sail="#d8c9a8") + chip(1640, G + 60, "1722", GOLD, te + .3, 28)
    for k in range(3):
        els.append(arr([(xs[k] + 120, G - 150), (xs[k] + 230, G - 150)], tt + .4 * (k + 1), "rgba(201,193,238,.7)", 2.4, "claimed", .4))
    els += qmark(889, 300, tq, 140)
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": False, "cam": CAM, "els": els}


# ================================================================== chapter 1: a forest of giant palms
def hills(y0, at=-1, c=GRASS, seed=3, amp=60, op=None):
    rnd = random.Random(seed)
    pts = [(-20, y0 + rnd.uniform(-amp, amp) * .3)]
    for k in range(1, 9):
        pts.append((-20 + 1840 * k / 8, y0 - abs(math.sin(k * 1.3 + seed)) * amp))
    return poly(pts + [(1820, 1020), (-20, 1020)], c, at=at, op=op, curve=True)


def sc_landing():
    """s5: dawn at Anakena, seen from the bay: green hills of tall palms behind a narrow white beach; a double-hulled voyaging canoe with
    a crab-claw sail in the shallows; three figures wade ashore. 'Anakena', 'Hotu Matu'a'; a small Polynesian triangle at the upper
    right with Rapa Nui at its eastern corner."""
    els = sky_wash("dawn", -220, 560)
    els += [gl(1640, 360, 340, -1, .5, "sun"), circ(1640, 372, 30, "#ffe2b4", at=-1)]
    els += [hills(360, -1, "#3a5530", 3, 70), hills(400, -1, "#46663a", 7, 50)]
    rnd = random.Random(11)
    for k in range(17):
        x = 40 + k * 110 + rnd.uniform(-30, 30)
        els += palm(x, 470 + rnd.uniform(-30, 20), rnd.uniform(120, 190), -1, seed=20 + k, lean=rnd.uniform(-6, 6))
    els += [poly([(-20, 480), (300, 470), (700, 486), (1100, 482), (1500, 470), (1800, 476), (1800, 520), (-20, 520)], "#e2d6bc", "rgba(255,246,226,.5)", 1.2, -1,
                  curve=True)]
    els += [rect(-20, 512, 1820, 520, SEA, at=-1), rect(-20, 512, 1820, 520, "url(#k-water)", at=-1, op=.55)]
    els += waves_band(0, 1780, 520, -1, 30, op=.3) + waves_band(0, 1780, 640, -1, 24, op=.22, seed=4)
    els += vaka(1180, 700, 640, .3, "rise", crew=4)
    th = T("landing", "Hotu")
    sea_ = static([rect(-20, 512, 1820, 520, SEA, at=-1), rect(-20, 512, 1820, 520, "url(#k-water)", at=-1, op=.55)])
    for k, (x, hh) in enumerate(((640, 78), (700, 74), (760, 70))):
        t = round(th - .8 + .2 * k, 2)
        els += [ppl(x, 600, hh, t, "#241b14"), {"k": "group", "clip": [x - 30, 584, 60, 24, 0], "els": sea_, "in": t}]
    els += [gl(640, 540, 90, th, .45), lab(640, 470 - 16, "Hotu Matu'a", th + .2, GOLD, 30)]
    els += [lab(300, 452, "Anakena", T("landing", "Anakena"), BONE, 32)] + chip(220, 200, "about 1200", GOLD, .4, 28)
    tx, ty, tw_, th_ = 1260, 130, 400, 230
    els += [rect(tx, ty, tw_, th_, "rgba(14,22,30,.86)", "rgba(255,236,206,.3)", 2, 10, .4)]
    A, Bp, C = (tx + 160, ty + 48), (tx + 60, ty + 186), (tx + 330, ty + 150)
    els += [ln([A, Bp, C, A], .6, "rgba(242,201,142,.6)", 2, "inferred", 1.0), dot(A[0], A[1], 6, BONE, .6), dot(Bp[0], Bp[1], 6, BONE, .7),
            gl(C[0], C[1], 40, .9, .6), dot(C[0], C[1], 8, GOLD, .9),
            lab(A[0] + 14, A[1] + 8, "Hawaii", .6, DIM, 24, "start"), lab(Bp[0] + 4, Bp[1] + 32, "Aotearoa", .7, DIM, 24),
            lab(C[0] - 10, C[1] + 34, "Rapa Nui", .9, GOLD, 24)]
    return {"base": "sky", "tod": "dawn", "ground": 1100, "sun": False, "cam": CAM, "els": els}


def pollen(x, y, r, at, kind="grass"):
    """A pollen grain under the magnifier: grass (a pale round grain with one pore), palm (a dark green boat-shaped grain with a furrow),
    tree (a three-pored round grain)."""
    if kind == "grass":
        return [circ(x, y, r, "#e8d9a0", "#b8a870", 1.2, at, fx="pop"), circ(x + r * .3, y - r * .2, r * .2, "#b8a870", at=at, fx="pop")]
    if kind == "palm":
        return [poly(E(x, y, r * 1.3, r * .75, 18), "#5a8a4a", "#a8d090", 1.2, at, fx="pop"), ln([(x - r, y), (x + r, y)], at, "#2a4a22", 2, draw=False)]
    return [circ(x, y, r, "#7aa060", "#b8d8a0", 1.2, at, fx="pop")] + [circ(x + math.cos(a) * r * .6, y + math.sin(a) * r * .6, r * .16, "#3a5a2a", at=at, fx="pop")
                                                                       for a in (0, 2.1, 4.2)]


def sc_core():
    """s6: a crater lake in cross-section: the rim, still water, and the mud below it in many thin layers filling the bowl; a raft and a
    coring tube going down; at the right the core enlarged as a column of layers with two magnifiers: near the top grass pollen, deep
    down palm and tree pollen."""
    cx, ly, depth, hw = 600, 430, 250, 330
    wfun = lambda d: hw * math.sqrt(max(0.0, 1 - (d / (depth + 6)) ** 2))
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1), gl(600, 300, 760, -1, .12)]
    wall = [(-20, 300), (100, 270), (180, 300), (cx - hw - 40, ly - 10), (cx - hw, ly), (cx + hw, ly), (cx + hw + 40, ly - 10), (1040, 290), (1120, 262), (1220, 300),
            (1220, 1020), (-20, 1020)]
    els += [poly(wall, "#3a3128", "rgba(255,226,190,.35)", 1.5, -1)]
    for x in range(-10, 1220, 26):
        yy = 300 if x < 200 or x > 1000 else None
        if yy:
            els.append(ln([(x - 4, yy - 2), (x, yy - 12), (x + 4, yy - 2)], -1, GRASS_L, 1.4, draw=False, op=.6))
    cols = ["#857456", "#76664a", "#8a7a5a", "#6e5e44", "#80704e", "#686046", "#5c6e44", "#4e663c", "#5a7444", "#46623a", "#52703f"]
    n = len(cols)
    tdi = T("core", "keep a diary")
    for k, c in enumerate(cols):
        da, db = depth * k / n, depth * (k + 1) / n
        p = [(cx - wfun(da), ly + da), (cx + wfun(da), ly + da), (cx + wfun(db), ly + db), (cx - wfun(db), ly + db)]
        els.append(poly(p, c, at=-1))
    els += [poly([(cx - hw, ly), (cx + hw, ly), (cx + hw - 6, ly + 8), (cx - hw + 6, ly + 8)], "#3f7f9c", at=-1, op=.9),
            rect(cx - hw, ly - 60, 2 * hw, 60, "rgba(63,127,156,.25)", at=-1)]
    els += [lab(cx - 150, ly - 80, "crater lake", .4, "#bfe6f5", 28)]
    tl = T("core", "layer upon layer")
    els += [{"k": "dim", "x1": cx - hw - 70, "y1": ly + 6, "x2": cx - hw - 70 + 60, "y2": ly + depth, "t": "", "c": BONE, "in": tl, "fx": "draw", "dur": .6},
            lab(cx, ly + depth + 56, "layer upon layer", tl, BONE, 28)]
    td = T("core", "Drill down")
    els += [rect(cx + 40, ly - 16, 100, 16, WOOD, "rgba(255,226,180,.4)", 1, 3, td - 1.2, fx="pop"),
            ln([(cx + 60, ly - 16), (cx + 90, ly - 90), (cx + 120, ly - 16)], td - 1.0, "#cbbca8", 2.5, draw=False),
            ln([(cx + 90, ly - 80), (cx + 90, ly + depth - 10)], td, "#e8e0d0", 7, dur=1.2)]
    k0, kw_, ky0, kh = 1300, 120, 150, 560
    tc = td + 1.0
    for k in range(n):
        els.append(rect(k0, ky0 + kh * k / n, kw_, kh / n + 1, cols[k], at=round(tc + .06 * k, 2), fx="pop"))
    els += [rect(k0, ky0, kw_, kh, "none", "rgba(255,236,206,.55)", 2, 4, tc), lab(k0 + kw_ / 2, ky0 - 18, "the core", tc, DIM, 24),
            ln([(cx + 98, ly + depth - 10), (k0 - 8, ky0 + kh * .8)], tc, "rgba(255,236,206,.3)", 1.5, "inferred", .6)]
    tp, tg = T("core", "pollen from"), T("core", "full of trees")
    for (yy, kind, t, txt, col) in ((ky0 + kh * .12, "grass", tp, "grass", BONE), (ky0 + kh * .82, "palm", tg - .2, "palms and trees", "#a8d090")):
        mx, my = 1570, yy
        els += [ln([(k0 + kw_, yy), (mx - 82, my)], t, "rgba(255,236,206,.5)", 1.5, dur=.3), circ(mx, my, 82, "#1e1a14", "#e8d6b0", 3, t, fx="pop")]
        rnd = random.Random(int(yy))
        for j in range(6):
            a = j * 1.05 + rnd.uniform(-.2, .2)
            kk = kind if kind == "grass" else ("palm" if j % 2 == 0 else "tree")
            els += pollen(mx + math.cos(a) * 42, my + math.sin(a) * 38, 12, t + .2 + .06 * j, kk)
        els += [lab(mx, my + 118, txt, t + .3, col, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def pip(pt, poly_):
    x, y = pt
    inside = False
    n = len(poly_)
    for i in range(n):
        x1, y1 = poly_[i]
        x2, y2 = poly_[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


RNV_CARD = View(-109.47, -109.20, -27.215, -27.045, (1110, 240, 540, 360))


def palm_marks(v, at, dur, n=110, seed=3, frac=.7, c=PALM_L):
    """Small palm crowns filling about frac of the island (a schematic of the woodland cover, not a map of it)."""
    P = [v.p(lo, la) for lo, la in RN]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    rnd = random.Random(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        q = (rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys)))
        if pip(q, P):
            pts.append(q)
    pts.sort(key=lambda q: q[0] + q[1] * .3)
    keep = pts[:int(len(pts) * frac / .75)] if frac < .75 else pts
    out = []
    for k, (x, y) in enumerate(keep):
        out.append(circ(x, y, 5.5, c, "rgba(20,40,15,.6)", 1, round(at + dur * k / max(1, len(keep)), 2), fx="pop"))
    return out


def palm_hill(at=-1):
    els = sky_wash("day", -200, 640)
    els += [hills(560, at, "#3e5a30", 5, 80), hills(640, at, "#4a6a36", 9, 40)]
    rnd = random.Random(4)
    spots = [(140, 600, 300), (290, 590, 360), (430, 610, 330), (560, 600, 380), (700, 620, 420), (860, 640, 470), (990, 660, 360), (230, 680, 260), (640, 700, 300)]
    for k, (x, y, h) in enumerate(spots):
        els += palm(x, y, h, at, seed=40 + k, lean=rnd.uniform(-5, 5))
    return els


def sc_palms():
    """s7: left, a hillside of giant palms with a person by the nearest trunk ('a giant palm, now extinct'); right, the island outline
    filling with palm marks over about 70 percent of its area, a counter '16 million +'."""
    els = palm_hill()
    els += [ppl(905, 640, 74, .4, "#2a2018")]
    tg = T("palms", "giant palm")
    els += [lab(560, 760, "giant palm, now extinct", tg + .2, BONE, 28)]
    els += [rect(1090, 170, 580, 520, "rgba(14,22,30,.9)", "rgba(255,236,206,.3)", 2, 12, .3)]
    els += island(RNV_CARD, .3, fill="#5a5a3a", volcanoes=False)
    ts = T("palms", "sixteen million")
    els += palm_marks(RNV_CARD, ts - 1.2, 1.8)
    els += [lab(1380, 660, "16 million +", ts, "#a8d090", 40, st="serif")]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "cam": CAM, "els": els}


def add_gone():
    """s8 (back on the palm panel): the hillside again, bare: grass and stumps fade in over the palms; the island's palm marks dim away;
    'by the 1500s'."""
    bare = sky_wash("day", -200, 640) + [hills(560, -1, "#5a6a3a", 5, 80), hills(640, -1, "#66763e", 9, 40)]
    for (x, y, h) in [(140, 600, 300), (290, 590, 360), (430, 610, 330), (560, 600, 380), (700, 620, 420), (860, 640, 470), (990, 660, 360), (230, 680, 260), (640, 700, 300)]:
        bare += stump(x, y, h * .14, -1)
    bare += [ppl(905, 640, 74, -1, "#2a2018")]
    els = [{"k": "group", "els": static(bare), "in": .3, "dur": 1.6}]
    card = [rect(1090, 170, 580, 520, "rgba(14,22,30,.96)", "rgba(255,236,206,.3)", 2, 12, -1)] + island(RNV_CARD, -1, fill="#6a6a44", volcanoes=False)
    els += [{"k": "group", "els": static(card), "in": .3, "dur": 1.6}]
    els += [lab(1380, 660, "nearly all gone", .9, BONE, 30)] + chip(1380, 740, "by the 1500s", GOLD, .8, 28)
    return els


def flame(x, y, s, at, op=None):
    return [gl(x, y - s * .4, s * 1.6, at, .55 if op is None else op, "fire"),
            poly([(x - s * .35, y), (x - s * .2, y - s * .6), (x - s * .05, y - s * .45), (x, y - s * 1.1), (x + s * .12, y - s * .5), (x + s * .25, y - s * .7),
                  (x + s * .35, y)], "#ff9a4a", "#ffd08a", 1, at, fx="pop", curve=True, op=op),
            poly([(x - s * .15, y), (x, y - s * .55), (x + s * .15, y)], "#ffe0a0", at=at, fx="pop", op=op)]


def smoke(x, y, at, n=5, seed=1):
    rnd = random.Random(seed)
    return [circ(x + rnd.uniform(-20, 20) + k * 14, y - 40 - k * 46, 22 + k * 8, "#8a8078", at=round(at + .2 * k, 2), op=.22 - .03 * k) for k in range(n)]


def sc_fire():
    """s9: above, land cleared with fire: figures with torches, flames and smoke on the slope, burned stumps, palms beyond; below, the
    soil in section: a black burned layer with charred palm nuts and a burned stump in it. 'burned stump', 'charred nuts', '1250 to 1500'."""
    G = 430
    els = sky_wash("dusk", -200, 560)
    els += [poly([(-20, G), (1820, G), (1820, 1020), (-20, 1020)], "#4a3a2a", at=-1)]
    rnd = random.Random(9)
    for k in range(6):
        els += palm(1180 + k * 100 + rnd.uniform(-20, 20), G + 4, rnd.uniform(170, 230), -1, seed=60 + k)
    els += stump(420, G, 44, -1, burnt=True) + stump(640, G, 38, -1, burnt=True) + stump(860, G, 46, -1, burnt=True)
    tp = T("fire", "point to people")
    els += [ppl(260, G, 80, tp - .4, "#1d1813"), ppl(980, G, 78, tp - .2, "#1d1813")]
    els += flame(520, G, 70, tp) + flame(760, G, 90, tp + .2) + flame(1080, G, 60, tp + .4) + smoke(520, G, tp + .3, 5, 2) + smoke(760, G, tp + .5, 5, 3)
    els += [ln([(268, G - 70), (300, G - 110)], tp - .3, "#6a4a2a", 4, draw=False)] + flame(304, G - 112, 22, tp - .2)
    # the soil, in section
    els += [rect(-20, G + 30, 1820, 120, "#6a523a", at=-1), rect(-20, G + 150, 1820, 70, CHAR, at=-1), rect(-20, G + 220, 1820, 400, "#7a4a32", at=-1),
            rect(-20, G + 30, 1820, 600, "url(#k-speck)", at=-1)]
    tb, tc = T("fire", "Burned stumps"), T("fire", "charred palm")
    els += [poly([(820, G + 120), (812, G + 220), (900, G + 220), (890, G + 120)], "#151210", "rgba(255,160,100,.35)", 1.2, tb, fx="pop"),
            gl(856, G + 180, 90, tb, .25, "fire")]
    for k in range(12):
        x = 140 + k * 128 + rnd.uniform(-30, 30)
        if 790 < x < 920:
            continue
        els += nut(x, G + 186 + rnd.uniform(-14, 14), 13, tc + .05 * k, charred=True)
    els += [lab(960, G + 132, "burned stump", tb + .2, "#ffb07a", 28, "start"), lab(380, G + 278, "charred nuts", tc + .3, "#ffb07a", 28)]
    els += chip(1490, G + 278, "1250 to 1500", GOLD, T("fire", "twelve fifty"), 28)
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": False, "cam": CAM, "els": els}


def sc_rat():
    """s10: close, at the scale of life: a Polynesian rat by a little pile of palm nuts; on 'gnawed', a ragged hole shows in each; a small
    canoe with a rat aboard at the upper left ('carried by canoe'). 'Polynesian rat', 'gnawed by rats'."""
    G = 650
    els = [rect(-20, -20, 1820, 1040, "#18140f", at=-1), gl(900, 560, 720, -1, .16), rect(-20, G, 1820, 400, "#241d16", at=-1),
           ln([(-20, G), (1800, G)], -1, "rgba(255,226,190,.25)", 1.5, draw=False)]
    tr, tg = T("rat", "Polynesian rat"), T("rat", "gnawed by")
    els += vaka(330, 330, 300, .3, "rise", crew=0) + rat(310, 318, 56, tr - .3, face=1)
    els += [lab(330, 400, "carried by canoe", tr, DIM, 26)]
    els += rat(1130, G, 380, tr, face=-1)
    pile = [(640, G - 30, 36, 10), (720, G - 32, 38, 60), (800, G - 30, 36, 130), (680, G - 86, 36, 200), (760, G - 88, 37, 300), (720, G - 140, 35, 250),
            (880, G - 34, 36, 340)]
    for k, (x, y, r, a) in enumerate(pile):
        els += nut(x, y, r, -1, None, ang=a, seed=k + 3)
    for k, (x, y, r, a) in enumerate(pile):
        els += nut(x, y, r, round(tg - .6 + .1 * k, 2), gnawed=True, ang=a, seed=k + 3)
    els += [lab(1130, 330, "Polynesian rat", tr + .2, BONE, 32), lab(740, G + 70, "gnawed by rats", tg + .3, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_ratchart():
    """s11: a chart that builds: rat numbers over 0 to 50 years, from a pair to 11 million by year 47 (the model's curve); beside it,
    twenty seeds of which nineteen are eaten, one left whole ('almost every seed')."""
    x0, x1, y0, y1 = 200, 1000, 700, 220
    X = lambda t: x0 + (x1 - x0) * t / 50
    Y = lambda n: y0 - (y0 - y1) * n / 12e6
    els = [axis(x0, x1, y0, [(X(t), str(t)) for t in (0, 10, 20, 30, 40, 50)], .2, "years"),
           ln([(x0, y0), (x0, y1 - 20)], .2, "#e9dccb", 2, draw=False)]
    for n, t in ((4e6, "4 million"), (8e6, "8 million"), (12e6, "12 million")):
        els += [ln([(x0, Y(n)), (x1, Y(n))], .3, "rgba(233,220,203,.15)", 1.2, draw=False), lab(x0 - 14, Y(n) + 9, t, .3, DIM, 24, "end")]
    K, r = 11.5e6, .408
    pts = []
    for k in range(0, 101):
        t = 50 * k / 100
        nN = K / (1 + (K - 2) / 2 * math.exp(-r * t))
        pts.append((X(t), Y(nN)))
    tp = T("ratchart", "rats could pass")
    els += [ln(pts, tp, "#e8b87a", 5, dur=2.2, curve=True), dot(X(47), Y(K / (1 + (K - 2) / 2 * math.exp(-r * 47))), 9, GOLD, tp + 2.1),
            lab(X(47) - 20, Y(11.2e6) - 24, "11 million", tp + 2.2, GOLD, 32, "end")]
    els += [lab(x0 + 10, y1 - 34, "rats", .3, AMBER, 28, "start", st="cap")]
    te = T("ratchart", "eating almost")
    gx, gy = 1180, 300
    for k in range(20):
        x, y = gx + (k % 5) * 92, gy + (k // 5) * 92
        if k == 12:
            els += nut(x, y, 26, .4) + [gl(x, y, 60, te + 1.4, .5)]
        else:
            els += nut(x, y, 26, .4) + nut(x, y, 26, round(te + .06 * k, 2), gnawed=True, ang=30 * k)
    els += [lab(gx + 184, gy + 400, "almost every seed", te + .6, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_balance():
    """s12: a balance: on the left pan a flame and a stone adze ('people'), on the right a rat ('rats'); then both glow together, 'both'."""
    tp, tr, tb = T("balance", "blames people"), T("balance", "the rats were"), T("balance", "Most likely")

    def left(x, y, at):
        return flame(x - 30, y, 60, tp) + adze(x + 10, y - 6, 70, tp + .2, c=TUFF_L, style="known") + [lab(x, y + 60, "people", tp + .3, BONE, 28)]

    def right(x, y, at):
        return rat(x + 20, y, 150, tr, face=-1) + [lab(x, y + 60, "rats", tr + .2, BONE, 28)]
    els = balance(889, 300, 700, 0, 760, .3, left, right, drop_=230, pan=230)
    els += [gl(889, 520, 520, tb, .25), lab(889, 220, "both", tb + .3, GOLD, 44, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def ahu(x0, x1, y, h, at, fx=None, op=None):
    """A stone platform (ahu) in front view: fitted basalt blocks, its top at y, h tall."""
    els = [rect(x0, y, x1 - x0, h, "#4a4440", "rgba(255,236,206,.3)", 1.5, 2, at, fx=fx, op=op)]
    rnd = random.Random(int(x0))
    rows = max(2, int(h // 26))
    for r_ in range(rows):
        yy = y + h * r_ / rows
        els.append(ln([(x0, yy), (x1, yy)], at, "#2e2a26", 1.2, draw=False, op=op))
        xx = x0 + rnd.uniform(10, 50)
        while xx < x1 - 10:
            els.append(ln([(xx, yy), (xx, yy + h / rows)], at, "#2e2a26", 1.2, draw=False, op=op))
            xx += rnd.uniform(40, 90)
    return els


def sc_paro():
    """s13: Paro standing on its stone platform at dusk, lit from the right, the sea behind it; a person (1.7 m) at the platform's foot;
    a dimension line 'about 10 m' and a chip 'about 80 t'. 55 units = 1 m."""
    G, M = 760, 55.0
    els = sky_wash("dusk", -240, 560)
    els += [rect(-20, 520, 1820, 260, SEA_D, at=-1), rect(-20, 520, 1820, 260, "url(#k-water)", at=-1, op=.4)] + waves_band(0, 1780, 530, -1, 22, op=.22)
    els += [gl(1500, 500, 300, -1, .35, "sun")]
    els += [poly([(-20, G - 20), (400, G - 30), (900, G - 26), (1400, G - 30), (1800, G - 20), (1800, 1020), (-20, 1020)], "#2f3a22", at=-1)]
    ah = 1.0 * M
    els += ahu(560, 1220, G - 30 - ah, ah, -1)
    top = G - 30 - ah
    tp = T("paro", "Paro")
    els += moai(889, top, 9.8 * M, -1, light=1)
    els += [ppl(1290, G - 26, 1.7 * M, .4, "#1d1813"), lab(1290, G + 16, "1.7 m", .5, DIM, 24)]
    tt, te = T("paro", "ten metres"), T("paro", "eighty")
    els += [{"k": "dim", "x1": 1120, "y1": top, "x2": 1120, "y2": top - 9.8 * M, "t": "about 10 m", "c": GOLD, "in": tt, "fx": "draw", "dur": .8, "lx": 30, "a": "start", "upright": True}]
    els += [lab(889, top - 9.8 * M - 22, "Paro", tp, GOLD, 32)]
    els += chip(560, 300, "about 80 t", AMBER, te, 30)
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": False, "cam": CAM, "els": els}


RNV_BIG = View(-109.47, -109.20, -27.215, -27.045, (110, 150, 1000, 560))


def wheel_icon(x, y, r, at, c=BONE):
    els = [circ(x, y, r, "none", c, 4, at, fx="pop"), circ(x, y, r * .18, c, at=at, fx="pop")]
    for k in range(6):
        a = math.pi * k / 3
        els.append(ln([(x, y), (x + math.cos(a) * r, y + math.sin(a) * r)], at, c, 3, draw=False))
    return els


def ox_icon(x, y, s, at, c=BONE):
    """A draught ox in side view, a flat silhouette."""
    body = [(x - .5 * s, y - .5 * s), (x + .25 * s, y - .55 * s), (x + .45 * s, y - .72 * s), (x + .62 * s, y - .62 * s), (x + .6 * s, y - .45 * s),
            (x + .42 * s, y - .4 * s), (x + .38 * s, y), (x + .28 * s, y), (x + .24 * s, y - .3 * s), (x - .3 * s, y - .3 * s), (x - .34 * s, y),
            (x - .44 * s, y), (x - .48 * s, y - .3 * s), (x - .56 * s, y - .42 * s)]
    return [poly(body, "none", c, 3, at, fx="pop"), ln([(x + .44 * s, y - .72 * s), (x + .36 * s, y - .86 * s)], at, c, 3, draw=False),
            ln([(x + .52 * s, y - .70 * s), (x + .62 * s, y - .84 * s)], at, c, 3, draw=False)]


def sc_problem():
    """s14: Rapa Nui: the quarry Rano Raraku pinned, platforms round the coast, dashed paths from the quarry to the coast; two icons struck
    through: a wheel and an ox ('no wheels', 'no draft animals')."""
    v = RNV_BIG
    els = island(v, -1, fill="#4e5a34")
    qx, qy = v.p(*RN_PLACES["Rano Raraku"])
    els += [gl(qx, qy, 70, -1, .5), {"k": "pin", "x": qx, "y": qy, "t": "Rano Raraku", "c": GOLD, "in": -1, "lx": 18, "ly": 34}]
    for k, (lo, la) in enumerate(RN_AHU):
        x, y = v.p(lo, la)
        els += [rect(x - 9, y - 4, 18, 8, "#2e2a26", "rgba(255,236,206,.5)", 1, 1, .3 + .04 * k, fx="pop"), moai_mark(x, y - 4, 16, .35 + .04 * k)]
    tm = T("problem", "move that")
    for k, (lo, la) in enumerate(RN_AHU):
        if k % 2:
            continue
        x, y = v.p(lo, la)
        mx_, my_ = (qx + x) / 2, (qy + y) / 2 - 30
        els.append(ln([(qx, qy), (mx_, my_), (x, y - 8)], round(tm + .08 * k, 2), AMBER, 2.4, "inferred", .7, curve=True))
    tw, ta = T("problem", "no wheels"), T("problem", "no animals")
    els += wheel_icon(1380, 330, 70, tw) + cross(1380, 330, tw + .4, RED, 3.2) + [lab(1380, 450, "no wheels", tw + .2, BONE, 28)]
    els += ox_icon(1400, 680, 190, ta) + cross(1400, 600, ta + .4, RED, 3.2) + [lab(1400, 730, "no draft animals", ta + .2, BONE, 28)]
    return {"base": "map", "cam": CAM, "els": els}


def lying(x, y, h, at, up=True, fx="pop", op=None, broken=False, base=None, sockets=True, style="known"):
    """A statue lying on the ground in side view, its head to the right: on its back (up=True, face to the sky) or face down; x, y the
    middle of its length on the ground. broken: split at the neck."""
    if up:      # mirror, then a quarter turn: the back on the ground, the face up
        tr = "translate(%s %s) rotate(90) scale(-1 1)" % (round(x - .5 * h, 1), round(y - .105 * h, 1))
    else:       # a quarter turn: the face on the ground
        tr = "translate(%s %s) rotate(90)" % (round(x - .5 * h, 1), round(y - .17 * h, 1))
    out = [grp(moai_side(0, 0, h, -1, base=base, sockets=sockets, style=style), at, fx, tr=tr, op=op)]
    if broken:
        out.append(ln([(x + .06 * h, y - .3 * h), (x + .1 * h, y + .02 * h)], at, "#120e0b", max(3, .025 * h), draw=False))
    return out


def sc_sledge():
    """s15: a replica lying on its back on a wooden sledge over log rails; long ropes run forward to two rows of pullers ('60 people');
    chip '1998', 'about 10 t'; along the ground 'nearly 100 m in a day'."""
    G = 640
    els = sky_wash("day", -200, 640) + [rect(-20, G, 1820, 400, "#4a5a30", at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,236,206,.3)", 1.5, draw=False)]
    els += [hills(560, -1, "#56663a", 13, 50)] + [rect(-20, G, 1820, 400, "#4a5a30", at=-1)]
    ts = T("sledge", "lay them")
    for k in range(16):
        x = 120 + k * 60
        els.append(rect(x, G - 6, 14, 12, WOOD, "rgba(255,226,180,.3)", 1, 3, -1))
    els += [ln([(110, G - 8), (1080, G - 8)], -1, WOOD_L, 4, draw=False), ln([(110, G + 4), (1080, G + 4)], -1, WOOD_L, 4, draw=False)]
    els += [poly([(260, G - 14), (760, G - 14), (800, G - 34), (300, G - 40)], WOOD, "rgba(255,226,180,.35)", 1.2, -1)]
    els += [grp(moai_side(0, 0, 520, -1), ts + .5, "rise", tr="translate(270 %s) rotate(90) scale(-1 1)" % round(G - 40 - .105 * 520, 1))]
    tr_ = T("sledge", "sixty Rapanui")
    pullers = []
    for row in range(2):
        for k in range(30):
            x = 900 + k * 25 + row * 12
            pullers.append(ppl(x, G + 8 + row * 18, 48 - row * 4, round(tr_ + .015 * (k + row * 30), 2), "#241b14" if row else "#2e241a"))
    els += [ln([(800, G - 30), (900, G - 22), (1660, G - 20)], tr_ - .2, "#c9a86a", 2.2, dur=.6), ln([(800, G - 22), (912, G - 6), (1672, G - 2)], tr_ - .2, "#c9a86a", 2.2, dur=.6)]
    els += pullers
    els += [lab(1290, G - 70, "60 people", tr_ + .4, BONE, 30)]
    els += chip(380, 300, "1998", GOLD, tr_ - .4, 30) + [lab(380, 370, "about 10 t", tr_, BONE, 28)]
    td = T("sledge", "nearly a hundred")
    els += [arr([(140, G + 90), (1640, G + 90)], td, AMBER, 3, "inferred", 1.2), lab(889, G + 140, "nearly 100 m", td + .4, AMBER, 28)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "cam": CAM, "els": els}


def quarry_hill(x, y, w, h, at=-1, c="#323a24", rim="rgba(255,220,170,.35)", op=None):
    """Rano Raraku from afar: a broad volcanic cone with a dipping crater rim and a pale quarried cliff on its flank."""
    p = [(x - w / 2, y), (x - w * .36, y - h * .38), (x - w * .22, y - h * .82), (x - w * .1, y - h), (x + w * .06, y - h * .9), (x + w * .16, y - h * .96),
         (x + w * .26, y - h * .7), (x + w * .36, y - h * .36), (x + w / 2, y)]
    els = [poly(p, c, rim, 1.2, at, op=op, curve=True)]
    els.append(poly([(x - w * .05, y - h * .1), (x - w * .02, y - h * .62), (x + w * .1, y - h * .7), (x + w * .14, y - h * .3), (x + w * .1, y - h * .08)],
                    "#6a6250", at=at, op=.55 if op is None else op * .55, curve=True))
    for k in range(5):
        xx = x - w * .02 + k * w * .028
        els.append(rect(xx, y - h * .5 + (k % 2) * h * .08, w * .012, h * .12, "#9a8e78", at=at, op=.7 if op is None else op * .7))
    return els


def sc_road():
    """s16: dusk: an old road runs from the quarry hill in the distance towards the viewer, a shallow dished track; on 'walked', a soft
    gold label 'the moai walked' (tradition, not graded). On 'Look at the statues', statues lying beside the road build in, seen from a
    little above: some on their backs, faces to the sky, some face down, one broken at the neck."""
    els = sky_wash("dusk", -220, 470)
    els += [gl(1460, 430, 260, -1, .35, "sun")]
    els += quarry_hill(860, 456, 640, 170, -1)
    els += [poly([(-20, 452), (1820, 452), (1820, 1020), (-20, 1020)], "#3a4428", at=-1)]
    rnd = random.Random(3)
    for k in range(60):
        x, y = rnd.uniform(0, 1780), rnd.uniform(470, 990)
        els.append(ln([(x - 4, y), (x, y - 8 - (y - 450) * .02), (x + 4, y)], -1, "#5a6a3a", 1.3, draw=False, op=.6))
    road = [(830, 456), (890, 456), (1300, 1020), (460, 1020)]
    els += [poly(road, "#5a4a36", at=-1), poly([(850, 456), (870, 456), (990, 1020), (770, 1020)], "#4a3c2c", at=-1, op=.8),
            ln([(830, 456), (460, 1020)], -1, "rgba(255,226,190,.25)", 2, draw=False), ln([(890, 456), (1300, 1020)], -1, "rgba(255,226,190,.25)", 2, draw=False)]
    tw = T("road", "statues walked")
    els += [gl(889, 210, 260, tw - .2, .3), lab(889, 216, "the moai walked", tw, GOLD, 44, st="ital"), lab(889, 262, "Rapanui tradition", tw + .4, DIM, 24)]
    tl = T("road", "Look at the statues")
    spots = [(1300, 880, 470, 96, True, False), (120, 830, 450, 84, False, True), (1110, 650, 240, 100, True, False), (560, 640, 230, 82, False, False),
             (975, 540, 120, 96, True, False), (720, 548, 112, 86, True, False)]
    for k, (x, y, h, ang, up, br) in enumerate(spots):
        t = round(tl + .3 * k, 2)
        els += [poly(E(x + .5 * h, y + 4, .55 * h, .05 * h + 3, 18), "#1a1e12", at=t, op=.45)]
        els += lying_top(x, y, h, t, ang=ang, squash=.42, up=up, broken=br)
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": False, "cam": CAM, "els": els}


def sc_compare():
    """s17: two statues in side view: left 'on a platform' (upright on a low platform, flat base, eye sockets), right 'on the road'
    (leaning forward, wide D-shaped base, no eye sockets); under each its base seen from above: a narrow rectangle, a wide D.
    'leans forward', 'D-shaped base', 'no eye sockets'."""
    G = 640
    els = [rect(-20, G, 1820, 400, "#221c15", at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,226,190,.3)", 1.5, draw=False), gl(889, 420, 760, -1, .12)]
    els += ahu(330, 630, G - 34, 34, -1) + moai_side(480, G - 34, 440, -1, sockets=True) + [lab(480, 150, "on a platform", .3, BONE, 30)]
    tl, tb, te = T("compare", "lean"), T("compare", "D-shaped"), T("compare", "eye sockets")
    els += moai_side(1150, G, 470, .3, base="D", sockets=False, lean=9, fx="fade") + [lab(1150, 150, "on the road", .3, GOLD, 30)]
    els += [arr([(1250, 200), (1300, 184), (1350, 196)], tl, AMBER, 3, dur=.4, curve=True), lab(1380, 205, "leans forward", tl + .2, AMBER, 28, "start")]
    els += [circ(1262, 236, 24, "none", AMBER, 2.5, te, fx="draw"), ln([(1288, 244), (1370, 290)], te + .1, AMBER, 2, dur=.4),
            lab(1380, 300, "no eye sockets", te + .2, AMBER, 28, "start")]
    els += [circ(545, 235 - 34 + 30, 20, "none", DIM, 2, te - .3, fx="draw")]
    els += [poly([(420, 700), (540, 700), (540, 740), (420, 740)], TUFF, TUFF_E, 1.5, tb - .2, fx="pop"), lab(480, 780, "flat base", tb, DIM, 24)]
    D = [(1080, 690)] + [(1150 + math.cos(math.radians(a)) * 80, 720 + math.sin(math.radians(a)) * 34) for a in range(-90, 91, 15)] + [(1080, 750)]
    els += [poly(D, TUFF, TUFF_E, 1.5, tb, fx="pop"), lab(1150, 790, "D-shaped base", tb + .2, AMBER, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def fridge(x, y, s, at, ang=0, op=None):
    """A fridge rocked onto one corner (ang degrees about the corner it stands on)."""
    w, h = .5 * s, s
    piv = (x + (w / 2 if ang > 0 else -w / 2), y)
    p = rot_pts([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h), (x - w / 2, y - h)], piv[0], piv[1], ang)
    d = rot_pts([(x - w / 2 + 6, y - h * .62), (x + w / 2 - 6, y - h * .62)], piv[0], piv[1], ang)
    return [poly(p, "#e8e4dc" if op is None else "none", "#cbbca8", 2, at, fx="pop", op=op), ln(d, at, "#8a8478", 2, draw=False, op=op)]


def sc_walk():
    """s18: the replica upright in a field (front view), three ropes from its head to two side teams and one behind (18 people); faint
    ghosts rocked onto one corner, then the other; a zig-zag of base prints along a dashed 100 m track. Chip '2012', '4.35 t replica',
    '18 people', '100 m in 40 min'; a small fridge rocking at the upper right."""
    G = 700
    els = sky_wash("day", -200, 560) + [hills(520, -1, "#56663a", 21, 50), rect(-20, 560, 1820, 480, "#4e5e32", at=-1)]
    cx = 889
    H = 360
    tr_, tp, tf, tw = T("walk", "In twenty twelve"), T("walk", "Eighteen people"), T("walk", "full fridge"), T("walk", "It walked")
    els += moai(cx, G, H, .3, fx="fade", light=-1)
    els += [arr([(cx - 40, G - H - 40), (cx - 110, G - H - 10)], tp + .3, GOLD, 3, dur=.4, curve=False), arr([(cx + 40, G - H - 40), (cx + 110, G - H - 10)], tp + .8, GOLD, 3, dur=.4, curve=False),
            lab(cx, G - H - 56, "side to side", tp + .5, GOLD, 26)]
    hy = G - .82 * H
    teams = [(-1, [(cx - 540 + 70 * k, G - 6 + 6 * k) for k in range(6)]), (1, [(cx + 190 + 70 * k, G + 30 - 4 * k) for k in range(6)])]
    els += [ln([(cx - 40, hy), (cx - 520, G - 70)], tr_ + .6, "#c9a86a", 2.4, dur=.5), ln([(cx + 40, hy), (cx + 560, G - 40)], tr_ + .7, "#c9a86a", 2.4, dur=.5),
            ln([(cx, hy - 10), (cx + 30, G + 120)], tr_ + .8, "#c9a86a", 2.4, dur=.5)]
    k = 0
    for sgn, spots in teams:
        for (x, y) in spots:
            els.append(ppl(x, y, 62, round(tp + .04 * k, 2), "#241b14"))
            k += 1
    for j in range(6):
        els.append(ppl(cx - 60 + 30 * j, G + 150 + (j % 2) * 10, 66, round(tp + .04 * (12 + j), 2), "#241b14"))
    els += chip(260, 180, "2012", GOLD, tr_, 30) + [lab(cx, 210, "4.35 t replica", tr_ + .3, BONE, 28)]
    els += [lab(cx - 330, G - 120, "18 people", tp + .5, BONE, 28)]
    for j in range(7):
        x = 1080 + j * 80
        y = G + 70 - j * 14
        els.append(poly(E(x + (12 if j % 2 else -12), y, 26, 9, 14), "rgba(255,236,206,.25)", "rgba(255,236,206,.5)", 1, round(tw + .1 * j, 2), fx="pop"))
    els += [arr([(1050, G + 110), (1660, G - 10)], tw, AMBER, 2.5, "inferred", 1.0), lab(1440, G + 100, "100 m in 40 min", tw + .5, AMBER, 30)]
    els += [rect(1420, 150, 270, 230, "rgba(14,12,10,.7)", "rgba(255,236,206,.3)", 2, 10, tf - .3)]
    els += fridge(1500, 340, 130, tf - .2, -10, op=.35) + fridge(1610, 340, 130, tf + .2, 10, op=.35) + fridge(1555, 340, 130, tf)
    els += [lab(1555, 186, "like a fridge", tf + .3, DIM, 24)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "cam": CAM, "els": els}


def sc_dish():
    """s19: left, the road in cross-section, a shallow dish 4.5 m wide cut into the ground, a walking statue in it ('4.5 m'); right, how
    many roadside statues lie at each distance from the quarry: a curve falling away (the exponential fall-off), the part within 2 km
    shaded ('half within 2 km')."""
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1), gl(450, 500, 600, -1, .12)]
    cx, G = 450, 640
    ground = [(-20, G - 30), (cx - 300, G - 30)] + [(cx + u, G - 30 + 54 * (1 - (u / 260.0) ** 2)) for u in range(-260, 261, 20)] + [(cx + 300, G - 30), (880, G - 30),
                                                                                                                               (880, 1020), (-20, 1020)]
    els += [poly(ground, "#4a3c2c", "rgba(255,226,190,.5)", 2, -1), rect(-20, G - 30, 900, 400, "url(#k-speck)", at=-1)]
    for k in range(3):
        yy = G + 40 + k * 50
        els.append(ln([(-20, yy), (880, yy + 4)], -1, "rgba(255,226,190,.12)", 1.4, "inferred", draw=False))
    els += moai(cx, G + 24, 330, .5, fx="fade", light=-1)
    tw_ = T("dish", "four and a half")
    els += [{"k": "dim", "x1": cx - 260, "y1": G + 90, "x2": cx + 260, "y2": G + 90, "t": "4.5 m", "c": GOLD, "in": tw_, "fx": "draw", "dur": .7, "ly": 40}]
    els += [lab(cx, 200, "dished like a bowl", T("dish", "dished"), BONE, 28)]
    x0, x1, y0, y1 = 1000, 1660, 680, 260
    X = lambda d: x0 + (x1 - x0) * d / 10
    Y = lambda f: y0 - (y0 - y1) * f
    th = T("dish", "half the roadside")
    els += [axis(x0, x1, y0, [(X(d), str(d)) for d in (0, 2, 4, 6, 8, 10)], th - 1.0, "km from the quarry")]
    lam = math.log(1 / (1 - .516)) / 2
    pts = [(X(d / 10), Y(math.exp(-lam * d / 10))) for d in range(0, 101)]
    shade = [(X(0), y0)] + [(X(d / 10), Y(math.exp(-lam * d / 10))) for d in range(0, 21)] + [(X(2), y0)]
    els += [poly(shade, "rgba(242,201,142,.35)", at=th + .6, fx="fade"), ln(pts, th - .6, GOLD, 4, dur=1.2, curve=True),
            ln([(X(2), y0), (X(2), Y(math.exp(-lam * 2)) - 10)], th + .6, "rgba(242,201,142,.8)", 2, "inferred", .4),
            lab(X(2) + 16, Y(.55), "half within 2 km", th + .8, GOLD, 30, "start"), lab(x0, y1 - 40, "statues by the road", th - .8, DIM, 26, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def rope_coil(x, y, r, at):
    return [circ(x, y, r * (1 - .18 * k), "none", "#c9a86a", 5, round(at + .05 * k, 2), fx="draw") for k in range(4)]


def sc_doubts():
    """s20: a road across the bottom with a statue lying beside it; then, left, a statue standing on a little platform beside the road, in
    lilac dashes ('set up on purpose?'); middle, the small replica beside a huge dashed outline of Paro ('80 t: not yet tried'); right, a
    coil of rope (solid) and a stack of logs (dashed, struck through)."""
    G = 700
    els = [rect(-20, G, 1820, 340, "#221c15", at=-1), rect(-20, G + 30, 1820, 60, "#3a2e22", at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,226,190,.3)", 1.5, draw=False),
           gl(889, 420, 760, -1, .1)]
    els += [poly(E(560, G + 2, 120, 8, 16), "#120e0b", at=-1, op=.5)] + lying(560, G, 230, -1, up=True, base="D", sockets=False, fx=None)
    tp, t80, tr_ = T("doubts", "on purpose"), T("doubts", "eighty tonnes"), T("doubts", "rope and")
    els += [poly([(140, G), (420, G), (420, G - 40), (140, G - 40)], "rgba(201,193,238,.08)", LILAC, 2.4, tp - .3, style="inferred", fx="pop")]
    els += moai(280, G - 40, 300, tp - .1, style="inferred", fx="pop")
    els += [lab(280, 300, "set up on purpose?", tp + .2, LILAC, 28)]
    els += moai(960, G, 9.8 * 55 * .8, t80 - .2, style="inferred", fx="pop") + moai(800, G, 4.0 * 55 * .8 + 40, t80 - .4, light=-1, fx="pop")
    els += [lab(960, 230, "80 t: untested", t80 + .2, BONE, 28), lab(800, G + 40, "4.35 t", t80, DIM, 24)]
    els += rope_coil(1340, 560, 70, tr_) + [lab(1340, 680, "rope", tr_ + .2, BONE, 28)]
    logs = []
    for r_ in range(3):
        for k in range(3 - r_):
            logs.append(circ(1520 + k * 56 + r_ * 28, 620 - r_ * 50, 26, "rgba(245,236,220,.05)", BONE, 2.2, tr_ + .6, style="inferred", fx="pop"))
    els += logs + [I.strike(1470, 660, 1700, 500, tr_ + 1.0, RED, 6), lab(1580, 690, "rollers", tr_ + .7, DIM, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def book(x, y, w, h, at, title, sub, c="#7a3a2a", tc="#f5ecdc", fx="rise"):
    """A hardback book standing a little turned: its cover with a title and a line under it, the spine's shadow."""
    return [rect(x + 10, y + 14, w, h, "rgba(0,0,0,.45)", at=at, fx=fx), rect(x, y, w, h, c, "rgba(255,236,206,.35)", 1.5, 4, at, fx=fx),
            rect(x, y, w * .08, h, "rgba(0,0,0,.25)", at=at, fx=fx),
            label(round(x + w / 2, 1), round(y + h * .34, 1), title, round(at + .1, 2), tc, 40, "middle", "serif", halo=False, scl=True),
            ln([(x + w * .25, y + h * .42), (x + w * .75, y + h * .42)], at + .1, tc, 2, draw=False, op=.6),
            label(round(x + w / 2, 1), round(y + h * .54, 1), sub, round(at + .1, 2), tc, 24, "middle", "lab", halo=False, scl=True)]


def bowl_icon(x, y, s, at, c=LILAC, style="claimed"):
    return [poly([(x - s, y - .3 * s), (x + s, y - .3 * s), (x + .6 * s, y + .3 * s), (x - .6 * s, y + .3 * s)], "rgba(201,193,238,.06)", c, 2.4, at, style=style, fx="pop")]


def crack_icon(x, y, s, at, c=LILAC, style="claimed"):
    return [rect(x - s, y - .4 * s, 2 * s, .8 * s, "rgba(201,193,238,.06)", c, 2.4, 4, at, fx="pop", style=style),
            ln([(x - .6 * s, y - .4 * s), (x - .2 * s, y), (x - .4 * s, y + .4 * s)], at, c, 2, style, draw=False),
            ln([(x + .3 * s, y - .4 * s), (x + .1 * s, y - .05 * s), (x + .5 * s, y + .4 * s)], at, c, 2, style, draw=False)]


def stump_icon(x, y, s, at, c=LILAC, style="claimed"):
    return [poly([(x - .5 * s, y), (x - .4 * s, y - .7 * s), (x - .1 * s, y - .8 * s), (x + .2 * s, y - .65 * s), (x + .4 * s, y - .75 * s), (x + .5 * s, y)],
                 "rgba(201,193,238,.06)", c, 2.4, at, style=style, fx="pop")]


YX = lambda yr: round(640 + (yr - 1200) / 600 * 1000, 1)        # years 1200 to 1800 on the panels of chapter 3


def sc_collapse():
    """s21: the book at the left (a cover 'Collapse', '2005'); at the right the story's population curve in lilac dots (a claim): rising
    to '15,000 or more?' then crashing at 'about 1680', before a ship mark at 1722; icons along the fall as named: a stump, a cracked
    field, an empty bowl, crossed spears; 'destroyed itself?'."""
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1), gl(889, 460, 760, -1, .12)]
    els += book(140, 220, 300, 420, -1, "Collapse", "2005")
    y0, y1 = 700, 230
    Y = lambda n: y0 - (y0 - y1) * n / 16000
    els += [axis(YX(1200), YX(1800), y0, [(YX(y), str(y)) for y in (1200, 1400, 1600, 1800)], -1, "years CE")]
    tp, tg, ts, th, tw, t80, td = (T("collapse", "Perhaps fifteen"), T("collapse", "forest goes"), T("collapse", "soil fails"), T("collapse", "hunger"),
                                   T("collapse", "war follow"), T("collapse", "sixteen eighty"), T("collapse", "destroyed"))
    rise = [(YX(1200), Y(50)), (YX(1300), Y(900)), (YX(1400), Y(3500)), (YX(1500), Y(9000)), (YX(1580), Y(14000)), (YX(1630), Y(15500))]
    fall = [(YX(1630), Y(15500)), (YX(1660), Y(12000)), (YX(1680), Y(6000)), (YX(1700), Y(2600)), (YX(1722), Y(2200))]
    els += [ln(rise, tp - .6, LILAC, 4, "claimed", 1.4, curve=True), lab(YX(1600), Y(15500) - 40, "15,000 or more?", tp + .4, LILAC, 30, "end")]
    els += [ln(fall, tg - .2, LILAC, 4, "claimed", 1.6, curve=True)]
    els += stump_icon(YX(1640) + 60, Y(13000), 44, tg) + crack_icon(YX(1660) + 70, Y(10000), 30, ts) + bowl_icon(YX(1680) + 70, Y(7000), 30, th)
    els += spear(YX(1700) + 30, Y(4200), YX(1700) + 110, Y(5600), tw) + spear(YX(1700) + 110, Y(4200), YX(1700) + 30, Y(5600), tw + .1)
    els += [ln([(YX(1680), y0), (YX(1680), Y(6000))], t80, "rgba(201,193,238,.6)", 2, "claimed", .4), lab(YX(1680), y0 + 90, "about 1680", t80, LILAC, 28)]
    els += [ln([(YX(1722), y0), (YX(1722), y1 + 40)], t80 + .4, GOLD, 2, "inferred", .5)] + ship_icon(YX(1722), y1 + 30, 50, t80 + .5, GOLD)
    els += [lab(YX(1420), Y(12500), "destroyed itself?", td, LILAC, 30, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def hare(x, y, w, at, fx=None, op=None):
    """A boat-shaped house (hare paenga): a long low thatched hull on a stone footing, a small door."""
    h = w * .32
    els = [poly([(x - w / 2, y), (x - w * .46, y - h * .5), (x - w * .3, y - h * .9), (x, y - h), (x + w * .3, y - h * .9), (x + w * .46, y - h * .5),
                 (x + w / 2, y)], "#6a5a3a", "rgba(255,226,180,.35)", 1.2, at, fx=fx, op=op, curve=True),
           rect(x - w * .5, y - 6, w, 8, "#4a4440", at=at, fx=fx, op=op), rect(x - w * .05, y - h * .45, w * .1, h * .45, "#1a1410", at=at, fx=fx, op=op)]
    for k in range(5):
        xx = x - w * .36 + k * w * .18
        els.append(ln([(xx, y - h * .2), (xx + w * .04, y - h * .8)], at, "#4a3e2a", 1.2, draw=False, op=op))
    return els


def sc_dates():
    """s22: left, boat-shaped houses with hearths; charcoal flecks rise from the fires and fly into an open drawer of receipts (the
    analogy). Right, radiocarbon dates by century 1200 to 1800, marks stacking into a curve that climbs steadily up to the line at 1722
    ('charcoal dates', '1722')."""
    G = 560
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1), gl(360, 420, 520, -1, .14)]
    els += [poly([(-20, G + 10), (120, G - 6), (420, G), (640, G + 16), (660, 1020), (-20, 1020)], "#2a2a1c", at=-1, curve=True)]
    els += hare(170, G, 230, -1) + hare(440, G + 14, 210, -1)
    tc, td, tp = T("dates", "leaves charcoal"), T("dates", "receipts"), T("dates", "Pile up")
    for (fx_, fy_) in ((300, G + 2), (560, G + 16)):
        els += [gl(fx_, fy_ - 20, 70, -1, .5, "fire"), poly([(fx_ - 12, fy_), (fx_, fy_ - 30), (fx_ + 12, fy_)], "#ffb060", at=-1)]
    rnd = random.Random(4)
    for k in range(14):
        sx, sy = (300, G - 30) if k % 2 == 0 else (560, G - 14)
        t = round(tc + .12 * k, 2)
        ex, ey = 360 + rnd.uniform(-60, 60), 330 + rnd.uniform(-30, 30)
        els += [dot(round(sx + (ex - sx) * .5 + rnd.uniform(-20, 20), 1), round(sy + (ey - sy) * .5 - 40, 1), 4, "#2a2420", t), dot(round(ex, 1), round(ey, 1), 4, "#1a1612", round(t + .3, 2))]
    els += [rect(240, 260, 240, 110, WOOD, "rgba(255,226,180,.4)", 1.5, 4, td - .6, fx="rise"), rect(256, 250, 208, 40, "#1a1410", at=td - .6, fx="rise")]
    for k in range(6):
        els.append(rect(266 + k * 32, 214 - (k % 3) * 8, 26, 50, "#efe6d2", "#bba890", 1, 2, round(td - .4 + .06 * k, 2), fx="rise"))
    els += [lab(360, 410, "like receipts", td, DIM, 24)]
    x0, x1, y0, y1 = 760, 1660, 600, 200
    X = lambda yr: x0 + (x1 - x0) * (yr - 1200) / 600
    els += [axis(x0, x1, y0, [(X(y), str(y)) for y in (1200, 1400, 1600, 1800)], -1, "years CE")]
    for k in range(12):
        bx = X(1212 + 43.5 * k)
        for j in range(k + 1):
            els.append(rect(bx - 15, y0 - 8 - 30 * (j + 1), 30, 26, AMBER, at=round(tp + .05 * k + .03 * j, 2), fx="pop", op=.85))
    els += [ln([(X(1722), y0), (X(1722), y1 - 30)], -1, GOLD, 2, "inferred", draw=False)] + ship_icon(X(1722), y1 - 44, 50, -1, GOLD)
    tcl = T("dates", "climb steadily")
    els += [arr([(X(1230), y0 - 70), (X(1520), y0 - 220), (X(1700), y0 - 380)], tcl, GOLD, 3, dur=1.0, curve=True),
            lab(X(1250), y1 + 20, "charcoal dates", tp, BONE, 28, "start"), lab(X(1722) + 14, y1 + 30, "1722", -1, GOLD, 26, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def ahu_icon(x, y, s, at, c=TUFF_L):
    return [rect(x - s, y - .3 * s, 2 * s, .3 * s, "#4a4440", "rgba(255,236,206,.4)", 1, 1, at, fx="pop")] + \
           [moai_mark(x + dx * s, y - .3 * s, .9 * s, at, c) for dx in (-.55, 0, .55)]


def add_ahu():
    """s23 (on the dates panel): under the chart, a row of platform icons pops along the time line, the last ones after the 1722 line;
    'platforms still built'."""
    x0, x1 = 760, 1660
    X = lambda yr: x0 + (x1 - x0) * (yr - 1200) / 600
    els = [rect(740, 712, 940, 92, "rgba(14,12,10,.88)", "rgba(255,236,206,.25)", 1.5, 8, .2)]
    for k, yr in enumerate((1320, 1380, 1440, 1500, 1560, 1620, 1680, 1735, 1760)):
        els += ahu_icon(X(yr), 784, 22, round(.4 + .14 * k, 2), GOLD if yr > 1722 else TUFF_L)
    els += [lab(X(1722) + 10, 736, "after 1722", 1.6, GOLD, 24, "start")]
    els += [lab(X(1300), 734, "platforms still built", T("ahu", "still being built"), BONE, 26, "start")]
    return els


def sc_gardens():
    """s24: left, a rock garden in section: broken stones over brown soil, sweet potato leaves between them; small arrows 'keeps it damp'
    and 'minerals'. Right, a satellite; under it an infrared view of the ground where garden patches glow; beside it a small dry lawn
    with one watered patch (the analogy)."""
    G = 560
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1), gl(420, 520, 600, -1, .14)]
    els += [rect(60, G, 760, 240, SOIL, at=-1), rect(60, G, 760, 240, "url(#k-speck)", at=-1), ln([(60, G), (820, G)], -1, "rgba(255,226,190,.3)", 1.5, draw=False)]
    rnd = random.Random(8)
    tk, tm = T("gardens", "keep the soil"), T("gardens", "minerals")
    for k in range(26):
        x = 80 + k * 28 + rnd.uniform(-6, 6)
        r = rnd.uniform(14, 24)
        els.append(poly([(x + math.cos(a) * r * rnd.uniform(.7, 1.1), G - r * .5 + math.sin(a) * r * .6) for a in [i * math.pi / 3 for i in range(6)]],
                        "#6e6a64", "rgba(255,236,206,.35)", 1, -1))
    for k in range(6):
        x = 130 + k * 120
        els += [ln([(x, G - 10), (x, G - 60)], -1, "#4a7a3a", 3, draw=False)]
        for s in (-1, 1):
            els.append(poly(E(x + s * 22, G - 62, 20, 12, 12), "#5a8a44", "#8ab86a", 1, -1))
    els += [lab(440, 230, "a rock garden", -1, DIM, 26)]
    for k in range(5):
        x = 150 + k * 140
        els.append(arr([(x, G - 120), (x, G + 30)], round(tk + .1 * k, 2), BLUE, 2.4, "known", .5))
    els += [lab(440, G - 150, "keeps it damp", tk + .2, BLUE, 28)]
    for k in range(4):
        x = 200 + k * 150
        els.append(arr([(x, G + 20), (x + 10, G + 140)], round(tm + .1 * k, 2), GOLD, 2.4, "known", .5))
    els += [lab(440, G + 200, "minerals", tm + .2, GOLD, 28)]
    ts, ti, tl = T("gardens", "from space"), T("gardens", "infrared"), T("gardens", "watered patch")
    els += [rect(1200, 150, 90, 50, "#8a96a2", "#cbd6e0", 1.5, 4, ts - .8, fx="pop"), rect(1130, 165, 60, 22, "#3a5a8a", at=ts - .8, fx="pop"),
            rect(1300, 165, 60, 22, "#3a5a8a", at=ts - .8, fx="pop"), ln([(1245, 200), (1170, 330)], ts - .5, "rgba(159,208,255,.5)", 2, "inferred", .5),
            ln([(1245, 200), (1330, 330)], ts - .5, "rgba(159,208,255,.5)", 2, "inferred", .5)]
    ix, iy, iw, ih = 1040, 330, 420, 300
    els += [rect(ix, iy, iw, ih, "#3a1f2e", "rgba(255,236,206,.35)", 2, 8, ti - .4)]
    for k in range(40):
        els.append(circ(ix + rnd.uniform(14, iw - 14), iy + rnd.uniform(14, ih - 14), rnd.uniform(4, 9), "#6a3a50", at=ti - .4, op=.6))
    for k in range(9):
        cx_, cy_ = ix + rnd.uniform(40, iw - 40), iy + rnd.uniform(40, ih - 40)
        els += [gl(cx_, cy_, 40, round(ti + .1 * k, 2), .6, "lamp"), poly(E(cx_, cy_, rnd.uniform(14, 24), rnd.uniform(10, 16), 12), "#ffd38a", at=round(ti + .1 * k, 2),
                                                                         op=.85, fx="pop")]
    els += [lab(ix + iw / 2, iy + ih + 40, "gardens glow in infrared", ti + .4, BONE, 26)]
    lx, ly_ = 1520, 380
    els += [rect(lx, ly_, 200, 200, "#8a7a4a", "rgba(255,236,206,.35)", 2, 8, tl - .4), poly(E(lx + 100, ly_ + 100, 52, 40, 18), "#4a7a3a", at=tl, fx="pop"),
            lab(lx + 100, ly_ + 240, "a watered patch", tl + .2, BONE, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def poly_area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2


RNV_AREA = View(-109.47, -109.20, -27.215, -27.045, (110, 170, 900, 540))


def sc_area():
    """s25: the island: a big dashed area, 'up to 21 km2' (earlier estimates, drawn at 21 of 164 km2 of the island), then the mapped gardens
    as small solid patches, '0.76 km2' (drawn at their true share). Right: 30 small figures pop, each for 100 people, 'about 3,000', beside
    a ship tag '1722 reports'."""
    v = RNV_AREA
    els = island(v, -1, fill="#4e5a34")
    P = [v.p(lo, la) for lo, la in RN]
    A = poly_area(P)
    te, tm, tp = T("area", "Earlier estimates"), T("area", "less than"), T("area", "three thousand")
    # earlier estimate: a dashed blob of 21/164 of the island's area, inland
    r = math.sqrt(A * 21 / 164 / math.pi)
    cx_, cy_ = v.p(-109.345, -27.118)
    blob = [(cx_ + math.cos(a) * r * 1.35, cy_ + math.sin(a) * r / 1.35) for a in [i * math.pi / 14 for i in range(28)]]
    els += [poly(blob, "rgba(242,201,142,.18)", GOLD, 2.5, te, style="inferred", fx="pop", curve=True), lab(cx_, cy_ - r / 1.35 - 22, "up to 21 km²", te + .3, GOLD, 30)]
    # the mapped gardens: 30 patches whose total area is 0.76/164 of the island's
    rnd = random.Random(12)
    each = A * .76 / 164 / 30
    rr = math.sqrt(each / math.pi)
    k = 0
    while k < 30:
        q = (rnd.uniform(min(p[0] for p in P), max(p[0] for p in P)), rnd.uniform(min(p[1] for p in P), max(p[1] for p in P)))
        if pip(q, P):
            els.append(circ(q[0], q[1], rr, "#fff1c2", "#ffd38a", 1, round(tm + .03 * k, 2), fx="pop"))
            k += 1
    els += [lab(560, 760, "mapped in 2024: 0.76 km²", tm + .4, "#ffd38a", 28)]
    for k in range(30):
        x, y = 1180 + (k % 6) * 66, 300 + (k // 6) * 86
        els.append(ppl(x, y, 62, round(tp + .04 * k, 2), BONE))
    els += [lab(1345, 760 - 10 - 40, "about 3,000", tp + .6, BONE, 32), lab(1345, 752, "each figure: 100 people", tp + .8, DIM, 24)]
    els += tag(1345, 210, "1722 reports", tp + 1.4, GOLD, 26)
    return {"base": "map", "cam": CAM, "els": els}


def sc_critics():
    """s26: the island map again on its own panel: the uplands outlined in dashes ('missed gardens?'), the dry northwest shaded ('use fell
    after 1650'); at the right the story's lilac crash curve, then a solid gold line, rising gently, without a crash."""
    v = View(-109.47, -109.20, -27.215, -27.045, (90, 200, 780, 500))
    els = island(v, -1, fill="#4e5a34")
    tu, tn, ts, tc = T("critics", "upland"), T("critics", "dry northwest"), T("critics", "Strain"), T("critics", "great crash")
    up = [v.p(lo, la) for lo, la in [(-109.405, -27.09), (-109.37, -27.075), (-109.345, -27.085), (-109.36, -27.115), (-109.395, -27.12)]]
    els += [poly(up, "rgba(242,201,142,.12)", GOLD, 2.5, tu, style="inferred", fx="pop", curve=True), lab(sum(p[0] for p in up) / 5, min(p[1] for p in up) - 22, "missed gardens?", tu + .3, GOLD, 26)]
    nw = [v.p(lo, la) for lo, la in [(-109.424, -27.118), (-109.418, -27.100), (-109.408, -27.084), (-109.394, -27.071), (-109.40, -27.10), (-109.41, -27.12)]]
    els += [poly(nw, "rgba(255,138,122,.35)", RED, 2, tn, fx="pop", curve=True), lab(140, 180, "dry northwest:", tn + .2, "#ffb0a0", 26, "start"),
            lab(140, 214, "use fell after 1650", tn + .3, "#ffb0a0", 26, "start")]
    x0, x1, y0, y1 = 1000, 1660, 660, 260
    X = lambda yr: x0 + (x1 - x0) * (yr - 1200) / 600
    Y = lambda f: y0 - (y0 - y1) * f
    els += [axis(x0, x1, y0, [(X(y), str(y)) for y in (1200, 1400, 1600, 1800)], .3, "years CE")]
    crash = [(X(1200), Y(.02)), (X(1400), Y(.25)), (X(1580), Y(.92)), (X(1630), Y(.96)), (X(1680), Y(.4)), (X(1720), Y(.14))]
    els += [ln(crash, .4, LILAC, 3, "claimed", 1.0, curve=True, op=.6)]
    steady = [(X(1200), Y(.02)), (X(1300), Y(.09)), (X(1400), Y(.16)), (X(1500), Y(.22)), (X(1600), Y(.26)), (X(1722), Y(.30))]
    els += [ln(steady, ts, GOLD, 5, dur=1.4, curve=True), lab(x0, y1 - 20, "no great crash", tc, GOLD, 30, "start")]
    els += [I.strike(X(1560), Y(.98), X(1700), Y(.36), tc + .3, RED, 5)]
    return {"base": "map", "cam": CAM, "els": els}


def helix(x0, x1, y, amp, at, c1=GOLD, c2=AMBER, dur=1.4, rungs=14):
    n = 60
    p1 = [(x0 + (x1 - x0) * k / n, y + amp * math.sin(k / n * 4 * math.pi)) for k in range(n + 1)]
    p2 = [(x0 + (x1 - x0) * k / n, y - amp * math.sin(k / n * 4 * math.pi)) for k in range(n + 1)]
    els = [ln(p1, at, c1, 4, dur=dur, curve=True), ln(p2, at + .1, c2, 4, dur=dur, curve=True)]
    for k in range(rungs):
        t = (k + .5) / rungs
        x = x0 + (x1 - x0) * t
        a = amp * math.sin(t * 4 * math.pi)
        els.append(ln([(x, y + a), (x, y - a)], round(at + dur * t, 2), "rgba(255,236,206,.5)", 2, draw=False))
    return els


def sc_museum():
    """s27: a quiet museum store: fifteen small boxes on shelves, each with a soft warm light (no bones drawn); a DNA double helix draws
    itself in gold above them (chip '2024'); a time bar '1670 to 1950'; then a gentle line links the fifteen lights to a group of
    present-day Rapanui ('closest kin')."""
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1), gl(560, 520, 600, -1, .14)]
    for r_ in range(3):
        y = 400 + r_ * 130
        els += [rect(160, y + 70, 800, 12, "#4a3a2a", "rgba(255,226,180,.3)", 1, 2, -1)]
        for k in range(5):
            x = 200 + k * 150
            els += [rect(x, y, 110, 70, "#6a5a48", "rgba(255,236,206,.35)", 1.2, 4, -1), rect(x + 30, y + 22, 50, 22, "#efe6d2", at=-1, op=.7)]
    tg, td, tk = T("museum", "read their"), T("museum", "sixteen seventy"), T("museum", "closest kin")
    for r_ in range(3):
        for k in range(5):
            x, y = 255 + k * 150, 400 + r_ * 130 - 18
            els += [gl(x, y, 40, round(tg - .6 + .05 * (r_ * 5 + k), 2), .6), dot(x, y, 5, "#ffe2a8", round(tg - .6 + .05 * (r_ * 5 + k), 2))]
    els += helix(180, 940, 250, 46, tg) + chip(1040, 250, "2024", GOLD, tg + .2, 28)
    els += [bar(180, 940, 860, 10, td, AMBER, 1.0), lab(180, 836, "1670", td, AMBER, 26, "start"), lab(940, 836, "1950", td + .6, AMBER, 26, "end")]
    for k in range(5):
        els.append(ppl(1330 + k * 70, 720 - (k % 2) * 8, 110 - (k % 3) * 10, round(tk - .4 + .1 * k, 2), "#cbbca8"))
    els += [ln([(980, 530), (1160, 560), (1300, 640)], tk - .6, "rgba(255,226,168,.6)", 2.5, dur=.8, curve=True), lab(1470, 520, "closest kin", tk, GOLD, 30),
            lab(1470, 790, "Rapanui today", tk + .3, DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


BEAD_COLS = ["#e8b87a", "#9fd0ff", "#8fd9b0", "#ff8a7a", "#c9c1ee", "#f2c98e", "#cbbca8", "#7fd1d4", "#d98ab0", "#a6d98f"]


def jar(x, y, w, h, at):
    return [poly([(x - w / 2, y - h), (x - w / 2 + 8, y - h + 16), (x - w / 2 + 6, y), (x + w / 2 - 6, y), (x + w / 2 - 8, y - h + 16), (x + w / 2, y - h)],
                 "rgba(200,230,240,.06)", "rgba(220,240,250,.6)", 2, at, fx="pop")]


def sc_beads():
    """s28: left, a jar of many-coloured beads; one handful goes into a new jar, which fills with only a few colours ('after a crash').
    Right, the genomes' population line from 1200 to 1750: a dashed lilac pinch at the 1600s is drawn and struck through ('no
    squeeze'), then the solid gold line rises steadily to 1722."""
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1), gl(420, 520, 560, -1, .12)]
    rnd = random.Random(6)
    els += jar(240, 640, 220, 280, -1)
    for k in range(70):
        els.append(circ(150 + rnd.uniform(0, 180), 640 - 14 - rnd.uniform(0, 230), 9, rnd.choice(BEAD_COLS), at=-1))
    ts, tr_ = T("beads", "Rebuild"), T("beads", "one handful")
    hand = [BEAD_COLS[0], BEAD_COLS[1], BEAD_COLS[0], BEAD_COLS[2], BEAD_COLS[1]]
    for k, c in enumerate(hand):
        els.append(circ(400 + k * 18, 380 - (k % 2) * 14, 9, c, at=round(ts + .1 * k, 2), fx="pop"))
    els += [arr([(370, 420), (470, 360), (560, 420)], ts + .4, BONE, 2.4, dur=.6, curve=True)]
    els += jar(620, 640, 220, 280, tr_ - .4)
    for k in range(60):
        els.append(circ(530 + rnd.uniform(0, 180), 640 - 14 - rnd.uniform(0, 210), 9, rnd.choice(hand[:3]), at=round(tr_ + .02 * k, 2)))
    els += [lab(620, 720, "after a crash", tr_ + .6, BONE, 28), lab(240, 720, "before", .5, DIM, 26)]
    x0, x1, y0, y1 = 980, 1660, 640, 260
    X = lambda yr: x0 + (x1 - x0) * (yr - 1200) / 550
    Y = lambda f: y0 - (y0 - y1) * f
    tn, tg = T("beads", "no such squeeze"), T("beads", "growing steadily")
    els += [axis(x0, x1, y0, [(X(y), str(y)) for y in (1200, 1400, 1600, 1750)], tn - 1.2, "years CE"), lab(x0, y1 - 30, "the genomes' population", tn - 1.0, DIM, 26, "start")]
    pinch = [(X(1500), Y(.5)), (X(1580), Y(.55)), (X(1630), Y(.12)), (X(1680), Y(.2)), (X(1720), Y(.3))]
    els += [ln(pinch, tn - .4, LILAC, 3, "claimed", .9, curve=True), I.strike(X(1580), Y(.66), X(1700), Y(.06), tn + .5, RED, 5),
            lab(X(1560), Y(.06), "no squeeze", tn + .6, RED, 28, "end")]
    grow = [(X(1200), Y(.05)), (X(1300), Y(.18)), (X(1400), Y(.3)), (X(1500), Y(.45)), (X(1600), Y(.6)), (X(1722), Y(.78))]
    els += [ln(grow, tg, GOLD, 5, dur=1.4, curve=True), lab(X(1722) - 10, Y(.78) - 26, "steady growth", tg + 1.2, GOLD, 28, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


AMV = View(-115.0, -64.0, -45.0, -5.0, (860, 130, 820, 640))


def sc_americas():
    """s29: left, a 10 by 10 grid of squares, 10 of them turning amber ('about a tenth'). Right, Rapa Nui and the coast of South America,
    a dashed arc with arrowheads at both ends between them ('3,500 km'), chip '1250 to 1430'."""
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1)]
    tt, td, tc = T("americas", "About a tenth"), T("americas", "twelve fifty"), T("americas", "Someone crossed")
    gx, gy, p = 140, 200, 50
    for k in range(100):
        x, y = gx + (k % 10) * p, gy + (k // 10) * p
        am = k in (7, 18, 26, 33, 45, 52, 61, 74, 88, 96)
        els.append(rect(x, y, p - 8, p - 8, "#7a8a9a", at=round(.3 + .006 * k, 3), fx="pop", r=5, op=.55))
        if am:
            els.append(rect(x, y, p - 8, p - 8, AMBER, at=round(tt + .12 * (k % 10), 2), fx="pop", r=5))
    els += [lab(gx + 5 * p - 4, gy + 10 * p + 50, "a tenth Native American", tt + 1.2, AMBER, 28)]
    v = AMV
    els += [rect(840, 120, 860, 660, "#10232e", at=-1), {"k": "group", "clip": [840, 120, 860, 660, 8], "els": [pacific_land(v, -1)], "in": -1},
            rect(840, 120, 860, 660, "none", "rgba(255,236,206,.3)", 2, 8, -1)]
    rx, ry = v.p(-109.35, -27.12)
    cx_, cy_ = v.p(-74.0, -20.0)
    els += [gl(rx, ry, 60, -1, .6), circ(rx, ry, 7, GOLD, "#fff6e6", 2, -1), lab(rx, ry + 40, "Rapa Nui", -1, GOLD, 26), lab(cx_ + 10, cy_ - 160, "South America", -1, SAND_E, 26, st="ital")]
    mid = ((rx + cx_) / 2, ry - 170)
    els += [arr([(rx + 10, ry - 10), mid, (cx_ - 10, cy_ - 6)], tc, AMBER, 3, "inferred", 1.2, curve=True),
            arr([(cx_ - 10, cy_ - 6), mid, (rx + 10, ry - 10)], tc + .6, AMBER, 3, "inferred", 1.2, curve=True),
            lab(mid[0], mid[1] - 20, "3,500 km", tc + .8, AMBER, 30)]
    els += chip(1270, 730 - 20, "1250 to 1430", GOLD, td, 28)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_home():
    """s30: left, '2017': five small dots with thin data bars; '2024': fifteen dots with long full bars. Then fifteen small warm lights
    travel along a dotted arc across the ocean towards the island ('home')."""
    els = [rect(-20, -20, 1820, 1040, "#16130f", at=-1)]
    t7, t4, th = T("home", "A smaller study"), T("home", "far more"), T("home", "bring the fifteen")
    els += [lab(150, 230, "2017", t7, DIM, 30, "start")]
    for k in range(5):
        els += [dot(170 + k * 36, 290, 9, DIM, round(t7 + .1 * k, 2)), bar(170 + k * 36 - 4, 170 + k * 36 + 4, 330, 30, round(t7 + .3 + .1 * k, 2), "rgba(203,188,168,.5)", .3)]
    els += [lab(150, 450, "2024", t4, GOLD, 30, "start")]
    for k in range(15):
        x = 170 + k * 36
        els += [dot(x, 510, 9, GOLD, round(t4 + .05 * k, 2)), ln([(x, 540), (x, 680)], round(t4 + .2 + .03 * k, 2), AMBER, 8, dur=.5)]
    els += [lab(450, 740, "far more DNA", t4 + .8, AMBER, 28)]
    sea = [(900, 120, 800, 660)]
    els += [rect(900, 120, 800, 660, "#10232e", "rgba(255,236,206,.25)", 2, 10, -1)] + waves_band(920, 1680, 300, -1, 30, op=.2) + waves_band(920, 1680, 560, -1, 30, op=.15, seed=7)
    ix, iy = 1560, 600
    els += [poly([(ix - 60, iy + 20), (ix - 10, iy - 40), (ix + 70, iy + 10), (ix + 20, iy + 40)], "#56653a", "#c9d29a", 1.5, -1, curve=True), lab(ix, iy + 90, "Rapa Nui", -1, DIM, 24)]
    path = [(980, 220), (1150, 200), (1330, 300), (1470, 460), (ix - 10, iy - 10)]
    els += [ln(path, th - .4, "rgba(255,226,168,.5)", 2.5, "claimed", 1.2, curve=True)]
    for k in range(15):
        t = (k + 1) / 16
        a = path[0] if t == 0 else None
        seg = t * (len(path) - 1)
        i = min(int(seg), len(path) - 2)
        f = seg - i
        x = path[i][0] + (path[i + 1][0] - path[i][0]) * f
        y = path[i][1] + (path[i + 1][1] - path[i][1]) * f
        els += [gl(x, y, 26, round(th + .08 * k, 2), .6), dot(round(x, 1), round(y, 1), 5, "#ffe2a8", round(th + .08 * k, 2))]
    els += [gl(ix, iy, 120, th + 1.4, .45), lab(ix - 40, iy - 70, "home", th + 1.4, GOLD, 34)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_dutch():
    """s31: morning, seen from inland: a row of moai standing on a platform, backs to the sea; beyond them three Dutch sailing ships at
    anchor (chip '1722'); people on the shore. On 'shots ring out', a puff of musket smoke by a landing boat; then twelve small lights on
    the shore go out, quietly ('about a dozen killed'). No bodies drawn."""
    G = 700
    els = sky_wash("day", -200, 520)
    els += [rect(-20, 470, 1820, 140, SEA, at=-1), rect(-20, 470, 1820, 140, "url(#k-water)", at=-1, op=.5)] + waves_band(0, 1780, 480, -1, 26, op=.25)
    els += ship(330, 500, 230, -1, None, c="#2a2018", sail="#e8dcc0", flag="#c84a3a") + ship(1480, 494, 250, -1, None, c="#2a2018", sail="#e8dcc0", flag="#c84a3a")
    els += ship(1180, 486, 160, -1, None, c="#2a2018", sail="#e8dcc0", flag="#c84a3a")
    els += [poly([(-20, 600), (400, 590), (900, 600), (1400, 588), (1820, 600), (1820, 1020), (-20, 1020)], "#4e5a34", at=-1),
            poly([(-20, 600), (400, 590), (900, 600), (1400, 588), (1820, 600), (1820, 618), (-20, 618)], "#d8ccb0", at=-1, op=.6)]
    els += ahu(520, 1260, G - 36, 36, -1)
    for k, x in enumerate((600, 735, 870, 1005, 1140)):
        els += moai(x, G - 36, 250, -1, light=1, lichen=0)
    els += chip(200, 200, "1722", GOLD, .4, 30)
    tp, ts, tk = T("dutch", "people on"), T("dutch", "shots ring out"), T("dutch", "killed")
    crowd = [(140, 640), (200, 652), (260, 644), (1330, 650), (1390, 640), (1450, 655), (1510, 646)]
    for k, (x, y) in enumerate(crowd):
        els.append(ppl(x, y, 56, round(tp + .1 * k, 2), "#2a2018"))
    els += [poly([(1580, 606), (1700, 606), (1690, 618), (1590, 618)], WOOD_D, at=ts - .6, fx="rise")]
    for k in range(4):
        els.append(ppl(1600 + k * 24, 606, 34, ts - .5, "#3a3029"))
    els += [circ(1560 + k * 26, 570 - k * 14, 16 + k * 6, "#e8e4dc", at=round(ts + .1 * k, 2), op=.5 - .08 * k, fx="pop") for k in range(4)]
    lights = [(120 + (k % 6) * 62, 690 + (k // 6) * 40 - (k % 2) * 8) for k in range(12)]
    for k, (x, y) in enumerate(lights):
        els += [gl(x, y, 26, round(ts + .4 + .04 * k, 2), .7), dot(x, y, 5, "#ffe2a8", round(ts + .4 + .04 * k, 2))]
    for k, (x, y) in enumerate(lights):
        els += [dot(x, y, 30, "#4e5a34", round(tk + .5 + .12 * k, 2), op=.85)]
    els += [lab(275, 790, "about a dozen killed", tk + .3, BONE, 28)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "cam": CAM, "els": els}


XT = lambda yr: round(200 + (yr - 1720) / 150 * 1380, 1)            # 1720 to 1870 on the falling panel


def sc_topple():
    """s32: a time line 1722 to 1870 under a platform of seven statues: at 1722 all stand; by 1774 three have fallen; by the 1860s all
    lie fallen in front of the platform; small ship marks at the visits; a lilac question mark over the fallen row."""
    G = 470
    BG = "#15120e"
    els = [rect(-20, -20, 1820, 1040, BG, at=-1), rect(-20, G + 150, 1820, 30, "#2a241c", at=-1)]
    xs = [300 + k * 196 for k in range(7)]
    els += ahu(200, 1580, G - 30, 30, -1)
    for x in xs:
        els += moai(x, G - 30, 220, -1, light=-1, lichen=0)
    t74, t60, tq = T("topple", "seventy-four"), T("topple", "eighteen sixties"), T("topple", "Why they fell")
    falls = [(1, t74), (3, t74 + .3), (5, t74 + .6), (0, t60), (2, t60 + .2), (4, t60 + .4), (6, t60 + .6)]
    for i, t in falls:
        x = xs[i]
        els += [rect(x - 64, G - 30 - 236, 128, 238, BG, at=round(t, 2), dur=.35)]
        sgn = -1 if i % 2 else 1
        els += fallen(x - sgn * 90, G + 112, 180, round(t + .15, 2), ang=sgn * 86)
    els += [axis(XT(1720), XT(1870), 770, [(XT(y), str(y)) for y in (1722, 1774, 1838, 1868)], .3)]
    for yr in (1722, 1770, 1774, 1786, 1838, 1862):
        els += ship_icon(XT(yr), 730, 34, .5 + (yr - 1722) / 300, DIM)
    els += [dot(XT(1774), 770, 9, GOLD, t74), dot(XT(1862), 770, 9, GOLD, t60)]
    els += qmark(889, 190, tq, 100) + [gl(889, 380, 700, -1, .12)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_raid():
    """s33: night: raiders' ships offshore ('December 1862'). In a card at the left, the island's people as a block of small lights; a third
    of them go dark there and appear in a card by the ships ('more than 1,400 taken'), and most of those lights go out ('most died in
    Peru')."""
    CARD_ = "#100e0b"
    els = sky_wash("night", -300, 600) + [rect(-20, 600, 1820, 420, "#0b1a24", at=-1)] + waves_band(0, 1780, 620, -1, 30, op=.15)
    els += [poly([(-20, 640), (300, 610), (640, 630), (700, 1020), (-20, 1020)], "#1a1e14", at=-1, curve=True)]
    els += ship(1200, 640, 220, -1, None, c="#1a140e", sail="#6a6458") + ship(1520, 650, 200, -1, None, c="#1a140e", sail="#6a6458")
    els += chip(1360, 200, "December 1862", GOLD, .4, 28)
    tt, td = T("raid", "fourteen hundred"), T("raid", "Most die")
    els += [rect(90, 200, 560, 340, CARD_, "rgba(255,236,206,.25)", 2, 12, -1), lab(370, 580, "the island's people", -1, DIM, 26)]
    pts = []
    for r_ in range(8):
        for k in range(15):
            pts.append((130 + k * 34 + (r_ % 2) * 14, 240 + r_ * 36))
    for k, (x, y) in enumerate(pts):
        els += [dot(x, y, 6, "#ffe2a8", -1, None, op=.9)]
    taken = sorted(range(0, 120, 3))
    for j, k in enumerate(taken):
        x, y = pts[k]
        els += [dot(x, y, 9, CARD_, round(tt + .02 * j, 2))]
    els += [rect(800, 250, 360, 200, CARD_, "rgba(255,236,206,.25)", 2, 12, tt - .2)]
    for j in range(40):
        x, y = 840 + (j % 10) * 30, 290 + (j // 10) * 34
        els += [dot(x, y, 6, "#ffcf8a", round(tt + .3 + .02 * j, 2))]
    els += [arr([(660, 360), (730, 330), (790, 350)], tt, AMBER, 3, dur=.5, curve=True), lab(980, 230 - 14, "more than 1,400 taken", tt + .4, AMBER, 28)]
    for j in range(40):
        if j in (3, 17, 26, 38):
            continue
        x, y = 840 + (j % 10) * 30, 290 + (j // 10) * 34
        els += [dot(x, y, 9, CARD_, round(td + .03 * j, 2))]
    els += [lab(980, 500, "most died in Peru", td + .6, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_smallpox():
    """s34: a map: a dashed route from Peru to Rapa Nui, a ship with a dozen lights; at the island a dull red haze spreads ('smallpox');
    then, at the right, the people left by 1877: a small cluster of 110 dots ('about 110')."""
    v = View(-118.0, -66.0, -38.0, -4.0, (90, 130, 1000, 640))
    els = [rect(-20, -20, 1820, 1040, "#10232e", at=-1), {"k": "group", "clip": [60, 110, 1080, 700, 8], "els": [pacific_land(v, -1)], "in": -1},
           rect(60, 110, 1080, 700, "none", "rgba(255,236,206,.3)", 2, 8, -1)]
    rx, ry = v.p(-109.35, -27.12)
    px, py = v.p(-77.1, -12.05)
    els += [circ(rx, ry, 7, GOLD, "#fff6e6", 2, -1), lab(rx, ry + 40, "Rapa Nui", -1, GOLD, 26), dot(px, py, 7, BONE, -1, None), lab(px - 14, py - 18, "Peru", -1, BONE, 26, "end")]
    th, ts, tl = T("smallpox", "shipped"), T("smallpox", "sweeps"), T("smallpox", "about a hundred")
    route = [(px - 10, py + 6), ((px + rx) / 2, (py + ry) / 2 - 90), (rx + 14, ry - 8)]
    els += [ln(route, th, AMBER, 2.5, "inferred", 1.2, curve=True)]
    sx, sy = (px + rx) / 2 + 20, (py + ry) / 2 - 76
    els += ship_icon(sx, sy, 60, th + .6, BONE) + [dot(sx - 26 + 5 * k, sy + 14, 2.6, "#ffe2a8", th + .7) for k in range(12)]
    els += [gl(rx, ry, 140, ts - .2, .55, "red"), gl(rx, ry, 70, ts + .3, .6, "red"), lab(rx + 60, ry + 100, "smallpox", ts + .3, "#ff9a8a", 30, "start")]
    els += [rect(1200, 110, 520, 700, "#14110d", "rgba(255,236,206,.25)", 2, 8, tl - 1.2)]
    rnd = random.Random(3)
    k = 0
    while k < 110:
        a, rr = rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.uniform(0, 1)) * 120
        x, y = 1460 + math.cos(a) * rr, 430 + math.sin(a) * rr * .8
        els.append(dot(round(x, 1), round(y, 1), 4.5, "#ffe2a8", round(tl - .8 + .008 * k, 2)))
        k += 1
    els += chip(1460, 200, "1877", GOLD, tl - .6, 28) + [lab(1460, 640, "about 110", tl + .3, BONE, 40, st="serif"), lab(1460, 690, "Rapanui left", tl + .5, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def sheep(x, y, s, at, op=None):
    return [poly(E(x, y - .5 * s, .6 * s, .38 * s, 14), "#e8e2d4", "rgba(120,110,100,.6)", 1, at, fx="pop", op=op, curve=True),
            poly(E(x + .58 * s, y - .62 * s, .18 * s, .14 * s, 10), "#3a332c", at=at, fx="pop", op=op),
            ln([(x - .3 * s, y - .2 * s), (x - .3 * s, y)], at, "#3a332c", 2, draw=False, op=op), ln([(x + .3 * s, y - .2 * s), (x + .3 * s, y)], at, "#3a332c", 2, draw=False, op=op)]


def sc_ranch():
    """s35: left, the island with sheep over its grass and a walled village by the west coast ('one village', 'until the 1960s'). Right,
    the island's people from 1200 to 1900: a line steady until the 1860s, then dropping steeply, a ship at the drop ('the collapse')."""
    v = View(-109.47, -109.20, -27.215, -27.045, (90, 180, 800, 520))
    els = island(v, -1, fill="#5a6a3a")
    tsh, tv, tc = T("ranch", "sheep ranch"), T("ranch", "one village"), T("ranch", "There was a collapse")
    rnd = random.Random(21)
    P = [v.p(lo, la) for lo, la in RN]
    k = 0
    while k < 26:
        q = (rnd.uniform(min(p[0] for p in P), max(p[0] for p in P)), rnd.uniform(min(p[1] for p in P), max(p[1] for p in P)))
        if pip(q, P):
            els += sheep(q[0], q[1], 22, round(tsh + .05 * k, 2))
            k += 1
    hx_, hy_ = v.p(-109.425, -27.150)
    els += [poly(E(hx_ + 30, hy_, 54, 40, 18), "rgba(255,226,168,.25)", GOLD, 3, tv, fx="pop"), dot(hx_ + 30, hy_, 6, GOLD, tv),
            ln([(hx_ + 10, hy_ + 40), (220, 690)], tv + .1, GOLD, 1.5, dur=.4), lab(220, 730, "one village", tv + .2, GOLD, 28), lab(220, 766, "until the 1960s", tv + .4, DIM, 26)]
    x0, x1, y0, y1 = 1000, 1660, 660, 250
    X = lambda yr: x0 + (x1 - x0) * (yr - 1200) / 700
    Y = lambda f: y0 - (y0 - y1) * f
    els += [axis(x0, x1, y0, [(X(y), str(y)) for y in (1200, 1500, 1700, 1900)], .3, "years CE"), lab(x0, y1 - 30, "the island's people", .3, DIM, 26, "start")]
    line_ = [(X(1200), Y(.04)), (X(1350), Y(.3)), (X(1500), Y(.52)), (X(1650), Y(.66)), (X(1722), Y(.72)), (X(1800), Y(.72)), (X(1860), Y(.72))]
    els += [ln(line_, .5, GOLD, 5, dur=1.2, curve=True), ln([(X(1860), Y(.72)), (X(1868), Y(.36)), (X(1877), Y(.03)), (X(1900), Y(.04))], tc - .6, RED, 5, dur=.8)]
    els += ship_icon(X(1862) - 50, Y(.8) - 20, 50, tc - .5, RED) + [lab(X(1877) - 20, Y(.03) - 26, "110", tc, RED, 26, "end"), lab(X(1855), Y(.45), "the collapse", tc + .3, RED, 30, "end")]
    return {"base": "map", "cam": CAM, "els": els}


GLYPHS = {   # small signs in a 1 x 1.4 box (x right, y down), as strokes: figures, birds, fish, plants (schematic, not real readings)
    "man": [[(.5, .18), (.5, .2)], [(.5, .3), (.5, .85)], [(.2, .2), (.5, .45), (.8, .2)], [(.3, 1.3), (.5, .85), (.7, 1.3)]],
    "bird": [[(.15, .55), (.45, .45), (.55, .2), (.7, .3), (.6, .5), (.85, .55)], [(.45, .5), (.5, 1.0), (.3, 1.3)], [(.5, 1.0), (.7, 1.3)]],
    "fish": [[(.1, .7), (.4, .45), (.8, .6), (.4, .95), (.1, .7)], [(.8, .6), (.95, .4)], [(.8, .6), (.95, .85)]],
    "plant": [[(.5, 1.3), (.5, .2)], [(.5, .5), (.2, .3)], [(.5, .7), (.8, .5)], [(.5, .9), (.2, .7)]],
    "moon": [[(.7, .2), (.35, .45), (.3, .8), (.45, 1.15), (.75, 1.25)], [(.7, .2), (.5, .5), (.5, .9), (.75, 1.25)]],
    "staff": [[(.5, .1), (.5, 1.3)], [(.3, .35), (.5, .1), (.7, .35)], [(.35, .9), (.65, .9)]],
    "birdman": [[(.3, .3), (.45, .15), (.6, .25), (.5, .35)], [(.5, .35), (.5, .9)], [(.15, .5), (.5, .55), (.85, .45)], [(.3, 1.3), (.5, .9), (.75, 1.3)]],
    "hand": [[(.5, 1.3), (.5, .6)], [(.5, .6), (.2, .2)], [(.5, .6), (.4, .15)], [(.5, .6), (.6, .15)], [(.5, .6), (.8, .25)]],
    "turtle": [[(.2, .7), (.5, .45), (.8, .7), (.5, .95), (.2, .7)], [(.8, .7), (.95, .65)], [(.3, .5), (.2, .35)], [(.7, .5), (.8, .35)], [(.3, .9), (.2, 1.05)], [(.7, .9), (.8, 1.05)]],
    "loop": [[(.5, 1.3), (.5, .7), (.25, .45), (.5, .2), (.75, .45), (.5, .7)]],
}


GKEYS = list(GLYPHS)


def glyph_row(x, y, n, size, seed, c="#e8d6b0", w=2.2):
    """A row of n small signs starting at (x, y) (their tops), each `size` wide."""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        g = GLYPHS[rnd.choice(GKEYS)]
        gx = x + k * size * 1.05
        for stroke in g:
            out.append(ln([(gx + u * size * .9, y + v * size * .9) for u, v in stroke], -1, c, w, draw=False))
    return out


def tablet(x, y, w, h, at, rows=8, flip_at=None, fx="pop", seed=5, notch=False, glyphs=True):
    """A rongorongo tablet: dark wood with a rounded outline and fluted lines, rows of small carved signs. flip_at: when the even rows
    turn over (before that every row stands upright)."""
    rnd = random.Random(seed)
    outline = [(x + 10, y + rnd.uniform(-3, 3)), (x + w * .5, y - 6), (x + w - 10, y + rnd.uniform(-3, 3)), (x + w + 6, y + h * .5), (x + w - 10, y + h + rnd.uniform(-3, 3)),
               (x + w * .5, y + h + 6), (x + 10, y + h), (x - 6, y + h * .5)]
    if notch:
        outline = outline[:3] + [(x + w + 4, y + h * .32), (x + w - 30, y + h * .38), (x + w - 28, y + h * .5), (x + w + 6, y + h * .56)] + outline[4:]
    els = [poly(outline, WOOD, "rgba(255,226,180,.45)", 2, at, fx=fx, curve=True), poly(outline, "url(#k-speck)", at=at, fx=fx, curve=True)]
    if not glyphs:
        return els
    lh = h / (rows + .4)
    size = lh * .62
    n = int((w - 40) / (size * 1.05))
    for r_ in range(rows):
        yy = y + 14 + r_ * lh
        row = glyph_row(x + 22, yy, n, size, seed * 31 + r_)
        if r_ % 2 == 1 and flip_at is not None:
            els.append(grp(row, at, None))
            els.append(rect(x + 14, yy - 4, w - 28, lh - 4, WOOD, at=round(flip_at, 2), dur=.3))
            els.append(rect(x + 14, yy - 4, w - 28, lh - 4, "url(#k-speck)", at=round(flip_at, 2), dur=.3))
            els.append(grp(row, round(flip_at + .3, 2), "pop", tr="rotate(180 %s %s)" % (round(x + w / 2, 1), round(yy + size * .62, 1))))
        elif r_ % 2 == 1:
            els.append(grp(row, at, None, tr="rotate(180 %s %s)" % (round(x + w / 2, 1), round(yy + size * .62, 1))))
        else:
            els.append(grp(row, at, None))
        if r_ < rows - 1:
            els.append(ln([(x + 14, yy + lh - 6), (x + w - 14, yy + lh - 6)], at, "rgba(20,12,8,.5)", 1.4, draw=False))
    return els


def sc_tablet():
    """s36: a rongorongo tablet, dark wood, eight rows of small carved signs; on 'upside down' every second row turns over; an arrow
    shows the reading direction left to right and a curved arrow turns the tablet at the end of each row ('turn at each row')."""
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1), gl(760, 470, 700, -1, .16)]
    tu, tt = T("tablet", "upside down"), T("tablet", "turns the tablet")
    els += tablet(260, 180, 1000, 560, -1, rows=8, flip_at=tu)
    els += [arr([(300, 160), (1200, 160)], tu - .6, AMBER, 3, dur=.8), lab(750, 140, "read left to right", tu - .4, AMBER, 26)]
    els += [arr([(1300, 230), (1380, 300), (1380, 380), (1300, 450)], tt, GOLD, 3, dur=.8, curve=True), lab(1420, 350, "turn at each row", tt + .3, GOLD, 30, "start")]
    els += [{"k": "line", "p": [[1490, 440], [1560, 440]], "c": "rgba(0,0,0,0)", "w": 1, "in": -1}]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_shelf():
    """s37: 'rongorongo' as a title on dark ground; below, two shelves with 26 small inscribed objects (flat tablets, a staff, a few
    carved pieces) popping one by one ('fewer than 30 survive'); a small lock ('not yet read')."""
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1), gl(889, 400, 760, -1, .14)]
    tr_, tf, tn = T("shelf", "rongorongo"), T("shelf", "Fewer than thirty"), T("shelf", "no one can")
    els += [lab(889, 250, "rongorongo", tr_, GOLD, 72, st="serif")]
    rnd = random.Random(9)
    for row, y in enumerate((520, 700)):
        els += [rect(150, y, 1480, 14, "#4a3a2a", "rgba(255,226,180,.3)", 1, 2, tf - .4)]
        for k in range(13):
            x = 190 + k * 110
            i = row * 13 + k
            t = round(tf + .06 * i, 2)
            if i == 7:
                els += [rect(x + 30, y - 150, 16, 150, WOOD, "rgba(255,226,180,.4)", 1, 5, t, fx="pop")]
                els += [ln([(x + 34, y - 140 + 9 * j), (x + 42, y - 140 + 9 * j)], t, "#c8a878", 1.2, draw=False) for j in range(14)]
                continue
            w, hh = rnd.uniform(64, 90), rnd.uniform(70, 120)
            els += [rect(x + (90 - w) / 2, y - hh - 2, w, hh, WOOD, "rgba(255,226,180,.4)", 1.2, 10, t, fx="pop")]
            for j in range(int(hh // 14)):
                yy = y - hh + 8 + j * 14
                els.append(ln([(x + (90 - w) / 2 + 8, yy), (x + (90 + w) / 2 - 8, yy)], t, "#c8a878", 1.6, "inferred", draw=False, op=.7))
    els += [lab(889, 790 - 20, "fewer than 30 survive", tf + 1.6, BONE, 30)]
    els += [rect(1480, 160, 60, 50, "none", BONE, 3, 6, tn, fx="pop"), ln([(1490, 160), (1490, 140), (1510, 126), (1530, 140), (1530, 160)], tn, BONE, 3, draw=False, curve=True),
            lab(1510, 250, "not yet read", tn + .3, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_quill():
    """s38: a Spanish ship offshore ('1770'); on the shore, a sheet of paper and a quill with a few marks on it; two paths to a tablet at
    the right, one from an island house (gold, 'invented here?'), one from the paper (lilac dots, 'copied?'); a question mark between."""
    G = 620
    els = sky_wash("day", -220, 520) + [rect(-20, 470, 1820, 150, SEA, at=-1)] + waves_band(0, 1780, 480, -1, 20, op=.25)
    els += [poly([(-20, G - 20), (800, G - 30), (1820, G - 20), (1820, 1020), (-20, 1020)], "#4e5a34", at=-1)]
    els += ship(380, 500, 220, -1, None, c="#2a2018", sail="#e8dcc0", flag="#d8b030") + chip(380, 240, "1770", GOLD, .4, 28)
    tq, tc = T("quill", "a quill"), T("quill", "Invented on")
    els += [rect(520, 640, 170, 120, "#f3ead8", "#c9b89a", 1.5, 3, tq - .6, fx="rise")]
    for k in range(3):
        els.append(ln([(545 + k * 44, 690), (560 + k * 44, 670), (575 + k * 44, 700)], round(tq - .2 + .1 * k, 2), "#3a3029", 2.4, dur=.3))
    els += [ln([(660, 720), (760, 610)], tq, "#e8e0d0", 3, draw=False), poly([(752, 612), (790, 560), (800, 570), (764, 622)], "#f5f0e6", at=tq, fx="pop")]
    els += hare(1000, 600, 200, -1)
    els += tablet(1340, 300, 280, 200, -1, rows=4, seed=11)
    els += [arr([(1000, 540), (1150, 430), (1320, 400)], tc, GOLD, 3, dur=.7, curve=True), lab(1130, 360, "invented here?", tc + .2, GOLD, 28)]
    els += [arr([(700, 630), (1000, 560), (1330, 480)], tc + .9, LILAC, 3, "claimed", .7, curve=True), lab(1150, 640, "copied?", tc + 1.1, LILAC, 28)]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": False, "cam": CAM, "els": els}


XR = lambda yr: round(200 + (yr - 1400) / 500 * 1380, 1)     # 1400 to 1900 on the Rome panel


def sc_rome():
    """s39: four tablet silhouettes in a row ('Rome, 2024'), the notched tablet first; a time line 1400 to 1900 below them with a ship
    mark at 1722; a line from each tablet drops to its date: the notched tablet's to about 1500, the other three to the 1800s."""
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1), gl(889, 360, 760, -1, .14)]
    xs = [260, 640, 980, 1320]
    for k, x in enumerate(xs):
        els += tablet(x, 200, 200, 230, -1, rows=5, seed=20 + k, notch=(k == 0))
    els += chip(889, 150, "Rome, 2024", GOLD, .4, 26)
    els += [axis(XR(1400), XR(1900), 700, [(XR(y), str(y)) for y in (1400, 1500, 1600, 1700, 1800, 1900)], .3)]
    els += [ln([(XR(1722), 700), (XR(1722), 540)], .5, BONE, 2, "inferred", .4)] + ship_icon(XR(1722), 530, 44, .6, BONE) + [lab(XR(1722) + 34, 560, "1722", .6, BONE, 24, "start")]
    t3, t4 = T("rome", "Three came"), T("rome", "The fourth")
    for k, (x, yr) in enumerate(((640, 1820), (980, 1845), (1320, 1875))):
        els += [ln([(x + 100, 440), (x + 100, 470), (XR(yr), 690)], round(t3 + .2 * k, 2), AMBER, 2.4, dur=.6), dot(XR(yr), 700, 9, AMBER, round(t3 + .6 + .2 * k, 2))]
    els += [lab(XR(1850), 650 - 20, "1800s", t3 + 1.2, AMBER, 26)]
    els += [ln([(360, 440), (360, 500), (XR(1501), 690)], t4, GOLD, 3, dur=.8), rect(XR(1493), 690, XR(1509) - XR(1493), 20, GOLD, at=t4 + .8, fx="pop"),
            gl(XR(1501), 700, 60, t4 + .8, .55), lab(360, 478, "the notched tablet", t4 + .2, GOLD, 28), lab(XR(1501), 664, "about 1500", t4 + 1.0, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


SAFV = View(-130.0, 50.0, -60.0, 10.0, (860, 150, 840, 560))


def brick(x, y, w, at, stamp="1500"):
    h = w * .45
    return [rect(x, y, w, h, "#9a4a34", "rgba(255,200,170,.4)", 1.5, 3, at, fx="pop"), rect(x + w * .25, y + h * .25, w * .5, h * .5, "none", "#d88a6a", 1.5, 2, at, fx="pop"),
            label(round(x + w / 2, 1), round(y + h * .62, 1), stamp, round(at + .1, 2), "#f5e0d0", 24, "middle", "lab", halo=False, scl=True)]


def sc_brick():
    """s40: left, a brick stamped '1500' ('the tree's date') and, apart from it, a house going up later, its date dashed ('the carving?').
    Right, a map from southern Africa to Rapa Nui: a dashed arc with a drifting log and a ship, both with question marks ('from southern
    Africa')."""
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1)]
    tb, th, ta = T("brick", "a brick"), T("brick", "went up"), T("brick", "southern Africa")
    els += brick(150, 300, 200, tb) + [lab(250, 460, "the tree's date", tb + .2, GOLD, 26)]
    els += [arr([(380, 340), (470, 340)], th - .4, DIM, 2.4, "inferred", .4)]
    for r_ in range(5):
        for k in range(4 - (r_ % 2)):
            els.append(rect(500 + k * 64 + (r_ % 2) * 32, 560 - r_ * 34, 60, 30, "#9a4a34", "rgba(255,200,170,.35)", 1, 2, round(th - .3 + .06 * (r_ * 4 + k), 2), fx="pop"))
    els += [poly([(490, 390), (630, 300), (770, 390)], "none", BONE, 2.4, th + .3, style="inferred", fx="pop"), lab(630, 640, "the carving: ?", th + .5, LILAC, 26)]
    v = SAFV
    els += [rect(860, 150, 840, 560, "#10232e", at=-1), {"k": "group", "clip": [860, 150, 840, 560, 8], "els": [pacific_land(v, -1)], "in": -1},
            rect(860, 150, 840, 560, "none", "rgba(255,236,206,.3)", 2, 8, -1)]
    ax_, ay_ = v.p(28.0, -30.0)
    rx, ry = v.p(-109.35, -27.12)
    els += [dot(ax_, ay_, 8, GOLD, ta - .3), lab(ax_, ay_ + 40, "southern Africa", ta, GOLD, 26), circ(rx, ry, 7, BONE, "#fff6e6", 2, -1), lab(rx + 10, ry + 36, "Rapa Nui", -1, BONE, 24, "start")]
    arc = [(ax_ - 8, ay_ + 10), ((ax_ + rx) / 2, max(ay_, ry) + 170), (rx + 10, ry + 8)]
    els += [ln(arc, ta + .3, AMBER, 2.5, "inferred", 1.2, curve=True)]
    mx_, my_ = (ax_ + rx) / 2, max(ay_, ry) + 128
    els += [rect(mx_ - 140, my_ - 10, 70, 16, WOOD_L, "rgba(255,226,180,.4)", 1, 6, ta + 1.0, fx="pop"), lab(mx_ - 105, my_ - 26, "driftwood?", ta + 1.1, DIM, 24)]
    els += ship_icon(mx_ + 100, my_ + 2, 50, ta + 1.3, DIM) + [lab(mx_ + 100, my_ - 50, "a ship?", ta + 1.4, DIM, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


WORLDV = View(-180.0, 180.0, -58.0, 72.0, (90, 150, 1600, 620))


def sc_inventions():
    """s41: a world map: four gold pins pop as named (Mesopotamia, Egypt, China, Mesoamerica: the known independent inventions of
    writing); then a lilac dashed ring on Rapa Nui with a question mark; on 'a speck of land' the ring glows."""
    v = WORLDV
    els = [pacific_land(v, -1, "#2e271f")]
    tm, te, tc, tma, tr_, ts = (T("inventions", "Mesopotamia"), T("inventions", "Egypt"), T("inventions", "China"), T("inventions", "Mesoamerica"),
                                T("inventions", "invented here"), T("inventions", "speck of land"))
    for (lo, la, t, nm, a) in ((45.6, 31.3, tm, "Mesopotamia", "start"), (31.9, 26.2, te, "Egypt", "end"), (114.4, 36.1, tc, "China", "start"),
                               (-96.7, 17.1, tma, "Mesoamerica", "end")):
        x, y = v.p(lo, la)
        e = {"k": "pin", "x": x, "y": y, "t": nm, "c": GOLD, "in": round(t, 2)}
        if a == "end":
            e.update(a="end", lx=-18)
        els.append(e)
    rx, ry = v.p(-109.35, -27.12)
    els += [circ(rx, ry, 30, "none", LILAC, 3, tr_, style="inferred", fx="pop"), lab(rx, ry - 44, "Rapa Nui?", tr_ + .2, LILAC, 28)]
    els += [gl(rx, ry, 90, ts, .6), dot(rx, ry, 6, "#fff1d2", ts)]
    return {"base": "map", "cam": CAM, "els": els}


ROWS = [270, 430, 590]


def lrow(k, at, pic, text, grade, gt, gc):
    y = ROWS[k]
    return [rect(130, y - 66, 1520, 132, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(330, y + 11, text, at + .1, BONE, 32, "start")] + \
        pic(230, y, at) + chip(1180, y, grade, gc, gt, 30, a="start")


def pic_stump(x, y, at):
    return stump(x, y + 30, 70, at, fx="pop")


def pic_lean(x, y, at):
    return [grp(moai_side(x - 20, y + 48, 110, -1, base="D", sockets=False, lean=10), at, "pop")]


def pic_crash(x, y, at):
    return [ln([(x - 60, y + 30), (x - 20, y - 10), (x + 5, y - 40), (x + 30, y + 30)], at, LILAC, 3, "claimed", .5, curve=True), I.strike(x - 55, y - 40, x + 40, y + 40, at + .3, RED, 4)]


def pic_arc(x, y, at):
    return [dot(x - 55, y + 20, 7, GOLD, at), dot(x + 55, y + 20, 7, SAND_E, at), arr([(x - 50, y + 12), (x, y - 30), (x + 50, y + 12)], at, AMBER, 3, "inferred", .5, curve=True)]


def pic_ship(x, y, at):
    return ship_icon(x, y + 30, 90, at, BONE)


def pic_tablet(x, y, at):
    return tablet(x - 50, y - 40, 100, 80, at, rows=3, seed=4)


def sc_ledger1():
    """s42: the ledger fills row by row (a pictogram, a short text and a grade chip that pops as the grade is said): 'a palm forest lost'
    Established; 'giants that walked' Strong evidence; 'a crash before 1722' Ruled out."""
    els = [rect(110, 170, 1560, 560, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .1)]
    t1, e1 = T("ledger1", "A palm forest"), T("ledger1", "Established")
    t2, e2 = T("ledger1", "Giants that walked"), T("ledger1", "Strong evidence")
    t3, e3 = T("ledger1", "A great crash"), T("ledger1", "Ruled out")
    els += lrow(0, t1, pic_stump, "a palm forest lost", "Established", e1, GRADE["established"])
    els += lrow(1, t2, pic_lean, "giants that walked", "Strong evidence", e2, GRADE["strong"])
    els += lrow(2, t3, pic_crash, "a crash before 1722", "Ruled out", e3, GRADE["ruled"])
    els += [lab(330, ROWS[0] + 50, "shares still argued", e1 + .6, MUTED, 24, "start"), lab(330, ROWS[1] + 50, "untested at 80 t", e2 + .6, MUTED, 24, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_ledger2():
    """s43: a second ledger: 'contact with the Americas' Strong evidence; 'a collapse after contact' Established; 'a script invented here'
    Open question; then a banner across the bottom: 'the famous story' with the chip Mixed record, a stump at one side and a small group
    of people at the other."""
    els = [rect(110, 170, 1560, 480, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .1)]
    t1, e1 = T("ledger2", "Contact with the"), T("ledger2", "Strong evidence")
    t2, e2 = T("ledger2", "A collapse after"), T("ledger2", "Established")
    t3, e3 = T("ledger2", "A script invented"), T("ledger2", "Open question")
    tf, tm, tv, te = T("ledger2", "the famous story"), T("ledger2", "mixed record"), T("ledger2", "vanished"), T("ledger2", "endured")
    rows = [250, 390, 530]
    for k, (t, e, pic, text, grade, gc) in enumerate(((t1, e1, pic_arc, "contact with the Americas", "Strong evidence", GRADE["strong"]),
                                                       (t2, e2, pic_ship, "a collapse after contact", "Established", GRADE["established"]),
                                                       (t3, e3, pic_tablet, "a script invented here", "Open question", GRADE["open"]))):
        y = rows[k]
        els += [rect(130, y - 60, 1520, 120, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, t, fx="pop"), lab(330, y + 11, text, t + .1, BONE, 32, "start")]
        els += pic(230, y, t) + chip(1180, y, grade, gc, e, 30, a="start")
    els += [rect(110, 670, 1560, 120, "rgba(232,184,122,.12)", GRADE["mixed"], 2.5, 18, tf - .2, fx="pop"), lab(330, 742, "the famous story", tf, BONE, 34, "start", st="serif")]
    els += chip(1180, 730, "Mixed record", GRADE["mixed"], tm, 32, a="start")
    els += stump(780, 760, 46, tv, fx="pop") + [ppl(900 + 26 * k, 762, 50 - 4 * (k % 2), round(te + .08 * k, 2), BONE) for k in range(4)]
    return {"base": "dark", "cam": CAM, "els": els}


def dframe(x, y, w, h, at, title, c=BONE):
    return [rect(x, y, w, h, "rgba(245,236,220,.04)", c, 2.4, 14, at, fx="pop", style="inferred"), lab(x + w / 2, y + h + 40, title, at + .2, c, 28)]


def sc_test():
    """s44: four dashed frames pop as named: a DNA helix ('before 1600'); an upland slope with a garden and a house outline ('upland
    gardens'); a big statue with ropes and a question mark ('80 t walk'); a tablet of island wood ('before 1722?')."""
    els = [rect(-20, -20, 1820, 1040, "#15120e", at=-1)]
    tq, tg, tu, tw, tr_ = T("test", "change our"), T("test", "Genomes from"), T("test", "Dated gardens"), T("test", "eighty-tonne"), T("test", "rongorongo tablet")
    els += [lab(889, 150, "?", tq, LILAC, 54, st="serif")]
    xs = [120, 520, 920, 1320]
    W, Hh, Y0 = 340, 380, 230
    els += dframe(xs[0], Y0, W, Hh, tg, "genomes before 1600") + helix(xs[0] + 40, xs[0] + W - 40, Y0 + 190, 50, tg + .3, dur=1.0, rungs=10)
    els += dframe(xs[1], Y0, W, Hh, tu, "upland gardens")
    els += [poly([(xs[1] + 20, Y0 + 330), (xs[1] + 160, Y0 + 170), (xs[1] + 320, Y0 + 330)], "#3a4428", "rgba(255,236,206,.3)", 1.5, tu + .3, fx="pop")]
    els += [poly(E(xs[1] + 150, Y0 + 260, 50, 16, 14), "#6e6a64", at=tu + .5, fx="pop"), poly([(xs[1] + 210, Y0 + 300), (xs[1] + 230, Y0 + 270), (xs[1] + 280, Y0 + 270),
                                                                                            (xs[1] + 300, Y0 + 300)], "none", BONE, 2, tu + .6, style="inferred", fx="pop"),
            {"k": "pin", "x": xs[1] + 160, "y": Y0 + 120, "c": GOLD, "in": round(tu + .7, 2)}]
    els += dframe(xs[2], Y0, W, Hh, tw, "an 80 t walk") + moai(xs[2] + W / 2, Y0 + Hh - 30, 300, tw + .3, style="inferred", fx="pop")
    els += [ln([(xs[2] + W / 2 - 20, Y0 + 120), (xs[2] + 30, Y0 + 300)], tw + .5, "#c9a86a", 2, dur=.4), ln([(xs[2] + W / 2 + 20, Y0 + 120), (xs[2] + W - 30, Y0 + 300)], tw + .5, "#c9a86a", 2, dur=.4)]
    els += dframe(xs[3], Y0, W, Hh, tr_, "island wood, before 1722") + tablet(xs[3] + 50, Y0 + 100, W - 100, 180, tr_ + .3, rows=4, seed=33)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_close():
    """s45: the opening slope again at night on its own panel: the heads under stars, a low moon; far off along the coast, the warm lights
    of a village; the heads catch a little moonlight. Then the end card."""
    els = sc_hero(night=True)
    els += [rect(-20, -20, 1820, 1040, "#0a1222", at=-1, op=.45)]
    els += [gl(330, 210, 120, -1, .5, "lamp"), circ(330, 210, 22, "#efe8da", at=-1)]
    tl = T("close", "their people")
    for k in range(14):
        els += [dot(70 + k * 22 + (k % 3) * 6, 540 - (k % 2) * 4, 3, "#ffd690", round(tl + .08 * k, 2)), gl(70 + k * 22, 540, 18, round(tl + .08 * k, 2), .5)]
    return {"base": "sky", "tod": "night", "ground": 1100, "sun": False, "moon": False, "cam": [1.0, 889, 500], "els": els}


def fallen(x, y, h, at, ang=84, light=-1):
    """A statue fallen over, drawn as its front view turned on its side (the head away from the platform): a schematic of a toppled
    statue; (x, y) where its base lies."""
    return [grp(moai(0, 0, h, -1, light=light, lichen=0), at, "pop", tr="translate(%s %s) rotate(%s)" % (round(x, 1), round(y, 1), ang))]


def lying_top(x, y, h, at, ang=90, squash=.5, up=True, fx="pop", broken=False, light=-1):
    """A statue lying on the ground seen from a little above: its front view laid along the ground (turned by ang degrees, head to the
    right at 90) and foreshortened (squash). up: on its back, the face to the sky; otherwise face down, its plain back showing. (x, y) the
    middle of its base on the ground."""
    if up:
        body = moai(0, 0, h, -1, light=light, lichen=0)
    else:
        body = [poly(_front_outline(0, 0, h), TUFF_D, TUFF_E, 1.4, -1), poly(_front_outline(0, 0, h * .98), TUFF, at=-1, op=.55),
                ln([(0, -.08 * h), (0, -.55 * h)], -1, "#3a332b", max(1.5, .006 * h), draw=False)]
    tr = "translate(%s %s) scale(1 %s) rotate(%s)" % (round(x, 1), round(y, 1), squash, ang)
    out = [grp(body, at, fx, tr=tr)]
    if broken:
        a = math.radians(ang)
        bx, by_ = x + math.sin(a) * .56 * h, y - math.cos(a) * .56 * h * squash
        out.append(ln([(bx - 6, by_ - .2 * h * squash), (bx + 6, by_ + .2 * h * squash)], at, "#120e0b", max(3, .03 * h), draw=False))
    return out


def _stub(name):
    def f():
        return {"base": "dark", "cam": CAM, "els": [lab(889, 480, name, .3, AMBER, 40)]}
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
    (0, 0, "hook", "hero", [(0, "Dig, and", "dig"), (0, "Nearly a thousand", "pacific"), (1, "A famous story", "story")], {}),
    (0, 1, "title", "story", [], {"intro": True}),
    (1, 0, "world", "landing", [(1, "How do we know", "core")], {"chapter": "A forest of giant palms"}),
    (1, 1, "collision", "palms", [(0, "By the {1500s", "gone")], {}),
    (1, 2, "reversal", "fire", [(1, "But the canoes", "rat"), (1, "With no predators", "ratchart")], {}),
    (1, 3, "tag", "balance", [], {}),
    (2, 0, "world", "paro", [(1, "So how do you", "problem")], {"chapter": "Giants on the road"}),
    (2, 1, "collision", "sledge", [(1, "But Rapanui tradition", "road")], {}),
    (2, 2, "reversal", "road", [(0, "Unlike the ones", "compare"), (1, "In {2012", "walk"), (2, "The roads fit", "dish")], {}),
    (2, 3, "tag", "doubts", [], {}),
    (3, 0, "world", "collapse", [], {"chapter": "Counting the people"}),
    (3, 1, "collision", "dates", [(1, "And the great stone", "ahu")], {}),
    (3, 2, "reversal", "gardens", [(1, "Earlier estimates", "area")], {}),
    (3, 3, "tag", "critics", [], {}),
    (4, 0, "world", "museum", [], {"chapter": "Fifteen ancestors"}),
    (4, 1, "collision", "beads", [], {}),
    (4, 2, "reversal", "americas", [], {}),
    (4, 3, "tag", "home", [], {}),
    (5, 0, "world", "dutch", [], {"chapter": "When the ships came"}),
    (5, 1, "collision", "topple", [], {}),
    (5, 2, "reversal", "raid", [(1, "After protests", "smallpox")], {}),
    (5, 3, "tag", "ranch", [], {}),
    (6, 0, "world", "tablet", [(1, "Rapanui call it", "shelf")], {"chapter": "A script of their own"}),
    (6, 1, "collision", "quill", [], {}),
    (6, 2, "reversal", "rome", [(1, "But that is", "brick")], {}),
    (6, 3, "tag", "inventions", [], {}),
    (7, 0, "weigh", "ledger1", [(1, "Contact with the", "ledger2")], {"chapter": "The weighing"}),
    (7, 1, "test", "test", [], {}),
    (7, 2, "close", "close", [], {}),
]

# alias shots: (the panel they return to, the camera on that panel, the function drawing their additions on arrival)
ALIASES = {
    "dig": ("hero", [1.35, 726, 600], "add_dig"),
    "gone": ("palms", [1, 889, 500], "add_gone"),
    "ahu": ("dates", [1, 889, 500], "add_ahu"),
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
        head_ = parts[0]
        if kw.get("chapter"):
            acts = [m.start() for m in SENT.finditer(head_) if m.start() > 0]
            head_ = head_[acts[0]:] if acts else ""
        if role != "title":
            say[frm] = say[frm] + "\n" + head_ if frm in say else head_
        for k in range(1, len(parts), 2):
            say[parts[k]] = parts[k + 1].strip("\n")
    return say


def film():
    script = json.load(open(SCRIPT, encoding="utf-8"))
    SAY.clear(); SAY.update(_segments(script))
    CLK.clear(); DUR.clear()
    for k, v in SAY.items():
        CLK[k], DUR[k] = _clock(v)
    g = globals()
    panels = {}
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in ALIASES and sid not in panels:
                panels[sid] = (g.get("sc_" + sid + "_scene") or g.get("sc_" + sid) or _stub(sid))()
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
    ep = {"id": "lf-rapa-nui", "code": "LF.27", "series": script["series"], "title": script["title"], "case": "rapa-nui",
          "verdict": "mixed", "claim": "Did the people of Rapa Nui destroy their own world before Europeans arrived?", "mood": "mystery",
          "hook_text": "Did they destroy their own *world*?", "beats": beats, "shots": shots,
          "sources": "Moreno-Mayar et al. 2024 (doi:10.1038/s41586-024-07881-4) · Davis et al. 2024 (doi:10.1126/sciadv.ado1459) · "
                     "Ferrara et al. 2024 (doi:10.1038/s41598-024-53063-7) · Lipo & Hunt 2025 (doi:10.1016/j.jas.2025.106383) · "
                     "Hunt & Lipo 2025 (doi:10.1016/j.jas.2025.106388) · Mieth & Bork 2010 (doi:10.1016/j.jas.2009.10.006) · "
                     "DiNapoli et al. 2020 (doi:10.1016/j.jas.2020.105094), 2021 (doi:10.1038/s41467-021-24252-z) · "
                     "Stevenson et al. 2015 (doi:10.1073/pnas.1420712112) · Diamond 2005 · Fischer 2005 · Maude 1981",
          "post": "Nearly a thousand stone giants on an island 24 km long, and a famous story: the islanders cut down every tree, starved, fought "
                  "and fell before Europeans came. The palms, the rats, the walking statues, radiocarbon, rock gardens from space, the 2024 "
                  "genomes, the slave raids of 1862 and the rongorongo tablets, claim by claim. Weighed.",
          "hashtags": ["#RapaNui", "#EasterIsland", "#Moai", "#Archaeology", "#History", "#WeighItYourself"],
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
