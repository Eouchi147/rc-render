"""The mural: a whole film as one continuous take across a wall of full-frame panels.

Every scene of a film (a map, a model, a cross-section, a sky) hangs on one wall as a framed panel. The camera never cuts:
it lifts off one panel and settles on the next as the narrator moves on, a thread drawing itself between them, and each
panel's drawing builds itself when the camera arrives (the scene's own animations, timed from the arrival).

remix(ep, scenes={i: new_scene}, ...) turns an existing film (shots + beats with [go:] markers) into the mural version:
scene i is shot i of the film (or its replacement), beats keep their words, [k:] kicker titles go, every cut becomes a glide.

A long film (ep["aspect"] == "16:9") goes to wall() instead: 16:9 panels (1778 x 1000) hung in a meander, one row (a room) per
chapter, a drawn chapter card the camera visits as each chapter starts, 9:16 scenes from the Shorts reused through a window
(inset) or hung as they are (tall), and every element built once (kit.js WALL), so a 10 minute film with 80 panels stays
light to load and to draw. See films/long/LONG_ENGINE.md.
"""
import copy, math, re

PW, PH = 1000, 1778
TEXT = ("para", "num", "title", "q", "cap")          # dropped from reused scenes: the mural shows, the narrator tells
THREAD = "#e8b87a"


def settle(e):
    """An element already on the wall: no build-in (and none for anything inside it)."""
    e = copy.deepcopy(e)
    e["in"] = -1
    for c in e.get("els", []) or []:
        c["in"] = -1
        for cc in c.get("els", []) or []:
            cc["in"] = -1
    return e


def base_params(sc):
    return {k: v for k, v in sc.items() if k not in ("els", "cam", "dir", "cont", "hop", "base", "note", "_own")}


class Mural:
    def __init__(self, scenes, cols=2, gap=170, drop=TEXT, keep=None):
        self.scenes = scenes
        self.cols, self.gap = cols, gap
        self.drop, self.keep = set(drop), keep
        self.pos = []
        for i in range(len(scenes)):
            r, c = divmod(i, cols)
            if r % 2:
                c = cols - 1 - c                                   # a snake: the next panel is always a neighbour
            self.pos.append((c * (PW + gap), r * (PH + gap)))
        self.steps, self.visited, self.cur = [], [], None

    def cam(self, i, cam=None):
        z, x, y = (cam or self.scenes[i].get("cam") or [1, 500, 860])[:3]
        ox, oy = self.pos[i]
        return [z, round(x + ox, 1), round(y + oy, 1)]

    def frame(self, i):
        sc = self.scenes[i]; ox, oy = self.pos[i]
        return {"k": "panel", "ox": ox, "oy": oy, "base": sc.get("base", "dark"), "bs": base_params(sc), "els": [], "edge": "rgba(255,236,206,.16)", "in": -1}

    def content(self, i):
        sc = self.scenes[i]; ox, oy = self.pos[i]
        els = []
        for e in sc.get("els", []):
            if not sc.get("_own") and e.get("k") in self.drop and not (self.keep and self.keep(e)):     # authored scenes keep their words
                continue
            els.append(copy.deepcopy(e))
        return {"k": "panel", "ox": ox, "oy": oy, "base": "none", "els": els, "scene": True}

    def thread(self, a, b, at=.1):
        """A line drawn across the gap between two neighbouring panels: the argument moving on."""
        (ax, ay), (bx, by) = self.pos[a], self.pos[b]
        if not ((ay == by and abs(bx - ax) <= PW + self.gap + 1) or (ax == bx and abs(by - ay) <= PH + self.gap + 1)):
            return []                                              # only between neighbours
        if ay == by:
            y = ay + PH * .5; x0, x1 = (ax + PW, bx) if bx > ax else (ax, bx + PW)
            p = [[x0, y], [x1, y]]
        elif ax == bx:
            x = ax + PW * .5; y0, y1 = (ay + PH, by) if by > ay else (ay, by + PH)
            p = [[x, y0], [x, y1]]
        else:
            return []
        return [{"k": "line", "p": p, "c": THREAD, "w": 4, "op": .8, "keepop": True, "fx": "draw", "dur": .8, "in": at}]

    def visit(self, i, add=(), cam=None, force=False):
        """The next step of the take: the camera settles on scene i (its drawing builds if it is new here).
        add: elements in the scene's own frame units, drawn on this step and kept."""
        ox, oy = self.pos[i]
        add = [{"k": "panel", "ox": ox, "oy": oy, "base": "none", "els": list(add)}] if add else []
        els = [self.frame(k) for k in range(len(self.scenes))]
        for k in self.visited:
            els.append(settle(self.content(k)))
        if self.steps:                                            # what earlier steps added stays on the wall
            els += [settle(e) for e in self.steps[-1].get("_added", [])]
        new = []
        if i not in self.visited:
            new.append(self.content(i)); self.visited.append(i)
        if self.cur is not None and self.cur != i:
            new += self.thread(self.cur, i)
        new += list(add)
        prev = self.steps[-1]["cam"] if self.steps else None
        c = cam or self.cam(i)
        hop = 0
        if prev:
            d = math.hypot(c[1] - prev[1], c[2] - prev[2])
            hop = round(min(.7, .1 + d / 6500), 3) if d > 400 else 0
        s = {"base": "dark", "cam": c, "els": els + new, "cont": True, "dir": {"move": "hold"}}
        if hop:
            s["hop"] = hop
        s["_added"] = (self.steps[-1].get("_added", []) if self.steps else []) + [e for e in new if not e.get("scene")]
        self.steps.append(s)
        self.cur = i
        return len(self.steps) - 1

    def shots(self):
        out = []
        for s in self.steps:
            s = dict(s); s.pop("_added", None); out.append(s)
        return out


