"""LF.06 Impossible Stones (16:9 long form): how do you move a 1,000-tonne stone? Baalbek, Puma Punku, Sacsayhuamán, weighed.

Script: films/long/lf-impossible-stones/script.json (its lines are read from there and kept word for word; this module only adds
the [go:N|t] markers where the picture changes). One scene per script shot (s1..s58 = ep shots 0..57), hung on one wall
(mural.wall), six rooms: the cold open, Giants in a Roman wall, How to move 1,000 tonnes, The kit at Puma Punku, A jigsaw above
Cusco, The weighing. Three shots return to an earlier panel (aliases): s5 and s7 to the quarry of s1, s46 to the jigsaw wall of s4;
their additions are attached to the alias step itself (_attach, after lf_gobekli), timed on the step's own clock.

Drawings are schematic but true to the numbers said: the 2014 block 19.6 x 6 x 5.6 m with a 1.7 m person; the trilithon's three
19 m giants over the course of six; 800 t (the classic estimate) and 1,000 t (the DAI) both marked on the dial; the quarry blocks
1,000 t, 1,240 t and 1,650 t; the podium planned for three or four courses, two built (van Ess 2015); 172 pullers in four rows;
about half the pull on wet sand (Fall et al. 2014); 18 people, 4.35 t, 100 m, 40 minutes (Lipo & Hunt); six capstans of 24 people
(Adam 1977); the Thunder Stone's 6 km and 400 people; the Titicaca map with 90 km and 10 km; the slab 7.8 x 5.2 x 1.1 m (131 t);
AD 536 to 600 on a timeline that starts at 16,000 BCE; 200 figures for 20,000 workers (40 quarrying, 60 hauling); ramps up to 8 m
and 80 abandoned blocks; Killke from about 900 CE. Claims are drawn dotted (lilac), inferences dashed, evidence solid.

Reused from the Shorts (File 06, f06.py): the trilithon wall, the quarry, the H-blocks, the slab and the zigzag terraces (their
iso models, recentred and rescaled for 16:9), the polygonal jigsaw() wall, and the ideas of baalbek_m(), puma_punku_m(),
sacsayhuaman_m() and cart_ruts_m() (the giants and buses, the dig, the capstans, the candle clock, the sliver of a degree, the
clamp, the template, the record, the workers, the carting, the hammerstone cycle), redrawn wide.

Compile (sandbox only):
  cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_lf-impossible-stones/boards && cp ../episodes/files.json /tmp/claude-0/sbx_lf-impossible-stones/
  RC_FILMS_OUT=/tmp/claude-0/sbx_lf-impossible-stones RC_FILMS_EPS=/tmp/claude-0/sbx_lf-impossible-stones/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_lf-impossible-stones/boards python3 films.py long.lf_impossible_stones
"""
import copy, json, math, os, random, re
from films import View
from mural import remix, SENT
from illus import person, arrow, line, glow, label, dot, box, oval, ring, strike, question, ellipse, BONE, AMBER, BLUE, LILAC, GREEN, RED, INK
import f06

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = json.load(open(os.path.join(HERE, "lf-impossible-stones", "script.json"), encoding="utf-8"))

W_, H_ = 1778, 1000            # the 16:9 frame: drawings in x 80..1700, y 120..800 (captions below 815, HUD above 110)
CAM = [1, 889, 500]
GOLD, DIM, WARM = "#f2c98e", "#cbbca8", "#ffb07a"
LIME, LIME_E, LIME_D = "#d8c49c", "#f2dcb4", "#a8946c"         # Baalbek limestone
AND, AND_E = "#8d8e8a", "#e8e2d6"                              # andesite
SAND_R = "#b06a4e"                                             # red sandstone
BRZ = "#c8743c"                                                # bronze
GRAN = "#9a938a"                                               # granite
GRADE = {"strong": "#7fd1d4", "established": "#8fd9b0", "awaiting": "#c9c1ee", "open": "#f0b06a", "ruled": "#e98a8a", "mixed": "#d8c7a8"}
FLAT = "#17120e"
C30 = math.cos(math.pi / 6)


# ================================================================ small drawing helpers (panel units)
def r1(v):
    return round(v, 1)


def R(pts):
    return [[r1(x), r1(y)] for x, y in pts]


