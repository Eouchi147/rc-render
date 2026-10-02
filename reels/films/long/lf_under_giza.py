"""LF.01 Under Giza (16:9 long form): the hidden rooms that are real, and the rumours.

Script: films/long/lf-under-giza/script.json (narration kept word for word; this module adds the pictures and the [go:] markers).
One wall, six rooms: the cold open, Particles from space, Pillars under Khafre, Doors in the dark, The Sphinx and the rain,
The ledger. Drawings are schematic but true to the numbers said: the Great Pyramid section after giza.Section (Petrie, Lehner),
the Big Void (Morishima et al. 2017) and the North Face Corridor (Procureur et al. 2023) where those papers put them, Khafre and
the claimed 648 m to one scale, the shafts at their slope, 20 cm at 9 units a centimetre. Solid = measured, dashed = inferred,
dotted = claimed.

Reused from the Shorts: big-void (iso3d.great_pyramid, the muon X-ray idea, the endoscope view, f05.corridor_view), khafre-pillars
(lg_b: the cut under Khafre, the claim, the satellite, the peer-review gate, the retraction, the tests, the paper), sealed-door
(lg_b: the shaft view and its pins, the 20 cm square with the bust and the cat, the climb, the side cut, the record), sphinx-erosion
(f05: the wall face, the rain, the timeline, the temple built from the pit), power-plant (iso3d.relieving_stack), the plateau
diorama (iso3d.giza on PLATEAU). All redrawn wide for 16:9.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-under-giza/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-under-giza/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-under-giza RC_FILMS_EPS=/tmp/claude-0/sbx_lf-under-giza/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-under-giza/boards python3 films.py long.lf_under_giza
"""
import copy, math, random
from films import View
from mural import remix
from illus import person, arrow, line, glow, label, dot, box, ring, oval, ellipse, question, BONE, AMBER, BLUE, RED, GREEN, LILAC
from giza import Section, BASE as GB, SLOPE
from scenes import GP, NILE, ROSETTA, DAMIETTA
import iso3d
from lg_b import _satellite, _paper, _check, _strike, _robot, _tv, _bust, _cat, _poly, COP, LIME, INK

W_, H_ = 1778, 1000            # the 16:9 frame; drawings in x 80..1700, y 120..800
GOLD, SCAN, ICE = "#f2c98e", "#cfe6ff", "#cfe6ff"
DIM = "#cbbca8"
GRADE = {"strong": "#7fd1d4", "established": "#8fd9b0", "awaiting": "#c9c1ee", "open": "#f0b06a", "ruled": "#e98a8a", "mixed": "#d8c7a8"}
FLAT = "#17120e"               # a flat background for panels that "morph" (veils of the same colour fade what is under them)
C30 = math.cos(math.pi / 6)


# ---------------------------------------------------------------- small helpers
def r1(v):
    return round(v, 1)


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words (scales with the picture, like a plaque)."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else x
    return [box(r1(x0), r1(y - h / 2), r1(w), r1(h), "rgba(18,13,10,.9)", c, 2.5, h / 2, at, fx="pop"),
            label(r1(x0 + w / 2), r1(y + size * .36), t, round(at + .05, 2), c, size, scl=True, fx="pop")]


def wipe(x, y, w, h, at, fill=FLAT, op=1.0, dur=.4, **kw):
    """A veil (op < 1) or a clean sheet (op 1) laid over part of a panel: what was there fades back."""
    e = box(x, y, w, h, fill, r=kw.pop("r", 0), at=at, op=op, **kw)
    e["dur"] = dur
    return e


def iso(items, x, y, s, az, spin=0.0, el=.32, at=-1, **kw):
    e = {"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": items, "in": at}
    e.update(kw)
    return e


def ov(base, items, at, fx="pop", **kw):
    """An overlay model: the same camera, scale and turn as `base`, other items, its own build-in (same panel clock: in step)."""
    e = {k: base[k] for k in ("x", "y", "s", "az", "spin", "el")}
    e.update(k="iso", items=items, **{"in": at})
    if fx:
        e["fx"] = fx
    e.update(kw)
    return e


def P3(e, p, t=0.0):
    """Where a world point (x, y, z) of an iso element lands on the panel at local time t."""
    az = math.radians(e.get("az", 35) + e.get("spin", 0) * t)
    ca, sa = math.cos(az), math.sin(az)
    x, y, z = p
    rx, rz = x * ca - z * sa, x * sa + z * ca
    S, el = e["s"], e.get("el", .32)
    return [r1(e["x"] + (rx - rz) * C30 * S), r1(e["y"] - y * S + (rx + rz) * el * S)]


def ilab(x, y, z, t, c=BONE, dy=0, st="lab", a="middle"):
    return {"t": "label", "x": x, "y": y, "z": z, "text": t, "st": st, "c": c, "dy": dy, "a": a}


def gp_parts(void=True, nfc=False, shafts=False):
    """The Great Pyramid model (iso3d.great_pyramid) split into its shell and its rooms, so the rooms can build in one by one."""
    items = iso3d.great_pyramid(void=void, nfc=nfc, shafts=shafts)
    rooms = {"gp": [], "gg": [], "kc": [], "qc": [], "bv": [], "nfc": [], "rest": []}
    for k, it in enumerate(items):
        i = it.get("id")
        if k == 1:
            rooms["gg"].append(it)
        elif i in rooms:
            rooms[i].append(it)
        elif it.get("t") == "glow":
            rooms["bv"].append(it)
        else:
            rooms["rest"].append(it)
    return rooms


def void_centre():
    bv = next(i for i in iso3d.great_pyramid(void=True) if i.get("id") == "bv")
    xs = [p[0] for p in bv["prof"]]; ys = [p[1] for p in bv["prof"]]
    return (sum(xs) / 4, sum(ys) / 4, 0.0)


def nfc_centre():
    h = 20.0; x0 = h / math.tan(SLOPE) + .8
    return (x0 + 4.5 - GB / 2, h + 1.1, 0.0)


def round_view(cx, cy, R):
    """A round camera view: black all round a circle of radius R (the whole panel), a faint rim."""
    out = 1300
    return [{"k": "circle", "x": cx, "y": cy, "r": (R + out) / 2, "c": "#0b0907", "w": out - R + 6, "op": 1, "in": -1},
            {"k": "circle", "x": cx, "y": cy, "r": R, "c": "rgba(255,226,168,.35)", "w": 2, "op": 1, "in": -1}]


def shaft_view(cx, cy, R, n=7, kend=.38, tone=(214, 190, 150), door=True, vc=None):
    """lg_b._shaft_view at any size: up a square stone shaft through a robot's camera, the slab at the end."""
    W = R * 1.58
    els = []
    def sq(t):
        k = 1 - t * (1 - kend); w = W * k / 2
        return [[r1(cx - w), r1(cy - w)], [r1(cx + w), r1(cy - w)], [r1(cx + w), r1(cy + w)], [r1(cx - w), r1(cy + w)]]
    rs = [sq(i / n) for i in range(n + 1)]
    for i in range(n):
        a, b = rs[i], rs[i + 1]; f = 1 - i / n
        for j, (p, q) in enumerate(((0, 1), (1, 2), (2, 3), (3, 0))):
            lit = [.55, .72, .95, .62][j]
            c = tuple(int(v * (.22 + .78 * f * f) * lit) for v in tone)
            els.append({"k": "poly", "p": [a[p], a[q], b[q], b[p]], "fill": "rgb(%d,%d,%d)" % c, "c": "rgba(40,28,18,.85)", "w": 1.4 if i % 2 else 1, "op": 1, "in": -1})
    far = rs[-1]
    if door:
        els.append({"k": "poly", "p": far, "fill": LIME, "c": "rgba(255,236,206,.7)", "w": 2, "in": -1})
        g = R * 12 / 482
        els.append({"k": "poly", "p": [[far[0][0] + g, far[0][1] + g], [far[1][0] - g, far[1][1] + g], [far[2][0] - g, far[2][1] - g], [far[3][0] + g, far[3][1] - g]],
                    "fill": "#e6d3b0", "c": "none", "w": 0, "in": -1, "op": .7})
    els.append(glow(cx, cy + 30, R * .75, -1, .32, "lamp"))
    return els + round_view(*(vc or (cx, cy)), R), far


def pins(cx, cy, R, at):
    """The two copper fittings on the slab's face, bent down against it (lg_b._pins at any size)."""
    k = R / 482
    out = []
    for sgn in (-1, 1):
        x = cx + sgn * 72 * k
        out += [line([[r1(x), r1(cy - 40 * k)], [r1(x), r1(cy - 96 * k)], [r1(x + sgn * 16 * k), r1(cy - 108 * k)]], at, COP, 8 * k, dur=.4),
                line([[r1(x - 2 * k), r1(cy - 44 * k)], [r1(x - 2 * k), r1(cy - 92 * k)]], at + .2, "#f4b27a", 2, draw=False, op=.8),
                glow(r1(x), r1(cy - 70 * k), 50 * k, at, .5)]
    return out


def corridor_view(cx, cy, R, n=8, tone=(214, 190, 150)):
    """f05.corridor_view at any size: down a stone corridor with a gabled roof, lamp-lit, through a round endoscope."""
    Wd, Hd = R * 1.95, R * 1.62
    els = []
    def rg(t):
        k = 1 - t * .86; w, h = Wd * k / 2, Hd * k / 2
        return [[r1(cx - w), r1(cy + h)], [r1(cx - w), r1(cy - h * .2)], [r1(cx), r1(cy - h)], [r1(cx + w), r1(cy - h * .2)], [r1(cx + w), r1(cy + h)]]
    rs = [rg(i / n) for i in range(n + 1)]
    for i in range(n):
        a, b = rs[i], rs[i + 1]; f = 1 - i / n
        for j, (p, q) in enumerate(((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))):
            lit = [.62, .9, .75, .5, .42][j]
            c = tuple(int(v * (.22 + .78 * f * f) * lit) for v in tone)
            els.append({"k": "poly", "p": [a[p], a[q], b[q], b[p]], "fill": "rgb(%d,%d,%d)" % c, "c": "rgba(40,28,18,.8)", "w": 1.2, "op": 1, "in": -1})
    els.append({"k": "poly", "p": rs[-1], "fill": "#0b0907", "c": "rgba(40,28,18,.8)", "w": 1, "in": -1})
    els.append(glow(cx, cy + 40, R * .8, -1, .35, "lamp"))
    return els + round_view(cx, cy, R)


# ---------------------------------------------------------------- Khafre cut open (lg_b._khafre_cut, widened): 0.8 units a metre
KGY, KPX, KX = 250, .8, 760
KH, KB = 143.5 * KPX, 215.3 * KPX / 2


def kD(m):
    return r1(KGY + m * KPX)


def kcut(cam=None, at=-1, khufu=False):
    """Khafre's pyramid on the plateau, the ground cut open below it to about 700 m, all to one scale."""
    els = [_poly([[KX - KB, KGY], [KX, KGY - KH], [KX + KB, KGY]], "url(#k-blocks)", "#f2dcb4", 2, at),
           _poly([[KX, KGY - KH], [KX + KB, KGY], [KX, KGY]], "rgba(0,0,0,.28)", at=at),
           _poly([[KX - KB * .2, KGY - KH * .8], [KX, KGY - KH], [KX + KB * .2, KGY - KH * .8]], "#efe0c2", at=at, op=.92)]
    if khufu:                                                  # the Great Pyramid beside it, a little behind (same scale)
        gx, gh, gb = KX + 330, 146.6 * KPX, 230.3 * KPX / 2
        els = [_poly([[gx - gb, KGY], [gx, KGY - gh], [gx + gb, KGY]], "rgba(242,220,180,.10)", "rgba(242,220,180,.45)", 1.6, at)] + els
    return {"base": "section", "tod": "night", "ground": KGY, "lx": 40, "cam": list(cam or [1, 889, 500]),
            "layers": [{"d": 0, "c": "#7a6248", "t": ""}, {"d": 21, "c": "#6a553f", "t": ""}, {"d": 240, "c": "#57473a", "t": ""}, {"d": 512, "c": "#463a2f", "t": ""}],
            "els": els}


def kshafts(at, op=1.0, n=8, spiral=True, dt=.1):
    """The claimed shafts (lilac dots): eight in a row under Khafre, paths spiralling round them, to about 570 m."""
    top, bot = KGY + 8, kD(568)
    els = []
    for k in range(n):
        x = KX + (k - 3.5) * 19
        e = box(r1(x - 6), top, 12, r1(bot - top), "rgba(201,193,238,.10)", LILAC, 1.6, 3, round(at + dt * k, 2), style="claimed")
        if op < 1:
            e.update(op=op, keepop=True)
        els.append(e)
        if spiral:
            pts = [[r1(x + 5.5 * math.sin(2 * math.pi * (y - top) / 28 + k)), y] for y in range(int(top) + 4, int(bot) - 2, 4)]
            els.append({"k": "line", "p": pts, "c": LILAC, "w": 1.4, "curve": True, "op": .7 * op, "keepop": True, "in": round(at + 1.0 + .06 * k, 2)})
    return els


def kcubes(at, op=1.0):
    """The two claimed cubes, about 80 m a side (64 units), below the shafts."""
    els = []
    s, d = 80 * KPX, 12
    for j, cx in enumerate((KX - 42, KX + 42)):
        x0, y0 = cx - s / 2, kD(570) + 2
        a = round(at + .3 * j, 2)
        for e in (box(r1(x0), r1(y0), r1(s), r1(s), "rgba(201,193,238,.12)", LILAC, 2.2, 2, a, style="claimed"),
                  _poly([[x0, y0], [x0 + d, y0 - d * .7], [x0 + s + d, y0 - d * .7], [x0 + s, y0]], "rgba(201,193,238,.18)", LILAC, 2, a, style="claimed"),
                  _poly([[x0 + s, y0], [x0 + s + d, y0 - d * .7], [x0 + s + d, y0 + s - d * .7], [x0 + s, y0 + s]], "rgba(201,193,238,.08)", LILAC, 2, a, style="claimed")):
            if op < 1:
                e.update(op=op, keepop=True)
            els.append(e)
    return els


# ================================================================ cold open
def s01_void():
    """s1 + s2: the Great Pyramid as an x-ray model turning slowly, the Big Void glowing in it, a '?' (2 s); then (at 'We only
    know about it', about 6.7 s) the camera eases back and muons rain through the stone: most stop inside it (red dots), a few
    pass straight through the void and on to the ground."""
    R = gp_parts(void=True)
    base = iso(R["gp"] + R["rest"] + R["gg"] + R["kc"] + R["qc"] + R["bv"] + iso3d.ground(122, grid=61), 889, 700, 2.7, -28, .6, el=.26, at=-1)
    vc = void_centre()
    els = [glow(889, 560, 620, -1, .16, "lamp"), base,
           ov(base, [{"t": "q", "x": vc[0], "y": vc[1] + 1, "z": 0, "size": 90, "c": ICE}], 2.0)]
    # the muons (shot 1, at about 6.7 s), drawn where the model stands at about 10 s
    T, t0 = 10.0, 6.9
    apex = P3(base, (0, 146.6, 0), T)
    vx, vy = P3(base, vc, T)
    xs = [P3(base, (x, 0, z), T)[0] for x, z in ((-115, -115), (115, -115), (115, 115), (-115, 115))]
    lx, rx = min(xs), max(xs)
    rnd = random.Random(7)
    rays = []
    for k in range(60):
        if len(rays) >= 30 * 2:
            break
        x = r1(rnd.uniform(lx + 40, rx - 40))
        if abs(x - vx) < 46:
            continue
        top = apex[1] + abs(x - apex[0]) * (690 - apex[1]) / ((rx - lx) / 2) + 20       # under the faces
        at = round(t0 + .3 + .045 * len(rays), 2)
        stop = r1(rnd.uniform(min(top, 680), 700))
        rays += [line([[x, 120], [x, stop]], at, BLUE, 1.6, dur=.5, op=.75), dot(x, stop, 5, RED, round(at + .5, 2))]
    thru = [line([[r1(vx + dx), 120], [r1(vx + dx), 790]], round(t0 + 2.2 + .25 * j, 2), ICE, 3, dur=1.0) for j, dx in enumerate((-24, -8, 8, 24))]
    els += rays + thru + [glow(vx, vy, 120, t0 + 2.6, .8, "blue"), label(1560, 210, "muons", t0 + 1.2, BLUE, 32, "end")]
    cx, cy = P3(base, vc, 2.0)
    return {"base": "dark", "stars": 90, "cam": [1.7, cx, cy + 40], "els": els}, base, (vx, vy)


def s03_khafre_hook():
    """s3: Khafre cut open to scale (0.8 units a metre): a white arrow draws down 648 m, a stop bar and a blue glow at the bottom;
    the claimed shafts fade in faintly, lilac dots."""
    s = kcut(at=-1)
    s["els"] += kshafts(1.6, op=.45, spiral=False, dt=.05)
    s["els"] += [arrow([[KX, KGY + 6], [KX, kD(648)]], 1.0, BONE, 4, "known", 1.6, False),
                 line([[KX - 40, kD(648)], [KX + 40, kD(648)]], 2.6, BONE, 4, dur=.3), glow(KX, kD(648), 130, 2.7, .6, "blue"),
                 label(KX + 70, kD(330) + 16, "648 m", 2.0, BONE, 48, "start", st="serif"),
                 label(KX, KGY - KH - 22, "Khafre", .4, AMBER, 28)]
    return s


def s04_door():
    """s4: a robot camera's round view up the square shaft to the pale slab; its two copper pins glint (0.8 s)."""
    cx, cy, R = 889, 465, 330
    els, far = shaft_view(cx, cy, R)
    return {"base": "dark", "cam": [1, 889, 500], "els": els + pins(cx, cy, R, .8)}


def sphinx_pit(tod="night", x=820, w=860, gy=720, pyr=True, sun=False):
    """scenes.sphinx_side, widened: the Sphinx in its pit, side view, east to the left; Khafre's pyramid behind."""
    els = []
    if pyr:
        els.append({"k": "pyramid", "x": x + 470, "y": gy - 85, "w": 780, "cap": .1, "light": "left", "layer": "far", "in": -1})
    els.append({"k": "poly", "p": [[-300, gy - 95], [x - w * .62, gy - 95], [x - w * .6, gy], [x + w * .6, gy], [x + w * .62, gy - 95], [2100, gy - 95], [2100, 1500], [-300, 1500]],
                "fill": "url(#k-ground)" if tod == "night" else "url(#k-sand)", "c": "rgba(255,226,190,.4)", "w": 1.5, "in": -1})
    els.append({"k": "sphinx", "x": x, "y": gy, "w": w, "in": -1})
    sc = {"base": "sky", "tod": tod, "ground": gy - 95, "sun": sun or False, "cam": [1, 889, 500], "els": els}
    if tod == "night":
        sc["groundc"] = "url(#k-ground)"
    return sc


def s05_sphinx_rain():
    """s5: the Sphinx at night in its pit, the pyramid behind; fine rain draws down across the frame (0.5 s); 'rain, in the desert?'."""
    s = sphinx_pit("night")
    s["moon"] = [300, 190, 26]
    s["els"] += [box(-100, -100, 2000, 1200, "rgba(14,16,34,.38)", r=0, at=-1)]
    s["els"] += [{"k": "rays", "x0": -100, "x1": 1880, "y0": 110, "y1": 760, "n": 150, "spread": .12, "c": "#b9d6e8", "in": .5, "fx": "draw", "dur": 1.6},
                 label(470, 330, "rain, in the desert?", 1.4, ICE, 44, st="ital")]
    return s


def plateau(az=-160, spin=.5, s=1.0, cx=889, cy=520, el=.42, extra=(), night=True):
    """iso3d.plateau, widened: the three pyramids and the Sphinx on their diorama table, true size and place, centred in the panel."""
    items = iso3d.giza(town=False) + list(extra)
    base = iso(iso3d.diorama(**iso3d.PLATEAU) + items, 0, 0, s, az, spin, el, at=-1)
    x, y = P3(base, (-135, 0, 470), 0)
    base.update(x=r1(cx - x), y=r1(cy - y))
    return base


def plateau_pts():
    """World points on the plateau (x east, z south): Khufu's void, Khafre and below it, the Queen's Chamber shafts, the Sphinx."""
    (kx, kn), _ = GP["khafre"]
    sx, sn = GP["sphinx"]
    vc = void_centre()
    return {"void": (0, 205, 0), "khafre": (kx, 0, -kn), "under": (kx, 0, -kn + 150), "shafts": (0, 50, 80), "sphinx": (sx, 36, -sn),
            "kc": (0, 0, 0)}


def s06_plateau():
    """s6 (and s7 under the title card): the whole plateau at night, turning slowly; four lilac '?' pop one by one: the Great
    Pyramid's void, under Khafre, the Queen's Chamber shafts, the Sphinx."""
    base = plateau()
    pp = plateau_pts()
    qs = [pp["void"], pp["under"], pp["shafts"], pp["sphinx"]]
    (kx, _, kz) = pp["khafre"]
    down = ov(base, [{"t": "line", "p": [[kx + dx, 2, kz + 150], [kx + dx, -60, kz + 150]], "c": LILAC, "w": 3, "style": "claimed"} for dx in (-30, 30)], 1.1)
    els = [glow(889, 520, 700, -1, .14, "lamp"), base, down] + \
          [ov(base, [{"t": "q", "x": p[0], "y": p[1], "z": p[2], "size": 64, "c": LILAC}], round(.7 + .4 * k, 2)) for k, p in enumerate(qs)]
    return {"base": "dark", "stars": 160, "cam": [1, 889, 500], "els": els}


# ================================================================ chapter 1: Particles from space
def s09_size():
    """s9 (with s8 folded in: the chapter card holds 'The Great Pyramid at Giza...'): a locator map of the lower Nile with Giza;
    the pyramid in north-south section to scale (base 230 m, 146.6 m as built, 3 units a metre); '146 m' (0.6 s), '230 m' (1.0 s);
    a dashed 40-storey tower of the same height rises beside it, a person 1.7 m at its foot."""
    S = Section(s=3.0, cx=1060, gy=700)
    body, shade = S.body(), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0}
    x0, x1 = S.P(0, 0)[0], S.P(GB, 0)[0]
    top = S.P(GB / 2, 146.6)[1]
    v = View(29.0, 33.6, 28.8, 31.7, (104, 150, 400, 300))
    land = v.land()
    gx, gy_ = v.p(31.134, 29.979)
    cx_, cy_ = v.p(31.235, 30.044)
    mp = {"k": "group", "clip": [100, 146, 408, 308, 14], "bg": "#1d3a4a", "in": .2, "dur": .8, "els": [
          {"k": "map", "land": land, "rivers": [v.line(NILE), v.line(ROSETTA), v.line(DAMIETTA)]}]}
    els = [mp, box(100, 146, 408, 308, "none", "rgba(255,236,206,.35)", 2, 14, .2),
           {"k": "pin", "x": gx, "y": gy_, "r": 8, "c": AMBER, "t": "Giza", "lx": -16, "ly": 34, "a": "end", "tc": AMBER, "in": .6},
           dot(cx_, cy_, 5, DIM, .8), label(cx_ + 12, cy_ - 8, "Cairo", .8, DIM, 24, "start"),
           label(300, 440, "Nile", 1.0, "#9fd0ff", 24, st="ital"),
           {"k": "scale", "x": 130, "y": 430, "w": r1(v.km(50)), "t": "50 km", "in": 1.0}]
    els += [dict(body, **{"in": -1}), dict(shade, **{"in": -1}),
            {"k": "dim", "x1": x0 - 40, "y1": 700, "x2": x0 - 40, "y2": top, "t": "", "c": AMBER, "in": .6, "fx": "draw", "dur": .8},
            label(x0 - 58, (700 + top) / 2 + 12, "146 m", .9, AMBER, 34, "end"),
            {"k": "dim", "x1": x0, "y1": 728, "x2": x1, "y2": 728, "t": "", "c": BONE, "in": 1.0, "fx": "draw", "dur": .8},
            label((x0 + x1) / 2, 770, "230 m", 1.2, BONE, 30)]
    # the 40-storey tower (146 m, about 30 m wide), dashed: it rises; floors every 3.65 m
    tx, tw = 1500, 30 * 3.0
    tower = [box(tx, top, tw, 700 - top, "rgba(159,208,255,.06)", BLUE, 2, 2, 3.6, style="inferred", fx="fill", dur=1.2)]
    tower += [line([[tx + 6, r1(700 - k * 3.65 * 3)], [tx + tw - 6, r1(700 - k * 3.65 * 3)]], 4.6, BLUE, 1, draw=False, op=.35) for k in range(1, 40)]
    tower += [label(tx + tw / 2, top - 22, "40 storeys", 4.4, BLUE, 28), person(tx - 14, 700, 5.1, 4.8, "#e8d6b8"),
              ring(tx - 14, 697, 16, 5.0, BONE, 1.5, dur=.5)]
    return {"base": "dark", "stars": 60, "floor": 700, "cam": [1, 889, 500], "els": els + tower}