KICK = re.compile(r"\[(?:k|cam):[^\]]*\]")
GO = re.compile(r"\[go:([\d.]+)(?:\|([\d.]+))?\]")


def rewritten(ep):
    """The clarity pass (science-show narration): films/rewrite/<id>.json holds {"beats": [[line, ...], ...]} replacing the lines beat by beat."""
    import json, os
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rewrite", ep["id"] + ".json")
    ep["_same"] = not os.path.exists(f)
    if os.path.exists(f):
        r = json.load(open(f, encoding="utf-8"))
        assert len(r["beats"]) == len(ep["beats"]), (ep["id"], "beat count")
        for b, lines in zip(ep["beats"], r["beats"]):
            b["lines"] = list(lines)
    return ep


WORD = re.compile(r"\[[^\]]*\]")


def step_words(beats):
    """Words spoken while each step of the take is on screen (from the remixed beats)."""
    n = {}
    for b in beats:
        cur = b["visual"]["from"]
        for ln in b["lines"]:
            pos = 0
            for m in re.finditer(r"\[go:(\d+)[^\]]*\]", ln):
                seg = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", WORD.sub(" ", ln[pos:m.start()]))
                n[cur] = n.get(cur, 0) + len(seg.split())
                cur = int(m.group(1)); pos = m.end()
            seg = re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", WORD.sub(" ", ln[pos:]))
            n[cur] = n.get(cur, 0) + len(seg.split())
    return n


def _stretch(e, k):
    e = dict(e)
    if isinstance(e.get("in"), (int, float)) and e["in"] > 0:
        e["in"] = round(e["in"] * k, 2)
    if e.get("els"):
        e["els"] = [_stretch(c, k) for c in e["els"]]
    return e


