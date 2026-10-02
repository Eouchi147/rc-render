"""LF.04 The Comet and the Cold (lf-sky-fell): did a comet bring back the Ice Age? The Younger Dryas, weighed. A 16:9 long film.

Script: films/long/lf-sky-fell/script.json (its lines are read from there and kept word for word; this module only adds the
[go:N|t] markers where the picture changes). One scene per script shot, hung on one wall (mural.wall), six chapter rooms.
Numbers drawn true to the script: central Greenland about 14 C warmer at 14,700 and about 9 C colder at 12,900 (22 units a
degree on the thermometer), the cold from 12,896 to 11,703 years before AD 2000 (GICC05), the German lake about 167 years
later, platinum up at least 100 times over 14 years and down in 7, 29 sites and 3 in the window, 354 dates and one century,
bay rims from 109,000 to 2,000 years, White Pond 31,000 years, the Mackenzie flood about 700 years from 12,940 +/- 150 beside
12,850 +/- 140, the 2025 platinum reading 45 years after the onset and 14 years long. Site positions on the maps (the 18
bead sites, the 4 Syrian sites, the bays) and the ice-sheet outline at about 12,900 years ago are schematic.
Claims are drawn dotted (the comet, its bursts, its fires, the ice rain), inferences dashed, evidence solid.
Reused from the Shorts: sky-fell (lg_c.py: the thermometer, the sea and ice, the dig, the core and its platinum, the
conveyor belt), carolina-bays (f03.py: the bays and their fan, the sand clock, White Pond), mammoths (f03.mammoth), taurids
(the felled forest), all redrawn wide for 16:9.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-sky-fell/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-sky-fell/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-sky-fell RC_FILMS_EPS=/tmp/claude-0/sbx_lf-sky-fell/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-sky-fell/boards python3 films.py long.lf_sky_fell
"""
import copy, json, math, os, random, re
from films import View
from mural import remix
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, question, ellipse, scatter, \
    BONE, AMBER, BLUE, LILAC, GREEN, RED, AU

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = json.load(open(os.path.join(HERE, "lf-sky-fell", "script.json"), encoding="utf-8"))

GOLD, ICE, WARM, INK, PAPER = "#f2c98e", "#e6eff6", "#ffb07a", "#3a2c20", "#efe6d2"
DIM = "#cbbca8"
W_, H_ = 1778, 1000          # the 16:9 frame; drawings in x 80..1700, y 120..800 (captions below 815, HUD above 110)


# ================================================================ small drawing helpers (panel units)
def P(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def poly(p, fill, c="none", w=0, at=0, curve=False, **kw):
    e = {"k": "poly", "p": P(p), "fill": fill, "c": c, "w": w, "curve": curve, "in": at}
    e.update(kw)
    return e


def rot(pts, cx, cy, deg):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    return [[round(cx + (x - cx) * ca - (y - cy) * sa, 1), round(cy + (x - cx) * sa + (y - cy) * ca, 1)] for x, y in pts]


def rell(cx, cy, rx, ry, deg=0, n=24):
    """A rotated ellipse as points."""
    return rot([[cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)] for k in range(n)], cx, cy, deg)


def lab(x, y, t, at=0, c=BONE, size=30, a="middle", **kw):
    return label(x, y, t, at, c, size, a, **kw)


def ink(x, y, t, at=0, c=INK, size=28, a="middle", st="lab"):
    """Text printed on paper: dark, no halo."""
    return label(x, y, t, at, c, size, a, st=st, halo=False)


def comet(x, y, at, ang=-35, L=120, c=LILAC, style="claimed", r=9, g=70):
    """A comet: a bright head at (x, y), its tail streaming back towards angle ang (degrees, screen space)."""
    a = math.radians(ang)
    tail = []
    for k, (da, f, w) in enumerate(((-.12, 1.0, 2.5), (0, 1.15, 3.5), (.12, .95, 2.5))):
        tx, ty = x + L * f * math.cos(a + da), y + L * f * math.sin(a + da)
        tail.append(line([[x, y], [round(tx, 1), round(ty, 1)]], at, c, w, style, .5))
    return [glow(x, y, g, at, .8, "scan")] + tail + [dot(x, y, r, "#f5f0ff", at)]


def wave(x, y, at, s=1.0, c=BLUE, op=None):
    """Meltwater: two wavy lines and a drop."""
    out = []
    for j in range(2):
        yy = y + 16 * s * j
        pts = [[x - 40 * s + 10 * s * k, yy + (6 * s if k % 2 else -6 * s)] for k in range(9)]
        e = line(pts, at, c, 3.5 * s, curve=True, dur=.5)
        if op is not None:
            e.update(op=op, keepop=True)
        out.append(e)
    drop = poly([[x, y - 46 * s], [x + 12 * s, y - 26 * s], [x + 10 * s, y - 18 * s], [x, y - 13 * s], [x - 10 * s, y - 18 * s], [x - 12 * s, y - 26 * s]], c, "none", 0, at, True)
    if op is not None:
        drop.update(op=op, keepop=True)
    return out + [drop]


def flake(x, y, r, at, c="#e6f4ff", w=2.5):
    return [line([[round(x - r * math.cos(a), 1), round(y - r * math.sin(a), 1)], [round(x + r * math.cos(a), 1), round(y + r * math.sin(a), 1)]], at, c, w, draw=False)
            for a in (0, math.pi / 3, 2 * math.pi / 3)]


def conifer(x, y, h, at, c="#1d2620", fx="pop", **kw):
    w = h * .42
    pts = [[x, y - h], [x + w * .32, y - h * .62], [x + w * .2, y - h * .62], [x + w * .45, y - h * .32], [x + w * .3, y - h * .32], [x + w * .5, y - h * .08],
           [x + w * .08, y - h * .08], [x + w * .08, y], [x - w * .08, y], [x - w * .08, y - h * .08], [x - w * .5, y - h * .08], [x - w * .3, y - h * .32],
           [x - w * .45, y - h * .32], [x - w * .2, y - h * .62], [x - w * .32, y - h * .62]]
    e = poly(pts, c, "rgba(255,226,190,.18)", 1, at, fx=fx)
    e.update(kw)
    return e


def clovis(x, y, h, at, fill="#c9c3b5", c="#f5ecdc", style="known", fx="pop", w=1.5):
    """A fluted Clovis point, tip up, base at y."""
    s = h / 80
    pts = [[x, y - 80 * s], [x + 12 * s, y - 52 * s], [x + 15 * s, y - 20 * s], [x + 11 * s, y], [x + 4 * s, y - 5 * s], [x, y - 2 * s], [x - 4 * s, y - 5 * s],
           [x - 11 * s, y], [x - 15 * s, y - 20 * s], [x - 12 * s, y - 52 * s]]
    out = [poly(pts, fill, c, w, at, True, fx=fx, style=style)]
    if fill != "none":
        out.append(line([[x, y - 4 * s], [x, y - 38 * s]], at, "#8d8678", 2.5 * s, draw=False))
    return out


def bone(x0, y0, x1, y1, at, w=10, c="#efe6d4", **kw):
    e = [line([[x0, y0], [x1, y1]], at, c, w, draw=False), dot(x0, y0, w * .9, c, at), dot(x1, y1, w * .9, c, at)]
    for q in e:
        q.update(kw)
    return e


def mag(cx, cy, r, at, fill="#15110d", hx=1, hy=1):
    """A magnifier: a dark lens with a rim and a handle."""
    a = math.atan2(hy, hx)
    h0 = [cx + r * math.cos(a), cy + r * math.sin(a)]
    h1 = [cx + (r + 70) * math.cos(a), cy + (r + 70) * math.sin(a)]
    return [{"k": "circle", "x": cx, "y": cy, "r": r, "fill": fill, "c": "none", "w": 0, "in": at, "fx": "pop"},
            line([P([h0])[0], P([h1])[0]], at + .1, "#8c7152", 12, draw=False),
            ring(cx, cy, r, at, BONE, 4, dur=.5)]


def chip(x, y, t, c, at, size=28, w=None, a="middle"):
    """A verdict chip: a rounded tag with its word."""
    w = w or round(len(t) * size * .56 + 34)
    x0 = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    return [box(round(x0, 1), y - size * .95, w, size * 1.5, "rgba(20,16,12,.85)", c, 2.5, size * .75, at, fx="pop"),
            label(round(x0 + w / 2, 1), round(y + size * .1, 1), t, at + .1, c, size, st="lab", halo=False)]


def thermo_glyph(x, top, bot, frac, at, c=AMBER, fill_at=None, dur=1.4, tube="#2a221b"):
    """A thermometer: a tube from top to bot and a bulb; the liquid rises to frac of the tube (fx fill)."""
    w = 26
    h = bot - top
    return [box(x - w / 2, top, w, h + 10, tube, BONE, 2.5, w / 2, at),
            {"k": "circle", "x": x, "y": bot + 22, "r": 24, "fill": c, "c": BONE, "w": 2.5, "in": at},
            box(x - 7, round(bot - h * frac, 1), 14, round(h * frac + 14, 1), c, r=7, at=fill_at if fill_at is not None else at + .3, fx="fill", dur=dur)]


def sheet(cx, cy, w, h, deg, at, title=None, lines_=6, tc=INK, extra=(), fx=None, ly0=None):
    """A sheet of paper (a paper, a journal page), turned by deg, with ruled text lines; extra: elements on it (its own coordinates)."""
    els = [box(cx - w / 2 + 8, cy - h / 2 + 10, w, h, "rgba(0,0,0,.45)", r=3, at=-1),
           box(cx - w / 2, cy - h / 2, w, h, PAPER, "#b8a888", 1.5, 3, -1)]
    y0 = ly0 if ly0 is not None else cy - h / 2 + (90 if title else 50)
    for j in range(lines_):
        ww = (w - 80) * (1 if j % 4 != 3 else .6)
        els.append(line([[cx - w / 2 + 40, y0 + 26 * j], [cx - w / 2 + 40 + ww, y0 + 26 * j]], -1, "#9a8a72", 4, draw=False, op=.8))
    if title:
        els.append(ink(cx, cy - h / 2 + 58, title, -1, tc, 34, st="serif"))
    els += [dict(e, **{"in": -1}) if (e.get("in") or 0) >= 0 else e for e in extra]
    g = {"k": "group", "tr": "rotate(%s %s %s)" % (deg, cx, cy), "in": at, "els": els}
    if fx:
        g["fx"] = fx
    return g


def move(els, dx, dy):
    """The same elements shifted by (dx, dy)."""
    out = []
    for e in copy.deepcopy(els):
        for k in ("x", "x0", "x1"):
            if isinstance(e.get(k), (int, float)):
                e[k] = round(e[k] + dx, 1)
        if isinstance(e.get("y"), (int, float)):
            e["y"] = round(e["y"] + dy, 1)
        if e.get("p"):
            e["p"] = [[round(q[0] + dx, 1), round(q[1] + dy, 1)] for q in e["p"]]
        if e.get("ticks"):
            e["ticks"] = [[round(t[0] + dx, 1), t[1]] for t in e["ticks"]]
        out.append(e)
    return out


def person_s(x, y, h, at, c="#e8d6b8", **kw):
    e = person(x, y, h, at, c)
    e.update(kw)
    return e


def flat_strip(y0, y1, c, at=-1, x0=-20, x1=1800, **kw):
    return box(x0, y0, x1 - x0, y1 - y0, c, r=0, at=at, **kw)


# ================================================================ narration: the script's lines, with [go:] markers added
TAGRUN = re.compile(r"\[(\w+):[^\]]*\]$")


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


# ================================================================ chapter 1 · The cold comes back
def X(ya):
    """The thermometer's time axis: 16,000 years ago at x 160, 10,000 at x 1560."""
    return round(160 + (16000 - ya) * 1400 / 6000, 1)


DEG = 22                                     # 22 units a degree: the Bolling warming (about 14 C) is 308, the cold snap (about 9 C) 198
BASE_Y, BOL_Y, ALL_Y, YD_Y = 620, 620 - 14 * DEG, 367, 367 + 9 * DEG
CA1 = [(16000, 622), (15800, 612), (15600, 626), (15400, 615), (15200, 628), (15000, 617), (14850, 625), (14740, 619)]
CA2 = [(14740, 619), (14705, 575), (14675, 430), (14645, 330), (14600, BOL_Y), (14450, 317), (14300, 328), (14150, 323), (14030, 346), (13920, 330),
       (13750, 337), (13550, 343), (13350, 350), (13230, 372), (13120, 353), (12990, 362), (12960, ALL_Y)]
CB = [(12960, ALL_Y), (12928, 400), (12896, 466), (12870, 535), (12850, YD_Y)]
CC = [(12850, YD_Y), (12700, 573), (12550, 560), (12400, 569), (12250, 561), (12100, 570), (11950, 562), (11800, 568), (11730, 566)]
CD = [(11730, 566), (11703, 480), (11685, 380), (11660, 318), (11610, 302), (11450, 296), (11250, 303), (11000, 295), (10700, 300), (10400, 293), (10000, 297)]
X0, X1 = X(12896), X(11703)                  # GICC05: the cold from 12,896 to 11,703 years before AD 2000


def _curve(pts):
    return [[X(a), b] for a, b in pts]


def thermo_base(settled=False, comet_bits=True):
    """The thermometer of the past on a night tundra horizon: a time axis 16,000 to 10,000 years ago, warmer up, colder down.
    settled: everything already drawn (a return to it); otherwise the opening build (the hook's first line)."""
    t = (lambda v: -1) if settled else (lambda v: v)
    els = [{"k": "axis", "x0": 160, "x1": 1560, "y": 715, "ticks": [[X(y), "{:,}".format(y)] for y in range(16000, 9999, -1000)], "in": t(.2)},
           lab(1580, 722, "years ago", t(.6), DIM, 24, "start"),
           arrow([[110, 650], [110, 300]], t(1.0), BONE, 2.5, dur=.6, curve=False),
           lab(128, 296, "warmer", t(1.2), WARM, 26, "start"), lab(128, 676, "colder", t(1.2), BLUE, 26, "start"),
           line(_curve(CA1), t(.6), AMBER, 5, dur=1.6, curve=True),
           line(_curve(CA2), t(3.4), AMBER, 5, dur=1.4, curve=True),
           line(_curve(CB), t(6.3), BLUE, 5, dur=.6, curve=True)]
    return els


def thermo_line2(settled=False):
    """(hook, line 2) central Greenland: about 9 C colder, 1,200 years; then the warmth comes back (about 12 C, to scale)."""
    t = (lambda v: -1) if settled else (lambda v: v)
    return [lab(160, 180, "central Greenland", t(.4), AMBER, 28, "start"),
            line([[850, ALL_Y], [850, YD_Y]], t(2.8), AU, 3, dur=.6), line([[836, ALL_Y], [864, ALL_Y]], t(2.8), AU, 3, draw=False),
            line([[836, YD_Y], [864, YD_Y]], t(3.2), AU, 3, draw=False),
            lab(828, 476, "about 9 °C colder", t(3.2), AU, 30, "end"),
            line(_curve(CC), t(4.8), BLUE, 5, dur=1.6, curve=True),
            {"k": "rect", "x": X0, "y": YD_Y + 8, "w": round(X1 - X0, 1), "h": 715 - YD_Y - 8, "r": 0, "fill": "rgba(159,208,255,.10)", "c": "none", "sw": 0,
             "in": t(5.2), "fx": "fill", "dur": 1.0},
            line([[X0, 612], [X1, 612]], t(5.8), BONE, 2.5, dur=.6), line([[X0, 600], [X0, 624]], t(5.8), BONE, 2.5, draw=False),
            line([[X1, 600], [X1, 624]], t(6.2), BONE, 2.5, draw=False),
            lab((X0 + X1) / 2, 656, "1,200 years", t(6.3), BONE, 30),
            line(_curve(CD), t(7.0), AMBER, 5, dur=1.4, curve=True)]


def thermo_sky():
    """(hook, line 2, on 'the sky fell') a dotted comet streaks in and bursts in four small rings; a question mark over the plunge."""
    rings = [(1385, 196, 30), (1510, 150, 24), (1470, 236, 22), (1605, 212, 26)]
    return [line([[1790, 30], [1480, 196]], 14.5, LILAC, 4, "claimed", .8), glow(1480, 196, 120, 15.2, .8, "scan"), dot(1480, 196, 9, "#f5f0ff", 15.2)] + \
           [line([[1480, 196], [x, y]], round(15.3 + .12 * k, 2), LILAC, 2, "claimed", .3) for k, (x, y, r) in enumerate(rings)] + \
           [ring(x, y, r, round(15.4 + .15 * k, 2), LILAC, 2.5, "claimed") for k, (x, y, r) in enumerate(rings)] + \
           [glow(x, y, 60, round(15.4 + .15 * k, 2), .7, "red") for k, (x, y, r) in enumerate(rings)] + \
           question(X0, 250, 16.4, 84)


def thermo():
    """0 · the thermometer of the past (s1): the Ice Age lets go at 14,700 (about 14 C warmer), then on 'came back' the plunge at 12,900."""
    return {"base": "sky", "tod": "night", "ground": 690, "groundc": "#1d1915", "sun": False, "cam": [1, 889, 500], "els": thermo_base()}


def thermo_b():
    """8 · back on the thermometer (s13): the cold trough rings green, it is real; then a big question mark at the moment it began."""
    els = thermo_base(True) + thermo_line2(True) + [
        poly(rell((X0 + X1) / 2 + 4, YD_Y + 2, (X1 - X0) / 2 + 46, 58), "none", GREEN, 4, .6, True, fx="draw", dur=.9),
        glow((X0 + X1) / 2, YD_Y, 200, .9, .35, "lamp"),
        glow(X0, 230, 150, 3.4, .6, "lamp"), lab(X0, 280, "?", 3.5, AU, 140, st="big", fx="pop", dur=.8)]
    return {"base": "sky", "tod": "night", "ground": 690, "groundc": "#1d1915", "sun": False, "cam": [1, 889, 500], "els": els}


