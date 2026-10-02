"""LF.19 · The Files · Stargate: The Pentagon's Psychic Spies (16:9 long film, one wall).

The script is films/long/lf-stargate/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s50; s5t, the title, is the intro card over the
panel of s5): Pat Price's crane drawn from coordinates in 1974 and the CIA's own drawing, the Cold War fear of Soviet psychic
research, the SRI lab of Russell Targ and Harold Puthoff, Ingo Swann and the CIA's first money, the Army unit at Fort Meade and its
code names, how a session worked, how the lab counted hits and why judging is hard (the clues Marks and Kammann found in the
transcripts, the uncanny matches to the wrong sites), the 1995 review for the CIA (Utts and Hyman on the lab, the users on the
operations), the 2017 release, and the weighing. Drawings are schematic and true to the numbers said: solid = on the record,
dashed = inferred or not yet done, dotted = claimed. The people are drawn as quiet figures, with respect.

Facts: the Short 'stargate-psychic' (f13.py, 13.03) and the script's facts_added (Kress 1977, Targ 1996, Puthoff & Targ 1976,
Targ & Puthoff 1974, Marks & Kammann 1978, Hyman 1996, Utts 1996, May 1996, the AIR report of 1995, the DIA report of 1972, the
CIA's press release of 2017).

Engine workaround (as in lf_mkultra.py and lf_voynich.py): the wall adds elements to a panel on its first visit, at a beat start
or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a
tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's
additions as a panel item (kit.js builds them on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-stargate/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-stargate/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-stargate RC_FILMS_EPS=/tmp/claude-0/sbx_lf-stargate/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-stargate/boards python3 films.py long.lf_stargate
"""
import json, math, os, random, re
from films import View, _topo
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-stargate", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN, INK = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN, I.INK
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
PAPER, PAPER_E, PAPER_D = "#efe6d2", "#fff6e2", "#cdbf9f"      # paper, its lit edge, its shade
MANILA, MANILA_E = "#cdb58a", "#8a6a48"                        # folders
CARD, CARD_S, CARD_T = "#9a7650", "#6e5236", "#b48e62"          # cardboard archive boxes: front, side, top
STAMP = "#b8322a"                                              # a rubber stamp's red, readable on paper
TYPE = "#3a3029"                                               # typewriter ink
STEEL, STEEL_D = "#5d6166", "#2c2f33"                          # warehouse shelving
FLOOR = "#17130f"
NIGHT = "#141019"                                              # flat backgrounds for panels with veils
GRADE = {"established": "#8fd9b0", "ruled": "#e98a8a", "awaiting": "#c9c1ee", "open": "#f0b06a"}
SKIN = "#cbbca8"


# ================================================================== narration: the script's own lines, and when each word is said
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")     # a sentence opens with [act:] (and its tags)
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


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


SAY, CLK, DUR = {}, {}, {}           # shot key -> its narration, its word clock, its estimated length (set in film())


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


# ---------------------------------------------------------------- paper, files, boxes
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


# ---------------------------------------------------------------- people, heads, rooms
HEAD = [(.0, -.5), (.18, -.47), (.32, -.36), (.38, -.2), (.4, -.08), (.5, .05), (.42, .1), (.41, .18), (.46, .24), (.4, .29), (.38, .38), (.28, .44),
        (.18, .47), (.16, .62), (.2, .78), (-.3, .78), (-.22, .55), (-.36, .4), (-.44, .18), (-.44, -.12), (-.34, -.38), (-.18, -.48)]


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


# ---------------------------------------------------------------- buildings
def uni(x, y, s, at, c="#cbbca8", fill="#3a3129", fx="pop", op=None):
    """A university: columns under a pediment, base on y, s = width."""
    h = s * .62
    els = [rect(x - s / 2, y - h, s, h, fill, c, 2, 2, at, fx=fx, op=op),
           poly([[x - s * .58, y - h], [x, y - h - s * .3], [x + s * .58, y - h]], fill, c, 2, at, fx=fx, op=op)]
    els += [rect(x - s * .38 + s * .19 * k - s * .04, y - h * .86, s * .08, h * .86, c, at=at, fx=fx, op=op) for k in range(5)]
    return els


# ================================================================== palette and small additions for this film
GRAPH, GRAPH_L = "#3b3530", "rgba(59,53,48,.32)"               # graphite on paper, and its faint second stroke
PLAN_BG, PLAN_L = "#16263d", "#cfe6ff"                          # the CIA's drawing: a dark blue sheet, light lines
DESK, DESK_E = "#21180f", "#3a2b1d"                             # a desk top at night
OLIVE = "#6f7a55"                                               # army fatigues
FLAT = "#15110d"                                                # flat panel background (for veils)
SOV = "#d65a4a"                                                 # the Soviet side (a muted red)


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


# ---------------------------------------------------------------- the crane: Pat Price's sketch, and the CIA's drawing from satellite photographs
# local units: rails at y = 0, the girder 1080 long and 485 high; four wheels under each leg (eight in all)
CR_BOGIE = 280
CR_WHEELS = [-99, -33, 33, 99]
CR_R, CR_AXLE = 28, -30


def crane(cx, ry, s, at=-1, kind="sketch", w=None, draw=False, col=None):
    """The gantry crane, side view, rails at ry, centred on cx, scale s. kind 'sketch' (graphite, doubled strokes, a little hatching:
    Price's drawing, which agrees with the CIA's in its main features, a gantry on rails with eight wheels, not in every detail)
    or 'plan' (clean light lines and pale fills: the CIA's drawing from satellite photographs). Returns (elements, wheel centres)."""
    P = lambda x, y: (round(cx + x * s, 1), round(ry + y * s, 1))
    sk = kind == "sketch"
    c = GRAPH if sk else (col or PLAN_L)
    w = w or (max(1.6, 3.4 * s / .78) if sk else max(1.3, 2.4 * s / .78))
    fillc = "rgba(59,53,48,.10)" if sk else "rgba(207,230,255,.10)"
    # the hand drawing: a shorter, slimmer girder, straighter legs, the cab on the other side, the trolley off centre
    gx, gt, gb = (500, -452, -400) if sk else (540, -462, -400)
    top = 56 if sk else 45
    cab = (158, 228) if sk else (-228, -158)
    tro = -90 if sk else 0
    els, wheels = [], []

    def L(pts, ww=None, op=None, dur=None):
        q = [P(x, y) for x, y in pts]
        if sk:
            return sketchy(q, at, c, ww or w, op=op, draw=draw, dur=dur)
        return [ln(q, at, c, ww or w, draw=draw, dur=dur, op=op)]

    def R_(x0, y0, x1, y1, f=None, ww=None):
        q = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
        out = [poly(q, f or fillc, "none", 0, at)]
        return out + L([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], ww)

    # rails, sleepers
    els += L([(-600, 0), (600, 0)], w * 1.2) + L([(-600, 9), (600, 9)], w * .6, op=.8)
    for k in range(-11, 12):
        els += [ln([P(k * 52, 9), P(k * 52 - 8, 22)], at, c, max(1.0, w * .5), draw=False, op=.55)]
    for sg in (-1, 1):
        bx = sg * CR_BOGIE
        # bogie beam and its four wheels
        els += R_(bx - 132, -84, bx + 132, -60, ww=w)
        for d in CR_WHEELS:
            x, y = P(bx + d, CR_AXLE)
            r = round(CR_R * s, 1)
            els.append(circ(x, y, r, "rgba(59,53,48,.08)" if sk else "rgba(207,230,255,.08)", c, w, at))
            els.append(circ(x, y, max(2.0, r * .22), c, at=at))
            if sk:
                els.append(circ(round(x + 1.5, 1), round(y + 1, 1), r, "none", GRAPH_L, max(1.0, w * .5), at))
            wheels.append((x, y, r))
        # the leg: two posts narrowing to the girder, braced in a zigzag
        lp = lambda h: bx - 110 + (110 - top) * ((h + 84) / -316)
        rp = lambda h: bx + 110 - (110 - top) * ((h + 84) / -316)
        els += L([(bx - 110, -84), (bx - top, -400)]) + L([(bx + 110, -84), (bx + top, -400)])
        zz, hs = [], ([-84, -168, -252, -336, -400] if sk else [-84, -147, -210, -273, -336, -400])
        for k, h in enumerate(hs):
            zz.append((lp(h) if k % 2 == 0 else rp(h), h))
        els += L(zz, w * .7)
        for h in hs[1:-1]:
            els += L([(lp(h), h), (rp(h), h)], w * .45, op=.7)
    # the girder: two chords, end posts, diagonals
    els += R_(-gx, gt, gx, gb, f="rgba(59,53,48,.06)" if sk else "rgba(207,230,255,.06)")
    nseg = int(2 * gx / 60)
    zz = [(-gx + 2 * gx * k / nseg, gb if k % 2 == 0 else gt) for k in range(nseg + 1)]
    els += L(zz, w * .6)
    # trolley, cable, hook block, hook
    els += R_(tro - 55, gt - 30, tro + 55, gt)
    els += [circ(*P(tro - 35, gt), max(2.0, 8 * s), "none", c, max(1.0, w * .6), at), circ(*P(tro + 35, gt), max(2.0, 8 * s), "none", c, max(1.0, w * .6), at)]
    hb = -212 if sk else -238
    els += L([(tro - 6, gb), (tro - 6, hb)], w * .5) + L([(tro + 6, gb), (tro + 6, hb)], w * .5)
    els += R_(tro - 18, hb, tro + 18, hb + 32)
    els += L([(tro, hb + 32), (tro, hb + 50), (tro - 10, hb + 62), (tro - 2, hb + 74), (tro + 10, hb + 66)], w * .7)
    # the operator's cab under the girder
    els += R_(cab[0], gb, cab[1], gb + 60)
    els += R_(cab[0] + 10, gb + 10, cab[1] - 10, gb + 34, f="rgba(242,201,142,.18)" if not sk else "rgba(59,53,48,.05)", ww=w * .6)
    if sk:      # a little pencil hatching on the cab and the bogie beams
        for k in range(5):
            els += [ln([P(cab[0] + 2 + 14 * k, gb + 58), P(cab[0] + 16 + 14 * k, gb + 44)], at, GRAPH, max(1.0, w * .4), draw=False, op=.55)]
        for sg in (-1, 1):
            for k in range(9):
                x0 = sg * CR_BOGIE - 126 + 30 * k
                els += [ln([P(x0, -62), P(x0 + 14, -82)], at, GRAPH, max(1.0, w * .4), draw=False, op=.5)]
    return els, wheels


def crane_person(cx, ry, s, at, c=LILAC):
    """A person beside the left wheels, the top of the head level with the axles (his words: a claim, in lilac)."""
    x = cx + (-CR_BOGIE - 132 - 34) * s
    h = -CR_AXLE * s
    return [ppl(x, ry, h, at, c, fx="pop")]


# ---------------------------------------------------------------- the globe (orthographic)
def ortho(lat0, lon0, cx, cy, R):
    la0, lo0 = math.radians(lat0), math.radians(lon0)

    def P(lon, lat):
        la, lo = math.radians(lat), math.radians(lon)
        cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo - lo0)
        x = R * math.cos(la) * math.sin(lo - lo0)
        y = R * (math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo - lo0))
        return cx + x, cy - y, cosc
    return P


def globe_land(P, cx, cy, R, step=2):
    out = []
    for poly_ in _topo():
        r = poly_[0]
        pts, vis = [], False
        for lo, la in r[::step]:
            x, y, cc = P(lo, la)
            if cc < 0:
                d = math.hypot(x - cx, y - cy) or 1
                x, y = cx + (x - cx) / d * R, cy + (y - cy) / d * R
            else:
                vis = True
            pts.append((round(x, 1), round(y, 1)))
        if vis and len(pts) > 4:
            q = [pts[0]]
            for p in pts[1:]:
                if abs(p[0] - q[-1][0]) + abs(p[1] - q[-1][1]) > 1.6:
                    q.append(p)
            if len(q) > 6:
                out.append("M" + "L".join(f"{x} {y}" for x, y in q) + "Z")
    return out


def gc_points(a, b, n=40):
    """Points along the great circle from a = (lon, lat) to b."""
    def v(lon, lat):
        la, lo = math.radians(lat), math.radians(lon)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
    A, Bv = v(*a), v(*b)
    om = math.acos(max(-1, min(1, sum(p * q for p, q in zip(A, Bv)))))
    out = []
    for k in range(n + 1):
        t = k / n
        s1, s2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
        x, y, z = (s1 * A[i] + s2 * Bv[i] for i in range(3))
        out.append((math.degrees(math.atan2(y, x)), math.degrees(math.asin(z))))
    return out


def globe(P, cx, cy, R, at=-1, lat_lines=(0, 30, 60), lon_step=30):
    """An ocean disc, a faint graticule (front half only), the land, and a thin lit rim."""
    els = [gl(cx, cy, R * 1.25, at, .18, "scan"), circ(cx, cy, R, "#0b1520", "none", 0, at)]
    for la in lat_lines:
        seg = []
        for lo in range(-180, 181, 4):
            x, y, cc = P(lo, la)
            if cc > 0:
                seg.append((x, y))
            elif seg:
                if len(seg) > 1:
                    els.append(ln(seg, at, "#6f8fa8", 1.2, draw=False, op=.35))
                seg = []
        if len(seg) > 1:
            els.append(ln(seg, at, "#6f8fa8", 1.2, draw=False, op=.35))
    for lo in range(-180, 180, lon_step):
        seg = []
        for la in range(-88, 89, 4):
            x, y, cc = P(lo, la)
            if cc > 0:
                seg.append((x, y))
            elif seg:
                if len(seg) > 1:
                    els.append(ln(seg, at, "#6f8fa8", 1.2, draw=False, op=.35))
                seg = []
        if len(seg) > 1:
            els.append(ln(seg, at, "#6f8fa8", 1.2, draw=False, op=.35))
    els.append({"k": "map", "land": globe_land(P, cx, cy, R, 3), "landc": "#66543c", "in": at})
    els.append(circ(cx, cy, R, "none", "rgba(159,208,255,.45)", 2.4, at))
    return els


# ---------------------------------------------------------------- figures and objects used across the film
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


def head_icon(x, y, s, at, face=1, fill="#2a2420", rim="rgba(255,236,206,.45)", fx=None, op=None):
    return [head(x, y, s, at, fill, rim, 2, fx=fx, op=op, face=face)]


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


def seated_figure(x, y, h, at, c="#9a9288", face=1, fx="rise", op=None, stool=True):
    return seated(x, y, h, at, c, stool=stool, face=face, fx=fx, op=op)


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


def barracks(x, y, w, h, at, lit=(1,), fx=None, op=None):
    """A long low wooden barracks: plank walls, a shallow roof, a row of windows."""
    els = [poly([(x - 16, y - h), (x + w / 2, y - h - h * .45), (x + w + 16, y - h)], "#3b2e22", "#8a6a48", 2, at, fx=fx, op=op),
           rect(x, y - h, w, h, "#4a3a2a", "#8a6a48", 2, 2, at, fx=fx, op=op)]
    for k in range(1, 7):
        els.append(ln([(x + 4, y - h + h * k / 7), (x + w - 4, y - h + h * k / 7)], at, "#3a2c20", 1.4, draw=False, op=.8 if op is None else op))
    nwin = max(3, int(w / 90))
    for k in range(nwin):
        wx = x + w * (k + .5) / nwin - 18
        els.append(rect(wx, y - h * .7, 36, h * .34, GOLD if k in lit else "#1a140f", "#8a6a48", 1.5, 2, at, fx=fx, op=op))
    return els


def tree(x, y, h, at, c="#1c1812", op=None):
    return [poly([(x - h * .22, y - h * .25), (x, y - h), (x + h * .22, y - h * .25)], c, at=at, op=op),
            poly([(x - h * .28, y - h * .02), (x, y - h * .62), (x + h * .28, y - h * .02)], c, at=at, op=op),
            rect(x - h * .03, y - h * .05, h * .06, h * .07, c, at=at, op=op)]


def star5(x, y, r, at, c=SOV, fx="pop"):
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        rr = r if k % 2 == 0 else r * .42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return poly(pts, c, at=at, fx=fx)


def card(x, y, w, h, at, c="#2a241d", e="#6a5a48", fx="pop", style="known", op=None, r=8):
    return rect(x, y, w, h, c, e, 2, r, at, fx=fx, style=style, op=op)


def bar(x0, x1, y, h, at, c=AMBER, dur=1.0, op=None):
    """A bar growing left to right (a thick line that draws itself)."""
    return ln([(x0, y), (x1, y)], at, c, h, dur=dur, op=op)


# ================================================================== cold open: a crane drawn from coordinates
HX, HY, HS = 1010, 640, .74            # the hero sketch: centre, rails, scale
SHEET = (468, 150, 1084, 562)          # the sheet on the desk (x, y, w, h)


