"""Legacy films rebuilt at the new standard (see rewrite/LEGACY_BRIEF.md): 00.01 Where is the rock going? and 13.01 MKUltra.
Each film is written from scratch as drawn scenes (no text cards), then played as one continuous take with remix().
Element times ("in") are seconds after the camera arrives on a panel; _clock() reads them off the narration itself."""
import math, random, re
from films import like, View, _topo
from f01 import mapshot
from f09 import B
from mural import remix
import illus as I

AU, BONE, AMBER, BLUE, LILAC, GREEN, RED, INK = I.AU, I.BONE, I.AMBER, I.BLUE, I.LILAC, I.GREEN, I.RED, I.INK
SEA_, LAND_ = "#2f5f7a", "#7f9a5a"
STAR = "#f2e6cf"


# ---------------------------------------------------------------- timing: when is a word spoken, counted from a panel's arrival
WPS, SENT, COMMA = 2.7, .32, .1


def _clock(beats):
    """{shot: [(word, seconds after the camera set off for that shot)]} from the beats' own lines and [go:] markers."""
    out, cur, t = {}, None, 0.0
    for b in beats:
        frm = b["visual"]["from"]
        if frm != cur:
            cur, t = frm, 0.0
        else:
            t += .5
        out.setdefault(cur, [])
        for ln in b["lines"]:
            pace = 1.0
            for tok in re.findall(r"\[[^\]]*\]|\{[^}]*\}|[^\s\[\{]+", ln):
                if tok.startswith("["):
                    m = re.match(r"\[go:(\d+)", tok)
                    if m:
                        cur, t = int(m.group(1)), 0.0
                        out.setdefault(cur, [])
                    m = re.match(r"\[p:([\d.]+)\]", tok)
                    if m:
                        pace = float(m.group(1))
                    m = re.match(r"\[gap:([\d.]+)\]", tok)
                    if m:
                        t += float(m.group(1))
                    continue
                words = tok[1:-1].split("|", 1)[1].split() if tok.startswith("{") else [tok]
                for w in words:
                    c = re.sub(r"[^a-z0-9'\-]", "", w.lower().split("@")[0])
                    if c:
                        out[cur].append((c, round(t, 2)))
                    t += 1 / (WPS * pace)
                    if re.search(r"[.?!]['*]*$", w):
                        t += SENT
                    elif re.search(r"[,:;]['*]*$", w):
                        t += COMMA
            t += SENT
    return out


def _at(clk, shot, phrase, k=0, dt=0.0):
    """Seconds after arrival on `shot` when the k-th `phrase` (words) starts."""
    ws = [w for w, _ in clk[shot]]
    ph = [re.sub(r"[^a-z0-9'\-]", "", p) for p in phrase.lower().split()]
    hits = [i for i in range(len(ws) - len(ph) + 1) if ws[i:i + len(ph)] == ph]
    assert len(hits) > k, (shot, phrase, ws)
    return round(clk[shot][hits[k]][1] + dt, 2)


# ---------------------------------------------------------------- drawing helpers
def _land_mask():
    """Outer rings of the land polygons (lon, lat) with their bounding boxes, for a point-in-land test."""
    rings = []
    for poly in _topo():
        r = poly[0]
        xs = [q[0] for q in r]; ys = [q[1] for q in r]
        rings.append((min(xs), max(xs), min(ys), max(ys), r))
    return rings


def _is_land(rings, lon, lat):
    inside = False
    for x0, x1, y0, y1, r in rings:
        if lat < y0 or lat > y1 or lon < x0 or lon > x1:
            continue
        c = False
        for (ax, ay), (bx, by) in zip(r, r[1:] + r[:1]):
            if abs(bx - ax) > 180:                       # a ring broken at the antimeridian: skip the jump
                continue
            if (ay > lat) != (by > lat) and lon < ax + (lat - ay) * (bx - ax) / (by - ay):
                c = not c
        inside = inside or c
        if inside:
            return True
    return False


_GLOBE = {}


def _globe(r=10.0, step=7.5):
    """A spinning Earth for the iso engine: a sphere of quads, each land or sea (Natural Earth outlines), lit from above."""
    key = (r, step)
    if key in _GLOBE:
        return _GLOBE[key]
    rings = _land_mask()
    P = lambda L, b: [round(r * math.cos(b) * math.cos(L), 3), round(r * math.sin(b), 3), round(-r * math.cos(b) * math.sin(L), 3)]
    items = []
    n_l, n_b = int(360 / step), int(180 / step)
    for i in range(n_l):
        L0 = -180 + i * step
        for j in range(n_b):
            b0 = -90 + j * step
            hits = sum(_is_land(rings, L0 + step * fx, b0 + step * fy) for fx, fy in ((.5, .5), (.25, .25), (.75, .25), (.25, .75), (.75, .75)))
            land = hits >= 2
            Lr, Lr1, br, br1 = map(math.radians, (L0, L0 + step, b0, b0 + step))
            Lm, bm = (Lr + Lr1) / 2, (br + br1) / 2
            n = [round(math.cos(bm) * math.cos(Lm), 3), round(math.sin(bm), 3), round(-math.cos(bm) * math.sin(Lm), 3)]
            items.append({"t": "quad", "p": [P(Lr, br), P(Lr1, br), P(Lr1, br1), P(Lr, br1)], "n": n, "c": LAND_ if land else SEA_,
                          "edge": "rgba(18,26,34,.35)", "ew": .6})
    _GLOBE[key] = items
    return items


def _spiral(cx, cy, R, ry, arms=2, a0=0.0, wind=1.7, f0=.14, n=70):
    """Trailing spiral arms of a disc galaxy seen at a tilt (counter-clockwise rotation on screen): one point list per arm."""
    out = []
    for k in range(arms):
        pts = []
        for i in range(n):
            f = f0 + (1 - f0) * i / (n - 1)
            th = a0 + 2 * math.pi * k / arms - wind * math.log(f / f0)
            pts.append([round(cx + R * f * math.cos(th), 1), round(cy - ry * f * math.sin(th), 1)])
        out.append(pts)
    return out


def _galaxy(cx, cy, R, ry, at, a0=0.0, arms=2, c=STAR, dt=.35, seed=3, glowc="lamp"):
    """A disc galaxy drawn as strings of stars: a glowing bulge, then each arm (a main band and fainter side strings),
    then a haze of field stars, thicker toward the centre."""
    r = random.Random(seed)
    els = [I.glow(cx, cy, R * .62, at, .55, glowc), I.glow(cx, cy, R * .3, at, .8, glowc),
           I.oval(cx, cy, R * .5, ry * .5, "rgba(242,230,207,.07)", "none", 0, 1, at), I.oval(cx, cy, R * .1, ry * .14, "#fff4dc", "none", 0, .85, at)]
    sw = max(2.6, R / 90)
    for k, arm in enumerate(_spiral(cx, cy, R, ry, arms, a0)):
        t0 = round(at + .3 + dt * k, 2)
        els.append({"k": "line", "p": arm, "c": c, "w": max(14, R / 14), "curve": True, "op": .07, "keepop": True, "in": t0})
        for j, (df, op, gap) in enumerate(((0, .9, 7), (.035, .5, 11), (-.035, .45, 13))):
            pts = [[round(cx + (x - cx) * (1 + df), 1), round(cy + (y - cy) * (1 + df), 1)] for x, y in arm]
            els.append({"k": "line", "p": pts, "c": c, "w": sw if j == 0 else sw * .8, "dash": "0.1 %.1f" % (gap * R / 300), "curve": True, "op": op, "keepop": True, "in": t0})
    for k in range(int(R / 2.2)):
        a, f = r.uniform(0, 2 * math.pi), r.uniform(.04, 1) ** 1.4
        els.append(I.dot(round(cx + R * f * math.cos(a), 1), round(cy - ry * f * math.sin(a), 1), round(r.uniform(1.0, 2.4), 1), c, round(at + .4 + .004 * k, 3), op=round(r.uniform(.25, .75), 2)))
    return els