def s10_rooms():
    """s10: the x-ray model again, no void; the three rooms build in the order named: King's Chamber, Queen's Chamber,
    Grand Gallery, each with its label."""
    R = gp_parts(void=False)
    base = iso(R["gp"] + R["rest"] + iso3d.ground(122, grid=61), 889, 760, 4.2, -28, .5, el=.26, at=-1)
    T = 5.0
    kc = (8.2, 43.0, 0); qc = (0.0, 21.2, 0); gg = (-20.0, 31.0, 0)
    els = [glow(889, 560, 620, -1, .16, "lamp"), base,
           ov(base, R["kc"] + [ilab(14, 47, 0, "King's Chamber", BONE, 8, a="start")], 2.9),
           ov(base, R["qc"] + [ilab(0, 21.2, 0, "Queen's Chamber", BONE, 56)], 4.2),
           ov(base, R["gg"] + [ilab(-30, 40, 0, "Grand Gallery", BONE, -24)], 5.6)]
    cx, cy = P3(base, (-6, 34, 0), T)
    return {"base": "dark", "stars": 70, "cam": [1.35, cx, cy], "els": els}


def hand(cx, cy, s=1.0):
    """An open hand, palm towards us, fingers up (outline, warm line)."""
    P = lambda x, y: [r1(cx + x * s), r1(cy + y * s)]
    pts = [(-62, 120), (-70, 30), (-112, -20), (-104, -38), (-80, -28), (-58, -2), (-60, -110), (-46, -122), (-32, -110), (-28, -30),
           (-24, -138), (-8, -150), (6, -138), (8, -32), (14, -128), (30, -138), (44, -124), (38, -28), (50, -100), (64, -108), (76, -96),
           (64, 20), (56, 120)]
    return [P(x, y) for x, y in pts]


def s11_sky():
    """s11: night sky over a thin horizon, a pyramid small on it (a mountain of stone); a cosmic ray strikes the air high up
    (a spark), a cone of muons fans down to the ground; 'cosmic ray', 'muons'; then an open hand, three streaks straight through it."""
    gy = 700
    els = [{"k": "pyramid", "x": 300, "y": gy, "w": 230, "courses": False, "turn": .12, "in": .3, "fx": "rise"}]
    sx, sy = 900, 200
    els += [line([[1260, 100], [sx, sy]], 4.6, GOLD, 3, dur=.6), glow(sx, sy, 90, 5.1, .9, "lamp"), dot(sx, sy, 8, "#fff6e6", 5.1),
            label(sx + 70, sy - 30, "cosmic ray", 5.3, GOLD, 30, "start")]
    rnd = random.Random(3)
    for k in range(26):
        ex = r1(sx + (k - 12.5) * 34 + rnd.uniform(-10, 10))
        els.append(line([[sx, sy + 10], [ex, gy]], round(6.2 + .04 * k, 2), BLUE, 1.6, dur=.9, op=.7))
    els += [label(sx - 230, 400, "muons", 7.0, BLUE, 32, "end")]
    hx, hy = 1400, 560
    els += [{"k": "poly", "p": hand(hx, hy, 1.1), "fill": "rgba(232,184,122,.14)", "c": AMBER, "w": 2.6, "curve": True, "in": 11.4, "fx": "fade", "dur": .8}]
    for j, dx in enumerate((-40, 5, 46)):
        els.append(line([[hx + dx - 30, 130], [hx + dx + 10, 760]], round(12.3 + .55 * j, 2), ICE, 3, dur=.6))
    return {"base": "sky", "tod": "night", "ground": gy, "groundc": "url(#k-ground)", "sun": False, "cam": [1, 889, 500], "els": els}


def s12_xray():
    """s12: the muon X-ray, wide: 'air'; a block of 'stone' fills from the bottom; streaks stop in it (red dots); a hollow pops at
    'empty'; streaks over it pass through to a 'detector'; a histogram of counts builds, one tall bar under the hollow: a bright patch."""
    X0, X1, Y0, Y1 = 330, 1450, 270, 560
    hx0, hx1, hy0, hy1 = 830, 970, 350, 470
    els = [line([[120, 190], [1660, 190]], .2, "#6f8fa8", 2, dur=1.0), label(130, 170, "air", .5, "#9fb8cc", 30, "start")]
    els += [box(X0, Y0, X1 - X0, Y1 - Y0, "rgba(150,118,84,.95)", "#e7cfa6", 2, 6, 1.0, fx="fill", dur=.8), box(X0, Y0, X1 - X0, Y1 - Y0, "url(#k-blocks)", r=6, at=1.0, op=.35, fx="fill", dur=.8),
            label(X0 - 16, Y0 + 40, "stone", 2.2, "#e7cfa6", 32, "end")]
    rnd = random.Random(5)
    xs = [380, 440, 500, 560, 620, 690, 750, 1050, 1110, 1170, 1230, 1300, 1370, 1420]
    for k, x in enumerate(xs):
        yy = r1(rnd.uniform(Y0 + 40, Y1 - 30))
        at = round(2.5 + .07 * k, 2)
        els += [line([[x, 120], [x, yy]], at, ICE, 2.2, dur=.5), dot(x, yy, 7, RED, round(at + .5, 2))]
    els += [box(hx0, hy0, hx1 - hx0, hy1 - hy0, "#0d0b09", BLUE, 2, 8, 4.4, fx="pop", style="inferred")]
    for k, x in enumerate((860, 900, 940)):
        els.append(line([[x, 120], [x, 602]], round(4.9 + .15 * k, 2), ICE, 3, dur=.7))
    els += [box(X0, 600, X1 - X0, 20, "#3d5566", BLUE, 2, 4, 5.8, fx="pop"), label(X0 - 16, 618, "detector", 6.0, ICE, 28, "end")]
    n = 16
    for k in range(n):
        x = X0 + 20 + k * (X1 - X0 - 40) / n
        under = abs(x + 25 - 900) < 45
        h = 140 if under else 34 + 14 * abs(math.sin(k * 1.7))
        els.append(box(r1(x), r1(790 - h), 50, r1(h), BLUE if under else "#56708a", r=4, at=round(7.4 + .1 * k, 2), fx="fill", dur=.5))
    els += [glow(900, 660, 120, 9.4, .85, "blue"), label(1010, 680, "bright patch", 9.8, ICE, 30, "start")]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


GS = Section(s=4.2, cx=700, gy=740)          # the Great Pyramid section used for the detectors, the void and the corridor views


