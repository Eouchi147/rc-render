"""LF.08 · Underworlds · The Cities Under Cappadocia (16:9 long film, one wall; see films/long/LONG_ENGINE.md).

The script is films/long/lf-derinkuyu/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added
at the sentence where the picture changes (see BEATS). One scene per script shot (s1..s53; s5, the title hold, is the panel of s4
under the intro card), drawn while it is said: the basement wall of 1963 and the city below it, the volcanic ash that made the
tuff, the rolling doors, the other underground cities (Kaymakli, Ozkonak, Nevsehir), the Ice Age claim at its strongest, why a
carved room cannot be dated and why carving erases its own history, what can be dated (crosses, churches, Byzantine pottery,
raids, a scholar's notes of 1910, 1923), and the weighing.

The city, the film's central picture, is ONE drawing made by the same functions wherever it recurs (the opening at dusk, the night
of the question, the tour by day, the deepest level, the survey, the close): the house where it was found and its basement, the
room behind the basement wall, then 8 levels as well-spaced strata of soft tuff down to about 85 m (7 units a metre, true depth),
each a few vaulted chambers joined by passages, a stair down to the next level and a stone wheel door at its foot, the deep shaft
(air shaft and well) from the surface to water, a person for scale. Chambers, passages and wheels are drawn about twice life size
so they read on a phone; depths are to scale. A shot dims the levels it does not name (a veil) and lights the one it names (its
stratum redrawn, its rooms lamp-lit), building in as the narration names them; never more than about 6 labels on a panel.

Drawings are schematic and true to the numbers said: 85 m, the 25-storey ghost to the same height, the door wheels to their
measured range (1.2 to 1.85 m, Yamac 2022), the water at about 70 m (Dawkins 1916). Solid = measured or documented, dashed =
inferred or proposed, dotted = claimed (the Ice Age shelter, Yima's refuge, the comet). Religions with respect: Yima's refuge is
drawn as an enclosure in the claimed style, with no text of any scripture; churches and crosses are drawn as plans and
incisions, as dating evidence. The massacres of 1909 are not shown: lamps go down.

Reused from the Shorts: derinkuyu (f07.derinkuyu_m: the basement, the city, the 25-storey ghost, the tour, the door seen from
inside, the 13,000-year timeline, the scraped room, the dots around Derinkuyu) and longyou-caves (f07.longyou: its iso hall), all
redrawn wide for 16:9.

Engine workaround (as in lf_atlantis.py): the wall only adds elements to a panel on its first visit, at a beat start or a line
start; shots that add to a panel they return to mid-line are aliases of that panel with a camera whose zoom carries a tiny unique
tag (+0.0001 per tag, invisible); after the wall is built, the step that reached that camera gets the shot's additions as a panel
item (kit.js builds them on that step's clock). Nothing can be removed from a panel, so a label that must go is covered by a
patch of the ground it sits on, and a level is dimmed by a veil laid over it.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-derinkuyu/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-derinkuyu/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-derinkuyu RC_FILMS_EPS=/tmp/claude-0/sbx_lf-derinkuyu/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-derinkuyu/boards python3 films.py long.lf_derinkuyu
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, ellipse, question

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-derinkuyu", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, GOLD, BLUE, LILAC, RED, GREEN, AU = I.BONE, I.AMBER, "#f2c98e", I.BLUE, I.LILAC, I.RED, I.GREEN, I.AU
DIM, TUFF, TUFF2, DARK, EDGE, WATER = "#cbbca8", "#c9b38a", "#b59e76", "#1a1511", "#8c7452", "#5fa8c9"
GRADE = {"established": "#8fd9b0", "awaiting": "#c9c1ee", "open": "#f0b06a"}
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


def _find(line_, phrase):
    """Index in the raw line where `phrase` starts, ignoring the ^ stress marks."""
    keep = [i for i, ch in enumerate(line_) if ch != "^"]
    flat = "".join(line_[i] for i in keep)
    assert flat.count(phrase) == 1, (phrase, line_)
    return keep[flat.index(phrase)]


def _mark(line_, phrase, tag):
    """Insert `tag` at the start of the sentence that begins with `phrase`: before its [p:]/[act:]/[sfx:]/[tune:]/[gap:] tags,
    after a [d:] mood tag."""
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
    e = {"k": "poly", "p": R(p), "fill": fill, "c": c, "w": w, "curve": curve, "in": round(at, 2) if at is not None else None}
    if style != "known":
        e["style"] = style
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(round(x, 1), round(y, 1), round(w, 1), round(h, 1), fill, c, sw, r, round(at, 2), op, fx, **kw)


def lab(x, y, t, at, c=BONE, size=28, a="middle", st="lab", **kw):
    return label(round(x, 1), round(y, 1), t, round(at, 2), c, size, a, st, **kw)


def ln(p, at, c=BONE, w=3, style="known", dur=None, curve=False, draw=True, op=None):
    return line(R(p), round(at, 2), c, w, style, dur, curve, draw, op)


def arr(p, at, c=AMBER, w=3, style="known", dur=1.0, curve=True):
    return arrow(R(p), round(at, 2), c, w, style, dur, curve)


def chip(x, y, t, at, c, size=28, a="middle", style="known"):
    """A grade chip: a dark pill with a coloured rim and its words (dashed rim: an estimate, a test not done)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    e = rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop")
    if style != "known":
        e["style"] = style
    return [e, lab(x0 + w / 2, y + size * .36, t, at + .05, c, size, halo=False)]


def tick(x, y, at, c=GREEN, s=1.0):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "draw", "dur": .45, "in": round(at, 2)}


def dimv(x, y1, y2, t, at, c=GOLD, lx=-18, dur=1.0, style="known"):
    """A vertical dimension that draws itself; its words fade in as it ends (kit.js's draw traces a dim's lines only, so a dim with
    words drawn late would show them at once): two dims on the same line, the first without words."""
    e = {"k": "dim", "x1": x, "y1": y1, "x2": x, "y2": y2, "t": "", "c": c, "fx": "draw", "dur": dur, "in": round(at, 2), "lx": lx}
    if style != "known":
        e["style"] = style
    if not t or at < 0:
        e["t"] = t
        return [e]
    w = dict(e, t=t, fx="fade", dur=.5, **{"in": round(at + dur * .7, 2)})
    return [e, w]


def cover(x, y, w, h, at, fill, op=1.0, dur=.6, r=0):
    """A sheet laid over part of a panel in its background colour: what was there fades away (op 1) or dims (op < 1)."""
    e = rect(x, y, w, h, fill, r=r, at=at, op=op)
    e["dur"] = dur
    return e


def scalebar(x, y, w, t, at, c="#e9dccb"):
    """A scale bar with its words at 24 (kit.js's own scale writes 21)."""
    return [ln([[x, y], [x + w, y]], at, c, 2, draw=False), ln([[x, y - 8], [x, y + 8]], at, c, 2, draw=False),
            ln([[x + w, y - 8], [x + w, y + 8]], at, c, 2, draw=False), lab(x + w / 2, y - 14, t, at, c, 24)]


def wheel(cx, cy, r, at, fx="pop", style="known", op=None, c="#b8a07a"):
    """A millstone door, face on: a stone disc with a hole through its centre."""
    e = {"k": "circle", "x": round(cx, 1), "y": round(cy, 1), "r": round(r, 1), "fill": c if style == "known" else "rgba(184,160,122,.25)", "c": "#fff3dc",
         "w": max(1.5, r * .03), "in": round(at, 2)}
    if style != "known":
        e["style"] = style
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    return [e, dot(round(cx, 1), round(cy, 1), round(max(2.2, r * .16), 1), DARK, round(at, 2), op=op)]


def flakes(n, x0, x1, y0, y1, at, seed=5, step=.03, s=(6, 11), c="#eef4fb", op=.9):
    """Snowflakes: little six-armed stars (so they don't read as sky stars), fading in one after another."""
    rr = random.Random(seed)
    out = []
    for k in range(n):
        x, y, r = rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(*s)
        t = round(at + step * k, 2)
        for a in (0, 60, 120):
            ca, sa = r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
            out.append(ln([[x - ca, y - sa], [x + ca, y + sa]], t, c, 1.8, draw=False, op=op))
    return out


def clock(x, y, r, at, c=BONE):
    return [{"k": "circle", "x": x, "y": y, "r": r, "fill": "rgba(18,13,10,.85)", "c": c, "w": 3, "in": round(at, 2), "fx": "pop"},
            ln([[x, y], [x, y - r * .7]], at + .2, c, 3, draw=False), ln([[x, y], [x + r * .5, y + r * .2]], at + .5, c, 3, dur=.4)]


def stair(x0, y0, x1, y1, at, n=5, c="#d8c7a8", w=2):
    """A little stair (a zig-zag) from (x0, y0) down to (x1, y1)."""
    pts = []
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        y = y0 + (y1 - y0) * k / n
        pts += [(x, y), (x + (x1 - x0) / n, y)] if k < n else [(x, y)]
    return ln(pts, at, c, w, dur=.5)


def beast(pts, x, y, s, at, c=DIM, face=1, fx="rise", op=None):
    return poly([(x + face * px * s, y + py * s) for px, py in pts], c, at=at, fx=fx, op=op)


ASS = [(-.52, -.30), (-.45, -.50), (-.10, -.52), (.20, -.52), (.30, -.62), (.34, -.80), (.33, -.92), (.37, -.84), (.40, -.92), (.40, -.80), (.52, -.62),
       (.50, -.57), (.40, -.62), (.34, -.50), (.30, -.38), (.30, 0), (.26, 0), (.24, -.32), (-.28, -.34), (-.30, 0), (-.34, 0), (-.36, -.36), (-.48, -.42)]
GOAT = [(-.42, -.50), (-.30, -.54), (.10, -.54), (.22, -.60), (.26, -.74), (.20, -.90), (.30, -.80), (.34, -.70), (.44, -.62), (.40, -.56), (.32, -.56),
        (.30, -.40), (.30, 0), (.26, 0), (.24, -.36), (-.24, -.38), (-.26, 0), (-.30, 0), (-.34, -.40), (-.44, -.46)]
COW = [(-.56, -.30), (-.50, -.52), (-.10, -.56), (.24, -.56), (.34, -.62), (.44, -.66), (.52, -.60), (.54, -.50), (.44, -.46), (.36, -.40), (.34, -.20),
       (.34, 0), (.28, 0), (.26, -.22), (-.28, -.24), (-.30, 0), (-.36, 0), (-.40, -.26), (-.52, -.30), (-.62, -.10), (-.58, -.30)]
HEN = [(-.20, -.10), (-.26, -.30), (-.10, -.36), (.08, -.34), (.14, -.46), (.22, -.48), (.28, -.42), (.24, -.36), (.20, -.24), (.10, -.10), (.04, 0), (-.02, 0), (-.04, -.08)]


def jar(x, y, h, at, c="#c8743c"):
    return {"k": "vase", "x": round(x, 1), "y": round(y, 1), "h": h, "w": h * .7, "tone": c, "in": round(at, 2), "fx": "pop"}


def church_plan(cx, cy, s, at, c=AU, w=3, fill="rgba(232,195,90,.12)", style="known"):
    """A cross-shaped church in plan (s = arm half-width)."""
    a, L = s, s * 2.6
    pts = [(cx - a, cy - L), (cx + a, cy - L), (cx + a, cy - a), (cx + L, cy - a), (cx + L, cy + a), (cx + a, cy + a), (cx + a, cy + L * 1.25),
           (cx - a, cy + L * 1.25), (cx - a, cy + a), (cx - L, cy + a), (cx - L, cy - a), (cx - a, cy - a)]
    return poly(pts, fill, c, w, at, ("draw" if fill in ("none", None) else "fade") if style == "known" else None, style=style)


def book(x, y, w, at, c="#e9d6ad"):
    """An open book (a chronicle): two pages, a spine, lines of writing."""
    h = w * .62
    out = [poly([(x, y - h * .42), (x - w / 2, y - h / 2), (x - w / 2, y + h / 2), (x, y + h * .58)], c, "#fff6e6", 1.5, at, "pop"),
           poly([(x, y - h * .42), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x, y + h * .58)], c, "#fff6e6", 1.5, at, "pop")]
    for j in range(4):
        yy = y - h * .25 + j * h * .17
        out += [ln([[x - w * .42, yy - 2], [x - w * .08, yy + 3]], at + .15, "#5a4632", 2, draw=False), ln([[x + w * .08, yy + 3], [x + w * .42, yy - 2]], at + .15, "#5a4632", 2, draw=False)]
    return out


def magnifier(x, y, r, at, c=BONE):
    return [ring(x, y, r, round(at, 2), c, 4, dur=.5), ln([[x + r * .7, y + r * .7], [x + r * 1.45, y + r * 1.45]], at + .3, c, 8, dur=.3)]


def hill(top, fill, edge, w, at, bottom=1010, **kw):
    return poly(list(top) + [(top[-1][0], bottom), (top[0][0], bottom)], fill, edge, w, at, curve=False, **kw)


def flat_house(x, gy, w, h, at, fill="#8e7152", door=True, win=True, fx=None, op=None):
    out = [rect(x, gy - h, w, h, fill, "rgba(255,236,206,.45)", 1.2, 0, at, fx, op)]
    if door:
        out.append(rect(x + w * .42, gy - h * .55, w * .16, h * .55, "#1e1712", at=at, fx=fx, op=op))
    if win:
        out.append(rect(x + w * .14, gy - h * .72, w * .14, h * .2, "#3a2c20", at=at, fx=fx, op=op))
    return out


def vault(x0, x1, fl, h, n=7):
    """A room cut into the rock, in section: a flat floor, upright walls, the ceiling's corners rounded (h tall)."""
    r = min(h * .62, (x1 - x0) / 2)
    cy = fl - h + r
    left = [(x0 + r + r * math.cos(math.radians(180 - 90 * j / n)), cy - r * math.sin(math.radians(180 - 90 * j / n))) for j in range(n + 1)]
    right = [(x1 - r + r * math.cos(math.radians(90 - 90 * j / n)), cy - r * math.sin(math.radians(90 - 90 * j / n))) for j in range(n + 1)]
    return [(x0, fl)] + left + right + [(x1, fl)]


def clip_y(pts, y0, y1):
    """The part of a polygon between the heights y0 and y1 (Sutherland-Hodgman against a horizontal band)."""
    def cut(P, keep, yc):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            ia, ib = keep(a), keep(b)
            if ib:
                if not ia:
                    out.append((a[0] + (b[0] - a[0]) * (yc - a[1]) / (b[1] - a[1]), yc))
                out.append(b)
            elif ia:
                out.append((a[0] + (b[0] - a[0]) * (yc - a[1]) / (b[1] - a[1]), yc))
        return out
    P = cut(list(pts), lambda p: p[1] >= y0, y0)
    return cut(P, lambda p: p[1] <= y1, y1) if P else []


def clip_line(pts, y0, y1):
    """The pieces of a polyline between the heights y0 and y1."""
    pieces, cur = [], []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        t0, t1 = 0.0, 1.0
        if ya == yb:
            if not y0 <= ya <= y1:
                if cur:
                    pieces.append(cur); cur = []
                continue
        else:
            for yc, lo in ((y0, True), (y1, False)):
                t = (yc - ya) / (yb - ya)
                if (yb > ya) == lo:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
            if t0 > t1:
                if cur:
                    pieces.append(cur); cur = []
                continue
        p0 = (xa + (xb - xa) * t0, ya + (yb - ya) * t0)
        p1 = (xa + (xb - xa) * t1, ya + (yb - ya) * t1)
        if cur and abs(cur[-1][0] - p0[0]) < .01 and abs(cur[-1][1] - p0[1]) < .01:
            cur.append(p1)
        else:
            if cur:
                pieces.append(cur)
            cur = [p0, p1]
    if cur:
        pieces.append(cur)
    return pieces


# ================================================================== the city: one picture, drawn by the same functions wherever it recurs
GY, PXM = 182, 7.0           # the ground line of the city panels; 7 units a metre (85 m = 595 units)
BOT = GY + 595               # 777: the deepest floor, about 85 m down
F0, H0 = GY + 34, 28         # the floor and height of the basement, and of the room found behind its wall (1963)
CH, PH = 32, 12              # a chamber's height at its crown and a passage's height: about twice life size, so they read
LVF = [GY + 91 + 72 * k for k in range(8)]           # the floors of the 8 levels drawn: 273, 345, ... 777 (about 13 to 85 m)
SHAFT = 1000                 # the deep shaft: the main air shaft and well, from the surface down to water
HOUSE, CELLAR, FOUND = (560, 660), (566, 654), (662, 752)
ROOMS = [[(400, 540, "stable"), (812, 950, "press"), (1050, 1170, "")],             # level 1
         [(420, 568, "store"), (660, 800, ""), (870, 975, "")],
         [(470, 610, ""), (812, 950, ""), (1040, 1160, "")],
         [(450, 608, ""), (700, 830, ""), (880, 985, ""), (1030, 1150, "")],
         [(500, 650, ""), (832, 975, ""), (1060, 1170, "")],
         [(470, 628, ""), (700, 960, "church"), (1040, 1150, "")],
         [(500, 640, ""), (732, 880, ""), (1040, 1160, "")],
         [(470, 628, ""), (700, 860, "deep"), (900, 985, "")]]                     # level 8, about 85 m
STAIRS = [(752, F0, 812), (640, LVF[0], 568), (740, LVF[1], 812), (680, LVF[2], 608),
          (760, LVF[3], 832), (700, LVF[4], 628), (660, LVF[5], 732), (700, LVF[6], 628)]   # stair k: (top x, top floor, foot x) down to level k
TUFF_A, TUFF_B = "#c9b38a", "#bca57d"                 # the strata: two tones of tuff, one band to a level
ROOMC, LITC, RIM, VEIL, FLOOR = "#201813", "#2c2017", "rgba(255,226,190,.42)", "#120d09", "#4a3a2b"
VEILED = "#16110d"           # an empty chamber seen through a veil (where a wheel was, once it has rolled)


def room_h(tag):
    return 40 if tag == "church" else CH


