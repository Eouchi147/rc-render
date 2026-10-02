"""LF.05 The UFO Files (lf-ufo-files): what governments have actually admitted about UFOs and UAP, file by file. A 16:9 long film.

Script: films/long/lf-ufo-files/script.json (its lines are read from there and kept word for word; this module only adds the
[go:N|t] markers where the picture changes). One ep shot per script shot (s1..s52 = shots 0..51), hung on one wall
(mural.wall), six chapter rooms. A shot that adds to a picture already on the wall (a closer look at the Tic Tac, the sun
lighting the U-2, a stamp on the reflector, the lower rows of the ledger) is an alias of that panel with its own camera; its
additions are attached to the step the camera makes for it, so they build on that step's clock (_attach(), as in lf_gobekli).
Build-ins inside a sentence are timed with a speech Clock (an estimate from syllables, as in lf_gobekli).

Numbers drawn true to the script: the Tic Tac about the length of an F/A-18 (about 12 m); Mogul's train of 23 balloons 20 feet
apart (more than 130 m) beside a person 1.7 m; Blue Book's 12,618 reports as 100 cards of which 5.6 are unexplained (701);
the U-2 at about 18 km against airliners at 3 to 6 km; over half of 100 reports as spy flights; 23 years of Stargate and
about $20 million; $22 million for 2007 to 2012; Go Fast about 4,000 m up and about 65 km/h; 144 reports and 1 explained;
over 2,000 cases, about half too thin to analyse; six releases in 2026. Claims are drawn dotted (lilac), inferences dashed,
evidence solid. Maps: New Mexico (the state outline schematic, sites from the Air Force reports), the Virginia coast.
Reused from the Shorts (f13.py, File 13): roswell-mogul (the newspaper, the map and debris, the debris on the ground, the
photocopies, the four answers, the balloon train), uap-disclosure (the infrared screen, the 144 reports, the hearsay chain, the
empty tray), stargate-psychic (the mind at a distance, the five code names, the viewer's sketch, the fog over the report), all
redrawn wide for 16:9.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-ufo-files/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-ufo-files/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-ufo-files RC_FILMS_EPS=/tmp/claude-0/sbx_lf-ufo-files/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-ufo-files/boards python3 films.py long.lf_ufo_files
"""
import copy, json, math, os, random, re
from films import View
from mural import remix, SENT
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, question, ellipse, scatter, \
    BONE, AMBER, BLUE, LILAC, GREEN, RED, AU

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = json.load(open(os.path.join(HERE, "lf-ufo-files", "script.json"), encoding="utf-8"))

GOLD, PAPER, INK, DIM, WARM = "#f2c98e", "#efe6d2", "#2a2219", "#cbbca8", "#ffb07a"
FLIR, FLIRG = "#0d1a12", "#9fe0a8"
CARD = "#1b1511"
GRADE = {"strong": "#7fd1d4", "established": "#8fd9b0", "awaiting": "#c9c1ee", "open": "#f0b06a", "ruled": "#e98a8a", "plausible": "#e8c86a"}
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800 (captions below 815, HUD above 110)
CAM = [1, 889, 500]


# ================================================================ small drawing helpers (panel units)
def r1(v):
    return round(v, 1)


def P(pts):
    return [[r1(x), r1(y)] for x, y in pts]


def poly(p, fill, c="none", w=0, at=0, curve=False, **kw):
    e = {"k": "poly", "p": P(p), "fill": fill, "c": c, "w": w, "curve": curve, "in": at}
    e.update(kw)
    return e


def rot(pts, cx, cy, deg):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    return [[r1(cx + (x - cx) * ca - (y - cy) * sa), r1(cy + (x - cx) * sa + (y - cy) * ca)] for x, y in pts]


def lab(x, y, t, at=0, c=BONE, size=30, a="middle", **kw):
    return label(r1(x), r1(y), t, round(at, 2), c, size, a, **kw)


def ink(x, y, t, at=0, c=INK, size=28, a="middle", st="lab", **kw):
    """Text printed on paper: dark, no halo."""
    return label(r1(x), r1(y), t, round(at, 2), c, size, a, st=st, halo=False, **kw)


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words (scales with the picture, like a plaque)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    return [box(r1(x0), r1(y - h / 2), r1(w), r1(h), "rgba(18,13,10,.9)", c, 2.5, h / 2, round(at, 2), fx="pop"),
            label(r1(x0 + w / 2), r1(y + size * .36), t, round(at + .05, 2), c, size, scl=True, fx="pop")]


def rgroup(deg, cx, cy, els, at, fx="pop", **kw):
    """A rotated group whose build-in animates: the rotation sits on an inner group (an fx on a group replaces its transform)."""
    inner = {"k": "group", "tr": "rotate(%s %s %s)" % (r1(deg), r1(cx), r1(cy)), "els": [dict(e, **{"in": -1}) for e in els]}
    g = {"k": "group", "in": round(at, 2), "els": [inner]}
    if fx:
        g["fx"] = fx
    g.update(kw)
    return g


def cross(x0, y0, x1, y1, at, c=RED, w=6):
    """A strike-through that fades in (a drawn line would show its round cap as a dot before it draws)."""
    e = line([[r1(x0), r1(y0)], [r1(x1), r1(y1)]], round(at, 2), c, w, draw=False)
    e["dur"] = .35
    return e


def stamp(x, y, t, c, at, size=34, deg=-8, w=None):
    """A rubber stamp: a rotated frame with its word, popping on."""
    w = w or len(t) * size * .72 + 40
    h = size * 1.7
    return rgroup(deg, x, y, [box(r1(x - w / 2), r1(y - h / 2), r1(w), r1(h), "rgba(20,14,10,.25)", c, 4, 8, -1),
                              label(r1(x), r1(y + size * .36), t, -1, c, size, st="cap", halo=False)], at)


def cover(x, y, w, h, fill, at, op=1.0, dur=.5, r=0):
    """A veil of the background's colour laid over part of a panel: what was there fades away (op 1) or back (op < 1)."""
    e = box(r1(x), r1(y), r1(w), r1(h), fill, r=r, at=round(at, 2), op=op if op < 1 else None)
    e["dur"] = dur
    return e


def person_s(x, y, h, at, c="#e8d6b8", **kw):
    e = person(r1(x), r1(y), h, round(at, 2), c)
    e.update(kw)
    return e


def folder(x, y, w, h, at, c="#cdb58a", edge="#8a6a48", tab=None, tc=INK, fx="rise", tab_x=None, tsize=26):
    """A manila folder seen face on, a tab on top with its word."""
    tw = max(110, len(tab or "") * tsize * .62 + 36) if tab else 120
    tx = x + 24 if tab_x is None else tab_x
    out = [box(r1(tx), r1(y - 30), r1(tw), 40, c, edge, 2, 8, round(at, 2), fx=fx),
           box(r1(x), r1(y), r1(w), r1(h), c, edge, 2, 6, round(at, 2), fx=fx)]
    if tab:
        out.append(ink(tx + tw / 2, y - 3, tab, at + .05, tc, tsize, st="lab"))
    return out


def sheet_lines(x, y, w, n, at, gap=26, c="#8c8478", wd=3, op=.8):
    return [line([[r1(x), r1(y + gap * j)], [r1(x + (w if j % 4 != 3 else w * .6)), r1(y + gap * j)]], round(at + .02 * j, 2), c, wd, draw=False, op=op) for j in range(n)]


def saucer(x, y, s, at, c=LILAC, fill="rgba(201,193,238,.10)"):
    """A flying saucer as people drew it, in the claimed (dotted) style."""
    return [poly(ellipse(x, y, 150 * s, 30 * s)[:-1], fill, c, 3, at, True, style="claimed", fx="draw", dur=.8),
            poly(ellipse(x, y - 18 * s, 62 * s, 44 * s, a0=180, a1=360), fill, c, 3, at + .3, True, style="claimed", fx="draw", dur=.6)]


def balloon(x, y, r, at, c="#efe6d2"):
    """A weather balloon: the envelope, its line and a small instrument box."""
    return [line([[x, y + r], [x, y + r + 2.2 * r]], at + .2, "#cbbca8", 2, dur=.5),
            oval(x, y, r, r * 1.12, c, "#ffffff", 2, 1, at, fx="rise"),
            box(r1(x - r * .22), r1(y + r * 3.2), r1(r * .44), r1(r * .3), "#a8865e", r=2, at=at + .5)]


def reflector(x, y, s, at, op=None, style="known"):
    """A Mogul radar reflector seen face on: a diamond of balsa sticks with foil-paper panes."""
    pts = [[x, y - 60 * s], [x + 46 * s, y], [x, y + 60 * s], [x - 46 * s, y]]
    out = [poly(pts, "#c9ccd2", "#ffffff", 2, at, False, fx="pop", style=style),
           poly([[x, y - 60 * s], [x + 46 * s, y], [x, y]], "#e6e8ec", "none", 0, at, fx="pop"),
           line([[x, y - 60 * s], [x, y + 60 * s]], at + .1, "#a8865e", 3 * max(s, .6), draw=False),
           line([[x - 46 * s, y], [x + 46 * s, y]], at + .1, "#a8865e", 3 * max(s, .6), draw=False)]
    if op is not None:
        for e in out:
            e.update(op=op, keepop=True)
    return out


def jet_side(x, y, L, at, c="#9aa3ad", face=-1, style="known", fill=None, fx="rise", op=None, w=1.5):
    """A twin-tailed fighter in side view, nose towards `face` (-1 = left), length L, its belly line at y."""
    prof = [(0, 0), (.1, -.03), (.2, -.06), (.27, -.11), (.36, -.12), (.44, -.08), (.62, -.07), (.76, -.09), (.84, -.25), (.93, -.26),
            (.95, -.08), (1.0, -.06), (1.0, .01), (.84, .03), (.55, .04), (.2, .03)]
    pts = [[x + (u - .5) * L * (-face), y + v * L] for u, v in prof]
    e = poly(pts, fill or c, "#e9edf2" if fill != "none" else c, w, at, False, fx=fx, style=style)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def plane_side(x, y, L, at, c="#e6e8ec", kind="u2", fx="pop"):
    """A plane in side view, nose left: kind 'u2' (slim, one tall fin, a long thin wing seen nearly edge on) or 'liner' (a 1950s airliner)."""
    if kind == "u2":
        prof = [(0, 0), (.08, -.035), (.3, -.06), (.36, -.09), (.44, -.07), (.8, -.05), (.88, -.24), (.97, -.25), (1.0, -.04), (1.0, .02), (.7, .03), (.1, .03)]
        wing = [[x - L * .22, y - L * .02], [x + L * .9, y - L * .05], [x + L * .9, y - L * .02], [x - L * .22, y + L * .015]]
    else:
        prof = [(0, 0), (.06, -.06), (.2, -.09), (.8, -.09), (.9, -.22), (.98, -.23), (1.0, -.08), (1.0, .0), (.8, .05), (.1, .05)]
        wing = [[x - L * .12, y + L * .0], [x + L * .2, y - L * .02], [x + L * .2, y + L * .02], [x - L * .12, y + L * .03]]
    pts = [[x + (u - .5) * L, y + v * L] for u, v in prof]
    return [poly(wing, c, "none", 0, at, fx=fx, op=.8, keepop=True), poly(pts, c, "#ffffff", 1, at, fx=fx)]


def plane_top(x, y, L, span, at, c="#9aa3ad", heading=0, fx="pop", op=None, tail=.32, wing_at=.42, chord=.12):
    """A plane seen from above, nose towards heading (degrees; 0 = left): fuselage, straight wings, tailplane."""
    h = L * .05
    pts = [[x - L / 2, y], [x - L / 2 + L * .08, y - h], [x + L / 2, y - h * .6], [x + L / 2, y + h * .6], [x - L / 2 + L * .08, y + h]]
    wx = x - L / 2 + L * wing_at
    wing = [[wx, y - span / 2], [wx + L * chord, y - span / 2], [wx + L * chord * 1.4, y], [wx + L * chord, y + span / 2], [wx, y + span / 2], [wx - L * .02, y]]
    tx = x + L / 2 - L * .1
    tl = [[tx, y - span * tail / 2], [tx + L * .08, y - span * tail / 2], [tx + L * .1, y], [tx + L * .08, y + span * tail / 2], [tx, y + span * tail / 2]]
    out = [poly(rot(q, x, y, heading), c, "none", 0, at, fx=fx) for q in (wing, tl, pts)]
    if op is not None:
        for e in out:
            e.update(op=op, keepop=True)
    return out


def tictac(x, y, L, at, c="#f5f3ee", style="known", fx="pop", op=None, deg=0, glow_op=.55):
    """The Tic Tac as the aviators described it: a white capsule, no wings, no exhaust."""
    h = L * .36
    caps = box(r1(x - L / 2), r1(y - h / 2), r1(L), r1(h), c if style == "known" else "rgba(245,243,238,.12)", "#ffffff" if style == "known" else c, 2, h / 2, round(at, 2),
               style=style)
    if op is not None:
        caps["op"] = op
    out = [rgroup(deg, x, y, [caps], at, fx)]
    if glow_op:
        out.insert(0, glow(r1(x), r1(y), L * 1.1, round(at, 2), glow_op, "scan"))
    return out


def cow(x, y, s, at, c="#e8dcc8", fx="pop", spots="#3a2f25"):
    """A cow in side view, standing (feet at y), facing left."""
    body = [[x - 60 * s, y - 70 * s], [x + 50 * s, y - 72 * s], [x + 62 * s, y - 58 * s], [x + 60 * s, y - 30 * s], [x - 58 * s, y - 30 * s]]
    head = [[x - 60 * s, y - 72 * s], [x - 88 * s, y - 80 * s], [x - 96 * s, y - 60 * s], [x - 86 * s, y - 52 * s], [x - 62 * s, y - 50 * s]]
    out = [poly(body, c, "#5a4a3a", 1.5, at, True, fx=fx), poly(head, c, "#5a4a3a", 1.5, at, True, fx=fx)]
    for lx in (-48, -30, 34, 50):
        out.append(line([[x + lx * s, y - 32 * s], [x + lx * s, y]], at, c, 7 * s, draw=False))
    out += [oval(x - 10 * s, y - 56 * s, 16 * s, 10 * s, spots, at=at), oval(x + 30 * s, y - 46 * s, 12 * s, 9 * s, spots, at=at),
            line([[x + 62 * s, y - 60 * s], [x + 74 * s, y - 36 * s]], at, c, 3 * s, draw=False)]
    return out


def person_sit(x, y, h, at, c="#e8d6b8"):
    """A person seated behind a table: head and shoulders above y (the table edge)."""
    return [poly([[x - h * .17, y], [x - h * .15, y - h * .3], [x - h * .05, y - h * .36], [x + h * .05, y - h * .36], [x + h * .15, y - h * .3], [x + h * .17, y]],
                 c, "none", 0, at, True, fx="rise"),
            {"k": "circle", "x": r1(x), "y": r1(y - h * .47), "r": r1(h * .1), "fill": c, "c": "none", "w": 0, "in": round(at, 2), "fx": "rise"}]


def desk(x0, x1, y, at=-1, c="#5a4330", edge="#c9a070", h=34):
    return [box(r1(x0), r1(y), r1(x1 - x0), h, c, edge, 1.4, 4, at), box(r1(x0 + 10), r1(y + h), r1(x1 - x0 - 20), 120, "rgba(40,30,22,.85)", r=0, at=at)]


def mic(x, y, at):
    return [line([[x, y], [x - 14, y - 50]], at, "#9aa0a8", 3, draw=False), dot(r1(x - 16), r1(y - 56), 7, "#3a3f45", at)]


def cards_grid(x0, y0, nx, ny, w, h, gx, gy, at, step, fill="#cdb58a", edge="#8a6a48", op=None):
    out = []
    for k in range(nx * ny):
        c, r = k % nx, k // nx
        out.append(box(r1(x0 + gx * c), r1(y0 + gy * r), w, h, fill, edge, 1, 2, round(at + step * k, 2), op=op, fx="pop"))
    return out


# ================================================================ timing: when each word is said (an estimate, from syllables)
TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
RATE, SGAP, LGAP, CGAP = 4.25, .15, .9, .12          # syllables a second (x [p:]), gaps after a sentence, a line, a comma


def _syl(w):
    a = re.sub(r"[^A-Za-z]", "", w)
    if len(a) >= 2 and a.isupper():
        return len(a)                                  # UAP, CIA: letters
    w = a.lower()
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def _spoken(seg):
    s = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", TAGS.sub(" ", seg))
    return re.sub(r"@\w+", "", s.replace("^", "").replace("*", "")).split()


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Clock:
    """Estimated word times per beat (seconds from the beat's first word). A shot's step starts at its [go:] marker (or at the beat's
    first word; at a chapter beat's second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said,
    counted from the start of shot i's step."""
    def __init__(self, beats):
        self.start, self.words = {}, {}
        for bi, b in enumerate(beats):
            t, ws, sents = 0.0, [], []
            for li, ln in enumerate(b["lines"]):
                if li:
                    t += LGAP
                cuts = [0] + [m.start() for m in SENT.finditer(ln) if m.start() > 0] + [len(ln)]
                for a, z in zip(cuts, cuts[1:]):
                    seg = ln[a:z]
                    p = re.search(r"\[p:([\d.]+)\]", seg)
                    r = RATE * (float(p.group(1)) if p else 1.0)
                    sents.append(t)
                    for m in GOM.finditer(seg):
                        self.start[int(m.group(1))] = (bi, t)
                    for w in _spoken(seg):
                        ws.append((_norm(w), t))
                        t += _syl(w) / r
                        if w[-1] in ",:;":
                            t += CGAP
                    t += SGAP
            frm = b["visual"]["from"]
            self.start.setdefault(frm, (bi, sents[1] if b.get("chapter") else 0.0))
            self.words[bi] = ws

    def at(self, i, phrase, lo=.4, dt=0.0):
        bi, t0 = self.start[i]
        want = [_norm(x) for x in phrase.split()]
        ws = self.words[bi]
        for k in range(len(ws)):
            if ws[k][1] >= t0 - 1e-6 and [w for w, _ in ws[k:k + len(want)]] == want:
                return round(max(lo, ws[k][1] - t0 + dt), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))


