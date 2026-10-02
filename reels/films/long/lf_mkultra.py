"""LF.14 · The Files · MKUltra: The Files That Survived (16:9 long film, one wall).

The script is films/long/lf-mkultra/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s67; s5, the title, is the intro card over the
panel of s4): seven forgotten boxes in a records warehouse, the Cold War fear of brainwashing, Dulles's speech and his approval,
149 subprojects and 80 institutions, the money through fronts and a hospital wing, the safe houses, the Inspector General, Frank
Olson's last days and the accounts of his death, the destruction of 1973 and the boxes of 1977, the Senate hearing, Montreal and
the compensation, and the weighing. Drawings are schematic and true to the numbers said: solid = on the record, dashed = inferred
or destroyed, dotted = claimed or hoped for. People harmed are drawn as quiet silhouettes, never in distress; no fall is shown.

Facts: the Short 'mkultra' (lg_d.py, 13.01) and the script's facts_added (the 1977 joint Senate hearing, the Church Committee 1976,
the CIA Inspector General 1963, the Rockefeller Commission 1975, Marks 1979, the National Security Archive's documents, the
court and press records on Frank Olson and on the Allan Memorial Institute).

Engine workaround (as in lf_voynich.py and lf_atlantis.py): the wall adds elements to a panel on its first visit, at a beat start
or a line start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a
tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's
additions as a panel item (kit.js builds them on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-mkultra/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-mkultra/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-mkultra RC_FILMS_EPS=/tmp/claude-0/sbx_lf-mkultra/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-mkultra/boards python3 films.py long.lf_mkultra
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-mkultra", "script.json")
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


def END(sid, back=.5):
    return round(max(.5, DUR[sid] - back), 2)


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


def ghost_box(x, y, w, h, at, c="#c9a27a", style="inferred", op=.75):
    """The dashed outline of a box that is no longer there."""
    d = h * .22
    return [poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], "rgba(201,162,122,.04)", c, 2, at, style=style, op=op),
            ln([(x, y), (x - d * .55, y - d), (x + w - d * .55, y - d), (x + w, y)], at, c, 1.6, style, draw=False, op=op)]


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


def glass(x, y, at, h=56, c="#cbd2d8", fill_at=None, liquid="rgba(220,170,110,.65)"):
    """A small glass standing on y (x = centre); fill_at: when the drink is poured."""
    w = h * .62
    out = [poly([[x - w / 2, y - h], [x + w / 2, y - h], [x + w * .38, y], [x - w * .38, y]], "rgba(159,208,255,.08)", c, 2.4, at)]
    if fill_at is not None:
        out.append(poly([[x - w * .45, y - h * .6], [x + w * .45, y - h * .6], [x + w * .36, y - 2], [x - w * .36, y - 2]], liquid, at=fill_at, fx="fill"))
    return out


def drop(x, y, at, c=LILAC, s=1.0):
    """A falling drop (point up) and its short dotted trail."""
    return [ln([[x, y - 80 * s], [x, y - 34 * s]], at, c, 2.4, "claimed", .4),
            poly([[x, y - 24 * s], [x + 10 * s, y - 4 * s], [x + 7 * s, y + 6 * s], [x, y + 9 * s], [x - 7 * s, y + 6 * s], [x - 10 * s, y - 4 * s]], c, at=at + .35, fx="rise", curve=True)]


def clock(x, y, r, at, sweep_at=None, sweep=300, c=BONE):
    """A wall clock; sweep_at: its hand sweeps round (a trailing arc draws itself)."""
    out = [circ(x, y, r, "#1d1813", c, 3, at)] + [ln([(x + (r - 10) * math.cos(a), y + (r - 10) * math.sin(a)), (x + (r - 3) * math.cos(a), y + (r - 3) * math.sin(a))], at, c, 2, draw=False)
                                                  for a in [k * math.pi / 6 for k in range(12)]]
    out += [ln([(x, y), (x, y - r * .6)], at, c, 4, draw=False), ln([(x, y), (x + r * .45, y + r * .15)], at, c, 3, draw=False)]
    if sweep_at is not None:
        pts = [(x + r * .78 * math.sin(math.radians(a)), y - r * .78 * math.cos(math.radians(a))) for a in range(0, sweep + 1, 10)]
        out.append(ln(pts, sweep_at, AMBER, 4, dur=1.4, curve=True))
    return out


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


def gavel(x, y, at, s=1.0, fx="rise", c="#8a5a36"):
    return [rect(x - 60 * s, y - 22 * s, 120 * s, 44 * s, c, "#d8b48a", 2, 8 * s, at, fx=fx),
            rect(x - 8 * s, y + 18 * s, 16 * s, 110 * s, "#6b4528", "#d8b48a", 1.5, 4 * s, at, fx=fx)]


def pill(x, y, w, at, c1="#e8e1d2", c2=AMBER, fx="pop"):
    """A two-tone capsule: one rounded body, its left half clipped in the second colour, a seam, a rim."""
    h = w * .42
    x0, y0 = x - w / 2, y - h / 2
    half = {"k": "group", "clip": [round(x0, 1), round(y0, 1), round(w / 2, 1), round(h, 1), 0], "els": [rect(x0, y0, w, h, c1, "none", 0, h / 2, -1)], "in": -1}
    return [grp([rect(x0, y0, w, h, c2, "none", 0, h / 2, -1), half, ln([(x, y0 + 1), (x, y0 + h - 1)], -1, "rgba(60,40,20,.3)", 1.5, draw=False),
                 rect(x0, y0, w, h, "none", "rgba(255,236,206,.5)", 1.5, h / 2, -1)], at, fx)]


# ---------------------------------------------------------------- buildings
def uni(x, y, s, at, c="#cbbca8", fill="#3a3129", fx="pop", op=None):
    """A university: columns under a pediment, base on y, s = width."""
    h = s * .62
    els = [rect(x - s / 2, y - h, s, h, fill, c, 2, 2, at, fx=fx, op=op),
           poly([[x - s * .58, y - h], [x, y - h - s * .3], [x + s * .58, y - h]], fill, c, 2, at, fx=fx, op=op)]
    els += [rect(x - s * .38 + s * .19 * k - s * .04, y - h * .86, s * .08, h * .86, c, at=at, fx=fx, op=op) for k in range(5)]
    return els


def hosp(x, y, s, at, c="#cbbca8", fill="#3a3129", fx="pop", op=None, cross_c="#e0574a"):
    h = s * .7
    return [rect(x - s / 2, y - h, s, h, fill, c, 2, 3, at, fx=fx, op=op),
            rect(x - s * .07, y - h * .82, s * .14, h * .42, cross_c, at=at, fx=fx, op=op), rect(x - s * .21, y - h * .68, s * .42, h * .14, cross_c, at=at, fx=fx, op=op),
            rect(x - s * .12, y - h * .28, s * .24, h * .28, c, at=at, fx=fx, op=op)]


def prison(x, y, s, at, c="#cbbca8", fill="#3a3129", fx="pop", op=None):
    h = s * .7
    els = [rect(x - s / 2, y - h, s, h, fill, c, 2, 2, at, fx=fx, op=op), rect(x - s * .3, y - h * .78, s * .6, h * .48, "#15110d", c, 2, 2, at, fx=fx, op=op)]
    els += [ln([[x - s * .3 + s * .12 * (k + 1), y - h * .78], [x - s * .3 + s * .12 * (k + 1), y - h * .3]], at, c, 3.5, draw=False, op=op) for k in range(4)]
    return els


def flask(x, y, s, at, c="#cbbca8", liquid="#7fb6a0", fx="pop", op=None):
    """A laboratory flask standing on y (a foundation or a drug company)."""
    return [poly([[x - s * .12, y - s], [x + s * .12, y - s], [x + s * .12, y - s * .62], [x + s * .45, y], [x - s * .45, y], [x - s * .12, y - s * .62]], "#2d2924", c, 2, at, fx=fx, op=op),
            poly([[x - s * .3, y - s * .22], [x + s * .3, y - s * .22], [x + s * .42, y - 2], [x - s * .42, y - 2]], liquid, at=at, fx=fx, op=op)]


def house(x, y, s, at, lit=True, c="#cbbca8", fill="#3a3129", fx="rise", op=None):
    """A small house: walls, a roof, a lit window."""
    h = s * .62
    els = [rect(x - s / 2, y - h, s, h, fill, c, 2, 2, at, fx=fx, op=op), poly([[x - s * .6, y - h], [x, y - h - s * .42], [x + s * .6, y - h]], fill, c, 2, at, fx=fx, op=op),
           rect(x - s * .3, y - h * .7, s * .22, s * .2, "#f2c98e" if lit else "#15110d", at=at, fx=fx, op=op),
           rect(x + s * .08, y - h * .7, s * .22, s * .2, "#f2c98e" if lit else "#15110d", at=at, fx=fx, op=op)]
    return els


def flats(x, y, w, h, at, rows=4, cols=3, lit=(), c="#cbbca8", fill="#2d2622", fx="rise"):
    """An apartment house: a block of windows, some lit (indices in `lit`)."""
    els = [rect(x - w / 2, y - h, w, h, fill, c, 2, 2, at, fx=fx)]
    ww, wh = w / (cols * 2 + 1), h / (rows * 2 + 1)
    for r in range(rows):
        for k in range(cols):
            i = r * cols + k
            els.append(rect(x - w / 2 + ww * (2 * k + 1), y - h + wh * (2 * r + 1), ww, wh, "#f2c98e" if i in lit else "#15110d", at=at, fx=fx))
    return els



# ================================================================== cold open: seven boxes in a warehouse
BOX_W, BOX_H, BOX_Y = 112, 96, 464           # the seven boxes on the middle shelf (their fronts: BOX_Y..BOX_Y+BOX_H, the board at 560)
BOX_X = [676 + 120 * k for k in range(7)]
SHELF_X0, SHELF_X1, BOARDS = 560, 1640, (400, 560, 720)


def shelf_unit(x0, x1, top, floor, levels, bw, bh, op, seed, gaps=0.0, steel=STEEL):
    """A far shelving unit seen from the front: uprights, boards, boxes on each board (dim with distance)."""
    rnd = random.Random(seed)
    els = [rect(x0, top, 10, floor - top, steel, at=-1, op=op), rect(x1 - 10, top, 10, floor - top, steel, at=-1, op=op)]
    for k in range(levels):
        y = top + (floor - top) * (k + 1) / levels
        els.append(rect(x0, y - 4, x1 - x0, 6, steel, at=-1, op=op))
        x = x0 + 14
        while x + bw < x1 - 12:
            if rnd.random() > gaps:
                els += static(abox(x, y - 4 - bh, bw, bh, -1, op=op, lab_=bw > 40, d=bh * .2))
            x += bw + 6
    return els


def sc_hero():
    """The hero image (s1), fully drawn from the first frame: a records warehouse in depth, a lamp over the front shelf, seven boxes."""
    els = [rect(-20, 760, 1820, 260, FLOOR, at=-1)]
    vx, vy = 720, 430
    for xb in range(-600, 2400, 230):                           # floor seams running to the vanishing point
        t = (760 - vy) / (1000 - vy)
        els.append(ln([(vx + (xb - vx) * t, 760), (xb, 1000)], -1, "#2e261f", 2, draw=False, op=.7))
    for y in (790, 840, 905):
        els.append(ln([(-20, y), (1800, y)], -1, "#231c16", 2, draw=False, op=.6))
    # the far aisle: two units further back, smaller and dimmer, and lamps down the hall
    els += [gl(330, 250, 90, -1, .25), gl(470, 270, 60, -1, .2), ln([(330, 0), (330, 236)], -1, "#3a332d", 1.5, draw=False)]
    els += shelf_unit(110, 520, 330, 600, 4, 40, 34, .28, 3)
    els += shelf_unit(170, 800, 270, 662, 4, 58, 50, .45, 5, gaps=.08)
    els += [rect(160, 662, 660, 40, "#120f0c", at=-1, op=.6), rect(-20, -20, 1820, 782, "#0b0907", at=-1, op=.42)]
    # the archivist in the aisle, his torch on the boxes
    els += [poly([[506, 584], [506, 600], [1010, 574], [740, 468]], "rgba(255,240,200,.16)", at=-1),
            ppl(470, 706, 200, -1, "#5a5249"), rect(498, 582, 16, 9, "#d8d0c0", at=-1), gl(508, 590, 40, -1, .9)]
    # the front unit: uprights, three boards, the seven boxes on the middle board (the fourth pulled half out)
    for x in (SHELF_X0, 1092, SHELF_X1 - 16):
        els.append(rect(x, 250, 16, 510, STEEL, "rgba(255,236,206,.18)", 1, 2, -1))
    for y in BOARDS:
        els += [rect(SHELF_X0 - 6, y, SHELF_X1 - SHELF_X0 + 12, 12, STEEL, "rgba(255,236,206,.25)", 1, 2, -1), ln([(SHELF_X0, y + 1), (SHELF_X1, y + 1)], -1, "#9aa0a6", 1.5, draw=False)]
    for k, x in enumerate(BOX_X):
        if k == 3:
            els += static(abox(x - 6, BOX_Y + 6, BOX_W + 12, BOX_H + 4, -1, out=True))
        else:
            els += static(abox(x, BOX_Y, BOX_W, BOX_H, -1))
    # the lamp and its light
    lx = 1092
    els += [cone(lx, 205, 70, 980, 560, -1, .1), gl(lx, 520, 600, -1, .4)] + static(lamp(lx, 190, -1, cord=190, op=.8, r=300)) + \
           [gl(lx, 790, 420, -1, .18)]
    rnd = random.Random(17)
    for _ in range(34):
        yy = rnd.uniform(240, 540)
        half = 35 + (yy - 205) / (560 - 205) * 455
        els.append(dot(round(lx + rnd.uniform(-half, half) * .9, 1), round(yy, 1), round(rnd.uniform(1.2, 2.6), 1), "#fff1d2", -1, op=round(rnd.uniform(.15, .45), 2)))
    t7 = T("hero", "seven")
    for k, x in enumerate(BOX_X):
        x0, w, y0, h = (x - 6, BOX_W + 12, BOX_Y + 6, BOX_H + 4) if k == 3 else (x, BOX_W, BOX_Y, BOX_H)
        els.append(rect(x0 - 3, y0 - 3, w + 6, h + 6, "none", AU, 3, 4, t7 + .14 * k, fx="pop"))
    els.append(gl(1092, 512, 420, t7 + .6, .3))
    return {"base": "dark", "cam": CAM, "els": els}


def add_gone():
    """s2: the files believed destroyed: dashed outlines of missing boxes all along the front shelves, a faint red glow."""
    t0 = T("gone", "destroyed") - .9
    els = [gl(1092, 520, 720, t0, .22, "red")]
    k = 0
    for y in (BOARDS[0], BOARDS[2]):
        for j in range(9):
            x = 588 + 116 * j
            els += ghost_box(x, y - BOX_H, 100, BOX_H, round(t0 + .05 * k, 2))
            k += 1
    els += ghost_box(582, BOX_Y, 86, BOX_H, round(t0 + .05 * k, 2)) + ghost_box(1522, BOX_Y, 96, BOX_H, round(t0 + .05 * (k + 1), 2))
    return els


def receipt(cx, cy, rot, at, seed, fx="rise", w=170, h=220):
    """A receipt or voucher: a sheet, a typed header, lines, a dollar column; as one group, turned by rot degrees."""
    x, y = cx - w / 2, cy - h / 2
    rnd = random.Random(seed)
    kids = [{"k": "rect", "x": x, "y": y, "w": w, "h": h, "r": 3, "fill": PAPER, "c": PAPER_D, "sw": 1.5},
            {"k": "rect", "x": x + 14, "y": y + 16, "w": w * .55, "h": 10, "r": 2, "fill": "#8a7a66", "c": "none", "sw": 0}]
    for j in range(6):
        yy = y + 52 + 24 * j
        kids += [{"k": "line", "p": [[x + 14, yy], [x + 14 + w * rnd.uniform(.35, .5), yy]], "c": "#6a5a48", "w": 3},
                 {"k": "label", "x": x + w - 50, "y": yy + 6, "t": "$", "st": "mono", "c": TYPE, "size": 16, "a": "end", "halo": False, "scl": True},
                 {"k": "line", "p": [[x + w - 46, yy], [x + w - 14 - rnd.uniform(0, 10), yy]], "c": TYPE, "w": 3}]
    kids += [{"k": "line", "p": [[x + w * .55, y + h - 30], [x + w - 12, y + h - 30]], "c": TYPE, "w": 2}]
    return grp(kids, at, fx, tr="rotate(%s %s %s)" % (rot, round(cx, 1), round(cy, 1)))


def sc_receipts():
    """s3: one box opened: receipts fan out; a university, a hospital and a prison pop as they are named, tied by threads."""
    els = [poly([[0, 650], [1778, 650], [1778, 1020], [0, 1020]], "#251c15", at=-1), ln([(0, 650), (1778, 650)], -1, "#5a4632", 2, draw=False),
           gl(889, 420, 620, -1, .22)]
    # the open box: its inside, the front, a label
    bx, by, bw, bh = 640, 520, 500, 240
    els += [poly([[bx, by], [bx + bw, by], [bx + bw - 40, by - 50], [bx + 40, by - 50]], "#1a130d", "rgba(255,236,206,.3)", 1.2, -1),
            rect(bx, by, bw, bh, CARD, "rgba(255,236,206,.3)", 1.5, 3, -1), rect(bx + 150, by + 50, 200, 70, PAPER, at=-1),
            ln([(bx + 175, by + 75), (bx + 325, by + 75)], -1, "#6a5a48", 3, draw=False), ln([(bx + 175, by + 98), (bx + 290, by + 98)], -1, "#6a5a48", 3, draw=False),
            poly(E(bx + bw / 2, by + 180, 60, 20, 16), "#2a1f15", at=-1)]
    t = T("receipts", "receipts")
    fan = [(700, 340, -15), (830, 300, -5), (960, 300, 6), (1090, 340, 16)]
    els += [receipt(cx, cy, r, round(.5 + .12 * k, 2), 11 + k) for k, (cx, cy, r) in enumerate(fan)]
    tu, th, tp = T("receipts", "universities"), T("receipts", "hospitals"), T("receipts", "prisons")
    els += uni(300, 430, 200, tu) + [lab(300, 474, "universities", tu + .2, BONE, 30), ln([(612, 330), (408, 380)], tu, AMBER, 2.5, dur=.5)]
    els += hosp(1490, 330, 170, th) + [lab(1490, 372, "hospitals", th + .2, BONE, 30), ln([(1180, 300), (1398, 300)], th, AMBER, 2.5, dur=.5)]
    els += prison(1490, 640, 170, tp) + [lab(1490, 682, "prisons", tp + .2, BONE, 30), ln([(1170, 420), (1400, 580)], tp, AMBER, 2.5, dur=.5)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_folder():
    """s4 (and the title card's backdrop): a folder on a desk; MKULTRA stamped on it; a head with a question; people, unnamed."""
    els = [poly([[0, 640], [1778, 640], [1778, 1020], [0, 1020]], "#221a14", at=-1), ln([(0, 640), (1778, 640)], -1, "#5a4632", 2, draw=False)]
    els += [ln([(150, 640), (170, 500), (250, 360)], -1, "#3a332d", 8, draw=False), poly([[200, 330], [320, 330], [290, 290], [230, 290]], "#3a3129", "rgba(255,226,180,.5)", 1.2, -1),
            gl(290, 420, 420, -1, .45)]
    fx0, fy0 = 330, 380
    els += [poly([[fx0, 640], [fx0 + 640, 640], [fx0 + 590, fy0], [fx0 + 50, fy0]], MANILA, MANILA_E, 2, -1),
            poly([[fx0 + 220, fy0], [fx0 + 240, fy0 - 30], [fx0 + 400, fy0 - 30], [fx0 + 410, fy0]], MANILA, MANILA_E, 2, -1),
            rect(fx0 + 170, fy0 + 40, 300, 46, PAPER, PAPER_D, 1, 2, -1)] + typed(fx0 + 190, fy0 + 64, 250, 1, -1, sw=4)
    tm = T("folder", "MKUltra")
    els.append(stamp(fx0 + 320, 540, "MKULTRA", tm, size=46, rot=-6))
    tq = T("folder", "control")
    els += [head(1330, 360, 330, tq - .6, "#2a2420", fx="rise", face=-1)] + qmark(1360, 340, tq, 120)
    tp = T("folder", "people")
    for k in range(9):
        els.append(ppl(990 + 80 * k, 792, 150 - 14 * (k % 3), round(tp + .12 * k, 2), "#5f574f", fx="fade", op=.55))
    els.append(gl(1300, 740, 380, tp, .18))
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 1 Brain warfare
def sc_paper():
    """s6: a 1950 newspaper, BRAIN-WASHING typing in; a head whose old lines are wiped and new ones written in (dotted: a claim)."""
    els = [gl(450, 470, 520, -1, .25), rect(150, 150, 610, 630, "#e8dcc2", PAPER_D, 1.5, 4, .2, fx="rise"), rect(190, 168, 530, 34, "#3a3029", at=.3),
           ln([(185, 212), (725, 212)], .3, TYPE, 3, draw=False), lab(205, 240, "1950", .5, TYPE, 24, "start", st="mono", halo=False, scl=True)]
    tb = T("paper", "brainwashing")
    els.append(lab(455, 318, "BRAIN-WASHING", tb - .6, INK, 64, st="serif", halo=False, scl=True, weight=700, fx="type", dur=1.0))
    els += typed(200, 352, 500, 2, tb, 20, sw=4)
    for c in range(3):
        els += typed(188 + 178 * c, 410, 150, 15, .6, 23, seed=c + 2, sw=2.5, dt=.01)
    hx, hy, hs = 1280, 380, 440
    els += [gl(1290, 300, 300, .3, .25), head(hx, hy, hs, .3, "#2a2420", face=-1)]
    old = [ln([(1188, 258 + 24 * j), (1188 + (200 if j % 2 == 0 else 160), 258 + 24 * j)], .6 + .1 * j, BONE, 4, draw=False, op=.85) for j in range(5)]
    els += old
    ts = T("paper", "scrubbing")
    els += [veil(1176, 240, 236, 120, ts + .4, "#2a2420", dur=.8),
            ln([(1120, 300), (1200, 230), (1300, 320), (1400, 236), (1460, 300)], ts, LILAC, 6, "claimed", .9, curve=True)]
    tn = T("paper", "writing in new")
    els += [ln([(1190, 262 + 26 * j), (1190 + (190 if j % 2 else 150), 262 + 26 * j)], tn + .25 * j, LILAC, 4, "claimed", .4) for j in range(4)]
    return {"base": "dark", "cam": CAM, "els": els}


def germ(x, y, r, at, c=LILAC):
    out = [circ(x, y, r, "rgba(201,193,238,.08)", c, 3, at, style="claimed")]
    for k in range(10):
        a = 2 * math.pi * k / 10
        out.append(ln([(x + r * math.cos(a), y + r * math.sin(a)), (x + (r + 18) * math.cos(a), y + (r + 18) * math.sin(a))], at, c, 3, "claimed", draw=False))
    return out


def sc_korea():
    """s7: Korea on a small map, a prison camp; a captured airman signs a confession; a germ (dotted); 'called false'; a '?' over a mind."""
    v = View(124.0, 131.2, 33.2, 43.0, (110, 160, 520, 600))
    cx_, cy_ = v.p(125.4, 40.6)
    els = [rect(96, 150, 548, 620, "rgba(16,13,10,.85)", "rgba(255,236,206,.3)", 2, 14, .2),
           {"k": "group", "clip": [98, 152, 544, 616, 14], "els": [{"k": "map", "land": v.land()}], "in": .2},
           {"k": "pin", "x": cx_, "y": cy_, "t": "prison camp", "c": GOLD, "in": .8}, lab(*v.p(127.9, 35.6), "Korea", .6, DIM, 30)]
    ts = T("korea", "signed")
    els += [gl(1080, 520, 300, .3, .25)] + table(1100, 600, 300, .3) + seated(930, 774, 300, .4, "#8a8278", face=1)
    els += sheet(1010, 360, 190, 230, ts - .5, lines=6, seed=4, lh=24) + [ln([(1040, 560), (1080, 548), (1110, 566), (1150, 550)], ts + .3, INK, 3, dur=.6, curve=True),
                                                                           lab(1105, 340, "a confession", ts, BONE, 28)]
    tg = T("korea", "germ")
    els += germ(1300, 300, 34, tg)
    tf = T("korea", "false")
    els.append(stamp(1105, 470, "CALLED FALSE", tf, size=28, rot=-9))
    tq = T("korea", "rewrite")
    els += [head(1530, 430, 300, tq - .5, "#2a2420", fx="rise", face=-1)] + qmark(1550, 410, tq, 110)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_teams():
    """s8: an interrogation room: a lie detector, drugs and a swinging watch pop on the table as they are named."""
    els = [rect(-20, 760, 1820, 260, FLOOR, at=-1)] + static(lamp(889, 200, -1, cord=150, op=.75, r=260)) + [cone(889, 215, 60, 920, 560, -1, .07)]
    els += static(table(889, 560, 900, -1, h=190))
    els += seated(380, 762, 300, .3, "#8a8278", face=1) + [ppl(1460, 762, 320, .4, "#5a524a")]
    tl, td, th = T("teams", "lie detector"), T("teams", "drugs"), T("teams", "hypnosis")
    els += [rect(560, 484, 160, 76, "#2d2924", BONE, 2, 6, tl, fx="pop"), circ(600, 520, 16, "#1a1511", BONE, 2, tl), circ(650, 520, 16, "#1a1511", BONE, 2, tl),
            rect(720, 516, 110, 18, PAPER, at=tl + .2, fx="pop"),
            ln([(724, 525), (740, 517), (752, 532), (766, 515), (780, 534), (794, 518), (808, 530), (824, 524)], tl + .4, RED, 2, dur=.6),
            lab(660, 450, "lie detector", tl, BONE, 28)]
    els += [rect(872, 488, 22, 72, "rgba(159,208,255,.25)", BLUE, 2, 4, td, fx="pop"), rect(908, 536, 110, 14, "#cbd2d8", BONE, 1.5, 3, td + .15, fx="pop"),
            ln([(1018, 543), (1050, 543)], td + .15, BONE, 2, draw=False), lab(940, 470, "drugs", td, BONE, 28)]
    els += [ln([(1180, 372), (1180, 470)], th, "#d8c08a", 2, draw=False), circ(1180, 494, 24, "#d8c08a", "#fff1d2", 2, th, fx="pop"),
            ln([(1130, 500), (1180, 520), (1230, 500)], th + .3, LILAC, 3, "claimed", .6, curve=True), lab(1290, 420, "hypnosis", th, BONE, 28, "start")]
    els.append(lab(1600, 190, "from 1950", T("teams", "From"), AMBER, 28, "end", st="cap"))
    return {"base": "dark", "cam": CAM, "els": els}


def calendar(x, y, w, h, day, at, month="APRIL", year="1953", fx="pop"):
    return [rect(x, y, w, h, PAPER, PAPER_D, 1.5, 4, at, fx=fx), rect(x, y, w, h * .22, STAMP, at=at, fx=fx),
            lab(x + w / 2, y + h * .16, month, at, PAPER, 26, st="cap", halo=False, scl=True),
            lab(x + w / 2, y + h * .72, str(day), at, INK, h * .46, st="serif", halo=False, scl=True),
            lab(x + w / 2, y + h * .92, year, at, TYPE, 22, st="mono", halo=False, scl=True)]


def sc_dulles():
    """s9: a hall, a speaker at a lectern ('Allen Dulles'), the audience in silhouette; 'brain warfare' rises; the calendar: 10 April 1953."""
    els = [cone(1000, 110, 80, 420, 560, -1, .08), gl(1000, 470, 300, -1, .3)]
    els += [ppl(1000, 720, 380, .2, "#8a8278"), poly([[905, 580], [1095, 580], [1072, 772], [928, 772]], "#4a3828", "#8a6a48", 2, .2),
            rect(895, 570, 210, 16, "#5a4632", "#8a6a48", 1.5, 3, .2), lab(1080, 372, "Allen Dulles", .8, BONE, 30, "start")]
    rnd = random.Random(7)
    for row, (y, r, n) in enumerate(((812, 22, 17), (772, 19, 19))):
        for k in range(n):
            x = 100 + (1580 / (n - 1)) * k + rnd.uniform(-14, 14)
            if 905 < x < 1095:
                continue
            col = ("#15110e", "#1c1713")[row]
            els += [poly(E(x, y + r * 1.5, r * 1.6, r * .9, 18), col, "rgba(255,226,190,.14)", 1, -1), circ(x, y, r * .78, col, "rgba(255,226,190,.2)", 1.2, -1)]
    tc = T("dulles", "tenth")
    els += calendar(200, 230, 230, 250, 10, tc)
    tb = T("dulles", "brain warfare")
    els += [ln([(985, 400), (880, 340), (780, 318)], tb - .3, LILAC, 3, "claimed", .6, curve=True), lab(620, 318, "brain warfare", tb, LILAC, 46, st="ital")]
    th = T("dulles", "handicapped")
    els.append(lab(620, 372, "the West, handicapped", th, "#d8d2ee", 28, st="ital"))
    return {"base": "dark", "cam": CAM, "els": els}


def add_approved():
    """s10: the calendar turns to 13 April; a typed memo slides in, stamped APPROVED."""
    t0 = T("approved", "Three days")
    els = []
    for k, d in enumerate((11, 12, 13)):
        els += calendar(200, 230, 230, 250, d, round(t0 + .35 * k, 2))
    ta = T("approved", "approved")
    els += sheet(1250, 170, 360, 440, ta - .7, lines=11, seed=8, lh=26) + [lab(1290, 216, "MEMORANDUM", ta - .5, TYPE, 24, "start", st="mono", halo=False, scl=True)]
    els.append(stamp(1430, 470, "APPROVED", ta + .2, size=40, rot=-8))
    return els


def ampoule(x, y, h, at, fx="pop", c="rgba(220,236,255,.35)", e="#e6f2ff"):
    """A glass ampoule standing on y: a body, a neck, a tip."""
    w = h * .32
    return [rect(x - w / 2, y - h * .62, w, h * .62, c, e, 2, w / 2, at, fx=fx), rect(x - w * .18, y - h * .82, w * .36, h * .22, c, e, 1.5, 2, at, fx=fx),
            rect(x - w * .3, y - h, w * .6, h * .18, c, e, 1.5, w * .3, at, fx=fx)]


def sc_lab():
    """s11: a lab bench at night, Sidney Gottlieb in a lab coat; the MKULTRA folder; 1953 to 1964; an ampoule of LSD glows."""
    els = static(lamp(640, 190, -1, cord=150, op=.7, r=240)) + [rect(-20, 760, 1820, 260, FLOOR, at=-1)]
    els += [ppl(560, 742, 330, .3, "#d9d2c4"), lab(560, 386, "Sidney Gottlieb", .9, BONE, 30)]
    els += [rect(240, 556, 1300, 18, "#5a4632", "#8a6a48", 1.5, 3, -1), rect(250, 574, 1280, 186, "#2a2019", "#4a3828", 1.5, 2, -1)]
    els += flask(760, 556, 110, .5) + flask(850, 556, 70, .6, liquid="#b8a07a") + [gl(700, 540, 60, .6, .7, "fire"), rect(690, 536, 20, 20, "#3a332d", at=.6)]
    for k in range(5):
        els.append(rect(930 + 18 * k, 496, 12, 60, "rgba(159,208,255,.2)", "#cbd2d8", 1.5, 6, .7))
    tn = T("lab", "name")
    els += [folder(1080, 420, 210, 136, tn, fx="pop"), lab(1185, 506, "MKULTRA", tn + .1, TYPE, 30, st="mono", halo=False, scl=True, fx="pop")]
    ty = T("lab", "ten years")
    els += [axis(1200, 1560, 250, [(1200, "1953"), (1560, "1964")], ty - .6), ln([(1200, 232), (1560, 232)], ty, AMBER, 10, dur=1.0, op=.9)]
    tl = T("lab", "LSD")
    els += ampoule(1440, 556, 90, tl - .3) + [gl(1440, 500, 140, tl, .7), lab(1440, 432, "LSD", tl, GOLD, 34, st="lab")]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_tongues():
    """s12: a head where the lines of the senses tangle; a clock sweeps through the hours; dotted words leave the mouth for a notepad."""
    hx, hy, hs = 560, 420, 460
    els = [head(hx, hy, hs, .2, "#2a2420"), gl(560, 340, 260, .2, .2)]
    ts = T("tongues", "scramble")
    for j, c in enumerate((BLUE, AMBER, GREEN)):
        pts = [(470 + 8 * i, 300 + 30 * j + 22 * math.sin(i * .9 + j * 2.1) + 10 * math.sin(i * 2.3 + j)) for i in range(27)]
        els.append(ln(pts, ts + .2 * j, c, 4, dur=1.2, curve=True))
    th = T("tongues", "hours")
    els += clock(1000, 290, 86, th - .8, sweep_at=th) + [lab(1000, 420, "for hours", th, BONE, 28)]
    tt = T("tongues", "loosen")
    els += [ppl(1610, 760, 320, .4, "#5a524a"), rect(1420, 470, 130, 160, PAPER, PAPER_D, 1.5, 3, tt - .4, fx="pop")] + typed(1436, 500, 96, 5, tt + .6, 22, seed=5)
    for k in range(3):
        els.append(ln([(785, 450 + 16 * k), (1000, 500 + 20 * k), (1410, 520 + 26 * k)], tt + .15 * k, LILAC, 3, "claimed", .9, curve=True))
    els.append(lab(1110, 640, "loosen tongues?", tt + .4, LILAC, 30))
    return {"base": "dark", "cam": CAM, "els": els}


# 80 institutions: blocks (x0, y0, cols, rows, n, kind)
INST = [(920, 300, 11, 4, 44, "uni"), (1420, 300, 6, 2, 12, "hosp"), (920, 540, 5, 3, 15, "flask"), (1180, 540, 3, 1, 3, "prison"), (1420, 540, 3, 2, 6, "other")]


def _inst_pos(b):
    x0, y0, cols, rows, n, kind = b
    return [(x0 + 40 * (i % cols), y0 + 40 * (i // cols)) for i in range(n)]


def sc_grid():
    """s13: 149 folders pop in (15 a row); then 80 grey markers, grouped as the next shot names them."""
    els = []
    t1 = T("grid", "hundred")
    for i in range(149):
        x, y = 140 + 38 * (i % 15), 300 + 32 * (i // 15)
        els.append(folder(x, y, 30, 20, round(t1 + .011 * i, 3), fx="pop"))
    els.append(lab(420, 252, "149 subprojects", T("grid", "subprojects"), AMBER, 34))
    t2 = T("grid", "eighty")
    k = 0
    for b in INST:
        for (x, y) in _inst_pos(b):
            els.append(dot(x, y, 9, "#6a625a", round(t2 + .012 * k, 3)))
            k += 1
    els.append(lab(1260, 252, "80 institutions", t2 + .2, AMBER, 34))
    return {"base": "dark", "cam": CAM, "els": els}


def add_groups():
    """s14: the markers light by group as named: 44 universities, 12 hospitals, 15 foundations and companies, 3 prisons; 6 others stay grey."""
    els = []
    ts = {"uni": T("groups", "Forty-four"), "hosp": T("groups", "Twelve"), "flask": T("groups", "Fifteen"), "prison": T("groups", "three prisons")}
    draw = {"uni": lambda x, y, at: uni(x, y + 14, 30, at, c=GOLD, fill="#3a3129"), "hosp": lambda x, y, at: hosp(x, y + 14, 30, at),
            "flask": lambda x, y, at: flask(x, y + 14, 30, at, c=GOLD), "prison": lambda x, y, at: prison(x, y + 14, 30, at, c=GOLD)}
    for b in INST:
        kind = b[5]
        if kind == "other":
            continue
        for j, (x, y) in enumerate(_inst_pos(b)):
            els += draw[kind](x, y, round(ts[kind] + .015 * j, 3))
    els += [lab(1120, 470, "44 universities", ts["uni"] + .3, BONE, 28), lab(1520, 392, "12 hospitals", ts["hosp"] + .3, BONE, 28),
            lab(1000, 674, "15 foundations, companies", ts["flask"] + .3, BONE, 28), lab(1220, 600, "3 prisons", ts["prison"] + .3, BONE, 28),
            lab(1460, 626, "6 others", ts["prison"] + .9, MUTED, 24)]
    return els


def add_claims():
    """s15: an expense-claim card over the grid: 'paid to' and 'amount' filled, 'what for' mostly blank (dashed)."""
    t0 = T("claims", "Reading")
    els = [rect(500, 300, 780, 430, PAPER, PAPER_D, 2, 6, t0 - .2, fx="rise")]
    hd = [(560, "PAID TO"), (840, "AMOUNT"), (1100, "WHAT FOR")]
    els += [lab(x, 350, t, t0 + .2, TYPE, 24, "start", st="mono", halo=False, scl=True) for x, t in hd]
    els.append(ln([(530, 372), (1250, 372)], t0 + .2, TYPE, 2, draw=False))
    tw = T("claims", "who was paid")
    tr = T("claims", "roughly why")
    rnd = random.Random(21)
    for j in range(5):
        y = 420 + 66 * j
        els += [ln([(560, y), (560 + rnd.uniform(160, 230), y)], tw + .1 * j, TYPE, 4, draw=False),
                lab(840, y + 8, "$", tw + .1 * j + .05, TYPE, 24, "start", st="mono", halo=False, scl=True),
                ln([(866, y), (866 + rnd.uniform(60, 110), y)], tw + .1 * j + .05, TYPE, 4, draw=False),
                rect(1090, y - 22, 160, 40, "none", "#8a7a66", 2, 4, tr + .1 * j, style="inferred")]
    els.append(lab(1170, 432, "?", tr + .6, "#8a7a66", 34, st="serif", halo=False, scl=True))
    return els


def bag(x, y, s, at, fx="rise"):
    """A money bag: a round sack, a tied neck, a dollar sign."""
    return [poly([(x + s * px, y + s * py) for px, py in ((-.5, .1), (-.42, -.25), (-.18, -.42), (-.1, -.55), (-.22, -.68), (.22, -.68), (.1, -.55), (.18, -.42),
                                                           (.42, -.25), (.5, .1), (.4, .38), (0, .46), (-.4, .38))], "#b89a62", "#e8d2a0", 2, at, fx=fx, curve=True),
            lab(x, y + s * .18, "$", at, "#4a3a22", s * .5, st="serif", halo=False, scl=True, fx=fx)]


def sc_front():
    """s16: money from a 'CIA' box goes into a bag, through a dotted front ('Human Ecology'), to three researchers who never knew."""
    els = [rect(130, 380, 200, 180, "#2a2420", BONE, 2.5, 10, .3, fx="pop"), lab(230, 488, "CIA", .4, BONE, 46, st="serif")]
    tb = T("front", "money")
    els += bag(470, 500, 150, tb) + [rect(432, 516, 76, 26, "#2a2420", at=tb, fx="rise"), lab(470, 535, "CIA", tb, BONE, 20, st="cap", halo=False, scl=True, fx="rise")]
    tc = T("front", "never said")
    els += [rect(424, 510, 92, 38, PAPER, PAPER_D, 1.5, 4, tc + .6, fx="pop")]
    tf = T("front", "fronts")
    els += [arr([(560, 470), (760, 470)], tf - .3, AMBER, 3)]
    fx_, fy_ = 910, 640
    els += [rect(780, 410, 260, 230, "rgba(201,193,238,.06)", LILAC, 2.5, 3, tf, style="claimed"),
            poly([[766, 410], [910, 330], [1054, 410]], "rgba(201,193,238,.06)", LILAC, 2.5, tf, style="claimed")]
    els += [ln([(810 + 50 * k, 430), (810 + 50 * k, 632)], tf + .2, LILAC, 2.5, "claimed", draw=False) for k in range(5)]
    els += [lab(910, 300, "a front", tf + .3, LILAC, 30), lab(910, 690, "Human Ecology", T("front", "Human Ecology"), LILAC, 30)]
    tr = T("front", "Many scientists")
    els += [arr([(1060, 470), (1260, 470)], tr - .8, AMBER, 3)] + [ppl(1330 + 110 * k, 700, 220, round(tr - .5 + .15 * k, 2), "#9a9288") for k in range(3)]
    els.append(lab(1440, 744, "researchers", tr - .2, BONE, 28))
    tq = T("front", "never knew")
    els += [lab(1330 + 110 * k, 452, "?", round(tq + .15 * k, 2), LILAC, 48, st="serif", fx="pop") for k in range(3)]
    return {"base": "dark", "cam": CAM, "els": els}


def coins(x, base, n, at, dt=.06, c="#d8b45a"):
    out = []
    for k in range(n):
        y = base - 18 * k
        out += [poly(E(x, y, 62, 16, 20), "#8a6a2e", c, 1.5, round(at + dt * k, 2), fx="pop"), poly(E(x, y - 6, 62, 16, 20), c, "#fff1d2", 1.2, round(at + dt * k, 2), fx="pop")]
    return out


def sc_wing():
    """s17: a hospital; a new wing draws itself beside it; $375,000 arrives as 'a private gift' (dotted); a federal match; the wing fills."""
    els = [rect(-20, 720, 1820, 300, "#1c1712", at=-1), ln([(-20, 720), (1800, 720)], -1, "#4a3e30", 2, draw=False), gl(640, 520, 600, -1, .18)]
    els += [rect(170, 300, 470, 420, "#3a3129", "#cbbca8", 2, 3, -1), rect(375, 330, 60, 120, "#e0574a", at=-1), rect(330, 365, 150, 50, "#e0574a", at=-1)]
    for r in range(3):
        for k in range(6):
            els.append(rect(200 + 72 * k, 480 + 70 * r, 38, 40, "#f2c98e" if (r + k) % 3 else "#15110d", at=-1))
    tw = T("wing", "wing")
    els += [rect(660, 400, 540, 320, "none", BONE, 2.5, 3, tw - .4, style="inferred")]
    tm = T("wing", "matched")
    els += [rect(660, 400, 540, 320, "#3a3129", "#cbbca8", 2, 3, tm + .3, fx="fill")]
    els += [rect(690 + 86 * k, 450 + 90 * r, 40, 44, "#f2c98e", at=round(tm + .7 + .03 * (k + r), 2)) for r in range(3) for k in range(6)]
    t3 = T("wing", "three hundred")
    els += coins(1390, 712, 12, t3 - .3) + [lab(1390, 768, "$375,000", t3 + .4, GOLD, 30)]
    tg = T("wing", "private gift")
    els += [ln([(1320, 560), (1390, 600), (1460, 560)], tg, LILAC, 5, "claimed", .6, curve=True), ln([(1390, 600), (1360, 640)], tg + .3, LILAC, 4, "claimed", .3),
            ln([(1390, 600), (1420, 640)], tg + .3, LILAC, 4, "claimed", .3), lab(1390, 440, "a private gift", tg, LILAC, 28)]
    els += coins(1570, 712, 12, tm - .2) + [lab(1570, 768, "federal match", tm + .4, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_sixth():
    """s18: the new wing split into six bays; one tinted lilac, 'a sixth for the CIA'; a '?' inside it."""
    t0 = T("sixth", "In return")
    els = [ln([(660 + 90 * k, 404), (660 + 90 * k, 716)], round(t0 + .1 * k, 2), BONE, 2.5, dur=.4) for k in range(1, 6)]
    ts = T("sixth", "sixth")
    els += [rect(1112, 404, 86, 312, "rgba(201,193,238,.28)", LILAC, 3, 2, ts, style="claimed"), lab(1155, 372, "a sixth for the CIA", ts + .2, LILAC, 28)]
    tq = T("sixth", "What happened")
    els += qmark(1155, 600, tq, 80)
    return els



# ================================================================== 2 The safe houses
def sc_labstreet():
    """s19: at the left a bright lab, a volunteer and a tester ('volunteers'); at the right a street at night, ordinary people
    ('normal life'), one of them softly lit ('unwitting'); between them the 1963 report, its word 'unwitting' marked."""
    tl = T("labstreet", "Lab tests")
    els = [rect(110, 200, 720, 540, "#39332b", "#8a7a66", 2, 6, .2), rect(300, 212, 340, 12, "#fff1d2", at=.2), gl(470, 300, 360, .3, .35)]
    els += table(470, 580, 420, .3, h=150) + seated(330, 730, 270, .4, "#9a9288", face=1)
    els += [ppl(640, 730, 300, .5, "#d9d2c4"), rect(600, 520, 50, 66, PAPER, PAPER_D, 1, 3, .6), lab(470, 172, "volunteers", tl + .4, BONE, 30)]
    to = T("labstreet", "real operation") - .6
    els += [rect(890, 700, 820, 60, "#1d1813", at=to)] + flats(990, 700, 170, 400, to, rows=6, cols=3, lit=(1, 3, 7, 11, 13, 16))
    els += flats(1210, 700, 200, 330, to + .1, rows=5, cols=3, lit=(0, 4, 5, 9, 14)) + flats(1450, 700, 180, 420, to + .2, rows=6, cols=3, lit=(2, 6, 8, 12, 15, 17))
    els += flats(1640, 700, 120, 300, to + .3, rows=5, cols=2, lit=(1, 4, 7))
    tu = T("labstreet", "unwitting")
    for k, (x, h) in enumerate(((960, 170), (1120, 160), (1300, 176), (1480, 164), (1620, 172))):
        els.append(ppl(x, 770, h, round(to + .4 + .15 * k, 2), "#7a7268" if k != 2 else "#cbbca8"))
    els += [gl(1300, 690, 120, tu, .55), lab(1300, 172, "normal life", T("labstreet", "normal life"), BONE, 30)]
    tr = T("labstreet", "A CIA report")
    els += [rect(780, 260, 240, 300, PAPER, PAPER_D, 1.5, 4, tr, fx="rise"), lab(900, 298, "1963 report", tr + .1, TYPE, 24, st="mono", halo=False, scl=True, fx="rise")]
    els += typed(806, 330, 188, 3, tr + .3, 26)
    els += [rect(804, 410, 150, 34, "rgba(232,184,122,.55)", at=tu), lab(879, 434, "unwitting", tu, INK, 24, st="mono", halo=False, scl=True)]
    els += typed(806, 470, 188, 3, tr + .5, 26, seed=4)
    return {"base": "dark", "cam": CAM, "els": els}


USV = View(-125.0, -66.5, 24.0, 50.0, (100, 140, 1580, 640))
SF, NY = USV.p(-122.42, 37.77), USV.p(-74.0, 40.71)


def sc_map():
    """s20: the United States; San Francisco and New York pinned as named; a small apartment house rises at each; a dashed line joins them."""
    ts, tn = T("map", "San Francisco"), T("map", "New York")
    els = [{"k": "map", "land": USV.land(), "in": -1},
           {"k": "pin", "x": SF[0], "y": SF[1], "t": "San Francisco", "c": GOLD, "in": ts},
           {"k": "pin", "x": NY[0], "y": NY[1], "t": "New York", "c": GOLD, "a": "end", "lx": -20, "in": tn}]
    els += flats(SF[0] + 14, SF[1] - 26, 64, 84, ts + .5, rows=3, cols=2, lit=(1, 2, 5)) + flats(NY[0] - 14, NY[1] - 26, 64, 84, tn + .5, rows=3, cols=2, lit=(0, 3, 4))
    tr = T("map", "rented")
    els += [ln([(SF[0] + 40, SF[1] - 80), (889, 230), (NY[0] - 40, NY[1] - 80)], tr, LILAC, 3, "inferred", 1.2, curve=True),
            lab(889, 214, "safe houses", tr + .6, LILAC, 32)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_closed():
    """s27: the safe houses close: their windows go dark ('1965', '1966')."""
    t0 = T("closed", "closed") - .4
    els = []
    for (x, y), yr, dt in ((SF, "1965", 0), (NY, "1966", .6)):
        cx = x + 14 if yr == "1965" else x - 14
        els += [veil(cx - 34, y - 26 - 86, 68, 88, t0 + dt, "#141110", op=.75, dur=1.0), lab(cx, y + 54, yr, t0 + dt + .2, BONE, 28)]
    return els


def sofa(x0, x1, y, at):
    return [rect(x0, y - 150, x1 - x0, 90, "#4a3328", "#7a5a44", 2, 14, at), rect(x0 - 10, y - 80, x1 - x0 + 20, 50, "#5a3e30", "#7a5a44", 2, 10, at),
            rect(x0 - 26, y - 120, 40, 90, "#4a3328", "#7a5a44", 2, 10, at), rect(x1 - 14, y - 120, 40, 90, "#4a3328", "#7a5a44", 2, 10, at),
            rect(x0, y - 30, 14, 30, "#2a1d16", at=at), rect(x1 - 14, y - 30, 14, 30, "#2a1d16", at=at)]


def sc_flat():
    """s21: an ordinary flat at night: a sofa, a lamp, a guest; George White hands over a glass; a dotted drop falls into it;
    beyond a partition, someone watches (a dotted blue sight line)."""
    els = [rect(120, 160, 1540, 600, "#2a221b", "#5a4632", 2, 6, -1), rect(-20, 760, 1820, 260, FLOOR, at=-1),
           rect(180, 230, 200, 230, "#101a2a", "#8a6a48", 6, 3, -1)]
    rnd = random.Random(8)
    els += [rect(round(rnd.uniform(195, 360), 1), round(rnd.uniform(330, 445), 1), 6, 8, "#f2c98e", at=-1, op=.8) for _ in range(16)]
    els += [ln([(280, 230), (280, 460)], -1, "#8a6a48", 4, draw=False), ln([(180, 345), (380, 345)], -1, "#8a6a48", 4, draw=False)]
    els += [ln([(450, 760), (450, 430)], -1, "#3a332d", 5, draw=False), poly([[410, 430], [490, 430], [470, 380], [430, 380]], "#c9a06a", "#fff1d2", 1, -1),
            gl(450, 430, 260, -1, .55)]
    els += static(clock(1010, 260, 50, -1))
    els += sofa(500, 840, 760, -1) + seated(612, 712, 270, .3, "#9a9288", face=1, stool=False)
    els += static(table(790, 690, 200, -1, h=56))
    tw = T("flat", "George White")
    els += [ppl(985, 760, 300, tw - .5, "#5a524a"), lab(985, 420, "George White", tw, BONE, 30)]
    tg = T("flat", "invited")
    els += glass(880, 572, tg, h=50, fill_at=tg + .3)
    tsl = T("flat", "slipped")
    els += drop(880, 506, tsl)
    els += [rect(1186, 160, 22, 250, "#3a2c20", "#5a4632", 1.5, 2, -1), rect(1186, 760, 22, 0.1, "#3a2c20", at=-1)]
    tw2 = T("flat", "watched")
    els += [ppl(1420, 760, 300, tw2 - .6, "#3d3833"), rect(1372, 560, 46, 60, PAPER, PAPER_D, 1, 3, tw2 - .4),
            ln([(1400, 488), (1000, 520), (650, 540)], tw2, BLUE, 2.5, "claimed", 1.0, curve=True)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_ampoule():
    """s22: a loupe over the flat: inside it a plastic ampoule and a clear glass, drawn large, a dotted line from one to the other;
    'about 80 micrograms'; 'invisible'."""
    t0 = T("ampoule", "ampoules")
    cx, cy, r = 730, 300, 128
    els = [ln([(cx + 60, cy + 112), (790, 676)], t0 - .6, GOLD, 2, "claimed", .5), circ(cx, cy, r, "#141110", GOLD, 3, t0 - .5, fx="pop"),
           gl(cx - 50, cy + 10, 110, t0, .4, "blue")]
    els += ampoule(cx - 50, cy + 80, 150, t0) + glass(cx + 62, cy + 80, t0 + .3, h=118)
    els += [ln([(cx - 50, cy - 74), (cx, cy - 120 + 12), (cx + 50, cy - 26)], t0 + .7, LILAC, 3, "claimed", .6, curve=True)]
    tm = T("ampoule", "eighty")
    els += [lab(cx, cy + 162, "about 80 micrograms", tm, GOLD, 28), lab(cx + 62, cy + 114, "invisible", T("ampoule", "invisible"), LILAC, 24)]
    return els


def add_ill():
    """s23: swirls round the guest's head; the clock's hand sweeps; day squares fill; the watcher's notes stop: 'when practical'."""
    t0 = T("ill", "no idea")
    hx, hy = 630, 530
    els = [ln([(hx + 44 * math.cos(a + .55 * j), hy + 44 * math.sin(a + .55 * j)) for j in range(6)], round(t0 + .25 * k, 2), LILAC, 3, dur=.6, curve=True)
           for k, a in enumerate((0, 2.1, 4.2))]
    th = T("ill", "hours")
    els += [ln([(1010 + 38 * math.sin(math.radians(a)), 260 - 38 * math.cos(math.radians(a))) for a in range(0, 331, 15)], th - .2, AMBER, 4, dur=1.4, curve=True)]
    els += [rect(900 + 46 * k, 330, 36, 36, "#3a3129", "#cbbca8", 1.5, 4, round(th + .2 + .12 * k, 2)) for k in range(5)]
    els += [rect(900 + 46 * k, 330, 36, 36, "rgba(232,184,122,.6)", at=round(T("ill", "days") + .1 * k, 2)) for k in range(5)]
    tp = T("ill", "practical")
    els += [rect(1372, 560, 46, 60, "#8a7a66", at=tp - .5), lab(1420, 418, "when practical", tp, LILAC, 28)]
    return els


def outline_person(x, y, h, at, c=LILAC, style="claimed", w=2.2):
    """A figure drawn as an outline only (an estimate, or someone not on the record)."""
    s = h
    body = [(x - .14 * s, y - .74 * s), (x + .14 * s, y - .74 * s), (x + .12 * s, y - .4 * s), (x + .08 * s, y), (x - .08 * s, y), (x - .12 * s, y - .4 * s)]
    return [circ(x, y - .88 * s, .09 * s, "none", c, w, at, style=style, fx="pop"), poly(body, "rgba(201,193,238,.05)", c, w, at, style=style, fx="pop")]


def sc_forty():
    """s24: forty figures in dotted outline, 'about 40 tests?' (Gottlieb's later guess); the records that could check it, dashed, gone."""
    tg = T("forty", "forty")
    els = qmark(1385, 330, .3, 110)
    for i in range(40):
        x, y = 230 + 78 * (i % 10), 360 + 128 * (i // 10)
        els += outline_person(x, y, 104, round(tg - .4 + .03 * i, 2))
    els += [lab(580, 196, "about 40 tests?", tg + .3, LILAC, 34)]
    tr = T("forty", "records")
    els += ghost_box(1250, 450, 270, 200, tr, c="#cbbca8") + [lab(1385, 700, "the records", tr + .2, DIM, 28)]
    els += cross(1385, 550, T("forty", "no longer"), RED, 2.2, 7)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_ig():
    """s25: an inspector reads at a desk under a lamp; his report (1963), SECRET; the words 'in jeopardy' light up on it."""
    els = static(lamp(560, 200, -1, cord=150, op=.7, r=240)) + [rect(-20, 760, 1820, 260, FLOOR, at=-1)]
    els += static(table(600, 560, 560, -1, h=190)) + seated(420, 762, 300, .2, "#9a9288", face=1)
    els += [rect(560, 540, 120, 18, PAPER, at=.3), lab(470, 380, "Inspector General", T("ig", "Inspector") - .2, BONE, 30)]
    tr = T("ig", "His report")
    els += [rect(1050, 150, 480, 570, PAPER, PAPER_D, 2, 4, tr - .6, fx="rise"), lab(1090, 200, "INSPECTION REPORT, 1963", tr - .4, TYPE, 24, "start", st="mono", halo=False, scl=True)]
    els += typed(1090, 250, 400, 6, tr - .2, 26, seed=6) + typed(1090, 470, 400, 3, tr - .1, 26, seed=7) + typed(1090, 620, 400, 3, tr, 26, seed=9)
    els.append(stamp(1400, 668, "TOP SECRET", tr, size=28, rot=-6))
    tj = T("ig", "jeopardy")
    els += [rect(1086, 404, 300, 40, "rgba(232,184,122,.6)", at=tj - .2), lab(1236, 432, "in jeopardy", tj - .2, INK, 28, st="mono", halo=False, scl=True)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_inside():
    """s26: a second line lights, 'professionally unethical'; a building's outline draws round the inspector: the alarm came from inside."""
    tu = T("inside", "unethical")
    els = [rect(1086, 554, 400, 40, "rgba(232,184,122,.6)", at=tu - .6), lab(1286, 582, "professionally unethical", tu - .6, INK, 24, st="mono", halo=False, scl=True)]
    ta = T("inside", "auditor")
    els += [ln([(150, 760), (150, 230), (960, 230), (960, 760)], ta, BONE, 3, dur=1.0)] + \
           [rect(200 + 150 * k, 252, 70, 40, "none", "#8a7a66", 2, 3, round(ta + .5 + .08 * k, 2)) for k in range(5)]
    tal = T("inside", "alarm")
    els += [circ(310, 272, 12, RED, at=tal, fx="pop"), gl(310, 272, 70, tal, .8, "red", pulse=True), lab(330, 200, "from inside", tal + .3, RED, 30, "start")]
    return els


# ================================================================== 3 Frank Olson
def tree(x, y, h, at, c="#1a1511", w=6):
    out = [ln([(x, y), (x + 4, y - h)], at, c, w, draw=False)]
    for k, (f, a, L) in enumerate(((.45, -40, .35), (.6, 35, .3), (.75, -30, .25), (.85, 28, .2))):
        bx, by = x + 4 * f, y - h * f
        out.append(ln([(bx, by), (bx + L * h * math.sin(math.radians(a)), by - L * h * math.cos(math.radians(a)))], at, c, max(2, w - 2), draw=False))
    return out


def sc_lake():
    """s28: late autumn at night: a lake, bare trees, a lodge with lit windows; a small map: Deep Creek Lake and Washington; November 1953."""
    els = [{"k": "water", "y": 650, "h": 420, "op": .85, "in": -1}, poly([[-20, 610], [520, 600], [980, 640], [1300, 618], [1800, 600], [1800, 656], [-20, 656]], "#16120e", at=-1)]
    for x, h in ((120, 260), (250, 210), (1080, 240), (1240, 280), (1380, 220)):
        els += tree(x, 640, h, -1)
    els += [rect(580, 470, 340, 170, "#3a2c20", "#6a5038", 2, 2, -1), poly([[560, 474], [750, 380], [940, 474]], "#2a1f17", "#6a5038", 2, -1),
            rect(820, 390, 30, 60, "#2a1f17", at=-1)]
    for x in (620, 700, 780, 860):
        els += [rect(x, 520, 40, 50, "#f2c98e", at=-1), rect(x, 672, 40, 24, "rgba(242,201,142,.25)", at=-1)]
    els += [gl(750, 545, 260, -1, .45), gl(750, 690, 200, -1, .2)]
    v = View(-80.2, -75.6, 37.9, 40.1, (1212, 166, 456, 228))
    dk, dc = v.p(-79.33, 39.51), v.p(-77.04, 38.90)
    els += [rect(1190, 146, 500, 268, "rgba(16,13,10,.9)", "rgba(255,236,206,.35)", 2, 12, .4),
            {"k": "group", "clip": [1192, 148, 496, 264, 12], "els": [{"k": "map", "land": v.land()}], "in": .4},
            {"k": "pin", "x": dk[0], "y": dk[1], "t": "Deep Creek Lake", "c": GOLD, "in": T("lake", "Deep Creek")},
            {"k": "pin", "x": dc[0], "y": dc[1], "t": "Washington", "c": BONE, "a": "end", "lx": -18, "in": T("lake", "Maryland")}]
    els.append(lab(300, 200, "November 1953", T("lake", "November"), AMBER, 28, st="cap"))
    return {"base": "sky", "tod": "night", "ground": 640, "sun": False, "moon": [1050, 210, 22], "cam": CAM, "els": els}


DINERS = [(480, 290), (630, 300), (780, 280), (1000, 296), (1150, 286), (1300, 300)]


def bottle(x, y, h, at, c="#6a3a1e", e="#e8b87a"):
    w = h * .32
    return [poly([[x - w / 2, y], [x + w / 2, y], [x + w / 2, y - h * .58], [x + w * .2, y - h * .72], [x + w * .2, y - h], [x - w * .2, y - h], [x - w * .2, y - h * .72],
                  [x - w / 2, y - h * .58]], c, e, 2, at), rect(x - w * .35, y - h * .45, w * .7, h * .22, PAPER, at=at)]


def sc_bottle():
    """s29: inside the lodge, after dinner: a table, an after-dinner bottle, small glasses; a dotted drop falls into the bottle; the glasses fill."""
    els = [rect(-20, -20, 1820, 800, "#22180f", at=-1, op=.55), rect(1300, 180, 260, 220, "#101a2a", "#6a5038", 6, 3, -1)]
    els += static(lamp(889, 200, -1, cord=150, op=.8, r=320))
    for x, h in DINERS:
        els.append(ppl(x, 760, h, -1, "#5f574f"))
    els += [rect(360, 560, 1060, 24, "#a89e8c", "#cfc5b2", 1.5, 4, -1), poly([[360, 584], [1420, 584], [1400, 700], [380, 700]], "#8a8170", at=-1)]
    els += bottle(889, 560, 150, -1)
    tl = T("bottle", "LSD")
    els += drop(889, 380, tl, s=1.2)
    ts = T("bottle", "served")
    for k, x in enumerate((480, 630, 780, 1000, 1150, 1300)):
        els += glass(x, 560, -1, h=44, fill_at=round(ts + .2 * k, 2))
    return {"base": "dark", "cam": CAM, "els": els}


def add_olson():
    """s30: one of the diners lit by a soft glow: Frank Olson; a small tag, Camp Detrick."""
    tf = T("olson", "Frank Olson")
    x, h = DINERS[4]
    return [gl(x, 760 - h * .7, 190, tf - .3, .6), ppl(x, 760, h, tf - .3, "#cbbca8", fx="fade"), rect(360, 560, 1060, 24, "#a89e8c", "#cfc5b2", 1.5, 4, tf - .3),
            poly([[360, 584], [1420, 584], [1400, 700], [380, 700]], "#8a8170", at=tf - .3)] + glass(x, 560, tf - .3, h=44, fill_at=tf - .3) + \
           glass(1000, 560, tf - .3, h=44, fill_at=tf - .3) + [lab(x, 420, "Frank Olson", tf, BONE, 32)] + tag(x, 372, "Camp Detrick", T("olson", "Camp Detrick"), DIM, 24)


RTV = View(-80.6, -73.4, 38.2, 41.3, (100, 140, 1580, 620))


def chipd(x, y, t, at, c=AMBER):
    return tag(x, y, t, at, c, 26)


def sc_route():
    """s31: the route: Deep Creek Lake, Washington, New York; the line draws to New York; '19 Nov', '24 Nov'."""
    dk, wa, ny, fr = RTV.p(-79.33, 39.51), RTV.p(-77.04, 38.90), RTV.p(-73.99, 40.75), RTV.p(-77.41, 39.41)
    els = [{"k": "map", "land": RTV.land(), "in": -1},
           {"k": "pin", "x": dk[0], "y": dk[1], "t": "Deep Creek Lake", "c": GOLD, "a": "end", "lx": -20, "in": .5},
           {"k": "pin", "x": wa[0], "y": wa[1], "t": "Washington", "c": BONE, "in": .8},
           {"k": "pin", "x": ny[0], "y": ny[1], "t": "New York", "c": GOLD, "a": "end", "lx": -20, "in": T("route", "New York")}]
    els += chipd(dk[0], dk[1] - 60, "19 Nov", .9)
    tt = T("route", "took him")
    els += [ln([dk, (fr[0], fr[1] - 10), (wa[0] + 120, wa[1] - 120), (ny[0] - 20, ny[1] + 6)], tt, AMBER, 4, dur=1.6, curve=True)]
    els += chipd(ny[0] - 40, ny[1] - 64, "24 Nov", T("route", "doctor"))
    return {"base": "map", "cam": CAM, "els": els}


def sc_nine():
    """s32: nine day squares, 19 to 28 November 1953, fill one by one; a hotel at night, its tenth-floor window lit; the light goes out."""
    tn = T("nine", "Nine days")
    els = []
    for k in range(10):
        x = 120 + 76 * k
        els += [rect(x, 250, 62, 62, "#2a2420", "#cbbca8", 2, 6, .2 + .05 * k), lab(x + 31, 346, str(19 + k), .3 + .05 * k, DIM, 24, st="mono")]
        if k:
            els.append(rect(x, 250, 62, 62, "rgba(232,184,122,.55)", at=round(tn + .22 * k, 2)))
    els += glass(151, 300, .3, h=40, fill_at=.4) + [lab(500, 214, "9 days", tn + 1.2, AMBER, 32), lab(500, 390, "November 1953", .4, DIM, 26, st="cap")]
    hx0, hx1, top, base = 1100, 1440, 160, 760
    els += [rect(hx0, top, hx1 - hx0, base - top, "#25211d", "#5a524a", 2, 2, -1), rect(hx0 - 10, top - 10, hx1 - hx0 + 20, 14, "#3a332d", at=-1)]
    fh = (base - top) / 13
    for f in range(13):
        y = base - fh * (f + 1) + fh * .25
        for c in range(5):
            x = hx0 + 22 + c * 64
            lit = (f == 9 and c == 2)
            if lit:
                els += [rect(x - 6, y - 6, 52, fh * .5 + 12, "rgba(242,201,142,.3)", r=4, at=-1), rect(x, y, 40, fh * .5, "#f2c98e", at=-1)]
            else:
                els.append(rect(x, y, 40, fh * .5, "#3a3128" if (f * 5 + c) % 7 else "#4a3f30", at=-1))
    wy = base - fh * 10 + fh * .25
    for f in range(10):
        els.append(ln([(hx1 + 18, base - fh * f), (hx1 + 34, base - fh * f)], -1, DIM, 2, draw=False))
    els += [ln([(hx1 + 26, base), (hx1 + 26, wy + 12)], -1, DIM, 2, draw=False), lab(hx1 + 50, wy + 22, "tenth floor", .5, DIM, 26, "start")]
    tw = T("nine", "death")
    els += [veil(hx0 + 22 + 128 - 7, wy - 7, 54, fh * .5 + 14, tw, "#25211d", dur=1.4), rect(hx0 + 150, wy, 40, fh * .5, "#3a3128", at=tw + 1.0)]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


def sc_told():
    """s33: a family house at dusk, one window lit; a typed card, 'suicide'; behind it, hidden and grey, a dashed tag: LSD."""
    els = [rect(-20, 700, 1820, 320, "#1c1712", at=-1), ln([(-20, 700), (1800, 700)], -1, "#4a3e30", 2, draw=False), gl(480, 560, 420, -1, .25)]
    els += static(house(480, 700, 380, -1, lit=True)) + tree(800, 700, 260, -1) + tree(160, 700, 220, -1)
    tn = T("told", "Nobody")
    els += [rect(1300, 500, 170, 70, "rgba(40,36,32,.6)", "#8a8278", 2, 10, tn, style="inferred", op=.6), lab(1385, 546, "LSD", tn + .1, "#8a8278", 30, halo=False)]
    tl = T("told", "suicide")
    els += [rect(980, 250, 440, 270, PAPER, PAPER_D, 2, 4, tl - .4, fx="rise"), lab(1010, 300, "CAUSE OF DEATH", tl - .2, TYPE, 24, "start", st="mono", halo=False, scl=True),
            lab(1200, 420, "suicide", tl + .2, INK, 52, st="mono", halo=False, scl=True, fx="type", dur=.6)]
    return {"base": "dark", "cam": CAM, "els": els}


def xyr(y):
    return round(200 + (y - 1950) / 30 * 1380, 1)


def sc_years22():
    """s34: a time line, 1953 to 1975, drawn with 22 ticks; a report, 1975; the hidden tag now solid: LSD."""
    els = [axis(200, 1580, 560, [(xyr(y), str(y)) for y in (1950, 1960, 1970, 1980)], .2)]
    t0 = T("years22", "twenty-two")
    els += [dot(xyr(1953), 520, 9, BONE, .4), lab(xyr(1953), 488, "1953", .5, BONE, 26), ln([(xyr(1953), 520), (xyr(1975), 520)], t0 - .3, AMBER, 8, dur=1.6)]
    els += [ln([(xyr(1953 + k), 508), (xyr(1953 + k), 532)], round(t0 - .3 + .07 * k, 2), AMBER, 2.5, draw=False) for k in range(23)]
    els += [lab(xyr(1964), 470, "22 years", t0 + .8, AMBER, 32)]
    tr = T("years22", "report")
    els += sheet(xyr(1975) - 80, 250, 160, 200, tr - .3) + typed(xyr(1975) - 60, 320, 120, 5, tr - .1, 24, seed=12) + \
        [lab(xyr(1975), 290, "1975", tr - .1, TYPE, 24, st="mono", halo=False, scl=True)]
    els += tag(xyr(1975) + 170, 300, "LSD", tr + .5, LILAC, 30)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_whitehouse():
    """s35: the White House, schematic; small figures at its door; 'July 1975'; '$750,000' paid by Congress in 1976."""
    wall_, edge = "#e2dccf", "#9a9284"
    els = [rect(-20, 700, 1820, 320, "#2a3020", at=-1), ln([(-20, 700), (1800, 700)], -1, "#4a5238", 2, draw=False), gl(889, 500, 620, -1, .2)]
    els += [rect(380, 450, 260, 250, wall_, edge, 2, 2, -1), rect(1140, 450, 260, 250, wall_, edge, 2, 2, -1), rect(640, 380, 500, 320, wall_, edge, 2, 2, -1),
            poly([[720, 380], [890, 300], [1060, 380]], wall_, edge, 2, -1), rect(370, 440, 280, 14, "#cfc8ba", at=-1), rect(1130, 440, 280, 14, "#cfc8ba", at=-1),
            rect(630, 370, 520, 14, "#cfc8ba", at=-1)]
    els += [rect(745 + 54 * k, 392, 18, 308, "#f6f2ea", edge, 1, 2, -1) for k in range(6)]
    for x0 in (400, 1160):
        for r in range(2):
            els += [rect(x0 + 22 + 58 * k, 480 + 100 * r, 30, 56, "#6a7078", at=-1) for k in range(4)]
    els += [rect(860, 610, 60, 90, "#4a4038", at=-1), ln([(890, 300), (890, 240)], -1, "#cfc8ba", 2, draw=False), poly([[890, 240], [930, 250], [890, 262]], RED, at=-1)]
    ta = T("whitehouse", "apologised")
    els += [ppl(830 + 26 * k, 704, 74 - 6 * (k % 2), round(ta + .1 * k, 2), "#3a3330") for k in range(5)] + [lab(889, 234, "July 1975", ta + .3, BONE, 28)]
    tm = T("whitehouse", "seven hundred")
    els += chip(1560, 290, "$750,000", GOLD, tm, 32) + [lab(1560, 356, "Congress, 1976", tm + .3, BONE, 26)]
    return {"base": "sky", "tod": "dusk", "ground": 700, "sun": False, "cam": CAM, "els": els}


def card_official(x, y, at):
    return [rect(x - 90, y - 150, 180, 140, PAPER, PAPER_D, 1.5, 3, at, fx="pop")] + typed(x - 70, y - 120, 140, 5, at + .1, 22, seed=2)


def card_family(x, y, at):
    return [rect(x - 90, y - 150, 180, 140, "rgba(201,193,238,.08)", LILAC, 2.5, 3, at, fx="pop", style="claimed")] + \
           [ln([(x - 70, y - 120 + 22 * j), (x + 60 - 20 * (j % 2), y - 120 + 22 * j)], at + .1, LILAC, 3, "claimed", draw=False) for j in range(5)]


def sc_balance():
    """s36: a balance: 'the official account' on one pan, 'his family's account' (dotted) on the other; the beam level."""
    to, tf = T("balance", "official"), T("balance", "His family")
    els = balance(889, 300, 760, 0, 760, -1, left=lambda x, y, at: card_official(x, y, to), right=lambda x, y, at: card_family(x, y, tf), drop_=230)
    els += [lab(509, 600, "the official account", to + .3, BONE, 30), lab(1269, 600, "his family's account", tf + .3, LILAC, 30)]
    tb = T("balance", "breakdown")
    els += [lab(509, 650, "a breakdown, a jump", tb + .2, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_level():
    """s40: the balance stays level; a '?' glows above the beam."""
    return qmark(889, 230, T("level", "never settled"), 110)


def sc_exhume():
    """s37: a quiet cemetery at dawn, a small team at a distance (1994); a head drawn in outline, a dashed mark at the temple: before the fall?"""
    els = [gl(420, 600, 520, -1, .35, "sun"), rect(-20, 620, 1820, 400, "#1d1913", at=-1), ln([(-20, 620), (1800, 620)], -1, "#4a3e30", 2, draw=False)]
    for x, s in ((150, .6), (250, .5), (700, .55), (820, .45)):
        els.append(rect(x, 620 - 110 * s, 60 * s, 110 * s, "#4a4640", "#6a665e", 1.5, 18 * s, -1))
    els += [rect(380, 470, 90, 150, "#6a665e", "#8a867e", 2, 26, -1)] + [ppl(560 + 40 * k, 640, 100 - 8 * (k % 2), round(.4 + .1 * k, 2), "#3a3632") for k in range(4)]
    els.append(lab(420, 200, "1994", T("exhume", "nineteen"), AMBER, 30, st="cap"))
    tf = T("exhume", "forensic")
    hx, hy, hs = 1320, 430, 430
    els += [head(hx, hy, hs, tf - .3, "rgba(245,236,220,.04)", BONE, 3, fx="fade")]
    ti = T("exhume", "injury")
    mx, my = hx + .26 * hs, hy - .2 * hs
    els += [circ(mx, my, 24, "rgba(240,176,106,.15)", AMBER, 3, ti, style="inferred", fx="pop"), ln([(mx + 20, my - 20), (1480, 220)], ti + .3, AMBER, 2, "inferred", .4)]
    els += tag(1480, 196, "before the fall?", T("exhume", "before the fall"), AMBER, 26, "inferred")
    return {"base": "dark", "cam": CAM, "els": els}


def sc_unknown():
    """s38: a record card, cause of death 'suicide'; 'REOPENED'; the word struck through and 'unknown' typed in; 'no charges'."""
    els = [rect(480, 220, 820, 440, PAPER, PAPER_D, 2, 6, .2, fx="rise"), lab(530, 290, "CAUSE OF DEATH", .4, TYPE, 26, "start", st="mono", halo=False, scl=True),
           lab(890, 420, "suicide", .5, INK, 60, st="mono", halo=False, scl=True)]
    tr = T("unknown", "reopened")
    els.append(stamp(1150, 300, "REOPENED", tr, size=30, rot=-8))
    tn = T("unknown", "charged no one")
    els += tag(1500, 520, "no charges", tn, DIM, 26)
    tc = T("unknown", "changed")
    els += [ln([(740, 402), (1040, 402)], tc, STAMP, 7, dur=.4), lab(890, 560, "unknown", T("unknown", "unknown") - .1, STAMP, 60, st="mono", halo=False, scl=True, fx="type", dur=.7)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_court():
    """s39: a court: a judge's bench, a file 'suit, 2012'; the gavel: 'dismissed, 2013'; a dotted '?' stays over the file."""
    els = [ppl(889, 560, 270, -1, "#3d3833"), rect(560, 390, 660, 290, "#4a3424", "#8a6a48", 2, 4, -1), rect(540, 380, 700, 22, "#5a4030", "#8a6a48", 1.5, 3, -1),
           circ(889, 520, 54, "none", "#8a6a48", 3, -1), rect(-20, 760, 1820, 260, FLOOR, at=-1), gl(889, 420, 420, -1, .25)]
    els += static(table(300, 600, 300, -1, h=160))
    ts = T("court", "sued")
    els += [rect(210, 420, 180, 170, PAPER, PAPER_D, 1.5, 3, ts - .2, fx="rise"), lab(300, 470, "suit, 2012", ts, TYPE, 24, st="mono", halo=False, scl=True)] + \
           typed(232, 510, 136, 3, ts + .2, 22)
    td = T("court", "dismissed")
    els += gavel(1290, 330, td - .3) + [lab(1290, 500, "dismissed, 2013", td + .2, BONE, 30)]
    tq = T("court", "without deciding")
    els += qmark(300, 380, tq, 90)
    return {"base": "dark", "cam": CAM, "els": els}



# ================================================================== 4 Seven boxes
CAB = "#1d1712"


def sc_cabinet():
    """s41: a cabinet of 152 folders; the order slip signed Gottlieb and Helms; two figures at an exit; the folders turn to dashed
    outlines in a wave, under a faint fire glow: 152 files."""
    els = [rect(110, 150, 960, 580, CAB, "#5a4632", 2, 6, -1)]
    pos = [(130 + 49 * c, 175 + 68 * r) for c in range(19) for r in range(8)]          # column by column, left to right
    for x, y in pos:
        els.append(folder(x, y + 8, 40, 50, -1))
    tg, th = T("cabinet", "Gottlieb ordered"), T("cabinet", "Helms")
    els += [rect(1530, 540, 120, 220, "#120e0b", "#8a6a48", 2, 3, -1)]
    els += [ppl(1250, 760, 230, tg - .2, "#9a9288"), lab(1250, 500, "Gottlieb", tg, BONE, 28),
            arr([(1200, 600), (1140, 520), (1082, 470)], tg + .5, RED, 3, "inferred", .6, curve=True), lab(1130, 440, "destroy", tg + .7, RED, 26)]
    els += [ppl(1400, 760, 240, th - .2, "#7a7268"), lab(1400, 490, "Helms", th, BONE, 28)] + tag(1400, 430, "approved", th + .4, AMBER, 24)
    tl = T("cabinet", "about to leave")
    els += [gl(1590, 650, 150, tl, .6), ln([(1290, 700), (1460, 690), (1525, 680)], tl + .2, MUTED, 2, "claimed", .6, curve=True)]
    tw = T("cabinet", "hundred and fifty-two") - .3
    els.append(gl(590, 450, 560, tw, .32, "fire"))
    for k, (x, y) in enumerate(pos):
        at = round(tw + .006 * k, 3)
        els += [veil(x - 2, y + 2, 44, 58, at, CAB, dur=.35), folder(x, y + 8, 40, 50, at, c="none", fill="rgba(205,181,138,.04)", edge="#a88a64", style="inferred")]
    els += [lab(590, 770, "152 files", tw + .8, AMBER, 32), lab(1370, 150, "January 1973", .4, AMBER, 26, st="cap")]
    return {"base": "dark", "cam": CAM, "els": els}


def shield(x, y, s, at, c=GREEN):
    return poly([(x, y - s * .55), (x + s * .45, y - s * .38), (x + s * .4, y + s * .1), (x, y + s * .5), (x - s * .4, y + s * .1), (x - s * .45, y - s * .38)],
                "rgba(143,217,176,.1)", c, 3, at, fx="pop")


def sc_reasons():
    """s42: Gottlieb's three reasons pop as named: a shield over researchers; a torn page with a '?'; a tall stack cut down to a short one."""
    tr, tm, tp = T("reasons", "protect"), T("reasons", "misread"), T("reasons", "paperwork")
    els = [shield(400, 360, 190, tr)] + [ppl(330 + 70 * k, 640, 150, round(tr + .1 * k, 2), "#9a9288") for k in range(3)] + [lab(400, 700, "to protect researchers", tr + .2, BONE, 28)]
    els += [poly([(790, 330), (990, 330), (990, 560), (960, 580), (930, 556), (900, 584), (870, 556), (840, 582), (810, 558), (790, 576)], PAPER, PAPER_D, 2, tm - .3, fx="pop")]
    els += typed(812, 370, 150, 6, tm - .1, 24, seed=18) + [lab(890, 528, "?", tm + .2, STAMP, 64, st="serif", halo=False, fx="pop"), lab(890, 700, "misread", tm + .2, BONE, 28)]
    for k in range(26):
        els.append(rect(1240, 640 - 11 * k, 150, 9, PAPER, PAPER_D, 1, 1, round(tp - 1.2 + .02 * k, 2)))
    els += [arr([(1405, 520), (1460, 560)], tp, AMBER, 3, dur=.4)]
    for k in range(6):
        els.append(rect(1470, 640 - 11 * k, 150, 9, PAPER, PAPER_D, 1, 1, round(tp + .3 + .03 * k, 2)))
    els.append(lab(1430, 700, "less paperwork", tp + .3, BONE, 28))
    return {"base": "dark", "cam": CAM, "els": els}


def sc_search75():
    """s43: a records centre in cutaway: in 'drug files' torches sweep and ticks pop (searched, 1975); next door, 'budget office' stays
    dark, seven boxes faint inside (not searched)."""
    els = [rect(360, 220, 1280, 540, "#211a14", "#6a5a48", 2.5, 4, -1), poly([[340, 222], [1000, 150], [1660, 222]], "#2a2019", "#6a5a48", 2.5, -1),
           rect(1010, 232, 620, 518, "#100c09", at=-1), rect(990, 230, 20, 530, "#3a2c20", at=-1), rect(352, 600, 16, 160, "#0d0b09", at=-1)]
    els += shelf_unit(420, 960, 280, 700, 3, 52, 44, .75, 31)
    els += shelf_unit(1060, 1590, 280, 700, 3, 52, 44, .22, 32, gaps=1.0)
    for k in range(7):
        els += static(abox(1120 + 64 * k, 588, 56, 48, -1, op=.35, d=10))
    ts = T("search75", "searched")
    els += [ppl(600, 760, 190, ts - .4, "#7a7268"), poly([[628, 600], [628, 614], [960, 520], [900, 400]], "rgba(255,240,200,.12)", at=ts), gl(632, 606, 30, ts, .9)]
    els += [tick(470 + 110 * k, 330 + 140 * (k % 3), round(ts + .3 + .15 * k, 2), GREEN, .9, 5) for k in range(5)]
    els += [lab(680, 198, "drug files", .4, BONE, 30), lab(1320, 198, "budget office", .5, BONE, 30), lab(680, 740, "searched, 1975", T("search75", "nineteen") + .6, GREEN, 28)]
    els.append(lab(1320, 740, "not searched", T("search75", "nobody checked"), MUTED, 28))
    return {"base": "dark", "cam": CAM, "els": els}


def add_foia():
    """s44: John Marks, 1977: a freedom of information request flies to the records centre's door."""
    tm = T("foia", "John Marks")
    els = [ppl(200, 760, 230, tm - .3, "#cbbca8"), lab(200, 500, "John Marks", tm, BONE, 28)]
    tl = T("foia", "freedom")
    els += envelope(230, 600, 90, tl) + [ln([(280, 600), (330, 640), (360, 680)], tl + .4, AMBER, 3, "claimed", .6, curve=True)] + envelope(372, 690, 60, tl + .9)
    els += [lab(244, 420, "freedom of information", tl + .2, AMBER, 26)]
    return els


def add_found():
    """s45: back in the opening's warehouse: the torch beam brightens and the seven boxes glow gold."""
    tf = T("found", "seven")
    els = [poly([[506, 584], [506, 600], [1010, 574], [740, 468]], "rgba(255,240,200,.16)", at=2.5)]
    for k, x in enumerate(BOX_X):
        els.append(gl(x + BOX_W / 2, BOX_Y + BOX_H / 2, 110, round(tf - .4 + .1 * k, 2), .55))
    return els


def sc_stack():
    """s46: forms rise out of a box as named (advance approval, voucher, account); a stack of pages grows: 5,000 pages, then dashed
    to 8,000 (perhaps)."""
    els = [poly([[150, 520], [520, 520], [490, 480], [180, 480]], "#1a130d", "rgba(255,236,206,.3)", 1.2, -1), rect(150, 520, 370, 230, CARD, "rgba(255,236,206,.3)", 1.5, 3, -1),
           rect(255, 560, 160, 56, PAPER, at=-1), gl(335, 470, 300, -1, .25)]
    forms = [(560, "Approvals", "ADVANCE"), (790, "Vouchers", "VOUCHER"), (1020, "Accounts", "ACCOUNT")]
    for k, (x, ph, t) in enumerate(forms):
        at = T("stack", ph) - .2
        els += [rect(x, 170, 190, 240, PAPER, PAPER_D, 1.5, 3, at, fx="rise"), lab(x + 95, 208, t, at + .1, STAMP, 24, st="mono", halo=False, scl=True, fx="rise")]
        els += typed(x + 20, 240, 150, 6, at + .2, 24, seed=40 + k)
    t5 = T("stack", "Five thousand")
    x0, w, base = 1290, 200, 740
    for k in range(50):
        els.append(rect(x0, base - 6 * (k + 1), w, 5, PAPER, PAPER_D, .8, 1, round(t5 - .4 + .022 * k, 3)))
    t8 = T("stack", "eight thousand")
    els += [rect(x0, base - 480, w, 180, "rgba(239,230,210,.06)", PAPER, 2, 2, t8 - .2, style="inferred")]
    els += [ln([(x0 + w + 16, base), (x0 + w + 16, base - 300)], t5 + .6, BONE, 2, draw=False), lab(x0 + w + 30, base - 290, "5,000 pages", t5 + .7, BONE, 26, "start"),
            ln([(x0 + w + 16, base - 300), (x0 + w + 16, base - 480)], t8, BONE, 2, "inferred", draw=False), lab(x0 + w + 30, base - 470, "8,000?", t8 + .1, BONE, 26, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def add_survived():
    """s50: a ghost row of dashed folders, 'destroyed'; the stack of receipts lit, 'survived'."""
    td, ts = max(1.8, T("survived", "destroyed")), T("survived", "survived")
    els = [folder(570 + 66 * k, 520, 56, 70, round(td + .04 * k, 2), c="none", fill="rgba(205,181,138,.04)", edge="#a88a64", style="inferred") for k in range(10)]
    els += [lab(900, 640, "destroyed", td + .3, MUTED, 28), gl(1390, 520, 260, ts, .45), lab(1390, 220, "survived", ts + .1, GOLD, 34)]
    return els


def sc_diary():
    """s47: the analogy: a diary burned away (dashed, a fire glow); a bank statement; an amber dotted trail from it to a university,
    a hospital and a house: follow the money."""
    td = T("diary", "diaries")
    els = [gl(360, 470, 260, td, .5, "fire"), rect(220, 300, 280, 340, "rgba(90,58,38,.12)", "#a8805a", 2.5, 8, td, style="inferred"),
           ln([(250, 300), (250, 640)], td, "#a8805a", 2, "inferred", draw=False), lab(360, 700, "diaries: burned", td + .3, MUTED, 28)]
    rnd = random.Random(9)
    els += [dot(round(rnd.uniform(240, 480), 1), round(rnd.uniform(320, 620), 1), 3, "#8a7a66", td + .4) for _ in range(14)]
    tb = T("diary", "bank statements")
    els += [rect(680, 190, 400, 470, PAPER, PAPER_D, 2, 4, tb - .2, fx="rise"), lab(710, 236, "STATEMENT", tb, TYPE, 24, "start", st="mono", halo=False, scl=True)]
    for j in range(9):
        y = 290 + 40 * j
        aw = rnd.uniform(26, 58)                 # an amount column with no figures in it: the sums are not invented
        els += [ln([(710, y), (790, y)], tb + .1, "#8a7a66", 3, draw=False), ln([(810, y), (810 + rnd.uniform(90, 140), y)], tb + .1, "#6a5a48", 3, draw=False),
                lab(1046 - aw, y + 7, "$", tb + .1, TYPE, 20, "end", st="mono", halo=False, scl=True), ln([(1056 - aw, y), (1060, y)], tb + .1, "#6a5a48", 5, draw=False)]
    els.append(lab(880, 700, "bank statements", tb + .2, BONE, 28))
    tf = T("diary", "follow")
    els += [ln([(1080, 330), (1250, 300), (1340, 320)], tf - .4, AMBER, 3, "claimed", .6, curve=True), ln([(1080, 450), (1360, 470), (1490, 500)], tf - .2, AMBER, 3, "claimed", .6, curve=True),
            ln([(1080, 570), (1250, 650), (1330, 690)], tf, AMBER, 3, "claimed", .6, curve=True)]
    els += uni(1400, 370, 120, tf - .1) + hosp(1560, 560, 110, tf + .1) + house(1400, 740, 110, tf + .3, fx="pop")
    els.append(lab(1450, 200, "follow the money", tf + .3, AMBER, 30))
    return {"base": "dark", "cam": CAM, "els": els}


SENATORS = [360, 560, 760, 1020, 1220, 1420]


def sc_hearing():
    """s48: a Senate hearing room: senators on the dais, Stansfield Turner at the witness table, seven boxes beside him; March to July;
    3 August 1977; Edward Kennedy lit: without consent."""
    els = [rect(-20, 150, 1820, 320, "#24190f", at=-1)] + [ln([(x, 150), (x, 470)], -1, "#2e2116", 2, draw=False) for x in range(60, 1780, 120)]
    for x in SENATORS:
        els.append(ppl(x, 478, 290, -1, "#5f574f"))
    els += [rect(240, 330, 1300, 150, "#4a3424", "#8a6a48", 2, 4, -1), rect(220, 320, 1340, 18, "#5a4030", "#8a6a48", 1.5, 3, -1)]
    els += [ppl(890, 762, 250, .3, "#8a8278"), rect(620, 690, 540, 70, "#4a3424", "#8a6a48", 2, 3, .3), rect(600, 680, 580, 14, "#5a4030", "#8a6a48", 1.5, 3, .3),
            lab(850, 566, "Stansfield Turner", T("hearing", "Turner"), BONE, 26, "end")]
    for k in range(7):
        x, y = (1220 + 62 * k, 712) if k < 4 else (1251 + 62 * (k - 4), 664)
        els += abox(x, y, 56, 48, .4 + .05 * k, d=10, fx="pop")
    tm = T("hearing", "three months")
    els += calendar(110, 560, 120, 130, "", tm, month="MARCH", year="1977") + calendar(300, 560, 120, 130, "", tm + .6, month="JULY", year="1977")
    els += [arr([(236, 625), (294, 625)], tm + .4, AMBER, 3, dur=.3), lab(265, 730, "3 months", tm + .8, AMBER, 26)]
    els.append(lab(1330, 186, "3 August 1977", T("hearing", "That August"), AMBER, 26, st="cap"))
    tk = T("hearing", "Kennedy")
    els += [gl(760, 300, 170, tk, .55), ppl(760, 478, 290, tk, "#cbbca8", fx="fade"), rect(240, 330, 1300, 150, "#4a3424", "#8a6a48", 2, 4, tk),
            rect(220, 320, 1340, 18, "#5a4030", "#8a6a48", 1.5, 3, tk), lab(760, 186, "Edward Kennedy", tk + .1, BONE, 26)]
    els.append(lab(760, 418, "without consent", T("hearing", "consent"), GOLD, 30))
    return {"base": "dark", "cam": CAM, "els": els}


def add_little():
    """s49: two bars beside the boxes: 'the scale' fills solid; 'what was done' stays a dashed outline with a '?'."""
    t0 = T("little", "scale")
    return [rect(1220, 560, 380, 24, AMBER, at=t0, fx="fill"), lab(1200, 580, "the scale", t0, BONE, 26, "end"),
            rect(1220, 610, 380, 24, "none", BONE, 2, 3, T("little", "little more"), style="inferred"), lab(1200, 630, "what was done", T("little", "little more"), BONE, 26, "end"),
            lab(1625, 632, "?", T("little", "little more") + .3, LILAC, 40, st="serif")]


# ================================================================== 5 Montreal
def mansion(x, base, s, at, fx=None, lit=True):
    """Ravenscrag, the Allan Memorial Institute: a grey stone villa with a square tower (schematic), base on `base`, x = its centre."""
    st_, rf = "#8a8478", "#3a3a40"
    w, h = 300 * s, 120 * s
    els = [rect(x - w / 2, base - h, w, h, st_, "#b8b2a6", 1.5, 2, at, fx=fx), poly([[x - w / 2 - 8 * s, base - h], [x - w / 2 + 30 * s, base - h - 34 * s], [x + w / 2 - 30 * s, base - h - 34 * s],
                                                                                    [x + w / 2 + 8 * s, base - h]], rf, at=at, fx=fx),
           rect(x - 70 * s, base - h - 110 * s, 64 * s, 110 * s, st_, "#b8b2a6", 1.5, 2, at, fx=fx), poly([[x - 78 * s, base - h - 110 * s], [x - 38 * s, base - h - 150 * s],
                                                                                                          [x + 2 * s, base - h - 110 * s]], rf, at=at, fx=fx)]
    for r in range(2):
        for k in range(6):
            els.append(rect(x - w / 2 + 20 * s + 46 * s * k, base - h + 20 * s + 50 * r * s, 22 * s, 28 * s, "#f2c98e" if (lit and (k + r) % 3) else "#2a2826", at=at, fx=fx))
    els.append(rect(x - 52 * s, base - h - 90 * s, 26 * s, 30 * s, "#f2c98e" if lit else "#2a2826", at=at, fx=fx))
    return els


NEV = View(-80.5, -68.5, 37.8, 47.2, (110, 160, 620, 580))


def sc_north():
    """s51: a map, Washington to Montreal, a dotted line north; Mount Royal and the Allan Memorial Institute above the city's lights;
    Ewen Cameron."""
    wa, mo = NEV.p(-77.04, 38.90), NEV.p(-73.57, 45.50)
    els = [rect(96, 150, 650, 600, "rgba(16,13,10,.85)", "rgba(255,236,206,.3)", 2, 14, -1),
           {"k": "group", "clip": [98, 152, 646, 596, 14], "els": [{"k": "map", "land": NEV.land()}], "in": -1},
           {"k": "pin", "x": wa[0], "y": wa[1], "t": "Washington", "c": BONE, "in": .3}, {"k": "pin", "x": mo[0], "y": mo[1], "t": "Montreal", "c": GOLD, "in": .5},
           ln([(wa[0], wa[1] - 10), (wa[0] + 80, (wa[1] + mo[1]) / 2), (mo[0], mo[1] + 12)], .4, AMBER, 3, "claimed", 1.0, curve=True)]
    hill = [[800, 780], [900, 640], [1080, 520], [1260, 440], [1420, 430], [1560, 480], [1700, 560], [1800, 600], [1800, 780]]
    els += [poly(hill, "#1d2418", "rgba(160,190,140,.25)", 1.5, -1, curve=True)]
    rnd = random.Random(23)
    for _ in range(60):
        x = rnd.uniform(860, 1780)
        ytop = 780
        for (ax, ay), (bx, by) in zip(hill, hill[1:]):
            if ax <= x <= bx:
                ytop = ay + (by - ay) * (x - ax) / (bx - ax)
        y = rnd.uniform(ytop + 14, min(ytop + 120, 770))
        els.append(circ(round(x, 1), round(y, 1), round(rnd.uniform(9, 16), 1), "#162012", at=-1))
    els += [dot(round(rnd.uniform(800, 1760), 1), round(rnd.uniform(740, 790), 1), 2.5, "#f2c98e", -1, op=.8) for _ in range(40)]
    tm = T("north", "Allan Memorial")
    els += mansion(1330, 470, 1.0, tm - .2, fx="pop") + [gl(1330, 420, 220, tm, .35), lab(1330, 168, "Allan Memorial Institute", tm + .2, BONE, 28)]
    tc = T("north", "Ewen Cameron")
    els += [ppl(1000, 760, 220, tc - .2, "#cbbca8"), lab(1000, 514, "Ewen Cameron", tc, BONE, 28)]
    els += tag(1000, 432, "World Psychiatric Association", T("north", "World"), DIM, 24)
    tw = T("north", "wipe away")
    hx, hy, hs = 1000, 262, 170
    els += [head(hx, hy, hs, tw - .4, "#16120f", "rgba(255,236,206,.35)", 2, fx="pop")]
    els += [ln([(hx - 42, hy - 52 + 14 * j), (hx + 22, hy - 50 + 14 * j)], tw - .2, "#8a8278", 3, draw=False) for j in range(4)]
    els += [veil(hx - 48, hy - 62, 80, 60, tw + .5, "#16120f", dur=.7)]
    tr = T("north", "rebuild")
    els += [ln([(hx - 38, hy - 48 + 18 * j), (hx + 20, hy - 48 + 18 * j)], tr + .2 * j, LILAC, 3, "claimed", .4) for j in range(3)]
    return {"base": "dark", "cam": CAM, "els": els}


def sc_flow():
    """s52: the money's path: CIA, the dotted Human Ecology front, the institute in Montreal; from 1957."""
    t0 = .3
    els = [rect(150, 390, 220, 160, "#2a2420", BONE, 2.5, 10, t0, fx="pop"), lab(260, 486, "CIA", t0 + .1, BONE, 42, st="serif"),
           arr([(390, 470), (600, 470)], t0 + .5, AMBER, 3)]
    els += [rect(620, 400, 280, 220, "rgba(201,193,238,.06)", LILAC, 2.5, 3, t0 + .9, style="claimed"),
            poly([[606, 400], [760, 320], [914, 400]], "rgba(201,193,238,.06)", LILAC, 2.5, t0 + .9, style="claimed")]
    els += [ln([(650 + 50 * k, 420), (650 + 50 * k, 612)], t0 + 1.0, LILAC, 2.5, "claimed", draw=False) for k in range(5)]
    els += [lab(760, 670, "Human Ecology", t0 + 1.1, LILAC, 30), arr([(930, 470), (1140, 470)], T("flow", "his work"), AMBER, 3)]
    els += mansion(1390, 560, .8, T("flow", "his work") + .4, fx="pop") + [lab(1390, 620, "Montreal", T("flow", "his work") + .6, BONE, 28)]
    els += [lab(889, 200, "from 1957", T("flow", "nineteen"), AMBER, 30, st="cap")] + tag(1040, 410, "subproject 68", T("flow", "front"), DIM, 24)
    return {"base": "dark", "cam": CAM, "els": els}


def moon_icon(x, y, r, at, c="#d8d2c0"):
    return [circ(x, y, r, c, at=at, fx="pop"), circ(x + r * .45, y - r * .25, r * .9, "#1f1b18", at=at, fx="pop")]


def sc_room():
    """s53: a hospital room at night, a patient asleep; weeks pass as small moons; electroshocks; a tape on a loop for 16 hours a day."""
    els = [rect(120, 150, 1540, 610, "#1f1b18", "#4a4038", 2, 6, -1), rect(-20, 760, 1820, 260, FLOOR, at=-1), rect(1300, 200, 260, 220, "#0f1626", "#6a6058", 6, 3, -1)]
    els += [circ(1470, 270, 26, "#e8e2cf", at=-1), circ(1482, 263, 23, "#0f1626", at=-1), gl(1430, 300, 160, -1, .2, "blue")]
    els += [rect(270, 640, 640, 60, "#4a4440", "#8a8278", 2, 6, -1), rect(270, 700, 20, 60, "#3a3430", at=-1), rect(890, 700, 20, 60, "#3a3430", at=-1),
            rect(250, 560, 20, 200, "#5a524a", at=-1), rect(300, 586, 110, 54, "#d8d2c4", at=-1), circ(352, 572, 28, "#9a9288", at=-1),
            poly([[380, 640], [400, 596], [600, 588], [880, 600], [900, 640]], "#6a6e78", "#9aa0aa", 1.5, -1, curve=True), gl(560, 600, 300, -1, .15, "blue")]
    tw = T("room", "weeks")
    els += [m for k in range(7) for m in moon_icon(400 + 74 * k, 270, 18, round(tw + .15 * k, 2))] + [lab(622, 330, "weeks of sleep", tw + .5, BONE, 28)]
    te = T("room", "electroshocks")
    els += [poly([[995, 470], [1020, 470], [1005, 510], [1030, 510], [985, 575], [998, 524], [975, 524]], AU, at=te, fx="pop"), gl(1005, 520, 70, te, .6, "lamp", pulse=True),
            lab(1005, 448, "electroshocks", te + .1, BONE, 28)]
    trm = T("room", "recorded")
    els += [rect(1150, 560, 300, 200, "#2a2420", "#6a6058", 1.5, 3, -1), rect(1180, 400, 240, 160, "#3a3430", "#9a9288", 2, 6, trm - .3, fx="pop")]
    for cx in (1245, 1355):
        els += [circ(cx, 455, 40, "#1a1612", "#cbbca8", 2.5, trm - .2, fx="pop"), circ(cx, 455, 8, "#cbbca8", at=trm - .2)]
        els.append(ln([(cx + 52 * math.cos(math.radians(a)), 455 + 52 * math.sin(math.radians(a))) for a in range(-150, 151, 15)], trm + .3, AMBER, 3, dur=.8, curve=True))
    els += [rect(1180, 300, 46, 60, "#3a3430", "#9a9288", 1.5, 4, trm), circ(1203, 330, 14, "#1a1612", "#9a9288", 2, trm)]
    els += [ln([(1165 - 24 * j, 306 - 8 * j), (1150 - 34 * j, 330), (1165 - 24 * j, 354 + 8 * j)], round(trm + .4 + .2 * j, 2), LILAC, 3, "claimed", .4, curve=True)
            for j in range(1, 4)]
    th = T("room", "sixteen")
    for k in range(24):
        els.append(rect(1110 + 20 * k, 700, 16, 26, "rgba(232,184,122,.75)" if k < 16 else "#2a2420", "#6a6058", 1, 2, round(th + .03 * k, 2)))
    els += [lab(1350, 680, "16 hours a day", th + .4, AMBER, 28), lab(622, 200, "depatterning", T("room", "depatterning"), LILAC, 26, st="cap")]
    return {"base": "dark", "cam": CAM, "els": els}


def add_photos():
    """s54: a string of photographs over the bed; one by one, four of the six fade blank (years, not a whole life); a child's
    silhouette at the door."""
    t0 = T("photos", "remember")
    els = [ln([(300, 372), (870, 372)], t0 - .8, "#8a8278", 2, dur=.6, curve=False)]
    for k in range(6):
        x = 312 + 92 * k
        els += [rect(x, 380, 84, 72, "#efe6d2", at=t0 - .7, fx="pop"), rect(x + 6, 386, 72, 46, "#6a7a88", at=t0 - .7, fx="pop"),
                rect(x + 6, 418, 72, 14, "#5a6a48", at=t0 - .7, fx="pop"), circ(x + 42, 412, 6, "#2a2420", at=t0 - .7)]
        if k < 4:
            els.append(veil(x + 6, 386, 72, 46, round(t0 + .45 * k, 2), "#efe6d2", dur=.6))
    tc = T("photos", "children")
    els += [gl(1560, 680, 140, tc, .4), ppl(1560, 760, 110, tc, "#8a8278")]
    return els


def sc_bars():
    """s55: Cameron with a dotted 'CIA?'; two bars: CIA, over $60,000 (short) and Canada, about $500,000 (tall), true to scale."""
    tq = T("bars", "never have known")
    els = [ppl(260, 760, 300, .3, "#cbbca8"), lab(260, 420, "Ewen Cameron", .5, BONE, 26)] + tag(260, 360, "CIA?", tq, LILAC, 28, "claimed")
    els.append(ln([(560, 740), (1250, 740)], .4, BONE, 2, draw=False))
    tc = T("bars", "funded")
    hc = round(400 * 60 / 500)
    els += [rect(630, 740 - hc, 150, hc, AMBER, at=tq + .8, fx="fill"), lab(705, 740 - hc - 20, "CIA: over $60,000", tq + 1.0, AMBER, 28)]
    th = T("bars", "half a million")
    els += [rect(940, 340, 150, 400, "#7fb6e6", at=th - .3, fx="fill", dur=1.2), lab(1015, 320, "Canada: about $500,000", th + .3, "#9fd0ff", 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_news():
    """s56: a newspaper of 1977, 'Senate hearings'; a family reads it."""
    tf = T("news", "family")
    els = [rect(1330, 170, 330, 360, "#e8dcc2", PAPER_D, 1.5, 4, tf - .3, fx="rise"), rect(1350, 186, 290, 26, "#3a3029", at=tf - .2),
           lab(1350, 242, "1977", tf - .1, TYPE, 24, "start", st="mono", halo=False, scl=True),
           lab(1495, 292, "SENATE", tf, INK, 34, st="serif", halo=False, scl=True, weight=700), lab(1495, 332, "HEARINGS", tf, INK, 34, st="serif", halo=False, scl=True, weight=700)]
    els += typed(1356, 370, 130, 6, tf + .2, 22, sw=2.5) + typed(1504, 370, 130, 6, tf + .2, 22, sw=2.5, seed=3)
    els += [ppl(1400, 760, 190, tf + .5, "#8a8278"), ppl(1470, 760, 176, tf + .6, "#7a7268"), ppl(1540, 760, 110, tf + .7, "#8a8278")]
    return els


def sc_nine9():
    """s57: 1988: nine former patients and a settlement, no fault admitted; 1992: Canada, $100,000 each, for humanitarian reasons."""
    tn = T("nine9", "nine former")
    els = sheet(150, 160, 420, 210, tn - .6) + typed(180, 240, 360, 4, tn - .4, 28, seed=50) + \
        [lab(180, 204, "SETTLEMENT, 1988", tn - .4, TYPE, 24, "start", st="mono", halo=False, scl=True)]
    els += [ppl(170 + 50 * k, 560, 130, round(tn + .1 * k, 2), "#cbbca8") for k in range(9)]
    els += tag(370, 630, "no fault admitted", T("nine9", "without admitting"), DIM, 26)
    tc = T("nine9", "Canada offered")
    els += sheet(900, 150, 520, 200, tc - .3, lines=0) + [lab(930, 194, "CANADA, 1992", tc - .2, TYPE, 24, "start", st="mono", halo=False, scl=True),
                                                       lab(1160, 262, "$100,000 each", tc + .2, INK, 40, st="mono", halo=False, scl=True),
                                                       lab(1160, 316, "humanitarian, not liability", T("nine9", "humanitarian"), TYPE, 24, st="mono", halo=False, scl=True)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_paid77():
    """s58: 77 figures light up in green; behind them about 250 dim outlines: turned away."""
    t7 = T("paid77", "Seventy-seven")
    els = []
    for i in range(77):
        c, r = i % 11, i // 11
        els.append(ppl(860 + 40 * c, 462 + 51 * r, 42, round(t7 + .012 * i, 3), GREEN))
    els.append(lab(1060, 396, "77 paid", t7 + .4, GREEN, 30))
    tt = T("paid77", "turned away")
    for i in range(252):
        c, r = i % 18, i // 18
        els.append(circ(1345 + 20 * c, 436 + 25 * r, 5.5, "#8a8278", at=round(tt + .004 * i, 3), op=.5))
    els.append(lab(1515, 396, "over 250 refused", tt + .3, MUTED, 28))
    return els


def sc_court25():
    """s59: a courthouse, Quebec, 2025; a gavel; three defendants pop: the hospital, McGill, Canada."""
    st_ = "#8a8478"
    els = [rect(240, 700, 680, 22, st_, at=-1), rect(270, 680, 620, 22, st_, at=-1), rect(300, 660, 560, 22, st_, at=-1), rect(300, 380, 560, 30, st_, at=-1),
           poly([[290, 380], [580, 290], [870, 380]], st_, "#b8b2a6", 1.5, -1)] + [rect(330 + 96 * k, 410, 36, 250, "#a8a296", at=-1) for k in range(6)]
    els += [gl(580, 520, 420, -1, .2), lab(580, 250, "Quebec, 2025", .4, AMBER, 28, st="cap")]
    tc = T("court25", "class")
    els += gavel(1390, 300, tc - .2, s=.9) + [lab(1390, 210, "class action", tc, BONE, 30)]
    th, tm, tg = T("court25", "hospital"), T("court25", "McGill"), T("court25", "government")
    els += hosp(1170, 600, 150, th) + [lab(1170, 640, "the hospital", th + .1, BONE, 26)]
    els += uni(1400, 600, 150, tm) + [lab(1400, 640, "McGill", tm + .1, BONE, 26)]
    els += [rect(1560, 495, 120, 105, "#3a3129", "#cbbca8", 2, 2, tg, fx="pop"), ln([(1620, 495), (1620, 440)], tg, "#cbbca8", 2, draw=False),
            rect(1620, 440, 48, 26, "#f6f2ea", at=tg, fx="pop"), rect(1620, 440, 12, 26, RED, at=tg, fx="pop"), rect(1656, 440, 12, 26, RED, at=tg, fx="pop"),
            lab(1620, 640, "Canada", tg + .1, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== 6 The weighing
def sc_four():
    """s60: four records pop and converge on one point: the 1963 inspector general, the 1975 commission, the 1976 Senate report, the 1977 hearing."""
    cx, cy = 889, 470
    els0 = [folder(cx - 70, cy - 40, 140, 100, .4, fx="pop"), lab(cx, cy + 100, "records of the time", .8, AMBER, 28)]
    docs = [(430, 290, "1963", "inspector general", "inspector general"), (1350, 290, "1975", "presidential commission", "presidential commission"),
            (430, 630, "1976", "Senate report", "two Senate"), (1350, 630, "1977", "Senate hearing", "two Senate")]
    els = els0
    for k, (x, y, yr, t, ph) in enumerate(docs):
        at = T("four", ph) + (.5 if k == 3 else 0)
        els += [rect(x - 110, y - 80, 220, 150, PAPER, PAPER_D, 1.5, 4, at, fx="pop"), lab(x, y - 26, yr, at + .1, INK, 40, st="serif", halo=False, scl=True, fx="pop")]
        els += typed(x - 80, y + 10, 160, 2, at + .2, 22) + [lab(x, y + 108, t, at + .2, BONE, 26)]
        els.append(ln([(x + (90 if x < cx else -90), y), (cx, cy)], at + .4, GREEN, 3, dur=.6))
    tl = T("four", "two Senate") + 1.2
    els += [gl(cx, cy, 160, tl, .5)]
    return {"base": "dark", "cam": CAM, "els": els}


ROWS = [235, 365, 495, 625]


def ledger_row(k, t, at, icon):
    y = ROWS[k]
    return [rect(130, y - 55, 1520, 110, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(340, y + 11, t, at + .1, BONE, 32, "start")] + icon(245, y, at)


def icon_glass(x, y, at):
    return glass(x, y + 34, at, h=56, fill_at=at) + drop(x, y - 10, at + .1, s=.6)


def icon_head(x, y, at):
    return [head(x, y - 6, 64, at, "#2a2420", "rgba(255,236,206,.4)", 1.5)] + [lab(x + 2, y - 4, "?", at, LILAC, 26, st="serif")]


def icon_box(x, y, at):
    return ghost_box(x - 34, y - 18, 68, 48, at, c="#cbbca8")


def icon_scale(x, y, at):
    return [ln([(x - 46, y - 18), (x + 46, y - 18)], at, BONE, 4, draw=False), ln([(x, y - 18), (x, y + 36)], at, BONE, 4, draw=False),
            poly([(x - 60, y + 8), (x - 32, y + 8), (x - 46, y - 18)], "none", MUTED, 2, at), poly([(x + 32, y + 8), (x + 60, y + 8), (x + 46, y - 18)], "none", MUTED, 2, at)]


def sc_ledger():
    """s61: the ledger: row 1, 'unwitting people drugged', its chip Established; under the board, consent required since 1976."""
    els = [rect(110, 150, 1560, 570, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += [rect(130, y - 55, 1520, 110, "none", "rgba(242,201,142,.16)", 1.5, 12, .5, style="inferred") for y in ROWS[1:]]   # three rows still to weigh
    t1 = T("ledger", "Did the CIA")
    els += ledger_row(0, "unwitting people drugged", t1, icon_glass)
    els += chip(1250, ROWS[0], "Established", GRADE["established"], T("ledger", "Established"), 30, a="start")
    els.append(lab(889, 770, "consent required since 1976", T("ledger", "Since"), MUTED, 26))
    return {"base": "dark", "cam": CAM, "els": els}


def add_ledger2():
    """s63: rows 2 to 4 as named: mind control that works (Awaiting evidence), the files tell it all (Ruled out), how Frank Olson died
    (Open question)."""
    els = ledger_row(1, "mind control that works", .3, icon_head) + chip(1250, ROWS[1], "Awaiting evidence", GRADE["awaiting"], T("ledger2", "Awaiting"), 30, a="start")
    els += ledger_row(2, "the files tell it all", T("ledger2", "Do the surviving"), icon_box) + chip(1250, ROWS[2], "Ruled out", GRADE["ruled"], T("ledger2", "Ruled"), 30, a="start")
    els += ledger_row(3, "how Frank Olson died", T("ledger2", "how Frank Olson"), icon_scale) + chip(1250, ROWS[3], "Open question", GRADE["open"], T("ledger2", "Open question"), 30, a="start")
    return els


def sc_pills():
    """s62: a head with a '?'; as of 1960, three pills pop as named and are crossed out: truth serum, knockout pill, recruitment pill."""
    els = [gl(380, 360, 300, .2, .2), head(380, 430, 460, .2, "#2a2420")] + qmark(390, 380, .6, 110)
    els.append(lab(1120, 250, "as of 1960", T("pills", "nineteen sixty"), AMBER, 28, st="cap"))
    for k, (ph, t) in enumerate((("truth", "truth serum"), ("knockout", "knockout pill"), ("recruit", "recruitment pill"))):
        x, at = 820 + 300 * k, T("pills", ph)
        els += pill(x, 450, 150, at) + [lab(x, 550, t, at + .1, BONE, 28)] + cross(x, 450, at + .3, RED, 2.4, 7)
    return {"base": "dark", "cam": CAM, "els": els}


def sc_hidden():
    """s64: a time line: 1953 to 1975 under a dark band, 'hidden'; the report of 1975 and the boxes of 1977."""
    els = [axis(200, 1580, 600, [(xyr(y), str(y)) for y in (1950, 1960, 1970, 1980)], .2), dot(xyr(1953), 600, 9, BONE, .3), lab(xyr(1953), 400, "1953", .4, BONE, 26)]
    th = T("hidden", "hidden")
    els += [rect(xyr(1953), 430, xyr(1975) - xyr(1953), 140, "rgba(8,6,5,.75)", "#6a5a48", 2, 6, th - .4, fx="fill"), lab((xyr(1953) + xyr(1975)) / 2, 512, "hidden", th, BONE, 36)]
    els += sheet(xyr(1975) - 40, 450, 80, 100, th + .5, lines=3, seed=60, lh=20) + [lab(xyr(1975), 420, "1975", th + .6, BONE, 26)]
    els += static(abox(xyr(1977) + 10, 490, 70, 60, -1, d=12))
    els[-1]["in"] = th + .9
    els += [lab(xyr(1977) + 45, 420, "1977", th + 1.0, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_gaps():
    """s65: soft lilac question marks glow in the dashed gaps where the destroyed files stood."""
    t0, t1 = max(2.7, T("gaps", "more happened")), T("gaps", "gaps")
    spots = [(646, 352), (994, 352), (1458, 352), (762, 672), (1226, 672), (1574, 672), (625, 512)]
    els = []
    for k, (x, y) in enumerate(spots):
        els += [gl(x, y - 14, 70, round(t0 + .2 * k, 2), .45), lab(x, y + 14, "?", round(t1 + .25 * k, 2), LILAC, 52, st="serif", fx="pop")]
    return els


def sc_test():
    """s66: three tests not yet done (dashed): a surviving copy in another building, the Montreal case, a record of a method that worked."""
    els = [lab(889, 206, "?", 2.4, LILAC, 70, st="serif", fx="pop")]
    tc = T("test", "copy")
    els += [rect(190, 330, 280, 300, "none", BONE, 2.5, 4, tc - .2, style="inferred"), poly([[170, 332], [330, 250], [490, 332]], "none", BONE, 2.5, tc - .2, style="inferred"),
            ln([(210, 520), (450, 520)], tc, BONE, 2, "inferred", draw=False)] + abox(290, 470, 70, 50, tc + .2, d=10, fx="pop") + [gl(325, 490, 90, tc + .3, .6)]
    els.append(lab(330, 700, "a surviving copy", tc + .3, BONE, 28))
    tm = T("test", "Montreal case")
    els += [rect(760, 360, 260, 30, "none", BONE, 2.5, 2, tm - .2, style="inferred"), poly([[750, 360], [890, 290], [1030, 360]], "none", BONE, 2.5, tm - .2, style="inferred")]
    els += [ln([(790 + 60 * k, 390), (790 + 60 * k, 560)], tm - .1, BONE, 2.5, "inferred", draw=False) for k in range(4)]
    els += [rect(750, 560, 280, 20, "none", BONE, 2.5, 2, tm - .1, style="inferred")] + abox(850, 600, 80, 56, tm + .3, d=10, fx="pop") + [lab(890, 700, "the Montreal case", tm + .3, BONE, 28)]
    tw = T("test", "method")
    els += [rect(1340, 320, 220, 290, "rgba(239,230,210,.05)", PAPER, 2.5, 4, tw - .2, style="inferred")] + typed(1366, 360, 168, 5, tw, 26, c="#8a7a66", sw=2.5)
    els += [{"k": "line", "p": R([(1400, 540), (1440, 576), (1500, 500)]), "c": GREEN, "w": 6, "style": "inferred", "in": round(tw + .4, 2)},
            lab(1450, 700, "a method that worked?", tw + .3, BONE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def add_close():
    """s67: the warehouse at night again: dim figures standing in the dark between the shelves; the light lowers a little."""
    t0 = max(2.4, T("close", "How many"))
    els = []
    for k, (x, y, h) in enumerate(((260, 690, 150), (345, 700, 158), (540, 776, 200), (1660, 784, 210))):
        els.append(ppl(x, y, h, round(t0 + .4 + .4 * k, 2), "#8a8278", fx="fade", op=.4))
    td = T("close", "anymore")
    els += [veil(-20, -20, 1820, 1040, td - .6, "#0d0b09", op=.28, dur=2.5), gl(1092, 512, 380, td + .4, .22)]
    return els


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "hero", [(0, "They belong", "gone"), (1, "Inside:", "receipts"), (2, "The programme was called", "folder")], {}),
    (0, 1, "title", "folder", [], {"intro": True}),
    (1, 0, "world", "paper", [(1, "Then, in the Korean", "korea")], {"chapter": "Brain warfare"}),
    (1, 1, "collision", "teams", [(1, "On the tenth", "dulles"), (1, "Three days later", "approved"), (2, "Its name", "lab"), (2, "A tiny dose", "tongues")], {}),
    (1, 2, "cost", "grid", [(0, "Forty-four universities", "groups"), (1, "Reading them", "claims")], {}),
    (1, 3, "reversal", "front", [(1, "One hospital", "wing"), (1, "In return", "sixth")], {}),
    (2, 0, "world", "labstreet", [], {"chapter": "The safe houses"}),
    (2, 1, "collision", "map", [(0, "A federal narcotics", "flat"), (1, "It came in tiny", "ampoule"), (1, "They had no idea", "ill")], {}),
    (2, 2, "cost", "forty", [], {}),
    (2, 3, "reversal", "ig", [(0, "It added that", "inside"), (1, "The testing on unwitting", "closed")], {}),
    (3, 0, "world", "lake", [(0, "After dinner", "bottle"), (1, "Among those", "olson")], {"chapter": "Frank Olson"}),
    (3, 1, "cost", "route", [(0, "Nine days after", "nine")], {}),
    (3, 2, "reversal", "told", [(0, "They learned of it", "years22"), (1, "The President", "whitehouse")], {}),
    (3, 3, "collision", "balance", [(1, "In {1994", "exhume"), (1, "New York prosecutors", "unknown"), (2, "In {2012", "court")], {}),
    (3, 4, "tag", "level", [], {}),
    (4, 0, "world", "cabinet", [(1, "Gottlieb later gave", "reasons")], {"chapter": "Seven boxes"}),
    (4, 1, "reversal", "search75", [(0, "A writer, John", "foia"), (0, "In {1977", "found"), (1, "Approvals for advances", "stack"), (1, "It was like finding", "diary")], {}),
    (4, 2, "cost", "hearing", [(1, "Even Turner", "little")], {}),
    (4, 3, "tag", "survived", [], {}),
    (5, 0, "world", "north", [(0, "From {1957", "flow")], {"chapter": "Montreal"}),
    (5, 1, "collision", "room", [(1, "Many could no longer", "photos")], {}),
    (5, 2, "reversal", "bars", [(0, "One patient's family", "news")], {}),
    (5, 3, "cost", "nine9", [(1, "Seventy-seven former", "paid77")], {}),
    (5, 4, "tag", "court25", [], {}),
    (6, 0, "weigh", "four", [(1, "Did the CIA run", "ledger")], {"chapter": "The weighing"}),
    (6, 1, "weigh", "pills", [(0, "Mind control that works", "ledger2"), (2, "The agency kept", "hidden"), (2, "So if you", "gaps")], {}),
    (6, 2, "test", "test", [], {}),
    (6, 3, "close", "close", [], {}),
]

# alias shots: (the panel they return to, the camera on that panel, the function drawing their additions on arrival)
ALIASES = {
    "gone": ("hero", [1.12, 960, 470], "add_gone"),
    "approved": ("dulles", [1, 889, 500], "add_approved"),
    "groups": ("grid", [1.4, 1143, 490], "add_groups"),
    "claims": ("grid", [1, 889, 500], "add_claims"),
    "sixth": ("wing", [1.15, 900, 480], "add_sixth"),
    "ampoule": ("flat", [1.2, 760, 420], "add_ampoule"),
    "ill": ("flat", [1, 889, 500], "add_ill"),
    "inside": ("ig", [1, 889, 500], "add_inside"),
    "closed": ("map", [1, 889, 500], "add_closed"),
    "olson": ("bottle", [1.15, 889, 470], "add_olson"),
    "level": ("balance", [1, 889, 500], "add_level"),
    "foia": ("search75", [1, 889, 500], "add_foia"),
    "found": ("hero", [1.2, 980, 480], "add_found"),
    "little": ("hearing", [1, 889, 500], "add_little"),
    "survived": ("stack", [1, 889, 500], "add_survived"),
    "photos": ("room", [1, 889, 500], "add_photos"),
    "news": ("bars", [1, 889, 500], "add_news"),
    "paid77": ("nine9", [1, 889, 500], "add_paid77"),
    "ledger2": ("ledger", [1, 889, 500], "add_ledger2"),
    "gaps": ("hero", [1.15, 940, 470], "add_gaps"),
    "close": ("hero", [1, 889, 500], "add_close"),
}


def _segments(script):
    """The narration each shot has on screen, from the beats with their markers (a chapter beat's first sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[@%s]" % sid)
        parts = re.split(r"\[@(\w+)\]", "\n".join(lines))
        head = parts[0]
        if kw.get("chapter"):
            ms = [m.start() for m in SENT.finditer(head) if m.start() > 0]
            head = head[ms[0]:] if ms else ""
        if role != "title":
            say[frm] = say[frm] + "\n" + head if frm in say else head
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
    ep = {"id": "lf-mkultra", "code": "LF.14", "series": script["series"], "title": script["title"], "case": "mkultra",
          "verdict": "solid", "claim": "The CIA ran illegal drug experiments on unwitting people?", "mood": "cold",
          "hook_text": "Did the CIA really try to control *minds*?", "beats": beats, "shots": shots,
          "sources": "US Senate 1977, Project MKULTRA joint hearing (3 August 1977) · Church Committee, Final Report Book I, 1976 · CIA Inspector General, "
                     "Report of Inspection of MKULTRA, 1963 · Rockefeller Commission, Report to the President, 1975 · Marks 1979, The Search for the "
                     "Manchurian Candidate · National Security Archive 2024 (MKULTRA documents) · Cameron 1956 (doi:10.1176/ajp.112.7.502) · "
                     "Torbay 2023 (doi:10.1177/0957154X231163763)",
          "post": "In 1973 the CIA destroyed the MKUltra files. In 1977 seven boxes of its receipts turned up anyway. What they show: LSD given to people "
                  "who never knew, a hospital wing with a secret sixth, Frank Olson's death and the questions it left, the patients in Montreal, and the "
                  "gaps nobody can see into. Weighed.",
          "hashtags": ["#MKUltra", "#CIA", "#ColdWar", "#History", "#DeclassifiedFiles", "#WeighItYourself"],
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