def poly(pts, fill, c="none", w=0, at=0, fx=None, curve=False, op=None, **kw):
    e = {"k": "poly", "p": R(pts), "fill": fill, "c": c, "w": w, "curve": curve, "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    if op is not None:
        e.update(op=op, keepop=True)
    e.update(kw)
    return e


def rect(x, y, w, h, fill="none", c="none", sw=0, r=0, at=0, fx=None, op=None, **kw):
    return box(r1(x), r1(y), r1(w), r1(h), fill, c, sw, r, round(at, 2), op, fx, **kw)


def lab(x, y, t, at=0, c=BONE, size=30, a="middle", st="lab", **kw):
    return label(r1(x), r1(y), t, round(at, 2), c, size, a, st=st, **kw)


def ink(x, y, t, at=0, c=INK, size=28, a="middle", st="lab"):
    return label(r1(x), r1(y), t, round(at, 2), c, size, a, st=st, halo=False)


def ln(p, at=0, c=BONE, w=3, style="known", dur=None, curve=False, draw=True, op=None):
    return line(R(p), round(at, 2), c, w, style, dur, curve, draw, op)


def arr(p, at=0, c=AMBER, w=3, style="known", dur=1.0, curve=True):
    return arrow(R(p), round(at, 2), c, w, style, dur, curve)


def gl(x, y, r=120, at=0, op=.6, kind="lamp"):
    return glow(r1(x), r1(y), r, round(at, 2), op, kind)


def pe(x, y, h=90, at=0, c="#e8d6b8", fx="rise", op=None):
    e = person(r1(x), r1(y), h, round(at, 2), c, fx)
    if op is not None:
        e.update(op=op, keepop=True)
    return e


def dt(x, y, r=6, fill=BONE, at=0, fx="pop", op=None):
    return dot(r1(x), r1(y), r, fill, round(at, 2), fx, op)


def rg(x, y, r, at=0, c=AMBER, w=3, style="known", dur=1.0):
    return ring(r1(x), r1(y), r, round(at, 2), c, w, style, dur)


def qm(x, y, at, size=90, c=LILAC):
    return question(r1(x), r1(y), round(at, 2), size, c)


def chip(x, y, t, c, at, size=28, a="middle"):
    """A grade chip: a dark pill with a coloured rim and its words."""
    w = len(t) * size * .56 + 44
    h = size * 1.7
    x0 = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    return [box(r1(x0), r1(y - h / 2), r1(w), r1(h), "rgba(18,13,10,.9)", c, 2.5, h / 2, round(at, 2), fx="pop"),
            label(r1(x0 + w / 2), r1(y + size * .36), t, round(at + .05, 2), c, size, scl=True, fx="pop")]


def dimline(x1, y1, x2, y2, t, at, c=GOLD, lx=0, dur=1.0, **kw):
    e = {"k": "dim", "x1": r1(x1), "y1": r1(y1), "x2": r1(x2), "y2": r1(y2), "t": t, "c": c, "fx": "draw", "dur": dur, "in": round(at, 2), "lx": lx}
    e.update(kw)
    return e


def stars(n, x0, x1, y0, y1, at=-1, seed=3):
    return {"k": "stars", "n": n, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "seed": seed, "in": at}


def tick(x, y, at, c=GREEN, s=1.0):
    return {"k": "line", "p": R([(x - 16 * s, y), (x - 4 * s, y + 13 * s), (x + 20 * s, y - 16 * s)]), "c": c, "w": 6, "fx": "draw", "dur": .45, "in": round(at, 2)}


def cross(x, y, at, c=RED, s=16, w=6):
    return [strike(r1(x - s), r1(y - s), r1(x + s), r1(y + s), round(at, 2), c, w), strike(r1(x + s), r1(y - s), r1(x - s), r1(y + s), round(at + .1, 2), c, w)]


def group(els, tr, at=0, **kw):
    g = {"k": "group", "tr": tr, "in": round(at, 2), "els": els}
    g.update(kw)
    return g


def block3d(x, y, w, h, d, at, fx="rise", **kw):
    """A stone block in oblique view (kit LIB.block): front face x..x+w, base on y, depth d (top and side faces)."""
    e = {"k": "block", "x": r1(x), "y": r1(y), "w": r1(w), "h": r1(h), "d": r1(d), "in": round(at, 2)}
    if fx:
        e["fx"] = fx
    e.update(kw)
    return e


def iso(items, x, y, s, az, spin=0.0, el=.32, at=-1, **kw):
    e = {"k": "iso", "x": x, "y": y, "s": s, "az": az, "spin": spin, "el": el, "items": items, "in": at}
    e.update(kw)
    return e


def ov(base, items, at, fx="pop", **kw):
    """An overlay model: the same camera, scale and turn as `base`, other items, its own build-in."""
    e = {k: base[k] for k in ("x", "y", "s", "az", "spin", "el")}
    e.update(k="iso", items=items, **{"in": round(at, 2)})
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


def hi(it, c=GOLD, op=.25, style="known"):
    """A highlight of one iso item: the same solid, see-through, outlined in colour."""
    e = dict(it)
    e.update(c=c, xray=True, edge=c, op=op, style=style)
    return e


def rim(it, c=GOLD, w=4):
    """The top outline of an iso box, as a thick line."""
    x0, x1, z0, z1, y = it["x"] - it["w"] / 2, it["x"] + it["w"] / 2, it["z"] - it["d"] / 2, it["z"] + it["d"] / 2, it["y"] + it["h"]
    return {"t": "line", "p": [[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1], [x0, y, z0]], "c": c, "w": w}


def ibox(x, z, y, w, d, h, c=LIME, e="rgba(0,0,0,.32)"):
    return {"t": "box", "x": x, "z": z, "y": y, "w": w, "d": d, "h": h, "c": c, "edge": e}


def ilab(x, y, z, t, c=BONE, dy=0, st="lab", a="middle"):
    return {"t": "label", "x": x, "y": y, "z": z, "text": t, "st": st, "c": c, "dy": dy, "a": a}


def short_iso(fn, k=0):
    """The iso model of a Short's shot k (f06), without its labels."""
    e = copy.deepcopy(next(x for x in fn()["shots"][k]["els"] if x.get("k") == "iso"))
    e["items"] = [it for it in e["items"] if it.get("t") != "label"]
    return e


def tv(cx, cy, w, at, screen_els=(), c="#3a2f26"):
    """An old television set: a wooden cabinet, a rounded screen (its contents drawn by the caller), two knobs and an aerial."""
    h = w * .72
    x0, y0 = cx - w / 2, cy - h / 2
    sw, sh = w * .7, h * .78
    sx, sy = x0 + w * .06, y0 + h * .11
    els = [rect(x0 + 10, y0 + 14, w, h, "rgba(0,0,0,.45)", r=22, at=at),
           rect(x0, y0, w, h, c, "#8a6a48", 3, 22, at, fx="pop"),
           rect(sx, sy, sw, sh, "#10151a", "#6a5a48", 3, 30, at + .1),
           ln([[cx - w * .12, y0], [cx - w * .3, y0 - h * .38]], at + .2, "#8a7a66", 3, draw=False),
           ln([[cx + w * .02, y0], [cx + w * .2, y0 - h * .42]], at + .2, "#8a7a66", 3, draw=False),
           dt(x0 + w * .88, y0 + h * .3, w * .035, "#c9b48a", at + .2), dt(x0 + w * .88, y0 + h * .5, w * .035, "#c9b48a", at + .25),
           gl(sx + sw / 2, sy + sh / 2, sw * .55, at + .3, .35, "blue")]
    return els + list(screen_els), (sx, sy, sw, sh)


# ================================================================ timing: when each word is said (an estimate, from syllables)
TAGS = re.compile(r"\[[^\]]*\]")
GOM = re.compile(r"\[go:(\d+)")
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
    return re.sub(r"@\w+", "", s.replace("^", "").replace("*", "")).split()


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Clock:
    """Estimated word times per beat (seconds from the beat's first word). A shot's step starts at its [go:] marker (or at the beat's
    first word; at a chapter beat's second sentence, when the camera leaves the card). at(i, phrase) = when the phrase is said,
    counted from the start of shot i's step (or of shot `ref`'s)."""
    def __init__(self, beats):
        self.start, self.words = {}, {}
        for bi, b in enumerate(beats):
            t, ws, sents = 0.0, [], []
            for li, ln_ in enumerate(b["lines"]):
                if li:
                    t += LGAP
                cuts = [0] + [m.start() for m in SENT.finditer(ln_) if m.start() > 0] + [len(ln_)]
                for a, z in zip(cuts, cuts[1:]):
                    seg = ln_[a:z]
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

    def at(self, i, phrase, ref=None, lo=.4, d=0.0, after=None):
        bi, ti = self.start[i]
        t0 = self.start[ref if ref is not None else i][1]
        if after:                                     # search from where `after` is said
            ti = self.at(i, after, lo=-1e9) + t0
        want = [_norm(x) for x in phrase.split()]
        ws = self.words[bi]
        for k in range(len(ws)):
            if ws[k][1] >= ti - 1e-6 and [w for w, _ in ws[k:k + len(want)]] == want:
                return round(max(lo, ws[k][1] - t0 + d), 2)
        raise ValueError("phrase not found after shot %d: %r" % (i, phrase))

    def end(self, i):
        """When the last word of shot i's beat is said, from the start of shot i's step."""
        bi, ti = self.start[i]
        return round(self.words[bi][-1][1] - ti, 2)


# ================================================================ the narration: the script's lines, with [go:] markers added
TAGRUN = re.compile(r"\[(\w+):[^\]]*\]$")


def go_at(ln_, anchor, n, t=1.6):
    """Put [go:n|t] at the start of the sentence whose words begin with `anchor`: before the run of tags in front of it
    ([p:]/[act:]/[tune:]...), after a [d:] mood tag if the run opens with one."""
    assert ln_.count(anchor) == 1, (anchor, ln_[:80])
    i = ln_.index(anchor)
    j = i
    while j > 0 and ln_[j - 1] == "]":
        j = ln_.rindex("[", 0, j - 1)
    if ln_.startswith("[d:", j):
        j = ln_.index("]", j) + 1
    return ln_[:j] + "[go:%d|%s]" % (n, t) + ln_[j:]


# shot index -> (chapter, beat, anchor: the first words of the sentence where the picture changes; None = the beat's own panel)
GO = {
    0: (0, 0, None), 1: (0, 0, "Nearby, three of its cousins"), 2: (0, 0, "In Bolivia, hard grey"), 3: (0, 0, "In Peru, walls so tight"),
    4: (0, 0, "So how could anyone"), 5: (0, 0, "On television, the answer"),
    6: (0, 1, None),
    7: (1, 0, None), 8: (1, 0, "Its platform holds"), 9: (1, 0, "Each weighs about eight"), 10: (1, 0, "And in the quarry, less than"),
    11: (1, 1, None),
    12: (1, 2, None), 13: (1, 2, "One geologist dated"), 14: (1, 2, "You date what the builders"), 15: (1, 2, "Inside the Roman platform"),
    16: (1, 3, None), 17: (1, 3, "The block found in {2014"), 18: (1, 3, "And the Roman ^silence"), 19: (1, 3, "And why leave the biggest"),
    20: (2, 0, None), 21: (2, 0, "Think of shoving"), 22: (2, 0, "Put a stone on a sledge"),
    23: (2, 1, None), 24: (2, 1, "In {2014|twenty fourteen}, a team"), 25: (2, 1, "Other experiments keep"),
    26: (2, 2, None), 27: (2, 2, "In {1977"),
    28: (2, 3, None), 29: (2, 3, "It still carries"),
    30: (2, 4, None),
    31: (3, 0, None), 32: (3, 0, "Today they lie broken"), 33: (3, 0, "The andesite came from"), 34: (3, 0, "Its biggest slab"),
    35: (3, 1, None), 36: (3, 1, "From the mismatch"), 37: (3, 1, "And on television, the blocks"),
    38: (3, 2, None), 39: (3, 2, "Organic material from"), 40: (3, 2, "Posnansky's method"),
    41: (3, 3, None), 42: (3, 3, "Architects who measured"), 43: (3, 3, "And the tools that cut"),
    44: (4, 0, None), 45: (4, 0, "Some stones weigh well"),
    46: (4, 1, None),
    47: (4, 2, None), 48: (4, 2, "One of them, Pedro"), 49: (4, 2, "And the rougher upper"),
    50: (4, 3, None), 51: (4, 3, "To fit two stones"), 52: (4, 3, "At the Inca quarry"),
    53: (4, 4, None),
    54: (5, 0, None), 55: (5, 0, "Taken together"),
    56: (5, 1, None),
    57: (5, 2, None),
}
NSHOT = 58
ALIAS = {4: 0, 6: 0, 45: 3}
ALIAS_CAMS = {4: [1, 889, 500], 6: [1, 889, 500], 45: [1.18, 760, 470]}


def B(role, frm, lines, **kw):
    b = {"role": role, "visual": {"from": frm}, "lines": lines}
    b.update(kw)
    return b


def BEATS():
    beats = []
    for ci, ch in enumerate(SCRIPT["chapters"]):
        for bi, sb in enumerate(ch["beats"]):
            lines = list(sb["lines"])
            mine = sorted(i for i, g in GO.items() if g[:2] == (ci, bi))
            frm = mine[0]
            assert GO[frm][2] is None
            for i in mine[1:]:
                anchor = GO[i][2]
                hits = [li for li, l in enumerate(lines) if anchor in l]
                assert len(hits) == 1, (i, anchor, hits)
                t = 1.4 if i in ALIAS else 1.6
                lines[hits[0]] = go_at(lines[hits[0]], anchor, i, t)
            kw = {}
            if ci > 0 and bi == 0:
                kw["chapter"] = ch["title"]
            if sb.get("intro") or sb["role"] == "title":
                kw["intro"] = True
            beats.append(B(sb["role"], frm, lines, **kw))
    return beats


# ================================================================ scenes (filled below)
def placeholder(i):
    return {"base": "dark", "stars": 20, "cam": CAM, "els": [lab(889, 470, "shot s%d" % (i + 1), .3, GOLD, 40)]}


SCENES = {}          # shot index -> function(C) returning a scene
LATES = {}           # alias shot index -> function(C) returning the elements it adds


def scene(i):
    def deco(f):
        SCENES[i] = f
        return f
    return deco


def late(i):
    def deco(f):
        LATES[i] = f
        return f
    return deco


# ================================================================ the cold open
QX, QY, QS = 240, 712, 40          # the 2014 block: front-left corner, base line, units a metre (19.6 x 5.6 m, 6 m deep)


def quarry_block(at=.2, tod="dusk"):
    """The 2014 block in its cutting: the bedrock face behind, the quarry floor, the block (19.6 m long, 5.6 m high, 6 m deep)."""
    w, h, d = 19.6 * QS, 5.6 * QS, 6 * QS
    face = [(-40, 470), (120, 452), (260, 470), (420, 448), (640, 462), (900, 440), (1180, 456), (1420, 438), (1640, 452), (1820, 446), (1820, 712), (-40, 712)]
    els = [poly(face, "#5c4a37", "rgba(255,226,190,.25)", 1.5, -1),
           ln([[-40, 520], [1820, 512]], -1, "#3e3125", 2, "inferred", draw=False, op=.6),
           ln([[-40, 586], [1820, 578]], -1, "#3e3125", 2, "inferred", draw=False, op=.6),
           ln([[-40, 650], [1820, 645]], -1, "#3e3125", 2, "inferred", draw=False, op=.6),
           rect(-40, QY, 1860, 300, "#3a2e23", r=0, at=-1),
           block3d(QX, QY, w, h, d, at, fx="rise"),
           poly([(QX - 30, QY + 2), (QX + w + d * .6 + 40, QY + 2), (QX + w + d * .6 + 60, QY + 26), (QX - 50, QY + 26)], "#2c231b", at=-1)]
    return els, (QX, QY, w, h, d)


@scene(0)
def s01(C):
    """The hook: dusk in the quarry at Baalbek; the 2014 block in its cutting, a person on top; a thousand cars fill in beside it;
    '1,650 t' as the weight is said."""
    els, (x, y, w, h, d) = quarry_block(.2)
    tc, tw = C.at(0, "thousand cars"), C.at(0, "About sixteen hundred")
    els += [gl(x + w * .5, y - h * .6, 520, .4, .28, "lamp"),
            gl(x + w * .55 + d * .3, y - h - d * .2 - 30, 70, 1.2, .55, "lamp"),
            pe(x + w * .55 + d * .3, y - h - d * .2, 1.7 * QS, 1.2, "#f5ecdc")]
    # a thousand cars, 50 x 20, in a car park on the quarry floor to the right
    cx0, cy0, cw, ch = 1255, 520, 8.8, 9.0
    els += [rect(cx0 - 14, cy0 - 14, 50 * cw + 28, 20 * ch + 28, "rgba(18,13,10,.82)", "rgba(255,236,206,.25)", 1.5, 10, tc - .2)]
    for r_ in range(20):
        for c_ in range(50):
            els.append(rect(cx0 + c_ * cw, cy0 + r_ * ch, 6.6, 4.6, "#e8b87a" if (r_ * 50 + c_) % 7 else "#cfd8de", r=1.5, at=round(tc + .06 * r_, 2)))
    els += [lab(cx0 + 25 * cw, cy0 + 20 * ch + 52, "a thousand cars", tc + .6, AMBER, 28),
            ink(x + w / 2, y - h / 2 + 18, "1,650 t", tw, "#2a1d12", 56, st="serif"),
            gl(x + w / 2, y - h / 2, 240, tw, .35, "lamp")]
    return {"base": "sky", "tod": "dusk", "ground": 712, "sun": [1500, 400, 26], "cam": CAM, "els": els}


@late(4)
def s05_late(C):
    """s5: back on the block: people with ropes, ropes slack; a large lilac question mark above the block."""
    x, y, w, h, d = QX, QY, 19.6 * QS, 5.6 * QS, 6 * QS
    t = C.at(4, "move")
    out = []
    for k in range(6):
        px = 96 + 24 * k
        at = round(.5 + .12 * k, 2)
        out += [pe(px, y, 1.7 * QS, at, "#e8d6b8"),
                ln([[px + 6, y - 40], [(px + x) / 2, y - 10 + 6 * k], [x + 2, y - 70 - 14 * k]], at + .2, "#c9a070", 2, curve=True, dur=.6)]
    out += qm(x + w / 2 + 60, 300, t, 120)
    return out


@scene(1)
def s02(C):
    """s2: the trilithon wall as an iso model (f06 baalbek shot 0): the six-block course and the three giants; each giant lights in gold;
    a 19 m dimension along the middle one; a person at its foot."""
    base = short_iso(f06.baalbek, 0)
    base.update(x=889, y=545, s=20, az=-40, spin=.12, el=.24, **{"in": -1})
    base["items"][0].update(x0=-31, x1=31, z0=-7, z1=9)
    giants = [it for it in base["items"] if it.get("t") == "box" and it.get("y") == 4]
    t19 = C.at(1, "each about nineteen")
    els = [gl(889, 560, 620, -1, .2, "lamp"), base]
    els += [ov(base, [hi(g), rim(g)], .5 + .35 * k, fx="draw", dur=.8) for k, g in enumerate(giants)]
    els += [ov(base, [{"t": "line", "p": [[-9.47, 8.9, 1.8], [9.47, 8.9, 1.8]], "c": BONE, "w": 3},
                      {"t": "line", "p": [[-9.47, 8.4, 1.8], [-9.47, 9.4, 1.8]], "c": BONE, "w": 3},
                      {"t": "line", "p": [[9.47, 8.4, 1.8], [9.47, 9.4, 1.8]], "c": BONE, "w": 3}], t19, fx="draw", dur=.8)]
    tx, ty = P3(base, (0, 9.6, 1.8), t19)
    els += [lab(tx, ty - 14, "19 m", t19 + .4, BONE, 34)]
    return {"base": "dark", "stars": 60, "cam": CAM, "els": els}


@scene(2)
def s03(C):
    """s3: four andesite H-blocks (f06 puma-punku shot 0); the inside corners of one glow and its inner H traces in gold."""
    base = short_iso(f06.puma_punku, 0)
    base.update(x=889, y=585, s=132, az=-22, spin=.4, el=.42, **{"in": -1})
    x1 = -1.8
    corners = [{"t": "glow", "x": x1 + u, "y": v, "z": .36, "r": 40, "kind": "lamp"} for u, v in ((.34, .36), (.86, .36), (.34, .64), (.86, .64))]
    inner = {"t": "line", "p": [[x1 + .34, .64, .36], [x1 + .34, .36, .36], [x1 + .86, .36, .36], [x1 + .86, .64, .36], [x1 + .34, .64, .36]], "c": GOLD, "w": 4}
    return {"base": "dark", "stars": 50, "cam": CAM, "els": [gl(889, 560, 600, -1, .2, "lamp"), base, ov(base, corners, .6), ov(base, [inner], 1.0, fx="draw", dur=.8)]}


JIG = (300, 210, 1180, 560, 8, 4)          # the polygonal wall of s4 / s46: x0, y0, w, h, cols, rows


def jig_wall(at=0.0, step=.025):
    wall = f06.jigsaw(*JIG)
    for k, e in enumerate(wall):
        e["in"] = round(at + step * k, 2)
    return wall


def jig_giant(wall):
    return next(e for e in wall if e["fill"] == "#d9c9a6" and len(e["p"]) > 12)["p"]


def knife(tip, at):
    """A steel knife lying flat, its tip at `tip`, the blade pointing left."""
    x, y = tip
    return [poly([(x, y), (x + 260, y - 24), (x + 260, y + 10)], "#e4e8ec", "#9aa0a8", 2, at, fx="pop"),
            rect(x + 258, y - 28, 150, 42, "#5a3a22", "#c9a070", 2, 10, at)]


@scene(3)
def s04(C):
    """s4: the polygonal wall (f06 jigsaw(), wide): stones cut to fit, no mortar; a knife comes to a joint and stops; a red cross."""
    wall = jig_wall(.1, .02)
    g = jig_giant(wall)
    ys = [p[1] for p in g]
    mid = [p for p in g if min(ys) + .3 * (max(ys) - min(ys)) <= p[1] <= min(ys) + .7 * (max(ys) - min(ys))]
    right = max(mid, key=lambda p: p[0])
    tip = (right[0] + 2, right[1])
    x0, y0, w, h = JIG[:4]
    return {"base": "dark", "stars": 30, "floor": y0 + h, "cam": CAM, "els": wall + [
        pe(x0 + w + 70, y0 + h, 150, .6, "#e8d6b8"),
        gl(tip[0], tip[1], 140, 1.6, .6, "lamp")] + knife(tip, 1.4) + cross(tip[0] + 40, tip[1] - 80, 2.6, RED, 22, 7)}


@scene(5)
def s06(C):
    """s6: an old television: on its screen the block glows lilac, dotted 'beams' play over it; 'lost technology?'."""
    els, (sx, sy, sw, sh) = tv(889, 430, 620, .3)
    bx0, by0 = sx + sw * .16, sy + sh * .62
    els += [rect(bx0, by0, sw * .68, sh * .2, "rgba(201,193,238,.25)", LILAC, 2, 4, .8),
            rect(bx0 + sw * .68, by0 - sh * .06, sw * .08, sh * .2, "rgba(201,193,238,.15)", LILAC, 1.5, 2, .8)]
    for k in range(4):
        els.append(ln([[sx + sw * (.15 + .22 * k), sy + 10], [bx0 + sw * (.1 + .16 * k), by0]], 1.4 + .25 * k, LILAC, 3, "claimed", .6))
    els += [gl(bx0 + sw * .34, by0, 120, 1.6, .5, "blue"),
            lab(889, 720, "lost technology?", C.at(5, "lost technology") - .3, LILAC, 36, st="serif")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


# ================================================================ chapter 1: Giants in a Roman wall
@scene(7)
def s08(C):
    """s8: Lebanon and its neighbours: the Mediterranean, Beirut, Damascus; Baalbek in the Beqaa valley; a temple glyph at 'Jupiter'."""
    v = View(32.8, 39.2, 32.55, 35.15, (90, 120, 1600, 680))
    bx, by = v.p(36.2039, 34.0069)
    tj, th = C.at(7, "Jupiter"), C.at(7, "Heliopolis")
    tx, ty = bx + 4, by - 118
    temple = [ln([[tx - 62, ty - 16], [tx + 62, ty - 16]], tj, AMBER, 4, dur=.4),
              poly([(tx - 66, ty - 18), (tx, ty - 52), (tx + 66, ty - 18)], "none", AMBER, 3, tj + .2, fx="draw", dur=.6)] + \
             [ln([[tx - 50 + 20 * k, ty - 12], [tx - 50 + 20 * k, ty + 40]], tj + .05 * k, AMBER, 5, dur=.3) for k in range(6)] + \
             [ln([[tx - 70, ty + 44], [tx + 70, ty + 44]], tj, AMBER, 4, dur=.4), gl(tx, ty + 10, 110, tj, .5)]
    els = [{"k": "map", "land": v.land(), "in": -1},
           {"k": "pin", "x": bx, "y": by, "t": "Baalbek", "c": GOLD, "in": .5},
           gl(bx, by, 90, .6, .5)]
    for name, lo, la, a in (("Beirut", 35.50, 33.89, "end"), ("Damascus", 36.29, 33.51, "start")):
        px, py = v.p(lo, la)
        els += [dt(px, py, 7, DIM, 1.0), lab(px + (-16 if a == "end" else 16), py + 9, name, 1.0, DIM, 26, a)]
    vx, vy = v.p(35.62, 33.62)
    mx, my = v.p(34.0, 33.6)
    lx_, ly_ = v.p(38.0, 33.3)
    els += [lab(vx, vy + 60, "the Beqaa valley", 1.6, "#c9ad85", 30, "end", st="ital"),
            ln([[vx + 6, vy + 46], [v.p(35.95, 33.8)[0], v.p(35.95, 33.8)[1]]], 1.6, "#c9ad85", 2, "inferred", .6),
            lab(lx_, ly_, "Syria", .3, DIM, 28), lab(*v.p(35.62, 34.38), "Lebanon", .3, DIM, 28, "end"),
            lab(mx, my, "the Mediterranean", .3, BLUE, 30, st="ital"),
            lab(tx + 90, ty + 4, "Roman Heliopolis", th + .3, AMBER, 30, "start"),
            {"k": "scale", "x": 140, "y": 760, "w": r1(v.km(50)), "t": "50 km", "in": .4}] + temple
    return {"base": "map", "cam": CAM, "els": els}


WS = 26                                 # the western wall in elevation: 26 units a metre
WX0, WG = 144, 720                      # its left end and the ground line


def west_wall(at=-1, giants_at=None, ink_=False):
    """The course of six (about 9.5 x 3.9 m) and the trilithon above (three giants, 19.1 x 4.35 m), to one scale."""
    els = []
    c1, c2 = 3.9 * WS, 4.35 * WS
    for k in range(6):
        els.append(rect(WX0 + k * 9.55 * WS, WG - c1, 9.55 * WS - 3, c1, "#c8b692", "#2a2219", 2, 3, at))
    ga = at if giants_at is None else giants_at
    for k in range(3):
        els.append(rect(WX0 + k * 19.1 * WS, WG - c1 - c2, 19.1 * WS - 3, c2, "#e0cfa8", "#2a2219", 2, 3, ga if isinstance(ga, (int, float)) else ga[k], fx=None))
    return els, (c1, c2)


@scene(8)
def s09(C):
    """s9: the wall in elevation, to scale: the giants outline in gold; '19 m' along the middle one; two 10 m buses above it, almost
    as long; a person at the foot."""
    els, (c1, c2) = west_wall(-1)
    tt, t3, t19, tb = C.at(8, "trilithon"), C.at(8, "three limestone"), C.at(8, "each about nineteen"), C.at(8, "almost two buses")
    top = WG - c1 - c2
    for k in range(3):
        x = WX0 + k * 19.1 * WS
        els += [rect(x - 2, top - 2, 19.1 * WS + 1, c2 + 4, "none", GOLD, 4, 4, t3 + .4 * k, fx="draw", dur=.6), gl(x + 9.5 * WS, top + c2 / 2, 200, t3 + .4 * k, .35)]
    gx0, gx1 = WX0 + 19.1 * WS, WX0 + 38.2 * WS - 3
    els += [lab((gx0 + gx1) / 2, top - 250, "the trilithon", tt, GOLD, 34, st="serif"),
            dimline(gx0, top - 40, gx1, top - 40, "19 m", t19, BONE, dur=.8),
            pe(WX0 - 30, WG, 1.7 * WS, .8, "#e8d6b8")]
    by = 330
    for k in range(2):
        bx = gx0 + k * 10.5 * WS
        els += [rect(bx, by, 10.5 * WS - 6, 3 * WS, "#c8743c", "rgba(255,236,206,.6)", 2, 10, tb + .35 * k, fx="rise"),
                rect(bx + 14, by + 12, 10.5 * WS - 34, 22, "#f2e6cc", r=4, at=tb + .35 * k + .1),
                dt(bx + 40, by + 3 * WS, 13, "#2a2219", tb + .35 * k + .1), dt(bx + 10.5 * WS - 46, by + 3 * WS, 13, "#2a2219", tb + .35 * k + .1)]
    els += [ln([[gx0, by + 3 * WS + 14], [gx0, top - 60]], tb + .6, DIM, 2, "inferred", .4), ln([[gx1, by + 3 * WS + 14], [gx1, top - 60]], tb + .6, DIM, 2, "inferred", .4),
            lab(gx0 + 21 * WS + 20, by + 50, "two buses", tb + .8, AMBER, 28, "start")]
    return {"base": "sky", "tod": "dusk", "ground": WG, "sun": [1580, 520, 22], "cam": CAM, "els": els}


@scene(9)
def s10(C):
    """s10: a weighing scale: one giant on its platform; the dial's needle marks 800 t (the classic estimate, dashed) and 1,000 t
    (the German team, gold): sources disagree, both are shown."""
    t8, t10 = C.at(9, "eight hundred tonnes"), C.at(9, "nearer a")
    bw, bh = 19.1 * 30, 4.35 * 30
    px0, py = 200, 470
    els = [rect(px0 - 30, py, bw + 60, 22, "#6b5640", "#c9a070", 2, 4, .2),
           rect(px0 + bw / 2 - 30, py + 22, 60, 190, "#4a3a2c", "#8c7152", 2, 2, .2),
           rect(px0 + bw / 2 - 160, py + 212, 320, 26, "#6b5640", "#c9a070", 2, 6, .2),
           block3d(px0, py, bw, bh, 3.6 * 30, .5),
           lab(px0 + bw / 2, py - bh - 90, "one giant", .8, GOLD, 30)]
    cx, cy, R_ = 1270, 470, 240
    ang = lambda v: math.radians(-210 + 240 * v / 1200)
    els += [{"k": "circle", "x": cx, "y": cy, "r": R_ + 18, "fill": "#2a221b", "c": "#c9a070", "w": 4, "in": .4},
            {"k": "circle", "x": cx, "y": cy, "r": R_, "fill": "#efe6d2", "c": "none", "w": 0, "in": .4},
            ln([[px0 + bw + 30, py + 11], [cx - R_ - 18, cy]], .4, "#8c7152", 4, draw=False)]
    for v_ in range(0, 1201, 100):
        a = ang(v_)
        r0 = R_ - (30 if v_ % 400 == 0 else 16)
        els.append(ln([[cx + r0 * math.cos(a), cy + r0 * math.sin(a)], [cx + (R_ - 4) * math.cos(a), cy + (R_ - 4) * math.sin(a)]], .5, "#3a2c20", 3, draw=False))
        if v_ % 400 == 0:
            els.append(ink(cx + (R_ - 66) * math.cos(a), cy + (R_ - 66) * math.sin(a) + 10, "{:,}".format(v_), .6, "#3a2c20", 26))
    els += [ink(cx, cy + 120, "tonnes", .6, "#6a5a48", 24)]
    for v_, t, c, st, txt, sub in ((800, t8, "#8a7a66", "inferred", "800 t", "classic estimate"), (1000, t10, "#b0702a", "known", "1,000 t", "German team")):
        a = ang(v_)
        els += [ln([[cx, cy], [cx + (R_ - 40) * math.cos(a), cy + (R_ - 40) * math.sin(a)]], t, c, 7, st, .5),
                lab(cx + (R_ + 44) * math.cos(a), cy + (R_ + 44) * math.sin(a) - 6, txt, t + .4, GOLD if v_ == 1000 else BONE, 34, "start", st="serif"),
                lab(cx + (R_ + 44) * math.cos(a), cy + (R_ + 44) * math.sin(a) + 28, sub, t + .7, GOLD if v_ == 1000 else DIM, 24, "start")]
    els += [dt(cx, cy, 16, "#3a2c20", .5)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


@scene(10)
def s11(C):
    """s11: the quarry (f06 baalbek shot 2): the Stone of the Pregnant Woman, the 2014 block and the block found in the 1990s light in
    gold as their weights are said; a small plan: temple to quarry, less than 1 km."""
    base = short_iso(f06.baalbek, 2)
    base.update(x=930, y=560, s=24, az=-30, spin=.25, el=.4, **{"in": -1})
    base["items"][0].update(x0=-15, x1=15, z0=-24, z1=19)
    base["items"] = base["items"][:1] + [ibox(0, -24, 0, 30, 2, 8, "#9c8a6a", "rgba(0,0,0,.3)"), ibox(0, -22.5, 0, 30, 1.5, 4.5, "#a8946c", "rgba(0,0,0,.3)")] + base["items"][1:]
    q = [it for it in base["items"] if it.get("t") in ("ext", "box") and it.get("w") != 30]
    names = [("about a thousand tonnes", "1,000 t", (0, 8.0, -18)), ("about twelve hundred", "1,240 t", (1, 5.6, 13)), ("and the one found", "1,650 t", (-.2, 6.8, -2))]
    order = [0, 2, 1]                   # q is [tilted (Pregnant Woman), 2014 block, 1990s block]
    els = [gl(889, 520, 640, -1, .2, "lamp"), base]
    for k, (phrase, t_, p_) in enumerate(names):
        it = q[order[k]]
        t = C.at(10, phrase)
        els.append(ov(base, [hi(it, GOLD, .22)] + ([rim(it)] if it["t"] == "box" else []), t, fx="draw", dur=.8))
        x, y = P3(base, p_, t + 1)
        els.append(lab(x, max(y - 30, 160), t_, t + .5, GOLD if k == 2 else BONE, 36 if k == 2 else 32, st="serif"))
    tq = C.at(10, "less than a kilometre")
    els += [rect(110, 640, 430, 110, "rgba(18,13,10,.85)", "rgba(255,236,206,.25)", 1.5, 10, tq - .2),
            poly([(150, 704), (180, 686), (210, 704)], "none", AMBER, 2.5, tq), ln([[150, 726], [210, 726]], tq, AMBER, 3, draw=False),
            ln([[230, 715], [440, 715]], tq + .2, BONE, 3, "inferred", .6), rect(450, 698, 50, 34, "#d6c49c", "#2a2219", 1.5, 3, tq + .6),
            lab(335, 696, "under 1 km", tq + .5, BONE, 26)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


@scene(11)
def s12(C):
    """s12: the giant courses under a Roman temple (schematic): 'older?' in lilac around the giants; beside them, ordinary Roman blocks
    ('usual'); a scroll with blank lines ('no boast')."""
    G, x0 = 720, 170
    c1, c2, u = 70, 78, 156
    els = [ln([[80, G], [1700, G]], -1, "#8c7152", 3, draw=False)]
    els += [rect(x0 + k * u, G - c1, u - 3, c1, "#c8b692", "#2a2219", 2, 2, .3 + .06 * k, fx="pop") for k in range(6)]
    els += [rect(x0 + k * 2 * u, G - c1 - c2, 2 * u - 3, c2, "#e0cfa8", "#2a2219", 2, 2, .8 + .12 * k, fx="pop") for k in range(3)]
    top = G - c1 - c2
    tt, to, tn, tb = C.at(11, "Roman temple"), C.at(11, "older than"), C.at(11, "Nothing else"), C.at(11, "boasts")
    cols = [x0 + 30 + k * (6 * u - 60) / 9 for k in range(10)]
    els += [ln([[x, top - 6], [x, top - 250]], tt - .6 + .05 * k, BONE, 7, dur=.5, op=.85) for k, x in enumerate(cols)]
    els += [rect(x0 + 10, top - 286, 6 * u - 20, 36, "none", BONE, 2.5, 2, tt, fx="draw", dur=.6),
            poly([(x0 + 10, top - 286), (x0 + 3 * u, top - 350), (x0 + 6 * u - 10, top - 286)], "none", BONE, 2.5, tt + .3, fx="draw", dur=.6),
            lab(x0 + 3 * u, 170, "the Roman temple", tt + .4, AMBER, 30),
            rect(x0 - 10, top - 10, 6 * u + 18, c1 + c2 + 18, "rgba(201,193,238,.08)", LILAC, 4, 6, to - .2, style="claimed"),
            lab(x0 + 3 * u, G + 54, "older?", to + .3, LILAC, 34, st="serif"),
            gl(x0 + 3 * u, G - 74, 300, to, .3)]
    rx = 1260
    els += [rect(rx + 26 * k, G - 26 - 26 * (k % 2), 24, 24 + 26 * (k % 2), "#bfae8a", "#2a2219", 1.5, 2, tn + .04 * k, fx="pop") for k in range(12)] + \
           [lab(rx + 150, G + 54, "usual Roman blocks", tn + .6, AMBER, 28)]
    els += [rect(rx, 200, 320, 190, "#e8dcc2", "#8a7a66", 2, 8, tb - .6), rect(rx - 12, 192, 24, 206, "#c9b48a", "#8a7a66", 1.5, 6, tb - .6),
            rect(rx + 308, 192, 24, 206, "#c9b48a", "#8a7a66", 1.5, 6, tb - .6)] + \
           [ln([[rx + 40, 236 + 30 * j], [rx + 280 - 50 * (j % 2), 236 + 30 * j]], tb - .4 + .1 * j, INK, 3, "inferred", .4) for j in (0, 1, 3, 4)] + \
           [lab(rx + 160, 440, "no boast", tb + .2, LILAC, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


@scene(12)
def s13(C):
    """s13: a limestone block in section: fine sea layers and tiny shells ('rock: millions of years'); chisel marks on its face
    ('cut: when?')."""
    x0, y0, w, h = 420, 230, 720, 400
    tones = ["#d8c49c", "#cdb88e", "#dfcda8", "#c9b38a", "#d6c29a", "#cbb590", "#e0cfa8", "#c6b088"]
    els = [rect(x0, y0 + h * k / 8, w, h / 8 + 1, tones[k], r=0, at=.3) for k in range(8)]
    els += [rect(x0, y0, w, h, "none", "#2a2219", 2.5, 4, .3)]
    rnd = random.Random(6)
    for k in range(26):
        sx, sy = rnd.uniform(x0 + 30, x0 + w - 60), rnd.uniform(y0 + 20, y0 + h - 20)
        els.append(ln([[sx - 7, sy], [sx, sy - 6], [sx + 7, sy]], .5, "#8a7356", 2, curve=True, draw=False, op=.7))
    tm, tw = C.at(12, "millions"), C.at(12, "date a wall")
    els += [lab(x0 - 30, y0 + h / 2 - 10, "rock:", tm, BONE, 30, "end"), lab(x0 - 30, y0 + h / 2 + 30, "millions of years", tm + .2, BONE, 30, "end")]
    for k in range(7):
        els.append(ln([[x0 + w - 6, y0 + 40 + 50 * k], [x0 + w - 40, y0 + 70 + 50 * k]], tw + .08 * k, "#5a4632", 4, draw=False))
    els += [poly([(x0 + w + 40, 300), (x0 + w + 180, 270), (x0 + w + 190, 290), (x0 + w + 50, 320)], "#9aa0a8", "#e8e2d6", 1.5, tw + .3, fx="pop"),
            rect(x0 + w + 180, 252, 110, 34, "#5a3a22", "#8a5d33", 1.5, 6, tw + .3),
            lab(x0 + w + 170, y0 + h / 2 + 10, "cut: when?", tw + .7, LILAC, 32, "start", st="serif"),
            gl(x0 + w, y0 + h / 2, 160, tw + .5, .4, "blue")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(13)
def s14(C):
    """s14: cart ruts cut in bare rock, running away in perspective, a cart wheel in one; 'before humans?' struck through. Then a very
    old hill with a new road winding up it: 'hill: very old', 'road: new'."""
    G = 470
    els = [poly([(60, 790), (860, 790), (600, G + 6), (360, G + 6)], "#d9c8a0", "#fff3dc", 1.5, .2)]
    for k in range(6):
        y = G + 30 + (790 - G - 30) * (k / 6) ** 1.6
        hw = 130 + (400 - 130) * (y - G) / (790 - G)
        els.append(ln([[460 - hw, y], [460 + hw, y]], .3, "#b8a57c", 1.5, "inferred", draw=False, op=.6))
    for s_ in (-1, 1):
        nx, fx_ = 460 + s_ * 170, 480 + s_ * 40
        els.append(poly([(nx - 30, 790), (nx + 30, 790), (fx_ + 5, G + 8), (fx_ - 5, G + 8)], "#6d5a3e", at=.5 + .1 * (s_ + 1)))
    els += [rg(290, 690, 80, .9, "#c9a070", 8, dur=.6), ln([[290, 610], [290, 770]], 1.0, "#c9a070", 4, draw=False), ln([[210, 690], [370, 690]], 1.0, "#c9a070", 4, draw=False),
            lab(470, G - 30, "cart ruts", .8, BONE, 30)]
    th, tr = C.at(13, "before humans"), C.at(13, "dating a road")
    els += [lab(470, 260, "before humans?", th, LILAC, 36, st="serif"), strike(320, 276, 620, 226, th + .9, RED, 5)]
    hill_ = [(920, 800), (1000, 680), (1100, 540), (1230, 420), (1350, 370), (1470, 400), (1580, 500), (1660, 640), (1700, 800)]
    els += [poly(hill_, "#4d3e30", "#8a6a48", 2, tr - .6, curve=True)]
    for k in range(5):
        y = 720 - 60 * k
        els.append(ln([[1000 + 40 * k, y], [1640 - 40 * k, y - 10]], tr - .5, "#3e3125", 2, "inferred", draw=False, op=.7))
    road = [(1000, 790), (1360, 730), (1560, 690), (1300, 620), (1200, 560), (1440, 500), (1360, 420)]
    els += [ln(road, tr + .3, "#e8d6b8", 6, dur=1.4, curve=True), ln(road, tr + .3, "#3a2c20", 2, "inferred", dur=1.4, curve=True),
            rect(1340, 402, 34, 16, "#9fd0ff", r=4, at=tr + 1.6, fx="pop"),
            lab(1310, 320, "hill: very old", tr - .2, BONE, 30), lab(1690, 640, "road: new", tr + 1.2, GOLD, 30, "end")]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": False, "cam": CAM, "els": els}


@scene(14)
def s15(C):
    """s15: a trench at dusk, two archaeologists with trowels, a sieve and a lamp; six standing columns on the skyline; a timeline from
    1898 to today, on and off."""
    G = 520
    els = [ln([[1200 + 34 * k, G], [1200 + 34 * k, G - 220]], -1, "#2a2229", 14, draw=False) for k in range(6)]
    els += [rect(1180, G - 250, 220, 30, "#2a2229", r=2, at=-1)]
    els += [poly([(380, G), (1000, G), (960, 700), (420, 700)], "#2a2119", "rgba(255,226,190,.35)", 2, .3),
            rect(440, 650, 500, 50, "#5f4c39", r=0, at=.3)]
    els += [pe(560, 650, 130, .6), pe(820, 650, 124, .8),
            ln([[600, 600], [660, 640]], 1.0, "#c9a070", 5, draw=False), oval(1080, G - 6, 56, 16, "#4a3a2c", "#c9a070", 2, 1, 1.2),
            gl(700, 600, 160, 1.0, .7, "lamp"), dt(700, 600, 8, "#ffcf8a", 1.0)]
    t98 = C.at(14, "since")
    X = lambda yr: 300 + (yr - 1898) / (2026 - 1898) * 1180
    els += [ln([[X(1898), 190], [X(2026), 190]], t98 - .4, "#8c7152", 2, "inferred", .8),
            ln([[X(1898), 190], [X(1905), 190]], t98, GOLD, 8, dur=.4), ln([[X(1997), 190], [X(2026), 190]], t98 + .4, GOLD, 8, dur=.6),
            lab(X(1898), 240, "1898", t98, GOLD, 30), lab(X(2026), 240, "today", t98 + .6, BONE, 28),
            lab(X(1950), 240, "German digs, on and off", t98 + .8, DIM, 26)]
    return {"base": "section", "tod": "dusk", "ground": G, "lx": 1500, "layers": [{"d": 0, "c": "#5f4c39", "t": ""}, {"d": 140, "c": "#4a3a2c", "t": ""}], "cam": CAM, "els": els}


@scene(15)
def s16(C):
    """s16: the platform cut open: inside, an older, smaller terrace of ordinary blocks builds course by course (1); then the giant blocks
    wrap around it on both sides (2): 'later'."""
    G = 720
    els = []
    to, tb, tw, tl = C.at(15, "older, smaller"), C.at(15, "ordinary blocks"), C.at(15, "wraps around"), C.at(15, "came later")
    for r_ in range(5):
        for c_ in range(10):
            els.append(rect(640 + 50 * c_, G - 40 * (r_ + 1), 48, 38, "#a8977c", "#3a2c1e", 1.5, 2, to + .2 * r_ + .02 * c_, fx="pop"))
    els += [lab(889, G + 56, "older terrace", tb, BONE, 32), dt(889, G - 100, 26, AMBER, tb + .2), ink(889, G - 90, "1", tb + .25, INK, 28, st="serif")]
    for side, x in ((-1, 440), (1, 1142)):
        for k in range(3):
            els.append(rect(x, G - 66 * (k + 1), 196, 64, "#e0cfa8", "#2a2219", 2, 3, tw + .25 * k + (.1 if side > 0 else 0), fx="pop"))
    els += [ln([[440, G], [440, G - 200], [1338, G - 200], [1338, G]], tw + .9, GOLD, 5, dur=1.2),
            dt(538, G - 236, 24, GOLD, tl - .3), ink(538, G - 226, "2", tl - .25, INK, 28, st="serif"),
            dt(1240, G - 236, 24, GOLD, tl - .3), ink(1240, G - 226, "2", tl - .25, INK, 28, st="serif"),
            lab(889, G - 290, "the giants: later", tl, GOLD, 34, st="serif")]
    return {"base": "section", "tod": "dusk", "ground": G, "lx": 1500, "layers": [{"d": 0, "c": "#4a3a2c", "t": ""}], "cam": CAM, "els": els}


@scene(16)
def s17(C):
    """s17: the quarry floor at dusk: a heap of stone chips; three potsherds glow; 'early Roman'."""
    G = 640
    rnd = random.Random(9)
    els = [poly([(-40, 400), (300, 380), (700, 410), (1100, 390), (1500, 404), (1820, 392), (1820, G), (-40, G)], "#5c4a37", "rgba(255,226,190,.25)", 1.5, -1)]
    heap = []
    for k in range(70):
        x, y = rnd.uniform(420, 1360), rnd.uniform(G + 8, G + 130)
        y = max(y, G + 8 + abs(x - 890) * .12)
        s_ = rnd.uniform(10, 24)
        heap.append(poly([(x - s_, y), (x - s_ * .3, y - s_ * .8), (x + s_ * .7, y - s_ * .5), (x + s_, y + s_ * .2)], "#b3a07c", "#6b5640", 1, .2 + .01 * k))
    els += [poly([(380, G + 160), (600, G + 40), (890, G + 6), (1180, G + 40), (1400, G + 160)], "#7a6248", at=.2, curve=True)] + heap
    tp, tr = C.at(16, "pottery"), C.at(16, "early Roman")
    for k, (x, y) in enumerate(((700, G + 60), (930, G + 40), (1130, G + 80))):
        els += [poly([(x - 26, y), (x - 4, y - 18), (x + 24, y - 10), (x + 18, y + 10), (x - 14, y + 12)], "#c8743c", "#ffd8a8", 1.5, tp + .4 * k, fx="pop"),
                gl(x, y, 70, tp + .4 * k, .8)]
    els += [lab(930, G - 70, "pottery", tp + .3, BONE, 30), lab(930, G - 120, "early Roman", tr, GOLD, 40, st="serif")]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [300, 330, 20], "cam": CAM, "els": els}


@scene(17)
def s18(C):
    """s18: the podium planned, in elevation (36 units a metre): course 1 (two blocks of about 9.5 x 3.9 m) and course 2 (a giant,
    19.6 x 4.35 m) built; course 3 drawn dashed with the 2014 block's outline (5.6 m high) 'never laid'; a dashed course 4 '?'."""
    S, G, x0 = 36, 740, 536
    w = 19.6 * S
    h1, h2, h3 = 3.9 * S, 4.35 * S, 5.6 * S
    t14, tp, t2 = C.at(17, "twenty fourteen"), C.at(17, "planned"), C.at(17, "Only two")
    els = [ln([[80, G], [1700, G]], -1, "#8c7152", 3, draw=False),
           rect(x0, G - h1, 9.8 * S - 3, h1, "#c8b692", "#2a2219", 2, 3, .3), rect(x0 + 9.8 * S, G - h1, 9.8 * S - 3, h1, "#c8b692", "#2a2219", 2, 3, .4),
           rect(x0, G - h1 - h2, w - 3, h2, "#e0cfa8", "#2a2219", 2, 3, .6),
           pe(x0 + w + 40, G, 1.7 * S, .8, "#e8d6b8")]
    y3 = G - h1 - h2 - h3
    els += [rect(x0, y3, w - 3, h3, "rgba(159,208,255,.10)", BLUE, 3, 3, t14, style="inferred"),
            lab(x0 + w / 2, y3 + h3 / 2 + 12, "2014 block: never laid", t14 + .5, BLUE, 30),
            rect(x0, y3 - 70, w - 3, 66, "none", LILAC, 2.5, 3, tp + .3, style="claimed"), lab(x0 + w / 2, y3 - 26, "?", tp + .6, LILAC, 40, st="big")]
    for k, (yc, t, c, s_) in enumerate(((G - h1 / 2, .4, GOLD, "1"), (G - h1 - h2 / 2, .7, GOLD, "2"), (y3 + h3 / 2, t14 + .3, BLUE, "3"), (y3 - 35, tp + .6, LILAC, "4"))):
        els += [dt(x0 - 50, yc, 22, c, t), ink(x0 - 50, yc + 10, s_, t + .05, INK, 26, st="serif")]
    els += [lab(x0 + w + 110, y3 + 30, "planned:", tp, LILAC, 30, "start"), lab(x0 + w + 110, y3 + 70, "3 or 4 courses", tp + .2, LILAC, 30, "start"),
            lab(x0 + w + 110, G - h1 - 30, "built: 2", t2, GOLD, 34, "start", st="serif"),
            ln([[x0 + w + 96, G - 6], [x0 + w + 96, G - h1 - h2 + 4]], t2, GOLD, 4, dur=.5)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


@scene(18)
def s19(C):
    """s19: a shelf of building records: two scrolls drawn solid, the rest dotted outlines: 'lost'; then the empty space glows."""
    els = [ln([[260, 380], [1520, 380]], .2, "#8c7152", 8, dur=.5), ln([[260, 620], [1520, 620]], .3, "#8c7152", 8, dur=.5),
           ln([[270, 380], [270, 640]], .2, "#6b4a2e", 8, draw=False), ln([[1510, 380], [1510, 640]], .2, "#6b4a2e", 8, draw=False)]
    tl, te = C.at(18, "simply lost"), C.at(18, "empty shelf")
    keep = {(0, 3), (1, 9)}
    for r_ in range(2):
        for j in range(12):
            x, y = 300 + 100 * j, 380 - 110 + 240 * r_
            if (r_, j) in keep:
                els += [rect(x, y, 70, 104, "#e8dcc2", "#8a7a66", 2, 10, .6 + .1 * r_), ln([[x + 14, y + 30], [x + 56, y + 30]], .7, INK, 2, draw=False), ln([[x + 14, y + 52], [x + 50, y + 52]], .7, INK, 2, draw=False)]
            else:
                els.append(rect(x, y, 70, 104, "none", LILAC, 2.5, 10, tl - .6 + .03 * (j + 12 * r_), style="claimed"))
    els += [lab(889, 740, "lost", tl + .4, LILAC, 40, st="serif"), gl(889, 500, 420, te, .25, "blue")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(19)
def s20(C):
    """s20: the Stone of the Pregnant Woman lying tilted in the quarry (about 20.5 m long, 34 units a metre); cracks draw along one end
    and dark karst hollows open in it; a dashed road towards the temple breaks."""
    G = 700
    L, Hh, ang = 20.5 * 34, 4.3 * 34, math.radians(-11)
    px, py = 260, G + 40
    ca, sa = math.cos(ang), math.sin(ang)
    P_ = lambda u, v: (px + u * ca + v * sa, py + u * sa - v * ca)
    corners = [P_(0, 0), P_(L, 0), P_(L, Hh), P_(0, Hh)]
    tn, tc, tr = C.at(19, "Pregnant Woman"), C.at(19, "hollows and cracks"), C.at(19, "broken on the road")
    els = [poly(corners, "#d8c49c", "#2a2219", 2.5, .3),
           poly([P_(0, Hh), P_(L, Hh), P_(L + 40, Hh + 30), P_(40, Hh + 30)], "#eed9b3", "#2a2219", 2, .3),
           rect(-40, G, 1860, 320, "#3a2e23", r=0, at=-1),
           lab(*P_(L / 2, Hh + 150), "Stone of the Pregnant Woman", tn, GOLD, 32, st="serif")]
    cracks = [[(30, 0), (48, 40), (40, 80), (62, 118), (56, Hh)], [(92, 0), (100, 30), (122, 52)], [(150, Hh), (136, 110), (150, 84)]]
    els += [ln([P_(u, v) for u, v in c], tc + .25 * k, "#2a1d12", 4 - k, dur=.5) for k, c in enumerate(cracks)]
    for k, (u, v, s_) in enumerate(((150, 14, 30), (230, 22, 22), (300, 10, 18))):
        pts = [P_(u + s_ * math.cos(a_) * (1 + .3 * math.sin(3 * a_)), v + s_ * .32 * math.sin(a_)) for a_ in [q * math.pi / 6 for q in range(12)]]
        els.append(poly(pts, "#1a120c", "#5a4632", 1.5, tc + .5 + .2 * k, fx="pop"))
    x, y = P_(70, Hh + 30)
    els += [gl(*P_(70, 70), 150, tc + .3, .4, "red"), lab(x - 20, y - 100, "cracks and hollows", tc + .6, RED, 28, "start")]
    rd = [(1010, G - 14), (1200, G - 30), (1380, G - 26), (1540, G - 40)]
    els += [ln(rd, tr - .8, BONE, 3, "inferred", 1.0, curve=True),
            ln([[1270, G - 66], [1290, G - 46], [1270, G - 26], [1290, G - 6]], tr, RED, 5, dur=.4),
            poly([(1540, G - 120), (1600, G - 150), (1660, G - 120)], "none", AMBER, 2.5, tr - .8), ln([[1540, G - 112], [1660, G - 112]], tr - .8, AMBER, 3, draw=False)] + \
           [ln([[1550 + 22 * k, G - 108], [1550 + 22 * k, G - 60]], tr - .8, AMBER, 4, draw=False) for k in range(6)] + \
           [lab(1600, G - 180, "the temple", tr - .6, AMBER, 26)]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1450, 380, 22], "cam": CAM, "els": els}


# ================================================================ chapter 2: How to move 1,000 tonnes
@scene(20)
def s21(C):
    """s21: a block on bare ground, a line of people pushing; at the contact, red friction marks flicker; 'friction'."""
    G = 660
    tf = C.at(20, "friction")
    els = [block3d(560, G, 640, 230, 220, .3)]
    els += [pe(300 + 46 * k, G, 92, .6 + .1 * k) for k in range(5)]
    els += [arr([[520, G - 60], [560, G - 60]], .9, AMBER, 4, dur=.4, curve=False)]
    for k in range(9):
        x = 590 + 70 * k
        els += [ln([[x, G + 6], [x - 26, G + 22]], tf + .12 * k, RED, 4, dur=.2), ln([[x + 14, G + 4], [x - 4, G + 26]], tf + .12 * k + .5, RED, 3, dur=.2)]
    els += [gl(880, G + 10, 300, tf, .4, "red"), lab(880, G + 110, "friction", tf + .3, RED, 36, st="serif"),
            lab(880, 250, "the weight?", .8, DIM, 30)]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1500, 420, 22], "cam": CAM, "els": els}


def fridge(x, y, at, w=120, h=250):
    return [rect(x, y - h, w, h, "#e8ecef", "#9aa4ab", 2, 10, at), ln([[x + 6, y - h * .62], [x + w - 6, y - h * .62]], at, "#9aa4ab", 2, draw=False),
            ln([[x + w - 18, y - h * .9], [x + w - 18, y - h * .7]], at, "#6a747b", 4, draw=False), ln([[x + w - 18, y - h * .52], [x + w - 18, y - h * .3]], at, "#6a747b", 4, draw=False)]


@scene(21)
def s22(C):
    """s22: left, a person shoves a fridge across a carpet that rucks up (red marks); right, the same fridge rolls on a trolley (gold arrow)."""
    G = 680
    tt = C.at(21, "trolley")
    els = [rect(110, G - 6, 700, 14, "#7a3d3a", r=4, at=.2), poly([(620, G - 4), (660, G - 30), (700, G - 4)], "#7a3d3a", at=.6, curve=True)] + fridge(500, G - 6, .4) + \
          [pe(450, G - 6, 150, .6), arr([[460, G - 110], [496, G - 110]], .8, AMBER, 4, dur=.3, curve=False)] + \
          [ln([[520 + 24 * k, G + 12], [508 + 24 * k, G + 26]], 1.0 + .1 * k, RED, 4, dur=.2) for k in range(5)] + \
          [lab(460, G + 70, "carpet", .8, DIM, 30)]
    els += [rect(1150, G - 34, 200, 18, "#5a5f64", "#9aa4ab", 2, 4, tt - .3), dt(1170, G - 10, 14, "#2a2a2a", tt - .3), dt(1330, G - 10, 14, "#2a2a2a", tt - .3),
            ln([[1350, G - 30], [1380, G - 200]], tt - .3, "#9aa4ab", 5, draw=False)] + fridge(1190, G - 34, tt - .2) + \
           [pe(1440, G, 150, tt), arr([[1130, G - 150], [980, G - 150]], tt - .1, GOLD, 5, dur=.5, curve=False), lab(1250, G + 70, "trolley", tt + .2, GOLD, 30)]
    return {"base": "dark", "stars": 20, "floor": G, "cam": CAM, "els": [ln([[80, G], [1700, G]], -1, "#8c7152", 3, draw=False)] + els}


@scene(22)
def s23(C):
    """s23: the block on a timber sledge, on a track of cross-timbers; a rope runs ahead; a long gold arrow: it glides."""
    G = 680
    els = [rect(80 + 64 * k, G - 6, 44, 16, "#6b4a2e", "#c9a070", 1.5, 2, .2 + .02 * k) for k in range(26)]
    els += [poly([(380, G - 10), (1060, G - 10), (1110, G - 40), (1080, G - 44), (1050, G - 30), (380, G - 30)], "#8c6a48", "#c9a070", 2, .6),
            block3d(420, G - 30, 600, 210, 200, .8)]
    els += [pe(1380 + 44 * k, G, 84, 1.3 + .1 * k) for k in range(6)]
    els += [ln([[1100, G - 40], [1640, G - 60]], 1.2, "#e8d6b8", 3, dur=.8),
            arr([[460, 300], [1300, 300]], 1.6, GOLD, 6, dur=1.0, curve=False), lab(880, 270, "sledge + track", 1.8, GOLD, 32, st="serif")]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1500, 440, 22], "cam": CAM, "els": els}


PLASTER, OCHRE, INKP = "#d9c29a", "#a8662e", "#2a1d14"


@scene(23)
def s24(C):
    """s24: the tomb painting of Djehutihotep (about 1880 BCE), drawn in ochre and black on plaster: a seated colossus on a sledge,
    four rows of pullers (172 figures) along the ropes, a man at the front pouring water; '60 t', '172 men', 'water', 'ritual?', '?'."""
    th, tf, tr, tq = C.at(23, "hauled by"), C.at(23, "And at the front"), C.at(23, "ritual"), C.at(23, "does it help")
    tc = C.at(23, "colossal statue")
    els = [rect(100, 150, 1580, 630, PLASTER, "#8a6a48", 3, 6, .2), rect(100, 150, 1580, 630, "url(#k-speck)", r=6, at=.2, op=.5)]
    # the colossus, seated, facing right, on its sledge (schematic)
    sx, sy = 170, 700
    statue = [(sx + 40, sy - 30), (sx + 40, sy - 300), (sx + 60, sy - 360), (sx + 110, sy - 380), (sx + 150, sy - 372), (sx + 165, sy - 340), (sx + 160, sy - 300),
              (sx + 140, sy - 285), (sx + 150, sy - 240), (sx + 270, sy - 236), (sx + 290, sy - 210), (sx + 290, sy - 120), (sx + 300, sy - 30)]
    els += [poly(statue, "#c8b28a", INKP, 3, tc), rect(sx, sy - 34, 360, 28, OCHRE, INKP, 2.5, 4, tc - .2),
            ink(sx + 150, sy - 110, "60 t", tc + .6, INKP, 36, st="serif")]
    rows = [330, 430, 530, 630]
    for r_, y in enumerate(rows):
        els.append(ln([[sx + 360, sy - 20], [620, y - 26], [1660, y - 26]], th - .3, INKP, 2, draw=False, op=.8))
        for k in range(43):
            x = 640 + 23 * k
            els.append(pe(x, y, 56, round(th + .02 * k + .25 * r_, 2), INKP, fx="pop"))
    els += [ink(1150, 250, "172 men", th + 1.4, INKP, 34, st="serif")]
    px_ = sx + 330
    els += [pe(px_, sy - 34, 70, tf, INKP), poly([(px_ + 10, sy - 70), (px_ + 30, sy - 64), (px_ + 26, sy - 50), (px_ + 12, sy - 54)], OCHRE, INKP, 1.5, tf),
            lab(px_ + 60, sy + 56, "water", tf + .6, "#1f5a7f", 32, "start", halo=False)]
    els += [dt(px_ + 34 + 8 * k, sy - 46 + 14 * k, 4.5, "#2f76a0", tf + .3 + .08 * k) for k in range(6)]
    els += [lab(px_ - 20, sy - 120, "ritual?", tr, "#5a3f9e", 32, "end", halo=False), lab(px_ + 130, sy - 4, "?", tq, "#9a5a1a", 70, st="big", halo=False)]
    return {"base": "dark", "stars": 10, "cam": CAM, "els": els}


@scene(24)
def s25(C):
    """s25: a lab tray of sand and a model sledge, dry and wet: on dry sand a berm piles up in front and the pull arrow is long; on wet
    sand no berm and the arrow is about half as long. Then the beach: a deep footprint in dry sand, a shallow one on wet."""
    tw, th, tb = C.at(24, "right amount of water"), C.at(24, "about half"), C.at(24, "Like walking")
    els = []
    for k, (x0, sand, name, t) in enumerate(((140, "#d8c08a", "dry", .4), (930, "#9c8460", "wet", tw))):
        els += [rect(x0, 300, 700, 170, "#4a3a2c", "#8c7152", 2, 8, t), rect(x0 + 10, 360, 680, 100, sand, r=4, at=t),
                lab(x0 + 350, 270, name, t + .2, BONE if k == 0 else BLUE, 32, st="serif"),
                rect(x0 + 120, 318, 120, 42, "#8c6a48", "#c9a070", 2, 4, t + .3)]
        if k == 0:
            els += [poly([(x0 + 240, 360), (x0 + 262, 336), (x0 + 290, 360)], sand, "#8c7152", 1.5, t + .6, curve=True),
                    arr([[x0 + 240, 340], [x0 + 600, 340]], 1.4, AMBER, 5, dur=.8, curve=False)]
        else:
            els += [dt(x0 + 200 + 40 * j, 380 + 18 * (j % 3), 4, "#9fd0ff", t + .4 + .05 * j) for j in range(10)] + \
                   [arr([[x0 + 240, 340], [x0 + 420, 340]], th - .3, GOLD, 5, dur=.5, curve=False)]
    els += [lab(1335, 520, "about half the pull", th, GOLD, 32, st="serif"), lab(500, 520, "pull", 1.6, AMBER, 28)]
    foot = lambda x, y: [(x + 1.8 * u, y + 1.8 * v) for u, v in [(0, -40), (22, -36), (30, -10), (26, 30), (10, 44), (-8, 34), (-12, 0), (-10, -30)]]
    els += [rect(140, 600, 700, 170, "#d8c08a", r=10, at=tb - .3), rect(930, 600, 700, 170, "#9c8460", r=10, at=tb - .3),
            poly(foot(490, 690), "#3a2c20", "#8c7152", 6, tb, fx="pop"), poly(foot(1280, 690), "rgba(60,48,36,.3)", "#6b5640", 2, tb + .4, fx="pop"),
            lab(600, 700, "deep", tb + .2, INK, 30, "start", halo=False), lab(1390, 700, "shallow", tb + .6, "#dbe9f3", 30, "start")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


MOAI = [(-75, 0), (75, 0), (68, -230), (58, -240), (62, -300), (72, -305), (74, -420), (62, -425), (60, -470), (-60, -470), (-62, -425), (-74, -420),
        (-72, -305), (-62, -300), (-58, -240), (-68, -230)]


def moai(cx, by, at, op=None, s=1.0, rot=0, piv=None, face=True):
    """An Easter Island statue seen from the front (schematic): long head, heavy brow, long nose, arms along the body."""
    P = lambda u, v: (cx + u * s, by + v * s)
    body = [poly([P(u, v) for u, v in MOAI], "#6a645c", "#cbbca8", 2, at)]
    if face:
        body += [ln([P(-50, -400), P(50, -400)], at, "#3a352f", 8, draw=False), poly([P(-44, -392), P(-12, -392), P(-14, -372), P(-42, -375)], "#2a2622", at=at),
                 poly([P(44, -392), P(12, -392), P(14, -372), P(42, -375)], "#2a2622", at=at), poly([P(0, -396), P(-16, -318), P(16, -318)], "#57514a", "#3a352f", 1.5, at),
                 ln([P(-30, -290), P(30, -290)], at, "#3a352f", 5, draw=False), ln([P(-56, -200), P(-50, -90), P(-10, -70)], at, "#3a352f", 4, draw=False, curve=True),
                 ln([P(56, -200), P(50, -90), P(10, -70)], at, "#3a352f", 4, draw=False, curve=True)]
    if rot:
        px, py = piv
        g = group(body, "rotate(%s %s %s)" % (rot, r1(px), r1(py)), at, fx="fade")
        if op is not None:
            g.update(op=op, keepop=True)
        return [g]
    return body


@scene(25)
def s26(C):
    """s26: a replica Easter Island statue (4.35 t) 'walked' upright: it rocks onto one corner, then the other (two ghost positions), ropes
    to three teams (18 people); a 100 m path; '40 min'."""
    G = 700
    tr, tw = C.at(25, "rocked"), C.at(25, "walked it")
    cx = 700
    els = [ln([[80, G], [1700, G]], -1, "#8c7152", 3, draw=False)]
    els += moai(cx, G, tr, op=.3, rot=-8, piv=(cx - 75, G)) + moai(cx, G, tr + .6, op=.3, rot=8, piv=(cx + 75, G)) + moai(cx, G, .5)
    head = (cx, G - 440)
    teams = [(cx - 360, -1, G), (cx + 360, 1, G), (cx + 120, 1, G + 60)]
    for k, (tx, side, y) in enumerate(teams):
        for j in range(6):
            els.append(pe(tx + side * 30 * j, y, 72, tr + .3 + .1 * j + .3 * k))
        els.append(ln([head, [tx, y - 52]], tr + .2 + .3 * k, "#c9a070", 2.5, dur=.6))
    els += [lab(cx, G - 500, "4.35 t replica", .8, BONE, 30), lab(cx - 440, G + 60, "18 people", tr + 1.0, AMBER, 30)]
    els += [ln([[1100, G + 110], [1640, G + 110]], tw, GOLD, 4, "inferred", 1.0), arr([[1500, G - 300], [1660, G - 300]], tw, GOLD, 5, dur=.5, curve=False),
            lab(1500, G - 330, "100 m in 40 min", tw + .6, GOLD, 32, st="serif")]
    return {"base": "sky", "tod": "day", "ground": G, "sun": [1450, 230, 26], "cam": CAM, "els": els}


@scene(26)
def s27(C):
    """s27: a capstan: an upright wooden drum with four bars; four people push the bars and walk in a circle; the rope winds onto the drum
    and runs off to a block."""
    cx, cy = 640, 420
    tb, tw, tr = C.at(26, "push its bars"), C.at(26, "walk in a circle"), C.at(26, "rope winds")
    spoke = [.4 + k * math.pi / 2 for k in range(4)]
    els = [rect(cx - 36, cy, 72, 300, "#8c6a48", "#c9a070", 2, 6, .4), oval(cx, cy, 36, 14, "#a8865e", "#c9a070", 2, 1, .4),
           oval(cx, cy + 300, 36, 14, "#6b4a2e", at=.4), ln([[cx - 400, cy + 300], [cx + 900, cy + 300]], -1, "#8c7152", 3, draw=False)]
    for k, a in enumerate(spoke):
        ex, ey = cx + 230 * math.cos(a), cy + 90 * math.sin(a) + 30
        els += [ln([[cx, cy + 30], [ex, ey]], tb - .5 + .1 * k, "#c9a070", 7, dur=.4), pe(ex, ey + 90, 110, tb + .1 * k)]
    els += [{"k": "arrow", "p": R([[cx + 300 * math.cos(a), cy + 30 + 120 * math.sin(a)] for a in [k * .28 for k in range(20)]]), "c": AMBER, "w": 4, "style": "inferred",
             "curve": True, "fx": "draw", "dur": 1.2, "in": tw},
            lab(cx, cy - 120, "capstan", .6, GOLD, 34, st="serif")]
    els += [ln([[cx + 30, cy + 240 - 10 * k], [cx - 30, cy + 250 - 10 * k]], tr + .1 * k, "#e8d6b8", 3, draw=False) for k in range(6)]
    els += [ln([[cx + 36, cy + 250], [1260, cy + 250]], tr + .3, "#e8d6b8", 3, dur=.6), block3d(1260, cy + 300, 340, 140, 120, .5),
            arr([[1250, cy + 200], [1100, cy + 200]], tr + .8, GOLD, 4, dur=.5, curve=False), lab(1430, cy + 30, "the rope winds in", tr + .6, BONE, 28)]
    return {"base": "dark", "stars": 20, "floor": cy + 300, "cam": CAM, "els": els}


@scene(27)
def s28(C):
    """s28: Jean-Pierre Adam's sums for Baalbek, in plan: the block (800 t) on a timber track; six capstans ahead, 24 people around each
    (144); ropes back to the block; '6 capstans', '144 people', '800 t'."""
    t6, t144, t1 = C.at(27, "Six capstans"), C.at(27, "forty-four"), C.at(27, "One eight-hundred-tonne")
    els = [rect(100, 520, 1580, 120, "#4a3a2c", r=6, at=.2)] + [ln([[130 + 50 * k, 524], [130 + 50 * k, 636]], .3, "#6b4a2e", 6, draw=False) for k in range(31)]
    els += [rect(140, 530, 460, 100, "#e0cfa8", "#2a2219", 2.5, 4, .5)]
    els += [lab(120, 190, "Jean-Pierre Adam, 1977", .4, DIM, 28, "start")]
    caps = [760 + 156 * k for k in range(6)]
    for k, x in enumerate(caps):
        at = t6 + .15 * k
        els += [dt(x, 330, 22, "#8c6a48", at), rg(x, 330, 22, at, "#c9a070", 3, dur=.3),
                ln([[x, 352], [600, 580]], at + .3, "#e8d6b8", 2, dur=.6)]
        for j in range(24):
            a_ = 2 * math.pi * j / 24
            els.append(dt(x + 56 * math.cos(a_), 330 + 56 * math.sin(a_), 6, "#e8d6b8", t144 - .6 + .006 * (24 * k + j)))
    els += [lab(1150, 250, "6 capstans", t6 + .4, GOLD, 30), lab(1150, 440, "144 people", t144, AMBER, 32, st="serif"),
            ink(370, 594, "800 t", t1, INK, 40, st="serif"), gl(370, 580, 220, t1, .4)]
    return {"base": "plan", "cam": CAM, "els": els}


def boulder(cx, base, w, h):
    """The Thunder Stone, a rounded granite boulder, as a soft polygon."""
    return [(cx - w * .5, base), (cx - w * .52, base - h * .45), (cx - w * .4, base - h * .85), (cx - w * .15, base - h), (cx + w * .2, base - h * .96),
            (cx + w * .45, base - h * .7), (cx + w * .52, base - h * .3), (cx + w * .46, base)]


@scene(28)
def s29(C):
    """s29: winter, 1770: the Thunder Stone on a timber sledge running on a track; two capstans ahead and a crowd of tiny figures ('about
    400 people'); a gold route '6 km'. A magnifier opens on the track: grooved rails, bronze balls between sledge and track."""
    G = 640
    tb, tp, tk = C.at(28, "bronze balls"), C.at(28, "four hundred people"), C.at(28, "six kilometres")
    els = [rect(-40, G, 1860, 400, "#6f7884", r=0, at=-1), rect(-40, G, 1860, 400, "url(#k-speck)", r=0, at=-1, op=.6),
           rect(-40, G, 1860, 60, "#8a94a0", r=0, at=-1, op=.6),
           rect(120, G - 8, 1500, 16, "#6b4a2e", "#c9a070", 1.5, 3, .2),
           rect(260, G - 40, 560, 32, "#8c6a48", "#c9a070", 2, 4, .4),
           poly(boulder(540, G - 40, 520, 300), GRAN, "#e8e2d6", 2, .6, curve=True),
           poly([(640, G - 330), (760, G - 280), (800, G - 160), (780, G - 44), (700, G - 44), (720, G - 170), (690, G - 280)], "rgba(40,36,34,.35)", at=.6, curve=True),
           ln([[420, G - 300], [440, G - 230], [420, G - 170]], .6, "#6f6a64", 2, draw=False), ln([[560, G - 320], [590, G - 250]], .6, "#6f6a64", 2, draw=False),
           ln([[330, G - 140], [380, G - 120], [400, G - 80]], .6, "#6f6a64", 2, draw=False),
           lab(200, 200, "1770", .8, GOLD, 40, st="serif")]
    for k, x in enumerate((1050, 1300)):
        els += [rect(x - 18, G - 120, 36, 112, "#6b4a2e", "#c9a070", 1.5, 4, tp - .4), ln([[x - 90, G - 110], [x + 90, G - 110]], tp - .3, "#c9a070", 5, draw=False),
                ln([[x, G - 60], [810, G - 30]], tp - .2, "#e8d6b8", 2, dur=.6)]
    rnd = random.Random(12)
    for k in range(70):
        x = rnd.uniform(860, 1560)
        y = G + rnd.uniform(-2, 60)
        els.append(pe(x, y, rnd.uniform(26, 34), tp + .015 * k, "#2a2229", fx="pop"))
    els += [lab(1220, G + 120, "about 400 people", tp + .6, BONE, 30),
            ln([[140, G + 90], [800, G + 90]], tk, GOLD, 4, "inferred", 1.0), lab(470, G + 140, "6 km over land", tk + .5, GOLD, 30)]
    mx, my, mr = 1350, 300, 150
    inner = [rect(mx - 160, my - 70, 320, 40, "#8c6a48", "#c9a070", 2, 2, -1), rect(mx - 160, my + 30, 320, 40, "#6b4a2e", "#c9a070", 2, 2, -1)] + \
            [ln([[mx - 160, my - 30], [mx + 160, my - 30]], -1, "#2a1d12", 3, draw=False), ln([[mx - 160, my + 30], [mx + 160, my + 30]], -1, "#2a1d12", 3, draw=False)] + \
            [{"k": "circle", "x": mx - 120 + 60 * j, "y": my, "r": 28, "fill": BRZ, "c": "#ffd8a8", "w": 2, "in": -1} for j in range(5)]
    els += [{"k": "circle", "x": mx, "y": my, "r": mr + 8, "fill": "#1a1511", "c": "#c9a070", "w": 4, "in": tb - .4, "fx": "pop"},
            group(inner, "", tb - .2, clip=[mx - mr, my - mr, 2 * mr, 2 * mr, mr]),
            ln([[mx - 106, my + 106], [690, G - 46]], tb - .2, "#c9a070", 2, "inferred", .5),
            lab(mx, my + mr + 46, "bronze balls", tb + .3, GOLD, 30)]
    return {"base": "sky", "tod": "dusk", "ground": G, "groundc": "#6f7884", "sun": [1600, 470, 18], "cam": CAM, "els": els}


HORSE = [(0, 0), (-8, -30), (-16, -70), (-20, -110), (10, -140), (70, -185), (120, -230), (150, -270), (175, -300), (195, -305), (200, -292), (235, -268),
         (240, -252), (222, -246), (195, -258), (178, -232), (186, -212), (220, -205), (238, -180), (226, -150), (214, -152), (220, -178), (196, -188), (170, -180),
         (150, -160), (110, -140), (70, -125), (45, -100), (40, -60), (34, -20), (36, 0)]
RIDER = [(60, -190), (75, -260), (95, -276), (160, -300), (163, -290), (102, -262), (104, -205), (112, -170), (98, -160), (84, -184)]
TAIL = [(-18, -112), (-40, -80), (-48, -30), (-36, -36), (-28, -80)]


@scene(29)
def s30(C):
    """s30: the boulder today, the pedestal of a bronze horseman in Saint Petersburg (a rearing horse and rider in silhouette); a
    balance: the boulder (more than 1,000 t) outweighs a Baalbek giant (800 to 1,000 t); then three icons: people, rope, patience."""
    G = 700
    th, tw, tn = C.at(29, "bronze horseman"), C.at(29, "outweighed"), C.at(29, "No lost technology")
    tp, tr, tpa = C.at(29, "Just people"), C.at(29, "rope"), C.at(29, "patience")
    els = [poly(boulder(380, G, 420, 220), GRAN, "#e8e2d6", 2, .3, curve=True)]
    hx, hy, k_ = 290, G - 214, .9
    H_ = lambda pts: [(hx + k_ * x, hy + k_ * y) for x, y in pts]
    els += [poly(H_(TAIL), "#3d4a3a", "#8fa08a", 1.5, th, fx="rise"), poly(H_(HORSE), "#3d4a3a", "#8fa08a", 2, th, fx="rise"),
            poly(H_(RIDER), "#34402f", "#8fa08a", 1.5, th + .2, fx="rise"), dt(hx + k_ * 92, hy - k_ * 290, 10, "#34402f", th + .2),
            gl(hx + 100, hy - 160, 200, th, .3, "lamp"), lab(380, G + 60, "Saint Petersburg", th + .4, DIM, 28)]
    px, py = 1180, 260
    a = math.radians(9)
    L = 300
    lp = (px - L * math.cos(a), py + L * math.sin(a))
    rp = (px + L * math.cos(a), py - L * math.sin(a))
    els += [ln([[px, py], [px, G]], tw - .4, "#8c7152", 6, draw=False), poly([(px - 60, G), (px, G - 40), (px + 60, G)], "#6b5640", at=tw - .4),
            ln([lp, rp], tw - .2, "#c9a070", 6, dur=.5), dt(px, py, 10, "#c9a070", tw - .2)]
    for (x, y), k in ((lp, 0), (rp, 1)):
        els += [ln([[x, y], [x - 70, y + 120]], tw, "#c9a070", 2, draw=False), ln([[x, y], [x + 70, y + 120]], tw, "#c9a070", 2, draw=False),
                ln([[x - 90, y + 120], [x + 90, y + 120]], tw, "#c9a070", 5, draw=False)]
    els += [poly(boulder(lp[0], lp[1] + 118, 150, 90), GRAN, "#e8e2d6", 2, tw + .2, curve=True), lab(lp[0], lp[1] + 170, "over 1,000 t", tw + .4, BONE, 28),
            rect(rp[0] - 80, rp[1] + 82, 160, 36, "#e0cfa8", "#2a2219", 2, 3, tw + .3), lab(rp[0], rp[1] + 170, "800 to 1,000 t", tw + .5, GOLD, 28),
            lab(rp[0], rp[1] + 206, "a Baalbek giant", tw + .6, DIM, 24)]
    icons = [(900, tp, "people"), (1180, tr, "rope"), (1460, tpa, "patience")]
    els += [pe(900, 780, 70, tp, "#e8d6b8"), rg(1180, 740, 30, tr, AMBER, 6, dur=.5), rg(1180, 740, 16, tr + .2, AMBER, 4, dur=.4),
            rg(1460, 740, 32, tpa, BONE, 4, dur=.5), ln([[1460, 740], [1460, 718]], tpa + .3, BONE, 4, draw=False), ln([[1460, 740], [1478, 750]], tpa + .3, BONE, 4, draw=False)]
    els += [lab(x + 52, 752, t_, t + .2, AMBER if t_ != "people" else BONE, 28, "start") for x, t, t_ in icons]
    els += [lab(1180, 640, "no lost technology", tn, GOLD, 32, st="serif")]
    return {"base": "dark", "stars": 40, "floor": G, "cam": CAM, "els": els}


@scene(30)
def s31(C):
    """s31: what we don't know: one giant hovers in a dashed outline above its course, a lilac '?'; a dashed earth ramp up to the course;
    a lever under the block; a blank sheet: 'instructions?'."""
    G = 720
    S = 26
    tr, tl, ti = C.at(30, "raised onto"), C.at(30, "Ramps and levers"), C.at(30, "instructions")
    els = [ln([[80, G], [1700, G]], -1, "#8c7152", 3, draw=False)]
    els += [rect(330 + k * 9.55 * S, G - 3.9 * S, 9.55 * S - 3, 3.9 * S, "#c8b692", "#2a2219", 2, 3, .3) for k in range(4)]
    top = G - 3.9 * S
    els += [rect(360, top - 4.35 * S - 60, 19.1 * S, 4.35 * S, "rgba(224,207,168,.15)", LIME_E, 3, 3, tr - .3, style="inferred"),
            arr([[608, top - 50], [608, top - 6]], tr + .2, LILAC, 3, "claimed", .5, False)] + qm(608, top - 200, tr + .4, 90)
    els += [poly([(330 + 4 * 9.55 * S, top), (1640, G), (330 + 4 * 9.55 * S, G)], "rgba(122,98,72,.35)", "#c9a070", 2.5, tl, style="inferred"),
            lab(1380, top - 20, "ramp?", tl + .3, AMBER, 30)]
    els += [ln([[260, top - 70], [470, top - 120]], tl + .6, "#c9a070", 7, dur=.4), poly([(300, top), (320, top - 70), (340, top)], "#6b5640", at=tl + .6),
            pe(240, top, 70, tl + .8), lab(230, top - 160, "lever?", tl + 1.0, AMBER, 30)]
    els += [rect(1180, 170, 260, 160, "#e8dcc2", "#8a7a66", 2, 8, ti - .4), lab(1310, 270, "?", ti, LILAC, 70, st="big"), lab(1310, 370, "instructions?", ti + .3, LILAC, 30)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================ chapter 3: The kit at Puma Punku
HPROF = [[0, 0], [.34, 0], [.34, .36], [.86, .36], [.86, 0], [1.2, 0], [1.2, 1.0], [.86, 1.0], [.86, .64], [.34, .64], [.34, 1.0], [0, 1.0]]


@scene(31)
def s32(C):
    """s32: the H-blocks again, wider and turning (f06 puma-punku shot 0): the inside corners glow; an amber template outline traces over
    each block in turn: like pieces of a kit."""
    base = short_iso(f06.puma_punku, 0)
    base.update(x=889, y=600, s=128, az=-30, spin=.6, el=.4, **{"in": -1})
    tc, tk = C.at(31, "crisp inside"), C.at(31, "pieces of a kit")
    els = [gl(889, 540, 640, -1, .22, "lamp"), base]
    for i in range(4):
        x1 = -3.6 + 1.8 * i
        els.append(ov(base, [{"t": "glow", "x": x1 + u, "y": v, "z": .36, "r": 30, "kind": "lamp"} for u, v in ((.34, .36), (.86, .36), (.34, .64), (.86, .64))], tc + .15 * i))
        els.append(ov(base, [{"t": "line", "p": [[x1 + u, v, .38] for u, v in HPROF + HPROF[:1]], "c": AMBER, "w": 3, "style": "inferred"}], tk - .6 + .4 * i, fx="draw", dur=.5))
    x, y = P3(base, (0, 1.3, 0), tk)
    els += [lab(889, 230, "like pieces of a kit", tk + .6, AMBER, 32, st="serif")]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


@scene(32)
def s33(C):
    """s33: Puma Punku today, from above: andesite and sandstone blocks, broken and tilted, scattered over the platform like a tipped-out toy box."""
    rnd = random.Random(31)
    els = [poly([(140, 200), (1640, 170), (1690, 760), (90, 780)], "#6e604e", "rgba(255,226,190,.25)", 2, -1),
           rect(90, 170, 1600, 610, "url(#k-speck)", r=0, at=-1, op=.6)]
    k = 0
    while k < 46:
        x, y = rnd.uniform(200, 1580), rnd.uniform(240, 720)
        if abs(x - 889) < 160 and abs(y - 480) < 60:
            continue
        w, h = rnd.uniform(40, 120), rnd.uniform(30, 70)
        ang = rnd.uniform(-40, 40)
        red = rnd.random() < .25
        if rnd.random() < .3 and not red:
            s_ = rnd.uniform(46, 70)
            pts = [(x + s_ * u, y + s_ * v) for u, v in HPROF]
        else:
            pts = [(x, y), (x + w, y), (x + w, y + h), (x + w * .3, y + h * 1.05), (x, y + h * .7)]
        els.append(group([poly(pts, SAND_R if red else AND, "#e8e2d6" if not red else "#f2b08a", 1.5, -1)], "rotate(%d %d %d)" % (ang, r1(x), r1(y)), .3 + .04 * k, fx="pop"))
        k += 1
    els += [lab(889, 490, "broken and scattered", 1.4, BONE, 32, st="serif")]
    return {"base": "dark", "cam": CAM, "els": els}


@scene(33)
def s34(C):
    """s34: Lake Titicaca and its shores: Tiwanaku, Copacabana, La Paz; the andesite's route, about 90 km, across or around the lake
    (dashed); the red sandstone from about 10 km (a red ring)."""
    v = View(-70.7, -67.5, -16.95, -15.0, (90, 130, 1600, 660))
    tx, ty = v.p(-68.68, -16.56)
    t90, t10 = C.at(33, "ninety kilometres"), C.at(33, "red sandstone")
    els = [{"k": "map", "land": v.land(), "in": -1}] + \
          [poly([v.p(a, b) for a, b in poly_], "#1f4f6d", "#6fa7c9", 1.6, -1, curve=True) for poly_ in f06.TITICACA] + \
          [{"k": "pin", "x": tx, "y": ty, "t": "Tiwanaku", "c": GOLD, "in": .4}, gl(tx, ty, 90, .5, .5),
           lab(*v.p(-69.55, -15.75), "Lake Titicaca", .3, BLUE, 32, st="ital")]
    for name, lo, la, a in (("Copacabana", -69.09, -16.17, "end"), ("La Paz", -68.15, -16.50, "start")):
        px, py = v.p(lo, la)
        els += [dt(px, py, 7, DIM, .8), lab(px + (-16 if a == "end" else 16), py + 9, name, .8, DIM, 26, a)]
    route = [v.p(-69.09, -16.17), v.p(-68.95, -16.42), v.p(-68.72, -16.54)]
    els += [ln(route, t90 - .3, GOLD, 5, "inferred", 1.4, curve=True), lab(route[1][0] - 30, route[1][1] + 70, "andesite: about 90 km", t90 + .6, GOLD, 30, "end"),
            {"k": "circle", "x": tx, "y": ty, "r": r1(v.km(10)), "fill": "rgba(176,106,78,.18)", "c": SAND_R, "w": 3, "in": t10, "fx": "draw", "dur": .6},
            lab(tx + 20, ty + v.km(10) + 40, "sandstone: 10 km", t10 + .4, "#f2b08a", 28, "start"),
            {"k": "scale", "x": 140, "y": 760, "w": r1(v.km(50)), "t": "50 km", "in": .4}]
    return {"base": "map", "cam": CAM, "els": els}


@scene(34)
def s35(C):
    """s35: the largest red sandstone slab (f06 puma-punku shot 2), 7.8 x 5.2 x 1.1 m, beside a 1.7 m person; '131 t'."""
    base = short_iso(f06.puma_punku, 2)
    base.update(x=889, y=520, s=74, az=-26, spin=.3, el=.42, **{"in": -1})
    slab = next(it for it in base["items"] if it.get("t") == "box")
    t = C.at(34, "a hundred and thirty-one")
    els = [gl(889, 520, 600, -1, .22, "lamp"), base, ov(base, [hi(slab, GOLD, .2), rim(slab)], .6, fx="draw", dur=.8),
           ov(base, [{"t": "line", "p": [[-3.9, 1.1, 3.0], [3.9, 1.1, 3.0]], "c": BONE, "w": 3}, ilab(0, 1.1, 3.0, "7.8 m", BONE, 40, st="body"),
                     {"t": "line", "p": [[4.3, 1.1, -2.6], [4.3, 1.1, 2.6]], "c": BONE, "w": 3}, ilab(4.3, 1.1, 0, "5.2 m", BONE, 34, st="body", a="start")], 1.0, fx="draw", dur=.8)]
    x, y = P3(base, (0, 1.4, -1), t)
    els += [lab(x, y - 70, "131 t", t, GOLD, 56, st="serif"), gl(x, y - 60, 160, t, .4)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


@scene(35)
def s36(C):
    """s36: dawn on the horizon: a wall aimed at a sunrise; long ago the sun rose on the sight line (lilac); the sky drifts; today it
    rises beside it (gold); the angle between the two lines: 'mismatch'."""
    G = 620
    tm, tdr, tt = C.at(35, "measured where"), C.at(35, "slowly drifts"), C.at(35, "no longer lines up")
    wx, wy = 300, G + 80
    els = [rect(-40, G, 1860, 400, "#3a2e23", r=0, at=-1),
           block3d(180, wy, 260, 70, 60, .4), pe(150, wy, 90, .7),
           ln([[wx + 140, wy - 70], [1000, G]], tm, AMBER, 4, dur=.8), lab(250, wy + 50, "the wall", tm + .3, BONE, 28),
           oval(1000, G, 36, 36, "#c9c1ee", at=tm + 1.2, op=.8), gl(1000, G - 10, 110, tm + 1.2, .55), lab(1000, G - 70, "long ago", tm + 1.4, LILAC, 30),
           {"k": "arrow", "p": R([[1030, G - 130], [1130, G - 160], [1230, G - 130]]), "c": BONE, "w": 3, "curve": True, "fx": "draw", "dur": 1.0, "in": tdr, "style": "inferred"},
           lab(1130, G - 190, "the sky drifts", tdr + .4, BONE, 30),
           oval(1260, G, 40, 40, "#ffd9a0", at=tt), gl(1260, G - 10, 160, tt, .75, "sun"), lab(1260, G - 70, "today", tt + .2, GOLD, 30),
           ln([[wx + 140, wy - 70], [1260, G]], tt + .4, GOLD, 3, "inferred", .8)]
    els += [{"k": "line", "p": R([[wx + 140 + 230 * math.cos(math.radians(a)), wy - 70 - 230 * math.sin(math.radians(a))] for a in (4.2, 5.0, 5.8, 6.6, 7.4, 8.4)]),
             "c": AMBER, "w": 5, "fx": "draw", "dur": .4, "in": tt + 1.0}, lab(wx + 390, wy - 120, "mismatch", tt + 1.2, AMBER, 30, "start")]
    return {"base": "sky", "tod": "dawn", "ground": G, "sun": False, "cam": CAM, "els": els}


def TLX(yr, x0=180, x1=1600):
    return r1(x0 + (yr + 16000) / 18000 * (x1 - x0))


def timeline_15k(y=520, at=-1, x0=180, x1=1600):
    ticks = [[TLX(v, x0, x1), t] for v, t in ((-15000, "15,000 BCE"), (-10000, "10,000"), (-5000, "5000"), (1, "1 CE"))]
    return [{"k": "axis", "x0": x0, "x1": x1, "y": y, "ticks": ticks, "t": "", "in": at}]


@scene(36)
def s37(C):
    """s37: a timeline from 16,000 BCE to today: a lilac dotted dot at 15,000 BCE ('Posnansky'); then a book '1990s' at the right with a
    dotted arrow back to it ('Hancock')."""
    td, th = C.at(36, "dated the city"), C.at(36, "Graham Hancock")
    X = TLX(-15000)
    els = timeline_15k(560, .2) + [lab(1600, 640, "today", .4, DIM, 26, "end"),
           dt(X, 560, 14, LILAC, td), rg(X, 560, 30, td, LILAC, 3, "claimed", .6), gl(X, 560, 90, td, .5, "blue"),
           lab(X, 460, "15,000 BCE?", td + .3, LILAC, 40, st="serif"), lab(X, 410, "Posnansky", td + .6, DIM, 28)]
    bx = 1440
    els += [rect(bx - 50, 340, 100, 130, "#6b3a2a", "#c8743c", 3, 6, th, fx="pop"), ln([[bx - 30, 380], [bx + 30, 380]], th + .1, "#f2dcb4", 3, draw=False),
            ln([[bx - 30, 402], [bx + 18, 402]], th + .1, "#f2dcb4", 3, draw=False), lab(bx, 310, "1990s", th + .2, BONE, 28), lab(bx, 520, "Hancock", th + .3, DIM, 26),
            arr([[bx - 70, 400], [800, 350], [X + 40, 440]], th + .5, LILAC, 3, "claimed", 1.2)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


@scene(37)
def s38(C):
    """s38: the television again: on its screen an H-block with a lilac gear; 'machined?'; 'too precise for hand tools?'."""
    els, (sx, sy, sw, sh) = tv(889, 430, 620, .3)
    hx, hy, hs = sx + sw * .3, sy + sh * .8, sh * .55
    els += [poly([(hx + hs * u, hy - hs * v) for u, v in HPROF], AND, AND_E, 2, .6)]
    gx, gy, gr = sx + sw * .78, sy + sh * .36, 46
    els += [rg(gx, gy, gr, .9, LILAC, 5, dur=.5), rg(gx, gy, gr * .38, 1.0, LILAC, 4, dur=.3)] + \
           [ln([[gx + gr * math.cos(a), gy + gr * math.sin(a)], [gx + (gr + 14) * math.cos(a), gy + (gr + 14) * math.sin(a)]], 1.1, LILAC, 8, draw=False) for a in [k * math.pi / 4 for k in range(8)]]
    tp = C.at(37, "too precise")
    els += [lab(889, 720, "machined?", .8, LILAC, 40, st="serif"), lab(889, 770, "too precise for hand tools?", tp, LILAC, 28)]
    return {"base": "dark", "stars": 40, "cam": CAM, "els": els}


@scene(38)
def s39(C):
    """s39: radiocarbon, the candle clock: a plant takes in carbon (green dots); after death it fades at a steady pace, like a candle
    burning down; a bar measures 'what's left'."""
    tl, tf, tc = C.at(38, "Living things"), C.at(38, "fades after death"), C.at(38, "candle")
    G = 640
    els = [ln([[200, G], [1600, G]], -1, "#8c7152", 3, draw=False),
           ln([[480, G], [480, G - 230]], tl, "#7fa35a", 7, dur=.6),
           poly([(480, G - 120), (400, G - 170), (380, G - 210), (450, G - 180)], "#7fa35a", at=tl + .4, fx="pop"),
           poly([(480, G - 170), (560, G - 230), (580, G - 270), (510, G - 230)], "#7fa35a", at=tl + .6, fx="pop")]
    els += [dt(380 + 40 * k, 260 + 26 * (k % 2), 9, GREEN, tl + .8 + .2 * k) for k in range(5)] + \
           [arr([[388 + 40 * k, 284 + 26 * (k % 2)], [440 + 14 * k, G - 250]], tl + 1.0 + .2 * k, GREEN, 2, dur=.3, curve=False) for k in range(5)] + \
           [lab(480, 220, "carbon", tl + .8, GREEN, 30)]
    cx = 1150
    els += [rect(cx - 40, G - 300, 80, 300, "none", "#efe6d2", 2, 8, tf, style="inferred"), rect(cx - 40, G - 150, 80, 150, "#efe6d2", r=8, at=tc - .2),
            ln([[cx, G - 150], [cx, G - 176]], tc, INK, 3, draw=False), gl(cx, G - 196, 90, tc, .9, "fire"), dt(cx, G - 192, 10, "#ffcf8a", tc),
            arr([[cx + 90, G - 290], [cx + 90, G - 160]], tc + .4, AMBER, 4, dur=.6, curve=False), lab(cx + 110, G - 230, "fades", tc + .6, AMBER, 30, "start"),
            ln([[cx - 80, G - 150], [cx - 80, G]], tc + 1.0, GOLD, 4, dur=.4), lab(cx - 100, G - 70, "what's left", tc + 1.2, GOLD, 30, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(39)
def s40(C):
    """s40: the platform in section: andesite and sandstone courses on top, the lowest fill below with green organic specks; 'AD 536 to
    600'; under it the timeline from 16,000 BCE, a short gold band at the far right and the 15,000 BCE dot struck out."""
    tf, td = C.at(39, "lowest fill"), C.at(39, "five thirty-six")
    els = [rect(420 + 132 * k, 170, 128, 62, AND, "#2a2219", 2, 3, .3 + .05 * k) for k in range(7)] + \
          [rect(420 + 132 * k, 234, 128, 62, SAND_R, "#2a2219", 2, 3, .5 + .05 * k) for k in range(7)] + \
          [rect(420, 298, 920, 100, "#5f4c39", "#c9a070", 2, 3, tf - .3, fx="fill"), lab(1380, 360, "lowest fill", tf, AMBER, 30, "start")]
    rnd = random.Random(4)
    els += [dt(rnd.uniform(450, 1310), rnd.uniform(318, 384), 6, "#9fcf6a", tf + .3 + .06 * k) for k in range(14)] + [gl(880, 350, 320, tf + .4, .45, "scan")]
    els += [lab(880, 500, "AD 536 to 600", td, GOLD, 56, st="serif")]
    els += timeline_15k(660, td - .4, 180, 1600) + [
        rect(TLX(536) - 3, 640, TLX(600) - TLX(536) + 8, 40, GOLD, r=3, at=td + .4), lab(TLX(560) - 10, 620, "radiocarbon", td + .6, GOLD, 26, "end"),
        dt(TLX(-15000), 660, 12, LILAC, td + .2), strike(TLX(-15000) - 34, 690, TLX(-15000) + 34, 630, td + 1.4, RED, 6)]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


@scene(40)
def s41(C):
    """s41: a sliver of a degree: two lines leave one point a sliver apart; far away they are far apart; a red double arrow at the end:
    'thousands of years'."""
    tw, ts, tt = C.at(40, "weak"), C.at(40, "sliver"), C.at(40, "thousands of years")
    vx, vy = 200, 480
    els = [block3d(110, vy + 60, 100, 50, 30, .3), dt(vx, vy, 10, BONE, .5),
           ln([[vx, vy], [1640, vy - 70]], ts - .3, BONE, 3, dur=1.0), ln([[vx, vy], [1640, vy + 70]], ts, BONE, 3, dur=1.0),
           {"k": "line", "p": R([[vx + 120 * math.cos(math.radians(a)), vy - 120 * math.sin(math.radians(a))] for a in (-2.8, -1.4, 0, 1.4, 2.8)]), "c": AMBER, "w": 4, "fx": "draw", "dur": .4, "in": ts + .3},
           lab(vx + 150, vy - 30, "a sliver of a degree", ts + .5, AMBER, 30, "start"),
           arr([[1600, vy - 64], [1600, vy + 64]], tt - .3, RED, 4, dur=.5, curve=False), arr([[1600, vy + 64], [1600, vy - 64]], tt - .3, RED, 4, dur=.5, curve=False),
           lab(1580, vy - 100, "thousands of years", tt, RED, 34, "end", st="serif")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


ISOCK = [[400, 440], [600, 440], [600, 480], [530, 480], [530, 540], [600, 540], [600, 580], [400, 580], [400, 540], [470, 540], [470, 480], [400, 480]]


@scene(41)
def s42(C):
    """s42: two andesite blocks meet at a joint; an I-shaped socket outlines across it; a crucible pours molten bronze that fills the
    socket; copper, arsenic, nickel; 'Tiwanaku's own era'."""
    tc, tp, ta, te = C.at(41, "I-shaped"), C.at(41, "poured molten"), C.at(41, "copper"), C.at(41, "own era")
    K, ox, oy = 1.6, 889 - 500 * 1.6, 380 - 510 * 1.6
    I_ = [(ox + K * x, oy + K * y) for x, y in ISOCK]
    els = [rect(300, 220, 580, 330, AND, AND_E, 2, 6, .3), rect(898, 220, 580, 330, AND, AND_E, 2, 6, .4), ln([[889, 210], [889, 560]], .6, INK, 3, draw=False),
           poly(I_, "none", GOLD, 3, tc, fx="draw", dur=.8, style="inferred"),
           poly(I_, "#1a1511", "#fff3dc", 1.6, tc + 1.0, fx="pop"),
           poly([(1180, 120), (1300, 120), (1286, 200), (1194, 200)], "#5a4a3a", "#c9a070", 2, tp - .5, fx="pop"),
           ln([[1190, 180], [1060, 260], [960, 360]], tp, "#ffb060", 9, dur=.6, curve=True), gl(960, 360, 140, tp, .9, "red"),
           poly(I_, BRZ, "#ffcf9a", 1.6, tp + .6, fx="fill", dur=1.2), lab(889, 600, "bronze", tp + 1.0, BRZ, 34, st="serif")]
    for k, (el_, c) in enumerate((("copper", "#d9894a"), ("arsenic", "#cbd2d8"), ("nickel", "#9fd0ff"))):
        els += [dt(560 + 330 * k, 680, 26, c, ta + .5 * k), lab(600 + 330 * k, 690, el_, ta + .5 * k + .1, c, 30, "start")]
    els += [lab(889, 770, "Tiwanaku's own era", te, GOLD, 32, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(42)
def s43(C):
    """s43: three H-block profiles of the same design, each a little different in size; a dashed amber template slides over each; small
    mismatches glow where it and the stone differ: 'not identical'."""
    tp, tn = C.at(42, "patterns"), C.at(42, "no two")
    els = []
    for k, (cx, s_) in enumerate(((420, 250), (889, 262), (1358, 242))):
        x0, y0 = cx - s_ * .6, 560
        els.append(poly([(x0 + s_ * u, y0 - s_ * v) for u, v in HPROF], AND, AND_E, 2, .3 + .2 * k))
        T = 250
        tx0 = cx - T * .6
        els.append(poly([(tx0 + T * u + 6, y0 - T * v - 6) for u, v in HPROF], "rgba(232,184,122,.08)", AMBER, 3, tp + .5 * k, style="inferred", fx="draw", dur=.6))
        if k != 0:
            for (u, v) in ((1.2, 1.0), (.86, .64), (0, 0)):
                els.append(gl(x0 + s_ * u, y0 - s_ * v, 40, tn + .2 * k, .8, "blue"))
    els += [lab(889, 230, "a template", tp + .2, AMBER, 32), lab(889, 660, "not identical", tn + .4, BLUE, 34, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(43)
def s44(C):
    """s44: close on a sharp inside corner, lit; a lilac question mark; a faint hammerstone outline and a struck-out gear; 'tools: unknown'."""
    tq, tu = C.at(43, "sharp inside"), C.at(43, "Still unknown")
    els = [poly([(300, 760), (300, 200), (760, 200), (760, 520), (1300, 520), (1300, 760)], AND, AND_E, 3, .3),
           poly([(300, 200), (360, 160), (820, 160), (760, 200)], "#b3b4b0", AND_E, 2, .3),
           poly([(760, 200), (820, 160), (820, 480), (760, 520)], "#6f706c", AND_E, 2, .3),
           poly([(760, 520), (820, 480), (1360, 480), (1300, 520)], "#b3b4b0", AND_E, 2, .3),
           gl(762, 518, 140, .8, .9, "lamp"), rg(762, 518, 40, 1.0, GOLD, 3, dur=.5)] + qm(1060, 360, tq, 100)
    els += [oval(1460, 330, 70, 52, "none", BONE, 3, 1, tu - .6, style="inferred"), lab(1460, 430, "hammerstones?", tu - .4, DIM, 26),
            rg(1460, 640, 46, tu - .2, LILAC, 5, dur=.4), strike(1400, 700, 1520, 580, tu, RED, 5),
            lab(889, 780, "tools: unknown", tu + .2, LILAC, 34, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


# ================================================================ chapter 4: A jigsaw above Cusco
@scene(44)
def s45(C):
    """s45: Sacsayhuamán's three zigzag terraces on the hill (f06 sacsayhuaman shot 0, about 400 m long); the zigzags trace in gold one
    after another; a '400 m' dimension along the top."""
    base = short_iso(f06.sacsayhuaman, 0)
    base.update(x=889, y=560, s=9.4, az=-18, spin=.25, el=.42, **{"in": -1})
    tz, t4 = C.at(44, "zigzag"), C.at(44, "four hundred metres")
    zz = lambda y, off: [[-42 + 12 * k, y + 5.5, off + (9 if k % 2 else 0)] for k in range(8)]
    els = [gl(889, 520, 680, -1, .2, "lamp"), base]
    els += [ov(base, [{"t": "line", "p": zz(y, off), "c": GOLD, "w": 5}], tz + .5 * i, fx="draw", dur=1.0) for i, (y, off) in enumerate(((0, 14), (5.5, 2), (11, -10)))]
    els += [ov(base, [{"t": "line", "p": [[-42, 18, -14], [42, 18, -14]], "c": BONE, "w": 3}, {"t": "line", "p": [[-42, 17, -14], [-42, 19, -14]], "c": BONE, "w": 3},
                      {"t": "line", "p": [[42, 17, -14], [42, 19, -14]], "c": BONE, "w": 3}], t4, fx="draw", dur=.8)]
    x, y = P3(base, (0, 18, -14), t4)
    els += [lab(x, y - 24, "about 400 m", t4 + .4, BONE, 34), lab(1480, 330, "Sacsayhuamán", C.at(44, "Sacsayhuamán"), GOLD, 36, st="serif")]
    return {"base": "dark", "stars": 50, "cam": CAM, "els": els}


@late(45)
def s46_late(C):
    """s46 (the jigsaw wall of s4, closer): one giant outlined in gold, '100+ t'; its many corners dot in turn; 'no mortar'."""
    wall = jig_wall()
    g = jig_giant(wall)
    t1, tm, tk = C.at(45, "a hundred tonnes"), C.at(45, "many-sided"), C.at(45, "without mortar")
    cx = sum(p[0] for p in g) / len(g); cy = sum(p[1] for p in g) / len(g)
    out = [{"k": "poly", "p": g, "fill": "none", "c": GOLD, "w": 5, "curve": True, "in": t1 - .3, "fx": "draw", "dur": 1.0}, gl(cx, cy, 200, t1, .45),
           ink(cx, cy + 16, "100+ t", t1 + .4, INK, 48, st="serif")]
    corners = [p for k, p in enumerate(g) if k % 2 == 0]
    out += [dt(x, y, 8, GOLD, tm + .08 * k) for k, (x, y) in enumerate(corners)]
    x0, y0, w, h = JIG[:4]
    out += [lab(x0 + w / 2, y0 - 30, "no mortar", tk, BONE, 32, st="serif")]
    return out


@scene(46)
def s47(C):
    """s47: the claim: in elevation, giant polygonal stones at the bottom (1), small rough stones above (2); a lilac dotted box round the
    giants: 'older?'; 'two builders?'."""
    G = 740
    wall = f06.jigsaw(200, 480, 1240, 260, 7, 2, seed=5)
    for k, e in enumerate(wall):
        e["in"] = round(.2 + .02 * k, 2)
    to, tg, ts, tb = C.at(46, "older"), C.at(46, "Huge"), C.at(46, "smaller"), C.at(46, "two builders")
    rnd = random.Random(8)
    rough, k = [], 0
    for row, (yb, hh0) in enumerate(((478, 40), (436, 36))):
        x = 206 + 18 * row
        while x < 1420:
            w_ = rnd.uniform(34, 70); hh = hh0 + rnd.uniform(-6, 4)
            pts = [(x + rnd.uniform(0, 4), yb), (x + w_ - rnd.uniform(0, 4), yb), (x + w_ + rnd.uniform(-3, 3), yb - hh * rnd.uniform(.6, .9)),
                   (x + w_ * rnd.uniform(.55, .8), yb - hh), (x + w_ * rnd.uniform(.15, .4), yb - hh + rnd.uniform(-4, 4)), (x + rnd.uniform(-2, 3), yb - hh * rnd.uniform(.5, .8))]
            rough.append(poly(pts, ("#a8977c", "#9c8a6e", "#b3a283")[k % 3], "#2a2219", 1.5, ts + .015 * k, fx="pop"))
            x += w_ + 2; k += 1
    els = wall + rough + [
        rect(190, 470, 1260, 280, "rgba(201,193,238,.06)", LILAC, 4, 8, to, style="claimed"), lab(1480, 630, "older?", to + .4, LILAC, 36, "start", st="serif"),
        dt(150, 610, 24, LILAC, tg), ink(150, 620, "1", tg + .05, INK, 28, st="serif"), lab(820, 790, "huge, perfect", tg + .3, LILAC, 30),
        dt(150, 440, 24, AMBER, ts), ink(150, 450, "2", ts + .05, INK, 28, st="serif"), lab(820, 360, "smaller, rougher", ts + .4, AMBER, 30),
        lab(820, 250, "two builders?", tb, LILAC, 40, st="serif")]
    return {"base": "dark", "stars": 30, "floor": G, "cam": CAM, "els": els}


@scene(47)
def s48(C):
    """s48: a timeline from 1500 to 1580: crossed swords at 1536 ('the siege'); an arc 'a generation' to a chronicle at about 1553
    ('an Inca work')."""
    X = lambda yr: r1(200 + (yr - 1500) / 80 * 1380)
    t36, tg, ti = C.at(47, "fifteen thirty-six"), C.at(47, "within a generation"), C.at(47, "Inca work")
    Y = 560
    els = [ln([[X(1500), Y], [X(1580), Y]], .2, "#8c7152", 3, dur=1.0)] + \
          [ln([[X(y), Y - 10], [X(y), Y + 10]], .4, "#8c7152", 2, draw=False) for y in range(1500, 1581, 10)] + \
          [lab(X(1500), Y + 50, "1500", .4, DIM, 26), lab(X(1580), Y + 50, "1580", .4, DIM, 26),
           dt(X(1536), Y, 12, RED, t36), ln([[X(1536) - 40, Y - 150], [X(1536) + 40, Y - 60]], t36 + .2, BONE, 6), ln([[X(1536) + 40, Y - 150], [X(1536) - 40, Y - 60]], t36 + .3, BONE, 6),
           lab(X(1536), Y + 50, "1536", t36, RED, 30), lab(X(1536), Y - 180, "the siege", t36 + .4, RED, 30),
           {"k": "arrow", "p": R([[X(1536), Y - 30], [X(1544.5), Y - 110], [X(1553), Y - 30]]), "c": AMBER, "w": 3, "curve": True, "fx": "draw", "dur": .8, "in": tg},
           lab(X(1544.5), Y - 130, "a generation", tg + .4, AMBER, 28),
           rect(X(1553) - 60, Y - 260, 120, 110, "#e8dcc2", "#8a7a66", 2, 6, ti - .3, fx="pop"), ln([[X(1553) - 40, Y - 225], [X(1553) + 40, Y - 225]], ti - .2, INK, 3, draw=False),
           ln([[X(1553) - 40, Y - 195], [X(1553) + 26, Y - 195]], ti - .2, INK, 3, draw=False), dt(X(1553), Y, 12, AMBER, ti - .3),
           lab(X(1553) + 90, Y - 200, "an Inca work", ti, GOLD, 32, "start", st="serif")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


@scene(48)
def s49(C):
    """s49: Cieza de León's twenty thousand: 200 small figures, each 100 workers; 40 turn amber (4,000 quarrying), 60 turn blue (6,000
    hauling with ropes)."""
    t20, tq, th = C.at(48, "twenty thousand"), C.at(48, "Four thousand"), C.at(48, "Six thousand")
    fig = lambda k: (r1(420 + 56 * (k % 20)), r1(330 + 48 * (k // 20)))
    els = [pe(*fig(k), 42, round(t20 + .008 * k, 2), "#8a8378", fx="pop") for k in range(200)]
    els += [lab(889, 190, "twenty thousand workers", t20, BONE, 34, st="serif"), lab(889, 240, "each figure: 100 workers", t20 + .6, DIM, 26)]
    els += [pe(*fig(k), 42, round(tq + .012 * j, 2), AMBER, fx="pop") for j, k in enumerate(range(40))] + [lab(380, 340, "4,000 quarrying", tq + .4, AMBER, 30, "end")]
    els += [pe(*fig(k), 42, round(th + .01 * j, 2), BLUE, fx="pop") for j, k in enumerate(range(40, 100))] + [lab(380, 460, "6,000 hauling", th + .4, BLUE, 30, "end")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(49)
def s50(C):
    """s50: the hill in elevation: the upper courses drawn as dotted ghosts ('gone'); arrows carry small stones down to the houses and
    tower of colonial Cusco; the giants at the bottom glow: 'too big to shift'."""
    G = 560
    tu, tc, tb = C.at(49, "rougher upper"), C.at(49, "carted down"), C.at(49, "too big")
    gi = [[(120, G), (200, G - 140), (330, G - 160), (360, G - 80), (340, G)], [(340, G), (360, G - 80), (330, G - 160), (470, G - 180), (560, G - 140), (540, G)],
          [(540, G), (560, G - 140), (690, G - 165), (760, G - 120), (740, G)]]
    els = [poly([(-40, G), (1820, G), (1820, 1010), (-40, 1010)], "#2e261e", at=-1),
           poly([(-40, G + 2), (420, G - 10), (900, G + 40), (1300, G + 160), (1820, G + 220), (1820, 1010), (-40, 1010)], "#3b3127", at=-1, curve=True)]
    els += [poly(p, "#d9c9a6", "#2a2219", 2.4, .3 + .15 * k, curve=True) for k, p in enumerate(gi)]
    els += [rect(130 + 50 * k, G - 230 - 52 * (k // 13), 46, 48, "none", "#cbbca8", 2, 3, tu + .02 * k, style="claimed") for k in range(13)] + \
           [rect(160 + 50 * k, G - 282, 46, 48, "none", "#cbbca8", 2, 3, tu + .3 + .02 * k, style="claimed") for k in range(11)] + \
           [lab(440, G - 330, "gone", tu + .6, LILAC, 34, st="serif")]
    els += [arr([[x0, G - 250], [x0 + 300, G - 120], [1150, G + 90]], tc + .3 * k, AMBER, 3, "inferred", 1.2) for k, x0 in enumerate((300, 480, 640))]
    for k in range(5):
        els.append({"k": "house", "x": 1150 + 80 * k, "y": G + 130 + (k % 2) * 12, "w": 68, "h": 44, "fill": "#8e7152", "in": round(tc + .5 + .12 * k, 2)})
    els += [rect(1560, G + 0, 40, 140, "#8e7152", "rgba(255,236,206,.4)", 1, 2, tc + .9), poly([(1554, G + 0), (1580, G - 40), (1606, G + 0)], "#6b4a2e", at=tc + .9),
            lab(1380, G + 210, "colonial Cusco", tc + 1.0, AMBER, 30),
            gl(440, G - 80, 300, tb, .45), lab(440, G + 60, "too big to shift", tb + .2, GOLD, 32, st="serif")]
    return {"base": "sky", "tod": "dusk", "ground": G, "sun": [1500, 300, 20], "cam": CAM, "els": els}


@scene(50)
def s51(C):
    """s51: Protzen's experiment: a 4 kg hammerstone strikes a small andesite block, dust flies; a stopwatch sweeps to 20 minutes; one
    face of the block turns smooth."""
    th, tk, tm = C.at(50, "hammerstones"), C.at(50, "four kilos"), C.at(50, "twenty minutes")
    G = 640
    els = [ln([[200, G], [1580, G]], -1, "#8c7152", 3, draw=False), block3d(620, G, 300, 220, 160, .3),
           oval(470, 330, 74, 60, "#6a645c", "#cbbca8", 3, 1, th, fx="pop"), lab(470, 240, "hammerstone", th + .3, BONE, 30),
           lab(470, 440, "about 4 kg", tk, AMBER, 30)]
    els += [{"k": "arrow", "p": R([[430, 410], [520, 480], [610, 470]]), "c": BONE, "w": 3, "style": "inferred", "curve": True, "fx": "draw", "dur": .4, "in": th + .5 + .6 * k} for k in range(3)]
    rnd = random.Random(2)
    els += [dt(620 + rnd.uniform(-40, 20), 420 + rnd.uniform(-40, 60), 4, "#cbbca8", th + .7 + .05 * k) for k in range(16)]
    els += [rect(622, G - 218, 296, 216, "rgba(255,240,210,.18)", GOLD, 3, 2, tm + .4, fx="draw", dur=.6), lab(770, G + 50, "one face, dressed", tm + .8, GOLD, 28)]
    cx, cy = 1260, 420
    els += [{"k": "circle", "x": cx, "y": cy, "r": 110, "fill": "#efe6d2", "c": "#c9a070", "w": 6, "in": tm - .6},
            rect(cx - 16, cy - 140, 32, 24, "#c9a070", r=4, at=tm - .6),
            {"k": "poly", "p": R([[cx, cy]] + [[cx + 100 * math.sin(math.radians(a)), cy - 100 * math.cos(math.radians(a))] for a in range(0, 121, 10)]), "fill": "rgba(232,184,122,.55)", "c": "none", "w": 0, "in": tm - .3, "fx": "draw", "dur": .8},
            ln([[cx, cy], [cx + 90 * math.sin(math.radians(120)), cy - 90 * math.cos(math.radians(120))]], tm, INK, 5, draw=False),
            ink(cx, cy + 60, "20 min", tm + .2, INK, 34, st="serif")]
    return {"base": "dark", "stars": 20, "floor": G, "cam": CAM, "els": els}


@scene(51)
def s52(C):
    """s52: the fitting cycle in four steps: lower (the upper stone set on the lower), mark (red dots where they touch), pound (the
    hammerstone), repeat (a loop arrow); then a tight joint glows: close to the Incas' own."""
    tl, tm, tp, tr, tj = C.at(51, "lower one"), C.at(51, "see where"), C.at(51, "pound"), C.at(51, "repeat"), C.at(51, "joints came")
    els = []
    xs = [300, 680, 1060, 1440]
    for k, x in enumerate(xs):
        t = (tl, tm, tp, tr)[k]
        els += [rect(x - 170, 200, 340, 380, "rgba(31,25,20,.85)", "rgba(245,236,220,.18)", 1.5, 14, t - .3),
                poly([(x - 120, 500), (x + 120, 500), (x + 110, 420), (x + 40, 400), (x - 30, 430), (x - 110, 410)], "#c9b894", "#2a2219", 2, t - .2)]
        if k == 0:
            els += [poly([(x - 120, 340), (x + 110, 340), (x + 110, 330 - 80), (x - 120, 260)], "#d9c9a6", "#2a2219", 2, t, fx="rise"),
                    arr([[x, 250], [x, 300]], t + .3, BONE, 3, dur=.3, curve=False)]
        if k == 1:
            els += [dt(x + 40, 400, 9, RED, t + .1 * j) for j in range(1)] + [dt(x - 30, 430, 9, RED, t + .2), dt(x - 110, 412, 9, RED, t + .3)]
        if k == 2:
            els += [oval(x + 10, 330, 44, 36, "#6a645c", "#cbbca8", 2, 1, t), ln([[x - 20, 372], [x - 34, 392]], t + .2, AMBER, 4, draw=False),
                    ln([[x + 40, 372], [x + 54, 392]], t + .2, AMBER, 4, draw=False)]
        if k == 3:
            els += [{"k": "arrow", "p": R([[x + 70 * math.cos(a), 310 + 60 * math.sin(a)] for a in [q * .4 + 3.4 for q in range(14)]]), "c": GOLD, "w": 4, "curve": True,
                     "fx": "draw", "dur": .7, "in": t}]
        els += [lab(x, 640, ("lower", "mark", "pound", "repeat")[k], t + .2, (BONE, RED, AMBER, GOLD)[k], 32)]
    els += [ln([[230, 720], [1510, 720]], tj, GOLD, 4, dur=1.0), lab(889, 770, "close to the Incas' own", tj + .5, GOLD, 32, st="serif")]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(52)
def s53(C):
    """s53: the Inca quarry for Ollantaytambo: a mountainside in elevation, a broad ramp road zigzagging down from the quarry to the valley
    ('up to 8 m wide'); 80 abandoned blocks lie along it."""
    tq, tr, tb = C.at(52, "Ollantaytambo"), C.at(52, "ramps"), C.at(52, "eighty blocks")
    els = [poly([(-40, 260), (200, 200), (420, 240), (700, 380), (1000, 560), (1300, 700), (1820, 760), (1820, 1010), (-40, 1010)], "#4d3e30", "#8a6a48", 2, -1, curve=True),
           poly([(80, 240), (260, 200), (330, 250), (200, 300)], "#cbbca8", at=.4), lab(210, 180, "quarry", .6, BONE, 30)]
    road = [(240, 280), (620, 360), (360, 420), (900, 520), (640, 590), (1250, 690), (1620, 760)]
    els += [ln(road, tr, "#a8977c", 22, dur=2.0), ln(road, tr, "#2a2219", 2, "inferred", dur=2.0), lab(980, 470, "ramps up to 8 m wide", tr + 1.0, AMBER, 30, "start")]
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(road, road[1:])]
    tot = sum(L)
    rnd = random.Random(14)
    for k in range(80):
        d = tot * (k + .5) / 80
        i = 0
        while d > L[i]:
            d -= L[i]; i += 1
        a, b = road[i], road[i + 1]
        u = d / L[i]
        x, y = a[0] + (b[0] - a[0]) * u + rnd.uniform(-14, 14), a[1] + (b[1] - a[1]) * u + rnd.uniform(-10, 4)
        els.append(rect(x - 7, y - 7, 14, 10, "#d8c49c", "#2a2219", 1, 1, tb + .02 * k, fx="pop"))
    els += [lab(500, 640, "80 abandoned blocks", tb + 1.0, GOLD, 32, st="serif"),
            {"k": "house", "x": 1500, "y": 700, "w": 60, "h": 36, "fill": "#8e7152", "in": tq}, {"k": "house", "x": 1570, "y": 712, "w": 60, "h": 36, "fill": "#8e7152", "in": tq},
            lab(1560, 640, "Ollantaytambo", tq + .3, DIM, 30)]
    return {"base": "sky", "tod": "dusk", "ground": 1000, "sun": [1560, 200, 20], "cam": CAM, "els": els}


@scene(53)
def s54(C):
    """s54: a timeline from 800 to 1600 CE: people on the hill before the Incas, from about 900 (a dim band); Inca works from about 1440
    (gold); above, the giant wall's outline with a lilac '?': 'older wall: undated'."""
    X = lambda yr: r1(200 + (yr - 800) / 800 * 1380)
    tb, tn = C.at(53, "nine hundred"), C.at(53, "no older wall")
    Y = 640
    ticks = [[X(y), str(y)] for y in (800, 1000, 1200, 1400, 1600)]
    els = [{"k": "axis", "x0": 200, "x1": 1580, "y": Y, "ticks": ticks, "t": "", "in": .2},
           {"k": "band", "x0": X(900), "x1": X(1440), "y": Y - 70, "h": 18, "c": "#c9ad85", "op": .75, "t": "people on the hill", "tc": DIM, "in": tb},
           {"k": "band", "x0": X(1440), "x1": X(1536), "y": Y - 70, "h": 18, "c": GOLD, "t": "Inca works", "tc": GOLD, "in": .6, "tx": X(1500), "a": "start"}]
    wall = f06.jigsaw(560, 200, 660, 230, 5, 2, seed=11)
    for k, e in enumerate(wall):
        e.update(fill="none", c=LILAC, w=2.5, style="claimed")
        e["in"] = round(tn - .4 + .02 * k, 2)
    els += wall + qm(889, 330, tn + .3, 90) + [lab(889, 490, "older wall: undated", tn + .6, LILAC, 32, st="serif")]
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


# ================================================================ chapter 5: The weighing
def icon(kind, x, y, at):
    if kind == "gear":
        return [rg(x, y, 26, at, LILAC, 5, dur=.3), rg(x, y, 10, at, LILAC, 3, dur=.2)] + \
               [ln([[x + 26 * math.cos(a), y + 26 * math.sin(a)], [x + 36 * math.cos(a), y + 36 * math.sin(a)]], at, LILAC, 6, draw=False) for a in [q * math.pi / 4 for q in range(8)]]
    if kind == "tri":
        return [rect(x - 50 + 34 * k, y + 4, 32, 16, "#c8b692", r=1, at=at) for k in range(3)] + [rect(x - 50, y - 14, 100, 16, "#e0cfa8", r=1, at=at)]
    if kind == "ramp":
        return [poly([(x - 50, y + 22), (x + 50, y + 22), (x + 50, y - 8)], "rgba(122,98,72,.6)", "#c9a070", 1.5, at), rect(x + 6, y - 34, 44, 24, "#e0cfa8", r=2, at=at)]
    if kind == "h":
        return [poly([(x - 36 + 60 * u, y + 26 - 52 * v) for u, v in HPROF], AND, AND_E, 1.5, at)]
    if kind == "corner":
        return [poly([(x - 40, y + 26), (x - 40, y - 26), (x, y - 26), (x, y), (x + 40, y), (x + 40, y + 26)], AND, AND_E, 1.5, at), gl(x, y, 30, at, .9)]
    if kind == "wall":
        w = f06.jigsaw(x - 50, y - 28, 100, 56, 3, 2, seed=2)
        for e in w:
            e["in"] = at; e["w"] = 1.2
        return w
    if kind == "hammer":
        return [oval(x, y, 30, 24, "#6a645c", "#cbbca8", 2, 1, at)]
    return []


@scene(54)
def s55(C):
    """s55: the ledger: seven rows, each with a small picture; each row lights as it is named and its grade chip pops as the grade is said."""
    rows = [("a lost high technology", "gear", "lost high technology", "ruled out", "Ruled out", "ruled"),
            ("Baalbek older than Rome", "tri", "older than Rome", "awaiting evidence", "Awaiting evidence", "awaiting"),
            ("raising the trilithon", "ramp", "Exactly how", "open question", "Open question", "open"),
            ("Puma Punku, 15,000 BCE", "h", "Puma Punku in", "ruled out", "Ruled out", "ruled"),
            ("cutting those corners", "corner", "sharp corners", "open question", "Open question", "open"),
            ("older builders, Cusco", "wall", "Older builders", "awaiting evidence", "Awaiting evidence", "awaiting"),
            ("Inca hammerstones", "hammer", "Inca hammerstones", "strong evidence", "Strong evidence", "strong")]
    els = [rect(110, 130, 1560, 660, "rgba(18,13,10,.78)", "rgba(255,236,206,.3)", 2, 18, .2)]
    y0, dy = 178, 90
    for k, (name, ic, ph, gph, chip_t, key) in enumerate(rows):
        y = y0 + dy * k
        tn = C.at(54, ph) - .2
        tg = C.at(54, gph, after=ph) - .1
        els += [rect(130, y - 40, 1520, 80, "rgba(242,201,142,.08)", "rgba(242,201,142,.3)", 1.5, 10, tn, fx="pop")] + icon(ic, 210, y, tn + .1) + \
               [lab(300, y + 10, name, tn + .2, BONE, 30, "start")] + chip(1160, y, chip_t, GRADE[key], tg, 28, a="start")
    return {"base": "dark", "stars": 30, "cam": CAM, "els": els}


@scene(55)
def s56(C):
    """s56: three small monuments side by side (the trilithon wall, the H-blocks, the polygonal wall); 'Mixed record' pops in the middle;
    under each, its builders as named; at 'monuments to people', small crowds rise in front of each."""
    tm, tr, tt, ti, tp = C.at(55, "mixed record"), C.at(55, "the Romans"), C.at(55, "builders of"), C.at(55, "the Incas"), C.at(55, "monuments to people")
    els = []
    G = 640
    # the trilithon wall
    els += [rect(160 + 66 * k, G - 60, 64, 60, "#c8b692", "#2a2219", 1.5, 2, .3) for k in range(6)] + [rect(160 + 132 * k, G - 128, 130, 66, "#e0cfa8", "#2a2219", 1.5, 2, .4) for k in range(3)]
    # the H-blocks
    for k in range(3):
        els.append(poly([(740 + 110 * k + 96 * u, G - 96 * v) for u, v in HPROF], AND, AND_E, 2, .5 + .1 * k))
    # the polygonal wall
    w = f06.jigsaw(1210, G - 190, 400, 190, 4, 2, seed=3)
    for e in w:
        e["in"] = .7
    els += w
    els += chip(889, 260, "Mixed record", GRADE["mixed"], tm, 36)
    els += [lab(359, G + 60, "the Romans", tr, GOLD, 32, st="serif"), lab(889, G + 60, "Tiwanaku", tt + .3, GOLD, 32, st="serif"), lab(1410, G + 60, "the Incas", ti, GOLD, 32, st="serif")]
    for k, cx in enumerate((359, 889, 1410)):
        for j in range(7):
            els.append(pe(cx - 150 + 50 * j, G + 150, 70, tp + .1 * j + .2 * k, "#e8d6b8"))
    els += [gl(889, 500, 700, tp, .2, "lamp")]
    return {"base": "dark", "stars": 50, "floor": G + 150, "cam": CAM, "els": els}


@scene(56)
def s57(C):
    """s57: what would change our minds, four cards: a sealed layer under the trilithon with a potsherd; a charcoal fleck behind a giant
    with a radiocarbon tag; a replica corner and stone tools; a dashed tool, workshop and drill bit with a '?'."""
    tb, ts, tp, tl = C.at(56, "At Baalbek"), C.at(56, "At Sacsayhuamán"), C.at(56, "At Puma Punku"), C.at(56, "lost technology")
    cw, gap, x0, y0, y1 = 380, 20, 90, 150, 760
    c = [x0 + k * (cw + gap) + cw / 2 for k in range(4)]
    els = [rect(x0 + k * (cw + gap), y0, cw, y1 - y0, "#1f1914", "rgba(245,236,220,.14)", 1.5, 14, (tb, ts, tp, tl)[k] - .4) for k in range(4)]
    # 1 · Baalbek: the trilithon over a sealed layer, a potsherd
    els += [rect(c[0] - 150, 300, 300, 90, "#e0cfa8", "#2a2219", 2, 3, tb), rect(c[0] - 150, 392, 300, 60, "rgba(159,208,255,.12)", BLUE, 2.5, 4, tb + .5, style="inferred"),
            poly([(c[0] - 20, 430), (c[0], 418), (c[0] + 24, 424), (c[0] + 18, 440), (c[0] - 12, 442)], BRZ, "#ffd8a8", 1.5, tb + 1.0, fx="pop"), gl(c[0], 430, 60, tb + 1.0, .8),
            lab(c[0], 520, "sealed layer", tb + .6, BLUE, 30), lab(c[0], 570, "Roman pottery?", tb + 1.4, AMBER, 26), lab(c[0], 214, "Baalbek", tb, BONE, 28)]
    # 2 · Sacsayhuamán: a giant, the fill behind it, a charcoal fleck
    els += [poly([(c[1] - 140, 460), (c[1] - 120, 300), (c[1] - 10, 280), (c[1] + 10, 460)], "#d9c9a6", "#2a2219", 2, ts),
            rect(c[1] + 10, 290, 130, 170, "#5f4c39", "#c9a070", 2, 3, ts + .3), dt(c[1] + 70, 380, 9, "#1a1511", ts + .8), gl(c[1] + 70, 380, 60, ts + .8, .9, "lamp"),
            rect(c[1] + 20, 480, 110, 34, "#efe6d2", r=6, at=ts + 1.2), ink(c[1] + 75, 504, "C-14", ts + 1.25, INK, 24),
            lab(c[1], 580, "one date", ts + 1.0, AMBER, 30), lab(c[1], 214, "Sacsayhuamán", ts, BONE, 28)]
    # 3 · Puma Punku: a replica corner and stone tools
    els += [poly([(c[2] - 120, 470), (c[2] - 120, 300), (c[2] - 10, 300), (c[2] - 10, 400), (c[2] + 120, 400), (c[2] + 120, 470)], "rgba(141,142,138,.6)", AND_E, 2, tp, style="inferred"),
            oval(c[2] + 60, 330, 30, 24, "#6a645c", "#cbbca8", 2, 1, tp + .5), dt(c[2] + 110, 350, 5, "#d8c08a", tp + .6), dt(c[2] + 120, 360, 5, "#d8c08a", tp + .65),
            lab(c[2], 580, "a replica", tp + .8, AMBER, 30), lab(c[2], 214, "Puma Punku", tp, BONE, 28)]
    # 4 · the lost technology: one thing left behind
    els += [rect(c[3] - 130, 300, 80, 50, "none", LILAC, 2.5, 6, tl, style="claimed"), poly([(c[3] - 20, 360), (c[3] + 50, 300), (c[3] + 120, 360)], "none", LILAC, 2.5, tl + .3, style="claimed"),
            rect(c[3] - 10, 360, 120, 70, "none", LILAC, 2.5, 2, tl + .3, style="claimed"), ln([[c[3] - 110, 470], [c[3] - 10, 470], [c[3] + 10, 480], [c[3] - 10, 490], [c[3] - 110, 490]], tl + .6, LILAC, 2.5, "claimed", .5)] + \
           qm(c[3], 600, tl + 1.0, 70) + [lab(c[3], 690, "one thing left behind", tl + 1.2, LILAC, 26), lab(c[3], 214, "the lost technology", tl, BONE, 28)]
    return {"base": "dark", "stars": 20, "cam": CAM, "els": els}


@scene(57)
def s58(C):
    """s58: the quarry at night under stars; the 2014 block alone in its cutting; a faint lamp glow on its face; nobody there."""
    els, (x, y, w, h, d) = quarry_block(-1, "night")
    night = "rgba(10,12,30,.55)"
    els += [poly([(x, y), (x + w, y), (x + w, y - h), (x, y - h)], night, at=-1),
            poly([(x, y - h), (x + w, y - h), (x + w + .6 * d, y - h - .4 * d), (x + .6 * d, y - h - .4 * d)], night, at=-1),
            poly([(x + w, y), (x + w + .6 * d, y - .4 * d), (x + w + .6 * d, y - h - .4 * d), (x + w, y - h)], "rgba(10,12,30,.65)", at=-1),
            gl(x + w * .3, y - h * .4, 260, 1.0, .35, "lamp"), dt(x + w * .3, y + 2, 7, "#ffcf8a", 1.0), gl(x + w * .5, y - h - 120, 600, 2.0, .12, "blue")]
    return {"base": "sky", "tod": "night", "ground": 712, "sun": False, "moon": [1450, 200, 26], "cam": CAM, "els": els}


# ================================================================ the film
def _tagged(cams):
    """Each alias camera gets a tiny unique extra zoom (invisible), so its step can be found after the wall is built."""
    out = {}
    for k, i in enumerate(sorted(cams)):
        z, x, y = cams[i]
        out[i] = [round(z + .0003 * (k + 1), 4), x, y]
    return out


def _attach(ep, cams, late_els):
    """Give each alias step its additions: a panel item on that step (built once, shown from the start of its glide, timed on its clock)."""
    panels = ep["wall"]["panels"]
    for i, els in late_els.items():
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


SOURCES = ("van Ess 2015 (e-Forschungsberichte des DAI) · Lohmann 2010 · Adam 1977 (Syria 54) · Fall et al. 2014 (doi:10.1103/PhysRevLett.112.175502) · "
           "Lipo & Hunt 2025 (doi:10.1016/j.jas.2025.106383) · Vranich 2018 (doi:10.1186/s40494-018-0231-0) · Lechtman 1998 · "
           "Protzen & Nair 1997 · Protzen 1985 · Cieza de León c. 1553 · Bauer 2004")

POST = ("How do you move a 1,000-tonne stone? Baalbek's giants, Puma Punku's H-blocks and Sacsayhuamán's jigsaw walls, the claims of a lost "
        "technology, and what sledges, wet sand, capstans, ramps and a boulder hauled by hand in 1770 tell us. Weighed claim by claim.")


def film():
    beats = BEATS()
    C = Clock(beats)
    shots = []
    for i in range(NSHOT):
        if i in ALIAS:
            shots.append({"base": "dark", "cam": CAM, "els": []})
        else:
            sc = SCENES[i](C) if i in SCENES else placeholder(i)
            sc["els"][0]["_sid"] = i                     # a tag (ignored by the kit): which script shot a panel shows (for previews)
            shots.append(sc)
    cams = _tagged(ALIAS_CAMS)
    late_els = {i: f(C) for i, f in LATES.items()}
    desc = re.sub(r"0:00 Impossible Stones\n(?:mm:ss [^\n]*\n?)+", "{chapters}\n", SCRIPT["description"])
    assert "{chapters}" in desc
    ep = {"id": "lf-impossible-stones", "code": "LF.06", "series": SCRIPT["series"], "title": SCRIPT["title"], "case": "impossible-stones",
          "verdict": "mixed", "claim": "Were the world's giant stones impossible without a lost technology?", "mood": "mystery",
          "hook_text": "How do you move a *1,000-tonne* stone?", "beats": beats, "shots": shots,
          "sources": SOURCES, "post": POST, "hashtags": ["#Baalbek", "#PumaPunku", "#Sacsayhuaman", "#AncientEngineering", "#WeighItYourself"],
          "aspect": "16:9", "intro_title": SCRIPT["title"], "yt_title": SCRIPT["yt_title"], "description": desc,
          "end_line": "The largest block of the ancient world still waits for a crew that never came."}
    out = remix(ep, alias=dict(ALIAS), cams=cams)
    return _attach(out, cams, late_els)


def EPISODES():
    return [film()]