def _dino(x, y, s, at, c="#cbbca8"):
    """A small early dinosaur on two legs, side view, schematic (facing right, feet at y)."""
    P = lambda pts: [[round(x + s * u, 1), round(y + s * v, 1)] for u, v in pts]
    body = [(-118, -60), (-72, -66), (-30, -74), (8, -76), (28, -82), (38, -98), (54, -108), (80, -104), (84, -95), (62, -90), (52, -82), (44, -66), (26, -54), (0, -48), (-30, -50), (-72, -56)]
    return [{"k": "poly", "p": P(body), "fill": c, "c": "none", "w": 0, "curve": True, "in": at, "fx": "pop"},
            {"k": "line", "p": P([(-12, -52), (-2, -26), (-10, 0), (2, 0)]), "c": c, "w": 9 * s, "in": at, "fx": "pop"},
            {"k": "line", "p": P([(8, -52), (20, -26), (14, 0), (26, 0)]), "c": c, "w": 9 * s, "in": at, "fx": "pop"},
            {"k": "line", "p": P([(36, -64), (50, -50)]), "c": c, "w": 5 * s, "in": at, "fx": "pop"}]


def _plane(x, y, s, at, c="#cbd2d8"):
    """An airliner in side view, schematic (nose to the right)."""
    body = [[x - 150 * s, y - 6 * s], [x - 120 * s, y - 16 * s], [x + 110 * s, y - 16 * s], [x + 150 * s, y - 4 * s], [x + 110 * s, y + 14 * s], [x - 130 * s, y + 12 * s]]
    tail = [[x - 140 * s, y - 12 * s], [x - 168 * s, y - 62 * s], [x - 146 * s, y - 62 * s], [x - 108 * s, y - 14 * s]]
    wing = [[x - 20 * s, y + 4 * s], [x + 40 * s, y + 4 * s], [x - 40 * s, y + 46 * s], [x - 64 * s, y + 46 * s]]
    return [{"k": "poly", "p": tail, "fill": c, "c": "none", "w": 0, "in": at}, {"k": "poly", "p": body, "fill": c, "c": "none", "w": 0, "curve": True, "in": at},
            {"k": "poly", "p": wing, "fill": "#9aa3ab", "c": "none", "w": 0, "in": at}] + \
           [I.dot(round(x + (-90 + 22 * k) * s, 1), round(y - 4 * s, 1), 3.2 * s, "#3a4048", at) for k in range(9)]


def _bg(x, y):
    """The colour of the dark base at (x, y) (its radial gradient), to paint something out."""
    d = min(1.0, math.hypot((x - 500) / 2470, (y - 468) / 3420))
    a, b = (0x3d, 0x2f, 0x22), (0x0d, 0x0b, 0x09)
    return "#%02x%02x%02x" % tuple(round(u + (v - u) * d) for u, v in zip(a, b))


# ---------------------------------------------------------------- 00.01 Where is the rock going?
def _wws_beats():
    return [
        B("hook", 0, ["[d:intrigue][sfx:shimmer][act:a startling fact, calmly]Right now, you're moving at up to [count:1670|km/h]{1,670|sixteen hundred and seventy} kilometres an ^hour.",
                      "[d:wonder][act:the playful turn][tune:level]And you ^feel... [act:amused, soft][tune:fall]^*nothing*. [p:0.93][act:explaining, simple]That's the Earth ^spinning: one lap of the equator, about forty thousand ^kilometres, every single ^day. "
                      "[act:an everyday picture, warm]On a smooth flight, your drink sits perfectly ^still. [act:the key idea, plain][tune:fall]You only feel speed when it ^changes."], cut=False),
        B("world", 1, ["[d:calm][act:zooming out, clear]And that's the ^slow part. [act:steady, a little amazed]Around the ^Sun, the Earth covers ^thirty kilometres every ^second. [p:0.93][act:a vivid comparison]That's its own width in about ^seven minutes@time.",
                       "[d:build][sfx:whoosh][go:2][act:bigger still]And the Sun carries us all around our ^galaxy, a vast, spinning disc of ^stars, at over two hundred kilometres a ^second. [p:0.93][act:awe at the scale]Even so, one lap takes about {230 million|two hundred and thirty million} ^years.",
                       "[d:aside][p:1.04][act:a fun aside, light]Last time we were at this spot, the ^dinosaurs were just getting ^*started*."]),
        B("collision", 3, ["[d:calm][act:turning to us][tune:rise]And ^us? [act:plain]The oldest known fossils of our own ^kind are about {300,000|three hundred thousand} years old.",
                           "[d:wonder][p:0.93][act:a vivid comparison]Squeeze all of Earth's history, about four and a half billion years, into a single ^day. [act:slowly, the reveal]The dinosaurs turn up at about a quarter to ^eleven at night. "
                           "[sfx:ticks][p:0.93][act:the punchline, hushed]And we arrive in the last ^*six seconds* before ^midnight."]),
        B("cost", 4, ["[d:calm][act:confident]The road ahead is ^*calculable*. [p:0.93][act:explaining, clear]Gravity is so regular that we can run the sums ^forward, like ^clockwork.",
                      "[d:build][act:a near miss, vivid]In {2029|twenty twenty-nine}, asteroid Apophis, a rock a few hundred metres ^across, passes closer than our TV ^*satellites*. "
                      "[p:0.93][act:precise, calm]They circle about thirty-six thousand kilometres ^up; Apophis slips by at about thirty-two ^thousand. [act:reassuring, a small smile][tune:fall]And the sums say it ^misses.",
                      "[d:tension][go:5][act:sober, the long view]In about a billion years, the slowly brightening Sun takes the ^*oxygen*. [p:0.93][act:explaining, step by step]A hotter Earth locks carbon dioxide away in its ^rocks, "
                      "plants go ^hungry, and the oxygen they breathe out ^fades."]),
        B("reversal", 6, ["[d:wonder][p:0.96][act:vast, slow]Then, in about five billion years, the Sun ^swells into a red ^*giant*, more than a hundred times ^wider than today.",
                          "[d:reveal][go:7][act:a cosmic twist][tune:rise]And ^Andromeda, the nearest big galaxy, is heading our ^way. [p:0.93][act:explaining, like a forecast]A {2025|twenty twenty-five} study ran the future again and again, "
                          "nudging every measurement within its ^error. [act:precise, a little amazed]In about half the runs, the two galaxies ^merge within ten billion years: a collision at [stamp:≈ 50 / 50|gold]about ^*even* odds."]),
        B("tag", 8, ["[d:verdict][p:0.95][act:humble, honest]Past that, the equations fog ^over. [act:the big thought, gentle]Physics can calculate the ^road. [p:0.93][act:quiet, sincere][tune:fall]What the journey ^means, no equation can tell us.",
                     "[d:tension][p:0.93][act:a pause to think][tune:level]So... [act:a real question, warm][tune:fall]where do ^*you* stand?"]),
    ]