def remix(ep, scenes=None, cols=2, gap=170, drop=TEXT, keep=None, adds=None, cams=None, glide=1.3, alias=None, beat_adds=None, line_adds=None, _rewrite=True):
    """(when the narration was rewritten longer, each step's drawings are stretched in time by how much longer its words got)"""
    if ep.get("aspect") == "16:9":                              # a long film: the 16:9 wall (see wall() below), every panel built once
        return wall(ep, scenes=scenes, keep=keep, adds=adds, cams=cams, alias=alias, beat_adds=beat_adds, line_adds=line_adds)
    kw = dict(scenes=scenes, cols=cols, gap=gap, drop=drop, keep=keep, adds=adds, cams=cams, glide=glide, alias=alias, beat_adds=beat_adds, line_adds=line_adds)
    new = _remix(rewritten(copy.deepcopy(ep)) if _rewrite else copy.deepcopy(ep), **kw)
    if not _rewrite or new.get("_same"):
        return new
    old = _remix(copy.deepcopy(ep), **kw)
    if len(old["shots"]) != len(new["shots"]):
        return new
    wn, wo = step_words(new["beats"]), step_words(old["beats"])
    for k, sh in enumerate(new["shots"]):
        r = max(1.0, min(2.5, (wn.get(k, 0) + 3) / (wo.get(k, 0) + 3)))
        if r > 1.05:
            sh["els"] = [_stretch(e, r) if (e.get("k") == "panel" and any((c.get("in") or 0) > 0 for c in e.get("els", []))) else e for e in sh["els"]]
    return new


def _remix(ep, scenes=None, cols=2, gap=170, drop=TEXT, keep=None, adds=None, cams=None, glide=1.3, alias=None, beat_adds=None, line_adds=None):
    """ep: a film spec (shots + beats). scenes: {shot index: replacement scene}. adds: {shot index: elements added on the first visit}.
    cams: {shot index: camera, in the shot's own frame units}. alias: {shot index: earlier shot index}: that shot is a return to the
    earlier panel (with its own camera), not a new panel. Returns a new spec with one continuous take."""
    alias = alias or {}
    order = [i for i in range(len(ep["shots"])) if i not in alias]
    pan = {i: k for k, i in enumerate(order)}
    for i, j in alias.items():
        pan[i] = pan[j]
    sc = [copy.deepcopy((scenes or {}).get(i, ep["shots"][i])) for i in order]
    for k, i in enumerate(order):
        if i in (scenes or {}):
            sc[k]["_own"] = True
    M = Mural(sc, cols=cols, gap=gap, drop=drop, keep=keep)
    adds = {pan[i]: v for i, v in (adds or {}).items()}
    cams = dict(cams or {})
    for i in alias:
        cams.setdefault(i, ep["shots"][i].get("cam"))
    cams = {i: c for i, c in cams.items()}
    beats = []

    def gl(s2, given=None):
        """Glide length: longer for longer trips across the wall."""
        a, b = M.steps[s2 - 1]["cam"], M.steps[s2]["cam"]
        d = math.hypot(b[1] - a[1], b[2] - a[2])
        g = max(given or 0, glide if d < 300 else 1.1 + d / 3500)
        return ("%.2f" % min(g, 2.6)).rstrip("0").rstrip(".")

    def cam_for(si):
        i = pan[si]
        return i, (M.cam(i, cams[si]) if si in cams else None)

    def need(i, c):
        return not M.steps or M.cur != i or (c is not None and c != M.steps[-1]["cam"])

    beat_adds = beat_adds or {}
    for bi, b in enumerate(ep["beats"]):
        frm, c = cam_for(b["visual"].get("from", 0))
        lines = [KICK.sub("", ln) for ln in b["lines"]]
        prefix = ""
        if bi in beat_adds:                                        # this beat draws more onto its panel (and may reframe it)
            els_b, cam_b = beat_adds[bi]
            if cam_b is not None:
                c = M.cam(frm, cam_b)
            if not M.steps:
                st = M.visit(frm, list(adds.get(frm, [])) + list(els_b), c)
            else:
                st = len(M.steps) - 1
                s2 = M.visit(frm, list(els_b) + (list(adds.get(frm, [])) if frm not in M.visited else []), c or (M.steps[-1]["cam"] if frm == M.cur else M.cam(frm)))
                prefix = "[go:%d|%s]" % (s2, gl(s2) if M.steps[s2 - 1]["cam"] != M.steps[s2]["cam"] else "0.8")
        elif not M.steps:
            st = M.visit(frm, adds.get(frm, []), c)
        elif need(frm, c):
            st = len(M.steps) - 1                                  # the beat opens on the last framing, then glides on its first words
            s2 = M.visit(frm, adds.get(frm, []) if frm not in M.visited else [], c)
            prefix = "[go:%d|%s]" % (s2, gl(s2))
        else:
            st = len(M.steps) - 1

        def rep(m):
            i, c2 = cam_for(int(float(m.group(1))))
            if not need(i, c2):
                return ""
            s2 = M.visit(i, adds.get(i, []) if i not in M.visited else [], c2)
            g = float(m.group(2)) if m.group(2) and float(m.group(2)) >= .8 else None
            return "[go:%d|%s]" % (s2, gl(s2, g))
        out = []
        for li, ln in enumerate(lines):
            pre = ""
            if li and (bi, li) in (line_adds or {}):              # this line draws more onto the panel it is on
                els_l, cam_l = line_adds[(bi, li)]
                i = M.cur
                c3 = M.cam(i, cam_l) if cam_l is not None else M.steps[-1]["cam"]
                s3 = M.visit(i, els_l, c3)
                pre = "[go:%d|%s]" % (s3, gl(s3) if M.steps[s3 - 1]["cam"] != M.steps[s3]["cam"] else "0.8")
            out.append(pre + GO.sub(rep, ln))
        out[0] = prefix + out[0]
        beats.append({"role": b["role"], "visual": {"from": st}, "lines": out})
    ep["beats"] = beats
    ep["shots"] = M.shots()
    return ep