def gsec(rooms=True, op=.85):
    S = GS
    els = [dict(S.body(), **{"in": -1}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": -1}]
    if rooms:
        els += [dict(e, **{"in": -1, "op": op}) for e in S.els()]
    return els


def s13_detectors():
    """s13: the section; ScanPyramids' three kinds of detector as blue pins: two in the Queen's Chamber, one outside at the foot
    of the north face; then the three as icons, a blue arrow rising from each to meet above the Gallery, a ring."""
    S = GS; R = S.rooms()
    qx, qh = R["qc"]
    q = S.P(qx, qh + 2)
    nf = S.P(4, 1)
    bv, bvc = S.big_void()
    els = gsec()
    els += [{"k": "pin", "x": q[0] - 6, "y": q[1] + 6, "r": 6, "c": BLUE, "t": "plates · Nagoya", "a": "end", "lx": -26, "ly": 60, "st": "lab", "in": 2.4},
            {"k": "pin", "x": q[0] + 6, "y": q[1] + 6, "r": 6, "c": BLUE, "t": "strips · KEK", "lx": 26, "ly": 60, "st": "lab", "in": 3.0},
            {"k": "pin", "x": nf[0] - 18, "y": 734, "r": 7, "c": BLUE, "t": "gas · CEA", "a": "end", "lx": -20, "ly": -24, "st": "lab", "in": 5.4}]
    # different tools, one question: three icons, three arrows meeting above the Gallery
    ix = (1330, 1470, 1610); iy = 660
    els += [box(ix[0] - 40, iy - 8, 80, 16, "#9fb8cc", BONE, 1.5, 3, 7.0, fx="pop")]
    els += [box(ix[1] - 34, iy - 26, 68, 52, "#3d5566", BLUE, 1.5, 4, 7.2, fx="pop")] + [line([[ix[1] - 34, iy - 26 + 10 * k], [ix[1] + 34, iy - 26 + 10 * k]], 7.2, BLUE, 1.4, draw=False) for k in range(1, 5)]
    els += [box(ix[2] - 32, iy - 30, 64, 60, "#2a3640", ICE, 1.5, 10, 7.4, fx="pop")] + [ring(ix[2], iy, r, round(7.5 + .1 * k, 2), BLUE, 1.4, dur=.3) for k, r in enumerate((8, 16, 24))]
    els += [label(x, 740, t, 7.6, DIM, 24) for x, t in zip(ix, ("plates", "strips", "gas"))]
    for k, x in enumerate(ix):
        e = arrow([[x, iy - 40], [r1((x + bvc[0]) / 2 + 80), r1(bvc[1] - 70 - 26 * k)], [r1(bvc[0] + 46), r1(bvc[1] - 14)]], round(7.9 + .25 * k, 2), BLUE, 2, "known", 1.0)
        e.update(op=.6, keepop=True)
        els.append(e)
    els += [ring(bvc[0], bvc[1], 40, 9.4, AMBER, 3, dur=.7)]
    return {"base": "section", "tod": "night", "ground": 740, "cam": [1, 889, 500], "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 60, "c": "#4d3e30", "t": ""}], "els": els}


def s14_s15_void():
    """s14 (a new step on the detectors' panel, close on the Gallery): fans of tracks rise from the detectors and meet above the
    Gallery; the void fades in, dashed, and glows: 'the Big Void'. s15 (closer, at 'At least thirty metres long'): three buses end
    to end along it (30 m in all, to the section's scale); the Gallery's cross-section beside the void's own, much alike."""
    S = GS; R = S.rooms()
    qx, qh = R["qc"]
    q = S.P(qx, qh + 2)
    bv, bvc = S.big_void()
    els = []
    for d0, (x0, y0) in enumerate(((q[0] - 6, q[1] + 6), (q[0] + 6, q[1] + 6), (S.P(4, 1)[0] - 18, 734))):
        base_a = math.atan2(bvc[1] - y0, bvc[0] - x0)
        for i in range(7):
            a = base_a + math.radians((i - 3) * 3.4)
            L = math.hypot(bvc[0] - x0, bvc[1] - y0) + (30 if abs(i - 3) <= 1 else -40)
            els.append({"k": "line", "p": [[x0, y0], [r1(x0 + math.cos(a) * L), r1(y0 + math.sin(a) * L)]], "c": BLUE, "w": 2 if abs(i - 3) <= 1 else 1.1,
                        "op": .85 if abs(i - 3) <= 1 else .4, "keepop": True, "in": round(2.8 + .4 * d0 + .05 * i, 2), "fx": "draw", "dur": .8})
    els += [dict(bv, **{"in": 4.8, "dur": 1.0}), glow(bvc[0], bvc[1], 90, 4.9, .8, "blue"),
            label(bvc[0] - 20, bvc[1] - 54, "the Big Void", 5.6, ICE, 30)]
    # the buses (s15): 30 m along the void, to scale (4.2 units a metre), each 10 m by 3 m
    a = math.radians(26)
    ca, sa = math.cos(a), math.sin(a)
    m = 4.2
    P = lambda u, v: [r1(bvc[0] + (u * ca + v * sa) * m), r1(bvc[1] + (-u * sa + v * ca) * m)]
    for k in range(3):
        u0 = -15 + 10 * k
        at = round(9.4 + .3 * k, 2)
        els += [{"k": "poly", "p": [P(u0 + .3, -1.6), P(u0 + 9.7, -1.6), P(u0 + 9.7, 1.4), P(u0 + .3, 1.4)], "fill": AMBER, "c": "#1a1511", "w": 1, "in": at, "fx": "pop"},
                {"k": "poly", "p": [P(u0 + 1.2, -.9), P(u0 + 8.8, -.9), P(u0 + 8.8, .1), P(u0 + 1.2, .1)], "fill": "#3a3128", "c": "none", "w": 0, "in": at, "fx": "pop"}]
    els += [label(bvc[0] + 36, bvc[1] - 52, "30 m or more", 8.0, AMBER, 28, "start")]
    # cross-sections side by side (end-on, 4.2 units a metre): the Gallery's (2.1 m at the floor, 8.6 m tall, stepped) and the void's
    def prof(cx, by, c, style, at, m=10.0):
        steps = 7; w0, w1, h = 2.1, 1.05, 8.6
        pts = []
        for k in range(steps + 1):
            w = w0 - (w0 - w1) * k / steps
            pts += [[r1(cx - w / 2 * m), r1(by - h * k / steps * m)], [r1(cx - w / 2 * m), r1(by - h * (k + 1) / steps * m)]]
        right = [[r1(2 * cx - x), y] for x, y in pts[::-1]]
        return {"k": "poly", "p": pts[:-1] + right[1:], "fill": "rgba(245,236,220,.08)" if style == "known" else "rgba(159,208,255,.12)", "c": c, "w": 2, "style": style, "in": at, "fx": "rise"}
    gx, gyb = r1(bvc[0] - 150), r1(bvc[1] - 40)
    els += [box(gx - 50, gyb - 112, 132, 150, "rgba(13,11,9,.75)", "rgba(255,236,206,.3)", 1.5, 10, 11.8, fx="pop"),
            prof(gx - 8, gyb, BONE, "known", 12.0), prof(gx + 40, gyb, BLUE, "inferred", 12.5),
            label(gx + 16, gyb + 30, "alike", 12.8, ICE, 24)]
    return els, bvc


def s16_sigma():
    """s16: each signal against the bar physicists set before they say 'discovery' (5 sigma): plates above 10 (13.7 and 12.7),
    strips 5 to 10 by slice, gas 5.8; each bar ticks green as it crosses the line."""
    y0, k = 740, 46                           # 46 units per sigma
    Y = lambda sg: r1(y0 - sg * k)
    els = [line([[300, y0], [1500, y0]], .2, BONE, 2.5, dur=.6), line([[300, Y(5)], [1500, Y(5)]], .5, AMBER, 3, "inferred", .8),
           label(1510, Y(5) + 10, "discovery bar", .9, AMBER, 30, "start"), label(1510, Y(5) + 44, "5 sigma", 1.0, DIM, 24, "start")]
    def bar(x, top, at, c=BLUE, w=120, rng=None):
        out = [box(x - w / 2, Y(top), w, r1(y0 - Y(top)), c, r=6, at=at, fx="fill", dur=1.0)]
        f = 5 / top
        tcross = at + 1.0 * (1 - (1 - f) ** (1 / 3))
        out.append(_check(x + w / 2 + 30, Y(5) - 22, 14, round(tcross + .05, 2)))
        return out
    els += bar(560, 10.2, 1.3) + [arrow([[560, Y(10.2)], [560, Y(13.4)]], 2.3, BLUE, 4, "known", .6, False), label(620, Y(12.6), "13.7", 2.6, ICE, 30, "start"),
                                  label(560, y0 + 40, "plates", 1.2, DIM, 28)]
    els += [box(840, Y(10), 120, r1(Y(5) - Y(10)), "rgba(120,170,215,.55)", BLUE, 1.5, 6, 2.6, fx="fill", dur=1.0)] + bar(900, 5.0, 2.0) + [
            label(900, Y(10) - 16, "5 to 10", 3.4, ICE, 28), label(900, y0 + 40, "strips", 2.0, DIM, 28)]
    els += bar(1240, 5.8, 2.9) + [label(1240, Y(5.8) - 16, "5.8", 3.8, ICE, 28), label(1240, y0 + 40, "gas", 2.9, DIM, 28)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s17_shape():
    """s17: the void close up above the Gallery: its outline 'morphs' (each option fades under a veil of the stone's colour as the
    next draws): one long level space, two shorter ones, one sloping space; 'shape unknown'."""
    m = 14.0
    a = math.radians(26)
    G0 = (520, 800)                                            # the Gallery's lower end (panel), rising at 26 degrees
    P = lambda u, v: [r1(G0[0] + u * m * math.cos(a) - v * m * math.sin(a)), r1(G0[1] - u * m * math.sin(a) - v * m * math.cos(a))]
    gal = [P(0, 0), P(46.7, 0), P(46.7, 8.6), P(0, 8.6)]
    STONE = "#3b2f24"
    els = [box(-50, -50, 1900, 1100, STONE, r=0, at=-1),
           {"k": "poly", "p": gal, "fill": "#0d0b09", "c": BONE, "w": 2, "in": -1}]
    for k in range(1, 7):
        els.append(line([P(0, 8.6 * k / 7), P(46.7, 8.6 * k / 7)], -1, "rgba(245,236,220,.25)", 1, draw=False))
    els += [label(P(36, 0)[0] + 40, P(36, 0)[1] + 46, "Grand Gallery", .3, BONE, 30, "start")]
    zc = P(29, 19.5)
    base_v = [P(14, 16), P(44, 16), P(44, 23), P(14, 23)]
    els += [{"k": "poly", "p": base_v, "fill": "rgba(159,208,255,.16)", "c": BLUE, "w": 2.4, "style": "inferred", "in": .4}]
    ytop = P(46, 24)[1] - 150
    b0, b1 = P(2, 11.5), P(56, 11.5)
    veil = [b0, b1, [b1[0], r1(b1[1] - 420)], [b0[0], r1(b0[1] - 420)]]
    hw, hh = 15 * m * math.cos(a), 6 * m
    level = [[r1(zc[0] - hw), r1(zc[1] - 25 + hh / 2)], [r1(zc[0] + hw), r1(zc[1] - 25 + hh / 2)], [r1(zc[0] + hw), r1(zc[1] - 25 - hh / 2)], [r1(zc[0] - hw), r1(zc[1] - 25 - hh / 2)]]
    opts = [(3.4, [level]),
            (4.6, [[P(12, 17), P(25, 17), P(25, 24), P(12, 24)], [P(31, 15), P(45, 15), P(45, 22), P(31, 22)]]),
            (5.8, [[P(14, 16), P(44, 16), P(44, 23), P(14, 23)]])]
    for at, polys in opts:
        els.append({"k": "poly", "p": veil, "fill": STONE, "c": "none", "w": 0, "op": .86, "keepop": True, "in": at, "dur": .35})
        for pp in polys:
            els.append({"k": "poly", "p": pp, "fill": "rgba(159,208,255,.14)", "c": BLUE, "w": 2.8, "style": "inferred", "in": round(at + .15, 2), "fx": "rise"})
    els += [label(zc[0], r1(ytop + 60), "shape unknown", 6.6, ICE, 32)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s18_relieve():
    """s18: left, the Gallery's stepped (corbelled) roof, end on, with heavy arrows of weight from the stone above; a gap opens
    above the roof and the arrows bend round it ('relieving space?', lilac, dashed). Right: a brick doorway with an arch, small
    arrows flowing round it. 'weight', 'arch'."""
    m = 40.0                                                   # 40 units a metre (end-on view of the Gallery)
    cx, fy = 460, 780
    steps = 7
    left = []
    for k in range(steps + 1):
        w = 2.06 - (2.06 - 1.04) * k / steps
        left += [[r1(cx - w / 2 * m), r1(fy - 8.6 * k / steps * m)], [r1(cx - w / 2 * m), r1(fy - 8.6 * (k + 1) / steps * m)]]
    top_y = r1(fy - 8.6 * m)
    right = [[r1(2 * cx - x), y] for x, y in left[::-1]]
    els = [box(130, 120, 660, 680, "url(#k-blocks)", r=8, at=-1, op=.85), box(130, 120, 660, 680, "rgba(13,11,9,.25)", r=8, at=-1),
           {"k": "poly", "p": left[:-1] + right[1:], "fill": "#0d0b09", "c": BONE, "w": 2, "in": -1}]
    for k, x in enumerate((cx - 140, cx, cx + 140)):
        els.append(arrow([[x, 130], [x, top_y - 170]], round(.6 + .15 * k, 2), AMBER, 6, "known", .6, False))
    els += [label(cx + 230, 160, "weight", 1.2, AMBER, 32, "start")]
    gap = box(cx - 120, top_y - 150, 240, 110, "rgba(13,11,9,.9)", LILAC, 2.4, 6, 3.6, fx="pop", style="inferred")
    els += [gap]
    for k, sg in enumerate((-1, 1)):
        els.append(arrow([[cx + sg * 70, top_y - 165], [cx + sg * 150, top_y - 110], [cx + sg * 190, top_y + 20], [cx + sg * 200, fy - 40]], round(4.3 + .2 * k, 2), AMBER, 4, "known", 1.0))
    els += [label(cx, top_y - 190, "relieving space?", 4.8, LILAC, 30)]
    # the arch
    ax, ay, aw, ah = 1300, 780, 230, 300
    bricks = []
    for r in range(13):
        for c in range(9):
            x = 1020 + c * 64 + (32 if r % 2 else 0); y = 780 - (r + 1) * 46
            if x > 1580:
                continue
            bricks.append(box(x, y, 60, 42, "#9c5a3c", "#c98a64", 1, 2, 5.6, op=.9))
    els += [{"k": "group", "els": bricks, "clip": [1020, 182, 576, 598, 8], "in": 5.6, "dur": .6}]
    arch = [[ax - aw / 2, ay]] + [[r1(ax - aw / 2 * math.cos(math.radians(t))), r1(ay - ah + aw / 2 - aw / 2 * math.sin(math.radians(t)))] for t in range(0, 181, 15)] + [[ax + aw / 2, ay]]
    els += [{"k": "poly", "p": arch, "fill": "#0d0b09", "c": "#e8c9a0", "w": 3, "in": 5.9, "fx": "pop"}]
    for k, sg in enumerate((-1, 1)):
        els.append(arrow([[ax + sg * 20, 200], [ax + sg * 60, ay - ah - 40], [ax + sg * (aw / 2 + 40), ay - ah + 90], [ax + sg * (aw / 2 + 50), ay - 30]], round(7.0 + .2 * k, 2), AMBER, 4, "known", 1.0))
    els += [label(ax, 160, "arch", 6.4, AMBER, 32)]
    return {"base": "dark", "stars": 20, "cam": [1, 889, 500], "els": els}


def s19_nfc():
    """s19: the north face in section, close (19 units a metre): the old entrance, the great gabled blocks over it; behind them a
    corridor draws itself level into the stone. Then: the corridor as an iso box, 2 x 2 x 9 m to scale, a person 1.7 m at its
    mouth; '9 m', '2 m'."""
    m = 19.0
    X = lambda x: r1(100 + x * m)
    Y = lambda h: r1(790 - (h - 8) * m)
    face = lambda h: h / math.tan(SLOPE)
    hmax = 38.0
    body = [[X(face(8)), Y(8)], [X(face(hmax)), Y(hmax)], [X(44), Y(hmax)], [X(44), Y(8)]]
    els = [{"k": "poly", "p": body, "fill": "url(#k-blocks)", "c": "none", "w": 0, "in": -1},
           {"k": "poly", "p": body, "fill": "rgba(0,0,0,.18)", "c": "none", "w": 0, "in": -1},
           line([[X(face(8)), Y(8)], [X(face(hmax)), Y(hmax)]], -1, "#f2dcb4", 2.6, draw=False),
           line([[X(face(hmax)), Y(hmax)], [X(44), Y(hmax)], [X(44), Y(8)], [X(face(8)), Y(8)]], -1, "rgba(242,220,180,.5)", 1.6, "inferred", draw=False),
           label(X(face(30)) - 24, Y(30), "north face", -1, DIM, 24, "end")]
    # the descending passage from the entrance (17 m up, 26.5 degrees down into the rock)
    e0 = (face(17.0), 17.0)
    d = math.radians(26.5)
    e1 = (e0[0] + 17 * math.cos(d), e0[1] - 17 * math.sin(d))
    els += [_poly([[X(e0[0]), Y(e0[1])], [X(e1[0]), Y(e1[1])], [X(e1[0]), Y(e1[1] - 1.2)], [X(e0[0] + .5), Y(e0[1] - 1.2)]], "#0d0b09", BONE, 1.6, -1),
            label(X(e0[0]) - 30, Y(e0[1]) + 8, "old entrance", 4.6, BONE, 26, "end")]
    # the North Face Corridor: 20 m up, 0.8 m behind the chevrons, 9 m long, 2 m wide, about 2 m high, a gabled roof
    h = 20.0; x0 = face(h) + .8
    nfc = [[X(x0), Y(h)], [X(x0 + 9), Y(h)], [X(x0 + 9), Y(h + 2)], [X(x0 + 4.5), Y(h + 2.9)], [X(x0), Y(h + 2)]]
    els += [{"k": "poly", "p": nfc, "fill": "#0d0b09", "c": BLUE, "w": 2.6, "in": 6.2, "fx": "draw", "dur": 1.2}, glow(X(x0 + 4.5), Y(h + 1.2), 110, 6.8, .7, "blue"),
            label(X(x0 + 9) + 16, Y(h + 1) + 10, "corridor", 7.2, ICE, 28, "start")]
    # the chevrons: two gabled pairs of great blocks over the entrance, in front of the corridor (schematic)
    for k, (h0, sp) in enumerate(((19.2, 3.0), (22.2, 3.4))):
        xm = face(h0) + sp + .3
        for sg in (-1, 1):
            els.append(_poly([[X(xm), Y(h0 + sp * .8)], [X(xm + sg * sp), Y(h0)], [X(xm + sg * sp), Y(h0 - .9)], [X(xm), Y(h0 + sp * .8 - .9)]], "#d8c4a0", "#fff1d8", 1.5, -1, op=.92))
    els += [label(X(face(26)) - 24, Y(26.4), "gabled blocks", 3.6, AMBER, 26, "end")]
    # the corridor as a box, to scale (34 units a metre), a person at its mouth
    items = [{"t": "box", "x": 0, "z": 0, "y": 0, "w": 9, "d": 2, "h": 2.1, "c": "#3d5566", "edge": "#cfe6ff"},
             {"t": "ext", "axis": "z", "z": 0, "y": 2.1, "at": 0, "d": 9, "prof": [[-1, 0], [1, 0], [0, .8]], "c": "#4a6476", "edge": "#cfe6ff"},
             {"t": "person", "x": -5.6, "y": 0, "z": .3, "h": 1.7, "color": "#e8d6b8"},
             {"t": "line", "p": [[-4.5, 0, 1.6], [4.5, 0, 1.6]], "c": BONE, "w": 2}, {"t": "line", "p": [[4.5, 0, -1], [4.5, 0, 1]], "c": BONE, "w": 2}]
    bx = iso(items, 1340, 520, 38, -30, 0, el=.34, at=10.4, fx="rise")
    els += [bx, label(1340, 300, "2 m by 2 m", 12.2, BONE, 30)]
    p9 = P3(bx, (0, 0, 2.6)); p2 = P3(bx, (5.6, 0, 0))
    els += [label(p9[0], p9[1] + 40, "9 m", 11.6, BONE, 30)]
    return {"base": "dark", "stars": 50, "cam": [1, 889, 500], "els": els}


def s20_probe():
    """s20: the chevron blocks face on: a radar sled crosses the face, waves go in and echo back; two ultrasound probes pulse; a
    crosshair settles on a joint. Then (closer, at 'Then a camera thinner than a pencil'): a pencil beside the joint for scale, the
    endoscope cable (thinner) snakes in through the joint, its lamp glows inside."""
    els = [box(80, 130, 1620, 660, "url(#k-blocks)", r=8, at=-1), box(80, 130, 1620, 660, "rgba(13,11,9,.15)", r=8, at=-1)]
    cx = 889
    def gable(y0, sp, th):
        out = []
        for sg in (-1, 1):
            out.append(_poly([[cx, y0 - sp * .62], [cx + sg * sp, y0], [cx + sg * sp, y0 + th], [cx, y0 - sp * .62 + th]], "#d8c4a0", "#fff1d8", 2, -1))
        return out
    els += gable(380, 360, 80) + gable(560, 300, 70)
    els += [box(cx - 70, 640, 140, 150, "#0d0b09", BONE, 2, 2, -1)]
    # the radar sled and its waves; two ultrasound probes
    for k, x in enumerate((420, 560)):
        els.append(box(x - 40, 760 - 34, 80, 34, "#3d5566", BLUE, 2, 6, round(.3 + .4 * k, 2), op=.45 if k == 0 else None, fx="pop"))
    els += [arrow([[400, 712], [700, 712]], .4, BLUE, 2, "inferred", .8, False)]
    for j, r in enumerate((40, 80, 120)):
        els.append({"k": "line", "p": ellipse(560, 726, r, r * .8, 12, 200, 340), "c": BLUE, "w": 2.4, "curve": True, "in": round(1.0 + .2 * j, 2), "fx": "draw", "dur": .4})
    for j, r in enumerate((100, 60)):
        els.append({"k": "line", "p": ellipse(560, 726, r, r * .8, 12, 200, 340), "c": AMBER, "w": 2.4, "curve": True, "in": round(1.8 + .2 * j, 2), "fx": "draw", "dur": .4})
    for k, (x, y) in enumerate(((1240, 420), (1330, 520))):
        els += [line([[x + 60, y - 60], [x, y]], round(1.0 + .3 * k, 2), "#cfd6dc", 8, dur=.4), dot(x, y, 7, BLUE, round(1.3 + .3 * k, 2))]
        els += [ring(x, y, r, round(1.5 + .3 * k + .15 * j, 2), BLUE, 2, dur=.3) for j, r in enumerate((16, 30))]
    jx, jy = 1034, 452                                         # a joint behind the lower gable
    els += [line([[jx, jy - 120], [jx, jy + 60]], -1, "#2a1f16", 4, draw=False)]
    els += [ring(jx, jy, 40, 2.4, AMBER, 3, dur=.5), line([[jx - 60, jy], [jx - 18, jy]], 2.6, AMBER, 3, dur=.3), line([[jx + 18, jy], [jx + 60, jy]], 2.6, AMBER, 3, dur=.3),
            line([[jx, jy - 60], [jx, jy - 18]], 2.7, AMBER, 3, dur=.3), line([[jx, jy + 18], [jx, jy + 60]], 2.7, AMBER, 3, dur=.3)]
    # close on the joint (shot 69): the pencil (7 mm) and the cable (5 mm, about 2.4 units a millimetre)
    pk = 2.4
    py = jy + 34
    pen = [_poly([[jx - 250, py - 3.5 * pk], [jx - 40, py - 3.5 * pk], [jx - 40, py + 3.5 * pk], [jx - 250, py + 3.5 * pk]], "#e8c35a", "#7a5a14", 1.2, 4.0, fx="pop"),
           _poly([[jx - 40, py - 3.5 * pk], [jx - 18, py], [jx - 40, py + 3.5 * pk]], "#e8cfa0", "#7a5a14", 1.2, 4.0, fx="pop"),
           label(jx - 145, py + 34, "pencil", 4.3, "#e8c35a", 24)]
    cab = [line([[jx + 220, jy + 150], [jx + 130, jy + 110], [jx + 60, jy + 20], [jx + 10, jy - 10], [jx - 1, jy - 30]], 4.8, "#1a1511", 5 * pk + 3, dur=1.2, curve=True),
           line([[jx + 220, jy + 150], [jx + 130, jy + 110], [jx + 60, jy + 20], [jx + 10, jy - 10], [jx - 1, jy - 30]], 4.8, "#c9ad85", 5 * pk, dur=1.2, curve=True),
           label(jx + 150, jy + 160, "endoscope", 5.6, "#c9ad85", 24, "start"), glow(jx - 6, jy - 46, 60, 6.0, .8, "lamp")]
    return {"base": "dark", "cam": [1, 889, 500], "els": els + pen + cab}, [2.4, jx, jy + 20]


def s21_corridor():
    """s21: the endoscope's round view down an empty corridor with a gabled roof, lamp-lit, dark at the far end; 'empty'."""
    cx, cy, R = 889, 470, 330
    return {"base": "dark", "cam": [1, 889, 500], "els": corridor_view(cx, cy, R) + [label(cx, cy + R + 50, "empty", 1.2, BONE, 28)]}


def s22_both():
    """s22: the x-ray model with both spaces: the corridor solid, a green tick, 'seen'; the void dashed and glowing, a small '?',
    'not yet entered'."""
    R = gp_parts(void=True, nfc=True)
    base = iso(R["gp"] + R["rest"] + R["gg"] + R["kc"] + R["qc"] + R["bv"] + R["nfc"] + iso3d.ground(140, grid=35), 889, 760, 3.6, -28, .4, el=.26, at=-1)
    vc, nc = void_centre(), nfc_centre()
    T = 4.0
    els = [glow(889, 560, 620, -1, .16, "lamp"), base,
           ov(base, [{"t": "line", "p": [[nc[0] - 6, nc[1] + 9, 0], [nc[0] - 3, nc[1] + 6, 0], [nc[0] + 4, nc[1] + 13, 0]], "c": GREEN, "w": 5}, ilab(nc[0] - 2, nc[1] + 15, 0, "seen", GREEN, -14)], 4.6),
           ov(base, [{"t": "q", "x": vc[0], "y": vc[1] + 1, "z": 0, "size": 54, "c": ICE}, ilab(vc[0], vc[1] + 12, 0, "not yet entered", ICE, -20)], 6.4)]
    cx, cy = P3(base, ((vc[0] + nc[0]) / 2, 40, 0), T)
    return {"base": "dark", "stars": 70, "cam": [1.45, cx, cy], "els": els}


# ================================================================ chapter 2: Pillars under Khafre
def s24_stack():
    """s24 (with s23 folded in: the card holds 'Next door stands the pyramid of Khafre...'): Khafre cut open, the Great Pyramid
    beside it, both to scale; '143 m' up its edge; then four and a half Khafres stacked one below another into the rock (dashed),
    '× 4½', and '648 m' with a ring at the bottom."""
    s = kcut(at=-1, khufu=True)
    s["els"] += [label(KX, KGY - KH - 22, "Khafre", .3, AMBER, 30), label(KX + 330, KGY - 146.6 * KPX - 20, "Great Pyramid", .5, DIM, 24),
                 {"k": "dim", "x1": KX - KB - 26, "y1": KGY, "x2": KX - KB - 26, "y2": KGY - KH, "t": "", "c": AMBER, "in": .6, "fx": "draw", "dur": .6},
                 label(KX - KB - 40, KGY - KH / 2 + 10, "143 m", .9, AMBER, 30, "end")]
    for k in range(4):
        y0, y1 = KGY + KH * k, KGY + KH * (k + 1)
        s["els"].append(_poly([[KX - KB, y1], [KX, y0], [KX + KB, y1]], "rgba(242,220,180,.07)", BONE, 2, round(1.7 + .5 * k, 2), style="inferred", op=.85, fx="rise"))
    y0 = KGY + KH * 4
    s["els"] += [_poly([[KX - KB / 2, y0 + KH / 2], [KX, y0], [KX + KB / 2, y0 + KH / 2]], "rgba(242,220,180,.07)", BONE, 2, 3.7, style="inferred", op=.85, fx="rise"),
                 label(KX - KB - 30, kD(330), "× 4½", 4.4, AMBER, 48, "end", st="serif"),
                 line([[KX - 60, kD(648)], [KX + 60, kD(648)]], 6.2, BONE, 4, dur=.3), ring(KX, kD(648) - 6, 50, 6.4, AMBER, 3, dur=.7),
                 label(KX + 90, kD(648) - 4, "648 m", 6.3, BONE, 48, "start", st="serif")]
    return s


def s25_claim():
    """s25: the same clean cut: a satellite crosses the sky top right, radar arcs reach the plateau; eight lilac dotted shafts draw
    down in a row, spiral paths round them, 'claimed'; then two lilac dotted cubes far below, 80 m a side to the same scale."""
    s = kcut(at=-1)
    s["els"] += [{"k": "dim", "x1": 600, "y1": KGY + 4, "x2": 600, "y2": kD(648), "t": "", "c": DIM, "in": .3},
                 label(580, kD(330) + 10, "648 m", .4, DIM, 30, "end")]
    sx, sy = 1180, 140
    s["els"] += _satellite(sx, sy, 6.8, .9)
    ang = math.degrees(math.atan2(KGY - sy, KX - sx))
    s["els"] += [line([[sx - 10, sy + 20], [KX - 110, KGY - 2]], 7.4, BLUE, 2, "inferred", .7), line([[sx, sy + 24], [KX + 110, KGY - 2]], 7.4, BLUE, 2, "inferred", .7)]
    s["els"] += [{"k": "line", "p": ellipse(sx, sy + 20, r, r, 10, ang - 9, ang + 9), "c": BLUE, "w": 2.6, "curve": True, "in": round(7.6 + .2 * j, 2), "fx": "draw", "dur": .4}
                 for j, r in enumerate((120, 240, 360))]
    s["els"] += [glow(KX, KGY, 160, 8.0, .45, "blue"), label(sx + 110, sy + 10, "satellite radar", 7.2, BLUE, 28, "start")]
    s["els"] += kshafts(8.6) + [label(KX + 110, kD(300), "claimed", 10.2, LILAC, 32, "start")]
    s["els"] += kcubes(12.4) + [label(KX + 90, kD(610), "80 m", 13.4, LILAC, 28, "start")]
    return s


def s26_tremble():
    """s26: a satellite over a cut of ground: its radar pulse goes down in blue arcs and bounces straight back off the surface; the
    stone below stays dark. Then a long strip of the surface: small tremors run in from both edges, the surface line shivers, a
    seismograph trace runs along the top."""
    gy = 480
    sx, sy = 889, 190
    els = _satellite(sx, sy, .3, 1.1)
    for j, r in enumerate((80, 170, 260)):
        els.append({"k": "line", "p": ellipse(sx, sy + 30, r * 1.3, r, 16, 60, 120), "c": BLUE, "w": 3, "curve": True, "in": round(2.6 + .25 * j, 2), "fx": "draw", "dur": .4})
    for j, r in enumerate((200, 120)):
        els.append({"k": "line", "p": ellipse(sx, gy, r * 1.3, r, 16, 240, 300), "c": AMBER, "w": 3, "curve": True, "in": round(3.8 + .25 * j, 2), "fx": "draw", "dur": .4})
    els += [line([[sx - 30, gy + 20], [sx - 30, gy + 120]], 4.4, BLUE, 2, "inferred", .4), line([[sx - 50, gy + 125], [sx - 10, gy + 125]], 4.7, RED, 4, dur=.3)]
    # tremors: little waves running in from both edges; the surface shivers; a seismograph trace
    for k in range(6):
        for sg, x0 in ((1, 120), (-1, 1660)):
            x = x0 + sg * 110 * k
            pts = [[r1(x + sg * u * 8), r1(gy - 5 * math.sin(u * 1.6))] for u in range(11)]
            els.append({"k": "line", "p": pts, "c": "#ffe2a8", "w": 2.4, "curve": True, "in": round(7.4 + .18 * k, 2), "fx": "draw", "dur": .3})
    els.append({"k": "line", "p": [[r1(x), r1(gy + 2.5 * math.sin(x / 23.0))] for x in range(80, 1710, 15)], "c": "#ffe2a8", "w": 1.6, "curve": True, "in": 8.6, "op": .8, "keepop": True})
    tr = [[r1(130 + u * 4), r1(195 + (14 * math.sin(u * .9) * math.sin(u * .13)) * (.4 + .6 * abs(math.sin(u * .05))))] for u in range(125)]
    els += [box(110, 140, 540, 110, "rgba(18,13,10,.85)", "rgba(255,236,206,.35)", 1.5, 10, 7.2, fx="pop"), line([[130, 195], [630, 195]], 7.3, "rgba(255,236,206,.25)", 1, draw=False),
            {"k": "line", "p": tr, "c": GREEN, "w": 2, "in": 7.6, "fx": "draw", "dur": 3.0}]
    return {"base": "section", "tod": "night", "ground": gy, "lx": 40, "cam": [1, 889, 500],
            "layers": [{"d": 0, "c": "#8a6e50", "t": ""}, {"d": 40, "c": "#5f4c39", "t": ""}, {"d": 200, "c": "#463a2f", "t": ""}], "els": els}


def fist(x, y, sg, at):
    """A fist about to knock, seen from the side (knuckles towards the wall on side sg), with its forearm."""
    P = lambda u, v: [r1(x + sg * u), r1(y + v)]
    hand = [P(0, -30), P(-8, -38), P(-70, -40), P(-84, -30), P(-84, 34), P(-70, 42), P(-8, 40), P(0, 30), P(4, 0)]
    arm = [P(-80, -24), P(-230, -30), P(-230, 26), P(-80, 26)]
    return [{"k": "poly", "p": arm, "fill": "rgba(232,184,122,.14)", "c": AMBER, "w": 2.2, "in": at, "fx": "rise"},
            {"k": "poly", "p": hand, "fill": "#3a2c20", "c": AMBER, "w": 2.6, "curve": True, "in": at, "fx": "rise"}] + \
           [line([P(-4, v), P(-40, v)], at, AMBER, 1.6, draw=False, op=.7) for v in (-20, -2, 16)] + [line([P(-30, 30), P(-64, 18)], at, AMBER, 1.6, draw=False, op=.7)]


def s27_knock():
    """s27: two walls side by side; a fist knocks on each: the solid one gives one short dull ring, the hollow one rings in wide
    arcs; 'solid', 'hollow'."""
    els = []
    for k, (x0, hollow) in enumerate(((180, False), (960, True))):
        els += [box(x0, 190, 440, 520, "url(#k-blocks)", "rgba(255,236,206,.5)", 2, 6, .3), box(x0, 190, 440, 520, "rgba(13,11,9,.2)", r=6, at=.3)]
        if hollow:
            els.append(box(x0 + 110, 300, 220, 300, "rgba(13,11,9,.6)", BLUE, 2.4, 6, .8, style="inferred"))
    for k, (x0, at, rings) in enumerate(((180, 5.4, (40,)), (960, 6.4, (40, 80, 120, 160)))):
        kx, ky = x0 + 440 + 6, 450
        els += fist(kx + 4, ky, -1, at)
        for j, r in enumerate(rings):
            els.append({"k": "line", "p": ellipse(kx - 10, ky, r, r * 1.2, 14, 110, 250), "c": BLUE if len(rings) > 1 else DIM, "w": 3 if len(rings) > 1 else 4,
                        "curve": True, "in": round(at + .35 + .18 * j, 2), "fx": "draw", "dur": .35})
        els.append(label(x0 + 220, 760, ("solid", "hollow")[k], at + .2, BONE if k == 0 else ICE, 32))
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


NILE_S = [(33.32, 19.53), (32.8, 19.25), (32.3, 18.9), (31.8, 18.47), (31.55, 18.15), (31.0, 18.08), (30.74, 18.22), (30.55, 18.65), (30.48, 19.17), (30.4, 19.6),
          (30.38, 20.3), (30.55, 20.95), (30.95, 21.45), (31.35, 21.8), (31.75, 22.3), (32.2, 22.7), (32.6, 23.2), (32.85, 23.8), (32.90, 24.09)]


def s28_shuttle():
    """s28: the eastern Sahara (Egypt and northern Sudan): the Space Shuttle's radar track draws across (1981, schematic line);
    along it, buried river valleys appear under the sand, blue and branching."""
    v = View(24, 34, 18, 26, (90, 120, 1600, 680))
    nile = v.line([q for q in NILE_S] + [q for q in NILE[1:]])
    els = [{"k": "map", "land": v.land(), "landc": "#6e5a43", "rivers": [nile], "in": -1}]
    b0, b1 = v.p(25, 22), v.p(31.3, 22)
    els += [line([b0, b1], -1, "rgba(245,236,220,.35)", 1.6, "inferred", draw=False),
            label(v.p(27.2, 23.2)[0], v.p(27.2, 23.2)[1], "Egypt", .2, DIM, 30), label(v.p(26.4, 20.6)[0], v.p(26.4, 20.6)[1], "Sudan", .2, DIM, 30),
            label(v.p(32.4, 21.3)[0], v.p(32.4, 21.3)[1], "Nile", .3, "#9fd0ff", 28, st="ital")]
    t0, t1 = v.p(24.6, 19.1), v.p(33.4, 24.9)
    els += [line([t0, t1], 4.2, GOLD, 3, "inferred", 1.4), label(v.p(30.6, 23.9)[0], v.p(30.6, 23.9)[1] - 20, "Shuttle radar, 1981", 4.8, GOLD, 30)]
    # buried valleys (schematic) under the Selima sand sheet, along the track
    rnd = random.Random(21)
    def branch(x, y, ang, L, depth, at, w):
        out = []
        x1, y1 = x + L * math.cos(ang), y + L * math.sin(ang)
        mid = [r1((x + x1) / 2 + rnd.uniform(-.06, .06)), r1((y + y1) / 2 + rnd.uniform(-.06, .06))]
        out.append({"k": "line", "p": [list(v.p(x, y)), list(v.p(*mid)), list(v.p(x1, y1))], "c": BLUE, "w": w, "curve": True, "in": round(at, 2), "fx": "draw", "dur": .5})
        if depth:
            for da in (-.55, .5):
                out += branch(x1, y1, ang + da + rnd.uniform(-.15, .15), L * .62, depth - 1, at + .3, max(1.4, w * .65))
        return out
    for k, (x, y, ang) in enumerate(((30.2, 22.0, 2.75), (30.0, 22.7, 3.3), (29.9, 21.5, 2.4))):
        els += branch(x, y, ang, .75, 3, 8.0 + .25 * k, 4.4)
    vx, vy = v.p(28.6, 20.9)
    els += [glow(*v.p(29.2, 22.1), 160, 8.2, .4, "blue"), label(vx, vy + 30, "buried valleys", 9.0, BLUE, 30)]
    els += [{"k": "scale", "x": 130, "y": 770, "w": r1(v.km(200)), "t": "200 km", "in": .4}]
    return {"base": "map", "cam": [1, 889, 500], "els": els}


def s29_depth():
    """s29: a depth chart to one scale (0.9 units a metre): the surface near the top, a person on it; a magnifier on the first
    10 m (40 units a metre): 'field', 1 to 2 m; 'lab', 5 m; then a lilac column drops 648 m: 'over 100 times deeper'."""
    sy, k = 180, .9
    cx = 520
    els = [line([[160, sy], [900, sy]], .2, "#ffe2a8", 3, dur=.6), box(160, sy, 740, 600, "url(#k-sand)", r=0, at=.2, op=.35),
           person(cx - 30, sy, 1.7 * k * 6, .3, "#e8d6b8")]
    # the magnifier (40 units a metre)
    mx, my, mr, M = 1260, 440, 300, 40
    top = my - mr + 96
    els += [box(cx - 12, sy - 2, 24, 12, "none", "#ffe2a8", 2, 2, .4), line([[cx + 12, sy], [mx - mr * .7, my - mr * .7]], .5, "rgba(255,226,168,.5)", 2, dur=.4),
            line([[cx + 12, sy + 10], [mx - mr * .7, my + mr * .7]], .5, "rgba(255,226,168,.5)", 2, dur=.4),
            {"k": "group", "clip": [mx - mr, my - mr, 2 * mr, 2 * mr, mr], "bg": "#2a2018", "in": .5, "els": [
                {"k": "rect", "x": mx - mr, "y": top, "w": 2 * mr, "h": 2 * mr, "fill": "#7a6248", "c": "none", "sw": 0},
                {"k": "rect", "x": mx - mr, "y": top, "w": 2 * mr, "h": 2 * mr, "fill": "url(#k-speck)", "c": "none", "sw": 0},
                {"k": "line", "p": [[mx - mr, top], [mx + mr, top]], "c": "#ffe2a8", "w": 3}]},
            {"k": "circle", "x": mx, "y": my, "r": mr, "c": "#ffe2a8", "w": 4, "in": .5},
            person(mx - 120, top, 1.7 * M, .8, "#e8d6b8")]
    for m_ in range(0, 11, 2):
        y = top + m_ * M
        if y < my + mr - 20:
            els += [line([[mx + 150, y], [mx + 170, y]], .9, DIM, 2, draw=False), label(mx + 180, y + 8, "%d m" % m_, .9, DIM, 24, "start")]
    els += [box(mx - mr + 30, top + 1 * M, 2 * mr - 220, M, "rgba(159,208,255,.45)", BLUE, 1.5, 3, 1.4, fx="fill", dur=.5),
            label(mx - 40, top + 1.5 * M + 9, "field", 1.8, ICE, 28)]
    els += [line([[mx - mr + 40, top + 5 * M], [mx + 130, top + 5 * M]], 3.3, AMBER, 3, "inferred", .5), label(mx - 40, top + 5 * M - 14, "lab", 3.6, AMBER, 28)]
    # the claim's depth, to the chart's scale
    els += [line([[cx, sy + 2], [cx, r1(sy + 648 * k)]], 5.8, LILAC, 26, dur=1.6, op=.75), line([[cx - 30, r1(sy + 648 * k)], [cx + 30, r1(sy + 648 * k)]], 7.3, LILAC, 3, dur=.3),
            label(cx - 40, r1(sy + 648 * k) - 10, "648 m", 7.4, LILAC, 30, "end"),
            label(cx + 40, 520, "over 100 times deeper", 7.6, LILAC, 30, "start")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s30_faint():
    """s30: left, a wave rises from the bottom of the deep column to the surface, its wiggle shrinking to a flat line; a meter on
    the surface reads nothing: 'too faint?'. Right: Khafre small, a gate with a padlock drawn across its base: 'no permission',
    'no basis'."""
    sy, cx = 200, 420
    els = [line([[120, sy], [800, sy]], .2, "#ffe2a8", 3, dur=.5), box(120, sy, 680, 580, "#3f3328", r=0, at=.2, op=.8),
           line([[cx, sy + 4], [cx, 770]], .3, LILAC, 20, "claimed", dur=.6, op=.5)]
    pts = []
    for k in range(120):
        y = 770 - k * (770 - sy - 10) / 119
        a = 34 * (1 - k / 119) ** 2.2
        pts.append([r1(cx + 90 + a * math.sin(k * .55)), r1(y)])
    els += [{"k": "line", "p": pts, "c": BLUE, "w": 3, "curve": True, "in": 3.6, "fx": "draw", "dur": 2.0}]
    gx, gy_ = cx + 90, sy - 10
    els += [{"k": "line", "p": ellipse(gx, gy_, 50, 50, 18, 180, 360), "c": BONE, "w": 3, "curve": True, "in": 5.4, "fx": "draw", "dur": .4},
            line([[gx, gy_], [gx - 46, gy_ - 6]], 5.6, AMBER, 3, dur=.3), dot(gx, gy_, 6, BONE, 5.6),
            label(gx + 70, gy_ - 30, "too faint?", 6.2, BLUE, 30, "start")]
    # Khafre, the gate
    kx, kb, kh = 1330, 300, 200
    by = 640
    els += [_poly([[kx - kb / 2, by], [kx, by - kh], [kx + kb / 2, by]], "url(#k-blocks)", "#f2dcb4", 2, .4), _poly([[kx, by - kh], [kx + kb / 2, by], [kx, by]], "rgba(0,0,0,.28)", at=.4),
            line([[kx - 300, by], [kx + 300, by]], .4, "rgba(255,226,190,.5)", 2, draw=False), label(kx, by - kh - 20, "Khafre", .6, AMBER, 28)]
    g0, g1 = kx - 230, kx + 230
    els += [line([[g0, by + 6], [g0, by - 120]], 12.6, BONE, 6, dur=.3), line([[g1, by + 6], [g1, by - 120]], 12.6, BONE, 6, dur=.3)]
    els += [line([[g0, by - 110 + 26 * j], [g1, by - 110 + 26 * j]], round(12.8 + .1 * j, 2), BONE, 3.5, dur=.6) for j in range(5)]
    px, py = kx, by - 40
    els += [{"k": "line", "p": ellipse(px, py - 30, 22, 26, 14, 180, 360), "c": "#cbbca8", "w": 7, "curve": True, "in": 13.3, "fx": "draw", "dur": .4},
            box(px - 32, py - 32, 64, 56, "#8c7152", "#f2dcb4", 2.5, 8, 13.2, fx="pop"), dot(px, py - 10, 7, INK, 13.4)]
    els += [label(kx, by + 60, "no permission", 13.6, RED, 32), label(kx, by + 104, "no basis", 15.2, RED, 32)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def alvarez_geo():
    """Khafre in section (3.8 units a metre) and the half-angle of a cone from its base centre that covers a fifth of the section."""
    m, cx, gy = 3.8, 700, 760
    H, Bh = 143.5, 215.3 / 2
    k = Bh / H
    def frac(th):
        t = math.tan(th); ys = H * k / (t + k)
        return (t * ys * ys + k * (H - ys) ** 2) / (k * H * H)
    lo, hi = .01, 1.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if frac(mid) < .2:
            lo = mid
        else:
            hi = mid
    th = (lo + hi) / 2
    t = math.tan(th); ys = H * k / (t + k)
    P = lambda x, y: [r1(cx + x * m), r1(gy - y * m)]
    cone = [P(0, 0), P(ys * t, ys), P(0, H), P(-ys * t, ys)]
    return m, cx, gy, H, Bh, P, cone


def khafre_section(P, H, Bh):
    return [_poly([P(-Bh, 0), P(0, H), P(Bh, 0)], "url(#k-blocks)", "#f2dcb4", 2, -1), _poly([P(0, H), P(Bh, 0), P(0, 0)], "rgba(0,0,0,.25)", at=-1),
            box(*P(-7, 0), 14 * 3.8, 5 * 3.8, "#0d0b09", BONE, 1.6, 2, -1)]


def s31_alvarez():
    """s31: Khafre in section, the Belzoni Chamber at its base; a detector pops in (1967); a cone of view opens upward. Then tracks
    fill the cone while a counter climbs to 1,000,000+; the cone, about a fifth of the pyramid, is shaded; a green tick and
    'no hidden chambers' inside it."""
    m, cx, gy, H, Bh, P, cone = alvarez_geo()
    els = khafre_section(P, H, Bh) + [label(*P(0, -14), "Belzoni Chamber", 1.0, DIM, 26)]
    els[-1]["y"] = r1(gy + 50)
    d = P(0, 2.4)
    els += [box(d[0] - 16, d[1] - 10, 32, 18, "#3d5566", BLUE, 2, 3, 3.2, fx="pop"), label(d[0] + 120, d[1] - 4, "1967", 3.6, BLUE, 30, "start"),
            line([cone[0], cone[1]], 5.0, BLUE, 2.4, "inferred", .8), line([cone[0], cone[3]], 5.0, BLUE, 2.4, "inferred", .8)]
    rnd = random.Random(11)
    for j in range(22):
        f = rnd.uniform(-1, 1)
        top = [r1(cone[0][0] + f * (cone[1][0] - cone[0][0]) * .98), cone[1][1] if abs(f) > .6 else r1(cone[2][1] + (cone[1][1] - cone[2][1]) * abs(f) / .6)]
        els.append(line([[cone[0][0], cone[0][1] - 8], top], round(8.8 + .05 * j, 2), BLUE, 1.2, dur=.4, op=.6))
    els += [{"k": "poly", "p": cone, "fill": "rgba(159,208,255,.20)", "c": BLUE, "w": 2, "in": 11.2, "dur": .8},
            label(r1(cone[1][0] + 60), r1(cone[1][1] + 40), "about a fifth", 11.6, ICE, 28, "start")]
    for k, (t, at) in enumerate((("10,000", 9.0), ("100,000", 9.6), ("1,000,000+", 10.2))):
        els += [box(1260, 300, 380, 90, "#17120e", "rgba(159,208,255,.6)", 2, 12, at), label(1450, 362, t, round(at + .02, 2), ICE, 50, st="serif")]
    els += [label(1450, 430, "muons counted", 9.0, DIM, 26)]
    cc = P(0, H * .55)
    els += [_check(cc[0] - 6, cc[1] + 6, 18, 13.6), label(cc[0], r1(cc[1] - 40), "no hidden chambers", 14.0, GREEN, 28)]
    return {"base": "dark", "stars": 50, "floor": 760, "cam": [1, 889, 500], "els": els}


def s32_review():
    """s32 + s33: a lilac 'Khafre claim' card heads for the journal and stops short (a red cross); peer review as a gate of three
    experts: a blue paper passes them, three ticks, and lands in the journal. Then (closer, at 'And on the tenth of August'): inside
    the journal an amber 'earlier study' is struck through: 'withdrawn', 10 Aug 2026; a bubble: 'authors disagree'."""
    els = []
    cx0, cy0 = 120, 190
    els += [box(cx0, cy0, 200, 240, "rgba(201,193,238,.10)", LILAC, 2.5, 8, .3, style="claimed")]
    els += [line([[cx0 + 40 + 17 * k, cy0 + 40], [cx0 + 40 + 17 * k, cy0 + 170]], .5, LILAC, 2, "claimed", draw=False) for k in range(8)]
    els += [box(cx0 + 46, cy0 + 176, 46, 40, "none", LILAC, 2, 2, .6, style="claimed"), box(cx0 + 108, cy0 + 176, 46, 40, "none", LILAC, 2, 2, .6, style="claimed"),
            label(cx0 + 100, cy0 + 280, "Khafre claim", .8, LILAC, 30)]
    jx, jy = 1060, 170
    els += [box(jx, jy, 330, 290, "#5a3e2a", "#e8b87a", 2.5, 8, 1.6), box(jx + 16, jy + 16, 298, 258, "#6e4c33", "#c9a070", 1.5, 6, 1.6),
            label(jx + 165, jy + 330, "journal", 1.8, AMBER, 30)]
    els += [arrow([[cx0 + 210, cy0 + 120], [520, cy0 + 100], [760, cy0 + 120]], 2.2, LILAC, 3, "claimed", .7), _strike(790, cy0 + 90, 850, cy0 + 150, 2.9, RED, 7), _strike(850, cy0 + 90, 790, cy0 + 150, 3.0, RED, 7)]
    gy = 770
    els += [label(700, 540, "peer review", 4.8, AMBER, 32)]
    for k, x in enumerate((580, 700, 820)):
        els.append(person(x, gy, 150, round(5.0 + .15 * k, 2), "#e8d6b8"))
    els += _paper(150, 590, 120, 150, 5.6, fill="#cfe6ff", c=BLUE, ink="#3d5566")
    els += [arrow([[280, 668], [560, 668], [840, 668], [1020, 560], [1120, 470]], 6.2, BLUE, 3, "known", 1.4)]
    for k, (x, at) in enumerate(((580, 7.0), (700, 7.6), (820, 8.2))):
        els.append(_check(x, 580, 16, at))
    els += _paper(1090, 240, 120, 150, 9.2, fill="#cfe6ff", c=BLUE, ink="#3d5566")
    els += [ring(1150, 315, 95, 9.6, GREEN, 3, dur=.6)]
    # the retraction (shot 32, about 10 s in)
    rx, ry = jx + 190, jy + 70
    els += [box(rx, ry, 120, 160, "#f2c98e", "#fff6e6", 2, 6, 10.8, fx="pop")]
    els += [line([[rx + 16, ry + 160 * (.22 + .14 * r)], [rx + 104, ry + 160 * (.22 + .14 * r)]], 10.9, "#8a6a48", 3, draw=False, op=.7) for r in range(5)]
    els += [label(1430, 250, "earlier study", 11.2, AMBER, 30, "start"), label(1430, 292, "10 Aug 2026", 12.0, BONE, 28, "start"),
            _strike(rx - 14, ry + 176, rx + 134, ry - 16, 14.8, RED, 8), _strike(rx - 14, ry - 16, rx + 134, ry + 176, 15.0, RED, 8),
            label(1430, 400, "withdrawn", 15.4, RED, 34, "start")]
    bx, by = 1420, 470
    els += [{"k": "poly", "p": [[bx, by], [bx + 240, by], [bx + 240, by + 80], [bx + 60, by + 80], [bx + 20, by + 112], [bx + 30, by + 80], [bx, by + 80]], "fill": "rgba(245,236,220,.10)",
             "c": BONE, "w": 2, "in": 21.0, "fx": "pop"}, label(bx + 120, by + 50, "authors disagree", 21.1, BONE, 26, scl=True, fx="pop")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}, [1.7, 1255, 420]


def s34_paper():
    """s34: the clean cut with the claimed shafts ghosted; the tests that could settle it, dashed (not done): a drill rig and a string
    648 m down, a seismic thump with echo arcs, an 'open data' file; then a sheet of paper settles over the ground, the shafts
    sketched on it in ink."""
    s = kcut(at=-1)
    s["els"] += kshafts(.2, op=.35, spiral=False, dt=0) + kcubes(.2, op=.35)
    rx = 1060
    s["els"] += [line([[rx - 40, KGY], [rx, KGY - 120], [rx + 40, KGY]], 1.2, DIM, 4, dur=.5), line([[rx - 24, KGY - 50], [rx + 24, KGY - 50]], 1.4, DIM, 3, dur=.3),
                 line([[rx, KGY], [rx, kD(648)]], 1.6, AMBER, 4, "inferred", 1.4), label(rx + 30, KGY - 90, "drill", 1.8, AMBER, 28, "start")]
    tx = 380
    s["els"] += [box(tx - 30, KGY - 30, 60, 30, "#8c7152", "#f2dcb4", 2, 5, 2.4, fx="pop"), label(tx, KGY - 50, "seismic", 2.6, BLUE, 28)]
    s["els"] += [{"k": "line", "p": ellipse(tx, KGY, r, r, 14, 40, 140), "c": BLUE, "w": 2.4, "style": "inferred", "curve": True, "in": round(2.8 + .3 * j, 2), "fx": "draw", "dur": .5}
                 for j, r in enumerate((60, 120, 180))]
    fx_, fy = 1460, 170
    s["els"] += [box(fx_ - 28, fy - 36, 56, 72, "#e9dcc4", "#fff6e6", 2, 6, 3.4, fx="pop"), glow(fx_, fy, 80, 3.5, .45), label(fx_ + 46, fy + 10, "open data", 3.6, AMBER, 28, "start")]
    # the paper
    cx, cy, w, h, ang = KX, 520, 520, 520, math.radians(-3)
    R = lambda x, y: [r1(cx + (x - cx) * math.cos(ang) - (y - cy) * math.sin(ang)), r1(cy + (x - cx) * math.sin(ang) + (y - cy) * math.cos(ang))]
    x0, y0 = cx - w / 2, cy - h / 2
    sheet = [R(x0, y0), R(x0 + w, y0), R(x0 + w, y0 + h), R(x0, y0 + h)]
    ink, at = "#4a3a5a", 5.6
    s["els"] += [_poly([[q[0] + 10, q[1] + 14] for q in sheet], "rgba(0,0,0,.35)", at=at, fx="pop"), _poly(sheet, "#efe4cf", "#fff6e6", 2, at, fx="pop")]
    s["els"] += [line([R(cx - 80, cy - 170), R(cx, cy - 230), R(cx + 80, cy - 170)], at + .4, ink, 3, dur=.4), line([R(cx - 200, cy - 170), R(cx + 200, cy - 170)], at + .5, ink, 2, dur=.4)]
    for k in range(8):
        x = cx - 42 + 12 * k
        s["els"].append(line([R(x, cy - 160), R(x, cy + 120)], round(at + .6 + .05 * k, 2), ink, 2.4, "claimed", draw=False))
    for x in (cx - 50, cx + 6):
        s["els"].append(_poly([R(x, cy + 130), R(x + 44, cy + 130), R(x + 44, cy + 174), R(x, cy + 174)], "none", ink, 2.4, at + 1.0, style="claimed"))
    return s


# ================================================================ chapter 3: Doors in the dark
QS = Section(s=4.2, cx=889, gy=770)            # the Great Pyramid section for the Queen's Chamber shafts
SA = math.radians(39.5)


def face_hit(x, h, dx, dh):
    """Where a ray from (x, h) along (dx, dh) meets the pyramid's faces (metres)."""
    t = math.tan(SLOPE)
    best = None
    for kind in ("n", "s"):
        # north face: h = x t ; south face: h = (GB - x) t
        if kind == "n":
            den = dh - dx * t; num = x * t - h
        else:
            den = dh + dx * t; num = (GB - x) * t - h
        if abs(den) > 1e-9:
            u = num / den
            if u > 0 and (best is None or u < best):
                best = u
    return (x + dx * best, h + dh * best)


def qc_shafts():
    """The Queen's Chamber shafts (metres): the southern straight at about 39.5 degrees, the northern with its bend; each about
    60 m, ending at a stone door short of the faces. Returns their polylines, door points and the points where the faces are."""
    R = QS.rooms(); qx, qh = R["qc"]
    sx0 = (qx + 2.6, 22.0); s1 = (qx + 4.6, 22.0)
    s2 = (s1[0] + 58 * math.cos(SA), s1[1] + 58 * math.sin(SA))
    n0 = (qx - 2.6, 22.0); n1 = (qx - 4.6, 22.0)
    n2 = (n1[0] - 24 * math.cos(SA), n1[1] + 24 * math.sin(SA))
    b = math.radians(46)
    n3 = (n2[0] - 9 * math.cos(b), n2[1] + 9 * math.sin(b))
    n4 = (n3[0] - 26 * math.cos(SA), n3[1] + 26 * math.sin(SA))
    sf = face_hit(*s2, math.cos(SA), math.sin(SA)); nf = face_hit(*n4, -math.cos(SA), math.sin(SA))
    P = lambda q: QS.P(*q)
    return {"south": [P(sx0), P(s1), P(s2)], "north": [P(n0), P(n1), P(n2), P(n3), P(n4)], "sdoor": P(s2), "ndoor": P(n4),
            "sface": P(sf), "nface": P(nf), "mouths": (P(sx0), P(n0)), "qc": P((qx, qh + 2.6))}


def qsec(night=True):
    S = QS
    return [dict(S.body(), **{"in": -1}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": -1}] + \
           [dict(e, **{"in": -1, "op": .6}) for e in S.els(which=("desc", "asc", "gg", "qc", "kc", "sub", "reliev"))]


SECBASE = {"base": "section", "tod": "night", "ground": 770, "lx": 40, "layers": [{"d": 0, "c": "#6f5a43", "t": ""}, {"d": 60, "c": "#4d3e30", "t": ""}]}


def s35_shafts():
    """s35: the pyramid in section, the Queen's Chamber glowing; two thin amber lines climb from it, the southern straight, the
    northern with its bend, both stopping short of the faces; then the mouths flash where the wall was cut ('1872'); dashed lines
    carry on beyond the shafts' ends, a small '?' near each face."""
    g = qc_shafts()
    els = qsec() + [glow(*g["qc"], 80, .3, .8), label(g["qc"][0] + 28, g["qc"][1] + 56, "Queen's Chamber", .5, BONE, 28, "start"),
                    line(g["south"], .8, AMBER, 3.4, dur=1.4), line(g["north"], .8, AMBER, 3.4, dur=1.4)]
    for k, (x, y) in enumerate(g["mouths"]):
        els += [glow(x, y, 46, round(2.8 + .15 * k, 2), .95), line([[x, y - 9], [x, y + 9]], round(2.8 + .15 * k, 2), "#ffe2a8", 5, dur=.3)]
    els += [label(g["qc"][0] - 40, g["qc"][1] + 56, "1872", 3.3, "#ffe2a8", 34, "end")]
    els += [line([g["sdoor"], g["sface"]], 5.8, AMBER, 2.4, "inferred", .7), line([g["ndoor"], g["nface"]], 5.8, AMBER, 2.4, "inferred", .7)]
    els += question(g["sface"][0] + 34, g["sface"][1] - 6, 6.4, 54) + question(g["nface"][0] - 34, g["nface"][1] - 6, 6.6, 54)
    return dict(SECBASE, cam=[1.15, 889, 520], els=els)


def wall20(at, x0=80, y0=140, w=1620, h=650, hx=799, hy=290, hs=180):
    els = [box(x0, y0, w, h, "#a88a64", "rgba(255,236,206,.4)", 1.5, 8, at), box(x0, y0, w, h, "url(#k-speck)", r=8, at=at),
           line([[x0, 230], [x0 + w, 230]], at, "#6b5640", 2, draw=False, op=.6), line([[x0, 640], [x0 + w, 640]], at, "#6b5640", 2, draw=False, op=.6),
           line([[560, 230], [560, 640]], at, "#6b5640", 2, draw=False, op=.5), line([[1250, 140], [1250, 230]], at, "#6b5640", 2, draw=False, op=.5),
           line([[1330, 230], [1330, 640]], at, "#6b5640", 2, draw=False, op=.5)]
    els.append(box(hx, hy, hs, hs, INK, "#3a2c1e", 3, 2, at))
    return els


def s36_square():
    """s36: the stone face round the shaft's 20 cm square mouth, 9 units a centimetre; a sheet of printer paper over it (A4, 21 cm
    wide); then a person's head and shoulders, struck through; then a cat that just fits."""
    cm = 9.0
    hx, hy, hs = 799, 290, 20 * cm
    els = wall20(-1)
    els += [{"k": "dim", "x1": hx, "y1": hy - 24, "x2": hx + hs, "y2": hy - 24, "t": "", "c": BONE, "in": .8},
            label(hx + hs / 2, hy - 42, "20 cm", 1.0, BONE, 32),
            {"k": "dim", "x1": hx + hs + 24, "y1": hy, "x2": hx + hs + 24, "y2": hy + hs, "t": "", "c": BONE, "in": 1.1},
            label(hx + hs + 42, hy + hs / 2 + 10, "20 cm", 1.2, BONE, 32, "start")]
    pw, ph = 21 * cm, 29.7 * cm
    els += [box(r1(889 - pw / 2), hy, r1(pw), r1(ph), "rgba(250,246,236,.8)", "#fff", 2, 2, 3.6, fx="pop"),
            label(889, r1(hy + ph - 26), "printer paper", 4.0, INK, 28, halo=False)]
    dims = lambda at: [{"k": "dim", "x1": hx, "y1": hy - 24, "x2": hx + hs, "y2": hy - 24, "t": "", "c": BONE, "in": at}, label(hx + hs / 2, hy - 42, "20 cm", at, BONE, 32)]
    els += wall20(5.4) + dims(5.4)
    head, body = _bust(889, 262, cm)
    els += [{"k": "line", "p": head, "c": BONE, "w": 3.5, "style": "inferred", "curve": True, "in": 5.7},
            {"k": "line", "p": body, "c": BONE, "w": 3.5, "style": "inferred", "in": 5.7},
            _strike(889 - 22.5 * cm - 10, 720, 889 - 22.5 * cm + 50, 660, 6.5, RED, 8), _strike(889 + 22.5 * cm + 10, 720, 889 + 22.5 * cm - 50, 660, 6.7, RED, 8)]
    els += wall20(7.5) + dims(7.5)
    els += _cat(889, hy + hs - 6, cm, 7.7)
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s37_climb():
    """s37 + the first half of s38: the southern shaft rising across the frame at its true slope (39.5 degrees) from the Queen's
    Chamber, 16 units a metre along it (its width drawn larger than life); the robot at its foot, lamp on: 'Upuaut · 1993'. Then
    (about 10 s in) ghost robots step up the shaft, a cable paying out behind; 'over 60 m'; a pale slab closes the top, two copper
    dots. Right: where this is in the pyramid."""
    m = 16.0
    q0 = (150, 770); q1 = (q0[0] + 2 * m, q0[1])
    L = 58 * m
    ux, uy = math.cos(SA), -math.sin(SA)
    nx, ny = math.sin(SA), math.cos(SA)
    E = (q1[0] + L * ux, q1[1] + L * uy)
    hw = 22
    edge_a = [[q0[0], q0[1] - hw], [r1(q1[0] + hw * math.tan(SA / 2)), q1[1] - hw], [r1(E[0] - nx * hw), r1(E[1] - ny * hw)]]
    edge_b = [[q0[0], q0[1] + hw], [r1(q1[0] - hw * math.tan(SA / 2)), q1[1] + hw], [r1(E[0] + nx * hw), r1(E[1] + ny * hw)]]
    els = [box(80, 120, 1000, 690, "url(#k-blocks)", r=10, at=-1, op=.55), box(80, 120, 1000, 690, "rgba(13,11,9,.3)", r=10, at=-1),
           _poly(edge_a + edge_b[::-1], "#120e0b", "none", 0, -1),
           {"k": "line", "p": edge_a, "c": "#c9ad85", "w": 1.8, "in": -1}, {"k": "line", "p": edge_b, "c": "#c9ad85", "w": 1.8, "in": -1},
           _poly([[84, 800], [150, 800], [150, 735], [117, 715], [84, 735]], INK, BONE, 2, -1), glow(117, 768, 70, .3, .5),
           label(100, 712, "Queen's Chamber", .5, BONE, 26, "start")]
    U = lambda f, off=0: (r1(q1[0] + L * f * ux + nx * off), r1(q1[1] + L * f * uy + ny * off))
    rx, ry = U(.05, 16)
    els += [_robot(rx, ry, 1.3, 3.0, 39.5), glow(rx + 34, ry - 40, 70, 3.6, .85), label(rx + 120, ry + 20, "Upuaut · 1993", 5.2, AMBER, 30, "start")]
    # the climb (about 10 s in)
    els += [line([U(.05, 6), U(.93, 6)], 10.3, "#cbbca8", 2.5, dur=2.0)]
    for k, f in enumerate((.3, .55, .78)):
        x, y = U(f, 16)
        els.append(_robot(x, y, 1.3, round(10.5 + .45 * k, 2), 39.5, op=.4, fx="fade"))
    x, y = U(.93, 16)
    els += [_robot(x, y, 1.3, 11.8, 39.5), glow(x + 40, y - 40, 80, 12.0, .8)]
    a, b = U(0, -70), U(1, -70)
    els += [{"k": "dim", "x1": a[0], "y1": a[1], "x2": b[0], "y2": b[1], "t": "", "c": BONE, "in": 11.0},
            label(r1((a[0] + b[0]) / 2 - 30), r1((a[1] + b[1]) / 2 - 24), "over 60 m", 11.2, BONE, 32, "end")]
    d0, d1 = (E[0] - nx * 24, E[1] - ny * 24), (E[0] + nx * 24, E[1] + ny * 24)
    els += [line([d0, d1], 12.2, LIME, 14, dur=.3), glow(E[0], E[1], 90, 12.3, .8),
            dot(r1(E[0] - ux * 10 - nx * 9), r1(E[1] - uy * 10 - ny * 9), 4.5, COP, 12.5), dot(r1(E[0] - ux * 10 + nx * 9), r1(E[1] - uy * 10 + ny * 9), 4.5, COP, 12.5)]
    # where this is: the pyramid, small, its Queen's Chamber and southern shaft
    S = Section(s=1.9, cx=1400, gy=640)
    R = S.rooms(); qx, qh = R["qc"]
    sp = [S.P(qx + 2.6, 22), S.P(qx + 4.6, 22), S.P(qx + 4.6 + 58 * math.cos(SA), 22 + 58 * math.sin(SA))]
    els += [dict(S.body(), **{"in": .4}), {"k": "poly", "p": S.outline(), "fill": "url(#k-shade)", "c": "none", "w": 0, "in": .4}] + \
           [dict(e, **{"in": .5, "op": .5}) for e in S.els(which=("desc", "asc", "gg", "qc", "kc"))] + \
           [line(sp, .8, AMBER, 3, dur=.8), glow(*S.P(qx, qh + 2), 40, .8, .9), label(1400, 700, "southern shaft", 1.0, AMBER, 26)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s38_doorview():
    """s38 (the cut in): the robot's round camera view: the slab at the end of the shaft, close, its two copper pins bent down
    against the face, lamp light."""
    cx, cy, R = 889, 465, 330
    els, far = shaft_view(cx, cy, R, kend=.6)
    hw = (far[1][0] - far[0][0]) / 2
    f = hw / 144.0
    for sgn in (-1, 1):
        x = cx + sgn * 72 * f
        els += [line([[r1(x), r1(cy - 40 * f)], [r1(x), r1(cy - 96 * f)], [r1(x + sgn * 16 * f), r1(cy - 108 * f)]], .6, COP, 8 * f, dur=.4),
                line([[r1(x - 2 * f), r1(cy - 44 * f)], [r1(x - 2 * f), r1(cy - 92 * f)]], .8, "#f4b27a", 2, draw=False, op=.8), glow(r1(x), r1(cy - 70 * f), 50 * f, .6, .5)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


Y0, Y1 = 470, 670                       # the shaft's floor and ceiling in the side cut (10 units a centimetre)
SL0, SL1 = 1000, 1060                   # the slab
ST0, ST1 = 1270, 1360                   # the second stone, about 21 cm beyond


def stone2(at, fx=None):
    pts = [[ST0, Y0], [ST0 + 30, Y0 + 2], [ST1, Y0 + 8], [ST1 - 6, Y0 + 70], [ST1 + 4, Y1 - 50], [ST1, Y1], [ST0 + 20, Y1 - 2], [ST0 - 6, Y1 - 60], [ST0 + 4, Y0 + 90]]
    e = _poly(pts, "#b9a07a", "rgba(255,236,206,.6)", 2, at, curve=False)
    if fx:
        e["fx"] = fx
    return e


def interior(at, hole=False, stone=False, x0=80, x1=1700):
    els = [box(x0, Y0, x1 - x0, Y1 - Y0, "#15110d", r=0, at=at),
           box(SL0, Y0, SL1 - SL0, Y1 - Y0, LIME, "rgba(255,236,206,.7)", 2, 2, at), line([[SL0, Y0 + 30], [SL0 - 16, Y0 + 30], [SL0 - 16, Y0 + 48]], at, COP, 6, draw=False)]
    if hole:
        els.append(box(SL0, 566, SL1 - SL0, 9, INK, r=1, at=at))
    if stone:
        els.append(stone2(at))
    return els


def side_cut():
    els = [box(80, 330, 1620, Y0 - 330, "#a88a64", "rgba(255,236,206,.35)", 1.2, 4, -1), box(80, Y1, 1620, 790 - Y1, "#a88a64", "rgba(255,236,206,.35)", 1.2, 4, -1),
           box(80, 330, 1620, 460, "url(#k-speck)", r=4, at=-1)]
    els += [line([[x, 330], [x, Y0]], -1, "#6b5640", 2, draw=False, op=.7) for x in (360, 700, 1180, 1520)]
    els += [line([[x, Y1], [x, 790]], -1, "#6b5640", 2, draw=False, op=.7) for x in (240, 560, 900, 1400)]
    return els


def s39_cut():
    """s39: nine years on a line, 1993 to 2002; the side cut of the shaft's end (10 units a centimetre): a new robot drills a hole
    through the slab; a television, 'live'. Then a probe slides through the hole; about 20 cm on, a rough second stone."""
    els = side_cut() + interior(-1)
    X = lambda yr: r1(220 + (yr - 1993) * 76)
    ty = 210
    els += [dot(X(1993), ty, 11, AMBER, .4), label(X(1993), ty + 50, "1993", .5, AMBER, 30), line([[X(1993), ty], [X(2002), ty]], .9, "#8c7152", 3, dur=2.4)]
    els += [line([[X(1993 + k), ty - 14], [X(1993 + k), ty + 14]], round(1.0 + .26 * k, 2), BONE, 2, draw=False) for k in range(1, 9)]
    els += [dot(X(2002), ty, 11, AMBER, 3.4), label(X(2002), ty + 50, "2002", 3.5, AMBER, 30), label((X(1993) + X(2002)) / 2, ty - 30, "9 years", 2.4, BONE, 30)]
    els += [_robot(800, Y1, 3.0, 4.6, 0), arrow([[880, 584], [SL0 - 6, 572]], 5.6, "#cbbca8", 6, "known", .5, False), box(SL0, 566, SL1 - SL0, 9, INK, r=1, at=6.4, fx="fill")]
    tvs, (sx, sy, sw, sh) = _tv(1260, 230, 230, 7.0)
    els += tvs + [box(r1(sx + sw * .3), r1(sy + sh * .18), r1(sw * .4), r1(sh * .64), LIME, r=2, at=7.2), dot(r1(sx + sw * .4), r1(sy + sh * .3), 4, COP, 7.3),
                  dot(r1(sx + sw * .6), r1(sy + sh * .3), 4, COP, 7.3)]
    els += [ring(1440, 200, r, round(7.6 + .25 * j, 2), RED, 3, dur=.4) for j, r in enumerate((12, 24, 36))] + [label(1490, 210, "live", 7.8, RED, 32, "start")]
    els += [line([[880, 570], [1230, 570]], 9.8, BLUE, 3, dur=.9), dot(1234, 570, 8, BLUE, 10.6), glow(1250, 570, 90, 10.8, .7, "lamp")]
    els += [stone2(12.0, "pop"), glow(1315, 570, 110, 12.1, .5),
            {"k": "dim", "x1": SL1, "y1": 640, "x2": ST0, "y2": 640, "t": "", "c": BONE, "in": 12.4}, label((SL1 + ST0) / 2, 628, "20 cm", 12.5, BONE, 28),
            label(1380, 520, "another stone", 13.0, AMBER, 32, "start")]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s40_both_doors():
    """s40: back to the pyramid in section: both shafts; a small slab near the top of each; a dashed line joins the two:
    'about the same distance'."""
    g = qc_shafts()
    els = qsec() + [glow(*g["qc"], 70, .2, .7), line(g["south"], -1, AMBER, 3.4, draw=False), line(g["north"], -1, AMBER, 3.4, draw=False)]
    for k, (d, at) in enumerate(((g["sdoor"], .6), (g["ndoor"], 1.8))):
        els += [box(d[0] - 7, d[1] - 7, 14, 14, LIME, "#fff6e6", 1.5, 2, at, fx="pop"), glow(d[0], d[1], 50, at, .8)]
    els += [line([g["ndoor"], g["sdoor"]], 2.6, BONE, 2.4, "inferred", .8), label(889, min(g["ndoor"][1], g["sdoor"][1]) - 30, "about the same distance", 3.0, BONE, 28)]
    return dict(SECBASE, cam=[1.25, 889, 560], els=els)


def s41_djedi():
    """s41 (a new step on the side cut, closer): the cut reset as it stood (slab, hole, second stone); the Djedi robot; a green
    snake camera bends through the hole and curls down into the little space; 'Djedi · 2011'."""
    els = interior(.2, hole=True, stone=True, x0=600)
    els += [_robot(820, Y1, 3.0, 1.4, 0), label(820, 520, "Djedi · 2011", 2.4, GREEN, 32)]
    els += [line([[900, 584], [960, 572], [SL0, 570], [SL1, 570], [1110, 580], [1140, 610], [1150, 650]], 3.6, GREEN, 4, dur=1.6, curve=True),
            dot(1150, 654, 8, GREEN, 5.2), glow(1160, 640, 90, 6.2, .75, "lamp")]
    return els


def s42_inside():
    """s42: close inside the little space (the snake camera's round view): the back of the slab catches the lamp, polished; one
    copper pin comes through and curls into a small loop. Then on the floor: a red line and a few short red strokes, a soft glow."""
    cx, cy, R = 889, 400, 330
    els, far = shaft_view(cx, cy, R, kend=.5, tone=(196, 172, 136), door=False, vc=(889, 465))
    fx0, fy0, fx1, fy1 = far[0][0], far[0][1], far[2][0], far[2][1]
    els.insert(0, box(-50, -50, 1900, 1100, "#0b0907", r=0, at=-1))
    els += [box(fx0, fy0, fx1 - fx0, fy1 - fy0, "#e6d3b0", "rgba(255,236,206,.7)", 2, 2, -1)]
    els += [_poly([[fx0 + 20, fy1 - 10], [fx0 + 70, fy1 - 10], [fx1 - 10, fy0 + 60], [fx1 - 10, fy0 + 10]], "rgba(255,255,255,.55)", at=.9, op=.6),
            glow(fx0 + (fx1 - fx0) * .6, fy0 + (fy1 - fy0) * .4, 160, .9, .5), label(cx, fy0 - 18, "polished", 1.4, BONE, 28)]
    px, py = fx0 + (fx1 - fx0) * .72, fy0 + (fy1 - fy0) * .3
    loop = [[r1(px), r1(py)], [r1(px + 10), r1(py + 30)]] + [[r1(px + 30 + 22 * math.cos(math.radians(a))), r1(py + 60 + 22 * math.sin(math.radians(a)))] for a in range(200, 560, 30)]
    els += [dot(px, py, 7, COP, 3.0), {"k": "line", "p": loop, "c": COP, "w": 6, "curve": True, "in": 3.2, "fx": "draw", "dur": 1.0}, glow(px + 30, py + 60, 60, 3.6, .6)]
    # the floor of the little space: red strokes in perspective
    fl = fy1 + 70
    marks = [[[cx - 150, fl + 6], [cx + 60, fl - 4]], [[cx - 120, fl + 40], [cx - 100, fl + 20]], [[cx - 70, fl + 42], [cx - 50, fl + 18]], [[cx + 10, fl + 44], [cx + 34, fl + 20]],
             [[cx + 90, fl + 30], [cx + 140, fl + 36]]]
    els += [line([[r1(a[0]), r1(a[1])], [r1(b[0]), r1(b[1])]], round(6.4 + .15 * k, 2), "#d8402e", 6, dur=.3) for k, (a, b) in enumerate(marks)]
    els += [glow(cx - 20, fl + 26, 120, 7.0, .6, "red"), label(cx, 465 + R + 50, "red paint", 7.4, "#ff8a7a", 32)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s43_marks():
    """s43: the sealed spaces above the King's Chamber as a cutaway stack (iso3d.relieving_stack, no names); red work-gang marks
    write themselves on several blocks as schematic strokes (nothing readable); beside it, a carpenter's pencil marks on a plank."""
    stack, top = iso3d.relieving_stack(names=())
    base = iso(stack, 600, 770, 30, -35, .6, el=.34, at=-1)
    els = [glow(640, 520, 520, -1, .16, "lamp"), base]
    marks = []
    zf = 3.99
    for k, (lvl, x) in enumerate(((0, -2.6), (1, .4), (2, -1.4), (3, 1.6), (4, -2.2))):
        y = 5.8 + lvl * 2.25 + .25
        marks.append(ov(base, [{"t": "line", "p": [[x, y, zf], [x + .9, y + .9, zf]], "c": "#e4553a", "w": 4},
                               {"t": "line", "p": [[x + 1.2, y + .1, zf], [x + 1.4, y + .95, zf]], "c": "#e4553a", "w": 4},
                               {"t": "line", "p": [[x - .3, y + .5, zf], [x + 2.2, y + .5, zf]], "c": "#e4553a", "w": 3}], round(3.8 + .4 * k, 2), fx="fade"))
    els += marks + [label(330, 330, "work-gang marks", 4.2, "#ff8a7a", 30, "end")]
    # the plank and the pencil
    px, py = 1180, 470
    els += [box(px, py, 460, 130, "#a87a4a", "#e8c9a0", 2, 6, 7.4, fx="pop")] + \
           [line([[px + 10, py + 22 + 22 * j], [px + 450, py + 26 + 22 * j]], 7.5, "#7a5230", 1.5, draw=False, op=.6) for j in range(5)]
    els += [line([[px + 80 + 70 * j, py + 40], [px + 80 + 70 * j, py + 92]], round(7.8 + .15 * j, 2), "#3a3a3a", 4, dur=.25) for j in range(5)]
    els += [_poly([[px + 140, py - 40], [px + 400, py - 90], [px + 406, py - 76], [px + 146, py - 26]], "#c0392b", "#f0c0a0", 1.5, 8.6, fx="pop"),
            label(px + 230, py + 180, "carpenter's marks", 8.8, BONE, 28)]
    return {"base": "dark", "stars": 40, "cam": [1, 889, 500], "els": els}


def s44_sky():
    """s44: the pyramid in section at night, its four shafts thin lines angled up; a soft gold glow travels slowly up the King's
    Chamber shafts towards the stars; 'a path to the sky?'. No figures, no named stars."""
    S = QS; R = S.rooms(); kx, kh = R["kc"]
    g = qc_shafts()
    ks0, kn0 = (kx + 2.6, kh + 1.0), (kx - 2.6, kh + 1.0)
    ks1 = face_hit(*ks0, math.cos(math.radians(45)), math.sin(math.radians(45)))
    kn1 = face_hit(*kn0, -math.cos(math.radians(32.5)), math.sin(math.radians(32.5)))
    els = qsec() + [line(g["south"], -1, "#c9ad85", 2, draw=False, op=.7), line(g["north"], -1, "#c9ad85", 2, draw=False, op=.7),
                    line([S.P(*ks0), S.P(*ks1)], .3, GOLD, 2.4, dur=1.0), line([S.P(*kn0), S.P(*kn1)], .3, GOLD, 2.4, dur=1.0)]
    for k, (a, b) in enumerate(((ks0, ks1), (kn0, kn1))):
        A, Bp = S.P(*a), S.P(*b)
        for j in range(7):
            f = j / 6
            x, y = A[0] + (Bp[0] - A[0]) * f, A[1] + (Bp[1] - A[1]) * f
            els.append(glow(r1(x), r1(y), 34 + 8 * j, round(3.0 + .55 * j + .2 * k, 2), .32 + .05 * j, "lamp"))
        d = (Bp[0] - A[0], Bp[1] - A[1]); n = math.hypot(*d)
        ex, ey = Bp[0] + d[0] / n * 220, Bp[1] + d[1] / n * 220
        els += [line([Bp, [r1(ex), r1(ey)]], round(6.9 + .2 * k, 2), GOLD, 2, "inferred", 1.2), glow(r1(ex), r1(ey), 80, round(8.0 + .2 * k, 2), .6, "lamp")]
    els += [label(889, 150, "a path to the sky?", 6.0, GOLD, 40, st="ital")]
    return dict(SECBASE, cam=[1, 889, 500], els=els)


def s45_record():
    """s45: three robots on a timeline, nine years apart (1993, 2002, 2011); a padlock above the gaps; under each, what it showed:
    a film reel, a television, a journal sheet, 2013."""
    X = lambda yr: r1(260 + (yr - 1990) * 52)
    ay = 470
    els = [line([[X(1990), ay], [X(2015), ay]], .2, "#8c7152", 3, dur=1.0)]
    for k, yr in enumerate((1993, 2002, 2011)):
        at = round(.5 + .3 * k, 2)
        els += [_robot(X(yr), ay - 14, 1.7, at, 0), dot(X(yr), ay, 9, AMBER, at), label(X(yr), ay + 50, str(yr), at + .1, AMBER, 30)]
    els += [box(X(1993), ay + 76, X(2002) - X(1993), 12, AMBER, r=6, at=1.2, fx="pop"), box(X(2002), ay + 76, X(2011) - X(2002), 12, AMBER, r=6, at=1.4, fx="pop"),
            label((X(1993) + X(2002)) / 2, ay + 124, "9 years", 1.3, BONE, 28), label((X(2002) + X(2011)) / 2, ay + 124, "9 years", 1.5, BONE, 28)]
    px, py = X(2002), 250
    els += [{"k": "line", "p": ellipse(px, py, 40, 46, 18, 180, 360), "c": "#cbbca8", "w": 9, "curve": True, "in": 1.8, "fx": "draw", "dur": .5},
            box(px - 56, py - 4, 112, 92, "#8c7152", "#f2dcb4", 2.5, 12, 1.7, fx="pop"), dot(px, py + 36, 9, INK, 1.9), box(px - 4, py + 40, 8, 22, INK, r=2, at=1.9)]
    els += question((X(1993) + X(2002)) / 2, ay - 120, 2.2, 60) + question((X(2002) + X(2011)) / 2, ay - 120, 2.4, 60)
    fx_ = X(1993); fy = 680
    els += [{"k": "circle", "x": fx_, "y": fy, "r": 54, "fill": "#2a231c", "c": "#c9ad85", "w": 3, "in": 5.0, "fx": "pop"}] + \
           [dot(r1(fx_ + 28 * math.cos(math.radians(a))), r1(fy + 28 * math.sin(math.radians(a))), 11, "#c9ad85", 5.1) for a in range(0, 360, 72)] + [label(fx_ + 80, fy + 10, "film", 5.4, BONE, 28, "start")]
    tvs, _ = _tv(X(2002), fy, 120, 6.4)
    els += tvs + [dot(X(2002) + 46, fy - 30, 6, RED, 6.6), label(X(2002) + 90, fy + 10, "live TV", 6.8, BONE, 28, "start")]
    jx = X(2013)
    els += _paper(jx - 46, fy - 60, 92, 116, 8.2, fill="#e9dcc4", ink="#6b5a48") + [label(jx + 70, fy + 10, "2013", 8.6, BONE, 30, "start"),
                                                                                   line([[X(2011), ay + 10], [jx, fy - 64]], 8.4, "#cbbca8", 2, "inferred", .5)]
    els += [glow(x, fy, 110, 9.0, .35) for x in (fx_, X(2002), jx)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s46_unknown():
    """s46: back in the dark side cut: the second stone, a lilac dashed ring round it and a large '?' beyond; the lamp dims slowly."""
    els = side_cut() + interior(-1, hole=True, stone=True) + [glow(1180, 570, 160, -1, .6, "lamp")]
    els += [wipe(80, Y0 + 2, 1620, Y1 - Y0 - 4, 3.4, fill="#15110d", op=.7, dur=3.0)]
    els += [ring(1315, 570, 120, 1.6, LILAC, 3, "claimed", .8)] + question(1560, 610, 2.4, 120)
    return {"base": "dark", "cam": [1.15, 1050, 520], "els": els}


# ================================================================ chapter 4: The Sphinx and the rain
def sphinx_line(x0, y0, w, h):
    """The Sphinx's side profile (iso3d.SPHINX_PROF, 73 m long, about 20 m high) as a polyline in a w x h box, head to the left."""
    pts = []
    for px, py in iso3d.SPHINX_PROF:
        pts.append([r1(x0 + px / 73.0 * w), r1(y0 - py / 29.6 * h)])
    return pts


def s47_sphinx():
    """s47: dawn; the Sphinx as an iso model (73 m long, about 20 m high) turning slowly on its ground; '73 m' along its body; a
    person at its paws. Then: a block of layered bedrock; the rock around a central mass is cut away into a pit, the lion's outline
    draws on the mass that is left, and the waste rock fades."""
    base = iso(iso3d.ground(46, grid=10) + iso3d.sphinx(0, 0) + [{"t": "person", "x": -42, "y": 0, "z": 4, "h": 1.7, "color": "#e8d6b8"}], 540, 540, 6.0, -32, .7, el=.3, at=-1)
    els = [glow(520, 470, 520, -1, .2, "lamp"), base,
           ov(base, [{"t": "line", "p": [[-36.5, 0, 13], [36.5, 0, 13]], "c": AMBER, "w": 3}, {"t": "line", "p": [[-36.5, 0, 11.5], [-36.5, 0, 14.5]], "c": AMBER, "w": 3},
                     {"t": "line", "p": [[36.5, 0, 11.5], [36.5, 0, 14.5]], "c": AMBER, "w": 3}, ilab(0, 0, 16, "73 m", AMBER, 36)], 1.2, fx="fade")]
    pp = P3(base, (-42, 1.7, 4), 2)
    els += [ring(pp[0], pp[1] + 6, 14, 1.5, BONE, 1.5, dur=.4), label(pp[0] - 22, pp[1] - 16, "a person", 1.6, DIM, 24, "end")]
    # the carving, on a card of its own: 1.6 units a metre... drawn at 6.6 units a metre (73 m = 480 units)
    X0, Y0_, W, H = 1020, 330, 680, 440
    FL = "#1d1712"
    els += [box(X0, Y0_, W, H, FL, "rgba(255,236,206,.3)", 1.5, 16, 5.0, fx="pop")]
    floor, surf = 720, 610
    lx0, lw = 1120, 480
    lion = sphinx_line(lx0, floor, lw, lw * 29.6 * .68 / 73)
    hill = [[1040, surf], [1090, surf], [1100, 560], [1150, 520], [1200, 500], [1260, 515], [1330, 540], [1450, 548], [1560, 560], [1610, 590], [1630, surf], [1680, surf], [1680, 750], [1040, 750]]
    els += [_poly(hill, "#a88a64", "#e8cfa6", 1.6, 5.3, fx="rise")]
    for k in range(4):
        y = 535 + 55 * k
        els.append(line([[1042, y], [1678, y]], 5.4, "#7d6448", 5, draw=False, op=.5))
    cut = [[1090, surf], [1100, floor], [1630, floor], [1630, surf], [1610, 590], [1560, 560], [1450, 548], [1330, 540], [1260, 515], [1200, 500], [1150, 520], [1100, 560]]
    mass = [[1105, floor], [1105, 560], [1150, 525], [1200, 505], [1260, 518], [1330, 543], [1450, 551], [1560, 563], [1615, 592], [1615, floor]]
    els += [_poly([[1090, surf], [1105, surf], [1105, floor], [1090, floor]], "#0d0b09", at=6.4), _poly([[1615, surf], [1630, surf], [1630, floor], [1615, floor]], "#0d0b09", at=6.6),
            line([[1090, floor], [1630, floor]], 6.7, "#e8cfa6", 2, draw=False), label(1360, 760, "the pit", 6.8, DIM, 26)]
    els += [{"k": "poly", "p": mass, "fill": FL, "c": "none", "w": 0, "op": .8, "keepop": True, "in": 8.2, "dur": .8},
            {"k": "poly", "p": lion, "fill": "#c8a978", "c": "#fff1d8", "w": 2.4, "in": 8.6, "fx": "fade", "dur": .8},
            {"k": "line", "p": lion + [lion[0]], "c": GOLD, "w": 3, "in": 7.6, "fx": "draw", "dur": 1.0}]
    return {"base": "sky", "tod": "dawn", "ground": 900, "sun": [1500, 790, 34], "cam": [1, 889, 500], "els": els}


def wall16(x, y, w, h, at=-1, round_at=None, fiss_at=None, water=False):
    """f05.wall_face, widened: an enclosure wall face on, hard and soft beds; the soft ones cut back into rounded recesses (round_at),
    four deep vertical fissures (fiss_at)."""
    n = 7
    bh = h / n
    els = [box(x, y, w, h, "#a88a64", "rgba(255,236,206,.5)", 1.5, 4, at)]
    for i in range(n):
        yy = y + bh * (i + .5)
        if i % 2:
            els.append(box(x, r1(yy - bh * .32), w, r1(bh * .64), "#7d6448", r=0, at=at))
            if round_at is not None:
                top = [[r1(x + u * w / 60), r1(yy - bh * .22 + 7 * math.sin(u * .9))] for u in range(61)]
                els.append({"k": "poly", "p": top + [[x + w, r1(yy + bh * .3)], [x, r1(yy + bh * .3)]],
                            "fill": "rgba(40,28,18,.45)", "c": "none", "w": 0, "in": round(round_at + .1 * (i // 2), 2), "fx": "fade", "dur": .6})
                els.append({"k": "line", "p": top, "c": "#5a4632", "w": 2, "in": round(round_at + .1 * (i // 2), 2), "fx": "draw", "dur": .8})
        els.append(line([[x, r1(yy + bh * .33)], [x + w, r1(yy + bh * .33)]], at, "#e7cfa6", 1.4, draw=False, op=.45))
    fx_ = (.16, .39, .63, .86)
    fis = [[[r1(x + w * f), y + 6], [r1(x + w * (f + .01)), r1(y + h * .3)], [r1(x + w * (f - .01)), r1(y + h * .6)], [r1(x + w * f), r1(y + h * .94)]] for f in fx_]
    if fiss_at is not None:
        for j, pp in enumerate(fis):
            els.append({"k": "line", "p": pp, "curve": True, "c": "#2a1f16", "w": 6, "op": .9, "keepop": True, "in": round(fiss_at + .15 * j, 2), "fx": "draw", "dur": .6})
    return els, fis


WX, WY, WW, WH = 150, 150, 1480, 610


def s48_wall():
    """s48: the enclosure wall face on: hard and soft beds; the soft ones cut back into rounded recesses (at 'Rounded'), four deep
    vertical fissures (at 'cracks'); then rain on the wall top, water running down the fissures one by one, pooling at the foot."""
    els, fxs = wall16(WX, WY, WW, WH, -1, 7.5, 9.7)
    els += [label(WX + WW / 2, WY - 20, "the pit wall", .4, DIM, 28)]
    els += [{"k": "rays", "x0": WX, "x1": WX + WW, "y0": 110, "y1": WY + 30, "n": 70, "spread": .1, "c": "#b9d6e8", "in": 11.6, "fx": "draw", "dur": 1.2}]
    for j, pp in enumerate(fxs):
        at = round(12.4 + .6 * j, 2)
        els += [line(pp + [[pp[-1][0], WY + WH]], at, "#9fd0ff", 3, dur=.8, curve=True), oval(pp[-1][0], WY + WH + 6, 46, 9, "rgba(111,182,214,.55)", at=round(at + .7, 2), fx="pop")]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def tl_axis(y=560, x0=200, x1=1580):
    X = lambda yr: r1(x0 + (yr + 10000) / 10000 * (x1 - x0))
    ticks = [[X(v), t] for v, t in ((-10000, "10,000 BCE"), (-7500, "7500"), (-5000, "5000"), (-2500, "2500"), (0, "1 CE"))]
    return X, {"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": ticks, "t": "", "in": .2}


def s49_dates(static=False):
    """s49: a timeline from 10,000 BCE to 1 CE: a tan band 'dry, as today' over the last five thousand years; Schoch's blue band,
    7000 to 5000 BCE, rain above it; Khafre about 2530 BCE; '2,500 to 4,500 years earlier'."""
    X, ax = tl_axis()
    y = 560
    T = (lambda t: -1) if static else (lambda t: t)
    els = [dict(ax, **{"in": T(.2)}),
           box(X(-3000), y + 70, X(0) - X(-3000), 14, "#c9ad85", r=7, at=T(1.2), op=.7, fx="fill"), label(r1((X(-3000) + X(0)) / 2), y + 116, "dry, as today", T(1.8), DIM, 28)]
    els += [box(X(-7000), 410, X(-5000) - X(-7000), 22, BLUE, r=11, at=T(7.6), fx="pop"), label(r1((X(-7000) + X(-5000)) / 2), 390, "Schoch", T(8.0), BLUE, 32),
            {"k": "rays", "x0": X(-7000), "x1": X(-5000), "y0": 150, "y1": 360, "n": 30, "spread": .12, "c": "#b9d6e8", "in": T(8.4), "fx": "draw", "dur": 1.2}]
    els += [line([[X(-2530), y], [X(-2530), y - 70]], T(12.4), AMBER, 3, dur=.4), dot(X(-2530), y, 11, AMBER, T(12.4)), label(X(-2530), y - 86, "Khafre", T(12.6), AMBER, 32)]
    if not static:
        els += [arrow([[X(-2530), y + 160], [X(-5000), y + 160]], 14.6, AMBER, 3, "known", .8, False), arrow([[X(-5000), y + 160], [X(-7000), y + 160]], 15.3, BLUE, 3, "inferred", .6, False),
                label(X(-5000), y + 210, "2,500 to 4,500 years earlier", 15.6, BONE, 30)]
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}, X


def s50_seismic():
    """s50: a section through the pit's floor: a hammer plate and a row of geophones on top; echo arcs; a weathered layer below the
    floor, thick under some parts and thin under others: 'uneven weathering'."""
    fy = 330
    els = [box(80, fy, 1620, 470, "#6f5a43", r=0, at=-1), box(80, fy, 1620, 470, "url(#k-speck)", r=0, at=-1), line([[80, fy], [1700, fy]], -1, "#e7cfa6", 2.4, draw=False),
           label(160, fy - 20, "pit floor", .3, DIM, 26, "start")]
    hx = 300
    els += [box(hx - 40, fy - 16, 80, 16, "#8c7152", "#f2dcb4", 2, 3, .6, fx="pop"), line([[hx + 70, fy - 120], [hx + 10, fy - 30]], .8, "#cbbca8", 6, dur=.3),
            box(hx - 6, fy - 46, 40, 24, "#8a8a90", "#e9dccb", 1.5, 4, 1.0, fx="pop")]
    for k in range(9):
        gx = 520 + 130 * k
        els.append(_poly([[gx - 9, fy], [gx + 9, fy], [gx, fy - 18]], BLUE, at=round(1.0 + .07 * k, 2), fx="pop"))
    for j, r in enumerate((70, 140, 210)):
        els.append({"k": "line", "p": ellipse(hx, fy, r * 1.2, r, 18, 15, 165), "c": BLUE, "w": 2.4, "curve": True, "in": round(1.8 + .3 * j, 2), "fx": "draw", "dur": .5})
    for k, gx in enumerate((650, 910, 1170)):
        els.append(arrow([[r1(hx + (gx - hx) * .45), fy + 240], [gx, fy + 8]], round(2.9 + .25 * k, 2), AMBER, 2.4, "known", .6, False))
    wl = [[80, fy]] + [[x, r1(fy + 50 + 95 * (1 + math.cos((x - 80) / 1620 * math.pi)) / 2 + 8 * math.sin(x / 37.0))] for x in range(80, 1701, 40)] + [[1700, fy]]
    els += [{"k": "poly", "p": wl, "fill": "rgba(232,207,166,.55)", "c": "#f2dcb4", "w": 2, "in": 4.2, "dur": .9, "curve": False}]
    els += [label(1320, 640, "uneven weathering", 5.2, "#f2dcb4", 32)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s51_salt():
    """s51 (a new step on the wall, close on one soft bed): the wall section clean again; moisture rises into the soft bed; salt
    crystals grow in its pores and push the grains apart; beside it, a pavement slab cracking as ice grows. Then the soft beds
    crumble back into rounded recesses, no rain drawn; the hard beds stay sharp."""
    n = 7; bh = WH / n
    cx, cy = 600, WY + bh * 3.5
    x0, x1, y0, y1 = 150, 1100, 150, 760
    els = [box(x0, y0, x1 - x0, y1 - y0, "#a88a64", r=0, at=.2)]
    for i in range(n):
        yy = WY + bh * (i + .5)
        if i % 2 and y0 < yy < y1:
            els.append(box(x0, r1(yy - bh * .32), x1 - x0, r1(bh * .64), "#7d6448", r=0, at=.2))
        if y0 < yy + bh * .33 < y1:
            els.append(line([[x0, r1(yy + bh * .33)], [x1, r1(yy + bh * .33)]], .2, "#e7cfa6", 1.4, draw=False, op=.45))
    for k, x in enumerate((360, 480, 600, 720, 840)):
        els.append(arrow([[x, cy + 120], [x, cy + 10]], round(4.0 + .1 * k, 2), BLUE, 3, "known", .5, False))
    rnd = random.Random(4)
    gr = [(r1(rnd.uniform(260, 940)), r1(rnd.uniform(cy - bh * .26, cy + bh * .26))) for _ in range(26)]
    for k, (x, y) in enumerate(gr):
        els.append(dot(x, y, 6, "#c9a77a", 4.4, fx="fade"))
    for k, (x, y) in enumerate(gr[::2]):
        els.append({"k": "poly", "p": [[x + 9, y - 9], [x + 17, y], [x + 9, y + 9], [x + 1, y]], "fill": "#f7f3ea", "c": "#ffffff", "w": 1, "in": round(5.6 + .06 * k, 2), "fx": "pop"})
    for k, (x, y) in enumerate(gr[1::3]):
        els += [line([[x - 4, y], [x - 16, y]], round(7.0 + .05 * k, 2), "#ffe2a8", 2, dur=.2), line([[x + 4, y], [x + 16, y]], round(7.0 + .05 * k, 2), "#ffe2a8", 2, dur=.2)]
    els += [label(600, r1(cy - bh * .5 - 14), "salt", 6.0, "#f7f3ea", 30)]
    # the pavement and the ice
    px, py = 830, 236
    els += [box(px - 10, py - 10, 210, 116, "rgba(18,13,10,.85)", "rgba(255,236,206,.4)", 1.5, 10, 9.3, fx="pop"),
            box(px, py, 190, 96, "#8f8f94", "#e9e9ee", 2, 6, 9.4, fx="pop"), line([[px + 60, py], [px + 92, py + 40], [px + 80, py + 96]], 9.8, INK, 4, dur=.5),
            {"k": "poly", "p": [[px + 86, py + 30], [px + 100, py + 44], [px + 86, py + 58], [px + 78, py + 44]], "fill": "#cfe6ff", "c": "#ffffff", "w": 1, "in": 10.2, "fx": "pop"},
            label(px + 95, py + 128, "ice", 10.4, ICE, 26)]
    # the beds crumble back into rounded recesses; the hard beds stay sharp
    for i in (1, 3, 5):
        yy = WY + bh * (i + .5)
        if y0 < yy < y1:
            top = [[r1(x0 + u * (x1 - x0) / 40), r1(yy - bh * .22 + 7 * math.sin(u * .9))] for u in range(41)]
            els.append({"k": "poly", "p": top + [[x1, r1(yy + bh * .3)], [x0, r1(yy + bh * .3)]], "fill": "rgba(40,28,18,.45)", "c": "none", "w": 0,
                        "in": round(12.2 + .2 * (i // 2), 2), "fx": "fade", "dur": .6})
            els.append({"k": "line", "p": top, "c": "#5a4632", "w": 2, "in": round(12.2 + .2 * (i // 2), 2), "fx": "draw", "dur": .8})
    for i in (2, 4):
        yy = WY + bh * (i + .5)
        els.append(line([[x0, r1(yy - bh * .5)], [x1, r1(yy - bh * .5)]], 12.8, "#fff1d8", 2, dur=.6))
    return els, [2.0, cx, cy - 20]


def s52_karst():
    """s52: a section through the limestone: underground water winds along joints and widens them into channels; a time arrow
    beneath, 'millions of years ago'; at the far right, much later, a tiny carver."""
    els = []
    for k, (y, c) in enumerate(((180, "#a88a64"), (300, "#8f7350"), (420, "#a07f5a"), (540, "#7d6448"))):
        els.append(box(80, y, 1620, 120, c, r=0, at=-1))
    els += [box(80, 180, 1620, 480, "url(#k-speck)", r=0, at=-1), line([[80, 180], [1700, 180]], -1, "#e7cfa6", 2, draw=False)]
    joints = (330, 640, 980, 1290)
    for x in joints:
        els.append(line([[x, 180], [x + 10, 330], [x - 6, 480], [x + 4, 660]], -1, "#3a2c1e", 2, draw=False, curve=True))
    for k, x in enumerate(joints):
        els.append(line([[x, 180], [x + 10, 330], [x - 6, 480], [x + 4, 660]], round(3.0 + .3 * k, 2), BLUE, 4, dur=1.0, curve=True))
        els.append({"k": "poly", "p": [[x - 14, 180], [x + 18, 180], [x + 26, 330], [x + 8, 480], [x + 18, 660], [x - 10, 660], [x - 20, 480], [x - 6, 330]], "fill": "rgba(63,134,168,.55)",
                    "c": "#9fd0ff", "w": 1.5, "curve": True, "in": round(4.6 + .2 * k, 2), "dur": .6})
    els += [arrow([[220, 720], [1500, 720]], 5.6, BONE, 3, "known", 1.0, False), label(220, 770, "millions of years ago", 6.0, BONE, 28, "start"),
            label(1560, 770, "now", 6.2, DIM, 26, "end"), person(1610, 724, 40, 7.4, "#e8d6b8"), label(1610, 670, "a carver", 7.6, AMBER, 26)]
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def plan_xy(e, n, k=1.05, ox=889, oy=455, e0=-52, n0=-202):
    return [r1(ox + (e - e0) * k), r1(oy - (n - n0) * k)]


def s53_runoff():
    """s53: a plan of the plateau sloping east to the Sphinx (schematic, positions after published plans): blue runoff arrows flow
    downhill into the Sphinx's enclosure; then quarry pits for Khufu's works open upslope and the arrows stop at their edge."""
    P = plan_xy
    els = []
    for key, name in (("khufu", "Khufu"), ("khafre", "Khafre")):
        (x, n), b = GP[key]; h = b / 2
        sq = [P(x - h, n - h), P(x + h, n - h), P(x + h, n + h), P(x - h, n + h)]
        els += [_poly(sq, "rgba(220,191,148,.55)", "#f2dcb4", 1.8, -1), line([sq[0], sq[2]], -1, "#8c7152", 1, draw=False, op=.8), line([sq[1], sq[3]], -1, "#8c7152", 1, draw=False, op=.8),
                label(P(x, n)[0], P(x, n - h)[1] + 34, name, .3, BONE, 28)]
    sx, sn = GP["sphinx"]
    enc = [P(sx - 45, sn + 35), P(sx + 40, sn + 35), P(sx + 40, sn - 40), P(sx - 45, sn - 40)]
    els += [_poly(enc, "rgba(13,11,9,.6)", "#f2dcb4", 2, -1), box(P(sx - 25, sn + 6)[0], P(sx - 25, sn + 6)[1], 48, 12, "#dcbf94", r=3, at=-1),
            label(P(sx, sn - 40)[0], P(sx, sn - 40)[1] + 32, "Sphinx", .3, BONE, 28)]
    for k in range(4):
        a = P(-200 + 120 * k, -560); b = P(260 + 120 * k, -100)
        els.append(line([a, b], -1, "rgba(245,236,220,.18)", 1.4, "inferred", draw=False))
    starts = [(-80, -230), (10, -290), (-30, -380), (80, -470)]
    ends = [(sx - 50, sn + 22), (sx - 50, sn + 6), (sx - 50, sn - 10), (sx - 50, sn - 26)]
    for k, (a, b) in enumerate(zip(starts, ends)):
        els.append(arrow([P(*a), P(*b)], round(4.6 + .25 * k, 2), BLUE, 3.4, "known", .9, False))
    els += [label(P(-80, -230)[0] - 14, P(-80, -230)[1] - 14, "runoff", 5.2, BLUE, 28, "end")]
    q = [P(150, -270), P(sx - 54, -330), P(sx - 54, sn - 46), P(150, -520)]
    els += [_poly(q, "#3a2c20", "#f2dcb4", 2, 8.2, fx="pop"), _poly(q, "url(#k-hatch)", at=8.25, fx="pop"),
            label(P(150, -520)[0] - 16, P(150, -520)[1] - 6, "quarries", 8.6, AMBER, 30, "end")]
    return {"base": "plan", "cam": [1, 889, 500], "els": els}


def s54_reader():
    """s54: the timeline again (Schoch's long blue band, Khafre, the dry years) and Reader's small green band just before Khafre:
    a few centuries, not thousands of years."""
    sc, X = s49_dates(static=True)
    sc["els"] += [box(X(-2900), 512, X(-2560) - X(-2900), 20, GREEN, r=10, at=1.4, fx="pop"), label(X(-2900) - 14, 532, "Reader: a few centuries", 2.0, GREEN, 30, "end")]
    return sc


def s55_temple():
    """s55: a side cut of the pit and the Sphinx in it; blocks lift out of the pit walls and fly into the temple in front, their
    coloured beds matching the beds left in the walls; rings mark two matches."""
    beds = ["#c8a978", "#8a6a4a", "#c8a978"]
    gy, py = 520, 700
    els = [box(80, gy, 1620, 280, "#6f5a43", r=0, at=-1), line([[80, gy], [1700, gy]], -1, "#e7cfa6", 2, draw=False)]
    els += [box(720, gy, 860, py - gy, "#15110d", r=0, at=-1)]
    for j, c in enumerate(beds):
        h = (py - gy) / 3
        els += [box(660, r1(gy + h * j), 60, r1(h), c, r=0, at=-1), box(1580, r1(gy + h * j), 60, r1(h), c, r=0, at=-1)]
    els += [{"k": "sphinx", "x": 1150, "y": py, "w": 640, "in": -1}, label(1150, 760, "the pit", .3, DIM, 26)]
    els += [box(150, 390, 400, 130, "none", BONE, 2, 4, 2.4, style="claimed"), label(350, 570, "the temple", 2.8, BONE, 28)]
    els += [arrow([[700, 560], [600, 420], [520, 440]], 4.0, AMBER, 3, "known", 1.0)]
    order = [(c, r) for r in range(2) for c in range(4)]
    for k, (c, r) in enumerate(order):
        els.append(box(160 + 96 * c, 455 - 62 * r, 92, 58, beds[(c + r) % 3], "#3a2c1e", 1.5, 3, round(4.4 + .14 * k, 2), fx="pop"))
    els += [line([[r1(160 + 96 * 3 + 46), 484], [690, 548]], 8.4, "#ffe2a8", 2.5, "inferred", .6), ring(690, 548, 30, 8.8, "#ffe2a8", 3, dur=.5), ring(r1(160 + 96 * 3 + 46), 484, 30, 9.0, "#ffe2a8", 3, dur=.5)]
    els += [line([[r1(160 + 96 * 1 + 46), 422], [690, 607]], 9.2, "#ffe2a8", 2.5, "inferred", .6), ring(690, 607, 30, 9.5, "#ffe2a8", 3, dur=.5), ring(r1(160 + 96 + 46), 422, 30, 9.6, "#ffe2a8", 3, dur=.5)]
    return {"base": "sky", "tod": "dawn", "ground": gy, "sun": [1500, 300, 30], "cam": [1, 889, 500], "els": els}


def s56_plan():
    """s56: a plan: the Sphinx Temple and Khafre's Valley Temple side by side on one terrace, their fronts and backs joined by two
    dashed alignment lines; Khafre's causeway runs up from the Valley Temple to his pyramid; an amber frame closes round pit, temple
    and Sphinx: 'one project'. (Schematic, positions after published plans.)"""
    k = 1.45
    S = (1230, 430)
    P = lambda e, n: [r1(S[0] + e * k), r1(S[1] - n * k)]
    (kx, kn), kb = GP["khafre"]; sx, sn = GP["sphinx"]
    kc = P(kx - sx, kn - sn)
    h = kb / 2
    khafre = [P(kx - sx - h, kn - sn - h), P(kx - sx + h, kn - sn - h), P(kx - sx + h, kn - sn + h), P(kx - sx - h, kn - sn + h)]
    els = [_poly(khafre, "rgba(220,191,148,.5)", "#f2dcb4", 1.8, -1), line([khafre[0], khafre[2]], -1, "#8c7152", 1, draw=False), line([khafre[1], khafre[3]], -1, "#8c7152", 1, draw=False),
           label(kc[0], khafre[0][1] + 40, "Khafre", .3, AMBER, 30)]
    enc = [P(-45, 35), P(40, 35), P(40, -40), P(-45, -40)]
    els += [_poly(enc, "rgba(13,11,9,.6)", "#f2dcb4", 2, -1), box(P(-28, 6)[0], P(-28, 6)[1], 70, 18, "#dcbf94", r=4, at=-1), label(P(-2, -40)[0], P(-2, -40)[1] + 34, "Sphinx", .3, BONE, 28)]
    st = [P(55, 28), P(108, 28), P(108, -24), P(55, -24)]
    vt = [P(55, -38), P(110, -38), P(110, -95), P(55, -95)]
    els += [_poly([P(47, 40), P(119, 40), P(119, -104), P(47, -104)], "rgba(242,201,142,.10)", "rgba(242,201,142,.4)", 1.5, 2.2, style="inferred"),
            label(P(83, -104)[0], P(83, -104)[1] + 34, "one terrace", 2.4, GOLD, 26),
            _poly(st, "rgba(220,191,148,.65)", "#f2dcb4", 2, .5, fx="pop"), _poly(vt, "rgba(220,191,148,.65)", "#f2dcb4", 2, .8, fx="pop"),
            label(P(126, 4)[0], P(126, 4)[1] + 8, "Sphinx Temple", .7, BONE, 28, "start"), label(P(126, -66)[0], P(126, -66)[1] + 8, "Valley Temple", 1.0, BONE, 28, "start")]
    els += [line([P(55, 62), P(55, -122)], 3.4, AMBER, 2.4, "inferred", .6), line([P(109, 62), P(109, -122)], 3.8, AMBER, 2.4, "inferred", .6)]
    cw = [P(55, -60), P(-60, -95), [r1(kc[0] + h * k), r1(kc[1] + 20)]]
    els += [line(cw, 4.6, "#c9ad85", 6, dur=1.2, op=.85), label(r1((cw[1][0] + cw[2][0]) / 2), r1((cw[1][1] + cw[2][1]) / 2 + 40), "causeway", 5.4, DIM, 26)]
    fr = P(-60, 52)
    els += [{"k": "rect", "x": fr[0], "y": fr[1], "w": r1(186 * k), "h": r1(162 * k), "r": 18, "fill": "none", "c": AMBER, "sw": 3.5, "in": 8.2, "fx": "draw", "dur": 1.2},
            label(r1(fr[0] + 93 * k), fr[1] - 18, "one project", 8.8, AMBER, 34)]
    return {"base": "plan", "cam": [1, 889, 500], "els": els}


def s57_clock():
    """s57: charcoal flecks in a mortar joint; a candle burning down step by step beside a bar of 'carbon left' that shrinks with it;
    then a timeline: the textbook date for the pyramids, a short amber band of radiocarbon results a few centuries older, and far to
    the left Schoch's band, dimmed; a small Sphinx with a 'no mortar' tag."""
    els = [box(120, 150, 560, 100, "url(#k-blocks)", "rgba(255,236,206,.4)", 1.5, 4, .3), box(120, 272, 560, 100, "url(#k-blocks)", "rgba(255,236,206,.4)", 1.5, 4, .3),
           box(120, 250, 560, 22, "#d8ccb4", r=0, at=.3)]
    rnd = random.Random(9)
    els += [dot(r1(rnd.uniform(140, 660)), r1(rnd.uniform(254, 268)), r1(rnd.uniform(2.5, 4.5)), "#1a1511", round(2.8 + .03 * k, 2)) for k in range(26)]
    els += [label(700, 268, "charcoal", 3.4, BONE, 28, "start")]
    for k, (hc, hb) in enumerate(((210, 150), (140, 100), (70, 50))):
        x = 190 + 170 * k; by = 740; at = round(8.0 + .8 * k, 2)
        els += [box(x - 20, by - hc, 40, hc, "#efe6d2", "#fff6e6", 1.5, 4, at, fx="pop"), line([[x, by - hc], [x, by - hc - 12]], at, "#1a1511", 2, draw=False),
                glow(x, by - hc - 26, 40, at, .9, "fire"), {"k": "poly", "p": ellipse(x, by - hc - 24, 7, 14, 10), "fill": "#ffd08a", "c": "none", "w": 0, "in": at},
                box(x + 34, by - hb, 18, hb, BLUE, r=3, at=round(at + .1, 2), fx="fill", dur=.4)]
    els += [label(360, 470, "carbon left", 8.4, BLUE, 28)]
    X = lambda bce: r1(820 + (7500 - bce) / 6000 * 840)
    ay = 600
    els += [line([[X(7500), ay], [X(1500), ay]], 11.6, BONE, 2.5, dur=.6)]
    els += [line([[X(v), ay - 8], [X(v), ay + 8]], 11.8, BONE, 1.6, draw=False) for v in (7000, 5000, 3000)] + \
           [label(X(v), ay + 44, t, 11.8, DIM, 24) for v, t in ((7000, "7000 BCE"), (5000, "5000"), (3000, "3000"))]
    els += [line([[X(2560), ay - 40], [X(2560), ay + 8]], 12.0, BONE, 3, dur=.3), label(X(2560), ay + 80, "textbook", 12.2, BONE, 26)]
    els += [box(X(2934), ay - 34, X(2660) - X(2934), 22, AMBER, r=6, at=13.6, fx="pop"), label(X(2800) - 10, ay - 50, "radiocarbon", 13.8, AMBER, 26, "end")]
    els += [box(X(7000), ay - 34, X(5000) - X(7000), 22, BLUE, r=11, at=15.6, op=.35, fx="pop"), label(r1((X(7000) + X(5000)) / 2), ay - 50, "Schoch", 15.8, BLUE, 26)]
    els += [{"k": "sphinx", "x": 1310, "y": 330, "w": 280, "in": 17.6, "fx": "rise"}] + chip(1310, 390, "no mortar", DIM, 18.4, 26)
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s58_verdict():
    """s58: the worn wall at dusk; a clock face drawn on the rock whose hands spin and blur (it cannot be read); 'stone', 'salt',
    'water'; a lilac '?' over the far-left end of the timeline; 'Awaiting evidence'."""
    els, fxs = wall16(110, 150, 880, 610, -1, -1, -1)
    els += [box(110, 150, 880, 610, "rgba(228,140,80,.10)", r=4, at=-1), glow(900, 200, 360, -1, .25, "fire")]
    cx, cy, R = 550, 430, 120
    els += [{"k": "circle", "x": cx, "y": cy, "r": R, "fill": "rgba(18,13,10,.55)", "c": BONE, "w": 3, "in": 4.6, "fx": "pop"}]
    els += [line([[r1(cx + (R - 18) * math.cos(math.radians(a))), r1(cy + (R - 18) * math.sin(math.radians(a)))], [r1(cx + R * math.cos(math.radians(a))), r1(cy + R * math.sin(math.radians(a)))]],
                 4.8, BONE, 3, draw=False) for a in range(0, 360, 30)]
    for k in range(10):
        a = math.radians(-90 + 41 * k)
        els.append(line([[cx, cy], [r1(cx + 92 * math.cos(a)), r1(cy + 92 * math.sin(a))]], round(5.6 + .16 * k, 2), BONE, 4, draw=False, op=round(.25 + .05 * (k % 3), 2)))
        els.append(line([[cx, cy], [r1(cx + 64 * math.cos(a * 2.3)), r1(cy + 64 * math.sin(a * 2.3))]], round(5.65 + .16 * k, 2), AMBER, 5, draw=False, op=.3))
    els += [dot(cx, cy, 8, BONE, 5.6)]
    for k, (t, x, y) in enumerate((("stone", 300, 250), ("salt", 790, 300), ("water", 760, 610))):
        els.append(label(x, y, t, round(7.7 + .8 * k, 2), ("#e7cfa6", "#f7f3ea", BLUE)[k], 32))
    X = lambda yr: r1(1090 + (yr + 10000) / 10000 * 560)
    ay = 640
    els += [line([[X(-10000), ay], [X(0), ay]], .4, BONE, 2.5, dur=.6), box(X(-7000), ay - 40, X(-5000) - X(-7000), 18, BLUE, r=9, at=.6, op=.7),
            dot(X(-2530), ay, 9, AMBER, .6), label(X(-2530), ay + 44, "Khafre", .7, AMBER, 26), label(X(-6000), ay + 44, "Schoch", .7, BLUE, 26)]
    els += question(X(-6000), ay - 70, 10.4, 80)
    els += chip(1370, 300, "Awaiting evidence", GRADE["awaiting"], 11.8, 30)
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


# ================================================================ chapter 5: The ledger
def mini_pyr(cx, by, w, at, op=1.0):
    h = w * .64
    return [_poly([[cx - w / 2, by], [cx, by - h], [cx + w / 2, by]], "rgba(242,220,180,.16)", "#f2dcb4", 2, at, op=op)]


def s59_ledger():
    """s59 + s60: a ledger board, five rows, each a small picture at the left (the void, the corridor, Khafre's shafts, the door,
    the Sphinx); each row lights as it is named and its grade chip pops as the grade is said; row 4 gets two chips."""
    els = [box(110, 130, 1560, 660, "rgba(18,13,10,.75)", "rgba(255,236,206,.3)", 2, 18, .2)]
    rows = [205, 330, 455, 580, 705]
    names = ["void above the Gallery", "corridor behind the face", "pillars under Khafre", "doors in the shafts", "a far older Sphinx"]
    t_row = [.4, 3.8, 7.3, 11.1, 17.8]
    for k, (y, t) in enumerate(zip(rows, names)):
        els += [box(130, y - 55, 1520, 110, "rgba(242,201,142,.10)", "rgba(242,201,142,.35)", 1.5, 12, t_row[k], fx="pop"),
                label(370, y + 11, t, round(t_row[k] + .1, 2), BONE, 32, "start")]
    ix = 245
    y = rows[0]
    els += mini_pyr(ix, y + 40, 150, .5) + [box(ix - 30, y - 22, 46, 12, "rgba(159,208,255,.25)", BLUE, 1.6, 2, .5, style="inferred"), glow(ix - 8, y - 16, 40, .5, .7, "blue")]
    y = rows[1]
    els += mini_pyr(ix, y + 40, 150, .6) + [box(ix - 46, y + 8, 22, 8, BLUE, r=1, at=.6)]
    y = rows[2]
    els += mini_pyr(ix, y + 10, 110, .7) + [line([[ix - 20 + 10 * j, y + 14], [ix - 20 + 10 * j, y + 50]], .7, LILAC, 2, "claimed", draw=False) for j in range(5)]
    y = rows[3]
    els += [box(ix - 30, y - 34, 60, 64, LIME, "#fff6e6", 2, 3, .8), dot(ix - 12, y - 18, 5, COP, .8), dot(ix + 12, y - 18, 5, COP, .8)]
    y = rows[4]
    els += [{"k": "sphinx", "x": ix, "y": y + 34, "w": 150, "in": .9}]
    cx0 = 1080
    els += chip(cx0, rows[0], "Strong evidence", GRADE["strong"], 2.4, a="start")
    els += chip(cx0, rows[1], "Established", GRADE["established"], 6.0, a="start")
    els += chip(cx0, rows[2], "Awaiting evidence", GRADE["awaiting"], 9.6, a="start")
    els += chip(cx0, rows[3], "Established", GRADE["established"], 13.6, a="start") + chip(cx0 + 240, rows[3], "Open question", GRADE["open"], 16.8, a="start")
    els += chip(cx0, rows[4], "Awaiting evidence", GRADE["awaiting"], 21.0, a="start")
    return {"base": "dark", "stars": 30, "cam": [1, 889, 500], "els": els}


def s61_open():
    """s61 (first half): the void on the x-ray model: 'Open question', what it is, what it was for."""
    R = gp_parts(void=True, nfc=True)
    base = iso(R["gp"] + R["rest"] + R["gg"] + R["kc"] + R["qc"] + R["bv"] + R["nfc"] + iso3d.ground(140, grid=35), 889, 760, 3.6, -28, .4, el=.26, at=-1)
    vc = void_centre()
    vx, vy = P3(base, vc, 2.0)
    els = [glow(889, 560, 620, -1, .16, "lamp"), base, glow(vx, vy, 150, .3, .7, "blue")]
    els += chip(vx, vy - 150, "Open question", GRADE["open"], .8, 30)
    els += [label(vx - 120, vy + 70, "what it is", 1.6, ICE, 28, "end"), label(vx + 120, vy + 70, "what it was for", 2.8, ICE, 28, "start")]
    return {"base": "dark", "stars": 70, "cam": [1.45, vx, vy - 20], "els": els}


def s61_ruled():
    """s61 (second half): Khafre in section with Alvarez's cone, about a fifth of the pyramid, shaded; inside it a chip 'Ruled out:
    hidden chambers'; outside the cone, left plain."""
    m, cx, gy, H, Bh, P, cone = alvarez_geo()
    els = khafre_section(P, H, Bh) + [{"k": "poly", "p": cone, "fill": "rgba(159,208,255,.22)", "c": BLUE, "w": 2, "in": .3}, label(r1(cone[1][0] + 60), r1(cone[1][1] + 40), "about a fifth", .6, ICE, 28, "start")]
    cc = P(0, H * .42)
    els += [line([[cc[0] + 4, cc[1]], [1150, cc[1]]], 4.3, GRADE["ruled"], 2.4, dur=.4), dot(cc[0], cc[1], 7, GRADE["ruled"], 4.3)]
    els += chip(1160, cc[1], "Ruled out: hidden chambers", GRADE["ruled"], 4.4, 28, a="start")
    els += [label(*P(-Bh * .62, 22), "not looked at", 5.6, DIM, 26)]
    return {"base": "dark", "stars": 50, "floor": 760, "cam": [1, 889, 500], "els": els}


def s62_mixed():
    """s62: the plateau diorama: the corridor and the void glow (solid and dashed); Khafre's claimed shafts and the old-Sphinx date
    fade as lilac dots; a central 'Mixed record' chip; a camera lights by the corridor; a data file and a clock grey out by the
    doubtful ones; at 'bold questions', a few figures with lamps walk back towards the pyramids and the Sphinx."""
    base = plateau(spin=0.0, cy=560)
    pp = plateau_pts()
    (kx, _, kz) = pp["khafre"]
    sx, sy_, sz = pp["sphinx"]
    vc = void_centre()
    V = P3(base, (0, vc[1] + 4, vc[0])); C = P3(base, (0, 22, -95)); K = P3(base, (kx, 0, kz)); S = P3(base, (sx, 0, sz))
    els = [glow(889, 560, 700, -1, .14, "lamp"), base,
           glow(*V, 60, .8, .9, "blue"), dot(*V, 7, BLUE, .8), glow(*C, 50, 1.0, .9, "lamp"), dot(*C, 6, GREEN, 1.0),
           ov(base, [{"t": "line", "p": [[kx + dx, -2, kz], [kx + dx, -60, kz]], "c": LILAC, "w": 3, "style": "claimed"} for dx in (-40, -15, 15, 40)], 1.6, fx="fade"),
           {"k": "circle", "x": S[0], "y": S[1] - 6, "r": 46, "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 1.8}]
    els += chip(889, 170, "Mixed record", GRADE["mixed"], 3.0, 34)
    # a camera by the corridor
    cxm, cym = C[0] - 70, C[1] + 40
    els += [box(cxm - 26, cym - 16, 52, 34, "#2a231c", GREEN, 2.5, 6, 8.4, fx="pop"), {"k": "circle", "x": cxm, "y": cym + 1, "r": 10, "fill": "#1d2a33", "c": GREEN, "w": 2.5, "in": 8.4},
            glow(cxm, cym, 70, 8.6, .7, "lamp")]
    # a data file by Khafre, a clock by the Sphinx: grey
    fx_, fy_ = K[0] + 90, K[1] - 120
    els += [box(fx_ - 22, fy_ - 28, 44, 56, "rgba(160,160,160,.25)", "#8a8a8a", 2, 5, 11.6, fx="pop")] + \
           [line([[fx_ - 12, fy_ - 12 + 10 * j], [fx_ + 12, fy_ - 12 + 10 * j]], 11.6, "#8a8a8a", 2, draw=False) for j in range(3)]
    ck = (S[0] + 90, S[1] - 70)
    els += [{"k": "circle", "x": ck[0], "y": ck[1], "r": 26, "fill": "rgba(160,160,160,.2)", "c": "#8a8a8a", "w": 2.5, "in": 13.8, "fx": "pop"},
            line([[ck[0], ck[1]], [ck[0], ck[1] - 16]], 13.9, "#8a8a8a", 2.5, draw=False), line([[ck[0], ck[1]], [ck[0] + 12, ck[1] + 6]], 13.9, "#8a8a8a", 2.5, draw=False)]
    # people with lamps walking back towards the monuments (a trail, older steps fainter)
    for g, (t0, pts) in enumerate(((16.4, ((1180, 790), (1120, 760), (1060, 730))), (17.0, ((560, 790), (610, 760), (660, 730))))):
        for k, (x, y) in enumerate(pts):
            at = round(t0 + .6 * k, 2)
            pe = person(x, y, 34, at, "#e8d6b8", fx="fade")
            if k < len(pts) - 1:
                pe.update(op=.4, keepop=True)
            els += [pe, glow(x + 8, y - 26, 26, at, .7 if k == len(pts) - 1 else .3, "lamp")]
    return {"base": "dark", "stars": 160, "cam": [1, 889, 500], "els": els}


def s63_void_tests():
    """s63: the Great Pyramid model: a thin borehole with a camera reaching the void (dashed: not done); big muon telescopes set
    round the base, their fields of view sweeping the whole pyramid (dashed)."""
    R = gp_parts(void=True)
    base = iso(R["gp"] + R["rest"] + R["gg"] + R["kc"] + R["qc"] + R["bv"] + iso3d.ground(170, grid=35), 889, 700, 2.4, -28, 0, el=.3, at=-1)
    vc = void_centre()
    entry = (-62, 68, 0)
    els = [glow(889, 520, 620, -1, .16, "lamp"), base,
           ov(base, [{"t": "line", "p": [list(entry), [vc[0] - 4, vc[1] + 3, 0]], "c": AMBER, "w": 3, "style": "inferred"}], 3.4, fx="fade")]
    a = P3(base, entry); b = P3(base, (vc[0] - 4, vc[1] + 3, 0))
    els += [dot(*b, 8, AMBER, 4.2), glow(*b, 50, 4.2, .8, "lamp"), label(a[0] - 20, a[1] - 10, "camera", 4.4, AMBER, 28, "end")]
    tel = [(-150, 0, 0), (150, 0, 0), (0, 0, -150), (0, 0, 150)]
    for k, (x, y, z) in enumerate(tel):
        at = round(5.6 + .2 * k, 2)
        els.append(ov(base, [{"t": "box", "x": x, "z": z, "y": 0, "w": 22, "d": 22, "h": 12, "c": "#3d5566", "edge": "#cfe6ff"}], at, fx="rise"))
        tp = P3(base, (x, 12, z))
        for j, tgt in enumerate(((0, 120, 0), (0, 60, -60), (0, 60, 60), (0, 40, 0))):
            q = P3(base, tgt)
            els.append(line([tp, q], round(at + .5 + .1 * j, 2), BLUE, 1.6, "inferred", .5, op=.6))
    els += [label(*P3(base, (150, 0, 0)), "muon telescopes", 6.2, BLUE, 28)]
    els[-1]["y"] = r1(els[-1]["y"] + 60)
    return {"base": "dark", "stars": 60, "cam": [1, 889, 480], "els": els}


def s64_khafre_tests():
    """s64: Khafre's cut: an open-data file glows and sends arrows outward; a seismic thump and echo arcs; a drill rig with a string
    648 m down and a core coming up (all dashed: not done)."""
    s = kcut(at=-1)
    s["els"] += kshafts(.2, op=.35, spiral=False, dt=0) + kcubes(.2, op=.35)
    fx_, fy = 1380, 170
    s["els"] += [box(fx_ - 30, fy - 38, 60, 76, "#e9dcc4", "#fff6e6", 2, 6, 1.0, fx="pop"), glow(fx_, fy, 90, 1.1, .5)]
    for k, a in enumerate((200, 250, 290, 340)):
        s["els"].append(arrow([[r1(fx_ + 50 * math.cos(math.radians(a))), r1(fy + 50 * math.sin(math.radians(a)))], [r1(fx_ + 92 * math.cos(math.radians(a))), r1(fy + 92 * math.sin(math.radians(a)))]],
                              round(1.4 + .12 * k, 2), AMBER, 2.5, "inferred", .4, False))
    s["els"] += [label(fx_ + 60, fy + 70, "open data", 1.6, AMBER, 30, "start")]
    tx = 380
    s["els"] += [box(tx - 34, KGY - 34, 68, 34, "#8c7152", "#f2dcb4", 2, 6, 4.0, fx="pop"), label(tx, KGY - 54, "seismic survey", 4.4, BLUE, 30)]
    s["els"] += [{"k": "line", "p": ellipse(tx, KGY, r, r, 14, 40, 140), "c": BLUE, "w": 2.4, "style": "inferred", "curve": True, "in": round(4.4 + .3 * j, 2), "fx": "draw", "dur": .5}
                 for j, r in enumerate((70, 140, 210))]
    rx = 1080
    s["els"] += [line([[rx - 40, KGY], [rx, KGY - 120], [rx + 40, KGY]], 5.6, DIM, 4, dur=.5), line([[rx, KGY], [rx, kD(648)]], 5.9, AMBER, 4, "inferred", 1.2),
                 box(rx + 50, KGY - 110, 24, 100, "#a88a64", "#f2dcb4", 2, 12, 6.8, fx="rise"), arrow([[rx + 62, kD(200)], [rx + 62, KGY + 20]], 6.4, AMBER, 3, "inferred", .8, False),
                 label(rx + 90, KGY - 70, "drill core", 6.2, AMBER, 30, "start")]
    return s


def s65_robot():
    """s65: the shaft's side cut: a small robot, dashed, beyond the second stone, its lamp lighting the unknown dark."""
    els = side_cut() + interior(-1, hole=True, stone=True)
    rx, ry, s_ = 1530, Y1, 2.2
    els += [box(rx - 26 * s_, ry - 30 * s_, 52 * s_, 26 * s_, "none", BONE, 2.4, 8, 1.2, style="inferred"),
            {"k": "circle", "x": rx - 16 * s_, "y": ry - 6 * s_, "r": 4 * s_, "c": BONE, "w": 2, "style": "inferred", "in": 1.2},
            {"k": "circle", "x": rx + 16 * s_, "y": ry - 6 * s_, "r": 4 * s_, "c": BONE, "w": 2, "style": "inferred", "in": 1.2},
            glow(rx - 70, ry - 70, 120, 1.8, .7, "lamp"), label(rx, Y0 - 30, "the next robot?", 2.2, BONE, 28)]
    return {"base": "dark", "cam": [1.15, 1250, 540], "els": els}


def s66_hearth():
    """s66: the pit wall in section: under the weathered layer, a small hearth with charcoal glows; a ring, and a radiocarbon tag:
    'dated?'."""
    els = []
    for k, (y, c) in enumerate(((240, "#a88a64"), (340, "#8f7350"), (440, "#a07f5a"), (540, "#7d6448"), (640, "#8f7350"))):
        els.append(box(80, y, 1620, 100, c, r=0, at=-1))
    wl = [[80, 240]] + [[x, r1(300 + 18 * math.sin(x / 61.0) + 10 * math.sin(x / 17.0))] for x in range(80, 1701, 30)] + [[1700, 240]]
    els += [_poly(wl, "rgba(232,207,166,.75)", "#f2dcb4", 1.6, -1), box(80, 240, 1620, 540, "url(#k-speck)", r=0, at=-1),
            line([[80, 240], [1700, 240]], -1, "#e7cfa6", 2, draw=False), label(1640, 280, "weathered", .3, "#3a2c1e", 26, "end", halo=False)]
    hx, hy = 860, 380
    els += [{"k": "poly", "p": ellipse(hx, hy, 110, 26, 20, 0, 180), "fill": "#1a1511", "c": "#5a4632", "w": 2, "in": 3.6}, glow(hx, hy + 6, 120, 3.8, .8, "fire")]
    rnd = random.Random(12)
    els += [dot(r1(hx + rnd.uniform(-80, 80)), r1(hy + rnd.uniform(4, 16)), 4, "#0d0b09", 3.8) for _ in range(12)]
    els += [ring(hx, hy + 8, 130, 5.0, AMBER, 3, dur=.6), line([[hx + 130, hy + 8], [hx + 250, hy + 8]], 5.4, AMBER, 2.4, dur=.3)] + chip(hx + 260, hy + 8, "dated?", AMBER, 5.6, 30, a="start")
    return {"base": "dark", "cam": [1, 889, 500], "els": els}


def s67_close():
    """s67: Giza at night from far off, the three pyramids dark against the stars; faint blue muon streaks fall like fine rain through
    the Great Pyramid; a soft glow where the void is; the picture holds for the end card."""
    gy = 690
    els = [_poly([[960, gy], [1210, gy - 300], [1460, gy]], "#1c1712", "rgba(255,226,190,.25)", 1.5, -1),
           _poly([[1380, gy], [1500, gy - 140], [1620, gy]], "#1a1511", "rgba(255,226,190,.2)", 1.5, -1),
           _poly([[420, gy], [760, gy - 410], [1100, gy]], "#221b15", "rgba(255,226,190,.3)", 1.5, -1),
           _poly([[760, gy - 410], [1100, gy], [760, gy]], "rgba(0,0,0,.25)", at=-1)]
    els += [glow(720, gy - 230, 90, 1.0, .75, "blue"), glow(720, gy - 230, 40, 1.4, .9, "blue")]
    rnd = random.Random(31)
    for k in range(40):
        x = r1(rnd.uniform(440, 1080)); y0 = r1(rnd.uniform(110, 300))
        els.append(line([[x, y0], [r1(x + rnd.uniform(-12, 12)), gy + 40]], round(.4 + .15 * k, 2), BLUE, 1.0, dur=1.6, op=round(rnd.uniform(.2, .45), 2)))
    return {"base": "sky", "tod": "night", "ground": gy, "groundc": "#211a14", "sun": False, "moon": [1550, 200, 24], "cam": [1, 889, 500], "els": els}


# ================================================================ the film
def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


def under_giza():
    void, vbase, vpos = s01_void()
    shots = [None] * 70            # ep shot k = script shot s(k+1); 68 is the second half of s61; 69 a closer framing of s20
    shots[0] = void
    shots[1] = {"cam": [1, 889, 500]}
    shots[2] = s03_khafre_hook()
    shots[3] = s04_door()
    shots[4] = s05_sphinx_rain()
    shots[5] = s06_plateau()
    shots[6] = {"cam": [1, 889, 500]}
    shots[8] = s09_size()
    shots[9] = s10_rooms()
    shots[10] = s11_sky()
    shots[11] = s12_xray()
    shots[12] = s13_detectors()
    s14, bvc = s14_s15_void()
    shots[13] = {"cam": [1.9, bvc[0] - 60, bvc[1] + 80]}
    shots[14] = {"cam": [2.6, bvc[0] + 120, bvc[1] - 20]}
    shots[15] = s16_sigma()
    shots[16] = s17_shape()
    shots[17] = s18_relieve()
    shots[18] = s19_nfc()
    shots[19], cam69 = s20_probe()
    shots[69] = {"cam": cam69}
    shots[20] = s21_corridor()
    shots[21] = s22_both()
    shots[23] = s24_stack()
    shots[24] = s25_claim()
    shots[25] = s26_tremble()
    shots[26] = s27_knock()
    shots[27] = s28_shuttle()
    shots[28] = s29_depth()
    shots[29] = s30_faint()
    shots[30] = s31_alvarez()
    shots[31], cam32 = s32_review()
    shots[32] = {"cam": cam32}
    shots[33] = s34_paper()
    shots[34] = s35_shafts()
    shots[35] = s36_square()
    shots[36] = s37_climb()
    shots[37] = s38_doorview()
    shots[38] = s39_cut()
    shots[39] = s40_both_doors()
    shots[40] = {"cam": [1.7, 1110, 620]}
    shots[41] = s42_inside()
    shots[42] = s43_marks()
    shots[43] = s44_sky()
    shots[44] = s45_record()
    shots[45] = s46_unknown()
    shots[46] = s47_sphinx()
    shots[47] = s48_wall()
    shots[48], _ = s49_dates()
    shots[49] = s50_seismic()
    salt, cam51 = s51_salt()
    shots[50] = {"cam": cam51}
    shots[51] = s52_karst()
    shots[52] = s53_runoff()
    shots[53] = s54_reader()
    shots[54] = s55_temple()
    shots[55] = s56_plan()
    shots[56] = s57_clock()
    shots[57] = s58_verdict()
    shots[58] = s59_ledger()
    shots[60] = s61_open()
    shots[68] = s61_ruled()
    shots[61] = s62_mixed()
    shots[62] = s63_void_tests()
    shots[63] = s64_khafre_tests()
    shots[64] = s65_robot()
    shots[65] = s66_hearth()
    shots[66] = s67_close()
    beat_adds = {16: (s41_djedi(), [1.7, 1110, 620]), 20: (salt, cam51)}
    line_adds = {(4, 1): (s14, [1.9, bvc[0] - 60, bvc[1] + 80])}
    # aliases: returns to (or new framings of) an earlier panel. s8 and s23 are folded into s9 and s24 (the chapter card holds
    # their sentence), s60 is the ledger board continuing; 67 is unused.
    alias = {1: 0, 6: 5, 7: 8, 13: 12, 14: 12, 22: 23, 32: 31, 40: 38, 50: 47, 59: 58, 67: 37, 69: 19}
    for k in alias:
        if shots[k] is None:
            shots[k] = {"cam": [1, 889, 500]}
    assert all(sh is not None for sh in shots)
    L = LINES
    beats = [B(r, f, ls, **kw) for (r, f, kw), ls in zip(BEATS, L)]
    ep = {"id": "lf-under-giza", "code": "LF.01", "series": "Under Giza", "title": "Under Giza", "case": "under-giza",
          "verdict": "mixed", "claim": "What is really under Giza?", "mood": "mystery",
          "hook_text": "What's *really* under Giza?", "beats": beats, "shots": shots,
          "sources": SOURCES, "post": POST, "hashtags": ["#Giza", "#GreatPyramid", "#Sphinx", "#AncientEgypt", "#Archaeology"],
          "aspect": "16:9", "intro_title": "Under Giza", "yt_title": "Under Giza: the hidden rooms that are real, and the rumours",
          "description": DESCRIPTION, "end_line": "A room nobody has entered, still letting the sky through."}
    return remix(ep, alias=alias, line_adds=line_adds, beat_adds=beat_adds)


BEATS = [("hook", 0, {}), ("title", 6, {"intro": True}),
         ("world", 8, {"chapter": "Particles from space"}), ("collision", 10, {}), ("cost", 12, {}), ("reversal", 16, {}), ("collision", 18, {}), ("tag", 21, {}),
         ("world", 23, {"chapter": "Pillars under Khafre"}), ("collision", 24, {}), ("cost", 27, {}), ("reversal", 30, {}), ("tag", 33, {}),
         ("world", 34, {"chapter": "Doors in the dark"}), ("collision", 36, {}), ("cost", 38, {}), ("reversal", 40, {}), ("tag", 44, {}),
         ("world", 46, {"chapter": "The Sphinx and the rain"}), ("collision", 47, {}), ("cost", 50, {}), ("reversal", 54, {}), ("tag", 57, {}),
         ("weigh", 58, {"chapter": "The ledger"}), ("test", 62, {}), ("close", 66, {})]

LINES = [
    [  # 0
        "[d:intrigue][sfx:boom][act:hushed wonder, drawing them in]Inside the Great Pyramid of Egypt, there's a space at least ^thirty metres long that ^*nobody* has ever entered. [go:1|1.4][act:the reveal, quietly delighted]We only know about it because of particles falling from ^*space*.",
        "[d:tension][go:2|1.6][act:quickening, a teaser][tune:level]Next door, a team says shafts plunge more than half a kilometre under another ^pyramid. [go:3|1.6][act:same pace, intrigued][tune:level]In a narrow shaft, a little stone ^door with two copper ^pins. [go:4|1.6][act:same pace, a raised eyebrow][tune:fall]And out front, a Sphinx that one geologist says was worn by ^*rain*.",
        "[d:wonder][go:5|1.6][act:the child's question, wide-eyed][tune:rise]So what's ^really under Giza?",
    ],
    [  # 1
        "[d:calm][act:warm, setting out]Under ^Giza. [act:the promise, friendly][tune:fall]The real rooms, the ^rumours, and how to tell them ^apart.",
    ],
    [  # 2
        "[d:calm][act:admiring, unhurried]The Great Pyramid at Giza, credited to the pharaoh ^Khufu, about four and a half thousand years ago. [p:0.93][act:giving the size, a touch of awe]A hundred and forty-six metres tall when it was built: about as tall as a forty-storey ^building.",
        "[d:calm][go:9|1.6][act:guiding the eye, unhurried]Inside, three known rooms: the King's ^Chamber, the ^Queen's, and the long, sloping Grand ^Gallery.",
    ],
    [  # 3
        "[d:build][act:curious, the child's question][tune:rise]How do you see inside a mountain of stone without moving a ^block? [act:explaining, a spark of wonder]Cosmic rays from space hit our air and make [sfx:shimmer]^muons, heavy cousins of the ^electron, raining down all the ^time. [act:playful, an aside]A few are going through your hand right ^now.",
        "[d:build][go:11|1.6][p:0.93][act:patient, the analogy]It works like an ^X-ray. [act:laying it out][tune:level]Stone stops some muons. [act:the payoff, clear and simple][tune:fall]Empty space lets more of them ^*through*. [p:0.93][act:explaining, step by step]Count them from every direction for months, and a hollow shows up as a bright ^patch.",
    ],
    [  # 4
        "[d:build][act:brisk, matter of fact]From {2015|twenty fifteen}, a project@noun called ^ScanPyramids set three kinds of detector inside the pyramid, and ^out. [p:0.93][act:the method, careful]Different tools, one question: if they all agree, it isn't a fault in one ^machine.",
        "[d:reveal][sfx:hit][act:the discovery, measured]In {2017|twenty seventeen}, all three saw the same thing: extra muons, from a space ^above the Grand Gallery. [go:14|1.4][p:0.9][act:letting the size land]At least ^*thirty* metres long, about three buses end to end, with a cross-section much like the Gallery's ^own. [go:15|1.6][p:0.93][act:precise, quietly impressed]Each signal cleared the bar physicists set before they say ^discovery.",
    ],
    [  # 5
        "[d:tension][act:curious, the open part][tune:rise]So what ^is it? [act:honest, plain]The physicists can't yet tell its shape: one space or several, level or ^sloping. [go:17|1.6][act:fair, the archaeologist's view]The Giza archaeologist Mark ^Lehner guessed a space to take weight off the Gallery's ^roof. [act:an everyday picture, light]A bit like an arch over a door, steering the load ^around it.",
    ],
    [  # 6
        "[d:reveal][act:leaning in, fresh news]Then came a ^test. [p:0.93][act:explaining, clear]In {2023|twenty twenty-three}, muons pinned down a second, smaller space, behind the huge gabled blocks over the old entrance@noun. [p:0.9][act:precise]A corridor about nine metres long, and two metres by ^two.",
        "[d:build][go:19|1.6][act:quiet, careful, step by step]Radar and ultrasound fixed its exact ^position. [go:69|1.4][act:quiet, careful]Then a camera thinner than a pencil slid in through a joint in the ^stones. [go:20|1.6][gap:0.4][act:hushed, the reveal][tune:fall]An ^*empty* corridor, under a gabled ^roof. [act:quiet satisfaction][tune:fall]^Right where the muons said.",
    ],
    [  # 7
        "[d:verdict][p:0.95][act:calm, landing it]That's how a new tool earns ^trust: it makes a prediction, and a camera ^checks it. [act:quieter, a little longing][tune:fall]The Big Void hasn't had its camera ^yet.",
    ],
    [  # 8
        "[d:calm][act:plain, placing it]Next door stands the pyramid of ^Khafre, Khufu's son, about a hundred and forty-three metres tall when ^new. [p:0.93][act:doing the sum, vivid]Now stack four and a half of those pyramids, one below another, down into the ^rock. [act:letting it land][tune:fall]{648|Six hundred and forty-eight} metres. [act:the kicker, dry][tune:fall]That's how deep the newest claim ^goes.",
    ],
    [  # 9
        "[d:build][act:reporting the announcement, brisk]In March {2025|twenty twenty-five}, in Italy, the radar engineer Filippo ^Biondi and the chemist Corrado ^Malanga said satellite radar had found ^eight shafts under Khafre, wrapped in spiral paths. [act:the big claim, eyebrows up]And far below, [sfx:hit]two giant ^cubes, each about eighty metres a ^side.",
        "[d:build][go:25|1.6][act:fair, genuinely interested]Their idea is a clever ^one. [p:0.93][act:explaining, patient]Radar from orbit can't see through stone, and they say so ^themselves. [p:0.93][act:explaining, the idea]But the ground is always trembling, very ^slightly. [go:26|1.6][act:the analogy, clear]Measure how the surface trembles, they argue, and you can map what lies beneath, like knocking on a wall to find a ^hollow.",
    ],
    [  # 10
        "[d:build][act:fair, the check][tune:rise]How deep can radar from space really ^reach? [act:storytelling, a nice find]In {1981|nineteen eighty-one}, radar on the Space Shuttle looked through the Sahara's dry sand and found buried river ^valleys. [go:28|1.6][p:0.9][act:precise]Field checks: one or two metres down. [act:same, precise]Lab tests: five or ^so. [p:0.9][act:the punchline, deadpan][tune:fall]Six hundred and forty-eight metres is more than a hundred times ^that.",
        "[d:list][go:29|1.6][act:fair, even][tune:level]The radar specialist Lawrence ^Conyers called it a huge ^exaggeration: trembles from that deep, he said, would be too faint to read@present. [act:same, firm][tune:fall]Zahi ^Hawass, Egypt's former antiquities minister, said the work had neither Egypt's permission nor a scientific ^basis.",
    ],
    [  # 11
        "[d:reveal][act:a twist of history, warm]The very first muon X-ray of any pyramid was taken inside ^Khafre's, from {1967|nineteen sixty-seven}, by the physicist Luis ^Alvarez and his ^team. [p:0.9][act:precise, the result]More than a million muons, about a fifth of the pyramid seen, and no hidden chambers of the usual ^size.",
        "[d:reveal][go:31|1.6][p:0.95][act:the turn][tune:rise]And the shafts ^below? [act:plain, sober][tune:fall]So far, no peer-reviewed ^paper. [p:0.93][act:explaining, simple]Peer review: experts check the method and the sums before a journal prints a ^study. [go:32|1.4][act:sober, a heavy fact]And on the tenth of August {2026|twenty twenty-six}, the journal Remote Sensing ^withdrew the team's earlier radar study of the Great Pyramid, for serious flaws in its methods and ^statistics. [act:fair, even][tune:fall]The authors say they ^disagree.",
    ],
    [  # 12
        "[d:verdict][act:warm, fair]Bold ideas deserve a ^test, and this one could have ^one. [act:the verdict, a small smile][tune:level]Until it passes, the pillars stand... [act:gently final][tune:fall]on ^*paper*.",
    ],
    [  # 13
        "[d:calm][act:plain, orienting]Back inside the Great Pyramid, two narrow shafts climb out of the Queen's ^Chamber, one north, one ^south. [p:0.93][act:intrigued, a little detail]Their mouths stayed hidden behind the chamber walls until {1872|eighteen seventy-two}, and as far as we know, neither reaches the ^outside.",
        "[d:aside][go:35|1.6][p:0.93][act:showing how small]Each is roughly twenty centimetres square: the width of a sheet of printer ^paper. [act:light, amused]Too narrow for a ^person. [act:a playful image]Barely wide enough for a ^*cat*.",
    ],
    [  # 14
        "[d:build][act:storytelling, onward]In {1993|nineteen ninety-three}, the engineer Rudolf ^Gantenbrink sent a small robot up the southern shaft, named ^Upuaut, after an Egyptian god called the opener of the ^ways. [sfx:whoosh][act:the discovery, hushed]More than sixty metres in, its lamp lit [go:37|1.4][sfx:hit]a small stone ^door, with two copper ^pins.",
    ],
    [  # 15
        "[d:tension][act:the wait, wry]Then the work ^stopped. [act:plain, counting]Nine years later, in {2002|two thousand and two}, a new robot drilled a small hole through the door, live@adj on ^television, and slid a camera ^through. [sfx:hit][act:the anticlimax, wry][tune:fall]About twenty centimetres on: ^*another* stone. [go:39|1.6][act:plain, a new detail]And the northern shaft is blocked by a door just like ^it.",
    ],
    [  # 16
        "[d:reveal][act:a new clue, intrigued]In {2011|twenty eleven}, another robot, ^Djedi, slipped a bendy snake camera through the same hole, and looked ^around. [go:41|1.6][act:describing, careful][tune:level]The back of the door is ^polished. [act:same careful pace][tune:level]One copper pin ends in a small, neat ^loop. [sfx:shimmer][act:the reveal, hushed][tune:fall]And on the floor: marks in red ^*paint*.",
        "[d:calm][go:42|1.6][act:the sensible answer, calm]Most likely builders' notes, perhaps ^numbers. [act:explaining, a nice detail]Work gangs left red marks elsewhere in the pyramid too, like a carpenter's pencil marks on ^wood. [go:43|1.6][act:respectful, unhurried][tune:rise]And the shafts themselves? [act:explaining, gentle]In Egyptian belief, the king's spirit would rise to the sky, and many Egyptologists think these shafts served that journey, not fresh ^air.",
    ],
    [  # 17
        "[d:verdict][act:fair, the critics' question][tune:rise]Was something found, and kept ^quiet? [act:even, careful]What each robot saw was ^shown: on film, on live@adj television, and in a robotics journal in {2013|twenty thirteen}. [go:45|1.6][act:the landing, quiet][tune:fall]The doors are ^real. [act:hushed, inviting][tune:fall]What lies past the last stone, nobody yet ^knows.",
    ],
    [  # 18
        "[d:calm][act:admiring, unhurried]Now, out front: the Great ^Sphinx. [p:0.93][act:giving the size, amazed]Seventy-three metres of lion, carved not from blocks but from the ^bedrock. [act:the image, vivid]The carvers dug a deep pit around a hill of rock, and shaped what was ^left.",
    ],
    [  # 19
        "[d:build][act:plain, a respectful introduction]Around {1990|nineteen ninety}, Robert ^Schoch, a geologist at Boston University, looked hard at the walls of that ^pit. [act:describing it, a careful eye][tune:level]Rounded, rolling ^layers. [act:same careful eye][tune:level]Deep vertical ^cracks. [act:sympathetic, his view][tune:fall]To him, that's what rain does@verb, running down rock for thousands of ^years.",
        "[d:build][go:48|1.6][p:0.93][act:his logic, clear and fair]But Egypt has been mostly dry for about five thousand ^years. [act:stating his claim, even]So in {1992|nineteen ninety-two}, he dated the first carving to between seven thousand and five thousand ^BCE. [p:0.9][act:the stakes, slower]The usual date, under ^Khafre, is around two and a half thousand BCE: thousands of years ^later. [go:49|1.6][act:his evidence, fair]A seismic survey@noun he joined found the rock under the pit's floor weathered ^unevenly, as if parts had been open to the air ^longer.",
    ],
    [  # 20
        "[d:build][act:the other side, crisp]Other geologists ^answered. [p:0.93][act:explaining, step by step]Lal ^Gauri and his colleagues pointed to ^salt: as moisture dries in the soft layers, crystals grow and push the grains apart, like ice cracking a ^pavement. [act:simple, matter of fact][tune:fall]Rounded walls, no ancient rains ^needed. [go:51|1.6][p:0.93][act:the surprise, delighted]And the deep cracks, they argued, are natural channels cut by underground water, millions of years before any ^carver.",
        "[d:aside][go:52|1.6][act:fair, even-handed]A third geologist, Colin ^Reader, stands in the ^middle: water did the damage, he agrees, but as runoff from the plateau, before Khufu's building works cut it ^off. [go:53|1.6][act:landing his view][tune:fall]His Sphinx is a few ^centuries older than Khafre, not thousands of ^years.",
    ],
    [  # 21
        "[d:reveal][act:turning the page, curious][tune:rise]And the ^archaeology? [act:revealing, clear]The temple in front of the Sphinx is built from blocks cut out of the same ^pit: their layers match the pit walls, like puzzle pieces fitting ^back. [go:55|1.6][act:connecting the dots]It's built like Khafre's own temples, on the same terrace, almost in line with his Valley ^Temple. [act:the logic, clear][tune:fall]Pit, temple and Sphinx look like one project@noun, under ^Khafre.",
        "[d:build][go:56|1.6][act:explaining, the method]There's a clock nearby, too. [p:0.93][act:explaining, patient]Charcoal in the pyramids' mortar came from living wood, and its radiocarbon has faded at a steady pace ever since, like a candle burning ^down. [act:the punchline, precise][tune:fall]Its dates: older than the textbooks, but by centuries, not ^thousands of years. [act:fair, the limit]The Sphinx, cut from bedrock, has no mortar of its own to ^date.",
    ],
    [  # 22
        "[d:verdict][p:0.95][act:fair, sincere]Schoch's ^observation is real: those walls are deeply ^worn. [act:thoughtful, explaining]But weathering is a poor clock: its speed depends on the stone, the salt and the ^water. [act:turning, measured][tune:rise]His ^date? [act:the verdict, level-headed][tune:fall]Still *awaiting ^evidence*.",
    ],
    [  # 23
        "[d:verdict][act:stepping back, calm]So, the ledger. [act:clear, counting them off][tune:level]A void above the Grand Gallery: *strong ^evidence*. [act:same steady pace][tune:level]A corridor behind the north face: ^*established*. [act:same pace][tune:level]Shafts and pillars under Khafre: *awaiting ^evidence*. [act:same pace][tune:level]Stone doors in the Queen's Chamber shafts: ^*established*; what lies beyond them, an *open ^question*. [act:closing the column][tune:fall]A Sphinx thousands of years older than Khafre: *awaiting ^evidence*.",
        "[d:calm][go:60|1.6][p:0.93][act:plain, the open part]Still open: what the void is, and what it was ^for. [go:68|1.6][act:plain, the firm part]And ruled out, in the fifth of Khafre's pyramid that Alvarez could see: hidden chambers of the usual ^size. [go:61|1.6][p:0.95][act:the whole picture, warm]Taken together, Giza's hidden rooms make a *mixed ^record@noun*. [act:fair, clear]The strongest finds come from methods others can repeat; one has already met a ^camera. [act:same, fair][tune:fall]The doubtful ones lean on data others can't yet check, or on a clock that rock can't ^keep. [act:warm, generous]But bold questions sent people back to look, and that's how it should ^work.",
    ],
    [  # 24
        "[d:tension][act:practical, counting them off][tune:rise]What would change our ^minds? [act:same beat][tune:level]For the void, a camera through a small hole, or giant muon telescopes to map it in three ^dimensions. [go:63|1.6][act:same beat][tune:level]For Khafre, open raw data, and a test anyone can repeat: a seismic survey@noun, or a drill core from that ^depth. [go:64|1.6][act:same beat][tune:level]For the doors, a robot past the last ^stone. [go:65|1.6][act:the last one, hopeful][tune:fall]For the Sphinx, one ^dated thing in the pit, like charcoal from an old fire, sealed under the weathered ^rock.",
    ],
    [  # 25
        "[d:wonder][p:0.93][act:quiet, warm]In that stone, a room nobody has entered is still letting the sky's particles ^through. [act:the last word, a smile][tune:fall]Weigh it ^yourself.",
    ],
]

SOURCES = ("Morishima et al. 2017 (doi:10.1038/nature24647) · Procureur et al. 2023 (doi:10.1038/s41467-023-36351-0) · "
           "Elkarmoty et al. 2023 (doi:10.1016/j.ndteint.2023.102809) · Alvarez et al. 1970 (doi:10.1126/science.167.3919.832) · "
           "McCauley et al. 1982 (doi:10.1126/science.218.4576.1004) · Remote Sensing retraction 2026 (doi:10.3390/rs18162679) · "
           "Richardson et al. 2013 (doi:10.1002/rob.21451) · Miatello 2021 (doi:10.5913/jarce.56.2020.a008) · "
           "Dobecki & Schoch 1992 (doi:10.1002/gea.3340070603) · Gauri et al. 1995 (doi:10.1002/gea.3340100203) · "
           "Reader 2001 (doi:10.1111/1475-4754.00009) · Lehner 1992 (doi:10.1017/S0959774300000421) · Bonani et al. 2001 (doi:10.1017/S0033822200038558)")

POST = ("What is really under Giza? A void nobody has entered, found by particles from space; a corridor a camera has seen; "
        "a claim of pillars 648 metres down; two stone doors in a narrow shaft; and a Sphinx some say was worn by rain. Weighed one by one.")

DESCRIPTION = "Inside the Great Pyramid there is a space nobody has entered, found by particles from space. Under the pyramid next door, a team claims shafts more than half a kilometre deep. In a narrow shaft, a stone door with two copper pins. And out front, a Sphinx that one geologist reads as worn by ancient rain.\n\nWe weigh them one claim at a time: what the muon detectors, the robots, the radar and the rock can and cannot tell us, with each challenger at their strongest and every grade stated plainly.\n\nChapters\n{chapters}\n\nSources\nMorishima et al. 2017, Nature, doi:10.1038/nature24647\nProcureur et al. 2023, Nature Communications, doi:10.1038/s41467-023-36351-0\nElkarmoty et al. 2023, NDT & E International, doi:10.1016/j.ndteint.2023.102809\nAlvarez et al. 1970, Science, doi:10.1126/science.167.3919.832\nMcCauley et al. 1982, Science, doi:10.1126/science.218.4576.1004\nBiondi & Malanga 2022, Remote Sensing (retracted), doi:10.3390/rs14205231\nRetraction notice 2026, Remote Sensing, doi:10.3390/rs18162679\nRichardson et al. 2013, Journal of Field Robotics, doi:10.1002/rob.21451\nMiatello 2021, Journal of the American Research Center in Egypt, doi:10.5913/jarce.56.2020.a008\nSchoch 1992, KMT 3(2)\nDobecki & Schoch 1992, Geoarchaeology, doi:10.1002/gea.3340070603\nGauri, Sinai & Bandyopadhyay 1995, Geoarchaeology, doi:10.1002/gea.3340100203\nReader 2001, Archaeometry, doi:10.1111/1475-4754.00009\nLehner 1992, Cambridge Archaeological Journal, doi:10.1017/S0959774300000421\nBonani et al. 2001, Radiocarbon, doi:10.1017/S0033822200038558\nBross et al. 2022, muon tomography proposal, doi:10.48550/arXiv.2202.08184\nLehner & Hawass 2017, Giza and the Pyramids (Thames & Hudson)"


def EPISODES():
    return [under_giza()]