def where_we_stand():
    from f00 import EP
    beats = _wws_beats()
    clk = _clock(beats)
    T = lambda s, ph, k=0, dt=0.0: _at(clk, s, ph, k, dt)
    EL = .45
    C30 = math.cos(math.pi / 6)

    # 0 · the spinning Earth: you, at the equator, a lap of 40,000 km a day; a drink that stays still on a smooth flight
    gx, gy, gr, gs = 500, 800, 10.0, 22.4
    A, Bv = 2 ** .5 * C30 * gr * gs, 2 ** .5 * EL * gr * gs                  # the equator's ellipse on screen
    eq = lambda a0, a1, n=40: [[round(gx + A * math.cos(math.radians(a0 + (a1 - a0) * k / n)), 1), round(gy + Bv * math.sin(math.radians(a0 + (a1 - a0) * k / n)), 1)] for k in range(n + 1)]
    spin, az0 = -5.0, 75.0 + 45                           # az = the longitude facing us + 45; "you" (25 E) comes round to the front in ~10 s
    Ly = math.radians(25)
    you = [round(gr * 1.03 * math.cos(Ly), 3), 0, round(-gr * 1.03 * math.sin(Ly), 3)]
    earth = {"k": "iso", "x": gx, "y": gy, "s": gs, "az": az0, "spin": spin, "el": EL, "items": _globe(gr), "in": .1}
    mark = {"k": "iso", "x": gx, "y": gy, "s": gs, "az": az0, "spin": spin, "el": EL, "in": T(0, "you're"),
            "items": [{"t": "glow", "x": you[0], "y": 0, "z": you[2], "r": 46, "kind": "lamp"}, {"t": "label", "x": you[0], "y": 0, "z": you[2], "text": "you", "st": "ital", "c": AU, "dy": -30}]}
    front = eq(180, 0)
    gl0, gl1 = T(0, "smooth"), T(0, "drink")
    wx_, wy_ = round(330 + 20 * 1.15, 1), round(1320 - 4 * 1.15, 1)
    glass = [I.ring(wx_, wy_, 16, gl1 - .3, AMBER, 2.5, dur=.4), I.line([[wx_ + 14, wy_ - 10], [690, 1262]], gl1 - .1, AMBER, 2, "inferred", .5),
             I.box(600, 1392, 300, 12, "#6a5a48", r=3, at=gl1),
             {"k": "poly", "p": [[700, 1262], [800, 1262], [788, 1390], [712, 1390]], "fill": "rgba(159,208,255,.10)", "c": "#cbd2d8", "w": 3, "in": gl1},
             {"k": "poly", "p": [[704, 1300], [796, 1300], [788, 1388], [712, 1388]], "fill": "rgba(63,134,168,.55)", "c": "none", "w": 0, "in": gl1 + .3, "fx": "fill"},
             I.line([[704, 1300], [796, 1300]], T(0, "still"), "#bfe6f5", 4, dur=.6)]
    s0 = {"base": "dark", "stars": 160, "cam": [1, 500, 900], "els": [I.glow(gx, gy, 420, .1, .25, "scan"), earth, mark,
          {"k": "arrow", "p": front, "c": AMBER, "w": 5, "curve": True, "fx": "draw", "dur": 1.4, "in": T(0, "moving")},
          I.label(500, 1136, "1,670 km/h at the equator", T(0, "sixteen"), AMBER, 34),
          I.line(eq(0, -180), T(0, "one lap"), AMBER, 3, "inferred", 1.2, op=.7),
          I.label(500, 1190, "40,000 km, every day", T(0, "forty"), BONE, 32)] + _plane(330, 1320, 1.15, gl0) + glass}

    # 1 · around the Sun: the Earth runs its orbit (the model turns: the Earth moves); its own width in about seven minutes
    ox, oy, ro = 500, 740, 310.0
    orbit = [[round(ro * math.cos(2 * math.pi * k / 90), 2), 0, round(ro * math.sin(2 * math.pi * k / 90), 2)] for k in range(91)]
    ring = {"k": "iso", "x": ox, "y": oy, "s": 1, "az": 0, "spin": -22, "el": EL, "in": T(1, "earth"),
            "items": [{"t": "line", "p": orbit, "c": "#9fd0ff", "w": 2.5, "op": .7}, {"t": "glow", "x": ro, "y": 0, "z": 0, "r": 44, "kind": "scan"},
                      {"t": "label", "x": ro, "y": 0, "z": 0, "text": "Earth", "st": "ital", "c": BLUE, "dy": -34}]}
    speed = {"k": "iso", "x": ox, "y": oy, "s": 1, "az": 0, "spin": -22, "el": EL, "in": T(1, "thirty"),
             "items": [{"t": "label", "x": ro, "y": 0, "z": 0, "text": "30 km/s", "st": "serif", "c": AMBER, "dy": 58}]}
    w0 = T(1, "width")
    width = [I.oval(330, 1250, 56, 56, "#2f5f7a", "#9fd0ff", 2, 1, w0), I.oval(316, 1236, 22, 16, "#7f9a5a", "none", 0, .9, w0),
             I.oval(442, 1250, 56, 56, "none", "#9fd0ff", 2.5, 1, w0 + .7, style="inferred"),
             I.arrow([[330, 1166], [442, 1166]], w0 + 1.0, AMBER, 4, dur=.6, curve=False), I.label(530, 1265, "7 minutes", T(1, "seven"), AMBER, 40, "start", st="serif")]
    s1 = {"base": "dark", "stars": 140, "cam": [1, 500, 900], "els": [I.glow(ox, oy, 230, T(1, "sun"), .9, "sun"), I.oval(ox, oy, 44, 44, "#ffd890", "#fff1d2", 2, 1, T(1, "sun"))] +
          [ring, speed, I.label(ox, oy + 96, "Sun", T(1, "sun", dt=.3), "#ffd890", 32)] + width}

    # 2 · around the galaxy: a lap of 230 million years; last time, the first dinosaurs
    cx, cy, R, ry = 500, 800, 430, 190
    sa = math.radians(205)
    sx, sy = round(cx + R * .56 * math.cos(sa), 1), round(cy - ry * .56 * math.sin(sa), 1)
    lap = [[round(cx + R * .56 * math.cos(sa + 2 * math.pi * k / 80), 1), round(cy - ry * .56 * math.sin(sa + 2 * math.pi * k / 80), 1)] for k in range(81)]
    d0 = T(2, "dinosaurs")
    s2 = {"base": "dark", "stars": 120, "cam": [1, 500, 900], "els": [I.dot(sx, sy, 10, AU, T(2, "sun")), I.ring(sx, sy, 24, T(2, "sun", dt=.2), AU, 3)] +
          _galaxy(cx, cy, R, ry, T(2, "galaxy"), a0=.6, arms=4, dt=.35) +
          [I.label(sx - 10, sy - 44, "the Sun", T(2, "sun", dt=.3), AU, 32, "end"), I.label(cx, cy - ry - 80, "our galaxy", T(2, "galaxy", dt=.4), BONE, 34),
           I.label(sx - 10, sy + 70, "200+ km/s", T(2, "two hundred"), AMBER, 34, "end"),
           {"k": "arrow", "p": lap, "c": AMBER, "w": 4, "curve": True, "fx": "draw", "dur": 3.2, "in": T(2, "one lap"), "head": 18},
           I.label(640, cy + ry + 74, "one lap: 230 million years", T(2, "two hundred", 1), AMBER, 34),
           I.glow(sx, sy, 90, d0, .7)] + _dino(sx + 40, sy + 330, 1.1, d0) + [I.line([[sx, sy + 26], [sx + 40, sy + 210]], d0, "#cbbca8", 2, "inferred", .5),
           I.label(sx + 40, sy + 380, "the first dinosaurs", d0 + .3, "#cbbca8", 30)]}

    # 3 · Earth's history as one day: the clock fills; dinosaurs at about 22:46; us, the last six seconds
    kx, ky, kr = 500, 740, 300
    hand = lambda h, rr: (round(kx + rr * math.sin(2 * math.pi * h / 24), 1), round(ky - rr * math.cos(2 * math.pi * h / 24), 1))
    q0 = T(3, "squeeze")
    wedges = []
    for h in range(24):
        pts = [[kx, ky]] + [list(hand(h + f / 6, kr - 8)) for f in range(7)]
        wedges.append({"k": "poly", "p": pts, "fill": AMBER, "c": "none", "w": 0, "op": .2, "keepop": True, "in": round(T(3, "single day") + .14 * h, 2)})
    ticks = [I.line([list(hand(h, kr - (26 if h % 6 == 0 else 14))), list(hand(h, kr))], q0 + .4 + .03 * h, BONE, 3 if h % 6 == 0 else 2, draw=False) for h in range(24)]
    dz = 24 * (1 - 230 / 4540)
    dt0 = T(3, "dinosaurs")
    bar0, cell = 140, 11.5
    last = T(3, "last")
    s3 = {"base": "dark", "cam": [1, 500, 900], "els": [I.person(860, 1312, 120, T(3, "fossils"), c="#e8d6b8"), I.label(930, 1370, "300,000 years", T(3, "three hundred"), BONE, 30, "end"),
          I.ring(kx, ky, kr, q0, BONE, 3, dur=1.4)] + ticks + wedges +
          [I.label(kx, ky - kr - 30, "midnight", q0 + 1.0, BONE, 30), I.label(kx, ky + 12, "4.5 billion years", T(3, "four and a half"), AMBER, 36, st="serif"),
           I.label(kx, ky + 60, "in one day", T(3, "single day"), BONE, 30),
           I.line([list(hand(dz, kr - 30)), list(hand(dz, kr + 12))], dt0, GREEN, 5, draw=False), ] + _dino(hand(dz, kr + 70)[0] - 20, hand(dz, kr + 70)[1] + 34, .6, dt0, GREEN) + [
           I.label(hand(dz, kr + 70)[0] - 60, hand(dz, kr + 70)[1] - 52, "dinosaurs", dt0 + .3, GREEN, 28, "end")] +
          [I.box(round(bar0 + cell * k, 1), 1250, cell - 2.5, 36, "#5a5048", r=2, at=round(last + .012 * k, 3)) for k in range(54)] +
          [I.box(round(bar0 + cell * k, 1), 1250, cell - 2.5, 36, AU, r=2, at=round(T(3, "six seconds") + .12 * (k - 54), 2), fx="pop") for k in range(54, 60)] +
          [I.line([list(hand(0, kr)), [bar0 + cell * 60, 1240]], last, AMBER, 2, "inferred", .8), I.line([list(hand(-.02, kr)), [bar0, 1240]], last, AMBER, 2, "inferred", .8),
           I.label(bar0, 1330, "the last minute", last + .4, BONE, 30, "start"), I.label(bar0 + cell * 57, 1222, "6 s", T(3, "six seconds", dt=.6), AU, 34)]}

    # 4 · the road is calculable: Apophis's path, worked out ahead, passes inside the ring of TV satellites (to scale)
    ex, ey, ER = 500, 860, 60                     # Earth's radius, 6,371 km = 60 px
    geo, apo = round(ER * 42164 / 6371), round(ER * 37970 / 6371)
    path = [[60, ey - apo - 58], [280, ey - apo - 14], [500, ey - apo], [720, ey - apo - 14], [940, ey - apo - 58]]
    sats = []
    for k in range(10):
        a = 2 * math.pi * k / 10                          # none sits right at the top, where Apophis passes
        x, y = ex + geo * math.cos(a), ey + geo * math.sin(a)
        sats += [I.box(round(x - 7, 1), round(y - 7, 1), 14, 14, "#cbd2d8", r=2, at=round(T(4, "satellites") + .1 * k, 2)),
                 I.box(round(x - 26, 1), round(y - 4, 1), 15, 8, "#5f87b3", r=1, at=round(T(4, "satellites") + .1 * k, 2)), I.box(round(x + 11, 1), round(y - 4, 1), 15, 8, "#5f87b3", r=1, at=round(T(4, "satellites") + .1 * k, 2))]
    a0 = T(4, "apophis")
    yp = lambda x: round(ey - apo - 58 * ((x - 500) / 440) ** 2, 1)
    rocks = [I.dot(x, yp(x), 12 if x == 500 else 7, "#e2b48a", round(a0 + .5 + .3 * k, 2), op=1 if x == 500 else .55) for k, x in enumerate(range(100, 501, 80))] + \
        [I.glow(500, yp(500), 60, round(a0 + 2.0, 2), .8, "lamp")]
    s4 = {"base": "dark", "stars": 120, "cam": [1, 500, 900], "els": [I.glow(ex, ey, 150, .3, .5, "scan"), I.oval(ex, ey, ER, ER, "#2f5f7a", "#9fd0ff", 2, 1, .3),
          I.oval(ex - 18, ey - 12, 22, 16, "#7f9a5a", "none", 0, .9, .3), I.oval(ex + 20, ey + 18, 16, 12, "#7f9a5a", "none", 0, .9, .3),
          I.line(path, T(4, "sums"), LILAC, 3, "inferred", 2.0, curve=True), I.label(930, ey - apo - 110, "worked out ahead", T(4, "sums", dt=1.4), LILAC, 30, "end"),
          I.label(80, ey - apo - 100, "Apophis, 2029", a0, "#e2c4a0", 32, "start")] + rocks +
         [I.ring(ex, ey, geo, T(4, "satellites"), "#9fd0ff", 2, dur=1.6)] + sats +
         [{"k": "dim", "x1": round(ex + ER * .7071, 1), "y1": round(ey + ER * .7071, 1), "x2": round(ex + geo * .7071, 1), "y2": round(ey + geo * .7071, 1), "c": BLUE, "in": T(4, "thirty-six")},
          I.label(640, 1035, "36,000 km", T(4, "thirty-six"), BLUE, 30, "start"),
          {"k": "dim", "x1": ex, "y1": ey - ER - 4, "x2": ex, "y2": ey - apo + 14, "c": "#e2c4a0", "in": T(4, "thirty-two"), "upright": True},
          I.label(520, 660, "32,000 km", T(4, "thirty-two"), "#e2c4a0", 30, "start"),
          I.label(500, 1350, "TV satellites", T(4, "satellites", dt=.6), BLUE, 32), I.label(930, 562, "it misses", T(4, "misses"), GREEN, 32, "end")]}

    # 5 · in a billion years: a brighter Sun, carbon dioxide locked into rock, hungry plants, the oxygen fading
    G = 1130
    r5 = random.Random(5)
    o2 = [(round(r5.uniform(120, 880), 1), round(r5.uniform(600, 1060), 1)) for _ in range(40)]
    o2 = [(x, y) for x, y in o2 if not (370 < x < 650 and y > 820) and not (110 < x < 400 and 690 < y < 850)][:22]
    co2 = [(150, 760), (235, 800), (320, 770), (690, 790), (775, 760), (860, 800)]
    b5, cc, hu, fa = T(5, "brightening"), T(5, "carbon dioxide"), T(5, "hungry"), T(5, "fades")
    def plant(c, at):
        els = [I.line([[510, G], [502, G - 120], [512, G - 250]], at, c, 7, dur=.8, curve=True)]
        for k, (dy, sd) in enumerate(((70, -1), (112, 1), (150, -1), (190, 1), (228, -1))):
            x0, y0 = 506 + 2 * sd, G - dy
            els.append({"k": "poly", "p": [[x0, y0], [x0 + sd * 34, y0 - 26], [x0 + sd * 78, y0 - 22], [x0 + sd * 52, y0 + 4]], "fill": c, "c": "none", "w": 0, "curve": True, "in": round(at + .25 + .12 * k, 2)})
        return els
    # (the Sun's light goes on top, so whatever is painted out vanishes under the same glow as the sky around it)
    s5 = {"base": "dark", "cam": [1, 500, 900], "els": [I.box(60, G, 880, 290, "#5a4632", r=4, at=.2), I.line([[60, G], [940, G]], .2, "#a8865e", 3, draw=False)] +
          [I.box(60, G + 80 + 60 * k, 880, 4, "#7a6248", r=1, at=.2) for k in range(3)] + plant(GREEN, .5) +
          [I.dot(x, y, 9, "#bfe6f5", round(.6 + .03 * k, 2), op=.85) for k, (x, y) in enumerate(o2)] +
          [I.dot(x, y, 12, "#a09486", round(cc + .1 * k, 2)) for k, (x, y) in enumerate(co2)] +
          [I.arrow([[x, y + 20], [x, G + 58]], round(cc + 1.1 + .08 * k, 2), "#a09486", 2.5, "inferred", .8, False) for k, (x, y) in enumerate(co2)] +
          [I.dot(x, G + 92 + 26 * (k % 2), 11, "#a09486", round(cc + 1.9 + .08 * k, 2)) for k, (x, y) in enumerate(co2)] +
          [I.dot(x, y, 15, _bg(x, y), round(cc + 1.9 + .08 * k, 2)) for k, (x, y) in enumerate(co2)] + plant("#8a6a48", hu) +
          [I.dot(x, y, 12, _bg(x, y), round(fa - .9 + .05 * k, 2)) for k, (x, y) in enumerate(o2) if k % 7 != 3] +
          [I.glow(200, 420, 150, .3, .7, "sun")] + [I.glow(200, 420, 220 + 90 * k, round(b5 + .7 * k, 2), .5, "sun") for k in range(3)] +
          [I.oval(200, 420, 46, 46, "#ffd890", "none", 0, 1, .3), I.oval(200, 420, 54, 54, "#fff1d2", "none", 0, 1, b5 + 1.6, fx="pop"),
           I.label(600, 400, "in about 1 billion years", T(5, "billion"), BONE, 32), I.label(880, 560, "oxygen", T(5, "oxygen"), "#bfe6f5", 32, "end"),
           I.label(120, 700, "carbon dioxide", cc + .3, "#cbbca8", 30, "start"), I.label(880, G + 240, "locked in rock", T(5, "rocks"), "#cbbca8", 30, "end")]}

    # 6 · in five billion years: the Sun swells into a red giant (to scale with today's Sun and Earth's orbit)
    rx_, ry_ = 360, 860
    rs = 2.6
    RG = rs * 110
    sw = T(6, "swells")
    s6 = {"base": "dark", "stars": 160, "cam": [1, 500, 900], "els": [I.glow(rx_, ry_, 70, T(6, "sun"), .9, "sun")] +
          [I.oval(rx_, ry_, round(RG * f, 1), round(RG * f, 1), "#d24e36", "none", 0, 1, round(sw + .45 * k, 2), fx="pop", dur=.9) for k, f in enumerate((.25, .5, .75, 1.0))] +
          [I.oval(rx_, ry_, round(RG * f, 1), round(RG * f, 1), c, "none", 0, .55, round(sw + 2.0 + .2 * k, 2)) for k, (f, c) in enumerate(((.8, "#e8663e"), (.55, "#f07e48"), (.3, "#f89a58")))] +
          [I.glow(rx_, ry_, 560, sw + 1.8, .5, "red"), I.dot(rx_, ry_, rs, "#fff6e6", T(6, "sun")),
           I.line([[rx_, ry_ - RG - 40], [rx_, ry_ - 10]], T(6, "sun", dt=.2), "#fff1d2", 2, draw=False), I.label(rx_, ry_ - RG - 56, "the Sun today", T(6, "sun", dt=.2), "#ffd890", 30),
           I.label(rx_, ry_ + 120, "a red giant", T(6, "giant"), BONE, 40, st="serif"),
           {"k": "dim", "x1": round(rx_ - RG, 1), "y1": ry_ + RG + 40, "x2": round(rx_ + RG, 1), "y2": ry_ + RG + 40, "c": BONE, "in": T(6, "hundred")},
           I.label(rx_, ry_ + RG + 90, "over 100 times wider", T(6, "hundred", dt=.3), BONE, 32),
           {"k": "line", "p": I.ellipse(rx_, ry_, rs * 215, rs * 215, 40, -38, 38), "c": BLUE, "w": 3, "style": "inferred", "curve": True, "in": T(6, "wider"), "fx": "draw", "dur": 1.0},
           I.dot(round(rx_ + rs * 215, 1), ry_, 9, BLUE, T(6, "wider", dt=.5)), I.label(round(rx_ + rs * 215, 1) - 20, ry_ - 330, "Earth's orbit", T(6, "wider", dt=.7), BLUE, 30, "end")]}

    # 7 · Andromeda: heading our way; the future run again and again: about half the runs merge, half swing past
    mx, my = 300, 1150
    ax_, ay_ = 690, 520
    an = T(7, "andromeda")
    runs = []
    for k in range(10):
        j = k // 2
        if k % 2 == 0:
            pts = [[ax_ - 60 + 14 * j, ay_ + 40], [640 - 40 * j, 760 + 10 * j], [430 + 6 * j, 990 - 10 * j], [mx + 12, my - 12]]
        else:
            pts = [[ax_ - 40 + 16 * j, ay_ + 44], [660 - 20 * j, 790], [560 - 14 * j, 1010], [490 - 10 * j, 1180 + 8 * j], [580 + 10 * j, 1330 - 6 * j], [760 + 30 * j, 1360 - 30 * j]]
        runs.append({"k": "line", "p": pts, "c": AMBER if k % 2 == 0 else BLUE, "w": 3, "style": "inferred", "curve": True, "op": .9, "keepop": True,
                     "in": round(T(7, "again and again") + .3 * k, 2), "fx": "draw", "dur": 1.0})
    hf = T(7, "half")
    s7 = {"base": "dark", "stars": 180, "cam": [1, 500, 900], "els": _galaxy(mx, my, 220, 86, .4, a0=1.0, arms=4, dt=.2, seed=5) + [I.label(mx, my + 136, "our galaxy", .8, BONE, 32)] +
          _galaxy(ax_, ay_, 250, 80, an, a0=2.6, arms=2, dt=.3, seed=9, c="#e8dcff") + [I.label(ax_, ay_ - 120, "Andromeda", an + .4, LILAC, 34)] +
          [I.arrow([[ax_ - 160, ay_ + 110], [ax_ - 300, ay_ + 290]], T(7, "heading"), LILAC, 5, dur=.8, curve=False)] + runs +
          [I.glow(mx, my, 280, T(7, "merge"), .7, "lamp"), I.label(180, 900, "merge", hf, AMBER, 36, "start", st="serif"), I.label(900, 1240, "miss", hf + .4, BLUE, 36, "end", st="serif")]}

    # 8 · the road ahead fades into fog; physics maps the road; and a person under the stars
    road = [[470, 1262], [540, 1190], [600, 1090], [600, 990], [530, 900], [470, 810], [480, 730], [540, 660], [580, 590], [560, 500], [510, 430]]
    marks = [(road[2], "2029", "start"), (road[4], "1 billion years", "end"), (road[6], "5 billion", "start"), (road[8], "10 billion", "start")]
    fg = T(8, "fog")
    s8 = {"base": "sky", "tod": "night", "ground": 1262, "groundc": "#1e1813", "sun": False, "cam": [1, 500, 900], "els": [I.line(road[:9], .3, AMBER, 4, dur=2.2, curve=True),
          I.line(road[8:], 1.6, AMBER, 3, "inferred", 1.0, curve=True, op=.6)] +
          sum([[I.dot(p[0], p[1], 9, AMBER, round(.6 + .4 * k, 2)), I.label(p[0] + (26 if a == "start" else -26), p[1] + 10, t, round(.7 + .4 * k, 2), BONE, 30, a)] for k, (p, t, a) in enumerate(marks)], []) +
          [I.glow(x, y, r, round(fg + d, 2), op, kind) for x, y, r, d, op, kind in ((530, 470, 300, 0, .55, "scan"), (420, 520, 240, .4, .5, "lamp"), (640, 430, 260, .8, .5, "scan"),
                                                                                    (520, 380, 340, 1.2, .5, "scan"), (560, 560, 200, 1.5, .45, "scan"))] +
          [I.glow(p[0], p[1], 70, round(T(8, "road") + .3 * k, 2), .9, "lamp") for k, (p, t, a) in enumerate(marks)] +
          [I.glow(400, 1200, 160, T(8, "you"), .7, "lamp"), I.person(400, 1262, 150, T(8, "where"), c="#e8d6b8")]}

    shots = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
    ep = EP("where-we-stand", "00.01", "Where is the rock going?", None, None, "A calculable road, and a question physics can't answer.", "You're moving at *1,670 km/h*.", beats, shots,
            "Hublin et al. 2017, Nature · Ozaki & Reinhard 2021, Nature Geoscience · Sawala et al. 2025, Nature Astronomy",
            "You're moving at up to 1,670 km/h through a galaxy, toward a calculable future. Where does physics stop? Sources on the site.",
            ["#Space", "#Earth", "#Andromeda", "#Science", "#WeighItYourself"])
    ep["mood"] = "space"                                   # the legacy film's music
    return ep