def room_of(k, tag=None, j=0):
    r = next(r for r in ROOMS[k] if r[2] == tag) if tag else ROOMS[k][j]
    return r[0], r[1], LVF[k], room_h(r[2])


def band(k):
    """The stratum of level k: from 52 above its floor to 20 below."""
    return LVF[k] - 52, LVF[k] + 20


def city_base(tod="dusk"):
    """The section: a sky strip, the plateau's surface, and the tuff in strata, one band to a level."""
    lay = [{"d": 0, "c": TUFF_A, "t": "", "tex": "blocks", "to": .05}]
    for k in range(8):
        lay.append({"d": LVF[k] - 52 - GY, "c": TUFF_B if k % 2 == 0 else TUFF_A, "t": "", "tex": "blocks", "to": .05})
    lay.append({"d": LVF[7] + 20 - GY, "c": TUFF_A, "t": "", "tex": "blocks", "to": .05})
    return {"base": "section", "tod": tod, "ground": GY, "lx": 130, "layers": lay}


def house_els(at=-1, window=False):
    """The house on the plateau where the city was found: stone walls, a flat roof, an arched door, a small annex."""
    x0, x1 = HOUSE
    out = [rect(x0 - 4, GY - 46, x1 - x0 + 8, 7, "#7a6146", "rgba(255,236,206,.4)", 1, 1, at),
           rect(x0, GY - 40, x1 - x0, 40, "#9b7f5e", "rgba(255,236,206,.45)", 1.2, 0, at),
           rect(x1, GY - 24, 34, 24, "#8a6f50", "rgba(255,236,206,.4)", 1, 0, at),
           poly(vault(602, 620, GY, 24, 8), "#1e1712", at=at),
           rect(574, GY - 31, 13, 10, "#ffd98a" if window else "#3a2c20", at=at)]
    out += [ln([[x0 + 2, GY - 20], [x1 - 2, GY - 20]], at, "rgba(60,44,30,.35)", 1, draw=False)]
    return out


def cellar_els(at=-1, lamp=True, man=True):
    """The basement under the house: a steep stair down from the house, a lamp; the man at its back wall with his pick."""
    x0, x1 = CELLAR
    out = [rect(x0, F0 - H0, x1 - x0, H0, "#2a2018", RIM, 1.4, 1, at), stair(x0 + 4, F0 - H0 + 1, x0 + 22, F0 - 1, at, 4, "#8a7050", 1.4)]
    if lamp:
        out += [glow(616, F0 - 9, 46, at, .8, "lamp"), dot(616, F0 - 3, 2.2, "#ffd98a", at)]
    if man:
        out += [person(638, F0, 12.5, at, "#efe6d4"), ln([[640, F0 - 8], [649.5, F0 - 13]], at, "#c9a46a", 1.3, draw=False),
                ln([[647.5, F0 - 16], [651, F0 - 10]], at, "#d8dde2", 1.6, draw=False)]
    return out


def wall_break(t_crack, t_open):
    """The basement's back wall: a crack runs down it, then it breaks open."""
    return [ln([(657.5, F0 - H0 + 1), (660, F0 - 22), (656.5, F0 - 16), (660, F0 - 10), (657, F0 - 5), (659, F0)], t_crack, BONE, 1.3, dur=.6),
            poly([(653.5, F0 - 24), (659, F0 - 26.5), (663, F0 - 20), (662, F0 - 3), (655, F0 - 1), (658, F0 - 12)], "#0d0a08", at=t_open, fx="pop")]


def found_room(at, lamp=True, fx="fade"):
    """The room behind the wall."""
    x0, x1 = FOUND
    out = [poly(vault(x0, x1, F0, H0), ROOMC, RIM, 1.4, at, fx)]
    if lamp:
        out.append(glow((x0 + x1) / 2 - 18, F0 - 11, 44, at + .25, .65, "lamp"))
    return out


def stair_geo(k):
    """Stair k: a sloping tunnel down to level k, its steps drawn on its floor."""
    xt, yt, xb = STAIRS[k]
    yb, s = LVF[k], (1 if xb > xt else -1)
    tun = [(xt, yt - PH), (xb + 2 * s, yb - PH), (xb + 2 * s, yb), (xt, yt)]
    n, dx, dy = 8, (xb - xt) / 8, (yb - yt) / 8
    st = []
    for j in range(n):
        st += [(xt + dx * j, yt + dy * j), (xt + dx * (j + 1), yt + dy * j)]
    st.append((xb, yb))
    return tun, st


def stair_els(k, at, bnd=None, op=None):
    tun, st = stair_geo(k)
    pieces = [st]
    if bnd:
        tun, pieces = clip_y(tun, *bnd), clip_line(st, *bnd)
    out = [poly(tun, ROOMC, at=at, fx="fade", op=op)] if len(tun) >= 3 else []
    return out + [ln(p, at, "#8a7050", 1.5, draw=False, op=op) for p in pieces if len(p) >= 2]


def door_xy(k, shut=False):
    """The wheel door at the foot of stair k: standing in its slot inside the room, or rolled across the doorway."""
    xt, yt, xb = STAIRS[k]
    s = 1 if xb > xt else -1
    return (xb - s * 3, LVF[k] - 9.5) if shut else (xb + s * 13, LVF[k] - 9.5)


def level_els(k, at, op=None, bnd=None, lit=(), lit_at=None, door=True):
    """Level k: its chambers (lit ones lamp-lit), the passages between them, the stair coming down to it and the wheel at its foot."""
    fl, rs = LVF[k], ROOMS[k]
    out = [poly(vault(x0, x1, fl, room_h(tg)), ROOMC, RIM, 1.5, at, "fade", op=op) for x0, x1, tg in rs]
    for x0, x1, tg in rs:
        if tg in lit or (x0, x1) in lit:
            ta = (lit_at or {}).get(tg, at) if isinstance(lit_at, dict) else (lit_at if lit_at is not None else at)
            h = room_h(tg)
            out += [poly(vault(x0 + 1.5, x1 - 1.5, fl, h - 1.5), LITC, at=ta, fx="fade"),
                    glow((x0 + x1) / 2, fl - h * .42, min(74, (x1 - x0) * .42), ta + .1, .85, "lamp")]
    out += [rect(a[1] - 2, fl - PH, b[0] - a[1] + 4, PH, ROOMC, at=at, fx="fade", op=op) for a, b in zip(rs, rs[1:])]
    out += [ln([[rs[0][0] + 3, fl - 1.2], [rs[-1][1] - 3, fl - 1.2]], at, FLOOR, 2.2, draw=False, op=op)]
    out += stair_els(k, at, bnd, op)
    if door:
        out += wheel(*door_xy(k), 9.5, at + .15, op=op)
    return out


def shaft_els(x, y1, at, op=None, w=14, bnd=None):
    y0 = GY - 1
    if bnd:
        y0, y1 = max(y0, bnd[0]), min(y1, bnd[1])
    return [rect(x - w / 2, y0, w, y1 - y0, ROOMC, at=at, fx="fade", op=op)] if y1 > y0 else []


def well_head(x, at, w=14):
    return [rect(x - w / 2 - 10, GY - 9, 10, 9, "#8a7454", "rgba(255,236,206,.4)", 1, 2, at), rect(x + w / 2, GY - 9, 10, 9, "#8a7454", "rgba(255,236,206,.4)", 1, 2, at)]


def water(x, at, w=14, y1=BOT):
    return [rect(x - w / 2, y1 - 20, w, 20, WATER, r=2, at=at, fx="fill")]


def city_all(at=-1, op=None, lit=None):
    """All 8 levels, the deep shaft with its well head and its water (lit: {level: room tags lamp-lit})."""
    out = []
    for k in range(8):
        out += level_els(k, at, op, lit=(lit or {}).get(k, ()))
    return out + shaft_els(SHAFT, BOT, at, op) + well_head(SHAFT, at) + water(SHAFT, at)


def city_full(tod_lamp=False, man=False, window=False):
    """The whole picture as it stands once found: the house, its basement opened into the room behind, the city below."""
    return house_els(window=window) + cellar_els(lamp=tod_lamp, man=man) + wall_break(-1, -1) + found_room(-1, lamp=False) + city_all()


def veil(at, op=.42, dur=.6):
    """Dims the whole underground: the levels not named."""
    return [cover(-10, GY + 1, 1800, 1010 - GY, at, VEIL, op, dur)]


def spot(k, at, lit=(), lit_at=None, shafts=((SHAFT, BOT),), well=False):
    """Lights level k: its stratum laid again over the veil, its rooms, passages, stairs (clipped to the band) and wheel redrawn,
    the named rooms lamp-lit."""
    y0, y1 = band(k)
    out = [rect(-10, y0, 1800, y1 - y0, TUFF_B if k % 2 == 0 else TUFF_A, at=at, fx="fade", dur=.5)]
    out += level_els(k, at, bnd=(y0, y1), lit=lit, lit_at=lit_at)
    if k < 7:
        out += stair_els(k + 1, at, (y0, y1))
    for x, yb in shafts:
        out += shaft_els(x, yb, at, bnd=(y0, y1))
    if well:
        out += water(SHAFT, at)
    return out


def door_close(k, at, under=ROOMC, glint=True, rim=False):
    """The wheel of level k rolls out of its slot and across the doorway (rim: a gold ring marks it shut)."""
    (ox, oy), (sx, sy) = door_xy(k), door_xy(k, shut=True)
    out = [{"k": "circle", "x": round(ox, 1), "y": round(oy, 1), "r": 11, "fill": under, "c": "none", "w": 0, "in": round(at, 2), "dur": .3}]
    out += wheel(sx, sy, 9.5, at + .12)
    if glint:
        out.append(glow(sx, sy, 26, at + .15, .55, "lamp"))
    if rim:
        out.append(ring(sx, sy, 15, at + .2, AU, 2.2, dur=.35))
    return out


def ghost(t_dim, t_g):
    """About 85 m: the dimension, and a 25-storey building drawn to the same height."""
    out = dimv(1252, GY, BOT, "about 85 m", t_dim, BONE, lx=26, dur=1.2)
    out.append(rect(1294, GY, 70, 595, "rgba(245,236,220,.05)", "#f5ecdc", 1.5, 0, t_g, style="inferred"))
    out += [ln([[1296, GY + 23.8 * j], [1362, GY + 23.8 * j]], t_g + .02 * j, "#f5ecdc", 1, draw=False, op=.45) for j in range(1, 25)]
    out.append(lab(1329, GY - 16, "25 storeys", t_g + .4, BONE, 26))
    return out


def stable_icon(at):
    x0, x1, fl, h = room_of(0, "stable")
    return [beast(ASS, x0 + 50, fl, 24, at, "#e8d6b8", fx="pop"), beast(ASS, x0 + 92, fl, 21, at + .15, "#cdb994", face=-1, fx="pop"),
            rect(x1 - 30, fl - 8, 20, 8, "#6a5440", "#c9a46a", 1, 2, at + .25, "pop")]


def store_icon(at):
    x0, x1, fl, h = room_of(1, "store")
    return [jar(x0 + 26 + 19 * j, fl, 15, at + .08 * j, ("#c8743c", "#b8865a")[j % 2]) for j in range(5)]


def press_icon(at):
    """A wine press: a treading floor, a channel, a red-stained vat."""
    x0, x1, fl, h = room_of(0, "press")
    return [rect(x0 + 24, fl - 7, 56, 7, "#6a4a3a", "#e98a8a", 1.2, 2, at, "pop"), rect(x0 + 82, fl - 3, 18, 3, "#7a2a2a", at=at + .15, fx="pop"),
            rect(x0 + 100, fl - 13, 18, 13, "#7a2a2a", "#e98a8a", 1.2, 3, at + .25, "pop"), dot(x0 + 109, fl - 9, 3.2, "#e98a8a", at + .35)]


def church_icon(at):
    """The church on a lower level: a cross-shaped plan drawn in its hall."""
    x0, x1, fl, h = room_of(5, "church")
    return [church_plan(x0 + 46, fl - 18, 5, at, AU, 2.2)]


def crowd(at, seed=11):
    """People in many rooms, a few animals with them (an estimate, drawn as one)."""
    rr = random.Random(seed)
    out, k = [], 0
    for lv in range(8):
        for x0, x1, tg in ROOMS[lv]:
            n = 1 + (x1 - x0 > 125) + (rr.random() < .35)
            for j in range(n):
                x = x0 + (x1 - x0) * (j + 1) / (n + 1) + rr.uniform(-6, 6)
                t = round(at + .025 * k, 2)
                if rr.random() < .2:
                    out.append(beast(GOAT, round(x, 1), LVF[lv], 14, t, "#d9c7a6", fx="pop"))
                else:
                    out.append(person(round(x, 1), LVF[lv], 12, t, "#efe6d4", fx="pop"))
                k += 1
    return out


def mini_city(x0, y0, at, n=8, lit=4, pitch=44, w=280, seed=4, lit_at=None, box=True):
    """A small section of another city in the same picture language: n levels of vaulted rooms, the top `lit` lamp-lit (at lit_at)."""
    rr = random.Random(seed)
    out = [rect(x0 - 22, y0 - 40, w + 44, n * pitch + 56, TUFF_A, "rgba(255,236,206,.5)", 1.5, 10, at, "pop")] if box else []
    out.append(ln([[x0 - 22, y0 - 14], [x0 + w + 22, y0 - 14]], at + .2, "rgba(255,226,190,.7)", 2, draw=False))
    for k in range(n):
        fl = y0 + pitch * (k + 1) - 8
        t = at + .25 + .1 * k
        xs, x = [], x0 + rr.randint(0, 30)
        while x < x0 + w - 60:
            ww = rr.randint(56, 96)
            xs.append((x, min(x + ww, x0 + w)))
            x += ww + rr.randint(22, 40)
        out += [poly(vault(a, b, fl, 22), ROOMC, RIM, 1.2, t, "fade") for a, b in xs]
        if k < lit:
            tl = (lit_at if lit_at is not None else t) + .15 * k
            for a, b in xs:
                out += [poly(vault(a + 1.2, b - 1.2, fl, 20.8), LITC, at=tl, fx="fade"), glow((a + b) / 2, fl - 9, 34, tl + .1, .75, "lamp")]
        out += [rect(a[1] - 1, fl - 9, b[0] - a[1] + 2, 9, ROOMC, at=t, fx="fade") for a, b in zip(xs, xs[1:])]
    return out


# ================================================================== the opening: the city behind the wall
def s1():
    """1963: the house on the plateau at dusk, framed close; the man in the basement with his lamp; a crack runs down the back wall,
    the wall breaks and a dark room glows behind it."""
    sid = "s1"
    t_wall, t_room = T(sid, "knocking through"), T(sid, "found a room")
    sc = city_base("dusk")
    sc.update(cam=[4.4, 676, 180], els=house_els() + cellar_els() + wall_break(t_wall, t_room) + found_room(t_room + .15) +
              [lab(812, 214, "1963", .5, GOLD, 34, st="serif")])
    return sc


def s2_add():
    """The camera pulls back: the city builds level by level below the house (8 levels, 85 m), the deep shaft drawing down with them,
    a person on the surface for scale, then the dimension and the 25-storey ghost."""
    sid = "s2"
    t0, t85, tg = T(sid, "Below it"), T(sid, "eighty five metres"), T(sid, "twenty five storey")
    a = t0 + .7
    step = max(.32, min(.5, (t85 - .2 - a) / 8))
    out = [cover(770, 184, 84, 36, .1, TUFF_A, 1.0, .4)]                  # the date goes as the camera pulls back
    for k in range(8):
        out += level_els(k, a + step * k)
    out += [ln([[SHAFT, GY + 7], [SHAFT, BOT - 7]], a, ROOMC, 14, dur=step * 8)] + well_head(SHAFT, a) + water(SHAFT, a + step * 8)
    out += [person(712, GY, 12, a + .3, "#2a2018")] + ghost(t85, tg)
    return out


def s3_add():
    """In the order said, the levels named light up and the others dim: the stables (two donkeys), the water at the foot of the deep
    shaft ('wells'), the church on a lower level (its cross-shaped plan), a stone wheel by a doorway, which rolls shut."""
    sid = "s3"
    t_st, t_we, t_ch, t_dr, t_sh = T(sid, "Stables"), T(sid, "wells"), T(sid, "A church"), T(sid, "doors made"), T(sid, "rolled shut")
    out = veil(.15)
    out += spot(0, t_st, lit=("stable",)) + stable_icon(t_st + .3)
    out += spot(7, t_we, well=True) + [glow(SHAFT, BOT - 12, 72, t_we + .25, .9, "blue")]
    out += spot(5, t_ch, lit=("church",)) + church_icon(t_ch + .25)
    out += spot(1, t_dr) + [ring(door_xy(1)[0], door_xy(1)[1], 20, t_dr + .3, AU, 2.5, dur=.5)] + door_close(1, t_sh)
    out += [ln([[SHAFT, GY + 8], [SHAFT, BOT - 24]], t_we, "#9fd0ff", 2.5, "inferred", .9),
            lab(470, 232, "stables", t_st + .35, AU, 26), lab(1018, 772, "wells", t_we + .45, "#9fd0ff", 26, "start"),
            lab(784, 625, "a church", t_ch + .45, AU, 26, "start"), lab(494, 377, "stone doors", t_dr + .45, BONE, 26)]
    return out + ghost(-1, -1)


def s4():
    """Night over the plateau: the city dim below; snow; the question, lilac, over the city; a dotted line from the house down to
    the deepest level, 'Ice Age shelter?'."""
    sid = "s4"
    t_q, t_when, t_ice = T(sid, "So who dug"), T(sid, "And when"), T(sid, "cold of the Ice")
    sc = city_base("night")
    els = city_full() + veil(-1, .5)
    els += flakes(46, 90, 1700, 120, 176, t_ice - 1.8, 7, .025, (3.5, 6.5))
    dx = room_of(7, "deep")
    cx = (dx[0] + dx[1]) / 2
    els += [poly(vault(dx[0] + 1.5, dx[1] - 1.5, BOT, CH - 1.5), "#1f2230", "rgba(201,193,238,.6)", 1.6, t_ice + 1.0, "fade")]
    els += [ln([[694, GY + 2], [770, 330], [736, 520], [cx, BOT - 14]], t_ice, LILAC, 3, "claimed", 1.6, curve=True),
            glow(cx, BOT - 14, 90, t_ice + 1.4, .85, "blue"), dot(cx, BOT - 14, 7, LILAC, t_ice + 1.4),
            lab(cx, 738, "Ice Age shelter?", t_ice + 1.5, LILAC, 32)]
    els += question(1440, 430, t_q, 120) + [lab(1500, 362, "who?", t_q + .5, LILAC, 34, "start"), lab(1500, 432, "when?", t_when, LILAC, 34, "start")]
    sc.update(cam=CAM, els=els)
    return sc


