"""LF.02 · Drowned Worlds · Atlantis: The Whole File, Weighed (16:9 long film, one wall).

The script is films/long/lf-atlantis/script.json: its lines are read from there, untouched, and only [go:N|t] markers are
added at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s69), drawn while it is said:
an island empire drowned in a day and a night, a chain of tellers, a date at the end of the ice, a sea floor with no room
for a continent, four places people have searched, a Greek city that really sank in Plato's lifetime, and the weighing.
Drawings are schematic and true to the numbers said: solid = measured, dashed = inferred, dotted = claimed (Plato's story).
Poseidon appears only as a name (Plato's story, Helike's temple): no god is drawn, a temple outline at most.

Engine workaround (reported): the wall only adds elements to a panel on its first visit, at a beat start or a line start;
several shots add to a panel they return to in the middle of a line. Such a shot is an alias of its panel with a camera
whose zoom carries a tiny unique tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that
camera gets the shot's additions as a panel item (kit.js builds them on that step's clock, exactly as `adds` would).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-atlantis/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-atlantis/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-atlantis RC_FILMS_EPS=/tmp/claude-0/sbx_lf-atlantis/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-atlantis/boards python3 films.py long.lf_atlantis
"""
import copy, json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, ellipse
import f04

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-atlantis", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800

BONE, AMBER, GOLD, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, "#f2c98e", I.BLUE, I.LILAC, I.RED, I.GREEN
SEA, DEEP, LAND, ISLET = "#3f86a8", "#1d3a4a", "#8aa05a", "#d9c9a0"
COPPER, BRONZE, TIN, DIM = "#e0703c", "#c0904c", "#c9ccd2", "#cbbca8"
WOOD, PAPY, STONE = "#8a6a44", "#e9d6ad", "#cdbb95"
WPS = 2.3                    # spoken words a second (the narrator's pace, pauses included)


# ================================================================== narration: the script's own lines, timing
def words(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", s)
    s = re.sub(r"@\w+", "", s).replace("-", " ")
    return [w for w in (re.sub(r"[^\w']", "", x).lower() for x in s.split()) if w]


SAY = {}                     # shot id -> the narration spoken while its step is on screen (set in film())


def T(sid, phrase, lead=.35, k=1):
    """Seconds after the shot's step starts at which `phrase` is said (its k-th occurrence)."""
    ws, ps = words(SAY[sid]), words(phrase)
    hits = [i for i in range(len(ws)) if ws[i:i + len(ps)] == ps]
    assert len(hits) >= k, (sid, phrase, SAY[sid])
    return round(lead + hits[k - 1] / WPS, 2)


def dur(sid):
    return round(len(words(SAY[sid])) / WPS, 2)


def _find(line, phrase):
    """Index in the raw line where `phrase` starts, ignoring the ^ stress marks."""
    keep = [i for i, ch in enumerate(line) if ch != "^"]
    flat = "".join(line[i] for i in keep)
    assert flat.count(phrase) == 1, (phrase, line)
    return keep[flat.index(phrase)]


def _mark(line, phrase, tag):
    """Insert `tag` at the start of the sentence that begins with `phrase`: before its [p:]/[act:]/[sfx:]/[tune:]/[gap:] tags,
    after a [d:] mood tag."""
    j = _find(line, phrase)
    while True:
        m = re.search(r"\[[^\]]*\]$", line[:j])
        if not m or line[m.start():m.start() + 3] == "[d:":
            break
        j = m.start()
    return line[:j] + tag + line[j:]


# ================================================================== small drawings
def E(cx, cy, rx, ry, n=48):
    return I.ellipse(cx, cy, rx, ry, n)[:-1]


def poly(p, fill, c="none", w=0, at=0, fx=None, op=None, curve=False, style="known", **kw):
    e = {"k": "poly", "p": [[round(a, 1), round(b, 1)] for a, b in p], "fill": fill, "c": c, "w": w, "in": at, "curve": curve, "style": style}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def lab(x, y, t, at, c=BONE, size=28, a="middle", st="lab", **kw):
    return label(round(x, 1), round(y, 1), t, at, c, size, a, st, **kw)


def chip(x, y, t, at, c=AMBER, size=26, fill="rgba(18,13,10,.82)", a="middle"):
    """A rounded tag with a few words, centred on x (or starting at x when a='start')."""
    w = len(t) * size * .56 + 30
    x0 = x - w / 2 if a == "middle" else x
    return [box(round(x0, 1), round(y - size * .95, 1), round(w, 1), round(size * 1.55, 1), fill, c, 2, size * .7, at, fx="pop"),
            lab(x0 + w / 2, y + size * .2, t, at + .1, c, size, halo=False)]


def bar(x0, x1, y, at, c=AMBER, w=10, dur=1.0, op=None, style="known"):
    e = {"k": "line", "p": [[round(x0, 1), y], [round(x1, 1), y]], "c": c, "w": w, "fx": "draw", "dur": dur, "in": at, "style": style}
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def bracket(x0, x1, y, at, t=None, c=BONE, up=True, size=26, ty=None):
    d = -12 if up else 12
    out = [line([[x0, y + d], [x0, y], [x1, y], [x1, y + d]], at, c, 2, dur=.6)]
    if t:
        out.append(lab((x0 + x1) / 2, ty if ty is not None else (y - 14 if not up else y + 34), t, at + .3, c, size))
    return out


def seated(x, y, h, at, c="#e8d6b8", stool=True):
    """A figure seated on a stool, facing right; feet on y, h = his standing height."""
    out = []
    if stool:
        out.append(box(x - .13 * h, y - .25 * h, .2 * h, .25 * h, "#3a2c20", "#8a6a48", 1.5, 3, at, fx="rise"))
    out += [poly([[x - .07 * h, y - .63 * h], [x + .11 * h, y - .63 * h], [x + .1 * h, y - .29 * h], [x - .1 * h, y - .29 * h]], c, at=at, fx="rise"),
            poly([[x - .1 * h, y - .33 * h], [x + .25 * h, y - .33 * h], [x + .26 * h, y - .25 * h], [x - .1 * h, y - .24 * h]], c, at=at, fx="rise"),
            poly([[x + .19 * h, y - .27 * h], [x + .26 * h, y - .27 * h], [x + .27 * h, y], [x + .18 * h, y]], c, at=at, fx="rise"),
            {"k": "circle", "x": round(x + .04 * h, 1), "y": round(y - .72 * h, 1), "r": round(.075 * h, 1), "fill": c, "c": "none", "w": 0, "in": at, "fx": "rise"},
            line([[x + .06 * h, y - .58 * h], [x + .2 * h, y - .5 * h], [x + .3 * h, y - .44 * h]], at, c, max(3, .05 * h), draw=False)]
    return out


def crown(x, y, s, at, c=GOLD):
    return poly([[x - s, y], [x - s, y - s * 1.1], [x - s * .5, y - s * .5], [x, y - s * 1.2], [x + s * .5, y - s * .5], [x + s, y - s * 1.1], [x + s, y]], c, at=at, fx="pop")


def king(x, y, h, at):
    return [person(x, y, h, at, "#e8d6b8", "pop"), crown(x, y - h * .99, h * .12, at + .05)]


def trireme(x, y, L, at, c="#c9a370", style="known", fx="rise", face=1):
    """A trireme side-on: a long low hull with a ram at the bow and a stern curving up, a mast and square sail, three banks of
    oars as ticks. x, y = middle of the waterline; L = length."""
    f = face
    P = lambda a, b: [round(x + f * a * L, 1), round(y + b * L, 1)]
    hull = [P(.58, .01), P(.47, -.02), P(.44, -.075), P(-.38, -.075), P(-.47, -.12), P(-.5, -.2), P(-.46, -.24), P(-.47, -.16), P(-.43, -.1), P(-.42, .035), P(.4, .035)]
    if style != "known":
        return [poly(hull, "rgba(201,193,238,.12)", c, 2.5, at, style=style), line([P(0, -.075), P(0, -.38)], at, c, 2.5, style, draw=False),
                poly([P(-.11, -.36), P(.11, -.36), P(.11, -.16), P(-.11, -.16)], "none", c, 2.5, at, style=style)]
    out = [poly(hull, "#5a4030", c, 1.5, at, fx=fx), line([P(0, -.075), P(0, -.38)], at, c, max(2, L * .008), draw=False),
           poly([P(-.11, -.36), P(.11, -.36), P(.12, -.17), P(-.1, -.17)], "#e9dcc0", "#8a6a44", 1, at + .1, fx="pop")]
    for k in range(15):
        a = -.36 + k * .052
        out.append(line([P(a, .03), P(a - .035, .1 + .015 * (k % 3))], at + .15, c, max(1.2, L * .006), draw=False))
    return out


def sailship(x, y, s, at, c=BONE):
    return [poly([[x - s, y - s * .15], [x + s, y - s * .15], [x + s * .75, y + s * .12], [x - s * .8, y + s * .12]], "#5a4030", c, 1.5, at, fx="pop"),
            line([[x, y - s * .15], [x, y - s * 1.3]], at, c, 2, draw=False),
            poly([[x + 4, y - s * 1.25], [x + s * .7, y - s * .3], [x + 4, y - s * .3]], "#efe6d2", at=at, fx="pop"),
            poly([[x - 4, y - s * 1.1], [x - s * .6, y - s * .3], [x - 4, y - s * .3]], "#e2d6bd", at=at, fx="pop")]


def steamer(x, y, s, at, c=BONE):
    return [poly([[x - s, y - s * .18], [x + s, y - s * .18], [x + s * .8, y + s * .14], [x - s * .85, y + s * .14]], "#3a3a40", c, 1.5, at, fx="pop"),
            box(x - s * .45, y - s * .45, s * .7, s * .27, "#8a8f98", r=2, at=at),
            box(x - s * .05, y - s * .85, s * .16, s * .42, "#b0503a", r=2, at=at),
            oval(x + s * .1, y - s * 1.05, s * .22, s * .1, "#8a8378", at=at + .2, op=.6)]


def drillship(x, y, s, at, c=BONE):
    return [poly([[x - s, y - s * .18], [x + s, y - s * .18], [x + s * .8, y + s * .14], [x - s * .85, y + s * .14]], "#3a3a40", c, 1.5, at, fx="pop"),
            line([[x - s * .22, y - s * .18], [x, y - s * 1.2], [x + s * .22, y - s * .18]], at, "#e8c35a", 3, draw=False),
            line([[x - s * .14, y - s * .55], [x + s * .14, y - s * .55]], at, "#e8c35a", 2, draw=False),
            box(x - s * .85, y - s * .4, s * .4, s * .22, "#cbd2d8", r=2, at=at)]


def temple_line(x, y, w, at, c=LILAC, style="claimed", wd=2.5):
    """A temple front in outline (a story's temple, or a temple drawn as a sign): base, five columns, pediment."""
    h = w * .55
    out = [line([[x - w / 2, y], [x + w / 2, y]], at, c, wd, style, draw=False)]
    for k in range(5):
        cx = x - w * .4 + k * w * .2
        out.append(line([[cx, y], [cx, y - h * .75]], at, c, wd, style, draw=False))
    out.append(line([[x - w * .52, y - h * .78], [x + w * .52, y - h * .78], [x, y - h * 1.15], [x - w * .52, y - h * .78]], at, c, wd, style, draw=False))
    return out


def droplet(x, y, s, at, c):
    return poly([[x, y - s], [x + s * .55, y - s * .05], [x + s * .5, y + s * .4], [x, y + s * .6], [x - s * .5, y + s * .4], [x - s * .55, y - s * .05]], c, "#fff6e6", 1.5, at, fx="pop", curve=True)


def elephant(x, y, s, at, c="#cbbca8"):
    """An elephant in profile facing right, feet on y, s = body length."""
    P = lambda a, b: [x + s * a, y + s * b]
    body = [P(-.5, -.42), P(-.3, -.62), P(.1, -.66), P(.32, -.6), P(.44, -.72), P(.6, -.7), P(.66, -.55), P(.64, -.3), P(.7, -.08), P(.64, -.06),
            P(.56, -.3), P(.5, -.36), P(.42, -.3), P(.4, 0), P(.26, 0), P(.24, -.26), P(-.18, -.26), P(-.2, 0), P(-.34, 0), P(-.38, -.3), P(-.5, -.34)]
    return [poly(body, c, at=at, fx="pop", curve=True), dot(round(x + s * .55, 1), round(y - s * .6, 1), max(2, s * .02), "#2a2018", at + .05)]


def bull(x, y, s, at, c="#3a2a22", face=1, style="known", lc=None):
    """A bull in profile, feet on y, s = body length, facing right (face=1) or left (-1): humped back, head lowered, horns forward."""
    P = lambda a, b: [round(x + face * s * a, 1), round(y + s * b, 1)]
    body = [P(-.52, -.44), P(-.42, -.56), P(-.1, -.62), P(.12, -.68), P(.28, -.64), P(.4, -.56), P(.5, -.5), P(.6, -.38), P(.58, -.3), P(.5, -.28),
            P(.38, -.3), P(.32, -.22), P(.1, -.2), P(-.3, -.22), P(-.48, -.26)]
    legs = [(.3, .22), (.2, .22), (-.32, .2), (-.42, .2)]
    lc = lc or c
    horns = [[P(.44, -.58), P(.5, -.7), P(.6, -.76), P(.66, -.72)], [P(.4, -.6), P(.42, -.72), P(.5, -.8), P(.55, -.8)]]
    tail = [P(-.5, -.5), P(-.6, -.38), P(-.6, -.16)]
    if style != "known":
        out = [poly(body, "rgba(201,193,238,.08)", lc, 2.5, at, style=style, curve=True)]
        out += [line([P(a, -.24), P(a + .02, 0)], at, lc, 2.5, style, draw=False) for a, _ in legs]
        out += [line(h, at, lc, 2.5, style, draw=False, curve=True) for h in horns] + [line(tail, at, lc, 2, style, draw=False, curve=True)]
        return out
    out = [poly(body, c, at=at, fx="rise", curve=True)]
    out += [poly([P(a - .03, -.24), P(a + .03, -.24), P(a + .025, 0), P(a - .015, 0)], c, at=at) for a, _ in legs]
    out += [line(h, at + .1, "#efe6d2", max(3, s * .02), draw=False, curve=True) for h in horns] + [line(tail, at, c, max(3, s * .015), draw=False, curve=True)]
    return out


def leaper(x, y, s, at, c="#b0301e"):
    """A Minoan bull-leaper vaulting upside down: hands on the bull's back at (x, y), body arched up and over; s = height."""
    P = lambda a, b: [round(x + s * a, 1), round(y + s * b, 1)]
    return [line([P(0, 0), P(.02, -.26)], at, c, max(4, s * .05), draw=False), line([P(.06, 0), P(.05, -.26)], at, c, max(4, s * .05), draw=False),
            {"k": "circle", "x": P(.1, -.2)[0], "y": P(.1, -.2)[1], "r": round(s * .07, 1), "fill": c, "c": "none", "w": 0, "in": at},
            line([P(.03, -.28), P(-.12, -.62), P(-.32, -.82)], at, c, max(6, s * .1), draw=False, curve=True),
            line([P(-.3, -.8), P(-.56, -.78)], at, c, max(5, s * .07), draw=False), line([P(-.32, -.84), P(-.6, -.9)], at, c, max(5, s * .07), draw=False)]


def volcano(x, y, s, at, c="#5a4636", erupt=True):
    out = [poly([[x - s, y], [x - s * .2, y - s * .7], [x + s * .2, y - s * .7], [x + s, y]], c, "#8a6a48", 1.5, at, fx="rise")]
    if erupt:
        out += [glow(x, y - s * .75, s * .7, at + .2, .9, "red")] + [oval(x + s * .15 * k, y - s * (1.0 + .32 * k), s * (.22 + .06 * k), s * (.14 + .03 * k), "#8a8378", at=round(at + .3 + .15 * k, 2), op=.75) for k in range(3)]
    return out


def magnifier(x, y, r, at, c=BONE):
    return [ring(x, y, r, at, c, 4, dur=.5), line([[x + r * .7, y + r * .7], [x + r * 1.5, y + r * 1.5]], at + .3, c, 7, dur=.3)]


def hammer(x, y, s, at, c="#cbd2d8"):
    return [line([[x, y], [x + s * .7, y - s * .7]], at, "#c9905a", max(4, s * .12), draw=False),
            poly([[x + s * .48, y - s * 1.0], [x + s * 1.0, y - s * .48], [x + s * .86, y - s * .34], [x + s * .34, y - s * .86]], c, at=at, fx="pop")]


def scroll(x, y, w, at, c=PAPY, style="known"):
    return f04._scroll(x, y, w, at, c, style)


def wave(x0, x1, y, at, c=BLUE, amp=10, n=None, w=3, dur=.8):
    return f04._wave(x0, x1, y, at, c, amp, n, w, dur)


def blob(cx, cy, rx, ry, seed=1, n=14, amp=.18):
    r = random.Random(seed)
    k = [1 + r.uniform(-amp, amp) for _ in range(n)]
    return [[round(cx + rx * k[i] * math.cos(2 * math.pi * i / n), 1), round(cy + ry * k[i] * math.sin(2 * math.pi * i / n), 1)] for i in range(n)]


def axis(x0, x1, y, ticks, at, t=None, below=True):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": at}
    if t:
        e["t"] = t
    if not below:
        e["below"] = False
    return e


def scalebar(x, y, w, t, at):
    w = round(w, 1)
    return [line([[x, y], [x + w, y]], at, "#e9dccb", 2, draw=False), line([[x, y - 8], [x, y + 8]], at, "#e9dccb", 2, draw=False),
            line([[x + w, y - 8], [x + w, y + 8]], at, "#e9dccb", 2, draw=False), lab(x + w / 2, y - 14, t, at, "#e9dccb", 24)]


def tick(x, y, at, c=GREEN, s=1.0):
    return f04._tick(x, y, at, c, s)


# ================================================================== the cold open
CX, CY, Q, U = 889, 610, .32, 22.0     # the ring city on the island: centre, plan tilt, units per stadion
RINGS = [(13.5, SEA), (10.5, LAND), (7.5, SEA), (5.5, LAND), (3.5, SEA), (2.5, ISLET)]    # outer edge of each zone (Critias 115d-116a)


def city_plan(cx, cy, u, at, q=Q, step=.3, ghost=False, c=LILAC):
    """Plato's ring city in plan: an islet 5 stadia across, rings of water 1, 2, 3 stadia and of land 2, 3 (27 stadia in all),
    built from the centre outwards. ghost: the same in lilac dotted outline (a story)."""
    if ghost:
        return [{"k": "line", "p": E(cx, cy, r * u, r * u * q), "c": c, "w": 2.5, "style": "claimed", "curve": True, "close": True, "in": round(at + .1 * k, 2)}
                for k, (r, _) in enumerate(reversed(RINGS))]
    out = []
    for k, (r, col) in enumerate(RINGS):
        tk = round(at + step * (len(RINGS) - 1 - k), 2)
        out.append(poly(E(cx, cy, r * u, r * u * q), col, "rgba(245,236,220,.45)", 1.2, tk, fx="pop", curve=True, op=.95))
    return out


def s1():
    """The island at night; the ring city traces itself from the centre outwards; its walls flash red, tin and bronze."""
    sid = "s1"
    rings_at = T(sid, "A city of rings") + .2
    red = T(sid, "red metal")
    els = [{"k": "water", "y": 380, "h": 700, "op": .9, "in": -1},
           poly(E(CX, CY + 14, 400, 128), "#2e2a1e", at=.2, fx="rise", curve=True),
           poly(E(CX, CY, 400, 128), "#55613a", "rgba(201,215,154,.6)", 2, .3, fx="rise", curve=True),
           glow(CX, CY, 420, .4, .25, "lamp")]
    els += city_plan(CX, CY, U, rings_at)
    els += [box(CX + 13.5 * U - 4, CY - 7, 400 - 13.5 * U + 8, 14, SEA, r=2, at=rings_at + 1.9)]               # the canal to the sea
    els += f04._temple(CX, CY + 2, 44, rings_at + 1.6, "#efe6d2")
    els += [lab(CX, 456, "Atlantis", 4.2, LILAC, 44, st="ital")]
    for k, (r, c, w) in enumerate(((10.5, BRONZE, 4), (5.5, TIN, 4), (2.5, COPPER, 5))):
        els.append({"k": "line", "p": E(CX, CY, r * U, r * U * Q), "c": c, "w": w, "curve": True, "close": True, "fx": "draw", "dur": .7, "in": round(red - .4 + .3 * k, 2)})
    els += [glow(CX, CY, 120, red + .3, .9, "red"), glow(CX - 30, CY - 6, 50, red + .5, .8, "fire")]
    return {"base": "sky", "tod": "night", "ground": 1300, "sun": False, "cam": [1, 889, 500], "els": els}


def s2_add():
    """Ten kings on the islet, a hundred pips of a hundred chariots on the outer ring, six triremes in the docks."""
    sid = "s2"
    k0, c0, d0 = T(sid, "Ten kings"), T(sid, "ten thousand"), T(sid, "docks")
    out = []
    for k in range(10):
        a = math.radians(-90 + 36 * k + 18)
        out += king(round(CX + 42 * math.cos(a), 1), round(CY + 6 + 14 * math.sin(a), 1), 22, round(k0 + .1 * k, 2))
    rr = 8.5 * U
    out += [dot(round(CX + rr * math.cos(2 * math.pi * k / 100), 1), round(CY + rr * Q * math.sin(2 * math.pi * k / 100), 1), 3.4, GOLD, round(c0 + .018 * k, 3)) for k in range(100)]
    out += [lab(CX, 772, "10,000 chariots", c0 + 1.6, GOLD, 30)]
    rw = 12 * U
    for k in range(6):
        a = math.radians(48 + 17 * k)
        out += trireme(round(CX + rw * math.cos(a), 1), round(CY + rw * Q * math.sin(a), 1), 34, round(d0 + .18 * k, 2))
    return out


def s3_add():
    """One day and one night: the sun sets, the moon crosses, the sun rises; the sea climbs over the rings; a question."""
    sid = "s3"
    t0, sea, q = T(sid, "in a single day"), T(sid, "the sea took"), T(sid, "Could an empire")
    arc = [[round(889 + 600 * math.cos(math.radians(a)), 1), round(372 - 222 * math.sin(math.radians(a)), 1)] for a in range(0, 181, 6)]
    out = [{"k": "line", "p": arc, "c": "#ffe2a8", "w": 2, "style": "inferred", "curve": True, "op": .7, "keepop": True, "in": t0, "fx": "draw", "dur": 2.2},
           glow(1489, 366, 110, t0, .9, "sun"), dot(1489, 366, 26, "#ffd9a0", t0),
           glow(889, 150, 90, t0 + 1.0, .5, "lamp"), dot(889, 150, 22, "#efe8da", t0 + 1.0), dot(899, 144, 22, "#141726", t0 + 1.0),
           glow(289, 366, 110, t0 + 2.0, .9, "sun"), dot(289, 366, 26, "#ffd9a0", t0 + 2.0),
           box(0, 474, W_, 340, "#1f5670", r=0, at=sea, op=.93, fx="fill", dur=2.6),
           wave(0, W_, 474, sea + 2.5, "#bfe6f5", 7, 30, 3, 1.2)]
    return out + I.question(889, 330, q, 110)


def s4():
    """Where people have searched: the Sahara, the Bahamas, a Greek volcano, the sea off Gibraltar."""
    sid = "s4"
    v = View(-85, 35, 10, 50, (90, 130, 1600, 660))
    pins = [("Sahara", "Eye of the Sahara", -11.39, 21.12, {"lx": 32}), ("Bahamas", "Bimini", -79.28, 25.77, {"lx": 32}),
            ("volcano", "Thera", 25.4, 36.4, {"lx": 30, "ly": 36}), ("Gibraltar", "Spartel Bank", -6.0, 35.9, {"a": "end", "lx": -32, "ly": -20})]
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(-45, 32), "Atlantic", .3, BLUE, 40, st="ital")]
    for cue, name, lo, la, o in pins:
        x, y = v.p(lo, la); at = T(sid, cue) - .2
        els.append(dict({"k": "pin", "x": x, "y": y, "t": name, "c": GOLD, "in": at, "fx": "pop"}, **o))
        els.append({"k": "circle", "x": x, "y": y, "r": 22, "fill": "none", "c": LILAC, "w": 2, "style": "inferred", "in": at + .2})
    els += scalebar(140, 760, v.km(1000), "1,000 km", .6)
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def room(x0=700, scroll_at=(4.0, 4.3), plato_at=.4, labels=True, lamp=True, settled=False, name_at=None):
    """Plato's room: a seated figure at a table, two scrolls, an oil lamp."""
    fy = 700
    els = [poly([[300, fy], [300, 300], [380, 220], [470, 200], [560, 220], [640, 300], [640, fy]], "rgba(60,46,34,.55)", "rgba(255,226,190,.18)", 2, -1),
           box(0, fy, W_, 120, "#1e1712", r=0, at=-1),
           line([[0, fy], [W_, fy]], -1, "rgba(255,226,190,.35)", 1.5, draw=False),
           box(1380, 260, 46, 440, "#5a4636", "rgba(255,226,190,.25)", 1.5, 2, -1), box(1366, 240, 74, 24, "#6b5440", r=2, at=-1)]
    els += seated(x0, fy, 300, plato_at)
    els += [box(880, 560, 400, 16, WOOD, "#c9a370", 1.5, 3, plato_at + .2), box(905, 576, 14, 124, "#5a4030", r=2, at=plato_at + .2),
            box(1240, 576, 14, 124, "#5a4030", r=2, at=plato_at + .2)]
    if lamp:
        els += [poly([[1180, 560], [1230, 560], [1222, 540], [1188, 540]], "#c9905a", at=plato_at + .3), glow(1205, 520, 180, plato_at + .3, .75, "fire"),
                glow(1100, 470, 520, plato_at + .3, .22, "lamp")]
    els += scroll(960, 528, 86, scroll_at[0]) + scroll(1080, 528, 86, scroll_at[1])
    if labels:
        els += [lab(x0 + 20, 738, "Plato", name_at if name_at is not None else plato_at + 2.0, BONE, 30),
                lab(960, 462, "Timaeus", scroll_at[0] + .3, GOLD, 30, st="ital"), lab(1080, 418, "Critias", scroll_at[1] + .3, GOLD, 30, st="ital")]
    if settled:
        for e in els:
            if e.get("in", 0) >= 0:
                e["in"] = -1
    return els


