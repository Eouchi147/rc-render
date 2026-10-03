"""LF.22 · Under Giza · The Age of the Sphinx (16:9 long film, one wall).

The script is films/long/lf-sphinx/script.json: its lines are read from there, untouched, and only [go:N|t] markers are added at
the sentence where the picture changes (see BEATS). One scene per script shot (s1..s50; s4, the title, is the intro card over the
panel of s3), drawn while it is said: the Sphinx in its pit at dawn with a jumbo jet for scale, the prince asleep in the sand, the
Eocene sea and its coin-shaped fossils (Strabo's lentils), the layer cake of the plateau and the U-shaped trench, the blocks dragged
to the temple and Aigner's yellow band, Khafre's causeway, the edge shared by trench and causeway, the joint of the two temples, the
builders' rubbish of 1978, the unfinished temple, the three candidate kings; Schoch's wall, the wind and the rain, the tombs, the
seismic floor (up to 2.5 m in front, about 1.2 m behind), his dates, the temples and the head; Reader's runoff; Gauri's salt, the
karst joints, Harrell's damp sand, the speed of decay, the critics' readings, the first farmers of the Fayum, Gobekli Tepe's trail,
light dating and its four dates; Thutmose IV's walls (a cartouche), the Dream Stele and the flaked name, the patches of every age,
the surveys and the hollow under the paws; the ledger, the tests and the close. Drawings are schematic and true to the numbers
said: solid = measured, dashed = inferred, dotted = claimed (the old-Sphinx claims are lilac and dotted throughout).

Facts: the Shorts 'sphinx-erosion', 'sphinx-chambers', 'sphinx-surveys' (f05.py, rewrite/*.json) and the script's facts_added
(Lehner 1992, 2003; AERA; Hadingham 2010; Schoch 1992, 1995; Dobecki & Schoch 1992; Schoch & Bauval 2017; Gauri 1984; Gauri et al.
1995; Harrell 1994; Reader 2001; Liritzis & Vafiadou 2015; Linseele et al. 2014; Dietrich et al. 2012, 2019; Strabo; Mallet 1888;
Dolphin 1999).

Engine workaround (as in lf_troy.py): the wall only adds elements to a panel on its first visit, at a beat start or a line start;
shots that return to a panel are aliases of it with a camera whose zoom carries a tiny unique tag (+0.0001 per tag, invisible);
after the wall is built, the step that reached that camera gets the shot's additions as a panel item (built on that step's clock).

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-sphinx/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-sphinx/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-sphinx RC_FILMS_EPS=/tmp/claude-0/sbx_lf-sphinx/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-sphinx/boards python3 films.py long.lf_sphinx
"""
import json, math, os, random, re
from films import View
from mural import remix
import illus as I
from illus import person, glow, label, dot, box, ellipse, strike
from scenes import GP, NILE, ROSETTA, DAMIETTA

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "lf-sphinx", "script.json")
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800
CAM = [1, 889, 500]

BONE, AMBER, BLUE, LILAC, RED, GREEN = I.BONE, I.AMBER, I.BLUE, I.LILAC, I.RED, I.GREEN
GOLD, AU, DIM, MUTED = "#f2c98e", "#e8c35a", "#cbbca8", "#bfb09c"
STONE, STONE_L, STONE_D, SOFT = "#d6bd92", "#ecd8b2", "#8c7152", "#9c8160"   # limestone, lit, shade, a soft bed
REEF, YEL = "#6f5a44", "#e3b84a"                                                # Member I, the yellow band
GRAN, GRAN_D = "#b8615a", "#7e3d38"                                             # red granite
MUD = "#8a6a4a"
SKIN, INK = "#e8d6b8", "#1a1511"
SAND, SAND_D = "#c9a978", "#7d6344"
SEAC = "#3f86a8"
GRADE = {"established": "#8fd9b0", "strong": "#7fd1d4", "open": "#f0b06a", "awaiting": "#c9c1ee", "ruled": "#e98a8a"}


# ================================================================== narration: the script's own lines, and when each word is said
TAGS = re.compile(r"\[[^\]]*\]")
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # BCE: three letters
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
    for li, ln in enumerate(text.split("\n")):
        if li:
            t += LGAP
        cuts = [0] + [m.start() for m in SENT.finditer(ln) if m.start() > 0] + [len(ln)]
        for a, z in zip(cuts, cuts[1:]):
            seg = ln[a:z]
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


def E(cx, cy, rx, ry, n=36):
    return ellipse(cx, cy, rx, ry, n)[:-1]


def chip(x, y, t, c, at, size=28, a="middle", z=1.0):
    """A pill with a coloured rim and its words (grades, dates). z: the camera zoom it will be seen at (the pill is drawn 1/z the size,
    so that it looks right next to its words, which keep their size against the zoom)."""
    w = (len(t) * size * .56 + 44) / z
    h = size * 1.7 / z
    x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
    return [rect(x0, y - h / 2, w, h, "rgba(18,13,10,.9)", c, 2.5 / z, h / 2, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .36 / z, 1), t, round(at + .05, 2), c, size, st="lab", fx="pop")]


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