def where_we_stand_m():
    """Where is the rock going? as one continuous take (see mural.py): a spinning globe, an orbit, a galaxy lap, Earth's history
    as one day, an asteroid inside the satellite ring, a fading breath of oxygen, a swelling Sun, the futures of Andromeda, a road into fog."""
    return remix(where_we_stand(), cams={})


# ---------------------------------------------------------------- 13.01 MKUltra: the files that survived
PAPER, MANILA, MANILA_E = "#efe6d2", "#cdb58a", "#8a6a48"


def _folder(x, y, w, h, at, c=MANILA, fx=None, op=None):
    """A manila folder seen flat: a body and a tab (x, y = top-left of the body)."""
    e = {"k": "poly", "p": [[x, y], [x + w * .32, y], [x + w * .36, y - 22], [x + w * .62, y - 22], [x + w * .66, y], [x + w, y], [x + w, y + h], [x, y + h]],
         "fill": c, "c": MANILA_E, "w": 2, "in": at}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def _cloud(cx, cy, rx, ry, n=11):
    pts = []
    for k in range(n * 6):
        a = 2 * math.pi * k / (n * 6)
        bump = 1 + .1 * abs(math.sin(n * a / 2))
        pts.append([round(cx + rx * bump * math.cos(a), 1), round(cy + ry * bump * math.sin(a), 1)])
    return pts


