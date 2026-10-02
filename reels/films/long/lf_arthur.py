"""LF.16 · Myths That Came True · King Arthur: The Search for the Man (16:9 long film, one wall).

The script is films/long/lf-arthur/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s61; s4, the title, is the intro card over the
panel of s3), drawn while it is said: the lead cross of Glastonbury and the grave the monks dug in 1191, Roman Britain going dark,
the newcomers from across the North Sea and their DNA, Gildas at his desk and the siege of Mount Badon, the Gododdin's ravens,
the History of the Britons with its twelve battles, 960 men and its wonders, the Welsh Annals, the chart of what we learn as the
centuries pass, Geoffrey of Monmouth's king, 215 manuscripts, Camelot, the doubts at Glastonbury, Cadbury Castle and its hall,
Tintagel and its trade, the Artognou slate, the candidates, the ledger and the tests. Drawings are schematic and true to the
numbers said: solid = recorded or excavated, dashed = inferred, dotted and lilac = the legend or a claim.

Facts: the Short 'arthur' (f11.py, rewrite/arthur.json) and the script's facts_added (Gildas; the Historia Brittonum; the Annales
Cambriae; Y Gododdin; Geoffrey of Monmouth; Charles-Edwards 1991; Dumville 1977; Padel 1994; Higham 2002; Halsall 2013; Alcock
1971, 1995; Rahtz 1993; Barrowman, Batey & Morris 2007; English Heritage; Gretzinger et al. 2022; Ashe 1981).

Engine workaround (as in lf_troy.py and lf_mkultra.py): the wall only adds elements to a panel on its first visit, at a beat start
or a line start; shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag,
invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that
step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-arthur/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-arthur/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-arthur RC_FILMS_EPS=/tmp/claude-0/sbx_lf-arthur/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-arthur/boards python3 films.py long.lf_arthur
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-arthur", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
LEAD, LEAD_D, LEAD_L, INCISE = "#868b91", "#4d5156", "#d5d9de", "#2c2f33"      # the lead cross
EARTH, EARTH_D, EARTH_L = "#3a2c20", "#241a12", "#5a4632"
STONE, STONE_D = "#cdbf9f", "#8c7a5e"
ROBE, ROBE_E = "#2c2622", "rgba(255,236,206,.35)"                               # monks' robes
SKIN = "#e8d6b8"
PURPLE = "#a77fd9"
FIRE = "#ff7a4a"
SEAC = "#3f86a8"
PARCH, PARCH_E, INK = "#e9dcc0", "#a8916c", "#4a3a28"
WOOD, WOOD_D = "#6b4a30", "#3a281a"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "awaiting": "#c9c1ee", "open": "#f0b06a", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # DNA: letter by letter
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
            g = re.search(r"\[gap:([\d.]+)\]", seg)
            if g:
                t += float(g.group(1))
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


def grp(els, at, fx="pop", tr=None, **kw):
    """A group that builds in as one piece (its children have no build-ins of their own); tr = an SVG transform."""
    if tr:
        els = [{"k": "group", "tr": tr, "els": els}]
    e = {"k": "group", "els": els, "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    e.update(kw)
    return e


def chip(x, y, t, c, at, size=28, a="middle"):
    """A pill with a coloured rim and its words (grades, dates)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


def tagc(x, y, t, at, c=AMBER, size=26, style="known", a="middle"):
    """A small rounded tag with a few words (dashed for an inference, dotted for a claim)."""
    w = len(t) * size * .55 + 30
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - size * .95, w, size * 1.55, "rgba(18,13,10,.85)", c, 2, size * .7, at, fx="pop", style=style),
            lab(x0 + w / 2, y + size * .2, t, at + .1, c, size, halo=False)]


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


def veil(x, y, w, h, at, fill, op=1.0, dur=.5, r=0):
    """A sheet of the background's own colour laid over something: what was there fades away."""
    e = rect(x, y, w, h, fill, r=r, at=at, op=op)
    e["dur"] = dur
    return e


def softveil(x, y, r, at, fill="#0d0b09", op=.8, n=6, dur=.9):
    """A soft-edged dark disc (n stacked discs, the inner ones darker): a light going out."""
    a = 1 - (1 - op) ** (1.0 / n)
    out = []
    for k in range(n):
        e = circ(x, y, r * (1 - k / (n + 1.5)), fill, at=at, op=round(a, 3))
        e["dur"] = dur
        out.append(e)
    return out


def crown(x, y, s, at, c=GOLD, style="known", fill=None, w=0, fx="pop", op=None):
    """A crown standing on y, s = half its width."""
    return poly([[x - s, y], [x - s, y - s * 1.1], [x - s * .5, y - s * .5], [x, y - s * 1.2], [x + s * .5, y - s * .5], [x + s, y - s * 1.1], [x + s, y]],
                fill if fill is not None else c, c if fill is not None else "none", w, at, fx=fx, style=style, op=op)


def flame(x, y, s, at, c=FIRE, glow_=True):
    """A small flame glyph standing on y."""
    out = [poly([[x, y], [x - .45 * s, y - .35 * s], [x - .25 * s, y - .8 * s], [x - .05 * s, y - .55 * s], [x + .05 * s, y - 1.1 * s], [x + .35 * s, y - .6 * s],
                 [x + .45 * s, y - .3 * s]], c, "#ffd08a", 1.5, at, fx="pop", curve=True)]
    if glow_:
        out.append(gl(x, y - .5 * s, 1.6 * s, at, .5, "fire"))
    return out


def monk(x, y, h, at, c=ROBE, face=1, fx="rise", op=None, edge=ROBE_E, style="known"):
    """A hooded figure in a long robe, feet on y, facing `face` (the hood's face opening on that side)."""
    f = face
    X = lambda a: x + f * a * h
    robe = [[X(-.18), y], [X(-.14), y - .45 * h], [X(-.12), y - .72 * h], [X(.12), y - .72 * h], [X(.15), y - .45 * h], [X(.19), y]]
    hood = [[X(-.1), y - .7 * h], [X(-.11), y - .86 * h], [X(-.03), y - .99 * h], [X(.08), y - .95 * h], [X(.11), y - .84 * h], [X(.1), y - .7 * h]]
    return [poly(robe, c, edge, 1.2, at, fx=fx, op=op, style=style), poly(hood, c, edge, 1.2, at, fx=fx, op=op, curve=True, style=style),
            poly([[X(.02), y - .9 * h], [X(.08), y - .88 * h], [X(.07), y - .8 * h], [X(.01), y - .8 * h]], "#14110e", at=at, fx=fx, op=op)]


def seated_monk(x, y, h, at, c=ROBE, face=1, fx="rise", op=None):
    """A hooded writer seated on a stool, facing `face`, feet on y (h = standing height); his hand reaches forward."""
    f = face
    X = lambda a: x + f * a * h
    return [rect(min(X(-.14), X(.06)), y - .27 * h, .2 * h, .27 * h, "#3a2c20", "#8a6a48", 1.5, 3, at, fx=fx, op=op),
            poly([[X(-.1), y - .27 * h], [X(-.12), y - .66 * h], [X(.1), y - .66 * h], [X(.12), y - .36 * h], [X(.3), y - .34 * h], [X(.32), y], [X(.2), y],
                  [X(.18), y - .24 * h], [X(-.08), y - .22 * h]], c, ROBE_E, 1.2, at, fx=fx, op=op),
            poly([[X(-.08), y - .64 * h], [X(-.09), y - .78 * h], [X(-.01), y - .9 * h], [X(.09), y - .86 * h], [X(.12), y - .75 * h], [X(.1), y - .63 * h]], c, ROBE_E, 1.2,
                 at, fx=fx, op=op, curve=True),
            poly([[X(.04), y - .82 * h], [X(.1), y - .8 * h], [X(.09), y - .72 * h], [X(.03), y - .72 * h]], "#14110e", at=at, fx=fx, op=op),
            ln([[X(.05), y - .58 * h], [X(.2), y - .5 * h], [X(.34), y - .47 * h]], at, c, max(3, .055 * h), draw=False, op=op)]


def writing_desk(x, y, w, at, h=None):
    """A slanted writing desk seen from the side: legs, a sloping board whose top edge is at y (x = the board's centre)."""
    h = h or w * .9
    return [ln([(x - w * .4, y + 30), (x - w * .38, y + h)], at, "#3a2c20", 10, draw=False), ln([(x + w * .4, y - 10), (x + w * .38, y + h)], at, "#3a2c20", 10, draw=False),
            poly([(x - w / 2, y + 36), (x + w / 2, y - 16), (x + w / 2, y), (x - w / 2, y + 52)], "#5a4632", "#8a6a48", 1.5, at),
            ln([(x - w * .42, y + h * .7), (x + w * .42, y + h * .7)], at, "#3a2c20", 6, draw=False)]


def candle(x, y, at, h=46, r=150):
    return [rect(x - 7, y - h, 14, h, "#efe3c8", "#a8916c", 1, 2, at, fx="pop"), poly([[x, y - h - 2], [x - 6, y - h - 12], [x, y - h - 26], [x + 6, y - h - 12]], "#ffd08a", at=at, fx="pop", curve=True),
            gl(x, y - h - 14, r, at, .75, "lamp")]


def book(x, y, w, h, at, c="#7a4a2e", edge="#d8b48a", fx="pop", op=None, style="known", fill=None, pages=True):
    """A closed book standing on its cover (seen from the front, a little from the side): x, y = top left of the front cover."""
    d = w * .14
    return [poly([[x + w, y], [x + w + d, y - d * .6], [x + w + d, y + h - d * .6], [x + w, y + h]], PARCH if pages else c, edge, 1, at, fx=fx, op=op, style=style),
            poly([[x, y], [x + d, y - d * .6], [x + w + d, y - d * .6], [x + w, y]], PARCH if pages else c, edge, 1, at, fx=fx, op=op, style=style),
            rect(x, y, w, h, fill if fill is not None else c, edge, 1.5, 3, at, fx=fx, op=op, style=style)]


def open_book(cx, y, w, h, at, c=PARCH, edge=PARCH_E, fx="pop", rows=6, op=None, ink="rgba(74,58,40,.55)"):
    """An open book seen from above, slightly tilted: two pages meeting at cx, top at y."""
    out = [poly([[cx, y + 8], [cx - w / 2, y], [cx - w / 2 - 6, y + h], [cx, y + h + 10]], c, edge, 1.5, at, fx=fx, op=op),
           poly([[cx, y + 8], [cx + w / 2, y], [cx + w / 2 + 6, y + h], [cx, y + h + 10]], c, edge, 1.5, at, fx=fx, op=op),
           ln([[cx, y + 8], [cx, y + h + 10]], at, "rgba(90,70,50,.6)", 2, draw=False, op=op)]
    if rows:
        out.append({"k": "glyphs", "x": round(cx - w / 2 + w * .06, 1), "y": round(y + h * .1, 1), "w": round(w * .38, 1), "h": round(h * .78, 1), "rows": rows, "cols": 5,
                    "kind": "latin", "c": ink, "in": round(at + .1, 2)})
        out.append({"k": "glyphs", "x": round(cx + w * .06, 1), "y": round(y + h * .1, 1), "w": round(w * .38, 1), "h": round(h * .78, 1), "rows": rows, "cols": 5,
                    "kind": "latin", "c": ink, "in": round(at + .1, 2), "seed": 7})
    return out


def ship(x, y, w, at, c="#2a2018", face=1, oars=8, fx="pop", op=None, mast=True, style="known", edge="rgba(255,236,206,.35)"):
    """A long open ship in side view (bow towards `face`), y = the waterline, w = length."""
    f = face
    X = lambda a: x + f * a * w
    hull = [[X(-.5), y - .16 * w], [X(-.44), y - .05 * w], [X(-.3), y + .02 * w], [X(.3), y + .02 * w], [X(.44), y - .05 * w], [X(.5), y - .17 * w],
            [X(.46), y - .12 * w], [X(.36), y - .06 * w], [X(-.36), y - .06 * w], [X(-.46), y - .11 * w]]
    out = [poly(hull, c, edge, 1.2, at, fx=fx, op=op, curve=True, style=style)]
    out += [ln([[X(-.3 + .6 * k / max(1, oars - 1)), y - .02 * w], [X(-.34 + .6 * k / max(1, oars - 1)), y + .07 * w]], at, c, max(1.5, .008 * w), draw=False, op=op)
            for k in range(oars)]
    if mast:
        out.append(ln([[X(0), y - .06 * w], [X(0), y - .4 * w]], at, c, max(2, .012 * w), draw=False, op=op))
    return out


def figure(x, y, h, at, c, fx="rise", op=None):
    e = {"k": "person", "x": round(x, 1), "y": round(y, 1), "h": round(h, 1), "t": False, "color": c, "in": round(at, 2), "fx": fx}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def warrior(x, y, h, at, c="#2a2018", face=1, fx="rise", op=None, spear=True, shield=True, edge="rgba(255,236,206,.3)"):
    """A standing figure with a spear and a round shield (feet on y)."""
    f = face
    out = [figure(x, y, h, at, c, fx, op)]
    if spear:
        out.append(ln([[x + f * .2 * h, y + .02 * h], [x + f * .27 * h, y - 1.18 * h]], at, c, max(2, .025 * h), draw=False, op=op))
        out.append(poly([[x + f * .27 * h, y - 1.18 * h], [x + f * .25 * h, y - 1.08 * h], [x + f * .29 * h, y - 1.08 * h]], c, at=at, fx=fx, op=op))
    if shield:
        out.append(circ(x - f * .05 * h, y - .5 * h, .17 * h, c, edge, 1.5, at, fx=fx, op=op))
        out.append(circ(x - f * .05 * h, y - .5 * h, .04 * h, "#8a7a66", at=at, fx=fx, op=op))
    return out


def knight(x, y, h, at, c=LILAC, style="claimed", fill="rgba(201,193,238,.12)", fx="fade", w=2.5):
    """A standing knight in outline: body, helm, a long kite shield and a sword (the romance, drawn as a claim)."""
    body = [[x - .2 * h, y], [x - .14 * h, y - .5 * h], [x - .13 * h, y - .74 * h], [x - .05 * h, y - .8 * h], [x + .05 * h, y - .8 * h], [x + .13 * h, y - .74 * h],
            [x + .14 * h, y - .5 * h], [x + .2 * h, y]]
    return [poly(body, fill, c, w, at, fx=fx, style=style),
            poly([[x - .07 * h, y - .8 * h], [x - .08 * h, y - .93 * h], [x, y - 1.0 * h], [x + .08 * h, y - .93 * h], [x + .07 * h, y - .8 * h]], fill, c, w, at, fx=fx, style=style),
            poly([[x - .34 * h, y - .66 * h], [x - .1 * h, y - .66 * h], [x - .12 * h, y - .3 * h], [x - .22 * h, y - .12 * h], [x - .32 * h, y - .3 * h]], "rgba(201,193,238,.2)", c, w,
                 at, fx=fx, style=style),
            ln([[x + .22 * h, y - .1 * h], [x + .3 * h, y - .78 * h]], at, c, w + 1, style, draw=False),
            ln([[x + .17 * h, y - .22 * h], [x + .29 * h, y - .2 * h]], at, c, w + 1, style, draw=False)]


def king(x, y, h, at, c="#2a2018", fx="rise", op=None, crown_c=GOLD, style="known", outline=None, cloak=True, w=2.5, fill=None):
    """A standing figure in a long cloak with a crown (feet on y). outline: draw it as an outline only (the legend)."""
    if outline:
        fl = fill or "rgba(201,193,238,.10)"
        body = [[x - .2 * h, y], [x - .15 * h, y - .5 * h], [x - .13 * h, y - .74 * h], [x - .05 * h, y - .8 * h], [x + .05 * h, y - .8 * h], [x + .13 * h, y - .74 * h],
                [x + .15 * h, y - .5 * h], [x + .2 * h, y]]
        return [poly(body, fl, outline, w, at, fx=fx, op=op, style=style),
                circ(x, y - .88 * h, .075 * h, fl, outline, w, at, fx=fx, op=op, style=style),
                crown(x, y - .95 * h, .085 * h, at, outline, style=style, fill=fl, w=w, fx=fx, op=op),
                ln([[x + .24 * h, y - .05 * h], [x + .24 * h, y - .62 * h]], at, outline, w + .5, style, draw=False, op=op),
                ln([[x + .17 * h, y - .52 * h], [x + .31 * h, y - .52 * h]], at, outline, w + .5, style, draw=False, op=op)]
    out = []
    if cloak:
        out.append(poly([[x - .16 * h, y - .78 * h], [x + .16 * h, y - .78 * h], [x + .21 * h, y - .02 * h], [x - .21 * h, y - .02 * h]], c, "rgba(255,236,206,.25)", 1, at, fx=fx, op=op))
    out.append(figure(x, y, h, at, c, fx, op))
    out.append(crown(x, y - .97 * h, .07 * h, at, crown_c, fx=fx, op=op))
    return out