# ================================================================== 16:9 walls (long form)
LW, LH = 1778, 1000                     # a 16:9 panel is the landscape frame
TALL_CAM = [.66, 500, 880]              # a tall (9:16) panel, framed whole: its drawing zone y 260..1420 above the caption band
TALL_GAP = 680                          # extra space beside a tall panel, so the zoomed-out camera does not see its neighbours
SENT = re.compile(r"(?:\[(?:d|p|gap|tune|sfx|beat|stamp|count|go):[^\]]*\])*\[act:")    # a sentence opens with [act:...] (and its tags)


def _keep(e, drop, keep):
    return not (e.get("k") in drop and not (keep and keep(e)))


def _bp(sc):
    """Base parameters of a scene (what BASE.* reads): everything but its elements, camera and private keys."""
    return {k: v for k, v in sc.items() if k not in ("els", "cam", "dir", "cont", "hop", "base", "note", "chapter") and not k.startswith("_")}


def inset(scene, s=None, crop=None, at=None, drop=TEXT, keep=None, base="dark", els=(), cam=None, edge="rgba(255,236,206,.2)", **bs):
    """A 9:16 scene from a Short shown through a window of a 16:9 panel.
    crop: [x, y, w, h] of the portrait frame to show (default its drawing zone, x 0..1000, y 260..1420); s: its scale (default:
    the window 740 units tall); at: the window's top left corner in the panel (default centred, lifted 40 above the middle so
    it clears the caption band). base/bs: the 16:9 panel's own background; els: 16:9 elements on the panel, around or over the
    window (labels, a timeline beside it). The old scene's text cards (para, num, title, q, cap) go, unless keep(e) keeps them;
    its build-ins play as in the Short, on the clock of the panel."""
    crop = list(crop or [0, 260, 1000, 1160])
    s = s or round(740 / crop[3], 4)
    w, h = crop[2] * s, crop[3] * s
    at = list(at or [round((LW - w) / 2), round((LH - h) / 2 - 40)])
    out = {"base": base, "els": list(els), "_inset": {"scene": copy.deepcopy(scene), "s": s, "crop": crop, "at": at, "drop": tuple(drop), "keep": keep, "edge": edge}}
    out.update(bs)
    if cam:
        out["cam"] = cam
    return out