def _glass(x, y, at, c="#cbd2d8", liquid="rgba(201,160,122,.6)"):
    """A drinking glass standing on y, centred on x."""
    return [{"k": "poly", "p": [[x - 34, y - 110], [x + 34, y - 110], [x + 26, y], [x - 26, y]], "fill": "rgba(159,208,255,.08)", "c": c, "w": 3, "in": at},
            {"k": "poly", "p": [[x - 30, y - 70], [x + 30, y - 70], [x + 25, y - 3], [x - 25, y - 3]], "fill": liquid, "c": "none", "w": 0, "in": at + .2, "fx": "fill"}]


def _drop(x, y, at, c=LILAC):
    """A falling drop (point up), and its short trail."""
    return [I.line([[x, y - 90], [x, y - 40]], at, c, 2, "claimed", .5),
            {"k": "poly", "p": [[x, y - 26], [x + 11, y - 4], [x + 8, y + 6], [x, y + 10], [x - 8, y + 6], [x - 11, y - 4]], "fill": c, "c": "none", "w": 0, "curve": True, "in": at + .4, "fx": "rise"}]


def _building(x, y, kind, at, c="#cbbca8"):
    """A small institution, base on y: a university (columns), a hospital (cross) or a prison (bars)."""
    els = [I.box(x - 80, y - 110, 160, 110, "#3a3129", c, 2, 3, at)]
    if kind == "uni":
        els += [{"k": "poly", "p": [[x - 92, y - 110], [x, y - 160], [x + 92, y - 110]], "fill": "#3a3129", "c": c, "w": 2, "in": at}] + \
               [I.box(x - 62 + 34 * k, y - 96, 14, 96, c, r=2, at=at + .1) for k in range(4)]
    elif kind == "hosp":
        els += [I.box(x - 10, y - 92, 20, 56, RED, r=2, at=at + .1), I.box(x - 28, y - 74, 56, 20, RED, r=2, at=at + .1), I.box(x - 18, y - 30, 36, 30, c, r=2, at=at + .1)]
    else:
        els += [I.box(x - 50, y - 86, 100, 58, "#15110d", c, 2, 2, at + .1)] + [I.line([[x - 34 + 17 * k, y - 86], [x - 34 + 17 * k, y - 28]], at + .2, c, 4, draw=False) for k in range(5)]
    return els