def fingerprint():
    """1 · the fingerprint (s3): one thin layer drawn across the ground, four pins on four continents tied to it by dotted threads."""
    v = View(-130, 60, -15, 62, (330, 125, 1120, 410))
    pins = [(-100, 39), (-68, 8), (5, 51), (38.4, 35.9)]
    G, LY = 600, 690
    bands = [(G, 660, "#5f4c39"), (660, 720, "#7a6248"), (720, 790, "#4f3f30"), (790, 1000, "#6b5640")]
    els = [box(-20, y0, 1820, y1 - y0, c, r=0, at=-1) for y0, y1, c in bands] + \
          [line([[-20, y], [1800, y]], -1, "#e9dccb", 1.2, "inferred", draw=False, op=.25) for y in (660, 720, 790)] + \
          [line([[-20, G], [1800, G]], -1, "#c9ad85", 2.5, draw=False)] + \
          [line([[40 + 31 * k, G], [46 + 31 * k, G - 12 - 4 * (k % 3)]], -1, "#7fa35a", 2, draw=False) for k in range(56)] + \
          [person(230, G, 96, .2, "#e8d6b8"), line([[256, G - 52], [300, G - 8]], .4, "#c9a370", 5, draw=False)] + \
          [{"k": "group", "clip": [v.ox - 14, 118, round(v.p(60, 0)[0] - v.ox + 28, 1), 424, 16], "bg": "#16303d", "in": .3,
            "els": [{"k": "map", "land": v.land()}]},
           {"k": "rect", "x": v.ox - 14, "y": 118, "w": round(v.p(60, 0)[0] - v.ox + 28, 1), "h": 424, "r": 16, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": .3}] + \
          [poly(rell(889, LY, 40 + 30 * j, 22 + 17 * j), "none", LILAC, 2, round(1.0 + .1 * j, 2), True, style="claimed", op=.35, keepop=True) for j in range(5)] + \
          [line([[60, LY + 1], [1720, LY + 1]], 2.2, LILAC, 12, dur=1.6, op=.25), line([[60, LY], [1720, LY]], 2.2, "#e9e2ff", 4, dur=1.6),
           glow(889, LY, 260, 2.8, .35, "scan"),
           lab(1690, LY - 22, "one thin layer?", 2.8, LILAC, 32, "end")]
    for k, (lo, la) in enumerate(pins):
        x, y = v.p(lo, la)
        at = round(4.2 + .15 * k, 2)
        els += [glow(x, y, 40, at, .9, "scan"), dot(x, y, 9, LILAC, at), line([[x, y + 10], [x, LY - 4]], round(at + .2, 2), LILAC, 2, "claimed", .6)]
    els += [lab(v.p(60, 0)[0] + 40, 320, "four continents", 4.7, BONE, 30, "start")]
    return {"base": "dark", "stars": 70, "cam": [1, 889, 500], "els": els}


# ---- the thaw (s6, s7): an ice dome recedes, the warmth, the forests, people; then the cold creeps back
TG = 640
SKYBOX = (-900, 1500)                        # the sky rect of BASE.sky (y -900, 2400 tall): a sky eraser spans it so its gradient matches


def _nye(e, x0=-150, h0=330, e0=920):
    """An ice sheet's profile (Nye): summit off the left edge, margin at x = e; thinner as it shrinks."""
    H = h0 * math.sqrt((e - x0) / (e0 - x0))
    xs = list(range(-20, int(e), 20)) + [e]
    return [[x, round(TG - H * math.sqrt(max(0, (e - x) / (e - x0))), 1)] for x in xs]


def _sky_eraser(outer, inner, at, tod="dusk", dur=.8):
    """Paint sky (the base's own gradient) over the region between two profiles: the ice is gone there."""
    pts = [[-20, SKYBOX[0]]] + outer + [[outer[-1][0], SKYBOX[1]], [outer[-1][0], TG]] + inner[::-1]
    return {"k": "poly", "p": P(pts), "fill": "url(#k-sky-%s)" % tod, "c": "none", "w": 0, "curve": False, "in": at, "dur": dur}


TREES = [(x, 74 + 22 * ((k * 7) % 3)) for k, x in enumerate(range(1690, 1010, -56))]


def thaw():
    """2 · the thaw (s6): central Greenland about 14 C warmer, the ice sheet recedes about 500 units, forests march north from the
    right, people walk onto the land the ice has left."""
    edges = [920, 790, 660, 530, 400]
    prof = [_nye(e) for e in edges]
    dome = poly([[-20, TG]] + prof[0] + [[920, TG]], ICE, "none", 0, -1)
    flow = [line([[x, y + 30 + 34 * j] for x, y in prof[0][::3] if x < 860 - 120 * j], -1, "#b9cfe0", 2, curve=True, draw=False, op=.7) for j in range(3)]
    er = []
    for k in range(1, 5):                    # each eraser also covers the rim drawn for the edge before it
        outer = [[x, y - 5] for x, y in prof[k - 1]]
        outer[-1] = [edges[k - 1] + 5, TG]
        er += [_sky_eraser(outer, prof[k], round(3.4 + .45 * k, 2)), line(prof[k], round(3.6 + .45 * k, 2), "#ffffff", 2, curve=True, draw=False, op=.7)]
    rim = []
    hills = poly([[860, TG], [1000, 614], [1150, 602], [1300, 588], [1450, 580], [1600, 572], [1800, 568], [1800, TG]], "#2a2229", "none", 0, -1, True)
    hy = lambda x: 640 - (x - 860) / 940 * 72 if x > 860 else 640
    trees = [conifer(x, round(hy(x) + 6, 1), h, round(5.0 + .11 * k, 2)) for k, (x, h) in enumerate(TREES)]
    tube = thermo_glyph(1640, 150, 350, .9, 1.0, AMBER, 1.2, 1.6)
    haze = {"k": "poly", "p": P([[-20, SKYBOX[0]], [-20, 520], [1800, 520], [1800, SKYBOX[1]], [1800, TG], [-20, TG]]), "fill": "url(#k-sky-dusk)", "c": "none", "w": 0, "in": -1}
    els = [haze, hills, dome] + flow + er + rim + trees + tube + [
        lab(1608, 254, "+14 °C", 2.6, AMBER, 34, "end"),
        lab(150, 600, "ice sheet", .6, "#2c3e4e", 30, halo=False)] + \
        [person_s(x, TG, 74, round(7.0 + .3 * k, 2), "#f0dcc0") for k, x in enumerate((640, 700, 760))] + \
        [arrow([[820, TG + 22], [690, TG + 24], [520, TG + 22]], 7.6, AU, 3, "inferred", 1.0)]
    return {"base": "sky", "tod": "dusk", "ground": TG, "groundc": "#3b3128", "sun": [1250, 420, 18], "ridges": [], "cam": [1, 889, 500], "els": els}


def thaw_cold():
    """(s7, the world beat's second line) less than 2,000 years later: the sky greys, snow, two trees at the edge frost over,
    the ice edge creeps forward (dashed); a strip timeline from 14,700 to 12,900."""
    r = random.Random(12)
    snow = [dot(round(r.uniform(80, 1700), 1), round(r.uniform(230, 630), 1), round(r.uniform(2, 4), 1), "#f4f8ff", round(2.8 + .03 * k, 2), op=.85) for k in range(56)]
    edge = _nye(560)
    frost = [conifer(x, round(640 - (x - 860) / 940 * 72 + 6, 1), h, round(3.4 + .3 * j, 2), "rgba(232,242,252,.62)", fx="fade") for j, (x, h) in enumerate(TREES[-1:-3:-1])]
    return [poly([[-20, -20], [1800, -20], [1800, TG], [-20, TG]], "#5d6470", "none", 0, 2.2, dur=1.6, op=.42, keepop=True),
            line([[300, 168], [1000, 168]], .2, BONE, 3, dur=1.2), line([[300, 156], [300, 180]], .2, BONE, 3, draw=False),
            line([[1000, 156], [1000, 180]], 1.2, BONE, 3, draw=False),
            lab(300, 214, "14,700", .4, AMBER, 26), lab(1000, 214, "12,900", 1.3, BLUE, 26),
            lab(650, 150, "under 2,000 years", 1.5, BONE, 30)] + snow + frost + \
           [line(edge, 3.9, "#ffffff", 3, "inferred", 1.0, True), arrow([[430, 600], [540, 600]], 4.3, "#ffffff", 3, "inferred", .6, False)]


def dryas():
    """3 · the Younger Dryas (s8): a mountain avens on the tundra, eight white petals and a gold centre opening; beside it a core of
    lake mud in which one band of its little leaves turns up."""
    fx, fy = 640, 420
    petals = [poly(rell(round(fx + 52 * math.cos(math.radians(45 * k)), 1), round(fy + 52 * math.sin(math.radians(45 * k)), 1), 46, 22, 45 * k, 20),
                   "#f7f4ec", "#d8d2c4", 1.5, round(2.9 + .09 * k, 2), True, fx="pop") for k in range(8)]
    leaves = []
    for k, (lx, ly, a) in enumerate(((548, 690, -20), (735, 686, 15), (600, 718, -8), (690, 720, 10))):
        sc = [[lx + 52 * (1 + .07 * math.sin(9 * t)) * math.cos(t), ly + 18 * (1 + .07 * math.sin(9 * t)) * math.sin(t)] for t in [2 * math.pi * j / 54 for j in range(54)]]
        leaves.append(poly(rot(sc, lx, ly, a), "#3f6a3a", "#7fa35a", 1.5, round(2.4 + .1 * k, 2), True, fx="pop"))
    stamens = [dot(round(fx + 12 * math.cos(2 * math.pi * k / 9), 1), round(fy + 12 * math.sin(2 * math.pi * k / 9), 1), 3.5, "#fff1b8", round(3.9 + .02 * k, 2)) for k in range(9)]
    r = random.Random(6)
    lichen = [dot(round(r.uniform(80, 1700), 1), round(r.uniform(600, 780), 1), round(r.uniform(2, 6), 1), r.choice(["#8a8a5a", "#6f7a4a", "#a39a70"]), -1, op=.7) for _ in range(90)]
    cx0, cy0, cy1 = 1180, 170, 770
    core = [box(cx0, cy0, 90, cy1 - cy0, "#5a4a3a", BONE, 2, 6, 5.2, fx="rise")] + \
           [line([[cx0 + 2, y], [cx0 + 88, y]], 5.4, "#7a6650" if k % 2 else "#3f3328", 3, draw=False) for k, y in enumerate(range(cy0 + 12, cy1, 14))]
    band = [box(cx0 + 2, 466, 86, 26, "#4d6a3e", r=2, at=6.1)] + \
           [poly(rell(cx0 + 14 + 16 * k, 479, 7, 3.5, -20 + 12 * k, 12), "#9cc47a", "none", 0, round(6.2 + .07 * k, 2), True, fx="pop") for k in range(5)] + \
           [glow(cx0 + 45, 479, 90, 6.3, .7, "lamp")]
    els = lichen + [line([[fx, fy + 30], [fx - 6, 560], [fx + 6, 700]], 2.2, "#4f7a40", 5, curve=True, dur=.6)] + leaves + petals + \
          [glow(fx, fy, 80, 3.8, .7, "lamp"), dot(fx, fy, 19, AU, 3.8)] + stamens + [
          lab(fx, 230, "Younger Dryas", 1.4, AU, 50, st="serif")] + core + band + [
          lab(cx0 + 120, cy0 + 30, "lake mud", 5.8, BONE, 30, "start"),
          lab(cx0 + 120, 487, "its leaves", 6.8, "#b9dc9a", 30, "start"),
          line([[790, 690], [1000, 610], [cx0 - 10, 482]], 6.5, AU, 2.5, "inferred", .8, True)]
    return {"base": "sky", "tod": "night", "ground": 560, "groundc": "#2c2820", "sun": False, "cam": [1, 889, 500], "els": els}


def icecore():
    """4 · how we know (s9): Greenland's ice sheet in section, a drill on top; snow falls; seasonal bands, a dusty spring line and a
    pale summer one, laid down year on year and pressed thinner with depth; a core lifts out; beside it a tree's rings."""
    cx, L, Hh, BED = 520, 470, 340, 720
    hgt = lambda x: Hh * max(0, 1 - (abs(x - cx) / L) ** 2.4) ** .5
    xs = [cx - L + 10 * k for k in range(int(2 * L / 10) + 1)]
    dome = poly([[x, round(BED - hgt(x), 1)] for x in xs], "#dbe8f2", "#ffffff", 2, .2, False, fx="rise")
    lay = [line([[x, round(BED - hgt(x) * f, 1)] for x in xs if hgt(x) * f > 4], round(9.4 + .18 * j, 2), "#9fb8cc", 2, curve=True, dur=.6)
           for j, f in enumerate((.9, .78, .67, .57, .48, .4, .33, .27, .22, .18, .145, .115))]
    r = random.Random(3)
    snow = [dot(x, y, 4, "#ffffff", round(2.6 + .05 * k, 2), op=.9) for k, (x, y) in enumerate(scatter(28, 160, 900, 140, 250, 7))]
    tower = [line([[cx - 36, BED - Hh], [cx, BED - Hh - 96], [cx + 36, BED - Hh]], 1.0, BONE, 3, dur=.5),
             line([[cx - 24, BED - Hh - 32], [cx + 24, BED - Hh - 32]], 1.2, BONE, 2, draw=False), line([[cx - 13, BED - Hh - 64], [cx + 13, BED - Hh - 64]], 1.2, BONE, 2, draw=False),
             line([[cx, BED - Hh], [cx, BED - 6]], 1.4, "#3b5368", 3, "inferred", 1.0)]
    bed = [box(40, BED, 1000, 120, "#3a2f26", r=0, at=-1), line([[40, BED], [1040, BED]], -1, "#8c7152", 2, draw=False)]
    # the magnified column: one year per pair of lines (spring dust, summer), thick near the top, thinner with depth
    c0, c1, ctop, cbot = 1100, 1250, 160, 760
    col = [box(c0, ctop, c1 - c0, cbot - ctop, "#9fb6c8", "#ffffff", 2, 6, 4.8, fx="rise"),
           line([[cx + 6, BED - Hh + 60], [c0 - 6, ctop + 4]], 4.9, BONE, 1.5, "inferred", .6), line([[cx + 6, BED - Hh + 120], [c0 - 6, cbot - 4]], 5.0, BONE, 1.5, "inferred", .6)]
    y, th, k, yrs = ctop + 10, 62.0, 0, []
    while y + th * .5 < cbot - 6:
        yrs.append((round(y, 1), round(th, 1)))
        y += th; th = max(7.0, th * .84); k += 1
    bands = []
    for k, (yy, th) in enumerate(yrs):
        at_d = 5.6 if k == 0 else round(9.4 + .07 * k, 2)
        at_s = 7.6 if k == 0 else round(9.45 + .07 * k, 2)
        bands += [box(c0 + 2, round(yy + th * .45, 1), c1 - c0 - 4, round(max(2.5, th * .42), 1), "#eef6fb", r=1, at=at_s),
                  line([[c0 + 2, yy], [c1 - 2, yy]], at_d, "#7a5c3c", max(2.0, min(5.0, th * .12)), draw=False)]
    y1, th1 = yrs[1]
    y2, th2 = yrs[2]
    bands += [line([[c1 + 14, y2], [c1 + 14, y2 + th2]], 12.3, AU, 3, dur=.4), line([[c1 + 6, y2], [c1 + 22, y2]], 12.3, AU, 3, draw=False),
              line([[c1 + 6, y2 + th2], [c1 + 22, y2 + th2]], 12.5, AU, 3, draw=False), lab(c1 + 32, y2 + th2 / 2 + 10, "one year", 12.6, AU, 30, "start"),
              line([[c1 + 4, yrs[0][0]], [c1 + 24, yrs[0][0]]], 6.0, "#d9b48a", 2, draw=False), lab(c1 + 32, yrs[0][0] + 9, "spring dust", 6.0, "#d9b48a", 28, "start")]
    core = {"k": "core", "x": cx + 96, "y": BED - Hh - 6, "w": 30, "h": 120, "grooves": 10, "in": 12.9, "fx": "rise"}
    tree = [{"k": "circle", "x": 1560, "y": 470, "r": 122, "fill": "#a8845c", "c": "#6b4f35", "w": 3, "in": 13.3, "fx": "pop"}] + \
           [ring(1560, 470, rr, round(13.5 + .12 * j, 2), "#6b4f35", 2.5, dur=.3) for j, rr in enumerate((14, 28, 42, 55, 67, 79, 90, 100, 110))] + \
           [lab(1560, 630, "a tree's rings", 14.8, DIM, 26)]
    els = bed + [dome] + lay + tower + snow + [lab(250, 300, "Greenland", 2.4, BONE, 34)] + col + bands + [core] + tree
    return {"base": "dark", "stars": 60, "cam": [1, 889, 500], "els": els}


def count():
    """5 · counting down the core (s10): the core on its side, a tick per century counted from the young end; the cold lights blue
    from 12,900 (12,896) to 11,700 (11,703) years ago."""
    XC = lambda ya: round(160 + (14000 - ya) * 1460 / 3000, 1)
    y0, y1 = 400, 490
    r = random.Random(9)
    stripes = [line([[round(x, 1), y0 + 3], [round(x, 1), y1 - 3]], -1, "#9fb6c8" if k % 2 else "#f2f7fb", round(r.uniform(1, 3), 1), draw=False, op=.8)
               for k, x in enumerate(sorted(r.uniform(166, 1614) for _ in range(260)))]
    core = [box(160, y0, 1460, y1 - y0, "#cfe0ec", "#ffffff", 2, 40, .2, fx="rise")]
    ticks = [line([[XC(14000 - 100 * k), y0 - 30], [XC(14000 - 100 * k), y0 - 8]], round(.8 + .1 * (30 - k), 2), BONE if k % 10 else AU, 2.5 if k % 10 else 3.5, draw=False)
             for k in range(31)]
    years = [lab(XC(y), y0 - 46, "{:,}".format(y), round(.9 + .1 * (30 - (14000 - y) / 100), 2), DIM, 26) for y in (14000, 13000, 12000, 11000)]
    a, b = XC(12896), XC(11703)
    seg = (b - a) / 24
    cold = [box(round(a + seg * k, 1), y0 - 3, round(seg + .6, 1), y1 - y0 + 6, "rgba(120,190,240,.62)", r=0, at=round(2.6 + .18 * k, 2), dur=.25) for k in range(24)] + \
           [line([[XC(12896), y0 - 6], [XC(12896), y1 + 30]], 3.2, AU, 3, dur=.4), lab(XC(12896), y1 + 66, "12,900", 3.6, AU, 34),
            line([[XC(11703), y0 - 6], [XC(11703), y1 + 30]], 6.6, AU, 3, dur=.4), lab(XC(11703), y1 + 66, "11,700", 7.0, AU, 34),
            glow((XC(12896) + XC(11703)) / 2, (y0 + y1) / 2, 360, 7.2, .35, "scan")]
    els = core + [dict(e, **{"in": .5}) for e in stripes] + ticks + years + [
        arrow([[1620, 250], [1100, 250], [500, 250], [170, 250]], .8, AU, 3, "inferred", 3.2, False),
        lab(1620, 226, "counted from the top", .9, AU, 26, "end"),
        lab(1620, y1 + 66, "years ago", 1.2, DIM, 26, "end"), lab(160, y1 + 66, "core laid flat", .6, DIM, 26, "start")] + cold
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": move(els, 0, 70)}


def lake():
    """6 · the lake's diary (s11): a crater lake in Germany in section, yearly layers of light and dark mud filling it from the
    bottom; above the water the winds blow one way, then swing to a new one between two neighbouring layers."""
    G, TOP, BOT, XC, RX = 330, 420, 760, 890, 410
    def half(y):
        u = min(1.0, max(0.0, (y - G) / (BOT - G)))
        return RX * math.sqrt(max(0.0, 1 - u ** 1.25))
    ys_ = [G + (BOT - G) * j / 40 for j in range(41)]
    bowl = [[round(XC - half(y), 1), round(y, 1)] for y in ys_] + [[round(XC + half(y), 1), round(y, 1)] for y in ys_[::-1]]
    rock = [box(-20, G, 1820, 700, "#3d3128", r=0, at=-1)] + \
           [line([[-20, y], [1800, y]], -1, "#5a4a3c", 2, "inferred", draw=False, op=.5) for y in (420, 520, 640, 760)] + \
           [poly([[XC - RX - 70, G], [XC - RX - 30, G - 16], [XC - RX + 10, G]], "#4a3c30", "none", 0, -1), poly([[XC + RX - 10, G], [XC + RX + 30, G - 16], [XC + RX + 70, G]], "#4a3c30", "none", 0, -1)]
    hole = poly(bowl, "#1a2a33", "#8c7152", 2, -1, False)
    n, layers = 44, []
    hgt = (BOT - TOP) / n
    for k in range(n):
        yb = BOT - k * hgt; yt = yb - hgt
        pts = [[XC - half(yt), yt], [XC + half(yt), yt], [XC + half(min(yb, BOT - 1)), yb], [XC - half(min(yb, BOT - 1)), yb]]
        layers.append(poly(pts, "#c4b394" if k % 2 else "#4e3f31", "none", 0, round(4.4 + .045 * k, 3)))
    water = poly([[XC - half(G + 1), G], [XC + half(G + 1), G], [XC + half(TOP), TOP], [XC - half(TOP), TOP]], "rgba(63,134,168,.85)", "#9fd0ff", 1.5, -1)
    ks = 26
    ys = BOT - ks * hgt
    v = View(-6, 18, 42, 58, (90, 125, 330, 190))
    mx, my = v.p(6.76, 50.10)
    win = [{"k": "group", "clip": [v.ox - 10, 120, round(v.p(18, 50)[0] - v.ox + 20, 1), 200, 12], "bg": "#16303d", "in": 2.6, "els": [{"k": "map", "land": v.land()}]},
           dot(mx, my, 8, AU, 3.2), glow(mx, my, 34, 3.2, .9, "lamp"), lab(mx + 14, my - 14, "Germany", 3.4, BONE, 24, "start")]
    old = [arrow([[x, 272], [x + 170, 236]], round(7.4 + .2 * j, 2), "#9fb2c8", 4, dur=.6, curve=False) for j, x in enumerate((560, 820, 1080))]
    for e in old:
        e.update(op=.7, keepop=True)
    new = [arrow([[x, 140], [x + 170, 196]], round(9.8 + .2 * j, 2), AU, 5, dur=.5, curve=False) for j, x in enumerate((560, 820, 1080))]
    switch = [line([[XC - half(ys + hgt), ys + hgt * .5], [XC + RX + 40, ys + hgt * .5]], 9.6, "#9fb2c8", 3, draw=False),
              line([[XC - half(ys), ys - hgt * .5], [XC + RX + 40, ys - hgt * .5]], 10.0, AU, 3, draw=False),
              line([[XC + RX + 52, ys - hgt], [XC + RX + 52, ys + hgt]], 10.2, AU, 3, dur=.3),
              lab(XC + RX + 66, ys + 9, "one year", 10.4, AU, 30, "start")]
    els = rock + [hole] + layers + [water] + win + [
        lab(XC + RX + 66, 640, "yearly layers", 5.6, "#e3d3b4", 30, "start"),
        lab(XC, 318, "a crater lake", 2.2, "#cfe6ff", 28)] + old + new + switch
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": False, "ridges": [], "cam": [1, 889, 500], "els": els}


def clocks():
    """7 · good clocks argue (s12): two strips on one time axis, Greenland's ice and the German lake; each ticks its start of the
    cold; the lake's tick about 167 years later (12,846 against 12,679 years before 1950); the gap bracketed."""
    XA = lambda ya: round(200 + (13100 - ya) * 2.3, 1)
    dy = 60
    xi, xl = XA(12846), XA(12679)
    def face(x, y, a1, a2, at):
        return [{"k": "circle", "x": x, "y": y, "r": 28, "fill": "#1f1a15", "c": BONE, "w": 2.5, "in": at, "fx": "pop"},
                line([[x, y], [round(x + 16 * math.cos(math.radians(a1)), 1), round(y + 16 * math.sin(math.radians(a1)), 1)]], at + .1, BONE, 3, draw=False),
                line([[x, y], [round(x + 22 * math.cos(math.radians(a2)), 1), round(y + 22 * math.sin(math.radians(a2)), 1)]], at + .1, AU, 2.5, draw=False)]
    els = [{"k": "axis", "x0": 200, "x1": 1580, "y": 650, "ticks": [[XA(13100 - 100 * k), ""] for k in range(7)], "in": .2},
           lab(200, 700, "older", .3, DIM, 26, "start"), lab(1580, 700, "younger", .3, DIM, 26, "end"),
           box(200, 300, 1380, 52, ICE, r=6, at=.4, fx="rise"), lab(200, 284, "Greenland ice", .5, ICE, 30, "start"),
           box(200, 450, 1380, 52, "#7a6248", r=6, at=.8, fx="rise"), lab(200, 434, "German lake", .9, "#d9b48a", 30, "start"),
           box(xi, 300, 1580 - xi, 52, "rgba(95,168,201,.75)", r=0, at=1.5, fx="fill", dur=.6),
           line([[xi, 286], [xi, 660]], 1.4, AU, 3, dur=.5),
           box(xl, 450, 1580 - xl, 52, "rgba(95,168,201,.75)", r=0, at=2.5, fx="fill", dur=.6),
           line([[xl, 436], [xl, 660]], 2.4, AU, 3, dur=.5),
           lab(1400, 340, "cold", 1.8, "#0d2230", 28, halo=False), lab(1400, 490, "cold", 2.8, "#0d2230", 28, halo=False),
           line([[xi, 585], [xl, 585]], 3.0, AU, 3, dur=.6), line([[xi, 572], [xi, 598]], 3.0, AU, 3, draw=False), line([[xl, 572], [xl, 598]], 3.3, AU, 3, draw=False),
           lab((xi + xl) / 2, 566, "over 150 years", 3.4, AU, 32)] + face(130, 326, -90, -10, 5.0) + face(130, 476, -60, 40, 5.3)
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": move(els, 0, dy)}


# ================================================================ chapter 2 · The comet's case
# the Laurentide ice sheet at about 12,900 years ago (schematic outline: its southern margin north of the Great Lakes and the
# St Lawrence), and a remnant of the Cordilleran ice in the western mountains
ICE13 = [(-133, 69.6), (-127, 66.4), (-122, 63.0), (-117, 60.0), (-113, 57.4), (-108, 55.0), (-102, 53.4), (-98, 52.4), (-93, 50.9), (-89, 49.6),
         (-85, 49.0), (-81, 48.6), (-77, 48.1), (-73, 48.0), (-70, 48.7), (-67, 49.8), (-63, 50.6), (-59, 51.7), (-57, 53.5), (-60, 56.5), (-62, 58.8),
         (-64, 61.0), (-68, 64.0), (-74, 68.0), (-82, 72.0), (-100, 76.0), (-120, 75.0), (-135, 72.0)]
CORD13 = [(-128, 58.2), (-123, 57.0), (-119, 53.5), (-116.5, 50.5), (-118.5, 49.6), (-122.5, 52.2), (-126.5, 55.2)]


def claim():
    """9 · the 2007 claim (s15), drawn dotted: a comet or its fragments explode over northern North America; shock waves; fires
    across the land; the ice sheet shaken and its meltwater run off to the Atlantic."""
    v = View(-150, -40, 18, 74, (90, 120, 1600, 680))
    pp = lambda q: [list(v.p(*p_)) for p_ in q]
    hit = v.p(-92, 57)
    bursts = [(-97, 53.5), (-83, 52.5), (-104, 58), (-89, 60)]
    fires = [(-121, 39), (-112, 44), (-104, 38), (-98, 34), (-91, 41), (-84, 35.5), (-79, 40.5), (-117, 48), (-100, 46), (-88, 46), (-109, 33), (-80, 34)]
    margin = [q for q in ICE13 if q[1] < 52 and q[0] > -100]
    els = [{"k": "map", "land": v.land(), "in": -1},
           poly(pp(ICE13), "rgba(235,245,255,.45)", "#ffffff", 1.6, -1), poly(pp(CORD13), "rgba(235,245,255,.4)", "#ffffff", 1.4, -1, True),
           lab(*v.p(-103, 66), "ice sheet", .6, "#e6eef6", 32, st="ital"),
           lab(170, 175, "the 2007 claim", .8, LILAC, 30, "start"),
           line([[1720, 120], list(hit)], 4.0, LILAC, 4, "claimed", 1.0), lab(1690, 176, "a comet?", 4.4, LILAC, 30, "end")] + \
          [line([list(hit), list(v.p(*b))], round(5.0 + .12 * k, 2), LILAC, 2.5, "claimed", .4) for k, b in enumerate(bursts)] + \
          [g for k, b in enumerate(bursts) for g in (glow(*v.p(*b), 80, round(5.5 + .12 * k, 2), .9, "red"), dot(*v.p(*b), 7, "#ffe7e0", round(5.5 + .12 * k, 2)))] + \
          [g for k, b in enumerate(bursts) for g in (ring(*v.p(*b), 34, round(8.6 + .14 * k, 2), LILAC, 2.5, "claimed"), ring(*v.p(*b), 64, round(8.9 + .14 * k, 2), LILAC, 2, "claimed"))] + \
          [glow(*v.p(*f), 26 + 6 * (k % 3), round(10.3 + .06 * k, 2), .95, "fire") for k, f in enumerate(fires)] + \
          [line(pp(margin), 11.8, LILAC, 3, "claimed", 1.0, True)] + \
          [glow(*v.p(lo, la), 60, round(12.0 + .08 * k, 2), .6, "scan") for k, (lo, la) in enumerate(margin[::2])] + \
          [arrow(pp([(-71, 47.5), (-62, 45.5), (-52, 43)]), 13.6, BLUE, 3.5, "claimed", 1.0), lab(*v.p(-50, 38.5), "to the Atlantic", 14.2, BLUE, 28)]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def dig():
    """10 · the ground read like pages (s16 to s18): a riverbank cut, layers filling from the bottom, newer up, older down; the black
    mat at about 50 Clovis-age sites (an inset map, positions schematic); below it Clovis points and mammoth bones; above it, none."""
    from f03 import _on_land
    G = 330
    bands = [(680, 1000, "#7a6248", .5), (560, 680, "#5f4c39", 1.0), (425, 560, "#8a6a4a", 1.5), (G, 425, "#6f5a43", 2.0)]
    els = [box(-20, y0, 1820, y1 - y0, c, r=0, at=at, fx="fill", dur=.6) for y0, y1, c, at in bands] + \
          [line([[-20, y], [1800, y]], at, "#e9dccb", 1.2, draw=False, op=.3) for y, at in ((680, .9), (560, 1.4), (425, 1.9))] + \
          [line([[-20, G], [1800, G]], -1, "#c9ad85", 2.5, draw=False)] + \
          [line([[30 + 33 * k, G], [36 + 33 * k, G - 12 - 4 * (k % 3)]], -1, "#7fa35a", 2, draw=False) for k in range(54)] + \
          [person(210, G, 112, .3, "#e8d6b8"), line([[234, G - 60], [286, G - 14]], .5, "#c9a370", 5, draw=False)] + \
          [arrow([[1690, 352], [1690, 760]], 3.0, BONE, 2.5, dur=1.0, curve=False), lab(1672, 370, "newer", 3.0, BONE, 26, "end"), lab(1672, 762, "older", 4.0, BONE, 26, "end")]
    v = View(-125, -66, 24, 50, (1110, 124, 520, 182))
    r = random.Random(50)
    sites = []
    while len(sites) < 50:
        lo, la = r.uniform(-122, -72), r.uniform(28, 48)
        if _on_land(lo, la):
            sites.append((lo, la))
    w = round(v.p(-66, 40)[0] - v.ox + 24, 1)
    els += [{"k": "group", "clip": [v.ox - 12, 118, w, 196, 12], "bg": "#16303d", "in": 5.6, "els": [{"k": "map", "land": v.land()}]},
            {"k": "rect", "x": v.ox - 12, "y": 118, "w": w, "h": 196, "r": 12, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": 5.6}] + \
           [dot(*v.p(lo, la), 4.5, GOLD, round(6.0 + .028 * k, 3)) for k, (lo, la) in enumerate(sites)] + \
           [glow(*v.p(-98, 37), 140, 7.2, .3, "lamp"), lab(v.ox - 30, 222, "about 50 sites", 7.2, BONE, 30, "end")]
    els += clovis(470, 300, 120, 10.0) + [glow(470, 250, 90, 10.0, .5, "lamp")]
    els += [line([[-20, 410], [1800, 410]], 12.0, "#0f0c0a", 30, dur=1.2), line([[-20, 395], [1800, 395]], 12.6, "#4a4038", 1.5, draw=False),
            lab(889, 377, "black mat", 13.3, BONE, 30)]
    pts = [p_ for k, x in enumerate((380, 450, 520)) for p_ in clovis(x, 528, 72, round(16.0 + .2 * k, 2))]
    bones = bone(610, 500, 750, 474, 17.5, 11) + bone(770, 522, 880, 514, 17.7, 10) + \
            [line([[870, 468], [910, 480], [945, 508], [958, 540]], 17.9, "#efe6d4", 9, curve=True, dur=.5)]
    els += pts + [lab(450, 552, "Clovis points", 16.6, BONE, 26)] + bones + [lab(760, 552, "mammoth bones", 18.0, BONE, 26)]
    els += [line([[540, 368], [640, 360]], 20.6, BONE, 3, "claimed", .4)] + \
           clovis(1180, 388, 46, 20.8, "none", BONE, "claimed", fx="fade", w=2.5) + \
           [strike(530, 386, 652, 342, 21.3), strike(1158, 392, 1202, 338, 21.5)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def clues():
    """(beat 4, on the dig, framed closer) the thin layer at the base of the mat, boxed dotted (the reported layer); a magnifier on what
    the team reported in it: magnetic grains, microspherules, soot, nanodiamonds."""
    cx, cy, R = 1390, 592, 168
    r = random.Random(19)
    grains = [poly([[x + r.uniform(-14, -8), 478 + r.uniform(-10, -4)], [x + r.uniform(4, 12), 478 + r.uniform(-12, -6)], [x + r.uniform(10, 16), 478 + r.uniform(2, 8)],
                    [x + r.uniform(-4, 4), 478 + r.uniform(8, 14)], [x + r.uniform(-16, -10), 478 + r.uniform(0, 6)]], "#5c6670", "#9fd0ff", 1.5, round(4.4 + .1 * k, 2), fx="pop")
              for k, x in enumerate((1310, 1360, 1415, 1470))]
    beads = [g for k, x in enumerate((1280, 1335, 1390, 1445, 1500)) for g in (
        {"k": "circle", "x": x, "y": 550, "r": 13, "fill": "#3d434a", "c": "#c8d2dc", "w": 1.5, "in": round(6.8 + .1 * k, 2), "fx": "pop"},
        dot(x - 4, 545, 3.5, "#ffffff", round(6.9 + .1 * k, 2), op=.8))]
    soot = [dot(round(r.uniform(1290, 1490), 1), round(r.uniform(608, 632), 1), round(r.uniform(2.5, 5), 1), "#050404", round(8.8 + .03 * k, 2)) for k in range(16)]
    dia = [g for k, x in enumerate((1345, 1380, 1415, 1450)) for g in (
        line([[x - 8, 690], [x + 8, 690]], round(9.8 + .1 * k, 2), "#ffffff", 2, draw=False), line([[x, 682], [x, 698]], round(9.8 + .1 * k, 2), "#ffffff", 2, draw=False),
        glow(x, 690, 16, round(9.8 + .1 * k, 2), .9, "scan"))]
    return [box(30, 417, 1720, 18, "rgba(201,193,238,.10)", LILAC, 2.5, 4, 2.8, style="claimed"),
            lab(330, 455, "the thin layer", 3.2, LILAC, 26, "start")] + mag(cx, cy, R, 3.8, "#1b1612", -1, 1.6) + \
           [line([[cx, 435], [cx, cy - R]], 3.9, LILAC, 2, "claimed", .3)] + grains + beads + soot + dia + \
           [lab(cx - R - 18, 486, "magnetic grains", 4.8, LILAC, 28, "end"), lab(cx - R - 18, 558, "microspherules", 7.6, LILAC, 28, "end"),
            lab(cx - R - 18, 628, "soot", 8.9, LILAC, 28, "end"), lab(cx - R - 18, 698, "nanodiamonds", 10.0, LILAC, 28, "end")]


def map18():
    """11 · eighteen sites by 2013 (s20, positions schematic) across North America, Europe and the Middle East; then Earth's surface
    as ten squares, one of them lilac: about a tenth."""
    v = View(-128, 50, 10, 64, (90, 120, 1600, 520))
    na = [(-120.1, 34.0), (-117.6, 33.4), (-110.1, 31.6), (-103.3, 34.3), (-113.9, 53.6), (-100.6, 49.4), (-93.6, 37.6), (-84.7, 42.9), (-83.6, 40.7),
          (-77.4, 35.6), (-81.4, 33.4), (-81.6, 33.0), (-77.3, 34.2), (-76.5, 40.7)]
    eu, me = [(5.3, 51.2), (6.4, 52.5), (7.6, 52.6)], [(38.4, 35.9)]
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for k, (lo, la) in enumerate(na + eu + me):
        at = round(3.2 + .1 * k, 2) if k < 14 else (round(5.4 + .1 * (k - 14), 2) if k < 17 else 6.6)
        x, y = v.p(lo, la)
        els += [glow(x, y, 30, at, .8, "scan"), dot(x, y, 7.5, LILAC, at)]
    els += [lab(*v.p(-38, 50), "18 sites", 7.0, LILAC, 36), lab(*v.p(-38, 45.5), "by 2013", 7.2, DIM, 26)]
    x0, sz, gap, y = 560, 46, 12, 682
    els.append(box(300, 652, 1180, 108, "rgba(13,11,9,.82)", "rgba(255,236,206,.25)", 1.5, 14, 9.4))
    for k in range(10):
        els.append(box(x0 + k * (sz + gap), y, sz, sz, "rgba(245,236,220,.06)", BONE, 2, 4, round(9.6 + .06 * k, 2), fx="pop"))
    els += [box(x0, y, sz, sz, LILAC, "#f5f0ff", 2, 4, 10.9, fx="pop"), glow(x0 + sz / 2, y + sz / 2, 50, 10.9, .8, "scan"),
            lab(x0 - 18, y + 34, "Earth's surface", 9.8, BONE, 28, "end"), lab(x0 + 10 * (sz + gap) + 8, y + 34, "a tenth", 11.2, LILAC, 30, "start")]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def platinum():
    """12 · the platinum in the ice (s21): beside the band where the cold begins, platinum is flat, then climbs over 14 yearly dots to
    at least 100 times its base, then falls back over 7; a plain rock, and a rock from space with gold flecks; from space?"""
    c0, c1, ct, cb, yb = 160, 250, 150, 760, 470
    r = random.Random(4)
    core = [box(c0, ct, c1 - c0, cb - ct, "#cfe0ec", "#ffffff", 2, 8, .3, fx="rise")] + \
           [line([[c0 + 3, y], [c1 - 3, y]], .5, "#9fb6c8", round(r.uniform(1, 2.6), 1), draw=False) for y in range(ct + 10, cb, 9)]
    X_ = lambda j: 520 + 20 * j
    def val(j):
        if j <= 8 or j >= 29:
            return 1
        if j <= 22:
            return 1 + 99 * ((j - 8) / 14) ** 1.3
        return 1 + 99 * (1 - (j - 22) / 7) ** 1.4
    Y_ = lambda j: round(700 - 4.3 * val(j), 1)
    pts = [[X_(j), Y_(j)] for j in range(31)]
    dots = [dot(X_(j), Y_(j), 5.5, AU, round(8.0 + .07 * j, 2) if j <= 8 else (round(9.6 + .14 * (j - 8), 2) if j <= 22 else (round(13.0 + .12 * (j - 22), 2) if j <= 29 else 14.0)))
            for j in range(31)]
    els = core + [lab(720, 180, "2013", 2.4, AU, 44, st="serif"), lab(c1 + 18, ct + 20, "Greenland ice", .6, ICE, 28, "start"),
                  box(c0 - 4, yb - 9, c1 - c0 + 8, 18, BLUE, r=3, at=7.2, fx="pop"), glow((c0 + c1) / 2, yb, 70, 7.2, .7, "scan"),
                  lab(c1 + 18, yb + 9, "start of the cold", 7.4, BLUE, 26, "start"),
                  line([[c1 + 6, yb], [500, 700]], 7.6, BLUE, 2, "inferred", .6),
                  line([[500, 700], [1150, 700]], 7.6, "#e9dccb", 2.5, dur=.6), line([[500, 700], [500, 250]], 7.7, "#e9dccb", 2, dur=.5),
                  line(pts[:9], 8.0, AU, 3, dur=.6), line(pts[8:23], 9.6, AU, 3, dur=2.0), line(pts[22:30], 13.0, AU, 3, dur=.8), line(pts[29:], 14.0, AU, 3, dur=.3)] + dots + [
                  lab(530, 236, "platinum", 8.4, AU, 32, "start"),
                  glow(X_(22), Y_(22), 70, 11.4, .8, "lamp"), lab(X_(22) - 24, Y_(22) - 2, "100 times", 11.6, AU, 30, "end"),
                  line([[X_(8), 722], [X_(22), 722]], 11.6, BONE, 2, dur=.4), lab((X_(8) + X_(22)) / 2, 758, "14 years", 11.8, BONE, 28),
                  line([[X_(22), 722], [X_(29), 722]], 13.8, BONE, 2, dur=.3), lab((X_(22) + X_(29)) / 2 + 20, 758, "7 years", 14.0, BONE, 28),
                  poly([[1250, 600], [1280, 560], [1340, 548], [1390, 570], [1400, 612], [1350, 640], [1280, 636]], "#7f7a72", "#c9c3b5", 2, 15.8, True, fx="pop"),
                  lab(1325, 690, "ordinary rock", 16.2, DIM, 26),
                  poly([[1480, 560], [1515, 512], [1580, 500], [1630, 530], [1640, 580], [1590, 616], [1510, 612]], "#5d4c3c", "#e9d3ab", 2, 18.6, True, fx="rise")] + \
          [dot(x, y, 4, AU, round(18.8 + .06 * k, 2)) for k, (x, y) in enumerate(((1530, 545), (1572, 528), (1600, 572), (1548, 590), (1610, 548)))] + \
          [glow(1560, 560, 110, 18.8, .5, "lamp"),
           arrow([[1540, 500], [1300, 330], [X_(22) + 26, Y_(22) + 14]], 19.4, LILAC, 3, "claimed", .9),
           lab(1560, 690, "from space?", 19.8, LILAC, 30)]
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": els}


EUPHRATES = [(37.95, 37.5), (37.97, 37.05), (38.01, 36.82), (38.1, 36.6), (38.2, 36.38), (38.25, 36.2), (38.15, 36.05), (38.07, 35.96), (38.3, 35.9),
             (38.56, 35.87), (38.8, 35.9), (39.0, 35.95), (39.3, 35.85), (39.6, 35.65), (39.9, 35.45), (40.14, 35.33), (40.4, 35.1), (40.6, 34.85), (40.92, 34.45)]
ASSAD = [(38.2, 36.22), (38.31, 36.16), (38.29, 36.02), (38.42, 35.96), (38.57, 35.91), (38.57, 35.85), (38.42, 35.84), (38.22, 35.89), (38.06, 35.92),
         (38.09, 36.04), (38.17, 36.16)]
ABU = (38.40, 35.866)


def syria(settled=False, v=None):
    """13 · Abu Hureyra (s22): northern Syria, the Euphrates drawing itself, the village by the river, dug in the 1970s just before the
    reservoir (Lake Assad, schematic outline) drowned it."""
    t = (lambda a: -1) if settled else (lambda a: a)
    v = v or View(36, 41, 34.5, 37.5, (90, 120, 1600, 680))
    ax, ay = v.p(*ABU)
    els = [{"k": "map", "land": v.land(), "in": -1},
           line([list(v.p(*q)) for q in EUPHRATES], t(4.6), "#6fb6d6", 5, curve=True, dur=1.4),
           lab(*v.p(39.75, 35.75), "Euphrates", t(5.2), "#9fd0ff", 30, st="ital"),
           lab(*v.p(37.3, 35.2), "Syria", t(5.6), BONE, 34, st="ital"), lab(*v.p(38.8, 37.25), "Turkey", t(5.8), DIM, 28, st="ital"),
           lab(*v.p(34.6, 35.6), "Mediterranean", t(6.0), "#9fd0ff", 26, st="ital"),
           glow(ax, ay, 60, t(3.2), .8, "lamp"), dot(ax, ay, 10, AU, t(3.2)),
           poly([list(v.p(*q)) for q in ASSAD], "rgba(63,134,176,.92)", "#cfe6ff", 2, t(12.6), True, dur=1.2),
           lab(ax, ay + 48, "Abu Hureyra", t(3.4), AU, 32),
           lab(ax, ay + 84, "dug in the 1970s", t(9.8), DIM, 26)]
    if not settled:
        els.append({"k": "scale", "x": 140, "y": 760, "w": round(v.km(50), 1), "t": "50 km", "in": 1.0})
    return els, v


def syria_map():
    return {"base": "map", "cam": [1, 889, 500], "els": syria()[0]}


def hut_items(huts, c="#b08a62", style="known"):
    out = []
    for x, z in huts:
        out += [{"t": "cyl", "x": x, "z": z, "y": 0, "r": 3.2, "h": .2, "c": "#4a3a2a", "n": 16, "style": style},
                {"t": "cyl", "x": x, "z": z, "y": 0, "r": 2.4, "h": 1.5, "c": c, "n": 14, "style": style, "edge": "rgba(40,30,20,.5)"}]
    return out


HUTS = [(-20, -10), (-7, -14), (6, -6), (19, -12), (-13, 5), (11, 7)]


def village():
    """14 · the layer from the start of the cold (s23): a small village of round, half-sunken huts on a terrace by the river, people for
    scale; a magnifier on a mud-brick fragment and an animal bone shows glassy droplets; melted, they argued, at over 2,200 C; the
    quote about a car, drawn dotted."""
    items = [{"t": "block", "x0": -30, "x1": 30, "z0": -20, "z1": 18, "y": 0, "ground": True, "layers": [{"h": 1.6, "c": "#7d6a4e"}, {"h": .6, "c": "#1f1812"}, {"h": 2.6, "c": "#5f4c39"}]},
             {"t": "flat", "pts": [[-46, 19], [46, 19], [46, 32], [-46, 32]], "y": -4.8, "c": "#3f86b0"}] + hut_items([(x * .8, z * .8) for x, z in HUTS]) + \
            [{"t": "person", "x": x, "y": 0, "z": z, "h": 1.7, "color": "#efe2c8"} for x, z in ((0, 1), (-4, 10), (20, 1), (2, -15))]
    vil = {"k": "iso", "x": 560, "y": 470, "s": 8, "az": -24, "spin": 0, "el": .42, "items": items, "in": .2, "fx": "fade"}
    mx, my, R = 1150, 410, 160
    r = random.Random(23)
    drops = lambda x0, x1, y0, y1, at, n: [g for k in range(n) for g in (
        poly(rell(round(r.uniform(x0, x1), 1), round(r.uniform(y0, y1), 1), round(r.uniform(5, 9), 1), round(r.uniform(4, 6), 1), r.uniform(0, 90), 12),
             "#1d3a32", "#9fd0c0", 1.2, round(at + .06 * k, 2), True, fx="pop"),)]
    brick = [poly([[1030, 360], [1140, 344], [1150, 420], [1040, 436]], "#9a7a58", "#e9d3ab", 1.5, 4.8, fx="pop")] + \
            [line([[1048 + 18 * k, 372 - 2 * k], [1060 + 18 * k, 420 - 2 * k]], 4.9, "#c9a46a", 1.5, draw=False, op=.7) for k in range(5)]
    bone_ = bone(1170, 470, 1260, 430, 6.0, 14, "#e9e0cc")
    car = [line([[1180, 720], [1180, 692], [1206, 686], [1232, 660], [1320, 656], [1350, 684], [1392, 690], [1394, 720], [1180, 720]], 14.2, BONE, 2.5, "claimed", .8),
           ring(1218, 722, 15, 14.4, BONE, 2.5, "claimed"), ring(1356, 722, 15, 14.4, BONE, 2.5, "claimed"),
           glow(1288, 690, 120, 15.0, .8, "fire"), lab(1288, 640, "melt a car?", 15.1, "#ffb07a", 26),
           line([[1176, 724], [1200, 712], [1236, 700], [1300, 704], [1350, 712], [1398, 724]], 15.5, "#ffb07a", 3, "claimed", .6, True)]
    els = [vil, glow(560, 520, 380, .4, .25, "lamp")] + mag(mx, my, R, 3.2, "#1b1612", -1, 1.4) + \
          [glow(497, 566, 60, 2.0, .8, "scan"), lab(330, 640, "the layer", 1.6, BLUE, 26), line([[520, 566], [mx - R + 6, my + 40]], 3.3, BONE, 2, "inferred", .5)] + brick + drops(1050, 1135, 360, 420, 5.0, 7) + bone_ + drops(1180, 1250, 436, 470, 6.3, 5) + \
          [lab(mx, my + R + 40, "glass", 5.6, "#9fd0c0", 28)] + \
          thermo_glyph(1600, 170, 600, .91, 8.8, "#ff8a5a", 9.0, 1.6) + \
          [line([[1574, 600 - 430 * .88], [1626, 600 - 430 * .88]], 9.0, AU, 3, draw=False), lab(1560, 600 - 430 * .88 + 10, "over 2,200 °C", 10.4, AU, 30, "end"),
           glow(1600, 220, 90, 10.4, .7, "fire")] + car
    return {"base": "dark", "stars": 60, "cam": [1, 889, 500], "els": els}


def gauge(comet_at=None, critics_at=None, x=160, top=210, bot=620):
    """'At its strongest': two columns, the comet camp and the critics; each fills to the top when that camp is at its strongest
    (not a score: each camp's best case, side by side). comet_at / critics_at: when it fills (-1: already full), None: empty."""
    out = []
    for k, (name, c, at) in enumerate((("comet camp", LILAC, comet_at), ("critics", AMBER, critics_at))):
        cx = x + 40 + 140 * k
        out += [box(cx - 40, top, 80, bot - top, "rgba(245,236,220,.04)", BONE, 2, 10, -1, op=.8),
                lab(cx, bot + 42, name, -1, c, 26)]
        if at is not None:
            out += [box(cx - 36, top + 4, 72, bot - top - 8, c, r=8, at=at, fx="fill", dur=1.2, op=.85 if at >= 0 else .5)]
            if at >= 0:
                out += [glow(cx, top + 40, 90, at + 1.0, .6, "lamp"), lab(cx, top - 24, "at its strongest", at + .9, c, 26)]
    return out


def three():
    """15 · the comet camp at its strongest (s24): its column fills; three changes land close together on one time line: the climate
    flips at 12,900, the giants vanish within a few centuries, the Clovis style ends; a dotted line from a comet ties all three."""
    from f03 import mammoth
    X3 = X3D
    LANE = "#1f1914"
    lanes = [(200, "climate", 5.8), (350, "giants", 7.4), (500, "Clovis", 9.4)]
    els = gauge(comet_at=.8)
    els += [box(470, y, 1170, 120, LANE, "rgba(245,236,220,.12)", 1.5, 12, 2.8) for y, _, _ in lanes] + \
           [lab(490, y + 34, t, at, BONE, 26, "start") for y, t, at in lanes] + \
           [{"k": "axis", "x0": 520, "x1": 1600, "y": 680, "ticks": [[X3(y), "{:,}".format(y)] for y in (14000, 13000, 12000, 11000)], "in": 3.0},
            lab(1600, 770, "years ago", 3.2, DIM, 24, "end")]
    warm = [[X3(14000), 236], [X3(13300), 232], [X3(12960), 236]]
    els += [line(warm, 5.9, AMBER, 4, dur=.4), line([[X3(12960), 236], [X3(12880), 284], [X3(12850), 292], [X3(11730), 292]], 6.2, BLUE, 4, dur=.9),
            line([[X3(11730), 292], [X3(11690), 238], [X3(11000), 234]], 6.9, AMBER, 4, dur=.4, op=.5)]
    m1 = mammoth(X3(13650), 431, 46, 7.3, "#d2b48c") + mammoth(X3(13250), 431, 46, 7.45, "#d2b48c")
    m3 = mammoth(X3(12720), 431, 46, 7.6, "#d2b48c")
    er = mammoth(X3(12720), 431, 46, 8.4, LANE)
    for e in er:
        e["w"] = (e.get("w") or 1) + 3; e["c"] = LANE
    ghost = [dict(e, fill="none", c="#b3a48c", w=2, style="claimed", **{"in": 8.6}) for e in m3 if e["k"] == "poly"]
    els += m1 + m3 + er + ghost
    els += [box(X3(13050), 588, X3(12750) - X3(13050), 10, "rgba(232,195,90,.5)", r=4, at=9.4)] + \
           [p_ for k, xx in enumerate((X3(13030), X3(12930), X3(12830))) for p_ in clovis(xx, 584, 52, round(9.5 + .15 * k, 2))] + \
           [box(X3(13090), 524, X3(12790) - X3(13090), 70, LANE, r=6, at=10.6, op=.72, dur=.8)]
    cx3 = X3(12900)
    els += comet(cx3 + 6, 150, 12.2, ang=-40, L=90) + [lab(cx3 + 120, 158, "one cause?", 13.0, LILAC, 28, "start"),
            line([[cx3, 166], [cx3, 660]], 12.6, LILAC, 3, "claimed", 1.0)] + \
           [glow(cx3, y, 70, round(13.6 + .2 * k, 2), .9, "scan") for k, y in enumerate((262, 410, 560))]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


# ================================================================ chapter 3 · The critics answer
def hole():
    """16 · where's the hole? (s26): a plain at dusk with an empty dotted crater and a question mark; north-west Greenland, a ring under
    the ice, the Hiawatha crater (about 31 km, to scale); its age against 12,900 years: a sliver against a bar that runs off the edge."""
    v = View(-74, -10, 59, 84, (1040, 126, 560, 390))
    hx, hy = v.p(-66.75, 78.73)
    rr = 12
    w = round(v.p(-10, 70)[0] - v.ox + 24, 1)
    G = 560
    els = [poly(rell(430, 650, 250, 52), "rgba(20,16,12,.25)", LILAC, 3, .3, True, style="claimed"),
           person(760, G, 92, .6, "#e8d6b8"), person(806, G, 58, .7, "#f0dcc0")] + question(430, 600, 1.0, 90) + \
          [{"k": "group", "clip": [v.ox - 12, 120, w, 398, 12], "bg": "#16303d", "in": 3.0, "els": [{"k": "map", "land": v.land(), "landc": "#d5e2ec"}]},
           {"k": "rect", "x": v.ox - 12, "y": 120, "w": w, "h": 398, "r": 12, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": 3.0},
           lab(v.ox + w - 30, 470, "Greenland", 3.2, "#2c3e4e", 26, "end", halo=False),
           glow(hx, hy, 60, 3.6, .7, "red"), ring(hx, hy, rr, 3.6, "#b03a2e", 4),
           lab(v.ox - 30, hy + 9, "Hiawatha crater", 4.0, BONE, 30, "end"), line([[v.ox - 22, hy], [hx - rr - 4, hy]], 4.0, BONE, 1.5, dur=.4),
           lab(1010, 588, "12,900 years", 5.6, AU, 28, "start"), box(1010, 600, 5, 24, AU, r=1, at=5.8),
           lab(1010, 664, "58 million years", 6.2, BONE, 28, "start"),
           line([[1010, 688], [1800, 688]], 6.4, "#d9cbb4", 16, dur=1.0),
           line([[1458, 700], [1478, 672]], 7.2, "#3b3128", 8, draw=False), line([[1474, 700], [1494, 672]], 7.2, "#3b3128", 8, draw=False)]
    return {"base": "sky", "tod": "dusk", "ground": G, "groundc": "#3b3128", "sun": [240, 470, 20], "cam": [1, 889, 500], "els": els}


def tunguska():
    """17 · 1908, Siberia (s27; the Short 'taurids', redrawn wide): a burst in the sky over a forest, trees felled outward from the
    point under it, and no crater."""
    r = random.Random(3)
    CX, CY = 889, 450
    trees = [dot(round(x, 1), round(y, 1), 3, "#4f6b3a", -1) for x, y in [(r.uniform(60, 1720), r.uniform(150, 790)) for _ in range(900)]]
    felled = []
    for rad in range(70, 420, 26):
        for d in range(0, 360, 10):
            t = math.radians(d + (rad % 3) * 4)
            x0_, y0_ = CX + rad * math.cos(t), CY + rad * .62 * math.sin(t)
            x1_, y1_ = CX + (rad + 20) * math.cos(t), CY + (rad + 20) * .62 * math.sin(t)
            if 120 < y0_ < 790:
                felled.append(line([[round(x0_, 1), round(y0_, 1)], [round(x1_, 1), round(y1_, 1)]], round(1.6 + rad * .0035, 2), "#c9a46a", 2.6, dur=.3))
    els = [box(-20, -20, 1820, 1040, "#1f2a1c", r=0, at=-1)] + trees + [glow(CX, CY, 300, 1.0, .8, "lamp"), glow(CX, CY, 130, 1.0, 1, "red")] + \
          [poly(rell(CX, CY, 60 + 80 * k, (60 + 80 * k) * .62, 0, 40), "none", "#ffe2a8", 2.5, round(1.2 + .2 * k, 2), True, fx="draw", dur=.5) for k in range(4)] + felled + \
          [{"k": "circle", "x": CX, "y": CY, "r": 40, "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 3.0},
           strike(CX - 52, CY + 44, CX + 52, CY - 44, 3.4), lab(CX, CY + 92, "no crater", 3.6, BONE, 30),
           lab(120, 190, "1908, Siberia", 4.4, AU, 44, "start", st="serif")]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def seven():
    """18 · seven sites, no peak (s28): seven columns of sediment, two of them the comet team's own (lilac); bead counts build up each;
    at the level of the start of the cold (gold, dashed) none of them spikes."""
    r = random.Random(28)
    xs = [200 + 200 * k for k in range(7)]
    top, bot, yl = 230, 700, 452
    els = [lab(800, 168, "7 sites", 3.2, BONE, 34), lab(200, 172, "2009", .8, AU, 44, "start", st="serif")]
    for k, x in enumerate(xs):
        own = k in (1, 4)
        els += [box(x - 34, top, 68, bot - top, "#5f4c39", LILAC if own else "#c9ad85", 4 if own else 1.5, 6, round(2.6 + .08 * k, 2), fx="rise")]
        els += [line([[x - 32, y], [x + 32, y]], round(2.7 + .08 * k, 2), "#4a3a2c", 2, draw=False, op=.7) for y in range(top + 30, bot, 40)]
        for j, y in enumerate(range(top + 16, bot - 6, 22)):
            ln_ = r.uniform(8, 34)
            els.append(line([[x + 38, y], [round(x + 38 + ln_, 1), y]], round(6.0 + .02 * j + .05 * k, 2), AU, 6, draw=False))
        if own:
            els.append(lab(x, bot + 40, "original", 5.2, LILAC, 26))
    els += [line([[150, yl], [1490, yl]], 5.8, AU, 3, "inferred", .8), lab(1500, yl + 9, "12,900", 6.0, AU, 28, "start"),
            lab(1500, 540, "no peak", 7.0, BONE, 34, "start"), lab(1500, 260, "bead counts", 6.4, AU, 26, "start")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def graphene():
    """19 · sequels (s29): under a magnifier the claimed nanodiamonds' lattice flattens into a honeycomb sheet, graphene; twelve tiles,
    the original clues, seven of them turn grey; two desks, papers flying back and forth, 2009 and 2012."""
    mx, my, R = 330, 430, 160
    lat = []
    for i in range(4):
        for j in range(4):
            x, y = mx - 75 + 50 * i + (25 if j % 2 else 0), my - 70 + 46 * j
            lat.append(dot(x, y, 7, LILAC, round(.6 + .03 * (4 * i + j), 2)))
            if i < 3:
                lat.append(line([[x, y], [x + 50, y]], .6, LILAC, 2, draw=False, op=.7))
            if j < 3:
                lat.append(line([[x, y], [x + (25 if j % 2 == 0 else -25), y + 46]], .6, LILAC, 2, draw=False, op=.7))
    hexes = []
    for i in range(-2, 3):
        for j in range(-2, 3):
            hx_, hy_ = mx + 52 * i + (26 if j % 2 else 0), my + 45 * j
            if math.hypot(hx_ - mx, hy_ - my) < R - 36:
                hexes.append(poly([[hx_ + 26 * math.cos(math.radians(60 * k + 30)), hy_ + 26 * math.sin(math.radians(60 * k + 30))] for k in range(6)],
                                  "none", "#e9e2d0", 2.5, round(2.2 + .02 * (i + j + 4), 2)))
    els = mag(mx, my, R, .3, "#1b1612", 1, 1.4) + lat + \
          [{"k": "circle", "x": mx, "y": my, "r": R - 6, "fill": "#1b1612", "c": "none", "w": 0, "in": 2.0, "op": .92, "keepop": True}] + hexes + \
          [lab(mx, my - R - 26, "nanodiamonds?", 1.2, LILAC, 28), lab(mx, my + R + 46, "graphene", 2.6, BONE, 30)]
    tx0, ty0, ts, tg = 650, 300, 64, 14
    for k in range(12):
        x, y = tx0 + (k % 6) * (ts + tg), ty0 + (k // 6) * (ts + tg)
        els.append(box(x, y, ts, ts, "rgba(201,193,238,.55)", LILAC, 2, 8, round(7.6 + .08 * k, 2), fx="pop"))
    for j, k in enumerate((0, 2, 3, 5, 7, 8, 10)):
        x, y = tx0 + (k % 6) * (ts + tg), ty0 + (k // 6) * (ts + tg)
        els.append(box(x, y, ts, ts, "#55504a", "#8a8378", 2, 8, round(10.0 + .17 * j, 2)))
    cxm = tx0 + 3 * (ts + tg) - tg / 2
    els += [lab(cxm, ty0 - 80, "2011", 5.6, AU, 44, st="serif"), lab(cxm, ty0 - 30, "12 original clues", 8.6, LILAC, 28), lab(cxm, ty0 + 2 * (ts + tg) + 44, "7 of 12", 11.4, BONE, 34),
            lab(cxm, ty0 + 2 * (ts + tg) + 84, "not reproduced", 11.6, DIM, 26)]
    def desk(x):
        return [line([[x - 80, 560], [x + 80, 560]], 12.6, "#8c7152", 8, draw=False), line([[x - 66, 560], [x - 66, 640]], 12.6, "#8c7152", 5, draw=False),
                line([[x + 66, 560], [x + 66, 640]], 12.6, "#8c7152", 5, draw=False)]
    els += desk(1270) + desk(1590) + [person(1220, 640, 112, 12.6, "#e8d6b8"), person(1640, 640, 112, 12.8, "#e8d6b8")]
    def fly(x0, x1, apex, at, n=3, deg=0):
        out = []
        for k in range(n):
            u = (k + 1) / (n + 1)
            x = x0 + (x1 - x0) * u; y = 540 - (540 - apex) * 4 * u * (1 - u)
            out.append({"k": "group", "tr": "rotate(%d %d %d)" % (deg + 14 * (k - 1), x, y), "in": round(at + .25 * k, 2),
                        "els": [box(x - 20, y - 26, 40, 52, PAPER, "#b8a888", 1.5, 3, -1)] + [line([[x - 12, y - 14 + 10 * j], [x + 12, y - 14 + 10 * j]], -1, "#9a8a72", 2.5, draw=False) for j in range(3)]})
        return out
    els += [line([[1290, 540], [1430, 330], [1570, 540]], 13.0, BONE, 1.5, "inferred", .8, True)] + fly(1290, 1570, 330, 13.2) + [lab(1430, 286, "2009", 13.6, AU, 30)] + \
           [line([[1570, 540], [1430, 450], [1290, 540]], 14.6, BONE, 1.5, "inferred", .8, True)] + fly(1570, 1290, 450, 14.8) + [lab(1430, 512, "2012", 15.2, AU, 30)] + \
           fly(1290, 1570, 150, 17.6, 2, 20) + fly(1570, 1290, 150, 18.4, 2, -20)
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": move(els, 0, 50)}


def mats():
    """20 · black mats everywhere (s30): the Americas with pins in the American southwest and northern Chile; a time axis from 45,000 years
    ago to today; black mats at many ages, the youngest about 6,000, the oldest past 40,000 (those between schematic); the same marker
    specks on every one."""
    v = View(-125, -55, -40, 45, (90, 125, 470, 650))
    w = round(v.p(-55, 0)[0] - v.ox + 24, 1)
    XM = lambda ya: round(1640 - ya * 900 / 45000, 1)
    ages = [(41500, 5), (36000, 3), (30500, 4), (24000, 2), (17500, 3), (12900, 1), (9500, 4), (6000, 2)]
    els = [{"k": "group", "clip": [v.ox - 12, 120, w, 662, 12], "bg": "#16303d", "in": -1, "els": [{"k": "map", "land": v.land()}]},
           {"k": "rect", "x": v.ox - 12, "y": 120, "w": w, "h": 662, "r": 12, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": -1}]
    for k, (lo, la) in enumerate(((-110, 34), (-69.5, -23))):
        x, y = v.p(lo, la)
        els += [glow(x, y, 40, round(5.8 + 1.6 * k, 2), .9, "lamp"), dot(x, y, 9, AU, round(5.8 + 1.6 * k, 2))]
    els += [lab(v.p(-110, 34)[0] + 20, v.p(-110, 34)[1] - 20, "US southwest", 6.2, BONE, 26, "start"),
            lab(v.p(-69.5, -23)[0] + 18, v.p(-69.5, -23)[1] + 8, "northern Chile", 7.8, BONE, 26, "start"),
            {"k": "axis", "x0": 740, "x1": 1640, "y": 640, "ticks": [[XM(y), "{:,}".format(y) if y else "today"] for y in (40000, 30000, 20000, 10000, 0)], "in": 2.2},
            lab(740, 742, "years ago", 2.4, DIM, 24, "start")]
    for k, (ya, row) in enumerate(sorted(ages, key=lambda q: -q[0])):
        x, y = XM(ya), 600 - 70 * row
        at = round(8.8 + .32 * (len(ages) - 1 - k), 2)
        els += [box(x - 36, y - 13, 72, 26, "#0f0c0a", "#8a7a66", 1.5, 7, at, fx="pop"), line([[x, y + 13], [x, 632]], at, "#6a5a48", 1.5, "inferred", draw=False)]
        els += [dot(round(x - 21 + 14 * j, 1), round(y - 2 + (j % 2) * 4, 1), 4, LILAC, round(13.8 + .1 * k + .03 * j, 2)) for j in range(4)]
    els += [lab(XM(6000), 600 - 70 * 2 - 24, "6,000", 9.2, BONE, 28), lab(XM(41500), 600 - 70 * 5 - 24, "over 40,000", 11.2, BONE, 28),
            lab(1190, 160, "same markers, every mat", 15.0, LILAC, 28), lab(1580, 230, "2012", 2.4, AU, 44, st="serif")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def album():
    """21 · the album (s31): pages one after another, confetti on every one; one page with a party hat gets a gold ring; then every
    page gets one: the confetti can't mark the day of the party."""
    r = random.Random(31)
    CF = ["#f2c98e", "#9fd0ff", "#c9c1ee", "#8fd9b0", "#ff8a7a"]
    els = [glow(889, 460, 520, -1, .2, "lamp")]
    for k in range(6):
        cx, cy = 260 + 252 * k, 440 + (16 if k % 2 else -16)
        deg = (-5, 4, -3, 5, -4, 3)[k]
        conf = [dot(round(r.uniform(cx - 80, cx + 80), 1), round(r.uniform(cy - 100, cy + 100), 1), round(r.uniform(3, 6), 1), r.choice(CF), -1) for _ in range(16)]
        photo = [box(cx - 70, cy - 90, 140, 104, "#5a6a74", "#ffffff", 3, 2, -1)] + [person(cx - 24 + 24 * j, cy + 10, 52 - 8 * (j % 2), -1, "#2a2420") for j in range(3)]
        hat = [poly([[cx + 40, cy - 52], [cx + 60, cy - 100], [cx + 80, cy - 52]], "#ff8a7a", "#fff3d6", 2, -1), dot(cx + 60, cy - 102, 6, AU, -1)] if k == 3 else []
        els.append({"k": "group", "tr": "rotate(%d %d %d)" % (deg, cx, cy), "in": round(.2 + .3 * k, 2),
                    "els": [box(cx - 104, cy - 134, 208, 268, "#efe6d2", "#b8a888", 2, 4, -1)] + photo + hat + conf})
    els += [ring(260 + 252 * 3, 440 + 16, 168, 3.0, AU, 5), glow(260 + 252 * 3, 456, 200, 3.0, .5, "lamp")] + \
           [ring(260 + 252 * k, 440 + (16 if k % 2 else -16), 160, round(3.8 + .12 * j, 2), AU, 2.5, "inferred") for j, k in enumerate((0, 1, 2, 4, 5))] + \
           [lab(260 + 252 * 3, 690, "the party?", 3.2, AU, 30)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def flash():
    """22 · one blast, one moment (s32): a clock; a camera flash bursts and four photos fly out in a row, each with the same clock face."""
    def face(x, y, r_, at, c=BONE):
        return [{"k": "circle", "x": x, "y": y, "r": r_, "fill": "#1f1a15", "c": c, "w": 2.5, "in": at, "fx": "pop"},
                line([[x, y], [x, round(y - r_ * .62, 1)]], at + .1, c, 3, draw=False), line([[x, y], [round(x + r_ * .5, 1), round(y + r_ * .3, 1)]], at + .1, AU, 3, draw=False)]
    els = face(889, 210, 56, 1.6) + [lab(889, 300, "time", 1.8, BONE, 30)]
    els += [glow(300, 380, 260, 5.6, 1, "sun"), box(240, 400, 220, 140, "#2a2622", "#cbbca8", 2.5, 14, 4.6, fx="pop"), {"k": "circle", "x": 350, "y": 470, "r": 46, "fill": "#14110e", "c": "#cbbca8", "w": 3, "in": 4.6},
            dot(350, 470, 18, "#3f86a8", 4.7), box(270, 382, 60, 22, "#2a2622", "#cbbca8", 2, 4, 4.6)] + \
           [line([[300, 380], [round(300 + 150 * math.cos(math.radians(a)), 1), round(380 + 150 * math.sin(math.radians(a)), 1)]], 5.6, "#fff3d6", 3, dur=.3)
            for a in range(-170, 10, 30)]
    for k in range(4):
        x = 760 + 230 * k
        els += [{"k": "group", "tr": "rotate(%d %d %d)" % ((-4, 3, -2, 4)[k], x, 470), "in": round(6.6 + .25 * k, 2),
                 "els": [box(x - 92, 380, 184, 190, "#efe6d2", "#b8a888", 2, 4, -1), box(x - 78, 394, 156, 118, "#5a6a74", "none", 0, 2, -1)] +
                        [person(x - 30 + 30 * j, 500, 46, -1, "#2a2420") for j in range(3)]}]
        els += face(x + 50, 540, 20, round(8.0 + .15 * k, 2), INK)
    els += [lab(1105, 640, "the same moment", 8.8, AU, 30)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


X3D = lambda ya: round(520 + (14000 - ya) * 1080 / 3000, 1)
_r29 = random.Random(29)
DATES29 = [12880, 12840, 12820]
while len(DATES29) < 23:                     # 20 more dated sites, none of them inside the window
    _d = round(_r29.uniform(13650, 11450))
    if not 12760 <= _d <= 12940:
        DATES29.append(_d)
DATES29 = sorted(DATES29, key=lambda q: -q)


def _scatter29(at0=2.0, settled=False, X=X3D, ys=(250, 640), hollow_x=470, out_window=True):
    """The 29 claimed sites: 23 dated (3 inside the narrow window at the start of the cold), 6 without a usable date (hollow, aside).
    Positions schematic."""
    t = (lambda a: -1) if settled else (lambda a: a)
    els = []
    r = random.Random(7)
    for k, ya in enumerate(DATES29):
        y = round(ys[0] + (ys[1] - ys[0]) * ((k * 7) % 23) / 22, 1)
        inside = 12800 <= ya <= 12900
        els += [dot(X(ya), y, 9, AU if inside else "#cbbca8", t(round(at0 + .07 * k, 2)))]
        if inside:
            els += [glow(X(ya), y, 40, t(5.2), .9, "lamp")]
    for k in range(6):
        els.append({"k": "circle", "x": hollow_x, "y": round(ys[0] + 60 * k + 20, 1), "r": 9, "fill": "none", "c": "#cbbca8", "w": 2, "in": t(round(at0 + 1.7 + .05 * k, 2))})
    return els


def dates():
    """23 · the sharpest test, time (s32, s33): 29 claimed sites on a time axis 14,000 to 11,000 years ago; a narrow gold window at the
    start of the cold; only 3 inside it; a gentler review: ages up to two centuries apart, some clues hard to explain; the critics at
    their strongest (their column fills)."""
    els = gauge(comet_at=-1, critics_at=15.6)
    els += [{"k": "axis", "x0": 520, "x1": 1600, "y": 690, "ticks": [[X3D(y), "{:,}".format(y)] for y in (14000, 13000, 12000, 11000)], "in": .2},
            lab(1600, 770, "years ago", .3, DIM, 24, "end"),
            box(X3D(12900), 236, X3D(12800) - X3D(12900), 446, "rgba(232,195,90,.25)", AU, 2, 2, .8),
            lab(X3D(12850), 224, "the window", 1.0, AU, 26)]
    els += _scatter29(2.0)
    els += [lab(560, 186, "29 sites", 3.6, BONE, 32, "start"), lab(470, 226, "no date", 3.8, DIM, 24), lab(1450, 190, "2014", .4, AU, 44, st="serif"),
            lab(X3D(12850) + 30, 770, "only 3", 6.4, AU, 30, "start")]
    b0, b1 = X3D(12950), X3D(12750)
    els += [line([[b0, 168], [b1, 168]], 9.8, BLUE, 3, dur=.5), line([[b0, 156], [b0, 180]], 9.8, BLUE, 3, draw=False), line([[b1, 156], [b1, 180]], 10.0, BLUE, 3, draw=False),
            lab(b1 + 18, 178, "up to 2 centuries", 10.6, BLUE, 28, "start")]
    hard = [DATES29[k] for k in (3, 8, 16)]
    pts_h = []
    for k, ya in enumerate(hard):
        kk = DATES29.index(ya)
        y = round(250 + 390 * ((kk * 7) % 23) / 22, 1)
        pts_h.append((X3D(ya), y))
        els.append(ring(X3D(ya), y, 17, round(12.8 + .3 * k, 2), AMBER, 3, dur=.4))
    hx_, hy_ = max(pts_h)
    els += [line([[hx_ + 20, hy_], [1420, 300]], 13.5, AMBER, 1.5, "inferred", .4), lab(1430, 308, "hard to explain", 13.6, AMBER, 26, "start")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def bell():
    """24 · same ground, opposite readings (s34): left, the critics' 29-site scatter; right, the comet team's 354 dates, a cloud, and the
    model they read from them: one bell inside a gold band 100 years wide (12,835 to 12,735 years ago)."""
    XL = lambda ya: round(150 + (14000 - ya) * 680 / 3000, 1)
    XR = lambda ya: round(960 + (13300 - ya) * 690 / 1000, 1)
    els = [lab(475, 168, "critics", .3, AMBER, 32), lab(1305, 168, "comet team", .4, LILAC, 32),
           line([[889, 200], [889, 690]], -1, "rgba(245,236,220,.15)", 2, draw=False),
           {"k": "axis", "x0": 150, "x1": 830, "y": 650, "ticks": [[XL(y), "{:,}".format(y)] for y in (14000, 13000, 12000, 11000)], "in": -1},
           box(XL(12900), 226, XL(12800) - XL(12900), 400, "rgba(232,195,90,.25)", AU, 1.5, 2, -1)] + \
          _scatter29(settled=True, X=XL, ys=(250, 600), hollow_x=110)
    r = random.Random(354)
    cloud = [dot(round(XR(r.gauss(12790, 260)), 1), round(r.uniform(250, 610), 1), 2.6, LILAC, round(2.0 + .0045 * k, 3), op=.55) for k in range(354)]
    cloud = [c for c in cloud if 965 <= c["x"] <= 1650]
    bx0, bx1 = XR(12835), XR(12735)
    mu, sd = (bx0 + bx1) / 2, (bx1 - bx0) / 4
    curve = [[round(mu + d, 1), round(620 - 330 * math.exp(-.5 * (d / sd) ** 2), 1)] for d in range(-90, 91, 6)]
    els += [{"k": "axis", "x0": 960, "x1": 1650, "y": 650, "ticks": [[XR(y), "{:,}".format(y)] for y in (13000, 12500)], "in": .5}] + cloud + \
           [box(bx0, 226, bx1 - bx0, 400, "rgba(232,195,90,.3)", AU, 2, 2, 5.4), line(curve, 5.8, LILAC, 4, curve=True, dur=1.0),
            glow(mu, 420, 120, 6.2, .6, "scan"), lab(bx1 + 16, 280, "within 100 years", 7.0, AU, 28, "start"),
            lab(975, 236, "354 dates", 3.4, LILAC, 26, "start")]
    els += [box(150, 716, 1500, 18, "#5f4c39", "#8c7152", 1.5, 6, 8.8, fx="rise"), lab(889, 770, "same ground", 9.0, BONE, 26),
            arrow([[860, 420], [760, 420]], 10.6, AMBER, 3, dur=.4, curve=False), arrow([[918, 420], [1018, 420]], 10.8, LILAC, 3, dur=.4, curve=False)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def bays():
    """25 · the Carolina Bays (s35, s36; the Short 'carolina-bays', wide): the Atlantic coastal plain, about 170 ovals (positions schematic,
    densest in the Carolinas), their long axes lined up; extended inland they meet near one point by the Great Lakes; then fifteen ring
    lilac (where the layer was reported) and the claimed rain of ice from that point, dotted."""
    from f03 import _bays
    v = View(-96, -62, 30, 45.6, (90, 120, 1600, 680))
    C = v.p(-87.5, 44.5)
    sites = _bays()
    def ov(cx, cy, a, b, ang):
        c, s_ = math.cos(ang), math.sin(ang)
        return [[round(cx + a * math.cos(t) * c - b * math.sin(t) * s_, 1), round(cy + a * math.cos(t) * s_ + b * math.sin(t) * c, 1)] for t in [2 * math.pi * j / 18 for j in range(18)]]
    els = [{"k": "map", "land": v.land(), "in": -1}]
    for i, (lo, la) in enumerate(sorted(sites, key=lambda q: math.sin(q[0] * 37.1 + q[1] * 11.3))):
        x, y = v.p(lo, la); a = math.atan2(C[1] - y, C[0] - x)
        els.append({"k": "poly", "p": ov(x, y, 10, 5.5, a), "fill": "rgba(159,208,255,.4)", "c": "#cfe6ff", "w": 1, "curve": True, "in": round(1.4 + i * .013, 3)})
    sub = sorted(sites, key=lambda q: q[1])[3::12]
    for i, (lo, la) in enumerate(sub):
        x, y = v.p(lo, la); a = math.atan2(C[1] - y, C[0] - x)
        els.append(line([[round(x - 22 * math.cos(a), 1), round(y - 22 * math.sin(a), 1)], [round(x + 22 * math.cos(a), 1), round(y + 22 * math.sin(a), 1)]], round(5.8 + .05 * i, 2), AU, 2.5, dur=.4))
        els.append(line([[round(x + 22 * math.cos(a), 1), round(y + 22 * math.sin(a), 1)], list(C)], round(6.6 + .06 * i, 2), AU, 1.4, "inferred", .8))
    els += [glow(C[0], C[1], 90, 7.6, .9, "lamp"), dot(C[0], C[1], 8, AU, 7.6), lab(C[0] - 20, C[1] - 26, "one point", 7.8, AU, 28, "end"),
            lab(*v.p(-72.5, 33.2), "Carolina Bays", 1.6, "#cfe6ff", 34)]
    fif = sorted(sites, key=lambda q: q[0] * 3 + q[1])[5::11][:15]
    els += [ring(*v.p(lo, la), 13, round(10.8 + .05 * k, 2), LILAC, 3, dur=.3) for k, (lo, la) in enumerate(fif)]
    els += [lab(*v.p(-72.0, 32.0), "layer reported in 15", 11.4, LILAC, 26)]
    icesh = [(-97, 44.6), (-92, 44.2), (-88, 43.9), (-84, 44.9), (-80, 45.6), (-76, 46.0), (-70, 46.4), (-66, 47.5), (-66, 50), (-97, 50)]
    els += [poly([list(v.p(*q)) for q in icesh], "rgba(235,245,255,.25)", "#ffffff", 2, 13.0, True, style="claimed"),
            line([[1720, 120], [C[0] + 8, C[1] - 8]], 13.2, LILAC, 4, "claimed", .8), glow(C[0], C[1], 150, 13.8, .8, "red")] + \
           [arrow([list(C), [round((C[0] + x) / 2 + 30, 1), round(min(C[1], y) - 120, 1)], [x, y]], round(13.9 + .12 * i, 2), LILAC, 2.5, "claimed", .8)
            for i, (x, y) in enumerate([v.p(lo, la) for lo, la in sub[1::2]])] + \
           [lab(*v.p(-70.5, 37.4), "craters?", 14.8, LILAC, 30)]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def sandclock():
    """26 · the sand clock (s37): buried grains charge up in the dark like tiny batteries; measure the charge and you know how long they
    have been buried; the bay rims: 109,000 years old down to 2,000; the proposed blast at 12,800, dotted."""
    r = random.Random(37)
    G = 300
    els = [box(80, G, 720, 470, "#2e251e", "#8c7152", 2, 8, -1), line([[80, G], [800, G]], -1, "#c9ad85", 2.5, draw=False),
           lab(440, G - 26, "buried sand", .4, "#d9c39a", 28)]
    els += [dot(round(r.uniform(100, 780), 1), round(r.uniform(G + 20, 750), 1), round(r.uniform(3, 6), 1), "#d9c39a", round(.4 + .01 * k, 2), op=.8) for k in range(70)]
    els += [glow(round(r.uniform(140, 740), 1), round(r.uniform(G + 40, 720), 1), 18, round(1.8 + .04 * k, 2), .9, "lamp") for k in range(20)]
    for j, x in enumerate((300, 440, 580)):
        els += [box(x - 30, 470, 60, 110, "#1a1511", BONE, 2.5, 6, round(3.6 + .15 * j, 2), fx="pop"), box(x - 12, 458, 24, 12, BONE, r=2, at=round(3.6 + .15 * j, 2)),
                box(x - 22, 480, 44, 92, AU, r=4, at=round(4.0 + .2 * j, 2), fx="fill", dur=2.0)]
    els += [{"k": "circle", "x": 700, "y": 400, "r": 46, "fill": "#1a1511", "c": BONE, "w": 2.5, "in": 5.2, "fx": "pop"},
            line([[700, 400], [728, 372]], 5.6, AU, 3, dur=.3), lab(700, 476, "measure", 5.6, BONE, 26)]
    XS = lambda ya: round(900 + (110000 - ya) * 750 / 110000, 1)
    els += [{"k": "axis", "x0": 900, "x1": 1650, "y": 600, "ticks": [[XS(y), "{:,}".format(y) if y else "today"] for y in (100000, 50000, 0)], "in": 9.6},
            lab(900, 702, "years ago", 9.7, DIM, 24, "start"),
            line([[XS(12800), 300], [XS(12800), 610]], 10.0, LILAC, 3, "claimed", .6), lab(XS(12800), 280, "the proposed blast", 10.2, LILAC, 26),
            lab(1275, 420, "bay rims", 10.6, "#d9c39a", 28)]
    n = 10
    for k in range(n):
        a = 109000 - (109000 - 2000) * k / n; b = 109000 - (109000 - 2000) * (k + 1) / n
        els.append(box(XS(a), 520, round(XS(b) - XS(a) + .5, 1), 26, AU, r=0, at=round(11.0 + .4 * k, 2), dur=.3))
    els += [lab(XS(109000), 500, "109,000", 11.4, AU, 28, "start"), lab(XS(2000), 500, "2,000", 15.0, AU, 28, "end")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def whitepond():
    """27 · White Pond (s38): mud settling in the bay layer by layer; the comet team's own core beside it, 31,000 years; a thin lilac
    line at the 12,800 level stays; the crater outline drawn over the bay is struck through."""
    G, XC, RX, BOT = 300, 760, 360, 700
    half = lambda y: RX * math.sqrt(max(0.0, 1 - ((y - G) / (BOT - G)) ** 1.6))
    ys = [G + (BOT - G) * j / 40 for j in range(41)]
    bowl = [[round(XC - half(y), 1), round(y, 1)] for y in ys] + [[round(XC + half(y), 1), round(y, 1)] for y in ys[::-1]]
    els = [box(-20, G, 1820, 720, "#3b3028", r=0, at=-1), line([[-20, G], [1800, G]], -1, "#8c7152", 2.5, draw=False), poly(bowl, "#22303a", "#8c7152", 2, -1)]
    n = 31; top = G + 30; hgt = (BOT - top) / n
    for k in range(n):
        yb = BOT - k * hgt; yt = yb - hgt
        els.append(poly([[XC - half(yt), yt], [XC + half(yt), yt], [XC + half(min(yb, BOT - 1)), yb], [XC - half(min(yb, BOT - 1)), yb]],
                        "#6b5640" if k % 2 else "#87705a", "none", 0, round(3.4 + .05 * k, 2)))
    els.append(poly([[XC - half(G + 1), G], [XC + half(G + 1), G], [XC + half(top), top], [XC - half(top), top]], "rgba(63,134,176,.8)", "#9fd0ff", 1.5, -1))
    els += [lab(XC, G - 24, "White Pond", .4, "#cfe6ff", 32)]
    c0, c1, ct, cb = 1300, 1380, G, 740
    yk = lambda ka: round(ct + (cb - ct) * ka / 31, 1)
    els += [box(c0, ct, c1 - c0, cb - ct, "#1a1511", BONE, 2, 4, 2.4, fx="fill", dur=1.0)] + \
           [box(c0 + 2, yk(30 - k), c1 - c0 - 4, round((cb - ct) / 31 + .5, 1), "#6b5640" if k % 2 else "#87705a", r=0, at=round(3.4 + .05 * k, 2)) for k in range(31)] + \
           [lab(c1 + 18, ct + 24, "today", 3.0, DIM, 26, "start"), lab(c1 + 18, cb - 4, "31,000 years", 5.4, AU, 30, "start"),
            lab(c0 - 16, ct + 28, "core", 2.6, BONE, 26, "end")]
    y12 = yk(12.8)
    els += [box(c0 - 4, y12 - 3, c1 - c0 + 8, 6, LILAC, r=2, at=7.2), glow((c0 + c1) / 2, y12, 60, 7.2, .8, "scan"), lab(c1 + 18, y12 + 9, "thin layer", 7.6, LILAC, 28, "start"),
            line([[XC - half(G + (BOT - G) * .41) + 4, G + (BOT - G) * .41], [XC + half(G + (BOT - G) * .41) - 4, G + (BOT - G) * .41]], 7.4, LILAC, 2, "inferred", .8)]
    crater = [[XC - RX - 40, G - 6], [XC - RX + 60, G + 150], [XC - 140, G + 330], [XC, G + 380], [XC + 140, G + 330], [XC + RX - 60, G + 150], [XC + RX + 40, G - 6]]
    els += [line(crater, 10.0, LILAC, 3, "claimed", .9, True), lab(XC - RX - 60, G + 60, "crater?", 10.2, LILAC, 28, "end"),
            strike(XC - 220, G + 330, XC + 220, G + 60, 11.0)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


# ================================================================ chapter 4 · Who turned the tap?
def belt():
    """28 · the Atlantic as a conveyor belt (s40, s41; the Short 'sky-fell', wide): warm, salty water north along the surface, cooling,
    sinking, a deep return south, more warmth pulled along; then fresh meltwater spreads on top like a lid, the sinking stops, the belt
    slows, the north turns cold."""
    S0, F0, XN = 330, 740, 1460
    sea = poly([[90, S0], [XN, S0], [XN, F0], [90, F0]], "#1d3a4a", "#5fa8c9", 2, -1)
    north = [poly([[XN - 4, F0], [XN - 4, S0 + 30], [XN + 20, S0 - 4], [XN + 70, S0 - 30], [1800, S0 - 40], [1800, F0 + 60], [XN - 4, F0 + 60]], "#4a3b2e", "#8c7152", 2, -1),
             poly([[XN + 50, S0 - 22], [XN + 80, S0 - 80], [XN + 130, S0 - 118], [XN + 200, S0 - 138], [1800, S0 - 146], [1800, S0 - 38]], ICE, "#ffffff", 2, -1)]
    loop = [[160, 360], [1380, 360], [1410, 700], [170, 712]]
    lid = [box(x0, S0 - 4, 96, 26, "rgba(191,230,245,.9)", r=3, at=round(12.6 + .18 * k, 2)) for k, x0 in enumerate(range(XN - 100, 760, -96))]
    snow = [g for k, (x, y) in enumerate(((1250, 170), (1380, 230), (1500, 150), (1180, 260), (1600, 240), (1330, 130))) for g in flake(x, y, 14, round(19.0 + .12 * k, 2))]
    els = [sea, line([[90, S0], [XN, S0]], -1, "#9fd0ff", 2, draw=False)] + north + \
          [lab(110, S0 - 18, "south", .2, BONE, 26, "start"), lab(1700, S0 - 170, "north", .2, BONE, 26, "end"),
           glow(220, 180, 120, .2, .9, "sun"), dot(220, 180, 24, "#ffe2b4", .2)] + wave(1330, 230, .3, .9) + [lab(1330, 290, "meltwater", .6, BLUE, 26)] + \
          [line(loop + [loop[0]], 1.6, BONE, 2, "inferred", 1.4, True, op=.35),
           arrow([[160, 366], [600, 360], [1000, 360], [1370, 372]], 4.0, WARM, 7, dur=1.8), lab(420, S0 - 22, "warm, salty", 4.6, WARM, 30),
           glow(1400, 410, 90, 6.6, .9, "scan"),
           arrow([[1408, 400], [1428, 540], [1420, 690]], 8.0, BLUE, 7, dur=1.0), lab(1380, 470, "sinks", 8.4, BLUE, 30, "end"),
           arrow([[1380, 716], [800, 726], [200, 712]], 9.0, BLUE, 6, dur=1.4),
           arrow([[150, 690], [130, 520], [150, 390]], 10.0, WARM, 4, "inferred", .9),
           arrow([[180, 392], [420, 384], [700, 388]], 10.6, WARM, 3.5, dur=.9)] + \
          [arrow([[XN + 40, S0 - 40], [XN - 10, S0 - 14], [XN - 80, S0 + 2]], 12.2, "#cfe6ff", 4, dur=.5)] + lid + \
          [lab(1060, S0 - 24, "fresh meltwater", 13.8, "#bfe6f5", 30),
           box(92, S0 + 24, XN - 94, F0 - S0 - 26, "#14242d", r=0, at=17.4, dur=1.0, op=.6),
           strike(1380, 600, 1460, 500, 17.0), strike(1380, 500, 1460, 600, 17.2),
           glow(1350, 220, 220, 18.8, .6, "scan")] + snow
    return {"base": "dark", "stars": 60, "cam": [1, 889, 500], "els": els}


AGASSIZ = [(-100, 50.8), (-98, 52.2), (-95.5, 51.8), (-94.2, 50.2), (-94.8, 48.6), (-96.2, 47.0), (-97.2, 46.2), (-98.0, 47.5), (-99.2, 49.0)]
MISS = [(-96.6, 45.9), (-95, 45.1), (-93.2, 44.9), (-91.3, 43.4), (-90.6, 41.5), (-90.2, 38.7), (-89.3, 36.5), (-90.9, 33.5), (-91.2, 31.0), (-90.0, 29.4)]
STL_LAND = [(-94.4, 49.3), (-90.5, 48.6), (-87, 47.6), (-84.5, 46.6), (-82, 45.6), (-79.5, 46.1), (-76.5, 45.6), (-73.6, 45.5), (-71.2, 46.8)]
STL_SEA = [(-71.2, 46.8), (-68.5, 48.5), (-64.5, 49.6), (-60, 47.8), (-54, 46.2)]
V_AG = View(-118, -48, 24, 62, (90, 120, 1600, 680))


def agassiz():
    """29 · 1989, the meltwater idea (s42): North America with the ice sheet at about 12,900 years ago (schematic); Lake Agassiz along its
    edge (schematic outline); its outlet south down the Mississippi fades; a new one runs east through the Great Lakes and the St
    Lawrence into the North Atlantic."""
    v = V_AG
    pp = lambda q: [list(v.p(*p_)) for p_ in q]
    els = [{"k": "map", "land": v.land(), "in": -1},
           poly(pp(ICE13), "rgba(235,245,255,.45)", "#ffffff", 1.6, -1), poly(pp(CORD13), "rgba(235,245,255,.4)", "#ffffff", 1.4, -1, True),
           lab(170, 190, "1989", .4, AU, 46, "start", st="serif"),
           poly(pp(AGASSIZ), "rgba(95,168,201,.85)", "#cfe6ff", 2, 4.2, True, fx="pop"), lab(v.p(-100.5, 49)[0] - 16, v.p(-100.5, 49)[1] + 8, "Lake Agassiz", 4.6, "#cfe6ff", 30, "end"),
           lab(*v.p(-92, 59.5), "ice sheet", 7.0, "#e6eef6", 32, st="ital"),
           arrow(pp(MISS), 9.4, "#6fb6d6", 5, dur=1.2), lab(v.p(-91.5, 35)[0] - 18, v.p(-91.5, 35)[1], "Mississippi", 9.8, "#9fd0ff", 28, "end"),
           line(pp(MISS), 10.8, "#3a2f24", 9, draw=False, op=.72),
           line(pp(STL_LAND), 10.6, "#6fb6d6", 5, dur=1.2), arrow(pp(STL_SEA), 11.7, "#6fb6d6", 5, dur=.8),
           lab(v.p(-73, 44.6)[0], v.p(-73, 44.6)[1] + 22, "St Lawrence", 11.2, "#9fd0ff", 28),
           glow(*v.p(-54, 46.2), 70, 13.0, .9, "scan"), lab(*v.p(-50, 41.5), "North Atlantic", 13.0, "#9fd0ff", 30, st="ital")]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def agassiz_gap():
    """(beat 11, back on the map) 2010: the St Lawrence route turns dashed; a magnifier along it finds no flood channel at the right time
    and place; a question mark at its mouth."""
    v = V_AG
    pp = lambda q: [list(v.p(*p_)) for p_ in q]
    mx, my = v.p(-80, 46)
    cx, cy, R = mx + 60, 620, 110
    return [line(pp(STL_LAND), 1.4, "#3a2f24", 11, draw=False), line(pp(STL_SEA)[:-1] + [list(v.p(-55, 46.4))], 1.4, "#172f3d", 11, draw=False),
            line(pp(STL_LAND + STL_SEA[1:]), 1.8, "#6fb6d6", 4, "inferred", 1.0)] + mag(cx, cy, R, 6.2, "#1b1612", -1, 1.2) + \
           [line([[mx, my + 8], [cx, cy - R]], 6.3, BONE, 1.5, "inferred", .4),
            poly([[cx - 104, cy + 10], [cx - 40, cy + 6], [cx, cy + 14], [cx + 40, cy + 6], [cx + 104, cy + 10]] +
                 [[round(cx + (R - 6) * math.cos(math.radians(a)), 1), round(cy + (R - 6) * math.sin(math.radians(a)), 1)] for a in range(6, 175, 8)],
                 "#5f4c39", "#c9ad85", 2, 6.6), line([[cx - 88, cy + 34], [cx + 88, cy + 34]], 6.7, "#8a6a4a", 2, draw=False),
            line([[cx - 72, cy + 60], [cx + 72, cy + 60]], 6.7, "#8a6a4a", 2, draw=False),
            lab(cx, cy - 26, "?", 7.0, BONE, 54, st="big", fx="pop"),
            lab(cx, cy + R + 40, "no clear trace", 7.4, BONE, 30)] + question(*v.p(-57, 48.5), 9.0, 70)


def kennett():
    """30 · one of his co-authors (s43): two papers side by side, 1989 (meltwater) and 2007 (comet); a gold thread links the name Kennett
    on the 1989 author list to the 2007 paper."""
    def paper(cx, deg, title, at, icon):
        authors = [ink(cx - 170 + 125 * (j // 3), 260 + 32 * (j % 3), nm, -1, "#6a5a48", 24, "start") for j, nm in enumerate(icon["names"])]
        return sheet(cx, 440, 420, 560, deg, at, title, 6, extra=authors + icon["els"], ly0=372)
    p89 = paper(560, -3, "1989", .2, {"names": ["Broecker", "Kennett", "Flower", "Teller", "Trumbore", "Bonani", "Wolfli"], "els": wave(560, 620, -1, 1.1)})
    p07 = paper(1220, 3, "2007", 4.0, {"names": ["Firestone", "West", "Kennett", "Becker", "Bunch", "Revay", "..."], "els": comet(1200, 620, -1, ang=-35, L=80)})
    def hl(cx, deg, j, at):
        x, y = cx - 170 + 125 * (j // 3), 260 + 32 * (j % 3)
        return {"k": "group", "tr": "rotate(%s %s %s)" % (deg, cx, 440), "in": at,
                "els": [box(x - 8, y - 23, 116, 32, "rgba(232,195,90,.35)", AU, 2, 4, -1), ink(x, y, "Kennett", -1, "#2a1d10", 24, "start")]}
    a = rot([[560 - 170 - 14, 284]], 560, 440, -3)[0]
    b = rot([[1220 - 170 - 14, 316]], 1220, 440, 3)[0]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": [p89, p07, hl(560, -3, 1, 2.2), hl(1220, 3, 2, 4.6),
            glow(a[0], a[1], 70, 2.2, .7, "lamp"),
            line([a, [a[0] - 14, 200], [a[0] + 40, 120], [b[0] - 40, 120], [b[0] - 14, 220], b], 4.6, AU, 3.5, curve=True, dur=1.2), glow(b[0], b[1], 70, 5.6, .7, "lamp"),
            lab(560, 770, "meltwater", .6, BLUE, 28), lab(1220, 770, "comet", 4.4, LILAC, 28)]}


def plumbing():
    """31 · the shared plumbing (s44): the ice sheet as a tank, a pipe, a tap, the Atlantic basin and its belt; the comet camp on one side,
    a dotted comet pointing at the tap; the meltwater camp on the other, a blue melting arrow; both argue about who turned the tap."""
    els = [box(120, 160, 380, 200, "#cfe0ec", "#ffffff", 2, 14, .2, fx="rise"),
           poly([[130, 168], [200, 120], [310, 100], [420, 112], [490, 168]], ICE, "#ffffff", 2, .3, True),
           ink(310, 280, "ice sheet", .4, "#2c3e4e", 30),
           line([[500, 330], [880, 330]], .5, "#8a8378", 18, dur=.5), line([[500, 330], [880, 330]], .6, "#b9b2a6", 6, draw=False),
           line([[889, 330], [889, 400]], .7, "#8a8378", 16, draw=False),
           {"k": "circle", "x": 889, "y": 330, "r": 28, "fill": "#2a2622", "c": AU, "w": 4, "in": .8, "fx": "pop"},
           line([[869, 330], [909, 330]], .9, AU, 4, draw=False), line([[889, 310], [889, 350]], .9, AU, 4, draw=False),
           poly([[560, 560], [1500, 560], [1460, 760], [600, 760]], "#1d3a4a", "#5fa8c9", 2, 1.0),
           poly(rell(1030, 670, 330, 46, 0, 40), "none", "#9fd0ff", 2, 1.4, True, style="inferred"),
           arrow([[760, 626], [940, 622], [1120, 624]], 1.6, WARM, 3, dur=.6), arrow([[1300, 714], [1100, 718], [900, 716]], 1.9, BLUE, 3, dur=.6),
           lab(1300, 618, "Atlantic", 2.0, "#9fd0ff", 28, st="ital"),
           line([[150, 562], [350, 562]], -1, "#8c7152", 3, draw=False), line([[1510, 562], [1720, 562]], -1, "#8c7152", 3, draw=False),
           line([[889, 404], [889, 556]], 3.6, "#6fb6d6", 8, dur=.6)] + \
          [dot(889 + (k % 2) * 12 - 6, 430 + 34 * k, 5, "#9fd0ff", round(3.8 + .1 * k, 2)) for k in range(4)] + \
          comet(1660, 150, 2.8, ang=-30, L=70) + [arrow([[1640, 168], [1300, 220], [918, 312]], 3.0, LILAC, 3, "claimed", .9)] + \
          [arrow([[420, 470], [640, 440], [866, 348]], 9.4, BLUE, 4, dur=.8)] + wave(360, 450, 9.2, .8) + \
          [person(x, 560, 84, round(6.6 + .15 * k, 2), "#c9c1ee") for k, x in enumerate((1560, 1610, 1660))] + \
          [person(x, 560, 84, round(6.9 + .15 * k, 2), "#9fd0ff") for k, x in enumerate((200, 250, 300))] + \
          [lab(1610, 430, "comet camp", 7.4, LILAC, 28), lab(250, 640, "meltwater camp", 7.6, BLUE, 28),
           glow(889, 330, 100, 10.6, .8, "lamp"), lab(889, 276, "the tap", 10.6, AU, 32)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def mackenzie():
    """32 · 2018, the Mackenzie (s46): the map widens north; from Lake Agassiz an arrow runs north-west down the Mackenzie River to the
    Arctic Ocean; a core on the seabed off its mouth; the flood lasted about 700 years, from 12,940 +/- 150 years ago, beside the cold's
    onset in Greenland at 12,850 +/- 140: the two bars overlap."""
    v = View(-150, -55, 40, 76, (90, 120, 940, 660))
    pp = lambda q: [list(v.p(*p_)) for p_ in q]
    route = [(-98, 50.5), (-104, 54.2), (-110, 56.8), (-111, 58.6), (-113.5, 61.0), (-117.5, 61.6), (-121.3, 62.0), (-125.5, 64.6), (-128.6, 66.3), (-133.5, 68.3), (-135, 69.6)]
    w = round(v.p(-55, 60)[0] - v.ox + 16, 1)
    els = [{"k": "group", "clip": [v.ox - 8, 118, w, 664, 12], "bg": "#16303d", "in": -1,
            "els": [{"k": "map", "land": v.land()}, poly(pp(ICE13), "rgba(235,245,255,.45)", "#ffffff", 1.6, -1),
                    poly(pp(AGASSIZ), "rgba(95,168,201,.85)", "#cfe6ff", 2, -1, True)]},
           {"k": "rect", "x": v.ox - 8, "y": 118, "w": w, "h": 664, "r": 12, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": -1}]
    cx_, cy_ = v.p(-136.5, 71.0)
    els += [lab(1080, 210, "2018", .9, AU, 44, "start", st="serif"), box(cx_ - 7, cy_ - 22, 14, 44, "#87705a", BONE, 2, 3, 2.0, fx="rise"), glow(cx_, cy_, 50, 2.2, .8, "lamp"),
            lab(*v.p(-140, 74.2), "Arctic Ocean", 3.0, "#9fd0ff", 28, st="ital"),
            arrow(pp(route), 5.4, "#6fb6d6", 5, dur=1.8), lab(v.p(-127, 62.5)[0] - 14, v.p(-127, 62.5)[1] + 10, "Mackenzie River", 6.6, "#9fd0ff", 28, "end"),
            lab(v.p(-99, 48.6)[0], v.p(-99, 48.6)[1] + 30, "Lake Agassiz", 5.0, "#cfe6ff", 24)]
    XK = lambda ya: round(1080 + (13300 - ya) * .5, 1)
    yB, yC, yX = 360, 500, 600
    els += [{"k": "axis", "x0": 1080, "x1": 1680, "y": yX, "ticks": [[XK(13000), "13,000"], [XK(12500), "12,500"]], "in": 7.4},
            lab(1680, yX + 92, "years ago", 7.5, DIM, 24, "end")]
    n = 8
    els += [box(round(XK(12940 - 700 * k / n), 1), yB - 10, round(700 / n * .5 + .5, 1), 20, "rgba(111,182,214,.75)", r=0, at=round(7.6 + .12 * k, 2), dur=.2) for k in range(n)] + \
           [lab((XK(12940) + XK(12240)) / 2, yB - 30, "flood, about 700 years", 8.4, "#9fd0ff", 28),
            box(XK(12850), yC - 10, XK(12100) - XK(12850), 20, "rgba(230,239,246,.45)", r=0, at=10.4, fx="fill", dur=.4),
            lab((XK(12850) + XK(12100)) / 2, yC - 30, "the cold", 10.6, ICE, 28)]
    def bar(c, ya, pm, y, at):
        return [line([[XK(ya + pm), y], [XK(ya - pm), y]], at, c, 4, dur=.5), line([[XK(ya + pm), y - 16], [XK(ya + pm), y + 16]], at, c, 3, draw=False),
                line([[XK(ya - pm), y - 16], [XK(ya - pm), y + 16]], at + .2, c, 3, draw=False), dot(XK(ya), y, 8, c, at + .2)]
    els += bar(AU, 12940, 150, yB, 10.0) + bar(AU, 12850, 140, yC, 10.6) + [lab(XK(13110), (yB + yC) / 2 + 8, "margins", 10.2, AU, 26, "end")]
    o0, o1 = XK(12990), XK(12790)
    els += [box(o0, yB - 22, o1 - o0, yC - yB + 44, "rgba(232,195,90,.18)", AU, 2, 6, 12.8, style="inferred"), glow((o0 + o1) / 2, (yB + yC) / 2, 100, 13.0, .6, "lamp"),
            lab((o0 + o1) / 2, yC + 56, "overlap", 13.0, AU, 26)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def recount():
    """33 · 2025, the platinum re-read (s47, s48): the Greenland core with year ticks finer near the onset; a decade line: the cooling
    begins at year 0, 45 yearly dots tick by, the platinum runs from year 45 to 59; Iceland, a glowing fissure, a plume drifting
    towards Greenland; a new reading, still being tested; the bang at year 0, and a dotted arrow back from the platinum to it, struck."""
    c0, c1, ct, cb, yo = 130, 210, 150, 760, 470
    r = random.Random(47)
    els = [box(c0, ct, c1 - c0, cb - ct, "#cfe0ec", "#ffffff", 2, 8, .3, fx="rise")] + \
          [line([[c0 + 3, y], [c1 - 3, y]], .4, "#9fb6c8", round(r.uniform(1, 2.4), 1), draw=False) for y in range(ct + 10, cb, 10)] + \
          [lab(c1 + 16, ct + 24, "Greenland ice", .6, ICE, 26, "start"), box(c0 - 4, yo - 6, c1 - c0 + 8, 12, BLUE, r=3, at=4.4),
           lab(1080, 230, "2025", 2.2, AU, 44, st="serif")]
    ticks, y, d = [], yo, 26.0
    for k in range(9):
        ticks += [line([[c1 + 6, round(yo - d * k * (1 + .12 * k), 1)], [c1 + 26, round(yo - d * k * (1 + .12 * k), 1)]], round(5.6 + .06 * k, 2), BONE, 2, draw=False),
                  line([[c1 + 6, round(yo + d * k * (1 + .12 * k), 1)], [c1 + 26, round(yo + d * k * (1 + .12 * k), 1)]], round(5.6 + .06 * k, 2), BONE, 2, draw=False)]
    els += [t for t in ticks if ct + 6 < t["p"][0][1] < cb - 6]
    XT = lambda t: round(400 + (t + 10) * 9.4, 1)
    yl = 520
    els += [line([[XT(-10), yl], [XT(72), yl]], 7.0, "#e9dccb", 2.5, dur=.6), line([[c1 + 30, yo], [XT(-10) - 10, yl]], 7.0, BLUE, 1.5, "inferred", .6),
            line([[XT(0), 400], [XT(0), yl + 18]], 7.6, BLUE, 4, dur=.4), lab(XT(0), 384, "cooling begins", 7.8, BLUE, 26)]
    els += [dot(XT(t), yl - 14, 3.2, BONE, round(8.6 + .04 * t, 2)) for t in range(1, 46)] + \
           [line([[XT(0), yl + 40], [XT(45), yl + 40]], 10.0, BONE, 2, dur=.4), lab((XT(0) + XT(45)) / 2, yl + 76, "45 years", 10.2, BONE, 28)]
    els += [box(round(XT(45 + 14 * k / 7), 1), yl - 30, round(14 / 7 * 9.4 + .5, 1), 26, AU, r=0, at=round(11.8 + .12 * k, 2), dur=.2) for k in range(7)] + \
           [lab((XT(45) + XT(59)) / 2, yl - 44, "platinum", 12.2, AU, 28), lab((XT(45) + XT(59)) / 2, yl + 76, "14 years", 12.6, AU, 28)]
    v = View(-50, -8, 58.5, 71.5, (1250, 140, 430, 400))
    w = round(v.p(-6, 65)[0] - v.ox + 20, 1)
    fis = pp_ = [list(v.p(*q)) for q in ((-19.1, 63.75), (-18.5, 64.05), (-17.9, 64.35))]
    els += [{"k": "group", "clip": [v.ox - 10, 136, w, 428, 12], "bg": "#16303d", "in": 13.8, "els": [{"k": "map", "land": v.land()}]},
            {"k": "rect", "x": v.ox - 10, "y": 136, "w": w, "h": 428, "r": 12, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": 13.8},
            lab(*v.p(-42, 66.5), "Greenland", 14.2, ICE, 26, st="ital"),
            glow(fis[1][0], fis[1][1], 70, 15.8, 1, "fire"), line(fis, 15.8, "#ff9a4a", 5, dur=.5), lab(fis[2][0] + 18, fis[2][1] + 40, "Iceland", 16.2, BONE, 28, "start")] + \
           [{"k": "circle", "x": round(fis[1][0] - 50 * k, 1), "y": round(fis[1][1] - 20 * k, 1), "r": 22 + 8 * k, "fill": "rgba(160,150,140,.35)", "c": "none", "w": 0,
             "in": round(16.4 + .3 * k, 2)} for k in range(4)] + \
           [box(XT(-12), 360, XT(72) - XT(-12), 270, "none", BONE, 2, 12, 20.0, style="inferred"), lab(XT(30), 344, "new, still being tested", 20.4, BONE, 26)]
    bx_, by_ = XT(0), yl - 66
    els += [glow(bx_, by_, 60, 23.2, .9, "red")] + [line([[bx_, by_], [round(bx_ + 26 * math.cos(math.radians(a)), 1), round(by_ + 26 * math.sin(math.radians(a)), 1)]], 23.2, "#ffd0a0", 3, dur=.2)
                                                    for a in range(0, 360, 45)] + \
           [lab(bx_ - 40, by_ + 6, "the bang", 23.4, "#ffb09a", 26, "end"),
            arrow([[XT(52), yl - 34], [XT(26), yl - 120], [bx_ + 30, by_ - 10]], 23.8, LILAC, 3, "claimed", .8), strike(XT(26) - 30, yl - 150, XT(26) + 30, yl - 90, 24.8)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


# ================================================================ chapter 5 · The first farmers
def glass():
    """34 · back to Abu Hureyra's glass (s50): four Syrian sites on the map (schematic); a time line from 13,000 to 10,000 years ago with
    their glassy droplets spread across it; a mud-brick house with a straw roof burns, and glassy droplets form in its ash."""
    v = View(37.3, 40.1, 35.25, 36.75, (100, 140, 640, 440))
    w = round(v.p(40.1, 36)[0] - v.ox + 20, 1)
    pp = lambda q: [list(v.p(*p_)) for p_ in q]
    els = [{"k": "group", "clip": [v.ox - 10, 130, w, 460, 12], "bg": "#16303d", "in": -1,
            "els": [{"k": "map", "land": v.land()}, line(pp(EUPHRATES), -1, "#6fb6d6", 5, curve=True, draw=False),
                    poly(pp(ASSAD), "rgba(63,134,176,.92)", "#cfe6ff", 2, -1, True)]},
           {"k": "rect", "x": v.ox - 10, "y": 130, "w": w, "h": 460, "r": 12, "fill": "none", "c": "rgba(255,236,206,.3)", "sw": 2, "in": -1},
           lab(*v.p(38.9, 35.55), "Euphrates", -1, "#9fd0ff", 24, st="ital")]
    for k, q in enumerate(((38.40, 35.866), (38.12, 36.05), (38.24, 36.32), (38.66, 35.97))):
        x, y = v.p(*q)
        els += [glow(x, y, 30, round(2.6 + .2 * k, 2), .9, "lamp"), dot(x, y, 8, AU, round(2.6 + .2 * k, 2))]
    els += [lab(*v.p(38.4, 35.62), "Abu Hureyra", -1, AU, 26), lab(v.ox + 20, 176, "4 sites", 3.4, AU, 30, "start")]
    XG = lambda ya: round(900 + (13000 - ya) * .25, 1)
    els += [{"k": "axis", "x0": 900, "x1": 1650, "y": 300, "ticks": [[XG(y), "{:,}".format(y)] for y in (13000, 12000, 11000, 10000)], "in": 3.8},
            lab(1650, 380, "years ago", 3.9, DIM, 24, "end")]
    for k, ya in enumerate((12950, 12100, 11100, 10150)):
        x = XG(ya)
        els += [poly(rell(x, 262, 10, 14, 0, 14), "#1d3a32", "#9fd0c0", 1.5, round(4.1 + .3 * k, 2), True, fx="pop")]
    els += [line([[XG(13000), 214], [XG(10000), 214]], 5.2, AU, 2.5, dur=.6), line([[XG(13000), 204], [XG(13000), 224]], 5.2, AU, 2.5, draw=False),
            line([[XG(10000), 204], [XG(10000), 224]], 5.4, AU, 2.5, draw=False), lab((XG(13000) + XG(10000)) / 2, 196, "3,000 years", 5.4, AU, 28)]
    items = [{"t": "slab", "x0": -9, "x1": 9, "z0": -7, "z1": 7, "y": 0, "c": "#5f4c39"},
             {"t": "box", "x": 0, "z": 0, "y": 0, "w": 8, "d": 6, "h": 3.2, "c": "#a8845c", "edge": "rgba(40,30,20,.5)"},
             {"t": "pyr", "x": 0, "z": 0, "y": 3.2, "b": 8.8, "h": 3.6, "c": "#cdb35a"}]
    els += [{"k": "iso", "x": 1260, "y": 640, "s": 20, "az": -30, "spin": 0, "el": .4, "items": items, "in": 6.2, "fx": "rise"},
            glow(1260, 560, 160, 7.2, 1, "fire"), glow(1210, 600, 90, 7.4, .9, "fire"), glow(1320, 590, 90, 7.6, .9, "fire")] + \
           [poly(rell(x, y, 8, 6, 20, 12), "#1d3a32", "#9fd0c0", 1.2, round(8.4 + .1 * k, 2), True, fx="pop")
            for k, (x, y) in enumerate(((1150, 690), (1200, 706), (1262, 712), (1330, 704), (1384, 690), (1290, 724)))] + \
           [lab(1450, 520, "house fire", 8.0, "#ffb07a", 30, "start")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def thermos():
    """35 · still argued (s51): two thermometers, a house fire (part-filled, no number) and the comet team's glass, filling past 2,200 C;
    a balance between them wobbles and settles level."""
    els = [lab(1220, 150, "comet team", .4, LILAC, 30)] + thermo_glyph(1220, 190, 610, .93, .5, "#ff8a5a", .6, 3.0) + \
          [line([[1196, 610 - 420 * .88], [1244, 610 - 420 * .88]], 3.4, AU, 3, draw=False), lab(1262, 610 - 420 * .88 + 10, "over 2,200 °C", 3.6, AU, 30, "start"),
           glow(1220, 230, 90, 3.6, .7, "fire"),
           lab(560, 150, "house fire", 4.4, "#ffb07a", 30)] + thermo_glyph(560, 190, 610, .55, 4.4, "#ff8a5a", 4.6, 1.0)
    pv, L_ = (889, 420), 170
    def beam(deg, at, style="known", op=None):
        a = math.radians(deg)
        p0 = [round(pv[0] - L_ * math.cos(a), 1), round(pv[1] - L_ * math.sin(a), 1)]
        p1 = [round(pv[0] + L_ * math.cos(a), 1), round(pv[1] + L_ * math.sin(a), 1)]
        e = [line([p0, p1], at, BONE, 5, style, draw=False)]
        for q in (p0, p1):
            e += [line([q, [q[0] - 34, q[1] + 70]], at, BONE, 2, style, draw=False), line([q, [q[0] + 34, q[1] + 70]], at, BONE, 2, style, draw=False),
                  line([[q[0] - 44, q[1] + 70], [q[0] + 44, q[1] + 70]], at, BONE, 4, style, draw=False)]
        if op is not None:
            for x in e:
                x.update(op=op, keepop=True)
        return e
    els += [line([[889, 640], [889, 420]], 6.2, BONE, 6, draw=False), line([[840, 640], [938, 640]], 6.2, BONE, 6, draw=False), dot(889, 420, 9, AU, 6.2)] + \
           beam(-10, 6.4, "inferred", .45) + beam(8, 6.8, "inferred", .45) + beam(0, 7.2) + [lab(889, 720, "still argued", 7.6, BONE, 30)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def village2():
    """36 · why the village matters (s52): the village again, round half-sunken huts on the terrace above the Euphrates, people gathering
    among wild cereals; as the cold sets in the sky greys, the woodland edge pulls back tree by tree, the stalks thin."""
    G = 600
    haze = {"k": "poly", "p": P([[-20, SKYBOX[0]], [-20, 440], [1800, 440], [1800, SKYBOX[1]], [1800, G], [-20, G]]), "fill": "url(#k-sky-dusk)", "c": "none", "w": 0, "in": -1}
    hy = lambda x: round(G - 50 - (x - 760) / 1040 * 70, 1) if x > 760 else G - 50
    hill_pts = [[620, G], [700, G - 40], [760, G - 50]] + [[x, hy(x)] for x in range(900, 1801, 150)] + [[1800, G]]
    hill = poly(hill_pts, "#2e2a24", "none", 0, -1)
    trees, erasers = [], []
    for k, x in enumerate(range(830, 1760, 62)):
        y0 = hy(x) + 4; rr = 30 + 6 * (k % 3)
        trees += [line([[x, y0], [x, y0 - 42]], -1, "#2a221c", 6, draw=False), {"k": "circle", "x": x, "y": round(y0 - 42 - rr * .7, 1), "r": rr, "fill": "#3f4a2c", "c": "none", "w": 0, "in": -1}]
        if k < 7:                             # the woodland edge pulls back: the nearest seven trees go, one by one (sky painted back over them)
            xl, xr, top = x - rr - 6, x + rr + 6, round(y0 - 42 - rr * 1.7 - 6, 1)
            erasers.append({"k": "poly", "p": P([[xl, SKYBOX[0]], [xl, top], [xr, top], [xr, SKYBOX[1]], [xr, y0 - 1], [xl, y0 - 1]]), "fill": "url(#k-sky-dusk)",
                            "c": "none", "w": 0, "curve": False, "in": round(9.6 + .26 * k, 2), "dur": .6})
    hill2 = poly(hill_pts, "#2e2a24", "none", 0, -1)
    TERR = "#3a3226"
    field = poly([[60, G], [110, G - 132], [700, G - 140], [760, G]], TERR, "none", 0, -1)
    r = random.Random(52)
    stalks, cuts = [], []
    for k in range(52):
        x = round(130 + 11.5 * k + r.uniform(-4, 4), 1); h = r.uniform(70, 96)
        stalks += [line([[x, G], [x + 3, G - h]], -1, "#c9b27a", 2.2, draw=False), poly(rell(x + 4, G - h - 9, 4, 11, 10, 10), "#e3cf94", "none", 0, -1, True)]
        if k % 2:
            at = round(12.2 + .03 * k, 2)
            cuts += [line([[x, G - 3], [x + 3, G - h]], at, TERR, 6, draw=False), poly(rell(x + 4, G - h - 9, 7, 14, 10, 10), TERR, "none", 0, at, True)]
    huts = []
    for k, x in enumerate((210, 380, 550)):
        huts += [poly([[x - 74 + 148 * j / 20, G - 52 * math.sin(math.pi * j / 20)] for j in range(21)], "#8a6a4a", "#d9b48a", 1.5, -1, True),
                 box(x - 10, G - 30, 20, 30, "#2a1d12", r=8, at=-1)]
    river = [poly([[-20, G], [1800, G], [1800, G + 70], [-20, G + 70]], "#5f4c39", "none", 0, -1), poly([[-20, G + 70], [1800, G + 70], [1800, G + 140], [-20, G + 140]], "#3f86a8", "#9fd0ff", 1.5, -1)]
    sky_grey = poly([[-20, -20], [1800, -20], [1800, G], [-20, G]], "#5d6470", "none", 0, 8.0, dur=1.6, op=.42, keepop=True)
    people = [person(x, G, 96, round(3.6 + .2 * k, 2), "#f0dcc0") for k, x in enumerate((290, 470, 640))]
    els = [haze, hill] + trees + erasers + [hill2, field] + river + stalks + cuts + [sky_grey] + huts + people + [
        lab(420, 440, "wild cereals", 5.8, "#e3cf94", 30),
        lab(1330, 420, "woodland", 1.0, "#9fb07a", 28),
        line([[826, G - 40], [826, 400]], 11.4, "#9fb07a", 2.5, "inferred", .5), lab(838, 386, "woodland retreats", 11.6, "#9fb07a", 28, "start"),
        lab(889, 716, "Euphrates", .6, "#cfe6ff", 26, st="ital")]
    return {"base": "sky", "tod": "dusk", "ground": G, "groundc": "#3b3128", "sun": [1500, 330, 16], "ridges": [], "cam": [1, 889, 500], "els": els}


def seeds():
    """37 · the seeds (s53): a tray of charred seeds under a lamp; rye grains glow gold and a small dotted field with two people tilling
    appears (the cultivation reading); then the tray fans out into many kinds of seed (the broader diet)."""
    r = random.Random(53)
    tray = [glow(490, 470, 260, .3, .45, "lamp"), box(220, 430, 540, 170, "#5a4128", "#a8845c", 3, 18, .3, fx="rise")]
    sd = []
    rye = []
    for k in range(44):
        x, y = round(r.uniform(250, 730), 1), round(r.uniform(455, 575), 1)
        a = r.uniform(0, 180)
        sd.append(poly(rell(x, y, 9, 4.5, a, 10), "#1b1410", "#4a3a2a", 1, round(.6 + .02 * k, 2), True))
        if k % 4 == 0:
            rye.append(poly(rell(x, y, 10, 5, a, 10), AU, "#fff1b8", 1, round(4.2 + .03 * k, 2), True))
            rye.append(glow(x, y, 20, round(4.2 + .03 * k, 2), .6, "lamp"))
    field = [line([[1000 + 30 * j, 330], [1080 + 30 * j, 220]], round(5.6 + .05 * j, 2), "#c9b27a", 2.5, "inferred", .4) for j in range(16)] + \
            [person(1180, 330, 80, 6.0, "#f0dcc0"), line([[1196, 284], [1236, 330]], 6.1, "#c9a370", 4, draw=False),
             person(1420, 330, 80, 6.3, "#f0dcc0"), line([[1436, 284], [1476, 330]], 6.4, "#c9a370", 4, draw=False),
             lab(1300, 190, "first farming?", 6.6, AU, 28)]
    kinds = [("#8a6a3a", 10, 5), ("#5a4a2a", 7, 7), ("#a07a4a", 12, 4), ("#6f7a4a", 6, 6), ("#b89a6a", 9, 6), ("#3a2a1a", 11, 3.5)]
    fan = []
    for k in range(36):
        t = math.radians(200 + 140 * k / 35)
        rr = 170 + 70 * (k % 3)
        x, y = 1300 + rr * math.cos(t) * 1.2, 760 + rr * math.sin(t) * .9
        c, a_, b_ = kinds[k % 6]
        fan.append(poly(rell(round(x, 1), round(y, 1), a_, b_, k * 23, 10), c, "#e9d3ab", 1, round(9.4 + .028 * k, 2), True, fx="pop"))
    els = tray + sd + rye + [lab(490, 650, "rye", 4.6, AU, 32)] + \
          [arrow([[770, 450], [880, 360], [990, 300]], 5.4, AU, 2.5, "inferred", .6)] + field + \
          [arrow([[770, 560], [900, 600], [1040, 610]], 9.2, BONE, 2.5, "inferred", .6)] + fan + [lab(1300, 770, "broader diet", 10.2, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def rebuilt():
    """38 · the comet team's chapter (s54), all drawn dotted (a reading): a flash in the sky; the round huts give way to rectangular houses
    above ground; a few people return; a small field."""
    G = 640
    huts = [poly([[x - 80 + 160 * j / 20, G - 58 * math.sin(math.pi * j / 20)] for j in range(21)], "rgba(201,193,238,.08)", LILAC, 2.5, .4, False, style="claimed")
            for x in (200, 390, 580)]
    houses = [box(x, G - 100, 170, 100, "rgba(201,193,238,.08)", LILAC, 2.5, 2, round(6.0 + .25 * k, 2), style="claimed") for k, x in enumerate((900, 1090, 1280))] + \
             [line([[x - 8, G - 100], [x + 85, G - 150], [x + 178, G - 100]], round(6.1 + .25 * k, 2), LILAC, 2.5, "claimed", .4) for k, x in enumerate((900, 1090, 1280))]
    field = [line([[1490 + 24 * j, G + 6], [1540 + 24 * j, G - 70]], round(7.2 + .05 * j, 2), LILAC, 2, "claimed", .3) for j in range(9)]
    els = [lab(889, 170, "in their reading", 2.4, LILAC, 30)] + huts + \
          [glow(700, 280, 260, 4.6, .8, "red"), glow(700, 280, 100, 4.6, 1, "lamp"), ring(700, 280, 70, 4.7, LILAC, 2.5, "claimed")] + \
          [person(x, G, 100, round(4.0 + .2 * k, 2), "#c9c1ee") for k, x in enumerate((710, 760, 810))] + \
          [arrow([[600, G - 90], [740, G - 170], [890, G - 110]], 5.8, LILAC, 2.5, "claimed", .6)] + houses + field
    return {"base": "sky", "tod": "dusk", "ground": G, "groundc": "#3b3128", "sun": False, "cam": [1, 889, 500], "els": els}


def thermo_c():
    """(beat 16, back on the opening thermometer) for the first farmers what mattered was the cold: a gold ring round it, two dim suspects
    with question marks; when it lifted, about 11,600 years ago a carved T-pillar rises (Gobekli Tepe), a person for scale; about a thousand
    years later, a wheat ear: domesticated cereals."""
    px, wx = X(11400), X(10400)
    wheat = [line([[wx, 690], [wx, 590]], 20.0, "#d9c06a", 3, dur=.4)] + \
            [poly(rell(round(wx + (7 if j % 2 else -7), 1), round(586 - 12 * (j // 2), 1), 5, 9, (25 if j % 2 else -25), 10), "#e3cf94", "none", 0, round(20.2 + .04 * j, 2), True)
             for j in range(10)]
    return [poly(rell((X0 + X1) / 2 + 4, YD_Y + 2, (X1 - X0) / 2 + 24, 60), "none", AU, 4, 2.8, True, fx="draw", dur=.9)] + \
           [dict(e, op=.55, keepop=True) for e in comet(965, 470, 5.8, ang=-40, L=60, r=7, g=50)] + [lab(965, 420, "?", 6.0, LILAC, 40, st="big")] + \
           wave(1095, 490, 6.2, .7, BLUE, op=.6) + [lab(1095, 420, "?", 6.4, BLUE, 40, st="big"),
           glow(X1, 420, 90, 8.2, .7, "lamp"),
           {"k": "tpillar", "x": px, "y": 690, "h": 150, "in": 13.8, "fx": "rise"}, person(px + 70, 690, 54, 14.0, "#e8d6b8"),
           lab(1182, 512, "Göbekli Tepe", 15.6, BONE, 30, "start")] + wheat + [lab(wx + 60, 542, "domesticated cereals", 20.4, "#e3cf94", 28)]


def duskfield():
    """39 · a cold snap may have nudged people towards farming (s57): dusk, a person at the edge of a small field; behind, faint in the sky,
    the cold band of the thermometer; above, the comet and the meltwater, both still with question marks."""
    G = 600
    sc = lambda pts: [[round(300 + (X(a) - 160) * .8, 1), round(150 + (b - 290) * .45, 1)] for a, b in pts]
    rows = [line([[860 + 70 * j, G + 4], [940 + 110 * j, 800]], -1, "#5f4c39", 3, draw=False) for j in range(10)] + \
           [dot(round(880 + 70 * j + (940 + 110 * j - 860 - 70 * j) * u, 1), round(G + 10 + 190 * u, 1), 3, "#8fb46a", -1) for j in range(10) for u in (.15, .35, .55, .75)]
    els = [poly([[840, G], [1800, G], [1800, 820], [940, 820]], "#4a3c2a", "none", 0, -1)] + rows + \
          [line(sc(CA2[-6:] + CB), .3, AMBER, 4, curve=True, draw=False, op=.3), line(sc(CC), .3, BLUE, 4, curve=True, draw=False, op=.35),
           line(sc(CD[:5]), .3, AMBER, 4, curve=True, draw=False, op=.3),
           person(820, G, 100, .6, "#f0dcc0"), line([[838, G - 54], [884, G - 4]], .8, "#c9a370", 4, draw=False)] + \
          comet(640, 170, 3.8, ang=-35, L=80) + [lab(600, 250, "?", 5.0, LILAC, 50, st="big")] + \
          wave(1250, 200, 4.2, .9) + [lab(1330, 214, "?", 5.2, BLUE, 50, st="big")]
    return {"base": "sky", "tod": "dusk", "ground": G, "groundc": "#3b3128", "sun": [1560, 520, 16], "cam": [1, 889, 500], "els": els}


# ================================================================ chapter 6 · The weighing
def journals():
    """40 · 2023 and 2024 (s59): two journal papers face each other on a desk; thirteen authors above the 2023 refutation, one of them lit
    gold beside a tiny platinum spike (the man whose team found it); the 2024 reply answers with an arrow back."""
    els = [poly([[-20, 640], [1800, 640], [1800, 1020], [-20, 1020]], "#2a1f17", "#5a4632", 2, -1)]
    els += [sheet(560, 530, 380, 300, -5, .2, "2023", 4, extra=[ink(560, 470, "a comprehensive refutation", -1, "#5a4632", 24)], ly0=500),
            sheet(1220, 530, 380, 300, 5, 9.8, "2024", 4, extra=[ink(1220, 470, "a reply", -1, "#5a4632", 24)], ly0=500)]
    xs = [404 + 26 * k for k in range(13)]
    els += [person(x, 362, 48, round(1.8 + .06 * k, 2), "#cbbca8") for k, x in enumerate(xs)]
    els += [person(xs[9], 362, 48, 6.4, AU), glow(xs[9], 338, 50, 6.4, .9, "lamp"),
            line([[xs[9] + 16, 284], [xs[9] + 26, 284], [xs[9] + 32, 258], [xs[9] + 38, 284], [xs[9] + 50, 284]], 7.8, AU, 2.5, dur=.3),
            lab(560, 262, "13 authors", 2.6, BONE, 28),
            arrow([[1030, 580], [890, 540], [760, 580]], 11.0, AU, 4, dur=.7), lab(890, 510, "reply", 11.4, AU, 26)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def retract():
    """41 · retractions (s60): three papers, a red strike across each; two of them linked to the thin layer; the authors disagree; a
    retraction is not a refutation, but the flagship evidence keeps failing its checks: a balance tips slowly away from the comet's pan."""
    els = []
    for k, (x, deg) in enumerate(((280, -4), (560, 2), (840, 5))):
        els += [sheet(x, 420, 220, 290, deg, round(.4 + .2 * k, 2), None, 7), strike(x - 100, 540, x + 100, 300, round(2.6 + .3 * k, 2))]
    els += [lab(560, 640, "retracted", 3.4, RED, 32), lab(560, 180, "since 2025", .6, AU, 40, st="serif")]
    els += [box(1110, 200, 300, 160, "#5f4c39", "#8c7152", 2, 8, 6.6), box(1110, 250, 300, 40, "#7a6248", r=0, at=6.6),
            line([[1114, 272], [1406, 272]], 6.8, LILAC, 4, dur=.6), lab(1260, 186, "this very layer", 7.2, LILAC, 28),
            line([[280, 270], [1104, 272]], 7.0, LILAC, 1.5, "inferred", .6), line([[560, 270], [1104, 290]], 7.3, LILAC, 1.5, "inferred", .6)]
    els += [person(x, 760, 60, round(9.8 + .12 * k, 2), "#cbbca8") for k, x in enumerate((180, 220, 260))] + \
           [lab(300, 742, "authors disagree", 10.2, DIM, 26, "start")]
    pv, L_ = (1470, 520), 170
    def beam(deg, at, style="known", op=None):
        a = math.radians(deg)
        p0 = [round(pv[0] - L_ * math.cos(a), 1), round(pv[1] - L_ * math.sin(a), 1)]
        p1 = [round(pv[0] + L_ * math.cos(a), 1), round(pv[1] + L_ * math.sin(a), 1)]
        e = [line([p0, p1], at, BONE, 5, style, draw=False)]
        for q in (p0, p1):
            e += [line([q, [q[0] - 34, q[1] + 64]], at, BONE, 2, style, draw=False), line([q, [q[0] + 34, q[1] + 64]], at, BONE, 2, style, draw=False),
                  line([[q[0] - 44, q[1] + 64], [q[0] + 44, q[1] + 64]], at, BONE, 4, style, draw=False)]
        if op is not None:
            for x in e:
                x.update(op=op, keepop=True)
        return e, p0, p1
    lv, _, _ = beam(0, 14.6, "inferred", .5)
    tl, p0, p1 = beam(12, 16.6)
    els += [line([[pv[0], 740], [pv[0], pv[1]]], 14.4, BONE, 6, draw=False), line([[pv[0] - 50, 740], [pv[0] + 50, 740]], 14.4, BONE, 6, draw=False), dot(pv[0], pv[1], 9, AU, 14.4)] + lv + tl + \
           comet(p0[0], p0[1] + 40, 16.8, ang=-40, L=40, r=6, g=40) + \
           [box(p1[0] - 26, p1[1] + 30, 52, 30, PAPER, "#b8a888", 1.5, 3, 16.8), box(p1[0] - 22, p1[1] + 22, 52, 30, PAPER, "#b8a888", 1.5, 3, 16.9),
            lab(p0[0], p0[1] + 104, "comet", 17.0, LILAC, 26), lab(p1[0], p1[1] + 104, "checks", 17.0, AU, 26)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def ledger():
    """42 · the ledger (s61, s62): the cold snap, established (the thermometer's cold band, ringed green); the Carolina Bays as its
    craters, ruled out (struck); the trigger and the platinum, open, meltwater the leading suspect; a comet behind it all, awaiting
    evidence: a faint airburst glow over a landscape with no crater."""
    cells = [(110, 140), (908, 140), (110, 470), (908, 470)]
    els = [box(x, y, 760, 300, "#1f1914", "rgba(245,236,220,.14)", 1.5, 14, -1) for x, y in cells] + \
          [lab(840, 186, "the cold snap", .3, BONE, 28, "end"), lab(1638, 186, "the bays as craters", 5.2, BONE, 28, "end"),
           lab(1638, 516, "a comet behind it?", 18.6, LILAC, 28, "end"), lab(840, 516, "what tipped it?", 10.4, BONE, 28, "end")]
    sc = lambda pts: [[round(150 + (X(a) - 160) * .3, 1), round(170 + (b - 290) * .62, 1)] for a, b in pts]
    els += [line(sc(CA1), -1, AMBER, 3, curve=True, draw=False), line(sc(CA2), -1, AMBER, 3, curve=True, draw=False), line(sc(CB + CC), -1, BLUE, 3, curve=True, draw=False),
            line(sc(CD), -1, AMBER, 3, curve=True, draw=False),
            poly(rell(round(150 + (X0 - 160) * .3 + (X1 - X0) * .15, 1), round(170 + (YD_Y - 290) * .62, 1), (X1 - X0) * .15 + 26, 30), "none", GREEN, 3.5, 1.6, True, fx="draw", dur=.7)] + \
           chip(700, 300, "Established", GREEN, 2.0, 30)
    v = View(-84, -73, 30, 40.5, (930, 150, 380, 280))
    from f03 import _bays
    sites = _bays()[::3]
    w = round(v.p(-73, 35)[0] - v.ox + 20, 1)
    els += [{"k": "group", "clip": [v.ox - 10, 150, w, 280, 10], "bg": "#16303d", "in": 5.2,
             "els": [{"k": "map", "land": v.land()}] + [dot(*v.p(lo, la), 3, "#9fd0ff", -1) for lo, la in sites]},
            strike(v.ox, 420, v.ox + w - 20, 160, 8.2)] + chip(1500, 300, "Ruled out", RED, 8.4, 30)
    els += [line([[160, 720], [190, 720], [205, 610], [222, 720], [260, 720]], 12.6, AU, 3, dur=.4), lab(210, 590, "platinum", 12.8, AU, 24)] + \
           [glow(410, 640, 120, 16.0, .8, "scan")] + wave(410, 660, 15.8, 1.3) + [lab(410, 720, "meltwater", 16.2, BLUE, 26)] + \
           chip(700, 580, "trigger: open", AMBER, 14.6, 28) + chip(700, 680, "platinum: open", AMBER, 14.9, 28)
    els += comet(1060, 560, 18.8, ang=-35, L=80) + chip(1500, 640, "Awaiting evidence", LILAC, 20.8, 28) + \
           [line([[960, 720], [1100, 712], [1260, 722], [1350, 716]], 24.0, "#8c7152", 3, curve=True, dur=.6), glow(1150, 650, 90, 24.6, .5, "red"),
            ring(1150, 650, 34, 24.8, LILAC, 2, "claimed")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def blind():
    """43 · what would change our minds (s63): a boundary section, six numbered sample bags with no layer names, sent to three labs; a
    blindfold in each window, like a blind taste test."""
    cols = ["#6f5a43", "#8a6a4a", "#5f4c39", "#7a6248", "#4f3f30", "#6b5640"]
    els = [box(120, 220 + 80 * k, 440, 80, c, r=0, at=.3) for k, c in enumerate(cols)] + [box(120, 220, 440, 480, "none", BONE, 2, 6, .3)]
    for k in range(6):
        y = 260 + 80 * k
        els += [box(300, y - 22, 54, 44, "#efe6d2", "#b8a888", 1.5, 10, round(3.0 + .1 * k, 2), fx="pop"), ink(327, y + 9, str(k + 1), round(3.05 + .1 * k, 2), INK, 26)]
        els += [lab(530, y + 10, "?", 5.6, DIM, 30, "end")]
    labs_ = [(900, 600), (1200, 600), (1500, 600)]
    for k, (x, y) in enumerate(labs_):
        els += [box(x - 110, y - 160, 220, 160, "#3a3028", "#cbbca8", 2, 4, round(2.4 + .15 * k, 2), fx="rise"),
                poly([[x - 124, y - 160], [x, y - 230], [x + 124, y - 160]], "#5a4a3c", "#cbbca8", 2, round(2.5 + .15 * k, 2)),
                box(x - 50, y - 130, 100, 80, "#1a1511", "#cbbca8", 2, 6, round(2.6 + .15 * k, 2)),
                {"k": "circle", "x": x, "y": y - 86, "r": 24, "fill": "#e8d6b8", "c": "none", "w": 0, "in": round(4.6 + .2 * k, 2)},
                box(x - 28, y - 100, 56, 13, "#2a3a5a", r=4, at=round(4.7 + .2 * k, 2)),
                line([[x + 26, y - 94], [x + 40, y - 84]], round(4.7 + .2 * k, 2), "#2a3a5a", 4, draw=False), line([[x + 26, y - 94], [x + 42, y - 98]], round(4.7 + .2 * k, 2), "#2a3a5a", 4, draw=False),
                line([[x - 8, y - 74], [x + 8, y - 74]], round(4.7 + .2 * k, 2), "#6a4a3a", 2.5, draw=False),
                arrow([[575, 280 + 70 * k], [round((575 + x) / 2, 1), 170 - 20 * k], [x, y - 244]], round(4.0 + .2 * k, 2), AU, 2.5, "inferred", .8)]
    els += [lab(1200, 700, "blind test", 7.4, AU, 32), lab(340, 190, "same sections", 1.0, BONE, 28)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def tests():
    """44 · the tests that would decide it (s64): shocked quartz or a crater, confirmed by outside impact experts; platinum and iridium in
    several ice and ocean cores, telling a comet from a volcano; one layer with one date everywhere; or, the other way, the same specks
    at every level, and the comet fades."""
    cw, gap, x0, y0, y1 = 380, 20, 90, 150, 760
    CARD = "#1f1914"
    els = [box(x0 + k * (cw + gap), y0, cw, y1 - y0, CARD, "rgba(245,236,220,.14)", 1.5, 14, -1) for k in range(4)]
    c = [x0 + k * (cw + gap) + cw / 2 for k in range(4)]
    q = [[c[0] - 70, 300], [c[0] - 20, 250], [c[0] + 60, 262], [c[0] + 84, 330], [c[0] + 30, 384], [c[0] - 54, 372]]
    els += [poly(q, "#d8d2c8", "#ffffff", 2, .2, fx="pop")] + \
           [line([[c[0] - 44 + 22 * j, 366], [c[0] - 14 + 22 * j, 270]], .6, "#7a7a8a", 1.5, draw=False) for j in range(5)] + \
           [line([[c[0] - 50, 300 + 18 * j], [c[0] + 56, 280 + 18 * j]], .7, "#7a7a8a", 1.5, draw=False) for j in range(4)] + \
           [lab(c[0], 214, "shocked quartz", .4, BONE, 26),
            poly(rell(c[0], 480, 110, 26), "none", LILAC, 2.5, 1.4, True, style="claimed"), lab(c[0], 548, "or a crater", 1.6, LILAC, 24),
            person(c[0] - 40, 690, 76, 3.0, "#e8d6b8"), lab(c[0] + 20, 740, "outside experts", 3.2, BONE, 26),
            line([[c[0] + 40, 620], [c[0] + 58, 640], [c[0] + 96, 590]], 4.4, GREEN, 5, dur=.4)]
    for k, (col, xx) in enumerate(((ICE, c[1] - 90), ("#87705a", c[1] - 30), (ICE, c[1] + 30), ("#87705a", c[1] + 90))):
        els += [box(xx - 16, 250, 32, 210, col, BONE, 1.5, 6, round(6.6 + .25 * k, 2), fx="rise")]
    els += [lab(c[1], 214, "ice and ocean cores", 6.8, BONE, 26),
            line([[c[1], 470], [c[1], 520]], 8.6, BONE, 2.5, dur=.3), line([[c[1], 520], [c[1] - 90, 590]], 8.7, BONE, 2.5, dur=.3), line([[c[1], 520], [c[1] + 90, 590]], 8.7, BONE, 2.5, dur=.3)] + \
           comet(c[1] - 90, 640, 9.2, ang=-40, L=50, r=7, g=40) + \
           [poly([[c[1] + 50, 690], [c[1] + 80, 630], [c[1] + 100, 630], [c[1] + 130, 690]], "#6a5040", "#cbbca8", 2, 10.0, fx="pop"),
            glow(c[1] + 90, 624, 40, 10.2, .9, "fire"), lab(c[1] - 90, 730, "comet", 9.4, LILAC, 24), lab(c[1] + 90, 730, "volcano", 10.2, "#ffb07a", 24)]
    v = View(-130, 50, 0, 62, (c[2] - 175, 270, 350, 240))
    w = round(v.p(50, 30)[0] - v.ox + 16, 1)
    pins = [(-100, 38), (-80, 35), (-110, 33), (5, 51), (38, 36), (-68, 8)]
    els += [lab(c[2], 214, "one layer, one date", 11.4, BONE, 26),
            {"k": "group", "clip": [v.ox - 8, 264, w, 252, 10], "bg": "#16303d", "in": 11.4, "els": [{"k": "map", "land": v.land()}]}]
    for k, pq in enumerate(pins):
        x, y = v.p(*pq)
        els += [dot(x, y, 6, AU, round(11.6 + .07 * k, 2)), line([[x, y + 6], [x, 600]], 12.8, AU, 1.5, "inferred", .5), glow(x, y, 30, 13.6, .9, "lamp")]
    els += [line([[c[2] - 160, 600], [c[2] + 160, 600]], 12.8, AU, 4, dur=.6), lab(c[2], 646, "everywhere", 13.8, AU, 28)]
    cols = ["#6f5a43", "#8a6a4a", "#5f4c39", "#7a6248", "#4f3f30"]
    els += [box(c[3] - 150, 330 + 70 * k, 300, 70, cc, r=0, at=15.0) for k, cc in enumerate(cols)] + comet(c[3], 250, 15.0, ang=-35, L=60, r=7, g=50) + \
           [dot(round(c[3] - 120 + 60 * j + 14 * (k % 2), 1), 365 + 70 * k, 4, LILAC, round(16.4 + .05 * (5 * k + j), 2)) for k in range(5) for j in range(5)] + \
           [{"k": "circle", "x": c[3], "y": 250, "r": 70, "fill": CARD, "c": "none", "w": 0, "in": 18.8, "op": .82, "keepop": True, "dur": 1.0},
            lab(c[3], 214, "the same specks", 15.2, LILAC, 26), lab(c[3], 720, "at every level", 17.8, LILAC, 26)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def night():
    """45 · the last image (s65): night tundra under stars, the little white flower in the foreground, the ground cut open below it where
    the thin layer glows faintly, a faint dotted comet trail high in the sky."""
    G = 600
    bands = [(G, 660, "#3e3326"), (660, 720, "#4f4030"), (720, 790, "#34291f"), (790, 1000, "#433629")]
    els = [box(-20, y0, 1820, y1 - y0, c, r=0, at=-1) for y0, y1, c in bands] + \
          [line([[-20, y], [1800, y]], -1, "#e9dccb", 1.2, "inferred", draw=False, op=.18) for y in (660, 720, 790)] + \
          [line([[-20, G], [1800, G]], -1, "#8c7152", 2.5, draw=False)] + \
          [line([[30 + 37 * k, G], [36 + 37 * k, G - 10 - 4 * (k % 3)]], -1, "#56703f", 2, draw=False) for k in range(48)] + \
          [line([[-20, 690], [1800, 690]], .6, LILAC, 10, dur=2.4, op=.14), line([[-20, 690], [1800, 690]], .6, "#e9e2ff", 2.5, dur=2.4, op=.42),
           glow(1200, 690, 240, 1.6, .3, "scan")]
    fx, fy = 420, 548
    els += [line([[fx, fy + 12], [fx - 3, G + 2]], 3.0, "#4f7a40", 3, curve=True, dur=.4)] + \
           [poly(rell(round(fx + 15 * math.cos(math.radians(45 * k)), 1), round(fy + 15 * math.sin(math.radians(45 * k)), 1), 14, 7, 45 * k, 16),
                 "#f7f4ec", "#d8d2c4", 1, round(3.2 + .06 * k, 2), True, fx="pop") for k in range(8)] + \
           [dot(fx, fy, 6, AU, 3.7), glow(fx, fy, 44, 3.7, .5, "lamp")] + \
           [line([[1560, 120], [1120, 290]], 5.8, LILAC, 2.5, "claimed", 1.4, op=.55), glow(1120, 290, 50, 6.8, .4, "scan")]
    return {"base": "sky", "tod": "night", "ground": G, "groundc": "#1d1915", "sun": False, "moon": [300, 200, 22], "cam": [1, 889, 500], "els": els}
# ================================================================ the film
def film():
    S = [None] * 50                             # the scenes (0 to 45) and four reframings of earlier panels (46 to 49)
    S[0], S[1], S[2], S[3], S[4], S[5], S[6], S[7], S[8] = thermo(), fingerprint(), thaw(), dryas(), icecore(), count(), lake(), clocks(), thermo_b()
    S[9], S[10], S[11], S[12], S[13], S[14], S[15] = claim(), dig(), map18(), platinum(), syria_map(), village(), three()
    S[16], S[17], S[18], S[19], S[20], S[21], S[22], S[23], S[24] = hole(), tunguska(), seven(), graphene(), mats(), album(), flash(), dates(), bell()
    S[25], S[26], S[27] = bays(), sandclock(), whitepond()
    S[28], S[29], S[30], S[31], S[32], S[33] = belt(), agassiz(), kennett(), plumbing(), mackenzie(), recount()
    S[34], S[35], S[36], S[37], S[38], S[39] = glass(), thermos(), village2(), seeds(), rebuilt(), duskfield()
    S[40], S[41], S[42], S[43], S[44], S[45] = journals(), retract(), ledger(), blind(), tests(), night()
    S[46] = {"cam": [1.12, 900, 446]}          # alias of 0: the camera tilts up into the sky
    S[47] = {"cam": [1.18, 889, 470]}          # alias of 10: closer on the bones
    S[48] = {"cam": [1.6, 1430, 390]}          # alias of 33: the Iceland map
    S[49] = {"cam": [1, 889, 500]}             # alias of 33: the whole recount again
    alias = {46: 0, 47: 10, 48: 33, 49: 33}
    beats = [
        B("hook", 0, lines_of(0, 0, [(1, "What could throw", 46, 1.4), (1, "And that it left", 1, 1.6)])),
        B("title", 1, lines_of(0, 1), intro=True),
        B("world", 2, lines_of(0, 2, [(1, "Scientists call it", 3, 1.6), (2, None, 4, 1.6), (2, "Count them down", 5, 1.6), (3, None, 6, 1.6), (4, None, 7, 1.6),
                                      (4, "The cold itself", 8, 1.6)]), chapter=SCRIPT["chapters"][0]["title"]),
        B("collision", 9, lines_of(1, 0, [(1, None, 10, 1.6), (1, "Below it", 47, 1.4)]), chapter=SCRIPT["chapters"][1]["title"]),
        B("cost", 10, lines_of(1, 1, [(0, "By {2013", 11, 1.6), (1, None, 12, 1.6)])),
        B("reversal", 13, lines_of(1, 2, [(0, "In its layer", 14, 1.6), (1, None, 15, 1.6)])),
        B("collision", 16, lines_of(2, 0, [(0, "To be ^fair", 17, 1.6)]), chapter=SCRIPT["chapters"][2]["title"]),
        B("cost", 18, lines_of(2, 1, [(0, "Another said", 19, 1.6), (1, None, 20, 1.6), (1, "If the confetti", 21, 1.6), (2, None, 22, 1.6),
                                      (2, "In {2014", 23, 1.6), (2, "The comet team answered", 24, 1.6)])),
        B("reversal", 25, lines_of(2, 2, [(0, "But buried sand", 26, 1.6), (1, None, 27, 1.6)])),
        B("world", 28, lines_of(3, 0, [(1, None, 29, 1.6)]), chapter=SCRIPT["chapters"][3]["title"]),
        B("reversal", 30, lines_of(3, 1, [(0, "And even the comet paper", 31, 1.6)])),
        B("cost", 29, lines_of(3, 2, [(0, "Then, in {2018", 32, 1.6)])),
        B("tag", 33, lines_of(3, 3, [(0, "more like a long", 48, 1.4), (0, "That reading is new", 49, 1.4)])),
        B("collision", 34, lines_of(4, 0, [(0, "The comet team answers", 35, 1.6)]), chapter=SCRIPT["chapters"][4]["title"]),
        B("world", 36, lines_of(4, 1)),
        B("cost", 37, lines_of(4, 2, [(0, "And the comet team adds", 38, 1.6)])),
        B("reversal", 0, lines_of(4, 3)),
        B("tag", 39, lines_of(4, 4)),
        B("weigh", 40, lines_of(5, 0, [(0, "Since {2025", 41, 1.6), (1, None, 42, 1.6)]), chapter=SCRIPT["chapters"][5]["title"]),
        B("test", 43, lines_of(5, 1, [(0, "Shocked minerals", 44, 1.6)])),
        B("close", 45, lines_of(5, 2)),
    ]
    desc = re.sub(r"00:00 The cold comes back\n(?:mm:ss [^\n]*\n?)+", "{chapters}\n", SCRIPT["description"])
    ep = {"id": "lf-sky-fell", "code": "LF.04", "series": SCRIPT["series"], "title": SCRIPT["title"], "case": "younger-dryas-impact",
          "verdict": "unsupported", "claim": "Did a comet bring back the Ice Age cold, 12,900 years ago?", "mood": "mystery",
          "hook_text": "Did a *comet* bring back the Ice Age?", "beats": beats, "shots": S,
          "sources": "Rasmussen et al. 2006 (doi:10.1029/2005JD006079) · Buizert et al. 2014 (doi:10.1126/science.1254961) · "
                     "Firestone et al. 2007 (doi:10.1073/pnas.0706977104) · Meltzer et al. 2014 (doi:10.1073/pnas.1401150111) · "
                     "Kennett et al. 2015 (doi:10.1073/pnas.1507146112) · Keigwin et al. 2018 (doi:10.1038/s41561-018-0169-6) · "
                     "Holliday et al. 2023 (doi:10.1016/j.earscirev.2023.104502)",
          "post": "12,900 years ago the north froze again for 1,200 years. Did a comet do it? Two decades of evidence, both camps at their strongest, weighed.",
          "hashtags": ["#YoungerDryas", "#IceAge", "#Comet", "#Prehistory", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": SCRIPT["title"], "yt_title": SCRIPT["yt_title"], "description": desc,
          "end_line": "Something abrupt really did happen. We just haven't caught what."}
    return remix(ep, alias=alias,
                 line_adds={(0, 1): (thermo_line2() + thermo_sky(), None), (2, 1): (thaw_cold(), None)},
                 beat_adds={4: (clues(), [1.15, 1005, 480]), 11: (agassiz_gap(), None), 16: (thermo_c(), None)})


def EPISODES():
    return [film()]