def tall(scene, cam=None, drop=TEXT, keep=None):
    """A 9:16 scene from a Short hung on the wall as it is: a tall panel, 1000 x 1778, drawn exactly as in its Short.
    cam = [z, x, y] in the panel's own units (the point x, y at the centre of the picture); the default frames its whole drawing
    zone, zoomed out (TALL_CAM). Give later steps closer cams (cams= or beat_adds) to tilt down it: sky, ground, strata."""
    sc = copy.deepcopy(scene)
    sc["_tall"] = {"drop": tuple(drop), "keep": keep}
    sc["cam"] = list(cam or TALL_CAM)
    return sc


def card(n, title, kicker=None):
    """A chapter card on its own panel: the number large and faint, a kicker, a rule that draws itself, the title rising in."""
    size = min(108, int(1480 / max(1, .52 * len(title))))       # Newsreader 500: about half an em per character
    return {"base": "dark", "_card": True, "cam": [1, LW / 2, LH / 2], "els": [
        {"k": "glow", "x": 889, "y": 500, "r": 560, "kind": "lamp", "op": .2, "keepop": True, "in": 0, "dur": 1.4},
        {"k": "label", "x": 889, "y": 730, "t": "%02d" % n, "st": "big", "size": 560, "c": "#e8b87a", "op": .07, "halo": False, "keepop": True, "in": .1, "dur": 1.6},
        {"k": "cap", "x": 889, "y": 388, "t": kicker or "Chapter %d" % n, "c": "#e8b87a", "size": 26, "in": .25},
        {"k": "line", "p": [[739, 430], [1039, 430]], "c": "#e8b87a", "w": 2, "op": .9, "keepop": True, "fx": "draw", "dur": 1.0, "in": .45},
        {"k": "label", "x": 889, "y": 562, "t": title, "st": "serif", "size": size, "c": "#f5ecdc", "fx": "rise", "dur": 1.1, "in": .75},
    ]}