def horse(x, y, s, at, c="#d9c7a6", face=1, op=None, style="known", fill=None, w=0, fx="rise"):
    """A horse in side view, hooves on y, s = its height at the withers; face = 1 looks right."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    body = [P(-.95, -.98), P(-.6, -1.02), P(-.1, -.97), P(.32, -1.04), P(.55, -1.26), P(.72, -1.5), P(.78, -1.62), P(.84, -1.5), P(1.08, -1.2), P(1.04, -1.1),
            P(.82, -1.14), P(.66, -1.0), P(.6, -.76), P(.34, -.6), P(-.48, -.58), P(-.82, -.68), P(-.96, -.86)]
    fl = fill if fill is not None else c
    out = [poly(body, fl, c if fill is not None else "none", w, at, fx=fx, op=op, style=style, curve=True)]
    for lx, kx in ((.5, .56), (.36, .3), (-.42, -.36), (-.6, -.64)):
        out.append(ln([P(lx, -.64), P(kx, -.3), P(lx + (.02 if lx > 0 else -.02), 0)], at, c, max(3, .085 * s) if style == "known" else 3, style, draw=False, op=op))
    out.append(ln([P(-.94, -.9), P(-1.08, -.6), P(-1.04, -.38)], at, c, max(3, .07 * s) if style == "known" else 3, style, draw=False, op=op, curve=True))
    return out


def dog(x, y, s, at, c=LILAC, op=None, style="known", fill=None, w=0, fx="rise", face=1):
    """A hound in side view, paws on y, s = height at the shoulder."""
    f = face
    P = lambda a, b: (x + f * a * s, y + b * s)
    body = [P(-.8, -.88), P(-.2, -.92), P(.42, -.95), P(.6, -1.2), P(.72, -1.3), P(.95, -1.18), P(1.02, -1.08), P(.78, -1.04), P(.66, -.86), P(.5, -.6),
            P(-.2, -.55), P(-.7, -.6)]
    fl = fill if fill is not None else c
    out = [poly(body, fl, c if fill is not None else "none", w, at, fx=fx, op=op, style=style, curve=True)]
    for lx, kx in ((.44, .5), (.3, .26), (-.55, -.5), (-.68, -.74)):
        out.append(ln([P(lx, -.62), P(kx, -.3), P(lx, 0)], at, c, max(3, .08 * s) if style == "known" else 3, style, draw=False, op=op))
    out.append(ln([P(-.78, -.85), P(-1.0, -1.05), P(-1.12, -1.2)], at, c, max(2.5, .06 * s) if style == "known" else 3, style, draw=False, op=op, curve=True))
    return out


def raven(x, y, s, at, c="#0e0b09", fx="pop", flip=1, op=None):
    """A bird in flight, wings up (s = span)."""
    f = flip
    return poly([[x - .5 * s * f, y - .18 * s], [x - .2 * s * f, y - .02 * s], [x, y + .04 * s], [x + .08 * s * f, y], [x + .2 * s * f, y - .02 * s],
                 [x + .5 * s * f, y - .2 * s], [x + .22 * s * f, y + .06 * s], [x + .06 * s * f, y + .1 * s], [x - .1 * s * f, y + .08 * s], [x - .22 * s * f, y + .06 * s]],
                c, at=at, fx=fx, curve=True, op=op)


def tree(x, y, h, at, c="#1f241a", op=None):
    return [poly(E(x, y - h * .62, h * .3, h * .4, 18), c, at=at, op=op), ln([[x, y], [x, y - h * .3]], at, "#2a2016", 4, draw=False, op=op)]


def church(x0, base, w, h, at, c="#1c1714", op=None, edge="rgba(255,226,190,.35)", lit=False, fx=None):
    """A Romanesque church in side view: nave with round-headed windows, a west tower; x0 = its west end."""
    nave = [[x0 + .2 * w, base], [x0 + .2 * w, base - .55 * h], [x0 + .6 * w, base - .75 * h], [x0 + w, base - .55 * h], [x0 + w, base]]
    tower = [[x0, base], [x0, base - h], [x0 + .1 * w, base - h * 1.12], [x0 + .2 * w, base - h], [x0 + .2 * w, base]]
    out = [poly(tower, c, edge, 1.2, at, op=op, fx=fx), poly(nave, c, edge, 1.2, at, op=op, fx=fx)]
    for k in range(5):
        wx = x0 + .27 * w + k * .14 * w
        out.append(poly([[wx - 9, base - .2 * h], [wx - 9, base - .38 * h], [wx, base - .44 * h], [wx + 9, base - .38 * h], [wx + 9, base - .2 * h]],
                        "#f2c98e" if lit else "#0d0b09", at=at, op=op, fx=fx))
    return out


def pillar(x, base, h, at, op=None, fx=None, c=STONE_D):
    """A tall tapering stone monument (the 'pyramids' of the cemetery)."""
    w = h * .14
    return [poly([[x - w / 2, base], [x - w * .32, base - h], [x, base - h * 1.05], [x + w * .32, base - h], [x + w / 2, base]], c, "rgba(255,236,206,.45)", 1.2, at, op=op, fx=fx),
            poly([[x, base], [x, base - h * 1.05], [x + w * .32, base - h], [x + w / 2, base]], "rgba(0,0,0,.22)", at=at, op=op, fx=fx),
            ln([[x - w * .38, base - h * .3], [x + w * .38, base - h * .3]], at, "rgba(40,30,20,.5)", 1.2, draw=False, op=op),
            ln([[x - w * .35, base - h * .6], [x + w * .35, base - h * .6]], at, "rgba(40,30,20,.5)", 1.2, draw=False, op=op)]


def amphora(x, y, h, at, c="#c98a5a", fx="pop", op=None):
    """A storage jar standing on y (x = its axis)."""
    w = h * .32
    return [poly([[x - w * .2, y - h], [x + w * .2, y - h], [x + w * .25, y - h * .86], [x + w * .5, y - h * .7], [x + w * .55, y - h * .35], [x + w * .25, y - h * .08], [x, y],
                  [x - w * .25, y - h * .08], [x - w * .55, y - h * .35], [x - w * .5, y - h * .7], [x - w * .25, y - h * .86]], c, "rgba(255,236,206,.5)", 1.2, at, fx=fx,
                 curve=True, op=op),
            ln([[x - w * .22, y - h * .9], [x - w * .55, y - h * .82], [x - w * .45, y - h * .66]], at, c, 3, draw=False, op=op),
            ln([[x + w * .22, y - h * .9], [x + w * .55, y - h * .82], [x + w * .45, y - h * .66]], at, c, 3, draw=False, op=op)]


def bowl(x, y, w, at, c="#c4502e", fx="pop", op=None):
    """A shallow red tableware bowl in side view standing on y."""
    return [poly([[x - w / 2, y - w * .28], [x + w / 2, y - w * .28], [x + w * .38, y - w * .08], [x + w * .12, y], [x - w * .12, y], [x - w * .38, y - w * .08]], c,
                 "rgba(255,236,206,.55)", 1.2, at, fx=fx, curve=True, op=op),
            ln([[x - w / 2 + 6, y - w * .25], [x + w / 2 - 6, y - w * .25]], at, "rgba(255,236,206,.45)", 1.5, draw=False, op=op)]


def beaker(x, y, h, at, c="rgba(159,208,255,.25)", e="#bfe6f5", fx="pop", op=None):
    w = h * .5
    return [poly([[x - w / 2, y - h], [x + w / 2, y - h], [x + w * .3, y - h * .2], [x + w * .2, y], [x - w * .2, y], [x - w * .3, y - h * .2]], c, e, 2, at, fx=fx, op=op),
            gl(x, y - h * .5, h * .8, at, .3, "glow")]


def paw(x, y, s, at, c=GOLD, op=None):
    """A dog's paw print: a pad and four toes."""
    return [poly(E(x, y + .15 * s, .32 * s, .26 * s, 16), c, at=at, fx="pop", op=op)] + \
           [poly(E(x + dx * s, y + dy * s, .11 * s, .14 * s, 12), c, at=round(at + .05, 2), fx="pop", op=op) for dx, dy in ((-.36, -.2), (-.13, -.38), (.13, -.38), (.36, -.2))]


def mill(x, y, r, at, fx="pop"):
    """A millstone seen face on."""
    return [circ(x, y, r, "#8a8378", "rgba(255,236,206,.5)", 2, at, fx=fx), circ(x, y, r * .2, "#1a1612", "rgba(255,236,206,.4)", 1.5, at, fx=fx)] + \
           [ln([[x + r * .25 * math.cos(a), y + r * .25 * math.sin(a)], [x + r * .92 * math.cos(a + .35), y + r * .92 * math.sin(a + .35)]], at, "rgba(40,34,28,.6)", 2, draw=False)
            for a in [k * math.pi / 4 for k in range(8)]]


def coins(x, base, n, at, dt=.06, c="#e8c35a", w=40):
    return [poly(E(x, base - 7 * k, w / 2, w * .16, 18), c, "#7a5a1a", 1.2, at + dt * k, fx="pop") for k in range(n)]


def roundhouse(x, base, w, at, op=None, lit=True):
    h = w * .32
    return [rect(x - w / 2, base - h, w, h, "#4a3a2a", "rgba(255,236,206,.3)", 1.2, 2, at, op=op),
            poly([[x - w * .58, base - h], [x, base - h - w * .48], [x + w * .58, base - h]], "#6a5a3c", "rgba(255,236,206,.3)", 1.2, at, op=op),
            rect(x - w * .07, base - h * .75, w * .14, h * .75, "#f2c98e" if lit else "#120e0b", at=at, op=op)]


def ox(x, y, s, at, c="#1c1612", op=None):
    """A plough ox in side view, hooves on y (s = its height)."""
    body = [[x - .9 * s, y - .55 * s], [x + .5 * s, y - .62 * s], [x + .7 * s, y - .72 * s], [x + .95 * s, y - .6 * s], [x + .85 * s, y - .42 * s], [x + .6 * s, y - .4 * s],
            [x + .55 * s, y], [x + .45 * s, y], [x + .38 * s, y - .32 * s], [x - .6 * s, y - .3 * s], [x - .65 * s, y], [x - .75 * s, y], [x - .85 * s, y - .3 * s]]
    return [poly(body, c, "rgba(255,236,206,.25)", 1, at, fx="rise", op=op)]


def star(x, y, r, at, c=LILAC, op=None, fx="pop"):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * .42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return poly(pts, c, at=at, fx=fx, op=op)


def swords(x, y, s, at, c=LILAC, style="known", op=None):
    return [ln([[x - s, y + s], [x + s, y - s]], at, c, 4, style, dur=.3, op=op), ln([[x + s, y + s], [x - s, y - s]], at + .1, c, 4, style, dur=.3, op=op),
            ln([[x - s * .55, y + s * .25], [x - s * .25, y + s * .55]], at + .2, c, 4, draw=False, op=op), ln([[x + s * .55, y + s * .25], [x + s * .25, y + s * .55]], at + .2, c, 4, draw=False, op=op)]


def mist(y, at=-1, op=.09, seed=1):
    rnd = random.Random(seed)
    pts = [(-40, y)] + [(-40 + 200 * k, y - rnd.uniform(6, 22)) for k in range(1, 10)] + [(1820, y - 10), (1820, y + 34), (-40, y + 34)]
    return poly(pts, "rgba(232,226,236,%s)" % op, at=at, curve=False)


def lead_cross(cx, top, at, s=1.0, op=None, fx=None, c=LEAD, letters=True, lsize=46):
    """The Glastonbury cross, s = scale (1.0: about 720 wide and 640 tall), with its inscription in incised capitals (schematic layout)."""
    uw, bw, bt, bb, H = 130 * s, 360 * s, top + 120 * s, top + 330 * s, 640 * s
    P = [(cx - uw, top), (cx + uw, top), (cx + uw, bt), (cx + bw, bt), (cx + bw, bb), (cx + uw, bb), (cx + uw, top + H), (cx - uw, top + H), (cx - uw, bb), (cx - bw, bb),
         (cx - bw, bt), (cx - uw, bt)]
    inset = lambda d: [(cx - uw + d, top + d), (cx + uw - d, top + d), (cx + uw - d, bt + d), (cx + bw - d, bt + d), (cx + bw - d, bb - d), (cx + uw - d, bb - d),
                       (cx + uw - d, top + H - d), (cx - uw + d, top + H - d), (cx - uw + d, bb - d), (cx - bw + d, bb - d), (cx - bw + d, bt + d), (cx - uw + d, bt + d)]
    out = [poly([(x + 18 * s, y + 22 * s) for x, y in P], "rgba(0,0,0,.6)", at=at, op=op, fx=fx),
           poly(P, c, "rgba(220,226,232,.8)", max(1.2, 2.2 * s), at, op=op, fx=fx)]
    if s >= .5:
        # light from the upper left: the left arm and the top lit, the right arm and the foot in shade; a worn bevel
        out += [poly([(cx - bw, bt), (cx - uw, bt), (cx - uw, top), (cx, top), (cx, bb), (cx - bw, bb)], "rgba(255,250,240,.07)", at=at, op=op, fx=fx),
                poly([(cx + uw * .4, bt), (cx + bw, bt), (cx + bw, bb), (cx + uw, bb), (cx + uw, top + H), (cx + uw * .4, top + H)], "rgba(0,0,0,.13)", at=at, op=op, fx=fx),
                poly(inset(10 * s), "none", "rgba(28,30,34,.5)", 2.5 * s, at, op=op, fx=fx),
                poly(inset(16 * s), "none", "rgba(230,236,240,.18)", 1.5 * s, at, op=op, fx=fx),
                ln([(cx - uw, top + H), (cx - uw, bb), (cx - bw, bb)], at, "rgba(20,22,26,.6)", 3 * s, draw=False, op=op),
                ln([(cx - bw, bb), (cx - bw, bt), (cx - uw, bt), (cx - uw, top), (cx + uw, top)], at, LEAD_L, 2.5 * s, draw=False, op=op)]
        rnd = random.Random(9)
        for k in range(22):                            # patina: pale oxide blooms and dark pits
            x = cx + rnd.uniform(-uw * .85, uw * .85)
            y = top + rnd.uniform(24, H - 30) * 1.0
            if bt + 10 < y < bb - 10:
                x = cx + rnd.uniform(-bw * .9, bw * .9)
            pale = k % 3 != 0
            out.append(poly(E(x, y, rnd.uniform(8, 26) * s, rnd.uniform(4, 12) * s, 12), "rgba(226,232,236,.10)" if pale else "rgba(24,26,30,.28)", at=at, op=op, fx=fx))
    if letters:
        rows = [("HIC IACET", bt + 62 * s, lsize * s), ("SEPULTUS INCLITUS", bt + 124 * s, lsize * s), ("REX ARTURIUS", bt + 186 * s, lsize * s),
                ("IN INSULA", bb + 90 * s, (lsize - 6) * s), ("AVALONIA", bb + 160 * s, (lsize - 6) * s)]
        for t, y, sz in rows:
            out += [lab(cx + 1.5 * s, y + 1.5 * s, t, at, "rgba(232,236,242,.5)", round(sz), st="serif", halo=False, scl=True, op=op),
                    lab(cx, y, t, at, INCISE, round(sz), st="serif", halo=False, scl=True, op=op)]
    return out


def CROSS_ROWS(cx, top, s=1.0):
    """The baselines of the inscription's rows (for the glows): REX ARTURIUS and AVALONIA."""
    bt, bb = top + 120 * s, top + 330 * s
    return {"rex": bt + 186 * s, "aval": bb + 160 * s}


GROUND = "#2b241c"


# ================================================================== COLD OPEN · the cross and the grave
CX1, TOP1 = 1100, 148


def s1():
    """The hero image, complete from the first frame: the lead cross of Glastonbury, its Latin incised, lit warm from the upper left, on dark earth."""
    t91, tka, tav = T("s1", "eleven ninety-one"), T("s1", "King Arthur"), T("s1", "Avalon")
    rnd = random.Random(3)
    els = [rect(-40, -40, 1860, 1080, "#1d150e", at=-1, op=.5)]
    for k, (y, c) in enumerate(((210, "rgba(90,70,48,.18)"), (470, "rgba(70,54,38,.2)"), (760, "rgba(96,76,52,.18)"))):
        els.append(poly([(-40, y)] + [(-40 + 190 * j, y + 18 * math.sin(j * 1.3 + k)) for j in range(1, 11)] + [(1820, y + 60), (-40, y + 70)], c, at=-1))
    els += [poly([(110, 1000), (150, 660), (300, 600), (520, 580), (700, 620), (760, 1000)], "#3d3730", "rgba(255,236,206,.22)", 1.5, -1),
            ln([(300, 600), (360, 700), (330, 820)], -1, "rgba(0,0,0,.4)", 2, draw=False),
            poly([(1480, 1000), (1500, 720), (1660, 680), (1820, 720), (1820, 1000)], "#352f29", "rgba(255,236,206,.18)", 1.5, -1),
            gl(470, 280, 820, -1, .34, "lamp"), gl(1650, 420, 460, -1, .14, "glow")]
    for k in range(46):
        x, y = rnd.uniform(90, 1700), rnd.uniform(780, 990)
        els.append(poly(E(x, y, rnd.uniform(5, 15), rnd.uniform(3, 8), 10), "#5a4a3a", "rgba(255,236,206,.15)", .8, -1, op=.8))
    els += lead_cross(CX1, TOP1, -1)
    rows = CROSS_ROWS(CX1, TOP1)
    els += [rect(CX1 - 180, rows["rex"] - 40, 360, 54, "rgba(242,201,142,.18)", GOLD, 2.5, 8, tka, fx="pop"),
            lab(CX1, rows["rex"], "REX ARTURIUS", tka + .05, AU, 46, st="serif", halo=False, scl=True, fx="pop"),
            gl(CX1, rows["rex"] - 14, 280, tka, .45, "lamp"),
            lab(CX1 + 392, rows["rex"] - 4, "King Arthur", tka + .2, GOLD, 34, "start", st="lab"),
            rect(CX1 - 118, rows["aval"] - 34, 236, 46, "rgba(201,193,238,.16)", LILAC, 2.5, 8, tav, fx="pop"),
            lab(CX1, rows["aval"], "AVALONIA", tav + .05, LILAC, 40, st="serif", halo=False, scl=True, fx="pop"),
            lab(CX1 + 160, rows["aval"] - 4, "isle of Avalon", tav + .2, LILAC, 32, "start", st="ital")]
    els += chip(470, 520, "1191", AMBER, t91, 34)
    return {"base": "dark", "cam": CAM, "els": els}


G2, M2 = 400, 70                     # the cemetery: ground line, units per metre (5 m = 350)


def trunk(x0, x1, y0, y1, at, fx="fill"):
    """A hollowed oak trunk in long section: rounded ends, bark, the dark hollow."""
    rx = (y1 - y0) * .5
    outer = [(x0 + rx, y0)] + [(x0 + rx - rx * math.sin(math.radians(a)), (y0 + y1) / 2 - rx * math.cos(math.radians(a))) for a in range(0, 181, 30)] + \
            [(x1 - rx, y1)] + [(x1 - rx + rx * math.sin(math.radians(a)), (y0 + y1) / 2 + rx * math.cos(math.radians(a))) for a in range(0, 181, 30)]
    out = [poly(outer, "#6a4a2c", "rgba(255,226,190,.55)", 2, at, fx=fx, dur=.6)]
    out += [ln([(x0 + rx + 30 * k, y0 + 4), (x0 + rx + 30 * k + 14, y0 + 10)], at + .3, "rgba(40,24,12,.6)", 2, draw=False) for k in range(int((x1 - x0 - 2 * rx) / 30))]
    out += [poly([(x0 + rx * .8, y0 + 12), (x1 - rx * .8, y0 + 12), (x1 - rx * .9, y1 - 14), (x0 + rx * .9, y1 - 14)], "#20140b", at=at + .2, fx=fx, dur=.5)]
    return out


def s2():
    """The cemetery of Glastonbury Abbey at dusk, cut open: two stone pillars, the monks, the pit, the cross under its stone, the oak trunk 5 m down."""
    ta, tp, to, tf, tb = T("s2", "Glastonbury Abbey"), T("s2", "stone pillars"), T("s2", "oak trunk"), T("s2", "five metres"), T("s2", "bones")
    bot = G2 + 5 * M2
    els = [rect(-40, -40, 1860, G2 + 40, "#0a0c1a", at=-1, op=.42)]
    els += church(110, G2, 470, 200, -1, op=.8)
    els += pillar(600, G2, 210, -1) + pillar(1180, G2, 180, -1)
    rnd = random.Random(8)
    for k in range(30):                                 # stones in the earth
        x, y = rnd.uniform(80, 1700), rnd.uniform(G2 + 30, 760)
        if 740 < x < 1040:
            continue
        els.append(poly(E(x, y, rnd.uniform(6, 16), rnd.uniform(4, 9), 10), "#4a3e32", at=-1, op=.7))
    els += [poly([(760, G2), (1020, G2), (1000, bot), (780, bot)], "#120d09", "rgba(255,226,190,.45)", 1.5, -1),
            poly([(1030, G2), (1060, G2 - 34), (1120, G2 - 46), (1170, G2 - 30), (1200, G2)], "#4a3a28", "rgba(255,226,190,.3)", 1.2, -1),
            gl(890, G2 + 200, 260, -1, .22, "lamp"),
            poly([(800, G2 + 160), (980, G2 + 152), (984, G2 + 172), (796, G2 + 180)], "#6b6358", "rgba(255,236,206,.45)", 1.2, -1)]
    els += lead_cross(890, G2 + 190, -1, s=.075, letters=False) + [gl(890, G2 + 205, 60, -1, .55, "lamp")]
    els += trunk(800, 990, bot - 52, bot - 4, to - .2)
    els += [gl(895, bot - 28, 120, tb, .65, "lamp")]
    for k, (x, f, yb) in enumerate(((700, 1, G2), (1060, -1, G2 - 34), (1112, -1, G2 - 44))):
        els += monk(x, yb, 119, .3 + .25 * k, face=f)
    els += [ln([(728, G2 - 60), (760, G2 + 6)], .5, "#8a6a48", 4, draw=False), ln([(1036, G2 - 88), (1004, G2 - 16)], .7, "#8a6a48", 4, draw=False),
            ln([(1140, G2 - 120), (1150, G2 - 170)], .8, "#6a5a48", 3, draw=False), circ(1150, G2 - 178, 9, "#ffd08a", at=.8, fx="pop"), gl(1150, G2 - 178, 160, .8, .7, "lamp")]
    els += [{"k": "dim", "x1": 1060, "y1": G2, "x2": 1060, "y2": bot, "t": "5 m", "c": AMBER, "lx": 34, "dur": .8, "in": tf}]
    els += [lab(345, 158, "Glastonbury Abbey", ta, DIM, 28), lab(890, 160, "two stone pillars", tp, BONE, 30),
            ln([(760, 168), (622, 186)], tp + .2, DIM, 1.5, dur=.3), ln([(1020, 168), (1166, 212)], tp + .2, DIM, 1.5, dur=.3),
            lab(1012, bot - 16, "oak trunk", to + .4, BONE, 28, "start")]
    layers = [{"d": 0, "c": "#3a2c20", "t": ""}, {"d": 120, "c": "#33261b", "t": ""}, {"d": 250, "c": "#2a2017", "t": ""}]
    return {"base": "section", "tod": "dusk", "ground": G2, "layers": layers, "lx": 120, "cam": CAM, "els": els}


