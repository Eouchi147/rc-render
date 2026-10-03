"""LF.21 · The Files · Roswell: What Fell on the Ranch (16:9 long film, one wall).

The script is films/long/lf-roswell/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s45; s5t, the title, is the intro card over the
panel of s5), drawn while it is said: the Roswell Daily Record of 8 July 1947 over a ranch at dusk, the 509th's air field, the next
day's balloon, thirty quiet years, Mac Brazel's debris (rubber, foil, paper, sticks, tape with flowers), the sheriff, the press
release and the wires, the debris on the floor in Fort Worth, the rancher's own account, the base history; Marcel in 1978, the books
and the crash sites that multiplied, Haut's sealed statement, a memory against a photograph, two debris fields to scale; Schiff and
the auditors, Project Mogul's sound channel, the NYU train of 23 balloons beside a football pitch on end, the radar reflector and its
flowered tape, Flight 4, the match, the markings, the gap; the two documents of 1947 and the destroyed messages, the 1995 film and
its set, the dummies, the accidents and memories that merge, four answers, the 2024 review; the ledger, the tests and the ranch at
dusk. Drawings are schematic and true to the numbers said: solid = on the record, dashed = inferred or missing, dotted = claimed.
People are drawn as quiet figures, with respect; the air crash of 1956 is marked, never shown.

Facts: the Short 'roswell-mogul' (f13.py, 13.04) and the script's facts_added (Roswell Daily Record 8 and 9 July 1947; the FBI
teletype of 8 July 1947; GAO 1995; Schiff 1995; Weaver 1994 with the Newton and Cavitt statements; McAndrew 1995 and 1997; AARO
2024; Saler, Ziegler & Moore 1997; Thomas 1995; Pflock 2001; Pratt 1980; the books of 1980 to 1994; Carey & Schmitt 2007; the
2006 documentary and Santilli's own account).

Engine workaround (as in lf_stargate.py and lf_mkultra.py): the wall adds elements to a panel on its first visit, at a beat start
or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a
tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's
additions as a panel item (kit.js builds them on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-roswell/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-roswell/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-roswell RC_FILMS_EPS=/tmp/claude-0/sbx_lf-roswell/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-roswell/boards python3 films.py long.lf_roswell
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-roswell", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN, INK = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN, I.INK
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
PAPER, PAPER_E, PAPER_D = "#efe6d2", "#fff6e2", "#cdbf9f"      # paper, its lit edge, its shade
NEWS, NEWS_D = "#e9dfca", "#b9ab90"                            # newsprint and its shade
MANILA, MANILA_E = "#cdb58a", "#8a6a48"                        # folders
CARD, CARD_S, CARD_T = "#9a7650", "#6e5236", "#b48e62"          # cardboard archive boxes: front, side, top
STAMP = "#b8322a"                                              # a rubber stamp's red, readable on paper
TYPE = "#3a3029"                                               # typewriter ink
STEEL, STEEL_D = "#5d6166", "#2c2f33"                          # archive shelving
DESK, DESK_E = "#21180f", "#3a2b1d"                            # a desk top at night
FLAT = "#15110d"                                               # flat panel background (for veils)
GRADE = {"established": "#8fd9b0", "strong": "#a6d98f", "plausible": "#f2c98e", "ruled": "#e98a8a", "awaiting": "#c9c1ee"}
# the ranch, the debris, the balloons
SIL = "#120e0b"                                                # silhouettes against the sky
GRASS, SCRUB = "#4a3b2a", "#2a2219"
FOIL, FOIL_E = "#d3d8dd", "#ffffff"
RUBBER = "#77716b"                                             # 'smoke gray' rubber
TOUGH = "#e3d6ba"                                              # 'a rather tough paper'
BALSA, BALSA_E = "#d9b98a", "#9a7a52"
TAPE, PINK, PURPLE = "#f3dbe4", "#e0679a", "#9a6ad0"           # the toy company's tape: pale, pink and purple flowers
BAL = "#f1ebe0"                                                # a meteorological balloon
SAND, SAND_E = "#4f4130", "#c9ad85"                            # the map of New Mexico
RIVER = "#6fb6d6"


# ================================================================== narration: the script's own lines, and when each word is said
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")     # a sentence opens with [act:] (and its tags)
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma
SAY, CLK, DUR = {}, {}, {}           # shot key -> its narration, its word clock, its estimated length (set in film())


def END(sid, back=.5):
    return round(max(.5, DUR[sid] - back), 2)


GRAPH, GRAPH_L = "#3b3530", "rgba(59,53,48,.32)"               # pencil on paper, and its faint second stroke
def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # CIA, LSD: letter by letter
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
    for li, ln in enumerate(text.split("\n")):
        if li:
            t += LGAP
        cuts = [m.start() for m in SENT.finditer(ln)]
        cuts = sorted(set([0] + cuts + [len(ln)]))
        for a, z in zip(cuts, cuts[1:]):
            seg = ln[a:z]
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


def grp(els, at, fx="pop", tr=None, **kw):
    """A group that builds in as one piece (its children have no build-ins of their own); tr = an SVG transform."""
    if tr:                                   # the build-in sets the outer group's transform: the turn lives on an inner group
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
    """A grade chip: a dark pill with a coloured rim and its words (scales with the picture, like a plaque)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.92)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", scl=True, fx="pop")]


def tag(x, y, t, at, c=AMBER, size=26, style="known", a="middle"):
    """A small rounded tag with a few words (dashed for an inference, dotted for a claim)."""
    w = len(t) * size * .55 + 30
    x0 = x - w / 2 if a == "middle" else x
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


def typed(x, y, w, n, at, lh=22, c=TYPE, sw=3, dt=.05, seed=1, op=None, short=True):
    """n typed lines on a sheet (grey strokes), the last of a paragraph shorter."""
    rnd = random.Random(seed)
    out = []
    for j in range(n):
        L = w * (rnd.uniform(.55, .8) if (short and j % 4 == 3) else rnd.uniform(.88, 1.0))
        out.append(ln([(x, y + lh * j), (x + L, y + lh * j)], at + dt * j, c, sw, draw=False, op=op))
    return out


def sheet(x, y, w, h, at, fx="rise", c=PAPER, lines=0, seed=1, lh=24, op=None, edge=PAPER_D):
    out = [rect(x, y, w, h, c, edge, 1.5, 3, at, fx=fx, op=op)]
    if lines:
        out += typed(x + w * .1, y + h * .14, w * .8, lines, at + .2, lh, seed=seed)
    return out


def folder(x, y, w, h, at, c=MANILA, fx=None, op=None, edge=MANILA_E, style="known", fill=None):
    """A manila folder seen flat: a body and a tab (x, y = the top left of the body)."""
    e = {"k": "poly", "p": R([[x, y], [x + w * .32, y], [x + w * .36, y - h * .12], [x + w * .62, y - h * .12], [x + w * .66, y], [x + w, y], [x + w, y + h], [x, y + h]]),
         "fill": fill or c, "c": edge, "w": 2, "in": round(at, 2), "style": style}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def abox(x, y, w, h, at, fx=None, op=None, d=None, lab_=True, c=CARD, cs=CARD_S, ct=CARD_T, style="known", out=False):
    """A cardboard archive box seen from the front, a little from above: front face (x, y, w, h), the top face receding,
    a white end label and a hand hole. out=True: pulled forward (a darker rim at the bottom)."""
    d = d if d is not None else h * .22
    els = [poly([[x, y], [x + w, y], [x + w - d * .55, y - d], [x - d * .55 + 0, y - d]], ct, "rgba(255,236,206,.25)", 1, at, fx=fx, op=op, style=style),
           rect(x, y, w, h, c, "rgba(255,236,206,.3)", 1.2, 2, at, fx=fx, op=op, style=style)]
    if lab_:
        els += [rect(x + w * .2, y + h * .18, w * .6, h * .3, "#efe6d2", "none", 0, 2, at, fx=fx, op=op),
                ln([(x + w * .28, y + h * .27), (x + w * .72, y + h * .27)], at, "#6a5a48", 2, draw=False, op=op),
                ln([(x + w * .28, y + h * .38), (x + w * .6, y + h * .38)], at, "#6a5a48", 2, draw=False, op=op),
                poly(E(x + w / 2, y + h * .72, w * .14, h * .07, 16), "#2a1f15", at=at, fx=fx, op=op)]
    if out:
        els.append(rect(x, y + h - 6, w, 6, "#4a3622", at=at, fx=fx, op=op))
    return els


def stamp(x, y, t, at, c=STAMP, size=34, rot=-7, w=None, fx="pop", op=None):
    """A rubber stamp: a ruled frame and its word, tilted, thumped on with a pop."""
    w = w or len(t) * size * .68 + 36
    h = size * 1.55
    els = [{"k": "rect", "x": round(x - w / 2, 1), "y": round(y - h / 2, 1), "w": round(w, 1), "h": round(h, 1), "r": 4, "fill": "none", "c": c, "sw": 4},
           {"k": "label", "x": round(x, 1), "y": round(y + size * .36, 1), "t": t, "st": "lab", "c": c, "size": size, "a": "middle", "halo": False, "scl": True, "weight": 700}]
    e = grp(els, at, fx, tr="rotate(%s %s %s)" % (rot, round(x, 1), round(y, 1)))
    if op is not None:
        e.update(op=op)
    return e


def envelope(x, y, w, at, fx="pop", c=PAPER):
    h = w * .62
    return [rect(x - w / 2, y - h / 2, w, h, c, PAPER_D, 1.5, 3, at, fx=fx),
            ln([(x - w / 2, y - h / 2), (x, y + h * .08), (x + w / 2, y - h / 2)], at, "#9a8a70", 2, draw=False)]


def head(cx, cy, s, at, fill="#2a2420", c="rgba(255,236,206,.35)", w=2, fx=None, op=None, face=1, style="known"):
    """A head and neck in profile (facing right if face=1), about s tall, centred on (cx, cy)."""
    return poly([(cx + face * px * s, cy + py * s) for px, py in HEAD], fill, c, w, at, fx=fx, op=op, curve=True, style=style)


def seated(x, y, h, at, c="#9a9288", stool=True, face=1, fx="rise", op=None):
    """A figure seated facing right (face=1) or left; feet on y, h = standing height."""
    f = face
    X = lambda a: x + f * a
    out = []
    if stool:
        out.append(rect(min(X(-.13 * h), X(.07 * h)), y - .25 * h, .2 * h, .25 * h, "#3a2c20", "#8a6a48", 1.5, 3, at, fx=fx, op=op))
    out += [poly([[X(-.07 * h), y - .63 * h], [X(.11 * h), y - .63 * h], [X(.1 * h), y - .29 * h], [X(-.1 * h), y - .29 * h]], c, at=at, fx=fx, op=op),
            poly([[X(-.1 * h), y - .33 * h], [X(.25 * h), y - .33 * h], [X(.26 * h), y - .25 * h], [X(-.1 * h), y - .24 * h]], c, at=at, fx=fx, op=op),
            poly([[X(.19 * h), y - .27 * h], [X(.26 * h), y - .27 * h], [X(.27 * h), y], [X(.18 * h), y]], c, at=at, fx=fx, op=op),
            circ(X(.04 * h), y - .72 * h, .075 * h, c, at=at, fx=fx, op=op),
            ln([[X(.06 * h), y - .58 * h], [X(.2 * h), y - .5 * h], [X(.3 * h), y - .44 * h]], at, c, max(3, .05 * h), draw=False, op=op)]
    return out