# ================================================================== chapter 1: rooms cut from volcanic ash
TV = View(25.6, 45.2, 35.2, 42.4, (90, 120, 1600, 680))
DRK = (34.7351, 38.3735)


def s6():
    """A map of Turkey: Istanbul and Ankara small, Cappadocia as a soft amber region on the central plateau, Derinkuyu in gold."""
    sid = "s6"
    t_c, t_t = T(sid, "Cappadocia"), T(sid, "central Turkey")
    v = TV
    cx, cy = v.p(34.85, 38.65)
    els = [{"k": "map", "land": v.land(), "in": -1},
           {"k": "pin", "x": v.p(28.97, 41.01)[0], "y": v.p(28.97, 41.01)[1], "t": "Istanbul", "c": DIM, "r": 6, "in": .4},
           {"k": "pin", "x": v.p(32.85, 39.93)[0], "y": v.p(32.85, 39.93)[1], "t": "Ankara", "c": DIM, "r": 6, "a": "end", "lx": -18, "in": .5},
           poly(ellipse(cx, cy, 120, 80, 40)[:-1], "rgba(232,184,122,.18)", AMBER, 2.4, t_c, curve=True, style="inferred"),
           lab(cx + 150, cy - 70, "Cappadocia", t_c + .2, AMBER, 34, "start", st="ital"),
           {"k": "pin", "x": v.p(*DRK)[0], "y": v.p(*DRK)[1], "t": "Derinkuyu", "c": GOLD, "in": t_c + .8, "a": "start"},
           lab(v.p(31.5, 38.9)[0], v.p(31.5, 38.9)[1], "the Anatolian plateau", t_t, DIM, 26, st="ital")] + \
          scalebar(140, 770, round(v.km(200), 1), "200 km", .6)
    return {"base": "map", "cam": CAM, "els": els}


VOLC = [(330, 300, 150), (880, 250, 210), (1380, 290, 170)]      # cone tips (x, y) and half-width at the ground