class Wall:
    """Panels hung in rows that snake (a meander: each row starts under the end of the last one and runs back the other way).
    Rows hold up to `cols` panels; a chapter card always starts a new row, so each chapter is a room of the wall. Panels may be
    16:9 (1778 x 1000) or tall (1000 x 1778); a row is as tall as its tallest panel and the others sit on its middle line."""
    def __init__(self, panels, rows, gap=220):
        self.sc, self.gap = panels, gap
        self.size = [(PW, PH) if p.get("_tall") else (LW, LH) for p in panels]
        self.pos, self.row = [None] * len(panels), [0] * len(panels)
        y, cx_end = 0.0, None
        for r, row in enumerate(rows):
            d = 1 if r % 2 == 0 else -1
            hmax = max(self.size[j][1] for j in row)
            cx = None
            for k, j in enumerate(row):
                w, h = self.size[j]
                if k == 0:
                    cx = cx_end if cx_end is not None else w / 2
                else:
                    pj = row[k - 1]
                    g = gap + (TALL_GAP if (panels[j].get("_tall") or panels[pj].get("_tall")) else 0)
                    cx += d * (self.size[pj][0] / 2 + g + w / 2)
                self.pos[j] = (round(cx - w / 2, 1), round(y + (hmax - h) / 2, 1)); self.row[j] = r
            cx_end = cx
            y += hmax + gap
        self.steps, self.visited, self.cur, self.drawn = [], [], None, set()

    def bbox(self):
        xs = [p[0] for p in self.pos] + [p[0] + s[0] for p, s in zip(self.pos, self.size)]
        ys = [p[1] for p in self.pos] + [p[1] + s[1] for p, s in zip(self.pos, self.size)]
        return [min(xs), min(ys), max(xs), max(ys)]

    def cam(self, j, cam=None):
        w, h = self.size[j]
        z, x, y = (cam or self.sc[j].get("cam") or [1, w / 2, h / 2])[:3]
        if not self.sc[j].get("_tall") and z >= 1:                # a 16:9 panel: the picture stays inside it (no bare wall at an edge)
            hx, hy = LW / 2 / z, LH / 2 / z
            x, y = min(max(x, hx), w - hx), min(max(y, hy), h - hy)
        ox, oy = self.pos[j]
        return [z, round(x + ox, 1), round(y + oy, 1)]

    def frame(self, j):
        sc = self.sc[j]; (ox, oy), (w, h) = self.pos[j], self.size[j]
        f = {"k": "panel", "ox": ox, "oy": oy, "w": w, "h": h, "base": sc.get("base", "dark"), "bs": _bp(sc), "els": [], "edge": "rgba(255,236,206,.16)", "in": -1}
        ins = sc.get("_inset")
        if ins:                                                    # the window: the old scene's own background, scaled and cropped
            p = ins["scene"]
            f["els"] = [{"k": "panel", "w": PW, "h": PH, "s": ins["s"], "crop": ins["crop"], "ox": ins["at"][0], "oy": ins["at"][1],
                         "base": p.get("base", "dark"), "bs": _bp(p), "els": [], "edge": ins["edge"], "r": 14, "in": -1}]
        return f

    def content(self, j):
        sc = self.sc[j]; (ox, oy), (w, h) = self.pos[j], self.size[j]
        els = copy.deepcopy(sc.get("els", []))
        if sc.get("_tall"):
            els = [e for e in els if _keep(e, sc["_tall"]["drop"], sc["_tall"]["keep"])]
        ins = sc.get("_inset")
        if ins:
            pe = [copy.deepcopy(e) for e in ins["scene"].get("els", []) if _keep(e, ins["drop"], ins["keep"])]
            els = [{"k": "panel", "w": PW, "h": PH, "s": ins["s"], "crop": ins["crop"], "ox": ins["at"][0], "oy": ins["at"][1], "base": "none", "els": pe, "r": 14}] + els
        return {"k": "panel", "ox": ox, "oy": oy, "w": w, "h": h, "base": "none", "els": els, "pn": j}

    def thread(self, a, b, at=.1):
        """The line drawn across the gap to the next panel of the wall (only between neighbours, once)."""
        if abs(a - b) != 1 or (min(a, b), max(a, b)) in self.drawn:
            return []
        self.drawn.add((min(a, b), max(a, b)))
        (ax, ay), (aw, ah), (bx, by), (bw, bh) = self.pos[a], self.size[a], self.pos[b], self.size[b]
        if self.row[a] == self.row[b]:
            y = round(ay + ah / 2, 1); x0, x1 = (ax + aw, bx) if bx > ax else (ax, bx + bw)
            p = [[x0, y], [x1, y]]
        else:
            x = round(ax + aw / 2, 1); y0, y1 = (ay + ah, by) if by > ay else (ay, by + bh)
            p = [[x, y0], [x, y1]]
        box = [min(p[0][0], p[1][0]) - 30, min(p[0][1], p[1][1]) - 30, max(p[0][0], p[1][0]) + 30, max(p[0][1], p[1][1]) + 30]
        return [{"k": "line", "p": p, "c": THREAD, "w": 4, "op": .8, "keepop": True, "fx": "draw", "dur": .8, "in": at, "box": box}]

    def visit(self, j, add=(), cam=None):
        """The next step of the take: the camera settles on panel j. Only what is new is listed (its content on the first visit,
        the thread to it, additions); everything already on the wall stays, built once."""
        new = []
        if j not in self.visited:
            new.append(self.content(j)); self.visited.append(j)
        if self.cur is not None and self.cur != j:
            new += self.thread(self.cur, j)
        if add:
            (ox, oy), (w, h) = self.pos[j], self.size[j]
            new.append({"k": "panel", "ox": ox, "oy": oy, "w": w, "h": h, "base": "none", "els": list(add), "pn": j})
        prev = self.steps[-1]["cam"] if self.steps else None
        c = cam or self.cam(j)
        s = {"base": "dark", "cam": c, "els": new, "cont": True, "dir": {"move": "hold"}}
        if prev:
            d = math.hypot(c[1] - prev[1], c[2] - prev[2])
            if d > 400:
                s["hop"] = round(min(.5, .08 + d / 7000), 3)
        self.steps.append(s); self.cur = j
        return len(self.steps) - 1