def sc_hero():
    """s1, the hero image, fully drawn from the first frame: a desk at night, a lamp, a sheet with a graphite gantry crane (eight
    wheels), a pencil, a man's dim silhouette at the left. Labels build after the hook title: 'summer 1974', 'California'."""
    x, y, w, h = SHEET
    els = desk_bg()
    els += [ln([(-20, 70), (1800, 40)], -1, DESK_E, 2, draw=False, op=.5)]
    # the lamp's pool of light on the sheet
    els += [gl(1060, 430, 760, -1, .32), poly([(1530, -20), (1640, -20), (1590, 860), (380, 900)], "rgba(255,214,150,.035)", at=-1)]
    # a second sheet beneath, the sheet, its shadow
    els += [rect(x - 26, y + 22, w, h, "#d8ccb2", "#b9a98a", 1.2, 3, -1), rect(x + 14, y + 18, w, h, "rgba(0,0,0,.5)", at=-1),
            rect(x, y, w, h, "#efe6d2", "#fff6e2", 1.5, 3, -1)]
    els += [rect(x + 6, y + 6, w - 12, h - 12, "none", "rgba(160,140,110,.25)", 1, 2, -1)]
    cr, _ = crane(HX, HY, HS)
    els += cr
    # a few faint construction marks and a scribbled note in the corner
    els += [ln([(x + 60, y + 70), (x + 210, y + 70)], -1, GRAPH, 2, draw=False, op=.35), ln([(x + 60, y + 96), (x + 160, y + 96)], -1, GRAPH, 2, draw=False, op=.3)]
    # the pencil across the lower right corner
    px0, py0, px1, py1 = 1360, 790, 1660, 690
    els += [poly([(px0, py0), (px1, py1), (px1 + 8, py1 + 22), (px0 + 8, py0 + 22)], "#d9a63a", "#8a6420", 1.5, -1),
            poly([(px0, py0), (px0 + 8, py0 + 22), (px0 - 34, py0 + 22)], "#e8c99a", "#8a6420", 1, -1),
            poly([(px0 - 24, py0 + 18), (px0 - 34, py0 + 22), (px0 - 22, py0 + 23)], GRAPH, at=-1),
            poly([(px1, py1), (px1 + 30, py1 - 10), (px1 + 38, py1 + 12), (px1 + 8, py1 + 22)], "#c06a5a", "#7a3a30", 1, -1)]
    # the man, in shadow at the left, leaning over the desk
    els += [poly([(-20, 1000), (-20, 560), (60, 470), (200, 430), (310, 470), (380, 600), (420, 1000)], "#0e0b08", "rgba(255,226,180,.10)", 2, -1, curve=True),
            head(250, 330, 250, -1, "#0e0b08", "rgba(255,214,150,.28)", 2.5, face=1)]
    els += [lab(150, 742, "summer 1974", T("hero", "Summer", lead=.1), GOLD, 30, "start", st="cap"),
            lab(150, 784, "California", T("hero", "California"), BONE, 30, "start"),
            lab(x + w / 2, y + h + 50, "a viewer's sketch, schematic", T("hero", "draws") + .4, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_axles():
    """s3: close on the sketch's left wheels: a card 'coordinates only' slides in; a tiny figure, the top of its head level with the
    axles (his words, lilac), ringed so it can be found."""
    tc, ta = T("axles", "coordinates"), T("axles", "axles")
    cx0, cy0, cw, ch = 432, 392, 176, 112
    els = [rect(cx0 + 8, cy0 + 10, cw, ch, "rgba(0,0,0,.4)", at=tc - .5, fx="rise"), rect(cx0, cy0, cw, ch, "#1b2230", "#8fb6d6", 2, 8, tc - .5, fx="rise")]
    for k in range(1, 5):
        els.append(ln([(cx0 + cw * k / 5, cy0 + 8), (cx0 + cw * k / 5, cy0 + ch - 8)], tc - .4, "#6f8fa8", 1.2, draw=False, op=.6))
    for k in range(1, 4):
        els.append(ln([(cx0 + 8, cy0 + ch * k / 4), (cx0 + cw - 8, cy0 + ch * k / 4)], tc - .4, "#6f8fa8", 1.2, draw=False, op=.6))
    mx, my = cx0 + cw / 2, cy0 + ch / 2
    els += [circ(mx, my, 16, "none", GOLD, 2.5, tc), ln([(mx, my - 26), (mx, my + 26)], tc, GOLD, 2, draw=False), ln([(mx - 26, my), (mx + 26, my)], tc, GOLD, 2, draw=False),
            note(mx, cy0 + ch + 30, "coordinates only", tc + .2, TYPE, 28)]
    px = HX + (-CR_BOGIE - 132 - 34) * HS
    hy = HY + CR_AXLE * HS
    els += [gl(px, hy + 10, 46, ta - .7, .55, "scan"), circ(px, hy + 11, 24, "none", LILAC, 2.5, ta - .7, style="claimed")]
    els += crane_person(HX, HY, HS, ta - .6)
    els += [ln([(px - 6, hy), (px + 96, hy)], ta - .2, LILAC, 2, "claimed", .5)]
    els += [ln([(px - 2, hy + 26), (600, 664)], ta - .1, LILAC, 1.6, "claimed", .4),
            note(560, 686, "only up to the axles", ta, "#4b3d8f", 28), note(560, 710, "his words", ta + .3, "#6a5a48", 24)]
    return els


GLOBE = (700, 470, 318)
GP = ortho(68, 160, *GLOBE)
SRI_LL, SEMI_LL = (-122.17, 37.46), (78.4, 50.1)


def sc_globe():
    """s2: a night globe; California and the Soviet test site pinned; a dotted trail along the great circle between them,
    'about 10,000 km'. (s5 returns to it, wider: a head, a question mark, 23 years.)"""
    cx, cy, R = GLOBE
    els = globe(GP, cx, cy, R)
    sx, sy, _ = GP(*SRI_LL)
    tx, ty, _ = GP(*SEMI_LL)
    els += [gl(tx, ty, 160, -1, .28, "red")]
    ts, tt, td = T("globe", "stands"), T("globe", "secret Soviet"), T("globe", "ten thousand")
    els += [{"k": "pin", "x": round(sx, 1), "y": round(sy, 1), "t": "California", "c": GOLD, "in": ts},
            {"k": "pin", "x": round(tx, 1), "y": round(ty, 1), "t": "secret Soviet site", "t2": "Semipalatinsk", "c": SOV, "a": "end", "lx": -18, "in": tt}]
    path = [GP(lo, la) for lo, la in gc_points(SRI_LL, SEMI_LL, 44)]
    lift = [(x + (x - cx) * .06 * math.sin(math.pi * k / 44), y + (y - cy) * .06 * math.sin(math.pi * k / 44)) for k, (x, y, _) in enumerate(path)]
    els += dots_along(lift, td - .9, 1.3, LILAC, 4)
    mx, my = min(lift, key=lambda q: q[1])
    els.append(lab(mx, my - 56, "about 10,000 km", td + .3, LILAC, 32))
    return {"base": "dark", "stars": 90, "cam": [1.28, 700, 470], "els": els}


def add_mind():
    """s5: wider on the globe: a head in profile at the right, looking at it; a dotted line from the head over the globe; a question
    mark; a gold band 1972 to 1995, '23 years'."""
    tq, ty = T("mind", "Can a mind"), T("mind", "twenty-three")
    els = [gl(1440, 600, 280, tq - .6, .16), head(1460, 660, 330, tq - .6, "#120e0b", "rgba(255,214,150,.45)", 3, fx="rise", face=-1)]
    arc = [(1350, 560), (1260, 450), (1140, 380), (1010, 360), (905, 380)]
    pts = []
    for k in range(len(arc) - 1):
        for j in range(8):
            t = j / 8
            pts.append((arc[k][0] + (arc[k + 1][0] - arc[k][0]) * t, arc[k][1] + (arc[k + 1][1] - arc[k][1]) * t))
    els += dots_along(pts, tq, 1.0, LILAC, 4)
    els += qmark(1150, 310, tq + 1.2, 100)
    els += [bar(1010, 1640, 168, 12, ty, GOLD, 1.4), lab(1010, 142, "1972", ty, BONE, 26, "start"), lab(1640, 142, "1995", ty + 1.2, BONE, 26, "end"),
            lab(1325, 214, "23 years", ty + .8, GOLD, 32)]
    return els


def sc_compare():
    """s4: his sketch beside the CIA's drawing from satellite photographs; the wheels light up one by one on both (eight each);
    two analysts tick it: accurate."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(889, 420, 900, -1, .12)]
    L = (130, 150, 700, 470)
    Rr = (948, 150, 700, 470)
    els += [rect(L[0] + 12, L[1] + 14, L[2], L[3], "rgba(0,0,0,.5)", at=-1), rect(*L, "#efe6d2", "#fff6e2", 1.5, 3, -1)]
    a, wl = crane(L[0] + L[2] / 2, L[1] + L[3] - 70, .5)
    els += a
    tc = T("compare", "its own")
    els += [rect(Rr[0] + 12, Rr[1] + 14, Rr[2], Rr[3], "rgba(0,0,0,.5)", at=tc - .4, fx="rise"), rect(*Rr, PLAN_BG, "#5d7ea6", 2, 3, tc - .4, fx="rise")]
    for k in range(1, 9):
        els.append(ln([(Rr[0] + Rr[2] * k / 9, Rr[1] + 6), (Rr[0] + Rr[2] * k / 9, Rr[1] + Rr[3] - 6)], tc - .3, "#28406a", 1, draw=False, op=.7))
    b, wr = crane(Rr[0] + Rr[2] / 2, Rr[1] + Rr[3] - 70, .5, tc, "plan", draw=True)
    els += b
    els += [lab(L[0] + L[2] / 2, 668, "his sketch", .4, BONE, 28), lab(Rr[0] + Rr[2] / 2, 668, "CIA drawing, from satellite photos", tc + .2, BLUE, 28)]
    tw = T("compare", "Two analysts") - 1.6
    order = sorted(range(8), key=lambda i: wl[i][0])
    for n, i in enumerate(order):
        for (x, y, r) in (wl[i], wr[i]):
            els.append(circ(x, y, r + 5, "none", AU, 3.5, round(tw + .16 * n, 2), fx="pop"))
    els.append(lab(889, 722, "both: eight wheels", tw + 1.4, AU, 30))
    ta = T("compare", "agree")
    for k, x in enumerate((850, 928)):
        els += [ppl(x, 640, 96, ta - .5 + .15 * k, "#a9b8c6"), tick(x, 520, ta + .1 + .15 * k, GREEN, 1.1)]
    els.append(lab(889, 770, "two analysts: accurate", ta + .5, GREEN, 28))
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 1: the psychic arms race
USSR_V = View(22, 178, 36, 78, (840, 170, 820, 520))


def sc_report():
    """s6: a desk at night; the 1972 report pops in ('Controlled Offensive Behavior, USSR', 'July 1972', 'for the DIA'); behind it
    on the right a dim map of the Soviet lands; two pictures rise as named: telepathy, mind over matter."""
    els = desk_bg()
    els += inset_map(USSR_V, 830, 160, 840, 540, -1, "#3a2622", "#151b22") + [gl(1250, 400, 420, -1, .3, "red")]
    lines = [("CONTROLLED OFFENSIVE", 118, 30, 700), ("BEHAVIOR  USSR", 160, 30, 700), ("July 1972", 236, 26, None), ("for the DIA", 540, 26, None)]
    els += report_cover(210, 190, 480, 590, .3, lines, body=4, seed=11)
    tt, tp = T("report", "telepathy"), T("report", "moving objects")
    # telepathy: two heads face to face, dotted waves between them
    els += [rect(890, 210, 340, 220, "rgba(18,13,10,.82)", "rgba(201,193,238,.5)", 2, 12, tt - .4, fx="pop")]
    els += head_icon(975, 318, 150, tt - .3, 1, "#2e2833", "rgba(201,193,238,.6)") + head_icon(1145, 318, 150, tt - .3, -1, "#2e2833", "rgba(201,193,238,.6)")
    els += waves(1015, 300, 1105, 300, tt + .1)
    els.append(lab(1060, 470, "telepathy", tt + .2, LILAC, 30))
    # mind over matter: a head watching a cup slide along dotted lines
    els += [rect(1270, 430, 360, 230, "rgba(18,13,10,.82)", "rgba(201,193,238,.5)", 2, 12, tp - .4, fx="pop")]
    els += head_icon(1330, 545, 150, tp - .3, 1, "#2e2833", "rgba(201,193,238,.6)")
    els += [rect(1500, 560, 54, 56, "#cbbca8", "#f5ecdc", 1.5, 4, tp), ln([(1554, 572), (1572, 582), (1554, 598)], tp, "#cbbca8", 4, draw=False, curve=True),
            ln([(1400, 616), (1600, 616)], tp, "#8a7a66", 2, draw=False)]
    els += [ln([(1440, 578 + 14 * k), (1490, 578 + 14 * k)], tp + .3 + .1 * k, LILAC, 2.5, "claimed", draw=False) for k in range(3)]
    els.append(lab(1450, 700, "mind over matter", tp + .2, LILAC, 30))
    return {"base": "dark", "cam": CAM, "els": els}


def sc_balance():
    """s7: a balance tipping towards the USSR; the report's claim, dotted: 'superior?'."""
    t0 = .2
    left = lambda x, y, at: [star5(x, y - 52, 30, at), lab(x, y + 52, "USSR", at + .1, SOV, 34)]
    right = lambda x, y, at: [star5(x, y - 52, 28, at, "#e9dccb"), lab(x, y + 52, "USA", at + .1, BONE, 34)]
    els = [gl(889, 420, 520, -1, .14)] + static(balance(889, 300, 760, -11, 700, t0, left, right, drop_=200, pan=220))
    ts = T("balance", "superior")
    lx = 889 - 380 * math.cos(math.radians(11))
    els += [lab(lx, 236, "superior?", ts, SOV, 36, st="serif"), lab(lx, 272, "the report's claim", ts + .3, MUTED, 24)]
    els += report_cover(150, 300, 220, 280, -1, [], body=3, seed=12) + [ln([(180, 340 + 22 * j), (340 - 30 * (j == 2), 340 + 22 * j)], -1, TYPE, 5, draw=False) for j in range(3)]
    els += [lab(260, 630, "July 1972", -1, MUTED, 26)]
    els += dots_along([(390 + 14 * k, 420 - 150 * math.sin(math.pi * k / 26) + 2.2 * k) for k in range(19)], ts - .8, .8, SOV, 3.5)
    return {"base": "dark", "cam": CAM, "els": els}


BAY = View(-122.75, -121.75, 37.15, 38.05, (130, 175, 560, 450))


def sc_sri():
    """s8: a small map of the Bay with SRI at Menlo Park; a lab bench with a laser beam drawing itself, two figures: Targ, Puthoff."""
    els = inset_map(BAY, 110, 150, 600, 500)
    sx, sy = BAY.p(-122.1739, 37.4566)
    els.append({"k": "pin", "x": sx, "y": sy, "t": "Stanford Research", "t2": "Institute, 1972", "c": GOLD, "a": "end", "lx": -18, "in": T("sri", "Stanford")})
    tl = T("sri", "laser")
    # two physicists behind the bench, the laser and its beam
    els += [gl(1220, 480, 560, -1, .18)]
    els += [rect(930, 600, 580, 24, "#4a3f36", "#8a7a66", 2, 3, -1), rect(950, 624, 540, 120, "#2c241e", "#5a4a3c", 2, 3, -1),
            rect(960, 542, 150, 58, "#3a4048", "#9aa4ae", 2, 4, -1), circ(1110, 570, 6, "#ff6a5a", at=-1),
            rect(1340, 530, 14, 70, "#9aa4ae", at=-1), rect(1460, 530, 14, 70, "#9aa4ae", at=-1)]
    els += [ppl(840, 744, 330, T("sri", "Russell") - .2, "#a39a8e"), ppl(1600, 744, 330, T("sri", "Harold") - .2, "#a39a8e")]
    els += [ln([(1116, 570), (1346, 570)], tl, "#ff5a4a", 4, dur=.7), gl(1346, 570, 50, tl + .6, .8, "red"),
            ln([(1346, 570), (1466, 548)], tl + .7, "#ff5a4a", 3, dur=.4)]
    els += [lab(840, 382, "Russell Targ", T("sri", "Russell"), BONE, 30), lab(1600, 382, "Harold Puthoff", T("sri", "Harold"), BONE, 30),
            lab(1220, 790, "laser physicists", tl + .3, AMBER, 28)]
    bx, by = BAY.p(-122.2, 37.62)
    els += [lab(bx + 10, by, "the Bay", -1, "#8fb6d6", 24, st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_swann():
    """s9: Swann at his easel (an artist); a shielded magnetometer and a chart recorder whose trace doubles its wiggle; two dashed
    cards: accounts differ. June 1972."""
    els = [gl(380, 460, 360, -1, .14)]
    # the easel and canvas
    els += [ln([(470, 760), (540, 300)], -1, "#8a6a48", 6, draw=False), ln([(640, 760), (560, 300)], -1, "#8a6a48", 6, draw=False), ln([(550, 300), (556, 760)], -1, "#6a5038", 5, draw=False),
            rect(440, 330, 230, 190, "#e8dcc4", "#8a6a48", 3, 2, -1), rect(452, 342, 206, 166, "#203040", at=-1)]
    els += [ln([(470, 470), (520, 400), (580, 430), (640, 360)], -1, "#e8b87a", 6, draw=False, curve=True), circ(600, 390, 24, "#f2c98e", at=-1, op=.85),
            ln([(470, 492), (650, 480)], -1, "#8fd9b0", 5, draw=False)]
    els += [ppl(330, 760, 250, -1, "#a39a8e")]
    ti = T("swann", "Ingo")
    els += [lab(400, 220, "Ingo Swann", ti, BONE, 32), lab(400, 258, "artist, New York", ti + .4, MUTED, 26)]
    tm, tt = T("swann", "magnetometer"), T("swann", "trace")
    # the magnetometer in the floor, wires, the chart recorder
    els += [ln([(800, 640), (1160, 640)], tm - .6, "#8a7a66", 2, "inferred", draw=False),
            rect(900, 420, 140, 220, "#5d6166", "#c9d0d6", 2, 6, tm - .5, fx="rise"), rect(900, 640, 140, 120, "#3a3d40", "#7a8086", 2, 6, tm - .5, op=.6),
            poly(E(970, 420, 70, 16, 24), "#7a8086", "#c9d0d6", 2, tm - .5), lab(970, 360, "magnetometer", tm, BONE, 28)]
    els += [ln([(1040, 470), (1120, 470), (1120, 430), (1220, 430)], tm + .2, "#9aa4ae", 2, dur=.5),
            rect(1220, 330, 400, 230, "#2a2f35", "#9aa4ae", 2, 8, tm + .2, fx="pop"), rect(1240, 350, 360, 150, "#efe6d2", at=tm + .3)]
    pts = []
    for k in range(91):
        x = 1250 + k * 3.8
        f = .45 if (k < 36 or k > 62) else .9
        ph = sum(.45 if (j < 36 or j > 62) else .9 for j in range(k))
        pts.append((x, 425 + 24 * math.sin(ph)))
    els += [ln(pts, tt - .4, "#b0301e", 2.5, dur=2.2)]
    els += [lab(1420, 300, "June 1972", tm + .4, MUTED, 26)]
    td = T("swann", "accounts")
    els += [card(1250, 600, 170, 100, td - .3, style="inferred"), card(1440, 600, 170, 100, td - .1, style="inferred"),
            lab(1335, 664, "?", td, MUTED, 44, st="serif"), lab(1525, 664, "?", td + .2, MUTED, 44, st="serif"), lab(1430, 750, "accounts differ", td + .4, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_hidden():
    """s10: a table and a tall screen; two CIA visitors and a box of hidden objects behind it; Swann on the near side, dotted lines
    towards the box; August 1972; a typed card 'the subject did well'."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(889, 430, 760, -1, .16)]
    tv, th = T("hidden", "CIA visitors"), T("hidden", "hid objects")
    els += [ppl(1170, 600, 250, tv, "#8a96a2"), ppl(1300, 600, 240, tv + .2, "#8a96a2"), lab(1235, 300, "CIA visitors", tv + .2, BLUE, 28)]
    els += table(889, 560, 900, -1)
    els += seated_figure(600, 640, 250, -1, "#a39a8e", 1)
    els += [rect(866, 250, 46, 312, "#3a3129", "#8a6a48", 2, 4, -1), lab(600, 316, "Swann", .4, BONE, 28)]
    els += abox(1010, 500, 120, 60, th, fx="pop", d=12, lab_=False)
    els += [circ(1035, 486, 10, "#cbbca8", at=th + .2), rect(1060, 474, 18, 26, "#8fd9b0", at=th + .3), rect(1092, 480, 22, 16, AMBER, at=th + .4)]
    els += [lab(1070, 640, "hidden objects", th + .4, BONE, 28)]
    td = T("hidden", "describe")
    arc = [(640 + (1060 - 640) * k / 20, 410 - 230 * math.sin(math.pi * k / 20) + 70 * k / 20) for k in range(21)]
    els += dots_along(arc, td, 1.0, LILAC, 4)
    els.append(lab(889, 168, "August 1972", .5, MUTED, 26))
    tw = T("hidden", "did")
    els += [rect(230, 680, 520, 84, PAPER, PAPER_D, 1.5, 3, tw - .4, fx="rise"), ink(490, 732, "the subject did well", tw - .2, TYPE, 30, st="ital"),
            lab(490, 800 - 16, "a CIA account", tw + .3, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_money():
    """s11: a work order for $2,500 and its bar; then a bar twenty times longer, $50,000, within months (bars to scale)."""
    els = desk_bg()
    t1 = T("money", "work order")
    els += [rect(160, 210, 380, 270, "rgba(0,0,0,.45)", at=-1), rect(150, 200, 380, 270, PAPER, PAPER_D, 1.5, 3, -1),
            ink(340, 252, "WORK ORDER", -1, TYPE, 30, weight=700)] + static(page_lines(190, 290, 300, 3, -1, 26, seed=5)) + \
           [ink(340, 430, "$2,500", t1 + .2, "#b8322a", 46, st="serif"), rect(150, 200, 380, 270, "none", AU, 3, 3, t1 + .2, fx="pop")]
    x0, unit = 640, 50.0                                     # $2,500 = 50 units; $50,000 = 1,000 units
    tb = T("money", "two and a half")
    els += [bar(x0, x0 + unit, 330, 46, tb, AMBER, .5), lab(x0 + unit + 22, 342, "$2,500", tb + .4, AMBER, 32, "start")]
    tf = T("money", "fifty-thousand-dollar")
    els += [bar(x0, x0 + 20 * unit, 540, 46, tf - .8, GOLD, 1.8), lab(x0 + 20 * unit, 494, "$50,000", tf + .6, GOLD, 36, "end"),
            lab(x0, 626, "within months", T("money", "Within months"), BONE, 30, "start")]
    els += [ln([(x0, 300), (x0, 580)], -1, MUTED, 2, draw=False, op=.6), lab(x0 + 20 * unit, 640, "bars to scale", tf + 1.0, MUTED, 24, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_nature():
    """s12: a journal on a lectern, 'Nature', 'October 1974'; a head whose eyes and ears are shielded; a dotted channel passes the
    shield into it: 'no known sense' (their claim)."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(470, 360, 420, -1, .22), gl(1200, 470, 420, -1, .12)]
    els += [poly([(330, 760), (610, 760), (560, 470), (380, 470)], "#3a2c20", "#8a6a48", 2, -1),
            poly([(290, 470), (650, 470), (610, 420), (330, 420)], "#4a3828", "#8a6a48", 2, -1)]
    els += [rect(350, 170, 260, 300, "#7a2a22", "#e8b87a", 2, 4, .3, fx="rise"), ink(480, 250, "Nature", .4, "#f5ecdc", 54, st="serif"),
            ln([(380, 290), (580, 290)], .4, "#f5ecdc", 2, draw=False, op=.6)] + static(page_lines(385, 330, 190, 4, -1, 26, c="#e8c9a6", seed=9)) + \
           [lab(480, 520, "October 1974", .7, BONE, 28)]
    tk = T("nature", "no known sense")
    hx, hy, hs = 1220, 470, 440
    els += [head(hx, hy, hs, .3, "#3a3029", "rgba(255,236,206,.45)", 2.5)]
    tsh = T("nature", "perceiving") - .4
    els += [poly([(hx - .43 * hs, hy - .2 * hs), (hx + .41 * hs, hy - .14 * hs), (hx + .42 * hs, hy - .04 * hs), (hx - .44 * hs, hy - .08 * hs)], "#0b0907", "#8a7a66", 2, tsh, fx="pop"),
            circ(hx - .06 * hs, hy + .06 * hs, .085 * hs, "#0b0907", "#8a7a66", 2, tsh + .2, fx="pop"),
            lab(hx - .06 * hs, hy + .26 * hs, "eyes and ears shielded", tsh + .3, MUTED, 24)]
    pts = [(760 + 20 * k, 230 + 6 * k + 30 * math.sin(k / 3)) for k in range(22)]
    els += dots_along(pts, tk - .8, 1.0, LILAC, 4.5) + [gl(1200, 330, 120, tk + .2, .5)]
    els += [lab(900, 200, "no known sense", tk, LILAC, 32), lab(900, 236, "their claim", tk + .3, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_coords():
    """s13: a sheet of map grid; a crosshair settles on one point; everything else fades, leaving the crosshair: 'coordinates only'."""
    x0, y0, x1, y1 = 260, 150, 1520, 760
    els = [rect(x0, y0, x1 - x0, y1 - y0, "#1b2230", "#5d7ea6", 2, 4, -1)]
    X = lambda lo: x0 + 40 + (lo - 55) * 29.5
    Y = lambda la: y1 - 30 - (la - 35) * 19
    for lo in range(55, 96, 5):
        els.append(ln([(X(lo), y0 + 8), (X(lo), y1 - 8)], -1, "#3c5a7a", 1.4 if lo % 10 else 2, draw=False, op=.8))
    for la in range(35, 66, 5):
        els.append(ln([(x0 + 8, Y(la)), (x1 - 8, Y(la))], -1, "#3c5a7a", 1.4 if la % 10 else 2, draw=False, op=.8))
    els += [lab(X(60), y1 + 34, "60° E", -1, MUTED, 24), lab(X(80), y1 + 34, "80° E", -1, MUTED, 24),
            lab(x0 - 12, Y(40) + 8, "40° N", -1, MUTED, 24, "end"), lab(x0 - 12, Y(60) + 8, "60° N", -1, MUTED, 24, "end")]
    cx, cy = X(78), Y(50)
    tc = T("coords", "coordinates")
    els += [circ(cx, cy, 46, "none", GOLD, 3, tc - 1.2, fx="draw"), ln([(cx, cy - 74), (cx, cy + 74)], tc - 1.0, GOLD, 2.5, dur=.4),
            ln([(cx - 74, cy), (cx + 74, cy)], tc - 1.0, GOLD, 2.5, dur=.4), dot(cx, cy, 6, GOLD, tc - .8)]
    tv = tc - .2
    els += [veil(x0 + 2, y0 + 2, cx - 140 - x0, y1 - y0 - 4, tv, "#1b2230", .88, 1.0), veil(cx + 140, y0 + 2, x1 - cx - 142, y1 - y0 - 4, tv, "#1b2230", .88, 1.0),
            veil(cx - 140, y0 + 2, 280, cy - 120 - y0, tv, "#1b2230", .88, 1.0), veil(cx - 140, cy + 120, 280, y1 - cy - 122, tv, "#1b2230", .88, 1.0)]
    els += [lab(cx, cy + 170, "coordinates only", tc + .3, GOLD, 34)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_price():
    """s14: Pat Price at a table with an open atlas and a pencil circle; then the crane sketch slides in beside him: July 1974."""
    els = desk_bg(c="#1b140e")
    tp = T("price", "Pat")
    els += [gl(560, 420, 520, -1, .18)] + table(600, 590, 760, -1, h=110)
    els += seated_figure(330, 700, 330, .4, "#a39a8e", 1)
    els += [poly([(500, 586), (690, 520), (700, 588)], "#d8ccb2", "#8a7a66", 1.5, -1), poly([(700, 588), (690, 520), (900, 540), (900, 590)], "#e4d8be", "#8a7a66", 1.5, -1)]
    els += [{"k": "line", "p": R([(720, 560), (760, 548), (820, 556), (860, 546)]), "c": "#6f8fa8", "w": 2, "in": -1, "curve": True},
            {"k": "line", "p": R([(540, 575), (600, 560), (660, 548)]), "c": "#6f8fa8", "w": 2, "in": -1, "curve": True}, ring_(800, 566, 34, T("price", "Burbank") - .6),
            lab(700, 650, "an atlas", T("price", "Burbank") - .4, MUTED, 24)]
    els += [lab(330, 248, "Pat Price", tp, BONE, 32), lab(330, 286, "former police commissioner", tp + .5, MUTED, 26)]
    ts = T("price", "crane") - .6
    els += [rect(1022, 196, 560, 420, "rgba(0,0,0,.45)", at=ts, fx="rise"), rect(1010, 184, 560, 420, "#efe6d2", "#fff6e2", 1.5, 3, ts, fx="rise")]
    cr, _ = crane(1290, 540, .4, ts + .2)
    els += [grp(cr, ts + .2, "rise")]
    els += [lab(1290, 664, "July 1974", ts + .5, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def ring_(x, y, r, at, c="#3b3530"):
    return {"k": "line", "p": R([(x + r * math.cos(math.radians(a)), y + r * .45 * math.sin(math.radians(a))) for a in range(0, 380, 20)]), "c": c, "w": 3, "fx": "draw", "dur": .6, "in": round(at, 2), "curve": True}


ST_COLS, ST_ROWS, ST_W, ST_H, ST_GX, ST_GY = 8, 5, 150, 84, 22, 22
ST_X0 = round((1778 - (ST_COLS * ST_W + (ST_COLS - 1) * ST_GX)) / 2)
ST_Y0 = 150
HITS = {13: "crane", 22: "tanks", 34: "buildings"}             # the descriptions the CIA report singles out as amazing
UNCHECKED = {1, 4, 6, 9, 11, 16, 19, 25, 27, 29, 31, 36, 38, 2, 17}   # a schematic share; the report gives no count


def st_xy(i):
    return ST_X0 + (i % ST_COLS) * (ST_W + ST_GX), ST_Y0 + (i // ST_COLS) * (ST_H + ST_GY)


def mini_icon(kind, x, y, s, at, c=AU):
    if kind == "crane":
        cr, _ = crane(x, y + 22 * s, .085 * s, at, "plan", w=1.4 if s < 2 else 2.2, col=GOLD)
        return [grp(cr, at, None)]
    if kind == "tanks":
        return [circ(x - 18 * s, y + 4, 15 * s, "none", c, 2.5, at), circ(x + 18 * s, y + 4, 15 * s, "none", c, 2.5, at)]
    return [rect(x - 30 * s, y - 14 * s, 60 * s, 34 * s, "none", c, 2.5, 2, at), ln([(x - 30 * s, y - 14 * s), (x, y - 30 * s), (x + 30 * s, y - 14 * s)], at, c, 2.5, draw=False)]


def sc_statements():
    """s15: forty cards, Price's statements (schematic); most get a red cross or a grey '?' as said; three glow gold (the crane, the
    tank sections, the buildings); then the crane card lifts out and glows: remembered."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    for i in range(ST_COLS * ST_ROWS):
        x, y = st_xy(i)
        hit = i in HITS
        els.append(card(x, y, ST_W, ST_H, round(.2 + .012 * i, 2), "#2a241d", AU if hit else "#5a4a3c", fx="pop"))
        if hit:
            els += mini_icon(HITS[i], x + ST_W / 2, y + ST_H / 2, 1.0, round(.3 + .012 * i, 2))
            els.append(gl(x + ST_W / 2, y + ST_H / 2, 90, round(.5 + .012 * i, 2), .35))
        else:
            els += page_lines(x + 16, y + 24, ST_W - 32, 3, round(.25 + .012 * i, 2), 18, sw=2.5, seed=40 + i)
    tw, tc = T("statements", "wrong"), T("statements", "checked")
    k = 0
    for i in range(ST_COLS * ST_ROWS):
        if i in HITS or i in UNCHECKED:
            continue
        x, y = st_xy(i)
        els += cross(x + ST_W / 2, y + ST_H / 2, round(tw - .3 + .03 * k, 2), RED, 1.2, 5)
        k += 1
    for j, i in enumerate(sorted(UNCHECKED)):
        x, y = st_xy(i)
        els.append(lab(x + ST_W / 2, y + ST_H / 2 + 14, "?", round(tc - .2 + .04 * j, 2), MUTED, 40, st="serif"))
    els += [lab(889, 718, "most: wrong or unchecked", tc + .5, BONE, 30), lab(889, 754, "schematic: the report gives no count", tc + .9, MUTED, 24)]
    tr = T("statements", "remembers") - .5
    cx, cy = 889, 380
    els += [rect(cx - 220 + 14, cy - 140 + 16, 440, 280, "rgba(0,0,0,.6)", at=tr, fx="pop"), card(cx - 220, cy - 140, 440, 280, tr, "#2a241d", AU),
            gl(cx, cy, 300, tr + .1, .4)] + mini_icon("crane", cx, cy - 30, 3.3, tr + .1)
    els.append(lab(cx, cy + 112, "remembered", tr + .4, AU, 32, st="serif"))
    return {"base": "dark", "cam": CAM, "els": els}


def add_memory():
    """s35: back on Price's cards: the others fade almost away ('forgotten'); the crane card glows larger ('told again and again')."""
    t0, tf = T("memory", "told again"), T("memory", "forgotten")
    els = [veil(ST_X0 - 20, ST_Y0 - 20, 1778 - 2 * ST_X0 + 40, 800 - ST_Y0, tf - .8, FLAT, .86, 1.6),
           veil(560, 120, 660, 560, tf - .8, FLAT, .9, 1.6), veil(420, 680, 940, 100, tf - .8, FLAT, 1.0, 1.0)]
    cx, cy = 889, 380
    for k in range(3):
        els.append({"k": "circle", "x": cx, "y": cy, "r": 200 + 70 * k, "fill": "none", "c": AU, "w": 3 - .7 * k, "in": round(t0 + .35 * k, 2), "fx": "draw", "dur": .8,
                    "op": .7 - .2 * k, "keepop": True})
    els += [card(cx - 250, cy - 140, 500, 280, t0 - .3, "#2a241d", AU), gl(cx, cy, 360, t0, .45)] + mini_icon("crane", cx, cy - 8, 4.3, t0 - .2)
    els += [lab(cx, 140, "told again and again", t0 + .4, AU, 32), lab(889, 718, "forgotten", tf, MUTED, 30)]
    return els


# ================================================================== chapter 2: the unit at Fort Meade
MEADE_V = View(-77.75, -76.25, 38.6, 39.6, (120, 165, 500, 380))


def sc_meade():
    """s16: a map of the Washington area, Fort Meade pinned; at the right two low wooden barracks among trees at dusk, a flag."""
    els = inset_map(MEADE_V, 110, 150, 520, 410, -1)
    fx_, fy_ = MEADE_V.p(-76.743, 39.108)
    wx, wy = MEADE_V.p(-77.037, 38.907)
    mx, my = MEADE_V.p(-77.25, 39.42)
    els += [{"k": "pin", "x": wx, "y": wy, "t": "Washington", "a": "end", "lx": -18, "in": -1},
            {"k": "pin", "x": fx_, "y": fy_, "t": "Fort Meade", "c": GOLD, "in": T("meade", "Fort Meade")},
            lab(mx, my, "Maryland", -1, "#c9ad85", 26, st="ital")]
    # dusk: trees behind, two barracks, a flagpole, dark grass
    els += [rect(-20, 688, 1820, 340, "#1a1712", at=-1, op=.92)]
    for k, (x, h) in enumerate(((760, 210), (840, 260), (1150, 230), (1330, 280), (1520, 240), (1640, 200))):
        els += tree(x, 640, h, -1, "#17130f", op=.9)
    els += barracks(1120, 600, 470, 110, -1, lit=(3,), op=.75)
    els += barracks(760, 680, 600, 150, -1, lit=(1, 4))
    els += [ln([(1560, 690), (1560, 360)], -1, "#cbbca8", 3, draw=False), poly([(1562, 362), (1650, 376), (1562, 400)], "#9a4a3a", at=-1, curve=True)]
    els += [lab(1060, 300, "1977", T("meade", "From nineteen"), GOLD, 36, st="serif"),
            lab(1060, 750, "old wooden barracks", T("meade", "barracks"), BONE, 28)]
    return {"base": "sky", "tod": "dusk", "ground": 690, "sun": [1460, 640, 24], "cam": CAM, "els": els}


NAMES = [("GONDOLA WISH", 1977, 0), ("GRILL FLAME", 1978, 1), ("CENTER LANE", 1983, 0), ("SUN STREAK", 1985, 1), ("STAR GATE", 1991, 0)]
NAME_SAY = ["Gondola", "Grill", "Center", "Sun Streak", "Star Gate"]


def sc_names():
    """s17: five manila folders hung on a time axis at their years (1977, 1978, 1983, 1985, 1991), each stamped with its code name as
    it is said; the last, STAR GATE, larger and gold. Then a satellite and a head: could a mind see what cameras couldn't?"""
    X = lambda y: 190 + (y - 1975) * 68
    els = [axis(190, 1550, 740, [(X(1980), "1980"), (X(1990), "1990")], .2)]
    for k, (n, yr, row) in enumerate(NAMES):
        big = k == 4
        w, h = (330, 170) if big else (270, 136)
        x0, y0 = X(yr) - w / 2, (220 if row == 0 else 460)
        ta = T("names", NAME_SAY[k])
        els += [folder(x0, y0, w, h, .4 + .1 * k, "none", style="inferred", op=.5, edge="#8a6a48"),
                ln([(X(yr), y0 + h), (X(yr), 732)], .4 + .1 * k, "#8a6a48", 1.5, "inferred", draw=False, op=.6),
                dot(X(yr), 740, 6, MUTED, .5 + .1 * k)]
        els += [folder(x0, y0, w, h, ta, AU if big else MANILA, fx="pop", edge="#b8942a" if big else MANILA_E),
                ink(X(yr), y0 + h / 2 + 12, n, ta + .05, "#7a1f16" if big else TYPE, 34 if big else 28, weight=700),
                lab(X(yr), y0 + h + 30 if row == 1 else y0 - 16, str(yr), ta + .1, MUTED, 24)]
        if big:
            els.append(gl(X(yr), y0 + h / 2, 240, ta, .45))
    tc = T("names", "cameras")
    # a satellite looking down, a head looking out: which one sees?
    sx, sy = 1590, 300
    els += [rect(sx - 26, sy - 20, 52, 40, "#9aa4ae", "#e9eef2", 2, 4, tc - .6, fx="pop"), rect(sx - 96, sy - 12, 62, 24, "#2c4a6e", "#9fd0ff", 1.5, 2, tc - .6, fx="pop"),
            rect(sx + 34, sy - 12, 62, 24, "#2c4a6e", "#9fd0ff", 1.5, 2, tc - .6, fx="pop"), circ(sx, sy + 26, 9, "#1b2230", "#9fd0ff", 2, tc - .5),
            poly([(sx - 8, sy + 34), (sx + 8, sy + 34), (sx + 60, sy + 150), (sx - 60, sy + 150)], "rgba(159,208,255,.12)", at=tc - .4)]
    els += [head(1600, 600, 160, tc - .2, "#2a2420", "rgba(201,193,238,.6)", 2, fx="pop", face=-1)]
    els += qmark(1480, 500, tc + .4, 70)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_mcmoneagle():
    """s18: a soldier in fatigues, Joseph McMoneagle, 'Remote Viewer No. 1', 1978; at the right Swann at a board with a coordinate
    grid, two trainees: Swann trains viewers."""
    tj, tr, ts = T("mcmoneagle", "Joseph"), T("mcmoneagle", "Remote Viewer"), T("mcmoneagle", "Ingo Swann later")
    els = [gl(420, 470, 380, -1, .16), gl(1300, 420, 460, -1, .12)]
    els += [ppl(400, 760, 340, tj - .3, OLIVE), lab(400, 386, "Joseph McMoneagle", tj, BONE, 30)]
    els += [rect(520, 470, 300, 76, "#2a241d", AU, 2.5, 38, tr - .3, fx="pop"), lab(670, 518, "Remote Viewer No. 1", tr, AU, 28),
            lab(670, 590, "1978", tr + .4, MUTED, 26)]
    # Swann's class: a board with a coordinate grid and a crosshair, two seated trainees
    bx0, by0, bw, bh = 1080, 190, 520, 320
    els += [rect(bx0, by0, bw, bh, "#1d2a24", "#6a7a66", 3, 6, ts - .6, fx="rise")]
    for k in range(1, 7):
        els.append(ln([(bx0 + bw * k / 7, by0 + 14), (bx0 + bw * k / 7, by0 + bh - 14)], ts - .4, "#cfe0d0", 1.5, draw=False, op=.5))
    for k in range(1, 5):
        els.append(ln([(bx0 + 14, by0 + bh * k / 5), (bx0 + bw - 14, by0 + bh * k / 5)], ts - .4, "#cfe0d0", 1.5, draw=False, op=.5))
    els += [circ(bx0 + bw * 4 / 7, by0 + bh * 2 / 5, 22, "none", "#f5ecdc", 3, ts), ln([(bx0 + bw * 4 / 7 - 36, by0 + bh * 2 / 5), (bx0 + bw * 4 / 7 + 36, by0 + bh * 2 / 5)], ts, "#f5ecdc", 2.5, dur=.3),
            ln([(bx0 + bw * 4 / 7, by0 + bh * 2 / 5 - 36), (bx0 + bw * 4 / 7, by0 + bh * 2 / 5 + 36)], ts, "#f5ecdc", 2.5, dur=.3)]
    els += [ppl(1000, 760, 300, ts - .2, "#a39a8e"), ln([(1040, 540), (1120, 440)], ts + .2, "#a39a8e", 6, draw=False)]
    els += seated_figure(1250, 760, 220, ts + .3, "#7d766c", -1) + seated_figure(1470, 760, 220, ts + .45, "#7d766c", -1)
    els += [lab(1340, 580, "Swann trains viewers", ts + .5, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_room():
    """s19: a quiet room in dim light: the viewer at the left with paper and pencil, the monitor at the right with a clipboard and a
    dotted '?' (blind too); on the table a card with a row of digits: only a number."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), rect(170, 140, 1440, 640, "#211a14", "#4a3a2c", 2, 6, -1), rect(170, 690, 1440, 90, "#18120d", at=-1)]
    els += [ln([(170, 690), (1610, 690)], -1, "#4a3a2c", 2, draw=False)] + lamp(889, 260, -1, cord=120, op=.7, r=380) + [cone(889, 276, 60, 640, 600, -1, .07)]
    els += table(889, 560, 520, -1, h=130)
    tv, tm, tb, tn = T("room", "viewer sat"), T("room", "monitor"), T("room", "did not know"), T("room", "number")
    els += seated_figure(560, 690, 300, tv - .3, "#a39a8e", 1)
    els += [rect(660, 540, 120, 20, "#efe6d2", at=tv), ln([(690, 538), (740, 520)], tv, GOLD, 3, draw=False)]
    els += seated_figure(1220, 690, 300, tm - .3, "#8a96a2", -1)
    els += [rect(1050, 470, 70, 92, "#c9a86a", "#6a5038", 2, 4, tm), rect(1058, 480, 54, 70, "#efe6d2", at=tm)]
    els += [lab(560, 330, "the viewer", tv, BONE, 28), lab(1220, 330, "the monitor", tm, BONE, 28)]
    cx, cy = 1290, 240
    els += [dot(cx + 34 * math.cos(math.radians(a)), cy + 26 * math.sin(math.radians(a)), 3.5, LILAC, round(tb - .3 + .02 * k, 2)) for k, a in enumerate(range(0, 360, 20))]
    els += [lab(cx, cy + 14, "?", tb, LILAC, 40, st="serif"), dot(1262, 286, 4, LILAC, tb), dot(1248, 300, 3, LILAC, tb + .1), lab(cx + 60, cy - 40, "blind too", tb + .3, LILAC, 26, "start")]
    els += [rect(830, 536, 118, 26, "#f5ecdc", "#cdbf9f", 1.5, 3, tn - .3, fx="pop")]
    els += [dot(846 + 10 * k + (8 if k > 3 else 0), 549, 3, TYPE, tn - .2) for k in range(8)]
    els += [gl(889, 548, 80, tn, .5), lab(889, 650, "only a number", tn + .2, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_sheet():
    """s20: the viewer's sheet, close: a few words appear one by one, a rough sketch scribbles itself; then the sheet goes out as a
    typed report (schematic)."""
    els = desk_bg(c="#1b140e")
    x0, y0, w, h = 300, 150, 960, 600
    els += [rect(x0 + 12, y0 + 14, w, h, "rgba(0,0,0,.5)", at=-1), rect(x0, y0, w, h, "#efe6d2", "#fff6e2", 1.5, 3, -1)]
    td, tk = T("sheet", "described"), T("sheet", "sketched")
    for k, wd in enumerate(("tall", "metal", "cold")):
        els.append(note(x0 + 90, y0 + 120 + 70 * k, wd, td + .1 + .55 * k, GRAPH, 40, "start", st="ital"))
    sx = x0 + 460
    sk = [[(sx + 70, y0 + 520), (sx + 110, y0 + 290)], [(sx + 250, y0 + 520), (sx + 210, y0 + 290)], [(sx + 90, y0 + 410), (sx + 230, y0 + 410)],
          [(sx + 70, y0 + 290), (sx + 70, y0 + 170), (sx + 250, y0 + 170), (sx + 250, y0 + 290), (sx + 70, y0 + 290)], [(sx + 60, y0 + 170), (sx + 160, y0 + 110), (sx + 260, y0 + 170)],
          [(sx - 20, y0 + 520), (sx + 330, y0 + 520)]]
    for k, pts in enumerate(sk):
        els += sketchy(pts, tk + .25 * k, GRAPH, 3.2, draw=True, dur=.5)
    els += [ln([(sx + 40 + 16 * k, y0 + 560), (sx + 60 + 16 * k, y0 + 536)], tk + 1.6, GRAPH, 2, draw=False, op=.5) for k in range(10)]
    tr = T("sheet", "report")
    els += [rect(1300, 300, 330, 430, "rgba(0,0,0,.5)", at=tr - .5, fx="rise"), rect(1288, 286, 330, 430, PAPER, PAPER_D, 1.5, 3, tr - .5, fx="rise"),
            rect(1288, 286, 330, 56, "#b8322a", at=tr - .4), note(1453, 326, "REPORT", tr - .3, "#f5ecdc", 30, weight=700)]
    els += [grp(page_lines(1318, 380, 270, 10, -1, 30, seed=21), tr - .2, "rise")]
    els += [lab(x0 + w / 2, 800, "schematic", tk + 1.0, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_agencies():
    """s21: three agency buildings at the left; sealed envelopes travel along an arrow into the unit's barracks at the right
    ('targets'); reports travel back along the lower arrow ('reports')."""
    els = [gl(500, 520, 420, -1, .12), gl(1400, 540, 380, -1, .12)]
    els += building(250, 660, 210, -1, "columns") + building(520, 660, 180, -1, "hq") + building(800, 660, 180, -1, "block", lit=(1, 5))
    els += [lab(520, 724, "intelligence agencies", .3, BONE, 28)]
    els += barracks(1240, 660, 420, 130, -1, lit=(1,))
    els += [lab(1450, 724, "the unit", .5, BONE, 28)]
    tt, tw = T("agencies", "real targets"), T("agencies", "wanted")
    els += [arr([(900, 420), (1220, 420)], tt - .4, AMBER, 4, dur=.8), lab(1060, 376, "targets", tt, AMBER, 30)]
    for k in range(3):
        els += [grp(envelope(955 + 95 * k, 420, 64, -1), round(tt + .1 + .25 * k, 2), "pop")]
    els += [arr([(1220, 540), (900, 540)], tw - .2, BLUE, 4, dur=.8), lab(1060, 604, "reports", tw + .3, BLUE, 30)]
    for k in range(3):
        els += [grp(sheet(1110 - 95 * k - 22, 514, 44, 52, -1, None, lines=3, seed=50 + k, lh=12), round(tw + .3 + .25 * k, 2), "pop")]
    els += [lab(1060, 300, "foreign places and things", tt + .8, MUTED, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_timeline():
    """s22: a time line 1970 to 1997; bands for who ran it: CIA 1972 to 1977 (the lab), Army 1977 to 1985, DIA 1985 to 1995; a
    bracket over 1972 to 1995, 23 years; about $20 million."""
    X = lambda y: round(160 + (y - 1970) * 1460 / 27, 1)
    els = [axis(160, 1620, 680, [(X(1972), "1972"), (X(1985), "1985"), (X(1995), "1995")], .2)]
    td, ty, tm = T("timeline", "Defense Intelligence"), T("timeline", "twenty-three years"), T("timeline", "twenty million")
    for (a, b, t, c, at) in ((1972, 1977, "CIA", BLUE, .5), (1977, 1985, "Army", "#9aa37a", 1.0), (1985, 1995, "DIA", AMBER, td - .3)):
        els += [{"k": "band", "x0": X(a), "x1": X(b), "y": 580, "h": 26, "c": c, "t": t, "tc": c, "in": round(at, 2), "dur": .9}]
    els += [ln([(X(1972), 480), (X(1972), 460), (X(1995), 460), (X(1995), 480)], ty - .3, GOLD, 3, dur=1.0), lab((X(1972) + X(1995)) / 2, 440, "23 years", ty + .3, GOLD, 34)]
    cx = 889
    els += [grp([circ(cx - 300, 316 - 9 * k, 26, "#d8b45a", "#8a6420", 1.5, -1) for k in range(8)], tm - .4, "rise"),
            lab(cx - 250, 332, "about $20 million", tm, GOLD, 40, "start", st="serif")]
    els += [lab(X(1974.5), 532, "the lab", .8, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


WORLD_V = View(-10, 125, -15, 74, (110, 140, 1560, 560))


def plane_icon(x, y, s, at, c=LILAC):
    pts = [(-60, 0), (-40, -8), (40, -8), (58, -2), (60, 4), (40, 8), (-40, 8)]
    wing = [(-6, -8), (14, -50), (26, -50), (18, -8)]
    wing2 = [(-6, 8), (14, 50), (26, 50), (18, 8)]
    tail = [(-48, -6), (-56, -26), (-48, -26), (-38, -6)]
    q = lambda P_: [(x + px * s, y + py * s) for px, py in P_]
    return [poly(q(pts), "rgba(201,193,238,.12)", c, 2.5, at, style="claimed", fx="pop"), poly(q(wing), "rgba(201,193,238,.12)", c, 2.5, at, style="claimed"),
            poly(q(wing2), "rgba(201,193,238,.12)", c, 2.5, at, style="claimed"), poly(q(tail), "rgba(201,193,238,.12)", c, 2.5, at, style="claimed")]


def sub_icon(x, y, s, at, c=LILAC):
    hull = [(x + 70 * s * math.cos(math.radians(a)), y + 14 * s * math.sin(math.radians(a))) for a in range(0, 360, 15)]
    sail = [(x - 10 * s, y - 12 * s), (x - 4 * s, y - 34 * s), (x + 18 * s, y - 34 * s), (x + 20 * s, y - 12 * s)]
    return [poly(hull, "rgba(201,193,238,.12)", c, 2.5, at, style="claimed", fx="pop", curve=True), poly(sail, "rgba(201,193,238,.12)", c, 2.5, at, style="claimed")]


def sc_legends():
    """s23: a dim map; a dotted plane in central Africa ('a crashed plane'), a dotted submarine in the Soviet north ('a new
    submarine'): their accounts, in the claimed style; a grey dashed card: hard to check."""
    els = inset_map(WORLD_V, 110, 140, 1560, 560, -1, "#2e2820", "#101820")
    px, py = WORLD_V.p(22, 0)
    sx, sy = WORLD_V.p(40, 63)
    tp, ts, tc = T("legends", "crashed"), T("legends", "submarine"), T("legends", "hard to check")
    els += [gl(px, py, 120, tp - .3, .4, "scan")] + plane_icon(px, py, 1.3, tp - .2) + [lab(px + 100, py + 10, "a crashed plane", tp + .2, LILAC, 28, "start")]
    els += [gl(sx, sy, 120, ts - .3, .4, "scan")] + sub_icon(sx, sy, 1.4, ts - .2) + [lab(sx, sy + 70, "a new Soviet submarine", ts + .2, LILAC, 28)]
    els += [rect(560, 726, 660, 60, "rgba(18,13,10,.85)", MUTED, 2, 30, tc - .4, fx="pop", style="inferred"), lab(889, 766, "their accounts: hard to check", tc - .2, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_target():
    """s24: a paper target with dart holes; one in the bullseye glows ('a hit?'); then a tally counts itself: the misses outnumber
    the hit."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(600, 470, 420, -1, .14)]
    cx, cy = 600, 460
    els += [rect(330, 180, 540, 560, "#4a3a2a", "#8a6a48", 3, 6, -1), rect(370, 210, 460, 500, "#efe6d2", "#cdbf9f", 1.5, 2, -1)]
    for k, (r, c) in enumerate(((200, "#efe6d2"), (160, "#3b3530"), (120, "#efe6d2"), (80, "#3b3530"), (40, "#b8322a"))):
        els.append(circ(cx, cy, r, c, "#3b3530", 2, -1))
    rnd = random.Random(7)
    holes = []
    while len(holes) < 13:
        a, d = rnd.uniform(0, 2 * math.pi), rnd.uniform(70, 230)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        if 380 < x < 820 and 220 < y < 700:
            holes.append((x, y))
    th = T("target", "real hit")
    els += [dot(round(x, 1), round(y, 1), 6, "#15110d", -1) for x, y in holes]
    els += [dot(cx + 12, cy - 8, 7, "#15110d", -1), gl(cx + 12, cy - 8, 70, th, .7), circ(cx + 12, cy - 8, 22, "none", AU, 3, th, fx="draw"),
            lab(cx + 150, cy - 230, "a hit?", th + .2, AU, 32), ln([(cx + 118, cy - 214), (cx + 28, cy - 24)], th + .2, AU, 2, "inferred", .4)]
    tc = T("target", "You count")
    els += [lab(1050, 330, "misses", tc - .6, BONE, 30, "start"), lab(1050, 560, "hits", tc - .6, BONE, 30, "start")]
    for k in range(13):
        g, j = divmod(k, 5)
        x = 1060 + g * 150 + j * 22
        if j == 4:
            els.append(ln([(x - 92, 420), (x + 6, 372)], round(tc + .08 * k, 2), BONE, 4, dur=.15))
        else:
            els.append(ln([(x, 370), (x, 424)], round(tc + .08 * k, 2), BONE, 4, dur=.15))
    els.append(ln([(1060, 600), (1060, 654)], tc + 1.2, AU, 4, dur=.15))
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 3: the judging problem
def on_land(lon, lat):
    """Is this point on land (Natural Earth 50 m)? Ray casting on the rings near it."""
    inside = False
    for poly_ in _topo():
        r = poly_[0]
        xs = [q[0] for q in r]
        ys = [q[1] for q in r]
        if not (min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys)):
            continue
        n = len(r)
        c = False
        for i in range(n):
            x1, y1 = r[i]
            x2, y2 = r[(i + 1) % n]
            if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / ((y2 - y1) or 1e-12) + x1:
                c = not c
        inside = inside or c
    return inside


def safe_icon(x, y, w, h, at, door=True):
    """A steel safe, front view, its door swung open to the left; (x, y) = top left of the body."""
    els = [rect(x, y, w, h, "#4d5257", "#c9d0d6", 3, 10, at), rect(x + 26, y + 26, w - 52, h - 52, "#16181b", "#7a8086", 2, 6, at)]
    if door:
        els += [poly([(x - 4, y + 10), (x - w * .42, y + 50), (x - w * .42, y + h - 50), (x - 4, y + h - 10)], "#5d6266", "#c9d0d6", 3, at),
                circ(x - w * .24, y + h / 2, 34, "#3a3d40", "#c9d0d6", 3, at), ln([(x - w * .24, y + h / 2 - 34), (x - w * .24, y + h / 2 - 20)], at, "#c9d0d6", 3, draw=False)]
    return els


def sc_safe():
    """s25: a feeling turned into a number (a dotted cloud, an arrow, a tally); then a steel safe, open: more than a hundred sealed
    envelopes fill its shelves; a padlock: locked."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(860, 460, 520, -1, .14)]
    sx, sy, sw, shh = 660, 180, 520, 560
    els += safe_icon(sx, sy, sw, shh, -1)
    tf = T("safe", "feeling")
    cl = [(1420 + 70 * math.cos(math.radians(a)) + 12 * math.sin(math.radians(3 * a)), 300 + 44 * math.sin(math.radians(a))) for a in range(0, 360, 12)]
    els += [lab(1420, 312, "?", tf - .2, LILAC, 44, st="serif")] + dots_along(cl, tf - .4, .6, LILAC, 3.5)
    tn = T("safe", "number")
    els += [arr([(1420, 360), (1420, 450)], tn - .3, MUTED, 3, dur=.4)]
    for k in range(6):
        g, j = divmod(k, 5)
        x = 1360 + g * 110 + j * 20
        els.append(ln([(x - 76, 530), (x + 6, 488)] if j == 4 else [(x, 486), (x, 532)], round(tn + .08 * k, 2), GOLD, 4, dur=.15))
    els += [lab(1420, 590, "a number", tn + .5, GOLD, 30)]
    th, tse, tl = T("safe", "hundred"), T("safe", "sealed"), T("safe", "locked")
    ex0, ey0 = sx + 40, sy + 44
    k = 0
    for r_ in range(8):
        els.append(rect(sx + 30, ey0 + 58 * r_ + 46, sw - 60, 5, "#3a3d40", at=-1))
        for c_ in range(13):
            x = ex0 + 34 * c_
            y = ey0 + 58 * r_ + 8
            els += [rect(x, y, 28, 36, "#e8dcc2", "#a8987c", 1, 2, round(th + .012 * k, 2), fx="pop")]
            k += 1
    els += [lab(sx + sw / 2, sy + shh + 46, "more than 100 places", th + .9, BONE, 30)]
    els += [lab(sx - 120, sy + shh + 46, "sealed", tse, AMBER, 28)]
    px_, py_ = sx + sw + 70, sy + shh / 2
    els += [rect(px_ - 30, py_ - 6, 60, 52, AU, "#8a6420", 2, 6, tl - .2, fx="pop"),
            ln([(px_ - 18, py_ - 4), (px_ - 18, py_ - 30), (px_, py_ - 44), (px_ + 18, py_ - 30), (px_ + 18, py_ - 4)], tl - .2, AU, 6, draw=False, curve=True),
            lab(px_, py_ + 90, "locked", tl + .2, AU, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


BAYB = View(-122.58, -121.86, 37.22, 37.74, (90, 130, 1600, 660))
SRI_PT = (-122.1739, 37.4566)


def pool_points(n=104, seed=11):
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        lon, lat = rnd.uniform(-122.52, -121.9), rnd.uniform(37.26, 37.70)
        d = math.hypot((lon - SRI_PT[0]) * 88.0, (lat - SRI_PT[1]) * 111.0)
        if 1.5 < d < 26 and on_land(lon, lat):
            out.append((lon, lat))
    return out


POOL = None


def sc_baymap():
    """s26: the Bay: about a hundred dim dots around SRI (the target pool); one lights gold (drawn at random); the team drives to it;
    at SRI a shielded room with the viewer and an experimenter; a dotted line joins the room to the site (the claim)."""
    global POOL
    if POOL is None:
        POOL = pool_points()
    els = inset_map(BAYB, 90, 130, 1600, 660, -1, "#3a3024", "#12202a")
    sx, sy = BAYB.p(*SRI_PT)
    els += [{"k": "pin", "x": sx, "y": sy, "t": "SRI", "c": GOLD, "in": -1}]
    els += [dot(*BAYB.p(lo, la), 5, "#cbbca8", round(.2 + .006 * k, 2), op=.55) for k, (lo, la) in enumerate(POOL)]
    bx, by = BAYB.p(-122.27, 37.64)
    els += [lab(bx, by, "San Francisco Bay", -1, "#8fb6d6", 26, st="ital")]
    tr, td, tv = T("baymap", "random"), T("baymap", "drove"), T("baymap", "viewer described")
    tgt = min(POOL, key=lambda q: abs(math.hypot((q[0] - SRI_PT[0]) * 88, (q[1] - SRI_PT[1]) * 111) - 14) + (0 if q[1] < SRI_PT[1] else 3))
    gx, gy = BAYB.p(*tgt)
    els += [gl(gx, gy, 60, tr, .8), dot(gx, gy, 9, AU, tr), lab(gx + 18, gy - 22, "drawn at random", tr + .2, AU, 28, "start")]
    els += [ln([(sx, sy), ((sx + gx) / 2 + 30, (sy + gy) / 2 - 20), (gx, gy)], td - .2, AMBER, 4, dur=1.0, curve=True),
            rect(gx - 30, gy + 22, 60, 26, "#cbbca8", "#f5ecdc", 1.5, 8, td + .7, fx="pop"), circ(gx - 16, gy + 50, 7, "#2a2420", at=td + .7), circ(gx + 16, gy + 50, 7, "#2a2420", at=td + .7),
            lab(gx, gy + 90, "the team", td + .9, BONE, 28)]
    rx, ry = sx - 330, sy + 40
    els += [rect(rx - 110, ry - 70, 220, 140, "#1d2228", "#9aa4ae", 3, 8, tv - .4, fx="pop"),
            ppl(rx - 40, ry + 60, 100, tv - .2, "#a39a8e", fx="pop"), ppl(rx + 40, ry + 60, 100, tv - .1, "#8a96a2", fx="pop"),
            lab(rx, ry + 106, "shielded room", tv, BONE, 28)]
    arc = [(rx + 110 + (gx - rx - 110) * t, ry - 40 + (gy - ry + 40) * t - 120 * math.sin(math.pi * t)) for t in [k / 24 for k in range(25)]]
    els += dots_along(arc, tv + .3, 1.0, LILAC, 4)
    return {"base": "dark", "cam": CAM, "els": els}


def site_icon(kind, x, y, s, at, c=BONE):
    """Small pictures of local places, drawn in a few lines (illustrative)."""
    L = lambda pts, w=2.5: ln([(x + px * s, y + py * s) for px, py in pts], at, c, w, draw=False)
    if kind == "tower":
        return [L([(-10, 30), (-6, -30), (6, -30), (10, 30)]), L([(-14, -30), (0, -42), (14, -30)])]
    if kind == "boat":
        return [L([(-26, 14), (26, 14), (18, 26), (-18, 26), (-26, 14)]), L([(0, 14), (0, -32), (20, 6), (0, 6)])]
    if kind == "bridge":
        return [L([(-32, 0), (32, 0)]), {"k": "line", "p": R([(x - 30 * s, y + 24 * s), (x, y - 4 * s), (x + 30 * s, y + 24 * s)]), "c": c, "w": 2.5, "in": round(at, 2), "curve": True}]
    if kind == "church":
        return [L([(-18, 28), (-18, -4), (0, -22), (18, -4), (18, 28), (-18, 28)]), L([(0, -22), (0, -40)]), L([(-7, -33), (7, -33)])]
    if kind == "tree":
        return [L([(0, 28), (0, 4)]), circ(x, y - 8 * s, 18 * s, "none", c, 2.5, at)]
    if kind == "pool":
        return [L([(-28, -14), (28, -14), (28, 20), (-28, 20), (-28, -14)]), L([(-20, 2), (-10, -4), (0, 2), (10, -4), (20, 2)], 2)]
    if kind == "fountain":
        return [L([(-24, 16), (24, 16), (16, 28), (-16, 28), (-24, 16)]), L([(0, 16), (0, -18)]), {"k": "line", "p": R([(x - 18 * s, y + 10 * s), (x, y - 24 * s), (x + 18 * s, y + 10 * s)]),
                                                                                                    "c": c, "w": 2, "in": round(at, 2), "curve": True}]
    if kind == "plaza":
        return [L([(-26, -20), (26, -20), (26, 24), (-26, 24), (-26, -20)]), L([(-26, 2), (26, 2)], 1.5), L([(0, -20), (0, 24)], 1.5)]
    return [circ(x + dx * s, y + 10 * s, 6 * s, "none", c, 2, at) for dx in (-16, 0, 16)] + [L([(-24, 24), (24, 24)])]


SITES = ["tower", "boat", "bridge", "church", "tree", "pool", "fountain", "plaza", "garden"]


def sc_judging():
    """s27: nine transcripts at the left, nine sites at the right, a judge between them: lines run from every transcript to the judge
    and from the judge to every site; then a schematic of where the right site was ranked: guessing spreads the ranks anywhere from 1
    to 9, the star viewers' cluster near 1 (far better than chance)."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    ys = [168 + 66 * k for k in range(9)]
    for k, y in enumerate(ys):
        els += sheet(150, y - 26, 150, 52, -1, None, lines=2, seed=60 + k, lh=14)
        els += [card(1460, y - 28, 80, 56, -1, "#2a241d", "#6a5a48", fx=None)] + site_icon(SITES[k], 1500, y, .8, -1)
    els += [lab(225, 136, "transcripts", -1, BONE, 26), lab(1500, 136, "sites", -1, BONE, 26)]
    tj, tg, tb = T("judging", "judges visited"), T("judging", "only guessing"), T("judging", "star viewers")
    jx, jy = 889, 300
    for k, y in enumerate(ys):
        els.append(ln([(304, y), (jx - 30, jy)], round(tj + .1 + .06 * k, 2), AMBER, 1.6, dur=.5, op=.6))
        els.append(ln([(jx + 30, jy), (1456, y)], round(tj + .7 + .06 * k, 2), AMBER, 1.6, dur=.5, op=.6))
    els += [gl(jx, jy, 120, tj - .3, .3), ppl(jx, jy + 150, 210, tj - .3, "#cbbca8"), rect(jx + 20, jy - 10, 40, 54, "#c9a86a", "#6a5038", 2, 3, tj - .2),
            lab(jx, jy - 104, "a judge", tj, BONE, 28)]
    # the ranks, schematic: where the right site landed, 1 (best) to 9
    X = lambda r: 700 + (r - 1) * 60
    els += [rect(560, 520, 680, 250, "#120d0a", "#5a4a3c", 2, 10, tg - .5, fx="pop")]
    els += [lab(X(1), 562, "rank 1", tg - .3, MUTED, 24), lab(X(9), 562, "rank 9", tg - .3, MUTED, 24)]
    rnd = random.Random(3)
    guess = [rnd.randint(1, 9) for _ in range(9)]
    star = [1, 1, 2, 1, 3, 1, 2, 1, 1]
    seen = {}
    for k, r in enumerate(guess):
        n = seen.get(r, 0); seen[r] = n + 1
        els.append(dot(X(r), 618 - 14 * n, 7, "#9a9288", round(tg + .1 + .08 * k, 2)))
    els += [lab(670, 624, "guessing", tg, MUTED, 26, "end")]
    seen = {}
    for k, r in enumerate(star):
        n = seen.get(r, 0); seen[r] = n + 1
        els.append(dot(X(r) + 16 * n, 690, 7, AU, round(tb + .1 + .08 * k, 2)))
    els += [lab(670, 696, "star viewers", tb, AU, 26, "end"), lab(X(6) + 20, 696, "far better than chance", tb + .6, AU, 26),
            lab(X(5), 748, "schematic", tb + .4, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def lectern(x, at=-1):
    return [poly([(x - 150, 760), (x + 130, 760), (x + 80, 470), (x - 100, 470)], "#3a2c20", "#8a6a48", 2, at),
            poly([(x - 190, 470), (x + 170, 470), (x + 130, 420), (x - 150, 420)], "#4a3828", "#8a6a48", 2, at)]


def sc_ieee():
    """s28: a journal on the lectern, 'Proceedings of the IEEE', 'March 1976'; on an open page an arc between two places: over
    kilometre distances (from its title)."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(470, 360, 420, -1, .2), gl(1200, 450, 460, -1, .12)] + lectern(480)
    els += [rect(350, 170, 260, 300, "#1f3a5a", "#9fd0ff", 2, 4, .2, fx="rise"), ink(480, 230, "Proceedings", .3, "#f5ecdc", 34, st="serif"),
            ink(480, 268, "of the IEEE", .3, "#f5ecdc", 30, st="serif"), ln([(380, 296), (580, 296)], .3, "#9fd0ff", 2, draw=False, op=.7)] + \
           static(page_lines(385, 330, 190, 4, -1, 26, c="#9fc0e0", seed=19)) + [lab(480, 520, "March 1976", .5, BONE, 28)]
    px0, py0 = 860, 200
    els += [rect(px0, py0, 760, 500, "#efe6d2", "#cdbf9f", 1.5, 3, .6, fx="rise"), ln([(px0 + 380, py0 + 12), (px0 + 380, py0 + 488)], .7, "#cdbf9f", 2, draw=False)]
    els += [grp(page_lines(px0 + 40, py0 + 60, 300, 12, -1, 30, seed=23), .8, "rise")]
    ax, ay, bx_, by_ = px0 + 440, py0 + 360, px0 + 700, py0 + 300
    ta = T("ieee", "engineering")
    els += [dot(ax, ay, 8, GRAPH, ta - .4), dot(bx_, by_, 8, GRAPH, ta - .4),
            {"k": "line", "p": R([(ax, ay), ((ax + bx_) / 2, py0 + 150), (bx_, by_)]), "c": "#4b3d8f", "w": 3, "style": "claimed", "curve": True, "in": round(ta - .3, 2)},
            note(px0 + 570, py0 + 110, "over kilometre", ta, "#4b3d8f", 28), note(px0 + 570, py0 + 142, "distances", ta, "#4b3d8f", 28),
            note(px0 + 570, py0 + 440, "a perceptual channel?", ta + .4, "#6a5a48", 24)]
    return {"base": "dark", "cam": CAM, "els": els}


NZ_V = View(165.5, 179.5, -47.6, -34.2, (120, 150, 520, 560))


def sc_nz():
    """s29: New Zealand, Dunedin pinned (University of Otago); David Marks and Richard Kammann; their own results sit on the chance
    line: not repeated."""
    els = inset_map(NZ_V, 110, 140, 540, 580, -1, "#3a3024", "#12202a")
    dx, dy = NZ_V.p(170.50, -45.87)
    els += [{"k": "pin", "x": dx, "y": dy, "t": "Dunedin", "t2": "University of Otago", "c": GOLD, "in": T("nz", "New Zealand")}]
    tm, tk, tt, tr = T("nz", "David Marks"), T("nz", "Richard"), T("nz", "versions"), T("nz", "didn't repeat")
    els += [ppl(840, 700, 300, tm - .3, "#a39a8e"), lab(840, 360, "David Marks", tm, BONE, 28),
            ppl(1060, 700, 290, tk - .3, "#8a96a2"), lab(1060, 360, "Richard Kammann", tk, BONE, 28)]
    cx0, cy0, cw, ch = 1240, 300, 400, 300
    els += [rect(cx0, cy0, cw, ch, "rgba(18,13,10,.9)", "#5a4a3c", 2, 10, tt - .4, fx="pop"), ln([(cx0 + 20, cy0 + 170), (cx0 + cw - 20, cy0 + 170)], tt - .2, MUTED, 2, "inferred", .5),
            lab(cx0 + cw - 24, cy0 + 160, "chance", tt, MUTED, 24, "end")]
    for k, hgt in enumerate((92, 118, 104, 128, 96, 112)):
        els.append(rect(cx0 + 40 + 58 * k, cy0 + ch - 30 - hgt, 38, hgt, "#9a9288", at=round(tt + .1 * k, 2), fx="fill"))
    els += [lab(cx0 + cw / 2, cy0 + ch + 46, "not repeated", tr, BONE, 30), lab(cx0 + cw / 2, cy0 + ch + 80, "schematic", tr + .3, MUTED, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_clues():
    """s30: an unedited transcript; amber highlights pop: a date at the top, a line mentioning an earlier site; arrows lead to the list
    of sites in the order visited: clues to the order. Nature, 1978."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(600, 450, 520, -1, .12)]
    x0, y0, w, h = 300, 150, 620, 610
    els += [rect(x0 + 12, y0 + 14, w, h, "rgba(0,0,0,.5)", at=-1), rect(x0, y0, w, h, PAPER, PAPER_D, 1.5, 3, -1)]
    els += static(page_lines(x0 + 50, y0 + 120, w - 100, 15, -1, 30, seed=31))
    els += [note(x0 + 50, y0 + 70, "TRANSCRIPT", -1, TYPE, 26, "start", weight=700), note(x0 + w - 190, y0 + 70, "Date:", -1, TYPE, 24, "start"), ln([(x0 + w - 116, y0 + 72), (x0 + w - 50, y0 + 72)], -1, TYPE, 2, draw=False)]
    tu, tdt, tme, to = T("clues", "unedited"), T("clues", "dates"), T("clues", "mentions"), T("clues", "order")
    els += [lab(x0 + w / 2, y0 + h + 34, "unedited", tu, AMBER, 28)]
    els += [rect(x0 + w - 200, y0 + 44, 166, 40, "rgba(232,184,122,.35)", AMBER, 2.5, 4, tdt - .2, fx="pop"), lab(x0 + w + 40, y0 + 70, "a date", tdt, AMBER, 28, "start")]
    yl = y0 + 120 + 30 * 8
    els += [rect(x0 + 40, yl - 18, w - 80, 34, "rgba(232,184,122,.35)", AMBER, 2.5, 4, tme - .2, fx="pop"), lab(x0 + w + 40, yl + 8, "an earlier site", tme, AMBER, 28, "start")]
    lx0, ly0 = 1230, 300
    els += [rect(lx0, ly0, 380, 380, "rgba(18,13,10,.9)", "#5a4a3c", 2, 10, to - .6, fx="pop"), lab(lx0 + 190, ly0 - 20, "sites, in order", to - .4, BONE, 28)]
    for k in range(6):
        els += [lab(lx0 + 40, ly0 + 60 + 56 * k, str(k + 1), to - .4 + .1 * k, AU, 28, "start"), ln([(lx0 + 80, ly0 + 52 + 56 * k), (lx0 + 330, ly0 + 52 + 56 * k)], to - .4 + .1 * k, MUTED, 3, draw=False)]
    els += [arr([(x0 + w + 160, y0 + 64), (lx0 - 20, ly0 + 110)], to, AMBER, 3, dur=.6), arr([(x0 + w + 220, yl + 4), (lx0 - 20, ly0 + 166)], to + .2, AMBER, 3, dur=.6)]
    els += [lab(lx0 + 190, ly0 + 440, "clues to the order", to + .6, AMBER, 30)]
    els += [rect(1290, 160, 260, 50, "rgba(18,13,10,.9)", GOLD, 2, 25, tdt - .9, fx="pop"), lab(1420, 194, "Nature, 1978", tdt - .8, GOLD, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_quiz():
    """s31: a quiz sheet with ten questions; faint pencilled answers in its margin; a big score, 10/10, pops, then greys: it means far
    less."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(800, 450, 480, -1, .12)]
    x0, y0, w, h = 560, 150, 560, 610
    els += [rect(x0 + 12, y0 + 14, w, h, "rgba(0,0,0,.5)", at=-1), rect(x0, y0, w, h, PAPER, PAPER_D, 1.5, 3, -1), note(x0 + w / 2, y0 + 60, "QUIZ", -1, TYPE, 32, weight=700)]
    for k in range(10):
        y = y0 + 110 + 48 * k
        els += [note(x0 + 50, y + 8, "%d." % (k + 1), -1, TYPE, 24, "start"), ln([(x0 + 100, y), (x0 + w - 60, y)], -1, "#8a7a66", 3, draw=False),
                ln([(x0 + w - 200, y + 12), (x0 + w - 60, y + 12)], -1, "#bfb09c", 2, draw=False)]
    tp, ts, tl = T("quiz", "pencilled"), T("quiz", "high score"), T("quiz", "far less")
    for k in range(10):
        y = y0 + 110 + 48 * k
        els.append(ln([(x0 - 70, y + 4), (x0 - 54, y - 6), (x0 - 40, y + 2), (x0 - 26, y - 4)], round(tp + .06 * k, 2), "#7a7268", 2.5, dur=.25, curve=True))
    els += [lab(x0 - 50, y0 + h + 40, "answers in the margin", tp + .5, MUTED, 26)]
    els += [lab(1420, 470, "10/10", ts, AU, 110, st="serif", fx="pop"), gl(1420, 430, 160, ts, .4)]
    els += [veil(1250, 330, 340, 190, tl - .3, FLAT, .7, .8), lab(1420, 590, "means far less", tl, BONE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def letter_card(x, y, w, h, yr, t1, t2, at, c):
    return [card(x, y, w, h, at, "#2a241d", c), lab(x + 40, y + 76, yr, at + .1, c, 52, "start", st="serif"),
            lab(x + 40, y + 136, t1, at + .2, BONE, 30, "start"), lab(x + 40, y + 176, t2, at + .3, MUTED, 26, "start")]


def sc_letters():
    """s32: two letters as cards: 1980, still above chance (SRI's side); 1986, clues remain (the critics); an arrow each way; then a
    third card: Utts: some matches from clues alone."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    tc, tu = T("letters", "critics answered"), T("letters", "Even Jessica")
    els += letter_card(200, 230, 560, 220, "1980", "still above chance", "SRI's side, in Nature", .3, BLUE)
    els += letter_card(1020, 230, 560, 220, "1986", "clues remain", "the critics, in Nature", tc - .3, RED)
    els += [arr([(780, 300), (1000, 300)], tc - .1, MUTED, 3, dur=.5), arr([(1000, 380), (780, 380)], tc + .3, MUTED, 3, dur=.5)]
    els += [card(480, 540, 820, 190, tu - .3, "#2a241d", GREEN), lab(530, 610, "Jessica Utts, statistician:", tu, GREEN, 30, "start"),
            lab(530, 660, "some matches could be made", tu + .3, BONE, 30, "start"), lab(530, 702, "from clues in the transcripts alone", tu + .5, BONE, 30, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_uncanny():
    """s33: Marks and Kammann's own tests: at a site (a footbridge over a stream, trees) the viewer's description seems to fit, dotted
    lines join its words to the place ('uncanny'); the judge, a professor, ticks it ('convinced'); then the lines turn red: wrong sites."""
    els = [gl(1200, 420, 600, -1, .14)]
    # the site: stream, footbridge, trees
    els += [poly([(760, 640), (1700, 600), (1700, 700), (760, 740)], "#1d3a4a", "#5fa8c9", 2, -1, curve=True),
            {"k": "line", "p": R([(880, 640), (1180, 520), (1480, 620)]), "c": "#cbbca8", "w": 8, "in": -1, "curve": True},
            ln([(900, 640), (1460, 640)], -1, "#8a7a66", 3, draw=False)]
    for k in range(9):
        x = 960 + 60 * k
        y = 520 + 0.0017 * (x - 1180) ** 2 * 1.0
        els.append(ln([(x, min(632, y + 4)), (x, 640)], -1, "#8a7a66", 2, draw=False))
    els += tree(820, 600, 280, -1, "#2a3a26") + tree(1560, 600, 300, -1, "#2a3a26") + tree(1660, 610, 220, -1, "#22301f")
    els += [ln([(760, 600), (1700, 590)], -1, "#3a3024", 3, draw=False)]
    tu, tc, tw = T("uncanny", "uncanny"), T("uncanny", "convinced"), T("uncanny", "wrong sites")
    # the experimenters with the transcript
    els += [ppl(400, 720, 250, .3, "#a39a8e"), ppl(520, 720, 240, .4, "#8a96a2")]
    els += sheet(560, 430, 130, 170, .5, "pop", lines=5, seed=71, lh=24)
    fx_ = [(1180, 520), (840, 440), (1320, 676)]
    for k, (x, y) in enumerate(fx_):
        els.append({"k": "line", "p": R([(690, 470 + 40 * k), ((690 + x) / 2, (470 + 40 * k + y) / 2 - 40), (x, y)]), "c": LILAC, "w": 2.5, "style": "claimed", "curve": True,
                    "in": round(tu - .6 + .25 * k, 2)})
    els += [lab(1180, 330, "uncanny accuracy", tu + .2, LILAC, 30)]
    els += [ppl(230, 720, 230, tc - .5, "#cbbca8"), lab(230, 440, "a professor", tc - .3, BONE, 26), tick(230, 400, tc, GREEN, 1.4), lab(230, 360, "convinced", tc + .2, GREEN, 28)]
    for k, (x, y) in enumerate(fx_):
        els.append({"k": "line", "p": R([(690, 470 + 40 * k), ((690 + x) / 2, (470 + 40 * k + y) / 2 - 40), (x, y)]), "c": RED, "w": 3, "curve": True,
                    "in": round(tw - .3 + .15 * k, 2), "fx": "draw", "dur": .6})
    els += cross(1180, 520, tw + .3, RED, 2.2, 8) + [lab(1180, 230, "wrong sites", tw + .4, RED, 40, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def scene_city(x, y, at):
    return [rect(x - 150, y - 60, 300, 60, "#2f2822", "#8a7a66", 2, 2, at), rect(x - 30, y - 210, 60, 150, "#3a3129", "#cbbca8", 2, 2, at),
            poly([(x - 30, y - 210), (x, y - 250), (x + 30, y - 210)], "#3a3129", "#cbbca8", 2, at),
            ln([(x + 80, y - 6), (x + 80, y - 50)], at, "#9fd0ff", 3, draw=False), {"k": "line", "p": R([(x + 60, y - 30), (x + 80, y - 56), (x + 100, y - 30)]), "c": "#9fd0ff", "w": 2.5, "in": round(at, 2), "curve": True},
            rect(x - 130, y - 30, 60, 22, "#9a4a3a", at=at), circ(x - 118, y - 6, 7, "#15110d", at=at), circ(x - 82, y - 6, 7, "#15110d", at=at),
            ln([(x - 160, y - 18), (x - 140, y - 18)], at, MUTED, 2, draw=False), ln([(x - 166, y - 28), (x - 142, y - 28)], at, MUTED, 2, draw=False)]


def scene_harbour(x, y, at):
    return [rect(x - 150, y - 50, 300, 50, "#1d3a4a", at=at), ln([(x - 150, y - 50), (x + 150, y - 50)], at, "#5fa8c9", 2, draw=False),
            ln([(x - 100, y - 50), (x - 100, y - 230), (x + 20, y - 230)], at, "#cbbca8", 5, draw=False), ln([(x - 100, y - 190), (x - 60, y - 230)], at, "#cbbca8", 3, draw=False),
            ln([(x, y - 230), (x, y - 160)], at, "#cbbca8", 2, draw=False),
            poly([(x + 40, y - 56), (x + 130, y - 56), (x + 116, y - 36), (x + 54, y - 36)], "#cbbca8", at=at), ln([(x + 84, y - 56), (x + 84, y - 130)], at, "#cbbca8", 3, draw=False),
            poly([(x + 86, y - 128), (x + 120, y - 66), (x + 86, y - 66)], "#efe6d2", at=at)]


def scene_park(x, y, at):
    return [rect(x - 150, y - 26, 300, 26, "#2a3a26", at=at)] + tree(x - 70, y - 20, 220, at, "#3a5a34") + \
           [poly(E(x + 70, y - 34, 70, 16, 24), "#1d3a4a", "#5fa8c9", 2, at)] + \
           [ln([(x + 10 + 30 * k, y - 120 - 12 * k), (x + 60 + 30 * k, y - 126 - 12 * k)], at, "#9a9288", 2.5, draw=False) for k in range(3)]


def sc_anywhere():
    """s34: three words as pictures: something tall, some water, movement; three very different places each get three ticks: subjective
    validation."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    tt, tw, tm = T("anywhere", "tall"), T("anywhere", "water"), T("anywhere", "movement")
    els += [ln([(470, 270), (470, 150)], tt, BONE, 6, dur=.4), lab(470, 320, "something tall", tt + .1, BONE, 28)]
    els += [ln([(840 + 20 * k, 210 + (8 if k % 2 else -8)) for k in range(9)], tw, "#9fd0ff", 4, dur=.5, curve=True),
            ln([(840 + 20 * k, 240 + (8 if k % 2 else -8)) for k in range(9)], tw + .1, "#9fd0ff", 4, dur=.5, curve=True), lab(920, 320, "some water", tw + .1, BONE, 28)]
    els += [ln([(1240, 190 + 26 * k), (1340 - 14 * k, 190 + 26 * k)], tm + .08 * k, LILAC, 4, dur=.3) for k in range(3)] + [lab(1300, 320, "movement", tm + .1, BONE, 28)]
    ta = T("anywhere", "all three")
    for k, (fn, x) in enumerate(((scene_city, 330), (scene_harbour, 889), (scene_park, 1450))):
        els += [rect(x - 190, 400, 380, 300, "rgba(18,13,10,.85)", "#5a4a3c", 2, 12, .4 + .2 * k, fx="pop")] + fn(x, 650, .5 + .2 * k)
        for j in range(3):
            els.append(tick(x - 60 + 60 * j, 372, round(ta + .3 * k + .1 * j, 2), GREEN, 1.0))
    els += [lab(889, 770, "subjective validation", T("anywhere", "subjective"), AU, 34, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 4: the review of 1995
def sc_review():
    """s36: Congress sends the programme to the CIA, which orders the review: a report rises, 'An Evaluation of Remote Viewing', AIR,
    29 September 1995; two tabs: the lab? the field?"""
    els = [gl(560, 470, 520, -1, .12), gl(1370, 430, 420, -1, .14)]
    tc, ta = T("review", "Congress"), T("review", "outside review")
    els += building(290, 640, 300, -1, "dome") + [lab(290, 700, "Congress", -1, BONE, 30)]
    els += building(760, 640, 200, tc + .3, "hq") + [lab(760, 700, "CIA", tc + .4, BONE, 30)]
    els += [arr([(450, 520), (590, 520)], tc + .1, AMBER, 4, dur=.5), arr([(930, 520), (1100, 520)], ta - .2, AMBER, 4, dur=.5)]
    lines = [("AN EVALUATION OF", 92, 26, 700), ("REMOTE VIEWING", 128, 26, 700), ("Research and Applications", 168, 24, None),
             ("American Institutes", 466, 24, None), ("for Research", 496, 24, None), ("29 September 1995", 548, 24, None)]
    els += report_cover(1150, 150, 400, 600, ta, lines, body=0, seed=81) + page_lines(1200, 380, 300, 3, ta + .3, 26, seed=81)
    tl, tf = T("review", "in the lab"), T("review", "in the field")
    els += [rect(1550, 250, 150, 50, BLUE, at=tl - .2, fx="pop", r=6), note(1625, 284, "the lab?", tl, "#0d1824", 26, weight=700),
            rect(1550, 330, 150, 50, AMBER, at=tf - .2, fx="pop", r=6), note(1625, 364, "the field?", tf, "#241a10", 26, weight=700)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_experts():
    """s37: a long table under a lamp: Jessica Utts (statistician, a bar chart) and Ray Hyman (psychologist, a head in profile), a
    stack of lab reports between them; then their tags: found the data convincing; a well-known sceptic."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)] + lamp(889, 250, -1, cord=130, op=.6, r=420) + [cone(889, 266, 60, 900, 640, -1, .06)]
    els += table(889, 610, 1000, -1, h=120)
    tu, th, tc, ts = T("experts", "Jessica"), T("experts", "Ray"), T("experts", "convincing"), T("experts", "sceptic")
    els += seated_figure(520, 730, 320, tu - .3, "#a39a8e", 1) + seated_figure(1260, 730, 320, th - .3, "#8a96a2", -1)
    for k in range(5):
        els += sheet(820 + 6 * k, 520 - 14 * k, 150, 90, -1, None, lines=2, seed=90 + k, lh=18)
    els += [rect(560, 470, 130, 120, "rgba(18,13,10,.9)", GREEN, 2, 8, tu + .2, fx="pop")] + \
           [rect(580 + 26 * j, 570 - 22 * (j + 1), 18, 22 * (j + 1), GREEN, at=round(tu + .3 + .1 * j, 2), fx="fill") for j in range(4)]
    els += [rect(1090, 470, 130, 120, "rgba(18,13,10,.9)", AMBER, 2, 8, th + .2, fx="pop"), head(1155, 532, 90, th + .3, "#2a2420", "rgba(232,184,122,.7)", 2, face=-1)]
    els += [lab(520, 300, "Jessica Utts", tu, BONE, 30), lab(520, 336, "statistician", tu + .3, MUTED, 26),
            lab(1260, 300, "Ray Hyman", th, BONE, 30), lab(1260, 336, "psychologist", th + .3, MUTED, 26)]
    els += [lab(520, 384, "found the data convincing", tc, GREEN, 26), lab(1260, 384, "a well-known sceptic", ts, AMBER, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def photo(x, y, w, h, kind, at, rim="#6a5a48"):
    els = [rect(x, y, w, h, "#e8dcc4", rim, 3, 3, at, fx="pop"), rect(x + 10, y + 10, w - 20, h - 20, "#3a4a5a", at=at, fx="pop")]
    gx, gy, gw, gh = x + 10, y + 10, w - 20, h - 20
    b = gy + gh
    if kind == 0:
        els += [poly([(gx, b), (gx + gw * .35, gy + gh * .3), (gx + gw * .6, gy + gh * .6), (gx + gw * .8, gy + gh * .35), (gx + gw, b)], "#6a7a6a", at=at, fx="pop")]
    elif kind == 1:
        els += [rect(gx + gw * (.08 + .17 * k), b - gh * (.3 + .12 * (k % 3)), gw * .13, gh * (.3 + .12 * (k % 3)), "#1d2630", at=at, fx="pop") for k in range(5)]
    elif kind == 2:
        els += [rect(gx, b - gh * .25, gw, gh * .25, "#2a5a7a", at=at, fx="pop"), {"k": "line", "p": R([(gx, b - gh * .25), (gx + gw / 2, gy + gh * .3), (gx + gw, b - gh * .25)]),
                                                                                    "c": "#c9a86a", "w": 4, "curve": True, "in": round(at, 2)}]
    elif kind == 3:
        els += [rect(gx, b - gh * .3, gw, gh * .3, "#2a5a7a", at=at, fx="pop")] + tree(gx + gw * .3, b - gh * .25, gh * .6, at, "#2a3a26")
    else:
        els += [rect(gx + gw * .44, gy + gh * .2, gw * .12, gh * .8, "#c9bfae", at=at, fx="pop"), poly([(gx + gw * .44, gy + gh * .2), (gx + gw * .5, gy + gh * .05), (gx + gw * .56, gy + gh * .2)], "#c9bfae", at=at)]
    return els


def sc_five():
    """s38: the viewer's description and five photographs: one gets a gold rim (the real target), four a grey tag (decoys); a strip of
    five squares where one lights: 1 in 5 by chance."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    els += sheet(110, 230, 220, 280, -1, None, lines=7, seed=95, lh=30) + [lab(220, 560, "the description", -1, BONE, 26)]
    tp, tr, tdc, t5 = T("five", "five photographs"), T("five", "one real"), T("five", "decoys"), T("five", "one time in")
    xs = [400 + 252 * k for k in range(5)]
    for k, x in enumerate(xs):
        els += [rect(x, 250, 220, 170, "none", MUTED, 2, 3, round(.4 + .08 * k, 2), style="inferred", op=.6)]
        els += photo(x, 250, 220, 170, k, round(tp - .3 + .12 * k, 2))
    els += [rect(xs[2] - 8, 242, 236, 186, "none", AU, 5, 6, tr, fx="pop"), gl(xs[2] + 110, 335, 170, tr, .4), lab(xs[2] + 110, 470, "the real target", tr + .2, AU, 28)]
    for k in (0, 1, 3, 4):
        els += [rect(xs[k] + 62, 438, 96, 36, "#5a5048", at=round(tdc + .1 * k, 2), fx="pop", r=6), lab(xs[k] + 110, 464, "decoy", round(tdc + .1 * k, 2), BONE, 24)]
    els += [rect(700 + 84 * k, 600, 70, 70, AU if k == 2 else "#3a332c", "#8a7a66", 2, 6, round(t5 - .4 + .1 * k, 2), fx="pop") for k in range(5)]
    els += [lab(889, 720, "1 in 5 by chance", t5 + .3, AU, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_agree():
    """s39 (first framing): a chart: the chance line dashed; a row of bars just above it (schematic: a small, steady effect); a bracket
    'not flukes', two ticks (both experts agree); over 1,000 sessions. At the right, two empty chips wait."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    x0, x1, base, chance = 140, 820, 700, 520
    els += [ln([(x0, base), (x1, base)], -1, MUTED, 2, draw=False), ln([(x0, base), (x0, 300)], -1, MUTED, 2, draw=False),
            ln([(x0, chance), (x1 + 60, chance)], .3, BONE, 2.5, "inferred", .8), lab(x1 + 70, chance + 9, "chance", .6, MUTED, 26, "start")]
    ta, tf, ts = T("agree", "agreed"), T("agree", "flukes"), T("agree", "thousand")
    hs = [192, 196, 188, 200, 194, 198, 190, 197, 193, 199]
    for k, hgt in enumerate(hs):
        els.append(rect(x0 + 30 + 64 * k, base - hgt, 40, hgt, AMBER, at=round(ta - .4 + .08 * k, 2), fx="fill", op=.85))
    els += [ln([(x0 + 26, 470), (x0 + 26, 452), (x1 - 40, 452), (x1 - 40, 470)], tf - .5, GOLD, 3, dur=.6), lab((x0 + x1) / 2 - 10, 430, "not flukes", tf - .2, GOLD, 30),
            tick((x0 + x1) / 2 - 150, 380, tf + .1, GREEN, 1.1), tick((x0 + x1) / 2 + 130, 380, tf + .3, GREEN, 1.1),
            lab((x0 + x1) / 2 - 150, 350, "Utts", tf + .1, MUTED, 24), lab((x0 + x1) / 2 + 130, 350, "Hyman", tf + .3, MUTED, 24)]
    els += [lab((x0 + x1) / 2, 752, "a small effect over 1,000 sessions, schematic", ts, BONE, 26)]
    els += [rect(1000, 250, 300, 80, "none", MUTED, 2, 40, .8, style="inferred", op=.5), rect(1350, 250, 300, 80, "none", MUTED, 2, 40, .8, style="inferred", op=.5)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_split():
    """s39 (second beat): Utts' chip, well established (green); Hyman's, premature (amber); under it one lab solid and three dashed:
    no independent repeat."""
    tu, th, ti = T("split", "Utts concluded"), T("split", "premature"), T("split", "independent")
    els = chip(1150, 290, "well established", GREEN, tu + .2, 28) + [lab(1150, 380, "Utts", tu + .3, GREEN, 28)]
    els += chip(1500, 290, "premature", AMBER, th, 28) + [lab(1500, 380, "Hyman", th + .1, AMBER, 28)]
    for k in range(4):
        x = 1150 + 116 * k
        solid = k == 0
        els += [rect(x - 44, 540, 88, 96, "#2f2822" if solid else "none", "#cbbca8", 2, 3, round(ti - .4 + .15 * k, 2), style="known" if solid else "inferred", fx="pop"),
                poly([(x - 54, 540), (x, 498), (x + 54, 540)], "#2f2822" if solid else "none", "#cbbca8", 2, round(ti - .4 + .15 * k, 2), style="known" if solid else "inferred")]
    els += [lab(1325, 690, "no independent repeat", ti + .4, BONE, 28)]
    return els


def sc_branches():
    """s40: the report sheet with 'statistically significant' lit; from a lilac '?' four branches: the viewers? the judges? the
    targets? the methods?"""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    els += [rect(172, 214, 400, 520, "rgba(0,0,0,.45)", at=-1), rect(160, 200, 400, 520, PAPER, PAPER_D, 1.5, 3, -1)]
    els += static(page_lines(200, 260, 320, 13, -1, 34, seed=101))
    tsg, tv, tj, tt, tm = T("branches", "statistically"), T("branches", "the viewers"), T("branches", "the judges"), T("branches", "the targets"), T("branches", "the methods")
    els += [rect(190, 380, 340, 40, "rgba(232,184,122,.35)", AMBER, 2.5, 4, tsg - .3, fx="pop"), lab(360, 770, "statistically significant", tsg, AMBER, 28)]
    els += qmark(760, 500, tsg + 1.2, 110)
    for (t, y, at, icon) in (("the viewers?", 230, tv, "head"), ("the judges?", 390, tj, "judge"), ("the targets?", 550, tt, "photo"), ("the methods?", 710, tm, "gear")):
        els.append({"k": "line", "p": R([(800, 470), (930, y - 10), (1080, y - 10)]), "c": LILAC, "w": 2.5, "style": "claimed", "curve": True, "in": round(at - .3, 2)})
        els += [lab(1260, y, t, at, BONE, 30, "start")]
        if icon == "head":
            els += [head(1170, y - 18, 80, at, "#2a2420", "rgba(201,193,238,.7)", 2, fx="pop")]
        elif icon == "judge":
            els += [ppl(1170, y + 18, 80, at, "#cbbca8", fx="pop")]
        elif icon == "photo":
            els += [rect(1130, y - 46, 80, 60, "#e8dcc4", "#6a5a48", 2, 3, at, fx="pop"), rect(1138, y - 38, 64, 44, "#3a4a5a", at=at, fx="pop")]
        else:
            els += [circ(1170, y - 16, 26, "none", "#cbbca8", 6, at, style="inferred"), circ(1170, y - 16, 10, "#cbbca8", at=at)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_users():
    """s41: the agencies' people at a table receive reports; each report has two grades, accuracy and value (from 1994); then two
    meters: broad background partly right, concrete detail empty."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(420, 460, 420, -1, .12)]
    tu, tg, tb, tc = T("users", "useful"), T("users", "grade"), T("users", "broad"), T("users", "concrete")
    for k, x in enumerate((230, 400, 570)):
        els += [ppl(x, 720, 300, -1, ("#8a96a2", "#a39a8e", "#7d766c")[k])]
    els += table(400, 600, 600, -1, h=150)
    els += [lab(400, 360, "the agencies", -1, BONE, 28)]
    els += [rect(760, 210, 330, 470, PAPER, PAPER_D, 1.5, 3, tg - .6, fx="rise"), note(925, 260, "REPORT", tg - .5, TYPE, 28, weight=700)]
    els += [grp(page_lines(790, 300, 270, 4, -1, 28, seed=111), tg - .4, "rise")]
    for k, t in enumerate(("accuracy", "value")):
        y = 470 + 90 * k
        els += [note(790, y + 10, t, tg + .2 * k, TYPE, 26, "start")] + [rect(930 + 28 * j, y - 14, 22, 22, "none", TYPE, 2, 3, round(tg + .2 * k + .05 * j, 2), fx="pop") for j in range(5)]
    els += [lab(925, 720, "graded, from 1994", tg + .4, MUTED, 26)]
    mx0 = 1230
    els += [lab(mx0, 300, "broad background", tb, BONE, 28, "start"), rect(mx0, 330, 400, 50, "none", AMBER, 2, 25, tb - .1, fx="pop"),
            bar(mx0 + 25, mx0 + 25 + 190, 355, 36, tb + .2, AMBER, .8)]
    els += [lab(mx0, 520, "concrete detail", tc, BONE, 28, "start"), rect(mx0, 550, 400, 50, "none", MUTED, 2, 25, tc - .1, fx="pop", style="inferred"),
            lab(mx0 + 200, 586, "?", tc + .4, MUTED, 34, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_vague():
    """s42: a report whose lines blur under a fog; a red stamp, VAGUE AND AMBIGUOUS; a big 0: intelligence operations guided."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    els += [rect(332, 184, 480, 560, "rgba(0,0,0,.45)", at=-1), rect(320, 170, 480, 560, PAPER, PAPER_D, 1.5, 3, -1), note(560, 230, "EVALUATION, 1995", -1, TYPE, 26, weight=700)]
    els += static(page_lines(360, 290, 400, 12, -1, 34, seed=121))
    tv, tn = T("vague", "vague"), T("vague", "In no case")
    els += [{"k": "glow", "x": 560, "y": 470, "r": 300, "kind": "lamp", "op": .55, "keepop": True, "in": round(tv - .8, 2), "dur": 1.2},
            rect(320, 170, 480, 560, "rgba(239,230,210,.55)", at=tv - .6, op=1)]
    els += [stamp(560, 470, "VAGUE AND AMBIGUOUS", tv, STAMP, 34, rot=-8)]
    els += [lab(1300, 540, "0", tn, BONE, 260, st="serif", fx="pop"), lab(1300, 620, "intelligence operations", tn + .4, BONE, 30),
            lab(1300, 656, "guided by it", tn + .4, BONE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_lightsout():
    """s43: the barracks inside: two rows of desks, three with a viewer under a lit lamp; the lamps go out one by one; 1995; a folder
    stamped DECLASSIFIED."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), rect(110, 140, 1560, 640, "#261d15", "#4a3a2c", 2, 6, -1), gl(889, 470, 700, -1, .1)]
    t3, tsd, tdc = T("lightsout", "three viewers"), T("lightsout", "shut down"), T("lightsout", "declassified")
    rows = [(430, .72, [330, 610, 890, 1170]), (650, 1.0, [300, 640, 980])]
    occ = [(0, 1), (0, 3), (1, 1)]
    k = 0
    for r_, (y, sc_, xs) in enumerate(rows):
        for j, x in enumerate(xs):
            w = 230 * sc_
            lx, ly = x + w * .32, y - 70 * sc_
            if (r_, j) in occ:
                els += [ppl(x - w * .12, y + 64 * sc_, 200 * sc_, -1, "#a39a8e")]
            els += [rect(x - w / 2, y - 16 * sc_, w, 16 * sc_, "#6a5038", "#9a7a58", 1.5, 2, -1), rect(x - w / 2 + 10, y, 10 * sc_, 70 * sc_, "#4a3a2a", at=-1),
                    rect(x + w / 2 - 20, y, 10 * sc_, 70 * sc_, "#4a3a2a", at=-1),
                    ln([(lx, y - 16 * sc_), (lx, ly)], -1, "#6a5a48", 2.5, draw=False),
                    poly([(lx - 18 * sc_, ly + 10 * sc_), (lx + 18 * sc_, ly + 10 * sc_), (lx + 9 * sc_, ly - 8 * sc_), (lx - 9 * sc_, ly - 8 * sc_)], "#3a3129", at=-1)]
            if (r_, j) in occ:
                n = occ.index((r_, j))
                els += [gl(lx, ly + 24 * sc_, 150 * sc_, round(t3 - .3 + .25 * n, 2), .75), circ(lx, ly + 12 * sc_, 5 * sc_, "#fff1d2", at=round(t3 - .3 + .25 * n, 2))]
    els += [veil(111, 141, 1558, 638, tsd - .2, "#140f0b", .72, 2.0, r=6)]
    els += [lab(889, 210, "three viewers", t3 + .5, BONE, 30), lab(1460, 380, "1995", tsd + .4, GOLD, 40, st="serif")]
    els += [folder(1320, 520, 300, 180, tdc - .4, MANILA, fx="pop"), stamp(1470, 616, "DECLASSIFIED", tdc, STAMP, 28, rot=-6)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_objection():
    """s44: a time line 1972 to 1995 with a lens over only its last stretch (the final operations); Edwin May, dotted: not
    representative; Joseph McMoneagle, dotted: defended it."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1)]
    X = lambda y: round(200 + (y - 1972) * 1380 / 23, 1)
    els += [axis(200, 1580, 660, [(X(1972), "1972"), (X(1995), "1995")], .2), {"k": "band", "x0": X(1972), "x1": X(1995), "y": 640, "h": 12, "c": "#5a4a3c", "in": .3}]
    tm, tf, tj = T("objection", "Edwin"), T("objection", "final operations"), T("objection", "Joseph")
    lx_ = X(1994.2)
    els += [circ(lx_, 646, 80, "rgba(159,208,255,.10)", "#cfe6ff", 5, tf - .4, fx="pop"), ln([(lx_ + 56, 702), (lx_ + 110, 772)], tf - .3, "#cfe6ff", 10, draw=False),
            lab(lx_ - 10, 540, "final operations", tf, BLUE, 28, "end")]
    els += [ppl(420, 560, 260, tm - .3, "#a39a8e"), rect(240, 160, 420, 110, "rgba(18,13,10,.9)", AMBER, 2, 14, tm + .2, fx="pop", style="claimed"),
            lab(450, 206, "Edwin May:", tm + .3, AMBER, 28), lab(450, 246, "not representative", tm + .4, BONE, 28)]
    els += [ppl(900, 560, 260, tj - .3, OLIVE), rect(720, 160, 420, 110, "rgba(18,13,10,.9)", AMBER, 2, 14, tj + .2, fx="pop", style="claimed"),
            lab(930, 206, "Joseph McMoneagle:", tj + .3, AMBER, 28), lab(930, 246, "defended it", tj + .4, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_online():
    """s45: stacks of pages rising: over 12 million pages, January 2017; a laptop's screen glows with the crane sketch: Star Gate
    files."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(1300, 450, 520, -1, .12)]
    tp, tl, tr = T("online", "twelve million"), T("online", "Star Gate files"), T("online", "Anyone")
    for k in range(7):
        h = 220 + 60 * ((k * 3) % 5)
        x = 140 + 110 * k
        els += [rect(x, 700 - h, 90, h, "#d8ccb2", "#8a7a66", 1.5, 2, round(.4 + .2 * k, 2), fx="fill")]
        els += [ln([(x + 4, 700 - h + 14 * j), (x + 86, 700 - h + 14 * j)], round(.8 + .2 * k, 2), "#a8987c", 1.2, draw=False) for j in range(1, int(h / 14))]
    els += [lab(520, 160, "over 12 million pages", tp + .3, BONE, 32), lab(520, 750, "online, January 2017", tp + .6, MUTED, 28)]
    lx0, ly0 = 1060, 250
    els += [rect(lx0, ly0, 500, 320, "#1a1f26", "#9aa4ae", 3, 10, tl - .6, fx="rise"), rect(lx0 + 16, ly0 + 16, 468, 288, "#efe6d2", at=tl - .4),
            poly([(lx0 - 50, ly0 + 330), (lx0 + 550, ly0 + 330), (lx0 + 510, ly0 + 380), (lx0 - 10, ly0 + 380)], "#3a3f45", "#9aa4ae", 2, tl - .6)]
    cr, _ = crane(lx0 + 250, ly0 + 240, .3, tl - .2)
    els += [grp(cr, tl - .2, "pop")]
    els += [gl(lx0 + 250, ly0 + 160, 320, tl, .25), lab(lx0 + 250, ly0 + 440, "the Star Gate files", tl + .2, GOLD, 30)]
    els += [lab(lx0 + 250, ly0 + 486, "sessions, sketches, verdicts", tr + .3, MUTED, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== chapter 5: the weighing
ROWS3 = [255, 435, 615]


def ledger_row3(k, t, at, icon):
    y = ROWS3[k]
    return [rect(130, y - 70, 1520, 140, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(330, y + 11, t, at + .1, BONE, 32, "start")] + icon(230, y, at)


def icon_folder(x, y, at):
    return [folder(x - 44, y - 26, 88, 60, at, MANILA, fx="pop")]


def icon_crane(x, y, at):
    cr, _ = crane(x, y + 24, .1, at, "plan", w=1.6, col=GOLD)
    return [grp(cr, at, "pop")]


def icon_chart(x, y, at):
    return [ln([(x - 40, y + 30), (x + 40, y + 30)], at, MUTED, 2, draw=False), ln([(x - 40, y - 6), (x + 40, y - 6)], at, BONE, 2, "inferred", draw=False)] + \
           [rect(x - 34 + 18 * j, y - 12 - 4 * (j % 2), 12, 42 + 4 * (j % 2), AMBER, at=at) for j in range(4)]


def sc_ledger():
    """s46: the ledger: row 1, the programme existed, its chip Established; a note: the crane, called accurate; but one match can't tell
    insight from luck. Rows 2 and 3 wait, dashed."""
    els = [rect(110, 150, 1560, 620, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += [rect(130, y - 70, 1520, 140, "none", "rgba(242,201,142,.16)", 1.5, 12, .5, style="inferred") for y in ROWS3[1:]]
    t1, te, tc, tl = T("ledger", "The programme itself"), T("ledger", "Established"), T("ledger", "So is the crane"), T("ledger", "luck")
    els += ledger_row3(0, "the programme existed", t1, icon_folder)
    els += chip(1260, ROWS3[0] - 14, "Established", GRADE["established"], te, 30, a="start")
    els += [lab(330, ROWS3[0] + 50, "and the crane: called accurate", tc, GREEN, 24, "start"), lab(1260, ROWS3[0] + 50, "insight or luck?", tl - .2, LILAC, 24, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def add_ledger2():
    """s47: rows 2 and 3 as named: reliable intelligence, Ruled out; a psychic effect in the lab, Awaiting evidence."""
    tr, tro, tp, ta = T("ledger2", "reliable"), T("ledger2", "Ruled"), T("ledger2", "A psychic effect"), T("ledger2", "Awaiting")
    els = ledger_row3(1, "reliable intelligence", tr, icon_crane) + chip(1260, ROWS3[1], "Ruled out", GRADE["ruled"], tro, 30, a="start")
    els += ledger_row3(2, "a psychic effect in the lab", tp, icon_chart) + chip(1260, ROWS3[2], "Awaiting evidence", GRADE["awaiting"], ta, 30, a="start")
    return els


def sc_people():
    """s48: a row of quiet figures in warm light (physicists, soldiers, analysts); some say, in public, that it worked (dotted); then in
    front of them a blind test: a viewer, a screen, a sealed target."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), gl(889, 360, 760, -1, .16)]
    cols = ["#a39a8e", OLIVE, "#8a96a2", "#a39a8e", "#7d766c", OLIVE, "#a39a8e", "#8a96a2"]
    xs = [230 + 190 * k for k in range(8)]
    for k, x in enumerate(xs):
        els.append(ppl(x, 470, 220 + 16 * ((k * 5) % 3), round(.2 + .08 * k, 2), cols[k], fx="fade", op=.75))
    tsp, th, tb = T("people", "said in public"), T("people", "honest"), T("people", "blind tests")
    for k, x in enumerate((xs[1], xs[4], xs[6])):
        els += [rect(x - 80, 150, 160, 54, "rgba(18,13,10,.85)", LILAC, 2, 27, round(tsp + .2 * k, 2), fx="pop", style="claimed"),
                lab(x, 186, "it worked", round(tsp + .1 + .2 * k, 2), LILAC, 24)]
    els += [lab(889, 530, "honest, clever people", th, BONE, 28)]
    els += seated_figure(660, 770, 190, tb - .5, "#cbbca8", 1)
    els += [rect(840, 590, 40, 180, "#3a3129", "#8a6a48", 2, 4, tb - .4, fx="rise"), rect(990, 690, 110, 80, PAPER, PAPER_D, 1.5, 3, tb - .3, fx="pop"),
            ln([(990, 690), (1045, 725), (1100, 690)], tb - .3, "#9a8a70", 2, draw=False), circ(1045, 728, 10, STAMP, at=tb - .2)]
    els += [lab(1150, 742, "a blind test", tb + .2, AU, 30, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_test():
    """s49: three tests not yet done (dashed): nobody near knows the target; the scoring written down first; sceptical labs repeat it;
    then a sealed prediction, opened later."""
    els = [rect(-20, -20, 1820, 1040, FLAT, at=-1), lab(889, 200, "?", 1.0, LILAC, 64, st="serif", fx="pop")]
    tn, tw, tr, tsl = T("test", "nobody near"), T("test", "written down"), T("test", "sceptical labs"), T("test", "sealed prediction")
    P1, P2, P3 = 150, 670, 1190
    els += [rect(P1, 250, 440, 330, "none", BONE, 2.5, 12, tn - .3, style="inferred", fx="pop"), rect(P1 + 290, 380, 30, 180, "#3a3129", BONE, 2, 3, tn - .1, style="inferred"),
            rect(P1 + 340, 470, 70, 50, PAPER, PAPER_D, 1.5, 3, tn), circ(P1 + 375, 497, 8, STAMP, at=tn)]
    els += [ppl(P1 + 120, 560, 150, tn, "#cbbca8", fx="fade"), lab(P1 + 220, 630, "nobody near knows", tn + .3, BONE, 28)]
    els += [rect(P2, 250, 440, 330, "none", BONE, 2.5, 12, tw - .3, style="inferred", fx="pop"), rect(P2 + 140, 300, 160, 210, PAPER, PAPER_D, 1.5, 3, tw - .1, fx="rise")]
    els += [grp(page_lines(P2 + 160, 340, 120, 5, -1, 24, seed=131), tw, "rise"),
            rect(P2 + 270, 450, 60, 50, AU, "#8a6420", 2, 6, tw + .3, fx="pop"), ln([(P2 + 282, 452), (P2 + 282, 428), (P2 + 300, 414), (P2 + 318, 428), (P2 + 318, 452)], tw + .3, AU, 5, draw=False, curve=True),
            lab(P2 + 220, 630, "scoring set first", tw + .3, BONE, 28)]
    els += [rect(P3, 250, 440, 330, "none", BONE, 2.5, 12, tr - .3, style="inferred", fx="pop")]
    for k in range(3):
        x = P3 + 90 + 130 * k
        els += [rect(x - 40, 420, 80, 90, "#2f2822", "#cbbca8", 2, 3, round(tr + .15 * k, 2), fx="pop"), poly([(x - 50, 420), (x, 384), (x + 50, 420)], "#2f2822", "#cbbca8", 2, round(tr + .15 * k, 2)),
                {"k": "line", "p": R([(x - 18, 340), (x - 6, 352), (x + 20, 322)]), "c": GREEN, "w": 5, "style": "inferred", "in": round(tr + .4 + .15 * k, 2)}]
    els += [lab(P3 + 220, 630, "sceptical labs repeat", tr + .5, BONE, 28)]
    els += [rect(780, 690, 150, 92, PAPER, PAPER_D, 1.5, 3, tsl - .3, fx="pop"), ln([(780, 690), (855, 740), (930, 690)], tsl - .3, "#9a8a70", 2, draw=False),
            circ(855, 744, 14, STAMP, at=tsl - .2), lab(980, 750, "a sealed prediction, opened later", tsl + .2, AU, 28, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_close():
    """s50: the desk of the opening, at night: the crane sketch on top of a deep stack of other session sheets; the lamp lowers."""
    els = desk_bg()
    els += [gl(1000, 430, 700, -1, .28)]
    for k in range(18):
        x = 520 - 6 * k + (k % 3) * 4
        y = 230 + 5 * k
        els.append(rect(x, y, 960, 520, "#d8ccb2" if k % 2 else "#cfc2a6", "#a8987c", 1, 3, -1, op=round(.35 + .03 * k, 2)))
    x, y, w, h = 560, 190, 960, 520
    els += [rect(x + 14, y + 16, w, h, "rgba(0,0,0,.5)", at=-1), rect(x, y, w, h, "#efe6d2", "#fff6e2", 1.5, 3, -1)]
    cr, _ = crane(x + w / 2, y + h - 70, .66)
    els += cr
    tr = T("close", "everybody remembers")
    els += [veil(-20, -20, 1820, 1040, tr - .4, "#0d0b09", .3, 2.5)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "hero", [(0, "It stands at", "globe"), (1, "He has been given", "axles"), (2, "The CIA compares", "compare"), (3, "Can a mind", "mind")], {}),
    (0, 1, "title", "mind", [], {"intro": True}),
    (1, 0, "world", "report", [(0, "Soviet knowledge", "balance")], {"chapter": "The psychic arms race"}),
    (1, 1, "collision", "sri", [(1, "One of them was", "swann"), (2, "CIA visitors", "hidden"), (2, "Next came", "money")], {}),
    (1, 2, "reversal", "nature", [(1, "Swann is credited", "coords"), (1, "That summer", "price")], {}),
    (1, 3, "tag", "statements", [], {}),
    (2, 0, "world", "meade", [(0, "Over the years", "names")], {"chapter": "The unit at Fort Meade"}),
    (2, 1, "collision", "mcmoneagle", [(1, "A session went", "room"), (1, "Then the viewer described", "sheet")], {}),
    (2, 2, "cost", "agencies", [(0, "From about", "timeline"), (1, "People who worked", "legends")], {}),
    (2, 3, "tag", "target", [], {}),
    (3, 0, "world", "safe", [(0, "One was drawn", "baymap"), (1, "Then judges visited", "judging"), (1, "In {1976", "ieee")], {"chapter": "The judging problem"}),
    (3, 1, "collision", "nz", [(1, "So they studied", "clues"), (2, "Like a quiz", "quiz"), (3, "SRI's side", "letters")], {}),
    (3, 2, "reversal", "uncanny", [(1, "Try it", "anywhere")], {}),
    (3, 3, "tag", "memory", [], {}),
    (4, 0, "world", "review", [(1, "Two experts examined", "experts")], {"chapter": "The review of 1995"}),
    (4, 1, "collision", "five", [(1, "The two experts agreed", "agree"), (1, "Utts concluded", "split"), (2, "The review's own", "branches")], {}),
    (4, 2, "reversal", "users", [(1, "The report's words", "vague"), (2, "By then the unit", "lightsout")], {}),
    (4, 3, "cost", "objection", [], {}),
    (4, 4, "tag", "online", [], {}),
    (5, 0, "weigh", "ledger", [(1, "Did remote viewing", "ledger2")], {"chapter": "The weighing"}),
    (5, 1, "weigh", "people", [], {}),
    (5, 2, "test", "test", [], {}),
    (5, 3, "close", "close", [], {}),
]

# alias shots: (the panel they return to, the camera on that panel, the function drawing their additions on arrival)
ALIASES = {
    "axles": ("hero", [2.2, 760, 590], "add_axles"),
    "mind": ("globe", [1, 889, 500], "add_mind"),
    "memory": ("statements", [1, 889, 500], "add_memory"),
    "split": ("agree", [1, 889, 500], "add_split"),
    "ledger2": ("ledger", [1, 889, 500], "add_ledger2"),
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
    ep = {"id": "lf-stargate", "code": "LF.19", "series": script["series"], "title": script["title"], "case": "stargate-psychic",
          "verdict": "debunked", "claim": "Did remote viewing ever produce reliable intelligence?", "mood": "mystery",
          "hook_text": "Can a mind see across the *world*?", "beats": beats, "shots": shots,
          "sources": "Mumford, Rose & Goslin 1995, An Evaluation of Remote Viewing (AIR, for the CIA) · Utts 1996 and Hyman 1996, Journal of Scientific "
                     "Exploration 10(1) · Kress 1977, Parapsychology in Intelligence (CIA, Studies in Intelligence) · Targ & Puthoff 1974 "
                     "(doi:10.1038/251602a0) · Puthoff & Targ 1976 (doi:10.1109/PROC.1976.10113) · Marks & Kammann 1978 (doi:10.1038/274680a0) · "
                     "CIA CREST, STAR GATE files (online 2017)",
          "post": "In 1974 a former police commissioner drew a giant crane at a secret Soviet site from little more than map coordinates, and CIA "
                  "analysts called it accurate. For twenty-three years the US government paid for psychic spying: the code names, how a session "
                  "worked, why judging a hit is so hard, and the 1995 review that closed it. Weighed.",
          "hashtags": ["#Stargate", "#RemoteViewing", "#CIA", "#ColdWar", "#History", "#WeighItYourself"],
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