def s3_add():
    """The question: the legend's king glimmers in the sky beside the grave; a question mark between the legend and the ground."""
    tq, ta = T("s3", "Was this"), T("s3", "at all")
    kx = 1440
    els = [gl(kx, 250, 330, .2, .5, "glow")] + king(kx, G2 - 8, 262, .3, outline=LILAC, style="claimed", fx="fade", w=3.5, fill="rgba(201,193,238,.22)")
    els += [lab(kx - 150, 190, "the legend", .9, LILAC, 34, "end", st="ital"), lab(1240, 600, "the ground", 1.2, BONE, 30, "start")]
    els += qmark(1250, 330, ta - .4, 110)
    return els


# ================================================================== CHAPTER 1 · When Rome left
VB = View(-10.8, 6.2, 49.4, 56.0, (90, 120, 1600, 680))
TOWNS = {"London": (-0.13, 51.51), "York": (-1.08, 53.96), "Chester": (-2.89, 53.19), "Caerleon": (-2.96, 51.61), "Bath": (-2.36, 51.38),
         "Exeter": (-3.53, 50.72), "Lincoln": (-0.54, 53.23), "Cirencester": (-1.97, 51.72), "Colchester": (0.90, 51.89), "Wroxeter": (-2.65, 52.67),
         "Canterbury": (1.08, 51.28), "Carlisle": (-2.93, 54.89), "Leicester": (-1.13, 52.63), "Gloucester": (-2.24, 51.86)}
ROADS = [("London", "Colchester"), ("London", "Canterbury"), ("London", "Lincoln"), ("Lincoln", "York"), ("London", "Wroxeter"), ("Wroxeter", "Chester"),
         ("Exeter", "Bath"), ("Bath", "Cirencester"), ("Cirencester", "Leicester"), ("Leicester", "Lincoln"), ("London", "Cirencester"), ("Gloucester", "Caerleon"),
         ("Cirencester", "Gloucester"), ("York", "Carlisle"), ("Chester", "York")]


def s5():
    """Roman Britain at night: towns light up, the roads draw between them, villas and coins glint; Hadrian's Wall in the north."""
    v = VB
    tr = T("s5", "province of")
    tt, tro, tc = T("s5", "towns"), T("s5", "roads"), T("s5", "coins")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for k, (a, b) in enumerate(ROADS):
        els.append(ln([v.p(*TOWNS[a]), v.p(*TOWNS[b])], tro + .06 * k, AMBER, 2.2, dur=.7, op=.85))
    els.append(ln([v.p(-3.27, 54.95), v.p(-1.53, 54.99)], tro + .5, BONE, 4, dur=.6))
    for k, (n, q) in enumerate(TOWNS.items()):
        x, y = v.p(*q)
        els += [gl(x, y, 46, tt + .05 * k, .7, "lamp"), dot(x, y, 5, "#ffe2a8", round(tt + .05 * k, 2))]
    rnd = random.Random(4)
    for k in range(16):
        lo, la = rnd.uniform(-3.3, 0.9), rnd.uniform(50.9, 52.4)
        x, y = v.p(lo, la)
        els.append(dot(x, y, 3, BONE, round(tt + .6 + .04 * k, 2), op=.75))
    for k in range(9):
        lo, la = rnd.uniform(-2.6, 0.6), rnd.uniform(51.2, 53.6)
        x, y = v.p(lo, la)
        els += [circ(x, y, 7, AU, "#7a5a1a", 1.2, tc + .06 * k, fx="pop"), gl(x, y, 26, tc + .06 * k, .5, "lamp")]
    lx, ly = v.p(-0.13, 51.51)
    yx, yy = v.p(-1.08, 53.96)
    els += [lab(lx + 18, ly + 34, "London", tt + .2, BONE, 26, "start"), lab(yx + 18, yy + 8, "York", tt + .3, BONE, 26, "start"),
            lab(*v.p(2.9, 53.9), "Britannia", tr, GOLD, 40, st="ital")]
    els += chip(330, 190, "about 410", AMBER, .3, 28)
    return {"base": "map", "cam": CAM, "els": els}


def s6_add():
    """The last armies march off across the Channel to Gaul; a sealed letter flies in from the south-east on a dotted arc (the story); the lights dim."""
    v = VB
    tl, te = T("s6", "last armies"), T("s6", "emperor")
    kx, ky = v.p(1.0, 51.15)
    els = []
    for k, a in enumerate(((-1.08, 53.9), (-2.8, 53.0), (-0.3, 51.6))):
        p0 = v.p(*a)
        p2 = v.p(2.5 + .25 * k, 50.15 - .2 * k)
        els.append(arr([p0, (kx, ky + 6 * k), p2], tl - .3 + .25 * k, AMBER, 3.5, dur=1.5))
    for k in range(10):
        x, y = v.p(0.55 + .16 * (k % 5), 51.35 - .14 * (k // 5))
        els.append(figure(x, y, 26, tl + .5 + .05 * k, AMBER, "pop"))
    els += [lab(*v.p(-1.2, 50.15), "the last armies", tl + .8, AMBER, 30, "middle")]
    sx, sy = v.p(6.0, 49.6)
    ex, ey = v.p(0.7, 51.95)
    els += [ln([(sx, sy), ((sx + ex) / 2 + 60, min(sy, ey) - 150), (ex + 20, ey - 26)], te, LILAC, 3, "claimed", 1.3, True),
            rect(ex - 22, ey - 44, 44, 30, PARCH, "#8a6a3e", 1.5, 3, te + 1.2, fx="pop"), circ(ex, ey - 29, 6, "#b0301e", at=te + 1.3, fx="pop"),
            lab(*v.p(4.4, 52.15), "look to your", te + .8, LILAC, 28, "middle", st="ital"), lab(*v.p(4.4, 51.85), "own defence?", te + .9, LILAC, 28, "middle", st="ital")]
    cx_, cy_ = v.p(-1.6, 52.6)
    els += softveil(cx_, cy_, 300, te + 1.6, "#0a1218", .5, n=14, dur=1.8)
    return els


def plinth(x, y, at, w=170):
    return [rect(x - w / 2, y, w, 26, "#3a3129", "rgba(255,236,206,.35)", 1.5, 4, at), rect(x - w / 2 + 14, y + 26, w - 28, 120, "#2a231d", "rgba(255,236,206,.2)", 1, 2, at)]


def s7():
    """Four lights of Roman Britain on their plinths: coins, pottery, a town, writing; each goes dark as it is named."""
    tc, tp, tw = T("s7", "stop arriving"), T("s7", "pottery and towns"), T("s7", "writes anything")
    xs, py = (340, 700, 1060, 1420), 560
    els = []
    for x in xs:
        els += plinth(x, py, -1)
    els += [gl(x, py - 90, 240, -1, .7, "lamp") for x in xs]
    els += coins(xs[0], py - 2, 9, -1, 0, w=80)
    els += [{"k": "lib", "k2": "vase", "x": xs[1], "y": py, "h": 160, "w": 118, "tone": "#c8743c", "in": -1}]
    gx = xs[2]
    els += [rect(gx - 80, py - 150, 160, 150, "#7a6650", "rgba(255,236,206,.55)", 1.5, 2, -1),
            poly([(gx - 34, py), (gx - 34, py - 70), (gx, py - 100), (gx + 34, py - 70), (gx + 34, py)], "#1a1410", at=-1),
            rect(gx - 92, py - 172, 26, 172, "#8a7660", "rgba(255,236,206,.55)", 1.2, 1, -1), rect(gx + 66, py - 172, 26, 172, "#8a7660", "rgba(255,236,206,.55)", 1.2, 1, -1)]
    els += [rect(gx - 60 + 30 * k, py - 132, 14, 20, "#ffd590", at=-1) for k in range(5)]
    wx = xs[3]
    els += [poly([(wx - 80, py - 8), (wx - 70, py - 120), (wx + 70, py - 126), (wx + 80, py - 12)], "#f3e8d0", PARCH_E, 1.5, -1),
            {"k": "glyphs", "x": wx - 58, "y": py - 108, "w": 116, "h": 84, "rows": 5, "cols": 4, "kind": "latin", "c": "rgba(74,58,40,.8)", "in": -1},
            ln([(wx + 40, py - 60), (wx + 110, py - 200)], -1, "#e9dccb", 4, draw=False), poly([(wx + 104, py - 196), (wx + 150, py - 250), (wx + 116, py - 190)], "#e9dccb", at=-1)]
    els += chip(xs[0], 230, "after about 402", AMBER, tc - .6, 28)
    dark = "#0d0b09"
    outs = [(xs[0], tc + .3, [rect(xs[0] - 46, py - 90, 92, 92, dark, r=10, at=0, op=.62)]),
            (xs[1], tp, [poly(E(xs[1], py - 80, 64, 84, 24), dark, at=0, op=.62)]),
            (xs[2], tp + .6, [rect(gx - 96, py - 176, 192, 176, dark, r=4, at=0, op=.62)]),
            (xs[3], tw, [poly([(wx - 84, py - 4), (wx - 74, py - 124), (wx + 74, py - 130), (wx + 84, py - 8)], dark, at=0, op=.62),
                         poly([(wx + 30, py - 50), (wx + 120, py - 210), (wx + 160, py - 256), (wx + 112, py - 180), (wx + 50, py - 40)], dark, at=0, op=.62)])]
    for x, at, cover in outs:
        els += softveil(x, py - 90, 185, at, dark, .78, n=18, dur=1.0)
        for e in cover:
            e["in"] = round(at, 2); e["dur"] = 1.0
        els += cover
    for x, t in zip(xs, ("coins", "pottery", "towns", "writing")):
        els.append(lab(x, py + 80, t, -1, BONE, 30))
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s8():
    """A farmstead at dusk, people at work in the light of a big lantern; the lantern dims, the people work on in the shadow."""
    tl, tg = T("s8", "light we see"), T("s8", "goes out")
    g = 720
    els = [poly([(80, g + 2)] + [(80 + 70 * k, g - 4 - 4 * math.sin(k)) for k in range(1, 22)] + [(1600, g + 2)], "#3c3a26", at=-1, op=.9)]
    els += [ln([(1000 + 70 * k, g + 4), (900 + 120 * k, g + 80)], -1, "rgba(150,120,70,.45)", 2.5, draw=False) for k in range(7)]
    els += roundhouse(500, g - 2, 380, -1) + [ln([(500, g - 300), (484, g - 350), (506, g - 400), (488, g - 450)], -1, "rgba(220,210,200,.3)", 9, curve=True, draw=False)]
    els += roundhouse(170, g, 200, -1, lit=False)
    els += [figure(800, g, 180, -1, "#2a2420", None), ln([(826, g - 110), (870, g - 64)], -1, "#2a2420", 8, draw=False),
            poly(E(884, g - 56, 36, 24, 14), "#6a5238", "rgba(255,236,206,.35)", 1, -1), figure(930, g, 112, -1, "#2a2420", None)]
    els += ox(1150, g + 2, 136, -1, "#241c16") + [figure(1340, g, 184, -1, "#2a2420", None), ln([(1310, g - 96), (1210, g - 80)], -1, "#6a5238", 5, draw=False)]
    lx, ly = 1560, 300
    els += [ln([(lx, 110), (lx, ly - 70)], -1, "#5a5048", 3, draw=False),
            poly([(lx - 38, ly - 70), (lx, ly - 104), (lx + 38, ly - 70)], "#3a3129", "#c9a46a", 2, -1),
            poly([(lx - 30, ly - 70), (lx + 30, ly - 70), (lx + 38, ly + 30), (lx - 38, ly + 30)], "rgba(255,226,168,.5)", "#c9a46a", 2, -1),
            poly([(lx - 22, ly + 30), (lx + 22, ly + 30), (lx + 14, ly + 46), (lx - 14, ly + 46)], "#3a3129", "#c9a46a", 2, -1),
            gl(lx, ly - 20, 1100, -1, .5, "lamp"), gl(lx, ly - 20, 150, -1, .95, "lamp"),
            poly([(lx - 30, ly + 30), (lx + 30, ly + 30), (1100, g + 60), (300, g + 60)], "rgba(255,214,150,.06)", at=-1)]
    els += [veil(-40, 100, 1860, 900, tg, "#07060a", op=.55, dur=2.2)]
    els += [poly([(lx - 30, ly - 70), (lx + 30, ly - 70), (lx + 38, ly + 30), (lx - 38, ly + 30)], "#120e0b", at=tg, op=.8, dur=1.4)]
    els += [lab(lx - 70, ly + 100, "the light we see it by", tl, AMBER, 30, "end"), lab(1000, 470, "life goes on", tg + 1.4, BONE, 30)]
    return {"base": "sky", "tod": "dusk", "ground": g, "groundc": GROUND, "sun": [300, 580, 26],
            "ridges": [{"y": 660, "a": 50, "c": "#3b3140", "seed": 4}, {"y": 710, "a": 20, "c": "#2a2229", "seed": 8}], "cam": CAM, "els": els}


VN = View(-6.5, 13.5, 49.6, 58.6, (90, 120, 1600, 680))


def s9():
    """The North Sea: boats cross from today's Netherlands, Germany and Denmark to the east coast of Britain."""
    v = VN
    tn, ts = T("s9", "North Sea"), T("s9", "Saxons")
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(3.0, 55.6), "North Sea", .4, "#9fd0ff", 38, st="ital"),
           lab(*v.p(-3.0, 52.6), "Britain", .6, BONE, 30)]
    routes = [((8.4, 55.6), (-0.3, 54.2)), ((8.6, 54.0), (1.5, 52.8)), ((7.0, 53.6), (1.2, 52.2)), ((5.2, 53.3), (1.4, 51.6)), ((9.0, 55.0), (0.2, 53.3)),
              ((6.2, 53.5), (0.9, 51.9)), ((8.2, 54.4), (-0.1, 53.7)), ((4.5, 52.8), (1.3, 51.3))]
    for k, (a, b) in enumerate(routes):
        p0, p1 = v.p(*a), v.p(*b)
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 30)
        at = ts - .4 + .35 * k
        els.append(arr([p0, mid, p1], at, AMBER, 2.5, dur=1.4, op=.85))
        els += ship(mid[0], mid[1] + 4, 52, at + .4, "#e8d6b8", face=-1, oars=4, mast=False)
    els += [lab(*v.p(10.4, 52.3), "today's Germany", tn + .8, DIM, 28), lab(*v.p(9.6, 56.6), "Denmark", tn + 1.0, DIM, 28),
            {"k": "scale", "x": 160, "y": 760, "w": round(v.km(200), 1), "t": "200 km", "in": 1.0}]
    return {"base": "map", "cam": CAM, "els": els}


def s10():
    """Gildas's account, framed as his: three ships drawn up on a beach, a British ruler inviting them in; the monthly supplies; the treaty torn."""
    tg, t3, tm, tr = T("s10", "Gildas"), T("s10", "three ships"), T("s10", "monthly supplies"), T("s10", "rebelled")
    hz = 560
    shore = [(-40, 770), (420, 724), (820, 668), (1200, 632), (1820, 616)]
    els = [poly([(-40, hz), (1820, hz)] + shore[::-1], "#24485c", at=-1),
           ln([(-40, hz + 2), (1820, hz + 2)], -1, "rgba(255,226,190,.45)", 1.5, draw=False)]
    els += [ln([(80 + 160 * k, hz + 30 + 18 * (k % 3)), (150 + 160 * k, hz + 30 + 18 * (k % 3))], -1, "rgba(191,230,245,.25)", 2, draw=False) for k in range(9)]
    els += [poly(shore + [(1820, 1000), (-40, 1000)], "#6e5a42", "rgba(255,226,190,.3)", 1.5, -1),
            ln(shore, -1, "rgba(220,236,240,.55)", 3, curve=True, draw=False)]
    for k, (x, y) in enumerate(((250, 736), (520, 702), (790, 672))):
        els += ship(x, y, 250, t3 - .2 + .35 * k, "#1d1611", face=1, oars=9)
    els += tagc(520, 520, "3 ships", t3 + .9, AMBER, 26)
    els += warrior(930, 676, 120, .4, "#1d1611", face=1) + warrior(1000, 672, 116, .55, "#1d1611", face=1) + warrior(870, 680, 112, .7, "#1d1611", face=1)
    els += king(1440, 650, 160, .3, "#2a221c", crown_c=AU) + [ln([(1420, 540), (1340, 512)], .5, "#2a221c", 10, draw=False)]
    els += [rect(110, 150, 1560, 640, "rgba(201,193,238,.03)", LILAC, 2.5, 14, tg, style="claimed"), lab(140, 192, "Gildas's story", tg + .3, LILAC, 30, "start", st="ital")]
    sx = 1180
    els += [poly([(sx - 40, 640), (sx - 48, 582), (sx - 22, 550), (sx + 22, 550), (sx + 48, 582), (sx + 40, 640)], "#a8875a", "rgba(255,236,206,.5)", 1.5, tm, fx="pop", curve=True),
            rect(sx - 26, 420, 84, 96, PARCH, PARCH_E, 1.5, 4, tm + .2, fx="pop"), rect(sx - 26, 420, 84, 24, "#b0301e", at=tm + .2, fx="pop"),
            lab(sx + 16, 492, "30", tm + .3, INK, 34, st="serif", halo=False, fx="pop"), lab(sx + 16, 396, "monthly supplies", tm + .5, BONE, 26)]
    tx, ty = 1180, 280
    els += [rect(tx - 150, ty - 40, 300, 90, PARCH, PARCH_E, 1.5, 6, tm - .6, fx="pop"),
            {"k": "glyphs", "x": tx - 130, "y": ty - 28, "w": 260, "h": 64, "rows": 3, "cols": 6, "kind": "latin", "c": "rgba(74,58,40,.6)", "in": round(tm - .5, 2)},
            lab(tx, ty - 58, "treaty", tm - .4, BONE, 26),
            ln([(tx - 6, ty - 46), (tx + 10, ty - 10), (tx - 8, ty + 14), (tx + 6, ty + 56)], tr, RED, 5, dur=.4),
            veil(tx - 4, ty - 44, 160, 98, tr + .3, "#141019", op=.5, dur=.4)]
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": [300, 520, 24], "ridges": [{"y": 548, "a": 26, "c": "#3b3140", "seed": 5}, {"y": 560, "a": 8, "c": "#2a2229", "seed": 2}],
            "cam": CAM, "els": els}