def _starts(lines):
    """Where each sentence of a beat starts: (line, position). Sentences open with [act:...] (house markup), else after . ? !"""
    out = []
    for li, ln in enumerate(lines):
        out.append((li, 0))
        ms = [m.start() for m in SENT.finditer(ln) if m.start() > 0]
        if not SENT.search(ln):
            ms = [m.end() for m in re.finditer(r"(?<=[.?!])\s+(?=\S)", ln)]
        out += [(li, p) for p in ms if ln[:p].strip()]
    return out


def wall(ep, scenes=None, keep=None, adds=None, cams=None, glide=1.4, alias=None, beat_adds=None, line_adds=None, cols=3, gap=220, rooms=True, hold=1):
    """A long film (16:9) as one continuous take across a wall. ep: shots (16:9 scenes, inset(...) or tall(...) reuses of Short
    scenes) and beats with [go:N|t] markers, as for remix(). A beat may carry "chapter": "Title" (and "chapter_kicker"): the wall
    gets a chapter card, hung at the start of a new row (rooms=True), and the beat opens with a glide to it; the card holds for
    the beat's first `hold` sentence(s), then the camera glides to the beat's own panel (unless a [go:] in those words already
    moved it; a one-sentence beat moves on as its last word ends). Panels are hung in the order the story first visits them.
    scenes / adds / cams / alias / beat_adds / line_adds: as for remix(), cams in the panel's own units (x, y = the centre)."""
    ep = copy.deepcopy(ep)
    alias = alias or {}
    shots = ep["shots"]
    root = lambda i: alias.get(i, i)
    order = [i for i in range(len(shots)) if i not in alias]
    sc = {i: copy.deepcopy((scenes or {}).get(i, shots[i])) for i in order}
    seq = []                                                       # the story's order of first visits: the wall is hung that way
    for bi, b in enumerate(ep["beats"]):
        if b.get("chapter"):
            seq.append(("card", bi))
        seq.append(("scene", root(int(float(b["visual"].get("from", 0))))))
        for ln in b["lines"]:
            seq += [("scene", root(int(float(m.group(1))))) for m in GO.finditer(ln)]
    units, seen = [], set()
    for u in seq + [("scene", i) for i in order]:
        if u not in seen:
            seen.add(u); units.append(u)
    rows, cur = [], []
    for k, u in enumerate(units):
        if cur and ((rooms and u[0] == "card") or len(cur) >= cols):
            rows.append(cur); cur = []
        cur.append(k)
    rows.append(cur)
    panels, nch = [], 0
    for u in units:
        if u[0] == "card":
            nch += 1; b = ep["beats"][u[1]]
            panels.append(card(nch, b["chapter"], b.get("chapter_kicker")))
        else:
            panels.append(sc[u[1]])
    M = Wall(panels, rows, gap)
    jof = {u: k for k, u in enumerate(units)}
    pan = {i: jof[("scene", root(i))] for i in range(len(shots))}
    adds = {pan[i]: v for i, v in (adds or {}).items()}
    cams = dict(cams or {})
    for i in alias:
        cams.setdefault(i, shots[i].get("cam"))

    def gl(s2, given=None):
        a, b = M.steps[s2 - 1]["cam"], M.steps[s2]["cam"]
        d = math.hypot(b[1] - a[1], b[2] - a[2])
        g = max(given or 0, glide if d < 300 else 1.2 + d / 3000)
        return ("%.2f" % min(g, 2.6)).rstrip("0").rstrip(".")

    def cam_for(si):
        j = pan[si]
        return j, (M.cam(j, cams[si]) if si in cams else None)

    def need(j, c):
        return not M.steps or M.cur != j or (c is not None and c != M.steps[-1]["cam"])

    def first(j):
        return list(adds.get(j, [])) if j not in M.visited else []

    beats, beat_adds, line_adds = [], beat_adds or {}, line_adds or {}
    for bi, b in enumerate(ep["beats"]):
        frm, c = cam_for(int(float(b["visual"].get("from", 0))))
        lines = [KICK.sub("", ln) for ln in b["lines"]]
        prefix, defer, moved = "", None, [False]
        els_b, cam_b = beat_adds.get(bi, ([], None))
        if cam_b is not None:
            c = M.cam(frm, cam_b)
        if b.get("chapter"):                                       # the chapter opens on its card
            cj = jof[("card", bi)]
            if not M.steps:
                st = M.visit(cj)
            else:
                st = len(M.steps) - 1; s2 = M.visit(cj); prefix = "[go:%d|%s]" % (s2, gl(s2))
            ss = _starts(lines)
            defer = ss[hold] if len(ss) > hold else (len(lines) - 1, None)
        elif bi in beat_adds:                                      # this beat draws more onto its panel (and may reframe it)
            if not M.steps:
                st = M.visit(frm, first(frm) + list(els_b), c)
            else:
                st = len(M.steps) - 1
                s2 = M.visit(frm, list(els_b) + first(frm), c or (M.steps[-1]["cam"] if frm == M.cur else M.cam(frm)))
                prefix = "[go:%d|%s]" % (s2, gl(s2) if M.steps[s2 - 1]["cam"] != M.steps[s2]["cam"] else "0.8")
        elif not M.steps:
            st = M.visit(frm, first(frm), c)
        elif need(frm, c):
            st = len(M.steps) - 1; s2 = M.visit(frm, first(frm), c); prefix = "[go:%d|%s]" % (s2, gl(s2))
        else:
            st = len(M.steps) - 1

        def rep(m):
            j, c2 = cam_for(int(float(m.group(1))))
            if not need(j, c2):
                return ""
            moved[0] = True
            s2 = M.visit(j, first(j), c2)
            g = float(m.group(2)) if m.group(2) and float(m.group(2)) >= .8 else None
            return "[go:%d|%s]" % (s2, gl(s2, g))

        def leave_card():                                          # from the chapter card to the beat's own panel
            if moved[0]:
                return ""
            moved[0] = True
            s3 = M.visit(frm, first(frm) + list(els_b), c)
            return "[go:%d|%s]" % (s3, gl(s3))

        out = []
        for li, ln in enumerate(lines):
            pre = ""
            if li and (bi, li) in line_adds:                       # this line draws more onto the panel it is on
                els_l, cam_l = line_adds[(bi, li)]
                c3 = M.cam(M.cur, cam_l) if cam_l is not None else M.steps[-1]["cam"]
                s3 = M.visit(M.cur, els_l, c3)
                pre = "[go:%d|%s]" % (s3, gl(s3) if M.steps[s3 - 1]["cam"] != M.steps[s3]["cam"] else "0.8")
            if defer and defer[0] == li:
                if defer[1] is None:                               # a one-sentence chapter beat: move on as its last word ends
                    body = GO.sub(rep, ln); out.append(pre + body + leave_card())
                else:
                    head = GO.sub(rep, ln[:defer[1]]); tail = ln[defer[1]:]
                    lc = leave_card(); out.append(pre + head + lc + GO.sub(rep, tail))
                continue
            out.append(pre + GO.sub(rep, ln))
        out[0] = prefix + out[0]
        nb = {k: v for k, v in b.items() if k not in ("lines", "visual")}
        nb.update(visual={"from": st}, lines=out)
        beats.append(nb)
    ep["beats"] = beats
    ep["shots"] = M.steps
    ep["wall"] = {"panels": [M.frame(j) for j in range(len(panels))], "bbox": M.bbox()}
    return ep
