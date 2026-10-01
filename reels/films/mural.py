"""The mural: a whole film as one continuous take across a wall of full-frame panels.

Every scene of a film (a map, a model, a cross-section, a sky) hangs on one wall as a framed panel. The camera never cuts:
it lifts off one panel and settles on the next as the narrator moves on, a thread drawing itself between them, and each
panel's drawing builds itself when the camera arrives (the scene's own animations, timed from the arrival).

remix(ep, scenes={i: new_scene}, ...) turns an existing film (shots + beats with [go:] markers) into the mural version:
scene i is shot i of the film (or its replacement), beats keep their words, [k:] kicker titles go, every cut becomes a glide.
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