def s5():
    sid = "s5"
    man, books = T(sid, "one man"), T(sid, "two books")
    return {"base": "dark", "cam": [1.08, 960, 480], "els": room(scroll_at=(books, books + .35), plato_at=.3, name_at=man)}


# ================================================================== chapter 1: the only witness
V7 = View(4, 41, 28.5, 41.5, (90, 125, 1600, 505))


def s7():
    """Greece, the Aegean, the Nile delta: Athens, about 360 BCE; Plato writes two dialogues."""
    sid = "s7"
    v = V7
    ax, ay = v.p(23.73, 37.98)
    two = T(sid, "two dialogues")
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(17.5, 34.6), "Mediterranean", .2, BLUE, 30, st="ital"),
           {"k": "pin", "x": ax, "y": ay, "t": "Athens", "c": GOLD, "in": .5, "fx": "pop"}]
    els += f04._temple(ax, ay - 22, 30, .7, "#efe6d2")
    els += chip(ax, ay - 96, "about 360 BCE", 1.0, AMBER, 26)
    els += scroll(ax + 120, ay - 40, 44, two) + scroll(ax + 176, ay - 32, 44, two + .3)
    els += scalebar(1480 - v.km(200), 610, v.km(200), "200 km", .8)
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s9_add():
    """Egyptian priests at Sais told it to Solon, about two centuries before Plato wrote."""
    sid = "s9"
    v = V7
    ax, ay = v.p(23.73, 37.98)
    sx, sy = v.p(30.77, 30.96)
    t_sais, t_solon, t_cent = T(sid, "Sais"), T(sid, "Solon"), T(sid, "about two centuries")
    X = lambda bce: round(300 + (650 - bce) / 350 * 1180, 1)
    out = [{"k": "pin", "x": sx, "y": sy, "t": "Sais", "c": AMBER, "in": t_sais - .3, "fx": "pop", "a": "start", "ly": 36}]
    out += f04._temple(sx, sy - 20, 30, t_sais - .2, "#efe6d2")
    out += [person(sx - 42, sy + 4, 46, t_sais + .2, "#e8d6b8"), person(sx - 70, sy + 4, 46, t_sais + .35, "#e8d6b8")]
    out += [arrow([[sx - 10, sy - 36], [(sx + ax) / 2 + 40, (sy + ay) / 2 - 30], [ax + 24, ay + 16]], t_solon - .9, AMBER, 3, "inferred", 1.0),
            person(ax - 46, ay + 14, 54, t_solon, BONE), lab(ax - 60, ay + 50, "Solon", t_solon + .2, BONE, 28, "end")]
    ty = 712
    out += [axis(300, 1480, ty, [(X(600), "600 BCE"), (X(500), "500"), (X(400), "400"), (X(300), "300")], t_cent - 1.0),
            dot(X(590), ty, 10, BONE, t_cent - .6), lab(X(590), ty - 22, "Solon", t_cent - .5, BONE, 26),
            dot(X(360), ty, 10, GOLD, t_cent - .3), lab(X(360), ty - 22, "Plato writes", t_cent - .2, GOLD, 26)]
    out += bracket(X(590), X(360), ty - 62, t_cent + .2, "about 2 centuries", AMBER, up=True, ty=ty - 76)
    return out


def s8():
    """A dialogue: a long scroll unrolls like the script of a play, four speakers on it; Timaeus and Critias; Critias tells a story."""
    sid = "s8"
    play, tim, cri, chain = T(sid, "script of a play"), T(sid, "Timaeus"), T(sid, "Critias"), T(sid, "chain of tellers")
    told = T(sid, "the speaker Critias")
    els = [glow(889, 450, 700, .2, .25, "lamp"),
           {"k": "line", "p": [[250, 450], [1530, 450]], "c": PAPY, "w": 300, "op": .95, "keepop": True, "fx": "draw", "dur": 1.6, "in": .3},
           box(222, 286, 36, 328, "#cdb58a", "#8a6a3e", 2, 18, .3), box(1520, 286, 36, 328, "#cdb58a", "#8a6a3e", 2, 18, 1.8)]
    els += [{"k": "glyphs", "x": 290, "y": 330, "w": 1200, "h": 70, "rows": 2, "cols": 34, "kind": "latin", "c": "#6b5236", "op": .55, "in": 1.4}]
    xs = [460, 740, 1020, 1300]
    for k, x in enumerate(xs):
        at = round(play - .3 + .3 * k, 2)
        els += [person(x, 580, 120, at, "#3a2c20"), f04._bubble(x + 64, 438, 96, at + .15, WOOD, fill="rgba(255,248,232,.9)")]
    els += [glow(1020, 520, 110, told, .7, "lamp")]
    els += [{"k": "line", "p": [[1050 + 14 * j, 440 + (4 if j % 2 else -4)] for j in range(6)], "c": "#8a6a3e", "w": 3, "fx": "draw", "dur": .8, "in": chain}]
    els += [line([[240, 614], [240, 660]], tim, BONE, 2, draw=False), lab(240, 694, "Timaeus", tim, GOLD, 32, st="ital"),
            line([[1538, 614], [1538, 660]], cri, BONE, 2, draw=False), lab(1538, 694, "Critias", cri, GOLD, 32, st="ital")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s10():
    """The chain of tellers, as Plato tells it: priests, Solon, his family, an old man of about ninety, a boy of ten, then Plato.
    The story hops along it; the links are dashed (we have only Plato's word for the chain)."""
    sid = "s10"
    fam, old, boy, hops = T(sid, "passed down a family"), T(sid, "old man"), T(sid, "a boy"), T(sid, "Two hundred years")
    fy = 640
    els = [line([[100, fy], [1680, fy]], .2, "rgba(255,226,190,.3)", 2, draw=False)]
    els += f04._temple(190, fy, 120, .3, "#c9a878") + [person(260, fy, 110, .45, "#e8d6b8"), person(300, fy, 110, .55, "#e8d6b8"), lab(250, fy + 46, "priests", .7, AMBER, 28)]
    els += [person(500, fy, 140, .8, BONE), lab(500, fy + 46, "Solon", 1.0, BONE, 28)]
    els += [person(700, fy, 128, fam, "#d9c7a6"), person(860, fy, 128, fam + .4, "#d9c7a6"), lab(780, fy + 46, "his family", fam + .6, DIM, 26)]
    els += [{"k": "group", "tr": "rotate(10 1080 %d)" % fy, "in": old, "els": [person(1080, fy, 132, -1, "#d9c7a6")]},
            line([[1120, fy], [1112, fy - 70]], old, "#c9905a", 4, draw=False), lab(1080, fy + 46, "90", old + 1.0, AMBER, 32)]
    els += [person(1220, fy, 74, boy, "#e8d6b8"), lab(1220, fy + 46, "10", boy + .8, AMBER, 32)]
    els += seated(1430, fy, 150, boy + 1.4) + scroll(1540, fy - 70, 50, boy + 1.6) + [lab(1460, fy + 46, "Plato", boy + 1.6, BONE, 28)]
    heads = [(280, fy - 115), (500, fy - 145), (700, fy - 134), (860, fy - 134), (1095, fy - 132), (1220, fy - 80), (1440, fy - 118)]
    for k in range(len(heads) - 1):
        (xa, ya), (xb, yb) = heads[k], heads[k + 1]
        els.append(arrow([[xa + 18, ya - 10], [(xa + xb) / 2, min(ya, yb) - 46], [xb - 18, yb - 12]], round(hops - 1.4 + .25 * k, 2) if k else .9, AMBER, 2.5, "inferred", .5))
    for k, (x, y) in enumerate(heads):
        els += [glow(x, y - 24, 46, round(hops + .55 * k, 2), .95, "lamp"), dot(x, y - 24, 7, "#ffe2a8", round(hops + .55 * k, 2))]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 470], "els": els}


V11 = View(-60, 45, 12, 50, (90, 125, 1600, 640))


def _gpoly(v, pts):
    return [list(v.p(lo, la)) for lo, la in pts]


LIBYA = [(-9.5, 30.0), (-6.0, 35.8), (-1.0, 35.3), (3.0, 36.8), (10.0, 37.2), (11.0, 33.5), (15.0, 32.3), (20.0, 30.8), (25.0, 31.8), (29.0, 30.9),
         (29.0, 26.0), (16.0, 24.5), (0.0, 25.5), (-9.5, 27.5)]
ASIA = [(26.2, 40.2), (29.0, 41.2), (36.0, 42.0), (41.5, 41.4), (42.5, 37.5), (39.0, 34.0), (36.0, 31.0), (34.3, 31.3), (35.8, 34.2), (35.9, 36.6),
        (30.0, 36.2), (27.3, 37.0)]


def _area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2


def s11():
    """Beyond the Pillars of Heracles; larger than Libya and Asia put together: the two shapes, moved west, sit inside the
    claimed island, whose outline is drawn about 15 per cent larger in area than both together."""
    sid = "s11"
    v = V11
    gx, gy = v.p(-5.35, 36.0)
    pil, gib, lib, asia, tog = T(sid, "Pillars of Heracles"), T(sid, "Strait of Gibraltar"), T(sid, "Libya"), T(sid, "Asia"), T(sid, "put together")
    Lp, Ap = _gpoly(v, LIBYA), _gpoly(v, ASIA)
    bb = lambda P: (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))
    (lx0, ly0, lx1, ly1), (ax0, ay0, ax1, _) = bb(Lp), bb(Ap)
    cx, cy = 470, 430                                    # the open Atlantic, west of the Pillars
    A = (_area(Lp) + _area(Ap)) * 1.15
    rx = (lx1 - lx0) / 2 * 1.06; ry = A / math.pi / rx
    Lm = [[p[0] - (lx0 + lx1) / 2 + cx, p[1] - ly1 + cy + ry * .78] for p in Lp]
    Am = [[p[0] - (ax0 + ax1) / 2 + cx + 40, p[1] - ay0 + cy - ry * .8] for p in Ap]
    isle = blob(cx, cy, rx * 1.02, ry, 7, 16, .06)
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(-42, 16.5), "Atlantic", .3, BLUE, 34, st="ital")]
    els += f04._pillars(gx - 16, gy - 4, 36, pil - .2, "#efe6d2") + [lab(gx + 10, gy - 66, "Pillars of Heracles", pil + .2, BONE, 28, "start"),
                                                                     glow(gx, gy, 70, gib, .8, "lamp")]
    els += [poly(Lp, "rgba(232,184,122,.32)", AMBER, 2.5, lib - .2, curve=True), lab(*v.p(10, 28.5), "Libya", lib, AMBER, 34, st="ital"),
            poly(Ap, "rgba(232,184,122,.32)", AMBER, 2.5, asia - .2, curve=True), lab(*v.p(35, 38.3), "Asia", asia, AMBER, 34, st="ital")]
    els += [arrow([[(lx0 + lx1) / 2 - 60, (ly0 + ly1) / 2 + 30], [gx - 20, gy + 70], [cx + rx * .55, cy + ry * .55]], tog - .4, AMBER, 2.5, "inferred", .9),
            arrow([[(ax0 + ax1) / 2 - 40, ay0 + 10], [gx + 40, gy - 110], [cx + rx * .62, cy - ry * .62]], tog - .2, AMBER, 2.5, "inferred", 1.0),
            poly(Lm, "rgba(232,184,122,.2)", AMBER, 2, tog + .6, curve=True, style="inferred"),
            poly(Am, "rgba(232,184,122,.2)", AMBER, 2, tog + .8, curve=True, style="inferred"),
            poly(isle, "rgba(201,193,238,.14)", LILAC, 3.5, tog + 1.4, curve=True, style="claimed"),
            lab(cx, cy - ry - 26, "Atlantis?", tog + 1.8, LILAC, 40, st="ital")]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s12():
    """Plato's city to scale (27 stadia, about 5 km) with its canal to the sea (50 stadia, about 9 km); the plain around it,
    3,000 by 2,000 stadia (about 550 by 370 km), where the city is a dot; hot and cold springs; elephants."""
    sid = "s12"
    t_city, t_canal, t_plain, t_spr, t_ele = T(sid, "A ring city"), T(sid, "a canal"), T(sid, "a plain"), T(sid, "hot and cold"), T(sid, "elephants")
    u = 7.4                                  # units per stadion at the city
    ccx, ccy = 300, 272
    els = [box(110, 640, 460, 150, DEEP, r=0, at=.2), wave(110, 570, 640, .2, "#bfe6f5", 6, 10, 2, .8), lab(140, 690, "sea", .4, BLUE, 26, "start"),
           box(110, 120, 460, 520, "#3a3424", r=0, at=.2, op=.7)]
    for k, (r, col) in enumerate(RINGS):
        els.append({"k": "circle", "x": ccx, "y": ccy, "r": round(r * u, 1), "fill": col, "c": "rgba(245,236,220,.4)", "w": 1, "in": round(t_city + .15 * (5 - k), 2), "fx": "pop"})
    els += [box(ccx - 4, ccy + 13.5 * u, 8, 640 - ccy - 13.5 * u, SEA, r=1, at=t_canal, fx="fill", dur=1.0),
            {"k": "dim", "x1": ccx - 13.5 * u, "y1": ccy - 13.5 * u - 18, "x2": ccx + 13.5 * u, "y2": ccy - 13.5 * u - 18, "t": "5 km", "c": GOLD, "in": t_city + 1.4, "fx": "draw"},
            {"k": "dim", "x1": ccx + 30, "y1": ccy + 13.5 * u + 4, "x2": ccx + 30, "y2": 636, "t": "9 km", "c": BLUE, "in": t_canal + .8, "lx": 30, "upright": True}]
    els += [droplet(ccx - 10, ccy - 2, 14, t_spr, "#ff7a6b"), droplet(ccx + 12, ccy - 2, 14, t_spr + .4, "#7fc4f0")]
    # the plain: 3,000 x 2,000 stadia; the city a dot 50 stadia from the sea
    px0, py0, pw, ph = 760, 175, 840, 560
    k = pw / 3000.0
    dcx, dcy = px0 + pw / 2, py0 + ph - 50 * k
    els += [box(px0, py0 + ph, pw, 50, DEEP, r=0, at=t_plain - .3), wave(px0, px0 + pw, py0 + ph, t_plain - .3, "#bfe6f5", 5, 18, 2, .8),
            box(px0, py0, pw, ph, "rgba(138,160,90,.28)", LAND, 2.5, 4, t_plain, fx="pop"),
            {"k": "dim", "x1": px0, "y1": py0 - 26, "x2": px0 + pw, "y2": py0 - 26, "t": "plain: about 550 km", "c": AMBER, "in": t_plain + .6},
            {"k": "dim", "x1": px0 + pw + 26, "y1": py0, "x2": px0 + pw + 26, "y2": py0 + ph, "t": "370 km", "c": DIM, "in": t_plain + 1.0, "lx": 34},
            dot(dcx, dcy, 3, GOLD, t_plain + .4), ring(dcx, dcy, 26, t_plain + .6, GOLD, 2.5, dur=.4),
            line([[dcx - 18, dcy - 18], [ccx + 74, ccy - 76]], t_plain + .8, GOLD, 1.5, "inferred", .6),
            line([[dcx - 18, dcy + 18], [ccx + 74, ccy + 76]], t_plain + .8, GOLD, 1.5, "inferred", .6),
            ring(ccx, ccy, 104, t_plain + .7, GOLD, 2.5, dur=.6)]
    els += elephant(1030, 470, 120, t_ele) + elephant(1210, 520, 90, t_ele + .3)
    return {"base": "plan", "north": False, "cam": [1, 889, 500], "els": els}