def axis(x0, x1, y, ticks, at, t=None):
    e = {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": [[round(a, 1), b] for a, b in ticks], "in": round(at, 2)}
    if t:
        e["t"] = t
    return e


def wipe(x, y, w, h, at, fill="#15110d", op=1.0, dur=.5, r=0):
    """A veil (op < 1) or a clean sheet (op 1) laid over part of a panel: what was there fades back."""
    e = rect(x, y, w, h, fill, "none", 0, r, at, op=op)
    e["dur"] = dur
    return e


def hspans(P, y):
    """Where the horizontal line at height y crosses the closed polygon P: the inside intervals [(x0, x1), ...]."""
    xs = []
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


def vtop(P, x):
    """The highest point of polygon P above x (0 if none)."""
    ys = []
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (x1 <= x < x2) or (x2 <= x < x1):
            ys.append(y1 + (x - x1) * (y2 - y1) / (x2 - x1))
    return max(ys) if ys else 0.0


def hband(P, y0, y1, dy=.08, widest=True):
    """The part of polygon P between heights y0 and y1 (y up), as one polygon (the widest span at each height)."""
    L, Rr = [], []
    n = max(2, int(abs(y1 - y0) / dy) + 1)
    for k in range(n + 1):
        y = y0 + (y1 - y0) * k / n
        y = min(max(y, min(y0, y1) + 1e-6), max(y0, y1) - 1e-6)
        sp = hspans(P, y)
        if not sp:
            continue
        a, b = max(sp, key=lambda s: s[1] - s[0]) if widest else (sp[0][0], sp[-1][1])
        L.append((a, y)); Rr.append((b, y))
    return L + Rr[::-1]


# ================================================================== the Sphinx (profile, head to the left = east), in metres
# x: 0 at the tip of the forepaws to 73 at the rump; y: height above the floor of the pit (about 20 m at the top of the head).
# After Lehner 1992 (73 m, the head a block about 20 x 20 cubits, the body about one head-length long) and iso3d.SPHINX_PROF.
BODY = [(0, 0), (0.08, .9), (.35, 1.7), (.9, 2.2), (1.8, 2.42), (6.0, 2.5), (10.2, 2.55), (11.7, 2.9), (12.7, 3.8), (13.3, 5.0), (13.7, 6.8),
        (13.85, 8.6), (13.6, 10.2), (13.0, 11.2), (12.4, 11.7), (14.5, 12.8), (18, 12.9), (22.1, 13.3), (24.5, 13.25), (28, 12.9), (33, 12.4),
        (39, 11.8), (45, 11.15), (51, 10.5), (56, 9.95), (60, 9.7), (63.5, 9.5), (66.5, 9.0), (69.3, 8.0), (71.4, 6.3), (72.6, 4.0), (73, 1.8), (73, 0)]
NEMES = [(12.6, 19.2), (13.4, 19.95), (15.5, 20.15), (18.4, 20.1), (19.9, 19.5), (20.7, 18.4), (21.2, 16.6), (21.6, 14.6), (22.1, 13.3), (21.2, 12.4),
         (19.6, 11.0), (17.6, 10.0), (15.8, 9.6), (14.8, 9.8), (14.4, 11.2), (14.3, 13.2), (14.5, 15.0), (14.4, 16.6), (13.6, 17.9)]
FACE = [(12.6, 19.2), (12.0, 18.9), (11.45, 18.2), (11.2, 17.5), (11.05, 16.95), (11.25, 16.6), (11.0, 16.4), (10.85, 15.9), (10.75, 15.3), (10.8, 14.9),
        (11.0, 14.7), (10.9, 14.3), (10.75, 13.9), (10.95, 13.6), (10.85, 13.2), (11.0, 12.8), (11.1, 12.3), (11.5, 11.8), (12.2, 11.6), (13.3, 12.3),
        (14.3, 13.2), (14.5, 15.0), (14.4, 16.6), (13.6, 17.9)]
EAR = [(13.45, 16.7), (13.85, 16.95), (14.2, 16.6), (14.25, 15.3), (13.95, 14.7), (13.6, 15.0), (13.55, 15.9)]
HAUNCH = [(56.6, 0), (57.0, 3.2), (59.2, 6.2), (62.6, 7.9), (66.4, 8.3), (69.4, 7.3), (71.3, 5.3), (72.2, 2.6), (72.5, 0)]
HINDPAW = [(49.0, 0), (49.1, .9), (49.8, 1.35), (54.8, 1.45), (55.9, 1.0), (56.3, 0)]
BEDS = [(2.0, 3.2, "soft"), (3.2, 4.6, "hard"), (4.6, 5.6, "soft"), (5.6, 7.0, "hard"), (7.0, 8.0, "soft"), (8.0, 9.4, "hard"), (9.4, 10.4, "soft")]
M3 = 10.4                                                    # Member III above this height (neck and head)


def m1_top(x):
    """Member I, the old reef: about 0.7 m high at the paws, rising to about 3.7 m at the rump (AERA: 2 to 3 ft and 12 ft)."""
    return .7 + 3.0 * max(0.0, min(1.0, x / 73.0))


def sphinx(x0, gy, s, at=-1, beds=True, casing=True, light=1.0, yellow=None, op=None, outline=None, shadow=True):
    """The Great Sphinx in profile, head to the left: x0 = the tip of the forepaws, gy = the floor of the pit, s = units a metre.
    Body in the plateau's beds (Member I reef at the foot, Member II soft and hard bands, Member III for the neck and head),
    the striped nemes, the worn face without its nose, the ear, the eye; the restorers' casing blocks along the foot.
    yellow = a time: the yellow band at chest and shoulder height glows in then."""
    X = lambda x: x0 + x * s
    Y = lambda y: gy - y * s
    M = lambda pts: [(X(x), Y(y)) for x, y in pts]
    kw = {} if op is None else {"op": op}
    w1 = max(1.0, s * .07)
    out = []
    if shadow:
        out.append(poly(M([(-1, -.2), (74, -.2), (74, .5), (-1, .5)]), "rgba(0,0,0,.35)", "none", 0, at))
    out.append(poly(M(BODY), "url(#k-stoneC)", "none", 0, at, **kw))
    if beds:
        for y0, y1, kind in BEDS:
            b = hband(BODY, y0, y1)
            if kind == "soft":
                out.append(poly(M(b), "#6b553e", "none", 0, at, op=round(.36 * light, 2)))
                sp = hspans(BODY, y1 - .02)
                if sp:
                    a, c = max(sp, key=lambda q: q[1] - q[0])
                    out.append(ln([(X(a), Y(y1)), (X(c), Y(y1))], at, "#3a2c1e", max(1.0, s * .07), draw=False, op=.5))
            else:
                out.append(poly(M(b), "#f2dfbb", "none", 0, at, op=round(.18 * light, 2)))
        out.append(poly(M(hband(BODY, M3, 13.4)), "#f4e3c2", "none", 0, at, op=round(.22 * light, 2)))
    if yellow is not None:
        out.append(poly(M(hband(BODY, 8.0, 9.4)), YEL, "none", 0, yellow, op=.7, fx="fade"))
    # Member I: the knobbly reef at the foot
    reef = [(0, 0)] + [(x, min(m1_top(x) + .25 * math.sin(x * 1.7) + .15 * math.sin(x * 4.1), vtop(BODY, x) - .05)) for x in [.1 + k * .5 for k in range(146)]] + [(73, 0)]
    out.append(poly(M(reef), "#6a5440", "none", 0, at, op=.7))
    out.append(poly(M(HAUNCH), "rgba(70,52,36,.22)", "none", 0, at))
    out.append(ln(M(HAUNCH[:5]), at, "rgba(40,28,18,.45)", w1, draw=False, curve=True))
    out.append(poly(M(HINDPAW), "#cdb287", "rgba(40,28,18,.5)", w1, at, curve=True))
    # forepaw: toes and the elbow; the shoulder
    for tx in (.55, 1.05, 1.55):
        out.append(ln(M([(tx, .25), (tx + .05, 1.6)]), at, "rgba(40,28,18,.55)", max(1, s * .06), draw=False))
    out.append(ln(M([(12.6, 3.6), (11.6, 2.75), (10.2, 2.55)]), at, "rgba(40,28,18,.45)", w1, draw=False, curve=True))
    out.append(ln(M([(22, 12.4), (19.5, 9.4), (16.2, 6.0), (13.6, 3.6)]), at, "rgba(40,28,18,.22)", max(1, s * .08), draw=False, curve=True))
    if casing:
        cas = [(1.5, 0), (1.5, 1.8), (10.5, 2.0), (11.6, 2.5), (12.4, 3.0), (13.0, 2.0), (47, 2.4), (47, 0)]
        out.append(poly(M(cas), "url(#k-blocks)", "none", 0, at, op=.32))
    # the head: nemes (striped), face, ear, eye
    out.append(poly(M(NEMES), "#dcc497", "none", 0, at))
    k, y = 0, 10.0
    while y < 20.0:
        if k % 2 == 0:
            st = hband(NEMES, y, y + .55, widest=True)
            if len(st) > 2:
                out.append(poly(M(st), "#7a5f43", "none", 0, at, op=.55))
        y += .55; k += 1
    out.append(poly(M(FACE), "#ead4aa", "none", 0, at))
    out.append(poly(M(FACE[:11]), "none", "rgba(255,240,214,.75)", max(1, s * .06), at))   # the lit brow and the broken nose
    out.append(poly(M([(10.85, 15.95), (10.75, 15.3), (10.8, 14.9), (10.95, 15.0), (10.98, 15.8)]), "#a9895f", "none", 0, at, op=.85))
    out.append(poly(M(EAR), "#c9ad80", "rgba(60,44,30,.6)", max(1, s * .05), at))
    out.append(poly(M([(11.5, 16.45), (11.9, 16.62), (12.3, 16.42), (11.9, 16.32)]), "#3a2c1e", "none", 0, at))
    out.append(ln(M([(12.3, 16.45), (12.9, 16.55)]), at, "#3a2c1e", max(1, s * .06), draw=False))
    out.append(ln(M([(11.3, 17.1), (12.4, 17.2)]), at, "rgba(58,44,30,.7)", max(1, s * .06), draw=False))
    out.append(ln(M([(11.0, 13.75), (11.5, 13.65)]), at, "rgba(58,44,30,.7)", max(1, s * .05), draw=False))
    out.append(ln(M([(12.0, 18.9), (12.6, 19.25), (13.4, 19.95)]), at, "#f4e3c2", max(1.2, s * .1), draw=False))
    out.append(ln(M([(12.6, 19.2), (13.6, 17.9), (14.4, 16.6), (14.5, 15.0), (14.3, 13.2), (14.4, 11.2), (14.8, 9.8)]), at, "rgba(58,44,30,.6)", max(1.2, s * .08), draw=False))
    # outline in warm light
    out.append(poly(M(BODY), "none", outline or "rgba(255,236,206,.6)", max(1.2, s * .08), at))
    out.append(poly(M(NEMES), "none", outline or "rgba(255,236,206,.55)", max(1.2, s * .08), at))
    return out


def dimline(x0, x1, y, at, t, c=GOLD, size=28, ty=None):
    """A dimension line that draws itself, end ticks, its label after it."""
    return [ln([(x0, y), (x1, y)], at, c, 2, dur=.9), ln([(x0, y - 10), (x0, y + 10)], at, c, 2, draw=False), ln([(x1, y - 10), (x1, y + 10)], at + .8, c, 2, draw=False),
            lab((x0 + x1) / 2, ty if ty is not None else y + 36, t, at + .7, c, size)]


def sph_pts(x0, gy, s):
    """Where to point at parts of the Sphinx drawn by sphinx(x0, gy, s)."""
    X = lambda x: round(x0 + x * s, 1)
    Y = lambda y: round(gy - y * s, 1)
    return {"face": (X(11.0), Y(15.5)), "head_top": (X(16), Y(20.1)), "chest": (X(13.6), Y(7.5)), "shoulder": (X(24), Y(12.6)),
            "paws": (X(5), Y(1.3)), "rump": (X(72), Y(5)), "back": (X(40), Y(11.9)), "body": (X(38), Y(6)), "X": X, "Y": Y}


def jet(x0, yb, s, at, c="rgba(225,238,250,.95)", style="inferred"):
    """A Boeing 747 in side view (about 70.6 m long, the fin about 19.4 m high), nose to the left, as a dotted outline."""
    P = [(0, 3.0), (.6, 4.6), (2.5, 6.2), (6, 7.6), (10, 8.3), (20, 8.4), (26, 7.0), (30, 6.4), (56, 6.4), (66, 19.4), (69.5, 19.4), (70.6, 6.0), (70.6, 5.0),
         (69, 3.6), (58, .8), (50, 0), (8, 0), (3, .5), (1, 1.6)]
    M = lambda pts: [(x0 + x * s, yb - y * s) for x, y in pts]
    out = [poly(M(P), "rgba(220,232,245,.10)", c, 2.6, at, style=style, fx="draw", dur=1.2)]
    out.append(poly(M([(24, 2.6), (42, 3.6), (42.6, 3.1), (25, 2.2)]), "none", c, 2, at + .5, style=style))
    for ex in (25.5, 33.0):
        out.append(poly(M([(ex - 2.6, 1.2), (ex + 2.6, 1.4), (ex + 2.4, .3), (ex - 2.4, .2)]), "none", c, 2, at + .6, style=style))
    out.append(poly(M([(58, 5.2), (66, 5.6), (66.4, 4.9), (58.6, 4.6)]), "none", c, 2, at + .7, style=style))
    return out


HX0, HGY, HS = 300, 690, 15.75            # the hero: paws at x 300, pit floor at y 690, 15.75 units a metre (73 m = 1150 units)


def pit_scene(tod="dawn", x0=HX0, gy=HGY, s=HS, wall_top=11.0, sun=None, pyr=True, beds=True, stars=False, at=-1):
    """The Sphinx in its pit, seen from the north: the far (south) wall of the pit behind it in the same beds, the plateau above,
    Khafre's pyramid behind; the floor of the pit in front. Returns (elements, base fields)."""
    top = gy - wall_top * s
    els = []
    if pyr:
        els.append({"k": "pyramid", "x": 1210, "y": round(top + 14, 1), "w": 600, "cap": .1, "light": "left", "in": at})
    # the far wall of the pit, with the same beds as the lion (they run straight through)
    wall = [(-60, gy + 2)] + [(x, top + 4 * math.sin(x / 37.0) + 3 * math.sin(x / 13.0)) for x in range(-60, 1861, 20)] + [(1860, gy + 2)]
    els.append(poly(wall, "#4e4034", "none", 0, at))
    if beds:
        for y0, y1, kind in BEDS:
            if kind == "soft":
                els.append(rect(-60, gy - y1 * s, 1920, (y1 - y0) * s, "#2c231b", at=at, op=.5))
                els.append(ln([(-60, gy - y1 * s), (1860, gy - y1 * s)], at, "#1e1712", 1.6, draw=False, op=.6))
        els.append(rect(-60, gy - 3.0 * s, 1920, 3.0 * s, "#2a211a", at=at, op=.55))
    els.append(ln([(x, y) for x, y in wall[1:-1]], at, "rgba(255,226,190,.55)", 2, draw=False))
    # the floor of the pit
    els.append(poly([(-60, gy), (1860, gy), (1860, 1100), (-60, 1100)], "url(#k-sand)", "none", 0, at))
    els.append(ln([(-60, gy), (1860, gy)], at, "rgba(255,226,190,.4)", 1.5, draw=False))
    base = {"base": "sky", "tod": tod, "ground": round(top + 6), "sun": sun if sun is not None else False,
            "ridges": [{"y": round(top - 40), "a": 30, "c": "#3b3140", "seed": 3}, {"y": round(top - 6), "a": 14, "c": "#2a2229", "seed": 9}]}
    return els, base


# ================================================================== COLD OPEN
def s1():
    """The hero image, complete from the first frame: the Sphinx in its pit at dawn, Khafre's pyramid behind, a person at the paws;
    a 747 drawn over it for length (73 m); then the beds of the pit wall run straight through the lion: carved out of the hill."""
    els, base = pit_scene("dawn", sun=[150, 452, 30])
    els += [gl(560, 470, 380, -1, .22, "lamp")]
    els += sphinx(HX0, HGY, HS, -1)
    els += [person(262, HGY, 27, -1, "#2a2018") | {"in": -1}]
    tj, tk, th = T("s1", "jumbo jet"), T("s1", "face of a king"), T("s1", "carved out")
    els += jet(HX0 + 2, HGY - 1.2 * HS, HS, tj)
    els += dimline(HX0, HX0 + 73 * HS, HGY + 40, tj + .6, "73 m") + [lab(1430, 380, "jumbo jet", tj + 1.0, "#dce8f5", 28, "start")]
    P = sph_pts(HX0, HGY, HS)
    els += [gl(P["face"][0] - 10, P["face"][1], 120, tk, .45, "lamp")]
    for k, (y0, y1, kind) in enumerate([b for b in BEDS if b[2] == "soft"]):
        y = HGY - y1 * HS
        els.append(ln([(80, y), (1700, y)], th + .15 * k, "rgba(242,201,142,.95)", 2.4, dur=1.4, op=.7))
    els += [lab(1560, HGY - 6.5 * HS, "the same beds", th + 1.2, GOLD, 26, "middle")]
    base.update(cam=CAM, els=els)
    return base



def sleeper(x, y, L, at, c="#2a2018", rim="rgba(220,226,255,.55)"):
    """A figure asleep on the ground, lying on its side, head to the left: L = its length, feet to the right."""
    h = L * .16
    out = [poly([(x + L * .12, y), (x + L * .14, y - h * .95), (x + L * .45, y - h * 1.15), (x + L * .7, y - h * .9), (x + L, y - h * .45), (x + L, y)], c, rim, 1.2, at, curve=True),
           circ(x + L * .07, y - h * .75, h * .62, c, rim, 1.2, at)]
    return out


def crown(x, y, s, at, op=1.0):
    """The double crown of Egypt (red crown round a white one), standing on y, s = its height."""
    W = [(x - .2 * s, y - .3 * s), (x - .19 * s, y - .6 * s), (x - .13 * s, y - .82 * s), (x - .08 * s, y - .9 * s), (x - .09 * s, y - .95 * s), (x - .03 * s, y - 1.02 * s),
         (x + .03 * s, y - .97 * s), (x + .02 * s, y - .9 * s), (x + .08 * s, y - .8 * s), (x + .13 * s, y - .58 * s), (x + .14 * s, y - .3 * s)]
    Rr = [(x - .38 * s, y), (x - .36 * s, y - .42 * s), (x - .16 * s, y - .44 * s), (x - .14 * s, y - .3 * s), (x + .2 * s, y - .3 * s), (x + .22 * s, y - .86 * s),
          (x + .34 * s, y - .86 * s), (x + .36 * s, y)]
    return [poly(W, "#f4efe2", "rgba(255,246,220,.9)", 1.5, at, fx="pop", op=op, curve=True),
            poly(Rr, "#b5423a", "#ffd9b0", 1.5, at + .05, fx="pop", op=op),
            ln([(x - .3 * s, y - .44 * s), (x - .46 * s, y - .62 * s), (x - .38 * s, y - .74 * s), (x - .28 * s, y - .66 * s)], at + .1, "#ffd9b0", 2.2, dur=.4, curve=True)]


def s2():
    """Night: the Sphinx buried to its neck in drifted sand under the moon (only the head stands clear), a prince asleep on the sand
    in its shadow; the dream (a dotted line to the double crown); then a strip: carved about 2500 BCE, the dream about 1400 BCE."""
    x0, gy, sc = 354, 859, 26.0
    X = lambda m: x0 + m * sc
    Y = lambda m: gy - m * sc
    els = [gl(1480, 190, 300, -1, .22, "lamp"), gl(560, 470, 420, -1, .16, "lamp")]
    els += sphinx(x0, gy, sc, -1, light=.8, casing=False, shadow=False)
    dune = [(-60, 650), (180, 628), (X(6), 600), (X(10.5), Y(11.6)), (X(13.2), Y(11.9)), (X(16), Y(12.2)), (X(19.5), Y(12.9)), (X(22.5), Y(13.9)), (X(30), Y(14.6)),
            (X(40), Y(14.4)), (1500, 512), (1700, 530), (1860, 548), (1860, 1100), (-60, 1100)]
    els += [poly(dune, "#5d4c3c", "rgba(230,222,255,.4)", 1.8, -1, curve=True)]
    els += [poly([(x, y + 26) for x, y in dune[:-2]] + [(1860, 1100), (-60, 1100)], "#463a2f", "none", 0, -1, curve=True, op=.7)]
    for k in range(5):
        xx = 120 + 330 * k
        els.append(ln([(xx, 700 + 18 * (k % 2)), (xx + 160, 690 + 18 * (k % 2))], -1, "rgba(230,222,255,.12)", 2, draw=False, curve=True))
    els += [poly([(X(-7.5), 642), (X(2.5), 606), (X(9.5), 598), (X(4), 640)], "rgba(8,8,18,.45)", "none", 0, -1, curve=True)]   # the head's moon shadow
    tp, td, ts, tc, to = T("s2", "young prince"), T("s2", "In his dream"), T("s2", "clear away the sand"), T("s2", "a crown"), T("s2", "Even then")
    sx, sy = X(-7.4), 632
    els += [poly(E(sx + 80, sy + 4, 120, 16, 24), "rgba(220,214,240,.16)", "none", 0, -1)]
    els += sleeper(sx, sy, 150, tp - .3, "#cfc3ad", "rgba(60,50,70,.8)")
    els += [gl(sx + 60, sy - 18, 110, tp - .3, .3, "lamp")]
    cx, cy = sx + 30, 300
    els += [ln([(sx + 22, sy - 32), (sx + 2, sy - 100), (sx + 40, sy - 170), (sx + 18, sy - 240), (cx, cy + 8)], td, LILAC, 3, "claimed", 1.0, curve=True)]
    els += [ln([(x, y - 6) for x, y in dune[3:10]], ts, "rgba(201,193,238,.9)", 3, "claimed", 1.2, curve=True)]
    els += [gl(cx, cy - 50, 150, tc, .55, "lamp")] + crown(cx, cy, 120, tc)
    els += [lab(cx + 90, cy - 50, "a crown", tc + .4, LILAC, 30, "start", st="ital")]
    ax0, ax1, ay = 900, 1600, 270
    els += [ln([(ax0, ay), (ax1, ay)], to, BONE, 2.5, dur=.6),
            circ(ax0, ay, 8, AMBER, "none", 0, to + .2, fx="pop"), circ(ax1, ay, 8, LILAC, "none", 0, to + .5, fx="pop"),
            lab(ax0, ay + 40, "carved, about 2500 BCE", to + .3, AMBER, 26, "start"),
            lab(ax1, ay + 40, "the dream, about 1400 BCE", to + .6, LILAC, 26, "end")]
    els += bracket(ax0, ax1, ay - 26, to + 1.0, "about 1,100 years", GOLD, up=False, size=30, ty=ay - 46)
    return {"base": "sky", "tod": "night", "ground": 600, "groundc": "#2a231d", "sun": False, "moon": [1480, 170, 26],
            "ridges": [{"y": 560, "a": 24, "c": "#221d26", "seed": 3}, {"y": 590, "a": 10, "c": "#1b171d", "seed": 9}], "cam": CAM, "els": els}


def s3_add():
    """The question: a lilac dotted arrow sweeps from the Sphinx far to the left into the sky, a '?' on 'pharaohs'."""
    t0, tp = T("s3", "So how old"), T("s3", "pharaohs")
    out = [arr([(540, 400), (420, 330), (260, 290), (120, 280)], t0 + .2, LILAC, 3.5, "claimed", 1.4)]
    for k, x in enumerate((380, 300, 220)):
        out.append(ln([(x, 300 - 4 * k), (x, 318 - 4 * k)], t0 + .8 + .2 * k, "rgba(201,193,238,.7)", 2, draw=False))
    out += qmark(180, 250, tp, 120)
    return out


# ================================================================== CHAPTER 1 · Cut from the living rock
VE = View(28.4, 33.6, 28.9, 31.8, (90, 130, 1600, 660))


def nile_lines(v, at, w=7):
    out = []
    for path in (NILE, ROSETTA, DAMIETTA):
        out.append(ln([v.p(lo, la) for lo, la in path], at, "#6fb6d6", w, draw=False, op=.95, curve=True))
    return out


def s5():
    """Map of northern Egypt: the Nile, its delta, Giza and Cairo; then a shallow sea rises over the map: 50 million years ago."""
    v = VE
    gx, gy_ = v.p(31.134, 29.979); cx, cy = v.p(31.235, 30.044)
    els = [{"k": "map", "land": v.land(), "in": -1}]
    els += [poly([v.p(30.6, 29.7), v.p(31.0, 30.6), v.p(31.6, 30.6), v.p(31.5, 29.6), v.p(31.1, 29.2), v.p(30.7, 29.3)], "rgba(120,170,90,.10)", "none", 0, -1, curve=True)]
    els += nile_lines(v, -1)
    els += [{"k": "pin", "x": gx, "y": gy_, "t": "Giza", "c": GOLD, "in": -1, "a": "end", "lx": -20, "ly": 10},
            {"k": "pin", "x": cx, "y": cy, "t": "Cairo", "c": "#cbbca8", "in": -1, "r": 6, "a": "start", "lx": 18, "ly": -4},
            lab(v.p(29.4, 31.62)[0], v.p(29.4, 31.62)[1], "Mediterranean Sea", -1, "#9fc4d8", 28, st="ital"),
            lab(v.p(31.45, 29.2)[0] + 16, v.p(31.45, 29.2)[1], "Nile", -1, "#9fd0ff", 28, "start", st="ital"),
            {"k": "scale", "x": 1300, "y": 740, "w": round(v.km(50), 1), "t": "50 km", "in": -1}]
    tf = T("s5", "fifty million")
    els += [rect(-60, -20, 1900, 1060, "rgba(63,134,168,.5)", at=tf, fx="fill", dur=2.2)]
    for k in range(6):
        y = 250 + 90 * k
        els.append(ln([(140 + 240 * ((k + j) % 6), y + 8 * math.sin(j)) for j in range(0)] or [(200 + 260 * (k % 3), y), (260 + 260 * (k % 3), y - 8), (320 + 260 * (k % 3), y)],
                      round(tf + 1.6 + .1 * k, 2), "rgba(220,240,255,.45)", 2, dur=.5, curve=True))
    els += [rect(520, 600, 760, 64, "rgba(14,24,32,.75)", "none", 0, 32, tf + 1.8, op=1),
            lab(900, 643, "a shallow sea, about 50 million years ago", tf + 1.9, "#cfe6ff", 30)]
    return {"base": "map", "cam": CAM, "els": els}


def nummulite(x, y, r, at, edge=False, ang=0.0, fx="pop"):
    """A nummulite: a coin-shaped fossil shell, seen face on (a disc with its spiral) or edge on (a lens)."""
    if edge:
        a = math.radians(ang)
        pts = [(x + r * math.cos(a) * math.cos(t) - r * .28 * math.sin(a) * math.sin(t), y + r * math.sin(a) * math.cos(t) + r * .28 * math.cos(a) * math.sin(t))
               for t in [k * math.pi / 12 for k in range(24)]]
        return [poly(pts, "#efe2c4", "#7d6448", 1.4, at, fx=fx), ln([(x - r * .8 * math.cos(a), y - r * .8 * math.sin(a)), (x + r * .8 * math.cos(a), y + r * .8 * math.sin(a))],
                                                                     at, "#8c7152", 1, draw=False)]
    sp = [(x + r * .85 * (k / 30) * math.cos(k * .62 + ang), y + r * .85 * (k / 30) * math.sin(k * .62 + ang)) for k in range(31)]
    return [circ(x, y, r, "#efe2c4", "#7d6448", 1.4, at, fx=fx), ln(sp, at, "#8c7152", 1.1, draw=False, curve=True)]


def s6():
    """A limestone face packed with coin-shaped fossil shells (some broken open on their spiral), a coin for size; then Strabo's
    bowl of lentils, dotted to the shells: the builders' lentils?"""
    els = [rect(110, 130, 1560, 640, "#c7ab7f", "rgba(255,236,206,.35)", 1.5, 16, -1), rect(110, 130, 1560, 640, "url(#k-speck)", at=-1, r=16),
           gl(500, 300, 700, -1, .18, "lamp")]
    rnd = random.Random(11)
    pts = []
    while len(pts) < 46:
        x, y = rnd.uniform(160, 1080), rnd.uniform(180, 730)
        if all(math.hypot(x - a, y - b) > 62 for a, b in pts):
            pts.append((x, y))
    for k, (x, y) in enumerate(pts):
        edge = k % 3 == 1
        els += nummulite(x, y, rnd.uniform(18, 30), -1 if k < 30 else round(.4 + .05 * (k - 30), 2), edge, rnd.uniform(0, 3.1))
    tc, ts, ti = T("s6", "little coins"), T("s6", "Strabo"), T("s6", "not improbable")
    cx, cy = 1000, 540
    els += [circ(cx, cy, 30, "#c9a46a", "#fff0c8", 2.5, tc, fx="pop"), circ(cx, cy, 22, "none", "rgba(110,80,40,.6)", 1.5, tc + .05, fx="pop"),
            lab(cx, cy + 66, "a coin, for size", tc + .3, BONE, 24), lab(600, 112 + 52, "fossil shells", tc + .4, BONE, 30)]
    bx, by = 1390, 470
    els += [gl(bx, by - 30, 200, ts, .35, "lamp"),
            poly([(bx - 120, by - 40), (bx + 120, by - 40), (bx + 96, by + 30), (bx + 50, by + 56), (bx - 50, by + 56), (bx - 96, by + 30)], "#7a4e2c", "#e3b07a", 2, ts, fx="pop", curve=True)]
    for k in range(28):
        lx, ly = bx - 95 + (k % 10) * 21 + (k // 10) * 9, by - 50 - (k // 10) * 12 + (k % 3) * 3
        els.append(poly(E(lx, ly, 10, 5, 12), "#c9783a", "#f2b47a", 1, round(ts + .2 + .02 * k, 2), fx="pop"))
    els += [ln([(bx - 130, by - 20), (1180, 440), (1090, 400)], ts + .8, LILAC, 3, "claimed", .8, curve=True),
            lab(bx, by + 110, "the builders' lentils?", ts + .6, LILAC, 30, st="ital"),
            lab(bx, by + 150, "Strabo, about 2,000 years ago", ts + .9, DIM, 24),
            lab(bx, by - 120, "not improbable", ti, LILAC, 26, st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


def cake(cx, by, w, h, at, gap=False, fx="pop"):
    """A three-layer cake seen from the side and a little above: a dark base, a striped middle, a pale top."""
    x0, x1 = cx - w / 2, cx + w / 2
    hs = [h * .3, h * .45, h * .25]
    cols = ["#6f5a44", "#c8a978", "#efe2c4"]
    out, y = [], by
    for k in range(3):
        out.append(rect(x0, y - hs[k], w, hs[k], cols[k], "rgba(40,28,18,.6)", 1.2, 0, at + .08 * k, fx=fx))
        if k == 1:
            for j in range(1, 4):
                out.append(ln([(x0, y - hs[k] * j / 4), (x1, y - hs[k] * j / 4)], at + .1, "#7a5f43", 2, draw=False, op=.8))
        y -= hs[k]
    out.append(poly(E(cx, y, w / 2, w * .1, 24), "#f6eedb", "rgba(40,28,18,.5)", 1.2, at + .25, fx=fx))
    if gap:
        out.append(poly([(cx, by), (cx + w * .2, by), (cx + w * .2, y), (cx, y)], "#15110d", "none", 0, at + .3, fx=fx))
    return out


SEC = dict(x0=170, x1=1150, top=250, bot=730)


def layer_block(x0, x1, top, bot, at=-1, op=1.0, knob=True):
    """A block of the plateau's bedrock in section: Member I (the reef, knobbly) at the foot, Member II in soft and hard bands,
    Member III on top. Heights in the proportions of the Sphinx's beds (bot = the floor, top = 21 m above it)."""
    s = (bot - top) / 21.0
    Y = lambda m: bot - m * s
    out = [rect(x0, top, x1 - x0, bot - top, "#b89a70", at=at, op=op)]
    for y0, y1, kind in BEDS:
        if kind == "soft":
            out.append(rect(x0, Y(y1), x1 - x0, (y1 - y0) * s, "#8c7152", at=at, op=op))
            out.append(ln([(x0, Y(y1)), (x1, Y(y1))], at, "#5a4632", 1.4, draw=False, op=op))
        else:
            out.append(rect(x0, Y(y1), x1 - x0, (y1 - y0) * s, "#cdb184", at=at, op=op))
    out.append(rect(x0, top, x1 - x0, Y(M3) - top, "#e2cda4", at=at, op=op))
    reef = [(x0, bot)] + [(x, Y(2.0 + .35 * math.sin(x / 23.0) + .25 * math.sin(x / 9.0))) for x in range(int(x0), int(x1) + 1, 12)] + [(x1, bot)]
    out.append(poly(reef, "#6a5440", "none", 0, at, op=op))
    out.append(rect(x0, top, x1 - x0, bot - top, "url(#k-speck)", at=at, op=op))
    return out, Y


def s7():
    """The plateau's bedrock in section, three units lighting up from the bottom as named (old reef, soft and hard bands, better
    stone); a small layer cake beside it."""
    x0, x1, top, bot = 170, 1120, 230, 730
    H = bot - top
    yr, yb = bot - H * .24, bot - H * .64                         # tops of the reef and of the bands (schematic proportions)
    els = [rect(x0 - 6, top - 6, x1 - x0 + 12, H + 12, "#120e0b", "rgba(255,236,206,.3)", 1.5, 8, -1)]
    reef_top = [(x, yr + 10 * math.sin(x / 31.0) + 6 * math.sin(x / 11.0)) for x in range(x0, x1 + 1, 10)]
    reef = [(x0, bot)] + reef_top + [(x1, bot)]
    bands = []
    n = 7
    for k in range(n):
        ya, yb_ = yr - (yr - yb) * k / n, yr - (yr - yb) * (k + 1) / n
        bands.append((ya, yb_, k % 2 == 0))
    # dim, from the first second
    els += [rect(x0, top, x1 - x0, H, "#2c241d", at=-1)]
    els += [rect(x0, b, x1 - x0, a - b, "#3a3027" if soft else "#4a3e32", at=-1) for a, b, soft in bands] + [poly(reef, "#4a3c2e", "none", 0, -1)]
    els += [rect(x0, top, x1 - x0, yb - top, "#55493c", at=-1)]
    tk, tr, tb, tt = T("s7", "like a cake"), T("s7", "old reef"), T("s7", "soft and hard"), T("s7", "harder, better")
    for k, (a, b, soft) in enumerate(bands):
        if k == 0:
            a = bot - 4
        els.append(rect(x0, b, x1 - x0, a - b, "#8c7152" if soft else "#d6bb8c", at=round(tb - .2 + .12 * k, 2)))
        if soft:
            els.append(ln([(x0, b), (x1, b)], round(tb - .2 + .12 * k, 2), "#5a4632", 1.4, draw=False))
    els += [poly(reef, "#7a6248", "#e8cfa6", 1.5, tr - .2), poly(reef, "url(#k-speck)", "none", 0, tr)]
    els += [rect(x0, top, x1 - x0, yb - top, "#ead7b0", at=tt - .2), rect(x0, top, x1 - x0, H, "url(#k-speck)", at=tt)]
    els += [lab(x1 + 30, (yr + bot) / 2 + 10, "old reef", tr + .2, BONE, 30, "start"), lab(x1 + 30, (yr + yb) / 2 + 10, "soft and hard bands", tb + .3, BONE, 30, "start"),
            lab(x1 + 30, (yb + top) / 2 + 10, "better stone", tt + .2, BONE, 30, "start")]
    els += cake(1560, 720, 190, 150, tk) + [lab(1560, 770, "like a cake", tk + .4, DIM, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def plan_sphinx(cx, cy, k, at, c="#d6bd92", op=None, face=1):
    """The Sphinx seen from above, head to the east (face=1: to the right): body, haunches, forepaws, the head and its nemes. k = units a metre."""
    f = face
    P = lambda e, n: (cx + f * e * k, cy - n * k)
    body = [P(-36.5, 0), P(-35.8, 5.5), P(-31, 8.8), P(-22, 9.2), P(-6, 8.6), P(8, 8.2), P(16, 9.4), P(22, 9.0), P(22, -9.0), P(16, -9.4), P(8, -8.2), P(-6, -8.6),
            P(-22, -9.2), P(-31, -8.8), P(-35.8, -5.5)]
    paws = [[P(22, 8.6), P(36.5, 8.4), P(36.5, 3.6), P(22, 3.8)], [P(22, -3.8), P(36.5, -3.6), P(36.5, -8.4), P(22, -8.6)]]
    head = [P(13.5, 5.6), P(24, 4.4), P(26.2, 2.4), P(26.2, -2.4), P(24, -4.4), P(13.5, -5.6)]
    kw = {} if op is None else {"op": op}
    out = [poly(body, c, "rgba(255,236,206,.55)", 1.5, at, curve=True, **kw)]
    out += [poly(p, c, "rgba(255,236,206,.55)", 1.5, at, **kw) for p in paws]
    out += [poly(head, "#e6d1a8", "rgba(60,44,30,.6)", 1.5, at, **kw)]
    for j in range(5):
        e = 15 + j * 2
        out.append(ln([P(e, 5.0 - .25 * j), P(e, -5.0 + .25 * j)], at, "#7a5f43", 2, draw=False, op=.6))
    return out


def s8():
    """Top left, from above: a U-shaped trench (open to the east) cut round a block of bedrock. Below, from the side and large: the
    layered block; the lion's outline is planned on it, the waste rock darkens to the far wall of the trench, and the Sphinx is left
    standing in the beds: head, body, floor."""
    tu, tl, tf, tb_, th = T("s8", "shape of a U"), T("s8", "shaped what"), T("s8", "for the floor"), T("s8", "for the body"), T("s8", "for the head")
    px, py, k = 330, 265, 2.9
    els = [rect(110, 150, 450, 230, "#a88a64", "rgba(255,236,206,.3)", 1.5, 10, -1), rect(110, 150, 450, 230, "url(#k-speck)", at=-1, r=10),
           lab(580, 190, "seen from above", -1, DIM, 24, "start")]
    U = [(px - 46 * k, py - 33 * k), (px + 50 * k, py - 33 * k), (px + 50 * k, py + 33 * k), (px - 46 * k, py + 33 * k), (px - 46 * k, py + 20 * k),
         (px + 38 * k, py + 20 * k), (px + 38 * k, py - 20 * k), (px - 46 * k, py - 20 * k)]
    els += [poly(U, "#1d1712", "rgba(255,236,206,.45)", 1.5, tu - .3, fx="fade")]
    els += [lab(660, 262, "a U-shaped trench", tu + .3, GOLD, 30, "start")]
    els += plan_sphinx(px - 4 * k, py, k, tl + .6, face=-1)
    x0, x1, gy, sc = 200, 1620, 760, 16.4
    top = gy - 21 * sc
    blk, Y = layer_block(x0, x1, top, gy, -1)
    els += blk
    lx0 = x0 + 120
    P = sph_pts(lx0, gy, sc)
    els += [poly([(P["X"](x), P["Y"](y)) for x, y in BODY], "none", GOLD, 3, tu, style="inferred"),
            poly([(P["X"](x), P["Y"](y)) for x, y in NEMES], "none", GOLD, 3, tu + .2, style="inferred")]
    els += [rect(x0, top, x1 - x0, gy - top, "#120e0b", at=tl, op=.62)]
    els += sphinx(lx0, gy, sc, tl + .3, casing=False, shadow=False)
    els += [lab(P["X"](40), gy - .6 * sc + 8, "floor: the reef", tf + .2, GOLD, 28),
            ln([(P["X"](52), P["Y"](10.6)), (P["X"](60), P["Y"](17))], tb_, GOLD, 2, dur=.3), lab(P["X"](60) + 10, P["Y"](17) - 6, "body: the bands", tb_ + .2, GOLD, 28, "start"),
            ln([(P["X"](22.5), P["Y"](18)), (P["X"](30), P["Y"](19.6))], th, GOLD, 2, dur=.3), lab(P["X"](30) + 10, P["Y"](19.6) + 4, "head: the better stone", th + .2, GOLD, 28, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def sledge(x, y, w, at, people=3, face=-1):
    """A wooden sledge with a block on it, hauled by a small team (to the left)."""
    out = [rect(x - w / 2, y - 8, w, 8, "#6b4a30", "#a07850", 1, 2, at, fx="pop")]
    for j in range(people):
        px = x + face * (w / 2 + 34 + 30 * j)
        out.append(person(round(px, 1), y, 46, round(at + .1 + .05 * j, 2), "#2a2018"))
        out.append(ln([(x + face * w / 2, y - 14), (px - face * 6, y - 22)], at + .1, "#c9ad85", 1.2, draw=False))
    return out


def s9():
    """Dawn, side view: the Sphinx in its trench; big blocks come up out of the trench and go east (left) on sledges, stacking into the
    walls of a temple in front of the paws, on a terrace a little lower; 'up to 100 tonnes' on the biggest."""
    x0, gy, sc = 860, 600, 11.0
    els, base = pit_scene("dawn", x0=x0, gy=gy, s=sc, wall_top=11.0, sun=[150, 420, 26], pyr=False)
    tg = round(gy + 2.5 * sc)
    els += [rect(-60, gy - 2, 1920, 1100, "#86694d", at=-1), rect(-60, gy - 2, x0 - 40 + 60, tg - gy + 2, "#2a211a", at=-1),
            rect(-60, gy + 120, 1920, 1000, "url(#k-fadeup)", at=-1, op=.8),
            ln([(-60, tg), (x0 - 40, tg), (x0 - 40, gy), (1860, gy)], -1, "rgba(255,226,190,.5)", 1.6, draw=False)]
    els += sphinx(x0, gy, sc, -1)
    tw, tt, tb = T("s9", "didn't go to"), T("s9", "hundred tonnes"), T("s9", "build a")
    tx0, tx1 = 150, 560
    els += [rect(tx0, tg - 150, tx1 - tx0, 150, "none", "rgba(255,236,206,.45)", 2, 2, -1, style="inferred"), lab((tx0 + tx1) / 2, tg - 170, "a temple", tb + 1.2, BONE, 30)]
    for k in range(3):
        bx = 1140 + 150 * k
        at = round(tw + .35 * k, 2)
        els += [rect(bx, gy - 12.4 * sc - 44, 96, 44, "#d6bb8c", "rgba(40,28,18,.7)", 1.4, 2, at, fx="rise"),
                arr([(bx + 20, gy - 12.4 * sc - 50), (bx - 160 - 60 * k, gy - 17 * sc), (800 - 40 * k, tg - 90)], at + .3, AMBER, 2.6, "inferred", 1.0)]
    els += sledge(760, tg, 110, tt - .4, 4)
    els += [rect(685, tg - 56, 110, 48, "#d6bb8c", "rgba(40,28,18,.7)", 1.6, 2, tt - .4, fx="pop"), lab(740, tg - 76, "up to 100 tonnes", tt + .2, GOLD, 28)]
    order = [(c, r) for r in range(3) for c in range(4)]
    for j, (c, r) in enumerate(order):
        els.append(rect(tx0 + 4 + 100 * c, tg - 2 - 48 * (r + 1), 98, 46, "#cdb184" if (c + r) % 2 else "#d9c196", "rgba(40,28,18,.6)", 1.2, 1, round(tb - .3 + .1 * j, 2), fx="pop"))
    base.update(cam=CAM, els=els)
    return base


def fossil_icons(x, y, at, s=1.0, c="#efe2c4"):
    """Four small fossils of the plateau's old sea: an urchin, an oyster, a shark's tooth, a coral branch."""
    out = [circ(x, y, 16 * s, "none", c, 2, at, fx="pop")] + [circ(x + 10 * s * math.cos(a), y + 10 * s * math.sin(a), 2.2 * s, c, at=at + .05, fx="pop") for a in [k * math.pi / 4 for k in range(8)]]
    out += [poly([(x + 46 * s, y + 14 * s), (x + 40 * s, y - 10 * s), (x + 56 * s, y - 18 * s), (x + 72 * s, y - 6 * s), (x + 66 * s, y + 16 * s)], "none", c, 2, at + .1, fx="pop", curve=True)]
    out += [poly([(x + 96 * s, y + 16 * s), (x + 106 * s, y - 18 * s), (x + 116 * s, y + 16 * s)], "none", c, 2, at + .2, fx="pop")]
    out += [ln([(x + 140 * s, y + 18 * s), (x + 140 * s, y - 4 * s), (x + 132 * s, y - 16 * s)], at + .3, c, 2, dur=.3),
            ln([(x + 140 * s, y - 4 * s), (x + 150 * s, y - 18 * s)], at + .35, c, 2, dur=.3)]
    return out


def s10():
    """Aigner's log: a column of the trench's beds with its fossils; 173 temple blocks pop into a grid, each one logged; 'Aigner, 1980'."""
    ty, tn = T("s10", "nineteen eighty"), T("s10", "hundred and seventy-three")
    cx0, cx1, top, bot = 170, 330, 200, 700
    blk, Y = layer_block(cx0, cx1, top, bot, -1)
    els = [rect(cx0 - 6, top - 6, cx1 - cx0 + 12, bot - top + 12, "#120e0b", "rgba(255,236,206,.3)", 1.5, 6, -1)] + blk
    els += [lab((cx0 + cx1) / 2, top - 26, "the trench", -1, DIM, 26)]
    els += fossil_icons(360, 300, .4, .8) + [lab(430, 268, "fossils", .9, BONE, 24)]
    for k, y in enumerate((620, 520, 420, 330)):
        els.append(ln([(cx1 + 6, y), (420, y)], round(.5 + .2 * k, 2), "rgba(242,201,142,.7)", 1.5, draw=False))
    els += chip(1450, 200, "Aigner, 1980", AMBER, ty)
    gx, gy0, px, py, nc = 520, 270, 46, 40, 19
    for k in range(173):
        c, r = k % nc, k // nc
        at = round(tn - .2 + .012 * k, 3)
        els.append(rect(gx + px * c, gy0 + py * r, 38, 28, "#cdb184", "rgba(40,28,18,.6)", 1, 2, at, fx="pop"))
        els.append(ln([(gx + px * c + 4, gy0 + py * r + 16), (gx + px * c + 34, gy0 + py * r + 16)], at + .05, YEL if k % 7 else "#8c7152", 3, draw=False, op=.8))
    els += [lab(gx + px * nc / 2, gy0 + py * 10 + 30, "173 temple blocks, logged", tn + 2.3, GOLD, 32)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def temple_wall(x0, y0, cols, rows, bw, bh, at, band=None, step=.06, fx="pop"):
    """A wall of big limestone blocks (courses on y0 going up); band = (y offset within the wall, height): a yellow bed running through
    adjacent blocks."""
    out = []
    for r in range(rows):
        off = (bw / 2 if r % 2 else 0)
        for c in range(cols):
            x = x0 + c * bw - off
            w = bw
            if x < x0:
                w -= x0 - x; x = x0
            if x + w > x0 + cols * bw:
                w = x0 + cols * bw - x
            if w < 10:
                continue
            out.append(rect(x + 1, y0 - (r + 1) * bh + 1, w - 2, bh - 2, "#cdb184", "rgba(40,28,18,.6)", 1.2, 1, round(at + step * (r * cols + c), 2), fx=fx))
    if band:
        out.append(rect(x0 + 1, y0 - band[0] - band[1], cols * bw - 2, band[1], YEL, at=band[2], op=.75))
    return out


def s11():
    """The Sphinx at left with its yellow band glowing across chest and shoulders; the temple's wall at right with the same band
    running through its blocks; dashed links between; a cake slice slides back into its cake."""
    x0, gy, sc = 120, 700, 10.0
    tb, ts, tc = T("s11", "yellow band"), T("s11", "same band"), T("s11", "layer cake")
    els = [rect(-60, gy, 1900, 400, "#3a2e24", at=-1)]
    els += sphinx(x0, gy, sc, -1, yellow=tb)
    wy = gy - 1.5 * sc
    els += [rect(1000, wy, 660, gy - wy, "#3a2e24", at=-1)]
    els += temple_wall(1020, wy, 6, 4, 104, 58, -1, band=(118, 22, tb + .4))
    els += [lab(1330, wy - 4 * 58 - 22, "the temple's blocks", -1, DIM, 26)]
    for k, (ax, ay) in enumerate([(x0 + 40 * sc, gy - 8.7 * sc), (x0 + 55 * sc, gy - 8.7 * sc)]):
        els.append(ln([(ax, ay), (1020 + 30, wy - 129)], round(ts + .2 * k, 2), GOLD, 2.5, "inferred", .9, curve=True))
    els += [lab(760, gy - 13 * sc, "the same yellow bed", ts + .4, YEL, 30)]
    els += cake(1450, 330, 170, 120, tc - .6, gap=True)
    sl = [(1450, 330), (1450 + 34, 330), (1450 + 34, 210), (1450, 210)]
    els += [poly(sl, "#c8a978", "rgba(40,28,18,.6)", 1.2, tc, fx="rise"), lab(1450, 380, "a slice, back in place", tc + .5, BONE, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s12():
    """The Sphinx in its trench at morning; the rock that was cut away round it (above its back and in front of its face) shows as a
    hatched, dashed volume with an arrow east 'to the temple'; then the lion alone glows: what the quarrymen left standing."""
    x0, gy, sc = 330, 690, 15.0
    els, base = pit_scene("dawn", x0=x0, gy=gy, s=sc, wall_top=14.0, sun=[150, 488, 28], pyr=True)
    els += sphinx(x0, gy, sc, -1)
    tb, ts = T("s12", "isn't a building"), T("s12", "left standing")
    hill = lambda x: 21.0 if 8.5 <= x <= 22.5 else 14.0
    top_of = lambda x: max(vtop(BODY, x), vtop(NEMES, x), vtop(FACE, x))
    xs = [k * .25 for k in range(0, 293)]
    up = [(x, hill(x)) for x in xs]
    lo = [(x, min(hill(x), top_of(x))) for x in xs]
    region = up + lo[::-1]
    M = lambda pts: [(x0 + x * sc, gy - y * sc) for x, y in pts]
    els += [poly(M(region), "rgba(245,236,220,.2)", "none", 0, tb), poly(M(region), "url(#k-hatch)", "none", 0, tb + .1), poly(M(region), "url(#k-hatch)", "none", 0, tb + .2),
            ln(M([(0, top_of(0))] + up + [(73, top_of(73))]), tb, "rgba(245,236,220,.8)", 2.2, "inferred", 1.2)]
    els += [lab(x0 + 45 * sc, gy - 15.2 * sc, "cut away", tb + .6, BONE, 28)]
    els += [arr([(x0 + 4 * sc, gy - 22.5 * sc), (150, gy - 22.5 * sc)], tb + 1.0, AMBER, 3, "known", .8, False), lab(150, gy - 22.5 * sc - 22, "to the temple", tb + 1.2, AMBER, 26, "start")]
    P = sph_pts(x0, gy, sc)
    els += [gl(P["body"][0], P["body"][1] - 40, 560, ts, .32, "lamp"), lab(x0 + 30 * sc, gy + 50, "left standing", ts + .3, GOLD, 30)]
    base.update(cam=CAM, els=els)
    return base


# ================================================================== CHAPTER 2 · Khafre's building site
PK = .68
PX = lambda e: round(889 + (e + 100) * PK, 1)
PY = lambda n: round(457 - (n + 337) * PK, 1)
SPH = GP["sphinx"]                                          # (e, n) of the Sphinx on the plateau (metres east, north of Khufu's centre)


def rel(e, n):
    """A point given relative to the Sphinx (metres east, north), on the plateau plan."""
    return (PX(SPH[0] + e), PY(SPH[1] + n))


ENCL = [(-56, 30), (46, 30), (46, -31), (-56, -19)]                       # the trench round the Sphinx, its south side along the causeway
STEMP = [(52, 25), (100, 25), (100, -24), (52, -24)]                     # the Sphinx Temple
VTEMP = [(52, -31), (104, -31), (104, -84), (52, -84)]                   # Khafre's Valley Temple
CW_N = [(52, -32), (-56, -19), (-640, 52)]                               # the causeway's north edge, from the Valley Temple up towards Khafre


def pyr_sq(e, n, b, at, c="rgba(220,191,148,.55)", edge="#f2dcb4", w=1.8):
    h = b / 2
    sq = [(PX(e - h), PY(n + h)), (PX(e + h), PY(n + h)), (PX(e + h), PY(n - h)), (PX(e - h), PY(n - h))]
    return [poly(sq, c, edge, w, at), ln([sq[0], sq[2]], at, "#8c7152", 1, draw=False, op=.8), ln([sq[1], sq[3]], at, "#8c7152", 1, draw=False, op=.8)]


def s13():
    """The plateau, north up (positions after published plans): Khufu, Khafre (lit, 'about 2500 BCE'), Menkaure; Khafre's pyramid
    temple, then his causeway draws down to the Valley Temple ('almost half a kilometre'); the Sphinx dim beside it."""
    (kx, kn), kb = GP["khafre"]
    els = []
    for key, name in (("khufu", "Khufu"), ("menkaure", "Menkaure")):
        (x, n), b = GP[key]
        els += pyr_sq(x, n, b, -1, "rgba(220,191,148,.35)", "rgba(242,220,180,.6)")
        els.append(lab(PX(x - b / 2) - 14, PY(n) + 9, name, -1, DIM, 26, "end"))
    els += pyr_sq(kx, kn, kb, -1, "rgba(242,201,142,.55)", GOLD, 2.6) + [lab(PX(kx), PY(kn - kb / 2) + 36, "Khafre", -1, GOLD, 30)]
    els += chip(PX(kx), PY(kn + kb / 2) - 34, "about 2500 BCE", AMBER, -1, 24)
    els += [{"k": "line", "p": [[1560, 220], [1560, 160]], "c": "#e9dccb", "w": 2, "in": -1}, lab(1560, 250, "N", -1, "#e9dccb", 24)]
    tt, tc, tv = T("s13", "From its temple"), T("s13", "a causeway"), T("s13", "second temple")
    pt = [(PX(kx + kb / 2 + 8), PY(kn + 40)), (PX(kx + kb / 2 + 60), PY(kn + 40)), (PX(kx + kb / 2 + 60), PY(kn - 40)), (PX(kx + kb / 2 + 8), PY(kn - 40))]
    els += [poly(pt, "rgba(242,201,142,.4)", GOLD, 2, tt, fx="pop")]
    sx, sn = SPH
    cw = [(PX(kx + kb / 2 + 60), PY(kn)), rel(-56, -24), rel(52, -36)]
    els += [ln(cw, tc, "#e2c79c", 5, dur=1.6)]
    els += [poly([rel(*p) for p in VTEMP], "rgba(242,201,142,.45)", GOLD, 2, tv, fx="pop"), lab(rel(78, -84)[0] + 6, rel(78, -84)[1] + 34, "Valley Temple", tv + .2, BONE, 26)]
    els += [lab((cw[0][0] + cw[1][0]) / 2, (cw[0][1] + cw[1][1]) / 2 - 26, "almost half a kilometre", tc + 1.2, "#e2c79c", 28),
            {"k": "scale", "x": 1300, "y": 740, "w": round(100 * PK, 1), "t": "100 m", "in": tc + 1.4}]
    els += [poly([rel(*p) for p in ENCL], "rgba(13,11,9,.6)", "rgba(242,220,180,.5)", 1.5, -1)] + plan_sphinx(rel(0, 0)[0], rel(0, 0)[1], PK, -1)
    els += [poly([rel(*p) for p in STEMP], "rgba(220,191,148,.4)", "rgba(242,220,180,.6)", 1.5, -1)]
    return {"base": "plan", "north": False, "cam": CAM, "els": els}


def s14_add():
    """Closer on the foot of the causeway: the Sphinx in its trench glows beside the Valley Temple; the Sphinx Temple in front of it."""
    t = T("s14", "lies the Sphinx")
    x, y = rel(0, 0)
    return [gl(x, y, 120, t - .3, .6, "lamp"), ring_(x, y, 70, t, GOLD), lab(x - 20, y - 74, "the Sphinx", t + .2, GOLD, 26, "end"),
            lab(rel(104, 0)[0] + 12, rel(104, 0)[1] + 8, "Sphinx Temple", .6, BONE, 24, "start")]


def ring_(x, y, r, at, c=GOLD, w=3, style="known", dur=.8):
    return {"k": "circle", "x": round(x, 1), "y": round(y, 1), "r": round(r, 1), "fill": "none", "c": c, "w": w, "style": style, "in": round(at, 2), "fx": "draw", "dur": dur}


QK = 4.4
QX = lambda e: round(840 + (e - 20) * QK, 1)
QY = lambda n: round(440 - (n + 27) * QK, 1)
Q = lambda e, n: (QX(e), QY(n))


def close_plan(at=-1, labels=True):
    """The trench and its neighbours close up, north up (schematic, after published plans): the Sphinx in its trench, the Sphinx Temple
    in front, the Valley Temple south of it, the causeway running up to the west-north-west along the trench's south side."""
    els = [rect(80, 120, 1620, 680, "#a88a64", at=at, op=.5)]
    cwS = [(52, -40), (-56, -27), (-110, -20)]
    cw = [Q(*p) for p in CW_N[:2]] + [Q(-110, -6)] + [Q(*p) for p in cwS[::-1]]
    els += [poly(cw, "#c9ad85", "#f2dcb4", 1.8, at), poly(cw, "url(#k-hatch)", "none", 0, at, op=.6)]
    els += [poly([Q(*p) for p in ENCL], "#1d1712", "rgba(242,220,180,.6)", 1.8, at)]
    els += plan_sphinx(QX(0), QY(0), QK, at)
    els += [poly([Q(*p) for p in STEMP], "#cdb184", GRAN, 4, at), poly([Q(*p) for p in VTEMP], "#cdb184", GRAN, 4, at)]
    if labels:
        els += [lab(QX(76), QY(0) + 8, "Sphinx Temple", at, INK, 24, halo=False), lab(QX(78), QY(-58) + 8, "Valley Temple", at, INK, 24, halo=False),
                lab(QX(-84), QY(-18) + 44, "causeway", at, "#f2dcb4", 26), lab(QX(-5), QY(30) - 14, "trench", at, BONE, 26)]
    els += [{"k": "line", "p": [[1640, 760], [1640, 700]], "c": "#e9dccb", "w": 2, "in": at}, lab(1640, 690, "N", at, "#e9dccb", 24)]
    return els


def s15():
    """The close plan: the trench's south wall and the causeway's north edge flash as one line ('one edge'); an inset of a path with
    a flowerbed hugging its edge (1 path, 2 flowerbed); then the same order on the plan (1 causeway, 2 trench)."""
    els = close_plan(-1)
    te, tf, tp = T("s15", "south wall"), T("s15", "When a flowerbed"), T("s15", "So the trench")
    edge = [Q(*p) for p in CW_N[:2]]
    els += [gl((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2, 240, te, .4, "lamp"), ln(edge, te, GOLD, 6, dur=1.0),
            lab((edge[0][0] + edge[1][0]) / 2 - 40, (edge[0][1] + edge[1][1]) / 2 + 44, "one edge", te + .6, GOLD, 30)]
    ix, iy = 1290, 150
    els += [rect(ix, iy, 380, 250, "rgba(18,13,10,.92)", "rgba(255,236,206,.4)", 1.5, 14, tf - .2, fx="pop"),
            poly([(ix + 20, iy + 150), (ix + 360, iy + 120), (ix + 360, iy + 175), (ix + 20, iy + 205)], "#9a958c", "#e9e4da", 1.5, tf),
            poly([(ix + 20, iy + 150), (ix + 360, iy + 120), (ix + 360, iy + 80), (ix + 20, iy + 110)], "#4f7a3a", "#9fd08a", 1.5, tf + .5)]
    for k in range(8):
        fx_ = ix + 40 + 40 * k
        els.append(circ(fx_, iy + 122 - 3.4 * k, 7, ["#e98a8a", "#f2c98e", "#c9c1ee"][k % 3], at=round(tf + .7 + .05 * k, 2), fx="pop"))
    els += [lab(ix + 300, iy + 230, "1 path", tf + .3, BONE, 24), lab(ix + 90, iy + 60, "2 flowerbed", tf + .8, "#9fd08a", 24)]
    els += chip(QX(-84) - 110, QY(-18) + 36, "1", AMBER, tp, 26) + chip(QX(-5) + 70, QY(30) - 22, "2", AMBER, tp + .5, 26)
    return {"base": "plan", "north": False, "cam": CAM, "els": els}


def s16():
    """Left: where the two temples meet, in elevation: the Valley Temple's wall, faced with red granite, its granite bench at the foot
    (1); then the Sphinx Temple's huge limestone end block is lowered into place over the bench (2). Right: the two temples in plan,
    limestone cores inside red granite casing."""
    tg, tl, ta = T("s16", "granite was already"), T("s16", "wall went up"), T("s16", "built alike")
    gyb = 650
    els = [rect(100, gyb, 820, 70, "#3a2e24", at=-1), ln([(100, gyb), (920, gyb)], -1, "rgba(255,226,190,.4)", 1.5, draw=False),
           lab(510, 150, "where the two temples meet", -1, DIM, 26)]
    vx = 560
    els += [rect(vx, gyb - 420, 330, 420, "#cdb184", "rgba(40,28,18,.6)", 1.5, 2, tg, fx="pop"), rect(vx, gyb - 420, 40, 420, GRAN, "#ffd0c0", 1.5, 1, tg + .1, fx="pop"),
            rect(vx - 120, gyb - 90, 160, 90, GRAN, "#ffd0c0", 2, 2, tg + .3, fx="pop")]
    els += [lab(vx + 165, gyb - 440, "Valley Temple", tg + .2, BONE, 26)] + chip(vx + 190, gyb - 250, "1 granite", GRAN, tg + .5, 24)
    blk = [(160, gyb - 360), (520, gyb - 360), (520, gyb - 92), (440, gyb - 92), (440, gyb), (160, gyb)]
    els += [poly(blk, "#d9c196", "rgba(40,28,18,.75)", 2, tl, fx="rise"), poly(blk, "url(#k-speck)", "none", 0, tl + .1)]
    els += [lab(300, gyb - 380, "Sphinx Temple", tl + .3, BONE, 26)] + chip(300, gyb - 200, "2 limestone", AMBER, tl + .6, 24)
    def temple(x, y, w, h, at, name, hall=False):
        out = [rect(x, y, w, h, GRAN, "#ffd0c0", 2, 3, at, fx="pop"), rect(x + 16, y + 16, w - 32, h - 32, "#cdb184", "rgba(40,28,18,.6)", 1.5, 2, at + .1, fx="pop")]
        if hall:
            out += [rect(x + w * .3, y + h * .2, w * .4, h * .55, "#3a2e24", at=at + .2, fx="pop"), rect(x + w * .15, y + h * .2, w * .7, h * .14, "#3a2e24", at=at + .2, fx="pop")]
        else:
            out += [rect(x + w * .25, y + h * .25, w * .5, h * .5, "#3a2e24", at=at + .2, fx="pop")]
        out += [lab(x + w / 2, y + h + 34, name, at + .3, BONE, 26)]
        return out
    els += temple(1040, 200, 250, 240, ta, "Sphinx Temple") + temple(1370, 210, 260, 270, ta + .3, "Valley Temple", True)
    els += [lab(1335, 600, "limestone core, granite casing", ta + 1.0, GOLD, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s17():
    """The trench's north-east corner, from the side: three big blocks lie on a dragging track short of the temple, the Sphinx's paws
    at right; two excavators kneel by them; chip '1978'."""
    x0, gy, sc = 980, 640, 13.0
    els, base = pit_scene("day", x0=x0, gy=gy, s=sc, wall_top=11.0, sun=[1500, 260, 26], pyr=False)
    els += sphinx(x0, gy, sc, -1)
    els += temple_wall(150, gy + 4, 4, 2, 90, 50, -1)
    tr, ty, tb = T("s17", "rubbish"), T("s17", "nineteen seventy-eight"), T("s17", "big blocks")
    els += [ln([(380, gy + 2), (960, gy + 2)], tr, "rgba(255,236,206,.6)", 2, "inferred", 1.0)]
    for k, bx in enumerate((470, 620, 770)):
        els += [rect(bx, gy - 58, 120, 58, "#d6bb8c", "rgba(40,28,18,.7)", 1.6, 2, round(tb + .25 * k, 2), fx="pop"),
                ring_(bx + 60, gy - 30, 76, round(tb + .8 + .2 * k, 2), GOLD, 2.5)]
    els += [person(560, gy, 40, tb + .5, "#2a2018"), person(720, gy, 40, tb + .6, "#2a2018")]
    els += chip(615, 360, "1978", AMBER, ty) + [lab(615, 300, "abandoned on the way", tb + 1.2, GOLD, 28)]
    base.update(cam=CAM, els=els)
    return base


def jar_profile(cx, by, h):
    """The outline of a plain Old Kingdom jar (tall, a rounded shoulder, a narrow base, a rolled rim), as a closed polygon."""
    pr = [(0, .0), (.16, .02), (.26, .12), (.34, .32), (.36, .52), (.32, .72), (.22, .86), (.15, .92), (.17, .97), (.15, 1.0)]
    right = [(cx + w * h * .6, by - y * h) for w, y in pr]
    left = [(cx - w * h * .6, by - y * h) for w, y in pr[::-1]]
    return right + left


def s18():
    """A finds tray under a lamp: half of a plain jar (its broken edge jagged), round hammer stones; copper flecks glint on one
    stone's striking end; a dotted copper chisel taps it."""
    els = [gl(889, 420, 700, -1, .25, "lamp"), rect(200, 190, 1380, 540, "#3a2c20", "rgba(255,236,206,.35)", 2, 18, -1),
           rect(220, 210, 1340, 500, "url(#k-speck)", at=-1, r=14)]
    tj, th, tc, tx = T("s18", "half of an"), T("s18", "stone hammers"), T("s18", "flecked with copper"), T("s18", "striking a chisel")
    jx, jy, jh = 470, 650, 360
    full = jar_profile(jx, jy, jh)
    els += [poly(full, "none", "rgba(232,184,122,.5)", 2, tj, style="inferred")]
    half = [(jx, jy - jh * .0)] + [(x, y) for x, y in full if x <= jx + 1] + [(jx, jy - jh)]
    brk = [(jx, jy - jh), (jx + 14, jy - jh * .88), (jx - 6, jy - jh * .74), (jx + 18, jy - jh * .6), (jx - 4, jy - jh * .45), (jx + 16, jy - jh * .3), (jx - 2, jy - jh * .15), (jx + 8, jy)]
    left = [(x, y) for x, y in full if x <= jx]
    els += [poly(left + brk, "#b07a4e", "#e9b98a", 2, tj + .2, fx="pop"), ln(brk, tj + .4, "#ffe2c0", 2, dur=.5)]
    els += [lab(jx, jy + 46, "half a jar, pyramid age", tj + .6, BONE, 26)]
    stones = [(880, 610, 52), (1010, 640, 44), (1140, 600, 56), (1270, 645, 42)]
    for k, (x, y, r) in enumerate(stones):
        pts = [(x + r * (1 + .08 * math.sin(3 * a + k)) * math.cos(a), y + r * .84 * (1 + .08 * math.cos(2 * a + k)) * math.sin(a)) for a in [j * math.pi / 10 for j in range(20)]]
        els += [poly(pts, "#8f8f8a", "#d9d6cc", 1.5, round(th + .15 * k, 2), fx="pop", curve=True),
                poly([(px + 0, py) for px, py in pts[11:16]] + [(x, y)], "rgba(255,255,255,.12)", "none", 0, round(th + .15 * k, 2), fx="pop")]
    els += [lab(1075, 712, "stone hammers", th + .6, BONE, 26)]
    x, y, r = stones[2]
    rnd = random.Random(4)
    for k in range(16):
        a = rnd.uniform(-2.5, -.6)
        els.append(circ(x + r * .82 * math.cos(a) + rnd.uniform(-5, 5), y + r * .7 * math.sin(a) + rnd.uniform(-4, 4), rnd.uniform(2.5, 4.5), "#7fd1a6", at=round(tc + .03 * k, 2), fx="pop"))
    els += [gl(x, y - r * .6, 80, tc, .6, "lamp"), lab(x + 90, y - r - 30, "copper flecks", tc + .3, "#9fe0b8", 26, "start")]
    ch = [(x - 50, y - r - 230), (x - 36, y - r - 236), (x + 4, y - r - 40), (x + 10, y - r - 20), (x - 14, y - r - 14), (x - 12, y - r - 36)]
    els += [poly(ch, "rgba(217,137,74,.18)", "#d9894a", 2.6, tx, style="claimed"),
            ln([(x - 22, y - r - 8), (x - 34, y - r + 2)], tx + .4, "#ffe2a8", 2, dur=.2), ln([(x + 2, y - r - 8), (x + 14, y - r + 4)], tx + .4, "#ffe2a8", 2, dur=.2),
            lab(x - 70, y - r - 160, "a chisel?", tx + .3, "#e8a066", 28, "end")]
    return {"base": "dark", "cam": CAM, "els": els}


def tomb_door(x, y, w, h, at, lit=False):
    """A small tomb doorway seen face on, its lintel and jambs carved with text."""
    out = [rect(x, y, w, h, "#b89a70", "rgba(255,236,206,.5)", 1.5, 2, at, fx="pop"), rect(x + w * .3, y + h * .35, w * .4, h * .65, "#1a1410", at=at + .05, fx="pop"),
           {"k": "glyphs", "x": round(x + 8, 1), "y": round(y + 8, 1), "w": round(w - 16, 1), "h": round(h * .22, 1), "rows": 2, "cols": 6, "kind": "hieroglyph", "c": "#4a3522", "in": round(at + .1, 2)}]
    return out


def s19():
    """Left: the temple's corner core blocks with rough knobs still sticking out (rings: 'never trimmed'). Right: a row of tomb doorways;
    a magnifier passes along them and none lights: 'no priest of the Sphinx'."""
    tk, tt, tm = T("s19", "rough knobs"), T("s19", "none of the hundreds"), T("s19", "A building site")
    els = [rect(110, 640, 700, 90, "#3a2e24", at=-1)]
    for r in range(3):
        for c in range(3):
            x, y = 170 + c * 200 - (60 if r == 1 else 0), 640 - (r + 1) * 130
            els.append(rect(x, y, 196, 126, "#cdb184", "rgba(40,28,18,.6)", 1.5, 2, -1))
    knobs = [(330, 460), (530, 330), (250, 200)]
    for k, (x, y) in enumerate(knobs):
        els += [poly([(x - 26, y), (x - 20, y - 24), (x + 18, y - 26), (x + 28, y)], "#d9c196", "rgba(40,28,18,.6)", 1.5, -1),
                ring_(x, y - 12, 48, round(tk + .25 * k, 2), GOLD, 3)]
    els += [lab(460, 160, "never trimmed", tk + .8, GOLD, 30), lab(460, 770, "the temple's corner", -1, DIM, 24)]
    for k in range(6):
        els += tomb_door(930 + 125 * k, 380, 105, 150, round(tt - .4 + .1 * k, 2))
    for k in range(6):
        mx = 982 + 125 * k
        at = round(tt + .3 + .35 * k, 2)
        els += [ring_(mx, 440, 36, at, "rgba(245,236,220,.7)", 3, dur=.3)]
    els += [lab(1305, 330, "hundreds of tombs", tt - .2, DIM, 26), lab(1305, 610, "no priest of the Sphinx", tt + 2.5, LILAC, 30)]
    els += [lab(1305, 680, "a building site, abandoned", tm + .2, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s20():
    """A small family tree (Khufu above Djedefre and Khafre). A time axis from 7500 to 2000 BCE: the three reigns are a hair-thin
    cluster near 2550 BCE; a magnifier lifts it into a box where they show side by side ('decades'); along the axis, a long lilac
    dotted bar: 'millennia'."""
    tk, tm, tf, td = T("s20", "Was it Khafre"), T("s20", "Most Egyptologists"), T("s20", "his father"), T("s20", "decades")
    els = []
    def node(x, y, t, at, c=BONE, w=200):
        return [rect(x - w / 2, y - 28, w, 56, "rgba(18,13,10,.9)", c, 2, 10, at, fx="pop"), lab(x, y + 10, t, at + .05, c, 28)]
    els += node(370, 230, "Khufu", tf, BONE) + node(230, 400, "Djedefre", tf + .4, BONE) + node(510, 400, "Khafre", tk, GOLD)
    els += [ln([(370, 258), (370, 320), (230, 320), (230, 372)], tf + .2, DIM, 2, dur=.5), ln([(370, 320), (510, 320), (510, 372)], tf + .2, DIM, 2, dur=.5)]
    els += [lab(510, 462, "most Egyptologists", tm, GOLD, 26)]
    ax0, ax1, ay = 760, 1640, 640
    X = lambda bce: round(ax0 + (7500 - bce) / 5500 * (ax1 - ax0), 1)
    els += [axis(ax0, ax1, ay, [(X(7000), "7000 BCE"), (X(5000), "5000"), (X(3000), "3000"), (X(2000), "2000")], .2)]
    els += [rect(X(2590), ay - 14, X(2532) - X(2590), 10, GOLD, at=tk, fx="pop")]
    mx, my = X(2560), ay - 10
    els += [ring_(mx, my, 22, tf + .2, BONE, 2), ln([(mx, my - 22), (1300, 470)], tf + .4, DIM, 1.5, dur=.4)]
    bx0, bx1, by = 1060, 1600, 380
    els += [rect(bx0 - 20, by - 150, bx1 - bx0 + 40, 230, "rgba(18,13,10,.9)", "rgba(255,236,206,.35)", 1.5, 12, tf + .5, fx="pop")]
    BX = lambda bce: round(bx0 + (2600 - bce) / 80 * (bx1 - bx0), 1)
    for k, (a, b, c, t, name) in enumerate([(2590, 2566, BONE, tf + .7, "Khufu"), (2566, 2558, BONE, tf + .9, "Djedefre"), (2558, 2532, GOLD, tk + .2, "Khafre")]):
        y = by - 90 + 46 * k
        els += [rect(BX(a), y, BX(b) - BX(a), 22, c, at=max(t, tf + .7), fx="pop"), lab(BX(a) - 12, y + 18, name, max(t, tf + .7) + .1, c, 24, "end")]
    els += bracket(BX(2590), BX(2532), by + 56, td, "decades", GOLD, up=True, size=30, ty=by + 64 + 0)
    els += [rect(X(7000), ay - 50, X(3000) - X(7000), 12, "rgba(201,193,238,.35)", at=td + .6, fx="fade"),
            lab((X(7000) + X(3000)) / 2, ay - 70, "millennia", td + .8, LILAC, 30, st="ital")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}



# ================================================================== CHAPTER 3 · Written by rain?
def wall_face(x, y, w, h, at=-1, round_at=None, fiss_at=None, n=7, rain_at=None, deep=1.0):
    """A pit wall seen face on: hard beds (pale, sharp) and soft beds (darker); at round_at the soft beds are cut back into rounded
    hollows under the hard ones (a shadow under each overhang); at fiss_at four deep vertical cracks draw down from the top."""
    bh = h / n
    els = [rect(x, y, w, h, "#b39773", "rgba(255,236,206,.45)", 1.5, 4, at), rect(x, y, w, h, "url(#k-speck)", at=at, r=4)]
    for i in range(n):
        y0 = y + bh * i
        if i % 2:
            els.append(rect(x, y0, w, bh, "#8a6f52", at=at))
            if round_at is not None:
                top = [(x + u * w / 60, y0 + bh * (.35 + .1 * math.sin(u * .7 + i)) * deep) for u in range(61)]
                els.append(poly([(x, y0)] + top + [(x + w, y0)], "rgba(30,20,12,.55)", "none", 0, round(round_at + .12 * (i // 2), 2)))
                els.append(ln(top, round(round_at + .12 * (i // 2), 2), "#3a2c1e", 2.2, dur=.8, curve=True))
                bot = [(x + u * w / 60, y0 + bh - bh * (.12 + .05 * math.sin(u * .9 + i))) for u in range(61)]
                els.append(poly([(x, y0 + bh)] + bot + [(x + w, y0 + bh)], "rgba(255,236,206,.14)", "none", 0, round(round_at + .12 * (i // 2), 2)))
        else:
            els.append(ln([(x, y0 + 2), (x + w, y0 + 2)], at, "rgba(255,240,214,.5)", 1.6, draw=False))
    fis = []
    for j, f in enumerate((.17, .41, .62, .85)):
        pts = [(x + w * f, y + 4), (x + w * (f + .012), y + h * .28), (x + w * (f - .01), y + h * .55), (x + w * (f + .006), y + h * .8), (x + w * f, y + h - 6)]
        fis.append(pts)
        if fiss_at is not None:
            els.append(ln(pts, round(fiss_at + .15 * j, 2), "#21180f", 7, dur=.7, curve=True))
            els.append(ln([(px + 4, py) for px, py in pts], round(fiss_at + .15 * j, 2), "rgba(255,226,190,.25)", 1.5, dur=.7, curve=True))
    if rain_at is not None:
        for j, pts in enumerate(fis):
            at2 = round(rain_at + .4 + .3 * j, 2)
            els.append(ln(pts, at2, "#7fc0e0", 3.5, dur=.9, curve=True))
            els.append(poly(E(pts[-1][0], y + h + 6, 40, 8, 16), "rgba(111,182,214,.6)", "none", 0, round(at2 + .8, 2), fx="pop"))
    return els, fis


def s21():
    """The pit wall face on, hard and soft beds; a small geologist with a hand lens at its foot ('about 1990'); on 'rounded hollows'
    the soft beds cut back into rolling recesses; on 'cracks' four deep vertical cracks draw down from the top."""
    tr, tc = T("s21", "rounded hollows"), T("s21", "long cracks")
    els, fis = wall_face(150, 140, 1480, 600, -1, tr, tc)
    els += [rect(80, 740, 1620, 60, "#2a211a", at=-1), person(300, 742, 92, .3, "#2a2018"), circ(326, 668, 9, "none", "#f2dcb4", 2, .5, fx="pop"),
            ln([(318, 676), (312, 690)], .5, "#f2dcb4", 2, draw=False)]
    els += chip(300, 610, "about 1990", AMBER, .4, 24)
    return {"base": "dark", "cam": CAM, "els": els}


def s29_add():
    """The worn wall as a clock: a clock face draws itself on the rock, its hands spinning unevenly; a lilac '?'."""
    t, tq = T("s29", "a clock"), T("s29", "keeps good time")
    cx, cy, R = 889, 440, 150
    out = [circ(cx, cy, R, "rgba(18,13,10,.6)", BONE, 3.5, t, fx="pop")]
    out += [ln([(cx + (R - 20) * math.cos(math.radians(a)), cy + (R - 20) * math.sin(math.radians(a))), (cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))],
               t + .1, BONE, 3, draw=False) for a in range(0, 360, 30)]
    for k in range(9):
        a = math.radians(-90 + 37 * k + (k % 3) * 22)
        out.append(ln([(cx, cy), (cx + 110 * math.cos(a), cy + 110 * math.sin(a))], round(t + .4 + .14 * k * (1 + (k % 2)), 2), BONE, 5, draw=False, op=round(.2 + .08 * (k % 3), 2)))
    out += [circ(cx, cy, 9, BONE, at=t + .3, fx="pop")] + qmark(cx + 260, cy + 40, tq, 110)
    return out


def s22():
    """Rain streams down a wall and into its cracks; two swatches, 'wind' (sharp level grooves, arrows sideways) and 'rain' (rounded,
    cut downwards); then a tomb front with a crisp carved inscription: 'tomb of Khafre's age'."""
    tr, tw, td, tt = T("s22", "signature of rain"), T("s22", "Wind carves"), T("s22", "rain cuts down"), T("s22", "tombs of Khafre's")
    els, fis = wall_face(110, 170, 560, 520, -1, -1, -1, rain_at=tr)
    els += [{"k": "rays", "x0": 110, "x1": 670, "y0": 120, "y1": 200, "n": 40, "spread": .1, "c": "#b9d6e8", "in": tr, "fx": "draw", "dur": 1.0}]
    els += [lab(390, 760, "Schoch: rain", tr + 1.2, BLUE, 28)]
    sx, sw = 760, 330
    els += [rect(sx, 170, sw, 220, "#b39773", "rgba(255,236,206,.4)", 1.5, 6, tw - .2, fx="pop")]
    for k in range(4):
        y = 205 + 50 * k
        els.append(poly([(sx, y), (sx + sw, y), (sx + sw, y + 16), (sx, y + 16)], "#6f5640", "none", 0, round(tw + .1 * k, 2)))
    els += [arr([(sx + 30, 382), (sx + 130, 382)], tw + .5, BONE, 2.5, "known", .5, False), arr([(sx + 160, 382), (sx + 260, 382)], tw + .6, BONE, 2.5, "known", .5, False),
            lab(sx + sw / 2, 160, "wind", tw, BONE, 28)]
    els += [rect(sx, 450, sw, 240, "#b39773", "rgba(255,236,206,.4)", 1.5, 6, td - .2, fx="pop")]
    for k in range(4):
        x = sx + 40 + 80 * k
        els.append(poly([(x - 16, 452), (x + 16, 452), (x + 10, 600), (x + 4, 680), (x - 4, 680), (x - 10, 600)], "#6f5640", "none", 0, round(td + .1 * k, 2), curve=True))
    els += [arr([(sx + sw + 24, 470), (sx + sw + 24, 660)], td + .5, BLUE, 2.5, "known", .5, False), lab(sx + sw / 2, 730, "rain", td, BLUE, 28)]
    tx0, ty0 = 1200, 230
    els += [poly([(tx0, 680), (tx0 + 30, ty0), (tx0 + 430, ty0), (tx0 + 460, 680)], "#c2a57c", "rgba(255,236,206,.5)", 2, tt, fx="pop"),
            rect(tx0 + 170, 470, 120, 210, "#1a1410", at=tt + .1, fx="pop"),
            rect(tx0 + 120, 270, 220, 170, "#d6bb8c", "rgba(40,28,18,.6)", 1.5, 3, tt + .2, fx="pop"),
            {"k": "glyphs", "x": tx0 + 134, "y": 284, "w": 192, "h": 140, "rows": 4, "cols": 5, "kind": "hieroglyph", "c": "#3a2a1a", "in": round(tt + .3, 2)},
            lab(tx0 + 230, 740, "tomb of Khafre's age", tt + .4, BONE, 28), lab(tx0 + 230, ty0 - 20, "inscription still sharp", tt + .8, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s23():
    """A section through the pit's floor: a hammer strikes a plate, a row of geophones, sound arcs spread and echoes return ('1991');
    inset: a wall with damp creeping in from its face, '1 year' and '10 years' deep."""
    fy = 360
    els = [rect(80, fy, 1060, 440, "#6f5a43", at=-1), rect(80, fy, 1060, 440, "url(#k-speck)", at=-1), ln([(80, fy), (1140, fy)], -1, "#e7cfa6", 2.4, draw=False),
           lab(1120, fy - 22, "the floor of the pit", -1, DIM, 26, "end")]
    ts, ta = T("s23", "sent sound waves"), T("s23", "Weathering creeps")
    hx = 330
    els += [rect(hx - 40, fy - 16, 80, 16, "#8c7152", "#f2dcb4", 2, 3, .3, fx="pop"), ln([(hx + 70, fy - 130), (hx + 10, fy - 34)], .5, "#cbbca8", 7, dur=.3),
            rect(hx - 4, fy - 52, 44, 26, "#8a8a90", "#e9dccb", 1.5, 4, .5, fx="pop")]
    for k in range(7):
        gx = 440 + 100 * k
        els.append(poly([(gx - 10, fy), (gx + 10, fy), (gx, fy - 20)], BLUE, at=round(.6 + .07 * k, 2), fx="pop"))
    for j, r in enumerate((70, 140, 210, 280)):
        a0 = 12 if r * 1.25 < hx - 90 else math.degrees(math.acos(min(1, (hx - 90) / (r * 1.25))))
        els.append({"k": "line", "p": R(ellipse(hx, fy, r * 1.25, r, 18, 12, 180 - a0)), "c": BLUE, "w": 2.4, "curve": True, "in": round(ts + .3 * j, 2), "fx": "draw", "dur": .5})
    for k, gx in enumerate((640, 840, 1040)):
        els.append(arr([(hx + (gx - hx) * .5, fy + 280), (gx, fy + 6)], round(ts + 1.4 + .25 * k, 2), AMBER, 2.4, "known", .6, False))
    els += chip(700, 220, "1991", AMBER, ts - .2)
    ix, iy, iw, ih = 1220, 200, 440, 460
    els += [rect(ix, iy, iw, ih, "rgba(18,13,10,.92)", "rgba(255,236,206,.4)", 1.5, 14, ta - .3, fx="pop"),
            rect(ix + 60, iy + 60, 280, 340, "#b39773", "rgba(255,236,206,.4)", 1.5, 2, ta - .2, fx="pop"),
            lab(ix + 40, iy + 40, "the face", ta, DIM, 22, "start")]
    els += [rect(ix + 60, iy + 60, 50, 340, "rgba(63,134,168,.55)", at=ta + 1.0, fx="pop"), rect(ix + 60, iy + 60, 150, 340, "rgba(63,134,168,.3)", at=ta + 2.6, fx="pop")]
    els += [lab(ix + 85, iy + 436, "1 year", ta + 1.2, BLUE, 24), lab(ix + 200, iy + 436, "10 years", ta + 2.8, BLUE, 24)]
    return {"base": "dark", "cam": CAM, "els": els}


def s24():
    """The Sphinx in its pit, from above (north up, the face to the east, right): the floor's weathered layer shaded deep blue in front
    and along both sides ('up to 2.5 m deep'), pale behind the haunches ('about 1.2 m'); beside it two depth bars and a person to scale."""
    tf, tb = T("s24", "In front and"), T("s24", "Behind the lion")
    k, cx, cy = 7.0, 640, 450
    P = lambda e, n: (cx + e * k, cy - n * k)
    els = [rect(80, 140, 1150, 620, "#a88a64", at=-1, op=.5)]
    pit = [P(-62, 34), P(56, 34), P(56, -34), P(-62, -34)]
    els += [poly(pit, "#2a2119", "rgba(242,220,180,.6)", 1.8, -1)]
    els += [poly([P(-40, 34), P(56, 34), P(56, -34), P(-40, -34)], "rgba(63,134,168,.75)", "none", 0, tf, fx="fade"),
            poly([P(-62, 34), P(-40, 34), P(-40, -34), P(-62, -34)], "rgba(159,208,255,.22)", "none", 0, tb, fx="fade")]
    els += plan_sphinx(cx, cy, k, -1)
    els += [poly(pit, "none", "rgba(242,220,180,.6)", 1.8, -1)]
    els += [ln([P(50, 30), P(64, 44)], tf + .4, BLUE, 2, dur=.3), lab(P(64, 44)[0] + 8, P(64, 44)[1] - 4, "up to 2.5 m deep", tf + .5, BLUE, 30, "start"),
            ln([P(-56, -30), P(-66, -44)], tb + .3, "#cfe6ff", 2, dur=.3), lab(P(-66, -44)[0] + 6, P(-66, -44)[1] + 28, "about 1.2 m", tb + .4, "#cfe6ff", 30, "start")]
    els += [{"k": "line", "p": [[1180, 760], [1180, 700]], "c": "#e9dccb", "w": 2, "in": -1}, lab(1180, 690, "N", -1, "#e9dccb", 22)]
    bx, by, m = 1340, 420, 100
    els += [ln([(1270, by), (1680, by)], -1, "#e7cfa6", 2, draw=False), lab(1475, by - 210, "depth below the floor", -1, DIM, 24)]
    els += [rect(bx, by, 70, 2.4 * m, "rgba(63,134,168,.75)", BLUE, 2, 2, tf + .4, fx="fade"), lab(bx + 35, by + 2.4 * m + 34, "2.5 m", tf + .8, BLUE, 26)]
    els += [rect(bx + 120, by, 70, 1.2 * m, "rgba(159,208,255,.3)", "#cfe6ff", 2, 2, tb + .4, fx="fade"), lab(bx + 155, by + 1.2 * m + 34, "1.2 m", tb + .8, "#cfe6ff", 26)]
    els += [person(bx + 270, by, 1.7 * m, -1, "#e8d6b8"), lab(bx + 270, by - 1.7 * m - 14, "a person", -1, DIM, 22)]
    return {"base": "plan", "north": False, "cam": CAM, "els": els}


def s25():
    """A timeline from 12,000 BCE to 1 CE: Khafre about 2500 BCE (amber, 'the back'); Schoch's blue dashed band 7000 to 5000 BCE
    ('1992', 'the front'); then a lilac dotted mark near 10,000 BCE ('2017, with Bauval'). Above, a small Sphinx: its back amber, its front blue."""
    tbk, tfr, t92, t17 = T("s25", "back was cut"), T("s25", "front long"), T("s25", "nineteen ninety-two"), T("s25", "twenty seventeen")
    X = lambda bce: round(180 + (12000 - bce) / 12000 * 1420, 1)
    ay = 600
    els = [axis(180, 1600, ay, [(X(12000), "12,000 BCE"), (X(10000), "10,000"), (X(8000), "8000"), (X(6000), "6000"), (X(4000), "4000"), (X(2000), "2000"), (1600, "1 CE")], .2)]
    els += [ln([(X(2500), ay), (X(2500), ay - 70)], .4, AMBER, 3, dur=.3), circ(X(2500), ay, 9, AMBER, at=.4, fx="pop"), lab(X(2500), ay - 84, "Khafre", .5, AMBER, 28)]
    x0, gy, sc = 760, 420, 7.5
    els += sphinx(x0, gy, sc, -1, casing=False, beds=False, shadow=False)
    M = lambda pts: [(x0 + x * sc, gy - y * sc) for x, y in pts]
    back = [(x, vtop(BODY, x)) for x in [50 + k * .5 for k in range(47)]] + [(73, 0), (50, 0)]
    frontb = [(0, 0)] + [(x, vtop(BODY, x)) for x in [k * .5 for k in range(101)]] + [(50, 0)]
    els += [poly(M(back), "rgba(232,184,122,.55)", AMBER, 2, tbk, fx="fade"), lab(x0 + 62 * sc, gy + 34, "the back", tbk + .3, AMBER, 24),
            poly(M(frontb), "rgba(159,208,255,.35)", BLUE, 2, tfr, fx="fade"), poly(M(NEMES), "rgba(159,208,255,.35)", BLUE, 2, tfr, fx="fade"),
            poly(M(FACE), "rgba(159,208,255,.35)", BLUE, 2, tfr, fx="fade"), lab(x0 + 25 * sc, gy + 34, "the front", tfr + .3, BLUE, 24)]
    els += [rect(X(7000), ay - 46, X(5000) - X(7000), 24, "rgba(159,208,255,.4)", BLUE, 2, 12, t92, fx="pop", style="inferred"),
            lab((X(7000) + X(5000)) / 2, ay - 60, "Schoch, 1992", t92 + .3, BLUE, 28)]
    els += [rect(X(10500), ay - 46, X(9700) - X(10500), 24, "rgba(201,193,238,.35)", LILAC, 2.5, 12, t17, fx="pop", style="claimed"),
            lab(X(10100), ay - 94, "2017, with Bauval:", t17 + .3, LILAC, 26), lab(X(10100), ay - 62, "about 12,000 years ago", t17 + .4, LILAC, 26)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s26():
    """A temple wall in section: a limestone core block with a rounded, worn face; a red granite facing slab comes in and its back
    follows the worn curve; tag 'worn first?' in blue dashes (Schoch's reading)."""
    ta = T("s26", "already weathered")
    bx0, bx1, y0, y1 = 420, 900, 230, 670
    face = [(bx1 - 10 * math.sin((y - y0) / 40.0) - 24 * math.sin((y - y0) / 110.0) - 18, y) for y in range(y0, y1 + 1, 20)]
    blk = [(bx0, y0)] + face + [(bx0, y1)]
    els = [rect(300, y1, 1100, 60, "#3a2e24", at=-1), poly(blk, "#cdb184", "rgba(40,28,18,.6)", 2, -1), poly(blk, "url(#k-speck)", "none", 0, -1),
           lab((bx0 + bx1) / 2 - 40, y0 - 24, "limestone core", -1, BONE, 28)]
    gr = face + [(bx1 + 110, y1), (bx1 + 110, y0)]
    els += [poly(gr, GRAN, "#ffd0c0", 2, ta - 1.2, fx="fade"), lab(bx1 + 60, y0 - 24, "granite facing", ta - 1.0, "#f0b0a0", 28),
            arr([(bx1 + 300, 450), (bx1 + 140, 450)], ta - 1.4, "#f0b0a0", 3, "known", .5, False)]
    els += [ln(face, ta, BLUE, 4, "inferred", 1.0, curve=True), lab(bx1 + 220, 600, "worn first?", ta + .5, BLUE, 32, "start"), lab(bx1 + 220, 640, "Schoch's reading", ta + .7, DIM, 24, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s27():
    """The Sphinx in profile; the head outlined in gold; a larger, dotted lilac head behind it (an older head, as he suggests);
    'too small?'."""
    th, tr = T("s27", "head looks too"), T("s27", "recarved")
    x0, gy, sc = 300, 720, 15.0
    els = [rect(-60, gy, 1900, 400, "#2a211a", at=-1), gl(560, 440, 420, -1, .18, "lamp")]
    els += sphinx(x0, gy, sc, -1)
    M = lambda pts: [(x0 + x * sc, gy - y * sc) for x, y in pts]
    head = NEMES
    els += [poly(M(head), "none", GOLD, 3.5, th, fx="draw", dur=.9), poly(M(FACE), "none", GOLD, 3.5, th + .1, fx="draw", dur=.9)]
    cxh, cyh, f = 17.0, 11.0, 1.45
    big = [(cxh + (x - cxh) * f, cyh + (y - cyh) * f) for x, y in NEMES]
    bigf = [(cxh + (x - cxh) * f, cyh + (y - cyh) * f) for x, y in FACE]
    els += [poly(M(big), "rgba(201,193,238,.12)", LILAC, 4, tr, style="claimed"), poly(M(bigf), "rgba(201,193,238,.08)", LILAC, 4, tr + .1, style="claimed"),
            lab(x0 + 17 * sc, gy - 25.5 * sc, "an older head?", tr + .4, LILAC, 32, st="ital"),
            ln([(x0 + 22.5 * sc, gy - 17 * sc), (x0 + 30 * sc, gy - 16.5 * sc)], th + .3, GOLD, 2, dur=.3), lab(x0 + 30.6 * sc, gy - 16.2 * sc, "too small?", th + .4, GOLD, 32, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s28():
    """The plateau in section sloping east (left) down to the pit: rain falls upslope, blue runoff runs down the surface and pours
    over the pit's back edge ('runoff'). Below, a small timeline: Khafre's mark, Reader's short green band just before it ('a few
    centuries'), Schoch's blue band far to the left, dimmed."""
    trr, tr = T("s28", "rain runoff"), T("s28", "His Sphinx")
    x0, gy, sc = 300, 560, 8.0
    pe = 300 + 73 * sc + 80
    surf = [(-60, 430), (220, 440), (pe, 440)] + [(x, 440 - (x - pe) * .22) for x in range(int(pe) + 40, 1861, 40)]
    els = [poly(surf + [(1860, 1100), (-60, 1100)], "#6f5a43", "rgba(255,226,190,.5)", 2, -1), poly(surf + [(1860, 1100), (-60, 1100)], "url(#k-speck)", "none", 0, -1)]
    els += [rect(220, 440, pe - 220, gy - 440, "#1d1712", "rgba(255,226,190,.4)", 1.5, 0, -1)]
    els += sphinx(x0, gy, sc, -1, shadow=False)
    els += [lab(pe + 180, 330, "the plateau", -1, DIM, 26), lab(240, 420, "east", -1, DIM, 22, "start"), lab(1700, 230, "west", -1, DIM, 22, "end")]
    els += [{"k": "rays", "x0": pe + 120, "x1": 1700, "y0": 130, "y1": 300, "n": 40, "spread": .08, "c": "#b9d6e8", "in": trr - .6, "fx": "draw", "dur": 1.0}]
    for k in range(4):
        a = round(trr + .2 + .2 * k, 2)
        x1_ = 1650 - 120 * k
        els.append(arr([(x1_, 440 - (x1_ - pe) * .22 - 8), (pe + 40, 432), (pe - 10, 470 + 20 * k)], a, BLUE, 3.4, "known", 1.0))
    els += [lab(pe + 300, 380, "runoff", trr + .9, BLUE, 30)]
    X = lambda bce: round(300 + (7500 - bce) / 5500 * 1200, 1)
    ay = 700
    els += [ln([(X(7500), ay), (X(2000), ay)], tr - .4, BONE, 2, dur=.5)]
    els += [circ(X(2500), ay, 8, AMBER, at=tr - .2, fx="pop"), lab(X(2500), ay + 34, "Khafre", tr - .1, AMBER, 24)]
    els += [rect(X(2850), ay - 18, X(2560) - X(2850), 14, GREEN, at=tr + .3, fx="pop"), lab(X(2700), ay - 30, "Reader: a few centuries", tr + .5, GREEN, 26)]
    els += [rect(X(7000), ay - 18, X(5000) - X(7000), 14, "rgba(159,208,255,.35)", at=tr + .8, fx="pop"), lab(X(6000), ay - 30, "Schoch", tr + 1.0, "rgba(159,208,255,.7)", 24)]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": False, "cam": CAM, "els": els}


# ================================================================== CHAPTER 4 · Salt, sand and silence
def s30():
    """Magnified grains of a soft bed: a moon, dew soaks in between the grains (blue); a sun, it dries, white salt crystals grow in the
    pores and push the grains apart (cracks). Inset: a damp cellar wall with a white crust flaking off."""
    tn, td, tg, tb, tc = T("s30", "Night dew"), T("s30", "by day"), T("s30", "salt crystals"), T("s30", "burst the"), T("s30", "white crust")
    cx, cy, R = 560, 450, 290
    els = [circ(cx, cy, R + 12, "#120e0b", "rgba(255,236,206,.5)", 3, -1), lab(cx, cy - R - 28, "a soft bed, magnified", -1, DIM, 24)]
    rnd = random.Random(8)
    grains = []
    for i in range(-5, 6):
        for j in range(-5, 6):
            x, y = cx + i * 56 + (28 if j % 2 else 0) + rnd.uniform(-6, 6), cy + j * 50 + rnd.uniform(-6, 6)
            if math.hypot(x - cx, y - cy) < R - 30:
                grains.append((x, y, rnd.uniform(22, 27)))
    for x, y, r in grains:
        els.append(poly(E(x, y, r, r * .86, 14), "#c9ab7e", "rgba(60,44,30,.6)", 1.2, -1, curve=True))
    els += [circ(cx - R + 20, cy - R + 40, 26, "#efe8da", at=tn - .2, fx="pop"), circ(cx - R + 32, cy - R + 34, 24, "#120e0b", at=tn - .2, fx="pop"),
            lab(cx - R + 60, cy - R + 100, "dew", tn + .4, BLUE, 26, "start")]
    for k, (x, y, r) in enumerate(grains[::3]):
        els.append(circ(x + r * .95, y + r * .5, 7, "rgba(111,182,214,.8)", at=round(tn + .2 + .02 * k, 2), fx="pop"))
    els += [circ(cx + R - 20, cy - R + 40, 30, "#ffe2b4", at=td, fx="pop"), gl(cx + R - 20, cy - R + 40, 90, td, .6, "sun")]
    for k, (x, y, r) in enumerate(grains[1::2]):
        els.append(poly([(x + r + 2, y - 8), (x + r + 12, y), (x + r + 2, y + 8), (x + r - 8, y)], "#f7f3ea", "#ffffff", 1, round(tg + .03 * k, 2), fx="pop"))
    els += [lab(cx + R - 70, cy + R + 10, "salt crystals", tg + .5, "#f7f3ea", 26, "end")]
    for k, (x, y, r) in enumerate(grains[2::4]):
        els.append(ln([(x - r * .3, y - r * .2), (x + r * .1, y + r * .3), (x + r * .4, y + r * .1)], round(tb + .03 * k, 2), "#ffe2a8", 2, dur=.2))
    ix, iy = 1130, 230
    els += [rect(ix, iy, 470, 420, "rgba(18,13,10,.92)", "rgba(255,236,206,.4)", 1.5, 14, tc - .3, fx="pop"),
            rect(ix + 40, iy + 40, 390, 300, "#8f7f6c", "rgba(255,236,206,.4)", 1.5, 2, tc - .2, fx="pop")]
    for k in range(12):
        x, y = ix + 60 + (k % 6) * 60, iy + 120 + (k // 6) * 110
        els.append(poly([(x, y), (x + 40, y - 8), (x + 52, y + 14), (x + 12, y + 22)], "#f2efe8", "#ffffff", 1, round(tc + .05 * k, 2), fx="pop"))
    els += [lab(ix + 235, iy + 390, "a damp cellar wall", tc + .3, BONE, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s31():
    """Left: the wall, its soft bands retreating into rounded hollows while the hard ones stay, no rain drawn ('no rain needed').
    Right: a deep section of the limestone, joints widening into channels as groundwater moves; a time arrow from 'millions of years
    ago' to 'humans', a tiny person at its far end."""
    ts, tj, th = T("s31", "Soft bands"), T("s31", "natural joints"), T("s31", "humans")
    els, fis = wall_face(110, 150, 680, 560, -1, ts + .3, None, deep=1.25)
    els += [lab(450, 760, "no rain needed", ts + 1.4, GOLD, 30)]
    x0, x1, y0, y1 = 900, 1660, 170, 620
    for k, (y, c) in enumerate(((y0, "#a88a64"), (y0 + 115, "#8f7350"), (y0 + 230, "#a07f5a"), (y0 + 345, "#7d6448"))):
        els.append(rect(x0, y, x1 - x0, 115 if k < 3 else y1 - y, c, at=-1))
    els += [rect(x0, y0, x1 - x0, y1 - y0, "url(#k-speck)", at=-1), lab((x0 + x1) / 2, y0 - 22, "deep in the rock", -1, DIM, 24)]
    for k, x in enumerate((1010, 1200, 1390, 1560)):
        pts = [(x, y0), (x + 10, y0 + 140), (x - 6, y0 + 300), (x + 4, y1)]
        els.append(ln(pts, -1, "#3a2c1e", 2, draw=False, curve=True))
        els.append(poly([(x - 14, y0 + 2), (x + 18, y0 + 2), (x + 26, y0 + 140), (x + 8, y0 + 300), (x + 18, y1 - 2), (x - 10, y1 - 2), (x - 20, y0 + 300), (x - 6, y0 + 140)],
                        "rgba(63,134,168,.6)", "#9fd0ff", 1.5, round(tj + .2 * k, 2)))
    els += [lab(1280, y1 + 40, "joints widened by groundwater", tj + .8, BLUE, 26)]
    els += [arr([(940, 720), (1580, 720)], tj + 1.2, BONE, 3, "known", 1.0, False), lab(940, 760, "millions of years ago", tj + 1.4, BONE, 24, "start"),
            person(1620, 724, 40, th, "#e8d6b8"), lab(1620, 670, "humans", th + .2, AMBER, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s32():
    """Side section: the pit filled with sand up to the lion's neck; a damp blue zone through the lower sand; at left a blue flood line
    rises to just below the pit floor ('Nile floods'); small blue arrows of moisture press into the walls."""
    tr, tf, td = T("s32", "wetted by rain"), T("s32", "Nile floods"), T("s32", "Damp sand")
    x0, gy, sc = 380, 640, 13.0
    els, base = pit_scene("dusk", x0=x0, gy=gy, s=sc, wall_top=11.0, sun=False, pyr=False)
    els += sphinx(x0, gy, sc, -1, light=.8)
    X = lambda m: x0 + m * sc
    Y = lambda m: gy - m * sc
    sand = [(-60, Y(11.0)), (X(4), Y(11.4)), (X(12), Y(12.0)), (X(18), Y(12.6)), (X(30), Y(13.6)), (X(50), Y(12.8)), (X(70), Y(12.0)), (1860, Y(11.2)), (1860, gy), (-60, gy)]
    els += [poly(sand, "#a98b62", "rgba(255,236,206,.45)", 1.5, -1, curve=True), poly(sand, "url(#k-speck)", "none", 0, -1, curve=True)]
    els += [lab(X(40), Y(12.6) - 18, "sand", -1, BONE, 28)]
    els += [{"k": "rays", "x0": 200, "x1": 1600, "y0": 130, "y1": Y(13), "n": 50, "spread": .08, "c": "#b9d6e8", "in": tr, "fx": "draw", "dur": 1.0}]
    damp = [(-60, Y(6)), (X(20), Y(6.8)), (X(45), Y(6.2)), (1860, Y(6.6)), (1860, gy), (-60, gy)]
    els += [poly(damp, "rgba(63,134,168,.45)", "none", 0, td - .2, curve=True), lab(X(40), Y(3.2), "damp sand", td + .3, "#cfe6ff", 28)]
    els += [rect(-60, gy + 14, 380, 200, "rgba(63,134,168,.8)", at=tf, fx="fill", dur=1.4), ln([(-60, gy + 14), (320, gy + 14)], tf + 1.2, "#9fd0ff", 3, dur=.6),
            arr([(340, gy + 140), (340, gy + 26)], tf + .3, BLUE, 3, "known", .9, False), lab(360, gy + 90, "Nile floods", tf + .6, "#cfe6ff", 28, "start")]
    for k, x in enumerate((60, 1720)):
        for j in range(3):
            y = Y(2 + 3 * j)
            d = -1 if x > 900 else 1
            els.append(arr([(x + d * -40, y), (x + d * 10, y)], round(td + .4 + .1 * (j + 3 * k), 2), BLUE, 2.4, "known", .4, False))
    base.update(cam=CAM, els=els)
    return base


def s33():
    """The Sphinx in profile: casing blocks pop along its worn body ('about 1400 BCE'); then a chunk of the shoulder lies fallen on the
    floor, a dark gap where it was ('1988'); then wind lines and flakes peeling off the pit wall behind."""
    tc, tf, tw = T("s33", "new skin"), T("s33", "nineteen eighty-eight"), T("s33", "windy days")
    x0, gy, sc = 330, 690, 15.0
    els, base = pit_scene("day", x0=x0, gy=gy, s=sc, wall_top=11.0, sun=[1560, 220, 26], pyr=False)
    els += sphinx(x0, gy, sc, -1, casing=False)
    k = 0
    for x in range(2, 60, 3):
        h = 2.6 if x < 12 else min(3.4, vtop(BODY, x + 1.5) - .2)
        if x >= 12 and x < 14:
            continue
        els.append(rect(x0 + x * sc, gy - h * sc, 3 * sc - 2, h * sc, "#e2cda4", "rgba(40,28,18,.6)", 1.2, 1, round(tc + .05 * k, 2), fx="pop"))
        k += 1
    els += chip(x0 + 30 * sc, gy + 46, "about 1400 BCE", AMBER, tc + .3, 24)
    sx, sy = x0 + 24 * sc, gy - 11.6 * sc
    chunk = [(sx - 20, sy - 12), (sx + 26, sy - 16), (sx + 34, sy + 14), (sx - 10, sy + 20)]
    els += [poly(chunk, "#1d1712", "none", 0, tf), poly([(x + 60, y + 11.6 * sc - 22) for x, y in chunk], "#d6bb8c", "rgba(40,28,18,.7)", 1.5, tf + .2, fx="rise"),
            arr([(sx + 6, sy + 20), (sx + 60, gy - 40)], tf + .1, RED, 2.5, "inferred", .5, False)]
    els += chip(sx + 60, sy - 60, "1988", RED, tf, 24)
    for k in range(6):
        y = 380 + 30 * k
        els.append(ln([(1250 + 30 * (k % 2), y), (1450 + 30 * (k % 2), y - 6)], round(tw + .08 * k, 2), "rgba(245,236,220,.6)", 2, dur=.4, curve=True))
    rnd = random.Random(2)
    for k in range(10):
        x, y = rnd.uniform(1300, 1650), rnd.uniform(gy - 10.5 * sc, gy - 5 * sc)
        els.append(poly([(x, y), (x + 14, y - 4), (x + 10, y + 8)], "#d6bb8c", "rgba(40,28,18,.6)", 1, round(tw + .3 + .06 * k, 2), fx="rise"))
    els += [lab(1460, 340, "flakes, on a windy day", tw + .6, BONE, 26)]
    base.update(cam=CAM, els=els)
    return base


def s34():
    """A strip of time from 3000 to 2300 BCE: Khafre's mark; the Fifth Dynasty shaded; blue rain bars keep falling after Khafre
    ('runoff after Khafre', Reader)."""
    tr = T("s34", "even Reader")
    X = lambda bce: round(250 + (3000 - bce) / 700 * 1280, 1)
    ay = 600
    els = [axis(250, 1530, ay, [(X(3000), "3000 BCE"), (X(2800), "2800"), (X(2600), "2600"), (X(2400), "2400")], -1)]
    els += [ln([(X(2500), ay), (X(2500), ay - 90)], -1, AMBER, 3, draw=False), circ(X(2500), ay, 9, AMBER, at=-1), lab(X(2500), ay - 104, "Khafre", -1, AMBER, 28)]
    els += [rect(X(2465), ay - 40, X(2325) - X(2465), 30, "rgba(242,201,142,.15)", "rgba(242,201,142,.5)", 1.5, 4, .4), lab((X(2465) + X(2325)) / 2, ay - 52, "Fifth Dynasty", .6, DIM, 24)]
    els += [rect(1250, 300, 420, 110, "#1d1712", "rgba(255,226,190,.4)", 1.5, 0, -1)] + sphinx(1265, 402, 5.0, -1, casing=False, shadow=False)
    rnd = random.Random(6)
    for k in range(34):
        x = rnd.uniform(X(2950), X(2330))
        y = rnd.uniform(200, 290) if x > 1240 else rnd.uniform(220, 420)
        els.append(ln([(x, y), (x - 6, y + 40)], round(tr + .03 * k, 2), "#9fd0ff", 2.5, dur=.3))
    els += [lab(800, 480, "runoff after Khafre", tr + 1.0, BLUE, 30), lab(800, 512, "Reader", tr + 1.2, DIM, 24)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s35():
    """Three small panes: the pit floor's weak layer relabelled 'softer rock?'; the granite and limestone joint where a chisel trims the
    limestone to the granite's rough back (arrow reversed from s26); the Sphinx's body with a natural crack across its back and a
    bracket 'one head length' along the body."""
    tw, tg, tl = T("s35", "The weak layer"), T("s35", "The temple's limestone"), T("s35", "to Lehner")
    def pane(x, at, title):
        return [rect(x, 180, 500, 520, "rgba(18,13,10,.92)", "rgba(255,236,206,.35)", 1.5, 14, at, fx="pop"), lab(x + 250, 165, title, at, DIM, 24)]
    els = pane(100, tw - .3, "under the floor") + pane(639, tg - .3, "the temple wall") + pane(1178, tl - .3, "the body")
    els += [rect(120, 330, 460, 120, "#6f5a43", at=tw - .2), rect(120, 450, 460, 140, "#8a7458", at=tw - .2), ln([(120, 330), (580, 330)], tw - .2, "#e7cfa6", 2, draw=False)]
    els += [rect(120, 330, 460, 120, "rgba(159,208,255,.25)", BLUE, 2, 0, tw, style="inferred"), lab(350, 400, "weathered?", tw + .1, BLUE, 26),
            lab(350, 640, "softer rock?", tw + .9, GOLD, 30)]
    face = [(870 - 10 * math.sin((y - 260) / 40.0) - 16, y) for y in range(260, 621, 20)]
    els += [poly([(680, 260)] + face + [(680, 620)], "#cdb184", "rgba(40,28,18,.6)", 1.5, tg - .2), poly(face + [(980, 620), (980, 260)], GRAN, "#ffd0c0", 1.5, tg - .2)]
    els += [poly([(820, 300), (836, 292), (884, 404), (872, 412)], "#d9894a", "#ffe2a8", 1.5, tg + .3, fx="pop"), arr([(780, 470), (850, 470)], tg + .6, GOLD, 3, "known", .5, False),
            lab(889, 660, "trimmed to fit", tg + .8, GOLD, 30)]
    x0, gy, sc = 1200, 520, 6.0
    els += sphinx(x0, gy, sc, tl - .2, beds=False, casing=False, shadow=False)
    els += [ln([(x0 + 60 * sc, gy - 9.7 * sc), (x0 + 59 * sc, gy - 6.5 * sc), (x0 + 61 * sc, gy - 3.5 * sc), (x0 + 60 * sc, gy)], tl + .4, "#1d1712", 4, dur=.6),
            lab(x0 + 60 * sc, gy - 12 * sc, "a great crack", tl + .6, BONE, 24)]
    els += bracket(x0 + 60 * sc, x0 + 71 * sc, gy + 30, tl + 1.0, "one head length", GOLD, up=False, size=24, ty=gy + 64)
    els += [lab(1428, 660, "the body was stretched", tl + 1.4, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


VF = View(29.9, 32.0, 28.95, 30.55, (90, 150, 820, 600))


def s36():
    """Left, a map: the Nile valley, Giza, the Fayum's lake ('first farmers, about 5400 BCE'). Right, a grain pit in section, lined with
    basketry and full of grain. Above, a strip from 7000 to 5000 BCE: an empty stretch ('no farming villages'), then the first farmers;
    on 'who carved', a dotted lilac Sphinx at 7000 BCE with a '?'."""
    tv, tf, tb, tw = T("s36", "no farming"), T("s36", "first farmers"), T("s36", "storing grain"), T("s36", "So who carved")
    v = VF
    els = [{"k": "map", "land": v.land(), "in": -1}]
    vb = [v.p(31.05, 29.0), v.p(31.15, 29.6), v.p(31.16, 30.0), v.p(31.08, 30.4), v.p(31.42, 30.4), v.p(31.36, 30.0), v.p(31.33, 29.6), v.p(31.25, 29.0)]
    els += [poly(vb, "rgba(120,170,90,.14)", "none", 0, -1, curve=True)] + nile_lines(v, -1, 6)
    els += [lab(v.p(31.3, 29.2)[0] + 14, v.p(31.3, 29.2)[1], "Nile", -1, "#9fd0ff", 26, "start", st="ital"), lab(260, 210, "northern Egypt", -1, DIM, 24)]
    fy = [v.p(30.45, 29.50), v.p(30.62, 29.53), v.p(30.82, 29.49), v.p(30.85, 29.44), v.p(30.62, 29.43), v.p(30.45, 29.45)]
    els += [poly(fy, "#3f86a8", "#9fd0ff", 1.5, -1, curve=True), lab(v.p(30.65, 29.36)[0], v.p(30.65, 29.36)[1] + 16, "Fayum", -1, "#9fd0ff", 26, st="ital")]
    gx, gy_ = v.p(31.134, 29.979)
    els += [{"k": "pin", "x": gx, "y": gy_, "t": "Giza", "c": GOLD, "in": -1, "a": "start", "lx": 18}]
    els += [rect(930, 120, 800, 690, "#191410", "rgba(255,236,206,.25)", 1.5, 16, -1)]
    ax0, ax1, ay = 1000, 1640, 230
    X = lambda bce: round(ax0 + (7000 - bce) / 2000 * (ax1 - ax0), 1)
    els += [axis(ax0, ax1, ay, [(X(7000), "7000 BCE"), (X(6000), "6000"), (X(5000), "5000")], -1)]
    els += [rect(X(7000), ay - 34, X(5400) - X(7000), 20, "rgba(245,236,220,.06)", "rgba(245,236,220,.45)", 1.5, 6, tv, style="inferred"),
            lab((X(7000) + X(5400)) / 2, ay - 46, "no farming villages", tv + .3, DIM, 24)]
    fx_, fy_ = v.p(30.75, 29.49)
    els += [circ(X(5400), ay, 9, GREEN, at=tf, fx="pop"), lab(X(5400), ay + 76, "first farmers", tf + .2, GREEN, 26), lab(X(5400), ay + 104, "about 5400 BCE", tf + .3, GREEN, 24),
            ring_(fx_, fy_, 34, tf, GREEN, 3)]
    px, py = 1320, 600
    pit = [(px - 150, py - 160), (px + 150, py - 160), (px + 120, py + 40), (px + 60, py + 90), (px - 60, py + 90), (px - 120, py + 40)]
    els += [rect(980, py - 160, 680, 220, "#6f5a43", at=tb - .4), rect(980, py - 160, 680, 220, "url(#k-speck)", at=tb - .4), poly(pit, "#2a2119", "#c9a46a", 4, tb - .2, curve=True)]
    for k in range(9):
        y = py - 140 + 26 * k
        w = 140 - 6 * k
        els.append(ln([(px - w, y), (px + w, y)], round(tb + .05 * k, 2), "#c9a46a", 2, draw=False, op=.6))
    rnd = random.Random(12)
    for k in range(70):
        x, y = rnd.uniform(px - 110, px + 110), rnd.uniform(py - 120, py + 70)
        if abs(x - px) < 120 - (y - py + 120) * .3:
            els.append(poly(E(x, y, 6, 3.5, 8), "#e9cf8a", "none", 0, round(tb + .2 + .01 * k, 2), fx="pop"))
    els += [lab(px, py + 140, "a grain pit lined with basketry", tb + .5, BONE, 24)]
    ux, uy = X(7000), ay + 120
    els += [poly([(ux - 60, uy + 30), (ux + 60, uy + 30), (ux + 60, uy + 10), (ux - 30, uy + 10), (ux - 40, uy - 14), (ux - 56, uy - 14), (ux - 60, uy)], "rgba(201,193,238,.08)",
                 LILAC, 2.5, tw, style="claimed")] + qmark(ux + 90, uy + 30, tw + .3, 70)
    return {"base": "map", "cam": CAM, "els": els}


def t_pillar(x, by, h, at, c="#cdb184"):
    """A T-shaped pillar of Gobekli Tepe in side view with a carved fox on its shaft (schematic)."""
    w = h * .2
    out = [rect(x - w / 2, by - h * .78, w, h * .78, c, "rgba(40,28,18,.6)", 1.5, 2, at, fx="pop"), rect(x - w * 1.4, by - h, w * 2.8, h * .22, c, "rgba(40,28,18,.6)", 1.5, 2, at, fx="pop")]
    out += [poly([(x - w * .3, by - h * .5), (x + w * .1, by - h * .58), (x + w * .3, by - h * .52), (x + w * .2, by - h * .44), (x - w * .2, by - h * .42)], "#8c7152", "none", 0, at + .2, fx="pop")]
    return out


def s37():
    """Two columns under one band: left 'Gobekli Tepe', a carved T-pillar standing on a layer that fills with grinding stones, flints and
    bones as named; right 'Giza', the same layer empty, a lilac dashed outline and a small '?' ('nothing found')."""
    tg, tt, ts, tf, tb, tz = (T("s37", "Göbekli Tepe"), T("s37", "they left a trail"), T("s37", "grinding stones"), T("s37", "flint tools"),
                              T("s37", "animal bones"), T("s37", "At Giza"))
    els = [lab(470, 170, "Göbekli Tepe, about 9500 BCE", tg, BONE, 30), lab(1300, 170, "Giza, the same ages", tz - .6, BONE, 30)]
    els += [rect(140, 560, 660, 150, "#5c4a37", "rgba(255,236,206,.4)", 1.5, 6, tg), rect(970, 560, 660, 150, "#5c4a37", "rgba(255,236,206,.4)", 1.5, 6, tz - .6)]
    els += t_pillar(470, 560, 330, tg + .3)
    rnd = random.Random(9)
    for k in range(12):
        x, y = rnd.uniform(170, 770), rnd.uniform(590, 690)
        els.append(poly(E(x, y, 26, 11, 14), "#9a958c", "#d9d6cc", 1.2, round(ts + .05 * k, 2), fx="pop"))
    for k in range(14):
        x, y = rnd.uniform(170, 770), rnd.uniform(590, 690)
        els.append(poly([(x, y - 10), (x + 9, y + 8), (x - 9, y + 8)], "#3a3a40", "#c9c9d4", 1, round(tf + .04 * k, 2), fx="pop"))
    for k in range(10):
        x, y = rnd.uniform(170, 770), rnd.uniform(590, 690)
        els += [ln([(x - 16, y), (x + 16, y)], round(tb + .05 * k, 2), "#efe6d2", 5, draw=False), circ(x - 18, y, 5, "#efe6d2", at=round(tb + .05 * k, 2)),
                circ(x + 18, y, 5, "#efe6d2", at=round(tb + .05 * k, 2))]
    els += [lab(470, 750, "a trail of work", tt + .2, GOLD, 28)]
    els += [rect(990, 580, 620, 110, "none", LILAC, 2.5, 6, tz, style="claimed")] + qmark(1300, 660, tz + .3, 70) + [lab(1300, 750, "nothing found", tz + .5, LILAC, 28)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s38():
    """A blackboard: the sun's light wipes it clean; then darkness and tally marks appear one by one ('natural radiation'); beside it a
    block set in a wall, its hidden face carrying the same marks: 'when it last saw the sun'."""
    tsun, tdark, tm = T("s38", "Sunlight wipes"), T("s38", "in the dark"), T("s38", "Measure the")
    bx, by, bw, bh = 180, 200, 640, 400
    els = [rect(bx - 16, by - 16, bw + 32, bh + 32, "#6b4a30", "#a07850", 2, 10, -1), rect(bx, by, bw, bh, "#22342a", at=-1)]
    rnd = random.Random(5)
    for k in range(10):
        x, y = rnd.uniform(bx + 30, bx + bw - 60), rnd.uniform(by + 30, by + bh - 40)
        els.append(ln([(x, y), (x + 40, y + 6)], -1, "rgba(240,240,230,.6)", 3, draw=False))
    els += [circ(bx - 60, by - 40, 34, "#ffe2b4", at=tsun - .2, fx="pop"), gl(bx - 60, by - 40, 120, tsun - .2, .7, "sun"),
            rect(bx, by, bw, bh, "#22342a", at=tsun + .3, fx="fill", dur=1.2), lab(bx + bw / 2, by + bh + 50, "light wipes it clean", tsun + .8, "#ffe2b4", 26)]
    els += [rect(bx - 20, by - 20, bw + 40, bh + 40, "rgba(8,8,14,.55)", at=tdark, op=1)]
    for k in range(20):
        x = bx + 60 + (k % 10) * 54
        y = by + 90 + (k // 10) * 140
        els.append(ln([(x, y), (x + 6, y + 70)], round(tdark + .3 + .1 * k, 2), "#f0f0e6", 4, dur=.2))
    els += [lab(bx + bw / 2, by - 40, "natural radiation, slowly", tdark + .6, BONE, 26)]
    wx, wy = 1000, 200
    for r in range(3):
        for c in range(3):
            els.append(rect(wx + c * 200 + (60 if r == 1 else 0), wy + r * 120, 196, 116, "#cdb184", "rgba(40,28,18,.6)", 1.2, 2, -1))
    els += [rect(wx + 260, wy + 120, 196, 116, "#2a2119", "rgba(255,236,206,.5)", 2, 2, tm - .4)]
    for k in range(6):
        els.append(ln([(wx + 290 + 26 * k, wy + 150), (wx + 294 + 26 * k, wy + 205)], round(tm + .1 * k, 2), "#f0f0e6", 3, dur=.2))
    els += [lab(wx + 358, wy + 420, "when it last saw the sun", tm + .8, GOLD, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s39():
    """Timeline 8000 BCE to 1 CE: four dots with error bars pop (3100, 2740, 2220, 1190 BCE); Khafre's mark; 'first farmers, about 5400
    BCE' and Schoch's dimmed band far to the left; a bracket shows the gap."""
    td, tn = T("s39", "four stones"), T("s39", "None came")
    X = lambda bce: round(180 + (8000 - bce) / 8000 * 1420, 1)
    ay = 600
    els = [axis(180, 1600, ay, [(X(8000), "8000 BCE"), (X(6000), "6000"), (X(4000), "4000"), (X(2000), "2000"), (1600, "1 CE")], -1)]
    els += [ln([(X(2500), ay), (X(2500), ay - 60)], -1, AMBER, 3, draw=False), lab(X(2500), ay + 60, "Khafre", -1, AMBER, 24)]
    els += [rect(X(7000), ay - 36, X(5000) - X(7000), 18, "rgba(159,208,255,.3)", at=-1), lab(X(6000), ay - 50, "Schoch", -1, "rgba(159,208,255,.75)", 24)]
    els += [circ(X(5400), ay, 8, GREEN, at=-1), ln([(X(5400), ay + 8), (X(5400), ay + 66)], -1, GREEN, 1.5, draw=False), lab(X(5400), ay + 92, "first farmers", -1, GREEN, 24)]
    dates = [(3100, 540, 330), (2740, 640, 380), (2220, 220, 430), (1190, 340, 480)]
    for k, (c, e, y) in enumerate(dates):
        at = round(td + .5 + .35 * k, 2)
        els += [ln([(X(c + e), y), (X(c - e), y)], at, GOLD, 3, dur=.3), ln([(X(c + e), y - 8), (X(c + e), y + 8)], at, GOLD, 2, draw=False),
                ln([(X(c - e), y - 8), (X(c - e), y + 8)], at, GOLD, 2, draw=False), circ(X(c), y, 9, GOLD, "#fff4dc", 2, at, fx="pop")]
    els += [lab(X(2200), 290, "light dates, Sphinx Temple", td + 1.8, GOLD, 26)]
    els += bracket(X(5400), X(3640), 520, tn, "the gap", BONE, up=True, size=26, ty=556)
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}



# ================================================================== CHAPTER 5 · Dreams, patches and probes
def s40_add():
    """Back at the buried lion: where the prince slept, he now stands, crowned ('Thutmose IV, about 1400 BCE'); amber arrows push the
    sand away."""
    t = T("s40", "He became king")
    tb = T("s40", "kept his side")
    x0, sc = 354, 26.0
    sx, sy = x0 - 7.4 * sc, 632
    out = [poly(E(sx + 80, sy - 4, 100, 26, 24), "#5d4c3c", "none", 0, t - .2), poly(E(sx + 80, sy + 4, 120, 16, 24), "rgba(220,214,240,.16)", "none", 0, t - .2)]
    x = sx + 70
    out += [person(x, sy + 6, 150, t, "#e8d6b8"), gl(x, sy - 120, 150, t, .45, "lamp")] + crown(x + 2, sy - 132, 66, t + .3)
    out += chip(x + 60, sy + 60, "Thutmose IV, about 1400 BCE", AMBER, t + .5, 24)
    for k, (a, b) in enumerate((((760, 586), (640, 626)), ((1000, 540), (1140, 596)), ((1260, 520), (1440, 560)))):
        out.append(arr([a, b], round(tb + .2 * k, 2), AMBER, 3, "known", .5, False))
    return out


def s41():
    """From above (north up, the face to the east): the pit cleared, the Sphinx in it, its body given a skin of limestone blocks; a
    rounded mudbrick wall draws round the pit ('mudbrick, over 8 m high'); beside it a royal name in its oval frame, the same shape."""
    tc, tw, tr = T("s41", "new skin"), T("s41", "mudbrick walls"), T("s41", "royal name")
    k, cx, cy = 5.6, 640, 470
    P = lambda e, n: (cx + e * k, cy - n * k)
    els = [rect(80, 150, 1150, 640, "#a88a64", at=-1, op=.55), rect(80, 150, 1150, 640, "url(#k-speck)", at=-1, op=.55)]
    els += [poly([P(-62, 33), P(54, 33), P(54, -33), P(-62, -33)], "#2a2119", "rgba(242,220,180,.6)", 1.8, -1)]
    els += plan_sphinx(cx, cy, k, -1)
    for j in range(16):
        e = -34 + j * 3.6
        els.append(ln([P(e, 8.6), P(e, 5.8)], round(tc + .04 * j, 2), "#f4e3c2", 2, draw=False))
        els.append(ln([P(e, -8.6), P(e, -5.8)], round(tc + .04 * j, 2), "#f4e3c2", 2, draw=False))
    els += [ln([P(-34, 8.4), P(20, 8.4)], tc, "#f4e3c2", 2.5, dur=.8), ln([P(-34, -8.4), P(20, -8.4)], tc, "#f4e3c2", 2.5, dur=.8),
            lab(cx - 10 * k, cy + 15 * k + 30, "a new skin of stone", tc + .6, "#f4e3c2", 26)]
    ov = []
    for a in range(-90, 91, 10):
        ov.append(P(48 + 40 * math.cos(math.radians(a)), 40 * math.sin(math.radians(-a))))
    for a in range(90, 271, 10):
        ov.append(P(-54 + 40 * math.cos(math.radians(a)), 40 * math.sin(math.radians(-a))))
    ov.append(ov[0])
    els += [ln(ov, tw, MUD, 14, dur=1.6, op=.95), ln(ov, tw + .2, "#c08e60", 3, dur=1.6)]
    els += [lab(cx, cy - 40 * k - 24, "mudbrick, over 8 m high", tw + 1.2, "#e0b48a", 28)]
    els += [{"k": "line", "p": [[1180, 760], [1180, 700]], "c": "#e9dccb", "w": 2, "in": -1}, lab(1180, 690, "N", -1, "#e9dccb", 22)]
    qx, qy = 1460, 460
    co = []
    for a in range(0, 361, 10):
        r = math.radians(a)
        co.append((qx + 90 * math.cos(r) * (1 + .18 * abs(math.cos(r)) ** 6) * .0 + 70 * math.cos(r), qy + 190 * math.sin(r)))
    els += [poly(co, "rgba(232,184,122,.12)", GOLD, 5, tr, fx="pop"), ln([(qx - 70, qy + 205), (qx + 70, qy + 205)], tr + .2, GOLD, 6, draw=False),
            {"k": "glyphs", "x": qx - 40, "y": qy - 160, "w": 80, "h": 300, "rows": 5, "cols": 1, "kind": "hieroglyph", "c": GOLD, "in": round(tr + .3, 2)},
            lab(qx, qy + 260, "a royal name, in its frame", tr + .5, GOLD, 26)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def sphinx_front(cx, gy, s, at=-1):
    """The Great Sphinx seen from the front (from the east), s units a metre: the striped nemes, the face without its nose (ears,
    eyes, lips), the chest in the beds, the two forepaws towards us, the body's shoulders behind."""
    X = lambda m: cx + m * s
    Y = lambda m: gy - m * s
    out = [poly([(X(-9.5), Y(0)), (X(-9.5), Y(8.6)), (X(-9.0), Y(10.2)), (X(-8.0), Y(11.3)), (X(-6.6), Y(12.2)), (X(6.6), Y(12.2)), (X(8.0), Y(11.3)), (X(9.0), Y(10.2)),
                 (X(9.5), Y(8.6)), (X(9.5), Y(0))], "#7d6448", "rgba(255,236,206,.4)", 1.5, at)]
    chest = [(X(-5.4), Y(0)), (X(-5.6), Y(4.0)), (X(-6.0), Y(7.0)), (X(-5.6), Y(9.4)), (X(-4.4), Y(11.2)), (X(4.4), Y(11.2)), (X(5.6), Y(9.4)), (X(6.0), Y(7.0)),
             (X(5.6), Y(4.0)), (X(5.4), Y(0))]
    out += [poly(chest, "url(#k-stoneC)", "rgba(255,236,206,.5)", 1.5, at, curve=True)]
    for y0, y1, kind in BEDS:
        if y1 < 10.5:
            b = hband([(x_ - cx, gy - y_) for x_, y_ in chest], y0 * s, y1 * s)
            if len(b) > 2:
                out.append(poly([(cx + a, gy - c) for a, c in b], "#6b553e" if kind == "soft" else "#f2dfbb", "none", 0, at, op=.36 if kind == "soft" else .14))
    for sx in (-1, 1):
        paw = [(X(sx * 2.4), Y(0)), (X(sx * 2.5), Y(2.2)), (X(sx * 3.4), Y(2.7)), (X(sx * 6.0), Y(2.7)), (X(sx * 6.9), Y(2.2)), (X(sx * 7.0), Y(0))]
        out += [poly(paw, "#d6bd92", "rgba(255,236,206,.6)", 1.5, at), poly(paw, "url(#k-blocks)", "none", 0, at, op=.3)]
        for t in range(1, 4):
            xx = X(sx * (2.5 + 4.4 * t / 4))
            out.append(ln([(xx, Y(0)), (xx, Y(1.5))], at, "rgba(40,28,18,.5)", 1.6, draw=False))
    nem = [(X(-3.3), Y(20.0)), (X(-4.4), Y(19.2)), (X(-4.9), Y(17.6)), (X(-5.1), Y(15.4)), (X(-5.6), Y(13.6)), (X(-6.7), Y(11.6)), (X(-6.9), Y(10.4)), (X(-3.1), Y(10.4)),
           (X(-3.0), Y(12.6)), (X(3.0), Y(12.6)), (X(3.1), Y(10.4)), (X(6.9), Y(10.4)), (X(6.7), Y(11.6)), (X(5.6), Y(13.6)), (X(5.1), Y(15.4)), (X(4.9), Y(17.6)),
           (X(4.4), Y(19.2)), (X(3.3), Y(20.0))]
    out += [rect(X(-3.1), Y(12.8), 6.2 * s, 2.6 * s, "#cdb287", at=at), poly(nem, "#dcc497", "rgba(255,236,206,.6)", 1.5, at)]
    rel_ = [(x_ - cx, gy - y_) for x_, y_ in nem]
    yy, k = 10.4, 0
    while yy < 19.9:
        if k % 2 == 0:
            for lo, hi in hspans(rel_, (yy + .25) * s):
                if hi - lo > 4:
                    out.append(rect(cx + lo, gy - (yy + .5) * s, hi - lo, .5 * s, "#7a5f43", at=at, op=.5))
        yy += .5; k += 1
    face = [(X(-2.45), Y(18.7)), (X(-2.55), Y(16.6)), (X(-2.45), Y(14.6)), (X(-2.0), Y(13.3)), (X(-1.2), Y(12.5)), (X(0), Y(12.25)), (X(1.2), Y(12.5)), (X(2.0), Y(13.3)),
            (X(2.45), Y(14.6)), (X(2.55), Y(16.6)), (X(2.45), Y(18.7))]
    out += [poly(face, "url(#k-stoneC)", "rgba(60,44,30,.55)", 1.5, at, curve=True), poly([(X(-2.4), Y(16.0)), (X(-1.0), Y(15.6)), (X(-1.4), Y(13.6)), (X(-2.2), Y(14.4))],
                                                                                            "rgba(255,244,222,.35)", "none", 0, at, curve=True)]
    out += [rect(X(-3.3), Y(19.3), 6.6 * s, .55 * s, "#efe2c4", "rgba(60,44,30,.5)", 1, 2, at)]
    for sx in (-1, 1):
        out += [poly([(X(sx * 2.5), Y(16.9)), (X(sx * 3.05), Y(16.6)), (X(sx * 3.1), Y(15.2)), (X(sx * 2.55), Y(14.8))], "#c9ad80", "rgba(60,44,30,.6)", 1.2, at, curve=True)]
        out += [poly([(X(sx * .45), Y(16.32)), (X(sx * 1.0), Y(16.52)), (X(sx * 1.6), Y(16.3)), (X(sx * 1.0), Y(16.15))], "#3a2c1e", "none", 0, at),
                ln([(X(sx * 1.6), Y(16.3)), (X(sx * 2.0), Y(16.45))], at, "#3a2c1e", 1.6, draw=False),
                ln([(X(sx * .4), Y(16.95)), (X(sx * 1.1), Y(17.15)), (X(sx * 1.8), Y(16.95))], at, "rgba(58,44,30,.65)", 1.6, draw=False, curve=True)]
    out += [poly([(X(-.5), Y(16.1)), (X(.5), Y(16.1)), (X(.7), Y(14.75)), (X(.2), Y(14.6)), (X(-.3), Y(14.75)), (X(-.7), Y(14.8))], "#a7865c", "rgba(255,240,214,.4)", 1, at),
            poly([(X(-.95), Y(13.75)), (X(-.3), Y(13.95)), (X(0), Y(13.85)), (X(.3), Y(13.95)), (X(.95), Y(13.75)), (X(.3), Y(13.6)), (X(-.3), Y(13.6))], "#b9946a", "none", 0, at),
            poly([(X(-.8), Y(13.6)), (X(.8), Y(13.6)), (X(.4), Y(13.25)), (X(-.4), Y(13.25))], "#c9a67a", "none", 0, at, curve=True)]
    out += [rect(X(-.3), Y(20.1), .6 * s, .9 * s, "#b39367", at=at, op=.8)]
    return out


def stele_face(x, y, w, h, at, scene=True):
    """The Dream Stele seen face on: a round-topped granite slab; in its lunette two sphinxes back to back and the king offering; below,
    rows of text."""
    top = [(x + w / 2 + w / 2 * math.cos(math.radians(a)), y + w * .32 - w * .32 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    out = [poly([(x + w, y + h)] + top + [(x, y + h)], "#6d6a6e", "#c9c4cc", 1.5, at)]
    if scene:
        cy = y + w * .3
        for sxn in (-1, 1):
            bx = x + w / 2 + sxn * w * .2
            out += [rect(bx - w * .12, cy, w * .24, w * .05, "#4a4750", at=at),
                    poly([(bx - sxn * w * .11, cy), (bx - sxn * w * .11, cy - w * .05), (bx + sxn * w * .06, cy - w * .06), (bx + sxn * w * .08, cy - w * .12),
                          (bx + sxn * w * .12, cy - w * .1), (bx + sxn * w * .12, cy)], "#3d3a42", "none", 0, at)]
            out += [person(round(x + w / 2 + sxn * w * .43, 1), round(cy + w * .05, 1), round(w * .17, 1), at, "#3d3a42") | {"in": at}]
        out += [ln([(x + w * .06, cy + w * .09), (x + w * .94, cy + w * .09)], at, "#4a4750", 1.5, draw=False)]
    for r in range(14):
        yy = y + w * .48 + r * (h - w * .52) / 14
        out.append(ln([(x + w * .1, yy), (x + w * (.9 - .03 * (r % 3)), yy)], at, "#4a4750", 1.6, draw=False, op=.8))
    return out


FS, FGY = 30.0, 760                          # the front view in s42: 30 units a metre, the floor at y 760
ST = dict(w=round(2.2 * FS), h=round(3.6 * FS))   # the stele: 3.6 m tall (and about 2.2 m wide, schematic)


def s42():
    """Front view between the forepaws (from the east): the Sphinx face on; the Dream Stele between the paws, round-topped granite with
    its scene and text, 3.6 m tall beside two people of 1.7 m. Then, on a plate at right, the same slab lying across two jambs as the
    lintel of a doorway: 'once a door lintel'."""
    ts, tr = T("s42", "slab of granite"), T("s42", "recycled")
    cx, gy, sc = 760, FGY, FS
    els = [rect(-60, gy, 1900, 400, "#7d6650", at=-1), rect(-60, gy - 9 * sc, 1900, 9 * sc, "#4e4034", at=-1), gl(cx, 400, 560, -1, .2, "lamp")]
    els += sphinx_front(cx, gy, sc, -1)
    w, h = ST["w"], ST["h"]
    x, y = cx - w / 2, gy - h
    els += [gl(cx, y + 40, 150, ts, .45, "lamp")] + stele_face(x, y, w, h, ts)
    els += [person(x - 36, gy, 1.7 * sc, ts + .3, "#2a2018"), person(x + w + 36, gy, 1.7 * sc, ts + .4, "#2a2018")]
    els += [ln([(cx + w / 2 + 4, y + 14), (cx + 150, y - 70)], ts + .5, GOLD, 1.5, dur=.3), lab(cx + 156, y - 76, "the Dream Stele", ts + .6, GOLD, 28, "start")]
    px, py = 1290, 250
    els += [rect(px, py, 380, 400, "rgba(18,13,10,.9)", "rgba(255,236,206,.3)", 1.5, 14, tr - .3, fx="pop")]
    jx0, jx1, jt, jb = px + 100, px + 280, py + 150, py + 360
    els += [rect(jx0 - 30, jt, 30, jb - jt, "none", "rgba(245,236,220,.75)", 2.5, 2, tr, style="claimed"), rect(jx1, jt, 30, jb - jt, "none", "rgba(245,236,220,.75)", 2.5, 2, tr, style="claimed"),
            rect(jx0 - 50, jt - h * .62, (jx1 + 50) - (jx0 - 50), h * .62, "#6d6a6e", "#c9c4cc", 2, 3, tr + .5, fx="rise"),
            lab(px + 190, py + 50, "once a door lintel", tr + .7, BONE, 28), lab(px + 190, py + 390, "in one of Khafre's temples", tr + .9, DIM, 22)]
    els += [arr([(x + w + 10, y + 20), (px - 10, jt - h * .3)], tr + .3, GOLD, 2.5, "inferred", .8)]
    return {"base": "sky", "tod": "dawn", "ground": round(gy - 9 * sc), "sun": [120, 300, 24], "cam": CAM, "els": els}


def s43_add():
    """Close on the stele: a broken line glows with a fragment of a royal name ('Khaf...', copied in the 1800s); the stone round it
    flakes and falls away, leaving a blank ('flaked away'); 'a hint, not a signature'."""
    tc, tf, th = T("s43", "show part"), T("s43", "flaked away"), T("s43", "A hint")
    w, h = ST["w"], ST["h"]
    x, y = 760 - w / 2, FGY - h
    ly = y + w * .48 + 7 * (h - w * .52) / 14
    out = [rect(x + w * .1, ly - 4, w * .8, 8, "rgba(242,201,142,.45)", GOLD, 1, 1, tc, fx="pop"), ln([(x + w * .9, ly), (x + w + 22, ly - 40)], tc + .2, GOLD, 1.2, dur=.3),
           lab(x + w + 26, ly - 44, "Khaf...", tc + .3, GOLD, 32, "start", st="serif"), lab(x + w + 26, ly - 30, "copied in the 1800s", tc + .5, BONE, 22, "start")]
    rnd = random.Random(3)
    for k in range(10):
        fx_ = x + w * .15 + rnd.uniform(0, w * .7)
        out.append(poly([(fx_, ly + 6), (fx_ + 4, ly + 5), (fx_ + 3, ly + 9)], "#8a868e", "none", 0, round(tf + .05 * k, 2), fx="rise"))
    out += [rect(x + w * .08, ly - 5, w * .84, 10, "#56535a", at=tf + .3), ln([(x + w * .1, ly), (x - 22, ly - 40)], tf + .5, BONE, 1.2, dur=.3),
            lab(x - 26, ly - 44, "flaked away", tf + .6, BONE, 24, "end")]
    out += chip(760, y - 22, "a hint, not a signature", AMBER, th, 26, z=2.6)
    return out


def s44():
    """The Sphinx in profile with patches popping along its body in tones as each age is named ('about 1400 BCE', 'about 600 BCE',
    'Greek and Roman', '1980s and 1990s'); at right a clipboard 'medical record' whose lines tick one by one."""
    t1, t2, t3, t4, tm = T("s44", "patched it"), T("s44", "six hundred"), T("s44", "Greek and Roman"), T("s44", "nineteen eighties"), T("s44", "medical record")
    x0, gy, sc = 110, 730, 15.0
    els = [rect(-60, gy, 1900, 400, "#2a211a", at=-1), gl(560, 470, 420, -1, .16, "lamp")]
    els += sphinx(x0, gy, sc, -1, casing=False)
    def patch(xa, xb, ya, yb, c, at):
        return rect(x0 + xa * sc, gy - yb * sc, (xb - xa) * sc - 2, (yb - ya) * sc, c, "rgba(40,28,18,.6)", 1.2, 1, at, fx="pop")
    ages = [(t1, "#e2cda4", [(2, 7, 0, 2.4), (7, 12, 0, 2.4), (16, 22, 0, 3.2), (22, 28, 0, 3.2), (28, 34, 0, 3.0)], "about 1400 BCE"),
            (t2, "#b9b0a2", [(36, 39, 1.0, 3.6), (40, 43, 0, 2.4), (6, 9, 2.4, 2.8)], "about 600 BCE"),
            (t3, "#f2eee6", [(44, 46, 0, 1.6), (46.2, 48, 0, 1.6), (48.2, 50, 0, 1.6), (13.2, 14.6, 1.0, 2.8)], "Greek and Roman"),
            (t4, "#d9cbb0", [(52, 56, 0, 2.2), (60, 64, 0, 3.0), (66, 70, 0, 2.6)], "1980s and 1990s")]
    for k, (t, c, boxes, name) in enumerate(ages):
        for j, (xa, xb, ya, yb) in enumerate(boxes):
            els.append(patch(xa, xb, ya, yb, c, round(t + .08 * j, 2)))
        ly = 170 + 54 * k
        els += [rect(x0 + 2, ly - 22, 34, 26, c, "rgba(40,28,18,.6)", 1.2, 2, t, fx="pop"), lab(x0 + 50, ly, name, t + .1, BONE, 26, "start")]
    cx, cy = 1450, 390
    els += [rect(cx - 150, cy - 220, 300, 400, "#e9dcc4", "#fff6e6", 2, 10, tm - .4, fx="pop"), rect(cx - 50, cy - 236, 100, 30, "#8c7152", at=tm - .4, fx="pop"),
            lab(cx, cy - 170, "medical record", tm - .2, INK, 26, halo=False)]
    for k in range(5):
        y = cy - 110 + 56 * k
        els += [ln([(cx - 100, y), (cx + 90, y)], round(tm - .3 + .05 * k, 2), "#8c7152", 2, draw=False), tick(cx - 120, y - 6, round(tm + .2 + .15 * k, 2), "#3a8a5a", .6, 4)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


def s45():
    """A section under the Sphinx: sounding fans from several spots on the floor ('since 1978'); two thin drill holes go down, a camera
    at each bottom finds a hairline crack ('natural cracks'); a groundwater test hole slants from beside the paws under the body ('2009',
    Hadingham 2010; Heritage Key 2011), clear of the drawn hollow, since no report says whether any hole crossed it; under the front
    paws a lilac dashed hollow with a '?' ('1991: a hollow')."""
    to, ts, td, tw, th = T("s45", "Others have"), T("s45", "Since nineteen"), T("s45", "Where drills"), T("s45", "one angled"), T("s45", "Whether any")
    x0, gy, sc = 380, 420, 13.0
    els = [rect(-60, -100, 1900, gy + 100, "#1c1822", at=-1), rect(-60, gy, 1900, 700, "#6f5a43", at=-1), rect(-60, gy, 1900, 700, "url(#k-speck)", at=-1),
           ln([(-60, gy), (1860, gy)], -1, "#e7cfa6", 2.4, draw=False)]
    els += sphinx(x0, gy, sc, -1, shadow=False)
    els += [lab(120, gy + 40, "the floor", -1, DIM, 24, "start")]
    sx0, sy0, sx1, sy1 = 600, gy, 860, gy + 230
    els += [ln([(sx0, sy0), (sx1, sy1)], tw, BONE, 4, dur=.8), rect(sx1 - 12, sy1 - 8, 24, 18, "#8a8a90", "#e9dccb", 1.5, 3, tw + .8, fx="pop"),
            ln([(sx1 - 34, sy1 + 30), (sx1 - 12, sy1 + 24), (sx1 + 2, sy1 + 36), (sx1 + 24, sy1 + 28)], tw + 1.0, "#1d1712", 2.5, dur=.4)]
    els += chip(sx1 + 92, sy1 + 4, "2009", AMBER, tw + .4, 24)
    for k, fx_ in enumerate((240, 760, 1150, 1500)):
        els.append({"k": "fan", "x": fx_, "y": gy, "a0": 60, "a1": 120, "r": 200, "n": 9, "in": round(ts + .3 * k, 2), "fx": "fade"})
    els += chip(1500, 180, "since 1978", AMBER, ts + .2, 24) + [lab(1500, 240, "radar and sound", ts + .6, BLUE, 26)]
    for k, dx in enumerate((1080, 1640)):
        at = round(td + .3 * k, 2)
        els += [ln([(dx, gy), (dx, gy + 260)], at, BONE, 4, dur=.6), rect(dx - 12, gy + 252, 24, 18, "#8a8a90", "#e9dccb", 1.5, 3, at + .6, fx="pop"),
                ln([(dx - 30, gy + 290), (dx - 8, gy + 284), (dx + 6, gy + 296), (dx + 28, gy + 288)], at + .8, "#1d1712", 2.5, dur=.4)]
    els += [lab(1360, gy + 340, "natural cracks", T("s45", "natural rock"), BONE, 26)]
    hx, hy = x0 + 6 * sc, gy + 120
    els += [poly(E(hx, hy, 110, 44, 24), "rgba(201,193,238,.12)", LILAC, 3, th, style="claimed"), lab(hx, hy + 84, "1991: a hollow", th + .4, LILAC, 26)]
    els += qmark(hx, hy + 22, th + .3, 54, LILAC, False)
    return {"base": "dark", "cam": CAM, "els": els}


# ================================================================== CHAPTER 6 · The weighing
LROWS = [200, 315, 430, 545]


def lrow(k, at, pic, text, grade=None, gt=None, gc=None):
    y = LROWS[k]
    out = [rect(140, y - 50, 1500, 100, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 12, at, fx="pop"), lab(300, y + 11, text, at + .1, BONE, 30, "start")]
    out += pic(215, y, at + .1)
    if grade:
        out += chip(1180, y, grade, gc, gt, 28, "start")
    return out


def pic_quarry(x, y, at):
    return [rect(x - 50, y - 30, 100, 60, "#a88a64", at=at, fx="pop"), poly([(x - 40, y - 20), (x + 30, y - 20), (x + 30, y + 20), (x - 40, y + 20), (x - 40, y + 10), (x + 18, y + 10),
                                                                            (x + 18, y - 10), (x - 40, y - 10)], "#1d1712", at=at + .05, fx="pop"),
            rect(x - 26, y - 6, 34, 12, "#e2cda4", at=at + .1, fx="pop")]


def pic_pyramid(x, y, at):
    return [poly([(x - 40, y + 26), (x - 8, y - 30), (x + 24, y + 26)], "#dcc497", "rgba(255,236,206,.6)", 1.5, at, fx="pop"), ln([(x + 24, y + 20), (x + 52, y + 30)], at, "#e2c79c", 3, draw=False)]


def pic_tl(x, y, at):
    return [ln([(x - 48, y + 8), (x + 48, y + 8)], at, BONE, 2, draw=False), rect(x + 6, y - 6, 26, 10, GREEN, at=at, fx="pop"), circ(x + 34, y + 8, 5, AMBER, at=at, fx="pop")]


def pic_old(x, y, at):
    return [poly([(x - 46, y + 20), (x + 46, y + 20), (x + 46, y + 4), (x - 18, y + 4), (x - 24, y - 16), (x - 40, y - 16), (x - 46, y)], "rgba(201,193,238,.1)", LILAC, 2, at, style="claimed"),
            lab(x + 30, y - 10, "?", at, LILAC, 34, st="serif")]


def s46():
    """The ledger fills row by row: 'cut from the rock, quarry to temple' Established; 'Khafre's works, about 2500 BCE' Strong evidence
    (small tag 'Khufu or Djedefre: decades')."""
    t1, g1 = T("s46", "Carved from the living"), T("s46", "established")
    t2, g2, td = T("s46", "Carved in Khafre's"), T("s46", "strong evidence"), T("s46", "Khufu or")
    els = [rect(110, 135, 1560, 480, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    els += lrow(0, t1, pic_quarry, "cut from the rock, its quarry fed the temple", "Established", g1, GRADE["established"])
    els += lrow(1, t2, pic_pyramid, "carved in Khafre's works, about 2500 BCE", "Strong evidence", g2, GRADE["strong"])
    els += [lab(1180, LROWS[1] + 46, "Khufu or Djedefre: decades", td, DIM, 22, "start")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s47_add():
    """Rows 3 and 4: 'a start a few centuries earlier' Open question; 'thousands of years before the pharaohs' Awaiting evidence."""
    t3, g3 = T("s47", "A start a few"), T("s47", "Open question")
    t4, g4 = T("s47", "A Sphinx carved"), T("s47", "Awaiting evidence")
    els = lrow(2, t3, pic_tl, "a start a few centuries earlier", "Open question", g3, GRADE["open"])
    els += lrow(3, t4, pic_old, "thousands of years before the pharaohs", "Awaiting evidence", g4, GRADE["awaiting"])
    els += [gl(1330, LROWS[3], 220, g4, .35, "lamp")]
    return els


def s48_add():
    """Under row 4: a balance, 'weathering' level with 'salt, damp sand, fast decay'; the dated traces line up under 'the pyramid age';
    a small clock with uneven hands: 'a poor clock'."""
    tw, tp, tc = T("s48", "Its case rests"), T("s48", "every trace"), T("s48", "makes a poor")
    y = 740
    out = [ln([(360, y), (360, y - 60)], tw, "#8c7152", 6, draw=False), ln([(230, y - 60), (490, y - 60)], tw, BONE, 4, draw=False), circ(360, y - 60, 7, GOLD, at=tw)]
    out += [lab(230, y - 80, "weathering", tw + .2, LILAC, 24), lab(490, y - 80, "salt, sand, decay", tw + .4, BONE, 24)]
    for k, (ix, t) in enumerate(((760, "jar"), (870, "hammer"), (980, "light dates"))):
        out += [circ(ix, y - 50, 16, "#cdb184", "rgba(40,28,18,.6)", 1.5, round(tp + .2 * k, 2), fx="pop"), lab(ix, y - 10, t, round(tp + .2 * k + .1, 2), DIM, 20)]
    out += chip(870, y - 110, "the pyramid age", AMBER, tp + .8, 24)
    cx, cy = 1340, y - 50
    out += [circ(cx, cy, 44, "rgba(18,13,10,.6)", BONE, 2.5, tc, fx="pop")]
    for k in range(5):
        a = math.radians(-90 + 63 * k)
        out.append(ln([(cx, cy), (cx + 34 * math.cos(a), cy + 34 * math.sin(a))], round(tc + .1 * k, 2), BONE, 3, draw=False, op=round(.3 + .1 * (k % 3), 2)))
    out += [lab(cx + 70, cy + 8, "a poor clock", tc + .4, BONE, 26, "start")]
    return out


def s49():
    """Four 'wanted' items in lilac dashed outline, popping as named: charcoal, a tool and a pot under a weathered crust ('sealed and
    datable'); a stone face with a light-dating sample ('more light dates'); a hearth with tools ('a camp of that age'); a narrow drill
    over the hollow and an open data file ('one drill hole, open data')."""
    t1, t2, t3, t4 = T("s49", "Something datable"), T("s49", "More light"), T("s49", "A camp of"), T("s49", "And for the hollow")
    els = [gl(889, 420, 700, .1, .18, "lamp")]
    def card(x, at, title):
        return [rect(x - 180, 200, 360, 420, "rgba(201,193,238,.06)", LILAC, 2.5, 18, at, fx="pop", style="claimed"), lab(x, 680, title, at + .4, LILAC, 26)]
    xs = (260, 660, 1060, 1460)
    els += card(xs[0], t1, "sealed and datable")
    els += [rect(xs[0] - 140, 470, 280, 110, "#7d6448", at=t1 + .1), rect(xs[0] - 140, 440, 280, 34, "#b39773", "rgba(255,236,206,.5)", 1.5, 0, t1 + .1),
            poly(E(xs[0] - 70, 520, 22, 14, 12), "#1d1712", "none", 0, t1 + .3, fx="pop"), poly(jar_profile(xs[0] + 10, 560, 80), "#b07a4e", "#e9b98a", 1.5, t1 + .4, fx="pop"),
            poly(E(xs[0] + 80, 530, 26, 18, 14), "#8f8f8a", "#d9d6cc", 1.5, t1 + .5, fx="pop", curve=True)]
    els += card(xs[1], t2, "more light dates")
    els += [rect(xs[1] - 120, 300, 240, 260, "#cdb184", "rgba(40,28,18,.6)", 1.5, 2, t2 + .1), circ(xs[1], 430, 40, "none", GOLD, 3, t2 + .3, fx="pop"),
            gl(xs[1], 430, 70, t2 + .3, .5, "lamp")]
    els += card(xs[2], t3, "a camp of that age")
    hx, hy = xs[2], 548
    ring = [(k, math.pi * k / 5) for k in range(10)]
    stone = lambda k, a: poly(E(hx + 58 * math.cos(a), hy + 16 * math.sin(a), 13, 8, 10), "#6d665c", "#bdb6a8", 1, round(t3 + .1 + .03 * k, 2), fx="pop")
    els += [gl(hx, hy - 40, 100, t3 + .2, .7, "fire")] + [stone(k, a) for k, a in ring if math.sin(a) <= 0]
    els += [poly([(hx - 32, hy), (hx - 24, hy - 38), (hx - 9, hy - 28), (hx, hy - 78), (hx + 11, hy - 32), (hx + 24, hy - 50), (hx + 32, hy)],
                 "rgba(255,160,90,.75)", "none", 0, t3 + .2, fx="pop"),
            poly([(hx - 14, hy), (hx - 6, hy - 30), (hx + 2, hy - 18), (hx + 14, hy)], "rgba(255,226,180,.85)", "none", 0, t3 + .3, fx="pop")]
    els += [stone(k, a) for k, a in ring if math.sin(a) > 0]
    els += [poly([(hx - 130, 586), (hx - 117, 556), (hx - 104, 586)], "#3a3a40", "#c9c9d4", 1, t3 + .5, fx="pop"),
            poly([(hx - 96, 590), (hx - 87, 568), (hx - 78, 590)], "#3a3a40", "#c9c9d4", 1, t3 + .55, fx="pop"),
            poly(E(hx + 112, 580, 34, 13, 16), "#9a958c", "#d9d6cc", 1.2, t3 + .6, fx="pop")]
    els += card(xs[3], t4, "one drill hole, open data")
    els += [ln([(xs[3] - 60, 260), (xs[3] - 60, 470)], t4 + .2, BONE, 4, dur=.5), poly(E(xs[3] - 60, 500, 70, 28, 18), "rgba(201,193,238,.12)", LILAC, 2, t4 + .3, style="claimed"),
            rect(xs[3] + 20, 300, 120, 150, "#e9dcc4", "#fff6e6", 2, 8, t4 + .5, fx="pop")]
    els += [ln([(xs[3] + 40, 340 + 22 * k), (xs[3] + 120, 340 + 22 * k)], round(t4 + .6 + .05 * k, 2), "#3d5566", 2, draw=False) for k in range(4)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s50():
    """The close: the Sphinx in its pit at dusk, wide and quiet, Khafre's pyramid behind; a faint lilac '?' far to the left in the sky."""
    els, base = pit_scene("dusk", sun=[120, 470, 22])
    els += [gl(560, 470, 380, -1, .18, "fire")]
    els += sphinx(HX0, HGY, HS, -1, light=.9)
    els += [person(262, HGY, 27, -1, "#2a2018") | {"in": -1}]
    t = T("s50", "Whether it's older")
    els += [lab(170, 290, "?", t, LILAC, 90, st="big", fx="pop", op=.55)]
    base.update(cam=[1.04, 889, 500], els=els)
    return base


# ================================================================== the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


# (chapter, beat, role, the beat's panel, [(line, first words of the sentence where the picture changes, shot)], beat fields)
BEATS = [
    (0, 0, "hook", "s1", [(1, "Around {1400", "s2"), (2, "So how old", "s3")], {}),
    (0, 1, "title", "s3", [], {"intro": True}),
    (1, 0, "world", "s5", [(1, "Its limestone", "s6")], {"chapter": "Cut from the living rock"}),
    (1, 1, "collision", "s7", [(1, "The carvers didn't", "s8")], {}),
    (1, 2, "reversal", "s9", [(1, "How do we", "s10"), (1, "Most of those", "s11")], {}),
    (1, 3, "tag", "s12", [], {}),
    (2, 0, "world", "s13", [(1, "And right beside", "s14")], {"chapter": "Khafre's building site"}),
    (2, 1, "collision", "s15", [(1, "Next door", "s16")], {}),
    (2, 2, "reversal", "s17", [(0, "In a little heap", "s18"), (1, "The job@work", "s19")], {}),
    (2, 3, "tag", "s20", [], {}),
    (3, 0, "world", "s21", [(1, "To him", "s22")], {"chapter": "Written by rain?"}),
    (3, 1, "collision", "s23", [(1, "In front and", "s24"), (2, "Schoch reasoned", "s25")], {}),
    (3, 2, "cost", "s26", [(0, "And the head", "s27")], {}),
    (3, 3, "reversal", "s28", [], {}),
    (3, 4, "tag", "s29", [], {}),
    (4, 0, "world", "s30", [(1, "Soft bands", "s31")], {"chapter": "Salt, sand and silence"}),
    (4, 1, "collision", "s32", [(1, "And this rock", "s33")], {}),
    (4, 2, "cost", "s34", [(0, "The weak layer", "s35")], {}),
    (4, 3, "reversal", "s36", [(1, "Schoch points", "s37")], {}),
    (4, 4, "tag", "s38", [(1, "In {2015", "s39")], {}),
    (5, 0, "world", "s40", [(1, "His workers", "s41")], {"chapter": "Dreams, patches and probes"}),
    (5, 1, "collision", "s42", [(1, "Copies made", "s43")], {}),
    (5, 2, "reversal", "s44", [(1, "Others have", "s45")], {}),
    (6, 0, "weigh", "s46", [(1, "A start a few", "s47"), (2, "Its case rests", "s48")], {"chapter": "The weighing"}),
    (6, 1, "test", "s49", [], {}),
    (6, 2, "close", "s50", [], {}),
]

# alias shots: (panel shot, camera on that panel, additions built when the camera arrives)
ALIASES = {
    "s3": ("s1", [1, 889, 500], "s3_add"),
    "s14": ("s13", [2.3, 1230, 520], "s14_add"),
    "s29": ("s21", [1, 889, 500], "s29_add"),
    "s40": ("s2", [1, 889, 500], "s40_add"),
    "s43": ("s42", [2.6, 760, 690], "s43_add"),
    "s47": ("s46", [1, 889, 500], "s47_add"),
    "s48": ("s46", [1, 889, 500], "s48_add"),
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


def _todo(sid):
    return {"base": "dark", "stars": 30, "cam": CAM, "els": [lab(889, 500, sid, .2, DIM, 60, st="serif")]}


def film():
    script = json.load(open(SCRIPT, encoding="utf-8"))
    SAY.clear(); SAY.update(_segments(script))
    g = globals()
    panels = {}
    for c, b, role, frm, cuts, kw in BEATS:
        for sid in [frm] + [s for _, _, s in cuts]:
            if sid not in ALIASES and sid not in panels:
                panels[sid] = g[sid]() if sid in g else _todo(sid)
    ids = list(panels) + [a for a in ALIASES]
    idx = {s: i for i, s in enumerate(ids)}
    shots = [panels[s] for s in panels] + [{"base": "dark", "els": []} for _ in ALIASES]
    tags, alias, cams = {}, {}, {}
    for k, (sid, (root, cam, fn)) in enumerate(ALIASES.items()):
        z = round(cam[0] + .0001 * (k + 1), 4)
        alias[idx[sid]] = idx[root]
        cams[idx[sid]] = [z] + list(cam[1:])
        tags[z] = (g[fn]() if fn in g else []) if fn else []
    beats = []
    for c, b, role, frm, cuts, kw in BEATS:
        lines = list(script["chapters"][c]["beats"][b]["lines"])
        for li, phrase, sid in cuts:
            lines[li] = _mark(lines[li], phrase, "[go:%d|1.4]" % idx[sid])
        beats.append(B(role, idx[frm], lines, **kw))
    desc = script["description"]
    desc = re.sub(r"Chapters\n0:00[^\n]*\n(?:mm:ss[^\n]*\n)+", "Chapters\n{chapters}\n", desc)
    assert "{chapters}" in desc and "mm:ss" not in desc
    ep = {"id": "lf-sphinx", "code": "LF.22", "series": script["series"], "title": script["title"], "case": "sphinx-erosion",
          "verdict": "unsupported", "claim": "Was the Great Sphinx carved long before the pharaohs?", "mood": "mystery",
          "hook_text": "Older than the *pharaohs*?", "beats": beats, "shots": shots,
          "sources": "Lehner 1992 (doi:10.1017/S0959774300000421) · Lehner 2003 · Dobecki & Schoch 1992 (doi:10.1002/gea.3340070603) · Schoch 1992 (KMT 3.2) · "
                     "Gauri et al. 1995 (doi:10.1002/gea.3340100203) · Harrell 1994 (KMT 5.2) · Reader 2001 (doi:10.1111/1475-4754.00009) · "
                     "Liritzis & Vafiadou 2015 (doi:10.1016/j.culher.2014.05.007) · Linseele et al. 2014 (doi:10.1371/journal.pone.0108517)",
          "post": "A lion as long as a jumbo jet, cut from the rock at Giza. Was it carved long before the pharaohs? The quarry and its temples, the rain "
                  "hypothesis at its strongest, salt, damp sand, the builders' rubbish, light dates and the Dream Stele, weighed.",
          "hashtags": ["#Sphinx", "#Giza", "#AncientEgypt", "#Archaeology", "#Geology", "#WeighItYourself"],
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