def _mk_beats():
    return [
        B("hook", 0, ["[d:intrigue][sfx:typewriter][act:dry, cutting through]This isn't a conspiracy ^theory. [act:plain, pointed]It's ^*paperwork*.",
                      "[d:reveal][act:sober, grave]The CIA drugged people, without their ^knowledge. [act:firm]It's on the ^*record@noun*. [p:0.93][act:quiet, serious]Let's open the ^file."], cut=False),
        B("world", 1, ["[d:calm][act:factual, clear]In {1953|nineteen fifty-three}, in the middle of the Cold War, the CIA approved a secret programme: ^MKUltra. "
                       "[p:0.93][act:explaining, measured]Officials feared enemy ^brainwashing, and wanted their own drugs to ^control behaviour.",
                       "[d:list][act:the scale, measured]The surviving records@noun list a hundred and forty-nine ^subprojects. [act:naming them, darker][tune:level]At ^universities. [act:the next, same beat][tune:level]At ^hospitals. [act:the last, heavier][tune:fall]In ^*prisons*. "
                       "[p:0.93][act:explaining, plain]Much of the money went through front organisations, so many researchers never knew the CIA was ^paying."]),
        B("collision", 2, ["[d:tension][act:quiet, uneasy]In safe houses@noun! in San Francisco and New York, ordinary flats rented in ^secret, members of the public were given ^LSD without being told... "
                           "[sfx:heartbeat][act:chilling, soft][tune:fall]and ^*watched*, to see what the drug would ^do. [p:0.93][act:explaining, plain]LSD is a powerful drug that can scramble the senses for ^hours. [act:quiet, heavy][tune:fall]They had no idea what was ^happening to them."]),
        B("cost", 3, ["[d:reveal][act:grave, respectful]In {1953|nineteen fifty-three}, the year it began, Army scientist Frank Olson was secretly given ^LSD, slipped into his drink at a work ^retreat. [act:somber, slow]Nine days later, he fell to his ^*death*.",
                      "[d:tension][p:0.96][act:gentle, heavy][tune:level]His family only learned he had been ^drugged... [act:quiet, pained][tune:fall]twenty-two years ^later."]),
        B("reversal", 4, ["[d:build][sfx:paper][act:the cover-up, firm]In {1973|nineteen seventy-three}, the CIA's director ordered the MKUltra files ^*destroyed*.",
                          "[d:build][act:the lucky break][tune:fall]But some had been filed with the ^*accounts*, and were ^missed. [p:0.93][act:relief, precise]In {1977|nineteen seventy-seven}, a freedom-of-information request turned up about twenty thousand ^pages. "
                          "[d:aside][act:dry, a small smile]Saved, by ^bureaucracy."]),
        B("tag", 5, ["[d:verdict][act:measured authority]That same year, a Senate hearing put it all on the ^record@noun. [p:0.93][act:asking it, steady]How do we ^know? [act:clear, measured]The CIA's own surviving ^files, "
                     "its inspector general's report from {1963|nineteen sixty-three}, and a Senate ^investigation all tell the same ^story. [p:0.9][act:the everyday picture]Records@noun written at the time, by the people in charge: "
                     "like a company's own ^receipts. [act:the verdict, firm][tune:fall]^*Established*.",
                     "[d:tension][p:0.93][act:quiet, with care]Behind those pages are people who never said ^yes. [go:6][p:0.94][act:quiet, pointed][tune:level]So when someone says it could never ^happen... "
                     "[act:the final word, calm][tune:fall]it's ^*paperwork*."]),
    ]