# ================================================================ narration: the script's lines, with [go:] markers added
def go_at(ln, anchor, n, t=1.6):
    """Put [go:n|t] at the start of the sentence whose words begin with `anchor`: before the run of tags in front of it
    ([p:]/[act:]/[tune:]...), after a [d:] mood tag if the run opens with one."""
    assert ln.count(anchor) == 1, (anchor, ln[:80])
    i = ln.index(anchor)
    j = i
    while j > 0 and ln[j - 1] == "]":
        j = ln.rindex("[", 0, j - 1)
    if ln.startswith("[d:", j):
        j = ln.index("]", j) + 1
    return ln[:j] + "[go:%d|%s]" % (n, t) + ln[j:]


def lines_of(ci, bi, gos=()):
    """The lines of chapter ci, beat bi, with markers: gos = [(line index, anchor or None for the line start, shot, glide)]."""
    out = list(SCRIPT["chapters"][ci]["beats"][bi]["lines"])
    for li, anchor, n, t in gos:
        ln = out[li]
        if anchor is None:
            if ln.startswith("[d:"):
                k = ln.index("]") + 1
                out[li] = ln[:k] + "[go:%d|%s]" % (n, t) + ln[k:]
            else:
                out[li] = "[go:%d|%s]" % (n, t) + ln
        else:
            out[li] = go_at(ln, anchor, n, t)
    return out


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


CH = [c["title"] for c in SCRIPT["chapters"]]


def BEATS():
    return [
        B("hook", 0, lines_of(0, 0, [(0, "Above the foam", 1, 1.4), (1, None, 2, 1.4), (1, "Nineteen years later", 3, 1.6), (2, None, 4, 1.6)])),
        B("title", 5, lines_of(0, 1), intro=True),
        B("world", 6, lines_of(1, 0, [(1, None, 7, 1.6), (1, "Rubber", 8, 1.6), (2, None, 9, 1.6)]), chapter=CH[1]),
        B("collision", 10, lines_of(1, 1, [(1, None, 11, 1.4)])),
        B("cost", 12, lines_of(1, 2, [(1, None, 13, 1.6), (2, None, 14, 1.4)])),
        B("reversal", 15, lines_of(1, 3, [(1, None, 16, 1.6)])),
        B("world", 17, lines_of(2, 0, [(1, None, 18, 1.6)]), chapter=CH[2]),
        B("collision", 19, lines_of(2, 1, [(0, "At sunrise", 20, 1.4), (1, None, 21, 1.6), (2, None, 22, 1.6)])),
        B("cost", 23, lines_of(2, 2, [(1, None, 24, 1.6), (2, None, 25, 1.6), (2, "But one striking", 26, 1.6)])),
        B("reversal", 27, lines_of(2, 3)),
        B("tag", 28, lines_of(2, 4)),
        B("world", 29, lines_of(3, 0, [(1, None, 30, 1.6), (1, "In {2020", 31, 1.4)]), chapter=CH[3]),
        B("collision", 32, lines_of(3, 1, [(1, None, 33, 1.6)])),
        B("reversal", 34, lines_of(3, 2, [(0, "Off Virginia", 35, 1.6), (1, None, 36, 1.6), (2, None, 37, 1.6)])),
        B("world", 38, lines_of(4, 0, [(0, "He says America", 39, 1.6), (1, None, 40, 1.6)]), chapter=CH[4]),
        B("collision", 41, lines_of(4, 1, [(0, "The Pentagon's UAP office", 42, 1.6), (1, None, 43, 1.6)])),
        B("reversal", 44, lines_of(4, 2, [(1, None, 45, 1.6), (1, "By September", 46, 1.6)])),
        B("weigh", 47, lines_of(5, 0, [(0, "Go Fast drifting", 48, 1.4), (1, None, 49, 1.6)]), chapter=CH[5]),
        B("test", 50, lines_of(5, 1)),
        B("close", 51, lines_of(5, 2)),
    ]


# ================================================================ the wall: aliases (closer looks at a panel already hung)
ALIAS = {1: 0, 2: 0, 5: 4, 11: 10, 14: 13, 20: 19, 31: 30, 48: 47}
ALIAS_CAMS = {1: [1.8, 1150, 590], 2: [1, 889, 500], 5: [1.06, 889, 470], 11: [1, 889, 500], 14: [1.1, 889, 470], 20: [1, 889, 500],
              31: [1, 889, 500], 48: [1.05, 889, 520]}


def _tagged(cams):
    """Each alias camera gets a tiny unique extra zoom (a few ten-thousandths: invisible), so its step can be found after the wall is built."""
    out = {}
    for k, i in enumerate(sorted(cams)):
        z, x, y = cams[i]
        out[i] = [round(z + .0003 * (k + 1), 4), x, y]
    return out


def _attach(ep, cams, late):
    """Give each alias step its additions: a panel item on that step (built once, shown from the start of its glide, timed on its clock)."""
    panels = ep["wall"]["panels"]
    for i, els in late.items():
        z = cams[i][0]
        ks = [k for k, s in enumerate(ep["shots"]) if abs(s["cam"][0] - z) < 1e-9]
        assert len(ks) == 1, ("alias step", i, ks)
        k = ks[0]
        cx, cy = ep["shots"][k]["cam"][1:]
        js = [j for j, p in enumerate(panels) if p["ox"] <= cx <= p["ox"] + p.get("w", W_) and p["oy"] <= cy <= p["oy"] + p.get("h", H_)]
        assert len(js) == 1, ("panel of alias", i, js)
        p = panels[js[0]]
        ep["shots"][k]["els"].append({"k": "panel", "ox": p["ox"], "oy": p["oy"], "w": p.get("w", W_), "h": p.get("h", H_), "base": "none", "els": list(els), "pn": js[0]})
    return ep


# ================================================================ chapter 0 · the cold open: the Tic Tac over a churning sea
SEA_Y = 330                                     # the horizon of the opening sea


def _hexrgb(h):
    h = h.lstrip("#")
    return [int(h[k:k + 2], 16) for k in (0, 2, 4)]


def _lerpc(a, b, t):
    return [a[k] + (b[k] - a[k]) * t for k in range(3)]


def sea_col(y, y0=SEA_Y, h=700, op=.9):
    """The colour the day sea shows at height y (the water's gradient over the day sky): for veils that must vanish into it."""
    tw = max(0, min(1, (y - y0) / h))
    w = _lerpc(_hexrgb("#3f7f9c"), _hexrgb("#10303f"), tw)
    wa = .9 + .05 * tw
    ts = (y + 900) / 2400
    sky = _lerpc(_hexrgb("#35507a"), _hexrgb("#8aa3b8"), ts / .6) if ts < .6 else _lerpc(_hexrgb("#8aa3b8"), _hexrgb("#e9d6b5"), (ts - .6) / .4)
    c = [op * (wa * w[k] + (1 - wa) * sky[k]) + (1 - op) * sky[k] for k in range(3)]
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)


def sea_veil(x, y0, w, y1, at, n=4, dur=.5):
    """A veil in strips, each the sea's colour at its height, so the patch it hides melts back into the water."""
    hs = (y1 - y0) / n
    return [cover(x, y0 + hs * k, w, hs + 1, sea_col(y0 + hs * (k + .5)), at, dur=dur) for k in range(n)]


TT = (889, 470)                                  # where the Tic Tac hangs over the churn


def s01_sea(C):
    """s1: a bright day over the Pacific: a calm sea, two fighters high up at the right, then the water churning in the middle."""
    r = random.Random(7)
    swell = []
    for k in range(26):
        x, y = r.uniform(100, 1700), r.uniform(360, 790)
        if 640 < x < 1140 and 420 < y < 660:
            continue
        L = 40 + 60 * (y - 330) / 470
        swell.append(line([[r1(x - L / 2), r1(y)], [r1(x), r1(y - 3)], [r1(x + L / 2), r1(y)]], -1, "#d8eef7", 1.6, curve=True, draw=False, op=.22))
    cx, cy = 889, 600
    foam = [oval(cx, cy, 120, 20, "rgba(240,250,255,.42)", at=1.4, fx="pop")] + \
           [poly(ellipse(cx, cy, rx, ry)[:-1], "none", "#f2fbff", 2.2, round(1.6 + .3 * k, 2), True, fx="draw", dur=.9, op=.6 - .12 * k, keepop=True)
            for k, (rx, ry) in enumerate(((150, 27), (185, 33), (222, 40)))] + \
           [dot(x, y, 2.6, "#ffffff", round(1.5 + .015 * k, 2), op=.75) for k, (x, y) in enumerate(scatter(40, cx - 100, cx + 100, cy - 14, cy + 14, 3))
            if ((x - cx) / 105) ** 2 + ((y - cy) / 17) ** 2 < 1]
    jets = []
    for k, (x, y) in enumerate(((1190, 172), (1352, 204))):
        at = .4 + .4 * k
        jets += [line([[x + 50, y - 4], [x + 260, y - 10]], at + .2, "#ffffff", 3, draw=True, dur=.8, op=.32), jet_side(x, y, 96, at, "#aab2bb", -1)]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [1600, 150, 24], "cam": [1.2, 960, 440], "els": [
        {"k": "water", "y": SEA_Y, "h": 700, "op": .9, "in": -1}] + swell + jets + foam}


def s02_late(C):
    """s2 (alias of s1, closer): the white capsule darts about over the foam (ghosts and dotted hops), then hangs; a detail card at the
    right: the capsule beside a fighter of the same length, dotted wings and a dotted exhaust struck through."""
    T = lambda ph, dt=0: C.at(1, ph, dt=dt)
    x, y = TT
    hop = [line([[780, 492], [995, 452], [870, 488], [x, y]], .7, "#ffffff", 2.2, "claimed", dur=1.2, curve=True)]
    ghosts = tictac(780, 492, 64, .4, op=.32, glow_op=0) + tictac(995, 452, 64, 1.0, op=.32, glow_op=0)
    main = tictac(x, y, 64, T("shaped"), glow_op=.45)
    # the detail card: the capsule, and a fighter of the same length under it
    kx, ky, kw, kh = 1100, 450, 460, 290
    at_c = T("shaped", .4)
    card_ = [box(kx, ky, kw, kh, "rgba(12,22,30,.8)", "rgba(230,245,255,.45)", 2, 18, at_c, fx="pop"),
             line([[x + 36, y + 8], [kx, ky + 70]], at_c, "rgba(230,245,255,.45)", 2, "inferred", dur=.5)]
    cx, cy = kx + kw / 2 - 20, ky + 95
    big = tictac(cx, cy, 170, at_c + .3, glow_op=.35)
    jet_at = T("about the size")
    jet = [jet_side(cx, ky + 240, 170, jet_at, "#c9d2da", -1, style="inferred", fill="rgba(201,210,218,.10)", fx="pop", w=2.2),
           lab(cx - 100, ky + 236, "a fighter jet", jet_at + .3, "#c9d2da", 26, "end")]
    wings_at, ex_at = T("No wings"), T("No exhaust")
    wings = [poly([[cx - 26, cy], [cx + 8, cy - 52], [cx + 34, cy - 52], [cx + 26, cy]], "none", LILAC, 2.5, wings_at, style="claimed", fx="pop"),
             cross(cx - 36, cy + 4, cx + 44, cy - 58, wings_at + .35, RED, 5), lab(cx - 46, cy - 40, "no wings", wings_at + .2, BONE, 26, "end")]
    plume = [poly([[cx + 86, cy - 10], [cx + 150, cy - 16], [cx + 168, cy], [cx + 150, cy + 16], [cx + 86, cy + 10]], "none", LILAC, 2.5, ex_at,
                  style="claimed", fx="pop"),
             cross(cx + 82, cy + 28, cx + 172, cy - 28, ex_at + .35, RED, 5), lab(cx + 130, cy + 62, "no exhaust", ex_at + .2, BONE, 26)]
    return ghosts + hop + main + card_ + big + jet + wings + plume


def s03_late(C):
    """s3 (alias of s1, the whole sea): one fighter spirals down to the capsule; the capsule swings round to face it, climbs and streaks
    away to the left; where it hung, a question mark."""
    T = lambda ph, dt=0: C.at(2, ph, dt=dt)
    x, y = TT
    path = line([[1150, 196], [1060, 250], [1120, 300], [1010, 352], [950, 392], [925, 418]], .6, BONE, 2.5, "claimed", dur=1.6, curve=True)
    dj = rgroup(32, 952, 400, [jet_side(952, 400, 60, -1, "#d8dee4", -1)], 2.0)
    name = lab(1190, 300, "David Fravor", T("David"), BONE, 26, "start")
    sw = T("swings")
    turn = sea_veil(x - 52, y - 30, 104, y + 30, sw, n=3, dur=.3) + tictac(x, y, 64, sw + .1, deg=-38, glow_op=0)
    cl = T("climbs")
    streak = [line([[x - 20, y - 20], [700, 330], [420, 230], [130, 190]], cl, "#bfe6f5", 7, dur=.6, curve=True, op=.12),
              line([[x - 20, y - 20], [700, 330], [420, 230], [130, 190]], cl, "#ffffff", 2.5, dur=.6, curve=True, op=.7)]
    gone = T("gone")
    vanish = sea_veil(x - 70, y - 50, 140, y + 50, gone, n=4, dur=.4) + [dict(question(x, y + 16, gone + .5, 76)[1]), glow(x, y - 10, 90, gone + .5, .35, "scan")]
    return [path, dj, name] + turn + streak + vanish