def ppl(x, y, h, at, c="#9a9288", fx="rise", op=None):
    e = person(round(x, 1), round(y, 1), round(h, 1), round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def lamp(x, y, at, cord=110, op=.75, r=260, shade="#3a3129"):
    """A hanging lamp: a cord from above, a shade, the bulb's glow."""
    return [ln([(x, y - cord), (x, y - 14)], at, "#5a5048", 2, draw=False),
            poly([[x - 34, y + 10], [x + 34, y + 10], [x + 16, y - 16], [x - 16, y - 16]], shade, "rgba(255,226,180,.5)", 1.2, at),
            gl(x, y + 18, r, at, op, "lamp"), circ(x, y + 12, 7, "#fff1d2", at=at)]


def cone(x, y, w0, w1, y1, at, op=.1, c="255,214,150"):
    """A cone of lamp light from (x, y), w0 wide at the lamp, w1 wide at y1."""
    return poly([[x - w0 / 2, y], [x + w0 / 2, y], [x + w1 / 2, y1], [x - w1 / 2, y1]], "rgba(%s,%s)" % (c, op), at=at)


def table(x, y, w, at, h=70, top="#5a4632", edge="#8a6a48", legs="#3a2c20", fx=None):
    """A table seen from the front, its top at y (x = centre)."""
    return [rect(x - w / 2, y, w, 14, top, edge, 1.5, 3, at, fx=fx),
            rect(x - w / 2 + 14, y + 14, 12, h, legs, at=at, fx=fx), rect(x + w / 2 - 26, y + 14, 12, h, legs, at=at, fx=fx)]


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


def uni(x, y, s, at, c="#cbbca8", fill="#3a3129", fx="pop", op=None):
    """A university: columns under a pediment, base on y, s = width."""
    h = s * .62
    els = [rect(x - s / 2, y - h, s, h, fill, c, 2, 2, at, fx=fx, op=op),
           poly([[x - s * .58, y - h], [x, y - h - s * .3], [x + s * .58, y - h]], fill, c, 2, at, fx=fx, op=op)]
    els += [rect(x - s * .38 + s * .19 * k - s * .04, y - h * .86, s * .08, h * .86, c, at=at, fx=fx, op=op) for k in range(5)]
    return els


def ink(x, y, t, at, c=INK, size=28, a="middle", st="lab", weight=None, **kw):
    """Text printed or typed on paper: no halo, scales with the picture (it belongs to the page)."""
    e = label(round(x, 1), round(y, 1), t, round(at, 2), c, size, a, st, halo=False, scl=True, **kw)
    if weight:
        e["weight"] = weight
    return e


def note(x, y, t, at, c=TYPE, size=28, a="middle", st="lab", **kw):
    """A label written on a light page: no dark halo, constant size on screen."""
    return label(round(x, 1), round(y, 1), t, round(at, 2), c, size, a, st, halo=False, **kw)


def sketchy(pts, at, c=GRAPH, w=3.0, op=None, dur=None, draw=False, curve=False, off=(1.6, 1.1), ghost=True):
    """A pencil line: the stroke and a faint second stroke beside it, as a hand draws twice."""
    out = [ln(pts, at, c, w, draw=draw, dur=dur, op=op, curve=curve)]
    if ghost:
        out.append(ln([(x + off[0], y + off[1]) for x, y in pts], at, GRAPH_L if c == GRAPH else c, max(1.0, w * .55), draw=draw, dur=dur,
                      op=.45 if op is None else op * .45, curve=curve))
    return out


def inset_map(view, x, y, w, h, at=-1, landc="#3a3024", sea="#12202a", edge="#3c4a58"):
    """A framed map window: the sea, the land clipped to the frame, a rim."""
    return [{"k": "group", "clip": [x, y, w, h, 6], "bg": sea, "els": [{"k": "map", "land": view.land(), "landc": landc}], "in": at},
            rect(x, y, w, h, "none", edge, 2, 6, at)]


def desk_bg(at=-1, top=-20, c=DESK):
    """A desk top filling the panel, a little lighter towards the lamp."""
    return [rect(-20, top, 1820, 1040 - top, c, at=at), gl(1100, 420, 900, at, .16)]


def page_lines(x, y, w, n, at, lh=26, c="#8a7a66", sw=3, seed=1, op=None):
    return typed(x, y, w, n, at, lh, c=c, sw=sw, seed=seed, op=op)


def report_cover(x, y, w, h, at, lines=(), fx="rise", seed=3, body=6):
    """A typed report: a sheet, its title lines (ink), a few body lines."""
    els = [rect(x + 10, y + 14, w, h, "rgba(0,0,0,.45)", at=at, fx=fx), rect(x, y, w, h, PAPER, PAPER_D, 1.5, 3, at, fx=fx)]
    for (t, dy, size, wt) in lines:
        els.append(ink(x + w / 2, y + dy, t, at + .15, TYPE, size, weight=wt))
    if body:
        els += page_lines(x + w * .12, y + h * .62, w * .76, body, at + .3, 24, seed=seed)
    return els


def waves(x0, y0, x1, y1, at, c=LILAC, n=3, dt=.25):
    """Dotted arcs travelling from (x0, y0) towards (x1, y1)."""
    out = []
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    for k in range(n):
        t = (k + 1) / (n + 1)
        cx_, cy_ = x0 + dx * t, y0 + dy * t
        r = 26 + 10 * k
        pts = [(cx_ + ux * (r * .3 * math.cos(math.radians(v))) + nx * r * math.sin(math.radians(v)), cy_ + uy * (r * .3 * math.cos(math.radians(v))) + ny * r * math.sin(math.radians(v)))
               for v in range(-60, 61, 15)]
        out.append(ln(pts, at + dt * k, c, 3, "claimed", draw=False, curve=True))
    return out


def dots_along(pts, at, dur, c=LILAC, r=4, every=1):
    """A dotted trail appearing along a path, dot by dot (a claim: dotted)."""
    out = []
    n = len(pts)
    for k, (x, y) in enumerate(pts[::every]):
        out.append(dot(round(x, 1), round(y, 1), r, c, round(at + dur * k * every / max(1, n - 1), 2)))
    return out


def building(x, y, s, at, kind="block", c="#cbbca8", fill="#2f2822", fx="pop", op=None, lit=()):
    """Small schematic buildings, base on y: 'block' (office), 'columns' (a portico), 'dome' (a capitol), 'hq' (a long block)."""
    els = []
    if kind == "block":
        w, h = s, s * .9
        els.append(rect(x - w / 2, y - h, w, h, fill, c, 2, 2, at, fx=fx, op=op))
        for r_ in range(3):
            for k in range(3):
                i = r_ * 3 + k
                els.append(rect(x - w / 2 + w * (.14 + .27 * k), y - h + h * (.14 + .28 * r_), w * .18, h * .16, GOLD if i in lit else "#15110d", at=at, fx=fx, op=op))
    elif kind == "columns":
        els += uni(x, y, s, at, c, fill, fx, op)
    elif kind == "dome":
        w = s
        els += [rect(x - w / 2, y - w * .32, w, w * .32, fill, c, 2, 2, at, fx=fx, op=op),
                rect(x - w * .2, y - w * .44, w * .4, w * .12, fill, c, 2, 2, at, fx=fx, op=op),
                poly(ellipse(x, y - w * .44, w * .2, w * .2, 18, 180, 360), fill, c, 2, at, fx=fx, op=op),
                ln([(x, y - w * .64), (x, y - w * .74)], at, c, 3, draw=False, op=op)]
        els += [rect(x - w * .42 + w * .12 * k, y - w * .3, w * .05, w * .3, c, at=at, fx=fx, op=op) for k in range(8)]
    elif kind == "hq":
        w, h = s * 1.5, s * .55
        els.append(rect(x - w / 2, y - h, w, h, fill, c, 2, 2, at, fx=fx, op=op))
        for r_ in range(3):
            for k in range(9):
                els.append(rect(x - w / 2 + w * (.04 + .107 * k), y - h + h * (.12 + .29 * r_), w * .06, h * .15, "#15110d", at=at, fx=fx, op=op))
    return els


def tree(x, y, h, at, c="#1c1812", op=None):
    return [poly([(x - h * .22, y - h * .25), (x, y - h), (x + h * .22, y - h * .25)], c, at=at, op=op),
            poly([(x - h * .28, y - h * .02), (x, y - h * .62), (x + h * .28, y - h * .02)], c, at=at, op=op),
            rect(x - h * .03, y - h * .05, h * .06, h * .07, c, at=at, op=op)]


def card(x, y, w, h, at, c="#2a241d", e="#6a5a48", fx="pop", style="known", op=None, r=8):
    return rect(x, y, w, h, c, e, 2, r, at, fx=fx, style=style, op=op)


def bar(x0, x1, y, h, at, c=AMBER, dur=1.0, op=None):
    """A bar growing left to right (a thick line that draws itself)."""
    return ln([(x0, y), (x1, y)], at, c, h, dur=dur, op=op)







# ================================================================== drawings for this film
def rot_pts(pts, cx, cy, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def nl(x, y, t, size, at=-1, c=INK, a="middle", st="serif", weight=None):
    """Newsprint: text that belongs to the page (no halo, scales with the picture)."""
    e = label(round(x, 1), round(y, 1), t, round(at, 2), c, size, a, st, halo=False, scl=True)
    if weight:
        e["weight"] = weight
    return e


def news_lines(x, y, w, n, lh=17, seed=1, c="#9a8f80", sw=4, op=None):
    rnd = random.Random(seed)
    out = []
    for j in range(n):
        L = w * (rnd.uniform(.5, .78) if j % 7 == 6 else rnd.uniform(.9, 1.0))
        out.append(ln([(x, y + lh * j), (x + L, y + lh * j)], -1, c, sw, draw=False, op=op))
    return out


def newspaper(x, y, w, h, kind="8jul", at=-1, fx=None, rot=0.0):
    """A front page of the Roswell Daily Record, its top two thirds: masthead, date, the banner headline in two lines, subheads, columns
    of type. kind '8jul' (RAAF Captures Flying Saucer On Ranch in Roswell Region) or '9jul' (Gen. Ramey Empties Roswell Saucer).
    Returns one group (built in as one piece), tilted by rot degrees about its centre."""
    s = w / 640.0
    X = lambda u: x + u * s
    Y = lambda v: y + v * s
    els = [rect(x + 12 * s, y + 16 * s, w, h, "rgba(0,0,0,.5)"), rect(x, y, w, h, NEWS, NEWS_D, 1.5, 3),
           rect(x + 6 * s, y + 6 * s, w - 12 * s, h - 12 * s, "none", "rgba(120,100,70,.25)", 1, 2)]
    els += [nl(X(320), Y(64), "ROSWELL DAILY RECORD", round(40 * s, 1), weight=600),
            ln([(X(26), Y(82)), (X(614), Y(82))], -1, INK, max(1.0, 2.4 * s), draw=False),
            nl(X(320), Y(108), "Tuesday, 8 July 1947" if kind == "8jul" else "Wednesday, 9 July 1947", round(24 * s, 1), st="lab", c="#4a4038"),
            ln([(X(26), Y(122)), (X(614), Y(122))], -1, INK, max(1.0, 1.2 * s), draw=False)]
    if kind == "8jul":
        els += [nl(X(320), Y(178), "RAAF Captures Flying Saucer", round(45 * s, 1), weight=800),
                nl(X(320), Y(232), "On Ranch in Roswell Region", round(45 * s, 1), weight=800),
                ln([(X(26), Y(254)), (X(614), Y(254))], -1, INK, max(1.0, 1.6 * s), draw=False)]
        els += [nl(X(118), Y(290), "No Details of", round(25 * s, 1), weight=700), nl(X(118), Y(318), "Flying Disk", round(25 * s, 1), weight=700),
                nl(X(118), Y(346), "Are Revealed", round(25 * s, 1), weight=700)]
        els += [nl(X(522), Y(290), "Roswell Hardware", round(22 * s, 1), weight=700), nl(X(522), Y(316), "Man and Wife", round(22 * s, 1), weight=700),
                nl(X(522), Y(342), "Report Disk Seen", round(22 * s, 1), weight=700)]
        els += [ln([(X(220), Y(268)), (X(220), Y(620))], -1, "#8a7f70", max(1.0, 1.2 * s), draw=False),
                ln([(X(422), Y(268)), (X(422), Y(620))], -1, "#8a7f70", max(1.0, 1.2 * s), draw=False)]
        els += news_lines(X(34), Y(372), 172 * s, int((h / s - 380) / 17), 17 * s, 3, sw=max(1.5, 4 * s))
        els += news_lines(X(236), Y(280), 172 * s, int((h / s - 290) / 17), 17 * s, 5, sw=max(1.5, 4 * s))
        els += news_lines(X(438), Y(372), 172 * s, int((h / s - 380) / 17), 17 * s, 7, sw=max(1.5, 4 * s))
    else:
        els += [nl(X(320), Y(184), "Gen. Ramey Empties", round(48 * s, 1), weight=800),
                nl(X(320), Y(240), "Roswell Saucer", round(48 * s, 1), weight=800),
                ln([(X(26), Y(262)), (X(614), Y(262))], -1, INK, max(1.0, 1.6 * s), draw=False)]
        els += [nl(X(160), Y(298), "Harassed Rancher", round(24 * s, 1), weight=700), nl(X(160), Y(326), "who Located 'Saucer'", round(24 * s, 1), weight=700),
                nl(X(160), Y(354), "Sorry He Told About It", round(24 * s, 1), weight=700)]
        els += [ln([(X(310), Y(276)), (X(310), Y(620))], -1, "#8a7f70", max(1.0, 1.2 * s), draw=False)]
        els += news_lines(X(34), Y(380), 262 * s, int((h / s - 388) / 17), 17 * s, 11, sw=max(1.5, 4 * s))
        els += news_lines(X(326), Y(288), 280 * s, int((h / s - 296) / 17), 17 * s, 13, sw=max(1.5, 4 * s))
    tr = "rotate(%s %s %s)" % (rot, round(x + w / 2, 1), round(y + h / 2, 1)) if rot else None
    return grp(els, at, fx, tr=tr)


def windmill(x, y, h, at=-1, c=SIL, rim="rgba(255,214,160,.28)", op=None):
    """A ranch windmill: a lattice tower on y, the wheel at the top, a tail vane."""
    w0, w1 = h * .16, h * .05
    top = y - h
    els = [ln([(x - w0, y), (x - w1, top)], at, c, max(2.0, h * .016), draw=False, op=op), ln([(x + w0, y), (x + w1, top)], at, c, max(2.0, h * .016), draw=False, op=op)]
    for k in range(1, 6):
        t0, t1 = (k - 1) / 5, k / 5
        xa, xb = x - w0 + (w0 - w1) * t0, x + w0 - (w0 - w1) * t1
        els.append(ln([(xa, y - h * t0), (xb, y - h * t1)], at, c, max(1.2, h * .007), draw=False, op=op))
        els.append(ln([(x - w0 + (w0 - w1) * t1, y - h * t1), (x + w0 - (w0 - w1) * t1, y - h * t1)], at, c, max(1.2, h * .007), draw=False, op=op))
    R0 = h * .2
    cx, cy = x - h * .02, top - h * .02
    for k in range(14):
        a = math.radians(360 * k / 14)
        els.append(ln([(cx + R0 * .25 * math.cos(a), cy + R0 * .25 * math.sin(a)), (cx + R0 * math.cos(a), cy + R0 * math.sin(a))], at, c, max(1.8, h * .012), draw=False, op=op))
    els += [circ(cx, cy, R0, "none", c, max(1.2, h * .008), at, op=op), circ(cx, cy, R0 * .25, c, at=at, op=op),
            poly([(cx + h * .02, cy - h * .015), (cx + h * .3, cy - h * .05), (cx + h * .3, cy + h * .06), (cx + h * .02, cy + h * .015)], c, rim, 1, at, op=op)]
    return els


def fence(x0, y0, x1, y1, n, h0, h1, at=-1, c="#2a1f16", wire="rgba(225,205,175,.6)", op=None):
    """A wire fence in perspective: n posts from (x0, y0) (near, h0 tall) to (x1, y1) (far, h1 tall), three wires."""
    els, tops = [], []
    for k in range(n):
        t = k / (n - 1)
        tt = t ** .7
        x, y, h = x0 + (x1 - x0) * tt, y0 + (y1 - y0) * tt, h0 + (h1 - h0) * tt
        els.append(ln([(x, y), (x, y - h)], at, c, max(2.4, h * .085), draw=False, op=op))
        els.append(ln([(x + max(1.0, h * .03), y), (x + max(1.0, h * .03), y - h)], at, "rgba(255,226,190,.22)", max(1.0, h * .02), draw=False, op=op))
        tops.append((x, y, h))
    for f in (.35, .62, .9):
        els.append(ln([(x_, y_ - h_ * f) for x_, y_, h_ in tops], at, wire, 1.4, draw=False, op=op))
    return els


def scrub(seed, n, x0, x1, y0, y1, at=-1, c=SCRUB, s=1.0, op=None, rim="rgba(255,220,170,.16)"):
    """Low desert bushes: each a cluster of three or four overlapping rounded lobes, bigger nearer the viewer."""
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        k = s * (.45 + .75 * (y - y0) / max(1, y1 - y0))
        lobes = [(r.uniform(-14, 14) * k, -r.uniform(4, 12) * k, r.uniform(8, 14) * k) for _ in range(r.randint(3, 4))]
        for dx, dy, rr in lobes:
            out.append(circ(x + dx, y + dy, rr, c, rim, 1, at, op=op))
        out.append(poly(E(x, y + 1, 22 * k, 4 * k, 12), "rgba(0,0,0,.25)", at=at))
    return out


def glints(seed, n, x0, x1, y0, y1, at=-1, s=1.0, glow_=True):
    """Bits of foil catching the light in the grass: small bright diamonds, a few with a halo."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        d = r.uniform(4, 8) * s
        a = r.uniform(0, 1.5)
        pts = [(x + d * math.cos(a + q * math.pi / 2) * (1.6 if q % 2 == 0 else .7), y + d * math.sin(a + q * math.pi / 2) * (1.6 if q % 2 == 0 else .7)) for q in range(4)]
        if glow_ and k % 3 == 0:
            out.append(gl(x, y, 26 * s, at, .5, "lamp"))
        out.append(poly(pts, FOIL, FOIL_E, 1, at))
    return out


def sticks_scatter(seed, n, x0, x1, y0, y1, at=-1, s=1.0):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        L, a = r.uniform(26, 48) * s, r.uniform(-.5, .5)
        out.append(ln([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], at, BALSA, 3.2 * s, draw=False))
    return out


# ---------------------------------------------------------------- New Mexico
NM = [(-109.05, 37.0), (-103.0, 37.0), (-103.0, 36.5), (-103.04, 36.5), (-103.06, 32.0), (-106.62, 32.0), (-106.53, 31.78),
      (-108.21, 31.78), (-108.21, 31.33), (-109.05, 31.33)]
RIO = [(-105.72, 37.0), (-105.95, 36.4), (-106.25, 35.85), (-106.62, 35.1), (-106.75, 34.6), (-106.88, 34.05), (-107.05, 33.6), (-107.25, 33.1),
       (-107.0, 32.65), (-106.75, 32.25), (-106.62, 32.0), (-106.53, 31.78)]
PECOS = [(-105.55, 35.75), (-105.15, 35.2), (-104.7, 34.85), (-104.45, 34.45), (-104.4, 33.9), (-104.45, 33.4), (-104.37, 32.85), (-104.2, 32.42),
         (-103.95, 32.0)]
PLACES = {"Roswell": (-104.52, 33.39), "RAAF": (-104.53, 33.30), "ranch": (-105.30, 33.95), "Corona": (-105.60, 34.25), "Alamogordo": (-106.10, 32.85),
          "Albuquerque": (-106.65, 35.08), "Santa Fe": (-105.94, 35.69), "San Agustin": (-107.70, 34.10), "north": (-104.52, 33.88)}


def nm_map(v, at=-1, op=None, rivers=True):
    els = [poly([v.p(lo, la) for lo, la in NM], SAND, SAND_E, 2.2, at, op=op)]
    if rivers:
        els += [ln([v.p(lo, la) for lo, la in RIO], at, RIVER, 2.4, draw=False, curve=True, op=.55 if op is None else op * .55),
                ln([v.p(lo, la) for lo, la in PECOS], at, RIVER, 2.0, draw=False, curve=True, op=.5 if op is None else op * .5)]
    return els


# ---------------------------------------------------------------- the things that fell, and the things they came from
def saucer(x, y, s, at, c=LILAC, style="claimed", fx="pop", w=3, fill="rgba(201,193,238,.10)"):
    """The legend's flying saucer: a lens and a dome, drawn dotted (a claim)."""
    els = [poly(E(x, y, 150 * s, 30 * s, 40), fill, c, w, at, fx=fx, curve=True, style=style),
           poly(ellipse(x, y - 14 * s, 62 * s, 44 * s, 20, 180, 360), fill, c, w, at, fx=fx, curve=True, style=style)]
    return els


def balloon(x, y, r, at, fx="rise", c=BAL, string=0, op=None, sc="#cbbca8"):
    """A meteorological balloon: an oval a little taller than wide, a neck; optional string below."""
    els = []
    if string:
        els.append(ln([(x, y + r * 1.15), (x, y + r * 1.15 + string)], at, sc, max(1.2, r * .06), draw=False, op=op))
    els += [poly(E(x, y, r, r * 1.1, 24), c, "rgba(255,255,255,.9)", max(1.0, r * .05), at, fx=fx, op=op, curve=True),
            poly([(x - r * .16, y + r * 1.02), (x + r * .16, y + r * 1.02), (x + r * .08, y + r * 1.2), (x - r * .08, y + r * 1.2)], "#d8d0c2", at=at, fx=fx, op=op),
            poly(E(x - r * .35, y - r * .4, r * .22, r * .3, 12), "rgba(255,255,255,.6)", at=at, fx=fx, op=op, curve=True)]
    return els


def reflector(cx, cy, r, at, fx="pop", tape=True, op=None, edge=BALSA, sw=None):
    """A radar reflector of the kind Mogul flew: balsa sticks and foil-backed paper, seen corner-on as a hexagon of six facets."""
    sw = sw or max(1.5, r * .035)
    V = [(cx + r * math.cos(math.radians(90 + 60 * k)), cy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    els = []
    for k in range(6):
        a, b = V[k], V[(k + 1) % 6]
        els.append(poly([(cx, cy), a, b], "#e9eef2" if k % 2 == 0 else "#9ea6ae", "none", 0, at, fx=fx, op=op))
    for k in range(6):
        a, b = V[k], V[(k + 1) % 6]
        els.append(ln([(cx, cy), a], at, edge, sw, draw=False, op=op))
        els.append(ln([a, b], at, edge, sw, draw=False, op=op))
    if tape:
        for k in (0, 2, 4):
            a = V[k]
            for t in (.3, .62):
                px, py = cx + (a[0] - cx) * t, cy + (a[1] - cy) * t
                els.append(circ(px, py, max(1.6, r * .03), PINK, at=at, fx=fx, op=op))
    return els


def flower(x, y, r, at, c=PINK, fx=None, op=None):
    els = [circ(x + r * .55 * math.cos(math.radians(72 * k - 90)), y + r * .55 * math.sin(math.radians(72 * k - 90)), r * .45, c, at=at, fx=fx, op=op) for k in range(5)]
    els.append(circ(x, y, r * .3, "#f7e08a", at=at, fx=fx, op=op))
    return els


def tape_strip(x0, y0, x1, y1, at, w=16, fx="pop", n=None, op=None):
    """The toy company's tape: a pale strip with pink and purple flowers and little diamonds along it."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy * w / 2, ux * w / 2
    els = [poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], TAPE, "rgba(200,150,170,.8)", 1, at, fx=fx, op=op)]
    n = n or max(2, int(L / (w * 2.2)))
    for k in range(n):
        t = (k + .5) / n
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if k % 3 == 1:
            d = w * .26
            els.append(poly([(px - d, py), (px, py - d), (px + d, py), (px, py + d)], PURPLE, at=at, fx=fx, op=op))
        else:
            els += flower(px, py, w * .34, at, PINK if k % 2 == 0 else PURPLE, fx, op)
    return els


def stick(x0, y0, x1, y1, at, w=8, fx=None, op=None):
    """A square balsa stick: a darker edge under a light core."""
    els = [ln([(x0, y0), (x1, y1)], at, BALSA_E, w + 2, draw=False, op=op), ln([(x0, y0), (x1, y1)], at, BALSA, w, draw=False, op=op)]
    if fx:
        for e in els:
            e["fx"] = fx
    return els


def rubber(x, y, L, at, k=0, w=9, op=None):
    pts = [(x + L * t, y + 10 * math.sin(t * 7 + k) + 4 * math.sin(t * 17 + k)) for t in [j / 10 for j in range(11)]]
    return [ln(pts, at, RUBBER, w, draw=False, curve=True, op=op), ln([(px, py - w * .25) for px, py in pts], at, "rgba(255,255,255,.18)", 1.5, draw=False, curve=True, op=op)]


def foil(x, y, s, at, fx="pop", op=None):
    pts = [(-60, 8), (-48, -36), (-14, -28), (6, -52), (40, -30), (58, 6), (30, 26), (0, 16), (-30, 30)]
    P = [(x + px * s, y + py * s) for px, py in pts]
    return [poly(P, FOIL, FOIL_E, 2, at, fx=fx, op=op),
            ln([(x - 40 * s, y - 10 * s), (x - 6 * s, y - 20 * s), (x + 30 * s, y - 6 * s)], at, "#ffffff", 2, draw=False, op=op),
            ln([(x - 20 * s, y + 12 * s), (x + 10 * s, y + 2 * s)], at, "#9ea6ae", 2, draw=False, op=op)]


def scrap(x, y, s, at, fx="pop", op=None):
    pts = [(-56, -40), (-10, -46), (4, -36), (50, -42), (56, 30), (20, 38), (6, 30), (-52, 36)]
    P = [(x + px * s, y + py * s) for px, py in pts]
    return [poly(P, TOUGH, "#9a8a70", 2, at, fx=fx, op=op), ln([(x - 30 * s, y - 40 * s), (x - 24 * s, y + 34 * s)], at, "#b9a98a", 1.6, draw=False, op=op)]


def person_hat(x, y, h, at, c="#9a9288", fx="rise", op=None):
    """A standing figure with a hat brim (a rancher)."""
    els = [ppl(x, y, h, at, c, fx, op)]
    els.append(rect(x - h * .085, y - h * 1.0, h * .17, h * .05, c, at=at, fx=fx, op=op))
    els.append(rect(x - h * .05, y - h * 1.04, h * .1, h * .06, c, at=at, fx=fx, op=op))
    return els


def horse(x, y, s, at, c="#2a2018", fx="rise", op=None, face=1, rider="#3a2c22"):
    """A horse in side view, hooves on y (about 190 * s tall at the ears), with a rider in a hat."""
    f = face
    P = lambda u, v: (x + f * u * s, y + v * s)
    body = [P(-72, -118), P(-40, -126), P(20, -124), P(45, -132), P(62, -150), P(84, -178), P(100, -190), P(112, -188), P(134, -166), P(130, -157),
            P(108, -160), P(96, -150), P(80, -122), P(68, -96), P(40, -86), P(-30, -84), P(-62, -88), P(-76, -100)]
    els = [poly(body, c, "rgba(255,226,190,.28)", 1.2, at, fx=fx, op=op, curve=True)]
    for leg in ([(52, -90), (56, -46), (50, 0)], [(40, -88), (44, -46), (37, 0)], [(-50, -88), (-62, -48), (-54, 0)], [(-62, -90), (-74, -46), (-67, 0)]):
        els.append(ln([P(u, v) for u, v in leg], at, c, 7 * s, draw=False, op=op))
    els.append(ln([P(-74, -112), P(-90, -88), P(-94, -58)], at, c, 7 * s, draw=False, op=op, curve=True))
    els.append(poly([P(98, -192), P(104, -206), P(108, -190)], c, at=at, fx=fx, op=op))
    if rider:
        els += [poly([P(-2, -126), P(18, -126), P(22, -186), P(0, -188)], rider, "rgba(255,226,190,.25)", 1, at, fx=fx, op=op),
                circ(*P(11, -202), 11 * s, rider, at=at, fx=fx, op=op),
                rect(P(-6, -210)[0] if f > 0 else P(28, -210)[0], P(0, -212)[1], 34 * s, 4 * s, rider, at=at, fx=fx, op=op),
                rect(P(3, -224)[0] if f > 0 else P(19, -224)[0], P(0, -224)[1], 16 * s, 12 * s, rider, at=at, fx=fx, op=op),
                ln([P(8, -128), P(26, -104), P(22, -78)], at, rider, 7 * s, draw=False, op=op),
                ln([P(16, -170), P(46, -150), P(92, -166)], at, rider, 4 * s, draw=False, op=op)]
    return els


def b29(x, y, s, at=-1, c=SIL, rim="rgba(255,226,190,.4)", op=None):
    """A B-29 in side view on its wheels; x = middle, y = ground, s = units per metre (length 30 m, tail 8.5 m)."""
    P = lambda u, v: (x + u * s, y - v * s)
    fus = [P(-15, 4.0), P(-14.6, 5.0), P(-13.4, 5.6), P(-9, 5.8), P(10, 5.6), P(14.6, 5.0), P(15.3, 4.6), P(15, 3.9), P(10, 3.3), P(-9, 2.9), P(-13.8, 3.0), P(-14.8, 3.4)]
    fin = [P(9.8, 5.4), P(12.6, 8.6), P(14.4, 8.6), P(15.2, 5.0)]
    stab = [P(11.2, 5.1), P(15.6, 5.4), P(15.6, 5.0), P(11.6, 4.8)]
    wing = [P(-4.5, 4.25), P(4.0, 4.4), P(4.0, 4.1), P(-4.5, 3.95)]
    els = [poly(fin, c, rim, 1.2, at, op=op), poly(stab, c, rim, 1.2, at, op=op), poly(fus, c, rim, 1.4, at, op=op, curve=True), poly(wing, c, rim, 1, at, op=op)]
    for u0 in (-5.6, -1.2):
        els.append(poly([P(u0, 3.75), P(u0 + 3.6, 3.85), P(u0 + 3.9, 3.35), P(u0 + .3, 3.2)], c, rim, 1, at, op=op, curve=True))
        els.append(ln([P(u0 - .15, 2.3), P(u0 - .15, 5.2)], at, "rgba(255,226,190,.35)", max(1.0, .12 * s), draw=False, op=op))
    els += [ln([P(.6, 3.2), P(.6, .7)], at, c, max(2.0, .25 * s), draw=False, op=op), circ(*P(.6, .65), .65 * s, c, rim, 1, at, op=op),
            ln([P(-12.2, 3.0), P(-12.2, .5)], at, c, max(1.6, .18 * s), draw=False, op=op), circ(*P(-12.2, .5), .5 * s, c, rim, 1, at, op=op),
            poly([P(-15, 4.0), P(-14.6, 5.0), P(-13.6, 5.2), P(-14.2, 4.0)], "rgba(255,226,180,.25)", at=at, op=op)]
    return els


def hangar(x, y, w, h, at=-1, c="#1b1612", rim="rgba(255,226,190,.3)", lit=True, op=None):
    """An arched hangar seen from the front: base on y."""
    arch = ellipse(x + w / 2, y - h * .62, w / 2, h * .38, 24, 180, 360)
    els = [poly([(x, y), (x, y - h * .62)] + [tuple(p) for p in arch] + [(x + w, y - h * .62), (x + w, y)], c, rim, 1.4, at, op=op)]
    els.append(rect(x + w * .14, y - h * .5, w * .72, h * .5, "#2a221b", rim, 1, 0, at, op=op))
    if lit:
        els.append(rect(x + w * .47, y - h * .5, w * .06, h * .5, "rgba(255,214,150,.75)", at=at, op=op))
        els.append(gl(x + w * .5, y - h * .1, w * .3, at, .3))
    return els


def tower(x, y, h, at=-1, c="#1b1612", rim="rgba(255,226,190,.3)", op=None):
    w = h * .14
    els = [rect(x - w / 2, y - h * .8, w, h * .8, c, rim, 1, 0, at, op=op),
           rect(x - w * 1.1, y - h, w * 2.2, h * .2, "#2a221b", rim, 1.2, 2, at, op=op),
           rect(x - w * .95, y - h * .97, w * 1.9, h * .12, "rgba(255,214,150,.8)", at=at, op=op),
           gl(x, y - h * .9, h * .45, at, .35)]
    return els


def truck(x, y, s, at, c="#3a3029", rim="rgba(255,226,190,.35)", fx="rise", op=None, load=False, face=1):
    """A 1940s pickup in side view, wheels on y, about 300 * s long."""
    f = face
    P = lambda u, v: (x + f * u * s, y - v * s)
    body = [P(-150, 30), P(-150, 80), P(10, 80), P(20, 120), P(80, 124), P(98, 86), P(150, 78), P(158, 40), P(150, 30)]
    els = [poly(body, c, rim, 1.4, at, fx=fx, op=op, curve=False),
           poly([P(28, 112), P(76, 116), P(88, 88), P(28, 88)], "#6a7a86", at=at, fx=fx, op=op)]
    for u in (-100, 100):
        els += [circ(*P(u, 26), 26 * s, "#15110e", rim, 1.2, at, fx=fx, op=op), circ(*P(u, 26), 9 * s, "#6a6058", at=at, fx=fx, op=op)]
    if load:
        for k in range(3):
            els.append(rect(x + f * (-142 + 46 * k) * s - (44 * s if f < 0 else 0), y - 118 * s, 44 * s, 40 * s, "#ece4d4", "#a89c88", 1.2, 6 * s, at, fx=fx, op=op))
    return els


def calendar(x, y, w, day, month, at, c=GOLD, fx="pop", year="1947"):
    h = w * 1.12
    els = [rect(x - w / 2 + 6, y + 8, w, h, "rgba(0,0,0,.45)", at=at, fx=fx), rect(x - w / 2, y, w, h, PAPER, PAPER_D, 1.5, 4, at, fx=fx),
           rect(x - w / 2, y, w, h * .26, c, at=at, fx=fx)]
    els += [ink(x, y + h * .19, month.upper(), at + .05, "#2a1f15", round(max(24, w * .14), 1), weight=700),
            ink(x, y + h * .74, str(day), at + .05, TYPE, round(w * .42, 1), st="serif", weight=600)]
    if year:
        els.append(ink(x, y + h * .92, year, at + .05, "#6a5a48", round(max(24, w * .12), 1)))
    return els


def plane_icon(x, y, s, at, c="#3a3532", fx="pop", op=None):
    """A small aircraft seen from above, nose up."""
    P = lambda u, v: (x + u * s, y + v * s)
    return [poly([P(0, -50), P(5, -40), P(5, -8), P(46, 4), P(46, 12), P(5, 6), P(4, 34), P(16, 42), P(16, 48), P(0, 44), P(-16, 48), P(-16, 42), P(-4, 34),
                  P(-5, 6), P(-46, 12), P(-46, 4), P(-5, -8), P(-5, -40)], c, "rgba(255,236,206,.4)", 1.2, at, fx=fx, op=op)]


def gondola(x, y, s, at, tilt=0, c="#8a96a2", fx="pop", op=None):
    pts = [(-30, -40), (30, -40), (34, 0), (-34, 0)]
    pts = rot_pts([(x + u * s, y + v * s) for u, v in pts], x, y, tilt)
    return [poly(pts, c, "#e8eef2", 1.5, at, fx=fx, op=op), poly(rot_pts([(x - 14 * s, y - 32 * s), (x + 14 * s, y - 32 * s), (x + 14 * s, y - 18 * s), (x - 14 * s, y - 18 * s)], x, y, tilt),
                                                                   "#1e2a33", at=at, fx=fx, op=op)]


def parachute(x, y, w, at, c="#f1ebe0", fx="pop", op=None):
    """A canopy (top at y) and its lines down to a point w * .9 below."""
    can = ellipse(x, y + w * .32, w / 2, w * .32, 18, 180, 360)
    els = [poly([tuple(p) for p in can], c, "#b9ab94", 1.4, at, fx=fx, op=op, curve=True)]
    for u in (-.5, -.2, .2, .5):
        els.append(ln([(x + u * w, y + w * .32), (x, y + w * .95)], at, "#cbbca8", 1.2, draw=False, op=op))
    return els


def dummy(x, y, h, at, fx="pop", op=None, c="#a8aeb4"):
    """A test dummy: a plain human shape, grey, no face."""
    return [ppl(x, y, h, at, c, fx, op)]


def book(x, y, w, h, at, c, t=None, fx="pop", tc="#f5ecdc", size=20):
    els = [rect(x, y, w, h, c, "rgba(255,236,206,.35)", 1.2, 2, at, fx=fx), rect(x + 3, y + h * .1, w - 6, 3, "rgba(255,236,206,.5)", at=at, fx=fx),
           rect(x + 3, y + h * .86, w - 6, 3, "rgba(255,236,206,.5)", at=at, fx=fx)]
    if t:
        els.append(grp([nl(x + w / 2 + size * .35, y + h / 2, t, size, -1, tc, st="lab", weight=600)], at, fx,
                       tr="rotate(-90 %s %s)" % (round(x + w / 2 + size * .35, 1), round(y + h / 2, 1))))
    return els


def dish(x, y, s, at, c="#cbbca8", fx="pop"):
    """A tracking radar: a pedestal and a round dish tilted up to the left (x, y = the foot of the pedestal)."""
    cx, cy = x, y - 110 * s
    rim = [(cx + 80 * s * math.cos(math.radians(a)) * .45, cy + 80 * s * math.sin(math.radians(a))) for a in range(0, 361, 15)]
    rim = rot_pts(rim, cx, cy, 35)
    return [rect(x - 50 * s, y - 16 * s, 100 * s, 16 * s, "#3a3129", c, 1.5, 3, at, fx=fx), rect(x - 10 * s, y - 100 * s, 20 * s, 86 * s, "#4a4038", c, 1.5, 2, at, fx=fx),
            poly(rim, "#6a625a", c, 2.4, at, fx=fx, curve=True), ln(rot_pts([(cx, cy), (cx - 70 * s, cy)], cx, cy, 35), at, c, 2.4, draw=False),
            circ(*rot_pts([(cx - 70 * s, cy)], cx, cy, 35)[0], 6 * s, c, at=at, fx=fx)]


def pitch(x, y, w, h, at, fx="rise", op=None):
    """A football pitch standing on end: x, y = top left; w = its width (68 m), h = its length (105 m)."""
    lc = "rgba(255,255,255,.85)"
    els = [rect(x, y, w, h, "#2f6b3a", "none", 0, 0, at, fx=fx, op=op)]
    for k in range(7):
        els.append(rect(x, y + h * k / 7, w, h / 14, "rgba(255,255,255,.05)", at=at, fx=fx, op=op))
    els += [rect(x + 4, y + 4, w - 8, h - 8, "none", lc, 2, 0, at, fx=fx, op=op), ln([(x + 4, y + h / 2), (x + w - 4, y + h / 2)], at, lc, 2, draw=False, op=op),
            circ(x + w / 2, y + h / 2, w * .135, "none", lc, 2, at, fx=fx, op=op),
            rect(x + w * .2, y + 4, w * .6, h * .157, "none", lc, 2, 0, at, fx=fx, op=op), rect(x + w * .2, y + h - 4 - h * .157, w * .6, h * .157, "none", lc, 2, 0, at, fx=fx, op=op)]
    return els


def train_icon(x, y, h, at, fx="pop", n=7, op=None):
    """A small Mogul train: balloons on a line, a reflector, a box at the bottom (x, y = top)."""
    els = [ln([(x, y), (x, y + h)], at, "#cbbca8", 2, draw=False, op=op)]
    for k in range(n):
        els += balloon(x, y + k * h * .09, h * .035, at, fx, op=op)
    els += reflector(x, y + h * .78, h * .06, at, fx, tape=False, op=op)
    els.append(rect(x - h * .03, y + h * .94, h * .06, h * .06, "#3a3532", "#cbbca8", 1, 2, at, fx=fx, op=op))
    return els


def tv(x, y, w, h, at, fx=None):
    """An old cathode ray television: a cabinet, a curved grey screen (x, y = the screen's top left)."""
    els = [rect(x - w * .1, y - h * .1, w * 1.2, h * 1.32, "#2a2420", "#6a5a48", 2, 18, at, fx=fx),
           rect(x, y, w, h, "#55595c", "#1a1714", 3, 26, at, fx=fx),
           rect(x + w * .86, y + h * 1.06, w * .06, h * .06, "#6a5a48", at=at, fx=fx), rect(x + w * .74, y + h * 1.06, w * .06, h * .06, "#6a5a48", at=at, fx=fx),
           ln([(x + w * .3, y - h * .1), (x + w * .16, y - h * .42)], at, "#8a7a66", 3, draw=False), ln([(x + w * .7, y - h * .1), (x + w * .84, y - h * .42)], at, "#8a7a66", 3, draw=False)]
    return els


def grain(seed, n, x0, x1, y0, y1, at, c="#d8d8d8", op=.25):
    r = random.Random(seed)
    return [dot(round(r.uniform(x0, x1), 1), round(r.uniform(y0, y1), 1), round(r.uniform(1.0, 2.4), 1), c, round(at, 2), None, op=round(r.uniform(.1, op), 2)) for _ in range(n)]


def figure(x, y, h, at, c="#a39a8e", fx="rise", op=None, hat=False):
    return person_hat(x, y, h, at, c, fx, op) if hat else [ppl(x, y, h, at, c, fx, op)]


def ghost_person(x, y, h, at, c=LILAC, style="claimed", w=2.4, fx="pop", op=None):
    """A person drawn as a dotted outline (a figure that is claimed, not recorded)."""
    wd = h * .26
    body = [(x - wd * .5, y - h * .78), (x + wd * .5, y - h * .78), (x + wd * .42, y - h * .42), (x + wd * .3, y), (x + wd * .08, y), (x, y - h * .36),
            (x - wd * .08, y), (x - wd * .3, y), (x - wd * .42, y - h * .42)]
    return [poly(body, "rgba(201,193,238,.08)", c, w, at, fx=fx, op=op, style=style), circ(x, y - h * .9, h * .085, "rgba(201,193,238,.08)", c, w, at, fx=fx, op=op, style=style)]


def ranch(at=-1, fence_=True, mill=(560, 640, 290), glint=True, night=False, seed=3):
    """The ranch country at the left of the frame: a mesa, scrub, a windmill, a wire fence, foil glints in the grass."""
    els = [poly([(-20, 612), (60, 566), (300, 556), (350, 586), (520, 592), (570, 612)], "#2c2228" if not night else "#151420", at=at)]
    els += scrub(seed, 16, 80, 1000, 640, 790, at, "#262619" if night else SCRUB, s=.9)
    if mill:
        els += windmill(*mill, at, SIL)
    if fence_:
        els += fence(470, 812, 990, 628, 8, 120, 18, at)
    if glint:
        els += glints(seed + 2, 16, 200, 900, 676, 788, at)
        els += sticks_scatter(seed + 4, 7, 260, 820, 692, 780, at)
        els += rubber(430, 744, 60, at, 2, w=6) + rubber(700, 716, 52, at, 4, w=5)
    return els


# ================================================================== cold open
NP_HERO = (1000, 150, 640, 628)


def sc_hero():
    """s1, the hero image, fully drawn from the first frame: the Roswell Daily Record of 8 July 1947 (RAAF Captures Flying Saucer On
    Ranch in Roswell Region) over the ranch country at dusk: a windmill, a wire fence, foil glinting in the grass. Labels build after
    the hook title: '8 July 1947', 'Roswell, New Mexico'."""
    els = ranch()
    els += [gl(1320, 430, 640, -1, .14)]
    els += [newspaper(*NP_HERO, kind="8jul", at=-1, rot=-3)]
    els += [lab(130, 742, "8 July 1947", T("hero", "eighth", lead=.1), GOLD, 30, "start", st="cap"),
            lab(130, 784, "Roswell, New Mexico", T("hero", "Roswell"), BONE, 30, "start")]
    return {"base": "sky", "tod": "dusk", "ground": 612, "groundc": "url(#k-ground)", "sun": [300, 566, 26], "cam": CAM, "els": els}


def sc_base():
    """s2: Roswell Army Air Field at dusk: a runway, hangars, the tower, a B-29 on the apron; 'Roswell Army Air Field', then '509th Bomb
    Group', then a tag: the world's only atomic bomb unit."""
    els = [poly([(260, 800), (1380, 800), (960, 604), (820, 604)], "#2a241e", "rgba(255,226,190,.18)", 1.2, -1),
           ln([(820, 800), (889, 604)], -1, "#cbbca8", 3, "inferred", draw=False, op=.45)]
    els += hangar(1150, 602, 210, 120) + hangar(1390, 602, 210, 120, lit=False) + tower(1040, 602, 180)
    els += [ln([(980, 602), (980, 470)], -1, "#3a3029", 3, draw=False), poly([(982, 472), (1030, 480), (982, 490)], "#8a3a30", at=-1)]
    els += b29(560, 772, 16)
    els += [gl(560, 700, 420, -1, .1)]
    tb, th, ta = T("base", "base itself"), T("base", "home to"), T("base", "atomic bombs")
    els += [lab(1395, 440, "Roswell Army Air Field", tb, BONE, 30),
            lab(560, 610, "509th Bomb Group", th, GOLD, 32)]
    els += tag(1130, 712, "the world's only", ta, AMBER, 26) + tag(1130, 756, "atomic bomb unit", ta + .15, AMBER, 26)
    return {"base": "sky", "tod": "dusk", "ground": 602, "groundc": "url(#k-ground)", "sun": [1560, 548, 22], "cam": CAM, "els": els}


def sc_nextday():
    """s3: the next day's front page (Gen. Ramey Empties Roswell Saucer) rises beside the first; a weather balloon with a radar
    reflector rises between them; 'Flying Saucer' on the first page is struck through."""
    els = desk_bg()
    x, y, w, h, r = 140, 150, 560, 520, 2
    els += [newspaper(x, y, w, h, kind="8jul", at=-1, rot=r)]
    els += [newspaper(1060, 168, 580, 520, kind="9jul", at=.4, fx="rise", rot=-3)]
    tw = T("nextday", "weather balloon")
    els += [gl(880, 330, 220, tw - .4, .45)] + balloon(880, 300, 54, tw - .4, "rise", string=170)
    els += [grp(reflector(880, 560, 50, -1, None), tw, "pop")]
    s = w / 640.0
    a, b = rot_pts([(x + 378 * s, y + 166 * s), (x + 604 * s, y + 166 * s)], x + w / 2, y + h / 2, r)
    els += [ln([a, b], tw + .3, RED, 7, dur=.5)]
    els += [lab(880, 224, "a weather balloon", tw + .3, BONE, 28),
            lab(x + w / 2, 728, "8 July", .3, GOLD, 28), lab(1350, 744, "9 July", .6, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


TL_X = lambda yr: round(170 + (yr - 1940) / 90 * 1440, 1)


def sc_slept():
    """s4: a time line 1940 to 2030: 1947, then thirty quiet years, then from 1978 the line lights and the legend's icons pop
    (dotted: claims): a crashed craft, alien bodies, a cover-up."""
    X = TL_X
    ticks = [(X(y_), str(y_)) for y_ in (1940, 1960, 1980, 2000, 2020)]
    els = [axis(170, 1610, 600, ticks, .1), dot(X(1947), 600, 13, AU, .3), lab(X(1947), 556, "1947", .3, AU, 30)]
    t30, tw = T("slept", "thirty years"), T("slept", "woke")
    els += [ln([(X(1947) + 18, 572), (X(1978) - 6, 572)], t30 - .3, MUTED, 3, "inferred", 1.2), lab((X(1947) + X(1978)) / 2, 540, "30 quiet years", t30 + .4, MUTED, 28)]
    els += [dot(X(1978), 600, 11, LILAC, tw - .2), lab(X(1978), 556, "1978", tw - .2, LILAC, 30), bar(X(1978) + 8, X(2026), 600, 8, tw, LILAC, 1.4)]
    tc, tb, tu = T("slept", "crashed craft"), T("slept", "alien bodies"), T("slept", "cover-up")
    els += saucer(X(1991), 420, .55, tc - .2) + [lab(X(1991), 500, "a crashed craft", tc, LILAC, 26)]
    els += ghost_person(X(2005), 470, 120, tb - .2) + [lab(X(2005), 500, "alien bodies", tb, LILAC, 26)]
    els += [folder(X(2019) - 80, 352, 160, 100, tu - .2, MANILA, fx="pop", style="claimed"),
            stamp(X(2019), 404, "COVER-UP", tu, STAMP, 24, -6), lab(X(2019), 500, "a cover-up", tu + .1, LILAC, 26)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def sc_night():
    """s5: the ranch at night: a few glints of debris in the grass under a lilac question mark; at the right a tall stack of what grew
    from it (books, film reels, a museum front), far larger than the debris. (The title card is shown over this panel.)"""
    els = ranch(night=True, glint=False, mill=(300, 640, 270))
    els += glints(21, 9, 420, 760, 690, 770, -1, .9)
    tq, tk, tf = T("night", "what really"), T("night", "few kilos"), T("night", "most famous")
    els += qmark(575, 520, tq, 100)
    els += [lab(575, 772, "a few kilos", tk, MUTED, 28)]
    cols = ["#7a4a3a", "#3f5a6e", "#8a7040", "#55406e", "#4a6a4a", "#7a3a4a", "#3a4a7a"]
    y = 790
    for k in range(6):
        w = 300 - 18 * (k % 3)
        els += book(1350 - w / 2, y - 50, w, 48, tf - .6 + .1 * k, cols[k], fx="rise")
        y -= 52
    for k in range(3):
        els += [circ(1272 + 78 * k, y - 40, 38, "#2a2622", "#cbbca8", 2, tf + .2 + .1 * k, fx="pop"),
                circ(1272 + 78 * k, y - 40, 9, "#cbbca8", at=tf + .2 + .1 * k, fx="pop")]
    y -= 82
    els += building(1350, y + 2, 210, tf + .6, "columns", "#cbbca8", "#2f2822", "rise")
    els += [gl(1350, 460, 420, tf, .22), lab(1350, 176, "the world's most famous", tf + .8, GOLD, 30)]
    return {"base": "sky", "tod": "night", "ground": 612, "groundc": "url(#k-ground)", "sun": False, "moon": [190, 180, 22], "cam": CAM, "els": els}


# ================================================================== chapter 1: a disc in the paper
NMV = View(-109.4, -102.7, 31.1, 37.4, (100, 135, 820, 650))


def pin(xy, t, at, c=GOLD, a="start", lx=None, ly=None, t2=None):
    e = {"k": "pin", "x": round(xy[0], 1), "y": round(xy[1], 1), "t": t, "c": c, "in": round(at, 2)}
    if a != "start":
        e["a"] = a
        e["lx"] = -18 if lx is None else lx
    elif lx is not None:
        e["lx"] = lx
    if ly is not None:
        e["ly"] = ly
    if t2:
        e["t2"] = t2
    return e


def ranch_inset(x, y, w, h, at):
    """A framed window on the ranch at noon: hills, scrub, a rider passing a patch of glinting debris (static inside the frame)."""
    g = [rect(x, y, w, h, "url(#k-sky-day)"), rect(x, y + h * .62, w, h * .38, "#6b5a40"),
         poly([(x, y + h * .62), (x + w * .2, y + h * .5), (x + w * .45, y + h * .55), (x + w * .7, y + h * .46), (x + w, y + h * .58), (x + w, y + h * .62)], "#8a7458", at=-1)]
    g += scrub(31, 10, x + 20, x + w - 20, y + h * .66, y + h * .97, -1, "#4a4a2e", s=.8, rim="rgba(255,236,190,.25)")
    g += glints(33, 12, x + w * .5, x + w * .82, y + h * .72, y + h * .9, -1, .8, False)
    g += sticks_scatter(35, 5, x + w * .52, x + w * .78, y + h * .74, y + h * .88, -1, .8)
    g += horse(x + w * .3, y + h * .93, 1.15, -1, "#2a2018", None, face=1)
    return [{"k": "group", "clip": [x, y, w, h, 8], "els": static(g), "in": round(at, 2)}, rect(x, y, w, h, "none", "#8a7a66", 2, 8, at)]


def sc_nmmap():
    """s6: New Mexico: Roswell and the Foster ranch pinned as named; at the right a window on the ranch at noon, a rider passing the
    debris, '14 June 1947'; then a dashed arrow: he rode on."""
    v = NMV
    els = nm_map(v) + [lab(*v.p(-107.6, 36.55), "New Mexico", -1, SAND_E, 30, st="ital"),
                       {"k": "scale", "x": 820, "y": 772, "w": round(v.km(50), 1), "t": "50 km", "in": -1}]
    tf, tr, tb = T("nmmap", "fourteenth"), T("nmmap", "sheep ranch"), T("nmmap", "Roswell")
    rx, ry = v.p(*PLACES["ranch"])
    els += [pin(v.p(*PLACES["ranch"]), "the Foster ranch", tr, GOLD, "end"), pin(v.p(*PLACES["Roswell"]), "Roswell", tb, BONE)]
    ix, iy, iw, ih = 960, 170, 700, 520
    els += ranch_inset(ix, iy, iw, ih, .3)
    els += [ln([(rx + 14, ry), (ix - 6, iy + ih * .8)], tr + .3, GOLD, 1.0, "inferred", .8)]
    els += [lab(ix + iw / 2, 740, "14 June 1947", tf, GOLD, 30)]
    td = T("nmmap", "left it there")
    els += [arr([(ix + iw * .34, iy + ih * .8), (ix + iw * .55, iy + ih * .62), (ix + iw * .92, iy + ih * .6)], T("nmmap", "rounds") - .2, AMBER, 3, "inferred", 1.0, curve=True),
            lab(ix + iw * .66, iy + ih + 4 - 60, "left it there", td, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


USV = View(-125.5, -66.0, 23.5, 50.5, (90, 150, 1100, 600))


def crescent(x, y, s, at, c=LILAC):
    a = ellipse(x, y, 16 * s, 7 * s, 16, 200, 340)
    b = ellipse(x, y + 4 * s, 14 * s, 4 * s, 16, 340, 200)
    return poly([tuple(p) for p in a] + [tuple(p) for p in b], "rgba(240,240,255,.85)", c, 1.4, at, fx="pop")


def small_paper(x, y, w, h, at, head_="FLYING SAUCERS", seed=1, rot=0):
    s = w / 300.0
    els = [rect(x + 6, y + 8, w, h, "rgba(0,0,0,.45)"), rect(x, y, w, h, NEWS, NEWS_D, 1.2, 2),
           ln([(x + 14 * s, y + 40 * s), (x + w - 14 * s, y + 40 * s)], -1, INK, 2, draw=False),
           nl(x + w / 2, y + 80 * s, head_, round(30 * s, 1), weight=800), ln([(x + 14 * s, y + 98 * s), (x + w - 14 * s, y + 98 * s)], -1, INK, 1.4, draw=False)]
    els += news_lines(x + 16 * s, y + 116 * s, w - 32 * s, int((h / s - 124) / 15), 15 * s, seed, sw=max(1.2, 3 * s))
    tr = "rotate(%s %s %s)" % (rot, round(x + w / 2, 1), round(y + h / 2, 1)) if rot else None
    return grp(els, at, "pop", tr=tr)


def sc_arnold():
    """s7: the western United States: Mount Rainier pinned, '24 June 1947', nine shiny objects in a chain (his report, dotted), a saucer
    skipping on water; newspapers pile up at the right with flying saucer headlines; a reward poster."""
    v = USV
    els = inset_map(v, 90, 140, 1100, 620, -1, "#3a3024", "#12202a")
    mx, my = v.p(-121.76, 46.85)
    tm, tn, ts = T("arnold", "Mount Rainier"), T("arnold", "nine shiny"), T("arnold", "skipped")
    els += [pin((mx, my), "Mount Rainier", tm, GOLD), lab(mx + 18, my + 40, "24 June 1947", tm + .3, BONE, 26, "start")]
    for k in range(9):
        els.append(crescent(260 + 34 * k, 196 + 7 * k + 5 * math.sin(k), 1.0, tn + .08 * k))
    els += [lab(430, 300, "nine shiny objects", tn + .6, LILAC, 26)]
    cx, cy = 360, 470
    els += [rect(cx - 150, cy - 60, 300, 130, "rgba(18,13,10,.88)", LILAC, 2, 14, ts - .4, fx="pop", style="claimed"),
            ln([(cx - 130, cy + 40), (cx + 130, cy + 40)], ts - .3, BLUE, 2, draw=False, op=.7)]
    for k in range(3):
        x0 = cx - 120 + 80 * k
        els.append(ln([(x0, cy + 38), (x0 + 40, cy + 10 - 6 * k), (x0 + 80, cy + 38)], ts - .2 + .25 * k, LILAC, 2, "claimed", .4, curve=True))
    els += saucer(cx + 100, cy - 10, .16, ts + .6, LILAC, "known", w=2)
    els += [lab(cx, cy + 104, "like saucers on water", ts + .3, LILAC, 26)]
    tp, tr = T("arnold", "papers were full"), T("arnold", "rewards")
    heads = ["FLYING SAUCERS", "DISCS SEEN", "SAUCER WAVE", "MORE DISCS"]
    for k, (px, py) in enumerate(((1200, 160), (1430, 190), (1215, 410), (1445, 440))):
        els.append(small_paper(px, py, 240, 270, tp + .35 * k, heads[k], seed=40 + k, rot=(-5 + 3 * k)))
    els += [rect(1380, 640, 240, 136, PAPER, PAPER_D, 1.5, 3, tr, fx="pop"), ink(1500, 684, "REWARD", tr + .1, STAMP, 30, weight=800),
            ink(1500, 734, "$1,000", tr + .1, TYPE, 36, st="serif", weight=700)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_debris():
    """s8: 4 July, on the ranch by day: Brazel and his family gather the debris; the things laid out in the foreground as each is named:
    rubber strips, tinfoil, a tough paper, sticks, tape printed with flowers. No metal parts, nothing heavy."""
    els = [poly([(-20, 470), (200, 430), (520, 446), (900, 420), (1300, 440), (1800, 426), (1800, 470)], "#8a7458", at=-1)]
    els += scrub(53, 12, 80, 1700, 488, 560, -1, "#4a4a2e", s=.7, rim="rgba(255,236,190,.25)")
    els += [rect(-20, 590, 1820, 430, "#4e3f2e", at=-1), ln([(-20, 590), (1800, 590)], -1, "rgba(255,236,206,.25)", 1.5, draw=False)]
    els += glints(51, 10, 300, 1100, 500, 570, -1, .7, False)
    tf, tfam = T("debris", "fourth of July"), T("debris", "family")
    els += [lab(160, 200, "4 July 1947", tf, GOLD, 30, "start")]
    fam = [(250, 250, True, "#5a4c3e"), (340, 232, False, "#6a5a4a"), (418, 176, False, "#7a6a58"), (486, 214, False, "#665848")]
    for k, (x, h, hat, c) in enumerate(fam):
        els += figure(x, 580, h, tfam - .3 + .15 * k, c, hat=hat)
    tr_, tt, tp, ts, tw = T("debris", "Rubber"), T("debris", "Tinfoil"), T("debris", "tough paper"), T("debris", "sticks"), T("debris", "flowers")
    X = [330, 610, 890, 1170, 1460]
    els += [grp(rubber(X[0] - 110, 640, 220, -1, 0, 12) + rubber(X[0] - 100, 676, 206, -1, 2, 12) + rubber(X[0] - 90, 712, 190, -1, 4, 12), tr_ - .2, "pop")]
    els += [lab(X[0], 770, "rubber strips", tr_ + .2, BONE, 30)]
    els += foil(X[1], 680, 1.9, tt - .2) + [lab(X[1], 770, "tinfoil", tt, BONE, 30)]
    els += scrap(X[2], 680, 1.7, tp - .2) + [lab(X[2], 770, "tough paper", tp, BONE, 30)]
    els += [grp(stick(X[3] - 110, 636, X[3] + 110, 722, -1, 9) + stick(X[3] - 100, 724, X[3] + 100, 640, -1, 9) + stick(X[3] - 6, 630, X[3] + 8, 728, -1, 9), ts - .2, "pop"),
            lab(X[3], 770, "sticks", ts, BONE, 30)]
    els += [grp(stick(X[4] - 120, 640, X[4] + 120, 720, -1, 9) + stick(X[4] - 110, 720, X[4] + 110, 642, -1, 9), tw - 1.0, "pop")]
    els += tape_strip(X[4] - 96, 652, X[4] + 98, 712, tw - .5, 24)
    els += [lab(X[4], 770, "tape with flowers", tw, PINK, 30)]
    return {"base": "sky", "tod": "day", "ground": 470, "groundc": "#6e5a42", "sun": [1560, 170, 30], "cam": CAM, "els": els}


def storefront(x, w, h, at, fill, sign=None, ground=660):
    y = ground - h
    els = [rect(x, y, w, h, fill, "rgba(255,236,206,.35)", 1.5, 2, at),
           poly([(x - 10, y + h * .42), (x + w + 10, y + h * .42), (x + w - 6, y + h * .52), (x + 6, y + h * .52)], "#5a3a2a", "rgba(255,236,206,.3)", 1, at),
           rect(x + w * .1, y + h * .58, w * .36, h * .3, "#22303a", "#cbbca8", 1.2, 2, at), rect(x + w * .58, y + h * .56, w * .26, h * .44, "#2a1f16", "#cbbca8", 1.2, 2, at)]
    if sign:
        els += [rect(x + w * .12, y + h * .1, w * .76, h * .2, "#efe2c4", "#6a5a48", 1.2, 3, at), ink(x + w / 2, y + h * .24, sign, at, TYPE, 26, weight=800)]
    else:
        els += [rect(x + w * .12, y + h * .1, w * .76, h * .2, "#4a3a2c", "rgba(255,236,206,.25)", 1, 3, at)]
    return els


def sc_sheriff():
    """s9: Roswell, Monday 7 July: a street of low storefronts, a pickup with wool bales; Brazel leans to the sheriff; a dotted bubble
    holds a tiny saucer ('kinda confidential like'); a telephone line runs to the air base on the horizon."""
    G = 720
    els = [poly([(-20, 640), (300, 600), (700, 624), (1100, 590), (1500, 616), (1800, 600), (1800, 640)], "#6a5a4a", at=-1)]
    els += storefront(90, 300, 300, -1, "#7a5d43", ground=G) + storefront(410, 330, 340, -1, "#8a6a4c", ground=G) + storefront(760, 360, 320, -1, "#6e5440", "SHERIFF", ground=G)
    els += [rect(-20, G, 1820, 320, "#5c4a36", at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,236,206,.3)", 1.5, draw=False)]
    els += truck(300, 800, 1.2, -1, load=True)
    els += person_hat(800, 800, 236, -1, "#4a3c30", None) + person_hat(940, 800, 244, -1, "#3a3a44", None)
    els += [circ(955, 640, 7, AU, at=-1)]
    th, tw, tq, tc = T("sheriff", "heard about"), T("sheriff", "whispered"), T("sheriff", "kinda"), T("sheriff", "called the air base")
    els += [small_paper(450, 440, 240, 270, th, "FLYING DISCS", seed=61, rot=-5)]
    els += [poly(E(760, 440, 116, 62, 30), "rgba(18,13,10,.9)", LILAC, 2.6, tw, fx="pop", style="claimed", curve=True),
            poly([(784, 496), (806, 532), (816, 494)], "rgba(18,13,10,.9)", LILAC, 2, tw, fx="pop", style="claimed")]
    els += saucer(760, 450, .42, tw + .2, LILAC, "known", w=2)
    els += [lab(760, 350, "kinda confidential like", tq, LILAC, 30)]
    els += [lab(140, 170, "Monday, 7 July", .4, GOLD, 30, "start")]
    els += hangar(1480, 626, 120, 64, at=-1, lit=False, op=.75) + hangar(1600, 626, 120, 64, at=-1, lit=False, op=.75) + tower(1440, 626, 80, -1, op=.75)
    els += [ln([(1150, 400), (1150, G)], -1, "#3a2c20", 7, draw=False), ln([(1118, 414), (1182, 414)], -1, "#3a2c20", 5, draw=False),
            ln([(1350, 470), (1350, 640)], -1, "#3a2c20", 5, draw=False), ln([(1328, 480), (1372, 480)], -1, "#3a2c20", 4, draw=False)]
    els += [ln([(1080, 420), (1150, 414)], tc - .5, GOLD, 2.4, dur=.3), ln([(1150, 414), (1250, 448), (1350, 480)], tc - .3, GOLD, 2.4, dur=.5, curve=True),
            ln([(1350, 480), (1440, 540), (1520, 590)], tc, GOLD, 2.4, dur=.5, curve=True), lab(1560, 540, "the air base", tc + .3, BONE, 28)]
    return {"base": "sky", "tod": "day", "ground": 640, "groundc": "#6a5a4a", "sun": [1580, 170, 30], "cam": CAM, "els": els}


def add_drive():
    """s10 (back on the map, close): the intelligence officer and a counter-intelligence officer drive from the base to the ranch and bring
    the debris back."""
    v = NMV
    ax_, ay_ = v.p(*PLACES["RAAF"])
    rx, ry = v.p(*PLACES["ranch"])
    tb, tc, tl, tk = T("drive", "intelligence officer"), T("drive", "counter-intelligence"), T("drive", "loaded"), T("drive", "brought it back")
    mx, my = (ax_ + rx) / 2, (ay_ + ry) / 2
    ux, uy = (ry - ay_), -(rx - ax_)
    L = math.hypot(ux, uy) or 1
    ux, uy = ux / L * 9, uy / L * 9
    els = [ln([(ax_ - 3, ay_ - 4), (mx + ux, my + uy), (rx + 5, ry + 3)], tb - .6, AMBER, 1.0, "inferred", 1.2, curve=True)]
    els += [ppl(rx - 12, ry + 16, 13, tb, "#e8d6b8", "pop"), ppl(rx - 4, ry + 16, 13, tc, "#cbbca8", "pop")]
    els += [lab(rx - 6, ry - 47, "Maj. Jesse Marcel", tb + .1, GOLD, 28, "end"), lab(rx - 6, ry - 38, "and a counter-intelligence officer", tc + .1, BONE, 26, "end")]
    els += truck(rx + 14, ry + 18, .05, tl, "#cbbca8", "rgba(255,236,206,.5)", "pop")
    els += [arr([(rx + 2, ry + 9), (mx - ux, my - uy), (ax_ - 7, ay_ - 1)], tk, GOLD, 1.2, dur=1.0, curve=True)]
    els += [dot(round(rx + (mx - ux - rx) * (k + 1) / 6, 1), round(ry + 9 + (my - uy - ry - 9) * (k + 1) / 6 + 3, 1), 1.2, FOIL, round(tk + .12 * k, 2)) for k in range(5)]
    return els


US2 = View(-125.0, -66.5, 24.0, 50.0, (820, 170, 860, 540))
CITIES = [(-74.0, 40.7), (-87.6, 41.9), (-118.2, 34.05), (-122.4, 37.8), (-122.3, 47.6), (-96.8, 32.8), (-105.0, 39.7), (-84.4, 33.7),
          (-71.1, 42.4), (-77.0, 38.9), (-93.3, 45.0), (-90.1, 30.0)]


def sc_release():
    """s11: the base's press release rises, 'possession of a flying disc' lit in gold; then at the right the news runs out along the
    wires from Roswell to cities across the country, each popping a tiny newspaper."""
    els = desk_bg()
    x, y, w, h = 170, 150, 560, 620
    els += [rect(x + 10, y + 14, w, h, "rgba(0,0,0,.45)", at=.3, fx="rise"), rect(x, y, w, h, PAPER, PAPER_D, 1.5, 3, .3, fx="rise")]
    els += [ink(x + w / 2, y + 62, "ROSWELL ARMY AIR FIELD", .45, TYPE, 26, weight=700), ink(x + w / 2, y + 100, "509th Bomb Group", .45, TYPE, 24),
            ink(x + w / 2, y + 136, "8 July 1947", .45, TYPE, 24)]
    els += page_lines(x + 60, y + 190, w - 120, 6, .5, 28, seed=71)
    tp = T("release", "gained possession")
    els += [rect(x + 40, y + 372, w - 80, 46, "rgba(242,201,142,.55)", at=tp - .3, fx="pop"), ink(x + w / 2, y + 404, "possession of a flying disc", tp - .2, TYPE, 28, weight=700)]
    els += page_lines(x + 60, y + 460, w - 120, 5, .6, 28, seed=73)
    v = US2
    els += inset_map(v, 820, 170, 860, 540, -1, "#3a3024", "#12202a")
    rx, ry = v.p(-104.52, 33.39)
    tw, tc = T("release", "raced along"), T("release", "across the country")
    els += [pin((rx, ry), "Roswell", .3, GOLD, "start")]
    for k, (lo, la) in enumerate(CITIES):
        cx, cy = v.p(lo, la)
        mx, my = (rx + cx) / 2, (ry + cy) / 2 - 30
        t0 = round(tw + .1 * k, 2)
        els += [ln([(rx, ry), (mx, my), (cx, cy)], t0, AMBER, 1.8, dur=.6, curve=True, op=.85), dot(cx, cy, 6, AU, t0 + .5),
                rect(cx - 10, cy - 30, 20, 16, NEWS, NEWS_D, 1, 1, t0 + .6, fx="pop")]
    els += [lab(1250, 760, "across the country", tc, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_ramey():
    """s12: Fort Worth, the evening of 8 July: a general's office at night, the debris spread on the floor; photographers' flashes; the
    weather officer's identification: 'a balloon' (the rubber), 'a radar target' (the foil reflector); 'the photographs'."""
    els = [rect(-20, -20, 1820, 360, "#2a211b", at=-1), poly([(80, 800), (1700, 800), (1470, 330), (310, 330)], "#3a2620", "rgba(255,226,190,.2)", 1.2, -1)]
    els += [rect(240, 140, 260, 150, "#3a3024", "#8a7a66", 2, 3, -1), ln([(260, 200), (480, 190)], -1, "#8a7a66", 2, draw=False, op=.5),
            ln([(300, 160), (330, 280)], -1, "#8a7a66", 2, draw=False, op=.4),
            rect(1250, 130, 220, 170, "#162030", "#8a7a66", 2, 3, -1), ln([(1360, 130), (1360, 300)], -1, "#8a7a66", 2, draw=False)]
    els += [rect(640, 240, 520, 80, "#4a3626", "#8a6a48", 2, 4, -1), gl(900, 560, 700, -1, .14)]
    tf = T("ramey", "Fort Worth")
    # the debris on the floor
    db = foil(760, 560, 1.1, -1) + foil(1010, 640, .9, -1) + rubber(800, 680, 140, -1, 1, 8) + rubber(980, 530, 120, -1, 3, 7)
    db += stick(880, 500, 1000, 560, -1, 6) + stick(860, 610, 960, 700, -1, 6) + stick(1060, 560, 1140, 650, -1, 6)
    els += [grp(db, -1, None)]
    els += [grp(reflector(1180, 470, 58, -1, None, False) + [ln([(1150, 440), (1210, 500)], -1, "#2a2016", 4, draw=False)], -1, None)]
    els += person_hat(1400, 760, 250, -1, "#4a4a3e", None)
    els += [circ(1386, 560, 5, AU, at=-1), circ(1414, 560, 5, AU, at=-1)]
    tr_ = T("ramey", "showed reporters")
    for k, (x, h) in enumerate(((420, 230), (560, 214))):
        els += [ppl(x, 790, h, -1, "#5a5650", None), rect(x + 14, 790 - h * .74, 34, 24, "#1a1a1a", "#cbbca8", 1.2, 3, -1),
                gl(x + 40, 790 - h * .78, 140, tr_ + .5 * k, .9, "lamp")]
    els += [lab(889, 180, "Fort Worth, 8 July, evening", tf, GOLD, 30)]
    tb, tt, tp = T("ramey", "a balloon"), T("ramey", "radar"), T("ramey", "photographs")
    els += [arr([(700, 760), (760, 712)], tb, BONE, 2.5, dur=.4), lab(690, 790, "a balloon", tb + .1, BONE, 28, "end")]
    els += [arr([(1250, 392), (1214, 428)], tt, BONE, 2.5, dur=.4), lab(1260, 380, "a radar target", tt + .1, BONE, 28, "start")]
    els += [rect(1500, 460, 200, 140, "#d8d4cc", "#f5f0e6", 3, 2, tp - .2, fx="pop"), rect(1512, 472, 176, 116, "#4a4744", at=tp - .2, fx="pop")]
    els += [grp(foil(1580, 530, .45, -1) + rubber(1540, 560, 90, -1, 2, 4) + stick(1620, 500, 1670, 560, -1, 3), tp, "pop"),
            lab(1600, 640, "the photographs", tp + .2, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def scale_(x, y, at, fx="pop"):
    """A kitchen scale: base, pan, dial."""
    return [rect(x - 120, y - 40, 240, 70, "#3a3532", "#9a8a70", 2, 10, at, fx=fx), rect(x - 150, y - 60, 300, 20, "#6a625a", "#cbbca8", 1.5, 8, at, fx=fx),
            circ(x, y - 4, 26, "#efe6d2", "#6a5a48", 2, at, fx=fx), ln([(x, y - 4), (x + 18, y - 16)], at, RED, 3, draw=False)]


def sc_account():
    """s13: the 9 July paper's column; a scale under the bundle: about 5 lb, 2 kg; a gear and a nut, dotted and struck through (no
    metal, no engine); the two weather balloons he had found before, 'not like these'."""
    els = desk_bg()
    x, y, w, h = 100, 150, 400, 620
    els += [rect(x + 10, y + 12, w, h, "rgba(0,0,0,.45)", at=-1), rect(x, y, w, h, NEWS, NEWS_D, 1.5, 3, -1)]
    els += [nl(x + w / 2, y + 60, "Harassed Rancher", 30, weight=800), nl(x + w / 2, y + 98, "who Located 'Saucer'", 30, weight=800),
            nl(x + w / 2, y + 136, "Sorry He Told About It", 30, weight=800), ln([(x + 20, y + 158), (x + w - 20, y + 158)], -1, INK, 1.5, draw=False)]
    els += news_lines(x + 24, y + 186, w - 48, 24, 17, 81, sw=3.4)
    tb, tf, tn, tw, tnot = T("account", "whole bundle"), T("account", "five pounds"), T("account", "No sign"), T("account", "weather balloons"), T("account", "neither")
    sx, sy = 760, 640
    els += [rect(sx - 170, sy - 50, 340, 96, "#3a3532", "#9a8a70", 2, 12, .3, fx="pop"), rect(sx - 210, sy - 80, 420, 28, "#6a625a", "#cbbca8", 1.5, 10, .3, fx="pop"),
            circ(sx, sy, 36, "#efe6d2", "#6a5a48", 2, .3, fx="pop"), ln([(sx, sy), (sx + 26, sy - 18)], tf, RED, 4, dur=.4)]
    els += [grp(rubber(sx - 150, sy - 118, 170, -1, 2, 10) + foil(sx - 40, sy - 126, 1.0, -1) + stick(sx - 130, sy - 150, sx + 40, sy - 96, -1, 7) +
                scrap(sx + 90, sy - 120, .8, -1) + tape_strip(sx + 30, sy - 104, sx + 140, sy - 132, -1, 14, None, n=3), tb, "pop")]
    els += [lab(sx, 760, "about 5 lb, 2 kg", tf, GOLD, 32)]
    gx, gy = 1080, 360
    els += [I.ring(gx, gy, 74, tn - .3, LILAC, 4, "claimed")] + [rect(round(gx + 88 * math.cos(a) - 12, 1), round(gy + 88 * math.sin(a) - 12, 1), 24, 24, LILAC, r=3, at=tn - .2, op=.6)
                                                                  for a in [k * math.pi / 4 for k in range(8)]]
    els += [I.ring(gx, gy, 26, tn - .2, LILAC, 4, "claimed")]
    hx = 1290
    els += [poly([(round(hx + 62 * math.cos(math.pi / 3 * k), 1), round(gy + 62 * math.sin(math.pi / 3 * k), 1)) for k in range(6)], "rgba(201,193,238,.12)", LILAC, 4,
                 tn - .1, style="claimed"), I.ring(hx, gy, 24, tn - .1, LILAC, 4, "claimed")]
    els += [I.strike(980, 470, 1370, 250, tn + .4, RED, 7), lab(1185, 520, "no metal, no engine", tn + .3, BONE, 30)]
    for k, bx in enumerate((1440, 1590)):
        els += balloon(bx, 530, 44, tw - .2 + .2 * k, "pop", string=70, op=.85)
    els += [lab(1515, 450, "found before", tw + .2, BONE, 28)]
    els += [ln([(1380, 660), (1380, 680), (1650, 680), (1650, 660)], tnot - .2, MUTED, 2.4, "inferred", .5), lab(1515, 724, "not like these", tnot, MUTED, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_history():
    """s14: the 509th's history for July 1947 under a lamp: one line lights in gold: 'The object turned out to be a radar tracking
    balloon.' A manila folder closes over the page."""
    els = desk_bg() + lamp(1200, 40, -1, 60, .6, 300)
    x, y, w, h = 400, 140, 980, 640
    els += [rect(x + 12, y + 14, w, h, "rgba(0,0,0,.45)", at=-1), rect(x, y, w, h, PAPER, PAPER_D, 1.5, 3, -1)]
    els += [ink(x + w / 2, y + 66, "509th BOMB GROUP", -1, TYPE, 30, weight=700), ink(x + w / 2, y + 104, "Roswell Army Air Field", -1, TYPE, 24),
            ink(x + w / 2, y + 140, "History, July 1947", -1, TYPE, 26)]
    els += typed(x + 80, y + 200, w - 160, 7, -1, 28, seed=91) + typed(x + 80, y + 470, w - 160, 5, -1, 28, seed=93)
    tq = T("history", "the object")
    els += [rect(x + 60, y + 398, w - 120, 50, "rgba(242,201,142,.6)", at=tq - .3, fx="pop"),
            ink(x + w / 2, y + 432, "The object turned out to be a radar tracking balloon.", tq - .2, TYPE, 28, weight=600)]
    te = END("history", .2)
    els += [folder(x - 30, y + 30, w + 60, h - 20, te, MANILA, fx="rise"), ink(x + w / 2, y + h * .55, "509th History, July 1947", te + .2, "#5a4630", 30, weight=700)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 2: thirty years later
def sc_footnote():
    """s15: an open book: grey lines of text, and at the foot of the right page a one-line footnote, 'Roswell, 1947: a weather balloon';
    the decades pass along the top (1950s, 1960s, 1970s)."""
    els = desk_bg()
    els += [rect(312, 182, 1180, 590, "rgba(0,0,0,.45)", at=-1), rect(300, 170, 590, 590, PAPER, PAPER_D, 1.5, 4, -1), rect(890, 170, 590, 590, PAPER, PAPER_D, 1.5, 4, -1),
            ln([(890, 172), (890, 758)], -1, "rgba(90,70,50,.5)", 6, draw=False)]
    els += typed(360, 240, 470, 16, -1, 28, c="#8a7a66", seed=101) + typed(950, 240, 470, 13, -1, 28, c="#8a7a66", seed=103)
    els += [ln([(950, 640), (1110, 640)], -1, "#8a7a66", 1.5, draw=False), ink(950, 682, "1. Roswell, 1947: a weather balloon.", -1, TYPE, 24, a="start")]
    for k, d in enumerate(("1950s", "1960s", "1970s")):
        els += [lab(560 + 380 * k, 140, d, .3 + .45 * k, MUTED, 28)]
    tf = T("footnote", "footnote")
    els += [arr([(1500, 560), (1400, 640), (1330, 668)], tf - .3, GOLD, 3, dur=.7, curve=True), lab(1560, 540, "a footnote", tf, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


SOUTH = View(-110.0, -88.0, 27.5, 37.5, (110, 160, 760, 560))


def sc_friedman():
    """s16: 1978: a line from New Mexico to Houma, Louisiana, where Marcel lives; two figures face each other: Stanton Friedman, Jesse
    Marcel; a dotted card rises from Marcel: 'a cover story' (his claim)."""
    v = SOUTH
    els = inset_map(v, 110, 160, 760, 560, -1, "#3a3024", "#12202a")
    els += [poly([v.p(lo, la) for lo, la in NM], "rgba(201,173,133,.18)", SAND_E, 1.6, -1)]
    t78, tm, tf, tc = T("friedman", "seventy-eight"), T("friedman", "Jesse Marcel"), T("friedman", "Stanton"), T("friedman", "cover story")
    rx, ry = v.p(-104.52, 33.39)
    hx, hy = v.p(-90.72, 29.6)
    els += [lab(889, 150, "1978", t78 - .4, GOLD, 34)]
    els += [dot(rx, ry, 7, BONE, .3), lab(rx, ry - 20, "Roswell", .3, BONE, 26)]
    els += [ln([(rx, ry), ((rx + hx) / 2, ry - 120), (hx, hy)], tf + .4, AMBER, 2.4, "inferred", 1.2, curve=True)]
    els += [pin((hx, hy), "Houma, Louisiana", tm, GOLD, "end", ly=-22)]
    els += [gl(1330, 520, 380, .2, .22)] + table(1330, 640, 380, .2)
    els += seated(1180, 760, 220, tf - .2, "#8a96a2", face=1) + seated(1480, 760, 220, tm - .2, "#a39a8e", face=-1)
    els += [lab(1150, 470, "Stanton Friedman", tf, BONE, 26), lab(1500, 470, "Jesse Marcel", tm, BONE, 26)]
    els += [rect(1360, 270, 280, 70, "rgba(18,13,10,.88)", LILAC, 2.4, 22, tc - .2, fx="pop", style="claimed"), lab(1500, 316, "a cover story", tc, LILAC, 28),
            ln([(1480, 342), (1484, 420)], tc - .2, LILAC, 2, "claimed", .4)]
    return {"base": "dark", "cam": CAM, "els": els}


def hand(x, y, s, at, c="#cbbca8"):
    """An open hand, palm up, seen from the side: fingers to the right."""
    P = lambda u, v: (x + u * s, y + v * s)
    return [poly([P(-80, 26), P(-74, -4), P(-40, -14), P(10, -12), P(64, -18), P(92, -12), P(96, -2), P(60, 6), P(70, 14), P(40, 30), P(-30, 38)], "#5a4a3e", c, 2, at,
                  fx="pop", curve=True),
            poly([P(-6, -12), P(4, -34), P(18, -36), P(14, -12)], "#5a4a3e", c, 2, at, fx="pop", curve=True)]


def sc_marcel():
    """s17: Marcel's account in three dotted cards as named: a piece as light as balsa, floating over a hand; a piece that would not
    burn over a lighter's flame; a stick with markings like writing. Then: 'not from earth' (Marcel, 1979)."""
    els = []
    xs = [340, 889, 1438]
    for k, x in enumerate(xs):
        els.append(rect(x - 250, 150, 500, 460, "rgba(18,13,10,.6)", LILAC, 2.4, 20, .2 + .15 * k, fx="pop", style="claimed"))
    tl, tb, tm, tq = T("marcel", "light as balsa"), T("marcel", "would not burn"), T("marcel", "Markings"), T("marcel", "came to earth")
    els += [lab(889, 132, "Jesse Marcel's account, 1979", .4, LILAC, 28)]
    x = xs[0]
    els += balance(x, 330, 300, 0, 560, tl - .4, drop_=110, pan=120)
    els += [poly([(x - 200, 424), (x - 104, 420), (x - 104, 432), (x - 200, 436)], BALSA, BALSA_E, 1.5, tl, fx="pop")]
    els += [lab(x - 150, 480, "a piece", tl + .2, MUTED, 24), lab(x + 150, 480, "nothing", tl + .2, MUTED, 24)]
    els += [lab(x, 660, "light as balsa", tl, LILAC, 30)]
    x = xs[1]
    els += [rect(x - 34, 440, 68, 130, "#6a625a", "#cbbca8", 2, 8, tb - .3, fx="rise"), rect(x - 26, 420, 52, 24, "#8a8278", "#cbbca8", 1.5, 4, tb - .3, fx="rise"),
            gl(x, 380, 110, tb, .9, "fire"), poly([(x - 16, 418), (x - 4, 350), (x + 4, 352), (x + 16, 418)], "#ffd08a", at=tb, fx="pop", curve=True),
            poly([(x - 170, 300), (x + 170, 288), (x + 172, 312), (x - 168, 324)], FOIL, FOIL_E, 2, tb - .2, fx="pop")]
    els += [lab(x, 660, "would not burn", tb, LILAC, 30)]
    x = xs[2]
    els += stick(x - 210, 400, x + 210, 372, tm - .3, 34, fx="pop")
    for k in range(7):
        gx = x - 170 + 52 * k
        els.append(ln([(gx, 392 - 2 * k), (gx + 12, 376 - 2 * k), (gx + 22, 398 - 2 * k), (gx + 34, 380 - 2 * k)], tm + .1 * k, PURPLE, 4, draw=False))
    els += [lab(x, 660, "markings like writing", tm, LILAC, 30)]
    els += [lab(889, 750, "not from earth", tq + 1.0, LILAC, 40, st="ital")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def sc_books():
    """s18: 1980: a tabloid front page and a book, The Roswell Incident; a grid of ninety small figures fills (over 90 people); then a
    shelf of later books grows: hundreds of interviews."""
    els = desk_bg()
    tt, tb, tn, tm = T("books", "tabloid"), T("books", "a book"), T("books", "more than ninety"), T("books", "More books")
    x, y, w, h = 130, 160, 400, 560
    els += [grp([rect(x + 8, y + 10, w, h, "rgba(0,0,0,.45)"), rect(x, y, w, h, NEWS, NEWS_D, 1.5, 3), rect(x, y, w, 70, "#b8322a"),
                 nl(x + w / 2, y + 48, "EXCLUSIVE", 34, -1, "#fff4e6", weight=800), nl(x + w / 2, y + 130, "UFO WRECKAGE", 44, weight=900),
                 nl(x + w / 2, y + 176, "FOUND IN 1947", 30, weight=800), rect(x + 40, y + 210, w - 80, 190, "#cfc6b4", "#8a7f70", 1.5, 2)]
                + saucer(x + w / 2, y + 310, .55, -1, "#5a4a8a", "known", None, 3, "rgba(90,74,138,.15)") + news_lines(x + 30, y + 430, w - 60, 7, 17, 111, sw=3.4), tt - .2, "rise")]
    bx, by = 600, 230
    els += [grp([rect(bx + 10, by + 10, 300, 430, "rgba(0,0,0,.5)"), rect(bx, by, 300, 430, "#2a3a52", "#cbbca8", 2, 4), rect(bx + 18, by + 18, 264, 394, "none", "#c9b37a", 1.5, 2),
                 nl(bx + 150, by + 110, "THE", 30, -1, "#f2e6c8", weight=700), nl(bx + 150, by + 160, "ROSWELL", 44, -1, "#f2e6c8", weight=800),
                 nl(bx + 150, by + 210, "INCIDENT", 44, -1, "#f2e6c8", weight=800)] + saucer(bx + 150, by + 300, .5, -1, "#f2e6c8", "known", None, 2, "none"), tb, "rise")]
    els += [lab(450, 762, "1980", tt, GOLD, 32)]
    k = 0
    for r_ in range(9):
        for c_ in range(10):
            els.append(ppl(1010 + 62 * c_, 210 + 40 * r_, 30, round(tn + .012 * k, 3), "#cbbca8", "pop"))
            k += 1
    els += [lab(1290, 590, "over 90 people", tn + .6, GOLD, 30)]
    cols = ["#7a4a3a", "#3f5a6e", "#8a7040", "#55406e", "#4a6a4a", "#7a3a4a", "#3a4a7a", "#6a5a3a", "#4a5a6a", "#7a5a4a"]
    yrs = ["1991", "1992", "1994", "1994", "1997", "2001", "2007", "", "", ""]
    for j in range(10):
        els += book(1000 + 58 * j, 620, 50, 130, tm + .12 * j, cols[j], yrs[j] or None, "rise", size=24)
    els += [ln([(980, 752), (1600, 752)], tm, "#8a6a48", 4, draw=False), lab(1290, 794 - 14, "hundreds of interviews", T("books", "hundreds"), GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


SITEV = View(-109.4, -102.7, 31.1, 37.4, (100, 135, 1000, 650))


def sc_sites():
    """s19: New Mexico again: the one place on the record (the ranch, 1947, debris), then the crash sites the books added, dotted, each
    with its year: 1980 bodies far to the west, 1992 two saucers and eight aliens, 1994 a new site north of Roswell; they disagree."""
    v = SITEV
    els = nm_map(v)
    rx, ry = v.p(*PLACES["ranch"])
    sx, sy = v.p(*PLACES["San Agustin"])
    nx, ny = v.p(*PLACES["north"])
    els += [pin((rx, ry), "the ranch", .3, GOLD, "end", ly=-16), pin(v.p(*PLACES["Roswell"]), "Roswell", .3, BONE, "start", ly=26)]
    t80, t92, t8, t94, td = T("sites", "second crash site"), T("sites", "two saucers"), T("sites", "eight aliens"), T("sites", "new site"), T("sites", "disagree")
    # the legend
    LX, rows = 1110, [250, 380, 510, 640]
    els += [dot(LX, rows[0], 12, AU, .3), lab(LX + 30, rows[0] + 10, "1947: debris, on record", .4, GOLD, 28, "start")]
    els += [I.ring(sx, sy, 26, t80 - .3, LILAC, 3, "claimed")] + ghost_person(sx - 10, sy + 12, 30, t80, w=1.6) + ghost_person(sx + 10, sy + 12, 30, t80 + .1, w=1.6)
    els += [ln([(rx - 12, ry + 4), (sx + 30, sy + 4)], t80, LILAC, 2, "claimed", .8), lab(sx, sy + 70, "240 km west", t80 + .4, LILAC, 24)]
    els += [I.ring(LX, rows[1], 13, t80, LILAC, 3, "claimed"), lab(LX + 30, rows[1] + 10, "1980: bodies", t80 + .2, LILAC, 28, "start")]
    els += saucer(rx + 40, ry - 78, .2, t92, LILAC, "claimed", w=2) + saucer(sx + 4, sy - 56, .2, t92 + .2, LILAC, "claimed", w=2)
    els += saucer(LX, rows[2], .12, t92, LILAC, "claimed", w=2) + [lab(LX + 30, rows[2] + 10, "1992: two saucers", t92 + .2, LILAC, 28, "start")]
    els += [g for k in range(8) for g in ghost_person(LX + 300 + 30 * k, rows[2] + 22, 34, round(t8 + .08 * k, 2), w=1.4)]
    els += [I.ring(nx, ny, 20, t94 - .2, LILAC, 3, "claimed"), I.ring(LX, rows[3], 13, t94 - .2, LILAC, 3, "claimed"),
            lab(LX + 30, rows[3] + 10, "1994: north of Roswell", t94, LILAC, 28, "start")]
    els += [ln([(sx + 20, sy - 10), (nx - 20, ny)], td - .3, LILAC, 1.6, "claimed", .8, curve=False)] + qmark(640, 360, td + .2, 70)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_haut():
    """s20: a sealed envelope opens; a typed statement rises (Walter Haut, signed 2002, published 2007), its claim in dotted lilac (a
    craft and bodies); a bar from 1947 to 2002: 55 years; then his sworn statement of 1993, which describes neither."""
    els = desk_bg()
    ex, ey = 230, 330
    els += [rect(ex + 10, ey + 12, 420, 260, "rgba(0,0,0,.45)", at=-1), rect(ex, ey, 420, 260, PAPER, PAPER_D, 1.5, 4, -1),
            ln([(ex, ey), (ex + 210, ey + 140), (ex + 420, ey)], -1, "#9a8a70", 2, draw=False), circ(ex + 210, ey + 144, 30, STAMP, "#7a1a14", 2, -1),
            circ(ex + 210, ey + 144, 16, "none", "#e8a090", 1.5, -1)]
    ts, tc, t55, t93, tn = T("haut", "sealed statement"), T("haut", "a craft"), T("haut", "fifty-five"), T("haut", "under oath"), T("haut", "neither")
    els += [veil(ex - 2, ey - 2, 424, 264, ts + .2, FLAT, .55, .8)]
    x, y, w, h = 760, 140, 560, 520
    els += [rect(x + 10, y + 12, w, h, "rgba(0,0,0,.45)", at=ts + .3, fx="rise"), rect(x, y, w, h, PAPER, PAPER_D, 1.5, 3, ts + .3, fx="rise")]
    els += [ink(x + w / 2, y + 60, "Walter Haut", ts + .5, TYPE, 32, weight=700), ink(x + w / 2, y + 98, "statement, signed 2002", ts + .5, TYPE, 24)]
    els += typed(x + 60, y + 150, w - 120, 6, ts + .6, 28, seed=121)
    els += [rect(x + 40, y + 330, w - 80, 48, "rgba(201,193,238,.35)", "#6a5aa8", 2, 6, tc - .2, fx="pop", style="claimed"),
            ink(x + w / 2, y + 364, "a craft and bodies", tc, "#4b3d8f", 30, weight=700)]
    els += typed(x + 60, y + 420, w - 120, 3, ts + .7, 28, seed=123)
    X = lambda yr: 230 + (yr - 1945) / 60 * 1100
    els += [axis(230, 1330, 740, [(X(1947), "1947"), (X(2002), "2002")], t55 - .6), bar(X(1947), X(2002), 718, 10, t55 - .3, AMBER, 1.2),
            lab((X(1947) + X(2002)) / 2, 700, "55 years", t55 + .4, AMBER, 30)]
    x2 = 1420
    els += [rect(x2 + 8, 330, 230, 300, "rgba(0,0,0,.45)", at=t93 - .3, fx="pop"), rect(x2, 320, 230, 300, PAPER, PAPER_D, 1.5, 3, t93 - .3, fx="pop"),
            ink(x2 + 115, 372, "1993", t93 - .2, TYPE, 30, weight=700), ink(x2 + 115, 406, "sworn statement", t93 - .2, TYPE, 24)]
    els += typed(x2 + 30, 440, 170, 5, t93, 26, seed=125)
    els += [lab(x2 + 115, 680, "describes neither", tn, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def house(x, y, s, at, c, fill, extra=False, style="known", fx="pop", op=None):
    """A small house (x = centre, y = ground); extra = the remembered house: a storey and a tower more."""
    w, h = 160 * s, 90 * s
    els = [rect(x - w / 2, y - h, w, h, fill, c, 2, 2, at, fx=fx, op=op, style=style),
           poly([(x - w / 2 - 12 * s, y - h), (x, y - h - 60 * s), (x + w / 2 + 12 * s, y - h)], fill, c, 2, at, fx=fx, op=op, style=style),
           rect(x - 14 * s, y - 50 * s, 28 * s, 50 * s, "#2a2016", c, 1.5, 2, at, fx=fx, op=op, style=style),
           rect(x + 30 * s, y - 70 * s, 34 * s, 28 * s, "#e8c878", c, 1.5, 2, at, fx=fx, op=op, style=style)]
    if extra:
        els += [rect(x - w / 2, y - h - 80 * s, w, 80 * s, fill, c, 2, 2, at, fx=fx, op=op, style=style),
                rect(x + w / 2 - 50 * s, y - h - 200 * s, 50 * s, 200 * s, fill, c, 2, 2, at, fx=fx, op=op, style=style),
                poly([(x + w / 2 - 60 * s, y - h - 200 * s), (x + w / 2 - 25 * s, y - h - 250 * s), (x + w / 2 + 10 * s, y - h - 200 * s)], fill, c, 2, at, fx=fx, op=op, style=style)]
    return els


def sc_photo():
    """s21: most accounts came 30 to 50 years after 1947 (a bracket on a time line); an old photograph of a house with a gold tick,
    a dotted thought bubble with the same house remembered bigger; then the 1947 newspaper column, framed: 'our photograph'."""
    X = lambda yr: 230 + (yr - 1945) / 60 * 1320
    els = [axis(230, 1550, 230, [(X(1950), "1950"), (X(1970), "1970"), (X(1990), "1990")], .1, below=False), dot(X(1947), 230, 11, AU, .3)]
    t30, tm, tp, to = T("photo", "thirty to fifty"), T("photo", "a memory"), T("photo", "trust the photograph"), T("photo", "our photograph")
    els += [ln([(X(1977), 262), (X(1977), 276), (X(1997), 276), (X(1997), 262)], t30 - .3, LILAC, 3, "known", .6),
            lab((X(1977) + X(1997)) / 2, 318, "30 to 50 years later", t30, LILAC, 28)]
    els += [rect(200, 380, 380, 300, "#d9c49a", "#f5ecdc", 6, 3, tm - .3, fx="pop"), rect(220, 400, 340, 260, "#b89a6a", at=tm - .3, fx="pop")]
    els += [grp(house(390, 620, .9, -1, "#5a4630", "#c9a978"), tm - .2, "pop"), lab(390, 724, "a photograph", tm, BONE, 28)]
    els += [poly(E(900, 520, 230, 190, 40), "rgba(18,13,10,.5)", LILAC, 2.4, tm + .4, fx="pop", style="claimed", curve=True),
            circ(660, 690, 14, "none", LILAC, 2, tm + .4, style="claimed"), circ(626, 720, 9, "none", LILAC, 2, tm + .4, style="claimed")]
    els += house(870, 650, .75, tm + .7, "#e4dcff", "rgba(201,193,238,.28)", True, "inferred")
    els += [lab(900, 760, "a memory", tm + .8, LILAC, 28)]
    els += [tick(390, 440, tp + .2, GREEN, 1.6)]
    x, y, w, h = 1240, 380, 320, 330
    els += [rect(x - 14, y - 14, w + 28, h + 28, "#3a2c20", GOLD, 3, 4, to - .4, fx="pop"), rect(x, y, w, h, NEWS, NEWS_D, 1.5, 2, to - .4, fx="pop")]
    els += [grp([nl(x + w / 2, y + 48, "Harassed Rancher", 26, weight=800), nl(x + w / 2, y + 80, "Sorry He Told About It", 24, weight=800)]
                + news_lines(x + 24, y + 104, w - 48, 12, 17, 131, sw=3.2), to - .3, "pop")]
    els += [lab(x + w / 2, 760, "our photograph: 1947", to, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_fields():
    """s22: two debris fields to the same scale (1.2 units = 1 m): the 1947 field, about 200 yards (183 m) across, solid gold; the
    field Marcel remembered in 1979, three-quarters of a mile (1,207 m) long and about 80 m wide, dotted lilac, drawing itself out."""
    k = 1.2
    els = [rect(-20, -20, 1820, 1040, "#1c1712", at=-1)]
    els += [ln([(x, 120), (x, 800)], -1, "rgba(255,236,206,.05)", 1, draw=False) for x in range(190, 1700, 120)]
    t47, t79, tn, tm = T("fields", "rancher described"), T("fields", "Marcel remembered"), T("fields", "Nobody has"), T("fields", "Memories drift")
    cx, cy, r = 300, 290, 91.5 * k
    els += [circ(cx, cy, r, "rgba(242,201,142,.14)", GOLD, 3, t47 - .2, fx="pop")]
    els += glints(141, 14, cx - r * .6, cx + r * .6, cy - r * .5, cy + r * .6, t47, .8, False)
    els += [lab(cx + r + 30, cy - 4, "1947: about 200 yards", t47 + .3, GOLD, 30, "start"), lab(cx + r + 30, cy + 34, "the rancher, at the time", t47 + .5, MUTED, 26, "start")]
    x0, L, wd, y0 = 190, 1207 * k, 80 * k, 560
    els += [bar(x0, x0 + L, y0, wd, t79 - .3, "rgba(201,193,238,.22)", 2.4),
            rect(x0, y0 - wd / 2, L, wd, "none", LILAC, 2.4, 6, t79 + 2.0, style="claimed")]
    els += [lab(x0, y0 - wd / 2 - 20, "1979: three-quarters of a mile", t79 + .4, LILAC, 30, "start"), lab(x0, y0 + wd / 2 + 40, "Marcel's memory", t79 + .8, MUTED, 26, "start")]
    els += [{"k": "scale", "x": 190, "y": 740, "w": round(200 * k, 1), "t": "200 m", "in": -1}]
    els += [lab(1500, 740, "memories drift", tm, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 3: a secret in the sky
def cabinet(x, y, w, h, at, fx="pop", open_at=None):
    """A filing cabinet: four drawers; one slides out at open_at."""
    els = [rect(x, y, w, h, "#5d6166", "#9aa4ae", 2, 4, at, fx=fx)]
    for k in range(4):
        dy = y + 10 + k * (h - 20) / 4
        els += [rect(x + 10, dy, w - 20, (h - 20) / 4 - 10, "#4a4e53", "#8a949e", 1.5, 3, at, fx=fx), rect(x + w / 2 - 18, dy + 14, 36, 8, "#cbbca8", at=at, fx=fx)]
    if open_at is not None:
        dy = y + 10 + 1 * (h - 20) / 4
        els += [rect(x - 30, dy - 6, w + 10, (h - 20) / 4 - 4, "#5a5e63", "#cbd4dc", 2, 3, open_at, fx="rise")]
    return els


def sc_schiff():
    """s23: the Capitol; a figure, Steven Schiff of New Mexico; an arrow to the auditors (the GAO), another to the Air Force's files; a
    drawer slides out, a folder lifts: TOP SECRET, PROJECT MOGUL, 1994."""
    els = building(260, 600, 330, -1, "dome", "#cbbca8", "#2f2822", None)
    els += [gl(260, 520, 300, -1, .14)]
    t94, ts, ta, tf, tn, tm = (T("schiff", "ninety-four"), T("schiff", "Steven Schiff"), T("schiff", "auditors"), T("schiff", "Air Force"),
                               T("schiff", "named a"), T("schiff", "Mogul"))
    els += [lab(889, 150, "1994", t94, GOLD, 34)]
    els += [ppl(500, 640, 150, ts - .2, "#a39a8e"), lab(500, 690, "Steven Schiff", ts, BONE, 28), lab(500, 724, "New Mexico", ts + .2, MUTED, 24)]
    els += [arr([(560, 560), (690, 560)], ta - .3, AMBER, 3, dur=.5)] + building(820, 640, 200, ta - .1, "hq", "#cbbca8", "#2f2822", "pop")
    els += [lab(820, 690, "the auditors", ta + .1, BONE, 28)]
    els += [arr([(950, 560), (1060, 560)], tf - .3, AMBER, 3, dur=.5)] + cabinet(1100, 380, 200, 260, tf - .1, "pop", tf + .4)
    els += [lab(1200, 690, "Air Force files", tf + .1, BONE, 28)]
    fx_, fy_ = 1330, 180
    els += [folder(fx_, fy_, 340, 230, tn - .2, MANILA, fx="rise"), stamp(fx_ + 170, fy_ + 70, "TOP SECRET", tn + .3, STAMP, 30, -6),
            ink(fx_ + 170, fy_ + 170, "PROJECT MOGUL", tm, TYPE, 34, weight=800)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_channel():
    """s24: the sound channel: a distant test flashes on the horizon; high up, a layer of air; sound rays bounce along inside it,
    thousands of kilometres, to a balloon-borne microphone; inset: a whispering gallery carries a whisper round its dome."""
    els = [poly([tuple(p) for p in ellipse(889, 2700, 2300, 2000, 80, 180, 360)] + [(3200, 2700), (-1500, 2700)], "#1d1813", "rgba(255,226,190,.35)", 2, -1)]
    tt, ta, th, tr_, tk, tl, tw = (T("channel", "top secret"), T("channel", "atomic bomb"), T("channel", "high in the sky"), T("channel", "low rumble"),
                                    T("channel", "thousands"), T("channel", "layer of air"), T("channel", "whispering gallery"))
    els += [stamp(250, 170, "TOP SECRET", tt, STAMP, 28, -5)]
    bx, by = 230, 700
    els += [gl(bx, by - 30, 160, ta, .9, "red"), poly([(bx - 16, by), (bx - 10, by - 60), (bx - 40, by - 76), (bx - 20, by - 104), (bx + 22, by - 104), (bx + 40, by - 76),
                                                     (bx + 10, by - 60), (bx + 16, by)], "#d27a5a", "#ffd0a0", 1.5, ta + .1, fx="rise"),
            lab(bx + 10, 772, "a distant test", ta + .3, BONE, 28)]
    top = lambda x: 300 + ((x - 889) / 2300.0) ** 2 * 2000 * .5
    xs = list(range(120, 1680, 40))
    upper = [(x, round(top(x), 1)) for x in xs]
    lower = [(x, round(top(x) + 90, 1)) for x in xs]
    els += [poly(upper + lower[::-1], "rgba(159,208,255,.10)", "none", 0, th - .2),
            ln(upper, th - .2, BLUE, 1.6, "inferred", draw=False, op=.7), ln(lower, th - .2, BLUE, 1.6, "inferred", draw=False, op=.7)]
    els += [lab(560, top(560) + 136, "a layer of air", tl, BLUE, 28)]
    zz = []
    for j, x in enumerate(range(260, 1400, 76)):
        zz.append((x, round(top(x) + (82 if j % 2 else 8), 1)))
    els += [ln([(bx + 10, by - 104)] + zz, tr_, BLUE, 2.6, "claimed", 2.4)]
    els += [lab(860, top(860) - 40, "thousands of km", tk, BLUE, 28)]
    mx = 1440
    els += balloon(mx, top(mx) - 30, 26, tr_ + 1.4, "pop", string=60) + [rect(mx - 12, top(mx) + 62, 24, 30, "#3a3532", "#cbbca8", 1.5, 4, tr_ + 1.6, fx="pop"),
                                                                       lab(mx, top(mx) + 130, "a microphone", tr_ + 1.8, BONE, 26)]
    gx, gy, gr = 1440, 760, 150
    els += [poly([tuple(p) for p in ellipse(gx, gy, gr, gr, 30, 180, 360)], "rgba(203,188,168,.08)", "#cbbca8", 2.4, tw - .4, fx="pop"),
            ln([(gx - gr - 20, gy), (gx + gr + 20, gy)], tw - .4, "#cbbca8", 2.4, draw=False),
            ppl(gx - gr + 22, gy, 40, tw - .3, "#a39a8e", "pop"), ppl(gx + gr - 22, gy, 40, tw - .3, "#a39a8e", "pop")]
    arc = [(gx + (gr - 12) * math.cos(math.radians(a)), gy - (gr - 12) * math.sin(math.radians(a))) for a in range(170, 9, -10)]
    els += [ln(arc, tw, GOLD, 2.4, "claimed", 1.4, curve=True), lab(gx, gy - gr - 22, "a whispering gallery", tw + .2, GOLD, 26)]
    return {"base": "dark", "stars": 70, "cam": CAM, "els": els}


ALV = View(-107.3, -103.9, 32.4, 34.6, (110, 150, 1000, 620))


def sc_alamo():
    """s25: south-central New Mexico: Alamogordo Army Air Field, the ranch, Roswell; a dashed line from the launch site to the ranch,
    '140 km'; at the right the New York University team launching a train of balloons at dawn."""
    v = ALV
    g = [rect(110, 150, 1000, 620, "#12202a"), poly([v.p(lo, la) for lo, la in NM], SAND, SAND_E, 2.2),
         ln([v.p(lo, la) for lo, la in RIO], -1, RIVER, 3, draw=False, curve=True, op=.55), ln([v.p(lo, la) for lo, la in PECOS], -1, RIVER, 2.6, draw=False, curve=True, op=.5)]
    els = [{"k": "group", "clip": [110, 150, 1000, 620, 6], "els": static(g), "in": -1}, rect(110, 150, 1000, 620, "none", "#3c4a58", 2, 6, -1)]
    ax_, ay_ = v.p(*PLACES["Alamogordo"])
    rx, ry = v.p(*PLACES["ranch"])
    wx, wy = v.p(*PLACES["Roswell"])
    tn, ta, tk = T("alamo", "New York University"), T("alamo", "Alamogordo"), T("alamo", "forty kilometres")
    els += [pin((rx, ry), "the ranch", -1, GOLD, "start", ly=-12), pin((wx, wy), "Roswell", -1, BONE, "start", ly=22)]
    els += [pin((ax_, ay_), "Alamogordo", ta, AU, "start", ly=24)]
    els += [ln([(ax_, ay_), (rx, ry)], tk - .6, AMBER, 3, "inferred", 1.0), lab((ax_ + rx) / 2 + 26, (ay_ + ry) / 2 + 6, "140 km", tk, AMBER, 30, "start")]
    els += [rect(1180, 150, 500, 620, "url(#k-sky-dawn)", "#8a7a66", 2, 8, tn - .4, fx="pop")]
    els += [rect(1180, 690, 500, 80, "#3a2f24", at=tn - .4, fx="pop")]
    els += [grp(train_icon(1440, 200, 470, -1, None, 9), tn, "rise")]
    for k, x in enumerate((1330, 1390, 1500)):
        els.append(ppl(x, 700, 70, tn + .2 + .1 * k, "#2a2420", "pop"))
    els += [lab(1430, 740, "New York University team", tn + .4, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


SC_M = 4.5        # units per metre on the train panel


def sc_train():
    """s26: the train to scale (4.5 units = 1 m): 23 balloons 6.1 m apart on one line (134 m), radar reflectors among them, the
    instrument box at the foot; beside it a football pitch (105 x 68 m) standing on end; at the foot a person, 1.7 m, ringed."""
    G = 790
    els = [rect(-20, G, 1820, 260, "#2a2219", at=-1), ln([(-20, G), (1800, G)], -1, "rgba(255,226,190,.3)", 1.5, draw=False)]
    x = 700
    top = G - 26 - 22 * 6.1 * SC_M
    tn, tt, ts, tl, tf, te = (T("train", "Not one balloon"), T("train", "twenty-three"), T("train", "six metres"), T("train", "longer than"),
                              T("train", "football pitch"), T("train", "stood on end"))
    els += [ln([(x, top), (x, G - 14)], .3, "#cbbca8", 2, dur=1.0)]
    ys = [round(top + k * 6.1 * SC_M, 1) for k in range(23)]
    els += balloon(x, ys[0], 10, tn, "pop")
    for k in range(1, 23):
        els += balloon(x, ys[k], 10, round(tt + .07 * k, 2), "pop")
    for k in (8, 15):
        yy = (ys[k] + ys[k + 1]) / 2
        els += [grp(reflector(x, yy, 16, -1, None, False, edge="#e8c890", sw=1.6), tt + 1.6, "pop")]
    els += [rect(x - 9, G - 22, 18, 16, "#3a3532", "#cbbca8", 1.2, 2, tt + 1.7, fx="pop")]
    els += [lab(x + 40, ys[0] + 8, "23 balloons", tt + .2, GOLD, 30, "start")]
    els += [ln([(x + 26, ys[3]), (x + 36, ys[3]), (x + 36, ys[4]), (x + 26, ys[4])], ts - .2, BONE, 2, "known", .4), lab(x + 48, (ys[3] + ys[4]) / 2 + 9, "6 m apart", ts, BONE, 26, "start")]
    els += [{"k": "dim", "x1": x - 60, "y1": ys[0], "x2": x - 60, "y2": ys[22], "t": "more than 130 m", "c": GOLD, "fx": "draw", "dur": 1.2, "in": round(tl, 2), "lx": -24}]
    pw, ph = 68 * SC_M, 105 * SC_M
    px = 1160
    els += pitch(px, G - ph, pw, ph, te - .2)
    els += [lab(px + pw / 2, G - ph - 52, "a football pitch", tf + .1, BONE, 28), lab(px + pw / 2, G - ph - 20, "105 m", tf + .3, MUTED, 26)]
    els += [ppl(x + 22, G, 1.7 * SC_M, -1, "#e8d6b8", None), I.ring(x + 22, G - 6, 14, te + .6, AMBER, 2), lab(x + 60, G - 40, "a person", te + .8, AMBER, 26, "start")]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


def sc_reflector():
    """s27: one radar reflector, close: balsa sticks and foil-backed paper; a radar dish's beam bounces back from it; made by a toy
    company; a roll of its tape unrolls along a stick: pink and purple flowers."""
    cx, cy, r = 640, 440, 270
    els = [gl(cx, cy, 520, -1, .12)] + reflector(cx, cy, r, .2, "pop", False)
    tb, tf, tt, ty, tw = T("reflector", "balsa sticks"), T("reflector", "foil-backed"), T("reflector", "tracked"), T("reflector", "toy company"), T("reflector", "flowers")
    els += [arr([(330, 760), (cx - 60, cy + 150)], tb - .2, BONE, 2.5, dur=.5), lab(320, 790 - 18, "balsa sticks", tb, BONE, 28)]
    els += [arr([(1010, 200), (cx + 140, cy - 90)], tf - .2, BONE, 2.5, dur=.5), lab(1020, 186, "foil-backed paper", tf, BONE, 28, "start")]
    els += dish(1500, 780, 1.4, tt - .6)
    dx_, dy_ = 1440, 600
    for k in range(4):
        t = (k + 1) / 5
        px, py = dx_ + (cx + r * .55 - dx_) * t, dy_ + (cy + 60 - dy_) * t
        els.append(ln([(px + 16, py - 30), (px - 4, py), (px + 16, py + 30)], round(tt + .15 * k, 2), BLUE, 2.4, "claimed", .3, curve=True))
    els += [lab(1180, 500, "tracked by radar", tt + .4, BLUE, 28)]
    bx, by = 1360, 260
    els += [rect(bx - 90, by - 10, 180, 120, "#3a3129", "#cbbca8", 2, 3, ty - .2, fx="pop"), poly([(bx - 100, by - 10), (bx, by - 70), (bx + 100, by - 10)], "#3a3129", "#cbbca8", 2, ty - .2, fx="pop")]
    els += [poly([(bx - 20, by + 30), (bx, by + 10), (bx + 20, by + 30), (bx, by + 60)], "#e0679a", "#fff", 1.2, ty, fx="pop"), ln([(bx, by + 60), (bx + 8, by + 90)], ty, "#fff", 1.5, draw=False)]
    els += [lab(bx, by + 160, "a toy company", ty + .1, GOLD, 28)]
    els += tape_strip(cx - r * .82, cy + r * .44, cx - r * .12, cy + r * .06, tw - .8, 22)
    els += [lab(330, 690, "tape with flowers", tw, PINK, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def sc_flight4():
    """s28: 4 June 1947: Flight 4 rises and drifts away (never recovered); 14 June: the debris on the ranch; a dotted line between, 10 days."""
    tl, tn, td = T("flight4", "Flight Four"), T("flight4", "never got"), T("flight4", "Ten days")
    els = calendar(320, 160, 220, 4, "June", .3, GOLD)
    els += [ln([(470, 760), (560, 600), (640, 420), (760, 170)], tl - .2, AMBER, 2.6, "claimed", 1.6, curve=True)]
    els += [grp(train_icon(640, 250, 280, -1, None, 7), tl, "rise")]
    els += [lab(700, 330, "Flight 4", tl, GOLD, 32, "start")]
    els += tag(790, 420, "never recovered", tn, MUTED, 26, "inferred")
    els += calendar(1460, 160, 220, 14, "June", td - .2, GOLD)
    els += [rect(1290, 560, 340, 160, "#3a2f24", "#8a7a66", 1.5, 8, td, fx="pop")] + [grp(glints(171, 10, 1320, 1600, 600, 700, -1, .8, False) +
                                                                                       sticks_scatter(173, 5, 1330, 1590, 620, 700, -1, .8), td + .1, "pop")]
    els += [lab(1460, 760, "the debris", td + .3, BONE, 28)]
    arc = [(700 + (1270 - 700) * t, 660 - 140 * math.sin(math.pi * t)) for t in [j / 30 for j in range(31)]]
    els += dots_along(arc, td + .3, 1.2, AMBER, 4) + [lab(985, 490, "10 days", td + 1.0, AMBER, 32)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def sc_match():
    """s29: the match: the rancher's 1947 list at the left (rubber, foil and paper, sticks, flowered tape), a Mogul train's parts at the
    right (a balloon, a reflector, a balsa stick, the toy company's tape); gold lines join each pair as named, a tick on each."""
    L, Rx = 330, 1450
    rows = [260, 400, 540, 680]
    els = [lab(L, 170, "1947: the rancher", .2, GOLD, 30), lab(Rx, 170, "a Mogul train", .2, GOLD, 30)]
    els += rubber(L - 70, rows[0] - 10, 140, -1, 1, 8) + rubber(L - 66, rows[0] + 14, 132, -1, 3, 8)
    els += foil(L - 40, rows[1], .7, -1, None) + scrap(L + 50, rows[1], .55, -1, None)
    els += stick(L - 80, rows[2] - 20, L + 80, rows[2] + 20, -1, 7) + stick(L - 70, rows[2] + 20, L + 70, rows[2] - 18, -1, 7)
    els += stick(L - 90, rows[3], L + 90, rows[3] + 6, -1, 7) + tape_strip(L - 60, rows[3] + 1, L + 60, rows[3] + 5, -1, 18, None)
    tr_, tf, tb, tt = T("match", "Rubber"), T("match", "Foil and paper"), T("match", "Balsa"), T("match", "Tape with")
    items = [(tr_, "rubber: balloons"), (tf, "foil and paper: reflectors"), (tb, "balsa sticks"), (tt, "tape with flowers")]
    rights = [balloon(Rx, rows[0] - 6, 34, tr_ + .2, "pop"), reflector(Rx, rows[1], 44, tf + .2, "pop", False),
              stick(Rx - 80, rows[2] - 12, Rx + 80, rows[2] + 12, tb + .2, 7, fx="pop"),
              stick(Rx - 90, rows[3], Rx + 90, rows[3] + 6, tt + .1, 7, fx="pop") + tape_strip(Rx - 60, rows[3] + 1, Rx + 60, rows[3] + 5, tt + .2, 18)]
    for k, ((t, txt), rr) in enumerate(zip(items, rights)):
        y = rows[k]
        els += [ln([(L + 140, y), (Rx - 130, y)], t, GOLD, 2.4, dur=.6), lab(889, y - 16, txt, t + .2, BONE, 28)]
        els += rr + [tick(889, y + 30, t + .5, GREEN, .9, 5)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_writing():
    """s30: close on a balsa stick wrapped in the toy company's tape (pink or lavender figures); Marcel's words as recalled, dotted:
    'alien writing?'; the weather officer, in 1994: faded figures on tape."""
    els = [rect(140, 236, 1500, 52, BALSA, BALSA_E, 2, 6, -1)]
    for k in range(8):
        x0 = 220 + 175 * k
        els += tape_strip(x0, 300, x0 + 60, 224, -1, 30, None, n=3)
    tw, tm, tp, ta = T("writing", "weather officer"), T("writing", "Marcel showing"), T("writing", "pink or lavender"), T("writing", "alien writing")
    els += [lab(889, 360, "pink or lavender figures", tp, PINK, 28)]
    els += figure(1330, 780, 240, .3, "#8a96a2") + [lab(1330, 470, "the weather officer", tw, BONE, 26)] + tag(1330, 506, "recalled in 1994", tw + .3, MUTED, 24)
    els += figure(450, 780, 240, .4, "#a39a8e")
    els += [rect(270, 440, 360, 70, "rgba(18,13,10,.88)", LILAC, 2.4, 22, ta - .2, fx="pop", style="claimed"), lab(450, 486, "alien writing?", ta, LILAC, 30)]
    els += [lab(450, 420, "Marcel, as recalled", ta + .3, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_gap():
    """s31: the Mogul folder, TOP SECRET, ticked: a real secret; a dotted saucer struck through: not that one. Then the gap: a table of
    flights with rows 2, 3 and 4 empty; a diary open at 4 June; a path worked out from wind records; still argued."""
    els = [folder(140, 220, 380, 260, -1, MANILA), stamp(330, 300, "TOP SECRET", -1, STAMP, 30, -6), ink(330, 410, "PROJECT MOGUL", -1, TYPE, 32, weight=800)]
    ta, tn, tf, td, tw, tg = (T("gap", "A real secret"), T("gap", "not that one"), T("gap", "formal reports"), T("gap", "diary"),
                              T("gap", "wind"), T("gap", "still argued"))
    els += [tick(330, 520, ta, GREEN, 1.6), lab(330, 590, "a real secret", ta + .2, GREEN, 28)]
    els += saucer(330, 700, .5, tn - .3) + [I.strike(230, 740, 430, 660, tn, RED, 6)]
    x, y = 640, 160
    els += [rect(x, y, 420, 560, PAPER, PAPER_D, 1.5, 3, tf - .6, fx="pop"), ink(x + 210, y + 50, "NYU flights, 1947", tf - .5, TYPE, 26, weight=700)]
    for k in range(8):
        yy = y + 90 + 56 * k
        miss = k in (0, 1, 2)
        els += [ink(x + 40, yy + 30, "Flight %d" % (k + 2), tf - .4, "#9a8a70" if miss else TYPE, 24, a="start")]
        if miss:
            els += [rect(x + 170, yy + 8, 220, 30, "none", "#b9ab90", 2, 4, tf + .1 * k, style="inferred")]
        else:
            els += typed(x + 170, yy + 24, 210, 1, tf - .4, 20, seed=181 + k)
    els += [lab(x + 210, 760, "not in the reports", tf + .4, BONE, 26)]
    dx, dy = 1200, 180
    els += [rect(dx, dy, 220, 160, PAPER, PAPER_D, 1.5, 3, td - .3, fx="pop"), rect(dx + 220, dy, 220, 160, PAPER, PAPER_D, 1.5, 3, td - .3, fx="pop"),
            ln([(dx + 220, dy), (dx + 220, dy + 160)], td - .3, "#9a8a70", 3, draw=False)]
    els += typed(dx + 20, dy + 30, 180, 5, td - .2, 24, c="#5a4a3a", seed=191) + typed(dx + 240, dy + 30, 180, 5, td - .2, 24, c="#5a4a3a", seed=193)
    els += [ln([(dx + 236, dy + 104), (dx + 410, dy + 104)], td + .1, AU, 4, dur=.4), lab(dx + 220, dy + 196, "one diary, 4 June", td + .2, GOLD, 26)]
    wx, wy = 1210, 420
    els += [rect(wx, wy, 430, 230, "#1c2830", "#3c4a58", 2, 6, tw - .4, fx="pop"), dot(wx + 70, wy + 190, 8, AU, tw - .3), dot(wx + 360, wy + 50, 8, GOLD, tw - .3)]
    els += [arr([(wx + 120 + 60 * k, wy + 140 - 30 * k), (wx + 160 + 60 * k, wy + 120 - 30 * k)], tw - .2 + .1 * k, "#8fb6d6", 2, dur=.3) for k in range(4)]
    els += [ln([(wx + 70, wy + 190), (wx + 150, wy + 100), (wx + 260, wy + 120), (wx + 360, wy + 50)], tw, GOLD, 2.6, "inferred", 1.0, curve=True),
            lab(wx + 215, wy + 280, "a path from wind records", tw + .3, BONE, 26)]
    els += [lab(1425, 760, "still argued", tg, LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 4: dummies, a film and lost files
def teletype(x, y, w, h, at, fx="rise"):
    """The FBI teletype of 8 July 1947: a strip of paper, its header, and a sketch of what it describes: a hexagon hanging from a balloon."""
    els = [rect(x + 8, y + 10, w, h, "rgba(0,0,0,.45)", at=at, fx=fx), rect(x, y, w, h, "#f2ecd8", PAPER_D, 1.5, 2, at, fx=fx)]
    els += [ink(x + w / 2, y + 40, "FBI, 8 July 1947", at + .1, TYPE, 26, weight=700, st="mono")]
    els += typed(x + 24, y + 70, w * .5, 4, at + .2, 22, seed=201)
    bx, by = x + w * .78, y + 66
    els += balloon(bx, by, 22, at + .3, "pop", string=40) + reflector(bx, by + 92, 22, at + .4, "pop", False)
    return els


def history_page(x, y, w, h, at, fx="rise"):
    els = [rect(x + 8, y + 10, w, h, "rgba(0,0,0,.45)", at=at, fx=fx), rect(x, y, w, h, PAPER, PAPER_D, 1.5, 2, at, fx=fx)]
    els += [ink(x + w / 2, y + 40, "509th history", at + .1, TYPE, 26, weight=700)]
    els += typed(x + 24, y + 70, w - 48, 3, at + .2, 22, seed=211)
    els += [rect(x + 18, y + h - 56, w - 36, 40, "rgba(242,201,142,.6)", at=at + .3, fx=fx), ink(x + w / 2, y + h - 28, "radar tracking balloon", at + .35, TYPE, 24, weight=600)]
    return els


def sc_agencies():
    """s32: six agencies in a row, each lit as it is searched; only two sheets from 1947 come forward: the base history (radar tracking
    balloon) and the FBI teletype (a hexagonal disc hanging from a balloon)."""
    t6, th, tf = T("agencies", "six agencies"), T("agencies", "base history"), T("agencies", "FBI message")
    kinds = ["dome", "hq", "block", "columns", "block", "hq"]
    els = [lab(889, 150, "1995", .2, GOLD, 34)]
    for k, kd in enumerate(kinds):
        x = 230 + 264 * k
        els += building(x, 470, 170 if kd != "hq" else 130, .2 + .05 * k, kd, "#cbbca8", "#2f2822", "pop")
        els += [gl(x, 400, 130, round(t6 + .2 * k, 2), .45)]
    els += [lab(889, 530, "6 agencies searched", t6 + 1.2, BONE, 28)]
    els += history_page(430, 580, 360, 200, th - .2) + teletype(990, 580, 400, 200, tf - .2)
    els += [lab(1560, 690, "2 documents", tf + .6, GOLD, 30), lab(1560, 726, "from 1947", tf + .7, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_destroyed():
    """s33: archive shelves; one run of boxes, the base's outgoing messages October 1946 to December 1949, fades to dashed outlines; a
    disposition form with blank fields: who? when? authority?; a dashed arrow from Roswell to its superiors."""
    els = []
    for row, yb in enumerate((300, 520)):
        els += [rect(120, yb, 1540, 14, STEEL, "#8a949e", 1.2, 2, -1), rect(120, yb - 190, 12, 204, STEEL_D, at=-1), rect(1648, yb - 190, 12, 204, STEEL_D, at=-1)]
        for k in range(10):
            x = 150 + 150 * k
            if row == 1 and 3 <= k <= 6:
                continue
            els += abox(x, yb - 120, 130, 120, -1, lab_=True)
    td, tr_, ts = T("destroyed", "Destroyed"), T("destroyed", "No record"), T("destroyed", "superiors")
    for k in range(3, 7):
        x = 150 + 150 * k
        els += abox(x, 400, 130, 120, -1, lab_=True)
        els += [veil(x - 14, 366, 158, 156, td - .4 + .1 * k, FLAT, 1.0, .8)]
        els += [rect(x, 400, 130, 120, "none", "#c9a27a", 2, 2, td + .3 + .1 * k, style="inferred")]
    els += [rect(600, 532, 600, 36, PAPER, PAPER_D, 1.2, 3, .3), ink(900, 558, "outgoing messages, Oct 1946 to Dec 1949", .3, TYPE, 24, weight=700)]
    fx_, fy_ = 140, 590
    els += [rect(fx_, fy_, 520, 190, PAPER, PAPER_D, 1.5, 3, tr_ - .3, fx="rise"), ink(fx_ + 260, fy_ + 36, "records disposition", tr_ - .2, TYPE, 24, weight=700)]
    for k, t in enumerate(("who?", "when?", "authority?")):
        y = fy_ + 82 + 40 * k
        els += [ink(fx_ + 40, y, t, tr_ + .3 * k, STAMP, 26, a="start", weight=700), ln([(fx_ + 200, y + 4), (fx_ + 480, y + 4)], tr_ + .3 * k, "#9a8a70", 2, draw=False)]
    els += [rect(800, 640, 220, 90, "#2a241d", "#cbbca8", 2, 8, ts - .6, fx="pop"), lab(910, 696, "Roswell", ts - .5, BONE, 28),
            arr([(1030, 685), (1260, 685)], ts - .2, AMBER, 3, "inferred", .8), rect(1270, 640, 300, 90, "#2a241d", "#cbbca8", 2, 8, ts, fx="pop", style="inferred"),
            lab(1420, 696, "its superiors", ts + .1, BONE, 28), lab(1150, 640, "?", ts + .4, LILAC, 44, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def screen_scene(x, y, w, h):
    """Inside the television: a grainy grey picture, two hooded figures beside a table with a sheet over a still form (nothing more)."""
    g = [rect(x, y, w, h, "#6d6f70")]
    g += [rect(x + w * .2, y + h * .58, w * .6, h * .1, "#4a4c4e"), rect(x + w * .24, y + h * .68, w * .03, h * .3, "#3e4042"), rect(x + w * .73, y + h * .68, w * .03, h * .3, "#3e4042"),
          poly([tuple(p) for p in ellipse(x + w * .5, y + h * .58, w * .26, h * .07, 20, 180, 360)], "#c9c9c4", "none", 0)]
    for fx_ in (.18, .82):
        g += [ppl(x + w * fx_, y + h * .98, h * .62, -1, "#a9abad", None), circ(x + w * fx_, y + h * .98 - h * .62 * .9, h * .07, "#9a9c9e")]
    g += grain(221, 160, x, x + w, y, y + h, -1, "#e8e8e8", .35)
    g += [ln([(x, y + h * k / 18), (x + w, y + h * k / 18)], -1, "#000000", 1.4, draw=False, op=.18) for k in range(18)]
    return [{"k": "group", "clip": [x, y, w, h, 22], "els": static(g), "in": -1}]


def sc_tv():
    """s34: 1995: an old television in a dark room; on its grainy grey screen two hooded figures beside a table with a sheet over a still
    form; broadcast arcs spread from it: round the world."""
    els = [rect(-20, 640, 1820, 400, "#191410", at=-1), gl(889, 420, 700, -1, .12, "scan")]
    sx, sy, sw, sh = 640, 230, 500, 360
    els += tv(sx, sy, sw, sh, -1) + screen_scene(sx, sy, sw, sh)
    els += [rect(sx - 80, sy + sh + 60, sw + 160, 90, "#2a2018", "#5a4a3a", 2, 6, -1)]
    tw, tr_ = T("tv", "round the world"), T("tv", "said to come")
    els += [lab(260, 180, "1995", .3, GOLD, 34)]
    for k in range(4):
        rr = 320 + 80 * k
        els.append(ln([tuple(p) for p in ellipse(889, 410, rr, rr * .72, 16, 200, 340)], round(tw + .2 * k, 2), BLUE, 2.2, "claimed", .6, curve=True))
        els.append(ln([tuple(p) for p in ellipse(889, 410, rr, rr * .72, 16, -20, 20)], round(tw + .2 * k, 2), BLUE, 2.2, "claimed", .6, curve=True))
    els += [lab(1480, 190, "round the world", tw + .5, BLUE, 28)]
    els += [lab(889, 776, "said to be from Roswell", tr_, LILAC, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_set():
    """s35: the same scene as a set in a London flat: sheets pinned to the walls, a lamp on a stand, a film camera on a tripod, a sculpted
    dummy on the table. A re-creation; his claim (dotted): a restoration of real footage; an empty film can: never shown."""
    els = [rect(-20, -20, 1820, 700, "#3a2f2a", at=-1), rect(-20, 680, 1820, 360, "#2a211b", at=-1)]
    els += [rect(160 + 210 * k, 150, 180, 400, "#e8e4da", "#b9b0a0", 1.5, 2, -1, op=.85) for k in range(7)]
    els += [circ(250 + 210 * k, 162, 5, "#8a7a66", at=-1) for k in range(7)]
    els += [rect(1480, 160, 180, 240, "#1a2430", "#6a5a48", 4, 2, -1), ln([(1570, 160), (1570, 400)], -1, "#6a5a48", 4, draw=False),
            ln([(1480, 280), (1660, 280)], -1, "#6a5a48", 4, draw=False)]
    els += [rect(620, 560, 560, 30, "#5a4636", "#8a6a48", 2, 3, -1), rect(650, 590, 20, 140, "#3a2c20", at=-1), rect(1130, 590, 20, 140, "#3a2c20", at=-1),
            poly([tuple(p) for p in ellipse(900, 560, 230, 46, 24, 180, 360)], "#d9d2c4", "#a89c88", 1.5, -1, curve=True), circ(690, 528, 34, "#d9d2c4", "#a89c88", 1.5, -1)]
    els += [ln([(1300, 730), (1300, 260)], -1, "#2a2420", 6, draw=False), poly([(1250, 260), (1350, 260), (1330, 200), (1270, 200)], "#2a2420", "#8a7a66", 1.5, -1),
            gl(1260, 360, 420, -1, .45)]
    els += [ln([(380, 730), (420, 560)], -1, "#2a2420", 5, draw=False), ln([(460, 730), (420, 560)], -1, "#2a2420", 5, draw=False), ln([(420, 730), (420, 560)], -1, "#2a2420", 5, draw=False),
            rect(360, 470, 130, 90, "#1e1a17", "#8a7a66", 2, 6, -1), circ(392, 452, 30, "#1e1a17", "#8a7a66", 2, -1), circ(458, 452, 30, "#1e1a17", "#8a7a66", 2, -1),
            rect(490, 494, 50, 40, "#1e1a17", "#8a7a66", 2, 4, -1)]
    t06, tf, tc, tr_, tn = T("set", "two thousand and six"), T("set", "London flat"), T("set", "re-creation"), T("set", "restoration"), T("set", "never been shown")
    els += [lab(260, 186, "2006", t06, GOLD, 34)]
    els += [lab(900, 470, "a re-creation", tc, GOLD, 32), lab(1500, 470, "a London flat", tf, BONE, 28)]
    els += [rect(560, 610, 680, 64, "rgba(18,13,10,.9)", LILAC, 2.4, 22, tr_ - .2, fx="pop", style="claimed"), lab(900, 652, "his account: a restoration", tr_, LILAC, 28)]
    els += [circ(1520, 700, 52, "none", "#cbbca8", 2.4, tn - .2, fx="pop", style="inferred"), circ(1520, 700, 14, "none", "#cbbca8", 2, tn - .2, fx="pop", style="inferred"),
            lab(1520, 784 - 10, "never shown", tn, MUTED, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


DX = lambda yr: round(260 + (yr - 1945) / 17 * 1260, 1)      # the 1945 to 1962 time line on the dummies panel
DY = 690


def sc_dummies():
    """s36: a desert sky: a high-altitude balloon; test dummies come down under parachutes; one lies on the ground, a recovery truck
    comes; below, a time line 1945 to 1962: 1947 alone at the left, and a band 1954 to 1959 where 67 dots pop: 67 dummies."""
    els = [rect(-20, 560, 1820, 460, "#6b5a40", at=-1), ln([(-20, 560), (1800, 560)], -1, "rgba(255,236,206,.35)", 1.5, draw=False)]
    els += scrub(231, 10, 100, 1700, 580, 650, -1, "#4a4a2e", s=.7, rim="rgba(255,236,190,.25)")
    els += balloon(260, 170, 64, -1, None, string=120) + gondola(260, 330, .8, -1, 0)
    t97, td, t67 = T("dummies", "ninety-seven"), T("dummies", "test dummies"), T("dummies", "Sixty-seven")
    els += [lab(1500, 190, "Air Force, 1997", t97, GOLD, 30)]
    for k, (x, y) in enumerate(((520, 230), (720, 330), (920, 210))):
        els += parachute(x, y, 120, td - .2 + .3 * k) + dummy(x, y + 112 + 70, 70, td + .3 * k)
    els += [poly([(560, 586), (680, 580), (690, 590), (566, 596)], "#a8aeb4", "#6a6e72", 1.2, td + 1.0, fx="pop"), circ(552, 588, 9, "#a8aeb4", at=td + 1.0, fx="pop")]
    els += truck(820, 610, .45, td + 1.2, "#4a5a46", "rgba(255,236,206,.4)", "rise", face=-1)
    ticks = [(DX(y_), str(y_)) for y_ in (1945, 1950, 1955, 1960)]
    els += [axis(DX(1945), DX(1962), DY + 30, ticks, .2), dot(DX(1947), DY + 30, 11, AU, .3), lab(DX(1947), DY - 6, "1947", .3, AU, 28)]
    els += [{"k": "band", "x0": DX(1954), "x1": DX(1959.15), "y": DY + 2, "h": 14, "c": LILAC, "in": round(t67 - .2, 2), "dur": .8}]
    for k in range(67):
        x = DX(1954) + (DX(1959.15) - DX(1954)) * (k % 34 + .5) / 34
        els.append(dot(round(x, 1), DY - 12 - 14 * (k // 34), 4, "#e8eef2", round(t67 + .015 * k, 3)))
    els += [lab((DX(1954) + DX(1959)) / 2, DY - 50, "67 dummies, 1954 to 1959", t67 + .8, BONE, 28)]
    return {"base": "sky", "tod": "day", "ground": 560, "groundc": "#6b5a40", "sun": [1180, 150, 24], "cam": CAM, "els": els}


def add_accidents():
    """s37 (the time line, closer): 1956: a small dark aircraft and eleven quiet marks, eleven airmen died (nothing more is shown);
    1959: a balloon gondola tilted on the ground, a pilot injured."""
    tc, tb = T("accidents", "air crash"), T("accidents", "balloon accident")
    x1, x2 = DX(1956.5), DX(1959.4)
    c1, c2 = 1090, 1430
    els = [rect(c1 - 150, 300, 300, 200, "rgba(18,13,10,.9)", "#8a7a66", 2, 14, tc - .3, fx="pop"), ln([(c1, 500), (x1, DY - 16)], tc - .2, MUTED, 2, "inferred", .5)]
    els += plane_icon(c1, 370, .6, tc, "#8a8478")
    els += [dot(round(c1 - 75 + 15 * k, 1), 432, 4.5, BONE, round(tc + .3 + .05 * k, 2), op=.85) for k in range(11)]
    els += [lab(c1, 476, "1956: eleven airmen died", tc + .4, BONE, 24)]
    els += [rect(c2 - 150, 300, 300, 200, "rgba(18,13,10,.9)", "#8a7a66", 2, 14, tb - .3, fx="pop"), ln([(c2, 500), (x2, DY - 16)], tb - .2, MUTED, 2, "inferred", .5)]
    els += gondola(c2, 420, .9, tb, 16, "#8a96a2")
    els += [lab(c2, 476, "1959: a pilot injured", tb + .3, BONE, 24)]
    return els


def snapshot(x, y, w, h, kind, yr, at, fx="pop", rot=0):
    g = [rect(x, y, w, h, "#f2ecdc", "#cbbca8", 1.5, 2), rect(x + 8, y + 8, w - 16, h - 34, "#3a4a5a")]
    ix, iy, iw, ih = x + 8, y + 8, w - 16, h - 34
    if kind == "beach":
        g += [rect(ix, iy + ih * .55, iw, ih * .45, "#d9c08a"), rect(ix, iy + ih * .4, iw, ih * .15, "#3f7f9c"), circ(ix + iw * .75, iy + ih * .25, ih * .12, "#ffe2a8")]
    elif kind == "mountain":
        g += [poly([(ix, iy + ih), (ix + iw * .35, iy + ih * .25), (ix + iw * .6, iy + ih * .6), (ix + iw * .8, iy + ih * .35), (ix + iw, iy + ih)], "#5a6a5a")]
    else:
        g += [rect(ix, iy + ih * .6, iw, ih * .4, "#3f7f9c"), poly([(ix + iw * .1, iy + ih * .6), (ix + iw * .2, iy + ih * .2), (ix + iw * .3, iy + ih * .6)], "#2f4a32")]
    g += [nl(x + w - 34, y + h - 7, yr, 24, -1, TYPE, st="lab", weight=600)]
    tr = "rotate(%s %s %s)" % (rot, round(x + w / 2, 1), round(y + h / 2, 1)) if rot else None
    return grp(g, at, fx, tr=tr)


def sc_merge():
    """s38: the time line again: the 1950s marks (dummies, the 1956 crash, the 1959 gondola) slide along curved arrows onto 1947, which
    becomes a calendar page, July 1947: merged in memory. Below: three holiday snapshots from different summers go into one album: one trip."""
    X = lambda yr: round(300 + (yr - 1945) / 17 * 1100, 1)
    els = [axis(X(1945), X(1962), 300, [(X(1950), "1950"), (X(1955), "1955"), (X(1960), "1960")], -1), dot(X(1947), 300, 10, AU, -1)]
    els += [dot(round(X(1954) + (X(1959) - X(1954)) * k / 20, 1), 270, 4, "#e8eef2", -1) for k in range(21)]
    els += plane_icon(X(1956.5), 228, .35, -1, "#55504a") + gondola(X(1959.4), 236, .45, -1, 18, "#8a96a2")
    tm, tj, th, ta, to = T("merge", "merged in memory"), T("merge", "July"), T("merge", "holiday photos"), T("merge", "one album"), T("merge", "single trip")
    for k, yr in enumerate((1955.5, 1956.5, 1959.4)):
        els += [arr([(X(yr), 250), ((X(yr) + X(1947)) / 2, 150 - 10 * k), (X(1947) + 30, 262)], round(tm - .6 + .25 * k, 2), LILAC, 2.6, dur=.8, curve=True)]
    els += calendar(X(1947), 330, 120, 1947, "July", tj, LILAC, year="")
    els += [lab(X(1947) + 260, 400, "merged in memory", tm + .3, LILAC, 28, "start")]
    shots = [("beach", "1954", 220), ("mountain", "1956", 500), ("lake", "1959", 780)]
    for k, (kind, yr, x) in enumerate(shots):
        els += [snapshot(x, 520, 220, 170, kind, yr, round(th - .2 + .2 * k, 2))]
        els += [veil(x - 6, 514, 236, 186, round(ta + .2 * k, 2), FLAT, .85, .6)]
    els += [rect(1130, 470, 470, 300, "#3a2c20", "#8a6a48", 3, 6, ta - .4, fx="pop"), ln([(1365, 470), (1365, 770)], ta - .4, "#2a2016", 4, draw=False)]
    for k, (kind, yr, _) in enumerate(shots):
        els += [snapshot(1150 + 60 * k + (220 if k == 2 else 0) * 0, 490 + 20 * k, 200, 150, kind, yr, round(ta + .25 * k, 2), "pop", rot=(-6 + 6 * k))]
    els += [lab(1365, 806 - 20, "one trip", to, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_answers():
    """s39: four answers as cards, counted: 1947 a disc, 1947 a balloon, 1994 Mogul, 1997 dummies (dropped from 1954, seven years
    after 1947); a gauge of trust drains."""
    xs = [250, 650, 1050, 1450]
    els = [rect(x - 170, 180, 340, 320, "rgba(18,13,10,.6)", "#8a7a66", 2, 14, .2 + .1 * k, fx="pop") for k, x in enumerate(xs)]
    ta, tb, tm, td, tt = T("answers", "A disc"), T("answers", "weather balloon"), T("answers", "Mogul"), T("answers", "Dummies that"), T("answers", "trust")
    els += saucer(xs[0], 340, .7, ta) + [lab(xs[0], 470, "1947: a disc", ta + .1, LILAC, 28)]
    els += balloon(xs[1], 290, 44, tb, "pop", string=60) + reflector(xs[1], 410, 30, tb + .2, "pop", False) + [lab(xs[1], 470, "1947: a balloon", tb + .1, BONE, 28)]
    els += [grp(train_icon(xs[2], 210, 230, -1, None, 7), tm, "pop"), lab(xs[2], 470, "1994: Mogul", tm + .1, BONE, 28)]
    els += parachute(xs[3], 210, 110, td - .1) + dummy(xs[3], 420, 90, td) + [lab(xs[3], 470, "1997: dummies", td + .1, BONE, 28)]
    els += [ln([(xs[3] - 150, 530), (xs[3] - 150, 548), (xs[3] + 150, 548), (xs[3] + 150, 530)], td + 1.0, MUTED, 2, dur=.4),
            lab(xs[3], 590, "dropped from 1954", td + 1.2, MUTED, 26)]
    els += [rect(500, 676, 840, 40, "#2a241d", "#8a7a66", 2, 20, .4), rect(506, 682, 828, 28, GOLD, at=.6, op=.85)]
    els += [{"k": "line", "p": [[1320, 696], [520, 696]], "c": "#2a241d", "w": 30, "fx": "draw", "dur": 1.6, "in": round(tt, 2)}, lab(470, 706, "trust", .4, BONE, 28, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_aaro():
    """s40: the Pentagon review of 2024: a report cover rises; three findings light as said (a military balloon, test dummies, later
    accidents); a balance with both pans empty and level: no new evidence."""
    els = desk_bg()
    x, y, w, h = 230, 150, 520, 620
    els += report_cover(x, y, w, h, .3, [("Historical Record Report", 90, 30, 700), ("Volume I", 132, 26, None), ("March 2024", 170, 26, None)], seed=241, body=7)
    els += [circ(x + w / 2, y + 290, 60, "none", "#8a7a66", 3, .5), circ(x + w / 2, y + 290, 44, "none", "#8a7a66", 2, .5)]
    tb, td, tl, tn = T("aaro", "military balloon"), T("aaro", "dummies"), T("aaro", "later accidents"), T("aaro", "no new evidence")
    rows = [(260, tb, "a military balloon"), (390, td, "test dummies"), (520, tl, "later accidents")]
    for y_, t, txt in rows:
        els += [rect(900, y_ - 50, 700, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.4)", 1.5, 12, t - .2, fx="pop"), lab(1040, y_ + 10, txt, t, BONE, 30, "start")]
    els += balloon(960, 248, 26, tb - .1, "pop", string=30)
    els += dummy(960, 432, 64, td - .1)
    els += plane_icon(940, 514, .4, tl - .1, "#8a8478") + gondola(985, 548, .35, tl - .1, 18, "#8a96a2")
    els += [lab(1600, 150, "2024", .3, GOLD, 34)]
    els += balance(1250, 668, 360, 0, 790, tn - .3, drop_=70, pan=150)
    els += [lab(1250, 616, "no new evidence", tn + .3, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 5: the weighing
ROWS = [250, 390, 530, 670]


def ledger_row(k, t, at, icon):
    y = ROWS[k]
    return [rect(130, y - 60, 1520, 120, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(330, y + 11, t, at + .1, BONE, 32, "start")] + icon(230, y, at)


def icon_secret(x, y, at):
    return [folder(x - 46, y - 26, 92, 62, at, MANILA, fx="pop"), stamp(x, y + 6, "SECRET", at + .1, STAMP, 14, -6)]


def icon_train(x, y, at):
    return [grp(train_icon(x, y - 50, 100, -1, None, 5), at, "pop")]


def icon_memory(x, y, at):
    return [grp([rect(x - 40, y - 34, 56, 44, "#f2ecdc", "#cbbca8", 1.2, 2), rect(x - 20, y - 20, 56, 44, "#e8e2d2", "#cbbca8", 1.2, 2),
                 rect(x - 2, y - 6, 56, 44, "#ddd6c4", "#cbbca8", 1.2, 2)], at, "pop")]


def icon_film(x, y, at):
    return [circ(x, y, 38, "#2a2622", "#cbbca8", 2, at, fx="pop"), circ(x, y, 10, "#cbbca8", at=at, fx="pop")] + \
           [circ(round(x + 22 * math.cos(a), 1), round(y + 22 * math.sin(a), 1), 7, "#5a5550", at=at, fx="pop") for a in [k * math.pi / 3 for k in range(6)]]


def sc_ledger():
    """s41: the ledger: four rows light as named, each with its chip: a secret hidden behind a weather balloon in 1947, Established; a Mogul balloon train,
    Strong evidence (gap: which flight); bodies as merged memories, Plausible; the autopsy film, Ruled out."""
    els = [rect(110, 150, 1560, 620, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .1)]
    els += [rect(130, y - 60, 1520, 120, "none", "rgba(242,201,142,.16)", 1.5, 12, .3, style="inferred") for y in ROWS]
    t1, e1 = T("ledger", "A secret"), T("ledger", "Established")
    t2, e2, g2 = T("ledger", "The debris"), T("ledger", "Strong evidence"), T("ledger", "which flight")
    t3, e3 = T("ledger", "The bodies"), T("ledger", "Plausible")
    t4, e4 = T("ledger", "The autopsy film"), T("ledger", "Ruled out")
    els += ledger_row(0, "a secret, hidden in 1947", t1, icon_secret) + chip(1220, ROWS[0], "Established", GRADE["established"], e1, 30, a="start")
    els += ledger_row(1, "a Mogul balloon train", t2, icon_train) + chip(1220, ROWS[1], "Strong evidence", GRADE["strong"], e2, 30, a="start")
    els += [lab(330, ROWS[1] + 46, "the gap: which flight", g2, MUTED, 24, "start")]
    els += ledger_row(2, "bodies as merged memories", t3, icon_memory) + chip(1220, ROWS[2], "Plausible", GRADE["plausible"], e3, 30, a="start")
    els += ledger_row(3, "the autopsy film as real", t4, icon_film) + chip(1220, ROWS[3], "Ruled out", GRADE["ruled"], e4, 30, a="start")
    return {"base": "dark", "cam": CAM, "els": els}


def doc_icons(x, y, at):
    """Four tiny pictures: rubber, foil, paper, sticks."""
    return [grp(rubber(x - 70, y, 36, -1, 1, 4) + foil(x - 6, y, .26, -1, None) + scrap(x + 36, y, .24, -1, None) + stick(x + 58, y - 12, x + 82, y + 10, -1, 3), at, "pop")]


def sc_craft():
    """s42: five records of July 1947 in a row (the 8 July paper, the FBI teletype, the 9 July interview, the Fort Worth photograph, the
    base history), each showing the same four things: rubber, foil, paper, sticks; an alien craft on the ranch, dotted, struck through:
    Ruled out. Then bodies or a second craft elsewhere, dotted, over three empty dashed trays: Awaiting evidence, 79 years."""
    te, tr_, ta, t80 = T("craft", "Every document"), T("craft", "Ruled"), T("craft", "Awaiting"), T("craft", "eighty years")
    els = [lab(889, 140, "the records of July 1947", .2, GOLD, 28)]
    xs = [240, 545, 850, 1155, 1460]
    for k, x in enumerate(xs):
        els += [rect(x - 120, 170, 240, 150, NEWS if k != 3 else "#d8d4cc", NEWS_D, 1.5, 3, .3 + .1 * k, fx="pop")]
        if k == 3:
            els += [rect(x - 104, 184, 208, 122, "#4a4744", at=.3 + .1 * k, fx="pop")]
        elif k == 1:
            els += typed(x - 100, 200, 140, 4, .4 + .1 * k, 22, seed=251 + k) + [grp(reflector(x + 80, 260, 22, -1, None, False), .4 + .1 * k, "pop")]
        else:
            els += typed(x - 100, 196, 200, 5, .4 + .1 * k, 22, seed=251 + k)
        els += doc_icons(x, 354, round(te + .25 * k, 2))
    els += saucer(470, 520, .75, tr_ - .8) + [I.strike(330, 580, 610, 460, tr_, RED, 7)]
    els += [lab(470, 616, "on the ranch", tr_ - .4, LILAC, 26)]
    els += chip(470, 690, "Ruled out", GRADE["ruled"], tr_ + .1, 30)
    els += saucer(1300, 470, .5, ta - .9) + [g for k in range(3) for g in ghost_person(1220 + 80 * k, 560, 60, ta - .7 + .1 * k, w=1.8)]
    for k in range(3):
        x = 1160 + 140 * k
        els += [rect(x, 580, 120, 70, "none", "#cbbca8", 2.4, 8, ta - .4 + .1 * k, fx="pop", style="inferred")]
    els += [lab(1065, 620, "elsewhere", ta - .5, LILAC, 26, "end")]
    els += chip(1300, 700, "Awaiting evidence", GRADE["awaiting"], ta + .1, 30)
    els += [lab(1300, 764, "79 years and counting", t80, MUTED, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_people():
    """s43: quiet silhouettes in warm light (a rancher, an officer, a press officer, a researcher); above them a stamp, TOP SECRET, with
    a gold tick: the secrecy was real. Then Karl Pflock steps forward: a former CIA officer; eight calendar squares fill: 8 years; a balloon train: Mogul."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(700, 420, 720, -1, .16)]
    sil = [(260, 250, True, "#7d766c"), (460, 262, False, "#6f7a55"), (660, 244, False, "#7d766c"), (860, 256, False, "#8a96a2")]
    for k, (x, h, hat, c) in enumerate(sil):
        els += figure(x, 760, h, .2 + .1 * k, c, "fade", op=.8, hat=hat)
    tc, tk, t8, tm = T("people", "secrecy"), T("people", "Karl"), T("people", "eight years"), T("people", "concluded")
    els += [stamp(560, 300, "TOP SECRET", tc, STAMP, 30, -5), tick(760, 300, tc + .6, GREEN, 1.4), lab(840, 312, "real", tc + .7, GREEN, 30, "start")]
    px = 1280
    els += [gl(px, 560, 300, tk - .3, .3), ppl(px, 760, 260, tk - .3, "#cbbca8", "rise")]
    els += [lab(px, 420, "Karl Pflock", tk, GOLD, 32), lab(px, 456, "former CIA officer", tk + .3, MUTED, 26)]
    for k in range(8):
        els += [rect(1110 + 44 * k, 250, 36, 36, "rgba(242,201,142,.7)", GOLD, 1.5, 4, round(t8 + .12 * k, 2), fx="pop")]
        els += [rect(1110 + 44 * k, 250, 36, 9, "#b8322a", at=round(t8 + .12 * k, 2), fx="pop")]
    els += [lab(1280, 226, "8 years", t8 + .4, GOLD, 28)]
    els += [grp(train_icon(1560, 230, 300, -1, None, 7), tm, "rise"), lab(1560, 580, "Mogul", tm + .3, GOLD, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_test():
    """s44: what would change our minds, three tests not yet done (dashed): a fragment in a sealed bag traced to 1947 and three
    independent labs; Roswell's lost messages and the copies at the offices that received them; Flight 4's own log."""
    tq, t1, t2, t3 = T("test", "change our minds"), T("test", "One fragment"), T("test", "Copies"), T("test", "Flight Four's")
    P = [(120, 620), (650, 1150), (1180, 1680)]
    els = [rect(a, 170, b - a - 20, 480, "none", BONE, 2.5, 14, .2 + .1 * k, fx="pop", style="inferred") for k, (a, b) in enumerate(P)]
    els += [lab(889, 140, "?", tq, LILAC, 44, st="serif")]
    a = P[0][0]
    els += [rect(a + 60, 230, 200, 150, "rgba(220,236,255,.12)", "#cfe6ff", 2, 12, t1 - .2, fx="pop"), ln([(a + 60, 256), (a + 260, 256)], t1 - .2, "#cfe6ff", 2, draw=False)]
    els += foil(a + 160, 320, .7, t1)
    els += [ln([(a + 260, 300), (a + 300, 300), (a + 300, 230)], t1 + .3, GOLD, 2, dur=.5), rect(a + 280, 196, 140, 40, PAPER, PAPER_D, 1.2, 4, t1 + .6, fx="pop"),
            ink(a + 350, 224, "1947", t1 + .6, TYPE, 24, weight=700)]
    for k in range(3):
        x = a + 90 + 140 * k
        els += building(x, 560, 90, round(t1 + 1.0 + .15 * k, 2), "block", "#cbbca8", "#2f2822", "pop")
        els += [{"k": "line", "p": R([(x - 16, 470), (x - 4, 482), (x + 20, 452)]), "c": GREEN, "w": 5, "style": "inferred", "in": round(t1 + 1.4 + .15 * k, 2)}]
    els += [lab((P[0][0] + P[0][1]) / 2 - 10, 700, "tested in the open", t1 + 1.2, BONE, 28)]
    a = P[1][0]
    els += [rect(a + 30, 300, 150, 90, "#2a241d", "#cbbca8", 2, 8, t2 - .3, fx="pop"), lab(a + 105, 354, "Roswell", t2 - .2, BONE, 24)]
    for k, (yy, nm) in enumerate(((240, "Fort Worth"), (450, "Wright Field"))):
        els += [arr([(a + 185, 345), (a + 300, yy + 40)], t2 + .2 * k, AMBER, 2.4, "inferred", .5),
                rect(a + 300, yy, 170, 90, "#2a241d", "#cbbca8", 2, 8, t2 + .3 + .2 * k, fx="pop"), lab(a + 385, yy + 52, nm, t2 + .3 + .2 * k, BONE, 24),
                rect(a + 330, yy + 100, 110, 30, "none", GOLD, 2, 4, t2 + .7 + .2 * k, style="inferred")]
    els += [lab((P[1][0] + P[1][1]) / 2 - 10, 700, "the copies", t2 + 1.0, BONE, 28)]
    a = P[2][0]
    els += [rect(a + 90, 210, 300, 400, PAPER, PAPER_D, 1.5, 3, t3 - .2, fx="pop"), ink(a + 240, 256, "Flight 4", t3 - .1, TYPE, 30, weight=700)]
    for k in range(6):
        y = 310 + 46 * k
        els += [ln([(a + 120, y), (a + 360, y)], t3 + .2 * k, "#8a7a66", 3, "inferred" if k > 1 else "known", .4)]
    els += [lab((P[2][0] + P[2][1]) / 2 - 10, 700, "which balloon", t3 + .8, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_close():
    """s45: the ranch at dusk, quiet: the windmill, the fence, grass where the debris lay; on one barb of the fence a short strip of tape
    with tiny pink flowers; far off, the lights of Roswell. The light fades a little."""
    els = [poly([(-20, 612), (60, 566), (300, 556), (350, 586), (520, 592), (570, 612)], "#2c2228", at=-1)]
    els += scrub(301, 16, 80, 1700, 640, 790, -1, s=.9) + windmill(420, 640, 300, -1, SIL)
    els += fence(1640, 812, 900, 628, 8, 140, 18, -1)
    els += [dot(1460 + 22 * k, 606 - (k % 2) * 3, 3, GOLD, -1, None) for k in range(9)] + [gl(1550, 604, 120, -1, .35)]
    tk, tf = T("close", "two kilos"), T("close", "most famous")
    els += tape_strip(1500, 712, 1560, 760, -1, 16, None, n=3) + [gl(1530, 736, 60, -1, .3)]
    els += [lab(1250, 760, "about 2 kg", tk, MUTED, 28)]
    els += [veil(-20, -20, 1820, 1040, tf + .6, "#0d0b09", .35, 3.0)]
    return {"base": "sky", "tod": "dusk", "ground": 612, "groundc": "url(#k-ground)", "sun": [700, 600, 20], "cam": [1.04, 889, 500], "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "hero", [(1, "The news came", "base"), (2, "By the next morning", "nextday"), (2, "For thirty years", "slept"), (3, "So what really", "night")], {}),
    (0, 1, "title", "night", [], {"intro": True}),
    (1, 0, "world", "nmmap", [(1, "Ten days later", "arnold"), (2, "On the fourth of July", "debris")], {"chapter": "A disc in the paper"}),
    (1, 1, "collision", "sheriff", [(1, "The base sent", "drive"), (1, "On the eighth of July", "release")], {}),
    (1, 2, "reversal", "ramey", [(1, "The next day, Brazel", "account")], {}),
    (1, 3, "tag", "history", [], {}),
    (2, 0, "world", "footnote", [(1, "In {1978", "friedman")], {"chapter": "Thirty years later"}),
    (2, 1, "collision", "marcel", [(1, "In {1980", "books"), (2, "With each book", "sites")], {}),
    (2, 2, "reversal", "haut", [(1, "Most of these accounts", "photo"), (2, "In {1947", "fields")], {}),
    (3, 0, "world", "schiff", [], {"chapter": "A secret in the sky"}),
    (3, 1, "collision", "channel", [(1, "So a team", "alamo"), (1, "Not one balloon", "train"), (2, "Hung on the line", "reflector")], {}),
    (3, 2, "reversal", "flight4", [(1, "Rubber from", "match"), (1, "And Marcel's strange", "writing")], {}),
    (3, 3, "tag", "gap", [], {}),
    (4, 0, "world", "agencies", [(1, "And the base's outgoing", "destroyed")], {"chapter": "Dummies, a film and lost files"}),
    (4, 1, "collision", "tv", [(0, "In {2006", "set")], {}),
    (4, 2, "reversal", "dummies", [(0, "Add an air crash", "accidents"), (1, "Its idea", "merge"), (2, "But to many", "answers")], {}),
    (4, 3, "tag", "aaro", [], {}),
    (5, 0, "weigh", "ledger", [], {"chapter": "The weighing"}),
    (5, 1, "weigh", "craft", [(1, "Nobody here", "people")], {}),
    (5, 2, "test", "test", [], {}),
    (5, 3, "close", "close", [], {}),
]

# alias shots: (the panel they return to, the camera on that panel, the function drawing their additions on arrival)
ALIASES = {
    "drive": ("nmmap", [3.6, 600, 516], "add_drive"),
    "accidents": ("dummies", [1.25, 1060, 540], "add_accidents"),
}


def _segments(script):
    """The narration each shot has on screen, from the beats with their markers (a chapter beat's first sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[@%s]" % sid)
        parts = re.split(r"\[@(\w+)\]", "\n".join(lines))
        head_ = parts[0]
        if kw.get("chapter"):
            ms = [m.start() for m in SENT.finditer(head_) if m.start() > 0]
            head_ = head_[ms[0]:] if ms else ""
        if role != "title":
            say[frm] = say[frm] + "\n" + head_ if frm in say else head_
        for k in range(1, len(parts), 2):
            say[parts[k]] = parts[k + 1]
    return say


def _stub(sid):
    return {"base": "dark", "cam": CAM, "els": [lab(889, 480, sid, .3, AMBER, 40)]}


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
                panels[sid] = g["sc_" + sid]() if "sc_" + sid in g else _stub(sid)
    ids = list(panels) + [a for a in ALIASES]
    idx = {s: i for i, s in enumerate(ids)}
    shots = [panels[s] for s in panels] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[idx[sid]] = idx[root]
        cams[idx[sid]] = [z] + list(cam[1:])
        tags[z] = g[fn]() if fn in g else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-roswell", "code": "LF.21", "series": script["series"], "title": script["title"], "case": "roswell-mogul",
          "verdict": "debunked", "claim": "Did an alien craft fall on the ranch near Roswell in 1947?", "mood": "mystery",
          "hook_text": "What really fell on that *ranch*?", "beats": beats, "shots": shots,
          "sources": "Roswell Daily Record, 8 and 9 July 1947 · FBI teletype, 8 July 1947 · GAO 1995 (GAO/NSIAD-95-187) · Weaver 1994 and "
                     "McAndrew 1995, The Roswell Report (US Air Force) · McAndrew 1997, Case Closed (US Air Force) · AARO 2024, Historical Record "
                     "Report Vol. I · Saler, Ziegler & Moore 1997 (Smithsonian) · Pflock 2001",
          "post": "On 8 July 1947 the army air field at Roswell said it had a flying disc; by evening it was a weather balloon. The rancher's "
                  "debris, thirty quiet years, the books, the secret Mogul balloon trains, the dummies, the destroyed records and the 2024 "
                  "review, document by document. Weighed.",
          "hashtags": ["#Roswell", "#UFO", "#ProjectMogul", "#ColdWar", "#History", "#WeighItYourself"],
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