def s13():
    """Socrates: the tale has a great advantage, it is fact, not fiction (a balance tips towards 'fact')."""
    sid = "s13"
    t_s, t_adv, t_fact, t_fic = T(sid, "Socrates"), T(sid, "great advantage"), T(sid, "fact"), T(sid, "fiction")
    els = [glow(560, 470, 340, .2, .3, "lamp"), person(560, 690, 230, t_s - .3, BONE), lab(560, 744, "Socrates", t_s + .2, BONE, 30),
           poly([[700, 150], [1560, 150], [1560, 600], [840, 600], [760, 660], [790, 600], [700, 600]], "rgba(255,248,232,.06)", BONE, 3, t_adv - .4, fx="pop")]
    bx, by = 1130, 470
    beam = [[bx - 280, by - 46], [bx + 280, by + 46]]       # tipped: the 'fact' side (right) lower
    els += [poly([[bx - 30, 560], [bx + 30, 560], [bx, by]], "#8a6a48", at=t_adv + .2), line(beam, t_adv + .3, GOLD, 6, dur=.6),
            line([[bx - 280, by - 46], [bx - 280, by - 6]], t_adv + .5, DIM, 2, draw=False), line([[bx + 280, by + 46], [bx + 280, by + 86]], t_adv + .5, DIM, 2, draw=False),
            line([[bx - 360, by - 6], [bx - 200, by - 6]], t_adv + .5, DIM, 4, draw=False), line([[bx + 200, by + 86], [bx + 360, by + 86]], t_adv + .5, DIM, 4, draw=False)]
    els += [box(bx + 210, by - 8, 140, 90, "rgba(242,201,142,.2)", GOLD, 3, 8, t_fact, fx="pop"), lab(bx + 280, by + 50, "fact", t_fact, GOLD, 34, st="serif"),
            box(bx - 350, by - 100, 140, 90, "rgba(203,188,168,.08)", DIM, 2, 8, t_fic, fx="pop", op=.7), lab(bx - 280, by - 44, "fiction", t_fic, DIM, 30, st="serif"),
            strike(bx - 350, by - 20, bx - 210, by - 92, t_fic + .5, RED, 4)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s14():
    """A painting of animals, standing still; Socrates longs to see his ideal city move as one longs to see painted animals move:
    the deer step out of the frame and walk off."""
    sid = "s14"
    t_city, t_move = T(sid, "ideal city"), T(sid, "move")
    fx0, fy0, fx1, fy1 = 470, 180, 1250, 640
    els = [glow(860, 420, 560, .2, .22, "lamp"),
           box(fx0 + 14, fy0 + 14, fx1 - fx0 - 28, fy1 - fy0 - 28, "#2c3a2a", r=2, at=.6),
           box(fx0 + 14, fy0 + 14, fx1 - fx0 - 28, 220, "#3a4a5a", r=2, at=.6),
           poly([[fx0 + 14, 470], [700, 430], [960, 450], [fx1 - 14, 420], [fx1 - 14, fy1 - 14], [fx0 + 14, fy1 - 14]], "#56653a", at=.7),
           {"k": "rect", "x": fx0, "y": fy0, "w": fx1 - fx0, "h": fy1 - fy0, "r": 6, "fill": "none", "c": "#d8b25a", "sw": 16, "in": .5, "fx": "draw", "dur": 1.4},
           {"k": "rect", "x": fx0 - 10, "y": fy0 - 10, "w": fx1 - fx0 + 20, "h": fy1 - fy0 + 20, "r": 8, "fill": "none", "c": "#8a6a2a", "sw": 3, "in": .9}]
    els += f04._houses(590, 430, 5, t_city, 26, "#e6d6b2") + f04._temple(760, 432, 60, t_city + .3, "#efe6d2")
    deer = [(660, 612, 96), (860, 618, 100), (1060, 612, 96)]
    for k, (x, y, s) in enumerate(deer):
        els += f04._deer(x, y, s, 1.2 + .3 * k, "#c9a87a")
    for k, (x, y, s) in enumerate(deer):
        at = round(t_move + .45 * k, 2)
        els.append(box(x - s * .64, y - s * 1.24, s * 1.28, s * 1.24 + 3, "#56653a", r=6, at=at, dur=.5))
        els += f04._deer(1360 + 120 * k, 700 - 6 * k, s * .9, at + .2, "#e0c08e")
    els.append(line([[1290, 706], [1700, 706]], t_move + .2, "rgba(255,226,190,.3)", 2, draw=False))
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s15():
    """Critias sets the ideal city in ancient Athens and gives it an enemy: a rich sea power grown proud; the villain falls."""
    sid = "s15"
    t_ath, t_enemy, t_sea, t_proud, t_vil = T(sid, "ancient Athens"), T(sid, "an enemy"), T(sid, "sea power"), T(sid, "grown proud"), T(sid, "villain")
    els = [line([[100, 650], [1680, 650]], .2, "rgba(255,226,190,.3)", 2, draw=False),
           poly([[160, 650], [260, 520], [360, 470], [480, 470], [580, 530], [660, 650]], "rgba(242,201,142,.12)", GOLD, 3, .4, fx="rise", curve=True)]
    els += temple_line(410, 470, 120, t_ath - .5, GOLD, "known", 3)
    els += [line([[230, 560], [250, 520], [570, 520], [600, 560]], t_ath, GOLD, 3, dur=.6)]
    els += [person(240 + 46 * k, 650, 70, round(t_ath + .5 + .12 * k, 2), "#e6d6b2") for k in range(6)]
    els += [lab(410, 740, "ancient Athens", t_ath + .2, GOLD, 30)]
    cx, cy = 1280, 560
    els += city_plan(cx, cy, 15, t_enemy, .35, ghost=True)
    els += sum([trireme(1140 + 140 * k, 690, 100, round(t_sea + .2 * k, 2), LILAC, "claimed") for k in range(3)], [])
    els += [crown(cx, 410, 36, t_proud, LILAC), glow(cx, 390, 90, t_proud, .5, "lamp"),
            lab(cx, 770, "Atlantis", t_enemy + .3, LILAC, 32, st="ital")]
    els += [arrow([[1060 - 30 * (k % 2), 470 + 40 * k], [820, 450 + 40 * k], [690, 480 + 40 * k]], round(t_proud + .5 + .15 * k, 2), LILAC, 2.5, "claimed", .8) for k in range(3)]
    els += [strike(cx - 46, 360, cx + 40, 420, t_vil, RED, 5), wave(1080, 1500, 545, t_vil + .4, BLUE, 16, 9, 5, 1.0)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


SHELF_X = 1495


def s16():
    """No older text has been found, in Egypt or in Greece: an empty shelf of wanted scrolls before Plato's two, about 360 BCE."""
    sid = "s16"
    t_eg, t_gr = T(sid, "Egypt"), T(sid, "Greece")
    X = lambda bce: round(160 + (1000 - bce) / 700 * 1460, 1)
    ty = 730
    els = [axis(160, 1620, ty, [(X(1000), "1000 BCE"), (X(800), "800"), (X(600), "600"), (X(400), "400")], .2)]
    els += scroll(X(360) - 30, 600, 70, .5) + scroll(X(360) + 40, 620, 70, .7) + [line([[X(360), 655], [X(360), ty]], .6, GOLD, 2, draw=False),
                                                                             lab(X(360) - 70, 690, "Plato", .9, GOLD, 28, "end")]
    for k in range(8):
        x = 260 + 120 * k + (60 if k >= 4 else 0)
        els += scroll(x, 600, 70, round(.9 + .15 * k, 2), LILAC, "claimed") + [lab(x, 612, "?", round(1.4 + .15 * k, 2), LILAC, 34, st="serif")]
    els += [line([[200, 650], [1220, 650]], .8, "rgba(201,193,238,.5)", 3, "claimed", .8),
            lab(440, 692, "Egypt", t_eg, AMBER, 30), lab(1040, 692, "Greece", t_gr, AMBER, 30)]
    # the Critias, opened large above: blank until the camera comes up to it
    els += [box(1060, 150, 600, 300, PAPY, "#8a6a3e", 2, 10, 1.0, op=.95), box(1040, 140, 26, 320, "#cdb58a", "#8a6a3e", 2, 13, 1.0),
            box(1654, 140, 26, 320, "#cdb58a", "#8a6a3e", 2, 13, 1.0),
            line([[1500, 462], [X(360) + 66, 598]], 1.2, GOLD, 1.5, "inferred", .5), lab(980, 300, "Critias", 1.2, GOLD, 32, "end", st="ital")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s16b_add():
    """The Critias breaks off mid-sentence: its lines write themselves, the last stops halfway; the quill lifts."""
    sid = "s16b"
    t_brk, t_fin = T(sid, "breaks off"), T(sid, "never finished")
    out = []
    for k in range(6):
        out.append({"k": "glyphs", "x": 1100, "y": 172 + 44 * k, "w": 520 if k < 5 else 230, "h": 30, "rows": 1, "cols": 13 if k < 5 else 6, "kind": "latin",
                    "c": "#5a4632", "op": .8, "in": round(.3 + .3 * k, 2), "fx": "draw", "dur": .3, "seed": 3 + 7 * k})
    stop = 1.8 + .35
    out += [line([[1330, 410], [1330, 386]], stop + .2, AMBER, 3, draw=False), lab(1330, 432, "breaks off", t_brk + .6, AMBER, 28),
            poly([[1352, 366], [1442, 256], [1462, 244], [1454, 268], [1364, 376]], "#efe6d2", "#8a6a3e", 1.5, stop + .4, fx="rise"),
            line([[1352, 366], [1344, 378]], stop + .4, "#2a2018", 3, draw=False),
            glow(1360, 300, 260, t_fin, .5, "lamp")]
    return out


def s17():
    """Back in the room: Plato at his table, the two scrolls glowing."""
    els = room(settled=True)
    els += [glow(960, 520, 120, .6, .8, "fire"), glow(1080, 520, 120, 1.0, .8, "fire")]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


# ================================================================== chapter 2: a date at the end of the ice
X18 = lambda bce: round(140 + (11000 - bce) / 11000 * 1500, 1)       # 11,000 BCE .. 1 CE across the panel
A18 = 430


def timeline18(at=.2, settled=False):
    """11,000 BCE to 1 CE: Solon about 590 BCE; Plato's date, 9,000 years earlier, about 9600 BCE."""
    X, y = X18, A18
    ticks = [(X(10000), "10,000 BCE"), (X(8000), "8,000"), (X(6000), "6,000"), (X(4000), "4,000"), (X(2000), "2,000"), (X(0), "1 CE")]
    return [axis(140, 1640, y, ticks, at)]


def s18():
    sid = "s18"
    X, y = X18, A18
    t_war, t_sol, t_96, t_rnd = T(sid, "put the war"), T(sid, "Solon's visit"), T(sid, "about ninety six hundred"), T(sid, "round number")
    arc = [[round(X(590) - 20 - (X(590) - 20 - X(9600)) * u, 1), round(y - 70 - 190 * math.sin(math.pi * u), 1)] for u in [k / 24 for k in range(25)]]
    els = timeline18(.2)
    els += [person(X(590), y, 100, t_war, BONE), lab(X(590) + 34, y - 64, "Solon", t_sol, BONE, 28, "start"),
            {"k": "arrow", "p": arc + [[X(9600), y - 14]], "c": AMBER, "w": 3, "style": "claimed", "curve": True, "fx": "draw", "dur": 1.6, "in": t_war + .4},
            lab(945, 196, "9,000 years", t_war + 1.2, AMBER, 46, st="serif", fx="rise"),
            dot(X(9600), y, 11, AMBER, t_96), lab(X(9600) - 22, y - 40, "Plato's date", t_96 + .2, AMBER, 28, "end"),
            glow(915, 180, 64, t_rnd, .7, "lamp"), glow(945, 180, 50, t_rnd + .15, .6, "lamp")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def s20_add():
    """A magnifier on 10,000 to 9,400 BCE: the end of the cold snap, about 9700 BCE, give or take 99 years; Plato's date at the edge."""
    sid = "s20"
    X = X18
    X2 = lambda bce: round(190 + (10000 - bce) / 600 * 870, 1)
    t_97, t_cen, t_pl, t_edge = T(sid, "ninety seven hundred"), T(sid, "give or take"), T(sid, "Plato's date"), T(sid, "edge")
    y0, y1, ay = 555, 785, 712
    out = [box(150, y0, 950, y1 - y0, "rgba(13,11,9,.88)", BONE, 2, 10, .3, fx="pop"),
           line([[150, y0], [X(10000), A18 + 8]], .5, BONE, 1.5, "inferred", .5), line([[1100, y0], [X(9400), A18 + 8]], .5, BONE, 1.5, "inferred", .5),
           box(X(10000), A18 - 10, X(9400) - X(10000), 20, "none", BONE, 2, 3, .4),
           line([[X2(10000), ay], [X2(9400), ay]], .8, "#e9dccb", 2, dur=.6)]
    out += [line([[X2(b), ay - 8], [X2(b), ay + 8]], .9, "#e9dccb", 1.6, draw=False) for b in (10000, 9900, 9800, 9700, 9600, 9500, 9400)]
    out += [lab(X2(10000), ay + 40, "10,000 BCE", 1.0, DIM, 26, "start"), lab(X2(9400), ay + 40, "9,400 BCE", 1.0, DIM, 26, "end"),
            dot(X2(9700), ay, 11, BLUE, t_97), lab(X2(9700), ay - 66, "cold snap ends", t_97 + .2, BLUE, 28),
            box(X2(9799), ay - 40, X2(9601) - X2(9799), 40, "rgba(159,208,255,.28)", BLUE, 1.5, 3, t_cen, fx="pop"),
            dot(X2(9600), ay, 11, AMBER, t_pl), lab(X2(9600) + 24, ay - 66, "Plato's date", t_pl + .2, AMBER, 28, "start")]
    out += bracket(X2(9700), X2(9600), ay + 22, t_edge, None, BONE, up=False) + [lab((X2(9700) + X2(9600)) / 2, ay + 58, "100 years", t_edge + .3, BONE, 26)]
    return out


def s19():
    """Greenland's ice piles up year on year like the pages of a diary: a drill on the ice sheet, the core laid out, its yearly layers."""
    sid = "s19"
    t_yr, t_pg = T(sid, "year on year"), T(sid, "like pages")
    dome = [[120, 470], [260, 360], [480, 270], [889, 226], [1300, 270], [1520, 360], [1660, 470]]
    els = [box(80, 470, 1620, 60, "#4a3c34", r=0, at=.2),
           poly(dome + [[1660, 470], [120, 470]], "#dfeaf2", "#ffffff", 2, .3, fx="rise", curve=True),
           lab(230, 250, "Greenland", .6, BLUE, 32, st="ital", a="start")]
    for k in range(5):                       # the yearly layers inside the ice, piled up
        els.append(line([[400 + 40 * (4 - k), 320 + 34 * k], [1378 - 40 * (4 - k), 320 + 34 * k]], round(t_yr + .15 * k, 2), "#9fb8c8", 2, dur=.5))
    els += [line([[862, 226], [889, 140], [916, 226]], .9, "#e8c35a", 3, dur=.5), line([[872, 196], [906, 196]], 1.0, "#e8c35a", 2, draw=False),
            line([[878, 170], [900, 170]], 1.0, "#e8c35a", 2, draw=False), line([[889, 226], [889, 460]], 1.4, "#cfe6ff", 2, "inferred", .8),
            arrow([[900, 470], [1000, 540], [1160, 580]], t_pg - .9, "#cfe6ff", 2, "inferred", .6)]
    x0, x1, cy, n = 200, 1580, 630, 60
    w = (x1 - x0) / n
    els += [box(x0 - 6, cy - 36, x1 - x0 + 12, 72, "#cfe2ee", "#ffffff", 2, 30, t_pg - .6, fx="pop")]
    els += [box(round(x0 + w * k, 1), cy - 30, round(w * .52, 1), 60, "#8eaabd", r=0, at=round(t_pg + .05 * k, 2)) for k in range(n)]
    mx = x0 + w * 30
    els += magnifier(mx + w * .5, cy, 74, t_pg + 3.2, BONE)
    els += bracket(mx, mx + w, cy - 46, t_pg + 3.6, None, BLUE, up=False) + [lab(mx + w / 2, cy - 64, "one year", t_pg + 3.8, BLUE, 30)]
    els += [lab(x0, cy + 74, "today", t_pg + .3, DIM, 26, "start"), lab(x1, cy + 74, "deeper, older", t_pg + 3.0, DIM, 26, "end")]
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": els}


def s21():
    """The Ice Age: water locked in ice, the sea more than 120 m lower (a forty-storey tower), the shelf dry land. 3 units = 1 m."""
    sid = "s21"
    t_rise, t_cold, t_lock, t_low, t_tow = T(sid, "seas were rising"), T(sid, "coldest point"), T(sid, "locked in ice"), T(sid, "a hundred and twenty"), T(sid, "forty storey")
    Y = lambda m: round(300 - 3 * m, 1)
    prof = [[80, 790], [380, 760], [640, 690], [760, 640], [980, 520], [1180, 410], [1400, 300], [1560, 250], [1700, 232]]
    els = [box(80, Y(0), 1320, 500, SEA, r=0, at=.2, op=.32),
           box(80, Y(-120), 700, 800 - Y(-120), "#2c6688", r=0, at=t_low, op=.9, fx="fill", dur=1.2),
           poly(prof + [[1700, 820], [80, 820]], "#7a6248", "#e9dccb", 2, .3, fx="rise"),
           line([[80, Y(0)], [1400, Y(0)]], .6, BLUE, 3, "inferred", .8), lab(100, Y(0) - 16, "sea today", t_rise, BLUE, 28, "start"),
           poly([[1150, 425], [1230, 330], [1380, 232], [1540, 178], [1700, 160], [1700, 234], [1560, 252], [1400, 302], [1180, 412]], "#e6f0f7", "#ffffff", 2, t_cold, fx="fill", dur=1.4, curve=True),
           lab(1560, 140, "ice sheet", t_cold + .5, "#e6f0f7", 30)]
    els += [arrow([[420 + 160 * k, Y(0) - 6], [560 + 200 * k, 200 - 16 * k], [1250 + 40 * k, 250 - 20 * k]], round(t_lock + .3 * k, 2), "#cfe6ff", 2.5, "inferred", 1.0) for k in range(3)]
    els += [wave(80, 712, Y(-120), t_low + .9, "#bfe6f5", 6, 16, 3, .8), lab(100, Y(-120) + 40, "Ice Age sea", t_low + 1.0, "#cfe6ff", 28, "start"),
            {"k": "dim", "x1": 200, "y1": Y(0) + 4, "x2": 200, "y2": Y(-120) - 4, "t": "120 m", "c": AMBER, "in": t_low + 1.4, "lx": -34},
            poly([[712, Y(-120)], [760, 640], [980, 520], [1180, 410], [1400, 300], [1400, 340], [1180, 450], [980, 560], [760, 680], [700, 700]], AMBER, at=t_low + 2.2, op=.35),
            lab(1110, 590, "dry land", t_low + 2.4, AMBER, 32)]
    els += [box(282, Y(-120) - 360, 60, 360, "#3a3540", "#cbd2d8", 2, 2, t_tow - .3, fx="fill", dur=1.2)]
    els += [line([[290 + 22 * (j % 2), Y(-120) - 9 * (j // 2) - 5], [302 + 22 * (j % 2), Y(-120) - 9 * (j // 2) - 5]], round(t_tow + .4 + .01 * j, 2), "#e8c35a", 3, draw=False, op=.6) for j in range(80)]
    els += [lab(312, Y(0) - 16, "40 storeys", t_tow + .6, "#cbd2d8", 28, "start")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s22():
    """Britain joined to Europe; Java to Borneo: the dry shelves of the Ice Age (outlines schematic)."""
    sid = "s22"
    v = View(-15, 125, -15, 62, (90, 120, 1600, 680))
    pl = lambda pts_, at: poly([v.p(lo, la) for lo, la in pts_], AMBER, AMBER, 2.5, at, op=.32, curve=True, style="inferred")
    dogger = [(-5.5, 50.0), (-1.0, 49.4), (3.0, 50.8), (8.2, 53.2), (9.0, 56.8), (5.0, 58.4), (0.0, 58.0), (-3.0, 56.0)]
    sunda = [(95.0, 6.0), (102.0, 8.5), (108.5, 7.0), (117.0, 6.5), (119.5, 0.0), (117.5, -8.6), (106.0, -8.4), (99.0, -3.5), (94.5, 2.0)]
    t_br, t_jav, t_bor = T(sid, "Britain"), T(sid, "Java"), T(sid, "Borneo")
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(-13.5, 53.5), "Britain", t_br, BONE, 28, "end"), pl(dogger, t_br + .4),
           pl(sunda, t_jav), lab(*v.p(110, -11.5), "Java", t_jav + .1, BONE, 28), lab(*v.p(114.5, 5.5), "Borneo", t_bor, BONE, 28)]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s23():
    """Then the melt took it back: the sea-level curve, 22,000 years ago to today (Lambeck et al. 2014); one pulse of 14 to 18 m in
    350 years (Deschamps et al. 2012); Plato's date marked on the rising curve."""
    sid = "s23"
    t_melt, t_pulse = T(sid, "the melt"), T(sid, "fourteen to eighteen")
    Tx = lambda ya: round(200 + (22000 - ya) / 22000 * 1400, 1)
    Ym = lambda m: round(170 - 4.0 * m, 1)
    pts = [(22000, -125), (19000, -120), (16000, -105), (14600, -95), (14300, -78), (12000, -60), (10000, -40), (8000, -18), (7000, -6), (4000, -1), (0, 0)]
    els = [axis(200, 1600, 700, [(Tx(20000), "20,000 years ago"), (Tx(15000), "15,000"), (Tx(10000), "10,000"), (Tx(5000), "5,000"), (Tx(0), "today")], .2),
           line([[180, Ym(0)], [180, Ym(-130)]], .2, "#e9dccb", 2, draw=False)]
    els += [line([[172, Ym(m)], [188, Ym(m)]], .2, "#e9dccb", 1.6, draw=False) for m in (0, -50, -100)]
    els += [lab(160, Ym(0) + 8, "0", .3, DIM, 26, "end"), lab(160, Ym(-50) + 8, "50 m", .3, DIM, 26, "end"), lab(160, Ym(-100) + 8, "100 m", .3, DIM, 26, "end"),
            lab(200, 136, "below today's sea", .4, DIM, 26, "start"),
            line([[180, Ym(0)], [1600, Ym(0)]], .4, BLUE, 2, "inferred", .8), lab(1600, Ym(0) - 16, "sea today", .6, BLUE, 28, "end"),
            {"k": "line", "p": [[Tx(a), Ym(m)] for a, m in pts], "c": SEA, "w": 6, "curve": True, "in": t_melt, "fx": "draw", "dur": 2.4},
            {"k": "line", "p": [[Tx(14600), Ym(-95)], [Tx(14450), Ym(-86.5)], [Tx(14300), Ym(-78)]], "c": AMBER, "w": 12, "in": t_pulse, "fx": "draw", "dur": .5},
            glow(Tx(14450), Ym(-86), 80, t_pulse, .9, "lamp"), lab(Tx(14450) + 40, Ym(-86) + 2, "14 to 18 m", t_pulse + .5, AMBER, 30, "start"), lab(Tx(14450) + 40, Ym(-86) + 38, "in 350 years", t_pulse + .7, AMBER, 30, "start"),
            line([[Tx(11600) - 14, Ym(-56) + 14], [Tx(11600) + 14, Ym(-56) - 14]], t_pulse + 2.4, AMBER, 4, draw=False),
            lab(Tx(11600) - 20, Ym(-56) - 22, "Plato's date", t_pulse + 2.5, AMBER, 26, "end")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def _proj(e, p, t=0.0):
    """Where an iso world point lands on the panel (the iso element e, at time t of its spin)."""
    az = math.radians(e.get("az", 35) + e.get("spin", 0) * t); ca, sa = math.cos(az), math.sin(az)
    x, y, z = p; rx, rz = x * ca - z * sa, x * sa + z * ca
    S, el, C30 = e.get("s", 4), e.get("el", .32), math.cos(math.pi / 6)
    return round(e["x"] + (rx - rz) * C30 * S, 1), round(e["y"] - y * S + (rx + rz) * el * S, 1)


def _iso_from(short_shot, drop=("label", "person"), **kw):
    e = copy.deepcopy(next(x for x in short_shot["els"] if x.get("k") == "iso"))
    e["items"] = [it for it in e["items"] if it.get("t") not in drop]
    e.update(kw)
    return e


def s24():
    """Off Israel, Atlit Yam: seven standing stones around a spring, now ten metres down (the Short's model, redrawn wide)."""
    sid = "s24"
    t_isr, t_st, t_spr, t_10 = T(sid, "off Israel"), T(sid, "seven standing"), T(sid, "around a spring"), T(sid, "ten metres")
    iso = _iso_from(f04.drowned_coasts()["shots"][2], x=889, y=560, s=10, az=-24, spin=0, el=.5, **{"in": .2})
    iso["items"] += [f04.water(-28, 28, -22, 22, 10.0, op=.22, over=6),
                     {"t": "line", "p": [[28, 0, 22], [28, 10, 22]], "c": "#cfe6ff", "w": 2},
                     {"t": "line", "p": [[26, 10, 22], [30, 10, 22]], "c": "#cfe6ff", "w": 2}, {"t": "line", "p": [[26, 0, 22], [30, 0, 22]], "c": "#cfe6ff", "w": 2}]
    stones = [_proj(iso, (14 * math.cos(2 * math.pi * k / 7), 8, 14 * math.sin(2 * math.pi * k / 7))) for k in range(7)]
    wx, wy = _proj(iso, (0, 0, 0))
    dx, dy = _proj(iso, (28, 5, 22))
    els = [iso, lab(889, 150, "Atlit Yam", t_isr, AMBER, 34), lab(889, 188, "about 8,500 years old", t_isr + .3, DIM, 26)]
    els += [glow(x, y, 46, round(t_st + .12 * k, 2), .8, "lamp") for k, (x, y) in enumerate(stones)]
    els += [glow(wx, wy, 80, t_spr, .9, "lamp"), lab(dx + 26, dy + 10, "10 m", t_10, "#cfe6ff", 30, "start"), f04._diver(1080, 330, 80, .8)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


X25 = lambda bce: round(140 + (10400 - bce) / 10400 * 1500, 1)
A25 = 520


def flint(x, y, s, at, c=BONE):
    return poly([[x - s * .12, y], [x - s * .2, y - s * .5], [x, y - s], [x + s * .2, y - s * .5], [x + s * .12, y]], c, "#8a7a66", 1.5, at, fx="pop")


def wheat(x, y, s, at, c="#e8c35a"):
    out = [line([[x, y], [x, y - s]], at, c, 3, draw=False)]
    for k in range(5):
        yy = y - s * (.45 + .11 * k)
        out += [oval(x - s * .07, yy, s * .07, s * .035, c, at=at), oval(x + s * .07, yy - s * .03, s * .07, s * .035, c, at=at)]
    return out


def axe(x, y, s, at, c=BRONZE):
    """A bronze axe: a shaft and a flared blade."""
    return [line([[x - s * .25, y], [x + s * .2, y - s]], at, "#8a6a44", 6, draw=False),
            poly([[x + s * .1, y - s * .78], [x + s * .5, y - s * .98], [x + s * .56, y - s * .7], [x + s * .5, y - s * .44], [x + s * .2, y - s * .62]], c, "#f4c890", 1.5, at, fx="pop", curve=True)]


def s25():
    """At Plato's date people everywhere worked stone, not metal; fully tamed crops about a thousand years later, bronze about six
    thousand (Larson et al. 2014): a bronze-walled empire at 9600 BCE is struck out."""
    sid = "s25"
    X, y = X25, A25
    t_fl, t_not, t_st, t_cr, t_th, t_br, t_six = (T(sid, "real flood"), T(sid, "not on a real"), T(sid, "worked stone"), T(sid, "Fully tamed"),
                                                  T(sid, "a thousand years"), T(sid, "bronze"), T(sid, "six thousand"))
    ticks = [(X(10000), "10,000 BCE"), (X(8000), "8,000"), (X(6000), "6,000"), (X(4000), "4,000"), (X(2000), "2,000"), (X(0), "1 CE")]
    els = [axis(140, 1640, y, ticks, .2, below=False),
           dot(X(9600), y, 11, AMBER, .5), lab(X(9600), y + 40, "9600 BCE", .6, AMBER, 26),
           wave(X(9600) - 60, X(9600) + 60, 372, t_fl, BLUE, 10, 3, 4, .6), wave(X(9600) - 60, X(9600) + 60, 392, t_fl + .2, BLUE, 10, 3, 4, .6)]
    gx = X(9600)
    ghost = [line([[gx - 70, 300], [gx - 70, 220], [gx + 70, 220], [gx + 70, 300]], t_not, LILAC, 3, "claimed", draw=False),
             line([[gx - 70, 240], [gx - 50, 240], [gx - 50, 220]], t_not, LILAC, 3, "claimed", draw=False),
             line([[gx + 50, 220], [gx + 50, 240], [gx + 70, 240]], t_not, LILAC, 3, "claimed", draw=False),
             {"k": "poly", "p": [[gx - 34, 196], [gx - 34, 166], [gx - 17, 182], [gx, 160], [gx + 17, 182], [gx + 34, 166], [gx + 34, 196]], "fill": "none", "c": LILAC, "w": 3,
              "style": "claimed", "in": t_not + .2}]
    els += ghost + [strike(gx - 90, 310, gx + 90, 150, t_not + 1.0, RED, 5)]
    els += [flint(X(9600), y - 46, 64, t_st)]
    els += wheat(X(8500), y - 40, 76, t_cr) + bracket(X(9600), X(8500), y + 80, t_th, None, AMBER, up=True) + [lab((X(9600) + X(8500)) / 2, y + 114, "about 1,000 years", t_th + .3, AMBER, 26)]
    els += axe(X(3300), y - 40, 80, t_br) + bracket(X(9600), X(3300), y + 160, t_six, None, BRONZE, up=True) + [lab((X(9600) + X(3300)) / 2, y + 194, "about 6,000 years", t_six + .3, BRONZE, 26)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s26_add():
    """Atlantis keeps triremes in its docks: the warship of Plato's own day (about 500 to 300 BCE)."""
    sid = "s26"
    X, y = X25, A25
    t_tri, t_own = T(sid, "triremes"), T(sid, "own day")
    out = trireme(560, 320, 280, t_tri - .2, "#c9a370", fx="rise") + [lab(560, 196, "trireme", t_tri + .3, AMBER, 30)]
    out += [bar(X(500), X(300), y, t_own - .8, AMBER, 16, .6), dot(X(360), y, 9, GOLD, t_own - .5), lab(X(360), y + 40, "Plato", t_own - .4, GOLD, 26),
            arrow([[730, 320], [1200, 340], [X(400), y - 20]], t_own - .9, AMBER, 2.5, "inferred", 1.0)]
    return out


def s26b_add():
    """The rising sea is real (the measured curve, solid); the fleet is Plato's (the trireme turns to a dotted outline)."""
    sid = "s26b"
    t_sea, t_fl = T(sid, "rising sea"), T(sid, "fleet")
    Tx = lambda ya: round(860 + (22000 - ya) / 22000 * 330, 1)
    Ym = lambda m: round(200 - .9 * m, 1)
    pts = [(22000, -125), (16000, -105), (14600, -95), (14300, -78), (12000, -60), (10000, -40), (8000, -18), (7000, -6), (0, 0)]
    out = [box(830, 160, 390, 160, "rgba(13,11,9,.6)", "rgba(159,208,255,.4)", 1.5, 10, t_sea - .2),
           {"k": "line", "p": [[Tx(a), Ym(m)] for a, m in pts], "c": BLUE, "w": 5, "curve": True, "in": t_sea, "fx": "draw", "dur": .9},
           glow(1025, 260, 200, t_sea + .3, .45, "lamp"), lab(1025, 352, "real", t_sea + .6, BLUE, 28)]
    out += [glow(560, 290, 200, t_fl, .35, "lamp")] + trireme(560, 320, 300, t_fl + .2, LILAC, "claimed") + [lab(560, 382, "Plato's", t_fl + .5, LILAC, 30)]
    return out


# ================================================================== chapter 3: no room on the sea floor
SURF = 300
ST27 = [300, 470, 640, 810, 980, 1150, 1320, 1490]          # Donnelly's soundings: eight stations across the North Atlantic
DEP27 = [700, 640, 520, 420, 430, 540, 650, 700]


def ocean_base(at=-1):
    """The North Atlantic in section: America left, Europe and Africa right, the water between."""
    return [box(80, SURF, 1620, 500, "#163142", r=0, at=at),
            poly([[80, 250], [200, 252], [236, SURF], [262, 620], [300, 800], [80, 800]], "#6f5a44", "#c9ad85", 2, at),
            poly([[1700, 250], [1580, 252], [1544, SURF], [1520, 620], [1480, 800], [1700, 800]], "#6f5a44", "#c9ad85", 2, at),
            lab(150, 520, "America", at, "#e9dccb", 26), lab(1630, 520, "Europe", at, "#e9dccb", 26),
            wave(236, 1544, SURF, at, "#bfe6f5", 5, 30, 2, .8)]


def floor27(at, fill="#4a3c34", op=1):
    pts = [[262, 620]] + [[x, d] for x, d in zip(ST27, DEP27)][:3] + [[840, 300], [870, 390], [930, 296], [960, 410]] + [[x, d] for x, d in zip(ST27, DEP27)][4:] + [[1520, 620]]
    return poly(pts + [[1480, 800], [300, 800]], fill, "#cbbca8", 2, at, op=op, curve=False)


def s27():
    """Donnelly, 1882: a ship lowers weighted lines at eight stations; the floor rises in the middle; two peaks break the surface: the Azores."""
    sid = "s27"
    t_sh, t_ri, t_mid, t_pk, t_az = T(sid, "Ships lowering"), T(sid, "great ridge"), T(sid, "middle of the Atlantic"), T(sid, "peaks breaking"), T(sid, "Azores")
    els = ocean_base()
    els += [person(150, 252, 92, .4, "#d9c7a6"), box(186, 168, 56, 38, "#efe6d2", "#8a6a48", 2, 3, .6, fx="pop"), line([[214, 168], [214, 206]], .7, "#8a6a48", 2, draw=False),
            lab(110, 146, "Donnelly, 1882", .8, AMBER, 30, "start")]
    els += sailship(ST27[0], SURF, 36, t_sh - .3)
    els += [line([[ST27[0] + 40, SURF - 8], [ST27[-1], SURF - 8]], t_sh, BONE, 2, "inferred", 3.6)]
    for k, (x, d) in enumerate(zip(ST27, DEP27)):
        at = round(t_sh + .2 + .45 * k, 2)
        els += [line([[x, SURF + 4], [x, d - 8]], at, DIM, 1.5, dur=.4), dot(x, d, 8, GOLD, at + .4)]
    els += [line([[x, d] for x, d in zip(ST27, DEP27)], t_ri + .2, GOLD, 3, "inferred", 1.2, curve=True),
            floor27(t_mid, "#4a3c34", .85),
            poly([[812, SURF + 2], [840, 286], [866, SURF + 2]], "#8a7458", "#e9dccb", 2, t_pk, fx="pop"),
            poly([[906, SURF + 2], [930, 290], [954, SURF + 2]], "#8a7458", "#e9dccb", 2, t_pk + .2, fx="pop"),
            lab(886, 252, "Azores", t_az, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s28_add():
    """Donnelly read the rise as the drowned spine of Atlantis (the claim dotted); his soundings were real (they glow)."""
    sid = "s28"
    t_at, t_back = T(sid, "spine of Atlantis"), T(sid, "Back then")
    shape = [[560, 640], [620, 420], [720, 330], [889, 312], [1060, 330], [1160, 420], [1220, 640]]
    out = [poly(shape, "rgba(201,193,238,.22)", LILAC, 3, t_at - 1.0, curve=True, style="claimed"),
           lab(889, 470, "Atlantis?", t_at, LILAC, 40, st="ital")]
    out += [glow(x, d, 44, round(t_back + .12 * k, 2), .9, "lamp") for k, (x, d) in enumerate(zip(ST27, DEP27))]
    return out


def fine_floor():
    r = random.Random(11)
    pts = []
    for x in range(270, 1515, 10):
        base = 700 - 290 * math.exp(-((x - 889) / 330) ** 2)
        if abs(x - 889) < 34:
            base += 60 * (1 - abs(x - 889) / 34)            # the rift valley down the crest
        pts.append([x, round(base + r.uniform(-12, 12) + 10 * math.sin(x / 23), 1)])
    return pts


def s29():
    """Then ships mapped the floor with sound: a ping goes down, the echo comes back and is timed (like shouting into a well);
    ping by ping, the floor appears in fine detail: one long rugged ridge with a valley down its crest."""
    sid = "s29"
    t_png, t_ech, t_tim, t_well, t_cnt = T(sid, "A ping"), T(sid, "the echo"), T(sid, "is timed"), T(sid, "shouting"), T(sid, "counting")
    els = ocean_base()
    els += [floor27(-1, "#3a302a", .7)]
    els += steamer(1150, SURF, 46, .4)
    els += [{"k": "fan", "x": 1150, "y": SURF + 14, "r": 330, "a0": 70, "a1": 110, "n": 9, "c": BLUE, "in": t_png},
            {"k": "fan", "x": 1150, "y": 560, "r": 230, "a0": 250, "a1": 290, "n": 7, "c": AMBER, "in": t_ech}]
    els += [ring(1270, 214, 30, t_tim, BONE, 3, dur=.5), line([[1270, 214], [1270, 194]], t_tim + .2, BONE, 3, draw=False),
            line([[1270, 214], [1286, 222]], t_tim + .5, AMBER, 3, draw=False), box(1264, 176, 12, 8, BONE, r=2, at=t_tim)]
    els += [box(330, 120, 380, 160, "rgba(13,11,9,.85)", "rgba(255,226,190,.4)", 2, 12, t_well - .3, fx="pop"),
            person(420, 260, 90, t_well), line([[446, 196], [480, 206]], t_well + .1, BONE, 2, draw=False),
            box(520, 206, 90, 54, "#5a4a3c", "#a89070", 2, 4, t_well), box(534, 206, 62, 54, "#120e0b", r=2, at=t_well),
            {"k": "line", "p": I.ellipse(565, 230, 22, 10, 16, 20, 160), "c": BLUE, "w": 2, "curve": True, "in": t_well + .4, "fx": "draw", "dur": .4},
            {"k": "line", "p": I.ellipse(565, 246, 30, 12, 16, 20, 160), "c": BLUE, "w": 2, "curve": True, "in": t_well + .7, "fx": "draw", "dur": .4},
            {"k": "line", "p": I.ellipse(565, 200, 26, 10, 16, 200, 340), "c": AMBER, "w": 2, "curve": True, "in": t_cnt, "fx": "draw", "dur": .4},
            {"k": "line", "p": I.ellipse(565, 186, 36, 13, 16, 200, 340), "c": AMBER, "w": 2, "curve": True, "in": t_cnt + .3, "fx": "draw", "dur": .4}]
    els += [{"k": "line", "p": fine_floor(), "c": "#ffcf9a", "w": 3, "in": t_cnt + 1.0, "fx": "draw", "dur": 1.6}]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


MAR = [(-17, 66.0), (-19, 64.0), (-25, 61), (-30, 57.5), (-33, 54), (-35, 52.5), (-30, 50), (-28.5, 45), (-28, 41), (-29, 38.5), (-33, 35), (-38, 31),
       (-41.5, 27), (-44.5, 23), (-46, 18), (-45.5, 14), (-43, 10), (-38, 7.5), (-33, 4.5), (-27, 1.5), (-20, 0), (-14, -1.5), (-13, -5), (-13.5, -10),
       (-14, -15), (-13, -20), (-13, -25), (-14, -30), (-15, -35), (-16, -40), (-17, -45), (-15, -50), (-12, -54)]


def s30():
    """Ping by ping, a map: the Mid-Atlantic Ridge, one long ridge snaking down the whole Atlantic between the coasts (path schematic)."""
    sid = "s30"
    v = View(-80, 20, -55, 65, (90, 120, 1600, 680))
    t_rid = T(sid, "one long ridge")
    pts = [list(v.p(lo, la)) for lo, la in MAR]
    lx, ly = v.p(-37, 30)
    els = [{"k": "map", "land": v.land(), "in": -1},
           {"k": "line", "p": pts, "c": "#ff9a7a", "w": 5, "curve": True, "in": .5, "fx": "draw", "dur": 2.6},
           {"k": "line", "p": pts, "c": "#ffcf9a", "w": 14, "curve": True, "op": .25, "keepop": True, "in": 2.6},
           line([[lx - 8, ly], [560, 300]], t_rid, BONE, 1.5, "inferred", .5), lab(560, 288, "Mid-Atlantic Ridge", t_rid + .3, "#ffb09a", 32, "end")]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s31():
    """1968, a drilling ship samples the floor: young rock at the ridge, older and older on either side (mirror symmetry)."""
    sid = "s31"
    t_ship, t_young, t_old = T(sid, "a drilling ship"), T(sid, "young rock"), T(sid, "older and older")
    S0 = 280
    fy = lambda x: round(470 + abs(x - 889) / 740 * 170 + (40 * (1 - abs(x - 889) / 36) if abs(x - 889) < 36 else 0), 1)
    prof = [[x, fy(x)] for x in range(150, 1631, 20)]
    cols = ["#efe2c4", "#d9bb8a", "#b48d5e", "#8a6a44", "#6a4f34", "#4d3a28"]
    els = [box(80, S0, 1620, 520, "#163142", r=0, at=-1), wave(80, 1700, S0, -1, "#bfe6f5", 5, 36, 2, .8),
           poly(prof + [[1630, 800], [150, 800]], "#3a302a", "#cbbca8", 2, -1)]
    for k in range(6):                                        # the floor's ages, in mirror-image bands either side of the crest
        w = 125
        for sgn in (-1, 1):
            xa = 889 + sgn * w * k; xb = 889 + sgn * w * (k + 1)
            band = [[xa, fy(xa) + 4]] + [[x, fy(x) + 4] for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1, 20)][::sgn] + [[xb, fy(xb) + 4], [xb, 800], [xa, 800]]
            band = [[xa, fy(xa) + 4], [xb, fy(xb) + 4], [xb, 800], [xa, 800]]
            els.append(poly(band, cols[k], at=round(t_young + .2 + .25 * k, 2), op=.55))
    els += drillship(889, S0, 60, t_ship - .3) + chip(1060, S0 - 90, "1968", t_ship, AMBER, 28)
    order = [1, -1, 2, -2, 3, -3]
    for k, m in enumerate(order):
        x = 889 + m * 220; at = round(t_ship + .9 + .35 * k, 2)
        els += [line([[x, S0 + 6], [x, fy(x) + 50]], at, "#e8c35a", 2, dur=.4), box(x - 16, fy(x) + 34, 32, 32, cols[abs(m) * 2 - 1], "#fff6e6", 1.5, 4, at + .35, fx="pop")]
    els += [lab(889, 420, "young", t_young, "#efe2c4", 30), lab(250, 470, "older", t_old, "#d9bb8a", 30), lab(1528, 470, "older", t_old + .3, "#d9bb8a", 30)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s32():
    """The ridge is not a sunken land: new sea floor is born there. Lava wells up, cools, is pushed aside on two conveyor belts,
    about 2.5 cm a year; fingernails grow about 4 cm a year (Yaemsiri et al. 2010)."""
    sid = "s32"
    t_born, t_lava, t_cool, t_push, t_belt, t_cm, t_nail = (T(sid, "is born"), T(sid, "Lava wells"), T(sid, "cools into"),
                                                                   T(sid, "pushed aside"), T(sid, "conveyor belts"), T(sid, "two and a half"), T(sid, "fingernails"))
    WAT = "#18323f"
    els = [box(0, 0, W_, 380, WAT, r=0, at=-1), wave(0, W_, 130, -1, "#bfe6f5", 5, 40, 2, .8),
           box(0, 380, W_, 150, "#4a3c34", "rgba(255,226,190,.3)", 1.5, 0, -1),
           box(0, 530, W_, 300, "#7a3a1e", r=0, at=-1, op=.85), lab(300, 690, "hot rock below", .3, "#ffb08a", 28, "start")]
    ghost = [[560, 380], [640, 250], [760, 200], [889, 186], [1020, 200], [1140, 250], [1220, 380]]
    els += [poly(ghost, "rgba(201,193,238,.22)", LILAC, 3, -1, curve=True, style="claimed"), lab(889, 300, "Atlantis?", -1, LILAC, 34, st="ital"),
            poly([[540, 382], [630, 236], [760, 182], [889, 168], [1020, 182], [1150, 236], [1240, 382]], WAT, at=t_born - .2, dur=1.2, curve=True)]
    els += [box(869, 380, 40, 400, "#ff6a2a", r=4, at=t_born, fx="fill", dur=1.2), glow(889, 420, 160, t_born + .6, .9, "red"),
            glow(889, 600, 220, t_lava, .7, "fire")]
    stripes = []
    for k in range(9):
        for sgn in (-1, 1):
            x0 = 889 + sgn * (20 + 70 * k)
            stripes.append(box(min(x0, x0 + sgn * 70), 380, 70, 150, "#6a5446" if k % 2 else "#8a7462", "rgba(255,226,190,.25)", 1, 0, round(t_belt + .2 * k, 2), fx="pop"))
    els += [box(849, 380, 20, 150, "#a05a3a", r=0, at=t_cool, fx="pop"), box(909, 380, 20, 150, "#a05a3a", r=0, at=t_cool, fx="pop")] + stripes
    for sgn in (-1, 1):
        xa, xb = 889 + sgn * 70, 889 + sgn * 640
        lo, hi = min(xa, xb), max(xa, xb)
        els += [box(lo, 552, hi - lo, 44, "none", AMBER, 3, 22, t_belt), ring(lo + 22, 574, 16, t_belt, AMBER, 3, dur=.3), ring(hi - 22, 574, 16, t_belt, AMBER, 3, dur=.3),
                arrow([[xa, 548], [xb, 548]], t_push, AMBER, 5, dur=.8, curve=False)]
    bx, by = 1200, 150
    k = 70
    els += [box(bx - 20, by - 26, 500, 210, "rgba(13,11,9,.88)", "rgba(255,226,190,.35)", 2, 12, t_cm - .4, fx="pop"),
            line([[bx, by + 150], [bx + 5 * k, by + 150]], t_cm - .2, "#e9dccb", 2, draw=False)]
    els += [line([[bx + k * c, by + 140], [bx + k * c, by + 160]], t_cm - .2, "#e9dccb", 1.6, draw=False) for c in range(6)]
    els += [lab(bx, by + 184, "0", t_cm - .1, DIM, 24), lab(bx + 5 * k, by + 184, "5 cm", t_cm - .1, DIM, 24),
            bar(bx, bx + 2.5 * k, by + 40, t_cm + .3, AMBER, 22, 1.0), lab(bx + 2.5 * k + 14, by + 48, "sea floor", t_cm + 1.0, AMBER, 26, "start"),
            bar(bx, bx + 4.0 * k, by + 96, t_nail, "#f0e2cc", 22, 1.0), lab(bx + 4.0 * k + 14, by + 104, "nail", t_nail + .8, "#f0e2cc", 26, "start"),
            lab(bx + 240, by - 2, "in a year", t_cm + .5, BONE, 26)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def pitch(x, y, w, h, at):
    m = w / 105.0
    c = "rgba(245,236,220,.75)"
    return [box(x, y, w, h, "#365f34", c, 2, 0, at, fx="pop"),
            line([[x + w / 2, y], [x + w / 2, y + h]], at + .1, c, 2, draw=False),
            {"k": "circle", "x": round(x + w / 2, 1), "y": round(y + h / 2, 1), "r": round(9.15 * m, 1), "fill": "none", "c": c, "w": 2, "in": at + .1},
            box(x, y + h / 2 - 20.15 * m, 16.5 * m, 40.3 * m, "none", c, 2, 0, at + .1), box(x + w - 16.5 * m, y + h / 2 - 20.15 * m, 16.5 * m, 40.3 * m, "none", c, 2, 0, at + .1)]


def s33():
    """Since Plato's date the Atlantic has widened about 290 m (2.5 cm a year for about 11,600 years): a bar over three football
    pitches to the same scale (4.5 units = 1 m; a person, 1.7 m, is a speck)."""
    sid = "s33"
    t_wid, t_300 = T(sid, "widened"), T(sid, "three hundred")
    m = 4.5
    pw, ph = 105 * m, 68 * m
    els = []
    for k in range(3):
        els += pitch(160 + pw * k, 330, pw, ph, round(.3 + .2 * k, 2))
    x1 = 160 + 290 * m
    els += [lab(160, 210, "2.5 cm a year", .9, DIM, 26, "start"), lab(380, 210, "for 11,600 years", 1.1, DIM, 26, "start"),
            bar(160, x1, 268, t_wid - .6, AMBER, 30, 2.4), line([[x1, 240], [x1, 650]], t_300 - .2, AMBER, 2, "inferred", .5),
            lab(x1 + 16, 278, "about 300 m", t_300, AMBER, 34, "start"),
            person(150, 330 + ph, 1.7 * m, 1.0, BONE), ring(150, 330 + ph - 4, 14, 1.2, BONE, 2, dur=.4), lab(176, 330 + ph + 40, "a person", 1.4, DIM, 24, "start")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s34():
    """Continental crust is light and about 41 km thick; ocean crust heavy basalt, about 7 km (Christensen & Mooney 1995;
    White et al. 1992). Both float on the mantle; the thick block rides high, as a thick wooden block floats higher than a plank.
    To scale: 10 units = 1 km (the ocean 4.5 km deep)."""
    sid = "s34"
    t_cont, t_40, t_oc, t_7, t_float, t_high, t_wood, t_plank = (T(sid, "Continental rock"), T(sid, "forty kilometres"), T(sid, "ocean floor"), T(sid, "about seven"),
                                                                  T(sid, "Both float"), T(sid, "rides high"), T(sid, "block of wood"), T(sid, "thin plank"))
    sea, ctop, cbot, ofl, obot, xm = 330, 322, 732, 375, 445, 860
    els = [box(xm, sea, 1660 - xm, ofl - sea, SEA, r=0, at=-1, op=.85), wave(xm, 1660, sea, -1, "#bfe6f5", 4, 20, 2, .8),
           line([[120, sea], [1660, sea]], -1, BLUE, 1.5, "inferred", .5), lab(1650, sea - 14, "sea level", .3, BLUE, 26, "end"),
           box(120, ctop, xm - 120, cbot - ctop, "#c9a878", "#f0dcb8", 2, 2, t_cont - .6, fx="rise"), lab(490, 520, "continent", t_cont, "#3a2a1a", 34, halo=False),
           {"k": "dim", "x1": 170, "y1": ctop, "x2": 170, "y2": cbot, "t": "40 km", "c": "#3a2a1a", "in": t_40, "lx": 0, "ly": 0, "fx": "draw"},
           box(xm, ofl, 1660 - xm, obot - ofl, "#4a4a50", "#a0a0a8", 2, 2, t_oc, fx="rise"), lab(1180, 420, "ocean crust", t_oc + .3, "#e9e9ee", 28),
           {"k": "dim", "x1": 1600, "y1": ofl, "x2": 1600, "y2": obot, "t": "7 km", "c": BONE, "in": t_7, "lx": -56, "ly": 8, "upright": True},
           poly([[120, cbot], [xm, cbot], [xm, obot], [1660, obot], [1660, 790], [120, 790]], "#b8562a", at=t_float, op=.75),
           lab(1180, 640, "mantle: hot rock", t_float + .4, "#ffd0b0", 30),
           glow(490, ctop, 200, t_high, .5, "lamp")]
    bx, by = 1180, 128
    els += [box(bx, by, 470, 170, "rgba(13,11,9,.9)", "rgba(255,226,190,.4)", 2, 12, t_wood - .5, fx="pop"),
            box(bx + 20, by + 80, 430, 80, SEA, r=4, at=t_wood - .4, op=.85), wave(bx + 20, bx + 450, by + 80, t_wood - .4, "#bfe6f5", 3, 10, 2, .5),
            box(bx + 70, by + 28, 110, 100, "#b88a50", "#f0d0a0", 2, 3, t_wood, fx="pop"),
            box(bx + 270, by + 70, 150, 24, "#b88a50", "#f0d0a0", 2, 3, t_plank, fx="pop"),
            line([[bx + 125, by + 130], [600, ctop + 10]], t_plank + .5, AMBER, 2, "inferred", .7),
            line([[bx + 345, by + 96], [1350, ofl + 8]], t_plank + .7, AMBER, 2, "inferred", .5)]
    return {"base": "dark", "stars": 20, "cam": [1, 889, 500], "els": els}


def s35():
    """West of Gibraltar: a short shelf, a steep slope, ocean floor 4 to 5 km down on ocean crust; a continent tried in the gap does
    not fit (vertical scale exaggerated: 80 units = 1 km)."""
    sid = "s35"
    t_gib, t_oc, t_45, t_room = T(sid, "Beyond Gibraltar"), T(sid, "ocean crust"), T(sid, "four to five"), T(sid, "no room")
    sl, fl = 220, 580
    prof = [[100, fl + 6], [400, fl - 4], [700, fl + 8], [1000, fl], [1150, fl - 10], [1300, 420], [1400, 250], [1500, 232], [1530, 200]]
    els = [box(80, sl, 1460, 560, "#163142", r=0, at=-1), wave(80, 1530, sl, -1, "#bfe6f5", 5, 30, 2, .8),
           poly([[1530, 160], [1700, 150], [1700, 800], [1450, 800], [1400, 250], [1500, 232], [1530, 200]], "#7a6248", "#e9dccb", 2, t_gib - .3, fx="rise"),
           lab(1610, 142, "Gibraltar", t_gib, BONE, 30)] + f04._pillars(1565, 160, 34, t_gib + .1, "#efe6d2")
    els += [poly(prof + [[1450, 800], [100, 800]], "#3a302a", "#cbbca8", 2, t_oc - .8, fx="rise"),
            poly([[100, fl + 6], [400, fl - 4], [700, fl + 8], [1000, fl], [1150, fl - 10], [1150, 800], [100, 800]], "#4a4a50", at=t_oc - .2, op=.9),
            lab(600, 700, "ocean crust", t_oc, "#e9e9ee", 30), lab(700, 290, "Atlantic", .5, BLUE, 34, st="ital"),
            arrow([[300, 160], [130, 160]], .6, BONE, 3, dur=.5, curve=False), lab(320, 168, "west", .7, BONE, 26, "start"),
            {"k": "dim", "x1": 230, "y1": sl + 4, "x2": 230, "y2": fl - 4, "t": "4 to 5 km", "c": AMBER, "in": t_45, "lx": -34}]
    cont = [[420, fl], [470, 330], [560, 260], [640, 300], [720, 240], [820, 290], [900, 250], [1000, 320], [1060, fl]]
    els += [poly(cont, "rgba(201,193,238,.16)", LILAC, 3, t_room - 1.0, style="claimed"), lab(740, 214, "a continent?", t_room - .8, LILAC, 30, st="ital"),
            strike(420, fl, 1060, 240, t_room + .6, RED, 6), strike(420, 240, 1060, fl, t_room + .8, RED, 6)]
    return {"base": "dark", "stars": 20, "cam": [1, 889, 500], "els": els}


V36 = View(-8.5, -4.5, 35.0, 37.0, (90, 120, 1600, 680))


def s36():
    """Right outside the Strait, a drowned island: Spartel Bank (Collina-Girard 2001)."""
    sid = "s36"
    v = V36
    t_out, t_isl, t_sp = T(sid, "outside the Strait"), T(sid, "drowned island"), T(sid, "Spartel Bank")
    gx, gy = v.p(-5.35, 36.14); mx, my = v.p(-5.41, 35.9); sx, sy = v.p(-6.03, 35.93)
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(-6.4, 36.62), "Spain", .3, "#e9dccb", 30), lab(*v.p(-5.3, 35.35), "Morocco", .3, "#e9dccb", 30), lab(*v.p(-7.8, 36.2), "Atlantic", .3, BLUE, 34, st="ital")]
    els += f04._pillars(gx - 12, gy, 30, t_out - .4, "#efe6d2") + f04._pillars(mx - 12, my + 6, 30, t_out - .2, "#efe6d2")
    els += [arrow([[gx - 30, (gy + my) / 2], [sx + 60, sy - 6]], t_out + .4, AMBER, 3, dur=.8, curve=False),
            ring(sx, sy, 40, t_isl, LILAC, 2.5, "inferred", .6), {"k": "pin", "x": sx, "y": sy, "t": "Spartel Bank", "c": GOLD, "in": t_sp, "fx": "pop", "a": "end", "lx": -22, "ly": 46},
            ] + scalebar(140, 760, v.km(20), "20 km", .8)
    return {"base": "map", "cam": [1, 889, 500], "els": els}


BCX, BCY = 700, 500
CONTOURS = [(150, [(BCX, BCY, 330, 215, 3)]), (140, [(BCX, BCY, 295, 188, 4)]), (130, [(BCX, BCY, 260, 160, 5)]), (120, [(BCX - 10, BCY - 4, 215, 128, 6)]),
            (100, [(BCX - 20, BCY - 6, 160, 92, 8)]), (90, [(BCX - 60, BCY - 10, 86, 50, 9), (BCX + 80, BCY + 18, 70, 44, 10)]),
            (80, [(BCX - 92, BCY - 20, 34, 22, 12), (BCX - 22, BCY + 2, 26, 18, 13), (BCX + 66, BCY + 10, 30, 20, 14), (BCX + 112, BCY + 34, 20, 14, 15)])]
DEPTHC = {150: "#173a50", 140: "#1d4862", 130: "#245777", 120: "#2c6888", 100: "#357b98", 90: "#4590a8", 80: "#5aa6b8"}


def _contour(level, at, fill=None, op=1, line_only=False, c="rgba(220,240,250,.5)"):
    out = []
    for cx, cy, rx, ry, seed in dict(CONTOURS)[level]:
        p = blob(cx, cy, rx, ry, seed, 18, .1)
        if line_only:
            out.append({"k": "line", "p": p, "c": c, "w": 1.5, "curve": True, "close": True, "in": at})
        else:
            out.append(poly(p, fill or DEPTHC[level], c, 1.2, at, curve=True, op=op))
    return out


def s37():
    """Spartel Bank in plan, multibeam colours (Gutscher 2005): with the sea 130 m lower it was an island about 6.5 by 4 km, on a coast
    of great earthquakes and tsunamis; a sea-floor core with one unusually thick layer about 12,000 years old."""
    sid = "s37"
    t_low, t_dry, t_65, t_eq, t_ts, t_mud, t_12 = (T(sid, "Ice Age low"), T(sid, "stood above"), T(sid, "six and a half"), T(sid, "earthquakes"),
                                                    T(sid, "tsunamis"), T(sid, "thick layer"), T(sid, "twelve thousand"))
    els = [box(0, 0, W_, H_, "#10283a", r=0, at=-1)]
    for k, (lev, _) in enumerate(CONTOURS):
        els += _contour(lev, round(.3 + .15 * k, 2))
    els += chip(250, 470, "sea 130 m lower", t_low, BLUE, 26)
    els += _contour(130, t_dry, "#8a7450", .95) + _contour(120, t_dry + .1, line_only=True, c="rgba(240,220,180,.5)") + \
        _contour(100, t_dry + .1, line_only=True, c="rgba(240,220,180,.5)") + _contour(90, t_dry + .1, line_only=True, c="rgba(240,220,180,.5)") + \
        _contour(80, t_dry + .1, line_only=True, c="rgba(240,220,180,.5)")
    els += [{"k": "dim", "x1": BCX - 260, "y1": BCY - 196, "x2": BCX + 260, "y2": BCY - 196, "t": "6.5 km", "c": AMBER, "in": t_65}]
    r = random.Random(3)
    seis = [[200 + 12 * j, round(165 + (r.uniform(-1, 1) * (30 if 30 < j < 52 else 6)), 1)] for j in range(84)]
    els += [{"k": "line", "p": seis, "c": "#ff9a7a", "w": 2.5, "in": t_eq, "fx": "draw", "dur": 1.0},
            wave(160, 1240, 236, t_ts, "#bfe6f5", 22, 7, 4, 1.2)]
    cx0, cw = 1360, 84
    lay = [(190, 250, "#7a6a58"), (250, 300, "#8f7d68"), (300, 360, "#6f604f"), (360, 420, "#8a785f"), (420, 530, "#a8885a"), (530, 600, "#7a6a58"), (600, 700, "#6a5a48")]
    els += [box(cx0 - 6, 184, cw + 12, 522, "none", BONE, 2, 6, t_mud - .6)]
    els += [box(cx0, a, cw, b - a, c, r=0, at=round(t_mud - .5 + .05 * k, 2)) for k, (a, b, c) in enumerate(lay)]
    els += [box(cx0 - 4, 420, cw + 8, 110, "rgba(232,184,122,.35)", AMBER, 3, 4, t_mud + 1.0, fx="pop")]
    els += [dot(round(cx0 + r.uniform(8, cw - 8), 1), round(r.uniform(430, 520), 1), round(r.uniform(2.5, 5), 1), "#f0d8a8", round(t_mud + 1.1 + .02 * j, 2)) for j in range(22)]
    els += [lab(cx0 - 20, 486, "about 12,000 years ago", t_12, AMBER, 28, "end"),
            lab(cx0 + cw / 2, 160, "core", t_mud - .4, DIM, 26)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s38_add():
    """Sea level alone: the waterline climbs past 120, 100, 90 and 80 m below today, and the island shrinks to wave-swept rocks by
    about 13,000 years ago; only if quakes dropped it about 40 m was it larger then (about 5 by 2 km, Gutscher 2005)."""
    sid = "s38"
    t_rise, t_rocks, t_13, t_unl = T(sid, "rising seas"), T(sid, "wave swept"), T(sid, "thirteen thousand"), T(sid, "unless earthquakes")
    out = []
    levels = [130, 120, 100, 90, 80]
    for k in range(1, len(levels)):
        at = round(t_rise + .3 + .75 * (k - 1), 2)
        out += _contour(levels[k - 1], at) + _contour(levels[k], at, "#8a7450", .95)
        for lev in levels[k + 1:]:
            out += _contour(lev, at, line_only=True, c="rgba(240,220,180,.5)")
    for cx, cy, rx, ry, _ in dict(CONTOURS)[80]:
        out += [{"k": "line", "p": I.ellipse(cx, cy, rx + 14, ry + 10, 24, 200, 340), "c": "#ffffff", "w": 2, "curve": True, "in": t_rocks, "fx": "draw", "dur": .4},
                {"k": "line", "p": I.ellipse(cx, cy, rx + 14, ry + 10, 24, 20, 160), "c": "#ffffff", "w": 2, "curve": True, "in": t_rocks + .2, "fx": "draw", "dur": .4}]
    out += chip(BCX, 760, "about 13,000 years ago", t_13, BLUE, 26)
    out += [{"k": "line", "p": blob(BCX, BCY, 200, 80, 21, 16, .08), "c": LILAC, "w": 3, "style": "claimed", "curve": True, "close": True, "in": t_unl + .6},
            lab(BCX, BCY + 128, "if quakes dropped it", t_unl + 1.0, LILAC, 30)]
    return out


def s39_add():
    """Anyone living there: probably simple fishermen (a boat, two figures, a net), not a Bronze Age empire (Plato's city struck out)."""
    sid = "s39"
    t_fish, t_emp = T(sid, "simple fishermen"), T(sid, "Bronze Age")
    x, y = 560, 410
    out = [{"k": "boat", "x": x, "y": y, "w": 110, "in": t_fish - .4, "fx": "rise"}, person(x - 18, y - 12, 40, t_fish - .2, GOLD), person(x + 22, y - 12, 40, t_fish, GOLD),
           {"k": "line", "p": I.ellipse(x + 90, y + 6, 46, 20, 16, 0, 180), "c": GOLD, "w": 2, "style": "inferred", "curve": True, "in": t_fish + .2, "fx": "draw", "dur": .5}]
    out += city_plan(1080, 560, 9.6, t_emp, .35, ghost=True)
    out += [strike(940, 610, 1220, 510, t_emp + 1.1, RED, 5), lab(1080, 650, "Bronze Age empire", t_emp + .3, LILAC, 28)]
    return out


# ================================================================== chapter 4: three places on the map
def s40():
    """The search map again: Spartel Bank set aside, the other three lit one by one, a hammer at each: let's ask the rock."""
    sid = "s40"
    base = s4()
    for e in base["els"]:
        if e.get("in", 0) >= 0:
            e["in"] = -1
    v = View(-85, 35, 10, 50, (90, 130, 1600, 660))
    t_three, t_rock = T(sid, "Three favourite"), T(sid, "ask the rock")
    sx, sy = v.p(-6.0, 35.9)
    els = base["els"] + [oval(sx - 70, sy - 18, 110, 34, "#10202a", at=.3, op=.75), oval(sx, sy, 30, 30, "#10202a", at=.3, op=.6)]
    for k, (lo, la) in enumerate(((-11.39, 21.12), (-79.28, 25.77), (25.4, 36.4))):
        x, y = v.p(lo, la)
        els += [glow(x, y, 90, round(t_three + .4 * k, 2), .8, "lamp")] + hammer(x + 14, y - 14, 40, round(t_rock + .45 * k, 2))
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s41():
    """The Eye of the Sahara (Richat Structure, Mauritania), seen as if from orbit: rings of rock 40 km across (the Short's model, wide)."""
    sid = "s41"
    t_mau, t_40, t_sp = T(sid, "Mauritania"), T(sid, "forty kilometres"), T(sid, "staring up")
    iso = _iso_from(f04.richat()["shots"][0], x=889, y=470, s=8, spin=.6, **{"in": .2})
    return {"base": "dark", "stars": 140, "cam": [1, 889, 500], "els": [glow(889, 470, 560, .2, .2, "lamp"), iso,
            lab(1430, 250, "the Eye, 40 km across", t_40, AMBER, 32), lab(1430, 292, "Mauritania", t_mau, DIM, 28), glow(889, 470, 300, t_sp, .25, "lamp")]}


V42 = View(-26, 6, 15, 36.5, (90, 120, 1600, 680))


def s42():
    """At first glance it fits: rings, the Atlantic side of Africa, mountains to the north (three ticks)."""
    sid = "s42"
    v = V42
    t_r, t_at, t_mt = T(sid, "rings"), T(sid, "Atlantic side"), T(sid, "mountains")
    ex, ey = v.p(-11.39, 21.12)
    cx, cy = v.p(-16.6, 21.3)
    atlas = [v.p(lo, la) for lo, la in ((-9.6, 29.9), (-8.5, 30.2), (-7.4, 30.45), (-6.3, 30.65), (-5.2, 30.8), (-4.1, 30.9), (-2.8, 31.6), (-1.5, 32.6))]
    els = [{"k": "map", "land": v.land(), "in": -1}, {"k": "pin", "x": ex, "y": ey, "t": "the Eye", "c": GOLD, "in": .3, "fx": "pop", "ly": 46, "lx": 10},
           lab(*v.p(-21.5, 27), "Atlantic", .3, BLUE, 36, st="ital"), lab(*v.p(-2, 24), "Sahara", .3, "#c9ad85", 30, st="ital")]
    els += [ring(ex, ey, 40, t_r - .3, AMBER, 3), ring(ex, ey, 26, t_r - .1, AMBER, 3), tick(ex + 70, ey - 40, t_r + .4)]
    els += [arrow([[ex - 30, ey + 4], [(ex + cx) / 2, ey + 26], [cx + 12, cy]], t_at - .2, BLUE, 3, "inferred", .7), tick(cx - 30, cy + 64, t_at + .6)]
    els += [I.tri(x, y - 6, 16, 0, "#c9ad85", round(t_mt - .2 + .08 * k, 2)) for k, (x, y) in enumerate(atlas)]
    els += [lab(atlas[3][0], atlas[3][1] - 34, "Atlas", t_mt, "#c9ad85", 28, st="ital"), tick(atlas[-1][0] + 40, atlas[-1][1] - 10, t_mt + .8)]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s43():
    """Plato's whole city, about 5 km across: eight of them fit across the Eye's 40 km; and the Eye is hundreds of km from the sea."""
    sid = "s43"
    t_city, t_8, t_far = T(sid, "Plato's whole city"), T(sid, "eight times"), T(sid, "hundreds of kilometres")
    ex, ey, R = 480, 405, 280
    els = [oval(ex, ey, R, R, "rgba(201,163,112,.16)", at=.2), ring(ex, ey, R, .2, "#c9a370", 5), ring(ex, ey, R * .72, .35, "#a07a50", 4), ring(ex, ey, R * .44, .5, "#c9a370", 4),
           lab(ex, ey - R * .84, "the Eye", .6, AMBER, 32)]
    cr = R / 8.0
    for k in range(8):
        at = round(t_city + .6 if k == 0 else t_8 - 2.4 + .3 * k, 2)
        els += f04._rings(round(ex - R + cr + 2 * cr * k, 1), ey, round(cr / 2.8, 2), at, .03)
    els += [lab(ex - R + cr, ey - cr - 16, "5 km", t_city + 1.0, BLUE, 28),
            {"k": "dim", "x1": ex - R, "y1": ey + R + 26, "x2": ex + R, "y2": ey + R + 26, "t": "40 km", "c": AMBER, "in": t_8, "ly": 38}]
    gx0, gy = 900, 640
    els += [box(gx0, gy - 6, 130, 90, SEA, r=0, at=t_far - 1.2, op=.85), wave(gx0, gx0 + 130, gy - 6, t_far - 1.2, "#bfe6f5", 4, 4, 2, .5), lab(gx0 + 60, gy + 46, "sea", t_far - 1.0, BLUE, 26),
            poly([[gx0 + 130, gy - 6], [1200, 590], [1380, 520], [1680, 500], [1680, 730], [gx0 + 130, 730]], "#8a6a48", "#c9ad85", 2, t_far - 1.1, fx="rise"),
            {"k": "line", "p": I.ellipse(1560, 500, 40, 9, 24), "c": AMBER, "w": 3, "curve": True, "in": t_far - .6}, {"k": "line", "p": I.ellipse(1560, 500, 24, 5, 24), "c": AMBER, "w": 3, "curve": True, "in": t_far - .5},
            lab(1560, 470, "the Eye", t_far - .4, AMBER, 26),
            arrow([[gx0 + 150, 690], [1520, 690]], t_far, BONE, 3, dur=1.0, curve=False), lab(1290, 670, "hundreds of km", t_far + .4, BONE, 30)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def s44():
    """The Eye cut open: flat rock layers pushed up into a dome about 100 million years ago (Matton & Jebrak 2014), its top shaved
    off by the wind (the lost dome dashed); the cut edges of the layers are the rings seen from above."""
    sid = "s44"
    t_lay, t_up, t_100, t_wind, t_blank, t_bl = (T(sid, "rock layers"), T(sid, "pushed up"), T(sid, "a hundred million"), T(sid, "shaved flat"), T(sid, "stack of blankets"),
                                                  T(sid, "A natural blister"))
    S, BOT, X0, X1, CX = 560, 780, 200, 1580, 889
    apex = [350, 410, 470, 530, 600, 660]
    kq = (S - apex[0]) / 600.0 ** 2
    yb = lambda k, x: apex[k] + kq * (x - CX) ** 2
    cols = ["#d9b98a", "#7a6248", "#e6cfa6", "#8c6a48", "#cdb48e", "#6f5a44", "#a08060"]
    els = [box(X0, S, X1 - X0, BOT - S, "none", BONE, 2, 2, .3, fx="draw")]
    for k in range(-1, 6):
        segs, cur = [], []
        for x in range(X0, X1 + 1, 10):
            top = S if k < 0 else max(S, yb(k, x))
            bot = BOT if k == 5 else min(BOT, yb(k + 1, x))
            if top < bot - .5:
                cur.append((x, top, bot))
            elif cur:
                segs.append(cur); cur = []
        if cur:
            segs.append(cur)
        for sg in segs:
            pp = [[x, round(t, 1)] for x, t, b in sg] + [[x, round(b, 1)] for x, t, b in reversed(sg)]
            els.append(poly(pp, cols[k + 1], at=round(t_lay + .2 * (5 - k), 2), fx="fill", dur=.7))
    els += [line([[X0, S], [X1, S]], .3, "#ffe2be", 3, dur=.8), arrow([[CX, BOT - 10], [CX, 610]], t_up, BONE, 5, dur=.7, curve=False),
            lab(CX + 30, 640, "pushed up", t_up + .4, BONE, 28, "start"), lab(CX + 30, 678, "100 million years ago", t_100, BONE, 28, "start")]
    for k in range(4):
        d = math.sqrt((S - apex[k]) / kq)
        els.append(line([[round(x, 1), round(yb(k, x), 1)] for x in [CX - d + 2 * d * j / 24 for j in range(25)]], round(t_wind + .7 + .2 * k, 2), BONE, 2.5, "inferred", 1.0, curve=True, op=.6))
    els += [arrow([[120, y], [500, y - 12], [1000, y + 8], [1660, y - 6]], round(t_wind - .2 + .25 * j, 2), "#cfe6ff", 3, "known", 1.0) for j, y in enumerate((500, 440, 380))]
    for k in range(4):
        d = math.sqrt((S - apex[k]) / kq)
        at = round(t_blank + .35 * k, 2)
        els += [{"k": "line", "p": I.ellipse(CX, 240, d, d * .1, 48), "c": cols[k + 1] if k % 2 == 0 else "#b8905e", "w": 7, "curve": True, "in": at, "fx": "draw", "dur": .7},
                line([[CX - d, S], [CX - d, 240]], at + .1, AMBER, 1.5, "inferred", .5, op=.6), line([[CX + d, S], [CX + d, 240]], at + .1, AMBER, 1.5, "inferred", .5, op=.6)]
    els += [lab(CX, 150, "seen from above: rings", t_blank + 1.2, AMBER, 30), glow(CX, 240, 380, t_bl, .3, "lamp")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s45():
    """Bimini: half a mile of squared stones under 5.5 m of clear water, found in 1968, the year a 1940 prediction named; the banks
    were dry land in the Ice Age (the Short's model, wide)."""
    sid = "s45"
    t_sq, t_fd, t_cay, t_dry = T(sid, "half a mile"), T(sid, "found in"), T(sid, "Edgar Cayce"), T(sid, "dry land")
    iso = _iso_from(f04.bimini()["shots"][0], x=740, y=470, s=5.6, spin=.12, **{"in": .2})
    iso["items"] += [{"t": "line", "p": [[66, -.1, 36], [66, 6.2, 36]], "c": "#cfe6ff", "w": 2}, {"t": "label", "x": 66, "y": 3.1, "z": 36, "text": "5.5 m", "c": "#cfe6ff", "dy": 0, "st": "lab"}]
    els = [glow(740, 470, 520, .2, .2, "lamp"), iso, lab(1410, 210, "squared blocks,", t_sq, GOLD, 30), lab(1410, 250, "half a mile", t_sq + .1, GOLD, 30), f04._diver(1120, 340, 76, 1.0)]
    els += chip(330, 600, "1968: found", t_fd, AMBER, 26) + chip(330, 540, "1940: predicted for 1968", t_cay, LILAC, 26)
    bx, by = 1160, 520
    els += [box(bx, by, 500, 250, "rgba(13,11,9,.85)", "rgba(255,226,190,.35)", 2, 12, t_dry - 1.4, fx="pop"), lab(bx + 20, by + 34, "Ice Age", t_dry - 1.2, AMBER, 26, "start"),
            line([[bx + 20, by + 130], [bx + 480, by + 130]], t_dry - 1.2, "#c9b48c", 6, draw=False),
            wave(bx + 20, bx + 480, by + 80, t_dry - 1.0, BLUE, 5, 10, 2, .5), lab(bx + 470, by + 72, "sea today", t_dry - 1.0, BLUE, 24, "end"),
            line([[bx + 20, by + 220], [bx + 480, by + 220]], t_dry - .2, BLUE, 2, "inferred", .6), lab(bx + 470, by + 210, "Ice Age sea", t_dry, "#cfe6ff", 24, "end"),
            person(bx + 200, by + 128, 46, t_dry + .2, "#e8d6b8"), person(bx + 250, by + 128, 46, t_dry + .35, "#e8d6b8"), lab(bx + 225, by + 168, "dry land", t_dry + .5, AMBER, 26)]
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": els}


def s46():
    """Beachrock: beach sand glued by lime at the tide line hardens into a slab, which cracks into squares by itself, like mud drying
    in a puddle."""
    sid = "s46"
    t_br, t_glue, t_cr, t_mud = T(sid, "beachrock"), T(sid, "glued by lime"), T(sid, "cracks into squares"), T(sid, "mud drying")
    r = random.Random(5)
    beach = [[100, 380], [500, 470], [860, 580], [860, 760], [100, 760]]
    els = [box(100, 480, 760, 280, SEA, r=0, at=.2, op=.5), poly(beach, "#c9b48c", "#efe2c4", 2, .3), wave(480, 860, 480, .5, "#bfe6f5", 6, 8, 2, .6),
           line([[420, 452], [860, 452]], .7, BLUE, 2, "inferred", .5), lab(860, 440, "tide line", .9, BLUE, 26, "end"),
           lab(480, 150, "beachrock", t_br, AMBER, 34)]
    els += [dot(round(x, 1), round(y, 1), 3.5, "#8a7452", round(t_glue - .4 + .006 * k, 3)) for k, (x, y) in enumerate(
        [(r.uniform(110, 850), r.uniform(0, 1)) for _ in range(140)]) for x, y in [(x, 380 + (x - 100) * .26 + 10 + y * (740 - 390 - (x - 100) * .26))] if y < 760]
    slab = [[440, 478], [700, 538], [700, 566], [440, 506]]
    els += [poly(slab, "#e0cfa8", "#fff4dc", 2, t_glue + .4, fx="pop"), lab(560, 610, "sand glued by lime", t_glue + .6, "#3a2a1a", 26, halo=False)]
    els += [line([[440 + 52 * j, 478 + 52 * j * .2308 - 2], [440 + 52 * j, 508 + 52 * j * .2308 + 2]], round(t_cr + .12 * j, 2), "#3a2a1c", 3, dur=.3) for j in range(1, 5)]
    els += [line([[440, 492], [700, 552]], t_cr + .7, "#3a2a1c", 3, dur=.6)]
    px, py = 1290, 460
    els += [oval(px, py, 330, 210, "#6b5236", "#c9a370", 2, 1, t_mud - .6), lab(px, 180, "a drying puddle", t_mud - .3, "#c9a370", 30)]
    pts = {}
    for i in range(7):
        for j in range(5):
            pts[(i, j)] = (round(px - 270 + 90 * i + r.uniform(-14, 14), 1), round(py - 160 + 80 * j + r.uniform(-12, 12), 1))
    inside = lambda q: ((q[0] - px) / 320) ** 2 + ((q[1] - py) / 200) ** 2 < 1
    segs = []
    for (i, j), q in pts.items():
        for di, dj in ((1, 0), (0, 1)):
            q2 = pts.get((i + di, j + dj))
            if q2 and inside(q) and inside(q2):
                segs.append([list(q), list(q2)])
    els += [line(sg, round(t_mud + .1 + .03 * k, 2), "#2a1d12", 4, dur=.3) for k, sg in enumerate(segs)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s47():
    """Cores show the layers running on from block to block (McKusick & Shinn 1980); the shells are about 3,500 years old, younger
    than the pyramids (about 4,500 years); the cement younger still."""
    sid = "s47"
    t_cor, t_run, t_sh, t_pyr = T(sid, "Cores show"), T(sid, "running on"), T(sid, "shells are"), T(sid, "younger than the pyramids")
    els = []
    for k in range(4):
        x = 330 + 290 * k
        els += f04._block(x, 380, 260, 190, round(.3 + .15 * k, 2), "#c9b48c", fx="pop")
        els += [box(x + 117, 200, 26, 170, "#efe6d2", "#8a7a66", 1.5, 8, round(t_cor + .2 * k, 2), fx="fill", dur=.6)]
    els += [line([[330, 236 + 34 * j], [1460, 290 + 34 * j]], round(t_run + .3 * j, 2), GOLD, 3, dur=1.4) for j in range(4)]
    els += [lab(895, 150, "layers run on", t_run + 1.0, GOLD, 30)]
    Tx = lambda ya: round(200 + (12000 - ya) / 12000 * 1400, 1)
    ay = 620
    els += [axis(200, 1600, ay, [(Tx(12000), "12,000 years ago"), (Tx(8000), "8,000"), (Tx(4000), "4,000"), (Tx(0), "today")], t_sh - 1.2),
            dot(Tx(11700), ay, 11, BLUE, t_sh - .9), lab(Tx(11700) + 6, ay - 26, "Ice Age ends", t_sh - .8, BLUE, 26, "start"),
            dot(Tx(3500), ay, 12, GOLD, t_sh + 1.4), lab(Tx(3500), ay - 30, "shells", t_sh + 1.6, GOLD, 28),
            poly([[Tx(4500) - 34, ay - 16], [Tx(4500) + 34, ay - 16], [Tx(4500), ay - 70]], "#d9c29a", "#f2dcb4", 1.5, t_pyr, fx="rise"),
            lab(Tx(4500) - 40, ay - 84, "pyramids", t_pyr + .2, "#d9c29a", 26, "end"),
            arrow([[Tx(3500) + 14, ay + 26], [Tx(2300), ay + 26]], t_pyr + 1.0, GOLD, 3, dur=.5, curve=False), lab(Tx(2900), ay + 100, "cement: younger", t_pyr + 1.2, GOLD, 24)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


V48 = View(21.8, 28.6, 34.4, 38.6, (90, 120, 1600, 680))


def s48():
    """Thera, today's Santorini: the volcano exploded around 1600 BCE; Crete and Knossos, over 100 km to the south."""
    sid = "s48"
    v = V48
    t_th, t_x = T(sid, "Thera"), T(sid, "exploded")
    kn, th = v.p(25.1631, 35.298), v.p(25.4, 36.4)
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(24.4, 34.95), "Crete", .3, "#c9ad85", 32, st="ital"), lab(*v.p(23.0, 37.6), "Aegean", .3, BLUE, 32, st="ital"),
           {"k": "pin", "x": th[0], "y": th[1], "t": "Thera", "c": RED, "in": t_th - .2, "fx": "pop"}, lab(th[0] + 18, th[1] + 40, "today's Santorini", t_th + .9, DIM, 24, "start"),
           glow(th[0], th[1], 150, t_x, .95, "red")]
    els += [oval(th[0] + 22 * k, th[1] - 60 - 62 * k, 44 + 14 * k, 28 + 7 * k, "#8a8378", at=round(t_x + .3 + .3 * k, 2), op=.6) for k in range(4)]
    els += [{"k": "pin", "x": kn[0], "y": kn[1], "t": "Knossos", "c": GOLD, "in": t_x + 1.4, "fx": "pop", "ly": 36},
            line([kn, th], t_x + 1.6, BONE, 2, "inferred", .8), lab((kn[0] + th[0]) / 2 - 24, (kn[1] + th[1]) / 2, "over 100 km", t_x + 1.8, BONE, 28, "end"),
            ] + scalebar(140, 760, v.km(50), "50 km", .6)
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s48b_add():
    """The plume settles: a real catastrophe, perhaps a distant memory, but not Plato's island."""
    sid = "s48b"
    v = V48
    th = v.p(25.4, 36.4)
    t_mem = T(sid, "distant memory")
    return [oval(th[0] + 40, th[1] - 10, 260, 60, "#8a8378", at=.6, op=.45), oval(th[0] + 120, th[1] + 30, 320, 70, "#8a8378", at=1.2, op=.3),
            glow(th[0], th[1], 260, t_mem, .4, "lamp")]


def s49():
    """Left: the olive tree buried alive under about 60 m of pumice (Friedrich et al. 2006), a person to scale (10 units = 1 m).
    Right: Akrotiri under the ash: houses of two and three storeys, a painted wall, a drain under the street (Doumas 1983)."""
    sid = "s49"
    t_ol, t_60, t_ak, t_ho, t_pw, t_dr = T(sid, "olive tree"), T(sid, "sixty metres"), T(sid, "Akrotiri"), T(sid, "houses"), T(sid, "painted walls"), T(sid, "drains")
    gy = 760
    els = [box(100, gy, 640, 30, "#5a4636", r=0, at=.2)]
    for k in range(6):
        els.append(box(100, gy - 100 * (k + 1), 640, 100, "#d8cdb6" if k % 2 == 0 else "#c4b89c", "rgba(90,70,50,.35)", 1, 0, round(t_ol + .8 + .3 * k, 2), fx="fill", dur=.5))
    els += [line([[300, gy], [300, gy - 26]], t_ol - .2, "#6b4f34", 5, draw=False), oval(300, gy - 38, 30, 18, "#7a8a5a", "#3a4a2a", 1.5, 1, t_ol - .2),
            lab(300, gy - 72, "olive tree", t_ol + .2, "#3a2a1a", 26, halo=False),
            person(352, gy, 17, t_60 + 1.2, "#3a2a1a"), lab(372, gy - 4, "1.7 m", t_60 + 1.3, "#3a2a1a", 24, "start", halo=False),
            {"k": "dim", "x1": 690, "y1": gy, "x2": 690, "y2": gy - 600, "t": "60 m", "c": "#3a2a1a", "in": t_60, "lx": -46, "ly": 10, "upright": True},
            lab(420, 136, "pumice", t_60 + .4, "#d8cdb6", 30)]
    E49 = dict(x=1240, y=520, s=9, az=-30, spin=0, el=.5)
    items = [{"t": "slab", "x0": -30, "x1": 30, "z0": -14, "z1": 14, "y": 0, "c": "#6a5a48"},
             {"t": "flat", "pts": [[-30, -2], [30, -2], [30, 2], [-30, 2]], "y": .05, "c": "#8a7a66"}]
    for x, h in ((-23, 6), (-9, 9), (5, 6), (19, 9)):
        items.append({"t": "box", "x": x, "z": -8, "y": 0, "w": 12, "d": 10, "h": h, "c": "#b8a68a", "edge": "rgba(40,30,20,.5)"})
    for x, h in ((-19, 9), (-4, 6), (12, 9)):
        items.append({"t": "box", "x": x, "z": 8.5, "y": 0, "w": 12, "d": 9, "h": h, "c": "#c4b294", "edge": "rgba(40,30,20,.5)"})
    items.append({"t": "box", "x": 0, "z": 0, "y": 0, "w": 60, "d": 28, "h": 11, "c": "#9a958c", "op": .22, "edge": "rgba(220,220,220,.35)"})
    iso = dict({"k": "iso", "items": items, "in": t_ak - .4}, **E49)
    paint = dict({"k": "iso", "in": t_pw, "items": [
        {"t": "quad", "p": [[-9.5, 2.2, 13.05], [1.5, 2.2, 13.05], [1.5, 3.2, 13.05], [-9.5, 3.2, 13.05]], "n": [0, 0, 1], "c": "#3f86b0", "edge": "rgba(0,0,0,0)"},
        {"t": "quad", "p": [[-9.5, 3.5, 13.05], [1.5, 3.5, 13.05], [1.5, 4.4, 13.05], [-9.5, 4.4, 13.05]], "n": [0, 0, 1], "c": "#c8442a", "edge": "rgba(0,0,0,0)"}]}, **E49)
    drain = dict({"k": "iso", "in": t_dr, "items": [{"t": "line", "p": [[-30, -.6, 0], [30, -.6, 0]], "c": BLUE, "w": 4, "style": "inferred"}]}, **E49)
    fx_, fy_ = _proj(E49, (-4, 3.5, 13))
    dx_, dy_ = _proj(E49, (24, -.6, 0))
    hx, hy = _proj(E49, (-9, 9, -8))
    els += [iso, lab(1240, 150, "Akrotiri, under ash", t_ak, AMBER, 32), paint, drain,
            lab(hx, hy - 30, "3 storeys", t_ho + 1.0, BONE, 26), glow(fx_, fy_, 70, t_pw, .7, "lamp"), lab(fx_, fy_ + 70, "painted wall", t_pw + .2, BONE, 26),
            lab(dx_ + 20, dy_ + 40, "drain", t_dr + .2, BLUE, 26, "start")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s50():
    """Minoan Crete's bull games (a fresco, solid) beside the bull hunt Plato puts in his story's temple (lilac dotted: a story)."""
    sid = "s50"
    t_min, t_sea, t_bull, t_hunt, t_tem = T(sid, "Minoans"), T(sid, "seafaring"), T(sid, "bull games"), T(sid, "bull hunt"), T(sid, "Plato's temple")
    els = [box(140, 170, 680, 470, "#d9b98a", "#3f86a8", 10, 6, t_min - .4, fx="pop"), lab(480, 700, "Crete: bull games", t_min, AMBER, 30),
           {"k": "boat", "x": 690, "y": 236, "w": 120, "in": t_sea}]
    els += bull(470, 600, 420, t_bull - .2, "#7a3a22") + leaper(436, 338, 160, t_bull + .4)
    els += temple_line(1300, 610, 560, t_hunt - .6, LILAC, "claimed", 3)
    els += bull(1300, 580, 230, t_hunt, face=-1, style="claimed", lc=LILAC)
    for k, x in enumerate((1050, 1102, 1154, 1414, 1466, 1518)):         # ten hunters with staves and nooses: six below, four above
        at = round(t_hunt + .3 + .1 * k, 2)
        els += [person(x, 600, 52, at, LILAC), line([[x + 8, 564], [x + 22, 538]], at, LILAC, 2, draw=False)]
    for k, (x, y) in enumerate(((1170, 470), (1220, 450), (1380, 450), (1430, 470))):
        at = round(t_hunt + .7 + .1 * k, 2)
        els += [person(x, y, 44, at, LILAC), ring(x + 16, y - 52, 8, at, LILAC, 2, dur=.3)]
    els += [lab(1300, 700, "Plato's bull hunt", t_tem, LILAC, 30), line([[820, 400], [1010, 400]], t_tem + .6, BONE, 2, "inferred", .6)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s51():
    """A slip of ten (Galanopoulos 1969): 900 years before Solon instead of 9,000 lands near the Thera eruption (about 1620 to
    1525 BCE). The 9,000 loses a zero; the arc of 900 years ends about 1490 BCE."""
    sid = "s51"
    X, y = X18, A18
    t_ten, t_900, t_er = T(sid, "slip of ten"), T(sid, "nine hundred years"), T(sid, "near the eruption")
    base = s18()["els"]
    for e in base:
        if isinstance(e.get("in"), (int, float)) and e["in"] >= 0:
            e["in"] = -1
    arc = [[round(X(590) - 16 - (X(590) - 16 - X(1490)) * u, 1), round(y - 70 - 80 * math.sin(math.pi * u), 1)] for u in [k / 12 for k in range(13)]]
    els = base + [strike(840, 186, 960, 166, t_ten, RED, 4),
                  {"k": "group", "tr": "rotate(40 1046 250)", "in": t_ten + .3, "els": [lab(1046, 250, "0", -1, AMBER, 44, st="serif")]},
                  {"k": "group", "tr": "rotate(80 1080 310)", "in": t_ten + .6, "els": [lab(1080, 310, "0", -1, AMBER, 40, st="serif", op=.6)]},
                  {"k": "arrow", "p": arc + [[X(1490), y - 14]], "c": AMBER, "w": 3.5, "style": "claimed", "curve": True, "fx": "draw", "dur": .8, "in": t_900},
                  lab((X(590) + X(1490)) / 2 - 10, y - 166, "900", t_900 + .4, AMBER, 50, st="serif", fx="rise"),
                  dot(X(1490), y, 11, AMBER, t_900 + .9), ring(X(9600), y, 20, t_900 + 1.0, DIM, 2, "inferred", .4),
                  box(X(1620), y - 22, X(1525) - X(1620), 44, RED, r=3, at=t_er, fx="pop"), glow(X(1572), y, 70, t_er, .7, "red"),
                  lab(X(1572) - 10, y + 92, "Thera erupts", t_er + .3, RED, 28, "end")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


V52 = View(-12, 30, 30, 42, (90, 120, 1600, 520))


def s52():
    """Nothing says which numbers to shrink; Plato puts Atlantis outside the Pillars, far from Thera; Knossos carried on for
    generations after the eruption."""
    sid = "s52"
    v = V52
    t_txt, t_out, t_pil, t_cr = T(sid, "nothing in the text"), T(sid, "outside the Pillars"), T(sid, "Pillars of Heracles"), T(sid, "carried on")
    gx, gy = v.p(-5.35, 36.0); tx, ty = v.p(25.4, 36.4)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += scroll(560, 548, 70, t_txt) + [lab(560, 560, "?", t_txt + .4, LILAC, 40, st="serif")]
    els += f04._pillars(gx - 14, gy, 34, t_pil - .3, "#efe6d2") + [lab(gx + 30, gy - 50, "Pillars", t_pil, BONE, 28, "start"),
                                                                   arrow([[gx - 20, gy - 10], [gx - 200, gy - 40], [v.p(-11.5, 34.5)[0], v.p(-11.5, 34.5)[1]]], t_out, LILAC, 3, "claimed", .8),
                                                                   lab(*v.p(-10.5, 33.2), "Atlantis", t_out + .5, LILAC, 30, st="ital")]
    els += [{"k": "pin", "x": tx, "y": ty, "t": "Thera", "c": RED, "in": t_pil + .8, "fx": "pop"}, line([[gx + 24, gy + 10], [tx - 14, ty]], t_pil + 1.1, BONE, 2.5, dur=1.2)]
    X = lambda bce: round(300 + (1700 - bce) / 400 * 1200, 1)
    ay = 700
    els += [axis(300, 1500, ay, [(X(1700), "1700 BCE"), (X(1600), "1600"), (X(1500), "1500"), (X(1400), "1400"), (X(1300), "1300")], t_cr - .8),
            box(X(1620), ay - 34, X(1525) - X(1620), 30, RED, r=4, at=t_cr - .5, fx="pop", op=.85), lab((X(1620) + X(1525)) / 2, ay - 46, "eruption", t_cr - .4, RED, 26),
            bar(X(1700), X(1375), ay - 56 - 20, t_cr, GOLD, 14, 1.4), lab(X(1375) + 14, ay - 70, "Knossos", t_cr + 1.2, GOLD, 28, "start")]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s53():
    """Even the eruption's date is argued: the olive tree's rings say 1627 to 1600 BCE (Friedrich et al. 2006); annual tree rings
    allow about 1600 to 1525 BCE (Pearson et al. 2018)."""
    sid = "s53"
    t_ol, t_tr = T(sid, "about sixteen twenty"), T(sid, "about fifteen twenty five")
    X = lambda bce: round(200 + (1700 - bce) / 250 * 1400, 1)
    ay = 600
    els = [axis(200, 1600, ay, [(X(1700), "1700 BCE"), (X(1650), "1650"), (X(1600), "1600"), (X(1550), "1550"), (X(1500), "1500"), (X(1450), "1450")], .3),
           box(X(1627), ay - 90, X(1600) - X(1627), 34, "#8a9a5a", "#c9d79a", 2, 6, t_ol, fx="pop"), lab(X(1627) - 14, ay - 64, "olive tree", t_ol + .3, "#c9d79a", 28, "end"),
           line([[X(1613), ay - 110], [X(1613) - 30, ay - 200]], t_ol + .2, "#6b4f34", 4, draw=False)]
    els += [oval(X(1613) - 30 + 18 * math.cos(a), ay - 200 + 30 * k / 3 + 10 * math.sin(a), 16, 7, "#8a9a5a", at=t_ol + .3) for k, a in enumerate((0, 2.1, 4.2))]
    els += [box(X(1600), ay - 160, X(1525) - X(1600), 34, AMBER, "#f4d0a0", 2, 6, t_tr, fx="pop"), lab(X(1525) + 16, ay - 134, "tree rings", t_tr + .3, AMBER, 28, "start")]
    els += [ring(X(1562), ay - 250, r, round(t_tr + .1 * k, 2), AMBER, 2, dur=.3) for k, r in enumerate((10, 22, 34, 46))]
    els += I.question(X(1600), ay - 260, t_tr + 1.0, 70)
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


# ================================================================== chapter 5: the city that really sank
V54 = View(21.0, 24.5, 37.4, 38.8, (90, 120, 1600, 680))


def s54():
    """Winter, 373 BCE: the Gulf of Corinth; Helike, less than 150 km from Athens (about 143 km in a straight line)."""
    sid = "s54"
    v = V54
    t_w, t_gulf, t_less, t_ath = T(sid, "Winter"), T(sid, "Gulf of Corinth"), T(sid, "less than"), T(sid, "Athens")
    hx, hy = v.p(22.12, 38.22); ax, ay = v.p(23.73, 37.98)
    els = [{"k": "map", "land": v.land(), "in": -1}, box(0, 0, W_, H_, "#05070f", r=0, at=-1, op=.35),
           dot(1600, 190, 26, "#efe8da", .3), dot(1612, 183, 26, "#141726", .3), glow(1600, 190, 90, .3, .4, "lamp")]
    els += chip(330, 190, "winter, 373 BCE", t_w, AMBER, 28)
    els += [lab(*v.p(22.55, 38.27), "Gulf of Corinth", t_gulf, BLUE, 32, st="ital"),
            {"k": "pin", "x": hx, "y": hy, "t": "Helike", "c": RED, "in": t_gulf + .6, "fx": "pop", "a": "end", "lx": -20, "ly": 40},
            {"k": "pin", "x": ax, "y": ay, "t": "Athens", "c": GOLD, "in": t_ath - .4, "fx": "pop"},
            line([[hx + 14, hy + 4], [ax - 14, ay - 2]], t_less, BONE, 2.5, "inferred", 1.2),
            lab((hx + ax) / 2 + 10, (hy + ay) / 2 + 44, "under 150 km", t_less + .6, BONE, 30),
            ] + scalebar(140, 760, v.km(50), "50 km", .6)
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s55():
    """Helike on its coastal plain at night: houses, the temple of Poseidon (an outline of columns); at night an earthquake, then the
    sea rolls over the town and settles. Nobody is drawn in the water."""
    sid = "s55"
    t_city, t_tem, t_eq, t_sea = T(sid, "The city of"), T(sid, "temple"), T(sid, "earthquake"), T(sid, "Then the sea")
    els = [poly([[0, 400], [200, 330], [420, 360], [640, 300], [900, 350], [1150, 310], [1420, 360], [1640, 320], [1778, 350], [1778, 420], [0, 420]], "#2a2633", at=-1, curve=True),
           box(0, 410, W_, 130, "#1f4a62", r=0, at=-1, op=.95), wave(0, W_, 412, -1, "#bfe6f5", 4, 40, 2, .8),
           poly([[0, 520], [500, 512], [1100, 516], [1778, 510], [1778, 1000], [0, 1000]], "#3a3424", "rgba(255,226,190,.3)", 1.5, -1)]
    els += f04._houses(330, 600, 7, t_city, 40, "#d9c9a6") + f04._houses(1130, 606, 7, t_city + .3, 40, "#d9c9a6") + f04._houses(560, 660, 5, t_city + .5, 46, "#cdbd98")
    els += temple_line(889, 640, 170, t_tem, "#efe6d2", "known", 4) + [glow(889, 600, 160, t_tem, .35, "lamp"), lab(889, 700, "Helike", t_city + .8, BONE, 32)]
    r = random.Random(7)
    quake = [[x, round(520 + r.uniform(-14, 14), 1)] for x in range(0, 1779, 26)]
    els += [{"k": "line", "p": quake, "c": RED, "w": 3, "in": t_eq, "fx": "draw", "dur": .6}, line([[0, 545], [1778, 545]], t_eq + .5, "#e9dccb", 2, "inferred", .6)]
    crest = [[x, round(500 - 70 * math.sin(math.pi * (x - 150) / 1480) * (1 if 150 < x < 1630 else 0), 1)] for x in range(0, 1779, 30)]
    els += [poly(crest + [[1778, 560], [0, 560]], "#2c6a88", "#ffffff", 4, t_sea, fx="rise", curve=True, op=.95),
            box(0, 412, W_, 290, "#1f5670", r=0, at=t_sea + .9, op=.94, dur=1.4), wave(0, W_, 412, t_sea + 1.6, "#bfe6f5", 4, 40, 2, .8),
            wave(0, W_, 700, t_sea + 1.8, "#bfe6f5", 5, 30, 3, 1.0)]
    return {"base": "sky", "tod": "night", "ground": 1300, "sun": False, "moon": [1500, 170, 26], "cam": [1, 889, 500], "els": els}


def s57_add():
    """Grey dawn; the new waterline far inland; two thousand men on the shore, twenty groups of a hundred (one figure stands for 20)."""
    sid = "s57"
    t_men = T(sid, "Two thousand")
    out = [box(0, 0, W_, 410, "#8a90a0", r=0, at=.3, op=.25, dur=1.6), glow(889, 400, 700, .3, .25, "lamp"),
           box(0, 704, W_, 296, "#4a4234", "rgba(255,226,190,.3)", 1.5, 0, .4)]
    for g in range(20):
        x0 = 120 + 78 * g
        for j in range(5):
            out.append(person(x0 + 9 * j, 742 + (j % 2) * 4, 26, round(t_men + .06 * g + .02 * j, 2), "#cbbca8"))
    out += [lab(889, 640, "2,000 men", t_men + 1.4, BONE, 32), lab(1660, 690, "each group: 100", t_men + 1.8, DIM, 24, "end")]
    return out


def s56():
    """Heracleides, very likely of Plato's own school (the Academy, hedged: dashed), writes that it happened by night, in his time,
    and the whole district vanished (Strabo 8.7.2)."""
    sid = "s56"
    t_her, t_sch, t_says, t_van = T(sid, "Heracleides"), T(sid, "own school"), T(sid, "says it happened"), T(sid, "vanished")
    els = [line([[880, 0], [880, 170]], .2, "#8a6a48", 2, draw=False), poly([[850, 170], [910, 170], [900, 192], [860, 192]], "#c9905a", at=.2),
           glow(880, 200, 120, .3, .9, "fire"), glow(880, 400, 640, .3, .3, "lamp"),
           line([[0, 700], [W_, 700]], -1, "rgba(255,226,190,.3)", 1.5, draw=False)]
    els += [person(700, 700, 230, t_her - .4, "#e0cfb0"), lab(700, 752, "Heracleides", t_her, BONE, 30)]
    els += seated(1060, 700, 260, t_sch - .6) + [lab(1080, 752, "Plato", t_sch - .3, BONE, 30)]
    els += [line([[722, 470], [880, 430], [1060, 500]], t_sch, GOLD, 2, "inferred", .8), lab(880, 410, "the Academy", t_sch + .3, GOLD, 26)]
    els += [box(170, 300, 380, 250, PAPY, "#8a6a3e", 2, 8, t_her + .2, fx="pop"), box(156, 292, 22, 266, "#cdb58a", "#8a6a3e", 2, 10, t_her + .2),
            box(542, 292, 22, 266, "#cdb58a", "#8a6a3e", 2, 10, t_her + .2), line([[560, 470], [650, 520]], t_her + .3, "#8a6a3e", 2, draw=False)]
    els += [{"k": "glyphs", "x": 200, "y": 322 + 34 * k, "w": 320, "h": 26, "rows": 1, "cols": 9, "kind": "latin", "c": "#5a4632", "op": .8, "in": round(t_says + .35 * k, 2), "fx": "draw", "dur": .35}
            for k in range(5)]
    els += [wave(230, 490, 515, t_van, "#3f6f88", 8, 6, 3, .6), glow(360, 500, 120, t_van, .5, "lamp")]
    return {"base": "dark", "stars": 20, "cam": [1, 889, 470], "els": els}


def s58():
    """About 150 years later, ferrymen said a bronze statue still stood under the water (Strabo, citing Eratosthenes): a ferry, the
    drowned stones, a plinth and a dotted outline of what they reported. No god is drawn."""
    sid = "s58"
    t_later, t_ferry, t_bronze, t_under = T(sid, "A century and a half"), T(sid, "ferrymen"), T(sid, "bronze"), T(sid, "under the water")
    els = [box(0, 300, W_, 500, "#163142", r=0, at=-1), wave(0, W_, 300, -1, "#bfe6f5", 6, 40, 3, .8),
           poly([[0, 720], [600, 712], [1200, 724], [1778, 716], [1778, 800], [0, 800]], "#3a302a", "#8a7a66", 1.5, -1)]
    els += chip(330, 190, "about 150 years later", t_later, AMBER, 28)
    els += [{"k": "boat", "x": 600, "y": 300, "w": 180, "in": t_ferry - .4, "fx": "rise"}, person(620, 286, 70, t_ferry - .2, "#e8d6b8"),
            line([[650, 230], [700, 380]], t_ferry, "#c9905a", 4, draw=False)]
    for k, (x, h) in enumerate(((960, 110), (1020, 70), (1180, 130), (1240, 50), (1300, 96))):
        els.append(box(x, 712 - h, 26, h, "#6f7f88", "#a8b8c0", 1.5, 2, round(t_under - .4 + .1 * k, 2), op=.75))
    els += [box(1060, 640, 90, 72, "#6f7f88", "#a8b8c0", 2, 3, t_bronze - .2), glow(1105, 560, 120, t_bronze, .55, "lamp"),
            {"k": "rect", "x": 1072, "y": 450, "w": 66, "h": 186, "r": 30, "fill": "rgba(150,170,120,.12)", "c": LILAC, "sw": 2.5, "style": "claimed", "in": t_bronze + .2},
            lab(1105, 420, "a bronze statue?", t_bronze + .5, LILAC, 30),
            line([[700, 330], [1060, 560]], t_bronze + .8, LILAC, 2, "claimed", .8)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


DELTA = [(0, "#4f6a3a"), (12, "#7a6248"), (90, "#8a7458"), (180, "#5f4c39"), (240, "#7a6a58"), (320, "#6a5442"), (400, "#4a3c30")]


def s59():
    """Helike found: between 1991 and 2002, 99 boreholes into the river delta (Soter & Katsonopoulou 2011), like straws pushed into a
    layer cake to read its layers."""
    sid = "s59"
    t_found, t_yr, t_99, t_cake = T(sid, "has been found"), T(sid, "Between"), T(sid, "ninety nine"), T(sid, "layer cake")
    sy = 360
    els = []
    for k, (d, c) in enumerate(DELTA):
        nxt = DELTA[k + 1][0] if k + 1 < len(DELTA) else 450
        els.append(box(80, sy + d, 1300, nxt - d, c, r=0, at=-1))
    els += [line([[80, sy], [1380, sy]], -1, "rgba(255,226,190,.5)", 2, draw=False)]
    els += [line([[120 + 40 * j, sy - 4], [128 + 40 * j, sy - 16]], -1, "#8fb06a", 3, draw=False) for j in range(30)]
    els += [box(1240, sy - 6, 70, 30, SEA, r=6, at=-1), lab(1275, sy - 30, "river", .3, BLUE, 26)]
    els += chip(300, 250, "1991 to 2002", t_yr, AMBER, 28) + [lab(830, 300, "Helike", t_found - .2, AMBER, 32), line([[830, 312], [830, 354]], t_found, AMBER, 2, "inferred", .4)]
    els += [line([[150 + 50 * j, sy], [150 + 50 * j, 760]], round(t_99 - .3 + .12 * j, 2), "#e8e0d0", 2, dur=.3) for j in range(22)]
    gx, gy = 1430, 150
    els += [box(1395, 120, 270, 300, "rgba(13,11,9,.9)", "rgba(255,226,190,.35)", 2, 12, t_99 - .5, fx="pop")]
    els += [dot(gx + 24 * (k % 10) + 12, gy + 22 * (k // 10) + 4, 7, GOLD, round(t_99 + .035 * k, 3)) for k in range(99)]
    els += [lab(1530, 404, "99 boreholes", t_99 + 3.4, GOLD, 28)]
    els += [box(1395, 450, 270, 320, "rgba(13,11,9,.9)", "rgba(255,226,190,.35)", 2, 12, t_cake - .4, fx="pop"),
            box(1420, 590, 150, 30, "#5a3a2a", r=0, at=t_cake - .2), box(1420, 620, 150, 30, "#efe2c4", r=0, at=t_cake - .2), box(1420, 650, 150, 30, "#8a4a3a", r=0, at=t_cake - .2),
            box(1420, 680, 150, 34, "#c99a6a", r=0, at=t_cake - .2), box(1416, 714, 158, 8, "#cbd2d8", r=3, at=t_cake - .2),
            box(1600, 560, 22, 160, "rgba(255,255,255,.18)", "#ffffff", 1.5, 6, t_cake + .5, fx="rise"),
            box(1603, 590, 16, 30, "#5a3a2a", r=0, at=t_cake + .9), box(1603, 620, 16, 30, "#efe2c4", r=0, at=t_cake + .9),
            box(1603, 650, 16, 30, "#8a4a3a", r=0, at=t_cake + .9), box(1603, 680, 16, 34, "#c99a6a", r=0, at=t_cake + .9)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s60_add():
    """Ruins about 3 m down, in the mud of an old lagoon, under what is dry land today (60 units = 1 m; a person, 1.7 m)."""
    sid = "s60"
    t_ru, t_3, t_lag, t_dry = T(sid, "Ruins"), T(sid, "three metres"), T(sid, "old lagoon"), T(sid, "dry land")
    sy = 360
    out = [box(80, sy + 160, 1300, 70, "#5f7480", r=0, at=t_lag - .3, op=.85), lab(330, sy + 205, "old lagoon", t_lag, "#e6f0f7", 28)]
    for k, (x, h) in enumerate(((700, 50), (760, 36), (860, 56), (930, 30))):
        out.append(box(x, sy + 220 - h, 34, h, "#c8b890", "#efe2c4", 1.5, 2, round(t_ru + .1 * k, 2), fx="rise"))
    out += [poly([[790, sy + 214], [810, sy + 204], [830, sy + 214]], "#a0502a", at=t_ru + .5), poly([[812, sy + 216], [832, sy + 206], [852, sy + 216]], "#a0502a", at=t_ru + .6),
            lab(830, sy + 262, "walls, roof tiles", t_ru + .8, BONE, 26),
            {"k": "dim", "x1": 1040, "y1": sy, "x2": 1040, "y2": sy + 180, "t": "3 m", "c": AMBER, "in": t_3, "lx": 34},
            person(990, sy, 102, t_dry - .4, BONE), line([[600, sy], [600, sy - 60]], t_dry - .2, "#6b4f34", 6, draw=False),
            oval(600, sy - 80, 50, 34, "#7a8a5a", "#3a4a2a", 1.5, 1, t_dry - .2), lab(420, sy - 40, "dry land today", t_dry + .2, "#c9d79a", 28)]
    return out


def s61():
    """Plato's life, about 428 to 348 BCE; Helike drowned in 373 BCE, when he was in his fifties; about a dozen years later he wrote
    the Timaeus and the Critias (about 360 BCE)."""
    sid = "s61"
    t_dr, t_fif, t_doz, t_wr = T(sid, "drowned"), T(sid, "in his fifties"), T(sid, "About a dozen"), T(sid, "he wrote")
    X = lambda bce: round(160 + (440 - bce) / 110 * 1440, 1)
    ay = 600
    els = [axis(160, 1600, ay, [(X(440), "440 BCE"), (X(420), "420"), (X(400), "400"), (X(380), "380"), (X(360), "360"), (X(340), "340")], .2),
           wave(X(373) - 50, X(373) + 50, 450, t_dr, BLUE, 12, 3, 4, .6), wave(X(373) - 50, X(373) + 50, 474, t_dr + .2, BLUE, 12, 3, 4, .6),
           line([[X(373), 490], [X(373), ay]], t_dr + .3, BLUE, 2, "inferred", .4), lab(X(373), 400, "Helike", t_dr + .4, BLUE, 30),
           bar(X(428), X(348), 540, t_fif - .8, AMBER, 16, 1.4), lab(X(428), 510, "Plato's life", t_fif - .6, AMBER, 28, "start"),
           person(X(373) - 36, 532, 64, t_fif, BONE), glow(X(373) - 36, 500, 60, t_fif + .2, .6, "lamp")]
    els += scroll(X(360), 456, 64, t_wr - .2) + [line([[X(360), 490], [X(360), ay]], t_wr, GOLD, 2, "inferred", .4), lab(X(360) + 10, 400, "Timaeus, Critias", t_wr + .2, GOLD, 28, "start")]
    els += bracket(X(373), X(360), 690, t_doz, None, BONE, up=False) + [lab((X(373) + X(360)) / 2, 730, "about 13 years", t_doz + .3, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s62():
    """Did Helike shape the ending of Plato's story (Giovannini 1985)? We can't know: a real drowning in his lifetime beside his
    story's drowned city, joined by a question; he did not need 9,000 years to picture a drowning."""
    sid = "s62"
    t_hel, t_end, t_know, t_never = T(sid, "Helike"), T(sid, "ending of his story"), T(sid, "We can't"), T(sid, "nine thousand")
    els = [box(160, 200, 600, 400, "rgba(13,11,9,.6)", BLUE, 2, 12, t_hel - .4), box(162, 420, 596, 178, "#1f5670", r=0, at=t_hel + .4, op=.9, fx="fill", dur=.8)]
    els += f04._houses(240, 470, 8, t_hel - .2, 44, "#d9c9a6") + temple_line(620, 470, 90, t_hel - .1, "#efe6d2", "known", 3)
    els += [wave(162, 758, 420, t_hel + .9, "#bfe6f5", 10, 10, 3, .6), lab(460, 650, "Helike, 373 BCE", t_hel + .2, BLUE, 30)]
    els += [box(1020, 200, 600, 400, "rgba(13,11,9,.6)", LILAC, 2, 12, t_end - .4, style="claimed")]
    els += city_plan(1320, 390, 16, t_end - .2, .35, ghost=True) + [wave(1022, 1618, 430, t_end + .6, LILAC, 10, 10, 3, .6), lab(1320, 650, "Plato's story", t_end, LILAC, 30)]
    els += [arrow([[780, 400], [1000, 400]], t_end + 1.0, BONE, 3, "inferred", .8, curve=False)] + I.question(890, 370, t_know, 80)
    els += [lab(1320, 250, "9,000 years ago?", t_never - .2, LILAC, 28), strike(1210, 240, 1430, 240, t_never + .6, RED, 4)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 470], "els": els}


def s63():
    """An old warning about pride wrapped around something true: under the night sea, a drowned shoreline and the stones of a
    settlement (solid, dim); on the surface, the reflection of a ring city (dotted: a story) breaking in the waves."""
    sid = "s63"
    t_pride, t_coast, t_cities = T(sid, "warning about pride"), T(sid, "coasts really"), T(sid, "cities really")
    els = [{"k": "water", "y": 420, "h": 700, "op": .9, "in": -1},
           poly([[0, 400], [160, 392], [340, 404], [460, 424], [520, 440], [0, 446]], "#2a2228", "rgba(255,226,190,.3)", 1.5, -1, curve=True),
           person(230, 398, 46, .3, "#e8d6b8"), glow(270, 384, 90, .4, .9, "fire"), dot(270, 390, 6, "#ffcf8a", .4)]
    els += city_plan(1150, 470, 20, t_pride, .14, ghost=True)
    els += [glow(1150, 470, 300, t_pride + .5, .25, "lamp")]
    els += [{"k": "line", "p": [[300, 600], [700, 640], [1100, 660], [1500, 650], [1778, 660]], "c": "#7fb4cc", "w": 2, "curve": True, "op": .7, "keepop": True,
             "in": t_coast, "fx": "draw", "dur": 1.4}]
    els += [box(780 + 46 * k, 668 - (k % 3) * 8, 22, 30 + (k % 3) * 8, "#6f8f9f", r=2, at=round(t_cities - .4 + .1 * k, 2), op=.55) for k in range(8)]
    els += [glow(950, 680, 200, t_cities, .35, "lamp")] + [wave(980 + 80 * k, 1060 + 80 * k, 474 + (k % 2) * 8, round(t_cities + .6 + .15 * k, 2), "#bfe6f5", 4, 2, 2, .4) for k in range(5)]
    return {"base": "sky", "tod": "night", "ground": 1300, "sun": False, "moon": [1500, 170, 24], "cam": [1, 889, 500], "els": els}


# ================================================================== chapter 6: the weighing
COLS = [(100, 620, "established", GOLD), (660, 1120, "open", LILAC), (1160, 1680, "ruled out", RED)]


def s64():
    """The whole file as a ledger: established, open, ruled out. Established: Plato's text (about 360 BCE, the only ancient source);
    the Ice Age seas rose more than 120 m; Helike sank in 373 BCE; Thera exploded around 1600 BCE."""
    sid = "s64"
    t_est, t_pl, t_sea, t_hel, t_th = T(sid, "Established"), T(sid, "Plato wrote"), T(sid, "Ice Age seas"), T(sid, "Helike sank"), T(sid, "Thera exploded")
    els = []
    for k, (x0, x1, t, c) in enumerate(COLS):
        els += [box(x0, 130, x1 - x0, 560, "rgba(13,11,9,.55)", c, 2.5, 14, round(.3 + .2 * k, 2), fx="pop"), lab((x0 + x1) / 2, 180, t, round(.4 + .2 * k, 2), c, 30)]
    els += [glow(360, 180, 160, t_est, .5, "lamp")]
    x = 180
    els += scroll(x, 270, 70, t_pl) + [lab(x + 60, 280, "360 BCE: Plato", t_pl + .4, BONE, 28, "start"), lab(x + 60, 314, "the only ancient source", t_pl + 2.0, DIM, 24, "start")]
    els += [line([[x - 40, 420], [x - 20, 414], [x, 400], [x + 14, 380], [x + 30, 372], [x + 40, 370]], t_sea, BLUE, 4, curve=True, dur=.6),
            lab(x + 60, 400, "seas rose 120 m+", t_sea + .4, BONE, 28, "start")]
    els += f04._houses(x - 40, 540, 3, t_hel, 22, "#d9c9a6") + [wave(x - 44, x + 40, 506, t_hel + .2, BLUE, 8, 3, 3, .4), lab(x + 60, 524, "Helike, 373 BCE", t_hel + .4, BONE, 28, "start")]
    els += volcano(x, 640, 40, t_th) + [lab(x + 60, 628, "Thera, about 1600 BCE", t_th + .4, BONE, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": [1, 889, 500], "els": els}


def s65_add():
    """Open: Plato's date beside the end of the ice, a clue to check, not an answer; what inspired him: Helike, old tales of Thera,
    or his own imagination."""
    sid = "s65"
    t_pd, t_ice, t_clue, t_still, t_hel, t_th, t_im = (T(sid, "Plato's date"), T(sid, "end of the ice"), T(sid, "a clue"), T(sid, "Still open"), T(sid, "whether Helike"),
                                                        T(sid, "tales of Thera"), T(sid, "imagination"))
    out = [dot(845, 296, 12, AMBER, t_pd), lab(845, 340, "9600", t_pd + .2, AMBER, 26), dot(935, 296, 12, BLUE, t_ice), lab(935, 340, "9700", t_ice + .2, BLUE, 26),
           lab(890, 374, "BCE", t_ice + .3, DIM, 24)]
    out += magnifier(890, 304, 92, t_clue, BONE)
    out += scroll(890, 612, 70, t_still)
    out += [wave(700, 780, 470, t_hel, BLUE, 8, 3, 3, .4), wave(700, 780, 490, t_hel + .1, BLUE, 8, 3, 3, .4)] + volcano(890, 500, 34, t_th, erupt=False)
    out += [{"k": "poly", "p": [[1050, 510], [1030, 490], [1042, 466], [1070, 460], [1092, 470], [1080 + 34, 464], [1132, 482], [1124, 508], [1090, 516]], "fill": "rgba(201,193,238,.15)",
             "c": LILAC, "w": 2.5, "curve": True, "in": t_im}, dot(1060, 532, 6, LILAC, t_im + .1), dot(1050, 548, 4, LILAC, t_im + .2)]
    out += [arrow([[740, 510], [860, 586]], t_hel + .3, LILAC, 2, "inferred", .4), arrow([[890, 520], [890, 578]], t_th + .3, LILAC, 2, "inferred", .4),
            arrow([[1056, 560], [924, 590]], t_im + .3, LILAC, 2, "inferred", .4)] + I.question(1030, 640, t_im + .8, 60)
    return out


def s66_add():
    """Ruled out: a real island empire beyond Gibraltar, sunk around 9600 BCE (the sea floor, the rocks and the digs agree);
    and the Eye, the Bimini stones and Spartel Bank as Plato's city: natural, too young, too small."""
    sid = "s66"
    t_emp, t_gib, t_96, t_out, t_floor, t_rocks, t_digs, t_eye, t_bim, t_sp, t_nat, t_young, t_small = (
        T(sid, "A real island"), T(sid, "beyond Gibraltar"), T(sid, "ninety six hundred"), T(sid, "Ruled out"), T(sid, "sea floor"), T(sid, "the rocks"), T(sid, "the digs"),
        T(sid, "And the Eye"), T(sid, "Bimini stones"), T(sid, "Spartel Bank"), T(sid, "Natural"), T(sid, "too young"), T(sid, "too small"))
    cx = 1440
    out = city_plan(cx, 280, 7.0, t_emp, .38, ghost=True) + f04._pillars(1200, 320, 50, t_gib, "#efe6d2") + [lab(cx, 360, "9600 BCE", t_96, LILAC, 26),
                                                                                                              strike(1180, 340, 1650, 230, t_out, RED, 6)]
    out += chip(1420, 732, "Ruled out", t_out + .3, RED, 30)
    out += [line([[1240, 470], [1270, 430], [1300, 470]], t_floor, BONE, 3, dur=.3), arrow([[1270, 420], [1330, 330]], t_floor + .2, BONE, 2, dur=.3, curve=False),
            line([[1400, 470], [1460, 470]], t_rocks, BONE, 3, dur=.2), line([[1400, 455], [1460, 455]], t_rocks + .05, BONE, 3, dur=.2), line([[1400, 440], [1460, 440]], t_rocks + .1, BONE, 3, dur=.2),
            arrow([[1430, 425], [1430, 330]], t_rocks + .2, BONE, 2, dur=.3, curve=False),
            line([[1590, 420], [1590, 475]], t_digs, BONE, 3, dur=.3), dot(1590, 478, 6, BONE, t_digs), arrow([[1580, 415], [1530, 330]], t_digs + .2, BONE, 2, dur=.3, curve=False)]
    out += [ring(1260, 570, 34, t_eye, AMBER, 3, dur=.4), ring(1260, 570, 20, t_eye + .1, AMBER, 3, dur=.4)]
    out += f04._block(1390, 592, 70, 42, t_bim, "#c9b48c", fx="pop")
    out += [oval(1560, 576, 16, 10, "#8a7450", at=t_sp), oval(1594, 584, 12, 8, "#8a7450", at=t_sp + .1), oval(1622, 572, 10, 7, "#8a7450", at=t_sp + .2)]
    out += [lab(1260, 646, "natural", t_nat, BONE, 26), lab(1425, 646, "too young", t_young, BONE, 26), lab(1592, 646, "too small", t_small, BONE, 26)]
    return out


def s67():
    """What would change our minds: a text about Atlantis older than Plato (wanted, not found)."""
    sid = "s67"
    t_text, t_old = T(sid, "A text about"), T(sid, "older than Plato")
    X = lambda bce: round(200 + (1000 - bce) / 640 * 1200, 1)
    ay = 560
    els = [axis(200, X(360), ay, [(X(1000), "1000 BCE"), (X(800), "800"), (X(600), "600"), (X(400), "400")], .3),
           box(X(360) - 4, ay - 60, 8, 120, GOLD, r=3, at=.4)]
    els += scroll(X(360), 450, 80, .6) + [lab(X(360), 370, "Plato, 360 BCE", .8, GOLD, 28)]
    els += scroll(X(680), 450, 80, t_text, LILAC, "claimed") + [lab(X(680), 370, "older than Plato?", t_text + .3, LILAC, 30)]
    els += [{"k": "line", "p": I.ellipse(X(680), 450, 220, 40, 30, 200, 340), "c": BONE, "w": 2, "style": "inferred", "curve": True, "in": t_old, "fx": "draw", "dur": 1.0}]
    els += magnifier(X(680) + 30, 456, 64, t_old + .6, BONE) + [lab(X(680), 680, "not yet found", t_old + 1.2, DIM, 28)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 470], "els": els}


def s68():
    """Or: on a drowned Ice Age shore, a city with metal, ships or writing, securely dated before the ice ended (wanted, dotted);
    or walls on Spartel Bank, where sonar has so far shown only natural rock. The shores are real and almost unsearched."""
    sid = "s68"
    t_shore, t_met, t_shp, t_wri, t_date, t_sp, t_none, t_real = (T(sid, "drowned Ice Age"), T(sid, "metal"), T(sid, "ships"), T(sid, "writing"), T(sid, "securely dated"),
                                                                  T(sid, "Spartel Bank"), T(sid, "shown none"), T(sid, "Those shores"))
    floor = [[80, 560], [600, 580], [1000, 596], [1250, 612], [1300, 600], [1380, 470], [1480, 440], [1580, 470], [1650, 600], [1700, 610]]
    els = [box(80, 250, 1620, 550, "#163142", r=0, at=-1), wave(80, 1700, 250, -1, "#bfe6f5", 5, 36, 2, .8),
           poly(floor + [[1700, 800], [80, 800]], "#3a302a", "#8a7a66", 1.5, -1)]
    els += steamer(480, 250, 44, .3) + [{"k": "fan", "x": 480, "y": 262, "r": 290, "a0": 70, "a1": 110, "n": 9, "c": BLUE, "in": t_shore + .4},
                                        line([[470, 262], [470, 575]], t_date - .3, "#e8c35a", 2, dur=.8), box(462, 572, 16, 22, "#e8c35a", r=2, at=t_date + .4)]
    els += [f04._diver(780, 400, 80, t_shore), glow(800, 440, 60, t_shore + .2, .8, "lamp")]
    els += [poly([[600, 584], [636, 520], [656, 528], [626, 590]], "rgba(201,193,238,.1)", LILAC, 3, t_met, style="claimed"),
            line([[613, 588], [600, 614]], t_met, LILAC, 4, "claimed", draw=False)]
    els += trireme(780, 590, 170, t_shp, LILAC, "claimed")
    els += [box(910, 530, 74, 62, "rgba(201,193,238,.1)", LILAC, 3, 6, t_wri, style="claimed")] + \
        [line([[922, 546 + 12 * j], [972, 546 + 12 * j]], t_wri + .1, LILAC, 2.5, "claimed", draw=False) for j in range(3)]
    els += chip(780, 470, "before 9700 BCE", t_date, LILAC, 26)
    els += steamer(1480, 250, 36, t_sp - .6) + [{"k": "fan", "x": 1480, "y": 262, "r": 180, "a0": 60, "a1": 120, "n": 11, "c": BLUE, "in": t_sp},
                                                lab(1480, 160, "Spartel Bank", t_sp + .2, GOLD, 30),
                                                {"k": "line", "p": [[1330, 560], [1380, 470], [1480, 440], [1580, 470], [1630, 560]], "c": "#ffcf9a", "w": 4, "in": t_none - .6, "fx": "draw", "dur": .8},
                                                lab(1480, 520, "natural rock", t_none - .2, "#ffcf9a", 26), lab(1480, 560, "no walls", t_none + .3, DIM, 24)]
    els += [glow(800, 580, 70, t_real, .9, "lamp"), {"k": "line", "p": [[100, 700], [100, 716], [1240, 716], [1240, 700]], "c": LILAC, "w": 2, "in": t_real + .6, "fx": "draw", "dur": .8},
            lab(670, 752, "almost unsearched", t_real + 1.2, LILAC, 28)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s69():
    """The sea really did swallow coasts; Plato gave them a city: dawn over the sea, a drowned shoreline under it, and for a moment
    the ring city's outline on the water."""
    sid = "s69"
    t_sea, t_city = T(sid, "The sea really"), T(sid, "Plato gave")
    els = [{"k": "water", "y": 430, "h": 600, "op": .88, "in": -1},
           {"k": "line", "p": [[80, 620], [500, 650], [900, 660], [1300, 650], [1700, 662]], "c": "#7fb4cc", "w": 2, "curve": True, "op": .6, "keepop": True, "in": t_sea, "fx": "draw", "dur": 1.6}]
    els += [box(560 + 44 * k, 670 - (k % 3) * 8, 20, 28 + (k % 3) * 8, "#6f8f9f", r=2, at=round(t_sea + .8 + .1 * k, 2), op=.5) for k in range(7)]
    els += city_plan(889, 480, 22, t_city, .12, ghost=True) + [glow(889, 480, 360, t_city + .4, .3, "lamp")]
    return {"base": "sky", "tod": "dawn", "ground": 1300, "sun": [1250, 430, 34], "cam": [1, 889, 500], "els": els}


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(0, "Ten kings", "s2"), (1, "Then, in a single", "s3"), (1, "People have searched", "s4"), (1, "And every search", "s5")], {}),
    (0, 1, "title", "s5", [], {"intro": True}),
    (1, 0, "world", "s7", [(0, "conversations set down", "s8"), (1, "Egyptian priests", "s9"), (1, "Solon's story", "s10")], {"chapter": "The only witness"}),
    (1, 1, "collision", "s11", [(0, "A ring city", "s12"), (1, "And Socrates", "s13")], {}),
    (1, 2, "reversal", "s14", [(0, "So Critias sets", "s15"), (1, "No older text", "s16"), (1, "And the Critias breaks", "s16b")], {}),
    (1, 3, "tag", "s17", [], {}),
    (2, 0, "world", "s18", [], {"chapter": "A date at the end of the ice"}),
    (2, 1, "collision", "s18", [(0, "Greenland's ice", "s19"), (0, "Counting the pages", "s20")], {}),
    (2, 2, "cost", "s21", [(0, "Britain was joined", "s22"), (0, "Then the melt", "s23"), (1, "And people lived", "s24")], {}),
    (2, 3, "reversal", "s25", [(0, "And Atlantis keeps", "s26"), (1, "The rising sea", "s26b")], {}),
    (3, 0, "world", "s27", [(0, "Donnelly read", "s28")], {"chapter": "No room on the sea floor"}),
    (3, 1, "collision", "s29", [(0, "Ping by ping", "s30"), (0, "In {1968", "s31")], {}),
    (3, 2, "reversal", "s32", [(0, "Lava wells up", "s32b"), (0, "Since Plato's date", "s33")], {}),
    (3, 3, "cost", "s34", [(0, "Both float", "s34b"), (0, "Beyond Gibraltar", "s35")], {}),
    (3, 4, "reversal", "s36", [(0, "At the Ice Age low", "s37"), (1, "But rising seas", "s38"), (1, "The geologist", "s39")], {}),
    (4, 0, "world", "s40", [], {"chapter": "Three places on the map"}),
    (4, 1, "collision", "s41", [(0, "At first glance", "s42"), (0, "But Plato's whole city", "s43"), (1, "Its rings are", "s44")], {}),
    (4, 2, "cost", "s45", [(1, "But it's beachrock", "s46"), (1, "Cores show", "s47")], {}),
    (4, 3, "reversal", "s48", [(0, "It buried", "s49"), (0, "Nearby on Crete", "s50"), (0, "A Greek seismologist", "s51"), (1, "But nothing in the text", "s52"),
                               (1, "Even its date", "s53"), (1, "A real catastrophe", "s48b")], {}),
    (5, 0, "world", "s54", [(0, "The city of", "s55")], {"chapter": "The city that really sank"}),
    (5, 1, "collision", "s56", [(0, "Two thousand men", "s57"), (0, "A century and a half", "s58")], {}),
    (5, 2, "cost", "s59", [(0, "Ruins lay", "s60")], {}),
    (5, 3, "reversal", "s61", [(0, "Some scholars", "s62")], {}),
    (5, 4, "tag", "s63", [], {}),
    (6, 0, "weigh", "s64", [(0, "Plato's date beside", "s65"), (1, "A real island", "s66")], {"chapter": "The weighing"}),
    (6, 1, "test", "s67", [(0, "Or, on a drowned", "s68")], {}),
    (6, 2, "close", "s69", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1.6, 889, 600], "s2_add"), "s3": ("s1", [1, 889, 500], "s3_add"), "s9": ("s7", [1, 889, 500], "s9_add"),
    "s16b": ("s16", [1.75, 1350, 300], "s16b_add"), "s20": ("s18", [1.25, 700, 600], "s20_add"), "s26": ("s25", [1, 889, 500], "s26_add"),
    "s26b": ("s25", [1, 889, 500], "s26b_add"), "s28": ("s27", [1, 889, 500], "s28_add"), "s38": ("s37", [1, 889, 500], "s38_add"),
    "s39": ("s37", [1, 889, 500], "s39_add"), "s48b": ("s48", [1.4, 916, 520], "s48b_add"), "s57": ("s55", [1, 889, 500], "s57_add"),
    "s60": ("s59", [1.4, 800, 470], "s60_add"), "s32b": ("s32", [1.12, 930, 440], None), "s34b": ("s34", [1.12, 1000, 420], None), "s65": ("s64", [1.15, 890, 480], "s65_add"), "s66": ("s64", [1, 889, 500], "s66_add"),
}


def _segments(script):
    """The narration each shot has on screen, from the beats with their markers (a chapter beat's first sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            if sid in ALIASES and ALIASES[sid][2] is None:      # a new framing only: the words stay with the panel's own clock
                continue
            lines[li] = _mark(lines[li], phrase, "[@%s]" % sid)
        text = " ".join(lines)
        parts = re.split(r"\[@([\w]+)\]", text)
        head = parts[0]
        if kw.get("chapter"):
            acts = [m.start() for m in re.finditer(r"\[act:", head)]
            if len(acts) > 1:
                head = head[acts[1]:]
        if role != "title":
            say[frm] = say.get(frm, "") + " " + head if frm in say else head
        for k in range(1, len(parts), 2):
            say[parts[k]] = parts[k + 1]
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
    ep = {"id": "lf-atlantis", "code": "LF.02", "series": script["series"], "title": script["title"], "case": "atlantis",
          "verdict": "debunked", "claim": "Was Atlantis a real island empire that sank beyond Gibraltar around 9600 BCE?", "mood": "mystery",
          "hook_text": "Could an empire really sink in one *night*?", "beats": beats, "shots": shots,
          "sources": "Plato, Timaeus and Critias (trans. Jowett 1892) · Walker et al. 2009 (doi:10.1002/jqs.1227) · Lambeck et al. 2014 (doi:10.1073/pnas.1411762111) · "
                     "Gutscher 2005 (doi:10.1130/G21597AR.1) · McKusick & Shinn 1980 (doi:10.1038/287011a0) · Friedrich et al. 2006 (doi:10.1126/science.1125087) · "
                     "Soter & Katsonopoulou 2011 (doi:10.1002/gea.20366)",
          "post": "Atlantis, weighed: one ancient source, a date at the end of the Ice Age, a sea floor with no room for a continent, four places people searched, and a Greek city that really sank in Plato's lifetime.",
          "hashtags": ["#Atlantis", "#Plato", "#IceAge", "#History", "#Archaeology"],
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