def s04_oath(C):
    """s4: a hearing room in warm light: a dais with members, a witness at a table with a microphone, his right hand rising: the oath."""
    els = [glow(889, 430, 620, -1, .22, "lamp"),
           box(260, 200, 1258, 70, "#4a3626", "#c9a070", 1.5, 6, -1), box(260, 270, 1258, 40, "#2f2219", r=0, at=-1)]
    els += [{"k": "circle", "x": 330 + 120 * k, "y": 178, "r": 16, "fill": "#7a6a58", "c": "none", "w": 0, "in": -1} for k in range(10)] + \
           [box(312 + 120 * k, 192, 36, 14, "#7a6a58", r=6, at=-1) for k in range(10)]
    els += person_sit(889, 600, 260, .3, "#e8d6b8") + desk(560, 1218, 600) + mic(930, 600, .5) + \
           [box(810, 610, 160, 32, "#e8dcc2", "#8a7a66", 1, 3, .6), ink(890, 634, "WITNESS", .6, INK, 24, st="small")]
    hand = C.at(3, "under")
    els += [line([[935, 520], [980, 470], [990, 400]], hand, "#e8d6b8", 16, dur=.5), dot(990, 392, 15, "#e8d6b8", hand + .4),
            glow(990, 400, 80, hand + .4, .5, "lamp"), lab(889, 748, "under oath, 2023", hand + .3, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


YEARS = ["1947", "1952", "1972", "2004", "2017", "2023", "2026"]


def s05_files(C):
    """s5: a dark desk under a lamp, a long box of file folders whose tabs pop in with their years, 1947 to 2026; a question rises at
    the question."""
    els = [glow(560, 260, 520, -1, .35, "lamp"), box(-20, 640, 1820, 400, "#3a2c20", r=0, at=-1), line([[-20, 640], [1800, 640]], -1, "#8c7152", 2, draw=False)]
    x0, w = 330, 150
    for k, yv in enumerate(YEARS):
        at = round(.5 + .32 * k, 2)
        x = x0 + 165 * k
        els += folder(x, 430, w, 200, at, tab=yv, tab_x=x + 18, tsize=26)
    els += [box(300, 560, 1180, 110, "#5a4330", "#c9a070", 2, 6, .2), box(300, 560, 1180, 14, "#6e5440", r=3, at=.2)]
    q = C.at(4, "So what")
    els += question(889, 330, q, 96)
    return {"base": "dark", "cam": CAM, "els": els}



# ================================================================ chapter 1 · A saucer in the paper (Roswell, 1947)
def s07_paper(C):
    """s7: the Roswell Daily Record of 8 July 1947 on a dark desk: masthead, date, the headline typing in; a dotted saucer glows beside it
    (the claim); a gold frame round the headline at 'front page'."""
    T = lambda ph, dt=0: C.at(6, ph, dt=dt)
    x0, y0, w, h = 300, 140, 820, 650
    cx = x0 + w / 2
    els = [glow(889, 460, 700, -1, .2, "lamp"), box(x0 + 14, y0 + 18, w, h, "rgba(0,0,0,.5)", r=4, at=.2),
           box(x0, y0, w, h, PAPER, "#fff8ea", 1.2, 4, .2),
           ink(cx, y0 + 74, "ROSWELL DAILY RECORD", .5, INK, 46, st="serif"),
           line([[x0 + 40, y0 + 100], [x0 + w - 40, y0 + 100]], .5, INK, 2.5, draw=False),
           ink(cx, y0 + 130, "Tuesday, 8 July 1947", .6, "#6a645c", 24, st="small"),
           line([[x0 + 40, y0 + 144], [x0 + w - 40, y0 + 144]], .6, INK, 1.2, draw=False)]
    hd = T("tells the press")
    els += [{"k": "label", "x": cx, "y": y0 + 230, "t": "RAAF Captures Flying Saucer", "st": "serif", "size": 58, "c": INK, "halo": False, "in": hd, "fx": "type", "dur": 1.4},
            {"k": "label", "x": cx, "y": y0 + 296, "t": "On Ranch in Roswell Region", "st": "serif", "size": 40, "c": INK, "halo": False, "in": hd + 1.2, "fx": "type", "dur": 1.0}]
    els += sum([sheet_lines(x0 + 50 + 250 * c, y0 + 350, 210, 11, hd + 1.6 + .1 * c, gap=24) for c in range(3)], [])
    sc = T("flying saucer")
    els += [glow(1440, 330, 210, sc, .5, "scan")] + saucer(1440, 330, 1.05, sc) + [lab(1440, 450, "the claim", sc + .6, LILAC, 28)]
    fp = T("front page")
    els += [{"k": "rect", "x": x0 + 28, "y": y0 + 172, "w": w - 56, "h": 146, "r": 6, "fill": "none", "c": GOLD, "sw": 3, "in": fp, "fx": "draw", "dur": .8}]
    return {"base": "dark", "cam": CAM, "els": els}


NM = [(-109.05, 37.0), (-103.0, 37.0), (-103.0, 36.5), (-103.04, 32.0), (-106.62, 32.0), (-106.53, 31.78), (-108.21, 31.78), (-108.21, 31.33), (-109.05, 31.33)]
V_NM = View(-107.4, -103.2, 32.45, 34.75, (90, 120, 1600, 680))


def s08_map(C):
    """s8: New Mexico (the state outline schematic): the Roswell air base, the debris field near Corona; white debris dots scatter on the
    ranch and an amber arrow carries them to the base; a 100 km scale."""
    T = lambda ph, dt=0: C.at(7, ph, dt=dt)
    v = V_NM
    rw, db = v.p(-104.52, 33.39), v.p(-105.3, 33.95)
    els = [{"k": "map", "land": v.land(), "in": -1},
           lab(*v.p(-106.6, 34.55), "New Mexico", .4, "#c9ad85", 36, st="ital"),
           {"k": "pin", "x": rw[0], "y": rw[1], "t": "Roswell air base", "c": GOLD, "in": .6},
           {"k": "scale", "x": 140, "y": 760, "w": r1(v.km(100)), "t": "100 km", "in": .8}]
    rio = [(-106.68, 34.9), (-106.75, 34.4), (-106.88, 34.05), (-106.9, 33.6), (-107.2, 33.2), (-107.0, 32.8), (-106.85, 32.45)]
    pecos = [(-104.6, 34.75), (-104.45, 34.3), (-104.42, 33.85), (-104.35, 33.4), (-104.4, 32.9), (-104.2, 32.45)]
    els += [line([v.p(*q) for q in rio], -1, "#5fa8c9", 2.5, curve=True, draw=False, op=.55), line([v.p(*q) for q in pecos], -1, "#5fa8c9", 2, curve=True, draw=False, op=.5),
            lab(*v.p(-107.15, 33.95), "Rio Grande", .5, "#8fc4dc", 24, st="ital"), lab(*v.p(-104.05, 34.4), "Pecos", .5, "#8fc4dc", 24, st="ital"),
            dot(*v.p(-105.6, 34.25), 6, DIM, .7), lab(v.p(-105.6, 34.25)[0], v.p(-105.6, 34.25)[1] - 16, "Corona", .7, DIM, 24)]
    rc = T("a ranch")
    els += [{"k": "pin", "x": db[0], "y": db[1], "t": "the debris field", "t2": "near Corona", "c": BONE, "a": "end", "lx": -60, "ly": -6, "in": rc}]
    wr = T("field of wreckage")
    els += [dot(x, y, 4, "#efe6d2", round(wr + .03 * k, 2)) for k, (x, y) in enumerate(scatter(26, db[0] - 46, db[0] + 46, db[1] - 30, db[1] + 30, 4))]
    els += [arrow([[db[0] + 30, db[1] + 24], [r1((db[0] + rw[0]) / 2 + 30), r1((db[1] + rw[1]) / 2 - 40)], [rw[0] - 18, rw[1] - 14]], wr + 1.2, AMBER, 4, dur=1.0),
            person_s(db[0] - 30, db[1] + 120, 70, rc + .3, "#e8d6b8"), lab(db[0] - 30, db[1] + 160, "Mac Brazel", T("Mac Brazel"), BONE, 28)]
    return {"base": "map", "cam": CAM, "els": els}


def s09_debris(C):
    """s9: the debris laid out on the ground at dusk, each piece as named (rubber, foil, paper, sticks); a strip of tape printed with
    small pink flowers; then the two weather balloons Brazel had found before, ghosted in the sky, and a 'not equal' sign."""
    T = lambda ph, dt=0: C.at(8, ph, dt=dt)
    G = 600
    els = [box(-20, G, 1820, 420, "#3a2f24", r=0, at=-1), line([[-20, G], [1800, G]], -1, "#8c7152", 3, draw=False)]
    a = T("Rubber")
    els += [line([[230 + 6 * j, G + 70 - 16 * j], [280, G + 50 - 16 * j], [330, G + 74 - 16 * j], [380, G + 52 - 16 * j], [430, G + 72 - 16 * j]], a + .1 * j, "#77716b", 9, dur=.4, curve=True)
            for j in range(3)] + [lab(330, G + 150, "rubber", a + .2, BONE, 30)]
    b = T("Tinfoil")
    els += [poly([[560, G + 80], [585, G + 20], [640, G + 34], [672, G - 6], [722, G + 26], [744, G + 84], [700, G + 66], [650, G + 92]], "#c9ccd2", "#ffffff", 2, b, fx="pop"),
            line([[600, G + 50], [650, G + 40], [700, G + 58]], b + .1, "#ffffff", 2, draw=False), lab(650, G + 150, "foil", b + .2, BONE, 30)]
    c = T("A rather tough")
    els += [poly([[840, G + 90], [866, G - 6], [1040, G + 12], [1026, G + 100]], "#e8dcc2", "#8a7a66", 2, c, fx="pop"), lab(940, G + 150, "paper", c + .2, BONE, 30)]
    d = T("And sticks")
    els += [line([[1150 + 16 * j, G + 86 - 10 * j], [1390 - 10 * j, G + 20 + 16 * j]], d + .1 * j, "#b08a5a", 7, draw=False) for j in range(3)] + \
           [lab(1270, G + 150, "sticks", d + .2, BONE, 30)]
    f = T("printed with")
    tape = [box(1170, G + 34, 220, 22, "#f0d8e0", "#c9a0b0", 1, 3, f, fx="pop")] + \
           [dot(1186 + 22 * k, G + 45, 5, "#e07aa0", round(f + .3 + .04 * k, 2)) for k in range(10)] + \
           [dot(1186 + 22 * k, G + 45, 2, "#ffe36a", round(f + .3 + .04 * k, 2)) for k in range(10)] + \
           [ring(1280, G + 45, 80, f + .8, GOLD, 3), lab(1280, G - 66, "tape with flowers", f + .9, GOLD, 30)]
    g = T("Brazel said")
    ghosts = []
    for k, (bx, by) in enumerate(((1360, 230), (1530, 270))):
        ghosts += [line([[bx, by + 54], [bx, by + 150]], g + .2 * k, "#cbbca8", 2, "inferred", dur=.5),
                   poly(ellipse(bx, by, 48, 54)[:-1], "rgba(239,230,210,.08)", "#efe6d2", 2.5, round(g + .2 * k, 2), True, style="inferred", fx="pop"),
                   box(bx - 12, by + 150, 24, 18, "none", "#a8865e", 2, 3, round(g + .2 * k, 2), style="inferred")]
    ghosts += [lab(1445, 140, "his two weather balloons", g + .4, DIM, 26), lab(1190, 300, "≠", g + 1.0, BONE, 90, st="big", fx="pop")]
    return {"base": "sky", "tod": "dusk", "ground": G, "groundc": "#3a2f24", "sun": [240, 520, 26], "cam": CAM, "els": els + tape + ghosts}


def s10_fortworth(C):
    """s10: Fort Worth the same evening: the debris on brown paper on an office floor, a general standing over it, two photographers
    whose flashes pop; a dashed weather balloon with its radar target drawn above as the explanation; then a large question mark."""
    T = lambda ph, dt=0: C.at(9, ph, dt=dt)
    F = 640
    els = [box(-20, -20, 1820, F + 20, "#2a211a", r=0, at=-1), box(-20, F, 1820, 400, "#4a3828", r=0, at=-1),
           line([[-20, F], [1800, F]], -1, "#8c7152", 3, draw=False), glow(900, 300, 640, -1, .22, "lamp"),
           lab(889, 168, "Fort Worth, Texas, the same evening", .4, GOLD, 30)]
    els += [poly([[620, F + 40], [1180, F + 26], [1220, F + 110], [580, F + 120]], "#9a7a52", "#6a5236", 2, .5, fx="pop")]
    els += [line([[660 + 30 * j, F + 90 - 8 * j], [760 + 34 * j, F + 70 - 4 * j]], .7, "#d8d4cc", 4, draw=False) for j in range(3)] + \
           [poly([[860, F + 92], [900, F + 52], [960, F + 66], [990, F + 96]], "#c9ccd2", "#ffffff", 1.5, .8, fx="pop"),
            line([[1020, F + 96], [1150, F + 60]], .8, "#b08a5a", 6, draw=False), line([[1040, F + 60], [1160, F + 92]], .8, "#b08a5a", 6, draw=False)]
    gen = T("a general")
    els += [person_s(1380, F + 10, 260, gen, "#c9b48a"), box(1356, F - 210, 48, 10, "#e8c35a", r=2, at=gen + .2)]
    rp = T("showed reporters")
    for k, x in enumerate((300, 470)):
        els += [person_s(x, F + 10, 220, rp + .2 * k, "#e8d6b8"), box(x + 26, F - 168, 44, 30, "#3a3f45", "#9aa0a8", 1.5, 4, rp + .2 * k),
                glow(x + 48, F - 160, 120, rp + .6 + .5 * k, .95, "lamp"), dot(x + 48, F - 160, 10, "#ffffff", rp + .6 + .5 * k)]
    wb = T("a weather")
    els += balloon(900, 300, 60, wb) + reflector(900, 470, .55, wb + .4, style="inferred") + \
           [line([[900, 420], [900, 438]], wb + .4, "#cbbca8", 2, draw=False), lab(1060, 270, "a weather balloon", wb + .5, BONE, 30, "start")]
    q = T("Case")
    els += question(1520, 330, q, 110)
    return {"base": "dark", "cam": CAM, "els": els}


def XM(y):
    """The memory time line: 1940 at x 200, 2000 at x 1580."""
    return r1(260 + (y - 1940) * 21)


AXM = 330


def s11_memory(C):
    """s11: a time line 1940 to 2000: 1947, an arc '31 years' to 1978 where Marcel speaks of a cover story; then about ninety interview
    cards pop over the 1980s and 1990s, and three dotted bubbles: strange metal, threats, bodies."""
    T = lambda ph, dt=0: C.at(10, ph, dt=dt)
    ticks = [[XM(y), str(y)] for y in range(1940, 2001, 10)]
    els = [{"k": "axis", "x0": XM(1940), "x1": XM(2000), "y": AXM, "ticks": ticks, "in": .2},
           dot(XM(1947), AXM, 12, AU, .5), lab(XM(1947) - 24, AXM - 22, "1947", .6, AU, 30, "end")]
    t31 = T("Thirty-one")
    mid = (XM(1947) + XM(1978)) / 2
    els += [arrow([[XM(1947) + 10, AXM - 22], [mid, AXM - 112], [XM(1978) - 8, AXM - 50]], t31, AMBER, 3, dur=1.0), lab(mid, AXM - 56, "31 years", t31 + .4, AMBER, 30)]
    mj = T("Major Jesse")
    els += [person_s(XM(1978), AXM, 150, mj, "#e8d6b8"), lab(XM(1978), AXM + 66, "Jesse Marcel, 1978", mj + .3, BONE, 26)]
    cs = T("cover story")
    bx = XM(1978) - 300
    els += [poly([[bx, 136], [bx + 236, 136], [bx + 236, 196], [bx + 214, 196], [bx + 262, 214], [bx + 186, 196], [bx, 196]], PAPER, "none", 0, cs, fx="pop"),
            ink(bx + 118, 176, "a cover story", cs + .1, INK, 28)]
    hu = T("hundreds")
    cards = [box(r1(x - 14), r1(y - 10), 28, 20, "#e8dcc2", r=3, at=round(hu + .012 * k, 2), op=.7, fx="pop")
             for k, (x, y) in enumerate(scatter(90, XM(1982), XM(2000) - 6, 150, 296, 11))]
    els += cards + [lab(XM(1990), 132, "hundreds of interviews", hu + .6, BONE, 26)]
    for k, (ph, t, x, y) in enumerate((("strange metal", "strange metal", XM(1988), 196), ("threats", "threats", XM(1993), 262), ("bodies", "even bodies", XM(1997), 180))):
        at = T(t)
        w = len(ph) * 15 + 40
        els += [box(r1(x - w / 2), y - 26, r1(w), 44, "rgba(30,24,40,.85)", LILAC, 2, 22, at, style="claimed", fx="pop"), lab(x, y + 6, ph, at + .05, LILAC, 26)]
    return {"base": "dark", "cam": [1.25, 889, 400], "els": els}


def s12_late(C):
    """s12 (alias of s11, a little lower): a bracket '30 to 50 years later' from 1977 to 1997; four sheets in a row, each a copy of the
    last, the balloon on it fading and gaining specks: detail lost, noise added."""
    T = lambda ph, dt=0: C.at(11, ph, dt=dt)
    at0 = .4
    els = [line([[XM(1977), AXM + 92], [XM(1977), AXM + 110], [XM(1997), AXM + 110], [XM(1997), AXM + 92]], at0, AMBER, 3, dur=.8),
           lab((XM(1977) + XM(1997)) / 2, AXM + 146, "30 to 50 years later", at0 + .4, AMBER, 28)]
    ph = T("photocopy of")
    for k in range(4):
        x = 330 + 300 * k
        a = round(ph + .45 * k, 2)
        op = 1 - .2 * k
        els += [box(x - 100, 520, 200, 220, "#e8dcc2", "#8a7a66", 2, 4, a, fx="pop"),
                {"k": "circle", "x": x, "y": 600, "r": 34, "fill": "none", "c": INK, "w": max(1.2, 4 - k), "in": a, "op": op, "keepop": True},
                line([[x, 634], [x, 700]], a, INK, max(1, 3 - .6 * k), draw=False, op=op)]
        els += [dot(px, py, 2.4, "#3a3530", round(a + .1, 2), op=.8) for px, py in scatter(9 * k, x - 90, x + 90, 530, 730, 20 + k)]
        if k:
            els += [arrow([[x - 190, 630], [x - 112, 630]], a - .1, "#cbbca8", 3, dur=.3, curve=False)]
    dl = T("loses")
    els += [lab(630, 778, "detail lost", dl, BONE, 26), lab(1230, 778, "noise added", T("picks up"), BONE, 26)]
    return els


def s13_mogul(C):
    """s13: dawn over the desert: Project Mogul, a train of 23 balloons on one line (20 feet apart: more than 130 m), three radar
    reflectors and a microphone hung below; a person to scale on the ground; far off on the horizon, a faint glow sends sound arcs
    towards the microphone (the far-off boom it listened for)."""
    T = lambda ph, dt=0: C.at(12, ph, dt=dt)
    G = 760
    k_m = 4.0                                    # units a metre: 23 balloons at 6.1 m = 134 m
    tx, top = 1180, 150
    ys = [r1(top + 6.1 * k_m * j) for j in range(23)]
    nm = T("Project")
    els = [lab(560, 220, "Project Mogul", nm, GOLD, 44, st="serif"), lab(560, 268, "named in 1994", nm + .3, DIM, 26)]
    tr = T("Trains of")
    els += [line([[tx, top - 8], [tx, 716]], tr, "#e9dccb", 1.6, dur=1.2, op=.8)]
    els += [oval(tx, y, 8, 9.5, "#efe6d2", "#ffffff", 1, 1, round(tr + .3 + .05 * j, 2), fx="pop") for j, y in enumerate(ys)]
    els += [{"k": "dim", "x1": tx - 60, "y1": ys[0], "x2": tx - 60, "y2": ys[-1], "t": "over 100 m", "c": GOLD, "in": T("more than"), "fx": "draw", "dur": 1.0, "lx": -10}]
    rf = T("radar reflectors")
    for j, y in enumerate((640, 668, 696)):
        els += reflector(tx, y, .22, rf + .2 * j)
    els += [line([[tx + 20, 668], [tx + 120, 640]], rf + .4, BONE, 1.5, draw=False), lab(tx + 130, 648, "radar reflectors", rf + .5, BONE, 26, "start")]
    mc = T("microphone")
    els += [box(tx - 8, 712, 16, 18, "#5b5550", "#e9dccb", 1.5, 3, mc), line([[tx + 14, 720], [tx + 120, 720]], mc + .1, BONE, 1.5, draw=False),
            lab(tx + 130, 728, "a microphone", mc + .2, BONE, 26, "start")]
    els += [person_s(tx + 40, G, 7, tr + 1.4, "#ffe2b4", fx="pop"), ring(tx + 40, G - 4, 14, tr + 1.5, BONE, 1.5), lab(tx + 40, G + 18, "a person, to scale", tr + 1.6, DIM, 24)]
    bm = T("far-off")
    els += [glow(230, G - 10, 150, bm, .7, "red"), dot(230, G - 6, 8, "#ffd08a", bm)]
    for j in range(5):
        r = 160 + 140 * j
        pts = [[r1(230 + r * math.cos(math.radians(a))), r1(G - 6 - r * math.sin(math.radians(a)))] for a in range(6, 38, 3)]
        els.append(line(pts, round(bm + .5 + .35 * j, 2), "#9fd0ff", 2.5, curve=True, dur=.8, op=round(.7 - .1 * j, 2)))
    els += [lab(230, G - 56, "a far-off boom", bm + .3, "#ffb09a", 26)]
    return {"base": "sky", "tod": "dawn", "ground": G, "groundc": "#5a4632", "sun": [1560, G - 40, 26], "cam": CAM, "els": els}


def s14_reflector(C):
    """s14: one radar reflector close up: balsa sticks and foil-paper panes; a toy-block icon ('toy company'); a strip of tape with small
    pink flowers seals one seam; the flower tape from Brazel's pile slides in beside it and a gold ring joins the two."""
    T = lambda ph, dt=0: C.at(13, ph, dt=dt)
    x, y, s = 560, 470, 4.0
    els = [glow(x, y, 520, -1, .2, "lamp")] + reflector(x, y, s, .4)
    tc = T("toy")
    blocks = [box(1080, 230, 64, 64, "#e8b87a", "#fff", 2, 6, tc, fx="pop"), box(1150, 230, 64, 64, "#9fd0ff", "#fff", 2, 6, tc + .1, fx="pop"),
              box(1115, 166, 64, 64, "#e07aa0", "#fff", 2, 6, tc + .2, fx="pop"), lab(1300, 276, "a toy company", tc + .3, BONE, 30, "start")]
    fo, pa, st = T("foil"), T("paper and"), T("balsa")
    names = [lab(x + 210, y - 150, "foil", fo, BONE, 30, "start"), line([[x + 200, y - 158], [x + 90, y - 120]], fo, BONE, 1.5, draw=False),
             lab(x - 230, y + 150, "paper", pa, BONE, 30, "end"), line([[x - 220, y + 140], [x - 110, y + 100]], pa, BONE, 1.5, draw=False),
             lab(x + 230, y + 30, "balsa sticks", st, BONE, 30, "start"), line([[x + 220, y + 20], [x + 150, y + 4]], st, BONE, 1.5, draw=False)]
    fl = T("printed with")
    seam = [[x, y - 60 * s], [x + 46 * s, y]]
    dx, dy = seam[1][0] - seam[0][0], seam[1][1] - seam[0][1]
    L = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    tape = rgroup(ang, seam[0][0], seam[0][1], [box(r1(seam[0][0]), r1(seam[0][1] - 14), r1(L), 28, "#f0d8e0", "#c9a0b0", 1, 3, -1)] +
                  [dot(r1(seam[0][0] + 18 + 26 * k), r1(seam[0][1]), 6, "#e07aa0", -1) for k in range(int(L // 26))] +
                  [dot(r1(seam[0][0] + 18 + 26 * k), r1(seam[0][1]), 2.4, "#ffe36a", -1) for k in range(int(L // 26))], fl)
    els += blocks + names + [tape, lab(x + 160, y - 270, "pink flowers", fl + .3, "#f0b0c8", 30, "start")]
    m = fl + 1.6
    piece = [box(1150, 520, 240, 26, "#f0d8e0", "#c9a0b0", 1, 3, m, fx="rise")] + \
            [dot(1166 + 24 * k, 533, 6, "#e07aa0", m) for k in range(10)] + [dot(1166 + 24 * k, 533, 2.4, "#ffe36a", m) for k in range(10)] + \
            [lab(1270, 600, "from the ranch, 1947", m + .2, DIM, 26)]
    link = [line([[1140, 530], [960, 470], [x + 130, y - 170]], m + .8, GOLD, 3, "inferred", dur=.8, curve=True), lab(1000, 420, "the same tape", m + 1.2, GOLD, 30)]
    return {"base": "dark", "cam": CAM, "els": els + piece + link}


def s15_late(C):
    """s15 (alias of s14): a red TOP SECRET stamp on the reflector; a dotted saucer above the toy blocks, struck through."""
    T = lambda ph, dt=0: C.at(14, ph, dt=dt)
    a = T("A real")
    b = T("Just not")
    return [stamp(600, 590, "TOP SECRET", RED, a + .2, 40, -10)] + saucer(1480, 380, .55, b - .2) + [cross(1380, 420, 1580, 330, b + .3, RED, 6)]


def s16_answers(C):
    """s16: four cards, each drawing its answer as said: a dotted saucer (1947: a disc), a weather balloon (1947: a balloon), a balloon
    train (1994: Mogul), a test dummy under a parachute (1997: dummies); below, an axis 1945 to 1962: 1947 in gold, the dummy drops of
    1954 to 1959 in lilac, and the gap between them."""
    T = lambda ph, dt=0: C.at(15, ph, dt=dt)
    xs = [315, 685, 1055, 1425]
    els = []
    for k, x in enumerate(xs):
        els += [box(x - 165, 150, 330, 380, "rgba(18,13,10,.6)", "#8a7a66", 2, 14, round(.3 + .1 * k, 2))]
    a1, a2, a3, a4 = T("A flying disc"), T("A weather"), T("Project Mogul"), T("test dummies")
    els += saucer(xs[0], 320, .8, a1) + [lab(xs[0], 490, "1947: a disc", a1 + .3, BONE, 28)]
    els += [arrow([[xs[0] + 150, 340], [xs[1] - 150, 340]], a2 - .2, "#cbbca8", 3, dur=.3, curve=False)] + balloon(xs[1], 260, 46, a2) + \
           [lab(xs[1], 490, "1947: a balloon", a2 + .3, BONE, 28)]
    els += [arrow([[xs[1] + 150, 340], [xs[2] - 150, 340]], a3 - .2, "#cbbca8", 3, dur=.3, curve=False),
            line([[xs[2], 186], [xs[2], 440]], a3, "#cbbca8", 2, dur=.5)] + \
           [oval(xs[2], 200 + 34 * j, 13, 15, "#efe6d2", "none", 0, 1, round(a3 + .08 * j, 2), fx="pop") for j in range(5)] + \
           reflector(xs[2], 400, .5, a3 + .5) + [lab(xs[2], 490, "1994: Mogul", a3 + .3, BONE, 28)]
    els += [arrow([[xs[2] + 150, 340], [xs[3] - 150, 340]], a4 - .2, "#cbbca8", 3, dur=.3, curve=False),
            poly(ellipse(xs[3], 250, 90, 60, a0=180, a1=360), "rgba(232,184,122,.25)", AMBER, 2.5, a4, True, fx="pop"),
            line([[xs[3] - 88, 250], [xs[3], 360]], a4 + .1, "#cbbca8", 1.5, draw=False), line([[xs[3] + 88, 250], [xs[3], 360]], a4 + .1, "#cbbca8", 1.5, draw=False),
            person_s(xs[3], 450, 100, a4 + .2, "#9aa0a8"), lab(xs[3], 490, "1997: dummies", a4 + .3, BONE, 28)]
    X = lambda yv: r1(300 + (yv - 1945) * 70)
    ax0 = T("dropped")
    els += [{"k": "axis", "x0": X(1945), "x1": X(1962), "y": 650, "ticks": [[X(y), str(y)] for y in (1945, 1950, 1955, 1960)], "in": ax0},
            dot(X(1947), 650, 11, AU, ax0 + .2), lab(X(1947), 616, "1947", ax0 + .3, AU, 28)]
    yr = T("from nineteen fifty-four")
    els += [box(X(1954), 640, X(1959) - X(1954), 20, LILAC, r=10, at=yr, fx="pop"), lab((X(1954) + X(1959)) / 2, 616, "dummy drops", yr + .3, LILAC, 28)]
    ya = T("years after")
    els += [arrow([[X(1947) + 14, 700], [X(1954) - 6, 700]], ya, AMBER, 3, dur=.6, curve=False), lab((X(1947) + X(1954)) / 2, 742, "7 years later", ya + .3, AMBER, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s17_records(C):
    """s17: an archive shelf of record boxes, 1944 to 1951; the boxes of 1945 to 1949 glow red and vanish; a sheet 'GAO, 1995' with two
    question marks (who, on whose authority); then small dotted saucers sprout in the gap: legends."""
    T = lambda ph, dt=0: C.at(16, ph, dt=dt)
    els = [box(-20, -20, 1820, 1040, CARD, r=0, at=-1), glow(889, 380, 720, -1, .18, "lamp"),
           box(200, 520, 1380, 22, "#6e5440", "#c9a070", 1.5, 3, -1)]
    xs = {y: 230 + 165 * k for k, y in enumerate(range(1944, 1952))}
    for k, (yv, x) in enumerate(xs.items()):
        els += [box(x, 350, 150, 170, "#cdb58a", "#8a6a48", 2, 6, round(.2 + .05 * k, 2), fx="rise"), ink(x + 75, 450, str(yv), round(.25 + .05 * k, 2), INK, 30)]
    ds = T("Destroyed")
    for k, yv in enumerate(range(1945, 1950)):
        x = xs[yv]
        els += [glow(x + 75, 435, 120, round(ds - .3 + .1 * k, 2), .9, "red"), cover(x - 4, 340, 158, 184, CARD, round(ds + .3 + .1 * k, 2), dur=.6)]
    gap = (xs[1945] - 6, xs[1949] + 156)
    els += [box(gap[0], 344, gap[1] - gap[0], 178, "none", "#8a7a66", 2, 8, ds + 1.2, style="inferred"), lab((gap[0] + gap[1]) / 2, 320, "records destroyed", ds + 1.2, RED, 30)]
    ga = T("Congress's auditors")
    els += [box(240, 590, 220, 180, PAPER, "#b8a888", 1.5, 3, ga, fx="pop"), ink(350, 632, "GAO, 1995", ga + .1, INK, 26)] + \
           sheet_lines(266, 664, 168, 4, ga + .2, gap=22) + \
           [lab(540, 650, "who?", T("who destroyed"), LILAC, 32, "start"), lab(540, 720, "on whose authority?", T("on whose"), LILAC, 30, "start")]
    lg = T("But legends")
    rng = random.Random(5)
    for k in range(5):
        cx, cy = gap[0] + 90 + (gap[1] - gap[0] - 180) * k / 4, 420 + rng.uniform(-30, 40)
        els += saucer(r1(cx), r1(cy), .38 + .06 * (k % 2), round(lg + .25 * k, 2))
    els += [lab(1340, 640, "a missing file", T("A missing"), BONE, 30), lab(1340, 690, "is not a spaceship", T("A missing", .5), BONE, 30)]
    return {"base": "dark", "cam": CAM, "els": els}



# ================================================================ chapter 2 · Spy planes and psychic spies (Blue Book, the U-2, Stargate)
def s18_bluebook(C):
    """s18: Project Blue Book, 1952 to 1969: 100 file cards pop in row by row (one card for about 126 reports: 12,618 in all); then 5.6 of
    them turn lilac and glow (701 unexplained)."""
    T = lambda ph, dt=0: C.at(17, ph, dt=dt)
    els = [lab(889, 172, "Project Blue Book", .4, GOLD, 44, st="serif"), lab(889, 214, "1952 to 1969", .8, DIM, 26)]
    x0, y0, cw, chh, px, py = 590, 262, 50, 38, 62, 48
    tw = T("twelve thousand")
    for k in range(100):
        c, r = k % 10, k // 10
        els.append(box(x0 + px * c, y0 + py * r, cw, chh, "#cdb58a", "#8a6a48", 1, 3, round(tw + .02 * k, 2), fx="pop"))
    els += [lab(x0 - 40, 470, "12,618", tw + .4, BONE, 44, "end", st="serif"), lab(x0 - 40, 512, "sightings", tw + .5, BONE, 28, "end"),
            lab(x0 + 10 * px + 30, 290, "one card:", tw + 1.2, DIM, 24, "start"), lab(x0 + 10 * px + 30, 322, "about 126", tw + 1.2, DIM, 24, "start")]
    sv = T("Seven hundred")
    for j, k in enumerate(range(94, 100)):
        c, r = k % 10, k // 10
        w = cw if k > 94 else round(cw * .56, 1)
        xx = x0 + px * c + (cw - w if k == 94 else 0)
        els.append(box(r1(xx), y0 + py * r, w, chh, LILAC, "#ffffff", 1, 3, round(sv + .12 * j, 2), fx="pop"))
    els += [glow(x0 + px * 7.5, y0 + py * 9 + 20, 160, sv + .4, .5, "scan"), lab(x0 + 10 * px + 30, y0 + py * 9 + 28, "701 unexplained", sv + .8, LILAC, 32, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s19_hynek(C):
    """s19: night: an astronomer at a small telescope; beside him a dial whose needle swings from 'sceptic' towards 'worth study'."""
    T = lambda ph, dt=0: C.at(18, ph, dt=dt)
    G = 700
    els = [line([[520, G], [560, G - 130]], .3, "#8a8378", 4, draw=False), line([[600, G], [560, G - 130]], .3, "#8a8378", 4, draw=False),
           line([[560, G], [560, G - 130]], .3, "#8a8378", 3, draw=False),
           rgroup(-32, 560, G - 140, [box(480, G - 158, 200, 34, "#c9ccd2", "#ffffff", 1.5, 8, -1), box(660, G - 162, 30, 42, "#9aa3ad", r=4, at=-1)], .4),
           person_s(440, G, 190, .5, "#e8d6b8"), lab(470, G + 50, "J. Allen Hynek, astronomer", T("astronomer"), BONE, 28)]
    cx, cy, R = 1250, 560, 230
    face = [poly([[cx - R, cy]] + [[r1(cx - R * math.cos(math.radians(a))), r1(cy - R * math.sin(math.radians(a)))] for a in range(0, 181, 10)] + [[cx + R, cy]],
                 "#231b15", "#c9a070", 2.5, .6, fx="pop")]
    face += [line([[r1(cx - (R - 10) * math.cos(math.radians(a))), r1(cy - (R - 10) * math.sin(math.radians(a)))],
                   [r1(cx - (R - 34) * math.cos(math.radians(a))), r1(cy - (R - 34) * math.sin(math.radians(a)))]], .7, "#c9a070", 2, draw=False) for a in range(10, 180, 20)]
    face += [lab(cx - R + 10, cy + 44, "sceptic", .8, BONE, 28), lab(cx + R - 10, cy + 44, "worth study", .8, GREEN, 28)]
    def needle(a, at, c):
        x2, y2 = cx - (R - 50) * math.cos(math.radians(a)), cy - (R - 50) * math.sin(math.radians(a))
        return [line([[cx, cy], [r1(x2), r1(y2)]], at, c, 6, draw=False), dot(cx, cy, 12, c, at)]
    s1, s2 = T("began as"), T("came to")
    x18, y18 = cx - (R - 50) * math.cos(math.radians(18)), cy - (R - 50) * math.sin(math.radians(18))
    els += face + needle(18, s1, AMBER) + [line([[cx, cy], [r1(x18), r1(y18)]], s2, "#231b15", 12, draw=False)] + \
           [arrow([[r1(cx - (R - 80) * math.cos(math.radians(a))), r1(cy - (R - 80) * math.sin(math.radians(a)))] for a in range(24, 137, 8)], s2 + .2, GREEN, 3,
                  "inferred", 1.0)] + needle(140, s2 + 1.0, GREEN)
    return {"base": "sky", "tod": "night", "ground": G, "groundc": "#1d1915", "sun": False, "cam": CAM, "els": els}


def YK(km):
    return r1(720 - km * 28)


def s20_u2(C):
    """s20: an altitude chart at dusk, 0 to 20 km: airliners of the 1950s in a band at 3 to 6 km; the U-2 slides in at about 18 km;
    a dimension shows it at least three times higher; a person on the ground looks up."""
    T = lambda ph, dt=0: C.at(19, ph, dt=dt)
    els = [line([[200, 720], [200, YK(20)]], .3, BONE, 2, dur=.8)] + \
          [line([[192, YK(k)], [208, YK(k)]], .4, BONE, 2, draw=False) for k in (0, 5, 10, 15, 20)] + \
          [lab(184, YK(k) + 9, "%d km" % k, .5, DIM, 24, "end") for k in (0, 5, 10, 15, 20)] + \
          [person_s(330, 720, 70, .6, "#e8d6b8")]
    al = T("at least")
    els += [box(220, YK(6), 1400, YK(3) - YK(6), "rgba(159,208,255,.10)", "rgba(159,208,255,.4)", 1.5, 6, al - 1.2)] + \
           plane_side(820, YK(4.5), 130, al - .9, "#cbd2d8", "liner") + [lab(240, YK(4.5) + 9, "airliners, 1950s", al - .6, BLUE, 28, "start")]
    u2 = T("U two")
    els += plane_side(900, YK(18), 150, u2, "#e6e8ec", "u2") + [lab(900, YK(18) - 56, "U-2, about 18 km", u2 + .3, GOLD, 30)]
    els += [{"k": "dim", "x1": 1500, "y1": 720, "x2": 1500, "y2": YK(6), "t": "6 km", "c": BLUE, "in": al, "fx": "draw", "dur": .6, "lx": -24},
            {"k": "dim", "x1": 1580, "y1": 720, "x2": 1580, "y2": YK(18), "t": "18 km", "c": GOLD, "in": al + .4, "fx": "draw", "dur": 1.0, "lx": 24},
            lab(1460, YK(12) + 10, "3 times higher", al + 1.0, GOLD, 30, "end")]
    return {"base": "sky", "tod": "dusk", "ground": 720, "groundc": "#2a2119", "sun": False, "cam": CAM, "els": els}


def s21_late(C):
    """s21 (alias of s20): the sun just below the horizon at the right: its rays slant up and light only the U-2, which flares
    orange-gold while the ground stays dark; the person raises an arm; a dotted 'UFO?' tag by the bright spot."""
    T = lambda ph, dt=0: C.at(20, ph, dt=dt)
    a = T("At sunrise", dt=.3)
    els = [glow(1700, 760, 260, a, .7, "sun")] + \
          [line([[1700, 740], [960, YK(18) + 10 * k]], round(a + .3 + .1 * k, 2), "#ffcf8a", 2, dur=.8, op=.45) for k in (-1, 0, 1)]
    f = T("silver wings")
    els += [glow(900, YK(18), 120, f, .95, "fire"), glow(900, YK(18), 60, f + .2, .9, "lamp")]
    lf = T("looked like fire")
    els += [line([[322, 664], [300, 620], [290, 590]], lf - .4, "#e8d6b8", 7, dur=.4),
            box(640, YK(18) + 30, 120, 44, "rgba(30,24,40,.85)", LILAC, 2, 22, lf, style="claimed", fx="pop"), lab(700, YK(18) + 60, "UFO?", lf + .05, LILAC, 28)]
    return els


def s22_overhalf(C):
    """s22: 100 report cards (late 1950s and 1960s); more than half of them (55) turn amber with a small U-2 mark: spy flights; three
    cards slide out at the right with a stamp 'natural cause' while a U-2 shows through the paper; 'misleading and deceptive'."""
    T = lambda ph, dt=0: C.at(21, ph, dt=dt)
    x0, y0, cw, chh, px, py = 150, 300, 44, 32, 54, 42
    els = [lab(x0 + 5 * px - 5, 256, "UFO reports, late 1950s and 1960s", .3, BONE, 28)]
    els += [box(x0 + px * (k % 10), y0 + py * (k // 10), cw, chh, "#cdb58a", "#8a6a48", 1, 3, round(.4 + .01 * k, 2), fx="pop") for k in range(100)]
    oh = T("over half")
    order = sorted(range(100), key=lambda k: (k * 37) % 100)[:55]
    for j, k in enumerate(sorted(order)):
        x, y = x0 + px * (k % 10), y0 + py * (k // 10)
        at = round(oh + .02 * j, 2)
        els += [box(x, y, cw, chh, AMBER, "#ffffff", 1, 3, at, fx="pop"), line([[x + 8, y + 16], [x + cw - 8, y + 16]], at, "#3a2c20", 2, draw=False),
                line([[x + 18, y + 9], [x + 18, y + 23]], at, "#3a2c20", 2, draw=False)]
    els += [lab(x0 + 5 * px - 5, y0 + 10 * py + 40, "over half: spy flights", oh + 1.0, AMBER, 30)]
    bb = T("Blue Book staff")
    for k in range(3):
        x, y = 860 + 270 * k, 340 + 30 * k
        at = round(bb + .3 * k, 2)
        els += [box(x, y, 230, 170, PAPER, "#b8a888", 1.5, 4, at, fx="rise")] + \
               [dict(e, op=.3, keepop=True) for e in plane_top(x + 115, y + 70, 80, 150, at + .1, "#c08a4a", 0, fx="pop")] + \
               sheet_lines(x + 22, y + 126, 186, 2, at + .1, gap=20) + [stamp(x + 115, y + 72, "NATURE", "#c0392b", at + .5, 28, -9)]
    md = T("misleading")
    els += [lab(1265, 680, "misleading and deceptive", md, RED, 34, st="serif"), lab(1265, 726, "a CIA history, 1997", md + .3, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def school(x, y, at):
    return [box(x - 70, y - 60, 140, 80, "#b08a62", "#e8dcc2", 2, 3, at, fx="pop"), poly([[x - 84, y - 60], [x, y - 116], [x + 84, y - 60]], "#8a5a3a", "#e8dcc2", 2, at, fx="pop"),
            box(x - 16, y - 30, 32, 50, "#3a2c20", r=2, at=at + .1), dot(x, y - 82, 9, "#e8dcc2", at + .1)]


def club(x, y, at):
    return [oval(x, y - 10, 90, 24, "#6e5440", "#c9a070", 2, 1, at, fx="pop"), line([[x, y + 14], [x, y + 20]], at, "#c9a070", 6, draw=False)] + \
           [person_sit(x + dx, y - 14, 90, at + .1) [1] for dx in (-80, 0, 80)]


def cinema(x, y, at):
    return [glow(x, y - 50, 160, at + .1, .45, "lamp"), box(x - 100, y - 110, 200, 120, "#e8e4da", "#8a8378", 2, 3, at, fx="pop"),
            poly([[x - 60, y - 20], [x - 30, y - 70], [x, y - 40], [x + 30, y - 85], [x + 70, y - 20]], "#b8b0a0", "none", 0, at + .2, fx="pop")]


def s23_panel(C):
    """s23: a CIA panel of five at a long table under a lamp, a folder '1953' with a stamp 'debunk'; then three pictures pop as named:
    a schoolhouse, a club table, a cinema screen ('even Disney')."""
    T = lambda ph, dt=0: C.at(22, ph, dt=dt)
    els = [glow(889, 260, 520, -1, .35, "lamp"), lab(889, 160, "a CIA panel, 1953", .3, GOLD, 32)]
    for k in range(5):
        els += person_sit(589 + 150 * k, 360, 150, round(.4 + .1 * k, 2))
    els += desk(470, 1310, 360, at=.3) + [box(820, 330, 140, 34, "#cdb58a", "#8a6a48", 1.5, 3, .9), ink(890, 356, "1953", .9, INK, 24)]
    db = T("debunk")
    els += [stamp(889, 450, "DEBUNK", RED, db, 34, -8)]
    sc, cl, di = T("schools"), T("clubs"), T("Disney")
    els += school(470, 690, sc) + [lab(470, 760, "schools", sc + .2, BONE, 28)]
    els += club(889, 690, cl) + [lab(889, 760, "clubs", cl + .2, BONE, 28)]
    els += cinema(1320, 690, di) + [lab(1320, 760, "even Disney", di + .2, GOLD, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s24_mind(C):
    """s24: a person seated at a table at the left; a dotted line leaves their head and travels far across the panel to a dim building
    ('the target'); along the bottom, 23 ticks for 23 years, 1972 to 1995."""
    T = lambda ph, dt=0: C.at(23, ph, dt=dt)
    els = [person_s(330, 600, 210, .4, "#e8d6b8"), box(250, 600, 240, 24, "#6e5440", "#c9a070", 1.5, 3, .4), glow(330, 420, 100, .6, .5, "scan")]
    tg = [box(1360, 330, 170, 150, "none", "#8a8378", 3, 4, .8), line([[1360, 330], [1445, 260], [1530, 330]], .8, "#8a8378", 3, dur=.5),
          lab(1445, 530, "the target", .9, DIM, 28)]
    yr = T("twenty-three")
    X = lambda y: r1(300 + (y - 1972) * 52)
    ticks = [line([[X(y), 690], [X(y), 730]], round(yr + .06 * (y - 1972), 2), AMBER, 4, draw=False) for y in range(1972, 1996)]
    ticks += [lab(X(1972), 768, "1972", yr, BONE, 26), lab(X(1995), 768, "1995", yr + 1.4, BONE, 26), lab(X(1983.5), 680, "23 years", yr + .8, AMBER, 28)]
    mi = T("with their")
    beam = [line([[370, 405], [700, 330], [1000, 330], [1350, 390]], mi - .6, LILAC, 3, "claimed", dur=1.4, curve=True), glow(1445, 400, 140, mi + .6, .4, "scan")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els + tg + ticks + beam}


NAMES = ["GONDOLA WISH", "GRILL FLAME", "CENTER LANE", "SUN STREAK", "STAR GATE"]


def s25_codes(C):
    """s25: five manila folders drop in a row as each code name is said, the name on the tab; the last, STAR GATE, gold-lit."""
    T = lambda ph, dt=0: C.at(24, ph, dt=dt)
    els = []
    for k, n in enumerate(NAMES):
        at = T(n.split()[0].title() if k < 4 else "Star")
        x = 120 + 315 * k
        gold = k == 4
        els += folder(x, 360, 290, 300, at, c="#e2c48c" if gold else "#cdb58a", tab=n, tab_x=x + 8, tsize=26 if not gold else 28)
        if gold:
            els += [glow(x + 145, 460, 260, at + .1, .55, "lamp")]
    return {"base": "dark", "cam": CAM, "els": els}


def s26_sketch(C):
    """s26: remote viewing: a sheet with only 'TARGET 4471' typed at the top; a pencil sketch draws itself: a tall frame, a beam, a hook:
    big, metal, a crane?"""
    T = lambda ph, dt=0: C.at(25, ph, dt=dt)
    els = [lab(330, 260, "remote viewing", .4, GOLD, 40, st="serif"), box(640, 150, 680, 620, PAPER, "#fff8ea", 1.2, 4, .3), box(652, 166, 680, 620, "rgba(0,0,0,.35)", r=4, at=-1)]
    els = [els[2], els[0], els[1]]
    nb = T("only a number")
    els += [{"k": "label", "x": 690, "y": 220, "t": "TARGET 4471", "st": "mono", "size": 30, "c": INK, "halo": False, "a": "start", "in": nb, "fx": "type", "dur": 1.0}]
    sk = T("sketched")
    els += [line([[800, 700], [800, 360], [1180, 360], [1180, 700]], sk, INK, 3, dur=1.2),
            line([[770, 360], [1210, 360]], sk + 1.0, INK, 5, dur=.6),
            line([[1040, 360], [1040, 470], [1010, 500], [1070, 500]], sk + 1.4, INK, 2.5, dur=.8),
            line([[740, 700], [1240, 700]], sk + 1.8, INK, 2, dur=.6),
            {"k": "label", "x": 990, "y": 310, "t": "big, metal, a crane?", "st": "ital", "size": 34, "c": "#7a2a1a", "halo": False, "in": sk + 2.2, "fx": "type", "dur": 1.0}]
    return {"base": "dark", "cam": CAM, "els": els}


def s27_chance(C):
    """s27: a coin lands heads, tails... twenty small coins fall into two columns that end level ('chance: about half'); a small bar
    chart with a dashed line 'chance' and a dotted bar 'viewers?' trying to rise above it."""
    T = lambda ph, dt=0: C.at(26, ph, dt=dt)
    ct = T("coin")
    els = [{"k": "circle", "x": 420, "y": 250, "r": 46, "fill": AU, "c": "#fff3c4", "w": 3, "in": ct - .3, "fx": "pop"}, lab(420, 262, "?", ct - .2, INK, 40, st="serif", halo=False)]
    seq = [0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
    hcount = [0, 0]
    for j, side in enumerate(seq):
        n = hcount[side]; hcount[side] += 1
        x = 330 if side == 0 else 510
        els.append({"k": "circle", "x": x, "y": 680 - 26 * n, "r": 14, "fill": AU, "c": "#fff3c4", "w": 1.5, "in": round(ct + .2 + .08 * j, 2), "fx": "pop"})
    els += [lab(330, 730, "heads", ct + .3, BONE, 26), lab(510, 730, "tails", ct + .3, BONE, 26),
            lab(420, 380, "chance: about half", ct + 2.0, AMBER, 30)]
    bc = T("The question")
    bx0, by0 = 950, 680
    els += [line([[bx0, by0], [bx0 + 560, by0]], bc, BONE, 2, dur=.5), line([[bx0, by0], [bx0, 300]], bc, BONE, 2, dur=.5),
            box(bx0 + 70, 470, 150, by0 - 470, AMBER, r=4, at=bc + .3, fx="fill", dur=.8), lab(bx0 + 145, by0 + 40, "chance", bc + .4, AMBER, 26),
            line([[bx0, 470], [bx0 + 560, 470]], bc + .6, AMBER, 2.5, "inferred", dur=.6),
            box(bx0 + 330, 390, 150, by0 - 390, "rgba(201,193,238,.12)", LILAC, 3, 4, T("beat chance"), style="claimed", fx="fill", dur=1.2),
            lab(bx0 + 405, by0 + 40, "viewers?", T("beat chance") + .2, LILAC, 26), lab(bx0 + 405, 350, "again and again?", T("again and"), LILAC, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s28_closed(C):
    """s28: a report of 1995 on a desk; a fog rolls over its lines at 'vague and ambiguous'; a big 0 for operations guided; a row of 23
    small stacks of banknotes (about $20 million over 23 years); a red CLOSED stamp on the report."""
    T = lambda ph, dt=0: C.at(27, ph, dt=dt)
    els = [box(200, 160, 420, 560, PAPER, "#b8a888", 1.5, 4, .3), ink(410, 214, "EVALUATION, 1995", .4, INK, 26)] + sheet_lines(240, 260, 340, 14, .5, gap=30)
    vg = T("vague")
    els += [glow(410, 470, 300, vg, .9, "scan"), oval(410, 470, 220, 150, "#d8dde2", "none", 0, .6, vg + .3), oval(330, 400, 120, 70, "#d8dde2", "none", 0, .45, vg + .5),
            oval(500, 560, 130, 80, "#d8dde2", "none", 0, .45, vg + .6), lab(410, 770, "vague and ambiguous", vg + .6, BONE, 30, st="ital")]
    op = T("never guided")
    els += [lab(960, 410, "0", op, BONE, 150, st="big", fx="pop"), lab(960, 470, "operations guided", op + .3, BONE, 28)]
    mn = T("twenty million")
    for k in range(23):
        x = 1100 + 24 * k
        els += [box(x, 640 - 14 * j, 20, 12, "#8fbf8a", "#3a5a3a", 1, 2, round(mn + .03 * k + .02 * j, 2)) for j in range(3)]
    els += [lab(1376, 700, "about $20 million", mn + .5, "#8fd9b0", 28), lab(1376, 740, "over 23 years", mn + .7, DIM, 24)]
    sd = T("shut")
    els += [stamp(410, 660, "CLOSED", "#c0392b", sd, 56, -12)]
    return {"base": "dark", "cam": CAM, "els": els}


def s29_declass(C):
    """s29: three documents rise from a dark drawer as named: a budget sheet with bars, a folder tab STAR GATE, a bound report '1995';
    a DECLASSIFIED stamp lands across them."""
    T = lambda ph, dt=0: C.at(28, ph, dt=dt)
    els = [glow(889, 400, 600, -1, .25, "lamp")]
    bu, cn, fr = T("budgets"), T("code names"), T("a final")
    bud = [box(400, 230, 260, 330, PAPER, "#b8a888", 1.5, 3, bu, fx="rise"), ink(530, 270, "BUDGET", bu + .1, INK, 24)] + \
          [box(440 + 46 * k, 520 - h, 30, h, "#8fbf8a", "#3a5a3a", 1, 2, round(bu + .3 + .1 * k, 2), fx="fill") for k, h in enumerate((60, 110, 150, 90, 70))]
    fol = folder(770, 250, 250, 310, cn, c="#e2c48c", tab="STAR GATE", tab_x=780, tsize=26)
    rep = [box(1130, 230, 250, 330, "#3a4a5a", "#9fb0c0", 2, 4, fr, fx="rise"), box(1130, 230, 26, 330, "#2a3644", r=2, at=fr),
           lab(1268, 380, "FINAL", fr + .1, BONE, 26), lab(1268, 420, "REPORT", fr + .1, BONE, 26), lab(1268, 480, "1995", fr + .15, GOLD, 30)]
    drawer = [box(340, 560, 1100, 170, "#3a2c20", "#8c7152", 2, 6, .2), box(820, 620, 140, 22, "#8c7152", r=8, at=.3)]
    st = fr + 1.4
    return {"base": "dark", "cam": CAM, "els": els + bud + fol + rep + drawer + [stamp(889, 400, "DECLASSIFIED", RED, st, 44, -7)]}



# ================================================================ chapter 3 · The Tic Tac tapes (2017 to 2021)
def flir(x, y, w, h, at, blob, tag, tag_at):
    """An infrared targeting screen: dark green, crosshairs, a white heat signature, its tag under it."""
    cx, cy = x + w / 2, y + h / 2
    out = [box(x, y, w, h, FLIR, "#2f5a3a", 2, 6, at, fx="pop"),
           line([[cx, y + 30], [cx, cy - 40]], at + .1, FLIRG, 1.6, draw=False, op=.8), line([[cx, cy + 40], [cx, y + h - 30]], at + .1, FLIRG, 1.6, draw=False, op=.8),
           line([[x + 30, cy], [cx - 40, cy]], at + .1, FLIRG, 1.6, draw=False, op=.8), line([[cx + 40, cy], [x + w - 30, cy]], at + .1, FLIRG, 1.6, draw=False, op=.8),
           box(cx - 40, cy - 40, 80, 80, "none", FLIRG, 1.6, 2, at + .1), lab(x + 16, y + 32, "IR", at + .1, FLIRG, 24, "start", st="mono", halo=False)]
    out += blob(cx, cy, tag_at)
    out += [lab(cx, y + h + 44, tag, tag_at + .2, BONE, 28)]
    return out


def s30_times(C):
    """s30: a newspaper page (schematic, December 2017) at the left; an axis 2006 to 2013 with a gold band 2007 to 2012 ('the hidden study')
    and 22 small coin stacks rising along it ('about $22 million'); a film strip slides out of the paper at 'videos'."""
    T = lambda ph, dt=0: C.at(29, ph, dt=dt)
    els = [box(150, 170, 500, 580, PAPER, "#fff8ea", 1.2, 4, .3), ink(400, 222, "THE NEW YORK TIMES", .4, INK, 28, st="serif"),
           line([[180, 240], [620, 240]], .4, INK, 2, draw=False), ink(400, 268, "December 2017", .5, "#6a645c", 24, st="small"),
           box(180, 290, 440, 26, INK, r=3, at=.6), box(180, 326, 300, 22, INK, r=3, at=.65)] + \
          sheet_lines(180, 380, 200, 13, .7, gap=24) + sheet_lines(410, 380, 210, 13, .75, gap=24)
    X = lambda yv: r1(800 + (yv - 2006) * 120)
    st = T("The Pentagon had")
    els += [{"k": "axis", "x0": X(2006), "x1": X(2013), "y": 450, "ticks": [[X(y), str(y)] for y in range(2006, 2014)], "in": st},
            box(X(2007), 400, X(2012) - X(2007), 22, GOLD, r=11, at=T("from two thousand"), fx="pop"),
            lab((X(2007) + X(2012)) / 2, 548, "a hidden UFO study", T("from two thousand") + .3, GOLD, 30)]
    mn = T("twenty-two")
    for k in range(22):
        x = X(2007) + 8 + k * (X(2012) - X(2007) - 16) / 21
        els += [box(r1(x - 9), 389 - 8 * j, 18, 7, AU, "#8a6a2a", 1, 2, round(mn + .04 * k + .03 * j, 2)) for j in range(3)]
    els += [lab((X(2007) + X(2012)) / 2, 340, "about $22 million", mn + 1.0, AU, 30)]
    vd = T("Navy")
    fx0, fy0 = 900, 620
    els += [box(fx0, fy0, 330, 70, "#1a1511", "#8a8378", 2, 4, vd, fx="rise")] + \
           [box(fx0 + 16 + 40 * k, fy0 + 10, 28, 12, "#8a8378", r=2, at=vd) for k in range(8)] + [box(fx0 + 16 + 40 * k, fy0 + 48, 28, 12, "#8a8378", r=2, at=vd) for k in range(8)] + \
           [box(fx0 + 50, fy0 + 26, 70, 18, FLIR, FLIRG, 1, 2, vd + .2), box(fx0 + 160, fy0 + 26, 70, 18, FLIR, FLIRG, 1, 2, vd + .2),
            arrow([[660, fy0 + 35], [fx0 - 16, fy0 + 35]], vd, FLIRG, 2.5, dur=.5, curve=False), lab(fx0 + 350, fy0 + 45, "Navy videos", vd + .3, FLIRG, 30, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def s31_screens(C):
    """s31: three infrared screens in a row: the Tic Tac (2004), Gimbal (2015, a glare that turns), Go Fast (2015, a dot over the sea);
    'infrared: heat, not light' above them."""
    T = lambda ph, dt=0: C.at(30, ph, dt=dt)
    hx = T("heat")
    els = [lab(889, 176, "infrared: heat, not light", hx, FLIRG, 30)]

    def b_tic(cx, cy, at):
        return [glow(cx, cy, 70, at, .5, "scan"), box(cx - 30, cy - 11, 60, 22, "#f4fff2", r=11, at=at, fx="pop")]

    def b_gim(cx, cy, at):
        return [glow(cx, cy, 80, at, .6, "scan")] + \
               [poly(rot(ellipse(cx, cy, 34, 13)[:-1], cx, cy, a), "none", "#f4fff2", 2, round(at + .25 * j, 2), True, op=.3 + .2 * j, keepop=True) for j, a in enumerate((-30, -12, 6))] + \
               [poly(rot(ellipse(cx, cy, 22, 9)[:-1], cx, cy, 6), "#0a120c", "#f4fff2", 3, at + .6, True)]

    def b_go(cx, cy, at):
        return [line([[cx - 200 + 40 * j, cy + 30 + 18 * (j % 3)], [cx - 170 + 40 * j, cy + 30 + 18 * (j % 3)]], at, "#7a8a7e", 2, draw=False, op=.6) for j in range(10)] + \
               [glow(cx, cy, 40, at, .6, "scan"), dot(cx, cy, 7, "#f4fff2", at)]
    a0 = .4
    xs = [110, 654, 1198]
    els += flir(xs[0], 250, 470, 300, a0, b_tic, "2004: the Tic Tac", T("One from"))
    els += flir(xs[1], 250, 470, 300, a0 + .15, b_gim, "2015: Gimbal", T("Gimbal"))
    els += flir(xs[2], 250, 470, 300, a0 + .3, b_go, "2015: Go Fast", T("Go Fast"))
    return {"base": "dark", "cam": CAM, "els": els}


def s32_late(C):
    """s32 (alias of s31): a stamp 'released 2020' across the screens; then the letters UAP, with their three words under them."""
    T = lambda ph, dt=0: C.at(31, ph, dt=dt)
    rl = T("released")
    u = T("UAP")
    els = [stamp(889, 400, "RELEASED 2020", GOLD, rl, 40, -5)]
    for k, (L, w) in enumerate((("U", "unidentified"), ("A", "anomalous"), ("P", "phenomena"))):
        x = 650 + 240 * k
        els += [lab(x, 712, L, u + .25 * k, BONE, 80, st="big", fx="pop"), lab(x, 770, w, u + 1.0 + .5 * k, DIM, 26)]
    return els


def s33_train(C):
    """s33: a train window (dark carriage around it): outside, fence posts streak past and a cow slides by with speed lines; then the
    view holds and the cow gets its tag: standing still."""
    T = lambda ph, dt=0: C.at(32, ph, dt=dt)
    els = [box(-20, -20, 1820, 1040, "#1d1712", r=0, at=-1)]
    wx, wy, ww, wh = 360, 170, 1060, 500
    els += [{"k": "group", "clip": [wx, wy, ww, wh, 30], "bg": "#9cc3d8", "in": .2,
             "els": [box(wx, wy + 300, ww, 220, "#6f9a52", r=0, at=-1), box(wx, wy + 300, ww, 4, "#4f7a40", r=0, at=-1),
                     oval(wx + 260, wy + 120, 90, 30, "#eef4f7", at=-1), oval(wx + 780, wy + 90, 70, 22, "#eef4f7", at=-1),
                     poly([[wx, wy + 300], [wx + 200, wy + 250], [wx + 420, wy + 280], [wx + 700, wy + 240], [wx + ww, wy + 290], [wx + ww, wy + 300]], "#7fa6b4", "none", 0, -1, True)]},
            box(wx, wy, ww, wh, "none", "#5a4a3a", 14, 30, .2), box(wx - 40, wy + wh + 10, ww + 80, 40, "#3a2c20", "#6a5440", 2, 6, .2)]
    sp = T("speeding")
    for k in range(8):
        x = wx + 60 + 120 * k
        els += [line([[x, wy + 330], [x + 90, wy + 330]], round(sp + .05 * k, 2), "#4a3a2a", 10, draw=True, dur=.25, op=.7),
                line([[x + 20, wy + 345], [x + 120, wy + 345]], round(sp + .05 * k, 2), "#4a3a2a", 3, draw=True, dur=.25, op=.4)]
    cw = T("a cow")
    els += cow(wx + 520, wy + 420, 1.0, cw)
    els += [line([[wx + 600, wy + 360 + 16 * j], [wx + 860 - 40 * j, wy + 360 + 16 * j]], round(cw + .1 * j, 2), "#f5f0e8", 3, dur=.4, op=.6) for j in range(4)]
    els += [lab(889, 140, "a cow seems to race past", T("seems"), BONE, 30)]
    stl = T("standing still")
    els += [box(wx + 330, wy + 440, 380, 50, "rgba(18,13,10,.85)", GREEN, 2, 25, stl, fx="pop"), lab(wx + 520, wy + 474, "0 km/h: standing still", stl + .05, GREEN, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s34_gofast(C):
    """s34: a side view over the sea: the jet high at the left; its camera's sight line slants down past a small white object about
    4,000 m up to the sea far beyond. As the jet moves on, the sight line sweeps a long way across the sea (what the camera sees race past)
    while the object moves only a short way (about 65 km/h, the wind)."""
    T = lambda ph, dt=0: C.at(33, ph, dt=dt)
    SEA = 720
    els = [{"k": "water", "y": SEA, "h": 400, "op": .9, "in": -1}, lab(889, 160, "NASA, 2023: Go Fast", .4, GOLD, 32)]
    j1, j2, o1, o2 = (250, 230), (520, 230), (880, 448), (905, 448)
    sea = lambda j, o: r1(j[0] + (SEA - j[1]) * (o[0] - j[0]) / (o[1] - j[1]))
    s1, s2 = sea(j1, o1), sea(j2, o2)
    rd = T("worked out")
    els += [jet_side(j1[0], j1[1], 110, .5, "#cbd2d8", 1), line([j1, [s1, SEA]], rd, BLUE, 2, "inferred", dur=1.0),
            tictac(o1[0], o1[1], 26, rd + .4, glow_op=.4)[1], dot(o1[0], o1[1], 7, "#ffffff", rd + .4)]
    up = T("four thousand")
    els += [{"k": "dim", "x1": 820, "y1": SEA, "x2": 820, "y2": o1[1], "t": "about 4,000 m", "c": GOLD, "in": up, "fx": "draw", "dur": .8, "lx": -26}]
    mv = T("moving at")
    els += [jet_side(j2[0], j2[1], 110, mv, "#cbd2d8", 1, op=.55), arrow([[j1[0] + 70, j1[1] - 30], [j2[0] - 70, j2[1] - 30]], mv, BONE, 2.5, dur=.6, curve=False),
            line([j2, [s2, SEA]], mv + .3, BLUE, 2, "inferred", dur=.8),
            arrow([[s1, SEA + 30], [s2 + 10, SEA + 30]], mv + 1.0, BLUE, 4, dur=.8, curve=False), lab((s1 + s2) / 2, SEA + 62, "the sea races past", mv + 1.2, BLUE, 28),
            arrow([[o1[0] + 16, o1[1] - 26], [o2[0] + 30, o2[1] - 26]], mv + .6, AU, 4, dur=.5, curve=False), lab(o1[0] + 20, o1[1] - 52, "about 65 km/h", mv + .8, AU, 28)]
    wd = T("a typical")
    els += [arrow([[990 + 30 * j, 430 + 24 * j], [1090 + 30 * j, 430 + 24 * j]], round(wd + .2 * j, 2), "#cfe6ff", 2.5, dur=.6, curve=False) for j in range(3)] + \
           [lab(1170, 470, "the wind at that height", wd + .6, "#cfe6ff", 28, "start")]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [1560, 180, 24], "cam": CAM, "els": els}


def ship(x, y, L, at, c="#3a434c"):
    """A warship on the horizon, side view, bow left."""
    hull = [[x - L / 2, y - L * .06], [x + L / 2, y - L * .06], [x + L * .46, y], [x - L * .42, y]]
    sup = [[x - L * .12, y - L * .06], [x - L * .1, y - L * .16], [x + L * .02, y - L * .16], [x + L * .04, y - L * .22], [x + L * .1, y - L * .22],
           [x + L * .12, y - L * .06]]
    return [poly(hull, c, "#8a96a2", 1.2, at, fx="pop"), poly(sup, c, "#8a96a2", 1.2, at, fx="pop")]


def s35_nimitz(C):
    """s35: the sea again, wide: two jets, each with two seats that light one by one (four aviators); the white capsule over a churn with a
    question mark; on the horizon a warship whose radar sweeps, 14 day ticks above it ('two weeks, Fravor says')."""
    T = lambda ph, dt=0: C.at(34, ph, dt=dt)
    H0 = 420
    els = [{"k": "water", "y": H0, "h": 640, "op": .9, "in": -1}]
    els += [poly(ellipse(560, 600, rx, ry)[:-1], "none", "#f2fbff", 2, -1, True, op=.45, keepop=True) for rx, ry in ((110, 20), (150, 28))] + \
           [oval(560, 600, 90, 16, "rgba(240,250,255,.4)", at=-1)] + tictac(560, 520, 70, .4, glow_op=.4)
    fa = T("four aviators")
    for k, (x, y) in enumerate(((720, 230), (1000, 270))):
        els += [jet_side(x, y, 150, .3 + .2 * k, "#aab2bb", -1)]
        for j in range(2):
            sx = x - 150 * .5 + 150 * (.30 + .07 * j) * 1
            els += [dot(r1(x + (.30 + .07 * j - .5) * 150), r1(y - 150 * .1), 6, GOLD, round(fa + .3 * (2 * k + j), 2)),
                    glow(r1(x + (.30 + .07 * j - .5) * 150), r1(y - 150 * .1), 26, round(fa + .3 * (2 * k + j), 2), .8, "lamp")]
    els += [lab(860, 150, "four aviators", fa + 1.2, GOLD, 30)]
    rd = T("radar")
    els += ship(1420, H0 + 6, 200, .5) + \
           [line([[r1(1420 + R * math.cos(math.radians(a))), r1(H0 - 40 - R * math.sin(math.radians(a)))] for a in range(20, 161, 10)], round(rd + .3 * j, 2), "#9fd0ff", 2,
                 curve=True, dur=.6, op=round(.75 - .15 * j, 2)) for j, R in enumerate((60, 110, 160))]
    tw = T("two weeks")
    els += [line([[1300 + 18 * k, 180], [1300 + 18 * k, 200]], round(tw + .05 * k, 2), BONE, 3, draw=False) for k in range(14)] + \
           [lab(1418, 160, "two weeks, Fravor says", tw + .5, BONE, 26)]
    ne = T("No official")
    els += question(560, 460, ne - .2, 70) + [lab(560, 690, "no official explanation", ne + .3, LILAC, 30)]
    return {"base": "sky", "tod": "day", "ground": 1200, "sun": [200, 170, 22], "cam": CAM, "els": els}


V_VA = View(-80.6, -70.4, 34.2, 39.4, (90, 120, 1600, 680))


def s36_graves(C):
    """s36: the US east coast at Virginia (map): a dashed training area offshore; a jet track loops inside it and small white dots pop in
    it, day after day; a run of ticks along the bottom: every day, for years (his account)."""
    T = lambda ph, dt=0: C.at(35, ph, dt=dt)
    v = V_VA
    vb = v.p(-75.98, 36.85)
    bx = [v.p(-75.2, 37.7), v.p(-73.0, 37.7), v.p(-73.0, 35.9), v.p(-75.2, 35.9)]
    els = [{"k": "map", "land": v.land(), "in": -1}, lab(*v.p(-78.6, 37.6), "Virginia", .3, "#c9ad85", 34, st="ital"),
           {"k": "pin", "x": vb[0], "y": vb[1], "t": "Virginia Beach", "c": GOLD, "a": "end", "lx": -20, "in": .5},
           poly(bx, "rgba(159,208,255,.06)", BLUE, 2.5, .8, style="inferred"), lab(r1((bx[0][0] + bx[1][0]) / 2), r1(bx[0][1] - 18), "a training area", 1.0, BLUE, 26)]
    rg = T("Ryan")
    cx, cy = (bx[0][0] + bx[1][0]) / 2, (bx[0][1] + bx[2][1]) / 2
    els += [line([[r1(cx + 150 * math.cos(math.radians(a)) * (1 + .1 * math.sin(math.radians(3 * a)))), r1(cy + 90 * math.sin(math.radians(a)))] for a in range(0, 361, 15)],
                 rg, "#e8d6b8", 2, dur=1.4, curve=True, op=.7), jet_side(r1(cx + 150), r1(cy + 6), 60, rg + 1.2, "#e8d6b8", 1),
            lab(r1(bx[1][0] + 30), r1(cy - 40), "Ryan Graves", rg + .3, BONE, 30, "start"), lab(r1(bx[1][0] + 30), r1(cy), "his account", rg + .5, DIM, 26, "start")]
    ed = T("every day")
    pts = scatter(60, bx[0][0] + 30, bx[1][0] - 30, bx[0][1] + 30, bx[2][1] - 30, 9)
    els += [dot(x, y, 5, "#ffffff", round(ed + .03 * k, 2), op=.85) for k, (x, y) in enumerate(pts)]
    yr = T("couple of years")
    els += [line([[r1(900 + 9 * k), 760], [r1(900 + 9 * k), 784]], round(ed + .02 * k, 2), BONE, 2, draw=False, op=.7) for k in range(70)] + \
           [lab(880, 778, "every day", ed + .4, BONE, 26, "end"), lab(1550, 778, "for years", yr, BONE, 26, "start")]
    return {"base": "map", "cam": CAM, "els": els}


def s37_reports(C):
    """s37: 144 grey dots in a 16 x 9 block (the 2021 review); one turns green, a small sagging balloon beside it (1 explained); then
    most of the rest dim behind a veil (not enough data)."""
    T = lambda ph, dt=0: C.at(36, ph, dt=dt)
    els = [box(-20, -20, 1820, 1040, CARD, r=0, at=-1)]
    x0, y0, p = 320, 280, 44
    rp = T("a hundred and")
    els += [lab(x0 + 7.5 * p, 220, "144 reports, 2021", rp, BONE, 32)]
    els += [dot(x0 + p * (k % 16), y0 + p * (k // 16), 12, "#8a8378", round(rp + .01 * k, 2)) for k in range(144)]
    ex = T("explain")
    gx, gy = x0 + p * 15, y0 + p * 8
    els += [dot(gx, gy, 15, GREEN, ex + .3), glow(gx, gy, 60, ex + .3, .7, "scan"),
            line([[gx + 40, gy - 10], [1250, 520]], ex + .5, GREEN, 2, "inferred", dur=.5),
            poly([[1250, 500], [1290, 460], [1340, 470], [1360, 520], [1330, 560], [1290, 556], [1262, 540]], "rgba(143,217,176,.15)", GREEN, 2.5, ex + .8, True, fx="pop"),
            line([[1310, 556], [1312, 620]], ex + .9, GREEN, 2, draw=False), lab(1310, 670, "1 explained:", ex + 1.0, GREEN, 30), lab(1310, 710, "a deflating balloon", ex + 1.1, GREEN, 28)]
    nd = T("wasn't enough")
    els += [cover(x0 - 20, y0 - 20, 15 * p + 34, 7 * p + 42, CARD, nd, op=.72, dur=.8), cover(x0 - 20, y0 + 8 * p - 22, 14 * p + 42, 44, CARD, nd, op=.72, dur=.8),
            lab(x0 + 7 * p, y0 + 4 * p + 10, "not enough data", nd + .3, BONE, 34)]
    return {"base": "dark", "cam": CAM, "els": els}


def s38_bird(C):
    """s38: a large circle 'unexplained' and a small dotted circle 'alien' with a not-equal sign; a photo frame with a blurred bird:
    'unidentified bird'; a dotted tag 'new species?' struck through."""
    T = lambda ph, dt=0: C.at(37, ph, dt=dt)
    ue = T("unexplained")
    al = T("alien")
    els = [oval(460, 440, 230, 230, "rgba(159,208,255,.10)", BLUE, 3, 1, ue, fx="pop"), lab(460, 450, "unexplained", ue + .2, BLUE, 34),
           oval(860, 440, 95, 95, "rgba(201,193,238,.06)", LILAC, 3, 1, al, style="claimed", fx="pop"), lab(860, 450, "alien", al + .2, LILAC, 30),
           lab(710, 470, "≠", al + .5, BONE, 96, st="big", fx="pop")]
    bd = T("A bird")
    fx0, fy0 = 1110, 220
    els += [box(fx0, fy0, 440, 320, "#c8ccc6", "#f5f0e8", 8, 4, bd, fx="pop")]
    bird = lambda x, y: [[x - 60, y - 10], [x - 20, y - 30], [x, y - 8], [x + 20, y - 30], [x + 60, y - 12], [x + 10, y + 6], [x - 10, y + 6]]
    for j, (dx, dy, op) in enumerate(((-8, 4, .25), (6, -3, .3), (0, 0, .55))):
        els.append(poly(bird(fx0 + 220 + dx, fy0 + 160 + dy), "#4a4a4a", "none", 0, round(bd + .2 + .1 * j, 2), True, op=op, keepop=True))
    ub = T("unidentified bird")
    ns = T("new species")
    els += [lab(fx0 + 220, fy0 + 380, "unidentified bird", ub, BONE, 30),
            box(fx0 + 110, fy0 + 420, 220, 50, "rgba(30,24,40,.85)", LILAC, 2, 25, ns, style="claimed", fx="pop"), lab(fx0 + 220, fy0 + 455, "new species?", ns + .05, LILAC, 26),
            cross(fx0 + 100, fy0 + 470, fx0 + 340, fy0 + 420, ns + .5, RED, 5)]
    return {"base": "dark", "cam": CAM, "els": els}



# ================================================================ chapter 4 · Under oath (2023 to 2026)
def s39_hearing(C):
    """s39: the hearing room wide: a raised dais with members at the top, a witness table with three people seated and microphones; the
    middle witness lit: David Grusch, beside two Navy pilots; '26 July 2023'."""
    T = lambda ph, dt=0: C.at(38, ph, dt=dt)
    els = [box(-20, -20, 1820, 1040, "#211913", r=0, at=-1), glow(889, 420, 760, -1, .18, "lamp"),
           box(200, 220, 1378, 64, "#4a3626", "#c9a070", 1.5, 6, -1), box(200, 284, 1378, 36, "#2f2219", r=0, at=-1)]
    els += [{"k": "circle", "x": 270 + 124 * k, "y": 196, "r": 16, "fill": "#7a6a58", "c": "none", "w": 0, "in": -1} for k in range(11)] + \
           [box(252 + 124 * k, 210, 36, 14, "#7a6a58", r=6, at=-1) for k in range(11)]
    gr = T("David")
    pl = T("two former")
    for k, x in enumerate((560, 889, 1218)):
        at = gr if k == 1 else pl + .2 * (k // 2)
        els += person_sit(x, 600, 240, at, "#e8d6b8" if k == 1 else "#c9bba6") + mic(x + 40, 600, at)
    els += desk(380, 1398, 600) + [glow(889, 470, 200, gr + .2, .45, "lamp")]
    els += [lab(889, 690, "David Grusch", gr + .3, GOLD, 30), lab(560, 690, "Navy pilot", pl + .3, BONE, 28), lab(1218, 690, "Navy pilot", pl + .5, BONE, 28),
            lab(1218, 730, "David Fravor", T("one of them"), DIM, 24), lab(889, 380, "26 July 2023, under oath", .5, DIM, 26)]
    return {"base": "dark", "cam": CAM, "els": els}


def s40_claims(C):
    """s40: everything in the claimed style (lilac, dotted): a hangar outline; inside it a dotted craft; a long dotted band 'decades';
    then a dotted stretcher with a covered shape; labels 'claimed: craft', 'claimed: bodies'."""
    T = lambda ph, dt=0: C.at(39, ph, dt=dt)
    hg = [[260, 700], [260, 400]] + [[r1(680 - 420 * math.cos(math.radians(a))), r1(400 - 170 * math.sin(math.radians(a)))] for a in range(0, 181, 10)] + [[1100, 400], [1100, 700]]
    dc = T("decades-long")
    els = [line(hg, dc, LILAC, 3, "claimed", dur=1.2), line([[220, 700], [1600, 700]], dc, LILAC, 2, "claimed", dur=.8, op=.6),
           box(300, 186, 760, 26, "rgba(201,193,238,.10)", LILAC, 2, 13, dc + .6, style="claimed", fx="pop"), lab(680, 172, "decades?", dc + .8, LILAC, 28)]
    cr = T("recover crashed")
    els += [poly(ellipse(680, 600, 190, 46)[:-1], "rgba(201,193,238,.08)", LILAC, 3, cr, True, style="claimed", fx="pop"),
            poly(ellipse(680, 572, 80, 46, a0=180, a1=360), "rgba(201,193,238,.08)", LILAC, 3, cr + .3, True, style="claimed", fx="pop"),
            lab(680, 760, "claimed: crashed craft", cr + .5, LILAC, 30)]
    bd = T("bodies came")
    els += [line([[1280, 640], [1560, 640]], bd, LILAC, 3, "claimed", dur=.5), line([[1300, 640], [1300, 690]], bd, LILAC, 3, "claimed", dur=.3),
            line([[1540, 640], [1540, 690]], bd, LILAC, 3, "claimed", dur=.3),
            poly([[1290, 636], [1330, 590], [1500, 584], [1550, 610], [1550, 636]], "rgba(201,193,238,.08)", LILAC, 3, bd + .3, True, style="claimed", fx="pop"),
            lab(1420, 760, "claimed: bodies", bd + .5, LILAC, 30), lab(1420, 520, "non-human biologics", T("biologics"), LILAC, 26, st="ital")]
    return {"base": "dark", "cam": CAM, "els": els}


def s41_chain(C):
    """s41: five people in a row; a speech bubble passes from one to the next, growing fainter, to Grusch at the end, lit; a closed door
    with a lock ('access denied'); a magnifier finds nothing to test; a Pentagon outline: 'no verifiable information'."""
    T = lambda ph, dt=0: C.at(40, ph, dt=dt)
    xs = [220, 400, 580, 760, 940]
    els = [person_s(x, 640, 180, round(.3 + .1 * k, 2), "#8a8378" if k < 4 else "#e8d6b8") for k, x in enumerate(xs)] + [glow(940, 520, 110, .8, .45, "lamp"),
           lab(940, 690, "Grusch", .9, GOLD, 26), lab(400, 690, "others", 1.0, DIM, 26)]
    ch = T("A story passed")
    for k in range(4):
        x = (xs[k] + xs[k + 1]) / 2
        op = round(1 - .2 * k, 2)
        els += [dict(oval(x, 410, 52, 30, PAPER, "none", 0, op, round(ch + .45 * k, 2)), fx="pop"),
                arrow([[xs[k] + 16, 470], [x, 450], [xs[k + 1] - 16, 470]], round(ch + .45 * k, 2), DIM, 2, dur=.4)]
    ad = T("denied")
    els += [box(1100, 450, 120, 200, "#3a2f25", "#8a6a48", 3, 4, ad, fx="pop"), dot(1190, 560, 6, AU, ad),
            box(1132, 520, 56, 44, "none", RED, 4, 6, ad + .3), {"k": "circle", "x": 1160, "y": 514, "r": 18, "fill": "none", "c": RED, "w": 4, "in": ad + .3},
            lab(1160, 700, "access denied", ad + .4, RED, 26)]
    ic = T("impossible to check")
    els += [ring(600, 300, 50, ic, BONE, 4), line([[636, 336], [690, 390]], ic + .3, BONE, 10, draw=False), lab(600, 230, "impossible to check", ic + .5, BONE, 28)]
    pn = T("The Pentagon")
    pent = [[r1(1450 + 110 * math.cos(math.radians(-90 + 72 * k))), r1(330 + 110 * math.sin(math.radians(-90 + 72 * k)))] for k in range(5)]
    pin_ = [[r1(1450 + 50 * math.cos(math.radians(-90 + 72 * k))), r1(330 + 50 * math.sin(math.radians(-90 + 72 * k)))] for k in range(5)]
    els += [poly(pent, "rgba(232,184,122,.10)", AMBER, 3, pn, fx="pop"), poly(pin_, "none", AMBER, 2, pn + .1, fx="pop"),
            lab(1450, 490, "no verifiable", pn + .4, AMBER, 28), lab(1450, 528, "information", pn + .4, AMBER, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s42_nasa(C):
    """s42: the NASA panel of 2023: sixteen people at a long curved table; 'no evidence: extraterrestrial'; then three sensors pop as
    'better data': a camera, a radar dish, a satellite."""
    T = lambda ph, dt=0: C.at(41, ph, dt=dt)
    np_ = T("NASA's panel")
    els = [glow(889, 330, 620, -1, .25, "lamp"), lab(889, 160, "NASA's independent panel, 2023", np_, GOLD, 32)]
    arcy = lambda x: 400 + 80 * ((x - 889) / 520) ** 2
    for k in range(16):
        x = 400 + 978 * k / 15
        els += person_sit(r1(x), r1(arcy(x)), 110, round(np_ + .05 * k, 2), "#d8ccb8")
    els += [line([[r1(x), r1(arcy(x) + 4)] for x in range(340, 1441, 50)], np_, "#6e5440", 22, curve=True, draw=False),
            line([[r1(x), r1(arcy(x) - 6)] for x in range(340, 1441, 50)], np_, "#c9a070", 3, curve=True, draw=False)]
    ne = T("no evidence")
    els += chip(889, 575, "no evidence: extraterrestrial", GREEN, ne, 30)
    bd = T("better")
    cam_ = [box(470, 650, 90, 60, "#5b5550", "#cbd2d8", 2, 6, bd, fx="pop"), {"k": "circle", "x": 515, "y": 680, "r": 20, "fill": "#1a1511", "c": "#cbd2d8", "w": 2, "in": bd}]
    dish = [poly(ellipse(889, 670, 60, 26, a0=0, a1=180), "#9aa0a8", "#ffffff", 2, bd + .3, True, fx="pop"), line([[889, 690], [889, 730]], bd + .3, "#9aa0a8", 5, draw=False)]
    sat = [box(1270, 660, 50, 40, "#c9a070", "#ffffff", 2, 4, bd + .6, fx="pop"), box(1200, 670, 60, 20, "#5f8fb0", "#ffffff", 1, 2, bd + .6, fx="pop"),
           box(1330, 670, 60, 20, "#5f8fb0", "#ffffff", 1, 2, bd + .6, fx="pop")]
    els += cam_ + dish + sat + [lab(889, 776, "a plea for better data", bd + .9, BLUE, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s43_aaro(C):
    """s43: a long time axis 1945 to 2024 with archive boxes along it; a magnifier's path sweeps from 1945 to 2024 over the boxes; at the
    end a result card: confirmed alien technology, 0."""
    T = lambda ph, dt=0: C.at(42, ph, dt=dt)
    X = lambda yv: r1(180 + (yv - 1945) * 17.7)
    els = [{"k": "axis", "x0": X(1945), "x1": X(2025), "y": 640, "ticks": [[X(y), str(y)] for y in (1945, 1965, 1985, 2005, 2024)], "in": .3},
           lab(889, 170, "the Pentagon's UAP office, 2024", .4, GOLD, 32)]
    for k, yv in enumerate(range(1947, 2024, 8)):
        els += [box(X(yv) - 40, 556, 80, 84, "#cdb58a", "#8a6a48", 2, 4, round(.5 + .08 * k, 2), fx="rise")]
    cb = T("combing")
    els += [line([[X(1945), 520], [X(2024), 520]], cb, BONE, 2, "inferred", dur=2.4), ring(X(2024) - 40, 500, 40, cb + 2.2, BONE, 4),
            line([[X(2024) - 12, 528], [X(2024) + 30, 570]], cb + 2.3, BONE, 9, draw=False), lab(X(1945), 494, "back to 1945", cb + .3, BONE, 26, "start")]
    ns = T("no sign")
    els += [box(620, 250, 540, 200, "rgba(18,13,10,.9)", GREEN, 2.5, 16, ns, fx="pop"), lab(890, 320, "confirmed alien technology", ns + .2, BONE, 30),
            lab(890, 420, "0", ns + .5, GREEN, 90, st="big", fx="pop")]
    return {"base": "dark", "cam": CAM, "els": els}


def s44_circle(C):
    """s44: six people in a ring; one claim at the centre; a note travels round the ring and a copy pops at each person (six sources?);
    then lines trace every copy back to the one claim in the middle."""
    T = lambda ph, dt=0: C.at(43, ph, dt=dt)
    cx, cy, R = 889, 500, 270
    els = [lab(380, 220, "circular reporting", T("circular"), GOLD, 38, st="serif")]
    pos = [(cx + R * 1.3 * math.cos(math.radians(-90 + 60 * k)), cy + R * .82 * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
    els += [person_s(r1(x), r1(y + 60), 110, round(.4 + .1 * k, 2), "#c9bba6") for k, (x, y) in enumerate(pos)]
    one = T("The same few")
    els += [box(cx - 34, cy - 22, 68, 44, LILAC, "#ffffff", 1.5, 4, one, fx="pop"), lab(cx, cy + 64, "one claim", one + .3, LILAC, 28)]
    pa = T("passed around")
    arc = [[r1(cx + R * 1.12 * math.cos(math.radians(a))), r1(cy + R * .7 * math.sin(math.radians(a)))] for a in range(-90, 271, 10)]
    els += [line(arc, pa, LILAC, 2.5, "claimed", dur=2.4, curve=True)]
    for k, (x, y) in enumerate(pos):
        nx, ny = x + (36 if math.cos(math.radians(-90 + 60 * k)) >= 0 else -36), y - 40
        els += [box(r1(nx - 22), r1(ny - 15), 44, 30, LILAC, "#ffffff", 1, 3, round(pa + .4 * k, 2), fx="pop")]
    ms = T("many sources")
    els += [lab(1450, 250, "six sources?", ms, LILAC, 30)]
    tb = ms + 1.0
    for k, (x, y) in enumerate(pos):
        nx, ny = x + (36 if math.cos(math.radians(-90 + 60 * k)) >= 0 else -36), y - 40
        els += [line([[r1(nx), r1(ny)], [cx, cy]], round(tb + .1 * k, 2), GOLD, 2, "inferred", dur=.5)]
    return {"base": "dark", "cam": CAM, "els": els}


def s45_prank(C):
    """s45: a briefing table: a new officer receives a folder; it opens on a photo of a dotted saucer; a band behind: 'for decades, until
    2023'; then a red stamp PRANK lands on the photo."""
    T = lambda ph, dt=0: C.at(44, ph, dt=dt)
    els = [glow(889, 400, 640, -1, .22, "lamp"), lab(889, 160, "inside the military, reported 2025", .4, DIM, 26)]
    fd = T("For decades")
    els += [box(300, 210, 1180, 26, "rgba(232,184,122,.25)", AMBER, 2, 13, fd, fx="pop"), lab(889, 280, "for decades, until 2023", fd + .3, AMBER, 30)]
    of = T("officers")
    els += person_sit(520, 620, 260, of, "#c9bba6") + desk(300, 1480, 620) + \
           [box(660, 560, 120, 70, "#cdb58a", "#8a6a48", 2, 4, of + .3)]
    ph = T("told")
    els += [box(880, 360, 440, 270, PAPER, "#b8a888", 2, 4, ph, fx="pop"), box(910, 390, 380, 210, "#2a3038", "#9aa0a8", 2, 2, ph + .2)] + \
           saucer(1100, 500, .9, ph + .4) + [ink(1100, 620, "ALIEN PROGRAMME", ph + .3, INK, 24)]
    pr = T("hazing prank")
    els += [stamp(1100, 470, "PRANK", RED, pr, 60, -10), lab(1100, 700, "a hazing prank", pr + .4, RED, 30)]
    return {"base": "dark", "cam": CAM, "els": els}


def s46_cases(C):
    """s46: an order sealed in gold: February 2026, release the files; then a wall of 200 small case cards (one for ten cases: over
    2,000); about half grey out behind a veil: too thin to analyse."""
    T = lambda ph, dt=0: C.at(45, ph, dt=dt)
    els = [box(-20, -20, 1820, 1040, CARD, r=0, at=-1)]
    od = T("ordered")
    els += [box(640, 140, 500, 120, PAPER, "#b8a888", 1.5, 4, od, fx="pop"), {"k": "circle", "x": 700, "y": 200, "r": 34, "fill": AU, "c": "#fff3c4", "w": 3, "in": od + .2, "fx": "pop"},
            ink(910, 192, "RELEASE THE FILES", od + .3, INK, 26), ink(910, 232, "February 2026", od + .4, "#6a645c", 24, st="small")]
    tw = T("two thousand")
    x0, y0, px, py = 520, 320, 37, 44
    for k in range(200):
        els.append(box(x0 + px * (k % 20), y0 + py * (k // 20), 30, 34, "#cdb58a", "#8a6a48", 1, 2, round(tw + .008 * k, 2), fx="pop"))
    els += [lab(x0 - 30, 520, "2,000+", tw + .5, BONE, 44, "end", st="serif"), lab(x0 - 30, 560, "cases", tw + .6, BONE, 28, "end")]
    hf = T("about half")
    els += [cover(x0 + px * 10 - 4, y0 - 4, px * 10 + 4, py * 10, CARD, hf, op=.75, dur=.8),
            lab(x0 + px * 20 + 20, 520, "too thin", hf + .4, DIM, 30, "start"), lab(x0 + px * 20 + 20, 560, "to analyse", hf + .4, DIM, 30, "start")]
    return {"base": "dark", "cam": CAM, "els": els}


def tray(x, y, t, at):
    return [glow(x, y - 140, 150, at, .45, "lamp"), line([[x, y - 300], [x - 110, y]], at, "#ffe9c8", 2, draw=False, op=.18),
            line([[x, y - 300], [x + 110, y]], at, "#ffe9c8", 2, draw=False, op=.18),
            box(x - 120, y, 240, 40, "#8a939c", "#cbd2d8", 2, 6, at, fx="pop"), box(x - 96, y - 40, 192, 40, "none", LILAC, 2.5, 8, at + .2, style="claimed"),
            lab(x, y + 90, t, at + .2, BONE, 30)]


def s47_released(C):
    """s47: a filing cabinet; six folders slide out one by one (May, May, June, July, August, September 2026) spilling small photos of
    lights; then three empty trays light under a lamp as said: craft, bodies, material."""
    T = lambda ph, dt=0: C.at(46, ph, dt=dt)
    els = [box(120, 220, 300, 520, "#5a4a3a", "#8a7a66", 2, 6, .2)] + [box(140, 240 + 84 * k, 260, 70, "#4a3c30", "#8a7a66", 1.5, 4, .2) for k in range(6)] + \
          [box(250, 268 + 84 * k, 40, 12, "#8a7a66", r=4, at=.2) for k in range(6)]
    sx = T("six")
    for k, m in enumerate(("May", "May", "June", "July", "August", "September")):
        at = round(sx + .3 * k, 2)
        els += [box(440, 240 + 84 * k, 220, 64, "#cdb58a", "#8a6a48", 2, 4, at, fx="pop"), ink(550, 280 + 84 * k, m, at + .05, INK, 24)]
    us = T("Unresolved")
    for k, (x, y) in enumerate(scatter(9, 700, 960, 260, 700, 4)):
        at = round(us + .08 * k, 2)
        els += [box(x - 40, y - 30, 80, 60, "#1a2028", "#cbd2d8", 2, 2, at, fx="pop"), glow(x, y, 26, at + .1, .7, "scan"), dot(x, y, 4, "#ffffff", at + .1)]
    els += [lab(830, 760, "unresolved sightings", us + .6, BLUE, 28)]
    for k, (t, ph) in enumerate((("craft", "No craft"), ("bodies", "No bodies"), ("material", "No material"))):
        els += tray(1120 + 220 * k, 560, t, T(ph))
    return {"base": "dark", "cam": CAM, "els": els}



# ================================================================ chapter 5 · The ledger
ROWS = [175, 270, 365, 460, 555, 650, 745]


def row_icon(k, x, y, at):
    """The small drawing at the head of each ledger row."""
    if k == 0:
        return [line([[x, y - 36], [x, y + 30]], at, "#e9dccb", 1.5, draw=False)] + [oval(x, y - 34 + 12 * j, 5, 6, "#efe6d2", at=at) for j in range(4)] + \
               reflector(x, y + 22, .16, at)
    if k == 1:
        return plane_side(x, y, 90, at, "#e6e8ec", "u2") + [glow(x, y, 40, at, .5, "fire")]
    if k == 2:
        return [box(x - 34, y - 32, 68, 64, PAPER, "#b8a888", 1, 2, at), line([[x - 20, y + 22], [x - 20, y - 14], [x + 20, y - 14], [x + 20, y + 22]], at, INK, 2, draw=False),
                line([[x + 6, y - 14], [x + 6, y + 4]], at, INK, 1.5, draw=False)]
    if k == 3:
        return [box(x - 40, y - 28, 30, 12, "#cdb58a", "#8a6a48", 1.5, 3, at, fx="pop"), box(x - 40, y - 20, 80, 48, "#cdb58a", "#8a6a48", 1.5, 4, at, fx="pop"),
                ink(x, y + 12, "2007", at + .1, INK, 24)]
    if k == 4:
        return [line([[x - 40, y + 18], [x - 20, y + 12], [x, y + 18], [x + 20, y + 12], [x + 40, y + 18]], at, BLUE, 2, curve=True, draw=False),
                glow(x, y - 6, 24, at, .7, "scan"), dot(x, y - 6, 6, "#ffffff", at), arrow([[x + 14, y - 22], [x + 40, y - 22]], at, "#cfe6ff", 2, dur=.3, curve=False)]
    if k == 5:
        return tictac(x, y, 64, at, glow_op=.3)
    return saucer(x, y + 6, .3, at)


LEDGER = [("Roswell: a secret balloon", "Strong evidence", "strong", "strong evidence"),
          ("Spy planes behind sightings", "Established", "established", "sightings established"),
          ("Psychic spies", "Ruled out", "ruled", "ruled out"),
          ("A hidden UFO study", "Established", "established", "study established"),
          ("Go Fast: the wind", "Plausible", "plausible", "plausible"),
          ("The Tic Tac", "Open question", "open", "open question"),
          ("Crashed craft and bodies", "Awaiting evidence", "awaiting", "awaiting evidence")]


def _row(k, at_row, at_chip):
    y = ROWS[k]
    t, g, key, _ = LEDGER[k]
    return [box(130, y - 44, 1520, 88, "rgba(242,201,142,.08)", "rgba(242,201,142,.30)", 1.5, 12, at_row, fx="pop"),
            lab(320, y + 10, t, at_row + .1, BONE, 32, "start")] + row_icon(k, 225, y, at_row + .1) + chip(1120, y, g, GRADE[key], at_chip, 30, a="start")


def s48_ledger(C):
    """s48: the ledger board: seven rows, each a small drawing and its words; rows 1 to 4 light as named and their chips pop as each grade
    is said: Strong evidence, Established, Ruled out, Established."""
    T = lambda ph, dt=0: C.at(47, ph, dt=dt)
    els = [box(110, 122, 1560, 670, "rgba(18,13,10,.7)", "rgba(255,236,206,.25)", 2, 18, .2)]
    names = ["Roswell's secret", "Spy planes behind", "Psychic spies", "A hidden Pentagon"]
    for k in range(4):
        els += _row(k, T(names[k]), T(LEDGER[k][3]))
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


def s49_late(C):
    """s49 (alias of s48, lower): rows 5 to 7 light as named; chips Plausible, Open question, Awaiting evidence pop as said."""
    T = lambda ph, dt=0: C.at(48, ph, dt=dt)
    els = []
    names = ["Go Fast drifting", "The Tic Tac", "Crashed craft"]
    for j, k in enumerate((4, 5, 6)):
        els += _row(k, T(names[j]), T(LEDGER[k][3]))
    return els


def s50_pattern(C):
    """s50: four small pictures pop as named (balloon train, U-2, viewer's sketch, prank folder) and a bracket gathers them over three
    people: human; a grey cover sheet slides over them and dotted saucers sprout from its edges (legends); at the right a pilot beside
    better sensors; in the centre a large chip 'Awaiting evidence' over a dotted saucer."""
    T = lambda ph, dt=0: C.at(49, ph, dt=dt)
    els = [lab(889, 160, "the pattern", T("Notice"), GOLD, 38, st="serif")]
    xs = [200, 350, 500, 650]
    for k, ph in enumerate(("balloons", "spy planes", "psychic spies", "pranks")):
        at = T(ph)
        kk = [0, 1, 2, None][k]
        if kk is not None:
            els += row_icon(kk, xs[k], 290, at)
        else:
            els += [box(xs[k] - 62, 258, 124, 66, PAPER, "#b8a888", 1, 2, at, fx="pop"), stamp(xs[k], 292, "PRANK", RED, at + .1, 24, -10)]
    hu = T("human")
    els += [line([[160, 360], [160, 380], [690, 380], [690, 360]], hu, BONE, 2.5, dur=.6)] + \
           [person_s(345 + 80 * j, 540, 130, round(hu + .2 + .15 * j, 2), "#e8d6b8") for j in range(3)] + [lab(425, 590, "human", hu + .6, BONE, 32)]
    cv = T("cover stories")
    els += [box(140, 230, 580, 130, "#4a4440", "#8a8378", 2, 8, cv, op=.9, fx="rise")]
    lg = T("legends")
    els += sum([saucer(x, y, .32, round(lg + .3 * j, 2)) for j, (x, y) in enumerate(((180, 210), (420, 200), (660, 215), (720, 300)))], [])
    pi = T("The pilots")
    els += [person_s(1330, 560, 170, pi, "#e8d6b8"), box(1306, 380, 48, 22, "#9aa3ad", r=10, at=pi + .1), lab(1330, 610, "the pilots", pi + .3, BONE, 28)]
    bd = T("better data")
    els += [box(1440, 380, 80, 54, "#5b5550", "#cbd2d8", 2, 6, bd, fx="pop"), {"k": "circle", "x": 1480, "y": 407, "r": 17, "fill": "#1a1511", "c": "#cbd2d8", "w": 2, "in": bd},
            poly(ellipse(1480, 490, 50, 22, a0=0, a1=180), "#9aa0a8", "#ffffff", 2, bd + .2, True, fx="pop"), line([[1480, 510], [1480, 540]], bd + .2, "#9aa0a8", 5, draw=False),
            box(1556, 420, 40, 30, "#c9a070", "#ffffff", 2, 3, bd + .4, fx="pop"), box(1600, 428, 40, 14, "#5f8fb0", r=2, at=bd + .4),
            lab(1500, 650, "better data", bd + .5, BLUE, 28)]
    aw = T("Awaiting")
    els += [glow(980, 560, 200, aw - .4, .4, "scan")] + saucer(980, 520, .7, aw - .6) + chip(980, 650, "Awaiting evidence", GRADE["awaiting"], aw, 34)
    return {"base": "dark", "cam": CAM, "els": els}


def s51_tests(C):
    """s51: four cards build as named: a sample under a glass dome with three labs sending arrows to it; a radar screen and an infrared
    screen pouring data dots into an open folder; a trail of folders and a budget sheet; the first three dashed (not done); then a fourth
    card where a row of question marks turn one by one into a balloon, a drone and a wind arrow."""
    T = lambda ph, dt=0: C.at(50, ph, dt=dt)
    cw, gap, x0, y0, y1 = 380, 20, 90, 150, 760
    c = [x0 + k * (cw + gap) + cw / 2 for k in range(4)]
    els = []
    a1, a2, a3, a4 = T("One piece"), T("The raw"), T("Or a paper"), T("And if")
    for k, at in enumerate((a1, a2, a3, a4)):
        els += [box(x0 + k * (cw + gap), y0, cw, y1 - y0, "#1f1914", "rgba(245,236,220,.4)", 2, 14, at - .2, style="inferred", fx="pop")]
    els += [poly(ellipse(c[0], 420, 70, 70, a0=180, a1=360), "rgba(207,230,255,.12)", "#cfe6ff", 2.5, a1 + .2, True, fx="pop"), line([[c[0] - 80, 420], [c[0] + 80, 420]], a1 + .2, "#cfe6ff", 3, draw=False),
            poly([[c[0] - 22, 418], [c[0] - 10, 392], [c[0] + 14, 388], [c[0] + 24, 418]], "#9aa0a8", "#ffffff", 1.5, a1 + .3, fx="pop")]
    for j in range(3):
        lx = c[0] - 120 + 120 * j
        els += [box(lx - 30, 600, 60, 50, "#3a3028", "#cbbca8", 2, 3, a1 + .6 + .2 * j, fx="rise"), poly([[lx - 36, 600], [lx, 570], [lx + 36, 600]], "#5a4a3c", "#cbbca8", 2, a1 + .6 + .2 * j),
                arrow([[lx, 560], [r1((lx + c[0]) / 2), 500], [c[0], 450]], a1 + 1.0 + .2 * j, AU, 2.5, "inferred", .6)]
    els += [lab(c[0], 214, "one piece of material", a1 + .1, BONE, 26), lab(c[0], 710, "independent labs", a1 + 1.4, AU, 28)]
    els += [box(c[1] - 150, 280, 130, 100, "#0d1a12", "#2f5a3a", 2, 6, a2 + .2, fx="pop"), dot(c[1] - 85, 330, 6, "#f4fff2", a2 + .3),
            box(c[1] + 20, 280, 130, 100, "#0a1820", "#5fa8c9", 2, 6, a2 + .3, fx="pop")] + \
           [line([[r1(c[1] + 85), 330], [r1(c[1] + 85 + 50 * math.cos(math.radians(a))), r1(330 - 50 * math.sin(math.radians(a)))]], a2 + .4, "#9fd0ff", 2, draw=False, op=.6)
            for a in (40, 100)] + \
           [dot(r1(c[1] - 60 + 120 * ((j * 7) % 10) / 10), r1(420 + 14 * j), 4, "#cfe6ff", round(a2 + .6 + .06 * j, 2)) for j in range(12)] + \
           [box(c[1] - 90, 600, 180, 110, "#cdb58a", "#8a6a48", 2, 4, a2 + .8, fx="pop"), lab(c[1], 214, "raw data, in full", a2 + .1, BONE, 26)]
    els += [box(c[2] - 150 + 22 * j, 300 + 70 * j, 200, 60, "#cdb58a", "#8a6a48", 2, 4, round(a3 + .2 + .2 * j, 2), fx="pop") for j in range(4)] + \
           [ink(c[2] - 50 + 22 * j, 338 + 70 * j, n, round(a3 + .25 + .2 * j, 2), INK, 24) for j, n in enumerate(("CODE NAME", "BUDGET", "ORDERS", "REPORT"))] + \
           [lab(c[2], 214, "a paper trail", a3 + .1, BONE, 26), lab(c[2], 710, "like Stargate's", a3 + 1.2, DIM, 26)]
    qs = [c[3] - 110, c[3], c[3] + 110]
    for j, x in enumerate(qs):
        els += [lab(x, 380, "?", a4 + .3, LILAC, 60, st="big", fx="pop")]
    b, d, w = T("balloons"), T("drones"), T("wind")
    els += [cover(qs[0] - 40, 320, 80, 80, "#1f1914", b, dur=.3)] + balloon(qs[0], 340, 26, b + .2) + \
           [cover(qs[1] - 40, 320, 80, 80, "#1f1914", d, dur=.3), box(qs[1] - 20, 352, 40, 14, "#9aa0a8", r=4, at=d + .2),
            line([[qs[1] - 34, 344], [qs[1] + 34, 344]], d + .2, "#cbd2d8", 3, draw=False), dot(qs[1] - 34, 342, 6, "#cbd2d8", d + .2), dot(qs[1] + 34, 342, 6, "#cbd2d8", d + .2),
            cover(qs[2] - 40, 320, 80, 80, "#1f1914", w, dur=.3)] + \
           [arrow([[qs[2] - 30, 340 + 14 * j], [qs[2] + 30, 340 + 14 * j]], w + .2 + .1 * j, "#cfe6ff", 2.5, dur=.3, curve=False) for j in range(3)] + \
           [lab(c[3], 214, "or ordinary things", a4 + .1, BONE, 26), lab(c[3], 710, "an answer too", w + .8, GREEN, 28)]
    return {"base": "dark", "cam": CAM, "els": els}


def s52_close(C):
    """s52: dusk over the Pacific: a calm sea, the last light on the horizon, a jet's contrail drawing slowly high up, a few stars; on the
    horizon a ship's radar sweeps once; the camera holds still for the end card."""
    H0 = 560
    els = [{"k": "water", "y": H0, "h": 520, "op": .9, "in": -1}] + \
          [line([[r1(x - 30), r1(y)], [r1(x + 30), r1(y)]], -1, "#ffd9b0", 1.4, draw=False, op=.18) for x, y in scatter(18, 200, 1600, 600, 780, 3)] + \
          [line([[1700, 210], [900, 250], [600, 266]], 1.0, "#fff1e0", 2.5, dur=5.0, curve=True, op=.5), dot(600, 266, 3, "#ffffff", 5.8)] + \
          ship(1180, H0 + 4, 120, .4, "#22262c") + \
          [line([[r1(1180 + R * math.cos(math.radians(a))), r1(H0 - 30 - R * math.sin(math.radians(a)))] for a in range(20, 161, 10)], round(2.5 + .4 * j, 2), "#9fd0ff", 1.6,
                curve=True, dur=.8, op=round(.5 - .12 * j, 2)) for j, R in enumerate((40, 80, 120))]
    return {"base": "sky", "tod": "dusk", "ground": 1200, "sun": [420, H0 + 10, 26], "cam": CAM, "els": els}


# ================================================================ the film
def _todo(i):
    return lambda C: {"base": "dark", "cam": CAM, "els": [lab(889, 480, "s%d" % (i + 1), .2, BONE, 60)]}


SCENES = {0: s01_sea, 3: s04_oath, 4: s05_files, 6: s07_paper, 7: s08_map, 8: s09_debris, 9: s10_fortworth, 10: s11_memory,
          12: s13_mogul, 13: s14_reflector, 15: s16_answers, 16: s17_records, 17: s18_bluebook, 18: s19_hynek, 19: s20_u2,
          21: s22_overhalf, 22: s23_panel, 23: s24_mind, 24: s25_codes, 25: s26_sketch, 26: s27_chance, 27: s28_closed, 28: s29_declass,
          29: s30_times, 30: s31_screens, 32: s33_train, 33: s34_gofast, 34: s35_nimitz, 35: s36_graves, 36: s37_reports, 37: s38_bird,
          38: s39_hearing, 39: s40_claims, 40: s41_chain, 41: s42_nasa, 42: s43_aaro, 43: s44_circle, 44: s45_prank, 45: s46_cases, 46: s47_released,
          47: s48_ledger, 49: s50_pattern, 50: s51_tests, 51: s52_close}
LATES = {1: s02_late, 2: s03_late, 11: s12_late, 14: s15_late, 20: s21_late, 31: s32_late, 48: s49_late}
DESCRIPTION = re.sub(r"0:00 The UFO Files\n(?:mm:ss [^\n]*\n?)+", "{chapters}\n", SCRIPT["description"])


def film():
    beats = BEATS()
    C = Clock(beats)
    shots = []
    for i in range(52):
        if i in ALIAS:
            shots.append({"base": "dark", "cam": CAM, "els": []})
        else:
            shots.append(SCENES.get(i, _todo(i))(C))
    cams = _tagged(ALIAS_CAMS)
    late = {i: f(C) for i, f in LATES.items()}
    ep = {"id": "lf-ufo-files", "code": "LF.05", "series": SCRIPT["series"], "title": SCRIPT["title"], "case": "uap-disclosure",
          "verdict": "unsupported", "claim": "Have governments recovered craft or bodies of non-human origin? What have they actually admitted?",
          "mood": "mystery", "hook_text": "What have governments actually *admitted*?", "beats": beats, "shots": shots,
          "sources": "GAO 1995 (GAO/NSIAD-95-187) · McAndrew 1997 (USAF) · Haines 1997 (Studies in Intelligence) · Mumford et al. 1995 (AIR) · "
                     "Targ & Puthoff 1974 (doi:10.1038/251602a0) · Marks & Kammann 1978 (doi:10.1038/274680a0) · ODNI 2021 · NASA 2023 · AARO 2024",
          "post": "From the Roswell headline of 1947 to the Pentagon's file releases of 2026: secret balloons, hidden spy planes, psychic spies, Navy "
                  "videos and sworn testimony. What governments have actually admitted, file by file, and what is still only said.",
          "hashtags": ["#UFO", "#UAP", "#Roswell", "#TicTac", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": SCRIPT["title"], "yt_title": SCRIPT["yt_title"], "description": DESCRIPTION,
          "end_line": "The sky is watched better than ever. The evidence can still arrive."}
    out = remix(ep, alias=dict(ALIAS), cams=cams)
    return _attach(out, cams, late)


def EPISODES():
    return [film()]