def s7():
    """About 10 to 5 million years ago: three volcanoes on the horizon (there as the camera lands); glowing ash clouds billow up one
    after another as it is said, and grey ash flows spread over the plain."""
    sid = "s7"
    t_ash, t_again = T(sid, "glowing ash"), T(sid, "again and")
    gy = 470
    els = [lab(889, 570, "about 10 to 5 million years ago", .7, BONE, 32)]
    for k, (x, y, hw) in enumerate(VOLC):
        t = .2 + .25 * k
        els += [poly([(x - hw * 1.1, gy), (x - hw * .45, y + 34), (x - hw * .25, y + 4), (x - hw * .1, y + 16), (x + hw * .1, y + 16), (x + hw * .25, y + 4),
                      (x + hw * .45, y + 34), (x + hw * 1.1, gy)], "#3b2f2a", "#8a6a48", 1.5, t, "rise", curve=True),
                glow(x, y + 6, 60, t + .5, .6, "fire")]
    for k, (x, y, hw) in enumerate(VOLC):
        t = t_ash + 1.0 * k
        if k == 2:
            t = t_again
        els += [glow(x, y - 10, 120, t, .9, "fire")]
        for j in range(4):
            els.append(oval(x + (j - 1.5) * 34, y - 50 - j * 34, 70 + j * 18, 42 + j * 10, "rgba(170,160,150,.55)", at=t + .15 * j, fx="pop"))
        els.append(poly([(x - 30, gy - 4), (x - hw - 120, gy + 2), (x - hw - 260, gy + 14), (x + hw + 260, gy + 14), (x + hw + 120, gy + 2), (x + 30, gy - 4)],
                        "rgba(200,190,175,.55)", at=t + .8, fx="fade"))
    return {"base": "section", "tod": "dusk", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": "#4a3c30", "t": ""}], "cam": CAM, "els": els}


def s8_add():
    """The ash settles, layer on layer (pale bands fill from the bottom), 'over 430 m' up the right side; the top layer: tuff."""
    sid = "s8"
    t_lay, t_430, t_tuff = T(sid, "layer on layer"), T(sid, "four hundred"), T(sid, "tuff")
    top, bot = 486, 800
    tones = ["#a8916b", "#c9b38a", "#b8a27c", "#d8c49c", "#bfa982", "#d2bd95"]
    n = len(tones)
    hh = (bot - top) / n
    els = []
    for j in range(n):
        y = bot - (j + 1) * hh
        e = rect(-10, y, 1800, hh - 2, tones[j], at=t_lay + .4 * j, fx="fill")
        els += [e, ln([[-10, y], [1790, y]], t_lay + .4 * j + .3, "rgba(255,236,206,.35)", 1.2, draw=False)]
    els += dimv(1640, top, bot, "over 430 m", t_430, GOLD, lx=-20) + [lab(889, top + 60, "tuff", t_tuff, "#3a2c20", 40, st="serif", halo=False)]
    return els


def pores(cx, cy, r, n, at, seed=3):
    rr = random.Random(seed)
    out = []
    for k in range(n):
        a, d = rr.uniform(0, 2 * math.pi), math.sqrt(rr.random()) * (r - 12)
        out.append(dot(round(cx + d * math.cos(a), 1), round(cy + d * math.sin(a), 1), round(rr.uniform(2.5, 7), 1), "#6f5a44", round(at + .012 * k, 2), fx="fade"))
    return out


def s9():
    """Tuff close: a magnified disc full of small pores; a hand pick cuts grooves in a tuff face; then a small chart: 'outside' swings
    between hot and cold, 'inside' stays nearly flat (schematic, no numbers). The disc, the face and the chart's frame are there as
    the camera lands; each fills as it is said."""
    sid = "s9"
    t_light, t_soft, t_steady, t_bl = T(sid, "light and full"), T(sid, "soft enough"), T(sid, "steady temperature"), T(sid, "wool")
    cx, cy, r = 360, 400, 210
    els = [{"k": "circle", "x": cx, "y": cy, "r": r, "fill": TUFF, "c": "#f2dcb4", "w": 3, "in": .3, "fx": "pop"}] + pores(cx, cy, r, 90, .5) + \
          magnifier(cx, cy, r + 8, .5, BONE)[1:] + [lab(cx, 660, "light, full of holes", t_light + .3, GOLD, 30)]
    fx0, fy0 = 700, 230
    els += [rect(fx0, fy0, 240, 400, TUFF2, "#e9dccb", 1.5, 4, .3), rect(fx0, fy0, 240, 400, "rgba(0,0,0,.08)", r=4, at=.3)] + pores(fx0 + 120, fy0 + 200, 150, 40, .5, 8)
    els += [ln([[fx0 + 60, fy0 + 60 + 40 * j], [fx0 + 180, fy0 + 70 + 40 * j]], t_soft + .3 * j, "#5a4632", 4, dur=.4) for j in range(5)]
    hx, hy = fx0 + 210, fy0 + 230
    els += [poly([(hx, hy), (hx + 70, hy - 18), (hx + 120, hy - 6), (hx + 70, hy - 8)], "#c9ccd2", "#ffffff", 1, t_soft, "pop"),
            ln([[hx + 70, hy - 12], [hx + 140, hy + 100]], t_soft, "#8a6a44", 8, draw=False)]
    els += [lab(fx0 + 120, 670, "hand tools", t_soft + .6, GOLD, 30)]
    x0, x1, yc = 1080, 1640, 420
    els += [ln([[x0, 600], [x1, 600]], 1.0, "#e9dccb", 2, dur=.5), ln([[x0, 240], [x0, 600]], 1.0, "#e9dccb", 2, dur=.5),
            lab(x0 + 14, 228, "temperature", 1.2, DIM, 24, "start")]
    wave = [(x0 + (x1 - x0) * k / 40, yc - 150 * math.sin(k / 40 * 4 * math.pi)) for k in range(41)]
    els += [ln(wave, t_steady, AMBER, 4, dur=1.4, curve=True), lab(x1, 230, "outside", t_steady + .4, AMBER, 26, "end"),
            ln([[x0, yc + 6], [x1, yc - 6]], t_steady + 1.2, "#9fd0ff", 5, dur=1.2), lab(x1, yc + 46, "inside", t_steady + 1.6, "#9fd0ff", 26, "end"),
            lab((x0 + x1) / 2, 680, "a stone blanket", t_bl, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def chimney(x, gy, h, w, at, cap_at=None, door=False):
    """A fairy chimney: a cone of soft tuff; its darker cap of harder rock pops on when the hat is said."""
    out = [poly([(x - w / 2, gy), (x - w * .3, gy - h * .4), (x - w * .17, gy - h * .85), (x - w * .12, gy - h), (x + w * .12, gy - h), (x + w * .17, gy - h * .85),
                 (x + w * .3, gy - h * .4), (x + w / 2, gy)], "#d9c29a", "#f2dcb4", 1.2, at, "rise")]
    out.append(poly([(x - w * .3, gy - h + 4), (x - w * .22, gy - h - h * .12), (x + w * .22, gy - h - h * .12), (x + w * .3, gy - h + 4)], "#6f5a44", "#a8916b", 1.2,
                    at + .25 if cap_at is None else cap_at, "pop"))
    if door:
        out += [rect(x - 9, gy - 48, 18, 34, DARK, EDGE, 1.2, 8, at + .4), rect(x - 6, gy - h * .55, 12, 16, DARK, EDGE, 1, 5, at + .5)]
    return out


def s10():
    """Rain and wind on the tuff: a valley of fairy chimneys (there as the camera lands); rain streaks and a wind arrow; the darker
    caps pop on with 'a hat of harder stone'; a little rock-cut church door in one; 'World Heritage, 1985'."""
    sid = "s10"
    t_rain, t_hat, t_wh = T(sid, "Rain and wind"), T(sid, "hat of harder"), T(sid, "World Heritage")
    gy = 700
    els = [hill([(80, gy), (400, gy - 6), (900, gy + 4), (1400, gy - 4), (1700, gy)], "#5a4636", "#8a6a48", 1.5, -1)]
    for k, (x, h, w) in enumerate([(260, 260, 120), (430, 340, 140), (640, 220, 110), (1000, 380, 150), (1220, 260, 120), (1430, 320, 130), (1590, 200, 100)]):
        els += chimney(x, gy, h, w, .15 + .12 * k, cap_at=t_hat + .12 * k, door=(k == 3))
    rr = random.Random(4)
    els += [ln([[x, y], [x - 14, y + 46]], t_rain + .02 * j, "#9fd0ff", 2, dur=.3, op=.7) for j, (x, y) in
            enumerate([(rr.uniform(150, 1650), rr.uniform(140, 380)) for _ in range(40)])]
    els += [arr([[180, 520], [380, 500], [560, 520]], t_rain + .6, "#cfe6ff", 3, dur=.8), lab(200, 480, "rain, wind", t_rain + .8, "#cfe6ff", 26, "start")]
    els += [lab(1000, 250, "harder cap", t_hat + .4, AU, 26), ln([[1000, 262], [1000, 300]], t_hat + .4, AU, 2, dur=.3),
            lab(1000, 760, "a rock-cut church", t_wh - .6, BONE, 26)] + chip(1450, 165, "World Heritage, 1985", t_wh, GOLD, 26)
    return {"base": "sky", "tod": "dusk", "ground": gy, "sun": [1500, 420, 26], "cam": CAM, "els": els}


def s11():
    """A tuff cliff with a wooden door; inside, a chamber where sacks and crates of potatoes stack up; '2,000+ tuff stores';
    'harvest to harvest'; a fridge outline, struck."""
    sid = "s11"
    t_dig, t_2k, t_pot, t_next, t_fr = T(sid, "still"), T(sid, "two thousand"), T(sid, "potatoes"), T(sid, "harvest to"), T(sid, "No fridge")
    gy = 640
    els = [hill([(-10, 380), (150, 320), (400, 285), (700, 290), (880, 320), (980, 380), (1010, 470), (1030, gy)], TUFF, "#f2dcb4", 2, -1, bottom=gy + 2),
           poly([(360, gy), (360, 500), (400, 456), (960, 456), (1000, 500), (1000, gy)], DARK, EDGE, 2.5, .4, "pop"),
           rect(1000, 520, 22, 120, "#8a6a44", "#e7c99a", 1.5, 2, .5), glow(680, 560, 260, .6, .35, "lamp"),
           person(1120, gy, 120, t_dig, "#efe6d4"), ln([[1140, gy - 70], [1190, gy - 20]], t_dig + .2, "#8a6a44", 5, draw=False)]
    for j in range(12):
        x, y = 400 + 46 * (j % 6), gy - 30 - 42 * (j // 6)
        els.append(oval(x + 20, y + 12, 22, 17, "#c9a46a", "#8a6a44", 1.2, at=t_pot + .08 * j, fx="pop"))
    for j in range(4):
        x, y = 720 + 60 * (j % 2), gy - 46 - 48 * (j // 2)
        els.append(rect(x, y, 54, 44, "#8a6a44", "#e7c99a", 1.2, 2, t_pot + .5 + .1 * j, "pop"))
    els += chip(640, 230, "2,000+ tuff stores", t_2k, GOLD, 30)
    els += [arr([[450, 400], [680, 370], [910, 400]], t_next, BONE, 3, dur=.9), lab(680, 350, "harvest to harvest", t_next + .4, BONE, 26)]
    fx0, fy0 = 1400, 400
    els += [rect(fx0, fy0, 120, 200, "#e8ecef", "#ffffff", 2, 8, t_fr, "pop"), ln([[fx0, fy0 + 70], [fx0 + 120, fy0 + 70]], t_fr, "#8a9aa8", 2, draw=False),
            ln([[fx0 + 100, fy0 + 20], [fx0 + 100, fy0 + 50]], t_fr, "#8a9aa8", 4, draw=False), strike(fx0 - 30, fy0 + 230, fx0 + 150, fy0 - 30, t_fr + .4)]
    return {"base": "sky", "tod": "day", "ground": gy, "sun": [1550, 200, 28], "cam": CAM, "els": els}


RCOL = 1420                  # the label column of the tour panels, right of the city


def s12():
    """Back on the city, whole, by day (the same picture): 'Derinkuyu', 'deep well' as the well shaft glows down to water; 'open
    since the 1960s'."""
    sid = "s12"
    t_d, t_w, t_69 = T(sid, "Derinkuyu"), T(sid, "deep"), T(sid, "opened to visitors")
    sc = city_base("day")
    els = city_full() + [person(712, GY, 12, -1, "#2a2018")]
    els += [lab(RCOL, 300, "Derinkuyu", t_d, GOLD, 46, "start", st="serif"),
            ln([[SHAFT, GY + 6], [SHAFT, BOT - 22]], t_w, "#9fd0ff", 4, dur=1.2), glow(SHAFT, BOT - 12, 80, t_w + 1.0, .85, "blue"),
            glow(SHAFT, GY - 4, 40, t_w, .6, "blue"), lab(SHAFT + 22, 166, "deep well", t_w + .4, "#bfe2ff", 30, "start", st="ital")]
    els += chip(RCOL + 150, 372, "open since the 1960s", t_69, BONE, 26)
    sc.update(cam=CAM, els=els)
    return sc


def s13_add():
    """'Up to 18 levels', a bracket down the whole depth; a warm dashed outline round a small part near the top, 'open to visitors';
    then little people and animals in many rooms, and a dashed chip '20,000? an estimate'."""
    sid = "s13"
    t_18, t_vis, t_20, t_est = T(sid, "eighteen levels"), T(sid, "small part"), T(sid, "twenty thousand"), T(sid, "not a count")
    els = [ln([[378, GY + 16], [360, GY + 16], [360, BOT], [378, BOT]], t_18, BONE, 2.5, dur=1.0),
           lab(344, 488, "up to 18 levels", t_18 + .5, BONE, 28, "end")]
    els += [rect(390, 226, 300, 132, "rgba(255,200,120,.10)", GOLD, 2.2, 10, t_vis, style="inferred"), lab(540, 382, "open to visitors", t_vis + .3, GOLD, 26)]
    els += crowd(t_20)
    els += chip(RCOL + 150, 468, "20,000? an estimate", t_20 + .6, LILAC, 26, style="inferred")
    return els


def s14():
    """The tour, closer, on the upper levels (the same picture, the levels not named dimmed): the stables light up with their
    donkeys, the storeroom with its jars, the wine press with its red vat."""
    sid = "s14"
    t_st, t_sr, t_wi = T(sid, "Stables"), T(sid, "storerooms"), T(sid, "Presses")
    sc = city_base("day")
    els = city_full() + veil(-1)
    els += spot(0, t_st, lit=("stable", "press"), lit_at={"stable": t_st, "press": t_wi}) + spot(1, t_sr, lit=("store",))
    els += stable_icon(t_st + .3) + store_icon(t_sr + .3) + press_icon(t_wi + .3)
    els += [lab(455, 232, "stables", t_st + .4, AU, 26), lab(508, 377, "storerooms", t_sr + .4, AU, 26, "end"), lab(881, 232, "wine press", t_wi + .4, "#f2a0a0", 26)]
    sc.update(cam=[1.9, 720, 300], els=els)
    return sc


def s14c_add():
    """Down to a lower level: the church lights up, its plan the shape of a cross."""
    sid = "s14c"
    t_ch = T(sid, "A church")
    return spot(5, t_ch, lit=("church",)) + church_icon(t_ch + .3) + [lab(784, 625, "a church", t_ch + .5, AU, 26, "start")]


def s14b_add():
    """Whole again: four more air shafts draw down from the surface through the levels, two of them to water; small arrows of air
    going down."""
    sid = "s14b"
    t_sh, t_wa, t_air = T(sid, "fifty air"), T(sid, "down to"), T(sid, "fresh air")
    els = []
    for j, (x, yb) in enumerate(((520, BOT), (1080, BOT), (770, LVF[3]), (1140, LVF[5]))):
        t = max(1.0, t_sh - .4) + .3 * j
        sh = ln([[x, GY + 3], [x, yb - 3]], t, ROOMC, 9, dur=1.1)
        sh["keepdraw"] = True                         # drawn down from the surface (its cap dot shows only while the camera settles)
        els += [sh] + well_head(x, t, 9)
        if yb == BOT:
            els += water(x, t_wa + .2 * j, 9)
    els += [lab(RCOL, 300, "50+ air shafts", t_sh + .5, BONE, 30, "start")]
    for j, x in enumerate((520, 770, SHAFT, 1080, 1140)):
        els.append(arr([[x + 16, GY + 28], [x + 16, GY + 96]], t_air + .15 * j, "#cfe6ff", 2.5, dur=.4, curve=False))
    return els


def door_wall(at=-1):
    """A passage seen from inside: a tuff wall face, an arched doorway on the left of a slot where the wheel stands."""
    els = [rect(160, 150, 1180, 610, TUFF2, "#e9dccb", 1.5, 6, at), rect(160, 150, 1180, 610, "rgba(0,0,0,.12)", r=6, at=at),
           poly([(600, 760), (600, 600), (618, 556), (663, 538), (708, 556), (726, 600), (726, 760)], DARK, EDGE, 2, at, curve=False),
           rect(765, 495, 270, 265, "#2a221b", EDGE, 2, 4, at), ln([[160, 760], [1340, 760]], at, "#e9dccb", 2, draw=False)]
    return els


def s15():
    """The door: a stone wheel up to 1.85 m across (140 units a metre) rests in its slot beside the doorway; a person 1.7 m tall
    beside it; the dimension 'up to 1.85 m'."""
    sid = "s15"
    t_w, t_185, t_slot = T(sid, "Stone wheels"), T(sid, "almost two"), T(sid, "slots")
    els = door_wall() + [lab(750, 138, "seen from inside", .4, DIM, 26)]
    els += wheel(900, 630, 129.5, t_w)
    els += dimv(1080, 500.5, 759.5, "up to 1.85 m", t_185, GOLD, lx=24) + [person(420, 760, 238, t_w + .4, "#efe6d4"),
            lab(420, 500, "1.7 m", t_w + .8, DIM, 24), ring(900, 630, 150, t_slot, AU, 2.5, dur=.6), lab(900, 462, "its slot", t_slot + .3, AU, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s16_add():
    """The operation room behind glows; the wheel rolls across the doorway (cover and pop); at the right, a small section in the
    city's own picture language where each level's wheel rolls shut in turn, top to bottom."""
    sid = "s16"
    t_room, t_roll, t_each = T(sid, "little room"), T(sid, "rolled them"), T(sid, "each level")
    els = [rect(1110, 600, 190, 160, DARK, AU, 2, 6, t_room, "pop"), glow(1205, 680, 90, t_room + .2, .8, "lamp"),
           lab(1205, 580, "a little room", t_room + .4, AU, 26),
           arr([[1000, 560], [880, 520], [720, 560]], t_roll, AU, 4, dur=.9)]
    els += [cover(767, 497, 266, 261, t_roll + .9, "#2a221b", 1.0, .4)]
    els += wheel(663, 630, 129.5, t_roll + 1.0)
    x0, y0, pitch = 1420, 196, 66
    els += [rect(x0 - 26, y0 - 40, 296, 6 * pitch + 60, TUFF_A, "rgba(255,236,206,.5)", 1.5, 10, t_each - .5, "pop")]
    for k in range(6):
        fl = y0 + pitch * (k + 1) - 10
        els += [poly(vault(x0, x0 + 150, fl, 30), ROOMC, RIM, 1.2, t_each - .4, "fade"), rect(x0 + 148, fl - 13, 62, 13, ROOMC, at=t_each - .4, fx="fade")]
        els += wheel(x0 + 214, fl - 10, 10, t_each + .3 + .3 * k) + [glow(x0 + 214, fl - 10, 26, t_each + .35 + .3 * k, .5, "lamp")]
    els += [lab(x0 + 122, y0 - 54, "level by level", t_each + .2, BONE, 26)]
    return els


def s17_add():
    """The whole city: every level's wheel rolls across its doorway, top to bottom: built for hiding."""
    sid = "s17"
    t_c, t_h = T(sid, "no cave"), T(sid, "built for")
    els = []
    for k in range(8):
        under = LITC if k in (0, 1) else VEILED
        els += door_close(k, t_c + .2 + .26 * k, under, rim=True)
    els += [lab(RCOL, 380, "built for hiding", t_h + .3, GOLD, 32, "start")]
    return els


# ================================================================== chapter 2: a landscape of hiding places
LV = View(34.15, 35.15, 38.28, 38.86, (90, 120, 1180, 680))
RIVER = [(35.2, 38.80), (35.05, 38.74), (34.92, 38.71), (34.80, 38.72), (34.70, 38.74), (34.62, 38.75), (34.52, 38.80), (34.42, 38.87)]
SITES = {"Derinkuyu": DRK, "Kaymakli": (34.7522, 38.4597), "Nevsehir": (34.7144, 38.6206), "Ozkonak": (34.8407, 38.8069), "Asikli": (34.2297, 38.3486)}


def lp(name):
    return LV.p(*SITES[name])


def local_map():
    """Central Cappadocia (about 85 by 65 km): the Kizilirmak river; drawn once, under the pins."""
    rv = [LV.p(lo, la) for lo, la in RIVER]
    return [{"k": "map", "land": LV.land(), "landc": "#4a3c2e", "in": -1}, ln(rv, -1, "#6fb6d6", 5, curve=True)]


KV = View(34.42, 35.06, 38.29, 38.56, (100, 140, 1120, 620))       # Derinkuyu and Kaymakli, close


def graticule(v, lon0, lon1, lat0, lat1, d=.1, at=-1):
    """A faint grid of meridians and parallels over the land (a map without a coast needs something to read as a map)."""
    out = []
    lo = math.ceil(lon0 / d) * d
    while lo < lon1:
        out.append(ln([v.p(lo, lat0), v.p(lo, lat1)], at, "rgba(233,220,203,.10)", 1.2, draw=False))
        lo += d
    la = math.ceil(lat0 / d) * d
    while la < lat1:
        out.append(ln([v.p(lon0, la), v.p(lon1, la)], at, "rgba(233,220,203,.10)", 1.2, draw=False))
        la += d
    return out


def s18():
    """The two cities on a close map: Derinkuyu and Kaymakli, 10 km apart; a small section of Kaymakli in the city's picture language
    (8 levels, 4 lit); a dotted lilac tunnel between them, 'a tunnel?', then 'never found'."""
    sid = "s18"
    t_k, t_8, t_4, t_tun, t_nf = T(sid, "About ten"), T(sid, "eight levels"), T(sid, "four of them"), T(sid, "a tunnel"), T(sid, "ever been")
    v = KV
    dx, dy = v.p(*DRK)
    kx, ky = v.p(*SITES["Kaymakli"])
    els = [{"k": "map", "land": v.land(), "landc": "#4a3c2e", "in": -1}] + graticule(v, 34.42, 35.06, 38.29, 38.56) + [
           {"k": "pin", "x": dx, "y": dy, "t": "Derinkuyu", "c": GOLD, "in": .4, "a": "end", "lx": -22},
           {"k": "pin", "x": kx, "y": ky, "t": "Kaymaklı", "c": AMBER, "in": t_k, "a": "end", "lx": -22}] + scalebar(200, 740, round(v.km(10), 1), "10 km", t_k + .4)
    x0, y0 = 1330, 236
    els += mini_city(x0, y0, .9, n=8, lit=4, pitch=46, w=290, lit_at=t_4)
    els += [ln([[kx + 16, ky - 4], [x0 - 34, 300]], t_k + .3, "rgba(232,184,122,.6)", 2, "inferred", .5),
            lab(x0 + 145, y0 + 8 * 46 + 52, "4 of 8 levels open", t_4 + .8, GOLD, 26)]
    els += [ln([[dx + 10, dy - 12], [dx + 70, (dy + ky) / 2], [kx + 10, ky + 12]], t_tun, LILAC, 3, "claimed", 1.0, curve=True),
            lab(dx + 96, (dy + ky) / 2 - 6, "a tunnel?", t_tun + .6, LILAC, 30, "start"),
            lab(dx + 96, (dy + ky) / 2 + 32, "never found", t_nf, BONE, 28, "start")]
    return {"base": "map", "cam": CAM, "els": els}


OZ_GY = 400                  # Ozkonak's field; below it the city, drawn about four times larger than Derinkuyu's


def s19():
    """Ozkonak, 1972, close: a field on the plateau, a village and poplars beyond it, hills; the imam with his hoe; irrigation water runs
    along its channel, then drains into a crack in the ground (below it, the tuff, still blank)."""
    sid = "s19"
    t_w, t_d = T(sid, "irrigation water"), T(sid, "drain away")
    gy = OZ_GY
    els = [rect(-10, gy + 30, 1800, 700, TUFF_A, at=-1), rect(-10, gy + 30, 1800, 700, "url(#k-blocks)", at=-1, op=.06),
           rect(-10, gy, 1800, 30, "#6f5a44", at=-1), ln([[-10, gy + 30], [1790, gy + 30]], -1, "rgba(255,226,190,.25)", 1.2, draw=False),
           lab(760, 236, "Özkonak, 1972", .4, GOLD, 32)]
    for x, h in ((846, 74), (1118, 92), (1300, 80), (1560, 96)):
        els += [oval(x, gy - h * .55, 13, h * .5, "#4f5a3a", at=-1), rect(x - 2, gy - 12, 4, 12, "#5a4632", at=-1)]
    els += flat_house(880, gy, 120, 78, -1, "#a8916b") + flat_house(1006, gy, 96, 60, -1, "#9b7f5e", win=False) + \
           flat_house(1340, gy, 130, 84, -1, "#a8916b") + flat_house(1480, gy, 90, 58, -1, "#9b7f5e", door=False)
    rr = random.Random(6)
    for j in range(19):
        x = 140 + 34 * j
        if 690 < x < 712:
            continue
        els.append(poly([(x - 9, gy), (x - 3, gy - 14 - rr.uniform(0, 6)), (x, gy - 6), (x + 3, gy - 16 - rr.uniform(0, 6)), (x + 9, gy)], "#7d8a52", at=-1))
    els += [person(420, gy, 62, .5, "#efe6d4"), ln([[436, gy - 34], [476, gy - 4]], .7, "#8a6a44", 4, draw=False), ln([[468, gy - 10], [486, gy - 2]], .7, "#c9ccd2", 5, draw=False)]
    els += [rect(130, gy - 4, 572, 8, "#3a2c20", r=3, at=-1), rect(132, gy - 3, 568, 5, "#5fa8c9", r=2, at=t_w - .6, fx="fade"),
            arr([[260, gy - 26], [480, gy - 26]], t_w, "#9fd0ff", 2.5, dur=.8, curve=False),
            ln([[700, gy - 1], [706, gy + 16], [701, gy + 34], [708, gy + 52]], t_d - .3, "#2a2018", 3, dur=.4),
            ln([[701, gy + 2], [706, gy + 18], [702, gy + 36], [707, gy + 54]], t_d, "#5fa8c9", 3, dur=.8)]
    return {"base": "sky", "tod": "day", "ground": gy, "groundc": "#6f5a44", "sun": [1010, 214, 22], "cam": [1.75, 640, 300], "els": els}


def s19b_add():
    """The camera pulls back: below the field, the rooms of another underground city (the same picture language), the water running
    on down into them; then the narrow holes between its levels, under a magnifier: 'about 5 cm'."""
    sid = "s19b"
    t_city, t_holes, t_5 = T(sid, "another underground"), T(sid, "narrow holes"), T(sid, "five centimetres")
    gy = OZ_GY
    rows = [(520, [(560, 800), (900, 1200)]), (640, [(420, 680), (760, 1060), (1140, 1400)]), (760, [(600, 880), (960, 1260)])]
    els = []
    for k, (fl, rs) in enumerate(rows):
        t = t_city + .45 * k
        els += [poly(vault(a, b, fl, 70), ROOMC, RIM, 1.6, t, "fade") for a, b in rs]
        els += [rect(p[1] - 2, fl - 30, q[0] - p[1] + 4, 30, ROOMC, at=t, fx="fade") for p, q in zip(rs, rs[1:])]
    els += [ln([[707, gy + 54], [704, 452]], t_city, "#5fa8c9", 3, dur=.4), rect(670, 514, 70, 6, "#5fa8c9", r=2, at=t_city + .5, fx="fill"),
            glow(690, 490, 120, t_city + .4, .45, "lamp")]
    holes = [(620, 520, 570), (980, 520, 570), (820, 640, 690), (1200, 640, 690)]
    for j, (x, y1, y2) in enumerate(holes):
        els.append(ln([[x, y1], [x, y2]], t_holes + .15 * j, "#f2dcb4", 2.5, draw=False))
    els += magnifier(980, 545, 40, t_5 - .2, BONE) + [lab(1046, 553, "holes about 5 cm wide", t_5 + .3, "#f2dcb4", 28, "start")]
    return els


def s20():
    """Across the region (a clean map): small amber dots pop until '200+'; lighter dashed rings join them, '360+?': two counts; then
    a counter '1.5 million visitors, 2023'."""
    sid = "s20"
    t_200, t_360, t_vis = T(sid, "two hundred"), T(sid, "three hundred"), T(sid, "one and a half")
    dx, dy = lp("Derinkuyu")
    rr = random.Random(9)
    x0, x1, y0, y1 = 250, 1110, 150, 760
    pts = []
    while len(pts) < 200:
        x, y = rr.uniform(x0, x1), rr.uniform(y0, y1)
        if all(abs(x - px) > 7 or abs(y - py) > 7 for px, py in pts) and not (dx - 150 < x < dx + 10 and dy - 22 < y < dy + 22):
            pts.append((x, y))
    els = local_map() + [{"k": "pin", "x": dx, "y": dy, "t": "Derinkuyu", "c": GOLD, "in": .3, "a": "end", "lx": -20},
                         lab(470, 300, "Cappadocia", .6, AMBER, 34, st="ital")]
    els += [dot(round(x, 1), round(y, 1), 4, AU, round(.9 + (t_200 + .4) * k / 200, 3), fx="fade") for k, (x, y) in enumerate(pts)]
    els += chip(1450, 300, "200+ shelters", t_200 + .9, AU, 30)
    pts2 = [(rr.uniform(x0, x1), rr.uniform(y0, y1)) for _ in range(160)]
    els += [{"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": 4.5, "fill": "none", "c": "#f2dcb4", "w": 1.5, "style": "inferred", "in": round(t_360 + .006 * k, 3)}
            for k, (x, y) in enumerate(pts2)]
    els += chip(1450, 390, "360+ sites?", t_360 + .9, "#f2dcb4", 30, style="inferred")
    els += [lab(1450, 540, "1.5 million", t_vis, BONE, 46, st="serif"), lab(1450, 586, "visitors in 2023", t_vis + .2, DIM, 26)]
    return {"base": "map", "cam": CAM, "els": els}


NV_TOP = [(80, 720), (400, 690), (650, 560), (820, 380), (960, 360), (1120, 400), (1300, 560), (1560, 690), (1700, 720)]


def hy(x, top=NV_TOP):
    for (xa, ya), (xb, yb) in zip(top, top[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / (xb - xa)
    return top[-1][1]


def s21():
    """Nevsehir, 2013: a hill with a small castle on top and old houses on its slopes; a bulldozer rolls in; the houses go; dark
    openings appear in the hillside where they stood."""
    sid = "s21"
    t_n, t_bd, t_br = T(sid, "Nevsehir"), T(sid, "demolition crews"), T(sid, "broke into")
    gy = 720
    els = [hill(NV_TOP, "#8a7454", "#c9ad85", 2, -1),
           rect(830, 296, 120, 70, "#7a6a58", "#d8c7a8", 1.5, 2, -1)] + [rect(830 + 26 * j, 284, 16, 14, "#7a6a58", "#d8c7a8", 1, 1, -1) for j in range(5)] + \
          [lab(890, 250, "the castle", .5, DIM, 26), lab(1620, 170, "Nevşehir, 2013", t_n, GOLD, 32, "end")]
    houses = [(560, 60, 40), (700, 52, 36), (1150, 56, 40), (1250, 60, 40), (1380, 54, 36), (620, 50, 34)]
    houses = [(x, round(hy(x + w / 2) + 6, 1), w, h) for x, w, h in houses]
    for j, (x, y, w, h) in enumerate(houses):
        els += flat_house(x, y, w, h, -1, "#a8916b", win=False)
    for j, (x, y, w, h) in enumerate(houses):
        els += [cover(x - 4, y - h - 4, w + 8, h + 6, t_br - .6 + .1 * j, "#8a7454", 1.0, .5)]
    for j, (x, y, w, h) in enumerate(houses):
        els += [poly([(x + 8, y), (x + 8, y - h * .6), (x + w / 2, y - h * .9), (x + w - 8, y - h * .6), (x + w - 8, y)], DARK, EDGE, 2, t_br + .15 * j, "pop")]
    bx, by = 330, 712
    els += [rect(bx, by - 46, 120, 34, "#e8b84a", "#fff1c4", 1.5, 4, t_bd, "rise"), rect(bx + 70, by - 80, 44, 36, "#e8b84a", "#fff1c4", 1.5, 3, t_bd, "rise"),
            rect(bx - 6, by - 14, 132, 14, "#3a3530", r=7, at=t_bd, fx="rise"), poly([(bx - 40, by - 4), (bx - 10, by - 50), (bx - 4, by - 50), (bx - 4, by - 4)], "#c9ccd2", "#ffffff", 1, t_bd, "rise")]
    els += [lab(bx + 60, by - 110, "urban renewal", t_bd + .4, DIM, 26)]
    return {"base": "sky", "tod": "day", "ground": gy, "sun": [1450, 230, 26], "cam": CAM, "els": els}


def s22_add():
    """Scans: electrodes along the hill and arcs of current and sound going into it, like an ultrasound."""
    sid = "s22"
    t_sc, t_us = T(sid, "electric currents"), T(sid, "ultrasound")
    els = []
    for j, x in enumerate(range(600, 1330, 70)):
        els.append(dot(x, round(hy(x) - 4, 1), 6, "#9fd0ff", t_sc + .05 * j))
    for j in range(5):
        r = 90 + 60 * j
        els.append({"k": "line", "p": ellipse(960, 420, r * 1.5, r * .9, 24, 20, 160), "c": "#9fd0ff", "w": 2, "style": "inferred", "curve": True,
                    "in": round(t_sc + .5 + .3 * j, 2), "fx": "draw", "dur": .6})
    els += [lab(1170, 300, "electric currents, sound waves", t_sc + .4, "#9fd0ff", 26, "start"), lab(960, 770, "an ultrasound of the hill", t_us, BONE, 26)]
    return els


def blob(cx, cy, rx, ry, seed=1, n=16, amp=.16):
    rr = random.Random(seed)
    return [(cx + rx * (1 + rr.uniform(-amp, amp)) * math.cos(2 * math.pi * k / n), cy + ry * (1 + rr.uniform(-amp, amp)) * math.sin(2 * math.pi * k / n)) for k in range(n)]


def s23():
    """Two footprints: Derinkuyu solid (there as the camera lands), a dotted lilac outline a third bigger ('first results'); a small
    spade, 'digging is slower'; a timeline from 500 CE to today: 'finds inside' fills from about 550 to today; a tick at 2020."""
    sid = "s23"
    t_big, t_dig, t_open, t_6 = T(sid, "a third bigger"), T(sid, "Digging is"), T(sid, "Part of it"), T(sid, "sixth century")
    k = math.sqrt(4 / 3)
    els = [poly(blob(420, 430, 150, 110, 3), "rgba(242,201,142,.16)", GOLD, 3, .3, curve=True), lab(420, 438, "Derinkuyu", .5, GOLD, 30),
           poly(blob(420, 430, 150 * k * 1.08, 110 * k * 1.08, 3), "rgba(201,193,238,.06)", LILAC, 3, t_big, curve=True, style="claimed"),
           lab(420, 246, "first scans: a third bigger?", t_big + .4, LILAC, 28)]
    els += [poly([(380, 700), (400, 650), (440, 650), (460, 700)], "#c9ccd2", "#ffffff", 1, t_dig, "pop"), ln([[420, 650], [420, 570]], t_dig, "#8a6a44", 6, draw=False),
            lab(500, 682, "digging is slower", t_dig + .3, DIM, 26, "start")]
    X = lambda yr: round(860 + (yr - 500) / 1530 * 760, 1)
    ax = 600
    els += [{"k": "axis", "x0": X(500), "x1": X(2030), "y": ax, "ticks": [[X(500), "500"], [X(1000), "1000"], [X(1500), "1500"], [X(2000), "2000"]], "in": .9},
            ln([[X(2020), ax - 80], [X(2020), ax]], t_open, BONE, 2.5, dur=.4), lab(X(2020), ax - 92, "opened 2020", t_open + .2, BONE, 26, "end"),
            ln([[X(550), ax - 40], [X(2026), ax - 40]], t_6, GOLD, 16, dur=1.4), lab(X(1250), ax - 64, "finds inside", t_6 + .6, GOLD, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s24():
    """Houses on a slope in section; under each, a cellar and a short stair down into an older passage that runs on beneath the
    next house; jars and a lamp in each cellar."""
    sid = "s24"
    t_c, t_lost = T(sid, "cellars"), T(sid, "Lost")
    sy = lambda x: 300 + (x - 80) * 200 / 1620
    surf = [(-10, sy(-10)), (1790, sy(1790))]
    els = [hill(surf, TUFF2, "#e9dccb", 2, -1)]
    bottoms = []
    for j, x in enumerate((240, 660, 1080, 1460)):
        y = sy(x + 55)
        els += flat_house(x, y, 110, 70, -1, "#a8916b")
        els += [rect(x + 10, y + 4, 100, 60, "#2a221b", EDGE, 1.5, 3, -1), stair(x + 40, y + 64, x + 80, y + 150, t_c + .2 * j, 4, "#e9dccb", 2.5)]
        els += [jar(x + 26 + 18 * i, y + 62, 18, t_c + .3 + .2 * j + .05 * i) for i in range(2)] + [glow(x + 80, y + 36, 30, t_c + .4 + .2 * j, .7, "lamp")]
        bottoms.append((x + 80, y + 160))
    pas = [(100, bottoms[0][1] - 10)] + bottoms + [(1700, bottoms[-1][1] + 20)]
    els += [ln(pas, -1, "#2a221b", 34, curve=True), ln(pas, -1, EDGE, 1.5, curve=True, op=.6),
            lab(500, bottoms[1][1] + 80, "an older passage", t_c - .2, DIM, 26), lab(900, 230, "cellars", t_c + .4, GOLD, 30)]
    els += [glow(900, bottoms[2][1], 300, t_lost, .25, "lamp")]
    return {"base": "sky", "tod": "day", "ground": 1100, "sun": [1500, 180, 24], "cam": CAM, "els": els}


# ================================================================== chapter 3: shelters from the Ice Age?
XT = lambda ya: round(200 + (13000 - ya) / 13000 * 1380, 1)      # 13,000 years ago .. today
TL_Y = 560


def tl13(t_ax, t_claim, at_dated=.6):
    """13,000 years on one line: the dated sliver at the right end; at 12,800 years ago the claim (dotted), its arc to the dated end."""
    ay = TL_Y
    gl = mini_city(1452, 372, at_dated if at_dated < 0 else at_dated + .2, n=3, lit=3, pitch=30, w=118, seed=7, lit_at=at_dated if at_dated < 0 else at_dated + .4)
    for e in gl:
        if e.get("k") == "glow":
            e["r"] = 22
    return gl + [{"k": "axis", "x0": XT(13000), "x1": XT(0), "y": ay, "ticks": [[XT(12000), "12,000"], [XT(9000), "9,000"], [XT(6000), "6,000"], [XT(3000), "3,000"], [XT(0), "today"]],
             "t": "years ago", "in": t_ax},
            ln([[XT(1400), ay - 22], [XT(0), ay - 22]], at_dated, GOLD, 16, dur=.6), lab((XT(1400) + XT(0)) / 2, ay - 48, "dated", at_dated + .3, GOLD, 28),
            ln([[XT(12800), ay - 160], [XT(12800), ay]], t_claim, LILAC, 3, "claimed", .6), dot(XT(12800), ay - 160, 9, LILAC, t_claim),
            lab(XT(12800) - 14, ay - 186, "Ice Age shelter?", t_claim + .2, LILAC, 30, "start"),
            ln([[XT(12800) + 16, ay - 150], [(XT(12800) + XT(1400)) / 2, ay - 300], [XT(1400) - 6, ay - 40]], t_claim + .8, LILAC, 2, "claimed", 1.2, curve=True)]


def s25():
    """13,000 years on one line: a gold sliver at the right end, 'dated'; far left, at 12,800 years ago, a lilac dotted marker
    'Ice Age shelter?' and a dotted arc from it; a small screen, 'Netflix, 2022'."""
    sid = "s25"
    t_h, t_long, t_tv = T(sid, "Graham Hancock"), T(sid, "long before"), T(sid, "Netflix")
    ay = TL_Y
    els = tl13(.3, t_long) + [lab(XT(12800) - 14, ay - 222, "Hancock", t_h, DIM, 26, "start")]
    tx, ty = 1450, 190
    els += [rect(tx - 90, ty - 54, 180, 108, "#1b2430", "#cfe6ff", 2, 8, t_tv, "pop"), ln([[tx - 40, ty + 66], [tx + 40, ty + 66]], t_tv, "#cfe6ff", 3, draw=False),
            lab(tx, ty + 8, "2022", t_tv + .2, "#cfe6ff", 28), lab(tx, ty + 112, "a Netflix series", t_tv + .3, DIM, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s26():
    """A schematic temperature curve, 16,000 to 10,000 years ago: out of the Ice Age, then a sharp drop into a blue band 'Younger
    Dryas' about 1,200 years wide, then up again (shape only); beside it an ice core whose yearly layers draw one by one, and tree
    rings."""
    sid = "s26"
    t_cold, t_yd, t_ice, t_ring = T(sid, "lurched back"), T(sid, "Younger Dryas"), T(sid, "We read"), T(sid, "rings of")
    X = lambda ya: round(230 + (16000 - ya) / 6000 * 790, 1)
    Y = lambda v: round(640 - v * 380, 1)          # v 0 = glacial, 1 = warm
    curve = [(16000, .05), (15000, .12), (14700, .78), (14200, .7), (13500, .66), (13000, .6), (12900, .12), (12500, .1), (12000, .14), (11700, .2), (11500, .86), (11000, .9), (10000, .95)]
    pts = [(X(a), Y(v)) for a, v in curve]
    els = [ln([[230, 660], [1020, 660]], .2, "#e9dccb", 2, draw=False), lab(230, 700, "16,000", .3, DIM, 24), lab(1020, 700, "10,000 years ago", .3, DIM, 24, "end"),
           lab(212, Y(.95), "warmer", .4, "#ffb07a", 24, "end"), lab(212, Y(.05), "colder", .4, "#9fd0ff", 24, "end"),
           rect(X(12900), 200, X(11700) - X(12900), 450, "rgba(159,208,255,.16)", "#9fd0ff", 1.5, 6, t_cold, style="inferred"),
           ln(pts[:6], .4, AMBER, 4, dur=1.0), ln(pts[5:10], t_cold, "#9fd0ff", 5, dur=.8), ln(pts[9:], t_yd - .2, AMBER, 4, dur=.8),
           lab((X(12900) + X(11700)) / 2, 180, "Younger Dryas", t_yd, "#9fd0ff", 30), lab((X(12900) + X(11700)) / 2, 232, "about 1,200 years", t_yd + .4, DIM, 24)]
    cx, y0, y1 = 1250, 190, 700
    els += [rect(cx - 50, y0, 100, y1 - y0, "#dfeaf2", "#ffffff", 2, 10, t_ice, "pop")]
    els += [ln([[cx - 44, y0 + 12 + 14 * j], [cx + 44, y0 + 12 + 14 * j]], t_ice + .4 + .04 * j, "#8aa8bc", 1.5, draw=False) for j in range(35)]
    els += [lab(cx, y1 + 40, "a layer a year", t_ice + 1.0, "#cfe6ff", 26)]
    rings = [{"k": "circle", "x": 1520, "y": 430, "r": 16 + 13 * j, "fill": "#8a6a44" if j == 7 else "none", "c": "#c9a46a", "w": 2, "in": round(t_ring + .08 * j, 2)} for j in range(8)]
    els += list(reversed(rings)) + [lab(1520, 580, "like tree rings", t_ring + .7, "#c9a46a", 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s27():
    """An old Persian story, drawn in lilac dotted lines (a story, not a site), there as the camera lands: a snowy plain at night, a
    walled enclosure with a gate, people and animals walking in, snow falling: 'a refuge from winter'."""
    sid = "s27"
    t_k, t_ref, t_win = T(sid, "a king"), T(sid, "built a refuge"), T(sid, "deadly winter")
    gy = 640
    A, B, C, D = (720, 572), (1000, 512), (1320, 572), (1040, 632)        # the enclosure's corners on the ground
    hh = 74
    up = lambda p: (p[0], p[1] - hh)
    els = [lab(300, 200, "an old Persian story", .4, DIM, 26, "start")]
    els += [poly([A, B, up(B), up(A)], "rgba(201,193,238,.05)", LILAC, 2, .6, style="claimed"),
            poly([B, C, up(C), up(B)], "rgba(201,193,238,.05)", LILAC, 2, .6, style="claimed"),
            poly([D, C, up(C), up(D)], "rgba(201,193,238,.12)", LILAC, 2.5, .8, style="claimed")]
    g0 = (A[0] + (D[0] - A[0]) * .42, A[1] + (D[1] - A[1]) * .42)
    g1 = (A[0] + (D[0] - A[0]) * .62, A[1] + (D[1] - A[1]) * .62)
    els += [poly([A, g0, up(g0), up(A)], "rgba(201,193,238,.12)", LILAC, 2.5, .8, style="claimed"),
            poly([g1, D, up(D), up(g1)], "rgba(201,193,238,.12)", LILAC, 2.5, .8, style="claimed")]
    for j in range(7):
        x = 300 + 52 * j
        y = 640 - j * 4
        if j % 2:
            els.append(beast(GOAT, x, y, 44, 1.0 + .15 * j, LILAC, fx="pop", op=.75))
        else:
            p = person(x, y, 58, 1.0 + .15 * j, LILAC)
            p.update(op=.75, keepop=True)
            els.append(p)
    els += [arr([[680, 622], [800, 616]], t_ref + .2, LILAC, 2.5, "claimed", .6)]
    els += flakes(70, 90, 1700, 140, 760, t_win - 1.2, 8, .02)
    els += [lab(1020, 410, "a refuge from winter", t_win + .2, LILAC, 32)]
    return {"base": "sky", "tod": "night", "ground": gy, "groundc": "#8d97a6", "sun": False, "cam": CAM, "els": els}


def s28_add():
    """The same sky: a comet streaks in and breaks up (lilac, dotted); waves roll across the plain; 'flood stories'; 'older than
    the Flood?'; a dotted arrow plunges into the ground: 'why dig so deep?'."""
    sid = "s28"
    t_c, t_fl, t_older, t_deep = T(sid, "comet"), T(sid, "flood stories"), T(sid, "older than"), T(sid, "dig so")
    els = [ln([[1650, 140], [1380, 260]], t_c, LILAC, 4, "claimed", .6)] + \
          [ln([[1380, 260], [1380 - 60 - 30 * j, 270 + 30 * j]], t_c + .6 + .1 * j, LILAC, 2, "claimed", .4) for j in range(4)] + \
          [glow(1380, 260, 90, t_c + .5, .7, "blue"), lab(1500, 330, "a comet?", t_c + .7, LILAC, 26)]
    for j in range(3):
        y = 690 + 34 * j
        els.append(ln([(80 + 40 * k, y + (9 if k % 2 else -9)) for k in range(41)], t_fl - .6 + .3 * j, "#3f86a8", 4, "inferred", 1.0, curve=True))
    els += [lab(130, 676, "flood stories", t_fl, "#9fd0ff", 26, "start"),
            lab(1020, 300, "older than the Flood?", t_older, LILAC, 34, st="serif")]
    els += [arr([[1500, 600], [1490, 680], [1500, 770]], t_deep, "#8a7ad0", 5, "inferred", .8, curve=True), lab(1480, 560, "why dig so deep?", t_deep + .3, LILAC, 28)]
    return els


def s29():
    """Radiocarbon: a bone and a lump of charcoal, each with a small clock that ticks; beside them an empty carved room in a tuff
    cliff (there as the camera lands, 'the digging: undated'), a dashed ring and a '?': nothing to put a clock on."""
    sid = "s29"
    t_nob, t_alive, t_bone, t_empty = T(sid, "Nobody has"), T(sid, "once alive"), T(sid, "bone"), T(sid, "empty space")
    bone = [(-90, -10), (-70, -26), (-56, -14), (56, -14), (70, -26), (90, -10), (80, 0), (90, 10), (70, 26), (56, 14), (-56, 14), (-70, 26), (-90, 10), (-80, 0)]
    els = [poly([(320 + x, 380 + y) for x, y in bone], "#efe6d2", "#ffffff", 1.5, t_bone, "pop", curve=True), lab(320, 450, "bone", t_bone + .2, BONE, 26),
           poly(blob(560, 380, 56, 40, 6, 12, .25), "#2a2420", "#6a5a4a", 1.5, t_bone + .5, "pop", curve=True), lab(560, 450, "charcoal", t_bone + .7, BONE, 26)]
    els += clock(320, 290, 34, t_alive) + clock(560, 290, 34, t_alive + .3) + [lab(440, 560, "once alive: datable", t_alive + .6, GREEN, 28)]
    els += [rect(950, 200, 640, 520, TUFF2, "#e9dccb", 1.5, 6, .2), rect(950, 200, 640, 520, "rgba(0,0,0,.08)", r=6, at=.2)]
    els += [ln([[960 + 24 * j, 210 + (j * 37) % 60], [980 + 24 * j, 230 + (j * 37) % 60]], .4, "#8a7454", 2, draw=False, op=.6) for j in range(26)]
    els += [poly([(1100, 720), (1100, 470), (1150, 380), (1270, 350), (1390, 380), (1440, 470), (1440, 720)], DARK, EDGE, 3, .4, "fade"),
            person(1180, 720, 66, .7, "#d9c7a6"), lab(1270, 172, "the digging: undated", min(t_nob, 1.4), BONE, 28),
            {"k": "circle", "x": 1290, "y": 560, "r": 110, "fill": "none", "c": LILAC, "w": 3, "style": "inferred", "in": t_empty}] + question(1300, 600, t_empty + .4, 90) + \
           [lab(1270, 770, "empty space", t_empty + .6, LILAC, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s30():
    """Xenophon, about 400 BCE: snow on a mountain plain; a cut-away underground house, there as the camera lands: a mouth like a
    well with a ladder, a wide room below, a sloping ramp for the animals; goats, sheep, cattle and poultry come in as they are
    named; a bowl of barley beer with straws; a small map inset, Armenia far east of Cappadocia."""
    sid = "s30"
    t_x, t_mouth, t_ramp, t_in, t_beer = (T(sid, "Xenophon"), T(sid, "a mouth"), T(sid, "ramps"), T(sid, "Inside were"), T(sid, "barley beer"))
    gy = 330
    els = [rect(-10, gy - 2, 1800, 16, "#eef2f6", r=0, at=-1)] + flakes(40, 90, 1700, 130, 320, -1, 3, 0, (4, 8)) + \
          [lab(160, 210, "Xenophon, about 400 BCE", .5, GOLD, 30, "start")]
    els += [rect(640, gy, 60, 120, "#2a221b", EDGE, 2, 2, .4, "fade"), ln([[655, gy - 20], [655, gy + 130]], .6, "#c9a46a", 3, draw=False),
            ln([[685, gy - 20], [685, gy + 130]], .6, "#c9a46a", 3, draw=False)] + \
           [ln([[655, gy + 10 + 22 * j], [685, gy + 10 + 22 * j]], .7, "#c9a46a", 3, draw=False) for j in range(6)] + \
           [poly([(420, 720), (420, 520), (480, 450), (860, 450), (920, 520), (920, 720)], DARK, EDGE, 3, .5, "fade", curve=True),
            glow(670, 600, 260, .8, .35, "lamp"),
            poly([(920, 640), (1240, gy), (1300, gy), (1300, gy + 40), (980, 720), (920, 720)], "#2a221b", EDGE, 2, .6, "fade")]
    els += [lab(560, 300, "a mouth like a well", t_mouth + .3, BONE, 26, "end"), lab(1300, 300, "a ramp for animals", t_ramp + .3, BONE, 26, "start")]
    an = [(GOAT, 500, 30), (COW, 600, 52), (GOAT, 720, 28), (ASS, 820, 40)]
    for j, (sh, x, s) in enumerate(an):
        els.append(beast(sh, x, 720, s * 2, t_in + .2 * j, "#cbbca8", fx="pop"))
    els += [beast(HEN, 470, 718, 60, t_in + .9, "#e8d6b8", fx="pop"), beast(HEN, 880, 718, 56, t_in + 1.0, "#e8d6b8", fx="pop", face=-1)]
    els += [poly([(560, 560), (640, 560), (630, 600), (570, 600)], "#c8743c", "#f4b27a", 1.5, t_beer, "pop")] + \
           [ln([[585 + 14 * j, 566], [600 + 18 * j, 505]], t_beer + .3 + .1 * j, "#f2dcb4", 2, draw=False) for j in range(3)] + \
           [lab(600, 490, "barley beer, with straws", t_beer + .5, AU, 26)]
    v = View(26, 46, 35.5, 42.5, (1340, 470, 330, 200))
    els += [rect(1330, 460, 350, 220, "rgba(18,13,10,.82)", "rgba(255,236,206,.35)", 1.5, 8, t_x)]
    ax_, ay_ = v.p(*DRK)
    bx_, by_ = v.p(43.0, 39.6)
    els += [dot(ax_, ay_, 6, GOLD, t_x + .2), lab(ax_, ay_ + 32, "Cappadocia", t_x + .3, GOLD, 24),
            dot(bx_, by_, 6, "#cfe6ff", t_x + .4), lab(bx_, by_ + 32, "Armenia", t_x + .5, "#cfe6ff", 24),
            arr([[ax_ + 14, ay_ - 8], [(ax_ + bx_) / 2, ay_ - 40], [bx_ - 14, by_ - 8]], t_x + .6, "#cfe6ff", 2.5, dur=.6)]
    return {"base": "sky", "tod": "dusk", "ground": gy, "groundc": "#6a5642", "sun": [1450, 230, 22], "cam": CAM, "els": els}


def s31():
    """The 13,000-year line again (the same drawing): a bone-coloured tick at 2,400 years ago, 'Xenophon', close to the dated sliver,
    very far from the lilac Ice Age marker."""
    sid = "s31"
    t_24, t_east = T(sid, "two thousand four"), T(sid, "east")
    ay = TL_Y
    els = tl13(-1, -1, -1)
    els += [ln([[XT(2400), ay], [XT(2400), ay + 90]], t_24, BONE, 3, dur=.4), dot(XT(2400), ay + 90, 7, BONE, t_24 + .3),
            lab(XT(2400) - 8, ay + 128, "Xenophon", t_24 + .4, BONE, 28, "end"), lab(XT(2400) - 8, ay + 162, "about 2,400 years ago", t_24 + .6, DIM, 26, "end"),
            ln([[XT(12800) + 20, ay + 70], [XT(2400) - 24, ay + 70]], t_east, DIM, 2, "inferred", 1.0), lab((XT(12800) + XT(2400)) / 2, ay + 106, "10,000 years apart", t_east + .5, DIM, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


def s32():
    """Built versus carved, both there as the camera lands. Left: a mound in section, layers stacking up one by one, oldest at the
    bottom, like pages. Right: a room in tuff whose outline grows outwards, each older outline cut away."""
    sid = "s32"
    t_add, t_diary, t_away = T(sid, "grows by adding"), T(sid, "diary"), T(sid, "taking")
    els = [lab(450, 170, "built", .5, GOLD, 34, st="serif"), lab(1300, 170, "carved", .7, GOLD, 34, st="serif"),
           ln([[889, 200], [889, 760]], .3, "rgba(255,236,206,.25)", 2, draw=False), ln([[150, 741], [750, 741]], .3, "#e9dccb", 2, draw=False)]
    tones = ["#6f5a44", "#8a7454", "#a8916b", "#7a6248", "#b9ab94", "#8c7152"]
    for j, c in enumerate(tones):
        y = 740 - 70 * (j + 1)
        w = 520 - 50 * j
        els.append(rect(450 - w / 2, y, w, 68, c, "rgba(255,236,206,.35)", 1, 4, .5 if j == 0 else t_add + .35 * j, "fill"))
    els += [lab(450 + 290, 700, "oldest", t_add + .2, DIM, 24, "start"), lab(450 + 190, 330, "newest", t_add + 2.0, DIM, 24, "start")]
    els += [rect(160 + 40 * j, 230 - 10 * j, 70, 90, "#efe6d2", "#8a7a66", 1, 3, t_diary + .1 * j, "pop") for j in range(3)]
    els += [rect(1000, 240, 600, 500, TUFF2, "#e9dccb", 1.5, 6, .2)]
    rooms = [(1300, 600, 70, 60), (1300, 600, 130, 110), (1300, 600, 210, 180)]
    shape = lambda cx, cy, rx, ry: [(cx - rx, cy + 100), (cx - rx, cy - ry * .4), (cx - rx * .6, cy - ry), (cx + rx * .6, cy - ry), (cx + rx, cy - ry * .4), (cx + rx, cy + 100)]
    for j, r_ in enumerate(rooms):
        t = .6 if j == 0 else t_away - 1.2 + 1.0 * j
        els.append(poly(shape(*r_), DARK, EDGE, 3, t, "pop"))
        for i in range(j):
            els.append(poly(shape(*rooms[i]), "none", LILAC, 2.5, t + .1, style="claimed"))
    els += [person(1420, 700, 50, .9, "#d9c7a6"), lab(1300, 780 - 20, "older walls: gone", t_away + 1.2, LILAC, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s33():
    """The room scraped: the older wall (lilac, dashed) scraped away stroke by stroke, rubble carried out in a basket by a small
    figure; today's wall drawn solid; at right, a blackboard with chalk marks, wiped, and written on again."""
    sid = "s33"
    t_en, t_scr, t_out, t_bb, t_again = T(sid, "enlarged"), T(sid, "scraped off"), T(sid, "carried"), T(sid, "blackboard"), T(sid, "written on")
    old = [(420, 720), (420, 520), (470, 450), (650, 420), (830, 450), (880, 520), (880, 720)]
    new = [(300, 720), (300, 460), (380, 340), (650, 300), (920, 340), (1000, 460), (1000, 720)]
    els = [rect(160, 200, 960, 560, TUFF2, "#e9dccb", 1.5, 6, -1),
           poly(old, DARK, EDGE, 3, -1),
           poly(new, DARK, EDGE, 3, t_en + .6, "pop"), poly(old, "none", LILAC, 3, t_en + .7, style="claimed")]
    marks = [(430, 690), (430, 620), (434, 550), (480, 470), (560, 440), (650, 430), (740, 440), (820, 470), (866, 550), (870, 620), (870, 690)]
    els += [ln([[x, y], [x + 16, y - 12]], t_scr + .08 * k, "#cbbca8", 2.5, dur=.2) for k, (x, y) in enumerate(marks)]
    els += [lab(650, 560, "older surface", t_en, LILAC, 26), lab(650, 280, "today's wall", t_en + 1.0, BONE, 26)]
    els += [person(1060, 740, 90, t_out, "#efe6d4"), oval(1092, 680, 22, 14, "#8a6a44", "#e7c99a", 1.2, at=t_out + .2, fx="pop"),
            arr([[1000, 640], [1100, 610], [1160, 640]], t_out + .4, BONE, 2.5, dur=.5)]
    bx, by, bw, bh = 1250, 300, 400, 280
    els += [rect(bx - 10, by - 10, bw + 20, bh + 20, "#6a4a2a", "#a8805a", 2, 4, .5, "pop"), rect(bx, by, bw, bh, "#1f3a2e", r=2, at=.5, fx="pop")]
    els += [ln([[bx + 40, by + 60 + 50 * j], [bx + 360 - 60 * (j % 2), by + 60 + 50 * j]], t_bb + .2 * j, "#eef2ee", 3, dur=.4) for j in range(4)]
    els += [cover(bx + 2, by + 2, bw - 4, bh - 4, t_bb + 1.5, "#1f3a2e", 1.0, .6)]
    els += [ln([[bx + 40, by + 80 + 60 * j], [bx + 340 - 50 * j, by + 70 + 60 * j]], t_again + .25 * j, "#eef2ee", 3, dur=.5) for j in range(3)]
    els += [lab(bx + bw / 2, by + bh + 60, "wiped, and written again", t_again + .5, BONE, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def longyou_hall():
    """The iso hall of the Short 'longyou-caves' (f07.longyou shot 0), its labels dropped: a cavern with pillars and a sloping roof."""
    import f07
    sc = f07.longyou()["shots"][0]
    iso = next(e for e in sc["els"] if e.get("k") == "iso")
    items = [it for it in iso["items"] if it.get("t") != "label"]
    return items


def s34():
    """Longyou: the hall from the Short (iso, wide); a small pot on its floor, 'about 2,000 years'; a solid arrow to the pot, a dotted
    one to the walls with a '?': a pot dates a visit, not the digging."""
    sid = "s34"
    t_long, t_pot, t_visit, t_dig = T(sid, "Longyou"), T(sid, "pottery inside"), T(sid, "a visit"), T(sid, "Not the")
    els = [glow(760, 560, 560, .2, .2, "lamp"),
           {"k": "iso", "x": 760, "y": 650, "s": 13, "az": -26, "spin": .6, "el": .45, "items": longyou_hall(), "in": .2},
           lab(1320, 170, "Longyou, China", t_long, GOLD, 32), lab(1320, 208, "found 1992, 24 halls", t_long + .4, DIM, 26)]
    px, py = 900, 700
    els += [{"k": "vase", "x": px, "y": py, "h": 60, "in": t_pot, "fx": "rise"}, glow(px, py - 30, 60, t_pot + .2, .7, "lamp"),
            lab(1320, 420, "about 2,000 years", t_pot + .4, AU, 30)]
    els += [arr([[1200, 440], [1000, 520], [px + 34, py - 40]], t_visit, AU, 3, dur=.7), lab(1320, 470, "a visit", t_visit + .3, AU, 28),
            arr([[1240, 540], [1060, 420], [880, 340]], t_dig, LILAC, 3, "claimed", .8)] + question(840, 330, t_dig + .5, 70) + \
           [lab(1320, 590, "not the digging", t_dig + .4, LILAC, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


DEEP = room_of(7, "deep")
X_DEEP = (DEEP[0] + DEEP[1]) / 2


def s35():
    """The deepest level, close, at night (the same picture, the levels above dimmed): the lowest room glows; two faint tags,
    'very old?' and 'fairly new?', then a single lilac '?' in the room."""
    sid = "s35"
    t_old, t_new, t_tell = T(sid, "very old"), T(sid, "fairly new"), T(sid, "alone")
    sc = city_base("night")
    els = city_full() + veil(-1, .55) + spot(7, .3, lit=("deep",), lit_at=.6)
    els += [lab(X_DEEP - 96, 724, "very old?", t_old, "#f2dcb4", 30, "end"), lab(X_DEEP + 96, 724, "fairly new?", t_new, "#f2dcb4", 30, "start"),
            label(round(X_DEEP, 1), 771, "?", round(t_tell, 2), LILAC, 64, st="big", fx="pop")]
    sc.update(cam=[1.8, X_DEEP, 680], els=els)
    return sc


# ================================================================== chapter 4: chapels, raids and refugees
def car(x, y, s, at, kind):
    k = s / 100.
    P = lambda pts: [(x + a * k, y + b * k) for a, b in pts]
    if kind == 0:     # an early, boxy car
        body = P([(-60, 0), (-60, -22), (-30, -22), (-24, -52), (24, -52), (30, -22), (60, -22), (60, 0)])
    elif kind == 1:   # long, with fins
        body = P([(-80, 0), (-80, -20), (-40, -24), (-26, -44), (20, -44), (36, -24), (74, -26), (82, -34), (84, 0)])
    else:             # rounded, modern
        body = P([(-70, 0), (-72, -18), (-40, -26), (-18, -46), (26, -46), (50, -24), (72, -18), (70, 0)])
    return [poly(body, "#c9ad85", "#f2dcb4", 1.5, at, "pop", curve=(kind == 2)),
            {"k": "circle", "x": round(x - 36 * k, 1), "y": round(y, 1), "r": round(11 * k, 1), "fill": "#2a2420", "c": "#8a7a66", "w": 1.5, "in": round(at, 2), "fx": "pop"},
            {"k": "circle", "x": round(x + 38 * k, 1), "y": round(y, 1), "r": round(11 * k, 1), "fill": "#2a2420", "c": "#8a7a66", "w": 1.5, "in": round(at, 2), "fx": "pop"}]


def s36():
    """What can be dated: a tuff wall with a lamp niche, where a cross is incised stroke by stroke, a church plan in the shape of a
    cross, three sherds, each with a green tick; then pots of three styles over cars of three eras: 'styles change'."""
    sid = "s36"
    t_cr, t_ch, t_pot, t_style, t_cars = T(sid, "crosses"), T(sid, "carved churches"), T(sid, "broken Byzantine"), T(sid, "dated by its"), T(sid, "like cars")
    els = [rect(140, 190, 700, 560, TUFF2, "#e9dccb", 1.5, 6, .2), rect(140, 190, 700, 560, "rgba(0,0,0,.06)", r=6, at=.2),
           lab(490, 160, "what can be dated", .5, AMBER, 26)]
    els += [ln([[150 + 28 * j, 200 + (j * 41) % 70], [168 + 28 * j, 222 + (j * 41) % 70]], .4, "#8a7454", 2, draw=False, op=.55) for j in range(24)]
    els += [ln([[300, 260], [300, 420]], t_cr, "#3a2c20", 6, dur=.4), ln([[240, 310], [360, 310]], t_cr + .4, "#3a2c20", 6, dur=.3), tick(380, 260, t_cr + .9)]
    els += [church_plan(600, 330, 26, t_ch, "#3a2c20", 4, "rgba(26,21,17,.15)"), tick(720, 240, t_ch + 1.0)]
    sh = [[(0, 0), (60, -10), (70, 30), (10, 40)], [(0, 0), (50, 6), (40, 50), (-6, 36)], [(0, 0), (64, 4), (56, 34), (6, 30)]]
    for j, s in enumerate(sh):
        x0, y0 = 220 + 180 * j, 560
        els += [poly([(x0 + a, y0 + b) for a, b in s], "#c8743c", "#f4b27a", 1.5, t_pot + .2 * j, "pop"),
                ln([[x0 + 8, y0 + 12], [x0 + 46, y0 + 8]], t_pot + .2 * j + .1, "#5a2a14", 2, draw=False), tick(x0 + 80, y0 - 20, t_pot + .2 * j + .3)]
    els += [lab(490, 700, "Byzantine pottery", t_pot + .8, BONE, 26)]
    els += [rect(960, 432, 620, 10, "#6a5440", "#c9a46a", 1.2, 2, .6), ln([[960, 660], [1580, 660]], .7, "#8a7a66", 2, draw=False)] + \
           [rect(1050 + 220 * j - 46, 442, 92, 22, "#4a3a2b", "#8a7050", 1, 2, .7) for j in range(3)]
    profiles = [[[0, .28], [.1, .24], [.3, .46], [.7, .44], [1, .2]], [[0, .2], [.2, .18], [.5, .5], [.8, .4], [1, .28]], [[0, .34], [.3, .3], [.6, .42], [1, .3]]]
    for j, pr in enumerate(profiles):
        els.append({"k": "vase", "x": 1050 + 220 * j, "y": 430, "h": 120, "w": 100, "profile": pr, "tone": ["#b88a5a", "#c8743c", "#9a7a5a"][j], "in": round(t_style + .3 * j, 2), "fx": "pop"})
    els += [lab(1270, 230, "styles change", t_style + .4, AU, 28)]
    for j in range(3):
        els += car(1050 + 220 * j, 640, 110, t_cars + .3 * j, j)
    els += [lab(1270, 730, "like cars", t_cars + .9, AU, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


AV = View(25.5, 42.5, 33.6, 42.4, (90, 120, 1600, 680))


def s37():
    """Anatolia: Cappadocia pinned and the Taurus ridge drawn as the camera lands; the Byzantine side shaded warm, Caesarea (611); red
    arrows cross the mountains into Cappadocia one after another; '600s to 900s'; two chronicles, one each side."""
    sid = "s37"
    t_by, t_611, t_arab, t_yr, t_chr = T(sid, "Byzantine Empire"), T(sid, "six hundred and eleven"), T(sid, "Arab armies"), T(sid, "every year"), T(sid, "Chroniclers")
    v = AV
    byz = [v.p(lo, la) for lo, la in [(26.5, 41.5), (30, 41.4), (34, 42.0), (38, 41.2), (41, 41.0), (40.5, 39.5), (38.5, 38.4), (36.5, 37.6), (34.5, 37.4), (32, 37.0), (29.5, 36.6), (27, 37.2), (26.2, 39)]]
    taurus = [v.p(lo, la) for lo, la in [(29.6, 37.0), (31.5, 37.0), (33.0, 37.2), (34.5, 37.3), (35.5, 37.6), (36.6, 37.9), (38.0, 38.3), (39.6, 38.7)]]
    dx, dy = v.p(*DRK)
    els = [{"k": "map", "land": v.land(), "in": -1},
           ln(taurus, .6, "#8a6a48", 7, dur=1.0, curve=True), dot(dx, dy, 7, GOLD, .4), ln([[dx - 9, dy + 2], [dx - 132, dy + 12]], .5, GOLD, 1.5, draw=False, op=.7),
           lab(dx - 140, dy + 22, "Derinkuyu", .5, GOLD, 26, "end"),
           poly(byz, "rgba(232,184,122,.16)", AMBER, 2, t_by, curve=True, style="inferred"), lab(*v.p(31.0, 39.6), "Byzantine Empire", t_by + .3, AMBER, 30, st="ital"),
           lab(*v.p(32.0, 36.6), "Taurus mountains", t_arab - .3, DIM, 26, st="ital"),
           lab(*v.p(38.5, 35.6), "Arab caliphate", t_arab, "#e98a8a", 28, st="ital")]
    kx, ky = v.p(35.48, 38.73)
    els += [{"k": "pin", "x": kx, "y": ky, "t": "Caesarea, 611", "c": AMBER, "in": t_611}]
    starts = [(33.2, 36.4), (34.0, 36.6), (34.8, 36.7), (35.6, 36.8), (36.4, 36.6), (37.2, 36.7), (33.6, 36.2), (35.2, 36.3), (36.8, 36.3), (34.4, 36.3)]
    ends = [(32.8, 38.6), (34.0, 39.0), (34.9, 38.5), (35.8, 39.2), (36.6, 38.9), (37.6, 39.4), (33.5, 39.3), (35.3, 39.6), (37.0, 38.3), (34.5, 38.0)]
    for j, (a0, b0) in enumerate(zip(starts, ends)):
        a, b = v.p(*a0), v.p(*b0)
        m = ((a[0] + b[0]) / 2 + (12 if j % 2 else -12), (a[1] + b[1]) / 2)
        els.append(arr([a, m, b], t_yr - 1.6 + .32 * j, RED, 2.5, dur=.6))
    els += chip(v.p(39.5, 37.0)[0], v.p(39.5, 37.0)[1], "600s to 900s", t_yr + 1.6, RED, 26)
    els += book(v.p(27.4, 40.7)[0], v.p(27.4, 40.7)[1], 110, t_chr) + book(v.p(40.3, 35.0)[0], v.p(40.3, 35.0)[1], 110, t_chr + .4)
    return {"base": "map", "cam": CAM, "els": els}


def s38():
    """Dusk: a line of people and a goat go down the entrance stair beneath a house; dust of riders on the horizon; a wheel rolls
    across behind them; lamps glow in the rooms below."""
    sid = "s38"
    t_r, t_an, t_roll, t_wait = T(sid, "raiders came"), T(sid, "animals"), T(sid, "rolled the"), T(sid, "waited")
    gy = 330
    els = [poly(blob(1450, gy - 30, 150, 40, 5, 14, .3), "rgba(200,170,130,.4)", at=t_r, fx="pop", curve=True)] + \
          [person(1360 + 50 * j, gy, 50, t_r + .2 + .1 * j, "#2a2420") for j in range(4)] + flat_house(380, gy, 200, 100, -1, "#8e7152")
    els += [poly([(440, gy), (476, gy), (726, gy + 262), (690, gy + 262)], ROOMC, RIM, 2, -1),
            stair(452, gy + 4, 700, gy + 258, -1, 12, "#8a7050", 2),
            poly(vault(700, 1400, gy + 370, 140), ROOMC, RIM, 2, -1), poly(vault(820, 1340, gy + 520, 100), ROOMC, RIM, 2, -1),
            poly([(1196, gy + 370), (1232, gy + 370), (1262, gy + 420), (1226, gy + 420)], ROOMC, at=-1)]
    for j in range(5):
        x = 470 + 44 * j
        y = gy + 44 * j
        f = beast(GOAT, x, y + 10, 50, t_an + .2 * j, "#e8d6b8", fx="pop") if j == 2 else person(x, y + 6, 70, t_an + .2 * j, "#efe6d4")
        els.append(f)
    els += wheel(745, gy + 300, 52, t_roll, fx=None, op=.5) + [arr([[810, gy + 300], [760, gy + 250], [710, gy + 260]], t_roll, AU, 3, dur=.5)] + \
           wheel(690, gy + 210, 52, t_roll + .6)
    els += [glow(900 + 160 * j, gy + 300, 70, t_wait - .3 + .2 * j, .8, "lamp") for j in range(3)] + [glow(1000, gy + 470, 80, t_wait, .7, "lamp")]
    els += [person(880 + 120 * j, gy + 370, 54, t_wait - .2 + .1 * j, "#efe6d4") for j in range(4)]
    return {"base": "section", "tod": "dusk", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": TUFF, "t": "", "tex": "blocks", "to": .05}], "cam": CAM, "els": els}


XP = lambda yr: round(200 + (yr + 2000) / 4000 * 1380, 1)        # 2000 BCE .. 2000 CE


def s39():
    """2000 BCE to 2000 CE: a solid gold band 'most specialists' from 600 to 1100 CE; dashed markers 'Phrygians?' (about 750 BCE) and
    'Hittites?' (about 1650 to 1200 BCE), both amber and open (a chip 'open' beside them); an arrow off the left edge, 'Ice Age? far
    off this chart'."""
    sid = "s39"
    t_sp, t_ph, t_hi, t_open = T(sid, "Most specialists"), T(sid, "Phrygians"), T(sid, "Hittites"), T(sid, "stay")
    ay = 560
    els = [{"k": "axis", "x0": XP(-2000), "x1": XP(2000), "y": ay, "ticks": [[XP(-2000), "2000 BCE"], [XP(-1000), "1000 BCE"], [XP(1), "1 CE"], [XP(1000), "1000"], [XP(2000), "2000"]], "in": .2},
           ln([[XP(600), ay - 26], [XP(1100), ay - 26]], t_sp + .3, GOLD, 18, dur=.8), lab((XP(600) + XP(1100)) / 2, ay - 56, "most specialists", t_sp + .8, GOLD, 28),
           lab((XP(600) + XP(1100)) / 2, ay - 92, "600s to 1000s CE", t_sp + 1.2, DIM, 26)]
    els += [ln([[XP(-750), ay - 140], [XP(-750), ay]], t_ph, AMBER, 3, "inferred", .5), dot(XP(-750), ay - 140, 8, AMBER, t_ph), lab(XP(-750), ay - 162, "Phrygians?", t_ph + .2, AMBER, 28)]
    els += [rect(XP(-1650), ay - 260, XP(-1200) - XP(-1650), 20, "rgba(240,176,106,.15)", AMBER, 2, 10, t_hi, style="inferred"), lab((XP(-1650) + XP(-1200)) / 2, ay - 280, "Hittites?", t_hi + .2, AMBER, 28),
            ln([[XP(-1425), ay - 240], [XP(-1425), ay]], t_hi, AMBER, 2, "inferred", .5)]
    els += chip((XP(-1425) + XP(-750)) / 2, ay - 360, "open", t_open, GRADE["open"], 28)
    els += [arr([[XP(-1900), ay + 120], [120, ay + 120]], t_open + .6, LILAC, 3, "claimed", .6), lab(XP(-1900) + 10, ay + 160, "Ice Age? far off this chart", t_open + .8, LILAC, 26, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s40():
    """A village about 1910 in section: houses, a trapdoor and stair inside each; galleries running down beneath the village to a blue
    water line, 'water, about 70 m'; a notebook '1910'; 'katafygia: refuges'."""
    sid = "s40"
    t_10, t_ent, t_kat, t_mal, t_70 = T(sid, "Around"), T(sid, "entrances inside"), T(sid, "katafygia"), T(sid, "Malakopi"), T(sid, "seventy metres")
    gy = 260
    main = [(640, gy + 200), (980, gy + 200), (1000, gy + 290), (620, gy + 300), (600, gy + 390), (1000, gy + 400), (1010, gy + 488)]
    rooms = [(700, gy + 178, 140), (450, gy + 278, 150), (1050, gy + 380, 150), (760, gy + 370, 120)]
    els = [ln(main, .5, "#2a221b", 16, draw=False, op=.22)] + [rect(x, y, w, 40, DARK, at=.5, op=.22, r=6) for x, y, w in rooms] + \
          [ln([[x + 120, gy + 92], [x + 150, gy + 150], [700 + 60 * j, gy + 200]], .5, "#2a221b", 14, draw=False, op=.22) for j, x in enumerate((240, 520, 800, 1080))]
    for j, x in enumerate((240, 520, 800, 1080)):
        els += flat_house(x, gy, 160, 90, -1, "#a8916b")
        els += [rect(x + 60, gy - 6, 36, 8, "#3a2c20", r=1, at=t_ent + .2 * j, fx="pop"), stair(x + 70, gy + 2, x + 120, gy + 90, t_ent + .2 * j + .1, 4, "#e9dccb", 2.5)]
    for j, x in enumerate((240, 520, 800, 1080)):
        els += [ln([[x + 120, gy + 92], [x + 150, gy + 150], [700 + 60 * j, gy + 200]], t_ent + .3 + .2 * j, "#2a221b", 14, dur=.6)]
    els += [ln(main, t_mal, "#2a221b", 16, dur=1.8)]
    for j, (x, y, w) in enumerate(rooms):
        els.append(rect(x, y, w, 40, DARK, EDGE, 1.5, 6, t_mal + .4 + .3 * j, "pop"))
    els += [rect(920, gy + 466, 200, 34, DARK, EDGE, 1.5, 4, t_70 - .4, "pop"), rect(80, gy + 490, 1620, 16, "rgba(95,168,201,.55)", at=t_70, fx="fill"),
            lab(1150, gy + 474, "water, about 70 m", t_70 + .3, "#9fd0ff", 28, "start")] + dimv(1520, gy, gy + 490, "", t_70, "#9fd0ff", lx=24)
    els += [rect(1520, 132, 150, 108, "#efe6d2", "#8a7a66", 1.5, 4, t_10, "pop"), lab(1595, 172, "1910", t_10 + .2, "#5a4632", 32, st="serif", halo=False)] + \
           [ln([[1536, 192 + 13 * j], [1654, 192 + 13 * j]], t_10 + .1, "#8a7a66", 2, draw=False) for j in range(3)]
    els += [lab(160, gy + 230, "katafygia:", t_kat, GOLD, 32, "start", st="ital"), lab(160, gy + 272, "refuges", t_kat + .3, GOLD, 32, "start", st="ital"),
            lab(160, gy + 120, "Malakopi (Derinkuyu)", t_mal, DIM, 26, "start")]
    return {"base": "section", "tod": "day", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": TUFF, "t": "", "tex": "blocks", "to": .05}], "cam": CAM, "els": els}


def s41_add():
    """The same village at night: a dark veil over the sky (the notebook of 1910 fades under it), lamps going down the stairs into the
    galleries; '1909'."""
    sid = "s41"
    t_09, t_ref, t_n = T(sid, "In"), T(sid, "took refuge"), T(sid, "some nights")
    gy = 260
    els = [cover(-10, 0, 1800, gy + 1, t_09, "#0b0d16", .8, 1.2), lab(1470, 176, "1909", t_09 + .4, GOLD, 36, "end", st="serif"), lab(1470, 218, "news from Adana", t_09 + .8, DIM, 26, "end")]
    for j, x in enumerate((240, 520, 800, 1080)):
        els.append(rect(x + 18, gy - 63, 22, 16, "#ffd98a", at=t_09 + .6 + .1 * j, fx="fade", op=.85))
        for k in range(3):
            els.append(glow(x + 76 + 16 * k, gy + 20 + 28 * k, 26, t_ref + .25 * j + .3 * k, .9, "lamp"))
    els += [glow(820, gy + 300, 160, t_n + .4, .5, "lamp")]
    return els


ZV = View(19.5, 37.5, 34.6, 42.4, (90, 120, 1600, 680))


def s42():
    """The Aegean and Anatolia: a soft arrow from Cappadocia to Greece and another from Greece to Anatolia; '1923: an exchange of
    populations'; Cappadocia's pin dims: the tunnels fell silent."""
    sid = "s42"
    t_ex, t_gr, t_sil = T(sid, "exchange"), T(sid, "had to leave"), T(sid, "fell")
    v = ZV
    cx, cy = v.p(*DRK)
    ax, ay = v.p(22.9, 40.6)
    bx, by = v.p(23.7, 38.0)
    tx, ty = v.p(30.5, 39.5)
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(22.0, 39.3), "Greece", .4, DIM, 30, st="ital"), lab(*v.p(32.5, 39.0), "Turkey", .4, DIM, 30, st="ital"),
           {"k": "pin", "x": cx, "y": cy, "t": "Cappadocia", "c": GOLD, "in": .5},
           arr([[cx - 10, cy - 14], [(cx + ax) / 2, min(cy, ay) - 120], [ax + 14, ay + 10]], t_gr, AMBER, 4, dur=1.2),
           arr([[bx + 14, by + 4], [(bx + tx) / 2, by + 60], [tx - 10, ty + 10]], t_ex + .4, "#cfe6ff", 3, "inferred", 1.0)] + \
          chip(889, 760 - 40, "1923: an exchange of populations", t_ex, GOLD, 28) + \
          [{"k": "circle", "x": cx, "y": cy, "r": 30, "fill": "rgba(13,11,9,.6)", "c": "none", "w": 0, "in": t_sil, "dur": 1.2}]
    return {"base": "map", "cam": CAM, "els": els}


def s43():
    """The opening picture again (the same drawing): the house on the plateau at dusk, the man in the basement, the wall breaking
    open and the room behind it; '1963'."""
    sid = "s43"
    t = T(sid, "basement wall")
    sc = city_base("dusk")
    sc.update(cam=[4.4, 676, 180], els=house_els() + cellar_els() + wall_break(t - .5, t + .3) + found_room(t + .45) +
              [lab(812, 214, "1963", .4, GOLD, 34, st="serif")])
    return sc


# ================================================================== chapter 5: the weighing
ROWS = [210, 345, 480, 615]


def s44():
    """A ledger board: four rows, each with a small picture (a church plan, a house with a cellar stair, a first pick mark, a
    snowflake); row 1 'Byzantine refuges' lights and its chip 'Established' pops; row 2 'used until 1923', 'Established'."""
    sid = "s44"
    t_r1, t_e1, t_r2, t_e2 = T(sid, "Underground refuges"), T(sid, "established"), T(sid, "Their use"), T(sid, "established", k=2)
    els = [rect(110, 130, 1560, 600, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    names = ["Byzantine refuges", "used until 1923", "the first rooms", "Ice Age shelters"]
    t_rows = [t_r1, t_r2, None, None]
    for k, (y, nm) in enumerate(zip(ROWS, names)):
        tr = t_rows[k] if t_rows[k] is not None else 999
        els += [rect(130, y - 55, 1520, 110, "rgba(242,201,142,.06)", "rgba(242,201,142,.25)", 1.5, 12, .3)]
        if tr < 999:
            els += [rect(130, y - 55, 1520, 110, "rgba(242,201,142,.10)", "rgba(242,201,142,.45)", 1.5, 12, tr, "pop"), lab(380, y + 11, nm, tr + .1, BONE, 32, "start")]
    ix = 250
    els += [church_plan(ix, ROWS[0] - 4, 9, .5, AU, 2.5)]
    y = ROWS[1]
    els += flat_house(ix - 40, y + 4, 80, 44, .6, "#a8916b", win=False) + [stair(ix - 10, y + 6, ix + 20, y + 44, .6, 3, "#e9dccb", 2)]
    y = ROWS[2]
    els += [rect(ix - 50, y - 36, 100, 72, TUFF2, "#e9dccb", 1.2, 4, .7), ln([[ix - 20, y - 10], [ix + 20, y + 14]], .7, "#3a2c20", 4, draw=False)]
    y = ROWS[3]
    for a in range(3):
        ang = math.radians(60 * a)
        els.append(ln([[ix - 30 * math.cos(ang), y - 30 * math.sin(ang)], [ix + 30 * math.cos(ang), y + 30 * math.sin(ang)]], .8, "#e8f0f8", 4, draw=False))
    cx0 = 1080
    els += chip(cx0, ROWS[0], "Established", t_e1, GRADE["established"], a="start")
    els += chip(cx0, ROWS[1], "Established", t_e2, GRADE["established"], a="start")
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s45_add():
    """Ledger row 3 'the first rooms' lights ('Phrygians? Hittites? Byzantines?' under it) and its chip 'Open question' pops."""
    sid = "s45"
    t_r3, t_o = T(sid, "When were"), T(sid, "open question")
    y = ROWS[2]
    return [rect(130, y - 55, 1520, 110, "rgba(242,201,142,.10)", "rgba(242,201,142,.45)", 1.5, 12, t_r3, "pop"), lab(380, y + 2, "the first rooms", t_r3 + .1, BONE, 32, "start"),
            lab(380, y + 38, "Phrygians? Hittites? Byzantines?", t_r3 + 1.6, DIM, 24, "start")] + chip(1080, y, "Open question", t_o, GRADE["open"], a="start")


def s46():
    """The doors' clue: a stone wheel shut across a passage; small raider figures stop at it, red arrows bounce back; snowflakes drift
    down an air shaft beside it, unaffected: 'keeps out people', 'not frost'."""
    sid = "s46"
    t_d, t_p, t_f = T(sid, "the doors"), T(sid, "keeps out"), T(sid, "frost")
    els = [rect(140, 200, 1500, 560, TUFF2, "#e9dccb", 1.5, 6, -1), rect(140, 200, 1500, 360, "rgba(0,0,0,.06)", at=-1)] + \
          [dot(round(160 + 1120 * ((j * 0.618034) % 1), 1), round(222 + 320 * ((j * 0.414214) % 1), 1), round(2 + 2.5 * ((j * 0.732051) % 1), 1), "#6f5a44", -1, op=.55) for j in range(70)] + \
          [ln([[170 + 46 * j, 222 + (j * 37) % 80], [188 + 46 * j, 246 + (j * 37) % 80]], -1, "#8a7454", 2, draw=False, op=.5) for j in range(24)] + \
          [rect(140, 560, 1500, 200, "#2a221b", EDGE, 2, 2, -1), glow(1120, 690, 120, .3, .45, "lamp")]
    els += wheel(889, 660, 98, t_d)
    for j in range(3):
        x = 300 + 120 * j
        els += [person(x, 760, 120, t_p - .6 + .15 * j, "#cbbca8"), arr([[x + 60, 700], [800 - 10, 690], [x + 120, 650]], t_p + .2 * j, RED, 3, dur=.6)]
    els += [lab(450, 520, "keeps out people", t_p + .5, GREEN, 30)]
    els += [rect(1300, 120, 60, 640, "#2a221b", EDGE, 1.5, 2, -1)] + flakes(18, 1312, 1348, 140, 740, t_f - .4, 2, .05, (5, 8)) + \
           [lab(1400, 300, "not frost", t_f + .3, LILAC, 30, "start"), lab(1400, 340, "air shafts stay open", t_f + .6, DIM, 26, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s47_add():
    """Ledger row 4 'Ice Age shelters' lights, its snowflake gets a lilac ring, and its chip 'Awaiting evidence' pops."""
    sid = "s47"
    t_r4, t_aw = T(sid, "Shelters from"), T(sid, "Awaiting")
    y = ROWS[3]
    return [rect(130, y - 55, 1520, 110, "rgba(201,193,238,.10)", "rgba(201,193,238,.5)", 1.5, 12, t_r4, "pop"), lab(380, y + 11, "Ice Age shelters", t_r4 + .1, BONE, 32, "start"),
            ring(250, y, 46, t_aw + .3, LILAC, 3)] + chip(1080, y, "Awaiting evidence", t_aw, GRADE["awaiting"], a="start")


def mud_house(x, gy, w, h, at):
    return [rect(x, gy - h, w, h, "#9a7a52", "#d8bd93", 1.2, 2, at, "rise")] + [ln([[x, gy - h + 8 * j], [x + w, gy - h + 8 * j]], at + .1, "#7a5a3a", 1, draw=False, op=.6) for j in range(1, int(h / 8))]


AV2 = View(34.10, 34.90, 38.22, 38.50, (100, 170, 1120, 560))        # Asikli Hoyuk and Derinkuyu


def s48():
    """A close map again: Derinkuyu; a pin 'Asikli Hoyuk' about 45 km west; beside it, small mud-brick houses rise above the ground;
    'after the Ice Age'."""
    sid = "s48"
    t_a, t_mud, t_after = T(sid, "Asikli"), T(sid, "mud brick"), T(sid, "after the Ice")
    v = AV2
    ax, ay = v.p(*SITES["Asikli"])
    dx, dy = v.p(*DRK)
    els = [{"k": "map", "land": v.land(), "landc": "#4a3c2e", "in": -1}] + graticule(v, 34.10, 34.90, 38.22, 38.50) + [
           {"k": "pin", "x": dx, "y": dy, "t": "Derinkuyu", "c": GOLD, "in": .3, "a": "middle", "lx": 0, "ly": -30},
           dot(ax, ay, 8, GREEN, 1.0), {"k": "pin", "x": ax, "y": ay, "t": "Aşıklı Höyük", "c": GREEN, "in": t_a, "a": "middle", "lx": 0, "ly": -30},
           ln([[ax + 18, ay - 3], [dx - 18, dy + 2]], t_a + .4, DIM, 2, "inferred", .8), lab((ax + dx) / 2, (ay + dy) / 2 + 44, "about 45 km", t_a + .8, DIM, 28)] + \
          scalebar(200, 740, round(v.km(10), 1), "10 km", .6)
    x0, gy = 1330, 560
    els += [rect(x0 - 20, 330, 380, 330, "rgba(18,13,10,.82)", "rgba(255,236,206,.35)", 1.5, 10, 1.2, "pop"),
            rect(x0 - 18, gy, 376, 98, "#6a5642", at=1.3, fx="fade"), ln([[x0 - 18, gy], [x0 + 358, gy]], 1.3, "#d8bd93", 2, draw=False),
            glow(x0 + 170, gy - 60, 150, 1.4, .25, "lamp"), ln([[ax + 14, ay - 14], [x0 - 26, 470]], t_a + .3, "rgba(143,217,176,.5)", 2, "inferred", .5)]
    for j in range(5):
        els += mud_house(x0 + 20 + 64 * j - (j % 2) * 18, gy - (j % 2) * 26, 54, 42, t_a + .6 + .15 * j)
    els += [lab(x0 + 170, 630, "mud brick, above ground", t_mud + .6, AU, 26)]
    els += chip(x0 + 170, 390, "after the Ice Age", t_after, GREEN, 28)
    return {"base": "map", "cam": CAM, "els": els}


def s49_add():
    """Test 1: under the deepest room's floor, a small hearth with charcoal and a bone glows; a dashed ring and a tag 'dated?'
    (dashed: not done)."""
    sid = "s49"
    t_h, t_d = T(sid, "A hearth"), T(sid, "radiocarbon")
    x0, x1, fl, h = DEEP
    cx, cy = X_DEEP - 20, fl + 14
    return [poly(blob(cx, cy, 26, 7, 4, 10, .2), "#3a2a20", "#8a6a4a", 1.2, t_h, "pop", curve=True), dot(cx - 10, cy - 1, 4, "#2a2420", t_h + .1), dot(cx + 6, cy + 1, 3.5, "#2a2420", t_h + .15),
            poly([(cx + 10, cy - 3), (cx + 22, cy - 5), (cx + 24, cy - 1), (cx + 12, cy + 1)], "#efe6d2", at=t_h + .3, fx="pop"),
            glow(cx, cy, 34, t_h + .2, .9, "fire"),
            {"k": "circle", "x": round(cx, 1), "y": round(cy, 1), "r": 34, "fill": "none", "c": "#f2dcb4", "w": 2.5, "style": "inferred", "in": t_d}] + \
           chip(cx + 150, cy + 4, "dated?", t_d + .3, "#f2dcb4", 28, style="inferred")


def s50():
    """Test 2: a tuff wall (there as the camera lands, two magnifiers on it) whose marks draw as said: broad shallow scoops on one side,
    narrow sharp cuts on the other; a stone tool and an iron pick hover beside them with a '?'."""
    sid = "s50"
    t_tm, t_st, t_ir = T(sid, "tool marks"), T(sid, "stone tools"), T(sid, "iron")
    els = [rect(160, 190, 1460, 560, TUFF2, "#e9dccb", 1.5, 6, -1), rect(160, 190, 1460, 560, "rgba(0,0,0,.08)", r=6, at=-1),
           glow(889, 300, 300, .3, .25, "lamp")]
    els += [ln([[180 + 44 * j, 210 + (j * 53) % 90], [196 + 44 * j, 236 + (j * 53) % 90]], -1, "#8a7454", 2, draw=False, op=.5) for j in range(32)]
    els += magnifier(500, 420, 170, .5, BONE) + magnifier(1180, 400, 170, .8, BONE)
    for j in range(6):
        els.append({"k": "line", "p": ellipse(420 + 70 * (j % 3), 360 + 120 * (j // 3), 50, 22, 12, 200, 340), "c": "#5a4632", "w": 4, "curve": True, "in": round(t_tm + .1 * j, 2), "fx": "draw", "dur": .4})
    els += [ln([[1060 + 26 * j, 300 + 6 * (j % 2)], [1100 + 26 * j, 470]], t_tm + .6 + .07 * j, "#3a2c20", 2.5, dur=.3) for j in range(10)]
    els += [poly([(440, 640), (500, 600), (560, 620), (540, 680), (470, 690)], "#6a6e72", "#c9ccd2", 1.5, t_st, "pop"), lab(500, 740, "stone tools?", t_st + .2, BONE, 28)]
    els += [poly([(1100, 640), (1170, 610), (1240, 618), (1170, 626)], "#c9ccd2", "#ffffff", 1, t_ir, "pop"), ln([[1170, 618], [1200, 700]], t_ir, "#8a6a44", 7, draw=False),
            lab(1190, 740, "iron?", t_ir + .2, BONE, 28)]
    els += question(840, 520, t_ir + .4, 80)
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s51():
    """Test 3: near the town (there as the camera lands), a low spoil heap of pale tuff chips over the old dark soil line; a dashed
    core is drawn down through the heap into that soil; tag 'date it' (dashed: not done)."""
    sid = "s51"
    t_rock, t_dump, t_soil = T(sid, "dug out rock"), T(sid, "dumped"), T(sid, "buried beneath")
    gy = 560
    heap = [(400, gy), (520, gy - 80), (700, gy - 140), (900, gy - 150), (1100, gy - 110), (1280, gy - 40), (1380, gy)]
    els = flat_house(1450, gy, 140, 80, -1, "#8e7152") + flat_house(1600, gy, 110, 64, -1, "#9a7d5c") + flat_house(160, gy, 120, 70, -1, "#9a7d5c")
    els += [poly(heap, TUFF, "#f2dcb4", 2, .3, "rise", curve=True)]
    rr = random.Random(12)
    els += [dot(round(rr.uniform(520, 1250), 1), round(rr.uniform(gy - 120, gy - 10), 1), round(rr.uniform(3, 6), 1), "#e9dccb", round(.6 + .01 * k, 2)) for k in range(70)]
    els += [lab(900, gy - 190, "dug-out rock", t_rock + .3, AU, 28), glow(900, gy - 60, 260, t_dump, .3, "lamp")]
    els += [rect(80, gy, 1620, 26, "#3a2a1e", "#6a4a32", 1.2, 0, -1), lab(200, gy + 70, "old soil", t_soil, "#c9a46a", 26, "start")]
    els += [rect(880, gy - 190, 40, 250, "rgba(245,236,220,.06)", BONE, 2.5, 6, t_soil + .2, style="inferred"),
            ln([[900, gy - 240], [900, gy - 190]], t_soil + .2, BONE, 3, "inferred", .4)] + chip(1100, gy + 110, "date it?", t_soil + .8, "#f2dcb4", 28, style="inferred")
    return {"base": "section", "tod": "day", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": "#5a4636", "t": ""}, {"d": 26, "c": TUFF2, "t": ""}], "cam": CAM, "els": els}


def s52():
    """Test 4: the city at night (the same picture, dimmed), and survey lines sweeping across the levels no visitor sees."""
    sid = "s52"
    t = T(sid, "full survey")
    sc = city_base("night")
    els = city_full() + veil(-1, .45)
    for j, k in enumerate(range(3, 8)):
        y = LVF[k] - 16
        els += [ln([[380, y], [1180, y]], t + .2 * j, "#9fd0ff", 1.6, dur=.8, op=.75)]
        els += [dot(400 + 80 * i, y, 3.2, "#cfe6ff", round(t + .2 * j + .08 * i, 2)) for i in range(10)]
    els += [ln([[1196, LVF[3] - 52], [1212, LVF[3] - 52], [1212, BOT + 6], [1196, BOT + 6]], t, "#9fd0ff", 2.5, dur=.8),
            lab(1230, 600, "levels no visitor sees", t + .4, "#bfe2ff", 28, "start")]
    sc.update(cam=CAM, els=els)
    return sc


def s53_add():
    """The close, nearer the house: one lit window; in its cellar near the surface, a figure with a lamp cuts a new niche, tiny
    chips falling."""
    sid = "s53"
    t_s, t_dug = T(sid, "Soft rock"), T(sid, "keeps getting")
    x0 = CELLAR[0]
    return [rect(574, GY - 31, 13, 10, "#ffd98a", at=t_s, fx="pop"), glow(580, GY - 26, 40, t_s, .8, "lamp"),
            glow(596, F0 - 10, 46, t_s + .3, .85, "lamp"), dot(598, F0 - 3, 2.2, "#ffd98a", t_s + .3),
            person(582, F0, 12.5, t_s + .4, "#efe6d4"), ln([[579, F0 - 8], [571, F0 - 13]], t_s + .5, "#c9a46a", 1.3, draw=False),
            poly([(x0 + 1, F0 - 22), (x0 - 9, F0 - 20), (x0 - 11, F0 - 9), (x0 + 1, F0 - 7)], "#120d09", at=t_dug, fx="pop")] + \
           [dot(x0 + 3 + 2 * (j % 2), F0 - 12 + 2.5 * j, 1.2, "#efe6d4", round(t_dug + .3 + .18 * j, 2)) for j in range(5)]


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "Below it lay", "s2"), (2, "Stables and", "s3"), (3, "So who dug", "s4")], {}),
    (0, 1, "title", "s4", [], {"intro": True}),
    (1, 0, "world", "s6", [(0, "Between about ten", "s7"), (1, "The ash settled", "s8"), (2, "Tuff is light", "s9"), (3, "Rain and wind", "s10")],
     {"chapter": "Rooms cut from volcanic ash"}),
    (1, 1, "cost", "s11", [], {}),
    (1, 2, "collision", "s12", [(0, "Reports count", "s13"), (1, "Stables and storerooms", "s14"), (1, "A church cut", "s14c"), (1, "And more than fifty", "s14b")], {}),
    (1, 3, "reversal", "s15", [(0, "From a little room", "s16"), (1, "This was no cave", "s17")], {}),
    (2, 0, "world", "s18", [(1, "In {1972", "s19"), (1, "It led him", "s19b"), (2, "Surveyors now", "s20")], {"chapter": "A landscape of hiding places"}),
    (2, 1, "collision", "s21", [(1, "Geophysicists scanned", "s22"), (1, "Their first results", "s23")], {}),
    (2, 2, "tag", "s24", [], {}),
    (3, 0, "world", "s25", [(1, "Nearly thirteen", "s26"), (1, "Hancock points", "s27"), (2, "He ties that cold", "s28")], {"chapter": "Shelters from the Ice Age?"}),
    (3, 1, "collision", "s29", [(1, "And people really", "s30"), (2, "That was about", "s31")], {}),
    (3, 2, "reversal", "s32", [(1, "Every time a room", "s33"), (2, "It's the same at", "s34")], {}),
    (3, 3, "tag", "s35", [], {}),
    (4, 0, "world", "s36", [(1, "From the six", "s37")], {"chapter": "Chapels, raids and refugees"}),
    (4, 1, "collision", "s38", [(1, "Most specialists", "s39")], {}),
    (4, 2, "reversal", "s40", [(1, "In {1909", "s41"), (2, "In {1923", "s42"), (2, "Forty years later", "s43")], {}),
    (5, 0, "weigh", "s44", [(1, "When were the very", "s45"), (1, "And the doors hint", "s46"), (2, "Shelters from the Ice", "s47"),
                            (2, "And the oldest village", "s48")], {"chapter": "The weighing"}),
    (5, 1, "test", "s49", [(0, "A study of the tool", "s50"), (0, "Or the dug-out", "s51"), (0, "And a full survey", "s52")], {}),
    (5, 2, "close", "s53", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s2": ("s1", [1, 889, 500], "s2_add"), "s3": ("s1", [1, 889, 500], "s3_add"),
    "s8": ("s7", [1, 889, 500], "s8_add"),
    "s13": ("s12", [1, 889, 500], "s13_add"),
    "s14c": ("s14", [1.9, 830, 652], "s14c_add"), "s14b": ("s14", [1, 889, 500], "s14b_add"),
    "s16": ("s15", [1, 889, 500], "s16_add"), "s17": ("s14", [1, 889, 500], "s17_add"),
    "s19b": ("s19", [1, 889, 500], "s19b_add"),
    "s22": ("s21", [1, 889, 500], "s22_add"), "s28": ("s27", [1, 889, 500], "s28_add"),
    "s41": ("s40", [1, 889, 500], "s41_add"),
    "s45": ("s44", [1, 889, 500], "s45_add"), "s47": ("s44", [1, 889, 500], "s47_add"),
    "s49": ("s35", [1.6, X_DEEP, 690], "s49_add"), "s53": ("s52", [2.6, 640, 205], "s53_add"),
}


def _segments(script):
    """The narration each shot has on screen, from the beats with their markers (a chapter beat's first sentence is the card's)."""
    say = {}
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            if sid in ALIASES and ALIASES[sid][2] is None:
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
            say[frm] = say[frm] + " " + head if frm in say else head
        for k in range(1, len(parts), 2):
            say[parts[k]] = parts[k + 1]
    return say


def _no_cap_dots(els):
    """kit.js traces a line by its dash offset, and Chromium paints the round cap of the hidden dash at the line's start: a thick line
    drawn late would show a dot there until it draws. Those fade in instead."""
    for e in els:
        if e.get("k") == "panel":
            _no_cap_dots(e.get("els", []))
        elif e.get("k") == "line" and e.get("fx") == "draw" and (e.get("w") or 2) >= 7 and (e.get("in") or 0) >= 1.6 and not e.get("keepdraw"):
            e["fx"], e["dur"] = "fade", .5


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
    ep = {"id": "lf-derinkuyu", "code": "LF.08", "series": script["series"], "title": script["title"], "case": "derinkuyu",
          "verdict": "unsupported", "claim": "Were Cappadocia's underground cities first dug as shelters from the Ice Age, or as Byzantine refuges?",
          "mood": "mystery", "hook_text": "Who dug a *city* under the ground?", "beats": beats, "shots": shots,
          "sources": "Nývlt et al. 2016 (doi:10.1016/j.proeng.2016.08.824) · Yamaç 2022 (doi:10.52486/01.00003.6) · Yamaç & Tok 2026 (doi:10.1007/978-3-032-16095-9) · "
                     "Ulusay & Aydan 2018 (doi:10.1007/s10064-017-1190-5) · Dawkins 1916, Modern Greek in Asia Minor · Hancock 2015, Magicians of the Gods",
          "post": "In 1963 a man knocked through his basement wall in central Turkey and found a city 85 metres deep. Who dug Cappadocia's underground "
                  "cities, and when? Byzantine refuges, a scholar's notes from 1910, and the claim that they are Ice Age shelters older than the Flood, weighed.",
          "hashtags": ["#Derinkuyu", "#Cappadocia", "#UndergroundCity", "#Archaeology", "#WeighItYourself"],
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
    for st in ep["shots"]:
        _no_cap_dots(st.get("els", []))
    return ep


def EPISODES():
    return [film()]