def card_(x, y, at, c, w=88, h=124, rot=0):
    """A playing card: its back in the deck's colour, a lighter rim, a small diamond pattern."""
    els = [rect(-w / 2, -h / 2, w, h, c, "rgba(255,255,255,.6)", 2, 8, -1),
           rect(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, "none", "rgba(255,255,255,.35)", 1.5, 5, -1),
           poly([(0, -h * .28), (w * .22, 0), (0, h * .28), (-w * .22, 0)], "rgba(255,255,255,.28)", at=-1)]
    return grp(els, at, "pop", tr="translate(%s %s) rotate(%s)" % (round(x, 1), round(y, 1), round(rot, 1)))


def s11():
    """Two decks, amber (Britain) and blue (across the sea), riffle into one shuffled fan; a DNA helix above."""
    td, tc = T("s11", "DNA"), T("s11", "pack of cards")
    els = []
    for k in range(8):
        els.append(card_(220 + 6 * k, 600 - 5 * k, -1, "#b07a3c", rot=-8 + 2 * k))
        els.append(card_(1560 - 6 * k, 600 - 5 * k, -1, "#3a78a8", rot=8 - 2 * k))
    els += [lab(250, 730, "Britain", .3, AMBER, 30), lab(1530, 730, "across the sea", .3, BLUE, 30)]
    rnd = random.Random(8)
    seq = [1 if rnd.random() < .5 else 0 for _ in range(15)]
    for k, s in enumerate(seq):
        ang = -46 + 6.6 * k
        x = 889 + 330 * math.sin(math.radians(ang))
        y = 760 - 330 * math.cos(math.radians(ang))
        els.append(card_(x, y, tc + .2 + .14 * k, "#3a78a8" if s else "#b07a3c", rot=ang))
    hx0, hx1, hy = 560, 1220, 200
    a1 = [(hx0 + (hx1 - hx0) * k / 40, hy + 34 * math.sin(k * .5)) for k in range(41)]
    a2 = [(hx0 + (hx1 - hx0) * k / 40, hy - 34 * math.sin(k * .5)) for k in range(41)]
    els += [ln(a1, td, BLUE, 3, dur=1.0, curve=True), ln(a2, td + .1, AMBER, 3, dur=1.0, curve=True)]
    els += [ln([a1[k], a2[k]], td + .5 + .02 * k, "rgba(245,236,220,.4)", 1.5, draw=False) for k in range(1, 41, 3)]
    els += [lab(889, 290, "ancient DNA", td + .3, BONE, 32)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


VE = View(-4.5, 12.5, 50.2, 57.2, (100, 160, 760, 560))


def s12():
    """Eastern England and the North Sea (a map in a window); 100 squares, 76 turn blue: up to three quarters of the ancestry from across the sea."""
    v = VE
    tq, tg = T("s12", "three quarters"), T("s12", "northern Germany")
    els = [{"k": "group", "clip": [90, 150, 780, 580, 16], "bg": "#1d3a4a", "in": -1, "els": [{"k": "map", "land": v.land()}]},
           rect(90, 150, 780, 580, "none", "rgba(255,236,206,.35)", 2, 16, -1)]
    ex, ey = v.p(0.9, 52.4)
    gx, gy = v.p(9.2, 54.6)
    els += [gl(ex, ey, 90, .3, .6, "lamp"), lab(ex - 10, ey + 100, "eastern England", .5, BONE, 28),
            arr([(gx, gy), ((gx + ex) / 2, min(gy, ey) - 90), (ex + 30, ey - 10)], tg - 1.2, BLUE, 4, dur=1.2)]
    x0, y0, p, q = 1000, 190, 52, 44
    for k in range(100):
        cx, cy = x0 + p * (k % 10), y0 + p * (k // 10)
        els.append(rect(cx, cy, q, q, AMBER, at=round(.2 + .006 * k, 3), op=.55, r=5))
        if k < 76:
            els.append(rect(cx, cy, q, q, BLUE, at=round(tq - .3 + .035 * k, 3), r=5, fx="pop"))
    els += [lab(x0 + 5 * p - 4, y0 + 10 * p + 40, "up to 76 in 100", tq + 2.4, BLUE, 32), lab(x0 + 5 * p - 4, y0 - 26, "early medieval graves", .6, DIM, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s13():
    """A cemetery in section: grave cuts side by side, tagged blue (ancestry from across the sea) or amber (local), mixed; weapons in both kinds."""
    ts, tw = T("s13", "same cemeteries"), T("s13", "weapons")
    g = 330
    xs = [180 + 210 * k for k in range(7)]
    tags = [1, 0, 0, 1, 0, 1, 0]
    weap = [1, 2, 3]                                    # graves with a spear and a shield boss: two amber, one blue
    els = []
    rnd = random.Random(11)
    for k in range(46):
        x, y = rnd.uniform(80, 1700), rnd.uniform(g + 20, 780)
        els.append(poly(E(x, y, rnd.uniform(5, 14), rnd.uniform(3, 8), 10), "#4a3e32", at=-1, op=.6))
    for k, x in enumerate(xs):
        cut = [(x, g), (x + 170, g), (x + 162, g + 210), (x + 8, g + 210)]
        els += [poly(cut, "#4a3a2a", "rgba(255,226,190,.4)", 1.5, -1), poly([(x + 8, g + 200), (x + 162, g + 200), (x + 162, g + 210), (x + 8, g + 210)], "#2a1f15", at=-1)]
        els += [ln([(x + 20, g + 40 + 46 * j), (x + 150, g + 46 + 46 * j)], -1, "rgba(30,20,12,.35)", 2, "inferred", draw=False) for j in range(4)]
    for k, x in enumerate(xs):
        c = BLUE if tags[k] else AMBER
        els += [ln([(x + 85, g - 60), (x + 85, g - 4)], ts + .15 * k, c, 2.5, draw=False), rect(x + 60, g - 96, 50, 34, c, "rgba(255,255,255,.5)", 1.5, 6, ts + .15 * k, fx="pop")]
    for j, k in enumerate(weap):
        x = xs[k]
        at = tw + .3 * j
        els += [ln([(x + 24, g + 186), (x + 146, g + 102)], at, "#e2cfa4", 4, dur=.4), poly([(x + 146, g + 102), (x + 128, g + 104), (x + 154, g + 90), (x + 142, g + 118)], "#e2cfa4", at=at),
                circ(x + 56, g + 166, 16, "#b0a080", "#f4e8cc", 1.5, at + .2, fx="pop")]
    els += [lab(889, 178, "same cemetery", ts + .3, BONE, 32), lab(xs[2] + 85, g + 262, "weapons: both", tw + .9, AMBER, 30)]
    els += [rect(1240, 610, 30, 22, BLUE, at=ts + 1.2, fx="pop", r=4), lab(1284, 629, "from across the sea", ts + 1.3, BLUE, 26, "start"),
            rect(1240, 656, 30, 22, AMBER, at=ts + 1.4, fx="pop", r=4), lab(1284, 675, "local", ts + 1.5, AMBER, 26, "start")]
    layers = [{"d": 0, "c": "#3c2e22", "t": ""}, {"d": 240, "c": "#30251b", "t": ""}]
    return {"base": "section", "tod": "dusk", "ground": g, "layers": layers, "cam": CAM, "els": els}


def s14():
    """The half-lit world: a long ridge at dusk with the ring of an old hillfort, mist in the valley, a few farm lights, the legend's rider on the ridge."""
    tl = T("s14", "legend")
    g = 760
    ridge = [(-40, 700), (200, 660), (420, 640), (640, 600), (860, 540), (1060, 470), (1240, 448), (1400, 460), (1560, 510), (1700, 560), (1820, 590), (1820, 820), (-40, 820)]
    els = [poly(ridge, "#221d27", "rgba(255,226,190,.25)", 1.5, -1, curve=True),
           ln([(1130, 472), (1240, 452), (1350, 458), (1430, 474)], -1, "rgba(255,226,190,.35)", 3, curve=True, draw=False),
           ln([(1110, 492), (1240, 474), (1360, 480), (1460, 500)], -1, "rgba(255,226,190,.22)", 2.5, curve=True, draw=False)]
    els += [mist(660, op=.10, seed=2), mist(705, op=.08, seed=5), mist(745, op=.07, seed=9)]
    rnd = random.Random(7)
    for k in range(9):
        x = rnd.uniform(120, 1000)
        els += [gl(x, rnd.uniform(690, 760), 26, -1, .7, "lamp")]
    rx, ry = 1250, 452
    els += [gl(rx, ry - 120, 260, .3, .5, "glow")] + horse(rx, ry, 74, .4, LILAC, style="claimed", fill="rgba(201,193,238,.18)", w=2.5, fx="fade")
    els += [poly([(rx - 12, ry - 76), (rx + 14, ry - 76), (rx + 18, ry - 128), (rx + 4, ry - 146), (rx - 10, ry - 132)], "rgba(201,193,238,.18)", LILAC, 2.5, .5, style="claimed"),
            circ(rx + 4, ry - 158, 12, "rgba(201,193,238,.18)", LILAC, 2.5, .5, style="claimed"), ln([(rx + 22, ry - 80), (rx + 52, ry - 200)], .6, LILAC, 3, "claimed", draw=False)]
    els += [lab(rx, ry - 236, "the legend", tl - .6, LILAC, 34, st="ital")]
    return {"base": "sky", "tod": "dusk", "ground": g, "groundc": GROUND, "sun": [430, 600, 20],
            "ridges": [{"y": 690, "a": 60, "c": "#2e2834", "seed": 6}, {"y": 740, "a": 26, "c": "#221c26", "seed": 2}], "cam": CAM, "els": els}


# ================================================================== CHAPTER 2 · The only witness
def arched_window(x, y, w, h, at, sky="#1d2638"):
    pts = [(x, y + h), (x, y + w / 2)] + [(x + w / 2 - w / 2 * math.cos(math.radians(a)), y + w / 2 - w / 2 * math.sin(math.radians(a))) for a in range(0, 181, 20)] + [(x + w, y + h)]
    return [poly(pts, sky, "rgba(255,236,206,.45)", 2.5, at), ln([(x + w / 2, y), (x + w / 2, y + h)], at, "rgba(255,236,206,.3)", 2, draw=False),
            gl(x + w / 2, y + h * .4, w * 1.4, at, .25, "glow")]


def s15():
    """Gildas at his desk by an arched window; his book as a stack of pages: most of it sermon, a part of it history."""
    tb, ts, th = T("s15", "On the Ruin"), T("s15", "sermon"), T("s15", "pages of history")
    f = 730
    els = [ln([(80, f), (980, f)], -1, "#4a3a28", 3, draw=False)] + arched_window(170, 200, 140, 240, -1)
    els += writing_desk(690, 470, 300, -1, 250) + candle(820, 452, -1, 40, 200)
    els += [poly([(560, 516), (600, 490), (720, 466), (700, 496)], "#f3e8d0", PARCH_E, 1.2, -1)]
    els += seated_monk(470, f, 300, -1, face=1)
    els += [lab(470, f + 50, "Gildas", .4, BONE, 30)]
    x0, x1, yb, yt = 1100, 1480, 650, 310
    hh = yb - yt
    split = yb - hh * .76
    els += [rect(x0, split, x1 - x0, yb - split, "#7a3a28", "rgba(255,236,206,.4)", 1.5, 3, ts - .3, fx="fill", dur=.7),
            rect(x0, yt, x1 - x0, split - yt, "#d8b060", "rgba(255,236,206,.5)", 1.5, 3, th - .4, fx="fill", dur=.6),
            gl((x0 + x1) / 2, (yt + split) / 2, 200, th, .45, "lamp")]
    els += [ln([(x0 + 6, y), (x1 - 6, y)], ts, "rgba(20,10,5,.25)", 1, draw=False) for y in range(int(split) + 8, yb - 4, 9)]
    els += [lab((x0 + x1) / 2, yt - 40, "On the Ruin of Britain", tb, GOLD, 36, st="ital"),
            lab(x1 + 24, (split + yb) / 2 + 8, "a sermon", ts + .3, "#e8a080", 28, "start"), lab(x1 + 24, (yt + split) / 2 + 8, "history", th + .2, GOLD, 28, "start")]
    return {"base": "dark", "stars": 12, "cam": CAM, "els": els}


def XG(yr):
    return round(200 + (yr - 450) / 150 * 1380, 1)


YG = 600


def s16():
    """When Gildas wrote: the traditional date about 540, and the case for decades earlier, back to the 480s (on a row of its own)."""
    tt, te = T("s16", "Traditionally"), T("s16", "decades earlier")
    y = YG
    els = [axis(200, 1580, y, [(XG(v), str(v)) for v in (450, 500, 550)] + [(XG(600), "600 CE")], .1)]
    els += [ln([(XG(540), y - 130), (XG(540), y)], tt, GOLD, 3, dur=.4), dot(XG(540), y - 130, 12, GOLD, tt), gl(XG(540), y - 130, 120, tt, .4, "lamp"),
            lab(XG(540), y - 160, "traditional date", tt + .3, GOLD, 30)]
    els += book(XG(540) - 22, y - 250, 44, 60, tt + .2, "#7a3a28")
    els += [{"k": "band", "x0": XG(480), "x1": XG(530), "y": 300, "h": 18, "c": LILAC, "op": .6, "in": te},
            rect(XG(480), 298, XG(530) - XG(480), 22, "none", LILAC, 2, 11, te, style="inferred"),
            lab((XG(480) + XG(530)) / 2, 280, "earlier?", te + .3, LILAC, 30, st="ital"),
            ln([(XG(480), 330), (XG(480), y - 8)], te + .4, LILAC, 1.5, "inferred", dur=.5), ln([(XG(530), 330), (XG(530), y - 8)], te + .4, LILAC, 1.5, "inferred", dur=.5)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s19_add():
    """Badon, in the year Gildas was born: a gold marker on the line, a cradle under it, and about 44 years to the writing."""
    tb = T("s19", "year he was")
    y = YG
    bx = XG(496)
    els = [dot(bx, y, 13, AU, tb - .8), gl(bx, y, 90, tb - .8, .5, "lamp"), lab(bx - 16, y - 24, "Badon", tb - .7, AU, 32, "end")]
    cy = y + 96
    els += [poly([(bx - 44, cy), (bx + 44, cy), (bx + 34, cy + 30), (bx - 34, cy + 30)], "#8a6a48", "rgba(255,236,206,.55)", 1.5, tb, fx="pop"),
            poly([(bx - 44, cy), (bx - 50, cy - 24), (bx - 30, cy - 30), (bx - 18, cy)], "#8a6a48", "rgba(255,236,206,.55)", 1.5, tb, fx="pop"),
            ln([(bx - 34, cy + 30), (bx - 46, cy + 40), (bx + 46, cy + 40), (bx + 34, cy + 30)], tb, "#8a6a48", 3, draw=False),
            lab(bx, cy + 82, "the year he was born", tb + .3, BONE, 28)]
    els += bracket(bx, XG(540), y - 60, tb + .8, "about 44 years", AMBER, up=False, size=28)
    return els


def s17():
    """Ambrosius Aurelianus among the ruins of the Roman world, his parents in purple as faint ghosts behind him, lit on 'left standing'."""
    ta, tp, ts = T("s17", "Ambrosius"), T("s17", "worn the purple"), T("s17", "left standing")
    f = 720
    els = [ln([(80, f), (1700, f)], -1, "#4a3a28", 3, draw=False)]
    for x, h in ((300, 330), (1480, 260)):
        els += [rect(x - 30, f - h, 60, h, "#6a6058", "rgba(255,236,206,.45)", 1.2, 2, -1, op=.75),
                poly([(x - 40, f - h), (x + 40, f - h), (x + 30, f - h - 26), (x - 10, f - h - 40)], "#6a6058", "rgba(255,236,206,.4)", 1, -1, op=.75)]
        els += [ln([(x - 30 + 15 * k, f - h + 6), (x - 30 + 15 * k, f - 6)], -1, "rgba(30,24,20,.35)", 2, draw=False) for k in range(1, 4)]
    for x0 in (120, 420, 1260):
        els += [poly([(x0, f), (x0, f - 44), (x0 + 120, f - 50), (x0 + 120, f - 4)], "#5a5048", "rgba(255,236,206,.3)", 1, -1, op=.7)]
    for k, x in enumerate((640, 1140)):
        h = 250
        els += [circ(x, f - 40 - .9 * h, .085 * h, "#b8a8c8", at=tp - .4 + .2 * k, fx="fade", op=.22),
                poly([(x - .13 * h, f - 40 - .78 * h), (x + .13 * h, f - 40 - .78 * h), (x + .2 * h, f - 40), (x - .2 * h, f - 40)], "#b8a8c8", at=tp - .4 + .2 * k, fx="fade", op=.18),
                poly([(x - .12 * h, f - 40 - .76 * h), (x + .12 * h, f - 40 - .76 * h), (x + .17 * h, f - 40 - .3 * h), (x - .17 * h, f - 40 - .3 * h)], PURPLE,
                     at=tp - .2 + .2 * k, fx="fade", op=.3)]
    els += [poly([(889 - 56, f - 300), (889 + 60, f - 300), (889 + 96, f - 30), (889 - 90, f - 30)], "#4a3436", "rgba(255,236,206,.35)", 1.2, .25, fx="rise")]
    els += warrior(889, f, 380, .3, "#5a4e46", face=1, shield=False)
    els += [gl(889, f - 220, 340, ts, .5, "lamp"), lab(889, f + 56, "Ambrosius Aurelianus", ta, BONE, 34), lab(1150, f - 330, "worn the purple", tp + .2, PURPLE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def hillfort(x0, x1, base, top, at, c="#2e3a26", ring=True, op=None):
    """A rounded hill with a rampart round its top, in side view."""
    w = x1 - x0
    pts = [(x0, base), (x0 + .18 * w, base - .45 * (base - top)), (x0 + .32 * w, top + 8), (x0 + .68 * w, top), (x0 + .84 * w, base - .5 * (base - top)), (x1, base)]
    out = [poly(pts, c, "rgba(255,226,190,.35)", 1.5, at, curve=True, op=op)]
    if ring:
        out += [ln([(x0 + .3 * w, top + 14), (x0 + .5 * w, top - 10), (x0 + .7 * w, top + 2)], at, "#8a7a5a", 6, curve=True, draw=False, op=op),
                ln([(x0 + .27 * w, top + 34), (x0 + .5 * w, top + 14), (x0 + .74 * w, top + 26)], at, "#6a5a40", 5, curve=True, draw=False, op=op)]
    return out


def s18():
    """Wins and losses, back and forth, then the siege of Mount Badon: a hill fort ringed by camp fires, its place unknown."""
    tw, tb = T("s18", "wins and losses"), T("s18", "Mount Badon")
    els = [axis(140, 1000, 240, [], .1)]
    rnd = random.Random(12)
    for k in range(12):
        win = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1][k]
        x = 170 + 68 * k
        els += [rect(x - 14, 240 - (54 if win else -14), 28, 40, GREEN if win else RED, at=tw + .15 * k, fx="pop", r=4, op=.85)]
    els += [lab(160, 190, "wins", tw, GREEN, 26, "start"), lab(160, 330, "losses", tw + .2, RED, 26, "start")]
    els += hillfort(980, 1700, 720, 400, -1, "#29331f")
    els += [figure(1240 + 30 * k, 404 - (k % 2) * 4, 34, .4 + .05 * k, "#1a1511", None) for k in range(8)]
    for k in range(9):
        x = 1000 + 80 * k
        els += [gl(x, 730 - rnd.uniform(0, 20), 40, tb - .4 + .08 * k, .8, "fire"), dot(x, 730, 4, "#ffd08a", round(tb - .4 + .08 * k, 2))]
    els += [lab(1340, 300, "Mount Badon", tb, AU, 36, st="serif")] + tagc(1340, 348, "where? unknown", tb + .8, DIM, 24, "inferred")
    els += [ln([(1000, 240), (1210, 300)], tb - .6, DIM, 2, "inferred", dur=.6)]
    return {"base": "sky", "tod": "dusk", "ground": 760, "groundc": GROUND, "sun": [500, 640, 22],
            "ridges": [{"y": 700, "a": 40, "c": "#2a2430", "seed": 3}, {"y": 750, "a": 18, "c": "#221c26", "seed": 7}], "cam": CAM, "els": els}


def s20_add():
    """On the rampart of Badon, in front of the defenders, an empty dashed leader with a question mark."""
    tq = T("s20", "who led")
    x, y = 1520, 440
    els = [poly([(x - 10, y), (x - 24, y - 64), (x - 18, y - 104), (x, y - 114), (x + 18, y - 104), (x + 24, y - 64), (x + 10, y)], "rgba(201,193,238,.08)", LILAC, 3, tq - .2,
                style="inferred"), circ(x, y - 130, 15, "none", LILAC, 3, tq - .2, style="inferred")]
    els += qmark(x, y - 170, tq + .3, 70)
    return els


def s21():
    """Gildas's book open: 'Ambrosius' lights green, five crowns for the five kings, and an empty slot for Arthur, struck."""
    ta, tk, tn = T("s21", "Ambrosius"), T("s21", "five kings"), T("s21", "never names")
    els = [gl(889, 450, 700, -1, .2, "lamp")] + open_book(889, 200, 1260, 520, -1, rows=11)
    els += [rect(330, 330, 330, 64, "rgba(143,217,176,.14)", GREEN, 2.5, 8, ta - .2, fx="pop"), lab(495, 374, "Ambrosius", ta, GREEN, 38, st="serif")]
    for k in range(5):
        els.append(crown(1010 + 90 * k, 380, 30, tk + .15 * k, AU, fill="#5a4a2a", w=2))
    els += [lab(1190, 440, "five kings", tk + .8, AU, 30)]
    els += [rect(1080, 520, 220, 70, "rgba(201,193,238,.06)", LILAC, 2.5, 10, tn - .3, style="inferred"), lab(1190, 566, "Arthur", tn - .2, LILAC, 34, st="serif"),
            strike(1070, 600, 1310, 512, tn + .4, RED, 6), lab(1190, 650, "not named", tn + .7, RED, 30)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s22():
    """A timber rampart on a hill at dusk, a warrior on it, black ravens wheeling: 'though he was no Arthur'."""
    tg, tr, ta = T("s22", "Gododdin"), T("s22", "black ravens"), T("s22", "no Arthur")
    g = 740
    els = hillfort(220, 1520, g, 520, -1, "#28301f", ring=False)
    for k in range(28):
        x = 480 + 30 * k
        top = 466 - 6 * math.sin(k * .7)
        els += [rect(x, top, 14, 560 - top, "#4a3a28", "rgba(255,226,190,.25)", 1, 2, -1)]
    els += [rect(460, 520, 860, 16, "#3a2c20", at=-1)]
    els += warrior(880, 470, 150, .3, "#14100c", face=1)
    for k, (x, y, s) in enumerate(((740, 300, 64), (850, 240, 74), (980, 280, 60), (1090, 220, 68), (1200, 290, 54), (680, 210, 50), (940, 170, 56))):
        els.append(raven(x, y, s, tr + .12 * k, flip=1 if k % 2 else -1))
    els += chip(300, 210, "about 600", AMBER, tg, 28)
    els += [lab(1420, 410, "he was no Arthur", ta - .2, LILAC, 36, st="ital")]
    return {"base": "sky", "tod": "dusk", "ground": g, "groundc": GROUND, "sun": [1500, 600, 26],
            "ridges": [{"y": 690, "a": 40, "c": "#2e2834", "seed": 9}, {"y": 730, "a": 16, "c": "#221c26", "seed": 4}], "cam": CAM, "els": els}


def s23_add():
    """Behind the warrior, a far larger figure glows faintly: the name everyone already knew."""
    te = T("s23", "Einstein")
    return [gl(1150, 330, 420, .2, .3, "glow")] + king(1150, 560, 400, .3, outline=LILAC, style="claimed", fx="fade", op=.7, w=3) + \
           [lab(1420, 470, "a byword", te + .6, LILAC, 32, st="ital"), gl(1420, 400, 120, te + .4, .45, "lamp")]


def XM(yr):
    return round(160 + (yr - 500) / 800 * 1460, 1)


def s24():
    """The poem's dates: the battle about 600, the only manuscript of the late 1200s, the Arthur line somewhere between."""
    tm, tl = T("s24", "one manuscript"), T("s24", "line may be")
    y = 600
    els = [axis(160, 1620, y, [(XM(v), str(v)) for v in (500, 700, 900, 1100)] + [(XM(1300), "1300 CE")], .1)]
    els += [dot(XM(600), y, 10, BONE, .4), lab(XM(600), y - 30, "the battle", .5, BONE, 26)]
    bx = XM(1265)
    els += book(bx - 30, y - 150, 56, 80, tm, "#6a3a24") + [lab(bx, y - 180, "the only manuscript", tm + .3, BONE, 28)]
    els += [{"k": "band", "x0": XM(600), "x1": XM(1000), "y": y - 120, "h": 18, "c": LILAC, "op": .55, "in": tl},
            rect(XM(600), y - 122, XM(1000) - XM(600), 22, "none", LILAC, 2, 11, tl, style="inferred"),
            lab(XM(800), y - 150, "the line: when?", tl + .3, LILAC, 30, st="ital")]
    els += qmark(XM(800), y - 210, tl + 1.2, 70)
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s25_add():
    """Gildas's book, closed and silent, at the start; a long dashed arrow to the line that may be centuries late."""
    ts, tl = T("s25", "silent"), T("s25", "centuries late")
    y = 600
    gx = XM(520)
    return book(gx - 26, y - 300, 52, 76, ts - .6, "#7a3a28") + [circ(gx + 2, y - 262, 8, "#b0301e", at=ts - .3, fx="pop"), lab(gx + 10, y - 330, "Gildas: silent", ts, BONE, 28),
                                                                 arr([(gx + 40, y - 270), (XM(700), y - 250)], tl - .6, DIM, 2.5, "inferred", 1.0, False)]


# ================================================================== CHAPTER 3 · Arthur appears
def s26():
    """Five crowned kings behind, and before them one uncrowned leader with a banner: 'leader of battles'; the crown he never had, struck."""
    tl, tn = T("s26", "leader of battles"), T("s26", "Not a")
    f = 720
    els = [ln([(80, f), (1700, f)], -1, "#4a3a28", 3, draw=False)]
    for k, x in enumerate((420, 600, 1180, 1360, 1540)):
        els += king(x, f - 50, 230, -1, "#3e3632", crown_c="#c8b07a", op=.75)
    els += [gl(889, f - 220, 380, .2, .45, "lamp")]
    els += [ln([(830, f - 10), (800, f - 560)], .3, "#8a6a48", 6, draw=False), poly([(800, f - 560), (650, f - 536), (664, f - 480), (802, f - 470)], "#8a2a24", "rgba(255,236,206,.45)", 1.5,
                                                                                   .4, fx="pop")]
    els += warrior(889, f, 420, .2, "#4a4038", face=1, shield=True)
    els += [lab(889, f + 56, "leader of battles", tl, GOLD, 34)]
    els += [crown(889, f - 470, 40, tn, LILAC, style="claimed", fill="rgba(201,193,238,.1)", w=2.5), strike(834, f - 446, 944, f - 536, tn + .5, RED, 6)]
    els += book(120, 150, 70, 100, -1, "#6a3a24") + chip(320, 186, "829", AMBER, -1, 28) + [lab(120, 300, "History of the Britons", -1, BONE, 26, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def battle_icon(x, y, kind, at, c=BONE):
    if kind == "river":
        return [ln([(x - 26 + 13 * k, y + 6 * (1 if k % 2 else -1)) for k in range(5)], at, c, 3, curve=True, draw=False),
                ln([(x - 26 + 13 * k, y + 14 + 6 * (1 if k % 2 else -1)) for k in range(5)], at, c, 3, curve=True, draw=False)]
    if kind == "forest":
        return tree(x - 12, y + 20, 44, at, "#7fa060") + tree(x + 14, y + 20, 38, at, "#6a8c50")
    if kind == "city":
        return [rect(x - 26, y - 10, 52, 28, c, at=at), rect(x - 30, y - 22, 12, 40, c, at=at), rect(x + 18, y - 22, 12, 40, c, at=at), rect(x - 6, y + 2, 12, 16, "#2a221c", at=at)]
    if kind == "fort":
        return [rect(x - 24, y - 6, 48, 24, c, at=at)] + [rect(x - 24 + 12 * k, y - 14, 6, 10, c, at=at) for k in range(5)]
    return [poly([(x - 30, y + 18), (x - 8, y - 14), (x + 8, y - 14), (x + 30, y + 18)], c, at=at)]


BATTLES = ["river", "river", "river", "river", "river", "river", "forest", "fort", "city", "river", "hill", "hill"]


def s27():
    """Twelve battles as twelve shields, each with the kind of place it names; rivers, the forest, the City of the Legion and Badon light as said."""
    tl = T("s27", "twelve battles")
    tr, tf, tc, tb = T("s27", "rivers"), T("s27", "forest"), T("s27", "City of the"), T("s27", "twelfth")
    els = [lab(889, 190, "twelve battles", tl, BONE, 34)]
    for k, kind in enumerate(BATTLES):
        x, y = 330 + 224 * (k % 6), 340 + 250 * (k // 6)
        at = tl + .1 * k
        gold = k == 11
        els += [circ(x, y, 78, "#3a2c20" if not gold else "#5a4422", AU if gold else "#a8916c", 3, at, fx="pop"), circ(x, y, 64, "none", "rgba(255,236,206,.25)", 1.5, at, fx="pop"),
                lab(x, y - 22, str(k + 1), at + .05, AU if gold else BONE, 30, st="serif", fx="pop")]
        els += battle_icon(x, y + 26, kind, at + .1, AU if gold else BONE)
    hl = {"river": tr, "forest": tf, "city": tc}
    for k, kind in enumerate(BATTLES):
        x, y = 330 + 224 * (k % 6), 340 + 250 * (k // 6)
        if kind in hl:
            els.append(gl(x, y, 110, hl[kind] + .05 * k, .35, "lamp"))
    els += [gl(330 + 224 * 5, 590, 170, tb, .6, "lamp"), lab(330 + 224 * 5, 720, "Mount Badon", tb + .2, AU, 30)]
    els += [lab(889, 780, "most places unknown", tb + 1.0, DIM, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s28():
    """One charge, 960 men: a lilac warrior and a block of 960 small marks filling in, row by row."""
    tf, t9 = T("s28", "nine hundred and sixty men"), T("s28", "Nine hundred and sixty", k=2)
    els = warrior(300, 700, 280, .3, "rgba(201,193,238,.25)", face=1)
    els += [poly([(300 - 40, 700 - 225), (300 + 44, 700 - 225), (300 + 70, 700 - 30), (300 - 64, 700 - 30)], "rgba(201,193,238,.15)", LILAC, 2, .3, style="claimed")]
    x0, y0, p = 760, 300, 20
    for r in range(24):
        els.append({"k": "group", "in": round(tf + .07 * r, 2), "fx": "pop", "els": [dot(x0 + p * c, y0 + p * r, 6, BONE, -1, None, op=.8) for c in range(40)]})
    els += [arr([(420, 520), (560, 470), (740, 470)], tf - .2, LILAC, 3.5, "claimed", .8), lab(560, 440, "one charge", tf + .4, LILAC, 30, st="ital"),
            lab(x0 + 20 * 19.5, 240, "960", t9 - .2, BONE, 80, st="num", fx="pop")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s29():
    """Badon to 829: about 300 years, ten generations passing a story hand to hand; the closest witness under a lens."""
    tg, tw = T("s29", "ten generations"), T("s29", "closest witness")
    y = 640
    els = [ln([(160, y), (1620, y)], .1, "#8c7152", 3, draw=False), dot(200, y, 12, AU, .2), lab(240, y + 56, "Badon, about 500", .3, AU, 28, "start"),
           dot(1580, y, 12, BONE, .4), lab(1580, y + 56, "829", .5, BONE, 28)]
    els += book(1544, y - 120, 64, 88, .5, "#6a3a24")
    els += bracket(200, 1580, 200, .8, "about 300 years", BONE, up=False, size=30)
    xs = [320 + 118 * k for k in range(10)]
    for k, x in enumerate(xs):
        old = k % 2 == 0
        h = 156 if old else 120
        els += [figure(x, y - 4, h, tg - .4 + .1 * k, "#cbbca8" if old else "#e8d6b8", "rise")]
        if old:
            els.append(ln([(x + 26, y - 4), (x + 30, y - h * .55)], tg - .3 + .1 * k, "#8a6a48", 3, draw=False))
    tb = tg + 1.2
    shades = ["#fff1c8", "#ffe2a8", "#ffd590", "#f9c880", "#f2bc78", "#e8b070", "#e0a468", "#d89860", "#d08c58", "#c88050"]
    for k, x in enumerate(xs):
        h = 156 if k % 2 == 0 else 120
        els += [gl(x + 40, y - h * .55, 46, tb + .45 * k, .8, "lamp"), dot(x + 40, y - h * .55, 9, shades[k], round(tb + .45 * k, 2))]
    els += monk(200, y - 6, 100, tw - .4)
    els += [circ(200, y - 60, 76, "none", GOLD, 4, tw, fx="draw"), ln([(146, y - 114), (110, y - 150)], tw, GOLD, 7, draw=False),
            lab(240, y - 170, "closest witness", tw + .3, GOLD, 28, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s30():
    """The wonders: Cabal's paw print on a stone of a cairn; the grave of Arthur's son, which measures 6, 9, 12 or 15 feet."""
    tc, tg, tf = T("s30", "paw print"), T("s30", "grave of Arthur's"), T("s30", "folklore")
    t6, t9, t12, t15 = T("s30", "six feet"), T("s30", "nine"), T("s30", "twelve"), T("s30", "fifteen")
    els = []
    rnd = random.Random(5)
    row = [0] * 8 + [1] * 7 + [2] * 6 + [3] * 4 + [4]
    for k in range(26):
        r = row[k]
        n = [8, 7, 6, 4, 1][r]
        j = k - sum([8, 7, 6, 4][:r])
        x = 420 + (j - (n - 1) / 2) * 62 + rnd.uniform(-6, 6)
        y = 700 - 44 * r - 26
        els.append(poly(E(x, y, 34, 24, 12), "#7a7068", "rgba(255,236,206,.35)", 1.2, -1))
    els += [poly(E(420, 470, 70, 34, 18), "#8a8078", "rgba(255,236,206,.5)", 1.5, -1)]
    els += paw(420, 470, 46, tc, GOLD) + [gl(420, 470, 120, tc, .5, "lamp"), lab(420, 380, "Cabal's paw print", tc + .3, GOLD, 30)]
    gx0, gy = 940, 700
    els += [poly([(gx0, gy), (gx0 + 40, gy - 50), (gx0 + 360, gy - 56), (gx0 + 400, gy)], "#4a5a34", "rgba(255,236,206,.3)", 1.5, -1, curve=True)]
    els += [lab(gx0 + 200, gy + 50, "grave of Arthur's son", tg, BONE, 28)]
    for k, (ft, at) in enumerate(((6, t6), (9, t9), (12, t12), (15, t15))):
        x1 = gx0 + 40 * ft
        yy = gy - 120 - 52 * k
        els += [ln([(gx0, yy), (x1, yy)], at - .2, AMBER, 4, dur=.4), ln([(gx0, yy - 12), (gx0, yy + 12)], at - .2, AMBER, 3, draw=False),
                ln([(x1, yy - 12), (x1, yy + 12)], at, AMBER, 3, draw=False), lab(x1 + 14, yy + 9, "%d ft" % ft, at, AMBER, 26, "start")]
    els += [gl(889, 420, 700, tf - .2, .22, "glow"), lab(889, 220, "folklore", tf, LILAC, 40, st="ital")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s31():
    """A page of the Welsh Annals: a column of years, most lines empty; Badon and Camlann light up."""
    tb, tc = T("s31", "battle of Badon"), T("s31", "strife of")
    x0, y0, w, h = 560, 140, 660, 650
    els = [rect(x0 + 10, y0 + 14, w, h, "#000", at=-1, op=.4), rect(x0, y0, w, h, PARCH, PARCH_E, 2, 4, -1)]
    rnd = random.Random(2)
    for k in range(17):
        y = y0 + 50 + 35 * k
        els.append(lab(x0 + 50, y, "an", -1, "rgba(74,58,40,.85)", 24, st="ital", halo=False))
        if rnd.random() < .3 and k not in (5, 11):
            els.append(ln([(x0 + 100, y - 8), (x0 + 100 + rnd.uniform(80, 300), y - 8)], -1, "rgba(74,58,40,.55)", 4, draw=False))
    yb, yc = y0 + 50 + 35 * 5, y0 + 50 + 35 * 11
    els += [rect(x0 + 90, yb - 30, 440, 40, "rgba(232,195,90,.3)", AU, 2, 6, tb - .2, fx="pop"), lab(x0 + 104, yb, "about 516: Badon", tb, "#5a3c10", 28, "start", halo=False),
            rect(x0 + 90, yc - 30, 470, 40, "rgba(255,138,122,.25)", RED, 2, 6, tc - .2, fx="pop"), lab(x0 + 104, yc, "about 537: Camlann", tc, "#7a2018", 28, "start", halo=False)]
    els += swords(x0 + w + 70, yc - 10, 26, tc + .3, RED)
    els += [lab(x0 - 30, y0 + 60, "Welsh Annals", .4, GOLD, 32, "end"), lab(x0 + w + 120, yc + 8, "Arthur and Medraut fell", tc + .6, BONE, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def XA(yr):
    return round(160 + (yr - 500) / 600 * 1460, 1)


def s32():
    """The annals' distance: 516 and 537 at one end, the compilation of about 950 to 970 more than four centuries later, the oldest copy about 1100."""
    tp, tl = T("s32", "put together"), T("s32", "added as late")
    y = 600
    els = [axis(160, 1620, y, [(XA(v), str(v)) for v in (500, 700, 900)] + [(XA(1100), "1100 CE")], .1),
           dot(XA(516), y, 10, AU, .2), dot(XA(537), y, 10, RED, .3), lab(XA(526), y - 34, "Badon, Camlann", .4, BONE, 26)]
    els += [{"k": "band", "x0": XA(950), "x1": XA(970), "y": y - 70, "h": 18, "c": AMBER, "t": "compiled", "tc": AMBER, "in": tp}]
    els += bracket(XA(516), XA(950), y - 180, tp + .5, "over 400 years", BONE, up=False, size=30)
    els += [gl(XA(970), y + 70, 90, tl, .5, "lamp"), lab(XA(970), y + 110, "added as late as 970?", tl + .2, LILAC, 26, st="ital"),
            ln([(XA(970), y - 50), (XA(970), y + 80)], tl, LILAC, 1.5, "inferred", dur=.4)]
    els += book(XA(1100) - 30, y - 120, 52, 76, tp + 1.5, "#6a3a24") + [lab(XA(1100), y - 140, "oldest copy", tp + 1.7, DIM, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s33():
    """The further from Badon, the more we learn: Gildas says nothing, the History twelve battles, the Annals dates, Geoffrey a whole reign."""
    tf = T("s33", "further we get")
    tm = T("s33", "the more we learn")
    x0, x1, y = 260, 1560, 690
    X = lambda yrs: round(x0 + yrs / 700 * (x1 - x0), 1)
    els = [ln([(x0, y), (x1 + 40, y)], .1, "#e9dccb", 2.5, draw=False), ln([(x0, y), (x0, 160)], .1, "#e9dccb", 2.5, draw=False),
           lab(x0, y + 90, "years after Badon", .2, AMBER, 24, "start", st="cap"), lab(x0 + 16, 170, "what we learn", .2, AMBER, 24, "start", st="cap")]
    src = [(40, "Gildas", 0, "nothing", DIM), (330, "829", 120, "12 battles", BONE), (450, "900s", 170, "2 dates", BONE), (636, "1136", 500, "a whole reign", LILAC)]
    for k, (yrs, name, hgt, what, c) in enumerate(src):
        x = X(yrs)
        at = tf + .5 * k if k < 3 else tm
        els.append(lab(x, y + 40, name, .3 + .1 * k, BONE, 26))
        if hgt:
            els.append(rect(x - 46, y - hgt, 92, hgt, c if k < 3 else "rgba(201,193,238,.45)", "rgba(255,236,206,.45)", 1.5, 4, at, fx="fill", dur=.6 if k < 3 else 1.4))
            if k < 3:
                els.append(lab(x, y - hgt - 16, what, at + .4, c, 28))
            else:
                els += [lab(x - 66, y - hgt + 40, what, at + 1.0, c, 30, "end", st="ital"), arr([(x, y - hgt - 6), (x, y - hgt - 56)], at + 1.2, LILAC, 4, dur=.4, curve=False)]
        else:
            els += [ln([(x - 46, y - 4), (x + 46, y - 4)], at, DIM, 3, "inferred", dur=.4), lab(x, y - 30, what, at + .3, DIM, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 4 · The making of a king
def s34():
    """Geoffrey at his writing desk with his finished book; beside it, the 'very ancient book' as a dotted outline that never fills in."""
    tv, tn = T("s34", "very ancient"), T("s34", "No modern")
    f = 730
    els = [ln([(80, f), (1000, f)], -1, "#4a3a28", 3, draw=False)]
    els += writing_desk(690, 470, 300, -1, 250) + candle(820, 452, -1, 40, 200)
    els += [poly([(560, 516), (600, 490), (720, 466), (700, 496)], "#f3e8d0", PARCH_E, 1.2, -1)]
    els += seated_monk(470, f, 300, -1, c="#5a4a40")
    els += [lab(470, f + 50, "Geoffrey of Monmouth", .3, BONE, 30)] + chip(300, 200, "about 1136", AMBER, .3, 28)
    els += book(1150, 270, 200, 270, tv, "rgba(201,193,238,.05)", LILAC, fx="fade", style="claimed", fill="rgba(201,193,238,.04)", pages=False)
    els += [lab(1270, 610, "a very ancient book?", tv + .4, LILAC, 30, st="ital")] + qmark(1255, 460, tn - .3, 100)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


VG = View(-13.0, 15.0, 48.0, 60.5, (90, 120, 1600, 680))


def s35():
    """Geoffrey's story on a map, all in the legend's dotted lilac: a crown over Britain, Tintagel, conquests over the sea, Camlann, a boat to Avalon."""
    v = VG
    tk, tt, tc, ta = T("s35", "His Arthur"), T("s35", "Tintagel"), T("s35", "conquers"), T("s35", "Avalon")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    bx, by = v.p(-1.5, 52.8)
    els += [gl(bx, by - 40, 240, tk, .55, "glow"), crown(bx, by - 30, 62, tk, LILAC, style="claimed", fill="rgba(201,193,238,.35)", w=3.5)]
    tx, ty = v.p(-4.76, 50.67)
    els += [star(tx, ty, 22, tt), gl(tx, ty, 80, tt, .6, "glow"), lab(tx - 30, ty + 8, "Tintagel", tt + .2, LILAC, 30, "end")]
    for k, (lo, la) in enumerate(((9.0, 60.4), (10.0, 56.2), (2.4, 48.8), (-8.0, 53.3))):
        p1 = v.p(lo, la)
        els.append(arr([(bx, by), ((bx + p1[0]) / 2, (by + p1[1]) / 2 - 40), p1], tc + .3 * k, LILAC, 4, "claimed", 1.0))
    els += [lab(*v.p(12.8, 58.3), "northern Europe", tc + 1.0, LILAC, 32, st="ital")]
    ax, ay = v.p(-9.6, 49.6)
    els += [ln([(tx - 10, ty + 20), ((tx + ax) / 2, ty + 80), (ax + 40, ay)], ta - .6, LILAC, 3, "claimed", 1.0, True),
            {"k": "boat", "x": round(ax + 60, 1), "y": round(ay - 4, 1), "w": 80, "in": ta - .2, "fx": "rise"},
            gl(ax, ay, 140, ta, .45, "glow"), lab(ax, ay + 66, "Avalon", ta + .2, LILAC, 32, st="ital")]
    return {"base": "map", "cam": CAM, "els": els}


def s36():
    """A library wall of 215 manuscripts filling in."""
    t2 = T("s36", "two hundred and fifteen")
    cols = ["#7a3a28", "#5a4a2a", "#3a4a3a", "#2e3a4e", "#6a4a2c", "#4a2a2a", "#7a5a3a"]
    els = [rect(560, 140, 960, 660, "#1a140f", "rgba(255,236,206,.2)", 1.5, 8, -1)]
    rnd = random.Random(6)
    for k in range(215):
        r, c = k // 20, k % 20
        x, y = 590 + 46 * c, 160 + 58 * r
        els.append(rect(x, y, 36, 50, cols[rnd.randrange(len(cols))], "rgba(255,226,190,.35)", 1, 2, round(t2 - .3 + .012 * k, 3), fx="pop"))
    els += [lab(330, 470, "215", t2 + .5, GOLD, 110, st="big"), lab(330, 540, "medieval manuscripts", t2 + .8, BONE, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s37():
    """The poem's Camelot: slender towers on a hill in dotted lilac, Lancelot before it, the poet at left."""
    tc, tl, tn = T("s37", "French poet"), T("s37", "Lancelot"), T("s37", "Camelot")
    g = 720
    hill = [(820, g)] + [(1230 + 410 * math.cos(math.radians(a)), g - 170 * math.sin(math.radians(a)) ** .8) for a in range(180, -1, -10)] + [(1640, g)]
    els = [poly(hill[::-1], "#26222c", "rgba(201,193,238,.3)", 1.5, -1)]
    for k, (x, h) in enumerate(((1000, 230), (1100, 300), (1210, 360), (1320, 290), (1420, 220))):
        top = 550 - h
        els += [rect(x - 26, top, 52, 570 - top, "rgba(201,193,238,.10)", LILAC, 2.5, 2, tc + .2 + .15 * k, style="claimed"),
                poly([(x - 34, top), (x, top - 70), (x + 34, top)], "rgba(201,193,238,.14)", LILAC, 2.5, tc + .3 + .15 * k, style="claimed")]
    els += [rect(980, 480, 470, 90, "rgba(201,193,238,.08)", LILAC, 2.5, 2, tc + .2, style="claimed"), gl(1210, 400, 380, tc, .35, "glow")]
    els += knight(660, g, 240, tl - .3)
    els += [lab(660, g + 50, "Lancelot", tl + .3, LILAC, 30)]
    els += [figure(300, g, 170, .3, "#cbbca8", "rise")] + open_book(366, g - 130, 90, 48, .5, rows=0) + [

            lab(300, g + 50, "Chrétien de Troyes", .5, BONE, 28)] + chip(300, 330, "1170s", AMBER, tc, 28)
    els += [lab(1210, 200, "Camelot", tn, LILAC, 52, st="serif")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


def s38():
    """The sceptic: William of Newburgh at his desk; red question marks rise over Geoffrey's book."""
    tw, td = T("s38", "William of Newburgh"), T("s38", "shamelessly")
    f = 730
    els = [ln([(80, f), (900, f)], -1, "#4a3a28", 3, draw=False)]
    els += writing_desk(470, 470, 280, -1, 250) + candle(360, 486, -1, 40, 200)
    els += seated_monk(690, f, 300, -1, face=-1, c="#2a2a30")
    els += [lab(690, f + 50, "William of Newburgh", tw, BONE, 30)] + chip(560, 220, "1190s", AMBER, tw + .3, 28)
    els += open_book(1250, 260, 560, 360, -1, rows=9) + [lab(1250, 230, "Geoffrey's History", .4, DIM, 26)]
    for k, (x, y) in enumerate(((1060, 350), (1180, 470), (1310, 330), (1420, 470), (1250, 560))):
        els.append(lab(x, y, "?", td - .6 + .25 * k, RED, 60, st="serif", fx="pop"))
    els.append(ln([(990, 650), (1520, 650)], td + .4, RED, 4, dur=.6))
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s39():
    """Glastonbury, 1184: the abbey burns (left); then the rebuilding, scaffolding round new walls, and pilgrims walking towards it with coins (right)."""
    tf, tr, tp = T("s39", "fire destroyed"), T("s39", "Rebuilding"), T("s39", "pilgrims")
    g = 700
    els = [gl(450, 460, 520, tf - .4, .3, "fire")] + church(130, g, 640, 280, -1, "#221a16", op=1, edge="rgba(255,180,120,.55)")
    for k, x in enumerate((180, 300, 420, 540, 660, 740)):
        top = g - (280 if x < 260 else 210 if x < 700 else 160) - 10 * math.sin(k * 1.7)
        els += flame(x, top + 34, 80 + 18 * math.sin(k), tf - .5 + .12 * k)
        els.append(gl(x, top, 150, tf - .5 + .12 * k, .75, "fire", pulse=True))
    els += chip(450, 240, "1184", RED, tf - .3, 30)
    els += [arr([(820, 420), (930, 420)], tr - .4, BONE, 4, dur=.5, curve=False)]
    x0, w = 980, 540
    els += [rect(x0, g - 150, w, 150, "#6a5a48", "rgba(255,236,206,.5)", 1.5, 2, tr, fx="fill", dur=1.0),
            rect(x0 + 40, g - 230, 120, 80, "#6a5a48", "rgba(255,236,206,.5)", 1.5, 2, tr + .4, fx="fill", dur=.6)]
    for k in range(5):
        x = x0 - 10 + 140 * k
        els.append(ln([(x, g), (x, g - 300)], tr + .5 + .1 * k, "#c9a46a", 4, dur=.4))
    for k in range(2):
        els.append(ln([(x0 - 20, g - 120 - 130 * k), (x0 + w + 20, g - 120 - 130 * k)], tr + 1.1 + .1 * k, "#c9a46a", 3, dur=.6))
    els += [lab(x0 + w / 2, g - 330, "rebuilding", tr + .9, BONE, 28)]
    for k in range(5):
        x = 1580 - 10 + 34 * (k % 3) - 60 * (k // 3)
        x = 1560 + 30 * k
        els += [figure(x, g, 92, tp - .4 + .2 * k, "#cbbca8", "rise"), ln([(x + 16, g), (x + 20, g - 100)], tp - .3 + .2 * k, "#8a6a48", 3, draw=False),
                circ(x, g - 140, 8, AU, "#7a5a1a", 1, tp + .4 + .15 * k, fx="pop"), gl(x, g - 140, 24, tp + .4 + .15 * k, .5, "lamp")]
    els += [lab(1620, g + 50, "pilgrims", tp + .6, BONE, 28)]
    return {"base": "sky", "tod": "night", "ground": g, "groundc": GROUND, "sun": False,
            "ridges": [{"y": 650, "a": 30, "c": "#1f1a26", "seed": 3}, {"y": 690, "a": 14, "c": "#18141e", "seed": 6}], "cam": CAM, "els": els}


def s40_add():
    """Back in the grave: 1191, and the cross glows brighter."""
    tm = T("s40", "find")
    return chip(600, 520, "1191", AMBER, .4, 32) + [gl(890, G2 + 205, 140, tm, .7, "lamp")]


def s41_add():
    """REX and AVALONIA glow lilac, tied by dotted threads to Geoffrey's book of about 1136; the 500s' 'leader of battles' sits apart."""
    tk, tg, t5 = T("s41", "calls him"), T("s41", "Geoffrey's story"), T("s41", "not of the")
    rows = CROSS_ROWS(CX1, TOP1)
    bx, by = 1560, 150
    els = [rect(CX1 - 180, rows["rex"] - 40, 360, 54, "rgba(201,193,238,.2)", LILAC, 3, 8, tk, fx="pop"),
           rect(CX1 - 118, rows["aval"] - 34, 236, 46, "rgba(201,193,238,.2)", LILAC, 3, 8, tk + .5, fx="pop")]
    els += book(bx, by, 80, 110, tg - .4, "#6a3a24") + [lab(bx + 46, by + 150, "Geoffrey, 1136", tg - .2, LILAC, 26)]
    els += [ln([(CX1 + 182, rows["rex"] - 30), (1450, 260), (bx - 6, by + 60)], tg - .2, LILAC, 3, "claimed", .9, True),
            ln([(CX1 + 120, rows["aval"] - 20), (1420, 560), (bx + 30, by + 116)], tg, LILAC, 3, "claimed", .9, True)]
    els += tagc(1460, 740, "the 500s: leader of battles", t5, DIM, 24, "inferred")
    return els


VW = View(-5.6, -0.6, 50.7, 53.6, (90, 120, 1600, 680))


def s42():
    """Wales and the west of England: the hope of Arthur's return glowing over Wales; England's kings; a dashed arrow from the grave: he is dead."""
    v = VW
    tk, td = T("s42", "England's kings"), T("s42", "was dead")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    wx, wy = v.p(-3.7, 52.3)
    els += [gl(wx, wy, 260, .3, .45, "glow")] + king(wx, wy + 60, 150, .5, outline=LILAC, style="claimed", fx="fade", w=3, fill="rgba(201,193,238,.18)")
    els += [lab(wx, wy + 110, "his return?", .8, LILAC, 30, st="ital"), lab(*v.p(-3.9, 52.95), "Wales", .4, DIM, 30)]
    ex, ey = v.p(-1.5, 52.3)
    els += [crown(ex, ey, 44, tk, AU, fill="#5a4a2a", w=2.5), gl(ex, ey - 30, 120, tk, .45, "lamp"), lab(ex, ey + 50, "England's kings", tk + .3, AU, 30)]
    gx, gy = v.p(-2.72, 51.15)
    els += [dot(gx, gy, 9, BONE, .3), lab(gx + 18, gy + 34, "Glastonbury", .4, BONE, 26, "start")]
    els += [arr([(gx - 10, gy - 14), ((gx + wx) / 2 + 40, (gy + wy) / 2 + 20), (wx + 120, wy + 70)], td - .4, AMBER, 3.5, "inferred", 1.0),
            lab((gx + wx) / 2 + 150, (gy + wy) / 2 + 60, "he is dead", td + .4, AMBER, 30, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def s43():
    """1278: a black marble tomb before the altar, a king and queen watching; then the tomb fades to a dashed outline: lost; 'publicity stunt?'."""
    t78, tl, tp = T("s43", "twelve seventy-eight"), T("s43", "were lost"), T("s43", "publicity")
    f = 720
    els = [ln([(80, f), (1700, f)], -1, "#4a3a28", 3, draw=False), gl(1250, 380, 420, -1, .3, "lamp")]
    els += [rect(1140, 470, 260, 250, "#3a2e24", "rgba(255,236,206,.35)", 1.5, 3, -1), rect(1120, 452, 300, 22, "#e8dcc2", "rgba(255,236,206,.5)", 1.5, 2, -1),
            rect(1150, 474, 240, 90, "#7a2a24", at=-1, op=.85)] + candle(1180, 452, -1) + candle(1360, 452, -1)
    els += [{"k": "lib", "k2": "box3d", "x": 700, "y": f, "w": 340, "h": 140, "d": 120, "tone": "#1d1b1e", "light": "#3e3c44", "in": .3}]
    els += king(380, f, 260, t78 - .2, "#5a4e46", crown_c=AU) + king(540, f, 236, t78, "#5a4660", crown_c=AU)
    els += chip(460, 330, "1278", AMBER, t78, 30)
    els += [veil(690, 560, 450, 170, tl - .3, "#120e0b", op=.94, dur=1.2),
            rect(700, f - 140, 340, 140, "none", BONE, 2.5, 2, tl, style="inferred"), lab(870, f + 50, "lost", tl + .3, BONE, 30)]
    els += tagc(870, 470, "publicity stunt?", tp, RED, 30, "inferred")
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


def s44():
    """1184 to 1191: the fire, and seven years later, the find."""
    tf = T("s44", "found")
    X = lambda yr: round(300 + (yr - 1180) / 15 * 1180, 1)
    y = 560
    els = [axis(300, 1480, y, [(X(v), str(v)) for v in (1180, 1185, 1190, 1195)], .1)]
    els += flame(X(1184), y - 30, 80, .3) + [lab(X(1184), y - 150, "fire", .5, FIRE, 32)]
    els += lead_cross(X(1191), y - 160, tf - .4, s=.2, letters=False) + [gl(X(1191), y - 100, 100, tf - .4, .5, "lamp"), lab(X(1191), y - 190, "Arthur found", tf, AMBER, 32)]
    els += bracket(X(1184), X(1191), y + 120, tf + .4, "7 years", BONE, up=True, size=30)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================== CHAPTER 5 · Digging for Camelot
def cadbury_hill(at=-1, x0=420, x1=1560, base=720, top=420):
    """Cadbury Castle in side view: a broad hill with a flat top, its flanks stepped by four grassy ramparts (a steep bank, a ditch, a bench), trees below."""
    w, H = x1 - x0, base - top
    xs = [.0, .07, .085, .14, .155, .21, .225, .28, .3]          # left flank, foot to shoulder: bank faces and benches (fractions of the width)
    ys = [0, .22, .2, .45, .43, .68, .66, .92, 1.0]               # heights (fractions of H)
    left = [(x0 + w * a, base - H * b) for a, b in zip(xs, ys)]
    right = [(x1 - w * a, base - H * b) for a, b in zip(xs, ys)][::-1]
    pts = left + right
    out = [poly(pts, "#4f6838", "rgba(220,240,190,.45)", 2, at)]
    for (a, b), (a2, b2) in zip(zip(xs[1::2], ys[1::2]), zip(xs[2::2], ys[2::2])):
        for side in (-1, 1):
            xa = x0 + w * a if side < 0 else x1 - w * a
            xb = x0 + w * a2 if side < 0 else x1 - w * a2
            out.append(ln([(xa, base - H * b), (xb, base - H * b2)], at, "rgba(230,245,200,.6)", 3, draw=False))
            out.append(poly([(xa, base - H * b), (xb, base - H * b2), (xb, base - H * b2 + 14), (xa, base - H * b + 14)], "rgba(20,30,12,.28)", at=at))
    rnd = random.Random(14)
    for k in range(12):
        side = -1 if k % 2 else 1
        u = rnd.uniform(.0, .06)
        x = x0 + w * u if side < 0 else x1 - w * u
        out += tree(x + side * -rnd.uniform(0, 30), base + 4, rnd.uniform(40, 64), at, "#2c3a22")
    return out


def s45():
    """Somerset by day: Cadbury Castle, a broad flat-topped hill ringed by ramparts; John Leland with his notebook, 1542; 'Camelot?'."""
    tl, tc = T("s45", "John Leland"), T("s45", "Camelot")
    g = 720
    els = cadbury_hill()
    els += church(1580, g, 150, 90, -1, "#3a3430", op=.9)
    els += [figure(250, g, 160, .3, "#3a3430", "rise"), rect(276, g - 120, 36, 46, PARCH, PARCH_E, 1.2, 2, .5, fx="pop"),
            lab(250, g + 46, "John Leland", tl, BONE, 30)] + chip(250, 470, "1542", AMBER, tl + .3, 28)
    els += [lab(990, 380, "Cadbury Castle", .6, BONE, 34), lab(990, 270, "Camelot?", tc, LILAC, 44, st="ital")]
    return {"base": "sky", "tod": "day", "ground": g, "groundc": "#4a5a34", "sun": [330, 200, 30],
            "ridges": [{"y": 690, "a": 40, "c": "#5a6a7a", "seed": 3}, {"y": 716, "a": 14, "c": "#4a5a50", "seed": 9}], "cam": CAM, "els": els}


RINGS = [(560, 300), (500, 262), (440, 224), (380, 186)]      # rx, ry of the four banks on the plan; the innermost is the 1.2 km bank


def _perim(a, b):
    return math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))


def s46():
    """The hillfort in plan: four banks; Alcock's trenches; the innermost bank, rebuilt from about 470, more than a kilometre round."""
    ta, tr = T("s46", "Leslie Alcock"), T("s46", "rebuilt its old")
    cx, cy = 820, 470
    els = []
    for k, (a, b) in enumerate(RINGS):
        els.append(poly(E(cx, cy, a, b, 60), "rgba(110,140,80,.10)" if k == 3 else "none", "#8aa060" if k < 3 else "#a8bf78", 6 - k * .6, -1, curve=True, op=.75 - .1 * (3 - k)))
    for k, (x, y, w, h) in enumerate(((330, 440, 260, 26), (900, 230, 24, 180), (1090, 520, 220, 24), (700, 610, 24, 150), (820, 420, 120, 60))):
        els.append(rect(x, y, w, h, "#2a2019", "rgba(255,236,206,.5)", 1.5, 2, ta + .2 + .2 * k, fx="pop"))
    els += [lab(330, 200, "Alcock, 1966 to 1970", ta + .4, BONE, 30)]
    a, b = RINGS[3]
    els += [poly(E(cx, cy, a, b, 72), "none", GOLD, 6, tr, curve=True, fx="draw", dur=2.0), gl(cx, cy, 420, tr + 1.0, .25, "lamp")]
    els += [lab(1420, 300, "rebuilt from", tr + .6, GOLD, 30), lab(1420, 340, "about 470", tr + .7, GOLD, 30),
            lab(1420, 640, "1.2 km around", tr + 1.6, GOLD, 30)]
    unit = _perim(a, b) / 12                                   # 100 m on the plan
    els += [{"k": "scale", "x": 1340, "y": 740, "w": round(unit, 1), "t": "100 m", "in": .6}]
    return {"base": "plan", "cam": CAM, "els": els}


def hall_items():
    """The great hall as a toy model: 20 x 10 m, posts, low walls, a thatched roof (iso units: 1 = 1 m)."""
    items = [{"t": "slab", "x0": -16, "x1": 16, "z0": -10, "z1": 10, "y": 0, "c": "#4a5a30"},
             {"t": "box", "x": 0, "z": 0, "y": 0, "w": 20, "d": 10, "h": 2.6, "c": "#8a6a44", "edge": "rgba(0,0,0,.35)"},
             {"t": "ext", "axis": "z", "at": 0, "d": 20.6, "z": 0, "y": 2.6, "prof": [[-5.6, 0], [5.6, 0], [0, 4.6]], "c": "#b89a5a", "edge": "rgba(0,0,0,.3)"},
             {"t": "box", "x": 0, "z": 5.05, "y": 0, "w": 1.6, "d": .2, "h": 2.0, "c": "#2a1d12"},
             {"t": "person", "x": 2.2, "y": 0, "z": 6.2, "h": 1.7, "color": "#e8d6b8"}]
    for k in range(6):
        items.append({"t": "cyl", "x": -9 + 3.6 * k, "z": 5.3, "y": 0, "r": .22, "h": 2.6, "c": "#6a4a2c", "n": 8})
    items.append({"t": "line", "p": [[-10, 0, 6.6], [10, 0, 6.6]], "c": GOLD, "w": 3})
    items.append({"t": "label", "x": 0, "y": 0, "z": 7.4, "text": "20 m", "c": GOLD, "dy": 40})
    return items


def s47():
    """The great timber hall, 20 m long, turning slowly; a person at its door; sherds of eastern Mediterranean jars."""
    th, tp = T("s47", "great timber hall"), T("s47", "pottery")
    els = [gl(760, 520, 520, .1, .22, "lamp"),
           {"k": "iso", "x": 760, "y": 560, "s": 26, "az": -28, "spin": 1.6, "el": .38, "items": hall_items(), "in": .2},
           lab(760, 190, "the great hall", th, GOLD, 36)]
    for k, (x, y, rot) in enumerate(((1360, 420, -12), (1500, 520, 18), (1390, 600, 8))):
        sh = [poly([(-46, -20), (40, -30), (52, 10), (-30, 26)], "#c98a5a", "rgba(255,236,206,.55)", 1.5, -1),
              ln([(-30, -6), (34, -14)], -1, "rgba(80,40,20,.5)", 2, draw=False), ln([(-26, 8), (40, 0)], -1, "rgba(80,40,20,.5)", 2, draw=False)]
        els.append(grp(sh, tp + .2 * k, "pop", tr="translate(%d %d) rotate(%d)" % (x, y, rot)))
    els += [lab(1440, 700, "eastern Mediterranean", tp + .7, AMBER, 28), lab(1440, 736, "pottery", tp + .8, AMBER, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s48_add():
    """The hill again: the largest of its age; the dig billed as 'Cadbury-Camelot'; Alcock's book of 1971; then a millstone."""
    tl, tb, t71, tm = T("s48", "largest"), T("s48", "billed"), T("s48", "nineteen seventy-one"), T("s48", "millstone")
    els = [gl(990, 440, 560, tl, .35, "lamp"), ln([(760, 426), (990, 420), (1220, 426)], tl, GOLD, 5, curve=True, dur=1.0),
           lab(990, 560, "largest of its age", tl + .4, GOLD, 32)]
    els += [rect(1250, 150, 360, 96, "rgba(201,193,238,.12)", LILAC, 2.5, 6, tb - .2, fx="pop", style="claimed"),
            lab(1430, 210, "CADBURY-CAMELOT", tb, LILAC, 30, st="lab", weight=700)]
    els += book(1300, 470, 90, 120, t71 - .2, "#6a3a24") + [lab(1345, 630, "1971", t71, BONE, 28)]
    els += mill(1520, 540, 60, tm - .3) + [lab(1520, 640, "a millstone", tm + .2, BONE, 26)]
    return els


def s49():
    """Tintagel at dusk: the island headland with sheer cliffs and a green top seen a little from above, the neck to the mainland, the sea;
    about a hundred building footprints on the top."""
    tt, tb, t45 = T("s49", "Tintagel"), T("s49", "hundred buildings"), T("s49", "four fifty")
    sea = 640
    els = [{"k": "water", "y": sea, "h": 500, "op": .92, "in": -1}]
    # the mainland: cliffs on the left, grass on top
    els += [poly([(-40, sea + 20), (-40, 320), (180, 300), (360, 306), (470, 330), (520, 420), (548, sea + 20)], "#3a352d", "rgba(255,226,190,.35)", 1.5, -1),
            poly([(-40, 320), (180, 300), (360, 306), (470, 330), (454, 352), (300, 338), (-40, 350)], "#4f6838", at=-1)]
    els += [poly([(548, sea + 20), (580, 500), (640, 470), (700, 500), (728, sea + 20)], "#332e27", "rgba(255,226,190,.3)", 1.5, -1)]
    cliff = [(700, sea + 20), (722, 420), (760, 330), (980, 300), (1300, 304), (1500, 340), (1560, 420), (1580, sea + 20)]
    top = [(760, 330), (900, 250), (1300, 236), (1500, 300), (1500, 340), (1300, 304), (980, 300)]
    els += [poly(cliff, "#3e3a31", "rgba(255,226,190,.4)", 1.5, -1), poly(top, "#56703c", "rgba(220,240,190,.4)", 1.5, -1)]
    for k in range(8):
        x = 740 + 105 * k
        els.append(ln([(x, sea + 10), (x + 20, 330 + 8 * math.sin(k))], -1, "rgba(24,20,16,.4)", 2.5, draw=False))
    els += [ln([(700, sea + 8), (900, sea + 2), (1200, sea + 10), (1580, sea + 4)], -1, "rgba(235,245,250,.7)", 3, curve=True, draw=False),
            ln([(-40, sea + 10), (300, sea + 4), (548, sea + 12)], -1, "rgba(235,245,250,.6)", 3, curve=True, draw=False)]
    rnd = random.Random(21)
    k = 0
    def inside(x, y):
        # between the plateau's back edge (900,250)-(1300,236)-(1500,300) and its front edge (980,300)-(1300,304)-(1500,340)
        if x < 790 or x > 1490:
            return False
        if x < 900:
            yb = 330 - (x - 760) / 140 * 80
            yf = 330 - (x - 760) / 220 * 30 if x < 980 else 300
        elif x < 1300:
            yb = 250 - (x - 900) / 400 * 14
            yf = 300 + (x - 980) / 320 * 4 if x > 980 else 300
        else:
            yb = 236 + (x - 1300) / 200 * 64
            yf = 304 + (x - 1300) / 200 * 36
        return yb + 7 < y < yf - 6
    while k < 100:
        x, y = rnd.uniform(800, 1480), rnd.uniform(240, 336)
        if not inside(x, y):
            continue
        els.append(rect(x - 7, y - 3.5, 14, 7, "#e2d2a8", "rgba(40,30,20,.6)", .8, 1, round(tb - .4 + .025 * k, 3), fx="pop"))
        k += 1
    els += [lab(1130, 190, "Tintagel", tt, BONE, 42, st="serif")] + chip(1300, 520, "450 to 650", AMBER, t45, 28)
    els += [lab(1130, 420, "about 100 buildings", tb + 1.2, GOLD, 30)]
    return {"base": "sky", "tod": "dusk", "ground": 1100, "sun": [1640, 560, 24], "ridges": [{"y": 600, "a": 20, "c": "#2e2834", "seed": 5}, {"y": 630, "a": 8, "c": "#252030", "seed": 9}],
            "cam": CAM, "els": els}


VM = View(-12.0, 30.0, 34.0, 54.5, (90, 120, 1600, 680))


def s50():
    """The trade: a dotted ship route from the eastern Mediterranean to Cornwall; a storage jar, a red bowl and a glass beaker pop as named."""
    v = VM
    tj, tr, tg = T("s50", "storage jars"), T("s50", "red tableware"), T("s50", "glass")
    tm = T("s50", "Mediterranean pottery")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    route = [(27.0, 38.5), (24.0, 36.6), (20.0, 35.9), (15.5, 36.6), (11.5, 37.6), (5.0, 37.6), (-1.0, 36.6), (-5.6, 35.95), (-9.6, 37.3), (-10.0, 42.5), (-8.0, 44.6),
             (-5.5, 48.2), (-4.9, 50.4)]
    els += [ln([v.p(*q) for q in route], tm - .8, AMBER, 3.5, "claimed", 2.4, True), {"k": "boat", "x": v.p(-1.0, 36.6)[0], "y": v.p(-1.0, 36.6)[1] - 4, "w": 60, "in": tm, "fx": "rise"}]
    tx, ty = v.p(-4.76, 50.67)
    ex, ey = v.p(25.5, 37.3)
    els += [{"k": "pin", "x": tx, "y": ty, "t": "Tintagel", "c": GOLD, "a": "end", "lx": -20, "ly": 8, "in": .4},
            lab(ex, ey + 70, "eastern Mediterranean", tm - .4, "#9fd0ff", 28, st="ital")]
    bx0, by0 = 1190, 150
    els += [rect(bx0, by0, 440, 290, "rgba(18,13,10,.82)", "rgba(255,236,206,.35)", 1.5, 14, tj - .5, fx="pop")]
    els += amphora(bx0 + 90, by0 + 250, 200, tj) + bowl(bx0 + 230, by0 + 160, 120, tr) + beaker(bx0 + 360, by0 + 250, 110, tg)
    els += [lab(bx0 + 220, by0 + 330, "the most in Britain", tm + .4, GOLD, 30)]
    return {"base": "map", "cam": CAM, "els": els}


def slate(cx, cy, at, s=1.0):
    pts = [(-330, -150), (-80, -190), (120, -170), (330, -130), (310, 40), (340, 160), (60, 190), (-200, 170), (-340, 120), (-300, -20)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], "#3e4650", "rgba(220,226,232,.55)", 2, at)


def s51():
    """The Artognou slate of 1998 with its scratched letters; a headline 'ARTHUR STONE?' struck; ARTOGNOU glows: bear-knowing."""
    t98, th, ta, tb = T("s51", "nineteen ninety-eight"), T("s51", "Arthur stone"), T("s51", "Artognou"), T("s51", "bear-knowing")
    cx, cy = 720, 470
    els = [gl(cx, cy, 520, -1, .2, "lamp"), slate(cx, cy, -1)]
    sc = "rgba(232,236,240,.85)"
    els += [lab(cx - 110, cy - 90, "PATERN", -1, sc, 44, st="lab", halo=False, scl=True), lab(cx - 20, cy - 10, "COLI AVI FICIT", -1, sc, 44, st="lab", halo=False, scl=True),
            lab(cx - 20, cy + 70, "ARTOGNOU", -1, sc, 50, st="lab", halo=False, scl=True),
            lab(cx + 180, cy + 140, "COL  FICIT", -1, "rgba(232,236,240,.5)", 28, st="lab", halo=False, scl=True)]
    els += chip(260, 200, "1998", AMBER, t98, 30)
    nx, ny = 1250, 200
    els += [rect(nx, ny, 400, 300, "#e8e2d4", "#8a8070", 1.5, 3, th - .4, fx="pop"), rect(nx + 20, ny + 20, 360, 10, "#2a2622", at=th - .3, fx="pop"),
            lab(nx + 200, ny + 90, "ARTHUR STONE?", th - .2, "#1a1612", 38, st="lab", halo=False, weight=700, fx="pop"),
            {"k": "glyphs", "x": nx + 30, "y": ny + 120, "w": 340, "h": 150, "rows": 6, "cols": 7, "kind": "latin", "c": "rgba(40,36,30,.6)", "in": round(th, 2)},
            strike(nx + 10, ny + 110, nx + 390, ny + 60, ta - .2, RED, 7)]
    els += [rect(cx - 160, cy + 22, 280, 66, "rgba(232,195,90,.16)", AU, 2.5, 8, ta, fx="pop"), gl(cx - 20, cy + 54, 200, ta, .45, "lamp"),
            lab(cx - 20, cy + 250, "Artognou: bear-knowing", tb - .4, GOLD, 34)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s52():
    """The dig from 2016 in section: a stone wall a metre thick, a slate floor, slate steps, a digger for scale; a name slot that stays empty."""
    tw, tf, ts, tn = T("s52", "walls a metre"), T("s52", "slate floors"), T("s52", "steps"), T("s52", "None of them")
    g, m = 300, 110                                     # ground line; 110 units a metre
    floor = g + 380
    els = [poly([(200, g), (1560, g), (1520, floor + 30), (240, floor + 30)], "#2a2018", "rgba(255,226,190,.45)", 1.5, -1)]
    els += [ln([(210 + 6 * k, g + 40 + 60 * k), (1550 - 6 * k, g + 40 + 60 * k)], -1, "rgba(255,226,190,.07)", 2, "inferred", draw=False) for k in range(6)]
    els += [rect(560, floor - 300, m, 300, "url(#k-blocks)", "rgba(255,236,206,.55)", 1.5, 2, tw - .4, fx="fill", dur=.7)]
    els += [{"k": "dim", "x1": 560, "y1": floor - 330, "x2": 560 + m, "y2": floor - 330, "t": "1 m", "c": AMBER, "ly": -16, "dur": .5, "in": tw}]
    for k in range(9):
        els.append(rect(670 + 60 * k, floor - 10, 56, 10, "#5a6672", "rgba(220,226,232,.6)", 1, 1, tf - .2 + .06 * k, fx="pop"))
    for k in range(4):
        els.append(rect(1240 + 70 * k, floor - 40 * (k + 1), 260 - 70 * k, 40, "#5a6672", "rgba(220,226,232,.6)", 1, 1, ts - .2 + .15 * k, fx="pop"))
    els += [figure(900, floor - 10, 187, .4, "#cbbca8", "rise"), ln([(930, floor - 90), (968, floor - 60)], .6, "#9aa0a8", 4, draw=False)]
    els += chip(330, 200, "from 2016", AMBER, .3, 28)
    els += [rect(586, floor - 220, 58, 90, "rgba(201,193,238,.06)", LILAC, 2, 4, tn - .2, style="inferred"), lab(615, floor - 160, "?", tn, LILAC, 40, st="serif"),
            lab(615, floor - 250, "Arthur?", tn + .3, LILAC, 28, st="ital")]
    els += [lab(800, floor + 74, "slate floor", tf + .3, DIM, 26), lab(1380, floor - 200, "steps", ts + .4, DIM, 26)]
    layers = [{"d": 0, "c": "#4a3c2c", "t": ""}, {"d": 100, "c": "#3a2f24", "t": ""}, {"d": 260, "c": "#2e251c", "t": ""}]
    return {"base": "section", "tod": "dusk", "ground": g, "layers": layers, "cam": CAM, "els": els}


def s53_add():
    """Earl Richard's castle of the 1230s draws itself on the mainland and the island; a dotted arrow from Geoffrey's story."""
    tb, tw, tl = T("s53", "Built in"), T("s53", "share of the fame"), T("s53", "legend built")
    els = []
    wall = [(40, 304), (40, 232), (70, 232), (70, 252), (110, 252), (110, 228), (140, 228), (140, 252), (330, 252), (330, 216), (370, 216), (370, 304)]
    els += [poly(wall, "#8a7e6a", "rgba(255,236,206,.6)", 1.5, tb, fx="rise"), rect(210, 266, 40, 38, "#1a1410", at=tb + .1)]
    els += [poly([(860, 258), (860, 196), (900, 196), (900, 214), (1020, 214), (1020, 248)], "#8a7e6a", "rgba(255,236,206,.6)", 1.5, tb + .4, fx="rise")]
    els += chip(260, 470, "1230s", AMBER, tb + .2, 28)
    els += [lab(330, 168, "Earl Richard's castle", tb + .6, BONE, 30)]
    els += book(1530, 140, 64, 88, tw - .4, "#6a3a24") + [lab(1562, 270, "Geoffrey's story", tw - .2, LILAC, 26),
                                                           arr([(1520, 196), (1100, 130), (440, 200)], tw, LILAC, 3, "claimed", 1.2)]
    els += [gl(200, 262, 260, tl, .4, "lamp")]
    return els


# ================================================================== CHAPTER 6 · The weighing
VR = View(-7.8, 5.2, 45.4, 52.4, (90, 120, 1600, 680))


def s54():
    """Riothamus: twelve ships, a thousand men each, from Britain round to the Loire and inland to the Bituriges, about 470."""
    v = VR
    tr, tg, t12 = T("s54", "Riothamus"), T("s54", "Gaul"), T("s54", "twelve thousand")
    els = [{"k": "map", "land": v.land(), "in": -1}]
    route = [(-3.8, 50.2), (-4.8, 49.3), (-5.6, 48.3), (-4.4, 47.3), (-2.4, 47.15), (-0.5, 47.3), (1.0, 47.3), (2.4, 47.08)]
    pts = [v.p(*q) for q in route]
    els += [ln(pts, t12 - .4, AMBER, 3.5, "claimed", 2.4, True)]
    sea_pts = [v.p(*q) for q in [(-3.6, 50.0), (-4.3, 49.6), (-4.9, 49.15), (-5.4, 48.7), (-5.7, 48.2), (-5.3, 47.8), (-4.8, 47.5), (-4.2, 47.25), (-3.6, 47.05), (-3.0, 46.95),
                                 (-2.6, 47.0), (-4.6, 48.9)]]
    for k, (x, y) in enumerate(sea_pts):
        els += ship(x, y, 58, t12 + .12 * k, "#e8d6b8", face=1, oars=4, mast=True)
    bx, by = v.p(2.4, 47.08)
    els += [{"k": "pin", "x": bx, "y": by, "t": "Bituriges", "c": GOLD, "a": "start", "lx": 18, "ly": 8, "in": t12 + 1.4},
            lab(*v.p(-1.4, 51.65), "Riothamus", tr, GOLD, 44, st="serif"), lab(*v.p(1.8, 48.9), "Gaul", tg, DIM, 36, st="ital"),
            lab(*v.p(-5.4, 46.3), "12,000 men", t12 + .6, AMBER, 34)] + chip(300, 200, "about 470", AMBER, tg + .4, 28)
    return {"base": "map", "cam": CAM, "els": els}


def XC(yr):
    return round(200 + (yr - 100) / 500 * 1380, 1)


def s55():
    """Artorius Castus about 200, Badon about 500, centuries apart; the name chain Artorius to Arthur."""
    ta, tc, tn = T("s55", "Lucius Artorius"), T("s55", "centuries too"), T("s55", "name probably")
    y = 640
    els = [axis(200, 1580, y, [(XC(v), str(v)) for v in (100, 200, 300, 400, 500)] + [(XC(600), "600 CE")], .1)]
    els += [{"k": "band", "x0": XC(150), "x1": XC(250), "y": y - 40, "h": 16, "c": BONE, "op": .5, "in": ta},
            rect(XC(150), y - 42, XC(250) - XC(150), 20, "none", BONE, 2, 10, ta, style="inferred")]
    ox_ = XC(200)
    els += warrior(ox_, y - 60, 220, ta, "#6a5a4c", face=1)
    els += [poly([(ox_ - 26, y - 270), (ox_ + 10, y - 312), (ox_ + 40, y - 280)], RED, at=ta + .1, fx="pop"),
            lab(ox_, y - 340, "Artorius Castus", ta + .3, BONE, 30)]
    els += [dot(XC(500), y, 12, AU, .3), lab(XC(500), y - 30, "Badon", .4, AU, 30)]
    els += bracket(XC(200), XC(500), y + 110, tc, "centuries apart", AMBER, up=True, size=28)
    els += [lab(1000, 250, "Artorius", tn, BONE, 46, st="serif"), arr([(1140, 238), (1290, 238)], tn + .5, AMBER, 4, dur=.5, curve=False),
            lab(1400, 250, "Arthur", tn + .9, GOLD, 46, st="serif"), lab(1200, 310, "the name", tn + 1.2, DIM, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s56():
    """A hero of folklore: a lilac giant with his hound walks out of the mist towards an open book."""
    tf, th = T("s56", "folklore"), T("s56", "history")
    f = 720
    els = [mist(560, op=.08, seed=3), mist(630, op=.09, seed=6), mist(690, op=.08, seed=8)]
    els += [gl(620, 420, 440, tf - .4, .45, "glow")] + king(620, f, 440, tf - .4, outline=LILAC, style="claimed", fx="fade", w=3.5, fill="rgba(201,193,238,.2)")
    els += dog(860, f, 110, tf, LILAC, style="claimed", fill="rgba(201,193,238,.2)", w=3, fx="fade")
    els += open_book(1330, 430, 440, 250, th - .6, rows=6) + [gl(1330, 520, 260, th, .5, "lamp")]
    els += [lab(620, 210, "a folk hero?", tf + .3, LILAC, 34, st="ital"), lab(1330, 760, "given a history", th, GOLD, 32)]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


LROWS = [205, 315, 425, 535, 645]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 48, 1500, 96, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1180, y, grade, gc, gt, 28, "start")
    return out


def pic_hill(x, y, at):
    return [poly([(x - 50, y + 30), (x - 20, y - 14), (x + 20, y - 20), (x + 50, y + 30)], "#4a5a34", "rgba(255,236,206,.4)", 1, at, fx="pop"), dot(x - 18, y + 22, 5, FIRE, at)]


def pic_hall(x, y, at):
    return [rect(x - 40, y - 4, 80, 30, "#8a6a44", "rgba(255,236,206,.4)", 1, 2, at, fx="pop"), poly([(x - 48, y - 4), (x, y - 36), (x + 48, y - 4)], "#b89a5a", at=at, fx="pop")]


def pic_castle(x, y, at):
    out = []
    for k, (dx, h) in enumerate(((-30, 40), (0, 60), (30, 46))):
        out += [rect(x + dx - 9, y + 30 - h, 18, h, "none", LILAC, 2, 1, at, style="claimed")]
    return out


def pic_cross(x, y, at):
    return lead_cross(x, y - 34, at, s=.11, letters=False)


def pic_man(x, y, at):
    return [figure(x - 12, y + 38, 74, at, "#cbbca8", "pop"), poly([(x + 14, y + 38), (x + 30, y - 26), (x + 44, y + 38)], "rgba(201,193,238,.08)", LILAC, 2, at, style="claimed")]


def s57():
    """The ledger: Badon (Strong evidence), the great lords of Tintagel and Cadbury (Established); three rows still to weigh."""
    t1, g1 = T("s57", "British victory"), T("s57", "Strong evidence")
    t2, g2 = T("s57", "Great lords"), T("s57", "Established")
    els = [rect(110, 140, 1560, 570, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += [rect(140, y - 48, 1500, 96, "none", "rgba(242,201,142,.16)", 1.5, 12, .5, style="inferred") for y in LROWS[2:]]
    els += lrow(0, t1, pic_hill, "a British victory at Badon", "Strong evidence", g1, GRADE["strong"])
    els += lrow(1, t2, pic_hall, "great lords at Tintagel and Cadbury", "Established", g2, GRADE["established"])
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s58_add():
    """Rows 3 and 4: Camelot at Cadbury and the birth at Tintagel (Awaiting evidence); the grave at Glastonbury (Ruled out), its cross struck."""
    t3, g3 = T("s58", "Camelot at"), T("s58", "Awaiting evidence")
    t4, g4 = T("s58", "His grave"), T("s58", "Ruled out")
    els = lrow(2, t3, pic_castle, "Camelot at Cadbury, birth at Tintagel", "Awaiting evidence", g3, GRADE["awaiting"])
    els += lrow(3, t4, pic_cross, "the grave at Glastonbury", "Ruled out", g4, GRADE["ruled"]) + [strike(170, LROWS[3] + 34, 262, LROWS[3] - 34, g4 + .2, RED, 5)]
    return els


def s59_add():
    """Row 5: a real war-leader called Arthur, Open question; a soft glow on its chip."""
    t5, g5 = T("s59", "real war-leader"), T("s59", "Open question")
    els = lrow(4, t5, pic_man, "a real war-leader called Arthur", "Open question", g5, GRADE["open"])
    els += [gl(1330, LROWS[4], 220, g5, .35, "lamp")]
    return els


def s60():
    """What would settle it: a memorial stone and a page from his lifetime, blank and dashed; two slates found at Tintagel; an almost empty shelf."""
    tt, t2, tn = T("s60", "text or an"), T("s60", "two inscribed"), T("s60", "almost nothing")
    els = [gl(560, 430, 560, .1, .2, "lamp")]
    els += [poly([(240, 720), (240, 300), (290, 236), (420, 236), (470, 300), (470, 720)], "rgba(201,193,238,.06)", LILAC, 3, tt, style="claimed"),
            ln([(280, 420), (430, 420)], tt + .3, LILAC, 3.5, "claimed", draw=False), ln([(280, 480), (430, 480)], tt + .35, LILAC, 3.5, "claimed", draw=False),
            rect(560, 280, 260, 340, "rgba(201,193,238,.06)", LILAC, 3, 4, tt + .5, style="claimed")]
    els += [ln([(596, 330 + 38 * k), (784, 330 + 38 * k)], tt + .6, "rgba(201,193,238,.45)", 2.5, draw=False) for k in range(7)]
    els += [lab(530, 780, "a name from his lifetime", tt + .8, LILAC, 32, st="ital")]
    for k, (x, yr) in enumerate(((1040, "1998"), (1250, "2018"))):
        els += [poly([(x - 76, 520), (x - 52, 400), (x + 64, 388), (x + 88, 494), (x + 52, 566), (x - 64, 566)], "#3e4650", "rgba(220,226,232,.6)", 2, t2 + .3 * k, fx="pop"),
                {"k": "glyphs", "x": x - 50, "y": 420, "w": 110, "h": 110, "rows": 3, "cols": 4, "kind": "latin", "c": "rgba(232,236,240,.65)", "in": round(t2 + .3 * k + .1, 2)}]
        els += tagc(x, 630, yr, t2 + .3 * k + .2, AMBER, 28)
    els += [lab(1145, 340, "found at Tintagel", t2 + .6, BONE, 30)]
    els += [rect(1380, 700, 300, 14, "#5a4632", "rgba(255,236,206,.35)", 1, 2, tn - .3), rect(1400, 610, 30, 90, "#7a3a28", "rgba(255,236,206,.35)", 1, 2, tn, fx="pop"),
            lab(1530, 760, "almost nothing survives", tn + .4, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s61():
    """The close: a hill at dawn, the ring of an old fort and one figure on its rampart; beneath it, a buried stone with a name we cannot read."""
    tw, tg = T("s61", "won"), T("s61", "ground may")
    g = 580
    hill = [(-40, g), (200, 560), (420, 500), (640, 420), (800, 384), (980, 380), (1140, 404), (1360, 470), (1600, 540), (1820, 570), (1820, g + 40), (-40, g + 40)]
    els = [poly(hill, "#232620", "rgba(255,226,190,.35)", 1.5, -1, curve=True),
           ln([(700, 404), (889, 372), (1080, 386), (1180, 412)], -1, "rgba(255,226,190,.4)", 3.5, curve=True, draw=False),
           ln([(660, 432), (889, 400), (1110, 414), (1220, 440)], -1, "rgba(255,226,190,.25)", 3, curve=True, draw=False)]
    els += [mist(500, op=.10, seed=4), mist(548, op=.09, seed=7)]
    els += [figure(889, 376, 40, tw - .4, "#1a1511", "fade")]
    sx, sy = 889, 720
    els += [poly([(sx - 110, sy - 30), (sx - 70, sy - 80), (sx + 100, sy - 84), (sx + 120, sy - 20), (sx + 70, sy + 26), (sx - 90, sy + 26)], "#3e4650", "rgba(220,226,232,.4)", 1.5,
                 tg - .4, fx="fade"),
            ln([(sx - 60, sy - 38), (sx + 70, sy - 38)], tg, LILAC, 3.5, "claimed", draw=False), ln([(sx - 60, sy - 4), (sx + 40, sy - 4)], tg + .1, LILAC, 3.5, "claimed", draw=False),
            gl(sx, sy - 20, 230, tg, .4, "glow")]
    return {"base": "sky", "tod": "dawn", "ground": g, "groundc": GROUND, "sun": [1500, 470, 26],
            "ridges": [{"y": 540, "a": 40, "c": "#3a3046", "seed": 4}, {"y": 570, "a": 16, "c": "#2a2436", "seed": 8}], "cam": CAM, "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "The monks of", "s2"), (2, "Was this King", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(0, "Then the last armies", "s6"), (1, "After about {402", "s7"), (1, "That's why it's called", "s8")], {"chapter": "When Rome left"}),
    (1, 1, "collision", "s9", [(0, "A British churchman", "s10")], {}),
    (1, 2, "reversal", "s11", [(1, "In early medieval", "s12"), (1, "Yet newcomers", "s13")], {}),
    (1, 3, "tag", "s14", [], {}),
    (2, 0, "world", "s15", [(1, "When did he", "s16")], {"chapter": "The only witness"}),
    (2, 1, "collision", "s17", [(1, "Then wins and", "s18"), (1, "And Gildas adds", "s19")], {}),
    (2, 2, "reversal", "s20", [(0, "He names Ambrosius", "s21")], {}),
    (2, 3, "collision", "s22", [(1, "Like saying", "s23"), (1, "But the poem", "s24")], {}),
    (2, 4, "tag", "s25", [], {}),
    (3, 0, "world", "s26", [], {"chapter": "Arthur appears"}),
    (3, 1, "collision", "s27", [(1, "There, nine hundred", "s28")], {}),
    (3, 2, "reversal", "s29", [], {}),
    (3, 3, "cost", "s30", [], {}),
    (3, 4, "collision", "s31", [(1, "But these annals", "s32")], {}),
    (3, 5, "tag", "s33", [], {}),
    (4, 0, "world", "s34", [(1, "His Arthur is", "s35")], {"chapter": "The making of a king"}),
    (4, 1, "collision", "s36", [(0, "In the {1170s", "s37")], {}),
    (4, 2, "reversal", "s38", [], {}),
    (4, 3, "collision", "s39", [(1, "Seven years later", "s40"), (1, "Their cross calls", "s41"), (1, "And England's kings", "s42")], {}),
    (4, 4, "cost", "s43", [], {}),
    (4, 5, "tag", "s44", [], {}),
    (5, 0, "world", "s45", [(1, "From {1966", "s46"), (1, "They raised a great", "s47")], {"chapter": "Digging for Camelot"}),
    (5, 1, "collision", "s48", [], {}),
    (5, 2, "collision", "s49", [(0, "And it has given", "s50")], {}),
    (5, 3, "reversal", "s51", [(1, "From {2016", "s52")], {}),
    (5, 4, "tag", "s53", [], {}),
    (6, 0, "weigh", "s54", [(0, "Lucius Artorius", "s55"), (0, "Or a hero of", "s56")], {"chapter": "The weighing"}),
    (6, 1, "weigh", "s57", [(1, "Camelot at Cadbury", "s58"), (2, "And a real war-leader", "s59")], {}),
    (6, 2, "test", "s60", [], {}),
    (6, 3, "close", "s61", [], {}),
]

# alias shots: (the panel they return to, the camera on that panel, the function drawing their additions on arrival)
ALIASES = {
    "s3": ("s2", [1, 889, 500], "s3_add"),
    "s6": ("s5", [1, 889, 500], "s6_add"),
    "s19": ("s16", [1, 889, 500], "s19_add"),
    "s20": ("s18", [1.45, 1300, 450], "s20_add"),
    "s23": ("s22", [1, 889, 500], "s23_add"),
    "s25": ("s24", [1, 889, 500], "s25_add"),
    "s40": ("s2", [1.3, 900, 540], "s40_add"),
    "s41": ("s1", [1.3, 1120, 470], "s41_add"),
    "s48": ("s45", [1, 889, 500], "s48_add"),
    "s53": ("s49", [1, 889, 500], "s53_add"),
    "s58": ("s57", [1, 889, 500], "s58_add"),
    "s59": ("s57", [1, 889, 500], "s59_add"),
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


def _stub(sid):
    return {"base": "dark", "cam": CAM, "els": [lab(889, 480, sid, .3, AMBER, 40)]}


def film():
    script = json.load(open(SCRIPT, encoding="utf-8"))
    SAY.clear(); SAY.update(_segments(script))
    g = globals()
    panels = {}
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in ALIASES and sid not in panels:
                panels[sid] = g[sid]() if sid in g else _stub(sid)
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
    ep = {"id": "lf-arthur", "code": "LF.16", "series": script["series"], "title": script["title"], "case": "arthur",
          "verdict": "contested", "claim": "Was there a real King Arthur behind the legend?", "mood": "mystery",
          "hook_text": "Was there ever a *real* King Arthur?", "beats": beats, "shots": shots,
          "sources": "Gildas, De Excidio (c. 540 or earlier) · Historia Brittonum (c. 829) · Annales Cambriae (10th century) · Geoffrey of Monmouth (c. 1136) · "
                     "Charles-Edwards 1991 · Dumville 1977 · Padel 1994 · Higham 2002 · Halsall 2013 · Alcock 1971, 1995 · Rahtz 1993 · "
                     "Barrowman, Batey & Morris 2007 · Gretzinger et al. 2022 (doi:10.1038/s41586-022-05247-2) · Ashe 1981 (doi:10.2307/2846937)",
          "post": "In 1191, monks at Glastonbury said they had found King Arthur's grave. We read the sources in the order they were written: Gildas, "
                  "who lived through the battle of Badon and never names Arthur; the History of the Britons, three centuries later; Geoffrey of Monmouth, "
                  "who made him a king; then the digs at Cadbury and Tintagel, the candidates, and each piece of the legend, weighed.",
          "hashtags": ["#KingArthur", "#Camelot", "#Glastonbury", "#Tintagel", "#DarkAges", "#WeighItYourself"],
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