def mkultra():
    from f13 import EP
    beats = _mk_beats()
    clk = _clock(beats)
    T = lambda s, ph, k=0, dt=0.0: _at(clk, s, ph, k, dt)

    # 0 · not a theory: a cloud of rumour struck out; a stack of files; a drink, a drop; a stamp; the file opens
    pw = T(0, "paperwork")
    stack = [_folder(330 + 8 * k, 930 - 14 * k, 360, 230, round(pw + .12 * k, 2), fx="rise") for k in range(5)]
    top_x, top_y = 330 + 32, 930 - 56
    s0 = {"base": "dark", "cam": [1, 500, 900], "els": [
        {"k": "poly", "p": _cloud(500, 575, 220, 95), "fill": "rgba(201,193,238,.06)", "c": LILAC, "w": 3, "style": "claimed", "curve": True, "in": .6},
        I.label(500, 605, "?", .9, LILAC, 84, st="big"), I.strike(270, 670, 730, 480, pw, RED, 7)] + stack +
        [I.person(190, 1380, 190, T(0, "drugged"), c="#9a9288")] + _glass(320, 1300, T(0, "drugged", dt=.3)) + [I.box(250, 1300, 150, 12, "#6a5a48", r=3, at=T(0, "drugged", dt=.3))] +
        _drop(320, 1150, T(0, "knowledge")) +
        [I.box(top_x + 190, top_y + 120, 150, 70, "none", RED, 5, 8, T(0, "record"), fx="pop"), I.line([[top_x + 210, top_y + 148], [top_x + 320, top_y + 148]], T(0, "record", dt=.1), RED, 6, draw=False),
         I.line([[top_x + 210, top_y + 166], [top_x + 290, top_y + 166]], T(0, "record", dt=.1), RED, 4, draw=False),
         I.box(top_x + 24, top_y - 150, 300, 190, PAPER, "#8a7a66", 2, 3, T(0, "open"), fx="rise")] +
        [I.line([[top_x + 50, top_y - 118 + 24 * j], [top_x + 300 - (40 if j % 3 == 2 else 0), top_y - 118 + 24 * j]], T(0, "open", dt=.3 + .05 * j), "#8a8378", 3, draw=False) for j in range(6)]}

    # 1 · 1953: the programme; 149 subprojects; universities, hospitals, prisons; money through front organisations
    sp = T(1, "subprojects")
    grid = []
    for k in range(149):
        x, y, at = round(152 + 47 * (k % 15), 1), round(686 + 31 * (k // 15), 1), round(sp + .012 * k, 3)
        grid += [I.box(x, y, 36, 22, MANILA, r=2, at=at), I.box(x, y - 5, 13, 6, MANILA, r=1, at=at)]
    fo = T(1, "front")
    FY = 1305
    flow = [I.box(110, FY - 35, 150, 70, "#3a3129", "#cbbca8", 2, 8, fo), I.label(185, FY + 11, "CIA", fo, BONE, 32),
            I.arrow([[270, FY], [380, FY]], fo + .3, AMBER, 3, dur=.4, curve=False),
            I.box(390, FY - 40, 220, 80, "none", LILAC, 3, 8, fo + .5, style="claimed"), I.label(500, FY + 11, "a front", fo + .6, LILAC, 32),
            I.arrow([[620, FY], [730, FY]], fo + .9, AMBER, 3, dur=.4, curve=False)] + \
        [I.person(770 + 46 * k, FY + 40, 90, round(fo + 1.1 + .15 * k, 2), c="#cbbca8") for k in range(3)] + [I.label(816, FY + 86, "researchers", fo + 1.4, BONE, 30)]
    s1 = {"base": "dark", "cam": [1, 500, 900], "els": [I.label(500, 450, "1953", T(1, "nineteen"), BONE, 64, st="serif"),
          _folder(330, 520, 340, 90, T(1, "mkultra")), I.label(500, 580, "MKULTRA", T(1, "mkultra", dt=.2), INK, 34, halo=False, st="serif"),
          I.label(500, 650, "149 subprojects", sp + 1.6, AMBER, 32)] + grid +
         _building(220, 1165, "uni", T(1, "universities")) + [I.label(220, 1208, "universities", T(1, "universities", dt=.2), BONE, 28)] +
         _building(500, 1165, "hosp", T(1, "hospitals")) + [I.label(500, 1208, "hospitals", T(1, "hospitals", dt=.2), BONE, 28)] +
         _building(780, 1165, "prison", T(1, "prisons")) + [I.label(780, 1208, "prisons", T(1, "prisons", dt=.2), BONE, 28)] + flow}

    # 2 · the safe houses: San Francisco and New York; a room, a drink, a mind scrambled, and someone watching
    v = View(-125, -66, 24, 50, (40, 330, 920, 900))
    sf, ny = v.p(-122.42, 37.77), v.p(-74.0, 40.71)
    hs = lambda p, at: [{"k": "house", "x": round(p[0] - 22, 1), "y": round(p[1] - 22, 1), "w": 44, "h": 30, "in": at, "fx": "pop"}]
    r0 = T(2, "ordinary")
    lsd = T(2, "lsd")
    wt = T(2, "watched")
    sc = T(2, "scramble")
    RY = 1410
    room = [I.box(80, 1050, 840, RY - 1050, "#2a221b", "#8a7a66", 3, 6, r0), I.box(120, 1090, 120, 96, "#12161c", "#8a7a66", 2, 3, r0 + .2),
            I.box(300, RY - 110, 220, 14, "#6a5a48", r=3, at=r0 + .3), I.person(250, RY, 200, r0 + .4, c="#9a9288")] + _glass(440, RY - 110, lsd) + \
        [I.line([[640, 1050], [640, RY]], wt - .4, BLUE, 4, "inferred", .8), I.person(790, RY, 200, wt, c="#5a524a"), I.glow(790, RY - 160, 110, wt, .5, "lamp"),
         I.box(816, RY - 150, 40, 54, PAPER, "#8a7a66", 1.5, 2, wt + .3), I.line([[768, RY - 182], [300, RY - 182]], wt + .2, BLUE, 2, "claimed", .8)] + \
        [I.line([[250 + 40 * math.cos(a + .6 * j), round(RY - 182 + 40 * math.sin(a + .6 * j), 1)] for j in range(6)], round(sc + .25 * k, 2), LILAC, 3, dur=.6, curve=True)
         for k, a in enumerate((0, 2.1, 4.2))]
    s2 = mapshot(v, pins=[("San Francisco", -122.42, 37.77, {"c": AU}), ("New York", -74.0, 40.71, {"c": AU, "a": "end", "lx": -18})], cam=[1, 500, 900])
    for e in s2["els"]:
        if e.get("k") == "pin":
            e["in"] = T(2, "san francisco") if e["t"] == "San Francisco" else T(2, "new york")
    s2["els"] += hs(sf, T(2, "san francisco", dt=.4)) + hs(ny, T(2, "new york", dt=.4)) + room

    # 3 · Frank Olson: a drink at a retreat; nine days; twenty-two years until his family knew
    dk = T(3, "drink")
    nd = T(3, "nine days")
    yr, fm = T(3, "twenty-two"), T(3, "family")
    days = [I.box(130 + 82 * k, 760, 66, 66, "#3a3129" if k < 8 else "#15110d", "#cbbca8", 2, 6, round(nd + .2 * k, 2)) for k in range(9)]
    s3 = {"base": "dark", "cam": [1, 500, 900], "els": _glass(170, 640, dk) + _drop(170, 500, dk + .4) +
          [I.label(310, 600, "a work retreat", T(3, "retreat"), BONE, 30, "start")] + days +
          [I.dot(163, 793, 9, LILAC, nd + .1), I.ring(130 + 82 * 8 + 33, 793, 46, round(nd + 2.2, 2), BONE, 2, dur=1.2), I.glow(130 + 82 * 8 + 33, 793, 90, round(nd + 2.4, 2), .35, "lamp"),
           I.label(500, 900, "9 days", nd + 1.9, BONE, 34, st="serif")] +
          [I.line([[130, 1080], [870, 1080]], fm - .2, "#8c7152", 3, dur=1.0), I.label(130, 1140, "1953", fm, BONE, 30)] +
          [I.line([[round(130 + 740 * k / 22, 1), 1066], [round(130 + 740 * k / 22, 1), 1094]], round(fm + .1 * k, 2), AMBER, 3, draw=False) for k in range(23)] +
          [I.label(870, 1140, "1975", yr, BONE, 30), I.label(500, 1040, "22 years", yr, AMBER, 36, st="serif")] +
          [I.glow(800, 1300, 160, yr + .3, .5, "lamp")] + [I.person(740 + 55 * k, 1380, (150, 130, 110)[k], round(yr + .3 + .15 * k, 2), c="#cbbca8") for k in range(3)]}

    # 4 · 1973: the files destroyed; the boxes filed with the accounts missed; 20,000 pages; saved by bureaucracy
    ds = T(4, "destroyed")
    ac = T(4, "accounts")
    pg = T(4, "pages")
    shelf = []
    for r in range(4):
        shelf.append(I.box(110, 560 + 96 * r + 80, 560, 8, "#6a5a48", r=2, at=.3))
        for c in range(6):
            x, y = 130 + 90 * c, 560 + 96 * r
            shelf += [I.box(x, y, 76, 78, MANILA, MANILA_E, 2, 3, round(.4 + .03 * (6 * r + c), 2)),
                      I.box(x, y, 76, 78, _bg(x + 38, y + 39), "#8a7a66", 2, 3, round(ds + .9 + .05 * (6 * r + c), 2), style="inferred")]
    s4 = {"base": "dark", "cam": [1, 500, 900], "els": [I.label(390, 500, "1973", T(4, "nineteen"), BONE, 48, st="serif")] + shelf +
          [I.glow(390, 760, 330, ds + .2, .7, "fire"), I.glow(260, 700, 200, ds + .5, .6, "fire"), I.glow(520, 820, 200, ds + .7, .6, "fire")] +
          [I.box(720, 640 + 96 * k, 150, 78, "#c9b07a", MANILA_E, 2, 3, round(ac + .15 * k, 2)) for k in range(3)] +
          [I.label(795, 690 + 96 * k, "$", round(ac + .15 * k, 2), INK, 40, st="serif", halo=False) for k in range(3)] +
          [I.box(700, 610, 190, 330, "none", AU, 4, 12, ac + .9, fx="pop"), I.label(795, 990, "the accounts", ac + 1.0, AU, 30)] +
          [I.box(250, 1360 - 18 * k, 300, 15, PAPER, "#8a7a66", 1.2, 2, round(pg + .1 * k, 2), fx="pop") for k in range(20)] +
          [I.label(620, 1250, "20,000 pages", pg + 1.6, BONE, 40, "start", st="serif"),
           I.ring(470, 1110, 56, T(4, "bureaucracy"), GREEN, 5, dur=.6), I.line([[444, 1110], [464, 1132], [500, 1086]], T(4, "bureaucracy", dt=.2), GREEN, 6, dur=.4)]}

    # 5 · 1977: the hearing; three independent records that agree; established; and the people behind the pages
    hk = T(5, "know")
    fl, ig, si = T(5, "files"), T(5, "inspector"), T(5, "investigation")
    es = T(5, "established")
    P0 = (800, 1060)
    src = [(170, 940, fl, "CIA files"), (170, 1060, ig, "1963 report"), (170, 1180, si, "Senate inquiry")]
    s5 = {"base": "dark", "cam": [1, 500, 900], "els": [I.person(230 + 135 * k, 610, 130, round(.4 + .1 * k, 2), c="#9a9288") for k in range(5)] +
          [I.box(150, 545, 700, 70, "#4a3a2c", "#8a6a48", 2, 6, .3)] +
          [I.person(500, 784, 130, .9, c="#9a9288"), I.box(380, 735, 240, 50, "#4a3a2c", "#8a6a48", 2, 4, .9), I.line([[560, 735], [536, 690]], 1.1, "#cbd2d8", 3, draw=False),
           I.dot(533, 684, 7, "#cbd2d8", 1.1), I.label(500, 440, "1977 · a Senate hearing", .6, BONE, 32)] +
          sum([[_folder(x - 60, y - 34, 120, 70, at, fx="pop"), I.label(x + 80, y + 10, t, at + .2, BONE, 30, "start"),
                I.line([[x + 300, y], [P0[0] - 20, P0[1]]], round(at + .5, 2), GREEN, 4, dur=.8)] for x, y, at, t in src], []) +
          [I.dot(P0[0], P0[1], 16, GREEN, es - .4), I.glow(P0[0], P0[1], 110, es - .4, .5, "lamp"), I.label(P0[0], P0[1] + 80, "Established", es, GREEN, 40, st="serif")] +
          [I.glow(500, 1330, 260, T(5, "behind"), .4, "lamp")] + [I.person(260 + 80 * k, 1400, 92, round(T(5, "behind") + .15 * k, 2), c="#7a7268") for k in range(7)]}
    s6 = like(s0, cam=[1.12, 520, 1000])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    return EP("mkultra", "13.01", "MKUltra: the files that survived", "mkultra", "solid", "The CIA ran illegal drug experiments on unwitting people?", "Not a theory. *On the record.*", beats, shots,
              "US Senate hearing on MKULTRA, 1977 · Church Committee report, 1976 · CIA Inspector General, 1963",
              "MKUltra isn't a theory, it's paperwork. What the CIA did, what it shredded, and how 20,000 pages survived. Sources in the case file.",
              ["#MKUltra", "#CIA", "#History", "#DeclassifiedFiles", "#WeighItYourself"], mood="cold")


def mkultra_m():
    """MKUltra as one continuous take (see mural.py): a rumour struck out by a stack of files, 149 subprojects, a watched room,
    nine days and twenty-two years, a shelf burned and a box of accounts missed, three records that agree; back to the files."""
    return remix(mkultra(), alias={6: 0})


def EPISODES():
    return [where_we_stand_m(), mkultra_m()]
